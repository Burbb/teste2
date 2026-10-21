"""Sobe o jogo web num cenário preparado, para os testes de navegador (fumaca.mjs).

    python -m tests.navegador.cenarios combate   # mago em luta, com contrato de caça no lugar (FEITO)
    python -m tests.navegador.cenarios titulo    # menu principal com um save de dia para carregar
    python -m tests.navegador.cenarios vila      # guerreiro acha um item raro e abre o mural de contratos (ACHADO, ARMA)
    python -m tests.navegador.cenarios campanha  # menu principal com saves dos dois modos; começar a campanha
    python -m tests.navegador.cenarios baus      # vila com três baús na bolsa (BAUS): a pilha abre inteira
    python -m tests.navegador.cenarios missao    # campanha no Bosque do Moinho, na etapa de seguir o canal
    python -m tests.navegador.cenarios recarga   # título com um save da campanha (Bosque, à noite) e um do mundo gerado
    python -m tests.navegador.cenarios capela    # herói na Capela Afogada (CLASSE, ESPEC, ETAPA, SALA, DESFECHO, NIVEL, PREPARO, LUGAR, SEMENTE, PRISAO, PERIODO, TOCHAS)
    python -m tests.navegador.cenarios retorno   # chegando ao Vau com Ilse resolvida (DESFECHO, DIAS, LODO, YARA)
    python -m tests.navegador.cenarios praca     # depois da resposta a Caspar (POSTURA, YARA, LUGAR); no Vau, abre no fim do capítulo
    python -m tests.navegador.cenarios encruzilhada  # a escolha de especialização, comparando (CLASSE, NIVEL)
    python -m tests.navegador.cenarios covil        # mundo gerado, no covil de um guardião (CLASSE, EVENTO, SEMENTE)
    python -m tests.navegador.cenarios tiro_duplo    # Patrulheiro contra três lobos feridos de jeitos diferentes (NIVEL, VIDAS)
    python -m tests.navegador.cenarios broquel       # Guerreiro nv 4 com o Broquel contra três lobos; repete com/sem o Revide (LUTA, ESPEC, NIVEL)
    python -m tests.navegador.cenarios resgate       # a recuperação: fome ou infecção no Charco, à noite (CLASSE, CAUSA, COMITIVA, CONTRATOS)
    python -m tests.navegador.cenarios abertura      # campanha nova no Vau: a despensa e as orientações (CLASSE, TUTORIAL, MOREL, DESPENSA, VIDA_RATOS)
    python -m tests.navegador.cenarios fogueira      # a comitiva na fogueira e a fome (LUGAR, SALA, CLASSE, COMITIVA, RESERVA, FERIDO, FERA, FOME, PROVISOES, TOCHAS, PERIODO, CLIMA, EXAUSTO)
    python -m tests.navegador.cenarios tutorial      # a segunda parte da abertura guiada (LUGAR, PERIODO, VIDA, REC, OURO, PROVISOES, COMITIVA, PONTOS, ITEM, BAUS, CONTRATO, LUTA, VISTAS, BOLSA, TROCA)
    python -m tests.navegador.cenarios gelo          # Mago com a iniciativa contra um lobo: duas Lanças antes de ele agir (PRISAO, NIVEL, SEMENTE)
    python -m tests.navegador.cenarios aneis         # acha um anel com os dois espaços ocupados (ANEIS=1: um vazio; CHEIA, OURO)
    python -m tests.navegador.cenarios reacoes       # Contra-ataque, espinhos, roubo de vida e o Revide juntos (CONTRA, ESPINHOS, ROUBO, LUTA)
    python -m tests.navegador.cenarios relatorio     # Explorar cai numa luta comum: o relatório e o que vem depois (EVENTO, VEZES, SEMENTE, PERIODO)
    python -m tests.navegador.cenarios muralha       # Guerreiro nv 6, Muralha + Contra-ataque (CONTRA) e o Broquel, contra bandidos e um cultista

Imprime o endereço do servidor na primeira linha e fica no ar até ser encerrado.
"""

import argparse
import os
import random
import sys
import tempfile
import threading
import time

from rpg import comitiva as cm
from rpg.classes import habilidades_ate
from rpg.itens import gerar_equip
from rpg.jogo import Derrota, FimDeJogo, Jogo
from rpg.web.ponte import WebUI
from rpg.web.servidor import Servidor


def espaco_do_desenho(desenho):
    """O espaço de uma peça pelo desenho das bases (itens.py): "gibao" é armadura, "bota" é pes; arma se não achar."""
    from rpg import itens
    if any(i == desenho for bases in itens.ARMADURAS.values() for _, _, i in bases):
        return "armadura"
    return next((slot for slot, por_classe in itens.PECAS.items()
                 if any(i == desenho for bases in por_classe.values() for _, _, i in bases)), "arma")


def vestir_arma(g):
    """ARMA=<desenho> (machado, maca...): a arma vestida passa a ser uma comum com esse desenho (para ver o desenho no
    corpo, na ficha e na comparação). VESTIR=<desenho>[,<desenho>] (gibao,bota...): o mesmo para as outras peças, cada
    uma no seu espaço. Sorteios próprios: sem ARMA e sem VESTIR, o cenário sai igual."""
    if os.environ.get("ARMA"):
        r = random.Random(2)
        g.j.equip["arma"] = next(e for e in iter(lambda: gerar_equip(r, g.j.classe, max(1, g.j.nivel), slot="arma", raridade="comum"), None)
                                 if e["icone"] == os.environ["ARMA"])
    if os.environ.get("VESTIR"):
        r = random.Random(4)
        for desenho in os.environ["VESTIR"].split(","):
            espaco = espaco_do_desenho(desenho)
            g.j.equip[espaco] = next(e for e in iter(lambda: gerar_equip(r, g.j.classe, max(1, g.j.nivel), slot=espaco,
                                                                          raridade="comum"), None) if e["icone"] == desenho)
    if os.environ.get("ARMA") or os.environ.get("VESTIR"):
        g.j.recalcular()


def lugar_por_chave(g, padrao):
    """O lugar de LUGAR (a chave, como "vau_do_turvo"), ou o padrão do cenário. Um LUGAR que sobrou de outro teste no
    terminal ("vila", "selvagem") não trava o cenário: avisa e usa o padrão."""
    chave = os.environ.get("LUGAR", padrao)
    achado = next((l for l in g.mundo["locais"] if l["chave"] == chave), None)
    if achado is None:
        print(f'LUGAR="{chave}" não é um lugar deste mapa; usando {padrao}. (Para limpar no PowerShell: '
              f'Remove-Item Env:LUGAR)', flush=True)
        achado = next(l for l in g.mundo["locais"] if l["chave"] == padrao)
    return achado


def lutar(g, inimigos, **kw):
    """Uma luta preparada antes de o jogo rodar: cair nela leva ao resgate de sempre (o mesmo de Jogo.rodar), e o
    cenário segue dali."""
    try:
        g.combate(inimigos, **kw)
    except Derrota as d:
        g.resgate(d.causa)


def combate(ui):
    g = Jogo(ui, seed=21, pasta_saves=tempfile.mkdtemp())
    ui.jogo = g
    g.iniciar("Jean", "mago")
    loc = next(l for l in g.mundo["locais"] if l["tipo"] == "selvagem" and l["bioma"] == "floresta")
    g.mundo["atual"] = loc["id"]
    loc["visitado"] = True
    g.periodo, g.clima = 1, "limpo"
    cm.recrutar(g, "odete")["aprovacao"] = 30
    g.j.nivel, g.j.spec = 7, "piromante"
    g.j.habilidades = habilidades_ate("mago", "piromante", 7)
    g.j.talentos.update({"ignicao": 1, "brasas": 2})
    g.j.consumiveis["tonico"] = 2
    for semente in range(40):  # uma arma na mochila, para a troca em combate
        it = gerar_equip(random.Random(semente), "mago", 6)
        if it["slot"] in ("arma", "secundaria"):
            g.j.mochila.append(it)
            break
    g.j.base["poder"], g.j.base["max_rec"] = 44, 110
    g.j.recalcular()
    g.j.rec = g.j.max_rec
    # FEITO=2: o javali desta luta fecha o contrato (o espólio mostra o contrato concluído)
    g.contratos.append({"id": 991, "tipo": "caca", "local": loc["id"], "familia": "javali", "total": 3,
                        "feito": int(os.environ.get("FEITO", "1")),
                        "ouro": 60, "xp": 80, "desc": f"Eliminar 3 javalis em {loc['nome']}."})
    ui.cena("Clareira", g.contexto_cena(), "evento")
    g.dizer("Um javali enorme fareja o ar.")
    e = g.inimigo("javali", nivel=2)
    e.hp = e.max_hp = 160
    lobo = g.inimigo("lobo", nivel=1)  # um segundo inimigo, para a luta pedir o alvo
    lobo.hp = lobo.max_hp = 20
    g.j.hp = g.j.max_hp = 400
    lutar(g, [e, lobo])
    try:
        g.rodar()
    except FimDeJogo:
        pass


