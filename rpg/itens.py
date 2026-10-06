"""Consumíveis e geração procedural de equipamentos."""

CONSUMIVEIS = {
    "pocao_vida": {"nome": "Poção de Vida", "preco": 40, "desc": "Recupera 35% da vida. Gosto de ferrugem."},
    "tonico": {"nome": "Tônico Restaurador", "preco": 35, "desc": "Recupera 50% do recurso (vigor/foco/mana)."},
    "antidoto": {"nome": "Antídoto", "preco": 15, "desc": "Cura veneno."},
    "bandagem": {"nome": "Bandagem", "preco": 10, "desc": "Estanca sangramento e trata uma ferida aberta (evita infecção)."},
    "unguento": {"nome": "Unguento de Prata", "preco": 30, "desc": "Cura uma infecção."},
    "tocha": {"nome": "Tocha", "preco": 4, "desc": "Luz para uma ação no escuro (noite, ruínas, cidadela)."},
    "bomba_fumaca": {"nome": "Bomba de Fumaça", "preco": 35, "desc": "Garante a fuga de um combate (exceto chefes)."},
    "pena_fenix": {"nome": "Pena de Fênix", "preco": 220, "desc": "Revive você com metade da vida se cair em combate."},
}

RARIDADES = ["comum", "magico", "raro", "lendario"]
NOMES_RARIDADE = {"comum": "Comum", "magico": "Mágico", "raro": "Raro", "lendario": "LENDÁRIO"}
COR_RARIDADE = {"comum": None, "magico": "azul", "raro": "amarelo", "lendario": "magenta+negrito"}

MATERIAIS = [  # qualidade da base conforme o nível
    ("Enferrujado", "Enferrujada", 0.75), ("de Ferro", "de Ferro", 0.9), ("de Aço", "de Aço", 1.0),
    ("Temperado", "Temperada", 1.1), ("Rúnico", "Rúnica", 1.2),
]
MATERIAIS_COURO = [("Rasgado", "Rasgada", 0.75), ("Curtido", "Curtida", 0.9), ("Reforçado", "Reforçada", 1.0),
                   ("Tachonado", "Tachonada", 1.1), ("Rúnico", "Rúnica", 1.2)]
MATERIAIS_TECIDO = [("Puído", "Puída", 0.75), ("de Linho", "de Linho", 0.9), ("de Lã Negra", "de Lã Negra", 1.0),
                    ("Bordado", "Bordada", 1.1), ("Rúnico", "Rúnica", 1.2)]
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
AMULETOS = [("Amuleto", "m"), ("Talismã", "m"), ("Pingente", "m"), ("Medalhão", "m")]
ANEIS = [("Anel", "m"), ("Sinete", "m"), ("Aro", "m")]
PECAS = {  # partes da armadura e mão secundária, por classe
    "cabeca": {"guerreiro": [("Elmo", "m"), ("Capacete", "m"), ("Barbuta", "f")],
               "arqueiro": [("Capuz", "m"), ("Chapéu de Couro", "m")],
               "mago": [("Capuz", "m"), ("Chapéu Pontudo", "m"), ("Diadema", "m")]},
    "maos": {"guerreiro": [("Manopla", "f")], "arqueiro": [("Braçadeira", "f")], "mago": [("Luva de Seda", "f")]},
    "pernas": {"guerreiro": [("Perneira", "f"), ("Greva", "f")], "arqueiro": [("Calça de Couro", "f")],
               "mago": [("Calça de Viagem", "f")]},
    "pes": {"guerreiro": [("Bota Ferrada", "f")], "arqueiro": [("Bota de Caça", "f")], "mago": [("Sandália", "f")]},
    "secundaria": {"guerreiro": [("Escudo", "m"), ("Broquel", "m")], "arqueiro": [("Aljava", "f")],
                   "mago": [("Tomo", "m"), ("Foco Arcano", "m")]},
}
# Espaços do corpo (chaves de jogador.equip). Itens de anel cabem em anel1 ou anel2.
SLOTS = ["cabeca", "amuleto", "armadura", "maos", "arma", "secundaria", "pernas", "pes", "anel1", "anel2"]
NOMES_SLOT = {"arma": "Arma", "secundaria": "Apoio", "cabeca": "Cabeça", "armadura": "Peito", "maos": "Mãos",
              "pernas": "Pernas", "pes": "Pés", "amuleto": "Amuleto", "anel": "Anel", "anel1": "Anel", "anel2": "Anel"}
