"""Sobe o jogo web num cenário preparado, para os testes de navegador (fumaca.mjs).

    python -m tests.navegador.cenarios combate   # mago em luta, com contrato de caça no lugar (FEITO)
    python -m tests.navegador.cenarios titulo    # menu principal com um save de dia para carregar
    python -m tests.navegador.cenarios vila      # guerreiro acha um item raro e abre o mural de contratos
    python -m tests.navegador.cenarios campanha  # menu principal com saves dos dois modos; começar a campanha
    python -m tests.navegador.cenarios baus      # vila com três baús na bolsa (BAUS): a pilha abre inteira
    python -m tests.navegador.cenarios missao    # campanha no Bosque do Moinho, na etapa de seguir o canal
    python -m tests.navegador.cenarios recarga   # título com um save da campanha (Bosque, à noite) e um do mundo gerado
    python -m tests.navegador.cenarios capela    # herói na Capela Afogada (CLASSE, ESPEC, ETAPA, NIVEL, PREPARO, LUGAR, SEMENTE, PRISAO, PERIODO, TOCHAS)
    python -m tests.navegador.cenarios retorno   # chegando ao Vau com Ilse resolvida (DESFECHO, DIAS, LODO, YARA)
    python -m tests.navegador.cenarios praca     # depois da resposta a Caspar (POSTURA, YARA, LUGAR); no Vau, abre no fim do capítulo
    python -m tests.navegador.cenarios encruzilhada  # a escolha de especialização, comparando (CLASSE, NIVEL)
    python -m tests.navegador.cenarios covil        # mundo gerado, no covil de um guardião (CLASSE, EVENTO, SEMENTE)
    python -m tests.navegador.cenarios tiro_duplo    # Patrulheiro contra três lobos feridos de jeitos diferentes (NIVEL, VIDAS)
    python -m tests.navegador.cenarios broquel       # Guerreiro nv 4 com o Broquel contra três lobos; repete com/sem o Revide (LUTA, ESPEC, NIVEL)
    python -m tests.navegador.cenarios resgate       # a recuperação: fome ou infecção no Charco, à noite (CLASSE, CAUSA, COMITIVA, CONTRATOS)
    python -m tests.navegador.cenarios abertura      # campanha nova no Vau: a despensa e as orientações (CLASSE, TUTORIAL, MOREL, DESPENSA, VIDA_RATOS)
    python -m tests.navegador.cenarios fogueira      # a comitiva na fogueira e a fome (LUGAR, COMITIVA, RESERVA, FERIDO, FOME, PROVISOES)
    python -m tests.navegador.cenarios gelo          # Mago com a iniciativa contra um lobo: duas Lanças antes de ele agir (PRISAO, NIVEL, SEMENTE)
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
from rpg.jogo import FimDeJogo, Jogo
from rpg.web.ponte import WebUI
from rpg.web.servidor import Servidor


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
    g.combate([e, lobo])
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
    """Guerreiro numa vila: acha um item raro (cartão do saque) e depois abre o mural de contratos."""
    g = Jogo(ui, seed=8, pasta_saves=tempfile.mkdtemp())
    ui.jogo = g
    g.iniciar("Jean", "guerreiro")
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
    com menos de três baús, a semente 1)."""
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
    for seed in range(1, 300 if baus >= 3 else 2):
        Conta.achados = 0
        t = montar(Conta(random.Random(1)), seed)
        t.sortear(AMBIENTE_VILA)
        t.usar_consumivel("bau")
        if Conta.achados >= 2:
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
    disponível). PRISAO (mago, nível 4 ou mais): o talento Prisão de Gelo já comprado, levando a "prisao" ou a "lanca";
    o resto dos talentos sai igual nas duas, para comparar o mesmo herói. PONTOS: pontos de talento sobrando. PERIODO
    (padrão 0, manhã; 3 é noite) e TOCHAS (padrão: as do começo). Sair do jogo leva ao título, com o save."""
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
              + (["ilse", "sigilo_do_turvo", "marcados"] if depois("sacristia") else [])
              + (["correntes"] if depois("ossuario") else []))
    preparo = os.environ.get("PREPARO", "")
    preparos = ["corpo_solto"] if preparo in ("correntes", "pronto") else []
    if preparo in ("berta", "pronto"):
        pistas += ["verdade_de_ilse", "nome_e_fita"]
        preparos.append("fita")
    missoes.registro(g, "febre_do_turvo").update(etapa=etapa, cenas=["abertura", "capela_exterior"], pistas=pistas,
                                                  preparos=preparos)
    for chave in ("bosque_do_moinho", "capela_afogada"):
        next(l for l in g.mundo["locais"] if l["chave"] == chave)["visitado"] = True
    g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["chave"] == os.environ.get("LUGAR", "capela_afogada"))["id"]
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
    g.mundo["atual"] = next(l["id"] for l in g.mundo["locais"] if l["chave"] == os.environ.get("LUGAR", "vau_do_turvo"))
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
    CONTRATOS=n: n contratos de caça já cumpridos, que pagam na página do Vau depois do resgate. Sair leva ao título."""
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
        cm.recrutar(g, "morel")
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
    g.combate(inimigos)
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
    g.combate([e], emboscada="jogador")
    try:
        g.rodar()
    except FimDeJogo:
        pass


