"""As cenas da Capela Afogada (1.76.0 e 1.79.0, roadmapIDEIAS/20): qual ambiente a tela gráfica desenha em cada
momento e o que os pontos fazem. A página do lugar mostra a sala em que o personagem está (separada do passo da
missão), com os pontos ativos só quando a ação ou a passagem está no menu; dentro de uma cena, o ambiente que o texto
descreve, sem ação. Andar entre salas vencidas só troca a vista. Nada disso muda regra, custo, sorteio ou progressão."""

import json
import tempfile
import unittest

from rpg import missoes
from rpg.jogo import Jogo
from rpg.regras import Derrota
from tests.test_missoes import MID, Roteiro, fazer, ir, lutas, na_capela, opcoes_febre


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
        self.assertEqual(ponto(d, "brecha")["acao"], {"capela_ir": "exterior"})
        g = na_capela(etapa="ossuario")  # a sacristia não tem arte: um fundo neutro, sem pontos, nunca o salão
        d = pagina(g)
        self.assertEqual((d["cena"], d["sala"], d["pontos"]), ("neutra", "sacristia", []))

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
        self.assertEqual([d["cena"] for d in cenas(g)], ["neutra", "exterior"])  # a sacristia, num fundo neutro
        self.assertEqual(missoes.sala_atual(g), "exterior")

    def test_a_luta_do_ossuario_no_ossuario(self):
        """A arte do topo vira o chão da arena: a luta do ossuário acontece no ossuário (1.77.0)."""
        g = na_capela("mago", etapa="ossuario")
        lutas(g, "fuga")
        fazer(g, "ossuario")
        self.assertEqual([d["cena"] for d in cenas(g)], ["ossuario", "neutra"])  # a fuga sobe à sacristia
        self.assertEqual((missoes.registro(g, MID)["etapa"], missoes.sala_atual(g)), ("ossuario", "sacristia"))

    def test_ossuario_vencido_mostra_o_sarilho_sem_acao(self):
        g = na_capela("mago", etapa="ossuario")  # (o guerreiro ganharia o broquel aqui: outra escolha no meio)
        lutas(g, "vitoria")
        fazer(g, "ossuario")
        d = cenas(g)[-1]
        self.assertEqual((d["cena"], d["correntes"], ponto(d, "sarilho")["acao"]), ("ossuario", "presas", None))
        self.assertTrue(all(p["acao"] is None for p in d["pontos"]))

    def test_texto_sem_paineis(self):
        """O terminal não desenha cena nenhuma: o Roteiro anota os painéis, mas a interface de texto os ignora."""
        g = na_capela(etapa="capela", ui=Roteiro())
        lutas(g, "vitoria")
        fazer(g, "nave")
        self.assertEqual(missoes.registro(g, MID)["etapa"], "sacristia")


def passagens(g):
    return [o[1][1] for o in missoes.passagens(g)]


def foto(g):
    """O que andar pela capela não pode mexer: missão (sem a sala), tempo, recursos, vida e bolsa."""
    m = {k: v for k, v in missoes.registro(g, MID).items() if k != "sala"}
    return json.dumps([m, g.dia, g.periodo, g.j.hp, g.j.rec, g.j.ouro, g.j.consumiveis, g.j.flechas, g.j.provisoes,
                       g.j.xp], sort_keys=True, default=str)


