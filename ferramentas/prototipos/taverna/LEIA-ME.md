# Protótipo: o interior da taverna (o balcão animado e a vista diante de Morel; o resto como histórico)

**A queda de braço no canto** (30/10/2026, a candidata): o canto foi aprovado pelo Jean e a disputa recomeça nessa cena,
como continuação da conversa (a seção "A queda de braço no canto", abaixo); a alimentação ganhou três correções (a
colher de metal, a coleta dentro do caldo, o cotovelo longe da caneca).

**A nova direção** (30/10/2026, antes): o encontro com Morel passa para **o canto da taverna**, numa câmera de primeira
pessoa (a seção "Morel no canto da taverna", abaixo); **a queda de braço fica suspensa** até essa base ser aprovada;
**a vista diante do balcão fica reservada para a Vó Berta**, sem queda de braço. **A candidata revisada** (a
mastigação, o tronco e a gola, a parede da esquerda; a seção "A revisão dos três pontos") está em avaliação; a primeira
candidata do canto fica no painel, no mesmo estado do encontro.

**O estado anterior** (30/10/2026): as duas vistas **aprovadas** pelo Jean (o balcão da G4 e a vista diante de Morel, com as
últimas correções) estão **ligadas ao encontro** no protótipo: sentar com o homem do canto leva à mesa dele, as opções do
evento aparecem ali, o pagamento lança moedas na mesa, e a conversa acaba de volta ao balcão. Na vista de Morel, o
**braço da colher ganhou o acabamento de uma manga só** (o ombro e o cotovelo liam como peças articuladas; em
avaliação; a versão anterior no painel). A **queda de braço** voltou ao "queda 1" (a primeira proposta, na câmera da
conversa), refeito pela postura (Morel debruçado, nós colados ao apoio, o encontro no meio do tampo) sobre a vista
aprovada e **animado** nos dois desfechos: a candidata está em avaliação; as propostas anteriores ficam como
histórico. Nada integrado à produção.

## Morel no canto da taverna: a nova direção (30/10/2026; a candidata, em avaliação)

**A mudança de direção (o Jean):** as tentativas de queda de braço mostraram um problema anterior à animação, a
perspectiva: a câmera da vista diante do balcão não transmitia a visão de um adulto sentado à mesa, e o braço do
jogador ficava comprido demais. Primeiro a nova cena da conversa e da comida, pela referência aprovada "Encontro com
Morel na taverna" (`ferramentas/arte/referencias/cenarios internos/`; a captura do Gwent, ao lado dela, só para o ponto
de vista). **A queda de braço fica suspensa** até esta base ser aprovada (as propostas ficam como histórico).
**A vista diante do balcão** (com o taverneiro ao fundo) fica preservada e **reservada para a Vó Berta**, sem queda de
braço; nada foi substituído nela (no painel, "Diante de Morel, junto do balcão").

**O lugar:** outro ponto da mesma taverna, o canto (o texto do encontro: "No canto da taverna, um homem grande come
sozinho, de costas para a parede"): Morel de costas para a parede de pedra escura, junto do canto, com os esteios e a
travessa de madeira; o balcão e o taverneiro não aparecem atrás dele.

**O enquadramento** (`morel/canto/espaco.py`): os olhos de quem senta diante dele, perto, o tampo de cima, a borda do
nosso lado fora do quadro, nenhum braço nosso. A referência tem 2,5 por 1; na altura das cenas (96) ela ocupa 240 de
largura, no tamanho dela (nada esticado, Morel não achata, a câmera não recua); os 40 px de cada lado continuam o canto
(mais da parede lateral à esquerda, outra baia da parede do fundo à direita, com o esteio). Morel fica grande: a cabeça
com 28×34 (na vista do balcão, 21×25). O horizonte na altura dos olhos dele (y 22), o ponto de fuga do tampo no meio.
Para uma futura queda de braço, a mão e o antebraço nossos podem entrar pela borda de baixo, com o cotovelo perto dela,
sem mostrar o braço até o ombro (não desenhado nesta rodada).

**O que precisou ser adaptado à grade e à coerência:**
- **A parede da esquerda:** na imagem gerada, as fiadas dela descem para o canto como se o olho estivesse abaixo do
  tampo, o que não fecha com o tampo visto de cima. Na primeira candidata ela foi um pano em ângulo, com um ponto de
  fuga próprio e longe (lia como outra parede de frente); na revisada, é a lateral do cômodo, fugindo para o ponto da
  sala (a seção "A revisão dos três pontos").
- **A redução da imagem não virou arte:** a redução mapeada nas paletas do jogo ficou granulada (o pontilhado da
  redução, o vermelho vazando para o pão e a parede, o rosto ruidoso); ela fica só como a camada `guia` da fonte. Cada
  coisa foi construída: as paredes, os esteios e o tampo em código (`espaco.py`); o castiçal, a vela e a chama, a
  caneca, o pão e a tigela com o ensopado (`objetos.py`); Morel por partes (`morel.py`).
- **Morel, desenhado de novo nesta escala,** com as paletas e o jeito da vista aprovada: a cabeça numa grade à mão (os
  três tons do cabelo, a pele com o lado da vela claro e o outro em sombra, a cicatriz num traço de um pixel
  atravessando a sobrancelha, a barba em dois tons com a boca num traço; os olhos baixos, abertos no olhar, a boca
  aberta para a colher, o queixo mastigando); o casaco, o colete com a costura e as duas tiras com as fivelas, a gola;
  as duas ombreiras diferentes (a clara como um casco inclinado, com a crista acesa e os rebites; a escura sem brilho de
  aço); a espada às costas com o pomo acima do ombro direito; os braços pela manga aprovada (`vista/manga.py`) com os
  raios desta escala; as mãos em bolinha; a colher de madeira rígida. Simplificados para a grade: o rosto, os dedos
  (nenhum), o ensopado (pedaços de um ou dois pixels), o miolo do pão, as texturas.
- **A mesa:** a borda de lá do tampo em y 72 (na referência, 76 nas laterais), para os cotovelos pousarem nele.

**A animação** (`morel/canto/juntas.py`, pelo método do braço aprovado: os comprimentos fixos, o cotovelo pela
cinemática, a colher rígida): as mesmas 20 poses da vista aprovada, na mesma ordem e com a mesma linha do tempo (156
tiques), para a reação ao pagamento continuar a mesma; as trajetórias são novas (o cotovelo do braço da colher pousa
para fora, ao lado da caneca, como na referência; na boca ele sobe à frente do peito e a colher chega à boca com a
cabeça descendo ao encontro dela). O tronco desce 1 px enquanto ele come; o braço que descansa acompanha o tronco no
ombro, com a mão parada no tampo. **O pagamento:** as moedas são as da vista, com o pouso nesta mesa (entre o pão e a
tigela, na frente); ele para, olha as moedas, olha para quem pagou e volta à tigela. **Movimento reduzido:** a pose de
repouso, a chama parada, as moedas já assentadas.

**A fonte** `morel/canto/canto.aseprite` (20 quadros com as etiquetas; as camadas `guia` e `juntas` ocultas): montada
uma vez por `cena.py --criar` (recusa sobrescrever sem `--refazer`); depois ela é a autoridade, e `exportar.py` só lê
dela (`camadas/morel-canto/`; `--conferir` compara a fonte com o desenho em código).

**Na tela:** `CenaTavernaMorelCanto` (a mesma função da vista do balcão, sem o taverneiro); a cena do encontro
(`taverna_mesa`) é agora `CenaTavernaMesa`, que mostra o canto por padrão e a vista do balcão pela faixa ("A mesa do
encontro"). Nada do encontro mudou (os textos, as opções, os preços, os testes).

**Conferido:** a fonte igual ao desenho; `morel/conferir-encontro.mjs` a 1920×945 e 1280×720 com a mesa nova (o
fluxo inteiro: as quatro opções, pagar 40 com clique duplo e tecla repetida, perder e pagar 25, perder sem os 25,
vencer, o Vazio, a bebida, o Esc, a pose parada, o console): tudo certo; as fotos em `morel/capturas/canto/`.

**O que depende do olho do Jean:** a leitura de primeira pessoa e a proximidade; o rosto na escala nova (o tom da
pele, a cicatriz); as ombreiras e as mangas; a parede da esquerda em ângulo; o ciclo de comer nesta postura.

### A revisão dos três pontos (30/10/2026; a candidata revisada, em avaliação)

O Jean aprovou a direção, a proximidade e a composição, e marcou três problemas, sem reiniciar a arte. A primeira
candidata ficou preservada (`morel/canto-v1/canto.aseprite`, exportada em `camadas/morel-canto-v1/`): no painel,
"Morel no canto da taverna, a primeira candidata" e, no encontro, a faixa "A mesa do encontro: no canto, a primeira
candidata". A identidade, a paleta, os objetos, as poses dos braços, o encontro, a alimentação e o pagamento não
mudaram.

1. **A mastigação: o rosto partido.** A causa (na construção, não numa sombra): a variante `mastiga` descia 1 px um
   recorte das linhas da boca para baixo e preenchia o vão só no meio, então dos dois lados da barba ficava a parede à
   mostra, uma faixa de fundo atravessando o rosto (nas quatro poses que a usam, inclusive a da volta à tigela que o
   pagamento reaproveita). Agora a variante é uma grade inteira (`morel.cabeca`): o bigode e as bochechas ficam, a boca
   fechada e um pouco mais curta desce com o queixo, a barba ganha uma linha inteira, com o contorno contínuo.
   Conferido por conta em todas as 20 poses: nenhum pixel de fundo entre os contornos da cabeça, da gola e do tronco.
   Os contatos da colher com a boca não mudaram (a variante `boca` é a mesma).
2. **O tronco e a ligação com o pescoço e a barba.** Antes, um polígono de 92 px (mais largo que as juntas dos ombros)
   enchia o espaço entre os braços, e a gola era uma faixa reta entre o colete e a barba. O estudo
   (`morel/canto/tronco_estudo.py`; as fontes e o que se aproveitou de cada uma na skill `arte-personagens-fenda`,
   `tronco-e-rosto.md`): a caixa torácica pela cabeça (62 px, mais estreita que os ombros), o trapézio, o ombro
   arredondado, a axila em x 141 e 203; abaixo dela, o fundo aparece entre o braço e o tronco onde o braço se afasta. A
   roupa por cima: o casaco aberto acompanhando o tronco, a gola em pé dos dois lados da barba, as lapelas descendo até
   as bordas do colete, o colete fechado até a garganta (a barba por cima dele), as tiras seguindo a curva do peito. A
   grade `morel.TRONCO` saiu da construção e é retocada à mão; a construção fica na camada oculta `construcao`.
3. **A parede da esquerda como plano lateral.** O estudo (na skill `arte-cenas-fenda`, `paredes-laterais.md`): a câmera
   de um ponto (a parede do fundo de frente), então as linhas horizontais da lateral fogem para o mesmo ponto do tampo
   (x 170, y 22), não para um ponto próprio. No canto, as fiadas na altura das do fundo e a travessa virando o canto;
   acima do horizonte as linhas descem para o canto, abaixo sobem; os blocos encurtam para o canto pela profundidade
   (7 px no canto, 36 na borda); a viga de cima mostra a face de baixo e a do meio, a de cima; o esteio da direita
   mostra a face da esquerda. A mesa encosta na parede (antes o tampo atravessava a parede), numa linha que também foge
   para o ponto. As guias ficam na camada oculta `construcao`.

**As folhas** (no painel, "Inspeção ampliada"; antes em cima, depois embaixo): `revisao-mastigacao.png` (repouso, as
três poses de mastigar, a colher na boca, o olhar), `revisao-tronco.png` (sem braços, ombreiras e objetos; e com tudo
em repouso, na boca e olhando), `revisao-parede.png` (o espaço sozinho, com as guias da sala e a cena inteira).

**Conferido:** a fonte remontada (`cena.py --refazer`: a anterior não tinha retoques, `--conferir` dava igual) e
exportada, a fonte igual ao desenho; a conta de fendas nas 20 poses; `morel/conferir-encontro.mjs` a 1920×945 e
1280×720 (o encontro inteiro, as folhas da revisão e a primeira candidata no mesmo estado): tudo certo; as fotos em
`morel/capturas/canto-revisao/` (fora do git). Teste técnico, não aprovação artística.

**Ainda hipótese, para o olho do Jean:** se 1 px de mandíbula lê como mastigar no tamanho do jogo; se a gola em pé
lê como gola; se o vão entre o braço da colher e o tronco lê como espaço; se a convergência forte da parede lê como o
canto de uma sala pequena (ou pede o canto mais para a esquerda, com fugas mais suaves); se a mesa encostada lê bem
com o castiçal junto dela.

### A queda de braço no canto (30/10/2026; a candidata, em avaliação)

**O olhar (o Jean):** igualados na rodada anterior, os olhos ficaram cópias um do outro, e o olhar não ia ao jogador
(o olho aberto era escuro-branco-escuro-branco: a pupila do lado). Agora cada estado tem o seu desenho
(`morel.OLHOS_BAIXO`, `OLHOS_OLHA`): comendo, a pálpebra baixada com o escuro embaixo do olho (para a tigela); olhando
para nós, a íris no meio de cada olho, o branco baixo dos lados e a dobra da pálpebra por cima, o branco do mesmo tom
nos dois olhos (apagado no olho da sombra, parecia faltar). O mesmo `olha` serve à queda de braço (as 4 poses em que ele olha para nós). Antes e depois em
`camadas/morel-canto/revisao-olhar.png`.

**A colher, na quarta revisão (o Jean):** a terceira apagava a colher inteira quando a ponta entrava no caldo (recusado:
Morel segura o cabo fora da tigela), e a colher ainda girava demais entre a coleta e a boca. Agora ela se esconde por
trecho (`morel.colher(mergulha=morel.no_caldo)`: da superfície do caldo para a ponta, não se desenha; `atras_da_borda`:
o que ficaria atrás da borda da frente e do bojo): a haste sai da mão, passa por cima da borda e some no caldo. As
chaves (`juntas.CHAVES`) dão uma colher rígida, um pouco mais longa (20, uns 0,7 do antebraço), com a pega fixa e a
mão um pouco afastada da borda; a direção muda só o que o gesto pede: a ponta para dentro do caldo na coleta, quase
nivelada subindo, um ajuste curto para a boca, onde a concha chega aos lábios. A colher largada na queda de braço
mostra a haste saindo da tigela; a disputa não mudou. Antes e depois em `camadas/morel-canto/revisao-colher.png`.

**A colher, na terceira revisão (o Jean; a ocultação inteira foi recusada na quarta):** ela ainda se distorcia entre os quadros, a ponta aparecia fora da
tigela, ia de encontro à cara em vez de entrar na boca e o braço tinha dois pixels de sujeira. Agora a colher é desenhada
pixel a pixel (`morel.colher`: o cabo numa linha limpa de 1 px com a sombra, a concha em 3 pixels que continuam o cabo),
some inteira na tigela quando a ponta está no caldo (`morel.na_tigela`, também atrás da borda da frente e do bojo), e na
boca nada dela passa da linha dos lábios. A subida e a descida são uma curva só cada (`juntas.SUBIDA`, `DESCIDA`): a mão
não faz mais gancho, e o passo cresce e diminui aos poucos. A sujeira era o vinco do cotovelo da manga, que nesta vista
caía no meio do antebraço: tirado só aqui. O olho da direita tinha 5 px; ficou com 4, como o outro.

**A colher, na segunda revisão (o Jean):** ela mudava de forma subindo para a boca (a mão cobria quase todo o cabo, e
a concha era uma elipse sempre deitada) e, na coleta, a ponta aparecia na borda da frente, como apoiada para fora da
tigela. Agora é uma peça rígida (`morel.colher`: o cabo com a mesma largura em qualquer ângulo, a concha girando com
ele), a mão um pouco mais perto do pulso (o cabo aparece além dela; a ponta na boca não mudou), e o que cai no caldo
não se desenha (`morel.no_caldo`): na coleta, o cabo passa por cima da borda de trás e a ponta fica mergulhada; saindo,
ela reaparece. Solta antes da queda de braço, ela fica assim na tigela e vai junto quando a tigela é varrida.

**Antes, as três correções da alimentação** (a câmera, a perspectiva, o cenário, o tronco, a gola e a mastigação ficam; a versão anterior, preservada em `morel/canto-v2/` e `camadas/morel-canto-v2/`, no painel e na faixa da mesa):
- **a colher** era de madeira nos tons do tampo: pousada, coincidia com a borda dele; subindo, parecia um pedaço da
  mesa que se soltou. Agora é de metal, no cinza do estanho da caneca (`morel.COLHER`), e, pousada, fica dentro da
  tigela (o pulso junto da borda dela), não ao longo da borda do tampo;
- **a coleta**: a ponta buscava comida na borda da tigela; agora pega o caldo por dentro da boca dela (`juntas.CHAVES`:
  o pulso 8 px mais perto e a colher descendo para dentro; a passagem mais longa da ponta fica em 11 px, como antes);
- **o cotovelo e a caneca**: nas poses de repouso e de coleta, o cotovelo pousava em cima da caneca. A caneca veio 4 px
  para perto da vela e, com o pulso mais perto da tigela, o cotovelo também se afastou dela: conferido por conta, o
  braço não toca a caneca em nenhuma das 20 poses (8 px de folga no mínimo), o que vale também para a reação ao
  pagamento, que usa as mesmas poses.

**A construção** (`morel/queda-canto/geometria.py`, pela skill `arte-personagens-fenda`, "Dois corpos ligados por um
contato"): a câmera do canto lida como perspectiva (o horizonte em y 22, o ponto em x 170, 140 px de distância focal: a
borda de lá do tampo a 109 cm, o olho 39 cm acima dele, a borda de baixo do quadro a 74 cm). Os cotovelos ficam: o de
Morel no tampo, à frente do ombro direito dele; o nosso fora do quadro, embaixo (a 58 cm; o antebraço é cortado pela
borda antes dele). Com os antebraços e as mãos de comprimento fixo, a pega anda num círculo; quem vence leva a mão do
outro para a própria esquerda. A disposição dos cotovelos saiu de uma busca com números: com os dois quase alinhados em
profundidade, o nosso antebraço cobria o dele; com 26 cm de lado, os dois aparecem na disputa (o dele à esquerda, o
nosso entrando pela direita), a pega fica na frente do peito (y 46, abaixo da barba) e os dois fins caem no tampo, longe
do pão (a mão dele em x ~129) e da tigela (a nossa em x ~195).

**A preparação** (no encontro, enquanto o dado rola): Morel volta ao repouso pelo caminho do pagamento e olha para nós;
solta a colher, que fica mergulhada na tigela; a mão esquerda sai do tampo para o colo (onde ela estava, a nossa mão cai
quando ele vence); o antebraço direito deita no tampo e **varre a tigela para a direita com o lado de fora** (a mão de
cutelo encostada na borda da esquerda dela, o cotovelo deslizando junto, o tronco inclinando para alcançar), na mesma
profundidade, no meio do tampo (não na borda de lá); o braço vai ao meio, o cotovelo pousa; o nosso antebraço entra pela
borda de baixo; a pega se firma. **A disputa** (o método da `queda-vista`): quem perde ganha um pouco primeiro e segura, o outro recupera;
o tronco dele pende 1 px para o lado em que força. **Os derrubes**, devagar no começo e acelerando até o tampo; a pausa;
as mãos se soltam, o nosso braço sai por baixo e o dele pousa no tampo (o depois, que fica: a conversa continua no
texto; nada volta a comer).

**No encontro, pelo motor:** o `demo.py` embrulha o teste de Força do evento: quando ele começa, a cena recebe
`prepara` (a preparação e a disputa); quando o motor decide, `nos` ou `morel` (o derrube desse resultado). Os textos, os
preços, o pagamento e o teste não mudaram; perdendo e pagando os 25, as moedas caem na mesa do depois. **No painel:**
"Queda de braço no canto, candidata: ... nós vencemos" e "... Morel vence" (da comida ao depois, uma vez; o depois fica),
"Queda de braço no canto: repetir do começo" (um reinício: o repouso parado, depois a sequência de novo; não é uma
transição animada) e as folhas "as poses principais" e "todas as poses". **Movimento reduzido:** a disputa parada, o fim
e o depois, sem passagens.

**A fonte** `morel/queda-canto/queda-canto.aseprite` (41 poses com as etiquetas; as camadas `construcao` e `juntas`
ocultas): montada por `poses.py --criar` a partir do código da cena do canto (igual à fonte dela); `exportar.py` lê dela
(`camadas/morel-canto/queda-canto.png` e `.json`, as folhas `queda-canto-poses.png` e `queda-canto-sequencia.png`);
`--conferir` compara a fonte com o desenho.

**Conferido:** as duas fontes iguais ao desenho; `morel/conferir-encontro.mjs` a 1920×945 e 1280×720 (o encontro
inteiro; a cena recebe `prepara` e depois o resultado do motor; a preparação, a disputa e cada desfecho no encontro; as
duas candidatas no painel, o depois que fica, o reinício, a pose parada, as folhas): tudo certo; as fotos em
`morel/capturas/queda-canto/` (fora do git). Teste técnico, não aprovação artística.

**Limitações visuais à vista (para o olho do Jean):**
- o texto do resultado ("Seu braço bate na mesa...") aparece logo depois do dado, enquanto a cena ainda está na
  disputa: o derrube vem uns 5 s depois do texto (segurar o texto até o derrube mexeria no fluxo da tela, fora deste
  protótipo);
- com esta câmera, o tampo visível tem só uns 35 cm de profundidade: na nossa vitória, a mão de Morel deita perto da
  borda de baixo, e no meio desse derrube (as poses 4 e 5) o nosso antebraço passa na frente do dele (é a profundidade
  real: o nosso está mais perto); no fim, o antebraço dele volta a aparecer, do cotovelo à mão;
- na derrota, o nosso antebraço deita apontando para o fundo e fica curto na tela (uns 20 px), largo e com a palma para
  cima: é o escorço de verdade, mas pode ler como um toco;
- a pega são dois volumes de mão em três tons cada, a dele um degrau mais escura: distinguíveis no zoom, pequenos no
  tamanho do jogo.

## O encontro à mesa de Morel (30/10/2026; protótipo)

**O fluxo, pelo caminho normal.** Entrar na taverna mostra o balcão (G4). O evento de sempre, `morel_na_taverna` (pelo
cartão "Sentar com o homem do canto" da abertura, enquanto ele nunca apareceu, ou pela bebida, com as condições do
evento: dia 2 em diante, livre, até 3 vezes, o intervalo), abre a vista diante de Morel no quadro de cima, com o texto e
as opções do evento embaixo. Nada do evento muda: os textos, os preços (40; 25 depois de perder), os testes (Força 14,
Carisma 15), as consequências (a vaga na comitiva, a simpatia). Terminada a conversa (pagando, vencendo, perdendo sem
os 25, recusando, o Vazio), o balcão da taverna continua aberto até o Voltar à vila, como o templo faz (a meta `balcao`);
recrutado ou já apresentado, o cartão do homem do canto sai, pela regra da abertura.
- **Como:** `demo.py` embrulha a função do evento (`a_mesa`): ao começar, manda a cena `taverna_mesa` (a vista de Morel;
  uma cena à parte, porque o `vila.js` tira os interiores quando aparece outro menu); a cada ouro que o motor cobra de
  fato (`perder_ouro`), manda a mesma cena com mais um pagamento. A tela lança as moedas uma vez por pagamento contado
  pelo motor: clique duplo, tecla repetida, Esc ou o texto adiantado não cobram de novo nem lançam outra vez.
- **O nome:** a mesa "do homem do canto" antes de conhecê-lo, "de Morel" depois (pela contagem do evento); o texto do
  evento é o de sempre (ele se apresenta nele).

**O pagamento sobre a mesa** (`morel/moedas/`: a fonte `moedas.aseprite`, desenhada em grade à mão, e `moedas.py`).
Cinco moedas (não quarenta), de latão da paleta da cena, com 3 px (a escala da vista): entram pela borda de baixo, de
quem está sentado, voam girando (deitada, de quina, de pé), passam por cima da borda da mesa, caem no tampo entre a vela
e a tigela, dão um pulinho de 2 px e outro de 1, escorregam 1 px; uma cai de pé, rola 3 px e tomba. A sombra corre no
tampo embaixo de cada uma e encosta quando ela assenta. 12 tiques (1,2 s); as moedas ficam na mesa até a cena acabar (a
volta ao balcão), sem sumir. A mesma animação nos 40 e nos 25 (o texto, a opção e o ouro da HUD dizem o valor).
- **Morel** para de comer: a colher volta ao descanso pelo caminho mais curto entre as poses aprovadas (termina de descer,
  ou desfaz a subida e pousa na tigela), os olhos ficam baixos, nas moedas, enquanto elas caem e ele conta, depois ele
  olha para quem pagou (a pose `olha`) e volta à tigela; a rotina recomeça do começo. Nenhuma pose nova.
- **Movimento reduzido:** as moedas já assentadas e Morel parado.

**Os casos de teste da faixa** (só valem onde as regras do evento já deixam): o ouro ("Homem do canto" com 60, com 30 —
sem os 40 — e com 10 — nem os 25); o dado da queda de braço (o sorteio, o dado em 20, o dado em 1: só no teste de Força
desse evento; a conta e a rolagem na tela são as do motor); "Bebida: Morel puxa conversa" (força o evento na próxima
bebida só quando ele é candidato agora). `morel/conferir-encontro.mjs` percorre os casos a 1920×945 e 1280×720.

**A opção do Vazio** fica com a apresentação normal: o texto conduz, a regra e a consequência são as do evento.

### Roteiro curto para testar

1. `demo.bat`, entrar na taverna pelo prédio: o balcão animado.
2. Cartão "Sentar com o homem do canto": a mesa de Morel (no canto, a nova direção; a vista diante do balcão pela
   faixa, "A mesa do encontro: diante do balcão"), as quatro opções. "Pagar 40 ouro" (pode clicar duas vezes): as
   moedas caem, Morel para, olha; o ouro cai 40 uma vez. Aceitar: de volta ao balcão, sem o cartão.
3. Faixa "Homem do canto, 30 de ouro" e "Queda de braço: o dado em 1": sem os 40; a queda de braço perdida, "Pagar 25":
   as mesmas moedas; o ouro vai a 5.
4. "Homem do canto, 10 de ouro" com o dado em 1: perde e a conversa acaba (sem a pergunta dos 25).
5. "Morel conhecido" e "Bebida: Morel puxa conversa": a bebida leva à mesa de Morel (já conhecido).
6. "Pose parada": as moedas já na mesa, nada se mexe.
7. A pose central da queda de braço: "Queda de braço, terceira proposta: a disputa" no painel (na área de cena); a
   comparação com a vista aprovada e as guias em "Inspeção ampliada"; as propostas anteriores, para comparar, em
   "segunda proposta" e "primeira proposta". Para ver o dado: com a pose à vista, um teste de Força (no console,
   `rolagem({atributo: "Força", cd: 14, d20: 10, mod: 4, total: 14, sucesso: true})`) rola embaixo da arte.
8. **A queda de braço na vista aprovada (a candidata):** no painel, "Queda de braço na vista aprovada (o queda 1
   refinado), animada: nós vencemos" e "...: Morel vence" (a sequência inteira, em volta, a partir do momento em que
   aparece); "Pose parada" para o movimento reduzido; o dado por cima pelo mesmo comando do console. Para comparar: a
   vista aprovada ("Diante de Morel (animada)"), a primeira candidata ("a primeira candidata (Morel na postura da
   conversa)") e o queda 1 antes ("primeira proposta (o queda 1, antes do refinamento)"). Na inspeção ampliada: a
   comparação, as 22 poses com a construção e as trajetórias.

