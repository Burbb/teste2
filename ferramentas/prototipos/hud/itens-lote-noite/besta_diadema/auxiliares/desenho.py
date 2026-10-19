# A Besta Leve do Arqueiro e o Diadema do Mago (proposta de 19/10/2026). A construção é a mesma em 32, 40 e 48 (as
# medidas no quadro de 32); o 64 é o 32 ampliado 2x (a política da skill). A luz é a da família: de cima e da esquerda.
# Uso: python desenho.py <besta|diadema> <32|40|48> [silhueta] [<pasta>]. Grava a prévia e as listas em <pasta>/<N>/.
import pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6] / "ferramentas" / "arte"))
from pixel_comum import grade, contornar, imagem, limpar, listas_camadas

PECA = sys.argv[1]; N = int(sys.argv[2]); ETAPA = "silhueta" if "silhueta" in sys.argv[3:] else "final"
SAIDA = pathlib.Path(next((a for a in sys.argv[3:] if a != "silhueta"), "."))
K = N / 32
RAMPAS = {
    "m": ["#1c0f08", "#351a0d", "#522812", "#713819", "#8f4c22", "#ab6631", "#c58449", "#dba56a"],   # a madeira (o teixo do arco)
    "k": ["#140b09", "#251412", "#3a1f1a", "#522c23", "#6b3b2d", "#86503c"],                       # o couro (o do arco)
    "a": ["#24272c", "#3c4148", "#5a616b", "#7d8590", "#a3abb5", "#d2d8de"],                       # o aço
    "f": ["#5f584a", "#8f8670", "#bdb497", "#e1dabe"],                                             # a corda (a do arco)
    "o": ["#5E3E14", "#946422", "#C89434", "#EED070", "#FFF0B0"],                                  # o latão (o do manto)
    "g": ["#2A1240", "#4A2470", "#7040A8", "#A070D8", "#D8B8F8"],                                  # a gema violeta (a do amuleto)
    "d": ["#140D06", "#24170A", "#3A2610"],                                                        # o latão por dentro, na sombra
}
mat, tom, fixo, X, Y = grade(N)
cam = np.full((N, N), "", dtype=object)
x32, y32 = X / K, Y / K


def pinta(onde, m, t, c):
    mat[onde] = m; tom[onde] = t if np.isscalar(t) else t[onde]; cam[onde] = c


def poligono(pts):
    dentro = np.zeros((N, N), bool)
    n = len(pts)
    for i in range(n):
        (xa, ya), (xb, yb) = pts[i], pts[(i + 1) % n]
        cruza = ((ya > y32) != (yb > y32)) & (x32 < (xb - xa) * (y32 - ya) / ((yb - ya) or 1e-9) + xa)
        dentro ^= cruza
    return dentro


def faixa(pts, larg):
    """Os pixels perto da linha quebrada (no quadro de 32), meia largura `larg` (no mínimo meio pixel), e para cada um a
    posição ao longo da linha (0 a 1) e o lado (negativo à esquerda de quem segue a linha)."""
    meia = max(larg * K, 0.5)
    d = np.full((N, N), np.inf); pos = np.zeros((N, N)); lado = np.zeros((N, N))
    n = len(pts) - 1
    for k, ((xa, ya), (xb, yb)) in enumerate(zip(pts[:-1], pts[1:])):
        ddx, ddy = xb - xa, yb - ya; L2 = ddx * ddx + ddy * ddy or 1e-9
        t = np.clip(((x32 - xa) * ddx + (y32 - ya) * ddy) / L2, 0, 1)
        dd = np.hypot(x32 - (xa + t * ddx), y32 - (ya + t * ddy)) * K
        s = ((x32 - xa) * ddy - (y32 - ya) * ddx) / np.sqrt(L2)
        melhor = dd < d
        d = np.where(melhor, dd, d); pos = np.where(melhor, (k + t) / n, pos); lado = np.where(melhor, s, lado)
    return d <= meia, pos, lado


