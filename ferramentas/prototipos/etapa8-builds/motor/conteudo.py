"""O conteúdo provisório do protótipo X1 da etapa 8 (31/10/2026; nada no jogo): montagem de builds e a estrutura dos
talentos, pela seção 15 do roadmapIDEIAS/28-ETAPA8-HABILIDADES-TALENTOS-E-BUILDS.md.

- Duas especializações (Berserker e Piromante), cada uma com oito habilidades para escolher cinco, e a ultimate fixa.
- Duas estruturas de talentos com o mesmo orçamento (7 pontos): a híbrida (T4: regras por etiqueta, versões em
  habilidades centrais e números que disputam os pontos) e a de versões com princípios (T1).
- Exemplos de build são atalhos de montagem: carregam kit e nós, e tudo continua editável.
- Encontros com inimigos que existem no jogo (lobos, bandidos, mercenário, sapo, bruxa do pântano, troll, ratos),
  simplificados. Sem intenção geral, travas, chefe abalado, ambientes nem mudanças de ordem.

Valores de teste, não catálogo: servem para observar decisões, não para balancear a campanha."""

PONTOS = 7          # o orçamento de talentos
ESPACOS = 5         # habilidades no kit, além da ultimate (fixa por especialização)
FICHA_TETO = 2      # Guarda, Força e Exposto
CAMADAS_TETO = 3    # Queimadura
PINGOS = 3          # duração da Queimadura, em turnos do alvo
PINGO_CAMADA = 3    # dano de fogo por camada, no começo de cada turno do alvo
DETONA_CAMADA = 9   # dano de fogo por camada detonada
REGEN = 6           # recurso no começo de cada turno de quem age
BASICO_GANHA = 6    # Atacar e Defender devolvem mais 6
LIMITE_RODADAS = 30

# Linhas da árvore híbrida: quantos pontos as linhas anteriores precisam ter
REQUISITO_LINHA = {1: 0, 2: 2, 3: 4}
CUSTO_TIPO = {"N": 1, "R": 2, "V": 1, "P": 3}
NOME_TIPO = {"N": "Número", "R": "Regra", "V": "Versão", "P": "Princípio"}
ESTRUTURAS = {
    "t4": {"nome": "Híbrida", "frase": "Regras que valem para famílias de habilidades, versões em habilidades centrais e "
                                       "números, todos disputando os mesmos 7 pontos. Três linhas: a 2 pede 2 pontos "
                                       "na linha 1; a 3 pede 4 pontos nas linhas 1 e 2."},
    "t1": {"nome": "Versões e princípios", "frase": "Uma versão por habilidade (1 ponto) e princípios que definem a "
                                                    "especialização (3 pontos), disputando os mesmos 7 pontos. Sem "
                                                    "linhas nem números."},
}

TIPOS = {"fisico": "físico", "fogo": "fogo", "gelo": "gelo", "sagrado": "sagrado", "sombra": "sombra"}

# ---------------------------------------------------------------- o grupo
HEROI = {
    "berserker": {"nome": "Jean", "classe": "Guerreiro", "spec": "Berserker", "retrato": "guerreiro", "vida": 64,
                  "recurso": "Vigor", "recurso_max": 60, "poder": 14, "agi": 5, "ultimate": "furia_cega"},
    "piromante": {"nome": "Jean", "classe": "Mago", "spec": "Piromante", "retrato": "mago", "vida": 52,
                  "recurso": "Mana", "recurso_max": 60, "poder": 14, "agi": 6, "ultimate": "conflagracao"},
}
COMPANHEIROS = {
    "morel": {"nome": "Morel", "retrato": "morel", "vida": 52, "recurso": "Vigor", "recurso_max": 50, "poder": 11,
              "agi": 7, "kit": ["atacar", "oportuno", "proteger", "defender"]},
    "odete": {"nome": "Odette", "retrato": "odete", "vida": 44, "recurso": "Fé", "recurso_max": 50, "poder": 9,
              "agi": 4, "kit": ["bastao", "prece", "bencao", "defender"]},
}

