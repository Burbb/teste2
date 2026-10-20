---
name: arte-luvas-fenda
description: Construir, revisar ou avaliar luvas e manoplas em pixel art em The Unquiet (Crônicas da Fenda), da manopla básica do equipamento a luvas de couro, de tecido, de malha, de placas, reais ou de fim de jogo. Use junto da arte-itens-fenda sempre que o objeto for uma luva, uma manopla ou outro equipamento das mãos, para partir da base canônica da mão (a M5, adaptada da glove_04 da Dungeon Crawl Stone Soup, CC0), preservar a pose, os dedos, o polegar e as proporções, e mudar só o material e o acabamento. Não serve para anéis, braceletes soltos, armas nem o punho cerrado dos ícones de atributo.
---

# Luvas em pixel art

A manopla passou por muitas tentativas até a aprovada (a M5, `53d28893`): três rodadas desenhadas por medidas num
script (`c5fd33b`, `89be986`, `9509530`), uma à mão no Aseprite, um lote de seis construções independentes e duas
adaptações do Idylwild's Armory. Quase todos os erros foram de
**anatomia** (os dedos, o polegar, a palma, a proporção entre a mão e o punho), e não de material. O que resolveu foi
**adaptar uma luva pronta e bem desenhada**, trocando o material sobre uma cópia, em vez de reconstruir a mão a partir de
uma referência. Esta skill reúne isso.

**Como usar com a skill geral:** ela complementa a `arte-itens-fenda`, que continua valendo inteira: antes de desenhar,
a política de tamanhos, o fluxo do Aseprite pelo MCP, conferir, entregar. Aqui fica só o que é próprio de luva. Ela não
aprova nada: termina numa proposta com fotos, e o Jean decide.

**O que é regra e o que é exemplo:** a regra é **partir da mão da base canônica** e preservá-la. A malha, a paleta de
ferro e a tira de couro da M5 são **escolhas desta luva**, não obrigações: outra luva pode ser de couro, de placas, de
tecido bordado, dourada ou com uma gema. O detalhe da M5 e das tentativas recusadas está em [exemplos.md](exemplos.md).

## A base canônica: a mão da M5

