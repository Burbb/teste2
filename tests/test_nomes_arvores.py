"""As árvores vivas com o nome novo (1.181.0): o ent jovem é a árvore desperta e o Ent Ancião, a Árvore Anciã. Os ids,
os números e as regras ficam; o nome, o plural e o gênero vêm do catálogo. Um save de antes (formato 5) carrega com os
nomes novos no guardião, nos rumores e nos contratos (o teste desse save, do mundo gerado, saiu com ele na 1.206.0)."""

import random
import unittest

from rpg.dados import FAMILIAS
from rpg.inimigos import GUARDIOES, criar, gerar_guardiao, instanciar_guardiao
from rpg.sistemas.contratos import desc_alvo, desc_caca

ANCIA = next(t for t in GUARDIOES["floresta"] if t["id"] == "ent_anciao")


class TestNomes(unittest.TestCase):
    def test_catalogo(self):
        f = FAMILIAS["ent_jovem"]
        self.assertEqual((f["nome"], f["plural"], f["g"]), ("árvore desperta", "árvores despertas", "f"))
        self.assertEqual((f["hp"], f["atk"], f["habs"], f["tracos"]), (40, 8, ["esmagar", "regenerar"], ["planta", "blindado"]))
        self.assertEqual((ANCIA["base"], ANCIA["g"], ANCIA["hp"]), ("Árvore Anciã", "f", 160))

    def test_concordancia(self):
        r = random.Random(1)
        self.assertEqual(criar(r, "ent_jovem", 3, "corrompido").nome, "Árvore desperta Corrompida")
        self.assertEqual(criar(r, "ent_jovem", 3, "anciao", "Grum").nome, "Grum, a Árvore desperta Anciã")
        self.assertEqual(desc_caca(3, "ent_jovem", "Bosque X"), "Eliminar 3 árvores despertas em Bosque X.")
        self.assertEqual(desc_alvo("Grum", "ent_jovem", "Bosque X"), "Caçar Grum, uma árvore desperta enorme que aterroriza Bosque X.")
        while (spec := gerar_guardiao(r, "floresta"))["id"] != "ent_anciao":
            pass
        self.assertTrue(spec["nome"].endswith(", a Árvore Anciã"), spec["nome"])
        self.assertEqual(instanciar_guardiao(spec, 5).nome, spec["nome"])


if __name__ == "__main__":
    unittest.main()
