"""O estudo de construção da queda de braço na vista de detalhe (protótipo): formas simples, antes do acabamento.

    python ferramentas/prototipos/taverna/morel/queda2/estudo.py --criar    # monta estudo-queda2.aseprite (só se não existir)
    python ferramentas/prototipos/taverna/morel/queda2/estudo.py            # exporta a folha de inspeção

Pela `arte-personagens-fenda` (o estudo com formas simples, as juntas pela geometria) e a `arte-cenas-fenda` (o espaço
antes dos objetos): o balcão e o chão ao fundo, o tampo com as tábuas, a tigela deslizada para oeste, o tronco de
Morel (os ombros, o peito), os braços em cápsulas de cores (Morel: o braço vermelho, o antebraço laranja, a mão
amarela; nós: azul, azul claro, ciano; o braço esquerdo dele num tom mais escuro), a pega; cada pixel com a superfície
mais perto da câmera (`desenho.py`). Na `guia` (separada, oculta na exportação das poses), as juntas, a linha dos
cotovelos e o arco que a pega percorre de um derrube ao outro; na `dado`, a área que o dado cobre enquanto rola.

Os quadros: 1 a 3, as poses (`disputa`, `vitoria_jogador`, `vitoria_morel`); 4, `percurso`: as três pegas e o arco
sobre a disputa, para ver se o quadro comporta o caminho; 5, `planta`: a mesa vista de cima (os cotovelos, o arco no
tampo, os dois derrubes, a tigela no lugar de antes e no novo, a vela, a caneca, o pão); 6, `pega`: as três pegas
construídas (maos.py), ampliadas 3×, nas cores das partes."""
import math
import pathlib
import sys
import tempfile

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.append(str(AQUI.parent / "queda"))  # só o fonte_aseprite.py (o juntas.py de lá é o da primeira proposta)

import desenho as D  # noqa: E402
import fonte_aseprite as fa  # noqa: E402
import juntas as J  # noqa: E402
import maos as M  # noqa: E402

FONTE = AQUI / "estudo-queda2.aseprite"
SAIDA = AQUI.parents[1] / "camadas" / "morel-vista" / "queda2-estudo.png"
QUADROS = ["disputa", "vitoria_jogador", "vitoria_morel", "percurso", "planta", "pega"]
CAMADAS = ["fundo", "mesa", "objetos", "tronco", "morel_esquerdo", "morel_braco", "morel_antebraco", "morel_mao",
           "nosso_braco", "nosso_antebraco", "nossa_mao", "guia", "dado"]
C = {
    "balcao": (58, 42, 30), "chao": (34, 29, 25), "mesa": (122, 92, 58), "tabua": (100, 74, 46), "ponta": (84, 60, 38),
    "tigela": (150, 90, 160), "tronco": (110, 110, 132), "cabeca": (150, 150, 172), "esquerdo": (150, 80, 60),
    "morel_braco": (205, 62, 52), "morel_antebraco": (238, 132, 52), "morel_mao": (250, 212, 82),
    "nosso_braco": (40, 70, 165), "nosso_antebraco": (72, 132, 232), "nossa_mao": (130, 222, 242),
    "junta": (255, 255, 255), "arco": (255, 240, 120), "linha": (255, 120, 220),
}
PARTE_COR = {"nossa_mao": (80, 190, 230), "nossos_dedos": (170, 240, 255), "nosso_polegar": (255, 255, 255),
             "mao_morel": (240, 180, 40), "dedos_morel": (255, 110, 60), "polegar_morel": (255, 240, 150)}


def _cor_parte(parte, normal):
    k = 1.0 if D.luz(normal) > 0.1 else 0.72
    return tuple(int(v * k) for v in PARTE_COR[parte.split(":")[0]]) + (255,)


RAIOS = {"morel": (5.8, 5.2, 4.8, 3.6), "nos": (5.2, 4.8, 4.4, 3.4)}  # o ombro, o cotovelo, o antebraço, o pulso


