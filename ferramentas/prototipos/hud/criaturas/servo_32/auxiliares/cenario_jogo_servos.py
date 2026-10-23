"""A conferência da integração do servo (1.196.0), com o código real do jogo: o cenário "tutorial" dos testes de navegador
(GRUPO=esqueleto:1,lobo:1, CLASSE=mago), com uma troca só desta conferência: quando a luta começa, o herói aprende o talento
Rei dos Mortos, usa o Erguer Servo de verdade (habilidades._erguer_servo) e o lobo cai pelo caminho real da morte
(Combate.ao_morrer, que dispara o talento). Assim ficam lado a lado o esqueleto inimigo, o "Esqueleto (Invocado)" com o
crânio nu e o lobo erguido com o retrato do lobo, cada um pelo retrato que o motor escolheu. Nada do jogo muda.
    PYTHONPATH=<raiz> GRUPO=esqueleto:1,lobo:1 CLASSE=mago python cenario_jogo_servos.py tutorial
"""
from tests.navegador import cenarios

from rpg import comitiva, talentos
from rpg.habilidades import _erguer_servo

_preparar = comitiva.preparar_combate


def com_os_servos(cb):
    _preparar(cb)
    if not cb.j.tal("senhor_mortos"):
        talentos.aprender(cb.j, next(t for t in talentos.TALENTOS["mago"] if t["id"] == "senhor_mortos"))
    _erguer_servo(cb, cb.j, None)
    lobo = next(e for e in cb.inimigos if e.familia == "lobo")
    lobo.hp = 0
    cb.ao_morrer(lobo, por=cb.j)


comitiva.preparar_combate = com_os_servos

if __name__ == "__main__":
    cenarios.main()
