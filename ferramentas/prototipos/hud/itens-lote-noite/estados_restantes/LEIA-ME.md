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
