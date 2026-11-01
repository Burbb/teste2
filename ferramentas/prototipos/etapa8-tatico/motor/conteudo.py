"""O conteúdo provisório do protótipo tático da etapa 8 (nada no jogo): combate numa grade vista de cima, pelo
roadmapIDEIAS/29-ETAPA8-COMBATE-TATICO.md. Os números partem do X1 (etapa8-builds) para os encontros equivalentes;
são de teste, não catálogo.

A economia da vez (hipótese escolhida): **uma ação principal e pontos de movimento (PM)**, que se gastam antes e
depois da ação, em quantos trechos quiser. A ordem dos turnos é a do jogo (Agilidade), sem mudanças."""

VERSAO = "Tático 1 · 31/10/2026"
LARGURA, ALTURA = 9, 7
ZONA_CONTROLE = 1        # PM a mais para sair de uma casa vizinha a um inimigo (0 desliga)
MOVER_DEPOIS = False     # andar depois de agir na mesma vez (False: agir encerra o movimento da vez; seção 6 do 29)
COLISAO_CASA = 6         # dano por casa que o empurrão não percorreu (quem bate numa rocha, borda ou unidade)
FOGO_CHAO = 4            # dano de quem entra numa casa em chamas ou começa a vez nela (e 1 camada)
FOGO_RODADAS = 2         # duração das chamas no chão
PINGO_CAMADA = 3
DETONA_CAMADA = 9
CAMADAS_TETO = 3
PINGOS = 3
FICHA_TETO = 2
REGEN = 6
BASICO_GANHA = 6
LIMITE_RODADAS = 30

TIPOS = {"fisico": "físico", "fogo": "fogo", "sagrado": "sagrado", "sombra": "sombra"}

# ---------------------------------------------------------------- o grupo
HEROI = {
    "berserker": {"nome": "Jean", "spec": "Berserker", "retrato": "guerreiro", "vida": 64, "recurso": "Vigor",
                  "recurso_max": 60, "poder": 14, "agi": 5, "pm": 3,
                  "kit": ["golpe_pesado", "investida", "golpe_escudo", "corrente", "redemoinho", "guarda_costas"]},
    "piromante": {"nome": "Jean", "spec": "Piromante", "retrato": "mago", "vida": 52, "recurso": "Mana",
                  "recurso_max": 60, "poder": 14, "agi": 6, "pm": 3,
                  "kit": ["bola_fogo", "chuva", "muralha_fogo", "combustao", "explosao_calor", "sentinela"]},
}
COMPANHEIROS = {
    "morel": {"nome": "Morel", "retrato": "morel", "vida": 52, "recurso": "Vigor", "recurso_max": 50, "poder": 11,
              "agi": 7, "pm": 3, "kit": ["atacar", "oportuno", "proteger"]},
    "odete": {"nome": "Odette", "retrato": "odete", "vida": 44, "recurso": "Fé", "recurso_max": 50, "poder": 9,
              "agi": 4, "pm": 3, "kit": ["bastao", "luz", "prece", "bencao"]},
}
SENTINELA = {"nome": "Sentinela de Gelo", "vida": 34, "poder": 0, "agi": 0, "pm": 0}


def _h(nome, alvo, custo, desc, alcance=(1, 1), visao=True, linha=False, **extra):
    """alvo: inimigo | aliado | unidade | casa | casa_vazia | proprio. alcance: (mínimo, máximo) em casas.
    linha: só nas quatro direções retas. visao: precisa de linha de visão."""
    return dict(nome=nome, alvo=alvo, custo=custo, desc=desc, alcance=alcance, visao=visao, linha=linha, **extra)


