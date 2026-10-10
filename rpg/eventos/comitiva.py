"""Eventos da comitiva: encontros que trazem companheiros, conversas ao pé do fogo,
missões pessoais em três atos e as brigas entre quem caminha com você."""

from .. import caspar
from .. import comitiva as cm
from ..comitiva import conversa
from .motor import evento


def _vivos_covis(g):
    return [l for l in g.mundo["locais"] if l["tipo"] == "covil" and not l["guardiao"]["derrotado"]]


# ====================================================================== ODETE
@evento(contextos=("explorar", "viagem"), peso=lambda g: 16 if g.dia <= 8 else 6, cooldown=0, unico=True,
        cond=lambda g: g.dia >= 2 and cm.disponivel(g, "odete") and g.loc["tipo"] != "cidadela")
def odete_na_estrada(g):
    g.dizer("À beira da estrada, uma mulher de hábito chamuscado está ajoelhada ao lado de um homem com a barriga "
            "aberta. Ela aperta a ferida com as próprias mãos. Não tem bandagens. Não tem mais nada.")
    g.dizer("\"Segure aqui\", ela diz, sem olhar para você, como se você sempre tivesse estado ali.", "amarelo")
    op = g.menu("O que faz?", [
        ("Estancar o sangue com uma bandagem", "bandagem") if g.j.tem("bandagem") else None,
        ("Segurar a ferida enquanto ela reza (Vontade)", "segurar"),
        ("Perguntar quem ela é", "perguntar"),
        ("Revistar o moribundo enquanto ela está distraída", "roubar"),
        ("Seguir seu caminho", "nao"),
    ])
    simpatia = 0
    if op == "bandagem":
        g.j.consumiveis["bandagem"] -= 1
        g.dizer("Vocês trabalham juntos, rápido, sem uma palavra. O sangue para. O homem abre os olhos e pergunta "
                "pela mãe.", "verde")
        g.mudar_reputacao(2)
        simpatia = 12
    elif op == "segurar":
        if g.teste("vontade", 12):
            g.dizer("Você segura firme. Ela reza baixo, rápido, como quem já rezou demais. Quando termina, o homem "
                    "respira. Fraco, mas respira.", "verde")
            g.mudar_reputacao(2)
            simpatia = 10
        else:
            g.dizer("Você segura até as mãos ficarem dormentes. Não adianta. Ela fecha os olhos dele com dois dedos "
                    "e fica um tempo ali, parada.", "cinza")
            simpatia = 5
    elif op == "perguntar":
        g.dizer("\"Odette. Irmã Odette.\" Ela não tira as mãos da ferida. \"Ele já está morto, sabia? Só não percebeu "
                "ainda.\" Ele percebe pouco depois.", "cinza")
        simpatia = 0
    elif op == "roubar":
        g.dizer("Você encontra três moedas e um dente de ouro. Odette se levanta, com sangue até os cotovelos, e te "
                "encara até você ir embora.", "vermelho")
        g.ganhar_ouro(4)
        g.mudar_reputacao(-3)
        cm.reagir(g, "crueldade", "ganancia")
        g.marcar("comitiva:odete", "recusou")
        return
    else:
        g.dizer("Você segue. Atrás de você, uma voz de mulher começa a rezar.", "cinza")
        g.marcar("comitiva:odete", "recusou")
        return
    cm.reagir(g, "misericordia")
    g.dizer("Ela limpa as mãos na terra. \"Você vai para onde está a dor. Dá para ver. Eu também.\" Pela primeira "
            "vez ela olha para você. \"Alguém vai precisar fechar suas feridas no caminho.\"", "amarelo")
    if cm.oferecer_vaga(g, "odete"):
        cm.mudar_aprovacao(g, "odete", simpatia, mostrar=False)
    else:
        g.dizer("Odette assente, como se esperasse isso, e segue para o outro lado.", "cinza")
        g.marcar("comitiva:odete", "recusou")


@conversa("odete", 0, dias=1)
def odete_conversa_habito(g, m):
    g.dizer("Você pergunta pelo hábito chamuscado. Odette demora a responder.")
    g.dizer("\"Chamuscado, não queimado. Tem diferença. Queimado é quem ficou.\"", "amarelo")
    op = g.menu("O que diz?", [
        ("\"Não precisa me contar nada.\"", "respeito"),
        ("\"Quem ficou?\"", "insistir"),
        ("\"Desertora, então.\"", "acusar"),
    ])
    if op == "respeito":
        g.dizer("Ela solta o ar devagar. \"Obrigada. Um dia eu conto. Não hoje.\"", "verde")
        cm.mudar_aprovacao(g, "odete", 5)
    elif op == "insistir":
        g.dizer("\"Quarenta acólitos\", diz ela, olhando o fogo. \"E a irmã de vigília daquela noite era eu.\" "
                "Ela se deita de costas para você e não diz mais nada.", "cinza")
        cm.mudar_aprovacao(g, "odete", 1)
    else:
        g.dizer("\"Sim\", diz Odette, sem se ofender. \"É exatamente o que eu sou.\" O silêncio depois é pior que "
                "qualquer resposta.", "cinza")
        cm.mudar_aprovacao(g, "odete", -5)