## A queda de braço na vista aprovada: o queda 1 refeito pela postura (30/10/2026; a candidata, em avaliação)

**O pedido do Jean:** com a vista de Morel sentado aprovada, voltar ao queda 1 e refiná-lo com a cena aprovada como
autoridade (a identidade, o estilo, o cenário, a câmera): a disputa naquela mesa, diante daquele Morel; mãos simples;
a estrutura sem aparecer; nada de regra nova nem de produção.

**A primeira candidata e por que ela foi refeita.** Ela reaproveitou a vista e resolveu o acabamento (a manga
aprovada nos dois braços, a pega em duas bolinhas, a luz num tom só sobre as figuras), mas partiu de Morel na postura
da conversa: o nosso braço atravessava a mesa para alcançá-lo e, na nossa derrota, parecia uma peça dobrada tombando.
Para a vitória dele ter curso, ela chegou a arrastar o cotovelo dele (recusado: um remendo, não uma construção). O
Jean pediu a postura de origem refeita, os dois desfechos com os apoios parados, o corpo participando além do braço, e
a face interna do nosso antebraço quando ele deita. A primeira candidata fica no painel ("a primeira candidata");
a fonte em `morel/queda-vista/v1/`, as camadas em `camadas/morel-vista-qv1/`.

**As referências** (busca, 30/10/2026): o cotovelo à frente de quem disputa, perto do peito e centrado no corpo; o
ombro um pouco à frente; quem vence põe o corpo por cima do braço e empurra com o tronco; no "press", a palma de quem
perde termina virada para o teto, com a mão do vencedor por cima (fitnessvolt.com, "Arm Wrestling Techniques";
nzarmwrestling.co.nz, "Basic moves").

**A construção** (`morel/queda-vista/geometria.py`; o estudo das cinco poses, em formas simples sobre a cena, está na
folha "as 22 poses, a construção em cima"):
- **Morel se debruça:** o tronco desce 3 px e vem 2 para o meio; a cabeça desce 2 a mais (de frente, um debruçar se lê
  pelo pescoço que encurta). O ombro direito vem junto (a 134 cm, 8 à frente da conversa) e, com o braço de cima de
  31 cm até o tampo, o cotovelo cai à frente do meio do tronco dele.
- **Nós, colados ao apoio:** o cotovelo à frente do nosso peito, a 3 cm da nossa borda; o braço de cima desce quase
  reto para fora do quadro. Com esta câmera (74 cm atrás da borda), o nosso ombro de verdade cairia dentro do quadro,
  com o tronco por cima da mesa; o braço que desce reto diz "estamos na mesa" sem mudar a cena.
- **O encontro no meio do tampo:** os cotovelos a 45 cm; a projeção da pega no tampo cai no meio entre as duas bordas
  (y 77 de 62 a 92) e entre os dois corpos; a pega fica logo abaixo do queixo de Morel debruçado. Com o olho 33 cm
  acima do tampo, uma pega na altura real (~28 cm) cai na linha do queixo dele: por isso ele precisa se debruçar, e por
  isso os cotovelos não ficam mais perto (a pega subiria para o rosto).
- **Os dois desfechos com os apoios parados:** a linha dos cotovelos corre quase na direção da câmera (22° de lado),
  então os dois fins correm para os lados: na nossa vitória, o antebraço dele deita para a esquerda e aparece acima do
  nosso (26 px); na nossa derrota, o nosso deita para a direita (20 px; o pão saiu dali para a esquerda da caneca).
- **A face interna:** perdendo, o nosso antebraço gira com a palma para cima ao descer (a partir de um quinto do
  derrube): deitado, a face larga de dentro vira para cima e para a câmera, e a forma lê achatada (o topo largo num
  tom aceso, a borda de baixo estreita e escura, a dobra do cotovelo por cima, a ponta do cotovelo para baixo, sem o
  realce que a fazia ler como um joelho); a mão de Morel por cima da nossa.
