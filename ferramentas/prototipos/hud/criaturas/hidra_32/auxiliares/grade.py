"""A Hidra do Brejo construída em 32×32 nativos e adaptada à mão para 16 (pedido do Jean, 23/10/2026; protótipo, nada no
jogo), o caminho do Dragão de Gelo: as três cabeças de réptil olhando para a ESQUERDA (a orientação corrigida pelo Jean;
a referência `Hidra do pântano de três cabeças-1.png` dá o material, a anatomia e a expressão, não a direção), com
focinho, testa e mandíbula de verdade e pescoços grossos ligados ao corpo. A cabeça principal na frente, embaixo e à
esquerda, a boca entreaberta com as presas; a segunda no alto, atrás; a terceira à direita, no meio, atrás e em parte
escondida. As tentativas recusadas (a H1, a H2 e a `hidra-t`: cabecinhas na ponta de pescoços finos) não foram usadas. A
guia (a referência reduzida por média) fica oculta na fonte. Cada desenho foi pintado em três partes, da cabeça de trás
para a da frente (`pintar`): a de trás é coberta pela da frente onde se sobrepõem.
    python grade.py .. [<id> ...]      # grava grades/<id>.txt e listas/<id>/<camada>.lua (a guia, do png dela)
"""
import pathlib
import sys

from PIL import Image

PALETA = {"o": "101810", "s": "24382a", "m": "3a5a3e", "l": "5a7e52", "h": "82a06a", "k": "0a0c08",
          "e": "d8c040", "d": "e0d8b8", "r": "8a2e2e", "R": "4a1414"}


def pintar(partes, n):
    """Cada parte é uma lista de (linha, x, pixels); '.' não pinta. As de depois cobrem as de antes."""
    g = [["."] * n for _ in range(n)]
    for parte in partes:
        for y, x, s in parte:
            for i, ch in enumerate(s):
                if ch != "." and 0 <= x + i < n:
                    g[y][x + i] = ch
    return ["".join(l) for l in g]


# o estudo de 32: a cabeça de cima (B), a da direita (C) e a principal (A), nessa ordem
B = [
    (0, 14, "ooooooooo"),
    (1, 11, "ooohhhsshhhhoo"),
    (2, 10, "olklllmseksmmso"),
    (3, 10, "olllllmmssmmmso"),
    (4, 10, "ommmmmmmmmmmmso"),
    (5, 10, "oooooooooommsso"),
    (6, 11, "ollmmmmmmmssso"),
    (7, 12, "oossmmmmmmssso"),
    (8, 15, "ossmmmmmmsssso"),
    (9, 17, "osmmmmmmssssso"),
    (10, 18, "osmmmmmmssssss"),
    (11, 19, "osmmmmmsssssss"),
]
# a cabeça da direita, atrás (C): o focinho para a esquerda, escondido em parte atrás da A
C = [
    (11, 23, "ooooooooo"),
    (12, 20, "ooohhhsshhhh"),
    (13, 19, "olklllmseksmm"),
    (14, 19, "ollllmmmssmmm"),
    (15, 19, "ommmmmmmmmmmm"),
    (16, 19, "oooooooooommm"),
    (17, 20, "ollmmmmmmsmm"),
    (18, 21, "oossssmmmmm"),
    (19, 24, "smmmmmmmm"),
    (20, 24, "smmmmmmmm"),
    (21, 24, "smmmlmmmm"),
    (22, 24, "smmmlmmmm"),
    (23, 24, "smmmlmmmm"),
    (24, 24, "smmmlmmmm"),
    (25, 24, "smmlmmmmm"),
    (26, 23, "osmmlmmmmm"),
    (27, 23, "osmmlmmmmm"),
    (28, 23, "osmllmmmmm"),
    (29, 23, "osmllmmmmm"),
    (30, 22, "ossmllmmmmm"),
    (31, 22, "ossmllmmmmm"),
]
# a cabeça principal (A), na frente: o focinho longo e chato, a crista da testa sobre o olho de fenda, o lábio com as
# presas, a boca em cunha (alta na frente, fechando para trás), a mandíbula forte e o pescoço grosso
A = [
    (10, 8, "ooooooo"),
    (11, 3, "ooooohhhhhhhoooo"),
    (12, 1, "oollllhhhssshlllmmo"),
    (13, 0, "olkllllmmseksmllmmmmo"),
    (14, 0, "ollllllmmssssmmlmmmmo"),
    (15, 0, "ommmmmmmmmmmmmmllmmso"),
    (16, 0, "oooooooooooooommlmmso"),
    (17, 0, "..dRRRRdRRRRRomllmmso"),
    (18, 0, "..oRrrRRRRooommlmmsso"),
    (19, 0, "..odRRoooooommmlmmmsso"),
    (20, 0, "..ollllllmmmmmlmmmsso"),
    (21, 0, "...ossmmmmmmmmmmmsso"),
    (22, 0, "....oooosssmmmmmmssso"),
    (23, 5, "ooolllmmmmmmssso"),
    (24, 8, "olllmmmmmmssso"),
    (25, 8, "olhllmmmmmsssso"),
    (26, 8, "olhllmmmmmssssso"),
    (27, 9, "olhllmmmmmsssso"),
    (28, 9, "olhllmmmmmssssso"),
    (29, 10, "olhllmmmmmssssso"),
    (30, 10, "olhllmmmmmsssssso"),
    (31, 11, "olhllmmmmmsssssso"),
]
GRADE_32 = pintar([B, C, A], 32)