PESO_SLOT = {"arma": 3, "armadura": 3, "cabeca": 2, "maos": 2, "pernas": 2, "pes": 2, "secundaria": 2,
             "amuleto": 1, "anel": 1.5}


def espacos(slot):
    """Chaves de equip onde um item deste tipo pode ir."""
    return ["anel1", "anel2"] if slot == "anel" else [slot]

# Afixos: (nome, atributo, valor base). Os especiais são lidos pelo combate.
AFIXOS_ITEM = [
    ("do Urso", "max_hp", 6), ("da Águia", "agi", 1.2), ("do Lobo", "atk", 1.2), ("da Coruja", "poder", 1.2),
    ("da Tartaruga", "defesa", 1.0), ("da Fonte", "max_rec", 4), ("do Vampiro", "roubo_vida", 2.5),
    ("da Precisão", "critico", 2.5), ("dos Espinhos", "espinhos", 2.0), ("da Regeneração", "regen_vida", 0.8),
    ("do Carniceiro", "vida_abate", 2.5),
]
ESPECIAIS = ("roubo_vida", "critico", "espinhos", "regen_vida", "vida_abate")

NOMES_RAROS_A = ["Presa", "Agonia", "Lamento", "Sussurro", "Grito", "Mordida", "Ruína", "Fome", "Pranto", "Cicatriz",
                 "Sombra", "Juramento", "Maldição", "Brasa", "Osso"]
NOMES_RAROS_B = ["do Abismo", "da Carne", "do Corvo", "Sangrenta", "da Forca", "do Túmulo", "Negra", "da Peste",
                 "Sem Nome", "do Mártir", "Faminta", "da Fenda", "do Carrasco", "Antiga", "da Viúva"]

UNICOS = [
    dict(nome="Lamento de Gharbad", slot="arma", classe="guerreiro", base="Machado",
         bonus={"atk": 1.5, "roubo_vida": 6, "vida_abate": 5},
         lore="Um caído quis ser ferreiro. Forjou isto com os ossos dos próprios irmãos."),
    dict(nome="O Açougueiro", slot="arma", classe="guerreiro", base="Cutelo",
         bonus={"atk": 1.8, "critico": 6},
         lore="\"Ahh... carne fresca!\" — a última coisa que muitos ouviram."),
    dict(nome="Ventre da Tempestade", slot="arma", classe="arqueiro", base="Arco Longo",
         bonus={"atk": 1.4, "agi": 1.5, "critico": 8},
         lore="A corda foi trançada com cabelo de uma bruxa afogada. Ela ainda canta quando você atira."),
    dict(nome="Sussurro do Vazio", slot="arma", classe="arqueiro", base="Arco Recurvo",
         bonus={"atk": 1.5, "roubo_vida": 5, "agi": 0.8},
         lore="As flechas voltam com menos sangue do que deveriam."),
    dict(nome="Olho do Abismo", slot="arma", classe="mago", base="Orbe",
         bonus={"poder": 1.6, "max_rec": 10, "regen_vida": 2},
         lore="Ele olha de volta. Sempre olhou."),
    dict(nome="Cajado da Peste", slot="arma", classe="mago", base="Cajado",
         bonus={"poder": 1.5, "vida_abate": 6, "max_rec": 6},
         lore="Pertenceu a um curandeiro que descobriu que era mais fácil matar a doença junto com o doente."),
    dict(nome="Pele do Penitente", slot="armadura", classe=None, base="Couraça de Couro Humano",
         bonus={"defesa": 1.2, "max_hp": 14, "espinhos": 5},
         lore="Ninguém sabe quem ela era. Ela ainda sente dor por você."),
    dict(nome="Manto de Cinzas", slot="armadura", classe=None, base="Manto",
         bonus={"defesa": 0.8, "max_rec": 12, "regen_vida": 2},
         lore="Tecido com as cinzas da última vila que a Fenda engoliu."),
    dict(nome="Coroa dos Afogados", slot="cabeca", classe=None, base="Diadema",
         bonus={"max_hp": 12, "regen_vida": 2, "defesa": 1},
         lore="Achada na cabeça de um rei no fundo do pântano. Ele não estava morto."),
    dict(nome="Égide do Mártir", slot="secundaria", classe="guerreiro", base="Escudo de Torre",
         bonus={"defesa": 1.4, "max_hp": 10, "espinhos": 6},
         lore="Cada amassado é uma oração que alguém não terminou de fazer."),
    dict(nome="Aljava dos Mil Corvos", slot="secundaria", classe="arqueiro", base="Aljava",
         bonus={"agi": 1.2, "critico": 7, "atk": 0.6},
         lore="Penas negras. As flechas voltam sozinhas, às vezes, de madrugada."),
    dict(nome="Tomo do Nome Esquecido", slot="secundaria", classe="mago", base="Tomo",
         bonus={"poder": 1.1, "max_rec": 14, "roubo_vida": 3},
         lore="As páginas estão em branco até você sangrar nelas."),
    dict(nome="Botas do Andarilho Morto", slot="pes", classe=None, base="Bota",
         bonus={"agi": 1.4, "regen_vida": 2, "max_hp": 6},
         lore="Ainda caminham à noite. Calce-as antes que vão embora sem você."),
    dict(nome="Mãos do Estrangulador", slot="maos", classe=None, base="Luvas",
         bonus={"atk": 0.8, "poder": 0.8, "critico": 6},
         lore="Os dedos se fecham sozinhos quando alguém mente perto de você."),
    dict(nome="Anel do Último Rei", slot="anel", classe=None, base="Anel",
         bonus={"atk": 1, "poder": 1, "critico": 5, "roubo_vida": 3},
         lore="O reino caiu. O anel não."),
]

