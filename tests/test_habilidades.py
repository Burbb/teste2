"""O catálogo de habilidades se mantém coerente: tudo o que a luta faz, o Grimório descreve, e vice-versa."""

import random
import tempfile
import unittest

from rpg import habilidades as H
from rpg.classes import CLASSES, SPECS, habilidades_ate
from rpg.combate import NOMES_EFEITOS
from rpg.jogo import Jogo
from rpg.ui import BotUI


def _blocos(passos):
    for p in passos:
        yield p
        yield from _blocos(getattr(p, "depois", []))
        yield from _blocos(getattr(p, "passos", []))


def _heroi(spec):
    classe = SPECS[spec]["classe"]
    g = Jogo(BotUI(random.Random(1)), seed=3, pasta_saves=tempfile.mkdtemp())
    g.iniciar("Teste", classe)
    g.j.nivel, g.j.spec = 8, spec
    g.j.habilidades = habilidades_ate(classe, spec, 8)
    g.j.recalcular()
    return g.j


class TestCatalogo(unittest.TestCase):
    def test_toda_habilidade_tem_execucao_e_descricao(self):
        for h_id, h in H.HABILIDADES.items():
            for chave in ("nome", "custo", "alvo", "desc", "fn", "linhas"):
                self.assertIn(chave, h, f"{h_id} sem {chave}")
            self.assertTrue(callable(h["fn"]) and callable(h["linhas"]), h_id)
            self.assertIn(h["alvo"], H_ALVOS, h_id)

    def test_toda_habilidade_das_classes_existe(self):
        for c in list(CLASSES.values()) + list(SPECS.values()):
            for _, h_id in c["habilidades"]:
                self.assertIn(h_id, H.HABILIDADES)

    def test_estados_aplicados_existem(self):
        """Um Aplicar/Buff com um estado que o combate não conhece seria um efeito fantasma."""
        for h_id, h in H.HABILIDADES.items():
            for b in _blocos(h.get("passos", [])):
                if isinstance(b, (H.Aplicar, H.Buff)):
                    self.assertIn(b.efeito, NOMES_EFEITOS, f"{h_id}: estado {b.efeito}")

    def test_grimorio_mostra_cada_golpe(self):
        """Cada bloco de Dano visível vira uma linha de dano no Grimório, com o mesmo multiplicador."""
        for spec in SPECS:
            j = _heroi(spec)
            for h_id in j.habilidades:
                h = H.HABILIDADES[h_id]
                if "passos" not in h:
                    continue
                visiveis = []

                def coletar(passos):
                    for p in passos:
                        if isinstance(p, H.Dano):
                            if p.em != "outro" or p.grimorio:  # o 2º disparo do Tiro Duplo repete os números do
                                visiveis.append(p)              # 1º: o Grimório diz só para onde ele vai
                            coletar(p.depois)
                        elif isinstance(p, H.Se) and p.mostrar or isinstance(p, H.Salva):
                            coletar(p.passos)
                coletar(h["passos"])
                linhas = [x for x in h["linhas"](j) if x["tipo"] == "dano"]
                self.assertEqual(len(linhas), len(visiveis), h_id)
                for bloco, linha in zip(visiveis, linhas):
                    self.assertIn(f"× {bloco.mult * 100:.0f}%", linha["formula"], h_id)


H_ALVOS = ("inimigo", "todos", "proprio", "aliado", "aliados")


if __name__ == "__main__":
    unittest.main()
