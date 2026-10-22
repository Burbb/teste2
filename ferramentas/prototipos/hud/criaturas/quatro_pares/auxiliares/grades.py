"""Os quatro pares da madrugada de 22/10/2026 (1E.3, pedido do Jean; propostas, nada no jogo): duas direções para cada
criatura, cabeças/bustos de 16×16 na linguagem dos retratos aprovados (sem contorno, a paleta contida, a luz da
esquerda), vistas a 2× na carta (32 px) e a 3× no Bestiário e no mural (48 px). As grades à mão; as fontes no Aseprite
pelo conector (o pintar.lua), em fontes/<id>/<id>-16.aseprite.
    python grades.py <pasta> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

CORES = {}

# Par 1, o pântano: o sapo-touro gigante e a sanguessuga gigante (os dois hoje no "fera", o rosto de lobo)
CORES.update({
    # o sapo: o lodo escuro, o oliva, o oliva claro, a barriga, a barriga na sombra, o olho, a pupila, a boca, o veneno
    "K": "1c1a10", "G": "3d3a1f", "g": "5f5a2e", "h": "85803f", "c": "b8a77a", "C": "8f805a", "Y": "d0a030", "k": "100e0a",
    "M": "2a1612", "O": "c06a2a",
    # a sanguessuga: o escuro, o corpo, o brilho úmido, a faixa avermelhada, o lábio, os dentes, a água
    "S": "1e1a17", "s": "211c16", "t": "3e3628", "w": "6a604a", "r": "7a3a28", "R": "a3433a", "P": "d9b5a0", "A": "1d2e2c",
    "a": "2e4440",
})
# Sapo A, de frente: a cabeçorra larga enchendo a carta, os olhos saltados sob a sobrancelha pesada (a pupila
# horizontal), a boca de ponta a ponta caindo nos cantos, as manchas do veneno, a papada clara
SAPO_A = [
    "................",
    "................",
    "..GGG......GGG..",
    ".GgGGG....GGGgG.",
    ".GYkkG....GkkYG.",
    ".GYYYGGggGGYYYG.",
    "GgGGgghhhhggGGgG",
    "GghgOgghhggOghgG",
    "GgggghhhhhhggggG",
    "KMMMMMMMMMMMMMMK",
    "GMCcccccccccccMG",
    "GgCcCcccccCcCCgG",
    "KGgCccccccccCgGK",
    "KKGGCCccccCCGGKK",
    ".KKGGGGGGGGGGKK.",
    "..KKKKKKKKKKKK..",
]
# Sapo B, de perfil para a esquerda: o papo inchado (o coaxar), o olho alto, a boca comprida, a pata da frente
SAPO_B = [
    "................",
    "................",
    "................",
    "....GGG.........",
    "...GYkYG........",
    "..GgYYgGGGGG....",
    ".GhhgggghhgGG...",
    "GhhgOghhgggOgG..",
    "MMMMMMMghhgggGG.",
    "MCcccCMggghhggG.",
    ".CccccCCgggOggGK",
    ".CCcccCCGggggGGK",
    "..CCCCGgGGgggGK.",
    "....GhgGKGGGGK..",
    "...GhhG.KKKKK...",
    "..KKKK..........",
]
# Sanguessuga A, empinada de frente: a ventosa redonda com o anel de dentes, o corpo gordo em anéis com a faixa, a água
SANG_A = [
    "................",
    "...ssttttts.....",
    "..sRRRRRRRRs....",
    ".sRrPrPrPrPRs...",
    ".sRPkkkkkkPRs...",
    ".sRrkkkkkkrRs...",
    ".sRPkkkkkkPRs...",
    ".sRrPrPrPrPRs...",
    ".stRRRRRRRRts...",
    ".swttrttrttws...",
    ".ssssssssssss...",
    ".stwtrttrtwts...",
    ".ssssssssssss...",
    "..stwrttrwts....",
    "AaAstrttrtsAaAaA",
    "aAaAasssssaAaAaA",
]
# Sanguessuga B, o corpo em curva saindo da água, a cabeça com a boca de dentes para a esquerda
SANG_B = [
    "................",
    "................",
    "..sRRRs.........",
    ".sRPkPRs........",
    ".sRkkkRws.......",
    "..sRPRwtws......",
    "...stwtrtws.....",
    "....stwrtwts....",
    ".....stwrtwts...",
    "......stwrtwts..",
    ".......stwrtws..",
    "......stwrtwts..",
    ".....stwrtwts...",
    "....stwrtwts....",
    "AaAstwrtwtsAaAaA",
    "aAaAasssssaAaAaA",
]

# Par 2, os conjuradores humanos: o cultista e a bruxa do pântano (os dois hoje no "humano", o bandido de lenço)
CORES2 = {
    # o cultista: o manto vermelho-escuro (do escuro ao claro), a pele, a sombra da pele, o olho, a marca violeta da Fenda
    "V": "241010", "v": "461c1c", "x": "6a2a26", "X": "8c3c30", "F": "c4a284", "f": "8e6a54", "E": "1a1210", "Z": "9a6ac0",
    "z": "5a3a7a",
    # a bruxa: o chapéu e o xale (o escuro, o meio, o musgo), a pele, a pele na sombra, o olho branco, o olho, o cabelo, o
    # frasco verde (a cura e o veneno)
    "H": "1f1c16", "h": "3a352a", "m": "4f5a2e", "M": "6f7a3a", "P": "b0a48a", "p": "7e745e", "c": "c8c4b4", "e": "141210",
    "q": "8a8478", "Q": "b8b4a8", "G": "6cc04a", "g": "3a7a2e",
}
# Cultista A, encapuzado de frente: o capuz vermelho-escuro, o rosto na sombra, a marca violeta da Fenda na testa e no
# peito
CULT_A = [
    "......xxxx......",
    ".....xXXxxv.....",
    "....xXxxxxvv....",
    "...xXxVVVVvvv...",
    "...xXVVZZVVvv...",
    "..xXxVfzzfVvvv..",
    "..xXvVEffEVvvv..",
    "..xXvVfFFfVvvv..",
    "..xXvVfFFfVvvv..",
    "..xxvVVffVVvvv..",
    ".xXxvvVVVVvvvvv.",
    ".xXxxvvzZvvvvvv.",
    "xXxxxvvzZvvvvvvv",
    "xXxxvvvzZvvvvvVV",
    "xxxvvvvvvvvvvVVV",
    "xxvvvvvvvvvvVVVV",
]
# Cultista B, sem capuz: a cabeça raspada com a cicatriz ritual em fenda, o olhar fixo, a boca fina, o manto com a faixa
CULT_B = [
    "................",
    "......ffFFf.....",
    ".....fFFFFFf....",
    "....fFFFZFFff...",
    "....FFFFzFFff...",
    "....FFFFzFFff...",
    "....FcEFzFcEf...",
    "....fFFFFFFff...",
    ".....FfFfFff....",
    ".....fFfffFf....",
    "......fFFff.....",
    "...xxXxffxxvv...",
    "..xXXxxxxxxvvV..",
    ".xXxxzZzZzxvvVV.",
    "xXxxxxxxxxxvvVVV",
    "xxxxxxxxxxvvvVVV",
]
# Bruxa A, a velha do chapéu: a aba mole com musgo, o cabelo grisalho, um olho branco, a boca pequena, o xale
BRUXA_A = [
    "................",
    "......hhhh......",
    ".....hMmhhh.....",
    "....hMmmhhhh....",
    "..HhhhhhhhhhhhH.",
    ".HhhmmhhhhhhmhhH",
    "...qqPPPPppqq...",
    "..qqPcePPePpq...",
    "..qqPPPPPPppq...",
    "..q.PPPPPppqq...",
    "..q.pPPPpppq....",
    "..qq.ppEppqq....",
    "..hhhmmppmmhhh..",
    ".hhhhmmhhmmhhhh.",
    "hhhhhhhhhhhhhhhh",
    "HHhhhhhhhhhhhhHH",
]
# Bruxa B, encapuzada com o frasco: o sorriso torto e o frasco verde de rolha erguido na mão ("curas, maldições e às
# vezes as duas coisas no mesmo frasco")
BRUXA_B = [
    "................",
    ".....hhhhh......",
    "....hhmmhhh.....",
    "...hhmPPPhhh....",
    "...hmPPPPPhh....",
    "...hPePPePhh....",
    "...hPPPPPPhh....",
    "...hPPpEEphh....",
    "...hhpPPphhh.cc.",
    "..hhhhppphhh.Qq.",
    ".hhhhhhhhhhhgGGg",
    ".hhhhhhhhhhhGGGg",
    "hhhhhhhhhhhhgGgP",
    "hhhhhhhhhhhhhPPp",
    "hhhhhhhhhhhhhhhh",
    "HHhhhhhhhhhhhhHH",
]

# Par 3, os mortos-vivos: o carniçal e o espectro (hoje a "caveira" e o "etereo")
CORES3 = {
    # o carniçal: a pele lívida cinza-violácea (a luz, o meio, a sombra, a sombra funda), o olho doente, o sangue, os
    # dentes, a boca, o trapo
    "L": "a89a96", "l": "7a6c6c", "d": "4e4246", "D": "2e262a", "Y": "d0c060", "R": "8a1e1e", "T": "d8d0bc", "k": "120c0c", "t": "3a3226",
    # o espectro: a névoa fria (do claro ao escuro), o vazio, o olho pálido
    "C": "aeb6c4", "c": "7a8698", "s": "4c5468", "S": "343a4a", "V": "0c0e14", "E": "b8eef0",
}
# Carniçal A, de frente e curvado: o crânio sem pelo, os olhos fundos e doentes, a mandíbula comprida de dentes tortos
# com o sangue, os ombros magros
CARN_A = [
    "................",
    ".....dlllld.....",
    "....dlLLLlld....",
    "...dlLLLLllld...",
    "...lLdkLLkdld...",
    "...lLkYlLYkdd...",
    "...dLlllllldD...",
    "....dLlddlldD...",
    "....kRTkTTkk....",
    "....kTTkkTRk....",
    "....dlkkkkld....",
    ".....dllllD.....",
    "..ddD.dlld.Ddd..",
    ".dlLldDllDdlLld.",
    "dlLlldttttdllLld",
    "DlllddttttddlllD",
]
# Carniçal B, de perfil mordendo: a cabeça baixa e comprida, a boca aberta com os dentes e o sangue, o dorso curvado
CARN_B = [
    "................",
    "................",
    "......ddllld....",
    ".....dlLLLlld...",
    "....dlLLLLLlld..",
    "...dlLdkLLLlld..",
    "..dlLkYlLLlldD..",
    ".dLLlllLLllddD..",
    "kTkTkllLlldD....",
    "kRkkkRdlldD.....",
    ".kTkTkdldD......",
    "..kkkddlddlld...",
    "....DdlLdlLlLd..",
    "...DdlddlddlLld.",
    "..DdlLdlLdlLlld.",
    ".DDDDDDDDDDDDDD.",
]
# Espectro A, o capuz de névoa: o rosto vazio com um ponto de olho pálido, os farrapos se desfazendo embaixo
ESP_A = [
    "................",
    "......cccc......",
    ".....cCCCcs.....",
    "....cCcSSccs....",
    "...cCcSVVScss...",
    "...cCSVEVVScs...",
    "...cCSVVEVScs...",
    "...cCSVVVVScss..",
    "...cCcSVVScsss..",
    "..ccCccSScccss..",
    "..cCccccccccss..",
    ".cCcc.cccc.css..",
    ".cCc..cc.c..cs..",
    ".cc...c..c...s..",
    "..c...s..c...s..",
    "......s..s......",
]
# Espectro B, o grito: o rosto comprido, os olhos em fenda, a boca esticada do grito de terror, os braços em fiapos
ESP_B = [
    "................",
    ".......ccc......",
    "......cCCcs.....",
    ".....cCCCccs....",
    ".....cCVcVcs....",
    ".....cEVcVEs....",
    ".....cCcccsS....",
    "..s..cCVVcsS..s.",
    ".sc..cCVVcss.cs.",
    ".cs.scCVVcsSscs.",
    "..csscCVVcsssc..",
    "...scCcccssss...",
    "....sCcscsSs....",
    "....s.cs.sS.....",
    ".....s.s..s.....",
    "......s...s.....",
]

CAMADAS = {
    "sapo-a": (SAPO_A, ["corpo", "barriga", "olhos", "manchas"],
               lambda x, y, ch: "olhos" if ch in "Yk" else "manchas" if ch == "O" else "barriga" if ch in "cCM" else "corpo"),
    "sapo-b": (SAPO_B, ["corpo", "barriga", "olhos", "manchas"],
               lambda x, y, ch: "olhos" if ch in "Yk" else "manchas" if ch == "O" else "barriga" if ch in "cCM" else "corpo"),
    "sanguessuga-a": (SANG_A, ["agua", "corpo", "boca"],
                      lambda x, y, ch: "agua" if ch in "Aa" else "boca" if ch in "RPkr" and y <= 8 else "corpo"),
    "sanguessuga-b": (SANG_B, ["agua", "corpo", "boca"],
                      lambda x, y, ch: "agua" if ch in "Aa" else "boca" if ch in "RPk" and y <= 5 else "corpo"),
    "cultista-a": (CULT_A, ["manto", "rosto", "marca"],
                   lambda x, y, ch: "marca" if ch in "Zz" else "rosto" if ch in "FfE" else "manto"),
    "cultista-b": (CULT_B, ["manto", "rosto", "marca"],
                   lambda x, y, ch: "marca" if ch in "Zz" else "rosto" if ch in "FfEc" else "manto"),
    "bruxa-a": (BRUXA_A, ["xale", "cabelo", "rosto", "chapeu"],
                lambda x, y, ch: "chapeu" if y <= 5 else "cabelo" if ch in "qQ" else "rosto" if ch in "Ppce" else "xale"),
    "bruxa-b": (BRUXA_B, ["capuz", "rosto", "frasco"],
                lambda x, y, ch: "frasco" if ch in "GgcQq" or (x >= 12 and ch in "Pp") else "rosto" if ch in "Ppe" else "capuz"),
    "carnical-a": (CARN_A, ["corpo", "rosto", "boca"],
                   lambda x, y, ch: "boca" if ch in "RTk" else "rosto" if ch == "Y" or 1 <= y <= 11 else "corpo"),
    "carnical-b": (CARN_B, ["corpo", "rosto", "boca"],
                   lambda x, y, ch: "boca" if ch in "RTk" else "rosto" if ch == "Y" or y <= 10 else "corpo"),
    "espectro-a": (ESP_A, ["nevoa", "vazio"], lambda x, y, ch: "vazio" if ch in "VE" else "nevoa"),
    "espectro-b": (ESP_B, ["nevoa", "vazio"], lambda x, y, ch: "vazio" if ch in "VE" else "nevoa"),
}
# o mapa de cores de cada desenho (o par 1 usa CORES; os outros pares, o próprio)
PALETA = {"cultista-a": CORES2, "cultista-b": CORES2, "bruxa-a": CORES2, "bruxa-b": CORES2,
          **dict.fromkeys(("carnical-a", "carnical-b", "espectro-a", "espectro-b"), CORES3)}


def imagem(ident):
    im = Image.new("RGBA", (16, 16))
    for y, l in enumerate(CAMADAS[ident][0]):
        for x, ch in enumerate(l):
            if ch != ".":
                im.putpixel((x, y), tuple(int(PALETA.get(ident, CORES)[ch][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def gravar(base, ids=None):
    for ident in ids or CAMADAS:
        grade, ordem, camada = CAMADAS[ident]
        assert len(grade) == 16 and all(len(l) == 16 for l in grade), (ident, [len(l) for l in grade])
        (base / "grades").mkdir(parents=True, exist_ok=True)
        (base / f"grades/{ident}.txt").write_text(chr(10).join(grade) + chr(10), encoding="utf-8")
        listas = {c: [] for c in ordem}
        for y, l in enumerate(grade):
            for x, ch in enumerate(l):
                if ch != ".":
                    listas[camada(x, y, ch)].append(f"{x},{y},{PALETA.get(ident, CORES)[ch]}")
        d = base / f"listas/{ident}"
        d.mkdir(parents=True, exist_ok=True)
        for k, v in listas.items():
            (d / f"{k}.lua").write_text('return "' + ";".join(v) + '"' + chr(10), encoding="utf-8")
        (d / "ordem.txt").write_text(",".join(ordem) + chr(10), encoding="utf-8")
        print(ident, {k: len(v) for k, v in listas.items()})


if __name__ == "__main__":
    gravar(pathlib.Path(sys.argv[1]), sys.argv[2:])
