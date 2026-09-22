#!/usr/bin/env python3
"""
TaskFlow - Projeto Final (interface em modo texto interativo, via curses)

Arquitetura:
- TaskFlowApp: toda a logica de negocio (colunas, undo/redo, avisos).
  Nao imprime nada nem le input diretamente -- recebe parametros e
  devolve listas de strings com o resultado. Isso deixa a logica
  testavel isoladamente da interface (ver testes/).
- Funcoes tela_*: camada de interface com curses, que desenha o menu,
  le entradas do usuario e chama os metodos de TaskFlowApp.

curses e biblioteca padrao do Python em Linux/Mac. No Windows, requer
`pip install windows-curses`.
"""

import copy
import curses
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modulo1_utils.datas import parse_data
from modulo1_utils.prioridade import calcular_urgencia
from modulo3_listas.lista_dupla import ListaDuplamenteEncadeada
from modulo4_pilhas.undo_redo import GerenciadorUndoRedo
from modulo5_filas.fila_prioridade import FilaPrioridade


COLUNAS = ("a_fazer", "fazendo", "concluido")
NOMES_COLUNAS = {"a_fazer": "A Fazer", "fazendo": "Fazendo", "concluido": "Concluido"}


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

    def adicionar_tarefa(self, titulo: str, prazo_texto: str, prioridade: str) -> list:
        titulo = titulo.strip()
        prioridade = prioridade.strip().lower()

        if not titulo:
            return ["Erro: titulo nao pode ser vazio."]
        try:
            parse_data(prazo_texto.strip())
        except ValueError:
            return ["Erro: data invalida. Use o formato AAAA-MM-DD."]
        if prioridade not in ("baixa", "media", "alta"):
            return ["Erro: prioridade invalida (use baixa, media ou alta)."]

        self._antes_de_alterar()
        tarefa = {
            "id": self.proximo_id,
            "titulo": titulo,
            "prazo": prazo_texto.strip(),
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

    def colunas_disponiveis_texto(self) -> list:
        return [f"{i + 1}) {NOMES_COLUNAS[c]}" for i, c in enumerate(COLUNAS)]

    def mover_tarefa(self, id_texto: str, escolha_coluna_texto: str) -> list:
        try:
            id_tarefa = int(id_texto.strip())
        except ValueError:
            return ["Erro: ID invalido."]

        coluna_atual, tarefa = self._encontrar_tarefa(id_tarefa)
        if tarefa is None:
            return ["Erro: tarefa nao encontrada."]

        try:
            nova_coluna = COLUNAS[int(escolha_coluna_texto.strip()) - 1]
        except (ValueError, IndexError):
            return ["Erro: opcao de coluna invalida."]

        if nova_coluna == coluna_atual:
            return ["A tarefa ja esta nessa coluna."]

        self._antes_de_alterar()
        self.colunas[coluna_atual].remover(id_tarefa)
        tarefa["status"] = nova_coluna
        self.colunas[nova_coluna].inserir(tarefa)
        return [f"Tarefa #{id_tarefa} movida para {NOMES_COLUNAS[nova_coluna]}."]

    def marcar_concluida(self, id_texto: str) -> list:
        try:
            id_tarefa = int(id_texto.strip())
        except ValueError:
            return ["Erro: ID invalido."]

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


def tela_adicionar(stdscr, app: TaskFlowApp) -> list:
    stdscr.erase()
    stdscr.addstr(0, 2, "=== Adicionar tarefa ===", curses.A_BOLD)
    titulo = ler_texto(stdscr, "Titulo: ", 2)
    prazo = ler_texto(stdscr, "Prazo (AAAA-MM-DD): ", 3)
    prioridade = ler_texto(stdscr, "Prioridade (baixa/media/alta): ", 4)
    return app.adicionar_tarefa(titulo, prazo, prioridade)


def tela_mover(stdscr, app: TaskFlowApp) -> list:
    stdscr.erase()
    stdscr.addstr(0, 2, "=== Mover tarefa ===", curses.A_BOLD)
    id_texto = ler_texto(stdscr, "ID da tarefa: ", 2)

    y = 4
    stdscr.addstr(y, 2, "Colunas disponiveis:")
    for i, linha in enumerate(app.colunas_disponiveis_texto()):
        stdscr.addstr(y + 1 + i, 4, linha)

    escolha = ler_texto(stdscr, "Mover para (numero): ", y + 1 + len(COLUNAS) + 1)
    return app.mover_tarefa(id_texto, escolha)


def tela_concluir(stdscr, app: TaskFlowApp) -> list:
    stdscr.erase()
    stdscr.addstr(0, 2, "=== Marcar tarefa como concluida ===", curses.A_BOLD)
    id_texto = ler_texto(stdscr, "ID da tarefa: ", 2)
    return app.marcar_concluida(id_texto)


def main_curses(stdscr):
    curses.curs_set(0)
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
        if tecla not in (curses.KEY_ENTER, ord("\n"), ord("\r")):
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
