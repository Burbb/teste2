"""As juntas do braço da colher de Morel no canto, pose a pose (protótipo): o estudo de construção em números.

    python ferramentas/prototipos/taverna/morel/canto/juntas.py      # a tabela e os passos

O método é o do braço aprovado (`morel/estudo-construcao/juntas.py`, pela skill `arte-personagens-fenda`): o braço com
comprimento físico fixo, o cotovelo pela cinemática inversa de dois ossos, a colher rígida a partir do pulso; o que
muda na tela é o escorço. As trajetórias antigas não são forçadas aqui: a cena nova tem outra escala (Morel ~1,35 vez
maior) e outra postura (o cotovelo do braço da colher pousado bem para fora, ao lado da caneca, como na referência).

A projeção: a câmera um pouco acima dos olhos dele, olhando uns 35° para baixo (o que vem para a frente aparece mais
baixo, como o tampo). As poses são as mesmas 20 da vista aprovada, na mesma ordem e com os mesmos nomes, para a linha
do tempo e a reação ao pagamento continuarem as mesmas (recolher duas vezes, sair da tigela, subir, a pausa com a
colher cheia diante do peito, a boca, descer, repousar, mastigar, olhar)."""
import math

BRACO, ANTEBRACO, COLHER = 34.0, 28.0, 20.0
CA, SA = math.cos(math.radians(35)), math.sin(math.radians(35))
OMBRO_Y = 44


def tela(p, dy=0):
    """Do espaço (x, y para baixo, z para quem olha) para a tela; dy é o quanto o corpo desceu."""
    return (p[0], OMBRO_Y + (p[1] - OMBRO_Y) * CA + p[2] * SA + dy)


def espaco(sx, sy, z):
    return (sx, OMBRO_Y + (sy - z * SA - OMBRO_Y) / CA, z)


def _sub(a, b): return tuple(x - y for x, y in zip(a, b))
def _add(a, b): return tuple(x + y for x, y in zip(a, b))
def _mul(a, s): return tuple(x * s for x in a)
def _dot(a, b): return sum(x * y for x, y in zip(a, b))
def _un(a): n = math.sqrt(_dot(a, a)); return _mul(a, 1 / n)
def _lerp(a, b, t): return tuple(x + (y - x) * t for x, y in zip(a, b))


def cotovelo(ombro, pulso, polo):
    """O cotovelo com braço e antebraço no comprimento certo, dobrando para `polo`."""
    d = _sub(pulso, ombro)
    dist = min(math.sqrt(_dot(d, d)), BRACO + ANTEBRACO - 0.01)
    u = _un(d)
    a = (BRACO ** 2 - ANTEBRACO ** 2 + dist ** 2) / (2 * dist)
    hh = math.sqrt(max(BRACO ** 2 - a * a, 0))
    lado = _un(_sub(polo, _mul(u, _dot(polo, u))))
    return _add(_add(ombro, _mul(u, a)), _mul(lado, hh))


