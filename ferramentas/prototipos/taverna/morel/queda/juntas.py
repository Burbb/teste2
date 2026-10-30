"""A queda de braço diante de Morel: o estudo de construção em números (protótipo, só as poses; nada animado).

    python ferramentas/prototipos/taverna/morel/queda/juntas.py          # a tabela das juntas e as conferências

**A câmera** é a da vista aprovada (320×96, o mesmo pixel), não outra: assim Morel, a sala e a mesa ficam como foram
aprovados e a disputa ocupa o meio do quadro. As tábuas do tampo fogem para (238, 30), a borda de lá do tampo está em
y 62 e a de cá em y 92; uma câmera de furo (f = 140 px, o eixo em x 238, o horizonte em y 30, 33 cm acima do tampo)
reproduz isso com a borda de cá a 74,5 cm e a de lá a 144,5 cm, e põe o ombro direito de Morel (198, 35 na tela) a uns
27 cm acima do tampo e 44 cm à direita dele do eixo: as medidas abaixo são em cm, nesse espaço (X para a direita de
quem olha, Y para cima a partir do tampo, z a distância da câmera).

**O gesto e os apoios.** Uma queda de braço com a mão direita: os dois cotovelos fincados no tampo e parados (é a
regra), as mãos agarradas entre eles, cada antebraço com o comprimento dele (Morel 28 cm do cotovelo ao pulso, mais 6
até o meio da pega; o nosso 27 e 6). As mãos só podem estar onde as duas distâncias batem: um círculo no plano que corta
ao meio a linha entre os cotovelos. No alto dele, a disputa; caindo para um lado ou para o outro até o dorso da mão de
quem perde tocar o tampo (4 cm), o fim. Quem vence leva a mão do outro para a própria esquerda: nós vencendo, as mãos
caem para a nossa esquerda e para perto de nós; Morel vencendo, para a esquerda dele (a nossa direita) e para longe.
Nenhum braço torce: o antebraço gira em volta do cotovelo, no mesmo plano o tempo todo.

**O que participa** (o esforço é grande, o alcance curto, os apoios são os cotovelos): os antebraços e as mãos
conduzem; o ombro de Morel acompanha (desce e avança 2 a 3 px na disputa, cede para o lado de quem perde, vem por
cima quando ele vence) e o tronco vai junto 1 px; a cabeça olha para nós (a pose `olha`, aprovada); o braço esquerdo
dele planta a mão no tampo, à direita do nosso antebraço; o quadril, a cadeira e a mesa ficam. Do nosso lado só se vê
o antebraço e a mão: o braço de cima sai pela borda de baixo do quadro, na direção do nosso ombro, que fica embaixo
da câmera (sem escorço do ombro nem do peito).

**A tigela** sai da área dos cotovelos antes da disputa: Morel a empurra com a mão direita para a direita dele (a
nossa esquerda), rente à borda de lá, entre a vela e o cotovelo dele (x 150 a 188); as mãos, quando nós vencemos,
caem logo à direita dela, sem tocá-la. O pão fica onde está (o nosso cotovelo pousa à esquerda dele, no eixo da câmera). Na volta à vista
normal, Morel puxa a tigela de volta antes de comer (o plano da animação, no LEIA-ME).

A tabela impressa dá, por pose, as juntas na tela (o ombro, o cotovelo, o pulso e a pega de cada um), o comprimento de
cada osso na tela e no espaço, e as conferências: os cotovelos no tampo, o comprimento dos antebraços igual nas três
poses, a pega a 4 cm do tampo nos fins."""
import math

F, CX, HOR, ALTURA = 140.0, 238.0, 30.0, 33.0

# os cotovelos, fincados no tampo nas três poses
COTOVELO_MOREL = (-28.0, 0.0, 128.0)
COTOVELO_NOSSO = (0.0, 0.0, 82.0)
ANTEBRACO_MOREL, ANTEBRACO_NOSSO, MAO = 28.0, 27.0, 6.0  # do cotovelo ao pulso; do pulso ao meio da pega
BRACO_MOREL = 31.0                                        # do ombro ao cotovelo
TAMPO_MAO = 4.0                                           # a altura da pega quando o dorso da mão toca o tampo
# o ombro direito de Morel em cada pose (no espaço): descansando, (198, 35) na tela
OMBRO_MOREL = {
    "disputa": (-41.0, 25.0, 142.0),         # inclinado sobre a mesa: o ombro desce e avança
    "vitoria_jogador": (-43.0, 22.0, 141.0),  # cede para o lado em que perde, mais baixo
    "vitoria_morel": (-38.0, 26.0, 137.0),    # vem por cima do braço, para a frente
}
# o nosso ombro fica embaixo da câmera, fora do quadro: só a direção do braço de cima importa (sai pela borda de baixo)
OMBRO_NOSSO_TELA = (268, 116)


