"""As três poses da queda de braço diante de Morel (protótipo; só as poses, para a avaliação do Jean, nada animado).

    python ferramentas/prototipos/taverna/morel/queda/poses.py --criar     # monta queda.aseprite (só se não existir)
    python ferramentas/prototipos/taverna/morel/queda/poses.py             # exporta camadas/morel-vista/queda.png

**A fonte** `queda.aseprite` (320×96, três quadros: `disputa`, `vitoria_jogador`, `vitoria_morel`) tem a pilha da vista
aprovada (`morel/vista/morel-vista.aseprite`): a sala, o fogo e o taverneiro parados, Morel com o corpo e a cabeça da
pose `olha` (os olhos em nós) deslocados com o ombro, a mesa, a luz (`sombra` em multiplicar, `brilho` em somar) e as
chamas; e as camadas novas: `morel_esquerdo` (o antebraço esquerdo dele, a mão plantada no tampo), `morel_braco` (o
direito), `nosso_braco` (o nosso antebraço e o braço de cima saindo pela borda de baixo), `maos` (a pega, desenhada à
mão em grade, `PEGAS`) e `guia` (as juntas, oculta). `--criar` monta a fonte uma vez; depois ela é a autoridade.

**O que veio de onde:** as juntas, de `juntas.py` (os comprimentos fixos, a pega no círculo possível; ninguém põe o
cotovelo na tela à mão); os braços vestidos pelo método do `vestir.lua` (estudo-construcao), o que vestiu o braço
aprovado de Morel: o couro em volume com a luz da lareira e da vela, o antebraço um tom abaixo do braço, a sombra do
antebraço no braço, o vinco do cotovelo, o punho da manga escuro, a sombra de um pixel no tampo onde o braço encosta;
a nossa manga é de lã azul-acinzentada (fria, para não se confundir com o couro dele) e a nossa pele um pouco mais
clara; as mãos, desenhadas à mão (a pega do estudo, simplificada em bolinhas de pele, sem dedos). A tigela saiu da
área dos cotovelos (empurrada para a direita dele, a nossa esquerda, na mesma linha do tampo) e o lugar dela ficou
com as tábuas e as juntas, continuando as linhas que fogem para (238, 30)."""
import math
import pathlib
import sys
import tempfile

import numpy as np
from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import fonte_aseprite as fa  # noqa: E402
import juntas as J  # noqa: E402

FONTE = AQUI / "queda.aseprite"
VISTA = AQUI.parent / "vista" / "morel-vista.aseprite"
SAIDA = AQUI.parents[1] / "camadas" / "morel-vista" / "queda.png"
QUADROS = ["disputa", "vitoria_jogador", "vitoria_morel"]
RECORTE = (140, 0, 300, 96)  # a disputa inteira, com Morel, nas folhas de inspeção
CAMADAS = ["parede", "fundo_bar", "fogo", "caldeirao", "taverneiro", "balcao", "cadeira", "morel_corpo",
           "morel_cabeca", "mesa", "morel_esquerdo", "morel_braco", "nosso_braco", "maos", "sombra", "brilho",
           "chamas", "guia"]
FIXAS = ["parede", "fundo_bar", "caldeirao", "balcao", "cadeira", "sombra", "brilho"]
MODOS = {"sombra": 14, "brilho": 29}
OLHA = 19  # a pose da vista em que Morel olha para quem está à mesa (o quadro da fonte menos 1)

H = lambda s: tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))  # noqa: E731
# o couro de Morel (vestir.lua, V4) e a pele dele
MOREL = {"j": H("8a5a38"), "a": H("6a4a2c"), "b": H("4e3420"), "c": H("33231a"), "l": H("2a1c14"), "w": H("1f150e"),
         "punho": (H("3a2716"), H("2a1c14")), "pele": (H("c09070"), H("9a6c52"), H("6c4a38"))}
