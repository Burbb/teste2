# Fontes em Aseprite

Os ícones cuja fonte final é um `.aseprite` em camadas, desenhado no Aseprite (pelo MCP ou à mão). O jogo nunca lê
nada daqui: só os PNGs exportados para `rpg/web/static/hud/icones/`.

## As fontes finais

| Peça | Arquivos | Camadas (de baixo para cima) | No jogo desde |
|---|---|---|---|
| varinha | `varinha/varinha-32.aseprite`, `-40`, `-48`, `-64` (RGBA, 1 quadro, fundo transparente) | pomo, empunhadura, anel, haste, taca, pedra, garras, contorno | 1.109.0 |
| gibao (peito de couro) | `gibao/gibao-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** (sem fonte própria) | forro, corpo, abas, pala, bordas, fecho, costuras, contorno | 1.110.0 |
| bota (botas de couro) | `bota/bota-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** (sem fonte própria) | tras, tras_dobra, tras_sola, frente, frente_dobra, frente_sola, tira, detalhes, contorno | 1.110.0 |
| capuz (capuz de couro) | `capuz/capuz-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | capa, capuz, interior, borda, cordao, desgaste, contorno | 1.112.0 |
| luva (luva de couro com braçadeira) | `luva/luva-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | bracadeira, luva, cordao, desgaste, contorno | 1.112.0 |
| capuz_tecido (capuz de tecido) | `capuz_tecido/capuz_tecido-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | capa, capuz, interior, borda, contorno | 1.112.0 |
| luva_seda (luva de seda) | `luva_seda/luva_seda-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | punho, luva, brilho, contorno | 1.112.0 |
| calca_couro (Calça de Couro do Arqueiro) | `calca_couro/calca_couro-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | pernas, remendo, cos, barra, braguilha, desgaste, contorno | 1.119.0 |
| attr-ataque (o ícone de Ataque) | `attr-ataque/attr-ataque-24.aseprite`, `-32`; **o 64 é o 32 ampliado 2×** | lamina, guarda, cabo, pomo, contorno | 1.120.0 |
| attr-defesa (o ícone de Defesa) | `attr-defesa/attr-defesa-24.aseprite`, `-32`; **o 64 é o 32 ampliado 2×** | face, borda, bossa, contorno | 1.120.0 |
| attr-poder (o ícone de Poder) | `attr-poder/attr-poder-24.aseprite`, `-32`; **o 64 é o 32 ampliado 2×** | chama, miolo, faisca, contorno | 1.123.0 |
| atalho-inventario (o Inventário da doca) | `atalho-inventario/atalho-inventario-36.aseprite`, `-32` | rolo, bolsos, corpo, aba, cinta, fivela, contorno | 1.124.0 |
| vital-vida (a Vida do topo) | `vital-vida/vital-vida-20.aseprite` | coracao, brilho, contorno | 1.130.0 |
| vital-mana (a Mana do topo) | `vital-mana/vital-mana-20.aseprite` | gota, brilho, contorno | 1.130.0 |
| vital-vigor (o Vigor do topo) | `vital-vigor/vital-vigor-20.aseprite` | pulso, dedos, polegar, dobras, contorno | 1.131.0 |
| vital-foco (o Foco do topo) | `vital-foco/vital-foco-20.aseprite` | anel, marcas, centro, contorno | 1.131.0 |
| moedas (o Ouro do topo e do balcão) | `moedas/moedas-24.aseprite`, `-32` | pilha, topo, moeda, contorno | 1.132.0 (o 32, 1.133.0) |
| provisoes (as Provisões do topo e do mercado) | `provisoes/provisoes-24.aseprite`, `-32` | carne, osso, contorno | 1.132.0 |
| atalho-salvar (o Salvar da doca) | `atalho-salvar/atalho-salvar-36.aseprite`, `-32` | tampa, corpo, latao, seta, contorno | 1.129.0 |
| atalho-sair (o Sair da doca) | `atalho-sair/atalho-sair-36.aseprite`, `-32` | arco, passagem, seta, contorno | 1.129.0 |
| atalho-bestiario (o Bestiário da doca) | `atalho-bestiario/atalho-bestiario-36.aseprite`, `-32` | chifres, cranio, contorno | 1.128.0 |
| atalho-talentos (os Talentos da doca) | `atalho-talentos/atalho-talentos-36.aseprite`, `-32` | galhos, nos, contorno | 1.127.0 |
| atalho-comitiva (a Comitiva da doca) | `atalho-comitiva/atalho-comitiva-36.aseprite`, `-32` | tras_esquerda, tras_direita, frente, contorno | 1.127.0 |
| atalho-grimorio (o Grimório da doca e o Habilidades da luta) | `atalho-grimorio/atalho-grimorio-36.aseprite`, `-32` | contracapa, folhas, lombada, capa, emblema, cravos, fita, contorno | 1.126.0 |
| atalho-diario (o Diário da doca) | `atalho-diario/atalho-diario-36.aseprite`, `-32` | capa, paginas, anotacoes, fita, pena, contorno | 1.125.0 |
| atalho-mapa (o Mapa da doca) | `atalho-mapa/atalho-mapa-36.aseprite`, `-32` | espessura, papel, vincos, terreno, percurso, destino, contorno | 1.124.0 |
| aljava (a aljava do Patrulheiro e as flechas do topo) | `aljava/aljava-24.aseprite`, `-32`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | alca, couro, cintas, latao, boca, hastes, penas, contorno | 1.122.0 |
| attr-agilidade (a Agilidade e o Fugir) | `attr-agilidade/attr-agilidade-24.aseprite`, `-32`; **o 64 é o 32 ampliado 2×** | rastros, sola, bota, dobra, tira, fivela, contorno | 1.121.0 |

A varinha é a aprovada pelo Jean (commit `451ff11`): a haste com o mesmo perfil nos quatro tamanhos e a pedra
compacta (quadrada, de cantos cortados) também no 32. A camada `garras` do 32 fica vazia (lá a garra é um pixel da
taça). As rodadas, as tentativas descartadas e as fotos estão em `ferramentas/prototipos/hud/varinha-aseprite/`
(histórico: os `.aseprite` de lá são cópias das rodadas, não a fonte).

O gibão e as botas são os aprovados pelo Jean na rodada 2 (commit `9d49726`). Neste lote, **o 32 é a fonte do 64**:
o 64 do jogo é o 32 final ampliado exatamente 2× por vizinho mais próximo, sem retoque (a escolha do Jean depois de
comparar no cartão do saque). Os 64 desenhados à parte (`historico/gibao-64-trabalhado.aseprite`,
`historico/bota-64-trabalhado.aseprite`) ficam como histórico, fora da exportação. As rodadas estão em
`ferramentas/prototipos/hud/couro-aseprite/`.

A cabeça e as mãos de couro e de tecido são as aprovadas pelo Jean (registro em `df01f5a`): o capuz de couro revisado
(rodada 2), a luva de couro com braçadeira (rodada 1), a luva de seda (rodada 2) e o capuz de tecido da rodada 3
(`1c061e1`); os 32 são cópias exatas dessas fontes e o 64 de cada um é o 32 ampliado 2×. Os 40 e 48 (rodada 4) saem da
mesma construção de cada peça, escrita para qualquer grade (`ferramentas/prototipos/hud/couro2-aseprite/auxiliares/
couro2_r4.py`, que no 32 reproduz o aprovado pixel a pixel), pintados pelo `pintar.lua`. As rodadas estão em
`ferramentas/prototipos/hud/couro2-aseprite/`.

**Cuidado com a linha de comando e o conector:** cada `aseprite -b` (o exportador, a conferência) carrega também a
extensão do MCP, que se conecta ao mesmo canal (`ws://127.0.0.1:6515`) e o fecha ao sair; o editor aberto perde o
conector até ser reiniciado. Pinte e confira pelo editor primeiro; exporte pela linha de comando por último.

