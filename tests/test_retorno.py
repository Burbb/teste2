"""A volta ao Vau depois da guardiã (fim da E3) e a primeira consequência local (E4): a cena de retorno, uma vez, que
conclui a missão; o Diário com a conclusão; a herança de Berta antes ou depois de concluir; a Fonte Nova e a frase da
vila pelos dias desde o desfecho; Pita e Marta na curandeira; saves e o mundo gerado."""

import json
import tempfile
import unittest

from rpg import consequencias, missoes
from rpg import sobrevivencia
from rpg.jogo import Jogo
from rpg.web.estado import estado
from tests.test_missoes import MID, Roteiro, campanha, ir


def resolvida(desfecho, ui=None, pasta=None, heranca=False, dias=0):
    """Campanha com a guardiã resolvida `dias` atrás e o herói chegando ao Vau (a cena de retorno ainda por tocar)."""
    g = campanha("guerreiro", ui, pasta)
    m = missoes.registro(g, MID)
    g.dia = 10
    m.update(etapa="retorno", cenas=["abertura", "capela_exterior"] + (["heranca"] if heranca else []),
             pistas=["agua_do_leste", "ilse"], preparos=["corpo_solto", "fita"], desfecho=desfecho,
             dia_desfecho=g.dia - dias)
    ir(g, "vau_do_turvo")
    g.periodo = 0
    return g


class TestRetorno(unittest.TestCase):
    def test_retorno_conclui_uma_vez_nos_dois_desfechos(self):
        for desfecho in ("descansada", "destruida"):
            ui = Roteiro()
            g = resolvida(desfecho, ui)
            self.assertEqual(len(estado(g)["missoes"]), 1)  # antes: o objetivo de voltar ao Vau
            self.assertTrue(missoes.cena_pendente(g))
            self.assertEqual(ui.cenas[-1], "De Volta ao Vau")
            m = missoes.registro(g, MID)
            self.assertEqual(m["concluida"], g.dia)
            self.assertEqual(estado(g)["missoes"], [])  # nem rastreador nem marcador
            self.assertEqual(missoes.cartoes(g), [])
            cartao = missoes.cartoes(g, todas=True)[0]  # o Diário guarda tudo
            self.assertEqual((cartao["concluida"], cartao["desfecho"]), (g.dia, desfecho))
            self.assertIn(missoes.CONCLUSAO[desfecho], cartao["conclusao"])
            self.assertEqual(len(cartao["pistas"]), 2)
            self.assertEqual(len(cartao["preparos"]), 2)
            self.assertFalse(missoes.cena_pendente(g))  # repetir a visita não toca de novo
            self.assertEqual(m["concluida"], g.dia)
            self.assertEqual(ui.continuares[-1], ("De Volta ao Vau", True))

    def test_retorno_imediato_e_tardio(self):
        casos = [("destruida", 0, "corre escura"), ("destruida", 2, "cor de chá fraco"), ("descansada", 0, "lodo assentou"),
                 ("descansada", 6, "corre clara")]
        for desfecho, dias, trecho in casos:
            ui = Roteiro()
            g = resolvida(desfecho, ui, dias=dias)
            missoes.cena_pendente(g)
            texto = " ".join(ui.ditos)
            self.assertIn(trecho, texto, (desfecho, dias))
            self.assertEqual("Marta está na porta" in texto, consequencias.marta_de_pe(g), (desfecho, dias))

    def test_heranca_depois_de_concluir(self):
        ui = Roteiro(["Guardar"])
        g = resolvida("descansada", ui)
        missoes.cena_pendente(g)
        self.assertEqual(missoes.cartoes(g, todas=True)[0]["pendente"], "Vó Berta ainda espera você na taverna.")
        opcao = next(o for o in missoes.opcoes(g) if o[1][2] == "heranca")
        self.assertEqual(opcao[2]["predio"], "taverna")
        antes = len(g.j.mochila)
        self.assertTrue(missoes.executar(g, MID, "heranca"))
        self.assertEqual(len(g.j.mochila), antes + 1)
        self.assertFalse(missoes.executar(g, MID, "heranca"))
        self.assertIsNone(missoes.cartoes(g, todas=True)[0]["pendente"])
        self.assertEqual(len(g.j.mochila), antes + 1)

    def test_heranca_antes_de_concluir(self):
        """Um save da 1.53 em que a herança já foi recebida na volta: a cena de retorno toca e não pede a herança."""
        ui = Roteiro()
        g = resolvida("descansada", ui, heranca=True)
        missoes.cena_pendente(g)
        self.assertNotIn("ergue a caneca", " ".join(ui.ditos))
        self.assertIsNone(missoes.cartoes(g, todas=True)[0]["pendente"])
        self.assertFalse([o for o in missoes.opcoes(g) if o[1][2] == "heranca"])

    def test_destruir_nao_deixa_heranca_pendente(self):
        g = resolvida("destruida")
        missoes.cena_pendente(g)
        self.assertIsNone(missoes.cartoes(g, todas=True)[0]["pendente"])
        self.assertFalse(missoes.opcoes(g))


