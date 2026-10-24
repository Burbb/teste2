# 1E.4: o mapa e o minimapa da campanha (23/10/2026; levantamento e primeiro lote; nada no jogo)

**Pedido do Jean:** levantar os caminhos, os símbolos dos lugares, a posição do jogador, as marcas de missão e contrato,
os estados, os tamanhos e os compartilhamentos do mapa e do minimapa, priorizando a campanha; depois, um primeiro lote
pequeno de protótipos, só aqui, aguardando a avaliação. Navegação, áreas de clique, destinos, regras de viagem,
descoberta e progressão não mudam. Produção consultada: **1.199.3**.

## As folhas

- **`levantamento.png`**: onde o mapa aparece (a página e o mapa grande a 1920×945), o minimapa e o mapa grande em
  tamanho real, as peças de hoje em contexto e ampliadas sem suavizar, e o resumo do que se achou.
- **`pecas.png`** (revisada): a cancela antes e agora, a plaqueta B com as três classes (em cima e de lado), as marcas
  de missão e contrato e a seta A, a 1× e a 4×.
- **`comparacao.png`** (revisada): atual × B (a escolhida) × A (a alternativa), nas quatro situações da campanha, com os
  mesmos dados (o minimapa a 2×, o mapa grande a 1×, o lugar atual a 2×) e a legenda.
- **`origem-lugares.png`**: de onde vêm os ícones de lugar de 32 e 40 (a referência, o recorte, as duas reduções).
- **`presenca-lugares.png`**: o mapa grande com o 40 aprovado e com um 48 pelo mesmo processo.
- **`nativos.png`**: a vila e a floresta em grade nativa (32 e 48), antigo × novo, e o nome perto da borda.
- **`cinco.png`**: os cinco símbolos da campanha em grade nativa, antigo × novo de dia e à noite, e o nome do Bosque.
- As capturas inteiras, a 1920×945: `capturas/atual/`, `capturas/proposta-b/` (a escolhida, com o 40),
  `capturas/proposta-b48/` (com o 48 no mapa grande) e `capturas/proposta-a/` (a alternativa); para cada situação:
  `-pagina`, `-mundo`, `-mini`, `-mapa`, `-grande`, `-janela`, com o `registro.json` de cada bateria (o canvas nativo e
  exibido, os símbolos, os botões, os centros, o console).

## A revisão depois da escolha do Jean (23/10/2026): a direção B, a cancela, as fontes, o estado fechado

**A escolha:** a direção **B** (o herói na plaqueta) é a principal; a **A** (a seta) fica preservada como alternativa
(`POS=a` no roteiro de fotos; as peças `posicao` e `posicao-mini` continuam em `proposta/`). Tudo continua só no
protótipo, aguardando a avaliação.

### 1. A origem dos ícones de lugar de 32 e 40 (o que temos; nada foi redesenhado)

- **Os arquivos reaproveitados:** os 16 `rpg/web/static/hud/icones/lugar-<vila|floresta|pantano|ruinas|planicie|
  cidadela|caverna|montanha>-<32|40>.png` (o protótipo usa os da vila, do pântano, da floresta, das ruínas e da
  planície; a caverna, no covil do procedural). São idênticos, byte a byte, aos de
  `ferramentas/prototipos/hud/assets4p/exibicao/`, e o script `preparar_hud4p.py` os refaz idênticos hoje (conferido
  pelo `auxiliares/lugares48.py`, que repete o processo antes de gravar o 48).
- **A referência** (a origem do desenho): `assets4p/original/lugares-atributos-recursos.webp`, 1122×1402, uma das quatro
  folhas anexadas na rodada "HUD 4 pixel" (14/10/2026, commit `32e3823c`; aprovada como direção na rodada seguinte e
  levada ao jogo em `58c20d8d`). Os registros a chamam de folha anexada que **imita pixel art sem grade nativa exata**
  (o "pixel" mede de 6 a 9 px da imagem e varia de peça para peça) e não dizem com que ferramenta foi feita; o aspecto
  é o de uma imagem gerada. (Os quatro lugares da HUD 4 completa, da `assets4c/`, são outra folha e não estão no jogo.)
