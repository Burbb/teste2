"""Os retoques da G refinada (G2), seletivos, sobre as células da fonte da G (`g/aseprite/taverna-g.aseprite`): cada um
age só numa região marcada e só nos pixels que atrapalham a leitura; o resto da G (a câmera, o balcão, os objetos, a
luz, a textura da camisa) fica como está. As cores vêm da própria G (as que já estão na região, com a luz dela); nada
é pintado chapado por cima.

- `pele_lisa`: na testa e nos antebraços, o pixel solto do pontilhado da luz (diferente dos vizinhos, que concordam
  entre si) toma a cor dos vizinhos; as sombras, os relevos, o rosto e as bordas ficam.
- `mangas`: as rugas diagonais das mangas saem (elas cortavam o braço); entra uma dobra atravessando cada manga,
  perpendicular ao braço, acima do rolo, com a luz em cima. O pontilhado da camisa em volta fica.
- `pescoco`: a barba termina em pontas irregulares, não numa linha reta; embaixo dela, a sombra segue essas pontas; os
  lados do pescoço escurecem descendo para a gola. O pescoço não cresce: tudo acontece nos pixels que já são pescoço.
- `cabeca_e_prateleira`: a prateleira escurece até a sombra da parede nos dois pixels em volta da cabeça, onde a tábua
  encostava no cabelo; a prateleira continua inteira.
- `fregues_esquerda`: o freguês da esquerda refeito pela referência: a cabeça menor, afundada nos ombros, a capa
  larga subindo até o queixo, o perfil da barba e a orelha do lado do fogo; na G a cabeça era uma bola grande sobre um
  ombro pequeno (a observação do Jean). Continua uma silhueta escura, sem braço."""
import math

import numpy as np

# o taverneiro da G (g/taverneiro.py), nas coordenadas da cena
CX = 160
BRACOS = (((141, 50), (135, 66)), ((179, 50), (185, 66)))  # do ombro ao cotovelo
RUGAS_DA_G = (((137, 58), (140, 55)), ((139, 60), (142, 57)), ((183, 58), (180, 55)), ((181, 60), (178, 57)))


def _lum(c):
    return 0.3 * int(c[0]) + 0.59 * int(c[1]) + 0.11 * int(c[2])


def _pele(c):
    r, g, b = int(c[0]), int(c[1]), int(c[2])
    return c[3] and r > g > b and r - b > 50 and r > 90


def _camisa(c):
    r, g, b = int(c[0]), int(c[1]), int(c[2])
    return c[3] and r > 100 and abs(r - g) < 30 and r - b > 15 and r - b < 70 and g > 90


def _linha(a, b):
    (x0, y0), (x1, y1) = a, b
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    return [(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)]


def _maioria(a, x, y, aceita, fora=()):
    """A cor que a maioria dos 8 vizinhos aceitos tem (fora dos pixels em `fora`), ou None."""
    cores = {}
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if (dx or dy) and (x + dx, y + dy) not in fora:
                c = tuple(a[y + dy, x + dx])
                if aceita(c):
                    cores[c] = cores.get(c, 0) + 1
    return max(cores, key=cores.get) if cores else None


def pele_lisa(a):
    """O pontilhado da pele na testa e nos antebraços: o pixel solto (os dois vizinhos de um eixo iguais entre si e
    diferentes dele) toma a cor deles."""
    regioes = [(152, 17, 169, 26)]                     # a testa e a calva (acima das sobrancelhas)
    for (_, cot), punho in zip(BRACOS, ((151, 62), (169, 62))):
        xs = sorted((cot[0], punho[0]))
        regioes.append((xs[0] - 5, 57, xs[1] + 2, 72))  # o antebraço, do cotovelo ao punho
    n = 0
    for x0, y0, x1, y1 in regioes:
        orig = a.copy()
        for y in range(y0, y1):
            for x in range(x0, x1):
                c = tuple(orig[y, x])
                if not _pele(c):
                    continue
                for (ax, ay), (bx, by) in (((x - 1, y), (x + 1, y)), ((x, y - 1), (x, y + 1))):
                    p, q = tuple(orig[ay, ax]), tuple(orig[by, bx])
                    if p == q and p != c and _pele(p) and abs(_lum(p) - _lum(c)) < 22:
                        a[y, x] = p
                        n += 1
                        break
    return n


