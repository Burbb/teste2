# A Sandália do Mago, rodada 2 (19/10/2026): o par em três quartos, visto um pouco de cima, pela referência do Jean
# (ferramentas/arte/referencias/botas/). Uma sandália é desenhada por formas no quadro de 32 (a mesma construção em 32,
# 40 e 48; o 64 é o 32 ampliado 2x): a palmilha clara com o contorno de um pé, a ponta embaixo à esquerda e o calcanhar
# em cima à direita; a sola baixa com a espessura embaixo; as tiras largas e inclinadas que sobem da beira de perto e
# passam por cima do espaço do pé (a ponta de cada uma passa da beira de longe: o volume do pé, vazio); o tornozelo,
# duas tiras largas em volta, presas pelo calcanhar e pela frente, com o vão por onde a perna entraria. O par: a de trás
# é a mesma, deslocada para cima e para a esquerda e um tom mais escura; o contorno separa a da frente. O couro é o
# das botas aprovadas; a palmilha, o couro cru.
# Uso: python sandalia_par.py <32|40|48> [silhueta] [uma] [<pasta>]. Grava a prévia e as listas em <pasta>/<N>/.
import pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6] / "ferramentas" / "arte"))
from pixel_comum import grade, contornar, imagem, limpar, listas_camadas

N = int(sys.argv[1]); ARGS = sys.argv[2:]
ETAPA = "silhueta" if "silhueta" in ARGS else "final"
UMA = "uma" in ARGS                                              # só a sandália da frente (a construção, antes do par)
SAIDA = pathlib.Path(next((a for a in ARGS if a not in ("silhueta", "uma")), "."))
K = N / 32
RAMPAS = {
    "k": ["#1E130C", "#3E2716", "#57381F", "#724B2A", "#8E6236", "#B08C62"],   # o couro (o das botas aprovadas)
    "p": ["#4A3A2C", "#7A6650", "#9E8A70", "#BFAA8C", "#D8C8A8"],              # a palmilha (o couro cru, gasto)
}
mat, tom, fixo, X, Y = grade(N)
cam = np.full((N, N), "", dtype=object)
x32, y32 = X / K, Y / K


def poligono(pts, dx=0.0, dy=0.0):
    dentro = np.zeros((N, N), bool)
    n = len(pts)
    for i in range(n):
        (xa, ya), (xb, yb) = pts[i], pts[(i + 1) % n]
        xa, xb, ya, yb = xa + dx, xb + dx, ya + dy, yb + dy
        cruza = ((ya > y32) != (yb > y32)) & (x32 < (xb - xa) * (y32 - ya) / ((yb - ya) or 1e-9) + xa)
        dentro ^= cruza
    return dentro


def pinta(onde, m, t, c):
    mat[onde] = m; tom[onde] = t if np.isscalar(t) else t[onde]; cam[onde] = c


def vizinhos(m):
    v = np.zeros_like(m)
    for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        v |= np.roll(np.roll(m, oy, 0), ox, 1)
    return v & ~m


# A sandália, no quadro de 32 (a da frente). A palmilha: a beira de longe, o calcanhar, a beira de perto e a ponta.
PALMILHA = [(7.0, 22.4), (9.4, 21.0), (13.0, 20.0), (18.0, 18.8), (22.6, 17.6), (26.4, 16.8), (28.6, 17.4), (29.2, 19.0),
            (28.4, 20.8), (24.0, 22.2), (19.0, 23.8), (15.0, 25.2), (11.0, 26.4), (8.0, 27.0), (5.8, 26.6), (5.0, 25.0)]
ESPESSURA = 1.9
# as tiras do pé: cada uma sobe da beira de perto, passa por cima do espaço do pé e desce na beira de longe (a perna
# de trás, mais escura): (o pé de perto, o alto, o pé de longe)
TIRAS = [((10.0, 25.8), (11.8, 19.4), (13.8, 20.3)), ((15.4, 24.3), (16.8, 16.8), (19.0, 18.9))]
LARG = 1.25                                                                   # a meia largura das tiras
# o tornozelo: a tira larga em volta (a elipse), a presa da frente e a do calcanhar
CT, RX, RY = (24.8, 10.8), 4.4, 2.6
PRESAS = [((21.6, 22.2), (21.0, 12.4)), ((28.6, 18.8), (29.0, 11.4))]


def faixa(pts, larg, dx, dy):
    """Os pixels perto da linha quebrada (no quadro de 32, deslocada), e para cada um o trecho mais perto (0 a 1)."""
    meia = max(larg * K, 0.5)
    d = np.full((N, N), np.inf); pos = np.zeros((N, N))
    n = len(pts) - 1
    for k, ((xa, ya), (xb, yb)) in enumerate(zip(pts[:-1], pts[1:])):
        xa, xb, ya, yb = xa + dx, xb + dx, ya + dy, yb + dy
        ddx, ddy = xb - xa, yb - ya; L2 = ddx * ddx + ddy * ddy or 1e-9
        t = np.clip(((x32 - xa) * ddx + (y32 - ya) * ddy) / L2, 0, 1)
        dd = np.hypot(x32 - (xa + t * ddx), y32 - (ya + t * ddy)) * K
        melhor = dd < d
        d = np.where(melhor, dd, d); pos = np.where(melhor, (k + t) / n, pos)
    return d <= meia, pos


