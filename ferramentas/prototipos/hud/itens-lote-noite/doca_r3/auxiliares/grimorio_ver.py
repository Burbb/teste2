from PIL import Image
PAL = {**{str(i + 1): c for i, c in enumerate(["#1A0D28", "#2A1640", "#3E2258", "#553272", "#6E4690", "#8A5EAE", "#A87CC8", "#C49CDE"])},
       "r": "#8E7650", "p": "#BFA272", "q": "#E2CC9C", "s": "#F6E8C2",
       "a": "#5A3410", "b": "#9A5E1C", "c": "#D89A34", "d": "#F4C860", "e": "#FFF0B0",
       "R": "#6E1A12", "S": "#B23C1C", "T": "#E8682C", "O": "#08080a"}
def salvar(g, n, nome):
    forma = set(g); h = dict(g)
    for y in range(n):
        for x in range(n):
            if (x, y) not in h and any((x + dx, y + dy) in forma for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                h[(x, y)] = "O"
    im = Image.new("RGBA", (n, n))
    for (x, y), c in h.items():
        if 0 <= x < n and 0 <= y < n: im.putpixel((x, y), tuple(int(PAL[c][i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    im.save(nome)
    open(nome.replace(".png", ".txt"), "w").write("\n".join("".join(h.get((x, y), ".") for x in range(n)) for y in range(n)) + "\n")
