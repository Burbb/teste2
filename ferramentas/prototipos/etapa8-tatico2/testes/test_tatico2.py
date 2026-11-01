"""O protótipo tático por turnos (Tático 2): isolamento do jogo e os testes das regras e da IA (Node).

    python -m unittest discover -s ferramentas/prototipos/etapa8-tatico2/testes -t ferramentas/prototipos/etapa8-tatico2

As regras são JavaScript (rodam no navegador); os testes estão em regras.test.mjs e rodam com `node --test`. Sem o
Node no PATH, só o isolamento é conferido."""
import pathlib
import shutil
import subprocess
import unittest

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[3]


class Isolamento(unittest.TestCase):
    def test_o_jogo_nao_carrega_nada_do_prototipo(self):
        for arq in (RAIZ / "rpg").rglob("*"):
            if arq.suffix in (".py", ".js", ".html", ".css"):
                self.assertNotIn("etapa8-tatico2", arq.read_text(encoding="utf-8", errors="ignore"), arq)

    def test_o_servidor_le_a_versao(self):
        texto = (AQUI.parent / "tela" / "conteudo.js").read_text(encoding="utf-8")
        self.assertIn('export const VERSAO = "Tático', texto)


@unittest.skipUnless(shutil.which("node"), "sem o Node no PATH")
class Regras(unittest.TestCase):
    def test_os_testes_das_regras_passam(self):
        r = subprocess.run(["node", "--test", str(AQUI / "regras.test.mjs")], capture_output=True, text=True,
                           encoding="utf-8", timeout=600)
        self.assertEqual(r.returncode, 0, r.stdout[-4000:] + r.stderr[-2000:])


if __name__ == "__main__":
    unittest.main()
