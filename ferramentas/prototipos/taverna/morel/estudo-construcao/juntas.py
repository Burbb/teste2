"""As juntas do braço da colher de Morel, pose a pose: o estudo de construção em números.

    python ferramentas/prototipos/taverna/morel/estudo-construcao/juntas.py          # a tabela e os passos
    python ferramentas/prototipos/taverna/morel/estudo-construcao/juntas.py --lua    # a tabela para o Aseprite

O braço tem comprimento físico fixo (braço 28 px, antebraço 22, do pulso à ponta da colher 12); o que muda na tela é o
escorço. As poses-chave dizem onde ficam o ombro (na tela, com a profundidade z), o pulso e a direção da colher no
espaço; o cotovelo sai da cinemática inversa de dois ossos (o `polo` diz para que lado ele dobra). As passagens
interpolam as chaves. A projeção é a da cena: a câmera um pouco acima, olhando 30° para baixo (o que vem para a frente
aparece mais baixo, como o tampo da mesa).

A tabela impressa mostra, por pose, as juntas na tela, o comprimento projetado de cada osso (o braço "encurta" quando
aponta para quem olha) e quanto a mão, o cotovelo e a ponta da colher andam de uma pose para a seguinte (as passagens
de 100 ms). É o que a vista usa: as juntas de cada quadro estão na camada `guia` de morel/vista/morel-vista.aseprite e
as cinco chaves, desenhadas com formas simples, em morel-construcao.aseprite. Os números valem para Morel nesta cena;
o método é o da skill `arte-personagens-fenda`."""
import math
import sys

BRACO, ANTEBRACO, COLHER = 28.0, 22.0, 12.0
C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))


def tela(p, dy=0):
    """Do espaço (x, y para baixo, z para quem olha) para a tela; dy é o quanto o corpo desceu."""
    return (p[0], 35 + (p[1] - 35) * C30 + p[2] * S30 + dy)


def espaco(sx, sy, z):
    """Da tela (com o corpo no lugar) para o espaço, sabendo a profundidade."""
    return (sx, 35 + (sy - z * S30 - 35) / C30, z)


def _sub(a, b): return tuple(x - y for x, y in zip(a, b))
def _add(a, b): return tuple(x + y for x, y in zip(a, b))
def _mul(a, s): return tuple(x * s for x in a)
def _dot(a, b): return sum(x * y for x, y in zip(a, b))
def _un(a): n = math.sqrt(_dot(a, a)); return _mul(a, 1 / n)
def _lerp(a, b, t): return tuple(x + (y - x) * t for x, y in zip(a, b))


def cotovelo(ombro, pulso, polo):
    """Cinemática inversa de dois ossos: o cotovelo com braço e antebraço no comprimento certo, dobrando para `polo`."""
    d = _sub(pulso, ombro)
    dist = min(math.sqrt(_dot(d, d)), BRACO + ANTEBRACO - 0.01)
    u = _un(d)
    a = (BRACO ** 2 - ANTEBRACO ** 2 + dist ** 2) / (2 * dist)
    h = math.sqrt(max(BRACO ** 2 - a * a, 0))
    lado = _un(_sub(polo, _mul(u, _dot(polo, u))))
    return _add(_add(ombro, _mul(u, a)), _mul(lado, h))


# a boca no espaço com a cabeça 3 px abaixo (a cabeça desce ao encontro da colher); a colher entra nela de frente, então
# a mão fica à frente do queixo e o cotovelo logo abaixo do ombro (um V de uns 30° na tela, o mais aberto que os
# comprimentos permitem sem curvar o tronco)
BOCA = (216.5, 19, 4)
_DC = (0.5, -0.45, -0.75)
_n = math.sqrt(_dot(_DC, _DC))
# as chaves: o ombro na tela (com o corpo no lugar) e a profundidade dele, o pulso no espaço, a direção da colher, o polo
CHAVES = {
    "recolher": dict(S=(198, 35, -4), W=(205, 64, 20), T=(0.9, 0.15, 0.1), polo=(-1, 1, 0)),
    "levantar": dict(S=(198, 35, -3), W=(205, 46, 15), T=(0.7, -0.3, 0.5), polo=(-1, 1, 0.1)),
    # na boca o ombro sobe e vem para dentro 1 px (a clavícula sobe e avança junto com o braço)
    "boca": dict(S=(199, 34, -2), W=tuple(b - d / _n * COLHER for b, d in zip(BOCA, _DC)), T=_DC, polo=(-1, 1, 0)),
    "retornar": dict(S=(198, 35, -3), W=(204, 49, 17), T=(0.65, -0.2, 0.45), polo=(-1, 1, 0.1)),
    "repousar": dict(S=(198, 35, -4), W=(204, 64, 21), T=(0.9, 0.15, 0.1), polo=(-1, 1, 0)),
}
# (pose, chave de partida, chave de chegada, fração, corpo desce, cabeça, cabeça desce, colher cheia): a ordem dos
# quadros da fonte. As frações dão a facilidade (devagar ao sair da tigela e ao chegar à boca).
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
            W = (W[0] + 1, W[1] + 1, W[2]); d = (d[0], d[1] + 0.25, d[2])
        T = _add(W, _mul(_un(d), COLHER))
        E = cotovelo(S, W, p["polo"])
        s, e, w, tt = tela(S, dy), tela(E, dy), tela(W), tela(T)
        r = lambda q: (round(q[0]), round(q[1]))  # noqa: E731
        out.append(dict(nome=nome, dy=dy, cabeca=cab, dyc=dyc, cheia=cheia, S=r(s), E=r(e), W=r(w), T=r(tt),
                        braco=math.dist(s, e), antebraco=math.dist(e, w), cotovelo_y=E[1]))
    return out


def main():
    P = poses()
    if "--lua" in sys.argv:
        linhas = [f'{{nome="{x["nome"]}", dy={x["dy"]}, cab="{x["cabeca"]}", dyc={x["dyc"]}, '
                  f'cheia={"true" if x["cheia"] else "false"}, S={{{x["S"][0]},{x["S"][1]}}}, '
                  f'E={{{x["E"][0]},{x["E"][1]}}}, W={{{x["W"][0]},{x["W"][1]}}}, T={{{x["T"][0]},{x["T"][1]}}}}}'
                  for x in P]
        print("POSES3 = {\n" + ",\n".join(linhas) + "\n}")
        return
    for i, x in enumerate(P):
        passo = ""
        if i:
            a = P[i - 1]
            passo = (f"  anda: mão {math.dist(x['W'], a['W']):4.1f} cotovelo {math.dist(x['E'], a['E']):4.1f} "
                     f"colher {math.dist(x['T'], a['T']):4.1f}")
        print(f"{i:2d} {x['nome']:9s} ombro{x['S']} cotovelo{x['E']} pulso{x['W']} colher{x['T']}  "
              f"braço {x['braco']:4.1f}/28 antebraço {x['antebraco']:4.1f}/22{passo}")


if __name__ == "__main__":
    main()