def titulo(ui):
    from rpg.__main__ import menu_principal
    from rpg.ui import BotUI
    pasta = tempfile.mkdtemp()
    g = Jogo(BotUI(random.Random(1), max_decisoes=10), seed=4, pasta_saves=pasta)
    g.iniciar("Jean", "guerreiro")
    g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["tipo"] == "selvagem")["id"]
    g.periodo, g.clima = 1, "limpo"
    g.salvar(silencioso=True)
    menu_principal(ui, argparse.Namespace(seed=1, saves=pasta, brando=False))


def vila(ui):
    """Guerreiro numa vila: acha um item raro (cartão do saque) e depois abre o mural de contratos. ACHADO=martelo: o
    item achado é um martelo (para conferir o desenho no cartão e no voo ao equipar); ARMA=machado: a arma vestida
    (o cartão "você usa" ao lado). CLASSE (padrão guerreiro): o herói e o achado dessa classe (ACHADO=arco, cajado...).
    ACHADO_ID=<id> (pele_do_penitente...): o achado é esse único do catálogo (itens.UNICOS), no nível 4. VESTIDO=<desenho>
    (calca_couro...): uma peça desse desenho da classe vestida no espaço dela (o cartão "você usa" ao lado do achado)."""
    g = Jogo(ui, seed=8, pasta_saves=tempfile.mkdtemp())
    ui.jogo = g
    g.iniciar("Jean", os.environ.get("CLASSE", "guerreiro"))
    g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["tipo"] == "vila")["id"]
    g.periodo, g.clima = 1, "limpo"
    g.j.ouro = 300
    rng = random.Random(5)
    for _ in range(80):  # algo vestido em quase todo espaço, para o mercado e o Shift terem com o que comparar
        it = gerar_equip(rng, "guerreiro", 2)
        espaco = "anel1" if it["slot"] == "anel" else it["slot"]
        if espaco != "arma" and not g.j.equip.get(espaco):
            g.j.equip[espaco] = it
    g.j.recalcular()
    g.j.hp = g.j.max_hp // 2  # ferido, para a poção da bolsa ter uso
    cm.recrutar(g, "odete")["hp"] -= 5  # com alguém por perto, poção e bandagem perguntam em quem usar
    for _ in range(60):  # um item raro de um espaço que já está ocupado, para comparar
        it = gerar_equip(rng, "guerreiro", 4, qualidade=1)
        if it["slot"] in ("arma", "armadura") and g.j.equip.get(it["slot"]):
            break
    if os.environ.get("ACHADO"):
        it = next(e for e in iter(lambda: gerar_equip(rng, g.j.classe, 4, qualidade=1), None) if e["icone"] == os.environ["ACHADO"])
    if os.environ.get("ACHADO_ID"):
        from rpg import itens
        it = itens.fazer_unico(itens.UNICOS_POR_ID[os.environ["ACHADO_ID"]], 4)
    vestir_arma(g)
    if os.environ.get("VESTIDO"):
        vest = next(e for e in iter(lambda: gerar_equip(rng, g.j.classe, 2), None) if e["icone"] == os.environ["VESTIDO"])
        g.j.equip["anel1" if vest["slot"] == "anel" else vest["slot"]] = vest
        g.j.recalcular()
    ui.cena("Ruínas do caminho", g.contexto_cena(), "evento")
    g.dizer("Entre as pedras, algo reluz.")
    g.oferecer_equip(it)
    g.mural()
    try:
        g.rodar()
    except FimDeJogo:
        pass


def campanha(ui):
    """Menu principal com um save do mundo gerado (brando) e um da campanha (resgate), para criar outra campanha."""
    from rpg.__main__ import menu_principal
    from rpg.ui import BotUI
    pasta = tempfile.mkdtemp()
    g = Jogo(BotUI(random.Random(1), max_decisoes=10), seed=4, pasta_saves=pasta, hardcore=False)
    g.iniciar("Jean", "guerreiro")
    g.salvar(silencioso=True)
    c = Jogo(BotUI(random.Random(1), max_decisoes=10), seed=6, pasta_saves=pasta, hardcore=False)
    c.iniciar("Maria", "arqueiro", "turvo")
    c.salvar(silencioso=True)
    menu_principal(ui, argparse.Namespace(seed=1, saves=pasta, brando=False))


def baus(ui):
    """Guerreiro numa vila com três baús na bolsa (BAUS=n para outra quantidade), numa semente em que saem ao menos dois
    equipamentos (conferida antes com o mesmo estado: o menu da vila sorteia a frase de ambiente e então a pilha abre;
    com menos de três baús, a semente 1). SUPRIMENTO=unguento (um id da bolsa): a primeira semente em que esse
    suprimento sai dos baús, em vez dos dois equipamentos (para ver o desenho dele no quadro e no voo para a bolsa)."""
    from rpg.regras import AMBIENTE_VILA
    from rpg.ui import BotUI, InterfaceGrafica

    def montar(u, seed):
        g = Jogo(u, seed=seed, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Jean", "guerreiro")
        g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["tipo"] == "vila")["id"]
        g.periodo, g.clima = 1, "limpo"
        g.j.nivel = 4
        g.j.consumiveis["bau"] = baus
        return g

    class Conta(InterfaceGrafica, BotUI):
        achados = 0

        def painel(self, tipo, dados):
            Conta.achados += tipo == "achado"
            return True

        def escolher(self, pergunta, opcoes):
            return next(i for i, o in enumerate(opcoes) if o.startswith(("Guardar", "Deixar")))
    baus = int(os.environ.get("BAUS", "3"))
    suprimento = os.environ.get("SUPRIMENTO")
    for seed in range(1, 300 if baus >= 3 or suprimento else 2):
        Conta.achados = 0
        t = montar(Conta(random.Random(1)), seed)
        t.sortear(AMBIENTE_VILA)
        t.usar_consumivel("bau")
        if (t.j.consumiveis.get(suprimento, 0) > 0) if suprimento else Conta.achados >= 2:
            break
    g = montar(ui, seed)
    ui.jogo = g
    try:
        g.rodar()
    except FimDeJogo:
        pass


def missao(ui):
    """Campanha (mago) no Bosque do Moinho, de dia, com a fonte nova já examinada: a missão está na etapa "canal"."""
    from rpg import missoes
    g = Jogo(ui, seed=8, pasta_saves=tempfile.mkdtemp(), hardcore=False)
    ui.jogo = g
    g.iniciar("Jean", "mago", "turvo")
    m = missoes.registro(g, "febre_do_turvo")
    m.update(etapa="canal", cenas=["abertura"], pistas=["agua_do_leste"])
    bosque = next(l for l in g.mundo["locais"] if l["chave"] == "bosque_do_moinho")
    g.mundo["atual"], bosque["visitado"] = bosque["id"], True
    g.periodo, g.clima = 0, "limpo"
    try:
        g.rodar()
    except FimDeJogo:
        pass


def recarga(ui):
    """Título com dois saves para carregar: a campanha no Bosque do Moinho (etapa "capela", noite de chuva, dia 25) e
    um do mundo gerado. Para conferir que o lugar carregado aparece com a tela inteira, antes de qualquer ação."""
    from rpg import missoes
    from rpg.__main__ import menu_principal
    from rpg.ui import BotUI
    pasta = tempfile.mkdtemp()
    c = Jogo(BotUI(random.Random(1), max_decisoes=10), seed=6, pasta_saves=pasta, hardcore=False)
    c.iniciar("Maria", "guerreiro", "turvo")
    missoes.registro(c, "febre_do_turvo").update(etapa="capela", cenas=["abertura"],
                                                  pistas=["agua_do_leste", "represa", "canal_da_capela"])
    bosque = next(l for l in c.mundo["locais"] if l["chave"] == "bosque_do_moinho")
    c.mundo["atual"], bosque["visitado"] = bosque["id"], True
    c.dia, c.periodo, c.clima = 25, 3, "chuva"
    c.salvar(silencioso=True)
    g = Jogo(BotUI(random.Random(1), max_decisoes=10), seed=4, pasta_saves=pasta, hardcore=False)
    g.iniciar("Jean", "mago")
    g.salvar(silencioso=True)
    os.utime(g.caminho_save(), (1, 1))  # o da campanha fica primeiro na lista
    menu_principal(ui, argparse.Namespace(seed=1, saves=pasta, brando=False))


