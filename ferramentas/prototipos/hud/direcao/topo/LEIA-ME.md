# O topo pintado da HUD (em avaliação, nada no jogo)

**Pedido de Jean (18/10/2026):** concluir o topo da HUD com a pintura horizontal que ele mandou. A barra fica com a
altura de hoje e os textos no mesmo lugar. O desgaste liga o topo às laterais com discrição. Conferir também os dois
estados que ficaram fora da última demonstração: a vida máxima bloqueada e a habilidade indisponível.

**A fonte da decoração:** `../topo.png`, de Jean (2172×724, com transparência). É uma faixa de tinta preta com
passadas diagonais, o rasgo embaixo e manchas de papel bege nas pontas.

## Como entra

O estudo do conjunto (`../conjunto/`) fica como estava; esta camada vem por cima dele.

**`derivar_topo.py` → `pecas/topo-faixa.png` (2144×76):**
- **O recorte.** Tira as margens transparentes (x 15 a 2158) e as linhas de cima, que não cabem na barra. Ficam as
  linhas 419 a 495 da pintura:
  - dentro da barra, o carvão sólido e o começo do rasgo (até a linha 470);
  - abaixo dela, só as pontas do rasgo, apagando nas últimas 12 linhas, sem corte reto.
- **Nada é esticado.** A escala é uniforme.
- **A atenuação local, a única desta rodada.** Na altura da barra, as manchas bege das pontas ficavam atrás do
  logotipo e de "Fonte" e "Som" e disputavam com o texto. Só ali o claro escurece até o tom do carvão. Abaixo da barra
  as pontas do rasgo continuam bege, ligando o topo às colunas; a da esquerda fica pela metade, para não somar com a
  mancha do canto da ficha.

**`topo.css`:**
- **A pintura.** Um pseudo-elemento atrás dos textos (z-index −1 dentro da barra, sem clique). Tem a largura da tela,
  e a altura vem da proporção (68 px a 1920, dos quais 46 na barra e ~22 de pontas sobre a borda de cima das colunas).
- **A barra.** Fica com 46 px, sem o fundo de antes.
- **Ajuste local.** 4 px a menos no alto da ficha: na luta com um ferimento, a linha dele fazia a coluna rolar.

**`fotografar.mjs [jogo|topo]`:** as cenas das rodadas anteriores (exploração; luta com o seletor e a mira) e uma
nova para os estados. É a mesma luta, com o herói mordido e com fome e com 10% do Vigor.

## Conferido (`capturas/relatorio-jogo-topo.json`, 1920×945)

- **A barra:** 46 px (como no jogo).
- **O centro e a arena:** 1088 px.
- **A rolagem:** a página, a ficha e o mundo não rolam, nas três cenas.
- **A luta:** o seletor abre e Esc volta; a mira marca o alvo, e o golpe leva ao turno 2.
- **Erros:** nenhum na página.
- **A vida máxima bloqueada:** 105 de 146 (Mordida dilacerada e a fome, do motor).
  - A carta do herói mostra a parte bloqueada tracejada: "105/146".
  - A ficha mostra os atributos abaixo do normal (−20%, −28%) e o ferimento aberto.
  - Tudo legível sobre o carvão.
- **A habilidade indisponível:** as 7 do paladino com "Vigor insuficiente", o motivo do motor, iguais no jogo e no
  estudo. No seletor, a faixa apagada e o motivo escrito embaixo do nome.

**Comparações** (`comparacoes/`, tamanho real):
- `topo-1-exploracao.png`: a tela inteira com o topo;
- `topo-5-seletor.png`;
- `topo-6-mira.png`;
- `topo-7-estados.png`;
- `topo-8-indisponivel.png` e `jogo-8-indisponivel.png`: o seletor com as indisponíveis, no estudo e no jogo.

**O que não rodei:** a suíte, o gabarito e a fumaça. Nenhum arquivo do jogo mudou.

## Limitações

- **Outra largura de janela.** A altura da pintura acompanha a largura (escala uniforme): numa tela mais estreita, a
  parte dentro da barra fica menor e as pontas sobem para dentro dela. Sem bateria de resoluções.
- **As pontas sobre as colunas.** Passam por cima da borda de cima delas (sem clique), onde não há informação, a
  1920×945.
