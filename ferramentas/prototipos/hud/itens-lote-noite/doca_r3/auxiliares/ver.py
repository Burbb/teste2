from PIL import Image
PAL = {**{str(i + 1): c for i, c in enumerate(["#230B1C", "#33112A", "#451838", "#582046", "#6C2954", "#833563", "#9C4673"])},
       **{k: c for k, c in zip("abcdefg", ["#40270C", "#623C12", "#8A571B", "#AE7526", "#CF9737", "#E9BB5C", "#F8DC94"])},
       "r": "#9C7E4E", "p": "#C7A76B", "q": "#ECD9A9", "s": "#FFF5D6",
       "V": "#2E1180", "W": "#5A1FC8", "X": "#8A3CEA", "Y": "#BC5CF2", "Z": "#F2C8FC",
       "k": "#3A2414", "l": "#5E3C22", "m": "#86582E", "n": "#A87440", "o": "#C89458",
       "t": "#3C3A44", "u": "#8C8A96", "w": "#E8E4EC", "R": "#7A1E1A", "S": "#B83A2C", "h": "#6A5A48", "O": "#08080a"}
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