- **O corpo participa:** o tronco e a cabeça de Morel pose a pose (ajeita-se e se debruça enquanto a pega se firma;
  pende 1 px para o lado de quem força; cede para a direita dele e desce quando perde; vem por cima quando vence: o
  ombro passa sobre o cotovelo e a cabeça desce sobre a pega), com o ombro do braço sempre a no máximo 1,3 px do ombro
  do tronco; o nosso ombro, fora do quadro, entra quando empurramos.

**O acabamento** (`poses.py`, o mesmo da primeira candidata): a manga aprovada nos dois braços (a dele em couro, a
nossa em lã), a ombreira direita aprovada acompanhando o ombro, o braço de cima dele recuando atrás do antebraço na
disputa, a luz da sala num tom só sobre os braços e as mãos, a pega em duas bolinhas sobrepostas, a tigela atrás da
vela e a mão livre dele no colo.

**A animação** (22 poses na fonte `queda-vista.aseprite`; `geometria.CICLO`, 93 tiques de 100 ms por desfecho): a
pega se firma enquanto ele se debruça; a disputa com intenção, poses de 3 a 8 tiques, a pega andando 1 a 2 px por
troca; o derrube devagar no começo e acelerando até o tampo (1 tique cada no fim); o impacto (o tronco cede 1 px) e a
pausa de 2,8 s. Os cotovelos não saem do lugar em nenhuma pose. Movimento reduzido: a pose do meio durante a disputa e
a final depois. Em volta, o fim emenda no começo por um corte (a volta à conversa, não feita).

**A cena** (`tela/cena-taverna-anim.js`, `CenaTavernaQuedaVista`): o fundo, a pose da vez na caixa dela e as chamas
da vista por cima. `exportar.py` só lê a fonte; `--conferir` compara a fonte com o desenho em código.

**Conferido** (`queda-vista/conferir.mjs`, a 1920×945 e 1280×720): em oito poses de cada desfecho, a pose que a linha
do tempo pede e o canvas igual à exportação, pixel a pixel; a emenda; o movimento reduzido; o dado embaixo da arte; a
volta à vista aprovada, à primeira candidata e ao queda 1; o console. A fonte igual ao desenho. O código do jogo e o
encontro não mudaram.

**O que depende do olho do Jean:** se Morel lê preparado para disputar; se o nosso braço, colado à borda, deixou de
parecer longo; o antebraço deitado com a face de dentro para cima; a pega no tamanho do jogo; na disputa, o antebraço
dele fica estreito entre o braço de cima dele e o nosso.

## A queda de braço: a pose central desenhada à mão (30/10/2026; a terceira proposta, histórico)

**O pedido do Jean:** a segunda proposta separava bem os braços, mas o acabamento parecia um modelo 3D simplificado em
baixa resolução (os braços como tubos facetados, o peito um bloco com o vermelho aplicado como placa, a ombreira
arredondada, as juntas do boneco à mostra, o pontilhado igual em áreas grandes). Só a pose central, para acertar a
linguagem: a construção como guia oculta e o acabamento redesenhado por cima, com a vista aprovada de Morel comendo ao
lado; a câmera um pouco mais baixa e menos inclinada; mãos simples (duas formas, um polegar no máximo); o dado inteiro
e a disputa à vista enquanto ele gira.

**A câmera** (`morel/queda3/juntas.py`): 40° do nosso lado e 15° acima do tampo (antes 50° e 30°), um pouco mais perto
(~2 px por cm na pega), a pega no meio do quadro, em (150, 26). O tampo vira uma faixa; Morel ganha porte (o peito, a
ombreira, a ponta da barba no alto); à esquerda entram a vela, a caneca e a tigela deslizada (objetos da cena aprovada,
na mesma mesa), no lugar da parede vazia. O nosso ombro fica no canto de baixo, na sombra (desta altura ele entra no
quadro; o tronco, não). Os dois derrubes continuam correndo de lado e cabem no quadro (a guia `guia_vitorias`: o arco
da pega e os dois fins, com os antebraços de quem perde).

**O desenho** (`morel/queda3/pose.py`, a fonte `disputa.aseprite`; a autoridade é a fonte): cada elemento é uma silhueta
e grupos de luz escolhidos à mão, não volume calculado: o tampo com as juntas para o ponto de fuga, o halo da vela (o
único pontilhado grande, na passagem da luz), as arestas; a frente do balcão no escuro, esquentando para a esquerda; o
peito de Morel (o couro em tons de bloco, mais escuro atrás do braço direito, com a sombra que o braço faz no peito; a
lapela acesa; o colete sobre o corpo, com a borda clara do lado da vela, a costura, as duas tiras curvando com o peito e
as fivelas quadradas; a gola, o pescoço e a borda da barba; o punho da espada; a ombreira em cunha, estreita e escura,
como na vista, com o pontilhado só nela); o braço direito dele (a manga de couro com a aresta acesa, a costura do ombro,
as dobras de dentro do cotovelo, o antebraço um tom abaixo, o punho escuro, a sombra do cotovelo no tampo); o esquerdo
saindo da ombreira até a mão na borda de lá; o nosso antebraço de lã (a aresta acesa, as dobras perto do cotovelo, o
punho escuro); a pega em duas formas (a nossa mão na frente, mais clara, com o polegar por cima; a de Morel atrás, mais
escura e quente, o nó do polegar em cima e os dedos numa faixa só dobrada sobre a borda do nosso punho). As camadas da
construção (`guia`) e dos derrubes (`guia_vitorias`) ficam ocultas e fora da exportação.

**O dado** (`tela/rolagem-queda.js`, só no protótipo): a captura que mostrava o dado cortado era um recorte da
conferência; na tela inteira ele estava inteiro. O que atrapalhava era o layout: o grupo do dado centrado na altura da
cena e o véu escurecendo a arte. Com a pose da queda de braço à vista, o grupo desce para logo embaixo da arte (inteiro
na janela; a doca fica atrás dele por um instante) e o véu cobre só a página: a disputa fica clara enquanto o dado
gira. O dado, o tempo, o som, o resultado e a descida até a tirinha são os do jogo.

**Conferido:** a fonte exportada idêntica ao desenho; a pose na área de cena a 1920×945 e 1280×720, sozinha e com o dado
(o dado inteiro, embaixo da arte, o véu fora da disputa); a folha lado a lado com a vista aprovada.
**O que depende do olho do Jean:** se o acabamento está na linguagem da vista aprovada (o couro, o colete sobre o corpo,
a ombreira, as mãos simples); se a pega lê firme e cada mão segue até o seu antebraço; se o nosso ombro no canto e o
enquadramento funcionam no jogo.

A sequência futura continua a mesma (preparar a pega, o esforço contido enquanto o dado gira, revelar o resultado, o
derrube, a pausa), e a continuidade da tigela também (abaixo, na segunda proposta).

## A queda de braço: a vista de detalhe (30/10/2026; a segunda proposta, histórico)

Recusada no acabamento (acima); a câmera, a pesquisa, a construção e a continuidade da tigela continuam valendo.

**O pedido do Jean:** a primeira proposta não comunicava a disputa (as mãos numa massa só, a mão derrubada indistinta na
nossa vitória, o nosso antebraço parecendo em pé na de Morel, a ação pequena na câmera da conversa). Uma vista própria,
próxima, um pouco de lado e acima do tampo, com a pega no centro da ação, os dois cotovelos apoiados, o peito de Morel
ao fundo; construída com formas simples antes do acabamento; as vitórias reconhecíveis sem legenda nem só pela sombra.

**As referências reais** (as regras e a mesa da WAF, World Armwrestling Federation): a pega palma com palma, os
polegares cruzados em cima e o nó do polegar à vista, os punhos retos no começo; os cotovelos nas almofadas, quase
alinhados (uns 38 cm, na direção de um para o outro), parados até o fim; a mão perdedora vai à almofada que fica à
esquerda de quem vence (braço direito): **o derrube corre de lado**, não para longe nem para perto.

**A câmera** (`morel/queda2/juntas.py`, uma câmera de verdade em números): de detalhe, não os nossos olhos; 50° a leste
do nosso lado e 30° acima do tampo, a ~2 px por cm na pega (a conversa tem 0,9). Assim o V da disputa abre (de trás de
nós, um antebraço esconde o outro), os dois derrubes correm para os lados do quadro (nós vencendo, para a esquerda;
Morel vencendo, para a direita), e o braço de quem perde fica deitado e comprido no tampo, atravessado. Os esboços que
levaram a ela (de trás, de lado demais) estão descritos no `juntas.py`. **O dado** dos testes rola no meio do palco; a
pega da disputa fica no alto e à esquerda, fora dele nas duas janelas (medido); a 1280×720 o dado cobre o cotovelo de
Morel enquanto rola, não a pega nem os antebraços.

**O lugar:** a mesa da conversa (70 cm de fundo, comprida para o oeste, a quina de leste perto do pão); a disputa fica
15 cm a oeste do eixo, diante do peito de Morel, para os dois derrubes caberem no tampo. Ao fundo, a frente do balcão no
escuro, com a luz do lampião no alto à direita (o tampo do balcão fica fora do quadro, desta altura); essa área quieta é
onde o dado rola. De Morel se vê o peito (o couro, o colete vermelho com as duas fivelas, a ombreira do ombro esquerdo,
o pescoço e a borda da barba no alto); o braço esquerdo dele agarra a borda de lá da mesa. Do nosso lado, o braço de lã
azul-acinzentada sai pela borda da esquerda (o tronco, fora do quadro).

**O estudo** (`estudo-queda2.aseprite`, `estudo.py`): as três poses em formas simples (Morel em vermelho e laranja, o
braço esquerdo dele mais escuro, nós em azul; as pegas construídas por partes), com as juntas, a linha dos cotovelos e o
arco da pega na camada `guia` e a área do dado na `dado`; o percurso (as três pegas e o arco sobre a disputa); a planta
(a mesa vista de cima: os cotovelos, o caminho da pega, os dois derrubes, a tigela no lugar de antes e no novo, a vela,
a caneca, o pão); e as três pegas construídas, ampliadas 3×, nas cores das partes (`maos.py`: os punhos, um dedo por
cápsula, os polegares; nos fins, a mão de quem perde de dorso no tampo, passando um pouco do punho de quem vence).
Conferido: os cotovelos parados; o braço de cima com 30 cm e os antebraços com 27 e 28 em todas as poses; a pega a
27 cm do tampo na disputa e a 5 cm nos fins; cada antebraço gira em volta do cotovelo, no mesmo plano.

**As poses acabadas** (`queda2.aseprite`, `poses.py`; a fonte é a autoridade, e a exportação sai dela idêntica ao
desenho): os volumes (os braços, o peito, a pega) projetados pela câmera, cada pixel na camada da superfície mais perto
(`desenho.py`), iluminados pela vela e pela lareira em degraus de tom, sem contorno, com as paletas aprovadas (o couro e
a pele de Morel, o colete, o aço, a madeira do tampo, a tigela); a sombra de contato no tampo onde o braço encosta. A
pega separada pelo valor: a pele de Morel mais escura e quente que a nossa; um pixel de sombra onde uma parte passa atrás
da outra; os pontinhos limpos; e, na disputa, os dedos de Morel sobre o nosso dorso retocados à mão em listras (o lado
de cima claro, o vão escuro). 1. A disputa: o V, a pega no alto, os polegares em cima. 2. Nós vencemos: o braço de
Morel deitado e comprido para a esquerda, a mão dele de dorso no tampo, os dedos dela além do nosso punho, fechado por
cima. 3. Morel vence: o nosso braço deitado para a direita, a nossa mão de dorso no tampo, o punho dele por cima.

**O que depende do olho do Jean:** se as duas vitórias se reconhecem sem legenda, no tamanho da HUD; se a pega lê como
duas mãos (e não uma massa); se o peito de Morel, feito por volume calculado e acabamento em degraus, segura a identidade
ao lado das cenas desenhadas à mão; se o fundo quieto à direita (onde o dado rola) pesa na composição parada.

**A tigela, a colher e os objetos** (para a animação): antes da disputa, Morel larga a colher dentro da tigela e, com a
mesma mão, desliza a tigela pela metade de lá da mesa para a direita dele (oeste), num empurrão, para além da coluna da
vela (na vista de detalhe, ela fica no canto de cima à esquerda); na vista da conversa, é o braço da colher indo para a
esquerda da tela e a tigela parando atrás da vela. Depois da disputa, de volta à conversa, ele puxa a tigela pelo mesmo
caminho e pega a colher antes de voltar a comer. A caneca, a vela e o pão não se mexem. As moedas do pagamento de 25 só
caem depois, na vista da conversa, com a tigela já no lugar.

**A animação, depois das poses aprovadas** (só a intenção, ligada à rolagem que já existe; nada feito):
1. Ao escolher a queda de braço: o corte para a vista de detalhe; a pega se firma (as mãos se ajeitam, os ombros descem).
2. Enquanto o dado gira (os 950 ms dele, mais o tempo de leitura): os dois fazem força na posição central, com uma
   tremida contida nas mãos e nos antebraços (a pega oscila 1 px pelo arco, um deslocamento curto e a recuperação), sem
   antecipar quem vence; os cotovelos não deslizam, as mãos não se soltam, a tela não treme.
3. Quando o dado mostra o resultado: o tempo de lê-lo e o desfecho que o motor já decidiu (o teste de Força 14 roda uma
   vez; a animação não muda chances, não cria outro teste nem repete consequências).
4. O derrube: quem vence leva a mão do outro pelo arco até o tampo, acelerando no fim; um impacto curto e a acomodação.
5. Uma pausa na posição final, para ficar claro quem venceu; depois a volta à conversa e às consequências de sempre.
Movimento reduzido: a posição central durante a rolagem e a pose final, sem tremida nem impacto.

## A queda de braço: a primeira proposta (30/10/2026; histórico)

Substituída pela vista de detalhe (acima), depois da avaliação do Jean; o plano de animação desta seção também. Fica no
painel para comparar ("primeira proposta (o queda 1) 1/2/3"), com o estudo dela (`morel/queda/`). Depois, o Jean
voltou a ela: a candidata refinada e animada está em "A queda de braço na vista aprovada" (acima).

**O enquadramento:** a câmera da vista aprovada, o mesmo pixel, não outra mais perto. Assim Morel (o rosto, a cicatriz,
o colete), a sala e a mesa ficam como foram aprovados, a disputa ocupa o meio do quadro e nada precisa ser redesenhado
noutra escala; o nosso antebraço entra pelo primeiro plano, o braço de cima sai pela borda de baixo (o ombro fica
embaixo da câmera, sem escorço do ombro nem do peito). Se o Jean quiser a disputa maior, o passo seguinte é uma câmera
mais perto (Morel e a mesa redesenhados nela), não um recorte ampliado.

**O estudo** (`morel/queda/`, pela `arte-personagens-fenda` e a `arte-cenas-fenda`): `juntas.py` dá a câmera da vista
em números (as tábuas fogem para (238, 30); uma câmera de furo reproduz as bordas do tampo e o ombro de Morel) e as
juntas das três poses: os dois cotovelos fincados no tampo e parados; o antebraço de Morel 28 cm e o nosso 27 (mais 6 até
o meio da pega); as mãos só onde as duas distâncias batem (um círculo no plano que corta ao meio a linha dos cotovelos);
no alto dele a disputa, caindo para a esquerda de quem vence até o dorso da mão de quem perde tocar o tampo (4 cm).
Nenhum braço torce: cada antebraço gira em volta do cotovelo, no mesmo plano. `estudo-queda.aseprite` (`estudo.py`) tem
as três poses em formas simples (Morel em vermelho e laranja, nós em azul, as juntas e o arco da pega na `guia`), a
mesa vista de cima (os cotovelos, o caminho da pega, os dois fins, a tigela, a vela, a caneca e o pão) e a pega
ampliada, à mão em grade: o nosso dorso na frente, os nossos dedos sobre o dorso da mão dele (à esquerda), os dele sobre
o nosso (à direita), os polegares cruzados em cima. A pega da cena é ela simplificada em bolinhas de pele.