if PECA == "besta":
    # A besta deitada, vista de cima, na diagonal das armas aprovadas: a coronha de madeira da soleira (embaixo à
    # esquerda) até a frente (em cima à direita); o arco de aço atravessado na frente, perpendicular à coronha, com as
    # pontas puxadas para trás pela corda; a corda das pontas até a noz no meio da coronha (o V da besta armada); o
    # estribo de aço na ponta da frente; a empunhadura de couro atrás da noz.
    d = np.array([1.0, -1.0]) / np.sqrt(2); p = np.array([1.0, 1.0]) / np.sqrt(2)   # ao longo da coronha / do arco
    SOLEIRA = np.array([3.8, 28.2]); FRENTE = np.array([24.8, 7.2])
    NOZ = FRENTE - 8.6 * d
    def ponto(base, ad, ap):
        return tuple(base + ad * d + ap * p)
    # a coronha: larga na soleira, estreita na frente (o lado de cima é a face clara, o de baixo, a espessura)
    coronha = poligono([ponto(SOLEIRA, -0.4, -1.9), ponto(SOLEIRA, 3.0, -1.8), ponto(NOZ, 0.0, -1.3), ponto(FRENTE, 0.6, -1.0),
                        ponto(FRENTE, 0.6, 1.0), ponto(NOZ, 0.0, 1.4), ponto(SOLEIRA, 3.0, 2.1), ponto(SOLEIRA, -0.4, 2.2)])
    # o arco transversal: uma curva de aço pela frente, as pontas para trás
    arco_pts = [ponto(FRENTE, -2.6 * (t * t), 9.8 * t) for t in np.linspace(-1, 1, 25)]
    arco, pos_a, lado_a = faixa(arco_pts, 0.95)
    pontas = [np.array(arco_pts[0]), np.array(arco_pts[-1])]
    corda = np.zeros((N, N), bool)
    for pt in pontas:
        corda |= faixa([tuple(pt), tuple(NOZ)], 0.45)[0]
    estribo = faixa([ponto(FRENTE, 0.4, -1.4), ponto(FRENTE, 2.6, -1.6), ponto(FRENTE, 3.4, 0.0), ponto(FRENTE, 2.6, 1.6),
                     ponto(FRENTE, 0.4, 1.4)], 0.5)[0]
    empunhadura = coronha & (np.abs(((x32 - NOZ[0]) * d[0] + (y32 - NOZ[1]) * d[1]) + 4.8) < 2.0)
    noz = np.hypot(x32 - NOZ[0], y32 - NOZ[1]) * K <= max(1.1 * K, 0.8)
    gatilho = faixa([ponto(NOZ, -1.6, 1.9), ponto(NOZ, -4.2, 2.6)], 0.45)[0] & ~coronha       # a alavanca sob a coronha
    if ETAPA == "silhueta":
        pinta(coronha | arco | estribo | gatilho, "m", 4, "coronha")
        pinta(corda, "f", 2, "corda")
    else:
        ap_px = (x32 - SOLEIRA[0]) * p[0] + (y32 - SOLEIRA[1]) * p[1]           # através da coronha (- em cima, + embaixo)
        pinta(gatilho, "a", 2, "metal")
        pinta(estribo, "a", 3, "metal")
        tc = np.where(ap_px < -0.6, 6, np.where(ap_px < 0.5, 5, 3))
        pinta(coronha, "m", tc, "coronha")
        pinta(coronha & (ap_px > 1.1), "m", 2, "coronha")                        # a espessura, embaixo
        # o sulco do virote: a linha escura da noz até a frente
        sulco = faixa([tuple(NOZ + 1.2 * d), tuple(FRENTE - 0.4 * d)], 0.35)[0] & coronha
        pinta(sulco, "m", 2, "coronha")
        pinta(empunhadura, "k", np.where(ap_px < -0.2, 5, 3), "empunhadura")
        pinta(empunhadura & (np.abs(((x32 - NOZ[0]) * d[0] + (y32 - NOZ[1]) * d[1]) + 4.8) < 0.45), "k", 1, "empunhadura")
        pinta(corda, "f", 2, "corda")
        # o arco de aço: claro em cima (a luz), escuro embaixo; as pontas com a corda presa
        ta = np.where(lado_a < -0.25, 5, np.where(lado_a < 0.35, 4, 2))
        pinta(arco, "a", ta, "arco")
        for pt in pontas:
            pinta(np.hypot(x32 - pt[0], y32 - pt[1]) * K <= max(0.8 * K, 0.6), "a", 1, "arco")
        pinta(noz, "o", 2, "metal")
        pinta(noz & (x32 < NOZ[0]) & (y32 < NOZ[1]), "o", 3, "metal")
    camadas = ["coronha", "empunhadura", "corda", "arco", "metal", "contorno"]
