"""A cabeça e as mãos de couro e de tecido (1.112.0): o Capuz e a Luva de Seda do Mago com os desenhos de tecido, o
Arqueiro e as Mãos do Estrangulador com os de couro. O que decide é o próprio item (o espaço, a classe para a qual foi
feito, o desenho que ele guarda), nunca o nome nem quem o carrega."""

import random
import unittest

from rpg import itens


def _peca(classe, slot, base, icone, **extra):
    return {"nome": base, "base": base, "slot": slot, "bonus": {"defesa": 2}, "preco": 10, "classe": classe,
            "raridade": "comum", "icone": icone, "nivel": 3, **extra}


class TestItensNovos(unittest.TestCase):
    def test_cada_classe_ganha_o_seu_material(self):
        rng = random.Random(1)
        vistos = {}
        for _ in range(400):
            for classe in ("mago", "arqueiro"):
                for slot in ("cabeca", "maos"):
                    it = itens.gerar_equip(rng, classe, 6, slot=slot, raridade="comum")
                    vistos.setdefault((classe, it["base"].split()[0]), set()).add(it["icone"])
        self.assertEqual(vistos[("mago", "Capuz")], {"capuz_tecido"})
        self.assertEqual(vistos[("mago", "Luva")], {"luva_seda"})
        self.assertEqual(vistos[("arqueiro", "Capuz")], {"capuz"})
        self.assertEqual(vistos[("arqueiro", "Chapéu")], {"capuz"})       # a exceção registrada: o chapéu usa o capuz
        self.assertEqual(vistos[("arqueiro", "Braçadeira")], {"luva"})

    def test_o_unico_das_maos_continua_de_couro(self):
        u = next(u for u in itens.UNICOS if u["id"] == "maos_do_estrangulador")
        self.assertEqual(u["icone"], "luva")

    def test_item_sem_desenho_guardado_usa_a_classe_do_item(self):
        # um item de um save de antes do desenho ir no item: a base e a classe dele decidem (não quem o carrega)
        sem = lambda classe, slot, base: {k: v for k, v in _peca(classe, slot, base, None).items() if k != "icone"}
        self.assertEqual(itens.icone_de(sem("mago", "cabeca", "Capuz de Linho")), "capuz_tecido")
        self.assertEqual(itens.icone_de(sem("arqueiro", "cabeca", "Capuz Curtido")), "capuz")
        self.assertEqual(itens.icone_de(sem("mago", "maos", "Luva de Seda Bordada")), "luva_seda")
        self.assertEqual(itens.icone_de(sem("arqueiro", "maos", "Braçadeira Rúnica")), "luva")


if __name__ == "__main__":
    unittest.main()
