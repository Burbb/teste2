"""O fim do primeiro capítulo (E9): a cena curta no Vau depois da febre e da resposta a Caspar, uma vez; o que ela diz
de cada desfecho; o rastreador e o Diário; os saves que já tinham tudo resolvido; e o que ela não faz (abrir Varn,
dar recompensa, tirar a herança de Berta, interromper uma luta)."""

import tempfile
import unittest

from rpg import capitulo, caspar, missoes
from rpg.jogo import Jogo
from rpg.web.estado import estado
from tests.test_caspar import com_yara, resolvida
from tests.test_missoes import Roteiro, ir

TITULO = capitulo.TITULO


def concluido(desfecho="descansada", postura="calar", yara="desconhecida", dias=1, pasta=None, ui=None):
    """As duas missões concluídas, no Vau, com a cena do fim ainda por ver (o que a praça deixa)."""
    g = com_yara(resolvida(desfecho, ui or Roteiro(), pasta=pasta, dias=dias), yara)
    v = caspar.registro(g)
    v["cenas"].append("praca")
    v.update(desfecho=postura, dia_desfecho=g.dia, concluida=g.dia, yara_na_praca=yara)
    return g


def texto(g):
    return " ".join(g.ui.ditos)


class TestCena(unittest.TestCase):
    def test_toca_uma_vez_no_vau(self):
        g = concluido()
        self.assertTrue(missoes.cena_pendente(g))
        self.assertEqual(g.ui.cenas[-1], TITULO)
        self.assertEqual(g.ui.continuares[-1], (TITULO, True))
        self.assertIn(capitulo.AVISO, texto(g))
        self.assertFalse(missoes.cena_pendente(g))
        self.assertEqual(g.ui.cenas.count(TITULO), 1)

    def test_logo_depois_da_praca(self):
        ui = Roteiro(["Calar"])
        g = resolvida("descansada", ui)
        self.assertTrue(missoes.cena_pendente(g))  # a praça: Caspar reivindica; o herói se cala
        self.assertEqual(ui.cenas[-1], "A Praça do Vau")
        self.assertTrue(missoes.cena_pendente(g))  # na tela seguinte, o fim do capítulo
        self.assertEqual(ui.cenas[-1], TITULO)
        self.assertFalse(missoes.cena_pendente(g))

    def test_nao_antes_da_resposta_nem_fora_do_vau(self):
        ui = Roteiro(["Ainda não"])
        g = resolvida("destruida", ui)
        missoes.cena_pendente(g)  # a praça, sem resposta
        self.assertFalse(missoes.cena_pendente(g))
        self.assertFalse(capitulo.concluido(g))
        g = concluido()
        ir(g, "charco_dos_juncos")
        self.assertFalse(missoes.cena_pendente(g))
        ir(g, "vau_do_turvo")
        g.combate_ativo = object()  # numa luta, nada de cena
        self.assertFalse(missoes.cena_pendente(g))
        g.combate_ativo = None
        self.assertTrue(missoes.cena_pendente(g))

    def test_nao_abre_varn_nem_da_nada(self):
        g = concluido()
        antes = (g.j.ouro, g.j.xp, len(g.j.mochila), dict(g.j.consumiveis), g.j.reputacao)
        missoes.cena_pendente(g)
        self.assertEqual((g.j.ouro, g.j.xp, len(g.j.mochila), dict(g.j.consumiveis), g.j.reputacao), antes)
        from rpg import campanha
        self.assertIn("estrada_de_varn", campanha.REGIOES["turvo"]["fechados"])
        self.assertEqual([c for c in missoes.cartoes(g) if not c["concluida"]], [])  # nenhuma missão nova

    def test_heranca_continua_na_taverna(self):
        g = concluido("descansada")
        self.assertTrue(missoes.heranca_pendente(missoes.registro(g, "febre_do_turvo")))
        missoes.cena_pendente(g)
        self.assertIn("Vó Berta ainda espera você na taverna.", texto(g))
        self.assertIn(("febre_do_turvo", "heranca"), [o[1][1:] for o in missoes.opcoes(g)])
        g = concluido("destruida")
        missoes.cena_pendente(g)
        self.assertNotIn("Vó Berta", texto(g))

    def test_campanha_nova_sem_capitulo(self):
        g = Jogo(Roteiro(), seed=5, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        self.assertFalse(capitulo.concluido(g))
        self.assertNotIn("capitulo", estado(g))


class TestDesfechos(unittest.TestCase):
    def test_fonte_e_marta_no_estado_de_agora(self):
        casos = [("destruida", 0, "ainda está escura", "Marta piorou"),
                 ("destruida", 2, "já não corre preta", "Marta ainda está de cama"),
                 ("descansada", 1, "está clareando", "Marta ainda está de cama"),
                 ("descansada", 5, "está limpa de novo", "Marta voltou a atender")]
        for desfecho, dias, agua, marta in casos:
            g = concluido(desfecho, dias=dias)
            missoes.cena_pendente(g)
            self.assertIn(agua, texto(g), (desfecho, dias))
            self.assertIn(marta, texto(g), (desfecho, dias))

    def test_ilse_caspar_yara(self):
        casos = [("descansada", "denunciado", "grupo", "fita de Berta", "foi embora do Vau", "Yara anda livre"),
                 ("destruida", "apoiar", "grupo", "queimados na praça", "vigília de Caspar reúne",
                  "não a deixa entrar no Vau"),
                 ("destruida", "calar", "desconhecida", "fundo da capela, sem nome", "a praça continua dele",
                  "culpa a moça do Charco dos Juncos"),
                 ("descansada", "denuncia_falhou", "morta", "fita de Berta", "a vigília dele acabou",
                  "morreu na fogueira"),
                 ("destruida", "denunciado", "desconhecida", "sem nome", "foi embora", "Ninguém mais procura")]
        for desfecho, postura, yara, ilse, caspar_, yara_ in casos:
            g = concluido(desfecho, postura, yara)
            missoes.cena_pendente(g)
            for trecho in (ilse, caspar_, yara_):
                self.assertIn(trecho, texto(g), (desfecho, postura, yara))

    def test_nao_repete_a_frase_da_vila(self):
        """A frase da vila (a Fonte e a praça) aparece logo depois da cena: nenhum trecho dela se repete na cena."""
        from rpg import consequencias
        for desfecho, dias in (("descansada", 0), ("descansada", 1), ("descansada", 5), ("destruida", 0),
                               ("destruida", 2), ("destruida", 5)):
            for postura in ("apoiar", "denunciado", "denuncia_falhou", "calar"):
                g = concluido(desfecho, postura, dias=dias)
                missoes.cena_pendente(g)
                for frase in consequencias.frase_da_vila(g).replace(":", ".").split(". "):
                    for pedaco in frase.split(", "):
                        if len(pedaco) > 18:
                            self.assertNotIn(pedaco.strip(' ."'), texto(g), (desfecho, dias, postura))


class TestTela(unittest.TestCase):
    def test_rastreador_e_diario(self):
        g = concluido()
        self.assertEqual(estado(g)["capitulo"], capitulo.para_tela(g))
        self.assertEqual(estado(g)["capitulo"]["texto"], "Primeiro capítulo concluído.")
        ui = Roteiro(["Fechar"])
        g.ui = ui
        g.diario()
        self.assertEqual(ui.paineis[-1][1]["capitulo"]["nome"], TITULO)
        self.assertIn("Primeiro capítulo concluído.", texto(g))  # no texto, a linha no alto do Diário

    def test_antes_do_fim_nada(self):
        g = resolvida("descansada")
        self.assertIsNone(capitulo.para_tela(g))
        self.assertNotIn("capitulo", estado(g))


class TestSaves(unittest.TestCase):
    def test_save_ja_concluido_recebe_a_cena_sem_repetir_as_outras(self):
        pasta = tempfile.mkdtemp()
        g = concluido(pasta=pasta)
        ir(g, "bosque_do_moinho")
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
        self.assertFalse(missoes.cena_pendente(h))  # longe do Vau: espera
        ir(h, "vau_do_turvo")
        self.assertTrue(missoes.cena_pendente(h))
        self.assertEqual(h.ui.cenas, [TITULO])  # nem a volta ao Vau nem a praça de novo
        h.salvar(silencioso=True)
        k = Jogo.carregar(Roteiro(), h.caminho_save(), pasta)
        self.assertFalse(missoes.cena_pendente(k))


if __name__ == "__main__":
    unittest.main()