**As poses** (`queda.aseprite`, `poses.py`; a autoridade é a fonte): 1. a disputa, a pega firme no alto, diante do peito
de Morel; 2. nós vencemos, a mão dele presa no tampo à nossa esquerda, perto de nós; 3. Morel vence, a nossa presa à
direita, longe. A pilha é a da vista aprovada (a sala, o taverneiro e o fogo parados, a luz em multiplicar e somar);
Morel com o corpo e a cabeça da pose `olha` (os olhos em nós), deslocados 1 px a cada 2 do ombro (ele se inclina na
disputa, cede no lado em que perde, vem por cima quando vence); os braços vestidos pelo método do `vestir.lua` (o couro
dele em volume, o antebraço um tom abaixo, a sombra no braço e no casaco, o vinco, o punho escuro, a sombra de um pixel
no tampo onde encosta); a nossa manga de lã azul-acinzentada e a nossa pele um pouco mais clara (os dois se distinguem
pela cor e pela sobreposição); o braço esquerdo dele planta a mão no tampo à direita do nosso antebraço. A tigela saiu
da área dos cotovelos: empurrada 46 px para a direita dele (a nossa esquerda), na mesma linha do tampo; o lugar dela
ganhou as tábuas e as juntas pelas linhas de fuga. O pão fica (o nosso cotovelo pousa à esquerda dele).
- **Conferido:** os cotovelos no tampo e os antebraços com o mesmo comprimento nas três poses (`juntas.py`); as poses na
  área de cena a 1920×945 e 1280×720; o estudo e as poses lado a lado (`queda-construcao.png`).
- **O que depende do olho do Jean:** se a pega lê como duas mãos agarradas no tamanho real; se a vitória de Morel lê como
  o nosso braço deitado (o antebraço aponta para longe e aparece curto, em pé na tela; a sombra no tampo é a única
  pista); se o enquadramento da vista basta ou se a disputa pede a câmera mais perto.

**A animação, depois das poses aprovadas** (só a intenção; nada feito): (1) Morel puxa a tigela para a direita dele com
a mão da colher e apoia o cotovelo; a pega se firma (as mãos se ajeitam 1 px, os ombros descem); (2) a disputa curta, a
resistência legível em poucas poses sustentadas (a pega oscila 1 a 2 px no arco, o ombro de quem força desce); (3) o
desfecho pelo resultado que o motor já decidiu (o teste de Força 14 roda antes; a animação não muda nem repete a
rolagem): a pega cai pelo arco até o tampo do lado de quem vence; (4) uma pausa curta na posição final; (5) a volta à
vista normal: as mãos se soltam e Morel puxa a tigela de volta antes de comer (ela não pula de lugar). Sem minigame,
comandos de força ou interação que não existe; sem som.

## O balcão animado (G4)

**O estado anterior** (29/10/2026): **o balcão aprovado** (a G2, com os retoques locais da G3) agora **animado** na **G4**: o
taverneiro limpa a caneca (na segunda atuação, com as mãos e os braços; o tronco firme) e para para olhar os
fregueses. **A vista diante de Morel**, saída do estudo livre (que o Jean
gostou), foi **adaptada ao acabamento do jogo e animada**, e continua **em avaliação**; na terceira passada, o braço
foi refeito a partir de um **estudo de construção** (a pesquisa, o boneco com formas simples, os comprimentos fixos) que
virou a skill `arte-personagens-fenda`; ela está aprovada para a avaliação e não mudou nesta rodada. As duas no mesmo `demo.bat`, com a pose parada de cada uma e as versões
anteriores para comparar. Nada integrado; sem som, diálogo ou regra nova.

## A G4: o balcão aprovado, animado

**A base:** a fonte da G3 (a G2 aprovada com os retoques locais), sem mudar a composição; mais o garrafão empalhado,
que era a "garrafa bojuda amarelada" marcada pelo Jean (o bojo torto, o gargalo fora do eixo): refeito simétrico, no
eixo x 207, a base reta apoiada na tábua, o gargalo de vidro de 3 px no meio (`g4/fonte.py`, `garrafao`). As duas
garrafas corrigidas na G3 (a de vinho e a bojuda de âmbar) ficam como estão.

**A rotina** (`g4/taverneiro.py`, pela seção 5b da skill, "Quanto do corpo participa"). A segunda versão da atuação
(29/10/2026): na primeira, o tronco (com a caneca e as duas mãos) descia 1 px a cada passada e a cabeça ia junto, e o
Jean viu o corpo inteiro limpando a caneca de um jeito forçado. Limpar uma caneca é trabalho de mãos (pouco esforço,
alcance curto), então as mãos conduzem e o tronco dá a base:

| Trecho | Conduz | Acompanha | Fica |
|---|---|---|---|
| Esfregar (três passadas, uma lenta, mais uma) | a mão do pano dá uma volta pela parede de cá da caneca: sobe, atravessa, desce fazendo força, volta (até 2 px; no máximo 1 px para o lado) | o antebraço do pano (sai do cotovelo); o cotovelo 1 px para dentro quando a mão atravessa a parede e 1 px abaixo na pressão; o ombro do pano 1 px abaixo só na pressão; a ponta do pano 1 px atrás da mão, caindo de volta | o tronco, a cabeça (os olhos baixos, na caneca), a caneca e a mão da asa |
| Ajustar a pega (na passada lenta) | a mão da asa ergue a caneca 1 px | a mão do pano e o pano da borda, que vão com ela | o tronco, a cabeça |
| Olhar os fregueses (a pausa, uma ação própria) | os olhos sobem primeiro (o olhar de lado da G) | a cabeça sobe 1 px um tique depois; depois o olhar vai para o outro lado; volta | as duas mãos na caneca, o tronco |

9 poses, sustentadas de 2 a 24 tiques (a pressão 3 ou 4); o ciclo tem 122 tiques (12,2 s, a 100 ms) e emenda na mesma
pose em que começa. Enquanto ele esfrega, a cabeça não muda um pixel (na primeira versão, até 329 px por troca de pose).
A pose parada (o movimento reduzido) é a da G3: o olhar de lado, desconfiado. A atuação anterior fica no painel
("Balcão animado, a atuação anterior": a fonte em `g4/aseprite-v1/`, as camadas em `camadas/g4-v1/`); o desenho, o
enquadramento, os objetos e o balcão são os mesmos (o fundo, a frente e as chamas saem idênticos).

**A dobra na pega** (o Jean marcou o vazio entre a mão do pano e a caneca): uma dobra de 3 px (x 153 a 155, y 55 a 59
na pose da G) liga o pano que entra pela boca ao que pende da mão; a crista pega a luz, uma sombra curta separa o
tecido do metal e dos dedos. Depois (o Jean viu o pano entrando na caneca e um pedaço da borda aparecendo atrás dele
na pressão): ele limpa o lado de fora virado para ele. O pano que passava por cima da borda (da G3, de quando ele entrava na
caneca) saiu: parado, lia como uma peça dura em cima da caneca. O pano fica todo na mão, apertado contra a parede de
cá (um volume curto acima dos dedos, descendo até a parte pendurada), e a mão sobe e desce pela parede, no máximo 1 px
para o lado; o ritmo e as poses do corpo são os mesmos.

**Sem cintilar:** cada parte (o tronco com os braços de cima, a cabeça, o braço do pano com o pano, a caneca com a mão
da asa, o pano na boca da caneca) é desenhada e iluminada na posição da G (o pontilhado da luz da G preso a ela),
retocada como na G2 e só depois deslocada; o pontilhado anda com a parte. A caneca mantém o tamanho, o volume e a pega.

**A fonte:** `g4/aseprite/taverna-g4.aseprite` (9 quadros: o taverneiro um por pose, o fogo e o lampião nos 4
primeiros), feita da fonte da G3 (`--criar` protegido; depois, a autoridade). `g4/fonte.py` exporta para `camadas/g4/`
(o fundo, as chamas, a tira das poses recortada na caixa delas, a frente e `rotina.json`); `--conferir` compara com o
código. A cena (`tela/cena-taverna-anim.js`, `CenaTavernaG4`) desenha o fundo, as chamas, a pose da vez e o balcão por
cima, pelo relógio da vista do jogo (sair e entrar não cria outro relógio).

## Diante de Morel: a terceira passada (a construção do braço; em avaliação)

**O pedido do Jean** (29/10/2026): o braço continuava estranho (o mesmo problema do ferreiro e dos jogadores);
pesquisar, estudar a anatomia simplificada, aplicar em Morel e consolidar o método numa skill. A segunda passada fica no
painel ("Diante de Morel, a segunda versão": a fonte em `morel/vista-v2/`, as camadas em `camadas/morel-vista-v2/`), no
mesmo estado do jogo; a primeira também ("a primeira versão").

- **O erro de construção:** o ombro 12 px abaixo do lugar (no fim da ombreira), o cotovelo indo ao meio do peito, o
  braço encurtando de 18 para 7 px sem pista de escorço, braço e antebraço no mesmo tom, a ombreira cobrindo a raiz do
  braço, o braço de apoio como uma faixa escura; a mão saltando 9 a 11 px a cada 200 ms. O diagnóstico e as fontes
  consultadas estão na skill.
- **O estudo** (`morel/estudo-construcao/morel-construcao.aseprite`): cinco poses-chave (recolher, levantar, boca,
  retornar, repousar) com formas simples (a cabeça, o tórax, as clavículas, os braços por cores, a mesa, a tigela) e as
  juntas na guia. `juntas.py` dá as juntas de cada quadro: braço 28 px e antebraço 22 no espaço, o cotovelo pela
  cinemática, a colher rígida de 12 px; o comprimento na tela muda pelo escorço (o braço tem 16 px na boca). Na boca, o
  cotovelo fica logo abaixo do ombro, à frente, e a mão à frente do queixo; a cabeça desce 3 px ao encontro da colher.
- **A aplicação** (`vestir.lua` refaz o braço da fonte pixel a pixel): o ombro da colher mostra o couro da jaqueta; a
  ombreira de aço ficou só no ombro esquerdo dele (como na referência), a mesma da v2, por cima do braço de apoio; os
  braços com o porte de Morel (11 px), o antebraço um tom abaixo do braço (separa os dois e separa o antebraço do
  tampo), a sombra do antebraço no braço, o vinco do cotovelo, o punho da manga, a mão em bolinha, a sombra de um pixel
  no peito e na mesa; o braço de apoio em três partes (a ombreira, o braço caído, o antebraço deitado). Rosto, cicatriz,
  colete, espada, cores e o lugar ficam como estavam (o fundo, o fogo, o taverneiro e a mesa saem idênticos aos da v2).
- **A animação:** 20 poses (as 5 chaves e as passagens interpoladas no espaço); a mão e o cotovelo andam no máximo 6 px
  de um desenho para o seguinte; o tempo como o da curandeira e o do balcão (as pontas de cada trecho 2 tiques, as
  passagens do meio 1, a boca 6); 156 tiques; a pose parada é `repousa`. As juntas de cada quadro estão na camada `guia`
  da fonte (um pixel de cor por junta).
- **Ver no painel:** "Diante de Morel: o estudo de construção e a aplicação" (as chaves nas formas simples e vestidas) e
  "as trajetórias do cotovelo, da mão e da colher" (uma volta, a v2 e a atual), em ampliação inteira, fora da HUD.
- **A lareira** (o Jean, 30/10/2026): o fogo passava na frente do caldeirão, ao contrário do balcão. O caldeirão e a
  cremalheira foram para uma camada própria, `caldeirao`, acima do `fogo`, e as chamas exportadas são cortadas por ela;
  o fundo e Morel saem iguais. Embaixo do braço de apoio, o tampo tinha um retângulo sem a sombra pontilhada e sem a
  junta da tábua (era onde ficavam o punho e o antebraço da v2): a camada `sombra` ganhou ali o mesmo pontilhado das
  linhas de cima, e a junta em x 240 continua até a borda da frente, para o ponto de fuga do tampo.
- **A manga** (o Jean, 30/10/2026; em avaliação): o ombro lia como uma peça encaixada no tronco e o cotovelo como
  uma dobradiça. A causa estava no acabamento do `vestir.lua`, não na construção nem em guia exportada (a `guia` fica
  fora da exportação): o braço vestido como duas cápsulas, cada uma com as faixas de luz dela; a do braço terminando
  numa calota acima da linha do ombro do tronco; o antebraço inteiro um tom abaixo exatamente na junta, com o vinco
  como um traço entre os dois. `morel/vista/manga.py` refaz a camada `morel_braco` das 20 poses com as mesmas juntas
  (as da `guia` e o ombro de `juntas.py`) e os mesmos raios: uma forma só, unida com suavidade no lado de fora do
  cotovelo (a curva); por dentro, o antebraço continua passando na frente do bíceps, com a luz dele e a sombra no braço
  (na primeira aplicação a união também por dentro esmagou o antebraço no bíceps nas poses de braço bem dobrado, que o
  Jean marcou); sem calota no ombro (fora do tronco, o alto da manga vai só até a linha do ombro do
  casaco), a luz de uma superfície só em três tons, o antebraço escurecendo meio tom depois da junta, uma dobra de dois
  pixels por dentro do cotovelo com a crista acesa; a mão e a colher de antes, intactas. Os retoques à mão ficam numa
  lista no script (`RETOQUES`), para refazer a manga sem perdê-los; depois de gravada, a fonte é a autoridade. A versão
  anterior: "Diante de Morel, a versão anterior (antes do acabamento da manga)" no painel (a fonte em `morel/vista-v3/`,
  as camadas em `camadas/morel-vista-v3/`); a folha "a manga, as 20 poses antes e depois" na inspeção. Conferido: o
  fundo, as chamas, o taverneiro e a mesa saem idênticos; a recomposição da cena igual ao achatamento do Aseprite nos 20
  quadros; as três poses-chave e o ciclo, quadro a quadro e em sequência; no jogo a 1920×945 e 1280×720, com a pose
  parada e a reação ao pagamento.
- **As ombreiras** (o Jean, 30/10/2026; em avaliação): nas outras versões de Morel no jogo (o retrato de
  `rpg/web/static/retratos.js`, a figura de 16 px), ele tem duas ombreiras (a do ombro direito em aço claro, com a
  guarda da espada logo acima; a do esquerdo mais escura); a espada nas costas pelo ombro direito, a cicatriz, a barba, o
  colete vermelho e o couro batem com a vista (as fivelas são só da vista, aprovadas). A vista tinha só a esquerda: a
  direita entrou à mão (`manga.py`, `OMBREIRA_DIR`), uma calota inclinada como a linha do ombro, assentada na raiz do
  braço e logo abaixo da guarda, em aço mais claro (o lado da luz), com a fileira de rebites, a borda escura embaixo e a
  sombra no braço; ela acompanha a junta do ombro em cada pose e fica atrás do antebraço e da mão quando a colher vai
  à boca; ela também cobre a ponta quadrada que sobrava no alto da manga. Na esquerda, o couro do ombro que aparecia
  acima e além da borda de cima da placa virou placa (`corpo_corrigido`, a camada `morel_corpo` nos 20 quadros, com o
  deslocamento do tronco de cada um). Depois (o Jean viu um ou dois pixels marrons, da manga, encostados na ponta
  esquerda da calota em alguns quadros, e uma beirada em cima quando o ombro sobe para a boca): acima da ponta esquerda
  da calota, nada da manga passa para fora dela; embaixo, a borda de fora do braço continua.
  E na esquerda (o Jean): a primeira correção estendia a placa sobre o fundo nas linhas de cima, numa lâmina
  horizontal discrepante; agora ela parte do tronco original (`morel/vista-v3`) e vai, linha a linha, só até o contorno
  do ombro (`FIM_PLACA`), com o canto de cima arredondado e a fresta escura fechando a curva: cobre o ombro como a
  direita.
