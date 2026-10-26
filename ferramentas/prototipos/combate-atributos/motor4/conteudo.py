"""O conteúdo provisório da quarta versão do protótipo de combate e atributos (26/10/2026; nada no jogo): um refinamento
pequeno da terceira (motor3/, preservada), pela seção 3.9 do 25:
- a Marca do Morel saiu; no lugar, para testar, o Golpe Oportuno (efeito imediato, sem preparação);
- o conjunto de fogo ganhou a Chuva de Brasas: pouco dano em área e uma camada de Queimadura em cada inimigo;
- o resto (atributos, recurso, encontros, as outras habilidades) é o da terceira.

O que a terceira já tinha mudado desde a segunda (motor2/), pela seção 3.8 do 25:
- toda habilidade diz o tipo de dano (físico, arcano, fogo), o que escala a potência e com que defesa se encontra;
- resistências percentuais por tipo (arcano e fogo), com teto, vindas do equipamento do protagonista e de alguns
  inimigos; o físico continua contra a proteção;
- o Baluarte ganha o Avanço do Baluarte, físico com parte da vida máxima;
- Vontade aumenta o recurso máximo (além da Tenacidade, ainda em avaliação); a reserva começa cheia;
- uma combinação pequena de aplicar e consumir queimadura (a especialização de demonstração "Lâmina e Chama", que se
  soma às habilidades do Guerreiro);
- a ultimate sem Ímpeto: uma utilização por combatente por luta, desde o início, com custo de recurso;
- as preparações dos inimigos contam os turnos em que eles agem (atordoar adia, não apaga); sem a regra geral de
  "firme depois da primeira interrupção"; um golpe específico ininterruptível, sinalizado.

Valores de teste, não catálogo: servem para observar decisões, não para balancear a campanha."""

ATRIBUTOS = ("forca", "agilidade", "constituicao", "intelecto", "percepcao", "vontade")  # os de combate
NOME_ATRIBUTO = {"forca": "Força", "agilidade": "Agilidade", "constituicao": "Constituição", "intelecto": "Intelecto",
                 "percepcao": "Percepção", "vontade": "Vontade", "presenca": "Presença", "vida": "vida máxima",
                 "nivel": "nível"}
SIGLA = {"forca": "FOR", "agilidade": "AGI", "constituicao": "CON", "intelecto": "INT", "percepcao": "PER",
         "vontade": "VON", "presenca": "PRE", "vida": "vida máx."}
FUNCAO = {"forca": "dano físico", "agilidade": "ordem inicial", "constituicao": "vida e resistência corporal",
          "intelecto": "dano arcano e de fogo", "percepcao": "crítico e ponto fraco",
          "vontade": "recurso máximo e Tenacidade", "presenca": "só fora da luta"}
ORCAMENTO = 30
ATRIBUTO_MIN, ATRIBUTO_MAX = 1, 10
PRESENCA_PADRAO = 4

TIPOS = {"fisico": "Físico", "arcano": "Arcano", "fogo": "Fogo"}
DEFESA_TIPO = {"fisico": "proteção (subtrai)", "arcano": "resistência arcana (%)", "fogo": "resistência ao fogo (%)"}
RESISTENCIA_TETO = 0.60

# ---------------------------------------------------------------- o equipamento (para comparar uma peça só)
EQUIPAMENTO = {
    "arma": {"comum": {"nome": "Espada comum", "valor": 5},
             "reforcada": {"nome": "Espada reforçada", "valor": 7},
             "mestre": {"nome": "Espada de mestre", "valor": 9}},
    "foco": {"simples": {"nome": "Amuleto simples", "valor": 3},
             "runico": {"nome": "Amuleto rúnico", "valor": 6}},
    "manto": {"comum": {"nome": "Manto de viagem", "valor": 0, "res": {}},
              "salamandra": {"nome": "Manto de couro de salamandra", "valor": 0, "res": {"fogo": 0.35}},
              "runico": {"nome": "Manto bordado de runas", "valor": 0, "res": {"arcano": 0.35}}},
}
EQUIPAMENTO_PADRAO = {"arma": "comum", "foco": "simples", "manto": "comum"}

# ---------------------------------------------------------------- o recurso: reserva e regeneração
RECURSO_BASE = 40          # da classe
RECURSO_NIVEL = 4          # por nível: 52 no nível 3
RECURSO_VONTADE = 3        # por ponto de Vontade
RECURSO_TURNO = 6          # regeneração: no início de cada turno do personagem
RECURSO_BASICO = 6         # o ataque básico recupera mais 6
# A reserva começa cheia: é a capacidade de uma sequência intensa; a regeneração sustenta a luta longa.

