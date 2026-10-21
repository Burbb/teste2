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

As rodadas seguintes da Esquiva (20/10 e 21/10/2026, pedidos do Jean; a E1 não foi aprovada: lembrava um símbolo
meteorológico):
  - E2 (estado-esquiva-e2, guardada como histórico, não aprovada: não comunicava evasão): o crescente principal fino
    nas pontas, de baixo-esquerda para cima-direita, e um crescente menor por dentro; antes dela, na bancada, a curva
    com a cabeça pesada lia como lâmina ou "visto", o arco como arco-íris, o traço com a ponta ">" como seta;
  - E3 (estado-esquiva-e3), a bota dando um passo: a bota de couro escuro de perfil (o couro das botas do jogo), a ponta
    para a direita, a sola escura, e o rastro curto atrás do calcanhar (dois traços de ar, o de baixo mais comprido).
    Fica perto da bota da Agilidade e do Fugir (a bota laranja em passada com os riscos): o couro escuro e o rastro em
    azul de ar são a diferença, e a avaliação diz se basta;
  - E4 (estado-esquiva-e4), a figura que sai do lugar: uma silhueta simples (a cabeça e o corpo, sem anatomia, o
    contorno do conjunto) inclinada para a direita, e o fantasma pontilhado, em pé, onde ela estava (sem contorno: a
    imagem que ficou para trás). Na bancada, os fantasmas sólidos liam como uma fileira de peças de xadrez.
Grava grades/<id>.txt e as listas por camada para o pintar.lua (listas/<id>/<camada>.lua).
    python icones16.py <pasta>
"""
import pathlib
import sys

CORES = {"#": "08080a",
         "3": "383c44", "4": "4c5159", "5": "646a73", "6": "848b94", "7": "b0b6bd", "8": "e4e8ec",   # a rampa de ferro
         "a": "e8f4f6", "b": "9fd0d8", "c": "4f8a96",                                               # o ar: claro, cacho, cauda
         "K": "b08c62", "L": "8e6236", "M": "724b2a", "N": "57381f", "O": "3e2716", "S": "1c1510"}    # o couro das botas

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


ESQUIVA_E2 = [".............#..", "............#a#.", "............#a#.", "........#...#a#.", ".......#b#.#aa#.",
              ".......#b#.#aa#.", "......#bb##aaa#.", "....##bb#.#aaa#.", "...#cbb#.#baaa#.", "....###.#bbbb#..",
              "......##bbbb#...", "...###cbbbb#....", ".##ccccbbb#.....", "#ccccccc##......", ".#######........",
              "................"]
ESQUIVA_E3 = ["................", "................", "......####......", ".....#KLLM#.....", ".....#KLMN#.....",
              ".....#KLMN#.....", ".....#KLMN#.....", ".###.#KLMNN#....", "#cba#KKLMNNN#...", ".####KKLLMNNO#..",
              "######KKLLMMNO#.", "ccbba##SSSSSSSS#", "#####..###SSSS#.", "..........####..", "................",
              "................"]
ESQUIVA_E4 = ["................", "................", "................", "...........##...", "..........#66#..",
              "...5.....#7866#.", "..5.5....#7766#.", "...5.5...##76#..", "....5...#7777#..", "...5.5.#77777#..",
              "..5.5.5777777#..", ".5.5.5#77777#...", "..5.5.577777#...", ".5.5.5.#####....", "................",
              "................"]


def camada_e2(x, y, ch, grade):
    return "contorno" if ch == "#" else "crescentes"


def camada_e3(x, y, ch, grade):
    return "contorno" if ch == "#" else "rastro" if ch in "abc" else "bota"


def camada_e4(x, y, ch, grade):
    return "contorno" if ch == "#" else "fantasma" if ch == "5" else "figura"


ICONES = {"estado-guarda": (GUARDA, camada_guarda), "estado-esquiva": (ESQUIVA, camada_esquiva),
          "estado-esquiva-e2": (ESQUIVA_E2, camada_e2), "estado-esquiva-e3": (ESQUIVA_E3, camada_e3),
          "estado-esquiva-e4": (ESQUIVA_E4, camada_e4)}

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
