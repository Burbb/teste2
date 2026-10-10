"""A vez do herói: atacar, habilidades, itens (em você ou em quem luta ao seu lado), analisar e fugir."""

from .. import texto as tx
from ..classes import CLASSES
from ..habilidades import HABILIDADES, custo_flechas, descricao_habilidade
from ..modificadores import disparar, mod
from ..dados import TRACOS
from ..inimigos import NOMES_HABS_INIMIGO
from ..itens import CONSUMIVEIS, EM_ALIADO, PENA_FENIX_AGE_SOZINHA, USAVEIS_NA_LUTA, ficha
from .. import comitiva, telemetria
from ..talentos import custo_habilidade
from .. import balanceamento as bal

USAVEIS_EM_COMBATE = USAVEIS_NA_LUTA  # o catálogo diz (itens.py: luta)


class AcoesDoHeroi:
    # ------------------------------------------------------------ jogador
    def fase_jogador(self):
        j = self.j
        self.mostrar_estado()
        if mod(j, "regen_vida") and j.hp < j.max_hp:
            j.curar(mod(j, "regen_vida"))
        if self.processar_efeitos(j) or not j.vivo:
            return None
        while True:
            nome_atk = CLASSES[j.classe]["ataque"][0]
            if j.classe == "arqueiro" and j.flechas <= 0:
                nome_atk = "Golpe de Adaga — sem flechas!"
            analisar = self.ui.analisar_no_menu
            opcoes = [f"Atacar ({nome_atk})", "Habilidades", "Itens"] + (["Analisar inimigos"] if analisar else [])
            # Na tela gráfica as ações viram uma barra dentro da arena, com as habilidades já à mostra.
            metas = [{"acao": "atacar", "nome": nome_atk}, {"acao": "habilidades", "habilidades": self.metas_habilidades()},
                     {"acao": "itens", "itens": self.metas_itens()}] + ([{"acao": "analisar"}] if analisar else [])
            if self.pode_fugir:
                opcoes.append("Fugir")
                metas.append({"acao": "fugir"})
            self.ui.meta_opcoes = metas
            try:
                esc = self.ui.escolher("Sua ação:", opcoes)
            finally:
                self.ui.meta_opcoes = None
            if esc >= 3 and not analisar:
                esc += 1  # mantém a numeração das ações abaixo
            if esc == 0:
                alvo = self.escolher_alvo(cancelavel=True)
                if alvo is None:
                    continue
                self.ataque_basico(alvo)
                return None
            if esc == 1:
                if self.menu_habilidades():
                    return None
            elif esc == 2:
                r = self.menu_itens()
                if r == "fuga":
                    return "fuga"
                if r:
                    return None
            elif esc == 3:
                self.analisar()
            elif esc == 4:
                return "fuga" if self.tentar_fuga() else None

    def escolher_alvo(self, cancelavel=False):
        """Com cancelavel, a lista ganha "Voltar" e devolve None se a pessoa desistir (nada foi gasto ainda)."""
        vivos = self.inimigos_vivos()
        if len(vivos) == 1:
            return vivos[0]
        self.ui.meta_opcoes = [{"alvo": self.uid(e)} for e in vivos] + ([{"voltar": True}] if cancelavel else [])
        try:
            esc = self.ui.escolher("Alvo:", [f"{e.nome} ({e.hp}/{e.max_hp})" for e in vivos] + (["Voltar"] if cancelavel else []))
        finally:
            self.ui.meta_opcoes = None
        return vivos[esc] if esc < len(vivos) else None

    def ataque_basico(self, alvo):
        j = self.j
        nome, alcance, tipo, stat, mult = CLASSES[j.classe]["ataque"]
        if j.classe == "arqueiro":
            if j.flechas > 0:
                j.flechas -= 1
                self.flechas_gastas += 1
            else:
                nome, alcance, mult = "Adaga", "corpo", 0.6
        with self.agindo(j, nome, alvo, hab="ataque"):
            dano = self.atacar(j, alvo, mult, tipo=tipo, alcance=alcance, stat=stat, rotulo=nome)
            if dano:
                disparar(self, j, "ataque_basico", alvo=alvo)  # Pontas Venenosas...
            if dano and j.rec < j.max_rec:
                ganho = min(j.max_rec - j.rec, max(bal.ATAQUE_RECURSO_MIN, round(j.max_rec * bal.ATAQUE_RECURSO)))
                j.rec += ganho
                self.recuperou(j, ganho, discreto=True)

    def motivo_bloqueio(self, h_id):
        """Por que não dá para usar a habilidade agora (ou None se dá)."""
        j, h = self.j, HABILIDADES[h_id]
        if j.rec < custo_habilidade(j, h_id):
            return f"{j.nome_recurso} insuficiente"
        if self.flechas_de(h) > j.flechas:
            return "Flechas insuficientes"
        if h.get("req"):
            return h["req"](self)
        return None

    def flechas_de(self, h):
        """Flechas que a habilidade gasta agora (a Chuva de Flechas, uma por inimigo de pé)."""
        return custo_flechas(h, len(self.inimigos_vivos()))

    def metas_habilidades(self):
        """Cada habilidade como a interface gráfica a desenha: ícone, custo, alvo, dica e se dá para usar agora."""
        j = self.j
        metas = []
        for h_id in j.habilidades:
            h = HABILIDADES[h_id]
            motivo = self.motivo_bloqueio(h_id)
            metas.append({"habilidade": h_id, "nome": h["nome"], "icone": h["icone"], "familia": h["familia"],
                          "custo": custo_habilidade(j, h_id),
                          "recurso": j.nome_recurso, "flechas": self.flechas_de(h), "alvo_tipo": h["alvo"],
                          "desc": descricao_habilidade(h_id, j), "pode": motivo is None, "motivo": motivo})
        return metas

    def menu_habilidades(self):
        j = self.j
        ids = list(j.habilidades)
        opcoes = []
        for h_id in ids:
            h = HABILIDADES[h_id]
            custo = f"{custo_habilidade(j, h_id)} {j.nome_recurso}"
            flechas = self.flechas_de(h)
            if flechas:
                custo += f", {flechas} flecha{'s' if flechas > 1 else ''}"
            opcoes.append(f"{h['nome']} [{custo}] — {h['desc']}")
        metas = self.metas_habilidades()
        opcoes.append("Voltar")
        self.ui.meta_opcoes = metas + [None]
        try:
            esc = self.ui.escolher("Habilidades:", opcoes)
        finally:
            self.ui.meta_opcoes = None
        if esc == len(ids):
            return False
        h = HABILIDADES[ids[esc]]
        custo = custo_habilidade(j, ids[esc])
        if j.rec < custo:
            self.dizer(f"{j.nome_recurso} insuficiente.", "cinza")
            return False
        if self.flechas_de(h) > j.flechas:
            self.dizer("Flechas insuficientes!", "cinza")
            return False
        if h.get("req"):
            erro = h["req"](self)
            if erro:
                self.dizer(erro, "cinza")
                return False
        alvo = None
        if h["alvo"] == "inimigo":
            alvo = self.escolher_alvo(cancelavel=True)
            if alvo is None:
                return False
        j.rec -= custo
        self.tel["habilidades"][ids[esc]] = self.tel["habilidades"].get(ids[esc], 0) + 1
        self.tel["rec_gasto"] += custo
        flechas = self.flechas_de(h)
        j.flechas -= flechas
        self.flechas_gastas += flechas
        with self.agindo(j, h["nome"], alvo, area=h["alvo"] == "todos", hab=ids[esc], anim=h.get("anim")):
            antes, self._cura_j = j.hp, 0
            efeitos_antes = {k: dict(v) for k, v in j.efeitos.items()}
            h["fn"](self, j, alvo)
            self.curou(j, j.hp - antes - self._cura_j, rotulo=h["nome"])
            # Buffs em si mesmo (grito, escudo, esquiva, sombras) também viram um lance: a tela anima e espera.
            novos = [k for k, v in j.efeitos.items() if efeitos_antes.get(k) != v]
            if novos:
                self.lance("buff", em="j", efeitos=novos, rotulo=h["nome"], hab=ids[esc],
                           **({"anim": h["anim"]} if h.get("anim") else {}))
        return True

    def itens_da_luta(self):
        """Consumíveis que servem em luta e armas (ou escudo/aljava/grimório) da mochila para trocar.
        Trocar de arma gasta o turno; armadura não: ninguém veste uma cota de malha com um lobo no pescoço."""
        j = self.j
        usaveis = [k for k in USAVEIS_EM_COMBATE if j.consumiveis.get(k, 0) > 0]
        armas = [it for it in j.mochila if it["slot"] in ("arma", "secundaria") and self.g.pode_usar(it)]
        return usaveis, armas

    def metas_itens(self):
        """Cada item usável na luta como a interface gráfica o desenha (ícone, quantidade, dica, se serve agora)."""
        j = self.j
        usaveis, armas = self.itens_da_luta()
        metas = [{"usar_item": k, "item": k, "qtd": j.consumiveis[k], "nome": CONSUMIVEIS[k]["nome"],
                  "desc": CONSUMIVEIS[k]["desc"],
                  "motivo": self.motivo_item(k)}
                 for k in usaveis]
        metas += [{"trocar": j.mochila.index(it), "equip": ficha(it, j.nome_recurso)} for it in armas]
        return metas

    def motivo_item(self, k):
        """Por que o item não serve agora, na luta (ou None). A bolsa do painel e o menu de itens dizem o mesmo."""
        if k == "pena_fenix":
            return PENA_FENIX_AGE_SOZINHA
        if k not in USAVEIS_EM_COMBATE:
            return "Isso não se usa no meio da luta."
        if k == "bomba_fumaca" or self.aliados_precisam(k):
            return None
        return self.g.motivo_inutil(k)

    def menu_itens(self):
        j = self.j
        usaveis, armas = self.itens_da_luta()
        if not usaveis and not armas:
            self.dizer("Sua bolsa não tem nada útil agora.", "cinza")
            return None
        opcoes = [f"{CONSUMIVEIS[k]['nome']} x{j.consumiveis[k]} — {CONSUMIVEIS[k]['desc']}" for k in usaveis]
        opcoes += [f"Trocar para {it['nome']} (gasta o turno)" for it in armas]
        metas = self.metas_itens()
        self.ui.meta_opcoes = metas + [None]
        try:
            esc = self.ui.escolher("Usar qual item?", opcoes + ["Voltar"])
        finally:
            self.ui.meta_opcoes = None
        if esc == len(opcoes):
            return None
        if esc >= len(usaveis):
            it = armas[esc - len(usaveis)]
            with self.agindo(j, "Troca de arma", hab="item"):
                self.g.equipar(it)
            return "turno"
        k = usaveis[esc]
        if k == "bomba_fumaca":
            if not self.pode_fugir:
                self.dizer("Não há como fugir desta luta!", "vermelho")
                return None
            j.consumiveis[k] -= 1
            self.dizer("Você estoura a bomba de fumaça e some na nuvem cinzenta!", "cinza")
            return "fuga"
        motivo = self.g.motivo_inutil(k)
        if k in EM_ALIADO:
            # Poção e bandagem também servem em quem luta ao seu lado (comitiva e animal); servos não.
            precisam = self.aliados_precisam(k)
            if precisam:
                quem = self.escolher_quem_trata(k, ([] if motivo else [j]) + precisam)
                if quem is None:
                    return None
                if quem is not j:
                    return self.tratar_aliado(k, quem)
                motivo = None
        if motivo:
            self.dizer(motivo, "cinza")
            return None
        with self.agindo(j, CONSUMIVEIS[k]["nome"], hab="item"):
            antes, antes_rec = j.hp, j.rec
            self.g.usar_consumivel(k)
            self.curou(j, j.hp - antes, rotulo=CONSUMIVEIS[k]["nome"])
            self.recuperou(j, j.rec - antes_rec, rotulo=CONSUMIVEIS[k]["nome"])
        return "turno"

    def aliados_precisam(self, k):
        """Quem luta ao seu lado (comitiva e animal; servos não) e precisa da poção ou da bandagem agora."""
        if k not in EM_ALIADO:
            return []
        return [a for a in self.aliados if a.vivo and a.tipo != "servo"
                and (a.hp < a.max_hp or (k == "bandagem" and a.efeito("sangramento")))]

    def escolher_quem_trata(self, k, candidatos):
        """Em quem usar a poção ou a bandagem. Na tela gráfica, as cartas acendem como na mira de um golpe."""
        self.ui.meta_opcoes = [{"alvo": self.uid(c)} for c in candidatos] + [{"voltar": True}]
        try:
            esc = self.ui.escolher(f"Em quem usar {CONSUMIVEIS[k]['nome']}?",
                                   [("Você" if c is self.j else c.nome) + f" ({c.hp}/{c.max_hp})" for c in candidatos]
                                   + ["Voltar"])
        finally:
            self.ui.meta_opcoes = None
        return candidatos[esc] if esc < len(candidatos) else None

    def tratar_aliado(self, k, a):
        j = self.j
        nome = CONSUMIVEIS[k]["nome"]
        j.consumiveis[k] -= 1
        telemetria.registrar(self.g, "consumivel", item=k, em_combate=True, em=getattr(a, "cid", None) or a.tipo)
        with self.agindo(j, nome, a, hab="item"):
            antes = a.hp
            if k == "pocao_vida":
                a.curar(a.max_hp * bal.POCAO_VIDA)
                self.dizer(f"Você joga a {nome} para {a.nome}, que bebe num gole. (+{a.hp - antes} vida)", "verde")
            else:
                estancou = a.efeito("sangramento")
                a.remover("sangramento")
                a.curar(bal.BANDAGEM_VIDA)
                self.dizer(f"Você enfaixa {a.nome} às pressas{', e o sangue para' if estancou else ''}. "
                           f"(+{a.hp - antes} vida)", "verde")
            self.curou(a, a.hp - antes, de=j, rotulo=nome)
        return "turno"

    def analisar(self):
        for e in self.inimigos_vivos():
            self.ui.separador()
            self.dizer(f"{e.nome} — Nível {e.nivel} — Vida {e.hp}/{e.max_hp}", "vermelho+negrito")
            if getattr(e, "nota", None):  # o que esta faz de diferente da espécie (a variante da capela)
                self.dizer(f"  ⚠ {e.nota}", "amarelo")
            for t in e.tracos:
                self.dizer(f"  • {TRACOS.get(t, t)}", "cinza")
            if not self.g.conhece(e.familia):
                self.dizer("  Fraquezas e habilidades: ??? (derrote mais destas criaturas para aprender)", "cinza")
                continue
            fracos = [k for k, v in e.resist.items() if v > 1]
            fortes = [k for k, v in e.resist.items() if v < 1]
            if fracos:
                self.dizer(f"  Fraco contra: {', '.join(fracos)}", "verde")
            if fortes:
                self.dizer(f"  Resiste a: {', '.join(fortes)}", "amarelo")
            if e.habilidades:
                self.dizer("  Habilidades: " + ", ".join(NOMES_HABS_INIMIGO.get(h, h) for h in e.habilidades), "cinza")
            if getattr(e, "chave", None) and self.g.flag(f"fraqueza:{e.chave}"):
                self.dizer("  Você conhece o ponto fraco desta criatura! (+25% de dano)", "verde+negrito")

    def tentar_fuga(self):
        vivos = self.inimigos_vivos()
        media = sum(e.agi for e in vivos) / len(vivos)
        chance = max(0.15, min(0.85, 0.5 + (self.j.agi - media) * 0.03))
        if any(f["id"] == "perna" for f in self.j.ferimentos):
            chance -= 0.2
        if self.rng.random() < chance:
            self.dizer("Você recua e consegue escapar!", "verde")
            comitiva.reagir(self.g, "fuga", forca=0.5)
            return True
        self.dizer(tx.concordar("Você tenta fugir, mas {eles} {corta o seu caminho|cercam você}!", vivos), "vermelho")
        return False