def tela(p):
    x, y, z = p
    return (CX + F * x / z, HOR + F * (ALTURA - y) / z)


def _sub(a, b): return tuple(x - y for x, y in zip(a, b))
def _add(a, b): return tuple(x + y for x, y in zip(a, b))
def _mul(a, s): return tuple(x * s for x in a)
def _dot(a, b): return sum(x * y for x, y in zip(a, b))
def _norma(a): return math.sqrt(_dot(a, a))
def _un(a): return _mul(a, 1 / _norma(a))


def pega(lado):
    """O meio da pega: no círculo em que as duas distâncias (cotovelo, pega) batem. `lado` 0 é o alto (a disputa);
    -1 cai para a nossa esquerda (nós vencemos), +1 para a esquerda de Morel (ele vence), até a pega estar a
    TAMPO_MAO do tampo."""
    A, B = COTOVELO_MOREL, COTOVELO_NOSSO
    ra, rb = ANTEBRACO_MOREL + MAO, ANTEBRACO_NOSSO + MAO
    d = _norma(_sub(B, A))
    u = _un(_sub(B, A))
    a = (ra * ra - rb * rb + d * d) / (2 * d)
    centro, r = _add(A, _mul(u, a)), math.sqrt(ra * ra - a * a)
    cima = (0.0, 1.0, 0.0)
    lado_h = _un((-u[2], 0.0, u[0]))  # horizontal, perpendicular à linha dos cotovelos: para a nossa direita e longe
    if lado == 0:
        return _add(centro, _mul(cima, r)), r
    s = math.sqrt(max(r * r - TAMPO_MAO * TAMPO_MAO, 0)) * lado
    return _add(centro, _add(_mul(cima, TAMPO_MAO), _mul(lado_h, s))), r


def poses():
    out = {}
    for nome, lado in (("disputa", 0), ("vitoria_jogador", -1), ("vitoria_morel", 1)):
        P, raio = pega(lado)
        pm = _add(COTOVELO_MOREL, _mul(_un(_sub(P, COTOVELO_MOREL)), ANTEBRACO_MOREL))
        pn = _add(COTOVELO_NOSSO, _mul(_un(_sub(P, COTOVELO_NOSSO)), ANTEBRACO_NOSSO))
        out[nome] = dict(pega=P, raio=raio, ombro_m=OMBRO_MOREL[nome], cotovelo_m=COTOVELO_MOREL, pulso_m=pm,
                         cotovelo_n=COTOVELO_NOSSO, pulso_n=pn)
    return out


def main():
    r = lambda q: tuple(round(v) for v in tela(q))  # noqa: E731
    for nome, p in poses().items():
        print(f"{nome}:")
        print(f"  Morel: ombro{r(p['ombro_m'])} cotovelo{r(p['cotovelo_m'])} pulso{r(p['pulso_m'])}"
              f"  braço {_norma(_sub(p['ombro_m'], p['cotovelo_m'])):.1f} cm / {math.dist(tela(p['ombro_m']), tela(p['cotovelo_m'])):.0f} px"
              f"  antebraço {_norma(_sub(p['cotovelo_m'], p['pulso_m'])):.1f} cm / {math.dist(tela(p['cotovelo_m']), tela(p['pulso_m'])):.0f} px")
        print(f"  nós:   cotovelo{r(p['cotovelo_n'])} pulso{r(p['pulso_n'])}"
              f"  antebraço {_norma(_sub(p['cotovelo_n'], p['pulso_n'])):.1f} cm / {math.dist(tela(p['cotovelo_n']), tela(p['pulso_n'])):.0f} px")
        print(f"  a pega{r(p['pega'])} a {p['pega'][1]:.1f} cm do tampo (o círculo tem {p['raio']:.1f} cm de raio);"
              f" das duas pontas: Morel {_norma(_sub(p['pega'], p['cotovelo_m'])):.1f}, nós {_norma(_sub(p['pega'], p['cotovelo_n'])):.1f} cm")
    print(f"o nosso braço de cima: do cotovelo {tuple(round(v) for v in tela(COTOVELO_NOSSO))} para {OMBRO_NOSSO_TELA} (fora do quadro)")


if __name__ == "__main__":
    main()
