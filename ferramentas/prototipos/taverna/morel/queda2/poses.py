"""As três poses da queda de braço na vista de detalhe, com o acabamento do jogo (protótipo; para a avaliação do Jean).

    python ferramentas/prototipos/taverna/morel/queda2/poses.py --criar     # monta queda2.aseprite (só se não existir)
    python ferramentas/prototipos/taverna/morel/queda2/poses.py             # exporta camadas/morel-vista/queda2*.png

**A fonte** `queda2.aseprite` (320×96; os quadros `disputa`, `vitoria_jogador`, `vitoria_morel`) tem uma camada por
parte: `fundo` (o balcão e o chão, no escuro), `mesa` (o tampo com as tábuas, a luz da vela e a sombra de contato do
que encosta nele), `objetos` (a tigela deslizada), `tronco` (o peito de Morel: o couro, o colete vermelho com as
fivelas, a ombreira do ombro esquerdo, o punho da espada), `morel_esquerdo`, `morel_braco`, `nosso_braco` e `maos`
(as pegas, desenhadas à mão em grade: `PEGAS`), e as guias ocultas (`guia`: as juntas; `dado`: a área do dado). Cada
pixel dos volumes fica na camada da superfície mais perto (`desenho.py`), então as camadas não se sobrepõem. `--criar`
monta a fonte uma vez; depois ela é a autoridade (os retoques no editor), e a exportação lê dela.

**De onde vem cada coisa:** as juntas, de `juntas.py`; os volumes (os braços, o peito) projetados pela câmera e
iluminados pela vela e pela lareira (a esquerda e a frente), em degraus de tom como as cenas aprovadas, sem contorno;
as cores, das paletas aprovadas (o couro e a pele de Morel do `vestir.lua`, o colete, a ombreira e a tigela da fonte da
vista; a madeira do tampo da vista); a nossa manga de lã azul-acinzentada, a mesma das poses anteriores. As mãos não
saem da fórmula: são grades à mão, a pega do estudo simplificada (o dorso, os dedos de um sobre o dorso do outro em
duas ou três listras, os polegares)."""
import math
import pathlib
import sys
import tempfile

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.append(str(AQUI.parent / "queda"))  # só o fonte_aseprite.py

import desenho as D  # noqa: E402
import fonte_aseprite as fa  # noqa: E402
import juntas as J  # noqa: E402

FONTE = AQUI / "queda2.aseprite"
SAIDA = AQUI.parents[1] / "camadas" / "morel-vista" / "queda2.png"
QUADROS = ["disputa", "vitoria_jogador", "vitoria_morel"]
CAMADAS = ["fundo", "mesa", "objetos", "tronco", "morel_esquerdo", "morel_braco", "nosso_braco", "maos", "guia", "dado"]
H = lambda s: tuple(int(s[i:i + 2], 16) for i in (0, 2, 4)) + (255,)  # noqa: E731

# o couro de Morel (vestir.lua) do mais claro ao mais escuro; a nossa lã; as peles
COURO = [H("8a5a38"), H("6a4a2c"), H("4e3420"), H("33231a"), H("2a1c14")]
LA = [H("7c889a"), H("5e6878"), H("474f5d"), H("333a45"), H("262b34")]
PUNHO_M, PUNHO_N = [H("3a2716"), H("2a1c14")], [H("3a4150"), H("262b34")]
PELE_M = {"q": H("b4805e"), "w": H("8c5c44"), "e": H("5e3e2e")}  # a pele de Morel, mais escura e quente que a nossa
SOMBRA_PELE = {"nos": H("5c3e30"), "morel": H("3e2820")}
PELE_N = {"1": H("e2b898"), "2": H("bc8c6a"), "3": H("86604a")}
# o colete, a ombreira e o punho da espada (a fonte da vista aprovada)
COLETE = [H("a8443a"), H("8a3428"), H("5e241c"), H("3e1610")]
BARBA = [H("5a3e2a"), H("4a3322"), H("3e2a1c"), H("2a1c14"), H("20160f")]
ACO = [H("c4c6cc"), H("9a9ca4"), H("6e7078"), H("4e4640"), H("2e3034")]
# a madeira do tampo (a vista aprovada, já com a luz: do mais claro ao mais escuro) e a junta das tábuas
MADEIRA = [H("7a512f"), H("744d2d"), H("6d492b"), H("654429"), H("5d4027"), H("543a23"), H("4a3320")]
JUNTA, ARESTA = H("3e2a18"), H("b27c44")
TIGELA = {"aro": H("9c6438"), "aro2": H("7a4a2c"), "caldo": H("6a2a14"), "caldo2": H("4c2c18"),
          "ponto": [H("c4843e"), H("c8642a"), H("6a7a2a"), H("d4b67e")], "sombra": H("2e2014")}
