# Os 14 estados restantes (lote da madrugada, 21/10/2026)

Pedido de Jean: uma proposta por estado para os 14 estados que ainda usam os sprites do jogo, em sete lotes, **só no
protótipo**. Nada daqui está aprovado nem integrado; o jogo não lê nada desta pasta. Firme (R2), Em guarda (G1) e
Esquiva (E6), já no jogo, são a referência de acabamento e não foram redesenhados.

## Como foi feito

- **Tamanho:** 16 px de arte e o @2x pela duplicação exata. É o tamanho do chip da carta e do selo do estado que chega
  (`.ef img.sprite { --s: 16 }`, ~18 px de tela a 1920×945 pelo zoom da HUD). Nenhum outro tamanho.
- **Desenho:** as grades à mão em `auxiliares/icones16.py` (uma letra por pixel; a paleta no topo do arquivo; o
  contorno de 1 px pelos lados, escrito à mão ou pelo `com_contorno`). As grades de um lote ainda não entregue, no mesmo
  arquivo, são rascunhos até o commit daquele lote. `auxiliares/previa.py` é a bancada (o 1× em
  chips escuros ao lado dos três finais, o 2× e a 12×).
- **Aseprite:** o conector do MCP (`aseprite-bridge`) **não conectou nesta sessão** ("Connection closed", conferido no
  começo; não foi reinstalado nem reconfigurado). As fontes saíram pelo caminho já registrado da linha de comando
  (`ferramentas/arte/montar_fontes.py`: o `montar_camadas.lua` com o `pintar.lua`, que relê cada pixel gravado), pelo
  `auxiliares/montar.py`:
  1. `icones16.py` grava `grades/<id>.txt` e `listas/<id>/<camada>.lua` (com `ordem.txt`);
  2. o Aseprite (`-b`) monta `fontes/<id>/<id>-16.aseprite`, uma camada por parte, o contorno por cima;
  3. o Aseprite exporta `proposta/<id>-16.png` (o composto das camadas visíveis); o @2x pelo Pillow (vizinho mais
     próximo);
  4. a conferência: 16×16 RGBA, fundo transparente, nenhum pixel parcial, o 1× igual pixel a pixel à grade, o @2x igual
     ao 1× ampliado.
  Operações: o desenho (as grades) é à mão; montar, pintar e exportar são do Aseprite pela linha de comando; o @2x, as
  folhas e as fotos são cálculos fora do editor.
- **Fotos:** `auxiliares/fotografar.mjs` (derivado de `flechas_firme/auxiliares/fotografar_luta.mjs`) sobe os cenários
  dos testes de navegador (`covil` com `EFEITOS`/`EFEITOS_INIMIGO`; `tutorial` para o servo do Necromante) a 1920×945,
  com as situações de cada lote em `auxiliares/situacoes.json` (cada estado onde ele de fato aparece: no herói, no
  inimigo ou no aliado). Na proposta, **só a página** troca a imagem do chip daquele estado
  (`.ef[data-ef="<id>"] img.sprite`); os sprites do jogo e os outros papéis deles ficam intactos. O selo de chegada
  (`.faixa-acao.selos`) não tem seletor por estado e não foi trocado nas fotos.
- **Folhas:** `auxiliares/prancha.py lote <n>` → `lote<n>.png` (a fileira da carta com os três finais, atual ×
  proposta, 1× e 2×; as tentativas guardadas; a 12× com a grade; as cartas na luta, atual × proposta, 1× e 2×);
  `prancha.py geral` → `geral.png` (os 17 identificados e os estados de dano lado a lado).

## As regras conferidas no código (`rpg/estados.py`, `rpg/inimigos.py`, `rpg/habilidades.py`, `rpg/talentos.py`)

