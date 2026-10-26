"""O conteúdo provisório da segunda versão do protótipo de combate e atributos (26/10/2026; nada no jogo).

O que mudou desde a primeira (motor/, preservada para comparar), pela revisão da seção 3.7 do 25:
- os atributos ofensivos entram direto no dano (Força no físico, Intelecto no sobrenatural), junto da arma ou do foco,
  do nível e da habilidade;
- nenhum desbloqueio por atingir X: cada ponto dá um ganho gradual, com tetos de segurança;
- Presença fica fora do orçamento de combate e só aparece fora da luta;
- Vontade testa a Tenacidade (chance de resistir a controle, com teto);
- o protagonista monta o kit com pontos por tier, até uma ultimate; Atacar, Defender e Usar item ficam fora do kit.

Valores de teste, não catálogo: servem para observar decisões, não para balancear a campanha. Tudo o que é dado
artificialmente para testar uma regra está marcado como "condição de teste"."""

ATRIBUTOS = ("forca", "agilidade", "constituicao", "intelecto", "percepcao", "vontade")  # os de combate
NOME_ATRIBUTO = {"forca": "Força", "agilidade": "Agilidade", "constituicao": "Constituição", "intelecto": "Intelecto",
                 "percepcao": "Percepção", "vontade": "Vontade", "presenca": "Presença"}
SIGLA = {"forca": "FOR", "agilidade": "AGI", "constituicao": "CON", "intelecto": "INT", "percepcao": "PER",
         "vontade": "VON", "presenca": "PRE"}
FUNCAO = {"forca": "dano físico", "agilidade": "ordem inicial", "constituicao": "vida e resistência corporal",
          "intelecto": "dano sobrenatural", "percepcao": "crítico e ponto fraco", "vontade": "Tenacidade",
          "presenca": "só fora da luta"}
ORCAMENTO = 30            # a soma dos seis atributos de combate do protagonista
ATRIBUTO_MIN, ATRIBUTO_MAX = 1, 10
PRESENCA_PADRAO = 4       # Presença: de 1 a 10, fora do orçamento (não custa potência de luta)

# ---------------------------------------------------------------- o equipamento (para comparar uma peça só)
EQUIPAMENTO = {
    "arma": {"comum": {"nome": "Espada comum", "valor": 5},
             "reforcada": {"nome": "Espada reforçada", "valor": 7},
             "mestre": {"nome": "Espada de mestre", "valor": 9}},
    "foco": {"simples": {"nome": "Amuleto simples", "valor": 3},
             "runico": {"nome": "Amuleto rúnico", "valor": 6}},
}
EQUIPAMENTO_PADRAO = {"arma": "comum", "foco": "simples"}

# ---------------------------------------------------------------- o recurso (revisto em conjunto: custos, reserva, recuperação)
RECURSO_MAX = 60
RECURSO_INICIO = 40       # era 30 de 60
RECURSO_TURNO = 8         # novo: no início de cada turno do personagem
RECURSO_BASICO = 8        # o ataque básico recupera mais 8 (era 10, sem recuperação por turno)
IMPETO_ULTIMATE = 3       # a ultimate pede 3 de Ímpeto (ver regras.py)

# ---------------------------------------------------------------- o kit do protagonista
KIT_PONTOS = 10           # pontos para montar o kit (não são de aprender nem o recurso da luta)
KIT_ESPACOS = 6           # hipótese: até seis
PONTOS_TIER = {1: 1, 2: 2, 3: 3, "ultimate": 4}
BASICOS = ("atacar", "defender")  # fora do kit e do orçamento; o item também (os consumíveis)

