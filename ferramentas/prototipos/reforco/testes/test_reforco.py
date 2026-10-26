"""O protótipo do reforço: as regras, as ações conferidas e os ciclos de recursos.

    python -m unittest discover -s ferramentas/prototipos/reforco/testes -t ferramentas/prototipos/reforco
"""

import os
import random
import subprocess
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
PASTA = os.path.dirname(AQUI)
RAIZ = os.path.normpath(os.path.join(PASTA, "..", "..", ".."))
for p in (RAIZ, PASTA):
    if p not in sys.path:
        sys.path.insert(0, p)

import demo as D  # noqa: E402
import regras as R  # noqa: E402
from rpg import itens  # noqa: E402
from rpg.jogo import Jogo  # noqa: E402
from rpg.regras import LIMITE_MOCHILA  # noqa: E402
from rpg.ui import BotUI  # noqa: E402

D.ativar()


def jogo():
    g = Jogo(BotUI(random.Random(1), max_decisoes=10 ** 6), seed=11, pasta_saves=tempfile.mkdtemp(), hardcore=False)
    g.iniciar("Jean", "guerreiro", "turvo")
    D.preparar(g)
    D.materiais(g)["fragmento"] = 8
    D.dar_uid(g)
    return g


def peca(classe, slot, nivel, material=None):
    rng = random.Random(5)
    while True:
        it = itens.gerar_equip(rng, classe, nivel, slot=slot, raridade="comum")
        if not material or material in it["base"]:
            return it


class TestFormula(unittest.TestCase):
    def test_cada_passo_melhora_algo_e_nunca_cai(self):
        for classe, slot in (("guerreiro", "arma"), ("arqueiro", "arma"), ("mago", "arma"), ("guerreiro", "armadura"),
                             ("mago", "armadura"), ("guerreiro", "secundaria"), ("mago", "secundaria")):
            for nivel in (1, 3, 6, 9, 12):
                it = peca(classe, slot, nivel)
                anterior = {}
                for n in range(1, R.LIMITE + 1):
                    g = R.ganho_total(it, n)
                    self.assertTrue(any(g[s] > anterior.get(s, 0) for s in g), (it["nome"], n, g))
                    self.assertTrue(all(g[s] >= anterior.get(s, 0) for s in g))
                    anterior = g

    def test_arma_inicial_alcanca_uma_base_mais_nova_por_um_tempo(self):
        velha = peca("guerreiro", "arma", 1, "Enferrujad")  # Ataque 2
        self.assertEqual(velha["bonus"]["atk"], 2)
        self.assertEqual(R.ganho_total(velha, R.LIMITE)["atk"], 4)  # +4: 6, como uma de Aço do nível 6
        nova = peca("guerreiro", "arma", 6, "de Aço")
        self.assertGreater(nova["bonus"]["atk"] + R.ganho_total(nova, R.LIMITE)["atk"], 6 + 3)

    def test_so_as_linhas_da_base_crescem(self):
        it = peca("guerreiro", "armadura", 4)
        it["bonus"].update(poder=3, critico=4)  # afixos: o reforço não mexe neles
        self.assertEqual(set(R.ganho_total(it, 2)), {"defesa", "max_hp"})

    def test_quem_nao_recebe_reforco(self):
        for slot, classe in (("cabeca", "guerreiro"), ("anel", None), ("amuleto", None), ("secundaria", "arqueiro")):
            it = {"slot": slot, "classe": classe, "bonus": {"defesa": 1}, "nome": "x"}
            self.assertIsNone(R.tipo(it))
            self.assertTrue(R.motivo_sem_reforco(it))


class TestReforcar(unittest.TestCase):
    def test_paga_e_aplica_junto(self):
        g = jogo()
        arma = g.j.equip["arma"]
        ouro, atk = g.j.ouro, arma["bonus"]["atk"]
        ok, texto = D.reforcar(g, arma["uid"], "fio")
        self.assertTrue(ok, texto)
        self.assertEqual(g.j.ouro, ouro - g.preco(R.OURO[0]))
        self.assertEqual(D.materiais(g)["fragmento"], 7)
        self.assertEqual((arma["reforco"], arma["bonus"]["atk"], arma["veio"]), (1, atk + 1, "fio"))
        self.assertTrue(arma["nome"].endswith(" +1"))

    def test_guerreiro_escolhe_o_veio_uma_vez(self):
        g = jogo()
        arma = g.j.equip["arma"]
        self.assertFalse(D.reforcar(g, arma["uid"])[0])  # sem escolher, nada
        self.assertEqual(D.materiais(g)["fragmento"], 8)
        D.reforcar(g, arma["uid"], "runas")
        self.assertIn("poder", arma["bonus"])
        D.reforcar(g, arma["uid"], "fio")  # o veio já está escolhido: segue Runas
        self.assertEqual(arma["veio"], "runas")
        self.assertEqual(arma["bonus"]["poder"], R.ganho_total(arma, 2)["poder"])

    def test_falta_recurso_nao_cobra_nada(self):
        g = jogo()
        arma = g.j.equip["arma"]
        D.materiais(g)["fragmento"] = 0
        antes = (g.j.ouro, dict(arma["bonus"]), arma.get("reforco", 0))
        ok, texto = D.reforcar(g, arma["uid"], "fio")
        self.assertFalse(ok)
        self.assertEqual((g.j.ouro, dict(arma["bonus"]), arma.get("reforco", 0)), antes)
        g.j.ouro = 0
        D.materiais(g)["fragmento"] = 9
        self.assertFalse(D.reforcar(g, arma["uid"], "fio")[0])
        self.assertEqual(D.materiais(g)["fragmento"], 9)

    def test_limite(self):
        g = jogo()
        g.j.ouro, D.materiais(g)["fragmento"] = 9999, 99
        arma = g.j.equip["arma"]
        for _ in range(R.LIMITE):
            self.assertTrue(D.reforcar(g, arma["uid"], "fio")[0])
        ok, texto = D.reforcar(g, arma["uid"], "fio")
        self.assertFalse(ok)
        self.assertIn("limite", texto)

    def test_companheiro_e_peca_que_ninguem_usa(self):
        g = jogo()
        cajado = D.FICHA.corpo(g, "odete")["arma"]
        poder = D.comitiva.atributos(g, D.comitiva.membro(g, "odete"))["poder"]
        self.assertTrue(D.reforcar(g, cajado["uid"])[0])
        self.assertGreater(D.comitiva.atributos(g, D.comitiva.membro(g, "odete"))["poder"], poder)
        arco = next(it for it in g.j.mochila if it.get("classe") == "arqueiro")
        self.assertIn("Ninguém do grupo", D.reforcar(g, arco["uid"])[1])


