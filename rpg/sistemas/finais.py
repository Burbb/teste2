"""Resumo, morte, vitória e o retrato final do herói para o registro."""

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
        self.dizer(f"Semente do mundo: {self.seed} (use --seed para jogar o mesmo reino de novo)", "cinza")
        caminho = telemetria.exportar(self)
        if caminho:
            self.dizer(f"Registro da partida salvo em: {caminho} (e o .jsonl ao lado). "
                       f"Mande esses arquivos para análise de equilíbrio.", "ciano")

    def fim_de_jogo(self, motivo):
        self.registrar_legado("morte", motivo)
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

    def vitoria(self):
        j = self.j
        a = self.antagonista
        self.registrar_legado("vitoria", f"derrotou {a['nome']}")
        self.estatisticas["venceu"] = True
        registrar(self, "fim", resultado="vitoria", causa=f"derrotou {a['nome']}", **self._retrato_final())
        self.ui.cena("Vitória", f"dia {self.dia}", "vitoria")
        self.narrar(f"{tx.maiuscula(a['curto'])} se desfaz como cinza ao vento. A Fenda se fecha com um "
                    f"suspiro que ecoa por todo o reino.", "amarelo")
        epilogos = {
            "paladino": "Os templos acendem velas em seu nome. Você se torna o escudo do reino.",
            "berserker": "Bardos cantam sobre a fúria que nem o Vazio conseguiu conter.",
            "patrulheiro": "Você volta às matas, onde cada árvore parece saudar seu retorno.",
            "sombra": "Ninguém sabe ao certo quem salvou o reino. É exatamente como você prefere.",
            "piromante": "Por anos, o céu sobre a Fenda brilha em tons de brasa. Sua marca.",
            "necromante": "Os vivos te temem, os mortos te agradecem. Você aprendeu a conviver com os dois.",
        }
        self.narrar(epilogos.get(j.spec, "Você volta para casa, mais velho do que os dias de viagem explicam."))
        if j.reputacao >= 20:
            self.narrar("Em cada vila por onde passa, crianças brincam de ser você.")
        elif j.reputacao <= -20:
            self.narrar("O reino está salvo, mas as portas se fecham quando você passa. Heróis nem sempre são amados.")
        self.resumo()
        self.pausar()
        raise FimDeJogo()
