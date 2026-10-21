"""Os ícones de estado Em guarda (G1) e Esquiva (E1), 20/10/2026, na resolução em que os estados aparecem na luta:
16 × 16 px (o chip da carta, `.ef img.sprite { --s: 16 }`, e o selo do estado que chega). O Firme aprovado (R2,
rpg/web/static/hud/icones/estado-firme-16.png) é a referência de acabamento e de quantidade de informação: contorno de
1 px, poucos tons por material, a luz de cima e da esquerda.

  - G1, Em guarda (recebe menos dano: −v% em todo golpe que acerta; o Erguer Escudo dá −50% por 2 turnos): o escudo de
    ferro em pé, de frente, com a ponta embaixo; o aro de 1 px (claro em cima e à esquerda, escuro à direita), a face em
    duas águas com a aresta acesa no meio (a água da esquerda clara, a da direita escura) e um brilho curto no alto da
    esquerda. Os metais e a rampa são os do conjunto (a rampa de ferro). No lugar do escudo vermelho e dourado do jogo.
  - E1, Esquiva (mais difícil de acertar: +v na chance de esquiva, até o teto; o Passo Ágil dá +30% por 2 turnos e o
    Desaparecer +50% por 1): a rajada de vento, três traços na horizontal (o de cima e o de baixo terminando num cacho
    enrolado, para cima e para baixo; o do meio curto), claros, com a cauda mais escura à esquerda: movimento e ar, sem
    figura nem mão. No lugar da folha do jogo, que é também a Fúria da Natureza, o talento Pés Leves, o Antídoto e a
    Agilidade das celebrações, e que não diz "esquivar".
Os dois se distinguem do Firme (os dois elos na diagonal) e entre si pela forma: o escudo é um bloco vertical de metal;
o vento, traços horizontais abertos, num azul claro de ar.

Grava grades/<id>.txt e as listas por camada para o pintar.lua (listas/<id>/<camada>.lua).
    python icones16.py <pasta>
"""
import pathlib
import sys

CORES = {"#": "08080a",
         "3": "383c44", "4": "4c5159", "5": "646a73", "6": "848b94", "7": "b0b6bd", "8": "e4e8ec",   # a rampa de ferro
         "a": "e8f4f6", "b": "9fd0d8", "c": "4f8a96"}                                               # o ar: claro, cacho, cauda

GUARDA = ["................",
          "...##########...",
          "..#8888866666#..",
          "..#7776754443#..",
          "..#7666754443#..",
          "..#7666754443#..",
          "..#7666754443#..",
          "..#7666754443#..",
          "..#7666754443#..",
          "...#76675443#...",
          "...#76675443#...",
          "....#767543#....",
          ".....#7753#.....",
          "......#73#......",
          ".......##.......",
          "................"]
ESQUIVA = ["................",
           "..........##....",
           ".........#bb#...",
           "........#b##b#..",
           ".........#.#b#..",
           ".##########b#...",
           "#ccaaaaaaaa#....",
           ".##########.....",
           "....######......",
           "...#caaaaa#.....",
           "....######......",
           "...#########....",
           "..#ccaaaaaaa#...",
           "...#########b#..",
           "...........#b#..",
           "..........#b#..."]


def camada_guarda(x, y, ch, grade):
    if ch == "#": return "contorno"
    linha = grade[y]
    dentro = [i for i, c in enumerate(linha) if c not in ".#"]
    return "aro" if y == 2 or x in (dentro[0], dentro[-1]) else "face"


def camada_esquiva(x, y, ch, grade):
    return "contorno" if ch == "#" else "cachos" if ch == "b" else "rajadas"


ICONES = {"estado-guarda": (GUARDA, camada_guarda), "estado-esquiva": (ESQUIVA, camada_esquiva)}

if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    for ident, (grade, camada) in ICONES.items():
        assert len(grade) == 16 and all(len(l) == 16 for l in grade), ident
        (base / "grades").mkdir(exist_ok=True)
        (base / f"grades/{ident}.txt").write_text("\n".join(grade) + "\n", encoding="utf-8")
        listas = {}
        for y, l in enumerate(grade):
            for x, ch in enumerate(l):
                if ch != ".": listas.setdefault(camada(x, y, ch, grade), []).append(f"{x},{y},{CORES[ch]}")
        d = base / f"listas/{ident}"; d.mkdir(parents=True, exist_ok=True)
        for k, v in listas.items():
            (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
        print(ident, {k: len(v) for k, v in listas.items()})
