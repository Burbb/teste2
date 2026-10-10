"""A consolidação da E4: a Yara depois da praça. O encontro no Charco quando a vigília acabou (uma vez, sem sorteio,
respeitando onde ela está), a Yara barrada que espera fora do Vau (continua na comitiva, mas ali não luta, não opina,
não conversa e não é cuidada; na estrada volta), a conversa dela sobre a praça (uma vez, sem aprovação nova, conforme o
que viu) e os textos do mundo gerado que contradiziam o Vau."""

import tempfile
import unittest

from rpg import caspar, comitiva as cm, consequencias, missoes
from rpg.eventos.comitiva import yara_na_fogueira
from rpg.jogo import Jogo
from rpg.regras import AMBIENTE_VILA
from rpg.web.estado import estado
from tests.test_caspar import com_yara, resolvida
from tests.test_missoes import Roteiro, campanha, ir

CHARCO = "charco_dos_juncos"


def decidida(postura, yara="desconhecida", ui=None, pasta=None, aceita=True):
    """A praça respondida (`postura`: Apoiar, Denunciar ou Calar) com a Yara onde se pede."""
    ui = ui or Roteiro()
    g = com_yara(resolvida("descansada", ui, pasta=pasta, lodo=True), yara)
    g.teste = lambda attr, cd: aceita
    ui.roteiro.insert(0, postura)
    missoes.cena_pendente(g)
    del g.teste
    return g


class TestCharco(unittest.TestCase):
    def test_denunciar_antes_de_conhecer_e_encontrar_depois(self):
        for aceita, desfecho in ((True, "denunciado"), (False, "denuncia_falhou")):
            ui = Roteiro()
            g = decidida("Denunciar", ui=ui, aceita=aceita)
            self.assertEqual(caspar.registro(g)["desfecho"], desfecho)
            self.assertIn("Charco dos Juncos", " ".join(ui.ditos))  # a praça diz onde ela está
            self.assertIn("Vive no Charco dos Juncos", missoes.cartoes(g, todas=True)[1]["linhas"][2])
            self.assertFalse(missoes.cena_pendente(g))  # no Vau, nada
            ir(g, CHARCO)
            ui.roteiro = ["Aceitar"]
            self.assertTrue(missoes.cena_pendente(g))  # na primeira chegada, sem sorteio
            self.assertEqual(ui.cenas[-1], "A Moça do Brejo")
            self.assertNotIn("lenha", " ".join(ui.ditos[-4:]))  # sem a execução
            m = cm.membro(g, "yara")
            self.assertEqual(m["aprovacao"], caspar.SIMPATIA_CHARCO[desfecho])
            self.assertEqual(ui.continuares[-1], ("A Moça do Brejo", True))
            self.assertFalse(missoes.cena_pendente(g))
            self.assertEqual(len([x for x in g.comitiva if x["id"] == "yara"]), 1)

    def test_recusar_no_charco_nao_repete(self):
        ui = Roteiro()
        g = decidida("Denunciar", ui=ui)
        ir(g, CHARCO)
        ui.roteiro = ["Recusar"]
        self.assertTrue(missoes.cena_pendente(g))
        self.assertEqual(g.flag("comitiva:yara"), "recusou")
        self.assertFalse(cm.membro(g, "yara"))
        self.assertFalse(missoes.cena_pendente(g))
        self.assertIn("vive por conta própria", caspar.linha_yara(g))

    def test_comitiva_cheia_oferece_a_troca_de_sempre(self):
        ui = Roteiro()
        g = decidida("Denunciar", ui=ui)
        cm.recrutar(g, "odete")
        cm.recrutar(g, "morel")
        ir(g, CHARCO)
        ui.roteiro = ["Yara espera no acampamento"]
        missoes.cena_pendente(g)
        self.assertTrue(cm.na_reserva(g, "yara"))
        self.assertEqual(len(g.comitiva), 2)

    def test_nao_aparece_para_quem_ja_tem_destino(self):
        """Morta, no grupo, na reserva, que recusou, dispensada ou que foi embora: o Charco não traz ninguém."""
        for onde in ("morta", "grupo", "reserva"):
            g = decidida("Denunciar", yara=onde)
            ir(g, CHARCO)
            self.assertFalse(missoes.cena_pendente(g), onde)
        for flag in ("recusou", "dispensado", "partiu"):
            g = decidida("Denunciar")
            g.marcar("comitiva:yara", flag)
            ir(g, CHARCO)
            self.assertFalse(missoes.cena_pendente(g), flag)
            self.assertFalse(cm.membro(g, "yara") or cm.na_reserva(g, "yara"))

    def test_nao_aparece_com_a_vigilia_de_pe_nem_antes_da_praca(self):
        for postura in ("Apoiar", "Calar"):
            g = decidida(postura)
            ir(g, CHARCO)
            self.assertFalse(missoes.cena_pendente(g), postura)
            self.assertTrue(caspar.fogueira_possivel(g))  # a fogueira do brejo continua possível
        g = resolvida("descansada")
        ir(g, CHARCO)
        self.assertFalse(missoes.cena_pendente(g))

    def test_save_nao_repete_o_encontro(self):
        pasta = tempfile.mkdtemp()
        ui = Roteiro()
        g = decidida("Denunciar", ui=ui, pasta=pasta)
        ir(g, CHARCO)
        ui.roteiro = ["Aceitar"]
        missoes.cena_pendente(g)
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
        self.assertFalse(missoes.cena_pendente(h))
        self.assertEqual([m["id"] for m in h.comitiva], ["yara"])
        self.assertEqual(cm.membro(h, "yara")["aprovacao"], caspar.SIMPATIA_CHARCO["denunciado"])


