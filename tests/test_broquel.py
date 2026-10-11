"""O Broquel do Vigia (E7, 1.63.0): o Revide, a vez do Contra-ataque, os ciclos, a ficha, a persistência e a
aquisição única (o ossuário, ou o ferreiro do Vau num save que já tinha vencido a sala)."""

import random
import tempfile
import unittest

from rpg import grimorio, itens, missoes
from rpg import balanceamento as bal
from rpg.combate import Combate
from rpg.itens import UNICOS_POR_ID, fazer_unico
from rpg.jogo import Jogo
from rpg.ui import BotUI
from tests.test_missoes import MID, Roteiro, fazer, ir, lutas, na_capela

BROQUEL = UNICOS_POR_ID["broquel_do_vigia"]


class Anota(BotUI):
    def __init__(self):
        super().__init__(random.Random(1), max_decisoes=10 ** 6)
        self.lances = []

    def lance(self, tipo, **d):
        self.lances.append((tipo, d))


class Sorteio:
    """O sorteio da luta numa fila: cada `random()` tira o próximo valor (depois dela, 0,9: nada de sorte)."""

    def __init__(self, fila=()):
        self.fila = list(fila)

    def random(self):
        return self.fila.pop(0) if self.fila else 0.9

    def uniform(self, a, b):
        return 1.0

    def randint(self, a, b):
        return a

    def choice(self, seq):
        return seq[0]


def heroi(com_broquel=True, contra=0, classe="guerreiro"):
    g = Jogo(Anota(), seed=1, pasta_saves=tempfile.mkdtemp())
    g.iniciar("Teste", classe)
    if com_broquel:
        g.j.equip["secundaria"] = fazer_unico(BROQUEL, 4)
    if contra:
        g.j.talentos["contra_ataque"] = contra
    g.j.recalcular()
    g.j.hp = g.j.max_hp
    return g


def luta(g, fila=(), familia="lobo", n=1):
    inimigos = [g.inimigo(familia, nivel=2) for _ in range(n)]
    cb = Combate(g, inimigos)
    cb.rng = Sorteio(fila)
    return cb, inimigos


def reacoes(g):
    return [(t, d.get("rotulo")) for t, d in g.ui.lances if d.get("reacao")]


# Um golpe do lobo no herói: [esquiva do herói, crítico do lobo] e, se houver Contra-ataque, a chance dele; depois o
# golpe de resposta: [esquiva do lobo, crítico do herói].
ACERTA = [0.9, 0.9]


