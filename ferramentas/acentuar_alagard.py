# Uso: python ferramentas/acentuar_alagard.py alagard.ttf rpg/web/static/fontes/alagard-pt.ttf   (pip install fonttools)
"""Acrescenta à Alagard (só ASCII) as letras acentuadas do português, desenhando os acentos no grid de pixels da
fonte (64 unidades por pixel) e montando cada letra como composição: a base mais o acento centralizado na tinta."""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib.tables._g_l_y_f import GlyphComponent, Glyph

U = 64
entrada, saida = sys.argv[1], sys.argv[2]
f = TTFont(entrada)
glyf, hmtx, cmap = f["glyf"], f["hmtx"], f.getBestCmap()
ordem = f.getGlyphOrder()

def novo_glifo(nome, pixels, avanco=0):
    pen = TTGlyphPen(None)
    for (x, y) in pixels:
        pen.moveTo((x * U, y * U)); pen.lineTo((x * U, (y + 1) * U)); pen.lineTo(((x + 1) * U, (y + 1) * U)); pen.lineTo(((x + 1) * U, y * U)); pen.closePath()
    g = pen.glyph(); glyf[nome] = g; hmtx[nome] = (avanco, 0)

# Acentos, com o pixel (0, 0) no canto de baixo à esquerda do acento.
ACENTOS = {
    "px_agudo": [(0, 0), (1, 1)],
    "px_grave": [(0, 1), (1, 0)],
    "px_circ": [(0, 0), (1, 1), (2, 0)],
    "px_til": [(0, 0), (1, 1), (2, 0), (3, 1)],
    "px_trema": [(0, 0), (2, 0)],
    "px_cedilha": [(1, 2), (2, 1), (0, 0), (1, 0)],
}
for nome, pxs in ACENTOS.items():
    novo_glifo(nome, pxs)
LARG = {"px_agudo": 2, "px_grave": 2, "px_circ": 3, "px_til": 4, "px_trema": 3, "px_cedilha": 3}

# i sem pingo: só os contornos de baixo do "i"
gs = f.getGlyphSet()
rec = DecomposingRecordingPen(gs); gs[cmap[ord("i")]].draw(rec)
contornos, atual = [], []
for op, args in rec.value:
    atual.append((op, args))
    if op in ("closePath", "endPath"): contornos.append(atual); atual = []
pen = TTGlyphPen(None)
for c in contornos:
    ys = [p[1] for op, a in c for p in a]
    if ys and max(ys) <= 512:
        for op, a in c: getattr(pen, op)(*a)
glyf["px_i_sem_pingo"] = pen.glyph(); hmtx["px_i_sem_pingo"] = hmtx[cmap[ord("i")]]

LETRAS = {  # letra: (base, acento)
    "á": ("a", "px_agudo"), "à": ("a", "px_grave"), "â": ("a", "px_circ"), "ã": ("a", "px_til"),
    "é": ("e", "px_agudo"), "ê": ("e", "px_circ"), "í": ("px_i_sem_pingo", "px_agudo"),
    "ó": ("o", "px_agudo"), "ô": ("o", "px_circ"), "õ": ("o", "px_til"), "ú": ("u", "px_agudo"), "ü": ("u", "px_trema"),
    "ç": ("c", "px_cedilha"),
    "Á": ("A", "px_agudo"), "À": ("A", "px_grave"), "Â": ("A", "px_circ"), "Ã": ("A", "px_til"),
    "É": ("E", "px_agudo"), "Ê": ("E", "px_circ"), "Í": ("I", "px_agudo"),
    "Ó": ("O", "px_agudo"), "Ô": ("O", "px_circ"), "Õ": ("O", "px_til"), "Ú": ("U", "px_agudo"), "Ç": ("C", "px_cedilha"),
}
novos = {}
for letra, (base, acento) in LETRAS.items():
    nome_base = base if base.startswith("px_") else cmap[ord(base)]
    gb = glyf[nome_base]; gb.recalcBounds(glyf)
    tinta = (gb.xMax - gb.xMin) // U  # largura da tinta em pixels
    col = gb.xMin // U + (tinta - LARG[acento] + 1) // 2
    if acento == "px_cedilha": dy = -3
    else: dy = (gb.yMax // U) + 1  # um pixel de folga acima da letra
    comp = Glyph(); comp.numberOfContours = -1; comp.components = []
    for nome, (x, y) in ((nome_base, (0, 0)), (acento, (col * U, dy * U))):
        c = GlyphComponent(); c.glyphName = nome; c.x, c.y = x, y; c.flags = 0x4 if nome == nome_base else 0; comp.components.append(c)
    nome = "uni%04X" % ord(letra)
    glyf[nome] = comp; hmtx[nome] = hmtx[nome_base]; novos[ord(letra)] = nome
f.setGlyphOrder(ordem)
for t in f["cmap"].tables:
    if t.isUnicode(): t.cmap.update(novos)
f["maxp"].numGlyphs = len(ordem)
if f["post"].formatType == 2.0: f["post"].extraNames = []; f["post"].mapping = {}
f.save(saida)
print("letras novas:", "".join(LETRAS))