| Estado | O que faz de fato | Onde aparece |
|---|---|---|
| Veneno (`veneno`) | dano por turno; não pega em mortos-vivos nem construtos | no herói (aranha, rato, lagarto, afixo "venenoso") e no inimigo (Flecha Envenenada) |
| Sangramento (`sangramento`) | dano por turno; não pega em construtos nem etéreos | no herói (Mordida Sangrenta de lobos e ratos) e no inimigo (Sede de Sangue, o lobo do Patrulheiro) |
| Chamas (`queimadura`) | dano por turno, acumula camadas ("em chamas ×N"); a chuva enfraquece; a Combustão detona o que falta arder | no herói (Bola de Fogo de cultistas e demônios) e no inimigo (Bola de Fogo, Inferno) |
| Maldição (`maldito`) | dano por turno e −40% de defesa | no herói (a maldição de cultistas, afogados, chefes) e no inimigo (Drenar Vida e a Maldição do Necromante) |
| Atordoado (`atordoado`; o rótulo "congelado" é o mesmo estado) | perde o próximo turno e não se esquiva; depois fica Firme por um turno; chefes e gigantes podem resistir | no inimigo (Golpe Pesado, Lança de Gelo, Combustão) e no herói (teia, imobilizar, congelar) |
| Enfraquecido (`enfraquecido`) | causa −25% de dano | no inimigo (Grito de Guerra) e no herói (Grito de Terror, ataques de alguns inimigos) |
| Marcado (`marcado`) | recebe +v% de dano de todos os golpes (os seus, os da comitiva e os do animal) | no inimigo (Marcar Presa, Tiro Certeiro) |
| Furtivo (`furtivo`) | o próximo ataque é crítico garantido e o estado se gasta; os inimigos continuam mirando você | no herói (Desaparecer, que também dá Esquiva por 1 turno) |
| Barreira (`barreira`) | absorve v de dano e se gasta ("absorve mais N de dano") | no herói (Barreira, do Mago) |
| Provocando (`provocando`) | os inimigos atacam quem está assim | no aliado: o esqueleto do Erguer Servo e o urso da Ordem da Fera (com Em guarda) |
| Fortalecido (`fortalecido`) | dano causado +v% enquanto dura (Grito de Guerra +30% por 3 turnos; o uivo dos lobos; outros) | no herói e no inimigo |
| Fúria (`furia`) | dano causado +v% enquanto dura; soma com o Fortalecido (cada fonte multiplica o golpe) | no herói (Fúria Cega e o talento do Berserker) |
| Frenesi (`frenesi`) | cada abate soma uma carga (até 3) e o dano cresce até o fim da luta (99 turnos, "∞" no chip) | no herói (o talento Frenesi do Berserker) |
| Iniciativa (`iniciativa`) | o primeiro golpe deste turno sai +v% mais forte e gasta o estado; usado para outra coisa, o turno passa e o estado vai junto | no herói, no turno livre de quem pegou o inimigo de surpresa |

## Lote 1: Veneno e Sangramento

- **Veneno — a serpente** (`estado-veneno`): uma cobra verde em S, a cabeça no alto voltada para a esquerda, o olho
  escuro e a língua bifurcada vermelha; camadas corpo, olho, lingua, contorno. Silhueta sem gota: não depende do verde
  para se separar do Sangramento.
- **Sangramento — as gotas de sangue** (`estado-sangramento`): a gota grande à direita (junto do número do chip) e uma
  gota pequena atrás, no alto, à esquerda; camadas gotas, contorno.
- **Tentativa guardada:** `estado-veneno-presas` (as duas presas pingando veneno). Recusada na bancada: na carta, em
  tamanho real, lia como "!!" (colidiria com a exclamação da Iniciativa). Antes dela, as bolhas sobre uma poça (liam
  como uma barra e bolas) e as presas presas a uma gengiva (liam como "π") não chegaram a fonte.
- **Correção vista na carta:** a primeira versão do Sangramento tinha a gota pequena embaixo, à direita; colada no
  número, lia como ponto decimal ("2.2"). A gota pequena passou para o alto, à esquerda.
- **Fotos:** o herói contra ratos (envenenado e sangrando, os dois do rato) e os lobos envenenados pelo Arqueiro.
  Sem erro nem aviso no console. Folha: `lote1.png`.
- **Avaliação sincera:** a serpente é a leitura mais forte do lote (lê como cobra no 1×); o Sangramento continua na
  família da gota do jogo, agora com duas gotas: claro, mas pouco novo.

## Lote 2: Chamas e Maldição

- **Chamas — as três línguas de fogo** (`estado-queimadura`): a língua do meio mais alta, duas menores dos lados, o
  miolo claro embaixo e a borda vermelha; camadas chamas, miolo, contorno. Continua sendo fogo (o estado é fogo), mas
  aberto em línguas separadas, em vez da bola de fogo do sprite `chama` (que fica no Vigor, no Poder e na Pena de
  Fênix).
- **Maldição — a caveira roxa** (`estado-maldito`): o crânio de osso tingido de roxo, as órbitas escuras com um ponto
  magenta aceso e os dentes; camadas cranio, olhos, contorno. Não é uma chama recolorida: outra silhueta (crânio) e
  outra cor.
- **Na bancada:** a primeira caveira tinha dois fios de fumaça em cima e lia como um inseto de antenas; a fumaça saiu e
  as órbitas cresceram (3×3, com o ponto aceso).
- **Fotos:** o herói contra cultistas (em chamas e amaldiçoado, os dois do cultista) e os lobos em chamas pelo Mago. Sem
  erro nem aviso no console. Folha: `lote2.png`.
- **Avaliação sincera:** a caveira é inconfundível em tamanho real; o risco é a leitura de "morte" mais que de
  "maldição" (a cor roxa e os olhos acesos ajudam). As Chamas leem como fogo de imediato, mas ficaram próximas do sprite
  atual: a mudança é de acabamento, não de conceito. A queda de 40% de defesa da Maldição não aparece no ícone (a dica
  diz).

## Lote 3: Atordoado e Enfraquecido

- **Atordoado — a espiral** (`estado-atordoado`): a espiral dourada de tontura, duas voltas e meia; camadas espiral,
  contorno. Vale para o congelado (o mesmo estado, só outro rótulo): não foi criado outro estado nem outro ícone.