class TestRevide(unittest.TestCase):
    def test_em_guarda_revida_o_golpe_corpo_a_corpo(self):
        g = heroi()
        cb, (lobo,) = luta(g)
        g.j.aplicar("guarda", 2, 0.5)
        antes = lobo.hp
        cb.atacar(lobo, g.j, 1.0, alcance="corpo")
        self.assertEqual(reacoes(g), [("golpe", "Revide")])
        dano = antes - lobo.hp
        self.assertGreater(dano, 0)
        golpe = next(d for t, d in g.ui.lances if d.get("rotulo") == "Revide")
        self.assertEqual(golpe["dano"], dano)

    def test_sem_guarda_a_distancia_esquivado_ou_sem_o_broquel_nao_revida(self):
        g = heroi()
        cb, (lobo,) = luta(g)
        cb.atacar(lobo, g.j, 1.0, alcance="corpo")  # sem guarda
        g.j.aplicar("guarda", 2, 0.5)
        cb.atacar(lobo, g.j, 1.0, alcance="distancia")  # magia, flecha
        cb.rng = Sorteio([0.0])  # o herói se esquiva: não acertou, não há o que revidar
        cb.atacar(lobo, g.j, 1.0, alcance="corpo")
        self.assertEqual(reacoes(g), [])
        g = heroi(com_broquel=False)
        cb, (lobo,) = luta(g)
        g.j.aplicar("guarda", 2, 0.5)
        cb.atacar(lobo, g.j, 1.0, alcance="corpo")
        self.assertEqual(reacoes(g), [])

    def test_um_revide_por_golpe_e_revide_nao_gera_reacao(self):
        g = heroi()
        cb, lobos = luta(g, n=3)
        g.j.aplicar("guarda", 2, 0.5)
        for lobo in lobos:
            cb.atacar(lobo, g.j, 1.0, alcance="corpo")
        self.assertEqual(reacoes(g), [("golpe", "Revide")] * 3)  # um por golpe recebido, em quem bateu
        self.assertTrue(all(lobo.hp < lobo.max_hp for lobo in lobos))

    def test_espinhos_que_matam_deixam_o_revide_sem_alvo(self):
        g = heroi()
        g.j.equip["armadura"] = fazer_unico(UNICOS_POR_ID["pele_do_penitente"], 4)
        g.j.recalcular()
        cb, (lobo,) = luta(g)
        lobo.hp = 1
        g.j.aplicar("guarda", 2, 0.5)
        cb.atacar(lobo, g.j, 1.0, alcance="corpo")
        self.assertFalse(lobo.vivo)
        self.assertEqual(reacoes(g), [])  # os espinhos já derrubaram; nada de golpe num morto
        self.assertEqual([d["rotulo"] for t, d in g.ui.lances if t == "golpe" and d.get("rotulo")], ["Espinhos"])

    def test_abate_por_revide_conta_e_cura_por_dano_vale(self):
        g = heroi()
        g.j.spec, g.j.talentos["frenesi"], g.j.talentos["sede_insaciavel"] = "berserker", 1, 1
        g.j.recalcular()
        cb, (lobo,) = luta(g)
        lobo.hp = 2
        g.j.hp = g.j.max_hp - 20
        g.j.aplicar("guarda", 2, 0.5)
        antes = g.j.hp
        cb.atacar(lobo, g.j, 0.01, alcance="corpo")  # um arranhão: o herói continua de pé e revida
        self.assertFalse(lobo.vivo)
        self.assertEqual(cb.memoria.get("frenesi"), 1)  # o abate do Revide é do herói
        self.assertTrue(any(t == "cura" and d.get("modo") == "roubo" for t, d in g.ui.lances))
        self.assertGreaterEqual(g.j.hp, antes - 1)


class TestContraAtaqueEPrioridade(unittest.TestCase):
    def test_contra_ataque_vem_antes_e_ocupa_a_resposta(self):
        for rank in (1, 2):
            g = heroi(contra=rank)
            cb, (lobo,) = luta(g, ACERTA + [0.0])  # o Contra-ataque sai
            g.j.aplicar("guarda", 2, 0.5)
            cb.atacar(lobo, g.j, 1.0, alcance="corpo")
            self.assertEqual(reacoes(g), [("golpe", "Contra-ataque")], rank)

    def test_contra_ataque_esquivado_tambem_ocupa(self):
        g = heroi(contra=2)
        cb, (lobo,) = luta(g, ACERTA + [0.0, 0.0])  # sai, e o lobo se esquiva dele
        g.j.aplicar("guarda", 2, 0.5)
        cb.atacar(lobo, g.j, 1.0, alcance="corpo")
        self.assertEqual(reacoes(g), [("erro", "Contra-ataque")])

    def test_sem_contra_ataque_o_revide_responde(self):
        g = heroi(contra=2)
        cb, (lobo,) = luta(g, ACERTA + [0.99])  # a chance do talento não sai
        g.j.aplicar("guarda", 2, 0.5)
        cb.atacar(lobo, g.j, 1.0, alcance="corpo")
        self.assertEqual(reacoes(g), [("golpe", "Revide")])

    def test_sem_o_broquel_o_talento_e_o_de_sempre(self):
        """A mesma fila de sorteio, com e sem guarda: o talento sai, com 70%, e nada mais; quando não sai, nada."""
        for guarda in (False, True):
            g = heroi(com_broquel=False, contra=1)
            cb, (lobo,) = luta(g, ACERTA + [0.0])
            if guarda:
                g.j.aplicar("guarda", 2, 0.5)
            cb.atacar(lobo, g.j, 1.0, alcance="corpo")
            self.assertEqual(reacoes(g), [("golpe", "Contra-ataque")])
            g = heroi(com_broquel=False, contra=1)
            cb, (lobo,) = luta(g, ACERTA + [0.99])
            if guarda:
                g.j.aplicar("guarda", 2, 0.5)
            cb.atacar(lobo, g.j, 1.0, alcance="corpo")
            self.assertEqual(reacoes(g), [])
            self.assertEqual(cb.rng.fila, [])  # a chance do talento foi sorteada uma vez, como antes


