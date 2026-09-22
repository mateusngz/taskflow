# Projeto Final — TaskFlow (integrado)

## Visão geral

Aplicação de terminal (CLI) que integra as estruturas implementadas nos
módulos anteriores:

- **Listas** (Módulo 3): colunas do Kanban (A Fazer / Fazendo / Concluído)
- **Pilha** (Módulo 4): undo/redo de ações
- **Fila de prioridade** (Módulo 5): avisos de tarefas urgentes

## Fluxo do menu (planejado)

```
1. Adicionar tarefa
2. Listar tarefas (por coluna)
3. Mover tarefa entre colunas
4. Marcar tarefa como concluída
5. Desfazer última ação
6. Refazer
7. Ver avisos de tarefas urgentes
0. Sair
```

## Como executar

```bash
python3 projeto_final/main.py
```

## Apresentação (10-15 min)

Roteiro sugerido:
1. Mostrar o menu funcionando (2 min)
2. Demonstrar undo/redo ao vivo (2 min)
3. Explicar a escolha lista array vs. encadeada, mostrando a tabela de
   complexidade do Módulo 3 (3 min)
4. Explicar a fila de prioridade e mostrar um exemplo com tarefa urgente
   furando a fila (3 min)
5. Perguntas

## TODO

- [ ] Implementar `main.py` conectando os módulos anteriores
- [ ] Testar o fluxo completo manualmente
- [ ] Preparar os slides/roteiro da apresentação
