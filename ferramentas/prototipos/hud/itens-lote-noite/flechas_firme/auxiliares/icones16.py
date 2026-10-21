"""As grades de 16 da flecha da carta do Arqueiro (F1) e do estado Firme (R1), 20/10/2026, desenhadas na resolução em que
os dois aparecem na luta: 16 × 16 px de tela (o `S(..., 1)` da carta, `.carta-flechas img.sprite { --s: 16 }`, e o dos
estados, `.ef img.sprite { --s: 16 }`). As referências (ferramentas/arte/referencias/icones/) são imagens geradas
ampliadas, não sprites de 16: delas vêm a construção e os materiais, e cada pixel daqui foi posto à mão.

  - a flecha (F1, da iconeflechaarqueiro.png e das flechas da aljava aprovada): a ponta de aço em cima à direita, um
    triângulo com o vértice no canto, a aresta acesa no meio (x + y = 15), a face de cima clara e a de baixo escura, as
    duas barbas e o encaixe escuro na haste; a haste de madeira clara na diagonal, de 1 px entre os contornos; as penas
    dos dois lados (a de cima clara, a de baixo na sombra), estreitas na frente e largas atrás; o amarrado vermelho no
    fim das penas, como nas flechas da aljava; o fim da haste em madeira mais escura;
  - o Firme (R1, da iconefirme.png, a corrente rompida): dois elos ovais na diagonal, cada um com o furo comprido, a luz de
    cima e da esquerda; um vão entre eles; a ponta de cada elo voltada para o vão aberta (um pixel do anel tirado) com a
    face do corte acesa; os dois traços azuis curtos de cada lado do vão (as faíscas da referência, numa camada própria,
    para poderem sair se virarem ruído).
A segunda rodada (20/10/2026, pedido do Jean), com as primeiras preservadas:
  - a F2, a flecha com a traseira corrigida (a F1 tinha as penas grandes e adiantadas, com haste sobrando atrás): pela
    composição da flecha simples do canto de cima à esquerda da prancha "Arrows" que o Jean mandou na conversa, as penas
    vão para a extremidade de trás, finas (uma faixa de cada lado da haste, com a ponta de trás virada para fora), sem
    madeira atrás delas (o encaixe só sugerido por um pixel de madeira escura entre as pontas das penas), a haste livre
    entre as penas e a ponta, o amarrado vermelho num pixel só; a ponta e a haste são as da F1;
  - a R2, o Firme limpo: sem as faíscas azuis, e o furo de cada elo mais legível pela luz de dentro do anel (a borda de
    dentro do lado de baixo-direita, que fica de frente para a luz, acesa; a de cima-esquerda, na sombra), com a mesma
    espessura, a mesma ruptura e a mesma composição.
Os tons de aço são a rampa de ferro do conjunto; a madeira, as penas e o vermelho, os das flechas da aljava
(rpg/web/static/hud/icones/aljava-32.png); o azul das faíscas, o da referência, mais escuro.

Grava grades/<id>.txt e as listas por camada para o pintar.lua (listas/<id>/<camada>.lua).
    python icones16.py <pasta>
"""
import pathlib
import sys

CONTORNO = "08080a"
CORES = {"#": CONTORNO,
         # o aço (a rampa de ferro do conjunto)
         "A": "e4e8ec", "B": "b0b6bd", "C": "848b94", "D": "4c5159",
         "3": "383c44", "4": "4c5159", "5": "646a73", "6": "848b94", "7": "b0b6bd", "8": "e4e8ec",
         # a madeira, as penas e o amarrado (os das flechas da aljava)
         "w": "dcbc86", "m": "b08a58", "f": "f4eedc", "g": "cfc6b0", "h": "8a8070", "r": "d04a2c", "R": "9a2a1c",
         # as faíscas do Firme
         "U": "9cc4f0", "u": "4a6fa8"}

FLECHA = ["..........#####.",
          ".........#BBBBA#",
          "..........#BBAC#",
          "...........#ACC#",
          "..........#DCCD#",
          ".........#w###D#",
          ".....#..#w#...#.",
          "....#f##w#......",
          "...#ff#w#.......",
          "..#ffgwg#.......",
          ".#ffgwgh#.......",
          ".#ggRgh#........",
          "..#rgh#.........",
          ".#m#h#..........",
          "#m#.#...........",
          ".#.............."]
FIRME = ["...........####.",
         "..........#7765#",
         ".........#77654#",
         "........#77##44#",
         "........#76##43#",
         "....u..#76#443#.",
         ".....U.#7#443#..",
         ".....##.#54##...",
         "...##78#.##.....",
         "..#776#6#.U.....",
         ".#776#44#..u....",
         "#77##44#........",
         "#76##43#........",
         "#65443#.........",
         "#5443#..........",
         ".####..........."]
FLECHA_F2 = ["..........#####.",
             ".........#BBBBA#",
             "..........#BBAC#",
             "...........#ACC#",
             "..........#DCCD#",
             ".........#w###D#",
             "........#w#...#.",
             ".......#w#......",
             "......#w#.......",
             "....##w#........",
             "...#gw#.........",
             ".##fwh#.........",
             "#ffRg#..........",
             ".#mg#...........",
             "..#h#...........",
             "...#............"]
FIRME_R2 = ["...........####.",
            "..........#7765#",
            ".........#76554#",
            "........#76##64#",
            "........#75##53#",
            ".......#76#653#.",
            ".......#7#443#..",
            ".....##.#54##...",
            "...##78#.##.....",
            "..#776#6#.......",
            ".#765#44#.......",
            "#76##64#........",
            "#75##53#........",
            "#65653#.........",
            "#5443#..........",
            ".####..........."]
CAMADAS = {   # o id do ícone: a grade e a camada de cada caractere
    "flecha_contador": (FLECHA, {"#": "contorno", **{c: "ponta" for c in "ABCD"}, "w": "haste", "m": "haste",
                                 **{c: "penas" for c in "fgh"}, "r": "amarrado", "R": "amarrado"}),
    "firme": (FIRME, {"#": "contorno", **{c: "elos" for c in "345678"}, "U": "faiscas", "u": "faiscas"}),
    "flecha_contador_f2": (FLECHA_F2, {"#": "contorno", **{c: "ponta" for c in "ABCD"}, "w": "haste", "m": "haste",
                                       **{c: "penas" for c in "fgh"}, "R": "amarrado"}),
    "firme_r2": (FIRME_R2, {"#": "contorno", **{c: "elos" for c in "345678"}}),
}

if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    for ident, (grade, camada) in CAMADAS.items():
        assert len(grade) == 16 and all(len(l) == 16 for l in grade), ident
        (base / "grades").mkdir(exist_ok=True)
        (base / f"grades/{ident}.txt").write_text("\n".join(grade) + "\n", encoding="utf-8")
        listas = {}
        for y, l in enumerate(grade):
            for x, ch in enumerate(l):
                if ch != ".": listas.setdefault(camada[ch], []).append(f"{x},{y},{CORES[ch]}")
        d = base / f"listas/{ident}"; d.mkdir(parents=True, exist_ok=True)
        for k, v in listas.items():
            (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
        print(ident, {k: len(v) for k, v in listas.items()})
