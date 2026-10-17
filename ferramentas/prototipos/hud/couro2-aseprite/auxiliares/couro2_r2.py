"""Rodada 2 do capuz e das luvas: as listas de pixels por camada que o pintar.lua (ferramentas/arte/aseprite/) escreve no
Aseprite pelo MCP. O Python só calcula.

    python ferramentas/prototipos/hud/couro2-aseprite/auxiliares/couro2_r2.py <pasta> [capuz|capuz_tecido|luva_seda]

- capuz (couro): o da rodada 1 com o caimento refeito: a cabeça, a abertura, a borda e a paleta iguais; a faixa da
  base (que lia como a borda enrolada de um gorro) virou uma capa que cai para os lados em diagonal, com a barra
  mais alta na frente e mais baixa nos lados, dois vincos de dobra e poucos planos, sem aro embaixo.
- capuz_tecido (o Capuz do Mago): o alto num pico macio, a borda da abertura numa dobra fina de pano (sem tira de
  couro), a capa caindo dos ombros como a do couro, mas pendurada, mais longa e com dobras verticais de pano e a barra
  ondulada, sem cordão; lã azul-acinzentada escura (mais clara, com a abertura escura, lia como um fantasma).
- luva_seda (a Luva de Seda): justa, os dedos separados e mais finos (a seda cola na mão), o polegar delgado, um punho
  curto e macio sem amarração; o brilho da seda numa faixa longa e suave nas costas da mão.
A luva de couro com braçadeira é a da rodada 1, aprovada: não se refaz aqui.

O 32 é a fonte (desenhado na grade); o 64 é o 32 ampliado 2× (previa-64.png). Luz de cima e da esquerda.
"""
import pathlib
import sys

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parents[1] / "couro-aseprite" / "auxiliares"))
from couro2_r1 import ABERTURA, N, faixas  # noqa: E402
from couro_r2 import BORDA, CORDAO, COURO, FORRO, GASTO, Desenho  # noqa: E402

TECIDO = ["10131C", "1C2230", "2A3346", "3B4760", "4F5E7C", "667696", "8392B0"]       # lã azul-acinzentada
FORRO_TECIDO = ["0B0D12", "161A24", "232A38"]                                        # o avesso do pano
SEDA = ["141826", "232A40", "34405E", "4A5A80", "6476A0", "8494BE", "B4C2E0"]         # seda azul, o claro é o brilho

# a cabeça do capuz de couro: a da rodada 1 (linhas 1 a 17); daí para baixo, o capuz já abre para a capa
CABECA = {1: (17, 18), 2: (15, 19), 3: (13, 20), 4: (11, 21), 5: (10, 21), 6: (9, 22), 7: (9, 22), 8: (8, 23),
          9: (8, 23), 10: (8, 23), 11: (7, 24), 12: (7, 24), 13: (7, 24), 14: (7, 24), 15: (7, 24), 16: (7, 24),
          17: (7, 24), 18: (7, 24), 19: (6, 25), 20: (5, 26)}
# a capa: a largura de cada linha cresce em diagonal até as bordas da tela; a barra de cada coluna desce do meio para
# os lados (o couro cai pelos ombros: a frente mais curta, os lados mais longos)
CAPA_LARG = {21: (4, 27), 22: (4, 27), 23: (3, 28), 24: (3, 28), 25: (3, 28), 26: (3, 28), 27: (3, 28)}


def barra(x, meio=23, lados=27):
    return meio + round(((abs(x - 15.5) / 12.5) ** 1.3) * (lados - meio))


