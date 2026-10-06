"""Eventos exclusivos de cada classe e especialização, incluindo a escolha do caminho no nível 4."""

from .. import texto as tx
from ..classes import SPECS
from ..itens import gerar_equip
from .motor import evento

TODOS = ("explorar", "viagem", "acampamento", "vila")


def _classe(c):
    return lambda g: g.j.classe == c


def _spec(s):
    return lambda g: g.j.spec == s


def _escolher_caminho(g, a, b, texto_a, texto_b):
    op = g.menu("Qual caminho você escolhe?", [
        (f"{SPECS[a]['nome']}: {texto_a}", a),
        (f"{SPECS[b]['nome']}: {texto_b}", b),
    ])
    g.especializar(op)
    return op


# ====================================================================== encruzilhadas (forçadas)
@evento(contextos=TODOS, peso=0)
def encruzilhada_guerreiro(g):
    g.narrar("Você chega a um templo em ruínas no alto de uma colina. Lá dentro, duas presenças.", "magenta")
    g.narrar("Ajoelhado diante de um altar partido, um cavaleiro de armadura gasta reza em voz baixa. A luz que "
             "entra pelo teto quebrado parece se curvar na direção dele.")
    g.narrar("Sentado sobre os escombros, um guerreiro coberto de tatuagens vermelhas afia um machado e ri "
             "sozinho. Os olhos dele brilham como brasas.")
    g.narrar("\"A espada precisa de um propósito\", diz o cavaleiro. \"Jure proteger os fracos, e a Luz "
             "lutará ao seu lado.\"", "amarelo")
    g.narrar("\"Propósito?\" O tatuado cospe. \"A dor é o propósito. Deixa a fúria entrar e nada mais vai "
             "te parar.\"", "vermelho")
    _escolher_caminho(g, "paladino", "berserker",
                      "o Oath of Light (cura, poder sagrado)",
                      "o Blood Pact (fúria, roubo de vida)")
    if g.j.spec == "paladino":
        g.narrar("Você se ajoelha ao lado do cavaleiro. Quando se levanta, ele não está mais lá — só a luz.")
    else:
        g.narrar("O tatuado corta a palma da mão e aperta a sua. Seu sangue ferve. Você ri sem saber por quê.")


@evento(contextos=TODOS, peso=0)
def encruzilhada_arqueiro(g):
    g.narrar("Um rastro de sangue leva a uma clareira. Uma velha patrulheira enfaixa a pata de um lobo "
             "ferido, cercada por um falcão e um urso que te observam sem medo.", "magenta")
    g.narrar("\"A mata escolhe os seus\", ela diz, sem olhar para você. \"E acho que escolheu você.\"", "verde")
    g.narrar("Uma flecha de penas negras se crava na árvore, a um palmo do seu rosto. Amarrado nela, "
             "um bilhete: \"Você atira bem. A Irmandade da Sombra paga melhor que a gratidão. "
             "Se quiser, apenas desapareça esta noite.\"", "cinza")
    _escolher_caminho(g, "patrulheiro", "sombra",
                      "seguir a velha patrulheira (companheiro animal, armadilhas)",
                      "desaparecer na noite (furtividade, venenos, execuções)")
    if g.j.spec == "sombra":
        g.narrar("Naquela noite, você some. Quando acorda, há uma capa negra dobrada ao lado do seu arco.")


@evento(contextos=TODOS, peso=0)
def encruzilhada_mago(g):
    g.narrar(f"{'Enquanto você dorme' if g.noite else 'Sem aviso'}, seu grimório começa a queimar sozinho. "
             "As páginas não viram cinza: viram palavras de "
             "fogo que flutuam no ar e sussurram promessas de calor e poder.", "magenta")
    g.narrar("Ao mesmo tempo, da terra sob seus pés, uma voz fria e paciente: \"O fogo consome. Eu "
             "preservo. Os mortos não esquecem quem lhes dá um propósito...\"", "cinza")
    _escolher_caminho(g, "piromante", "necromante",
                      "abraçar a Living Flame (fogo em área, combustão)",
                      "ouvir o Grave Whisper (drenar vida, servos, maldições)")
    if g.j.spec == "piromante":
        g.narrar("Você engole as palavras de fogo. Desde então, suas mãos nunca mais ficaram frias.")
    else:
        g.narrar("Você responde à voz. O grimório se apaga, e suas páginas agora são de pele fria e escura.")


