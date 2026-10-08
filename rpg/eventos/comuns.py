"""Eventos gerais: encontros, estranhos na estrada e consequências de escolhas passadas."""

from .. import balanceamento as bal
from .. import texto as tx
from ..dados import BIOMAS, FAMILIAS
from ..itens import gerar_equip
from .motor import evento


# ---------------------------------------------------------------------- encontros
@evento(peso=lambda g: 38 if g.noite else 28, cooldown=0)
def encontro_hostil(g):
    grupo = g.grupo()
    abertura = g.sortear(BIOMAS[g.bioma]["abertura"])
    cd = 11 + (3 if g.noite else 0) + (2 if g.clima in ("nevoa", "tempestade") else 0)
    if g.teste("percepcao", cd):
        g.dizer(tx.concordar("{abertura}, você avista {grupo} antes que {note|notem} sua presença.", grupo,
                             abertura=abertura), "amarelo")
        opcoes = [
            (f"Atacar de surpresa: um turno livre, e o golpe dele {round(bal.INICIATIVA_BONUS * 100)}% mais forte", "atacar"),
            ("Tentar passar despercebido (Destreza)", "evitar"),
        ]
        if g.j.classe == "arqueiro":
            # Escolha de verdade: a surpresa é um golpe certeiro agora; o ponto alto é uma vantagem que dura,
            # forte contra quem luta corpo a corpo e inútil contra quem voa ou conjura, e a subida pode falhar.
            opcoes.insert(1, ("Subir num ponto alto (Destreza): quem luta corpo a corpo perde o 1º turno "
                              "escalando; +15% de dano por 3 turnos", "alto"))
        if g.j.classe == "mago":
            opcoes.append((tx.concordar("Lançar uma ilusão para distraí{-los} (Arcano)", grupo), "ilusao"))
        if all("humano" in e.tracos for e in grupo):
            opcoes.append(("Conversar (Carisma)", "conversar"))
        op = g.menu("O que você faz?", opcoes)
        if op == "alto":
            if g.teste("destreza", 11):
                g.dizer(tx.concordar("Você escala as pedras sem um ruído. Lá de cima, {eles} {é um alvo fácil|são "
                                     "alvos fáceis}.", grupo), "verde")
                for e in grupo:
                    e.aplicar("marcado", 3, 0.15)
                    if not {"voador", "conjurador"} & set(e.tracos):
                        e.aplicar("atordoado", 1, 0)
                        e.efeitos["atordoado"]["r"] = "escalando"
            else:
                g.dizer(tx.concordar("Uma pedra solta rola encosta abaixo. {Eles} {olha|olham} para cima"
                                     "{| ao mesmo tempo}.", grupo), "vermelho")
            g.combate(grupo)
        elif op == "atacar":
            g.combate(grupo, emboscada="jogador")
        elif op == "evitar":
            if g.teste("destreza", 12):
                g.dizer("Você se esgueira para longe sem ser visto.", "verde")
                g.ganhar_xp(5)
            else:
                g.dizer(tx.concordar("Um galho estala sob seu pé. {Grupo} se {vira|viram}!", grupo), "vermelho")
                g.combate(grupo)
        elif op == "ilusao":
            if g.teste("arcano", 12):
                g.dizer(tx.concordar("Uma figura fantasmagórica surge ao longe e atrai a atenção {deles}. Você passa "
                                     "ileso.", grupo), "azul")
                g.ganhar_xp(8)
            else:
                g.dizer(tx.concordar("A ilusão tremeluz e se desfaz. {Eles} {olha|olham} direto para você.", grupo),
                        "vermelho")
                g.combate(grupo)
        elif op == "conversar":
            if g.teste("carisma", 13):
                g.dizer(tx.concordar("Depois de alguma tensão, {eles} {aceita|aceitam} uma moeda e {segue|seguem} "
                                     "caminho. Ninguém sangra hoje.", grupo), "verde")
                g.perder_ouro(5)
                g.ganhar_xp(8)
            else:
                g.dizer(tx.concordar("\"Belas palavras. Agora passa a bolsa.\" {A arma sai da bainha|As armas saem "
                                     "das bainhas}.", grupo), "vermelho")
                g.combate(grupo)
    else:
        g.dizer(tx.concordar("{abertura}, {grupo} {surge|surgem} de repente!", grupo, abertura=abertura), "vermelho")
        g.combate(grupo, emboscada="inimigo" if g.chance(0.5) else None)


@evento(peso=lambda g: 60, cooldown=4,
        cond=lambda g: g.nemesis and g.passos >= g.nemesis["pronto"] and g.loc["tipo"] != "vila")
def nemesis_retorna(g):
    n = g.nemesis
    n["vezes"] += 1
    f = FAMILIAS[n["familia"]]
    e = g.inimigo(n["familia"], afixo=n["afixo"], nome_unico=n["nome"], nivel=n["nivel"])
    e.chave = "nemesis"
    if n["vezes"] == 1:
        g.dizer(f"Você reconhece o cheiro antes de ver: {e.nome}. A mesma criatura de quem você fugiu. "
                f"Desta vez, ela te encontrou primeiro.", "vermelho+negrito")
    else:
        g.dizer(f"{e.nome} de novo! Mais cicatrizes, mais raiva. {tx.maiuscula(tx.artigo(f['g']))} "
                f"{f['nome']} não vai desistir de você.", "vermelho+negrito")
    if g.combate([e], emboscada="inimigo" if g.chance(0.4) else None) == "fuga":
        n["nivel"] += 1
        n["pronto"] = g.passos + 5


