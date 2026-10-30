"""A queda de braço na vista aprovada (o "queda 1" refinado): a construção em números (protótipo; nada no jogo).

    python ferramentas/prototipos/taverna/morel/queda-vista/geometria.py      # as poses, as conferências e o ciclo

**A câmera** é a da vista aprovada e a do queda 1 (`morel/queda/juntas.py`: f = 140 px, o eixo em x 238, o horizonte
em y 30, 33 cm acima do tampo; X para a direita de quem olha, Y para cima a partir do tampo, z a distância). A sala, a
mesa e a identidade de Morel ficam como foram aprovadas; a postura dele, não: a disputa começa no corpo.

**A postura de origem** (a revisão do Jean, 30/10/2026: na candidata anterior, Morel continuava na postura da conversa
e o nosso braço atravessava a mesa para alcançá-lo; os números de antes partiam dessa postura e não valem mais):
- **Morel se debruça.** O tronco desce e vem para o meio (`TRONCO`, 2 px para a direita e 3 para baixo na disputa) e a
  cabeça desce mais (2 px além do tronco: de frente, um debruçar se lê pelo pescoço que encurta). O ombro direito vem
  junto: fica onde o tronco o põe (a 134 cm, 8 à frente da conversa) e, com o braço de cima de 31 cm até o tampo, o
  cotovelo cai à frente do meio do tronco dele (`COTOVELO_MOREL`), como as referências de queda de braço pedem (o
  cotovelo à frente do corpo, centrado; o ombro um pouco à frente).
- **Nós, colados ao apoio.** O nosso cotovelo à frente do nosso peito, a 3 cm da nossa borda (`COTOVELO_NOSSO`); o
  braço de cima desce quase reto para fora do quadro (o ombro logo atrás e abaixo do cotovelo). Com esta câmera (a 74
  cm da borda), o nosso ombro de verdade cairia dentro do quadro e obrigaria a mostrar o tronco por cima da mesa: o
  braço que desce reto é o que diz "estamos na mesa" sem mudar a cena.
- **O encontro no meio do tampo:** os cotovelos a 45 cm; a pega no plano entre eles (no meio da mesa em profundidade e
  entre os dois corpos), logo abaixo do queixo de Morel debruçado. Com o olho 33 cm acima do tampo, uma pega na altura
  de verdade (~28 cm) cai na linha do queixo dele: é por isso que ele precisa se debruçar (a cabeça desce) e por que
  os cotovelos não ficam mais perto (a pega subiria para o rosto).
- **Os dois desfechos com os apoios parados** (o arraste do cotovelo da candidata anterior saiu): a linha dos
  cotovelos corre quase na direção da câmera (22° de lado), então os dois fins correm para os lados: na nossa
  vitória, o antebraço dele deita para a esquerda e aparece acima do nosso; na nossa derrota, o nosso deita para a
  direita (a mesa ficou livre: o pão saiu dali) e gira com a palma para cima (`SUPINA`, o "press" das referências:
  quem vence põe o corpo por cima e a palma de quem perde termina virada para o teto), mostrando a face interna.

**O corpo participa** (pela `arte-personagens-fenda`, passo 6, e o Jean: "não é só o membro que se move que mexe"):
conduzem as mãos e os antebraços; o tronco e a cabeça de Morel acompanham o esforço pose a pose (`TRONCO`: pendem
para o lado de quem força, cedem quando ele perde, vêm por cima quando ele vence) e o ombro dele vai junto, com o
braço de cima sempre de 31 cm (o ombro é o do tronco, ajustado ao comprimento; a conferência mede o desvio); o nosso
ombro, fora do quadro, entra quando empurramos e é puxado quando perdemos (`OMBRO_NOSSO`); os cotovelos, o quadril,
a cadeira e a mesa ficam.

**O tempo** (`CICLO`, 100 ms o tique): Morel se ajeita e se debruça enquanto a pega se firma; a disputa com intenção
(quem perde ganha um pouco primeiro e segura, o outro recupera); o derrube devagar no começo e acelerando até o tampo;
o impacto curto (o tronco de Morel cede 1 px) e a pausa no fim."""
import math