def _liso(cor):
    """A cor da parte, com um degrau de luz só para ler o volume (nada de acabamento)."""
    def f(normal, t, p):
        k = 1.0 if D.luz(normal) > 0.2 else 0.8
        return tuple(int(v * k) for v in cor) + (255,)
    return f


def cena(t, nome):
    """O fundo, a mesa, a tigela e o tronco de Morel: o que não é braço."""
    p = J.poses()[nome]
    D.plano_z(t, "fundo", 95.0, lambda x, y: -75 <= y <= 110, lambda x, y: C["balcao"] + (255,))
    D.plano_y(t, "fundo", -75.0, lambda x, z: z < 95, lambda x, z: C["chao"] + (255,))
    x0, x1 = J.MESA_X
    D.plano_y(t, "mesa", 0.0, lambda x, z: x0 <= x <= x1 and -33 <= z <= 33,
              lambda x, z: (C["tabua"] if (x - x0) % 12 < 0.7 else C["mesa"]) + (255,))
    D.plano_x(t, "mesa", x1, lambda y, z: -4 <= y <= 0 and -33 <= z <= 33, lambda y, z: C["ponta"] + (255,))
    D.plano_z(t, "mesa", 33.0, lambda x, y: x0 <= x <= x1 and -4 <= y <= 0, lambda x, y: C["ponta"] + (255,))
    tx, _, tz = J.TIGELA
    D.plano_y(t, "objetos", 9.0, lambda x, z: (x - tx) ** 2 + (z - tz) ** 2 <= J.TIGELA_RAIO ** 2,
              lambda x, z: C["tigela"] + (255,))
    # o tronco de Morel: os ombros e o peito em cápsulas (o peito largo, do meio dos ombros até a cintura, atrás da
    # borda de lá), a cabeça (acima do quadro)
    sm, se = p["ombro_m"], p["ombro_esq_m"]
    meio = J._mul(J._add(sm, se), 0.5)
    D.capsula(t, "tronco", sm, se, 8.0, 8.0, _liso(C["tronco"]))
    for dx in (-10.0, 0.0, 10.0):
        topo = J._add(meio, (dx, -4.0, 2.0))
        D.capsula(t, "tronco", topo, J._add(topo, (0.0, -40.0, 6.0)), 10.0, 11.0, _liso(C["tronco"]))
    D.capsula(t, "tronco", J._add(meio, (0, 22, 2)), J._add(meio, (0, 22, 2)), 11.0, 11.0, _liso(C["cabeca"]))


def bracos(t, nome):
    p = J.poses()[nome]
    for quem, S, E, W in (("morel", "ombro_m", "cotovelo_m", "pulso_m"), ("nos", "ombro_n", "cotovelo_n", "pulso_n")):
        rS, rE, rA, rW = RAIOS[quem]
        cam = "morel" if quem == "morel" else "nosso"
        D.capsula(t, f"{cam}_braco", p[S], p[E], rS, rE, _liso(C[f"{cam}_braco"]))
        D.capsula(t, f"{cam}_antebraco", p[E], p[W], rA, rW, _liso(C[f"{cam}_antebraco"]))
    # o braço esquerdo de Morel: do ombro à mão que agarra a borda de lá; o cotovelo para fora e para baixo
    se, m = p["ombro_esq_m"], J.MAO_ESQ_MOREL[nome]
    mao = J._add(m, (0.0, 2.5, 0.0))
    e = D.cotovelo(se, mao, (0.35, -1.0, -0.5), 30.0, 28.0)
    D.capsula(t, "morel_esquerdo", se, e, 5.6, 5.0, _liso(C["esquerdo"]))
    D.capsula(t, "morel_esquerdo", e, mao, 4.8, 3.6, _liso(C["esquerdo"]))
    # a pega construída (maos.py): cada parte numa cor; as camadas da fonte juntam as partes de cada um
    M.construir(t, nome, _cor_parte)
    for q, parte in list(t.camada.items()):
        if parte.split(":")[0] in M.PARTES:
            t.camada[q] = "nossa_mao" if M.dono(parte) == "nos" else "morel_mao"
    return e


