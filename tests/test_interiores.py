"""Os interiores dos balcões da vila (o templo, desde a 1.219.0): o motor manda a cena; a tela só a mostra diante do
prédio, com ou sem alguém para cuidar."""
import unittest

from rpg.sistemas.servicos import cena_templo
from rpg.web.estado import estado
from tests.test_missoes import campanha


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


if __name__ == "__main__":
    unittest.main()