# a proposta de 16, redesenhada à mão com o 32 como mapa
B16 = [
    (0, 6, "oooooo"),
    (1, 4, "oohhhsso"),
    (2, 3, "olllmsekso"),
    (3, 3, "oooooommsso"),
    (4, 5, "ollmmmssso"),
    (5, 9, "osmmssso"),
    (6, 11, "smssss"),
]
C16 = [
    (5, 12, "oooo"),
    (6, 10, "oohhsso"),
    (7, 9, "olllseks"),
    (8, 9, "oooooomm"),
    (9, 11, "osssmm"),
    (10, 12, "smlm"),
    (11, 12, "smlm"),
    (12, 12, "smlmm"),
    (13, 11, "osmlmm"),
    (14, 11, "osmlmm"),
    (15, 11, "osmlmm"),
]
A16 = [
    (5, 2, "oohhhhoo"),
    (6, 0, "olllhsslmo"),
    (7, 0, "oklllekmmmo"),
    (8, 0, "ooooooomlmso"),
    (9, 0, ".dRrRRomlmso"),
    (10, 0, ".ollllmmmmso"),
    (11, 0, "..oossmmmsso"),
    (12, 4, "olhmmmsso"),
    (13, 4, "olhlmmmsso"),
    (14, 5, "olhlmmmsso"),
    (15, 5, "olhlmmmssso"),
]
GRADE_16 = pintar([B16, C16, A16], 16)
# A segunda construção de 32 (23/10/2026, o N32 preservado): as cabeças eram faixas horizontais de cor sobre os pescoços
# (o topo aceso, o meio, o lábio, a boca), da mesma altura da nuca à ponta. Cada cabeça virou uma cunha: o alto do crânio
# chato atrás, o calombo da testa pesando sobre o olho, o degrau até o focinho, a ponta baixa com a narina, o lábio com as
# presas, a boca em cunha (aberta na frente, o canto descendo) e a mandíbula baixa; o pescoço da principal é uma peça
# própria, saindo de trás da mandíbula. As de trás com a mesma anatomia, menores e um tom mais escuras.


def rows(lista):
    return [(y, 0, s) for y, s in lista]