# ====================================================================== guerreiro
@evento(peso=6, cooldown=14, cond=_classe("guerreiro"))
def duelo_de_honra(g):
    nome = tx.nome_proprio(g.rng)
    g.dizer(f"Um mercenário de armadura polida bloqueia a ponte. \"Sou {nome}, the Unbeaten. Dizem que você "
            f"luta bem. Duelo de honra: o perdedor paga {15 + 5 * g.j.nivel} ouro.\"", "amarelo")
    op = g.menu("O que faz?", [("Aceitar o duelo", "aceitar"), ("Recusar", "recusar")])
    if op == "recusar":
        g.dizer("\"Covarde!\" ele grita, e você ouve risadas atrás de você por um bom tempo.", "cinza")
        return
    e = g.inimigo("mercenario", afixo="feroz", nome_unico=nome)
    e.habilidades = ["esmagar", "golpe_sujo"]
    if g.combate([e], pode_fugir=False, titulo="DUELO DE HONRA") == "vitoria":
        g.dizer(f"{nome} se ajoelha. \"Você me venceu limpo. Quando precisar de uma espada, chame.\"", "verde")
        g.ganhar_ouro(15 + 5 * g.j.nivel)
        g.mudar_reputacao(3)
        g.aliado_final(nome, f"{nome}, the Unbeaten, aparece com seu escudo erguido: \"Eu disse que viria!\" "
                             f"Juntos, vocês abrem caminho.", "dano", 0.08)


@evento(peso=5, cooldown=20, cond=_classe("guerreiro"), max_vezes=2)
def veterano_cicatrizes(g):
    g.dizer("Um velho de uma perna só pesca à beira do rio. Ao ver sua espada, ele sorri sem dentes. "
            "\"Lutei na Primeira Fenda. Quer aprender algo que nenhum mestre ensina?\"", "amarelo")
    op = g.menu("O que faz?", [
        ("Treinar com ele a tarde toda", "treinar"),
        ("Ouvir as histórias dele", "ouvir"),
        ("Agradecer e seguir", "nao"),
    ])
    if op == "treinar":
        g.avancar_periodo()
        g.dizer("Ele te derruba onze vezes. Na décima segunda, você entende.", "verde")
        g.bonus_permanente("atk", 1)
        g.bonus_permanente("defesa", 1)
        g.j.recalcular()
    elif op == "ouvir":
        g.dizer(f"Ele fala sobre {g.antagonista['curto']} como quem fala de um velho conhecido.", "cinza")
        g.ganhar_xp(15 + 3 * g.j.nivel)


@evento(peso=6, cooldown=14, cond=lambda g: g.j.classe == "guerreiro" and g.j.equip["arma"] is not None)
def ferreiro_itinerante(g):
    arma = g.j.equip["arma"]
    preco = 20 + 6 * g.j.nivel
    g.dizer(f"Uma bigorna sobre rodas! O ferreiro olha sua {arma['nome']} e estala a língua. \"Isso aí tá "
            f"pedindo socorro. Deixa eu dar um jeito: {preco} ouro.\"", "amarelo")
    op = g.menu("O que faz?", [
        (f"Pagar ({preco} ouro)", "pagar") if g.j.ouro >= preco else None,
        ("Ajudar na forja em troca do serviço (Força)", "forjar"),
        ("Recusar", "nao"),
    ])
    if op == "nao":
        return
    if op == "pagar":
        g.perder_ouro(preco)
    elif not g.teste("forca", 13):
        g.dizer("Você martela torto e quase perde um dedo. O ferreiro desiste de você.", "vermelho")
        return
    arma["bonus"]["atk"] = arma["bonus"].get("atk", 0) + 2
    if "+" not in arma["nome"]:
        arma["nome"] += " +"
    g.j.recalcular()
    g.dizer(f"Sua arma volta afiada como nunca. (+2 Ataque na {arma['nome']})", "verde")


# --- paladino
@evento(peso=7, cooldown=14, cond=_spec("paladino"))
def aldeia_assombrada(g):
    g.dizer("Um vilarejo sem nenhuma luz acesa. Os moradores se trancam em casa: à noite, os mortos do "
            "cemitério andam pelas ruas.", "magenta")
    op = g.menu("O que faz?", [("Consagrar o cemitério e enfrentar os mortos", "consagrar"),
                               ("Seguir viagem", "nao")])
    if op == "nao":
        g.mudar_reputacao(-1)
        return
    grupo = g.grupo("esqueleto", n=2) + [g.inimigo("espectro")]
    if g.combate(grupo, titulo="A NOITE DOS MORTOS") == "vitoria":
        g.dizer("Você planta sua arma no centro do cemitério e reza até o amanhecer. Os mortos descansam.",
                "amarelo")
        g.mudar_reputacao(7)
        g.ganhar_xp(30)
        g.aliado_final("Os aldeões de Lumen", "Os aldeões que você libertou cantam um hino ao longe. A luz "
                                              "dele te envolve e fecha suas feridas.", "cura", 0)