HABILIDADES = {
    # comuns
    "atacar": _h("Atacar", "inimigo", 0, f"Causa 100% do Poder em dano físico. Recupera {BASICO_GANHA} a mais.",
                 mult=1.0, tipo="fisico"),
    "defender": _h("Defender", "proprio", 0, f"Ganha 1 Guarda. Recupera {BASICO_GANHA} a mais.", alcance=(0, 0)),

    # Berserker
    "golpe_pesado": _h("Golpe Pesado", "inimigo", 14, "Causa 140% do Poder em dano físico.", mult=1.4, tipo="fisico",
                       funcao="dano corpo a corpo"),
    "investida": _h("Investida", "inimigo", 12,
                    "Avança em linha reta até ficar ao lado do inimigo e causa 80% do Poder em dano físico. Não gasta "
                    "PM e não paga a zona de controle; precisa do caminho livre.",
                    alcance=(2, 4), linha=True, mult=0.8, tipo="fisico", funcao="chegar"),
    "golpe_escudo": _h("Golpe de Escudo", "inimigo", 10,
                       f"Causa 50% do Poder em dano físico e empurra o alvo 2 casas. Se ele bater numa rocha, na borda "
                       f"ou numa unidade, leva {COLISAO_CASA} por casa que faltou.",
                       mult=0.5, tipo="fisico", empurra=2, funcao="afastar uma ameaça"),
    "corrente": _h("Corrente", "inimigo", 12,
                   "Puxa o alvo em linha reta até ficar ao seu lado e causa 40% do Poder em dano físico.",
                   alcance=(2, 4), linha=True, mult=0.4, tipo="fisico", puxa=True, funcao="trazer quem está longe"),
    "redemoinho": _h("Redemoinho", "proprio", 18,
                     "Causa 60% do Poder em dano físico a cada inimigo nas 8 casas ao seu redor (diagonais também).",
                     alcance=(0, 0), mult=0.6, tipo="fisico", area="ao_redor", funcao="cercado, bater em todos"),
    "guarda_costas": _h("Guarda-costas", "proprio", 10,
                        "Até a sua próxima vez, os golpes contra aliados vizinhos a você vêm para você.",
                        alcance=(0, 0), funcao="proteger quem está perto"),

    # Piromante
    "bola_fogo": _h("Bola de Fogo", "inimigo", 12,
                    "Causa 100% do Poder em dano de fogo e acende 1 camada de Queimadura.",
                    alcance=(2, 5), mult=1.0, tipo="fogo", funcao="dano à distância"),
    "chuva": _h("Chuva de Brasas", "casa", 18,
                "Causa 45% do Poder em dano de fogo e acende 1 camada em cada unidade da área (a casa e as 4 "
                "vizinhas). Atinge aliados.", alcance=(1, 4), mult=0.45, tipo="fogo", area="cruz", raio=1,
                funcao="área que pede inimigos juntos"),
    "muralha_fogo": _h("Muralha de Fogo", "casa", 14,
                       f"Põe fogo em 3 casas em linha, de través para você, por {FOGO_RODADAS} rodadas. Quem entra "
                       f"numa casa em chamas ou começa a vez nela leva {FOGO_CHAO} de fogo e 1 camada.",
                       alcance=(1, 4), area="muralha", funcao="zona que muda caminhos"),
    "combustao": _h("Combustão", "inimigo", 14,
                    f"Detona a Queimadura do alvo: causa 40% do Poder + {DETONA_CAMADA} por camada em dano de fogo.",
                    alcance=(1, 5), mult=0.4, tipo="fogo", funcao="cobrar as camadas"),
    "explosao_calor": _h("Explosão de Calor", "proprio", 12,
                         "Causa 30% do Poder em dano de fogo a quem está nas 4 casas vizinhas e empurra cada um 2 "
                         "casas. Atinge aliados.", alcance=(0, 0), mult=0.3, tipo="fogo", empurra=2, area="vizinhas",
                         funcao="abrir espaço"),
    "sentinela": _h("Sentinela de Gelo", "casa_vazia", 16,
                    "Invoca a Sentinela (34 de vida) numa casa vazia: ela bloqueia a passagem e a visão, e os inimigos "
                    "que começam a vez ao lado dela têm 1 PM a menos. Chamar de novo troca a anterior.",
                    alcance=(1, 3), visao=False, funcao="invocação que fecha um caminho"),

    # Morel
    "oportuno": _h("Golpe Oportuno", "inimigo", 14,
                   "Causa 120% do Poder em dano físico; +60% em quem está atordoado, preparando um golpe ou cercado "
                   "(outro aliado ao lado dele).", mult=1.2, tipo="fisico"),
    "proteger": _h("Proteger", "aliado", 12, "Os golpes contra o aliado vizinho vêm para Morel até a próxima vez dele.",
                   alcance=(1, 1), visao=False),
    # Odette
    "bastao": _h("Bastão", "inimigo", 0, f"Causa 100% do Poder em dano sagrado. Recupera {BASICO_GANHA} a mais.",
                 mult=1.0, tipo="sagrado"),
    "luz": _h("Luz", "inimigo", 10, "Causa 90% do Poder em dano sagrado.", alcance=(2, 4), mult=0.9, tipo="sagrado"),
    "prece": _h("Prece", "aliado", 14, "Cura 18 de vida de um aliado ou da Sentinela.", alcance=(0, 3), cura=18),
    "bencao": _h("Bênção", "aliado", 10, "Um aliado ganha 1 Força.", alcance=(0, 3)),
}

