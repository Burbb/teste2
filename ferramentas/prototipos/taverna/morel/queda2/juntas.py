"""A queda de braço diante de Morel, segunda proposta: a vista de detalhe e as juntas das três poses (protótipo).

    python ferramentas/prototipos/taverna/morel/queda2/juntas.py      # a tabela das juntas e as conferências

A primeira proposta (morel/queda/) usava a câmera da conversa: a ação pequena, a pega numa massa só, e os desfechos
indo para longe da câmera e para perto dela (escorço nos dois). Fica como histórico.

**As referências reais** (as regras e a mesa da WAF, World Armwrestling Federation; 30/10/2026):
- a mesa de 91 × 66 cm; as almofadas dos cotovelos, de 18 cm, a 5 cm de cada borda de cá e de lá, quase alinhadas
  (sobrepostas um pouco à direita do meio, numa mesa de braço direito): os cotovelos ficam a uns 38 cm um do outro, na
  direção de quem está sentado para quem está do outro lado;
- a pega é palma com palma, os polegares cruzados em cima e o nó do polegar à vista, os punhos retos no começo;
- o cotovelo não sai da almofada; a mão perdedora tem de chegar à altura da almofada de toque, que fica à esquerda de
  quem vence (numa queda de braço direito), na lateral do cotovelo dele: quem vence leva a mão do outro para a própria
  esquerda, de lado, não para longe nem para perto.
Daí a câmera: os dois desfechos correm de lado (oeste e leste), então uma vista de três quartos, do lado de cá e à
nossa direita (sudeste), um pouco acima do tampo, mostra os dois para os lados do quadro, e o braço de quem perde
fica deitado e comprido no tampo, atravessado na frente da câmera.

**O espaço** (cm): o tampo em y = 0, x para leste (a nossa direita), z para o norte (Morel); a origem no meio da mesa.
**A câmera** é de detalhe (cinematográfica: não são os nossos olhos): 50° a leste do nosso lado, 30° acima do tampo,
a 170 cm da pega; perto de 2 px por cm na pega (a conversa tem 0,9). Com menos giro, os dois antebraços se alinham na
profundidade e um esconde o outro na disputa; com mais, o tampo vira um losango no canto e sobra fundo vazio. O nosso
ombro fica na borda da esquerda (o tronco, fora do quadro); a cabeça de Morel, acima da borda de cima: dele se vê o
peito (o colete vermelho com as fivelas, o couro, a ombreira do ombro esquerdo, o punho da espada atrás do direito). A disputa fica no terço esquerdo do quadro (a pega em PEGA_TELA): o
dado dos testes aparece no meio do palco (na arte, x 100 a 220 a partir de y 63 a 1920×945; x 70 a 250 a partir de
y 45 a 1280×720) e não pode cobrir a pega enquanto rola.

**As juntas:** os cotovelos parados nas almofadas; os antebraços (do cotovelo ao meio da pega: Morel 34 cm, nós 33) só
alcançam a pega num círculo no plano que corta ao meio a linha dos cotovelos; no alto a disputa, nos lados os fins,
com a mão perdedora a 5 cm do tampo (o dorso no tampo, a mão de quem vence por cima). Os ombros participam: na
disputa os dois se inclinam sobre a mesa, o ombro atrás da mão; quem vence rola o ombro por cima do braço para o lado
da vitória; quem perde é puxado para o mesmo lado, o ombro desce. O braço de cima tem 30 cm (± 1) em todas as poses."""
import math