def capela(ui):
    """Herói de nível NIVEL (padrão 5; CLASSE, padrão guerreiro; SEMENTE, padrão 11) na Capela Afogada (ou na chave LUGAR), de manhã, com a
    missão na ETAPA (padrão "sacristia": a nave já vencida) e o que se sabe até ali. PREPARO: "correntes" (soltas),
    "berta" (Berta ouvida e a fita, as correntes ainda presas) ou "pronto" (Berta ouvida, a fita e as correntes: o rito
    disponível). CHEGADA=1: a cena de chegada ainda por ver (com ETAPA=capela, ela abre ao carregar). PRISAO (mago, nível 4 ou mais): o talento Prisão de Gelo já comprado, levando a "prisao" ou a "lanca";
    o resto dos talentos sai igual nas duas, para comparar o mesmo herói. PONTOS: pontos de talento sobrando. PERIODO
    (padrão 0, manhã; 3 é noite) e TOCHAS (padrão: as do começo). SALA: a sala da capela em que se começa (exterior,
    salao, sacristia, ossuario, fundo; padrão: a da etapa). DESFECHO: a guardiã já resolvida. BAU=1: o baú da sacristia
    ainda no canto. LIVRO=0: a sacristia vencida sem ter lido o livro (sem as pistas de Ilse e do Sigilo). Sair do jogo leva ao
    título, com o save."""
    from rpg import dev, missoes, talentos
    from rpg.habilidades import escolher_versao
    from rpg.__main__ import menu_principal
    from rpg.ui import BotUI
    pasta = tempfile.mkdtemp()
    g = Jogo(BotUI(random.Random(1)), seed=int(os.environ.get("SEMENTE", "11")), pasta_saves=pasta, hardcore=False)
    g.iniciar("Jean", os.environ.get("CLASSE", "guerreiro"), "turvo")
    nivel = int(os.environ.get("NIVEL", "5"))
    dev.subir_ate(g, nivel, spec=os.environ.get("ESPEC"))  # já especializado (ESPEC, ou a primeira da classe): o
    # acampamento não para na encruzilhada
    if os.environ.get("PRISAO"):  # a comparação da E6: o mesmo herói, com a Prisão ou com a Lança na mão
        talentos.aprender(g.j, talentos.POR_ID["prisao_gelo"])
        g.j.pontos_talento -= 1
        if os.environ["PRISAO"] == "lanca":
            escolher_versao(g.j, "lanca_gelo", None)
    dev.gastar_talentos(g, random.Random(3))
    g.j.pontos_talento += int(os.environ.get("PONTOS", "0"))  # pontos sobrando, para comprar na árvore
    dev.vestir(g, random.Random(3), nivel)
    g.j.consumiveis["pocao_vida"] = 3
    etapa = os.environ.get("ETAPA", "sacristia")
    ordem = list(missoes.MISSOES["febre_do_turvo"]["etapas"])
    def depois(e):
        return ordem.index(etapa) > ordem.index(e)
    pistas = (["agua_do_leste", "represa", "canal_da_capela"] + (["agua_da_capela"] if depois("capela") else [])
              + ((["marcados"] if os.environ.get("LIVRO") == "0" else ["ilse", "sigilo_do_turvo", "marcados"])
                 if depois("sacristia") else [])  # LIVRO=0: venceu a sacristia sem ler o livro (1.88.0)
              + (["correntes"] if depois("ossuario") else []))
    preparo = os.environ.get("PREPARO", "")
    preparos = ["corpo_solto"] if preparo in ("correntes", "pronto") else []
    if preparo in ("berta", "pronto"):
        pistas += ["verdade_de_ilse", "nome_e_fita"]
        preparos.append("fita")
    cenas = ["abertura"] if os.environ.get("CHEGADA") else ["abertura", "capela_exterior"]  # CHEGADA=1: a cena de fora
    missoes.registro(g, "febre_do_turvo").update(etapa=etapa, cenas=cenas, pistas=pistas,
                                                  preparos=preparos)
    if os.environ.get("SALA"):  # a sala em que se está (1.79.0); sem ela, a da etapa (como num save antigo)
        missoes.registro(g, "febre_do_turvo")["sala"] = os.environ["SALA"]
    if os.environ.get("BAU"):  # o baú da sacristia ainda no canto, por recolher (1.85.0; sem ele, já recolhido)
        missoes.registro(g, "febre_do_turvo")["bau"] = "no_canto"
    if os.environ.get("DESFECHO"):  # a guardiã já resolvida ("descansada" ou "destruida"): a capela toda aberta
        missoes.registro(g, "febre_do_turvo").update(desfecho=os.environ["DESFECHO"], etapa="retorno")
    for chave in ("bosque_do_moinho", "capela_afogada"):
        next(l for l in g.mundo["locais"] if l["chave"] == chave)["visitado"] = True
    g.mundo["atual"] = lugar_por_chave(g, "capela_afogada")["id"]
    g.periodo, g.clima = int(os.environ.get("PERIODO", "0")), "limpo"
    if os.environ.get("TOCHAS"):
        g.j.consumiveis["tocha"] = int(os.environ["TOCHAS"])
    g.ui, ui.jogo = ui, g
    try:
        g.rodar()
    except FimDeJogo:
        pass
    ui.jogo = None
    menu_principal(ui, argparse.Namespace(seed=1, saves=pasta, brando=False))  # depois de Sair: o título, para carregar


def retorno(ui):
    """Guerreiro chegando ao Vau do Turvo com a guardiã resolvida há DIAS dias (padrão 0) pelo DESFECHO (padrão
    "descansada"), com a herança de Berta por receber e um corte para a curandeira. LODO=1: já tem o frasco do lodo
    (a prova contra Caspar); YARA=grupo: Yara anda com ele. Sair leva ao título."""
    from rpg import caspar, missoes, sobrevivencia
    from rpg import comitiva as cm
    from rpg.__main__ import menu_principal
    from rpg.ui import BotUI
    pasta = tempfile.mkdtemp()
    g = Jogo(BotUI(random.Random(1)), seed=12, pasta_saves=pasta, hardcore=False)
    g.iniciar("Jean", "guerreiro", "turvo")
    g.dia, g.periodo, g.clima = 10, 0, "limpo"
    missoes.registro(g, "febre_do_turvo").update(
        etapa="retorno", cenas=["abertura", "capela_exterior"], desfecho=os.environ.get("DESFECHO", "descansada"),
        dia_desfecho=10 - int(os.environ.get("DIAS", "0")), preparos=["corpo_solto", "fita"],
        pistas=["agua_do_leste", "represa", "canal_da_capela", "agua_da_capela", "ilse", "sigilo_do_turvo"])
    g.j.sigilos.append("turvo")
    caspar.sincronizar(g)
    if os.environ.get("LODO"):
        caspar.registro(g)["preparos"].append("lodo")
    if os.environ.get("YARA") == "grupo":
        cm.recrutar(g, "yara")
    for l in g.mundo["locais"]:
        l["visitado"] = l["chave"] != "estrada_de_varn"
    sobrevivencia.ferir(g, "corte")
    g.ui, ui.jogo = ui, g
    try:
        g.rodar()
    except FimDeJogo:
        pass
    ui.jogo = None
    menu_principal(ui, argparse.Namespace(seed=1, saves=pasta, brando=False))


def praca(ui):
    """Guerreiro depois da praça de Caspar: a febre concluída e a decisão POSTURA tomada (padrão "apoiar"; também
    "denunciado", "denuncia_falhou", "calar"). YARA=grupo: Yara anda com ele (e viu a praça); sem YARA, ainda não a
    conhece. LUGAR: onde começa (padrão o Vau; "charco_dos_juncos" para o encontro). Sair leva ao título."""
    from rpg import caspar, missoes
    from rpg import comitiva as cm
    from rpg.__main__ import menu_principal
    from rpg.ui import BotUI
    pasta = tempfile.mkdtemp()
    g = Jogo(BotUI(random.Random(1)), seed=12, pasta_saves=pasta, hardcore=False)
    g.iniciar("Jean", "guerreiro", "turvo")
    g.dia, g.periodo, g.clima = 12, 0, "limpo"
    g.j.nivel = 4
    missoes.registro(g, "febre_do_turvo").update(
        etapa="retorno", cenas=["abertura", "capela_exterior", "retorno", "heranca"], desfecho="descansada",
        dia_desfecho=9, concluida=10, preparos=["corpo_solto", "fita"],
        pistas=["agua_do_leste", "represa", "canal_da_capela", "agua_da_capela", "ilse", "sigilo_do_turvo"])
    g.j.sigilos.append("turvo")
    caspar.sincronizar(g)
    yara = os.environ.get("YARA")
    if yara == "grupo":
        cm.recrutar(g, "yara")
        cm.membro(g, "yara")["desde"] = 5
    postura = os.environ.get("POSTURA", "apoiar")
    caspar.registro(g).update(cenas=["acusacao", "praca"], preparos=["lodo"], desfecho=postura, dia_desfecho=10,
                              concluida=10, yara_na_praca=yara or "desconhecida")
    for l in g.mundo["locais"]:
        l["visitado"] = l["chave"] != "estrada_de_varn"
    g.mundo["atual"] = lugar_por_chave(g, "vau_do_turvo")["id"]
    g.ui, ui.jogo = ui, g
    try:
        g.rodar()
    except FimDeJogo:
        pass
    ui.jogo = None
    menu_principal(ui, argparse.Namespace(seed=1, saves=pasta, brando=False))