- **Enfraquecido — a espada com a seta para baixo** (`estado-enfraquecido`): a espada de ferro apontada para baixo e uma
  seta roxa grande descendo ao lado ("ataque ↓"); camadas espada, seta, contorno. É o par oposto do Fortalecido (a
  espada para cima com a seta dourada subindo, lote 6): a direção e a cor separam os dois.
- **Tentativas guardadas:** `estado-atordoado-orbita` (a órbita com duas estrelinhas, a linguagem das estrelas que o jogo
  anima sobre o retrato do atordoado; na carta lia como um anel com uma joia, pior que a espiral);
  `estado-enfraquecido-partida` (a espada partida, a ponta caída; em tamanho real lia como "†,");
  `estado-enfraquecido-setinhas` (a espada com dois triângulos pequenos; encostados no número liam como ":").
- **Fotos:** os lobos atordoados e enfraquecidos pelo Guerreiro e o herói enfraquecido. O herói atordoado **não tem
  foto parada válida**: o estado se gasta no começo do turno dele, antes de o jogador poder agir (só aparece durante o
  turno dos inimigos). Sem erro nem aviso no console. Folha: `lote3.png`.
- **Avaliação sincera:** o Enfraquecido ficou claro e conversa com o Fortalecido. A espiral lê como tontura, mas também
  pode ler como "@"; é o ponto frágil do lote. A órbita fica guardada caso o Jean prefira as estrelas que o jogo já usa.

## Lote 4: Marcado e Furtivo

- **Marcado — o alvo** (`estado-marcado`): o alvo de anéis vermelho e creme com o centro aceso; camadas aneis, contorno.
  "Este é o alvo": recebe mais dano de todos.
- **Furtivo — o capuz** (`estado-furtivo`): o capuz escuro de frente, o rosto em sombra e dois olhos claros; camadas
  capuz, rosto, olhos, contorno. Fala da furtividade (o Desaparecer); o crítico garantido fica na dica.
- **Tentativa guardada:** `estado-marcado-mira` (a mira com os quatro traços e o ponto; em tamanho real parecia a face
  "5" de um dado num círculo escuro).
- **Fotos:** os lobos marcados pelo Arqueiro e o herói furtivo. A Esquiva do Desaparecer dura 1 turno e já se gastou
  quando o jogador pode agir; por isso a foto mostra o Furtivo sozinho (a Esquiva final aparece na fileira da folha).
  Sem erro nem aviso no console. Folha: `lote4.png`.
- **Avaliação sincera:** o alvo é o mais legível do conjunto até aqui. O capuz lê como figura encapuzada, mas é escuro
  sobre o chip escuro: funciona pela silhueta e pelos olhos, não pelo contraste.

## Lote 5: Barreira e Provocando

- **Barreira — a figura dentro da bolha** (`estado-barreira`): o anel azul de energia, claro em cima e à esquerda, com
  uma figura de ferro (cabeça e ombros) dentro; camadas bolha, figura, contorno. "Alguém protegido por uma bolha", sem
  escudo: se separa do Em guarda (o escudo de ferro) pelo formato e pelo material.
- **Provocando — os golpes vindo para a figura** (`estado-provocando`): a figura de ferro (cabeça e ombros) e três setas
  vermelhas descendo sobre ela, da esquerda, do alto e da direita; camadas figura, setas, contorno. "Os inimigos atacam
  ele".
- **Tentativas guardadas:** `estado-barreira-anel` (a bolha vazia com o reflexo; na carta lia como "O" junto do número,
  "O2"); `estado-barreira-cheia` (a esfera preenchida; lia como uma bola ou uma joia azul); `estado-provocando-lados`
  (as setas apontando dos lados para a figura; em tamanho real pareciam uma gravata-borboleta). Antes delas, na
  bancada: a cúpula (lia como gelatina), o hexágono (porca ou gema), o peão com as setas (lápide) e as setas em X sem
  ponta (lia como explosão).
- **Fotos:** o Mago com a Barreira e o esqueleto do Necromante provocando (o cenário `tutorial`, nível 4, Necromante; a
  foto usa o Erguer Servo pela roda e pelo seletor, como o jogador; os lobos ainda chegam fortalecidos pelo uivo). Sem
  erro nem aviso no console. Folha: `lote5.png`.
- **Avaliação sincera:** os dois são os mais frágeis da noite. A Barreira lê como "pessoa na bolha", mas lembra o ícone
  de "conta de usuário" (a figura num círculo). O Provocando é o mais fraco: a ideia (os golpes vindo para ele) aparece
  a 2×; no 1× as setas viram um borrão vermelho sobre a figura. Os dois repetem a mesma figura de cabeça e ombros, o
  que os aproxima. Se o Jean recusar, a próxima tentativa do Provocando seria de outra construção (o grito, ou a mão
  chamando), não um retoque desta.

## Lote 6: Fortalecido e Iniciativa

- **Fortalecido — a espada com a seta para cima** (`estado-fortalecido`): a espada de ferro em pé e uma seta dourada
  grande subindo ao lado ("ataque ↑"); camadas espada, seta, contorno. O par do Enfraquecido (lote 3): a mesma espada,
  a direção e a cor da seta invertidas.
