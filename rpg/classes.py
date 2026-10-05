"""Classes, especializações e habilidades do jogador.

Árvore:
    Guerreiro -> Paladino  | Berserker
    Arqueiro  -> Patrulheiro | Sombra
    Mago      -> Piromante | Necromante
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
        "ataque": ("Disparo", "distancia", "fisico", "atk", 1.1),
    },
    "mago": {
        "nome": "Mago",
        "recurso": "Mana",
        "cor": "azul",
        "desc": "Frágil, mas devastador. Magias elementais exploram fraquezas. Mana regenera devagar.",
        "base": dict(max_hp=42, atk=3, defesa=3, agi=4, poder=11, max_rec=40, regen=3),
        "cresc": dict(max_hp=6.5, atk=0.5, defesa=0.8, agi=0.6, poder=2.4, max_rec=5),
        "habilidades": [(1, "bola_fogo"), (1, "meditar"), (2, "lanca_gelo"), (3, "barreira")],
        "specs": ["piromante", "necromante"],
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
    },
    "berserker": {
        "nome": "Berserker", "classe": "guerreiro",
        "desc": "Pacto do Sangue. Quanto mais ferido, mais forte. Rouba vida e acerta todos ao redor.",
        "bonus": dict(atk=5, max_hp=10, defesa=-2),
        "cresc": dict(atk=1.0),
        "habilidades": [(4, "sede_sangue"), (4, "redemoinho"), (7, "furia_cega")],
    },
    "patrulheiro": {
        "nome": "Patrulheiro", "classe": "arqueiro",
        "desc": "Guardião das matas. Luta ao lado de um companheiro animal e domina armadilhas.",
        "bonus": dict(max_hp=10, atk=2, defesa=2),
        "cresc": dict(max_hp=2, atk=0.4),
        "habilidades": [(4, "tiro_duplo"), (4, "comando_fera"), (7, "furia_natureza")],
    },
    "sombra": {
        "nome": "Sombra", "classe": "arqueiro",
        "desc": "Irmandade da Sombra. Furtividade, venenos e execuções. Críticos devastadores.",
        "bonus": dict(agi=5, atk=3, max_hp=10, defesa=2),
        "cresc": dict(agi=0.6, atk=0.4),
        "habilidades": [(4, "desaparecer"), (4, "flecha_envenenada"), (7, "execucao")],
    },
    "piromante": {
        "nome": "Piromante", "classe": "mago",
        "desc": "A Chama Viva. Queimaduras mais fortes, magias em área e explosões em cadeia.",
        "bonus": dict(poder=6, max_rec=10),
        "cresc": dict(poder=0.8),
        "habilidades": [(4, "inferno"), (4, "combustao"), (7, "fenix")],
    },
    "necromante": {
        "nome": "Necromante", "classe": "mago",
        "desc": "O Sussurro do Túmulo. Drena vida, amaldiçoa e ergue servos dos mortos.",
        "bonus": dict(max_hp=12, poder=3, defesa=2),
        "cresc": dict(max_hp=2, poder=0.5),
        "habilidades": [(4, "drenar_vida"), (4, "erguer_servo"), (7, "maldicao")],
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


# ======================================================================
# Habilidades. Cada função recebe (combate, usuário, alvo).
# ======================================================================

# --- Guerreiro ---------------------------------------------------------
def _golpe_pesado(cb, u, alvo):
    cb.atacar(u, alvo, 1.7, rotulo="Golpe Pesado")


def _erguer_escudo(cb, u, alvo):
    turnos = 2 + u.tal("muralha")
    u.aplicar("guarda", turnos, 0.5)
    cb.dizer(f"Você ergue o escudo e firma os pés. (dano recebido -50% por {turnos} turnos)", "ciano")


def _investida(cb, u, alvo):
    dano = cb.atacar(u, alvo, 1.2, rotulo="Investida")
    if dano:
        cb.aplicar(alvo, "atordoado", 1, chance=0.45)


def _grito_guerra(cb, u, alvo):
    cb.dizer("Você solta um grito de guerra que faz o chão tremer!", "ciano")
    u.aplicar("fortalecido", 3, 0.3)
    for ini in cb.inimigos_vivos():
        cb.aplicar(ini, "enfraquecido", 2, chance=0.8)


def _golpe_sagrado(cb, u, alvo):
    dano = cb.atacar(u, alvo, 1.3, tipo="sagrado", bonus=u.poder * 0.8, rotulo="Golpe Sagrado")
    if dano:
        cura = u.curar(dano * 0.35 * (1 + 0.25 * u.tal("luz_curativa")))
        if cura:
            cb.dizer(f"A luz fecha suas feridas. (+{cura} vida)", "verde")


def _prece(cb, u, alvo):
    cura = u.curar((u.max_hp * 0.3 + u.poder * 1.5) * (1 + 0.25 * u.tal("luz_curativa")))
    u.limpar_negativos()
    cb.dizer(f"Você reza em voz baixa. Uma luz quente te envolve. (+{cura} vida, males removidos)", "verde")


def _julgamento(cb, u, alvo):
    cb.dizer("Você ergue a arma aos céus. Colunas de luz caem sobre seus inimigos!", "amarelo+negrito")
    for ini in cb.inimigos_vivos():
        cb.atacar(u, ini, 1.2, tipo="sagrado", bonus=u.poder, alcance="distancia", pode_esquivar=False)


def _sede_sangue(cb, u, alvo):
    dano = cb.atacar(u, alvo, 1.4, rotulo="Sede de Sangue")
    if dano:
        cura = u.curar(dano * 0.4)
        cb.aplicar(alvo, "sangramento", 3, valor=max(2, u.atk * 0.3))
        if cura:
            cb.dizer(f"Você bebe a fúria do golpe. (+{cura} vida)", "verde")


def _redemoinho(cb, u, alvo):
    cb.dizer("Você gira a arma num arco brutal!", "ciano")
    for ini in cb.inimigos_vivos():
        cb.atacar(u, ini, 1.1)


def _furia_cega(cb, u, alvo):
    custo = int(u.max_hp * 0.15)
    u.hp = max(1, u.hp - custo)
    u.aplicar("fortalecido", 3, 0.6)
    cb.dizer(f"Você morde o próprio lábio até sangrar e deixa a fúria tomar conta. (-{custo} vida, dano +60%)",
             "vermelho+negrito")
    cb.atacar(u, alvo, 1.3, rotulo="Fúria Cega")


# --- Arqueiro ----------------------------------------------------------
def _tiro_certeiro(cb, u, alvo):
    cb.atacar(u, alvo, 1.7, alcance="distancia", crit_extra=0.3, rotulo="Tiro Certeiro")


def _marcar_presa(cb, u, alvo):
    alvo.aplicar("marcado", 3, 0.25)
    cb.dizer(f"Você estuda os movimentos de {alvo.nome} e encontra os pontos fracos. (+25% dano recebido)", "ciano")


def _chuva_flechas(cb, u, alvo):
    cb.dizer("Você dispara uma saraivada de flechas para o alto...", "ciano")
    for ini in cb.inimigos_vivos():
        cb.atacar(u, ini, 1.0, alcance="distancia")


def _passo_agil(cb, u, alvo):
    u.aplicar("esquiva", 2, 0.4)
    cb.dizer("Você se move em zigue-zague, difícil de acertar. (+40% esquiva)", "ciano")


def _tiro_duplo(cb, u, alvo):
    cb.atacar(u, alvo, 0.9, alcance="distancia", rotulo="Tiro Duplo (1)")
    if alvo.vivo:
        cb.atacar(u, alvo, 0.9, alcance="distancia", rotulo="Tiro Duplo (2)")


def _comando_fera(cb, u, alvo):
    fera = cb.companheiro
    cb.dizer(f"\"Agora!\" — {fera.nome} salta sobre o inimigo!", "ciano")
    dano = cb.atacar(fera, alvo, 2.0, alcance="corpo", rotulo="Comando")
    if dano and fera.tipo == "urso":
        cb.aplicar(alvo, "atordoado", 1, chance=0.6)
    elif dano and fera.tipo == "lobo":
        cb.aplicar(alvo, "sangramento", 3, valor=max(2, fera.atk * 0.4))


def _req_fera(cb):
    if not cb.companheiro or not cb.companheiro.vivo:
        return "Seu companheiro não está em condições de lutar."
    return None


def _furia_natureza(cb, u, alvo):
    cb.dizer("Você assobia. A mata responde: vento, espinhos e flechas em uníssono!", "verde+negrito")
    for ini in cb.inimigos_vivos():
        cb.atacar(u, ini, 1.3, alcance="distancia")
        if ini.vivo:
            cb.aplicar(ini, "sangramento", 3, valor=max(2, u.atk * 0.3), chance=0.5)
    if cb.companheiro and cb.companheiro.vivo:
        cb.companheiro.curar(cb.companheiro.max_hp)
        cb.dizer(f"{cb.companheiro.nome} se ergue revigorado.", "verde")


def _desaparecer(cb, u, alvo):
    u.aplicar("furtivo", 3, 1)
    u.aplicar("esquiva", 1, 0.5)
    cb.dizer("Você se funde às sombras. Seu próximo ataque será crítico.", "magenta")


def _flecha_envenenada(cb, u, alvo):
    dano = cb.atacar(u, alvo, 1.0, alcance="distancia", rotulo="Flecha Envenenada")
    if dano:
        cb.aplicar(alvo, "veneno", 4, valor=max(3, u.atk * 0.45 + u.agi * 0.2))


def _execucao(cb, u, alvo):
    mult = 1.2
    if alvo.hp <= alvo.max_hp * 0.35:
        mult = 3.2
        cb.dizer("Você vê a abertura perfeita...", "magenta")
    cb.atacar(u, alvo, mult, alcance="distancia", crit_extra=0.2, rotulo="Execução")


# --- Mago --------------------------------------------------------------
def _bola_fogo(cb, u, alvo):
    dano = cb.atacar(u, alvo, 1.5, tipo="fogo", alcance="distancia", stat="poder", rotulo="Bola de Fogo")
    if dano:
        cb.aplicar(alvo, "queimadura", cb.duracao_queimadura(u), valor=cb.valor_queimadura(u),
                   chance=1.0 if u.tal("ignicao") else 0.4)


def _meditar(cb, u, alvo):
    ganho = min(u.max_rec - u.rec, 8 + int(u.poder * 0.4))
    u.rec += ganho
    cb.dizer(f"Você fecha os olhos e respira fundo. (+{ganho} mana)", "azul")


def _lanca_gelo(cb, u, alvo):
    dano = cb.atacar(u, alvo, 1.3, tipo="gelo", alcance="distancia", stat="poder", rotulo="Lança de Gelo")
    if dano:
        cb.aplicar(alvo, "atordoado", 1, chance=0.35, rotulo="congelado")


def _barreira(cb, u, alvo):
    valor = int(u.poder * 0.9 * (1.3 if u.tal("escudo_reflexo") else 1))
    u.remover("barreira")  # não acumula
    u.aplicar("barreira", 2 + u.tal("escudo_reflexo"), valor)
    cb.dizer(f"Runas brilhantes giram ao seu redor. (absorve {valor} de dano)", "azul")


def _inferno(cb, u, alvo):
    cb.dizer("O chão se abre em chamas sob seus inimigos!", "vermelho+negrito")
    for ini in cb.inimigos_vivos():
        dano = cb.atacar(u, ini, 0.75, tipo="fogo", alcance="distancia", stat="poder", pode_esquivar=False)
        if dano and ini.vivo:
            cb.aplicar(ini, "queimadura", cb.duracao_queimadura(u), valor=cb.valor_queimadura(u), chance=0.45)


def _combustao(cb, u, alvo):
    mult = 1.3
    if alvo.efeito("queimadura"):
        mult = 2.6
        alvo.remover("queimadura")
        cb.dizer(f"As chamas em {alvo.nome} explodem!", "vermelho")
    cb.atacar(u, alvo, mult, tipo="fogo", alcance="distancia", stat="poder", rotulo="Combustão")


def _fenix(cb, u, alvo):
    cb.dizer("Asas de fogo se abrem às suas costas. Você se torna a própria chama!", "amarelo+negrito")
    cb.atacar(u, alvo, 2.5, tipo="fogo", alcance="distancia", stat="poder", rotulo="Fênix")
    cura = u.curar(u.max_hp * 0.2)
    if cura:
        cb.dizer(f"O fogo renova sua carne. (+{cura} vida)", "verde")


def _drenar_vida(cb, u, alvo):
    dano = cb.atacar(u, alvo, 1.2, tipo="sombra", alcance="distancia", stat="poder", rotulo="Drenar Vida")
    if dano:
        cura = u.curar(dano * (0.5 + 0.2 * u.tal("pacto_sombrio")))
        if cura:
            cb.dizer(f"A vitalidade roubada flui para você. (+{cura} vida)", "verde")


def _erguer_servo(cb, u, alvo):
    servos = [a for a in cb.aliados if getattr(a, "tipo", "") == "servo" and a.vivo]
    maximo = 1 + u.tal("exercito")
    if len(servos) >= maximo:
        cb.dizer("Você não consegue controlar mais servos. O esforço se perde no ar.", "cinza")
        return
    origem = "dos ossos de um inimigo caído" if cb.mortos else "da própria terra"
    cb.dizer(f"Você ergue um servo esquelético {origem}!", "magenta")
    vida = (u.poder * 1.6 + 8) * (1 + 0.25 * u.tal("pacto_sombrio"))
    cb.invocar_aliado("Servo Esquelético", hp=int(vida), atk=int(u.poder * 0.45) + 2, tipo="servo")


def _maldicao(cb, u, alvo):
    for ini in cb.inimigos_vivos():
        cb.aplicar(ini, "maldito", 4, valor=max(3, u.poder * 0.4))
    cb.dizer("Você pronuncia palavras que não deveriam existir. Seus inimigos murcham.", "magenta")


HABILIDADES = {
    # Guerreiro
    "golpe_pesado": dict(nome="Golpe Pesado", custo=10, alvo="inimigo", desc="170% de dano físico.", fn=_golpe_pesado),
    "erguer_escudo": dict(nome="Erguer Escudo", custo=8, alvo="proprio", desc="Reduz o dano recebido pela metade por 2 turnos.", fn=_erguer_escudo),
    "investida": dict(nome="Investida", custo=12, alvo="inimigo", desc="120% de dano, 45% de chance de atordoar.", fn=_investida),
    "grito_guerra": dict(nome="Grito de Guerra", custo=14, alvo="proprio", desc="+30% de dano por 3 turnos e enfraquece inimigos.", fn=_grito_guerra),
    "golpe_sagrado": dict(nome="Golpe Sagrado", custo=15, alvo="inimigo", desc="Dano sagrado que cura você em 35% do dano.", fn=_golpe_sagrado),
    "prece": dict(nome="Prece", custo=20, alvo="proprio", desc="Cura 30% da vida + poder e remove males.", fn=_prece),
    "julgamento": dict(nome="Julgamento Divino", custo=28, alvo="todos", desc="Luz sagrada atinge todos os inimigos.", fn=_julgamento),
    "sede_sangue": dict(nome="Sede de Sangue", custo=12, alvo="inimigo", desc="140% de dano, rouba vida e causa sangramento.", fn=_sede_sangue),
    "redemoinho": dict(nome="Redemoinho", custo=16, alvo="todos", desc="Atinge todos os inimigos com 110% de dano.", fn=_redemoinho),
    "furia_cega": dict(nome="Fúria Cega", custo=0, alvo="inimigo", desc="Sacrifica 15% da vida: +60% de dano por 3 turnos e ataca.", fn=_furia_cega),
    # Arqueiro
    "tiro_certeiro": dict(nome="Tiro Certeiro", custo=8, flechas=1, alvo="inimigo", desc="170% de dano, +30% chance de crítico.", fn=_tiro_certeiro),
    "marcar_presa": dict(nome="Marcar Presa", custo=6, alvo="inimigo", desc="O alvo recebe +25% de dano por 3 turnos.", fn=_marcar_presa),
    "chuva_flechas": dict(nome="Chuva de Flechas", custo=14, flechas=3, alvo="todos", desc="Atinge todos os inimigos (3 flechas).", fn=_chuva_flechas),
    "passo_agil": dict(nome="Passo Ágil", custo=6, alvo="proprio", desc="+40% de esquiva por 2 turnos.", fn=_passo_agil),
    "tiro_duplo": dict(nome="Tiro Duplo", custo=10, flechas=2, alvo="inimigo", desc="Dois disparos de 90%.", fn=_tiro_duplo),
    "comando_fera": dict(nome="Comando: Atacar!", custo=12, alvo="inimigo", desc="Seu companheiro desfere um ataque de 200%.", fn=_comando_fera, req=_req_fera),
    "furia_natureza": dict(nome="Fúria da Natureza", custo=25, flechas=4, alvo="todos", desc="130% em todos, sangramento e cura o companheiro.", fn=_furia_natureza),
    "desaparecer": dict(nome="Desaparecer", custo=10, alvo="proprio", desc="Próximo ataque é crítico devastador; +esquiva.", fn=_desaparecer),
    "flecha_envenenada": dict(nome="Flecha Envenenada", custo=10, flechas=1, alvo="inimigo", desc="Dano e veneno forte por 4 turnos.", fn=_flecha_envenenada),
    "execucao": dict(nome="Execução", custo=16, flechas=1, alvo="inimigo", desc="320% de dano se o alvo estiver abaixo de 35% de vida.", fn=_execucao),
    # Mago
    "bola_fogo": dict(nome="Bola de Fogo", custo=14, alvo="inimigo", desc="150% de dano de fogo, pode queimar.", fn=_bola_fogo),
    "meditar": dict(nome="Meditar", custo=0, alvo="proprio", desc="Recupera mana.", fn=_meditar),
    "lanca_gelo": dict(nome="Lança de Gelo", custo=10, alvo="inimigo", desc="130% de dano de gelo, pode congelar.", fn=_lanca_gelo),
    "barreira": dict(nome="Barreira Arcana", custo=18, alvo="proprio", desc="Escudo que absorve dano por 2 turnos (não acumula).", fn=_barreira),
    "inferno": dict(nome="Inferno", custo=32, alvo="todos", desc="75% de dano de fogo em todos, pode queimar.", fn=_inferno),
    "combustao": dict(nome="Combustão", custo=14, alvo="inimigo", desc="Dano dobrado em alvos em chamas (consome a queimadura).", fn=_combustao),
    "fenix": dict(nome="Fênix", custo=40, alvo="inimigo", desc="250% de dano de fogo e cura 20% da vida.", fn=_fenix),
    "drenar_vida": dict(nome="Drenar Vida", custo=14, alvo="inimigo", desc="Dano sombrio que cura 50% do causado.", fn=_drenar_vida),
    "erguer_servo": dict(nome="Erguer Servo", custo=22, alvo="proprio", desc="Invoca um esqueleto aliado (máx. 1, mais com talentos).", fn=_erguer_servo),
    "maldicao": dict(nome="Maldição", custo=18, alvo="todos", desc="Amaldiçoa todos: dano contínuo e -40% de defesa.", fn=_maldicao),
}


def habilidades_ate(classe, spec, nivel):
    lista = [h for (nv, h) in CLASSES[classe]["habilidades"] if nv <= nivel]
    if spec:
        lista += [h for (nv, h) in SPECS[spec]["habilidades"] if nv <= nivel]
    return lista