# ------------------------------------------------------------------ o espaço e a câmera
COTOVELO_NOSSO = (-15.0, 0.0, -19.0)
COTOVELO_MOREL = (-21.0, 0.0, 19.0)
PEGA_NOSSA, PEGA_MOREL = 33.0, 34.0          # do cotovelo ao meio da pega
ANTEBRACO = {"nos": 27.0, "morel": 28.0}     # do cotovelo ao pulso
TAMPO_MAO = 5.0                              # a altura do meio da pega quando o dorso da mão perdedora toca o tampo
BRACO = 30.0                                 # do ombro ao cotovelo
# os ombros direitos em cada pose (o tronco vai junto, pela direção dos ombros: TRONCO_MOREL)
OMBRO_MOREL = {"disputa": (-24.0, 24.0, 35.0), "vitoria_jogador": (-30.0, 20.0, 34.0), "vitoria_morel": (-17.0, 21.0, 31.0)}
OMBRO_NOSSO = {"disputa": (-22.0, 26.0, -46.0), "vitoria_jogador": (-29.0, 23.0, -43.0), "vitoria_morel": (-15.0, 22.0, -47.0)}
# o ombro esquerdo de Morel (o tronco é a linha entre os dois ombros, descendo até o assento): na disputa, de frente;
# perdendo, o tronco gira e o ombro esquerdo vai para trás; vencendo, ele se debruça e o esquerdo acompanha
OMBRO_ESQ_MOREL = {"disputa": (16.0, 26.0, 41.0), "vitoria_jogador": (10.0, 22.0, 45.0), "vitoria_morel": (21.0, 22.0, 36.0)}

# a mesa (a da conversa): 70 cm de fundo (z de -33 a 33), comprida para o oeste; a ponta de leste, com a quina, uns
# 20 cm à direita da pega (na conversa, a quina perto do pão). Os cotovelos ficam 15 cm a oeste do eixo, diante do
# peito de Morel (onde o braço da colher dele trabalha), e os dois derrubes cabem no tampo.
MESA_X = (-170.0, 20.0)
# a tigela: Morel a desliza com a mão da colher para a direita dele (oeste), num empurrão pela metade de lá, além da
# coluna da vela, até longe dos dois derrubes (na vista de detalhe, ela fica no canto de cima à esquerda); o pão fica embaixo do quadro, a vela e a caneca à esquerda, fora dele. Depois, ele a puxa de
# volta pelo mesmo caminho. A mão esquerda de Morel agarra a borda de lá (numa mesa oficial se agarra o pino).
TIGELA = (-118.0, 0.0, 22.0)   # o centro, no tampo (na conversa ela ficava em (-6, 0, 1))
TIGELA_RAIO = 17.0
MAO_ESQ_MOREL = {"disputa": (9.0, 0.0, 33.0), "vitoria_jogador": (7.0, 0.0, 33.0), "vitoria_morel": (10.0, 0.0, 32.0)}

TEMA = 50.0   # graus a leste do nosso lado
ELEVA = 30.0  # graus acima do tampo
DIST = 170.0  # da câmera ao alvo
FOCO = 320.0  # px
ALVO = (0.0, 14.0, 0.0)
PEGA_TELA = (76.0, 21.0)  # onde a pega da disputa cai no quadro: no terço esquerdo, no alto (fora do dado)


