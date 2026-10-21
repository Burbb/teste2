"""Os 14 estados que faltavam (21/10/2026, lote da madrugada), em 16 px, o tamanho dos estados na luta (o chip da carta
e o selo do estado que chega). Firme (R2), Em guarda (G1) e Esquiva (E6) são a referência de acabamento: contorno de
1 px (#08080a), poucos tons por material, a luz de cima e da esquerda.

Grava grades/<id>.txt e as listas por camada para o pintar.lua (listas/<id>/<camada>.lua, com ordem.txt).
    python icones16.py <pasta do lote>
"""
import pathlib
import sys

CORES = {
    "#": "08080a",
    # ferro (a rampa dos estados finais)
    "3": "383c44", "4": "4c5159", "5": "646a73", "6": "848b94", "7": "b0b6bd", "8": "e4e8ec",
    # veneno
    "G": "1f4a25", "g": "3f7f2e", "h": "6db33f", "H": "a6e05a", "i": "e4f7b0",
    # sangue
    "R": "4a0a0c", "r": "8a1418", "s": "c42a2e", "S": "ec5a4c", "T": "ffc0b0",
    # fogo
    "F": "6e1a0a", "f": "b8380e", "o": "e86a1f", "O": "ffa64a", "y": "ffe08a", "Y": "fffbe0",
    # maldição
    "P": "1e0e2a", "p": "4a2266", "q": "7a4ab0", "Q": "b48ae8", "Z": "e6d6ff", "m": "ff5fd0",
    # ouro
    "C": "6b4a0e", "c": "b08418", "d": "e0b83a", "D": "f6d86a", "e": "fff6c8",
    # azul arcano
    "B": "1c2a6b", "b": "3d63c9", "u": "7fb0ff", "U": "d0e4ff", "v": "24356e",
    # couro e madeira
    "K": "b08c62", "L": "8e6236", "M": "6b4528", "N": "4a2e18",
    # sombra (o pano do capuz)
    "1": "28222f", "2": "3e3850", "9": "5e5672", "0": "8a80a0", "k": "050407",
    # osso (as presas) e o rosto da fúria
    "W": "f1e4c4", "w": "c0b8a8", "x": "8a8070", "n": "5a1c16", "X": "3a100c",
    # a bota da Agilidade (attr-agilidade-24.png), para a alternativa da Iniciativa
    "a": "eaaa62", "j": "cf8040", "l": "b0602c", "t": "8f4620", "z": "6e3317", "A": "4e2210",
    "E": "6e5442", "I": "4a3628", "J": "f0d070", "V": "c08a48",
}

