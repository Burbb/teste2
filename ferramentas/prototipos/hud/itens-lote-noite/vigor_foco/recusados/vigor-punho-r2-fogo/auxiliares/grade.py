# auxiliar: uma grade de letras (20x20) vira listas por camada para o pintar.lua; o contorno automático por fora
import sys, json
def listas(grade, cores, camadas, contorno_auto=True, saida="."):
    g = {}
    for y, linha in enumerate(grade):
        for x, ch in enumerate(linha):
            if ch != ".": g[(x, y)] = ch
    if contorno_auto:
        forma = {k for k, v in g.items() if v != "O"}
        for y in range(20):
            for x in range(20):
                if (x, y) not in g and any((x + dx, y + dy) in forma for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    g[(x, y)] = "O"
    por = {}
    for (x, y), ch in sorted(g.items()):
        por.setdefault(camadas[ch], []).append(f"{x},{y},{cores[ch]}")
    for cam, itens in por.items():
        open(f"{saida}/{cam}.lua", "w").write('return "' + ";".join(itens) + '"\n')
    return g, por