@conversa("odete", 1, dias=3, aprov=10)
def odete_conversa_confissao(g, m):
    g.dizer("Odette fala sem que você pergunte, com a voz de quem ensaiou muitas vezes e mesmo assim não está pronta.")
    g.narrar("\"Naquela noite eu ouvi a voz primeiro. Antes do chão abrir, antes dos gritos. Ela disse o meu nome. "
             "E eu corri. Tranquei a porta da cripta por fora, para que a coisa não me seguisse.\"", "amarelo")
    g.narrar("\"Os acólitos estavam lá dentro.\"", "amarelo+negrito")
    op = g.menu("O que diz?", [
        ("\"Você não tinha como saber o que estava acontecendo.\"", "consolar"),
        ("\"Você trancou quarenta pessoas para morrer.\"", "verdade"),
        ("\"E o que você quer fazer com isso agora?\"", "agora"),
    ])
    if op == "consolar":
        g.dizer("\"Todo mundo diz isso\", Odette sussurra. \"É o que eu digo também. Não ajuda, mas obrigada.\"", "verde")
        cm.mudar_aprovacao(g, "odete", 6)
    elif op == "verdade":
        g.dizer("Ela fica muito tempo calada. \"Sim. Ninguém nunca tinha dito em voz alta.\" E então, estranhamente, "
                "ela parece mais leve.", "cinza")
        cm.mudar_aprovacao(g, "odete", 2)
    else:
        g.dizer("\"Olhar nos olhos de alguém\", diz ela. \"Só isso. E não desviar.\"", "verde")
        cm.mudar_aprovacao(g, "odete", 4)
    g.dizer("\"As famílias deles ainda acham que morreram como mártires. Há uma mãe, a mãe de Thomas, que acende "
            "uma vela todo dia pelo filho. Um dia eu vou ter que encarar essa mulher.\"", "amarelo")
    m["missao"] = 1
    g.dizer("(Odette procura a mãe de Thomas. Talvez você a encontre em alguma vila.)", "ciano")


@evento(contextos=("vila",), peso=40, cooldown=0, unico=True,
        cond=lambda g: cm.presente(g, "odete") and cm.membro(g, "odete")["missao"] == 1)
def odete_a_mae(g):
    m = cm.membro(g, "odete")
    g.dizer("Na praça, uma velha acende uma vela diante de um retrato desbotado de um rapaz de hábito. Odette para, "
            "como se tivesse batido numa parede.")
    g.dizer("\"É ela\", sussurra. \"A mãe de Thomas.\"", "amarelo")
    op = g.menu("O que você diz a Odette?", [
        ("\"Vá. Conte a verdade. Eu fico ao seu lado.\" (Carisma)", "verdade"),
        ("\"Diga que ele morreu como herói. Ela merece paz.\"", "mentira"),
        ("\"Isso é entre vocês duas.\"", "sozinha"),
    ])
    if op == "mentira" and m["aprovacao"] < 45:
        g.dizer("Odette balança a cabeça. \"Não. Já menti calando por tempo demais.\" Ela vai sem você.", "cinza")
        cm.mudar_aprovacao(g, "odete", -4)
        op = "sozinha"
    if op == "mentira":
        g.narrar("Odette hesita, olha para você, e faz o que você disse. \"Ele morreu protegendo os outros\", diz. A velha "
                 "chora de orgulho. Odette sorri para ela. Você nunca viu um sorriso tão triste.", "cinza")
        cm.mudar_aprovacao(g, "odete", -6)
        m["caminho"] = "calada"
    else:
        apoio = op == "verdade"
        ok = g.teste("carisma", 13) if apoio else g.chance(0.5)
        g.narrar("Odette se ajoelha diante da velha e conta tudo. A voz, a porta, a chave. A velha escuta até o fim.",
                 "amarelo")
        if ok:
            g.narrar("Depois, levanta a mão e dá um tapa no rosto de Odette. E então a abraça, e as duas choram juntas "
                     "na praça. \"Pelo menos agora eu sei\", diz a mãe de Thomas.", "verde")
        else:
            g.narrar("Depois, grita. Grita até juntar gente. Alguém cospe em Odette. Ela não se defende.", "vermelho")
            g.mudar_reputacao(-2)
        cm.mudar_aprovacao(g, "odete", 15 if apoio else (8 if ok else 5))
        m["caminho"] = "penitente"
    m["missao"] = 3


@conversa("odete", 2, dias=4, aprov=40, cond=lambda g, m: m["missao"] == 3)
def odete_conversa_final(g, m):
    if m["caminho"] == "penitente":
        g.dizer("\"Ontem eu dormi a noite inteira\", diz Odette, espantada consigo mesma. \"A primeira vez desde a "
                "Fenda.\" Ela tira o rosário do pescoço e põe na sua mão.")
        g.dizer("\"Quando você for até ele, eu vou estar lá. E dessa vez a minha prece não vai tremer.\"", "amarelo")
        cm.mudar_aprovacao(g, "odete", 5)
    else:
        g.dizer("\"Ela ainda acende a vela todo dia\", diz Odette. \"Por uma mentira minha. Pelo menos ela dorme.\" "
                "Odette não diz se ela mesma dorme.", "cinza")
        cm.mudar_aprovacao(g, "odete", 2)