# tipo: "fisico" (arma + nível + Força) ou "sobrenatural" (foco + nível + Intelecto).
# alvo: "inimigo", "inimigos" (todos), "aliado", "aliado_caido", "proprio", "grupo".
HABILIDADES = {
    # os comandos básicos (todos os aliados)
    "atacar": {"nome": "Atacar", "alvo": "inimigo", "custo": 0, "ganha": RECURSO_BASICO, "mult": 1.0, "tipo": "fisico",
               "basico": True, "desc": f"Golpe com a arma. Recupera {RECURSO_BASICO} a mais."},
    "defender": {"nome": "Defender", "alvo": "proprio", "custo": 0, "basico": True,
                 "desc": "−40% de dano recebido até o início do seu próximo turno."},
    # o protagonista: as que se escolhem para o kit
    "corte": {"nome": "Corte Preciso", "tier": 1, "alvo": "inimigo", "custo": 10, "mult": 1.2, "tipo": "fisico",
              "ignora": 3, "desc": "Golpe barato que ignora 3 de proteção."},
    "proteger": {"nome": "Proteger", "tier": 1, "alvo": "aliado", "custo": 15,
                 "desc": "Os golpes contra o aliado vêm para você até o início do seu próximo turno."},
    "comando": {"nome": "Grito de Comando", "tier": 1, "alvo": "aliado", "custo": 15, "bonus": 0.3,
                "desc": "O próximo golpe do aliado +30% (até o fim da próxima rodada); tira o Terror dele."},
    "golpe_pesado": {"nome": "Golpe Pesado", "tier": 2, "alvo": "inimigo", "custo": 25, "mult": 1.8, "tipo": "fisico",
                     "rompe": True, "desc": "Dano alto. Rompe da Guarda do alvo o quanto você tem de Força."},
    "lamina": {"nome": "Lâmina Rúnica", "tier": 2, "alvo": "inimigo", "custo": 20, "mult": 1.7, "tipo": "sobrenatural",
               "desc": "Dano sobrenatural (foco + nível + Intelecto); a Guarda não reduz."},
    "escudo_golpe": {"nome": "Golpe de Escudo", "tier": 2, "alvo": "inimigo", "custo": 30, "mult": 0.6, "tipo": "fisico",
                     "interrompe": True, "controle": "atordoado", "aplicacao": 0.10,
                     "desc": "Desfaz a preparação do alvo e tenta atordoá-lo (a Tenacidade dele resiste)."},
    "desafio": {"nome": "Desafio", "tier": 3, "alvo": "proprio", "custo": 25,
                "desc": "Até o início do seu próximo turno, os golpes e preparações de alvo único dos inimigos miram "
                        "você, e você recebe −25%."},
    # as ultimates (no máximo uma no kit; pedem Ímpeto, não recurso)
    "furia": {"nome": "Fúria do Campeão", "tier": "ultimate", "alvo": "inimigos", "custo": 0, "mult": 1.4,
              "tipo": "fisico", "impeto": True, "desc": "Golpe físico em todos os inimigos."},
    "tempestade": {"nome": "Tempestade Rúnica", "tier": "ultimate", "alvo": "inimigos", "custo": 0, "mult": 1.4,
                   "tipo": "sobrenatural", "impeto": True, "desc": "Dano sobrenatural em todos os inimigos."},
    "juramento": {"nome": "Juramento", "tier": "ultimate", "alvo": "grupo", "custo": 0, "impeto": True,
                  "desc": "Até o início do seu próximo turno: o grupo recebe −50% e não sofre controle."},
    # Odette (kit fixo)
    "lampejo": {"nome": "Lampejo", "alvo": "inimigo", "custo": 10, "mult": 1.2, "tipo": "sobrenatural",
                "desc": "Dano sobrenatural barato."},
    "curar": {"nome": "Curar", "alvo": "aliado", "custo": 20, "cura": 16,
              "desc": "Cura 16 + 2 × nível + o símbolo sagrado (sem atributo nesta versão)."},
    "escudo_luz": {"nome": "Escudo de Luz", "alvo": "aliado", "custo": 15, "escudo": 18,
                   "desc": "Absorve 18 de dano até o fim da próxima rodada."},
    "reerguer": {"nome": "Reerguer", "alvo": "aliado_caido", "custo": 50, "uma_vez": True, "volta": 0.3,
                 "desc": "Ressurreição de alto custo: o aliado volta com 30% da vida. Uma vez por luta."},
    # Morel (kit fixo)
    "joelho": {"nome": "Golpe no Joelho", "alvo": "inimigo", "custo": 30, "mult": 0.6, "tipo": "fisico",
               "interrompe": True, "controle": "atordoado", "aplicacao": 0.10,
               "desc": "Desfaz a preparação do alvo e tenta atordoá-lo (a Tenacidade dele resiste)."},
    "marcar": {"nome": "Marcar", "alvo": "inimigo", "custo": 10, "marca": 0.4,
               "desc": "O próximo golpe de outro aliado no alvo +40% (até o fim da próxima rodada)."},
}
CONSUMIVEIS = {
    "pocao": {"nome": "Poção de Vida", "alvo": "aliado", "cura": 30, "desc": "Cura 30 de vida.", "icone": "pocao_vida"},
    "pena": {"nome": "Pena de Fênix", "alvo": "aliado_caido", "volta": 0.4, "icone": "pena_fenix",
             "desc": "Item escasso: o aliado caído volta com 40% da vida."},
}

