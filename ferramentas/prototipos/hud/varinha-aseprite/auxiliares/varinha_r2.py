"""Rodada 2 da varinha: as listas de pixels por camada que o pintar.lua escreve no Aseprite (aseprite-mcp-bridge).

    python ferramentas/prototipos/hud/varinha-aseprite/auxiliares/varinha_r2.py <pasta>

Grava <pasta>/<tamanho>/<camada>.txt ("x,y,RRGGBB;...", coordenadas do documento), o mesmo em <camada>.lua (para o
dofile do pintar.lua) e <pasta>/<tamanho>/previa.png (o
composto, só para conferir a leitura do Aseprite). As camadas, de baixo para cima, estão em CAMADAS.

- 32: o desenho aprovado (../varinha-32.png), só repartido em camadas pela família da cor e pela posição; nenhum pixel
  muda.
- 64: o aprovado (../varinha-64.png) com u <= 24 intacto (pomo, empunhadura, anel e haste; o contorno até u 22); a taça
  e a pedra refeitas por regra, e o contorno da ponta recalculado. A pedra deixou de ser a ponta afilada (lia como
  chama) e virou uma pedra lapidada quadrada (pedra_quadrada), assentada na taça.
- 40 e 48: desenhados na própria grade, com as medidas de cada tamanho em MEDIDAS.

A varinha corre na diagonal: u = x - y cresce para a ponta (em cima à direita), s = x + y cresce de través para o lado
da sombra (embaixo à direita). Um pixel existe quando u e s têm a mesma paridade. A luz é a da família: de cima e da
esquerda (s pequeno é o lado aceso).
"""
import pathlib
import sys

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
PROPOSTA = AQUI.parent
CAMADAS = ["pomo", "empunhadura", "anel", "haste", "taca", "pedra", "garras", "contorno"]
CONTORNO = "08080A"

# as rampas da primeira rodada (as do 64), do escuro ao claro
W = ["2A120D", "431D14", "5E291B", "7A3824", "974B31", "B5674A", "CC8462"]                      # jacarandá
L = ["24170F", "3A281B", "59402B", "7A5638", "8F6A48"]                                          # couro
M = ["1A160E", "332A1B", "4E4128", "6E5C38", "8F7A4C", "B09A64", "CDBB86"]                      # bronze envelhecido
A = ["2E1004", "4A1D05", "7A3307", "B0520C", "E0841A", "F4A530", "FFC85A", "FFE7A8", "FFF6DE"]  # âmbar

# as cores do 32 aprovado que não estão nas rampas acima (o 32 foi escrito à mão)
BRONZE32 = {"3A3020", "806B42", "1D1810", "5C4C30", "A89160", "D2BF8A"}
AMBAR32 = {"FFF0C8"}


def familia(cor):
    if cor == CONTORNO: return "contorno"
    if cor in A or cor in AMBAR32: return "pedra"
    if cor in W: return "haste"
    if cor in L: return "empunhadura"
    if cor in M or cor in BRONZE32: return "bronze"
    raise ValueError(cor)


def ler_png(nome):
    im = Image.open(PROPOSTA / nome).convert("RGBA")
    return im.size[0], {(x, y): "%02X%02X%02X" % im.getpixel((x, y))[:3]
                        for y in range(im.size[1]) for x in range(im.size[0]) if im.getpixel((x, y))[3]}


def repartir(px, pega_de, haste_de):
    """Separa os pixels de um desenho pronto nas camadas; o bronze vai para o pomo, o anel ou a taça pela posição."""
    camadas = {c: {} for c in CAMADAS}
    for (x, y), cor in px.items():
        f, u = familia(cor), x - y
        if f == "bronze":
            f = "pomo" if u < pega_de else "anel" if u < haste_de else "taca"
        camadas[f][(x, y)] = cor
    return camadas


def contornar(cheio, n):
    """Os vizinhos vazios (4 lados) da forma, dentro da tela."""
    return {(x + dx, y + dy) for x, y in cheio for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
            if (x + dx, y + dy) not in cheio and 0 <= x + dx < n and 0 <= y + dy < n}