- **Iniciativa — a exclamação** (`estado-iniciativa`), como o Jean sugeriu: a barra dourada de largura constante, o
  ponto bem separado e dois raios curtos de cada lado ("pegou de surpresa"); camadas exclamacao, raios, contorno.
- **Alternativa pedida pelo Jean:** `estado-iniciativa-bota`, a bota da Agilidade (a bota de couro em passada,
  `attr-agilidade-24.png`) reduzida à mão para 16 px, com o rastro. Está na foto da carta (o modo `proposta-bota`).
  Fica perto do sprite atual da Iniciativa e é o mesmo desenho da Agilidade e do Fugir: lê "rapidez", não "primeiro
  golpe mais forte".
- **Tentativas guardadas:** `estado-iniciativa-taca` (a exclamação larga em cima e fina embaixo; em tamanho real lia
  como uma taça dourada); `estado-fortalecido-setinhas` (a espada com dois triângulos pequenos; encostados no número
  liam como ":", o mesmo defeito do Enfraquecido).
- **Fotos:** o Guerreiro fortalecido pelo Grito de Guerra (com os lobos enfraquecidos, ainda com o sprite atual do
  Enfraquecido, que não é deste lote) e o Arqueiro com a Iniciativa; atual × proposta × a bota. Sem erro nem aviso no
  console. Folha: `lote6.png`.
- **Avaliação sincera:** a exclamação é clara e se distingue de tudo; o raio dos lados é o "legal" pedido, sem virar
  ruído. O Fortalecido é explícito ("ataque ↑"), mas é o mais "de interface" do conjunto (seta), menos pintado que os
  finais.

## Lote 7: Fúria e Frenesi

- **Fúria — o rosto vermelho de raiva** (`estado-furia`): o rosto redondo vermelho, as sobrancelhas em V, os olhos
  acesos em amarelo e a boca fechada para baixo (o "😡" conhecido); camadas rosto, sobrancelhas, olhos, contorno.
- **Frenesi — as três garras crescentes** (`estado-frenesi`): três rasgos vermelhos inclinados, cada um maior que o
  anterior; camadas garras, contorno. O tamanho que cresce fala do dano que cresce a cada abate.
- **Comparados com o Fortalecido e a Iniciativa** (lote 6): a espada com a seta (ferro e ouro), o rosto (vermelho e
  redondo), as garras (traços vermelhos abertos) e a exclamação (barra fina dourada) têm silhuetas diferentes; a Fúria e
  o Frenesi dividem o vermelho, mas não a forma. A foto do Berserker com os três ao mesmo tempo (Fortalecido + Fúria +
  Frenesi, uma combinação real) está na folha.
- **Tentativa guardada:** `estado-furia-escuro` (o mesmo rosto em vermelho quase preto, com olhos laranja; em tamanho
  real lia como uma bola escura com olhos, as sobrancelhas sumiam). Antes, na bancada: só os olhos e as sobrancelhas
  (liam como bigode).
- **Fotos:** o Berserker com Fortalecido, Fúria e Frenesi e o herói só com a Fúria. Sem erro nem aviso no console.
  Folha: `lote7.png`.
- **Avaliação sincera:** a Fúria é direta, mas é um emoji: o mais "moderno" da família, menos dentro do mundo que o
  capuz ou a serpente. As garras do Frenesi leem como "rasgos" e o crescimento aparece a 2×; no 1× o que fica é "três
  traços vermelhos", o que ainda as separa do resto.

## A prancha geral e a avaliação do conjunto

`geral.png`: os 17 estados identificados (os três finais do jogo e os 14 candidatos), em chips no tamanho real, a 2× e
a 4×; a fileira inteira lado a lado; e os estados de dano juntos (Fortalecido, Fúria, Frenesi, Iniciativa e o
Enfraquecido), o grupo que mais podia confundir.

**Conferência técnica (tudo passou):** os 26 desenhos (14 principais e 12 tentativas) reabertos do `.aseprite` pela
linha de comando saem idênticos à proposta e à grade; o @2x é exato; 16×16 RGBA, alfa só 0 ou 255, fundo
transparente; os scripts passam no `pyflakes` e no `node --check`; as 14 fotos de situação, sem erro nem aviso no
console. O jogo não mudou (`rpg/` e `tests/` intactos; a troca das fotos é só na página).

**Qualidade visual (a minha leitura em tamanho real, na carta, a 1920×945; quem aprova é o Jean):**

- *Funcionam melhor:* Marcado (o alvo), Veneno (a serpente), Maldição (a caveira roxa), Iniciativa (a exclamação),
  Furtivo (o capuz), Sangramento (as duas gotas). Leem no 1× sem precisar do nome e não se confundem com os vizinhos.
- *Funcionam, com ressalva:* Fortalecido e Enfraquecido (claros, "ataque ↑/↓", mas são símbolos de interface, menos
  pintados que os finais); Chamas (lê como fogo, mas mudou pouco em relação ao sprite atual); Fúria (direta, mas é um
  emoji, o mais moderno da família); Frenesi (três rasgos vermelhos; o crescimento só se vê a 2×); Atordoado (a espiral
  lê como tontura, mas pode ler como "@").