# ---------------------------------------------------------------- as habilidades
# alvo: inimigo | inimigos | aliado | proprio.  tipo: o tipo de dano.  etiquetas: o que as regras de talento perguntam.
HABILIDADES = {
    # comuns (fora do kit)
    "atacar": {"nome": "Atacar", "alvo": "inimigo", "custo": 0, "mult": 1.0, "tipo": "fisico", "etiquetas": ["golpe"],
               "desc": f"Causa 100% do Poder em dano físico. Recupera {BASICO_GANHA} a mais."},
    "defender": {"nome": "Defender", "alvo": "proprio", "custo": 0, "etiquetas": [],
                 "desc": f"Ganha 1 Guarda. Recupera {BASICO_GANHA} a mais."},

    # Berserker (Guerreiro e a especialização)
    "golpe_pesado": {"nome": "Golpe Pesado", "spec": "berserker", "alvo": "inimigo", "custo": 14, "mult": 1.4,
                     "tipo": "fisico", "etiquetas": ["golpe"],
                     "desc": "Causa 140% do Poder em dano físico."},
    "joelho": {"nome": "Golpe no Joelho", "spec": "berserker", "alvo": "inimigo", "custo": 14, "mult": 0.7,
               "tipo": "fisico", "etiquetas": ["golpe", "interrompe"],
               "desc": "Causa 70% do Poder em dano físico e tenta atordoar: certo em quem prepara um golpe (interrompe), "
                       "40% nos outros. Gigantes resistem metade das vezes; quem está Firme não é atordoado."},
    "quebra_guarda": {"nome": "Quebra-Guarda", "spec": "berserker", "alvo": "inimigo", "custo": 12, "mult": 0.9,
                      "tipo": "fisico", "etiquetas": ["golpe", "expoe"],
                      "desc": "Causa 90% do Poder em dano físico e deixa o alvo Exposto (1)."},
    "erguer_escudo": {"nome": "Erguer Escudo", "spec": "berserker", "alvo": "aliado", "custo": 8, "etiquetas": ["protecao"],
                      "desc": "Você ou um aliado ganha 1 Guarda."},
    "provocar": {"nome": "Provocar", "spec": "berserker", "alvo": "proprio", "custo": 12, "etiquetas": ["protecao"],
                 "desc": "Todos os inimigos miram você na próxima vez deles. Você ganha 1 Guarda."},
    "rugido": {"nome": "Rugido", "spec": "berserker", "alvo": "inimigo", "custo": 10, "mult": 0.8, "tipo": "fisico",
               "etiquetas": ["golpe", "furia"],
               "desc": "Causa 80% do Poder em dano físico e você entra em Fúria: seus golpes +40% e os golpes que você "
                       "recebe +40%. Na sua vez, sair da Fúria não gasta a ação e dá 12 de Vigor e 1 Guarda."},
    "sede": {"nome": "Sede de Sangue", "spec": "berserker", "alvo": "inimigo", "custo": 16, "mult": 1.0,
             "tipo": "fisico", "etiquetas": ["golpe", "cura"],
             "desc": "Causa 100% do Poder em dano físico e cura você em 40% do dano causado."},
    "redemoinho": {"nome": "Redemoinho", "spec": "berserker", "alvo": "inimigos", "custo": 20, "mult": 0.55,
                   "tipo": "fisico", "etiquetas": ["golpe", "area"],
                   "desc": "Causa 55% do Poder em dano físico a cada inimigo."},
    "furia_cega": {"nome": "Fúria Cega", "spec": "berserker", "alvo": "inimigo", "custo": 20, "mult": 2.2,
                   "tipo": "fisico", "etiquetas": ["golpe"], "ultimate": True,
                   "desc": "Causa 220% do Poder em dano físico. Se o alvo morrer, causa 120% ao inimigo com menos vida "
                           "(uma vez)."},

    # Piromante (Mago e a especialização)
    "bola_fogo": {"nome": "Bola de Fogo", "spec": "piromante", "alvo": "inimigo", "custo": 12, "mult": 1.0,
                  "tipo": "fogo", "etiquetas": ["fogo", "acende"],
                  "desc": "Causa 100% do Poder em dano de fogo e acende 1 camada de Queimadura."},
    "brasa": {"nome": "Brasa", "spec": "piromante", "alvo": "inimigo", "custo": 7, "mult": 0.5, "tipo": "fogo",
              "etiquetas": ["fogo", "acende"],
              "desc": "Causa 50% do Poder em dano de fogo e acende 1 camada de Queimadura."},
    "chuva": {"nome": "Chuva de Brasas", "spec": "piromante", "alvo": "inimigos", "custo": 18, "mult": 0.3,
              "tipo": "fogo", "etiquetas": ["fogo", "acende", "area"],
              "desc": "Causa 30% do Poder em dano de fogo a cada inimigo e acende 1 camada em cada um."},
    "combustao": {"nome": "Combustão", "spec": "piromante", "alvo": "inimigo", "custo": 14, "mult": 0.4,
                  "tipo": "fogo", "etiquetas": ["fogo", "detona"],
                  "desc": f"Detona a Queimadura do alvo: causa 40% do Poder + {DETONA_CAMADA} por camada em dano de fogo. "
                          "A Queimadura apaga."},
    "lanca": {"nome": "Lança de Gelo", "spec": "piromante", "alvo": "inimigo", "custo": 12, "mult": 0.9,
              "tipo": "gelo", "etiquetas": ["gelo", "congela", "interrompe"],
              "desc": "Causa 90% do Poder em dano de gelo. 35% de chance de congelar: o alvo perde a próxima vez e o "
                      "golpe que preparava. Gigantes resistem metade das vezes; quem está Firme não congela."},
    "barreira": {"nome": "Barreira", "spec": "piromante", "alvo": "aliado", "custo": 8, "etiquetas": ["protecao"],
                 "desc": "Você ou um aliado ganha 1 Guarda."},
    "escudo_chamas": {"nome": "Escudo de Chamas", "spec": "piromante", "alvo": "aliado", "custo": 12,
                      "etiquetas": ["protecao", "fogo", "acende"],
                      "desc": "Você ou um aliado ganha 1 Guarda. Até o fim da próxima rodada, cada inimigo que golpear "
                              "quem tem o escudo ganha 1 camada de Queimadura."},
    "meditar": {"nome": "Meditar", "spec": "piromante", "alvo": "proprio", "custo": 0, "etiquetas": [],
                "desc": "Recupera 24 de Mana."},
    "conflagracao": {"nome": "Conflagração", "spec": "piromante", "alvo": "inimigos", "custo": 20, "mult": 0.4,
                     "tipo": "fogo", "etiquetas": ["fogo", "detona", "area"], "ultimate": True,
                     "desc": f"Detona a Queimadura de cada inimigo: 40% do Poder + {DETONA_CAMADA} por camada em dano de "
                             "fogo em cada um. As Queimaduras apagam."},

    # Morel (kit fixo)
    "oportuno": {"nome": "Golpe Oportuno", "alvo": "inimigo", "custo": 14, "mult": 1.2, "tipo": "fisico",
                 "etiquetas": ["golpe"],
                 "desc": "Causa 120% do Poder em dano físico; +60% em quem está atordoado, preso ou preparando um golpe."},
    "proteger": {"nome": "Proteger", "alvo": "aliado_outro", "custo": 12, "etiquetas": ["protecao"],
                 "desc": "Os golpes contra o aliado vêm para Morel até a próxima vez dele."},
    # Odette (kit fixo)
    "bastao": {"nome": "Bastão", "alvo": "inimigo", "custo": 0, "mult": 1.0, "tipo": "sagrado", "etiquetas": ["golpe"],
               "desc": f"Causa 100% do Poder em dano sagrado. Recupera {BASICO_GANHA} a mais."},
    "prece": {"nome": "Prece", "alvo": "aliado", "custo": 14, "cura": 18, "etiquetas": ["cura"],
              "desc": "Cura 18 de vida de um aliado."},
    "bencao": {"nome": "Bênção", "alvo": "aliado", "custo": 10, "etiquetas": [],
               "desc": "Um aliado ganha 1 Força."},
}
POOL = {
    "berserker": ["golpe_pesado", "joelho", "quebra_guarda", "erguer_escudo", "provocar", "rugido", "sede", "redemoinho"],
    "piromante": ["bola_fogo", "brasa", "chuva", "combustao", "lanca", "barreira", "escudo_chamas", "meditar"],
}

