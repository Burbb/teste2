"""Classes, especializações e companheiros animais do jogador (as habilidades estão em habilidades.py).

Árvore:
    Guerreiro -> Paladino  | Berserker
    Arqueiro  -> Patrulheiro | Sombra
    Mago      -> Piromante | Necromante

Além dos números, classe e especialização declaram o que mudam fora deles:
    testes      {teste: (de onde vem, bônus)} nos testes de atributo ("olhos de arqueiro" +3 em Percepção)
    mods        modificadores, como os de um talento (modificadores.py): valem sempre, sem aparecer como passiva
    reage       o que a comitiva sente quando você escolhe a especialização (etiquetas de comitiva.reagir)
    companheiro a especialização vem com um animal (o jogo pergunta qual)
    limites     o que a escolha de especialização avisa e as contas não mostram sozinhas (especializacao.limites junta
                a isto o que sai das habilidades: o tipo de dano contra quem resiste, os estados que não pegam em todos)
"""

CLASSES = {
    "guerreiro": {
        "nome": "Guerreiro",
        "recurso": "Vigor",
        "cor": "vermelho",
        "desc": "Muita vida e defesa. Luta corpo a corpo e aguenta o tranco. Vigor regenera rápido.",
        "base": dict(max_hp=60, atk=9, defesa=6, agi=3, poder=1, max_rec=30, regen=6),
        "cresc": dict(max_hp=9, atk=2.0, defesa=1.2, agi=0.4, poder=0.3, max_rec=2),
        "habilidades": [(1, "golpe_pesado"), (1, "erguer_escudo"), (2, "investida"), (3, "grito_guerra")],
        "specs": ["paladino", "berserker"],
        "icone_ataque": "espada",
        "ataque": ("Golpe de espada", "corpo", "fisico", "atk", 1.0),
    },
    "arqueiro": {
        "nome": "Arqueiro",
        "recurso": "Foco",
        "cor": "verde",
        "desc": "Ágil e preciso, ataca à distância. Gasta flechas (que podem acabar!) e é ótimo contra voadores.",
        "base": dict(max_hp=52, atk=8, defesa=4, agi=8, poder=2, max_rec=25, regen=5),
        "cresc": dict(max_hp=8, atk=2.0, defesa=1.1, agi=1.2, poder=0.4, max_rec=2),
        "habilidades": [(1, "tiro_certeiro"), (1, "marcar_presa"), (2, "chuva_flechas"), (3, "passo_agil")],
        "specs": ["patrulheiro", "sombra"],
        "testes": {"percepcao": ("olhos de arqueiro", 3)},
        "icone_ataque": "arco",
        "ataque": ("Disparo", "distancia", "fisico", "atk", 1.1),
    },
    "mago": {
        "nome": "Mago",
        "recurso": "Mana",
        "cor": "azul",
        "desc": "Frágil, mas devastador. Magias elementais exploram fraquezas. Mana regenera devagar.",
        "base": dict(max_hp=42, atk=3, defesa=3, agi=4, poder=11, max_rec=40, regen=3),
        "cresc": dict(max_hp=8, atk=0.5, defesa=0.8, agi=0.6, poder=2.0, max_rec=5),
        "habilidades": [(1, "bola_fogo"), (1, "meditar"), (2, "lanca_gelo"), (3, "barreira")],
        "specs": ["piromante", "necromante"],
        "testes": {"vontade": ("mente treinada", 2)},
        "icone_ataque": "cajado",
        "ataque": ("Dardo Arcano", "distancia", "arcano", "poder", 1.0),
    },
}

