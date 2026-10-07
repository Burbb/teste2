"""Desenho do mapa do reino em caracteres.

`renderizar` devolve uma lista de linhas; cada linha é uma lista de pedaços
(texto, cor). A interface clássica pinta com ANSI e a interface Textual
converte para objetos Rich.
"""

from .dados import BIOMAS
from .mundo import nivel_regiao

GLIFO_BIOMA = {"floresta": "♣", "pantano": "≈", "montanha": "▲", "planicie": "∴", "ruinas": "Π", "cidadela": "♜"}
GLIFO_TIPO = {"vila": "⌂", "cidadela": "♜"}
COR_BIOMA = {"floresta": "verde", "pantano": "ciano", "montanha": "branco", "planicie": "amarelo",
             "ruinas": "magenta", "cidadela": "vermelho"}


def conhecidos(g):
    """Lugares visitados e seus vizinhos (você sabe para onde as estradas levam)."""
    locais = g.mundo["locais"]
    ids = {l["id"] for l in locais if l["visitado"]}
    for l in locais:
        if l["visitado"]:
            ids |= {int(i) for i in l["con"]}
    return ids


def covil_conhecido(g, loc):
    return loc["tipo"] == "covil" and (loc["visitado"] or g.flag(f"conhecido:{loc['id']}"))


def glifo(g, loc):
    if loc["tipo"] in GLIFO_TIPO:
        return GLIFO_TIPO[loc["tipo"]]
    if covil_conhecido(g, loc):
        return "✓" if loc["guardiao"]["derrotado"] else "☠"
    return GLIFO_BIOMA[loc["bioma"]]


def descricao(g, loc):
    if loc["tipo"] == "vila":
        tipo = "vila"
    elif loc["tipo"] == "cidadela":
        tipo = "CIDADELA" + ("" if len(g.j.sigilos) >= 3 else " (selada)")
    else:
        tipo = BIOMAS[loc["bioma"]]["nome"]
        if covil_conhecido(g, loc):
            tipo += ", covil" + (" derrotado" if loc["guardiao"]["derrotado"] else f" de {loc['guardiao']['nome']}")
    return tipo


def _posicao(loc, largura, altura):
    return round(loc["x"] * (largura - 4)) + 1, round(loc["y"] * (altura - 1))


def _linha(x0, y0, x1, y1):
    """Bresenham: devolve [(x, y, caractere)] sem as pontas."""
    pontos = []
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    x, y = x0, y0
    while (x, y) != (x1, y1):
        e2 = 2 * err
        mx = my = 0
        if e2 >= dy:
            err += dy
            x += sx
            mx = sx
        if e2 <= dx:
            err += dx
            y += sy
            my = sy
        if (x, y) == (x1, y1):
            break
        if mx and my:
            ch = "╲" if mx == my else "╱"
        elif mx:
            ch = "─"
        else:
            ch = "│"
        pontos.append((x, y, ch))
    return pontos


def renderizar(g, largura=66, altura=18):
    locais = g.mundo["locais"]
    vistos = conhecidos(g)
    atual = g.loc["id"]
    vizinhos_atuais = {int(i) for i in g.loc["con"]}
    tela = [[(" ", None) for _ in range(largura)] for _ in range(altura)]

    # Estradas primeiro, depois os lugares por cima.
    for loc in locais:
        for vid in loc["con"]:
            outro = locais[int(vid)]
            if loc["id"] > outro["id"] or loc["id"] not in vistos or outro["id"] not in vistos:
                continue
            x0, y0 = _posicao(loc, largura, altura)
            x1, y1 = _posicao(outro, largura, altura)
            if atual in (loc["id"], outro["id"]):
                cor = "amarelo"
            elif loc["visitado"] and outro["visitado"]:
                cor = "branco"
            else:
                cor = "cinza"
            for x, y, ch in _linha(x0, y0, x1, y1):
                if 0 <= y < altura and 0 <= x < largura:
                    tela[y][x] = (ch, cor)

    for loc in locais:
        if loc["id"] not in vistos:
            continue
        x, y = _posicao(loc, largura, altura)
        rotulo = str(loc["id"] + 1)
        if loc["id"] == atual:
            simbolo, cor = "@", "amarelo+negrito"
        else:
            simbolo = glifo(g, loc)
            if loc["tipo"] == "covil" and covil_conhecido(g, loc) and not loc["guardiao"]["derrotado"]:
                cor = "vermelho+negrito"
            elif loc["tipo"] == "vila":
                cor = "ciano+negrito"
            else:
                cor = COR_BIOMA[loc["bioma"]] if loc["visitado"] else "cinza"
            if loc["id"] in vizinhos_atuais:
                cor += "+negrito"
        tela[y][x] = (simbolo, cor)
        cor_rotulo = "amarelo" if loc["id"] in vizinhos_atuais else ("cinza" if not loc["visitado"] else None)
        for i, ch in enumerate(rotulo):
            if x + 1 + i < largura:
                tela[y][x + 1 + i] = (ch, cor_rotulo)

    # Junta caracteres vizinhos de mesma cor para desenhar mais rápido.
    linhas = []
    for linha in tela:
        pedacos = []
        for ch, cor in linha:
            if pedacos and pedacos[-1][1] == cor:
                pedacos[-1] = (pedacos[-1][0] + ch, cor)
            else:
                pedacos.append((ch, cor))
        linhas.append(pedacos)
    return linhas


def legenda(g, apenas_vizinhos=False):
    """Entradas da legenda: (rótulo, texto, cor)."""
    locais = g.mundo["locais"]
    vistos = conhecidos(g)
    atual = g.loc["id"]
    vizinhos_atuais = {int(i): d for i, d in g.loc["con"].items()}
    saida = []
    for loc in locais:
        if loc["id"] not in vistos or (apenas_vizinhos and loc["id"] not in vizinhos_atuais):
            continue
        nv = nivel_regiao(loc)
        texto = f"{glifo(g, loc)} {loc['nome']} — {descricao(g, loc)}"
        if loc["tipo"] != "vila":
            texto += f" · Nv.{nv}"
        if loc["id"] == atual:
            texto += "  ◄ você"
            cor = "amarelo+negrito"
        elif loc["id"] in vizinhos_atuais:
            d = vizinhos_atuais[loc["id"]]
            texto += f"  → {d} trecho{'s' if d > 1 else ''}"
            cor = "negrito"
        else:
            cor = None if loc["visitado"] else "cinza"
        saida.append((str(loc["id"] + 1), texto, cor))
    return saida


SIMBOLOS = "@ você  ⌂ vila  ♣ floresta  ≈ pântano  ▲ montanha  ∴ planície  Π ruínas  ☠ covil  ✓ covil vencido  ♜ cidadela"
