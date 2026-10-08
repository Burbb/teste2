"""Eventos ligados a biomas e ao clima."""

from .. import texto as tx
from ..itens import gerar_equip
from .motor import evento


def _bioma(*nomes):
    return lambda g: g.bioma in nomes


# ---------------------------------------------------------------------- floresta
@evento(peso=7, cooldown=14, cond=_bioma("floresta"))
def circulo_de_fadas(g):
    g.dizer("Um anel perfeito de cogumelos vermelhos. Dentro dele, a grama é mais verde e uma música sem "
            "instrumentos parece vir de lugar nenhum.", "magenta")
    op = g.menu("O que faz?", [
        ("Entrar no círculo e dançar", "dancar"),
        ("Oferecer algo em troca de um favor (uma poção)", "trocar") if g.j.tem("pocao_vida") else None,
        ("Chutar os cogumelos", "chutar"),
        ("Afastar-se devagar", "nao"),
    ])
    if op == "dancar":
        if g.teste("vontade", 13):
            g.dizer("Você dança uma noite inteira que dura um minuto. Ao sair, se sente leve como pluma.", "verde")
            g.bonus_permanente("agi", 1)
            g.j.recalcular()
        else:
            g.dizer("Você dança... e dança... quando para, o sol mudou de lugar. Você perdeu horas — e um pouco "
                    "de si.", "vermelho")
            g.avancar_periodo()
            g.ferir(g.j.max_hp * 0.15, " de exaustão")
    elif op == "trocar":
        g.j.consumiveis["pocao_vida"] -= 1
        g.dizer("A poção desaparece no ar. Em seu lugar, uma risadinha e um presente.", "magenta")
        g.oferecer_equip(gerar_equip(g.rng, g.j.classe, g.j.nivel, slot="amuleto", qualidade=1))
    elif op == "chutar":
        g.dizer("A música vira um guincho. Pequenas criaturas de dentes afiados saem do chão!", "vermelho")
        grupo = g.grupo("rato", n=3)
        for e in grupo:
            e.nome = e.nome.replace("Rato Gigante", "Duende Furioso")
            e.tracos = ["fera"]
        g.combate(grupo)


@evento(peso=6, cooldown=12, cond=_bioma("floresta", "planicie"))
def colmeia_selvagem(g):
    g.dizer("Um zumbido grave vem de uma árvore oca. Mel escorre pela casca: uma colmeia selvagem enorme.",
            "amarelo")
    op = g.menu("O que faz?", [
        ("Usar fumaça e coletar o mel com calma (Destreza)", "mel"),
        ("Queimar a colmeia com magia", "fogo") if g.j.classe == "mago" else None,
        ("Deixar as abelhas em paz", "nao"),
    ])
    if op == "nao":
        return
    if op == "fogo" or g.teste("destreza", 12):
        g.dizer("Você enche um frasco de mel dourado. Doce, quente, curativo.", "verde")
        g.curar(g.j.max_hp * 0.2)
        g.dar("pocao_vida")
    else:
        g.dizer("As abelhas acordam de mau humor.", "vermelho")
        g.ferir(5 + g.j.nivel * 2, " com as ferroadas")


# ---------------------------------------------------------------------- pântano
@evento(peso=8, cooldown=12, cond=lambda g: g.bioma == "pantano" or g.clima == "nevoa")
def luzes_fantasmas(g):
    g.dizer("Luzes azuladas flutuam sobre a água, uma atrás da outra, como se formassem um caminho.", "magenta")
    op = g.menu("O que faz?", [("Seguir as luzes", "seguir"), ("Resistir ao chamado (Vontade)", "resistir")])
    if op == "resistir" and g.teste("vontade", 12):
        g.dizer("Você desvia o olhar. As luzes se apagam, decepcionadas. Ao longe você ouve um corpo cair na "
                "água — não o seu.", "verde")
        g.ganhar_xp(10)
        return
    g.dizer("Você segue as luzes, passo a passo, para dentro do charco...", "magenta")
    if g.chance(0.5):
        g.dizer("Elas param sobre um barco afundado. Entre as tábuas podres, um pequeno tesouro.", "verde")
        g.ganhar_ouro(20 + 4 * g.j.nivel)
        if g.chance(0.5):
            g.oferecer_equip(gerar_equip(g.rng, g.j.classe, g.j.nivel))
    else:
        g.dizer("A água sobe até o peito. Mãos frias agarram suas pernas!", "vermelho+negrito")
        g.combate(g.grupo("afogado", n=2), emboscada="inimigo")