- **O processo que gerou os arquivos finais** (`preparar_hud4p.py`): o recorte de cada lugar por região conexa (a vila
  tem 265×203); a limpeza do alfa (só a franja de até 5% e os pontos soltos); a escala do grupo dos lugares pela área
  visível, sem folga; e a **redução "paleta"**: cada pixel de destino é a média do bloco da imagem, trocada pela cor
  mais próxima que o desenho tem, com o alfa duro. Nada foi redesenhado nem retocado; **não há fonte `.aseprite`, nem
  grade-base**.
- **Os tamanhos:** **cada um é uma redução própria do mesmo recorte, por fator não inteiro** (o 32 a ÷7,9 a ÷9,3; o 40
  a ÷6,4 a ÷7,4, conforme a peça). **O 40 não é desenho próprio, nem o 32 com margem, nem o 32 ampliado:** os dois
  enchem o quadrado (a vila: 32×25 dentro do 32 e 40×31 dentro do 40) e têm de 300 a 770 cores. O `@2x` de cada um
  também é outra redução (a 64 e a 80), não a duplicação exata.
- **O que isso quer dizer:** são os ícones aprovados da família, mas foram feitos antes da regra da skill de itens de
  que redução por fator não inteiro não vale como acabamento. Para o mapa, funcionam e leem bem; se o Jean quiser a
  família em grade nativa, seria um redesenho à mão (lugar por lugar, com a referência como mapa), uma entrega
  própria. Não comecei nada disso.

### 2. A cancela

A primeira (a faixa vermelha e branca) lembrava sinalização de trânsito; uma segunda, só com dois postes e duas
travessas, lia como um banco no minimapa (fica fora do repositório). **Agora: a barricada de madeira envelhecida**, os
dois postes de pontas cortadas e as **tábuas cruzadas em X**, em quatro tons de madeira acinzentada, sem pintura e sem
textura (13×11 no minimapa, 19×15 no mapa grande). O X é o que diz "fechado" de longe; no minimapa, a 1×, lê como
`|X|` sobre a estrada pontilhada.

### 3. A direção B e a composição

- **A plaqueta com a figura 16 da classe** (a aprovada, de `retratos.js`: o elmo do Guerreiro, o capuz do Mago, o
  capuz verde do Arqueiro), 1:1 no minimapa e a 2× no mapa grande (a moldura e a figura juntas, pixel a pixel).
  Conferida com as três classes (Vau: Guerreiro; Bosque: Mago; Capela: Arqueiro).
- **Onde ela vai:** acima do símbolo, com a ponta tocando a borda de cima dele; **sem espaço acima** (o lugar perto da
  borda de cima do mapa, como a Capela no minimapa), **ao lado**, com a ponta virada para o lugar (à esquerda; sem
  espaço à esquerda, espelhada à direita: a peça `posicao-plaqueta-lado`). Antes desta revisão, ela seria cortada pela
  borda.
- **O que ela não cobre:** o nome fica embaixo do símbolo; a missão e o contrato do lugar atual vão para o lado da
  plaqueta (com ela à direita, para o canto de cima à esquerda); o símbolo fica inteiro (a ponta encosta só na borda de
  cima). Conferido nas quatro situações, nos dois mapas.
- **O que ficou:** no mapa grande, a plaqueta a 2× (40×44) é maior que o ícone de 40 do lugar: o lugar continua
  reconhecível, mas ela domina; com o 48 (abaixo), a proporção melhora. No minimapa da Capela, o nome do lugar atual,
  empurrado para dentro da borda, encosta no quadrado tracejado do Bosque (já era assim no jogo; o encaixe dos nomes só
  evita outros nomes).
- **A alternativa A** ficou como estava; a seta **é cortada pela borda** no minimapa quando o lugar atual está perto da
  borda de cima (na Capela). Se o Jean voltar para A, ela precisa do mesmo recurso de ir para o lado.

### 4. A presença dos lugares no mapa grande: o 40 × um 48

