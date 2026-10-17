# A varinha do Mago desenhada no Aseprite pelo MCP (proposta, sem versão)

> **Integrada na 1.109.0 (histórico daqui para baixo).** A versão aprovada é a de `rodada2/` no commit `451ff11`. As
> fontes finais foram para `ferramentas/arte/aseprite/varinha/` e os PNGs do jogo saem de
> `ferramentas/arte/exportar_aseprite.py varinha` (ver `ferramentas/arte/aseprite/LEIA-ME.md`). O `pintar.lua` mudou
> para `ferramentas/arte/aseprite/pintar.lua` (o `auxiliares/montar.lua` já o carrega de lá). Papel de cada script
> desta pasta, todos histórico, nenhum grava no jogo: `auxiliares/varinha_r2.py` calcula as listas das camadas da
> rodada 2 (as prévias saem iguais aos finais) numa pasta dada; `auxiliares/partes64.py`, `contorno.py` e
> `conferir.py` são da primeira rodada; `../fotografar_varinha.mjs` e `../comparar_varinha.py` fotografam e montam as
> pranchas das propostas com o `icones.js` trocado na página. A conferência do jogo integrado é a de
> `ferramentas/arte/fotografar_itens.mjs` (`SO=varinha`).

Primeiro item real pelo fluxo Aseprite + MCP `aseprite` (aseprite-mcp 0.6.0, Aseprite 1.3.18.6 da Steam). Só no
protótipo: o jogo, a skill `arte-itens-fenda` e os dados da Varinha não mudaram. Espera a avaliação do Jean.

## O que o jogo diz

- `rpg/itens.py`: "Varinha" (feminino, desenho `varinha`) é uma das quatro bases de arma do Mago, ao lado de Cajado,
  Orbe e Grimório; os nomes variam pelo material ("Varinha de Ferro da Precisão", "Varinha Enferrujada"). Não há
  único com o desenho `varinha`.
- Papéis: só o equipamento. `Icones.ITEM` ainda não tem `varinha` (o jogo mostra o sprite 16×16 de
  `sprites-dados.js`: um risco marrom com uma ponta lilás). Nenhum outro papel usa o desenho.
- O desenho é um só para todos os materiais, como no cajado.

## A proposta

Varinha curta e esguia (cerca de 70% do comprimento do cajado), na diagonal da família, do pé embaixo à esquerda até a
ponta em cima à direita:
- **pomo** de bronze envelhecido, redondo, com um ponto de luz;
- **empunhadura** de couro, 3 linhas no 32 e 6 no 64, com duas costuras discretas só no 64;
- **anel** de bronze separando a empunhadura da haste;
- **haste** de jacarandá (madeira escura avermelhada, para não repetir o carvalho do cajado e contrastar com o âmbar),
  2 linhas no 32; no 64 afila em três trechos (5, 4 e 3 linhas), com o brilho de madeira polida na borda de cima;
- **soquete** de bronze em taça, com duas garras subindo pelas faces do cristal;
- **cristal âmbar** pequeno, mais largo que a boca da taça (lê como pedra assentada, não como continuação do tubo),
  em faces largas: a de cima clara, a da frente média, a de baixo escura; um reflexo pequeno (1 px no 32, um grupo
  de 3 no 64), a luz que atravessa embaixo e a sombra de contato junto da borda. Sem aura nem partículas.

Contorno de 1 px na cor comum (`#08080a`). Cores: 23 no 32 e 26 no 64, contando o contorno.

## Arquivos

| Arquivo | O que é |
|---|---|
| `varinha-32.aseprite`, `varinha-64.aseprite` | os editáveis, uma camada de arte (`Layer 1`), 1 quadro, RGB, fundo transparente |
| `varinha-32.png`, `varinha-64.png` | exportados pelo MCP (`export_png`) |
| `varinha-32@2x.png`, `varinha-64@2x.png` | a duplicação exata (vizinho mais próximo, em Python), para o `srcset` da página |
| `atual/` | o sprite 16×16 do jogo em 16, 32 e 64, para comparar |
| `capturas/` | as pranchas (abaixo) e `jogo/`, as fotos do jogo de `../fotografar_varinha.mjs` |
| `auxiliares/` | os scripts que calcularam os lotes do 64 e o contorno, e a conferência (ver "Limitações") |