else:
    # O Diadema, rodada 2: de frente, a face da frente da faixa à mostra (a apresentação da imagem que o Jean mandou para
    # o ângulo), com pouco do aro visto de cima. A faixa de latão (o do broche do manto) é um cilindro baixo visto quase
    # de frente: a face de fora em curva, clara à esquerda, com a beira de cima acesa e um friso no meio; atrás, por cima
    # da faixa, a face de dentro do lado de trás, escura, e por baixo dela o vão (o lugar da cabeça); a borda de trás,
    # uma linha fina. Na frente, a ponta estreita sobe da faixa com a gema violeta (a do amuleto aprovado) no engaste,
    # Sem coroa: uma ponta só, a faixa fina.
    C = np.array([16.0, 17.6]); RX, RY, ALT = 13.6, 2.6, 4.0
    ang = np.linspace(0, 2 * np.pi, 200)
    def elipse(cx, cy, rx, ry):
        return poligono([(cx + rx * np.cos(a), cy + ry * np.sin(a)) for a in ang])
    topo = elipse(C[0], C[1], RX, RY); base = elipse(C[0], C[1] + ALT, RX, RY)
    entre = poligono([(C[0] - RX, C[1]), (C[0] + RX, C[1]), (C[0] + RX, C[1] + ALT), (C[0] - RX, C[1] + ALT)])
    ESP = 0.9                                                                   # a espessura da chapa
    abertura = elipse(C[0], C[1], RX - ESP, RY - ESP * 0.45)                    # a boca de cima, por dentro
    corpo = topo | base | entre
    # a face de fora, na frente: abaixo da beira de cima da frente (a metade de baixo da elipse de cima)
    frente_y = C[1] + RY * np.sqrt(np.clip(1 - ((x32 - C[0]) / RX) ** 2, 0, 1))
    face = corpo & (y32 >= frente_y - 0.5)
    # pela boca: a face de dentro do lado de trás (de cima até ALT abaixo da borda de trás) e, abaixo dela, o vão
    tras_y = C[1] - (RY - ESP * 0.45) * np.sqrt(np.clip(1 - ((x32 - C[0]) / (RX - ESP)) ** 2, 0, 1))
    dentro = abertura & ~face & (y32 < tras_y + ALT)
    vao = abertura & ~face & ~dentro
    aro = corpo & ~vao
    # a ponta da frente, a gema e as contas dos lados
    PE = C[1] + RY + 1.4                                                        # o pé da ponta, na faixa da frente
    placa = poligono([(C[0] - 3.0, PE), (C[0] - 2.7, PE - 5.6), (C[0] - 1.1, PE - 12.4), (C[0], PE - 15.2),
                      (C[0] + 1.1, PE - 12.4), (C[0] + 2.7, PE - 5.6), (C[0] + 3.0, PE)])
    G = np.array([C[0], PE - 6.6])
    gema = np.hypot((x32 - G[0]) * 1.05, (y32 - G[1]) * 0.78) * K <= max(2.15 * K, 1.0)
    engaste = np.hypot((x32 - G[0]) * 1.05, (y32 - G[1]) * 0.78) * K <= max(3.0 * K, 1.6)
    if ETAPA == "silhueta":
        pinta(aro | placa, "o", 2, "aro")
        pinta(vao, "", 0, "")
    else:
        # a face de dentro, atrás: na sombra (mais escura embaixo, perto da face da frente); a borda de trás um tom acima
        pinta(dentro, "d", np.where(y32 < tras_y + 1.2, 2, np.where(y32 < tras_y + 2.4, 1, 0)), "aro")
        borda_tras = aro & ~face & ~dentro
        pinta(borda_tras, "o", np.where(x32 < C[0], 2, 1), "aro")
        # a face de fora: a luz da esquerda em faixas, a beira de cima acesa, a beira de baixo na sombra, o friso
        tf = np.where(x32 < C[0] + RX * 0.1, 2, 1)
        pinta(face, "o", tf, "aro")
        beira = face & (y32 < frente_y + 0.9 * K ** 0)
        pinta(beira, "o", np.minimum(tf + 1, 4), "aro")
        pinta(beira & (np.abs(x32 - (C[0] - RX * 0.55)) < 2.0), "o", 4, "aro")
        baixo_y = frente_y + ALT
        pinta(face & (y32 > baixo_y - 1.0), "o", np.maximum(tf - 1, 0), "aro")
        # a ponta: a face clara à esquerda, a sombra à direita; o engaste e a gema
        pinta(placa, "o", np.where(x32 < C[0] - 0.3, 3, 2), "placa")
        pinta(placa & (x32 > C[0] + 1.0), "o", 1, "placa")
        pinta(engaste, "o", 1, "placa")
        pinta(gema, "g", 2, "gema")
        pinta(gema & (x32 < G[0] + 0.2) & (y32 < G[1] + 0.2), "g", 3, "gema")
        pinta(gema & (x32 > G[0] + 0.6) & (y32 > G[1] + 0.4), "g", 1, "gema")
        pinta(np.hypot(x32 - (G[0] - 0.7), y32 - (G[1] - 0.8)) * K <= 0.6, "g", 4, "gema")
    camadas = ["aro", "placa", "gema", "contorno"]

if ETAPA == "final":
    tom = limpar(mat, tom, fixo)
mat[:, -1] = ""; mat[-1, :] = ""; mat[:, 0] = ""; mat[0, :] = ""
contornar(mat)
cam[mat == "c"] = "contorno"
img = imagem(mat, tom, RAMPAS)
pasta = SAIDA / str(N); pasta.mkdir(parents=True, exist_ok=True)
img.save(pasta / f"{PECA}_{ETAPA}_{N}.png")
if ETAPA == "final":
    listas_camadas((img, cam), pasta / "listas", camadas)