@evento(peso=45, cooldown=3, cond=lambda g: g.contrato_alvo_aqui() is not None)
def alvo_contrato(g):
    c = g.contrato_alvo_aqui()
    e = g.inimigo(c["familia"], afixo="anciao", nome_unico=c["nome"], bonus=1)
    e.chave = c["chave"]
    g.dizer(tx.concordar("Marcas enormes, carcaças roídas... Os sinais batem com a descrição do contrato. "
                         "Então você {os} vê: {nome}.", [e], nome=e.nome), "amarelo+negrito")
    if g.teste("percepcao", 13):
        g.dizer(tx.concordar("Você {os} vê antes que {eles} te veja.", [e]), "verde")
        g.combate([e], emboscada="jogador")
    else:
        g.combate([e])


# ---------------------------------------------------------------------- estranhos na estrada
@evento(peso=8, cooldown=10)
def viajante_ferido(g):
    p = g.npc()
    g.dizer(f"Encostad{p['o']} numa pedra, {p['um']} {p['prof']} {p['traco']} segura uma ferida "
            f"que não para de sangrar. \"Bandidos... levaram tudo.\"", "amarelo")
    op = g.menu("O que você faz?", [
        ("Dar uma poção de vida", "pocao") if g.j.tem("pocao_vida") else None,
        ("Fazer um curativo (Bandagem)", "bandagem") if g.j.tem("bandagem") else None,
        ("Rezar pela cura (Paladino)", "prece") if g.j.spec == "paladino" else None,
        ("Ir atrás dos bandidos", "cacar"),
        ("Revistar os bolsos enquanto está fraco", "roubar"),
        ("Seguir seu caminho", "ignorar"),
    ])
    if op in ("pocao", "bandagem", "prece"):
        if op != "prece":
            g.j.consumiveis["pocao_vida" if op == "pocao" else "bandagem"] -= 1
        else:
            g.dizer("Uma luz morna escorre das suas mãos e fecha a ferida.", "amarelo")
        g.dizer(f"{p['nome']} respira aliviad{p['o']}. \"Não vou esquecer isso. Juro pelos meus filhos.\"", "verde")
        g.mudar_reputacao(4)
        g.ganhar_xp(10)
        g.plantar("viajante_grato", 6, nome=p["nome"], g=p["g"], prof=p["prof"])
    elif op == "cacar":
        grupo = g.grupo("bandido", n=g.rng.randint(1, 2))
        g.dizer(tx.concordar("As pegadas são frescas. Não demora até você encontrar {o responsável|os "
                             "responsáveis}.", grupo), "amarelo")
        if g.combate(grupo) == "vitoria":
            g.dizer(f"Você devolve os pertences a {p['nome']}, que chora de gratidão.", "verde")
            g.mudar_reputacao(5)
            g.plantar("viajante_grato", 6, nome=p["nome"], g=p["g"], prof=p["prof"])
    elif op == "roubar":
        g.dizer(f"Você encontra algumas moedas escondidas na bota. {p['nome']} te olha com um ódio silencioso.",
                "vermelho")
        g.ganhar_ouro(g.rng.randint(8, 20))
        g.mudar_reputacao(-8)
        g.marcar("crueldade", g.flag("crueldade", 0) + 1)
    else:
        g.dizer("Você segue em frente. Os gemidos ficam para trás.", "cinza")


@evento(peso=50, cooldown=2, cond=lambda g: g.semente("viajante_grato"))
def viajante_grato(g):
    d = g.colher("viajante_grato")
    o = "o" if d["g"] == "m" else "a"
    g.dizer(f"\"Ei! Lembra de mim?\" — é {d['nome']}, {o} {d['prof']} que você ajudou. Parece outra pessoa: "
            f"saudável, bem vestid{o}.", "verde")
    if g.chance(0.5):
        g.dizer("\"Eu disse que não esqueceria. Tome. Era do meu avô, e ele também era teimoso como você.\"", "verde")
        g.oferecer_equip(gerar_equip(g.rng, g.j.classe, g.j.nivel, qualidade=1))
    else:
        g.dizer("\"Contei sua história em cada vila. Quando a hora chegar, me chame. Eu e meus amigos "
                "estaremos lá.\"", "verde")
        g.aliado_final(d["nome"], f"{d['nome']} surge com uma dúzia de aldeões armados com forcados e tochas! "
                                  f"Eles distraem as sombras enquanto você avança.", "dano", 0.08)
        g.ganhar_ouro(15)


