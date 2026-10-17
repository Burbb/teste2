# O peitoral e as botas de couro (rodada 1, proposta em 32 e 64)

Os desenhos "gibao" (o peito de couro) e "bota" (os pés de couro), desenhados no Aseprite pelo MCP. Só protótipo: o
jogo, `icones.js`, a versão e os dados dos itens não mudaram. Espera a avaliação do Jean; 40 e 48 ficam para depois
da aprovação.

## O que o jogo diz (rpg/itens.py)

| Desenho | Bases que o usam | Materiais | Únicos |
|---|---|---|---|
| `gibao` | Gibão de Couro, Capa de Patrulha, Colete Acolchoado (o peito do Arqueiro) | os de couro: Rasgado, Curtido, Reforçado, Tachonado, Rúnico | Pele do Penitente ("Couraça de Couro Humano", qualquer classe) |
| `bota` | Bota de Caça (os pés do Arqueiro) | os de couro (os mesmos cinco) | Botas do Andarilho Morto (base "Bota", qualquer classe) |

- Onde aparecem: 32 px na ficha (o corpo em miniatura), na mochila do mercado e nas dicas; 40 no corpo e na mochila do
  Inventário; 64 no cartão do saque e 48 no "você usa" dele (e o voo ao equipar parte dali). Sem desenho próprio, o
  jogo mostra hoje os sprites 16×16 (`atual/`).
- Outros papéis do mesmo sprite, que a troca (pelo `ITEM` do `Icones`, na integração) não tocaria: o estado
  Iniciativa usa o sprite `bota` (`rpg/estados.py`); o espaço vazio dos pés usa a bota de ferro (`Icones.VAZIO`).
- **Contradições com os dados, para o Jean decidir** (nada foi mudado nos dados):
  - a **Capa de Patrulha** usa o desenho `gibao`: um colete não é uma capa. A proposta é um colete (serve ao Gibão, ao
    Colete Acolchoado e à Pele do Penitente); a capa ficaria com um desenho que não é o dela;
  - **Tachonado** (com tachas) e **Rúnico** são materiais do mesmo desenho: o colete não mostra tachas nem runas, para
    não contradizer o Rasgado e o Curtido. Um desenho por material não existe no jogo hoje;
  - **Pele do Penitente** é "couro humano": o mesmo colete; o desenho não sugere a origem.

## A proposta

**Gibão (colete sem mangas, de frente).** Escolhido para não ler como camiseta (sem mangas, as cavas cortam a
silhueta) nem como placa (sem rebite nem brilho de metal). A construção explica a peça:
- duas alças de ombro com a nuca das costas mais baixa entre elas (a silhueta mostra o vão da gola), e o decote em V
  da frente mostrando o avesso das costas (a espessura);
- a pala dos ombros, uma peça por cima, com a costura dela (pontos claros só do lado aceso, no 64);
- o fechamento da frente amarrado com cordão de ilhós a ilhós até a cintura (no 32, pontos de cordão alternados);
- a cintura costurada e a saia em abas: no 64, quatro abas (cortes nas laterais e no centro), no 32 só o corte do
  centro; o recorte em V da barra aparece na silhueta nos dois;
- bordas de tira mais escura nas cavas, no decote e na barra (2 px no 64, 1 no 32).
Luz: três planos verticais (aceso à esquerda, a frente média, a sombra à direita), o peito esquerdo um degrau acima, a
pala clara em cima, a sombra da pala e da cintura em uma linha. Desgaste: um risco de couro raspado na aba da direita,
só no 64. Couro curtido castanho-médio; o avesso quase preto; cordão de couro claro.

**Botas (um par, de perfil, bico para a esquerda).** O par, como as botas de ferro da família; a de trás deslocada
para cima e para a direita, mais escura um tom, separada da da frente por uma linha de contorno: aparecem dela o cano
dobrado, o cano e o salto. As partes que a leitura pede:
- **cano** alto, mais largo na panturrilha e estreitando no tornozelo, em três planos (aceso à esquerda);
- o **topo dobrado**: o avesso de camurça (mais claro e fosco), mais largo que o cano, com a boca escura em cima e a
  sombra da dobra embaixo (a espessura do couro);
- o **tornozelo**: a tira com uma fivela de bronze velho do lado de fora e a dobra do couro logo abaixo (uma linha no
  32, duas no 64);
- o **peito do pé**: virado para cima, aceso, descendo até o bico arredondado; reflexo discreto no bico e no cano;
- a **sola** grossa e o salto, quase pretos, com a beira de cima mais clara.
Desgaste: o bico raspado (fosco), só no 64. Couro da bota um pouco mais escuro e quente que o do gibão.

## Arquivos