- **Os limites que ficam:** a boca é a pose mais fraca (o braço curto em escorço se mistura um pouco com o casaco
  claro); as poses do braço saem de `manga.py` (antes, de `vestir.lua`), revistas na ampliação e em sequência; a espada nas costas continua com a guarda logo acima do ombro.

## Diante de Morel: a segunda passada (o espaço, a mesa, o braço; histórico)

**O pedido do Jean** (29/10/2026): o mesmo lugar da G4 (que não muda), a mesa com fim, o braço da colher construído, a
postura participando do gesto. A versão anterior fica no painel ("Diante de Morel, a primeira versão": a fonte em
`morel/vista-v1/`, as camadas em `camadas/morel-vista-v1/`), no mesmo estado do jogo.

- **O fundo como a G4, visto da mesa:** uma prateleira só (a louça à esquerda; o vão; as garrafas à direita), as
  canecas penduradas embaixo dela, a bancada mais baixa (só o que está nela aparece acima do balcão: o barril no berço
  com a torneira para o meio, à esquerda; a jarra, o pão e o queijo à direita do taverneiro); os pendurados junto do
  esteio da direita (acima do ombro de Morel); o lampião no braço do esteio; a porta da despensa atrás da ponta do
  balcão, como na G4. As distâncias entre os grupos estão comprimidas (a parede está mais longe), a ordem não.
- **A lareira** com a construção da G4, simplificada: a chaminé de pedra em blocos, a verga com a prateleirinha (o pote
  de sal), o arco de pedras em cima da boca, as faces de dentro, a cremalheira com o caldeirão, a concha e a frigideira
  em pregos; as chamas atrás do balcão.
- **O balcão termina** depois da porta, com a quina acesa e a lateral curta (a ponta do tampo e a cabeceira de tábuas);
  além dela, a passagem para trás do balcão, até a porta, e a quina da sala.
- **O taverneiro** na proporção da G4: duas cabeças e meia acima do tampo (a figura inteira, com os pés no chão atrás do
  balcão, é a referência; só o que fica acima do tampo aparece), a calva, a barba, a camisa, as alças com as fivelas, a
  caneca e o pano.
- **A mesa:** o tampo e a espessura primeiro (a borda de lá, a lateral da direita recuando até a quina da frente, a borda
  da frente com a espessura; a da esquerda sai do quadro), e o chão do salão aparece além da quina; depois as tábuas,
  todas para o mesmo ponto de fuga do tampo (238, 30), num tom só um pouco abaixo da madeira; os riscos de uso curtos e
  noutras direções; as sombras de contato embaixo da tigela, da caneca, da vela e do pão (que foi para dentro do
  tampo, longe da mão).
- **O braço da colher, por partes** (`BRACO3` na fonte: o braço de cima, do ombro embaixo da ombreira ao cotovelo; o
  cotovelo como uma junta redonda, a dobra de dentro em sombra; o antebraço noutra direção até o punho da manga; a mão
  simples, sem dedos; a colher): recolhendo e descansando, o braço de cima sai por fora do tronco e o cotovelo pousa no
  tampo; subindo, o cotovelo sai do tampo e vem para a frente do peito; na boca, a mão fica ao lado da barba (sem
  atravessá-la) e a colher chega à boca. Uma sombra no lado do tronco, embaixo da ombreira, separa o braço do peito. O
  braço que descansa: o braço de cima com o corpo, o cotovelo e o antebraço no tampo, a mão simplificada.
- **A postura:** comendo, o corpo e a cabeça descem 2 px para a tigela; descansando, 1 px; olhando para quem está à
  mesa, ereto, e a cabeça sobe mais 1 px. O corpo de Morel virou uma célula por quadro (a mesma imagem, deslocada).
- **A animação:** as mesmas atividades e a mesma linha do tempo (12 poses, 148 tiques), com as poses refeitas; a última
  (descansa) emenda na primeira (recolhe) com a mão 1 px e o corpo 1 px.
- **A conferência:** a recomposição da cena sai idêntica ao achatamento do Aseprite nos 12 quadros (fora as chamas dos
  quadros que a linha do tempo não usa).

## Diante de Morel: a primeira versão adaptada (histórico)

**O que veio do estudo livre:** a ideia (sentados perto de Morel, do outro lado da mesa, o balcão e o taverneiro ao
fundo), a presença e a aparência dele, a vela e a caneca perto de nós. **O que mudou:** o acabamento é o dos interiores
aprovados e da G3 (a paleta da G e a do retrato de Morel, a pedra em fiadas com as juntas um tom abaixo, a madeira com a
aresta acesa, o metal com o brilho de um pixel, a luz em degraus pontilhados e o halo quente), na grade 320×96 (o pixel
do mesmo tamanho dos outros interiores; o rosto de Morel ganha mais pixels por estar perto: a cabeça tem 21×25).

**O esquema da sala e da câmera** (a G3 como referência): na parede do fundo, de oeste para leste, a lareira, a bancada
com o barril, as prateleiras, o taverneiro, os pendurados, o esteio com o lampião e a porta da despensa; o balcão corre
na frente deles. A mesa de Morel fica no salão, na frente da ponta leste do balcão; a câmera, sentada à mesa, olha para
o norte. À esquerda de Morel aparecem a lareira (atrás do balcão: as chamas por trás do tampo, não na frente), o barril
(entre a lareira e o taverneiro, como na G3; no estudo ele estava do lado errado), as prateleiras, o taverneiro e os
pendurados; à direita dele, o lampião e a porta da despensa. Escala: o balcão com 1,05 m a ~21 px/m, o taverneiro com
~1,72 m (a cabeça de ~6 px, o corpo escondido abaixo do tampo), as banquetas na altura de um assento de balcão, com o
assento, as pernas de 2 px, a travessa e o pé no chão.

**Morel** (a identidade do jogo: o retrato 80×80 e o 16×16): o cabelo e a barba castanhos curtos, as sobrancelhas
carregadas, a cicatriz em diagonal da testa à bochecha (atravessando a sobrancelha e o nariz), o gibão de couro, o
colete vermelho num V entre as abas, com o volume do peito e as tiras com as fivelas seguindo a curva, o punho da espada
atrás do ombro. **Os ombros, como no retrato:** a ombreira de metal no ombro da colher (menor e mais escura que no
estudo, o brilho só num fio) e, no outro, a peça escura cinza-amarronzada (menor, sem brilho de metal, com a costura) que
os registros chamam de "a pele". Ele se senta numa cadeira de espaldar (os montantes atrás dos ombros). Os dois braços
saem dos ombros e passam por cima da borda da mesa (no estudo, a borda passava por cima do braço): o da colher com o
cotovelo apoiado no tampo; o outro com o antebraço deitado e a mão espalmada junto da tigela.

**A mesa:** as juntas das tábuas correm para o mesmo ponto de fuga, de ponta a ponta (também à direita); os riscos de
uso são curtos, claros e em outras direções; as sombras de contato embaixo da tigela, da caneca, da vela e do pão; a
lateral da esquerda com a espessura.

**A rotina de Morel** (`morel/vista/exportar.py`, `ROTINA_MOREL`): recolher o ensopado (duas vezes, a colher no fundo
da tigela), a mão sair da tigela com o cotovelo ainda no tampo, subir pelo peito (o cotovelo sai do tampo), a colher na
boca (a cabeça desce 1 px ao encontro dela, a boca aberta), a volta com a colher vazia, descansar, mastigar (o queixo
desce e sobe), descansar; na segunda volta, ele ergue os olhos para quem está à mesa (a cabeça sobe 1 px) e volta à
comida. 12 poses, 148 tiques (14,8 s); a última (descansa) emenda na primeira (recolhe) com a mão 1 px. A pose parada:
descansando, os olhos na tigela (ele "fala sem levantar os olhos do prato"). **O taverneiro ao fundo** esfrega a caneca
em duas poses, com uma pausa longa (37 tiques). **A luz:** a vela (a principal), a lareira e o lampião; o rosto, as
mãos e a comida fora da sombra pontilhada; o halo contínuo, sem anéis.

**Os pontos:** só o que está desenhado: o Taverneiro (a bebida); Morel (o cartão do encontro, só quando o motor o manda,
o "Homem do canto"), com o nome no balcão ao lado dele, longe do rosto; a porta da despensa (só enquanto ela espera).
Dormir e o resto ficam nos cartões.

**Como foi feito (o que foi desenhado no editor e o que foi automatizado):**
- **No editor**, pelas ferramentas do Aseprite (o retângulo e a elipse cheios, o contorno preenchido, a linha, o lápis)
  comandadas pela ponte, camada por camada, conferindo cada passada na exportação ampliada: a sala, a lareira, as
  prateleiras e o que está nelas, o barril, o balcão, as banquetas, a cadeira, o corpo de Morel (refeito duas vezes: na
  primeira, largo demais para a cabeça), a ombreira, a peça do outro ombro, os braços em cada pose, as mãos, a colher, a
  mesa e o que está nela.
- **Grades desenhadas à mão, postas por um laço:** a cabeça de Morel (21×25, com os quatro jeitos: olhos baixos, boca
  aberta, mastigando, olhando) e o taverneiro ao fundo (15×15, duas poses).
- **Automatizado:** a camada `guia` (a referência reduzida, oculta); os padrões repetidos (as fiadas da pedra e das
  lajes, as juntas das tábuas para o ponto de fuga); a luz (`sombra` e `brilho`, calculadas por um laço com a regra da
  luz da G); as cópias dos quadros e a ligação das células paradas; a exportação (`morel/vista/exportar.py` só lê a
  fonte; a recomposição da cena saiu idêntica ao achatamento do Aseprite).

**A fonte:** `morel/vista/morel-vista.aseprite` (320×96, 12 quadros; as camadas `guia` (oculta), `parede`, `fundo_bar`,
`fogo`, `taverneiro`, `balcao`, `cadeira`, `morel_corpo`, `morel_cabeca`, `mesa`, `maos`, `morel_braco`, `sombra` em
multiplicar, `brilho` em somar, `chamas`; as paradas com as células ligadas em todos os quadros). Ela é a autoridade:
não há script que a gere. O estudo livre (`morel/aseprite/morel-mesa.aseprite`) fica como histórico.

**Ver:** no painel, "Diante de Morel (animada)" a mostra na área de cena da HUD, no lugar do balcão, com os cartões da
taverna embaixo; "Inspeção ampliada" mostra a vista na pose parada, ou o estudo livre, em ampliação inteira.

**Os limites que ficam:** o rosto de Morel tem poucos tons (resolve a expressão, a cicatriz e a barba, sem rugas); no
gesto da boca, a manga passa na frente da ombreira; o fogo da lareira aparece por trás do caldeirão; o taverneiro ao
fundo tem duas poses só.

## A G3 (a G2 aprovada com as correções locais)

## A G3 (a G2 aprovada com as correções locais)

**Feita a partir da fonte da G2**, sem reabrir a câmera, o balcão, a luz nem o acabamento: `g3/fonte.py --criar` lê as
células de `g2/aseprite/taverna-g2.aseprite`, aplica `g3/retoques.py` e grava `g3/aseprite/taverna-g3.aseprite` (a
autoridade daqui em diante; `--criar` não a sobrescreve sem `--refazer`). Cada parte nova usa a paleta e a luz da G.
- **O freguês da esquerda** (`fregues_esquerda`): na G2 a cabeça pequena ficava ligada a um corpo enorme descendo em
  diagonal, sem ombro, costas nem braço. Refeito pela anatomia de quem está sentado ao balcão, perto da câmera: a
  cabeça de um adulto nessa distância (~19×22 px, como na G), o pescoço, a gola, a linha dos ombros quase horizontal, o
  ombro de cá redondo e o braço descendo do ombro para fora do quadro (o cotovelo, apoiado no balcão, fica abaixo da
  borda), as costas entre a gola e o braço; depois a capa por cima. Continua uma silhueta escura e secundária, no mesmo
  canto, sem cobrir mais a lareira; o contorno do lado do fogo pega a luz dela. Onde o da G e o da G2 estavam, volta o
  balcão da G.
- **As garrafas** (`garrafas`): a de vinho verde e a bojuda de âmbar tinham o gargalo de 2 px sobre um corpo de
  largura ímpar (meio pixel fora do eixo, parecendo inclinado). Refeitas no eixo: a base apoiada na tábua, o corpo, os
  ombros afinando, o gargalo, o anel da boca e a rolha. Atrás delas volta a parede da G.
- **O pano** (`pano`): saía da mão como um bloco quadrado. Agora passa por cima da borda da caneca (a dobra entrando
  na boca), desce pelo lado dela até a mão que o aperta e pende em pregas que convergem para o punho, com a ponta mais
  baixa e a barra em diagonal. A pose, as mãos simples e a caneca não mudam.

**No painel:** "G3: a G2 com as correções" (o padrão), "G2 aprovada (antes das correções)" e "G original", com a troca
imediata, no mesmo estado do jogo. Os pontos, os cartões, os serviços e as condições são os da G.

## O estudo livre "Diante de Morel" (em avaliação)

**O pedido:** outra perspectiva da mesma taverna, com liberdade de acabamento (resolução, paleta, densidade, luz) e
construída no Aseprite: o jogador sentado à mesa, de frente para Morel, bem perto; ao fundo, o balcão, o taverneiro e
os elementos que reconhecem o lugar. A referência é "Morel diante do fogo na taverna"
(`ferramentas/arte/referencias/cenarios internos`): ela orienta a proximidade, a situação e a atmosfera; não é copiada.

**As escolhas:** 360×120 (3:1, como a referência; a cabeça de Morel com ~31 px), uma paleta própria mais rica que a das
cenas do jogo, a luz feita em camadas com modo de mistura (a `sombra` multiplica; o `brilho` soma, em anéis com a borda
pontilhada) e as chamas por cima. Morel segue o jogo, não a imagem gerada: o cabelo e a barba castanhos curtos, as
sobrancelhas carregadas, a cicatriz em diagonal da testa à bochecha passando pelo nariz, o gibão de couro com o colete
vermelho no peito (as duas tiras com fivelas), a ombreira de metal num ombro, a pele no outro, o punho da espada atrás
do ombro. Ele come "sem levantar os olhos do prato" (o texto do encontro): as pálpebras baixas, a colher na mão
direita com o cotovelo apoiado na mesa e a concha dentro do ensopado, a outra mão espalmada junto da tigela. Ele se
senta numa cadeira de espaldar (os montantes atrás dos ombros). Na mesa, a caneca de estanho e a vela no pires perto
de nós (a fonte de luz principal), a tigela, o pão na tábua. Ao fundo, à esquerda, o mesmo lugar da G2 visto de outro
ângulo: a lareira com o caldeirão, as prateleiras com a louça e as garrafas, o barril, as linguiças e o alho, o
lampião, o balcão com três banquetas e o taverneiro pequeno atrás dele (a calva, a barba, a camisa clara, o avental, a
caneca e o pano); à direita, a pedra, um esteio e uma prateleira curta.

**Como foi feito (o que foi desenhado no editor e o que foi automatizado):**
- **No editor, pelas ferramentas do Aseprite** (`app.useTool`: o retângulo e a elipse cheios, o contorno preenchido, a
  linha, o lápis), comandadas pela ponte do Aseprite, camada por camada, com cada forma posta por mim e conferida na
  exportação ampliada: as paredes, o balcão, as prateleiras e o que está nelas, as banquetas, a mesa, a tigela, a
  caneca, a vela, o pão, o corpo, a ombreira, a pele, os braços, as mãos, a colher, a cadeira, a sombra, os halos e as
  chamas. Os retoques também: o corpo refeito duas vezes (o pescoço comprido e a ombreira como uma panela, na primeira),
  o colete estreitado num V, a ombreira refeita como uma capa sobre o ombro, a pele refeita (lia como malha), a concha
  cheia, o modelado do rosto, o fogo refeito em línguas, os halos diminuídos.