@evento(peso=6, cooldown=14, cond=_bioma("pantano"))
def cabana_da_bruxa(g):
    g.dizer("Uma cabana sobre palafitas, com caveiras de pássaros penduradas. Uma velha de olhos leitosos "
            "acena da janela. \"Entra, querid@. Não mordo... muito.\"".replace("@", "o" if g.chance(0.5) else "a"),
            "magenta")
    op = g.menu("O que faz?", [
        ("Comprar um elixir (20 ouro)", "elixir") if g.j.ouro >= 20 else None,
        ("Pedir que ela leia seu futuro", "futuro"),
        ("Atacar a bruxa", "atacar"),
        ("Ir embora", "nao"),
    ])
    if op == "elixir":
        g.perder_ouro(20)
        if g.chance(0.8):
            g.dizer("O elixir tem gosto de terra e hortelã. Funciona.", "verde")
            g.bonus_permanente("max_hp", 4)
            g.j.recalcular()
            g.curar(g.j.max_hp * 0.4)
        else:
            g.dizer("Você passa a tarde inteira com dor de barriga. A bruxa ri muito.", "vermelho")
            g.ferir(g.j.max_hp * 0.12, " de cólica")
    elif op == "futuro":
        from .vila import ouvir_rumor
        g.dizer("Ela joga ossinhos sobre a mesa e franze a testa...", "magenta")
        ouvir_rumor(g, preferir="fraqueza")
    elif op == "atacar":
        g.mudar_reputacao(-2)
        g.combate([g.inimigo("bruxa_brejo", afixo="anciao")])


# ---------------------------------------------------------------------- montanha
@evento(peso=7, cooldown=10, cond=lambda g: g.bioma == "montanha" and g.clima in ("neve", "tempestade", "limpo",
                                                                                   "nublado"))
def avalanche(g):
    g.dizer("Um estrondo seco vem de cima. A encosta inteira começa a deslizar!", "vermelho+negrito")
    if g.teste("destreza", 13):
        g.dizer("Você se joga atrás de uma rocha no último segundo. A neve passa rugindo.", "verde")
        if g.chance(0.4):
            g.dizer("Quando tudo acalma, a avalanche revelou a entrada de uma pequena gruta com restos de um "
                    "acampamento antigo.", "verde")
            g.ganhar_ouro(15 + 3 * g.j.nivel)
            g.dar("tonico")
    else:
        g.dizer("Você é arrastado encosta abaixo.", "vermelho")
        g.ferir(g.j.max_hp * 0.25, " na queda")


@evento(peso=6, cooldown=14, cond=_bioma("montanha"))
def ninho_de_grifo(g):
    g.dizer("Num platô, um ninho de galhos do tamanho de uma carroça. Dentro: três ovos dourados. "
            "Nenhum sinal da mãe... por enquanto.", "amarelo")
    op = g.menu("O que faz?", [
        ("Pegar um ovo (valem uma fortuna)", "pegar"),
        ("Esperar a mãe e tentar fazer amizade (Patrulheiro)", "domar") if g.j.spec == "patrulheiro" else None,
        ("Deixar o ninho em paz", "nao"),
    ])
    if op == "pegar":
        if g.teste("destreza", 12):
            g.dizer("Você desce o platô com o ovo enrolado na capa. Um grito furioso ecoa às suas costas, mas "
                    "tarde demais.", "verde")
            g.ganhar_ouro(40 + 6 * g.j.nivel)
            g.mudar_reputacao(-1)
        else:
            g.dizer("Uma sombra cobre o sol. A mãe voltou.", "vermelho+negrito")
            g.combate([g.inimigo("grifo", afixo="feroz")], emboscada="inimigo")
    elif op == "domar":
        g.dizer("Você espera imóvel até a mãe pousar, de mãos abertas e olhos baixos, como os patrulheiros ensinam.",
                "verde")
        if g.teste("percepcao", 13):
            g.dizer("Ela te encara por longos segundos, depois abaixa a cabeça e deixa você tocar suas penas. Não é sua, "
                    "nunca vai ser, mas hoje vocês se entendem. Quando ela levanta voo, uma pena solta fica nas suas mãos.",
                    "verde+negrito")
            g.dar("pena_fenix")
            g.ganhar_xp(25)
        else:
            g.dizer("Ela não está a fim de conversa.", "vermelho")
            g.combate([g.inimigo("grifo")])