# B2: a cabeça de cima, atrás
B2 = [
    (0, 21, "oooo"),
    (1, 20, "ollllooooooo"),
    (2, 17, "oolllllllmmmmmm"),
    (3, 16, "ollmsssslmmmmmm"),
    (4, 15, "olmmseeksmmsmmm"),
    (5, 14, "olkmmmmssmmmsmmm"),
    (6, 14, "ommmmmmmmmmmsmmm"),
    (7, 14, "oooooooooommsmms"),
    (8, 15, "osssssssssmsmss"),
    (9, 16, "ooooooossmsss"),
    (10, 23, "ossmsss"),
]
# C: a cabeça da direita, atrás, espiando por trás do crânio da principal
C2 = [
    (10, 26, "oooo"),
    (11, 25, "ollloooo"),
    (12, 23, "oolllllmmm"),
    (13, 23, "olmsseksmm"),
    (14, 22, "olkmmmmmsm"),
    (15, 22, "ommmmmmmsm"),
    (16, 22, "oooooooomm"),
    (17, 23, "osssssssm"),
    (18, 24, "oooossmm"),
] + [(y, x, s) for y, x, s in rows([
    (19, "........................osmmlmmm"),
    (20, "........................osmmlmmm"),
    (21, "........................osmllmmm"),
    (22, "........................osmllmmm"),
    (23, ".......................osmmllmmm"),
    (24, ".......................osmmllmmm"),
    (25, ".......................osmmllmmm"),
    (26, "......................ossmmllmmm"),
    (27, "......................ossmmllmmm"),
    (28, "......................ossmmllmmm"),
    (29, "......................ossmmllmmm"),
    (30, ".....................osssmmllmmm"),
    (31, ".....................osssmmllmmm"),
])]
# A: a principal, na frente: a cunha (o crânio alto atrás, a testa caindo até a ponta baixa do focinho), a crista sobre o
# olho, a narina, o lábio com as presas, a boca em cunha (aberta na frente, o canto descendo), a mandíbula pesada, a
# papada e o pescoço grosso
A2 = rows([
    (8,  "...........oooo........."),
    (9,  "..........ohhhhoooooooo."),
    (10, "........oohhhhhhhhllllmo"),
    (11, ".......ohhlsssslllmmmmmo"),
    (12, "......ohhlseekslmmmmmmso"),
    (13, ".....ohllllssssmlmsmmmso"),
    (14, "....oohhllllllmmmmsmmmso"),
    (15, "...ohhllllllmmmmmsommmso"),
    (16, "..ohkllllllmmmmmmsommsso"),
    (17, ".ohllllmmmmmmmmmsommmsso"),
    (18, ".olmmmmmmmmmmmmsommmsso."),
    (19, ".odsssssssssssssommmsso."),
    (20, "..dkRRRdRRRRRkommmsso..."),
    (21, "...kRrrRRRRkoommsso....."),
    (22, "...dkRRRRkoommmsso......"),
    (23, "..oolllllooommsso......."),
    (24, "..ohllllllmmmmsso......."),
    (25, "...ossssmmmmmsso........"),
    (26, ".....oooosssmmsso......."),
])
FAIXAS = {17: (16, 23), 18: (15, 23), 19: (14, 23), 20: (14, 23), 21: (13, 23), 22: (12, 23), 23: (11, 23),
          24: (10, 23), 25: (9, 23), 26: (8, 23), 27: (8, 23), 28: (9, 24), 29: (9, 24), 30: (10, 25), 31: (10, 25)}
PESCOCO2 = [(y, a, "o" + "lhll" + "m" * (b - a - 8) + "sss" + ("o" if b < 24 else "s")) for y, (a, b) in FAIXAS.items()]
GRADE_32B = pintar([B2, C2, PESCOCO2, A2], 32)
# A correção da cabeça principal (23/10/2026, o N32B preservado): a testa descia numa rampa contínua até o nariz, a
# bochecha era grande e o perfil lembrava um cachorro de desenho, com a boca comprida sugerindo um sorriso. Pela
# referência, a cabeça em peças: o focinho num bloco horizontal de topo chato, um degrau nítido até a testa, a sobrancelha
# escura e pesada sobre o olho (no encontro do focinho com o crânio), a bochecha pequena, a mandíbula como bloco à parte,
# inclinada para baixo, e a boca aberta em ângulo, com o fundo escuro e a língua. As duas de trás, o pescoço, a composição
# e a paleta como no N32B.
A3 = rows([
    (8,  "..........oooooo........"),
    (9,  "........oohhhhhhoooo...."),
    (10, ".......ohhhhhhhhhlllmo.."),
    (11, ".ooooooksssssslllmmmmmo."),
    (12, "ohhhhhhhskeesmlmmmmmmso."),
    (13, "ohkllllllssssmlmmmmmmso."),
    (14, "ollllllllmmmmmsmmmmmsso."),
    (15, "ommmmmmmmmmmmmsmmmmsso.."),
    (16, "oooooooooooooomsmmmsso.."),
    (17, ".dRRRRRRRRRkkosmmmsso..."),
    (18, ".dRRRRRRRRkkosmmmsso...."),
    (19, "..RRrrRRRkkooommmsso...."),
    (20, "..RrrRRkkooolmmmsso....."),
    (21, "..RRRkkoollllmmsso......"),
    (22, "..dRkoollllmmmsso......."),
    (23, "..ooollllllmmsso........"),
    (24, "..ohllllmmmsso.........."),
    (25, "...ossssssso............"),
    (26, ".....oooooo............."),
])
GRADE_32C = pintar([B2, C2, PESCOCO2, A3], 32)
# A reconstrução pela nova referência (23/10/2026, `Hidra tríplice do pântano em pixel art.png`, a direção principal; o
# N32C e as tentativas anteriores preservados): as três cabeças olhando para a esquerda, a principal maior e à frente, com
# o crânio redondo atrás do olho, a sobrancelha pesada, o focinho projetado com a narina, a boca aberta com duas presas em
# cima e uma embaixo (os dentes simplificados) e a mandíbula grossa; as de trás no alto e à direita, cada uma com o
# focinho, o olho sob a sobrancelha e uma presa; os pescoços grossos, o da principal saindo de trás da mandíbula, e a nuca
# de cada cabeça continuando no pescoço dela. A paleta é a oliva da referência, com o intervalo de valor aberto (o topo
# aceso, as sombras fundas); a guia é a imagem inteira reduzida por média (guias/hidra-d-guia-32.png).
PALETA_D = {"o": "121510", "D": "1c2218", "s": "2a3020", "m": "40462a", "M": "545730", "l": "6c6c3a", "h": "8e8c50",
            "H": "a8a466", "e": "e8a422", "k": "0a0c08", "d": "e6dcc0", "R": "4a1612", "r": "7a2a1e"}