def mangas(a):
    """As rugas diagonais da G saem; uma dobra atravessa cada manga, perpendicular ao braço, acima do rolo."""
    n = 0
    rugas = {p for r in RUGAS_DA_G for p in _linha(*r)}
    for x, y in sorted(rugas):
        c = _maioria(a, x, y, _camisa, fora=rugas)
        if c is not None:
            a[y, x] = c
            n += 1
    for ombro, cotovelo in BRACOS:
        (ax, ay), (bx, by) = ombro, cotovelo
        comp = math.hypot(bx - ax, by - ay)
        dx, dy = (bx - ax) / comp, (by - ay) / comp
        nx, ny = -dy, dx
        caixa = a[ay - 6:by + 2, min(ax, bx) - 8:max(ax, bx) + 8].reshape(-1, 4)
        tons = sorted({tuple(c) for c in caixa if _camisa(c)}, key=_lum)
        escuro, claro = tons[0], tons[-1]
        for t, curva in ((0.62, 1.4),):
            cx, cy = ax + (bx - ax) * t, ay + (by - ay) * t
            r = 7 - t
            feitos = set()
            for k in range(-8, 9):
                s = k / 8
                x = round(cx + nx * s * r * 0.7 + dx * curva * (1 - s * s) - 0.5)
                y = round(cy + ny * s * r * 0.7 + dy * curva * (1 - s * s) - 0.5)
                if (x, y) in feitos or not (_camisa(a[y, x]) and _camisa(a[y - 1, x])):
                    continue
                feitos.add((x, y))
                a[y, x] = escuro
                a[y - 1, x] = claro if (x, y - 1) not in feitos else a[y - 1, x]
                n += 1
    return n


def pescoco(a):
    """A barba em pontas irregulares sobre o pescoço, a sombra embaixo seguindo as pontas, os lados do pescoço
    escurecendo para a gola."""
    def barba(c):
        return c[3] and _lum(c) < 75 and not _pele(c) and int(c[0]) < 110
    n = 0
    fundo_barba = {}
    for x in range(CX - 7, CX + 8):
        ys = [y for y in range(32, 44) if barba(a[y, x])]
        if ys:
            fundo_barba[x] = max(ys)
    tons = sorted({tuple(a[y, x]) for x in range(CX - 7, CX + 8) for y in range(38, 45) if _pele(a[y, x])}, key=_lum)
    escura, sombra = tons[0], tons[min(1, len(tons) - 1)]
    cor_barba = tuple(a[fundo_barba[CX], CX]) if CX in fundo_barba else None
    # as pontas: a barba desce um pixel em algumas colunas, espalhadas (sem ponta no meio)
    for x, extra in ((CX - 5, 1), (CX - 2, 1), (CX + 1, 1), (CX + 4, 1)):
        if x in fundo_barba and cor_barba is not None:
            for k in range(1, extra + 1):
                y = fundo_barba[x] + k
                if _pele(a[y, x]):
                    a[y, x] = cor_barba
                    n += 1
            fundo_barba[x] += extra
    # a sombra embaixo, seguindo as pontas (não uma faixa reta: só onde a barba acaba sobre a pele)
    for x, yb in fundo_barba.items():
        y = yb + 1
        if _pele(a[y, x]):
            a[y, x] = escura if abs(x - CX) < 5 else sombra
            n += 1
    # os lados do pescoço, escurecendo para a gola
    for y in range(39, 44):
        for x in (CX - 7, CX - 6, CX + 6, CX + 7):
            if _pele(a[y, x]) and (x > CX or y > 40):
                a[y, x] = sombra if x < CX else escura
                n += 1
    return n


def cabeca_e_prateleira(fundo, tav, prateleira=(26, 31), folga=2):
    """A tábua da prateleira escurece até a sombra da parede nos pixels perto da cabeça (a figura, acima dos ombros)."""
    corpo = tav[:, :, 3] > 0
    escuro = tuple(fundo[prateleira[1], 140])  # a sombra embaixo da tábua, longe da figura
    n = 0
    for y in range(prateleira[0], prateleira[1] + 1):
        for x in range(CX - 16, CX + 17):
            if corpo[y, x]:
                continue
            perto = corpo[max(0, y - folga):y + folga + 1, max(0, x - folga):x + folga + 1].any()
            if perto:
                fundo[y, x] = escuro
                n += 1
    return n


