"""Viagem entre lugares, chegada e o mapa."""

from .. import eventos
from .. import texto as tx
from .. import mapa
from .. import sobrevivencia
from ..dados import BIOMAS
from ..telemetria import registrar
from ..mundo import nivel_regiao, vizinhos


class Navegacao:
    def viajar(self):
        self.ui.cena("Viagem", self.contexto_cena(), "menu")
        self.desenhar_mapa()
        opcoes = []
        for loc, dist in sorted(vizinhos(self.mundo, self.loc), key=lambda v: v[0]["id"]):
            numero = f"[{loc['id'] + 1}] {mapa.glifo(self, loc)} " if self.ui.numerar_destinos else ""
            texto = f"{numero}{loc['nome']} — {mapa.descricao(self, loc)}"
            nv = nivel_regiao(loc)
            texto += f" · arredores Nv.{nv}" if loc["tipo"] == "vila" else f" · Nv.{nv}"
            if nv >= self.j.nivel + 2:
                texto += " (PERIGOSO!)"
            texto += f" · {dist} trecho{'s' if dist > 1 else ''}"
            if not loc["visitado"]:
                texto += " · inexplorado"
            opcoes.append((texto, (loc, dist), {"local": loc["id"]}))
        opcoes.append(("Voltar", None))
        destino = self.menu("Para onde?", opcoes)
        if not destino:
            return
        loc, dist = destino
        nv = nivel_regiao(loc)
        if nv >= self.j.nivel + 3:
            # Vila também: dentro dela se está seguro, mas as estradas em volta são da região (e é por elas que se sai).
            onde = (f"As estradas em volta de {loc['nome']} têm inimigos de nível {nv}" if loc["tipo"] == "vila"
                    else f"{loc['nome']} tem inimigos de nível {nv}")
            if not self.confirmar(f"{onde}. Você é nível {self.j.nivel}. "
                                  f"Lá, quase qualquer encontro pode te matar. Ir mesmo assim?",
                                  [("Não, voltar", False), ("Sim, eu sei o que estou fazendo", True)], perigo=True):
                return
        if loc["tipo"] == "cidadela" and len(self.j.sigilos) < 3:
            self.dizer(f"Uma muralha de sombras bloqueia o caminho. Você precisa dos três Sigilos "
                       f"({len(self.j.sigilos)}/3).", "magenta")
            return
        self.na_estrada = True
        try:
            for trecho in range(dist):
                if self.periodo > 3:
                    self.dizer("A noite está avançada demais para seguir viagem.", "cinza")
                    self.acampar()
                if trecho >= dist / 2:
                    self.mundo["atual"] = loc["id"]
                self.ui.cena(f"Rumo a {loc['nome']}", f"trecho {trecho + 1} de {dist} · {self.contexto_cena()}", "evento")
                sobrevivencia.acender_tocha(self)
                try:
                    if self.chance(0.65):
                        eventos.disparar(self, "viagem")
                    else:
                        self.dizer(self.ambiente() + " A viagem segue sem incidentes.", "cinza")
                finally:
                    self.sem_luz = False
                self.avancar_periodo()
        finally:
            self.na_estrada = False
        self.chegar(loc)

    def chegar(self, loc):
        self.mundo["atual"] = loc["id"]
        registrar(self, "chegada", local=loc["nome"], tipo_local=loc["tipo"], nivel_regiao=self.nivel_local(),
                  primeira=not loc["visitado"])
        primeira = not loc["visitado"]
        loc["visitado"] = True
        if self.chance(0.5):
            self.rolar_clima()
        self.ui.separador()
        perigo = self.nivel_local() >= self.j.nivel + 3
        if self.ui.conquistas_na_tela:  # o nome do lugar vira título de área, como nos jogos; o texto não repete
            # Chegar é página nova: o que aconteceu na estrada fica o tempo de ler, a página vira para o lugar e só
            # então o nome dele surge (antes, a chegada e os contratos pagos pipocavam por cima do texto da estrada).
            self.pausar()
            self.cabecalho()
            self.ui.celebrar("chegada", {"nome": loc["nome"], "sub": self.descrever_lugar(loc), "tipo": loc["tipo"],
                                         "nivel": self.nivel_local(), "primeira": primeira})
        else:
            self.dizer(f"Você chega a {loc['nome']}.", "amarelo+negrito")
        if primeira and loc["tipo"] != "vila":
            self.dizer(self.ambiente(), "cinza")
        if loc["tipo"] == "covil" and not loc["guardiao"]["derrotado"]:
            g = loc["guardiao"]
            self.dizer(f"Este é o covil de {g['nome']} (Nv.{self.nivel_guardiao(loc)}). Um dos Sigilos está aqui.",
                       "magenta")
        if perigo:
            self.dizer("A vila tem muros, mas as estradas em volta são de criaturas muito mais fortes do que você."
                       if loc["tipo"] == "vila" else
                       "Um arrepio sobe pela espinha. As criaturas daqui são muito mais fortes do que você.",
                       "vermelho+negrito")
        if loc["tipo"] == "cidadela":
            self.dizer(f"Os três Sigilos ardem em sua mão e a muralha de sombras se abre. "
                       f"{tx.maiuscula(self.antagonista['curto'])} sabe que você chegou.", "magenta+negrito")
        if loc["tipo"] == "vila":
            self.receber_contratos()
            if self.chance(0.35):
                eventos.disparar(self, "vila")
        self.pausar()

    @staticmethod
    def descrever_lugar(loc):
        """"Vila", "Floresta", "Covil · Ruínas", "Cidadela": o que o lugar é, numa linha."""
        bioma = BIOMAS[loc["bioma"]]["nome"] if loc.get("bioma") in BIOMAS else ""
        if loc["tipo"] == "vila":
            return "Vila"
        if loc["tipo"] == "cidadela":
            return "Cidadela"
        return " · ".join(x for x in ("Covil" if loc["tipo"] == "covil" else "", bioma) if x)

    def mapa(self):
        self.ui.cena("Mapa do reino", self.contexto_cena(), "menu")
        if self.desenhar_mapa(grande=True):
            self.pausar()
            return
        self.dizer(mapa.SIMBOLOS, "cinza")
        self.ui.separador()
        for rotulo, texto, cor in mapa.legenda(self):
            self.dizer(f"{rotulo:>2}  {texto}", cor)
        self.pausar()

    def desenhar_mapa(self, grande=False):
        """Devolve True se a interface desenha o próprio mapa (a web, em SVG); senão vai em caracteres."""
        return self.ui.desenhar_mapa(grande, lambda: mapa.renderizar(self))