# ====================================================================== MOREL
@evento(contextos=("taverna",), peso=lambda g: 18 if g.dia <= 10 else 7, cooldown=4, max_vezes=3,
        cond=lambda g: g.dia >= 2 and cm.disponivel(g, "morel"))  # no canto da taverna: quem bebe ali o encontra
def morel_na_taverna(g):
    g.dizer("No canto da taverna, um homem grande come sozinho, de costas para a parede. Cicatriz de orelha a orelha, "
            "armadura remendada com pedaços de outras armaduras. Ele fala sem levantar os olhos do prato.")
    g.dizer("\"Você tem cara de quem vai morrer na estrada. Eu tenho cara de quem impede isso. Quarenta moedas e a "
            "minha espada é sua. Bastian Morel, ex-capitão dos Cães de Ferro.\"", "amarelo")
    op = g.menu("O que faz?", [
        ("Pagar 40 ouro", "pagar") if g.j.ouro >= 40 else None,
        ("\"Queda de braço. Se eu ganhar, você vem de graça.\" (Força)", "braco"),
        ("\"Não tenho ouro. Tenho uma causa: o Vazio.\" (Carisma)", "causa"),
        ("Recusar", "nao"),
    ])
    if op == "nao":
        g.dizer("Morel dá de ombros e volta ao ensopado. \"Volta quando estiver sangrando.\"", "cinza")
        return
    simpatia = 0
    if op == "pagar":
        g.perder_ouro(40)
        g.dizer("Ele conta as moedas duas vezes. \"Negócio fechado. Eu seguro a linha; você não morre. Simples.\"",
                "verde")
        simpatia = 4
    elif op == "braco":
        g.dizer("A taverna inteira para para ver. A mesa range.", "amarelo")
        if g.teste("forca", 14):
            g.dizer("O braço dele bate na mesa. O silêncio dura um segundo; depois Morel gargalha até tossir. "
                    "\"Faz dez anos que ninguém me derruba. Tá bom. De graça. Desta vez.\"", "verde")
            simpatia = 12
        else:
            g.dizer("Seu braço bate na mesa com um estalo. Morel nem suou. \"Pelo espetáculo, faço por vinte e "
                    "cinco.\"", "vermelho")
            if g.j.ouro >= 25 and g.menu("Pagar 25?", [("Pagar 25 ouro", "sim"), ("Recusar", "nao")]) == "sim":
                g.perder_ouro(25)
                simpatia = 2
            else:
                return
    else:
        if g.teste("carisma", 15):
            g.dizer("Morel ri pelo nariz. \"Causa. Eu já tive uma.\" Ele limpa a boca na manga e se levanta. \"Vou "
                    "cobrar soldo toda semana. E se você fugir de uma luta, eu fujo de você.\"", "verde")
            simpatia = 2
        else:
            g.dizer("\"Causa não compra pão\", diz Morel, e volta a comer.", "cinza")
            return
    if cm.oferecer_vaga(g, "morel"):
        cm.mudar_aprovacao(g, "morel", simpatia, mostrar=False)


@conversa("morel", 0, dias=1)
def morel_conversa_caes(g, m):
    g.dizer("Morel afia a espada. \"Os Cães de Ferro. Duzentos homens. A melhor companhia do reino. Ganhamos a "
            "a Batalha dos Vaus por um saco de prata e uma barrica de vinho.\"")
    op = g.menu("O que diz?", [
        ("\"E onde estão agora?\"", "onde"),
        ("\"Quanto vocês cobravam?\"", "preco"),
        ("\"Mercenário é só ladrão com contrato.\"", "ladrao"),
    ])
    if op == "onde":
        g.dizer("\"Mortos, quase todos. O resto, pior.\" Ele testa o fio no polegar. Sangra um pouco. Não liga.", "cinza")
        cm.mudar_aprovacao(g, "morel", 2)
    elif op == "preco":
        g.dizer("Morel gargalha. \"Finalmente uma pergunta inteligente!\" E passa a noite contando quanto cobraram de "
                "cada duque, conde e bispo do reino. Muito.", "verde")
        cm.mudar_aprovacao(g, "morel", 5)
    else:
        g.dizer("\"Ladrão com contrato tem palavra\", diz Morel. \"Ladrão sem contrato tem só fome.\" Ele não fala "
                "mais com você naquela noite.", "cinza")
        cm.mudar_aprovacao(g, "morel", -5)