@evento(peso=7, cooldown=10)
def mercador_ambulante(g):
    p = g.npc()
    item = gerar_equip(g.rng, g.j.classe, g.j.nivel + 1)
    preco = int(item["preco"] * 0.7)
    g.dizer(f"Uma carroça colorida para ao seu lado. {p['nome']}, {p['um']} mercador{'a' if p['g'] == 'f' else ''} "
            f"{p['traco']}, abre um sorriso largo: \"Para você, preço de amigo!\"", "amarelo")
    g.dizer(f"Oferta: {item['nome']} por {preco} ouro.", "amarelo")
    op = g.menu("O que faz?", [
        (f"Comprar ({preco} ouro)", "comprar") if g.j.ouro >= preco else None,
        ("Examinar a mercadoria com atenção (Percepção)", "examinar"),
        ("Comprar uma poção de vida (15 ouro)", "pocao") if g.j.ouro >= 15 else None,
        ("Recusar", "nao"),
    ])
    if op == "examinar":
        if g.teste("percepcao", 13):
            if g.chance(0.4):
                g.dizer("A pedra do item é vidro pintado. Você aponta isso e o mercador, sem graça, baixa o preço "
                        "de outro item.", "verde")
                g.dar("pocao_vida")
            else:
                g.dizer("A peça é legítima. O mercador até baixa o preço, impressionado com seu olho.", "verde")
                preco = int(preco * 0.8)
                if g.j.ouro >= preco and g.menu(f"Comprar por {preco}?", [("Sim", True), ("Não", False)]):
                    g.perder_ouro(preco)
                    g.oferecer_equip(item)
        else:
            g.dizer("Parece tudo certo. Mas você não tem certeza.", "cinza")
            if g.j.ouro >= preco and g.menu(f"Comprar por {preco}?", [("Sim", True), ("Não", False)]):
                g.perder_ouro(preco)
                if g.chance(0.25):
                    g.dizer("Dois dias depois, a peça se desfaz em suas mãos. Golpe!", "vermelho")
                else:
                    g.oferecer_equip(item)
    elif op == "comprar":
        g.perder_ouro(preco)
        if g.chance(0.2):
            g.dizer("Quando a carroça some na curva, você percebe que a peça é falsa. Que ódio.", "vermelho")
            g.plantar("mercador_golpista", 8, nome=p["nome"], preco=preco)
        else:
            g.oferecer_equip(item)
    elif op == "pocao":
        g.perder_ouro(15)
        g.dar("pocao_vida")


@evento(peso=40, cooldown=3, cond=lambda g: g.semente("mercador_golpista"))
def mercador_golpista(g):
    d = g.colher("mercador_golpista")
    g.dizer(f"Uma carroça colorida atolada na lama. E quem está empurrando? {d['nome']}, o golpista.", "amarelo")
    op = g.menu("O que faz?", [
        ("Exigir seu dinheiro de volta", "exigir"),
        ("Ajudar a desatolar, sem dizer nada", "ajudar"),
        ("Dar uma lição nele", "licao"),
    ])
    if op == "exigir":
        g.dizer("Pálido, ele devolve tudo — e um pouco mais, \"pelos juros\".", "verde")
        g.ganhar_ouro(int(d["preco"] * 1.3))
    elif op == "ajudar":
        g.dizer("Ele fica tão envergonhado que te entrega uma peça de verdade, sem cobrar.", "verde")
        g.mudar_reputacao(3)
        g.oferecer_equip(gerar_equip(g.rng, g.j.classe, g.j.nivel, qualidade=1))
    else:
        g.dizer("Ele foge deixando a carroça para trás. Você pega o que é seu.", "amarelo")
        g.ganhar_ouro(d["preco"])
        g.dar("tonico")
        g.mudar_reputacao(-2)


@evento(peso=8, cooldown=8)
def bau_abandonado(g):
    lugar = g.sortear(["meio enterrado na lama", "sob raízes retorcidas", "atrás de uma pedra coberta de musgo",
                       "dentro de um tronco oco", "entre os restos de uma carroça"])
    g.dizer(f"Você encontra um baú {lugar}. A fechadura está enferrujada.", "amarelo")
    op = g.menu("O que faz?", [
        ("Abrir com cuidado, procurando armadilhas (Percepção)", "cuidado"),
        ("Arrombar com força (Força)", "forca"),
        ("Abrir com magia (Arcano)", "magia") if g.j.classe == "mago" else None,
        ("Deixar quieto", "nao"),
    ])
    if op == "nao":
        g.dizer("Algumas coisas é melhor não abrir.", "cinza")
        return
    if g.chance(0.12) and g.j.nivel >= 2:
        g.dizer("O baú abre... uma BOCA. Dentes, língua, e uma fome antiga. É um mímico!", "vermelho+negrito")
        mimico = g.inimigo("golem", afixo="feroz")
        mimico.nome = "Mímico"
        mimico.desc = "um mímico"
        mimico.tracos = ["construto"]
        mimico.habilidades = ["agarrar", "mordida_sangrenta"]
        mimico.ouro *= 4
        g.combate([mimico], emboscada="inimigo" if op == "forca" else None)
        return
    atributo = {"cuidado": "percepcao", "forca": "forca", "magia": "arcano"}[op]
    if g.teste(atributo, 12):
        g.dizer("A tampa cede.", "verde")
        g.ganhar_ouro(g.rng.randint(10, 25) + 3 * g.j.nivel)
        if g.chance(0.5):
            g.dar(g.sortear(["pocao_vida", "tonico", "antidoto", "bomba_fumaca"]))
        if g.chance(0.3):
            g.oferecer_equip(gerar_equip(g.rng, g.j.classe, g.j.nivel))
        g.dar_flechas(g.rng.randint(4, 8) if g.chance(0.5) else 0)
    else:
        g.dizer("Uma agulha salta da fechadura. Veneno!", "vermelho")
        g.ferir(5 + 2 * g.j.nivel, " com a armadilha")
        g.ganhar_ouro(g.rng.randint(3, 10))


