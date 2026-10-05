"""Eventos de vila e o gerador de rumores."""

from .. import texto as tx
from ..dados import BIOMAS, FAMILIAS
from .motor import evento

VILA = ("vila",)


# ---------------------------------------------------------------------- rumores
def ouvir_rumor(g, preferir=None):
    """Gera um rumor procedural. Alguns são falsos; outros ativam eventos em lugares específicos."""
    locais = g.mundo["locais"]
    selvagens = [l for l in locais if l["tipo"] in ("selvagem", "covil")]
    covis = [l for l in locais if l["tipo"] == "covil" and not l["guardiao"]["derrotado"]]
    p = g.npc()
    fonte = f"{p['um'].capitalize()} {p['prof']} {p['traco']}"
    tipos = ["tesouro", "fera", "mercador", "lore", "fofoca"]
    if covis:
        tipos += ["fraqueza", "covil", "fraqueza"]
    tipo = preferir if preferir in tipos else g.sortear(tipos)
    falso = g.chance(0.15) and tipo in ("tesouro", "fera", "mercador")

    if tipo == "fraqueza":
        l = g.sortear(covis)
        gu = l["guardiao"]
        g.dizer(f"{fonte} baixa a voz: \"Meu avô enfrentou {tx.aposto(gu['nome'])} e voltou vivo. Ele dizia que a criatura "
                f"tem uma ferida antiga que nunca fechou...\"", "amarelo")
        g.marcar(f"fraqueza:guardiao:{l['id']}")
        g.marcar(f"conhecido:{l['id']}")
        g.dizer(f"(Você causará +25% de dano em {gu['nome']}, que vive em {l['nome']}.)", "verde")
    elif tipo == "covil":
        l = g.sortear(covis)
        g.dizer(f"{fonte} diz: \"Ninguém mais passa por {l['nome']}. Dizem que {tx.aposto(l['guardiao']['nome'])} fez "
                f"seu covil lá.\"", "amarelo")
        g.marcar(f"conhecido:{l['id']}")
        g.rumores.append({"texto": f"{tx.aposto(l['guardiao']['nome'])} vive em {l['nome']}.", "expira": g.dia + 30})
    elif tipo == "tesouro":
        l = g.sortear(selvagens)
        g.dizer(f"{fonte} jura: \"Um contrabandista enterrou seu ouro em {l['nome']}, perto de uma pedra com "
                f"três riscos. Morreu antes de voltar.\"", "amarelo")
        _registrar(g, f"Tesouro enterrado em {l['nome']}.", "tesouro_escondido", l, falso)
    elif tipo == "fera":
        l = g.sortear(selvagens)
        fam = g.sortear(BIOMAS[l["bioma"]]["familias"])
        nome = tx.nome_proprio(g.rng)
        f = FAMILIAS[fam]
        g.dizer(f"{fonte} estremece: \"Já ouviu falar de {nome}? {tx.maiuscula(tx.artigo(f['g'], False))} "
                f"{f['nome']} do tamanho de uma carroça, em {l['nome']}. Os caçadores pagariam bem pela "
                f"cabeça.\"", "amarelo")
        _registrar(g, f"{nome}, {tx.artigo(f['g'], False)} {f['nome']} lendári{'o' if f['g'] == 'm' else 'a'}, "
                      f"em {l['nome']}.", "fera_lendaria", l, falso, familia=fam, nome=nome)
    elif tipo == "mercador":
        l = g.sortear(selvagens)
        g.dizer(f"{fonte} comenta: \"Vi uma tenda de seda roxa em {l['nome']}. O vendedor tinha olhos de ouro "
                f"e coisas que não se acham em mercado nenhum.\"", "amarelo")
        _registrar(g, f"Um mercador estranho em {l['nome']}.", "mercador_raro", l, falso)
    elif tipo == "lore":
        a = g.antagonista
        g.dizer(f"{fonte} conta a velha história de {a['nome']}, {a['origem']}. Dizem que ele ainda sente "
                f"falta de quem foi.", "amarelo")
        g.ganhar_xp(5)
    else:
        fofoca = g.sortear([
            "o padeiro está traindo a mulher com a irmã do moleiro",
            "a cerveja daqui é aguada desde que o dono novo chegou",
            "um bode falou na feira semana passada. Disse só uma palavra, mas ninguém concorda qual",
            "o capitão da guarda tem medo de galinhas",
            "o velho do moinho é, na verdade, três crianças dentro de um casaco",
        ])
        g.dizer(f"{fonte} jura que {fofoca}. Útil? Não. Divertido? Muito.", "cinza")


