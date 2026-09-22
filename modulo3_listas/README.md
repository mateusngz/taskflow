# Módulo 3 — Listas

## O que este módulo entrega

As colunas do Kanban (**A Fazer**, **Fazendo**, **Concluído**) implementadas
como TAD Lista, em duas versões, para comparação:

- `lista_array.py` — lista sequencial usando array (lista Python de
  tamanho fixo simulado, sem usar `append`/`insert` prontos do Python).
- `lista_encadeada.py` — lista com encadeamento simples (classe `No` com
  `dado` e `proximo`).
- `lista_dupla.py` — extensão para lista duplamente encadeada (`anterior`
  e `proximo`) — usada para permitir mover uma tarefa entre colunas ou
  reordenar prioridade dentro da coluna.

## Interface pública (igual nas três versões)

| Operação | Descrição |
|---|---|
| `inserir(tarefa, posicao=None)` | insere no fim, ou em uma posição específica |
| `remover(id_tarefa)` | remove pelo id |
| `buscar(id_tarefa)` | retorna a tarefa ou None |
| `mover(id_tarefa, nova_posicao)` | reordena dentro da lista |
| `percorrer()` | retorna/imprime todos os elementos em ordem |

## Complexidade a preencher (depois de implementar)

| Operação | Array | Encadeada simples | Duplamente encadeada |
|---|---|---|---|
| Inserir no fim | ? | ? | ? |
| Inserir no início | ? | ? | ? |
| Remover por id | ? | ? | ? |
| Buscar por id | ? | ? | ? |
| Mover (reordenar) | ? | ? | ? |

> Preencha esta tabela com O(...) depois de implementar — é exatamente o
> que o roteiro pede como "Entregável 3".

## TODO

- [ ] Implementar `lista_array.py`
- [ ] Implementar `lista_encadeada.py`
- [ ] Implementar `lista_dupla.py`
- [ ] Preencher a tabela de complexidade
