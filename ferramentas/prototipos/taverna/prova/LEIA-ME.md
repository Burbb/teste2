# Prova de qualidade: os jogadores em duas grades (29/10/2026)

As reconstruções completas da taverna estão interrompidas; a F fica como histórico, sem aprovação e sem integração.
Esta prova separa o que vem da resolução do que vem da construção e do acabamento: os dois jogadores, a mesa redonda e
os banquinhos da F, desenhados de novo em duas grades nativas, no mesmo lugar da tela. **Não é a taverna resolvida:** é
o padrão de qualidade a escolher antes de aplicar ao resto da sala. Nada foi animado nem integrado.

## Abrir

`demo.bat` (o mesmo de sempre) abre na prova. No botão **Protótipo**: **Grade A** ou **Grade B** (a troca é imediata, no
mesmo lugar), **Isolado** (um fundo neutro cobre a sala; o conjunto fica no mesmo tamanho, com um trecho de piso) e as
candidatas da F à A. A sala em volta é a F sem o conjunto, só como contexto provisório.

## As duas grades

| | A: a grade atual | B: o dobro |
|---|---|---|
| Nativa | 66×42 pixels (1 por pixel da sala) | 132×84 pixels (2×2 por pixel da sala) |
| Na tela a 1920×945 | 219,4×139,6 px (3,325 px por pixel da A) | o mesmo (1,66 px por pixel da B) |
| Na tela a 1280×720 | 146×92,8 px (2,21 px por pixel da A) | o mesmo (1,11 px por pixel da B) |

As duas ocupam exatamente o recorte R da sala (x 174, y 42, 66×42 pixels da sala), conferido no jogo nas duas janelas
(a posição e o tamanho iguais aos da vista), com a mesma câmera (a projeção da F), as mesmas posições, poses, paleta e
luz (a da sala, calculada no ponto da sala de cada pixel). O navegador as escala sem suavização
(`image-rendering: pixelated`, devicePixelRatio 1 nas conferências).

**O artefato da apresentação:** a escala da vista não é inteira. A 1920, cada pixel da A vira 3 ou 4 px da tela
(como o resto da sala), e cada pixel da B vira 1 ou 2 px: a irregularidade relativa da B é maior (uma linha de 1 pixel
da B sai com 1 ou 2 px de espessura conforme a posição). A 1280, a B fica quase nativa (1 px, com um de 2 a cada ~9).

## Como foi feito (`conjunto.py`)

- Os móveis saem da projeção da F nas duas escalas: o banquinho de quatro pés com o assento grosso, a mesa redonda de
  um pé torneado com a base em cruz, o tampo com a borda e a face de cima, o tabuleiro (quatro casas por lado na A,
  oito na B) com as peças em pé, as duas canecas, o castiçal; as sombras de contato embaixo dos pés.
- As pessoas são desenhadas à mão em cada grade, em trechos por linha; nenhuma é a outra ampliada ou reduzida. O de
  verde, à esquerda, de perfil e inclinado, o cotovelo no tampo e o punho no queixo (pensa); o de ocre, à direita, de
  três quartos, estende o braço e pega uma peça. O quadril no banquinho, as coxas debaixo da borda, as canelas até as
  botas no piso. Portes diferentes: o de verde mais largo, o de ocre mais magro.
- A referência ("entre brasas e sombras") orientou as poses e a relação com os móveis; nada dela foi reduzido.
- A F ganhou uma chave desligada por padrão (`f.desenho.SEM_RODA`) para exportar a sala sem o conjunto; as camadas da F
  continuam idênticas.

## O que a prova mostrou

- **Na grade atual (A):** os dois sentados, a mesa com tampo e pé, os banquinhos, as pernas até o piso e o braço
  estendido do de ocre leem no tamanho do jogo. O gesto do de verde (o punho no queixo, o braço dobrado) cabe em ~5×6
  pixels e só se lê pela manga mais clara; o tabuleiro vira uma mancha com dois pontos; os rostos são um olho e a barba.
- **O que a grade maior permitiu (B):** o braço dobrado inteiro (o braço, o antebraço, o punho fechado debaixo do
  queixo), a mão segurando a peça, as casas e as peças do tabuleiro, a orelha, o nariz e a linha da barba, o cinto, o
  joelho redondo, a panturrilha e o cano das botas. A atividade dos dois se lê sem ampliar.
