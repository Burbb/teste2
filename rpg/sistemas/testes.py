"""Testes de atributo: d20 + bônus contra a dificuldade."""

import math
from .. import atributos as atr
from .. import balanceamento as bal
from .. import sobrevivencia
from ..classes import CLASSES, SPECS
from ..regras import NOMES_TESTE


TESTE_POR_PONTO = 1.5
# o valor derivado de cada atributo: o que um ferimento ou a fome tiram dele vale no teste (sobrevivencia.py)
PENALIZA = {"forca": "atk", "agilidade": "agi", "intelecto": "poder"}
TESTE_DERIVADO = {"forca": "Ataque", "destreza": "Agilidade", "arcano": "Poder"}


class Testes:
    # ================================================================ testes
    @staticmethod
    def _bonus_atributo(valor):
        """Atributos ajudam nos testes, mas com retorno decrescente: 5 → +2, 11 → +4, 20 → +6, 43 → +8."""
        return int(round(2.5 * math.log2(1 + max(0, valor) / 5)))

    # para que serve cada teste (a ficha mostra; a lista vem dos eventos que pedem cada um)
    USO_TESTE = {
        "forca": "Arrombar, arrancar, separar uma briga, trabalho pesado.",
        "destreza": "Esgueirar-se, fugir, pegar sem ser visto, trabalho delicado.",
        "arcano": "Ler runas e escritos antigos, lidar com magia e anomalias.",
        "percepcao": "Notar armadilhas, pistas, golpes e emboscadas (às vezes o dado rola sozinho, como ao cruzar com inimigos).",
        "vontade": "Resistir a chamados, medo e impulsos; rezar; aguentar a dor.",
        "carisma": "Convencer, negociar, intimidar.",
    }
    CD_MEDIA = 12  # a dificuldade típica de um teste antes do ajuste por nível (a chance que a dica mostra)

    def partes_fixas_teste(self, attr):
        """O que o personagem soma no teste em qualquer situação: o nível, o atributo de origem e a classe."""
        j = self.j
        b = self._bonus_atributo
        partes = [("nível", j.nivel // 2)]
        # O atributo de origem (etapa 4, atributos.py): cada teste pelo seu; ×1,5 deixa o bônus perto do de antes, quando
        # vinha do Ataque, do Poder, da Agilidade e da Defesa. A Presença soma o que passou da inicial (no começo, nada:
        # o Carisma de quem começa é o de antes).
        origem = {"forca": "forca", "destreza": "agilidade", "arcano": "intelecto", "percepcao": "percepcao",
                  "vontade": "vontade"}
        if attr in origem:
            a = origem[attr]
            v = atr.de(j).get(a, 0)
            # ferimento e fome que tiram do valor derivado (a perna torcida, da Agilidade) tiram também do teste
            for _, f in sobrevivencia.fontes_penalidade(j).get(PENALIZA.get(a), []):
                v = v * f
            v = int(round(v))
            partes.append((f"{atr.NOMES[a]} {v}", b(v * TESTE_POR_PONTO)))
        elif attr == "carisma":
            partes.append((f"{atr.NOMES['presenca']} {atr.presenca(j)}", atr.presenca(j) - atr.PRESENCA_INICIAL))
            partes.append((f"Reputação {j.reputacao:+d}", j.reputacao // 10))
        for fonte in (CLASSES[j.classe], SPECS.get(j.spec, {})):  # "olhos de arqueiro", "paladino"...
            if attr in fonte.get("testes", {}):
                partes.append(fonte["testes"][attr])
        return [p for p in partes if p[1]]

    def situacao_teste(self, attr):
        """O que vale só agora, pela situação (sem luz), e não é do personagem."""
        partes = []
        if self.sem_luz and attr in ("percepcao", "destreza"):
            partes.append(("escuridão", -bal.ESCURO_TESTES))
        return partes

    def partes_teste(self, attr):
        """De onde vem o bônus de cada teste agora: [(rótulo, valor), ...] (as fixas e as da situação)."""
        return self.partes_fixas_teste(attr) + self.situacao_teste(attr)

    def chance_teste_media(self, attr):
        """A chance (em %) de passar num teste de dificuldade típica (CD_MEDIA, com o ajuste do nível), pela regra do
        teste: o menor d20 que passa, de 20 em 20 (5% cada face)."""
        return (21 - self.precisa_no_dado(self.dificuldade(self.CD_MEDIA), self.mod_teste(attr))) * 5

    def mod_teste(self, attr):
        return sum(v for _, v in self.partes_teste(attr))

    def dificuldade(self, cd):
        """O mundo endurece com você: cada dois níveis acima do primeiro, +1 na dificuldade."""
        return cd + (self.j.nivel - 1) // 2

    @staticmethod
    def precisa_no_dado(cd, mod):
        """O menor d20 que passa no teste (a regra de teste: o 20 sempre passa, o 1 sempre falha): 2 é "só falha com
        1", 20 é "só passa com 20". A tela mostra; não decide nada."""
        return min(20, max(2, cd - mod))

    def teste(self, attr, cd):
        d = self.rng.randint(1, 20)
        mod = self.mod_teste(attr)
        cd = self.dificuldade(cd)
        total = d + mod
        ok = d == 20 or (d != 1 and total >= cd)
        self.ui.rolagem(NOMES_TESTE[attr], cd, d, mod, total, ok, precisa=self.precisa_no_dado(cd, mod))
        return ok
