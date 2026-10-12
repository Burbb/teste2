"""A área de condições do herói (fora das barras): a fome, com o efeito de agora, e o que a faz sumir (comer no
amanhecer, o ensopado da taverna, comida comprada, o resgate). As regras da fome não mudam: só o que a tela recebe."""

import unittest

from rpg import comitiva as cm, sobrevivencia
from rpg.comitiva.fogueira import NOTA_ACAMPAMENTO
from rpg.web.estado import estado
from tests.test_recuperacao import cair_de_noite, faminto, no_charco


class TestFome(unittest.TestCase):
    def test_sem_fome_nada(self):
        g = no_charco()
        self.assertEqual(sobrevivencia.condicoes(g.j), [])
        self.assertEqual(estado(g)["heroi"]["condicoes"], [])

    def test_o_efeito_de_agora_pelos_dias(self):
        g = no_charco()
        for dias, texto, pct, aviso in ((1, "Com fome", 10, None), (2, "Com fome", 20, "começa a se consumir"),
                                        (3, "Morrendo de fome", 35, "Cada amanhecer sem comer tira")):
            g.j.fome = dias
            g.j.recalcular()
            [c] = sobrevivencia.condicoes(g.j)
            self.assertEqual((c["id"], c["texto"]), ("fome", texto))
            self.assertEqual(c["dica"][0], f"Ataque, Poder, Agilidade e vida máxima −{pct}%.")
            self.assertIn("30% da vida", c["dica"][1])
            if aviso:  # do segundo dia em diante, o que vem se ela continuar
                self.assertTrue(any(aviso in linha for linha in c["dica"]), dias)
            else:
                self.assertEqual(len(c["dica"]), 3)
        self.assertIn(f"tira {sobrevivencia.perda_fome(g.j)} de vida", " ".join(c["dica"]))

    def test_some_ao_comer(self):
        g = no_charco(provisoes=2)
        g.j.fome = 1
        g.novo_dia(descanso=1)  # o amanhecer come 1 provisão
        self.assertEqual(sobrevivencia.condicoes(g.j), [])
        g.j.fome = 1
        sobrevivencia.amanhecer(g, 2, refeicao=True)  # o ensopado da taverna
        self.assertEqual(sobrevivencia.condicoes(g.j), [])
        g.j.fome = 1
        g.dar_provisoes(1)  # comida comprada ou achada: come na hora
        self.assertEqual(sobrevivencia.condicoes(g.j), [])

    def test_some_no_resgate(self):
        g = faminto(no_charco(ouro=0))
        self.assertTrue(sobrevivencia.condicoes(g.j))
        g.resgate(cair_de_noite(g))
        self.assertEqual(estado(g)["heroi"]["condicoes"], [])


class TestFogueira(unittest.TestCase):
    def test_contador_e_nota_vem_do_motor(self):
        g = no_charco()
        for cid in ("yara", "morel"):
            cm.recrutar(g, cid)
        cm.para_acampamento(g, "yara", silencioso=True)
        dados = {}
        g.ui.painel = lambda tipo, d: dados.setdefault(tipo, d) and False
        g.ui.roteiro = ["Dormir"]
        cm.fogueira(g)
        d = dados["acampamento"]
        self.assertEqual((d["contador"], d["nota_acampamento"]), (f"Comitiva 1/{cm.LIMITE}", NOTA_ACAMPAMENTO))
        self.assertEqual([m["id"] for m in d["ativos"]], ["morel"])
        self.assertEqual([m["id"] for m in d["reserva"]], ["yara"])

    def test_ferido_com_a_concordancia(self):
        g = no_charco()
        for cid in ("odete", "morel"):
            cm.recrutar(g, cid)
            cm.membro(g, cid)["ferido"] = True
        txt = {m["id"]: m["ferido_txt"] for m in cm.estado(g)}
        self.assertEqual(txt, {"odete": "ferida, fora de combate", "morel": "ferido, fora de combate"})


if __name__ == "__main__":
    unittest.main()