def _registrar(g, texto, evento_id, local, falso, **dados):
    rumor = {"texto": texto, "evento": None if falso else evento_id, "local": local["id"],
             "expira": g.dia + 6}
    rumor.update(dados)
    g.rumores.append(rumor)
    g.marcar(f"conhecido:{local['id']}")
    if not falso:
        g.impulsos[evento_id] = 3


# ---------------------------------------------------------------------- eventos de vila
@evento(contextos=VILA, peso=8, cooldown=8)
def briga_de_taverna(g):
    g.dizer("Uma caneca voa pela taverna. Dois grandalhões se engalfinham e logo metade do salão está "
            "envolvida.", "amarelo")
    op = g.menu("O que faz?", [
        ("Separar a briga (Força)", "separar"),
        ("Entrar na briga por diversão", "entrar"),
        ("Aproveitar a confusão para pegar moedas do balcão", "roubar"),
        ("Sair de fininho", "nao"),
    ])
    if op == "separar":
        if g.teste("forca", 13):
            g.dizer("Você levanta um em cada mão. O taverneiro te serve de graça a noite toda.", "verde")
            g.mudar_reputacao(3)
            g.curar(10)
        else:
            g.dizer("Você leva um soco que faz o mundo girar.", "vermelho")
            g.ferir(6)
    elif op == "entrar":
        g.dizer("Socos, cadeiras, risadas. No fim, todos dividem uma rodada.", "verde")
        g.ferir(4)
        g.ganhar_xp(8)
    elif op == "roubar":
        if g.teste("destreza", 12):
            g.ganhar_ouro(12 + 2 * g.j.nivel)
            g.mudar_reputacao(-2)
        else:
            g.dizer("O taverneiro te vê. Você é expulso a vassouradas.", "vermelho")
            g.mudar_reputacao(-4)


@evento(contextos=VILA, peso=5, cooldown=16)
def festival(g):
    motivo = g.sortear(["da colheita", "do santo padroeiro", "da primeira neve", "dos lampiões"])
    g.dizer(f"A vila está em festa: é o festival {motivo}! Música, comida e jogos por toda a praça.", "amarelo")
    op = g.menu("O que faz?", [
        ("Comer e dançar até tarde", "festejar"),
        ("Participar do torneio de força (Força)", "torneio"),
        ("Visitar a tenda da cartomante", "cartomante"),
    ])
    if op == "festejar":
        g.curar(g.j.max_hp)
        g.dizer("Você não se diverte assim há muito tempo.", "verde")
        g.avancar_periodo()
    elif op == "torneio":
        if g.teste("forca", 13):
            g.dizer("Você levanta o barril mais pesado e ganha uma coroa de flores (e um prêmio).", "verde")
            g.ganhar_ouro(25)
            g.mudar_reputacao(2)
        else:
            g.dizer("O barril vence.", "cinza")
    else:
        ouvir_rumor(g, preferir="fraqueza")


