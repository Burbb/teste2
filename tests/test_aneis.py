"""Os dois espaços de anel: o item achado oferece um botão por espaço (qual anel sai, ou que o espaço está vazio), a
tela recebe os dois espaços para comparar, e a mochila (no texto e no mercado) deixa escolher qual substituir. Nada
troca o "pior" anel por conta própria."""

import random
import tempfile
import unittest

from rpg import itens
from rpg.itens import gerar_equip
from rpg.jogo import Jogo
from rpg.ui import InterfaceGrafica
from tests.test_missoes import Roteiro


class Tela(InterfaceGrafica, Roteiro):
    """Escolhe pelo texto, como o Roteiro, mas na tela gráfica: guarda os painéis e os rótulos oferecidos."""

    def painel(self, tipo, dados):
        self.paineis.append((tipo, dados))
        return True


def heroi(ui, aneis=2):
    g = Jogo(ui, seed=3, pasta_saves=tempfile.mkdtemp())
    g.iniciar("Teste", "guerreiro")
    g.j.nivel = 4  # o nível que os anéis pedem (o requisito da forja: o nível da peça menos 1)
    g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["tipo"] == "vila")["id"]
    rng = random.Random(2)
    if aneis >= 1:
        g.j.equip["anel1"] = itens.fazer_unico(next(u for u in itens.UNICOS if u["id"] == "anel_do_ultimo_rei"), 3)
    if aneis >= 2:
        g.j.equip["anel2"] = gerar_equip(rng, "guerreiro", 3, slot="anel", raridade="magico")
    g.j.recalcular()
    return g, gerar_equip(rng, "guerreiro", 4, slot="anel", raridade="raro")


class TestAchado(unittest.TestCase):
    def test_dois_ocupados_um_botao_por_anel(self):
        for espaco, fica in (("anel1", "anel2"), ("anel2", "anel1")):
            g, novo = heroi(Tela())
            antigo, outro = g.j.equip[espaco], g.j.equip[fica]
            g.ui.roteiro = [f"Substituir {antigo['nome']}"]
            g.oferecer_equip(novo)
            nomes = {s: (antigo if s == espaco else outro)["nome"] for s in ("anel1", "anel2")}
            self.assertEqual(g.ui.ofertas[-1], [f"Substituir {nomes['anel1']} (Anel 1)",
                                                f"Substituir {nomes['anel2']} (Anel 2)", "Guardar na mochila"])
            self.assertIs(g.j.equip[espaco], novo)
            self.assertIs(g.j.equip[fica], outro)  # o outro anel não sai
            self.assertIn(antigo, g.j.mochila)

    def test_um_vazio_diz_que_esta_vazio(self):
        g, novo = heroi(Tela(), aneis=1)
        rei = g.j.equip["anel1"]
        g.ui.roteiro = ["Equipar no Anel 2 (vazio)"]
        g.oferecer_equip(novo)
        self.assertEqual(g.ui.ofertas[-1][:2], [f"Substituir {rei['nome']} (Anel 1)", "Equipar no Anel 2 (vazio)"])
        self.assertEqual((g.j.equip["anel1"], g.j.equip["anel2"]), (rei, novo))
        self.assertEqual(g.j.mochila, [])
        # a tela recebe os dois espaços, cada um com o nome e o que tem
        _, dados = next(p for p in g.ui.paineis if p[0] == "achado")
        self.assertEqual([(e["espaco"], e["nome"], e["item"] and e["item"]["nome"]) for e in dados["espacos"]],
                         [("anel1", "Anel 1", itens.rotulo(rei)), ("anel2", "Anel 2", None)])

    def test_nenhum_anel_equipa_sem_perguntar(self):
        g, novo = heroi(Tela(), aneis=0)
        g.ui.roteiro = ["Equipar agora"]
        g.oferecer_equip(novo)
        self.assertIs(g.j.equip["anel1"], novo)

    def test_so_o_anel_leva_os_espacos(self):
        g, _ = heroi(Tela())
        g.ui.roteiro = ["Guardar"]
        g.oferecer_equip(gerar_equip(random.Random(1), "guerreiro", 3, slot="arma"))
        _, dados = next(p for p in g.ui.paineis if p[0] == "achado")
        self.assertNotIn("espacos", dados)
        self.assertIn("Equipar agora", g.ui.ofertas[-1])

    def test_no_texto_os_dois_espacos_e_os_botoes(self):
        g, novo = heroi(Roteiro(), aneis=1)
        g.ui.roteiro = ["Guardar"]
        g.oferecer_equip(novo)
        texto = "\n".join(g.ui.ditos)
        self.assertIn("  Anel 1: ", texto)
        self.assertIn("  Anel 2: vazio", texto)
        self.assertIn("Equipar no Anel 2 (vazio)", g.ui.ofertas[-1])

    def test_mochila_cheia_substituir_deixa_o_antigo(self):
        g, novo = heroi(Tela())
        g.j.mochila = [gerar_equip(random.Random(k), "guerreiro", 2) for k in range(12)]
        antigo = g.j.equip["anel2"]
        g.ui.roteiro = [f"Substituir {antigo['nome']}"]
        g.oferecer_equip(novo)
        self.assertIs(g.j.equip["anel2"], novo)
        self.assertNotIn(antigo, g.j.mochila)
        self.assertEqual(len(g.j.mochila), 12)


