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
