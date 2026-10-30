"""A queda de braço no canto da taverna: a construção em números (protótipo; nada no jogo).

    python ferramentas/prototipos/taverna/morel/queda-canto/geometria.py     # as poses, as medidas e as conferências

**A câmera é a da cena do canto** (`morel/canto/espaco.py`), lida como perspectiva: o horizonte em y 22, o ponto de fuga
em x 170, a borda de lá do tampo em y 72. Com a distância focal de 140 px (a das cenas da taverna), a borda de lá fica a
110 cm e o olho 39 cm acima do tampo (um adulto sentado, debruçado sobre a mesa); a borda de baixo do quadro mostra o
tampo a 74 cm. X para a direita de quem olha, Y para cima a partir do tampo, Z a distância, em cm.

**A construção da disputa** (a referência gerada orienta a pose do meio; o movimento sai daqui, pela skill
`arte-personagens-fenda`, "Dois corpos ligados por um contato"):
- **os cotovelos ficam:** o de Morel no tampo, à frente do ombro direito dele e um pouco para dentro (`COTOVELO_MOREL`);
  o nosso, à frente do nosso ombro direito, fora do quadro, embaixo (`COTOVELO_NOSSO`: a 62 cm, ele cairia em y ~100).
  A linha entre eles corre quase em profundidade, com uns 16 cm de lado (cada um à frente do próprio ombro direito);
- **a pega** só existe onde as duas cadeias alcançam: com o antebraço e a mão de cada um de comprimento fixo, ela anda
  num círculo perpendicular à linha dos cotovelos (`circulo`); a disputa é o alto do círculo, e cada desfecho é a pega
  descendo para um lado até o dorso de quem perde tocar o tampo;
- **quem vence leva a mão do outro para a própria esquerda:** nós vencendo, a pega vai para a esquerda da imagem (a
  esquerda nossa), e o antebraço de Morel deita para lá, para fora do pão; Morel vencendo, para a direita da imagem (a
  esquerda dele), e o nosso antebraço deita para lá: é por isso que a tigela sai dali (`TIGELA`);
- **o corpo de Morel acompanha só o que o esforço pede:** o ombro direito vem com o tronco (1 px por vez, para o lado de
  quem força), o braço de cima sempre do mesmo comprimento (o ombro ajustado ao comprimento: a conferência mede o
  desvio); a cabeça olha para nós.

**A preparação** (`PREPARO`): Morel para de comer e olha para nós; solta a colher dentro da tigela; a mão esquerda dele
pega a tigela pela borda e a desliza para a direita, sempre encostada nela, e fica no tampo ao lado; o braço da colher
vai ao meio da mesa, com o cotovelo no tampo e a mão aberta no alto; o nosso antebraço entra pela borda de baixo até a
mão dele."""
import math

F, CX, HOR, ALTURA = 140.0, 170.0, 22.0, 39.0


def tela(p):
    x, y, z = p
    return (CX + F * x / z, HOR + F * (ALTURA - y) / z)


def mundo(s, z):
    """O ponto a `z` de distância que cai em `s` na tela."""
    return ((s[0] - CX) * z / F, ALTURA - (s[1] - HOR) * z / F, z)


def no_tampo(s):
    """O ponto do tampo (Y 0) que cai em `s` na tela."""
    z = F * ALTURA / (s[1] - HOR)
    return ((s[0] - CX) * z / F, 0.0, z)


def _sub(a, b): return tuple(x - y for x, y in zip(a, b))
def _add(a, b): return tuple(x + y for x, y in zip(a, b))
def _mul(a, s): return tuple(x * s for x in a)
def _dot(a, b): return sum(x * y for x, y in zip(a, b))
def _norma(a): return math.sqrt(_dot(a, a))
def _un(a): return _mul(a, 1 / _norma(a))
def _lerp(a, b, t): return tuple(x + (y - x) * t for x, y in zip(a, b))


