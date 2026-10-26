"""A cabeça e as mãos de couro e de tecido (1.112.0): o Capuz e a Luva de Seda do Mago com os desenhos de tecido, o
Arqueiro e as Mãos do Estrangulador com os de couro, e os saves antigos (v4) levados ao desenho certo pela migração.
O que decide é o próprio item (o espaço, a classe para a qual foi feito, o desenho que ele guarda), nunca o nome nem
quem o carrega."""

import copy
import json
import os
import random
import tempfile
import unittest

from rpg import itens
from rpg.migracoes import VERSAO_SAVE, _v4_para_v5, migrar


def _peca(classe, slot, base, icone, **extra):
    return {"nome": base, "base": base, "slot": slot, "bonus": {"defesa": 2}, "preco": 10, "classe": classe,
            "raridade": "comum", "icone": icone, "nivel": 3, **extra}


class TestItensNovos(unittest.TestCase):
    def test_cada_classe_ganha_o_seu_material(self):
        rng = random.Random(1)
        vistos = {}
        for _ in range(400):
            for classe in ("mago", "arqueiro"):
                for slot in ("cabeca", "maos"):
                    it = itens.gerar_equip(rng, classe, 6, slot=slot, raridade="comum")
                    vistos.setdefault((classe, it["base"].split()[0]), set()).add(it["icone"])
        self.assertEqual(vistos[("mago", "Capuz")], {"capuz_tecido"})
        self.assertEqual(vistos[("mago", "Luva")], {"luva_seda"})
        self.assertEqual(vistos[("arqueiro", "Capuz")], {"capuz"})
        self.assertEqual(vistos[("arqueiro", "Chapéu")], {"capuz"})       # a exceção registrada: o chapéu usa o capuz
        self.assertEqual(vistos[("arqueiro", "Braçadeira")], {"luva"})

    def test_o_unico_das_maos_continua_de_couro(self):
        u = next(u for u in itens.UNICOS if u["id"] == "maos_do_estrangulador")
        self.assertEqual(u["icone"], "luva")

    def test_item_sem_desenho_guardado_usa_a_classe_do_item(self):
        # um item de um save de antes do desenho ir no item: a base e a classe dele decidem (não quem o carrega)
        sem = lambda classe, slot, base: {k: v for k, v in _peca(classe, slot, base, None).items() if k != "icone"}
        self.assertEqual(itens.icone_de(sem("mago", "cabeca", "Capuz de Linho")), "capuz_tecido")
        self.assertEqual(itens.icone_de(sem("arqueiro", "cabeca", "Capuz Curtido")), "capuz")
        self.assertEqual(itens.icone_de(sem("mago", "maos", "Luva de Seda Bordada")), "luva_seda")
        self.assertEqual(itens.icone_de(sem("arqueiro", "maos", "Braçadeira Rúnica")), "luva")


def _save_v4():
    """Um save v4 com peças de tecido do Mago e de couro do Arqueiro em todos os lugares que o jogo guarda."""
    mago_capuz = _peca("mago", "cabeca", "Capuz Rúnico", "capuz", afixos=["de Fogo"])
    mago_luva = _peca("mago", "maos", "Luva de Seda Bordada", "luva", raridade="magico")
    arq_capuz = _peca("arqueiro", "cabeca", "Capuz Rúnico", "capuz")                 # o mesmo nome de base, couro
    arq_chapeu = _peca("arqueiro", "cabeca", "Chapéu de Couro Curtido", "capuz")
    arq_bracadeira = _peca("arqueiro", "maos", "Braçadeira Tachonada", "luva")
    estrangulador = _peca(None, "maos", "Luvas", "luva", raridade="lendario", unico="maos_do_estrangulador",
                          nome_unico="Mãos do Estrangulador")
    mago_chapeu = _peca("mago", "cabeca", "Chapéu Pontudo de Linho", "chapeu")
    return {"versao": 4, "seed": 7, "jogador": {
        "classe": "mago", "equip": {"cabeca": copy.deepcopy(mago_capuz), "maos": copy.deepcopy(mago_luva), "pes": None},
        "mochila": [copy.deepcopy(arq_capuz), copy.deepcopy(mago_luva), copy.deepcopy(estrangulador), copy.deepcopy(mago_chapeu)]},
        "mundo": {"locais": [], "missoes": {}},
        "lojas": {"3": {"itens": [copy.deepcopy(mago_capuz), copy.deepcopy(arq_bracadeira)], "recompra": [copy.deepcopy(arq_chapeu)]}},
        "ofertas": [{"item": copy.deepcopy(mago_luva)}],
        "comitiva": [{"id": "odete", "equip": {"cabeca": copy.deepcopy(arq_capuz)}}]}


