"""O segundo par das criaturas (21/10/2026, pedido do Jean): o Lobo e o Bandido, duas propostas de cada, cabeças de 16×16
no formato dos retratos de carta aprovados (retratos.js: MOREL_FIGURA, ODETE_CARTA): sem contorno preto (a caixa da
carta é escura), cores agrupadas, a luz da esquerda. O jogo mostra a 2× na carta da luta e no rastro dos contratos
(32 px) e a 3× no Bestiário, no mural e na faixa do mestre caçador (48 px); não há desenho nativo de 32 nem de 48.

  - Lobo (`lobo`, fera do Bosque e da Planície: "caçam em matilha; durante a luta, seu uivo fortalece o grupo"): um
    lobo cinzento comum, sem nada de sobrenatural (o `fera` de hoje tem olhos vermelhos). A, de frente: as orelhas
    altas, a testa larga, o focinho claro que afina para o nariz, as bochechas e a pelagem do pescoço até a base.
    B, de perfil para a esquerda: o focinho comprido com o nariz na ponta, a mandíbula clara, a orelha em pé, o
    pescoço e o peito em pelagem até a base.
  - Bandido (`bandido`: "desertores, camponeses arruinados e gente pior; gostam mais do seu ouro do que de lutar"). A,
    o desertor: a cabeça raspada com o cabelo curto no alto, a barba por fazer, as sobrancelhas carregadas, o nariz
    claro, o lenço vermelho do sprite de hoje no pescoço, o gibão de couro. B, a salteadora: o capuz de pano pardo, a
    franja escura, o rosto à luz, a trança caindo no ombro.
  Na escala da comitiva: a cabeça humana de 6 a 7 px sobre os ombros, como o Morel e a Odette.

    python grades.py <pasta do par> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

CORES = {
    # o lobo: a pelagem cinza do claro ao escuro, o focinho e o peito claros, o nariz e a pupila, o olho âmbar natural,
    # o fundo da orelha e a boca
    "L": "9a948a", "l": "78736a", "d": "57534c", "D": "3a3731", "C": "c8bfae", "k": "17140f", "a": "a07a3a",
    "n": "4a3a34", "m": "3a1e18",
    # o bandido: a pele (as cores do Morel), a barba por fazer, o cabelo, o lenço, o couro, o capuz e a trança
    "P": "c09070", "x": "d8aa90", "p": "9a6c52", "o": "6c4a38", "e": "20160f", "s": "7e5e48",
    "H": "4a3424", "h": "2e2018", "R": "8a3428", "r": "5e241c", "T": "6a4a30", "t": "4a3220", "u": "2a1c14",
    "K": "6a5a40", "J": "4e4230", "j": "342c20", "B": "7a5a34",
    # a segunda rodada: os dentes, o chapéu e o casaco, o capuz cinza, a lâmina da faca
    "W": "d8d0b8", "Q": "4e3e2c", "q": "2e241a", "G": "55554b", "g": "3a3a33", "c": "26261f", "M": "b8bcc4", "N": "7a7e88",
}

LOBO_A = [
    "...D........D...",
    "..Dld......dlD..",
    "..LnlD....DnlD..",
    "..LnldDddDdnld..",
    "..LLllllllllld..",
    ".dLLlllllllllDD.",
    ".dLLakllllkaldD.",
    ".dLLLllCClllldD.",
    ".dLLlCCCCCClldD.",
    "..dLlCCCCCCldD..",
    "..dLLCCkkCCldD..",
    "...dLlCCCCldD...",
    "..ddLllCClldDd..",
    ".ddLLlllllldDDd.",
    "dLLLlllllldddDDd",
    "LLLlllllldddDDDd",
]
LOBO_B = [
    "................",
    ".........Dd.....",
    "........Dlld....",
    ".......LLlldD...",
    "......LLllllD...",
    ".....LLakllldD..",
    "..LLLLlllllldD..",
    ".kLLLLllllllldD.",
    ".kkLLLlllllldD..",
    "..mCCCllllllddD.",
    "...CCCClllllddDD",
    "....CLllllldddDD",
    "...LLllllddddDDd",
    "..LLlllldddddDDd",
    ".LLllllddddddDDd",
    "LLlllllddddddDDd",
]
BANDIDO_A = [
    "................",
    ".....hhHHh......",
    "....hHHHHHh.....",
    "....hxPPPPoh....",
    "....xooPpooo....",
    "....PePxpeoo....",
    "....PPPxppoo....",
    "....sPPppsoo....",
    "....sssmmsso....",
    ".....sssssoo....",
    "......soooo.....",
    "...RRRrRRRrr....",
    "..TTRRrrRrrTt...",
    ".TTTTRrrrtTttt..",
    "TTTTTTrtttttttu.",
    "TTTTTtttttttttuu",
]
BANDIDO_B = [
    "................",
    "......jJKKj.....",
    ".....jJKKKKj....",
    "....jJKKKKKKj...",
    "....JKKjjjjKKj..",
    "....JKhhHhhjKj..",
    "...jKhPPPPojKj..",
    "...jKjPePeojKj..",
    "...JKjPPPpojKj..",
    "...JKjjPpoojKj..",
    "..JJKjjoooojKjj.",
    ".JJKKjBBjjjjKJjj",
    "JJKKjjBBjjjjKJjj",
    "JKKjjjjBjjjjJjjj",
    "KKjjjjjjjjjjjjjj",
    "KjjjjjjjjjjjjjJj",
]

# A segunda rodada (21/10/2026, pedido do Jean). O Lobo A continua (a cabeça, a paleta, as orelhas e o focinho): embaixo,
# as massas dos lados e o centro claro liam como ombros e peito de um lobo humanoide. A base vira o começo do pescoço
# de um quadrúpede: os tufos da bochecha saindo da mandíbula, a garganta na sombra, o pescoço estreito que desce para a
# direita (para trás, para o corpo fora do quadro), sem o peito claro e sem os dois ombros. A cabeça fica no lugar
# (as orelhas no topo). Duas etapas: só a base (`lobo-a-base`) e a base com o ajuste discreto do olhar (a sombra da
# testa por cima do canto de dentro dos olhos) e dos planos do focinho (o alto claro, os lados na cor do pelo, a linha
# da boca) (`lobo-a-ajustado`).
LOBO_A_BASE = [
    "...D........D...",
    "..Dld......dlD..",
    "..LnlD....DnlD..",
    "..LnldDddDdnld..",
    "..LLllllllllld..",
    ".dLLlllllllllDD.",
    ".dLLakllllkaldD.",
    ".dLLLllCClllldD.",
    ".dLLlCCCCCClldD.",
    "..dLlCCCCCCldD..",
    "..dLLCCkkCCldD..",
    ".L.dLlCCCCldD.d.",
    "..d.ddllllddD...",
    "....dLlllddDDd..",
    "....dLllldddDDd.",
    "...dLlllddddDDDd",
]
LOBO_A_AJUSTADO = [
    "...D........D...",
    "..Dld......dlD..",
    "..LnlD....DnlD..",
    "..LnldDddDdnld..",
    "..LLllllllllld..",
    ".dLLldllllldlDD.",
    ".dLLakllllkaldD.",
    ".dLLLldCCdllldD.",
    ".dLLllCCCClllDD.",
    "..dLlLCCCCLldD..",
    "..dLLlCkkCllDD..",
    "..LdLlnCCnldDd..",
    "..d.ddllllddD...",
    "....dLlllddDDd..",
    "....dLllldddDDd.",
    "...dLlllddddDDDd",
]
# Os três Bandidos novos (o A e o B ficam como histórico): o brutamontes (careca, a cicatriz no crânio, as sobrancelhas
# em V, os dentes falhados cerrados na barba, o pescoço grosso no couro), o do chapéu (a aba larga que põe os olhos na
# sombra, o meio sorriso de lado, o cabelo comprido, o lenço vermelho, o casaco) e o da faca (o capuz cinza, a máscara
# de pano vermelho até o nariz, os olhos que encaram, a faca erguida ao lado do rosto).
BANDIDO_BRUTAMONTES = [
    "................",
    ".....xPPrPp.....",
    "....xPPPPrPpo...",
    "...PPPPPPPrpoo..",
    "...PnPPPPPnpoo..",
    "...PPnPPPnppoo..",
    "...PPePxpeoooo..",
    "...pPPPxppooo...",
    "...hmWmWmWhoo...",
    "...hhmmmmmhho...",
    "....hhhhhhho....",
    ".TTTToooooTTTt..",
    "TTTtTtoootTtTttt",
    "TTtttTttttTtttuu",
    "TTttttttttttttuu",
    "Tttttttttttttttu",
]
BANDIDO_CHAPEU = [
    "................",
    "......qQQQq.....",
    ".....qQQQQQq....",
    "..QQQQQQQQQQqq..",
    "...qqqqqqqqqqq..",
    "....hoooooooh...",
    "....hPePpeooh...",
    "....hPPxppooh...",
    "....hPPpmmmoh...",
    "....hhPPPpohh...",
    "....hh.ooo.hh...",
    "..qqhRRRRRrhqq..",
    ".qqqqRRrrRrqqqq.",
    "qqqqqqRrrqqqqqqq",
    "qQqqqqqrqqqqqqqq",
    "QQqqqqqqqqqqqqqq",
]
BANDIDO_FACA = [
    "................",
    "......gGGg......",
    ".....gGGGGg.....",
    "....gGGggGGg....",
    ".M..GGgPPpgGg...",
    ".MN.gGnPPnggGg..",
    ".MN.gGWePeWgGg..",
    ".MN.gGRRRRrrgGg.",
    ".MN.gGRRRRrrrgGg",
    ".MN.gGgRRrrrgGg.",
    ".Pu.GGggRrgggGGg",
    "PPPGGGgggggggGGg",
    "gPGGGgggggggGGgg",
    "gGGGggggggggGGgg",
    "GGGgggggggggGggg",
    "GGggggggggggggcc",
]

CAMADAS = {
    "lobo-a": (LOBO_A, ["pelagem", "focinho", "detalhes"],
               lambda x, y, ch: "focinho" if ch == "C" else "detalhes" if ch in "kanm" else "pelagem"),
    "lobo-b": (LOBO_B, ["pelagem", "focinho", "detalhes"],
               lambda x, y, ch: "focinho" if ch == "C" else "detalhes" if ch in "kanm" else "pelagem"),
    "lobo-a-base": (LOBO_A_BASE, ["pelagem", "focinho", "detalhes"],
                    lambda x, y, ch: "focinho" if ch == "C" else "detalhes" if ch in "kanm" else "pelagem"),
    "lobo-a-ajustado": (LOBO_A_AJUSTADO, ["pelagem", "focinho", "detalhes"],
                        lambda x, y, ch: "focinho" if ch == "C" else "detalhes" if ch in "kanm" else "pelagem"),
    "bandido-brutamontes": (BANDIDO_BRUTAMONTES, ["roupa", "pele", "barba", "rosto"],
                            lambda x, y, ch: "roupa" if ch in "Ttu" else "barba" if ch == "h" else "rosto" if ch in "enmWr"
                            else "pele"),
    "bandido-chapeu": (BANDIDO_CHAPEU, ["roupa", "lenco", "chapeu", "cabelo", "pele", "rosto"],
                       lambda x, y, ch: "chapeu" if ch in "Qq" and y < 5 else "roupa" if ch in "Qq" else "lenco" if ch in "Rr"
                       else "cabelo" if ch == "h" else "rosto" if ch in "em" else "pele"),
    "bandido-faca": (BANDIDO_FACA, ["capuz", "pele", "mascara", "rosto", "faca", "mao"],
                     lambda x, y, ch: "faca" if ch in "MNu" else "mao" if ch == "P" and x <= 3 else "capuz" if ch in "Ggc"
                     else "mascara" if ch in "Rr" else "rosto" if ch in "Wen" else "pele"),
    "bandido-a": (BANDIDO_A, ["roupa", "lenco", "pele", "cabelo", "rosto"],
                  lambda x, y, ch: "roupa" if ch in "Ttu" else "lenco" if ch in "Rr" else "cabelo" if ch in "Hh"
                  else "rosto" if ch in "em" else "pele"),
    "bandido-b": (BANDIDO_B, ["capuz", "cabelo", "pele", "rosto"],
                  lambda x, y, ch: "capuz" if ch in "KJj" else "cabelo" if ch in "HhB" else "rosto" if ch == "e"
                  else "pele"),
}


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
