from PIL import Image
PAL = {
 # pele
 "a": "#5A3424", "b": "#8E5A3C", "c": "#C08A62", "d": "#E0B088",
 # o manto verde do da frente
 "1": "#1E2A16", "2": "#2E4020", "3": "#44592C", "4": "#5E763A", "5": "#7C944C",
 # o couro marrom (chapéu, cinto, bolsas)
 "e": "#2E1E13", "f": "#45301E", "g": "#604229", "h": "#7C5634", "i": "#986C42", "j": "#B48752",
 # o aço (ombreiras) e o pano vermelho escuro
 "m": "#2A3040", "n": "#4A5468", "o": "#7A869C", "p": "#B4BECC",
 "q": "#3A1414", "r": "#5E2020", "s": "#843028",
 # o latão (fivelas, broche) e o cajado
 "x": "#6A4A14", "y": "#B48A30", "z": "#F0D070",
 "A": "#40270C", "B": "#623C12", "C": "#8A571B", "D": "#AE7526", "E": "#CF9737", "F": "#E9BB5C", "G": "#F8DC94",
 "H": "#FFF6D8", "I": "#2A1A08", "J": "#164246", "K": "#2A8480", "L": "#62D2C0", "M": "#D4FFF2", # o osso (marfim) e o chifre
 "Q": "#2E2014", "R": "#5A4430", "S": "#8A704C", "T": "#B89C70", "U": "#DCC79A", "V": "#F4E8C8",
 "W": "#140C08", "X": "#3A2618", "Y": "#5E4028", "Z": "#8A6644", "k": "#B48E64",
 "t": "#8A1E14", "u": "#D8482A",
 "P": "#DCE6F0", "w": "#4A3018", "v": "#2A1A0C", "!": "#1C1A22", "#": "#36343E", "$": "#57555F", "%": "#76747E", "&": "#97959E", "@": "#BEBCC4",
 "6": "#7A300C", "7": "#C25A18", "8": "#F28A2A", "9": "#FFC070", "O": "#08080a"}
def contorno(g, n):
    forma = set(g); h = dict(g)
    for y in range(n):
        for x in range(n):
            if (x, y) not in h and any((x + dx, y + dy) in forma for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                h[(x, y)] = "O"
    return h
def imagem(h, n, nome):
    im = Image.new("RGBA", (n, n))
    for (x, y), c in h.items():
        if 0 <= x < n and 0 <= y < n: im.putpixel((x, y), tuple(int(PAL[c][i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    im.save(nome)
    open(nome.replace(".png", ".txt"), "w").write("\n".join("".join(h.get((x, y), ".") for x in range(n)) for y in range(n)) + "\n")