| Arquivo | O que é |
|---|---|
| `rodada1/gibao-32/64.aseprite` | o gibão, 8 camadas: forro, corpo, abas, pala, bordas, fecho, costuras, contorno |
| `rodada1/bota-32/64.aseprite` | as botas, 9 camadas: tras, tras_dobra, tras_sola, frente, frente_dobra, frente_sola, tira, detalhes, contorno |
| `rodada1/*.png`, `*@2x.png` | exportados (`Image:drawSprite` + `saveAs`); o @2x pela duplicação exata |
| `atual/` | os sprites 16×16 de hoje em 16, 32 e 64 (`auxiliares/sprite_atual.py`) |
| `capturas/` | as pranchas e, em `jogo/`, as fotos e o `relatorio.json` |
| `logs/` | `aseprite.log` (a pintura e a conferência), `fotografar.log`, `verificacoes.log` |
| `auxiliares/` | `couro_r1.py` (as listas por camada), `montar.lua`, `sprite_atual.py`, `fila.py`, `silhueta.py` |

**Papel de cada parte do fluxo.** *Ferramentas do conector*: abrir, fechar, a captura do editor
(`get_sprite_screenshot`) e a listagem. *Lua pelo `execute_script`*: criar o documento e as camadas (`montar.lua`),
pintar cada camada (`ferramentas/arte/aseprite/pintar.lua`, nunca o `put_pixels`), salvar o `.aseprite`, exportar o
PNG e reabrir para contar as camadas. *Cálculos fora do editor* (`couro_r1.py`): as formas como polígonos num espaço
de 100 unidades, rasterizados na grade de cada tamanho pelo centro do pixel, a luz por planos e o que cada tamanho
simplifica (`MEDIDAS_GIBAO`, `MEDIDAS_BOTA`); as pranchas e o @2x. O 32 não é redução do 64: as mesmas formas
rasterizadas na grade de 32, com menos detalhe.

Refazer: `python ferramentas/prototipos/hud/couro-aseprite/auxiliares/couro_r1.py <pasta>` gera as listas; no
Aseprite, `dofile("<auxiliares>/montar.lua").montar(n, "<pasta>/<peça>-<n>/", {camadas})`.

## Conferência

- Silhueta numa cor só (`capturas/silhueta.png`), antes da cor. A primeira silhueta do gibão era quase um retângulo
  (ombros até a beira, as cavas rasas): refeita com alças, nuca, cavas fundas e o recorte da barra.
- Em 1× sobre o carvão, ao lado dos aprovados (`capturas/carvao-32.png`, `carvao-64.png`, `referencias-*.png`).
- Os `.aseprite` reabertos: camadas, dimensões e modo; a captura do editor igual ao PNG e à prévia; alfa só 0 e 255
  (`logs/aseprite.log`).
- No jogo, atual × candidato, os mesmos dados, 1500×950 e 1280×720 (`../fotografar_couro.mjs`,
  `../comparar_couro.py`): ficha e mercado (Vender, dica) em 32, cartão do saque em 64, as telas inteiras
  (`capturas/comparacao-<janela>-<peça>-<lugar>.png`, `prancha-zoom.png`). O "você usa" do cartão mostra a peça de
  ferro vestida pelo cenário, em 48 nativo: nenhum 48 do couro (que ainda não existe) aparece reduzido. Sem erro no
  console (`capturas/jogo/relatorio.json`).
- Para as fotos, `tests/navegador/cenarios.py` ganhou `VESTIR=<desenho>[,...]` (veste peças comuns com esses
  desenhos, cada uma no seu espaço) e `AMOSTRA` para peças que não são arma (o espaço vem do desenho). Para armas o
  sorteio é o mesmo de antes.

## Avaliação curta

- **Funciona:** o gibão lê como colete de couro vestível (alças, cavas, gola com o avesso, amarração, saia em abas),
  com volume em poucos planos, sem parecer camiseta nem placa. As botas leem como par de botas de cano alto: dobra,
  tornozelo com tira, peito do pé, sola e salto separados; a de trás se reconhece pelo cano dobrado e pelo salto.
- **Ainda fraco:** em 32 os dois são mais escuros e ocupam menos área que a cota e as botas de ferro; no espaço
  escuro da ficha ficam com menos presença que o placeholder laranja. A bota de trás mostra pouco do pé (o bico fica
  atrás da da frente). O cordão do gibão no 32 é só uma fileira de pontos. A fivela no 32 é um ponto.

---

# Rodada 2: o fechamento do gibão de 32 e os tamanhos 40 e 48

Pedido do Jean: preservar os desenhos; no gibão de 32, só o fechamento da frente (os pontos soltos pareciam botões,
enquanto o 64 mostra cordão): poucos traços conectados, lendo em tamanho real; depois o 40 e o 48 das duas peças, com
a construção aprovada. Tudo em `rodada2/`; a `rodada1/` ficou intacta.

