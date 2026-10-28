"""A vez do herói: atacar, habilidades, itens (em você ou em quem luta ao seu lado), analisar e fugir."""

from .. import texto as tx
from ..classes import CLASSES
from ..habilidades import custo_flechas, descricao_habilidade, efetiva, versao
from ..modificadores import disparar, nomes
from ..forja import fracao
from ..forja.fracao import mod_pontos
from ..dados import TRACOS
from ..inimigos import NOMES_HABS_INIMIGO
from ..itens import CONSUMIVEIS, EM_ALIADO, PENA_FENIX_AGE_SOZINHA, USAVEIS_NA_LUTA, descricao, ficha
from .. import abertura, comitiva, telemetria
from ..talentos import custo_habilidade
from .. import balanceamento as bal

USAVEIS_EM_COMBATE = USAVEIS_NA_LUTA  # o catálogo diz (itens.py: luta)


def _tipo_dano(h):
    """O tipo do primeiro golpe da habilidade (físico, fogo, arcano...), para a carta dizer; None se não fere."""
    from ..habilidades import Dano, blocos
    d = next((p for p in blocos(h) if isinstance(p, Dano)), None)
    return d.tipo if d else None


class AcoesDoHeroi:
    # ------------------------------------------------------------ jogador
    def fase_jogador(self):
        j = self.j
        fracao.tique(j)  # a cura por turno de peças reforçadas acumula a fração (forja/fracao.py)
        self.mostrar_estado()
        if mod_pontos(j, "regen_vida") and j.hp < j.max_hp:  # discreta na tela: o número e a barra, sem pausa
            self.curou(j, j.curar(mod_pontos(j, "regen_vida")), tipo="discreto", conta=False,
                       rotulo=(nomes(j, "regen_vida") or ["Regeneração"])[0])
        if self.processar_efeitos(j) or not j.vivo:
            return None
        while True:
            nome_atk = CLASSES[j.classe]["ataque"][0]
            if j.classe == "arqueiro" and j.flechas <= 0:
                nome_atk = "Golpe de Adaga — sem flechas!"
            analisar = self.ui.analisar_no_menu
            # Atacar, Defender e Usar item são comandos de toda vez, fora do kit (kit.py); as habilidades são as do kit.
            ids = ["atacar", "defender", "habilidades", "itens"] + (["analisar"] if analisar else [])
            opcoes = [f"Atacar ({nome_atk})", "Defender", "Habilidades", "Itens"] + (["Analisar inimigos"] if analisar else [])
            # Na tela gráfica as ações viram uma barra dentro da arena, com as habilidades já à mostra.
            metas = [{"acao": "atacar", "nome": nome_atk}, {"acao": "defender", "valor": bal.DEFENDER},
                     {"acao": "habilidades", "habilidades": self.metas_habilidades()},
                     {"acao": "itens", "itens": self.metas_itens()}] + ([{"acao": "analisar"}] if analisar else [])
            if self.pode_fugir:
                ids.append("fugir")
                opcoes.append("Fugir")
                metas.append({"acao": "fugir"})
            for m in metas:
                m["ator"] = "j"
            self.ui.meta_opcoes = metas
            selo = abertura.selo_da_vez(self.g)  # um selo novo numa carta (a orientação dele passa com a ação)
            abertura.dica_texto(self.g, "selo")
            try:
                esc = self.ui.escolher("Sua ação:", opcoes)
            finally:
                self.ui.meta_opcoes = None
            if selo:
                abertura.visto(self.g, selo["id"])
            acao = ids[esc]
            if acao == "atacar":
                alvo = self.escolher_alvo(cancelavel=True)
                if alvo is None:
                    continue
                self.ataque_basico(alvo)
                return None
            if acao == "defender":
                self.defender(j)
                return None
            if acao == "habilidades":
                if self.menu_habilidades():
                    return None
            elif acao == "itens":
                r = self.menu_itens()
                if r == "fuga":
                    return "fuga"
                if r:
                    return None
            elif acao == "analisar":
                self.analisar()
            elif acao == "fugir":
                return "fuga" if self.tentar_fuga() else None

    def defender(self, u):
        """Defender: −40% de dano até o começo da próxima vez de quem defende (o estado dura 1 turno dele)."""
        with self.agindo(u, "Defender", hab="defender", anim="falange"):
            u.aplicar("defendendo", 1, bal.DEFENDER)
            self.lance("buff", em=self.uid(u), efeitos=["defendendo"], rotulo="Defendendo", hab="defender")
            self.detalhe(f"{self.nome(u)} se defende: dano recebido −{round(bal.DEFENDER * 100)}% até a próxima vez.",
                         "ciano")

    def escolher_aliado(self, u, incluir_si=True, cancelavel=True, caidos=False):
        """Em quem a habilidade ou o item de apoio age: você e a comitiva (os caídos, com caidos=True)."""
        todos = [self.j] + [a for a in self.aliados if a.tipo == "comitiva"]
        if caidos:
            cands = [a for a in todos if not a.vivo]
        else:
            cands = [a for a in todos if a.vivo and (incluir_si or a is not u)]
        if not cands:
            return None
        self.ui.meta_opcoes = [{"alvo": self.uid(c)} for c in cands] + ([{"voltar": True}] if cancelavel else [])
        try:
            esc = self.ui.escolher("Em quem?", [("Você" if c is self.j else c.nome) + f" ({c.hp}/{c.max_hp})"
                                               for c in cands] + (["Voltar"] if cancelavel else []))
        finally:
            self.ui.meta_opcoes = None
        return cands[esc] if esc < len(cands) else None

    def caidos_da_comitiva(self):
        return [a for a in self.aliados if a.tipo == "comitiva" and not a.vivo]

    def reerguer(self, u, alvo, rotulo, fracao, item=None):
        """Ressurreição na luta (a Pena de Fênix num companheiro, o Reerguer de Odette): volta com uma fração da vida,
        na mesma posição da ordem; se a vez dele já passou nesta rodada, só age na próxima. Sem recuperar a vez."""
        if item:
            self.j.consumiveis[item] -= 1
            telemetria.registrar(self.g, "consumivel", item=item, em_combate=True, em=getattr(alvo, "cid", None))
        with self.agindo(u, rotulo, alvo, hab="item" if item else "reerguer"):
            alvo.hp = max(1, round(alvo.max_hp * fracao))
            alvo.limpar_negativos()
            self.curou(alvo, alvo.hp, tipo="levantar", de=u, rotulo=rotulo)
            self.dizer(f"{alvo.nome} se levanta com {alvo.hp} de vida.", "amarelo+negrito")
        return "turno"

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
                self.ui.atualizar()  # a flecha sai da aljava junto do disparo (como o custo das habilidades)
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
        j = self.j
        h = efetiva(j, h_id)
        if h.get("ultimate") and "j" in self.ultimates_usadas:
            return "Ultimate já usada nesta luta"
        if h["alvo"] == "aliado" and not any(a.vivo and a.tipo == "comitiva" for a in self.aliados):
            return "Ninguém para proteger"
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
        for h_id in j.kit:
            h = efetiva(j, h_id)  # a versão que o herói escolheu levar (E6); o id do botão continua o mesmo
            motivo = self.motivo_bloqueio(h_id)
            v = versao(j, h_id)
            metas.append({"habilidade": h_id, "nome": h["nome"], "icone": h["icone"], "familia": h["familia"],
                          "custo": custo_habilidade(j, h_id),
                          "recurso": j.nome_recurso, "flechas": self.flechas_de(h), "alvo_tipo": h["alvo"],
                          "desc": descricao_habilidade(h_id, j), "pode": motivo is None, "motivo": motivo,
                          "ultimate": bool(h.get("ultimate")), "tipo": _tipo_dano(h),
                          **({"variante": v} if v != h_id else {})})  # só na transformada: quem não tem, igual
        return metas

    def menu_habilidades(self):
        j = self.j
        ids = list(j.kit)
        opcoes = []
        for h_id in ids:
            h = efetiva(j, h_id)
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
        h = efetiva(j, ids[esc])
        h_ef = versao(j, ids[esc])  # o id da versão usada: a telemetria separa a Lança da Prisão
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
        elif h["alvo"] == "aliado":
            alvo = self.escolher_aliado(j, incluir_si=False)
            if alvo is None:
                return False
        if h.get("ultimate"):
            self.ultimates_usadas.add("j")
        j.rec -= custo
        self.habilidades_usadas += 1
        self.tel["habilidades"][h_ef] = self.tel["habilidades"].get(h_ef, 0) + 1
        self.tel["rec_gasto"] += custo
        flechas = self.flechas_de(h)
        j.flechas -= flechas
        self.flechas_gastas += flechas
        # O custo aparece já, junto do começo da ação: sem isto, a tela só via o recurso pago no próximo estado (depois
        # do texto do golpe, ou do fim de uma salva em área), e uma cura da própria habilidade podia vir antes dele.
        self.ui.atualizar()
        with self.agindo(j, h["nome"], alvo, area=h["alvo"] == "todos", hab=h_ef, anim=h.get("anim")):
            antes, self._cura_j = j.hp, 0
            efeitos_antes = {k: dict(v) for k, v in j.efeitos.items()}
            h["fn"](self, j, alvo)
            self.curou(j, j.hp - antes - self._cura_j, rotulo=h["nome"])
            # Buffs em si mesmo (grito, escudo, esquiva, sombras) também viram um lance: a tela anima e espera.
            novos = [k for k, v in j.efeitos.items() if efeitos_antes.get(k) != v]
            if novos:
                self.lance("buff", em="j", efeitos=novos, rotulo=h["nome"], hab=h_ef,
                           **({"anim": h["anim"]} if h.get("anim") else {}))
        return True

    def itens_da_luta(self):
        """Consumíveis que servem em luta e armas (ou escudo/aljava/grimório) da mochila para trocar.
        Trocar de arma gasta o turno; armadura não: ninguém veste uma cota de malha com um lobo no pescoço."""
        j = self.j
        usaveis = [k for k in USAVEIS_EM_COMBATE if j.consumiveis.get(k, 0) > 0]
        if j.consumiveis.get("pena_fenix", 0) > 0 and "pena_fenix" not in usaveis and self.caidos_da_comitiva():
            usaveis.append("pena_fenix")  # num companheiro caído (em você, ela age sozinha)
        armas = [it for it in j.mochila if it["slot"] in ("arma", "secundaria") and self.g.pode_usar(it)]
        return usaveis, armas

    def metas_itens(self):
        """Cada item usável na luta como a interface gráfica o desenha (ícone, quantidade, dica, se serve agora)."""
        j = self.j
        usaveis, armas = self.itens_da_luta()
        metas = [{"usar_item": k, "item": k, "qtd": j.consumiveis[k], "nome": CONSUMIVEIS[k]["nome"],
                  "desc": descricao(k, j),
                  "motivo": self.motivo_item(k)}
                 for k in usaveis]
        metas += [{"trocar": j.mochila.index(it), "equip": ficha(it, j.nome_recurso)} for it in armas]
        return metas

    def motivo_item(self, k):
        """Por que o item não serve agora, na luta (ou None). A bolsa do painel e o menu de itens dizem o mesmo."""
        if k == "pena_fenix":
            # num companheiro caído, usa-se (gasta a vez); em você, ela age sozinha quando você cai
            return None if self.caidos_da_comitiva() else PENA_FENIX_AGE_SOZINHA
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
        opcoes = [f"{CONSUMIVEIS[k]['nome']} x{j.consumiveis[k]} — {descricao(k, j)}" for k in usaveis]
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
        if k == "pena_fenix":
            quem = self.escolher_aliado(j, caidos=True)
            if quem is None:
                return None
            return self.reerguer(j, quem, "Pena de Fênix", bal.PENA_COMPANHEIRO, item="pena_fenix")
        if k == "bomba_fumaca":
            if not self.pode_fugir:
                self.dizer("Não há como fugir desta luta!", "vermelho")
                return None
            j.consumiveis[k] -= 1
            self.dizer("Você estoura a bomba de fumaça e some na nuvem cinzenta!", "cinza")
            return "fuga"
        motivo = self.g.motivo_inutil(k)
        if k in EM_ALIADO:
            # A poção também serve em quem luta ao seu lado (comitiva e animal); servos não.
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
        """Quem luta ao seu lado (comitiva e animal; servos não) e precisa da poção agora."""
        if k not in EM_ALIADO:
            return []
        return [a for a in self.aliados if a.vivo and a.tipo != "servo" and a.hp < a.max_hp]

    def escolher_quem_trata(self, k, candidatos):
        """Em quem usar a poção. Na tela gráfica, as cartas acendem como na mira de um golpe."""
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
            a.curar(a.max_hp * bal.POCAO_VIDA)
            self.dizer(f"Você joga a {nome} para {a.nome}, que bebe num gole. (+{a.hp - antes} vida)", "verde")
            self.curou(a, a.hp - antes, de=j, rotulo=nome)
        return "turno"

    # ------------------------------------------------------------ a vez de um companheiro (etapa 4)
    def motivo_comitiva(self, a, h):
        if h.get("uma_vez") and (a.cid, h["id"]) in self.ultimates_usadas:
            return "Já usada nesta luta"
        if h["alvo"] == "aliado_caido" and not self.caidos_da_comitiva():
            return "Ninguém caído"
        if h["alvo"] == "aliado" and h["id"] == "proteger" and not [c for c in [self.j] + self.aliados
                                                                   if c.vivo and c is not a and (c is self.j or c.tipo == "comitiva")]:
            return "Ninguém para proteger"
        if a.rec < h["custo"]:
            return f"{a.nome_recurso} insuficiente"
        return None

    def metas_comitiva(self, a):
        return [{"habilidade": h["id"], "nome": h["nome"], "icone": h["icone"], "familia": h["familia"],
                 "custo": h["custo"], "recurso": a.nome_recurso, "flechas": 0, "alvo_tipo": h["alvo"], "desc": h["desc"],
                 "pode": self.motivo_comitiva(a, h) is None, "motivo": self.motivo_comitiva(a, h)}
                for h in comitiva.KITS.get(a.cid, [])]

    def vez_comitiva(self, a):
        """Você escolhe a ação do companheiro: Atacar, Defender, Usar item (a bolsa do grupo) ou o kit dele."""
        nome_atk, mult, tipo, alcance, stat = comitiva.ATAQUE[a.cid]
        while True:
            ids = ["atacar", "defender", "habilidades", "itens"]
            opcoes = [f"{a.nome}: Atacar ({nome_atk})", "Defender", "Habilidades", "Itens"]
            metas = [{"acao": "atacar", "nome": nome_atk}, {"acao": "defender", "valor": bal.DEFENDER},
                     {"acao": "habilidades", "habilidades": self.metas_comitiva(a)},
                     {"acao": "itens", "itens": self.metas_itens_comitiva()}]
            for m in metas:
                m["ator"] = self.uid(a)
            self.ui.meta_opcoes = metas
            try:
                acao = ids[self.ui.escolher(f"Vez de {a.nome}:", opcoes)]
            finally:
                self.ui.meta_opcoes = None
            if acao == "atacar":
                alvo = self.escolher_alvo(cancelavel=True)
                if alvo is None:
                    continue
                with self.agindo(a, nome_atk, alvo, hab="ataque"):
                    self.atacar(a, alvo, mult, tipo=tipo, alcance=alcance, stat=stat, rotulo=a.nome)
                    comitiva.gritar(self, a, "ataque", 0.15)
                return
            if acao == "defender":
                self.defender(a)
                return
            if acao == "habilidades":
                if self.menu_comitiva(a):
                    return
            elif acao == "itens":
                if self.itens_comitiva(a):
                    return

    def menu_comitiva(self, a):
        kit = comitiva.KITS.get(a.cid, [])
        self.ui.meta_opcoes = self.metas_comitiva(a) + [None]
        try:
            esc = self.ui.escolher(f"Habilidades de {a.nome}:",
                                   [f"{h['nome']} [{h['custo']} {a.nome_recurso}] — {h['desc']}" for h in kit] + ["Voltar"])
        finally:
            self.ui.meta_opcoes = None
        if esc >= len(kit):
            return False
        h = kit[esc]
        motivo = self.motivo_comitiva(a, h)
        if motivo:
            self.dizer(motivo + ".", "cinza")
            return False
        alvo = a
        if h["alvo"] == "inimigo":
            alvo = self.escolher_alvo(cancelavel=True)
        elif h["alvo"] == "aliado":
            alvo = self.escolher_aliado(a, incluir_si=h["id"] != "proteger")
        elif h["alvo"] == "aliado_caido":
            alvo = self.escolher_aliado(a, caidos=True)
        if alvo is None:
            return False
        a.rec -= h["custo"]
        if h.get("uma_vez"):
            self.ultimates_usadas.add((a.cid, h["id"]))
        self.ui.atualizar()
        with self.agindo(a, h["nome"], alvo if alvo is not a else None, hab=f"{a.cid}:{h['id']}"):
            h["fn"](self, a, alvo)
        return True

    def metas_itens_comitiva(self):
        j = self.j
        lista = []
        for k in ("pocao_vida", "pena_fenix"):
            if j.consumiveis.get(k, 0) > 0:
                motivo = None
                if k == "pena_fenix" and not self.caidos_da_comitiva():
                    motivo = "Ninguém caído"
                elif k == "pocao_vida" and not [c for c in [j] + self.aliados if c.vivo and c.hp < c.max_hp
                                                  and (c is j or c.tipo == "comitiva")]:
                    motivo = "Ninguém ferido"
                lista.append({"usar_item": k, "item": k, "qtd": j.consumiveis[k], "nome": CONSUMIVEIS[k]["nome"],
                              "desc": descricao(k, j), "motivo": motivo})
        return lista

    def itens_comitiva(self, a):
        """O companheiro usa um item da bolsa do grupo: a poção em alguém de pé, a Pena num caído."""
        metas = self.metas_itens_comitiva()
        if not metas:
            self.dizer("A bolsa não tem nada que sirva agora.", "cinza")
            return False
        self.ui.meta_opcoes = metas + [None]
        try:
            esc = self.ui.escolher("Usar qual item?", [f"{m['nome']} x{m['qtd']}" for m in metas] + ["Voltar"])
        finally:
            self.ui.meta_opcoes = None
        if esc >= len(metas) or metas[esc]["motivo"]:
            return False
        k = metas[esc]["item"]
        if k == "pena_fenix":
            quem = self.escolher_aliado(a, caidos=True)
            if quem is None:
                return False
            self.reerguer(a, quem, "Pena de Fênix", bal.PENA_COMPANHEIRO, item="pena_fenix")
            return True
        quem = self.escolher_aliado(a)
        if quem is None:
            return False
        self.j.consumiveis[k] -= 1
        with self.agindo(a, CONSUMIVEIS[k]["nome"], quem, hab="item"):
            antes = quem.hp
            quem.curar(quem.max_hp * bal.POCAO_VIDA)
            self.curou(quem, quem.hp - antes, de=a, rotulo=CONSUMIVEIS[k]["nome"])
        return True

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
            self.lance("fuga_heroi", de="j", ok=True)  # a tela mostra a retirada (a carta sai, um som curto)
            self.dizer("Você recua e consegue escapar!", "verde")
            comitiva.reagir(self.g, "fuga", forca=0.5)
            return True
        self.lance("fuga_heroi", de="j", ok=False)  # cercado: a carta recua e volta
        self.dizer(tx.concordar("Você tenta fugir, mas {eles} {corta o seu caminho|cercam você}!", vivos), "vermelho")
        return False
