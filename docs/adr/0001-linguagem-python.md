# 0001 — Linguagem: Python

## Contexto

O roteiro da disciplina permite escolher livremente a linguagem, desde
que ela permita implementar modularização, passagem de parâmetros,
alocação de memória e estruturas encadeadas de forma explícita.

## Decisão

Usar Python 3 para todo o projeto.

## Consequências

- Python não tem `malloc`/`free` explícitos como C. A "alocação
  dinâmica" pedida no Módulo 2 foi simulada pela criação de objetos
  (`class Tarefa`), e a liberação de memória fica a cargo do garbage
  collector — isso é discutido no relatório do Módulo 2
  (`modulo2_tad/README.md`).
- Em compensação, Python permitiu focar o tempo do projeto nas
  estruturas de dados em si (listas, pilhas, filas) em vez de gerenciar
  ponteiros manualmente, o que também tornou viável construir a
  interface de terminal completa (curses) dentro do prazo do semestre.
- A ausência de tipagem estática exigiu disciplina manual para manter a
  interface de cada TAD consistente (ex.: sempre usar `dict` com as
  mesmas chaves para representar uma tarefa).
