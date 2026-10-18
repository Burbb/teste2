# Prova de fidelidade: a coluna da ficha (em avaliação, nada no jogo)

**Pedido de Jean (17/10/2026):** a primeira proposta (`../direcao.css`) ficou longe da referência. Antes de estender
o visual à HUD inteira, mudar o método: uma prova só da coluna da ficha (retrato, nome, experiência, atributos e a
superfície com as bordas), o mais perto possível da imagem de referência (`../referencia.png`), com os dados e os
desenhos do jogo. A proposta anterior fica como estava, para comparar.

## O que mudou no método

- **A referência entra no trabalho.** `../referencia.png` (1672×941) é uma tela de 1920×1080 reduzida a 0,871; ampliada
  na mesma escala, ela foi recortada lado a lado com a captura do jogo em tamanho real, e cada rodada foi conferida
  assim, também ampliada a 2× na borda (o canto de cima à esquerda, o retrato e os atributos).
- **A arte decorativa é imagem, não CSS.** A superfície e a borda rasgada saem de um gerador próprio
  (`gerar_arte.py`, reproduzível, semente fixa), no tamanho da coluna. O CSS (`ficha.css`) só cuida do conteúdo:
  proporções, tipografia e divisórias. A arte fica no fundo da coluna; o conteúdo e os controles ficam por cima, sem
  imagem nenhuma neles.

## As diferenças que guiaram a prova (atual × referência, na mesma escala)

1. **Escala.** Na referência tudo é cerca de 1,3× maior: retrato de ~112 px (era 80), nome de ~40 px (32), valores
   dos atributos de ~27 px (21), ícones de ~38 px (24), e a coluna mais larga.
2. **Borda.** Um rasgo irregular, com manchas grandes, trechos finos e trechos que desaparecem. Fora dele há uma faixa
   de papel cinza-bege com grão de pontinhos e tinta escura avançando sobre ela. No jogo havia uma moldura de aço com
   rebites; na proposta anterior, um serrilhado miúdo e repetido com um halo marrom em volta.
3. **Superfície.** Carvão quase preto, com manchas largas e discretas e nenhuma cor na borda.
4. **Divisórias.** Nenhuma caixa. Títulos de seção em versal espaçada com um fio que se apaga; entre as duas colunas de
   atributos, um fio vertical que some nas pontas; nenhuma linha horizontal.
5. **Hierarquia.** O nome e os valores com presença (claros, grandes); os rótulos e o subtítulo mais quietos.

## As peças criadas

- **`gerar_arte.py`:** gera as duas imagens de `arte/`, com ruído de valor em várias escalas (NumPy e Pillow). Os
  tamanhos são os da coluna na janela de referência (`fotografar.mjs medir`).
- **`arte/ficha-superficie.png`** (348×879, com transparência): o fundo da coluna.
  - O carvão: a cor base com manchas largas e discretas, passadas de pincel quase invisíveis e um grão fino. Escurece
    um pouco perto da borda, sem cor nenhuma.
  - A borda, com um limiar que varia ao longo do contorno:
    - manchas grandes mordem até ~36 px;
    - fibras finas correm ao longo da borda (o pincel seco, abrindo falhas);
    - um serrilhado miúdo;
    - em alguns trechos, o corte vira um degradê largo e o carvão se desfaz;
    - respingos de tinta perto do corte.
  - O lado de fora gasta mais que a emenda com o centro.
- **`arte/margem-papel.png`** (120×1100, repete na altura): a margem à esquerda da coluna.
  - O papel encosta no rasgo dela, com largura que vai de zero (a tinta cobre tudo) a ~40 px.
  - Para fora, a tinta quase preta, de recorte serrilhado, com respingos e frestas.
