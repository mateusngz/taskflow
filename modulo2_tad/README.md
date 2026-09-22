# Módulo 2 — TAD e Memória

## TAD: Tarefa

**Interface pública (o que o usuário do TAD pode fazer, sem saber como é implementado):**

- `criar(id, titulo, prazo, prioridade)` → cria uma nova tarefa
- `editar(campo, valor)` → altera um campo da tarefa
- `marcar_concluida()` → muda o status para "concluído"
- `to_dict()` → retorna os dados da tarefa como dicionário (para exibir/salvar)

## Duas versões

- `tarefa_estatica.py` — as tarefas ficam em um array de tamanho fixo
  pré-alocado (lista Python usada como array de tamanho fixo, sem
  `append`/`pop` — simula a limitação de um array estático em C).
- `tarefa_dinamica.py` — cada tarefa é um objeto criado sob demanda,
  sem limite de quantidade pré-definido.

## Sobre "alocação dinâmica" em Python

Python não expõe `malloc`/`free`. Aqui a "alocação dinâmica" é simulada
pela criação de objetos com `class Tarefa: ...` — cada `Tarefa(...)` gera
um objeto novo em tempo de execução, sem tamanho pré-reservado. Em vez de
`free()`, o **garbage collector** do Python libera a memória quando não há
mais referências ao objeto (pode-se mostrar isso com `sys.getrefcount()`
ou apenas discutir a diferença no relatório).

## Comparação (preencher depois de implementar)

| Aspecto | Estática | Dinâmica |
|---|---|---|
| Limite de tarefas | Fixo (definido na criação) | Sem limite fixo |
| Custo de criar tarefa | O(1), se houver espaço | O(1) |
| Desperdício de memória | Pode reservar espaço não usado | Usa só o necessário |
| Complexidade de busca por id | O(n) | O(n) |

## TODO

- [ ] Implementar `tarefa_estatica.py`
- [ ] Implementar `tarefa_dinamica.py`
- [ ] Escrever a comparação final na tabela acima
