"""Baús trancados: abrir a pilha inteira de uma vez dá exatamente o que daria abrir um por um (cada baú com o próprio
sorteio, na mesma ordem), num quadro só na tela gráfica, com as decisões de equipamento uma por uma depois dele."""

import random
import tempfile
import unittest

from rpg.jogo import Jogo
from rpg.regras import LIMITE_MOCHILA
from rpg.itens import gerar_equip
from rpg.ui import BotUI, InterfaceGrafica


class Robo(BotUI):
    """Decide o equipamento achado pelo texto ("Guardar", "Deixar", "Equipar"); anota celebrações e painéis."""

    def __init__(self, decisao="Guardar"):
        super().__init__(random.Random(1), max_decisoes=200)
        self.decisao = decisao
        self.festas, self.paineis, self.perguntas = [], [], []

    def escolher(self, pergunta, opcoes):
        self.perguntas.append(list(opcoes))
        alvo = next((i for i, o in enumerate(opcoes) if o.startswith(self.decisao)), None)
        if alvo is None:
            alvo = next(i for i, o in enumerate(opcoes) if o.startswith(("Guardar", "Deixar")))
        return alvo

    def celebrar(self, tipo, dados):
        self.festas.append((tipo, dados))

    def painel(self, tipo, dados):
        self.paineis.append((tipo, dados))
        return False


class RoboGrafico(InterfaceGrafica, Robo):
    """O mesmo robô seguindo os caminhos da tela gráfica (o quadro do espólio, a janela do item)."""

    def painel(self, tipo, dados):
        self.paineis.append((tipo, dados))
        return True


def na_vila(ui, baus, seed=11, nivel=4):
    g = Jogo(ui, seed=seed, pasta_saves=tempfile.mkdtemp())
    g.iniciar("Teste", "arqueiro")
    g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["tipo"] == "vila")["id"]
    g.j.nivel = nivel
    g.j.consumiveis["bau"] = baus
    return g


def resultado(g):
    """O que importa depois de abrir: ouro, bolsa, mochila, os registros dos baús e o estado do sorteio."""
    return {"ouro": g.j.ouro, "bolsa": {k: v for k, v in g.j.consumiveis.items() if v},
            "mochila": [(it["nome"], it.get("raridade"), sorted(it["bonus"].items())) for it in g.j.mochila],
            "baus": [(e["ouro_bau"], e["suprimentos"], e["equip"]) for e in g.registro if e["t"] == "bau"],
            "rng": g.rng.getstate()}


def um_por_um(ui, baus, **kw):
    """Como era antes: cada baú aberto sozinho, um depois do outro, a partir do mesmo estado."""
    g = na_vila(ui, baus, **kw)
    for _ in range(baus):
        g.j.consumiveis["bau"] -= 1
        g.abrir_bau()
    return g


