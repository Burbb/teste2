"""O conteúdo provisório do protótipo X1 da etapa 8 (nada no jogo): montagem de builds e a estrutura dos talentos, pelas
seções 15 e 16 do roadmapIDEIAS/28-ETAPA8-HABILIDADES-TALENTOS-E-BUILDS.md.

Rodada 2 do X1 (31/10/2026): o repertório cresceu para 16 habilidades por personagem (14 e duas ultimates à escolha),
sobre um vocabulário compartilhado pequeno:
- fichas (Guarda, Força, Exposto), em qualquer combatente;
- três estados de camadas nos inimigos: Queimadura (fogo), Sangramento (corte) e Frio (com 3, congela). Queimadura e
  Frio se anulam;
- invocações: aliados sem vez própria, que agem no fim da vez de quem as chamou e têm um efeito ao cair;
- a Fúria do Berserker e as preparações que o jogo já tem (Golpe Esmagador).

O kit continua com 5 habilidades e a ultimate. As duas estruturas de talentos usam o mesmo orçamento (9 pontos), os
mesmos números e os mesmos efeitos: na híbrida, uma regra vale para todas as habilidades com a propriedade; na de
versões, o mesmo efeito vem preso a uma habilidade ou junto de outro num princípio.

Valores de teste, não catálogo: servem para observar decisões, não para balancear a campanha."""

VERSAO = "X1 rodada 2 · 31/10/2026"
PONTOS = 9          # o orçamento de talentos
ESPACOS = 5         # habilidades no kit, além da ultimate
FICHA_TETO = 2      # Guarda, Força e Exposto
CAMADAS_TETO = 3    # Queimadura, Sangramento e Frio
PINGOS = 3          # duração da Queimadura e do Sangramento, em turnos do alvo
PINGO_CAMADA = 3    # dano por camada no começo de cada turno do alvo
DETONA_CAMADA = 9   # dano de fogo por camada detonada
FERIDA_CAMADA = 10  # dano por camada de Sangramento aberta
REGEN = 6           # recurso no começo de cada turno de quem age
BASICO_GANHA = 6    # Atacar, Bastão e Defender devolvem mais 6
LIMITE_RODADAS = 30

CUSTO_TIPO = {"N": 1, "R": 2, "V": 1, "P": 3}
NOME_TIPO = {"N": "Número", "R": "Regra", "V": "Versão", "P": "Princípio"}
ESTRUTURAS = {
    "t4": {"nome": "Híbrida", "frase": "Regras que valem para todas as habilidades com uma propriedade (2 pontos), versões "
                                       "que mudam o papel de uma habilidade (1 ponto) e números (1 ponto por nível), "
                                       "nos mesmos 9 pontos. Sem ordem de compra."},
    "t1": {"nome": "Versões e princípios", "frase": "Os mesmos efeitos, mas presos a uma habilidade (versão, 1 ponto) ou "
                                                    "juntos em princípios (3 pontos); os mesmos números. Os mesmos 9 "
                                                    "pontos, sem ordem de compra."},
}

TIPOS = {"fisico": "físico", "fogo": "fogo", "gelo": "gelo", "sagrado": "sagrado", "sombra": "sombra"}
FUNCOES = ["Dano", "Controle", "Defesa", "Apoio", "Recurso", "Invocação"]
PROPRIEDADES = ["Queimadura", "Frio", "Sangramento", "Guarda", "Força", "Exposto", "Fúria", "Área", "Preparações",
                "Mira", "Cura", "Invocação", "Recurso"]

# ---------------------------------------------------------------- o grupo
HEROI = {
    "berserker": {"nome": "Jean", "classe": "Guerreiro", "spec": "Berserker", "retrato": "guerreiro", "vida": 64,
                  "recurso": "Vigor", "recurso_max": 60, "poder": 14, "agi": 5,
                  "ultimates": ["furia_cega", "muralha_viva"]},
    "piromante": {"nome": "Jean", "classe": "Mago", "spec": "Piromante", "retrato": "mago", "vida": 52,
                  "recurso": "Mana", "recurso_max": 60, "poder": 14, "agi": 6,
                  "ultimates": ["conflagracao", "inverno"]},
}
COMPANHEIROS = {
    "morel": {"nome": "Morel", "retrato": "morel", "vida": 52, "recurso": "Vigor", "recurso_max": 50, "poder": 11,
              "agi": 7, "kit": ["atacar", "oportuno", "proteger", "defender"]},
    "odete": {"nome": "Odette", "retrato": "odete", "vida": 44, "recurso": "Fé", "recurso_max": 50, "poder": 9,
              "agi": 4, "kit": ["bastao", "prece", "bencao", "defender"]},
}
INVOCACOES = {
    "estandarte": {"nome": "Estandarte de Guerra", "vida": 30, "poder": 0, "agi": 0},
    "fogo_fatuo": {"nome": "Fogo-fátuo", "vida": 18, "poder": 0, "agi": 0},
    "sentinela": {"nome": "Sentinela de Gelo", "vida": 34, "poder": 0, "agi": 0},
}


def _h(nome, alvo, custo, desc, etiquetas, funcao, props, origem=None, **extra):
    return dict(nome=nome, alvo=alvo, custo=custo, desc=desc, etiquetas=etiquetas, funcao=funcao, props=props,
                origem=origem, **extra)


