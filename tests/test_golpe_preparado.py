"""O golpe preparado na capela (E5, P1): um dos esqueletos do ossuário e um dos afogados do sarilho preparam o Golpe
Esmagador que o troll e o mercenário já têm. A variante abre a luta preparando (uma vez), avisa, atordoar interrompe,
a guarda reduz; a ficha diz isso. O resto do jogo (as mesmas espécies no mundo gerado, a guardiã) fica como era."""

import tempfile
import unittest

from rpg import missoes
from rpg.combate import Combate
from rpg.dados import FAMILIAS
from rpg.jogo import Jogo
from rpg.web.estado import estado
from tests.test_missoes import MID, Roteiro, fazer, na_capela

SALAS = (("ossuario", missoes.grupo_ossuario, "esqueleto", "Esqueleto de Guarda"),
         ("sarilho", missoes.grupo_sarilho, "afogado", "Afogado Inchado"))


def luta(g, grupo):
    cb = Combate(g, grupo, None, pode_fugir=False, titulo="Teste")
    cb.turno = 1
    return cb


class TestVariantes(unittest.TestCase):
    def test_grupo_da_sala(self):
        for sala, fn, familia, nome in SALAS:
            g = na_capela(etapa="ossuario")
            grupo = fn(g)
            self.assertEqual([e.familia for e in grupo], [familia, familia], sala)  # dois, como antes
            guarda, outro = grupo
            self.assertTrue(guarda.nome.startswith(nome))
            self.assertIn("esmagar", guarda.habilidades)
            self.assertEqual((guarda.abre_com, guarda.nota), ("esmagar", missoes.GOLPE_PREPARADO))
            self.assertNotIn("esmagar", outro.habilidades)
            self.assertIsNone(getattr(outro, "nota", None))
            self.assertEqual(FAMILIAS[familia]["habs"], {"esqueleto": ["investida"],
                                                          "afogado": ["agarrar", "drenar"]}[familia])

    def test_sorteio_igual_ao_de_antes(self):
        """A variante só muda o que a luta faz: os inimigos sorteados (nível, vida, afixo) e o sorteio seguinte são
        os mesmos de g.grupo."""
        for _, fn, familia, _ in SALAS:
            g = na_capela(etapa="ossuario")
            g.rng.seed(42)
            antes = [(e.nivel, e.max_hp, e.afixo) for e in g.grupo(familia, n=2)] + [g.rng.random()]
            g.rng.seed(42)
            depois = [(e.nivel, e.max_hp, e.afixo) for e in fn(g)] + [g.rng.random()]
            self.assertEqual(antes, depois)

    def test_mundo_gerado_sem_variante(self):
        g = Jogo(Roteiro(), seed=5, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        for familia in ("esqueleto", "afogado"):
            for e in g.grupo(familia, n=2):
                self.assertNotIn("esmagar", e.habilidades)
                self.assertIsNone(getattr(e, "abre_com", None))
                self.assertIsNone(getattr(e, "nota", None))


class TestNaLuta(unittest.TestCase):
    def test_abre_preparando_e_atordoar_interrompe(self):
        for _, fn, _, _ in SALAS:
            g = na_capela(etapa="ossuario")
            guarda, outro = fn(g)
            cb = luta(g, [guarda, outro])
            cb.agir_inimigo(guarda)  # a primeira ação: prepara, sem sorteio
            self.assertTrue(guarda.carregando)
            self.assertIsNone(guarda.abre_com)  # uma vez só
            self.assertTrue(estado(g)["combate"]["inimigos"][0]["preparando"])  # a carta mostra o aviso
            vida = g.j.hp
            cb.aplicar(guarda, "atordoado", 1)
            cb.fase_inimigos(apenas=guarda)
            self.assertIsNone(guarda.carregando)  # perdeu o golpe que preparava
            self.assertEqual(g.j.hp, vida)
            self.assertIn("Atordoado, Esqueleto de Guarda perde o golpe que preparava!" if guarda.familia == "esqueleto"
                          else "Atordoado, Afogado Inchado perde o golpe que preparava!", g.ui.ditos)
            g.combate_ativo = None

    def test_guarda_reduz_o_golpe(self):
        perdas = {}
        for guarda_ativa in (False, True):
            g = na_capela(etapa="ossuario")
            g.j.max_hp = g.j.hp = 1000  # para o golpe não matar nem passar pelo juízo de "a um golpe da morte"
            guarda, outro = missoes.grupo_ossuario(g)
            guarda.agi = 0  # sem esquiva: a comparação é só da guarda
            g.j.agi = 0
            cb = luta(g, [guarda, outro])
            cb.agir_inimigo(guarda)
            if guarda_ativa:
                g.j.aplicar("guarda", 2, 0.5)
            g.rng.seed(3)
            cb.agir_inimigo(guarda)  # o golpe sai
            self.assertIsNone(guarda.carregando)
            perdas[guarda_ativa] = 1000 - g.j.hp
            g.combate_ativo = None
        self.assertGreater(perdas[False], 0)
        self.assertLessEqual(perdas[True], perdas[False] * 0.55)

    def test_a_um_golpe_da_morte_espera(self):
        """Como as outras habilidades que não ferem: com você a um golpe da morte, ela bate em vez de preparar, e
        prepara quando fizer sentido."""
        g = na_capela(etapa="ossuario")
        guarda, outro = missoes.grupo_ossuario(g)
        cb = luta(g, [guarda, outro])
        g.j.hp = 1
        cb.agir_inimigo(guarda)
        self.assertIsNone(guarda.carregando)
        self.assertEqual(guarda.abre_com, "esmagar")
        g.j.hp = g.j.max_hp
        cb.agir_inimigo(guarda)
        self.assertTrue(guarda.carregando)
        g.combate_ativo = None


class TestFicha(unittest.TestCase):
    def test_ficha_e_analisar_dizem_o_golpe(self):
        g = na_capela(etapa="ossuario")
        guarda, outro = missoes.grupo_ossuario(g)
        cb = luta(g, [guarda, outro])
        fichas = [e["ficha"] for e in estado(g)["combate"]["inimigos"]]
        self.assertEqual(fichas[0]["nota"], missoes.GOLPE_PREPARADO)
        self.assertNotIn("nota", fichas[1])
        cb.analisar()
        self.assertIn(f"  ⚠ {missoes.GOLPE_PREPARADO}", g.ui.ditos)
        g.combate_ativo = None

    def test_ficha_do_mundo_gerado_sem_nota(self):
        g = Jogo(Roteiro(), seed=5, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        luta(g, g.grupo("esqueleto", n=2))
        self.assertTrue(all("nota" not in e["ficha"] for e in estado(g)["combate"]["inimigos"]))
        g.combate_ativo = None


class TestMissao(unittest.TestCase):
    def test_as_salas_usam_a_variante_e_a_missao_segue(self):
        g = na_capela(etapa="ossuario")
        g.ui.efeitos = []
        g.ui.efeito = lambda texto, tipo=None: g.ui.efeitos.append(texto)
        vistas = []

        def combate(grupo, emboscada=None, pode_fugir=True, titulo=None, sozinho=False):
            vistas.append((titulo, [e.nome for e in grupo], pode_fugir))
            return "vitoria"
        g.combate = combate
        self.assertTrue(fazer(g, "ossuario"))
        self.assertTrue(fazer(g, "correntes"))  # à mão: a onda de afogados
        self.assertEqual([(t, n[0], len(n), f) for t, n, f in vistas],
                         [("O Ossuário", "Esqueleto de Guarda", 2, True), ("O Sarilho", "Afogado Inchado", 2, True)])
        m = missoes.registro(g, MID)
        self.assertEqual((m["etapa"], m["preparos"]), ("fundo", ["corpo_solto"]))
        self.assertFalse([t for t in g.ui.efeitos if "Protótipo" in t])  # o aviso antigo do fundo saiu


if __name__ == "__main__":
    unittest.main()