# a nossa manga: lã azul-acinzentada, fria; a pele um pouco mais clara que a dele
NOSSO = {"j": H("7c889a"), "a": H("5e6878"), "b": H("474f5d"), "c": H("333a45"), "l": H("262b34"), "w": H("1c2027"),
         "punho": (H("3a4150"), H("262b34")), "pele": (H("d6a888"), H("ae7c5e"), H("7a5440"))}
LUZ = (-0.6, -0.55, 0.58)
_n = math.sqrt(sum(v * v for v in LUZ))
LUZ = tuple(v / _n for v in LUZ)
DESCE = {"j": "a", "a": "b", "b": "c", "c": "l", "l": "w", "w": "w"}

# o braço esquerdo de Morel: o braço de cima é o do corpo (TRONCO4 em vestir.lua: do ombro em (238, 35) ao cotovelo em
# (247, 61)); o antebraço vai do cotovelo à mão plantada no tampo, à direita do nosso antebraço, diante do pão
MAO_ESQUERDA = {"disputa": (264, 70), "vitoria_jogador": (262, 71), "vitoria_morel": (265, 70)}
# a tigela empurrada: o deslocamento dela na tela (a mesma linha do tampo)
TIGELA_DX = -46


# ------------------------------------------------------------------ o volume (vestir.lua, em Python)
def volume(mapa, parte, a, b, ra, rb, realce=False, ante=False):
    (ax, ay), (bx, by) = a, b
    dx, dy = bx - ax, by - ay
    L2 = max(dx * dx + dy * dy, 1)
    r = max(ra, rb)
    tmp = {}
    for y in range(math.floor(min(ay, by) - r) - 1, math.ceil(max(ay, by) + r) + 2):
        for x in range(math.floor(min(ax, bx) - r) - 1, math.ceil(max(ax, bx) + r) + 2):
            px, py = x + 0.5, y + 0.5
            t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
            rr = ra + (rb - ra) * t
            ox, oy = px - (ax + t * dx), py - (ay + t * dy)
            if ox * ox + oy * oy <= rr * rr:
                nx, ny = ox / rr, oy / rr
                nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
                s = nx * LUZ[0] + ny * LUZ[1] + nz * LUZ[2]
                tom = ("j" if realce or ante else "a") if s > 0.78 else "a" if s > 0.5 else "b" if s > 0.12 else \
                    "c" if s > -0.25 else "l"
                tmp[(x, y)] = {"parte": parte, "tom": DESCE[tom] if ante else tom, "t": t}
    mapa.update(tmp)


def braco(pal, S, E, W, rS, rE, rW, rC, sombra_em=None):
    """Um braço vestido (o de cima de S a E, o antebraço de E a W, na frente): {(x, y): cor} e os pixels do antebraço
    que encostam no tampo (para a sombra). `S` None: só o antebraço."""
    mapa = {}
    if S:
        volume(mapa, "braco", S, E, rS, rE, realce=True)
    fo = {}
    volume(fo, "ante", E, W, rC, rW, ante=True)
    mapa.update(fo)
    if S:
        for (x, y), v in mapa.items():  # a sombra do antebraço no braço
            if v["parte"] == "braco" and any(mapa.get(q, {}).get("parte") == "ante" for q in ((x - 1, y), (x, y - 1), (x - 1, y - 1))):
                v["tom"] = "l"
        ux, uy = S[0] - E[0], S[1] - E[1]
        vx, vy = W[0] - E[0], W[1] - E[1]
        nu, nv = math.hypot(ux, uy), math.hypot(vx, vy)
        ux, uy, vx, vy = ux / nu, uy / nu, vx / nv, vy / nv
        if ux * vx + uy * vy > -0.5:  # o vinco de dentro do cotovelo, quando dobra mais de 120°
            bx, by = ux + vx, uy + vy
            nb = math.hypot(bx, by)
            if nb > 0.01:
                for k in range(1, 5):
                    p = mapa.get((math.floor(E[0] + bx / nb * k + 0.5), math.floor(E[1] + by / nb * k + 0.5)))
                    if p:
                        p["tom"] = "l"
    out = {}
    for q, v in mapa.items():
        cor = pal[v["tom"]]
        if v["parte"] == "ante" and v["t"] > 0.86:  # o punho da manga
            cor = pal["punho"][0] if v["tom"] in ("j", "a", "b") else pal["punho"][1]
        out[q] = cor
    return out


