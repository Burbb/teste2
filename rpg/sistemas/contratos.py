"""Contratos do mural: geração, caçada, recompensa, diário e abandono."""

from .. import texto as tx
from ..dados import BIOMAS, FAMILIAS, retrato
from .. import sobrevivencia
from ..mundo import distancias, nivel_regiao
from .. import balanceamento as bal


class Contratos:
    # Peso de cada lugar no mural conforme a diferença entre o nível dele e o seu:
    # quase sempre algo do seu tamanho, às vezes um desafio, raramente algo fácil.
    PESO_NIVEL_CONTRATO = bal.PESO_NIVEL_CONTRATO

    def recompensa_contrato(self, nivel, mult=1.0):
        """Ouro e XP crescem com o nível do CONTRATO (do lugar), não com o seu: um trabalho fácil paga pouco.
        O XP fica em torno de 1/8 do que falta para subir naquele nível, para não catapultar ninguém."""
        ouro = int((bal.CONTRATO_OURO_BASE + bal.CONTRATO_OURO_POR_NIVEL * nivel) * mult * self.rng.uniform(0.9, 1.2)
                   * bal.OURO_MUNDO)
        xp = int((bal.CONTRATO_XP_BASE + bal.CONTRATO_XP_FRACAO * bal.xp_para_subir(nivel)) * mult)
        return ouro, xp

    def lugar_para_contrato(self, selvagens):
        h = self.j.nivel
        pesos = [self.PESO_NIVEL_CONTRATO.get(nivel_regiao(l) - h, 0) for l in selvagens]
        if any(pesos):
            return self.rng.choices(selvagens, weights=pesos)[0]
        perto = min(abs(nivel_regiao(l) - h) for l in selvagens)
        return self.sortear([l for l in selvagens if abs(nivel_regiao(l) - h) == perto])

    def gerar_contrato(self):
        j = self.j
        selvagens = [l for l in self.mundo["locais"] if l["tipo"] in ("selvagem", "covil")]
        vilas = [l for l in self.mundo["locais"] if l["tipo"] == "vila" and l["id"] != self.loc["id"]]
        tipo = self.sortear(["caca", "caca", "alvo", "alvo", "entrega"])
        cid = self.novo_id()
        if tipo == "entrega" and vilas:
            dist = distancias(self.mundo["locais"], self.loc["id"])
            dest = self.sortear(vilas)
            ouro, xp = self.recompensa_contrato(j.nivel, 0.5 + 0.12 * dist.get(dest["id"], 2))
            objeto = self.sortear(["um baú lacrado", "uma carta com selo de cera negra", "um frasco de remédio",
                                   "um embrulho que se mexe às vezes", "as escrituras de uma fazenda",
                                   "um anel de noivado"])
            return {"id": cid, "tipo": "entrega", "destino": dest["id"], "objeto": objeto, "ouro": ouro, "xp": xp,
                    "desc": f"Levar {objeto} até {dest['nome']}."}
        loc = self.lugar_para_contrato(selvagens)
        nv = nivel_regiao(loc)  # só bichos que de fato aparecem por lá
        fam = self.sortear([f for f in BIOMAS[loc["bioma"]]["familias"] if FAMILIAS[f].get("nivel_min", 1) <= nv]
                           or BIOMAS[loc["bioma"]]["familias"])
        f = FAMILIAS[fam]
        if tipo == "alvo":
            nome = tx.nome_proprio(self.rng)
            ouro, xp = self.recompensa_contrato(nv, 1.4)
            return {"id": cid, "tipo": "alvo", "local": loc["id"], "familia": fam, "nome": nome,
                    "chave": f"alvo:{cid}", "ouro": ouro, "xp": xp,
                    "desc": f"Caçar {nome}, {tx.artigo(f['g'], False)} {f['nome']} enorme que aterroriza "
                            f"{loc['nome']}."}
        total = self.rng.randint(2, 4)
        ouro, xp = self.recompensa_contrato(nv, 0.7 + 0.15 * total)
        return {"id": cid, "tipo": "caca", "local": loc["id"], "familia": fam, "total": total, "feito": 0,
                "ouro": ouro, "xp": xp, "desc": f"Eliminar {total} {f['plural']} em {loc['nome']}."}

    def mural(self):
        vid = str(self.loc["id"])
        oferta = self.ofertas.get(vid)
        if not oferta or self.dia - oferta["dia"] >= 3:
            oferta = {"dia": self.dia, "lista": [self.gerar_contrato() for _ in range(3)]}
            self.ofertas[vid] = oferta
        while True:
            self.ui.cena("Mural de contratos", f"{self.loc['nome']} · contratos ativos: {len(self.contratos)}/3", "menu")
            if self.ui.painel("mural", self.dados_mural(oferta)):
                if self._mural_web(oferta):
                    return
                continue
            opcoes = [(f"{c['desc']} (recompensa: {c['ouro']} ouro, {c['xp']} XP)", c) for c in oferta["lista"]]
            c = self.menu("Aceitar qual contrato?", opcoes + [("Voltar", None)])
            if not c:
                return
            self.aceitar_contrato(c, oferta)

    def aceitar_contrato(self, c, oferta):
        """Tira o contrato do mural e o põe no diário (no máximo 3). True se aceitou."""
        if len(self.contratos) >= 3:
            self.dizer("Você já tem contratos demais. Termine ou abandone um antes.", "vermelho")
            return False
        oferta["lista"].remove(c)
        self.contratos.append(c)
        self.ui.efeito("Contrato aceito", "info")
        if c["tipo"] == "alvo":
            self.marcar(f"conhecido:{c['local']}")
        if c["tipo"] == "entrega":
            self.plantar("pacote_suspeito", 3, contrato=c["id"])
        return True

    def cartao_contrato(self, c):
        """Um contrato como cartão do mural: tipo, alvo, lugar, distância, recompensa e progresso."""
        locais = self.mundo["locais"]
        lugar = locais[c["destino"] if c["tipo"] == "entrega" else c["local"]]
        dist = distancias(locais, self.loc["id"]).get(lugar["id"])
        f = FAMILIAS.get(c.get("familia"), {})
        progresso = (f"{c.get('feito', 0)}/{c['total']}" if c["tipo"] == "caca" else
                     "abatido" if c.get("concluido") else None)
        return {"id": c["id"], "tipo": c["tipo"], "desc": c["desc"], "ouro": c["ouro"], "xp": c["xp"],
                "lugar": lugar["nome"], "lugar_id": lugar["id"], "lugar_tipo": lugar["tipo"], "bioma": lugar["bioma"], "distancia": dist,
                "nivel": None if lugar["tipo"] == "vila" else nivel_regiao(lugar),
                "alvo": c.get("nome"), "familia": c.get("familia"), "familia_nome": f.get("nome"),
                "tracos": f.get("tracos", []), "retrato": retrato(f.get("tracos", [])), "objeto": c.get("objeto"),
                "progresso": progresso,
                "concluido": bool(c.get("concluido")), "penalidade": 6 if c["tipo"] == "entrega" else 3}

    def dados_mural(self, oferta):
        return {"oferta": [self.cartao_contrato(c) for c in oferta["lista"]],
                "ativos": [self.cartao_contrato(c) for c in self.contratos], "limite": 3,
                "renova": max(0, 3 - (self.dia - oferta["dia"])), "nivel_heroi": self.j.nivel}

    def _mural_web(self, oferta):
        """Mural na interface web: aceitar e abandonar são cliques nos cartões. True = sair."""
        opcoes = [(f"Aceitar: {c['desc']}", ("aceitar", c), {"aceitar": c["id"]}) for c in oferta["lista"]]
        opcoes += [(f"Abandonar: {c['desc']}", ("abandonar", c), {"abandonar": c["id"]})
                   for c in self.contratos if not c.get("concluido")]
        op = self.menu("", opcoes + [("Voltar", None, {"voltar": True})])
        if op is None:
            return True
        acao, c = op
        if acao == "abandonar":
            self.abandonar_contrato(c)
        else:
            self.aceitar_contrato(c, oferta)
        return False

    REPUTACAO_CONTRATO = 3

    def receber_contratos(self):
        """Ao chegar numa vila: os contratos cumpridos pagam. Na tela gráfica, todos de uma vez, num quadro com os
        cartazes carimbados e o total (o pagamento é um momento, não uma enxurrada de linhas no registro)."""
        feitos = [c for c in self.contratos
                  if c.get("concluido") or (c["tipo"] == "entrega" and c["destino"] == self.loc["id"])]
        if not feitos:
            return
        festa = self.ui.conquistas_na_tela
        if festa:
            self.ui.celebrar("contratos", {
                "contratos": [dict(self.cartao_contrato(c), concluido=True) for c in feitos],
                "ouro": sum(c["ouro"] for c in feitos), "xp": sum(c["xp"] for c in feitos),
                "reputacao": min(50 - self.j.reputacao, self.REPUTACAO_CONTRATO * len(feitos))})
        for c in feitos:
            self.contratos.remove(c)
            if not festa:
                self.dizer(f"Recompensa de contrato: {c['desc']}", "verde+negrito")
            self.ganhar_ouro(c["ouro"], exato=True, avisar=not festa, fonte="contratos")
            self.mudar_reputacao(self.REPUTACAO_CONTRATO, avisar=not festa)
            self.ganhar_xp(c["xp"], avisar=not festa)

    def contratos_aqui(self):
        """Contratos de caça (bando ou alvo nomeado) ainda abertos neste lugar."""
        return [c for c in self.contratos if c["tipo"] in ("caca", "alvo") and c["local"] == self.loc["id"]
                and not c.get("concluido")]

    PISTAS = [
        "Pegadas frescas na lama, fundas e espaçadas", "Tufos de pelo presos nos espinhos",
        "Uma carcaça roída, ainda morna", "Galhos quebrados na altura do peito",
        "Fezes recentes e o cheiro forte de bicho", "Marcas de garras numa árvore caída",
    ]

    def cacar(self, c):
        """Caçada de contrato: quem foi contratado sabe o que procura. Seguir os rastros sempre leva ao alvo;
        a Percepção decide quem vê quem primeiro. Custa um período, como explorar."""
        f = FAMILIAS[c["familia"]]
        self.ui.cena("Caçada", self.contexto_cena(), "evento")
        sobrevivencia.acender_tocha(self)
        try:
            pista = self.sortear(self.PISTAS)
            if c["tipo"] == "alvo":
                e = self.inimigo(c["familia"], afixo="anciao", nome_unico=c["nome"], bonus=1)
                e.chave = c["chave"]
                self.narrar(f"{pista}. Grandes demais para {tx.artigo(f['g'], False)} {f['nome']} comum. "
                            f"Você segue a trilha até a toca e lá está: {e.nome}.", "amarelo")
                grupo = [e]
            else:
                restam = c["total"] - c["feito"]
                lo, hi = f["grupo"]
                n = max(1, min(restam, hi, self.rng.randint(1, 2)))
                self.narrar(f"{pista}. Rastros de {f['plural']}, como o mural descreveu. Você segue a trilha.",
                            "amarelo")
                grupo = self.grupo(c["familia"], n=n)
            if self.teste("percepcao", 12):
                self.dizer(tx.concordar("Você {os} vê antes que {eles} te {veja|vejam}. O primeiro golpe é seu.",
                                        grupo), "verde")
                self.combate(grupo, emboscada="jogador")
            else:
                self.dizer(tx.concordar("Um galho estala sob o seu pé. {Eles} se {vira|viram}{| ao mesmo tempo}.",
                                        grupo), "vermelho")
                self.combate(grupo)
        finally:
            self.sem_luz = False
        self.avancar_periodo()
        self.pausar()

    def contrato_alvo_aqui(self):
        for c in self.contratos:
            if c["tipo"] == "alvo" and c["local"] == self.loc["id"] and not c.get("concluido"):
                return c
        return None

    def diario(self):
        while True:
            self.ui.cena("Diário", f"dia {self.dia}", "menu")
            a = self.antagonista
            n = self.nemesis
            dados = {
                "antagonista": {"nome": a["nome"], "origem": a["origem"]} if a else None,
                "sigilos": len(self.j.sigilos),
                "dia": self.dia,
                "contratos": [self.cartao_contrato(c) for c in self.contratos], "limite": 3,
                "nivel_heroi": self.j.nivel,
                "rumores": [{"texto": r["texto"], "expira": r["expira"] - self.dia} for r in self.rumores],
                "nemesis": {"nome": n["nome"], "familia": FAMILIAS[n["familia"]]["nome"]} if n else None,
            }
            web = self.ui.painel("diario", dados)
            if not web:
                self._diario_texto(a)
            pendentes = [c for c in self.contratos if not c.get("concluido")]
            if not pendentes and not web:
                self.pausar()
                return
            c = self.menu("", [(f"Abandonar: {c['desc']}", c, {"abandonar": c["id"]}) for c in pendentes] +
                          [("Fechar o diário", None, {"voltar": True})])
            if not c:
                return
            self.abandonar_contrato(c)

    def _diario_texto(self, a):
        if a:  # a campanha escrita ainda não tem vilão
            self.dizer(f"Inimigo final: {a['nome']}, {a['origem']}.", "magenta")
        self.dizer(f"Sigilos: {len(self.j.sigilos)}/3   Dia {self.dia}", "magenta")
        self.dizer("Contratos:", "ciano")
        if not self.contratos:
            self.dizer("  nenhum", "cinza")
        for c in self.contratos:
            prog = f" ({c['feito']}/{c['total']})" if c["tipo"] == "caca" else ""
            estado = " — CONCLUÍDO, receba numa vila" if c.get("concluido") else ""
            self.dizer(f"  • {c['desc']}{prog}{estado}")
        self.dizer("Rumores:", "ciano")
        if not self.rumores:
            self.dizer("  nenhum", "cinza")
        for r in self.rumores:
            self.dizer(f"  • {r['texto']}")
        if self.nemesis:
            n = self.nemesis
            self.dizer(f"Nêmesis: {n['nome']}, {FAMILIAS[n['familia']]['nome']} que te persegue.", "vermelho")

    def abandonar_contrato(self, c):
        penalidade = 6 if c["tipo"] == "entrega" else 3
        # Pergunta curta (vira o rótulo dos botões, em vez de um aviso solto por cima deles); a consequência da
        # entrega vai no próprio botão.
        sim = ("Sim: fico com a encomenda (viro ladrão aos olhos de todos)" if c["tipo"] == "entrega"
               else "Sim, abandonar")
        if not self.confirmar(f"Abandonar este contrato? (reputação −{penalidade})", [(sim, True), ("Não", False)],
                              perigo=True):
            return
        self.contratos.remove(c)
        self.dizer("Você risca o contrato do diário. Alguém, em algum lugar, vai saber que você desistiu.", "cinza")
        self.mudar_reputacao(-penalidade)
