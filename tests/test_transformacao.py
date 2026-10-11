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
        self.assertEqual(pagina["linhas"][0]["nota"], "Não pode ser esquivado.")
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
        g = mago(roteiro=["Grimório: levar a Lança de Gelo"])
        vila = next(l for l in g.mundo["locais"] if l["tipo"] == "vila")
        g.mundo["atual"] = vila["id"]
        g.menu_vila()
        self.assertEqual(versao(g.j, "lanca_gelo"), "lanca_gelo")
        self.assertIn("Você passa a levar a Lança de Gelo no lugar da Prisão de Gelo. Na luta, é ela que sai.",
                      g.ui.ditos)
        self.assertEqual(g.registro[-1]["t"], "versao")
        meta = next(m for m in g.ui.metas[-1] if m and "versao" in m)
        self.assertEqual(meta, {"versao": "lanca_gelo", "para": "lanca_gelo"})
        self.assertEqual(g.opcoes_versao()[0][0], "Grimório: levar a Prisão de Gelo no lugar da Lança de Gelo")

    def test_troca_no_acampamento(self):
        from rpg.comitiva.fogueira import fogueira
        g = mago(roteiro=["Grimório: levar a Lança de Gelo", "Grimório: levar a Prisão de Gelo",
                          "Dormir até o amanhecer"])
        fogueira(g)
        self.assertEqual(versao(g.j, "lanca_gelo"), "prisao_gelo")
        self.assertEqual(sum(d.startswith("Você passa a levar") for d in g.ui.ditos), 2)

    def test_sem_talento_nenhuma_opcao(self):
        self.assertEqual(mago(talento=False).opcoes_versao(), [])
        g = mago(nivel=1, talento=True)  # o talento sem a Lança ainda aprendida: nada a trocar
        g.j.habilidades = [h for h in g.j.habilidades if h != "lanca_gelo"]
        self.assertEqual(g.opcoes_versao(), [])

    def test_pagina_do_grimorio(self):
        g = mago()
        pagina = next(p for p in grimorio.dados(g.j)["habilidades"] if p["id"] == "lanca_gelo")
        v = pagina["versao"]
        self.assertEqual(v["origem"], "Versão liberada pelo talento Prisão de Gelo, no lugar da Lança de Gelo.")
        self.assertEqual((v["para"], v["outra"]), ("lanca_gelo", "Lança de Gelo"))
        self.assertTrue(v["comparar"][0].startswith("Prisão de Gelo: 16 de mana"))
        self.assertTrue(v["comparar"][1].startswith("Lança de Gelo: 10 de mana"))
        escolher_versao(g.j, "lanca_gelo", None)
        pagina = next(p for p in grimorio.dados(g.j)["habilidades"] if p["id"] == "lanca_gelo")
        self.assertEqual(pagina["nome"], "Lança de Gelo")
        self.assertEqual(pagina["versao"]["origem"], "O talento Prisão de Gelo libera outra versão desta habilidade: "
                                                     "a Prisão de Gelo.")
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
