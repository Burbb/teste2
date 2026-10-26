"""A Prisão de Gelo (E6): uma transformação da Lança de Gelo, liberada por talento e resolvida por herói.

O catálogo nunca muda: cada herói resolve a sua ficha (`habilidades.efetiva`). Nome, custo, descrição, prévia, Grimório
e execução saem da mesma ficha. A versão se troca na vila e no acampamento; na luta, vale a escolhida. Congela sem
sorteio e não se esquiva, mas as regras de sempre continuam: firme, chefes e gigantes resistem metade, o golpe
preparado se perde."""

import random
import tempfile
import unittest

from rpg import dev, grimorio, talentos
from rpg.combate import Combate
from rpg.habilidades import HABILIDADES, VARIANTES, efetiva, escolher_versao, transformacoes, versao
from rpg.inimigos import criar, instanciar_guardiao
from rpg.jogo import Jogo
from rpg.web.estado import glossario, heroi as estado_heroi
from rpg.web.ponte import WebUI
from tests.test_missoes import Roteiro

PRISAO = talentos.POR_ID["prisao_gelo"]


class Anotador(Roteiro):
    def __init__(self, roteiro=()):
        super().__init__(roteiro)
        self.lances, self.metas = [], []

    def lance(self, tipo, **dados):
        self.lances.append(dict(dados, tipo=tipo))

    def escolher(self, pergunta, opcoes):
        self.metas.append(self.meta_opcoes)
        return super().escolher(pergunta, opcoes)


def mago(nivel=4, talento=True, pasta=None, roteiro=()):
    g = Jogo(Anotador(roteiro), seed=5, pasta_saves=pasta or tempfile.mkdtemp())
    g.iniciar("Teste", "mago", "turvo")
    dev.subir_ate(g, nivel, spec="piromante")
    if "lanca_gelo" not in g.j.kit:
        g.j.kit = ["lanca_gelo"] + g.j.kit[:3]  # a Lança (ou a Prisão) vai para a luta (o kit, etapa 4)
    if talento:
        talentos.aprender(g.j, PRISAO)
    g.j.hp, g.j.rec = g.j.max_hp, g.j.max_rec
    g.clima, g.periodo = "limpo", 1  # sem os efeitos do momento (clima, noite) que o Grimório não conta
    return g


def luta(g, familia="lobo", nivel=3, guardiao=False, semente=3):
    r = random.Random(semente)
    e = (instanciar_guardiao({"bioma": "floresta", "idx": 0, "nome": "Guardião"}, nivel) if guardiao
         else criar(r, familia, nivel))
    e.max_hp = e.hp = 10 ** 4  # de pé até o fim do teste
    cb = Combate(g, [e], pode_fugir=False, sozinho=True)
    cb.turno = 1
    return cb, e


def lancar(g, cb):
    """A Prisão pelo menu do combate (o botão é o da Lança: o id guardado continua `lanca_gelo`)."""
    g.ui.roteiro, g.ui.lances = ["Habilidades", "Prisão de Gelo"], []
    cb.fase_jogador()
    return g.ui.lances


