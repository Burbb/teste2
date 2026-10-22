"""A segunda rodada dos quatro pares (22/10/2026, pedido do Jean; propostas, nada no jogo): sobre as direções
escolhidas no lote de quatro_pares/, três capuzes para o cultista, três rostos para a bruxa, o carniçal com a boca
refeita, o espectro de olho único, o javali de presas grandes e três reconstruções do rato. 16×16 na linguagem dos
retratos aprovados, vistas a 2× na carta (32 px) e a 3× no Bestiário (48 px). As grades à mão; as fontes no Aseprite
pelo conector (o pintar.lua), em fontes/<id>/<id>-16.aseprite.
    python grades.py <pasta> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

# as paletas: as do primeiro lote (quatro_pares/auxiliares/grades.py), com poucos tons a mais
CORES_CULTO_BRUXA = {
    "V": "241010",
    "v": "461c1c",
    "x": "6a2a26",
    "X": "8c3c30",
    "F": "c4a284",
    "f": "8e6a54",
    "E": "1a1210",
    "Z": "9a6ac0",
    "z": "5a3a7a",
    "H": "1f1c16",
    "h": "3a352a",
    "m": "4f5a2e",
    "M": "6f7a3a",
    "P": "b0a48a",
    "p": "7e745e",
    "c": "c8c4b4",
    "e": "141210",
    "q": "8a8478",
    "Q": "b8b4a8",
    "G": "6cc04a",
    "g": "3a7a2e",
    "w": "9a9a78",
    "W": "c4c09c",
    "T": "d8d0bc",
}
# (w e W: a pele da bruxa no tom do brejo; T: o dente)
CORES_CARNE_NEVOA = {
    "L": "a89a96",
    "l": "7a6c6c",
    "d": "4e4246",
    "D": "2e262a",
    "Y": "d0c060",
    "R": "8a1e1e",
    "T": "d8d0bc",
    "k": "120c0c",
    "t": "b0a690",
    "C": "aeb6c4",
    "c": "7a8698",
    "s": "4c5468",
    "S": "343a4a",
    "V": "0c0e14",
    "E": "b8eef0",
    "G": "5a2a2e",
}
# (G: a gengiva escura; t: o dente na sombra)
CORES_JAVALI = {
    "J": "1e1612",
    "j": "3a2a20",
    "b": "5a4232",
    "B": "7a5c44",
    "n": "9a7462",
    "N": "c0988a",
    "o": "2a1814",
    "T": "e6dcc4",
    "E": "b0381e",
    "K": "1e1a18",
    "r": "443a34",
    "R": "6a5e56",
    "g": "928678",
    "p": "c4908a",
    "P": "8a5a58",
    "Y": "d8c070",
    "e": "d0302a",
    "t": "b4aa90",
    "Q": "8e8670",
}
# (t: a presa na sombra; Q: a base da presa)
CORES_RATO = {
    "J": "1e1612",
    "j": "3a2a20",
    "b": "5a4232",
    "B": "7a5c44",
    "n": "9a7462",
    "N": "c0988a",
    "o": "2a1814",
    "T": "e6dcc4",
    "E": "b0381e",
    "K": "1e1a18",
    "r": "443a34",
    "R": "6a5e56",
    "g": "928678",
    "p": "c4908a",
    "P": "8a5a58",
    "Y": "d8c070",
    "e": "d0302a",
    "D": "2c2622",
    "y": "c08a30",
}
# (D: o pelo mais fundo; y: o incisivo alaranjado na sombra)

# O cultista, três capuzes a partir do A (o capuz vermelho, o rosto encoberto, a marca violeta):
# c1, o capuz pontudo: o bico alto caindo para trás, a abertura estreita, o rosto quase todo na sombra (só o nariz
# e a boca), a marca na testa e no peito
CULT_C1 = [
    ".......X........",
    "......xXv.......",
    ".....xXxvv......",
    "....xXxxvvv.....",
    "...xXxVVVVvv....",
    "...xXVVZVVVvv...",
    "..xXxVVzVVVvvv..",
    "..xXVVfFfVVvvv..",
    "..xXVVFFFfVvvv..",
    "..xXvVfFfVVvvv..",
    ".xXxvvVVVVvvvvv.",
    ".xXxxvvzZvvvvvvV",
    "xXxxxvvzZvvvvvVV",
    "xXxxvvvzZvvvvVVV",
    "xxxvvvvvvvvvVVVV",
    "xxvvvvvvvvvVVVVV",
]
# c2, o capuz largo: a abertura emoldurando o rosto, os olhos escuros sob a marca vertical na testa
CULT_C2 = [
    "................",
    "....xxXXXxxv....",
    "...xXXxxxxxvv...",
    "..xXxxvvvvvxvv..",
    "..xXxvVVVVVvxvv.",
    ".xXxvVfFZfVvvxv.",
    ".xXxVfEFzEfVvxv.",
    ".xXxVfFFFFfVvvv.",
    ".xXxVVfFFfVVvvv.",
    ".xXxvVVffVVvvvv.",
    "xXxxvvVVVVvvvvvV",
    "xXxvvvvzZvvvvvVV",
    "xxXvvvvzZvvvvVVV",
    "xxxvvvvzZvvvvVVV",
    "xxvvvvvvvvvvVVVV",
    "xvvvvvvvvvvVVVVV",
]
# c3, o capuz que avança: a aba projetada cobre os olhos com uma faixa de sombra, a marca bordada na testa do capuz
CULT_C3 = [
    "................",
    ".....xxXXxx.....",
    "....xXXXXxxv....",
    "...xXXxZZxxvv...",
    "..xXXxxzzxxxvv..",
    "..xXxxxxxxxxvvv.",
    "..xXVVVVVVVVvvv.",
    "..xXVVfVVfVVvvv.",
    "..xXvVfFFfVvvvv.",
    "...xvVfFFfVvvv..",
    "...xvVVffVVvvv..",
    "..xXvvVVVVvvvvV.",
    ".xXxvvvvvvvvvVVV",
    "xXxxvvvvvvvvVVVV",
    "xxxvvvvvvvvVVVVV",
    "xxvvvvvvvvvVVVVV",
]

# A bruxa, três rostos a partir da A (o chapéu de aba mole com musgo, o cabelo grisalho, o xale), a pele no tom do
# brejo:
# b1, o nariz adunco para o lado, o olho apertado, o sorriso torto com um dente
BRUXA_B1 = [
    "................",
    "......hhhh......",
    ".....hMmhhh.....",
    "....hMmmhhhh....",
    "..HhhhhhhhhhhhH.",
    ".HhhmmhhhhhhmhhH",
    "...qqwWWWwwqq...",
    "..qqWeWWWeWwq...",
    "..qqwWWWWwwwq...",
    ".WWwWWWWwwwqq...",
    "..WwWwwTwwqq....",
    "..q.wwhhhwq.....",
    "..hhhmmwwmmhhh..",
    ".hhhhmmhhmmhhhh.",
    "hhhhhhhhhhhhhhhh",
    "HHhhhhhhhhhhhhHH",
]
# b2, um olho saltado e leitoso e o outro fechado, o nariz verruguento, a careta; o chapéu de ponta torta
BRUXA_B2 = [
    "..........hh....",
    "........hhMh....",
    "......hhMmh.....",
    ".....hMmmhh.....",
    "..HhhhhhhhhhhhH.",
    ".HhhmmhhhhhhmhhH",
    "...qqwWWWwwqq...",
    "..qqccWWeewwq...",
    "..qqcecWWwwwq...",
    "..qqccWwwwwwq...",
    "..q.wWWmWwwqq...",
    "..q.wwmemwwq....",
    "..hhhmwwwwmhhh..",
    ".hhhhmmhhmmhhhh.",
    "hhhhhhhhhhhhhhhh",
    "HHhhhhhhhhhhhhHH",
]
# b3, o rosto comprido de faces fundas e o sorriso largo e banguela sob a aba caída com junco
BRUXA_B3 = [
    "................",
    "......hhhh......",
    ".....hMmhhh.....",
    "....hMmmhhhh....",
    ".HhhhhhhhhhhhhhH",
    "HhmmhhhhhhhhhmmH",
    "m.qqwwwwwwwwqq.m",
    "..qqweWwwWewqq..",
    "..qqwWWwwWWwqq..",
    "..qq.wWwwWw.qq..",
    "..qq.weTeTe.qq..",
    "..q..wwwwww..q..",
    "..hhhmwwwwmhhh..",
    ".hhhhmmhhmmhhhh.",
    "hhhhhhhhhhhhhhhh",
    "HHhhhhhhhhhhhhHH",
]

# O carniçal A2: a boca aberta com a gengiva escura, os dentes de cima presos à arcada (as presas nos cantos), a
# garganta escura, os dentes de baixo na mandíbula caída e o sangue escorrendo; o resto do A
CARN_A2 = [
    "................",
    ".....dlllld.....",
    "....dlLLLlld....",
    "...dlLLLLllld...",
    "...lLdkLLkdld...",
    "...lLkYlLYkdd...",
    "...dLlllllldD...",
    "...dLlGGGGldD...",
    "...dlTtTTtTldD..",
    "...dlTkkkkTldD..",
    "...dlkkkkkkld...",
    "...dltkkkktld...",
    "....dTRTTtGd....",
    "..ddDdlRllDDdd..",
    ".dlLldDllDdlLld.",
    "dlLlldttttdllLld",
]
# O espectro A2: o trapo suspenso e irregular, a cavidade escura funda no centro e o olho dentro dela (a íris pálida
# em volta da pupila), as pontas rasgadas em comprimentos diferentes, flutuando (a linha de baixo vazia)
ESP_A2 = [
    "................",
    "......scc.......",
    ".....cCCCcs.....",
    "...scCCcCCcs....",
    "..scCcSSSScss...",
    "..cCSVVVVVScs...",
    ".scCVVEEEVVSs...",
    ".cCSVEEVEEVScs..",
    ".cCSVVEEEVVScs..",
    ".scCSVVVVVSccs..",
    "..cCcSSSSScccs..",
    "..cCc.cCc.ccs...",
    "..cc..cC..c.s...",
    "..c...c...c.....",
    "......s.........",
    "................",
]
# O javali A2: as presas grossas (dois pixels) nascendo ao lado do focinho e subindo em curva para fora até a altura
# dos olhos, maiores que as do Troll, o nariz entre elas
JAV_A2 = [
    "................",
    "..J..........J..",
    "..jJ.J.JJ.J.Jj..",
    "..jbJjJjjJjJbj..",
    ".jjbBbbjjbbBbjj.",
    ".jbEbBbbbbBbEbj.",
    "TjbbBBbbbbBBbbjT",
    "TTjbBnnnnnnBbjTT",
    "tTTbnNNNNNNnbTTt",
    ".tTQnNoNNoNnQTt.",
    "..tTQnNNNNnQTt..",
    "...tTnnnnnnTt...",
    "...jjbbbbbbjj...",
    "..jbbjbbbbjbbj..",
    ".jbbBbJJJJbBbbj.",
    "JjjjjJJJJJJjjjjJ",
]

# O rato, três reconstruções (a anatomia estudada em fotos do Wikimedia Commons, só para a forma: a cabeça em cunha
# até o nariz, o olho pequeno a um terço do focinho, a orelha redonda recuada, a cabeça emendada no pescoço grosso,
# os incisivos alaranjados):
# r1, de perfil farejando: a cabeça baixa em cunha, o nariz e os incisivos embaixo, a orelha no alto, o pescoço maciço
RATO_R1 = [
    "................",
    "................",
    ".........rr.....",
    "........rPpr....",
    ".......rPppPr...",
    "......rRRRRRrD..",
    ".....rRgRRRRRrD.",
    "....rRggRKeRRRrD",
    "...rRgggRRRRRRrD",
    "..rRgggRRRRRRRRD",
    ".pRgggRRRRRRRRRD",
    "pPgggrRRRRRRRRrD",
    ".YYggrRRRRRRRrDD",
    "..yrrrrRRRRRrrDD",
    "....rrrRRRRrrDDD",
    "...DrrrrrrrrDDDD",
]
# r2, de frente e de cabeça baixa: as orelhas redondas no alto, o focinho comprido descendo até o nariz e os
# incisivos, a massa dos ombros embaixo
RATO_R2 = [
    "................",
    "................",
    "................",
    "..pPr......rPp..",
    ".pPPPr....rPPPp.",
    ".rPPrRRRRRRrPPr.",
    "..rRRRRggRRRRr..",
    "..rRKeRggReKRr..",
    "..rRRRggggRRRr..",
    ".rrRRRggggRRRrr.",
    "rRRrRRggggRRrRRr",
    "rRRrrRpPPpRrrRRr",
    "rRRRrrPPPPrrRRRr",
    "DRRRRrYYYYrRRRRD",
    "DDRRRrYyyYrRRRDD",
    "DDDRRRrrrrRRRDDD",
]
# r3, em três quartos para a direita sibilando: a boca aberta com os incisivos, o nariz na ponta, a orelha atrás
RATO_R3 = [
    "................",
    "................",
    "......rPpr......",
    ".....rPppPr.....",
    "....rRRRRRRr....",
    "...rRRRRRRgRr...",
    "..rRRRReKRggRr..",
    ".rRRRRRRRRgggRr.",
    ".rRRRRRRRRggggPp",
    ".rRRRRRRRKKKYYgp",
    ".rrRRRRRRKKgYy..",
    ".DrrRRRRRRggg...",
    ".DDrrrRRRRRRr...",
    "DDDrrRRgRRRRRr..",
    "DDrrRRRRRRRRRRr.",
    "DDrRRRRRRRRRRRRr",
]


def _culto(x, y, ch):
    return "marca" if ch in "Zz" else "rosto" if ch in "FfE" else "manto"


def _bruxa(x, y, ch):
    return "chapeu" if y <= 5 else "cabelo" if ch in "qQ" else "rosto" if ch in "wWceTmP" and y <= 11 else "xale"


def _rato(x, y, ch):
    return "olhos" if ch in "eK" else "dentes" if ch in "Yy" else "pele" if ch in "pP" else "corpo"


CAMADAS = {
    "cultista-c1": (CULT_C1, ["manto", "rosto", "marca"], _culto, CORES_CULTO_BRUXA),
    "cultista-c2": (CULT_C2, ["manto", "rosto", "marca"], _culto, CORES_CULTO_BRUXA),
    "cultista-c3": (CULT_C3, ["manto", "rosto", "marca"], _culto, CORES_CULTO_BRUXA),
    "bruxa-b1": (BRUXA_B1, ["xale", "cabelo", "rosto", "chapeu"], _bruxa, CORES_CULTO_BRUXA),
    "bruxa-b2": (BRUXA_B2, ["xale", "cabelo", "rosto", "chapeu"], _bruxa, CORES_CULTO_BRUXA),
    "bruxa-b3": (BRUXA_B3, ["xale", "cabelo", "rosto", "chapeu"], _bruxa, CORES_CULTO_BRUXA),
    "carnical-a2": (CARN_A2, ["corpo", "rosto", "boca"],
                    lambda x, y, ch: "boca" if ch in "RTktG" and 7 <= y <= 13 else "rosto" if y <= 11 else "corpo",
                    CORES_CARNE_NEVOA),
    "espectro-a2": (ESP_A2, ["nevoa", "cavidade", "olho"],
                    lambda x, y, ch: "olho" if ch == "E" else "cavidade" if ch in "VS" and 4 <= y <= 10 else "nevoa",
                    CORES_CARNE_NEVOA),
    "javali-a2": (JAV_A2, ["corpo", "focinho", "presas", "olhos"],
                  lambda x, y, ch: "olhos" if ch == "E" else "presas" if ch in "TtQ" else "focinho" if ch in "nNo" else "corpo",
                  CORES_JAVALI),
    "rato-r1": (RATO_R1, ["corpo", "pele", "dentes", "olhos"], _rato, CORES_RATO),
    "rato-r2": (RATO_R2, ["corpo", "pele", "dentes", "olhos"], _rato, CORES_RATO),
    "rato-r3": (RATO_R3, ["corpo", "pele", "dentes", "olhos"], _rato, CORES_RATO),
}


def imagem(ident):
    grade, _, _, cores = CAMADAS[ident]
    im = Image.new("RGBA", (16, 16))
    for y, l in enumerate(grade):
        for x, ch in enumerate(l):
            if ch != ".":
                im.putpixel((x, y), tuple(int(cores[ch][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def gravar(base, ids=None):
    for ident in ids or CAMADAS:
        grade, ordem, camada, cores = CAMADAS[ident]
        assert len(grade) == 16 and all(len(l) == 16 for l in grade), (ident, [len(l) for l in grade])
        (base / "grades").mkdir(parents=True, exist_ok=True)
        (base / f"grades/{ident}.txt").write_text(chr(10).join(grade) + chr(10), encoding="utf-8")
        listas = {k: [] for k in ordem}
        for y, l in enumerate(grade):
            for x, ch in enumerate(l):
                if ch != ".":
                    listas[camada(x, y, ch)].append(f"{x},{y},{cores[ch]}")
        d = base / f"listas/{ident}"
        d.mkdir(parents=True, exist_ok=True)
        for k, v in listas.items():
            (d / f"{k}.lua").write_text('return "' + ";".join(v) + '"' + chr(10), encoding="utf-8")
        (d / "ordem.txt").write_text(",".join(ordem) + chr(10), encoding="utf-8")
        print(ident, {k: len(v) for k, v in listas.items()})


if __name__ == "__main__":
    gravar(pathlib.Path(sys.argv[1]), sys.argv[2:])
