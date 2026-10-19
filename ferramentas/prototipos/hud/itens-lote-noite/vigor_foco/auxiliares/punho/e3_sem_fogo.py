# etapa 3 (rodada 3): o punho sem o fogo, recentrado no quadro de 20. As camadas da etapa 2 andam 2 px para a direita
# e 2 para cima (o punho tinha ido para baixo e para a esquerda para dar lugar à labareda), e a base do pulso, que
# deixa de encostar na beira, fecha com o contorno. A forma e a luz não mudam. Grava as listas deslocadas e a prévia.
from PIL import Image
DX, DY = 2, -2
im = Image.new("RGBA", (20, 20))
for n in ("pulso", "dedos", "polegar", "dobras", "contorno"):
    pts = [p.split(",") for p in open(n + ".lua").read().split('"')[1].split(";")]
    pts = [(int(x) + DX, int(y) + DY, c) for x, y, c in pts]
    for x, y, c in pts: im.putpixel((x, y), tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    if n == "contorno":   # o fecho do pulso: embaixo de cada pixel da última linha do pulso
        pts += [(x, 18, "08080A") for x in range(20) if im.getpixel((x, 17))[3] and not im.getpixel((x, 18))[3]]
        for x, y, c in pts: im.putpixel((x, y), (8, 8, 10, 255)) if y == 18 else None
    open(n + "_r3.lua", "w").write('return "' + ";".join(f"{x},{y},{c}" for x, y, c in pts) + '"\n')
im.save("vigor20.png")