# ---------------------------------------------------------------- as habilidades
# alvo: inimigo | inimigos | aliado (inclui invocações) | aliado_outro (outro do grupo) | proprio.
# etiquetas: o que as regras de talento perguntam. funcao e props: os filtros da montagem.
# origem: "classe" (Guerreiro, Mago) ou "spec" (Berserker, Piromante).
HABILIDADES = {
    # comuns (fora do kit)
    "atacar": _h("Atacar", "inimigo", 0, f"Causa 100% do Poder em dano físico. Recupera {BASICO_GANHA} a mais.",
                 ["golpe"], [], [], mult=1.0, tipo="fisico"),
    "defender": _h("Defender", "proprio", 0, f"Ganha 1 Guarda. Recupera {BASICO_GANHA} a mais.", ["guarda"], [], []),

    # ---------------- Berserker: do Guerreiro
    "golpe_pesado": _h("Golpe Pesado", "inimigo", 14, "Causa 140% do Poder em dano físico.", ["golpe"],
                       ["Dano"], [], "classe", mult=1.4, tipo="fisico"),
    "joelho": _h("Golpe no Joelho", "inimigo", 14,
                 "Causa 70% do Poder em dano físico e tenta atordoar: certo em quem prepara um golpe (interrompe), 40% "
                 "nos outros. Gigantes resistem metade das vezes; quem está Firme não é atordoado.",
                 ["golpe", "interrompe"], ["Controle"], ["Preparações"], "classe", mult=0.7, tipo="fisico"),
    "quebra_guarda": _h("Quebra-Guarda", "inimigo", 12, "Causa 90% do Poder em dano físico e deixa o alvo Exposto (1).",
                        ["golpe", "expoe"], ["Dano", "Apoio"], ["Exposto"], "classe", mult=0.9, tipo="fisico"),
    "erguer_escudo": _h("Erguer Escudo", "aliado", 8, "Você, um aliado ou uma invocação ganha 1 Guarda.", ["guarda"],
                        ["Defesa"], ["Guarda"], "classe"),
    "provocar": _h("Provocar", "proprio", 12, "Todos os inimigos miram você na próxima vez deles. Você ganha 1 Guarda.",
                   ["guarda", "provoca"], ["Defesa"], ["Mira", "Guarda"], "classe"),
    "grito_guerra": _h("Grito de Guerra", "proprio", 16, "Cada aliado (não você nem as invocações) ganha 1 Força.",
                       ["forca"], ["Apoio"], ["Força"], "classe"),
    "escudo_alto": _h("Escudo Alto", "inimigo", 10,
                      "Consome todas as suas Guardas: causa 30% do Poder + 12 por Guarda em dano físico.",
                      ["golpe", "guarda"], ["Dano"], ["Guarda"], "classe", mult=0.3, tipo="fisico"),
    # ---------------- Berserker: da especialização
    "rugido": _h("Rugido", "inimigo", 10,
                 "Causa 80% do Poder em dano físico e você entra em Fúria: seus golpes +40% e os golpes que você recebe "
                 "+40%. Na sua vez, sair da Fúria não gasta a ação e dá 12 de Vigor e 1 Guarda.",
                 ["golpe", "furia"], ["Dano"], ["Fúria"], "spec", mult=0.8, tipo="fisico"),
    "sede": _h("Sede de Sangue", "inimigo", 16, "Causa 100% do Poder em dano físico e cura você em 40% do dano causado.",
               ["golpe", "cura"], ["Dano", "Recurso"], ["Cura"], "spec", mult=1.0, tipo="fisico"),
    "redemoinho": _h("Redemoinho", "inimigos", 20, "Causa 55% do Poder em dano físico a cada inimigo.",
                     ["golpe", "area"], ["Dano"], ["Área"], "spec", mult=0.55, tipo="fisico"),
    "talho": _h("Talho", "inimigo", 9,
                "Causa 60% do Poder em dano físico e abre 1 camada de Sangramento (até 3; 3 por camada no começo da "
                "vez do alvo, por 3 vezes). Mortos-vivos não sangram.",
                ["golpe", "sangra"], ["Dano"], ["Sangramento"], "spec", mult=0.6, tipo="fisico"),
    "abrir_feridas": _h("Abrir Feridas", "inimigo", 14,
                        f"Consome o Sangramento do alvo: causa 40% do Poder + {FERIDA_CAMADA} por camada em dano "
                        "físico.", ["golpe", "consome_sangue"], ["Dano"], ["Sangramento"], "spec", mult=0.4,
                        tipo="fisico"),
    "cerrar_dentes": _h("Cerrar os Dentes", "proprio", 8,
                        "Até a sua próxima vez, os golpes que você recebe −30%, e cada um deles dá 5 de Vigor.",
                        ["recebe"], ["Defesa", "Recurso"], ["Recurso"], "spec"),
    "estandarte": _h("Estandarte de Guerra", "proprio", 16,
                     "Invoca o Estandarte (30 de vida; os inimigos podem golpeá-lo). No fim de cada vez sua, ele dá 1 "
                     "Força ao aliado com menos Força. Chamar de novo troca o anterior.",
                     ["invocacao", "forca"], ["Invocação", "Apoio"], ["Invocação", "Força"], "spec"),
    "furia_cega": _h("Fúria Cega", "inimigo", 20,
                     "Causa 220% do Poder em dano físico. Se o alvo morrer, causa 120% ao inimigo com menos vida (uma "
                     "vez).", ["golpe"], ["Dano"], [], "spec", mult=2.2, tipo="fisico", ultimate=True),
    "muralha_viva": _h("Muralha Viva", "proprio", 20,
                       "Até a sua próxima vez, todos os golpes contra o grupo e as invocações vêm para você. Você ganha "
                       "2 Guarda.", ["guarda", "provoca"], ["Defesa"], ["Mira", "Guarda"], "spec", ultimate=True),

    # ---------------- Piromante: do Mago
    "bola_fogo": _h("Bola de Fogo", "inimigo", 12, "Causa 100% do Poder em dano de fogo e acende 1 camada de Queimadura.",
                    ["golpe", "fogo", "acende"], ["Dano"], ["Queimadura"], "classe", mult=1.0, tipo="fogo"),
    "lanca": _h("Lança de Gelo", "inimigo", 12,
                "Causa 90% do Poder em dano de gelo e dá 1 Frio ao alvo (2 se ele prepara um golpe). Com 3 Frio, o alvo "
                "congela: perde a próxima vez e o golpe que preparava.",
                ["golpe", "gelo", "frio"], ["Dano", "Controle"], ["Frio", "Preparações"], "classe", mult=0.9,
                tipo="gelo"),
    "nevasca": _h("Nevasca", "inimigos", 18, "Causa 30% do Poder em dano de gelo a cada inimigo e dá 1 Frio a cada um.",
                  ["golpe", "gelo", "frio", "area"], ["Controle"], ["Frio", "Área"], "classe", mult=0.3, tipo="gelo"),
    "barreira": _h("Barreira", "aliado", 8, "Você, um aliado ou uma invocação ganha 1 Guarda.", ["guarda"], ["Defesa"],
                   ["Guarda"], "classe"),
    "meditar": _h("Meditar", "proprio", 0, "Recupera 24 de Mana.", ["recurso"], ["Recurso"], ["Recurso"], "classe"),
    # ---------------- Piromante: da especialização
    "brasa": _h("Brasa", "inimigo", 7, "Causa 50% do Poder em dano de fogo e acende 1 camada de Queimadura.",
                ["golpe", "fogo", "acende"], ["Dano"], ["Queimadura"], "spec", mult=0.5, tipo="fogo"),
    "chuva": _h("Chuva de Brasas", "inimigos", 18,
                "Causa 30% do Poder em dano de fogo a cada inimigo e acende 1 camada em cada um.",
                ["golpe", "fogo", "acende", "area"], ["Dano"], ["Queimadura", "Área"], "spec", mult=0.3, tipo="fogo"),
    "combustao": _h("Combustão", "inimigo", 14,
                    f"Detona a Queimadura do alvo: causa 40% do Poder + {DETONA_CAMADA} por camada em dano de fogo. A "
                    "Queimadura apaga.", ["fogo", "detona"], ["Dano"], ["Queimadura"], "spec", mult=0.4, tipo="fogo"),
    "alastrar": _h("Alastrar", "inimigo", 12,
                   "As camadas de Queimadura do alvo passam a cada outro inimigo (cada um fica com as suas ou com as "
                   "dele, o que for maior). O alvo apaga. Não causa dano.",
                   ["fogo", "transfere"], ["Controle"], ["Queimadura", "Área"], "spec"),
    "escudo_chamas": _h("Escudo de Chamas", "aliado", 12,
                        "Você, um aliado ou uma invocação ganha 1 Guarda. Até o fim da próxima rodada, cada inimigo que "
                        "golpear quem tem o escudo ganha 1 camada de Queimadura.",
                        ["guarda", "fogo", "acende"], ["Defesa"], ["Guarda", "Queimadura"], "spec"),
    "arma_flamejante": _h("Arma Flamejante", "aliado_outro", 10,
                          "Até o fim da próxima vez do aliado, os golpes dele são de fogo e acendem 1 camada.",
                          ["aliados", "fogo", "acende"], ["Apoio"], ["Queimadura"], "spec"),
    "fogo_fatuo": _h("Fogo-fátuo", "proprio", 16,
                     "Invoca o Fogo-fátuo (18 de vida; os inimigos podem golpeá-lo). No fim de cada vez sua, ele acende "
                     "1 camada no inimigo com menos camadas. Quando cai, explode: 8 de fogo em cada inimigo. Chamar "
                     "de novo troca o anterior, sem explodir.",
                     ["invocacao", "fogo", "acende"], ["Invocação", "Dano"], ["Invocação", "Queimadura"], "spec"),
    "sentinela": _h("Sentinela de Gelo", "proprio", 16,
                    "Invoca a Sentinela (34 de vida). Os inimigos miram nela na próxima vez deles; quem a golpeia "
                    "ganha 1 Frio. Quando cai, cada inimigo ganha 1 Frio. Chamar de novo troca a anterior, sem efeito.",
                    ["invocacao", "gelo", "frio"], ["Invocação", "Defesa"], ["Invocação", "Frio", "Mira"], "spec"),
    "sobrecarga": _h("Sobrecarga", "proprio", 6, "Você ganha 2 Força e fica Exposto (2).", ["forca"], ["Apoio"],
                     ["Força", "Exposto"], "spec"),
    "conflagracao": _h("Conflagração", "inimigos", 20,
                       f"Detona a Queimadura de cada inimigo: 40% do Poder + {DETONA_CAMADA} por camada em dano de fogo "
                       "em cada um. As Queimaduras apagam.", ["fogo", "detona", "area"], ["Dano"],
                       ["Queimadura", "Área"], "spec", mult=0.4, tipo="fogo", ultimate=True),
    "inverno": _h("Inverno", "proprio", 20, "Cada inimigo ganha 2 Frio e cada aliado (e invocação) ganha 1 Guarda.",
                  ["gelo", "frio", "guarda"], ["Controle", "Defesa"], ["Frio", "Guarda", "Área"], "spec",
                  ultimate=True),

    # Morel (kit fixo)
    "oportuno": _h("Golpe Oportuno", "inimigo", 14,
                   "Causa 120% do Poder em dano físico; +60% em quem está atordoado, congelado, preso ou preparando um "
                   "golpe.", ["golpe"], [], [], mult=1.2, tipo="fisico"),
    "proteger": _h("Proteger", "aliado_outro", 12, "Os golpes contra o aliado vêm para Morel até a próxima vez dele.",
                   ["protecao"], [], []),
    # Odette (kit fixo)
    "bastao": _h("Bastão", "inimigo", 0, f"Causa 100% do Poder em dano sagrado. Recupera {BASICO_GANHA} a mais.",
                 ["golpe"], [], [], mult=1.0, tipo="sagrado"),
    "prece": _h("Prece", "aliado", 14, "Cura 18 de vida de um aliado ou invocação.", ["cura"], [], [], cura=18),
    "bencao": _h("Bênção", "aliado", 10, "Um aliado ganha 1 Força.", ["forca"], [], []),
}
POOL = {
    "berserker": ["golpe_pesado", "joelho", "quebra_guarda", "erguer_escudo", "provocar", "grito_guerra", "escudo_alto",
                  "rugido", "sede", "redemoinho", "talho", "abrir_feridas", "cerrar_dentes", "estandarte"],
    "piromante": ["bola_fogo", "lanca", "nevasca", "barreira", "meditar", "brasa", "chuva", "combustao", "alastrar",
                  "escudo_chamas", "arma_flamejante", "fogo_fatuo", "sentinela", "sobrecarga"],
}