def mao(pal, c, rx, ry):
    out = {}
    for y in range(math.floor(c[1]) - 4, math.floor(c[1]) + 5):
        for x in range(math.floor(c[0]) - 4, math.floor(c[0]) + 5):
            ox, oy = (x + 0.5 - c[0]) / rx, (y + 0.5 - c[1]) / ry
            if ox * ox + oy * oy <= 1:
                s = -ox * 0.7 - oy * 0.7
                out[(x, y)] = pal["pele"][0] if s > 0.35 else pal["pele"][1] if s > -0.45 else pal["pele"][2]
    return out


def sombra_no_tampo(figura, mesa_cor, perto):
    """A sombra de um pixel (do lado oposto à luz) no tampo, só junto do que encosta nele (`perto(x, y)`)."""
    out = {}
    for (x, y) in figura:
        if not perto(x, y):
            continue
        for dx, dy in ((1, 0), (0, 1), (1, 1)):
            q = (x + dx, y + dy)
            if q not in figura and q in mesa_cor:
                r, g, b = mesa_cor[q][:3]
                out[q] = (int(r * 0.68), int(g * 0.68), int(b * 0.68), 255)
    return out


# ------------------------------------------------------------------ a pega, à mão
# m/M/D a mão de Morel (pele clara, média, sombra); s/S/E a nossa; "." vazio. A origem da grade fica no meio da pega
# (o `pega` de juntas.py na tela): (ox, oy) é o canto de cima da grade em relação a ele.
PEGAS = {
    # a disputa: os polegares cruzados em cima (o nosso por cima do dele), os nossos dedos dobrados sobre o dorso da mão
    # dele (à esquerda), os dedos dele sobre o nosso dorso (à direita); embaixo, os dois punhos entrando nos antebraços,
    # com o vão entre eles
    "disputa": ((-5, -7), [
        "...Mm......",
        "..MMssS....",
        ".MMsssssS..",
        "sMMSssssSD.",
        "sMMSsssSSMD",
        "SMDSSssSSMD",
        "SDDSSSsSSD.",
        ".DMESSSSSE.",
        ".DMDESSSE..",
        ".DD..ESSSE.",
        ".D....ESE..",
    ]),
    # nós vencendo: o nosso punho por cima, deitado para a esquerda, prendendo a mão dele contra o tampo; da dele
    # aparecem os dedos na ponta da esquerda e a borda embaixo
    "vitoria_jogador": ((-5, -5), [
        "....ss........",
        "..sssssS......",
        ".ssssssSSE....",
        "MssSSSSSSSE...",
        "MmSSSSSSEEE...",
        "DMMDDSEE......",
        ".DDDD.........",
    ]),
    # Morel vencendo: a mão dele por cima, deitada para a direita; da nossa, presa embaixo, aparecem os dedos além da
    # dele e a borda que desce para o nosso punho
    "vitoria_morel": ((-7, -6), [
        ".......SS......",
        "......sSSE.....",
        "..mmmmmmMMS....",
        ".mmmmmmMMMMD...",
        "MMmmMMMMMMMDD..",
        "DMMMMMMMMMDD...",
        ".DDMMMDDDSE....",
        "....DD..SSE....",
    ]),
}


def pega(nome, centro):
    (ox, oy), linhas = PEGAS[nome]
    cor = {"m": MOREL["pele"][0], "M": MOREL["pele"][1], "D": MOREL["pele"][2],
           "s": NOSSO["pele"][0], "S": NOSSO["pele"][1], "E": NOSSO["pele"][2]}
    out = {}
    cx, cy = round(centro[0]), round(centro[1])
    for y, linha in enumerate(linhas):
        for x, ch in enumerate(linha):
            if ch in cor:
                out[(cx + ox + x, cy + oy + y)] = cor[ch] + (255,)
    return out