@conversa("morel", 1, dias=3, aprov=10)
def morel_conversa_ponte(g, m):
    g.dizer("Morel bebe mais do que costuma. Depois de um tempo, fala, olhando para o fogo.")
    g.narrar("\"A Ponte de Varn. O duque mandou segurar a passagem contra as crias do Vazio até a coluna dele "
             "passar. A coluna nunca veio. Ao amanhecer eu tinha quarenta homens e uma escolha.\"", "amarelo")
    g.narrar("\"Mandei recuar. Eu, o capitão. Saímos eu e mais seis. Meu tenente, Theodore, o Ruivo, ficou na ponte com "
             "o resto, gritando o meu nome. Dizem que sobreviveu. Dizem que me procura.\"", "amarelo")
    op = g.menu("O que diz?", [
        ("\"Você salvou seis homens. Ficar seria morrer junto.\"", "salvou"),
        ("\"Você abandonou seus homens.\"", "abandonou"),
        ("\"Se Theodore aparecer, você vai fugir de novo?\"", "fugir"),
    ])
    if op == "salvou":
        g.dizer("\"É o que eu digo pra mim\", Morel resmunga. \"Às vezes funciona.\"", "verde")
        cm.mudar_aprovacao(g, "morel", 6)
    elif op == "abandonou":
        g.dizer("Morel te encara por um bom tempo. \"Fala isso de novo e eu quebro o seu nariz.\" Pausa. \"Mas é.\"",
                "cinza")
        cm.mudar_aprovacao(g, "morel", -3)
    else:
        g.dizer("\"Não\", diz Morel, rápido demais. Depois, mais devagar: \"Não. Dessa vez eu fico.\"", "verde")
        cm.mudar_aprovacao(g, "morel", 4)
    m["missao"] = 1
    g.plantar("teodoro_ruivo", 3)


# Theodore e os desertores lutam como um grupo de elite: antes do nível 5, nem jogando bem dava (a semente espera).
@evento(contextos=("explorar", "viagem"), peso=40, cooldown=0, unico=True,
        cond=lambda g: cm.presente(g, "morel") and cm.membro(g, "morel")["missao"] == 1 and g.semente("teodoro_ruivo")
        and g.j.nivel >= 5)
def teodoro_ruivo(g):
    g.colher("teodoro_ruivo")
    m = cm.membro(g, "morel")
    g.dizer("Um assobio de três notas: o toque dos Cães de Ferro. Da mata saem seis homens com tabardos desbotados. "
            "O da frente tem metade do rosto queimada e um cabelo que um dia foi ruivo.")
    g.dizer("\"Capitão\", diz Theodore, e a palavra sai como cuspe. \"Procurei você por dois invernos.\" Ele olha para "
            "você. \"Isso não é com você, estranho. Entrega o covarde e vai embora com a bolsa cheia.\"", "vermelho")
    g.dizer("Morel põe a mão no punho da espada. Não olha para você.", "cinza")
    op = g.menu("O que faz?", [
        ("Entregar Morel (Theodore paga 80 ouro)", "entregar"),
        ("Desembainhar e lutar ao lado de Morel", "lutar"),
        ("\"Que os dois resolvam isso num duelo.\"", "duelo"),
        ("\"O inimigo é o Vazio, não ele. Depois vocês acertam as contas.\" (Carisma)", "convencer"),
    ])
    if op == "entregar":
        g.narrar("Morel solta a espada devagar. \"Justo\", diz, sem raiva nenhuma, e caminha até eles. Ninguém olha "
                 "para trás. Nem ele.", "cinza")
        cm.sair(g, "morel", "entregue")
        g.ganhar_ouro(107)  # ganhar_ouro desconta 25%: chegam 80
        cm.reagir(g, "crueldade", "ganancia")
        return
    if op == "convencer":
        if g.teste("carisma", 15):
            g.dizer("Theodore fica muito tempo calado. \"Depois que isso acabar, capitão. Depois.\" E então, mais baixo: "
                    "\"Os Cães ainda sabem lutar. Se você for mesmo contra a sombra, mande chamar.\"", "verde")
            m["caminho"] = "adiado"
            cm.mudar_aprovacao(g, "morel", 6)
            m["missao"] = 3
            return
        g.dizer("\"Bonito discurso\", diz Theodore, e saca a espada.", "vermelho")
        op = "lutar"
    if op == "duelo":
        g.narrar("Os homens de Theodore abrem uma roda. Os dois velhos camaradas se medem em silêncio, e então o aço "
                 "canta.", "amarelo")
        chance = 0.5 + m["aprovacao"] / 200
        if g.chance(chance):
            g.narrar("Morel desarma Theodore com um golpe que você nem vê direito. A ponta da espada para na garganta "
                     "do tenente.", "verde")
            op2 = g.menu("Morel olha para você.", [
                ("\"Poupe ele.\"", "poupar"),
                ("Não dizer nada. A decisão é dele.", "decidir"),
            ])
            if op2 == "poupar" and m["aprovacao"] >= 30:
                g.narrar("Morel abaixa a espada. \"Alguém tem que sair vivo da Ponte de Varn sem ter fugido\", diz. "
                         "Theodore chora como criança. Seus homens também.", "verde")
                m["caminho"] = "redencao"
                cm.mudar_aprovacao(g, "morel", 12)
                cm.reagir(g, "misericordia")
            else:
                if op2 == "poupar":
                    g.dizer("Morel ouve, mas não escuta.", "cinza")
                g.narrar("Morel crava a espada. Fecha os olhos de Theodore com cuidado e fica ali, de joelhos, até os "
                         "outros irem embora.", "cinza")
                m["caminho"] = "capitao"
                cm.mudar_aprovacao(g, "morel", 6)
        else:
            g.narrar("Theodore é mais rápido. A espada dele abre o flanco de Morel, que cai de joelhos. O tenente cospe "
                     "no chão. \"Agora estamos quites, capitão.\" E vai embora com os seus.", "vermelho")
            m["hp"] = 1
            m["ferido"] = True
            m["caminho"] = "quites"
            cm.mudar_aprovacao(g, "morel", 5)
        cm.reagir(g, "honra")
        m["missao"] = 3
        return
    # Luta
    lider = g.inimigo("mercenario", nome_unico="Theodore, o Ruivo", nivel=g.j.nivel + 1)
    grupo = [lider] + [g.inimigo("bandido", nivel=g.j.nivel) for _ in range(2)]
    for e in grupo[1:]:
        e.nome = "Desertor dos Cães"
    resultado = g.combate(grupo, pode_fugir=False, titulo="OS CÃES DE FERRO")
    if resultado == "vitoria" and cm.presente(g, "morel"):
        g.narrar("Morel se ajoelha ao lado de Theodore. \"Eu devia isso a você, Theo.\" Não fica claro se fala da luta "
                 "ou da ponte.", "cinza")
        m["caminho"] = "capitao"
        cm.mudar_aprovacao(g, "morel", 15)
        m["missao"] = 3