def resgate(ui):
    """A recuperação da campanha (E9): CLASSE (padrão mago) no Charco dos Juncos, à noite, com Morel e Odette
    (COMITIVA=0: sozinho). CAUSA=fome (padrão): três dias sem comer, sem provisões, 3 de ouro e pouca vida; a próxima
    noite derruba. CAUSA=infeccao: uma infecção e um corte aberto, um dia de fome (que corta a cura do acampamento) e
    40 de ouro. Acampar leva ao resgate no Vau, na casa de Marta (Pita cuida: a febre do Vau ainda não acabou).
    CONTRATOS=n: n contratos de caça já cumpridos, que pagam na página do Vau depois do resgate. MOREL_DIAS=4: o sétimo
    dia de Morel cai nos dias do resgate (o soldo vem depois de acordar); OURO, o ouro. Sair leva ao título."""
    from rpg.__main__ import menu_principal
    from rpg.ui import BotUI
    pasta = tempfile.mkdtemp()
    g = Jogo(BotUI(random.Random(1)), seed=21, pasta_saves=pasta, hardcore=False)
    g.iniciar("Jean", os.environ.get("CLASSE", "mago"), "turvo")
    g.dia, g.periodo, g.clima = 6, 3, "limpo"
    from rpg import missoes
    missoes.registro(g, "febre_do_turvo").update(etapa="capela", cenas=["abertura"],
                                                 pistas=["agua_do_leste", "represa", "canal_da_capela"])
    if os.environ.get("COMITIVA", "1") != "0":
        cm.recrutar(g, "morel")["dias"] = int(os.environ.get("MOREL_DIAS", "0"))  # 4: o soldo cai no resgate
        cm.recrutar(g, "odete")
    j = g.j
    if os.environ.get("CAUSA", "fome") == "infeccao":
        j.ferimentos += [{"id": "infeccao", "dias": None, "tratado": False}, {"id": "corte", "dias": 4, "tratado": False}]
        j.provisoes, j.fome, j.ouro = 0, 1, 40
        j.recalcular()
        j.hp = 1
    else:
        j.provisoes, j.fome, j.ouro = 0, 3, 3
        j.recalcular()
        j.hp = 2
    if os.environ.get("OURO"):
        j.ouro = int(os.environ["OURO"])
    for l in g.mundo["locais"]:
        l["visitado"] = l["chave"] in ("vau_do_turvo", "charco_dos_juncos", "bosque_do_moinho")
    g.mundo["atual"] = next(l["id"] for l in g.mundo["locais"] if l["chave"] == "charco_dos_juncos")
    for _ in range(int(os.environ.get("CONTRATOS", "0"))):
        c = g.gerar_contrato()
        c["concluido"] = True
        g.contratos.append(c)
    g.ui, ui.jogo = ui, g
    g.autosalvar = True
    try:
        g.rodar()
    except FimDeJogo:
        pass
    ui.jogo = None
    menu_principal(ui, argparse.Namespace(seed=1, saves=pasta, brando=False))


def encruzilhada(ui):
    """Herói da CLASSE (padrão guerreiro) no nível NIVEL (padrão 4), ainda sem especialização, no Charco dos Juncos:
    a encruzilhada abre logo (como no primeiro descanso depois do 4). Depois dela, o jogo segue; Sair leva ao título."""
    from rpg import dev
    from rpg.__main__ import menu_principal
    from rpg.ui import BotUI
    pasta = tempfile.mkdtemp()
    g = Jogo(BotUI(random.Random(1)), seed=11, pasta_saves=pasta, hardcore=False)
    g.iniciar("Jean", os.environ.get("CLASSE", "guerreiro"), "turvo")
    dev.subir_ate(g, int(os.environ.get("NIVEL", "4")), spec=False)
    g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["chave"] == "charco_dos_juncos")["id"]
    g.periodo, g.clima = 0, "limpo"
    g.ui, ui.jogo = ui, g
    try:
        g.encruzilhada_no_descanso()
        g.rodar()
    except FimDeJogo:
        pass
    ui.jogo = None
    menu_principal(ui, argparse.Namespace(seed=1, saves=pasta, brando=False))


def tiro_duplo(ui):
    """Patrulheiro (com o lobo) no nível NIVEL (padrão 5), numa floresta, contra três lobos chamados Alfa, Beta e
    Gama, com a vida em VIDAS (frações, padrão "0.05,1,0.4": Alfa cai com um disparo). Inimigos sem esquiva, para o
    tiro sair onde se espera; a luta segue até o fim e o jogo continua."""
    from rpg import dev
    from rpg.ui import BotUI
    pasta = tempfile.mkdtemp()
    g = Jogo(BotUI(random.Random(1)), seed=11, pasta_saves=pasta, hardcore=False)
    g.iniciar("Jean", "arqueiro", "turvo")
    dev.subir_ate(g, int(os.environ.get("NIVEL", "5")), spec="patrulheiro", animal="lobo")
    loc = next(l for l in g.mundo["locais"] if l["tipo"] == "selvagem" and l["bioma"] == "floresta")
    g.mundo["atual"] = loc["id"]
    loc["visitado"] = True
    g.periodo, g.clima = 1, "limpo"
    g.j.hp, g.j.rec = g.j.max_hp, g.j.max_rec
    g.ui, ui.jogo = ui, g
    ui.cena("Clareira", g.contexto_cena(), "evento")
    inimigos = []
    for nome, frac in zip(("Alfa", "Beta", "Gama"), os.environ.get("VIDAS", "0.05,1,0.4").split(",")):
        e = g.inimigo("lobo", nivel=max(1, g.j.nivel - 1))
        e.nome, e.agi = nome, 0
        e.hp = max(1, int(e.max_hp * float(frac)))
        inimigos.append(e)
    lutar(g, inimigos)
    try:
        g.rodar()
    except FimDeJogo:
        pass


def abertura(ui):
    """Uma campanha nova no Vau (CLASSE, padrão guerreiro; SEMENTE, padrão 7), logo depois da criação: o prólogo, a
    abertura da febre e o pedido do taverneiro (a despensa). TUTORIAL=0 desliga as orientações. MOREL=recrutado,
    recusou ou rumores: Morel já resolvido antes (no grupo; recusado pela bebida; encontrado pela bebida e deixado).
    DESPENSA=adiada: o pedido já foi recusado ("Agora não"). VIDA_RATOS=n: só para conferir a tela, os ratos com n de
    vida (1: um golpe derruba cada um, e a habilidade pode encerrar a luta). Sair leva ao título, com o save."""
    from rpg import abertura as ab
    if os.environ.get("VIDA_RATOS"):
        original = ab._rato

        def rato(g):
            e = original(g)
            e.hp = e.max_hp = int(os.environ["VIDA_RATOS"])
            return e
        ab._rato = rato
    from rpg.__main__ import menu_principal
    pasta = tempfile.mkdtemp()
    g = Jogo(ui, seed=int(os.environ.get("SEMENTE", "7")), pasta_saves=pasta, hardcore=False)
    ui.jogo = g
    g.iniciar("Jean", os.environ.get("CLASSE", "guerreiro"), "turvo")
    ab.comecar(g, os.environ.get("TUTORIAL", "1") != "0")
    morel = os.environ.get("MOREL")
    if morel == "recrutado":
        cm.recrutar(g, "morel")
        g.contagem["morel_na_taverna"] = 1
    elif morel in ("recusou", "rumores"):
        g.contagem["morel_na_taverna"] = 1
    if os.environ.get("DESPENSA") == "adiada":
        g.mundo["abertura"]["despensa"] = "adiada"
    g.periodo, g.clima = 0, "limpo"
    g.autosalvar = True
    g.introducao_campanha()
    try:
        g.rodar()
    except FimDeJogo:
        pass
    ui.jogo = None
    menu_principal(ui, argparse.Namespace(seed=1, saves=pasta, brando=False))


