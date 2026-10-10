"""Sobe o jogo web num cenário preparado, para os testes de navegador (fumaca.mjs).

    python -m tests.navegador.cenarios combate   # mago em luta, com contrato de caça no lugar
    python -m tests.navegador.cenarios titulo    # menu principal com um save de dia para carregar
    python -m tests.navegador.cenarios vila      # guerreiro acha um item raro e abre o mural de contratos
    python -m tests.navegador.cenarios campanha  # menu principal com saves dos dois modos; começar a campanha
    python -m tests.navegador.cenarios baus      # vila com três baús na bolsa: a pilha abre inteira

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


CENARIOS = {"combate": combate, "titulo": titulo, "vila": vila, "campanha": campanha, "baus": baus}


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