# ------------------------------------------------------------------ a mesa com a tigela empurrada
def mesa_sem_tigela(mesa):
    """A camada `mesa` (sem luz) com a tigela levada TIGELA_DX px para a esquerda; o lugar dela (uma elipse que cobre a
    tigela e a sombra de contato dela) ganha as tábuas e as juntas pelas linhas que fogem para (238, 30): cada pixel
    copia o da mesma linha de fuga mais perto de nós. O que muda nesse lugar (a tigela e a sombra) vai junto para o
    lugar novo; o que já está lá na frente (a vela) fica na frente."""
    a = np.array(mesa)
    buraco = {(x, y) for y in range(60, 86) for x in range(190, 242)
              if ((x + 0.5 - 215.5) / 21.5) ** 2 + ((y + 0.5 - 73) / 10.5) ** 2 <= 1 and a[y, x, 3]}
    out = a.copy()
    for (x, y) in buraco:
        u = (x - 238) / (y - 30)
        for yy in range(87, 92):
            xx = round(238 + u * (yy - 30))
            if a[yy, xx, 3]:
                out[y, x] = a[yy, xx]
                break
    madeira = {tuple(a[y, x]) for y in range(62, 92) for x in range(238, 250) if a[y, x, 3]}
    for (x, y) in buraco:
        if tuple(a[y, x]) != tuple(out[y, x]):
            q = (x + TIGELA_DX, y)
            if tuple(a[q[1], q[0]]) in madeira:
                out[q[1], q[0]] = a[y, x]
    return out


def _pixels(img, dx=0, dy=0):
    a = np.array(img.convert("RGBA"))
    ys, xs = np.nonzero(a[:, :, 3])
    return {(int(x) + dx, int(y) + dy): tuple(int(v) for v in a[y, x]) for y, x in zip(ys, xs)}


