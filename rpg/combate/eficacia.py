"""Quanto um golpe rende contra os traços e as resistências do alvo (a ficha da luta e o bestiário também leem
daqui)."""

from ..dados import TRACOS_FICHA


def mult_tracos(alvo, tipo, alcance):
    """Quanto o golpe rende contra os traços do alvo (catálogo TRACOS_FICHA, na ordem dele) e as resistências."""
    m = 1.0
    for nome, tr in TRACOS_FICHA.items():
        if nome in alvo.tracos:
            if "alcance" in tr:
                m *= tr["alcance"].get(alcance, tr["alcance"].get("*", 1))
            if "tipo" in tr:
                m *= tr["tipo"].get(tipo, tr["tipo"].get("*", 1))
    return m * alvo.resist.get(tipo, 1)


TIPOS_DANO = ("fisico", "fogo", "gelo", "sagrado", "sombra", "arcano", "veneno")
NOMES_TIPO_DANO = {"fisico": "corpo a corpo", "distancia": "à distância", "fogo": "fogo", "gelo": "gelo",
                   "sagrado": "sagrado", "sombra": "sombra", "arcano": "arcano", "veneno": "veneno"}
FRACO, RESISTE = 1.15, 0.85  # a partir de quanto a ficha e o bestiário chamam de fraqueza e de resistência


def eficacias(alvo):
    """Quanto rende cada tipo de dano contra o alvo (traços e resistências), em dois grupos para a tela: as
    fraquezas e as resistências (0 é imune). A ficha da luta e o bestiário leem daqui."""
    m = {tipo: round(mult_tracos(alvo, tipo, "corpo"), 2) for tipo in TIPOS_DANO}
    m["distancia"] = round(mult_tracos(alvo, "fisico", "distancia"), 2)
    return {k: v for k, v in m.items() if v >= FRACO}, {k: v for k, v in m.items() if v <= RESISTE}
