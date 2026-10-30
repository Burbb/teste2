"""O acabamento da manga do braço da colher de Morel (protótipo): uma manga só, do ombro ao punho, sobre a construção.

    python ferramentas/prototipos/taverna/morel/vista/manga.py --previa <pasta>   # as três poses-chave, antes e depois
    python ferramentas/prototipos/taverna/morel/vista/manga.py --aplicar          # grava a camada morel_braco da fonte
                                                                                  # (os 20 quadros, com os RETOQUES)
    python ferramentas/prototipos/taverna/morel/vista/manga.py --folha            # a folha antes e depois (inspeção)

**A causa** (30/10/2026, a marcação do Jean no ombro e no cotovelo): o `vestir.lua` (estudo-construcao) vestia o braço
como duas cápsulas, o braço e o antebraço, cada uma com o próprio sombreamento em faixas paralelas às bordas. O alto da
cápsula do braço terminava numa calota redonda acima da linha do ombro do tronco (o tronco é uma forma reta, sem
braço), e o antebraço inteiro descia um tom de uma vez, exatamente na junta, com o vinco como um traço escuro entre as
duas: o ombro lia como uma peça encaixada e o cotovelo como uma dobradiça. A construção (as juntas, os comprimentos, o
alcance da colher) estava certa; o acabamento é que contornava cada segmento.

**O tratamento:** as mesmas juntas (as da camada `guia` da fonte e o ombro de `juntas.py`), os mesmos raios, e:
- uma forma só: as duas cápsulas unidas por uma união suave do lado de fora do cotovelo (a curva); por dentro, o
  antebraço continua passando na frente do braço, com a luz dele e a sombra que ele faz no braço (com a união suave
  também por dentro, o V do braço bem dobrado se enchia e o antebraço sumia no bíceps: o Jean, 30/10/2026); sem calota
  no ombro: o que passaria do ombro para cima some fora do tronco e, dentro dele, vira o
  alto da manga continuando a linha do ombro do casaco;
- a luz de uma superfície só (a normal pela distância à borda da forma unida), em três tons de couro e o realce só nos
  pontos mais acesos: o grupo de luz passa do braço para o antebraço pela curva do cotovelo;
- o antebraço escurece aos poucos (meio tom), alguns pixels depois da junta, não na junta;
- a compressão por dentro do cotovelo: uma dobra de dois pixels do lado de dentro da curva para a junta (com três, na
  boca, lia como um corte), com o pixel aceso da crista ao lado (nada de mancha escura no lugar da junta);
- o alto da manga, fora do tronco, só até a linha do ombro (uns 4 px acima da junta, descendo para fora): o deltoide
  continua a inclinação do ombro do casaco;
- o punho escuro da manga, a sombra de um pixel no peito e no tampo, e a mão e a colher exatamente como estavam (os
  contatos com a tigela e a boca são os aprovados).
O que sai daqui é candidato: as poses são revistas uma a uma, paradas e em sequência, e os retoques à mão (RETOQUES)
entram por cima e ficam no código, então refazer a manga não os apaga. Depois de gravada, a fonte é a autoridade."""
import math
import pathlib
import shutil
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[4]
sys.path.insert(0, str(AQUI.parent / "estudo-construcao"))
sys.path.insert(0, str(RAIZ / "ferramentas" / "arte"))

import juntas as JC  # noqa: E402
from exportar_aseprite import aseprite  # noqa: E402

FONTE = AQUI / "morel-vista.aseprite"
CELULAS = RAIZ / "ferramentas" / "prototipos" / "hud" / "forja" / "h2" / "aseprite" / "exportar_forja.lua"
H = lambda s: (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), 255)  # noqa: E731
COURO = {"j": H("8a5a38"), "a": H("6a4a2c"), "b": H("4e3420"), "c": H("33231a"), "l": H("2a1c14")}
PUNHO = (H("3a2716"), H("2a1c14"))
# o que fica da camada anterior: a mão, a colher, o caldo na concha
MAO_COLHER = {H(c)[:3] for c in ("c09070", "9a6c52", "6c4a38", "9a9ca4", "cfd1d6", "6a2a14")}
R4 = {"ombro": 5.6, "cotovelo": 4.6, "cotoveloPerto": 5.1, "antebraco": 4.6, "punho": 3.3}
LUZ = (-0.6, -0.55, 0.58)
_n = math.sqrt(sum(v * v for v in LUZ))
LUZ = tuple(v / _n for v in LUZ)
COR_JUNTA = {(48, 255, 96): "E", (48, 128, 255): "W", (255, 224, 48): "T"}

