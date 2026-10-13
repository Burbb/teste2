"""As cenas da Capela Afogada (1.76.0, roadmapIDEIAS/20): qual ambiente a tela gráfica desenha em cada momento (o
exterior, o salão alagado, o ossuário) e o que os pontos fazem. A página do lugar mostra o ambiente do passo da
missão, com o ponto ativo só quando a ação está no menu; dentro de uma cena, o ambiente que o texto descreve, sem ação.
Nada disso muda regra, custo, sorteio ou progressão."""

import unittest

from rpg import missoes
from rpg.regras import Derrota
from tests.test_missoes import MID, Roteiro, fazer, lutas, na_capela


def cenas(g):
    return [d for t, d in g.ui.paineis if t == "cena"]


def ponto(d, pid):
    return next(p for p in d["pontos"] if p["id"] == pid)


def pagina(g):
    missoes.mostrar_cena(g)
    return cenas(g)[-1]


class TestPaginaDaCapela(unittest.TestCase):
    def test_antes_da_hora_o_exterior_sem_acao(self):
        g = na_capela(etapa="canal")
        d = pagina(g)
        self.assertEqual((d["cena"], d["pagina"], ponto(d, "buraco")["acao"]), ("exterior", True, None))
        self.assertTrue(ponto(d, "sapos")["olhar"])  # só aproxima: sem ação nem estado mudando
        self.assertIsNone(ponto(d, "sapos")["acao"])
        self.assertEqual(missoes.registro(g, MID)["etapa"], "canal")  # olhar não avança nada

    def test_na_etapa_da_capela_o_buraco_faz_a_acao_de_entrar(self):
        g = na_capela(etapa="capela")
        d = pagina(g)
        b = ponto(d, "buraco")
        self.assertEqual(b["acao"], {"missao": MID, "acao_missao": "nave"})
        self.assertEqual(b["faz"], "Entrar na capela pelo buraco do canal")
        self.assertTrue(any(o[1][1] == MID and o[1][2] == "nave" for o in missoes.opcoes(g)))  # o mesmo do menu

    def test_vencido_o_salao_a_porta_da_sacristia(self):
        g = na_capela(etapa="sacristia")
        d = pagina(g)
        self.assertEqual((d["cena"], d["agua"]), ("salao", "quieta"))
        self.assertEqual(ponto(d, "porta")["acao"], {"missao": MID, "acao_missao": "sacristia"})
        g = na_capela(etapa="ossuario")  # a sacristia ainda não tem arte: o salão, sem ação na porta
        d = pagina(g)
        self.assertEqual((d["cena"], ponto(d, "porta")["acao"]), ("salao", None))

    def test_depois_do_ossuario_o_sarilho(self):
        g = na_capela(etapa="fundo")
        missoes.registro(g, MID)["pistas"].append("correntes")
        self.assertEqual(pagina(g)["cena"], "ossuario")

    def test_so_na_capela_da_campanha(self):
        g = na_capela(etapa="capela")
        g.mundo["atual"] = next(l for l in g.mundo["locais"] if l.get("chave") == "bosque_do_moinho")["id"]
        missoes.mostrar_cena(g)
        self.assertEqual(cenas(g), [])


class TestCenasDentroDoTexto(unittest.TestCase):
    def test_chegada_mostra_o_exterior_sem_acao(self):
        g = na_capela(etapa="capela")
        missoes.registro(g, MID)["cenas"].remove("capela_exterior")
        g.ui.roteiro = []
        missoes._capela_exterior(g, MID)
        d = cenas(g)[-1]
        self.assertEqual((d["cena"], d["pagina"], ponto(d, "buraco")["acao"]), ("exterior", False, None))

    def test_salao_inquieto_e_depois_quieto(self):
        g = na_capela(etapa="capela")
        lutas(g, "vitoria")
        fazer(g, "nave")
        self.assertEqual([(d["cena"], d.get("agua")) for d in cenas(g)], [("salao", "inquieta"), ("salao", "quieta")])
        self.assertTrue(all(not d["pagina"] for d in cenas(g)))
        self.assertEqual(missoes.registro(g, MID)["etapa"], "sacristia")

    def test_fuga_volta_ao_exterior_e_nao_vence(self):
        g = na_capela(etapa="capela")
        lutas(g, "fuga")
        fazer(g, "nave")
        self.assertEqual([d["cena"] for d in cenas(g)], ["salao", "exterior"])
        self.assertEqual(missoes.registro(g, MID)["etapa"], "capela")
        self.assertEqual(pagina(g)["cena"], "exterior")  # a página continua do lado de fora

    def test_derrota_nao_conta(self):
        g = na_capela(etapa="capela")
        lutas(g, "derrota")
        with self.assertRaises(Derrota):
            fazer(g, "nave")
        self.assertEqual(missoes.registro(g, MID)["etapa"], "capela")
        self.assertEqual(pagina(g)["cena"], "exterior")

    def test_recuo_da_sacristia_termina_fora(self):
        g = na_capela(etapa="sacristia")
        lutas(g, "fuga")
        fazer(g, "sacristia")
        self.assertEqual([d["cena"] for d in cenas(g)], ["exterior"])  # a sacristia em si segue sem arte

    def test_ossuario_vencido_mostra_o_sarilho_sem_acao(self):
        g = na_capela("mago", etapa="ossuario")  # (o guerreiro ganharia o broquel aqui: outra escolha no meio)
        lutas(g, "vitoria")
        fazer(g, "ossuario")
        d = cenas(g)[-1]
        self.assertEqual((d["cena"], d["correntes"], ponto(d, "sarilho")["acao"]), ("ossuario", "presas", None))

    def test_texto_sem_paineis(self):
        """O terminal não desenha cena nenhuma: o Roteiro anota os painéis, mas a interface de texto os ignora."""
        g = na_capela(etapa="capela", ui=Roteiro())
        lutas(g, "vitoria")
        fazer(g, "nave")
        self.assertEqual(missoes.registro(g, MID)["etapa"], "sacristia")


if __name__ == "__main__":
    unittest.main()