class TestMigracao(unittest.TestCase):
    def test_v4_para_v5_troca_so_o_desenho_das_pecas_de_tecido_do_mago(self):
        antes = _save_v4()
        depois = migrar(copy.deepcopy(antes))
        self.assertEqual(depois["versao"], VERSAO_SAVE)
        j = depois["jogador"]
        self.assertEqual(j["equip"]["cabeca"]["icone"], "capuz_tecido")
        self.assertEqual(j["equip"]["maos"]["icone"], "luva_seda")
        self.assertEqual([x["icone"] for x in j["mochila"]], ["capuz", "luva_seda", "luva", "chapeu"])
        self.assertEqual([x["icone"] for x in depois["lojas"]["3"]["itens"]], ["capuz_tecido", "luva"])
        self.assertEqual(depois["lojas"]["3"]["recompra"][0]["icone"], "capuz")
        self.assertEqual(depois["ofertas"][0]["item"]["icone"], "luva_seda")
        self.assertEqual(depois["comitiva"][0]["equip"]["cabeca"]["icone"], "capuz")

    def test_nada_alem_do_desenho_muda(self):
        # só o passo v4 → v5 (os seguintes acrescentam o que é deles: os atributos e o kit, na v7)
        antes, depois = _save_v4(), _v4_para_v5(_save_v4())

        def sem_desenho(no):
            if isinstance(no, dict):
                return {k: sem_desenho(v) for k, v in no.items() if k not in ("icone", "versao")}
            if isinstance(no, list):
                return [sem_desenho(v) for v in no]
            return no
        self.assertEqual(sem_desenho(antes), sem_desenho(depois))

    def test_migrar_de_novo_nao_muda_nada(self):
        uma = migrar(_save_v4())
        duas = _v4_para_v5(copy.deepcopy(uma))
        self.assertEqual(uma, duas)
        self.assertEqual(migrar(copy.deepcopy(uma)), uma)  # um save já na v5 passa direto

    def test_save_antigo_carrega_e_regrava_na_v5(self):
        # um jogo de Mago com as peças antigas, gravado como v4, carregado pelo jogo: o desenho certo e o save novo
        from rpg.jogo import Jogo
        from rpg.ui import BotUI
        pasta = tempfile.mkdtemp()
        g = Jogo(BotUI(random.Random(1)), seed=11, pasta_saves=pasta, hardcore=False)
        g.iniciar("Teste", "mago")
        g.j.equip["cabeca"] = _peca("mago", "cabeca", "Capuz de Lã Negra", "capuz")
        g.j.mochila.append(_peca("mago", "maos", "Luva de Seda Puída", "luva"))
        g.j.mochila.append(_peca("arqueiro", "maos", "Braçadeira Curtida", "luva"))
        g.salvar(silencioso=True)
        caminho = next(os.path.join(pasta, f) for f in os.listdir(pasta) if f.endswith(".json"))
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
        dados["versao"] = 4
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False)
        h = Jogo.carregar(BotUI(random.Random(2)), caminho, pasta)
        self.assertEqual(h.j.equip["cabeca"]["icone"], "capuz_tecido")
        self.assertEqual([x["icone"] for x in h.j.mochila[-2:]], ["luva_seda", "luva"])
        h.salvar(silencioso=True)
        with open(caminho, encoding="utf-8") as f:
            self.assertEqual(json.load(f)["versao"], VERSAO_SAVE)


if __name__ == "__main__":
    unittest.main()
