"""A conferência da integração do Lich Menor (1.199.0), com o código real do jogo: o cenário "tutorial" dos testes de
navegador (CHEFE=lich_menor, GRUPO=esqueleto:1, CLASSE=mago), com uma troca só desta conferência: quando a luta começa, o
herói usa o Erguer Servo (habilidades._erguer_servo), o Lich usa o Invocar (inimigos._invocar, um esqueleto da família) e,
com FASE=2, a vida dele cai abaixo do limiar e a fase entra pelo caminho do jogo (Combate.checar_fase: o traço etéreo e
o texto). Nada do jogo muda.
    PYTHONPATH=<raiz> CHEFE=lich_menor GRUPO=esqueleto:1 CLASSE=mago [FASE=2] python cenario_jogo_lich.py tutorial
"""
import os

from tests.navegador import cenarios

from rpg import comitiva
from rpg.habilidades import _erguer_servo
from rpg.inimigos import _invocar

_preparar = comitiva.preparar_combate


def com_o_lich(cb):
    _preparar(cb)
    _erguer_servo(cb, cb.j, None)
    lich = next(e for e in cb.inimigos if getattr(e, "guardiao", None) == "lich_menor")
    _invocar(cb, lich, None)
    if os.environ.get("FASE") == "2":
        lich.hp = int(lich.max_hp * 0.4)
        cb.checar_fase(lich)


comitiva.preparar_combate = com_o_lich

if __name__ == "__main__":
    cenarios.main()
