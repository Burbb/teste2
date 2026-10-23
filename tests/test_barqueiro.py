"""O Barqueiro do Charco no lugar da Bruxa Afogada nos covis do pântano (1.200.0). A posição e as regras da ficha ficam
(o sorteio dos mundos não muda); a Ilse da campanha tem a ficha dela e não muda. Um save de antes (formato 6) carrega
com o Barqueiro no covil e nos rumores, sem perder progresso, e salvar de novo não repete a migração."""

import json
import random
import tempfile
import unittest

from rpg import migracoes, missoes
from rpg.dados import GUARDIOES, GUARDIOES_UNICOS
from rpg.eventos.comuns import sinais_do_guardiao
from rpg.inimigos import ficha_guardiao, gerar_guardiao, instanciar_guardiao
from rpg.jogo import Jogo
from tests.test_abertura import Jogador
from tests.test_missoes import MID, campanha

REGRAS = ("hp", "atk", "defesa", "agi", "poder", "tracos", "habs", "invoca", "ataque")


class TestCatalogo(unittest.TestCase):
    def test_no_lugar_da_bruxa_com_as_mesmas_regras(self):
        self.assertEqual([t["id"] for t in GUARDIOES["pantano"]], ["hidra_do_brejo", "barqueiro_do_charco"])
        b, ilse = GUARDIOES["pantano"][1], GUARDIOES_UNICOS["ilse"]
        self.assertEqual((b["base"], b["g"]), ("Barqueiro do Charco", "m"))
        self.assertEqual({k: b[k] for k in REGRAS}, {k: ilse[k] for k in REGRAS})
        (fb,), (fi,) = b["fases"], ilse["fases"]
        self.assertEqual({k: v for k, v in fb.items() if k != "texto"}, {k: v for k, v in fi.items() if k != "texto"})
        self.assertNotIn("canto", fb["texto"])
        self.assertTrue(all(t["id"] != "bruxa_afogada" for lista in GUARDIOES.values() for t in lista))

    def test_sorteado_com_o_artigo(self):
        r = random.Random(2)
        while (spec := gerar_guardiao(r, "pantano"))["id"] != "barqueiro_do_charco":
            pass
        self.assertEqual(spec["idx"], 1)
        self.assertTrue(spec["nome"].endswith(", o Barqueiro do Charco"), spec["nome"])
        e = instanciar_guardiao(spec, 5)
        self.assertEqual((e.nome, e.g, e.guardiao), (spec["nome"], "m", "barqueiro_do_charco"))

    def test_o_sinal_do_covil(self):
        ditos = []

        class G:
            loc = {"id": 9, "tipo": "covil", "guardiao": {"base": "Barqueiro do Charco", "derrotado": False}}

            def flag(self, nome):
                return True  # o ponto fraco já conhecido: depois do sinal, o evento só traz uma luta

            def combate(self, grupo):
                pass

            def grupo(self, n):
                return []

            def dizer(self, texto, cor=None):
                ditos.append(texto)
        sinais_do_guardiao(G())
        self.assertEqual(ditos, ["Uma lanterna verde atravessa o charco à noite, sem fazer barulho na água."])