class TestFicha(unittest.TestCase):
    def test_o_catalogo_nao_muda(self):
        antes = {k: (id(v), v["nome"], v["custo"], v["desc"]) for k, v in HABILIDADES.items()}
        g = mago()
        cb, _ = luta(g)
        lancar(g, cb)
        grimorio.dados(g.j)
        cb.metas_habilidades()
        self.assertEqual({k: (id(v), v["nome"], v["custo"], v["desc"]) for k, v in HABILIDADES.items()}, antes)
        self.assertNotIn("prisao_gelo", HABILIDADES)
        self.assertEqual(g.j.habilidades.count("lanca_gelo"), 1)  # o herói continua com o mesmo id

    def test_dois_herois_na_mesma_sessao(self):
        com, sem = mago(), mago(talento=False)
        self.assertEqual((efetiva(com.j, "lanca_gelo")["nome"], efetiva(sem.j, "lanca_gelo")["nome"]),
                         ("Prisão de Gelo", "Lança de Gelo"))
        self.assertEqual((talentos.custo_habilidade(com.j, "lanca_gelo"), talentos.custo_habilidade(sem.j, "lanca_gelo")),
                         (16, 10))
        nomes = lambda g: {p["id"]: p["nome"] for p in grimorio.dados(g.j)["habilidades"]}
        self.assertEqual((nomes(com)["lanca_gelo"], nomes(sem)["lanca_gelo"]), ("Prisão de Gelo", "Lança de Gelo"))
        escolher_versao(com.j, "lanca_gelo", None)
        self.assertEqual(versao(com.j, "lanca_gelo"), "lanca_gelo")
        escolher_versao(com.j, "lanca_gelo", "prisao_gelo")
        self.assertFalse(getattr(sem.j, "versoes", None))  # a escolha de um não vaza para o outro

    def test_escolha_sem_talento_nao_vale(self):
        g = mago(talento=False)
        g.j.versoes = {"lanca_gelo": "prisao_gelo"}  # um save mexido, ou o talento que não está mais lá
        self.assertEqual((versao(g.j, "lanca_gelo"), talentos.custo_habilidade(g.j, "lanca_gelo")), ("lanca_gelo", 10))
        self.assertEqual(transformacoes(g.j), {})

    def test_custo_com_eficiencia(self):
        g = mago(nivel=6)
        g.j.talentos["eficiencia"] = 2
        self.assertEqual(talentos.custo_habilidade(g.j, "lanca_gelo"), 13)
        self.assertEqual(talentos.custo_de(g.j, "lanca_gelo"), 8)  # a outra versão, para a comparação
        self.assertEqual(talentos.custo_habilidade(g.j, "lanca_gelo"), talentos.custo_de(g.j, versao(g.j, "lanca_gelo")))

    def test_previa_menu_e_tela_da_mesma_ficha(self):
        g = mago()
        cb, _ = luta(g)
        meta = next(m for m in cb.metas_habilidades() if m["habilidade"] == "lanca_gelo")
        self.assertEqual((meta["nome"], meta["custo"], meta["icone"]), ("Prisão de Gelo", 16, "gelo"))
        self.assertEqual(meta["desc"], VARIANTES["prisao_gelo"]["desc"])
        pagina = next(p for p in grimorio.dados(g.j)["habilidades"] if p["id"] == "lanca_gelo")
        self.assertEqual((pagina["nome"], pagina["custo"]), ("Prisão de Gelo", 16))
        self.assertIn("× 70%", pagina["linhas"][0]["formula"])
        self.assertTrue(pagina["linhas"][0]["sem_esquiva"])  # no resumo, uma vez (1.211.1: não mais na nota)
        self.assertIn("Prisão de Gelo", [h["nome"] for h in estado_heroi(g)["habilidades"]])
        self.assertEqual(glossario()["Prisão de Gelo"], "gelo")
        g.ui.roteiro = ["Voltar"]
        cb.menu_habilidades()
        self.assertTrue(any(o.startswith("Prisão de Gelo [16 Mana] — ") for o in g.ui.ofertas[-1]))