# Os retoques à mão, por pose (o índice do quadro da fonte menos 1): {(x, y): tom}, com "." apagando o pixel. Entram
# por cima do candidato e ficam aqui, então refazer a manga não os perde.
RETOQUES = {}


def _seg(p, a, b):
    ax, ay = a
    dx, dy = b[0] - ax, b[1] - ay
    L2 = max(dx * dx + dy * dy, 1e-9)
    t = max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2))
    return t, math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy)


def _cap(p, a, b, ra, rb):
    t, d = _seg(p, a, b)
    r = ra + (rb - ra) * t
    return d - r, t, r


def _smin(a, b, k):
    h = max(k - abs(a - b), 0.0) / k
    return min(a, b) - h * h * k * 0.25


def manga(S, E, W, corpo_alfa, k=2.4, vinco=True):
    """O candidato: {(x, y): cor} da manga (sem a mão nem a colher) e o conjunto dos pixels dela. `vinco`: a dobra
    marcada por dentro do cotovelo (sem ela quando o cotovelo pousa visto de cima e a marca cai no meio do antebraço)."""
    rE = R4["cotoveloPerto"] if math.dist(S, E) < 22 else R4["cotovelo"]

    # o ombro: o eixo do braço, para saber o que passa do ombro para cima
    ex, ey = E[0] - S[0], E[1] - S[1]
    nL = math.hypot(ex, ey)
    ux, uy = ex / nL, ey / nL
    # o comprimento ao longo da manga (do ombro ao punho), para o escurecimento do antebraço e o punho
    L1, L2 = math.dist(S, E), math.dist(E, W)
    # a dobra: o lado de dentro do cotovelo (a bissetriz entre o braço e o antebraço)
    vx, vy = (W[0] - E[0]) / L2, (W[1] - E[1]) / L2
    bx, by = -ux + vx, -uy + vy
    nb = math.hypot(bx, by)
    dobra = (bx / nb, by / nb) if nb > 0.15 else None  # quase reto: sem dobra

    def dentro(p):
        """Do lado de dentro do cotovelo (onde o antebraço se dobra sobre o braço)?"""
        return dobra is not None and (p[0] - E[0]) * dobra[0] + (p[1] - E[1]) * dobra[1] > 0

    def ante(p):
        return _cap(p, E, W, R4["antebraco"], R4["punho"])[0]

    def f(p):
        """A forma da manga: a união suave só do lado de fora do cotovelo (a curva); por dentro, o antebraço por cima
        do braço como ele é (com o braço bem dobrado, a união suave enchia o V e o antebraço sumia no bíceps)."""
        a = _cap(p, S, E, R4["ombro"], rE)[0]
        b = ante(p)
        return min(a, b) if dentro(p) else _smin(a, b, k)
    out = {}
    manga.antebraco = set()  # os pixels do antebraço (passam na frente da ombreira quando a colher vai à boca)
    frente = set()  # os pixels do antebraço que passa na frente do braço
    x0, x1 = int(min(S[0], E[0], W[0]) - 8), int(max(S[0], E[0], W[0]) + 8)
    y0, y1 = int(min(S[1], E[1], W[1]) - 8), int(max(S[1], E[1], W[1]) + 8)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            p = (x + 0.5, y + 0.5)
            d = f(p)
            if d > 0:
                continue
            # o que passa do ombro para cima: some fora do tronco; dentro dele, a manga continua o ombro do casaco
            alem = (p[0] - S[0]) * ux + (p[1] - S[1]) * uy
            # fora do tronco, o alto da manga só vai até a linha do ombro: o alto do ombro uns 4 px acima da junta,
            # descendo para fora (o deltoide continuando a inclinação do ombro do casaco, sem calota por cima)
            if alem < -0.5 and not corpo_alfa(x, y) and p[1] < S[1] - 4 + 0.8 * max(0.0, S[0] - p[0]):
                continue
            # a normal: a da superfície unida; onde o antebraço passa na frente do braço (por dentro do cotovelo), a do
            # próprio antebraço, que tem a sua luz e a sua borda
            h = 0.5
            g = ante if (ante(p) <= 0 and dentro(p)) else f
            if g is ante:
                frente.add((x, y))
                d = ante(p)
            gx = g((p[0] + h, p[1])) - g((p[0] - h, p[1]))
            gy = g((p[0], p[1] + h)) - g((p[0], p[1] - h))
            ng = math.hypot(gx, gy) or 1.0
            gx, gy = gx / ng, gy / ng
            ta, da = _seg(p, S, E)
            tb, db = _seg(p, E, W)
            r = (R4["ombro"] + (rE - R4["ombro"]) * ta) if da <= db else (R4["antebraco"] + (R4["punho"] - R4["antebraco"]) * tb)
            e = min(1.0, max(0.0, 1.0 + d / r))   # 0 no meio, 1 na borda
            nx, ny = gx * e, gy * e
            nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
            s = nx * LUZ[0] + ny * LUZ[1] + nz * LUZ[2]
            # ao longo da manga: 0 no ombro, L1 no cotovelo, L1 + L2 no punho
            u = ta * L1 if da <= db and ta < 1 else L1 + tb * L2
            if u > L1:
                manga.antebraco.add((x, y))
            if u > L1 + 3:   # o antebraço escurece aos poucos, depois da junta: meio tom
                s -= min(0.16, (u - L1 - 3) * 0.04)
            if u > L1 + 0.86 * L2:  # o punho da manga
                out[(x, y)] = PUNHO[0] if s > 0.1 else PUNHO[1]
                continue
            tom = "j" if s > 0.8 else "a" if s > 0.42 else "b" if s > 0.0 else "c"
            if alem < 0 and tom == "c":
                tom = "b"  # o alto da manga, dentro do ombro do casaco, sem a borda escura de uma peça encaixada
            out[(x, y)] = COURO[tom]
    # a sombra que o antebraço faz no braço onde passa na frente dele (do lado oposto à luz): a sobreposição, que separa
    # o antebraço do bíceps quando o braço dobra muito; perto da junta, por fora, não (ali a manga é uma curva só)
    for (x, y) in list(out):
        if (x, y) in frente or (x, y) not in out:
            continue
        if any(q in frente for q in ((x - 1, y), (x, y - 1), (x - 1, y - 1))) and dentro((x + 0.5, y + 0.5))                 and out[(x, y)] not in PUNHO:
            out[(x, y)] = COURO["c"]
    # a compressão por dentro do cotovelo: uma dobra curta, do lado de dentro da curva para a junta, e o pixel aceso
    # da crista ao lado dela (do lado da luz); nada de mancha no lugar da junta
    if dobra and vinco:
        perp = (-dobra[1], dobra[0])
        if perp[0] * LUZ[0] + perp[1] * LUZ[1] < 0:
            perp = (-perp[0], -perp[1])  # para o lado da luz
        c0 = (E[0] + dobra[0] * (rE - 0.6), E[1] + dobra[1] * (rE - 0.6))
        for s2, tom in ((0.0, "c"), (1.0, "b")):  # dois pixels: o fundo da dobra e a saída dela
            q = (math.floor(c0[0] - dobra[0] * s2), math.floor(c0[1] - dobra[1] * s2))
            if q in out:
                out[q] = COURO[tom]
        luz = (math.floor(c0[0] + perp[0] * 1.1 - dobra[0] * 0.5), math.floor(c0[1] + perp[1] * 1.1 - dobra[1] * 0.5))
        if luz in out and out[luz] != COURO["c"]:
            out[luz] = COURO["a"]
    return out


