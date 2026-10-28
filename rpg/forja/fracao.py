"""A casa decimal que o reforço traz (27, seção 1.2): a peça reforçada pode ter Ataque 4,5 ou Vida por turno 2,6.

- Ataque, Poder, Defesa e Agilidade do herói e dos companheiros levam a fração das peças (entidades.Jogador.recalcular,
  comitiva.grupo.atributos); a luta usa o número com a casa (dano, defesa, esquiva). Sem peça fracionária, o número é
  exatamente o de antes.
- Espinhos, Vida por turno e Vida por abate são pontos de vida (inteiros): a fração se acumula a cada disparo, na
  pessoa (2,6 por turno cura 2, 3, 3, 2, 3…, em média 2,6). A vez de cada um (tique) separa um disparo do outro: a
  cura por turno e por abate é consultada duas vezes no mesmo disparo (se há, quanto) e dá o mesmo número nas duas.
"""

from ..modificadores import mod
from .regras import limpo

FRACIONADOS = ("espinhos", "regen_vida", "vida_abate")


def fracao(v):
    """A parte decimal de um valor das peças (uma casa), ou 0."""
    return round(v - int(v), 1) if v > 0 else 0


def com_fracao(inteiro_jogo, total, parte):
    """O número do jogo (inteiro, pela regra dele) mais a fração que só o equipamento reforçado traz; sem fração,
    exatamente o de antes."""
    return limpo(inteiro_jogo(total - parte) + parte) if parte else inteiro_jogo(total)


def nas_pecas(equip, stat):
    """A fração de um atributo somado nas peças vestidas."""
    return fracao(sum(it["bonus"].get(stat, 0) for it in equip.values() if it))


def mod_pontos(u, chave):
    """O mod de uma chave de pontos de vida (FRACIONADOS) em inteiros, com a fração guardada na pessoa para o próximo
    disparo. Um valor inteiro passa como está."""
    v = mod(u, chave)
    if chave not in FRACIONADOS or not v or float(v).is_integer():
        return v
    conta = u.__dict__.setdefault("_fracao", {})
    vez = None if chave == "espinhos" else getattr(u, "_tique", 0)  # os espinhos, uma vez por golpe
    e = conta.get(chave)
    if e and vez is not None and e[0] == vez:
        return e[1]
    resto = (e[2] if e else 0.0) + v
    inteiro = int(resto + 1e-9)
    conta[chave] = (vez, inteiro, resto - inteiro)
    return inteiro


def tique(u):
    """A vez de `u` começou (ou ele derrubou alguém): um disparo novo de cura por turno ou por abate."""
    if u is not None:
        u._tique = getattr(u, "_tique", 0) + 1
