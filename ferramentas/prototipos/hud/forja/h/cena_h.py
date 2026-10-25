"""A cena da forja F montada, quadro a quadro, como o jogo a monta (forja-h.js faz a mesma coisa com as camadas
exportadas): o fundo, o fogo (4 quadros), a bigorna, a espada, a tenaz, o ferreiro na pose, as faíscas e o primeiro
plano. A linha do tempo é a da R (o ritmo aprovado): 100 ms por quadro, quatro golpes e a pausa da tenaz."""
import math

import ambiente_h as A
import ferreiro_h as F
from paleta_h import RAMPAS as R

# A linha do tempo da R, sem mudança: (pose, quadros). O último quadro (repouso) emenda no primeiro.
GOLPE = lambda alto, repouso: [("sobe1", 1), ("sobe2", 1), ("alto", alto), ("desce", 1), ("golpe", 1), ("volta", 1), ("repouso", repouso)]
CICLO = [("repouso", 3)] + GOLPE(3, 2) + GOLPE(2, 2) + GOLPE(3, 1) + GOLPE(4, 3) + [("ajuste", 6), ("repouso", 4)]
DURACAO = sum(d for _, d in CICLO)


def pose_de(q):
    r, golpes = q % DURACAO, 0
    for nome, d in CICLO:
        if r < d:
            return {"nome": nome, "t": r, "golpe": golpes, "volta": q // DURACAO}
        if nome == "golpe":
            golpes += 1
        r -= d
    return {"nome": "repouso", "t": 0, "golpe": 0, "volta": 0}


def faiscas(t, semente, idade):
    """As faíscas do golpe: nascem no ponto de contato e se abrem por dois quadros (do branco ao laranja); as
    direções variam de golpe para golpe (as mesmas para o mesmo golpe). A mesma conta da R."""
    x, y = F.CONTATO
    s = (semente * 9301 + 49297) % 233280 or 7

    def rnd():
        nonlocal s
        s = (s * 16807) % 2147483647
        return s / 2147483647
    Fo = R["fogo"]
    for i in range(9):
        ang, vel, sobe = math.pi * (1.05 + rnd() * 0.9), 2.5 + rnd() * 4.5, -1.2 - rnd() * 1.5
        d = idade * vel + 1.5
        lado = 1 if rnd() < 0.5 else -0.6
        qx = x + math.cos(ang) * d * lado
        qy = y + math.sin(ang) * d * 0.55 + idade * idade * 0.8 + sobe * (0.5 if idade > 0 else 0)
        if idade == 2 and i % 2:
            continue
        t.px(qx, qy, Fo[6] if idade == 0 else Fo[5] if idade == 1 else Fo[4])
        if idade > 0:
            t.px(qx + (-1 if qx > x else 1), qy + 0.5, Fo[4] if idade == 1 else Fo[3])
    if idade == 0:
        t.px(x - 1, y - 1, Fo[6]); t.px(x, y - 1, Fo[6]); t.px(x + 1, y - 1, Fo[6]); t.px(x, y - 2, Fo[6])


_cache = {}


def camadas_paradas():
    if not _cache:
        fundo = A.desenhar_fundo()
        _cache.update(fundo=fundo, bigorna=A.bigorna(), frente=A.frente())
    return _cache


def quadro(q, reduzido=False, com_faiscas=True):
    """A cena no quadro q do relógio (100 ms). Com movimento reduzido: a pose do alto, parada, sem faíscas."""
    c = camadas_paradas()
    t = A.Tela(A.QW, A.QH, c["fundo"].a)
    A.fogo(t, 1 if reduzido else (q // 2) % 4)
    t.sobre(c["bigorna"])
    p = {"nome": "alto", "t": 0, "golpe": 0, "volta": 0} if reduzido else pose_de(q)
    pose = F.POSES[p["nome"]]
    forte = not reduzido and p["nome"] in ("golpe", "volta")
    virada = pose.get("vira") and 1 <= p["t"] < 5
    A.espada(t, F.CONTATO[0], forte, virada)
    t.sobre(F.figura(p["nome"], virada=virada))
    if com_faiscas and not reduzido:
        n = p["golpe"] + p["volta"] * 4
        if p["nome"] == "golpe":
            faiscas(t, n, 0)
        elif p["nome"] == "volta":
            faiscas(t, n - 1, 1)
        elif p["nome"] == "repouso" and p["t"] == 0 and p["golpe"] > 0:  # logo depois do rebote
            faiscas(t, n - 1, 2)
    t.sobre(c["frente"])
    return t
