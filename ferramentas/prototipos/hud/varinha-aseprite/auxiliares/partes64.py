"""Lotes do 64 da varinha, parte por parte, para o draw_pixels_batch do Aseprite. Cada parte Ã© uma faixa ao longo da
diagonal: u = x - y (ao longo da varinha, para a ponta), s = x + y (de travÃ©s; s menor = lado da luz, em cima Ã 
esquerda). Um pixel existe quando u e s tÃªm a mesma paridade."""
import sys
W = ["2A120D", "431D14", "5E291B", "7A3824", "974B31", "B5674A", "CC8462"]          # jacarandÃ¡
L = ["24170F", "3A281B", "59402B", "7A5638", "8F6A48"]                              # couro
M = ["1A160E", "332A1B", "4E4128", "6E5C38", "8F7A4C", "B09A64", "CDBB86"]           # bronze envelhecido (rodada 2: mais escuro)
A = ["2E1004", "4A1D05", "7A3307", "B0520C", "E0841A", "F4A530", "FFC85A", "FFE7A8", "FFF6DE"]  # Ã¢mbar

def faixa(u0, u1, cor_de_s):
    """Os pixels de u0 a u1, com a cor dada por s (None = vazio)."""
    px = {}
    for u in range(u0, u1 + 1):
        for s in range(40, 90):
            if (u + s) % 2: continue
            c = cor_de_s(u, s)
            if c: px[((s + u) // 2, (s - u) // 2)] = c
    return px

def pomo(u, s):
    # uma esfera achatada: largura pela distÃ¢ncia ao centro do pomo (u = -33)
    larg = {-37: (62, 65), -36: (61, 66), -35: (60, 67), -34: (60, 67), -33: (60, 67), -32: (60, 67), -31: (60, 67),
            -30: (61, 66), -29: (61, 66)}[u]
    if not larg[0] <= s <= larg[1]: return None
    d = ((u + 34) ** 2) * 0.5 + (s - 61.5) ** 2          # distÃ¢ncia ao ponto da luz (em cima Ã  esquerda)
    t = 6 if d < 1.5 else 5 if d < 5 else 4 if d < 10 else 3 if d < 17 else 2 if d < 26 else 1
    if u >= -30: t = min(t, 3)                           # o pescoÃ§o, na sombra do pomo
    return M[t]

def pega(u, s):
    if not 61 <= s <= 66: return None
    t = {61: 4, 62: 3, 63: 3, 64: 2, 65: 1, 66: 0}[s]
    if u in (-24, -23, -17, -16) and s >= 62: t = max(0, t - 1)   # duas costuras discretas
    return L[t]

def anel(u, s):
    if not 61 <= s <= 66: return None
    t = {61: 6, 62: 5, 63: 4, 64: 3, 65: 2, 66: 1}[s]
    if u in (-11, -8): t = max(1, t - 2)                 # as bordas do anel
    return M[t]

def haste(u, s):
    if u <= 12:
        if not 62 <= s <= 65: return None
        t = {62: 5, 63: 4, 64: 3, 65: 1}[s]
    else:
        if not 62 <= s <= 64: return None
        t = {62: 4, 63: 3, 64: 1}[s]
    if s == 62 and -4 <= u <= 6: t = 6                   # o brilho da madeira polida, num trecho
    if s == 63 and u in (-2, 9, 18): t -= 1              # o veio
    return W[t]

def soquete(u, s):
    lim = (62, 65) if u <= 27 else (61, 66)              # (rodada 2: a taça abre em 6, menor que a pedra)
    if not lim[0] <= s <= lim[1]: return None
    t = {61: 5, 62: 5, 63: 4, 64: 3, 65: 2, 66: 1}[s]
    if u >= 30: t = min(6, t + 1)                        # a borda da frente, acesa
    if u == 28: t = max(0, t - 1)                        # a dobra onde a taÃ§a abre
    return M[t]

def cristal(u, s):
    larg = {32: (59, 68), 33: (59, 68), 34: (59, 68), 35: (59, 68), 36: (60, 67), 37: (60, 67), 38: (60, 67),
            39: (61, 66), 40: (61, 66), 41: (62, 65), 42: (62, 65), 43: (63, 64)}.get(u)
    if not larg or not larg[0] <= s <= larg[1]: return None
    if 31 <= u <= 34 and s in (59, 68):                  # as garras do soquete nas faces
        return M[5] if s == 59 else M[2]
    if s <= 63:   # a face de cima (luz)
        t = 5 if s <= 61 else 4
        if u >= 40: t = 4 if s <= 62 else 3             # a faceta da ponta, um degrau abaixo
    else:         # a face de baixo (sombra)
        t = 2 if s <= 65 else 1
    if s in (63, 64): t = 6 if s == 63 and u >= 34 else t   # a aresta do meio, acesa do lado da luz
    if u <= 33: t = max(1, t - 2)                        # a sombra de contato logo acima da borda
    if 35 <= u <= 37 and s in (65, 66): t = 4            # a luz que atravessa, embaixo
    return A[t]

PARTES = {"pomo": faixa(-37, -29, pomo), "pega": faixa(-28, -12, pega), "anel": faixa(-11, -8, anel),
          "haste": faixa(-7, 24, haste), "soquete": faixa(25, 31, soquete), "cristal": faixa(32, 43, cristal)}


def cristal2(u, s):
    """Rodada 2: corpo hexagonal (s 60 a 67) até u 37, ponta em pirâmide até u 43. Três faces: a de cima (60-62, luz),
    a da frente (63-64) e a de baixo (65-67, sombra); a crista entre a de cima e a da frente acesa."""
    hw = 4.0 if u <= 37 else 4.0 - (u - 37) * 0.6
    if not (63.5 - hw <= s <= 63.5 + hw or (u == 43 and s == 63)): return None
    if 32 <= u <= 34 and s in (60, 67):                  # as garras do soquete
        return M[5] if s == 60 else M[2]
    ponta = u >= 38
    if s <= 62: t = 6 if ponta else 5
    elif s <= 64: t = 5 if ponta else 4
    else: t = 3 if ponta else 2
    if s == 62 and u >= 33: t = 6                        # a crista entre a face de cima e a da frente
    if s == 67 and not ponta: t = 1                      # a beira de baixo
    if 35 <= u <= 36 and s in (60, 61): t = 7            # o reflexo
    if 33 <= u <= 35 and s == 66: t = 4                  # a luz que atravessa, embaixo
    if u <= 32: t = max(1, t - 2)                        # a sombra de contato junto da borda
    return A[t]
PARTES["cristal2"] = faixa(32, 43, cristal2)
PARTES["haste"] = faixa(-7, 24, haste); PARTES["soquete"] = faixa(25, 31, soquete); PARTES["pomo"] = faixa(-37, -29, pomo); PARTES["anel"] = faixa(-11, -8, anel)



def cristal3(u, s):
    """Rodada 3: faces largas, cada uma num tom (o serrilhado da rodada 2 vinha de um tom por linha diagonal)."""
    hw = 4.0 if u <= 37 else 4.0 - (u - 37) * 0.6
    if not (63.5 - hw <= s <= 63.5 + hw or (u == 43 and s == 63)): return None
    if 32 <= u <= 34 and s in (60, 67):                  # as garras do soquete
        return M[5] if s == 60 else M[2]
    ponta = u >= 39
    if s <= 62:   t = 6 if ponta else 5                  # a face de cima (luz); na ponta, um degrau acima
    elif s <= 65: t = 5 if ponta else 4                  # a face da frente
    else:         t = 3 if ponta else 2                  # a face de baixo (sombra)
    if 35 <= u <= 37 and s in (61, 62): t = 7            # o reflexo, um grupo pequeno
    if u == 36 and s == 61: t = 8
    if 34 <= u <= 36 and s == 66: t = 4                  # a luz que atravessa, embaixo
    if u <= 33: t = max(1, t - 2)                        # a sombra de contato junto da borda
    return A[t] if t < len(A) else A[-1]
PARTES["cristal3"] = faixa(32, 43, cristal3)

def haste2(u, s):
    """Rodada 3: o afinamento em três trechos (5, 4 e 3 linhas), o brilho de madeira polida na borda de cima."""
    tabela = ({61: 5, 62: 4, 63: 3, 64: 2, 65: 1} if u <= -1 else {62: 5, 63: 4, 64: 3, 65: 1} if u <= 11
              else {62: 4, 63: 3, 64: 1})
    if s not in tabela: return None
    t = tabela[s]
    if s == min(tabela) and -4 <= u <= 6: t = 6
    if s == 63 and u in (-2, 9, 18): t -= 1              # o veio
    return W[t]
PARTES["haste2"] = faixa(-7, 24, haste2)


if __name__ == "__main__":
    for nome in sys.argv[1:]:
        px = PARTES[nome]
        print(f"# {nome} {len(px)}", file=sys.stderr)
        print(";".join(f"{x},{y},{c}" for (x, y), c in sorted(px.items())))