FUNDO = {"balcao": [H("3e2a1a"), H("34231a"), H("2a1c14")], "tabua": H("221710"), "chao": [H("231a14"), H("1c1511")]}
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def _degrau(rampa, v, x, y):
    """v de 0 (claro) a 1 (escuro) na rampa, com o pontilhado de Bayer entre um degrau e o outro."""
    f = max(0.0, min(0.999, v)) * (len(rampa) - 1)
    i = int(f)
    return rampa[min(i + (1 if (f - i) * 16 > BAYER[y % 4][x % 4] else 0), len(rampa) - 1)]


def _tom(rampa, s):
    """O tom de um volume pela luz (s de -1 a 1), em degraus, como o vestir.lua."""
    i = 0 if s > 0.62 else 1 if s > 0.3 else 2 if s > -0.05 else 3 if s > -0.4 else 4
    return rampa[min(i, len(rampa) - 1)]


def volume(rampa, punho=None, ante=False, desce=0.18):
    def f(normal, t, p):
        s = D.luz(normal)
        if punho and t > 0.88:
            return punho[0] if s > 0.1 else punho[1]
        return _tom(rampa, s - (desce if ante else 0.0))  # o antebraço abaixo do braço (um tom, ou meio)
    return f


# ------------------------------------------------------------------ a cena (o que não é braço)
def _mesa_cor(x, z, sombras):
    x0, _ = J.MESA_X
    px, py, _ = J.tela((x, 0.0, z))
    ix, iy = int(px), int(py)
    if (x - x0) % 12 < 0.75:
        return JUNTA
    # a luz da vela (a oeste e de cá) e o escuro para leste e para longe; a sombra de contato escurece dois degraus
    d = math.hypot(x + 71, (z + 27) * 1.2)
    v = min(1.0, max(0.0, (d - 40) / 110))
    for (sx, sz, r) in sombras:
        if (x - sx) ** 2 + (z - sz) ** 2 <= r * r:
            v = min(1.0, v + 0.42)
            break
    return _degrau(MADEIRA, v, ix, iy)


