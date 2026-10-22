"""Os cenários do navegador (tests/navegador/cenarios.py) montam a situação pedida sem quebrar: a fumaça e as capturas
dependem deles."""

import os
import unittest
from unittest import mock

from rpg import comitiva as cm
from tests.navegador import cenarios
from tests.test_missoes import Roteiro


class Parar(Exception):
    pass


class Fogueira(Roteiro):
    """Acampa, conversa com a Yara (que espera no acampamento) e para de volta à fogueira, com as opções de lá."""

    def __init__(self):
        super().__init__()
        self.conversou = False
        self.fogueira = None

    def escolher(self, pergunta, opcoes):
        self.ofertas.append(list(opcoes))
        if "Dormir até o amanhecer" in opcoes:  # a fogueira
            if self.conversou:
                self.fogueira = list(opcoes)
                raise Parar
            self.conversou = True
            return next(i for i, o in enumerate(opcoes) if o.startswith("Conversar com Yara"))
        return next((i for i, o in enumerate(opcoes) if o == "Acampar"), 0)  # na conversa, a primeira resposta


class TestCenarioFogueira(unittest.TestCase):
    def test_conversa_com_quem_espera_no_acampamento(self):
        """CONVERSA=1 com alguém na RESERVA: quem espera não está em cm.membro, só na reserva (quebrava ao montar).
        Na fogueira, a conversa dela acontece uma vez, ela continua esperando e a de quem anda junto continua lá."""
        ui = Fogueira()
        with mock.patch.dict(os.environ, {"CONVERSA": "1", "RESERVA": "yara", "COMITIVA": "morel"}):
            with self.assertRaises(Parar):
                cenarios.fogueira(ui)
        g = ui.jogo
        yara, morel = cm.na_reserva(g, "yara"), cm.membro(g, "morel")
        self.assertEqual((yara["conversas"], yara["ultima_conversa"]), (1, g.dia))
        self.assertEqual(morel["conversas"], 0)
        self.assertIn("Conversar com Morel  ✉", ui.fogueira)
        self.assertIn("Conversar com Yara", ui.fogueira)  # a fala à toa: sem o ✉, sem repetir a conversa
        self.assertIn("Levar Yara amanhã", ui.fogueira)


if __name__ == "__main__":
    unittest.main()