def regravar(g, versao):
    """O save do jogo como se tivesse sido gravado no formato `versao`."""
    g.salvar(silencioso=True)
    with open(g.caminho_save(), encoding="utf-8") as f:
        dados = json.load(f)
    dados["versao"] = versao
    with open(g.caminho_save(), "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False)
    return dados


class TestSaveAntigo(unittest.TestCase):
    def preparar(self, guardiao):
        """Um mundo gerado com um covil da Bruxa Afogada, como um save de antes da 1.200.0 guardava."""
        pasta = tempfile.mkdtemp()
        g = Jogo(Jogador(), seed=4, pasta_saves=pasta, hardcore=False)
        g.iniciar("Teste", "guerreiro")
        covis = [l for l in g.mundo["locais"] if l["tipo"] == "covil"]
        covil, outro = covis[0], covis[1]
        covil["guardiao"] = dict(guardiao)
        outro["guardiao"]["derrotado"] = True
        g.rumores.append({"texto": f"Irdor, a Bruxa Afogada, vive em {covil['nome']}.", "expira": g.dia + 30})
        g.rumores.append({"texto": "Ninguém volta do Pico.", "expira": g.dia + 30})
        g.j.sigilos.append(outro["bioma"])
        regravar(g, 6)
        return g, covil["id"], outro, pasta

    BRUXA = {"bioma": "pantano", "id": "bruxa_afogada", "idx": 1, "nome": "Irdor, a Bruxa Afogada", "g": "f",
             "derrotado": False, "base": "Bruxa Afogada"}

    def conferir(self, guardiao, derrotado):
        g, cid, outro, pasta = self.preparar(dict(guardiao, derrotado=derrotado))
        h = Jogo.carregar(Jogador(), g.caminho_save(), pasta)
        covil = next(l for l in h.mundo["locais"] if l["id"] == cid)
        self.assertEqual(covil["guardiao"], {"bioma": "pantano", "id": "barqueiro_do_charco", "idx": 1,
                                             "nome": "Irdor, o Barqueiro do Charco", "g": "m", "derrotado": derrotado,
                                             "base": "Barqueiro do Charco"} if "idx" in guardiao else
                         {"bioma": "pantano", "id": "barqueiro_do_charco", "nome": "Irdor, o Barqueiro do Charco",
                          "g": "m", "derrotado": derrotado, "base": "Barqueiro do Charco"})
        self.assertEqual([r["texto"] for r in h.rumores][-2:],
                         [f"Irdor, o Barqueiro do Charco, vive em {covil['nome']}.", "Ninguém volta do Pico."])
        # o resto do progresso fica: o outro covil, o Sigilo, o resto do mundo
        self.assertEqual(next(l for l in h.mundo["locais"] if l["id"] == outro["id"])["guardiao"], outro["guardiao"])
        self.assertEqual(h.j.sigilos, g.j.sigilos)
        self.assertEqual(ficha_guardiao(covil["guardiao"])["id"], "barqueiro_do_charco")
        self.assertEqual(instanciar_guardiao(covil["guardiao"], 5).nome, "Irdor, o Barqueiro do Charco")
        # salvar e carregar de novo: o mesmo save, sem migrar outra vez
        h.salvar(silencioso=True)
        with open(h.caminho_save(), encoding="utf-8") as f:
            primeiro = json.load(f)
        self.assertEqual(primeiro["versao"], migracoes.VERSAO_SAVE)
        k = Jogo.carregar(Jogador(), h.caminho_save(), pasta)
        k.salvar(silencioso=True)
        with open(k.caminho_save(), encoding="utf-8") as f:
            segundo = json.load(f)
        for campo in ("mundo", "rumores", "contratos", "flags"):
            self.assertEqual(primeiro[campo], segundo[campo], campo)

    def test_covil_vivo(self):
        self.conferir(self.BRUXA, False)

    def test_covil_vencido(self):
        self.conferir(self.BRUXA, True)

    def test_save_de_antes_do_id(self):
        self.conferir({k: v for k, v in self.BRUXA.items() if k != "id"}, False)

    def test_save_de_antes_das_arvores(self):
        # um formato 5 passa pela migração das árvores (que já refaz o nome pelo catálogo) e depois por esta
        g, cid, _, pasta = self.preparar(self.BRUXA)
        regravar(g, 5)
        h = Jogo.carregar(Jogador(), g.caminho_save(), pasta)
        covil = next(l for l in h.mundo["locais"] if l["id"] == cid)
        self.assertEqual((covil["guardiao"]["id"], covil["guardiao"]["nome"]),
                         ("barqueiro_do_charco", "Irdor, o Barqueiro do Charco"))
        self.assertEqual(h.rumores[-2]["texto"], f"Irdor, o Barqueiro do Charco, vive em {covil['nome']}.")

    def test_migrar_duas_vezes_nao_muda(self):
        g, _, _, _ = self.preparar(self.BRUXA)
        with open(g.caminho_save(), encoding="utf-8") as f:
            dados = json.load(f)
        uma = migracoes._v6_para_v7(json.loads(json.dumps(dados)))
        duas = migracoes._v6_para_v7(json.loads(json.dumps(uma)))
        self.assertEqual(uma, duas)

    def test_os_outros_guardioes_nao_mudam(self):
        g, _, _, _ = self.preparar(self.BRUXA)
        with open(g.caminho_save(), encoding="utf-8") as f:
            dados = json.load(f)
        antes = [l["guardiao"] for l in dados["mundo"]["locais"] if l.get("guardiao")]
        depois = [l["guardiao"] for l in migracoes._v6_para_v7(json.loads(json.dumps(dados)))["mundo"]["locais"]
                  if l.get("guardiao")]
        mudou = [(a["id"] if "id" in a else a["idx"], b["id"]) for a, b in zip(antes, depois) if a != b]
        self.assertEqual(mudou, [("bruxa_afogada", "barqueiro_do_charco")])


class TestIlsePreservada(unittest.TestCase):
    def test_save_da_campanha_carrega_igual(self):
        pasta = tempfile.mkdtemp()
        g = campanha(pasta=pasta)
        m = missoes.registro(g, MID)
        m.update(etapa="fundo", pistas=["ilse", "verdade_de_ilse"], preparos=["fita"])
        dados = regravar(g, 6)
        h = Jogo.carregar(Jogador(), g.caminho_save(), pasta)
        self.assertEqual(h.mundo, {**dados["mundo"]})
        self.assertEqual(missoes.registro(h, MID)["pistas"], ["ilse", "verdade_de_ilse"])
        # a guardiã continua a Ilse: a ficha dela, o nome e as regras de sempre
        spec = {"bioma": "pantano", "id": "ilse", "nome": "Ilse, a Bruxa Afogada", "g": "f", "base": "Bruxa Afogada"}
        self.assertIs(ficha_guardiao(spec), GUARDIOES_UNICOS["ilse"])
        e = instanciar_guardiao(spec, 4)
        self.assertEqual((e.nome, e.g, e.guardiao, e.hp), ("Ilse, a Bruxa Afogada", "f", "ilse", e.max_hp))
        self.assertIn("canto", e.fases[0]["texto"])


if __name__ == "__main__":
    unittest.main()