- **Se a B destoa:** sim, um pouco. Na sala da A em volta, os pixels da B têm metade do tamanho, e o conjunto parece de
  outra escala de acabamento (mais fino que a lareira e a escada ao lado); a 1920 a escala não inteira deixa os
  pixels da B irregulares. Uma sala inteira na B teria o grão uniforme, mas isso muda todos os interiores (a forja, a
  curandeira e o templo estão na grade atual): não é uma decisão desta prova.
- **O que continua nas duas:** os troncos ainda retos demais (falta a curva das costas e do peito no tamanho do jogo);
  as roupas com poucas dobras; os rostos simples; o contraste entre as roupas e o fundo escuro da sala; a luz por cima é
  a da sala, sem um realce próprio da vela da mesa nas pessoas.

## A B2: a B refinada pela referência (29/10/2026)

A prova mostrou que a grade maior melhora a leitura, mas os corpos continuavam rígidos. A B2 refaz **só o conjunto dos
dois jogadores** na grade da B (132×84, no mesmo recorte R e no mesmo tamanho na tela), pela referência
"Jogo de tabuleiro na taverna" (poses, volumes, a relação com a mesa e os banquinhos; o registro e o hash em
`ferramentas/arte/referencias/cenarios internos/LEIA-ME.md`), com o acabamento da forja, da curandeira e do templo. A A
e a B ficam como estavam, para comparar. **Não aprova a resolução da taverna**; nada foi animado, integrado ou aplicado
ao resto da sala, e o entorno é a F de antes.

**Abrir:** `demo.bat` abre na B2. No botão **Protótipo**: **Grade A**, **Grade B** e **Grade B2** (a troca é imediata,
no mesmo lugar) e **Isolado** (o fundo neutro, o mesmo tamanho).

### Como foi feita

- **A fonte é a autoridade:** `b2/aseprite/b2.aseprite` (132×84), com as camadas guia, bancos, mesa, verde e ocre. A
  guia é a referência posta na grade (alinhada pelo centro do tampo, 13 pixels dela por pixel da grade), **oculta e
  meio transparente**, nunca exportada. `b2/fonte.py --criar` semeou a fonte a partir de `b2/desenho.py` e recusa
  sobrescrevê-la sem `--refazer`; `b2/fonte.py` exporta da fonte (as camadas visíveis, menos a guia) para
  `camadas/prova/b2.png`, e `--conferir` mostra quantos pixels diferem do código. Os retoques feitos na fonte
  (`b2/aseprite/retocar.lua`, pela linha de comando do Aseprite: a sombra do cotovelo no tampo e as das quatro botas no
  piso) ficam nela: hoje são 35 pixels diferentes do código.
- **As pessoas, à mão, parte por parte** (as pernas, o tronco, o braço de trás, a cabeça, o braço da frente), em
  trechos por linha, da silhueta aos volumes: as costas curvas, o lado da vela aceso, as dobras, os joelhos, o cano e o
  bico das botas. Nada da referência foi reduzido para virar arte.
- **O de verde:** o corpo mais largo; as costas inclinadas e os ombros caídos; o quadril no banquinho, as coxas
  acomodadas, a canela de cá para trás e a de lá em pé, as duas botas no piso. O braço da mesa: o ombro em (37, 27), o
  **cotovelo no tampo** em (46, 39) e o punho sob o queixo em (43, 26), braço de 13 px e antebraço de 11 px. Na
  referência o cotovelo fica no ar, ~7 px acima do tampo; para pousá-lo sem esticar o braço, o tronco inclina mais e a
  cabeça desce. A outra mão desce pelas costas e descansa na coxa.
- **O de ocre:** mais magro; o tronco inclinado para o tabuleiro; o braço do ombro (82, 29) ao cotovelo (71, 33) e à
  mão em (62, 37), que segura a peça de barro sobre o tabuleiro; a outra mão na coxa; as pernas espelhando as do de
  verde.
- **Os móveis:** os banquinhos afastados da mesa e mais estreitos e altos, como na referência (os centros em x 17 e
  104 da grade, o assento a 0,5 m), sob o quadril; a mesa da F com o tampo de 3 px de espessura, o pé torneado e a base
  em cruz; o tabuleiro simplificado em 4×2 casas grandes, com uma peça clara e uma escura (sem as canecas).
- **Os rostos** inclinados para o tabuleiro: mais alto da cabeça à vista, a pálpebra baixa, o nariz para baixo.

### O que melhorou (no jogo, a 1920×945 e a 1280×720, no tamanho real)

