# 0003 — Colunas do Kanban como lista duplamente encadeada

## Contexto

O Módulo 3 pede a implementação de listas em array e em encadeamento
(simples e duplo). O projeto final precisa escolher qual versão usar de
fato nas colunas do Kanban (A Fazer / Fazendo / Concluído).

## Decisão

Usar `ListaDuplamenteEncadeada` (Módulo 3) como estrutura real das
colunas no app integrado.

## Consequências

- Permite navegar a lista nos dois sentidos (`percorrer(reverso=True)`)
  sem custo adicional, o que seria útil para funcionalidades futuras
  como "ver as tarefas mais recentes primeiro".
- Mover uma tarefa de posição (remover + reinserir) fica direto: o nó
  já conhece seu vizinho anterior, sem precisar percorrer a lista desde
  o início para achar quem vem antes dele.
- Em troca, cada nó gasta mais memória que uma lista simples (guarda
  dois ponteiros — `anterior` e `proximo` — em vez de um).
- As versões com array e lista encadeada simples (`lista_array.py`,
  `lista_encadeada.py`) também foram implementadas e testadas, mas
  ficam como comparação didática — não estão plugadas no app final. A
  tabela de complexidade comparando as três está em
  `modulo3_listas/README.md`.