def _juntas_fonte(cel):
    """As juntas de cada quadro (a camada guia da fonte) e o ombro (juntas.py)."""
    P = JC.poses()
    out = []
    for k in range(len(P)):
        g = np.array(Image.open(cel / f"guia-{k}.png").convert("RGB"))
        j = {}
        for cor, nome in COR_JUNTA.items():
            ys, xs = np.nonzero((g == cor).all(2))
            if len(xs):
                j[nome] = (int(xs[0]) + 0.5, int(ys[0]) + 0.5)
        j["S"] = (P[k]["S"][0] + 0.5, P[k]["S"][1] + 0.5)
        out.append(j)
    return out


def _celulas(tmp, fonte=FONTE, nome="cel"):
    pasta = pathlib.Path(tmp) / nome
    pasta.mkdir()
    script = pathlib.Path(tmp) / "celulas.lua"
    shutil.copy(CELULAS, script)
    subprocess.run([aseprite(), "-b", "--script-param", f"fonte={fonte}", "--script-param", f"pasta={pasta}",
                    "--script", str(script)], capture_output=True, text=True)
    return pasta


# ------------------------------------------------------------------ as ombreiras (o Jean, 30/10/2026)
# Nas outras versões de Morel no jogo (o retrato de retratos.js, a figura de 16 px), ele tem duas ombreiras: a do ombro
# direito em aço claro, com a guarda da espada logo acima, e a do esquerdo mais escura. A vista tinha só a esquerda, e o
# couro do ombro aparecia acima e além da borda de cima dela.
PLACA = {H("4e4640")[:3], H("6a6058")[:3], H("34302c")[:3]}
COURO_ROUPA = {H("6a4a2c")[:3], H("8a5a38")[:3], H("4e3420")[:3]}
REPOUSO = 17          # o quadro de referência (o tronco e o ombro de repouso)
OMBRO_REPOUSO = (198, 35)