@conversa("morel", 2, dias=4, aprov=40, cond=lambda g, m: m["missao"] == 3)
def morel_conversa_final(g, m):
    g.dizer("Morel joga algo no seu colo: uma insígnia de bronze, um cão de dentes à mostra, gasta de tanto ser "
            "apertada.")
    if m["caminho"] in ("redencao", "adiado"):
        g.dizer("\"Eu guardava para quando achasse alguém que merecesse a companhia. A companhia agora é pouca. Serve.\"",
                "amarelo")
    else:
        g.dizer("\"Não sei mais o que ela significa\", diz Morel. \"Fica com você. Você parece saber.\"", "amarelo")
    cm.mudar_aprovacao(g, "morel", 5)


# ====================================================================== YARA
@evento(contextos=("explorar",), peso=lambda g: 18 if g.dia <= 12 else 8, cooldown=0, unico=True,
        cond=lambda g: g.dia >= 3 and g.bioma in ("pantano", "floresta") and cm.disponivel(g, "yara")
        and caspar.fogueira_possivel(g))  # no Vale do Turvo, não depois de Caspar perder a vigília
def yara_na_fogueira(g):
    g.dizer("Fumaça e gritos atrás das árvores. Numa clareira, aldeões com forcados e tochas cercam uma pilha de lenha. "
            "Amarrada a um poste no meio dela, uma moça de cabelo sujo de lama encara a multidão sem chorar.")
    quem = "o Irmão Caspar, o homem de batina remendada" if g.campanha else "um homem de batina remendada"
    g.dizer(f"\"BRUXA!\", grita {quem}. \"O gado morreu, o poço secou, as crianças têm febre! "
            "Foi ela!\"", "vermelho")
    g.dizer("A moça vê você. Não pede ajuda. Só olha.", "cinza")
    op = g.menu("O que faz?", [
        ("\"Soltem a moça.\" (Força)", "forca"),
        ("\"A febre vem do poço, não dela.\" (Carisma)", "falar"),
        ("Assustá-los com magia (Arcano)", "magia") if g.j.classe == "mago" else None,
        ("\"Eu levo a bruxa daqui. Vinte moedas pelo incômodo.\"", "comprar") if g.j.ouro >= 20 else None,
        ("Deixar que façam justiça", "deixar"),
    ])
    if op == "deixar":
        g.narrar("A lenha pega rápido. Ela não grita. É isso que você vai lembrar depois: ela não gritou.", "vermelho")
        g.narrar("Quando o fogo baixa, os aldeões rezam e voltam para casa. O poço continua seco.", "cinza")
        cm.reagir(g, "fanatismo", "crueldade")
        g.marcar("comitiva:yara", "morto")
        return
    simpatia = 0
    if op == "forca":
        if g.teste("forca", 13):
            g.dizer("Você arranca o forcado da mão do primeiro e o quebra no joelho. Ninguém quer ser o segundo.", "verde")
            simpatia = 8
        else:
            g.dizer("Alguém te acerta com um cabo de enxada. A turba avança!", "vermelho")
            turba = [g.inimigo("bandido", nivel=max(1, g.nivel_local() - 1)) for _ in range(2)]
            for e in turba:
                e.nome = "Aldeão furioso"
            if g.combate(turba, titulo="A TURBA") != "vitoria":
                return
            simpatia = 6
        g.mudar_reputacao(-2)
        cm.reagir(g, "rebeldia")
    elif op == "falar":
        if g.teste("carisma", 13):
            g.dizer("Você fala do moleiro que desviou o riacho, da água parada, das crianças que bebem dela. Um a um, "
                    "os forcados baixam. O pregador é o último a ir embora.", "verde")
            simpatia = 10
            cm.reagir(g, "diplomacia")
        else:
            g.dizer("\"Outro bruxo!\", grita o pregador. Mas ninguém se mexe, e você corta as cordas enquanto discutem.",
                    "amarelo")
            simpatia = 6
    elif op == "magia":
        if g.teste("arcano", 12):
            g.dizer("As tochas se apagam todas ao mesmo tempo. Na escuridão, você faz a fogueira sussurrar o nome de "
                    "cada um deles. A clareira se esvazia em segundos.", "verde")
            simpatia = 12
            cm.reagir(g, "magia_proibida")
        else:
            g.dizer("Sua magia falha, mas a turba se assusta mesmo assim. Você corta as cordas na confusão.", "amarelo")
            simpatia = 6
    else:
        g.perder_ouro(20)
        g.dizer("O pregador conta as moedas e abençoa você. A moça é desamarrada como se fosse uma cabra vendida.", "cinza")
        simpatia = -2
        cm.reagir(g, "pragmatismo")
    g.dizer("Ela esfrega os pulsos em carne viva. \"Yara\", diz. \"Eles vão voltar com mais lenha. Eu não tenho para "
            "onde ir.\" Um sorriso torto. \"E você tem cara de quem precisa de alguém que fale com sapos.\"", "amarelo")
    if cm.oferecer_vaga(g, "yara"):
        cm.mudar_aprovacao(g, "yara", simpatia, mostrar=False)
    else:
        g.dizer("Yara assente e some no brejo, entre a névoa, sem fazer barulho nenhum.", "cinza")
        g.marcar("comitiva:yara", "recusou")