def _cruz(px, cor, q):
    x, y = round(q[0]), round(q[1])
    for d in (-1, 0, 1):
        px[(x + d, y)] = cor + (255,)
        px[(x, y + d)] = cor + (255,)


def _arco(px, passo=3):
    alto, r = J.pega(0)
    A, B = J.COTOVELO_NOSSO, J.COTOVELO_MOREL
    u = J._un(J._sub(B, A))
    centro = J._sub(alto, (0.0, r, 0.0))
    lado = J._un((-u[2], 0.0, u[0]))
    for k in range(-90, 91, passo):
        a = math.radians(k)
        q = J._add(centro, J._add(J._mul((0.0, 1.0, 0.0), r * math.cos(a)), J._mul(lado, r * math.sin(a))))
        if q[1] >= J.TAMPO_MAO - 0.01:
            x, y, _ = J.tela(q)
            px[(round(x), round(y))] = C["arco"] + (255,)


def _guia(nome, cotovelo_esq):
    p = J.poses()[nome]
    g = {}
    _arco(g)
    A, B = J.tela(J.COTOVELO_NOSSO), J.tela(J.COTOVELO_MOREL)
    n = 20
    for k in range(0, n + 1, 2):
        g[(round(A[0] + (B[0] - A[0]) * k / n), round(A[1] + (B[1] - A[1]) * k / n))] = C["linha"] + (255,)
    for q in ("ombro_m", "cotovelo_m", "pulso_m", "ombro_n", "cotovelo_n", "pulso_n", "pega", "ombro_esq_m"):
        _cruz(g, C["junta"], J.tela(p[q]))
    _cruz(g, C["junta"], J.tela(cotovelo_esq))
    return g


def _dado():
    d = {}
    for (x0, y0, x1, y1), cor in ((J.DADO["1920×945"], (0, 255, 0)), (J.DADO["1280×720"], (255, 0, 255))):
        for x in range(x0, x1 + 1):
            d[(x, y0)] = cor + (255,)
        for y in range(y0, 96):
            d[(x0, y)] = cor + (255,)
            d[(x1, y)] = cor + (255,)
    return d


def pose(nome):
    t = D.Tela()
    cena(t, nome)
    e = bracos(t, nome)
    c = t.camadas()
    c["guia"] = _guia(nome, e)
    c["dado"] = _dado()
    return c


def percurso():
    """A disputa com as três pegas e o arco: o quadro comporta o caminho de um derrube ao outro?"""
    c = pose("disputa")
    for nome in ("vitoria_jogador", "vitoria_morel"):
        _cruz(c["guia"], C["arco"], J.tela(J.poses()[nome]["pega"]))
    _arco(c["guia"], passo=1)
    return c