def faixa(perfil, cor):
    """Os pixels de cada u do perfil {u: (s_baixo, s_alto)}, com a cor dada por cor(u, s, q) (None = vazio);
    q vai de 0 (a borda acesa) a 1 (a borda na sombra)."""
    px = {}
    for u, (lo, hi) in perfil.items():
        for s in range(lo, hi + 1):
            if (u + s) % 2: continue
            c = cor(u, s, (s - lo) / max(1, hi - lo))
            if c: px[((s + u) // 2, (s - u) // 2)] = c
    return px


def banda(q, tons):
    """O tom pela posição de través: tons é a lista do lado aceso ao da sombra, em faixas iguais."""
    return tons[min(len(tons) - 1, int(q * len(tons)))]


# --- a taça, a pedra e as garras (64 e, com outras medidas, 40 e 48) -------------------------------------------------------

def taca(m):
    """A taça: o pescoço estreito, a dobra onde abre (um degrau escuro) e a borda acesa que segura a pedra."""
    u_borda, u_dobra = max(m["taca"]), m["dobra"]
    def cor(u, s, q):
        t = banda(q, m["tons_taca"])
        if u == u_dobra: t = max(1, t - 1)                   # a dobra onde a taça abre
        if u == u_borda: t = min(6, t + 1)                   # a borda, virada para a luz
        return M[t]
    return faixa(m["taca"], cor)


def pedra_quadrada(m):
    """A pedra lapidada como uma pirâmide baixa vista de frente: um quadrado na grade (lados retos), com o canto de baixo
    à esquerda afundado na taça e o de cima à direita na ponta da varinha. As diagonais dividem quatro faces: a de cima
    e a da esquerda acesas, a da direita e a de baixo na sombra (as divisórias a 45° são as linhas mais nítidas do
    pixel). m["quadrado"] = (x0, y0, lado); m["tons_faces"] = cima, esquerda, direita, baixo; m["sem"] tira cantos."""
    x0, y0, n = m["quadrado"]
    cima, esq, dir_, baixo = m["tons_faces"]
    px = {}
    for b in range(n):
        for a in range(n):
            if (a, b) in m["sem"]: continue
            x, y = x0 + a, y0 + b
            if x - y < m["pedra_de"]: continue                  # o que está dentro da taça
            k = n - 1
            if a == b and a + b < k: t = m["aresta_luz"]        # a aresta entre as faces acesas
            elif a == b and a + b > k: t = m["aresta_sombra"]
            elif a + b == k: t = m["aresta_eixo"][0 if a > b else 1] if a != b else m["centro"]
            elif b < a and a + b < k: t = cima
            elif a < b and a + b < k: t = esq
            elif a > b: t = dir_
            else: t = baixo
            px[(x, y)] = A[t]
    for (x, y), t in m["toques"].items():
        px[(x, y)] = A[t]
    return px


def garras(m):
    return {((s + u) // 2, (s - u) // 2): M[t] for (u, s), t in m["garras"].items()}


# --- o resto da varinha (40 e 48) ----------------------------------------------------------------------------------

def pomo(m):
    """O pomo: uma esfera de bronze com o ponto de luz em cima à esquerda."""
    us = sorted(m["pomo"])
    u_luz = us[0] + (len(us) - 1) * 0.35
    lo = min(a for a, _ in m["pomo"].values()); hi = max(b for _, b in m["pomo"].values())
    s_luz, raio = lo + (hi - lo) * 0.3, (hi - lo) / 2
    def cor(u, s, q):
        d = ((u - u_luz) ** 2 * 0.6 + (s - s_luz) ** 2) ** 0.5 / raio
        t = 6 if d < 0.25 else 5 if d < 0.5 else 4 if d < 0.8 else 3 if d < 1.1 else 2 if d < 1.4 else 1
        if u >= us[-1] - m["pescoco"] + 1: t = min(t, 3)  # o pescoço, na sombra do pomo
        return M[t]
    return faixa(m["pomo"], cor)


def empunhadura(m):
    def cor(u, s, q):
        t = banda(q, m["tons_pega"])
        if u in m["costuras"] and q > 0.2: t = max(0, t - 1)
        return L[t]
    return faixa(m["pega"], cor)


def anel(m):
    us = sorted(m["anel"])
    def cor(u, s, q):
        t = banda(q, m["tons_anel"])
        if len(us) > 2 and u in (us[0], us[-1]): t = max(1, t - 2)   # as bordas do anel
        return M[t]
    return faixa(m["anel"], cor)


def haste(m):
    def cor(u, s, q):
        lo, hi = m["haste"][u]
        t = m["tons_haste"][hi - lo + 1][s - lo]
        if s == lo and m["brilho"][0] <= u <= m["brilho"][1]: t = 6   # o brilho da madeira polida
        if s == lo + 1 and u in m["veio"]: t -= 1                       # o veio
        return W[t]
    return faixa(m["haste"], cor)


def perfil(*trechos):
    """{u: (lo, hi)} a partir de trechos (u0, u1, lo, hi)."""
    return {u: (lo, hi) for u0, u1, lo, hi in trechos for u in range(u0, u1 + 1)}


MEDIDAS = {
    64: dict(
        taca=perfil((25, 26, 62, 65), (27, 29, 61, 66), (30, 31, 60, 67)), dobra=27,
        tons_taca=[4, 4, 3, 2, 1, 1],
        quadrado=(47, 11, 6), pedra_de=32, sem={(0, 0), (5, 5), (5, 0)}, tons_faces=(5, 6, 3, 1),
        aresta_luz=5, aresta_sombra=2, aresta_eixo=(4, 3), centro=4,
        toques={(48, 12): 8, (49, 12): 7, (51, 15): 4},          # o reflexo; a luz que atravessa, na face da direita
        garras={(32, 62): 5, (33, 61): 4, (32, 64): 2, (33, 65): 1},
    ),
    48: dict(
        pomo=perfil((-32, -32, 46, 49), (-31, -28, 45, 50), (-27, -26, 46, 49)), pescoco=2,
        pega=perfil((-25, -11, 46, 49)), tons_pega=[4, 3, 2, 1], costuras=(-21, -16),
        anel=perfil((-10, -8, 46, 49)), tons_anel=[6, 5, 3, 2],
        haste=perfil((-7, 0, 46, 49), (1, 15, 46, 48)),
        tons_haste={4: [5, 4, 3, 1], 3: [4, 3, 1]}, brilho=(-5, 3), veio=(-2, 7),
        taca=perfil((16, 17, 46, 48), (18, 19, 45, 49), (20, 21, 45, 50)), dobra=18, tons_taca=[4, 4, 3, 2, 1],
        quadrado=(34, 9, 5), pedra_de=22, sem={(0, 0), (4, 4), (4, 0)}, tons_faces=(5, 6, 3, 1),
        aresta_luz=5, aresta_sombra=2, aresta_eixo=(4, 3), centro=4,
        toques={(35, 10): 8, (36, 10): 7, (37, 12): 4},
        garras={(22, 46): 5, (23, 45): 4, (23, 49): 1},
    ),
    40: dict(
        pomo=perfil((-26, -26, 38, 40), (-25, -22, 37, 41), (-21, -21, 38, 40)), pescoco=1,
        pega=perfil((-20, -9, 38, 40)), tons_pega=[3, 2, 1], costuras=(),
        anel=perfil((-8, -7, 38, 40)), tons_anel=[6, 4, 2],
        haste=perfil((-6, 3, 38, 40), (4, 12, 39, 40)),
        tons_haste={3: [4, 3, 1], 2: [4, 2]}, brilho=(-4, 2), veio=(0, 7),
        taca=perfil((13, 14, 38, 40), (15, 17, 37, 41)), dobra=15, tons_taca=[4, 4, 3, 2, 1],
        quadrado=(28, 8, 4), pedra_de=18, sem={(0, 0), (3, 3)}, tons_faces=(5, 6, 3, 1),
        aresta_luz=5, aresta_sombra=2, aresta_eixo=(4, 3), centro=4,
        toques={(29, 9): 8},
        garras={(18, 38): 5, (18, 40): 2},
    ),
}


def desenhar(n):
    if n == 32:
        _, px = ler_png("varinha-32.png")
        return repartir(px, pega_de=-13, haste_de=0)
    m = MEDIDAS[n]
    if n == 64:
        _, px = ler_png("varinha-64.png")
        velho = repartir(px, pega_de=-28, haste_de=-7)
        camadas = {c: {p: k for p, k in v.items() if p[0] - p[1] <= 24} for c, v in velho.items() if c != "contorno"}
        contorno_fixo = {p: k for p, k in velho["contorno"].items() if p[0] - p[1] <= 22}
    else:
        camadas = {"pomo": pomo(m), "empunhadura": empunhadura(m), "anel": anel(m), "haste": haste(m)}
        contorno_fixo = {}
    camadas["taca"], camadas["garras"] = taca(m), garras(m)
    camadas["pedra"] = pedra_quadrada(m)
    for c in ("taca", "pedra", "garras"):                   # o que está por cima tira o pixel de baixo
        for p in camadas[c]:
            for d in CAMADAS[:CAMADAS.index(c)]:
                camadas.get(d, {}).pop(p, None)
    cheio = set().union(*(v.keys() for v in camadas.values()))
    novo = {p for p in contornar(cheio, n) if n != 64 or p[0] - p[1] >= 23}
    camadas["contorno"] = {**contorno_fixo, **{p: CONTORNO for p in novo}}
    return camadas


def gravar(n, camadas, pasta):
    pasta.mkdir(parents=True, exist_ok=True)
    previa = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    for c in CAMADAS:
        px = camadas.get(c, {})
        texto = ";".join(f"{x},{y},{k}" for (x, y), k in sorted(px.items()))
        (pasta / f"{c}.txt").write_text(texto)
        (pasta / f"{c}.lua").write_text(f'return "{texto}"\n')         # o pintar.lua lê por dofile
        for (x, y), k in px.items():
            previa.putpixel((x, y), tuple(int(k[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    previa.save(pasta / "previa.png")
    return previa


if __name__ == "__main__":
    saida = pathlib.Path(sys.argv[1])
    for n in [int(a) for a in sys.argv[2:]] or (32, 40, 48, 64):
        cam = desenhar(n)
        im = gravar(n, cam, saida / str(n))
        cores = {k for v in cam.values() for k in v.values()}
        print(n, "bbox", im.getbbox(), "opacos", sum(1 for p in im.getdata() if p[3]), "cores", len(cores),
              " ".join(f"{c}:{len(cam.get(c, {}))}" for c in CAMADAS))