def cena(t, nome, sombras):
    p = J.poses()[nome]

    # o balcão atrás de Morel (a frente de tábuas, o tampo com a aresta acesa), a parede além, o chão: no escuro, a luz
    # quente vindo da esquerda (a lareira)
    def balcao(x, y):
        px, py, _ = J.tela((x, y, 150.0))
        if (x + 400) % 18 < 1.4 and int(px + py) % 2 == 0:  # as juntas das tábuas, pontilhadas: o fundo fica quieto
            return FUNDO["tabua"]
        # a luz quente do lampião, no alto à direita (no esteio, como na vista), e o escuro em volta
        lamp = math.hypot((x - 175) / 1.3, y - 20)
        v = min(1.0, max(0.0, 0.35 + (x + 40) / 400 + min(0.0, (lamp - 95) / 160)))
        return _degrau(FUNDO["balcao"], v, int(px), int(py))
    D.plano_z(t, "fundo", 150.0, lambda x, y: -75 <= y <= 30, balcao)
    D.plano_y(t, "fundo", 30.0, lambda x, z: 150 <= z <= 185,
              lambda x, z: COURO[1] if z < 152 else _degrau(FUNDO["balcao"], min(1.0, max(0.0, (x + 40) / 200)), *map(int, J.tela((x, 30.0, z))[:2])))
    D.plano_z(t, "fundo", 185.0, lambda x, y: y > 30,
              lambda x, y: _degrau(FUNDO["chao"], 0.3, *map(int, J.tela((x, y, 185.0))[:2])))
    D.plano_y(t, "fundo", -75.0, lambda x, z: z < 150,
              lambda x, z: _degrau(FUNDO["chao"], 0.5, *map(int, J.tela((x, -75, z))[:2])))
    x0, x1 = J.MESA_X
    D.plano_y(t, "mesa", 0.0, lambda x, z: x0 <= x <= x1 and -33 <= z <= 33, lambda x, z: _mesa_cor(x, z, sombras))
    D.plano_x(t, "mesa", x1, lambda y, z: -4 <= y <= 0 and -33 <= z <= 33,
              lambda y, z: MADEIRA[-1] if y < -0.6 else ARESTA)
    D.plano_z(t, "mesa", 33.0, lambda x, y: x0 <= x <= x1 and -4 <= y <= 0, lambda x, y: MADEIRA[-2] if y < -0.6 else ARESTA)
    # a tigela deslizada: o aro, o caldo com os pedaços, a sombra no tampo
    tx, _, tz = J.TIGELA
    R = J.TIGELA_RAIO

    def tigela(x, z):
        d = math.hypot(x - tx, z - tz)
        if d > R - 2.4:
            return TIGELA["aro"] if (x - tx) < (z - tz) else TIGELA["aro2"]
        k = (int(x * 3) * 7 + int(z * 3) * 13) % 41
        if k < 4:
            return TIGELA["ponto"][k]
        return TIGELA["caldo"] if (x - tx) + (z - tz) < 4 else TIGELA["caldo2"]
    D.plano_y(t, "objetos", 9.0, lambda x, z: math.hypot(x - tx, z - tz) <= R, tigela)
    D.plano_z(t, "objetos", tz - 0.0, lambda x, y: abs(x - tx) <= R * 0.92 and 0 <= y <= 9,
              lambda x, y: TIGELA["aro2"] if y > 4 else TIGELA["sombra"])
    tronco(t, p)


