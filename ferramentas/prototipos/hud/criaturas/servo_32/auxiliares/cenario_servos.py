"""O cenário "tutorial" dos testes de navegador (LUTA= e QUANTOS=), com uma troca só do protótipo para demonstrar a seleção
que o retrato do servo vai pedir: os dois servos de pé quando a luta começa, pelo mesmo invocar_aliado do jogo e com o
mesmo tipo "servo". O "Esqueleto (Invocado)" é o do Erguer Servo (habilidades.py); o "Lobo (servo)" é como o talento Rei
dos Mortos ergue o primeiro inimigo que cai (talentos.py: o nome dele com "(servo)", 40% da vida, metade do ataque). Nada
do jogo muda.
    PYTHONPATH=<raiz> LUTA=esqueleto QUANTOS=1 python cenario_servos.py tutorial
"""
from tests.navegador import cenarios

from rpg import comitiva

_preparar = comitiva.preparar_combate


def com_os_dois_servos(cb):
    _preparar(cb)
    cb.invocar_aliado("Esqueleto (Invocado)", hp=60, atk=8, tipo="servo")  # o Erguer Servo
    cb.invocar_aliado("Lobo (servo)", hp=24, atk=5)  # o Rei dos Mortos (o tipo padrão também é "servo")


comitiva.preparar_combate = com_os_dois_servos

if __name__ == "__main__":
    cenarios.main()
