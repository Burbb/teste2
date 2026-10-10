"""Sobe o jogo web num cenário preparado, para os testes de navegador (fumaca.mjs).

    python -m tests.navegador.cenarios combate   # mago em luta, com contrato de caça no lugar
    python -m tests.navegador.cenarios titulo    # menu principal com um save de dia para carregar
    python -m tests.navegador.cenarios vila      # guerreiro acha um item raro e abre o mural de contratos
    python -m tests.navegador.cenarios campanha  # menu principal com saves dos dois modos; começar a campanha
    python -m tests.navegador.cenarios baus      # vila com três baús na bolsa: a pilha abre inteira
    python -m tests.navegador.cenarios missao    # campanha no Bosque do Moinho, na etapa de seguir o canal
    python -m tests.navegador.cenarios recarga   # título com um save da campanha (Bosque, à noite) e um do mundo gerado
    python -m tests.navegador.cenarios capela    # herói na Capela Afogada (CLASSE, ETAPA, NIVEL, PREPARO, LUGAR, SEMENTE)
    python -m tests.navegador.cenarios retorno   # chegando ao Vau com Ilse resolvida (DESFECHO, DIAS, LODO, YARA)
    python -m tests.navegador.cenarios praca     # depois da resposta a Caspar (POSTURA, YARA, LUGAR)

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
    g.contratos.append({"id": 991, "tipo": "caca", "local": loc["id"], "familia": "javali", "total": 3, "feito": 1,
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
    """Guerreiro numa vila com três baús na bolsa, numa semente em que saem ao menos dois equipamentos (conferida antes
    com o mesmo estado: o menu da vila sorteia a frase de ambiente e então a pilha abre)."""
    from rpg.regras import AMBIENTE_VILA
    from rpg.ui import BotUI, InterfaceGrafica

    def montar(u, seed):
        g = Jogo(u, seed=seed, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Jean", "guerreiro")
        g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["tipo"] == "vila")["id"]
        g.periodo, g.clima = 1, "limpo"
        g.j.nivel = 4
        g.j.consumiveis["bau"] = 3
        return g

    class Conta(InterfaceGrafica, BotUI):
        achados = 0

        def painel(self, tipo, dados):
            Conta.achados += tipo == "achado"
            return True

        def escolher(self, pergunta, opcoes):
            return next(i for i, o in enumerate(opcoes) if o.startswith(("Guardar", "Deixar")))
    for seed in range(1, 300):
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
    """Campanha (mago) no Bosque do Moinho, de dia, com a Fonte Nova já examinada: a missão está na etapa "canal"."""
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
    missão na ETAPA (padrão "sacristia": a nave já vencida) e o que se sabe até ali. PREPARO: "correntes" (soltas) ou
    "pronto" (Berta ouvida, a fita e as correntes: o rito disponível). Sair do jogo leva ao título, com o save."""
    from rpg import dev, missoes
    from rpg.__main__ import menu_principal
    from rpg.ui import BotUI
    pasta = tempfile.mkdtemp()
    g = Jogo(BotUI(random.Random(1)), seed=int(os.environ.get("SEMENTE", "11")), pasta_saves=pasta, hardcore=False)
    g.iniciar("Jean", os.environ.get("CLASSE", "guerreiro"), "turvo")
    nivel = int(os.environ.get("NIVEL", "5"))
    dev.subir_ate(g, nivel)  # já especializado (a primeira da classe): o acampamento não para na encruzilhada
    dev.gastar_talentos(g, random.Random(3))
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
    if preparo == "pronto":
        pistas += ["verdade_de_ilse", "nome_e_fita"]
        preparos.append("fita")
    missoes.registro(g, "febre_do_turvo").update(etapa=etapa, cenas=["abertura", "capela_exterior"], pistas=pistas,
                                                  preparos=preparos)
    for chave in ("bosque_do_moinho", "capela_afogada"):
        next(l for l in g.mundo["locais"] if l["chave"] == chave)["visitado"] = True
    g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["chave"] == os.environ.get("LUGAR", "capela_afogada"))["id"]
    g.periodo, g.clima = 0, "limpo"
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


CENARIOS = {"combate": combate, "titulo": titulo, "vila": vila, "campanha": campanha, "baus": baus, "missao": missao,
            "recarga": recarga, "capela": capela, "retorno": retorno, "praca": praca}


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
