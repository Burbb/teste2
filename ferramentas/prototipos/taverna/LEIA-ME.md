# Protótipo: o interior da taverna (candidatas A a F e a prova de qualidade)

**Agora: a prova de qualidade** (29/10/2026): as reconstruções completas estão interrompidas; os dois jogadores, a mesa e
os banquinhos em duas grades nativas (A, a atual; B, o dobro), no mesmo lugar da tela, sobre a F; e a **B2**, só esse
conjunto refinado na grade da B pela referência "Jogo de tabuleiro na taverna", com a fonte em Aseprite
(`prova/b2`); e a **B3**, a B2 com os ombros e os braços redesenhados para lerem sem ambiguidade (`prova/b3`); e a
**B4**, a B3 com o ombro de cá do de verde suavizado (`prova/b4`). O método, as medidas e as conclusões estão em
[prova/LEIA-ME.md](prova/LEIA-ME.md). Depois, o **M1**: Morel, a cadeira e a mesa dele na densidade da B4
(`prova/m1`). `demo.bat` abre na cena completa com a B4 e o M1, com a A, a B, a B2, a B3 e o canto da F para comparar (o
botão Protótipo diz as versões à vista); a F e as anteriores seguem no botão Protótipo, como histórico.

**A candidata F é um estudo estático** (29/10/2026), agora histórico, sem aprovação e sem integração: a composição, as poses e a relação
entre pessoas e móveis da **nova referência aprovada pelo Jean** ("Taverna medieval entre brasas e sombras", em
`ferramentas/arte/referencias/cenarios internos`), transpostas para a grade e o acabamento do jogo. As pessoas ficam
paradas; a animação vem só depois de a construção ser aprovada. **Da E à A, histórico.**

## Abrir

Dê dois cliques em `demo.bat` (ou `python ferramentas/prototipos/taverna/demo.py` na raiz). O jogo abre no navegador
num **save temporário** (os saves do Jean não são lidos nem tocados), na porta 8795: o Guerreiro no Vau, com a
campanha começada e 60 de ouro. Clique na **Taverna** na vila. Se uma demonstração antiga estiver aberta, feche a
janela dela antes (a porta é a mesma).

O botão **Protótipo** na barra do alto abre o painel: a candidata (**F**, o padrão; da **E** à **A**, o histórico), o
estado do save (**Despensa esperando**, **Homem do canto**, **Morel conhecido**, **Morel recrutado**, **Sem ouro**) e
a **Pose parada**.

## Roteiro curto para avaliar a F

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

## A candidata F

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

## Para integrar (se aprovada)

- O motor mandaria `cena_taverna` em `estado.local.interiores` (como `servicos.cena_templo`), com a regra de Morel no
  motor (hoje uma hipótese registrada em `demo.morel_no_canto`).
- `telas/cenas.js` passaria a aceitar `servicos: "<serviço>"` (o ponto leva ao cartão daquele serviço; hoje,
  `servicos: true` leva ao primeiro). A demonstração serve o cenas.js com essa mudança (`demo.cenas_js`).
- O balcão compacto com o interior (`tela/taverna.css`) e a rolagem repetida (`tela/balcao.js`) iriam para o jogo,
  valendo para todo balcão com interior (o templo também).
- A animação do elenco novo, a fonte em Aseprite pelo fluxo da skill `arte-cenas-fenda` e a cena de produção lendo de
  `static/cenas/taverna/`.

## Os arquivos

- `f/desenho.py` e `f/gente.py`: a F (a projeção, o espaço, os móveis, a figura de referência, a luz, o fogo, as
  velas; as pessoas, à mão); de `e/` a `b/`: as anteriores, do mesmo jeito.
- `exportar.py`: as camadas da A em `camadas/` e as dos estudos estáticos em `camadas/b/` a `camadas/f/` (o fundo com e sem
  Morel, o fogo, as velas).
- `tela/cena-taverna-b.js`: as cenas estáticas da B à F e a escolha entre as seis (`window.CenaTaverna`);
  `tela/cena-taverna.js`: a A;
  `tela/faixa.js`: o botão Protótipo; `tela/taverna.css` e `tela/balcao.js`: os nomes e o balcão.
- `demo.py` e `demo.bat`: a demonstração.

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