def planta():
    """A mesa vista de cima: 1,4 px por cm, o norte (Morel) em cima."""
    c = {k: {} for k in CAMADAS}
    P = lambda x, z: (round(200 + x * 1.4), round(48 - z * 1.25))  # noqa: E731
    x0, x1 = J.MESA_X
    for py in range(96):  # o tampo pixel a pixel (a conta ao contrário de P), sem os buracos do arredondamento
        for px in range(320):
            x, z = (px - 200) / 1.4, (48 - py) / 1.25
            if x0 <= x <= x1 and -33 <= z <= 33:
                c["mesa"][(px, py)] = (C["tabua"] if (x - x0) % 12 < 0.75 else C["mesa"]) + (255,)
    # a tigela no lugar novo (cheia) e no de antes (o aro); a vela, a caneca e o pão (verde): pixel a pixel
    for py in range(96):
        for px in range(320):
            x, z = (px - 200) / 1.4, (48 - py) / 1.25
            d_nova = math.hypot(x - J.TIGELA[0], z - J.TIGELA[2])
            d_antes = math.hypot(x + 6.0, z - 1.0)
            if d_nova <= J.TIGELA_RAIO:
                c["objetos"][(px, py)] = C["tigela"] + (255,)
            elif J.TIGELA_RAIO - 1.5 <= d_antes <= J.TIGELA_RAIO:
                c["objetos"][(px, py)] = C["tronco"] + (255,)
            elif any(abs(x - cx) <= r and abs(z - cz) <= r for cx, cz, r in ((-71, -27, 3), (-95, -22, 5), (17, -22, 5))):
                c["objetos"][(px, py)] = (90, 160, 90, 255)
    alto, r = J.pega(0)
    A, B = J.COTOVELO_NOSSO, J.COTOVELO_MOREL
    for q, cor in ((A, "nosso_antebraco"), (B, "morel_antebraco")):
        for dx in range(-4, 5):
            for dz in range(-4, 5):
                if dx * dx + dz * dz <= 16:
                    c[cor][P(q[0] + dx, q[2] + dz)] = C[cor] + (255,)
    f1, f2 = J.pega(-1)[0], J.pega(1)[0]
    for k in range(41):
        q = J._add(f1, J._mul(J._sub(f2, f1), k / 40))
        c["guia"][P(q[0], q[2])] = C["arco"] + (255,)
    for q in (f1, f2, alto):
        _cruz(c["guia"], C["junta"], P(q[0], q[2]))
    for k in range(0, 21, 2):
        q = J._add(A, J._mul(J._sub(B, A), k / 20))
        c["guia"][P(q[0], q[2])] = C["linha"] + (255,)
    return c


def pega_ampliada():
    """As três pegas construídas, ampliadas 3× (30×30 px da cena em cada uma), nas cores das partes: o nosso punho
    (azul), os nossos dedos (azul claro), o nosso polegar (branco); o punho de Morel (amarelo), os dedos dele
    (laranja), o polegar dele (amarelo claro); os antebraços (o nosso azul escuro, o dele castanho) e o tampo."""
    c = {k: {} for k in CAMADAS}
    for i, nome in enumerate(QUADROS[:3]):
        t = D.Tela()
        p = J.poses()[nome]
        for quem, E_, W_, rgb in (("morel", "cotovelo_m", "pulso_m", (150, 70, 50)), ("nos", "cotovelo_n", "pulso_n", (40, 60, 120))):
            _, _, rA, rW = RAIOS[quem]
            D.capsula(t, "fundo", p[E_], p[W_], rA, rW, lambda n_, t_, q, rgb=rgb: rgb + (255,))
        D.plano_y(t, "fundo", 0.0, lambda x, z: True, lambda x, z: (110, 80, 50, 255))
        M.construir(t, nome, _cor_parte)
        P = [round(v) for v in J.tela(p["pega"])[:2]]
        for (x, y), cor in t.cor.items():
            xx, yy = x - P[0] + 15, y - P[1] + 15
            if 0 <= xx < 30 and 0 <= yy < 30:
                cam = "nossa_mao" if t.camada[(x, y)].startswith("nos") else "morel_mao" if t.camada[(x, y)] in M.PARTES or ":" in t.camada[(x, y)] else "mesa"
                for dy in range(3):
                    for dx in range(3):
                        c[cam][(8 + i * 104 + xx * 3 + dx, 3 + yy * 3 + dy)] = cor
    return c


def criar(refazer=False):
    pixels = [pose(n) for n in QUADROS[:3]] + [percurso(), planta(), pega_ampliada()]
    print(fa.montar(FONTE, 320, 96, CAMADAS, QUADROS, pixels, refazer=refazer))


def exportar():
    with tempfile.TemporaryDirectory() as tmp:
        qs = fa.quadros(FONTE, tmp)
        folha = Image.new("RGBA", (320, 96 * len(qs)), (24, 22, 20, 255))
        for i, q in enumerate(qs):
            folha.alpha_composite(Image.open(q).convert("RGBA"), (0, 96 * i))
    folha.save(SAIDA, optimize=True)
    print(f"{SAIDA.name}: {len(qs)} quadros")


if __name__ == "__main__":
    if "--criar" in sys.argv or "--refazer" in sys.argv:
        criar("--refazer" in sys.argv)
    else:
        exportar()