## Exportar os PNGs e os @2x

    python ferramentas/arte/exportar_aseprite.py varinha             # grava no jogo (só na integração ou num ajuste aprovado)
    python ferramentas/arte/exportar_aseprite.py varinha <pasta>     # grava numa pasta qualquer (uma proposta)
    python ferramentas/arte/exportar_aseprite.py varinha --conferir  # compara com os do jogo, byte a byte e pixel a pixel

    python ferramentas/arte/exportar_aseprite.py gibao               # o gibão: 32, 40, 48 das fontes e o 64 derivado
    python ferramentas/arte/exportar_aseprite.py todas --conferir    # todas as peças: reproduz e compara os 24 arquivos

O 1× sai da linha de comando do Aseprite (`-b <fonte> --save-as <png>`: o composto das camadas visíveis); o @2x é a
duplicação exata do 1× (vizinho mais próximo, pelo Pillow), como o `salvar` de `../pixel_comum.py`. O executável vem
de `ASEPRITE=<executável>`, de `aseprite` no PATH ou do lugar de instalação comum (Steam). Na integração da 1.109.0, os
oito arquivos exportados saíram idênticos, byte a byte, aos aprovados.

Os tamanhos derivados são explícitos por peça na tabela `DERIVADOS` do exportador (lado: lado da fonte e fator
inteiro): no gibão e nas botas, `64: (32, 2)`. O derivado sai do PNG exportado da fonte, ampliado pelo vizinho mais
próximo, e o @2x dele é a duplicação exata. Uma peça fora da tabela (a varinha) exporta cada fonte que tem. O
`--conferir` reproduz todos os arquivos numa pasta temporária, compara com os do jogo e confere que cada derivado,
reduzido pegando um pixel de cada bloco, volta exatamente à fonte. Na integração da 1.110.0, os dezesseis arquivos do
couro saíram idênticos, byte a byte, aos escolhidos.