- **`ficha.css`:**
  - **A coluna:** 348 px (era 290), ganha da margem da mesa (a largura máxima dela sobe 58 px). O centro e a arena
    continuam com 1088 px; só andam 29 px para a direita.
  - **O conteúdo:**
    - retrato de 120 px num nicho de aresta clara;
    - nome em Alegreya 600 de 40 px, marfim, e subtítulo de 17,5 px;
    - experiência de 18 px, com a barra de 12 px;
    - títulos de seção em versal de 15 px, espaçada, com o fio que se apaga;
    - atributos com ícones de 32 px, rótulos de 17 px e valores de 26 px, e o fio vertical entre as colunas.
  - **O ajuste da altura:** os espaços entre as seções foram apertados para a coluna inteira caber sem rolar.
- **`ficha.js`:** só pede os desenhos de sempre em tamanhos maiores. O busto de 40×40 a ×3 (120 px, nítido) e os ícones
  de atributo de 32 px, que já existiam. Nenhum desenho novo.
- **`fotografar.mjs [medir]`:** jogo × prova no mesmo caso da proposta anterior (a Capela Afogada de dia, o arqueiro
  patrulheiro de nível 5), a 1920×945. Mede a coluna, o centro e se a ficha rola; fotografa a tela, o recorte, a
  dica de um atributo, a dos testes e o foco.

**Sem Aseprite nesta rodada.** O desgaste pedido é um padrão em várias escalas ao longo de ~2450 px de contorno, sem
repetir, e o gerador faz isso no tamanho exato da coluna. Ele também se refaz quando a medida mudar. O Aseprite fica
para o retoque à mão, se a avaliação pedir manchas desenhadas em pontos certos (ver abaixo).

## Comparações (`comparacoes/`, tamanho real)

- `referencia-x-prova.png`: a referência (ampliada à escala do jogo) e a prova, lado a lado.
- `referencia-x-anterior-x-prova.png`: a referência, a proposta anterior (`../direcao.css`) e a prova.
- `prova-tela-inteira.png`: a prova no jogo de produção (o resto da tela como está hoje).

## Conferido

- **O centro e a arena:** 1088 px, como no jogo.
- **A ficha:** cabe sem rolar (0 px de sobra).
- **As dicas:** a dica de um atributo e a dos testes abrem por cima da coluna, legíveis.
- **Erros:** nenhum na página (`capturas/relatorio.json`).
- **Os outros controles da coluna:** o aviso de talento, a bolsa e os espaços de item continuam os mesmos elementos,
  com o mesmo funcionamento. O foco do teclado é o de produção (a prova não mexe nele).
- **O que não rodei:** a suíte, o gabarito e a fumaça. Nenhum arquivo do jogo mudou.

## Os compromissos

- **O papel fica junto da coluna, não na beira da tela.** A mesa continua com a margem de hoje, para o centro não
  mudar. Na referência, a coluna encosta na beira da tela. Aproveitar a largura toda a 1920 é da consolidação.
- **A arte foi feita para a janela de referência.** Em outra altura, a superfície estica na vertical (o rasgo
  continua, mas mais esticado) e a margem repete. Não houve bateria de resoluções, e uma versão que se adapte (as
  bordas em tiras) fica para quando a linguagem for aprovada.
- **Ficaram como em produção:** o topo (com a sombra pontilhada caindo sobre a coluna), o equipamento, a comitiva, a
  bolsa, a reputação e o resto da tela. Eles só herdam a superfície e os títulos.

## O que ainda difere da referência

- **O papel:** na referência é um pouco mais amarelado e quente; aqui, mais cinzento.
- **Riscos claros de pincel seco:** na referência aparecem dentro do carvão, perto da borda. Aqui ficaram discretos,
  porque mais fortes viravam linhas retas.
- **O retrato:** na referência tem um fio duplo (claro e escuro); aqui, uma aresta clara só.
- **O topo da coluna:** na referência a coluna sobe por baixo do logotipo, sem barra; aqui, a barra de cima é a do
  jogo.
- **A experiência:** a barra roxa cheia não aparece, porque o caso começa com 0 de experiência.
- **Os ícones:** os de atributo são os de 32 px que já existiam; os da referência são um pouco maiores e mais
  pintados.