def _vulto_esquerda(px):
    """O freguês da esquerda refeito pela referência ("Taverneiro desconfiado atrás do balcão-1"): de três quartos de
    costas, virado para o balcão, a cabeça menor e afundada nos ombros, a capa subindo até o queixo, larga, com o capuz
    amontoado em volta do pescoço e as dobras descendo; do lado do fogo, o perfil da barba e a orelha. No escuro, com a
    lareira só no contorno. Sem braço nem rosto."""
    from g.desenho import QH
    _forma = px.t.poligono
    C = __import__("g.desenho", fromlist=["C"]).C
    # a capa: os ombros altos e largos, do canto até a borda de baixo
    _forma([(-1, 70), (6, 69), (14, 71), (22, 72), (30, 74), (38, 78), (45, 84), (50, 90), (53, QH), (-1, QH)],
           C["vulto"])
    # o capuz amontoado em volta do pescoço, um tom acima, e as dobras da capa
    _forma([(-1, 67), (8, 65), (18, 67), (25, 72), (19, 77), (7, 76), (-1, 74)], C["vultoMeio"])
    px.linha(21, 78, 40, 93, "vultoMeio")
    px.linha(9, 78, 20, 95, "vultoMeio")
    for x, y in ((19, 67), (22, 69), (24, 71), (31, 75), (36, 77), (41, 81)):  # a lareira no alto da capa
        px.p(x, y, "vultoLuz")
    # a cabeça, menor, afundada no capuz
    px.elipse(12, 60, 7.5, 8.5, "vulto")
    for y in range(51, 69):  # o contorno aceso do lado do fogo e no alto
        for x in range(3, 21):
            d = ((x + 0.5 - 12) / 7.5) ** 2 + ((y + 0.5 - 60) / 8.5) ** 2
            if 0.68 < d <= 1 and (x > 13 or y < 54):
                px.p(x, y, "vultoLuz")
    for x, y in ((8, 54), (11, 53), (6, 57), (14, 55)):  # o crespo do cabelo
        px.p(x, y, "vultoMeio")
    # o perfil da barba e da bochecha, do lado do balcão, e a orelha
    for y, (x0, x1) in ((60, (18, 20)), (61, (18, 21)), (62, (18, 21)), (63, (17, 21)), (64, (17, 21)), (65, (16, 20)),
                        (66, (15, 19)), (67, (14, 18))):
        for x in range(x0, x1):
            px.p(x, y, "vultoMeio")
        px.p(x1 - 1, y, "vultoLuz")
    px(19, 59, 2, 1, "#3a2416")  # a maçã do rosto, contra o fogo
    px(15, 58, 2, 3, "#3a2416")  # a orelha
    px.p(15, 59, "vultoMeio")


def fregues_esquerda(frente):
    """Troca o freguês da esquerda da G pelo refeito (`_vulto_esquerda`): onde o da G estava, volta o que fica atrás dele
    (o balcão, pelo desenho da G, com a luz dela); por cima, o novo, com a mesma luz."""
    from tela_h2 import Tela
    from g import desenho as G
    antigo = Tela(320, 96)
    G.fregues_esquerda(G.Pincel(antigo))
    atras = Tela(320, 96)
    pa = G.Pincel(atras)
    G.balcao(pa)
    G.caneca_do_fregues(pa)
    G.luz(atras)
    novo = Tela(320, 96)
    _vulto_esquerda(G.Pincel(novo))
    G.luz(novo)
    tirar = antigo.a[:, :, 3] > 0
    frente[tirar] = atras.a[tirar]
    por = novo.a[:, :, 3] > 0
    frente[por] = novo.a[por]
    return int(tirar.sum() + por.sum())


def aplicar(q):
    """{camada: [imagem, ...]} da G → as mesmas camadas com os retoques da G2 (cópias; a G não muda)."""
    from PIL import Image
    tav = np.array(q["taverneiro"][0].convert("RGBA"))
    fundo = np.array(q["fundo"][0].convert("RGBA"))
    frente = np.array(q["frente"][0].convert("RGBA"))
    feitos = {"pele": pele_lisa(tav), "mangas": mangas(tav), "pescoco": pescoco(tav),
              "prateleira": cabeca_e_prateleira(fundo, tav), "fregues": fregues_esquerda(frente)}
    novo = dict(q)
    novo["taverneiro"] = [Image.fromarray(tav, "RGBA")]
    novo["fundo"] = [Image.fromarray(fundo, "RGBA")]
    novo["frente"] = [Image.fromarray(frente, "RGBA")]
    return novo, feitos
