# 32 — Etapa 8: estudo de direção de arte do campo livre (mais sério, sombrio e brutal)

**01/11/2026 (data do computador local).** Estudo e amostra jogável, **nada aprovado**: duas direções próximas e viáveis
para o mesmo trecho, comparáveis no protótipo (Campo Livre 7, `ferramentas/prototipos/etapa8-campo/`), sem mudar
regras. A arte atual continua lá como terceira opção. O que foi feito no comportamento (navegação, alvos, investida,
controles, provocações) está na rodada 7 do [30](30-ETAPA8-CAMPO-LIVRE.md).

| Seção | O que tem |
|---|---|
| 1 | O pedido e o que ficou fixo |
| 2 | Referências: o que cada uma ensina, custo e limites |
| 3 | As duas direções na amostra |
| 4 | A escala: a atual e o herói menor |
| 5 | Sombrio sem perder leitura |
| 6 | A carnificina |
| 7 | Fontes e fluxo de arte |
| 8 | A perspectiva no resto do jogo (estudo, não conversão) |
| 9 | Hipóteses, limitações e o que avaliar |

## 1. O pedido e o que ficou fixo

O Jean gosta do minimalismo atual e do estilo das casas e quer estudar uma evolução para uma fantasia mais sombria:
construções bonitas, terreno mais convincente, personagens com identidade. **Fixos por decisão dele:** a perspectiva
atual (de cima, com os corpos e as construções em três quartos; nada de isometria), a escala miniatura (sem aumentar os
sprites; o herói do tamanho atual ou menor), o detalhe extra concentrado em cenário e efeitos, as mesmas regras nas duas
versões e a apresentação anterior acessível. Não refazer o catálogo antes da escolha.

## 2. Referências

Lidas nesta sessão (o conteúdo da página) ou só vistas no resultado da busca (marcado). Nenhum asset de outro jogo foi
usado; as referências orientam método, não desenho.