# ---------------------------------------------------------------- os talentos: escolhas em pares
# Em cada par, escolha um (ou nenhum). Cada um muda o jeito de usar uma ferramenta no espaço.
TALENTOS = {
    "berserker": [
        {"id": "b1", "titulo": "A linha de frente", "opcoes": [
            {"id": "ancora", "afeta": ["golpe_escudo", "corrente", "guarda_costas"], "nome": "Âncora",
             "texto": "Sair de uma casa vizinha a você custa 2 PM a mais (além da zona de controle) para os inimigos."},
            {"id": "cacador", "afeta": ["golpe_pesado", "investida", "redemoinho"], "nome": "Caçador",
             "texto": "Quando você derruba um inimigo na sua vez, ganha 3 PM para andar nesta vez, mesmo depois de agir (uma vez por vez)."}]},
        {"id": "b2", "titulo": "O empurrão", "opcoes": [
            {"id": "colisao_brutal", "afeta": ["golpe_escudo"], "nome": "Colisão Brutal",
             "texto": "Quem você empurra contra algo leva o dobro da colisão e fica atordoado (perde a próxima vez)."},
            {"id": "arremesso", "afeta": ["golpe_escudo"], "nome": "Arremesso",
             "texto": "O Golpe de Escudo empurra 4 casas; se o empurrado bater numa unidade, ela leva a mesma colisão."}]},
    ],
    "piromante": [
        {"id": "p1", "titulo": "A área", "opcoes": [
            {"id": "seletivas", "afeta": ["chuva", "explosao_calor"], "nome": "Chamas Seletivas",
             "texto": "A Chuva de Brasas e a Explosão de Calor não atingem aliados (nem os empurram)."},
            {"id": "labareda", "afeta": ["chuva"], "nome": "Labareda",
             "texto": "A Chuva de Brasas atinge as casas a até 2 de distância do centro (13 casas). Atinge aliados."}]},
        {"id": "p2", "titulo": "O chão", "opcoes": [
            {"id": "rastro", "afeta": ["bola_fogo"], "nome": "Rastro de Brasas",
             "texto": f"A Bola de Fogo também põe fogo na casa do alvo, por {FOGO_RODADAS} rodadas."},
            {"id": "fogo_eterno", "afeta": ["muralha_fogo"], "nome": "Fogo Eterno", "texto": "As casas da Muralha de Fogo queimam até o fim da luta."}]},
        {"id": "p3", "titulo": "A detonação", "opcoes": [
            {"id": "estouro", "afeta": ["bola_fogo", "chuva", "combustao", "muralha_fogo"], "nome": "Estouro",
             "texto": "Um inimigo que morre em chamas explode: 6 + 3 por camada em dano de fogo nas 4 casas vizinhas, "
                      "e quem está nelas ganha 1 camada (aliados também). Cada um explode uma vez."},
            {"id": "combustao_area", "afeta": ["combustao"], "nome": "Combustão em Área",
             "texto": "A Combustão detona também a Queimadura dos inimigos nas 4 casas vizinhas ao alvo."}]},
    ],
}