O 48 sai **do mesmo recorte, pelo mesmo processo** (`auxiliares/lugares48.py`, só em `proposta/`): tão nítido quanto o
40 (alfa duro, só cores do desenho), mas é mais uma redução, não um desenho nativo. O botão continua com 40 px (o
clique igual); o tracejado de destino acompanha o símbolo. **Leitura:** com o 48, os lugares ganham peso diante do
terreno e da plaqueta, sem amolecer; o 40 fica um pouco tímido, sobretudo a vila (mais larga que alta). **Minha
recomendação: o 48 no mapa grande**, com uma condição: se o Jean decidir refazer a família em grade nativa (item 1), o
tamanho do mapa grande se decide junto com esse redesenho. O minimapa fica com o 32.

### 5. O estado fechado: de onde vem a condição real

- **A regra que existe:** `campanha.py` guarda, por região, os `fechados` pela **chave** do lugar
  (`"estrada_de_varn": "<o porquê>"`), e `montar_mundo` copia o texto para `loc["fechado"]` (vai no save). A viagem
  (`rpg/sistemas/navegacao.py`, `_viajar`) oferece o destino e, escolhido, diz o texto e não sai do lugar. O
  `mapa.descricao` troca a descrição por "saída, fechada por enquanto", e o `estado.py` tira o nível. **Nada depende do
  nome "Estrada de Varn".** O protótipo lê o fechado pela descrição (a tela não recebe o campo).
- **O outro bloqueio (só procedural):** a cidadela com menos de 3 Sigilos ("selada" na descrição; a viagem pergunta do
  perigo e depois diz que a muralha bloqueia).
- **O que não é bloqueio:** o lugar **só conhecido** (`visitado` falso; a viagem vai, "inexplorado"); o lugar **não
  vizinho** (`distancia` vazia; não aparece entre os destinos, nem é clicável); o **perigoso** (o nível; a viagem pede
  confirmação, não impede).
- **Para a integração:** um campo próprio por lugar no `estado.py`, tirado da mesma regra da viagem, por exemplo
  `"bloqueio": loc.get("fechado") or None` (e, enquanto o procedural existir, o texto da cidadela selada pelos
  Sigilos), de preferência por uma função só em `rpg/mapa.py` que a viagem e a tela consultem, sem mudar a ordem das
  perguntas da viagem. O mapa passa a ler `n.bloqueio` no lugar da descrição. Isso não muda partidas nem o gabarito.

## Como o mapa funciona (o que o levantamento conferiu no código)

- **O desenho é um só, `rpg/web/static/mapa.js` (`MapaPx.criar`)**, para o minimapa do painel do mundo
  (`app/paineis.js`, `desenharMundo`), o mapa grande (M ou o atalho Mapa; `desenharMapaGrande`) e o mapa na página
  (o sistema Mapa do motor, `app/escolhas.js`, `mapaNaPagina`). Os dados vêm de `rpg/web/estado.py`
  (`mapa_conhecido`): os lugares visitados e os vizinhos deles, com `tipo`, `bioma`, `visitado`, `atual`, `distancia`
  (só os vizinhos do lugar atual), `nivel`, `descricao` e `covil`; as estradas com `atual` (toca o lugar atual) e
  `percorrida` (as duas pontas visitadas).
- **O terreno** é pintado por pixel num canvas (as manchas do bioma, a névoa pontilhada, os enfeites), tingido pela
  hora; **as estradas** são linhas de Bresenham de 1 px com a sombra; **os símbolos** são os sprites 16×16 do jogo
  (`sprites-dados.js`), desenhados no canvas em 14 (minimapa) ou 16 (mapa grande). Por cima, em HTML, os botões dos
  lugares (28 e 40 px: a área de clique e a dica), o "!" das marcas e os nomes.
- **A escolha do desenho:** `MapaPx.sprite` (covil ativo → `covil`, vencido → `vencido`, vila → `vila`, senão o bioma).
  O tipo `saida` da campanha (a Estrada de Varn) cai no bioma (planície). A mesma escolha serve a lista de Caminhos
  (`Icones.lugar`, os ícones aprovados de 32 e 40), o Diário (a missão e os contratos, o sprite 16), as opções de
  viagem do menu (o sprite 16) e a legenda (os nove sprites 16).
- **Os tamanhos a 1920×945:** o minimapa é um canvas de 224×128 exibido em 284×162 (**×1,27**); o mapa grande, de
  352×201 exibido em 928×530 (**×2,64**). O símbolo fica com ~18 px no minimapa e ~42 no mapa grande; o "!" tem 11 px de
  letra no minimapa e 14 no grande. Não há zoom: `enquadrar` ajusta o quadro aos lugares conhecidos (com os cinco
  lugares do Vale, os dois mapas mostram o mesmo quadro).
