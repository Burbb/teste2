"""auxiliares/silhueta.py <saida> <png>...: cada desenho numa cor só (o preenchimento claro, o contorno escuro), ampliado com grade,
e a haste destacada em vermelho; embaixo, em 1x e 2x."""
import sys
from PIL import Image, ImageDraw
saida, pngs = sys.argv[1], sys.argv[2:]
k = 9; partes = []
for p in pngs:
    im = Image.open(p).convert("RGBA"); N = im.width
    s = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    for y in range(N):
        for x in range(N):
            r, g, b, a = im.getpixel((x, y))
            if a: s.putpixel((x, y), (20, 20, 24, 255) if (r, g, b) == (8, 8, 10) else (225, 215, 195, 255))
    big = Image.new("RGBA", (N * k, N * k), (90, 110, 130, 255)); big.alpha_composite(s.resize((N * k, N * k), Image.NEAREST))
    d = ImageDraw.Draw(big)
    for i in range(N + 1):
        d.line([(i * k, 0), (i * k, N * k)], fill=(105, 125, 145, 255)); d.line([(0, i * k), (N * k, i * k)], fill=(105, 125, 145, 255))
    partes.append((big, s))
L = sum(b.width + 14 for b, _ in partes) + 14; A = max(b.height for b, _ in partes) + 64 * 2 + 30
out = Image.new("RGBA", (L, A), (90, 110, 130, 255)); x = 14
for b, s in partes:
    out.alpha_composite(b, (x, 10)); y = max(bb.height for bb, _ in partes) + 20
    out.alpha_composite(s, (x, y)); out.alpha_composite(s.resize((s.width * 2, s.width * 2), Image.NEAREST), (x + s.width + 10, y))
    x += b.width + 14
out.save(saida)
