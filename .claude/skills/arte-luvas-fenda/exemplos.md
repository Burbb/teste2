# A luva aprovada e as tentativas recusadas

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

## A lição: adaptar funcionou melhor que reconstruir

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