- *Frágeis:* Provocando (as setas sobre a figura viram um borrão vermelho no 1×) e Barreira (lê como pessoa na bolha,
  mas lembra o ícone de conta de usuário); os dois ainda repetem a mesma figura. São os primeiros a pedir outra
  construção se o Jean recusar (Provocando: o grito ou a mão chamando; Barreira: a cúpula ou uma parede de energia,
  já tentadas na bancada sem sucesso).
- *Riscos de confusão que ficaram resolvidos:* nenhum elemento pequeno encostado no número do chip (a gota pequena, os
  triângulos e as presas liam como pontuação e foram trocados); Fúria e Frenesi dividem o vermelho, não a forma;
  Fortalecido e Enfraquecido são o mesmo desenho de propósito, com a direção e a cor invertidas.
- *Limites das fotos:* o selo de chegada não foi trocado (não tem seletor por estado); o herói atordoado e a Esquiva de
  1 turno do Desaparecer não têm foto parada válida (se gastam antes de o jogador agir).

## A integração dos cinco aprovados (1.158.0)

**Decisão de Jean (21/10/2026):** Sangramento, Maldição, Marcado, Furtivo e Fúria, nas versões da prancha geral do
`b17ab3dd`, aprovados e integrados sem retoques. As fontes destes cinco (`fontes/estado-<id>/`) foram copiadas sem
mudança para `ferramentas/arte/aseprite/estado-<id>/`; os PNGs do jogo saem do `exportar_aseprite.py` idênticos, byte a
byte, aos de `proposta/`. O papel é `ESTADO` em `rpg/web/static/icones.js` (o chip da carta e o selo do estado que
chega); os sprites do jogo ficam nos outros papéis.

**Conferido no jogo** com os arquivos de produção e os saves temporários dos cenários, a 1920×945
(`auxiliares/fotografar.mjs` com `MODOS=atual` e as situações `integracao` de `situacoes.json`; as fotos e o registro
em `capturas/integracao-1.158.0/`): os chips nas mesmas situações dos lotes, e os selos de chegada pela roda e pelo
seletor de habilidades, como o jogador faz (o roteiro ganhou `selo`, `carta` e `SO`): Sede de Sangue (Sangramento ▼ no
bandido), a Maldição do Necromante (▼), Desaparecer (Furtivo ▲, com a Esquiva) e Fúria Cega (▲). **O Marcado não tem
selo de chegada no jogo:** as duas fontes dele (o Marcar Presa e o evento da estrada) aplicam o estado direto, sem
lance; o papel cobre o selo se um dia houver. O registro confirma que o Veneno, as Chamas, o Frenesi e o Fortalecido
continuam com os sprites. Sem erro nem aviso no console. A folha: `integracao-1.158.0.png`.

## A segunda rodada dos nove (21/10/2026, depois da avaliação do Jean)

**Pedido de Jean:** os cinco aprovados entram no jogo (seção acima); os outros nove são refinados aqui, com as versões
anteriores preservadas. Os candidatos do `b17ab3dd` continuam em `proposta/estado-<id>-16.png`; as alternativas novas
ficam em `proposta/estado-<id>-r2-16.png` (e `estado-veneno-gota-16.png`), com as fontes em `fontes/` e as grades em
`icones16.py` (a seção "a segunda rodada"). As folhas `rodada2-lote<n>.png` mostram, na carta a 1920×945 e com os
mesmos dados: o sprite do jogo (atual), o candidato anterior (proposta) e a alternativa nova (proposta-r2 /
proposta-gota), em tamanho real e a 2×, e a 12× com a grade.

**O que foi pedido por estado e o que foi feito (grupo 1: lotes 1, 2 e 3):**

- **Veneno — a gota verde como alternativa** (`estado-veneno-gota`): uma gota única, pontuda, caindo numa poça larga,
  com dois respingos e um reflexo; camadas poca, gota, contorno. A construção se separa do Sangramento (duas gotas
  soltas, sem chão) pela poça e pela gota única, além da cor. Na bancada, a primeira gota pendurada por um fio lia como
  um frasco (o fio virava gargalo) e foi trocada. **Comparação:** a serpente (o candidato preservado) lê como cobra no
  1× e não se parece com nada; a gota com a poça lê como "gota verde", mas no 1× também pode parecer uma arvorezinha num
  vaso. **Recomendação: a serpente.**
- **Chamas — a chama dominante** (`estado-queimadura-r2`): a silhueta primeiro, uma chama alta com a ponta inclinada e
  duas línguas menores na base, acompanhando o mesmo movimento; depois o miolo claro embaixo e a borda escura. A leitura
  de coroa (três pontas da mesma altura) sumiu.
