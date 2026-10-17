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

---

# Rodada 2: o caimento do capuz de couro e os materiais separados

Pedido do Jean: a luva de couro com braçadeira aprovada visualmente (preservada); o capuz de couro com o caimento
corrigido (a faixa larga da base parecia a borda enrolada de um gorro e, com a abertura, o conjunto lia como uma
balaclava); um capuz de tecido e uma luva de seda para os itens de tecido do Mago, que não devem receber os
desenhos de couro. Só protótipo; 32 no Aseprite em camadas, o 64 é o 32 ampliado 2×; 40 e 48 depois da aprovação.
Tudo em `rodada2/`; a `rodada1/` ficou intacta.

## Os mapeamentos reais (rpg/itens.py) e a proposta de separação

| Desenho hoje | Itens | Material dos dados | Desenho proposto |
|---|---|---|---|
| `capuz` | Capuz do Arqueiro | couro (Rasgado a Rúnico) | **capuz de couro** (`capuz`) |
| `capuz` | Chapéu de Couro do Arqueiro | couro | capuz de couro, por ora (um chapéu precisa de desenho próprio: registrado) |
| `capuz` | Capuz do Mago | tecido (Puído, de Linho, de Lã Negra, Bordado, Rúnico) | **capuz de tecido** (`capuz_tecido`) |
| `luva` | Braçadeira do Arqueiro | couro | **luva de couro com braçadeira** (`luva`) |
| `luva` | Luva de Seda do Mago | tecido | **luva de seda** (`luva_seda`) |
| `luva` | Mãos do Estrangulador (único, base "Luvas", sem classe nem material) | (sem material) | luva de couro (o desenho "luva" de hoje) |

Hoje o `Icones` escolhe o desenho só pelo nome do sprite (`capuz`, `luva`), igual para as duas classes; separar o
couro do tecido na integração pede uma decisão:
- **(recomendado)** dar às bases de tecido do Mago um desenho próprio nos dados: em `rpg/itens.py`, o terceiro campo de
  `("Capuz", "m", "capuz")` do Mago e de `("Luva de Seda", "f", "luva")` passaria a `capuz_tecido` e `luva_seda` (só
  o desenho do item, sem nome, regra ou material); o `Icones` ganharia os dois em `TAMANHOS` e `ITEM`, e o sprite
  16×16 de fallback seguiria o mesmo (um `trocar` do capuz e da luva, como `S.luva`). Itens já salvos guardam o
  ícone antigo: ver se o save os atualiza ou se ficam com o couro;
- ou o `Icones` receber o item inteiro (classe ou nome da base) para escolher: mexe em todas as telas que pedem
  `Icones.item(sprite)`.
Nada disso foi feito: nenhum dado, regra ou ícone do jogo mudou. Nas fotos, o Arqueiro recebe o couro e o Mago o
tecido, cada um nos dados da sua classe, pela página da prévia.

## O desenho

- **Capuz de couro (revisado):** a cabeça, a abertura funda com a borda de tira acesa em cima, o interior, o cordão
  e a paleta são os da rodada 1; a faixa horizontal da base saiu. A capa agora cai dos ombros para os lados em
  diagonal, com a barra mais alta na frente e mais baixa nos lados; dois vincos de dobra em diagonal (o vale escuro
  com a crista acesa ao lado) mostram o couro flexível dobrando; a beira de baixo vira para dentro só do lado da
  sombra (sem aro contínuo). A ponta tombada da rodada 1 ficou (não prejudica o 32). Sem rosto, pescoço ou ombros de
  gente: a capa vazia.
- **Capuz de tecido:** a mesma construção (abertura, interior), mas pano: o alto num pico macio em vez da ponta de
  couro, a borda da abertura numa dobra fina de pano (um tom acima, sem tira escura), a capa caindo dos ombros
  pendurada e mais longa, com dobras verticais (faixas de 2 a 3 px claras e escuras) e a barra ondulada, sem cordão;
  lã azul-acinzentada escura. Descartados nas prévias: a ponta em pixels soltos (uma bandeirinha) e o topo redondo
  com o pano claro (lia como um fantasma).
- **Luva de seda:** a mão direita de costas, como a de couro, mas justa: os quatro dedos separados até a mão (a seda
  cola em cada dedo), mais finos; o polegar delgado; um punho curto, um pouco aberto, com a dobra de cima e sem
  amarração; o brilho da seda numa faixa diagonal suave nas costas da mão e nos dedos de cima (a diferença para o
  couro fosco). Sem joia, runa ou brilho mágico.
- **Luva de couro:** a da rodada 1, aprovada: os arquivos copiados para `rodada2/` (iguais byte a byte).