# ---------------------------------------------------------------- o kit do protagonista
KIT_PONTOS = 10
KIT_ESPACOS = 6
PONTOS_TIER = {1: 1, 2: 2, 3: 3, "ultimate": 4}
BASICOS = ("atacar", "defender")  # fora do kit e do orçamento; o item também
ORIGEM = {"guerreiro": "Guerreiro (classe inicial)",
          "chama": "Lâmina e Chama (especialização de demonstração: soma-se às do Guerreiro)"}

# Campos de uma habilidade de dano:
#   tipo: fisico | arcano | fogo;  base: "arma" | "foco" | None (só nível);  escala: {atributo|"vida": coeficiente}
#   mult: o multiplicador da habilidade;  ignora: proteção ignorada (físico);  penetra: resistência ignorada (%)
# alvo: inimigo | inimigos | aliado | aliado_caido | proprio | grupo.
HABILIDADES = {
    # os comandos básicos (todos os aliados)
    "atacar": {"nome": "Atacar", "alvo": "inimigo", "custo": 0, "ganha": RECURSO_BASICO, "mult": 1.0, "tipo": "fisico",
               "base": "arma", "escala": {"forca": 1.0}, "basico": True,
               "desc": f"Golpe com a arma. Recupera {RECURSO_BASICO} a mais."},
    "defender": {"nome": "Defender", "alvo": "proprio", "custo": 0, "basico": True,
                 "desc": "−40% de dano recebido até o início do seu próximo turno."},
    # Guerreiro
    "corte": {"nome": "Corte Preciso", "origem": "guerreiro", "tier": 1, "alvo": "inimigo", "custo": 10, "mult": 1.2,
              "tipo": "fisico", "base": "arma", "escala": {"forca": 1.0}, "ignora": 3,
              "desc": "Golpe barato que ignora 3 de proteção."},
    "proteger": {"nome": "Proteger", "origem": "guerreiro", "tier": 1, "alvo": "aliado", "custo": 15,
                 "desc": "Os golpes contra o aliado vêm para você até o início do seu próximo turno."},
    "comando": {"nome": "Grito de Comando", "origem": "guerreiro", "tier": 1, "alvo": "aliado", "custo": 15, "bonus": 0.3,
                "desc": "O próximo golpe do aliado +30% (até o fim da próxima rodada); tira o Terror dele."},
    "golpe_pesado": {"nome": "Golpe Pesado", "origem": "guerreiro", "tier": 2, "alvo": "inimigo", "custo": 25, "mult": 1.8,
                     "tipo": "fisico", "base": "arma", "escala": {"forca": 1.0}, "rompe": True,
                     "desc": "Dano alto. Rompe da Guarda do alvo o quanto você tem de Força."},
    "escudo_golpe": {"nome": "Golpe de Escudo", "origem": "guerreiro", "tier": 2, "alvo": "inimigo", "custo": 30,
                     "mult": 0.6, "tipo": "fisico", "base": "arma", "escala": {"forca": 1.0}, "interrompe": True,
                     "controle": "atordoado", "aplicacao": 0.10,
                     "desc": "Desfaz a preparação do alvo (se ela não for ininterruptível) e tenta atordoá-lo."},
    "avanco": {"nome": "Avanço do Baluarte", "origem": "guerreiro", "tier": 2, "alvo": "inimigo", "custo": 20, "mult": 1.0,
               "tipo": "fisico", "base": None, "escala": {"vida": 0.25}, "atrai": True,
               "desc": "Avança com o escudo: dano pela vida máxima (25%) + nível, sem a arma nem a Força. Até o início "
                       "do seu próximo turno, os golpes de alvo único dos inimigos miram você (sem redução)."},
    "desafio": {"nome": "Desafio", "origem": "guerreiro", "tier": 3, "alvo": "proprio", "custo": 25,
                "desc": "Até o início do seu próximo turno, os golpes e preparações de alvo único miram você, e você "
                        "recebe −25%."},
    "furia": {"nome": "Fúria do Campeão", "origem": "guerreiro", "tier": "ultimate", "alvo": "inimigos", "custo": 30,
              "mult": 0.9, "tipo": "fisico", "base": "arma", "escala": {"forca": 1.0}, "desfaz_todas": True,
              "contra_preparo": 1.0,
              "desc": "Golpe físico em todos os inimigos: +100% em quem está preparando, e desfaz as preparações "
                      "interrompíveis."},
    "juramento": {"nome": "Juramento", "origem": "guerreiro", "tier": "ultimate", "alvo": "grupo", "custo": 30,
                  "desc": "Até o início do seu próximo turno: o grupo recebe −50% e não sofre controle."},
    # Lâmina e Chama (demonstração)
    "brasa": {"nome": "Brasa", "origem": "chama", "tier": 1, "alvo": "inimigo", "custo": 12, "mult": 0.7, "tipo": "fogo",
              "base": "foco", "escala": {"intelecto": 1.0}, "queima": True,
              "desc": "Fogo leve que põe 1 pilha de Queimadura (até 3): cada pilha pinga 30% da potência no início "
                      "dos 3 próximos turnos do alvo."},
    "lamina": {"nome": "Lâmina Rúnica", "origem": "chama", "tier": 2, "alvo": "inimigo", "custo": 20, "mult": 1.7,
               "tipo": "arcano", "base": "foco", "escala": {"intelecto": 1.0}, "penetra": 0.10,
               "desc": "Dano arcano alto; ignora 10% da resistência arcana. A Guarda (física) não reduz."},
    "combustao": {"nome": "Combustão", "origem": "chama", "tier": 2, "alvo": "inimigo", "custo": 20, "mult": 0.6,
                  "tipo": "fogo", "base": "foco", "escala": {"intelecto": 1.0}, "consome": 2.0,
                  "desc": "Fogo que consome a Queimadura do alvo: soma 200% do dano que ela ainda faria. Sem "
                          "Queimadura, é um golpe fraco."},
    "chuva": {"nome": "Chuva de Brasas", "origem": "chama", "tier": 2, "alvo": "inimigos", "custo": 22, "mult": 0.35,
              "tipo": "fogo", "base": "foco", "escala": {"intelecto": 1.0}, "queima": True,
              "desc": "Pouco fogo em todos e 1 pilha de Queimadura em cada um (a resistência reduz o dano, não a "
                      "Queimadura)."},
    "tempestade": {"nome": "Tempestade Rúnica", "origem": "chama", "tier": "ultimate", "alvo": "inimigos", "custo": 30,
                   "mult": 0.8, "tipo": "arcano", "base": "foco", "escala": {"intelecto": 1.0}, "contra_estado": 1.0,
                   "desc": "Dano arcano em todos; +100% em quem está atordoado ou queimando."},
    "conflagracao": {"nome": "Conflagração", "origem": "chama", "tier": "ultimate", "alvo": "inimigos", "custo": 30,
                     "mult": 0.6, "tipo": "fogo", "base": "foco", "escala": {"intelecto": 1.0}, "consome": 2.0,
                     "desc": "Fogo em todos que consome a Queimadura de cada um (+200% do que ela ainda faria)."},
    # Odette (kit fixo, com uma ultimate para testar a utilização única com queda e retorno)
    "lampejo": {"nome": "Lampejo", "alvo": "inimigo", "custo": 10, "mult": 1.2, "tipo": "arcano", "base": "foco",
                "escala": {"intelecto": 1.0}, "desc": "Dano arcano barato."},
    "curar": {"nome": "Curar", "alvo": "aliado", "custo": 20, "cura": 16,
              "desc": "Cura 16 + 2 × nível + o símbolo sagrado (sem atributo nesta versão)."},
    "escudo_luz": {"nome": "Escudo de Luz", "alvo": "aliado", "custo": 15, "escudo": 18,
                   "desc": "Absorve 18 de dano até o fim da próxima rodada."},
    "reerguer": {"nome": "Reerguer", "alvo": "aliado_caido", "custo": 50, "uma_vez": True, "volta": 0.3,
                 "desc": "Ressurreição de alto custo: o aliado volta com 30% da vida. Uma vez por luta."},
    "luz_restauradora": {"nome": "Luz Restauradora", "alvo": "grupo", "custo": 30, "ultimate": True, "cura": 22,
                         "desc": "Ultimate: cura 22 + o símbolo sagrado em todo o grupo de pé e tira Queimadura e "
                                 "Sangramento."},
    # Morel (kit fixo)
    "joelho": {"nome": "Golpe no Joelho", "alvo": "inimigo", "custo": 30, "mult": 0.6, "tipo": "fisico", "base": "arma",
               "escala": {"forca": 1.0}, "interrompe": True, "controle": "atordoado", "aplicacao": 0.10,
               "desc": "Desfaz a preparação do alvo (se ela não for ininterruptível) e tenta atordoá-lo."},
    "oportuno": {"nome": "Golpe Oportuno", "alvo": "inimigo", "custo": 15, "mult": 1.2, "tipo": "fisico", "base": "arma",
                 "escala": {"forca": 1.0}, "contra_vulneravel": 0.6,
                 "desc": "Golpe que aproveita a brecha: +60% em quem está atordoado ou preparando um golpe."},
}
for _h in HABILIDADES.values():  # as ultimates do kit do protagonista também são ultimates
    if _h.get("tier") == "ultimate":
        _h["ultimate"] = True