- **Os estados que existem:** o lugar atual (o anel que cresce e some a cada 1,5 s, e o nome em ouro; no minimapa, só o
  nome do lugar atual aparece); o destino clicável (o tracejado de ouro pulsando); o destacado (o contorno, ao passar o
  mouse na lista de Caminhos ou no rastreador); o conhecido não visitado (60% de opacidade, a névoa no terreno, o nome
  apagado); o perigo (o nome em vermelho quando o nível é 2 ou mais acima do seu); as estradas daqui (ouro), percorrida
  (bege) e só conhecida (pontilhada escura); a marca "!" (missão ou contrato, a mesma); o covil ativo e o vencido (só no
  procedural). **Não existem:** a missão concluída no mapa (a marca some, a missão fica no Diário), o lugar bloqueado (a
  cidadela "selada" e a saída fechada só no texto da dica e da lista).

## O que se achou

**Defeitos de leitura**
1. **A posição do jogador** não tem marca permanente: o anel some, e na maior parte do tempo só o nome em ouro diz onde
   você está. No minimapa noturno no Bosque, o nome cai ao lado do quadrado do Vau (`levantamento.png`, seção 2).
2. **A escala fracionária** (×1,27 e ×2,64) faz pixels de larguras diferentes nas estradas, no pontilhado e nos
   símbolos.
3. **Os símbolos do minimapa** saem borrados (o 16 desenhado em 14 com suavização, depois ampliado); a Capela e a
   Estrada de Varn quase somem.
4. **As estradas** atravessam o símbolo; a só conhecida (Bosque → Capela) quase não aparece no escuro; **a saída
   fechada parece um destino aberto** (a estrada em ouro e o tracejado de "clique para viajar"; o clique leva ao aviso).
5. **Missão e contrato com a mesma marca**, um "!" de texto numa caixa de ouro presa ao canto do botão (não do desenho).

**Provisórios** (nunca passaram por aprovação): os nove sprites 16 do mapa (a família de antes da HUD), o traço das
estradas, o "!" em CSS, o anel e o tracejado. **Aprovados que já servem ao mapa:** os ícones de lugar da família da HUD
(`lugar-*-32/40`, da `assets4c`), hoje só na lista de Caminhos; o atalho Mapa da doca. O mapa e a lista mostram o mesmo
lugar com dois desenhos diferentes.

**Prioridade** (frequência × problema; o minimapa está sempre à vista): 1) a posição do jogador; 2) os caminhos (a
escala, os estados, a saída fechada); 3) os símbolos dos lugares; 4) as marcas de missão e contrato. **Depois**: o
Diário e as opções de viagem com o mesmo desenho do mapa, a legenda só com o que existe, a missão concluída e o perigo
também no símbolo, o nome do lugar atual no minimapa que encosta num vizinho.

**Dependências do procedural** (para o levantamento da retirada): o covil (ativo e vencido) e a cidadela só existem lá,
com a "selada" da descrição; a legenda lista os nove desenhos dos dois modos; `MapaPx.sprite` cai no bioma para a
`saida` da campanha; `GLIFO_TIPO`/`GLIFO_BIOMA` (`rpg/mapa.py`, a interface de texto) e o `covil` de `estado.py`. Ao
retirar o procedural, isso sai ou muda junto; a campanha precisa de um desenho e de um estado próprios para a saída (o
`fechado` existe no motor, `campanha.py`, mas não chega à tela como campo: o protótipo o reconhece pela descrição).

## Os cinco símbolos da campanha (23/10/2026): a vila e a floresta aprovadas, os três restantes em avaliação

**Aprovadas pelo Jean, sem retoques:** a vila e a floresta nativas da rodada anterior, **o 32 no minimapa e o 48 no mapa
grande**, do commit **`094bb80a`**. As fontes escolhidas: `fontes/lugar-vila-n32.aseprite`, `fontes/lugar-vila-n48.aseprite`,
`fontes/lugar-floresta-n32.aseprite` e `fontes/lugar-floresta-n48.aseprite` (as grades em `auxiliares/lugares.py`); os
PNGs em `proposta/` (MD5: vila-n32 `5fabc101…`, vila-n48 `483eea70…`, floresta-n32 `883b4290…`, floresta-n48
`fa053fa5…`), conferidos iguais depois desta rodada (as fontes não foram remontadas).

