# Protótipo: o interior da taverna (candidatas A e B)

**A candidata B é um estudo estático** (29/10/2026): a sala, a arquitetura e as pessoas redesenhadas depois que a A não
foi aprovada visualmente; as pessoas ficam paradas numa pose de atividade, e a animação vem só depois de a construção
ser aprovada. **A A fica como histórico** (os ciclos de animação dela inclusive). Nada daqui entra no jogo até o Jean
avaliar. A referência de composição continua sendo `ferramentas/arte/referencias/cenarios internos/Taverna medieval
entre fogo e sombras.png` (o papel dela está no LEIA-ME daquela pasta).

## Abrir

Dê dois cliques em `demo.bat` (ou `python ferramentas/prototipos/taverna/demo.py` na raiz). O jogo abre no navegador
num **save temporário** (uma pasta nova a cada vez; os saves do Jean não são lidos nem tocados), na porta 8795: o
Guerreiro no Vau, com a campanha começada e 60 de ouro. Clique na **Taverna** na vila: a vista mostra o interior no
lugar da vila aproximada, e o balcão de sempre fica embaixo, com os cartões que já existem.

O botão **Protótipo** na barra do alto (entre os sigilos e o menu) abre o painel:

| Botão | O que faz |
|---|---|
| **Candidata B (estudo estático)** / **Candidata A (histórico)** | troca a sala (a demonstração abre na B; os pontos acompanham) |
| **Despensa esperando** | a despensa da abertura adiada: o cartão "Descer à despensa" e o ponto da Despensa; Morel no canto (ele assiste à luta), sem ponto |
| **Homem do canto** (o estado de abertura) | a despensa feita, a primeira caneca por conta da casa e o cartão "Sentar com o homem do canto", com o ponto dele |
| **Morel conhecido** | dia 3, Morel já falou com o herói e foi recusado: continua comendo no canto, sem ponto (o encontro volta pela bebida, como no jogo) |
| **Morel recrutado** | Morel na comitiva: o canto fica vazio (a mesa com a vela), sem Morel repetido |
| **Sem ouro** | Morel conhecido e 0 de ouro: os preços em vermelho nos cartões; a cena igual |
| **Pose parada** | o movimento reduzido (na B, o fogo e as velas param; na A, as pessoas também) |

Diante da taverna, a troca de estado sai, muda e entra de novo; a de candidata troca a sala no lugar.

## Roteiro curto para avaliar a B

1. Na vila, clique na Taverna. Olhe a sala no tamanho do jogo antes de ampliar: a parede do balcão mais perto, à
   esquerda (a porta da rua, os barris, o taverneiro sob o lampião, a porta baixa da despensa); o salão fundo à
   direita (a lareira, o velho que se aquece, a escada até a galeria com as portas dos quartos, Morel no canto debaixo
   dela); as mesas em três distâncias.
2. As pessoas: o taverneiro de frente, o freguês de pé no balcão de perfil, a freguesa de três quartos e o freguês de
   costas na mesa da frente (os maiores), os dois da mesa redonda (três quartos e perfil) com a cadeira vazia, o velho
   de perfil junto ao fogo e Morel de frente.
3. Passe o mouse (ou o Tab) pelos nomes: **Taverneiro** leva ao cartão da bebida, **Escada** ao Dormir, **Homem do
   canto** ao Sentar com ele, **Despensa** (em Despensa esperando) à porta baixa, **Saída** volta à vila.
4. Troque para **Morel recrutado** (o canto vazio) e para a **Candidata A**, para comparar.

## A candidata B (o estudo estático)

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

- `b/desenho.py`: o espaço, os móveis, a luz, o fogo e as velas da B; `b/gente.py`: as pessoas da B, à mão.
- `exportar.py`: as camadas da A em `camadas/` e as da B em `camadas/b/` (o fundo com e sem Morel, o fogo, as velas).
- `tela/cena-taverna-b.js`: a cena da B e a escolha entre as duas (`window.CenaTaverna`); `tela/cena-taverna.js`: a A;
  `tela/faixa.js`: o botão Protótipo; `tela/taverna.css` e `tela/balcao.js`: os nomes e o balcão.
- `demo.py` e `demo.bat`: a demonstração.

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