FICHAS = {
    "guarda": {"nome": "Guarda", "desc": "O próximo golpe recebido −50%. Anula 1 Exposto ao chegar."},
    "forca": {"nome": "Força", "desc": "A próxima ação que golpeia +50% (em área, vale para todos os alvos)."},
    "exposto": {"nome": "Exposto", "desc": "O próximo golpe recebido +50%. Anula 1 Guarda ao chegar."},
}

REGRAS_LUTA = [
    "Ordem fixa pela Agilidade; cada combatente age uma vez por rodada. Você escolhe as ações de Jean, Morel e Odette.",
    "Fichas (até 2 de cada): Guarda, o próximo golpe recebido −50%; Força, a próxima ação que golpeia +50%; Exposto, o "
    "próximo golpe recebido +50%. Guarda e Exposto se anulam.",
    "Camadas (até 3) nos inimigos: Queimadura e Sangramento pingam 3 por camada no começo da vez do alvo, por 3 vezes "
    "(acender ou abrir de novo renova). Frio não pinga: com 3, o alvo congela.",
    "Queimadura e Frio se anulam: fogo num alvo com Frio tira 1 Frio por camada que acenderia, e gelo num alvo em "
    "chamas apaga 1 camada por Frio que daria.",
    "Invocações não têm vez: agem no fim da vez de Jean. Os inimigos podem golpeá-las. Quando caem, fazem o efeito delas.",
    "Cadeia é tudo o que uma ação provoca. Cada efeito acontece uma vez por motivo em cada cadeia: cada morto explode "
    "uma vez, cada inimigo dá 1 Calor, cada invocação cai uma vez.",
    "Revide, espinhos e escudos respondem a golpes de ação. O dano deles, das camadas e das explosões não provoca outra "
    "resposta.",
    "Atordoado, congelado ou preso: perde a próxima vez e o golpe que preparava; depois fica Firme por 2 vezes dele.",
    f"Recurso: +{REGEN} no começo de cada vez; Atacar, Bastão e Defender devolvem mais {BASICO_GANHA}. A ultimate, uma "
    "vez por luta.",
]


# ---------------------------------------------------------------- os talentos
# Cada nó: tipo (N, R, V, P; o custo vem do tipo), ranks, efeitos (as bandeiras do motor; nos números, o valor cresce
# com o rank), afeta (as etiquetas das habilidades que ele muda; "aliados", "recebe" e "sempre" para o que não depende
# do kit), versao (a habilidade que a versão troca), exclui (o grupo de exclusão), props (os filtros), texto (a regra),
# nota (a linha que aparece em cada habilidade afetada; na versão, a descrição nova da habilidade) e equivale (na de
# versões, de que efeito da híbrida ele veio).
def _n(id, nome, tipo, efeitos, texto, nota=None, afeta=(), props=(), ranks=1, versao=None, exclui=None,
       requer_etiqueta=None, equivale=None):
    return dict(id=id, nome=nome, tipo=tipo, efeitos=efeitos, texto=texto, nota=nota or texto, afeta=list(afeta),
                props=list(props), ranks=ranks, versao=versao, exclui=exclui or versao, requer_etiqueta=requer_etiqueta,
                equivale=equivale)