# ---------------------------------------------------------------- as construções do protagonista
# A mesma arma, o mesmo foco, o mesmo nível e os mesmos companheiros; mudam os 30 pontos e o kit sugerido.
BUILDS = {
    "forca": {"nome": "Força", "frase": "Bate forte com a arma e aguenta; age tarde.",
              "ganha": "o maior dano físico e boa vida", "abre_mao": "da iniciativa, do crítico e da magia",
              "atributos": dict(forca=9, agilidade=3, constituicao=7, intelecto=1, percepcao=4, vontade=6),
              "kit": ["golpe_pesado", "proteger", "comando", "escudo_golpe", "furia"]},
    "precisao": {"nome": "Precisão", "frase": "Age primeiro e acerta pontos fracos e críticos.",
                 "ganha": "iniciativa, crítico e ponto fraco", "abre_mao": "de vida e de Tenacidade",
                 "atributos": dict(forca=6, agilidade=8, constituicao=4, intelecto=1, percepcao=9, vontade=2),
                 "kit": ["corte", "golpe_pesado", "comando", "proteger", "escudo_golpe", "desafio"]},
    "runa": {"nome": "Runa", "frase": "Luta com a lâmina rúnica: o Intelecto no lugar da Força.",
             "ganha": "dano sobrenatural que ignora a Guarda", "abre_mao": "do golpe físico e da vida",
             "atributos": dict(forca=2, agilidade=5, constituicao=5, intelecto=9, percepcao=4, vontade=5),
             "kit": ["lamina", "corte", "proteger", "escudo_golpe", "tempestade"]},
    "baluarte": {"nome": "Baluarte", "frase": "Segura as ameaças: muita vida e Tenacidade, dano menor.",
                 "ganha": "vida, Tenacidade e o Desafio", "abre_mao": "de dano e de iniciativa",
                 "atributos": dict(forca=5, agilidade=2, constituicao=9, intelecto=1, percepcao=3, vontade=10),
                 "kit": ["desafio", "proteger", "comando", "corte", "juramento"]},
}

# ---------------------------------------------------------------- o grupo
GRUPO = {
    "heroi": {"nome": "Jean", "retrato": "guerreiro", "papel": "protagonista", "nivel": 3, "vida_base": 40,
              "recurso": "Vigor", "protecao": 3},
    "odete": {"nome": "Odette", "retrato": "odete", "papel": "companheira", "feminino": True, "nivel": 3,
              "vida_base": 32, "recurso": "Fé", "protecao": 1, "arma": 3, "foco": 4, "simbolo": 4,
              "atributos": dict(forca=2, agilidade=4, constituicao=3, intelecto=6, percepcao=3, vontade=5),
              "kit": ["lampejo", "curar", "escudo_luz", "reerguer"]},
    "morel": {"nome": "Morel", "retrato": "morel", "papel": "companheiro", "nivel": 3, "vida_base": 38,
              "recurso": "Vigor", "protecao": 2, "arma": 6, "foco": 0,
              "atributos": dict(forca=6, agilidade=5, constituicao=5, intelecto=1, percepcao=4, vontade=3),
              "kit": ["joelho", "marcar"]},
}

