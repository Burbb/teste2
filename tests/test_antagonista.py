"""O antagonista do mundo gerado: o texto concorda com o gênero do título sorteado (1.199.2), sem mudar o sorteio."""

import random
import tempfile
import unittest

from rpg.dados import ANTAGONISTAS, ORIGENS_ANTAGONISTA
from rpg.eventos.biomas import eco_do_vazio
from rpg.eventos.classe import veterano_cicatrizes
from rpg.eventos.vila import ouvir_rumor
from rpg.jogo import Jogo
from rpg.mundo import gerar_mundo
from rpg.ui import BotUI

# As formas que só cabem num gênero (nas origens e nos eventos que falam do antagonista).
SO_MASCULINO = ("um herói", "nascido ", "o bispo", "ajoelhado", "seu inimigo", "velho conhecido", "que ele ")
SO_FEMININO = ("uma heroína", "nascida ", "a bispa", "ajoelhada", "sua inimiga", "velha conhecida", "que ela ")


class Anotador(BotUI):
    """Escolhe pelo texto e guarda tudo o que foi dito."""

    def __init__(self, roteiro=()):
        super().__init__(random.Random(1), max_decisoes=20)
        self.roteiro, self.falas = list(roteiro), []

    def dizer(self, texto="", cor=None):
        self.falas.append(texto)

    def narrar(self, texto, cor=None):
        self.falas.append(texto)

    def escolher(self, pergunta, opcoes):
        alvo = self.roteiro.pop(0) if self.roteiro else ""
        return next((i for i, o in enumerate(opcoes) if alvo in o), 0)


def com_antagonista(titulo, g, origem, roteiro=()):
    ui = Anotador(roteiro)
    jogo = Jogo(ui, seed=8, pasta_saves=tempfile.mkdtemp())
    jogo.iniciar("Teste", "guerreiro")
    jogo.mundo["antagonista"] = {"nome": f"Vharuk, {titulo}", "curto": titulo, "g": g,
                                 "origem": ORIGENS_ANTAGONISTA[origem][1 if g == "f" else 0]}
    ui.falas.clear()
    return jogo, ui


class TestConcordancia(unittest.TestCase):
    def test_o_sorteio_continua_do_mesmo_tamanho(self):
        # a sequência aleatória depende do tamanho das listas: 8 títulos, 5 origens (cada uma nas duas formas)
        self.assertEqual(len(ANTAGONISTAS), 8)
        self.assertEqual(len(ORIGENS_ANTAGONISTA), 5)
        self.assertTrue(all(len(o) == 2 for o in ORIGENS_ANTAGONISTA))

    def test_os_oito_titulos_com_as_cinco_origens(self):
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

    def test_o_mundo_sorteia_a_forma_do_titulo(self):
        for seed in range(40):
            a = gerar_mundo(random.Random(seed))["antagonista"]
            formas = next(o for o in ORIGENS_ANTAGONISTA if a["origem"] in o)
            self.assertEqual(a["origem"], formas[1 if a["g"] == "f" else 0], seed)

    def test_eco_do_vazio(self):
        for titulo, g in (("Noiva da Peste", "f"), ("Rei Enforcado", "m")):
            jogo, ui = com_antagonista(titulo, g, 0)
            jogo.teste = lambda *a, **k: True
            eco_do_vazio(jogo)
            texto = " ".join(ui.falas)
            self.assertIn("ajoelhada" if g == "f" else "ajoelhado", texto)
            self.assertIn("sua inimiga" if g == "f" else "seu inimigo", texto)

    def test_a_historia_da_taverna(self):
        for titulo, g in (("Mãe das Ninhadas", "f"), ("Arcebispo Profanado", "m")):
            jogo, ui = com_antagonista(titulo, g, 3)
            ouvir_rumor(jogo, preferir="lore")
            texto = " ".join(ui.falas)
            self.assertIn("a bispa que abriu" if g == "f" else "o bispo que abriu", texto)
            self.assertIn("Dizem que ela ainda" if g == "f" else "Dizem que ele ainda", texto)

    def test_o_veterano_fala_dela_sem_mudar_o_dele(self):
        jogo, ui = com_antagonista("Rainha das Moscas", "f", 2, roteiro=["Ouvir as histórias"])
        veterano_cicatrizes(jogo)
        fala = next(t for t in ui.falas if "Rainha das Moscas" in t)
        self.assertEqual(fala, "Ele fala sobre Rainha das Moscas como quem fala de uma velha conhecida.")


if __name__ == "__main__":
    unittest.main()