F, CX, HOR, ALTURA = 140.0, 238.0, 30.0, 33.0  # a câmera da vista, a mesma do queda 1 (morel/queda/juntas.py)


def tela(p):
    x, y, z = p
    return (CX + F * x / z, HOR + F * (ALTURA - y) / z)


def mundo(s, z):
    """O ponto do espaço a `z` de distância que cai em `s` na tela."""
    return ((s[0] - CX) * z / F, ALTURA - (s[1] - HOR) * z / F, z)


ALTURA_JUNTA = 4.0                    # a junta do cotovelo acima do tampo (o osso sobre a pele e a manga)
COTOVELO_MOREL = (-19.2, ALTURA_JUNTA, 119.6)
COTOVELO_NOSSO = (-2.0, ALTURA_JUNTA, 78.0)
BRACO_MOREL = 31.0                    # do ombro ao cotovelo
ANTEBRACO_MOREL, ANTEBRACO_NOSSO, MAO = 28.0, 27.0, 6.0  # do cotovelo ao pulso; do pulso ao meio da pega
TAMPO_MAO = 4.0                        # a pega quando o dorso da mão de quem perde toca o tampo (o meio do punho)
MEIA_PEGA = 2.4                        # do meio da pega ao meio de cada mão (as palmas encostadas)
OMBRO_OLHA = (198, 35)                 # o ombro direito de Morel na vista aprovada (a pose `olha`)
Z_OMBRO = 134.0                        # a profundidade do ombro dele debruçado (na conversa, 142)
# o nosso ombro, fora do quadro, embaixo do cotovelo: na disputa, logo atrás; quando empurramos (vencemos), entra para
# a esquerda; quando perdemos, é puxado para a direita (a tela; só a direção do braço de cima aparece)
OMBRO_NOSSO = {0: (10.0, 132.0), -1: (3.0, 130.0), 1: (8.0, 130.0)}


def _sub(a, b): return tuple(x - y for x, y in zip(a, b))
def _add(a, b): return tuple(x + y for x, y in zip(a, b))
def _mul(a, s): return tuple(x * s for x in a)
def _dot(a, b): return sum(x * y for x, y in zip(a, b))
def _norma(a): return math.sqrt(_dot(a, a))
def _un(a): return _mul(a, 1 / _norma(a))
def _lerp(a, b, t): return tuple(x + (y - x) * t for x, y in zip(a, b))


def circulo():
    """O centro, o raio e os dois eixos (para cima; para o lado em que Morel vence) do círculo da pega."""
    A, B = COTOVELO_MOREL, COTOVELO_NOSSO
    ra, rb = ANTEBRACO_MOREL + MAO, ANTEBRACO_NOSSO + MAO
    d = _norma(_sub(B, A))
    u = _un(_sub(B, A))
    a = (ra * ra - rb * rb + d * d) / (2 * d)
    centro, r = _add(A, _mul(u, a)), math.sqrt(ra * ra - a * a)
    lado = _un((-u[2], 0.0, u[0]))  # horizontal, perpendicular à linha dos cotovelos: para a direita
    return centro, r, (0.0, 1.0, 0.0), lado, d


def fi_fim():
    """O ângulo em que a pega chega a TAMPO_MAO do tampo (o fim, para os dois lados)."""
    centro, r, *_ = circulo()
    return math.acos((TAMPO_MAO - centro[1]) / r)