class TestFichaEPersistencia(unittest.TestCase):
    def test_ficha_comparacao_e_grimorio(self):
        it = fazer_unico(BROQUEL, 4)
        self.assertEqual(it["bonus"], {"defesa": 2, "max_hp": 8})
        f = itens.ficha(it, "Vigor")
        self.assertEqual(f["efeito_nome"], "Revide")
        self.assertIn(f"({round(bal.REVIDE * 100)}% do Ataque)", f["efeito"])
        self.assertNotIn("efeito", itens.ficha(fazer_unico(UNICOS_POR_ID["egide_do_martir"], 4)))
        g = heroi(com_broquel=False)
        pagina = lambda: next(h for h in grimorio.dados(g.j)["habilidades"] if h["id"] == "erguer_escudo")
        self.assertFalse(any("Broquel" in l.get("texto", "") for l in pagina()["linhas"]))
        g.j.equip["secundaria"] = it
        self.assertTrue(any(l.get("texto", "").startswith("Broquel do Vigia — Revide") for l in pagina()["linhas"]))
        g.j.talentos["contra_ataque"] = 1
        self.assertIn("Contra-ataque sai", pagina()["linhas"][-1]["texto"])

    def test_equipar_retirar_reforcar_vender_e_recomprar(self):
        g = heroi(com_broquel=False)
        it = fazer_unico(BROQUEL, 4)
        g.j.mochila.append(it)
        g.equipar(it)
        cb, (lobo,) = luta(g)
        g.j.aplicar("guarda", 2, 0.5)
        cb.atacar(lobo, g.j, 1.0, alcance="corpo")
        self.assertEqual(len(reacoes(g)), 1)
        # reforço: o nome ganha "+1", a Defesa sobe, a regra continua (o único é achado pelo id)
        it["bonus"]["defesa"] += 1
        it["reforco"] = 1
        it["nome"] = "Broquel do Vigia +1"
        self.assertIs(itens.unico_de(it), BROQUEL)
        self.assertEqual(itens.ficha(it)["efeito_nome"], "Revide")
        g.desequipar("secundaria")
        self.assertIn(it, g.j.mochila)
        g.ui.lances.clear()
        cb, (lobo,) = luta(g)
        g.j.aplicar("guarda", 2, 0.5)
        cb.atacar(lobo, g.j, 1.0, alcance="corpo")
        self.assertEqual(reacoes(g), [])  # retirado, a regra sai junto
        g.recompra = []
        g.vender_item(it)
        self.assertNotIn(it, g.j.mochila)
        self.assertTrue(g.recomprar_item(0))
        self.assertIs(itens.unico_de(g.j.mochila[-1]), BROQUEL)

    def test_salvar_e_carregar(self):
        g = heroi()
        g.salvar(silencioso=True)
        h = Jogo.carregar(Anota(), g.caminho_save(), g.pasta_saves)
        self.assertEqual(h.j.equip["secundaria"]["unico"], "broquel_do_vigia")
        cb, (lobo,) = luta(h)
        h.j.aplicar("guarda", 2, 0.5)
        cb.atacar(lobo, h.j, 1.0, alcance="corpo")
        self.assertEqual(reacoes(h), [("golpe", "Revide")])

    def test_isolado_e_fora_do_sorteio(self):
        com, sem = heroi(), heroi(com_broquel=False)
        for g, esperado in ((sem, []), (com, [("golpe", "Revide")])):
            cb, (lobo,) = luta(g)
            g.j.aplicar("guarda", 2, 0.5)
            cb.atacar(lobo, g.j, 1.0, alcance="corpo")
            self.assertEqual(reacoes(g), esperado)
        rng = random.Random(3)
        for _ in range(3000):  # o sorteio de lendários do Guerreiro nunca entrega o broquel
            it = itens.gerar_equip(rng, "guerreiro", 4, "secundaria", raridade="lendario")
            self.assertNotEqual(it.get("unico"), "broquel_do_vigia")


