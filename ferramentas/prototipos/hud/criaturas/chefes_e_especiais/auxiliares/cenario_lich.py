"""O cenário "tutorial" dos testes de navegador (CHEFE=lich_menor, GRUPO=esqueleto:1, CLASSE=mago), com uma troca só do
protótipo, para comparar o Lich ao lado do Esqueleto inimigo e do servo aliado: quando a luta começa, o herói usa o
Erguer Servo de verdade (habilidades._erguer_servo), e o servo entra com o retrato que o jogo dá a ele desde a 1.196.0.
Nada do jogo muda.
    PYTHONPATH=<raiz> CHEFE=lich_menor GRUPO=esqueleto:1 CLASSE=mago python cenario_lich.py tutorial
"""
from tests.navegador import cenarios

from rpg import comitiva
from rpg.habilidades import _erguer_servo

_preparar = comitiva.preparar_combate


def com_o_servo(cb):
    _preparar(cb)
    _erguer_servo(cb, cb.j, None)


comitiva.preparar_combate = com_o_servo

if __name__ == "__main__":
    cenarios.main()