@evento(peso=6, cooldown=14, cond=_spec("paladino"))
def os_enfermos(g):
    g.dizer("Uma casa com um X pintado na porta. Febre negra. Uma mãe implora: \"Ninguém entra. Ninguém "
            "nos ajuda.\"", "amarelo")
    op = g.menu("O que faz?", [("Entrar e curar os doentes (gasta suas forças)", "curar"),
                               ("Deixar remédios na porta", "remedio") if g.j.tem("pocao_vida") else None,
                               ("Seguir em frente", "nao")])
    if op == "curar":
        g.dizer("Você passa horas impondo as mãos. Quando termina, mal consegue ficar de pé — mas ninguém "
                "naquela casa vai morrer.", "amarelo")
        g.ferir(g.j.max_hp * 0.3, " de exaustão")
        g.bonus_permanente("poder", 2)
        g.j.recalcular()
        g.mudar_reputacao(8)
    elif op == "remedio":
        g.j.consumiveis["pocao_vida"] -= 1
        g.mudar_reputacao(3)


@evento(peso=5, cooldown=20, cond=_spec("paladino"), max_vezes=1)
def tentacao_do_juramento(g):
    g.dizer("Um nobre de luvas brancas te oferece uma bolsa pesada. \"Uma aldeia de camponeses está no "
            "caminho da minha nova estrada. Basta você... convencê-los a sair. Do jeito que for preciso.\"",
            "amarelo")
    op = g.menu("O que faz?", [("Recusar com desprezo", "recusar"), ("Aceitar o ouro", "aceitar"),
                               ("Prender o nobre", "prender")])
    if op == "aceitar":
        g.ganhar_ouro(80 + 10 * g.j.nivel)
        g.dizer("A Luz em você estremece. Algo se apaga.", "vermelho")
        g.j.base["poder"] -= 3
        g.j.recalcular()
        g.mudar_reputacao(-10)
    elif op == "prender":
        g.dizer("Os guardas do nobre sacam espadas.", "vermelho")
        if g.combate([g.inimigo("mercenario"), g.inimigo("mercenario")]) == "vitoria":
            g.mudar_reputacao(8)
            g.ganhar_ouro(30)
    else:
        g.dizer("\"Você vai se arrepender, santinho.\"", "cinza")
        g.mudar_reputacao(2)


# --- berserker
@evento(peso=7, cooldown=14, cond=_spec("berserker"))
def chamado_do_sangue(g):
    g.dizer("Um urso enorme bloqueia a trilha. Você sente o Pacto latejar nas veias: a fúria quer luta. "
            "De mãos nuas.", "vermelho+negrito")
    op = g.menu("O que faz?", [("Largar a arma e lutar de mãos nuas", "nuas"), ("Lutar normalmente", "normal"),
                               ("Resistir ao impulso (Vontade)", "resistir")])
    if op == "resistir":
        if g.teste("vontade", 14):
            g.dizer("Você respira fundo até o sangue esfriar. O urso vai embora.", "cinza")
            return
        g.dizer("A fúria vence. Você larga a arma.", "vermelho")
        op = "nuas"
    e = g.inimigo("javali", afixo="robusto")
    e.nome = "Urso das Cavernas"
    e.desc = "um urso das cavernas"
    if op == "nuas":
        arma = g.j.equip["arma"]
        g.j.equip["arma"] = None
        g.j.recalcular()
        r = g.combate([e], pode_fugir=False, titulo="FÚRIA DE MÃOS NUAS")
        g.j.equip["arma"] = arma
        g.j.recalcular()
        if r == "vitoria":
            g.dizer("Você ruge sobre o corpo do urso. O Pacto está satisfeito... e te recompensa.", "vermelho+negrito")
            g.bonus_permanente("atk", 2)
            g.bonus_permanente("max_hp", 5)
            g.j.recalcular()
    else:
        g.combate([e])


@evento(contextos=("acampamento",), peso=8, cooldown=12, cond=_spec("berserker"))
def furia_noturna(g):
    g.dizer("Você acorda com as mãos tremendo. Sonhou com sangue. A fúria quer sair — agora.", "vermelho")
    if g.teste("vontade", 13):
        g.dizer("Você medita até o amanhecer. Controle é uma forma de força.", "verde")
        g.bonus_permanente("defesa", 1)
        g.j.recalcular()
    else:
        g.dizer("Você destroça árvores com a arma até cair exausto.", "vermelho")
        g.ferir(g.j.max_hp * 0.15)
        if g.chance(0.5):
            g.dizer("O barulho atrai visitantes.", "vermelho")
            g.combate(g.grupo(n=1))


@evento(contextos=("vila", "viagem"), peso=6, cooldown=14, cond=_classe("guerreiro"))
def queda_de_braco(g):
    rival = g.npc()
    g.dizer(f"Numa mesa cercada de gente, {rival['um']} {rival['prof']} enorme {rival['traco']} desafia "
            f"qualquer um para uma queda de braço. Aposta: 20 ouro.", "amarelo")
    if g.j.ouro < 20 or not g.menu("Aceitar?", [("Sim", True), ("Não", False)]):
        return
    bonus = 2 if g.j.spec == "berserker" else 0
    if g.teste("forca", 14 - bonus):
        g.dizer("A mesa racha junto com o braço do adversário. A taverna explode em gritos.", "verde")
        g.ganhar_ouro(20)
        g.mudar_reputacao(2)
    else:
        g.dizer("Seu braço bate na mesa com um estalo humilhante.", "vermelho")
        g.perder_ouro(20)


