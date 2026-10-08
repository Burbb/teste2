"""Eventos que acontecem durante a noite no acampamento."""

from .. import texto as tx
from .motor import evento

ACAMP = ("acampamento",)


@evento(contextos=ACAMP, peso=14, cooldown=4)
def olhos_na_escuridao(g):
    grupo = g.grupo()
    g.dizer(tx.concordar("Você acorda com um galho estalando. {Um par de olhos reflete a luz da fogueira, na beira|"
                         "Olhos refletem a luz da fogueira, ao redor} do acampamento.", grupo), "vermelho")
    op = g.menu("O que faz?", [
        ("Pegar a arma e lutar", "lutar"),
        (tx.concordar("Atiçar a fogueira para assustá{-los} (Vontade)", grupo), "fogo"),
    ])
    if op == "fogo":
        g.dizer("Você joga galhos secos no fogo, que sobe alto e estala.", "amarelo")
        if all("fera" in e.tracos for e in grupo):
            if g.teste("vontade", 12):
                g.dizer(tx.concordar("Os olhos recuam{|, um a um,} e somem na mata. Bichos respeitam o fogo.", grupo),
                        "verde")
                return
            g.dizer(tx.concordar("A fome fala mais alto que o medo. {Eles} {avança|avançam}.", grupo), "vermelho")
        elif g.teste("vontade", 14):
            # Gente (e coisa pior) não foge de fogueira, mas a luz mostra onde cada um está.
            g.dizer(tx.concordar("{Eles} não {foge|fogem} do fogo, mas a luz {os} denuncia: você {os} vê antes do "
                                 "primeiro passo.", grupo), "verde")
            g.combate(grupo, emboscada="jogador")
            return
        else:
            g.dizer(tx.concordar("A chama sobe, mas {eles} não {é bicho|são bichos}. {Avança|Avançam} com o fogo "
                                 "refletido nos olhos.", grupo), "vermelho")
        g.combate(grupo, emboscada="inimigo" if g.chance(0.25) else None)
        return
    g.combate(grupo, emboscada="inimigo" if g.chance(0.4) else None)


@evento(contextos=ACAMP, peso=7, cooldown=8)
def visitante_misterioso(g):
    p = g.npc()
    g.dizer(f"Uma figura encapuzada se aproxima e pede para se aquecer. É {p['um']} {p['prof']} {p['traco']}.",
            "amarelo")
    op = g.menu("O que faz?", [("Dividir a fogueira e a comida", "dividir"), ("Mandar embora", "mandar")])
    if op == "mandar":
        g.dizer("A figura some na escuridão sem dizer nada.", "cinza")
        return
    if g.chance(0.25):
        g.dizer("Você cochila. Quando acorda, o visitante sumiu — junto com parte do seu ouro.", "vermelho")
        g.perder_ouro(10 + 3 * g.j.nivel)
        return
    from .vila import ouvir_rumor
    g.dizer(f"{p['nome']} conta histórias até tarde.", "verde")
    ouvir_rumor(g)
    if g.chance(0.4):
        g.dizer("Antes de partir ao amanhecer, deixa um presente ao lado do seu saco de dormir.", "verde")
        g.dar(g.sortear(["pocao_vida", "tonico", "antidoto", "bomba_fumaca"]))


@evento(contextos=ACAMP, peso=7, cooldown=8)
def ladrao_noturno(g):
    g.dizer("Um farfalhar perto da sua mochila...", "amarelo")
    if g.teste("percepcao", 12):
        g.dizer("Você agarra o pulso de um ladrãozinho magricela. Ele implora.", "verde")
        op = g.menu("O que faz?", [("Soltá-lo com um aviso", "soltar"), ("Entregá-lo aos guardas", "entregar")])
        if op == "soltar":
            g.mudar_reputacao(1)
            g.plantar("ladrao_redimido", 8)
        else:
            g.ganhar_ouro(10)
    else:
        g.dizer("De manhã, falta peso na sua bolsa.", "vermelho")
        g.perder_ouro(8 + 3 * g.j.nivel)
        if g.j.classe == "arqueiro":
            g.j.flechas = max(0, g.j.flechas - 5)
            g.dizer("E algumas flechas também!", "vermelho")