Mexeu numa fonte? Exporte para uma pasta, confira em tamanho real (`../prancha.py`) e no jogo
(`../fotografar_itens.mjs`, `SO=varinha`), e só então grave no jogo.

## Pintar pelo MCP: `pintar.lua`

`pintar.lua` é o caminho de pintura verificado para o conector `aseprite-mcp-bridge` (extensão 1.0.0), pelo
`execute_script`:

    local P = dofile("<raiz>/ferramentas/arte/aseprite/pintar.lua")
    return P.pintar("haste", "12,30,7A3824;13,29,974B31")     -- ou P.pintar_arquivo("haste", "<lista>.lua")
    return P.ler("haste")                                      -- os opacos da camada, em coordenadas do documento
    return P.camadas()                                         -- ordem, nome, visibilidade, pixels de cada camada

Por que não o `put_pixels` do conector (medido em 16/10/2026): ele descarta em silêncio o pixel fora do retângulo da
cel (a cel que o lápis do Aseprite cria, uma cel deslocada ou parcialmente fora da tela) e responde com o total
pedido; e escreve sem gerar desfazer. O `pintar.lua` cria uma imagem que cobre a cel antiga e a tela, copia o conteúdo
no mesmo lugar do documento, pinta por cima e troca a imagem da cel numa transação (um passo de desfazer); recusa e
lista o pixel fora da tela; relê cada pixel depois de gravar.

Cuidados: as listas entram por `dofile` (um `.lua` que só faz `return "<lista>"`); `io.open` e `sprite:saveCopyAs`
para PNG num `execute_script` abrem uma janela do Aseprite e travam o conector. Para exportar, use a ferramenta
`export_png` do conector ou o `exportar_aseprite.py`.

A Calça de Couro (1.119.0) é a aprovada pelo Jean no commit `ee0f01a`. As camadas saem de
`ferramentas/arte/desenhar_calca_couro_pixel.py --listas` e foram montadas pela linha de comando do Aseprite
(`ferramentas/prototipos/hud/itens-lote-noite/calca_couro/montar_fontes.sh`, com o `pintar.lua`). Os oito arquivos do
jogo são idênticos, pixel a pixel, aos aprovados, e `exportar_aseprite.py calca_couro --conferir` os reproduz byte a
byte.

## Montar as fontes a partir de um script de desenho (1.120.0)

Quando o desenho nasce num script de `ferramentas/arte/` (o método de `pixel_comum.py`), a fonte em camadas sai dele:

    python ferramentas/arte/desenhar_attr_ataque_pixel.py <pasta> --listas   # as listas por camada (pixel_comum.listas_camadas)
    python ferramentas/arte/montar_fontes.py attr-ataque <pasta>/listas      # aseprite/attr-ataque/attr-ataque-<lado>.aseprite
    python ferramentas/arte/exportar_aseprite.py attr-ataque --conferir      # o composto exportado = o jogo, byte a byte

- **As listas:** o script marca a camada de cada pixel (as `CAMADAS` dele). `listas_camadas` grava um `.lua` por
  camada e a ordem (`ordem.txt`).
- **A montagem:** `montar_fontes.py` roda o Aseprite em lote (`aseprite/montar_camadas.lua`, com o `pintar.lua`) para
  cada tamanho e mostra a releitura de cada camada.
- **Os espaços no caminho:** com um espaço no caminho do script, o Aseprite não o executa e não avisa. O
  `montar_fontes.py` copia o `.lua` para uma pasta temporária e passa o `pintar.lua` por parâmetro.
- **Na integração da 1.120.0:** os doze arquivos de Ataque e Defesa exportados das fontes saíram idênticos, pixel a
  pixel, aos aprovados (`b8637d0`).