class TestNavegacao(unittest.TestCase):
    def test_a_sequencia_fisica_so_pelas_salas_vencidas(self):
        g = na_capela(etapa="capela")
        self.assertEqual((missoes.sala_atual(g), passagens(g)), ("exterior", []))  # o salão ainda por vencer
        g = na_capela(etapa="fundo")
        self.assertEqual(missoes.sala_atual(g), "ossuario")
        self.assertEqual(passagens(g), ["sacristia"])  # o fundo, só pela ação da missão (a guardiã)
        self.assertFalse(missoes.ir_na_capela(g, "salao"))  # nada de atalho: só a sala vizinha
        for sala, vizinhas in (("sacristia", ["salao", "ossuario"]), ("salao", ["exterior", "sacristia"]),
                               ("exterior", ["salao"])):
            self.assertTrue(missoes.ir_na_capela(g, sala))
            self.assertEqual((missoes.sala_atual(g), passagens(g)), (sala, vizinhas))

    def test_andar_nao_gasta_nem_repete_nada(self):
        g = na_capela(etapa="fundo")
        missoes.registro(g, MID)["pistas"].append("correntes")
        lutas(g)  # nenhuma luta pode acontecer: a fila vazia quebraria
        antes = foto(g)
        for sala in ("sacristia", "salao", "exterior", "salao", "sacristia", "ossuario", "sacristia", "ossuario"):
            self.assertTrue(missoes.ir_na_capela(g, sala))
            missoes.mostrar_cena(g)
        self.assertEqual(foto(g), antes)
        self.assertEqual([o[1][2] for o in opcoes_febre(g)], ["correntes", "fundo"])  # de volta, o mesmo menu

    def test_cada_acao_so_na_sua_sala(self):
        g = na_capela(etapa="fundo")
        missoes.ir_na_capela(g, "sacristia")
        self.assertEqual(missoes.opcoes(g), [])  # o sarilho e o fundo ficam no ossuário
        self.assertFalse(fazer(g, "correntes", "Deixar"))
        g = na_capela(etapa="ossuario")
        missoes.ir_na_capela(g, "salao")
        self.assertEqual(missoes.opcoes(g), [])  # descer ao ossuário é da sacristia
        missoes.ir_na_capela(g, "sacristia")
        self.assertEqual([o[1][2] for o in missoes.opcoes(g)], ["ossuario"])  # a sala pendente pede o encontro

    def test_pontos_de_passagem_na_pagina(self):
        g = na_capela(etapa="fundo")
        missoes.registro(g, MID)["pistas"].append("correntes")
        d = pagina(g)
        self.assertEqual(ponto(d, "escada")["acao"], {"capela_ir": "sacristia"})
        self.assertEqual(ponto(d, "descida")["acao"], {"missao": MID, "acao_missao": "fundo"})
        metas = [o[2] for o in missoes.passagens(g)]
        self.assertIn({"capela_ir": "sacristia"}, metas)  # o mesmo endereço da opção do menu
        missoes.ir_na_capela(g, "sacristia")
        missoes.ir_na_capela(g, "salao")
        d = pagina(g)
        self.assertEqual(ponto(d, "porta")["acao"], {"capela_ir": "sacristia"})  # vencida: só passa
        missoes.ir_na_capela(g, "exterior")
        d = pagina(g)
        self.assertEqual(ponto(d, "buraco")["acao"], {"capela_ir": "salao"})
        self.assertEqual(ponto(d, "buraco")["faz"], "Entrar no salão pelo buraco do muro")

    def test_pelo_menu_do_lugar(self):
        """A passagem é uma opção do menu do lugar: escolher só troca a sala (sem Continuar, tempo nem gasto)."""
        g = na_capela(etapa="fundo", ui=Roteiro(["Subir à sacristia"]))
        antes = foto(g)
        g.menu_selvagem()
        self.assertEqual((missoes.sala_atual(g), foto(g), g.ui.continuares), ("sacristia", antes, []))
        g.ui.roteiro = ["Descer ao ossuário pelo alçapão"]
        g.menu_selvagem()
        self.assertEqual(missoes.sala_atual(g), "ossuario")

    def test_voltar_nao_desfaz_as_correntes(self):
        g = na_capela(etapa="fundo")
        missoes.registro(g, MID)["preparos"].append("corpo_solto")
        missoes.ir_na_capela(g, "sacristia")
        missoes.ir_na_capela(g, "ossuario")
        self.assertEqual(pagina(g)["correntes"], "soltas")
        self.assertEqual([o[1][2] for o in opcoes_febre(g)], ["fundo"])

    def test_chegar_viajando_e_o_resgate_deixam_do_lado_de_fora(self):
        g = na_capela(etapa="fundo")
        g.chegar(g.loc)
        self.assertEqual(missoes.sala_atual(g), "exterior")
        g = na_capela(etapa="fundo")
        g.resgate()
        ir(g, "capela_afogada")
        self.assertEqual(missoes.sala_atual(g), "exterior")
        self.assertEqual(missoes.registro(g, MID)["etapa"], "fundo")  # a missão não volta

    def test_explorar_e_acampar_sao_la_fora(self):
        g = na_capela(etapa="fundo")
        missoes.saiu_da_capela(g)
        self.assertEqual(missoes.sala_atual(g), "exterior")

    def test_save_guarda_a_sala_e_save_antigo_deduz(self):
        pasta = tempfile.mkdtemp()
        g = na_capela(etapa="fundo", pasta=pasta)
        missoes.ir_na_capela(g, "sacristia")
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
        self.assertEqual(missoes.sala_atual(h), "sacristia")  # carregar não simula viagem
        for etapa, sala in (("capela", "exterior"), ("sacristia", "salao"), ("ossuario", "sacristia"),
                            ("fundo", "ossuario"), ("retorno", "exterior")):
            g = na_capela(etapa=etapa)
            missoes.registro(g, MID).pop("sala", None)  # um save de antes da 1.79.0
            self.assertEqual(missoes.sala_atual(g), sala, etapa)

    def test_a_guardia_vencida_deixa_no_fundo_e_o_fundo_fica_aberto(self):
        g = na_capela("mago", etapa="fundo")
        m = missoes.registro(g, MID)
        missoes._por_na_sala(g, "fundo")  # o que a vitória sobre a guardiã faz, antes do desfecho
        m.update(desfecho="destruida", etapa="retorno")
        self.assertEqual((missoes.sala_atual(g), passagens(g)), ("fundo", ["ossuario"]))
        self.assertEqual(pagina(g)["cena"], "neutra")
        missoes.ir_na_capela(g, "ossuario")
        self.assertIn("fundo", passagens(g))  # resolvida: o fundo é só passagem, sem a luta de novo
        self.assertEqual(opcoes_febre(g), [])


if __name__ == "__main__":
    unittest.main()