class TestNaLuta(unittest.TestCase):
    def test_congela_sempre_e_nao_se_esquiva(self):
        for semente in range(25):
            g = mago()
            cb, e = luta(g, semente=semente)
            e.agi = 999  # esquivaria quase tudo
            rec = g.j.rec
            lances = lancar(g, cb)
            self.assertTrue(any(l["tipo"] == "golpe" and l["rotulo"] == "Prisão de Gelo" for l in lances), semente)
            self.assertTrue(e.efeito("atordoado"), semente)
            self.assertEqual(rec - g.j.rec, 16)
            acao = next(l for l in lances if l["tipo"] == "acao")
            self.assertEqual((acao["nome"], acao["hab"]), ("Prisão de Gelo", "prisao_gelo"))
            self.assertEqual(cb.tel["habilidades"], {"prisao_gelo": 1})  # a telemetria separa as versões
            g.combate_ativo = None

    def test_dano_dentro_do_grimorio(self):
        g = mago()
        linha = next(p for p in grimorio.dados(g.j)["habilidades"] if p["id"] == "lanca_gelo")["linhas"][0]
        vistos = 0
        for semente in range(30):
            cb, e = luta(g, semente=semente)
            e.defesa, e.resist = 0, {}
            for l in lancar(g, cb):
                if l["tipo"] == "golpe" and not l["crit"]:  # a faixa do Grimório trunca; o golpe arredonda (±1)
                    self.assertLessEqual(linha["min"] - 1, l["dano"])
                    self.assertLessEqual(l["dano"], linha["max"] + 1)
                    vistos += 1
            g.j.rec = g.j.max_rec
            g.combate_ativo = None
        self.assertGreater(vistos, 15)

    def test_firme_recusa(self):
        g = mago()
        cb, e = luta(g)
        e.aplicar("firme", 1)
        lances = lancar(g, cb)
        self.assertFalse(e.efeito("atordoado"))
        self.assertTrue(any(l["tipo"] == "efeito_negado" for l in lances))
        self.assertTrue(any(l["tipo"] == "golpe" and l["dano"] > 0 for l in lances))  # o golpe fraco sai
        g.combate_ativo = None

    def test_duas_lancas_nos_dois_turnos_da_iniciativa(self):
        """A iniciativa dá dois turnos seguidos: congelar de novo antes de o inimigo agir não soma (e a tela diz isso),
        ele perde uma ação só, fica firme depois dela, e a terceira Lança não o congela."""
        for prisao in (False, True):
            g = mago(talento=prisao)
            cb, e = luta(g)
            e.agi = 0  # a Lança acerta; o sorteio de congelar (35%) é forçado abaixo
            aplicar = cb.aplicar
            cb.aplicar = lambda alvo, ef, t, *a, **k: aplicar(alvo, ef, t, *a, **dict(k, chance=1.0))
            nome = "Prisão de Gelo" if prisao else "Lança de Gelo"
            g.j.aplicar("iniciativa", 2, 0.25)

            def lanca():
                g.ui.roteiro, g.ui.lances, g.j.rec = ["Habilidades", nome], [], g.j.max_rec
                cb.fase_jogador()
                return [(l["tipo"], l.get("rotulo")) for l in g.ui.lances if l["tipo"].startswith("efeito")]

            self.assertEqual(lanca(), [("efeito", "congelado")])  # turno da surpresa: os inimigos não agem
            g.j.remover("iniciativa")
            self.assertEqual(lanca(), [("efeito", "já congelado")])
            self.assertEqual(e.efeitos["atordoado"]["t"], 1)  # não soma
            g.ui.lances = []
            cb.fase_inimigos()
            self.assertEqual([l["tipo"] for l in g.ui.lances], ["atordoado"])  # perde uma ação
            self.assertEqual(list(e.efeitos), ["firme"])
            self.assertEqual(lanca(), [("efeito_negado", "firme")])
            g.ui.lances = []
            cb.fase_inimigos()
            self.assertIn("acao", [l["tipo"] for l in g.ui.lances])  # e age na rodada seguinte
            g.combate_ativo = None

    def test_chefes_e_gigantes_resistem_metade(self):
        for familia, guardiao in (("troll", False), (None, True)):
            congelou = 0
            for semente in range(120):
                g = mago()
                cb, e = luta(g, familia or "lobo", nivel=5, guardiao=guardiao, semente=semente)
                cb.rng.seed(semente)
                lancar(g, cb)
                congelou += bool(e.efeito("atordoado"))
                g.combate_ativo = None
            self.assertTrue(35 <= congelou <= 85, (familia, guardiao, congelou))

    def test_interrompe_o_golpe_preparado(self):
        g = mago()
        cb, e = luta(g, "mercenario", nivel=4)
        e.carregando = {"mult": 2.2, "rotulo": "Golpe Esmagador"}
        lancar(g, cb)
        hp = g.j.hp
        g.ui.lances = []
        cb.fase_inimigos()
        self.assertIsNone(e.carregando)
        self.assertTrue(any(l["tipo"] == "atordoado" and l["rotulo"] == "golpe interrompido!" for l in g.ui.lances))
        self.assertEqual(g.j.hp, hp)
        self.assertTrue(e.efeito("firme"))  # e depois fica firme: não congela de novo no turno seguinte
        g.combate_ativo = None

    def test_na_luta_nao_ha_troca(self):
        g = mago()
        cb, _ = luta(g)
        g.ui.roteiro = ["Atacar"]
        cb.fase_jogador()
        self.assertFalse(any(m and "versao" in m for ms in g.ui.metas for m in (ms or [])))
        g.combate_ativo = None