# ====================================================================== arqueiro
@evento(peso=8, cooldown=10, cond=lambda g: g.j.classe == "arqueiro" and g.bioma in ("floresta", "planicie",
                                                                                       "montanha"))
def rastro_de_caca(g):
    presa = g.sortear(["um cervo de galhada imensa", "um javali gordo", "uma lebre branca", "um alce velho"])
    g.dizer(f"Pegadas frescas na terra úmida. Você reconhece: {presa}, há pouco tempo.", "verde")
    op = g.menu("O que faz?", [("Rastrear e caçar (Percepção)", "caçar"), ("Deixar para lá", "nao")])
    if op == "nao":
        return
    if g.teste("percepcao", 12):
        if g.j.flechas <= 0:
            g.dizer("Você encontra a presa... e lembra que está sem flechas.", "cinza")
            return
        g.dizer("Um tiro limpo. Você aproveita tudo: carne, couro, e tendões para cordas de arco.", "verde")
        g.j.flechas -= 1
        g.dar_provisoes(3)
        g.ganhar_ouro(5 + g.j.nivel)
        g.dar_flechas(g.rng.randint(3, 6))
        if g.chance(0.3) and g.j.equip["arma"]:
            g.j.equip["arma"]["bonus"]["agi"] = g.j.equip["arma"]["bonus"].get("agi", 0) + 1
            g.j.recalcular()
            g.dizer("Com os tendões você troca a corda do arco. Ele fica mais responsivo. (+1 Agilidade no arco)",
                    "verde")
    else:
        g.dizer("O rastro se perde num riacho.", "cinza")
        if g.chance(0.3):
            g.dizer("E algo estava rastreando VOCÊ.", "vermelho")
            g.combate(g.grupo("lobo"), emboscada="inimigo")


@evento(peso=lambda g: 14 if g.j.flechas < 15 else 5, cooldown=8, cond=_classe("arqueiro"))
def madeira_para_flechas(g):
    g.dizer("Um bosque de freixos jovens, retos como lanças. Madeira perfeita para flechas.", "verde")
    op = g.menu("O que faz?", [("Parar e fabricar flechas (leva tempo)", "fazer"), ("Seguir", "nao")])
    if op == "fazer":
        g.avancar_periodo()
        bonus = 4 if g.teste("percepcao", 11) else 0
        g.dizer("Você corta, alisa, empluma e afia até os dedos doerem.", "verde")
        g.dar_flechas(8 + bonus + g.rng.randint(0, 4))


@evento(peso=6, cooldown=20, cond=_classe("arqueiro"), max_vezes=2)
def falcao_mensageiro(g):
    g.dizer("Um falcão com um tubo de couro preso à pata cruza o céu, voando baixo. Uma mensagem.", "amarelo")
    op = g.menu("O que faz?", [
        ("Derrubá-lo com um tiro preciso (Percepção)", "atirar") if g.j.flechas > 0 else None,
        ("Assobiar e tentar atraí-lo (Patrulheiro)", "assobiar") if g.j.spec == "patrulheiro" else None,
        ("Deixá-lo seguir", "nao"),
    ])
    if op == "nao":
        return
    if op == "atirar":
        g.j.flechas -= 1
        ok = g.teste("percepcao", 14)
    else:
        ok = g.teste("percepcao", 10)
    if not ok:
        g.dizer("O falcão desvia e some entre as nuvens.", "cinza")
        return
    alvos = [l for l in g.mundo["locais"] if l["tipo"] in ("selvagem", "covil") and l["id"] != g.loc["id"]]
    alvo = g.sortear(alvos)
    g.dizer(f"A mensagem é de um cultista: \"O dízimo da Fenda está guardado em {alvo['nome']}. Que ninguém "
            f"o encontre.\"", "verde+negrito")
    g.rumores.append({"texto": f"Um tesouro cultista escondido em {alvo['nome']} (carta do falcão).",
                      "evento": "tesouro_escondido", "local": alvo["id"], "expira": g.dia + 8})
    g.impulsos["tesouro_escondido"] = 3
    g.ganhar_xp(10)


@evento(peso=7, cooldown=12, cond=lambda g: g.j.classe == "arqueiro" and g.clima in ("chuva", "tempestade", "neve"))
def corda_encharcada(g):
    g.dizer("A chuva encharcou a corda do seu arco. Ela está frouxa e ameaça arrebentar.", "vermelho")
    op = g.menu("O que faz?", [
        ("Parar e trocar a corda (Destreza)", "trocar"),
        ("Secar perto do corpo e seguir", "seguir"),
    ])
    if op == "trocar":
        if g.teste("destreza", 11):
            g.dizer("Corda nova, bem encerada. Pronto para o que vier.", "verde")
            g.ganhar_xp(5)
        else:
            g.dizer("A corda escapa e te acerta no rosto. Ai.", "vermelho")
            g.ferir(3)
    else:
        if g.chance(0.5):
            g.dizer("Na primeira tentativa de atirar no caminho, a corda estala. Você perde flechas e tempo.",
                    "vermelho")
            g.j.flechas = max(0, g.j.flechas - 3)
            g.avancar_periodo()
        else:
            g.dizer("Ela aguenta. Por pouco.", "cinza")


