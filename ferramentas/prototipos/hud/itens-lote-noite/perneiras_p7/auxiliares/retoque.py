"""O retoque das laterais da P7 (20/10/2026, pedido do Jean sobre o 3cb041db; o antes em anterior_3cb041db/): no 32, as
laterais das coxas e das canelas liam como placas ou apetrechos de metal separados, fortes demais perto da malha. A
construção, as proporções, o cinto, as joelheiras e a separação das pernas ficam; as joelheiras continuam o aço mais
evidente. O que muda, por região (cada pixel com o "antes" conferido):
  - a beira de fora das coxas: a faixa acesa contínua (o 7 na da esquerda, o 6 na da direita) vira um tom liso perto do da
    malha ao lado, mais claro em cima e mais escuro embaixo, acompanhando a luz da perna;
  - a junta escura entre essa beira e a malha (o 3 da esquerda, o 3 da direita) entra na malha, no xadrez da cota com o
    volume da coluna vizinha; no quadril (linhas 5 e 6), a placa de 1 px também vira malha;
  - a junta entre a placa de cima e a de baixo (linha 11) fica só sugerida, um tom abaixo da beira;
  - a asa acima da canela (linhas 23 e 24): a linha 24 volta à largura da canela (a saliência fica só na 23, a borda de
    cima da caneleira), e a 23 perde o brilho de aba (as pontas e a faixa mais baixas);
  - as tiras de aço das canelas: a de fora (o 7) vira o tom liso da beira; a de dentro (o 5) entra na malha, na sombra.
Grava grades/P7.txt e as listas do retoque por camada para o pintar.lua (listas/retoque/<camada>.lua; o pixel que muda
de camada é apagado na antiga).
    python retoque.py <pasta da P7>
"""
import pathlib
import sys

FERRO = ["0e0f11", "1a1c20", "282b31", "383c44", "4c5159", "646a73", "848b94", "b0b6bd", "e4e8ec"]
COURO = {"a": "140b09", "b": "251412", "c": "3a1f1a", "d": "522c23", "e": "6b3b2d", "f": "86503c"}
CONTORNO = "08080a"
DIREITA = 11
RETOQUE = []   # (x, y, o pixel esperado antes, o novo, a camada nova, o porquê)


def xadrez(x, y, t):
    """O tom da malha da cota: o do volume onde (x + y) é par, o de baixo onde é ímpar."""
    return str(t if (x + y) % 2 == 0 else max(t - 1, 2))


def muda(x, y, antes, novo, porque):
    RETOQUE.append((x, y, antes, novo, porque))


BEIRA = "a beira de fora da coxa: o tom liso perto do da malha, pela luz da perna (no lugar da faixa acesa de aço)"
JUNTA = "a junta escura entre a beira e a malha entra na malha (o volume da coluna vizinha, no xadrez da cota)"
QUADRIL = "a placa de 1 px do quadril entra na malha"
PLACAS = "a junta entre a placa de cima e a de baixo, só sugerida (um tom abaixo da beira)"
# a coxa da esquerda: a beira (x 7) e a junta (x 8); o volume da malha em x 8 é o da coluna x 9 (6), com a sombra das
# linhas 5 e 14
for y, beira in ((7, "6"), (8, "6"), (9, "5"), (10, "5"), (12, "5"), (13, "5"), (14, "4")):
    muda(7, y, "7", beira, BEIRA)
for y in (7, 8, 9, 10, 12, 13, 14):
    muda(8, y, "3", xadrez(8, y, 5 if y == 14 else 6), JUNTA)
muda(7, 11, "3", "4", PLACAS)
muda(8, 11, "2", xadrez(8, 11, 6), JUNTA)
muda(8, 5, "5", xadrez(8, 5, 5), QUADRIL)
muda(8, 6, "6", xadrez(8, 6, 6), QUADRIL)
# a coxa da direita (do lado da sombra): a beira (x 24) e a junta (x 23), o volume da malha em x 23 o da x 22 (3)
for y in (7, 8, 9, 10, 12, 13, 14):
    muda(24, y, "6", "3" if y == 14 else "4", BEIRA)
    muda(23, y, "3", xadrez(23, y, 3), JUNTA)