- **A origem:** `ferramentas/arte/externas/cc0_hand_wear_icons/original/glove-dcss/32x32/glove/glove_04.png` (a B5 da
  escolha de base). Arte dos **artistas do Dungeon Crawl Stone Soup** (esforço coletivo; mantenedor Chris Hamons; a lista
  de artistas no pacote original), do pacote "Dungeon Crawl 32x32 tiles" (https://opengameart.org/node/12210), **CC0**,
  desenhada em 32 (nativa), reunida na coleção "CC0 Hand Wear Icons" montada por AntumDeluge
  (https://opengameart.org/content/cc0-hand-wear-icons). O registro completo da origem e da licença está em
  `ferramentas/arte/externas/cc0_hand_wear_icons/LEIA-ME.md`. O original fica intacto: adaptações trabalham sobre cópias.
- **A adaptação aprovada (M5, 32):** `ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/malha_dcss/`, a fonte
  `fontes/M5/M5-32.aseprite` (camadas `original` oculta, `malha`, `couro`) e o PNG `proposta/M5-32.png`. A silhueta, o
  contorno, a pose, os dedos, o polegar e o punho são os do original, pixel a pixel; mudou só o material (o couro preto
  com rebites virou a malha de ferro da cota). Os tamanhos 40, 48 e 64 (`fontes/M5/M5-40.aseprite`, `-48`;
  `proposta/M5-40.png`, `-48`, `-64`) foram propostos em `2d18ce15` e aguardam avaliação: confira o estado no plano
  (`roadmapIDEIAS/23-PLANO-DE-ARTE-INTERFACE-E-COMBATE.md`) antes de tratá-los como base.
- **O crédito acompanha:** se uma luva derivada entrar no jogo, o registro da origem (o `LEIA-ME.md` das externas) e o
  crédito vão junto na integração. Não invente autoria além da registrada.

## A regra: a mão não se redesenha

Para uma luva nova, **parta da base** (a mão da M5 ou o original da `glove_04`) e preserve:

- a **pose**: a luva de pé na diagonal, o punho embaixo, os dedos em cima;
- a **construção da mão**: as costas da mão, a linha dos nós, a mão que não é um bloco;
- os **dedos**: comprimentos diferentes, separados pelo contorno ou por um pixel de sombra, sem hastes;
- o **polegar**: a base perto do pulso, apontando para outra direção, ligado à mão;
- as **proporções**: a mão domina, o punho é curto; a presença dela ao lado do elmo, da cota e das armas (aprovada sem
  redução: não encolha a peça).

Não volte a desenhar a anatomia do zero, nem por medidas, nem por grade à mão, nem a partir de uma referência. Uma
mudança de silhueta pequena e necessária para o material (a borda de um punho de placas, uma garra num item de fim de
jogo) é desenhada **sobre a base**, numa camada própria, e comparada com a base em tamanho real; os dedos e o polegar
continuam os dela. Se um conceito pedir outra pose (um punho cerrado, a mão aberta de frente), isso é outra base: escolha
uma luva pronta com licença clara, como na escolha `2f91cf62`, e confirme com o Jean antes de adaptar.

## O acabamento: o que pode mudar

Separado da construção, numa ou mais camadas por cima da cópia do original:

- **O material:** couro (fosco, a luz só da forma), tecido (fosco, as dobras pela sombra do original), malha (o xadrez de
  dois tons vizinhos, como a cota), placas (o metal com reflexo localizado; os reforços nas costas da mão, nos nós ou no
  punho). Os reforços podem mudar de lugar e de forma, desde que não apaguem a separação dos dedos.
- **Metais, cores e ornamentos:** ferro, aço, latão, ouro, prata; a cor do couro ou do tecido; bordados, gemas,
  ferragens, rebites, tiras e fivelas. Cada material tem a sua rampa e a sua regra de luz (a da `arte-itens-fenda`), e a
  luz segue o volume que o original já tem.
- **O nível do equipamento:** a luva **simples** (a base comum: o material limpo, poucos reforços), a **real** (metais
  nobres, bordado, uma gema, ferragens trabalhadas) e a de **fim de jogo** (o material raro, reforços mais elaborados,
  talvez uma silhueta acrescentada sobre a base). Quanto mais decorada, mais cuidado com os dedos: a decoração fica nas
  costas da mão e no punho.
- **Efeitos** (fogo, energia, gelo, sombra): possibilidades futuras, em volta ou por cima da luva, **preservando a
  leitura dela** (os dedos, o polegar, o punho). Nenhum efeito nem animação de luva foi validado no jogo; o primeiro é
  uma proposta como as outras, sujeita à avaliação do Jean. Não acrescente efeitos nem animações por conta própria.

O jogo diz o que a luva é (`rpg/itens.py`): o acabamento mostra isso, sem brilho mágico que o item não tem.

## O fluxo

1. **A cópia da base no Aseprite:** um documento novo com a camada `original` (a base intacta, oculta, fora da
   exportação) e as camadas do material por cima (na M5: `malha` e `couro`). Guarde em `fontes/<id>/<id>-32.aseprite` no
   protótipo.
2. **A troca de material:** por regra sobre a cópia, sem mover pixel (o `manopla_perneiras/auxiliares/malha_dcss.lua` da M5 é o exemplo:
   o tom pela luminosidade do original, o contorno e as linhas dos dedos mantidos, o ornamento trocado pelo tom dos
   vizinhos), e o acabamento à mão onde a regra não basta, pelo `ferramentas/arte/aseprite/pintar.lua` (nunca o
   `put_pixels`). Uma regra nova para outro material é um script novo ao lado, no estilo do `malha_dcss.lua`.
3. **Os tamanhos:** o 32 primeiro, avaliado no jogo; o 64 = 32 ×2; o 40 e o 48 da mesma base na grade de cada tamanho
   (o `malha_dcss.lua` com `N`: a forma amostrada do original de 32, as linhas com 1 px, o padrão do material na grade do
   tamanho). O 32 aprovado não passa de novo pela regra.
4. **Exportar:** `python ferramentas/arte/exportar_aseprite.py <id> <pasta proposta> --fontes=<pasta fontes>` (a camada
   `original` fica fora); confira o composto do editor contra o PNG (`bandagem_pocao/auxiliares/soma.lua` e `soma.py`) e
   a silhueta contra a base (tem de ser idêntica, salvo o acréscimo combinado).
5. **Avaliar em tamanho real:** a prancha sobre o carvão junto do elmo, da cota, da espada, da maça e do escudo, com a
   base original ao lado e a ampliação sem suavização (as funções `malha_dcss` e `m5_tamanhos` de
   `bandagem_pocao/auxiliares/montar.py`); no jogo a 1920×945, a ficha, o Inventário (40) e o saque (64 e o "você usa"
   em 48), pelo `ferramentas/prototipos/hud/itens-lote-noite/fotografar.mjs` (`manopla_perneiras_ficha`, `m5_tamanhos`).
   Julgue pelo 1×.

## Os usos da manopla

O desenho `manopla` é a base Manopla do Guerreiro, os raros que usam o desenho da base e a silhueta das mãos vazias de
todas as classes (`VAZIO`). A habilidade Grito de Guerra usa o sprite `manopla` do jogo noutro papel e fica com ele; o
desenho de reserva das mãos sem base (`ICONE_ESPACO`) é a luva de couro. Trocar a manopla não troca esses outros papéis.

## A entrega

A da `arte-itens-fenda`, com mais três coisas:
- a comparação **base original × adaptação**, em tamanho real e ampliada, com a silhueta conferida;
- o registro da origem, da autoria e da licença da base na proposta (e no `LEIA-ME.md` das externas);
- a luva no jogo a 1920×945, ao lado do conjunto aprovado.

Pare para a avaliação. Integração só do que o Jean aprovou.
