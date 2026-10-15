"""A aljava do Arqueiro nas costas, na diagonal da alça que cruza o peito (do ombro esquerdo dele ao quadril direito,
uns 45 graus): a boca sobe por trás do ombro, para cima e para fora, e o corpo desce para dentro, sumindo atrás do
capuz e do ombro. Couro com a luz de cima e da esquerda (a borda de cima clara, a de baixo escura), uma cinta
atravessada perto da boca, o aro aceso e as flechas saindo dela, cada uma com a haste, a pena clara de cima, a escura
de baixo e o entalhe na ponta. No busto de 40×40 e na carta de 16×16 (a figura da fogueira é a carta).

Desenhada à mão, pixel a pixel: a 45 graus, uma conta (o eixo e a largura) deixava as penas em xadrez.

Lê as grades atuais do jogo (pelo extrair.mjs), tira a aljava que estiver lá (as versões anteriores: a de pé ao lado
da cabeça, de antes da 1.97.1, e a escondida, que não entrou) e imprime as grades novas; o resto do desenho não muda.
    python ferramentas/prototipos/hud/arqueiro/aljava.py"""
import json, pathlib, subprocess

AQUI = pathlib.Path(__file__).resolve().parent
atuais = json.loads(subprocess.run(["node", str(AQUI.parent / "personagens" / "extrair.mjs")], capture_output=True, text=True,
                                   check=True).stdout)
ALJAVA = set("LlmMfFo")  # couro, pena e haste: o que pode ser da aljava na área dela


def busto_px():
    px = {}
    for r in range(15, 22):  # o tubo: 6 px por linha, subindo 1 para a direita a cada linha (45 graus, como a alça)
        for i, t in enumerate("LLlmmM"):
            px[(27 + (20 - r) + i, r)] = t
    px.update({(31, 16): "m", (32, 16): "M", (32, 17): "M", (33, 17): "M", (33, 18): "M", (34, 18): "M"})  # a cinta
    for i, t in enumerate("LLLLLl"):  # o aro da boca
        px[(33 + i, 14)] = t
    # a flecha comprida (do lado da luz): a haste, três pares de penas e o entalhe
    px.update({(34, 13): "o", (35, 12): "o", (35, 11): "f", (36, 11): "F", (36, 10): "f", (37, 10): "F",
               (37, 9): "f", (38, 9): "F", (39, 8): "o"})
    # a curta (do lado da sombra)
    px.update({(37, 13): "o", (37, 12): "f", (38, 12): "F", (38, 11): "f", (39, 11): "F"})
    return px


def carta_px():
    return {(13, 10): "M", (12, 9): "L", (13, 9): "l", (14, 9): "M", (13, 8): "L", (14, 8): "m", (15, 8): "M",  # o tubo
            (13, 7): "L", (14, 7): "L", (15, 7): "l",                                                        # o aro
            (14, 6): "f", (15, 6): "F", (15, 5): "f", (15, 3): "o",          # a flecha da frente e o entalhe
            (13, 5): "f", (14, 5): "F", (14, 4): "f"}                         # a de trás


def pintar(papel, area, px):
    g = [list(l) for l in atuais[papel]["grade"]]
    x0, x1, y0, y1 = area
    for y in range(y0, y1):  # tira a aljava velha (o ombro, embaixo da área, fica)
        for x in range(x0, x1):
            if g[y][x] in ALJAVA:
                g[y][x] = "."
    for (x, y), t in px.items():
        if g[y][x] == ".":  # só por cima do vazio: o capuz e o ombro ficam na frente da aljava
            g[y][x] = t
    return ["".join(l) for l in g]


def busto():
    return pintar("arqueiro-busto", (28, 40, 0, 22), busto_px())


def carta():
    return pintar("arqueiro-carta", (12, 16, 0, 11), carta_px())


if __name__ == "__main__":
    print(json.dumps({"busto": busto(), "carta": carta(), "cores": atuais["arqueiro-busto"]["cores"]}))