# números iguais nas duas estruturas
_NUM_B = [
    _n("couro", "Couro Grosso", "N", {"couro": 1}, "+12 de vida máxima por ponto.", afeta=["sempre"], ranks=2),
    _n("braco", "Braço Pesado", "N", {"braco": 1}, "Seus golpes +8% por ponto.", afeta=["golpe"], ranks=2),
    _n("folego_largo", "Fôlego Largo", "N", {"recurso_extra": 1}, "+12 de Vigor máximo por ponto.",
       afeta=["sempre"], props=["Recurso"], ranks=2),
]
_NUM_P = [
    _n("chama_viva", "Chama Viva", "N", {"chama_viva": 1}, "Queimadura (pingos e detonações) +15% por ponto.",
       afeta=["acende", "detona"], props=["Queimadura"], ranks=2),
    _n("reserva", "Reserva Ardente", "N", {"recurso_extra": 1}, "+12 de Mana máxima por ponto.", afeta=["sempre"],
       props=["Recurso"], ranks=2),
    _n("foco", "Foco Afiado", "N", {"braco": 1}, "Seus golpes +8% por ponto.", afeta=["golpe"], ranks=2),
]

_B4 = _NUM_B + [
    _n("sangue_quente", "Sangue Quente", "R", {"sangue_quente": 1},
       "Na Fúria, cada golpe seu cura você em 15% do dano que causou.", "Sangue Quente: na Fúria, cura 15% do dano",
       afeta=["golpe"], props=["Fúria", "Cura"], requer_etiqueta="furia"),
    _n("sangue_frio", "Sangue Frio", "R", {"sangue_frio": 1}, "Sair da Fúria dá 1 Guarda também a cada aliado.",
       "Sangue Frio: sair da Fúria dá 1 Guarda a cada aliado", afeta=["furia"], props=["Fúria", "Guarda"]),
    _n("grito_contagiante", "Grito Contagiante", "R", {"grito_contagiante": 1},
       "Quando você entra em Fúria, cada aliado ganha 1 Força.",
       "Grito Contagiante: entrar em Fúria dá 1 Força a cada aliado", afeta=["furia"], props=["Fúria", "Força"]),
    _n("furia_contida", "Fúria Contida", "R", {"furia_contida": 1},
       "Na Fúria, os golpes que você recebe +20% (em vez de +40%).", "Fúria Contida: recebe +20%", afeta=["furia"],
       props=["Fúria"], exclui="modo_furia"),
    _n("furia_sem_freio", "Fúria Sem Freio", "R", {"furia_sem_freio": 1},
       "Na Fúria, seus golpes +60% (em vez de +40%), mas você só pode sair depois de 2 vezes suas nela.",
       "Fúria Sem Freio: causa +60%; sai só depois de 2 vezes", afeta=["furia"], props=["Fúria"], exclui="modo_furia"),
    _n("peso_golpe", "Peso do Golpe", "R", {"peso_golpe": 1},
       "Quando você interrompe um golpe preparado ou deixa um inimigo Exposto, o próximo aliado na ordem ganha 1 Força.",
       "Peso do Golpe: interromper ou expor dá 1 Força ao próximo aliado", afeta=["interrompe", "expoe"],
       props=["Força", "Exposto", "Preparações"]),
    _n("escudeiro", "Escudeiro", "R", {"escudeiro": 1},
       "Quando você dá Guarda a um aliado ou invocação, você também ganha 1 Guarda.",
       "Escudeiro: dar Guarda a outro dá 1 a você", afeta=["guarda"], props=["Guarda"]),
    _n("revide", "Revide", "R", {"revide": 1},
       "Quando um inimigo golpeia você, você revida com 60% do Poder. Uma vez por rodada. Revide não responde a outro "
       "revide nem a espinhos.", "Revide", afeta=["recebe"], props=["Mira"]),
    _n("folego", "Fôlego Rubro", "R", {"folego": 1},
       "Quando você é curado (por você ou por um aliado), ganha 6 de Vigor. Uma vez por rodada.",
       "Fôlego Rubro: ser curado dá 6 de Vigor (1 vez por rodada)", afeta=["cura", "sempre"], props=["Cura", "Recurso"]),
    _n("ate_o_fim", "Até o Fim", "R", {"ate_o_fim": 1}, "Com menos da metade da vida, seus golpes +30%.",
       "Até o Fim: abaixo da metade da vida, +30%", afeta=["golpe"]),
    _n("fio_cortante", "Fio Cortante", "R", {"fio_cortante": 1},
       "Seus golpes num alvo só abrem 1 camada de Sangramento se o alvo já sangra.",
       "Fio Cortante: num alvo que sangra, abre mais 1 camada", afeta=["golpe"], props=["Sangramento"]),
    _n("banho_sangue", "Banho de Sangue", "R", {"banho_sangue": 1},
       "Quando um inimigo que sangra morre, cada outro inimigo ganha as camadas dele (até 3).",
       "Banho de Sangue: quem morre sangrando passa as camadas aos outros", afeta=["sangra", "consome_sangue"],
       props=["Sangramento"]),
    _n("desequilibra", "Golpe que Desequilibra", "V", {"desequilibra": 1},
       "Golpe Pesado: causa 110% do Poder e interrompe o golpe que o alvo prepara, sem atordoar (vale em gigantes e "
       "em quem está Firme).",
       "Causa 110% do Poder em dano físico e interrompe o golpe que o alvo prepara, sem atordoar. Vale em gigantes e "
       "em quem está Firme.", versao="golpe_pesado", props=["Preparações"]),
    _n("acumulado", "Golpe Acumulado", "V", {"acumulado": 1},
       "Golpe Pesado: consome as Forças do grupo inteiro (as suas e as dos aliados): +50% por Força.",
       "Causa 140% do Poder em dano físico e consome as Forças do grupo inteiro: +50% por Força.",
       versao="golpe_pesado", props=["Força"]),
    _n("desafiador", "Rugido Desafiador", "V", {"desafiador": 1},
       "Rugido: além de entrar em Fúria, todos os inimigos miram você na próxima vez deles.",
       "Causa 80% do Poder em dano físico, você entra em Fúria e todos os inimigos miram você na próxima vez deles.",
       versao="rugido", props=["Mira", "Fúria"]),
    _n("redemoinho_sangrento", "Redemoinho Sangrento", "V", {"redemoinho_sangrento": 1},
       "Redemoinho: causa 45% do Poder a cada inimigo e abre 1 camada de Sangramento em cada um.",
       "Causa 45% do Poder em dano físico a cada inimigo e abre 1 camada de Sangramento em cada um.",
       versao="redemoinho", props=["Sangramento", "Área"]),
    _n("hemorragia", "Hemorragia", "V", {"hemorragia": 1},
       "Abrir Feridas: também cura você em 5 por camada consumida.",
       f"Consome o Sangramento do alvo: causa 40% do Poder + {FERIDA_CAMADA} por camada em dano físico e cura você em "
       "5 por camada.", versao="abrir_feridas", props=["Sangramento", "Cura"]),
    _n("estandarte_sangrento", "Estandarte Sangrento", "V", {"estandarte_sangrento": 1},
       "Estandarte: no fim de cada vez sua, abre 1 camada de Sangramento no inimigo com menos camadas, em vez de dar "
       "Força.",
       "Invoca o Estandarte (30 de vida). No fim de cada vez sua, ele abre 1 camada de Sangramento no inimigo com menos "
       "camadas.", versao="estandarte", props=["Sangramento", "Invocação"]),
]
_P4 = _NUM_P + [
    _n("paciente", "Fogo Paciente", "R", {"paciente": 1},
       "Uma Queimadura com 3 camadas não expira: pinga até ser detonada ou o alvo morrer.",
       "Fogo Paciente: com 3 camadas, não expira", afeta=["acende", "transfere"], props=["Queimadura"],
       exclui="ritmo_fogo"),
    _n("fornalha", "Fornalha Interior", "R", {"fornalha": 1},
       "Cada inimigo que você detona ou que explode dá 1 Calor (até 3). Com 3, a próxima habilidade de fogo custa 0 e "
       "gasta o Calor. O mesmo inimigo dá 1 Calor por cadeia.",
       "Fornalha Interior: cada inimigo detonado dá 1 Calor", afeta=["detona"], props=["Queimadura", "Recurso"],
       exclui="ritmo_fogo"),
    _n("partilhado", "Calor Partilhado", "R", {"partilhado": 1},
       "Quando Morel ou Odette golpeia um inimigo em chamas, ele ganha 1 camada.", "Calor Partilhado",
       afeta=["aliados"], props=["Queimadura"]),
    _n("estouro", "Estouro", "R", {"estouro": 1},
       "Um inimigo que morre em chamas (ou detonado) explode: 6 + 3 por camada que tinha em dano de fogo a cada outro "
       "inimigo, que ganha 1 camada. Cada inimigo explode uma vez.", "Estouro: quem morre em chamas explode",
       afeta=["acende", "detona"], props=["Queimadura", "Área"]),
    _n("queimar", "Queimar a Si Mesmo", "R", {"queimar": 1, "pagar_vida": 1},
       "Sem Mana suficiente, as habilidades de fogo usam vida no lugar da que falta (1 por 1; fica com pelo menos 1). "
       "Com menos da metade da vida, o que você acende põe 1 camada a mais.",
       "Queimar a Si Mesmo: falta de Mana sai da vida", afeta=["fogo"], props=["Queimadura", "Recurso"]),
    _n("cinza_fria", "Cinza Fria", "R", {"cinza_fria": 1},
       f"Gelo num inimigo em chamas não apaga: consome as camadas, causa {DETONA_CAMADA} por camada em dano de gelo e "
       "dá o mesmo número de Frio.", "Cinza Fria: o gelo converte a Queimadura em dano e Frio", afeta=["frio"],
       props=["Frio", "Queimadura"]),
    _n("vapor", "Vapor", "R", {"vapor": 1},
       "Fogo num inimigo com Frio não anula: consome o Frio, deixa o alvo Exposto (1 por Frio, até 2) e acende "
       "normalmente.", "Vapor: o fogo converte o Frio em Exposto", afeta=["acende"], props=["Frio", "Exposto"]),
    _n("frio_penetrante", "Frio Penetrante", "R", {"frio_penetrante": 1},
       "Inimigos com Frio recebem +10% de dano de qualquer fonte por camada de Frio.",
       "Frio Penetrante: +10% de dano por Frio no alvo, para todo o grupo", afeta=["frio"], props=["Frio"]),
    _n("elo_elemental", "Elo Elemental", "R", {"elo_elemental": 1},
       "Quando uma invocação sua cai (inclusive sacrificada), você ganha 12 de Mana e 1 Força.",
       "Elo Elemental: quando ela cai, 12 de Mana e 1 Força", afeta=["invocacao"],
       props=["Invocação", "Recurso", "Força"]),
    _n("sacrificio", "Sacrifício", "R", {"sacrificio": 1},
       "A Combustão pode mirar uma invocação sua, e a Conflagração também as alcança: a invocação cai e o efeito dela "
       "ao cair sai dobrado.", "Sacrifício: detonar uma invocação dobra o efeito dela", afeta=["invocacao", "detona"],
       props=["Invocação", "Queimadura"]),
    _n("pavio", "Pavio Curto", "V", {"pavio": 1},
       "Combustão: em vez de detonar agora, acende um pavio. No começo da próxima vez do alvo, a Queimadura detona com "
       "+50%, com as camadas que ele tiver nesse momento.",
       "Acende um pavio: no começo da próxima vez do alvo, a Queimadura detona com +50% (40% do Poder + "
       f"{DETONA_CAMADA} por camada que ele tiver nesse momento).", versao="combustao", props=["Queimadura"]),
    _n("contagio", "Contágio", "V", {"contagio": 1},
       "Combustão: depois de detonar, metade das camadas (arredondada para cima) passa ao outro inimigo com mais "
       "camadas (empate: o de menos vida).",
       f"Detona a Queimadura do alvo (40% do Poder + {DETONA_CAMADA} por camada); metade das camadas, arredondada para "
       "cima, passa ao outro inimigo com mais camadas.", versao="combustao", props=["Queimadura"]),
    _n("bola_pesada", "Bola Pesada", "V", {"bola_pesada": 1}, "Bola de Fogo: acende 2 camadas e custa 16.",
       "Causa 100% do Poder em dano de fogo e acende 2 camadas de Queimadura.", versao="bola_fogo",
       props=["Queimadura"]),
    _n("chuva_densa", "Chuva Densa", "V", {"chuva_densa": 1},
       "Chuva de Brasas: não causa dano; acende 2 camadas em cada inimigo.",
       "Acende 2 camadas de Queimadura em cada inimigo (sem dano).", versao="chuva", props=["Queimadura", "Área"]),
    _n("estilhaco", "Estilhaço", "V", {"estilhaco": 1},
       "Lança de Gelo: não dá Frio; num alvo congelado, causa +100%.",
       "Causa 90% do Poder em dano de gelo; num alvo congelado, +100%. Não dá Frio.", versao="lanca", props=["Frio"]),
    _n("fatuo_faminto", "Fátuo Faminto", "V", {"fatuo_faminto": 1},
       "Fogo-fátuo: acende no inimigo com mais camadas (o que ainda não tem 3), em vez de no com menos.",
       "Invoca o Fogo-fátuo (18 de vida). No fim de cada vez sua, ele acende 1 camada no inimigo com mais camadas que "
       "ainda não tem 3. Quando cai, explode: 8 de fogo em cada inimigo.", versao="fogo_fatuo",
       props=["Queimadura", "Invocação"]),
]

