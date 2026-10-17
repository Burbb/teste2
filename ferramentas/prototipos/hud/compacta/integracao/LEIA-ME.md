# A composição compacta integrada (1.114.0)

O Jean aprovou a B refinada e o registro na coluna do mundo (`5cb517d`, `../rodada2/`). Esta pasta confere o **jogo
integrado**, sem nenhuma troca na página: o que entrou no jogo está em `app/escolhas.js` (`dispor`), `app/paineis.js`
(`acomodarRegistro`), `18-seletor-habilidades.css` (o seletor `.lateral`) e `15-hud-luta.css` (o registro ao lado). A
produção não depende desta pasta. A correção do Rei dos Mortos, que limita os grupos reais, veio antes, em commit
próprio (1.113.2).

## O comportamento final

- **O seletor:** abre embaixo da arena quando cabem a lista inteira e uma descrição legível. Senão, abre sobre a
  ficha, numa coluna, com o custo embaixo do nome, o Voltar no título e a descrição embaixo. A ficha coberta não
  recebe clique nem foco, e escolher uma habilidade (a mira) tira o seletor.
- **Redimensionar com o seletor aberto:** ele se dispõe de novo, sem fechar; a habilidade examinada e o foco ficam.
- **O registro:** a conta é feita no começo da luta e a cada novo tamanho de janela. Se a arena, com uma linha de
  efeitos em cada carta, deixasse menos de 140 px para o registro, ele vai para uma coluna ao lado:
  - a coluna do mundo, embaixo do nome do lugar, do nível e dos avisos;
  - sem ela (abaixo de 1100 px), a da ficha, embaixo do nome, do nível e da experiência;
  - sem nenhuma (abaixo de 920 px), fica embaixo da arena com 240 px, e a página rola até ele.
- **O que fica coberto pelo registro:** o minimapa, a missão e os caminhos, ou o resto da ficha. Fica inerte e volta
  quando a luta acaba.
- **Estabilidade:** no mesmo tamanho de janela, efeitos que entram e saem não mudam o registro de lugar.

## Conferido (`fotografar.mjs`, `comparar.py`; 13 cenários em ~93 s)

- **Igual ao protótipo aprovado**, com os mesmos dados, em 1280×720: o Arqueiro (Foco e flechas) e o necromante com
  a comitiva e 3 servos, contra 5 caídos e o xamã. Também o necromante em 1500×950.
  - Habilidades 7 de 7 e Itens 5 de 5 sobre a ficha.
  - Nenhum nome em três linhas; os custos embaixo e alinhados; o Voltar no título.
  - Descrições de 163, 160 e 143 px, as mesmas do protótipo.
  - Na mira, o seletor sai, a ficha volta e os 6 alvos acendem.
  - O registro na coluna do mundo, com ~13 linhas, também com os efeitos reais.
  - Comparações em `capturas/comparacoes/`, o protótipo e o jogo lado a lado.
- **A passagem entre tamanhos**, com a luta em andamento e os efeitos reais do necromante (`janelas.png`):

  | janela | o registro | o seletor | inimigos à vista |
  |---|---|---|---|
  | 1500×950 (começo) | embaixo, ~7 linhas | sobre a ficha | 6 de 6 |
  | 1280×720 | coluna do mundo, ~13 linhas | sobre a ficha | 6 de 6 |
  | 1050×720 (o mundo some) | coluna da ficha, ~14 linhas (o seletor o cobre enquanto aberto) | sobre a ficha | 6 de 6 |
  | 900×720 (a ficha some) | embaixo, 216 px; a página rola | embaixo, rolando | 6 de 6 |
  | 1280×720, 1500×950 (volta) | como na primeira passagem | como na primeira | 6 de 6 |

  Em cada tamanho, os efeitos saindo e voltando não mexem no registro, e a mira funciona.
- **Teclado e movimento reduzido**, em 1280×720 e 1050×720:
  - a tecla 2 abre com o foco na primeira; as setas chegam à quinta, à vista e com a descrição;
  - os pontos da ficha caem no seletor, e o Tab vai do seletor para a arena, nunca para a ficha;
  - Esc fecha e devolve o foco; sem animação.
- **As verificações do CLAUDE.md:** a suíte (com `tests/test_rei_dos_mortos.py`), o gabarito sem mudança, o pyflakes e
  a fumaça uma vez (`capturas/logs/fumaca.log`, "tudo certo", ~8 min).

## Limitações

- **Abaixo de 920 px** não há coluna ao lado. O registro fica acessível rolando a página, mas o seletor também abre
  embaixo e pede rolagem; essa largura pede uma composição própria.
- **Na coluna da ficha** (entre 920 e 1100 px), o seletor aberto cobre o registro até fechar.
- **A estimativa da altura** usa uma linha de ícones por carta (até 4 cabem numa linha, o máximo visto). Um reforço
  invocado que entra depois do começo não refaz a conta, a não ser que a janela mude de tamanho.