Pranchas (`python ferramentas/prototipos/hud/comparar_varinha.py`):
- `carvao-tamanhos.png`: o 32 e o 64 em 1× sobre o carvão da HUD, com a ampliação;
- `familia.png`: a varinha ao lado do cajado, do orbe, do grimório e do escudo aprovados, em 32 e 64 (1× e 3×);
- `comparacao-<janela>-<lugar>.png`: atual × proposta no jogo (ficha, mercado/venda, dica de comparação, cartão do
  saque e as telas inteiras), em 1500×950 e 1280×720;
- `prancha-zoom.png`: os espaços no jogo ampliados 3× (ficha 32, venda 32, saque 48 e 64);
- `referencias-32.png`, `referencias-64.png`: as referências aprovadas e o sprite atual, vistos antes de desenhar.

Fotos: `PLAYWRIGHT_BROWSERS_PATH=C:/Users/Jean Wress/Tools/playwright/browsers PLAYWRIGHT_MODULO=file:///C:/Users/Jean%20Wress/Tools/playwright/node_modules/playwright/index.mjs node ferramentas/prototipos/hud/fotografar_varinha.mjs`
(o Playwright 1.48.2 e o Chromium dele foram instalados em `C:\Users\Jean Wress\Tools\playwright`, fora do jogo).
A página da proposta recebe um `icones.js` com `TAMANHOS.varinha = [32, 64]` e `ITEM.varinha`, e os arquivos daqui;
o jogo não muda. Conferido pelo relatório das fotos: a ficha e o mercado usam `varinha-32` (32 px), o cartão do saque
`varinha-64` (64 px); sem erro no console nas quatro rodadas.

## O que foi feito pelo MCP

Todo pixel dos dois desenhos foi escrito no Aseprite pelas ferramentas do MCP; o Python só calculou listas de
coordenadas (e o @2x e as pranchas, fora dos `.aseprite`).

**32** (`varinha-32.aseprite`, 9 passos no histórico do Aseprite):
1. `create_sprite` 32×32 RGB (camada `Layer 1`, transparente).
2. `draw_pixels_batch` 64 px: pomo, empunhadura, anel, haste, soquete e um primeiro cristal, coordenadas escritas à mão
   por coluna da diagonal.
3. `get_canvas_image` 8×: o cristal ficou fino e esfiapado; `draw_pixels_batch` 17 px com um cristal maior.
4. `get_region` 32×32 → contorno calculado (vizinhos vazios) → `draw_pixels_batch` 58 px.
5. `get_canvas_image` 8× e 1×: o cristal lia como chama (topo claro e chato). `erase_area` na ponta e
   `draw_pixels_batch` 16 px com o cristal em faces; `get_region` → `draw_pixels_batch` 12 px de contorno.
6. `export_png` de rascunho → prancha sobre o carvão: a empunhadura sumia no contorno e o cristal ainda parecia chama.
   `draw_pixels_batch` 29 px: couro mais claro, ponta escura, reflexo de 1 px, face de baixo do escuro ao quase preto.
7. Prancha de novo: o cristal com a largura da boca parecia vela. `draw_pixels_batch` 5 px: o meio do cristal 1 px
   mais largo de cada lado e o contorno.
8. `draw_pixels_batch` 4 px: o pomo chamava mais atenção que o cristal; um ponto claro só.
9. `save_sprite` e `export_png`.

**64** (`varinha-64.aseprite`, 10 passos no histórico):
1. `create_sprite` 64×64 RGB.
2. Três `draw_pixels_batch` (94, 83 e 43 px): pomo, empunhadura e anel; haste e soquete; cristal. As listas saíram de
   regras por parte ao longo da diagonal (`auxiliares/partes64.py`).
3. `get_canvas_image` 6×: cristal sem faces, pomo e bronze claros demais. `get_region` da ponta, `erase_area` 14×15,
   e dois lotes (43 e 112 px) com o bronze mais escuro, a taça menor que a pedra e o cristal refeito.
4. `get_region` 64×64 → `draw_pixels_batch` 96 px de contorno. `export_png` de rascunho → prancha.
5. Na prancha, o cristal ainda serrilhado (um tom por linha diagonal). `draw_pixels_batch` 36 px: faces largas, cada
   uma num tom.