| Referência | O que ensina | Custo de produção | Limite da adaptação |
|---|---|---|---|
| Slynyrd, *Pixelblog 3, Graphical Projection* ([página](https://www.slynyrd.com/blog/2018/3/14/pixelblog-3-graphical-projections-1)), lida | a projeção de cima em três quartos: a fachada encurtada, o telhado no ângulo de frente; **a uniformidade da projeção vale mais que o realismo**; a luz de um canto de cima, pintar em formas sólidas pela luz, com a paleta planejada antes | baixo: é regra, não asset | o post não ensina a construir prédios passo a passo; a nossa já é essa projeção (a construção sobe para o norte) |
| Slynyrd, *Pixelblog 20, Top Down Tiles* ([página](https://www.slynyrd.com/blog/2019/8/27/pixelblog-20-top-down-tiles)), lida | o chão em quadros de 16 × 16; misturar áreas lisas com textura de densidade variada; grupos que cruzam a borda para esconder a grade; formas repetidas que não se encostam de lado; espelhar quadros; poucas cores e pouco contraste dentro da textura; espaço vazio entre duas texturas cheias | baixo: um quadro desenhado à mão serve o campo inteiro | o nosso campo é contínuo (960 × 560), não um tilemap: a textura é carimbada espelhada por cima de manchas grandes |
| Slynyrd, *Pixelblog 44, Top Down Trees* ([página](https://www.slynyrd.com/blog/2023/5/22/pixelblog-44-top-down-trees)), lida | a copa por feixes de folhas repetidos, cada um sombreado como esfera (o crescente escuro de um lado, o claro do outro), em camadas pela luz; 4 ou 5 cores por feixe; o tronco cilíndrico com a casca listrada; a sombra pelo lado da luz | médio: um feixe bom vira muitas árvores | usamos 6 feixes por copa e a luz do noroeste (a mesma das construções), não a do artigo |
| Slynyrd, *Pixelblog 22, Top Down Character Sprites* ([página](https://www.slynyrd.com/blog/2019/10/21/pixelblog-22-top-down-character-sprites)), lida | o tamanho pelo quadro (1 × 2); 4 direções bastam, o lado se espelha; a caminhada de 4 quadros reaproveitada da corrida; cabeça grande para ler a expressão; o boneco nu com a roupa por cima, reaproveitado entre personagens | médio por personagem | as nossas miniaturas têm 13 a 15 px (menos que 1 × 2 de 16): só o lado, espelhado, e as pernas trocadas como passada |
| Slynyrd, *Pixelblog 47, Tiny Pixels* ([página](https://www.slynyrd.com/blog/2023/11/26/pixelblog-47-tiny-pixels)), lida | no muito pequeno, **só o necessário para a leitura**: a silhueta e um traço de identidade (ombreiras, o cabelo) bastam, o resto a imaginação completa; mover 1 pixel por quadro já é passada; 1 ou 2 px mudam a postura | baixo | é exatamente a nossa escala; confirma ganhar identidade por silhueta, paleta e arma, não por tamanho |
| *The Last Blog #18* (The Last Spell, Ishtar Games; [página](https://lastspell.com/?p=1401)), lida | um jogo de hordas contra uma vila, sombrio e em pixel: as influências declaradas são Into the Breach para a **leitura**, Stoneshard pelos sprites e Darkest Dungeon pelo clima; o diretor de arte pinta o conceito e depois faz a versão em pixel de cada peça | alto (equipe de arte) | a perspectiva deles é isométrica, que o Jean não quer; serve o princípio: o clima vem do conceito e da paleta, a leitura é critério à parte |
| Songs of Conquest, entrevistas de Carl Toftfelt e Niklas Borglund (Lavapotion) na [Game Rant](https://gamerant.com/songs-of-conquest-interview-carl-toftfelt-history-early-access-development/) e na [Game Rant](https://gamerant.com/songs-of-conquest-interview-coffee-stain-publishing-pixel-art-adventure-strategy/), **só o resumo da busca** | o pixel de alta resolução foi "uma quantidade absurda de trabalho"; pixel art não economiza tempo; depois de feito, é difícil refazer; parte dos jogadores reclama da leitura dos objetos e personagens ([GamePressure](https://www.gamepressure.com/songs-of-conquest/can-the-pixel-art-style-be-turned-off/za1142b)) | — | o aviso de custo e de leitura: mais detalhe por miniatura é caro e pode ler pior; por isso o detalhe novo foi para o cenário e os efeitos |
| Justin Ma (Into the Breach) à Rock, Paper, Shotgun, citado pela [Game Developer](https://gamedeveloper.com/design/-i-into-the-breach-i-dev-on-ui-design-sacrifice-cool-ideas-for-the-sake-of-clarity-every-time-), **só o resumo da busca** | "sacrificaríamos ideias legais pela clareza, sempre" | — | o critério de desempate: um efeito ou um detalhe que esconde ameaça sai |
| Stoneshard: a [prévia da PC Gamer](https://pcgamer.com/stoneshard-is-an-ambitious-turn-based-medieval-roguelike-with-brutal-injuries) (ferimentos brutais) e a atualização de arte ([GameBanshee](https://gamebanshee.com/k448y)), **só o resumo da busca** | a fantasia medieval sombria em pixel, com ferimentos e sangue como parte do mundo | — | não vimos o sistema de sangue deles; a nossa carnificina saiu das regras abaixo |
| Lospec, paletas com a etiqueta *darkfantasy* e *medieval* ([lista](https://lospec.com/palette-list/tag/medieval)), **só o resumo da busca** | uma paleta medieval de meios-tons com os claros contidos e os escuros saturados ("sombras coloridas") | baixo | não adotamos uma paleta pronta: as duas paletas do estudo saíram da atual, para comparar sem trocar de identidade |
| Decalques persistentes: [realtimevfx](https://realtimevfx.com/t/blood-decals-that-stay-in-the-world/29179) e o blog da [Deepwave](https://deepwavegame.github.io/news/advanced-decal-systems-bloody-footprints), **só o resumo da busca** | o sangue que fica se carimba numa camada (render target) que persiste; muitos detalhes iguais se juntam numa chamada só; marcas por cima umas das outras se fundem | baixo no nosso caso | o protótipo já tinha a camada de marcas do chão (`E.marcas`): cada gota é carimbada uma vez, ao pousar |

**O que as referências decidiram:** (1) identidade das miniaturas por silhueta, paleta, arma e poucas poses (Slynyrd 47 e
22), não por tamanho; (2) o detalhe novo no cenário (texturas de 16 × 16, blocos, telhas, copas em feixes) e nos efeitos,
com a luz de um canto só para tudo (Slynyrd 3, 20, 44); (3) clima pela paleta e pela luz, leitura como critério separado,
conferido com muitos soldados (The Last Spell, Into the Breach); (4) cuidado com o custo de detalhar cada unidade
(Songs of Conquest).

## 3. As duas direções na amostra

**A amostra:** o encontro "O portão da povoação" (`?enc=amostra`), um trecho de povoação fortificada que cabe numa tela a
1920 × 1080: a muralha de norte a sul com o portão entre duas torres e a estrada passando por ele, uma casa e o muro de um
quintal do lado de dentro, sete árvores e o campo aberto do lado de fora (os acessos: o portão e as duas pontas da
muralha). Você, Morel e Odette; Harg no portão; infantaria, arqueiros, cavalaria e pesados dos dois lados. Jogável, com
reforço aos 40 s. As árvores são obstáculo de verdade (o tronco barra a passagem; a copa não barra flechas), o mesmo em
todas as aparências.

**Como comparar:** `F8` troca a aparência (atual, sóbria, sombria), `F9` a escala do seu herói, `V` a violência, no meio da
luta, no mesmo quadro e no tamanho real (as regras e a batalha não mudam: só a imagem). Também nas opções da escolha e da
pausa, e por endereço (`?arte=sombria&escala=menor&violencia=3`). Todas as batalhas aceitam qualquer aparência: a vila a
2× serve para conferir muitos soldados.

| | Sóbria (a evolução do minimalismo) | Sombria (mais detalhe, mais escura) |
|---|---|---|
| Miniaturas | as grades atuais, a paleta menos saturada, os materiais separados (aço frio, couro, tecido), as equipes azul-aço e ferrugem | grades redesenhadas para soldado, arqueiro, pesado, cavaleiro e Harg: elmo de aba, malha nos braços, o tabardo da equipe por cima, capuz de couro no arqueiro, o escudo grande da equipe com borda de ferro no pesado, a xairel no cavalo, os chifres e o manto de pele de Harg; paleta escura com o contraste guardado nas cabeças, nas armas e nas bordas. Os heróis e quem não está na amostra usam as grades atuais com esta paleta |
| Chão | o verde-oliva acinzentado com a textura de 16 × 16 espelhada, manchas suaves, tufos, pedras e poucas flores | o verde-escuro com manchas de terra e lama, capim seco, sem flores |
| Estradas | terra batida com a beira pontilhada e dois sulcos de roda | lama com sulcos e poças (o reflexo claro no alto da poça) |
| Construções | reboco claro e madeira, telha de barro em fileiras com a cumeeira clara e o lado direito na sombra; pedra em blocos com as juntas desencontradas, ameias | reboco escurecido com enxaimel (as escoras em diagonal), telhado de lousa com musgo, chaminé, a janela acesa; pedra escura com musgo na base, o estandarte do inimigo nas torres, tochas acesas |
| Árvores | copas em feixes, verde médio, tronco listrado, sombra no chão | copas escuras, um galho seco |
| Luz | a do noroeste, nas faces e nas sombras do chão (sudeste) | a mesma, mais o brilho quente das tochas e da janela, somado ao chão com uma oscilação lenta |
| Quem está atrás | nas duas, a construção fica inteira e quem está atrás dela (ou debaixo de uma copa) aparece em **silhueta** por cima (azul os nossos, vermelho os inimigos, clara o herói), em vez de a construção ficar translúcida | |

## 4. A escala

**A atual:** o herói tem 15 px de altura e 17 de largura (o soldado, 13 e 13). **A alternativa, "Seu herói menor":** o
Guerreiro e o Mago redesenhados à mão com 1 linha de tronco e 2 colunas a menos (14 × 15), nas mesmas poses; Morel,
Odette e Harg ficam como estão (a robustez deles é silhueta: as ombreiras de Morel, a roupa e o cajado de Odette, os
chifres e o machado de Harg). O herói continua achável pelo contorno escuro, pela cor mais clara do campo, pelo anel
dourado no chão e pela seta dourada em cima. **A comparação** é no mesmo quadro (`F9` troca sem mexer na câmera nem no
zoom), em movimento. Não foi feita uma terceira escala: nada ficou maior.

## 5. Sombrio sem perder leitura

O que foi feito, além de escurecer a paleta (nenhum filtro sobre tudo): o terreno e a vegetação menos saturados que as
miniaturas; pedra, madeira, reboco e lousa com valores e texturas diferentes; uma luz só (noroeste) para as faces, as copas
e as sombras; as ameaças e os avisos com as cores saturadas de sempre (o vermelho dos avisos, o laranja do fogo, o roxo
do Grilhão), que contra o chão escuro se destacam mais, não menos; os números de dano e a HUD inalterados; as tochas como
a única luz quente. **Conferido** com a vila a 2× (cerca de 100 combatentes) e a amostra: as equipes se separam pela cor
do tabardo, os avisos e os números continuam por cima de tudo, as silhuetas mostram quem está atrás das casas e da
muralha sem deixar o cenário translúcido o tempo todo. **A avaliação de que lê bem é do Jean.**

## 6. A carnificina

Só tela (nada muda a luta), na camada de marcas do chão, embaixo dos vivos e dos avisos:
- **sangue direcional:** cada golpe forte e cada morte borrifa gotas na direção do golpe; cada gota mancha o chão onde
  cai;
- **manchas persistentes:** a poça embaixo de cada corpo; as gotas que pousaram ficam;
- **rastros curtos de arrasto:** o corpo que desliza depois de cair deixa um traço;
- **corpos arremessados:** os de antes (escurecidos e dessaturados no chão, para não parecerem alguém de pé);
- **armas e peças caídas:** a espada, a lança, o arco, às vezes o elmo voam e ficam no chão;
- **queimaduras:** as explosões de fogo (a Bola, os meteoros, as magias dos magos e a Coluna de Ardis) e as rachaduras dos
  saltos;
- **desmembramento estilizado:** na morte por golpe forte (o corpo arremessado), às vezes a cabeça ou um braço, 2 a 4 px,
  com o rastro de sangue; nunca em toda morte.

**A violência é ajustável** (`V`, opções, `?violencia=`): Desligada (sem sangue; corpos, armas e queimaduras ficam),
Contida, Normal (o padrão: sangue nos golpes fortes e nas mortes; pedaços em 30% das mortes por golpe forte) e Intensa
(também os golpes fracos respingam; pedaços em 60%). **Desempenho:** a vila a 2× com a sombria e a violência intensa,
14 s com o jogador automático: 57 qps nas duas janelas, simulação 1,7 ms (p95 3,4 a 3,8), desenho 4,2 a 4,3 ms (p95 16:
os primeiros quadros de cada aparência, quando as imagens são feitas e guardadas). As partículas batem no teto de 900 na
intensa (as mais antigas saem antes).

## 7. Fontes e fluxo de arte

- **As miniaturas:** à mão, uma letra por pixel, em `tela/sprites7.js` (as grades da sombria e as do herói menor) e
  `tela/sprites.js` (as atuais, que a sóbria usa com a paleta nova). As grades são a autoridade (o protótipo as lê).
- **As fontes em Aseprite:** `arte/fontes/<direção>/<unidade>.aseprite` (22 arquivos: as nove unidades da amostra nas
  duas direções e o herói menor), uma camada por equipe e um quadro por pose com a etiqueta (parado, andarA, andarB,
  preparo, golpe, recuo), montadas em lote pelo `arte/montar.mjs` (o Aseprite em linha de comando, sem tocar na janela
  aberta). Retocar no editor é possível; para o protótipo ver o retoque, ele volta para a grade.
- **O cenário:** `tela/arte7.js`: as texturas e os motivos (a textura do chão de 16 × 16, os blocos, as telhas, a
  enxaimel, os feixes das copas) desenhados em grade e repetidos no tamanho de cada construção, um kit modular, como nos
  Pixelblogs 20, 21 e 44. **Ainda não tem fonte em Aseprite:** fica para depois da escolha da direção.
- **As skills de arte:** a `arte-personagens-fenda` ganhou uma seção curta sobre miniaturas de campo (o que este estudo
  mostrou e o que ainda é hipótese). O fluxo completo da `arte-cenas-fenda` (levantamento, referência de composição
  aprovada, desenho na grade, fonte final) não foi seguido até o fim: isto é um estudo de direção, não uma candidata.
- **Imagens geradas:** não foram usadas. Uma geração não resolveria a consistência entre poses, direções e equipes, que é
  a maior parte do trabalho de uma miniatura; ela entraria, se o Jean quiser, como referência de composição para o
  cenário, transposta à mão.

## 8. A perspectiva no resto do jogo (estudo, não conversão)

O Jean considera este ângulo para o resto do jogo, sem aprovar a conversão. Duas possibilidades:

**A. A vila e os lugares nesta perspectiva, com interação por pontos clicáveis.** Cada lugar vira um mapa desta vista (o
chão, as construções, as árvores do kit), sem rolagem ou com pouca; os pontos de interação (a forja, a taverna, o templo,
a saída) são as próprias construções e figuras, com o rótulo que o jogo já usa; clicar leva o herói (a miniatura) até a
porta pelo grafo dos cantos e abre a cena do lugar. **Reaproveita:** o kit de cenário deste estudo, as miniaturas, a
navegação. **Os interiores** continuam nas cenas aprovadas (a forja, a curandeira, a taverna), na câmera delas: a vista de
fora é só a entrada. **Câmera:** fixa por lugar, enquadrada como a amostra. **Custo:** um mapa por lugar e as figuras
paradas de quem trabalha ali; diálogos, campanha e cenas não mudam.

**B. Exploração com movimento livre.** O herói anda com `WASD` pelos lugares, como na luta; colisão e caminho são os do
campo; os NPCs têm rotinas e o caminho deles; a câmera segue o herói. **Reaproveita** o mesmo motor de movimento e o kit.
**Diferenças:** cada lugar precisa de bordas, adereços e motivo para andar (o desenho de nível); os interiores viram mapas
desta vista (ou continuam como cenas, com uma transição na porta); as interações passam a ser por proximidade; o ritmo da
campanha (tempo de deslocamento), o salvamento (a posição) e os testes de jogo mudam. **Custo:** muito maior que o A, em
arte e em sistemas.

**Recomendação:** se a conversão for aprovada, começar pelo A (um lugar, a vila, como piloto), que testa a vista sem
mexer na estrutura das cenas, dos diálogos e da campanha; o B só se a exploração livre virar objetivo de jogo.

## 9. Hipóteses, limitações e o que avaliar

**Hipóteses (nada aprovado):** as duas direções; a escala menor; a silhueta atrás das construções no lugar da
transparência; o desmembramento e a quantidade de sangue do Normal; a luz das tochas.

**Limitações:** só as unidades da amostra têm grade sombria (os heróis, Morel, Odette e quem não está na amostra usam as
grades atuais com a paleta); o cenário não tem fonte em Aseprite; as poses são as do catálogo atual (sem quadros novos de
ataque); a luz é estática (a oscilação é só de brilho); a sombra das construções é um retângulo; as peças caídas não
reagem a nada depois de pousar.

**Para o Jean avaliar, jogando a amostra e a vila:** (1) qual direção segue (ou o que levar de uma para a outra)? (2) com
muitos soldados e efeitos, acha as ameaças sem esforço nas duas? (3) o herói menor ainda se acha, e vale a pena? (4) a
silhueta atrás das casas resolve melhor que a transparência? (5) a quantidade de sangue e os pedaços no Normal combinam
com a escala, ou o padrão deve ser o Contido? (6) a perspectiva no resto do jogo: o A, o B ou nenhum por enquanto?