class Pergunta(Roteiro):
    """Anota também o texto de cada pergunta (no modo texto, a curandeira fala na pergunta)."""

    def __init__(self, roteiro=()):
        super().__init__(roteiro)
        self.perguntas = []

    def escolher(self, pergunta, opcoes):
        self.perguntas.append(pergunta)
        return super().escolher(pergunta, opcoes)


class TestFonteEMarta(unittest.TestCase):
    def estados(self, desfecho, ate=6):
        g = resolvida(desfecho)
        saida = []
        for _ in range(ate):
            saida.append((consequencias.estado_fonte(g), consequencias.atendente(g)["quem"].split(",")[0]))
            g.dia += 1
        return saida

    def test_dar_descanso_limpa_sem_piora(self):
        self.assertEqual(self.estados("descansada", 4), [("limpando", "Pita"), ("limpando", "Pita"), ("limpa", "Marta"),
                                                          ("limpa", "Marta")])

    def test_destruir_escurece_uma_noite_e_depois_recupera(self):
        self.assertEqual(self.estados("destruida", 5), [("escura", "Pita"), ("limpando", "Pita"), ("limpando", "Pita"),
                                                         ("limpa", "Marta"), ("limpa", "Marta")])

    def test_frase_da_vila_difere_entre_os_desfechos(self):
        limpa = {}
        for desfecho in ("descansada", "destruida"):
            g = resolvida(desfecho, dias=5)
            limpa[desfecho] = consequencias.frase_da_vila(g)
        self.assertIn("fita", limpa["descansada"])
        self.assertIn("ninguém fala da capela", limpa["destruida"])
        g = resolvida("destruida")
        self.assertIn("corre escura", consequencias.frase_da_vila(g))
        ir(g, "bosque_do_moinho")
        self.assertIsNone(consequencias.frase_da_vila(g))  # só no Vau
        self.assertIsNone(consequencias.atendente(g))

    def test_frase_aparece_no_menu_da_vila(self):
        ui = Roteiro(["Sair do jogo", "Cancelar"])
        g = resolvida("descansada", ui, dias=5)
        missoes.registro(g, MID)["concluida"] = g.dia
        missoes.registro(g, MID)["cenas"].append("retorno")
        g.tela()
        self.assertIn(consequencias.FRASES[("descansada", "limpa")], ui.ditos)

    def test_antes_do_desfecho_pita_atende_e_a_vila_e_a_de_sempre(self):
        g = campanha()
        self.assertIsNone(consequencias.estado_fonte(g))
        self.assertTrue(consequencias.atendente(g)["quem"].startswith("Pita"))
        self.assertIsNone(consequencias.frase_da_vila(g))
        self.assertEqual(estado(g)["local"]["atendentes"], {"curandeiro": "Pita, a aprendiz de Marta"})
        self.assertIn("Pita", estado(g)["local"]["predios_fechados"]["curandeiro"])

    def test_curandeira_com_as_regras_de_sempre(self):
        """Quem atende muda (Pita, depois Marta); o preço e o tratamento são os de sempre."""
        for dias, quem in ((0, "Pita"), (5, "Marta")):
            ui = Pergunta()
            g = resolvida("descansada", ui, dias=dias)
            fid = next(f for f in sobrevivencia.FERIMENTOS if f != "infeccao")
            sobrevivencia.ferir(g, fid)
            ui.roteiro = [sobrevivencia.FERIMENTOS[fid]["nome"], "Voltar"]
            g.j.ouro = 200
            g.curandeiro()
            self.assertFalse(g.j.ferimentos)
            self.assertEqual(g.j.ouro, 200 - g.preco(12 + 3 * g.j.nivel))
            self.assertTrue(ui.perguntas[0].startswith(quem), ui.perguntas[0])

    def test_procedural_sem_consequencias(self):
        g = Jogo(Roteiro(), seed=5, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["tipo"] == "vila")["id"]
        self.assertIsNone(consequencias.estado_fonte(g))
        self.assertIsNone(consequencias.atendente(g))
        self.assertIsNone(consequencias.frase_da_vila(g))
        self.assertNotIn("atendentes", estado(g)["local"])


