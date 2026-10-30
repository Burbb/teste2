"""A pega construída com formas simples (protótipo): os punhos, os dedos e os polegares no mesmo espaço dos braços.

Pela referência (as regras da WAF): palma com palma, os polegares cruzados em cima, o nó do polegar à vista, os punhos
retos na disputa. Os cotovelos ficam quase alinhados (o nosso um pouco a leste), então a nossa mão fica do lado de
leste da pega, de dorso para leste, e a de Morel do lado de oeste, de dorso para oeste; os dedos de cada um dobram
sobre o dorso da mão do outro. A câmera (a sudeste) vê o nosso dorso com os dedos de Morel por cima, os polegares e
a mão dele atrás. Nos derrubes, quem perde fica com o dorso da mão no tampo (a palma para cima, os dedos dobrados por
cima da mão do outro) e quem vence fecha o punho por cima, o polegar por cima.

Isto é a construção: o estudo mostra as partes em cores, e a pega da cena (poses.PEGAS) é desenhada à mão em cima
dela, simplificada (o dorso, os dedos em duas ou três listras, os polegares)."""
import juntas as J
import desenho as D

PARTES = ["nossa_mao", "nossos_dedos", "nosso_polegar", "mao_morel", "dedos_morel", "polegar_morel"]


def dono(parte):
    """De quem é a parte ("nos" ou "morel"), com ou sem o número do dedo."""
    return "nos" if parte.startswith("nos") else "morel"


def separar(t):
    """O acabamento da pega pelo valor, não pelo contorno: onde uma parte encosta noutra que está mais perto da câmera
    (a mão do outro, outro dedo, o polegar por cima), o pixel de trás vira a sombra da pele dele, um pixel só. É o que
    separa as duas mãos (que têm tons de pele parecidos) e conta os dedos."""
    escurecer = []
    for (x, y), parte in t.camada.items():
        if parte.split(":")[0] not in PARTES:
            continue
        for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            outra = t.camada.get(q)
            if outra and outra != parte and outra.split(":")[0] in PARTES and t.prof[q] < t.prof[(x, y)] - 0.3:
                escurecer.append(((x, y), parte, dono(outra) != dono(parte)))
                break
    return escurecer


def _eixos(a1, ref):
    a1 = J._un(a1)
    a2 = J._un(J._sub(ref, J._mul(a1, J._dot(ref, a1))))
    return a1, a2, J._cruz(a1, a2)


def construir(t, nome, cor):
    """Desenha as mãos da pose `nome` na tela `t`; `cor(parte, normal)` dá a cor."""
    p = J.poses()[nome]
    P = p["pega"]
    fn = J._un(J._sub(P, p["cotovelo_n"]))
    fm = J._un(J._sub(P, p["cotovelo_m"]))
    up = (0.0, 1.0, 0.0)

    def punho(parte, centro, a1, ref, semi):
        D.elipsoide(t, parte, centro, _eixos(a1, ref), semi, lambda n, l, parte=parte: cor(parte, n))

    def dedo(parte, a, b, r):
        D.capsula(t, parte, a, b, r, r, lambda n, t_, c, parte=parte: cor(parte, n), passo=0.25)

    if nome == "disputa":
        Pn = J._add(P, (2.0, -0.5, -1.5))
        Pm = J._add(P, (-2.0, -0.5, 1.5))
        punho("nossa_mao", Pn, fn, (1.0, 0.0, 0.0), (5.0, 3.0, 4.3))
        punho("mao_morel", Pm, fm, (-1.0, 0.0, 0.0), (5.2, 3.1, 4.5))
        # os dedos de Morel dobrados sobre o nosso dorso (a face de leste, à vista), os nossos sobre o dele (oeste)
        for k, dy in enumerate((2.6, 0.6, -1.4, -3.2)):
            dedo(f"dedos_morel:{k}", J._add(Pn, (3.2, dy, 2.6)), J._add(Pn, (3.6, dy - 0.6, -1.2 + k * 0.3)), 0.95)
            dedo(f"nossos_dedos:{k}", J._add(Pm, (-3.2, dy, -2.6)), J._add(Pm, (-3.6, dy - 0.6, 1.2)), 0.9)
        # os polegares cruzados em cima: o nosso por cima do dele
        dedo("polegar_morel", J._add(P, (-1.6, 4.2, 2.2)), J._add(P, (1.8, 5.2, -0.6)), 1.3)
        dedo("nosso_polegar", J._add(P, (1.8, 4.8, -2.2)), J._add(P, (-1.6, 6.0, 0.8)), 1.25)
        return
    # os derrubes: quem perde, de dorso no tampo; quem vence, o punho fechado por cima
    perde, vence = ("mao_morel", "nossa_mao") if nome == "vitoria_jogador" else ("nossa_mao", "mao_morel")
    fp, fv = (fm, fn) if nome == "vitoria_jogador" else (fn, fm)
    dp = "dedos_morel" if perde == "mao_morel" else "nossos_dedos"
    pv = "nosso_polegar" if vence == "nossa_mao" else "polegar_morel"
    pp = "polegar_morel" if perde == "mao_morel" else "nosso_polegar"
    deitada = J._un((fp[0], 0.0, fp[2]))
    # para a mão presa aparecer, ela fica um pouco mais perto da câmera que o punho de cima (a câmera olha de sudeste)
    perto = J._un((J.CAMERA[0] - P[0], 0.0, J.CAMERA[2] - P[2]))
    base = J._add(J._add(P, (0.0, -2.6, 0.0)), J._mul(perto, 1.6))
    base = J._add(base, J._mul(deitada, 2.4))  # a mão presa passa do punho de cima: os dedos dela aparecem além dele
    punho(perde, J._add(base, J._mul(deitada, 0.5)), deitada, up, (5.2, 2.0, 4.4))
    # os dedos de quem perde, dobrados para cima do outro lado do punho de quem vence (a ponta da mão)
    lado = J._un(J._cruz(deitada, up))
    for i, k in enumerate((-2.4, -0.8, 0.8, 2.4)):
        a = J._add(base, J._add(J._mul(deitada, 4.6), J._mul(lado, k)))
        dedo(f"{dp}:{i}", a, J._add(a, J._add((0.0, 3.4, 0.0), J._mul(deitada, -1.6))), 0.95)
    dedo(pp, J._add(base, J._add(J._mul(deitada, -0.5), J._mul(lado, 4.2))),
         J._add(base, J._add(J._add(J._mul(deitada, 2.0), J._mul(lado, 4.0)), (0.0, 2.6, 0.0))), 1.15)
    # o punho de quem vence por cima, o polegar por cima dele
    deit_v = J._un((fv[0], -0.35, fv[2]))
    cima = J._add(J._add(P, (0.0, 2.2, 0.0)), J._mul(perto, -1.4))
    punho(vence, J._add(cima, J._mul(deit_v, 0.4)), deit_v, up, (5.0, 3.2, 4.4))
    dedo(pv, J._add(cima, J._add((0.0, 2.8, 0.0), J._mul(deit_v, -1.2))), J._add(cima, J._add((0.0, 3.0, 0.0), J._mul(deit_v, 2.6))), 1.2)