# ---------------------------------------------------------------- os inimigos
# Ajustes desde a primeira versão (registrados no LEIA-ME): a vida subiu ~60–70% porque o dano do grupo subiu com os
# atributos; o dano subiu um pouco porque a vida do grupo subiu; a Agilidade foi para a escala 1–10; os controles
# ganharam a Tenacidade; uma preparação já interrompida não pode ser interrompida de novo pelo mesmo inimigo.
INIMIGOS = {
    "lobo": {"nome": "Lobo", "retrato": "lobo", "vida": 56, "protecao": 0, "agi": 5, "per": 3, "dano": 9,
             "tenacidade": 0.0, "golpe": "Mordida"},
    "lobo_alfa": {"nome": "Lobo Alfa", "retrato": "lobo", "vida": 85, "protecao": 1, "agi": 6, "per": 4, "dano": 9,
                  "tenacidade": 0.10, "golpe": "Mordida",
                  "preparo": {"id": "bote", "nome": "Bote", "dano": 22, "sangra": 8, "em": (2, 5, 8),
                              "aviso": "abaixa e mira"}},
    "bruto": {"nome": "Bandido Bruto", "retrato": "bandido", "vida": 250, "protecao": 2, "agi": 2, "per": 2,
              "dano": 15, "tenacidade": 0.15, "golpe": "Porretada", "ponto_fraco": "o joelho enfaixado",
              "preparo": {"id": "esmagador", "nome": "Golpe Esmagador", "dano": 36, "controle": "atordoado",
                          "aplicacao": 0.10, "em": (2, 5, 8, 11), "aviso": "ergue o porrete com as duas mãos"}},
    "besteiro": {"nome": "Besteiro", "retrato": "mercenario", "vida": 64, "protecao": 1, "agi": 5, "per": 5,
                 "dano": 13, "tenacidade": 0.05, "golpe": "Virote"},
    "xama": {"nome": "Xamã Caído", "retrato": "xama_caido", "vida": 140, "protecao": 1, "agi": 4, "per": 4, "dano": 12,
             "tenacidade": 0.20, "golpe": "Garra",
             "preparo": {"id": "terror", "nome": "Grito de Terror", "area": True, "controle": "aterrorizado",
                         "aplicacao": 0.0, "em": (2, 5, 8), "aviso": "puxa o ar, o rosto se contorce"},
             "invoca": {"em": (1, 4, 7), "quem": "afogado", "max": 2}},
    "esqueleto": {"nome": "Soldado Morto", "retrato": "esqueleto", "vida": 110, "protecao": 2, "agi": 3, "per": 2,
                  "dano": 18, "tenacidade": 0.35, "golpe": "Espadada", "guarda": 6,
                  "ponto_fraco": "as juntas expostas"},
    "afogado": {"nome": "Afogado", "retrato": "afogado", "vida": 36, "protecao": 0, "agi": 1, "per": 1, "dano": 10,
                "tenacidade": 0.0, "golpe": "Agarrão", "invocado": True},
}

