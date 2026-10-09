"""O mercado: estoque, preços, compra e venda (texto e interface gráfica)."""

import random

from .. import balanceamento as bal
from .. import itens
from ..itens import CONSUMIVEIS, DO_MERCADO, RECURSOS, descrever_bonus, gerar_equip
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

    def _chave_vendidos(self):
        return f"vendidos:{self.loc['id']}:{self.dia}"

    def estoque_suprimentos(self):
        """Quanto o mercado desta vila ainda tem hoje de cada consumível. O sorteio tem semente própria (mundo,
        vila e dia: não mexe no resto da partida) e o dia novo traz estoque novo: reabastece toda manhã."""
        sorteio = random.Random(f"{self.seed}:{self.loc['id']}:{self.dia}")
        vendidos = self.lojas.get(self._chave_vendidos(), {})
        return {k: max(0, sorteio.randint(*bal.ESTOQUE_MERCADO[k]) - vendidos.get(k, 0)) for k in self.COM_ESTOQUE}

    def dados_loja(self):
        j = self.j
        estoque = self.estoque_suprimentos()
        def item(it, preco):
            return itens.ficha(it, j.nome_recurso, preco=preco)
        return {
            "ouro": j.ouro, "limite": LIMITE_MOCHILA, "ocupado": len(j.mochila),
            "consumiveis": [{"id": k, "nome": CONSUMIVEIS[k]["nome"], "icone": CONSUMIVEIS[k]["icone"],
                             "desc": CONSUMIVEIS[k]["desc"],
                             "preco": self.preco(CONSUMIVEIS[k]["preco"]), "tem": j.consumiveis.get(k, 0),
                             "estoque": estoque[k], "limite": estoque[k]} for k in self.SUPRIMENTOS]
            + [{"id": "provisoes", "nome": "Provisões (1 dia)", "icone": RECURSOS["comida"]["icone"], "desc": "Pão duro, carne seca e um odre de água.",
                "preco": self.preco(4), "tem": j.provisoes, "estoque": estoque["provisoes"],
                "limite": min(estoque["provisoes"], sobrevivencia.MAX_PROVISOES - j.provisoes)}]
            + ([{"id": "flechas", "nome": "Flecha", "icone": RECURSOS["flechas"]["icone"], "desc": f"Flecha de freixo, ponta de ferro. A aljava leva {self.max_flechas()}.",
                 "preco": self.preco(PRECO_FLECHAS), "tem": j.flechas,
                 "estoque": estoque["flechas"], "limite": min(estoque["flechas"], self.max_flechas() - j.flechas)}]
               if j.classe == "arqueiro" else []),
            "equipamentos": [item(it, self.preco(it["preco"])) for it in self.estoque()],
            "mochila": [dict(item(it, it["preco"] // 2), usavel=self.pode_usar(it)) for it in j.mochila],
            "recompra": [item(it, valor) for it, valor in self.recompra],
        }

    SUPRIMENTOS = DO_MERCADO  # o catálogo diz (itens.py: mercado)
    COM_ESTOQUE = SUPRIMENTOS + ("provisoes", "flechas")  # tudo o que o mercado vende a granel acaba e reabastece

    def preco_suprimento(self, k):
        """Preço (já com a reputação) de um consumível, de um dia de provisões ou de uma flecha."""
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
            qtd = min(qtd, self.max_flechas() - j.flechas)
            if qtd <= 0:
                self.dizer("Sua aljava já está cheia.", "vermelho")
                return False
        if k in self.COM_ESTOQUE:
            qtd = min(qtd, self.estoque_suprimentos()[k])
            if qtd <= 0:
                nome = {"provisoes": "Comida", "flechas": "Flechas"}.get(k) or CONSUMIVEIS[k]["nome"]
                self.dizer(f"\"{nome}? Acabou. Amanhã cedo chega mais.\"", "vermelho")
                return False
        qtd = min(qtd, j.ouro // preco)
        if qtd <= 0:
            self.dizer("\"Sem ouro, sem negócio.\"", "vermelho")
            return False
        if k in self.COM_ESTOQUE:
            chave = self._chave_vendidos()
            prefixo = f"vendidos:{self.loc['id']}:"  # o que se vendeu em outros dias já não importa
            self.lojas = {c: v for c, v in self.lojas.items() if not c.startswith(prefixo) or c == chave}
            vendidos = self.lojas.setdefault(chave, {})
            vendidos[k] = vendidos.get(k, 0) + qtd
        self.perder_ouro(preco * qtd, destino="mercado")
        categoria = k if k in ("provisoes", "flechas") else "consumivel"
        registrar(self, "compra", item=k, categoria=categoria, qtd=qtd, preco=preco * qtd)
        if k == "flechas":
            self.dar_flechas(qtd)
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
        self.perder_ouro(preco, destino="mercado")
        registrar(self, "compra", item=it["nome"], categoria="equipamento", qtd=1, preco=preco,
                  raridade=it.get("raridade", "comum"), vestiu=vago)
        a_venda.remove(it)
        if vago:
            self.equipar(it, espaco)
            # Na tela gráfica, o item "voa" até o espaço do corpo: ninguém acha que ele sumiu.
            self.ui.celebrar("equipou", {"espaco": espaco, "item": itens.ficha(it, j.nome_recurso)})
            self.ui.efeito(f"Vestiu {it['nome']}", "item")
        else:
            j.mochila.append(it)
            self.ui.efeito(f"{it['nome']} vai para a mochila", "item")
        return True

    RECOMPRA_MAX = 6  # quantos dos últimos vendidos o mercador ainda guarda no balcão

    def vender_item(self, it):
        """O mercador paga metade do valor. O item fica no balcão até você sair: dá para recomprar pelo mesmo preço."""
        j = self.j
        j.mochila.remove(it)
        valor = it["preco"] // 2  # exatamente o que o botão "Vender por" anunciou
        j.ouro += valor
        self.recompra = [(it, valor)] + self.recompra[:self.RECOMPRA_MAX - 1]
        self.ui.efeito(f"Vendeu {it['nome']}: +{valor} ouro", "ouro")
        registrar(self, "venda", item=it["nome"], raridade=it.get("raridade", "comum"), preco=valor)

    def recomprar_item(self, i):
        """Desfaz uma venda desta visita, pelo que o mercador pagou."""
        j = self.j
        it, valor = self.recompra[i]
        if j.ouro < valor:
            self.dizer("\"Sem ouro, sem negócio.\"", "vermelho")
            return False
        if len(j.mochila) >= LIMITE_MOCHILA:
            self.dizer("Sua mochila está cheia. Venda ou largue algo antes.", "vermelho")
            return False
        del self.recompra[i]
        self.perder_ouro(valor, destino="mercado")
        j.mochila.append(it)
        self.ui.efeito(f"{it['nome']} volta para a mochila", "item")
        return True

    # ------------------------------------------------------------ telas
    def loja(self):
        self.recompra = []  # visita nova: o balcão de recompra começa vazio
        while True:
            j = self.j
            self.ui.cena("Mercado", self.loc["nome"], "menu")  # o ouro já está no topo e no balcão
            a_venda = self.estoque()
            if self.ui.painel("loja", self.dados_loja()):
                if self._loja_web(a_venda):
                    return
                continue
            # Terminal: as mesmas regras, em forma de lista.
            opcoes = []
            estoque = self.estoque_suprimentos()
            for k in self.SUPRIMENTOS:
                c = CONSUMIVEIS[k]
                resta = f"{estoque[k]} à venda" if estoque[k] else "esgotado até amanhã"
                opcoes.append((f"{c['nome']} — {self.preco_suprimento(k)} ouro ({resta}; você tem {j.consumiveis.get(k, 0)})",
                               ("suprimento", k)))
            opcoes.append((f"Provisões para 1 dia — {self.preco_suprimento('provisoes')} ouro ({estoque['provisoes']} à "
                           f"venda; você tem {j.provisoes}/{sobrevivencia.MAX_PROVISOES})", ("suprimento", "provisoes")))
            if j.classe == "arqueiro":
                opcoes.append((f"5 flechas — {self.preco_suprimento('flechas')} ouro cada ({estoque['flechas']} à venda; "
                               f"você tem {j.flechas}/{self.max_flechas()})", ("suprimento", "flechas")))
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
            elif op[1] == "flechas":  # no terminal, flecha a flecha seria cansativo: cada escolha leva 5
                self.comprar_suprimento("flechas", 5)
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
        for i, (it, _) in enumerate(self.recompra):
            opcoes.append((f"Recomprar {it['nome']}", ("recomprar", i), {"recomprar": i}))
        op = self.menu("", opcoes + [("Sair do mercado", None, {"voltar": True})])
        if op is None:
            return True
        if op[0] == "vender":
            self.vender_item(op[1])
        elif op[0] == "recomprar":
            self.recomprar_item(op[1])
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