@evento(peso=6, cooldown=12)
def santuario_antigo(g):
    deus = g.sortear(["uma deusa de olhos vendados", "um deus-cervo de chifres de prata", "uma figura encapuzada sem rosto",
                      "um guerreiro de pedra ajoelhado", "uma mãe segurando uma lua"])
    g.dizer(f"Um pequeno santuário coberto de flores secas. A estátua representa {deus}.", "amarelo")
    op = g.menu("O que faz?", [
        ("Rezar (Vontade)", "rezar"),
        (f"Deixar uma oferenda ({10 + 2 * g.j.nivel} ouro)", "oferenda") if g.j.ouro >= 10 + 2 * g.j.nivel else None,
        ("Pegar as moedas deixadas por outros peregrinos", "saquear"),
        ("Seguir em frente", "nao"),
    ])
    if op == "nao":
        return
    if op == "saquear":
        g.ganhar_ouro(g.rng.randint(5, 15))
        if g.chance(0.6):
            g.dizer("Ao se afastar, você sente um peso frio nos ombros. A estátua parece te seguir com o olhar.",
                    "magenta")
            g.j.base["max_hp"] -= 3
            g.j.recalcular()
            g.dizer("Maldição: -3 de vida máxima.", "vermelho")
        g.mudar_reputacao(-3)
        return
    sucesso = True
    if op == "oferenda":
        g.perder_ouro(10 + 2 * g.j.nivel)
    else:
        sucesso = g.teste("vontade", 12)
    if not sucesso:
        g.dizer("Silêncio. Só o vento responde.", "cinza")
        return
    bencao = g.sortear(["vida", "fenix", "cura", "poder", "fenix" if not g.flag("bencao_fenix") else "vida"])
    if bencao == "vida":
        g.bonus_permanente("max_hp", 5)
        g.j.recalcular()
        g.curar(5)
        g.dizer("Um calor sobe pelo seu peito. (+5 vida máxima)", "verde")
    elif bencao == "fenix":
        g.marcar("bencao_fenix")
        g.dizer("Uma pena dourada pousa no altar e some na sua mão. Você sente que, se cair, poderá se erguer "
                "uma vez.", "amarelo+negrito")
    elif bencao == "cura":
        g.curar(g.j.max_hp * 0.5)
        g.j.rec = g.j.max_rec
        g.j.ferimentos = []
        g.j.recalcular()
        g.dizer("Um calor sobe da pedra. Ossos se recolocam, cortes se fecham. Todos os ferimentos somem.", "verde")
    else:
        stat = "atk" if g.j.classe != "mago" else "poder"
        g.bonus_permanente(stat, 1)
        g.j.recalcular()
        g.dizer("Sua arma parece mais leve, seus golpes mais certeiros. (+1 permanente)", "verde")


@evento(peso=7, cooldown=10, cond=lambda g: g.bioma in ("floresta", "planicie", "montanha", "pantano"))
def acampamento_bandidos(g):
    lider = tx.nome_proprio(g.rng)
    g.dizer(f"Fumaça entre as árvores. Um acampamento de bandidos: barracas remendadas, um caldeirão, "
            f"e um homem de chapéu de pena dando ordens — chamam-no de {lider}.", "amarelo")
    op = g.menu("O que faz?", [
        ("Atacar de surpresa", "atacar"),
        ("Esgueirar-se e roubar os ladrões (Destreza)", "roubar"),
        ("Entrar e propor um acordo (Carisma)", "acordo"),
        ("Dar a volta e evitar", "evitar"),
    ])
    if op == "evitar":
        g.dizer("Você contorna o acampamento. Melhor assim.", "cinza")
        return
    if op == "roubar":
        if g.teste("destreza", 13):
            g.dizer("Você entra e sai como uma brisa, levando um saco de moedas.", "verde")
            g.ganhar_ouro(g.rng.randint(20, 40) + 3 * g.j.nivel)
            return
        g.dizer("\"LADRÃO!\" — a ironia não passa despercebida por ninguém.", "vermelho")
        op = "atacar_mal"
    if op == "acordo":
        if g.teste("carisma", 14):
            g.dizer(f"{lider} ri. \"Gosto de você. Tome, por conta da casa — e diga aos guardas que somos "
                    f"pescadores.\"", "verde")
            g.ganhar_ouro(10)
            g.plantar("bandido_poupado", 10, lider=lider, tipo="acordo")
            return
        g.dizer("\"Acordo? O acordo é: você morre e a gente fica com suas botas.\"", "vermelho")
    grupo = g.grupo("bandido", n=2)
    chefe = g.inimigo("bandido", afixo="anciao", nome_unico=lider)
    r = g.combate(grupo + [chefe], emboscada="jogador" if op == "atacar" else None)
    if r == "vitoria":
        g.ganhar_ouro(g.rng.randint(15, 30))
        g.mudar_reputacao(3)


@evento(peso=10, cooldown=6, cond=lambda g: g.semente("bandido_poupado"))
def bandido_poupado(g):
    d = g.colher("bandido_poupado")
    g.dizer(f"Um assobio. Do mato sai {d['lider']}, o bandido de chapéu de pena, com metade do bando.", "amarelo")
    if g.j.reputacao >= 0 or g.chance(0.5):
        g.dizer("\"Ouvimos falar do que você anda fazendo contra a sombra. O Vazio é mau pros negócios. "
                "Quando for enfrentar o chefão, conta com a gente.\"", "verde")
        g.aliado_final(d["lider"], f"{d['lider']} e seu bando caem do teto em cordas, gritando como loucos! "
                                   f"Flechas e facas voam contra {g.antagonista['curto']}.", "dano", 0.1)
    else:
        g.dizer("\"Mudei de ideia sobre você. Sua cabeça vale mais do que sua amizade.\"", "vermelho")
        grupo = g.grupo("bandido", n=2) + [g.inimigo("bandido", afixo="feroz", nome_unico=d["lider"])]
        g.combate(grupo)


