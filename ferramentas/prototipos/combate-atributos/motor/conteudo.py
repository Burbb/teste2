"""O conteúdo provisório do protótipo de combate e atributos (25/10/2026; nada no jogo): o grupo, as distribuições de
atributos do protagonista, as habilidades, os inimigos, os encontros, os casos de teste e uma situação de aventura.
Valores de teste, não catálogo: servem para observar decisões, não para balancear a campanha.

Os números de potência saem do nível, da arma e da habilidade; os atributos mudam como as coisas funcionam
(regras.py). Tudo o que é dado artificialmente para testar uma regra está marcado como "condição de teste"."""

ATRIBUTOS = ("forca", "agilidade", "constituicao", "intelecto", "percepcao", "vontade", "presenca")
NOME_ATRIBUTO = {"forca": "Força", "agilidade": "Agilidade", "constituicao": "Constituição", "intelecto": "Intelecto",
                 "percepcao": "Percepção", "vontade": "Vontade", "presenca": "Presença"}
SIGLA = {"forca": "FOR", "agilidade": "AGI", "constituicao": "CON", "intelecto": "INT", "percepcao": "PER",
         "vontade": "VON", "presenca": "PRE"}
PONTOS_PROTAGONISTA = 24   # a soma dos sete atributos do protagonista
ATRIBUTO_MIN, ATRIBUTO_MAX = 1, 8

# As distribuições prontas do protagonista (o mesmo nível, a mesma arma, a mesma armadura, os mesmos companheiros).
DISTRIBUICOES = {
    "A": {"nome": "A · Força e Constituição", "resumo": "aguenta e rompe a guarda; age tarde",
          "atributos": dict(forca=7, agilidade=2, constituicao=6, intelecto=2, percepcao=2, vontade=3, presenca=2)},
    "B": {"nome": "B · Agilidade e Percepção", "resumo": "age cedo, acerta pontos fracos; frágil ao medo",
          "atributos": dict(forca=3, agilidade=6, constituicao=3, intelecto=2, percepcao=6, vontade=2, presenca=2)},
    "C": {"nome": "C · Vontade e Presença", "resumo": "resiste ao terror, defende melhor e comanda o grupo",
          "atributos": dict(forca=3, agilidade=3, constituicao=3, intelecto=3, percepcao=2, vontade=6, presenca=4)},
}

# ---------------------------------------------------------------- as habilidades (as do grupo)
# custo: no recurso de quem usa (Vigor ou Fé); alvo: "inimigo", "aliado", "aliado_caido", "proprio", "nenhum".
HABILIDADES = {
    # o protagonista (Guerreiro)
    "atacar": {"nome": "Atacar", "alvo": "inimigo", "custo": 0, "ganha": 10, "mult": 1.0,
               "desc": "Golpe confiável. Recupera 10 de recurso."},
    "golpe_pesado": {"nome": "Golpe Pesado", "alvo": "inimigo", "custo": 25, "mult": 1.8, "rompe": True,
                     "desc": "Dano alto. Rompe da Guarda do alvo o quanto você tem de Força (o golpe comum, 1)."},
    "proteger": {"nome": "Proteger", "alvo": "aliado", "custo": 15,
                 "desc": "Os golpes contra o aliado vêm para você até o início do seu próximo turno."},
    "comando": {"nome": "Grito de Comando", "alvo": "aliado", "custo": 20,
                "desc": "O próximo golpe do aliado causa mais dano (pela Presença) e o Terror sai dele."},
    "defender": {"nome": "Defender", "alvo": "proprio", "custo": 0,
                 "desc": "Reduz o dano recebido até o início do seu próximo turno (pela Vontade)."},
    # Odette (curandeira)
    "bastao": {"nome": "Bastão", "alvo": "inimigo", "custo": 0, "ganha": 10, "mult": 1.0,
               "desc": "Golpe simples. Recupera 10 de Fé."},
    "curar": {"nome": "Curar", "alvo": "aliado", "custo": 20, "cura": 24, "desc": "Cura 24 de vida."},
    "escudo_luz": {"nome": "Escudo de Luz", "alvo": "aliado", "custo": 15, "escudo": 16,
                   "desc": "Absorve 16 de dano até o fim da próxima rodada."},
    "reerguer": {"nome": "Reerguer", "alvo": "aliado_caido", "custo": 50, "uma_vez": True, "volta": 0.3,
                 "desc": "Ressurreição de alto custo: o aliado caído volta com 30% da vida. Uma vez por luta."},
    # Morel (mercenário)
    "golpe": {"nome": "Golpe", "alvo": "inimigo", "custo": 0, "ganha": 10, "mult": 1.0,
              "desc": "Golpe confiável. Recupera 10 de Vigor."},
    "joelho": {"nome": "Golpe no Joelho", "alvo": "inimigo", "custo": 30, "mult": 0.6, "interrompe": True,
               "desc": "Dano baixo; desfaz a preparação do alvo e o atordoa (perde a próxima vez), se não for firme."},
    "marcar": {"nome": "Marcar", "alvo": "inimigo", "custo": 10, "marca": 0.5,
               "desc": "O próximo golpe de outro aliado no alvo causa +50% e gasta a marca (até o fim da próxima rodada)."},
}
CONSUMIVEIS = {
    "pocao": {"nome": "Poção de Vida", "alvo": "aliado", "cura": 30, "desc": "Cura 30 de vida.", "icone": "pocao_vida"},
    "pena": {"nome": "Pena de Fênix", "alvo": "aliado_caido", "volta": 0.4, "icone": "pena_fenix",
             "desc": "Item escasso: o aliado caído volta com 40% da vida."},
}

