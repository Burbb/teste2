# Protótipo: o interior da taverna (candidata A)

A primeira candidata jogável do interior da taverna do Vau, **só no protótipo** (29/10/2026): nada daqui entra no jogo
até o Jean avaliar. A referência de composição é `ferramentas/arte/referencias/cenarios internos/Taverna medieval entre
fogo e sombras.png` (o papel dela está no LEIA-ME daquela pasta).

## Abrir

Dê dois cliques em `demo.bat` (ou `python ferramentas/prototipos/taverna/demo.py` na raiz). O jogo abre no navegador
num **save temporário** (uma pasta nova a cada vez; os saves do Jean não são lidos nem tocados), na porta 8795: o
Guerreiro no Vau, com a campanha começada e 60 de ouro. Clique na **Taverna** na vila: a vista mostra o interior no
lugar da vila aproximada, e o balcão de sempre fica embaixo, com os cartões que já existem.

O botão **Protótipo** na barra do alto (entre os sigilos e o menu) abre o painel dos estados:

| Botão | O que faz |
|---|---|
| **Despensa esperando** | a despensa da abertura adiada: o cartão "Descer à despensa" e o ponto da Despensa; Morel no canto (ele assiste à luta), sem ponto |
| **Homem do canto** (o estado de abertura) | a despensa feita, a primeira caneca por conta da casa e o cartão "Sentar com o homem do canto", com o ponto dele |
| **Morel conhecido** | dia 3, Morel já falou com o herói e foi recusado: continua comendo no canto, sem ponto (o encontro volta pela bebida, como no jogo) |
| **Morel recrutado** | Morel na comitiva: o canto fica vazio (a mesa com a vela), sem Morel repetido |
| **Sem ouro** | Morel conhecido e 0 de ouro: os preços em vermelho nos cartões; a cena igual |
| **Pose parada** | o movimento reduzido (o mesmo que a preferência do sistema) |

Diante da taverna, a troca sai, muda o estado e entra de novo.

## Roteiro curto para avaliar

1. Na vila, clique na Taverna. Olhe a sala no tamanho do jogo antes de ampliar: a porta à esquerda, o balcão no
   fundo, as três mesas da frente, a lareira, a escada e o canto debaixo dela.
2. Passe o mouse (ou o Tab) pelos nomes: **Taverneiro** leva ao cartão da bebida, **Escada** ao Dormir, **Homem do
   canto** ao Sentar com ele, **Saída** volta à vila. Nenhum ponto gasta ouro: todos levam ao cartão, onde está o preço.
3. Deixe a cena correr uns 20 segundos: cada mesa tem a sua atividade, com pausas, e ninguém muda junto.
4. Troque para **Despensa esperando** (o ponto do alçapão) e para **Morel recrutado** (o canto vazio).
5. Ligue **Pose parada**: todos ficam numa pose natural, e os pontos continuam valendo.

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

## Para integrar (se aprovada)

- O motor mandaria `cena_taverna` em `estado.local.interiores` (como `servicos.cena_templo`), com a regra de Morel no
  motor.
- `telas/cenas.js` passaria a aceitar `servicos: "<serviço>"` (o ponto leva ao cartão daquele serviço; hoje,
  `servicos: true` leva ao primeiro). A demonstração serve o cenas.js com essa mudança (`demo.cenas_js`).
- A fonte em Aseprite, pelo fluxo da skill `arte-cenas-fenda` (como `templo/fonte.py`), e a cena de produção lendo de
  `static/cenas/taverna/`.

## Os arquivos

- `desenho.py`: o espaço (as paredes, o piso, a porta, o balcão, a lareira, a escada, o alçapão, as mesas), a luz, o
  fogo e as velas; `frente_moveis()` (as mesas e o balcão que ficam na frente dos corpos).
- `gente.py`: as figuras (sentadas de perfil e de frente atrás de um móvel), as poses e as rotinas.
- `exportar.py`: as camadas em `camadas/` (`fundo`, `fogo`, `frente`, `velas`, uma tira por pessoa em `gente/` e o
  `taverna.json`). Só escreve em `camadas/`.
- `tela/cena-taverna.js`: a cena (a ordem: fundo, fogo, corpos, móveis da frente, mãos, velas); `tela/faixa.js` e
  `tela/taverna.css`: o botão Protótipo e o painel.
- `demo.py` e `demo.bat`: a demonstração.
