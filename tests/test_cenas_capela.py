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
        g = na_capela(etapa="ossuario")  # vencida a sacristia, a página é a dela (nunca o salão no lugar)
        d = pagina(g)
        self.assertEqual((d["cena"], d["momento"]), ("sacristia", "visita"))

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
        self.assertEqual([(d["cena"], d.get("momento")) for d in cenas(g)],
                         [("sacristia", "entrada"), ("sacristia", "luta"), ("exterior", None)])
        self.assertEqual(missoes.sala_atual(g), "exterior")

    def test_a_luta_do_ossuario_no_ossuario(self):
        """A arte do topo vira o chão da arena: a luta do ossuário acontece no ossuário (1.77.0)."""
        g = na_capela("mago", etapa="ossuario")
        lutas(g, "fuga")
        fazer(g, "ossuario")
        self.assertEqual([d["cena"] for d in cenas(g)], ["ossuario", "sacristia"])  # a fuga sobe à sacristia
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
        d = pagina(g)
        self.assertEqual((d["cena"], d["ilse"], d["agua"]), ("fundo", "ausente", "escura"))  # destruída: sem ela
        missoes.ir_na_capela(g, "ossuario")
        self.assertIn("fundo", passagens(g))  # resolvida: o fundo é só passagem, sem a luta de novo
        self.assertEqual(opcoes_febre(g), [])


class TestLodoNoFundo(unittest.TestCase):
    """A amostra do lodo (Caspar) se recolhe na água do fundo, onde a cena a descreve (1.80.0)."""

    def descida(self, classe="guerreiro", respostas=("Voltar por enquanto",)):
        from rpg import caspar
        g = na_capela(classe, etapa="fundo")
        g.ui.roteiro = list(respostas)
        lutas_vistas = []
        g.combate = lambda *a, **k: lutas_vistas.append(a)
        return g, caspar, lutas_vistas

    def test_no_ossuario_nao_e_na_descida_sim_sem_luta(self):
        g, caspar, lutas_vistas = self.descida(respostas=["Recolher uma amostra do lodo", "Voltar por enquanto"])
        self.assertNotIn("lodo", [o[1][2] for o in missoes.opcoes(g)])
        antes = (g.dia, g.periodo, g.j.consumiveis.get("tocha"))
        fazer(g, "fundo")
        self.assertEqual(caspar.registro(g)["preparos"], ["lodo"])
        self.assertEqual(lutas_vistas, [])  # estar no fundo e recolher não começam a luta
        self.assertEqual((g.dia, g.periodo, g.j.consumiveis.get("tocha")), antes)  # nem tempo, nem tocha
        self.assertEqual(missoes.sala_atual(g), "ossuario")  # voltar por enquanto: sobe ao ossuário
        self.assertEqual(g.ui.cenas[-2:], ["O Fundo da Capela", "O Fundo da Capela"])  # título e sala concordam
        fundos = [d for t, d in g.ui.paineis if t == "cena"][-2:]  # a descida e a coleta: Ilse na água, sem luta
        self.assertEqual([(d["cena"], d["momento"], d["ilse"]) for d in fundos], [("fundo", "descida", "presa"), ("fundo", "visita", "presa")])
        # descer de novo: Ilse e o recuo como antes, sem a amostra (já está no frasco)
        g.ui.roteiro = ["Voltar por enquanto"]
        fazer(g, "fundo")
        self.assertNotIn("Recolher uma amostra do lodo", g.ui.ofertas[-1])
        self.assertEqual(caspar.registro(g)["preparos"], ["lodo"])

    def test_o_mago_analisa_uma_vez(self):
        g, caspar, _ = self.descida("mago", ["Recolher uma amostra do lodo", "Voltar por enquanto"])
        fazer(g, "fundo")
        self.assertEqual(caspar.registro(g)["preparos"], ["lodo", "analise"])
        self.assertEqual(caspar.prova(g), (True, True))

    def test_depois_de_ilse_na_pagina_do_fundo(self):
        from rpg import caspar
        g = na_capela(etapa="fundo")
        missoes.registro(g, MID).update(desfecho="descansada", etapa="retorno")
        caspar.sincronizar(g)
        missoes.ir_na_capela(g, "salao")
        for sala in ("sacristia", "ossuario"):
            missoes.ir_na_capela(g, sala)
        self.assertNotIn("lodo", [o[1][2] for o in missoes.opcoes(g)])
        missoes.ir_na_capela(g, "fundo")
        self.assertEqual([o[1][2] for o in missoes.opcoes(g)], ["lodo"])
        d = pagina(g)
        self.assertEqual((d["cena"], d["ilse"], d["agua"]), ("fundo", "ausente", "clara"))
        self.assertEqual(ponto(d, "lodo")["acao"], {"missao": caspar.MID, "acao_missao": "lodo"})  # o mesmo do menu
        self.assertEqual(ponto(d, "escada")["acao"], {"capela_ir": "ossuario"})
        self.assertTrue(missoes.executar(g, caspar.MID, "lodo"))
        self.assertFalse(missoes.executar(g, caspar.MID, "lodo"))  # uma vez
        self.assertEqual((missoes.sala_atual(g), caspar.registro(g)["preparos"]), ("fundo", ["lodo"]))

    def test_save_antigo_com_o_frasco(self):
        from rpg import caspar
        pasta = tempfile.mkdtemp()
        g = na_capela(etapa="fundo", pasta=pasta)
        caspar.registro(g)["preparos"].append("lodo")
        missoes.registro(g, MID).pop("sala", None)
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(["Voltar por enquanto"]), g.caminho_save(), pasta)
        self.assertEqual((caspar.registro(h)["preparos"], missoes.sala_atual(h)), (["lodo"], "ossuario"))
        missoes.executar(h, MID, "fundo")
        self.assertNotIn("Recolher uma amostra do lodo", h.ui.ofertas[-1])  # quem já tem não recolhe de novo