def _dy_corpo(cel, k):
    """Quanto o tronco do quadro k está deslocado em relação ao do repouso (a mesma imagem, deslocada)."""
    topo = lambda q: Image.open(cel / f"morel_corpo-{q}.png").getbbox()[1]  # noqa: E731
    return topo(k) - topo(REPOUSO)


# o fim da placa esquerda em cada linha de cima (no repouso): o canto de cima arredondado, seguindo o contorno do ombro,
# e a fresta escura logo depois; nada passa do contorno (a primeira correção estendia a placa sobre o fundo, numa
# lâmina horizontal que o Jean marcou)
FIM_PLACA = {29: 237, 30: 239, 31: 240, 32: 241, 33: 241}
ORIGINAL = AQUI.parent / "vista-v3" / "morel-vista.aseprite"  # o tronco antes de qualquer correção da ombreira


def corpo_corrigido(cel, k, original):
    """O tronco do quadro k com a ombreira esquerda cobrindo o alto do ombro, a partir do tronco original (as células
    da versão anterior em `original`): em cada linha de cima, a placa vai da borda dela até FIM_PLACA (o alto aceso na
    primeira linha) e a fresta escura fecha a curva, só dentro do contorno do ombro."""
    im = np.array(Image.open(original / f"morel_corpo-{k}.png").convert("RGBA"))
    dy = _dy_corpo(cel, k)
    for y0, fim in FIM_PLACA.items():
        y = y0 + dy
        xs = [x for x in range(226, 246) if im[y, x, 3] and tuple(im[y, x, :3]) in PLACA]
        if not xs:
            continue
        for x in range(max(xs) + 1, fim + 1):
            im[y, x] = H("6a6058") if y0 == 29 else H("4e4640")
        if im[y, fim + 1, 3]:
            im[y, fim + 1] = H("34302c")
    return Image.fromarray(im, "RGBA")


# a ombreira direita, à mão: a calota no alto do ombro (como no retrato), com a borda de cima acesa do lado da luz, a
# fileira de rebites (o pontilhado da esquerda), a borda de baixo escura e a sombra no braço; inclinada como a linha do
# ombro (alta junto ao pescoço, descendo para fora), assentada na raiz do braço, entre a borda de fora dele e a do
# tronco (a borda de fora do braço fica em x 194 nessa altura); o canto de cima à esquerda em (193, 30), logo abaixo
# da guarda da espada (y 29), no ombro de repouso
OMBREIRA_DIR = [
    "........hhhh...",
    ".....hhSSSSSs..",
    "...hSSSSSSSSss.",
    "..hSSmSmSmSSsss",
    ".hSSSSSSSSSsssm",
    "hSSmSmSmSmmmmd.",
    "SSmmmmmmmmmdd..",
    "mmmmmmmmmddk...",
    ".ddddddddk.....",
    "..cccccc.......",
]
_OMB_COR = {"h": H("c4c6cc"), "S": H("9a9ca4"), "s": H("7a7c84"), "m": H("6e7078"), "d": H("4e4640"),
            "k": H("34302c"), "c": COURO["c"]}


def ombreira_direita(S):
    """A ombreira direita no quadro: acompanha a junta do ombro (o ombro sobe e entra 1 px quando a colher vai à boca)."""
    dx, dy = round(S[0] - 0.5) - OMBRO_REPOUSO[0], round(S[1] - 0.5) - OMBRO_REPOUSO[1]
    out = {}
    for y, linha in enumerate(OMBREIRA_DIR):
        for x, ch in enumerate(linha):
            if ch in _OMB_COR:
                out[(193 + x + dx, 30 + y + dy)] = _OMB_COR[ch]
    return out