def _sub(a, b): return tuple(x - y for x, y in zip(a, b))
def _add(a, b): return tuple(x + y for x, y in zip(a, b))
def _mul(a, s): return tuple(x * s for x in a)
def _dot(a, b): return sum(x * y for x, y in zip(a, b))
def _norma(a): return math.sqrt(_dot(a, a))
def _un(a): return _mul(a, 1 / _norma(a))
def _cruz(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


_t, _e = math.radians(TEMA), math.radians(ELEVA)
CAMERA = _add(ALVO, _mul((math.sin(_t) * math.cos(_e), math.sin(_e), -math.cos(_t) * math.cos(_e)), DIST))
_FRENTE = _un(_sub(ALVO, CAMERA))
_DIREITA = _un(_cruz((0.0, 1.0, 0.0), _FRENTE))  # o espaço tem z para o norte: a direita da tela é cima × frente
_CIMA = _cruz(_FRENTE, _DIREITA)


def _bruta(p):
    v = _sub(p, CAMERA)
    z = _dot(v, _FRENTE)
    return (FOCO * _dot(v, _DIREITA) / z, -FOCO * _dot(v, _CIMA) / z, z)


def tela(p):
    """Do espaço para a tela (x, y em px; e a profundidade, em cm); o quadro põe a pega da disputa em PEGA_TELA."""
    x, y, z = _bruta(p)
    return (x + _DESLOCA[0], y + _DESLOCA[1], z)


def escala(p):
    """Quantos px um cm tem nesse ponto (pela distância)."""
    return FOCO / _dot(_sub(p, CAMERA), _FRENTE)


# ------------------------------------------------------------------ a pega e as poses
def pega(lado):
    """O meio da pega: `lado` 0 é o alto (a disputa); -1 é a nossa vitória (a mão de Morel a oeste, a nossa esquerda);
    +1 é a dele (a nossa a leste, a esquerda dele), com a mão perdedora a TAMPO_MAO do tampo."""
    A, B = COTOVELO_NOSSO, COTOVELO_MOREL
    d = _norma(_sub(B, A))
    u = _un(_sub(B, A))
    a = (PEGA_NOSSA ** 2 - PEGA_MOREL ** 2 + d * d) / (2 * d)
    centro, r = _add(A, _mul(u, a)), math.sqrt(PEGA_NOSSA ** 2 - a * a)
    oeste = _un((-u[2], 0.0, u[0]))
    if oeste[0] > 0:
        oeste = _mul(oeste, -1)
    if lado == 0:
        return _add(centro, (0.0, r, 0.0)), r
    s = math.sqrt(r * r - TAMPO_MAO ** 2)
    return _add(centro, _add((0.0, TAMPO_MAO, 0.0), _mul(oeste, s if lado < 0 else -s))), r


POSES = {"disputa": 0, "vitoria_jogador": -1, "vitoria_morel": 1}
_p0 = _bruta(pega(0)[0])
_DESLOCA = (PEGA_TELA[0] - _p0[0], PEGA_TELA[1] - _p0[1])


def _ombro(cotovelo, ombro):
    """O ombro na direção dada, a BRACO do cotovelo (o braço de cima não estica nem encolhe)."""
    return _add(cotovelo, _mul(_un(_sub(ombro, cotovelo)), BRACO))


def poses():
    out = {}
    for nome, lado in POSES.items():
        P, r = pega(lado)
        pm = _add(COTOVELO_MOREL, _mul(_un(_sub(P, COTOVELO_MOREL)), ANTEBRACO["morel"]))
        pn = _add(COTOVELO_NOSSO, _mul(_un(_sub(P, COTOVELO_NOSSO)), ANTEBRACO["nos"]))
        out[nome] = dict(pega=P, raio=r, ombro_m=_ombro(COTOVELO_MOREL, OMBRO_MOREL[nome]), ombro_esq_m=OMBRO_ESQ_MOREL[nome],
                         cotovelo_m=COTOVELO_MOREL, pulso_m=pm, ombro_n=_ombro(COTOVELO_NOSSO, OMBRO_NOSSO[nome]),
                         cotovelo_n=COTOVELO_NOSSO,
                         pulso_n=pn)
    return out


# a área do dado na arte (as duas janelas): a pega da disputa não pode cair nela
DADO = {"1920×945": (100, 63, 220, 150), "1280×720": (70, 45, 250, 175)}


def main():
    r = lambda q: tuple(round(v) for v in tela(q)[:2])  # noqa: E731
    for nome, p in poses().items():
        print(f"{nome}:")
        for quem, S, E, W in (("Morel", "ombro_m", "cotovelo_m", "pulso_m"), ("nós", "ombro_n", "cotovelo_n", "pulso_n")):
            print(f"  {quem:5s} ombro{r(p[S])} cotovelo{r(p[E])} pulso{r(p[W])}"
                  f"  braço {_norma(_sub(p[S], p[E])):.1f} cm / {math.dist(r(p[S]), r(p[E])):.0f} px"
                  f"  antebraço {_norma(_sub(p[E], p[W])):.1f} cm / {math.dist(r(p[E]), r(p[W])):.0f} px")
        print(f"  a pega{r(p['pega'])} a {p['pega'][1]:.1f} cm do tampo; das pontas: Morel "
              f"{_norma(_sub(p['pega'], p['cotovelo_m'])):.1f}, nós {_norma(_sub(p['pega'], p['cotovelo_n'])):.1f} cm;"
              f" {escala(p['pega']):.2f} px/cm")
    x, y = r(pega(0)[0])
    for jan, (x0, y0, x1, y1) in DADO.items():
        print(f"o dado a {jan}: a pega da disputa ({x}, {y}) {'FORA' if not (x0 <= x <= x1 and y >= y0) else 'DENTRO'} da área dele")


if __name__ == "__main__":
    main()
