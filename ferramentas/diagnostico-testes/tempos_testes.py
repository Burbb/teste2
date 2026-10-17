"""Diagnóstico: roda a suíte como o CLAUDE.md (unittest discover -s tests) e mede cada teste e os intervalos entre eles (onde caem
setUpClass/setUpModule e a importação). Grava <saida>.tsv (um teste por linha) e imprime o resumo.

    python tempos_testes.py <saida-sem-extensão>
"""
import os
import sys
import time
import unittest

sys.path.insert(0, os.getcwd())   # como o python -m unittest, que põe o diretório atual no caminho

saida = sys.argv[1]
linhas, estado = [], {"fim": time.perf_counter(), "ini": None}


class Resultado(unittest.TextTestResult):
    def startTest(self, test):
        agora = time.perf_counter()
        estado["gap"] = agora - estado["fim"]
        estado["ini"] = agora
        super().startTest(test)

    def stopTest(self, test):
        super().stopTest(test)
        fim = time.perf_counter()
        linhas.append((test.id(), fim - estado["ini"], estado["gap"]))
        estado["fim"] = fim


t0 = time.perf_counter()
suite = unittest.defaultTestLoader.discover("tests")
t_desc = time.perf_counter() - t0
estado["fim"] = time.perf_counter()
r = unittest.TextTestRunner(resultclass=Resultado, verbosity=0, stream=open(os.devnull, "w")).run(suite)
total = time.perf_counter() - t0
with open(saida + ".tsv", "w", encoding="utf-8") as f:
    f.write("teste\tsegundos\tintervalo_antes\n")
    for nome, s, g in linhas:
        f.write(f"{nome}\t{s:.3f}\t{g:.3f}\n")
modulos = {}
for nome, s, g in linhas:
    m = nome.split(".")[0]
    modulos[m] = modulos.get(m, 0) + s + g
print(f"python {sys.version.split()[0]} | {r.testsRun} testes | falhas {len(r.failures)} erros {len(r.errors)} "
      f"pulados {len(r.skipped)} | descoberta {t_desc:.1f}s | total {total:.1f}s")
print("por módulo (testes + intervalos):")
for m, s in sorted(modulos.items(), key=lambda x: -x[1])[:15]:
    print(f"  {s:8.1f}s  {m}")
print("os testes mais lentos:")
for nome, s, g in sorted(linhas, key=lambda x: -x[1])[:25]:
    print(f"  {s:8.1f}s  {nome}")
print("os maiores intervalos (preparação de classe/módulo):")
for nome, s, g in sorted(linhas, key=lambda x: -x[2])[:10]:
    print(f"  {g:8.1f}s  antes de {nome}")
