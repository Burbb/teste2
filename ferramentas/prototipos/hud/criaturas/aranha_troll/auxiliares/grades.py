"""O par da 1E.3 depois dos animais (21/10/2026, pedido do Jean): a Aranha Gigante e o Troll, duas propostas de cada,
cabeças de 16×16 no formato dos retratos de carta aprovados (sem contorno preto, cores agrupadas, a luz da esquerda). O
jogo mostra a 2× na carta da luta e no rastro dos contratos (32 px) e a 3× no Bestiário, no mural e na faixa do mestre
caçador (48 px); não há desenho nativo de 32 nem de 48.

  - Aranha gigante (`aranha`, fera do Bosque: "tecem armadilhas entre as árvores; seu veneno paralisa antes de matar"):
    marrom-escura e peluda, os olhos pretos com um brilho frio (sem nada de mágico), as quelíceras com as presas de
    ponta avermelhada. A, de frente e de perto: o abdome atrás da cabeça com a marca clara, a carapaça, os olhos em
    fileira, as quelíceras e as presas, os palpos e as patas em arco dos dois lados. B, de lado, em ameaça: a cabeça
    à esquerda com os olhos e as presas, as patas da frente erguidas, o abdome grande atrás com a marca em cruz, as
    outras patas descendo até a base.
  - Troll da montanha (`troll`, gigante: "regeneram quase tudo, menos o fogo"; lento, muito forte, da montanha): a pele
    cinza-esverdeada de pedra, o musgo crescendo nele, os olhos pequenos e amarelos no fundo das órbitas. A, de frente:
    a cabeça enorme que enche o quadro, a testa baixa com a sombra das sobrancelhas, o nariz grande, a boca fechada e
    caída com as presas de baixo, o musgo no alto e nos ombros. B, de perfil para a esquerda: a cabeça baixa e pequena
    na frente de uma corcunda de musgo e pedra, o nariz comprido, a sobrancelha pesada, o queixo projetado com a presa.

    python grades.py <pasta do par> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

CORES = {
    # a aranha: o corpo do escuro ao claro, a marca, o olho e o brilho frio, as presas
    "k": "1e1813", "K": "3a2e24", "M": "5c4a38", "L": "7e664c", "H": "a68a64", "a": "b09a5a", "E": "060505", "x": "8a8a84", "F": "d2c09a", "f": "7a3a24",
    # o troll: a pele de pedra, a luz do nariz, as sombras, o musgo, os olhos, a boca, as presas
    "G": "8a8f80", "J": "a6ac98", "g": "6a7062", "d": "4c5248", "D": "30342e", "O": "5e6a3e", "o": "3e4a2c", "y": "c0a040", "e": "0e0c0a", "m": "2a1a14", "T": "d8d0b4",
    # a segunda rodada, das referências geradas: a aranha (o corpo marrom-acinzentado, as juntas claras, os olhos
    # âmbar, as quelíceras cinza e as presas claras) e o troll de carne (o verde, a sombra, os olhos pálidos, as presas,
    # a roupa de couro)
    "Q": "17120f", "R": "3a2f28", "S": "5e4c40", "U": "86705e", "V": "b8a48e", "P": "e08a34", "C": "7a746c", "c": "3e3a36", "X": "d8d0c0", "Y": "5a544c", "A": "6e8a4c", "I": "88a262", "i": "52683a", "N": "34482a", "Z": "1e2a18", "W": "c8b884", "B": "ecdcb4", "b": "b8a47e", "h": "6a4a30", "j": "46301e",
    # a terceira rodada: o ferro do elmo amassado da coroa do Rei Troll (a luz, o meio, a sombra, a ferrugem) e o âmbar
    # mais escuro dos olhos de lado da aranha
    "l": "a2a6aa", "p": "686c72", "q": "383c40", "r": "8a4a2c", "u": "b06a28",
    # a coroa dourada do Rei Troll (a quarta rodada): o ouro velho na luz, no meio, na sombra e no escuro do contorno
    "s": "f0c858", "t": "c8962e", "v": "8a6020", "w": "4e3414",
}

ARANHA_A = [
    "................",
    ".....kKKKKk.....",
    "....kKaKKaKk....",
    ".HM.kKKaaKKk.MH.",
    "M..MLHLLLLHLM..M",
    "M.HMEMLLLLMEMH.M",
    "MM.MLxEMMxELM.MM",
    "M.MMLEEKKEELMM.M",
    "M.M.MHKKKHKM.M.M",
    ".M.M.KHkkHK.M.M.",
    ".M.M.FK..KF.M.M.",
    ".M...f....f...M.",
    ".M............M.",
    "................",
    "................",
    "................",
]
ARANHA_B = [
    "...H............",
    "..M.H...kKKKk...",
    "..M.M..kKKaKKk..",
    ".M..M.kKKaaaKKk.",
    ".M.M..kKKKaKKKKk",
    "..M.MLkKKaaaKKKk",
    "...MLHLHkKaKKKKk",
    "..MLExELKkKKKKKk",
    ".MHLLLLLMKKKKKk.",
    "FMKKKKKKMkKKKk..",
    "f.M.M.M.KkkkK...",
    ".M..M.M..M..M...",
    "M..M..M...M..M..",
    "M..M...M..M...M.",
    "..M....M...M..M.",
    "..M.....M..M....",
]
TROLL_A = [
    "................",
    "...OoO...OOo....",
    "..OGGGGGGGGgo...",
    ".oGGGGGGGGGggd..",
    ".GGdDDGGGDDdgdd.",
    ".GGDyeDGGDeyDdd.",
    ".GGGddJJGGddgdD.",
    ".oGGGGJGGggggdD.",
    "..GGGdGGdgggdgD.",
    "..dGGTmmmTgddD..",
    "..dGmGGGGGmgdD..",
    "...dGGGGGggddD..",
    "...ddGGGggddD...",
    ".OoodddddddDDooO",
    "OoOOoodddDDoOoOO",
    "OOoOOOoooooOOoOO",
]
TROLL_B = [
    "................",
    "................",
    "......OoO.......",
    "....oGGGGo...OO.",
    "...GGGGGGgd.OoOo",
    "..dDDGGGggdOoOOo",
    ".GDyeDGgggdOOoOo",
    "GJJGGGGgggdOoOoO",
    "GJGGdGGggdOOoOOO",
    ".dGGTGGgddOoOOoO",
    ".dmmmGGgddOoOoOo",
    "..dGGGgdddDoOOoO",
    "...dddddDDoOOoOO",
    ".OoOooDDDoOoOOoO",
    "OoOOoOoOoOOoOoOO",
    "OOoOOoOOOoOOoOOO",
]

# A segunda rodada (21/10/2026, pedido do Jean; as propostas A e B ficam como histórico): três de cada, pelas duas
# referências geradas na conversa (ferramentas/arte/referencias/icones/: "Retrato pixelado da aranha sombria-1.png" e
# "Retrato pixelado de troll montanhês-2.png"), redesenhadas à mão na grade de 16 com a referência reduzida como guia
# oculta (guias/). A aranha: 1, a transposição de frente (as patas grossas e articuladas dos dois lados, os olhos âmbar
# em duas fileiras, as quelíceras cinza e as presas claras separadas); 2, o rosto de perto (os olhos e as quelíceras
# grandes, as presas compridas, só a ponta das patas nos cantos); 3, as patas da frente erguidas em arco por cima da
# cabeça. O troll de carne: 1, a transposição em três quartos (a orelha, a testa baixa, o olho pálido na sombra, o
# nariz largo, a mandíbula pesada com as duas presas, o pescoço grosso, a roupa de couro); 2, de frente (a cabeça
# estreita em cima e a mandíbula larga embaixo, a boca caída, as presas subindo por cima do lábio); 3, de perfil para
# a esquerda (a testa saliente, o nariz, a boca inclinada, o queixo projetado com a presa, a nuca e o pescoço grosso).
ARANHA_1 = [
    "................",
    "..VS........SV..",
    ".VSSQ.RSSR.QSSV.",
    ".SSQ.RSUUSR.QSS.",
    "VSQ.RSSSSSSR.QSV",
    "SSQ.RUSSSSUR.QSS",
    "SQ.VRSPSSPSRV.QS",
    "SQ.SRPSPPSPRS.QS",
    "Q.VSQRCCQCCRQSV.",
    ".VSQ.CCXQXCC.QSV",
    ".SSQ.cCXQXCc.QSS",
    "VSQ..cXQ.QXc..QS",
    "SSQ...Y...Y...QS",
    "SQ............QS",
    "Q..............Q",
    "................",
]
ARANHA_2 = [
    ".V............V.",
    ".SQ..RSSSSR..QS.",
    "VSQ.RSUUUUSR.QSV",
    "SQ.RSUSSSSUSR.QS",
    "SQ.RSPQSSPQSR.QS",
    "Q.RSPQPSSPQPSR.Q",
    ".VRSSSSSSSSSSRV.",
    "VSQRCCCQQCCCRQSV",
    "SQQCCXCQQCXCCQQS",
    "SQ.cCXCQ.CXCc.QS",
    "Q..cCXc...XCc..Q",
    "...ccXc...XCc...",
    "....cY.....Yc...",
    ".....Y.....Y....",
    "................",
    "................",
]
ARANHA_3 = [
    "..VSQ......QSV..",
    ".VSSQ......QSSV.",
    ".SSQ..V..V..QSS.",
    "VSQ..VSQQSV..QSV",
    "SSQ.VSQ..QSV.QSS",
    "SQ..SSRSSRSS..QS",
    "SQ..QRSUUSRQ..QS",
    "Q...RSPSSPSR...Q",
    "....RPSPPSPR....",
    "...VRCCQQCCRV...",
    "..VSQCXQ.QXCQSV.",
    "..SSQcX...XcQSS.",
    ".VSQ..Y...Y..QSV",
    ".SSQ.........QSS",
    "VSQ...........QS",
    "SQ.............Q",
]
TROLL_1 = [
    "................",
    "......NAAAAN....",
    ".....NAIIIAAN...",
    "....NAAAAAAAAN..",
    "..NNAZZZAAZZZAN.",
    ".NAiAZWZAAAZWZN.",
    ".NAiNAAAAiIIAiN.",
    ".NAiAAAAAiIIIiN.",
    "..NAAiBAAiZNZiN.",
    "..NAiBiZZZZZBiN.",
    "..NiABbZAAAZBbN.",
    "..NiiAAAAAAAAiN.",
    ".NNiiAAAAAAAiiN.",
    "hjNNiiiiiiiiiiN.",
    "hhjjNNNNNNNNNNjh",
    "hhhhjjjjjjjjjjhh",
]
TROLL_2 = [
    "................",
    "......NAAAN.....",
    ".....NAIIAAN....",
    "....NAAAAAAAN...",
    "...NZZZAAAZZZN..",
    "...NZWZAAAZWZN..",
    "..NAAAiIIiAAAiN.",
    "..NAAiIIIIiAAiN.",
    ".NAAAiZNNZiAAAiN",
    ".NABAAAAAAAABAiN",
    "NAiBiZZZZZZiBiiN",
    "NAiBbZAAAAZbBiiN",
    "NAiAAAAAAAAAAiiN",
    ".NiiiiiiiiiiiiN.",
    "hjjNNNNNNNNNNjjh",
    "hhhjjjjjjjjjjjhh",
]
TROLL_3 = [
    "................",
    "................",
    ".......NNNNN....",
    ".....NAAIIAAN...",
    "....NAIIAAAAiN..",
    "..NZZZZAAAAiiN..",
    "..NZWZAAANiiiiN.",
    ".NIIAAAAANiAiiN.",
    "NIIIAiAAAANiiiiN",
    "NAiZNAAAAiiiiiN.",
    ".NAAAZZZAiiiiiN.",
    ".NBAAAAZZiiiiN..",
    "NBBbAAAAAiiiNhj.",
    ".NAAAAAiiiNNhhhj",
    "..NNNiiiiNNhhhjj",
    "...hhhhhjjhhhjjj",
]

# A terceira rodada (21/10/2026, pedido do Jean; só no protótipo). O Rei Troll (o guardião `rei_troll`: "um troll
# colossal usa uma coroa feita de um elmo amassado", fases com a rocha arrancada do chão) a partir do Troll 2, de frente,
# da mesma espécie que o Troll comum: a cabeça desce para caber a "coroa", que é sucata achada por aí (pedido do Jean, que
# recusou a coroa de pontas): um elmo velho amassado, enferrujado e torto, pequeno para a cabeça, com um osso espetado de
# um lado e um prego do outro; a mandíbula larga com as presas, a da direita quebrada (o sinal de
# idade); a cicatriz clara cortando a sobrancelha e a bochecha do lado esquerdo; a testa baixa e o olhar sob a sombra. A
# Aranha 2B: a Aranha 2 reconstruída onde ela falhava (as presas claras e retas pareciam dentes de morsa e os olhos um
# par só): as quelíceras na cor do corpo, volumosas, com a luz no alto e a costura escura entre elas; as presas escuras,
# curtas, curvadas para dentro, com a pontinha clara; os olhos pequenos e separados (dois de frente e quatro de lado, os
# de lado num âmbar mais escuro); as patas ligadas aos lados da carapaça.
REI_TROLL = [
    "....B......l....",
    "....BqplplpN....",
    "...NBpprrppqN...",
    "..NAqplpprqqAN..",
    "..NZZbZAAZZZZN..",
    ".NZWZZbAAZZWZN..",
    ".NAAbAiIIiAAAiN.",
    ".NAAAiIIIIiAAiN.",
    "NAAAiZNNZiAAAAiN",
    "NABAAAAAAAAAAAiN",
    "AiBiZZZZZZiZBiiN",
    "AiBbZAAAAZbBiiiN",
    "AiAAAAAAAAAAAiiN",
    ".NiiiiiiiiiiiiN.",
    "hjjNNNNNNNNNNjjh",
    "hhhjjjjjjjjjjjhh",
]
ARANHA_2B = [
    "..V..........V..",
    ".VSQ........QSV.",
    ".SQR.RSSSSR.RQS.",
    "VSQRSUUUUUUSRQSV",
    "SQ.RSUSPSPSUSR.Q",
    "SQRSuQPQQPQuSRQS",
    "Q.RSSSSSSSSSSR.Q",
    ".VRSUSSRRSUSSRV.",
    "VSQSVUSRRSVUSQSV",
    "SQ.SUSSRRSUSS.QS",
    "SQ..SSRRRRSS..QS",
    "Q...RYS..SYR...Q",
    ".....XY..YX.....",
    "................",
    "................",
    "................",
]

# A quarta rodada do Rei Troll (21/10/2026, pedido do Jean, pela imagem gerada que ele mandou na conversa): só a coroa
# muda, e a base volta a ser o Troll 2 de frente, sem nenhum pixel do rosto mexido (as linhas 4 a 15 são as do TROLL_2):
# um aro grosso de ouro velho em duas linhas, mais largo que o alto da cabeça, e três pontas robustas e desiguais, a do
# meio mais alta e as dos lados tortas para fora; a luz da esquerda, a sombra embaixo e nas pontas, sem joias. A coroa
# cobre só o alto do crânio (as linhas 0 a 3), numa camada própria por cima.
COROA_OURO = [
    ".......st.......",
    "..st..wstv...st.",
    ".wsttwsstttvwstv",
    "..wstttttttttvw.",
]
REI_TROLL_OURO = [
    "".join(c if c != "." else t for c, t in zip(linha, TROLL_2[y])) if y < len(COROA_OURO) else TROLL_2[y]
    for y, linha in enumerate(COROA_OURO + [""] * (16 - len(COROA_OURO)))
]


def _aranha(patas):
    return lambda x, y, ch: "olhos" if ch in "Ex" else "presas" if ch in "Ff" else "patas" if patas(x, y) else "corpo"


TROLL = lambda x, y, ch: "musgo" if ch in "Oo" else "rosto" if ch in "yemT" else "pele"
CAMADAS = {
    "aranha-a": (ARANHA_A, ["patas", "corpo", "presas", "olhos"], _aranha(lambda x, y: x <= 3 or x >= 12)),
    "aranha-b": (ARANHA_B, ["patas", "corpo", "presas", "olhos"],
                 _aranha(lambda x, y: (y <= 6 and x <= 5) or (y >= 10 and not (y == 10 and 8 <= x <= 12)))),
    "troll-a": (TROLL_A, ["musgo", "pele", "rosto"], TROLL),
    "troll-b": (TROLL_B, ["musgo", "pele", "rosto"], TROLL),
}
# a segunda rodada: as patas (as partes do corpo nas bordas), o corpo, os olhos, as quelíceras e as presas; o troll em
# pele, rosto, presas e roupa
_ARANHA2 = lambda borda: lambda x, y, ch: ("olhos" if ch == "P" else "queliceras" if ch in "Cc" else "presas" if ch in "XY"
                                          else "patas" if borda(x, y) else "corpo")
_TROLL2 = lambda x, y, ch: "rosto" if ch == "W" else "presas" if ch in "Bb" else "roupa" if ch in "hj" else "pele"
CAMADAS["aranha-1"] = (ARANHA_1, ["patas", "corpo", "queliceras", "presas", "olhos"], _ARANHA2(lambda x, y: x <= 3 or x >= 12))
CAMADAS["aranha-2"] = (ARANHA_2, ["patas", "corpo", "queliceras", "presas", "olhos"], _ARANHA2(lambda x, y: x <= 2 or x >= 13))
CAMADAS["aranha-3"] = (ARANHA_3, ["patas", "corpo", "queliceras", "presas", "olhos"],
                       _ARANHA2(lambda x, y: x <= 3 or x >= 12 or (y <= 5 and not 6 <= x <= 9)))
# a terceira rodada: o Rei Troll com a coroa numa camada própria; a Aranha 2B com as camadas da 2
_REI = lambda x, y, ch: "coroa" if ch in "lpqr" or (ch == "B" and y <= 3) else "rosto" if ch == "b" and y <= 7 else _TROLL2(x, y, ch)  # a cicatriz
CAMADAS["rei-troll"] = (REI_TROLL, ["roupa", "pele", "presas", "rosto", "coroa"], _REI)
CAMADAS["rei-troll-ouro"] = (REI_TROLL_OURO, ["roupa", "pele", "presas", "rosto", "coroa"],
                             lambda x, y, ch: "coroa" if ch in "stvw" else _TROLL2(x, y, ch))
CAMADAS["aranha-2b"] = (ARANHA_2B, ["patas", "corpo", "queliceras", "presas", "olhos"],
                        lambda x, y, ch: "olhos" if ch in "Pu" else "presas" if ch in "XY" else
                        "queliceras" if 7 <= y <= 11 and 3 <= x <= 12 and ch in "SUVR" else "patas" if x <= 2 or x >= 13 else "corpo")
for _i, _g in (("1", TROLL_1), ("2", TROLL_2), ("3", TROLL_3)):
    CAMADAS[f"troll-{_i}"] = (_g, ["roupa", "pele", "presas", "rosto"], _TROLL2)


def gravar(base, ids=None):
    for ident in ids or CAMADAS:
        grade, ordem, camada = CAMADAS[ident]
        assert len(grade) == 16 and all(len(l) == 16 for l in grade), (ident, [len(l) for l in grade])
        (base / "grades").mkdir(parents=True, exist_ok=True)
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