def pose(fi, tronco, lado_n=0, t_n=0.0):
    """As juntas com a pega no ângulo `fi` (0 no alto) e o tronco de Morel deslocado `tronco` (px na tela, a partir da
    vista aprovada). O ombro dele é o do tronco (a `Z_OMBRO`), levado ao comprimento do braço de cima; `lado_n` e
    `t_n` dizem para onde e quanto o nosso ombro foi."""
    centro, r, cima, lado, _ = circulo()
    P = _add(centro, _add(_mul(cima, r * math.cos(fi)), _mul(lado, r * math.sin(fi))))
    # as palmas se encostam no meio da pega: cada mão do seu lado dela (T vai da mão dele para a nossa), e cada
    # antebraço aponta para a sua mão, não para o meio
    T = _add(_mul(cima, -math.sin(fi)), _mul(lado, math.cos(fi)))
    Pm, Pn = _sub(P, _mul(T, MEIA_PEGA)), _add(P, _mul(T, MEIA_PEGA))
    E, N = COTOVELO_MOREL, COTOVELO_NOSSO
    pm = _add(E, _mul(_un(_sub(Pm, E)), ANTEBRACO_MOREL))
    pn = _add(N, _mul(_un(_sub(Pn, N)), ANTEBRACO_NOSSO))
    S0 = mundo((OMBRO_OLHA[0] + tronco[0], OMBRO_OLHA[1] + tronco[1]), Z_OMBRO)
    S = _add(E, _mul(_un(_sub(S0, E)), BRACO_MOREL))
    en = tela(N)
    on = _lerp(OMBRO_NOSSO[0], OMBRO_NOSSO[lado_n], t_n) if lado_n else OMBRO_NOSSO[0]
    return dict(fi=fi, pega=P, mao_m=Pm, mao_n=Pn, lado_t=T, ombro_m=S, cotovelo_m=E, pulso_m=pm, cotovelo_n=N,
                pulso_n=pn, desvio_ombro=math.dist(tela(S), tela(S0)),
                tela=dict(S=tela(S), E=tela(E), W=tela(pm), P=tela(P), En=en, Wn=tela(pn),
                          Sn=(en[0] + on[0], on[1]), contato_m=tela((E[0], 0.0, E[2])),
                          contato_n=tela((N[0], 0.0, N[2]))))


# ------------------------------------------------------------------ as poses e o ciclo
# Cada pose: (nome, fração do caminho até o fim, lado, o tronco de Morel (dx, dy na tela), a cabeça além do tronco,
# as mãos fechadas). O lado -1 é nós vencendo, +1 Morel vencendo (na disputa, só para onde a pega pende). O tronco: na
# conversa (0, 0); ajeitando-se (1, 1); debruçado na disputa (2, 3); pende 1 px para o lado de quem força; cede para a
# direita dele (a nossa esquerda) e desce quando perde; vem por cima quando vence: o ombro passa sobre o cotovelo (para o
# meio e um pouco para cima: com o braço de cima de 31 cm, descer o afastaria do ombro do tronco) e a cabeça desce sobre
# a pega.
POSES = [
    ("firma", 0.00, 1, (1, 1), 1, False),
    ("disputa", 0.00, 1, (2, 3), 2, True),
    ("pende_m1", 0.035, 1, (3, 3), 2, True),
    ("pende_m2", 0.07, 1, (3, 4), 2, True),
    ("pende_n1", 0.035, -1, (2, 3), 2, True),
    ("pende_n2", 0.07, -1, (1, 3), 2, True),
    ("nos_1", 0.12, -1, (1, 3), 2, True), ("nos_2", 0.20, -1, (1, 4), 2, True), ("nos_3", 0.32, -1, (0, 4), 2, True),
    ("nos_4", 0.48, -1, (0, 4), 2, True), ("nos_5", 0.68, -1, (-1, 5), 2, True), ("nos_6", 0.88, -1, (-1, 5), 2, True),
    ("nos_impacto", 1.0, -1, (-1, 6), 2, True), ("nos_fim", 1.0, -1, (-1, 5), 2, True),
    ("morel_1", 0.12, 1, (3, 3), 2, True), ("morel_2", 0.20, 1, (3, 3), 2, True), ("morel_3", 0.32, 1, (4, 3), 3, True),
    ("morel_4", 0.48, 1, (4, 3), 3, True), ("morel_5", 0.68, 1, (5, 2), 4, True), ("morel_6", 0.88, 1, (5, 2), 4, True),
    ("morel_impacto", 1.0, 1, (5, 3), 4, True), ("morel_fim", 1.0, 1, (5, 2), 4, True),
]