def curva(a, b, c, n=16):
    """A tira como curva: do pé de perto ao alto e ao pé de longe (uma curva de Bézier)."""
    a, b, c = map(np.asarray, (a, b, c))
    ctrl = 2 * b - (a + c) / 2                                                  # passa pelo alto
    ts = np.linspace(0, 1, n)
    return [tuple((1 - t) ** 2 * a + 2 * (1 - t) * t * ctrl + t * t * c) for t in ts]


def sandalia(dx, dy, escuro, nome):
    """A sandália deslocada (dx, dy) no quadro de 32, `escuro` tons abaixo. Devolve a máscara dela."""
    t = lambda x: max(0, x - escuro)
    T = np.vectorize(t)
    palm = poligono(PALMILHA, dx, dy)
    sola = poligono(PALMILHA, dx + 0.3, dy + ESPESSURA) | palm
    ang = np.linspace(0, 2 * np.pi, 72)
    aro = [(CT[0] + RX * np.cos(a), CT[1] + RY * np.sin(a)) for a in ang]
    cuff, pos_c = faixa(aro, 1.05, dx, dy)
    vao = poligono(aro, dx, dy) & ~cuff                                          # o vão do tornozelo
    presas = [faixa(pp, LARG * 0.8, dx, dy)[0] for pp in PRESAS]
    tiras_pe = [faixa(curva(*tt), LARG, dx, dy) for tt in TIRAS]
    tudo = sola | cuff | np.any(presas, axis=0) | np.any([f for f, _ in tiras_pe], axis=0)
    if ETAPA == "silhueta":
        pinta(tudo, "k", 3, f"{nome}_sola")
        return tudo
    # a sola: o lado escuro, a beira de baixo mais escura
    lado = sola & ~palm
    pinta(lado, "k", t(2), f"{nome}_sola")
    pinta(lado & ~poligono(PALMILHA, dx + 0.3, dy + ESPESSURA * 0.5), "k", t(1), f"{nome}_sola")
    # a palmilha: clara; a beira de perto e o gasto do calcanhar um tom abaixo
    pinta(palm, "p", t(4), f"{nome}_palmilha")
    pinta(palm & (y32 - dy > 23.8 - (x32 - dx - 6) * 0.3), "p", t(3), f"{nome}_palmilha")
    pinta(palm & (np.hypot(x32 - dx - 25.6, (y32 - dy - 19.2) * 1.6) < 1.8), "p", t(3), f"{nome}_palmilha")
    # o tornozelo: a presa do calcanhar (atrás), o aro de trás (a metade de longe, escura), a presa da frente, o aro
    # da frente (a metade de perto, clara em cima)
    pinta(presas[1], "k", t(2), f"{nome}_tiras")
    longe = cuff & (y32 - dy < CT[1] - 0.2)
    pinta(longe, "k", t(2), f"{nome}_tiras")
    pinta(vao, "k", t(0), f"{nome}_tiras")
    pinta(vao & (y32 - dy > CT[1] + 0.3), "p", t(2), f"{nome}_palmilha")       # o calcanhar, lá embaixo
    pinta(presas[0], "k", t(3), f"{nome}_tiras")
    perto = cuff & ~longe
    pinta(perto, "k", T(np.where(x32 - dx < CT[0] - 1.2, 5, np.where(x32 - dx < CT[0] + 2.2, 4, 3))), f"{nome}_tiras")
    # as tiras do pé: a perna de perto em meio-tom, o alto claro, a perna de longe escura
    for f, pos in tiras_pe:
        pinta(f, "k", T(np.where(pos < 0.38, 3, np.where(pos < 0.62, 5, 2))), f"{nome}_tiras")
    tiras = cuff | np.any(presas, axis=0) | np.any([f for f, _ in tiras_pe], axis=0)
    sombra = (np.roll(tiras, 1, 1) | np.roll(tiras, 1, 0)) & ~tiras              # a sombra da tira, à direita e embaixo
    pinta(sombra & palm & ~vao, "k", t(1), f"{nome}_palmilha")
    return tudo


camadas = []
if not UMA:
    sandalia(-3.6, -3.4, 1, "tras")
    camadas += ["tras_sola", "tras_palmilha", "tras_tiras"]
frente = sandalia(0.0, 0.0, 0, "frente")
camadas += ["frente_sola", "frente_palmilha", "frente_tiras"]
if ETAPA == "final":
    tom = limpar(mat, tom, fixo)
if not UMA:
    sep = vizinhos(frente) & (mat != "")                          # a separação: o contorno da da frente sobre a de trás
    mat[sep] = "c"
mat[:, -1] = ""; mat[-1, :] = ""; mat[:, 0] = ""; mat[0, :] = ""
contornar(mat)
cam[mat == "c"] = "contorno"
camadas.append("contorno")
img = imagem(mat, tom, RAMPAS)
pasta = SAIDA / str(N); pasta.mkdir(parents=True, exist_ok=True)
sufixo = "_uma" if UMA else ""
img.save(pasta / f"sandalia{sufixo}_{ETAPA}_{N}.png")
if ETAPA == "final" and not UMA:
    listas_camadas((img, cam), pasta / "listas", camadas)
