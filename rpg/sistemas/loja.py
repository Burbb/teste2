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
                    "bonus": descrever_bonus(it["bonus"], j.nome_recurso), "bonus_bruto": it["bonus"], "base": it.get("base"),
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

    SUPRIMENTOS = ("tocha", "bandagem", "unguento", "pocao_vida", "tonico", "antidoto", "bomba_fumaca", "pena_fenix")

    def preco_suprimento(self, k):
        """Preço (já com a reputação) de um consumível, de um dia de provisões ou de um feixe de flechas."""
        base = PRECO_FLECHAS if k == "flechas" else 4 if k == "provisoes" else CONSUMIVEIS[k]["preco"]
        return self.preco(base)

    # ------------------------------------------------------------ regras (as mesmas para qualquer tela)
    def comprar_suprimento(self, k, qtd=1):
        """Compra `qtd` de um suprimento, respeitando ouro, comida que cabe e aljava. True se comprou."""
        j = self.j
        preco = self.preco_suprimento(k)
        try:
            qtd = max(1, min(99, int(qtd)))
        except (TypeError, ValueError):
            qtd = 1
        if k == "provisoes":
            qtd = min(qtd, sobrevivencia.MAX_PROVISOES - j.provisoes)
            if qtd <= 0:
                self.dizer("Você não consegue carregar mais comida.", "vermelho")
                return False
        if k == "flechas":
            qtd = min(qtd, (self.max_flechas() - j.flechas + 4) // 5)
            if qtd <= 0:
                self.dizer("Sua aljava já está cheia.", "vermelho")
                return False
        qtd = min(qtd, j.ouro // preco)
        if qtd <= 0:
            self.dizer("\"Sem ouro, sem negócio.\"", "vermelho")
            return False
        self.perder_ouro(preco * qtd)
        categoria = k if k in ("provisoes", "flechas") else "consumivel"
        registrar(self, "compra", item=k, categoria=categoria, qtd=qtd, preco=preco * qtd)
        if k == "flechas":
            self.dar_flechas(5 * qtd)
        elif k == "provisoes":
            self.dar_provisoes(qtd)
        else:
            self.dar(k, qtd)
        return True

    def comprar_equipamento(self, it, a_venda):
        """Compra uma peça do estoque. Com o espaço do corpo vazio, ela já sai vestida."""
        j = self.j
        preco = self.preco(it["preco"])
        if j.ouro < preco:
            self.dizer("\"Sem ouro, sem negócio.\"", "vermelho")
            return False
        espaco = self.espaco_para(it)
        vago = self.pode_usar(it) and not j.equip.get(espaco)
        if not vago and len(j.mochila) >= LIMITE_MOCHILA:
            self.dizer("Sua mochila está cheia. Venda ou largue algo antes.", "vermelho")
            return False
        self.perder_ouro(preco)
        registrar(self, "compra", item=it["nome"], categoria="equipamento", qtd=1, preco=preco,
                  raridade=it.get("raridade", "comum"), vestiu=vago)
        a_venda.remove(it)
        if vago:
            self.equipar(it, espaco)
        else:
            j.mochila.append(it)
            self.ui.efeito(f"{it['nome']} vai para a mochila", "item")
        return True

    def vender_item(self, it):
        """O mercador paga metade do valor."""
        j = self.j
        j.mochila.remove(it)
        self.ui.efeito(f"Vendeu {it['nome']}", "info")
        antes = j.ouro
        self.ganhar_ouro(it["preco"] // 2)
        registrar(self, "venda", item=it["nome"], raridade=it.get("raridade", "comum"), preco=j.ouro - antes)

    # ------------------------------------------------------------ telas
    def loja(self):
        while True:
            j = self.j
            self.ui.cena("Mercado", f"{self.loc['nome']} · seu ouro: {j.ouro}", "menu")
            a_venda = self.estoque()
            if self.ui.painel("loja", self.dados_loja()):
                if self._loja_web(a_venda):
                    return
                continue
            # Terminal: as mesmas regras, em forma de lista.
            opcoes = []
            for k in self.SUPRIMENTOS:
                c = CONSUMIVEIS[k]
                opcoes.append((f"{c['nome']} — {self.preco_suprimento(k)} ouro (você tem {j.consumiveis.get(k, 0)})",
                               ("suprimento", k)))
            opcoes.append((f"Provisões para 1 dia — {self.preco_suprimento('provisoes')} ouro (você tem {j.provisoes}/"
                           f"{sobrevivencia.MAX_PROVISOES})", ("suprimento", "provisoes")))
            if j.classe == "arqueiro":
                opcoes.append((f"Feixe de 5 flechas — {self.preco_suprimento('flechas')} ouro (você tem {j.flechas}/"
                               f"{self.max_flechas()})", ("suprimento", "flechas")))
            for it in a_venda:
                opcoes.append((f"{itens.rotulo(it)} [{NOMES_SLOT[it['slot']]}] {descrever_bonus(it['bonus'], j.nome_recurso)} — "
                               f"{self.preco(it['preco'])} ouro", ("equip", it)))
            if j.mochila:
                opcoes.append(("Vender itens da mochila", ("vender",)))
            op = self.menu("Comprar o quê?", opcoes + [("Voltar", None)])
            if op is None:
                return
            if op[0] == "vender":
                self.vender()
            elif op[0] == "equip":
                self.comprar_equipamento(op[1], a_venda)
            else:
                self.comprar_suprimento(op[1])

    def _loja_web(self, a_venda):
        """Mercado na interface web: cada compra e venda é uma opção direta. True = sair.
        Suprimentos podem ser comprados em quantidade (a tela manda "qtd" junto da escolha)."""
        j = self.j
        opcoes = []
        for k in self.SUPRIMENTOS:
            opcoes.append((f"Comprar {CONSUMIVEIS[k]['nome']}", ("suprimento", k), {"comprar": k}))
        opcoes.append(("Comprar provisões", ("suprimento", "provisoes"), {"comprar": "provisoes"}))
        if j.classe == "arqueiro":
            opcoes.append(("Comprar flechas", ("suprimento", "flechas"), {"comprar": "flechas"}))
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
            self.vender_item(op[1])
        elif op[0] == "equipar":
            self.equipar(op[1])
        elif op[0] == "equip":
            self.comprar_equipamento(op[1], a_venda)
        else:
            extra = getattr(self.ui, "extra_resposta", None) or {}
            self.comprar_suprimento(op[1], extra.get("qtd", 1))
        return False

    def vender(self):
        j = self.j
        opcoes = [(f"{it['nome']} — {descrever_bonus(it['bonus'], j.nome_recurso)} — vende por {it['preco'] // 2}", it)
                  for it in j.mochila]
        it = self.menu("Vender o quê?", opcoes + [("Voltar", None)])
        if it:
            self.vender_item(it)