@evento(peso=6, cooldown=12)
def crianca_perdida(g):
    nome = g.sortear(tx.NOMES_M + tx.NOMES_F)
    g.dizer(f"Um choro baixinho. Uma criança de uns sete anos, encolhida, diz que se chama {nome} e que se "
            f"perdeu da família.", "amarelo")
    vilas = [l for l in g.mundo["locais"] if l["tipo"] == "vila"]
    vila = g.sortear(vilas)
    op = g.menu("O que faz?", [
        (f"Levá-la até {vila['nome']} (perde tempo)", "levar"),
        ("Dar comida e indicar o caminho", "indicar"),
        ("Ignorar", "ignorar"),
    ])
    if op == "levar":
        g.dizer("Vocês caminham juntos. A criança não para de fazer perguntas sobre monstros.", "verde")
        g.avancar_periodo()
        if g.chance(0.4):
            g.dizer("No caminho, algo vos segue...", "vermelho")
            g.combate(g.grupo(n=1))
        g.dizer("Você a entrega a um guarda que conhece a família. \"Vão querer te agradecer\", ele diz.", "verde")
        g.mudar_reputacao(6)
        g.ganhar_xp(20)
        g.plantar("familia_grata", 4, nome=nome, vila=vila["id"])
    elif op == "indicar":
        g.dizer("Ela segue a trilha que você aponta. Você torce para que chegue bem.", "cinza")
        g.mudar_reputacao(1)
        if g.chance(0.5):
            g.plantar("familia_grata", 6, nome=nome, vila=vila["id"])
    else:
        g.mudar_reputacao(-4)


@evento(peso=7, cooldown=10)
def cadaver_aventureiro(g):
    classe = g.sortear(["um cavaleiro", "uma caçadora", "um mago de túnica rasgada", "uma mercenária",
                        "um jovem com uma espada grande demais para ele"])
    g.dizer(f"O corpo de {classe} jaz contra uma árvore. Morreu há poucos dias. Seus pertences ainda estão ali.",
            "amarelo")
    op = g.menu("O que faz?", [
        ("Revistar os pertences", "revistar"),
        ("Enterrar o corpo antes de qualquer coisa", "enterrar"),
        ("Deixar em paz", "nao"),
    ])
    if op == "nao":
        return
    if op == "enterrar":
        g.dizer("Você cava uma cova rasa e diz algumas palavras. Parece o certo a fazer.", "verde")
        g.avancar_periodo()
        g.mudar_reputacao(2)
        if g.j.spec == "necromante":
            g.dizer("Um sussurro agradecido sai da terra. O espírito te concede um pouco de sua força.", "magenta")
            g.bonus_permanente("poder", 1)
            g.j.recalcular()
    vivos = [l for l in g.mundo["locais"] if l["tipo"] == "covil" and not l["guardiao"]["derrotado"]
             and not g.flag(f"fraqueza:guardiao:{l['id']}")]
    if vivos and g.chance(0.6):
        alvo = g.sortear(vivos)
        gu = alvo["guardiao"]
        g.dizer(f"Num diário manchado de sangue: \"...{gu['nome']} em {alvo['nome']}... descobri o ponto fraco, "
                f"preciso avisar alguém...\" As anotações são detalhadas.", "verde+negrito")
        g.marcar(f"fraqueza:guardiao:{alvo['id']}")
        g.marcar(f"conhecido:{alvo['id']}")
        g.dizer(f"(Você causará +25% de dano em {gu['nome']}.)", "verde")
    g.ganhar_ouro(g.rng.randint(5, 20))
    if g.chance(0.4):
        g.oferecer_equip(gerar_equip(g.rng, g.j.classe, g.j.nivel))
    if op == "revistar" and g.chance(0.25):
        g.dizer("Ao tocar o anel do morto, um frio sobe pelo seu braço. Ele morreu de alguma coisa...", "magenta")
        g.ferir(g.j.max_hp * 0.15, " com a maldição")


@evento(peso=7, cooldown=8, cond=lambda g: g.bioma in ("floresta", "pantano", "planicie", "montanha"))
def ervas_medicinais(g):
    erva = g.sortear(["folhas-de-prata", "raiz-de-sangue", "flor-de-sereno", "musgo-estrela"])
    g.dizer(f"Você reconhece um tufo de {erva} — ou algo muito parecido.", "amarelo")
    if g.teste("percepcao", 11):
        g.dizer("É a planta certa. Você colhe o suficiente para preparar remédios — e algumas raízes comestíveis.",
                "verde")
        g.dar(g.sortear(["unguento", "antidoto", "bandagem"]))
        g.dar_provisoes(1)
        if g.j.spec == "patrulheiro" or g.chance(0.3):
            g.dar("bandagem")
    else:
        g.dizer("Você prova uma folha. Erro. Seu estômago revira por horas.", "vermelho")
        g.ferir(4 + g.j.nivel, " com a intoxicação")


@evento(peso=5, cooldown=12, cond=lambda g: g.j.ouro >= 10)
def jogo_de_dados(g):
    p = g.npc()
    g.dizer(f"Junto a uma fogueira, {p['um']} {p['prof']} {p['traco']} sacode dois dados num copo de couro. "
            f"\"Uma partida? Dobro ou nada.\"", "amarelo")
    aposta = min(g.j.ouro, 10 + 5 * g.j.nivel)
    op = g.menu("Apostar?", [
        (f"Apostar {aposta} ouro", "jogar"),
        ("Apostar e tentar trapacear (Destreza)", "trapacear"),
        ("Recusar", "nao"),
    ])
    if op == "nao":
        return
    if op == "trapacear":
        if g.teste("destreza", 14):
            g.dizer("Seis e seis. Que sorte, hein?", "verde")
            g.ganhar_ouro(aposta)
        else:
            g.dizer(f"{p['nome']} segura seu pulso. \"Dado viciado na manga? Logo comigo?\"", "vermelho")
            g.perder_ouro(aposta)
            g.mudar_reputacao(-3)
        return
    meu, dele = g.rng.randint(2, 12), g.rng.randint(2, 12)
    g.dizer(f"Você tira {meu}. {p['nome']} tira {dele}.")
    if meu > dele:
        g.ganhar_ouro(aposta)
    elif meu < dele:
        g.perder_ouro(aposta)
    else:
        g.dizer("Empate. Vocês riem e dividem uma bebida.", "cinza")