CONSUMIVEIS = {
    "pocao": {"nome": "Poção de Vida", "alvo": "aliado", "cura": 30, "desc": "Cura 30 de vida.", "icone": "pocao_vida"},
    "pena": {"nome": "Pena de Fênix", "alvo": "aliado_caido", "volta": 0.4, "icone": "pena_fenix",
             "desc": "Item escasso: o aliado caído volta com 40% da vida."},
}

# ---------------------------------------------------------------- as construções do protagonista
BUILDS = {
    "forca": {"nome": "Força", "frase": "Bate forte com a arma e aguenta; age tarde.",
              "ganha": "o maior dano físico e boa vida", "abre_mao": "da iniciativa, do crítico e do dano arcano",
              "atributos": dict(forca=9, agilidade=3, constituicao=7, intelecto=1, percepcao=4, vontade=6),
              "kit": ["golpe_pesado", "proteger", "comando", "escudo_golpe", "furia"]},
    "precisao": {"nome": "Precisão", "frase": "Age primeiro e acerta pontos fracos e críticos.",
                 "ganha": "iniciativa, crítico e ponto fraco", "abre_mao": "de vida, de recurso e de Tenacidade",
                 "atributos": dict(forca=6, agilidade=8, constituicao=4, intelecto=1, percepcao=9, vontade=2),
                 "kit": ["corte", "golpe_pesado", "comando", "proteger", "escudo_golpe", "desafio"]},
    "runa": {"nome": "Runa", "frase": "O guerreiro arcano: a Lâmina Rúnica pelo Intelecto.",
             "ganha": "dano arcano que passa pela Guarda", "abre_mao": "do golpe físico e de vida",
             "atributos": dict(forca=2, agilidade=5, constituicao=5, intelecto=9, percepcao=4, vontade=5),
             "kit": ["lamina", "corte", "proteger", "escudo_golpe", "tempestade"]},
    "chama": {"nome": "Chama", "frase": "Prepara a Queimadura (num alvo ou no grupo) e a consome: combinação em dois tempos.",
              "ganha": "dano de fogo acumulado e a Conflagração", "abre_mao": "do golpe físico e de dano imediato",
              "atributos": dict(forca=2, agilidade=6, constituicao=5, intelecto=9, percepcao=3, vontade=5),
              "kit": ["brasa", "chuva", "combustao", "proteger", "conflagracao"]},
    "baluarte": {"nome": "Baluarte", "frase": "Segura as ameaças e bate com o próprio corpo: vida, Tenacidade e o Avanço.",
                 "ganha": "vida, Tenacidade, recurso e o Avanço do Baluarte", "abre_mao": "de dano de arma e de iniciativa",
                 "atributos": dict(forca=5, agilidade=2, constituicao=9, intelecto=1, percepcao=3, vontade=10),
                 "kit": ["avanco", "desafio", "proteger", "juramento"]},
}

