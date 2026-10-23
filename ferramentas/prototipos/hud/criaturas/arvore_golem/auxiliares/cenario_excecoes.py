"""O cenário "relatorio" dos testes de navegador (o Explorar cai no EVENTO), com duas trocas só do protótipo, para
fotografar as exceções da 1.189.0 com o código real dos eventos: o herói no nível 5 (o Mímico só aparece do 2 em diante)
e a sorte do evento sempre a favor (a chance de 12% do baú abrir o Mímico; a de 50% do espantalho acordar quando se
examina). Nada do jogo muda.
    PYTHONPATH=<raiz> EVENTO=espantalho|bau_abandonado python cenario_excecoes.py relatorio
"""
import os

from tests.navegador import cenarios

from rpg.jogo import Jogo

_chance, _iniciar = Jogo.chance, Jogo.iniciar
SORTE = {"bau_abandonado": 0.12, "espantalho": 0.5}  # a chance do evento que leva à luta


def chance(self, p):
    return True if SORTE.get(os.environ.get("EVENTO")) == p else _chance(self, p)


def iniciar(self, *a, **k):
    r = _iniciar(self, *a, **k)
    self.j.nivel = max(self.j.nivel, 5)
    return r


Jogo.chance, Jogo.iniciar = chance, iniciar

if __name__ == "__main__":
    cenarios.main()