# ---------------------------------------------------------------------- planície
@evento(peso=6, cooldown=14, cond=_bioma("planicie"))
def espantalho(g):
    g.dizer("Um espantalho no meio de um milharal. Você poderia jurar que, há um momento, ele estava "
            "olhando para o outro lado.", "magenta")
    op = g.menu("O que faz?", [("Examinar de perto", "examinar"), ("Atear fogo nele", "fogo"),
                               ("Passar longe", "nao")])
    if op == "nao":
        return
    if op == "fogo" or g.chance(0.5):
        if op == "fogo":
            g.dizer("A palha pega fogo e algo lá dentro GRITA.", "vermelho")
        e = g.inimigo("ent_jovem", afixo="corrompido" if g.loc["perigo"] >= 4 else "feroz")
        e.nome = "Espantalho Possuído"
        e.desc = "um espantalho possuído"
        if op == "fogo":
            e.hp = int(e.hp * 0.7)
        g.combate([e], emboscada=None if op == "fogo" else "inimigo")
    else:
        g.dizer("É só palha e um chapéu velho. No bolso do casaco, porém, há um bilhete: \"não deixe ele "
                "descer do poste\". E algumas moedas.", "cinza")
        g.ganhar_ouro(8)


@evento(peso=6, cooldown=12, cond=_bioma("planicie", "floresta"))
def fazenda_em_apuros(g):
    g.dizer("Um fazendeiro corre até você, desesperado: \"Os lobos! Todo dia levam um carneiro. Pago o que "
            "puder!\"", "amarelo")
    op = g.menu("O que faz?", [("Ajudar", "ajudar"), ("Recusar", "nao")])
    if op == "ajudar":
        if g.combate(g.grupo("lobo")) == "vitoria":
            g.dizer("A família inteira te recebe com pão quente e queijo. Você come até se fartar.", "verde")
            g.ganhar_ouro(10 + 2 * g.j.nivel)
            g.dar_provisoes(3)
            g.curar(g.j.max_hp * 0.2)
            g.mudar_reputacao(3)


# ---------------------------------------------------------------------- ruínas
@evento(peso=8, cooldown=8, cond=_bioma("ruinas", "cidadela"))
def armadilha_antiga(g):
    tipo = g.sortear(["lâminas que saltam das paredes", "um piso que cede sobre estacas",
                      "dardos disparados por bocas de pedra", "um gás esverdeado"])
    g.dizer(f"Um clique sob sua bota. {tipo[0].upper() + tipo[1:]}!", "vermelho")
    if g.teste("destreza", 12):
        g.dizer("Seus reflexos te salvam por um fio.", "verde")
        g.ganhar_xp(8)
    else:
        g.ferir(6 + 3 * g.j.nivel, " na armadilha")
    if g.chance(0.4):
        g.dizer("Atrás da armadilha, uma câmara intocada há séculos.", "verde")
        g.ganhar_ouro(15 + 5 * g.j.nivel)


@evento(peso=7, cooldown=14, cond=_bioma("ruinas"))
def biblioteca_ruida(g):
    g.dizer("Uma biblioteca de teto desabado. A maioria dos livros virou pó, mas uma estante está protegida "
            "por runas ainda acesas.", "azul")
    op = g.menu("O que faz?", [
        ("Decifrar as runas (Arcano)", "runas"),
        ("Quebrar a proteção na força", "forca"),
        ("Ir embora", "nao"),
    ])
    if op == "nao":
        return
    if op == "runas":
        cd = 11 if g.j.classe == "mago" else 15
        if g.teste("arcano", cd):
            g.dizer("As runas se apagam com respeito. Os livros contêm conhecimento de verdade.", "verde")
            if g.j.classe == "mago":
                g.bonus_permanente("poder", 2)
                g.bonus_permanente("max_rec", 5)
                g.j.recalcular()
            g.ganhar_xp(20 + 5 * g.j.nivel)
        else:
            g.dizer("As runas explodem em faíscas.", "vermelho")
            g.ferir(5 + 2 * g.j.nivel)
    else:
        grupo = g.grupo("espectro", n=1 if g.nivel_local() <= 2 else 2)
        g.dizer(tx.concordar("A proteção estoura e acorda {o guardião|os guardiões} da biblioteca.", grupo), "vermelho")
        g.combate(grupo)