def tronco(t, p):
    """O peito de Morel, um volume só (um elipsoide da linha dos ombros até a cintura, atrás da borda de lá): o couro
    aberto na frente e o colete vermelho no meio, com as duas tiras de fivela; a ombreira de aço no ombro esquerdo; o
    punho da espada atrás do ombro direito."""
    sm, se = p["ombro_m"], p["ombro_esq_m"]
    larg = J._norma(J._sub(se, sm))
    e1 = J._un(J._sub(se, sm))
    e2 = J._un(J._sub((0.0, 1.0, 0.0), J._mul(e1, e1[1])))
    e3 = J._cruz(e1, e2)
    meio = J._mul(J._add(sm, se), 0.5)
    centro = J._add(meio, (0.0, -15.0, 3.0))
    semi = (larg / 2 + 2.0, 22.0, 11.0)

    def cor(normal, local):
        u = (local[0] + 1) / 2                     # 0 no ombro direito, 1 no esquerdo
        abaixo = 15.0 - local[1] * semi[1]         # quanto abaixo da linha dos ombros (cm)
        s = D.luz(normal)
        if 0.33 <= u <= 0.69 and abaixo > 2:
            for faixa in (11.0, 21.0):             # as tiras das fivelas
                if abs(abaixo - faixa) <= 1.5:
                    if abs(u - 0.52) < 0.05:
                        return ACO[1] if abaixo < faixa else ACO[3]
                    return ACO[3] if abaixo < faixa else ACO[4]
            if u < 0.355 or u > 0.665:             # a borda do colete, na sombra do couro
                return COLETE[3]
            return _tom(COLETE + [COLETE[3]], s - 0.15)
        return _tom(COURO, s - 0.1)
    D.elipsoide(t, "tronco", centro, (e1, e2, e3), semi, cor)
    D.capsula(t, "tronco", J._add(sm, (2.0, -3.0, 1.0)), J._add(se, (-2.0, -3.0, 1.0)), 5.0, 5.0,
              lambda n, t_, q: _tom(COURO, D.luz(n) - 0.1))
    # o pescoço e a ponta da barba (a da vista: castanha escura), na borda de cima: o rosto fica acima do quadro
    D.capsula(t, "tronco", J._add(meio, (0.0, 2.0, 3.0)), J._add(meio, (0.0, 9.0, 3.0)), 5.5, 5.5,
              lambda n, t_, q: _tom([PELE_M["w"], PELE_M["w"], PELE_M["e"], PELE_M["e"], COURO[3]], D.luz(n)))
    D.elipsoide(t, "tronco", J._add(meio, (0.0, 13.0, 6.0)), (e1, e2, e3), (8.0, 8.0, 6.5),
                lambda n, l: _tom(BARBA, D.luz(n) - 0.1))
    D.elipsoide(t, "tronco", J._add(se, (2.0, 1.5, 0.0)), (e1, e2, e3), (7.0, 4.6, 6.6),
                lambda n, l: _tom(ACO[1:] + [ACO[4]], D.luz(n) - 0.05))
    cabo = J._add(sm, (-4.0, 6.0, 7.0))
    D.capsula(t, "tronco", cabo, J._add(cabo, (-2.0, 9.0, 1.0)), 1.6, 1.6, lambda n, t_, q: _tom(COURO[1:], D.luz(n)))
    D.capsula(t, "tronco", J._add(cabo, (-4.0, 0.0, 0.0)), J._add(cabo, (4.0, 0.0, 0.0)), 1.1, 1.1,
              lambda n, t_, q: _tom(ACO[1:], D.luz(n)))


# ------------------------------------------------------------------ os braços
RAIOS = {"morel": (6.0, 5.4, 5.0, 3.7), "nos": (5.4, 5.0, 4.6, 3.5)}


def _amostras(a, b, ra, rb, n=24):
    return [(J._add(a, J._mul(J._sub(b, a), k / n)), ra + (rb - ra) * k / n) for k in range(n + 1)]