REGRAS_LUTA = [
    "Ordem fixa pela Agilidade; cada combatente age uma vez por rodada. Você escolhe as ações de Jean, Morel e Odette.",
    "Fichas (até 2 de cada): Guarda, o próximo golpe recebido −50%; Força, a próxima ação que golpeia +50%; Exposto, o "
    "próximo golpe recebido +50%. Guarda e Exposto se anulam.",
    "Cadeia é tudo o que uma ação provoca. Cada efeito acontece uma vez por motivo em cada cadeia: cada morto explode "
    "uma vez, cada inimigo dá 1 Calor, cada alvo cura uma vez o Sangue Quente.",
    "Revide, espinhos e escudos respondem a golpes de ação. O dano deles, da Queimadura e das explosões não provoca "
    "outra resposta.",
    "Atordoado, congelado ou preso: perde a próxima vez e o golpe que preparava; depois fica Firme por 2 vezes dele.",
    f"Recurso: +{REGEN} no começo de cada vez; Atacar, Bastão e Defender devolvem mais {BASICO_GANHA}. A ultimate, uma "
    "vez por luta.",
]

FICHAS = {
    "guarda": {"nome": "Guarda", "desc": "O próximo golpe recebido −50%. Anula 1 Exposto ao chegar."},
    "forca": {"nome": "Força", "desc": "A próxima ação que golpeia +50% (em área, vale para todos os alvos)."},
    "exposto": {"nome": "Exposto", "desc": "O próximo golpe recebido +50%. Anula 1 Guarda ao chegar."},
}

