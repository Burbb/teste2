"""Monta a cabeça 24×24 do Morel candidata por camadas (cabelo, rosto, barba, ombros, a cicatriz por cima) e imprime a
grade que está em candidatos.py (MOREL_CABECA). Cada camada foi decidida olhando o tamanho real; mexa aqui e cole a
saída lá.
    python desenhar_cabeca.py"""
L = 24
g = [["."] * L for _ in range(L)]
def put(x, y, c):
    if 0 <= x < L and 0 <= y < L: g[y][x] = c
def faixa(y, x0, x1, c):
    for x in range(x0, x1 + 1): put(x, y, c)
# ombros: a ombreira de aço remendada à esquerda (S/s/d), a de couro e placa gasta à direita (F/f/n), o couro (L/l) e
# o tabardo vermelho (R/r) no meio
for y in range(17, 24):
    faixa(y, 0, 23, "l")
for y in range(18, 24):
    w = min(7, 3 + (y - 18))
    faixa(y, 0, w, "s"); put(0, y, "S"); put(1, y, "S"); put(w, y, "d")
    faixa(y, 23 - w, 23, "f"); put(23, y, "n"); put(23 - w, y, "n")
faixa(17, 0, 3, "S"); faixa(17, 20, 23, "F")
faixa(18, 1, 4, "S"); faixa(18, 19, 22, "F")
put(3, 20, "D"); put(4, 21, "g")            # o remendo (rebite) na ombreira de aço
for y in range(19, 24):
    faixa(y, 9, 11, "R"); faixa(y, 12, 14, "r")
# o pescoço e a barba que desce
for y in range(14, 18):
    faixa(y, 8, 15, "B" if y > 15 else "b"); faixa(y, 13, 15, "B")
# o cabelo
faixa(1, 8, 15, "C"); faixa(2, 6, 17, "C"); faixa(3, 5, 18, "C")
for y in range(4, 12):
    put(5, y, "C"); put(6, y, "C" if y < 6 else "c"); put(17, y, "k"); put(18, y, "k")
for y in (1, 2, 3):
    for x in range(12, 19):
        if g[y][x] == "C": g[y][x] = "c"
put(15, 1, "c"); put(17, 2, "k"); put(18, 3, "k"); put(17, 3, "c")
# o rosto (luz da esquerda: P, p no meio, o à direita)
for y in range(4, 14):
    for x in range(7, 17):
        g[y][x] = "P" if x < 11 else "p" if x < 15 else "o"
# sobrancelhas carregadas e baixas, olhos
faixa(7, 7, 9, "k"); faixa(7, 13, 15, "k"); put(10, 8, "c"); put(12, 8, "c")  # carregadas, puxadas para o meio
put(8, 8, "e"); put(14, 8, "e")
put(11, 9, "p"); put(11, 10, "o"); put(12, 10, "o")   # o nariz
# a barba cheia: das bochechas ao queixo, o bigode, a boca fechada
for y in range(10, 15):
    faixa(y, 7, 8, "b"); faixa(y, 15, 16, "B")
faixa(11, 9, 14, "B"); put(9, 11, "b")
faixa(12, 9, 14, "B"); put(9, 12, "b"); faixa(12, 10, 13, "t")
faixa(13, 7, 16, "B"); faixa(13, 7, 9, "b")
faixa(14, 8, 15, "B"); put(8, 14, "b")
# a cicatriz: da testa à bochecha direita, passando entre os olhos
for i, (x, y) in enumerate([(8, 4), (9, 5), (10, 6), (11, 7), (12, 8), (13, 9), (14, 10)]):
    if g[y][x] in "Pp": g[y][x] = "x"
print("\n".join(f'    "{"".join(l)}",' for l in g))