6. `draw_pixels_batch` 62 px: a haste afilando em três trechos; `get_region` → `draw_pixels_batch` 4 px de contorno.
7. `save_sprite` e `export_png`.

**Conferência** (pelo MCP): `close_sprite` dos dois, `open_file` de cada `.aseprite`, `get_sprite_info` (32×32 e
64×64, RGB, 1 quadro, 1 camada), `list_layers` (`Layer 1`, visível, não é fundo), `get_pixel` nos cantos (alfa 0),
`get_canvas_image` em 1× e ampliado, `get_region` inteiro comparado com o PNG exportado (`auxiliares/conferir.py`):
0 diferenças; alfa só 0 ou 255; 129 pixels opacos no 32 e 306 no 64.

## Limitações reais encontradas

- **Camadas:** não há como renomear, apagar nem escolher a camada ativa. O documento novo nasce com `Layer 1`; a
  experiência ficou numa camada só, sem nome próprio. Num documento de duas camadas (o teste da conexão), só a última
  criada pode ser lida e editada.
- **Leitura:** `get_region` devolve a cor sem o alfa (vazio sai `000000`) e no máximo 4096 px por chamada (o 64×64
  inteiro cabe no limite); o alfa só pixel a pixel (`get_pixel`). `get_canvas_image` mostra o transparente sobre
  branco: para julgar sobre o carvão foi preciso exportar e montar a prancha fora.
- **Ferramentas de pixel art:** sem contorno automático (o Outline do Aseprite), sem paleta nem rampas, sem
  espelhar, girar ou escalar, sem exportar o @2x. O contorno saiu de uma conta em Python sobre a leitura
  (`auxiliares/contorno.py`) e foi desenhado pelo lote; o @2x, por duplicação em Python.
- **Desenho:** o lote pede cada coordenada. No 32, escritas à mão; no 64 (cerca de 300 pixels), calculadas por regras
  de faixa em Python antes de ir ao Aseprite. A decisão de cada correção veio da imagem lida pelo MCP; a execução foi
  sempre pelo MCP.
- **Arquivos:** `save_sprite` e `export_png` sobrescrevem qualquer caminho absoluto sem avisar (os nomes foram
  escolhidos para não colidir).
- **Conexão:** um Aseprite antigo (1.3-rc2) aberto ao mesmo tempo conectava na porta 9876 sem responder aos
  comandos (tempo esgotado); com só o da Steam aberto, tudo respondeu.
- **Verificações locais:** o `pyflakes` não está instalado neste Python (as sintaxes foram conferidas com
  `py_compile` e `node --check`).

## Avaliação curta

- **Melhorou** em relação ao sprite atual: material reconhecível (madeira, couro, bronze, âmbar), pomo e ponta que
  fazem a silhueta de varinha e não de graveto, e identidade separada do cajado (mais curta e fina, pedra âmbar em vez
  de azul, sem garras grandes). O 64 do saque ganhou volume e luz.
- **Ainda fraco:** no 32 ela ocupa menos área que os vizinhos da família e pode parecer frágil ao lado do orbe e do
  grimório; o cristal do 32 tem cerca de 4 px e as faces quase não se leem (lê como "ponta âmbar"); a haste do 32
  tem o serrilhado natural da diagonal de 2 px. O cristal do 64 tem menos acabamento que o do cajado.
- **Fora do pedido:** 40 (Inventário) e 48 (o "você usa" do saque) não foram desenhados; na foto, o 48 usa o @2x do 32
  reduzido pelo navegador (borrado), e o 40 ficaria no 32 centrado, como o jogo faz com qualquer peça sem 40.
- **O fluxo:** comparado aos geradores de `ferramentas/arte/`, o Aseprite deu o `.aseprite` editável, o histórico de
  desfazer e a leitura do resultado a cada passo. Mas faltaram camadas, contorno e paleta, e cada ida e volta custa
  uma chamada; as regras por tamanho continuaram fora do editor.

---

# Rodada 2 (16/10/2026): conector com camadas, a pedra do 64, o 40 e o 48

Com o conector `aseprite-bridge` (rezaahmadn/aseprite-mcp-bridge, extensão 1.0.0; registro fora do repositório, em
`C:\Users\Jean Wress\Tools\aseprite-mcp-bridge-INSTALACAO.md`). Os arquivos da primeira rodada, acima, ficaram intactos;
tudo desta rodada está em `rodada2/`. Só protótipo: o jogo, `icones.js`, regras e versão não mudaram.