SPECS = {
    "paladino": {
        "nome": "Paladino", "classe": "guerreiro",
        "desc": "Juramento da Luz. Cura a si mesmo, fere mortos-vivos e corrompidos com poder sagrado.",
        "bonus": dict(max_hp=15, poder=6, defesa=3),
        "cresc": dict(poder=1.5, max_hp=2),
        "habilidades": [(4, "golpe_sagrado"), (4, "prece"), (7, "julgamento")],
        "testes": {"vontade": ("paladino", 3), "carisma": ("paladino", 2)},
        "mods": {"resiste_terror": 0.6},  # a fé não vacila diante do grito de terror
        "reage": ("fe", "honra"),
        "limites": ("Até o nível 7, todo o dano é num alvo só: o Julgamento Divino é o primeiro golpe em todos.",),
    },
    "berserker": {
        "nome": "Berserker", "classe": "guerreiro",
        "desc": "Pacto de Sangue. Quanto mais ferido, mais forte. Rouba vida e acerta todos ao redor.",
        "bonus": dict(atk=5, max_hp=10, defesa=-2),
        "cresc": dict(atk=1.0),
        "habilidades": [(4, "sede_sangue"), (4, "redemoinho"), (7, "furia_cega")],
        "reage": ("violencia", "coragem"),
        "limites": ("O Pacto de Sangue rende mais quanto mais ferido você estiver: o risco é seu.",
                    "A Fúria Cega (nível 7) custa vida, não vigor."),
    },
    "patrulheiro": {
        "nome": "Patrulheiro", "classe": "arqueiro",
        "desc": "Guardião das matas. Luta ao lado de um companheiro animal e domina armadilhas.",
        "bonus": dict(max_hp=10, atk=2, defesa=2),
        "cresc": dict(max_hp=2, atk=0.4),
        "habilidades": [(4, "tiro_duplo"), (4, "comando_fera"), (7, "furia_natureza")],
        "testes": {"percepcao": ("patrulheiro", 2)},
        "companheiro": True,
        "limites": ("O animal ferido fica fora das lutas até você descansar.",
                    "As armadilhas são um talento (Armadilheiro, nível 6): um inimigo começa cada luta preso."),
    },
    "sombra": {
        "nome": "Sombra", "classe": "arqueiro",
        "desc": "Irmandade da Sombra. Furtividade, venenos e execuções. Críticos devastadores.",
        "bonus": dict(agi=5, atk=3, max_hp=10, defesa=2),
        "cresc": dict(agi=0.6, atk=0.4),
        "habilidades": [(4, "desaparecer"), (4, "flecha_envenenada"), (7, "execucao")],
        "reage": ("trapaca",),
        "limites": ("O talento Pontas Venenosas também é veneno, com o mesmo limite: contra mortos-vivos e construtos, "
                    "o caminho perde boa parte do dano.",
                    "Desaparecer garante o crítico e dá esquiva, mas não tira você da mira dos inimigos.",
                    "A Execução (nível 7) só rende muito em alvo abaixo de 35% de vida."),
    },
    "piromante": {
        "nome": "Piromante", "classe": "mago",
        "desc": "A Chama Viva. Queimaduras mais fortes, magias em área e explosões em cadeia.",
        "bonus": dict(poder=4, max_rec=10),
        "cresc": dict(poder=0.8),
        "habilidades": [(4, "inferno"), (4, "combustao"), (7, "fenix")],
        "reage": ("curiosidade",),
        "limites": ("A Combustão rende pouco sem chamas no alvo: acender vem antes, e cada camada pede uma Bola de Fogo "
                    "que acenda.",
                    "Quem resiste muito ao fogo não pega fogo; a chuva enfraquece as chamas."),
    },
    "necromante": {
        "nome": "Necromante", "classe": "mago",
        "desc": "O Sussurro do Túmulo. Drena vida, amaldiçoa e ergue servos dos mortos.",
        "bonus": dict(max_hp=12, poder=3, defesa=2),
        "cresc": dict(max_hp=2, poder=0.5),
        "habilidades": [(4, "drenar_vida"), (4, "erguer_servo"), (7, "maldicao")],
        "reage": ("magia_proibida", "sacrilegio"),
        "limites": ("Um servo por vez (dois com o talento Legião de Ossos); ele atrai os golpes só nos dois primeiros "
                    "turnos.",),
    },
}

COMPANHEIROS = {
    "lobo": dict(nome="Lobo Cinzento", hp=30, atk=7, agi=7, alcance="corpo", crit=0.05,
                 desc="Equilibrado. Morde e faz o inimigo sangrar."),
    "falcao": dict(nome="Falcão Peregrino", hp=18, atk=6, agi=12, alcance="distancia", crit=0.25,
                   desc="Frágil, mas veloz e certeiro. Ótimo contra voadores."),
    "urso": dict(nome="Urso Pardo", hp=50, atk=9, agi=2, alcance="corpo", crit=0.0,
                 desc="Lento e resistente. Atrai golpes e às vezes atordoa."),
}


# As habilidades (o que cada uma faz e como o Grimório a descreve) moram em habilidades.py.


def habilidades_ate(classe, spec, nivel):
    lista = [h for (nv, h) in CLASSES[classe]["habilidades"] if nv <= nivel]
    if spec:
        lista += [h for (nv, h) in SPECS[spec]["habilidades"] if nv <= nivel]
    return lista