**Os três restantes** (`lugar-pantano-n32/n48`, `lugar-ruinas-n32/n48`, `lugar-planicie-n32/n48`), à mão, como a vila e
a floresta: a forma construída na grade de cada tamanho (o 48 escrito para a grade de 48, não o 32 esticado), cores
agrupadas por material, contorno de 1 px, a luz da esquerda; fontes em camadas pelo Aseprite em lote (pântano: água,
juncos, árvore e contorno; ruínas: pedra, musgo e contorno; planície: morros, campo e contorno), 0 diferentes na
releitura, o exportado igual à grade, o `@2x` por duplicação exata.

- **Os usos compartilhados, conferidos antes:** o pântano serve ao Charco dos Juncos e aos pântanos do procedural; as
  ruínas, à Capela Afogada e às ruínas do procedural; a planície, à Estrada de Varn (a saída da campanha, que cai no
  bioma) e às planícies do procedural. Por isso os três são de bioma, sem nada só de um lugar: nem a capela nem a
  água da Ilse nas ruínas, nem estrada ou placa na planície. **A barricada não entra no desenho da planície:** é a
  marca separada da saída fechada, desenhada pelo mapa só onde a regra bloqueia.
- **O pântano:** a poça de água (quatro azuis-esverdeados, os reflexos em cima), as taboas e os juncos à esquerda e à
  direita, a árvore seca no meio, torta, com dois galhos e gravetos. No 48, uma primeira passada com hastes demais lia
  como cerca; ficaram as taboas e os tufos.
- **As ruínas:** o arco quebrado à esquerda (o pilar inteiro e o começo da arcada), o pilar partido do meio, a parede
  alta à direita com a fresta de janela e as fiadas de pedra, o entulho e o musgo na base; a pedra clara de contorno
  escuro, legível no roxo escuro da Capela, de dia e à noite. No 48, o pilar do meio tinha saído pontudo (como um
  obelisco) e foi quebrado reto. **A minha ressalva:** o arco novo lê mais como pilares quebrados do que como arcada; a
  curva do antigo era mais evidente.
- **A planície/saída:** o morro do fundo mais escuro, o da frente, a faixa clara do campo aberto com pontos de flor e
  duas moitas; larga e baixa, como a antiga.
- **O nome do Bosque** (à noite, colado no quadrado do Vau): o encaixe dos nomes agora exige folga dos outros lugares
  (12 px do botão, que o tracejado passa em 2), e, entre as posições livres embaixo e em cima (deslizando para os lados
  enquanto o nome ainda cobre o próprio símbolo), escolhe a mais longe dos outros lugares, e, empatando, a mais
  centrada. Quando nada cabe com 12, tenta com 4 e com 0 antes do comportamento do jogo. Resultado: o nome do Bosque
  fica sob as próprias árvores, deslocado para longe do Vau, sem depender da plaqueta; a Capela continua com "nome ·
  plaqueta · ruínas" na mesma linha.
- **As fotos** (`capturas/cinco-antigo`, os ícones antigos, e `capturas/cinco-novo`, os cinco nativos; as duas com a
  plaqueta B, a cancela de madeira e o encaixe novo dos nomes): o Vau de manhã, o Bosque à noite, a Capela à tarde e
  depois da praça; os mesmos lugares, destinos, estados, botões e rótulos acessíveis do jogo; nenhum erro ou aviso no
  console. A folha **`cinco.png`**: os cinco juntos (32 e 48, a 1× e ampliados), o antigo × novo dos três novos com a
  grade e o tamanho exibido, o minimapa de manhã, à noite e à tarde, o mapa grande de dia e à noite com os recortes do
  Charco, da Capela e da Estrada de Varn, e o nome do Bosque antes e depois.
- **Para a integração** (do conjunto aprovado): os cinco por lugar no lugar dos ícones antigos no mapa e no minimapa,
  e o campo de bloqueio vindo da regra real da viagem (`loc["fechado"]`), não da descrição. Fora deste lote: os
  símbolos só do procedural (a montanha, a cidadela, o covil, o vencido).