## O teste do conector

Num arquivo de teste fora do repositório (`C:\Users\Jean Wress\Tools\aseprite-mcp-bridge-teste\`), conferido pela
leitura das camadas, pelo PNG exportado (pixel a pixel, em Python) e pela imagem composta que chega ao Claude.

**Camadas: tudo funcionou pelas ferramentas do conector.** Criar (`add_layer`), desenhar e ler numa camada anterior
pelo nome sem trocar a ativa (`put_pixels`/`get_pixel` com `layer`), renomear, reordenar (`reorder_layer`, índice de
baixo para cima), esconder e mostrar, duplicar (a cópia é independente e vira a ativa), apagar; salvar `.aseprite`,
fechar e reabrir: camadas, nomes, ordem e visibilidade preservados; o composto exportado respeita a ordem e omite a
camada oculta; `get_sprite_screenshot` chega como imagem visível, em 1× (de 16 a 64 px: para julgar é preciso ampliar
fora), igual pixel a pixel ao PNG exportado.

**Dois defeitos do `put_pixels` (e do `put_pixel`), medidos:**
1. *Descarte fora da cel.* As coordenadas são do documento (a posição da cel é descontada; conferido numa cel
   deslocada), mas o pixel que cai fora do retângulo da cel é descartado em silêncio e a resposta conta todos
   (`pixels_set` com o total pedido). Não acontece numa cel de tela inteira (a que o conector cria; salvar e reabrir
   não recortou a cel), mas acontece numa cel menor: a que o lápis do próprio Aseprite cria (um traço gerou uma cel de
   9×7, outro de 3×1), uma cel deslocada (4×3 em 12,20) ou parcialmente fora da tela (em −2,−2). Em todas, os pixels
   das bordas sumiram e os de dentro da cel caíram no lugar certo.
2. *Desfazer não desfaz.* O comando escreve direto na imagem da cel, e o Aseprite não registra isso: `undo` consome um
   passo "Put Pixels" vazio e o pixel continua lá (conferido isolado).

**A solução usada (`auxiliares/pintar.lua`, pelo `execute_script`):** uma imagem nova que cobre a cel antiga e a tela
inteira, com o conteúdo antigo copiado no mesmo lugar do documento e os pixels pedidos por cima; a troca de
`cel.image` e `cel.position` acontece numa transação só. Preserva o desenho, escreve em qualquer ponto da tela, recusa e
lista o que cai fora da tela (nunca em silêncio), relê cada pixel pedido depois de gravar e é um passo de desfazer
(desfazer volta à cel pequena com o desenho antigo; refazer, à grande). Conferido nas três cels problemáticas, depois
de salvar, fechar e reabrir, e no PNG exportado. O `put_pixels` não foi usado no desenho da varinha.

**Outras observações:**
- `io.open` dentro do `execute_script`, e `sprite:saveCopyAs` para PNG num documento com camadas, pararam o conector
  por 60 s sem resposta, e nada foi gravado. O mais provável é uma janela de permissão ou de opções do Aseprite. Por
  isso o `pintar.lua` lê as listas por `dofile` (arquivos `.lua` que só fazem `return "<lista>"`) e o PNG sai sempre
  pelo `export_png` do conector (que desenha o sprite numa imagem e grava, sem janela).
- `save_sprite` com `path` grava uma cópia (`saveCopyAs`): o documento aberto continua "Sprite".
- `get_image_data` devolve só a imagem da cel, com `offset_x`/`offset_y`; em `hex_array` é longo demais para usar (um
  32×32 são 1024 cadeias). Para ler, o `pintar.lua` tem `P.ler` (só os opacos, em coordenadas do documento) e
  `P.camadas` (ordem, nome, visibilidade e quantos pixels).

## O desenho

`auxiliares/varinha_r2.py` calcula as listas de cada camada. O Python só calcula: cada pixel foi escrito no Aseprite
pelo `pintar.lua`, com o documento e as camadas criados pelo `auxiliares/montar.lua` (no primeiro 64 de teste, as
camadas foram criadas pelas ferramentas `add_layer`/`rename_layer` do conector). Camadas, de baixo para cima: `pomo`,
`empunhadura`, `anel`, `haste`, `taca`, `pedra`, `garras`, `contorno`.

- **32**: o aprovado, só repartido nas camadas (depois, só a haste mudou: ver "Ajuste" abaixo). A camada `garras`
  fica vazia.
- **64**: da haste para baixo, intacto nesta primeira entrega (só 66 pixels mudaram, todos da taça para cima, u ≥ 25;
  depois, a haste foi uniformizada: ver "Ajuste" abaixo). A pedra da
  primeira rodada (uma ponta afilada, que lia como chama) virou uma pedra lapidada quadrada na grade, de 6×6 com cantos
  cortados. Na diagonal da varinha ela fica como um losango baixo, com o canto de baixo afundado na taça e quatro faces
  planas divididas pelas diagonais (em cima e à esquerda acesas, à direita média, embaixo escura; as divisórias a 45°
  são as linhas mais nítidas do pixel), um reflexo de 2 px e a luz que atravessa saindo na face da direita. A taça
  ficou mais curta e escura, abrindo em degrau, e uma garra de bronze sobe pela aresta acesa da pedra.
  Tentativas descartadas nas prévias: um corpo octogonal de faces retas (lia como bola laranja) e o perfil de
  lapidação com pavilhão e coroa (lia como cogumelo).
- **48** e **40**: desenhados na própria grade com a mesma construção (`MEDIDAS`): pedra de 5×5 no 48 e de 4×4 no 40;
  empunhadura de 4 e haste de 4→3 no 48; empunhadura de 3 e haste de 3→2 no 40, como no 32.
- Cores: 23 (32), 22 (40), 25 (48) e 26 (64), com o contorno. Alfa só 0 ou 255.

| Arquivo (`rodada2/`) | O que é |
|---|---|
| `varinha-32/40/48/64.aseprite` | os editáveis: 8 camadas, 1 quadro, RGBA, fundo transparente |
| `varinha-32/40/48/64.png` | exportados pelo conector (`export_png`) |
| `varinha-*@2x.png` | a duplicação exata (vizinho mais próximo, em Python, conferida pixel a pixel) |
| `capturas/` | as pranchas; `capturas/jogo/`, as fotos e o `relatorio.json` |

Conferência: cada `.aseprite` reaberto pelo conector (`open_sprite`), as 8 camadas listadas, o composto reexportado
igual ao PNG salvo e à prévia do gerador; a captura (`get_sprite_screenshot`) do 32 igual ao PNG.

## As fotos

`SAIDA=ferramentas/prototipos/hud/varinha-aseprite/rodada2/capturas/jogo VERSOES=atual,proposta,rodada2` no
`fotografar_varinha.mjs` (com as variáveis do Playwright de cima), que agora também fotografa o Inventário e o voo ao
equipar; `python ferramentas/prototipos/hud/comparar_varinha.py rodada2` monta as pranchas (as da primeira rodada
continuam saindo sem o argumento). O relatório confirma, nas duas janelas: ficha e mercado com `varinha-32` (32 px),
corpo e mochila do Inventário com `varinha-40` (40 px), cartão do saque com `varinha-64` (64 px) e o "você usa" com
`varinha-48` (48 px); o voo parte do 48 (51 px no meio do caminho, a animação de sempre). Sem erro no console.

Pranchas: `ponta-64.png` (a ponta antes e depois em 1×, 2× e 8×), `carvao-tamanhos.png`, `familia.png` (com o
cajado, o orbe, o grimório e o escudo em 32, 40, 48 e 64), `comparacao-<janela>-<lugar>.png` (atual, rodada 1 e
rodada 2: ficha, Vender, dica, Inventário, cartão do saque, voo e as telas inteiras) e `prancha-zoom.png`.

## Avaliação curta

- **Melhorou:** a pedra do 64 lê como pedra maciça de faces planas, presa na taça; a gota afilada, que lia como chama,
  saiu. O 48 do "você usa" e o 40 do Inventário deixaram de ser o 32 reduzido ou centrado.
- **Ainda fraco ou a decidir:** a pedra do 64 (quadrada) e a do 32 aprovado (uma ponta mais alongada) não têm a mesma
  forma. Em tamanho real as duas leem como "ponta âmbar", mas de perto são cortes diferentes. A pedra de 4×4 do 40 é
  pouco mais que um bloco laranja com reflexo. No nicho, a varinha continua mais fina e leve que o cajado e o orbe,
  como no 32 aprovado.
- **O fluxo:** o conector novo resolve as camadas, que eram o maior limite da primeira rodada. O desenho continua
  vindo de listas calculadas fora, e o `put_pixels` só serve com a ressalva acima (o `pintar.lua` o substitui).

## Ajuste: o mesmo perfil de haste nos quatro tamanhos

Pedido do Jean: a haste reta, com afunilamento suave, na direção do 40, sem barrigas nem mudanças de lado no trecho
avermelhado; o 32 aprovado pode mudar para isso; materiais, paleta, enquadramento e o resto ficam.

- **O que estava errado** (o perfil de través de cada passo ao longo da varinha): cada tamanho afinava de um jeito. O 40
  mantinha reta a borda da sombra e afinava uma vez pelo lado aceso; o 48 mantinha reta a borda acesa; o 64 começava
  com 5 logo depois do anel (a barriga) e afinava para 4 pelo lado aceso e para 3 pela sombra, e o eixo ia e voltava;
  o 32 afinava só no anel, com um entalhe logo depois dele.
- **A regra agora** (`varinha_r2.py`, no cabeçalho): a borda da sombra da haste é uma linha reta do anel até a taça;
  a haste começa na largura do anel e afina num degrau só, do lado aceso, a cerca de 53% do comprimento (onde o 40
  afina); entra na taça sem degrau de lado. Espessuras: 32 3→2, 40 3→2, 48 4→3, 64 5→4 (o fim fica perto de 1/16 do
  tamanho nos quatro).
- **Mudou:** no 32, 8 pixels (3 de madeira clara na borda acesa da metade de baixo, 2 do meio um tom abaixo para a luz
  ficar na borda, e o contorno ao lado; `HASTE32`); no 48, a haste e o gargalo da taça (4 pixels, uma unidade para o
  lado da sombra, para a haste entrar reta); no 64, a haste sai da regra (antes vinha do PNG da primeira rodada) e o
  contorno do anel para cima é recalculado. O 40 não mudou. Pomo, empunhadura, anel, pedra, garras e paleta iguais.
- **Conferido:** primeiro a silhueta numa cor só (`capturas/haste-silhueta.png`: em cima antes, embaixo depois),
  depois o desenho completo (`capturas/haste-cor.png`) e de perto (`capturas/haste-zoom.png`: o 32 aprovado e o novo,
  e as emendas haste–taça do 48 e do 64). Pintado no Aseprite pelo `pintar.lua`; os `.aseprite` reabertos com as 8
  camadas e o composto igual ao PNG salvo e à prévia; @2x refeitos; fotos da rodada 2 refeitas nas duas janelas
  (as do jogo atual e da rodada 1 são as de antes), sem erro no console; pranchas remontadas.

## Ajuste: a pedra do 32 no corte compacto

Pedido do Jean (com a haste aprovada nos quatro tamanhos): só o cristal do 32, no mesmo corte compacto do 40, 48 e
64, sem a ponta alongada, mantendo o reflexo, o âmbar e a separação do suporte.

- **Feito** (`PEDRA32` em `varinha_r2.py`): a pedra quadrada de 4×4 de cantos cortados do 40 (o menor tamanho em que
  as quatro faces ainda aparecem; proporção 1:1, como nos outros), com o canto de baixo afundado na taça e o reflexo de
  1 px em cima à esquerda. O pixel de bronze da taça na aresta acesa fica por cima da pedra, como garra. A ponta
  alongada (16 px, até 28,3) virou uma pedra de 12 px visíveis que termina em 27,5; o contorno da ponta foi
  recalculado.
- **Não mudou:** haste, empunhadura, anel, pomo e taça do 32 (conferido: só 28 pixels mudaram, todos da pedra e do
  contorno dela, u ≥ 16); o 40, o 48 e o 64 intactos.
- **Conferido:** pintado no Aseprite pelo `pintar.lua`; o `.aseprite` reaberto com as 8 camadas e o composto igual ao
  PNG e à prévia; @2x refeito; `capturas/pedra-32-carvao.png` (antes e depois em 1× sobre o carvão) e
  `capturas/pedra-32-jogo.png` (ficha, Vender e dica, antes e depois, nas duas janelas); fotos da rodada 2 refeitas,
  sem erro no console.