@evento(contextos=("explorar", "viagem"), peso=40, cooldown=3, cond=lambda g: g.semente("ladrao_redimido"))
def ladrao_redimido(g):
    g.colher("ladrao_redimido")
    g.dizer("O ladrãozinho que você soltou aparece correndo. \"Tem uma emboscada te esperando à frente! "
            "Por aqui, conheço um atalho.\"", "verde")
    g.ganhar_xp(15)
    g.dar("bomba_fumaca")


@evento(contextos=ACAMP, peso=6, cooldown=10)
def sonho_profetico(g):
    g.dizer("Você sonha com um lugar que nunca viu, mas reconhece.", "magenta")
    vivos = [l for l in g.mundo["locais"] if l["tipo"] == "covil" and not l["guardiao"]["derrotado"]]
    if vivos:
        l = g.sortear(vivos)
        g.dizer(f"{tx.aposto(l['guardiao']['nome'])} dorme em {l['nome']}. No sonho, você vê uma cicatriz antiga na "
                f"criatura — um ponto fraco.", "magenta")
        g.marcar(f"conhecido:{l['id']}")
        if g.teste("vontade", 12):
            g.marcar(f"fraqueza:guardiao:{l['id']}")
            g.dizer("Você acorda lembrando de cada detalhe.", "verde")
        else:
            g.dizer("Ao acordar, os detalhes escorrem da memória.", "cinza")
    else:
        g.dizer(f"No sonho, {g.antagonista['curto']} te espera num trono. Você acorda suando frio.", "magenta")


@evento(contextos=ACAMP, peso=8, cooldown=6, cond=lambda g: g.clima in ("limpo", "nublado"))
def ceu_estrelado(g):
    g.dizer("O céu está limpo e coalhado de estrelas. Por algumas horas, o mundo parece em paz.", "azul")
    g.curar(g.j.max_hp * 0.1)
    if g.chance(0.3):
        g.dizer("Uma estrela cadente risca o céu. Você faz um pedido.", "azul")
        g.ganhar_xp(5 + g.j.nivel)


@evento(contextos=ACAMP, peso=3, cooldown=8, cond=lambda g: g.nivel_local() >= 5)
def sussurros_do_vazio(g):
    g.dizer(f"Uma voz dentro da fogueira, com o timbre de {g.antagonista['curto']}: \"Para que lutar? "
            f"Junte-se a mim e nunca mais terá medo.\"", "magenta+negrito")
    op = g.menu("O que faz?", [("Recusar (Vontade)", "recusar"), ("Ouvir mais um pouco...", "ouvir")])
    if op == "recusar" and g.teste("vontade", 14):
        g.dizer("Você joga terra no fogo. A voz se cala.", "verde")
        g.ganhar_xp(15)
        return
    g.dizer("Você escuta. É fácil escutar. A voz te ensina coisas — e cobra caro.", "magenta")
    stat = "poder" if g.j.classe == "mago" else "atk"
    g.bonus_permanente(stat, 2)
    g.j.base["max_hp"] -= 6  # o preço não tem teto
    g.j.recalcular()
    g.mudar_reputacao(-3)
    g.dizer(f"(+2 {'Poder' if stat == 'poder' else 'Ataque'}, mas −6 de vida máxima: a voz levou um pedaço de você)",
            "magenta")


@evento(contextos=ACAMP, peso=10, cooldown=6, cond=lambda g: g.j.companheiro is not None)
def companheiro_de_vigia(g):
    c = g.j.companheiro
    g.dizer(f"{c['nome']} passa a noite de vigia ao seu lado.", "verde")
    if g.chance(0.5):
        g.dizer(f"No meio da madrugada, {c['nome']} afugenta algo grande que rondava o acampamento. "
                f"Você nem acorda.", "verde")
    g.curar(g.j.max_hp * 0.08)
