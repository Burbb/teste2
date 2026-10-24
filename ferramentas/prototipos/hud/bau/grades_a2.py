"""A2 · o refino do A (24/10/2026): a mesma identidade (tábuas castanhas, cintas de ferro, espelho de latão) com a
tampa alta e abaulada, a três quartos mais evidente (a frente, o tampo e a ponta direita com o arco à vista) e o
volume pelos planos de luz: o tampo claro, a frente média, a ponta escura. As cintas das pontas acompanham o perfil
da tampa. Grades desenhadas à mão, um caractere por pixel (as linhas montadas por trechos, cada trecho escolhido)."""
import pathlib, sys  # noqa: E401
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from grades_a import PALETA, CAMADAS  # noqa: F401,E402  (a mesma paleta e as mesmas camadas do A)


def _monta(linhas):
    g = []
    for partes in linhas:
        r = "".join(partes)
        assert len(r) == 32, (partes, len(r))
        g.append(r)
    g += ["." * 32] * (32 - len(g))
    return g


#        fora        contorno  cinta esq.  tampo/frente            cinta dir.  ponta       aro   contorno  fora
G32 = [
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "..........kkkkkkkkkkkkkk........",
    "........kkdd4666666666ddek......",
    "......kkdd556666666655dcb44dk...",
    "....kkdc555555555554dcb44444dk..",
    "...kdc3333333333333dcb444443ck..",
    "..kdcb555555555554dcb4444433ck..",
    "..kdcb44444444444dcb44444333ck..",
    "..kdcb66666666666dcb44444443ck..",
    "..kdeb444hGGGh444deb444444kkck..",
    "..kdbb444hyGGh444dab4444kk22ck..",
    "..kdcb333hGkGh333dcb44kk2222ck..",
    "..kdcbkkkhGkGhkkkdcbkk222222ck..",
    "..kdcb555gGGGg555dcb22222222bk..",
    "..kdcb4444ghg4444dcb22222211bk..",
    "..kdcb22222222222dcb22221122bk..",
    "..kdcb44444444444dcb22112222bk..",
    "..kdeb33333333333deb11222222bk..",
    "..kdbb22222222222dab22222222bk..",
    "..kdcb44444444444dcb22222111kk..",
    "..kdcb33333333333dcb221111kkk...",
    "..kcbb22222222222cbb1111kk......",
    "..kbaa11111111111baa11kk........",
    "..kkkkkkkkkkkkkkkkkkkkk.........",
    "................................",
    "................................",
    "................................",
    "................................",
]


# ------------------------------------------------------------------ o 48 próprio (a pilha de vários baús abertos)
# A mesma construção do 32 na grade de 48, desenhada por trechos: a cumeeira curta e os cantos caindo, as cintas das
# pontas seguindo o perfil da tampa, o tampo com a junta, a borda da tampa na luz, o espelho de latão sobre a emenda,
# três tábuas na frente e a ponta direita com o arco claro em cima da emenda inclinada. Ocupa 39×33 (o antigo, 40×35).
def _r(*partes):
    r = "".join(partes)
    assert len(r) == 48, (partes, len(r))
    return list(r)


# a emenda da ponta: em que linha ela passa em cada coluna (sobe 1 a cada 2 colunas, para o fundo)
_EMENDA = {29: 23, 30: 23, 31: 22, 32: 22, 33: 21, 34: 21, 35: 20, 36: 20, 37: 19, 38: 19, 39: 18}
# o espelho de latão (x13..19) por linha; "-" deixa a madeira
_ESPELHO = {18: "-hGGGh-", 19: "hGyGGGh", 20: "hGGGGGh", 21: "hGGkGGh", 22: "hGGkGGh", 23: "hGGkGGh",
            24: "gGGGGGg", 25: "-ghhhg-", 26: "--ggg--"}
# a madeira da frente (x8..24), linha a linha: a borda da tampa na luz, a frente da tampa, a emenda, três tábuas
_FRENTE = {17: "6", 18: "4", 19: "4", 20: "4", 21: "3", 22: "3", 23: "k", 24: "5", 25: "4", 26: "4", 27: "4", 28: "3",
           29: "2", 30: "4", 31: "4", 32: "3", 33: "3", 34: "2", 35: "4", 36: "3", 37: "2", 38: "1"}


def _g48():
    g = [list("." * 48) for _ in range(48)]
    g[7] = _r("." * 14, "k" * 20, "." * 14)                                                        # a cumeeira
    g[8] = _r("." * 11, "kkk", "dd", "44666666666666666", "ddde", "k", "." * 10)
    g[9] = _r("." * 9, "kk", "ddd", "556666666666666655", "ddcb", "44", "d", "k", "." * 8)
    g[10] = _r("." * 7, "kk", "ddc", "666666666666666665", "ddcb", "44444", "d", "k", "." * 7)
    g[11] = _r("." * 6, "k", "ddc", "5555555555555555554", "dccb", "4444444", "c", "k", "." * 6)
    g[12] = _r("." * 5, "k", "ddc", "5555555555555555554", "dccb", "44444444", "c", "k", "." * 6)
    g[13] = _r("." * 4, "k", "ddc", "3333333333333333333", "dccb", "444444444", "c", "k", "." * 6)   # a junta do tampo
    g[14] = _r("." * 3, "k", "ddcb", "555555555555555554", "dccb", "4444444444", "c", "k", "." * 6)
    g[15] = _r("." * 3, "k", "ddcb", "4" * 17, "dccb", "44444444443", "c", "k", "." * 6)
    g[16] = _r("." * 3, "k", "ddcb", "4" * 17, "dccb", "44444444433", "c", "k", "." * 6)
    for y in range(17, 39):  # a frente, as cintas, a ponta e o aro do fundo
        cinta = "ccbb" if y == 37 else "cbaa" if y == 38 else "ddcb"
        frente = list(_FRENTE[y] * 17)
        for i, c in enumerate(_ESPELHO.get(y, "")):
            if c != "-":
                frente[5 + i] = c
        ponta = []
        for x in range(29, 40):
            e = _EMENDA[x]
            if y < e:
                ponta.append("4" if x < 38 else "3")
            elif y == e:
                ponta.append("k")
            elif y > e + 15:
                ponta.append("k" if y == e + 16 else ".")
            elif y - e in (5, 10):
                ponta.append("1")
            else:
                ponta.append("2" if y - e < 13 else "1")
        aro = "c" if y <= 22 else "b"
        fundo_fim = 18 + 15  # onde o aro do fundo acaba (a base da ponta, no fundo)
        if y <= fundo_fim:
            fim = [aro, "k"]
        elif y == fundo_fim + 1:
            fim = ["k", "."]
        else:
            fim = [".", "."]
        g[y] = _r("." * 3, "k", cinta, "".join(frente), cinta, "".join(ponta), "".join(fim), "." * 6)
    g[39] = _r("." * 3, "k" * 26, "." * 19)                                                           # a base
    for y, x in ((20, 5), (32, 5)):  # os cravos nas duas cintas da frente
        g[y][x] = "e"; g[y + 1][x] = "b"; g[y][x + 22] = "e"; g[y + 1][x + 22] = "a"
    return ["".join(r) for r in g]


G48 = _g48()
