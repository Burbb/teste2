"""A forja no save (27, seção 8): os materiais, o reforço, os sulcos e as gravações sobrevivem a salvar e carregar; um
save da 1.214 (formato 8) passa para o 9 com os materiais, os sulcos das peças antigas e as peças reforçadas pelo
ferreiro anterior de volta à peça original, no mesmo +N, pelas regras da forja. E a forja sem a tela gráfica."""

import copy
import json
import random
import unittest

from rpg import itens
from rpg.forja import encanto as E
from rpg.forja import oficina as D
from rpg.forja import regras as R
from rpg.jogo import Jogo
from rpg.migracoes import VERSAO_SAVE, _v8_para_v9, migrar
from tests import forja_apoio as A


class TestSalvarCarregar(unittest.TestCase):
    def test_materiais_reforco_sulcos_e_gravacoes_voltam_iguais(self):
        g = A.jogo()
        g.j.nivel = 9
        D.materiais(g).update({"fragmento": 17, "essencia_brasa_2": 3})
        arma = g.j.equip["arma"]
        g.j.ouro = 5000
        self.assertTrue(A.reforcar(g, arma["uid"], pedido="a")[0])
        self.assertTrue(D.encantar(g, arma["uid"], "brasa:2", 0, pedido="b")[0])
        antes = (copy.deepcopy(arma), dict(D.materiais(g)))
        g.salvar(silencioso=True)
        h = Jogo.carregar(g.ui, g.caminho_save(), g.pasta_saves)
        arma2 = h.j.equip["arma"]
        self.assertEqual((arma2, D.materiais(h)), antes)
        self.assertEqual(E.requisito(arma2), E.requisito(antes[0]))

    def test_o_save_novo_esta_no_formato_atual_sem_os_contadores_da_luta(self):
        g = A.jogo()
        g.j._tique, g.j._fracao = 3, {"regen_vida": (3, 2, 0.6)}
        g.salvar(silencioso=True)
        with open(g.caminho_save(), encoding="utf-8") as f:
            d = json.load(f)
        self.assertEqual(d["versao"], VERSAO_SAVE)
        self.assertIn("materiais", d)
        self.assertNotIn("_tique", d["jogador"])
        self.assertNotIn("_fracao", d["jogador"])


def save_antigo():
    """Um save do formato 8 (a 1.214): sem materiais, peças sem sulcos e a arma +3 do ferreiro anterior (Ataque 9 → 12:
    cada passo somou max(1, round(12%)) à linha da classe), sem a peça original guardada."""
    g = A.jogo()
    g.salvar(silencioso=True)
    with open(g.caminho_save(), encoding="utf-8") as f:
        d = json.load(f)
    d["versao"] = 8
    d.pop("materiais", None)

    def antigas(no):
        if isinstance(no, dict):
            if "slot" in no and isinstance(no.get("bonus"), dict):
                no.pop("encantos", None)
            for v in no.values():
                antigas(v)
        elif isinstance(no, list):
            for v in no:
                antigas(v)
    antigas(d)
    arma = d["jogador"]["equip"]["arma"]
    base = dict(arma["bonus"])
    arma["bonus"]["atk"] = 9
    for _ in range(3):  # o ferreiro anterior: +12% (mínimo 1) por passo, na mesma peça
        arma["bonus"]["atk"] += max(1, round(arma["bonus"]["atk"] * 0.12))
    arma["reforco"], arma["nome"] = 3, arma["nome"].split(" +")[0] + " +3"
    return d, base


class TestMigracao(unittest.TestCase):
    def test_o_formato_8_ganha_materiais_sulcos_e_a_peca_original(self):
        d, base = save_antigo()
        self.assertEqual(d["jogador"]["equip"]["arma"]["bonus"]["atk"], 12)  # 9 → 10 → 11 → 12 (12% arredondado: 1)
        m = migrar(copy.deepcopy(d))
        self.assertEqual(m["versao"], VERSAO_SAVE)
        self.assertEqual(m["materiais"], {})
        arma = m["jogador"]["equip"]["arma"]
        self.assertEqual(arma["bonus_base"]["atk"], 9)  # a conta antiga desfeita, passo a passo
        self.assertEqual(arma["reforco"], 3)
        self.assertEqual(arma["nome"].split(" +")[1], "3")
        self.assertEqual(arma["bonus"]["atk"], R.limpo(9 + R.ganho_total(arma, 3)["atk"]))  # o +3 pelas regras da forja
        for it in m["jogador"]["mochila"] + list(m["jogador"]["equip"].values()):
            if it and E.tipo(it):
                self.assertIsInstance(it.get("encantos"), list)

    def test_rodar_de_novo_nao_muda_nada(self):
        d, _ = save_antigo()
        d = migrar(d)
        d2 = _v8_para_v9(copy.deepcopy(d))
        self.assertEqual(d2, d)

    def test_carrega_e_joga_a_forja(self):
        d, _ = save_antigo()
        g = A.jogo()
        with open(g.caminho_save(), "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False)
        h = Jogo.carregar(g.ui, g.caminho_save(), g.pasta_saves)
        D.dar_uid(h)
        arma = h.j.equip["arma"]
        h.j.ouro, D.materiais(h)["fragmento"] = 999, 20
        ok, texto = A.reforcar(h, arma["uid"], pedido="x", teste="sucesso")
        self.assertTrue(ok, texto)
        self.assertEqual(arma["reforco"], 4)
        self.assertEqual(arma["bonus"]["atk"], R.limpo(9 + R.ganho_total(arma, 4)["atk"]))


class TestSemTelaGrafica(unittest.TestCase):
    def test_no_texto_a_forja_reforca_pela_lista(self):
        g = A.jogo()
        g.j.ouro, D.materiais(g)["fragmento"] = 999, 10
        arma = g.j.equip["arma"]
        escolhas = iter([arma["uid"], "voltar"])
        g.menu = lambda pergunta, opcoes, *a, **k: next(escolhas)
        D.forja(g)
        self.assertEqual(arma["reforco"], 1)  # o +1 é garantido
        self.assertEqual(D.materiais(g)["fragmento"], 10 - R.custo(0)[1])


class TestPecasNovas(unittest.TestCase):
    def test_o_gerador_e_o_unico_trazem_os_sulcos(self):
        rng = random.Random(4)
        for _ in range(30):
            it = itens.gerar_equip(rng, "guerreiro", 5)
            self.assertEqual("encantos" in it, bool(E.tipo(it)))
        u = itens.fazer_unico(itens.UNICOS_POR_ID["lamento_de_gharbad"], 3)
        self.assertIsInstance(u["encantos"], list)


if __name__ == "__main__":
    unittest.main()