# Versões e princípios: os mesmos efeitos. Cada regra da híbrida vira um princípio (junto de outra) ou uma versão de
# uma habilidade só; as versões e os números são os mesmos. `equivale` diz de onde veio, para a comparação (seção 16.4).
_B1 = _NUM_B + [
    _n("p_sangue", "Sangue em Fúria", "P", {"sangue_quente": 1, "sangue_frio": 1},
       "Na Fúria, cada golpe seu cura você em 15% do dano que causou. Sair da Fúria dá 1 Guarda também a cada aliado.",
       "Sangue em Fúria: na Fúria, cura 15% do dano", afeta=["golpe", "furia"], props=["Fúria", "Cura", "Guarda"],
       requer_etiqueta="furia", equivale="Sangue Quente + Sangue Frio"),
    _n("p_comando", "Comando", "P", {"peso_golpe": 1, "grito_contagiante": 1},
       "Quando você interrompe um golpe preparado ou deixa um inimigo Exposto, o próximo aliado na ordem ganha 1 Força. "
       "Quando você entra em Fúria, cada aliado ganha 1 Força.",
       "Comando: interromper, expor ou entrar em Fúria dá Força", afeta=["interrompe", "expoe", "furia"],
       props=["Força", "Exposto", "Preparações"], equivale="Peso do Golpe + Grito Contagiante"),
    _n("p_carnificina", "Carnificina", "P", {"fio_cortante": 1, "banho_sangue": 1},
       "Seus golpes num alvo só abrem 1 camada de Sangramento se o alvo já sangra. Quando um inimigo que sangra morre, "
       "cada outro inimigo ganha as camadas dele.", "Carnificina: golpes num alvo que sangra abrem mais 1 camada",
       afeta=["golpe", "sangra"], props=["Sangramento"], equivale="Fio Cortante + Banho de Sangue"),
    _n("v_rancor", "Provocação com Revide", "V", {"provoca_revide": 1},
       "Provocar: até a sua próxima vez, você revida o primeiro golpe de cada inimigo com 60% do Poder.",
       "Todos os inimigos miram você na próxima vez deles e você ganha 1 Guarda. Até a sua próxima vez, você revida o "
       "primeiro golpe de cada inimigo com 60% do Poder.", versao="provocar", props=["Mira"], equivale="Revide"),
    _n("v_sede_rubra", "Sede Rubra", "V", {"sede_rubra": 1}, "Sede de Sangue: também devolve 6 de Vigor.",
       "Causa 100% do Poder em dano físico, cura você em 40% do dano causado e devolve 6 de Vigor.", versao="sede",
       props=["Cura", "Recurso"], equivale="Fôlego Rubro"),
    _n("v_desesperada", "Fúria Desesperada", "V", {"desesperada": 1},
       "Fúria Cega: com menos da metade da sua vida, causa +30%.",
       "Causa 220% do Poder em dano físico (+30% com menos da metade da sua vida). Se o alvo morrer, causa 120% ao "
       "inimigo com menos vida (uma vez).", versao="furia_cega", equivale="Até o Fim"),
    _n("v_escudo_duplo", "Escudo Duplo", "V", {"escudo_duplo": 1},
       "Erguer Escudo: quando a Guarda vai para outro, você também ganha 1.",
       "Você, um aliado ou uma invocação ganha 1 Guarda; se não for você, você também ganha 1.",
       versao="erguer_escudo", props=["Guarda"], equivale="Escudeiro"),
    _n("v_contida", "Rugido Contido", "V", {"furia_contida": 1},
       "Rugido: na Fúria, os golpes que você recebe +20% (em vez de +40%).",
       "Causa 80% do Poder em dano físico e você entra em Fúria: seus golpes +40%, os que você recebe +20%.",
       versao="rugido", props=["Fúria"], equivale="Fúria Contida"),
    _n("v_sem_freio", "Rugido Sem Freio", "V", {"furia_sem_freio": 1},
       "Rugido: na Fúria, seus golpes +60% (em vez de +40%), mas você só pode sair depois de 2 vezes suas nela.",
       "Causa 80% do Poder em dano físico e você entra em Fúria: seus golpes +60% e os que você recebe +40%; só sai "
       "depois de 2 vezes suas.", versao="rugido", props=["Fúria"], equivale="Fúria Sem Freio"),
] + [dict(n, id="v_" + n["id"], equivale=n["nome"]) for n in _B4 if n["tipo"] == "V"]
_P1 = _NUM_P + [
    _n("p_paciencia", "Paciência", "P", {"paciente": 1, "partilhado": 1},
       "Uma Queimadura com 3 camadas não expira. Quando Morel ou Odette golpeia um inimigo em chamas, ele ganha 1 "
       "camada.", "Paciência: com 3 camadas, não expira", afeta=["acende", "transfere", "aliados"],
       props=["Queimadura"], exclui="ritmo_fogo", equivale="Fogo Paciente + Calor Partilhado"),
    _n("p_voracidade", "Voracidade", "P", {"fornalha": 1, "queimar": 1, "pagar_vida": 1},
       "Cada inimigo que você detona ou que explode dá 1 Calor (até 3); com 3, a próxima habilidade de fogo custa 0. "
       "Sem Mana suficiente, as habilidades de fogo usam vida no lugar da que falta; com menos da metade da vida, o que "
       "você acende põe 1 camada a mais.", "Voracidade: detonar dá Calor; falta de Mana sai da vida",
       afeta=["detona", "fogo"], props=["Queimadura", "Recurso"], exclui="ritmo_fogo",
       equivale="Fornalha Interior + Queimar a Si Mesmo"),
    _n("p_elementalista", "Elementalista", "P", {"elo_elemental": 1, "sacrificio": 1},
       "Quando uma invocação sua cai, você ganha 12 de Mana e 1 Força. A Combustão pode mirar uma invocação sua, e a "
       "Conflagração também as alcança: o efeito dela ao cair sai dobrado.",
       "Elementalista: invocações caídas dão Mana e Força", afeta=["invocacao", "detona"],
       props=["Invocação", "Recurso"], equivale="Elo Elemental + Sacrifício"),
    _n("v_estrondosa", "Combustão Estrondosa", "V", {"estrondosa": 1},
       "Combustão: se ela matar o alvo, ele explode: 6 + 3 por camada que tinha em dano de fogo a cada outro inimigo, "
       "que ganha 1 camada. Quem morre pela explosão não explode.",
       f"Detona a Queimadura do alvo (40% do Poder + {DETONA_CAMADA} por camada). Se ele morrer, explode: 6 + 3 por "
       "camada a cada outro inimigo, que ganha 1 camada.", versao="combustao", props=["Queimadura", "Área"],
       equivale="Estouro"),
    _n("v_termica", "Lança Térmica", "V", {"lanca_termica": 1},
       f"Lança de Gelo: num inimigo em chamas, consome as camadas: {DETONA_CAMADA} por camada em dano de gelo e o "
       "mesmo número de Frio.",
       f"Causa 90% do Poder em dano de gelo e dá 1 Frio (2 em quem prepara). Num inimigo em chamas, consome as camadas: "
       f"{DETONA_CAMADA} por camada em dano de gelo e o mesmo número de Frio.", versao="lanca",
       props=["Frio", "Queimadura"], equivale="Cinza Fria"),
    _n("v_vapor", "Bola de Vapor", "V", {"bola_vapor": 1},
       "Bola de Fogo: num inimigo com Frio, consome o Frio, deixa o alvo Exposto (1 por Frio, até 2) e acende "
       "normalmente.",
       "Causa 100% do Poder em dano de fogo e acende 1 camada. Num inimigo com Frio, consome o Frio e o deixa Exposto "
       "(1 por Frio, até 2).", versao="bola_fogo", props=["Frio", "Exposto"], equivale="Vapor"),
    _n("v_sentinela_cortante", "Sentinela Cortante", "V", {"sentinela_cortante": 1},
       "Sentinela de Gelo: enquanto ela está de pé, inimigos com Frio recebem +10% de dano por camada de Frio.",
       "Invoca a Sentinela (34 de vida); os inimigos miram nela e quem a golpeia ganha 1 Frio. Enquanto ela está de pé, "
       "inimigos com Frio recebem +10% de dano por camada.", versao="sentinela", props=["Frio", "Invocação"],
       equivale="Frio Penetrante"),
] + [dict(n, id="v_" + n["id"], equivale=n["nome"]) for n in _P4 if n["tipo"] == "V"]


