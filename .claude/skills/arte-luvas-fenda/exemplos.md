# As luvas: a M5 no jogo, a L7 em proposta e as tentativas recusadas

Exemplos de raciocínio, não regras: a malha, a paleta de ferro e a tira de couro são escolhas da M5, para combinar com a
cota. O histórico completo está em `ferramentas/prototipos/hud/itens-lote-noite/LEIA-ME.md` (as seções "A manopla e as
perneiras" até "A M5 em 40, 48 e 64") e as pastas das rodadas em
`ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/`.

## A M5 (o 32 aprovado no `53d28893`, o 40, o 48 e o 64 no `2d18ce15`; no jogo desde a 1.147.0)

- **A base:** a B5, `glove_04.png` da Dungeon Crawl Stone Soup (CC0; a origem na [SKILL.md](SKILL.md)), escolhida pelo
  Jean na prancha `escolha_base/escolha-base-luvas.png` pela forma da mão e pela silhueta. A original é uma manopla preta
  com os nós e os rebites de prata.
- **A adaptação** (`manopla_perneiras/auxiliares/malha_dcss.lua`, sem mover pixel):
  - o contorno de fora e as linhas pretas entre os dedos ficam, na cor do contorno da família;
  - cada pixel de dentro vira um tom da rampa de ferro pela luminosidade do original, na faixa da cota: a luz e a sombra
    são as que o artista desenhou;
  - na mão e no punho, a malha: um tom acima e um abaixo do volume, alternando (a média é o volume); os vincos pretos de
    dentro das placas viram malha;
  - nos dedos e no polegar, o tom liso, sem xadrez, para não apagar a separação nem as juntas;
  - os rebites e os pontos brancos (ornamento, não volume) viram a malha no tom dos vizinhos;
  - uma tira de couro de 9 px onde o original tinha a linha diagonal entre o punho e a mão.
- **Na bancada:** a primeira passada subia os tons e saía lavada, mais clara que a cota; a segunda, na faixa da cota,
  perdia o xadrez nos tons médios e a divisa do pulso; a terceira abriu a alternância e pôs a tira.
- **O 40 e o 48:** o mesmo script com o tamanho N: a forma e os tons amostrados do original de 32 (o vizinho mais
  próximo), o contorno, as linhas dos dedos e a tira com 1 px (a linha que dobra na amostragem fica só no primeiro pixel,
  em qualquer um dos eixos: exigir os dois apagava as linhas diagonais dos dedos), a malha na grade do tamanho.
- **A M4** (da B4, `glove_03.png`, o couro preto com ouro) saiu da mesma regra e não foi a escolhida; fica em
  `malha_dcss/` como histórico.
- **As fontes finais** estão em `ferramentas/arte/aseprite/manopla/` (cópias das do protótipo, sem retoque).

## A L7 (20/10/2026: o 32 aprovado visualmente no `c7639438`; o 40, o 48 e o 64 em proposta; nada integrado)

- **As referências:** o recorte escolhido (`ferramentas/arte/referencias/Luvas/luvas-par-recorte.png`) define o desenho:
  o par, a pose, as proporções e a divisão entre o couro (os dedos, a palma, as tiras) e a malha (as costas da mão
  direita e os dois punhos); a imagem gerada (`luvas-par-gerada.webp`) esclarece os volumes e o acabamento. Onde as duas
  diferem, vale o recorte.
- **A guia:** o recorte é uma captura de pixel art, o pixel de ~3,45 px de tela; a grade nativa (a mediana do miolo de
  cada célula) dá um par de ~29 × 30 px, que cabe no 32 na escala 1:1, só deslocado para centrar.
- **A transposição** (`luvas_l7/auxiliares/transpor.py` e `ajustes.py`): a cor mais perto da paleta do conjunto; o halo
  do fundo da captura saiu e a beira cinza virou contorno (o par todo contornado, como na referência); a malha pelo tom
  médio da vizinhança com o xadrez da cota (a mediana da captura apagava o xadrez das costas da mão; a tentativa com o
  tom de cada pixel anulava o xadrez irregular da captura); o dedo mínimo da direita refeito em couro (a marca d'água
  "©" o clareava). O couro sai mais quente que o do recorte: é a rampa do conjunto.
- **A limpeza e os retoques** (`limpeza.py`, `retoque.py`, `retoque2.py`, cada pixel com o porquê; as versões
  anteriores em `anterior_<commit>/`): os pixels residuais nas beiras, as manchas cinza no couro em sombras, os recortes
  pretos acidentais, a dobra da base do polegar contínua, a costura do pulso lisa, as junções da malha com o couro; o
  Jean apontou nas folhas um pixel perdido, uma ponta de sombra e um pixel prata na borda da malha (em contorno).
- **O 40 e o 48** (`tamanhos.py`), do 32 final como autoridade, pelo princípio da M5: a forma pelo vizinho mais
  próximo; o contorno de fora com 1 px e as linhas de dentro com 1 px na direção da espessura de cada linha no 32 (a
  regra de "primeiro pixel em qualquer eixo" pontilhava as linhas deitadas); a sombra sólida do tom 1 tratada como
  linha, não como malha; a malha refeita na grade de cada tamanho; poucos ajustes à mão nas sobras de cruzamento.
  **Revisto a pedido do Jean** (tinham perdido parte da leitura da mão): forçar toda linha de dentro a 1 px deixava as
  linhas finas demais para dedos maiores (riscos e cruzes no 48) e apagava os vãos dos dedos e do polegar no 40; as
  linhas de dentro passaram a vir do 32 pelo vizinho mais próximo (1 ou 2 px, na proporção do 32), com os ajustes à
  mão onde o arredondamento engrossou, afinou ou fundiu as formas (o bloco preto do encontro das luvas, a sombra do
  polegar da direita, a ponta do dedo do meio, os nós da direita na proporção, a costura do punho). Lição: compare os
  tamanhos ampliados à mesma altura antes de entregar; a regra de 1 px não vale mais que a leitura da mão.

## A lição: partir de um desenho de mão que funciona

Adaptar uma base pronta (a M5) funcionou melhor que reconstruir a mão por medidas, grades ou descrições; transpor uma
referência visual escolhida (a L7, como as botas B3) é o mesmo princípio: a anatomia vem resolvida por quem desenhou, e o
trabalho fica na escala, na paleta e na leitura.

### Adaptar funcionou melhor que reconstruir (a M5)

As rodadas que construíram a mão (por medidas num script, por grades à mão no Aseprite, a partir de referências de
manoplas, de guias de anatomia e das luvas da Dungeon Crawl lidas pixel a pixel) resolviam um defeito e traziam outro.
A adaptação de uma luva pronta bem desenhada foi aprovada na primeira proposta com a base certa, porque a anatomia já
vinha resolvida por quem a desenhou e só o material mudou. Estudar as luvas da Dungeon Crawl e redesenhar a mão a
partir delas (no lote de exploração) não chegou perto do resultado de partir de uma delas.

## As tentativas recusadas (e o problema de cada uma)

- **Dedos em hastes** (`recusadas_c5fd33b/`, o remake 3): quatro dedos de 2 px com 1 px de vão, cada um um cilindro com
  juntas: pareciam hastes retas presas a uma peça mecânica. O punho em sino largo e o polegar levantado faziam um troféu.
- **Dedos em ganchos e o punho dominando** (`rodada3_89be986/`): os dedos como faixas que curvavam nas pontas, por cima
  uns dos outros, pareciam ganchos de garra mecânica; a manchete em cone dominava a peça (a primeira, em sino, lia como
  um megafone).
- **O pente de dedos** (`rodada4_9509530/`): com quatro dedos de 2 px ficava um pente de linhas escuras; três de 3 px
  liam melhor, mas a luva ainda não convenceu. Depois dela, o Jean pediu para abandonar a construção dos dedos.
- **Os dedos fundidos** (a rodada 5, à mão no Aseprite; as fontes em `manopla_perneiras/fontes/manopla/`): os dedos
  juntos num volume só, separados só na beira de baixo; a primeira silhueta lia como um saco. Também foi o motivo de
  `urand_war` sair da escolha de base (os dedos fundidos num bloco).
- **A mão em pá** (o lote de exploração, antes do commit): a primeira mão de estudo, a base comum das cinco luvas, tinha
  a palma como uma pá e os dedos como franjas retas; o Jean recusou e as tentativas com ela foram descartadas. Os seis
  candidatos que vieram depois (`lote_exploracao/`, L1 a L6, cada um com a camada `estudo_mao`) também não foram
  aprovados.
- **A luva leve demais** (`adaptacao_idylwild/`, I1 e I2): a adaptação já era o método certo, mas as bases não: a I1
  (`cloth_gloves`) tinha a anatomia melhor e lia como luva leve, não como equipamento; a I2 (`gauntlets`), o par na
  horizontal com os dedos miúdos.
- **O punho dominando** (na escolha de base): `gauntlet_02` da Dungeon Crawl saiu porque o manguito comprido domina a
  mão. Na luva, a mão é a parte principal; o punho é curto.
