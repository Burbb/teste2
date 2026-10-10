"""Equipamento, mochila, consumíveis e a tela de personagem."""

from ..habilidades import HABILIDADES
from .. import itens
from ..itens import CONSUMIVEIS, EM_ALIADO, PENA_FENIX_AGE_SOZINHA, descrever_bonus
from .. import comitiva
from .. import sobrevivencia
from .. import texto as tx
from ..telemetria import registrar
from ..regras import LIMITE_MOCHILA, NOMES_SLOT
from .. import balanceamento as bal


class Inventario:
    # ================================================================ equipamento e itens
    def oferecer_equip(self, item):
        """Um item encontrado: a tela gráfica mostra o cartão do saque (com o que você usa ao lado); a de texto, as
        linhas. Deixar para trás só existe quando não há onde guardar. Achado depois de uma vitória, na tela gráfica,
        espera o quadro do espólio (é uma escolha: vem logo depois dele)."""
        if self.espolio_aberto is not None:
            self.espolio_aberto["equip"].append(item)
            return
        rec = self.j.nome_recurso
        usa = self.pode_usar(item)
        cabe = len(self.j.mochila) < LIMITE_MOCHILA
        equipados = [it for it in (self.j.equip[s] for s in itens.espacos(item["slot"])) if it]
        if not self.ui.painel("achado", {"item": itens.ficha(item, rec), "equipados": [itens.ficha(it, rec) for it in equipados],
                                         "pode_usar": usa, "cabe": cabe}):
            raridade = itens.NOMES_RARIDADE[item.get("raridade", "comum")]
            self.dizer(f"Você encontrou: {itens.rotulo(item)} [{NOMES_SLOT[item['slot']]}, {raridade}]",
                       itens.cor(item) or "branco+negrito")
            self.dizer(f"  {descrever_bonus(item['bonus'], rec)}", itens.cor(item))
            if item.get("lore"):
                self.dizer(f"  \"{item['lore']}\"", "cinza")
            atual = self.j.equip[self.espaco_para(item)]
            if atual:
                self.dizer(f"  Equipado agora: {itens.rotulo(atual)} — {descrever_bonus(atual['bonus'], rec)}", "cinza")
        # Na tela gráfica, o cartão e estas opções moram numa janela própria (fora do log): {"achado": ...}.
        op = self.menu("O que fazer com o item?", [
            ("Equipar agora", "equipar", {"achado": "equipar"}) if usa else None,
            ("Guardar na mochila" + ("" if usa else " (para vender)"), "guardar", {"achado": "guardar"}) if cabe else None,
            ("Deixar para trás (mochila cheia)", "deixar", {"achado": "deixar"}) if not cabe else None,
        ])
        registrar(self, "saque", item=item["nome"], raridade=item.get("raridade", "comum"), slot=item["slot"],
                  nivel=item.get("nivel"), escolha=op or "deixar")
        if op == "equipar":
            espaco = self.espaco_para(item)
            self.equipar(item, avisar=not self.ui.conquistas_na_tela)
            # o mesmo voo do mercado: o ícone sai do cartão e pousa no espaço do corpo, que brilha ao receber
            self.ui.celebrar("equipou", {"espaco": espaco, "item": itens.ficha(item, rec), "achado": True})
        elif op == "guardar":
            self.j.mochila.append(item)
            if self.ui.conquistas_na_tela:  # o ícone voa do cartão até a mochila
                self.ui.celebrar("guardou", {"item": itens.ficha(item, rec)})
            else:
                self.dizer("Guardado na mochila.", "cinza")

    def espaco_para(self, item, destino=None):
        """Em qual espaço do corpo o item entra (anéis: o vazio, ou o primeiro)."""
        opcoes = itens.espacos(item["slot"])
        if destino in opcoes:
            return destino
        return next((s for s in opcoes if not self.j.equip.get(s)), opcoes[0])

    def pode_usar(self, item):
        return not item.get("classe") or item["classe"] == self.j.classe

    def desequipar(self, slot):
        j = self.j
        item = j.equip.get(slot)
        if not item:
            return
        if len(j.mochila) >= LIMITE_MOCHILA:
            self.dizer("A mochila está cheia. Largue alguma coisa antes.", "vermelho")
            return
        j.equip[slot] = None
        j.mochila.append(item)
        j.recalcular()
        self.dizer(f"Você tira {item['nome']} e guarda na mochila.", "cinza")

    def largar(self, item):
        if item in self.j.mochila:
            self.j.mochila.remove(item)
            self.dizer(f"Você larga {item['nome']} no chão. Alguém vai achar.", "cinza")

    def equipar(self, item, destino=None, avisar=True):
        """avisar=False: a tela já mostra (o cartão do item achado vira "Vestido" e o ícone voa até o corpo)."""
        j = self.j
        espaco = self.espaco_para(item, destino)
        antigo = j.equip[espaco]
        j.equip[espaco] = item
        if item in j.mochila:
            j.mochila.remove(item)
        if antigo:
            if len(j.mochila) < LIMITE_MOCHILA:
                j.mochila.append(antigo)
            else:
                self.dizer(f"Mochila cheia: {antigo['nome']} fica para trás.", "cinza")
        j.recalcular()
        if avisar:
            self.dizer(f"Você equipa {item['nome']}.", "verde")
        registrar(self, "equipar", item=item["nome"], slot=espaco, raridade=item.get("raridade", "comum"),
                  bonus=item["bonus"])

    def motivo_inutil(self, k, m=None):
        """Por que usar o item agora não faria nada (ou None). m: um companheiro, em vez de você."""
        j = self.j
        if m is not None:
            if k not in EM_ALIADO:
                return "Isso só serve em você."
            if m is j.companheiro:  # o animal do patrulheiro
                return f"{m['nome']} não precisa disso agora." if m["hp"] >= m["max_hp"] else None
            if m["hp"] >= m["max_hp"] and not m["ferido"]:
                return f"{comitiva.nome(m['id'])} não precisa disso agora."
            return None
        if k == "bomba_fumaca":
            return "A Bomba de Fumaça só serve no meio de uma luta: para fugir dela."
        if k == "pena_fenix":
            return PENA_FENIX_AGE_SOZINHA
        if k == "pocao_vida" and j.hp >= j.max_hp:
            return "Sua vida já está cheia."
        if k == "tonico" and j.rec >= j.max_rec:
            return f"{j.nome_recurso} já está no máximo."
        if k == "antidoto" and not j.efeito("veneno"):
            return "Não há veneno no seu sangue."
        if k == "bandagem" and not j.efeito("sangramento") and j.hp >= j.max_hp and not any(
                sobrevivencia.FERIMENTOS[f["id"]].get("aberto") and not f["tratado"] for f in j.ferimentos):
            return "Nada para enfaixar: sem sangramento, sem feridas abertas."
        if k == "unguento" and not sobrevivencia.tem(j, "infeccao"):
            return "Você não tem nenhuma infecção para tratar."
        if k == "bau" and not self.lugar_seguro():
            return "Aqui não: forçar a fechadura leva tempo e faz barulho. Abra numa vila ou à luz da fogueira."
        return None

    def lugar_seguro(self):
        """Onde se abre um baú: numa vila ou em volta da fogueira, nunca no meio da luta nem na estrada."""
        return self.combate_ativo is None and (self.loc["tipo"] == "vila" or self.na_fogueira)

    BAU_SUPRIMENTOS = ["pocao_vida", "pocao_vida", "tonico", "bandagem", "bandagem", "antidoto", "unguento",
                       "tocha", "bomba_fumaca"]

    def abrir_bau(self):
        """O baú trancado: ouro, um ou dois suprimentos e, às vezes, um equipamento melhor que o das lutas comuns.
        Na tela gráfica, tudo sai num quadro só (o do espólio); o equipamento vem logo depois, na janela dele."""
        nv = self.j.nivel
        frase = ("À luz da fogueira, você força a fechadura. A tampa range e cede." if self.na_fogueira else
                 "Num canto sossegado, você força a fechadura. A tampa range e cede.")
        if not self.ui.conquistas_na_tela:
            self.dizer(frase, "amarelo")
        self.abrir_espolio(titulo="baú aberto", frase=frase)  # na tela gráfica, a frase abre o quadro do que saiu
        ouro = self.ganhar_ouro(self.rng.randint(*bal.BAU_OURO) + bal.BAU_OURO_POR_NIVEL * nv, fonte="baus")
        suprimentos = [self.sortear(self.BAU_SUPRIMENTOS) for _ in range(self.rng.randint(1, 2))]
        for k in suprimentos:
            self.dar(k)
        equip = None
        if self.chance(bal.BAU_EQUIP):
            equip = itens.gerar_equip(self.rng, self.j.classe, nv, qualidade=1)
        registrar(self, "bau", ouro_bau=ouro, suprimentos=suprimentos,
                  equip=equip and {"item": equip["nome"], "raridade": equip.get("raridade", "comum")})
        if equip:
            self.oferecer_equip(equip)
        self.fechar_espolio()

    def usar_no_animal(self, k):
        """Poção e bandagem também servem no animal do patrulheiro. A bandagem põe de pé quem não podia lutar."""
        f = self.j.companheiro
        if not f or not self.j.tem(k):
            return False
        motivo = self.motivo_inutil(k, f)
        if motivo:
            self.dizer(motivo, "cinza")
            return False
        self.j.consumiveis[k] -= 1
        registrar(self, "consumivel", item=k, em_combate=False, em="fera")
        antes = f["hp"]
        if k == "pocao_vida":
            f["hp"] = min(f["max_hp"], f["hp"] + int(f["max_hp"] * bal.POCAO_VIDA))
            self.dizer(f"{f['nome']} lambe a Poção de Vida da sua mão. (+{f['hp'] - antes} vida)", "verde")
        else:
            f["hp"] = min(f["max_hp"], f["hp"] + bal.BANDAGEM_VIDA)
            self.dizer(f"Você enfaixa {f['nome']}, que reclama mas deixa."
                       + (" Já consegue ficar de pé." if antes <= 0 else "") + f" (+{f['hp'] - antes} vida)", "verde")
        return True

    def usar_em_companheiro(self, k, cid):
        """Fora de combate, poção e bandagem também servem na comitiva. A bandagem põe de pé quem caiu."""
        if cid == "fera":
            return self.usar_no_animal(k)
        m = comitiva.membro(self, cid)
        if not m or not self.j.tem(k):
            return False
        motivo = self.motivo_inutil(k, m)
        if motivo:
            self.dizer(motivo, "cinza")
            return False
        self.j.consumiveis[k] -= 1
        nome = comitiva.nome(cid)
        registrar(self, "consumivel", item=k, em_combate=False, em=cid)
        antes = m["hp"]
        if k == "pocao_vida":
            m["hp"] = min(m["max_hp"], m["hp"] + int(m["max_hp"] * bal.POCAO_VIDA))
            m["ferido"] = False
            self.dizer(f"{nome} bebe a Poção de Vida e respira melhor. (+{m['hp'] - antes} vida)", "verde")
        else:
            m["hp"] = min(m["max_hp"], m["hp"] + bal.BANDAGEM_VIDA)
            if m["ferido"]:
                m["ferido"] = False
                self.dizer(f"Você enfaixa {nome} com cuidado. Já consegue ficar de pé e lutar. (+{m['hp'] - antes} vida)",
                           "verde")
            else:
                self.dizer(f"Você troca as faixas de {nome}. (+{m['hp'] - antes} vida)", "verde")
        return True

    def usar_consumivel(self, k):
        j = self.j
        if not j.tem(k):
            return False
        motivo = self.motivo_inutil(k)
        if motivo:
            self.dizer(motivo, "cinza")
            return False
        j.consumiveis[k] -= 1
        nome = CONSUMIVEIS[k]["nome"]
        registrar(self, "consumivel", item=k, em_combate=self.combate_ativo is not None)
        if k == "pocao_vida":
            c = j.curar(j.max_hp * bal.POCAO_VIDA)
            self.dizer(f"Você bebe a {nome}. (+{c} vida)", "verde")
        elif k == "tonico":
            ganho = min(j.max_rec - j.rec, int(j.max_rec * bal.TONICO))
            j.rec += ganho
            self.dizer(f"Você bebe o {nome}. (+{ganho} {j.nome_recurso})", "azul")
        elif k == "antidoto":
            j.remover("veneno")
            self.dizer("O veneno deixa seu corpo.", "verde")
        elif k == "bandagem":
            sangrando = j.efeito("sangramento")
            j.remover("sangramento")
            tratou = sobrevivencia.tratar_com_bandagem(self)
            c = j.curar(bal.BANDAGEM_VIDA)
            if not tratou and not sangrando:
                self.dizer(f"Você troca as faixas velhas. (+{c} vida)", "verde")
            elif sangrando:
                self.dizer(f"O sangramento para. (+{c} vida)", "verde")
        elif k == "bau":
            self.abrir_bau()
        elif k == "unguento":
            if not sobrevivencia.tem(j, "infeccao"):
                j.consumiveis[k] += 1
                self.dizer("Você não tem nenhuma infecção para tratar.", "cinza")
                return False
            sobrevivencia.curar_ferimento(self, "infeccao")
            self.dizer("O unguento arde como fogo. Horas depois, a febre cede. Infecção curada.", "verde+negrito")
        else:
            j.consumiveis[k] += 1
            self.dizer("Isso não tem uso agora.", "cinza")
            return False
        return True

    # ================================================================ telas de informação
    def personagem(self):
        while True:
            j = self.j
            self.ui.cena(j.nome, f"{j.nome_classe} nível {j.nivel}", "menu")
            if self.ui.painel("personagem", {"limite": LIMITE_MOCHILA}):
                if self._personagem_web():
                    return
                continue
            self._personagem_texto()
            op = self.menu("", [
                ("Usar item da bolsa", "usar"),
                ("Equipar item da mochila", "equipar") if j.mochila else None,
                ("Voltar", None),
            ])
            if op is None:
                return
            if op == "usar":
                usaveis = [k for k in self.USAVEIS_FORA if j.tem(k)]
                k = self.menu("Usar:", [(CONSUMIVEIS[k]["nome"], k, {"item": k}) for k in usaveis] + [("Voltar", None)])
                if k:
                    self.usar_consumivel(k)
            else:
                it = self.menu("Equipar:", [(f"{it['nome']} [{NOMES_SLOT[it['slot']]}] "
                                             f"{descrever_bonus(it['bonus'], self.j.nome_recurso)}", it, {"mochila": i})
                                            for i, it in enumerate(j.mochila)] + [("Voltar", None)])
                if it:
                    if it["classe"] and it["classe"] != j.classe:
                        self.dizer("Você não sabe usar isso.", "vermelho")
                    else:
                        self.equipar(it)

    def _personagem_web(self):
        """Na interface web, cada ação do inventário é uma opção direta (arrastar, clicar). True = sair."""
        j = self.j
        opcoes = []
        for i, it in enumerate(j.mochila):
            if self.pode_usar(it):
                for destino in itens.espacos(it["slot"]):
                    opcoes.append((f"Equipar {it['nome']}", ("equipar", it, destino), {"equipar": i, "destino": destino}))
        for slot, it in j.equip.items():
            if it:
                opcoes.append((f"Tirar {it['nome']}", ("tirar", slot), {"tirar": slot}))
        opcoes += self.opcoes_bolsa()
        for i, it in enumerate(j.mochila):
            opcoes.append((f"Largar {it['nome']}", ("largar", it), {"largar": i}))
        op = self.menu("", opcoes + [("Voltar", None, {"voltar": True})])
        if op is None:
            return True
        if op[0] == "equipar":
            self.equipar(op[1], op[2])
        elif op[0] == "tirar":
            self.desequipar(op[1])
        elif op[0] == "usar":
            self.usar_consumivel(op[1])
        elif op[0] == "usar_em":
            self.usar_em_companheiro(op[1], op[2])
        else:
            self.largar(op[1])
        return False

    def _personagem_texto(self):
        j = self.j
        self.dizer(f"Vida {j.hp}/{j.max_hp}   {j.nome_recurso} {j.rec}/{j.max_rec}   Ataque {j.atk}   "
                   f"Defesa {j.defesa}   Agilidade {j.agi}   Poder {j.poder}")
        self.dizer(f"Provisões: {tx.plural(j.provisoes, 'dia')}   Tochas: {j.consumiveis.get('tocha', 0)}", "amarelo")
        males = sobrevivencia.descrever(j)
        self.dizer("Condição: " + (", ".join(males) if males else "sem ferimentos"),
                   "vermelho" if males else "verde")
        self.dizer(f"Reputação: {j.reputacao:+d}   Ouro: {j.ouro}" +
                   (f"   Flechas: {j.flechas}" if j.classe == "arqueiro" else ""))
        self.dizer("Equipamento:", "ciano")
        for slot, it in j.equip.items():
            self.dizer(f"  {NOMES_SLOT[slot]}: " + (f"{itens.rotulo(it)} ({descrever_bonus(it['bonus'], self.j.nome_recurso)})" if it
                                                    else "—"), itens.cor(it) if it else None)
        self.dizer("Habilidades: " + ", ".join(HABILIDADES[h]["nome"] for h in j.habilidades), "ciano")
        cons = [f"{CONSUMIVEIS[k]['nome']} x{v}" for k, v in j.consumiveis.items() if v > 0]
        self.dizer("Bolsa: " + (", ".join(cons) if cons else "vazia"), "ciano")
        if j.mochila:
            self.dizer(f"Mochila ({len(j.mochila)}/{LIMITE_MOCHILA}): " +
                       ", ".join(it["nome"] for it in j.mochila), "ciano")
        if j.companheiro:
            c = j.companheiro
            self.dizer(f"Companheiro: {c['nome']} — vida {c['hp']}/{c['max_hp']}, ataque {int(c['atk'])}", "ciano")