- **A calça de couro:** foi montada pela versão de protótipo deste fluxo (`itens-lote-noite/calca_couro/`).

## A Agilidade (1.121.0)

A bota em passada é a aprovada pelo Jean (`e9b0499`, a sola corrigida). As fontes vieram do protótipo
(`ferramentas/prototipos/hud/itens-lote-noite/agilidade_aljava_ref/`), desenhadas em grade à mão e pintadas no editor
pelo `pintar.lua`. Os seis arquivos exportados delas são idênticos, byte a byte, aos aprovados, e
`exportar_aseprite.py attr-agilidade --conferir` os reproduz.

## A aljava (1.122.0)

**A origem:** é a direção nova, feita a partir da referência do Jean (`ferramentas/prototipos/hud/itens-lote-noite/
agilidade_aljava_ref/`):
- 24 e 32 aprovados em `ea3835f`;
- 40 e 48, derivados da construção do 32, em `fb403f5`;
- o 64 é o 32 ampliado 2×.

**As fontes:** desenhadas em grade à mão e pintadas no editor pelo `pintar.lua`. Os dez arquivos exportados delas são
idênticos, byte a byte, aos aprovados.

**O script antigo:** `desenhar_aljava_pixel.py` é a direção anterior, guardada como histórico, e só grava numa pasta.

## O Poder (1.123.0)

A chama violeta é a da rodada 2, aprovada pelo Jean (`c0dbab8`, `ferramentas/prototipos/hud/itens-lote-noite/poder_r2/`).
Foi desenhada em grade à mão e pintada no editor pelo `pintar.lua`. Os seis arquivos exportados das fontes são
idênticos, byte a byte, aos aprovados, e `exportar_aseprite.py attr-poder --conferir` os reproduz. O
`desenhar_attr_poder_pixel.py` é o candidato anterior, não aprovado, e fica como histórico: só grava numa pasta.

## O Inventário e o Mapa da doca (1.124.0)

Os primeiros atalhos da doca em pixel art: a mochila e o mapa dobrado da rodada 2. Jean os aprovou no `c02e566`, e eles
estão em `ferramentas/prototipos/hud/itens-lote-noite/doca_r2/`.

**As fontes:** o 36 (o da doca) e o 32 (as janelas estreitas), sem tamanho derivado. Foram desenhadas em grade à mão;
a camada de cada pixel vem do mapa de camadas, e a pintura no editor foi pelo `pintar.lua`.

**Conferido:** os oito arquivos exportados delas são idênticos, byte a byte, aos aprovados, e
`exportar_aseprite.py atalho-inventario --conferir` (e `atalho-mapa`) os reproduz. O `desenhar_doca_pixel.py` é a
primeira proposta, recusada, e fica como histórico.

## O Diário da doca (1.125.0)

O livro aberto com a pena e a fita é o da rodada 3 da doca, aprovado pelo Jean no `666b806`
(`ferramentas/prototipos/hud/itens-lote-noite/doca_r3/`). Tem o 36 e o 32, sem derivado. Os quatro arquivos exportados
das fontes são idênticos, byte a byte, aos aprovados, e `exportar_aseprite.py atalho-diario --conferir` os reproduz.

## O Grimório da doca (1.126.0)

O livro violeta fechado e inclinado, com a estrela de latão, é a rodada 3 da doca, aprovada pelo Jean no `61dcb81`
(`ferramentas/prototipos/hud/itens-lote-noite/doca_r3/`; o modelo do livro está em `auxiliares/grimorio_livro.py`).
- **Os usos:** o atalho da doca e o comando Habilidades da roda da luta (`ACAO.grimorio`, o 32).
- **Conferido:** os quatro arquivos exportados das fontes são idênticos, byte a byte, aos aprovados, e
  `exportar_aseprite.py atalho-grimorio --conferir` os reproduz.
- **As rodadas recusadas** estão no protótipo: `doca_r3/grimorio_r1/` e `grimorio_r2/`.

## Os Talentos e a Comitiva da doca (1.127.0)

Os dois são da rodada 4 da doca, aprovada pelo Jean no `4deb386` (`ferramentas/prototipos/hud/itens-lote-noite/doca_r4/`).
- **Os arquivos:** os oito exportados das fontes são idênticos, byte a byte, aos aprovados, e `exportar_aseprite.py
  <peça> --conferir` os reproduz.
- **A Comitiva:** ganhou papel próprio em `Icones` (`ATALHO`, `TAMANHOS`). O contorno dela está desenhado na camada
  `contorno`, também entre as figuras.

## O Bestiário da doca (1.128.0)