# ---------------------------------------------------------------- os inimigos (os do X1, com movimento)
# papel: perto (vai até o alvo) | longe (procura uma casa com visão e distância) | lingua (puxa em linha).
INIMIGOS = {
    "lobo": {"nome": "Lobo", "retrato": "lobo", "vida": 42, "poder": 11, "agi": 6, "pm": 4, "papel": "perto",
             "habs": ["uivo"], "golpe": "Mordida"},
    "bandido": {"nome": "Bandido", "retrato": "bandido", "vida": 48, "poder": 12, "agi": 5, "pm": 3, "papel": "perto",
                "habs": ["golpe_sujo"], "golpe": "Facada"},
    "mercenario": {"nome": "Mercenário", "retrato": "mercenario", "vida": 80, "poder": 13, "agi": 4, "pm": 3,
                   "papel": "perto", "habs": ["esmagar", "grito"], "chance_hab": 0.45, "golpe": "Espadada"},
    "sapo": {"nome": "Sapo-touro", "retrato": "sapo", "vida": 62, "poder": 12, "agi": 4, "pm": 2, "papel": "lingua",
             "habs": [], "golpe": "Mordida"},
    "bruxa": {"nome": "Bruxa do Pântano", "retrato": "bruxa_brejo", "vida": 56, "poder": 9, "magia": 16, "agi": 5,
              "pm": 3, "papel": "longe", "habs": ["cura", "maldicao"], "golpe": "Bola de Fogo", "tipo": "fogo",
              "alcance": (2, 4)},
    "troll": {"nome": "Troll da Montanha", "retrato": "troll", "vida": 230, "poder": 21, "agi": 1, "pm": 2,
              "papel": "perto", "habs": ["esmagar", "regenerar"], "chance_hab": 0.45, "tracos": ["gigante"],
              "res": {"fogo": 1.4}, "golpe": "Pancada"},
}
HABS_INIMIGO = {
    "uivo": "Uivo: os inimigos ficam Fortalecidos (+30%) por 2 vezes deles.",
    "grito": "Grito de Guerra: os inimigos ficam Fortalecidos (+30%) por 2 vezes deles.",
    "golpe_sujo": "Golpe Sujo: 110% e 35% de chance de Enfraquecer (−30%) por 2 vezes do alvo.",
    "esmagar": "Golpe Esmagador: marca o alvo e as 4 casas vizinhas; na próxima vez dele, 220% em quem estiver "
               "nelas. Atordoar interrompe; sair das casas marcadas escapa.",
    "regenerar": "Regenerar: com 70% da vida ou menos, recupera 15% da vida máxima.",
    "lingua": "Língua: em linha reta, a 2 ou 3 casas e com visão, puxa o alvo até o lado dele e morde (80%).",
    "cura": "Cura: um inimigo a até 3 casas, abaixo de 60% da vida, recupera 25%. Uma vez a cada 3 rodadas.",
    "maldicao": "Maldição: a até 4 casas, com visão, o alvo fica Enfraquecido (−30%) por 2 vezes dele.",
}

# ---------------------------------------------------------------- os encontros (arena 9 × 7; x = coluna, y = linha)
GRUPO_INICIO = {"heroi": (1, 3), "morel": (2, 2), "odete": (0, 4)}
ENCONTROS = {
    "aberto": {"nome": "Campo aberto · três lobos", "semente": 101, "x1": "lobos",
               "objetivo": "Pouco obstáculo: o movimento vira só aproximação? Recuar e atacar vence sempre?",
               "rochas": [(4, 1), (4, 5)], "agua": [],
               "inimigos": [("lobo", (7, 2)), ("lobo", (8, 3)), ("lobo", (7, 4))]},
    "passagem": {"nome": "A passagem · o mercenário e dois bandidos", "semente": 202, "x1": "mercenario",
                 "objetivo": "Uma parede de rocha com uma passagem e um trecho de água (vê-se através, não se passa): "
                             "segurar, fechar ou usar a passagem.",
                 "rochas": [(4, 0), (4, 1), (4, 2), (4, 4)], "agua": [(4, 5), (4, 6)],
                 "inimigos": [("mercenario", (6, 3)), ("bandido", (7, 1)), ("bandido", (7, 5))]},
    "prioridades": {"nome": "Perto e longe · a bruxa, o bandido e o sapo", "semente": 303, "x1": "bruxa",
                    "objetivo": "A bruxa atira e cura de trás das rochas; o sapo puxa quem fica em linha; o bandido "
                                "vem na frente. Quem atacar primeiro, e como chegar.",
                    "rochas": [(7, 2), (7, 4), (3, 1), (3, 5)], "agua": [(6, 0), (6, 6)],
                    "inimigos": [("bruxa", (8, 3)), ("sapo", (6, 2)), ("bandido", (5, 4))]},
    "troll": {"nome": "O troll", "semente": 404, "x1": "troll",
              "objetivo": "Um gigante lento que prepara um golpe em área: sair das casas marcadas, bloquear, "
                          "empurrar.",
              "rochas": [(4, 2), (4, 4)], "agua": [],
              "inimigos": [("troll", (7, 3))]},
}
