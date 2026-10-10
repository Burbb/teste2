"""O Tiro Duplo (E5, P2): o 1º disparo no alvo escolhido, o 2º em outro inimigo de pé, o mais ferido; sozinho, os
dois no mesmo alvo; a morte do 1º não cancela o 2º. Pela execução de verdade (o menu de habilidades do combate)."""

import random
import tempfile
import unittest

from rpg import dev, especializacao
from rpg.combate import Combate
from rpg.habilidades import HABILIDADES, SEGUNDO_ALVO, descricao_habilidade, mais_ferido, segundo_alvo
from rpg.inimigos import criar
from rpg.jogo import Jogo
from rpg.talentos import custo_habilidade
from tests.test_missoes import Roteiro

NOMES = ("Alfa", "Beta", "Gama")


class Anotador(Roteiro):
    """Roteiro que guarda os lances (a salva do Tiro Duplo chega à tela como um lance só)."""

    def __init__(self, roteiro=()):
        super().__init__(roteiro)
        self.lances = []

    def lance(self, tipo, **dados):
        self.lances.append(dict(dados, tipo=tipo))


def patrulheiro(nivel=5):
    g = Jogo(Anotador(["Lobo"]), seed=5, pasta_saves=tempfile.mkdtemp())
    g.iniciar("Teste", "arqueiro", "turvo")
    dev.subir_ate(g, nivel, spec="patrulheiro")
    g.j.hp, g.j.rec = g.j.max_hp, g.j.max_rec
    return g


def luta(g, vidas, familia="lobo"):
    """Inimigos sem esquiva (Agilidade 0), com a vida pedida (fração da máxima), chamados Alfa, Beta, Gama."""
    r = random.Random(3)
    inimigos = []
    for nome, frac in zip(NOMES, vidas):
        e = criar(r, familia, 4)
        e.nome, e.agi = nome, 0
        e.hp = max(1, int(e.max_hp * frac))
        inimigos.append(e)
    cb = Combate(g, inimigos, pode_fugir=False, sozinho=True)
    cb.turno = 1
    return cb, inimigos


def disparar(g, cb, alvo):
    """O Tiro Duplo pelo menu do combate, no alvo de nome `alvo`. Devolve a salva (os lances dos dois disparos)."""
    g.ui.roteiro = ["Habilidades", "Tiro Duplo", alvo] if len(cb.inimigos_vivos()) > 1 else ["Habilidades", "Tiro Duplo"]
    g.ui.lances = []
    cb.fase_jogador()
    salva = next(l for l in g.ui.lances if l["tipo"] == "salva")
    return [(cb.objeto(l["em"]).nome, l["tipo"]) for l in salva["lances"] if l["tipo"] in ("golpe", "erro")], salva


class TestSegundoAlvo(unittest.TestCase):
    def test_criterio_e_desempate(self):
        g = patrulheiro()
        cb, (a, b, c) = luta(g, (1.0, 0.6, 0.4))
        self.assertIs(segundo_alvo(cb, a), c)  # o mais ferido dos outros
        self.assertIs(segundo_alvo(cb, c), b)  # nunca o próprio alvo, havendo outro
        cb, (a, b, c) = luta(g, (1.0, 1.0, 1.0))
        self.assertIs(segundo_alvo(cb, b), a)  # empate: o primeiro na ordem da luta (o mais à esquerda)
        cb, (a, b, c) = luta(g, (0.5, 0.5, 0.5))
        b.max_hp *= 2  # mesma vida, máximo maior: a fração é menor, ele é o mais ferido
        self.assertIs(mais_ferido([a, b, c]), b)

    def test_sem_outro(self):
        g = patrulheiro()
        cb, (a,) = luta(g, (1.0,))
        self.assertIs(segundo_alvo(cb, a), a)  # sozinho: o mesmo alvo
        a.hp = 0
        self.assertIsNone(segundo_alvo(cb, a))  # ninguém de pé: o 2º não sai