@conversa("yara", 0, dias=1)
def yara_conversa_bruxa(g, m):
    g.dizer("\"Se bruxa é quem fala com sapo e sabe qual cogumelo mata, então sou\", diz Yara, mexendo o fogo com "
            "um graveto. \"O poço secou porque o moleiro desviou o riacho. Mas é mais fácil queimar a moça esquisita do "
            "que brigar com o moleiro.\"")
    op = g.menu("O que diz?", [
        ("\"Eles estavam com medo. Medo faz gente fazer coisas horríveis.\"", "medo"),
        ("\"Me ensina qual cogumelo mata?\"", "cogumelo"),
        ("\"Talvez eles tivessem razão em ter medo de você.\"", "razao"),
    ])
    if op == "medo":
        g.dizer("\"Medo\", repete Yara. \"É. Eu conheço bem.\"", "cinza")
        cm.mudar_aprovacao(g, "yara", 2)
    elif op == "cogumelo":
        g.dizer("Ela ri de verdade, pela primeira vez. Passa a noite te mostrando raízes, fungos e flores, e no fim te "
                "entrega um frasquinho. \"Para quando alguém tentar te envenenar. Vão tentar.\"", "verde")
        g.dar("antidoto")
        cm.mudar_aprovacao(g, "yara", 6)
    else:
        g.dizer("Yara para de mexer o fogo. \"Talvez\", diz, e sorri de um jeito que não chega aos olhos.", "vermelho")
        cm.mudar_aprovacao(g, "yara", -6)


@conversa("yara", 1, dias=3, aprov=10)
def yara_conversa_voz(g, m):
    g.dizer("Yara espera os outros dormirem. Então fala, quase sem som.")
    g.narrar("\"Desde que a Fenda abriu, eu ouço uma voz. Não é loucura. É ele: Ulook. Ele fala do jeito que a minha "
             "mãe falava, antes de morrer. Diz que eu sou especial. Que posso ficar forte o bastante para que ninguém "
             "nunca mais me amarre num poste.\"", "magenta")
    g.narrar("\"E a pior parte: quando eu deixo ele falar, eu fico forte mesmo.\"", "magenta+negrito")
    op = g.menu("O que diz?", [
        ("\"Você não precisa dele. Você tem a gente.\"", "cortar"),
        ("\"Use a voz. Tire dele tudo o que puder, e depois jogue fora.\"", "usar"),
        ("\"Se ele te controlar, eu vou ter que te matar.\"", "ameaca"),
    ])
    if op == "cortar":
        g.dizer("\"A gente\", repete Yara, como quem experimenta uma palavra nova. Ela não responde, mas dorme "
                "encostada no seu ombro.", "verde")
        cm.mudar_aprovacao(g, "yara", 5)
    elif op == "usar":
        g.dizer("Os olhos dela brilham à luz do fogo. \"É o que eu penso também. Ninguém nunca concordou comigo antes.\"",
                "magenta")
        cm.mudar_aprovacao(g, "yara", 6)
    else:
        g.dizer("Yara te olha por muito tempo. \"Justo. Promete que vai ser rápido.\"", "cinza")
        cm.mudar_aprovacao(g, "yara", -2)
    m["conselho"] = op
    m["missao"] = 1