PESO_PRECO = {"max_hp": 0.25, "max_rec": 0.4, "atk": 1.0, "poder": 1.0, "defesa": 1.2, "agi": 1.1,
              "roubo_vida": 1.5, "critico": 1.5, "espinhos": 1.0, "regen_vida": 2.5, "vida_abate": 1.0}


def rolar_raridade(rng, qualidade=0):
    pesos = [60, 28, 10, 2]
    for _ in range(max(0, qualidade)):
        pesos = [pesos[0] * 0.5, pesos[1] * 1.1, pesos[2] * 1.8, pesos[3] * 2.2]
    for _ in range(max(0, -qualidade)):
        pesos = [pesos[0] * 1.6, pesos[1] * 0.8, pesos[2] * 0.4, 0]
    return rng.choices(RARIDADES, weights=pesos)[0]


def _escala(nivel):
    return 1.5 + nivel * 0.9


def _afixos(rng, nivel, n):
    escolhidos = rng.sample(AFIXOS_ITEM, n)
    bonus = {}
    for _, stat, base in escolhidos:
        valor = base * (1 + nivel * 0.3) if stat not in ("critico", "roubo_vida") else base + nivel * 0.25
        bonus[stat] = bonus.get(stat, 0) + max(1, round(valor))
    return escolhidos, bonus


def _unico(rng, classe, nivel, slot):
    opcoes = [u for u in UNICOS if (slot is None or u["slot"] == slot) and u["classe"] in (None, classe)]
    if not opcoes:
        return None
    u = rng.choice(opcoes)
    forca = _escala(nivel) * 1.3
    bonus = {}
    for stat, v in u["bonus"].items():
        if stat in ("atk", "poder", "agi", "defesa"):
            bonus[stat] = max(1, round(forca * v * (0.5 if stat in ("agi", "defesa") and u["slot"] == "arma" else 1)
                                       * (0.6 if stat == "defesa" else 1)))
        elif stat in ("max_hp", "max_rec"):
            bonus[stat] = round(v * (1 + nivel * 0.25))
        else:
            bonus[stat] = round(v + nivel * 0.3)
    return {"nome": u["nome"], "base": u["base"], "slot": u["slot"], "bonus": bonus, "classe": u["classe"],
            "raridade": "lendario", "lore": u["lore"], "preco": _preco(bonus, "lendario")}


def _preco(bonus, raridade):
    fator = {"comum": 1.0, "magico": 1.5, "raro": 2.2, "lendario": 3.5}[raridade]
    return max(5, int(sum(abs(v) * PESO_PRECO[k] for k, v in bonus.items()) * 7 * fator))