# ---------------------------------------------------------------- os talentos
# Cada nó: tipo (N, R, V, P), custo por rank (CUSTO_TIPO), ranks, linha (só na híbrida), efeitos (as bandeiras que o
# motor lê; nos números, o valor cresce com o rank), afeta (as etiquetas do kit que ele muda; "aliados", "recebe" e
# "sempre" para o que não depende do kit), versao (a habilidade que a versão troca), exclui (o grupo de exclusão),
# texto (a regra, como a montagem mostra) e nota (a linha curta que aparece em cada habilidade afetada).
_B4 = [
    dict(id="couro", nome="Couro Grosso", tipo="N", ranks=2, linha=1, efeitos={"couro": 1}, afeta=["sempre"],
         texto="+12 de vida máxima por ponto.", nota="+12 de vida máxima por ponto"),
    dict(id="braco", nome="Braço Pesado", tipo="N", ranks=2, linha=1, efeitos={"braco": 1}, afeta=["golpe"],
         texto="Seus golpes +8% por ponto.", nota="Braço Pesado: +8% por ponto"),
    dict(id="sangue_quente", nome="Sangue Quente", tipo="R", linha=1, efeitos={"sangue_quente": 1},
         afeta=["golpe"], requer_etiqueta="furia",
         texto="Na Fúria, cada golpe seu cura você em 15% do dano que causou (inclusive o Revide).",
         nota="Sangue Quente: na Fúria, cura 15% do dano"),
    dict(id="peso_golpe", nome="Peso do Golpe", tipo="R", linha=1, efeitos={"peso_golpe": 1},
         afeta=["interrompe", "expoe"],
         texto="Quando você interrompe um golpe preparado ou deixa um inimigo Exposto, o próximo aliado na ordem "
               "ganha 1 Força.",
         nota="Peso do Golpe: interromper ou expor dá 1 Força ao próximo aliado"),
    dict(id="desequilibra", nome="Golpe que Desequilibra", tipo="V", linha=2, versao="golpe_pesado", exclui="golpe_pesado",
         efeitos={"desequilibra": 1},
         texto="Golpe Pesado: causa 110% do Poder e interrompe o golpe que o alvo prepara, sem atordoar (vale em "
               "gigantes e em quem está Firme).",
         nota="Causa 110% do Poder em dano físico e interrompe o golpe que o alvo prepara, sem atordoar. Vale em "
              "gigantes e em quem está Firme."),
    dict(id="acumulado", nome="Golpe Acumulado", tipo="V", linha=2, versao="golpe_pesado", exclui="golpe_pesado",
         efeitos={"acumulado": 1},
         texto="Golpe Pesado: consome as Forças do grupo inteiro (as suas e as dos aliados): +50% por Força.",
         nota="Causa 140% do Poder em dano físico e consome as Forças do grupo inteiro: +50% por Força."),
    dict(id="desafiador", nome="Rugido Desafiador", tipo="V", linha=2, versao="rugido", exclui="rugido",
         efeitos={"desafiador": 1},
         texto="Rugido: além de entrar em Fúria, todos os inimigos miram você na próxima vez deles.",
         nota="Causa 80% do Poder em dano físico, você entra em Fúria e todos os inimigos miram você na próxima vez "
              "deles."),
    dict(id="revide", nome="Revide", tipo="R", linha=2, efeitos={"revide": 1}, afeta=["recebe"],
         texto="Quando um inimigo golpeia você, você revida com 60% do Poder. Uma vez por rodada. Revide não "
               "responde a outro revide nem a espinhos.",
         nota="Revide"),
    dict(id="sangue_frio", nome="Sangue Frio", tipo="R", linha=2, efeitos={"sangue_frio": 1}, afeta=["furia"],
         texto="Sair da Fúria dá 1 Guarda também a cada aliado.",
         nota="Sangue Frio: sair da Fúria dá 1 Guarda a cada aliado"),
    dict(id="folego", nome="Fôlego Rubro", tipo="R", linha=3, efeitos={"folego": 1}, afeta=["cura", "sempre"],
         texto="Quando você é curado (por você ou por um aliado), ganha 6 de Vigor. Uma vez por rodada.",
         nota="Fôlego Rubro: ser curado dá 6 de Vigor (1 vez por rodada)"),
    dict(id="ate_o_fim", nome="Até o Fim", tipo="R", linha=3, efeitos={"ate_o_fim": 1}, afeta=["golpe"],
         texto="Com menos da metade da vida, seus golpes +30%.",
         nota="Até o Fim: abaixo da metade da vida, +30%"),
]
_P4 = [
    dict(id="chama_viva", nome="Chama Viva", tipo="N", ranks=2, linha=1, efeitos={"chama_viva": 1},
         afeta=["acende", "detona"],
         texto="Queimadura (pingos e detonações) +15% por ponto.", nota="Chama Viva: Queimadura +15% por ponto"),
    dict(id="reserva", nome="Reserva Ardente", tipo="N", ranks=2, linha=1, efeitos={"reserva": 1}, afeta=["sempre"],
         texto="+12 de Mana máxima por ponto.", nota="+12 de Mana máxima por ponto"),
    dict(id="paciente", nome="Fogo Paciente", tipo="R", linha=1, efeitos={"paciente": 1}, afeta=["acende"],
         texto="Uma Queimadura com 3 camadas não expira: pinga até ser detonada ou o alvo morrer.",
         nota="Fogo Paciente: com 3 camadas, não expira"),
    dict(id="partilhado", nome="Calor Partilhado", tipo="R", linha=1, efeitos={"partilhado": 1}, afeta=["aliados"],
         texto="Quando Morel ou Odette golpeia um inimigo em chamas, ele ganha 1 camada.",
         nota="Calor Partilhado"),
    dict(id="fornalha", nome="Fornalha Interior", tipo="R", linha=1, efeitos={"fornalha": 1}, afeta=["detona"],
         texto="Cada inimigo que você detona ou que explode dá 1 Calor (até 3). Com 3, a próxima habilidade de fogo "
               "custa 0 e gasta o Calor. O mesmo inimigo dá 1 Calor por cadeia.",
         nota="Fornalha Interior: cada inimigo detonado dá 1 Calor"),
    dict(id="pavio", nome="Pavio Curto", tipo="V", linha=2, versao="combustao", exclui="combustao",
         efeitos={"pavio": 1},
         texto="Combustão: em vez de detonar agora, acende um pavio. No começo da próxima vez do alvo, a Queimadura "
               "detona com +50%, com as camadas que ele tiver nesse momento.",
         nota="Acende um pavio: no começo da próxima vez do alvo, a Queimadura detona com +50% (40% do Poder + "
              f"{DETONA_CAMADA} por camada que ele tiver nesse momento)."),
    dict(id="contagio", nome="Contágio", tipo="V", linha=2, versao="combustao", exclui="combustao",
         efeitos={"contagio": 1},
         texto="Combustão: depois de detonar, metade das camadas (arredondada para cima) passa ao outro inimigo com "
               "mais camadas (empate: o de menos vida).",
         nota=f"Detona a Queimadura do alvo (40% do Poder + {DETONA_CAMADA} por camada); metade das camadas, "
              "arredondada para cima, passa ao outro inimigo com mais camadas."),
    dict(id="estouro", nome="Estouro", tipo="R", linha=2, efeitos={"estouro": 1}, afeta=["acende", "detona"],
         texto="Um inimigo que morre em chamas (ou detonado) explode: 6 + 3 por camada que tinha em dano de fogo a "
               "cada outro inimigo, que ganha 1 camada. Cada inimigo explode uma vez.",
         nota="Estouro: quem morre em chamas explode"),
    dict(id="queimar", nome="Queimar a Si Mesmo", tipo="R", linha=3, efeitos={"queimar": 1, "pagar_vida": 1},
         afeta=["fogo"],
         texto="Sem Mana suficiente, as habilidades de fogo usam vida no lugar da que falta (1 por 1; fica com pelo "
               "menos 1). Com menos da metade da vida, o que você acende põe 1 camada a mais.",
         nota="Queimar a Si Mesmo: falta de Mana sai da vida"),
    dict(id="cinza_fria", nome="Cinza Fria", tipo="R", linha=3, efeitos={"cinza_fria": 1}, afeta=["congela"],
         texto=f"Gelo num inimigo em chamas consome as camadas: {DETONA_CAMADA} por camada em dano de gelo e +15% de "
               "chance de congelar por camada.",
         nota="Cinza Fria: consome a Queimadura do alvo como gelo"),
]
_B1 = [
    dict(id="p_sangue", nome="Sangue em Fúria", tipo="P", efeitos={"sangue_quente": 1, "sangue_frio": 1},
         afeta=["golpe", "furia"], requer_etiqueta="furia",
         texto="Na Fúria, cada golpe seu cura você em 15% do dano que causou. Sair da Fúria dá 1 Guarda também a "
               "cada aliado.",
         nota="Sangue em Fúria: na Fúria, cura 15% do dano"),
    dict(id="p_peso", nome="Peso do Golpe", tipo="P", efeitos={"peso_golpe": 1}, afeta=["interrompe", "expoe"],
         texto="Quando você interrompe um golpe preparado ou deixa um inimigo Exposto, o próximo aliado na ordem "
               "ganha 1 Força.",
         nota="Peso do Golpe: interromper ou expor dá 1 Força ao próximo aliado"),
    dict(id="v_desequilibra", nome="Golpe que Desequilibra", tipo="V", versao="golpe_pesado", exclui="golpe_pesado",
         efeitos={"desequilibra": 1}, texto=_B4[4]["texto"], nota=_B4[4]["nota"]),
    dict(id="v_acumulado", nome="Golpe Acumulado", tipo="V", versao="golpe_pesado", exclui="golpe_pesado",
         efeitos={"acumulado": 1}, texto=_B4[5]["texto"], nota=_B4[5]["nota"]),
    dict(id="v_desafiador", nome="Rugido Desafiador", tipo="V", versao="rugido", exclui="rugido",
         efeitos={"desafiador": 1}, texto=_B4[6]["texto"], nota=_B4[6]["nota"]),
    dict(id="v_contido", nome="Rugido Contido", tipo="V", versao="rugido", exclui="rugido", efeitos={"contido": 1},
         texto="Rugido: não causa dano; você entra em Fúria e ganha 1 Guarda.",
         nota="Você entra em Fúria e ganha 1 Guarda (sem dano)."),
    dict(id="v_espinhos", nome="Escudo de Espinhos", tipo="V", versao="erguer_escudo", exclui="erguer_escudo",
         efeitos={"escudo_espinhos": 1},
         texto="Erguer Escudo: além da Guarda, o próximo inimigo que golpear o protegido leva 60% do seu Poder em dano "
               "físico (uma vez; não provoca revide).",
         nota="Você ou um aliado ganha 1 Guarda; o próximo inimigo que golpeá-lo leva 60% do seu Poder em dano físico "
              "(uma vez)."),
    dict(id="v_sede_rubra", nome="Sede Rubra", tipo="V", versao="sede", exclui="sede", efeitos={"sede_rubra": 1},
         texto="Sede de Sangue: também devolve 6 de Vigor.",
         nota="Causa 100% do Poder em dano físico, cura você em 40% do dano causado e devolve 6 de Vigor."),
    dict(id="v_temerario", nome="Redemoinho Temerário", tipo="V", versao="redemoinho", exclui="redemoinho",
         efeitos={"temerario": 1},
         texto="Redemoinho: 75% do Poder a cada inimigo; você fica Exposto (1).",
         nota="Causa 75% do Poder em dano físico a cada inimigo; você fica Exposto (1)."),
    dict(id="v_rancor", nome="Provocação com Revide", tipo="V", versao="provocar", exclui="provocar",
         efeitos={"provoca_revide": 1},
         texto="Provocar: até a sua próxima vez, você revida o primeiro golpe de cada inimigo com 60% do Poder.",
         nota="Todos os inimigos miram você na próxima vez deles e você ganha 1 Guarda. Até a sua próxima vez, você "
              "revida o primeiro golpe de cada inimigo com 60% do Poder."),
    dict(id="v_aberto", nome="Quebra-Guarda Aberto", tipo="V", versao="quebra_guarda", exclui="quebra_guarda",
         efeitos={"aberto": 1},
         texto="Quebra-Guarda: deixa o alvo Exposto (2).",
         nota="Causa 90% do Poder em dano físico e deixa o alvo Exposto (2)."),
]
_P1 = [
    dict(id="p_paciencia", nome="Paciência", tipo="P", efeitos={"paciente": 1, "partilhado": 1},
         afeta=["acende", "aliados"],
         texto="Uma Queimadura com 3 camadas não expira. Quando Morel ou Odette golpeia um inimigo em chamas, ele "
               "ganha 1 camada.",
         nota="Paciência: com 3 camadas, não expira"),
    dict(id="p_voracidade", nome="Voracidade", tipo="P", efeitos={"fornalha": 1, "pagar_vida": 1},
         afeta=["detona", "fogo"],
         texto="Cada inimigo que você detona dá 1 Calor (até 3); com 3, a próxima habilidade de fogo custa 0. Sem Mana "
               "suficiente, as habilidades de fogo usam vida no lugar da que falta.",
         nota="Voracidade: detonar dá Calor; falta de Mana sai da vida"),
    dict(id="v_pavio", nome="Pavio Curto", tipo="V", versao="combustao", exclui="combustao", efeitos={"pavio": 1},
         texto=_P4[5]["texto"], nota=_P4[5]["nota"]),
    dict(id="v_contagio", nome="Contágio", tipo="V", versao="combustao", exclui="combustao", efeitos={"contagio": 1},
         texto=_P4[6]["texto"], nota=_P4[6]["nota"]),
    dict(id="v_estrondosa", nome="Combustão Estrondosa", tipo="V", versao="combustao", exclui="combustao",
         efeitos={"estrondosa": 1},
         texto="Combustão: se ela matar o alvo, ele explode: 6 + 3 por camada que tinha em dano de fogo a cada outro "
               "inimigo, que ganha 1 camada. Quem morre pela explosão não explode.",
         nota=f"Detona a Queimadura do alvo (40% do Poder + {DETONA_CAMADA} por camada). Se ele morrer, explode: 6 + 3 "
              "por camada a cada outro inimigo, que ganha 1 camada."),
    dict(id="v_termica", nome="Lança Térmica", tipo="V", versao="lanca", exclui="lanca", efeitos={"cinza_fria": 1},
         texto=f"Lança de Gelo: num inimigo em chamas, consome as camadas: {DETONA_CAMADA} por camada em dano de gelo e "
               "+15% de chance de congelar por camada.",
         nota=f"Causa 90% do Poder em dano de gelo; num inimigo em chamas, consome as camadas ({DETONA_CAMADA} por "
              "camada em gelo e +15% de chance de congelar por camada). 35% de chance de congelar."),
    dict(id="v_pesada", nome="Bola Pesada", tipo="V", versao="bola_fogo", exclui="bola_fogo", efeitos={"bola_pesada": 1},
         texto="Bola de Fogo: acende 2 camadas e custa 16.",
         nota="Causa 100% do Poder em dano de fogo e acende 2 camadas de Queimadura."),
    dict(id="v_densa", nome="Chuva Densa", tipo="V", versao="chuva", exclui="chuva", efeitos={"chuva_densa": 1},
         texto="Chuva de Brasas: não causa dano; acende 2 camadas em cada inimigo.",
         nota="Acende 2 camadas de Queimadura em cada inimigo (sem dano)."),
    dict(id="v_partilhada", nome="Brasa Partilhada", tipo="V", versao="brasa", exclui="brasa",
         efeitos={"brasa_partilhada": 1},
         texto="Brasa: até o fim da próxima rodada, quando Morel ou Odette golpeia o alvo em chamas, ele ganha 1 "
               "camada.",
         nota="Causa 50% do Poder em dano de fogo e acende 1 camada. Até o fim da próxima rodada, os golpes de Morel e "
              "Odette nesse alvo em chamas acendem 1 camada."),
]