@evento(contextos=("vila",), peso=8, cooldown=12, cond=_classe("arqueiro"))
def competicao_de_tiro(g):
    g.dizer("Bandeirolas e uma multidão: competição de tiro com arco na praça! Inscrição: 10 ouro. "
            "Prêmio: 50 ouro e um arco de verdade.", "amarelo")
    if g.j.ouro < 10 or not g.menu("Participar?", [("Sim", True), ("Não", False)]):
        return
    g.perder_ouro(10)
    acertos = 0
    for alvo, cd in (("um alvo a cinquenta passos", 10), ("uma maçã na cabeça de um boneco", 13),
                     ("uma moeda jogada para o alto", 16)):
        g.dizer(f"Rodada: {alvo}.", "ciano")
        if g.teste("percepcao", cd):
            acertos += 1
        else:
            break
    if acertos == 3:
        g.dizer("A moeda cai partida ao meio. Silêncio. Depois, aplausos ensurdecedores!", "verde+negrito")
        g.ganhar_ouro(50)
        g.oferecer_equip(gerar_equip(g.rng, "arqueiro", g.j.nivel + 1, slot="arma", qualidade=1))
        g.mudar_reputacao(4)
    elif acertos == 2:
        g.dizer("Segundo lugar! Um prêmio de consolação.", "verde")
        g.ganhar_ouro(20)
    else:
        g.dizer("Você é eliminado cedo. Uma criança tira sarro.", "cinza")


# --- patrulheiro
@evento(peso=9, cooldown=10, cond=lambda g: g.j.spec == "patrulheiro" and g.j.companheiro
        and g.j.companheiro["hp"] > 0)
def companheiro_fareja(g):
    c = g.j.companheiro
    g.dizer(f"{c['nome']} para de repente, orelhas em pé, e dispara mato adentro.", "verde")
    sorte = g.rng.random()
    if sorte < 0.4:
        g.dizer("Você o encontra cavando sob uma raiz: um embrulho de couro enterrado há anos.", "verde")
        g.ganhar_ouro(15 + 4 * g.j.nivel)
        g.dar(g.sortear(["pocao_vida", "antidoto", "tonico"]))
    elif sorte < 0.7:
        g.dizer(f"{c['nome']} encurralou uma presa — que agora é sua refeição.", "verde")
        g.dar_provisoes(2)
    else:
        g.dizer(f"{c['nome']} rosna para o mato. Inimigos à espreita! Graças a ele, você os vê primeiro.",
                "amarelo")
        g.combate(g.grupo(), emboscada="jogador")


@evento(peso=5, cooldown=20, cond=_spec("patrulheiro"), max_vezes=1)
def circulo_dos_druidas(g):
    g.dizer("Pedras em círculo cobertas de musgo. Três druidas de túnicas verdes te esperam, como se "
            "soubessem que viria.", "verde")
    g.dizer("\"A patrulheira velha falou de você. A mata está doente com o Vazio. Aceite nossa marca, "
            "e você e seu companheiro serão mais fortes.\"", "verde")
    if g.menu("Aceitar a marca?", [("Sim", True), ("Não", False)]):
        c = g.j.companheiro
        if c:
            c["max_hp"] += 15
            c["atk"] += 3
            c["hp"] = c["max_hp"]
            g.dizer(f"{c['nome']} uiva para o céu. Seus olhos agora brilham verdes. (+15 vida, +3 ataque)", "verde")
        g.bonus_permanente("max_hp", 5)
        g.j.recalcular()
        g.aliado_final("Os druidas", "Raízes rompem o chão de obsidiana e prendem as pernas do inimigo — os "
                                     "druidas cumpriram a promessa.", "dano", 0.08)