| Arquivo (`rodada2/`) | Camadas |
|---|---|
| `capuz-32.aseprite` (couro) | capa, capuz, interior, borda, cordao, desgaste, contorno |
| `capuz_tecido-32.aseprite` | capa, capuz, interior, borda, contorno |
| `luva-32.aseprite` (couro, da rodada 1) | bracadeira, luva, cordao, desgaste, contorno |
| `luva_seda-32.aseprite` | punho, luva, brilho, contorno |
| `<peça>-32.png`, `-32@2x.png`, `-64.png`, `-64@2x.png` | o 32, a duplicação, o 32 ampliado 2× e a duplicação dele |

Gerador: `auxiliares/couro2_r2.py` (o `couro2_r1.py` fica como histórico).

## Conferência

- Silhueta numa cor só antes da cor (`rodada2/capturas/silhueta.png`: couro, tecido, as duas luvas e o capuz da
  rodada 1); o capuz de couro antes e depois (`capuz-couro-r1-r2.png`); couro × tecido (`couro-tecido.png`); em 1×
  sobre o carvão com o gibão, as botas e os aprovados (`carvao-32.png`, `carvao-64.png`).
- Os `.aseprite` reabertos (camadas, 32×32, RGB); a captura do editor e o arquivo reaberto iguais ao PNG e à prévia;
  alfa só 0 e 255; o 64 é o 32 ampliado 2× exato (`logs/aseprite-r2.log`).
- No jogo (`../fotografar_couro2.mjs` com `VERSOES=atual,couro,atual_mago,tecido`): o Arqueiro com o couro e o Mago
  com o tecido, atual × candidato, ficha e mercado em 32, cartão do saque com o 64 derivado, telas inteiras, em
  1500×950 e 1280×720 (`rodada2/capturas/comparacao-<janela>-<classe>-<peça>-<lugar>.png`); conferido pela imagem que
  cada cartão mostra o arquivo do material certo; sem erro no console (`logs/fotografar-r2.log`).

## Avaliação curta

- **Funciona:** o capuz de couro deixou de ler como gorro ou balaclava: a capa cai pelos ombros, com o couro dobrando.
  Couro e tecido se distinguem pela forma (ponta, tira e cordão × pico macio, dobra fina e pano pendurado; braçadeira
  amarrada × luva justa e lisa), não só pela cor.
- **Ainda fraco ou a decidir:** o capuz de tecido é escuro e perde um pouco de contraste no cartão escuro do saque; a
  barra ondulada é sutil em 32. A separação no jogo depende da decisão de mapeamento acima. O Chapéu de Couro
  continua com o capuz.

---

# Rodada 3: a passagem do capuz de tecido para a pala

Pedido do Jean: a luva de couro com braçadeira, o capuz de couro revisado e a luva de seda aprovados visualmente
(não tocados); refinar só o capuz de tecido. Na rodada 2, a passagem do capuz para a pala era ambígua: a linha 21 era
uma faixa escura de lado a lado, a silhueta abria num degrau, as dobras eram faixas verticais paralelas e a barra
ondulava em pontas, e a parte de baixo lia como uma cortininha separada. Só protótipo; o 32 no Aseprite em camadas, o
64 é o 32 ampliado 2×; 40 e 48 depois da aprovação. Tudo em `rodada3/`; a `rodada2/` ficou intacta para comparação.

## O desenho

- **A transição:** a silhueta desce do pescoço para os ombros em diagonal contínua (um pixel por linha de cada lado,
  das linhas 19 a 22), sem degrau. Os lados do capuz, das linhas 16 a 18, já usam os planos da pala: o lado aceso da
  cabeça continua no ombro aceso, o lado da sombra no ombro da sombra, sem a linha onde um terminava e o outro começava.
- **Sem a divisão horizontal:** no lugar da faixa, só uma sombra curta logo abaixo da abertura, que segue a curva dela
  e some para os lados em duas linhas.
- **As dobras:** duas, uma de cada lado, saindo do pescoço e abrindo para fora e para baixo, na direção em que o pano
  se espalha pelos ombros (raios a partir de um ponto acima do pescoço); cada uma é um vale um tom abaixo com a crista
  acesa do lado da luz.
- **Poucos planos:** o ombro esquerdo de frente para a luz (com o alto do ombro um tom acima), a frente média, o ombro
  direito na sombra e a beira de fora mais escura.
- **A barra:** uma curva lisa, mais alta na frente e mais baixa nos lados, sem ondas nem pontas; a beira vira só do
  lado da sombra.
- **Igual à rodada 2:** a cabeça (linhas 0 a 15), o pico macio, a abertura vazia, a borda em dobra fina, o interior e a
  paleta (lã azul-acinzentada). Sem rosto nem pessoa dentro; a pala termina nos ombros (não virou capa).