def gelo(ui):
    """Mago de nível NIVEL (padrão 4) com a iniciativa contra um lobo de muita vida e sem esquiva: dois turnos seguidos
    para congelar duas vezes antes de o lobo agir. PRISAO="prisao" leva a Prisão de Gelo (congela sempre); sem ela, a
    Lança de Gelo (35% de congelar; SEMENTE padrão 17: as duas primeiras Lanças congelam). A luta segue até o fim."""
    from rpg import dev, talentos
    from rpg.ui import BotUI
    g = Jogo(BotUI(random.Random(1)), seed=int(os.environ.get("SEMENTE", "17")), pasta_saves=tempfile.mkdtemp(),
             hardcore=False)
    g.iniciar("Jean", "mago", "turvo")
    nivel = int(os.environ.get("NIVEL", "4"))
    dev.subir_ate(g, nivel, spec="piromante")
    if os.environ.get("PRISAO") == "prisao":
        talentos.aprender(g.j, talentos.POR_ID["prisao_gelo"])
        g.j.pontos_talento -= 1
    loc = next(l for l in g.mundo["locais"] if l["tipo"] == "selvagem" and l["bioma"] == "floresta")
    g.mundo["atual"] = loc["id"]
    loc["visitado"] = True
    g.periodo, g.clima = 1, "limpo"
    g.j.hp, g.j.rec = g.j.max_hp, g.j.max_rec
    g.ui, ui.jogo = ui, g
    ui.cena("Clareira", g.contexto_cena(), "evento")
    e = g.inimigo("lobo", nivel=max(1, nivel - 1))
    e.agi = 0
    e.hp = e.max_hp = e.max_hp * 6
    lutar(g, [e], emboscada="jogador")
    try:
        g.rodar()
    except FimDeJogo:
        pass


def covil(ui):
    """Mundo gerado, CLASSE (padrão guerreiro) no nível 1, no covil de um guardião ainda vivo (ou no primeiro lugar do
    tipo LUGAR: vila, selvagem), no PERIODO (0 manhã ... 3 noite; padrão 0). BOLSA: "bandagem=0,pocao_vida=2" acerta a
    bolsa; OURO, o ouro; FERIMENTOS, os do herói; RECOLHER, a chance de cada flecha gasta voltar (1 ou 0). PROTECAO (mendigo, santuario ou 1) dá a proteção; LUTA (uma família: lobo, troll, aranha...) começa uma luta com o
    herói quase sem vida (VIDA, NIVEL_LUTA e QUANTOS mudam isso). Com EVENTO (o nome da função: crianca_perdida, madeira_para_flechas, os_enfermos, odete_na_estrada,
    mendigo_misterioso...), o evento toca antes do menu. EFEITOS e EFEITOS_INIMIGO ("firme:2,guarda:2:0.3": o estado, os turnos e o
    valor) começam a LUTA com esses estados no herói e em cada inimigo (para ver os ícones dos estados na carta);
    HABILIDADES ("passo_agil,...") acrescenta essas habilidades ao herói (para ver o selo de um estado que chega)."""
    from rpg import balanceamento as bal, sobrevivencia
    from rpg.eventos import classe as ev_classe, comitiva as ev_comitiva, comuns as ev_comuns, vila as ev_vila
    g = Jogo(ui, seed=int(os.environ.get("SEMENTE", "8")), pasta_saves=tempfile.mkdtemp(), hardcore=False)
    ui.jogo = g
    g.iniciar("Jean", os.environ.get("CLASSE", "guerreiro"))
    loc = next(l for l in g.mundo["locais"] if l["tipo"] == "covil")
    g.mundo["atual"], loc["visitado"] = loc["id"], True
    g.periodo, g.clima = int(os.environ.get("PERIODO", "0")), "limpo"
    if os.environ.get("LUGAR"):  # outro tipo de lugar: "vila" ou "selvagem" (o primeiro do mapa)
        loc = next(l for l in g.mundo["locais"] if l["tipo"] == os.environ["LUGAR"])
        g.mundo["atual"], loc["visitado"] = loc["id"], True
    for k, v in (x.split("=") for x in os.environ.get("BOLSA", "").split(",") if x):
        g.j.consumiveis[k] = int(v)
    if os.environ.get("OURO"):
        g.j.ouro = int(os.environ["OURO"])
    if os.environ.get("PROTECAO"):  # já com a proteção (a origem: mendigo, santuario, ou 1 para um save antigo)
        g.marcar("bencao_fenix", True if os.environ["PROTECAO"] == "1" else os.environ["PROTECAO"])
    for fid in [f for f in os.environ.get("FERIMENTOS", "").split(",") if f]:  # FERIMENTOS=corte,perna (do herói)
        g.j.ferimentos.append({"id": fid, "dias": sobrevivencia.FERIMENTOS[fid]["dias"], "tratado": False})
        g.j.recalcular()
    if os.environ.get("RECOLHER"):  # RECOLHER=1: toda flecha gasta volta (0: nenhuma), para ver o espólio do arqueiro
        bal.RECOLHER_FLECHA = float(os.environ["RECOLHER"])
    if os.environ.get("LUTA"):  # cai numa luta já quase sem vida, contra um inimigo forte: a proteção se ativa
        g.j.hp = int(os.environ.get("VIDA", "1"))  # VIDA e NIVEL_LUTA: uma luta comum (a teia da aranha, por exemplo)
        ui.cena(loc["nome"], g.contexto_cena(), "evento")
        g.dizer("Um vulto enorme sai da névoa.")
        for hid in [h for h in os.environ.get("HABILIDADES", "").split(",") if h and h not in g.j.habilidades]:
            g.j.habilidades.append(hid)
        inimigos = [g.inimigo(os.environ["LUTA"], nivel=int(os.environ.get("NIVEL_LUTA", "6")))
                    for _ in range(int(os.environ.get("QUANTOS", "1")))]
        for quem, var in [(g.j, "EFEITOS")] + [(e, "EFEITOS_INIMIGO") for e in inimigos]:
            for ef in [x.split(":") for x in os.environ.get(var, "").split(",") if x]:
                quem.aplicar(ef[0], int(ef[1]), float(ef[2]) if len(ef) > 2 else 0)
        lutar(g, inimigos)
    if os.environ.get("EVENTO"):
        nome = os.environ["EVENTO"]
        fn = next(getattr(m, nome) for m in (ev_comuns, ev_classe, ev_comitiva, ev_vila) if hasattr(m, nome))
        ui.cena(loc["nome"], g.contexto_cena(), "evento")
        fn(g)
    try:
        g.rodar()
    except FimDeJogo:
        pass


LUTAS_BROQUEL = {
    "lobos": lambda g, n: [g.inimigo("lobo", nivel=n) for _ in range(3)],
    "esqueletos": lambda g, n: [g.inimigo("esqueleto", nivel=n) for _ in range(3)],
    "misto": lambda g, n: [g.inimigo("bandido", nivel=n) for _ in range(2)] + [g.inimigo("cultista", nivel=n)],
    "cultistas": lambda g, n: [g.inimigo("cultista", nivel=n) for _ in range(2)],
    "bandido": lambda g, n: [g.inimigo("bandido", nivel=n)],
}


def _broquel(ui, nivel, talentos, luta, extra=None):
    """O Guerreiro (ESPEC, padrão paladino) no nível dado, vestido, com o Broquel do Vigia, no Bosque do Moinho, com o
    ossuário já vencido. Começa na LUTA (lobos, esqueletos, misto, cultistas, bandido), com inimigos um nível abaixo.
    Depois de cada luta: a mesma luta de novo (o mesmo sorteio de partida), com o Broquel ou com um broquel de números
    iguais e sem o efeito, ou seguir jogando."""
    from rpg import dev, missoes
    from rpg.itens import UNICOS_POR_ID, fazer_unico
    from rpg.ui import BotUI
    g = Jogo(BotUI(random.Random(1)), seed=int(os.environ.get("SEMENTE", "11")), pasta_saves=tempfile.mkdtemp(),
             hardcore=False)
    g.iniciar("Jean", "guerreiro", "turvo")
    dev.subir_ate(g, nivel, spec=os.environ.get("ESPEC", "paladino"))
    g.j.talentos.clear()
    for t in talentos:
        nome, _, rank = t.partition("=")
        g.j.talentos[nome] = int(rank or 1)
    g.j.pontos_talento = 0
    dev.vestir(g, random.Random(3), nivel)
    for espaco, bonus in (extra or {}).items():  # bônus a mais num item vestido (o cenário das reações)
        if g.j.equip.get(espaco):
            g.j.equip[espaco] = dict(g.j.equip[espaco], bonus={**g.j.equip[espaco]["bonus"], **bonus})
    com = fazer_unico(UNICOS_POR_ID["broquel_do_vigia"], nivel)
    sem = dict(com, nome="Broquel sem efeito", raridade="raro", bonus=dict(com["bonus"]))
    sem.pop("unico")
    missoes.registro(g, "febre_do_turvo").update(etapa="fundo", cenas=["abertura", "capela_exterior"])
    g.marcar(missoes.MARCA_BROQUEL, True)
    loc = next(l for l in g.mundo["locais"] if l["chave"] == "bosque_do_moinho")
    g.mundo["atual"], loc["visitado"] = loc["id"], True
    g.periodo, g.clima = 1, "limpo"
    g.ui, ui.jogo = ui, g
    criar = LUTAS_BROQUEL[os.environ.get("LUTA", luta)]
    escolha = "broquel"
    while escolha:
        g.j.equip["secundaria"] = com if escolha == "broquel" else sem
        g.j.recalcular()
        g.j.hp, g.j.rec, g.j.efeitos = g.j.max_hp, g.j.max_rec, {}
        g.j.consumiveis["pocao_vida"] = 2
        g.rng.seed(77)  # a mesma luta de partida a cada vez
        ui.cena("Clareira", g.contexto_cena(), "evento")
        g.dizer("Com o Broquel do Vigia." if escolha == "broquel" else "Com um broquel de números iguais, sem o Revide.",
                "cinza")
        lutar(g, criar(g, max(1, nivel - 1)))
        escolha = g.menu("A luta acabou.", [("A mesma luta, com o Broquel do Vigia", "broquel"),
                                            ("A mesma luta, com um broquel sem o Revide", "sem"),
                                            ("Seguir jogando", None)])
    try:
        g.rodar()
    except FimDeJogo:
        pass


