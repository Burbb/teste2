"""As árvores vivas com o nome novo (1.181.0): o ent jovem é a árvore desperta e o Ent Ancião, a Árvore Anciã. Os ids,
os números e as regras ficam; o nome, o plural e o gênero vêm do catálogo. Um save de antes (formato 5) carrega com os
nomes novos no guardião, nos rumores e nos contratos, sem perder progresso nem duplicar nada, e salvar de novo não muda."""

import json
import random
import tempfile
import unittest

from rpg import migracoes
from rpg.dados import FAMILIAS
from rpg.inimigos import GUARDIOES, criar, gerar_guardiao, instanciar_guardiao
from rpg.jogo import Jogo
from rpg.sistemas.contratos import desc_alvo, desc_caca
from tests.test_abertura import Jogador

ANCIA = next(t for t in GUARDIOES["floresta"] if t["id"] == "ent_anciao")


class TestNomes(unittest.TestCase):
    def test_catalogo(self):
        f = FAMILIAS["ent_jovem"]
        self.assertEqual((f["nome"], f["plural"], f["g"]), ("árvore desperta", "árvores despertas", "f"))
        self.assertEqual((f["hp"], f["atk"], f["habs"], f["tracos"]), (40, 8, ["esmagar", "regenerar"], ["planta", "blindado"]))
        self.assertEqual((ANCIA["base"], ANCIA["g"], ANCIA["hp"]), ("Árvore Anciã", "f", 160))

    def test_concordancia(self):
        r = random.Random(1)
        self.assertEqual(criar(r, "ent_jovem", 3, "corrompido").nome, "Árvore desperta Corrompida")
        self.assertEqual(criar(r, "ent_jovem", 3, "anciao", "Grum").nome, "Grum, a Árvore desperta Anciã")
        self.assertEqual(desc_caca(3, "ent_jovem", "Bosque X"), "Eliminar 3 árvores despertas em Bosque X.")
        self.assertEqual(desc_alvo("Grum", "ent_jovem", "Bosque X"), "Caçar Grum, uma árvore desperta enorme que aterroriza Bosque X.")
        while (spec := gerar_guardiao(r, "floresta"))["id"] != "ent_anciao":
            pass
        self.assertTrue(spec["nome"].endswith(", a Árvore Anciã"), spec["nome"])
        self.assertEqual(instanciar_guardiao(spec, 5).nome, spec["nome"])


class TestSaveAntigo(unittest.TestCase):
    def preparar(self):
        """Um jogo do mundo gerado com o que um save de antes da 1.181.0 guardava como texto."""
        pasta = tempfile.mkdtemp()
        g = Jogo(Jogador(), seed=4, pasta_saves=pasta, hardcore=False)
        g.iniciar("Teste", "guerreiro")
        covil = next(l for l in g.mundo["locais"] if l["tipo"] == "covil")
        selvagem = next(l for l in g.mundo["locais"] if l["tipo"] == "selvagem")
        covil["guardiao"] = {"bioma": "floresta", "id": "ent_anciao", "idx": GUARDIOES["floresta"].index(ANCIA),
                             "nome": "Thorn, o Ent Ancião", "g": "m", "derrotado": False, "base": "Ent Ancião"}
        g.rumores.append({"texto": f"Thorn, o Ent Ancião, vive em {covil['nome']}.", "expira": g.dia + 30})
        g.rumores.append({"texto": "Ninguém volta do Pico.", "expira": g.dia + 30})
        g.contratos.append({"id": 77, "tipo": "caca", "local": selvagem["id"], "familia": "ent_jovem", "total": 3,
                            "feito": 2, "ouro": 40, "xp": 50, "desc": f"Eliminar 3 ents jovens em {selvagem['nome']}."})
        g.contratos.append({"id": 78, "tipo": "caca", "local": selvagem["id"], "familia": "lobo", "total": 2, "feito": 0,
                            "ouro": 20, "xp": 20, "desc": f"Eliminar 2 lobos em {selvagem['nome']}."})
        g.ofertas[str(g.loc["id"])] = {"dia": g.dia, "lista": [
            {"id": 79, "tipo": "alvo", "local": selvagem["id"], "familia": "ent_jovem", "nome": "Grum", "chave": "alvo:79",
             "ouro": 60, "xp": 70, "desc": f"Caçar Grum, um ent jovem enorme que aterroriza {selvagem['nome']}."}]}
        g.salvar(silencioso=True)
        with open(g.caminho_save(), encoding="utf-8") as f:
            dados = json.load(f)
        dados["versao"] = 5  # como um save gravado antes da migração
        with open(g.caminho_save(), "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False)
        return g, covil["id"], selvagem["nome"], pasta

    def test_carregar_e_salvar_de_novo(self):
        g, cid, lugar, pasta = self.preparar()
        h = Jogo.carregar(Jogador(), g.caminho_save(), pasta)
        covil = next(l for l in h.mundo["locais"] if l["id"] == cid)
        self.assertEqual(covil["guardiao"]["nome"], "Thorn, a Árvore Anciã")
        self.assertEqual((covil["guardiao"]["base"], covil["guardiao"]["g"], covil["guardiao"]["id"]),
                         ("Árvore Anciã", "f", "ent_anciao"))
        self.assertFalse(covil["guardiao"]["derrotado"])
        self.assertEqual([r["texto"] for r in h.rumores][-2:],
                         [f"Thorn, a Árvore Anciã, vive em {covil['nome']}.", "Ninguém volta do Pico."])
        self.assertEqual([(c["id"], c["feito"], c["desc"]) for c in h.contratos][-2:],
                         [(77, 2, f"Eliminar 3 árvores despertas em {lugar}."), (78, 0, f"Eliminar 2 lobos em {lugar}.")])
        self.assertEqual(len(h.contratos), len(g.contratos))
        oferta = h.ofertas[str(g.loc["id"])]["lista"]
        self.assertEqual([c["desc"] for c in oferta], [f"Caçar Grum, uma árvore desperta enorme que aterroriza {lugar}."])
        self.assertEqual(instanciar_guardiao(covil["guardiao"], 5).nome, "Thorn, a Árvore Anciã")
        # salvar e carregar de novo: o mesmo save, sem migrar outra vez
        h.salvar(silencioso=True)
        with open(h.caminho_save(), encoding="utf-8") as f:
            primeiro = json.load(f)
        self.assertEqual(primeiro["versao"], migracoes.VERSAO_SAVE)
        k = Jogo.carregar(Jogador(), h.caminho_save(), pasta)
        k.salvar(silencioso=True)
        with open(k.caminho_save(), encoding="utf-8") as f:
            segundo = json.load(f)
        for campo in ("mundo", "rumores", "contratos", "ofertas"):
            self.assertEqual(primeiro[campo], segundo[campo], campo)

    def test_migrar_duas_vezes_nao_muda(self):
        g, _, _, _ = self.preparar()
        with open(g.caminho_save(), encoding="utf-8") as f:
            dados = json.load(f)
        uma = migracoes._v5_para_v6(json.loads(json.dumps(dados)))
        duas = migracoes._v5_para_v6(json.loads(json.dumps(uma)))
        self.assertEqual(uma, duas)


if __name__ == "__main__":
    unittest.main()