muda(24, 11, "3", "3", PLACAS)   # já no tom: fica (registrado para a conferência)
muda(23, 11, "2", xadrez(23, 11, 3), JUNTA)
muda(23, 5, "3", xadrez(23, 5, 3), QUADRIL)
muda(23, 6, "4", xadrez(23, 6, 3), QUADRIL)

ASA = "a asa acima da canela: a saliência fica só na borda de cima da caneleira (linha 23), sem o brilho de aba"
LARGURA = "a linha 24 volta à largura da canela (a asa de 2 linhas lia como aba de metal)"
FORA = "a tira de fora da canela: o tom liso da beira, pela luz da perna (no lugar da faixa acesa contínua)"
DENTRO = "a tira de dentro da canela entra na malha, na sombra"
for d in (0, DIREITA):
    for x, antes, novo in ((7, "7", "5"), (8, "6", "5"), (9, "6", "5"), (10, "5", "4"), (11, "5", "4"), (12, "4", "4"),
                           (13, "6", "3")):
        muda(x + d, 23, antes, novo, ASA)
    muda(6 + d, 24, "#", ".", LARGURA)
    muda(14 + d, 24, "#", ".", LARGURA)
    muda(7 + d, 24, "6", "#", LARGURA)
    muda(13 + d, 24, "4", "#", LARGURA)
    muda(8 + d, 24, "7", "5", FORA)
    muda(12 + d, 24, "5", xadrez(12 + d, 24, 3), DENTRO)
    for y, beira in ((25, "5"), (26, "5"), (27, "4")):
        muda(8 + d, y, "7", beira, FORA)
        muda(12 + d, y, "5", xadrez(12 + d, y, 3), DENTRO)


def camada(ch, x, y, malha):
    if ch == ".": return None
    if ch == "#": return "contorno"
    if ch in COURO: return "couro"
    return "malha" if (x, y) in malha else "aco"


def cor(ch):
    return CONTORNO if ch == "#" else COURO[ch] if ch in COURO else FERRO[int(ch)]


if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    antes = base / "anterior_3cb041db"
    g = [list(l) for l in (antes / "P7.txt").read_text(encoding="utf-8").split("\n")[:32]]
    lista = (antes / "listas/malha.lua").read_text(encoding="utf-8").split('"')[1]
    malha = {tuple(map(int, p.split(",")[:2])) for p in lista.split(";")}
    erros = [(x, y, g[y][x], a) for x, y, a, _, _ in RETOQUE if g[y][x] != a]
    if erros: raise SystemExit(f"o pixel de antes não confere: {erros}")
    novo_malha = set(malha)
    listas = {}
    for x, y, a, n, porque in RETOQUE:
        ca = camada(a, x, y, malha)
        if n.isdigit() and porque in (JUNTA, QUADRIL, DENTRO): novo_malha.add((x, y))
        else: novo_malha.discard((x, y))
        cn = camada(n, x, y, novo_malha)
        g[y][x] = n
        if ca and ca != cn: listas.setdefault(ca, []).append(f"{x},{y},00000000")
        if cn: listas.setdefault(cn, []).append(f"{x},{y},{cor(n)}")
    (base / "grades/P7.txt").write_text("\n".join("".join(l) for l in g) + "\n", encoding="utf-8")
    d = base / "listas/retoque"; d.mkdir(parents=True, exist_ok=True)
    for k, v in listas.items():
        (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
    print(len(RETOQUE), "pixels;", {k: len(v) for k, v in listas.items()})
    print("\n".join(f"{y:2d} {''.join(l)}" for y, l in enumerate(g)))