class TestSairParaAcampar(unittest.TestCase):
    """A fogueira é lá fora: a exaustão e o "Sair e acampar" usam a mesma saída, que só conta o caminho (1.81.0)."""

    def depois_de_acampar(self, sala, exausto):
        g = na_capela(etapa="fundo")
        g.rng.seed(7)
        g.ui.escolher = lambda pergunta, opcoes: 0  # um evento da noite: a primeira opção, igual nos dois
        g.combate = lambda *a, **k: "vitoria"  # e uma luta da noite, vencida (o que importa aqui é a saída)
        if sala != "ossuario":
            for s in {"sacristia": ["sacristia"], "salao": ["sacristia", "salao"],
                      "exterior": ["sacristia", "salao", "exterior"]}[sala]:
                missoes.ir_na_capela(g, s)
        if exausto:
            g.periodo = 4
            g.exausto()
        else:
            missoes.sair_para_acampar(g)
            g.acampar()
        return g

    def conta(self, g):
        return (g.dia, g.periodo, g.j.hp, g.j.rec, g.j.provisoes, dict(g.j.consumiveis), g.rng.getstate())

    def test_a_frase_segue_a_sala_e_o_amanhecer_e_fora(self):
        frases = {}
        for sala in ("salao", "sacristia", "ossuario"):
            g = self.depois_de_acampar(sala, exausto=True)
            self.assertEqual(missoes.sala_atual(g), "exterior")
            frases[sala] = next(d for d in g.ui.ditos if "brecha do muro" in d)
        self.assertEqual(frases["salao"], "Você está exausto. Volta pelo caminho já aberto e sai pela brecha do muro "
                                          "para descansar, perto da capela.")
        self.assertIn("atravessa o salão alagado", frases["sacristia"])
        self.assertIn("sobe pelo alçapão", frases["ossuario"])
        g = self.depois_de_acampar("exterior", exausto=True)  # já fora: a frase de sempre, sem "sai"
        self.assertFalse(any("brecha do muro" in d for d in g.ui.ditos))
        self.assertIn("Você está exausto demais para continuar. É preciso acampar.", g.ui.ditos)

    def test_sair_nao_custa_nada_alem_do_acampamento(self):
        """Mesmo sorteio, mesmo descanso, mesmas provisões e tochas que acampar do lado de fora."""
        for exausto in (True, False):
            dentro, fora = self.depois_de_acampar("ossuario", exausto), self.depois_de_acampar("exterior", exausto)
            self.assertEqual(self.conta(dentro), self.conta(fora))

    def test_o_rotulo_e_a_saida_manual(self):
        g = na_capela(etapa="fundo", ui=Roteiro(["Sair e acampar"] + ["Dormir"] * 5))
        g.menu_selvagem()
        self.assertIn("Sair e acampar", g.ui.ofertas[0])
        self.assertTrue(any(d.startswith("Você volta pelo caminho já aberto: sobe pelo alçapão") for d in g.ui.ditos))
        self.assertEqual(missoes.sala_atual(g), "exterior")
        self.assertEqual(missoes.registro(g, MID)["etapa"], "fundo")  # a missão não anda nem volta
        g = na_capela(etapa="capela", ui=Roteiro(["Acampar e descansar"] + ["Dormir"] * 5))
        g.menu_selvagem()  # do lado de fora, o nome de sempre
        self.assertIn("Acampar e descansar até o amanhecer", g.ui.ofertas[0])

    def test_voltar_depois_pelas_salas_abertas(self):
        g = self.depois_de_acampar("ossuario", exausto=True)
        lutas(g)  # nenhuma luta pode acontecer na volta
        for sala in ("salao", "sacristia", "ossuario"):
            self.assertTrue(missoes.ir_na_capela(g, sala))
        self.assertEqual([o[1][2] for o in opcoes_febre(g)], ["correntes", "fundo"])