def bracos(t, nome):
    """Os braços vestidos e as sombras que eles fazem no tampo (para `_mesa_cor`)."""
    p = J.poses()[nome]
    sombras = []
    for quem, S, E, W, rampa, punho, cam in (("morel", "ombro_m", "cotovelo_m", "pulso_m", COURO, PUNHO_M, "morel_braco"),
                                            ("nos", "ombro_n", "cotovelo_n", "pulso_n", LA, PUNHO_N, "nosso_braco")):
        rS, rE, rA, rW = RAIOS[quem]
        D.capsula(t, cam, p[S], p[E], rS, rE, volume(rampa))
        # o antebraço de Morel desce só meio tom: contra o tampo na sombra, atrás dele, um tom inteiro some
        D.capsula(t, cam, p[E], p[W], rA, rW, volume(rampa, punho, ante=True, desce=0.06 if quem == "morel" else 0.18))
        sombras += _amostras(p[S], p[E], rS, rE) + _amostras(p[E], p[W], rA, rW) + _amostras(p[W], p["pega"], 4.0, 4.0)
    # o nosso tronco, além do ombro: no escuro, saindo pela borda da esquerda (só a beirada dele aparece)
    D.capsula(t, "nosso_braco", J._add(p["ombro_n"], (-4.0, -2.0, -2.0)), J._add(p["ombro_n"], (-34.0, -6.0, -8.0)), 8.0, 11.0,
              lambda n, t_, q: _tom(LA[3:], D.luz(n) - 0.5))
    # o braço esquerdo de Morel: do ombro à mão que agarra a borda de lá
    se, m = p["ombro_esq_m"], J.MAO_ESQ_MOREL[nome]
    mao = J._add(m, (0.0, 2.5, 0.0))
    e = D.cotovelo(se, mao, (0.35, -1.0, -0.5), 30.0, 28.0)  # o cotovelo para baixo e para a frente
    D.capsula(t, "morel_esquerdo", se, e, 5.8, 5.2, volume(COURO))
    D.capsula(t, "morel_esquerdo", e, mao, 4.8, 3.6, volume(COURO, PUNHO_M, ante=True))
    D.capsula(t, "morel_esquerdo", mao, J._add(mao, (0.0, -1.0, 2.5)), 3.4, 3.0,
              lambda n, t_, q: _tom([PELE_M["q"], PELE_M["w"], PELE_M["w"], PELE_M["e"], PELE_M["e"]], D.luz(n)))
    sombras += _amostras(e, mao, 4.8, 3.6)
    # a sombra no tampo: cada esfera projetada pela luz no plano do tampo, só a que está perto dele (o contato)
    out = []
    for c, r in sombras:
        if c[1] - r > 7:
            continue
        k = c[1] / D.LUZ[1]
        out.append((c[0] - D.LUZ[0] * k + 1.0, c[2] - D.LUZ[2] * k + 1.0, r * 1.05))
    return out, e


# ------------------------------------------------------------------ as pegas
# A pega vem da construção (maos.py: os punhos, os dedos e os polegares no espaço), na pele de cada um (a de Morel mais
# escura e quente), separada pelo valor (`maos.separar`: um pixel de sombra onde uma parte passa atrás da outra, nada de
# contorno), limpa dos pontinhos e retocada à mão onde a construção não basta (RETOQUES).
def _cor_mao(parte, normal):
    parte = parte.split(":")[0]
    s = D.luz(normal)
    nossa = parte.startswith("nos")
    pele = [PELE_N["1"], PELE_N["2"], PELE_N["3"]] if nossa else [PELE_M["q"], PELE_M["w"], PELE_M["e"]]
    if "dedos" in parte:
        s -= 0.25  # os dedos dobrados por cima do dorso do outro, um tom abaixo do dorso
    return pele[0] if s > 0.45 else pele[1] if s > -0.1 else pele[2]


# Os retoques à mão nas pegas (a origem e a grade; "." deixa o que a construção pôs): na disputa, os dedos de Morel
# dobrados sobre o nosso dorso, na diagonal, cada um com a ponta clara (q) e o vão escuro (r) entre eles
RETOQUES = {
    "disputa": ((75, 13), [
        "qq......",
        "rqqw....",
        ".rrqqw..",
        "..qqwr..",
        "..rrqqw.",
        "...qqwr.",
        "...rrqqw",
        "....qwr.",
    ]),
}


def _limpar(mao):
    """Tira os pontinhos: um pixel da mão que não tem nenhum vizinho da mesma cor e é mais escuro que eles volta à cor
    que mais aparece em volta (a separação pelo valor deixa alguns soltos onde as formas se encostam de leve)."""
    from collections import Counter
    out = dict(mao)
    for (x, y), cor in mao.items():
        viz = [mao[q] for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)) if q in mao]
        if len(viz) >= 3 and cor not in viz and sum(cor[:3]) < min(sum(v[:3]) for v in viz):
            out[(x, y)] = Counter(viz).most_common(1)[0][0]
    return out


