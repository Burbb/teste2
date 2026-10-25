"""Resumo, morte e o retrato final do herói para o registro."""

import os
from .. import texto as tx
from ..itens import descrever_bonus
from .. import comitiva
from .. import telemetria
from ..telemetria import registrar
from ..regras import FimDeJogo


class Finais:
    def _retrato_final(self):
        """Como o herói terminou: equipamento, atributos, talentos e comitiva (para o registro da partida)."""
        j = self.j
        return {"equipamento": {s: (f"{it['nome']} [{it.get('raridade', 'comum')}] {descrever_bonus(it['bonus'], self.j.nome_recurso)}"
                                    if it else None) for s, it in j.equip.items()},
                "stats": telemetria.instantaneo(j), "talentos": dict(j.talentos), "spec": j.spec,
                "fontes": telemetria.fontes_poder(self), "poder_equip": telemetria.poder_equip(j),
                "ouro_fontes": dict(self.estatisticas.get("ouro_fontes", {})),
                "ouro_gastos": dict(self.estatisticas.get("ouro_gastos", {})),
                "comitiva": [{"id": m["id"], "aprovacao": m["aprovacao"]} for m in comitiva.membros(self)]}

    # ================================================================ finais
    def resumo(self):
        e = self.estatisticas
        j = self.j
        self.dizer(f"{j.nome}, {j.nome_classe} nível {j.nivel} — {tx.plural(self.dia, 'dia')} de jornada.", "ciano")
        self.dizer(f"Inimigos derrotados: {e['abates']}  ·  Guardiões: {e['chefes']}  ·  "
                   f"Eventos vividos: {e['eventos']}  ·  Ouro ganho: {e['ouro_ganho']}  ·  "
                   f"Quedas: {e.get('quedas', 0)}", "ciano")
        self.dizer(f"Semente: {self.seed} (use --seed para repetir o sorteio)", "cinza")
        caminho = telemetria.exportar(self)
        if caminho:
            self.dizer(f"Registro da partida salvo em: {caminho} (e o .jsonl ao lado). "
                       f"Mande esses arquivos para análise de equilíbrio.", "ciano")

    def cair_sem_luta(self, causa, motivo):
        """A fome ou a infecção zerou a vida (causa: "fome" ou "infeccao"). Com o resgate, é uma queda como a do
        combate: o resgate vem quando a noite termina (Tempo.novo_dia). No hardcore, a partida acaba (motivo: o texto
        da morte)."""
        if self.hardcore:
            self.fim_de_jogo(motivo)
        if self.resgatando:  # nos dias do próprio resgate o tratamento segura: não há queda dentro da queda
            self.j.hp = max(1, self.j.hp)
            return
        self.j.hp = 0
        self.queda_pendente = self.queda_pendente or causa

    def fim_de_jogo(self, motivo):
        self.estatisticas["causa"] = motivo
        registrar(self, "fim", resultado="morte", causa=motivo, **self._retrato_final())
        if self.hardcore:  # morte permanente de verdade: o save vai junto
            try:
                os.remove(self.caminho_save())
            except OSError:
                pass
        self.ui.cena("Você morreu", f"dia {self.dia}", "morte")
        self.narrar(motivo, "vermelho")
        epitafio = self.sortear([
            "Ninguém veio buscar o corpo. Os lobos vieram.",
            "Seu nome será esquecido antes do próximo inverno.",
            "Em alguma taverna, alguém pergunta por você. Ninguém sabe responder.",
            "O próximo a tentar encontrará seus ossos — e talvez aprenda com eles.",
        ])
        self.narrar(epitafio, "cinza")
        self.resumo()
        self.pausar()
        raise FimDeJogo()