class TestExplorarSoLaFora(unittest.TestCase):
    """Explorar a região só do lado de fora da capela (1.81.1): sem a opção dentro, sem "sair e explorar", e um pedido
    atrasado (tela desatualizada, atalho) não explora nem gasta nada."""

    INTERNAS = ("salao", "sacristia", "ossuario", "fundo")

    def em(self, sala, pasta=None):
        g = na_capela(etapa="retorno", pasta=pasta)  # a guardiã resolvida: todas as salas abertas
        missoes.registro(g, MID)["desfecho"] = "descansada"
        caminho = {"exterior": [], "salao": ["salao"], "sacristia": ["salao", "sacristia"],
                   "ossuario": ["salao", "sacristia", "ossuario"], "fundo": ["salao", "sacristia", "ossuario", "fundo"]}
        missoes.saiu_da_capela(g)
        for s in caminho[sala]:
            self.assertTrue(missoes.ir_na_capela(g, s))
        return g

    def menu(self, g):
        def escolher(pergunta, opcoes):
            g.ui.ofertas.append(list(opcoes))
            raise StopIteration
        g.ui.escolher = escolher
        with self.assertRaises(StopIteration):
            g.menu_selvagem()
        return g.ui.ofertas[-1]

    def test_dentro_nao_ha_explorar(self):
        for sala in self.INTERNAS:
            ops = self.menu(self.em(sala))
            self.assertFalse(any(o.startswith("Explorar") for o in ops), sala)
            self.assertFalse(any("explorar" in o.lower() for o in ops), sala)  # nem "Sair e explorar"
            self.assertIn("Sair e acampar", ops)  # a saída para acampar continua
        self.assertTrue(any(o.startswith("Explorar a região") for o in self.menu(self.em("exterior"))))

    def test_pedido_atrasado_dentro_nao_faz_nada(self):
        for sala in self.INTERNAS:
            g = self.em(sala)
            g.combate = lambda *a, **k: self.fail("explorar começou uma luta")
            antes = (foto(g), g.rng.getstate(), len(g.ui.cenas))
            self.assertFalse(g.explorar())
            self.assertEqual((foto(g), g.rng.getstate(), len(g.ui.cenas)), antes, sala)
            self.assertEqual(missoes.sala_atual(g), sala)  # e não leva para fora

    def test_do_lado_de_fora_explora_como_sempre(self):
        g = self.em("exterior")
        g.ui.escolher = lambda pergunta, opcoes: 0
        g.combate = lambda *a, **k: "vitoria"
        periodo = g.periodo
        g.explorar()
        self.assertIn("Explorando", g.ui.cenas)
        self.assertEqual(g.periodo, periodo + 1)

    def test_o_tutorial_espera_o_lado_de_fora(self):
        from rpg import abertura
        for sala in self.INTERNAS:
            g = self.em(sala)
            abertura.comecar(g, True)
            self.assertIsNone(abertura._v5(g, abertura.estado(g)), sala)
        g = self.em("exterior")
        abertura.comecar(g, True)
        self.assertEqual(abertura._v5(g, abertura.estado(g))["ancora"], "opcao:Explorar a região")

    def test_salvar_e_carregar_dentro_e_fora(self):
        for sala in self.INTERNAS + ("exterior",):
            pasta = tempfile.mkdtemp()
            g = self.em(sala, pasta)
            g.salvar(silencioso=True)
            h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
            self.assertEqual(missoes.sala_atual(h), sala)
            tem = any(o.startswith("Explorar") for o in self.menu(h))
            self.assertEqual(tem, sala == "exterior", sala)


