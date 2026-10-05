"""Motor de eventos: registro, condições, pesos dinâmicos e anti-repetição.

Cada evento declara em quais contextos pode ocorrer ("explorar", "viagem",
"acampamento", "vila"), um peso (fixo ou calculado a partir do estado do
jogo), uma condição opcional e um tempo de recarga. Na hora de sortear:

* eventos vistos recentemente ou muitas vezes perdem peso (novidade primeiro);
* rumores e contratos podem multiplicar o peso de eventos específicos;
* classe, especialização, bioma, clima, período do dia, reputação, corrupção
  e "sementes" plantadas por escolhas antigas habilitam eventos diferentes.
"""

REGISTRO = []


class Evento:
    def __init__(self, fn, id, contextos, peso, cond, cooldown, unico, max_vezes):
        self.fn = fn
        self.id = id
        self.contextos = contextos
        self.peso = peso
        self.cond = cond
        self.cooldown = cooldown
        self.unico = unico
        self.max_vezes = max_vezes


def evento(contextos=("explorar", "viagem"), peso=10, cond=None, cooldown=6, unico=False, max_vezes=None, id=None):
    def deco(fn):
        REGISTRO.append(Evento(fn, id or fn.__name__, tuple(contextos), peso, cond, cooldown, unico, max_vezes))
        return fn
    return deco


def candidatos(g, contexto):
    lista = []
    for ev in REGISTRO:
        if contexto not in ev.contextos:
            continue
        vezes = g.contagem.get(ev.id, 0)
        if ev.unico and vezes:
            continue
        if ev.max_vezes and vezes >= ev.max_vezes:
            continue
        ultimo = g.historico.get(ev.id)
        if ultimo is not None and g.passos - ultimo < ev.cooldown:
            continue
        if ev.cond and not ev.cond(g):
            continue
        peso = ev.peso(g) if callable(ev.peso) else ev.peso
        if peso <= 0:
            continue
        if ultimo is not None and g.passos - ultimo < ev.cooldown + 8:
            peso *= 0.5
        peso /= 1 + 0.25 * vezes
        peso *= g.impulsos.get(ev.id, 1)
        lista.append((ev, peso))
    return lista


def disparar(g, contexto):
    """Sorteia e executa um evento. Devolve o id do evento ou None."""
    forcado = g.evento_forcado(contexto)
    if forcado:
        ev = next(e for e in REGISTRO if e.id == forcado)
    else:
        lista = candidatos(g, contexto)
        if not lista:
            return None
        ev = g.rng.choices([e for e, _ in lista], weights=[p for _, p in lista])[0]
    g.historico[ev.id] = g.passos
    g.contagem[ev.id] = g.contagem.get(ev.id, 0) + 1
    g.estatisticas["eventos"] = g.estatisticas.get("eventos", 0) + 1
    from ..telemetria import registrar
    from .titulos import titulo
    registrar(g, "evento", id=ev.id, contexto=contexto)
    g.ui.cena(titulo(ev.id), g.contexto_cena(), tipo="evento")
    ev.fn(g)
    return ev.id
