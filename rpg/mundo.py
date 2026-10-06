"""Geração procedural do mapa do reino.

O mundo é gerado no espaço: lugares recebem coordenadas (x, y entre 0 e 1), os
biomas formam regiões contínuas (cada lugar pertence ao "centro de bioma" mais
próximo) e as estradas ligam vizinhos próximos sem se cruzar. Isso permite
desenhar o mapa no terminal de forma legível.
"""

import math
from collections import deque

from . import texto as tx
from .dados import ANTAGONISTAS, BIOMAS, NOMES_CIDADELA, ORIGENS_ANTAGONISTA, SUFIXOS_LUGAR, VILA_PREFIXOS, \
    VILA_SUFIXOS
from .inimigos import gerar_guardiao

SELVAGENS = ["floresta", "pantano", "montanha", "planicie", "ruinas"]
N_VILAS = 3
N_SELVAGENS = 6
N_COVIS = 3


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


def distancias(locais, origem):
    """Quantos trechos de estrada separam cada lugar da origem."""
    return _distancias(locais, origem)


def _dist_visual(p, q):
    # O mapa é desenhado com caracteres ~2x mais altos que largos.
    return math.hypot((p[0] - q[0]) * 64, (p[1] - q[1]) * 32)


def _cruza(a, b, c, d):
    """Os segmentos ab e cd se cruzam (sem contar pontas compartilhadas)?"""
    if len({a, b, c, d}) < 4:
        return False

    def orient(p, q, r):
        v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        return (v > 1e-12) - (v < -1e-12)

    return orient(a, b, c) * orient(a, b, d) < 0 and orient(c, d, a) * orient(c, d, b) < 0


def _posicoes(rng, n):
    inicio = (0.03, rng.uniform(0.3, 0.7))
    pontos = [inicio]
    minimo = 13.0
    tentativas = 0
    while len(pontos) < n:
        p = (rng.uniform(0.1, 0.86), rng.uniform(0.04, 0.96))
        if all(_dist_visual(p, q) >= minimo for q in pontos):
            pontos.append(p)
        tentativas += 1
        if tentativas > 400:
            minimo *= 0.9
            tentativas = 0
    return pontos


def _conectar(rng, pontos):
    n = len(pontos)
    pares = sorted(((_dist_visual(pontos[i], pontos[j]), i, j) for i in range(n) for j in range(i + 1, n)))
    pai = list(range(n))

    def raiz(i):
        while pai[i] != i:
            pai[i] = pai[pai[i]]
            i = pai[i]
        return i

    arestas = []

    def livre(i, j):
        return not any(_cruza(pontos[i], pontos[j], pontos[a], pontos[b]) for a, b in arestas)

    # Árvore geradora mínima (Kruskal), evitando cruzamentos quando possível.
    for _, i, j in pares:
        if raiz(i) != raiz(j) and livre(i, j):
            pai[raiz(i)] = raiz(j)
            arestas.append((i, j))
    for _, i, j in pares:  # garante conexão mesmo se algo ficou isolado
        if raiz(i) != raiz(j):
            pai[raiz(i)] = raiz(j)
            arestas.append((i, j))

    # Atalhos curtos que não cruzam estradas: criam ciclos e escolhas de rota.
    grau = [0] * n
    for a, b in arestas:
        grau[a] += 1
        grau[b] += 1
    extras = 0
    for d, i, j in pares:
        if extras >= 4 or d > 26:
            break
        if (i, j) in arestas or (j, i) in arestas or grau[i] >= 4 or grau[j] >= 4:
            continue
        if livre(i, j) and rng.random() < 0.7:
            arestas.append((i, j))
            grau[i] += 1
            grau[j] += 1
            extras += 1
    return arestas