# ---------------------------------------------------------------- o grupo
# Os companheiros têm atributos próprios (não se distribuem aqui) e um kit menor que o do protagonista.
GRUPO = {
    "heroi": {"nome": "Jean", "retrato": "guerreiro", "papel": "protagonista", "nivel": 3, "vida_base": 40,
              "recurso": "Vigor", "recurso_max": 60, "recurso_inicio": 30, "arma": 8, "protecao": 3,
              "kit": ["atacar", "golpe_pesado", "proteger", "comando", "defender"]},
    "odete": {"nome": "Odette", "retrato": "odete", "papel": "companheira", "feminino": True, "nivel": 3, "vida_base": 32,
              "recurso": "Fé", "recurso_max": 60, "recurso_inicio": 30, "arma": 5, "protecao": 1,
              "atributos": dict(forca=2, agilidade=4, constituicao=3, intelecto=5, percepcao=3, vontade=5, presenca=3),
              "kit": ["bastao", "curar", "escudo_luz", "reerguer", "defender"]},
    "morel": {"nome": "Morel", "retrato": "morel", "papel": "companheiro", "nivel": 3, "vida_base": 38,
              "recurso": "Vigor", "recurso_max": 60, "recurso_inicio": 30, "arma": 9, "protecao": 2,
              "atributos": dict(forca=5, agilidade=5, constituicao=4, intelecto=2, percepcao=4, vontade=3, presenca=2),
              "kit": ["golpe", "joelho", "marcar", "defender"]},
}

# ---------------------------------------------------------------- os inimigos
# agi: a posição na ordem. Os de preparação dizem quando preparam (`prepara_em`: as rodadas) e o que fazem.
INIMIGOS = {
    "lobo": {"nome": "Lobo", "retrato": "lobo", "vida": 26, "protecao": 0, "agi": 5, "per": 3, "dano": 8,
             "golpe": "Mordida"},
    "lobo_alfa": {"nome": "Lobo Alfa", "retrato": "lobo", "vida": 40, "protecao": 1, "agi": 6, "per": 4, "dano": 8,
                  "golpe": "Mordida",
                  "preparo": {"id": "bote", "nome": "Bote", "dano": 20, "sangra": True, "em": (2, 5, 8),
                              "alvo": "menos_vida", "aviso": "abaixa e mira"}},
    "bruto": {"nome": "Bandido Bruto", "retrato": "bandido", "vida": 110, "protecao": 2, "agi": 2, "per": 2, "dano": 14,
              "golpe": "Porretada", "ponto_fraco": "o joelho enfaixado",
              "preparo": {"id": "esmagador", "nome": "Golpe Esmagador", "dano": 34, "atordoa": True, "em": (2, 4, 6, 8),
                          "alvo": "menos_vida", "aviso": "ergue o porrete com as duas mãos"}},
    "besteiro": {"nome": "Besteiro", "retrato": "mercenario", "vida": 32, "protecao": 1, "agi": 5, "per": 5, "dano": 13,
                 "golpe": "Virote"},
    "xama": {"nome": "Xamã Caído", "retrato": "xama_caido", "vida": 65, "protecao": 1, "agi": 4, "per": 4, "dano": 9,
             "golpe": "Garra",
             "preparo": {"id": "terror", "nome": "Grito de Terror", "area": True, "terror": True, "em": (2, 5, 8),
                         "aviso": "puxa o ar, o rosto se contorce"},
             "invoca": {"em": (1, 4, 7), "quem": "afogado", "max": 2}},
    "esqueleto": {"nome": "Soldado Morto", "retrato": "esqueleto", "vida": 50, "protecao": 2, "agi": 3, "per": 2,
                  "dano": 14, "golpe": "Espadada", "guarda": 6, "firme": True, "ponto_fraco": "as juntas expostas"},
    "afogado": {"nome": "Afogado", "retrato": "afogado", "vida": 20, "protecao": 0, "agi": 1, "per": 1, "dano": 8,
                "golpe": "Agarrão", "invocado": True},
}