- **O gerador:** `auxiliares/couro_r2.py` (cópia do `couro_r1.py`, que fica como histórico). O que era fixo para o
  64 e o 32 virou medida de cada tamanho (`MEDIDAS_GIBAO`, `MEDIDAS_BOTA`: o tipo de cordão, os ilhós, o desgaste, a
  fivela, o furo, os vincos, o brilho, quanto o par desce). Conferido: o 64 das duas peças e as botas de 32 saem
  idênticos à rodada 1, pixel a pixel.
- **O fechamento do 32:** o cordão num traço só, em zigue-zague dentro da fenda escura: um pixel por linha,
  alternando as duas colunas (os pixels se tocam na diagonal), claro do lado aceso e médio do lado da sombra, de y 11
  a 16. Mudaram só 5 pixels. Comparadas em 1× três variantes (`rodada2/capturas/fecho-variantes-32.png`; o antes e depois em
  `rodada2/capturas/fecho-gibao-32.png`):
  o zigue-zague sobre a fenda escura leu como cordão; a "trança" (o vão preenchido com cordão escuro) perdeu contraste;
  a versão curta voltou a parecer pontos.
- **Gibão 40:** a construção do 32 com mais uma fileira: o mesmo cordão em zigue-zague, só o corte central da saia,
  borda de 1 px, sem costura nem desgaste; um ajuste tira a ponta de 1 px que a axila fazia (`AJUSTES_GIBAO[40]`).
- **Gibão 48:** a do 64 simplificada: ilhós e cordão em X (4 vãos em vez de 6), três cortes na saia, a costura da pala
  e da cintura em pontos, desgaste de 3 pixels.
- **Botas 40:** como o 32: uma dobra no tornozelo, fivela de poucos pixels, sem furo nem desgaste.
- **Botas 48:** como o 64: duas dobras no tornozelo com a linha clara em cima, fivela com furo, desgaste de 2 pixels no
  bico.
- **Conferido:** a silhueta numa cor só dos quatro tamanhos (`rodada2/capturas/silhueta.png`), depois a cor; os oito
  `.aseprite` reabertos (8 e 9 camadas, dimensões, RGB) e a captura do editor dos cinco que mudaram ou são novos, igual
  ao PNG e à prévia; alfa só 0 e 255; @2x exatos (`logs/aseprite-r2.log`). Sobre o carvão com os aprovados
  (`rodada2/capturas/carvao-32/40/48/64.png`). No jogo, atual × rodada 2, 1500×950 e 1280×720 (`../fotografar_couro.mjs`
  com `VERSOES=atual,rodada2`, que agora também fotografa o Inventário e o voo e, no saque, veste a mesma peça para o
  "você usa" mostrar o 48 nativo): ficha e mercado 32, corpo e mochila do Inventário 40, cartão do saque 64 com o 48 ao
  lado, voo a partir do 48 (`rodada2/capturas/comparacao-*.png`, `prancha-zoom.png`); sem erro no console
  (`logs/fotografar-r2.log`).

## Comparação pedida: o 64 trabalhado × o 32 final ampliado 2×

Pedido do Jean: ver no cartão do saque, no mesmo espaço e com os mesmos dados, o 64 trabalhado e o 32 final ampliado
exatamente 2× por vizinho mais próximo (o `rodada2/<peça>-32@2x.png`, sem suavização nem retoque), para avaliar se o
detalhe extra do 64 justifica o tratamento nos próximos itens. Não substitui os arquivos; a regra da skill não muda.

- **Como:** `../fotografar_couro.mjs` com `VERSOES=rodada2,x2 LUGARES=saque`: a versão "x2" é a rodada 2 com o pedido
  do 64 respondido pelo 32@2x; o mesmo cenário (vila, Arqueiro, o achado e a mesma peça vestida para o "você usa" em
  48), 1500×950 e 1280×720; fotos em `rodada2/capturas/jogo-x2/`, sem erro no console (`logs/fotografar-x2.log`).
  Pranchas: `rodada2/capturas/x2-gibao.png` e `x2-bota.png` (`python ferramentas/prototipos/hud/comparar_couro.py x2`),
  com os cartões rotulados "64 trabalhado" e "32 ampliado 2x" e as duas artes em 1× e 3×.
- **Conferido que cada cartão mostra o arquivo certo:** procurando cada arquivo no recorte do cartão, a diferença média
  é de 2,7 a 5,7 contra o arquivo pretendido e de 10 a 16 contra o outro (o resto vem do brilho de raridade, um
  `drop-shadow` da arte do cartão).