- Os dois **parecem sentados**: o quadril no assento, as coxas para a frente, as botas no piso.
- **Os gestos se reconhecem** nas duas janelas: o de verde pensa com o punho no queixo e o cotovelo no tampo; o de ocre
  estende o braço e pega a peça; as duas mãos de descanso na coxa.
- **Os corpos deixaram de ser placas:** as costas curvas, os portes diferentes, o lado aceso pela vela.
- **Braços, tampo e tabuleiro separados:** o cotovelo pousa à esquerda do tabuleiro, a mão do de ocre fica sobre a casa
  dele, o castiçal atrás, sem cruzamentos.

### O que ainda não resolveu

- **O tamanho em relação à sala:** seguindo as proporções da referência, as pessoas da B2 ficaram maiores que as da A e
  da B (a cabeça começa em y 10 a 11 da grade, não em 13) e um pouco maiores que as figuras da F em volta.
- **O grão:** como a B, a B2 é mais fina que a sala em volta.
- **A escala fracionada:** a 1920, cada pixel da B2 vira 1 ou 2 px da tela (1,66 px em média): o olho, a moldura do
  tabuleiro e o cinto saem com espessuras desiguais. A 1280 (1,1 px) a B2 fica quase nativa, mas pequena: o punho e o
  rosto do de verde viram uma mancha, ainda reconhecível pela pose.
- **Rostos, mãos e roupas** continuam simples (as poucas dobras, os dedos não separados).
- **A vista isolada** não mostra a chama da vela (ela vem da camada da sala, coberta pelo fundo neutro), como na A e na B.

## A B3: os ombros e os braços da B2 (29/10/2026)

O Jean viu, na cena e na vista isolada, que os braços da B2 liam ambíguos: pareciam sair do ombro oposto, e era preciso
achar a outra mão para entender a pose. A B3 é um **ajuste localizado** dos ombros e dos braços dos dois; a mesa, os
banquinhos, a escala, as pernas, as cabeças, os apoios e a composição continuam os da B2, que fica como estava para
comparar. **Abrir:** `demo.bat` abre na B3; Grade B2 e as outras no botão **Protótipo**, no mesmo lugar.

### O diagnóstico na B2

- **O de verde:** a manga do braço da mesa tinha o mesmo tom do peito, separada só por uma linha escura (lia como uma
  dobra, sem ombro); o braço que desce à coxa formava o contorno das costas (nascia atrás do corpo); os dois ombros
  não diziam quanto o peito estava girado.
- **O de ocre:** o alto da manga estendida tinha o mesmo tom aceso da frente da túnica; ombro, manga e cotovelo se
  misturavam.

### O que mudou

- **O de verde:** o peito em três quartos, virado para a câmera e para a mesa, com o decote no meio dele.
  - O **ombro de cá** é uma calota redonda acesa por cima. O braço desce **à frente do tronco**, com uma faixa escura
    das costas à vista atrás dele e a sombra dele no peito. O cotovelo dobra e o antebraço atravessa a barriga até a mão
    na coxa.
  - O **braço da mesa** é o de lá: o peito passa na frente da raiz dele. O braço sai à direita do tronco, mais escuro,
    com a aresta acesa pela vela, e desce estreito até o cotovelo no tampo; o antebraço sobe à direita dele até o punho
    no queixo. A frente do peito ao lado desse braço ficou no tom médio, para a aresta acesa ser só a do braço.
- **O de ocre:** o ombro de cá é uma calota acesa no alto da frente do tronco; a manga sai dela num tom próprio (o alto
  aceso, o meio claro, a dobra de baixo escura) sobre a túnica de tom médio, que fica na sombra do braço logo abaixo
  dele. O percurso ombro, manga, cotovelo, punho dobrado, antebraço e mão na peça segue sem interrupção. A outra mão
  continua na coxa.
- Sem contorno novo, sem textura, sem dedos: só silhueta, sobreposição e poucos planos de luz e sombra.

### A fonte

`b3/fonte.py --criar` copiou a fonte da B2 (com os retoques dela: as sombras do cotovelo e das botas) para
`b3/aseprite/b3.aseprite` e trocou, só nas camadas verde e ocre, os pixels em que `b3/desenho.py` difere do desenho da
B2 (356 no de verde, 116 no de ocre), pela troca de camada da forja (`trocar_camada.lua`), conferindo o que salvou. A
guia continua oculta e fora da exportação. A fonte é a autoridade: `--criar` não a sobrescreve sem `--refazer`, e
`b3/fonte.py` exporta dela para `camadas/prova/b3.png`; `--conferir` compara a exportação com a B2 mais o retoque (hoje,
0 pixels de diferença: nenhum retoque feito depois na fonte da B3). A B2 exporta igual a antes.