## A vila e a floresta em grade nativa (23/10/2026; pedido do Jean; só as duas, para validar o acabamento)

**O pedido:** reconstruir os símbolos de lugar numa grade nativa, começando pela vila e pela floresta, com os ícones
antigos como referência de composição e identidade. A plaqueta B, a cancela de madeira, os caminhos e as marcas do
protótipo ficam como base (aprovados). Nada no jogo; os outros lugares continuam com os ícones antigos.

- **As peças** (`auxiliares/lugares.py`, fontes em `fontes/`, exportadas em `proposta/`):
  - `lugar-vila-n32` e `lugar-floresta-n32`: **grade 32×32, exibidas a 32** (no minimapa, 1:1);
  - `lugar-vila-n48` e `lugar-floresta-n48`: **grade 48×48, exibidas a 48** (no mapa grande, 1:1): uma adaptação à
    mão para a grade de 48, com a mesma composição do 32, não o 32 esticado;
  - o `@2x` de cada uma é a duplicação exata por vizinho mais próximo (conferida: blocos inteiros que voltam ao
    original), nunca outra redução da referência.
- **O que ficou de cada referência:** a vila, a casa grande de enxaimel com a empena à esquerda, o telhado vermelho
  indo para a direita, a chaminé, a casa pequena de telhado vermelho à direita, as janelas acesas e a porta; a
  floresta, três pinheiros de alturas diferentes, o do meio mais alto, os da frente sobrepostos.
- **Como foram feitas:** a floresta pelas linhas de cada camada de copa escritas à mão (a largura, a luz da esquerda,
  a faixa escura embaixo de cada camada), as árvores da frente por cima da do meio; a vila por uma construção à mão das
  formas (o telhado, a empena, as paredes, as vigas, as janelas, a porta), depois limpa na grade (a chaminé
  estreitada, o canto de vigas aliviado, as mãos-francesas tiradas, os contornos que faltavam, o caixilho da janela).
  No 48, a floresta precisou de uma segunda passada: a primeira saiu com árvores magras, separadas e troncos longos,
  longe do 32; ficaram mais juntas, com camadas mais largas e troncos curtos. Os desenhos centralizados na altura. As
  cores agrupadas por material (o telhado em quatro vermelhos, a parede em dois cremes, as copas em cinco verdes); o
  creme da vila baixado depois da foto noturna, onde destoava.
- **As fontes:** o Aseprite em lote (o conector continua sem o editor), camadas paredes, enxaimel, janelas, telhado,
  chaminé, plantas e contorno (vila) e troncos, copas, luz e contorno (floresta); 0 diferentes na releitura; a fonte
  reaberta com as camadas na ordem; o exportado igual à grade, alfa só 0 ou 255.
- **No minimapa** (`capturas/proposta-n32`, de dia no Vau e à noite no Bosque): as duas leem no tamanho real; a vila
  nova é mais limpa e mais clara que a antiga (a casa e o telhado se separam melhor à noite); a floresta nova tem as
  três árvores mais distintas. A antiga tinha mais detalhe de textura (telhas, sombras miúdas), que a nova não carrega.
- **No mapa grande:** o 32 nativo em 1:1 (`capturas/proposta-n32`) ficou pequeno diante do terreno e da plaqueta (a
  plaqueta a 2× é maior que a vila); uma caixa maior não aumentaria o desenho. **O 48 nativo**
  (`capturas/proposta-n48`) tem presença e equilibra a plaqueta. **Recomendação: o 32 no minimapa e o 48 no mapa
  grande.**
- **O nome perto das bordas:** o nome do lugar agora procura um lugar livre (embaixo, como antes; senão em cima, à
  esquerda, antes da plaqueta, ou à direita) sem invadir o símbolo, o botão, a plaqueta, as marcas ou o nome de outro
  lugar; sem nenhum livre, faz como o jogo. Na Capela atual do minimapa, ficam "nome · plaqueta · ruínas" na mesma
  linha, sem encostar no Bosque. Só o desenho muda; o botão (a área de clique) é o mesmo. Ainda: à noite no Bosque, o
  nome cabe embaixo das árvores, mas fica perto do quadrado do Vau (a plaqueta desfaz a dúvida).