def _completar(nos, estrutura, spec):
    for n in nos:
        n.setdefault("ranks", 1)
        n.setdefault("afeta", [])
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
         frase="Entra em Fúria, aposta que o dano que vem é pequeno e se cura batendo; sai na hora certa, protegendo o "
               "grupo.",
         kit=["rugido", "sede", "redemoinho", "golpe_pesado", "erguer_escudo"],
         nos={"sangue_quente": 1, "braco": 1, "sangue_frio": 1, "ate_o_fim": 1}),
    dict(id="quebrador", nome="Quebrador", estrutura="t4", spec="berserker", estilo="responder e sustentar",
         frase="Interrompe golpes preparados e expõe inimigos; cada acerto desses dá Força ao próximo aliado. Provoca e "
               "revida.",
         kit=["golpe_pesado", "joelho", "quebra_guarda", "provocar", "erguer_escudo"],
         nos={"peso_golpe": 1, "couro": 2, "desequilibra": 1, "revide": 1}),
    dict(id="pavio", nome="Pavio", estrutura="t4", spec="piromante", estilo="construir e esperar",
         frase="Acumula camadas que não expiram, com Morel e Odette acendendo junto, e detona com o pavio.",
         kit=["brasa", "chuva", "combustao", "bola_fogo", "lanca"],
         nos={"paciente": 1, "partilhado": 1, "pavio": 1, "chama_viva": 2}),
    dict(id="fornalha", nome="Fornalha", estrutura="t4", spec="piromante", estilo="construir e arriscar",
         frase="Detona cedo e muitas vezes; quem morre em chamas explode, o Calor paga o próximo fogo e a vida paga o "
               "que falta.",
         kit=["brasa", "chuva", "combustao", "bola_fogo", "barreira"],
         nos={"fornalha": 1, "estouro": 1, "contagio": 1, "queimar": 1}),
    dict(id="choque", nome="Choque Térmico", estrutura="t4", spec="piromante", estilo="construir, híbrido",
         frase="Acende e congela: a Lança consome o fogo como gelo e congela mais.",
         kit=["brasa", "bola_fogo", "lanca", "chuva", "barreira"],
         nos={"paciente": 1, "partilhado": 1, "reserva": 1, "cinza_fria": 1}),
    dict(id="furia_t1", nome="Fúria (versões)", estrutura="t1", spec="berserker", estilo="arriscar",
         frase="A mesma ideia da Fúria com versões e um princípio.",
         kit=["rugido", "sede", "redemoinho", "golpe_pesado", "erguer_escudo"],
         nos={"p_sangue": 1, "v_contido": 1, "v_sede_rubra": 1, "v_temerario": 1, "v_espinhos": 1}),
    dict(id="quebrador_t1", nome="Quebrador (versões)", estrutura="t1", spec="berserker", estilo="responder e sustentar",
         frase="A mesma ideia do Quebrador com versões e um princípio.",
         kit=["golpe_pesado", "joelho", "quebra_guarda", "provocar", "erguer_escudo"],
         nos={"p_peso": 1, "v_desequilibra": 1, "v_aberto": 1, "v_espinhos": 1, "v_rancor": 1}),
    dict(id="pavio_t1", nome="Pavio (versões)", estrutura="t1", spec="piromante", estilo="construir e esperar",
         frase="A mesma ideia do Pavio com versões e um princípio.",
         kit=["brasa", "chuva", "combustao", "bola_fogo", "lanca"],
         nos={"p_paciencia": 1, "v_pavio": 1, "v_pesada": 1, "v_densa": 1, "v_termica": 1}),
    dict(id="fornalha_t1", nome="Fornalha (versões)", estrutura="t1", spec="piromante", estilo="construir e arriscar",
         frase="A mesma ideia da Fornalha com versões e um princípio.",
         kit=["brasa", "chuva", "combustao", "bola_fogo", "barreira"],
         nos={"p_voracidade": 1, "v_estrondosa": 1, "v_densa": 1, "v_pesada": 1, "v_partilhada": 1}),
]

