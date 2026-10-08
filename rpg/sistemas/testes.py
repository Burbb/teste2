"""Testes de atributo: d20 + bônus contra a dificuldade."""

import math
from ..classes import CLASSES, SPECS
from ..regras import NOMES_TESTE


class Testes:
    # ================================================================ testes
    @staticmethod
    def _bonus_atributo(valor):
        """Atributos ajudam nos testes, mas com retorno decrescente: 5 → +2, 11 → +4, 20 → +6, 43 → +8."""
        return int(round(2.5 * math.log2(1 + max(0, valor) / 5)))

    def partes_teste(self, attr):
        """De onde vem o bônus de cada teste: [(rótulo, valor), ...]."""
        j = self.j
        b = self._bonus_atributo
        partes = [("nível", j.nivel // 2)]
        if attr == "forca":
            partes.append((f"Ataque {j.atk}", b(j.atk)))
        elif attr == "destreza":
            partes.append((f"Agilidade {j.agi}", b(j.agi * 1.4)))
        elif attr == "arcano":
            partes.append((f"Poder {j.poder}", b(j.poder)))
        elif attr == "percepcao":
            partes.append((f"Agilidade {j.agi}", b(j.agi)))
        elif attr == "vontade":
            partes.append((f"Defesa {j.defesa}", b(j.defesa * 0.8)))
        elif attr == "carisma":
            partes.append((f"Reputação {j.reputacao:+d}", j.reputacao // 10))
        for fonte in (CLASSES[j.classe], SPECS.get(j.spec, {})):  # "olhos de arqueiro", "paladino"...
            if attr in fonte.get("testes", {}):
                partes.append(fonte["testes"][attr])
        if self.sem_luz and attr in ("percepcao", "destreza"):
            partes.append(("escuridão", -4))
        return [p for p in partes if p[1]]

    def mod_teste(self, attr):
        return sum(v for _, v in self.partes_teste(attr))

    def dificuldade(self, cd):
        """O mundo endurece com você: cada dois níveis acima do primeiro, +1 na dificuldade."""
        return cd + (self.j.nivel - 1) // 2

    def teste(self, attr, cd):
        d = self.rng.randint(1, 20)
        mod = self.mod_teste(attr)
        cd = self.dificuldade(cd)
        total = d + mod
        ok = d == 20 or (d != 1 and total >= cd)
        self.ui.rolagem(NOMES_TESTE[attr], cd, d, mod, total, ok)
        return ok