- **Conferido:** nas rodadas `proposta-b` (a base com os ícones antigos e o encaixe novo dos nomes), `proposta-n32` e
  `proposta-n48`, os mesmos lugares, destinos clicáveis, estados, botões (28 e 40 px) e rótulos acessíveis do jogo, e
  nenhum erro ou aviso no console. A folha **`nativos.png`**: as peças antigas e novas a 1× e ampliadas (com a grade e
  o tamanho exibido de cada uma), as silhuetas, o minimapa de dia e à noite, o mapa grande com a plaqueta (40 antigo,
  32 e 48 novos) e o nome da Capela antes e depois.
- **Continua registrado:** o campo real de bloqueio para a integração; o reconhecimento da saída fechada pela
  descrição é só uma limitação do protótipo. As capturas de `proposta-b` foram refeitas com o encaixe novo dos nomes
  (as folhas anteriores ficam como estavam; o antes da Capela está em `capturas/sprites/`).

## O primeiro lote (a primeira rodada, como foi apresentada; a escolha e a revisão estão acima)

Quatro elementos, escolhidos pelos defeitos acima e pela frequência: **a posição, os caminhos, os símbolos dos
lugares e as marcas de missão e contrato**. Uma proposta principal por elemento; uma segunda direção só na posição.

1. **A escala inteira (a base de tudo):** o canvas na resolução do pixel do mapa, **×2 no minimapa (142×81 → 284×162)
   e ×3 no mapa grande (309×177 → 927×531)**: o mesmo espaço (o mapa grande fica com 1 px a menos de largura e 1 a
   mais de altura), pixels iguais, o pontilhado e as estradas limpas. Na integração, o lado do canvas sai da largura do
   painel (o protótipo já mede o contêiner).
2. **Os caminhos, como conjunto:** a estrada começa e acaba na borda do símbolo; **daqui** (ouro), **percorrida**
   (bege, contínua), **só conhecida** (tracejada, mais clara que hoje, visível no escuro) e **para a saída fechada**
   (pontilhada, apagada, com a **cancela** na ponta e o tracejado de destino em cinza, sem pulsar). O clique continua lá:
   viajar para a Estrada de Varn continua dando o aviso de que está fechada.
3. **Os símbolos dos lugares:** os **ícones aprovados da família** (`lugar-*`), os mesmos da lista de Caminhos, **1:1**:
   o **40 no mapa grande** e o **32 no minimapa**, posicionados em pixel inteiro, com a mesma opacidade de "conhecido
   não visitado". **Nenhum desenho novo:** pela skill de itens, testei antes o reaproveitamento da arte aprovada em
   tamanho nativo; o 32 coube no minimapa e lê melhor que o 16 borrado, então não fiz o 24 previsto. O covil vira a
   caverna da família (a mesma da lista); o vencido, sem ícone na família, fica o sprite do jogo (só procedural).
4. **As marcas, desenhadas à mão** (`auxiliares/grade.py`, montadas no Aseprite em lote), uma para cada mapa:
   - **missão**: a plaqueta de ouro com o "!" (11×14; 9×11 no minimapa);
   - **contrato**: o cartaz do mural, o papel com o lacre vermelho e as linhas (11×14; 9×11);
   - presas ao canto do **símbolo**, a missão primeiro e o contrato ao lado quando os dois caem no mesmo lugar.
5. **O "você está aqui", permanente** (o anel que some sai):
   - **direção A, a seta** de ouro apontando para o lugar, com um balanço de 2 px (19×17; 13×12 no minimapa);
   - **direção B, o herói na plaqueta**: a figura 16 aprovada da classe (`retratos.js`) numa moldura de ouro com a ponta
     (20×22; no mapa grande a 2×, a moldura e a figura juntas). As marcas do lugar atual vão para o lado da plaqueta.
   - A escolha visual relevante: **A** é um sinal neutro, pequeno, que não disputa com o símbolo; **B** diz *quem* está
     ali e liga o mapa ao herói, mas é maior e esconde mais terreno. A minha recomendação é **A**: o minimapa é pequeno
     e o símbolo do lugar é que precisa aparecer; a seta resolve a dúvida sem pôr outro retrato na tela.