def braco(cel, k, j):
    """A camada morel_braco do quadro k: a manga nova, a sombra de um pixel no que está embaixo, a mão e a colher de
    antes, e os retoques à mão."""
    corpo = np.array(Image.open(cel / f"morel_corpo-{k}.png").convert("RGBA"))
    mesa = np.array(Image.open(cel / f"mesa-{k}.png").convert("RGBA")) if (cel / f"mesa-{k}.png").exists() else \
        np.array(Image.open(cel / "mesa-0.png").convert("RGBA"))
    antes = np.array(Image.open(cel / f"morel_braco-{k}.png").convert("RGBA"))
    alfa = lambda x, y: 0 <= x < 320 and 0 <= y < 96 and corpo[y, x, 3] > 0  # noqa: E731
    m = manga(j["S"], j["E"], j["W"], alfa)
    # a mão e a colher de antes, por cima (o que tem a cor delas na camada antiga)
    mao = {}
    ys, xs = np.nonzero(antes[:, :, 3])
    for y, x in zip(ys, xs):  # só perto do pulso e da colher (a ombreira, também de aço, fica de fora)
        if tuple(antes[y, x, :3]) in MAO_COLHER and _seg((x + 0.5, y + 0.5), j["W"], j.get("T", j["W"]))[1] <= 6:
            mao[(int(x), int(y))] = tuple(int(v) for v in antes[y, x])
    out = dict(m)
    out.update(mao)
    # a sombra de um pixel no peito e no tampo, do lado oposto à luz (como antes)
    ocup = set(out)
    for (x, y) in list(ocup):
        for dx, dy in ((1, 0), (0, 1), (1, 1)):
            q = (x + dx, y + dy)
            if q in ocup or q in out or not (0 <= q[0] < 320 and 0 <= q[1] < 96):
                continue
            for camada in (mesa, corpo):
                if camada[q[1], q[0], 3]:
                    r, g, b = camada[q[1], q[0], :3]
                    out[q] = (int(r * 0.68), int(g * 0.68), int(b * 0.68), 255)
                    break
    # a ombreira por cima da manga, mas atrás do antebraço e da mão (na boca, o antebraço sobe na frente do ombro)
    calota = ombreira_direita(j["S"])
    for q, cor in calota.items():
        if q not in manga.antebraco and q not in mao:
            out[q] = cor
    # o que a manga deixava aparecer em volta da calota (o alto do braço antigo: um ou dois pixels marrons à esquerda
    # dela, e a beirada de cima quando o ombro sobe para a boca): acima da ponta esquerda da calota, nada da manga passa
    # para fora dela
    placa = {q for q, cor in calota.items() if cor != COURO["c"]}
    ponta = min(placa, key=lambda q: (q[0], -q[1]))[1]  # a linha da ponta esquerda da calota
    for y in range(min(yy for _, yy in placa) - 3, ponta):
        xs = [x for x, yy in placa if yy == y]
        for x in range(min(xs) - 5 if xs else 0, min(xs) if xs else 0):
            if (x, y) in out and (x, y) not in mao and (x, y) not in manga.antebraco:
                del out[(x, y)]
        if not xs:  # acima da calota (a beirada de cima): só o que fica sobre ela
            for x in range(min(xx for xx, _ in placa), max(xx for xx, _ in placa) + 1):
                if (x, y) in out and (x, y) not in mao and (x, y) not in manga.antebraco:
                    del out[(x, y)]
    for q, tom in RETOQUES.get(k, {}).items():
        if tom == ".":
            out.pop(q, None)
        else:
            out[q] = COURO[tom] if tom in COURO else H(tom)
    img = Image.new("RGBA", (320, 96), (0, 0, 0, 0))
    for q, cor in out.items():
        if 0 <= q[0] < 320 and 0 <= q[1] < 96:
            img.putpixel(q, cor)
    return img