- **Grades desenhadas à mão, postas por um laço:** a cabeça de Morel (31×31) e o taverneiro (13×15) foram desenhados
  pixel a pixel numa grade de caracteres e postos na camada por um laço em Lua (o laço só copia; o desenho é a grade).
- **Automatizado:** a camada `guia` (a redução automática da referência a 360×120, oculta, fora da exportação); a
  repetição mecânica de alguns padrões (as juntas da pedra e das lajes, as juntas das tábuas fugindo para o ponto de
  fuga, a borda pontilhada dos anéis de luz, os tufos da pele); a exportação (`morel/exportar.py`: o Aseprite em lote
  achata as camadas visíveis com os modos de mistura; saiu idêntica à exportação do editor).
- **Não houve desenho com o mouse:** tudo passou pela ponte. Nenhuma imagem foi gerada em Python e empacotada.

**A fonte é a autoridade:** `morel/aseprite/morel-mesa.aseprite` (as camadas `guia` (oculta), `parede`, `balcao`,
`taverneiro`, `cadeira`, `morel`, `mesa`, `maos`, `sombra`, `brilho`, `chamas`). A exportação lê dela.

**Ver:** no botão Protótipo, "Diante de Morel (o estudo em Aseprite)" abre uma vista à parte, por cima do jogo (fora da
HUD), na maior ampliação inteira que cabe na janela (5× a 1920×945, 3× a 1280×720); os botões trocam para o tamanho nativo
(1×) ou outra ampliação inteira; "Caber na janela" é uma prévia reduzida, e a legenda diz quando a imagem não está
fiel. Esc ou Fechar voltam ao jogo. Não há navegação, diálogo, regra nem encontro novos.

**O que ainda vejo de limite:** a ombreira é grande e clara para o tamanho da cabeça; o rosto de Morel resolve a
expressão (os olhos baixos, a cicatriz, a barba) com pouco modelado; o taverneiro, pequeno, é reconhecível pela calva,
pela barba e pela camisa, sem leitura do gesto; o fundo da direita é simples (a pedra, um esteio, uma prateleira).

## A decisão anterior: a G escolhida e a G2

**A decisão do Jean** (29/10/2026): **a G é a composição escolhida** (a câmera, o enquadramento, o balcão, as
silhuetas). **A H foi uma experiência encerrada** (o afastamento não foi aprovado) e fica só como histórico. A **G
refinada (G2)** é a G com retoques locais (o taverneiro, a cabeça contra a prateleira, o freguês da esquerda); depois
**aprovada**.

**A candidata G** é a câmera perto do balcão, de frente, como quem está sentado diante dele, pela referência frontal
"Taverneiro desconfiado atrás do balcão-1" (`ferramentas/arte/referencias/cenarios internos`). A cena representa o
balcão, não a planta da taverna: um personagem com presença numa atividade legível (o taverneiro limpa uma caneca e
olha de lado para quem chegou), os produtos e utensílios da casa, os fregueses recortados nos cantos.

**O salão panorâmico está suspenso** (pedido do Jean, 29/10/2026): as candidatas A a F, a prova de qualidade (as grades
A e B, a B2, a B3, a B4) e o M1 de Morel não resolveram de forma satisfatória a anatomia, a escala, a perspectiva e a
qualidade visual com vários grupos na mesma vista. Ficam como histórico, no botão Protótipo e nas seções abaixo, sem
mais correções nessa direção.

## Abrir

Dê dois cliques em `demo.bat` (ou `python ferramentas/prototipos/taverna/demo.py` na raiz). O jogo abre no navegador
num **save temporário** (os saves do Jean não são lidos nem tocados), na porta 8795: o Guerreiro no Vau, com a
campanha começada e 60 de ouro. Clique na **Taverna** na vila: o balcão animado (G4) aparece no topo e o balcão de sempre
embaixo. Se uma demonstração antiga estiver aberta, feche a janela dela antes (a porta é a mesma).

O botão **Protótipo** na barra do alto abre o painel: a vista (**Balcão animado (G4)**, o padrão, com a atuação ajustada, a **atuação anterior** para comparar, **Diante de Morel
(animada)**, a segunda e a primeira versão dela, **G3 estática**, **G2** e **G original**: a troca é imediata, sem sair da taverna, no mesmo estado do jogo; a H, a prova de qualidade e da **F** à **A**, o
histórico), o estado do save (**Despensa esperando**, **Homem do canto**, **Morel conhecido**, **Morel recrutado**,
**Sem ouro**), a **Pose parada** (o fogo e o lampião param) e as vistas de inspeção de Morel (a vista parada, o
estudo de construção com a aplicação, as trajetórias, o estudo livre).

## A G refinada (G2)

**Feita a partir da fonte da G**, sem reorganizar nada: `g2/fonte.py --criar` lê as células de
`g/aseprite/taverna-g.aseprite` como estão, aplica os retoques de `g2/retoques.py` e grava
`g2/aseprite/taverna-g2.aseprite`. Cada retoque age numa região marcada, com as cores que já estão ali (a luz e o
pontilhado da G); não há limpeza geral nem preenchimento chapado (o erro da H, que deixou a camisa chapada e os ombros
como peças redondas separadas). A câmera, o balcão (as bordas e as linhas), os objetos, a luz e os fregueses são os da
G, pixel a pixel, fora das regiões abaixo.
- **A pele** (`pele_lisa`, 188 px): na testa e nos antebraços, o pixel solto do pontilhado (os dois vizinhos de um eixo
  iguais entre si e parecidos com ele) toma a cor dos vizinhos; as sombras, os relevos, o rosto e as bordas ficam.
- **As mangas** (`mangas`, 26 px): as quatro rugas diagonais da G, que cortavam o braço, saem; entra uma dobra
  atravessando cada manga, perpendicular ao braço, acima do rolo, com a luz em cima. O pontilhado da camisa em volta
  (o tecido gasto, as transições de volume) fica.
- **A barba, o pescoço e a gola** (`pescoco`, 29 px): a barba termina em pontas espalhadas, não numa linha reta; a
  sombra embaixo segue as pontas; os lados do pescoço escurecem descendo para a gola. O pescoço não cresce.
- **A cabeça e a prateleira** (`cabeca_e_prateleira`, 27 px): a tábua escurece até a sombra da parede nos dois pixels
  em volta da cabeça, onde encostava no cabelo; a prateleira continua inteira e no lugar.
- **O freguês da esquerda** (`fregues_esquerda`): na G a cabeça era uma bola grande sobre um ombro pequeno e baixo
  (a observação do Jean, comparando com a referência). Refeito pela referência: a cabeça menor (~15×17 px, contra
  ~18×21) e afundada nos ombros, a capa larga subindo até o queixo, o capuz amontoado em volta do pescoço, as dobras
  descendo, o perfil da barba e a orelha do lado do fogo. Onde o da G estava, volta o balcão da G; o novo recebe a
  mesma luz. Continua uma silhueta escura, no mesmo canto: sem braço, sem rosto, sem presença nova, e cobre menos o fogo.

**A fonte é a autoridade:** depois de criada, os retoques à mão se fazem em `taverna-g2.aseprite`; `--criar` não a
sobrescreve sem `--refazer`. `g2/fonte.py` exporta dela para `camadas/g2/`; `--conferir` compara com a fonte da G mais
os retoques do script (hoje, 4 de 4 iguais: ainda sem retoques à mão). A fonte da G não muda.

**No painel:** "G refinada (G2)" (o padrão) e "G original", com a troca imediata, sem sair da taverna, no mesmo estado do
jogo. Os pontos, os cartões, os serviços e as condições são os da G.

**Para avaliar:** no tamanho real, a 1920 e a 1280, alternando G2 e G: se o desenho ficou mais claro (a testa e os
braços, as mangas, a ligação da barba com o pescoço, a cabeça contra a prateleira, o ombro do freguês) sem perder o
volume, a textura e a personalidade da G.

## A H (experiência encerrada, histórico)

A H experimentou mais profundidade (a câmera um pouco mais afastada e para o lado, o balcão com volume, os fregueses
sentados de perto). O Jean preferiu a câmera, a composição, o balcão e as silhuetas da G; o afastamento não foi
aprovado. Ela continua no painel ("Candidata H (histórico)"), sem mais trabalho.

**Como a H foi feita:**

**O que muda em relação à G** (`h/desenho.py`, `h/taverneiro.py`):
- **A câmera:** uma perspectiva simplificada de um ponto, com o ponto de fuga na beira direita, na altura do olho de quem
  está sentado ao balcão (`PF`). A parede, as prateleiras e a frente do balcão ficam de frente; o que corre para o fundo
  converge para ele. Daí o tampo mais fundo (12 px, contra 6 na G) e a ponta da direita do balcão com a lateral curta
  (a quina da frente acesa pelo lampião, a aresta de cima subindo para o ponto de fuga); depois da ponta, a passagem e a
  porta da despensa até o fim do quadro.
- **Os planos:** os dois fregueses sentados na frente; o balcão (o tampo com a tábua do pão e do queijo e as canecas
  dos fregueses: a área de servir); o taverneiro e a bancada; a parede com as prateleiras, a lareira e a despensa.
- **O taverneiro do mesmo tamanho da G**, mais para cima e para a esquerda (`TAV`): o afastamento aparece no tampo, na
  ponta e nos fregueses, não na leitura dele. Os refinamentos: a pele e a camisa sem o pontilhado da luz (um tom de
  luz só para a figura; a modelagem fica nos planos do desenho); a sombra da barba no pescoço, os lados do pescoço, o
  peito no V da gola e as abas deitadas até o peitilho; as dobras das mangas como arcos atravessando cada braço, acima
  do rolo; a prateleira em duas partes, com o vão atrás da cabeça (nenhuma linha encosta nela).
- **O balcão com menos bordas competindo:** uma aresta clara atrás do tampo, emendas discretas, uma aresta forte na
  frente e a frente escura sem a travessa; a bancada de trás sem a aresta clara.
- **Os fregueses**, construídos por partes (`Vulto`): a cabeça, o pescoço, a linha dos ombros, as costas estreitando
  para a cintura, o braço do ombro ao cotovelo pousado na borda do tampo e o antebraço até a caneca, cada material em
  três tons escuros com o contorno aceso pelo fogo (o da esquerda) e pelo lampião (o de capuz, à direita). A primeira
  versão deles tinha as costas como dois montes redondos e grandes (a observação do Jean); a de agora tem a anatomia e
  a cabeça um pouco menor que a do taverneiro (~18×21 px).
- **Os objetos da G** entram pelo desenho dela (`de_g`), no lugar novo: o canto de preparo um pouco para a esquerda e
  para cima, a louça e as garrafas nas duas prateleiras, o barril e a jarra na bancada, o pão e o queijo no tampo, os
  pendurados perto do lampião, que agora sai do esteio para a esquerda, em cima da ponta do balcão.
- **Os pontos:** os mesmos da G, no lugar novo (o nome do Taverneiro ao lado da cabeça, na prateleira da direita; acima
  dela, a 1280, sairia da arte).
- **A fonte:** `h/aseprite/taverna-h.aseprite`, pelo mesmo caminho da G (`h/fonte.py` usa o `g/fonte.py`; `--criar`
  protegido, a exportação para `camadas/h/` conferida com o código).

**Os limites que ficam:** a cabeça dos fregueses fica um pouco menor que a do taverneiro, embora eles estejam mais
perto (para não dominarem a cena); a perspectiva é de um ponto só (a parede e a frente do balcão continuam de frente);
a lareira fica mais cortada pela borda e pelo freguês da esquerda; a fonte ainda sem retoques à mão.

## Roteiro curto para avaliar a G

1. No tamanho do jogo, a 1920 e a 1280: o taverneiro (a expressão, o olhar de lado, as mãos na caneca e no pano), o
   balcão de um lado a outro, a lareira com o caldeirão à esquerda, a despensa à direita, os fregueses nos cantos.
2. Os nomes pelo mouse, pelo Tab ou com F4: o **Taverneiro** leva ao cartão da bebida; a **Despensa** existe só com
   **Despensa esperando** e leva ao Descer à despensa.
3. Os estados: **Homem do canto** (o cartão de Morel embaixo, sem ponto na cena), **Morel recrutado** e **Sem ouro**
   (os cartões como antes). O Dormir e o Voltar à vila ficam nos cartões; o Esc volta à vila.
4. Para comparar, a **F** e a **prova** no mesmo painel.

## A candidata G

**O que foi construído** (`g/desenho.py`, `g/taverneiro.py`):
- **A grade:** 320×96, a mesma da forja, da curandeira e do templo. O pixel tem o mesmo tamanho na tela que nas cenas
  aprovadas; a câmera mais perto dá o tamanho: o taverneiro tem a cabeça com a barba em ~23 px e o corpo, da cabeça
  ao tampo, em ~57 (a régua no lugar dele é de ~80 px por metro). A grade maior da B4 e do M1 não foi usada: com a
  câmera perto, a 320×96 já dá espaço para o rosto e as mãos, e a cena fica coerente com as aprovadas.
- **O espaço antes dos objetos:** a parede de pedra, a viga e dois esteios; a prateleira alta (y 27) e a bancada de
  trabalho (y 66) entre os esteios; o balcão de um lado a outro (o tampo de y 74 a 79, visto um pouco de cima, a borda
  grossa com a aresta acesa, as tábuas da frente em pé com a travessa).
- **O taverneiro, da pose inteira:** em pé atrás do balcão, que fica na altura da barriga, logo abaixo dos cotovelos; a
  cabeça larga ligada ao tronco (a barba curta encosta na gola aberta, o pescoço grosso entre as abas); os ombros
  redondos de frente; os braços saindo dos ombros, os cotovelos abertos, os antebraços vindo para o meio; a mão
  direita dele aperta o pano contra a caneca, a outra a segura pela asa; o pano pende até perto do tampo. A camisa de
  linho cru com as mangas arregaçadas (o rolo da manga acima do cotovelo, as dobras), o avental de couro com o
  peitilho, as alças e as fivelas. O rosto desconfiado: a sobrancelha de lá baixa sobre o olho apertado, a de cá um
  pouco erguida, os olhos de lado, a boca fechada com os cantos para baixo; a calva com o cabelo crespo dos lados. As
  mãos simples, sem dedos.
- **Os objetos por função:** à esquerda, o canto de preparo (a lareira de pedra com a verga, o caldeirão na corrente
  da cremalheira na frente das chamas, os cães de ferro com a lenha, a concha e a frigideira em pregos); atrás dele, o
  barril deitado no berço com a torneira virada para o meio e espaço embaixo para a caneca, as canecas penduradas pela
  asa, a louça na prateleira à esquerda (a jarra de grés, a de barro, as canecas, as tigelas), o vão atrás da cabeça, as
  garrafas à direita (a de vinho, a bojuda de âmbar, o garrafão empalhado, a alta, o pote); na bancada, a jarra e a tábua
  com o pão cortado e a cunha de queijo; na viga, as linguiças e a trança de alho; à direita, o lampião no braço de ferro
  do esteio e a porta da despensa (a verga, as tábuas, as dobradiças, a argola).
- **Os fregueses da frente:** de costas à esquerda (a cabeça, a orelha contra o fogo, o capuz caído, o ombro da capa) e
  de capuz à direita (a abertura virada para o taverneiro, o ombro), no escuro, só com a luz no contorno; a caneca do da
  direita no tampo. Nenhum cobre o rosto, as mãos nem a caneca do taverneiro.
- **A luz:** o halo quente da lareira e o do lampião em anéis, a sala escurecendo em degraus pontilhados longe deles (a
  viga, os cantos, a frente do balcão). As chamas e a do lampião em 4 quadros (os efeitos de sempre); o taverneiro não
  se mexe.