def _completar(nos, estrutura, spec):
    for n in nos:
        n["custo"] = CUSTO_TIPO[n["tipo"]]
        n["estrutura"], n["spec"] = estrutura, spec
        if n.get("versao"):
            n["afeta"] = []
    return nos


ARVORES = {
    ("t4", "berserker"): _completar(_B4, "t4", "berserker"),
    ("t4", "piromante"): _completar(_P4, "t4", "piromante"),
    ("t1", "berserker"): _completar(_B1, "t1", "berserker"),
    ("t1", "piromante"): _completar(_P1, "t1", "piromante"),
}
VERSAO_CUSTO = {"bola_pesada": ("bola_fogo", 16)}  # versões que mudam o custo

# ---------------------------------------------------------------- exemplos (atalhos de montagem, não builds fechadas)
EXEMPLOS = [
    dict(id="furia", nome="Fúria", estrutura="t4", spec="berserker", estilo="arriscar",
         frase="Entra em Fúria, se cura batendo e sai na hora certa protegendo o grupo.",
         kit=["rugido", "sede", "redemoinho", "golpe_pesado", "erguer_escudo"], ultimate="furia_cega",
         nos={"sangue_quente": 1, "sangue_frio": 1, "ate_o_fim": 1, "braco": 2, "folego_largo": 1}),
    dict(id="quebrador", nome="Quebrador", estrutura="t4", spec="berserker", estilo="responder e sustentar",
         frase="Interrompe golpes preparados e expõe inimigos; cada acerto desses dá Força ao próximo aliado.",
         kit=["golpe_pesado", "joelho", "quebra_guarda", "provocar", "grito_guerra"], ultimate="muralha_viva",
         nos={"peso_golpe": 1, "desequilibra": 1, "revide": 1, "couro": 2, "folego_largo": 2}),
    dict(id="carniceiro", nome="Carniceiro", estrutura="t4", spec="berserker", estilo="construir",
         frase="Abre feridas que se multiplicam e as cobra de uma vez; quem morre sangrando passa as feridas adiante.",
         kit=["talho", "abrir_feridas", "redemoinho", "sede", "estandarte"], ultimate="furia_cega",
         nos={"fio_cortante": 1, "banho_sangue": 1, "redemoinho_sangrento": 1, "hemorragia": 1, "estandarte_sangrento": 1,
              "braco": 2}),
    dict(id="bastiao", nome="Bastião", estrutura="t4", spec="berserker", estilo="sustentar",
         frase="Junta Guarda protegendo os outros e a converte em dano com o Escudo Alto.",
         kit=["erguer_escudo", "provocar", "escudo_alto", "cerrar_dentes", "estandarte"], ultimate="muralha_viva",
         nos={"escudeiro": 1, "revide": 1, "couro": 2, "folego": 1, "folego_largo": 1}),
    dict(id="pavio", nome="Pavio", estrutura="t4", spec="piromante", estilo="construir e esperar",
         frase="Acumula camadas que não expiram, com Morel e Odette acendendo junto, e detona com o pavio.",
         kit=["brasa", "chuva", "combustao", "arma_flamejante", "lanca"], ultimate="conflagracao",
         nos={"paciente": 1, "partilhado": 1, "pavio": 1, "chama_viva": 2, "reserva": 2}),
    dict(id="fornalha", nome="Fornalha", estrutura="t4", spec="piromante", estilo="construir e arriscar",
         frase="Detona cedo e muitas vezes; quem morre em chamas explode e o Calor paga o próximo fogo.",
         kit=["brasa", "chuva", "combustao", "alastrar", "barreira"], ultimate="conflagracao",
         nos={"fornalha": 1, "estouro": 1, "contagio": 1, "queimar": 1, "chama_viva": 2}),
    dict(id="geada", nome="Geada", estrutura="t4", spec="piromante", estilo="responder e controlar",
         frase="Constrói Frio para congelar quem prepara, e o grupo bate mais em quem está gelado. Sobra 1 ponto.",
         kit=["lanca", "nevasca", "sentinela", "barreira", "meditar"], ultimate="inverno",
         nos={"frio_penetrante": 1, "foco": 2, "reserva": 2, "elo_elemental": 1}),
    dict(id="invocador", nome="Invocador", estrutura="t4", spec="piromante", estilo="construir e sacrificar",
         frase="Chama o Fogo-fátuo e a Sentinela, e os detona na hora certa para recuperar Mana e Força.",
         kit=["fogo_fatuo", "sentinela", "combustao", "brasa", "sobrecarga"], ultimate="conflagracao",
         nos={"elo_elemental": 1, "sacrificio": 1, "estouro": 1, "fatuo_faminto": 1, "chama_viva": 2}),
    dict(id="choque", nome="Choque Térmico", estrutura="t4", spec="piromante", estilo="híbrido",
         frase="Mistura fogo e gelo sem que se anulem: o gelo cobra as chamas e o fogo abre quem está gelado.",
         kit=["bola_fogo", "brasa", "lanca", "nevasca", "barreira"], ultimate="inverno",
         nos={"cinza_fria": 1, "vapor": 1, "frio_penetrante": 1, "foco": 2, "chama_viva": 1}),
]


