"""Os interiores dos balcões da vila (o templo, desde a 1.219.0; a taverna, desde a 1.220.0): o motor manda a cena; a
tela só a mostra diante do prédio, com ou sem alguém para cuidar. E a mesa de Morel no encontro com ele: a cena
acompanha o que o motor decide (as cobranças, o teste de Força), só na tela gráfica."""
import unittest

from rpg import abertura
from rpg.eventos.comitiva import morel_na_taverna
from rpg.sistemas.servicos import cena_taverna, cena_templo
from rpg.web.estado import estado
from tests.test_missoes import Roteiro, campanha


class Grafica(Roteiro):
    """O roteiro numa tela gráfica: os painéis valem (o motor manda a cena)."""

    def painel(self, tipo, dados):
        super().painel(tipo, dados)
        return True


class TestInteriores(unittest.TestCase):
    def test_o_templo_tem_o_interior_na_vila(self):
        g = campanha()
        self.assertEqual(g.loc["tipo"], "vila")
        d = estado(g)["local"]["interiores"]["templo"]
        self.assertEqual(d, cena_templo())
        self.assertEqual(d["cena"], "templo")
        self.assertEqual([p["id"] for p in d["pontos"]], ["clerigo", "saida"])
        clerigo, saida = d["pontos"]
        self.assertTrue(clerigo["servicos"])                 # o Clérigo leva aos cartões
        self.assertEqual(saida["acao"], {"local": "voltar"})  # a Saída é o Voltar à vila do balcão

    def test_sem_ninguem_para_cuidar_o_interior_continua(self):
        """O acesso não depende do serviço: com a vida cheia, o templo está "em silêncio", mas o interior continua."""
        g = campanha()
        g.j.hp = g.j.max_hp
        local = estado(g)["local"]
        self.assertIn("templo", local["predios_fechados"])
        self.assertIn("templo", local["interiores"])

    def test_fora_da_vila_nao_ha_interior(self):
        g = campanha()
        loc = next(lo for lo in g.mundo["locais"] if lo["tipo"] != "vila")
        g.mundo["atual"] = loc["id"]
        self.assertEqual(estado(g)["local"]["interiores"], {})


class TestTaverna(unittest.TestCase):
    def test_o_balcao_tem_o_interior_na_vila(self):
        g = campanha()
        d = estado(g)["local"]["interiores"]["taverna"]
        self.assertEqual(d, cena_taverna(g))
        self.assertEqual(d["cena"], "taverna")
        self.assertEqual([(p["id"], p["servicos"]) for p in d["pontos"]], [("taverneiro", "rumores")])  # leva à bebida

    def test_a_despensa_so_enquanto_espera(self):
        g = campanha()
        abertura.comecar(g, False)
        abertura.estado(g)["despensa"] = "adiada"
        self.assertEqual([(p["id"], p["servicos"]) for p in cena_taverna(g)["pontos"]],
                         [("taverneiro", "rumores"), ("despensa", "despensa")])
        abertura.estado(g)["despensa"] = "feita"
        self.assertEqual([p["id"] for p in cena_taverna(g)["pontos"]], ["taverneiro"])


class TestMesaDeMorel(unittest.TestCase):
    def mesas(self, g):
        return [d for t, d in g.ui.paineis if t == "cena" and d["cena"] == "taverna_mesa"]

    def test_pagar_lanca_as_moedas_uma_vez(self):
        g = campanha(ui=Grafica(["Pagar 40", "Recusar"]))
        g.j.ouro = 60
        morel_na_taverna(g)
        self.assertEqual(g.j.ouro, 20)
        self.assertEqual([d["pagamentos"] for d in self.mesas(g)], [0, 1])
        self.assertEqual(g.balcao_aberto, "taverna")  # depois do encontro, o balcão continua aberto

    def test_a_queda_de_braco_segue_o_resultado_do_teste(self):
        for ok, desfecho, roteiro in ((True, "nos", ['"Queda', "Recusar"]), (False, "morel", ['"Queda', "Pagar 25", "Recusar"])):
            g = campanha(ui=Grafica(roteiro))
            g.j.ouro = 30
            testes = []
            g.teste = lambda attr, cd, ok=ok: testes.append(attr) or ok  # o resultado vem do teste; nada mais rola
            morel_na_taverna(g)
            self.assertEqual(testes, ["forca"])
            quedas = [d.get("queda") for d in self.mesas(g)]
            self.assertEqual(quedas[:3], [None, "prepara", desfecho])
            pagos = [d["pagamentos"] for d in self.mesas(g)]
            self.assertEqual(pagos[-1], 0 if ok else 1)  # perdeu: os 25 lançam as moedas, na composição da queda
            self.assertEqual(g.j.ouro, 30 if ok else 5)

    def test_o_vazio_nao_encena_nada(self):
        g = campanha(ui=Grafica(['"Não tenho', "Recusar"]))
        g.teste = lambda attr, cd: False
        morel_na_taverna(g)
        self.assertEqual([(d.get("queda"), d["pagamentos"]) for d in self.mesas(g)], [(None, 0)])

    def test_na_tela_de_texto_nada_muda(self):
        g = campanha(ui=Roteiro(["Pagar 40", "Recusar"]))
        g.j.ouro = 60
        morel_na_taverna(g)
        self.assertEqual(len(self.mesas(g)), 1)  # a tentativa de mostrar a mesa, que a tela de texto ignora
        self.assertIsNone(g.balcao_aberto)

    def test_o_balcao_mantido_e_o_voltar_dele(self):
        g = campanha(ui=Grafica(["Voltar à vila"]))
        g.balcao_aberto = "taverna"
        g.menu_vila()
        voltar = [o for o in g.ui.ofertas[-1] if o == "Voltar à vila"]
        self.assertEqual(voltar, ["Voltar à vila"])
        self.assertIsNone(g.balcao_aberto)  # vale uma volta só


if __name__ == "__main__":
    unittest.main()