**A referência e as diferenças:** a imagem foi lida ampliada para o enquadramento, a composição do balcão e do espaço
de trabalho, o porte, a expressão e a atividade do taverneiro, a personalidade dos produtos e as silhuetas da frente;
nada dela foi reduzido para virar arte. Diferenças: o barril mostra o tampo da direita, o lado que a câmera vê (ele fica
à esquerda do centro), com a torneira virada para o meio; a porta da direita é a da despensa (a única porta da cena);
menos objetos, cada um apoiado (a prateleira, os ganchos, o berço, o prego); a textura e a granulação da imagem ficam de
fora. A segunda referência ("Taverna sombria e o estalajadeiro desconfiado-2", de três quartos) não entrou na
construção.

**Os pontos e o balcão** (só na demonstração): só o que está desenhado tem ponto. O **Taverneiro** leva ao cartão da
bebida e dos rumores, com o nome acima da cabeça; a **Despensa** (só enquanto ela espera) é a porta da direita, com o
nome no alto da folha. Não há escada, porta da rua nem Morel nesta vista: o Dormir, o Homem do canto e o Voltar à vila
ficam nos cartões, e o Esc volta à vila. A demonstração filtra os pontos pela candidata à vista (`demo.cenas_js`); no
jogo, o motor mandaria só os da cena integrada. Os serviços, os preços, as regras, os encontros e as condições não
mudaram.

**A fonte e a exportação** (`g/fonte.py`): a fonte é `g/aseprite/taverna-g.aseprite` (320×96, 4 quadros; as camadas
fundo, fogo, lampiao, caldeirao, taverneiro e frente). `--criar` a gera do código e não a sobrescreve sem `--refazer`;
depois de criada, os retoques se fazem nela. Sem opção, `fonte.py` exporta da fonte para `camadas/g/` (o fundo composto
e as tiras do fogo e do lampião, cortadas pelo que fica na frente delas); `--conferir` compara com o desenho do código
(hoje, 4 de 4 iguais: a fonte não tem retoques).

**Conferido** (`g/conferir.mjs`, no jogo da demonstração, a 1920×945 e a 1280×720): em cada estado (o homem do canto, a
despensa esperando, Morel conhecido, recrutado, sem ouro), os pontos esperados, os nomes dentro da arte sem cobrir o
rosto nem as mãos, cada ponto levando ao cartão dele, os cartões e o Voltar acima da doca; o Tab chegando ao ponto, o
Esc e o Voltar à vila voltando à vila, a pose parada parando o fogo, o console sem erro.

**Os limites que ficam:**
- os fregueses da frente são silhuetas escuras: leem como cabeça e ombro, mas pesam nos cantos de baixo, e o da
  esquerda cobre a ponta esquerda do fogo;
- o rosto em ~23 px é maior que o das figuras aprovadas (o detalhe acompanha a câmera); a sobrancelha, o olho de lado e
  a boca resolvem a expressão, sem rugas nem dentes;
- a camisa clara é a maior mancha da cena (de propósito, o foco), com poucas dobras;
- a parede do fundo é a mesma pedra de cima a baixo;
- a fonte ainda não tem retoques à mão: tudo saiu do código.

**Para integrar (se aprovada):** o motor mandaria `cena_taverna` em `estado.local.interiores` só com os pontos da G
(Taverneiro, Despensa); `telas/cenas.js` passaria a aceitar `servicos: "<serviço>"`; o balcão compacto
(`tela/taverna.css`, `tela/balcao.js`) iria para o jogo; a animação do taverneiro, pelo fluxo da skill
`arte-cenas-fenda`, viria depois da aprovação da estática.

## Os arquivos

- `g/desenho.py` e `g/taverneiro.py`: a G (o espaço, os objetos, o balcão, os fregueses, a luz, o fogo; o taverneiro);
  `g/fonte.py`: a fonte em Aseprite e a exportação para `camadas/g/`; `g/conferir.mjs`: a conferência no jogo, da G e
  da H.
- `g2/retoques.py` e `g2/fonte.py`: a G refinada (os retoques seletivos e a fonte dela, feita da fonte da G).
- `g3/retoques.py` e `g3/fonte.py`: a G3 (as correções locais e a fonte dela, feita da fonte da G2).
- `g4/taverneiro.py` e `g4/fonte.py`: o balcão animado (as poses e a rotina do taverneiro, o garrafão, a fonte).
- `morel/vista/morel-vista.aseprite` e `morel/vista/exportar.py`: a vista diante de Morel (a segunda passada; a
  primeira em `morel/vista-v1/` e `camadas/morel-vista-v1/`)
  (`camadas/morel-vista/`); `tela/cena-taverna-anim.js`: as duas cenas animadas.
- `morel/aseprite/morel-mesa.aseprite` e `morel/exportar.py`: o estudo livre de Morel e a exportação dele
  (`camadas/morel/estudo.png`).
- `h/desenho.py`, `h/taverneiro.py` e `h/fonte.py`: a H (histórico).
- `f/` a `b/`, `prova/` e a raiz (`desenho.py`, `gente.py`): o salão panorâmico, histórico.
- `exportar.py`: as camadas da A em `camadas/` e as dos estudos estáticos em `camadas/b/` a `camadas/f/`.
- `tela/cena-taverna-b.js`: as cenas estáticas da B à H e a escolha entre elas (`window.CenaTaverna`);
  `tela/cena-taverna-prova.js`: a prova de qualidade; `tela/cena-taverna.js`: a A; `tela/faixa.js`: o botão Protótipo;
  `tela/taverna.css` e `tela/balcao.js`: os nomes e o balcão.
- `demo.py` e `demo.bat`: a demonstração.

# Histórico: a prova de qualidade e o M1 (o salão panorâmico, suspenso)

Os dois jogadores, a mesa e os banquinhos em duas grades nativas (A, a atual; B, o dobro), no mesmo lugar da tela,
sobre a F; a **B2**, só esse conjunto refinado na grade da B pela referência "Jogo de tabuleiro na taverna", com a fonte
em Aseprite (`prova/b2`); a **B3**, a B2 com os ombros e os braços redesenhados (`prova/b3`); a **B4**, a B3 com o ombro
de cá do de verde suavizado (`prova/b4`); e o **M1**, Morel, a cadeira e a mesa dele na densidade da B4 (`prova/m1`). O
método, as medidas e as conclusões estão em [prova/LEIA-ME.md](prova/LEIA-ME.md). No botão Protótipo: "Prova: os
jogadores (histórico)", com as grades, o isolado e o canto de Morel.

# Histórico: a candidata F

**A candidata F é um estudo estático** (29/10/2026), sem aprovação e sem integração: a composição, as poses e a relação
entre pessoas e móveis da referência "Taverna medieval entre brasas e sombras", transpostas para a grade e o
acabamento do jogo.

**O roteiro que se usava para avaliá-la:**

1. Entre na Taverna e olhe no tamanho do jogo, ao lado da referência: o balcão à esquerda, com o taverneiro e as
   prateleiras atrás, a porta da rua e a da despensa no fundo; a mesa da frente com três; a lareira com o velho; os
   jogadores à direita; a escada até a galeria; Morel na beira direita.
2. Os conjuntos: a freguesa com o cotovelo na mesa; o freguês de costas com a cabeça, o pescoço e os ombros acima da
   mesa; o homem da cabeceira erguendo a caneca, na cadeira de espaldar; os jogadores nos banquinhos (o de verde
   pensa, o de ocre mexe a peça); o velho com as mãos para o fogo; Morel na cadeira robusta, a colher na tigela.
3. A escada (sobe da direita para a esquerda até o patamar), o patamar (no esteio) e a galeria (o piso, a testeira,
   os esteios, o guarda-corpo, as portas inteiras).
4. Compare com a **E** no mesmo estado e troque para **Morel recrutado** (a cadeira e a mesa vazias).
5. Os nomes pelo mouse ou pelo Tab (Taverneiro, Escada, Homem do canto, Despensa, Saída); Esc.

**Como foi construída:**
- **A referência medida, não reduzida:** a imagem foi lida na grade do jogo (320 de largura, com uma grade de 10 px)
  para as posições e os tamanhos; nada dela vira arte.
- **A projeção da E, com a câmera da referência** (`f/desenho.py`, `P`): mais perto e mais alta (14 px por metro no
  fundo, 28 na borda de baixo, o olho a 3 m, de onde se veem os tampos, os assentos, os degraus e o piso da galeria).
  As pessoas da frente têm a cabeça de ~7 a 8 px, as do meio de 6, as do fundo de 5.
- **Primeiro a construção:** as paredes, o piso de lajes, os móveis como caixas projetadas e a figura de referência em
  pé e sentada em cada lugar; depois as pessoas, à mão, no ponto que a projeção dá a cada assento.
- **A planta, pela referência:** no fundo, a porta da rua (fechada), as prateleiras com poucos objetos e a porta da
  despensa atrás da ponta do balcão, a lareira grande com o caldeirão e a laje, e à direita a galeria com as portas de
  dois quartos; a escada sobe da direita (o pé, no chão) para a esquerda (o patamar, num esteio, ligado à galeria);
  o balcão a 2 m do fundo, o taverneiro atrás, dois banquinhos vazios na frente; a mesa da frente com três; a mesa
  redonda dos jogadores; Morel na beira direita, na cadeira robusta de espaldar, com a mesa individual inteira.
- **As pessoas junto dos móveis:** o quadril no assento, o tronco e as pernas para a mesma atividade, as coxas debaixo
  do tampo, as mãos nos objetos, os pés no piso quando aparecem.

**As diferenças em relação à referência:**
- a galeria tem a altura que a projeção dá (2,1 m) e as portas inteiras; na imagem ela é baixa demais para a
  profundidade em que fica;
- a mesa de Morel aparece inteira, com margem à direita (na imagem, a borda a corta);
- Morel segue a aparência do jogo, sem a capa, as armas e as placas da imagem; o banco comprido das candidatas
  anteriores virou a cadeira de espaldar da referência;
- sem os estandartes, a cabeça de cervo, o tapete e as ervas penduradas; a porta da rua fechada (a hora e o clima);
- a arandela na parede da esquerda e o lampião sobre o balcão são as fontes de luz da esquerda.

**Os compromissos que ficam:**
- as pessoas da frente ficam um pouco menores que as da imagem (a cabeça do freguês de costas tem 8 px; na referência
  medida, ~9);
- a mão da freguesa no queixo é um gesto pequeno nessa escala (o cotovelo na mesa lê melhor que a mão);
- o velho junto do fogo e o taverneiro, no fundo, têm 5 px de cabeça;
- o corrimão da escada passa na frente da galeria, como numa escada real nesse lugar.

**O que se previa para integrá-la:**
- O motor mandaria `cena_taverna` em `estado.local.interiores` (como `servicos.cena_templo`), com a regra de Morel no
  motor (hoje uma hipótese registrada em `demo.morel_no_canto`).
- `telas/cenas.js` passaria a aceitar `servicos: "<serviço>"` (o ponto leva ao cartão daquele serviço; hoje,
  `servicos: true` leva ao primeiro). A demonstração serve o cenas.js com essa mudança (`demo.cenas_js`).
- O balcão compacto com o interior (`tela/taverna.css`) e a rolagem repetida (`tela/balcao.js`) iriam para o jogo,
  valendo para todo balcão com interior (o templo também).
- A animação do elenco novo, a fonte em Aseprite pelo fluxo da skill `arte-cenas-fenda` e a cena de produção lendo de
  `static/cenas/taverna/`.
- Os arquivos: `f/desenho.py` e `f/gente.py` (a projeção, o espaço, os móveis, a figura de referência, a luz, o fogo,
  as velas; as pessoas, à mão); de `e/` a `b/`, as anteriores, do mesmo jeito.

# Histórico: a candidata E

**Por que mudou a direção:** a D melhorou os apoios, mas a escala e a perspectiva não convenciam, sobretudo entre
Morel e a mesa dos jogadores: o piso seguia uma perspectiva verdadeira com o olho baixo, e os tampos, os assentos, o
balcão e a galeria mostravam a face de cima em quantidades escolhidas uma a uma; a parede parecia frontal e cada móvel
estava num grau. Continuar ajustando as pessoas no lugar não resolvia.

**A câmera e a projeção** (`e/desenho.py`, `P`): uma perspectiva simplificada e consistente, a mesma para tudo:
x = 160 + X·m(Z), y = 56 + 5,33·Z − H·m(Z), m(Z) = 14 + Z. A câmera um pouco elevada (cada metro de piso desce 5,3 px,
e a face de cima de mesas, bancos, degraus e da galeria aparece pela mesma conta), a escala crescendo pouco do fundo
(14 px/m) à borda de baixo (22), as paredes do lado convergindo e encontrando o piso. Os móveis são caixas projetadas:
a face de cima, a da frente e a do lado que olha para o meio.

**A escala:** uma figura de referência (cinza, 1,75 m em pé e sentada com o quadril a 0,45 m) foi posta na porta, no
balcão, no pé da escada, debaixo da galeria, no meio da sala e em cada assento, antes das pessoas; as portas, os
degraus, os tampos e os bancos foram conferidos contra ela. Depois, as pessoas foram desenhadas à mão no lugar que a
projeção dá ao assento de cada uma, com a cabeça de ~0,27 m. Morel é maior (o alto da cabeça a 1,45 m sentado, os
ombros mais largos) e usa um banco robusto, na mesma régua.

**A organização:** no fundo, da esquerda para a direita, a porta da despensa (entreaberta, na ponta de trás do balcão),
a porta da rua, a lareira (saindo 0,5 m da parede, com a laje) e a escada encostada na parede até o patamar e a
galeria, com as portas de dois quartos; à esquerda, o balcão a 3 m do fundo, o taverneiro atrás e o aparador com as
prateleiras; na mesma faixa da sala (a 5–7 m), a mesa comprida com três (esquerda) e a redonda com dois (direita); Morel
contra a parede da direita, um pouco mais para o fundo; o velho junto do fogo; a passagem livre no meio, da porta da
rua até a frente, o balcão, as mesas e o pé da escada.

**O que veio da D:** os objetos das prateleiras, as atividades, a luz contínua (sem anéis no reboco), o contexto da
taverna embaixo da cena (sem a narração da praça), os serviços e os pontos.

**Os compromissos que ficam:** a câmera mais aberta deixa as pessoas um pouco menores que as da frente da D (cabeças de
5 a 6 px; Morel com o rosto de 6 px, reconhecido pela roupa); os degraus da escada aparecem como paralelogramos (a
projeção inclina as faces de cima); o chão da frente da direita fica livre (a circulação, não um vazio a preencher);
as portas dos quartos têm o alto debaixo da viga do teto.

**Para o futuro, sem compromisso:** um salão geral com aproximações para conversas ou atividades específicas (a mesa de
Morel, o balcão) fica anotado como possibilidade; nada implementado.

# Histórico: a candidata D

**O que a C tinha de errado** (a avaliação do Jean): Morel na ponta do banco, longe do espaldar; a cadeira vazia
grande demais, o encosto atravessando o tampo; o jogador de amarelo suspenso atrás da mesa; o homem de marrom sentado
na mesa e no balcão ao mesmo tempo; o freguês de costas com os ombros em barra e o tronco fino; as mãos e a caneca do
taverneiro numa mancha clara; o velho do fogo sem pose; os degraus quase só espelho; o guarda-corpo mais forte que o
piso da galeria; a boca da lareira chapada; as faixas concêntricas no reboco; a direita fundida; a narração da praça
embaixo do interior.