# ---------------------------------------------------------------- os encontros e os casos de teste
ENCONTROS = {
    "e1": {"nome": "1 · Os lobos da estrada", "tipo": "encontro", "semente": 11,
           "objetivo": "Aprender os controles, o recurso (o ataque básico recupera; as habilidades gastam) e a defesa: "
                       "o Lobo Alfa anuncia o Bote antes de dar.",
           "inimigos": ["lobo_alfa", "lobo"], "consumiveis": {"pocao": 1}},
    "e2": {"nome": "2 · O bruto anunciado", "tipo": "encontro", "semente": 23,
           "objetivo": "O Bruto prepara o Golpe Esmagador a cada duas rodadas. Interromper, proteger, defender ou "
                       "aguentar e curar: mais de uma resposta funciona, e os dois besteiros não param de atirar.",
           "inimigos": ["bruto", "besteiro", "besteiro"], "consumiveis": {"pocao": 1}},
    "e3": {"nome": "3 · O xamã e o soldado", "tipo": "encontro", "semente": 37,
           "objetivo": "O xamã chama afogados e prepara o Grito de Terror; o Soldado Morto bate forte atrás da guarda. "
                       "Quem derrubar primeiro e quando responder ao grito muda conforme a sequência.",
           "inimigos": ["xama", "esqueleto"], "consumiveis": {"pocao": 1}},
    # casos de teste: as condições artificiais estão em `teste`
    "t1": {"nome": "Teste · atordoado e fim de rodada", "tipo": "teste", "semente": 5,
           "objetivo": "O protagonista começa atordoado: perde a primeira vez e a rodada termina mesmo assim.",
           "teste": "Condição de teste: o protagonista começa atordoado.", "inimigos": ["lobo"],
           "consumiveis": {}, "inicio": {"heroi": {"estados": ["atordoado"]}}},
    "t2": {"nome": "Teste · retorno antes da posição", "tipo": "teste", "semente": 7,
           "objetivo": "Morel está caído; o protagonista (Agilidade 6, antes de Morel) usa a Pena de Fênix nele: Morel "
                       "age ainda nesta rodada, na posição dele.",
           "teste": "Condições de teste: Morel começa caído; o protagonista começa com Agilidade 6 e uma Pena de Fênix.",
           "inimigos": ["lobo"], "consumiveis": {"pena": 1},
           "inicio": {"morel": {"caido": True}, "heroi": {"agilidade": 6}}},
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
}

# ---------------------------------------------------------------- uma situação de aventura (fora da luta)
# Os atributos fora da luta e a contribuição de um companheiro, sem decidir pelo protagonista.
SITUACAO = {
    "titulo": "A laje do ossuário",
    "texto": "Uma laje fecha a passagem. Há uma inscrição gasta na borda e uma fresta escura embaixo.",
    "opcoes": [
        {"id": "erguer", "texto": "Erguer a laje", "atributo": "forca", "minimo": 5,
         "ok": "Você ergue a laje com as costas e passa por baixo.",
         "nao": "A laje não se mexe sozinha. Morel pode ajudar a erguer, mas o barulho chega lá embaixo.",
         "ajuda": {"quem": "morel", "texto": "Erguer com Morel (faz barulho: quem estiver embaixo ouve)"}},
        {"id": "fresta", "texto": "Procurar por onde a laje corre", "atributo": "percepcao", "minimo": 5,
         "ok": "Na fresta, um trilho de pedra: a laje corre de lado sem esforço.",
         "nao": "Só se vê escuro na fresta."},
        {"id": "ler", "texto": "Ler a inscrição", "atributo": "intelecto", "minimo": 5,
         "ok": "\"Quem desce, desce calado.\" Um aviso, não uma ameaça.",
         "nao": "As letras são antigas demais para você.",
         "ajuda": {"quem": "odete", "texto": "Pedir a Odette que leia (ela lê; tocar a laje ou não continua sendo escolha sua)"}},
    ],
}