# --- sombra
@evento(peso=7, cooldown=16, cond=_spec("sombra"), max_vezes=3)
def contrato_da_irmandade(g):
    alvo = g.npc()
    titulo = "Lorde" if alvo["g"] == "m" else "Lady"
    g.dizer(f"Uma flecha de penas negras com um bilhete: \"{titulo} {alvo['nome']} vende crianças para o culto "
            f"do Vazio. Está viajando pela estrada com escolta. Pagamento: 60 moedas.\"", "magenta")
    op = g.menu("O que faz?", [("Aceitar o contrato", "aceitar"), ("Queimar o bilhete", "nao")])
    if op == "nao":
        return
    g.dizer(f"Você espera escondido na beira da estrada. A carruagem de {titulo} {alvo['nome']} se aproxima, "
            f"com dois guardas.", "magenta")
    escolta = [g.inimigo("mercenario"), g.inimigo("cultista")]
    if g.combate(escolta, emboscada="jogador") != "vitoria":
        return
    g.dizer(f"{titulo} {alvo['nome']} cai de joelhos. \"Piedade! Eu pago o dobro! Eu te dou nomes, provas, "
            f"tudo!\"", "amarelo")
    op = g.menu("O alvo está à sua mercê.", [("Cumprir o contrato", "matar"), ("Poupar em troca de informação",
                                                                              "poupar")])
    if op == "matar":
        g.dizer("Silencioso, rápido. A Irmandade paga o que deve.", "magenta")
        g.ganhar_ouro(60 + 5 * g.j.nivel)
        g.bonus_permanente("agi", 1)
        g.j.recalcular()
        g.mudar_reputacao(-2)
    else:
        g.dizer(f"{alvo['nome']} entrega o nome de um cultista importante e foge. A Irmandade não vai gostar.",
                "amarelo")
        g.ganhar_xp(30)
        vivos = [l for l in g.mundo["locais"] if l["tipo"] == "covil" and not l["guardiao"]["derrotado"]]
        if vivos:
            l = g.sortear(vivos)
            g.marcar(f"fraqueza:guardiao:{l['id']}")
            g.marcar(f"conhecido:{l['id']}")
            g.dizer(f"Entre os documentos: o ponto fraco de {l['guardiao']['nome']}!", "verde+negrito")
        g.plantar("irmandade_cobra", 8)


@evento(peso=40, cooldown=4, cond=lambda g: g.semente("irmandade_cobra") and g.loc["tipo"] != "vila")
def irmandade_cobra(g):
    g.colher("irmandade_cobra")
    g.dizer("Três flechas de penas negras se cravam no chão à sua frente. \"A Irmandade não esquece "
            "contratos quebrados.\"", "magenta+negrito")
    grupo = [g.inimigo("bandido", afixo="agil"), g.inimigo("bandido", afixo="venenoso")]
    for e in grupo:
        e.nome = e.nome.replace("Bandido", "Assassino")
    g.combate(grupo, emboscada="inimigo" if not g.teste("percepcao", 13) else "jogador")


@evento(contextos=("vila",), peso=8, cooldown=10, cond=_spec("sombra"))
def bolsos_alheios(g):
    p = g.npc()
    g.dizer(f"No mercado lotado, {p['um']} {p['prof']} {p['traco']} carrega uma bolsa gorda e distraída.",
            "magenta")
    op = g.menu("O que faz?", [("Aliviar o peso da bolsa (Destreza)", "roubar"), ("Deixar quieto", "nao")])
    if op == "roubar":
        if g.teste("destreza", 12):
            g.ganhar_ouro(15 + 3 * g.j.nivel)
            g.mudar_reputacao(-1)
        else:
            g.dizer("\"PEGA LADRÃO!\" Você precisa sair correndo da vila.", "vermelho")
            g.mudar_reputacao(-6)
            g.perder_ouro(10)


# ====================================================================== mago
@evento(peso=7, cooldown=12, cond=_classe("mago"))
def anomalia_arcana(g):
    g.dizer("O ar crepita. Folhas flutuam para cima, a gravidade parece indecisa, e sua mana vibra como "
            "uma corda tocada. Uma anomalia arcana!", "azul")
    op = g.menu("O que faz?", [("Absorver a energia (arriscado)", "absorver"),
                               ("Estabilizar a anomalia (Arcano)", "estabilizar"), ("Afastar-se", "nao")])
    if op == "nao":
        return
    if op == "estabilizar":
        if g.teste("arcano", 13):
            g.dizer("Você fecha a ruptura com um gesto preciso. Aprende muito com isso.", "verde")
            g.ganhar_xp(20 + 5 * g.j.nivel)
            g.mudar_reputacao(1)
        else:
            g.dizer("A anomalia explode na sua cara.", "vermelho")
            g.ferir(g.j.max_hp * 0.2)
        return
    resultado = g.sortear(["mana", "poder", "explosao", "teleporte", "elemental"])
    if resultado == "mana":
        g.bonus_permanente("max_rec", 8)
        g.j.recalcular()
        g.dizer("A energia se assenta em você. (+8 Mana máxima)", "azul")
    elif resultado == "poder":
        g.bonus_permanente("poder", 2)
        g.j.recalcular()
        g.dizer("Seus dedos soltam faíscas por horas. (+2 Poder)", "azul")
    elif resultado == "explosao":
        g.dizer("A energia te rejeita com violência.", "vermelho")
        g.ferir(g.j.max_hp * 0.3)
    elif resultado == "teleporte":
        destino = g.sortear([l for l in g.mundo["locais"] if l["tipo"] != "cidadela"])
        g.dizer(f"Um clarão... e você está em {destino['nome']}!", "magenta+negrito")
        g.mundo["atual"] = destino["id"]
        destino["visitado"] = True
    else:
        g.dizer("A energia toma forma: um elemental arcano instável!", "vermelho")
        e = g.inimigo("espectro", afixo="flamejante")
        e.nome = "Elemental Arcano"
        e.desc = "um elemental arcano"
        e.tracos = ["etereo"]
        g.combate([e])


