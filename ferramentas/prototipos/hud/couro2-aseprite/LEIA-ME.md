# O capuz e a luva com braçadeira de couro (rodada 1, proposta: o 32 como fonte e o 64 ampliado 2×)

Os desenhos "capuz" (cabeça) e "luva" (mãos) do Arqueiro, desenhados no Aseprite pelo MCP. Só protótipo: o jogo,
`icones.js`, a versão e os dados dos itens não mudaram. Espera a avaliação do Jean; 40 e 48 ficam para depois da
aprovação e partirão da fonte aprovada.

## O que o jogo diz (rpg/itens.py)

| Desenho | Bases que o usam | Materiais | Únicos |
|---|---|---|---|
| `capuz` | **Capuz** e **Chapéu de Couro** (cabeça do Arqueiro); **Capuz** (cabeça do Mago) | os de couro no Arqueiro (Rasgado a Rúnico); os de tecido no Mago (Puído, de Linho, de Lã Negra, Bordado, Rúnico) | nenhum |
| `luva` | **Braçadeira** (mãos do Arqueiro); **Luva de Seda** (mãos do Mago) | couro no Arqueiro; tecido no Mago | **Mãos do Estrangulador** (base "Luvas", qualquer classe) |

- A peça das mãos do Arqueiro é uma **Braçadeira**, não uma luva; o desenho comum se chama "luva". A proposta segue os
  dados com uma peça que serve aos dois nomes: a luva de couro com o cano longo de braçadeira amarrado.
- Outros papéis, que a troca (pelo `ITEM` do `Icones`, na integração) não tocaria: a habilidade **Desaparecer** do
  Arqueiro usa o sprite `capuz` (`rpg/habilidades.py`); os espaços vazios da cabeça e das mãos usam o elmo e a
  manopla de ferro (`Icones.VAZIO`); `ICONE_ESPACO["maos"] = "luva"` (itens de saves antigos sem desenho) segue o
  mesmo papel de equipamento. O sprite `luva` de hoje é a manopla recolorida em marrom (`sprites-dados.js`).
- **Contradições com os dados, para o Jean decidir** (nada foi mudado nos dados):
  - o **Chapéu de Couro** usa o desenho do capuz: um chapéu não é um capuz;
  - o **Capuz do Mago** (tecido) e a **Luva de Seda** (tecido) dividem desenhos de couro: a proposta é de couro, como
    pede a família do Arqueiro; um desenho de tecido para o Mago seria outro;
  - a **Braçadeira** é desenhada como luva com braçadeira (para servir também à Luva de Seda e às Mãos do
    Estrangulador).

## A proposta

**Capuz (de frente, sem rosto).** A cabeça redonda com a ponta curta tombada para a direita (a cauda do capuz: a
assimetria tira o ar de peça rígida), a costura do meio do crânio (duas peças de couro), a abertura funda: a borda
virada em volta, acesa em cima e à esquerda; dentro, o escuro, a faixa do forro logo abaixo da borda e a parede de
dentro da direita um pouco clara (a espessura e a fundura); a garganta com o cordão cruzado; a capa de ombro, um
degrau para fora onde ela pousa nos ombros, com a sombra do capuz por cima, a beira de fora acesa e dois cortes na
barra; o couro raspado em dois pixels na capa, do lado da sombra. O couro e as rampas são as do gibão.
Silhuetas descartadas (numa cor só): a primeira estrangulava o pescoço e lia como um peão de xadrez; a segunda, sem
o estrangulamento, virou um sino (a massa triangular a evitar); a final tem o degrau dos ombros.

**Luva com braçadeira (uma, de costas).** A mão direita de costas, com os dedos juntos: as pontas em alturas
diferentes e vincos curtos só entre as pontas (sem linhas até a mão), o polegar saindo à esquerda com a dobra na
base, o nó dos dedos aceso; o cano longo de braçadeira, de couro mais escuro (a rampa das botas), com a beira de
cima virada, a amarração em zigue-zague do gibão até a barra e o couro raspado do lado da sombra. Uma peça só, e não
o par: no 32 o par dividiria a área e os dedos virariam ruído.