6. **A legenda** do mapa grande: só o que o mapa conhecido mostra (os ícones da família em 32) e as marcas (a seta, a
   missão, o contrato, a saída fechada), no lugar dos nove sprites dos dois modos.

**O que melhorou:** o lugar atual se acha na hora, nos dois mapas e à noite; os símbolos são os da lista (o mesmo lugar,
o mesmo desenho) e leem no minimapa; as estradas não cortam os desenhos; a saída fechada não parece aberta; missão e
contrato se distinguem. **Limitações:** no mapa grande, o ícone de 40 tem margens próprias e o lugar parece um pouco
menor que o sprite antigo esticado a ~42 px; as marcas novas são pixel art 1:1 sobre ícones pintados (a mesma convivência
dos estados sobre os retratos); a "!" da missão lembra o ícone da Iniciativa da luta (contextos diferentes); no
minimapa noturno, o nome do lugar atual ainda encosta no quadrado do vizinho (a seta desfaz a dúvida); o Diário, as
opções de viagem e o "!" do texto do Diário (`MARCA_MAPA`) continuam com o desenho de hoje.

**Conferido:** em todas as situações, nas duas direções, os mesmos lugares, os mesmos destinos clicáveis, os mesmos
estados (`atual`, `clicavel`, `tem-contrato`; a proposta só acrescenta `fechado`), os mesmos botões (28 e 40 px) e os
mesmos rótulos acessíveis do jogo; nenhum erro ou aviso no console; o procedural continua funcionando com a proposta
(`procedural-covil`). As peças: a fonte reaberta com as camadas na ordem (corpo, marca, contorno), 0 diferentes na
releitura, o exportado igual à grade, alfa só 0 ou 255, o @2x em blocos inteiros que voltam ao original.

## Como refazer

    python auxiliares/grade.py ..                 # as grades e as listas das peças
    python auxiliares/exportar.py --montar        # as fontes (Aseprite em lote) e proposta/*.png, conferidas
    # as fotos (PLAYWRIGHT_BROWSERS_PATH e PLAYWRIGHT_MODULO como na fumaça):
    node auxiliares/fotografar.mjs <raiz> capturas/atual
    python auxiliares/lugares.py ..               # a vila e a floresta nativas (grades e listas); depois exportar.py --montar
    python auxiliares/lugares48.py                # o 48 dos lugares (o mesmo processo do 32 e do 40), só em proposta/
    PROTOTIPO=1 node auxiliares/fotografar.mjs <raiz> capturas/proposta-b              # B, a escolhida (POS=b é o padrão)
    PROTOTIPO=1 GRANDE=48 node auxiliares/fotografar.mjs <raiz> capturas/proposta-b48 vau-manha,bosque-noite,capela-tarde,praca-tudo
    PROTOTIPO=1 POS=a node auxiliares/fotografar.mjs <raiz> capturas/proposta-a vau-manha,bosque-noite,capela-tarde,praca-tudo
    python auxiliares/folhas.py                   # levantamento, pecas, comparacao, origem-lugares, presenca-lugares

O protótipo (`prototipo/mapa.js`) é uma cópia do `mapa.js` da 1.199.3 com a proposta, servida no lugar do do jogo só na
página das fotos (`page.route`); a legenda da proposta entra por `MapaPx.legenda`. O jogo não lê nada daqui.

**O Aseprite:** o conector desta sessão não subiu (ninguém escutava a porta 6515; o editor aberto, com um documento do
Jean, respondia "editor not connected"). Não toquei na janela nem encerrei processos: as fontes saíram pelo caminho em
lote documentado (`auxiliares/montar.lua`, o `montar_camadas.lua` para peças w×h, com o `pintar.lua`).

## Para a integração (só do que o Jean aprovar)

O `mapa.js` da proposta mostra o caminho; a integração faria: o `fechado` como campo em `estado.py`; as peças em
`hud/icones/` (pelo `exportar_aseprite.py`, com as fontes em `ferramentas/arte/aseprite/`), registradas em `Icones`; o
CSS em `05-paineis.css`; a legenda nova em `app/paineis.js`; e, numa entrega à parte, o Diário, as opções de viagem e o
`MARCA_MAPA` com o mesmo desenho.