@evento(contextos=VILA, peso=lambda g: 3 + g.corrupcao // 10, cooldown=12, cond=lambda g: g.corrupcao >= 20)
def pregador_do_vazio(g):
    a = g.antagonista
    g.dizer(f"Na praça, um homem de olhos fundos grita para a multidão: \"{tx.maiuscula(a['curto'])} não é "
            f"o fim, é o começo! Abram-se ao Vazio!\" Algumas pessoas escutam com atenção demais.", "magenta")
    op = g.menu("O que faz?", [
        ("Desmascarar o pregador diante de todos (Carisma)", "debater"),
        ("Segui-lo depois do sermão", "seguir"),
        ("Ignorar", "nao"),
    ])
    if op == "debater":
        if g.teste("carisma", 13):
            g.dizer("Você expõe as contradições dele. A multidão o expulsa da vila.", "verde")
            g.mudar_reputacao(4)
            g.corromper(-2)
        else:
            g.dizer("A multidão vaia — você.", "vermelho")
            g.mudar_reputacao(-2)
    elif op == "seguir":
        g.dizer("Ele te leva até um porão onde outros cultistas se reúnem.", "vermelho")
        if g.combate([g.inimigo("cultista"), g.inimigo("cultista", afixo="corrompido")]) == "vitoria":
            g.corromper(-4)
            g.mudar_reputacao(5)


@evento(contextos=VILA, peso=50, cooldown=2, cond=lambda g: g.semente("familia_grata")
        and g.semente("familia_grata")["dados"]["vila"] == g.loc["id"])
def familia_grata(g):
    d = g.colher("familia_grata")
    g.dizer(f"Uma criança corre e abraça suas pernas: é {d['nome']}! Atrás vêm os pais, chorando e rindo.",
            "verde")
    g.dizer("\"Não temos muito, mas isto é seu.\"", "verde")
    g.ganhar_ouro(20 + 3 * g.j.nivel)
    g.dar("pocao_vida", 2)
    g.mudar_reputacao(3)
    g.aliado_final(f"A família de {d['nome']}", f"Você ouve, de muito longe, a voz de {d['nome']} gritando seu "
                                                f"nome. Parece bobo, mas te enche de coragem.", "forca", 2)


@evento(contextos=VILA, peso=6, cooldown=12)
def mendigo_misterioso(g):
    g.dizer("Um mendigo coberto de trapos estende a mão. Os olhos dele são estranhamente lúcidos.", "amarelo")
    op = g.menu("O que faz?", [
        ("Dar 5 moedas", "dar") if g.j.ouro >= 5 else None,
        ("Pagar uma refeição para ele", "refeicao") if g.j.ouro >= 10 else None,
        ("Ignorar", "nao"),
    ])
    if op == "nao":
        return
    g.perder_ouro(5 if op == "dar" else 10)
    if op == "refeicao" or g.chance(0.4):
        g.dizer("Ele sorri. \"Gentileza com quem nada tem. Rara.\" Quando você pisca, ele sumiu. Em seu bolso, "
                "algo que não estava lá.", "magenta")
        g.marcar("bencao_fenix")
        g.dizer("(Você sente que, se cair, poderá se erguer mais uma vez.)", "amarelo")
    else:
        g.dizer("\"Obrigado, viu.\" Ele vai direto para a taverna.", "cinza")
    g.mudar_reputacao(1)


@evento(contextos=VILA, peso=lambda g: 5 + max(0, -g.j.reputacao) // 4, cooldown=10,
        cond=lambda g: g.j.reputacao <= -10)
def guarda_desconfiado(g):
    g.dizer("Dois guardas te cercam. \"Ouvimos histórias sobre você. Multa por perturbação da ordem — ou uma "
            "noite na cela.\"", "vermelho")
    multa = 15 + 3 * g.j.nivel
    op = g.menu("O que faz?", [
        (f"Pagar a multa ({multa})", "pagar") if g.j.ouro >= multa else None,
        ("Argumentar (Carisma)", "argumentar"),
        ("Passar a noite na cela", "cela"),
    ])
    if op == "pagar":
        g.perder_ouro(multa)
    elif op == "argumentar" and g.teste("carisma", 12):
        g.dizer("\"Tá, tá. Mas estamos de olho.\"", "cinza")
    else:
        g.dizer("A cela é úmida e cheira mal. Pelo menos é segura.", "cinza")
        g.descansar(0.5)
        g.novo_dia()


@evento(contextos=VILA, peso=6, cooldown=14)
def pedido_de_socorro(g):
    p = g.npc()
    l = g.sortear([x for x in g.mundo["locais"] if x["tipo"] in ("selvagem", "covil")])
    g.dizer(f"{p['nome']}, {p['um']} {p['prof']} {p['traco']}, te puxa pelo braço: \"Meu irmão foi para "
            f"{l['nome']} há três dias e não voltou. Por favor!\"", "amarelo")
    if g.menu("Aceitar?", [("Prometer procurar", True), ("Dizer que não pode", False)]):
        cid = g.novo_id()
        fam = g.sortear(BIOMAS[l["bioma"]]["familias"])
        g.contratos.append({"id": cid, "tipo": "alvo", "local": l["id"], "familia": fam,
                            "nome": tx.nome_proprio(g.rng), "chave": f"alvo:{cid}",
                            "ouro": 20 + 8 * g.j.nivel, "xp": 30 + 10 * g.j.nivel,
                            "desc": f"Encontrar o irmão de {p['nome']} em {l['nome']} (algo o pegou)."})
        g.dizer("Adicionado ao diário.", "cinza")