@evento(peso=6, cooldown=14, cond=_bioma("ruinas"))
def golem_adormecido(g):
    g.dizer("Um golem de pedra coberto de musgo bloqueia o corredor, imóvel. No peito, uma gema brilha "
            "fracamente.", "amarelo")
    op = g.menu("O que faz?", [
        ("Arrancar a gema (Destreza)", "gema"),
        ("Passar pelo vão entre as pernas dele (Destreza)", "passar"),
        ("Acordá-lo e lutar", "lutar"),
        ("Voltar por onde veio", "nao"),
    ])
    if op == "nao":
        return
    if op in ("gema", "passar") and g.teste("destreza", 13 if op == "gema" else 10):
        if op == "gema":
            g.dizer("A gema sai com um estalo. O golem desmorona em pedregulhos.", "verde")
            g.ganhar_ouro(35 + 6 * g.j.nivel)
        else:
            g.dizer("Você passa sem um ruído. Do outro lado, um baú esquecido.", "verde")
            g.dar(g.sortear(["pocao_vida", "tonico", "bomba_fumaca"]))
        return
    g.dizer("Os olhos do golem se acendem.", "vermelho+negrito")
    g.combate([g.inimigo("golem")])


# ---------------------------------------------------------------------- clima
@evento(peso=10, cooldown=10, cond=lambda g: g.clima in ("chuva", "tempestade", "neve"))
def abrigo_da_tempestade(g):
    g.dizer("O tempo piora de vez. Você encontra uma caverna seca e entra para se abrigar.", "cinza")
    if g.chance(0.35):
        dono = "um urso pardo" if g.bioma != "pantano" else "um sapo-touro do tamanho de um cavalo"
        g.dizer(f"Você não é o único com essa ideia: {dono} acorda no fundo da caverna.", "vermelho")
        if g.j.spec == "patrulheiro" and g.teste("percepcao", 12):
            g.dizer("Você fala baixo, se move devagar. O animal te aceita como companhia até a chuva passar.",
                    "verde")
            g.curar(g.j.max_hp * 0.15)
            return
        fam = "javali" if g.bioma != "pantano" else "sapo"
        e = g.inimigo(fam, afixo="robusto")
        if fam == "javali":
            e.nome = "Urso Pardo"
            e.desc = "um urso pardo"
        g.combate([e])
    else:
        g.dizer("Você acende uma fogueira e espera. Nas paredes, desenhos antigos de caçadores e feras.", "cinza")
        g.curar(g.j.max_hp * 0.1)
        if g.chance(0.4):
            g.dizer("Atrás de uma pedra solta, alguém escondeu provisões há muito tempo.", "verde")
            g.dar(g.sortear(["pocao_vida", "tonico", "antidoto"]))


@evento(peso=8, cooldown=12, cond=lambda g: g.clima == "nevoa" or (g.noite and g.bioma == "ruinas"))
def sussurros_na_nevoa(g):
    g.dizer("Na névoa, uma figura translúcida caminha ao seu lado. \"Me ajude a lembrar meu nome...\"",
            "magenta")
    op = g.menu("O que faz?", [
        ("Conversar com o espírito (Vontade)", "falar"),
        ("Libertá-lo com uma prece (Paladino)", "prece") if g.j.spec == "paladino" else None,
        ("Prender o espírito à sua vontade (Necromante)", "prender") if g.j.spec == "necromante" else None,
        ("Ignorar e apertar o passo", "nao"),
    ])
    if op == "prece":
        g.dizer("Você reza. O espírito sorri, se lembra, e se dissolve em luz.", "amarelo")
        g.ganhar_xp(25)
        g.mudar_reputacao(2)
    elif op == "prender":
        g.dizer("O espírito grita enquanto é arrastado para dentro do seu cajado. Seu poder cresce.", "magenta")
        g.bonus_permanente("poder", 2)
        g.j.recalcular()
        g.mudar_reputacao(-2)
    elif op == "falar":
        if g.teste("vontade", 12):
            g.dizer("Vocês conversam até ele lembrar. Em gratidão, ele aponta onde deixou suas coisas em vida.",
                    "verde")
            g.ganhar_ouro(20 + 3 * g.j.nivel)
        else:
            g.dizer("A voz fica cada vez mais fria. Ele não quer lembrar. Ele quer companhia.", "vermelho")
            g.combate(g.grupo("espectro", n=1))
    else:
        g.dizer("A figura fica para trás. A névoa, não.", "cinza")


# ---------------------------------------------------------------------- cidadela
@evento(peso=10, cooldown=6, cond=_bioma("cidadela"))
def eco_do_vazio(g):
    a = g.antagonista
    g.dizer(f"As paredes mostram cenas como janelas: {a['curto']} jovem, sorrindo; depois ajoelhado diante da "
            f"Fenda; depois algo que não é mais gente.", "magenta")
    if g.teste("vontade", 14):
        g.dizer("Você entende algo sobre seu inimigo. Isso te deixa mais forte.", "verde")
        g.ganhar_xp(30)
    else:
        g.ferir(g.j.max_hp * 0.15, " com a angústia")