# a boca no espaço (a da cabeça, com a cabeça descendo ao encontro da colher); a colher chega de frente e um pouco de
# baixo, a concha nos lábios
BOCA = (171.0, 22.0, 6.0)
_DC = (0.55, -0.25, -0.8)
_n = math.sqrt(_dot(_DC, _DC))
# as chaves: o ombro na tela e a profundidade, o pulso no espaço, a direção da colher, o polo (o cotovelo para fora e
# para baixo: na referência ele pousa ao lado da caneca). A colher é rígida e a pega não desliza: o que muda entre as
# chaves é só a direção, e só o que o gesto pede (a ponta para dentro do caldo na coleta, quase nivelada para carregar
# a comida subindo, um ajuste curto para a boca); a mão fica afastada da borda o bastante para a haste aparecer até o
# caldo
CHAVES = {
    "recolher": dict(S=(138, 44, -6), W=(139, 55, 17), T=(0.85, 0.45, 0.25), polo=(-1, 0.7, 0.3)),
    "levantar": dict(S=(138, 44, -5), W=(146, 44, 14), T=(0.9, 0.0, -0.3), polo=(-1, 0.7, 0.3)),
    "boca": dict(S=(140, 42, -4), W=tuple(b - d / _n * COLHER for b, d in zip(BOCA, _DC)), T=_DC, polo=(-1, 0.8, 0.3)),
    "retornar": dict(S=(138, 44, -5), W=(145, 47, 15), T=(0.9, 0.1, -0.2), polo=(-1, 0.7, 0.3)),
    "repousar": dict(S=(138, 44, -6), W=(138, 56, 18), T=(0.85, 0.45, 0.25), polo=(-1, 0.7, 0.3)),
}
# a subida e a descida, cada uma uma curva só (a curva de Bézier quadrática pelas três chaves do trecho: a do meio puxa
# a curva sem que a mão passe por ela, e a mão não faz gancho para um lado e depois para o outro); a fração na curva
# dá a facilidade: devagar ao sair da tigela, na pausa diante do peito e ao chegar à boca, passos parecidos no meio
SUBIDA = ("recolher", "levantar", "boca")
DESCIDA = ("boca", "retornar", "repousar")
# (pose, trecho, fração, corpo desce, cabeça, cabeça desce, colher cheia): a mesma ordem da vista aprovada
ROTEIRO = [
    ("recolhe", ("recolher",), 0, 1, "baixo", 1, False),
    ("recolhe2", ("recolher",), 0, 1, "baixo", 1, False),
    ("sai", SUBIDA, 0.09, 1, "baixo", 1, True),
    ("sobe1", SUBIDA, 0.21, 1, "baixo", 1, True),
    ("sobe2", SUBIDA, 0.34, 1, "baixo", 1, True),
    ("levanta", SUBIDA, 0.46, 1, "baixo", 1, True),
    ("sobe3", SUBIDA, 0.61, 1, "baixo", 1, True),
    ("sobe4", SUBIDA, 0.77, 1, "baixo", 2, True),
    ("sobe5", SUBIDA, 0.91, 1, "boca", 3, True),
    ("boca", ("boca",), 0, 1, "boca", 3, False),
    ("desce1", DESCIDA, 0.1, 1, "baixo", 2, False),
    ("desce2", DESCIDA, 0.23, 1, "mastiga", 1, False),
    ("desce2b", DESCIDA, 0.37, 1, "baixo", 1, False),
    ("desce2c", DESCIDA, 0.51, 1, "mastiga", 1, False),
    ("retorna", DESCIDA, 0.64, 1, "baixo", 1, False),
    ("desce3", DESCIDA, 0.77, 1, "baixo", 1, False),
    ("desce4", DESCIDA, 0.9, 0, "mastiga", 0, False),
    ("repousa", ("repousar",), 0, 0, "baixo", 0, False),
    ("mastiga", ("repousar",), 0, 0, "mastiga", 0, False),
    ("olha", ("repousar",), 0, 0, "olha", -1, False),
]


def _curva(trecho, t, k):
    if len(trecho) == 1:
        return CHAVES[trecho[0]][k]
    a, b, c = (CHAVES[n][k] for n in trecho)
    return tuple((1 - t) ** 2 * x + 2 * (1 - t) * t * y + t * t * z for x, y, z in zip(a, b, c))


def poses():
    out = []
    for nome, trecho, t, dy, cab, dyc, cheia in ROTEIRO:
        p = {k: _curva(trecho, t, k) for k in ("S", "W", "T", "polo")}
        S = espaco(p["S"][0], p["S"][1], p["S"][2])
        W, d = p["W"], _un(p["T"])
        if nome == "recolhe2":  # a concha mais funda no caldo
            W = (W[0] + 1, W[1] + 1, W[2])
            d = (d[0], d[1] + 0.2, d[2])
        T = _add(W, _mul(_un(d), COLHER))
        E = cotovelo(S, W, p["polo"])
        s, e, w, tt = tela(S, dy), tela(E, dy), tela(W), tela(T)
        out.append(dict(nome=nome, dy=dy, cabeca=cab, dyc=dyc, cheia=cheia, S=s, E=e, W=w, T=tt,
                        braco=math.dist(s, e), antebraco=math.dist(e, w), dir_colher=_un(_sub(tt, w))))
    return out


def main():
    P = poses()
    for i, x in enumerate(P):
        passo = ""
        if i:
            a = P[i - 1]
            passo = (f"  anda: mão {math.dist(x['W'], a['W']):4.1f} cotovelo {math.dist(x['E'], a['E']):4.1f} "
                     f"colher {math.dist(x['T'], a['T']):4.1f}")
        r = lambda q: tuple(round(v) for v in q)  # noqa: E731
        print(f"{i:2d} {x['nome']:9s} ombro{r(x['S'])} cotovelo{r(x['E'])} pulso{r(x['W'])} colher{r(x['T'])}  "
              f"braço {x['braco']:4.1f} antebraço {x['antebraco']:4.1f}{passo}")


if __name__ == "__main__":
    main()
