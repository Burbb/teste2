"""Apoio dos testes da forja (rpg/forja): o cenário de conferência (o mesmo da demonstração do protótipo: o Guerreiro
no nível 4, no Vau, com Morel e Odette e as peças dos exemplos), o resultado de uma tentativa forçado pelo sorteio
(o motor não tem caso de teste: o teste faz o dado cair onde precisa) e a subida de nível. Nada daqui é conteúdo."""

import contextlib
import random
import tempfile

from rpg import comitiva, itens
from rpg.forja import oficina
from rpg.jogo import Jogo
from rpg.ui import BotUI

FICHA = comitiva.ficha


def jogo(seed=11):
    g = Jogo(BotUI(random.Random(1), max_decisoes=10 ** 6), seed=seed, pasta_saves=tempfile.mkdtemp(), hardcore=False)
    g.iniciar("Jean", "guerreiro", "turvo")
    preparar(g)
    return g


def preparar(g):
    """O Guerreiro no nível 4 no Vau, com Morel e Odette, 380 de ouro e as peças dos exemplos (o cenário da
    demonstração do protótipo, sem a recompensa de teste)."""
    from rpg import missoes
    rng = random.Random(11)
    missoes.registro(g, "febre_do_turvo")["cenas"].append("abertura")
    g.marcar("templo_gratis_usado")
    g.marcar("curandeira_gratis_usado")
    g.j.nivel = 4
    for cid in ("morel", "odete"):
        comitiva.recrutar(g, cid)

    def peca(classe, slot, nivel, raridade="comum", evitar=None):
        while True:
            it = itens.gerar_equip(rng, classe, nivel, slot=slot, raridade=raridade)
            if not evitar or evitar not in it["nome"]:
                return it
    g.j.equip["arma"] = peca("guerreiro", "arma", 2)
    g.j.equip["armadura"] = peca("guerreiro", "armadura", 2)
    FICHA.corpo(g, "morel").update(arma=peca("guerreiro", "arma", 2), armadura=peca("guerreiro", "armadura", 3))
    FICHA.corpo(g, "odete").update(arma=peca("mago", "arma", 3), secundaria=peca("mago", "secundaria", 3))
    g.j.mochila = [
        peca("guerreiro", "arma", 7, evitar="Ferro"),
        itens.fazer_unico(itens.UNICOS_POR_ID["lamento_de_gharbad"], 3),
        peca("guerreiro", "armadura", 4, "magico"),
        peca("mago", "secundaria", 5, "magico"),
        peca("arqueiro", "arma", 3, "magico"),
        peca("guerreiro", "anel", 3, "magico"),
    ]
    g.j.equip["arma"]["encantos"] = [None, None]  # a arma do herói com 2 sulcos (os exemplos do encantamento)
    g.j.ouro = 380
    g.j.consumiveis["bau"] = 2
    for m in comitiva.membros(g):
        FICHA.atualizar(g, m["id"])
        m["hp"] = m["max_hp"]
    g.j.recalcular()
    g.j.hp, g.j.rec = g.j.max_hp, g.j.max_rec
    loc = next(lo for lo in g.mundo["locais"] if lo["chave"] == "vau_do_turvo")
    g.mundo["atual"], loc["visitado"] = loc["id"], True
    g.periodo, g.clima = 0, "limpo"
    oficina.dar_uid(g)


@contextlib.contextmanager
def dado(g, valor):
    """O próximo sorteio do jogo sai `valor` (0 acerta qualquer chance; 0,9999 erra qualquer uma abaixo de 100%)."""
    original = g.rng.random
    g.rng.random = lambda: valor
    try:
        yield
    finally:
        g.rng.random = original


def reforcar(g, uid, veio=None, pedido=None, teste=None):
    """oficina.reforcar com o resultado forçado pelo sorteio ("sucesso" ou "falha"); `veio` é ignorado (a peça inteira
    melhora), como no motor."""
    if teste in ("sucesso", "falha"):
        with dado(g, 0.0 if teste == "sucesso" else 0.9999):
            return oficina.reforcar(g, uid, pedido)
    return oficina.reforcar(g, uid, pedido)


def nivel_de_teste(g):
    """Sobe o grupo 4 níveis pelo caminho do jogo (dev.subir_ate), sem a festa de cada nível."""
    from rpg import dev
    from rpg.regras import NIVEL_MAXIMO
    g.ui.celebrar = lambda *a, **k: None
    try:
        dev.subir_ate(g, min(NIVEL_MAXIMO, g.j.nivel + 4), spec=False)
    finally:
        del g.ui.celebrar
    for m in comitiva.membros(g):
        FICHA.atualizar(g, m["id"])
    g.forja_ultimo = None


def transferencia_de_teste(g):
    """Na bolsa: duas armas comuns de Guerreiro, uma +10 e outra +2 (com uma gravação, que não se move), e um peito
    incomum +6 com outro incomum +0. Ouro de sobra."""
    from rpg.regras import LIMITE_MOCHILA
    oficina.dar_uid(g)
    rng = random.Random(28)

    def peca(slot, raridade, n, gravacao=None):
        while True:
            it = itens.gerar_equip(rng, "guerreiro", 5, slot=slot, raridade=raridade)
            if it.get("raridade") == raridade and not it.get("unico"):
                break
        it.setdefault("bonus_base", dict(it["bonus"]))
        it.setdefault("preco_base", it.get("preco", 0))
        oficina.aplicar_nivel(it, n)
        if gravacao and it.get("encantos"):
            it["encantos"][0] = gravacao
        return it
    novas = [peca("arma", "comum", 10), peca("arma", "comum", 2, "brasa"), peca("armadura", "magico", 6), peca("armadura", "magico", 0)]
    g.j.mochila = (novas + g.j.mochila)[:LIMITE_MOCHILA]
    oficina.dar_uid(g)
    g.j.ouro = max(g.j.ouro, 5000)
    g.forja_ultimo = None
