"""Clima, períodos do dia, dias, descanso, acampamento e taverna."""

from .. import eventos
from ..dados import CLIMAS, PESOS_CLIMA
from .. import comitiva
from .. import sobrevivencia
from ..telemetria import registrar
from .. import balanceamento as bal


class Tempo:
    # ================================================================ tempo e clima
    def rolar_clima(self):
        pesos = PESOS_CLIMA.get(self.bioma, PESOS_CLIMA["padrao"])
        self.clima = self.rng.choices(list(pesos), weights=list(pesos.values()))[0]

    def avancar_periodo(self):
        self.passos += 1
        self.periodo += 1
        if self.periodo == 3:
            self.dizer("A noite cai. Algo começa a se mover nas trevas, e não é gente.", "magenta")

    def novo_dia(self, descanso=1, refeicao=False):
        """refeicao: a noite já incluiu a comida de todos (a taverna); ninguém come das provisões."""
        self.dia += 1
        self.periodo = 0
        self.rolar_clima()
        self.rumores = [r for r in self.rumores if r["expira"] >= self.dia]
        self.impulsos = {}
        for r in self.rumores:
            if r.get("evento"):
                self.impulsos[r["evento"]] = self.impulsos.get(r["evento"], 1) * 3
        self.ui.separador()
        self.dizer(f"Amanhece o dia {self.dia}. {CLIMAS[self.clima]['desc']}", "amarelo")
        sobrevivencia.amanhecer(self, descanso, refeicao)
        comitiva.amanhecer(self, descanso, refeicao)
        registrar(self, "dia", descanso=descanso, provisoes=self.j.provisoes, fome=self.j.fome,
                  ferimentos=len(self.j.ferimentos), local=self.loc["nome"])

    def descansar(self, fracao, mana=1.0, folego=1.0):
        """Descanso devolve pouca vida: ferimentos de verdade levam dias. Com fome, quase nada.
        Mana volta pela metade numa noite ao relento; vigor e foco, quase todo (só a cama devolve tudo)."""
        j = self.j
        if j.fome:
            fracao *= 0.3
        cura = j.curar(j.max_hp * fracao)
        if cura:
            self.dizer(f"Você recupera {cura} de vida. ({j.hp}/{j.max_hp})", "verde")
        parte = mana if j.classe == "mago" else folego
        j.rec = min(j.max_rec, j.rec + int(j.max_rec * parte))
        j.efeitos = {}
        if j.companheiro:
            j.companheiro["hp"] = j.companheiro["max_hp"]
        comitiva.descansar(self, fracao)

    def exausto(self):
        self.ui.separador()
        if self.loc["tipo"] == "vila":
            self.dizer("Exausto, você pede abrigo num estábulo e dorme sobre o feno, entre ratos.", "cinza")
            self.descansar(bal.EXAUSTO_VIDA, mana=bal.EXAUSTO_RECURSO, folego=bal.EXAUSTO_RECURSO)
            self.novo_dia(descanso=1)
        else:
            self.dizer("Você está exausto demais para continuar. É preciso acampar.", "cinza")
            self.acampar()

    def acampar(self):
        juntos = [comitiva.nome(m["id"]) for m in comitiva.membros(self)]
        if juntos:
            quem = juntos[0] if len(juntos) == 1 else ", ".join(juntos[:-1]) + " e " + juntos[-1]
            intro = (f"Vocês juntam gravetos e a fogueira pega. {quem} se {'ajeita' if len(juntos) == 1 else 'ajeitam'} "
                     "perto do fogo; a noite fica um pouco menos escura.")
        elif comitiva.reserva(self):
            intro = "Você segue a fumaça até o seu acampamento. A fogueira de quem esperou por você ainda arde."
        else:
            intro = "Você junta gravetos, acende uma fogueira fraca e se enrola na capa. O frio entra mesmo assim."
        if comitiva.membros(self) or comitiva.reserva(self) or self.ui.fogueira_sozinho:
            conversou = comitiva.fogueira(self, intro)
            self.ui.cena("Acampamento", self.contexto_cena(), "evento")
        else:
            self.ui.cena("Acampamento", self.contexto_cena(), "evento")
            self.dizer(intro, "cinza")
            conversou = False
        if self.encruzilhada_no_descanso():
            conversou = True
        if not conversou and not comitiva.noite(self) and self.chance(0.45):
            eventos.disparar(self, "acampamento")
        fracao = bal.ACAMPAR_VIDA
        if self.clima in ("chuva", "tempestade", "neve"):
            fracao = bal.ACAMPAR_VIDA_RUIM
            self.dizer("Você dorme encharcado e tremendo. Quase não descansa.", "vermelho")
        self.descansar(fracao, mana=bal.ACAMPAR_MANA, folego=bal.ACAMPAR_FOLEGO)
        self.novo_dia(descanso=1)
        self.pausar()

    def dormir_taverna(self, preco):
        if self.j.ouro < preco:
            self.dizer("Sem ouro suficiente. O taverneiro aponta para a porta.", "vermelho")
            return
        self.ui.cena("A taverna", self.contexto_cena(), "evento")
        self.perder_ouro(preco)
        self.dizer("Uma cama de palha sem pulgas demais e um ensopado ralo para todos. É o melhor que este mundo "
                   "oferece.",
                   "verde")
        self.periodo = 3
        self.encruzilhada_no_descanso()
        self.descansar(bal.TAVERNA_VIDA)
        self.novo_dia(descanso=2, refeicao=True)  # o ensopado é de todos: ninguém come das provisões
        self.pausar()