- **Atordoado — a espiral preservada, e o teste opcional de rotação** (`rodada2-atordoado-gira.png`): só na página do
  protótipo, o selo de chegada do Atordoado ganha a espiral e gira uma volta em quatro passos de 90° (0,6 s, sem
  rotação fracionada, que borraria o pixel), dentro de `@media (prefers-reduced-motion: no-preference)`; o chip fica
  parado. Conferido no cenário `gelo` (a Prisão de Gelo pela roda): o registro mostra a imagem a 90°, a 270° e parada
  ao fim da volta; com `prefers-reduced-motion: reduce`, nenhuma animação. A mudança no jogo seria pequena (uma classe
  no selo do estado e a regra de CSS), mas pede decisão: não foi aplicada.
- **Enfraquecido — a guarda equilibrada** (`estado-enfraquecido-r2`): a guarda da espada passa a ter 3 px de cada lado
  da lâmina (antes, 3 de um lado e 2 do outro); a seta roxa para baixo e o resto, iguais. Coerente com o Fortalecido
  (lote 6).
- **Fotos:** as mesmas situações dos lotes 1, 2 e 3 (`capturas/rodada2-lote<n>/`), atual × candidato × alternativa; o
  Sangramento e a Maldição, agora no jogo, aparecem com os arquivos de produção. Sem erro nem aviso no console. Folhas:
  `rodada2-lote1.png`, `rodada2-lote2.png`, `rodada2-lote3.png`.

**Grupo 2: lotes 5, 6 e 7.**

- **Barreira — a figura de corpo inteiro dentro da bolha** (`estado-barreira-r2`): a mesma bolha azul, agora com o
  interior preenchido de azul escuro (a esfera) e uma figura clara de cabeça, tronco e pernas (o ferro claro), com
  espaço em volta; o reflexo saiu de perto da figura. Deixa de ser o busto de "conta de usuário". No 1×, porém, lê mais
  como "orbe azul" do que como "figura protegida": a figura só aparece com clareza a 2×.
- **Provocando — a figura e as setas separadas** (`estado-provocando-r2`): a figura de corpo inteiro com os braços
  abertos e três setas vermelhas finas, com pontas próprias, vindo da esquerda, do alto e da direita na direção da
  cabeça, com um vão entre as pontas e o corpo; o corpo fica inteiro à vista, sem a mancha vermelha.
- **Fortalecido — a seta verde e a guarda equilibrada** (`estado-fortalecido-r2`): a seta subindo em verde claro (o
  verde do veneno, com o contorno escuro; contraste bom no chip escuro e na borda dourada) e a guarda com 3 px de cada
  lado. A leitura "ataque ↑" continua.
- **Iniciativa — o golpe que sai primeiro** (`estado-iniciativa-r2`), com a exclamação preservada: a espada em
  estocada na diagonal, os riscos de velocidade atrás e um brilho dourado na ponta (o golpe rápido que acerta forte).
  Se separa do Fortalecido (espada em pé com a seta) pelo movimento.
- **Frenesi — as divisas que crescem** (`estado-frenesi-r2`), com as garras preservadas: três divisas empilhadas, a de
  baixo pequena e vermelho-escura, a do alto larga e amarela (a intensidade subindo a cada abate). A diferença aparece
  no 1×: "três degraus subindo", não "três traços".
- **Fotos:** as mesmas situações dos lotes 5, 6 e 7 (`capturas/rodada2-lote<n>/`), atual × candidato × alternativa; a
  Fúria, agora no jogo, aparece com o arquivo de produção. Sem erro nem aviso no console. Folhas: `rodada2-lote5.png`,
  `rodada2-lote6.png`, `rodada2-lote7.png`.

**A prancha geral** (`geral.png`, atualizada): os oito integrados (Firme, Em guarda, Esquiva e os cinco da 1.158.0),
os nove em avaliação com o sprite atual, o candidato preservado e a alternativa nova lado a lado, a fileira inteira e os
estados de dano juntos (Fortalecido, Fúria, Frenesi, Iniciativa e Enfraquecido, candidato e nova).

**Avaliação da segunda rodada (a minha leitura em tamanho real; quem aprova é o Jean):**

- *Melhoraram de verdade:* Chamas (a chama única), Fortalecido e Enfraquecido (equilibrados; a seta verde lê melhor que
  a dourada sobre a borda dourada), Provocando (as setas e o corpo separados), Frenesi (as divisas leem "crescer" no 1×,
  o que as garras não faziam).
- *Alternativas sem ganho claro:* Veneno (a gota com a poça é clara, mas a serpente é mais forte; recomendo a
  serpente); Iniciativa (o golpe rápido diz "primeiro golpe" melhor que a exclamação, mas no 1× é uma espadinha na
  diagonal; a exclamação continua mais legível, e diz "surpresa").
- *Continua frágil:* Barreira (a figura saiu do "avatar", mas no 1× o que se lê é uma esfera azul).
- *Atordoado:* a espiral parada fica; o giro do selo funciona e respeita o movimento reduzido, e é uma decisão de
  interface para o Jean (a mudança no jogo seria pequena).

## A integração da 1.159.0: Chamas, Fortalecido, Enfraquecido e Frenesi

