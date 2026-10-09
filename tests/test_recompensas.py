"""Recompensas: o contrato paga o que o cartaz promete, e a tela gráfica festeja em vez de encher o registro."""

import random
import tempfile
import unittest

from rpg.jogo import Jogo
from rpg.ui import BotUI, InterfaceGrafica


class Anotador(BotUI):
    def __init__(self, rng):
        super().__init__(rng)
        self.textos, self.festas = [], []

    def dizer(self, texto="", cor=None):
        self.textos.append(str(texto))

    def efeito(self, texto, tipo="info", item=None):
        self.textos.append(str(texto))

    def celebrar(self, tipo, dados):
        self.festas.append((tipo, dados))


class AnotadorGrafico(InterfaceGrafica, Anotador):
    pass


def _jogo(ui):
    g = Jogo(ui, seed=8, pasta_saves=tempfile.mkdtemp())
    g.iniciar("Teste", "guerreiro")
    for _ in range(2):
        c = g.gerar_contrato()
        c["concluido"] = True
        g.contratos.append(c)
    g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["tipo"] == "vila")["id"]
    return g


class TestContratos(unittest.TestCase):
    def test_paga_o_que_o_cartaz_promete(self):
        g = _jogo(Anotador(random.Random(1)))
        prometido = sum(c["ouro"] for c in g.contratos)
        antes = g.j.ouro
        g.receber_contratos()
        self.assertEqual(g.j.ouro - antes, prometido)
        self.assertEqual(g.contratos, [])

    def test_texto_conta_cada_contrato(self):
        g = _jogo(Anotador(random.Random(1)))
        g.receber_contratos()
        self.assertEqual(sum(t.startswith("Recompensa de contrato") for t in g.ui.textos), 2)

    def test_tela_grafica_festeja_uma_vez_sem_texto(self):
        ui = AnotadorGrafico(random.Random(1))
        g = _jogo(ui)
        ouro, xp = sum(c["ouro"] for c in g.contratos), sum(c["xp"] for c in g.contratos)
        ui.textos.clear()
        g.receber_contratos()
        festas = [d for t, d in ui.festas if t == "contratos"]
        self.assertEqual(len(festas), 1)
        self.assertEqual((festas[0]["ouro"], festas[0]["xp"], len(festas[0]["contratos"])), (ouro, xp, 2))
        self.assertFalse([t for t in ui.textos if "contrato" in t.lower() or "ouro" in t or "XP" in t], ui.textos)