class TestDesmontar(unittest.TestCase):
    def test_devolve_metade_do_investido_e_o_da_peca(self):
        g = jogo()
        g.j.ouro, D.materiais(g)["fragmento"] = 9999, 20
        it = next(x for x in g.j.mochila if x.get("raridade") == "magico" and R.tipo(x) == "peito")
        for _ in range(3):  # 1 + 2 + 3 = 6 investidos
            D.reforcar(g, it["uid"])
        self.assertEqual(R.desmontar_rende(it), (3, 1))
        antes = D.materiais(g)["fragmento"]
        ok, texto = D.desmontar(g, it["uid"], it["nome"])
        self.assertTrue(ok, texto)
        self.assertEqual(D.materiais(g)["fragmento"], antes + 4)
        self.assertNotIn(it, g.j.mochila)

    def test_selecao_antiga_ou_peca_vestida_nao_desmonta(self):
        g = jogo()
        alvo = next(x for x in g.j.mochila if x.get("raridade") == "magico")
        self.assertFalse(D.desmontar(g, alvo["uid"], "outro nome")[0])
        self.assertIn(alvo, g.j.mochila)
        self.assertFalse(D.desmontar(g, g.j.equip["arma"]["uid"], g.j.equip["arma"]["nome"])[0])
        n = len(g.j.mochila)
        self.assertTrue(D.desmontar(g, alvo["uid"], alvo["nome"])[0])
        self.assertFalse(D.desmontar(g, alvo["uid"], alvo["nome"])[0])  # já foi: o mesmo pedido de novo não pega outra
        self.assertEqual(len(g.j.mochila), n - 1)

    def test_peca_comum_sem_reforco_nao_rende(self):
        g = jogo()
        comum = next(x for x in g.j.mochila if x.get("raridade") == "comum")
        self.assertEqual(D.desmontar(g, comum["uid"], comum["nome"]), (False, "Não rende material."))

    def test_pilha_cheia_e_bolsa_cheia(self):
        g = jogo()
        while len(g.j.mochila) < LIMITE_MOCHILA:
            g.j.mochila.append(peca("guerreiro", "anel", 3))
        self.assertEqual(D.dar_material(g, "fragmento", 5, "teste"), 5)  # bolsa cheia: o material entra mesmo assim
        self.assertEqual(len(g.j.mochila), LIMITE_MOCHILA)
        D.materiais(g)["fragmento"] = R.PILHA_MAX
        self.assertEqual(D.dar_material(g, "fragmento", 1, "teste"), 0)
        lendaria = next(x for x in g.j.mochila if x.get("raridade") == "lendario")
        ok, texto = D.desmontar(g, lendaria["uid"], lendaria["nome"])
        self.assertFalse(ok)
        self.assertIn(lendaria, g.j.mochila)


class TestCiclos(unittest.TestCase):
    def test_reforcar_e_desfazer_nunca_rende_mais_do_que_custou(self):
        """Reforçar e depois desmontar ou vender: o grupo sai com menos ouro e menos fragmentos do que tinha."""
        for passos in range(1, R.LIMITE + 1):
            for fim in ("desmontar", "vender"):
                g = jogo()
                g.j.ouro, D.materiais(g)["fragmento"] = 2000, 30
                it = next(x for x in g.j.mochila if R.tipo(x) == "peito")
                preco_base = it["preco"]
                ouro0, frag0 = g.j.ouro, D.materiais(g)["fragmento"]
                for _ in range(passos):
                    self.assertTrue(D.reforcar(g, it["uid"])[0])
                if fim == "desmontar":
                    D.desmontar(g, it["uid"], it["nome"])
                    ganho_ouro = 0
                else:
                    ganho_ouro = it["preco"] // 2
                    g.j.mochila.remove(it)
                self.assertLess(g.j.ouro + ganho_ouro - preco_base // 2, ouro0, (passos, fim))
                self.assertLessEqual(D.materiais(g)["fragmento"], frag0 + R.DA_PECA[it["raridade"]], (passos, fim))


class TestIsolamento(unittest.TestCase):
    def test_o_jogo_nao_carrega_o_prototipo(self):
        codigo = ("import sys, rpg.jogo, rpg.web.servidor, rpg.web.estado; "
                  "print(any('prototipos' in (getattr(m, '__file__', '') or '') for m in list(sys.modules.values())))")
        saida = subprocess.run([sys.executable, "-c", codigo], cwd=RAIZ, capture_output=True, text=True).stdout.strip()
        self.assertEqual(saida, "False")


if __name__ == "__main__":
    unittest.main()