**Tamanhos:** o 32 é a fonte (desenhado na grade); o **64 é o 32 ampliado 2×** (vizinho mais próximo, sem retoque).
No cartão do saque, o 64 derivado lê bem (a abertura do capuz, os dedos, o polegar e a amarração continuam claros):
nenhuma perda de leitura que pedisse um 64 desenhado à parte.

## Arquivos

| Arquivo | O que é |
|---|---|
| `rodada1/capuz-32.aseprite` | 7 camadas: capa, capuz, interior, borda, cordao, desgaste, contorno |
| `rodada1/luva-32.aseprite` | 5 camadas: bracadeira, luva, cordao, desgaste, contorno |
| `rodada1/<peça>-32.png`, `-32@2x.png` | o 32 exportado (`Image:drawSprite` + `saveAs`) e a duplicação exata |
| `rodada1/<peça>-64.png`, `-64@2x.png` | o 32 ampliado 2× e a duplicação dele |
| `atual/` | os sprites de hoje em 16, 32 e 64 (`auxiliares/sprite_atual.py`, que agora lê também os sprites derivados por troca de letras) |
| `capturas/` | as pranchas e, em `jogo/`, as fotos e o `relatorio.json` |
| `logs/` | `aseprite.log`, `fotografar.log`, `verificacoes.log` |
| `auxiliares/couro2_r1.py` | as listas por camada do 32 (faixas por linha e luz por regras de região) |

Papel de cada parte: *ferramentas do conector* (abrir, fechar, a captura do editor); *Lua pelo `execute_script`*
(criar o documento e as camadas com `../couro-aseprite/auxiliares/montar.lua`, pintar com
`ferramentas/arte/aseprite/pintar.lua`, salvar, exportar, reabrir); *cálculos fora do editor* (`couro2_r1.py`, o 64
e os @2x, as pranchas). O `put_pixels` não foi usado.

## Conferência

- Silhueta numa cor só, antes da cor (`capturas/silhueta.png`, com o gibão e as botas); em 1× sobre o carvão ao lado
  do gibão, das botas e dos aprovados (`capturas/carvao-32.png`, `carvao-64.png`, `referencias-*.png`).
- Os `.aseprite` reabertos: camadas, 32×32, RGB; a captura do editor e o arquivo reaberto iguais ao PNG e à prévia;
  alfa só 0 e 255; o 64 é o 32 ampliado 2× exato e, reduzido de 2×2, volta ao 32; os @2x exatos
  (`logs/aseprite.log`).
- No jogo, atual × candidato, os mesmos dados, 1500×950 e 1280×720 (`../fotografar_couro2.mjs`,
  `../comparar_couro2.py`): ficha e mercado (Vender, dica) em 32, cartão do saque com o 64 derivado, as telas inteiras
  (`capturas/comparacao-<janela>-<peça>-<lugar>.png`, `prancha-zoom.png`). O "você usa" do cartão mostra o elmo e a
  manopla de ferro vestidos pelo cenário, em 48 nativo: nenhum 48 do couro aparece reduzido. Sem erro no console.

## Avaliação curta

- **Funciona:** o capuz lê como capuz vestível (a abertura funda, a borda virada, a capa nos ombros), sem rosto, sem
  parecer elmo; a luva lê como luva com polegar e braçadeira amarrada, sem parecer manopla. Os dois convivem com o
  gibão e as botas (o mesmo couro, as mesmas amarrações).
- **Ainda fraco ou a decidir:** a capa do capuz é uma faixa larga e chapada perto do resto; a ponta tombada é sutil
  em 32. Os dedos da luva em 32 são blocos de 2 px. As contradições acima (o Chapéu de Couro e os itens de tecido do
  Mago) continuam com o desenho de couro.