def broquel(ui):
    """Escudo e ataque, com e sem o Broquel: Guerreiro nível NIVEL (padrão 4), sem talentos, contra três lobos."""
    _broquel(ui, int(os.environ.get("NIVEL", "4")), [], "lobos")


def muralha(ui):
    """Muralha com Contra-ataque (CONTRA, padrão 1) e o Broquel: Guerreiro nível NIVEL (padrão 6), contra dois bandidos
    e um cultista (o cultista ataca de longe: o Revide não o alcança)."""
    _broquel(ui, int(os.environ.get("NIVEL", "6")), ["muralha", f"contra_ataque={os.environ.get('CONTRA', '1')}"], "misto")


def reacoes(ui):
    """As reações ao golpe juntas (para ver a ordem na tela): o Guerreiro com Contra-ataque (CONTRA, padrão 7: sempre
    revida), espinhos e roubo de vida nas botas e nas luvas (ESPINHOS, ROUBO) e o Broquel (o Revide), contra lobos
    (LUTA). Sem mexer em regra: só monta a situação."""
    _broquel(ui, int(os.environ.get("NIVEL", "6")), [f"contra_ataque={os.environ.get('CONTRA', '7')}"],
             os.environ.get("LUTA", "lobos"), extra={"pes": {"espinhos": int(os.environ.get("ESPINHOS", "4"))},
                                                     "maos": {"roubo_vida": int(os.environ.get("ROUBO", "20"))}})


def relatorio(ui):
    """Mundo gerado, guerreiro forte num lugar selvagem: cada Explorar (VEZES, padrão 2) cai no EVENTO (padrão
    encontro_hostil, uma luta comum), para o relatório da luta e o que vem depois dele."""
    import rpg.eventos as eventos
    from rpg.eventos.motor import disparar_id
    g = Jogo(ui, seed=int(os.environ.get("SEMENTE", "4")), pasta_saves=tempfile.mkdtemp(), hardcore=False)
    ui.jogo = g
    g.iniciar("Jean", "guerreiro")
    loc = next(l for l in g.mundo["locais"] if l["tipo"] == "selvagem")
    g.mundo["atual"], loc["visitado"] = loc["id"], True
    g.periodo, g.clima = int(os.environ.get("PERIODO", "0")), "limpo"
    g.j.base["atk"] = 400
    g.j.recalcular()
    g.j.hp = g.j.max_hp
    original, vezes = eventos.disparar, [int(os.environ.get("VEZES", "2"))]

    def forcado(g2, contexto):
        if contexto != "explorar" or not vezes[0]:
            return original(g2, contexto)
        vezes[0] -= 1
        return disparar_id(g2, os.environ.get("EVENTO", "encontro_hostil"), contexto) or True
    eventos.disparar = forcado
    try:
        g.rodar()
    except FimDeJogo:
        pass


def fogueira(ui):
    """A campanha no LUGAR (charco, padrão, à noite: acampar abre a fogueira; vau: a vila, de manhã; bosque: o Bosque
    do Moinho; capela: do lado de fora da Capela Afogada, ou na SALA dela, com a nave vencida), CLASSE (padrão
    arqueiro). COMITIVA: quem anda junto, separado por vírgula (padrão "morel,odete"); RESERVA: quem espera no
    acampamento (padrão "yara"); FERIDO: quem está ferido. CONVERSA=1: todos com a primeira conversa pronta (o ✉). FOME=n: n dias sem comer (PROVISOES, padrão 3); TOCHAS=n.
    FERA=1: o lobo do patrulheiro. PERIODO e CLIMA: a hora e o tempo (padrão: noite e limpo fora da vila). EXAUSTO=1: a
    noite passou sem dormir (abre já na entrada por exaustão). Sair leva ao título, com o save (para conferir que a
    fome volta igual)."""
    from rpg.__main__ import menu_principal
    pasta = tempfile.mkdtemp()
    g = Jogo(ui, seed=int(os.environ.get("SEMENTE", "5")), pasta_saves=pasta, hardcore=False)
    ui.jogo = g
    g.iniciar("Jean", os.environ.get("CLASSE", "arqueiro"), "turvo")
    from rpg import missoes
    lugar = os.environ.get("LUGAR", "charco")
    if lugar == "capela":  # já se viu a chegada; na SALA, a nave vencida (a sacristia é a etapa)
        sala = os.environ.get("SALA", "exterior")
        missoes.registro(g, "febre_do_turvo").update(
            etapa="capela" if sala == "exterior" else "sacristia", cenas=["abertura", "capela_exterior"], sala=sala,
            pistas=["agua_do_leste", "represa", "canal_da_capela"] + ([] if sala == "exterior" else ["agua_da_capela"]))
    else:
        missoes.registro(g, "febre_do_turvo").update(etapa="capela", cenas=["abertura"],
                                                     pistas=["agua_do_leste", "represa", "canal_da_capela"])
    ativos = [c for c in os.environ.get("COMITIVA", "morel,odete").split(",") if c]
    reserva = [c for c in os.environ.get("RESERVA", "yara").split(",") if c]
    for c in reserva + ativos:
        cm.recrutar(g, c)
    for c in reserva:
        cm.para_acampamento(g, c, silencioso=True)
    for c in os.environ.get("FERIDO", "").split(","):
        if cm.membro(g, c):
            cm.membro(g, c)["ferido"] = True
    if os.environ.get("CONVERSA"):  # todos com a primeira conversa pronta (o ✉): dias e aprovação de sobra
        for c in reserva + ativos:
            cm.membro(g, c).update(dias=99, aprovacao=max(cm.membro(g, c)["aprovacao"], 60))
    if os.environ.get("FERA"):  # o animal do patrulheiro, como a especialização dá
        from rpg import especializacao
        g.j.companheiro = {"nome": "Cinza", **especializacao.animal("lobo", g.j.nivel)}
    j = g.j
    j.provisoes, j.fome = int(os.environ.get("PROVISOES", "3")), int(os.environ.get("FOME", "0"))
    if os.environ.get("TOCHAS"):
        j.consumiveis["tocha"] = int(os.environ["TOCHAS"])
    j.recalcular()
    j.hp = j.max_hp
    chave = {"vau": "vau_do_turvo", "bosque": "bosque_do_moinho", "capela": "capela_afogada"}.get(lugar, "charco_dos_juncos")
    for l in g.mundo["locais"]:
        l["visitado"] = l["chave"] in ("vau_do_turvo", "charco_dos_juncos", "bosque_do_moinho", chave)
    g.mundo["atual"] = next(l["id"] for l in g.mundo["locais"] if l["chave"] == chave)
    g.dia, g.periodo = 5, int(os.environ.get("PERIODO", 0 if chave == "vau_do_turvo" else 3))
    g.clima = os.environ.get("CLIMA", "limpo")
    if os.environ.get("EXAUSTO"):
        g.periodo = 4  # a noite passou: a próxima tela já é a do exausto
    g.autosalvar = True
    try:
        g.rodar()
    except FimDeJogo:
        pass
    ui.jogo = None
    menu_principal(ui, argparse.Namespace(seed=1, saves=pasta, brando=False))


