# Fontes em Aseprite

Os ícones cuja fonte final é um `.aseprite` em camadas, desenhado no Aseprite (pelo MCP ou à mão). O jogo nunca lê
nada daqui: só os PNGs exportados para `rpg/web/static/hud/icones/`.

## As fontes finais

| Peça | Arquivos | Camadas (de baixo para cima) | No jogo desde |
|---|---|---|---|
| varinha | `varinha/varinha-32.aseprite`, `-40`, `-48`, `-64` (RGBA, 1 quadro, fundo transparente) | pomo, empunhadura, anel, haste, taca, pedra, garras, contorno | 1.109.0 |

A varinha é a aprovada pelo Jean (commit `451ff11`): a haste com o mesmo perfil nos quatro tamanhos e a pedra
compacta (quadrada, de cantos cortados) também no 32. A camada `garras` do 32 fica vazia (lá a garra é um pixel da
taça). As rodadas, as tentativas descartadas e as fotos estão em `ferramentas/prototipos/hud/varinha-aseprite/`
(histórico: os `.aseprite` de lá são cópias das rodadas, não a fonte).

## Exportar os PNGs e os @2x

    python ferramentas/arte/exportar_aseprite.py varinha             # grava no jogo (só na integração ou num ajuste aprovado)
    python ferramentas/arte/exportar_aseprite.py varinha <pasta>     # grava numa pasta qualquer (uma proposta)
    python ferramentas/arte/exportar_aseprite.py varinha --conferir  # compara com os do jogo, byte a byte e pixel a pixel

O 1× sai da linha de comando do Aseprite (`-b <fonte> --save-as <png>`: o composto das camadas visíveis); o @2x é a
duplicação exata do 1× (vizinho mais próximo, pelo Pillow), como o `salvar` de `../pixel_comum.py`. O executável vem
de `ASEPRITE=<executável>`, de `aseprite` no PATH ou do lugar de instalação comum (Steam). Na integração da 1.109.0, os
oito arquivos exportados saíram idênticos, byte a byte, aos aprovados.

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