ALTURA_JUNTA = 4.0                          # a junta do cotovelo acima do tampo (o osso, a pele, a manga)
COTOVELO_MOREL = (-16.0, ALTURA_JUNTA, 106.0)
COTOVELO_NOSSO = (10.0, ALTURA_JUNTA, 58.0)
ANTEBRACO_MOREL, ANTEBRACO_NOSSO, MAO = 30.0, 27.0, 6.0
TAMPO_MAO = 4.5                             # a pega quando o dorso de quem perde toca o tampo (o meio do punho)
MEIA_PEGA = 2.4                             # do meio da pega ao meio de cada mão (as palmas encostadas)
Z_OMBRO = 122.0                             # a profundidade dos ombros de Morel (debruçado sobre a mesa)
OMBRO_TELA = (138, 44)                      # a junta do ombro direito dele na tela (a da conversa)


def circulo():
    """O centro, o raio, o eixo de cima e o do lado (para a direita da imagem) do círculo da pega."""
    A, B = COTOVELO_MOREL, COTOVELO_NOSSO
    ra, rb = ANTEBRACO_MOREL + MAO, ANTEBRACO_NOSSO + MAO
    d = _norma(_sub(B, A))
    u = _un(_sub(B, A))
    a = (ra * ra - rb * rb + d * d) / (2 * d)
    centro, r = _add(A, _mul(u, a)), math.sqrt(ra * ra - a * a)
    lado = _un((-u[2], 0.0, u[0]))
    if lado[0] < 0:
        lado = _mul(lado, -1)
    return centro, r, (0.0, 1.0, 0.0), lado, d


def fi_fim():
    centro, r, *_ = circulo()
    return math.acos((TAMPO_MAO - centro[1]) / r)


def pose(fi, tronco=(0, 0)):
    """As juntas com a pega no ângulo `fi` (0 no alto; negativo para a esquerda da imagem, nós vencendo) e o tronco de
    Morel deslocado `tronco` px na tela."""
    centro, r, cima, lado, _ = circulo()
    P = _add(centro, _add(_mul(cima, r * math.cos(fi)), _mul(lado, r * math.sin(fi))))
    T = _add(_mul(cima, -math.sin(fi)), _mul(lado, math.cos(fi)))   # da mão dele para a nossa (no plano da pega)
    Pm, Pn = _sub(P, _mul(T, MEIA_PEGA)), _add(P, _mul(T, MEIA_PEGA))
    E, N = COTOVELO_MOREL, COTOVELO_NOSSO
    pm = _add(E, _mul(_un(_sub(Pm, E)), ANTEBRACO_MOREL))
    pn = _add(N, _mul(_un(_sub(Pn, N)), ANTEBRACO_NOSSO))
    S0 = mundo((OMBRO_TELA[0] + tronco[0], OMBRO_TELA[1] + tronco[1]), Z_OMBRO)
    return dict(fi=fi, pega=P, mao_m=Pm, mao_n=Pn, lado_t=T, ombro_m=S0, cotovelo_m=E, pulso_m=pm, cotovelo_n=N,
                pulso_n=pn, braco_m=_norma(_sub(S0, E)),
                tela=dict(S=tela(S0), E=tela(E), W=tela(pm), P=tela(P), En=tela(N), Wn=tela(pn),
                          Mm=tela(Pm), Mn=tela(Pn), contato_m=tela((E[0], 0.0, E[2]))))


def main():
    centro, r, _, lado, d = circulo()
    print(f"cotovelos a {d:.1f} cm; a pega: centro {tuple(round(v, 1) for v in centro)}, raio {r:.1f}; "
          f"o fim a {math.degrees(fi_fim()):.0f}° do alto; o lado {tuple(round(v, 2) for v in lado)}")
    for nome, fi in (("disputa", 0.0), ("nós vencemos", -fi_fim()), ("Morel vence", fi_fim())):
        p = pose(fi)
        t = {k: tuple(round(v) for v in q) for k, q in p["tela"].items()}
        print(f"{nome:13s} S{t['S']} E{t['E']} W{t['W']} P{t['P']} Wn{t['Wn']} En{t['En']} contato{t['contato_m']}"
              f"  braço de cima {p['braco_m']:.1f} cm  pega a {p['pega'][1]:.1f} cm")
    print("a borda de lá (y 72) a", round(F * ALTURA / 50), "cm; a de baixo do quadro (y 96) a", round(F * ALTURA / 74))


if __name__ == "__main__":
    main()