@evento(peso=4, cooldown=12, cond=lambda g: g.nivel_local() >= 5)
def visao_do_vazio(g):
    a = g.antagonista
    g.dizer("O mundo perde a cor. Por um instante você está em outro lugar: um trono rachado, um céu sem estrelas, "
            f"e {a['curto']} olhando diretamente para você.", "magenta+negrito")
    g.dizer(f"\"Eu vejo você, {g.j.nome}.\"", "magenta")
    if g.teste("vontade", 13):
        g.dizer("Você sustenta o olhar. Algo se rompe do outro lado — você viu mais do que deveria.", "verde")
        g.ganhar_xp(15 + 5 * g.j.nivel)
        vivos = [l for l in g.mundo["locais"] if l["tipo"] == "covil" and not l["guardiao"]["derrotado"]]
        if vivos:
            l = g.sortear(vivos)
            g.marcar(f"conhecido:{l['id']}")
            g.dizer(f"Na visão, você viu onde {tx.aposto(l['guardiao']['nome'])} se esconde: {l['nome']}.", "verde")
    else:
        g.dizer("Você cai de joelhos, sangrando pelo nariz.", "vermelho")
        g.ferir(g.j.max_hp * 0.2, " com a visão")


@evento(peso=50, cooldown=2, cond=lambda g: g.semente("ladrao_fugitivo"))
def ladrao_fugitivo(g):
    d = g.colher("ladrao_fugitivo")
    g.dizer(f"Risadas perto de um riacho. É {d['nome']}, o ladrão que fugiu com seu ouro, contando moedas.",
            "amarelo")
    e = g.inimigo("bandido", afixo="agil")
    e.nome = d["nome"]
    e.roubado = d["ouro"]
    if g.teste("destreza", 11):
        g.dizer("Ele nem percebe você chegando.", "verde")
        g.combate([e], emboscada="jogador")
    else:
        g.combate([e])


