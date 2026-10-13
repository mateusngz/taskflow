#!/usr/bin/env python3
"""
TaskFlow - Projeto Final (interface em modo texto interativo, via curses)

Arquitetura:
- TaskFlowApp: toda a logica de negocio (colunas, undo/redo, avisos).
  Nao imprime nada nem le input diretamente -- recebe parametros ja
  validados e devolve listas de strings com o resultado. Isso deixa a
  logica testavel isoladamente da interface (ver testes/).
- Funcoes tela_* e os seletores (selecionar_opcao, selecionar_tarefa,
  selecionar_data): camada de interface com curses. Em vez de pedir pro
  usuario digitar um ID ou uma data em texto livre, mostram uma lista
  ou um calendario navegavel por setas -- reduz erro de digitacao e
  deixa a interface mais parecida com ferramentas como ncdu/htop.

curses e biblioteca padrao do Python em Linux/Mac. No Windows, requer
`pip install windows-curses` (ja declarado como dependencia condicional
no pyproject.toml).
"""

import calendar as calendar_mod
import copy
import curses
import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modulo1_utils.datas import parse_data
from modulo1_utils.prioridade import calcular_urgencia
from modulo3_listas.lista_dupla import ListaDuplamenteEncadeada
from modulo4_pilhas.undo_redo import GerenciadorUndoRedo
from modulo5_filas.fila_prioridade import FilaPrioridade