def covil(ui):
    """Mundo gerado, CLASSE (padrão guerreiro) no nível 1, no covil de um guardião ainda vivo (ou no primeiro lugar do
    tipo LUGAR: vila, selvagem), no PERIODO (0 manhã ... 3 noite; padrão 0). BOLSA: "bandagem=0,pocao_vida=2" acerta a
    bolsa; OURO, o ouro. PROTECAO (mendigo, santuario ou 1) dá a proteção; LUTA (uma família: lobo, troll, aranha...) começa uma luta com o
    herói quase sem vida (VIDA, NIVEL_LUTA e QUANTOS mudam isso). Com EVENTO (o nome da função: crianca_perdida, madeira_para_flechas, os_enfermos, odete_na_estrada,
    mendigo_misterioso...), o evento toca antes do menu."""
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
    if os.environ.get("LUTA"):  # cai numa luta já quase sem vida, contra um inimigo forte: a proteção se ativa
        g.j.hp = int(os.environ.get("VIDA", "1"))  # VIDA e NIVEL_LUTA: uma luta comum (a teia da aranha, por exemplo)
        ui.cena(loc["nome"], g.contexto_cena(), "evento")
        g.dizer("Um vulto enorme sai da névoa.")
        g.combate([g.inimigo(os.environ["LUTA"], nivel=int(os.environ.get("NIVEL_LUTA", "6")))
                   for _ in range(int(os.environ.get("QUANTOS", "1")))])
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


def _broquel(ui, nivel, talentos, luta):
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
        g.combate(criar(g, max(1, nivel - 1)))
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


def fogueira(ui):
    """A campanha no LUGAR (charco, padrão, à noite: acampar abre a fogueira; vau: a vila, de manhã), CLASSE (padrão
    arqueiro). COMITIVA: quem anda junto, separado por vírgula (padrão "morel,odete"); RESERVA: quem espera no
    acampamento (padrão "yara"); FERIDO: quem está ferido. FOME=n: n dias sem comer (PROVISOES, padrão 3). Sair leva ao
    título, com o save (para conferir que a fome volta igual)."""
    from rpg.__main__ import menu_principal
    pasta = tempfile.mkdtemp()
    g = Jogo(ui, seed=int(os.environ.get("SEMENTE", "5")), pasta_saves=pasta, hardcore=False)
    ui.jogo = g
    g.iniciar("Jean", os.environ.get("CLASSE", "arqueiro"), "turvo")
    from rpg import missoes
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
    j = g.j
    j.provisoes, j.fome = int(os.environ.get("PROVISOES", "3")), int(os.environ.get("FOME", "0"))
    j.recalcular()
    j.hp = j.max_hp
    chave = {"vau": "vau_do_turvo"}.get(os.environ.get("LUGAR", "charco"), "charco_dos_juncos")
    for l in g.mundo["locais"]:
        l["visitado"] = l["chave"] in ("vau_do_turvo", "charco_dos_juncos", "bosque_do_moinho")
    g.mundo["atual"] = next(l["id"] for l in g.mundo["locais"] if l["chave"] == chave)
    g.dia, g.periodo, g.clima = 5, (0 if chave == "vau_do_turvo" else 3), "limpo"
    g.autosalvar = True
    try:
        g.rodar()
    except FimDeJogo:
        pass
    ui.jogo = None
    menu_principal(ui, argparse.Namespace(seed=1, saves=pasta, brando=False))


CENARIOS = {"combate": combate, "titulo": titulo, "vila": vila, "campanha": campanha, "baus": baus, "missao": missao,
            "recarga": recarga, "capela": capela, "retorno": retorno, "praca": praca, "encruzilhada": encruzilhada,
            "tiro_duplo": tiro_duplo, "covil": covil, "broquel": broquel, "muralha": muralha, "resgate": resgate,
            "gelo": gelo, "abertura": abertura, "fogueira": fogueira}


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