class TestMochila(unittest.TestCase):
    def test_no_texto_pergunta_qual_substituir(self):
        g, novo = heroi(Roteiro())
        g.j.mochila.append(novo)
        antigo = g.j.equip["anel2"]
        g.ui.roteiro = ["Substituir " + antigo["nome"]]
        self.assertEqual(g.escolher_espaco(novo), "anel2")
        self.assertTrue(g.ui.ofertas[-1][1].startswith(f"Substituir {antigo['nome']} (Anel 2) — "))
        g.ui.roteiro = ["Voltar"]
        self.assertIsNone(g.escolher_espaco(novo))

    def test_no_texto_vai_para_o_vazio_sem_perguntar(self):
        g, novo = heroi(Roteiro(), aneis=1)
        self.assertEqual(g.escolher_espaco(novo), "anel2")
        self.assertEqual(g.ui.ofertas, [])

    def test_mercado_oferece_um_equipar_por_espaco(self):
        g, novo = heroi(Tela())
        g.j.mochila.append(novo)
        espada = gerar_equip(random.Random(1), "guerreiro", 3, slot="arma")
        g.j.mochila.append(espada)
        antigo = g.j.equip["anel1"]
        g.ui.roteiro = ["Sair do mercado"]
        g.ui.metas = []
        menu = g.menu

        def anotar(pergunta, opcoes):
            g.ui.metas.append([o[2] if len(o) > 2 else None for o in opcoes if o])
            return menu(pergunta, opcoes)
        g.menu = anotar
        g.loja()
        metas = [m for m in g.ui.metas[0] if m and "equipar" in m]
        self.assertEqual(metas, [{"equipar": 0, "destino": "anel1"}, {"equipar": 0, "destino": "anel2"}, {"equipar": 1}])
        g.menu = menu
        g.equipar(novo, "anel1")
        self.assertIs(g.j.equip["anel1"], novo)
        self.assertIn(antigo, g.j.mochila)


if __name__ == "__main__":
    unittest.main()


class TestDestinoDoAntigo(unittest.TestCase):
    """O que a tela conta ao equipar segue a transferência real (1.88.1): no espaço vazio, só o novo entra (nada "foi
    para a mochila"); substituindo, o antigo vai para a mochila; com ela cheia, fica para trás. Nos dois anéis."""

    def equipado(self, g):
        festas = []
        g.ui.celebrar = lambda tipo, dados: festas.append((tipo, dados))
        return festas

    def test_achado_nos_dois_espacos(self):
        for espaco in ("anel1", "anel2"):
            g, novo = heroi(Tela(), aneis=1)
            if espaco == "anel1":  # o vazio é o Anel 1
                g.j.equip["anel2"], g.j.equip["anel1"] = g.j.equip["anel1"], None
            festas = self.equipado(g)
            g.ui.roteiro = [f"Equipar no {'Anel 1' if espaco == 'anel1' else 'Anel 2'} (vazio)"]
            g.oferecer_equip(novo)
            self.assertEqual([(t, d["espaco"], d["antigo"]) for t, d in festas], [("equipou", espaco, None)])
            self.assertEqual(g.j.mochila, [])

    def test_achado_substituindo_e_com_a_mochila_cheia(self):
        for cheia, destino in ((False, "mochila"), (True, "ficou")):
            g, novo = heroi(Tela())
            if cheia:
                g.j.mochila = [gerar_equip(random.Random(k), "guerreiro", 2) for k in range(12)]
            antigo = g.j.equip["anel2"]
            festas = self.equipado(g)
            g.ui.roteiro = [f"Substituir {antigo['nome']}"]
            g.oferecer_equip(novo)
            self.assertEqual([(d["espaco"], d["antigo"]) for _, d in festas], [("anel2", destino)])
            self.assertEqual(antigo in g.j.mochila, not cheia)

    def test_inventario_e_mercado_devolvem_o_que_aconteceu(self):
        g, novo = heroi(Roteiro(), aneis=1)
        g.j.mochila.append(novo)
        self.assertIsNone(g.equipar(novo, "anel2"))  # o espaço vazio: nada sai
        outro = gerar_equip(random.Random(9), "guerreiro", 4, slot="anel")
        g.j.mochila.append(outro)
        velho = g.j.equip["anel1"]
        self.assertEqual(g.equipar(outro, "anel1"), "mochila")
        self.assertIn(velho, g.j.mochila)