| Arquivo (`rodada3/`) | O que é |
|---|---|
| `capuz_tecido-32.aseprite` | 5 camadas: capa, capuz, interior, borda, contorno |
| `capuz_tecido-32.png`, `-32@2x.png`, `-64.png`, `-64@2x.png` | o 32, a duplicação, o 32 ampliado 2× e a duplicação dele |
| `capturas/` | `capuz-tecido-r2-r3.png` (antes × depois em 1×, 2× e 8×), `carvao-32.png` e `carvao-64.png` (com as outras três peças, o gibão, as botas e a varinha), `silhueta.png`, as comparações no jogo e `prancha-zoom.png`; as fotos em `jogo/` |

Gerador: `auxiliares/couro2_r3.py` (importa a cabeça, a abertura e a paleta do `couro2_r2.py`). Papel de cada parte
em `logs/aseprite-r3.log`: *ferramentas do conector* (versão, lista, captura do editor); *Lua pelo `execute_script`*
(montar e pintar pelo `pintar.lua`, salvar, exportar, reabrir); *cálculos fora do editor* (as listas, o 64, os @2x, as
pranchas). O `put_pixels` não foi usado.

## Conferência

- Os `.aseprite` reabertos (5 camadas, 32×32, RGB); a captura do editor, o arquivo reaberto e a prévia iguais ao PNG;
  alfa só 0 e 255; 11 cores; o 64 é o 32 ampliado 2× exato. O interior e a borda iguais aos da rodada 2; a cabeça
  igual até a linha 15; os 157 pixels que mudaram ficam da linha 16 para baixo (`logs/aseprite-r3.log`).
- No jogo, rodada 2 × rodada 3, o Mago com os mesmos dados (a luva de seda da rodada 2 nas duas), 1500×950 e
  1280×720: ficha e mercado (Vender, dica) em 32, o cartão do saque com o 64 derivado, as telas inteiras
  (`rodada3/capturas/comparacao-<janela>-mago-capuz-<lugar>.png`), sem erro no console (`logs/fotografar-r3.log`).
  `fotografar_couro2.mjs` ganhou a versão `tecido_r3` e `PECAS`; `comparar_couro2.py rodada3` monta as pranchas.

## Avaliação curta

- **Melhorou:** o capuz e a pala leem como uma peça só: o pano sai do pescoço e assenta nos ombros, as dobras apontam
  para onde ele cai; sem a barra de franja. Em 1× fica mais limpo (menos riscos verticais) e o volume do ombro aceso
  aparece.
- **A conferir:** sem as pontas da barra, o pano perde um pouco o ar de "tecido mole" e a silhueta fica mais perto de
  um sino largo (a forma a evitar no couro da rodada 1; aqui o degrau dos ombros a segura). A dobra do lado da sombra
  é discreta em 32. O capuz de tecido continua escuro no cartão do saque.

## Para a integração: distinguir couro de tecido também nos saves (investigado, não implementado)

- **Hoje:** `gerar_item` (`rpg/itens.py`) copia o terceiro campo da base (`("Capuz", "m", "capuz")`) para o campo
  `icone` do item, que vai no save. `icone_de` devolve esse campo primeiro; só sem ele cai no único, na base do
  catálogo (`_ICONE_BASE`) e no espaço (`ICONE_ESPACO`). As telas recebem o desenho pelo `icone_de` (`ficha`,
  `recompensas.py`; nenhum outro lugar lê o `icone` do item direto); o `Icones` escolhe o arquivo só pelo nome do desenho.
- **Consequência:** trocar só os dados (`capuz_tecido`, `luva_seda` nas bases do Mago) vale para itens novos; os que já
  estão nos saves (equipados, na mochila, nas lojas, nos baús, onde estiverem) continuam com `capuz` e `luva` e
  mostrariam o couro. Pela base não dá para distinguir: o material Rúnico existe nas duas listas ("Capuz Rúnico" do
  Arqueiro e do Mago); o que distingue é `classe` = `mago` com `slot` cabeça ou mãos.
- **Recomendado:** os dados com os desenhos novos (itens novos) e uma migração do save (`rpg/migracoes.py`, v4 → v5,
  o caminho que o projeto usa para "nenhum código do jogo se defender de saves velhos") que percorre o save inteiro
  recursivamente e, em todo item com `classe` `mago`, `slot` `cabeca`/`maos` e `icone` `capuz`/`luva`, troca para
  `capuz_tecido`/`luva_seda`. O percurso genérico não depende de saber onde cada lista de itens mora. Fica de fora,
  sem mudar: as Mãos do Estrangulador (`classe` vazia, continuam `luva`), o Arqueiro e a habilidade Desaparecer.
  Acompanham: `TAMANHOS` e `ITEM` no `icones.js`, um sprite 16×16 de reserva para os dois nomes em
  `sprites-dados.js` (como `S.luva`), testes da migração e o gabarito (a troca do nome não mexe no sorteio, mas
  confira se as transcrições mostram o desenho).
