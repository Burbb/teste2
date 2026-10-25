"""O catálogo de antagonistas (guardado para a expansão da campanha desde a retirada do mundo gerado, 1.206.0): as
origens concordam com o gênero do título (1.199.2), e a ficha de luta sai de qualquer combinação."""

import unittest

from rpg.dados import ANTAGONISTAS, ORIGENS_ANTAGONISTA
from rpg.inimigos import instanciar_antagonista

# As formas que só cabem num gênero (nas origens).
SO_MASCULINO = ("um herói", "nascido ", "o bispo", "ajoelhado", "seu inimigo", "velho conhecido", "que ele ")
SO_FEMININO = ("uma heroína", "nascida ", "a bispa", "ajoelhada", "sua inimiga", "velha conhecida", "que ela ")


def antagonista(titulo, g, origem):
    return {"nome": f"Vharuk, {titulo}", "curto": titulo, "g": g,
            "origem": ORIGENS_ANTAGONISTA[origem][1 if g == "f" else 0]}


class TestCatalogo(unittest.TestCase):
    def test_os_oito_titulos_com_as_cinco_origens(self):
        self.assertEqual((len(ANTAGONISTAS), len(ORIGENS_ANTAGONISTA)), (8, 5))
        for titulo, g in ANTAGONISTAS:
            for i, formas in enumerate(ORIGENS_ANTAGONISTA):
                origem = formas[1 if g == "f" else 0]
                frase = f"Do outro lado fala Vharuk, {titulo}, {origem}."
                errado = SO_MASCULINO if g == "f" else SO_FEMININO
                with self.subTest(titulo=titulo, origem=i):
                    self.assertFalse([x for x in errado if x in frase], frase)

    def test_as_formas_so_mudam_o_genero(self):
        # o conteúdo é o mesmo: as duas formas diferem só nas palavras que concordam
        for m, f in ORIGENS_ANTAGONISTA:
            self.assertEqual(len(m.split()), len(f.split()))
            self.assertLessEqual(sum(a != b for a, b in zip(m.split(), f.split())), 2, (m, f))

    def test_a_ficha_de_luta_de_cada_titulo(self):
        for titulo, g in ANTAGONISTAS:
            chefe = instanciar_antagonista(antagonista(titulo, g, 0), 10)
            self.assertEqual(chefe.nome, f"Vharuk, {titulo}")
            self.assertEqual(chefe.familia, "antagonista")
            self.assertGreater(chefe.max_hp, 0)


if __name__ == "__main__":
    unittest.main()