O crânio de fera com chifres foi aprovado pelo Jean no `e373618` (`ferramentas/prototipos/hud/itens-lote-noite/doca_r5/`).
- **As fontes:** são as `.aseprite` editadas no editor pelo MCP. As rodadas 3 e 4 (a parte de baixo e a ligação entre o
  focinho e a arcada) foram retocadas nelas, e as grades do protótipo ficam como histórico.
- **Conferido:** os quatro arquivos exportados são idênticos, byte a byte, aos aprovados, e
  `exportar_aseprite.py atalho-bestiario --conferir` os reproduz.

## O Salvar e o Sair da doca (1.129.0): a doca concluída

O baú aberto e o arco de pedra foram aprovados pelo Jean (`a872915`, reapresentados sem mudança no `682b189`;
`ferramentas/prototipos/hud/itens-lote-noite/doca_r5/`).
- **Conferido:** os oito arquivos exportados das fontes são idênticos, byte a byte, aos aprovados.
- **A doca:** com eles, os nove atalhos estão em pixel art: Talentos, Grimório, Inventário, Comitiva, Mapa, Diário,
  Bestiário, Salvar e Sair.

## A Vida e a Mana do topo (1.130.0)

O coração (`a914f18`) e a gota sem o miolo aceso (`f02566d`) foram aprovados pelo Jean
(`ferramentas/prototipos/hud/itens-lote-noite/vida_mana/`; a gota da rodada 1 em `vida_mana/mana_r1/`).
- **O uso:** só o topo, em 20 (`Icones.vital`); não há outro tamanho.
- **Conferido:** os quatro arquivos exportados das fontes são idênticos, byte a byte, aos aprovados.
- **Os auxiliares** que geraram as listas por camada ficam em `vida_mana/auxiliares/` (`vida.py`, `mana.py`).

## O Vigor e o Foco do topo (1.131.0): os quatro recursos concluídos

O punho cerrado sem fogo (`4eea5b6`) e o alvo verde (`1a1dae3`, reapresentado sem mudança no `4eea5b6`) foram
aprovados pelo Jean (`ferramentas/prototipos/hud/itens-lote-noite/vigor_foco/`; as rodadas recusadas em
`vigor_foco/recusados/`).
- **O uso:** só o topo, em 20 (`Icones.vital`); não há outro tamanho.
- **Conferido:** os quatro arquivos exportados das fontes são idênticos, byte a byte, aos aprovados.
- **Os auxiliares** que geraram as listas por camada ficam em `vigor_foco/auxiliares/` (`punho/`: `e2_partes.py` e
  depois `e3_sem_fogo.py`; `foco.py`).
- **Com eles,** os quatro ícones das barras do topo (Vida, Mana, Vigor, Foco) estão em pixel art.

## O Ouro e as Provisões (1.132.0)

A pilha de moedas e o pernil sem barbantes foram aprovados pelo Jean no `33d8a6c`
(`ferramentas/prototipos/hud/itens-lote-noite/ouro_provisoes/`; a versão com barbantes em `ouro_provisoes/recusados/`).
- **As fontes:** `moedas/moedas-24.aseprite` (camadas pilha, topo, moeda, contorno) e `provisoes/provisoes-24.aseprite`,
  `-32` (carne, osso, contorno).
- **Os usos:** o Ouro no topo, em 24; as Provisões no topo, em 24, e no cartão do mercado, em 32 nativo (`TAMANHOS`
  [24, 32]).
- **O Ouro do balcão (1.133.0):** o seu ouro no mercado e nos serviços (`.ouro-loja`, 32) passou do sprite `moedas` do
  jogo para a pilha aprovada, com uma fonte de 32 (`moedas/moedas-32.aseprite`, as mesmas quatro camadas) derivada da
  construção do 24: as medidas escaladas por 4/3 e as moedas da pilha com 3 px de altura em vez de 2. As listas saem do
  `ouro_provisoes/auxiliares/ouro.py final 32` (que no 24 reproduz o aprovado pixel a pixel), pintadas pelo
  `pintar.lua` (0 diferentes, 0 fora da tela); o composto do editor, as listas e o exportado são iguais, e o @2x é a
  duplicação exata. Sem retoque.
- **Conferido:** os seis arquivos exportados das fontes são idênticos, byte a byte, aos aprovados, e
  `exportar_aseprite.py moedas|provisoes --conferir` os reproduz.
- **Os auxiliares** que geraram as listas por camada ficam em `ouro_provisoes/auxiliares/` (`ouro.py`, `pernil.py`).