class TestNivel(unittest.TestCase):
    def test_tela_grafica_nao_repete_a_festa_no_texto(self):
        ui = AnotadorGrafico(random.Random(1))
        g = Jogo(ui, seed=8, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        ui.textos.clear()
        g.subir_nivel()
        self.assertTrue(any(t == "nivel" for t, _ in ui.festas))
        self.assertFalse([t for t in ui.textos if "ponto de talento" in t or "Nova habilidade" in t], ui.textos)

    def test_texto_continua_contando(self):
        ui = Anotador(random.Random(1))
        g = Jogo(ui, seed=8, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        g.subir_nivel()
        self.assertTrue(any("ponto de talento" in t for t in ui.textos))


if __name__ == "__main__":
    unittest.main()


class TestAmanhecer(unittest.TestCase):
    def test_tela_grafica_resume_a_noite_num_quadro(self):
        ui = AnotadorGrafico(random.Random(1))
        g = Jogo(ui, seed=8, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        g.j.hp = 10
        g.j.provisoes = 3
        ui.textos.clear()
        g.abrir_relato()
        g.descansar(0.3)
        g.novo_dia(descanso=1)
        quadros = [d for t, d in ui.festas if t == "amanhecer"]
        self.assertEqual(len(quadros), 1)
        icones = [x["icone"] for x in quadros[0]["itens"]]
        self.assertIn("coracao", icones)   # a vida que voltou
        self.assertIn("pernil", icones)    # a provisão gasta
        self.assertFalse([t for t in ui.textos if "Amanhece" in t or "recupera" in t], ui.textos)
        self.assertIsNone(g.relato)

    def test_texto_continua_contando(self):
        ui = Anotador(random.Random(1))
        g = Jogo(ui, seed=8, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        g.j.hp = 10
        g.abrir_relato()
        g.descansar(0.3)
        g.novo_dia(descanso=1)
        self.assertTrue(any(t.startswith("Você recupera") for t in ui.textos))
        self.assertTrue(any(t.startswith("Amanhece o dia") for t in ui.textos))
        self.assertFalse(ui.festas and any(t == "amanhecer" for t, _ in ui.festas))


class TestEspolio(unittest.TestCase):
    def test_trechos_da_barra_de_xp(self):
        g = Jogo(Anotador(random.Random(1)), seed=8, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        total = g.j.xp_proximo()
        g.j.xp = total - 3
        trechos = g.trechos_xp(10)
        self.assertEqual(trechos[0], [total - 3, total, total])  # enche este nível...
        self.assertEqual(trechos[1][:2], [0, 7])                 # ...e recomeça no seguinte com o resto
        self.assertEqual(g.trechos_xp(0), [])

    def test_vitoria_na_tela_grafica_mostra_o_espolio_antes_do_nivel(self):
        from rpg.combate import Combate
        ui = AnotadorGrafico(random.Random(1))
        g = Jogo(ui, seed=8, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        g.j.xp = g.j.xp_proximo() - 1
        e = g.inimigo("bandido", nivel=1)
        e.ouro, e.hp = 40, 0
        cb = Combate(g, [e])
        cb.fim("vitoria")
        self.assertNotIn("espolio", [t for t, _ in ui.festas])  # o quadro junta até a próxima pergunta...
        g.fechar_espolio()                                       # ...e aparece nela; o nível sobe depois dele
        tipos = [t for t, _ in ui.festas]
        self.assertLess(tipos.index("espolio"), tipos.index("nivel"))
        esp = dict(ui.festas)["espolio"]
        self.assertEqual(esp["ouro"], g.ouro_achado(40))
        self.assertFalse([t for t in ui.textos if t.endswith(" ouro") or t.endswith(" XP")], ui.textos)


class TestBau(unittest.TestCase):
    """O Baú Trancado mora na bolsa e só abre num lugar seguro: numa vila ou à luz da fogueira."""

    def _selvagem(self, g):
        g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["tipo"] == "selvagem")["id"]

    def test_na_estrada_nao_abre(self):
        g = _jogo(Anotador(random.Random(1)))
        self._selvagem(g)
        g.dar("bau")
        self.assertTrue(g.motivo_inutil("bau"))
        self.assertFalse(g.usar_consumivel("bau"))
        self.assertEqual(g.j.consumiveis["bau"], 1)

    def test_na_fogueira_abre(self):
        g = _jogo(Anotador(random.Random(1)))
        self._selvagem(g)
        g.dar("bau")
        g.na_fogueira = True
        self.assertIsNone(g.motivo_inutil("bau"))

    def test_na_vila_abre_e_entrega(self):
        g = _jogo(Anotador(random.Random(1)))
        g.dar("bau")
        antes = g.j.ouro
        self.assertTrue(g.usar_consumivel("bau"))
        self.assertEqual(g.j.consumiveis["bau"], 0)
        self.assertGreater(g.j.ouro, antes)
        aberto = [e for e in g.registro if e["t"] == "bau"]
        self.assertEqual(len(aberto), 1)
        self.assertEqual(g.j.ouro - antes, aberto[0]["ouro_bau"])
        self.assertEqual(g.estatisticas["ouro_fontes"]["baus"], aberto[0]["ouro_bau"])

    def test_tela_grafica_abre_num_quadro(self):
        ui = AnotadorGrafico(random.Random(1))
        g = _jogo(ui)
        g.dar("bau")
        ui.festas.clear()
        g.usar_consumivel("bau")
        quadros = [d for t, d in ui.festas if t == "espolio"]
        self.assertEqual(len(quadros), 1)
        self.assertEqual(quadros[0]["titulo"], "baú aberto")
        self.assertTrue(quadros[0]["ouro"] > 0 and quadros[0]["itens"])

    def test_guardiao_sempre_deixa_um_bau(self):
        g = _jogo(Anotador(random.Random(1)))
        chefe = g.inimigo("lobo", nivel=2)
        chefe.chefe = True
        g.saque_de_combate([chefe])
        self.assertEqual(g.j.consumiveis.get("bau"), 1)