if __name__ == "__main__":
    unittest.main()


class TestSacristia(unittest.TestCase):
    """A sacristia desenhada (1.83.0): o motor diz o momento (entrada, luta, vitória, visita), a luz, o baú e o livro; a
    tela só desenha. Nada de baú, livro ou pista a mais."""

    def test_entrada_luta_vitoria_e_a_pagina_depois(self):
        g = na_capela(etapa="sacristia")
        g.j.consumiveis["tocha"] = 2
        lutas(g, "vitoria")
        fazer(g, "sacristia")
        ds = [d for d in cenas(g) if d["cena"] == "sacristia"]
        self.assertEqual([(d["momento"], d["luz"], d["bau"], d["livro"]) for d in ds],
                         [("entrada", "lanterna", "coberto", "no_buraco"), ("luta", "lanterna", "coberto", "no_buraco"),
                          ("vitoria", "tocha", "coberto", "fora")])
        self.assertTrue(all(d["pontos"] == [] and not d["pagina"] for d in ds))  # dentro das cenas, nada se clica
        self.assertEqual(g.j.consumiveis["bau"], 1)  # o baú, uma vez, pelo motor
        d = pagina(g)
        self.assertEqual((d["momento"], d["bau"], d["livro"], d["luz"]), ("visita", "levado", "fora", None))
        self.assertEqual([p["id"] for p in d["pontos"]], ["porta", "janela", "livro", "alcapao"])
        self.assertEqual(ponto(d, "porta")["acao"], {"capela_ir": "salao"})
        self.assertEqual(ponto(d, "alcapao")["acao"], {"missao": MID, "acao_missao": "ossuario"})
        self.assertEqual(ponto(d, "alcapao")["faz"], "Descer ao ossuário")

    def test_sem_tocha_a_vitoria_fica_com_a_janela(self):
        g = na_capela(etapa="sacristia")
        g.j.consumiveis["tocha"] = 0
        lutas(g, "vitoria")
        fazer(g, "sacristia")
        self.assertIsNone(next(d for d in cenas(g) if d.get("momento") == "vitoria")["luz"])

    def test_olhar_nao_da_nada_nem_repete_o_livro(self):
        g = na_capela(etapa="ossuario")
        d = pagina(g)
        antes = json.dumps([g.j.para_dict(), g.mundo, g.dia, g.periodo], sort_keys=True, default=str)
        for pid in ("janela", "livro"):
            p = ponto(d, pid)
            self.assertIsNone(p["acao"])
            self.assertTrue(p["olhar"])
            self.assertNotIn("Sigilo", p["olhar"])  # o que o livro conta não se repete
        self.assertEqual(antes, json.dumps([g.j.para_dict(), g.mundo, g.dia, g.periodo], sort_keys=True, default=str))

    def test_depois_do_ossuario_o_alcapao_so_passa(self):
        g = na_capela(etapa="fundo")
        missoes.ir_na_capela(g, "salao")
        missoes.ir_na_capela(g, "sacristia")
        d = pagina(g)
        self.assertEqual(ponto(d, "alcapao")["acao"], {"capela_ir": "ossuario"})
        self.assertEqual(ponto(d, "porta")["acao"], {"capela_ir": "salao"})

    def test_a_fuga_do_ossuario_sobe_com_a_tocha(self):
        g = na_capela("mago", etapa="ossuario")
        g.j.consumiveis["tocha"] = 2
        lutas(g, "fuga")
        fazer(g, "ossuario")
        d = cenas(g)[-1]
        self.assertEqual((d["cena"], d["momento"], d["luz"]), ("sacristia", "visita", "tocha"))

    def test_a_luz_da_luta_nao_vai_no_save(self):
        g = na_capela(etapa="sacristia")
        lutas(g, "vitoria")
        fazer(g, "sacristia")
        self.assertNotIn("luz_na_sala", json.dumps(g.mundo))


