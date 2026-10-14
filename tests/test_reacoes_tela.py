"""A ordem das reações ao golpe como a tela recebe (1.88.x): o golpe do inimigo, os espinhos nele, o Contra-ataque e o
roubo de vida desse contra-ataque, cada um com quem bateu, quem apanhou e a vida de depois; e as curas que antes só
apareciam no redesenho (a regeneração de cada turno e a vida por abate) com o seu lance. Nada disso muda contas,
gatilhos ou sorteios: a tela só segue o que o motor já fazia."""

import random
import tempfile
import unittest

from rpg import dev
from rpg.combate import Combate
from rpg.inimigos import HABS
from rpg.itens import UNICOS_POR_ID, fazer_unico
from rpg.jogo import Jogo
from rpg.modificadores import mod
from rpg.ui import BotUI


class Registro(BotUI):
    conquistas_na_tela = True

    def __init__(self):
        super().__init__(random.Random(1), max_decisoes=50)
        self.ev = []

    def lance(self, tipo, **d):
        self.ev.append((tipo, d))

    def atualizar(self):
        cb = self.g.combate_ativo
        self.ev.append(("estado", {"j": self.g.j.hp, **{cb.uid(e): e.hp for e in cb.inimigos}}))


def guerreiro(semente, contra=7, espinhos=4, roubo=20, regen=0, abate=0):
    ui = Registro()
    g = Jogo(ui, seed=semente, pasta_saves=tempfile.mkdtemp())
    ui.g = g
    g.iniciar("T", "guerreiro")
    dev.subir_ate(g, 6, spec="paladino")
    g.j.talentos.clear()
    g.j.talentos["contra_ataque"] = contra
    dev.vestir(g, random.Random(3), 6)
    for espaco, bonus in (("pes", {"espinhos": espinhos, "regen_vida": regen}), ("maos", {"roubo_vida": roubo, "vida_abate": abate})):
        g.j.equip[espaco] = dict(g.j.equip[espaco], bonus={**g.j.equip[espaco]["bonus"], **{k: v for k, v in bonus.items() if v}})
    g.j.equip["secundaria"] = fazer_unico(UNICOS_POR_ID["broquel_do_vigia"], 6)
    g.j.recalcular()
    g.j.hp = g.j.max_hp - 40
    return g, ui


class TestOrdemDasReacoes(unittest.TestCase):
    def test_golpe_espinhos_contra_ataque_e_o_roubo_dele(self):
        g, ui = guerreiro(5)
        lobo = g.inimigo("lobo", nivel=5)
        cb = Combate(g, [lobo, g.inimigo("lobo", nivel=5)], None, titulo="t")
        g.combate_ativo = cb
        with cb.agindo(lobo, None, g.j):
            cb.atacar(lobo, g.j, 1.0)
        lances = [(t, d) for t, d in ui.ev if t in ("golpe", "cura")]
        quem = [(t, d.get("de"), d.get("em"), d.get("rotulo"), bool(d.get("refletido")), bool(d.get("reacao")),
                 d.get("fonte")) for t, d in lances]
        u = cb.uid(lobo)
        self.assertEqual(quem, [("golpe", u, "j", None, False, False, None),           # o lobo morde
                                ("golpe", None, u, "Espinhos", True, False, None),      # os espinhos, nele
                                ("golpe", "j", u, "Contra-ataque", False, True, None),   # o herói revida
                                ("cura", None, "j", lances[3][1]["rotulo"], False, False, u)])  # o roubo, do revide
        # cada lance traz a vida de depois dele, e o estado que vem em seguida concorda (nada adiantado)
        for i, (t, d) in enumerate(ui.ev):
            if t in ("golpe", "cura"):
                seguinte = next((e for tt, e in ui.ev[i + 1:] if tt == "estado"), None)
                if seguinte and t == "golpe":
                    self.assertEqual(seguinte[d["em"]], d["hp"])

    def test_regeneracao_e_vida_por_abate_tem_lance(self):
        g, ui = guerreiro(5, contra=0, espinhos=0, roubo=0, regen=3, abate=5)
        lobo = g.inimigo("lobo", nivel=1)
        cb = Combate(g, [lobo], None, titulo="t")
        g.combate_ativo = cb
        ui.ev.clear()
        lobo.hp = 1
        cb.atacar(g.j, lobo, 1.0)
        curas = [d for t, d in ui.ev if t == "cura"]
        self.assertEqual(len(curas), 1)
        self.assertEqual((curas[0]["em"], curas[0]["valor"], curas[0]["modo"]), ("j", 5, "cura"))
        antes = cb._cura_j
        ui.ev.clear()
        g.j.hp = g.j.max_hp - 10
        try:
            cb.fase_jogador()
        except Exception:
            pass  # o menu do robô (sem inimigos vivos); só importa a regeneração do começo da vez
        regen = [d for t, d in ui.ev if t == "cura"]
        esperado = min(mod(g.j, "regen_vida"), 10)  # o equipamento sorteado também pode trazer regeneração
        self.assertTrue(regen and regen[0]["modo"] == "discreto" and regen[0]["valor"] == esperado)
        self.assertEqual(cb._cura_j, antes)  # o relatório da luta não muda: ele nunca somou essas


class TestGritoDoCultista(unittest.TestCase):
    """O grito de terror: aplicado, o lance do efeito (a tela põe o selo e o ícone no cartão); resistido pela fé do
    paladino, o lance do motivo real no alvo, e nenhum anúncio de enfraquecimento."""

    def gritar(self, sorteio):
        g, ui = guerreiro(5)
        cultista = g.inimigo("lobo", nivel=5)
        cb = Combate(g, [cultista], None, titulo="t")
        g.combate_ativo = cb
        ui.ev.clear()
        cb.rng.random = lambda: sorteio
        HABS["grito_terror"]["fn"](cb, cultista, g.j)
        return g, [(t, d) for t, d in ui.ev if t in ("efeito", "efeito_negado")]

    def test_aplicado(self):
        g, lances = self.gritar(0.99)
        self.assertIn("enfraquecido", g.j.efeitos)
        self.assertEqual([(t, d["em"], d["efeito"]) for t, d in lances], [("efeito", "j", "enfraquecido")])

    def test_a_fe_resiste(self):
        g, lances = self.gritar(0.0)
        self.assertNotIn("enfraquecido", g.j.efeitos)
        self.assertEqual([(t, d["em"], d["por"], d["rotulo"]) for t, d in lances],
                         [("efeito_negado", "j", "fe", "a fé não vacila")])


if __name__ == "__main__":
    unittest.main()
