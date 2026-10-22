# O Mercenário e o Lobo Gélido (22/10/2026, propostas; nada no jogo)

**Pedido de Jean:** depois das integrações (o Esqueleto E1r, o urso e o falcão da fogueira, o cajado do Mago), o
próximo par de criaturas: duas propostas por criatura, só no protótipo, na linguagem dos retratos finais, comparadas na
carta e no Bestiário junto dos aprovados, com os mesmos dados.

## O que o jogo diz

- **Mercenário** (`mercenario`, `rpg/dados.py`): "Armadura boa, moral flexível. Lutam pelo maior lance."; humano e
  blindado; Preparar Golpe (o golpe esmagador, com aviso), Golpe Sujo e Grito de Guerra; 32 de vida, carrega flechas (o arqueiro
  acha algumas). Aparece nas planícies, no duelo de honra da ponte (o mercenário de armadura polida), nos guardas do
  nobre, na escolta do cultista, junto do bandido e no Theodore, o Ruivo, dos Cães de Ferro (a história do Morel).
  Hoje sai do traço `humano` (o rosto de máscara vermelha, o mesmo desenho genérico de outros nove).
- **Lobo Gélido** (`lobo_gelido`): "O frio da montanha mora dentro deles. Odeiam fogo mais que qualquer coisa."; fera;
  Mordida Gélida e Uivo; resiste ao gelo e sofre mais com o fogo; 24 de vida; nas montanhas, em matilha de até três.
  Hoje sai do traço `fera` (o rosto antigo de lobo, o mesmo de outras onze).
- **Usos dos dois:** a carta da luta (32), o Bestiário (48), o mural e o rastreador de contratos, a faixa do mestre
  caçador; o retrato pela família, como os integrados.

## As propostas (16×16; o 32 e o 48 são o 16 ×2 e ×3)

- **MA, o chapéu de ferro** (`mercenario-ma`; camadas roupa, rosto, elmo): o elmo de aba larga dos soldados a soldo,
  os olhos na sombra da aba, a barba por fazer, a boca fechada, o gibão acolchoado ocre no pescoço e a malha nos ombros.
- **MB, a coifa de malha** (`mercenario-mb`; camadas roupa, coifa, rosto): o rosto fechado na malha, as sobrancelhas
  pesadas e baixas, os olhos fundos, a barba cheia, o ombro de placa e a correia da bainha.
- **A distinção:** os dois de cabeça coberta por metal (o Bandido usa capuz de pano, máscara vermelha e faca; o Cultista,
  o manto vermelho; o Morel, mercenário da comitiva, anda de cabeça descoberta, de cabelo castanho e cicatriz); o elmo do
  MA não tem o nasal nem a caveira do Esqueleto.
- **LA, o lobo da geada** (`lobo-gelido-la`; camadas pelagem, focinho, detalhes): a construção do Lobo aprovado (a
  cabeça de frente, as orelhas, o focinho claro, o começo do pescoço), com a pelagem clara azulada, as pontas brancas nas
  orelhas e nas sobrancelhas, os olhos de gelo e a juba clara que alarga as bochechas.
- **LB, o lobo da nevasca** (`lobo-gelido-lb`; as mesmas camadas): a mesma construção, a pelagem escura de ardósia, as
  orelhas deitadas para trás, o focinho franzido e o rosnado com as presas, a geada na testa e os olhos acesos.
- **O rosto sempre à vista:** nenhum dos dois esconde a cara atrás de neblina ou gelo; o que muda é a pelagem, a forma da
  juba e a expressão.

## A minha leitura (quem escolhe é o Jean)

- **Mercenário:** o MA é o mais legível na carta (a aba larga é uma silhueta que nenhum outro retrato tem) e o mais
  "soldado de ofício"; o MB é o mais duro e o mais blindado, mas a coifa cinza fica perto do tom do Esqueleto na fileira.
- **Lobo Gélido:** o LA é o irmão claro do Lobo (lê "lobo da neve" de longe); o LB se separa mais do Lobo pela expressão e
  pelo escuro, e a boca vermelha é o que mais chama na carta.

## Processo

- As grades à mão em `auxiliares/grades.py` (uma rodada de bancada: o MB ganhou sobrancelhas e olhos próprios, para não
  repetir o rosto do MA; o LA trocou as pontas brancas soltas por mechas de dois pixels).
- **O conector do Aseprite estava preso nesta sessão:** as fontes saíram da linha de comando do Aseprite
  (`python auxiliares/exportar.py --montar`, pelo `ferramentas/arte/aseprite/montar_camadas.lua`, o do `montar_fontes.py`, com o `pintar.lua`;
  releitura de cada camada, 0 diferentes), em `fontes/<id>/<id>-16.aseprite`; a exportação igual à grade, o @2x exato,
  o 32 e o 48 em blocos inteiros, em `proposta/`.
- As fotos (`auxiliares/fotografar.mjs`, a 1920×945): a luta (o cenário `tutorial` com `GRUPO=mercenario:1,
  lobo_gelido:1,lobo:1,bandido:1,cultista:1,esqueleto:1`) e o Bestiário (o cenário `covil` com os mesmos seis), nos
  modos atual, A e B, trocados só na página pelo nome; sem erro no console (`capturas/registro.json`).
- As folhas `mercenario.png` e `lobo_gelido.png` (`python auxiliares/prancha.py`): a carta em tamanho real e a 2×, o
  Bestiário, a fileira com os aprovados e a 12× com a grade.

## Alcance, se aprovado

Pela família (`RETRATO_FAMILIA`: `mercenario`, `lobo_gelido`; o papel `CRIATURA` e os `TAMANHOS` em `icones.js`), com
os líderes, os afixos e os nomeados (o Invicto da ponte, o Theodore). O `humano` e o `fera` dos traços continuam nos
outros usos.
