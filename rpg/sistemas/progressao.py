"""Níveis, talentos, habilidades, especialização e companheiro animal."""

from .. import abertura
from .. import atributos as atr
from .. import balanceamento as bal
from .. import kit as kits
from ..classes import CLASSES, COMPANHEIROS, SPECS, habilidades_ate
from ..habilidades import HABILIDADES, efetiva, escolher_versao, ficha, transformacoes, versao
from ..entidades import NOMES_STATS
from .. import comitiva
from .. import especializacao
from .. import talentos
from .. import telemetria
from .. import texto as tx
from ..telemetria import registrar


class Progressao:
    # ================================================================ progressão
    def subir_nivel(self):
        j = self.j
        j.nivel += 1
        cresc = dict(CLASSES[j.classe]["cresc"])
        if j.spec:
            for k, v in SPECS[j.spec]["cresc"].items():
                cresc[k] = cresc.get(k, 0) + v
        antes_hp, antes_rec = j.max_hp, j.max_rec
        antes = {k: getattr(j, k) for k in ("max_hp", "max_rec", "atk", "defesa", "agi", "poder")}
        for k, v in cresc.items():
            j.base[k] += v * bal.HEROI_CRESCIMENTO
        if j.nivel % atr.PRESENCA_A_CADA == 0:
            j.presenca = atr.presenca(j) + 1  # a Presença sobe sozinha (fora da luta; o sistema social é outra etapa)
        j.pontos_atributo += atr.PONTOS_POR_NIVEL  # distribuídos fora da luta, como os de talento
        if getattr(self, "atributos_pela_classe", False):  # os níveis de teste (dev.subir_ate): sem perguntar
            self.distribuir_pela_classe()
        j.recalcular()
        j.hp = min(j.max_hp, j.hp + max(0, j.max_hp - antes_hp))  # só ganha o que o máximo aumentou
        for m in comitiva.membros(self) + comitiva.reserva(self):  # 1 ponto livre por nível para cada um (ficha.py)
            comitiva.ficha.preparar(m, j.nivel - 1)["pontos_atributo"] += comitiva.ficha.PONTOS_POR_NIVEL
        comitiva.atualizar_vida_maxima(self)
        j.rec = min(j.max_rec, j.rec + max(0, j.max_rec - antes_rec))
        registrar(self, "nivel", stats=telemetria.instantaneo(j), fontes=telemetria.fontes_poder(self),
                  poder_equip=telemetria.poder_equip(j))
        if j.companheiro:
            j.companheiro["max_hp"] += bal.ANIMAL_VIDA_SUBIR
            j.companheiro["atk"] += bal.ANIMAL_ATK_SUBIR
            j.companheiro["hp"] = j.companheiro["max_hp"]
        # Na tela gráfica, a festa do nível diz tudo (atributos, ponto de talento, habilidades novas): o texto não
        # repete. No texto, as linhas são a festa.
        festa = self.ui.conquistas_na_tela
        if not festa:
            self.ui.titulo(f"NÍVEL {j.nivel}!", "verde+negrito")
            self.dizer("Você se sente mais forte.", "verde")
        self.ganhar_ponto_talento(anunciar=not festa)
        if not festa and j.pontos_atributo:
            self.dizer(f"+{atr.PONTOS_POR_NIVEL} pontos de atributo (distribua em \"Atributos\": você tem "
                       f"{j.pontos_atributo}).", "amarelo+negrito")
        novas = self._aprender_habilidades(anunciar=not festa)
        ganhos = {NOMES_STATS.get(k, k) if k != "max_rec" else j.nome_recurso: getattr(j, k) - v
                  for k, v in antes.items() if getattr(j, k) > v}
        self.ui.celebrar("nivel", {"nivel": j.nivel, "ganhos": ganhos, "pontos": j.pontos_talento,
                                   "pontos_atributo": j.pontos_atributo,
                                   "habilidades": [{"nome": HABILIDADES[h]["nome"], "desc": HABILIDADES[h]["desc"],
                                                    "icone": HABILIDADES[h]["icone"]} for h in novas],
                                   "especializacao": j.nivel >= bal.NIVEL_ESPECIALIZACAO and not j.spec})
        if j.nivel >= bal.NIVEL_ESPECIALIZACAO and not j.spec and f"encruzilhada_{j.classe}" not in self.forcados:
            self.forcados.append(f"encruzilhada_{j.classe}")
            if not festa:
                self.dizer("Você sente que uma encruzilhada se aproxima. Talvez ela venha na próxima noite de "
                           "descanso...", "magenta")

    # ================================================================ atributos (etapa 4)
    def distribuir_pela_classe(self):
        """Gasta os pontos de atributo pela preferência da classe (os níveis de teste e o robô da arena)."""
        j = self.j
        for a in atr.distribuir_sozinho(j.classe, j.pontos_atributo, j.atributos):
            if j.atributos[a] < atr.ATRIBUTO_MAX:
                j.atributos = dict(j.atributos, **{a: j.atributos[a] + 1})
        j.pontos_atributo = 0
        j.recalcular()

    def motivo_atributo(self, a):
        if not self.j.pontos_atributo:
            return "Sem pontos para distribuir."
        if self.j.atributos[a] >= atr.ATRIBUTO_MAX:
            return f"{atr.NOMES[a]} já está no máximo ({atr.ATRIBUTO_MAX})."
        return None

    def opcoes_atributos(self):
        """Distribuir os pontos da subida de nível: fora da luta, em qualquer lugar. Na tela gráfica é o "+" de cada
        atributo na ficha (meta `atributo`); no texto, uma linha do menu."""
        j = self.j
        if not j.pontos_atributo:
            return []
        if not self.ui.troca_no_grimorio:
            return [(f"Atributos  ★ {tx.plural(j.pontos_atributo, 'ponto')} para distribuir", "atributos",
                     {"sistema": "atributos", "pontos": j.pontos_atributo})]
        return [(f"Atributo: +1 de {atr.NOMES[a]}", ("atributo", a), {"atributo": a, "motivo": self.motivo_atributo(a)})
                for a in atr.ATRIBUTOS]

    def gastar_atributo(self, a):
        """Um ponto num atributo. Os totais que ele muda (Ataque, vida, recurso...) sobem na hora."""
        j = self.j
        motivo = self.motivo_atributo(a)
        if motivo:
            self.dizer(motivo, "cinza")
            return False
        antes_hp, antes_rec = j.max_hp, j.max_rec
        j.atributos = dict(j.atributos, **{a: j.atributos[a] + 1})
        j.pontos_atributo -= 1
        j.recalcular()
        j.hp += max(0, j.max_hp - antes_hp)  # a vida e o recurso que o máximo ganhou vêm junto
        j.rec += max(0, j.max_rec - antes_rec)
        registrar(self, "ponto_atributo", atributo=a, valor=j.atributos[a])
        return True

    def menu_atributos(self):
        """No texto: um ponto de cada vez, com o que cada atributo dá (a mesma frase da ficha)."""
        j = self.j
        while j.pontos_atributo:
            opcoes = [(f"{atr.NOMES[a]} {j.atributos[a]} → {j.atributos[a] + 1}: {atr.FUNCAO[a]}", a,
                       {"atributo": a, "indisponivel": self.motivo_atributo(a)}) for a in atr.ATRIBUTOS]
            opcoes.append(("Depois", None, {"voltar": True}))
            a = self.menu(f"Pontos de atributo: {j.pontos_atributo}. Onde pôr um?", opcoes)
            if a is None:
                return
            self.gastar_atributo(a)

    def ganhar_ponto_talento(self, n=1, anunciar=True):
        self.j.pontos_talento += n
        if anunciar:
            self.dizer(f"+{n} ponto de talento! (use em \"Talentos\" — você tem {self.j.pontos_talento})",
                       "amarelo+negrito")

    def menu_talentos(self):
        abertura.visto(self, "T1")  # a árvore aberta: o quadro que apontava para ela não volta
        while True:
            j = self.j
            self.ui.mostrar_talentos(lambda: talentos.dados_arvore(j), lambda: talentos.desenhar(j),
                                     f"{j.nome_classe} · pontos disponíveis: {j.pontos_talento}")
            opcoes = []
            for t in talentos.TALENTOS[j.classe]:
                est = talentos.estado(j, t)
                texto = f"{t['nome']} {j.tal(t['id'])}/{t['max']} — {talentos.descricao(j, t)}"
                if est == "disponivel" and j.pontos_talento:
                    texto = "▶ " + texto
                elif est != "disponivel":
                    texto += f" ({talentos.motivo(t, est) or 'completo'})"
                opcoes.append((texto, t, {"talento": t["id"]}))
            t = self.menu("Escolha um talento para aprender:", opcoes + [("Voltar", None, {"voltar": True})])
            if t is None:
                return
            est = talentos.estado(j, t)
            if est != "disponivel":
                self.dizer(f"Indisponível: {talentos.motivo(t, est) or 'já está no máximo'}.", "vermelho")
            elif not j.pontos_talento:
                self.dizer("Você não tem pontos de talento. Suba de nível ou derrote guardiões.", "vermelho")
            else:
                j.pontos_talento -= 1
                talentos.aprender(j, t)
                registrar(self, "talento", id=t["id"], nome=t["nome"], rank=j.tal(t["id"]))
                antes = j.max_hp
                j.recalcular()
                j.hp += max(0, j.max_hp - antes)
                self.ui.talento_aprendido(t["nome"], j.tal(t["id"]), t["max"])
                if t["transforma"] and not self.ui.troca_no_grimorio:
                    self.dizer(talentos.frase_transformacao(t), "ciano")

    # ================================================================ versões (E6)
    def opcoes_versao(self):
        """Trocar a versão de uma habilidade transformada: só onde se descansa (a vila e o acampamento), nunca na
        luta. Na tela gráfica é o botão da página dela no Grimório (meta `versao`); no texto, uma linha do menu."""
        j = self.j
        opcoes = []
        for h_id, variante in transformacoes(j).items():
            if h_id not in j.habilidades:
                continue
            outra = h_id if versao(j, h_id) == variante else variante
            opcoes.append((f"Grimório: usar a {ficha(outra)['nome']} no lugar da {efetiva(j, h_id)['nome']}",
                           ("versao", h_id, None if outra == h_id else outra), {"versao": h_id, "para": outra}))
        return opcoes

    def trocar_versao(self, h_id, variante):
        escolher_versao(self.j, h_id, variante)
        registrar(self, "versao", habilidade=h_id, versao=versao(self.j, h_id))
        # Na tela, a página do Grimório já mostra o que mudou (a versão em uso e o botão para a outra): nada a dizer.
        # No texto, uma linha curta, porque o menu só mostra a troca de volta.
        if not self.ui.troca_no_grimorio:
            self.dizer(f"Em uso: {efetiva(self.j, h_id)['nome']}.", "ciano")

    # ================================================================ o kit (etapa 4)
    def opcoes_kit(self):
        """Montar o kit: só onde se descansa (a vila e o acampamento), nunca na luta (kit.py). Na tela gráfica é o
        botão da página de cada habilidade no Grimório (meta `kit`); no texto, uma linha do menu que abre a lista."""
        j = self.j
        if not self.ui.troca_no_grimorio:
            r = kits.resumo(j)
            return [(f"Kit de habilidades ({r['pontos']}/{r['max_pontos']} pontos, "
                     f"{r['espacos']}/{r['max_espacos']} habilidades)", ("kit", None), {"kit_menu": True})]
        return [(f"Kit: {'tirar' if h in j.kit else 'levar'} {efetiva(j, h)['nome']}", ("kit", h),
                 {"kit": h, "no_kit": h in j.kit, "motivo": kits.motivo_incluir(j, h)})
                for h in j.habilidades if h in HABILIDADES]

    def mexer_kit(self, h_id):
        """Põe ou tira uma habilidade (h_id) ou abre a lista do kit no texto (h_id None)."""
        j = self.j
        if h_id is not None:
            motivo = kits.alternar(j, h_id)
            if motivo:
                self.dizer(motivo, "cinza")
            else:
                registrar(self, "kit", habilidade=h_id, no_kit=h_id in j.kit)
            return
        while True:
            r = kits.resumo(j)
            opcoes = []
            for h in j.habilidades:
                if h not in HABILIDADES:
                    continue
                t = kits.tier(h)
                marca = "[x]" if h in j.kit else "[ ]"
                opcoes.append((f"{marca} {efetiva(j, h)['nome']} ({kits.NOME_TIER[t]}, {kits.PONTOS_TIER[t]} "
                               f"ponto{'s' if kits.PONTOS_TIER[t] > 1 else ''})", h,
                               {"kit": h, "no_kit": h in j.kit, "indisponivel": kits.motivo_incluir(j, h)}))
            opcoes.append(("Pronto", None, {"voltar": True}))
            h = self.menu(f"Kit: {r['pontos']}/{r['max_pontos']} pontos, {r['espacos']}/{r['max_espacos']} habilidades, "
                          "no máximo uma ultimate. Atacar, Defender e Itens não entram no kit.", opcoes)
            if h is None:
                return
            self.mexer_kit(h)

    def _aprender_habilidades(self, anunciar=True):
        j = self.j
        novas = []
        for h in habilidades_ate(j.classe, j.spec, j.nivel):
            if h not in j.habilidades:
                j.habilidades.append(h)
                novas.append(h)
                no_kit = kits.incluir_se_couber(j, h)
                if anunciar:
                    self.dizer(f"Nova habilidade: {HABILIDADES[h]['nome']} — {HABILIDADES[h]['desc']}"
                               + ("" if no_kit else " (fora do kit: troque na vila ou na fogueira)"),
                               "amarelo+negrito")
        return novas

    def especializar(self, spec):
        j = self.j
        j.spec = spec
        registrar(self, "spec", spec=spec)
        especializacao.aplicar_bonus(j, spec)  # a mesma conta da prévia que a escolha mostra
        j.hp = j.max_hp
        j.rec = j.max_rec
        festa = self.ui.conquistas_na_tela
        if not festa:
            self.ui.titulo(f"VOCÊ AGORA É {SPECS[spec]['nome'].upper()}", "magenta+negrito")
            self.dizer(SPECS[spec]["desc"], "magenta")
        novas = self._aprender_habilidades(anunciar=not festa)
        # o id da especialização: a tela escolhe a identidade visual da festa por ele, não pelo nome exibido
        self.ui.celebrar("spec", {"id": spec, "nome": SPECS[spec]["nome"], "desc": SPECS[spec]["desc"],
                                  "habilidades": [{"nome": HABILIDADES[h]["nome"], "desc": HABILIDADES[h]["desc"],
                                                   "icone": HABILIDADES[h]["icone"]} for h in novas]})
        if SPECS[spec].get("reage"):
            comitiva.reagir(self, *SPECS[spec]["reage"], forca=1.5)
        if SPECS[spec].get("companheiro"):
            self.escolher_companheiro()

    def escolher_companheiro(self, tipo=None):
        if tipo is None:
            tipos = list(COMPANHEIROS)
            esc = self.ui.escolher("Qual animal atende ao seu chamado?",
                                   [f"{COMPANHEIROS[t]['nome']} — {COMPANHEIROS[t]['desc']}" for t in tipos])
            tipo = tipos[esc]
        c = COMPANHEIROS[tipo]
        nome = self.ui.perguntar(f"Como vai chamar seu {c['nome'].split()[0].lower()}? (Enter para '{c['nome']}')",
                                 c["nome"])
        self.j.companheiro = {"nome": nome, **especializacao.animal(tipo, self.j.nivel)}  # a mesma conta da prévia
        self.dizer(f"{nome} agora caminha ao seu lado.", "verde+negrito")
