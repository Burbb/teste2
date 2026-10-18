from PIL import Image
PAL = {**{str(i + 1): c for i, c in enumerate(["#1E130C", "#2E1E13", "#45301E", "#604229", "#7C5634", "#986C42", "#B48752", "#CFA36C"])},
       "x": "#5A3C12", "y": "#9C6E22", "z": "#DDB45C",
       "g": "#262B1A", "h": "#3E4628", "i": "#5C663C", "j": "#7E8A56", "k": "#A0AC74",
       "A": "#3E2E1A", "B": "#6E5634", "C": "#9C8052", "D": "#C4A874", "E": "#E2CC98", "F": "#F4E6C0",
       "v": "#7E8A52", "w": "#A4AC72", "a2": "#000000", "l": "#6E8C9C", "m": "#9CB4BC", "r": "#6A1C12", "s": "#B23A24", "t": "#E0603A", "O": "#08080a"}
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