class TestTroca(unittest.TestCase):
    def test_a_compra_ja_leva_a_prisao_e_avisa(self):
        g = mago(talento=False, roteiro=["▶ Prisão de Gelo", "Voltar"])
        g.j.pontos_talento = 1
        g.menu_talentos()
        self.assertEqual((g.j.tal("prisao_gelo"), versao(g.j, "lanca_gelo")), (1, "prisao_gelo"))
        self.assertIn(talentos.frase_transformacao(PRISAO), g.ui.ditos)
        texto = next(o for o in g.ui.ofertas[0] if o.startswith("▶ Prisão de Gelo"))
        self.assertIn("Lança de Gelo: 10 de mana", texto)  # a árvore compara, com os números do herói
        self.assertIn("Prisão de Gelo: 16 de mana", texto)
        no = next(n for n in talentos.dados_arvore(g.j)["nos"] if n["id"] == "prisao_gelo")
        self.assertEqual((no["ramo"], no["camada"], no["max"], no["icone"]), ("tronco", 2, 1, "gelo"))

    def test_troca_na_vila(self):
        """No texto, a opção do menu troca, e uma linha curta diz a versão em uso (o menu só mostra a troca de volta)."""
        g = mago(roteiro=["Grimório: usar a Lança de Gelo"])
        vila = next(l for l in g.mundo["locais"] if l["tipo"] == "vila")
        g.mundo["atual"] = vila["id"]
        g.menu_vila()
        self.assertEqual(versao(g.j, "lanca_gelo"), "lanca_gelo")
        self.assertEqual(g.ui.ditos[-1], "Em uso: Lança de Gelo.")
        self.assertEqual(g.registro[-1]["t"], "versao")
        meta = next(m for m in g.ui.metas[-1] if m and "versao" in m)
        self.assertEqual(meta, {"versao": "lanca_gelo", "para": "lanca_gelo"})
        self.assertEqual(g.opcoes_versao()[0][0], "Grimório: usar a Prisão de Gelo no lugar da Lança de Gelo")

    def test_troca_no_acampamento(self):
        from rpg.comitiva.fogueira import fogueira
        g = mago(roteiro=["Grimório: usar a Lança de Gelo", "Grimório: usar a Prisão de Gelo",
                          "Dormir até o amanhecer"])
        fogueira(g)
        self.assertEqual(versao(g.j, "lanca_gelo"), "prisao_gelo")
        self.assertEqual([d for d in g.ui.ditos if d.startswith("Em uso:")],
                         ["Em uso: Lança de Gelo.", "Em uso: Prisão de Gelo."])

    def test_na_tela_a_pagina_confirma(self):
        """Na tela gráfica, a página do Grimório mostra o que mudou: o motor não diz nada, e a ponte não faz da troca
        um passo da história (sem eco no texto, sem página nova, sem Continuar)."""
        class Tela(Anotador):
            troca_no_grimorio = True
        g = mago()
        g.ui = Tela(["Grimório: usar a Lança de Gelo"])
        g.ui.jogo = g
        vila = next(l for l in g.mundo["locais"] if l["tipo"] == "vila")
        g.mundo["atual"] = vila["id"]
        g.menu_vila()
        self.assertEqual(versao(g.j, "lanca_gelo"), "lanca_gelo")
        self.assertFalse(any("Em uso" in d for d in g.ui.ditos))
        ui = WebUI()
        enviados = []
        ui._enviar = lambda tipo, **dados: enviados.append(tipo)
        ui.enviar_estado = lambda: None
        ui.respostas.put((1, 0))
        ui.meta_opcoes = [{"versao": "lanca_gelo", "para": "lanca_gelo"}, None]
        ui.tipo_cena, antes = "local", ui.escolhas_na_cena
        self.assertEqual(ui.escolher("", ["Grimório: usar a Lança de Gelo no lugar da Prisão de Gelo", "Passear"]), 0)
        self.assertEqual((enviados, ui.escolhas_na_cena), (["opcoes"], antes))  # a vila fica na mesma página
        ui.tipo_cena = "menu"  # a fogueira se redesenha: página nova, ainda sem eco
        ui.respostas.put((2, 0))
        ui.escolher("", ["Grimório: usar a Prisão de Gelo no lugar da Lança de Gelo", "Dormir"])
        self.assertEqual((enviados, ui.escolhas_na_cena), (["opcoes", "opcoes"], antes + 1))

    def test_sem_talento_nenhuma_opcao(self):
        self.assertEqual(mago(talento=False).opcoes_versao(), [])
        g = mago(nivel=1, talento=True)  # o talento sem a Lança ainda aprendida: nada a trocar
        g.j.habilidades = [h for h in g.j.habilidades if h != "lanca_gelo"]
        self.assertEqual(g.opcoes_versao(), [])

    def test_pagina_do_grimorio(self):
        g = mago()
        pagina = next(p for p in grimorio.dados(g.j)["habilidades"] if p["id"] == "lanca_gelo")
        v = pagina["versao"]
        self.assertEqual(v["origem"], "Duas versões, pelo talento Prisão de Gelo.")
        self.assertEqual((v["para"], v["outra"]), ("lanca_gelo", "Lança de Gelo"))
        self.assertEqual([(x["id"], x["em_uso"]) for x in v["versoes"]], [("lanca_gelo", False), ("prisao_gelo", True)])
        self.assertTrue(v["versoes"][0]["texto"].startswith("Lança de Gelo: 10 de mana"))
        self.assertTrue(v["versoes"][1]["texto"].startswith("Prisão de Gelo: 16 de mana"))
        self.assertEqual((pagina["nome"], pagina["custo"]), ("Prisão de Gelo", 16))  # a página é a da versão em uso
        escolher_versao(g.j, "lanca_gelo", None)
        pagina = next(p for p in grimorio.dados(g.j)["habilidades"] if p["id"] == "lanca_gelo")
        self.assertEqual((pagina["nome"], pagina["custo"]), ("Lança de Gelo", 10))
        self.assertIn("× 130%", pagina["linhas"][0]["formula"])
        self.assertEqual([(x["id"], x["em_uso"]) for x in pagina["versao"]["versoes"]],
                         [("lanca_gelo", True), ("prisao_gelo", False)])  # a mesma ordem: só a marca muda de linha
        self.assertEqual(pagina["versao"]["outra"], "Prisão de Gelo")
        self.assertIn("    Duas versões, pelo talento Prisão de Gelo. Em uso: Lança de Gelo; a outra é a Prisão de Gelo. "
                      "Troque na vila ou no acampamento. Na luta, vale a versão em uso.", grimorio.texto(g.j))
        sem = next(p for p in grimorio.dados(mago(talento=False).j)["habilidades"] if p["id"] == "lanca_gelo")
        self.assertNotIn("versao", sem)


class TestSave(unittest.TestCase):
    def test_a_escolha_volta_do_save(self):
        pasta = tempfile.mkdtemp()
        g = mago(pasta=pasta)
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
        self.assertEqual(versao(h.j, "lanca_gelo"), "prisao_gelo")
        escolher_versao(h.j, "lanca_gelo", None)
        h.salvar(silencioso=True)
        k = Jogo.carregar(Roteiro(), h.caminho_save(), pasta)
        self.assertEqual((versao(k.j, "lanca_gelo"), k.j.tal("prisao_gelo")), ("lanca_gelo", 1))

    def test_save_antigo_sem_o_campo(self):
        pasta = tempfile.mkdtemp()
        g = mago(talento=False, pasta=pasta)
        self.assertNotIn("versoes", g.j.para_dict())  # herói sem transformação: o save não ganha campo novo
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
        self.assertEqual(efetiva(h.j, "lanca_gelo")["nome"], "Lança de Gelo")
        self.assertEqual(h.opcoes_versao(), [])


if __name__ == "__main__":
    unittest.main()
