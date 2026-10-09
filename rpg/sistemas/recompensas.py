"""Ganhos e perdas: ouro, XP, vida, itens, reputação, sementes e rumores."""

from .. import eventos
from ..entidades import nome_stat
from ..itens import CONSUMIVEIS
from .. import sobrevivencia
from .. import texto as tx
from ..regras import NIVEL_MAXIMO
from .. import balanceamento as bal
from ..modificadores import mod
from ..telemetria import registrar


class Recompensas:
    # ================================================================ recompensas e perdas
    def ganhar_ouro(self, n, exato=False, avisar=True, fonte="eventos"):
        """exato: o valor já é o combinado (contrato); senão, o mundo é pobre e só fica parte (OURO_MUNDO).
        avisar=False: a tela já mostrou o ganho (o quadro do contrato). fonte: de onde veio, para a telemetria
        (lutas, contratos, baus, eventos); None quando já foi contado (o quadro do espólio entregando)."""
        n = int(n) if exato else self.ouro_achado(n)
        if n <= 0:
            return 0
        if fonte:
            fontes = self.estatisticas.setdefault("ouro_fontes", {})
            fontes[fonte] = fontes.get(fonte, 0) + n
        if self.espolio_aberto is not None:  # vai para o quadro do espólio, que entrega quando aparece
            self.espolio_aberto["ouro"] += n
            return n
        self.j.ouro += n
        self.estatisticas["ouro_ganho"] += n
        if avisar:
            self.ui.efeito(f"+{n} ouro", "ouro")
        return n

    # ------------------------------------------------------------ o quadro do espólio
    # Na tela gráfica, o que se ganha depois de uma vitória (o ouro dos inimigos, o XP, os contratos que andaram, o que
    # se acha nos corpos e o que o evento ainda der logo depois, como o cofre que o lobo guardava) vai para um quadro só,
    # mostrado antes da próxima pergunta ao jogador (menu, Continuar, outra luta) ou no fim do evento. O ouro e o XP são
    # entregues quando o quadro aparece (o ouro do topo sobe quando as moedas chegam; o nível sobe depois dele), e o
    # equipamento achado vem logo em seguida (é uma escolha). No texto, cada ganho é dito na hora, como sempre.
    def abrir_espolio(self, titulo=None):
        """titulo: o rótulo do quadro quando não é o espólio de uma vitória ("baú aberto")."""
        if self.ui.conquistas_na_tela and self.espolio_aberto is None:
            self.espolio_aberto = {"ouro": 0, "xp": 0, "itens": [], "contratos": [], "equip": []}
            self.titulo_espolio = titulo

    def fechar_espolio(self):
        e, self.espolio_aberto = self.espolio_aberto, None
        if e is None:
            return
        if any(e.values()):
            dados = {"ouro": e["ouro"], "xp": e["xp"], "nivel": self.j.nivel, "trechos": self.trechos_xp(e["xp"]),
                     "itens": e["itens"], "contratos": e["contratos"], "equip": len(e["equip"])}
            if self.titulo_espolio:
                dados["titulo"] = self.titulo_espolio
            self.ui.celebrar("espolio", dados)
        self.ganhar_ouro(e["ouro"], exato=True, avisar=False, fonte=None)
        self.ganhar_xp(e["xp"], avisar=False)
        for item in e["equip"]:
            self.oferecer_equip(item)

    def achou(self, chave, nome, qtd):
        """Um consumível, comida ou flechas achados: com o quadro do espólio aberto, entram nele (somando com o que já
        estava lá) e devolve True; senão devolve False, e quem chamou avisa do jeito de sempre."""
        e = self.espolio_aberto
        if e is None:
            return False
        ja = next((x for x in e["itens"] if x["id"] == chave), None)
        if ja:
            ja["qtd"] += qtd
        else:
            e["itens"].append({"id": chave, "nome": nome, "qtd": qtd})
        return True

    def contar_achado(self, texto, cor):
        """De onde veio um achado (os alforjes, os pertences): no quadro do espólio, o achado já aparece com nome e
        ícone, então o texto só vai quando não há quadro."""
        if self.espolio_aberto is None:
            self.dizer(texto, cor)

    def ouro_achado(self, n):
        """Quanto fica de um ouro achado (saque, evento): o mundo é pobre (OURO_MUNDO)."""
        return int(n * bal.OURO_MUNDO)

    def perder_ouro(self, n, destino="eventos"):
        """destino: para onde foi, para a telemetria (mercado, ferreiro, templo, curandeira, taverna...)."""
        n = min(self.j.ouro, int(n))
        self.j.ouro -= n
        if n:
            gastos = self.estatisticas.setdefault("ouro_gastos", {})
            gastos[destino] = gastos.get(destino, 0) + n
        if n:
            self.ui.efeito(f"−{n} ouro", "perda")
        return n

    def ganhar_xp(self, n, avisar=True):
        n = int(n)
        if n <= 0 or self.j.nivel >= NIVEL_MAXIMO:
            return
        if self.espolio_aberto is not None:  # o quadro enche a barra antes; o nível sobe depois dele
            self.espolio_aberto["xp"] += n
            return
        self.j.xp += n
        if avisar:
            self.ui.efeito(f"+{n} XP", "xp")
        while self.j.nivel < NIVEL_MAXIMO and self.j.xp >= self.j.xp_proximo():
            self.j.xp -= self.j.xp_proximo()
            self.subir_nivel()

    def trechos_xp(self, n):
        """Como a barra de XP vai encher com +n: um trecho por nível tocado, [de, até, tamanho do nível].
        Ex.: com 80/92 e +30, [[80, 92, 92], [0, 18, 104]] (enche, sobe de nível, recomeça). A tela anima isso."""
        j = self.j
        nivel, xp, n = j.nivel, j.xp, int(n)
        trechos = []
        while n > 0 and nivel < NIVEL_MAXIMO:
            total = bal.xp_para_subir(nivel)
            ate = min(total, xp + n)
            trechos.append([xp, ate, total])
            n -= ate - xp
            if ate < total:
                break
            nivel, xp = nivel + 1, 0
        return trechos

    def ferir(self, n, motivo=""):
        """Dano de evento (fora do combate). Não mata, mas pode deixar um ferimento duradouro."""
        n = int(n)
        if n <= 0:
            return
        self.j.hp = max(1, self.j.hp - n)
        self.ui.efeito(f"−{n} vida{motivo} ({self.j.hp}/{self.j.max_hp})", "dano")
        sobrevivencia.ferir_por_evento(self, n, motivo)

    def curar(self, n):
        c = self.j.curar(n)
        if c:
            self.ui.efeito(f"+{c} vida ({self.j.hp}/{self.j.max_hp})", "cura")

    def restaurar_recurso(self, n):
        j = self.j
        ganho = max(0, min(int(n), j.max_rec - j.rec))
        j.rec += ganho
        if ganho:
            self.ui.efeito(f"+{ganho} {j.nome_recurso}", "cura")

    def dar(self, item, qtd=1):
        self.j.consumiveis[item] = self.j.consumiveis.get(item, 0) + qtd
        if not self.achou(item, CONSUMIVEIS[item]["nome"], qtd):
            self.ui.efeito(f"{CONSUMIVEIS[item]['nome']} ×{qtd}", "item", item=item)

    def bonus_permanente(self, stat, valor):
        """Bônus de atributo vindo de eventos, com teto por partida (evita acumular sem fim)."""
        teto = {"max_hp": 15, "max_rec": 15}.get(stat, 4)
        ganhos = self.flags.setdefault("bonus_eventos", {})
        ganho = max(0, min(valor, teto - ganhos.get(stat, 0)))
        if not ganho:
            self.dizer("(Você sente que já tirou tudo o que podia desse tipo de experiência.)", "cinza")
            return 0
        ganhos[stat] = ganhos.get(stat, 0) + ganho
        self.j.base[stat] += ganho
        self.j.recalcular()
        registrar(self, "atributo", stat=stat, ganho=ganho)
        nome = nome_stat(stat, self.j.nome_recurso)
        if self.ui.conquistas_na_tela:  # o selo voa até o atributo no painel, que conta até o valor novo
            self.ui.celebrar("atributo", {"stat": stat, "nome": nome, "valor": ganho, "total": getattr(self.j, stat)})
        else:
            self.ui.efeito(f"+{ganho} {nome} permanente", "nivel")
        return ganho

    def dar_provisoes(self, n):
        antes = self.j.provisoes
        self.j.provisoes = min(sobrevivencia.MAX_PROVISOES, antes + n)
        n = self.j.provisoes - antes
        if n > 0 and not self.achou("comida", "Comida", n):
            self.ui.efeito(f"+{tx.plural(n, 'dia')} de comida (total {self.j.provisoes})", "item", item="comida")
        if n > 0 and self.j.fome:
            # Com fome, quem compra (ou acha) comida come ali mesmo: não espera o amanhecer para a fome passar.
            self.j.provisoes -= 1
            self.j.fome = 0
            self.ui.efeito("Comida na hora: a fome passou", "item")

    def max_flechas(self):
        """A aljava tem fundo: não dá para comprar cem flechas e esquecer delas."""
        return bal.ALJAVA + mod(self.j, "aljava")

    def dar_flechas(self, n):
        if self.j.classe != "arqueiro" or n <= 0:
            return 0
        n = min(n, self.max_flechas() - self.j.flechas)
        if n <= 0:
            self.dizer("Sua aljava já está cheia.", "cinza")
            return 0
        self.j.flechas += n
        if not self.achou("flechas", "Flechas", n):
            self.ui.efeito(f"+{tx.plural(n, 'flecha')} (total {self.j.flechas}/{self.max_flechas()})", "item",
                           item="flechas")
        return n

    def mudar_reputacao(self, d, avisar=True):
        antes = self.j.reputacao
        self.j.reputacao = max(-50, min(50, antes + d))
        if not avisar:
            return
        if self.j.reputacao > antes:
            self.ui.efeito(f"Reputação +{self.j.reputacao - antes}", "rep")
        elif self.j.reputacao < antes:
            self.ui.efeito(f"Reputação −{antes - self.j.reputacao}", "perda")

    # ---------------------------------------------------------------- sementes (consequências futuras)
    def plantar(self, id, atraso=4, **dados):
        self.sementes.append({"id": id, "pronto": self.passos + atraso, "dados": dados})

    def semente(self, id):
        for s in self.sementes:
            if s["id"] == id and s["pronto"] <= self.passos:
                return s
        return None

    def colher(self, id):
        s = self.semente(id)
        if s:
            self.sementes.remove(s)
            return s["dados"]
        return None

    def aliado_final(self, nome, texto, efeito, valor):
        if any(a["nome"] == nome for a in self.aliados_finais):
            return
        self.aliados_finais.append({"nome": nome, "texto": texto, "efeito": efeito, "valor": valor})
        self.dizer(f"({nome} pode ajudar você quando a hora final chegar.)", "ciano")

    def rumor_aqui(self, evento):
        for r in self.rumores:
            if r.get("evento") == evento and r.get("local") == self.loc["id"]:
                return r
        return None

    def consumir_rumor(self, evento):
        r = self.rumor_aqui(evento)
        if r:
            self.rumores.remove(r)
            self.impulsos.pop(evento, None)
        return r

    def encruzilhada_no_descanso(self):
        """A escolha de especialização chega na primeira noite de descanso depois do nível 4 (como um sonho, uma visão)."""
        pendente = next((f for f in self.forcados if f.startswith("encruzilhada_")), None)
        if not pendente:
            return False
        self.forcados.remove(pendente)
        self.forcados.insert(0, pendente)
        eventos.disparar(self, "noite")
        return True

    def evento_forcado(self, contexto):
        if self.forcados:
            return self.forcados.pop(0)
        return None