**O que a D faz** (`d/desenho.py`, `d/gente.py`):
- **Cada conjunto resolvido junto**, nesta ordem: o assento (onde o quadril pousa), a orientação do quadril, do tronco
  e das pernas, o alcance até a mesa (o braço de 0,6 m), a atividade.
  - **Morel:** o banco de espaldar com o espaldar na ponta da direita; Morel sentado junto dele, as costas apoiadas, o
    quadril no assento, as coxas para a frente e as botas no piso; inclinado para a mesa, a colher na tigela do
    ensopado e a outra mão na borda. O couro, o vermelho no peito e a ombreira o reconhecem de longe; a cicatriz é um
    traço claro só. A mesa veio para perto, com a tigela na ponta dele.
  - **A mesa redonda:** cada jogador no seu banquinho (o de amarelo atrás da mesa, com as coxas e as canelas visíveis
    embaixo do tampo; o velho de verde de perfil, o braço chegando à peça); o banquinho vazio na escala certa, fora do
    tampo; as roupas mais claras para se separar da madeira e do piso.
  - **A cabeceira:** o homem de barba ruiva numa cadeira de lado, o encosto atrás das costas, o antebraço no tampo
    com a caneca; o balcão termina antes dele e perdeu os banquinhos, que atravessavam as pernas.
  - **O freguês de costas:** os ombros caindo do pescoço, os braços separados do tronco pela costura e chegando aos
    cotovelos na borda da mesa, a cintura, e o quadril mais largo assentado no banco.
  - **O taverneiro:** o avental de couro escuro (a caneca e as mãos se leem contra ele); a mão de lá segura a caneca
    pela asa e a de cá esfrega com o pano, na altura do peito.
  - **O velho do fogo:** inclinado para a lareira, os antebraços estendidos, as palmas abertas para o fogo, as coxas
    para a frente no banquinho baixo.
- **A escada:** dez degraus de piso largo (o claro de cima com a aresta) e espelho baixo, menos íngreme, chegando ao
  patamar; **a galeria:** o piso mais largo e mais claro (a faixa por onde se anda até as portas), o guarda-corpo
  discreto (o corrimão fino, os balaústres espaçados), as portas inteiras debaixo da viga.
- **A lareira:** a verga fina (não domina mais), as ombreiras com a aresta clara (a espessura da pedra), as faces de
  dentro alargando para baixo com a aresta quente, o fundo escuro; o caldeirão pequeno e alto.
- **O balcão:** o tampo visto de cima, a borda grossa e clara, a sombra dela no corpo, o corpo mais escuro.
- **As prateleiras:** poucos objetos de silhueta diferente (duas canecas com a asa, a jarra bojuda com o bico e a asa,
  duas garrafas de gargalo fino, uma bilha, um prato de pé).
- **A luz:** contínua (o escuro cresce aos poucos, sem faixas nem anéis no reboco); a vela de Morel e a da redonda
  fazem ilhas de luz à direita.
- **Embaixo da cena** (só na demonstração): dentro da taverna, a narração da vila (a tábua no poço da praça) e o
  cabeçalho dela saem da página (`tela/balcao.js`, `tela/taverna.css`); o contexto é a frase da taverna que o jogo já
  tem, no balcão, uma vez só. Saindo, a narração da vila volta.

**Os compromissos que ficam:** o velho do fogo tem 4 px de cabeça; a perspectiva do piso da galeria é um pouco forçada
para ser lida; a canela do homem da cabeceira fica atrás da perna da mesa (é o que está na frente); dentro da taverna, a
página não mostra a narração anterior (se o jogador entrar logo depois de ouvir um rumor, o texto dele já foi lido na
página anterior); as pessoas não se mexem.

# Histórico: a candidata C

**O que a B tinha de errado** (a avaliação do Jean): profundidade demais (a diferença de três vezes entre as figuras da
frente e as do fundo não leu bem), as pessoas do fundo pequenas demais (Morel com 3 ou 4 px de cabeça), objetos com
cara de esboço (a escada uma diagonal de riscos, a galeria uma faixa sem piso, a lareira um bloco cinza), muito chão
vazio à esquerda e tudo concentrado à direita.

**O que a C faz** (`c/desenho.py`, `c/gente.py`):
- **A câmera:** o mesmo ângulo (de frente, um pouco de cima), com a profundidade contida: 13 px por metro na parede do
  fundo e 30 na borda de baixo (a B ia de 11 a 34). As pessoas importantes ficam no meio dessa faixa: o taverneiro a
  19, Morel a 20 (um pouco acima, "um homem grande"), os grupos de 20 a 34. O balcão veio para a frente junto com o
  taverneiro: ele aparece da cintura para cima, na régua.
- **A escada e a galeria, como estrutura:** o pilar do pé no chão, os degraus com o piso claro e o espelho escuro, o
  banzo de fora grosso, o corrimão nos balaústres; no alto, o pilar do patamar, que é o primeiro esteio da galeria. A
  galeria tem o piso visto de cima (a faixa por onde se anda entre as portas e o guarda-corpo, as tábuas), a testeira
  com as pontas das vigas (a espessura), dois esteios com mãos-francesas até sapatas de pedra no chão, o guarda-corpo
  com balaústres espaçados (o piso aparece entre eles) e as portas de dois quartos inteiras. A perspectiva da galeria é
  um pouco forçada (o piso dela aparece mais do que a altura do olho mostraria), para ele ser lido.
- **Os grupos:** três na mesa comprida da esquerda (a freguesa de três quartos, o freguês de costas no banco, o homem
  de colete de perfil na ponta), na frente do balcão, que fica atrás deles; dois na redonda, jogando (o tabuleiro no
  meio), com a cadeira vazia; o velho junto do fogo; Morel no banco de espaldar do canto, a mesa dele com a vela na
  ponta e o pão. A passagem do meio fica livre da porta até a lareira e o pé da escada; os bancos do balcão, vazios.
- **As pessoas:** à mão, com cabeça, pescoço, tronco, braços e mãos separados (o pescoço em pele entre a cabeça e a
  gola, o braço separado do tronco por uma costura ou um vão, a mão em pele na caneca, no tabuleiro, na colher); quem
  senta tem o quadril no assento, a coxa para a frente e a canela até o piso. Portes diferentes: o taverneiro
  corpulento, a freguesa miúda, o freguês de costas largo, o homem de colete de barba ruiva, o velho de barba grisalha,
  o moço de casaco ocre, Morel grande.
- **A lareira:** a laje no piso, a boca com as faces de dentro e o fundo de fuligem, a verga de madeira com a
  prateleira, a coifa que só abre embaixo e a chaminé estreita (não um bloco cinza); o fogo nos cães de ferro, com o
  caldeirão pequeno no gancho alto, as chamas aparecendo em volta.
- **O balcão:** o tampo visto de cima, a borda grossa, o corpo em almofadas, o rodapé; atrás, o aparador com o barril
  de torneira (a área de trabalho). As prateleiras com poucos grupos (as canecas emborcadas, a jarra, duas garrafas, o
  barrilete, os pratos de pé), com o vão atrás da cabeça do taverneiro.
- **Os objetos das mesas dizem a atividade:** a caneca nas mãos da freguesa, o pão na tábua e a jarra na comprida; o
  tabuleiro com as peças na redonda; o pão e a vela na de Morel.
- **A luz e os materiais:** a pedra do fundo mais calma (as juntas sem a aresta clara), o reboco claro, os móveis mais
  quentes que o piso; a sala escurece em faixas lisas, sem o pontilhado (que fazia anéis no reboco); a lareira, o
  lampião e as velas fazem as áreas acesas.

**Os limites que ficam:** o velho junto do fogo, no fundo, tem 4 px de cabeça; o rosto de Morel tem a cicatriz em dois
pixels claros (não dá para mais nessa distância); a perspectiva forçada do piso da galeria; as pessoas não se mexem; a
fonte em Aseprite só depois da aprovação. O balcão compacto embaixo da cena e a rolagem refeita continuam como na B (só
na demonstração).

# Histórico: a candidata B


**O que a A tinha de errado** (a avaliação do Jean): as pessoas estreitas, parecidas e quase todas de perfil; as três
mesas na mesma faixa de profundidade, com um par em cada ponta; o balcão enorme perto do taverneiro; as prateleiras
como filas de retângulos; piso, móveis, roupas e fundo no mesmo marrom; a escada saindo do quadro sem o acesso aos
quartos; no tamanho da HUD, um banner com figuras pequenas.

**O que a B faz** (`b/desenho.py`, `b/gente.py`):
- **A câmera:** de frente, um pouco de cima (o olho a ~2,1 m, o ponto de fuga dentro do quadro), com muita
  profundidade: 11 px por metro na parede do fundo e 34 na borda de baixo. Quem está na frente é três vezes maior que
  quem está no fundo, na mesma conta (`desenho.m`), e as portas, os móveis e as pessoas usam essa régua.
- **A planta:** a parede do balcão mais perto, à esquerda, virando para o fundo num canto de pedra; o salão fundo à
  direita. O balcão na proporção de quem está atrás dele (1,05 m: o taverneiro aparece da cintura para cima).
- **As mesas em três distâncias:** a comprida da frente (a freguesa de um lado, o freguês de costas no banco do outro,
  o pé de perto saindo do quadro), a redonda do meio (dois homens, a cadeira vazia de costas para nós), a pequena do
  canto (Morel); mais o velho no banquinho junto ao fogo e o freguês de pé no balcão.
- **A hospedaria:** a escada encostada no fundo sobe até o patamar e a galeria (2,2 m), apoiada em dois esteios, com as
  portas de dois quartos inteiras (batente, ferragens, argola); os quartos não têm interior.
- **A despensa:** uma porta baixa entreaberta na parede do balcão, entre a ponta dele e o canto, com o escuro da
  escada na fresta ("um porão baixo", `abertura.descer`). Um alçapão aberto foi tentado e lia como um caixote.
- **As pessoas, à mão:** cada uma numa grade própria, com silhueta e porte (o taverneiro corpulento, a freguesa de
  lenço, o freguês de costas largo de casaco azul, o velho de barba grisalha, o de casaco ocre, o velho de capuz),
  três tons por material, sem contorno, o olho de um pixel. Quem está atrás de um móvel é desenhado antes dele, e as
  mãos que pousam no tampo vêm depois. Morel segue a aparência do jogo, um pouco acima da escala (é "um homem grande").
- **Os materiais por valor:** a pedra do fundo fria e escura, o reboco do balcão claro e morno, a madeira dos móveis
  mais quente que o piso, as roupas em cores contidas e diferentes; o piso de tábuas paralelas ao fundo, com as juntas
  um tom só abaixo (as tábuas radiando de um ponto de fuga dentro do quadro viravam tracejado nas laterais). A lareira
  é o foco quente; os cantos escurecem.
- **As prateleiras:** grupos reconhecíveis (três canecas emborcadas, a jarra, duas garrafas, um barrilete, os pratos de
  pé), não uma fila; os barris em pé, de lado (deitados com o tampo para a sala, liam como rodas).
- **Fora da referência,** como na A: a placa, o tapete, os quadros, a garçonete andando, a rua pela porta aberta.

**O balcão embaixo da cena** (só na demonstração, `tela/taverna.css` e `tela/balcao.js`): com o interior à vista, o
topo do balcão fica numa linha (a fala e o ouro, como na forja) e os cartões vão em duas colunas, com o Voltar à vila
na próxima célula livre; tudo cabe acima da doca, sem rolar, a 1920×945 e a 1280×720. A rolagem automática do jogo é
feita uma vez quando o balcão monta; o texto da página ainda crescia depois, e a última linha ficava 42 px atrás da
doca: `balcao.js` repete a mesma conta quando a página muda, só para a frente.

**Ainda limitado:** Morel e o velho do fogo, no fundo, têm 3 a 4 px de cabeça (a cicatriz de Morel é um pixel claro);
as pessoas não se mexem; a fonte em Aseprite só depois da aprovação.

# Histórico: a candidata A

## O levantamento (o que o jogo estabelece)

- **O balcão:** "Fumaça, palha no chão e conversa baixa. O taverneiro nem levanta os olhos." (`app/vila.js`). Os
  cartões: Dormir até o amanhecer (`jogo.menu_vila`), Uma bebida e os rumores (a primeira caneca grátis depois da
  despensa), e os da abertura (`abertura.opcoes`): Descer à despensa (enquanto adiada) e Sentar com o homem do canto
  (depois da despensa, enquanto Morel nunca apareceu).
- **O que acontece dentro, pela bebida** (`servicos.ouvir_rumores`): os rumores, a briga de taverna, a queda de braço
  e o encontro com Morel (`eventos.comitiva.morel_na_taverna`: "No canto da taverna, um homem grande come sozinho, de
  costas para a parede"; "fala sem levantar os olhos do prato"; recusado, "volta ao ensopado").
- **A despensa** é "um porão baixo" (`abertura.descer`): daí o alçapão no piso.
- **Quem aparece:** o taverneiro (sem nome nem retrato no jogo: a figura é provisória) e Morel (a aparência segue
  `retratos.js`, `MOREL_FIGURA`: o cabelo e a barba castanhos, a cicatriz, a ombreira cinza num ombro e a pele no outro,
  o couro com o vermelho no peito). Ninguém mais conhecido: Odette, Yara e os outros não têm motivo para estar ali. Os
  fregueses são anônimos, sem fala nova.
- **A hora e o tempo:** os interiores do jogo (a forja, a curandeira, o templo) não mudam com o período; a taverna
  também não. Por isso a porta da rua fica fechada: uma rua de dia, com neve, na porta aberta da referência
  contradizia a noite e a chuva que a vila mostra.

## As decisões desta candidata

- **A câmera:** um pouco mais longe que o templo (a régua: 23 px por metro na borda de baixo do quadro, contra 28,2 no templo), a sala
  inteira de frente, com o ponto de fuga acima do quadro; o piso em tábuas que convergem para ele.
- **A organização da referência, corrigida:** a entrada à esquerda; o balcão e as prateleiras no fundo, com o barril
  deitado no cavalete; as mesas em profundidade (três na frente, ocupadas); a lareira com o caldeirão na cremalheira
  e a lenha empilhada; a escada para os quartos, com a galeria e a porta de um quarto (os quartos não têm interior);
  o canto reservado debaixo da escada; os caminhos livres entre a porta, o balcão, a lareira e a escada.
- **Fora da referência:** a placa pendurada dentro da porta, o tapete, os quadros na parede, a garçonete andando (nada
  anda nesta etapa), a rua de fora, as texturas de pedra e madeira miúdas e as sombras suaves.
- **As pessoas** (`gente.py`): cada figura em duas camadas (o corpo atrás da mesa ou do balcão; as mãos e o que
  seguram na frente), os braços com comprimento fixo (a mão fora do alcance é um erro de construção, não um braço
  esticado), o tronco inclinado como um bloco (só a cintura acomoda), as medidas pela régua do piso. As atividades:
  o taverneiro limpa uma caneca, olha contra a luz e a pousa; Morel come o ensopado sem levantar os olhos; junto do
  fogo, alguém aquece as mãos e se ajeita; à esquerda, um bebe e a outra come e ri; no meio, dois jogam, um de cada
  vez; à direita, um conta e o outro escuta, acena e responde (as duas mesas do meio e da direita se revezam de
  propósito: as fases iguais em `exportar.py`).
- **Os pontos** (`demo.cena_taverna`): só os que correspondem a ações que existem. A Despensa e o Homem do canto
  aparecem só enquanto o cartão deles existe; antes de o herói conhecer Morel, o nome é "Homem do canto".
- **Quando Morel está no canto** (`demo.morel_no_canto`, proposta para o Jean): livre (fora da comitiva) e com o
  encontro ainda possível (o evento acontece até 3 vezes, a partir do dia 2) ou com a abertura esperando por ele.

## Os arquivos da A

- `desenho.py`: o espaço (as paredes, o piso, a porta, o balcão, a lareira, a escada, o alçapão, as mesas), a luz, o
  fogo e as velas; `frente_moveis()` (as mesas e o balcão que ficam na frente dos corpos).
- `gente.py`: as figuras (sentadas de perfil e de frente atrás de um móvel), as poses e as rotinas.
- `exportar.py`: as camadas em `camadas/` (`fundo`, `fogo`, `frente`, `velas`, uma tira por pessoa em `gente/` e o
  `taverna.json`). Só escreve em `camadas/`.
- `tela/cena-taverna.js`: a cena (a ordem: fundo, fogo, corpos, móveis da frente, mãos, velas); `tela/faixa.js` e
  `tela/taverna.css`: o botão Protótipo e o painel.
- `demo.py` e `demo.bat`: a demonstração.
