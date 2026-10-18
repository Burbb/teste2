from PIL import Image
PAL = {"1": "#1C2230", "2": "#3A4458", "3": "#6A768C", "4": "#8C98AC", "5": "#B8C2D0", "6": "#DDE4EC", "7": "#FFFFFF",
       "a": "#5A3A10", "b": "#9A6A1C", "c": "#D8A438", "d": "#F6DC80", "k": "#3A2010", "l": "#6A4024", "m": "#9A6438",
       "z": "#3A240C", "O": "#08080a"}
def salvar(g, n, nome, sem=""):
    forma = {k for k, c in g.items() if c not in sem}
    h = dict(g)
    for y in range(n):
        for x in range(n):
            if (x, y) not in h and any((x + dx, y + dy) in forma for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                h[(x, y)] = "O"
    im = Image.new("RGBA", (n, n))
    for (x, y), c in h.items():
        if 0 <= x < n and 0 <= y < n: im.putpixel((x, y), tuple(int(PAL[c][i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    im.save(nome)
    open(nome.replace(".png", ".txt"), "w").write("\n".join("".join(h.get((x, y), ".") for x in range(n)) for y in range(n)) + "\n")
    return h