**Decisão de Jean (21/10/2026):** as Chamas R2, o Fortalecido R2 e o Enfraquecido R2 da segunda rodada, e o Frenesi das
três garras da primeira (`b17ab3dd`), sem retoques. As fontes (`fontes/estado-queimadura-r2/`,
`estado-fortalecido-r2/`, `estado-enfraquecido-r2/` e `estado-frenesi/`) foram copiadas sem mudança, com o nome do
estado, para `ferramentas/arte/aseprite/estado-<id>/`; o exportador grava os PNGs idênticos, byte a byte, aos de
`proposta/`. Conferido no jogo a 1920×945 (`MODOS=atual`, as situações `integracao-1.159.0`; as fotos em
`capturas/integracao-1.159.0/`): os chips no herói, nos lobos e no Berserker, e os selos de chegada da Bola de Fogo
(Chamas ▼) e do Grito de Guerra (Enfraquecido ▼ nos inimigos). **O Fortalecido e o Frenesi não têm selo de chegada no
jogo:** o Grito de Guerra usa a animação do grito, que dispensa o selo, e o uivo, o grito dos inimigos e o talento
Frenesi aplicam o estado direto. O Atordoado continua com o sprite. Sem erro nem aviso no console. Folha:
`integracao-1.159.0.png`.

## A terceira rodada: Veneno, Iniciativa, Atordoado e Barreira (21/10/2026)

**Pedido de Jean:** a gota verde do Veneno sem a poça; três exclamações para a Iniciativa (a espada em movimento não foi
escolhida); três conceitos estáticos novos para o Atordoado (a espiral não foi aprovada); três Barreiras sem pessoa
dentro. Provocando preservado, sem mudança. Nada destes autorizado para integração.

**Processo:** as grades em `icones16.py` (a seção "a terceira rodada"); as fontes montadas **no editor pelo MCP**
(`auxiliares/montar_mcp.py` gera o roteiro: o documento com as camadas, o `pintar.lua` com a releitura de cada pixel,
salvar o `.aseprite` e fechar), todas com "0 diferentes na releitura"; a exportação e a conferência pela linha de
comando (`montar.py --so-exportar`: o 1× igual à grade, @2x exato, alfa 0/255). O conector continuou de pé depois das
exportações em lote (`get_version` respondeu logo depois de cada leva). As folhas por estado (`rodada3-<estado>.png`,
`prancha.py rodada3 <estado>`): cada opção identificada, em chips junto dos 12 estados do jogo, a 12×, e a carta na
luta a 1920×945 com os mesmos dados em cada opção.

- **Veneno — a gota sem a poça** (`estado-veneno-gota2`): a gota da rodada 2 sem a poça e os respingos, centrada no
  quadro; a borda de baixo já fechava redonda (5 px na última linha) e não precisou de acabamento. Sozinha no chip, lê
  como gota verde, mas fica muito perto do sprite que já está no jogo (a mesma silhueta de gota com um reflexo): perdeu
  justamente o que a separava do Sangramento além da cor. A serpente continua preservada e **continua a minha
  recomendação**.
- **Iniciativa — três exclamações** (a exclamação com raios preservada):
  A, `estado-iniciativa-cunha`: a barra larga dourada de 4 px, com bisel claro à esquerda, a ponta curta e o ponto
  quadrado separado; a mais limpa e com mais peso.
  B, `estado-iniciativa-estouro`: a exclamação escura sobre um estouro creme e laranja, de bordas em ponta (o alerta
  dos quadrinhos); a de mais presença no chip.
  C, `estado-iniciativa-italico`: a exclamação inclinada para a frente com dois riscos de velocidade atrás; no 1× vira
  um "=/" e é a mais fraca.
  Nenhuma encosta no número com algo que pareça pontuação. Na bancada, a primeira cunha (larga em cima, fina embaixo)
  voltou a lembrar uma taça e foi refeita.
- **Atordoado — três conceitos novos** (a espiral preservada, não aprovada):
  A, `estado-atordoado-estrelas`: três estrelinhas douradas em arco, a mesma linguagem das estrelas que o jogo já anima
  sobre o retrato de quem está atordoado; lê bem, mas também pode ler como "avaliação de três estrelas".
  B, `estado-atordoado-ampulheta`: a ampulheta de madeira com a areia parada ("perde o turno"); clara e distinta de
  todos os outros estados, e diz a regra, não a sensação.
  C, `estado-atordoado-elmo`: o elmo de ferro com a viseira, uma rachadura clara e a faísca do golpe; no 1× lembra uma
  bomba cinza com pavio, é a mais fraca.
  Recusado na bancada: a corrente fechada (o par do Firme), que lia como óculos (a grade `ATORDOADO_CORRENTE` fica em
  `icones16.py`, sem fonte).
- **Barreira — três construções sem pessoa** (a figura na bolha preservada):
  A, `estado-barreira-cupula`: a cúpula oca de energia sobre o chão, a borda clara à esquerda e escura à direita, com
  um reflexo por dentro; lê como cúpula, às vezes como tampa.
  B, `estado-barreira-parede`: a parede de luz vertical parando uma flecha que chega da esquerda (a absorção); a mais
  clara sobre o que o estado faz, e bem distinta do escudo do Em guarda.
  C, `estado-barreira-impacto`: a película circular com o golpe estourando na borda esquerda e a rachadura entrando
  (absorve até romper); a primeira versão, com o impacto no alto à direita, lia como uma bomba com pavio e foi mudada;
  ainda é a mais frágil.
  Tentativa guardada: `estado-barreira-campo` (o cilindro de energia com as colunas de luz), que lia como uma gaiola
  ("preso", o Atordoado). Recusada na bancada antes da fonte: a colmeia de hexágonos (lia como cristais).