def tutorial(ui):
    """A segunda parte da abertura guiada (V2–V5, E1, T1, N1): a campanha depois da despensa (a luta e o Mural já
    vistos), com o tutorial ligado (TUTORIAL=0 desliga). LUGAR: vau (padrão), charco, bosque ou capela; PERIODO (0
    manhã ... 3 noite). VIDA e REC: a fração da vida e do recurso (0.5...). OURO, PROVISOES, TOCHAS, PONTOS (de
    talento). COMITIVA: quem anda junto ("morel,odete"); RESERVA: quem espera no acampamento; FERIDO. ITEM=1: um
    item da arma para comparar logo na chegada. BAUS=n na bolsa. CONTRATO=aceito ou feito: um contrato de caça no
    CONTRATO_EM (bosque, padrão, ou charco). LUTA=família (QUANTOS, NIVEL_LUTA): uma luta logo na chegada. VISTAS: as orientações já vistas, além da luta e do Mural ("V3,N1").
    HARDCORE=1: morte definitiva. PENA=n (Penas de Fênix) e PROTECAO=mendigo: o que levanta o herói na luta.
    FERIMENTOS=corte,costelas (do herói, sem tratar), BANDAGENS=n, FOME=n (dias sem comer). GRATIS_USADO=templo,curandeira:
    o primeiro atendimento ou tratamento grátis já usado. NOME: o nome do herói (padrão Jean; para conferir nome longo).
    VITRINE=1 (o experimento de itens e ícones): machado, espada, escudo e anel na mochila, escudo e anel vestidos,
    unguento e bomba de fumaça na bolsa; VITRINE=2, sem o machado e com
    a armadura (cota) vestida. ARMA=machado: a arma vestida. NIVEL e ESPEC: o herói já nesse nível, especializado (o
    seletor de habilidades); HABILIDADES=todas: também as habilidades da outra especialização (um teste de capacidade
    do seletor, com mais habilidades do que um herói tem hoje). ANIMAL (lobo, falcao...): o animal do patrulheiro.
    As lutas cheias (a disposição da arena): GRUPO="caido:5,xama_caido:1" troca LUTA/QUANTOS por um grupo misto (o maior
    bando real: caídos à noite com a comitiva, mais o xamã de escolta); SERVOS=n: n esqueletos invocados já de pé ao
    lado do herói (o necromante com a Legião de Ossos e o Rei dos Mortos chega a três); LONGOS=1: o primeiro inimigo
    com o nome de um único do sorteio (o mais longo visto: 49 letras) e os outros com a letra e "(invocado)", como o
    reforço que um guardião chama. EMBOSCADA=jogador ou inimigo: a luta começa com a surpresa de um dos lados. LUTA_APOS_ESCOLHA=1: a luta só começa depois de um
    clique ("Começar a luta"), com a página já aberta: sem isso, o começo dela chega antes da página e é relido sem animar. Sair leva ao título, com o save (para carregar com orientações pendentes)."""
    from rpg import abertura as ab, itens, missoes, sobrevivencia
    from rpg.__main__ import menu_principal
    pasta = tempfile.mkdtemp()
    g = Jogo(ui, seed=int(os.environ.get("SEMENTE", "5")), pasta_saves=pasta, hardcore=os.environ.get("HARDCORE") == "1")
    ui.jogo = g
    g.iniciar(os.environ.get("NOME", "Jean"), os.environ.get("CLASSE", "guerreiro"), "turvo")
    ab.comecar(g, os.environ.get("TUTORIAL", "1") != "0")
    a = g.mundo["abertura"]
    a.update(despensa="feita", caneca=False)
    a["vistas"] = ["combate", "V1"] + [v for v in os.environ.get("VISTAS", "").split(",") if v]
    g.contagem["morel_na_taverna"] = 1
    for c in [c for c in os.environ.get("RESERVA", "").split(",") if c] + [c for c in os.environ.get("COMITIVA", "").split(",") if c]:
        cm.recrutar(g, c)
    for c in [c for c in os.environ.get("RESERVA", "").split(",") if c]:
        cm.para_acampamento(g, c, silencioso=True)
    for c in os.environ.get("FERIDO", "").split(","):
        if cm.membro(g, c):
            cm.membro(g, c)["ferido"] = True
    j = g.j
    if os.environ.get("ETAPA"):
        missoes.registro(g, "febre_do_turvo").update(etapa=os.environ["ETAPA"], cenas=["abertura", "capela_exterior"],
                                                     pistas=["agua_do_leste", "represa", "canal_da_capela"])
    else:
        missoes.registro(g, "febre_do_turvo").update(cenas=["abertura"])
    for k, campo in (("OURO", "ouro"), ("PROVISOES", "provisoes"), ("PONTOS", "pontos_talento")):
        if os.environ.get(k):
            setattr(j, campo, int(os.environ[k]))
    if os.environ.get("TOCHAS"):
        j.consumiveis["tocha"] = int(os.environ["TOCHAS"])
    j.hp = max(1, int(j.max_hp * float(os.environ.get("VIDA", "1"))))
    j.rec = int(j.max_rec * float(os.environ.get("REC", "1")))
    chave = {"charco": "charco_dos_juncos", "bosque": "bosque_do_moinho", "capela": "capela_afogada"}.get(
        os.environ.get("LUGAR", "vau"), "vau_do_turvo")
    for l in g.mundo["locais"]:
        l["visitado"] = l["chave"] in ("vau_do_turvo", "charco_dos_juncos", "bosque_do_moinho", chave)
    g.mundo["atual"] = next(l["id"] for l in g.mundo["locais"] if l["chave"] == chave)
    g.periodo, g.clima = int(os.environ.get("PERIODO", "0")), "limpo"
    g.autosalvar = True
    if os.environ.get("BAUS"):
        j.consumiveis["bau"] = int(os.environ["BAUS"])
    if os.environ.get("CONTRATO"):  # um contrato de caça aceito (CONTRATO=aceito) ou já cumprido (feito), no CONTRATO_EM
        alvo = {"charco": "charco_dos_juncos", "bosque": "bosque_do_moinho"}.get(os.environ.get("CONTRATO_EM", "bosque"))
        lid = next(l["id"] for l in g.mundo["locais"] if l["chave"] == alvo)
        c = next(c for c in (g.gerar_contrato() for _ in range(400)) if c["tipo"] == "caca" and c["local"] == lid)
        if os.environ["CONTRATO"] == "feito":
            c["feito"], c["concluido"] = c["total"], True
        g.contratos.append(c)
        a["vistas"].append("K1")
    for fid in [f for f in os.environ.get("FERIMENTOS", "").split(",") if f]:  # FERIMENTOS=corte,costelas (do herói)
        j.ferimentos.append({"id": fid, "dias": sobrevivencia.FERIMENTOS[fid]["dias"], "tratado": False})
    if os.environ.get("FERIMENTOS"):
        j.recalcular()
        j.hp = min(j.hp, j.max_hp)
    if os.environ.get("BANDAGENS") is not None:  # BANDAGENS=0 tira as da bolsa
        j.consumiveis["bandagem"] = int(os.environ["BANDAGENS"])
    if os.environ.get("FOME"):
        j.fome = int(os.environ["FOME"])
    for qual in [q for q in os.environ.get("GRATIS_USADO", "").split(",") if q]:  # templo, curandeira
        g.marcar(f"{qual}_gratis_usado")
    if os.environ.get("PENA"):  # PENA=1: uma Pena de Fênix na bolsa (cair na luta levanta o herói)
        j.consumiveis["pena_fenix"] = int(os.environ["PENA"])
    if os.environ.get("VITRINE"):  # o experimento de itens e ícones (ferramentas/prototipos/hud): as peças comparadas
        r = random.Random(3)
        acha = lambda icone, slot=None: next(e for e in iter(lambda: itens.gerar_equip(r, "guerreiro", 2, slot=slot, raridade="comum"), None)
                                             if e["icone"] == icone)
        j.mochila[:0] = ([] if os.environ.get("VITRINE") == "2" else [acha("machado", "arma")]) + [
            acha("espada", "arma"), acha("escudo", "secundaria"), acha("anel", "anel")]
        j.equip["secundaria"], j.equip["anel1"] = acha("escudo", "secundaria"), acha("anel", "anel")
        if os.environ.get("VITRINE") == "2":  # o estudo da ocupação dos ícones: também a armadura vestida
            j.equip["armadura"] = acha("armadura", "armadura")
        j.consumiveis.update(unguento=1, bomba_fumaca=2)
        j.recalcular()
    vestir_arma(g)
    if os.environ.get("PROTECAO"):  # PROTECAO=mendigo (ou santuario): a proteção que levanta uma vez
        g.marcar("bencao_fenix", os.environ["PROTECAO"])
    if os.environ.get("NIVEL"):  # o herói num nível alto, especializado (ESPEC, ou a primeira da classe)
        from rpg import dev
        from rpg.classes import CLASSES, SPECS
        if os.environ.get("ANIMAL"):  # o patrulheiro já com o animal pedido (sem a pergunta do nível 4)
            from rpg import especializacao
            from rpg.classes import COMPANHEIROS
            tipo = os.environ["ANIMAL"]
            g.escolher_companheiro = lambda *_: setattr(j, "companheiro", {"nome": COMPANHEIROS[tipo]["nome"],
                                                                         **especializacao.animal(tipo, j.nivel)})
        dev.subir_ate(g, int(os.environ["NIVEL"]), spec=os.environ.get("ESPEC"))
        if os.environ.get("HABILIDADES") == "todas":  # o teste de capacidade: as da outra especialização também
            outra = next(e for e in CLASSES[j.classe]["specs"] if e != j.spec)
            j.habilidades += [h for nv, h in SPECS[outra]["habilidades"] if nv <= j.nivel and h not in j.habilidades]
        j.hp = max(1, int(j.max_hp * float(os.environ.get("VIDA", "1"))))
        j.rec = int(j.max_rec * float(os.environ.get("REC", "1")))
    for k, v in (x.split("=") for x in os.environ.get("BOLSA", "").split(",") if x):  # BOLSA="pocao_vida=2,bandagem=0"
        j.consumiveis[k] = int(v)
    if os.environ.get("TROCA"):  # uma arma da classe na mochila: a troca de arma na luta (o menu de Itens)
        j.mochila.append(gerar_equip(random.Random(9), j.classe, j.nivel, slot="arma"))
    try:  # a morte no modo hardcore (HARDCORE=1) já na luta preparada leva ao título, como no jogo
        if os.environ.get("LUTA") or os.environ.get("GRUPO"):  # uma luta comum contra LUTA (família), para os selos das cartas
            g.ui.cena(g.loc["nome"], g.contexto_cena(), "evento")
            if os.environ.get("LUTA_APOS_ESCOLHA"):  # a luta começa com a página já aberta (a surpresa animada ao vivo)
                g.ui.escolher("A luta começa quando você quiser.", ["Começar a luta"])
            nv = int(os.environ.get("NIVEL_LUTA", "1"))  # NIVEL_LUTA: inimigos que aguentam umas rodadas
            if os.environ.get("GRUPO"):
                grupo = [g.inimigo(f, nivel=nv) for f, n in (x.split(":") for x in os.environ["GRUPO"].split(",")) for _ in range(int(n))]
            else:
                grupo = [g.inimigo(os.environ["LUTA"], nivel=nv) for _ in range(int(os.environ.get("QUANTOS", "2")))]
            if os.environ.get("LONGOS"):  # os nomes mais longos que o jogo dá: um único e os reforços invocados
                grupo[0].nome = "Morion, o Troll da montanha Corrompido Flamejante"
                for k, e in enumerate(grupo[1:]):
                    e.nome = f"{e.nome} {'ABCDEFGHIJ'[k]} (invocado)"
            if os.environ.get("SERVOS"):  # os servos já de pé quando a luta começa (depois da comitiva, como no jogo)
                from rpg import comitiva as cm_luta
                preparar = cm_luta.preparar_combate
                def com_servos(cb):
                    preparar(cb)
                    for _ in range(int(os.environ["SERVOS"])):
                        cb.invocar_aliado("Esqueleto (Invocado)", hp=60, atk=8, tipo="servo")
                    cm_luta.preparar_combate = preparar
                cm_luta.preparar_combate = com_servos
            # EMBOSCADA=jogador (a sua iniciativa) ou inimigo (o golpe deles primeiro): a surpresa do começo da luta
            lutar(g, grupo, **({"emboscada": os.environ["EMBOSCADA"]} if os.environ.get("EMBOSCADA") else {}))
        if os.environ.get("ITEM"):
            g.ui.cena(g.loc["nome"], g.contexto_cena(), "evento")
            g.dizer("No chão, entre a palha, alguma coisa brilha.")
            g.oferecer_equip(itens.gerar_equip(random.Random(4), j.classe, j.nivel, slot="arma", qualidade=1))
        g.rodar()
    except FimDeJogo:
        pass
    ui.jogo = None
    menu_principal(ui, argparse.Namespace(seed=1, saves=pasta, brando=False))


