#!/bin/sh
# Monta as fontes em camadas da Calça de Couro (32, 40 e 48) no Aseprite, pela linha de comando, a partir das listas
# por camada que o desenhar_calca_couro_pixel.py grava (--listas). Rode da raiz do repositório:
#   sh ferramentas/prototipos/hud/itens-lote-noite/calca_couro/montar_fontes.sh
set -e
AQUI="ferramentas/prototipos/hud/itens-lote-noite/calca_couro"
A="${ASEPRITE:-/c/Program Files (x86)/Steam/steamapps/common/Aseprite/Aseprite.exe}"
TMP="$(mktemp -d)"
cp "$AQUI/montar_fontes.lua" "$TMP/montar_fontes.lua"
mkdir -p "$AQUI/fontes"
for n in 32 40 48; do
  "$A" -b --script-param n=$n \
    --script-param listas="$(cygpath -w "$PWD/$AQUI/proposta/listas/calca_couro-$n")" \
    --script-param saida="$(cygpath -w "$PWD/$AQUI/fontes/calca_couro-$n.aseprite")" \
    --script-param pintar="$(cygpath -w "$PWD/ferramentas/arte/aseprite/pintar.lua")" \
    --script "$(cygpath -w "$TMP/montar_fontes.lua")" 2>&1 | grep -v "MCP\|pixellab" || true
done
rm -rf "$TMP"