def pescoco(faixas, miolo):
    """Um pescoço: por linha, de onde a onde; o ventre claro na frente, a sombra atrás."""
    return [(y, a, "o" + miolo + "m" * max(0, b - a - len(miolo) - 4) + "sso") for y, (a, b) in faixas.items()]


# B: a cabeça de cima, atrás; a boca fechada com as presas por fora
BD = [
    (1, 12, "oooo"),
    (2, 10, "oolhhloo"),
    (3, 9, "olsssllmmms"),
    (4, 8, "oMlsekmmmmsss"),
    (5, 7, "olkMMMmmmmmsss"),
    (6, 7, "oMMMMmmmmmmssss"),
    (7, 7, "ooodoosmmmmsso"),
    (8, 8, "osdssmmmmsso"),
    (9, 9, "ooossmmmsso"),
    (10, 12, "osmmmssso"),
]
NBD = pescoco({11: (14, 23), 12: (15, 24), 13: (15, 24), 14: (16, 25), 15: (16, 25), 16: (17, 26), 17: (17, 26),
              18: (18, 27), 19: (18, 27), 20: (19, 28)}, "mMl")
# C: a cabeça da direita, atrás
CD = [
    (7, 25, "oooo"),
    (8, 23, "oolhhloo"),
    (9, 22, "olsssllmmo"),
    (10, 21, "oMlsekmmmmso"),
    (11, 20, "olkMMMmmmmmso"),
    (12, 20, "oMMMMmmmmmmss"),
    (13, 20, "ooodoosmmmmss"),
    (14, 21, "osdssmmmmss"),
    (15, 22, "ooossmmmss"),
]
NCD = pescoco({y: (24, 33) for y in range(16, 32)}, "mMl")
# A: a principal, na frente: o crânio redondo atrás do olho, a sobrancelha pesada, o degrau até o focinho, o focinho
# projetado com a narina, o lábio com as presas, a boca aberta, a mandíbula grossa
NAD = pescoco({17: (15, 24), 18: (14, 25), 19: (14, 25), 20: (13, 26), 21: (13, 26), 22: (12, 26), 23: (12, 27),
              24: (11, 27), 25: (11, 27), 26: (10, 28), 27: (10, 28), 28: (9, 28), 29: (9, 29), 30: (9, 29),
              31: (9, 29)}, "mlHHl")
AD = [
    (10, 8, "ooooo"),
    (11, 6, "oohhhhhoo"),
    (12, 5, "ohhhhhhhllmm"),
    (13, 4, "ohhlllllllmmmm"),
    (14, 3, "ohhhhhhhllllmmmm"),
    (15, 2, "ohssssssllmmmmmm"),
    (16, 1, "ohhhhlseksllmmmmmm"),
    (17, 0, "ohkMMMlMssssMmmmmso"),
    (18, 0, "oMMMMMMMMmmmmmmmsso"),
    (19, 0, "omMMMMMmmmmmmmmmsso"),
    (20, 1, "odoooodoooommmmsso"),
    (21, 1, "odRRRRdRRRRkomMmmsso"),
    (22, 1, "oRRrrrRRRRkoomMmsso"),
    (23, 2, "oRdRRRRkoommMmsso"),
    (24, 2, "oodooooooolllmmsso"),
    (25, 2, "oHllllllllllmmmsso"),
    (26, 3, "olllllllllmmmmsso"),
    (27, 4, "osssmmmmmmmmsso"),
    (28, 6, "oooosssssssso"),
]
GRADE_32D = pintar([BD, NBD, CD, NCD, NAD, AD], 32)
# A adaptação do N32D para 16 (23/10/2026, o N32D aprovado como base e preservado): redesenhada à mão na grade de 16, com
# o 32 como mapa das posições e dos volumes, na ordem: as três cabeças para a esquerda; a principal maior, à frente e
# embaixo; o focinho, a sobrancelha, a boca e a mandíbula dela; a separação das menores e os pescoços contínuos. Os dentes
# simplificados (uma presa em cima e uma embaixo na principal; uma em cada cabeça de trás) e o alto das de trás aceso,
# para não sumirem contra o fundo escuro da carta.
B16D = [
    (0, 4, "oooo"),
    (1, 3, "ohssmmo"),
    (2, 2, "oMlekmms"),
    (3, 2, "oMMMmmmss"),
    (4, 2, "oodooms"),
]
NB16D = [(5, 8, "Mmss"), (6, 8, "mmss"), (7, 9, "mms"), (8, 9, "mms")]
C16D = [
    (3, 11, "ooo"),
    (4, 10, "ohssmmm"),
    (5, 10, "oMekmm"),
    (6, 10, "oMMMmm"),
    (7, 10, "oodoms"),
    (8, 11, "oosmm"),
]
NC16D = [(y, 12, "olms") for y in range(9, 16)]
NA16D = [(7, 8, "mmms"), (8, 8, "mmmss"), (9, 8, "mmmss"), (10, 7, "mmmmss"), (11, 7, "lmmmss"), (12, 6, "lmmmmss"),
      (13, 6, "llmmmss"), (14, 5, "mlHHlmmss"), (15, 4, "omlHHlmmss")]
