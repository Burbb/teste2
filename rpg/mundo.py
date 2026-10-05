"""Geração procedural do mapa do reino."""

from collections import deque

from . import texto as tx
from .dados import BIOMAS, NOMES_CIDADELA, SUFIXOS_LUGAR, VILA_PREFIXOS, VILA_SUFIXOS, ANTAGONISTAS, \
    ORIGENS_ANTAGONISTA
from .inimigos import gerar_guardiao

SELVAGENS = ["floresta", "pantano", "montanha", "planicie", "ruinas"]


def _nome_vila(rng, usados):
    while True:
        nome = rng.choice(VILA_PREFIXOS) + rng.choice(VILA_SUFIXOS)
        if nome not in usados:
            usados.add(nome)
            return nome


def _nome_lugar(rng, bioma, usados):
    while True:
        lugar, _ = rng.choice(BIOMAS[bioma]["lugares"])
        nome = f"{lugar} {rng.choice(SUFIXOS_LUGAR)}"
        if nome not in usados:
            usados.add(nome)
            return nome


def _novo(locais, tipo, bioma, nome):
    loc = {
        "id": len(locais), "nome": nome, "tipo": tipo, "bioma": bioma, "con": {}, "visitado": False,
        "perigo": 1, "guardiao": None,
    }
    locais.append(loc)
    return loc


def _ligar(a, b, dist):
    a["con"][str(b["id"])] = dist
    b["con"][str(a["id"])] = dist


def _distancias(locais, origem=0):
    dist = {origem: 0}
    fila = deque([origem])
    while fila:
        atual = fila.popleft()
        for viz in locais[atual]["con"]:
            viz = int(viz)
            if viz not in dist:
                dist[viz] = dist[atual] + 1
                fila.append(viz)
    return dist


def gerar_mundo(rng):
    usados = set()
    locais = []
    inicio = _novo(locais, "vila", rng.choice(["planicie", "floresta"]), _nome_vila(rng, usados))
    for _ in range(2):
        b = rng.choice(SELVAGENS)
        _novo(locais, "vila", b, _nome_vila(rng, usados))
    for b in rng.sample(SELVAGENS, 4):
        _novo(locais, "selvagem", b, _nome_lugar(rng, b, usados))
    for b in rng.sample(SELVAGENS, 3):
        loc = _novo(locais, "covil", b, _nome_lugar(rng, b, usados))
        loc["guardiao"] = gerar_guardiao(rng, b)

    # Árvore aleatória: lugares comuns primeiro, covis depois (longe do início).
    comuns = [l for l in locais[1:] if l["tipo"] != "covil"]
    covis = [l for l in locais if l["tipo"] == "covil"]
    rng.shuffle(comuns)
    ordem = [inicio] + comuns + covis
    for i, loc in enumerate(ordem[1:], 1):
        candidatos = [p for p in ordem[:i] if len(p["con"]) < 3]
        if loc["tipo"] == "covil":
            candidatos = [p for p in candidatos if p is not inicio] or candidatos
        _ligar(rng.choice(candidatos), loc, rng.choice([1, 1, 2]))

    # Alguns atalhos para formar ciclos.
    for _ in range(2):
        a, b = rng.sample(locais, 2)
        if str(b["id"]) not in a["con"] and len(a["con"]) < 4 and len(b["con"]) < 4:
            _ligar(a, b, 2)

    dist = _distancias(locais)
    for loc in locais:
        loc["perigo"] = max(1, min(5, dist.get(loc["id"], 3)))
    inicio["perigo"] = 1

    # A Cidadela fica após o ponto mais distante.
    mais_longe = max((l for l in locais if l["tipo"] != "vila"), key=lambda l: dist.get(l["id"], 0))
    nome_cid = rng.choice(NOMES_CIDADELA)
    cid = _novo(locais, "cidadela", "cidadela", nome_cid)
    cid["perigo"] = 5
    _ligar(mais_longe, cid, 2)

    titulo, g = rng.choice(ANTAGONISTAS)
    antagonista = {
        "nome": f"{tx.nome_proprio(rng, 3)}, {titulo}",
        "curto": titulo,
        "g": g,
        "origem": rng.choice(ORIGENS_ANTAGONISTA),
    }
    return {"locais": locais, "antagonista": antagonista, "atual": 0}


def vizinhos(mundo, loc):
    return [(mundo["locais"][int(i)], d) for i, d in loc["con"].items()]