@evento(peso=lambda g: 6 + abs(g.j.reputacao) // 4, cooldown=12, cond=lambda g: g.j.reputacao <= -15)
def cacadores_de_recompensa(g):
    g.dizer("\"É ela... ou ele. Bate com o cartaz.\" Três figuras encapuzadas bloqueiam o caminho. Há um preço "
            "pela sua cabeça.", "vermelho+negrito")
    op = g.menu("O que faz?", [
        ("Lutar", "lutar"),
        (f"Pagar para sumirem ({30 + 5 * g.j.nivel} ouro)", "pagar") if g.j.ouro >= 30 + 5 * g.j.nivel else None,
    ])
    if op == "pagar":
        g.perder_ouro(30 + 5 * g.j.nivel)
        g.dizer("Eles contam as moedas e somem. Por enquanto.", "cinza")
        return
    grupo = [g.inimigo("mercenario"), g.inimigo("bandido", afixo="agil")]
    if g.j.nivel >= 4:
        grupo.append(g.inimigo("cultista"))
    g.combate(grupo)


@evento(peso=40, cooldown=3, cond=lambda g: g.semente("pacote_suspeito") and
        any(c["tipo"] == "entrega" for c in g.contratos))
def pacote_suspeito(g):
    g.colher("pacote_suspeito")
    c = next(c for c in g.contratos if c["tipo"] == "entrega")
    g.dizer(f"Uma figura de capa cinza se aproxima. \"Você leva {c['objeto']}. Pago o triplo do que te "
            f"prometeram. Ninguém precisa saber.\"", "amarelo")
    op = g.menu("O que faz?", [
        ("Recusar", "recusar"),
        ("Aceitar e entregar o pacote", "vender"),
        ("Perguntar por que ele quer tanto (Carisma)", "perguntar"),
    ])
    if op == "vender":
        g.contratos.remove(c)
        g.ganhar_ouro(c["ouro"] * 2)
        g.mudar_reputacao(-6)
        g.dizer("Ele some com o pacote. Você nunca vai saber o que havia dentro.", "cinza")
    elif op == "perguntar":
        if g.teste("carisma", 13):
            g.dizer("\"É prova contra um cultista do Vazio infiltrado na vila de destino.\" Ele hesita. "
                    "\"Quer saber? Entregue. Talvez você seja a pessoa certa.\" Ele te dá uma poção e some.", "verde")
            g.dar("pocao_vida")
            c["ouro"] = int(c["ouro"] * 1.3)
        else:
            g.dizer("Ele perde a paciência. \"Então vai ser do jeito difícil.\"", "vermelho")
            g.combate([g.inimigo("cultista", afixo="agil"), g.inimigo("bandido")])
    else:
        g.dizer("\"Que pena.\" Ele assobia. Dois capangas saem do mato.", "vermelho")
        g.combate([g.inimigo("bandido"), g.inimigo("bandido")])


@evento(peso=12, cooldown=6, cond=lambda g: g.loc["tipo"] == "covil" and not g.loc["guardiao"]["derrotado"])
def sinais_do_guardiao(g):
    gu = g.loc["guardiao"]
    sinais = {
        "Rainha Aracnídea": "Casulos do tamanho de homens pendem das árvores. Alguns ainda se mexem.",
        "Ent Ancião": "As árvores aqui têm rostos. Todos virados na mesma direção.",
        "Hidra do Brejo": "Escamas do tamanho de escudos boiam na água. E três trilhas paralelas de lodo.",
        "Bruxa Afogada": "Uma canção de ninar ecoa sobre a água. Ninguém à vista.",
        "Rei Troll": "Ossos roídos empilhados formando uma espécie de... muralha.",
        "Dragão de Gelo": "Uma faixa de gelo corta a rocha, como se algo tivesse soprado inverno puro.",
        "Senhor da Guerra": "Estacas com elmos espetados marcam a trilha. Um aviso.",
        "Profeta das Cinzas": "Cinzas caem do céu limpo. Cânticos distantes.",
        "Lich Menor": "Esqueletos montam guarda imóveis, lanças erguidas, esperando ordens.",
        "Golem Primordial": "O chão treme em intervalos regulares. Passos.",
    }
    g.dizer(sinais.get(gu["base"], "Algo enorme vive aqui."), "magenta")
    if not g.flag(f"fraqueza:guardiao:{g.loc['id']}") and g.teste("percepcao", 14):
        g.dizer(f"Você estuda os sinais com cuidado e entende como {gu['nome']} se move. Um ponto fraco!",
                "verde+negrito")
        g.marcar(f"fraqueza:guardiao:{g.loc['id']}")
    else:
        g.combate(g.grupo(n=1))


@evento(peso=6, cooldown=10)
def peregrinos(g):
    destino = g.sortear(["do Templo da Aurora", "do Poço das Sete Luas", "do túmulo de um santo esquecido"])
    g.dizer(f"Um grupo de peregrinos descalços canta a caminho {destino}.", "amarelo")
    op = g.menu("O que faz?", [
        ("Caminhar com eles um trecho e ouvir histórias", "ouvir"),
        (f"Doar {5 + g.j.nivel} ouro", "doar") if g.j.ouro >= 5 + g.j.nivel else None,
        ("Seguir sozinho", "nao"),
    ])
    if op == "ouvir":
        from .vila import ouvir_rumor
        ouvir_rumor(g)
    elif op == "doar":
        g.perder_ouro(5 + g.j.nivel)
        g.mudar_reputacao(3)
        g.dizer("Uma velha peregrina te abençoa com óleo na testa.", "verde")
        g.curar(g.j.max_hp * 0.15)


@evento(peso=3, cooldown=10, cond=lambda g: g.nivel_local() >= 3)
def refugiados(g):
    g.dizer("Uma fila de famílias com carroças e trouxas. Fogem de vilarejos onde \"a sombra comeu as "
            "colheitas e depois as pessoas\".", "amarelo")
    op = g.menu("O que faz?", [
        ("Escoltá-los até um lugar seguro", "escoltar"),
        (f"Dar ouro para a viagem ({15 + 3 * g.j.nivel})", "doar") if g.j.ouro >= 15 + 3 * g.j.nivel else None,
        ("Seguir em frente", "nao"),
    ])
    if op == "escoltar":
        g.avancar_periodo()
        g.dizer("Crias do Vazio surgem das sombras na retaguarda da coluna!", "vermelho")
        if g.combate([g.inimigo("cria_vazio") for _ in range(2)]) == "vitoria":
            g.mudar_reputacao(6)
            g.dizer("Um ferreiro entre os refugiados insiste em te recompensar: \"Quando você for até o fim "
                    "disso, eu forjo o que você precisar.\"", "verde")
            g.aliado_final("Os refugiados", "Os refugiados que você salvou trazem armas recém-forjadas e "
                                            "uma bênção coletiva. Você se sente invencível.", "forca", 3)
    elif op == "doar":
        g.perder_ouro(15 + 3 * g.j.nivel)
        g.mudar_reputacao(4)
    else:
        g.dizer("Os olhares das crianças te acompanham por um bom tempo.", "cinza")


@evento(peso=6, cooldown=10, cond=lambda g: g.bioma in ("planicie", "floresta"))
def caravana_atacada(g):
    atacantes = g.grupo(g.sortear(["bandido", "lobo", "cultista"]), n=2)
    g.dizer(f"Gritos à frente! Uma caravana mercante está sob ataque de {tx.descrever_grupo(atacantes)}.",
            "vermelho")
    op = g.menu("O que faz?", [("Correr para ajudar", "ajudar"), ("Esperar e ver no que dá", "esperar")])
    if op == "ajudar":
        if g.combate(atacantes, emboscada="jogador") == "vitoria":
            g.dizer("O mercador te cobre de agradecimentos — e de mercadorias.", "verde")
            g.ganhar_ouro(20 + 5 * g.j.nivel)
            g.dar(g.sortear(["pocao_vida", "tonico", "bomba_fumaca"]))
            g.mudar_reputacao(4)
    else:
        g.dizer("Quando a poeira baixa, só restam carroças tombadas. Você encontra algumas moedas no chão.", "cinza")
        g.ganhar_ouro(g.rng.randint(5, 12))
        g.mudar_reputacao(-2)


# ---------------------------------------------------------------------- eventos ativados por rumores
@evento(peso=35, cooldown=2, cond=lambda g: g.rumor_aqui("tesouro_escondido"))
def tesouro_escondido(g):
    g.consumir_rumor("tesouro_escondido")
    g.dizer("Você reconhece o marco descrito no rumor: uma pedra com três riscos. O chão ao lado parece "
            "remexido há muito tempo.", "amarelo")
    if g.chance(0.2):
        g.dizer("Você cava... e não há nada. Só uma bota velha e a sensação de ter sido feito de bobo.", "cinza")
        return
    if g.chance(0.35):
        g.dizer("Algo guarda o tesouro!", "vermelho")
        if g.combate(g.grupo(n=1, bonus=1)) != "vitoria":
            return
    g.dizer("Um cofre de ferro! Dentro, ouro antigo e uma peça bem cuidada.", "verde+negrito")
    g.ganhar_ouro(30 + 8 * g.j.nivel)
    g.oferecer_equip(gerar_equip(g.rng, g.j.classe, g.j.nivel + 1, qualidade=1))


@evento(peso=35, cooldown=2, cond=lambda g: g.rumor_aqui("fera_lendaria"))
def fera_lendaria(g):
    r = g.consumir_rumor("fera_lendaria")
    fam = r.get("familia") or g.sortear(BIOMAS[g.bioma]["familias"])
    e = g.inimigo(fam, afixo=g.sortear(["anciao", "robusto", "feroz"]), nome_unico=r.get("nome"), bonus=1)
    g.dizer(f"O rumor era verdade. {e.nome} está diante de você, maior do que qualquer história contava.",
            "vermelho+negrito")
    if g.combate([e]) == "vitoria":
        g.dizer("Você corta um troféu da criatura. Vai valer muito em qualquer vila.", "verde")
        g.ganhar_ouro(25 + 5 * g.j.nivel)
        g.mudar_reputacao(4)
        g.oferecer_equip(gerar_equip(g.rng, g.j.classe, g.j.nivel, qualidade=1))


@evento(peso=35, cooldown=2, cond=lambda g: g.rumor_aqui("mercador_raro"))
def mercador_raro(g):
    g.consumir_rumor("mercador_raro")
    g.dizer("Uma tenda de seda roxa no meio do nada. O mercador que os rumores mencionavam tem olhos dourados "
            "e não pisca.", "magenta")
    itens = [gerar_equip(g.rng, g.j.classe, g.j.nivel + 1, qualidade=2) for _ in range(2)]
    opcoes = [(f"{it['nome']} — {int(it['preco'] * 0.9)} ouro", it) for it in itens if g.j.ouro >= int(it["preco"] * 0.9)]
    opcoes.append(("Pena de Fênix — 120 ouro", "pena") if g.j.ouro >= 120 else None)
    opcoes.append(("Apenas olhar", None))
    esc = g.menu("\"Tudo tem um preço. Alguns preços são em ouro.\"", opcoes)
    if esc == "pena":
        g.perder_ouro(120)
        g.dar("pena_fenix")
    elif esc:
        g.perder_ouro(int(esc["preco"] * 0.9))
        g.oferecer_equip(esc)


# ---------------------------------------------------------------------- legado de partidas anteriores
@evento(contextos=("explorar", "viagem"), peso=80, cooldown=0, unico=True,
        cond=lambda g: g.flag("tumulo") and g.flag("tumulo")["local"] == g.loc["id"])
def tumulo_do_heroi(g):
    t = g.flag("tumulo")
    if t["resultado"] == "corrupcao":  # partidas de antes da 1.16, quando o reino podia cair
        causa = "quando a sombra engoliu o mundo"
    else:
        causa = t["causa"].replace("Você tombou diante de", "diante de").rstrip(".")
    g.dizer(f"Uma lápide tosca, coberta de musgo. Alguém gravou com a ponta de uma faca: \"{t['nome']}, "
            f"{t['nome_classe'].lower()} de nível {t['nivel']}. Caiu {causa}, no dia {t['dia']}.\"", "magenta")
    g.dizer("Este mundo não é o mesmo daquele herói... e ainda assim, aqui está. Ecos atravessam a Fenda.",
            "magenta")
    op = g.menu("O que faz?", [
        ("Prestar homenagem", "honrar"),
        ("Cavar e pegar o que ficou com o corpo", "cavar"),
    ])
    if op == "honrar":
        g.dizer(f"Você se ajoelha. Por um instante, sente a mão de {t['nome']} no seu ombro.", "verde")
        g.ganhar_xp(20 + 10 * g.j.nivel)
        g.mudar_reputacao(2)
        g.aliado_final(f"O espírito de {t['nome']}", f"Uma figura translúcida surge ao seu lado: {t['nome']}. "
                                                      f"\"Desta vez, terminamos juntos.\"", "dano", 0.08)
        return
    arma = t.get("arma")
    if arma and arma.get("classe") == g.j.classe:
        item = gerar_equip(g.rng, g.j.classe, g.j.nivel + 1, slot="arma", qualidade=1)
        item["nome"] = f"{arma['nome'].split(' ')[0]} de {t['nome']}"
    else:
        item = gerar_equip(g.rng, g.j.classe, g.j.nivel + 1, slot="amuleto", qualidade=1)
        item["nome"] = f"Medalhão de {t['nome']}"
    g.dizer("Entre os ossos, algo ainda brilha.", "amarelo")
    g.oferecer_equip(item)
    if g.chance(0.4):
        g.dizer("Um frio sobe pelos seus braços. Os mortos não gostam de ser roubados.", "vermelho")
        g.combate([g.inimigo("espectro", afixo="anciao")])