@evento(peso=6, cooldown=20, cond=_classe("mago"), max_vezes=2)
def grimorio_perdido(g):
    g.dizer("Preso nas raízes de uma árvore, um grimório encadernado em couro escuro. Ele está quente. "
            "E bate, devagar, como um coração.", "magenta")
    op = g.menu("O que faz?", [("Ler (Arcano)", "ler"), ("Queimar o livro", "queimar"), ("Deixar onde está", "nao")])
    if op == "ler":
        if g.teste("arcano", 14):
            g.dizer("Páginas de teoria proibida — e você entende cada palavra.", "verde")
            g.bonus_permanente("poder", 3)
            g.j.recalcular()
        else:
            g.dizer("As letras se mexem, entram pelos seus olhos. Você grita.", "vermelho")
            g.ferir(g.j.max_hp * 0.25)
            g.corromper(2)
    elif op == "queimar":
        g.dizer("O livro guincha ao queimar. A corrupção ao redor parece recuar um pouco.", "verde")
        g.corromper(-2)
        g.ganhar_xp(10)


@evento(peso=6, cooldown=14, cond=_classe("mago"))
def linha_ley(g):
    g.dizer("Você sente uma linha de energia correndo sob a terra, como um rio invisível. Uma linha ley!",
            "azul")
    op = g.menu("O que faz?", [("Meditar sobre ela (passa o tempo)", "meditar"), ("Seguir", "nao")])
    if op == "meditar":
        g.avancar_periodo()
        g.j.rec = g.j.max_rec
        g.bonus_permanente("max_rec", 4)
        g.j.recalcular()
        g.curar(g.j.max_hp * 0.15)
        g.dizer("Sua mana transborda. (+4 Mana máxima, mana restaurada)", "azul")


@evento(peso=6, cooldown=14, cond=_classe("mago"))
def aprendiz_em_apuros(g):
    p = g.npc()
    g.dizer(f"Um estrondo e fumaça roxa. {p['um'].capitalize()} jovem aprendiz sai correndo de um celeiro: "
            f"\"Eu só queria invocar um gato! UM GATO!\"", "amarelo")
    op = g.menu("O que faz?", [("Entrar e lidar com a invocação", "entrar"),
                               ("Ensinar o aprendiz a desfazer o feitiço (Arcano)", "ensinar")])
    if op == "ensinar" and g.teste("arcano", 12):
        g.dizer("Vocês desfazem o feitiço juntos. O aprendiz te olha como se você fosse uma lenda.", "verde")
        g.mudar_reputacao(3)
        g.ganhar_xp(20)
        g.plantar("aprendiz_grato", 10, nome=p["nome"])
        return
    e = g.inimigo("cria_vazio")
    e.nome = "Gato do Vazio"
    e.desc = "um gato do Vazio"
    if g.combate([e]) == "vitoria":
        g.mudar_reputacao(2)
        g.plantar("aprendiz_grato", 10, nome=p["nome"])


@evento(peso=40, cooldown=3, cond=lambda g: g.semente("aprendiz_grato"))
def aprendiz_grato(g):
    d = g.colher("aprendiz_grato")
    g.dizer(f"\"Mestre!\" É {d['nome']}, o aprendiz do celeiro — agora com túnica nova e olhar confiante. "
            f"\"Estudei dia e noite. Quero lutar ao seu lado no fim.\"", "verde")
    g.dar("tonico", 2)
    g.aliado_final(d["nome"], f"{d['nome']}, seu aprendiz, ergue uma barreira que absorve a primeira onda de "
                              f"sombras e lança um raio impressionante.", "dano", 0.07)