# ---------------------------------------------------------------- o grupo
GRUPO = {
    "heroi": {"nome": "Jean", "retrato": "guerreiro", "papel": "protagonista", "nivel": 3, "vida_base": 40,
              "recurso": "Vigor", "protecao": 3},
    "odete": {"nome": "Odette", "retrato": "odete", "papel": "companheira", "feminino": True, "nivel": 3,
              "vida_base": 32, "recurso": "Fé", "protecao": 1, "arma": 3, "foco": 4, "simbolo": 4,
              "atributos": dict(forca=2, agilidade=4, constituicao=3, intelecto=6, percepcao=3, vontade=5),
              "kit": ["lampejo", "curar", "escudo_luz", "reerguer", "luz_restauradora"]},
    "morel": {"nome": "Morel", "retrato": "morel", "papel": "companheiro", "nivel": 3, "vida_base": 38,
              "recurso": "Vigor", "protecao": 2, "arma": 6, "foco": 0,
              "atributos": dict(forca=6, agilidade=5, constituicao=5, intelecto=1, percepcao=4, vontade=3),
              "kit": ["joelho", "oportuno"]},
}

# ---------------------------------------------------------------- os inimigos
# preparo: "primeiro" = em qual turno agido o inimigo prepara a primeira vez; "cada" = de quantos em quantos turnos
# agidos depois. Turno perdido (atordoado, aterrorizado) não conta: o controle adia, não apaga a preparação.
# res: resistências por tipo (%). tipo: o tipo do golpe comum (físico se faltar).
INIMIGOS = {
    "lobo": {"nome": "Lobo", "retrato": "lobo", "vida": 56, "protecao": 0, "agi": 5, "per": 3, "dano": 9,
             "tenacidade": 0.0, "golpe": "Mordida"},
    "lobo_alfa": {"nome": "Lobo Alfa", "retrato": "lobo", "vida": 85, "protecao": 1, "agi": 6, "per": 4, "dano": 9,
                  "tenacidade": 0.10, "golpe": "Mordida",
                  "preparo": {"id": "bote", "nome": "Bote", "dano": 22, "sangra": 8, "primeiro": 2, "cada": 3,
                              "aviso": "abaixa e mira"}},
    "bruto": {"nome": "Bandido Bruto", "retrato": "bandido", "vida": 250, "protecao": 2, "agi": 2, "per": 2,
              "dano": 15, "tenacidade": 0.30, "golpe": "Porretada", "ponto_fraco": "o joelho enfaixado",
              "preparo": {"id": "esmagador", "nome": "Golpe Esmagador", "dano": 36, "controle": "atordoado",
                          "aplicacao": 0.10, "primeiro": 2, "cada": 3, "aviso": "ergue o porrete com as duas mãos",
                          "furioso": 0.5}},
    "besteiro": {"nome": "Besteiro", "retrato": "mercenario", "vida": 64, "protecao": 1, "agi": 5, "per": 5,
                 "dano": 13, "tenacidade": 0.05, "golpe": "Virote"},
    "xama": {"nome": "Xamã Caído", "retrato": "xama_caido", "vida": 140, "protecao": 1, "agi": 4, "per": 4, "dano": 12,
             "tipo": "arcano", "tenacidade": 0.20, "golpe": "Garra sombria", "res": {"arcano": 0.30},
             "preparo": {"id": "terror", "nome": "Grito de Terror", "area": True, "controle": "aterrorizado",
                         "aplicacao": 0.0, "primeiro": 2, "cada": 3, "aviso": "puxa o ar, o rosto se contorce"},
             "invoca": {"primeiro": 1, "cada": 3, "quem": "afogado", "max": 2}},
    "esqueleto": {"nome": "Soldado Morto", "retrato": "esqueleto", "vida": 110, "protecao": 2, "agi": 3, "per": 2,
                  "dano": 18, "tenacidade": 0.35, "golpe": "Espadada", "guarda": 6,
                  "ponto_fraco": "as juntas expostas"},
    "afogado": {"nome": "Afogado", "retrato": "afogado", "vida": 36, "protecao": 0, "agi": 1, "per": 1, "dano": 10,
                "tenacidade": 0.0, "golpe": "Agarrão", "invocado": True},
    "cao": {"nome": "Cão de Brasa", "retrato": "cao_infernal", "vida": 140, "protecao": 1, "agi": 6, "per": 4, "dano": 11,
            "tipo": "fogo", "tenacidade": 0.15, "golpe": "Mordida em brasa", "res": {"fogo": 0.60, "arcano": 0.0},
            "preparo": {"id": "sopro", "nome": "Sopro de Brasa", "area": True, "dano": 16, "tipo": "fogo",
                        "queima": 4, "primeiro": 2, "cada": 3, "aviso": "abre a boca e a garganta acende"}},
}

