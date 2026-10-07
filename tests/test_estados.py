"""O catálogo de estados cobre tudo o que o jogo aplica, e a tela tem desenho para cada ícone."""

import os
import re
import unittest

from rpg.estados import ESTADOS, NEGATIVOS, NOMES, descrever_aplicar, para_tela

RAIZ = os.path.join(os.path.dirname(__file__), "..")


def _codigo_python():
    for pasta, _, arquivos in os.walk(os.path.join(RAIZ, "rpg")):
        for a in arquivos:
            if a.endswith(".py"):
                with open(os.path.join(pasta, a), encoding="utf-8") as f:
                    yield a, f.read()


class TestEstados(unittest.TestCase):
    def test_todo_estado_usado_esta_no_catalogo(self):
        """aplicar("x"), Aplicar("x"), Buff("x") e efeito("x") em qualquer arquivo: x precisa existir aqui."""
        padrao = re.compile(r'(?:\.aplicar\(\s*[\w.]+,\s*|aplicar\(|Aplicar\(|Buff\(|\.efeito\()"([a-z_]+)"')
        usados = {}
        for nome, codigo in _codigo_python():
            for m in padrao.finditer(codigo):
                usados.setdefault(m.group(1), nome)
        self.assertTrue(usados)
        for est, onde in usados.items():
            self.assertIn(est, ESTADOS, f"estado '{est}' (em {onde}) não está em estados.py")

    def test_campos_coerentes(self):
        for k, e in ESTADOS.items():
            self.assertTrue(e["nome"] and e["icone"] and e["familia"], k)
            if e["tique"]:
                self.assertEqual(len(e["tique"]), 2, k)
            if e["camadas"]:
                self.assertIn("{s}", e["rotulo_camadas"], k)
        self.assertIn("veneno", NEGATIVOS)
        self.assertNotIn("guarda", NEGATIVOS)
        self.assertEqual(NOMES["queimadura"], "em chamas")

    def test_tela_tem_desenho_para_cada_icone(self):
        with open(os.path.join(RAIZ, "rpg", "web", "static", "sprites-dados.js"), encoding="utf-8") as f:
            sprites = f.read()
        for k, e in para_tela().items():
            self.assertRegex(sprites, rf"\b{e['icone']}\s*[:=]", f"{k}: ícone '{e['icone']}' sem desenho")

    def test_descricao_do_grimorio(self):
        self.assertEqual(descrever_aplicar("atordoado", 1, 0, "", 0.45, False, None),
                         "45% de chance de atordoar o alvo por 1 turno.")
        self.assertIn("congelar", descrever_aplicar("atordoado", 1, 0, "", 0.35, False, "congelado"))
        self.assertTrue(descrever_aplicar("sangramento", 3, 2.7, "Ataque × 30%", 1.0, False, None).startswith("Sangramento"))


if __name__ == "__main__":
    unittest.main()