# ---------------------------------------------------------------- os inimigos (famílias do jogo, simplificadas)
# poder: o golpe comum; magia: as habilidades de conjurador; habs: o que sorteiam (chance_hab por vez);
# res: multiplicador por tipo (acima de 1, fraqueza); tracos: "gigante" resiste a atordoar metade das vezes.
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
}
HABS_INIMIGO = {
    "mordida": "Mordida Sangrenta: 100% e 70% de chance de Sangramento (2 por turno, 3 turnos).",
    "uivo": "Uivo: os inimigos ficam Fortalecidos (+30%) por 2 vezes deles.",
    "grito": "Grito de Guerra: os inimigos ficam Fortalecidos (+30%) por 2 vezes deles.",
    "golpe_sujo": "Golpe Sujo: 110% e 35% de chance de Enfraquecer (−30%) por 2 vezes do alvo.",
    "esmagar": "Golpe Esmagador: prepara numa vez e golpeia com 220% na seguinte. Atordoar interrompe.",
    "regenerar": "Regenerar: com 70% da vida ou menos, recupera 15% da vida máxima.",
    "veneno": "Veneno: 80% e Veneno (2 por turno, 3 turnos).",
    "agarrar": "Agarrão: 80% e 40% de chance de prender (o alvo perde a próxima vez).",
    "maldicao": "Maldição: o alvo fica Enfraquecido (−30%) por 3 vezes dele.",
    "bola_fogo": "Bola de Fogo: 130% da magia em fogo.",
    "cura": "Cura: o inimigo mais ferido (abaixo de 60%) recupera 25% da vida máxima. Uma vez a cada 3 rodadas.",
}