# ---------------------------------------------------------------- os encontros e os casos de teste
ENCONTROS = {
    "e1": {"nome": "1 · Os lobos da estrada", "tipo": "encontro", "semente": 11,
           "objetivo": "O tutorial: a reserva cheia, a recuperação (todo turno +6; o ataque, +6 a mais), o kit, a "
                       "defesa e o Lobo Alfa anunciando o Bote antes de dar.",
           "inimigos": ["lobo_alfa", "lobo"], "consumiveis": {"pocao": 1}},
    "e2": {"nome": "2 · O bruto anunciado", "tipo": "encontro", "semente": 23,
           "objetivo": "O Bruto prepara o Golpe Esmagador a cada três turnos dele; atordoá-lo adia, não apaga. Abaixo "
                       "da metade da vida, o golpe vem furioso e não pode ser interrompido. Os besteiros não param.",
           "inimigos": ["bruto", "besteiro", "besteiro"], "consumiveis": {"pocao": 1}},
    "e3": {"nome": "3 · O xamã e o soldado", "tipo": "encontro", "semente": 37,
           "objetivo": "O xamã (resiste 30% ao arcano e ataca com arcano) chama afogados e prepara o Grito de Terror; o Soldado Morto "
                       "bate forte atrás da guarda.",
           "inimigos": ["xama", "esqueleto"], "consumiveis": {"pocao": 1}},
    "e4": {"nome": "4 · Os cães de brasa", "tipo": "encontro", "semente": 41,
           "objetivo": "Cães de fogo: resistem 60% ao fogo e mordem com fogo; o Sopro de Brasa queima o grupo todo. "
                       "Compare com o Manto de salamandra (35% de fogo) e o de viagem, e a Chama contra a Runa.",
           "inimigos": ["cao", "cao"], "consumiveis": {"pocao": 1}},
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
           "teste": "Condição de teste: Morel começa caído.", "inimigos": ["lobo"], "consumiveis": {},
           "inicio": {"morel": {"caido": True}}},
    "t4": {"nome": "Teste · inimigo derrotado antes da preparação", "tipo": "teste", "semente": 13,
           "objetivo": "O Lobo Alfa começa ferido e já preparando o Bote: derrubado antes da vez dele, o Bote não sai.",
           "teste": "Condições de teste: o Lobo Alfa começa com 8 de vida, Agilidade 1 (age por último) e o Bote já "
                    "preparado.",
           "inimigos": ["lobo_alfa"], "consumiveis": {},
           "inicio": {"lobo_alfa#1": {"vida": 8, "agilidade": 1, "preparando": True}}},
    "t5": {"nome": "Teste · ultimate, queda e retorno", "tipo": "teste", "semente": 17,
           "objetivo": "Odette usa a Luz Restauradora, cai e volta com a Pena: a ultimate continua gasta nesta luta.",
           "teste": "Condições de teste: Odette começa com 12 de vida e o grupo tem uma Pena de Fênix.",
           "inimigos": ["lobo_alfa", "lobo"], "consumiveis": {"pena": 1},
           "inicio": {"odete": {"vida": 12}}},
    "t7": {"nome": "Teste · Queimadura no grupo", "tipo": "teste", "semente": 29,
           "objetivo": "Três lobos parados para comparar a Chuva de Brasas, a Brasa e a Conflagração no grupo.",
           "teste": "Condições de teste: três lobos que não atacam, com 300 de vida cada.",
           "inimigos": ["lobo", "lobo", "lobo"], "consumiveis": {},
           "inicio": {f"lobo#{i}": {"vida": 300, "vida_max": 300, "parado": True} for i in (1, 2, 3)}},
    "t8": {"nome": "Teste · Queimadura contra resistência", "tipo": "teste", "semente": 31,
           "objetivo": "Dois Cães de Brasa parados (60% de fogo): a Queimadura pega, o dano cai.",
           "teste": "Condições de teste: dois Cães de Brasa que não atacam, com 300 de vida cada.",
           "inimigos": ["cao", "cao"], "consumiveis": {},
           "inicio": {f"cao#{i}": {"vida": 300, "vida_max": 300, "parado": True} for i in (1, 2)}},
    "t6": {"nome": "Teste · Queimadura e Combustão", "tipo": "teste", "semente": 19,
           "objetivo": "Um alvo parado para comparar a Brasa sozinha, a Combustão sozinha e as duas em sequência.",
           "teste": "Condições de teste: um Soldado Morto sem golpes (não ataca) e sem Guarda, com muita vida.",
           "inimigos": ["esqueleto"], "consumiveis": {},
           "inicio": {"esqueleto#1": {"vida": 400, "vida_max": 400, "guarda": 0, "parado": True}}},
}

# ---------------------------------------------------------------- uma situação de aventura (fora da luta)
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
