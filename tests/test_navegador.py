"""Teste de fumaça no navegador (tests/navegador/fumaca.mjs). Pulado se não houver Node + Playwright."""

import os
import shutil
import subprocess
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def modulo_playwright():
    if os.environ.get("PLAYWRIGHT_MODULO"):
        return os.environ["PLAYWRIGHT_MODULO"]
    npm = shutil.which("npm")
    if not npm:
        return None
    try:
        raiz = subprocess.run([npm, "root", "-g"], capture_output=True, text=True, timeout=30).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    caminho = os.path.join(raiz, "playwright", "index.mjs")
    return caminho if os.path.exists(caminho) else None


class TestNavegador(unittest.TestCase):
    def test_fumaca_da_interface_web(self):
        node, modulo = shutil.which("node"), modulo_playwright()
        if not node or not modulo:
            self.skipTest("precisa de node e do pacote playwright (npm i -g playwright)")
        r = subprocess.run([node, os.path.join(RAIZ, "tests", "navegador", "fumaca.mjs")], cwd=RAIZ,
                           env={**os.environ, "PLAYWRIGHT_MODULO": modulo}, capture_output=True, text=True,
                           timeout=600)
        if r.returncode == 77:
            self.skipTest(r.stdout.strip().splitlines()[-1])
        self.assertEqual(r.returncode, 0, r.stdout[-3000:] + r.stderr[-2000:])