class TestFundo(unittest.TestCase):
    """O fundo alagado desenhado (1.84.0): o motor diz o momento (descida, visita, luta, descanso, destruída), Ilse
    (presa, solta, ausente), as correntes, a água e a luz; os momentos dela vão para a tela só depois do texto que os
    conta, e só na tela gráfica. Nada de item, sorteio ou regra a mais."""

    def no_fundo(self, classe, respostas, grafica=True, **kw):
        from tests.test_guardia import no_fundo
        g = no_fundo(classe, respostas, **kw)
        ui = g.ui
        ui.paineis, ui.momentos = [], []
        ui.painel = lambda t, d: ui.paineis.append((t, d)) or False
        ui.conquistas_na_tela = grafica
        ui.celebrar = lambda tipo, dados: ui.momentos.append(dados["momento"]) if tipo == "ilse" else None
        ui.dizer = ui.narrar = lambda texto="", cor=None: (ui.ditos.append(str(texto)), ui.momentos.append(str(texto)))
        return g

    def fundos(self, g):
        return [(d["momento"], d["ilse"], d["correntes"], d["agua"]) for d in cenas(g) if d["cena"] == "fundo"]

    def depois_do_texto(self, g, momento, trecho):
        """O momento vem logo depois do texto que o conta (nunca antes)."""
        i = g.ui.momentos.index(momento)
        self.assertIn(trecho, g.ui.momentos[i - 1])

    def test_destruir_presa(self):
        from tests.test_guardia import DESTRUIR
        g = self.no_fundo("guerreiro", DESTRUIR, preparos=())
        missoes.executar(g, MID, "fundo")
        self.assertEqual(missoes.registro(g, MID)["desfecho"], "destruida")
        self.assertEqual(self.fundos(g), [("descida", "presa", "presas", "escura"), ("luta", "ausente", "presas", "escura"),
                                          ("destruida", "destruida", "presas", "escura")])
        self.assertEqual([m for m in g.ui.momentos if m in ("acorda", "canto_falha", "fita", "afunda", "desfaz")],
                         ["acorda", "desfaz"])
        self.depois_do_texto(g, "acorda", "Ela abre os olhos")
        self.depois_do_texto(g, "desfaz", "Ilse se desfaz")
        self.assertTrue(all(d["pontos"] == [] for d in cenas(g) if d["cena"] == "fundo"))  # dentro das cenas, nada se clica
        d = pagina(g)
        self.assertEqual((d["momento"], d["ilse"], d["agua"], [p["id"] for p in d["pontos"]]),
                         ("visita", "ausente", "escura", ["escada", "lodo"]))

    def test_descanso_solta_com_a_fita(self):
        from tests.test_guardia import DESCANSO, PRONTO
        g = self.no_fundo("mago", DESCANSO, **PRONTO)
        missoes.executar(g, MID, "fundo")
        self.assertEqual(missoes.registro(g, MID)["desfecho"], "descansada")
        self.assertEqual(self.fundos(g), [("descida", "solta", "soltas", "escura"), ("luta", "ausente", "soltas", "escura"),
                                          ("descanso", "descanso", "soltas", "escura")])
        self.assertEqual([m for m in g.ui.momentos if m in ("acorda", "canto_falha", "fita", "afunda", "desfaz")],
                         ["acorda", "canto_falha", "fita", "afunda"])
        self.depois_do_texto(g, "canto_falha", "O canto de Ilse falha")
        self.depois_do_texto(g, "fita", "pega a fita")
        self.depois_do_texto(g, "afunda", "afunda devagar")
        d = pagina(g)
        self.assertEqual((d["ilse"], d["agua"], d["correntes"]), ("ausente", "clara", "soltas"))

    def test_desistir_do_rito_falha_e_desfaz(self):
        from tests.test_guardia import PRONTO
        g = self.no_fundo("arqueiro", ["Chamar Ilse pelo nome", "Desistir do rito", "Guardar"], **PRONTO)
        missoes.executar(g, MID, "fundo")
        self.assertEqual([m for m in g.ui.momentos if m in ("acorda", "canto_falha", "fita", "afunda", "desfaz")],
                         ["acorda", "canto_falha", "desfaz"])

    def test_no_texto_sem_momentos_e_o_mesmo_jogo(self):
        from tests.test_guardia import DESCANSO, PRONTO
        a = self.no_fundo("mago", DESCANSO, **PRONTO)
        b = self.no_fundo("mago", DESCANSO, grafica=False, **PRONTO)
        for g in (a, b):
            missoes.executar(g, MID, "fundo")
        self.assertNotIn("acorda", b.ui.momentos)  # a tela de texto não recebe os momentos
        ilse = [t for t in a.ui.ditos if "Ilse" in t or "fita" in t]
        self.assertEqual(ilse, [t for t in b.ui.ditos if "Ilse" in t or "fita" in t])  # a mesma cena contada
        self.assertEqual(json.dumps([a.j.para_dict(), a.mundo, a.dia, a.periodo], sort_keys=True, default=str),
                         json.dumps([b.j.para_dict(), b.mundo, b.dia, b.periodo], sort_keys=True, default=str))

    def test_sem_tocha_a_luta_sem_luz(self):
        from tests.test_guardia import DESTRUIR
        g = self.no_fundo("guerreiro", DESTRUIR, preparos=())
        g.j.consumiveis["tocha"] = 0
        missoes.executar(g, MID, "fundo")
        luzes = [(d["momento"], d["luz"]) for d in cenas(g) if d["cena"] == "fundo"]
        self.assertEqual(luzes[:2], [("descida", None), ("luta", None)])

    def test_voltar_por_enquanto_nao_muda_ilse(self):
        g = na_capela(etapa="fundo")
        g.ui.roteiro = ["Voltar por enquanto"]
        lutas(g)
        fazer(g, "fundo")
        self.assertEqual([(d["momento"], d["ilse"]) for d in cenas(g) if d["cena"] == "fundo"], [("descida", "presa")])
        self.assertEqual(missoes.sala_atual(g), "ossuario")
        self.assertIsNone(missoes.registro(g, MID).get("desfecho"))
