"""O mercado: estoque, preços, compra e venda (texto e interface gráfica)."""

from .. import itens
from ..itens import CONSUMIVEIS, descrever_bonus, gerar_equip
from .. import sobrevivencia
from ..telemetria import registrar
from ..regras import LIMITE_MOCHILA, NOMES_SLOT
from ..balanceamento import PRECO_FLECHAS


class Loja:
    def preco(self, base):
        fator = 1 - self.j.reputacao / 200
        return max(1, int(round(base * fator)))

    def estoque(self):
        chave = f"{self.loc['id']}:{self.dia // 3}"
        if chave not in self.lojas:
            prefixo = f"{self.loc['id']}:"
            self.lojas = {k: v for k, v in self.lojas.items() if not k.startswith(prefixo)}
            estoque = [gerar_equip(self.rng, self.j.classe, self.j.nivel + self.rng.choice([-1, 0, 0, 1]), qualidade=-1)
                       for _ in range(4)]
            self.lojas[chave] = estoque
        return self.lojas[chave]

    def dados_loja(self):
        j = self.j
        cons = ["tocha", "bandagem", "unguento", "pocao_vida", "tonico", "antidoto", "bomba_fumaca", "pena_fenix"]
        def item(it, preco):
            return {"nome": itens.rotulo(it), "slot": it["slot"], "raridade": it.get("raridade", "comum"),
                    "bonus": descrever_bonus(it["bonus"]), "bonus_bruto": it["bonus"], "base": it.get("base"),
                    "preco": preco, "classe": it.get("classe"), "lore": it.get("lore")}
        return {
            "ouro": j.ouro, "limite": LIMITE_MOCHILA, "ocupado": len(j.mochila),
            "consumiveis": [{"id": k, "nome": CONSUMIVEIS[k]["nome"], "desc": CONSUMIVEIS[k]["desc"],
                             "preco": self.preco(CONSUMIVEIS[k]["preco"]), "tem": j.consumiveis.get(k, 0)} for k in cons]
            + [{"id": "provisoes", "nome": "Provisões (1 dia)", "desc": "Pão duro, carne seca e um odre de água.",
                "preco": self.preco(4), "tem": j.provisoes, "limite": sobrevivencia.MAX_PROVISOES - j.provisoes}]
            + ([{"id": "flechas", "nome": "Feixe de 5 flechas", "desc": f"Flechas de freixo, pontas de ferro. A aljava leva {self.max_flechas()}.",
                 "preco": self.preco(PRECO_FLECHAS), "tem": j.flechas,
                 "limite": (self.max_flechas() - j.flechas + 4) // 5}] if j.classe == "arqueiro" else []),
            "equipamentos": [item(it, self.preco(it["preco"])) for it in self.estoque()],
            "mochila": [dict(item(it, it["preco"] // 2), usavel=self.pode_usar(it)) for it in j.mochila],
        }

    def loja(self):
        while True:
            j = self.j
            self.ui.cena("Mercado", f"{self.loc['nome']} · seu ouro: {j.ouro}", "menu")
            a_venda = self.estoque()
            if self.ui.painel("loja", self.dados_loja()):
                if self._loja_web(a_venda):
                    return
                continue
            opcoes = []
            for k in ("tocha", "bandagem", "unguento", "pocao_vida", "tonico", "antidoto", "bomba_fumaca",
                      "pena_fenix"):
                c = CONSUMIVEIS[k]
                opcoes.append((f"{c['nome']} — {self.preco(c['preco'])} ouro (você tem {j.consumiveis.get(k, 0)})",
                               ("consumivel", k)))
            opcoes.append((f"Provisões para 1 dia — {self.preco(4)} ouro (você tem {j.provisoes}/"
                           f"{sobrevivencia.MAX_PROVISOES})", ("provisoes",)))
            if j.classe == "arqueiro":
                opcoes.append((f"Feixe de 5 flechas — {self.preco(PRECO_FLECHAS)} ouro (você tem {j.flechas}/"
                               f"{self.max_flechas()})", ("flechas",)))
            for it in a_venda:
                opcoes.append((f"{itens.rotulo(it)} [{NOMES_SLOT[it['slot']]}] {descrever_bonus(it['bonus'])} — "
                               f"{self.preco(it['preco'])} ouro", ("equip", it)))
            if j.mochila:
                opcoes.append(("Vender itens da mochila", ("vender",)))
            opcoes.append(("Sair do mercado", None))
            op = self.menu("Comprar o quê?", [(o[0].replace("Sair do mercado", "Voltar"), o[1]) for o in opcoes])
            if op is None:
                return
            if op[0] == "vender":
                self.vender()
                continue
            preco = self.preco({"consumivel": lambda: CONSUMIVEIS[op[1]]["preco"], "flechas": lambda: PRECO_FLECHAS,
                                "provisoes": lambda: 4, "equip": lambda: op[1]["preco"]}[op[0]]())
            if op[0] == "provisoes" and j.provisoes >= sobrevivencia.MAX_PROVISOES:
                self.dizer("Você não consegue carregar mais comida.", "vermelho")
                continue
            if j.ouro < preco:
                self.dizer("Ouro insuficiente.", "vermelho")
                continue
            if op[0] == "equip" and len(j.mochila) >= LIMITE_MOCHILA:
                self.dizer("Sua mochila está cheia.", "vermelho")
                continue
            self.perder_ouro(preco)
            registrar(self, "compra", item=op[1] if op[0] == "consumivel" else op[1]["nome"] if op[0] == "equip"
                      else op[0], categoria=op[0], qtd=1, preco=preco)
            if op[0] == "consumivel":
                self.dar(op[1])
            elif op[0] == "flechas":
                self.dar_flechas(5)
            elif op[0] == "provisoes":
                j.provisoes += 1
                self.dizer(f"Pão duro, carne seca e um odre de água. (provisões: {j.provisoes})", "verde")
            else:
                a_venda.remove(op[1])
                self.oferecer_equip_comprado(op[1])

    def _loja_web(self, a_venda):
        """Mercado na interface web: cada compra e venda é uma opção direta. True = sair.
        Suprimentos podem ser comprados em quantidade (a tela manda "qtd" junto da escolha)."""
        j = self.j
        opcoes = []
        for k in ("tocha", "bandagem", "unguento", "pocao_vida", "tonico", "antidoto", "bomba_fumaca", "pena_fenix"):
            opcoes.append((f"Comprar {CONSUMIVEIS[k]['nome']}", ("consumivel", k), {"comprar": k}))
        opcoes.append(("Comprar provisões", ("provisoes",), {"comprar": "provisoes"}))
        if j.classe == "arqueiro":
            opcoes.append(("Comprar flechas", ("flechas",), {"comprar": "flechas"}))
        for i, it in enumerate(a_venda):
            opcoes.append((f"Comprar {it['nome']}", ("equip", it), {"comprar_item": i}))
        for i, it in enumerate(j.mochila):
            if self.pode_usar(it):
                opcoes.append((f"Equipar {it['nome']}", ("equipar", it), {"equipar": i}))
            opcoes.append((f"Vender {it['nome']}", ("vender", it), {"vender": i}))
        op = self.menu("", opcoes + [("Sair do mercado", None, {"voltar": True})])
        if op is None:
            return True
        if op[0] == "vender":
            j.mochila.remove(op[1])
            self.ui.efeito(f"Vendeu {op[1]['nome']}", "info")
            antes = j.ouro
            self.ganhar_ouro(op[1]["preco"] // 2)
            registrar(self, "venda", item=op[1]["nome"], raridade=op[1].get("raridade", "comum"), preco=j.ouro - antes)
            return False
        if op[0] == "equipar":
            self.equipar(op[1])
            return False
        preco = self.preco({"consumivel": lambda: CONSUMIVEIS[op[1]]["preco"], "flechas": lambda: PRECO_FLECHAS,
                            "provisoes": lambda: 4, "equip": lambda: op[1]["preco"]}[op[0]]())
        if op[0] == "equip":
            if j.ouro < preco:
                self.dizer("\"Sem ouro, sem negócio.\"", "vermelho")
                return False
            espaco = self.espaco_para(op[1])
            vago = self.pode_usar(op[1]) and not j.equip.get(espaco)
            if not vago and len(j.mochila) >= LIMITE_MOCHILA:
                self.dizer("Sua mochila está cheia. Venda ou largue algo antes.", "vermelho")
                return False
            self.perder_ouro(preco)
            registrar(self, "compra", item=op[1]["nome"], categoria="equipamento", qtd=1, preco=preco,
                      raridade=op[1].get("raridade", "comum"), vestiu=vago)
            a_venda.remove(op[1])
            if vago:  # espaço vazio no corpo: já sai vestido
                self.equipar(op[1], espaco)
            else:
                j.mochila.append(op[1])
                self.ui.efeito(f"{op[1]['nome']} vai para a mochila", "item")
            return False
        extra = getattr(self.ui, "extra_resposta", None) or {}
        try:
            qtd = max(1, min(99, int(extra.get("qtd", 1))))
        except (TypeError, ValueError):
            qtd = 1
        if op[0] == "provisoes":
            qtd = min(qtd, sobrevivencia.MAX_PROVISOES - j.provisoes)
            if qtd <= 0:
                self.dizer("Você não consegue carregar mais comida.", "vermelho")
                return False
        if op[0] == "flechas":
            qtd = min(qtd, (self.max_flechas() - j.flechas + 4) // 5)
            if qtd <= 0:
                self.dizer("Sua aljava já está cheia.", "vermelho")
                return False
        qtd = min(qtd, j.ouro // preco)
        if qtd <= 0:
            self.dizer("\"Sem ouro, sem negócio.\"", "vermelho")
            return False
        self.perder_ouro(preco * qtd)
        registrar(self, "compra", item=op[1] if op[0] == "consumivel" else op[0], categoria=op[0], qtd=qtd, preco=preco * qtd)
        if op[0] == "consumivel":
            self.dar(op[1], qtd)
        elif op[0] == "flechas":
            self.dar_flechas(5 * qtd)
        else:
            self.dar_provisoes(qtd)
        return False

    def oferecer_equip_comprado(self, item):
        if self.menu(f"Equipar {item['nome']} agora?", [("Sim", True), ("Não, guardar na mochila", False)]):
            self.equipar(item)
        else:
            self.j.mochila.append(item)

    def vender(self):
        j = self.j
        opcoes = [(f"{it['nome']} — {descrever_bonus(it['bonus'])} — vende por {it['preco'] // 2}", it)
                  for it in j.mochila]
        it = self.menu("Vender o quê?", opcoes + [("Voltar", None)])
        if it:
            j.mochila.remove(it)
            antes = j.ouro
            self.ganhar_ouro(it["preco"] // 2)
            registrar(self, "venda", item=it["nome"], raridade=it.get("raridade", "comum"), preco=j.ouro - antes)