def no_ossuario(classe="guerreiro", roteiro=()):
    g = na_capela(classe, ui=Roteiro(list(roteiro)))
    missoes.registro(g, MID).update(etapa="ossuario")
    lutas(g, "vitoria")
    return g


def broqueis(g):
    return [it for it in [*g.j.mochila, *g.j.equip.values()] if it and it.get("unico") == "broquel_do_vigia"]


class TestAquisicao(unittest.TestCase):
    def test_o_ossuario_da_o_broquel_ao_guerreiro_uma_vez(self):
        g = no_ossuario(roteiro=["Guardar"])
        self.assertTrue(fazer(g, "ossuario"))
        self.assertEqual(len(broqueis(g)), 1)
        self.assertTrue(g.flag(missoes.MARCA_BROQUEL))
        self.assertIn("No braço do esqueleto de guarda ficou um broquel de ferro escuro, ainda preso pela correia.",
                      g.ui.ditos)
        self.assertEqual(missoes.registro(g, MID)["etapa"], "fundo")
        self.assertFalse(fazer(g, "ossuario"))  # a sala não se repete
        ir(g, "vau_do_turvo")
        self.assertFalse(missoes.broquel_no_ferreiro(g))  # já recebeu: o ferreiro não oferece
        for classe in ("arqueiro", "mago"):
            g = no_ossuario(classe)
            self.assertTrue(fazer(g, "ossuario"))
            self.assertEqual(broqueis(g), [])
            self.assertFalse(g.flag(missoes.MARCA_BROQUEL))

    def test_deixado_para_tras_nao_volta(self):
        g = no_ossuario(roteiro=["Deixar"])
        g.j.mochila.extend(fazer_unico(UNICOS_POR_ID["egide_do_martir"], 3) for _ in range(12))
        g.j.equip["secundaria"] = fazer_unico(UNICOS_POR_ID["egide_do_martir"], 3)  # nada vago, mochila cheia
        self.assertTrue(fazer(g, "ossuario"))
        self.assertEqual(broqueis(g), [])
        ir(g, "vau_do_turvo")
        self.assertFalse(missoes.broquel_no_ferreiro(g))

    def test_ferreiro_oferece_uma_vez_aos_saves_elegiveis(self):
        g = na_capela("guerreiro", ui=Roteiro(["Ferreiro: o broquel", "Guardar"]))
        missoes.registro(g, MID).update(etapa="fundo")  # um save de antes da E7, com o ossuário vencido
        ir(g, "vau_do_turvo")
        self.assertTrue(missoes.broquel_no_ferreiro(g))
        g.menu_vila()
        self.assertEqual(len(broqueis(g)), 1)
        self.assertFalse(missoes.broquel_no_ferreiro(g))
        # vendido, não volta pelo ferreiro
        g.recompra = []
        g.vender_item(broqueis(g)[0])
        self.assertFalse(missoes.broquel_no_ferreiro(g))
        # quem ainda não venceu o ossuário, outra classe e o mundo gerado: nada
        for classe, etapa in (("guerreiro", "ossuario"), ("guerreiro", "sacristia"), ("arqueiro", "fundo"),
                              ("mago", "retorno")):
            g = na_capela(classe)
            missoes.registro(g, MID).update(etapa=etapa)
            ir(g, "vau_do_turvo")
            self.assertFalse(missoes.broquel_no_ferreiro(g), (classe, etapa))
        g = Jogo(Roteiro(), seed=5, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        self.assertFalse(missoes.broquel_no_ferreiro(g))

    def test_save_carregado_mantem_a_marca(self):
        g = no_ossuario(roteiro=["Guardar"])
        fazer(g, "ossuario")
        ir(g, "vau_do_turvo")
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(), g.caminho_save(), g.pasta_saves)
        self.assertTrue(h.flag(missoes.MARCA_BROQUEL))
        self.assertFalse(missoes.broquel_no_ferreiro(h))
        self.assertEqual(len(broqueis(h)), 1)


if __name__ == "__main__":
    unittest.main()
