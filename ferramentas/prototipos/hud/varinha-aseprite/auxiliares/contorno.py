"""Lê o RLE do get_region (Aseprite via MCP) e devolve o lote do contorno: vizinhos vazios (4 lados) da forma."""
import sys, json
d = json.loads(open(sys.argv[1]).read()); W, H = d["width"], d["height"]
cheio, ja = set(), set()
for y, linha in enumerate(d["rows"].split("|")):
    x = 0
    for run in linha.split(";"):
        n, c = run.split(","); n = int(n)
        if c == "08080A":
            ja |= {(x + i, y) for i in range(n)}
        elif c != "000000":
            cheio |= {(x + i, y) for i in range(n)}
        x += n
ext = sorted({(x+dx, y+dy) for x, y in cheio for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))
              if (x+dx, y+dy) not in cheio and (x+dx, y+dy) not in ja and 0 <= x+dx < W and 0 <= y+dy < H}, key=lambda p: (p[1], p[0]))
print(";".join(f"{x},{y},08080A" for x, y in ext))
print(len(ext), file=sys.stderr)
