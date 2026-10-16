# A varinha do Mago desenhada no Aseprite pelo MCP (proposta, sem versão)

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
