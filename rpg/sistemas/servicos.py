"""Serviços da vila: ferreiro, curandeiro e rumores."""

from ..entidades import nome_stat
from ..eventos.vila import ouvir_rumor
from .. import itens
from .. import sobrevivencia
from ..telemetria import registrar


class Servicos:
    def ferreiro(self):
        j = self.j
        self.ui.cena("A forja", self.loc["nome"], "menu")
        while True:
            opcoes = []
            secundaria = {"guerreiro": "defesa", "arqueiro": "atk", "mago": "poder"}[j.classe]
            for slot, stat in (("arma", "poder" if j.classe == "mago" else "atk"), ("armadura", "defesa"),
                               ("secundaria", secundaria)):
                item = j.equip[slot]
                if not item:
                    continue
                ref = item.get("reforco", 0)
                if ref >= 5:
                    opcoes.append((f"{itens.rotulo(item)} — já está no limite (+5)", None))
                    continue
                custo = self.preco(int(40 * (ref + 1) ** 1.6))
                ganho = max(1, round(item["bonus"].get(stat, 0) * 0.12))
                opcoes.append((f"{itens.rotulo(item)} +{ref} → +{ref + 1}: +{ganho} {nome_stat(stat, self.j.nome_recurso)} — {custo} ouro",
                               (item, stat, ganho, custo)))
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
            self.perder_ouro(custo)
            item["bonus"][stat] = item["bonus"].get(stat, 0) + ganho
            item["reforco"] = item.get("reforco", 0) + 1
            item["nome"] = item["nome"].split(" +")[0] + f" +{item['reforco']}"
            j.recalcular()
            registrar(self, "ferreiro", item=item["nome"], stat=stat, ganho=ganho, custo=custo)
            self.dizer(f"Faíscas, marteladas, água fervendo. {item['nome']}: +{ganho} {nome_stat(stat, self.j.nome_recurso)}.", "verde")

    def curandeiro(self):
        j = self.j
        self.ui.cena("A curandeira", self.loc["nome"], "menu")
        while j.ferimentos:
            opcoes = []
            for f in j.ferimentos:
                d = sobrevivencia.FERIMENTOS[f["id"]]
                custo = self.preco((25 + 4 * j.nivel) if f["id"] == "infeccao" else (12 + 3 * j.nivel))
                opcoes.append((f"{d['nome']} — {custo} ouro", (f["id"], custo)))
            esc = self.menu("A curandeira, uma velha de mãos manchadas de sangue seco, examina você. "
                            "\"O que vai ser?\"", opcoes + [("Voltar", None)])
            if not esc:
                return
            fid, custo = esc
            if j.ouro < custo:
                self.dizer("\"Sem ouro, sem cura. Ninguém aqui faz caridade mais.\"", "vermelho")
                continue
            self.perder_ouro(custo)
            sobrevivencia.curar_ferimento(self, fid)
            self.dizer(f"Ela costura, cauteriza e enfaixa sem anestesia. Você grita. "
                       f"{sobrevivencia.FERIMENTOS[fid]['nome']}: tratado.", "verde")

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
        self.perder_ouro(preco)
        self.marcar(chave, self.flag(chave, 0) + 1)
        ouvir_rumor(self)