class TestBaus(unittest.TestCase):
    def test_a_pilha_da_o_mesmo_que_um_por_um(self):
        for interface in (Robo, RoboGrafico):
            for seed in (11, 12, 13, 14):
                juntos = na_vila(interface(), 4, seed=seed)
                self.assertTrue(juntos.usar_consumivel("bau"))
                separados = um_por_um(interface(), 4, seed=seed)
                self.assertEqual(resultado(juntos), resultado(separados), (interface.__name__, seed))
                self.assertEqual(len(resultado(juntos)["baus"]), 4)

    def test_um_bau_e_o_de_sempre(self):
        ui = RoboGrafico()
        g = na_vila(ui, 1)
        g.usar_consumivel("bau")
        espolios = [d for t, d in ui.festas if t == "espolio"]
        self.assertEqual(len(espolios), 1)
        self.assertEqual(espolios[0]["titulo"], "baú aberto")
        self.assertNotIn("baus", espolios[0])
        self.assertEqual(resultado(g), resultado(um_por_um(RoboGrafico(), 1)))

    def test_um_quadro_so_e_os_equipamentos_depois(self):
        """Vários baús: um quadro "Baús ×N" com o ouro e os suprimentos somados e a lista dos equipamentos; depois,
        uma janela de item por equipamento, na mesma ordem."""
        for seed in range(11, 31):
            ui = RoboGrafico()
            g = na_vila(ui, 5, seed=seed)
            g.usar_consumivel("bau")
            espolios = [d for t, d in ui.festas if t == "espolio"]
            self.assertEqual(len(espolios), 1)
            d = espolios[0]
            self.assertEqual((d["titulo"], d["baus"]), ("Baús ×5", 5))
            baus = [e for e in g.registro if e["t"] == "bau"]
            self.assertEqual(d["ouro"], sum(e["ouro_bau"] for e in baus))
            suprimentos = {}
            for e in baus:
                for k in e["suprimentos"]:
                    suprimentos[k] = suprimentos.get(k, 0) + 1
            self.assertEqual({x["id"]: x["qtd"] for x in d["itens"]}, suprimentos)
            nomes = [x["nome"] for x in d["equipamentos"]]
            self.assertEqual(len(nomes), len([e for e in baus if e["equip"]]))
            achados = [dd["item"]["nome"] for t, dd in ui.paineis if t == "achado"]
            self.assertEqual(achados, nomes)  # cada um com a janela dele, depois do quadro, com o mesmo nome
            if len(nomes) >= 2:
                return
        self.fail("nenhuma semente deu dois equipamentos em cinco baús")

    def test_mochila_cheia_segue_as_regras(self):
        """Com a mochila cheia, cada equipamento oferece deixar para trás; com uma vaga, o primeiro cabe e o seguinte
        já não."""
        for seed in range(11, 41):
            ui = RoboGrafico(decisao="Guardar")
            g = na_vila(ui, 6, seed=seed)
            g.j.mochila = [gerar_equip(random.Random(i), "arqueiro", 1) for i in range(LIMITE_MOCHILA - 1)]
            g.usar_consumivel("bau")
            janelas = [dd for t, dd in ui.paineis if t == "achado"]
            if len(janelas) < 2:
                continue
            self.assertTrue(janelas[0]["cabe"])
            self.assertTrue(all(not j["cabe"] for j in janelas[1:]))
            self.assertTrue(all(j["acoes"][-1].startswith("Deixar") for j in janelas[1:]))
            self.assertEqual(len(g.j.mochila), LIMITE_MOCHILA)
            return
        self.fail("nenhuma semente deu dois equipamentos em seis baús")

    def test_lugar_seguro_e_contagem(self):
        g = na_vila(Robo(), 3)
        g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["tipo"] == "selvagem")["id"]
        self.assertFalse(g.usar_consumivel("bau"))  # fora da vila e sem fogueira: não abre nenhum
        self.assertEqual(g.j.consumiveis["bau"], 3)
        self.assertFalse([e for e in g.registro if e["t"] in ("bau", "consumivel")])
        g.na_fogueira = True
        dia, periodo, ouro = g.dia, g.periodo, g.j.ouro
        self.assertTrue(g.usar_consumivel("bau"))
        self.assertEqual(g.j.consumiveis["bau"], 0)
        self.assertFalse(g.usar_consumivel("bau"))  # um segundo pedido logo depois não abre nada
        self.assertEqual(len([e for e in g.registro if e["t"] == "bau"]), 3)
        self.assertEqual(len([e for e in g.registro if e["t"] == "consumivel" and e["item"] == "bau"]), 3)
        self.assertEqual((g.dia, g.periodo), (dia, periodo))  # abrir não gasta tempo
        self.assertGreater(g.j.ouro, ouro)  # e não cobra nada

    def test_texto_diz_quantos_abre(self):
        ui = Robo()
        g = na_vila(ui, 3)
        g.j.mochila = []
        ui.decisao = "Usar item"
        # Personagem > Usar item da bolsa > o baú (o rótulo diz que abre os três) > guarda o que vier > Voltar
        roteiro = iter(["Usar item", "Baú Trancado", "Guardar", "Guardar", "Guardar", "Voltar"])
        original = ui.escolher

        def escolher(pergunta, opcoes):
            ui.perguntas.append(list(opcoes))
            for alvo in roteiro:
                i = next((k for k, o in enumerate(opcoes) if o.startswith(alvo)), None)
                if i is not None:
                    return i
            return original(pergunta, opcoes)
        ui.escolher = escolher
        g.personagem()
        self.assertIn("Baú Trancado (abre os 3)", [o for ops in ui.perguntas for o in ops])
        self.assertEqual(g.j.consumiveis["bau"], 0)


if __name__ == "__main__":
    unittest.main()