@evento(contextos=("acampamento",), peso=60, cooldown=0, unico=True,
        cond=lambda g: cm.presente(g, "yara") and cm.membro(g, "yara")["missao"] == 1)
def yara_sonambula(g):
    m = cm.membro(g, "yara")
    g.dizer("Você acorda de madrugada. O lugar de Yara está vazio. Pegadas descalças levam para longe da fogueira, "
            "em direção a um brilho roxo, fraco, no meio do mato.")
    op = g.menu("O que faz?", [
        ("Seguir as pegadas em silêncio", "seguir"),
        ("Acordá-la à força (Vontade)", "acordar"),
        ("Deixá-la ir. É escolha dela.", "deixar"),
    ])
    if op == "seguir":
        g.dizer("Você a encontra ajoelhada diante de uma rachadura no chão, de onde sobe uma luz que não ilumina. Ela "
                "fala. E alguma coisa responde.", "magenta")
        vivos = _vivos_covis(g)
        if vivos:
            l = g.sortear(vivos)
            g.marcar(f"conhecido:{l['id']}")
            g.marcar(f"fraqueza:guardiao:{l['id']}")
            g.dizer(f"Você ouve a voz falar de {l['guardiao']['nome']}: onde dorme ({l['nome']}), o que teme, onde "
                    "sangra. (Você causará +25% de dano nele.)", "verde")
        g.dizer("Ao amanhecer, Yara volta para o acampamento como se nada tivesse acontecido. Você não diz nada. Ela "
                "também não.", "cinza")
    elif op == "acordar":
        if g.teste("vontade", 13):
            g.dizer("Você a sacode até os olhos dela voltarem. Ela grita, te bate, e depois chora agarrada em você até "
                    "o sol nascer.", "verde")
            cm.mudar_aprovacao(g, "yara", 4)
        else:
            g.dizer("Quando você toca nela, algo do outro lado empurra de volta. Você é jogado longe.", "vermelho")
            g.ferir(g.j.max_hp * 0.15, " pela força da Fenda")
            cm.mudar_aprovacao(g, "yara", 2)
    else:
        g.dizer("Ela volta ao amanhecer. Os olhos estão mais escuros. Ela sorri para você como quem agradece.",
                "magenta")
        cm.mudar_aprovacao(g, "yara", 5)
        m["conselho"] = m.get("conselho") or "usar"
    m["missao"] = 2


@evento(contextos=("explorar",), peso=40, cooldown=0, unico=True,
        cond=lambda g: cm.presente(g, "yara") and cm.membro(g, "yara")["missao"] == 2
        and g.bioma in ("pantano", "floresta", "ruinas"))
def yara_circulo_negro(g):
    m = cm.membro(g, "yara")
    g.dizer("Yara para diante de um círculo de pedras negras que você nunca viu, mas ela já: em sonhos.")
    g.dizer("\"É aqui. Aqui ele mora mais perto. Aqui eu posso fechar a porta. Ou abrir de vez.\" Ela se vira para "
            "você. \"Eu queria que alguém escolhesse por mim. Mas ninguém nunca escolheu nada por mim que prestasse. "
            "Então eu vou perguntar. O que você faria?\"", "magenta")
    op = g.menu("O que diz?", [
        ("\"Feche a porta. Seja livre dele.\"", "fechar"),
        ("\"Abra. Pegue o poder. Nunca mais tenha medo de ninguém.\"", "abrir"),
        ("\"Eu não vou escolher por você.\"", "livre"),
    ])
    if op != "livre" and m["aprovacao"] >= 40:
        escolha = op  # ela confia em você o bastante para ouvir
    else:
        escolha = "fechar" if m.get("conselho") == "cortar" else "abrir"
        if op != "livre":
            g.dizer("Yara escuta, mas você vê nos olhos dela que já decidiu antes de perguntar.", "cinza")
    if escolha == "fechar":
        g.narrar("Yara enfia as mãos na terra e arranca algo que não é raiz. Grita. O círculo racha de ponta a ponta. "
                 "Quando ela se levanta, os olhos são castanhos de novo.", "verde")
        g.narrar("\"Silêncio\", diz ela, chorando e rindo ao mesmo tempo. \"Silêncio de verdade.\"", "verde+negrito")
        m["caminho"] = "liberta"
    else:
        g.narrar("As pedras se acendem. Yara abre os braços e a escuridão entra nela como água num jarro. Quando acaba, "
                 "ela flutua um palmo acima do chão, e sorri. Você nunca a viu tão bonita. Nem tão longe.", "magenta")
        m["caminho"] = "vazio"
        g.dizer("(O poder de Yara agora é muito maior, e bebe um pouco da sua vida a cada luta vencida.)", "ciano")
    if op == "livre":
        cm.mudar_aprovacao(g, "yara", 10)
    elif op == escolha:
        cm.mudar_aprovacao(g, "yara", 8)
    else:
        cm.mudar_aprovacao(g, "yara", -4)
    m["missao"] = 3