- **Fotos:** o herói contra ratos e os lobos envenenados (Veneno), o Arqueiro com a Iniciativa, os lobos atordoados e
  enfraquecidos (Atordoado) e o Mago com a Barreira, sozinha e ao lado do Em guarda; o atual, as opções preservadas e as
  novas, com os mesmos dados. Sem erro nem aviso no console.

**A prancha geral** (`geral.png`, atualizada): os 12 integrados; as alternativas não escolhidas dos estados já
integrados (as Chamas e o Fortalecido/Enfraquecido do `b17ab3dd`, as setinhas, a espada partida, as divisas do
Frenesi, a mira do Marcado); as propostas em avaliação (Veneno, Iniciativa, Atordoado, Barreira e Provocando, cada um
com o sprite atual, as opções preservadas e as novas); e a fileira dos 12 integrados com cada nova opção no fim.

**Minha avaliação desta rodada:** Iniciativa A ou B (a barra larga é a mais limpa; o estouro, a de mais presença);
Atordoado B (a ampulheta) é o conceito mais claro e mais distinto, com o A (as estrelas) logo atrás; Barreira B (a
parede parando a flecha) é a que melhor diz "absorve dano". Veneno: a serpente, não a gota. Frágeis: Iniciativa C,
Atordoado C e Barreira C.

## A integração da 1.160.0: Veneno, Atordoado e Barreira

**Decisão de Jean (21/10/2026):** a gota verde sem a poça (`estado-veneno-gota2`), as três estrelinhas
(`estado-atordoado-estrelas`, estática) e o golpe na película (`estado-barreira-impacto`), sem retoques. As fontes
foram copiadas sem mudança, com o nome do estado, para `ferramentas/arte/aseprite/estado-<id>/`; o exportador grava os
PNGs idênticos, byte a byte, aos de `proposta/`. Atenção aos nomes: no protótipo, `proposta/estado-veneno-16.png`
continua sendo a serpente, e `estado-atordoado-16.png` e `estado-barreira-16.png` continuam sendo a espiral e a figura
na bolha (candidatos antigos); no jogo, os arquivos com esses nomes são os aprovados. Conferido no jogo a 1920×945
(`MODOS=atual`, as situações `integracao-1.160.0`; as fotos em `capturas/integracao-1.160.0/`): os chips no herói e nos
lobos, a Barreira sozinha e ao lado do Em guarda, e os selos de chegada da Flecha Envenenada (Veneno ▼), da Prisão de
Gelo (Atordoado ▼, o congelado) e da Barreira Arcana (▲). Sem erro nem aviso no console. A cúpula e a parede da
Barreira ficam como alternativas não escolhidas. Folha: `integracao-1.160.0.png`.

## Provocando: o acabamento do busto do `b17ab3dd` (proposta)

**Pedido de Jean (21/10/2026):** retomar o candidato da primeira rodada (o busto com as três setas vermelhas
convergindo) e ajustar só o acabamento da figura: mais branca e legível no fundo escuro, sem os planos cinza de boneco
modelado, com sombras contidas para separar a cabeça dos ombros, e as setas distintas. Sem a figura de braços abertos
da rodada 2, sem outra pose e sem anatomia.

**Feito** (`estado-provocando-claro`): cada pixel no mesmo lugar do original (a mesma silhueta e o mesmo contorno; as
setas idênticas: nenhum pixel mudou fora da figura, conferido na comparação dos PNGs); a figura passa de quatro cinzas
(e4e8ec, b0b6bd, 848b94, 646a73, o volume modelado) para dois tons: o branco (f2f4f6) em toda a figura e uma sombra
contida (b4bcc6) só no pescoço, que separa a cabeça dos ombros, e na beira direita, do lado oposto à luz. Camadas
figura, setas, contorno. A fonte foi montada no editor pelo MCP (`montar_mcp.py`, 0 diferentes na releitura) e
exportada com a conferência (`montar.py --so-exportar`); o conector continuou de pé. A folha `rodada3-provocando.png`:
o sprite atual, o original e o ajuste, junto dos 15 estados do jogo, a 12× e na carta do esqueleto do Necromante a
1920×945 com os mesmos dados. Sem erro nem aviso no console.

**Leitura:** a figura passa a ler como uma silhueta clara e inteira contra o chip escuro, sem o aspecto de peça cinza
modelada; as setas vermelhas continuam à parte. O que não muda (de propósito, por ser a composição aprovada para
retomar): as setas ainda formam um grupo vermelho denso no alto, e a figura em busto continua parecida com a da
Barreira de antes (que saiu do jogo nesta mesma rodada; a Barreira integrada não tem figura).