ENCONTROS = {
    "lobos": {"nome": "Três lobos", "semente": 101, "inimigos": ["lobo", "lobo", "lobo"],
              "resumo": "Enxame sem golpe preparado; o uivo fortalece o bando.",
              "favorece": "Fúria, Pavio, Fornalha", "desfavorece": "Quebrador"},
    "mercenario": {"nome": "O mercenário e dois bandidos", "semente": 202,
                   "inimigos": ["mercenario", "bandido", "bandido"],
                   "resumo": "O mercenário prepara o Golpe Esmagador e grita ordens; os bandidos enfraquecem.",
                   "favorece": "Quebrador", "desfavorece": "Pavio (luta curta contra o mercenário)"},
    "bruxa": {"nome": "A bruxa, o bandido e o sapo", "semente": 303, "inimigos": ["bruxa", "bandido", "sapo"],
              "resumo": "A bruxa cura o mais ferido e enfraquece; o sapo envenena e prende.",
              "favorece": "Ninguém em especial", "desfavorece": "Fúria (preso na Fúria), Pavio (a cura desfaz o "
                                                                 "fogo lento)"},
    "troll": {"nome": "O troll sozinho", "semente": 404, "inimigos": ["troll"],
              "resumo": "Um gigante só: prepara o Golpe Esmagador, regenera e é fraco ao fogo (+40%).",
              "favorece": "Quebrador, fogo", "desfavorece": "Fornalha (ninguém morre para explodir), Fúria (o golpe "
                                                            "preparado na Fúria)"},
    "sorteado": {"nome": "Sorteado entre os comuns", "semente": 505, "sorteio": [
        ["lobo", "lobo"], ["rato", "rato", "rato", "rato"], ["bandido", "bandido"], ["sapo", "rato", "rato"],
        ["bandido", "lobo", "lobo"], ["mercenario", "rato", "rato"]],
                 "resumo": "Um grupo sorteado pela semente, para não haver só encontros escolhidos.",
                 "favorece": "—", "desfavorece": "—"},
}
