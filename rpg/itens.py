"""Consumíveis e geração procedural de equipamentos."""

CONSUMIVEIS = {
    "pocao_vida": {"nome": "Poção de Vida", "preco": 25, "desc": "Recupera 40% da vida."},
    "tonico": {"nome": "Tônico Restaurador", "preco": 20, "desc": "Recupera 50% do recurso (vigor/foco/mana)."},
    "antidoto": {"nome": "Antídoto", "preco": 12, "desc": "Cura veneno."},
    "bandagem": {"nome": "Bandagem", "preco": 8, "desc": "Estanca sangramento e cura 10 de vida."},
    "bomba_fumaca": {"nome": "Bomba de Fumaça", "preco": 30, "desc": "Garante a fuga de um combate (exceto chefes)."},
    "pena_fenix": {"nome": "Pena de Fênix", "preco": 160, "desc": "Revive você com metade da vida se cair em combate."},
}

TIERS = [
    ("Rústico", "Rústica", 0.7), ("Firme", "Firme", 1.0), ("Refinado", "Refinada", 1.3),
    ("Magistral", "Magistral", 1.6), ("Lendário", "Lendária", 2.0),
]
ARMAS = {
    "guerreiro": [("Espada", "f"), ("Machado", "m"), ("Maça", "f"), ("Montante", "m"), ("Martelo", "m")],
    "arqueiro": [("Arco Curto", "m"), ("Arco Longo", "m"), ("Arco Recurvo", "m"), ("Besta Leve", "f")],
    "mago": [("Cajado", "m"), ("Varinha", "f"), ("Orbe", "m"), ("Grimório", "m")],
}
ARMADURAS = {
    "guerreiro": [("Cota de Malha", "f"), ("Peitoral", "m"), ("Couraça", "f"), ("Brigantina", "f")],
    "arqueiro": [("Gibão de Couro", "m"), ("Capa de Patrulha", "f"), ("Colete Acolchoado", "m")],
    "mago": [("Manto", "m"), ("Túnica", "f"), ("Veste Rúnica", "f")],
}
AMULETOS = [("Amuleto", "m"), ("Anel", "m"), ("Talismã", "m"), ("Pingente", "m"), ("Bracelete", "m")]
SUFIXOS = [
    ("da Águia", "agi", 1.0), ("do Urso", "max_hp", 5.0), ("do Lobo", "atk", 1.0), ("da Coruja", "poder", 1.0),
    ("da Tartaruga", "defesa", 0.8), ("da Fonte", "max_rec", 3.0),
]
PESO_PRECO = {"max_hp": 0.25, "max_rec": 0.4, "atk": 1.0, "poder": 1.0, "defesa": 1.2, "agi": 1.1}


def gerar_equip(rng, classe, nivel, slot=None, qualidade=0):
    slot = slot or rng.choices(["arma", "armadura", "amuleto"], [4, 4, 2])[0]
    t = int(rng.gauss(nivel / 3.5, 0.8)) + qualidade
    t = max(0, min(len(TIERS) - 1, t))
    adj_m, adj_f, mult = TIERS[t]
    forca = (1.5 + nivel * 0.9) * mult
    bonus = {}
    if slot == "arma":
        base, g = rng.choice(ARMAS[classe])
        if classe == "guerreiro":
            bonus["atk"] = round(forca)
        elif classe == "arqueiro":
            bonus["atk"] = round(forca * 0.8)
            bonus["agi"] = max(1, round(forca * 0.25))
        else:
            bonus["poder"] = round(forca)
    elif slot == "armadura":
        base, g = rng.choice(ARMADURAS[classe])
        fator = {"guerreiro": 0.7, "arqueiro": 0.5, "mago": 0.35}[classe]
        bonus["defesa"] = max(1, round(forca * fator))
        bonus["max_hp"] = round(forca * 2)
    else:
        base, g = rng.choice(AMULETOS)
    nome = f"{base} {adj_m if g == 'm' else adj_f}"
    if slot == "amuleto" or t >= 2 or rng.random() < 0.4:
        suf, stat, peso = rng.choice(SUFIXOS)
        valor = max(1, round(peso * (1 + nivel * 0.35) * mult))
        bonus[stat] = bonus.get(stat, 0) + valor
        nome += f" {suf}"
    preco = sum(v * PESO_PRECO[k] for k, v in bonus.items()) * 7 * (1 + t * 0.3)
    return {
        "nome": nome, "slot": slot, "bonus": bonus, "preco": max(5, int(preco)),
        "classe": classe if slot != "amuleto" else None, "tier": t,
    }


def descrever_bonus(bonus):
    from .entidades import NOMES_STATS
    return ", ".join(f"{'+' if v >= 0 else ''}{v} {NOMES_STATS[k]}" for k, v in bonus.items())