def criar(refazer=False):
    with tempfile.TemporaryDirectory() as tmp:
        cel = fa.celulas(VISTA, pathlib.Path(tmp) / "cel")
        L = lambda n, q=0: Image.open(cel / f"{n}-{q}.png").convert("RGBA")  # noqa: E731
        mesa = mesa_sem_tigela(L("mesa"))
        mesa_cor = {(x, y): tuple(int(v) for v in mesa[y, x]) for y in range(96) for x in range(320) if mesa[y, x, 3]}
        fixas = {n: _pixels(L(n)) for n in FIXAS}
        fogo, chamas, tav = _pixels(L("fogo", 1)), _pixels(L("chamas", 1)), _pixels(L("taverneiro"))
        corpo, cabeca = L("morel_corpo", OLHA), L("morel_cabeca", OLHA)
        quadros = []
        for nome in QUADROS:
            p = J.poses()[nome]
            T = lambda q: tuple(round(v) for v in J.tela(q))  # noqa: E731
            S, E, W, P = T(p["ombro_m"]), T(p["cotovelo_m"]), T(p["pulso_m"]), T(p["pega"])
            dx, dy = round((S[0] - 198) / 2), round((S[1] - 35) / 2)  # o tronco acompanha o ombro, 1 px por 2 dele
            c = dict(fixas)
            c.update(fogo=fogo, chamas=chamas, taverneiro=tav, mesa=mesa_cor,
                     morel_corpo=_pixels(corpo, dx, dy), morel_cabeca=_pixels(cabeca, dx, dy))
            # o braço esquerdo de Morel: o antebraço do cotovelo do corpo até a mão plantada
            Ee = (247 + dx, 61 + dy)
            esq = braco(MOREL, None, Ee, MAO_ESQUERDA[nome], 0, 0, 3.5, 4.6)
            esq.update(mao(MOREL, MAO_ESQUERDA[nome], 3.0, 2.6))
            esq = {q: v + (255,) for q, v in esq.items()}
            esq.update(sombra_no_tampo(esq, mesa_cor, lambda x, y: True))
            c["morel_esquerdo"] = esq
            # o braço direito: o cotovelo maior quando o braço aponta para nós
            dir_ = braco(MOREL, S, E, W, 5.6, 4.6 if math.dist(S, E) >= 22 else 5.1, 3.3, 4.6)
            dir_ = {q: v + (255,) for q, v in dir_.items()}
            dir_.update(sombra_no_tampo(dir_, mesa_cor, lambda x, y, E=E, W=W, n=nome: math.dist((x, y), E) < 7
                                        or (n == "vitoria_morel" and y >= 60)))
            corpo_px = c["morel_corpo"]
            for (x, y) in list(dir_):  # a sombra de um pixel do braço no casaco (do lado oposto à luz)
                for ddx, ddy in ((1, 0), (0, 1), (1, 1)):
                    q = (x + ddx, y + ddy)
                    if q not in dir_ and q in corpo_px and q not in mesa_cor:
                        r, g, b = corpo_px[q][:3]
                        dir_[q] = (int(r * 0.68), int(g * 0.68), int(b * 0.68), 255)
            c["morel_braco"] = dir_
            # o nosso: o braço de cima saindo pela borda de baixo, o antebraço por cima dele
            B, Wn = T(p["cotovelo_n"]), T(p["pulso_n"])
            nos = braco(NOSSO, J.OMBRO_NOSSO_TELA, B, Wn, 7.5, 6.8, 4.4, 6.5)
            nos = {q: v + (255,) for q, v in nos.items() if 0 <= q[0] < 320 and 0 <= q[1] < 96}
            nos.update(sombra_no_tampo(nos, mesa_cor, lambda x, y, B=B, n=nome: math.dist((x, y), B) < 9
                                       or n in ("vitoria_jogador", "vitoria_morel")))
            c["nosso_braco"] = nos
            c["maos"] = pega(nome, P)
            guia = {}
            for q, cor in ((S, (255, 64, 64)), (E, (48, 255, 96)), (W, (48, 128, 255)), (B, (48, 255, 96)),
                           (Wn, (48, 128, 255)), (P, (255, 224, 48))):
                guia[q] = cor + (255,)
            c["guia"] = guia
            quadros.append(c)
    print(fa.montar(FONTE, 320, 96, CAMADAS, QUADROS, quadros, ocultas=("guia",), modos=MODOS, refazer=refazer))


def exportar():
    """As três poses achatadas, lado a lado (320×96 cada), para o painel mostrar na área de cena da HUD."""
    with tempfile.TemporaryDirectory() as tmp:
        qs = fa.quadros(FONTE, tmp, ignorar=("guia",))
        folha = Image.new("RGBA", (320 * len(qs), 96))
        for i, q in enumerate(qs):
            folha.paste(Image.open(q).convert("RGBA"), (320 * i, 0))
    folha.save(SAIDA, optimize=True)
    # a inspeção: em cima o estudo de construção de cada pose (estudo-queda.aseprite), embaixo a pose vestida, no recorte
    # da disputa (160×96 cada), como a folha do estudo do braço de Morel
    estudo = AQUI / "estudo-queda.aseprite"
    with tempfile.TemporaryDirectory() as tmp:
        es = [Image.open(q).convert("RGBA") for q in fa.quadros(estudo, tmp)[:3]]
    comp = Image.new("RGBA", (160 * 3, 192), (24, 22, 20, 255))
    for i in range(3):
        comp.alpha_composite(es[i].crop(RECORTE), (160 * i, 0))
        comp.alpha_composite(folha.crop((320 * i + RECORTE[0], 0, 320 * i + RECORTE[2], 96)), (160 * i, 96))
    comp.save(SAIDA.with_name("queda-construcao.png"), optimize=True)
    print(f"{SAIDA.name}: {len(qs)} poses; queda-construcao.png")


if __name__ == "__main__":
    if "--criar" in sys.argv or "--refazer" in sys.argv:
        criar("--refazer" in sys.argv)
    else:
        exportar()
