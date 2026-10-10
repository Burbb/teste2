"""Serviços da vila: ferreiro, curandeiro e rumores."""

from .. import comitiva, consequencias
from .. import eventos
from ..entidades import nome_stat
from ..eventos.vila import ouvir_rumor
from .. import itens
from .. import sobrevivencia
from ..telemetria import registrar


class Servicos:
    def pecas_da_forja(self):
        """O que o ferreiro pode reforçar: (espaço, item, atributo, ganho, custo), com ganho e custo nulos no limite."""
        j = self.j
        secundaria = {"guerreiro": "defesa", "arqueiro": "atk", "mago": "poder"}[j.classe]
        pecas = []
        for slot, stat in (("arma", "poder" if j.classe == "mago" else "atk"), ("armadura", "defesa"),
                           ("secundaria", secundaria)):
            item = j.equip[slot]
            if not item:
                continue
            ref = item.get("reforco", 0)
            if ref >= 5:
                pecas.append((slot, item, stat, None, None))
                continue
            pecas.append((slot, item, stat, max(1, round(item["bonus"].get(stat, 0) * 0.12)),
                          self.preco(int(40 * (ref + 1) ** 1.6))))
        return pecas

    def ferreiro(self):
        j = self.j
        while True:
            self.ui.cena("A forja", self.loc["nome"], "menu")  # a cada volta: na tela gráfica, a forja se redesenha
            pecas = self.pecas_da_forja()
            dados = {"ouro": j.ouro, "pecas": [
                {"slot": slot, "item": itens.ficha(item, j.nome_recurso), "reforco": item.get("reforco", 0),
                 "ganho": ganho and f"+{ganho} {nome_stat(stat, j.nome_recurso)}", "custo": custo,
                 "pode": custo is not None and j.ouro >= custo}
                for slot, item, stat, ganho, custo in pecas]}
            if self.ui.painel("ferreiro", dados):
                # Tela gráfica: cada peça é um cartão; o clique reforça. Fora isso, só sair.
                opcoes = [(f"Reforçar {item['nome']}", (item, stat, ganho, custo), {"reforcar": slot})
                          for slot, item, stat, ganho, custo in pecas if custo is not None]
                esc = self.menu("", opcoes + [("Voltar", "voltar", {"voltar": True})])
            else:
                opcoes = []
                for slot, item, stat, ganho, custo in pecas:
                    ref = item.get("reforco", 0)
                    if custo is None:
                        opcoes.append((f"{itens.rotulo(item)} — já está no limite (+5)", None))
                        continue
                    opcoes.append((f"{itens.rotulo(item)} +{ref} → +{ref + 1}: +{ganho} {nome_stat(stat, j.nome_recurso)} — "
                                   f"{custo} ouro", (item, stat, ganho, custo)))
                esc = self.menu(f"O ferreiro, um homem sem dois dedos, cospe na forja. \"Ouro primeiro.\" "
                                f"(você tem {j.ouro})", opcoes + [("Voltar", "voltar")])
            if esc == "voltar":
                return
            if esc is None:
                continue
            item, stat, ganho, custo = esc
            if j.ouro < custo:
                self.dizer("\"Volta quando tiver o dinheiro.\"", "vermelho")
                continue
            self.perder_ouro(custo, destino="ferreiro")
            item["bonus"][stat] = item["bonus"].get(stat, 0) + ganho
            item["reforco"] = item.get("reforco", 0) + 1
            item["nome"] = item["nome"].split(" +")[0] + f" +{item['reforco']}"
            j.recalcular()
            registrar(self, "ferreiro", item=item["nome"], stat=stat, ganho=ganho, custo=custo)
            self.dizer(f"Faíscas, marteladas, água fervendo. {item['nome']}: +{ganho} {nome_stat(stat, self.j.nome_recurso)}.", "verde")

    def curandeiro(self):
        j = self.j
        quem = consequencias.atendente(self)  # no Vau da campanha: Pita, ou Marta depois que a água limpa
        while j.ferimentos:
            self.ui.cena("A curandeira", self.loc["nome"], "menu")  # a cada volta: na tela gráfica, a cabana se redesenha
            custos = [self.preco((25 + 4 * j.nivel) if f["id"] == "infeccao" else (12 + 3 * j.nivel)) for f in j.ferimentos]
            dados = {"ouro": j.ouro, **({"quem": quem["quem"], "fala": quem["fala"]} if quem else {}), "ferimentos": [
                {"id": f["id"], "nome": sobrevivencia.FERIMENTOS[f["id"]]["nome"], "custo": custo, "pode": j.ouro >= custo,
                 "explica": sobrevivencia.explicar(f, j.nome_recurso, j)} for f, custo in zip(j.ferimentos, custos)]}
            if self.ui.painel("curandeira", dados):
                # Tela gráfica: cada ferimento é um cartão; o clique trata. Fora isso, só sair.
                esc = self.menu("", [(f"Tratar {sobrevivencia.FERIMENTOS[f['id']]['nome']}", (f["id"], custo),
                                      {"tratar": f["id"]}) for f, custo in zip(j.ferimentos, custos)]
                                + [("Voltar", None, {"voltar": True})])
            else:
                opcoes = [(f"{sobrevivencia.FERIMENTOS[f['id']]['nome']} — {custo} ouro", (f["id"], custo))
                          for f, custo in zip(j.ferimentos, custos)]
                esc = self.menu(quem["fala"] if quem else "A curandeira, uma velha de mãos manchadas de sangue seco, "
                                "examina você. \"O que vai ser?\"", opcoes + [("Voltar", None)])
            if not esc:
                return
            fid, custo = esc
            if j.ouro < custo:
                self.dizer("\"Sem ouro, sem cura. Ninguém aqui faz caridade mais.\"", "vermelho")
                continue
            self.perder_ouro(custo, destino="curandeira")
            sobrevivencia.curar_ferimento(self, fid)
            self.dizer(f"Ela costura, cauteriza e enfaixa sem anestesia. Você grita. "
                       f"{sobrevivencia.FERIMENTOS[fid]['nome']}: tratado.", "verde")

    def opcoes_templo(self):
        """O templo cuida de cada um pelo que falta a cada um: você e quem anda com você (desacordado também), cada um
        com o seu preço. Uma opção por pessoa; sem ninguém precisando, nenhuma."""
        j = self.j
        precisam = [(None, "você", j.max_hp - j.hp, j.max_hp)] if j.hp < j.max_hp else []
        precisam += [(m, comitiva.nome(m["id"]), m["max_hp"] - m["hp"], m["max_hp"])
                     for m in comitiva.junto(self) if m["hp"] < m["max_hp"] or m["ferido"]]
        opcoes = []
        for m, quem, falta, maximo in precisam:
            preco = self.preco(max(1, falta // 2))
            meta = {"predio": "templo", "servico": "templo", "curto": f"Cuidar de {quem}", "preco": preco,
                    "efeito": f"+{falta} de vida ({maximo}/{maximo})" + (", de pé de novo" if m and m["ferido"] else "")}
            if m:
                meta["alvo"] = m["id"]
            rotulo = f"Templo: cuidar da vida ({preco} ouro)" if m is None else f"Templo: cuidar de {quem} ({preco} ouro)"
            opcoes.append((rotulo, ("templo", m and m["id"], preco, falta), meta))
        return opcoes

    def balcao_templo(self, escolha):
        """Diante do balcão do templo: cuida de quem foi escolhido e continua ali, com o ouro e os preços de agora e só
        quem ainda precisa, até a pessoa voltar à vila. Sem mais ninguém para cuidar, o balcão diz isso e fica o Voltar.
        A meta `balcao` diz à tela gráfica que o balcão continua aberto (vila.js)."""
        while escolha:
            self.templo(*escolha)
            opcoes = self.opcoes_templo()
            op = self.menu("Mais alguém precisa de cuidados?" if opcoes else "Ninguém mais precisa de cuidados.",
                           opcoes + [("Voltar à vila", None, {"voltar": True, "balcao": "templo"})])
            escolha = op[1:] if op else None

    def templo(self, cid, preco, falta):
        if self.j.ouro < preco:
            self.dizer("Você não tem ouro suficiente.", "vermelho")
            return
        self.perder_ouro(preco, destino="templo")
        if cid is None:
            self.curar(falta)
            self.dizer("Um clérigo trata suas feridas com unguentos e orações.", "verde")
            return
        comitiva.cuidar(self, comitiva.membro(self, cid))
        self.dizer(f"Um clérigo trata {comitiva.nome(cid)} com unguentos e orações. De pé, inteiro de novo.", "verde")

    # ================================================================ vila: rumores, loja, mural
    def ouvir_rumores(self):
        chave = f"rumores:{self.dia}:{self.loc['id']}"
        if self.flag(chave, 0) >= 2:
            self.dizer("Os fregueses já contaram tudo o que sabiam hoje.", "cinza")
            return
        preco = self.preco(3)
        if self.j.ouro < preco:
            self.dizer("Sem ouro nem para uma caneca.", "vermelho")
            return
        self.perder_ouro(preco, destino="taverna")
        self.marcar(chave, self.flag(chave, 0) + 1)
        # O que se passa dentro da taverna só acontece ali, a quem senta para beber: às vezes a bebida vira briga, uma
        # queda de braço, ou o homem do canto (Morel) puxa conversa, em vez dos rumores. Enquanto ninguém conheceu
        # Morel, toda bebida sorteia (e ele é o mais provável): um companheiro não pode depender de sorte para aparecer.
        morel_esperando = any(ev.id == "morel_na_taverna" and not self.contagem.get(ev.id)
                              for ev, _ in eventos.motor.candidatos(self, "taverna"))
        if (morel_esperando or self.chance(0.35)) and eventos.disparar(self, "taverna"):
            return
        ouvir_rumor(self)
