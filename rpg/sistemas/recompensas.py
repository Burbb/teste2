"""Ganhos e perdas: ouro, XP, vida, itens, reputação, corrupção, sementes e rumores."""

from .. import eventos
from .. import texto as tx
from ..entidades import NOMES_STATS
from ..itens import CONSUMIVEIS
from .. import sobrevivencia
from ..regras import NIVEL_MAXIMO


class Recompensas:
    # ================================================================ recompensas e perdas
    def ganhar_ouro(self, n):
        n = int(n * 0.75)  # o mundo é pobre: ninguém carrega muito ouro
        if n <= 0:
            return
        self.j.ouro += n
        self.estatisticas["ouro_ganho"] += n
        self.ui.efeito(f"+{n} ouro", "ouro")

    def perder_ouro(self, n):
        n = min(self.j.ouro, int(n))
        self.j.ouro -= n
        if n:
            self.ui.efeito(f"−{n} ouro", "perda")
        return n

    def ganhar_xp(self, n):
        n = int(n)
        if n <= 0 or self.j.nivel >= NIVEL_MAXIMO:
            return
        self.j.xp += n
        self.ui.efeito(f"+{n} XP", "xp")
        while self.j.nivel < NIVEL_MAXIMO and self.j.xp >= self.j.xp_proximo():
            self.j.xp -= self.j.xp_proximo()
            self.subir_nivel()

    def ferir(self, n, motivo=""):
        n = int(n)
        if n <= 0:
            return
        self.j.hp = max(1, self.j.hp - n)
        self.ui.efeito(f"−{n} vida{motivo} ({self.j.hp}/{self.j.max_hp})", "dano")

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
        self.ui.efeito(f"{CONSUMIVEIS[item]['nome']} ×{qtd}", "item")

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
        self.ui.efeito(f"+{ganho} {NOMES_STATS[stat]} permanente", "nivel")
        return ganho

    def dar_provisoes(self, n):
        antes = self.j.provisoes
        self.j.provisoes = min(sobrevivencia.MAX_PROVISOES, antes + n)
        if self.j.provisoes > antes:
            self.ui.efeito(f"+{self.j.provisoes - antes} dia(s) de comida (total {self.j.provisoes})", "item")

    def max_flechas(self):
        """A aljava tem fundo: não dá para comprar cem flechas e esquecer delas."""
        return 30 + 5 * self.j.tal("aljava_funda")

    def dar_flechas(self, n):
        if self.j.classe != "arqueiro" or n <= 0:
            return 0
        n = min(n, self.max_flechas() - self.j.flechas)
        if n <= 0:
            self.dizer("Sua aljava já está cheia.", "cinza")
            return 0
        self.j.flechas += n
        self.ui.efeito(f"+{n} flechas (total {self.j.flechas}/{self.max_flechas()})", "item")
        return n

    def mudar_reputacao(self, d):
        antes = self.j.reputacao
        self.j.reputacao = max(-50, min(50, antes + d))
        if self.j.reputacao > antes:
            self.ui.efeito(f"Reputação +{self.j.reputacao - antes}", "rep")
        elif self.j.reputacao < antes:
            self.ui.efeito(f"Reputação −{antes - self.j.reputacao}", "perda")

    def corromper(self, d, silencioso=False):
        antes = self.corrupcao
        self.corrupcao = max(0, min(100, antes + d))
        if not silencioso:
            if d < 0:
                self.dizer(f"A corrupção do reino recua. ({self.corrupcao}%)", "verde")
            elif d > 0:
                self.dizer(f"A corrupção do reino aumenta. ({self.corrupcao}%)", "magenta")
        for limiar, texto in ((25, "As colheitas murcham e os animais andam inquietos. A sombra de {a} se espalha."),
                              (50, "Crias do Vazio são vistas em plena luz do dia. Os sinos das vilas tocam sem ninguém puxar as cordas."),
                              (75, "O céu tem cor de hematoma. Rumores dizem que {a} está prestes a atravessar a Fenda."),
                              (90, "O mundo range como um navio prestes a afundar. Resta pouco tempo!")):
            if antes < limiar <= self.corrupcao:
                self.ui.separador("magenta")
                self.dizer(texto.format(a=self.antagonista["curto"]), "magenta+negrito")
        if self.corrupcao >= 100:
            self.fim_de_jogo(f"A corrupção consumiu o reino. {tx.maiuscula(self.antagonista['curto'])} atravessou a "
                             f"Fenda, e o mundo que você conhecia deixou de existir.")

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
