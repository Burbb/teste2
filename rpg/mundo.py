"""O mundo da campanha: vizinhos, distâncias e o nível de cada lugar (o mapa vem de campanha.montar_mundo). A
geração do mundo procedural saiu na 1.206.0 (roadmapIDEIAS/24-RETIRADA-DO-PROCEDURAL.md)."""

from collections import deque


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


def vizinhos(mundo, loc):
    return [(mundo["locais"][int(i)], d) for i, d in loc["con"].items()]


def nivel_regiao(loc):
    """Nível típico dos inimigos de um lugar: o que a campanha declara para ele (campanha.py)."""
    return loc["nivel"]