def gerar_equip(rng, classe, nivel, slot=None, qualidade=0, raridade=None):
    raridade = raridade or rolar_raridade(rng, qualidade)
    if raridade == "lendario":
        item = _unico(rng, classe, nivel, slot)
        if item:
            return item
        raridade = "raro"
    slot = slot or rng.choices(list(PESO_SLOT), list(PESO_SLOT.values()))[0]
    materiais = MATERIAIS
    if slot in ("armadura", "cabeca", "maos", "pernas", "pes") and classe == "mago":
        materiais = MATERIAIS_TECIDO
    elif slot in ("armadura", "cabeca", "maos", "pernas", "pes", "secundaria") and classe == "arqueiro":
        materiais = MATERIAIS_COURO
    mat_m, mat_f, mult = materiais[max(0, min(len(materiais) - 1, nivel // 3 + rng.choice([-1, 0, 0, 1])))]
    forca = _escala(nivel) * mult
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
    elif slot in PECAS:
        base, g = rng.choice(PECAS[slot][classe])
        forca *= 0.65  # peças complementares: somadas, não devem valer mais que arma e armadura
        fator = {"guerreiro": 0.7, "arqueiro": 0.5, "mago": 0.35}[classe]
        principal = {"guerreiro": "atk", "arqueiro": "agi", "mago": "poder"}[classe]
        if slot == "cabeca":
            bonus["defesa"] = max(1, round(forca * fator * 0.4))
            bonus["max_hp"] = max(1, round(forca * 0.8))
        elif slot == "maos":
            bonus[principal] = max(1, round(forca * 0.25))
            bonus["defesa"] = max(1, round(forca * fator * 0.2))
        elif slot == "pernas":
            bonus["defesa"] = max(1, round(forca * fator * 0.45))
            bonus["max_hp"] = max(1, round(forca * 1.0))
        elif slot == "pes":
            bonus["agi"] = max(1, round(forca * 0.3))
            bonus["defesa"] = max(1, round(forca * fator * 0.2))
        elif classe == "guerreiro":  # escudo
            bonus["defesa"] = max(1, round(forca * 0.55))
            bonus["max_hp"] = max(1, round(forca * 0.8))
        elif classe == "arqueiro":  # aljava
            bonus["agi"] = max(1, round(forca * 0.3))
            bonus["atk"] = max(1, round(forca * 0.3))
        else:  # tomo
            bonus["poder"] = max(1, round(forca * 0.45))
            bonus["max_rec"] = max(1, round(forca * 1.5))
        if slot == "secundaria" and classe == "mago":
            mat_m = mat_f = ""
    else:
        base, g = rng.choice(ANEIS if slot == "anel" else AMULETOS)
        mat_m = mat_f = ""
    tipo_base = f"{base} {mat_m if g == 'm' else mat_f}".strip()
    n_afixos = {"comum": 1 if slot in ("amuleto", "anel") else 0, "magico": 1, "raro": rng.choice([2, 3])}[raridade]
    escolhidos, extras = _afixos(rng, nivel, n_afixos)
    for k, v in extras.items():
        bonus[k] = bonus.get(k, 0) + v
    if raridade == "raro":
        nome = f"{rng.choice(NOMES_RAROS_A)} {rng.choice(NOMES_RAROS_B)}"
    elif escolhidos:
        nome = f"{tipo_base} {escolhidos[0][0]}"
    else:
        nome = tipo_base
    return {"nome": nome, "base": tipo_base, "slot": slot, "bonus": bonus, "preco": _preco(bonus, raridade),
            "classe": classe if slot not in ("amuleto", "anel") else None, "raridade": raridade}


def rotulo(item):
    """Nome com raridade e tipo de base, para listas."""
    r = item.get("raridade", "comum")
    nome = item["nome"]
    if r in ("raro", "lendario") and item.get("base"):
        nome += f" ({item['base']})"
    if r == "lendario":
        nome = "★ " + nome
    return nome


def cor(item):
    return COR_RARIDADE[item.get("raridade", "comum")]


def descrever_bonus(bonus):
    from .entidades import NOMES_STATS
    partes = []
    for k, v in bonus.items():
        if k in ("roubo_vida", "critico"):
            partes.append(f"+{v}% {NOMES_STATS[k]}")
        else:
            partes.append(f"{'+' if v >= 0 else ''}{v} {NOMES_STATS[k]}")
    return ", ".join(partes)