def com_contorno(grade):
    """O contorno de 1 px (#) em volta do desenho, pelos lados (como o contornar de pixel_comum)."""
    g = [list(l) for l in grade]
    for y in range(16):
        for x in range(16):
            if grade[y][x] == "." and any(0 <= x + dx < 16 and 0 <= y + dy < 16 and grade[y + dy][x + dx] != "."
                                          for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                g[y][x] = "#"
    return ["".join(l) for l in g]


# --- lote 1
VENENO = com_contorno([
          "................",
          "........hhhg....",
          ".......hHHhgg...",
          "......hHkHhgg...",
          "..S.SShhhhgg....",
          "...S...hhgg.....",
          ".....hhhgg......",
          "...hhHhgg.......",
          "..hHhg..........",
          "..hhgg..........",
          "..ghhhhhgg......",
          "...gghhhhhggg...",
          "........ghhgg...",
          "......gghhgG....",
          "..GGgggggGG.....",
          "................"])
SANGRAMENTO = ["................",
               "..........#.....",
               ".........#S#....",
               "...#.....#S#....",
               "..#S#...#Sss#...",
               ".#Ssr#..#Sss#...",
               ".#Tsr#.#SSssr#..",
               ".#srR#.#STssr#..",
               "..###.#STsssrr#.",
               "......#STssssr#.",
               "......#STssssr#.",
               "......#Sssssrr#.",
               "......#ssssrrR#.",
               ".......#ssrRR#..",
               "........#####...",
               "................"]
# --- lote 2
CHAMAS = ["................",
          "........#.......",
          ".......#y#......",
          ".......#O#......",
          "......#OOo#..#..",
          "......#OyO#.#O#.",
          "..#..#OyYOo#OOf#",
          ".#O#.#OyYyOo#Of#",
          ".#Oo##OyYYyOoOf#",
          "#OooOOyYYYyOOof#",
          "#oOOyyYYYYyyOof#",
          "#foOyyYYYYyOoff#",
          "#ffoOyyyyyOoofF#",
          ".#ffooOOOOoofF#.",
          "..##FFffffFF##..",
          "....########...."]
MALDICAO = ["................",
            "....########....",
            "...#ZZQQQQqq#...",
            "..#ZQQQQQQQqq#..",
            ".#ZQQQQQQQQqqp#.",
            ".#QQQQQQQQQqqp#.",
            ".#QPPPQQqPPPpp#.",
            ".#QPmPQqqPmPpp#.",
            ".#qPPPqqqPPPpp#.",
            ".#qqqqqPPqqqpp#.",
            "..#qqqqPPqqpp#..",
            "...##qqqqqp##...",
            "....#ZpZpZp#....",
            "....#qPqPqP#....",
            ".....######.....",
            "................"]
# --- lote 3
ATORDOADO = ["................",
             "....########....",
             "...#DDDDDdddd#..",
             "..#De######ddc#.",
             ".#De#......#dc#.",
             ".#D#..####..#c#.",
             "#De#.#Dddd#.#c#.",
             "#D#.#D####.#cC#.",
             "#D#.#d#...#cC#..",
             "#D#.#dc###cC#...",
             "#dd#.#cccCC#....",
             ".#dc#.#####.....",
             ".#cc##..........",
             "..#cCC#####.....",
             "...##CCCCCC#....",
             ".....######....."]
ENFRAQUECIDO = com_contorno([
                "................",
                ".......dc.......",
                ".......LM.......",
                ".......LM.......",
                "...DDdddddcc....",
                "......786.......",
                "......786.......",
                "......786.......",
                "......7.5.......",
                "................",
                "..........67....",
                "..........765...",
                "...........65...",
                "............5...",
                "................",
                "................"])
# --- lote 4
MARCADO = [".....######.....",
           "...##SSSsss##...",
           "..#SS######sr#..",
           ".#S#..#SS#..#r#.",
           "#S#...#sr#...#r#",
           "#S#....##....#r#",
           "#S##..####..##r#",
           "#SSs#.#Ss#.#srr#",
           "#Ssr#.#sr#.#rrR#",
           "#S##..####..##R#",
           "#s#....##....#R#",
           "#s#...#sr#...#R#",
           ".#s#..#rR#..#R#.",
           "..#rr######rR#..",
           "...##rrrRRR##...",
           ".....######....."]
FURTIVO = ["................",
           ".......##.......",
           "......#00#......",
           ".....#0092#.....",
           "....#009922#....",
           "...#09####22#...",
           "...#0#kkkk#2#...",
           "..#09#kkkk#22#..",
           "..#09#UkkU#21#..",
           "..#09#kkkk#21#..",
           ".#0992####2221#.",
           ".#099222222221#.",
           "#09922222222211#",
           "#09222222222211#",
           ".##############.",
           "................"]
# --- lote 5
BARREIRA = com_contorno([
            "................",
            ".....UUUuuu.....",
            "...UUUuuuuubb...",
            "..UUu......bbb..",
            ".UUu..UU....bbB.",
            ".Uu..U.......bB.",
            ".Uu..U.......bB.",
            ".uu..........bB.",
            ".uu..........bB.",
            ".ub..........BB.",
            ".ub.........vBB.",
            ".ubb......vbBB..",
            "..bbb....bbBB...",
            "...bbbbbbBBB....",
            ".....bBBBB......",
            "................"])
PROVOCANDO = com_contorno([
              "................",
              "................",
              "................",
              "......7886......",
              ".....788865.....",
              ".....788665.....",
              "S....776655....S",
              "Ss....7655....sS",
              "Ssr..........rsS",
              "Ss..77766655..sS",
              "S..7776666555..S",
              "...7766666555...",
              "...7766665555...",
              "................",
              "................",
              "................"])
# --- lote 6
FORTALECIDO = com_contorno([
               "................",
               "......8.........",
               ".....786........",
               ".....786........",
               ".....786.....D..",
               ".....786....Ddc.",
               ".....786...Dddcc",
               ".....786........",
               ".....786.....D..",
               ".....786....Ddc.",
               "..DDdddddc.Dddcc",
               "......LM........",
               "......LM........",
               "......LM........",
               ".....Ddc........",
               "................"])
INICIATIVA = com_contorno([
              "................",
              ".......eD.......",
              ".......eD.......",
              "..d....Dd....c..",
              "...d...Dd...c...",
              ".......Dd.......",
              ".......Dc.......",
              ".dd....dc....cc.",
              ".......dc.......",
              ".......dC.......",
              "................",
              "................",
              ".......eD.......",
              ".......cC.......",
              "................",
              "................"])
# --- lote 7
FURIA = com_contorno([
               "................",
               "................",
               "...nnnnnnnnnn...",
               "..nRsnnnnnnsRn..",
               ".nnnRRsnnsRRnnn.",
               ".nnnnnRRRRnnnnn.",
               ".nnynnnnnnnnynn.",
               ".nnOyonnnnoyOnn.",
               ".nnnOOonnoOOnnn.",
               "..nnnnnnnnnnnn..",
               "..nnnnnnnnnnXn..",
               "...nnnXXXXnXX...",
               "....nnnnnXXX....",
               "......XXXX......",
               "................",
               "................"])
FRENESI = com_contorno([
           "................",
           "................",
           "..............s.",
           ".............Sr.",
           ".............Sr.",
           "............Sr..",
           ".........s..Sr..",
           "........Sr.Sr...",
           "....s...Sr.Sr...",
           "...Sr..Sr.Sr....",
           "...Sr..Sr.Sr....",
           "..s...s...s.....",
           "..s...s...s.....",
           "................",
           "................",
           "................"])

VENENO_PRESAS = com_contorno([
          "................",
          "..WWWWx..WWWWx..",
          "..WWWwx..WWWwx..",
          "..WWWwx..WWWwx..",
          "...WWwx...WWwx..",
          "...WWx....WWx...",
          "...Wwx....Wwx...",
          "....Wx.....Wx...",
          "....H......H....",
          "...HhH....HhH...",
          "...hgG...HhhgG..",
          "....G....hhggG..",
          ".........hgGGG..",
          "..........GGG...",
          "................",
          "................"])

ATORDOADO_ORBITA = com_contorno([
                    "................",
                    "................",
                    "...........e....",
                    "..........eDd...",
                    ".........eDDdd..",
                    "..........Ddc...",
                    "....ccccccdcdc..",
                    "..cc..........c.",
                    ".d.e..........d.",
                    ".deDd.........d.",
                    "eDDdd........d..",
                    ".Ddc.DDDDDDDd...",
                    ".d.c............",
                    "................",
                    "................",
                    "................"])

ENFRAQUECIDO_SETAS = com_contorno([
                "................",
                ".....dc.........",
                ".....LM.........",
                ".....LM.........",
                "..DDdddddc......",
                "....786.........",
                "....786....QQQq.",
                "....786.....Qq..",
                "....786......q..",
                "....786.........",
                "....786....QQQq.",
                "....786.....Qq..",
                "....786......q..",
                ".....8..........",
                "................",
                "................"])

ENFRAQUECIDO_SETA = com_contorno([
                "................",
                "....d...........",
                "....L......Qq...",
                "....L......Qq...",
                ".DDdddc....Qq...",
                "...786.....Qq...",
                "...786.....Qq...",
                "...786.....Qq...",
                "...786.....Qq...",
                "...786...QQQqqq.",
                "...786....QQqq..",
                "...786.....Qq...",
                "...786..........",
                "....8...........",
                "................",
                "................"])

FORTALECIDO_SETA = com_contorno([
               "................",
               "....8...........",
               "...786.....De...",
               "...786....DDdc..",
               "...786...DDDdcc.",
               "...786.....Dc...",
               "...786.....Dc...",
               "...786.....dc...",
               "...786.....dc...",
               "...786.....dc...",
               ".DDdddc....dC...",
               "....L......cC...",
               "....L...........",
               "....d...........",
               "................",
               "................"])

MARCADO_ALVO = com_contorno([
            "................",
            ".....SSSSSS.....",
            "...SSSSSSSSss...",
            "..SSSWWWWWWssr..",
            "..SSWWWWWWWWsr..",
            ".SSWWWSSSSwwwsr.",
            ".SSWWSSSSSswwsr.",
            ".SSWWSSWWsswwsr.",
            ".SsWWsswwsrwwrr.",
            ".SsWWssssrrwwrr.",
            ".sswwwssrrwwwrr.",
            "..sswwwwwwwwrr..",
            "..ssrwwwwwwrrR..",
            "...srrrrrrrrR...",
            ".....rrRRRR.....",
            "................"])

BARREIRA_CHEIA = com_contorno([
            "................",
            ".....UUUuuu.....",
            "...UUUuuuuubb...",
            "..UUuBBBBBBbbb..",
            ".UUuBBUUBBBBbbB.",
            ".UuBBUBBBBBBBbB.",
            ".UuBBUBBBBBBBbB.",
            ".uuBBBBBBBBBBbB.",
            ".uuBBBBBBBBBBbB.",
            ".ubBBBBBBBBBBBB.",
            ".ubBBBBBBBBBvBB.",
            ".ubbBBBBBBvbBB..",
            "..bbbBBBBbbBB...",
            "...bbbbbbBBB....",
            ".....bBBBB......",
            "................"])

PROVOCANDO_SETAS = com_contorno([
              ".S......S.....S.",
              "..S.....S....S..",
              "...S....S...S...",
              "...rSr.SSS.rSr..",
              "....rS..S..Sr...",
              ".....r.....r....",
              "......7886......",
              ".....788865.....",
              ".....788665.....",
              "......7665......",
              "......7655......",
              "...7776666555...",
              "..776666665555..",
              "..766666655555..",
              "..766666655555..",
              "................"])

BARREIRA_FIGURA = com_contorno([
            "................",
            ".....UUUuuu.....",
            "...UUUuuuuubb...",
            "..UUu......bbb..",
            ".UUu...78...bbB.",
            ".Uu...7886...bB.",
            ".Uu...7866...bB.",
            ".uu....65....bB.",
            ".uu..776655..bB.",
            ".ub.77666555.BB.",
            ".ub.76666555vBB.",
            ".ubb......vbBB..",
            "..bbb....bbBB...",
            "...bbbbbbBBB....",
            ".....bBBBB......",
            "................"])

INICIATIVA_BOTA = com_contorno([
              "................",
              "........jaal....",
              "........ljjtz...",
              "........lttzA...",
              "..VVV...ltzzA...",
              "........lttzA...",
              "...VVV..ltzzA...",
              "........JJJzA...",
              ".......lttttA...",
              "....VV.lttttzA..",
              "......llttttzzAA",
              "......ljtttzzzlj",
              "......EEEEtttzzj",
              ".......IIIEEEEEA",
              "..........IIIII.",
              "................"])

INICIATIVA_TACA = com_contorno([
              "................",
              "......eDDd......",
              "......eDdc......",
              "..d...DDdc...c..",
              "...d..Ddcc..c...",
              "......Ddcc......",
              ".......Dc.......",
              ".dd....dc....cc.",
              ".......dC.......",
              ".......cC.......",
              "................",
              ".......eD.......",
              "......eDdc......",
              ".......cC.......",
              "................",
              "................"])

FURIA_ROSTO = com_contorno([
               "................",
               ".....SSSSss.....",
               "...SSSssssssr...",
               "..SSssssssssrr..",
               ".SXXssssssssXXr.",
               ".SsXXXssssXXXrr.",
               ".SsssXXssXXsssr.",
               ".SssYYyssyYYssr.",
               ".SssyOOssOOyssr.",
               ".Sssssssssssrrr.",
               ".ssssXXXXXXssrr.",
               ".sssXssssssXrrR.",
               "..rsssssssrrrR..",
               "...rrrrrrrrRR...",
               ".....RRRRRR.....",
               "................"])

VENENO_GOTA = com_contorno([
          ".......h........",
          "......hHg.......",
          "......hHg.......",
          ".....hHhgg......",
          ".....hHhgg......",
          "....hHihhgg.....",
          "....hiGihgG.....",
          "...hhhihhggG....",
          "...hhhhhhggG....",
          "...ghhhhhgGG....",
          "....ghhhgGG.....",
          ".....GGGGG......",
          "..H..........h..",
          ".hHhhhhgggggggG.",
          "..gggGGGGGGGGG..",
          "................"])

CHAMAS_R2 = com_contorno([
          ".........O......",
          "........Oo......",
          "........Oo......",
          ".......OOo......",
          "...O..OyOof.....",
          "...Oo.OyOoo.....",
          "...oO.OyyOof.f..",
          "...oOOOyYyOofof.",
          "..foOOyYYyyOoof.",
          "..foOyYYYYyOoof.",
          "..foOyYYYYyOoff.",
          "..ffoOyYYyOooff.",
          "...ffoOyyOoofF..",
          "....FffooofFF...",
          "......FFFFF.....",
          "................"])

FORTALECIDO_R2 = com_contorno([
               "................",
               "....8...........",
               "...786.....Hi...",
               "...786....HHhg..",
               "...786...HHHhgg.",
               "...786.....Hg...",
               "...786.....Hg...",
               "...786.....hg...",
               "...786.....hg...",
               "...786.....hg...",
               ".DDdddcc...hG...",
               "....L......gG...",
               "....L...........",
               "....d...........",
               "................",
               "................"])

ENFRAQUECIDO_R2 = com_contorno([
                "................",
                "....d...........",
                "....L......Qq...",
                "....L......Qq...",
                ".DDdddcc...Qq...",
                "...786.....Qq...",
                "...786.....Qq...",
                "...786.....Qq...",
                "...786.....Qq...",
                "...786...QQQqqq.",
                "...786....QQqq..",
                "...786.....Qq...",
                "...786..........",
                "....8...........",
                "................",
                "................"])

BARREIRA_R2 = com_contorno([
            "................",
            ".....UUUuuu.....",
            "...UUUuuuuubb...",
            "..UUuvvvvvvbbb..",
            ".UUuvvv87vvvbbB.",
            ".UuvvvU76vvvvbB.",
            ".UuvvU8876vvvbB.",
            ".uuvvv8766vvvbB.",
            ".uuvvv7766vvvbB.",
            ".ubvvv7vv6vvvBB.",
            ".ubvvv7vv6vvvBB.",
            ".ubbvvvvvvvvbBB.",
            "..bbbvvvvvvbBB..",
            "...bbbbbbBBB....",
            ".....bBBBB......",
            "................"])

PROVOCANDO_R2 = com_contorno([
              ".......ss.......",
              ".s.....ss.....s.",
              "..s...SSss...s..",
              "...s.S.Ss.S.s...",
              "....SS....sS....",
              "...SSS....sSS...",
              "................",
              ".......87.......",
              ".......76.......",
              "....77788766....",
              "......8766......",
              "......7766......",
              "......7766......",
              "......7..6......",
              "......7..6......",
              "................"])

INICIATIVA_R2 = com_contorno([
              "................",
              ".............D..",
              "............DeD.",
              "...........8.D..",
              "..........876...",
              "....777..876....",
              ".........76.....",
              "..7777..876.....",
              ".......876......",
              "...777876.......",
              ".....dd6........",
              "....d.Ld........",
              ".....L..........",
              "....d...........",
              "................",
              "................"])

FRENESI_R2 = com_contorno([
           "................",
           ".......yy.......",
           "......yYYy......",
           ".....Oy..yO.....",
           "....OO....OO....",
           "...OO......OO...",
           ".......oo.......",
           "......oOOo......",
           ".....oo..oo.....",
           "....oo....oo....",
           "................",
           ".......ff.......",
           "......foof......",
           ".....ff..ff.....",
           "................",
           "................"])

# as camadas de cada desenho, de baixo para cima, pela letra
def _por(mapa, resto):
    return lambda ch: "contorno" if ch == "#" else next((k for k, v in mapa.items() if ch in v), resto)


ICONES = {
    "estado-veneno": (VENENO, ["corpo", "olho", "lingua", "contorno"],
                      lambda x, y, ch: "contorno" if ch == "#" else "olho" if ch == "k" else "lingua" if ch == "S"
                      else "corpo"),
    "estado-sangramento": (SANGRAMENTO, ["gotas", "contorno"], lambda x, y, ch: "contorno" if ch == "#" else "gotas"),
    "estado-queimadura": (CHAMAS, ["chamas", "miolo", "contorno"],
                          lambda x, y, ch: "contorno" if ch == "#" else "miolo" if ch in "yY" else "chamas"),
    "estado-maldito": (MALDICAO, ["cranio", "olhos", "contorno"],
                       lambda x, y, ch: "contorno" if ch == "#" else "olhos" if ch == "m" else "cranio"),
    "estado-atordoado": (ATORDOADO, ["espiral", "contorno"], lambda x, y, ch: "contorno" if ch == "#" else "espiral"),
    "estado-enfraquecido": (ENFRAQUECIDO_SETA, ["espada", "seta", "contorno"],
                            lambda x, y, ch: "contorno" if ch == "#" else "seta" if ch in "Qq" else "espada"),
    "estado-enfraquecido-setinhas": (ENFRAQUECIDO_SETAS, ["espada", "setas", "contorno"],
                                     lambda x, y, ch: "contorno" if ch == "#" else "setas" if ch in "Qq" else "espada"),
    "estado-marcado": (MARCADO_ALVO, ["aneis", "contorno"], lambda x, y, ch: "contorno" if ch == "#" else "aneis"),
    "estado-marcado-mira": (MARCADO, ["mira", "contorno"], lambda x, y, ch: "contorno" if ch == "#" else "mira"),
    "estado-furtivo": (FURTIVO, ["capuz", "rosto", "olhos", "contorno"],
                       lambda x, y, ch: "contorno" if ch == "#" else "olhos" if ch == "U" else "rosto" if ch == "k" else "capuz"),
    "estado-barreira": (BARREIRA_FIGURA, ["bolha", "figura", "contorno"],
                        lambda x, y, ch: "contorno" if ch == "#" else "figura" if ch in "5678" else "bolha"),
    "estado-barreira-anel": (BARREIRA, ["bolha", "reflexo", "contorno"],
                             lambda x, y, ch: "contorno" if ch == "#" else "reflexo" if 4 <= y <= 6 and 4 <= x <= 7 else "bolha"),
    "estado-provocando": (PROVOCANDO_SETAS, ["figura", "setas", "contorno"],
                          lambda x, y, ch: "contorno" if ch == "#" else "setas" if ch in "SsrR" else "figura"),
    "estado-provocando-lados": (PROVOCANDO, ["figura", "setas", "contorno"],
                                lambda x, y, ch: "contorno" if ch == "#" else "setas" if ch in "SsrR" else "figura"),
    "estado-fortalecido": (FORTALECIDO_SETA, ["espada", "seta", "contorno"],
                           lambda x, y, ch: "contorno" if ch == "#" else "seta" if x >= 9 else "espada"),
    "estado-fortalecido-setinhas": (FORTALECIDO, ["espada", "setas", "contorno"],
                                    lambda x, y, ch: "contorno" if ch == "#" else "setas" if x >= 11 and y <= 10
                                    else "espada"),
    "estado-iniciativa": (INICIATIVA, ["exclamacao", "raios", "contorno"],
                          lambda x, y, ch: "contorno" if ch == "#" else "exclamacao" if 6 <= x <= 9 else "raios"),
    "estado-furia": (FURIA_ROSTO, ["rosto", "sobrancelhas", "olhos", "contorno"],
                     lambda x, y, ch: "contorno" if ch == "#" else "olhos" if ch in "YyOo" else "sobrancelhas" if ch == "X"
                     else "rosto"),
    "estado-furia-escuro": (FURIA, ["rosto", "sobrancelhas", "olhos", "contorno"],
                     lambda x, y, ch: "contorno" if ch == "#" else "olhos" if ch in "yOo" else "sobrancelhas" if ch in "Rs"
                     else "rosto"),
    "estado-atordoado-orbita": (ATORDOADO_ORBITA, ["orbita", "estrelas", "contorno"],
                                lambda x, y, ch: "contorno" if ch == "#" else "estrelas" if ch in "eD" or y <= 5
                                or (y >= 8 and x <= 5) else "orbita"),
    "estado-enfraquecido-partida": (ENFRAQUECIDO, ["lamina", "ponta", "punho", "contorno"],
                                    lambda x, y, ch: "contorno" if ch == "#" else "punho" if ch not in "345678"
                                    else "ponta" if y >= 10 else "lamina"),
    "estado-barreira-cheia": (BARREIRA_CHEIA, ["bolha", "reflexo", "contorno"],
                              lambda x, y, ch: "contorno" if ch == "#" else "reflexo" if 4 <= y <= 6 and 4 <= x <= 7 and ch == "U"
                              else "bolha"),
    "estado-iniciativa-bota": (INICIATIVA_BOTA, ["bota", "fivela", "rastro", "contorno"],
                               lambda x, y, ch: "contorno" if ch == "#" else "rastro" if ch == "V" else "fivela" if ch == "J"
                               else "bota"),
    "estado-iniciativa-taca": (INICIATIVA_TACA, ["exclamacao", "raios", "contorno"],
                               lambda x, y, ch: "contorno" if ch == "#" else "exclamacao" if 6 <= x <= 9 else "raios"),
    # a segunda rodada (21/10/2026, depois da avaliação do Jean): as alternativas novas, com as anteriores preservadas
    "estado-veneno-gota": (VENENO_GOTA, ["poca", "gota", "contorno"],
                           lambda x, y, ch: "contorno" if ch == "#" else "poca" if y >= 12 else "gota"),
    "estado-queimadura-r2": (CHAMAS_R2, ["chama", "miolo", "contorno"],
                             lambda x, y, ch: "contorno" if ch == "#" else "miolo" if ch in "yY" else "chama"),
    "estado-fortalecido-r2": (FORTALECIDO_R2, ["espada", "seta", "contorno"],
                              lambda x, y, ch: "contorno" if ch == "#" else "seta" if x >= 9 else "espada"),
    "estado-enfraquecido-r2": (ENFRAQUECIDO_R2, ["espada", "seta", "contorno"],
                               lambda x, y, ch: "contorno" if ch == "#" else "seta" if ch in "Qq" else "espada"),
    "estado-barreira-r2": (BARREIRA_R2, ["bolha", "figura", "contorno"],
                           lambda x, y, ch: "contorno" if ch == "#" else "figura" if ch in "5678" and 6 <= x <= 9 else "bolha"),
    "estado-provocando-r2": (PROVOCANDO_R2, ["figura", "setas", "contorno"],
                             lambda x, y, ch: "contorno" if ch == "#" else "setas" if ch in "SsrR" else "figura"),
    "estado-iniciativa-r2": (INICIATIVA_R2, ["espada", "brilho", "rastro", "contorno"],
                             lambda x, y, ch: "contorno" if ch == "#" else "brilho" if ch in "De" and y <= 3
                             else "rastro" if ch == "7" and x <= 6 and y in (5, 7, 9) and not (y == 9 and x >= 6)
                             else "espada"),
    "estado-frenesi-r2": (FRENESI_R2, ["divisas", "contorno"], lambda x, y, ch: "contorno" if ch == "#" else "divisas"),
    # tentativas guardadas (fora da proposta principal)
    "estado-veneno-presas": (VENENO_PRESAS, ["presas", "veneno", "contorno"],
                             lambda x, y, ch: "contorno" if ch == "#" else "presas" if ch in "Wwx" else "veneno"),
    "estado-frenesi": (FRENESI, ["garras", "contorno"], lambda x, y, ch: "contorno" if ch == "#" else "garras"),
}
# o estado do motor de cada desenho (as alternativas têm sufixo: estado-<id>-<rodada>)
ESTADO_DE = {k: k.split("-")[1] for k in ICONES}


def gravar(base, ids=None):
    for ident in ids or ICONES:
        grade, ordem, camada = ICONES[ident]
        assert len(grade) == 16 and all(len(l) == 16 for l in grade), (ident, [len(l) for l in grade])
        (base / "grades").mkdir(exist_ok=True)
        (base / f"grades/{ident}.txt").write_text("\n".join(grade) + "\n", encoding="utf-8")
        listas = {c: [] for c in ordem}
        for y, l in enumerate(grade):
            for x, ch in enumerate(l):
                if ch != ".":
                    listas[camada(x, y, ch)].append(f"{x},{y},{CORES[ch]}")
        d = base / f"listas/{ident}"
        d.mkdir(parents=True, exist_ok=True)
        for k, v in listas.items():
            (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
        (d / "ordem.txt").write_text(",".join(ordem) + "\n", encoding="utf-8")
        print(ident, {k: len(v) for k, v in listas.items()})


if __name__ == "__main__":
    gravar(pathlib.Path(sys.argv[1]), sys.argv[2:])
