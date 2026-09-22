# TaskFlow

Gerenciador de tarefas estilo Kanban/agenda, desenvolvido como trabalho da
disciplina **Algoritmos e Estrutura de Dados I** (Engenharia de Software).

O projeto é construído incrementalmente ao longo do semestre: cada módulo do
roteiro da disciplina implementa uma parte do sistema, até chegar no
**projeto final**, que integra tudo em uma única aplicação de terminal (CLI).

## Ideia geral

O TaskFlow organiza tarefas em colunas (A Fazer / Fazendo / Concluído),
permite desfazer/refazer ações e avisa sobre tarefas com prazo próximo —
como um Kanban simples que você usaria de verdade.

## Linguagem

Python 3 (sem tipagem/alocação manual — as decisões sobre isso são
discutidas nos relatórios de cada módulo, quando aplicável).

## Estrutura do repositório

| Pasta | Módulo do roteiro | Conteúdo |
|---|---|---|
| `modulo1_utils/` | Módulo 1 — Modularização | Funções utilitárias (datas, prioridade, árvore de subtarefas) |
| `modulo2_tad/` | Módulo 2 — TAD e memória | TAD `Tarefa`, versão estática e dinâmica |
| `modulo3_listas/` | Módulo 3 — Listas | Colunas do Kanban: lista com array e lista encadeada (simples/dupla) |
| `modulo4_pilhas/` | Módulo 4 — Pilhas | Pilha de undo/redo |
| `modulo5_filas/` | Módulo 5 — Filas | Fila de lembretes (FIFO) e fila de prioridade |
| `projeto_final/` | Módulo 6 — Projeto final | Aplicação integrada (CLI) |
| `testes/` | — | Testes de cada módulo |

Cada pasta de módulo tem seu próprio `README.md` com o relatório técnico
(interface pública do TAD/estrutura e análise de complexidade das operações).

## Documentação de arquitetura

- [`docs/ARQUITETURA.md`](./docs/ARQUITETURA.md) — visão geral do sistema,
  diagrama de componentes e por que não há documentação de API (o
  TaskFlow não expõe rotas/endpoints).
- [`docs/adr/`](./docs/adr/) — decisões técnicas importantes (linguagem,
  interface de terminal, estrutura de dados das colunas, estratégia de
  undo/redo), cada uma com contexto, decisão e consequências.

## Como instalar e executar

```bash
git clone https://github.com/mateusngz/taskflow.git
cd taskflow
```

**Recomendado — instalar com `pipx`** (funciona em qualquer distro,
inclusive as que bloqueiam `pip install` direto no sistema, como Arch,
CachyOS e Manjaro):

```bash
# se ainda não tiver o pipx instalado:
# Arch/CachyOS/Manjaro:  sudo pacman -S python-pipx
# Debian/Ubuntu:         sudo apt install pipx
# Fedora:                sudo dnf install pipx

pipx install .
pipx ensurepath
```

Reinicie o terminal depois do `pipx ensurepath` (ou rode `exec $SHELL`)
pra garantir que o comando `taskflow` fique disponível.

**No Windows:**

```powershell
python -m pip install --user pipx
python -m pipx ensurepath
```

Feche e abra o terminal de novo, depois:

```powershell
pipx install .
```

O pacote `windows-curses` (necessário pra interface funcionar no
Windows, já que `curses` não vem por padrão nesse sistema) é instalado
automaticamente junto — não precisa fazer nada extra.

**Alternativa — `pip` tradicional:**

```bash
pip install --user .
```

> Se aparecer o erro `externally-managed-environment`, sua distro
> bloqueia instalação direta via pip (comportamento padrão em Arch e
> derivadas) — use o `pipx` acima em vez disso.

Depois de instalado (por qualquer um dos dois métodos), o comando fica
disponível globalmente:

```bash
taskflow
```

> Se o comando `taskflow` não for reconhecido mesmo depois de instalar,
> o diretório de scripts pode não estar no seu `PATH`. Com `pipx`, rode
> `pipx ensurepath` e reinicie o terminal. Com `pip --user`, rode
> `python3 -m site --user-base` para achar o caminho e adicione a
> subpasta `bin` dele ao seu `PATH` (no fish: `fish_add_path
> ~/.local/bin`, ajustando o caminho retornado).

**Alternativa sem instalar nada:** também dá pra rodar direto do
repositório, sem instalar:

```bash
python3 projeto_final/main.py
```

## Como rodar os testes

```bash
python3 -m unittest discover testes
```

## Status do desenvolvimento

- [x] Módulo 1 — Modularização
- [x] Módulo 2 — TAD e memória
- [x] Módulo 3 — Listas
- [x] Módulo 4 — Pilhas
- [x] Módulo 5 — Filas
- [x] Módulo 6 — Projeto final (funcional; relatórios/complexidade ainda a revisar)

## Autor

Mateus — Engenharia de Software
