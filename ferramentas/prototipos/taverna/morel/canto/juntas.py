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

BRACO, ANTEBRACO, COLHER = 34.0, 28.0, 17.0
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


# a boca no espaço (a da cabeça, com a cabeça descendo ao encontro da colher); a colher entra de frente e de baixo
BOCA = (171.0, 22.0, 6.0)
_DC = (0.45, -0.5, -0.7)
_n = math.sqrt(_dot(_DC, _DC))
# as chaves: o ombro na tela e a profundidade, o pulso no espaço, a direção da colher, o polo (o cotovelo para fora e
# para baixo: na referência ele pousa ao lado da caneca)
CHAVES = {
    # na tigela, a ponta da colher pega o caldo por dentro da boca dela (não na borda): o pulso junto da borda da
    # esquerda e a colher descendo para dentro
    "recolher": dict(S=(138, 44, -6), W=(143, 55, 17), T=(0.765, 0.294, 0.571), polo=(-1, 0.7, 0.3)),
    "levantar": dict(S=(138, 44, -5), W=(140, 44, 14), T=(0.6, -0.45, 0.45), polo=(-1, 0.7, 0.3)),
    "boca": dict(S=(140, 42, -4), W=tuple(b - d / _n * COLHER for b, d in zip(BOCA, _DC)), T=_DC, polo=(-1, 0.8, 0.3)),
    "retornar": dict(S=(138, 44, -5), W=(139, 47, 15), T=(0.6, -0.3, 0.45), polo=(-1, 0.7, 0.3)),
    "repousar": dict(S=(138, 44, -6), W=(142, 56, 18), T=(0.765, 0.294, 0.571), polo=(-1, 0.7, 0.3)),
}
# (pose, chave de partida, chave de chegada, fração, corpo desce, cabeça, cabeça desce, colher cheia): a mesma ordem da
# vista aprovada (as frações dão a facilidade: devagar ao sair da tigela e ao chegar à boca)
ROTEIRO = [
    ("recolhe", "recolher", "recolher", 0, 1, "baixo", 1, False),
    ("recolhe2", "recolher", "recolher", 0, 1, "baixo", 1, False),
    ("sai", "recolher", "levantar", 0.17, 1, "baixo", 1, True),
    ("sobe1", "recolher", "levantar", 0.44, 1, "baixo", 1, True),
    ("sobe2", "recolher", "levantar", 0.72, 1, "baixo", 1, True),
    ("levanta", "levantar", "levantar", 0, 1, "baixo", 1, True),
    ("sobe3", "levantar", "boca", 0.3, 1, "baixo", 1, True),
    ("sobe4", "levantar", "boca", 0.6, 1, "baixo", 2, True),
    ("sobe5", "levantar", "boca", 0.85, 1, "boca", 3, True),
    ("boca", "boca", "boca", 0, 1, "boca", 3, False),
    ("desce1", "boca", "retornar", 0.15, 1, "baixo", 2, False),
    ("desce2", "boca", "retornar", 0.36, 1, "mastiga", 1, False),
    ("desce2b", "boca", "retornar", 0.58, 1, "baixo", 1, False),
    ("desce2c", "boca", "retornar", 0.8, 1, "mastiga", 1, False),
    ("retorna", "retornar", "retornar", 0, 1, "baixo", 1, False),
    ("desce3", "retornar", "repousar", 0.4, 1, "baixo", 1, False),
    ("desce4", "retornar", "repousar", 0.73, 0, "mastiga", 0, False),
    ("repousa", "repousar", "repousar", 0, 0, "baixo", 0, False),
    ("mastiga", "repousar", "repousar", 0, 0, "mastiga", 0, False),
    ("olha", "repousar", "repousar", 0, 0, "olha", -1, False),
]


def poses():
    out = []
    for nome, a, b, t, dy, cab, dyc, cheia in ROTEIRO:
        p = {k: _lerp(CHAVES[a][k], CHAVES[b][k], t) for k in ("S", "W", "T", "polo")}
        S = espaco(p["S"][0], p["S"][1], p["S"][2])
        W, d = p["W"], p["T"]
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
