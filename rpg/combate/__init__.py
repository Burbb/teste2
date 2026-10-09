"""Combate por turnos, em partes:

    luta.py      quem está na luta, o laço dos turnos, os lances para a tela e o fim
    golpe.py     a conta de um golpe, os estados que ele deixa e as mortes
    heroi.py     a vez do herói (atacar, habilidades, itens, analisar, fugir)
    turnos.py    a vez da comitiva, do animal, dos servos e dos inimigos
    eficacia.py  quanto um golpe rende contra os traços do alvo

`Combate` junta as partes (como o Jogo junta os sistemas). Quem usa importa daqui: `from rpg.combate import Combate`.
"""

from ..estados import NOMES as NOMES_EFEITOS  # o catálogo de estados mora em estados.py
from .eficacia import FRACO, NOMES_TIPO_DANO, RESISTE, TIPOS_DANO, eficacias, mult_tracos
from .heroi import USAVEIS_EM_COMBATE
from .luta import Aliado, Combate, _SERIE

__all__ = ["Aliado", "Combate", "FRACO", "NOMES_EFEITOS", "NOMES_TIPO_DANO", "RESISTE", "TIPOS_DANO",
           "USAVEIS_EM_COMBATE", "eficacias", "mult_tracos", "_SERIE"]