### Conferido no jogo (1920×945 e 1280×720, no tamanho real, na cena e isolado)

No mesmo lugar e no mesmo tamanho da A, da B e da B2, sem suavização, console limpo, a demonstração inteira passando.
Nos dois tamanhos, os dois braços de cada um se acompanham até o ombro: no de verde, o ombro de cá aceso com o braço
caindo na frente das costas e o braço da mesa saindo de trás do peito; no de ocre, a manga clara do ombro à mão.

**Ainda aberto:**
- a 1280, o antebraço e o punho do de verde junto da barba ainda formam uma massa pequena (o gesto se lê pela pose);
- a calota acesa do ombro de cá do de verde é luz de cima, não da vela (que está do outro lado);
- o que já estava aberto na B2: o tamanho em relação à sala, o grão mais fino, a escala fracionada a 1920, os rostos e
  as mãos simples.

## A B4: o ombro de cá do de verde suavizado (29/10/2026)

A B3 esclareceu os braços, mas no de verde a construção do ombro de cá perdeu naturalidade: a faixa clara contínua no
alto do ombro, na aresta da manga e no punho dobrado lia como uma tira ou uma ombreira, e a coluna escura entre o braço
e o peito fazia o braço parecer encaixado no tronco. A B4 retoca **só esse ombro e essa manga**; a cabeça, o punho
junto da barba, o braço da mesa, as pernas, os móveis, a escala, a posição e o de ocre inteiro continuam os da B3, que
fica para comparar. **Abrir:** `demo.bat` abre na B4; no botão **Protótipo**, as grades da A à B4 e o Isolado, no
mesmo lugar. O botão mostra a versão à vista ("Protótipo: prova B4 · ..."), fora da arte; antes, ao abrir, ele dizia
"prova A" por um texto fixo, corrigido.

- **O ombro:** sem a calota de luz forte; a luz cai em duas manchas curtas sobre o tecido (o alto do ombro e o alto do
  braço, onde ele é mais redondo), quebradas por tons médios. O ombro continua no peito e nas costas pelo mesmo tom
  médio, sem a linha escura no alto.
- **Entre o braço e o peito:** uma sombra de um pixel no tom de sombra, só do sovaco ao cotovelo, no lugar da coluna
  dupla mais escura. A faixa escura das costas atrás do braço continua: é ela que põe o braço na frente do tronco.
- **O punho dobrado no cotovelo:** uma dobra baixa no tom da manga, sem a faixa clara.
- **A fonte:** `b4/fonte.py --criar` copiou `b3/aseprite/b3.aseprite` para `b4/aseprite/b4.aseprite` e trocou só a
  camada verde, nos 55 pixels em que `b4/desenho.py` difere do desenho da B3 (todos entre x 15 e 24, y 24 e 38),
  conferindo o que salvou; `--criar` não sobrescreve. A B3 e a B2 exportam iguais a antes.
- **O decote, retocado na fonte:** o Jean viu pixels cor de pele perdidos no peito. Eram o decote da B3 (x 28 a 31,
  y 24 a 27): com o pescoço escondido pela barba, ele ficava solto no meio da túnica. Os 10 pixels foram pintados na
  própria `b4.aseprite` (`b2/aseprite/retocar.lua`), no tom da túnica em volta; por isso `--conferir` dá 10 pixels
  diferentes da B3 com o retoque do ombro. Uma varredura da exportação não acha outros pixels de pele isolados. O giro
  do peito fica dito pelos dois ombros.

**Conferido no jogo** a 1920×945 e 1280×720, na cena e isolado, no mesmo lugar e tamanho das outras, console limpo,
a demonstração inteira passando: o ombro lê como tecido, sem tira e sem encaixe; os dois braços continuam se
acompanhando até os ombros, com o cotovelo no tampo e a mão na coxa.

**Ainda aberto:**
- **O tamanho e o acabamento em relação ao entorno**, visto na cena completa: os dois jogadores parecem maiores que as
  figuras da F à mesma distância (o homem junto da lareira, Morel no canto) e mais finos que elas (o grão da B contra a
  sala na grade atual). A escala ficou como estava, por pedido.
- A 1280, o braço de cá ficou um pouco menos marcado que na B3 (ainda se lê pela faixa das costas, pelo cotovelo e pela
  mão na coxa).
- O punho junto da barba, a escala fracionada a 1920 e os rostos simples, como antes.

