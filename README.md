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

## Como instalar e executar

```bash
git clone <url-do-seu-repositorio>
cd taskflow
pip install --user .
```

Isso instala o comando `taskflow` disponível globalmente no seu terminal
(não precisa mais chamar `python3` nem apontar pra pasta do projeto):

```bash
taskflow
```

> Se o comando `taskflow` não for reconhecido depois de instalar, o
> diretório de scripts do Python pode não estar no seu `PATH`. Rode
> `python3 -m site --user-base` para achar o caminho e adicione a
> subpasta `bin` dele ao seu `PATH` (no fish: `fish_add_path
> ~/.local/bin`, ajustando o caminho retornado).

**Alternativa sem instalar nada:** também dá pra rodar direto do
repositório, sem `pip install`:

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