def gerar_mundo(rng):
    n_comuns = N_VILAS + N_SELVAGENS + N_COVIS
    pontos = _posicoes(rng, n_comuns)
    arestas = _conectar(rng, pontos)

    vizinhos_de = {i: set() for i in range(n_comuns)}
    for a, b in arestas:
        vizinhos_de[a].add(b)
        vizinhos_de[b].add(a)
    saltos = {0: 0}
    fila = deque([0])
    while fila:
        atual = fila.popleft()
        for v in vizinhos_de[atual]:
            if v not in saltos:
                saltos[v] = saltos[atual] + 1
                fila.append(v)
    max_saltos = max(saltos.values())

    # Papéis: covis espalhados por distância (perto, meio, longe); vilas no meio do caminho.
    candidatos = sorted((i for i in range(1, n_comuns) if saltos[i] >= 2), key=lambda i: saltos[i])
    if len(candidatos) < N_COVIS + N_VILAS - 1:
        candidatos = sorted(range(1, n_comuns), key=lambda i: saltos[i])
    k = len(candidatos)
    covis = []
    for fracao in (0.15, 0.55, 1.0):
        alvo = candidatos[min(k - 1, int(fracao * (k - 1)))]
        livres = [c for c in candidatos if c not in covis]
        alvo = alvo if alvo not in covis else min(livres, key=lambda c: abs(saltos[c] - saltos[alvo]))
        covis.append(alvo)
    restantes = [i for i in range(1, n_comuns) if i not in covis]
    vilas = []
    for fracao in (0.35, 0.8):
        ordenados = sorted(restantes, key=lambda i: abs(saltos[i] - fracao * max_saltos))
        escolha = next((i for i in ordenados if i not in vilas and not any(v in vizinhos_de[i] for v in vilas)),
                       ordenados[0])
        vilas.append(escolha)
        restantes.remove(escolha)

    # Regiões de bioma: cada lugar pertence ao centro de bioma mais próximo.
    centros = {b: (rng.uniform(0.05, 0.95), rng.uniform(0.05, 0.95)) for b in SELVAGENS}

    def bioma_de(i):
        return min(SELVAGENS, key=lambda b: _dist_visual(pontos[i], centros[b]))

    biomas = {i: bioma_de(i) for i in range(n_comuns)}
    usados_covil = []
    for c in covis:
        if biomas[c] in usados_covil:
            livres = [b for b in SELVAGENS if b not in usados_covil]
            biomas[c] = min(livres, key=lambda b: _dist_visual(pontos[c], centros[b]))
        usados_covil.append(biomas[c])

    # Monta os lugares: o início é o id 0 e a Cidadela é sempre o último.
    usados = set()
    locais = []
    for i in range(n_comuns):
        if i == 0 or i in vilas:
            tipo = "vila"
            nome = _nome_vila(rng, usados)
        elif i in covis:
            tipo = "covil"
            nome = _nome_lugar(rng, biomas[i], usados)
        else:
            tipo = "selvagem"
            nome = _nome_lugar(rng, biomas[i], usados)
        locais.append({
            "id": i, "nome": nome, "tipo": tipo, "bioma": biomas[i], "con": {}, "visitado": False,
            "perigo": 1 if i == 0 else max(1, min(5, 1 + round(4 * (saltos[i] - 1) / max(1, max_saltos - 1)))),
            "guardiao": gerar_guardiao(rng, biomas[i]) if tipo == "covil" else None,
            "x": pontos[i][0], "y": pontos[i][1],
        })
    for a, b in arestas:
        _ligar(locais[a], locais[b], 2 if _dist_visual(pontos[a], pontos[b]) > 20 else 1)

    # A Cidadela fica na borda leste, ligada ao lugar não-vila mais próximo dela.
    pos_cid = (0.97, rng.uniform(0.15, 0.85))
    portao = min((l for l in locais if l["tipo"] != "vila" and l["id"] != 0),
                 key=lambda l: _dist_visual((l["x"], l["y"]), pos_cid))
    cid = {"id": len(locais), "nome": rng.choice(NOMES_CIDADELA), "tipo": "cidadela", "bioma": "cidadela",
           "con": {}, "visitado": False, "perigo": 5, "guardiao": None, "x": pos_cid[0], "y": pos_cid[1]}
    locais.append(cid)
    _ligar(portao, cid, 2)

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


def nivel_regiao(loc, corrupcao=0):
    """Nível típico dos inimigos de um lugar: cresce com a distância e com a corrupção."""
    base = 1 + round((loc["perigo"] - 1) * 1.9)
    if loc["tipo"] == "cidadela":
        base = 10
    return base + corrupcao // 34