class TestExecucao(unittest.TestCase):
    def test_um_em_cada(self):
        g = patrulheiro()
        cb, ins = luta(g, (1.0, 1.0, 0.7))
        foco, flechas = g.j.rec, g.j.flechas
        tiros, salva = disparar(g, cb, "Alfa")
        self.assertEqual(tiros, [("Alfa", "golpe"), ("Gama", "golpe")])
        self.assertEqual(salva["anim"], "rajada")
        self.assertEqual(ins[1].hp, ins[1].max_hp)  # Beta, mais inteiro, não leva nada
        self.assertEqual(foco - g.j.rec, custo_habilidade(g.j, "tiro_duplo"))
        self.assertEqual(flechas - g.j.flechas, 2)
        self.assertEqual(cb.flechas_gastas, 2)
        registro = [t for t in g.ui.ditos if t.startswith("[Tiro Duplo")]
        self.assertTrue(registro[0].startswith("[Tiro Duplo (1)] Você atinge Alfa"))
        self.assertTrue(registro[1].startswith("[Tiro Duplo (2)] Você atinge Gama"))

    def test_sozinho_dois_no_mesmo(self):
        g = patrulheiro()
        cb, _ = luta(g, (1.0,), familia="troll")
        tiros, _ = disparar(g, cb, "Alfa")
        self.assertEqual(tiros, [("Alfa", "golpe"), ("Alfa", "golpe")])

    def test_primeiro_cai_e_o_segundo_segue(self):
        g = patrulheiro()
        cb, (a, b) = luta(g, (0.01, 1.0))
        tiros, _ = disparar(g, cb, "Alfa")
        self.assertFalse(a.vivo)
        self.assertEqual(tiros, [("Alfa", "golpe"), ("Beta", "golpe")])
        self.assertLess(b.hp, b.max_hp)
        self.assertEqual(cb.mortos, [a])

    def test_dois_abates_sem_duplicar(self):
        g = patrulheiro()
        cb, (a, b, c) = luta(g, (0.01, 0.01, 1.0))
        tiros, _ = disparar(g, cb, "Alfa")
        self.assertEqual(tiros, [("Alfa", "golpe"), ("Beta", "golpe")])  # Beta é o mais ferido dos outros
        self.assertEqual(cb.mortos, [a, b])  # cada abate uma vez
        self.assertEqual(sum(1 for t in g.ui.ditos if t.startswith(("Alfa ", "Beta "))), 2)  # uma frase de queda cada

    def test_ultimo_cai_no_primeiro(self):
        g = patrulheiro()
        cb, (a,) = luta(g, (0.01,))
        flechas = g.j.flechas
        tiros, _ = disparar(g, cb, "Alfa")
        self.assertEqual(tiros, [("Alfa", "golpe")])  # o 2º não tem em quem: não sai
        self.assertEqual(flechas - g.j.flechas, 2)  # as duas flechas saem juntas, como antes
        self.assertEqual(cb._checar_fim(), "vitoria")

    def test_segundo_erra(self):
        g = patrulheiro()
        cb, (a, b) = luta(g, (1.0, 0.5))
        b.agi = 10 ** 3  # esquiva no teto
        erros = 0
        for s in range(40):
            a.hp, b.hp = a.max_hp, b.max_hp // 2
            g.rng.seed(s)
            g.j.rec, g.j.flechas = g.j.max_rec, 20
            tiros, _ = disparar(g, cb, "Alfa")
            self.assertEqual([n for n, _ in tiros], ["Alfa", "Beta"])
            erros += tiros[1][1] == "erro"
        self.assertGreater(erros, 0)  # o 2º pode errar, e o erro fica nele

    def test_marca_e_critico_no_alvo_de_cada_disparo(self):
        """A Marca de Beta vale só para o disparo que vai em Beta; o Tiro de Abertura, só para o primeiro."""
        danos = {}
        for marcado in (False, True):
            g = patrulheiro()
            cb, (a, b) = luta(g, (1.0, 0.9))
            if marcado:
                cb.aplicar(b, "marcado", 3, 0.25)
            g.rng.seed(7)
            disparar(g, cb, "Alfa")
            danos[marcado] = (a.max_hp - a.hp, int(b.max_hp * 0.9) - b.hp)
        self.assertEqual(danos[True][0], danos[False][0])
        self.assertAlmostEqual(danos[True][1] / danos[False][1], 1.25, delta=0.08)
        g = patrulheiro()
        cb, _ = luta(g, (1.0, 0.9))
        cb.abertura, cb.motivo_abertura = True, "Tiro de Abertura"
        _, salva = disparar(g, cb, "Alfa")
        golpes = [l for l in salva["lances"] if l["tipo"] == "golpe"]
        self.assertEqual((golpes[0]["crit"], golpes[0]["crit_motivo"]), (True, "Tiro de Abertura"))
        self.assertNotEqual(golpes[1].get("crit_motivo"), "Tiro de Abertura")


class TestDescricao(unittest.TestCase):
    def test_grimorio_desc_e_previa(self):
        g = patrulheiro()
        linhas = HABILIDADES["tiro_duplo"]["linhas"](g.j)
        self.assertEqual([l["tipo"] for l in linhas], ["dano", "efeito"])
        self.assertEqual(linhas[0]["rotulo"], "Cada um dos 2 disparos")
        self.assertEqual(linhas[1]["texto"], SEGUNDO_ALVO)
        self.assertIn("o 2º em outro inimigo (o mais ferido)", descricao_habilidade("tiro_duplo", g.j))
        g = Jogo(Roteiro(), seed=5, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "arqueiro", "turvo")
        dev.subir_ate(g, 4, spec=False)
        x = next(h for h in especializacao.previa(g.j, "patrulheiro")["habilidades"] if h["id"] == "tiro_duplo")
        self.assertIn("mais ferido", x["desc"])
        self.assertTrue(any(l.get("texto") == SEGUNDO_ALVO for l in x["linhas"]))


if __name__ == "__main__":
    unittest.main()