A16D = [
    (5, 4, "ooo"),
    (6, 2, "oohhhlm"),
    (7, 1, "ohhsssllm"),
    (8, 0, "ohhleksmmm"),
    (9, 0, "okMMMMmmmm"),
    (10, 0, "odoooooms"),
    (11, 1, "dRrrRRkom"),
    (12, 1, "oodooooom"),
    (13, 1, "oHllllmmm"),
    (14, 2, "osssmmso"),
]
GRADE_16D = pintar([B16D, NB16D, C16D, NC16D, NA16D, A16D], 16)
# a paleta de cada desenho (a da nova referência só no N32D e no N16D)
PALETAS = {"hidra-n32d": PALETA_D, "hidra-n16d": PALETA_D}
# cada desenho: a grade, o lado e a guia
DESENHOS = {"hidra-n32": (GRADE_32, 32, "guias/hidra-guia-32.png"),
            "hidra-n16": (GRADE_16, 16, "guias/hidra-guia-16.png"),
            "hidra-n32b": (GRADE_32B, 32, "guias/hidra-guia-32.png"),
            "hidra-n32c": (GRADE_32C, 32, "guias/hidra-guia-32.png"),
            "hidra-n32d": (GRADE_32D, 32, "guias/hidra-d-guia-32.png"),
            "hidra-n16d": (GRADE_16D, 16, "guias/hidra-d-guia-16.png")}
# as camadas, de baixo para cima (a guia por baixo de tudo)
ORDEM = ["guia", "escamas", "boca", "olhos", "contorno"]


def camada(x, y, ch, ident):
    if ch == "o":
        return "contorno"
    if ch in "ek":  # o olho (âmbar com a pupila) e a narina
        return "olhos"
    if ch in "drR":
        return "boca"
    return "escamas"


def imagem(ident):
    grade, n, _ = DESENHOS[ident]
    paleta = PALETAS.get(ident, PALETA)
    im = Image.new("RGBA", (n, n))
    for y, l in enumerate(grade):
        for x, ch in enumerate(l):
            if ch != ".":
                im.putpixel((x, y), tuple(int(paleta[ch][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def gravar(base, ident):
    grade, n, guia = DESENHOS[ident]
    assert len(grade) == n and all(len(l) == n for l in grade), (ident, [len(l) for l in grade])
    (base / "grades").mkdir(parents=True, exist_ok=True)
    (base / f"grades/{ident}.txt").write_text("\n".join(grade) + "\n", encoding="utf-8")
    g = Image.open(base / guia).convert("RGBA")
    listas = {c: [] for c in ORDEM}
    listas["guia"] = [f"{x},{y},{''.join(f'{v:02x}' for v in g.getpixel((x, y)))}" for y in range(n) for x in range(n)
                      if g.getpixel((x, y))[3]]
    for y, l in enumerate(grade):
        for x, ch in enumerate(l):
            if ch != ".":
                listas[camada(x, y, ch, ident)].append(f"{x},{y},{PALETAS.get(ident, PALETA)[ch]}")
    d = base / f"listas/{ident}"
    d.mkdir(parents=True, exist_ok=True)
    for k, v in listas.items():
        (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
    (d / "ordem.txt").write_text(",".join(ORDEM) + "\n", encoding="utf-8")
    print(ident, {k: len(v) for k, v in listas.items()})


if __name__ == "__main__":
    for ident in sys.argv[2:] or DESENHOS:
        gravar(pathlib.Path(sys.argv[1]), ident)