def _tom_abaixo(cor, quem):
    """Um tom abaixo na pele de quem é (entre dois dedos, embaixo do polegar)."""
    pele = [PELE_N["1"], PELE_N["2"], PELE_N["3"], SOMBRA_PELE["nos"]] if quem == "nos" else         [PELE_M["q"], PELE_M["w"], PELE_M["e"], SOMBRA_PELE["morel"]]
    return pele[min(pele.index(cor) + 1, 3)] if cor in pele else cor


def pose(nome):
    """As camadas de uma pose: os volumes pela profundidade, a pega separada pelo valor e retocada, as guias."""
    import estudo as E
    import maos as M
    t = D.Tela()
    sombras, e = bracos(t, nome)
    cena(t, nome, sombras)
    M.construir(t, nome, _cor_mao)
    c = t.camadas()
    for (q, parte, outra_mao) in M.separar(t):
        c[parte][q] = SOMBRA_PELE[M.dono(parte)] if outra_mao else _tom_abaixo(c[parte][q], M.dono(parte))
    mao = {}
    for parte in list(c):
        if parte.split(":")[0] in M.PARTES:
            mao.update(c.pop(parte))
    mao = _limpar(mao)
    if nome in RETOQUES:  # os retoques à mão, por cima da construção
        (ox, oy), linhas = RETOQUES[nome]
        cores = {"q": PELE_M["q"], "w": PELE_M["w"], "e": PELE_M["e"], "r": SOMBRA_PELE["morel"],
                 "1": PELE_N["1"], "2": PELE_N["2"], "3": PELE_N["3"], "4": SOMBRA_PELE["nos"]}
        for y, linha in enumerate(linhas):
            for x, ch in enumerate(linha):
                if ch in cores:
                    mao[(ox + x, oy + y)] = cores[ch]
    c["maos"] = mao
    c["guia"] = E._guia(nome, e)
    c["dado"] = E._dado()
    return c


def plano(c):
    """As camadas visíveis achatadas (para as prévias sem o Aseprite)."""
    im = Image.new("RGBA", (320, 96), (0, 0, 0, 255))
    for cam in CAMADAS:
        if cam in ("guia", "dado"):
            continue
        for q, cor in c.get(cam, {}).items():
            im.putpixel(q, cor)
    return im


def criar(refazer=False):
    pixels = [pose(n) for n in QUADROS]
    print(fa.montar(FONTE, 320, 96, CAMADAS, QUADROS, pixels, ocultas=("guia", "dado"), refazer=refazer))


def exportar():
    with tempfile.TemporaryDirectory() as tmp:
        qs = fa.quadros(FONTE, tmp, ignorar=("guia", "dado"))
        folha = Image.new("RGBA", (320 * len(qs), 96))
        for i, q in enumerate(qs):
            folha.paste(Image.open(q).convert("RGBA"), (320 * i, 0))
    folha.save(SAIDA, optimize=True)
    # a inspeção: em cima o estudo de construção de cada pose (estudo-queda2.aseprite, sem a área do dado), embaixo a
    # pose acabada
    with tempfile.TemporaryDirectory() as tmp:
        es = [Image.open(q).convert("RGBA") for q in fa.quadros(AQUI / "estudo-queda2.aseprite", tmp, ignorar=("dado",))[:3]]
    comp = Image.new("RGBA", (320 * 3, 192), (24, 22, 20, 255))
    for i in range(3):
        comp.alpha_composite(es[i], (320 * i, 0))
        comp.alpha_composite(folha.crop((320 * i, 0, 320 * i + 320, 96)), (320 * i, 96))
    comp.save(SAIDA.with_name("queda2-construcao.png"), optimize=True)
    print(f"{SAIDA.name}: {len(qs)} poses; queda2-construcao.png")


if __name__ == "__main__":
    if "--criar" in sys.argv or "--refazer" in sys.argv:
        criar("--refazer" in sys.argv)
    elif "--previa" in sys.argv:
        S = pathlib.Path(sys.argv[-1])
        for n in QUADROS:
            plano(pose(n)).save(S / f"q2-{n}.png")
    else:
        exportar()