class TestForaDoVau(unittest.TestCase):
    def apoiada(self, pasta=None):
        g = decidida("Apoiar", yara="grupo", pasta=pasta)
        self.assertTrue(caspar.yara_barrada(g))
        return g

    def test_continua_na_comitiva_mas_nao_esta_aqui(self):
        g = self.apoiada()
        m = cm.membro(g, "yara")
        aprov, vida = m["aprovacao"], m["hp"]
        self.assertTrue(cm.fora(g, m))
        self.assertEqual(cm.junto(g), [])
        self.assertEqual(cm.membros(g), [m])
        painel = cm.estado(g)[0]
        self.assertEqual(painel["fora"]["curto"], "espera fora do Vau")
        self.assertIn("vigília de Caspar", painel["fora"]["texto"])
        self.assertFalse(painel["conversa"])
        self.assertEqual(estado(g)["heroi"]["comitiva"][0]["fora"], painel["fora"])
        for _ in range(3):  # o tempo no Vau não a manda embora nem para a reserva
            g.dia += 1
        self.assertIs(cm.membro(g, "yara"), m)
        self.assertEqual((m["aprovacao"], m["hp"]), (aprov, vida))

    def test_na_estrada_e_fora_do_vau_ela_volta(self):
        g = self.apoiada()
        m = cm.membro(g, "yara")
        g.na_estrada = True
        self.assertIsNone(cm.fora(g, m))
        g.na_estrada = False
        ir(g, "bosque_do_moinho")
        self.assertIsNone(cm.fora(g, m))
        self.assertEqual(cm.junto(g), [m])
        self.assertNotIn("fora", cm.estado(g)[0])
        ir(g, "vau_do_turvo")
        self.assertTrue(cm.fora(g, m))

    def test_nao_luta_no_vau(self):
        g = self.apoiada()

        class Luta:
            inimigos, aliados = [], []
            dizer = staticmethod(lambda *a, **k: None)
        Luta.g = g
        self.assertEqual(cm.preparar_combate(Luta), [])
        ir(g, CHARCO)
        Luta.aliados = []
        self.assertEqual([a.cid for a in cm.preparar_combate(Luta)], ["yara"])

    def test_nao_opina_no_vau(self):
        g = self.apoiada()
        m = cm.membro(g, "yara")
        antes = m["aprovacao"]
        cm.reagir(g, "fanatismo", "crueldade")
        self.assertEqual(m["aprovacao"], antes)
        ir(g, CHARCO)
        cm.reagir(g, "fanatismo", "crueldade")
        self.assertLess(m["aprovacao"], antes)

    def test_templo_e_bolsa_so_para_quem_esta_aqui(self):
        g = self.apoiada()
        m = cm.membro(g, "yara")
        m["hp"] = 1
        g.j.consumiveis["pocao_vida"] = 1
        g.ui.bolsa_clicavel = True
        self.assertFalse([o for o in g.opcoes_templo() if o[2].get("alvo") == "yara"])
        self.assertFalse([o for o in g.opcoes_bolsa() if o[1][0] == "usar_em"])
        bolsa = next(b for b in estado(g)["heroi"]["bolsa"] if b["id"] == "pocao_vida")
        self.assertEqual(bolsa["alvos"], [])
        self.assertFalse(g.usar_em_companheiro("pocao_vida", "yara"))
        self.assertEqual((m["hp"], g.j.consumiveis["pocao_vida"]), (1, 1))
        ir(g, CHARCO)
        self.assertTrue([o for o in g.opcoes_bolsa() if o[1] == ("usar_em", "pocao_vida", "yara")])

    def test_a_praca_ve_a_yara_reagir_antes_de_ela_sair(self):
        g = self.apoiada()
        self.assertLess(cm.membro(g, "yara")["aprovacao"], 0)  # ela estava na praça e viu
        self.assertEqual(caspar.registro(g)["yara_na_praca"], "grupo")

    def test_save_mantem_a_ausencia_so_no_vau(self):
        pasta = tempfile.mkdtemp()
        g = self.apoiada(pasta)
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
        m = cm.membro(h, "yara")
        self.assertTrue(cm.fora(h, m))
        ir(h, CHARCO)
        self.assertEqual(cm.junto(h), [m])

    def test_outras_posturas_nao_barram(self):
        for postura in ("Calar", "Denunciar"):
            g = decidida(postura, yara="grupo")
            self.assertEqual(cm.junto(g), [cm.membro(g, "yara")], postura)

    def test_procedural_sem_ausencia(self):
        g = Jogo(Roteiro(), seed=5, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        m = cm.recrutar(g, "yara")
        self.assertIsNone(cm.fora(g, m))
        self.assertNotIn("fora", cm.estado(g)[0])


class TestConversaDaPraca(unittest.TestCase):
    def conversar(self, g, resposta=None):
        m = cm.membro(g, "yara") or cm.na_reserva(g, "yara")
        g.ui.roteiro = [resposta or "\""]
        antes = (m["aprovacao"], m["conversas"])
        self.assertTrue(cm.conversar(g, m))
        self.assertEqual((m["aprovacao"], m["conversas"]), antes)  # sem aprovação nova e sem adiantar a história
        return m

    def test_quatro_posturas_conforme_o_que_ela_viu(self):
        casos = [("Apoiar", "grupo", ("apoiar", True)), ("Denunciar", "grupo", ("denunciado", True)),
                 ("Denunciar", "reserva", ("denunciado", False)), ("Calar", "grupo", ("calar", True)),
                 ("Calar", "reserva", ("calar", False))]
        for postura, onde, chave in casos:
            g = decidida(postura, yara=onde)
            ir(g, CHARCO)
            self.conversar(g)
            self.assertIn(caspar.FALA_PRACA[chave], g.ui.ditos, (postura, onde))
        g = decidida("Denunciar", yara="grupo", aceita=False)
        ir(g, CHARCO)
        self.conversar(g)
        self.assertIn(caspar.FALA_PRACA[("denuncia_falhou", True)], g.ui.ditos)

    def test_uma_vez_e_nao_no_vau_enquanto_ela_espera_fora(self):
        g = decidida("Apoiar", yara="grupo")
        m = cm.membro(g, "yara")
        self.assertFalse(cm.estado(g)[0]["conversa"])  # ela está lá fora
        self.assertFalse(g.opcoes_conversa() if g.ui.conversa_no_painel else [])
        ir(g, CHARCO)
        self.assertTrue(cm.estado(g)[0]["conversa"])
        self.conversar(g, "\"Foi um erro")
        self.assertIn(caspar.RESPOSTAS_PRACA["apoiar"][1][1], g.ui.ditos)
        g.dia += 1
        self.assertNotEqual(cm.proxima_conversa(g, m), caspar._yara_fala_da_praca)
        self.assertEqual(m["avulsas"], ["praca"])

    def test_quem_ela_conheceu_no_charco_fala_noutro_dia(self):
        ui = Roteiro()
        g = decidida("Denunciar", ui=ui)
        ir(g, CHARCO)
        ui.roteiro = ["Aceitar"]
        missoes.cena_pendente(g)
        m = cm.membro(g, "yara")
        self.assertNotEqual(cm.proxima_conversa(g, m), caspar._yara_fala_da_praca)
        g.dia += 1
        self.assertEqual(cm.proxima_conversa(g, m), caspar._yara_fala_da_praca)
        self.conversar(g)
        self.assertIn(caspar.FALA_PRACA[("denunciado", False)], g.ui.ditos)

    def test_save_nao_repete_a_conversa(self):
        pasta = tempfile.mkdtemp()
        g = decidida("Denunciar", yara="grupo", pasta=pasta)
        ir(g, CHARCO)
        m = self.conversar(g)
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
        h.dia += 1
        n = cm.membro(h, "yara")
        self.assertEqual((n["avulsas"], n["aprovacao"]), (["praca"], m["aprovacao"]))
        self.assertNotEqual(cm.proxima_conversa(h, n), caspar._yara_fala_da_praca)

    def test_sem_decisao_nao_ha_conversa(self):
        g = com_yara(resolvida("descansada"), "grupo")
        g.dia += 1
        self.assertNotEqual(cm.proxima_conversa(g, cm.membro(g, "yara")), caspar._yara_fala_da_praca)


class TestTextos(unittest.TestCase):
    def fogueira(self, g):
        ui = g.ui
        ui.roteiro = ["\"A febre", "Recusar"]
        g.teste = lambda attr, cd: True
        yara_na_fogueira(g)
        return ui

    def test_fogueira_fala_da_fonte_na_campanha_e_do_poco_no_mundo_gerado(self):
        ui = self.fogueira(campanha())
        opcoes = ui.ofertas[0]
        self.assertTrue(any(o.startswith("\"A febre vem da água da Fonte Nova, não dela.\" (Carisma") for o in opcoes))
        self.assertIn("Você fala da Fonte Nova", " ".join(ui.ditos))
        g = Jogo(Roteiro(), seed=5, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        ui = self.fogueira(g)
        self.assertTrue(any(o.startswith("\"A febre vem do poço, não dela.\" (Carisma") for o in ui.ofertas[0]))
        self.assertIn("moleiro que desviou o riacho", " ".join(ui.ditos))

    def test_ambiente_do_vau_sem_padre_nem_peste(self):
        g = campanha()
        for frase in AMBIENTE_VILA:
            trocada = consequencias.ambiente(g, frase)
            self.assertNotIn("padre", trocada)
            self.assertNotIn("peste", trocada)
            self.assertNotIn("o fim chegou", trocada)
        self.assertEqual(consequencias.ambiente(g, AMBIENTE_VILA[1]), AMBIENTE_VILA[1])  # o que cabe, fica
        g = resolvida("descansada", dias=5)
        self.assertEqual(consequencias.ambiente(g, AMBIENTE_VILA[2]), consequencias.frase_da_vila(g))

    def test_ambiente_do_mundo_gerado_igual(self):
        g = Jogo(Roteiro(), seed=5, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["tipo"] == "vila")["id"]
        for frase in AMBIENTE_VILA:
            self.assertEqual(consequencias.ambiente(g, frase), frase)


if __name__ == "__main__":
    unittest.main()
