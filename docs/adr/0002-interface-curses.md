# 0002 — Interface em terminal com curses

## Contexto

A primeira versão do projeto final usava `print()`/`input()` simples,
o que fazia o terminal acumular todo o histórico de interações na tela,
sem nunca "limpar" — dificultando o uso e a apresentação.

## Decisão

Reescrever a interface usando o módulo `curses` (biblioteca padrão do
Python em Linux/Mac), que redesenha a tela inteira a cada ação, com
navegação por setas do teclado — no mesmo estilo de ferramentas de
terminal como `ncdu` ou `htop`.

## Consequências

- Só funciona em um terminal de verdade (TTY) — não roda, por exemplo,
  dentro de alguns consoles de IDE sem suporte a terminal interativo.
- No Windows, exige instalar o pacote `windows-curses`
  (`pip install windows-curses`), já que `curses` não é padrão lá.
- Em troca, a experiência de uso fica muito mais próxima de uma
  ferramenta de linha de comando profissional, o que ajuda na
  apresentação do projeto.
- Para manter a lógica testável sem precisar simular um terminal, toda
  a lógica de negócio foi isolada na classe `TaskFlowApp`, que não
  chama `curses` em nenhum momento — só a camada de interface (funções
  `tela_*`) depende dele. Essa separação está detalhada em
  `docs/ARQUITETURA.md`.