class TestSaves(unittest.TestCase):
    def test_save_preserva_conclusao_fonte_e_heranca_pendente(self):
        pasta = tempfile.mkdtemp()
        g = resolvida("destruida", pasta=pasta)
        missoes.cena_pendente(g)
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
        self.assertEqual(json.dumps(missoes.registro(h, MID)), json.dumps(missoes.registro(g, MID)))
        self.assertEqual(consequencias.estado_fonte(h), "escura")
        h.dia += 3
        self.assertEqual(consequencias.estado_fonte(h), "limpa")
        self.assertFalse(missoes.cena_pendente(h))
        k = resolvida("descansada", pasta=pasta)
        missoes.cena_pendente(k)
        k.salvar(silencioso=True)
        z = Jogo.carregar(Roteiro(), k.caminho_save(), pasta)
        self.assertEqual(missoes.cartoes(z, todas=True)[0]["pendente"], "Vó Berta ainda espera você na taverna.")
        ir(z, "vau_do_turvo")
        self.assertTrue([o for o in missoes.opcoes(z) if o[1][2] == "heranca"])

    def test_save_da_153_na_etapa_retorno(self):
        """Resolvida na 1.53 (sem `dia_desfecho` nem `concluida`): ao carregar, o desfecho conta de hoje e a volta ao Vau
        conclui normalmente."""
        pasta = tempfile.mkdtemp()
        g = resolvida("destruida", pasta=pasta)
        m = g.mundo["missoes"][MID]
        del m["dia_desfecho"], m["concluida"]
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
        m = missoes.registro(h, MID)
        self.assertEqual((m["dia_desfecho"], m["concluida"]), (h.dia, None))
        self.assertTrue(missoes.cena_pendente(h))
        self.assertEqual(missoes.registro(h, MID)["concluida"], h.dia)


class TestRito(unittest.TestCase):
    def test_desistir_do_rito_tem_texto_natural(self):
        from tests.test_guardia import TestPisoDoRito
        t = TestPisoDoRito()
        g, cb, e, _ = t.luta()
        g.ui.respostas = ["Desistir do rito"]
        cb.atacar(g.j, e, 50.0)
        missoes._momento_do_rito(g, cb, e)
        texto = " ".join(g.ui.ditos)
        self.assertIn("Sem o rito, os golpes que ela vinha aguentando chegam de uma vez", texto)
        self.assertNotIn("segurava", texto)
        g.combate_ativo = None


if __name__ == "__main__":
    unittest.main()
