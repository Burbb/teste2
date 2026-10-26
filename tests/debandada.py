"""A frequência da debandada (roadmapIDEIAS/26, "Ajustes da 1.212.0"): as mesmas lutas comuns com saída, as mesmas
sementes e o mesmo robô da arena, com a regra de agora ou com a da 1.211.0 (reconstruída aqui: avaliada depois de cada
vez, 25% da vida, sem as outras condições).

    python -m tests.debandada            # a regra de agora
    python -m tests.debandada antes      # a da 1.211.0
"""
import copy
import sys
from rpg.combate import Combate
from rpg.classes import SPECS
from rpg import texto as tx
from tests import equilibrio as eq

ANTIGA = len(sys.argv) > 1 and sys.argv[1] == "antes"


def debandada_antiga(self):
    vivos = self.inimigos_vivos()
    if len(self.inimigos) < 2 or not self.pode_fugir or not self.mortos or self.cena_propria:
        return False
    if any(e.chefe or e.carregando or e.invoca or getattr(e, "piso", None) is not None for e in vivos):
        return False
    if sum(e.hp for e in vivos) > self.vida_inicial * 0.25:
        return False
    for e in vivos:
        e.fugiu = True
        e.debandou = True
        self.lance("fuga", de=self.uid(e))
    quem = tx.maiuscula(tx.lista_natural([self.nome(e) for e in vivos]))
    self.dizer(f"{quem} fogem.", "verde")
    return True


if ANTIGA:
    checar = Combate._checar_fim

    def checar_fim(self):
        r = checar(self)
        if r:
            return r
        return "vitoria" if debandada_antiga(self) else None
    Combate._checar_fim = checar_fim
    Combate._debandada = lambda self: False

lutas = grupos2 = deband = 0
casos = []
for spec in SPECS:
    classe = SPECS[spec]["classe"]
    for nivel in (2, 4, 6, 8):
        semente = 7919 * nivel + list(SPECS).index(spec)
        g = eq.heroi(classe, spec, nivel, semente)
        g.nivel_local = lambda n=max(1, nivel - 1): n
        lugares = eq.regioes(g)
        salvo = g.j, g.comitiva, g.bestiario
        for k in range(10):
            g.j, g.comitiva, g.bestiario = copy.deepcopy(salvo[0]), copy.deepcopy(salvo[1]), copy.deepcopy(salvo[2])
            g.clima, g.periodo = "limpo", 1
            g.mundo["atual"] = lugares[k % len(lugares)]["id"]
            g.rng.seed(semente + k)
            g.ui.rng.seed(semente + k + 1)
            g.ganhar_xp = lambda *a, **kw: None
            g.ganhar_ouro = lambda *a, **kw: None
            g.saque_de_combate = lambda *a, **kw: None
            inimigos = g.grupo()
            cb = Combate(g, inimigos, None, pode_fugir=True)
            r = cb.executar()
            lutas += 1
            if len(inimigos) >= 2:
                grupos2 += 1
            if any(getattr(e, "debandou", False) for e in inimigos):
                deband += 1
                casos.append((spec, nivel, cb.turno, [(e.nome, e.hp) for e in inimigos if getattr(e, "debandou", False)]))
print(f"{'ANTES' if ANTIGA else 'DEPOIS'}: {lutas} lutas, {grupos2} com 2+ inimigos, debandada em {deband} "
      f"({100 * deband / max(1, grupos2):.0f}% das de grupo)")
for c in casos[:8]:
    print("  ", c)