def _t1(base, nos):
    ex = next(x for x in EXEMPLOS if x["id"] == base)
    return dict(ex, id=base + "_t1", nome=ex["nome"] + " (versões)", estrutura="t1",
                frase="A mesma ideia com versões e princípios.", nos=nos)


# Para comparar com o protótipo tático (etapa8-tatico): os equivalentes em cards dos kits de lá, sem talentos (lá, os
# talentos são outros). Não usam o orçamento; servem só à comparação dos mesmos encontros.
EXEMPLOS += [
    dict(id="tatico_berserker", nome="Comparar com o tático", estrutura="t4", spec="berserker", estilo="comparação",
         frase="O kit do Berserker do protótipo tático em cards: Golpe Pesado; Golpe no Joelho no lugar do Golpe de "
               "Escudo; Quebra-Guarda no lugar da Corrente; Redemoinho; Provocar no lugar do Guarda-costas. Sem "
               "talentos.", kit=["golpe_pesado", "joelho", "quebra_guarda", "redemoinho", "provocar"],
         ultimate="furia_cega", nos={}, comparacao=True),
    dict(id="tatico_piromante", nome="Comparar com o tático", estrutura="t4", spec="piromante", estilo="comparação",
         frase="O kit do Piromante do protótipo tático em cards: Bola de Fogo, Chuva de Brasas, Combustão, Sentinela; "
               "Escudo de Chamas no lugar da Muralha de Fogo (não há chão nos cards). Sem talentos.",
         kit=["bola_fogo", "chuva", "combustao", "sentinela", "escudo_chamas"], ultimate="conflagracao", nos={},
         comparacao=True),
]
EXEMPLOS += [
    _t1("furia", {"p_sangue": 1, "v_desesperada": 1, "v_sede_rubra": 1, "braco": 2, "folego_largo": 1, "v_contida": 1}),
    _t1("quebrador", {"p_comando": 1, "v_desequilibra": 1, "v_rancor": 1, "couro": 2, "folego_largo": 2}),
    _t1("carniceiro", {"p_carnificina": 1, "v_redemoinho_sangrento": 1, "v_hemorragia": 1, "v_estandarte_sangrento": 1,
                       "braco": 2, "v_sede_rubra": 1}),
    _t1("pavio", {"p_paciencia": 1, "v_pavio": 1, "chama_viva": 2, "reserva": 2, "v_chuva_densa": 1}),
    _t1("fornalha", {"p_voracidade": 1, "v_estrondosa": 1, "v_chuva_densa": 1, "chama_viva": 2, "foco": 2}),
    _t1("invocador", {"p_elementalista": 1, "v_fatuo_faminto": 1, "v_estrondosa": 1, "chama_viva": 2,
                      "v_sentinela_cortante": 1, "reserva": 1}),
]