_GRAVAR = r'''
local s = app.open(app.params["fonte"])
local camada, corpo
for _, l in ipairs(s.layers) do
  if l.name == "morel_braco" then camada = l end
  if l.name == "morel_corpo" then corpo = l end
end
local n = 0
app.transaction("A manga nova e as ombreiras", function()
  for i, f in ipairs(s.frames) do
    local img = Image{ fromFile = app.params["pasta"] .. "/braco-" .. (i - 1) .. ".png" }
    s:newCel(camada, f, img, Point(0, 0))
    local tr = Image{ fromFile = app.params["pasta"] .. "/corpo-" .. (i - 1) .. ".png" }
    s:newCel(corpo, f, tr, Point(0, 0))
    n = n + 1
  end
end)
s:saveAs(app.params["fonte"])
print("gravados " .. n)
'''


def _gravar(fonte, cel, tmp):
    J = _juntas_fonte(cel)
    original = _celulas(tmp, ORIGINAL, "original")
    pasta = pathlib.Path(tmp) / "novos"
    pasta.mkdir(exist_ok=True)
    for k, j in enumerate(J):
        braco(cel, k, j).save(pasta / f"braco-{k}.png")
        corpo_corrigido(cel, k, original).save(pasta / f"corpo-{k}.png")
    lua = pathlib.Path(tmp) / "gravar.lua"
    lua.write_text(_GRAVAR, encoding="utf-8")
    r = subprocess.run([aseprite(), "-b", "--script-param", f"fonte={fonte}", "--script-param", f"pasta={pasta}",
                        "--script", str(lua)], capture_output=True, text=True)
    return [x for x in r.stdout.splitlines() if x.startswith("gravados")] or [r.stdout + r.stderr]


def aplicar():
    with tempfile.TemporaryDirectory() as tmp:
        print(_gravar(FONTE, _celulas(tmp), tmp))


def _achatar(fonte, pasta):
    pasta.mkdir(parents=True, exist_ok=True)
    subprocess.run([aseprite(), "-b", "--ignore-layer", "guia", str(fonte), "--save-as", str(pasta / "q{frame}.png")],
                   capture_output=True, text=True)
    return [Image.open(pasta / f"q{k}.png").convert("RGBA") for k in range(len(list(pasta.glob("q*.png"))))]


def previa(saida, poses=None):
    """Os quadros achatados (com a luz) antes e depois, numa cópia da fonte: <saida>/antes-k.png e depois-k.png."""
    saida = pathlib.Path(saida)
    with tempfile.TemporaryDirectory() as tmp:
        copia = pathlib.Path(tmp) / "copia.aseprite"
        shutil.copy(FONTE, copia)
        print(_gravar(copia, _celulas(tmp), tmp))
        antes = _achatar(FONTE, pathlib.Path(tmp) / "a")
        depois = _achatar(copia, pathlib.Path(tmp) / "d")
    for k, (a, d) in enumerate(zip(antes, depois)):
        a.save(saida / f"antes-{k}.png")
        d.save(saida / f"depois-{k}.png")
    print(f"{len(antes)} quadros em {saida}")


def folha():
    """A inspeção: as 20 poses, recortadas no braço (44×56), a versão anterior em cima e a atual embaixo, recompostas
    das camadas do protótipo (camadas/morel-vista-v3 e camadas/morel-vista)."""
    import json
    cam = AQUI.parents[1] / "camadas"

    def cena(raiz, k):
        r = json.load(open(raiz / "rotina.json"))
        x, y, w, h = r["morel"]["caixa"]
        im = lambda n: Image.open(raiz / f"{n}.png").convert("RGBA")  # noqa: E731
        c = im("fundo").copy()
        m = im("morel")
        c.alpha_composite(m.crop((k * w, 0, k * w + w, h)), (x, y))
        c.alpha_composite(im("frente"))
        c.alpha_composite(im("chamas").crop((320, 0, 640, 96)))
        c.alpha_composite(m.crop((k * w, h, k * w + w, 2 * h)), (x, y))
        return c.crop((178, 24, 222, 80))
    out = Image.new("RGBA", (20 * 46, 2 * 58), (24, 22, 20, 255))
    for k in range(20):
        out.alpha_composite(cena(cam / "morel-vista-v3", k), (k * 46, 0))
        out.alpha_composite(cena(cam / "morel-vista", k), (k * 46, 58))
    out.save(cam / "morel-vista" / "manga-comparacao.png", optimize=True)
    print("manga-comparacao.png")


if __name__ == "__main__":
    if "--aplicar" in sys.argv:
        aplicar()
    elif "--previa" in sys.argv:
        previa(sys.argv[-1])
    elif "--folha" in sys.argv:
        folha()