@conversa("yara", 2, dias=4, aprov=40, cond=lambda g, m: m["missao"] == 3)
def yara_conversa_final(g, m):
    if m["caminho"] == "liberta":
        g.dizer("\"Sonhei com a minha mãe ontem\", diz Yara. \"Ela não disse nada. Só penteou o meu cabelo, como "
                "fazia.\" Ela sorri. \"Foi o melhor sonho da minha vida.\"", "verde")
    else:
        g.dizer("\"Ele ainda fala comigo\", diz Yara. \"Mas agora eu também falo com ele. E às vezes, só às vezes, "
                "ele tem medo de mim.\"", "magenta")
    cm.mudar_aprovacao(g, "yara", 3)


# ====================================================================== DISCUSSÕES
def _par(g, a, b):
    return cm.presente(g, a) and cm.presente(g, b)


def _acalmar(g, a, b):
    if g.teste("carisma", 13):
        g.dizer("Você fala até as duas vozes baixarem. Ninguém sai satisfeito, mas ninguém sai ferido.", "verde")
        cm.mudar_aprovacao(g, a, 2)
        cm.mudar_aprovacao(g, b, 2)
    else:
        g.dizer("Ninguém te escuta. Os dois dormem de costas um para o outro, e para você.", "vermelho")
        cm.mudar_aprovacao(g, a, -2)
        cm.mudar_aprovacao(g, b, -2)


@evento(contextos=("acampamento",), peso=22, cooldown=10, max_vezes=2, cond=lambda g: _par(g, "odete", "yara"))
def discussao_fe_e_bruxaria(g):
    g.dizer("Odette e Yara discutem baixo, do jeito que só se discute quando já se discutiu antes.")
    g.dizer("\"Você brinca com a mesma coisa que matou quarenta inocentes\", diz Odette.", "amarelo")
    g.dizer("\"E você reza para o mesmo deus que deixou acontecer\", responde Yara.", "magenta")
    op = g.menu("As duas olham para você.", [
        ("Ficar do lado de Odette", "odete"),
        ("Ficar do lado de Yara", "yara"),
        ("\"As duas têm razão, e as duas vão dormir agora.\" (Carisma)", "acalmar"),
    ])
    if op == "acalmar":
        _acalmar(g, "odete", "yara")
        return
    outra = "yara" if op == "odete" else "odete"
    cm.mudar_aprovacao(g, op, 6)
    cm.mudar_aprovacao(g, outra, -6)


@evento(contextos=("acampamento",), peso=22, cooldown=10, max_vezes=2, cond=lambda g: _par(g, "odete", "morel"))
def discussao_pao(g):
    g.dizer("De manhã, Odette separa um embrulho de pão para uma família que dorme na beira da estrada. Morel segura "
            "o pulso dela.")
    g.dizer("\"Comida é para quem segura a espada\", diz ele. \"Caridade não salva ninguém da Fenda.\"", "amarelo")
    g.dizer("\"Então para que estamos lutando?\", pergunta Odette.", "amarelo")
    op = g.menu("Os dois esperam a sua palavra.", [
        ("\"Deixe ela dar o pão, Morel.\" (−1 provisão)", "odete") if g.j.provisoes > 0 else None,
        ("\"Morel tem razão. A estrada é longa.\"", "morel"),
        ("\"Metade para eles, metade para nós.\" (Carisma)", "acalmar"),
    ])
    if op == "acalmar":
        _acalmar(g, "odete", "morel")
        return
    if op == "odete":
        g.j.provisoes -= 1
        g.mudar_reputacao(1)
    outro = "morel" if op == "odete" else "odete"
    cm.mudar_aprovacao(g, op, 6)
    cm.mudar_aprovacao(g, outro, -6)


@evento(contextos=("acampamento",), peso=22, cooldown=10, max_vezes=2, cond=lambda g: _par(g, "morel", "yara"))
def discussao_mao_na_espada(g):
    g.dizer("Morel dorme sentado, de frente para Yara, com a mão no punho da espada. Ela percebe.")
    g.dizer("\"Se eu quisesse te matar, mercenário, você nem acordava.\"", "magenta")
    g.dizer("\"É exatamente por isso que eu não durmo\", diz Morel.", "amarelo")
    op = g.menu("O que faz?", [
        ("\"Ela é uma de nós, Morel. Larga essa espada.\"", "yara"),
        ("\"Ele tem razão em ser cuidadoso, Yara.\"", "morel"),
        ("\"Se os dois não vão dormir, que pelo menos vigiem a estrada.\" (Carisma)", "acalmar"),
    ])
    if op == "acalmar":
        _acalmar(g, "morel", "yara")
        return
    outro = "morel" if op == "yara" else "yara"
    cm.mudar_aprovacao(g, op, 6)
    cm.mudar_aprovacao(g, outro, -5)