# ---------------------------------------------------------------- os inimigos (famílias do jogo, simplificadas)
# poder: o golpe comum; magia: as habilidades de conjurador; habs: o que sorteiam (chance_hab por vez);
# res: multiplicador por tipo (acima de 1, fraqueza); tracos: "gigante" resiste a atordoar e congelar metade das vezes;
# "morto-vivo" não sangra.
INIMIGOS = {
    "lobo": {"nome": "Lobo", "retrato": "lobo", "vida": 42, "poder": 11, "agi": 6, "golpe": "Mordida",
             "habs": ["mordida", "uivo"]},
    "bandido": {"nome": "Bandido", "retrato": "bandido", "vida": 48, "poder": 12, "agi": 5, "golpe": "Facada",
                "habs": ["golpe_sujo"]},
    "mercenario": {"nome": "Mercenário", "retrato": "mercenario", "vida": 80, "poder": 13, "agi": 4, "golpe": "Espadada",
                   "habs": ["esmagar", "golpe_sujo", "grito"], "chance_hab": 0.45},
    "sapo": {"nome": "Sapo-touro", "retrato": "sapo", "vida": 62, "poder": 12, "agi": 4, "golpe": "Língua",
             "habs": ["veneno", "agarrar"]},
    "bruxa": {"nome": "Bruxa do Pântano", "retrato": "bruxa_brejo", "vida": 56, "poder": 9, "magia": 16, "agi": 5,
              "golpe": "Toque sombrio", "tipo": "sombra", "habs": ["maldicao", "bola_fogo", "cura"]},
    "troll": {"nome": "Troll da Montanha", "retrato": "troll", "vida": 230, "poder": 21, "agi": 1, "golpe": "Pancada",
              "habs": ["esmagar", "regenerar"], "chance_hab": 0.45, "tracos": ["gigante"], "res": {"fogo": 1.4}},
    "rato": {"nome": "Rato Gigante", "retrato": "rato", "vida": 22, "poder": 7, "agi": 6, "golpe": "Mordida",
             "habs": ["mordida", "veneno"]},
    "esqueleto": {"nome": "Esqueleto", "retrato": "esqueleto", "vida": 54, "poder": 12, "agi": 3, "golpe": "Espadada",
                  "habs": ["investida"], "tracos": ["morto-vivo"]},
    "cultista": {"nome": "Cultista", "retrato": "cultista", "vida": 48, "poder": 7, "magia": 14, "agi": 4,
                 "golpe": "Adaga", "tipo": "sombra", "habs": ["bola_sombra", "cura", "grito_terror"]},
}
HABS_INIMIGO = {
    "mordida": "Mordida Sangrenta: 100% e 70% de chance de abrir 1 camada de Sangramento.",
    "uivo": "Uivo: os inimigos ficam Fortalecidos (+30%) por 2 vezes deles.",
    "grito": "Grito de Guerra: os inimigos ficam Fortalecidos (+30%) por 2 vezes deles.",
    "golpe_sujo": "Golpe Sujo: 110% e 35% de chance de Enfraquecer (−30%) por 2 vezes do alvo.",
    "esmagar": "Golpe Esmagador: prepara numa vez e golpeia com 220% na seguinte. Atordoar ou congelar interrompe.",
    "regenerar": "Regenerar: com 70% da vida ou menos, recupera 15% da vida máxima.",
    "veneno": "Veneno: 80% e Veneno (2 por turno, 3 turnos).",
    "agarrar": "Agarrão: 80% e 40% de chance de prender (o alvo perde a próxima vez).",
    "maldicao": "Maldição: o alvo fica Enfraquecido (−30%) por 3 vezes dele.",
    "bola_fogo": "Bola de Fogo: 130% da magia em fogo.",
    "bola_sombra": "Esfera Sombria: 130% da magia em sombra.",
    "cura": "Cura: o inimigo mais ferido (abaixo de 60%) recupera 25% da vida máxima. Uma vez a cada 3 rodadas.",
    "grito_terror": "Grito de Terror: o alvo fica Enfraquecido (−30%) por 2 vezes dele.",
    "investida": "Investida: 130% e 25% de chance de atordoar.",
}

ENCONTROS = {
    "lobos": {"nome": "Três lobos", "semente": 101, "inimigos": ["lobo", "lobo", "lobo"],
              "resumo": "Enxame sem golpe preparado; o uivo fortalece o bando, as mordidas sangram.",
              "favorece": "Área, explosões, Fúria", "desfavorece": "Quem só responde a preparações"},
    "mercenario": {"nome": "O mercenário e dois bandidos", "semente": 202,
                   "inimigos": ["mercenario", "bandido", "bandido"],
                   "resumo": "O mercenário prepara o Golpe Esmagador e grita ordens; os bandidos enfraquecem.",
                   "favorece": "Interromper, congelar, Exposto", "desfavorece": "Fogo lento"},
    "bruxa": {"nome": "A bruxa, o bandido e o sapo", "semente": 303, "inimigos": ["bruxa", "bandido", "sapo"],
              "resumo": "A bruxa cura o mais ferido e enfraquece; o sapo envenena e prende.",
              "favorece": "Quem escolhe bem o alvo", "desfavorece": "Fúria (presa nela), camadas lentas (a cura)"},
    "troll": {"nome": "O troll sozinho", "semente": 404, "inimigos": ["troll"],
              "resumo": "Um gigante só: prepara o Golpe Esmagador, regenera e é fraco ao fogo (+40%).",
              "favorece": "Interromper sem atordoar, fogo, invocações que absorvem",
              "desfavorece": "Explosões e Banho de Sangue (ninguém mais morre), Fúria (o golpe preparado nela)"},
    "cultista": {"nome": "O cultista e dois esqueletos", "semente": 505,
                 "inimigos": ["cultista", "esqueleto", "esqueleto"],
                 "resumo": "Esqueletos não sangram e atordoam na investida; o cultista cura e enfraquece.",
                 "favorece": "Fogo, gelo, Guarda", "desfavorece": "Sangramento"},
    "sorteado": {"nome": "Sorteado entre os comuns", "semente": 606, "sorteio": [
        ["lobo", "lobo"], ["rato", "rato", "rato", "rato"], ["bandido", "bandido"], ["sapo", "rato", "rato"],
        ["bandido", "lobo", "lobo"], ["mercenario", "rato", "rato"], ["esqueleto", "rato", "rato"]],
                 "resumo": "Um grupo sorteado pela semente, para não haver só encontros escolhidos.",
                 "favorece": "—", "desfavorece": "—"},
}