def mercado(ui):
    """Uma vila do mundo gerado com o herói direto no mercado (Voltar leva à vila; o prédio do mercado entra de novo).
    CLASSE (padrão arqueiro: as flechas também), OURO (padrão 300), MOCHILA (quantos equipamentos na mochila, padrão 8;
    alguns de outra classe), PROVISOES, PERIODO (padrão 1, tarde; 3 é noite). AMOSTRAS=1 (o experimento de resolução,
    ferramentas/prototipos/hud): um Martelo na frente da mochila e uma Pena de Fênix na bolsa. AMOSTRAS=2 (o escudo e o
    unguento da 1.94.0): um escudo na frente da mochila e um Unguento de Prata na bolsa. AMOSTRAS=3 (a proposta do
    machado e da bomba): um machado na frente da mochila e uma Bomba de Fumaça na bolsa. ARMA=machado: a arma vestida.
    AMOSTRA=<desenho> (arco, cajado, gibao, bota...): uma peça da CLASSE com esse desenho na frente da mochila.
    VESTIR=gibao,bota: as peças vestidas."""
    g = Jogo(ui, seed=int(os.environ.get("SEMENTE", "8")), pasta_saves=tempfile.mkdtemp())
    ui.jogo = g
    classe = os.environ.get("CLASSE", "arqueiro")
    g.iniciar("Jean", classe)
    g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["tipo"] == "vila")["id"]
    g.periodo, g.clima = int(os.environ.get("PERIODO", "1")), "limpo"
    g.j.ouro = int(os.environ.get("OURO", "300"))
    if os.environ.get("PROVISOES"):
        g.j.provisoes = int(os.environ["PROVISOES"])
    rng = random.Random(7)
    for k in range(int(os.environ.get("MOCHILA", "8"))):
        g.j.mochila.append(gerar_equip(rng, classe if k % 3 else "mago" if classe != "mago" else "guerreiro", 2))
    if os.environ.get("AMOSTRAS"):
        r = random.Random(1)
        icone, consumivel = {"2": ("escudo", "unguento"), "3": ("machado", "bomba_fumaca")}.get(os.environ["AMOSTRAS"],
                                                                                              ("martelo", "pena_fenix"))
        g.j.mochila.insert(0, next(e for e in iter(lambda: gerar_equip(r, "guerreiro", 2), None) if e["icone"] == icone))
        g.j.consumiveis[consumivel] = 1
    if os.environ.get("AMOSTRA"):
        r = random.Random(3)
        espaco = espaco_do_desenho(os.environ["AMOSTRA"])
        g.j.mochila.insert(0, next(e for e in iter(lambda: gerar_equip(r, classe, 2, slot=espaco), None) if e["icone"] == os.environ["AMOSTRA"]))
    vestir_arma(g)
    g.loja()
    try:
        g.rodar()
    except FimDeJogo:
        pass


def aneis(ui):
    """Guerreiro numa vila do mundo gerado acha um anel: ANEIS (padrão 2) anéis já vestidos (1: só o primeiro espaço;
    0: nenhum), um deles o Anel do Último Rei. Na mochila, outro anel (para equipar pelo inventário e pelo mercado);
    CHEIA=1 enche a mochila. OURO (padrão 300)."""
    from rpg import itens
    g = Jogo(ui, seed=8, pasta_saves=tempfile.mkdtemp())
    ui.jogo = g
    g.iniciar("Jean", "guerreiro")
    g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["tipo"] == "vila")["id"]
    g.periodo, g.clima = 1, "limpo"
    g.j.ouro = int(os.environ.get("OURO", "300"))
    rng = random.Random(11)
    n = int(os.environ.get("ANEIS", "2"))
    if n >= 1:
        g.j.equip["anel1"] = itens.fazer_unico(next(u for u in itens.UNICOS if u["id"] == "anel_do_ultimo_rei"), 3)
    if n >= 2:
        g.j.equip["anel2"] = gerar_equip(rng, "guerreiro", 3, slot="anel", raridade="magico")
    g.j.mochila.append(gerar_equip(rng, "guerreiro", 3, slot="anel", raridade="comum"))
    if os.environ.get("CHEIA") == "1":
        while len(g.j.mochila) < 12:
            g.j.mochila.append(gerar_equip(rng, "guerreiro", 2))
    g.j.recalcular()
    ui.cena("Ruínas do caminho", g.contexto_cena(), "evento")
    g.dizer("Entre as pedras, algo reluz.")
    g.oferecer_equip(gerar_equip(rng, "guerreiro", 4, slot="anel", raridade="raro"))
    try:
        g.rodar()
    except FimDeJogo:
        pass


CENARIOS = {"aneis": aneis, "mercado": mercado, "relatorio": relatorio, "combate": combate, "titulo": titulo, "vila": vila, "campanha": campanha, "baus": baus, "missao": missao,
            "recarga": recarga, "capela": capela, "retorno": retorno, "praca": praca, "encruzilhada": encruzilhada,
            "tiro_duplo": tiro_duplo, "covil": covil, "broquel": broquel, "muralha": muralha, "reacoes": reacoes, "resgate": resgate,
            "gelo": gelo, "abertura": abertura, "fogueira": fogueira,
            "tutorial": tutorial}


def main():
    nome = sys.argv[1] if len(sys.argv) > 1 else "combate"
    ui = WebUI()
    ui.jogo = None
    srv = Servidor(ui, config={"velocidade": os.environ.get("VELOCIDADE", "normal")}).iniciar()
    print(srv.url, flush=True)
    threading.Thread(target=CENARIOS[nome], args=(ui,), daemon=True).start()
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