def _abertura_e_borda(d, dentro, rampa_borda_luz, tons_borda, rampa_borda_sombra, forro, camada_borda="borda"):
    """A borda em volta da abertura (acesa em cima e à esquerda) e o interior (o forro logo abaixo da borda de cima, a
    parede de dentro da direita um pouco clara): como na rodada 1."""
    for (x, y) in list(d.px):
        if any((x + dx, y + dy) in dentro for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            acesa = y <= 10 or x < 15
            d.px[(x, y)] = (camada_borda, rampa_borda_luz if acesa else rampa_borda_sombra,
                            tons_borda[0] if acesa and x < 16 else tons_borda[1] if acesa else tons_borda[2])

    def tom_dentro(x, y):
        if (x, y - 1) not in dentro: return 1
        x1 = ABERTURA[y][1]
        return 2 if x == x1 else 1 if x == x1 - 1 else 0
    faixas(d, ABERTURA, "interior", forro, tom_dentro)


def capuz():
    d = Desenho(N)
    dentro = {(x, y) for y, (a, b) in ABERTURA.items() for x in range(a, b + 1)}

    def tom_cabeca(x, y):
        if (x, y) in dentro: return None
        t = 5 if x < 12 else 4 if x < 20 else 3
        if x >= 23: t = 2
        if y <= 8 and x < 16: t += 1                                   # o alto do crânio, de frente para a luz
        if 2 <= y <= 8 and x == 16 + (y <= 3): t = 3                   # a costura do meio
        if y >= 16: t -= 1                                             # o capuz vira para baixo, na sombra
        return t
    faixas(d, CABECA, "capuz", COURO, tom_cabeca)
    _abertura_e_borda(d, dentro, COURO, (6, 5, 2), BORDA, FORRO)

    # a capa: o plano aceso à esquerda, a frente média, a sombra à direita; dois vincos de dobra em diagonal (o vale
    # escuro com a crista acesa ao lado), que mostram o couro dobrando ao cair pelos ombros
    vinco_e = {(11 - k, 21 + k) for k in range(6)}                      # desce para a esquerda
    vinco_d = {(20 + k, 21 + k) for k in range(6)}                      # desce para a direita
    def tom_capa(x, y):
        if y > barra(x): return None
        t = 5 if x < 9 else 4 if x < 16 else 3 if x < 23 else 2
        if (x, y) in vinco_e: return 2
        if (x + 1, y) in vinco_e: return 6                              # a crista acesa do vinco da esquerda
        if (x, y) in vinco_d: return 1
        if (x - 1, y) in vinco_d: return 3
        if y == barra(x) and x >= 16: t -= 1                            # a beira de baixo vira para dentro, na sombra
        return t
    faixas(d, CAPA_LARG, "capa", COURO, tom_capa)
    for y in (21,):                                                      # a sombra do capuz logo abaixo dele
        for x in range(4, 28):
            if (x, y) in d.px and d.px[(x, y)][0] == "capa" and 7 <= x <= 24: d.px[(x, y)] = ("capa", COURO, 2)
    d.px[(15, 20)] = ("cordao", CORDAO, 2); d.px[(16, 20)] = ("cordao", CORDAO, 1)
    d.px[(15, 21)] = ("cordao", CORDAO, 1); d.px[(16, 21)] = ("cordao", CORDAO, 2)
    d.px[(25, 24)] = ("desgaste", GASTO, 1); d.px[(26, 25)] = ("desgaste", GASTO, 0)
    d.contornar()
    return d


# --- o capuz de tecido -------------------------------------------------------------------------------------------
CABECA_T = {1: (15, 17), 2: (13, 19), 3: (11, 20), 4: (10, 21), 5: (9, 22), 6: (9, 22), 7: (8, 23), 8: (8, 23),
            9: (8, 23), 10: (8, 23), 11: (7, 24), 12: (7, 24), 13: (7, 24), 14: (7, 24), 15: (7, 24), 16: (7, 24),
            17: (7, 24), 18: (7, 24), 19: (6, 25), 20: (6, 25)}
CAPA_T = {21: (4, 27), 22: (4, 27), 23: (3, 28), 24: (3, 28), 25: (3, 28), 26: (3, 28), 27: (3, 28), 28: (3, 28),
          29: (3, 28)}


def barra_t(x):
    """A barra do pano: cai dos ombros como a do couro, mas pendurada e mais longa, mais baixa nos lados e ondulada
    (as dobras terminam em pontas)."""
    return barra(x, meio=25, lados=28) + (1 if x % 5 in (1, 2) and abs(x - 15.5) < 11 else 0)


def capuz_tecido():
    d = Desenho(N)
    dentro = {(x, y) for y, (a, b) in ABERTURA.items() for x in range(a, b + 1)}

    def tom_cabeca(x, y):                                               # lã escura: um degrau abaixo do couro
        if (x, y) in dentro: return None
        t = 4 if x < 12 else 3 if x < 20 else 2
        if x >= 23: t = 1
        if y <= 8 and x < 16: t += 1
        if y >= 16: t -= 1
        return t
    faixas(d, CABECA_T, "capuz", TECIDO, tom_cabeca)
    # a borda da abertura: uma dobra fina de pano (um tom acima do pano em volta), sem tira escura
    _abertura_e_borda(d, dentro, TECIDO, (6, 5, 3), TECIDO, FORRO_TECIDO)
    # a capa de pano: dobras verticais (claro e escuro alternando em faixas de 2 a 3 px), mais longa
    dobras = {3: 4, 4: 4, 5: 4, 6: 2, 7: 3, 8: 4, 9: 3, 10: 1, 11: 2, 12: 3, 13: 3, 14: 1, 15: 2, 16: 3, 17: 3,
              18: 1, 19: 2, 20: 3, 21: 2, 22: 1, 23: 2, 24: 2, 25: 1, 26: 1, 27: 1, 28: 1}
    def tom_capa(x, y):
        if y > barra_t(x): return None
        t = dobras.get(x, 1)
        if y == 21 and 7 <= x <= 24: t = min(t, 2)                       # a sombra da cabeça sobre a capa
        return t
    faixas(d, CAPA_T, "capa", TECIDO, tom_capa)
    d.contornar()
    return d


# --- a luva de seda ----------------------------------------------------------------------------------------------
# A mão direita de costas, como a de couro, mas justa: os quatro dedos separados por um vão de 1 px até a mão (a seda
# cola em cada dedo), mais finos e mais longos; o polegar delgado; um punho curto, um pouco aberto, com uma dobra
# macia, sem amarração. O brilho: uma faixa longa e suave nas costas da mão e nos dedos de cima.
DEDOS_S = [((11, 12), 6), ((14, 15), 4), ((17, 18), 5), ((20, 21), 8)]
MAO_S = {y: (11, 21) for y in range(13, 20)} | {20: (12, 21), 21: (12, 20)}
POLEGAR_S = {11: (7, 7), 12: (7, 8), 13: (8, 9), 14: (9, 10), 15: (9, 10), 16: (10, 10)}
PUNHO_S = {22: (12, 20), 23: (11, 21), 24: (11, 21), 25: (10, 22), 26: (10, 22)}


def luva_seda():
    d = Desenho(N)
    tom_mao = lambda x, y: 5 if x < 14 else 4 if x < 18 else 3 if x < 20 else 2
    faixas(d, MAO_S, "luva", SEDA, tom_mao)
    for (c0, c1), topo in DEDOS_S:
        tons = {11: (5, 4), 14: (5, 4), 17: (4, 3), 20: (3, 2)}[c0]
        for y in range(topo, 13):
            d.px[(c0, y)] = ("luva", SEDA, tons[0] + (1 if y == topo else 0))
            d.px[(c1, y)] = ("luva", SEDA, tons[1])
    faixas(d, POLEGAR_S, "luva", SEDA, lambda x, y: 6 if y == 11 else 5 if x < 10 else 4)
    # o brilho da seda: uma faixa diagonal suave nas costas da mão, do nó dos dedos ao punho
    for (x, y), t in {(13, 13): 6, (13, 14): 6, (14, 15): 6, (14, 16): 5, (15, 17): 5, (15, 18): 5, (14, 6): 6,
                      (14, 7): 6, (11, 8): 6}.items():
        if (x, y) in d.px: d.px[(x, y)] = ("brilho", SEDA, t)
    # o punho curto: um pouco aberto, a beira de cima com a dobra (um tom acima) e a de baixo na sombra
    def tom_punho(x, y):
        if y == 22: return 5 if x < 16 else 3
        t = 4 if x < 14 else 3 if x < 18 else 2
        return t - (1 if y == 26 else 0)
    faixas(d, PUNHO_S, "punho", SEDA, tom_punho)
    d.contornar()
    return d


PECAS = {"capuz": (capuz, ["capa", "capuz", "interior", "borda", "cordao", "desgaste", "contorno"]),
         "capuz_tecido": (capuz_tecido, ["capa", "capuz", "interior", "borda", "contorno"]),
         "luva_seda": (luva_seda, ["punho", "luva", "brilho", "contorno"])}


def gravar(peca, pasta):
    fazer, ordem = PECAS[peca]
    cam = fazer().camadas()
    pasta.mkdir(parents=True, exist_ok=True)
    previa = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    for c in ordem:
        px = cam.get(c, {})
        texto = ";".join(f"{x},{y},{k}" for (x, y), k in sorted(px.items()))
        (pasta / f"{c}.txt").write_text(texto)
        (pasta / f"{c}.lua").write_text(f'return "{texto}"\n')
        for (x, y), k in px.items():
            previa.putpixel((x, y), tuple(int(k[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    previa.save(pasta / "previa.png")
    previa.resize((2 * N, 2 * N), Image.NEAREST).save(pasta / "previa-64.png")
    (pasta / "camadas.txt").write_text(",".join(ordem))
    return previa.getbbox(), sum(len(v) for v in cam.values()), len({k for v in cam.values() for k in v.values()})


if __name__ == "__main__":
    saida = pathlib.Path(sys.argv[1])
    for p in [a for a in sys.argv[2:] if a in PECAS] or list(PECAS):
        print(p, *gravar(p, saida / f"{p}-32"))