COLUNAS = ("a_fazer", "fazendo", "concluido")
NOMES_COLUNAS = {"a_fazer": "A Fazer", "fazendo": "Fazendo", "concluido": "Concluido"}
MESES_PT = [
    "Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]


def add_meses(d: date, delta: int) -> date:
    """Soma (ou subtrai) meses a uma data, ajustando o dia se o mes
    novo tiver menos dias (ex.: 31/jan + 1 mes -> 28/fev ou 29/fev)."""
    mes_total = d.month - 1 + delta
    ano = d.year + mes_total // 12
    mes = mes_total % 12 + 1
    ultimo_dia = calendar_mod.monthrange(ano, mes)[1]
    dia = min(d.day, ultimo_dia)
    return date(ano, mes, dia)


# ============================================================
# CAMADA DE LOGICA (sem I/O de terminal)
# ============================================================

class TaskFlowApp:
    def __init__(self):
        self.colunas = {c: ListaDuplamenteEncadeada() for c in COLUNAS}
        self.proximo_id = 1
        self.undo_redo = GerenciadorUndoRedo()

    def _snapshot(self) -> dict:
        return {c: copy.deepcopy(self.colunas[c].percorrer()) for c in COLUNAS}

    def _restaurar(self, snapshot: dict) -> None:
        for c in COLUNAS:
            nova_lista = ListaDuplamenteEncadeada()
            for tarefa in snapshot[c]:
                nova_lista.inserir(tarefa)
            self.colunas[c] = nova_lista

    def _antes_de_alterar(self) -> None:
        self.undo_redo.registrar_estado_anterior(self._snapshot())

    def _encontrar_tarefa(self, id_tarefa: int):
        for c in COLUNAS:
            tarefa = self.colunas[c].buscar(id_tarefa)
            if tarefa is not None:
                return c, tarefa
        return None, None

    def todas_tarefas(self) -> list:
        """Lista achatada de todas as tarefas, de todas as colunas,
        cada uma ja com o campo 'status' indicando a coluna atual --
        usada pela interface pra montar a lista de selecao."""
        todas = []
        for c in COLUNAS:
            todas.extend(self.colunas[c].percorrer())
        return todas

    def adicionar_tarefa(self, titulo: str, prazo_iso: str, prioridade: str) -> list:
        titulo = titulo.strip()
        if not titulo:
            return ["Erro: titulo nao pode ser vazio."]
        try:
            parse_data(prazo_iso)
        except ValueError:
            return ["Erro: data invalida."]
        if prioridade not in ("baixa", "media", "alta"):
            return ["Erro: prioridade invalida."]

        self._antes_de_alterar()
        tarefa = {
            "id": self.proximo_id,
            "titulo": titulo,
            "prazo": prazo_iso,
            "prioridade": prioridade,
            "status": "a_fazer",
        }
        self.colunas["a_fazer"].inserir(tarefa)
        msg = [f"Tarefa #{self.proximo_id} adicionada em 'A Fazer'."]
        self.proximo_id += 1
        return msg

    def listar_tarefas(self) -> list:
        linhas = []
        for c in COLUNAS:
            linhas.append(f"-- {NOMES_COLUNAS[c]} --")
            tarefas = self.colunas[c].percorrer()
            if not tarefas:
                linhas.append("  (vazio)")
            for t in tarefas:
                linhas.append(
                    f"  #{t['id']} {t['titulo']} | prazo: {t['prazo']} | prioridade: {t['prioridade']}"
                )
            linhas.append("")
        return linhas

    def mover_tarefa(self, id_tarefa: int, nova_coluna: str) -> list:
        coluna_atual, tarefa = self._encontrar_tarefa(id_tarefa)
        if tarefa is None:
            return ["Erro: tarefa nao encontrada."]
        if nova_coluna not in COLUNAS:
            return ["Erro: coluna invalida."]
        if nova_coluna == coluna_atual:
            return ["A tarefa ja esta nessa coluna."]

        self._antes_de_alterar()
        self.colunas[coluna_atual].remover(id_tarefa)
        tarefa["status"] = nova_coluna
        self.colunas[nova_coluna].inserir(tarefa)
        return [f"Tarefa #{id_tarefa} movida para {NOMES_COLUNAS[nova_coluna]}."]

    def marcar_concluida(self, id_tarefa: int) -> list:
        coluna_atual, tarefa = self._encontrar_tarefa(id_tarefa)
        if tarefa is None:
            return ["Erro: tarefa nao encontrada."]
        if coluna_atual == "concluido":
            return ["Essa tarefa ja esta concluida."]

        self._antes_de_alterar()
        self.colunas[coluna_atual].remover(id_tarefa)
        tarefa["status"] = "concluido"
        self.colunas["concluido"].inserir(tarefa)
        return [f"Tarefa #{id_tarefa} marcada como concluida."]

    def desfazer(self) -> list:
        anterior = self.undo_redo.desfazer(self._snapshot())
        if anterior is None:
            return ["Nao ha o que desfazer."]
        self._restaurar(anterior)
        return ["Ultima acao desfeita."]

    def refazer(self) -> list:
        proximo = self.undo_redo.refazer(self._snapshot())
        if proximo is None:
            return ["Nao ha o que refazer."]
        self._restaurar(proximo)
        return ["Acao refeita."]

    def ver_avisos(self) -> list:
        fila = FilaPrioridade()
        hoje = date.today()

        for c in ("a_fazer", "fazendo"):
            for tarefa in self.colunas[c].percorrer():
                prazo = parse_data(tarefa["prazo"])
                urgencia = calcular_urgencia(prazo, tarefa["prioridade"], hoje)
                fila.enfileirar(tarefa, urgencia)

        if fila.vazia():
            return ["Nenhuma tarefa pendente para avisar."]

        linhas = ["-- Avisos (da mais urgente para a menos urgente) --"]
        while not fila.vazia():
            tarefa = fila.desenfileirar()
            linhas.append(f"  #{tarefa['id']} {tarefa['titulo']} | prazo: {tarefa['prazo']}")
        return linhas


# ============================================================
# CAMADA DE INTERFACE (curses)
# ============================================================

MENU_ITENS = [
    ("Adicionar tarefa", "adicionar"),
    ("Listar tarefas", "listar"),
    ("Mover tarefa entre colunas", "mover"),
    ("Marcar tarefa como concluida", "concluir"),
    ("Desfazer ultima acao", "desfazer"),
    ("Refazer", "refazer"),
    ("Ver avisos de tarefas urgentes", "avisos"),
    ("Sair", "sair"),
]

ENTER_KEYS = (curses.KEY_ENTER, ord("\n"), ord("\r"))
ESC_KEY = 27


def desenhar_menu(stdscr, indice: int, ultima_mensagem: list) -> None:
    stdscr.erase()
    altura, largura = stdscr.getmaxyx()

    titulo = "=== TaskFlow ==="
    stdscr.addstr(0, max(0, (largura - len(titulo)) // 2), titulo, curses.A_BOLD)

    for i, (label, _) in enumerate(MENU_ITENS):
        y = 2 + i
        if y >= altura - 1:
            break
        texto = f"{'>' if i == indice else ' '} {label}"
        if i == indice:
            stdscr.addstr(y, 2, texto, curses.A_REVERSE)
        else:
            stdscr.addstr(y, 2, texto)

    y_msg = 2 + len(MENU_ITENS) + 1
    if ultima_mensagem and y_msg < altura - 2:
        for i, linha in enumerate(ultima_mensagem):
            if y_msg + i >= altura - 2:
                break
            stdscr.addstr(y_msg + i, 2, linha[: max(0, largura - 4)], curses.A_DIM)

    rodape = "setas: navegar | enter: selecionar | q: sair"
    stdscr.addstr(altura - 1, 2, rodape[: max(0, largura - 3)])
    stdscr.refresh()


def ler_texto(stdscr, prompt: str, y: int) -> str:
    altura, largura = stdscr.getmaxyx()
    stdscr.addstr(y, 2, prompt)
    stdscr.clrtoeol()
    stdscr.refresh()
    curses.echo()
    curses.curs_set(1)
    largura_campo = max(1, largura - len(prompt) - 6)
    try:
        bruto = stdscr.getstr(y, 2 + len(prompt) + 1, largura_campo)
        texto = bruto.decode("utf-8", errors="ignore")
    finally:
        curses.noecho()
        curses.curs_set(0)
    return texto.strip()


def mostrar_e_esperar(stdscr, linhas: list, titulo_tela: str = "") -> None:
    stdscr.erase()
    altura, largura = stdscr.getmaxyx()
    y = 0
    if titulo_tela:
        stdscr.addstr(0, 2, titulo_tela, curses.A_BOLD)
        y = 2
    for linha in linhas:
        if y >= altura - 2:
            stdscr.addstr(altura - 2, 2, "(mais itens do que cabem na tela...)")
            break
        stdscr.addstr(y, 2, linha[: max(0, largura - 4)])
        y += 1
    stdscr.addstr(altura - 1, 2, "Pressione qualquer tecla para voltar...")
    stdscr.refresh()
    stdscr.getch()


def selecionar_opcao(stdscr, titulo: str, opcoes: list, y_inicio: int = 2):
    """Lista navegavel generica. Retorna a string escolhida, ou None
    se o usuario cancelar com Esc."""
    indice = 0
    while True:
        stdscr.erase()
        altura, largura = stdscr.getmaxyx()
        stdscr.addstr(0, 2, titulo[: max(0, largura - 4)], curses.A_BOLD)

        for i, opcao in enumerate(opcoes):
            y = y_inicio + i
            if y >= altura - 1:
                break
            texto = f"{'>' if i == indice else ' '} {opcao}"
            if i == indice:
                stdscr.addstr(y, 2, texto[: max(0, largura - 4)], curses.A_REVERSE)
            else:
                stdscr.addstr(y, 2, texto[: max(0, largura - 4)])

        rodape = "setas: navegar | enter: selecionar | esc: cancelar"
        stdscr.addstr(altura - 1, 2, rodape[: max(0, largura - 3)])
        stdscr.refresh()

        tecla = stdscr.getch()
        if tecla in (curses.KEY_UP, ord("k")):
            indice = (indice - 1) % len(opcoes)
        elif tecla in (curses.KEY_DOWN, ord("j")):
            indice = (indice + 1) % len(opcoes)
        elif tecla in ENTER_KEYS:
            return opcoes[indice]
        elif tecla == ESC_KEY:
            return None


def selecionar_tarefa(stdscr, titulo: str, tarefas: list):
    """Lista navegavel de tarefas, mostrando id, titulo, prazo,
    prioridade e coluna atual. Retorna o dict da tarefa escolhida, ou
    None se a lista estiver vazia ou o usuario cancelar."""
    if not tarefas:
        mostrar_e_esperar(stdscr, ["Nenhuma tarefa disponivel."], titulo)
        return None

    indice = 0
    scroll = 0
    while True:
        stdscr.erase()
        altura, largura = stdscr.getmaxyx()
        stdscr.addstr(0, 2, titulo[: max(0, largura - 4)], curses.A_BOLD)

        area_visivel = max(1, altura - 4)
        if indice < scroll:
            scroll = indice
        elif indice >= scroll + area_visivel:
            scroll = indice - area_visivel + 1

        for offset, t in enumerate(tarefas[scroll: scroll + area_visivel]):
            i = scroll + offset
            y = 2 + offset
            coluna = NOMES_COLUNAS.get(t.get("status"), "?")
            linha = f"#{t['id']} {t['titulo']} | {t['prazo']} | {t['prioridade']} | {coluna}"
            texto = f"{'>' if i == indice else ' '} {linha}"
            if i == indice:
                stdscr.addstr(y, 2, texto[: max(0, largura - 4)], curses.A_REVERSE)
            else:
                stdscr.addstr(y, 2, texto[: max(0, largura - 4)])

        rodape = "setas: navegar | enter: selecionar | esc: cancelar"
        stdscr.addstr(altura - 1, 2, rodape[: max(0, largura - 3)])
        stdscr.refresh()

        tecla = stdscr.getch()
        if tecla in (curses.KEY_UP, ord("k")):
            indice = (indice - 1) % len(tarefas)
        elif tecla in (curses.KEY_DOWN, ord("j")):
            indice = (indice + 1) % len(tarefas)
        elif tecla in ENTER_KEYS:
            return tarefas[indice]
        elif tecla == ESC_KEY:
            return None


def selecionar_data(stdscr, titulo: str = "Selecione a data"):
    """Calendario navegavel por setas. Retorna a data escolhida em
    formato ISO (AAAA-MM-DD), ou None se o usuario cancelar com Esc."""
    atual = date.today()

    while True:
        stdscr.erase()
        altura, largura = stdscr.getmaxyx()
        stdscr.addstr(0, 2, titulo[: max(0, largura - 4)], curses.A_BOLD)

        cabecalho = f"{MESES_PT[atual.month - 1]} {atual.year}"
        stdscr.addstr(2, 2, cabecalho, curses.A_BOLD)
        stdscr.addstr(3, 2, "Dom Seg Ter Qua Qui Sex Sab")

        cal = calendar_mod.Calendar(firstweekday=6)  # semana comeca no domingo
        semanas = cal.monthdayscalendar(atual.year, atual.month)

        y = 4
        for semana in semanas:
            x = 2
            for dia_num in semana:
                if dia_num == 0:
                    x += 4
                    continue
                texto = f"{dia_num:>3} "
                if dia_num == atual.day:
                    stdscr.addstr(y, x, texto, curses.A_REVERSE)
                else:
                    stdscr.addstr(y, x, texto)
                x += 4
            y += 1

        rodape = "setas: dia | n/p: mes | enter: confirmar | esc: cancelar"
        stdscr.addstr(altura - 1, 2, rodape[: max(0, largura - 3)])
        stdscr.refresh()

        tecla = stdscr.getch()
        if tecla == curses.KEY_LEFT:
            atual -= timedelta(days=1)
        elif tecla == curses.KEY_RIGHT:
            atual += timedelta(days=1)
        elif tecla == curses.KEY_UP:
            atual -= timedelta(days=7)
        elif tecla == curses.KEY_DOWN:
            atual += timedelta(days=7)
        elif tecla in (ord("n"), curses.KEY_NPAGE):
            atual = add_meses(atual, 1)
        elif tecla in (ord("p"), curses.KEY_PPAGE):
            atual = add_meses(atual, -1)
        elif tecla in ENTER_KEYS:
            return atual.isoformat()
        elif tecla == ESC_KEY:
            return None


def tela_adicionar(stdscr, app: TaskFlowApp) -> list:
    stdscr.erase()
    stdscr.addstr(0, 2, "=== Adicionar tarefa ===", curses.A_BOLD)
    titulo = ler_texto(stdscr, "Titulo: ", 2)
    if not titulo.strip():
        return ["Titulo nao pode ser vazio. Operacao cancelada."]

    prazo_iso = selecionar_data(stdscr, "=== Prazo da tarefa ===")
    if prazo_iso is None:
        return ["Operacao cancelada."]

    prioridade = selecionar_opcao(stdscr, "=== Prioridade ===", ["baixa", "media", "alta"])
    if prioridade is None:
        return ["Operacao cancelada."]

    return app.adicionar_tarefa(titulo, prazo_iso, prioridade)


def tela_mover(stdscr, app: TaskFlowApp) -> list:
    tarefa = selecionar_tarefa(stdscr, "=== Mover tarefa - selecione ===", app.todas_tarefas())
    if tarefa is None:
        return []

    candidatas = [c for c in COLUNAS if c != tarefa.get("status")]
    nomes = [NOMES_COLUNAS[c] for c in candidatas]
    escolha_nome = selecionar_opcao(
        stdscr,
        f"Mover '{tarefa['titulo']}' (atual: {NOMES_COLUNAS[tarefa['status']]}) para:",
        nomes,
    )
    if escolha_nome is None:
        return ["Operacao cancelada."]

    nova_coluna = candidatas[nomes.index(escolha_nome)]
    return app.mover_tarefa(tarefa["id"], nova_coluna)


def tela_concluir(stdscr, app: TaskFlowApp) -> list:
    pendentes = [t for t in app.todas_tarefas() if t.get("status") != "concluido"]
    tarefa = selecionar_tarefa(stdscr, "=== Marcar como concluida - selecione ===", pendentes)
    if tarefa is None:
        return []
    return app.marcar_concluida(tarefa["id"])


def main_curses(stdscr):
    curses.curs_set(0)
    if hasattr(curses, "set_escdelay"):
        try:
            curses.set_escdelay(25)  # Esc responde mais rapido (padrao e ~1s)
        except curses.error:
            pass

    app = TaskFlowApp()
    indice = 0
    ultima_mensagem = []

    while True:
        desenhar_menu(stdscr, indice, ultima_mensagem)
        tecla = stdscr.getch()

        if tecla in (curses.KEY_UP, ord("k")):
            indice = (indice - 1) % len(MENU_ITENS)
            continue
        if tecla in (curses.KEY_DOWN, ord("j")):
            indice = (indice + 1) % len(MENU_ITENS)
            continue
        if tecla == ord("q"):
            break
        if tecla not in ENTER_KEYS:
            continue

        acao = MENU_ITENS[indice][1]
        ultima_mensagem = []

        if acao == "sair":
            break
        elif acao == "adicionar":
            ultima_mensagem = tela_adicionar(stdscr, app)
        elif acao == "listar":
            mostrar_e_esperar(stdscr, app.listar_tarefas(), "=== Tarefas ===")
        elif acao == "mover":
            ultima_mensagem = tela_mover(stdscr, app)
        elif acao == "concluir":
            ultima_mensagem = tela_concluir(stdscr, app)
        elif acao == "desfazer":
            ultima_mensagem = app.desfazer()
        elif acao == "refazer":
            ultima_mensagem = app.refazer()
        elif acao == "avisos":
            mostrar_e_esperar(stdscr, app.ver_avisos(), "=== Avisos ===")


def main():
    curses.wrapper(main_curses)


if __name__ == "__main__":
    main()