@evento(peso=lambda g: 5 + max(0, -g.j.reputacao) // 5, cooldown=16, cond=_classe("mago"))
def cacadores_de_bruxas(g):
    g.dizer("Homens com chapéus de abas largas e tochas: caçadores de bruxas. \"Você aí, de mãos "
            "manchadas de magia. Vai ter que nos acompanhar.\"", "vermelho")
    op = g.menu("O que faz?", [("Convencê-los de que você luta contra o Vazio (Carisma)", "falar"),
                               ("Mostrar o que um mago de verdade pode fazer", "lutar"),
                               ("Fugir (Destreza)", "fugir")])
    if op == "falar" and g.teste("carisma", 13):
        g.dizer("Eles se entreolham. \"Se você mente, a fogueira espera.\" E vão embora.", "verde")
        return
    if op == "fugir" and g.teste("destreza", 12):
        g.dizer("Você some entre as árvores antes que as tochas se aproximem.", "verde")
        return
    grupo = [g.inimigo("mercenario"), g.inimigo("bandido")]
    for e in grupo:
        e.nome = "Caçador de Bruxas"
        e.resist = {"fogo": 0.7, "sombra": 0.7, "arcano": 0.8}
    g.combate(grupo)


# --- piromante
@evento(peso=7, cooldown=14, cond=_spec("piromante"))
def elemental_selvagem(g):
    g.dizer("Uma coluna de fogo dança sozinha no meio da trilha: um elemental de fogo selvagem. Ele "
            "parece... curioso a seu respeito.", "vermelho")
    op = g.menu("O que faz?", [("Tentar absorvê-lo (Vontade)", "absorver"), ("Destruí-lo", "lutar"),
                               ("Deixá-lo seguir", "nao")])
    if op == "absorver":
        if g.teste("vontade", 13):
            g.dizer("O elemental se enrosca em seu braço como uma serpente e some sob a pele. Você queima por "
                    "dentro — de um jeito bom.", "verde")
            g.bonus_permanente("poder", 2)
            g.bonus_permanente("max_hp", 4)
            g.j.recalcular()
        else:
            g.ferir(g.j.max_hp * 0.25, " em queimaduras")
    elif op == "lutar":
        e = g.inimigo("espectro", afixo="flamejante")
        e.nome = "Elemental de Fogo"
        e.desc = "um elemental de fogo"
        e.tracos = ["etereo"]
        g.combate([e])


@evento(peso=6, cooldown=20, cond=lambda g: g.j.spec == "piromante" and g.bioma in ("floresta", "planicie"))
def incendio(g):
    g.dizer("Fumaça no horizonte. Um incêndio avança pela mata em direção a uma vila de lenhadores.", "vermelho")
    op = g.menu("O que faz?", [("Dominar as chamas com sua magia (Arcano)", "dominar"),
                               ("Ajudar a evacuar a vila", "evacuar"), ("Isso não é problema seu", "nao")])
    if op == "dominar":
        if g.teste("arcano", 14):
            g.dizer("Você abre os braços e as chamas se curvam para você, obedientes. O fogo morre.", "verde+negrito")
            g.mudar_reputacao(8)
            g.ganhar_xp(30)
        else:
            g.dizer("O fogo não te obedece hoje. Você sai chamuscado e a vila perde metade das casas.", "vermelho")
            g.ferir(g.j.max_hp * 0.2)
            g.mudar_reputacao(-3)
    elif op == "evacuar":
        g.avancar_periodo()
        g.mudar_reputacao(4)
        g.ganhar_xp(15)
    else:
        g.dizer("Dizem que um mago de fogo assistiu tudo sem fazer nada. Histórias assim correm rápido.", "cinza")
        g.mudar_reputacao(-5)


# --- necromante
@evento(peso=7, cooldown=14, cond=_spec("necromante"))
def cemiterio_antigo(g):
    g.dizer("Um cemitério esquecido, lápides tortas e nomes apagados. Você ouve os mortos murmurando, "
            "entediados.", "magenta")
    op = g.menu("O que faz?", [("Recrutar os mortos para a batalha final", "recrutar"),
                               ("Aprender os segredos que eles guardam", "aprender"),
                               ("Deixá-los descansar", "nao")])
    if op == "recrutar":
        g.dizer("Uma dezena de mãos ossudas rompe a terra. \"Quando você chamar, viremos.\"", "magenta")
        g.mudar_reputacao(-3)
        g.aliado_final("A legião do cemitério", "A terra treme e dezenas de mortos marcham contra as sombras, "
                                                "obedecendo a você.", "dano", 0.1)
    elif op == "aprender":
        if g.teste("arcano", 13):
            g.dizer("Os mortos falam de magias perdidas.", "verde")
            g.bonus_permanente("poder", 2)
            g.j.recalcular()
        else:
            g.dizer("Os mortos não gostam de perguntas.", "vermelho")
            g.combate(g.grupo("esqueleto", n=2))
    else:
        g.mudar_reputacao(1)


@evento(contextos=("vila",), peso=8, cooldown=12, cond=_spec("necromante"))
def aldeoes_temerosos(g):
    g.dizer("Ao te ver, uma mãe puxa os filhos para dentro. Alguém risca um sinal de proteção na porta. "
            "O cheiro de túmulo te acompanha, e eles sabem.", "magenta")
    op = g.menu("O que faz?", [
        ("Ajudar publicamente nas tarefas da vila para ganhar confiança", "ajudar"),
        ("Usar o medo deles a seu favor (Carisma)", "assustar"),
        ("Ignorar", "nao"),
    ])
    if op == "ajudar":
        g.avancar_periodo()
        g.dizer("Você carrega lenha, conserta um telhado, cura uma vaca doente. Os olhares mudam, um pouco.",
                "verde")
        g.mudar_reputacao(4)
    elif op == "assustar":
        if g.teste("carisma", 10):
            g.dizer("Uma palavra sussurrada e o comerciante te dá tudo pela metade do preço.", "magenta")
            g.dar("pocao_vida")
            g.dar("tonico")
        g.mudar_reputacao(-4)