# A linha do tempo de cada desfecho (pose, tiques de 100 ms). Morel se ajeita e se debruça enquanto a pega se firma; a
# disputa tem intenção: quem perde começa ganhando um pouco (a pega pende para o lado dele e segura), o outro recupera,
# a pega passa do meio; as poses seguram de 3 a 8 tiques, a pega anda 1 a 2 px de cada vez. O derrube começa devagar (2
# e 3 tiques) e acelera até o tampo (1 tique cada); o impacto, 2; a pausa no fim, 2,8 s.
_DISPUTA = {
    "nos": [("firma", 8), ("disputa", 6), ("pende_m1", 3), ("pende_m2", 8), ("pende_m1", 4), ("disputa", 3),
            ("pende_n1", 3), ("pende_n2", 6), ("pende_n1", 4), ("disputa", 5)],
    "morel": [("firma", 8), ("disputa", 6), ("pende_n1", 3), ("pende_n2", 8), ("pende_n1", 4), ("disputa", 3),
              ("pende_m1", 3), ("pende_m2", 6), ("pende_m1", 4), ("disputa", 5)],
}
_DERRUBE = {
    "nos": [("pende_n1", 2), ("pende_n2", 3), ("nos_1", 2), ("nos_2", 2), ("nos_3", 1), ("nos_4", 1), ("nos_5", 1),
            ("nos_6", 1), ("nos_impacto", 2), ("nos_fim", 28)],
    "morel": [("pende_m1", 2), ("pende_m2", 3), ("morel_1", 2), ("morel_2", 2), ("morel_3", 1), ("morel_4", 1),
              ("morel_5", 1), ("morel_6", 1), ("morel_impacto", 2), ("morel_fim", 28)],
}
CICLO = {k: _DISPUTA[k] + _DERRUBE[k] for k in _DISPUTA}
# movimento reduzido: a pose do meio enquanto dura a disputa e a pose final depois, sem passagens, tremida nem impacto
REDUZIDO = {k: [("disputa", sum(n for _, n in _DISPUTA[k])), (f"{k}_fim", sum(n for _, n in _DERRUBE[k]))]
            for k in _DISPUTA}


def supina(nome, f):
    """O quanto o nosso antebraço já girou com a palma para cima (0 a 1): só quando perdemos, a partir de um quinto do
    derrube (quem vence põe o corpo por cima e vira a nossa mão), devagar no começo."""
    if not nome.startswith("morel_"):
        return 0.0
    s = min(1.0, max(0.0, (f - 0.2) / 0.8))
    return s * s * (3 - 2 * s)


def todas():
    out = {}
    for nome, f, lado, tronco, cabeca, firme in POSES:
        derrube = nome.startswith(("nos_", "morel_"))
        p = pose(lado * f * fi_fim(), tronco, lado if derrube else 0, f if derrube else 0.0)
        out[nome] = dict(p, firme=firme, tronco=tronco, cabeca=cabeca, supina=supina(nome, f))
    return out


def main():
    centro, r, _, lado, d = circulo()
    print(f"cotovelos a {d:.1f} cm; o círculo da pega: centro {tuple(round(v, 1) for v in centro)}, raio {r:.1f} cm;"
          f" o fim a {math.degrees(fi_fim()):.0f}° do alto")
    print(f"contatos dos cotovelos na tela: Morel {tuple(round(v) for v in pose(0, (2, 3))['tela']['contato_m'])},"
          f" nós {tuple(round(v) for v in pose(0, (2, 3))['tela']['contato_n'])}")
    ant = None
    for nome, p in todas().items():
        t = {k: tuple(round(v) for v in q) for k, q in p["tela"].items()}
        braco = _norma(_sub(p["ombro_m"], p["cotovelo_m"]))
        am = _norma(_sub(p["pulso_m"], p["cotovelo_m"]))
        an = _norma(_sub(p["pulso_n"], p["cotovelo_n"]))
        anda = "" if ant is None else f"  anda: pega {math.dist(ant['P'], p['tela']['P']):.1f} px"
        print(f"{nome:13s} tronco{p['tronco']} S{t['S']} (desvio {p['desvio_ombro']:.1f}) E{t['E']} W{t['W']} P{t['P']}"
              f" Wn{t['Wn']} En{t['En']}  braço {braco:.1f} antebraços {am:.1f}/{an:.1f} cm  pega a {p['pega'][1]:.1f}"
              f" cm  supina {p['supina']:.2f}{anda}")
        ant = p["tela"]


if __name__ == "__main__":
    main()