# ---------------------------------------------------------------- os encontros e os casos de teste
ENCONTROS = {
    "e1": {"nome": "1 · Os lobos da estrada", "tipo": "encontro", "semente": 11,
           "objetivo": "O tutorial: o recurso (todo turno recupera 8; o ataque, mais 8), o kit, a defesa, e o Lobo "
                       "Alfa anunciando o Bote antes de dar.",
           "inimigos": ["lobo_alfa", "lobo"], "consumiveis": {"pocao": 1}},
    "e2": {"nome": "2 · O bruto anunciado", "tipo": "encontro", "semente": 23,
           "objetivo": "O Bruto prepara o Golpe Esmagador a cada três rodadas. Interromper (uma vez só), proteger, "
                       "desafiar, defender ou curar: mais de uma resposta funciona, e os besteiros não param de atirar.",
           "inimigos": ["bruto", "besteiro", "besteiro"], "consumiveis": {"pocao": 1}},
    "e3": {"nome": "3 · O xamã e o soldado", "tipo": "encontro", "semente": 37,
           "objetivo": "O xamã chama afogados e prepara o Grito de Terror; o Soldado Morto bate forte atrás da guarda. "
                       "Quem derrubar primeiro e quando responder ao grito muda conforme a sequência.",
           "inimigos": ["xama", "esqueleto"], "consumiveis": {"pocao": 1}},
    "t1": {"nome": "Teste · atordoado e fim de rodada", "tipo": "teste", "semente": 5,
           "objetivo": "O protagonista começa atordoado: perde a primeira vez e a rodada termina mesmo assim.",
           "teste": "Condição de teste: o protagonista começa atordoado.", "inimigos": ["lobo"],
           "consumiveis": {}, "inicio": {"heroi": {"estados": ["atordoado"]}}},
    "t2": {"nome": "Teste · retorno antes da posição", "tipo": "teste", "semente": 7,
           "objetivo": "Morel está caído; o protagonista (antes de Morel) usa a Pena de Fênix nele: Morel age ainda "
                       "nesta rodada, na posição dele.",
           "teste": "Condições de teste: Morel começa caído; o protagonista começa com Agilidade 9 e uma Pena de Fênix.",
           "inimigos": ["lobo"], "consumiveis": {"pena": 1},
           "inicio": {"morel": {"caido": True}, "heroi": {"agilidade": 9}}},
    "t3": {"nome": "Teste · retorno depois da posição", "tipo": "teste", "semente": 9,
           "objetivo": "Morel está caído; a vez dele passa (pulada). Odette, depois dele na ordem, usa Reerguer: Morel "
                       "só age na próxima rodada.",
           "teste": "Condições de teste: Morel começa caído; Odette começa com a Fé cheia.",
           "inimigos": ["lobo"], "consumiveis": {},
           "inicio": {"morel": {"caido": True}, "odete": {"recurso": 60}}},
    "t4": {"nome": "Teste · inimigo derrotado antes da preparação", "tipo": "teste", "semente": 13,
           "objetivo": "O Lobo Alfa começa ferido e já preparando o Bote: derrubado antes da vez dele, o Bote não sai.",
           "teste": "Condições de teste: o Lobo Alfa começa com 8 de vida, Agilidade 1 (age por último) e o Bote já "
                    "preparado.",
           "inimigos": ["lobo_alfa"], "consumiveis": {},
           "inicio": {"lobo_alfa#1": {"vida": 8, "agilidade": 1, "preparando": True}}},
    "t5": {"nome": "Teste · Ímpeto pronto", "tipo": "teste", "semente": 17,
           "objetivo": "O protagonista começa com o Ímpeto cheio contra os lobos: para experimentar a ultimate do kit.",
           "teste": "Condição de teste: o protagonista começa com 3 de Ímpeto.",
           "inimigos": ["lobo_alfa", "lobo", "lobo"], "consumiveis": {},
           "inicio": {"heroi": {"impeto": 3}}},
}

# ---------------------------------------------------------------- uma situação de aventura (fora da luta)
# Os atributos fora da luta (Presença entre eles) e a contribuição de um companheiro, sem decidir pelo protagonista.
# Os testes de aventura podem ter dificuldade (é a situação, não um desbloqueio de combate).
SITUACAO = {
    "titulo": "A laje do ossuário",
    "texto": "Uma laje fecha a passagem. Há uma inscrição gasta na borda e uma fresta escura embaixo. Do outro lado, "
             "alguém respira e pergunta quem está aí.",
    "opcoes": [
        {"id": "erguer", "texto": "Erguer a laje", "atributo": "forca", "minimo": 7,
         "ok": "Você ergue a laje com as costas e passa por baixo.",
         "nao": "A laje não se mexe sozinha. Morel pode ajudar a erguer, mas o barulho chega lá embaixo.",
         "ajuda": {"quem": "morel", "texto": "Erguer com Morel (faz barulho: quem estiver embaixo ouve)"}},
        {"id": "fresta", "texto": "Procurar por onde a laje corre", "atributo": "percepcao", "minimo": 6,
         "ok": "Na fresta, um trilho de pedra: a laje corre de lado sem esforço.",
         "nao": "Só se vê escuro na fresta."},
        {"id": "ler", "texto": "Ler a inscrição", "atributo": "intelecto", "minimo": 6,
         "ok": "\"Quem desce, desce calado.\" Um aviso, não uma ameaça.",
         "nao": "As letras são antigas demais para você.",
         "ajuda": {"quem": "odete", "texto": "Pedir a Odette que leia (ela lê; tocar a laje ou não continua sendo escolha sua)"}},
        {"id": "falar", "texto": "Responder à voz e pedir que abram", "atributo": "presenca", "minimo": 6,
         "ok": "A voz hesita, ri baixo e puxa a laje por dentro: \"Desce, então.\"",
         "nao": "A voz se cala. Do outro lado, passos se afastam."},
    ],
}
