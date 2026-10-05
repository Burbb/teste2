"""Estado do jogo, ciclo principal e ações do jogador."""

import json
import os
import random
import re

from . import eventos
from . import texto as tx
from .classes import CLASSES, COMPANHEIROS, HABILIDADES, SPECS, habilidades_ate
from .combate import Combate
from .dados import BIOMAS, CLIMAS, FAMILIAS, GUARDIOES, PERIODOS, PESOS_CLIMA
from .entidades import Jogador
from .eventos.vila import ouvir_rumor
from .inimigos import criar, instanciar_antagonista, instanciar_guardiao
from .itens import CONSUMIVEIS, descrever_bonus, gerar_equip
from .mundo import gerar_mundo, vizinhos

VERSAO_SAVE = 1
NOMES_TESTE = {
    "forca": "Força", "destreza": "Destreza", "arcano": "Arcano",
    "percepcao": "Percepção", "vontade": "Vontade", "carisma": "Carisma",
}
NOMES_SLOT = {"arma": "Arma", "armadura": "Armadura", "amuleto": "Amuleto"}
LIMITE_MOCHILA = 8
NIVEL_MAXIMO = 10


class FimDeJogo(Exception):
    pass


class Derrota(Exception):
    """Interrompe a ação atual quando o herói cai (fora do modo hardcore)."""


class Jogo:
    def __init__(self, ui, seed=None, pasta_saves="saves", hardcore=False):
        self.ui = ui
        self.hardcore = hardcore
        self.seed = seed if seed is not None else random.randrange(1_000_000_000)
        self.rng = random.Random(self.seed)
        self.pasta_saves = pasta_saves
        self.j = None
        self.mundo = None
        self.dia = 1
        self.periodo = 0
        self.clima = "limpo"
        self.corrupcao = 0
        self.passos = 0
        self.flags = {}
        self.historico = {}
        self.contagem = {}
        self.impulsos = {}
        self.sementes = []
        self.rumores = []
        self.contratos = []
        self.ofertas = {}
        self.lojas = {}
        self.nemesis = None
        self.aliados_finais = []
        self.forcados = []
        self.proximo_id = 1
        self.estatisticas = {"abates": 0, "eventos": 0, "ouro_ganho": 0, "chefes": 0, "quedas": 0}

    # ================================================================ atalhos
    @property
    def loc(self):
        return self.mundo["locais"][self.mundo["atual"]]

    @property
    def bioma(self):
        return self.loc["bioma"]

    @property
    def noite(self):
        return self.periodo >= 3

    @property
    def antagonista(self):
        return self.mundo["antagonista"]

    def dizer(self, texto="", cor=None):
        self.ui.dizer(texto, cor)

    def narrar(self, texto, cor=None):
        self.ui.narrar(texto, cor)

    def pausar(self):
        self.ui.pausar()

    def chance(self, p):
        return self.rng.random() < p

    def sortear(self, seq):
        return self.rng.choice(list(seq))

    def npc(self):
        return tx.npc(self.rng)

    def flag(self, nome, padrao=None):
        return self.flags.get(nome, padrao)

    def marcar(self, nome, valor=True):
        self.flags[nome] = valor

    def novo_id(self):
        self.proximo_id += 1
        return self.proximo_id

    def menu(self, pergunta, opcoes):
        """opcoes: lista de (rótulo, chave) ou None (opção indisponível)."""
        validas = [o for o in opcoes if o]
        esc = self.ui.escolher(pergunta, [o[0] for o in validas])
        return validas[esc][1]

    def ambiente(self):
        return self.sortear(BIOMAS[self.bioma]["ambiente"])

    # ================================================================ testes
    def mod_teste(self, attr):
        j = self.j
        base = j.nivel // 2
        if attr == "forca":
            return base + j.atk // 3
        if attr == "destreza":
            return base + j.agi // 2
        if attr == "arcano":
            return base + j.poder // 3
        if attr == "percepcao":
            return base + j.agi // 3 + (3 if j.classe == "arqueiro" else 0) + (2 if j.spec == "patrulheiro" else 0)
        if attr == "vontade":
            return base + j.defesa // 4 + (3 if j.spec == "paladino" else 0) + (2 if j.classe == "mago" else 0)
        if attr == "carisma":
            return base + j.reputacao // 10 + (2 if j.spec == "paladino" else 0)
        return base

    def teste(self, attr, cd):
        d = self.rng.randint(1, 20)
        mod = self.mod_teste(attr)
        total = d + mod
        ok = d == 20 or (d != 1 and total >= cd)
        extra = " (crítico!)" if d == 20 else " (desastre!)" if d == 1 else ""
        self.dizer(f"  [Teste de {NOMES_TESTE[attr]}] d20={d} {mod:+d} = {total} contra {cd} → "
                   f"{'SUCESSO' if ok else 'FALHA'}{extra}", "verde" if ok else "vermelho")
        return ok

    # ================================================================ recompensas e perdas
    def ganhar_ouro(self, n):
        n = int(n)
        if n <= 0:
            return
        self.j.ouro += n
        self.estatisticas["ouro_ganho"] += n
        self.dizer(f"+{n} de ouro.", "amarelo")

    def perder_ouro(self, n):
        n = min(self.j.ouro, int(n))
        self.j.ouro -= n
        if n:
            self.dizer(f"-{n} de ouro.", "vermelho")
        return n

    def ganhar_xp(self, n):
        n = int(n)
        if n <= 0 or self.j.nivel >= NIVEL_MAXIMO:
            return
        self.j.xp += n
        self.dizer(f"+{n} de experiência.", "ciano")
        while self.j.nivel < NIVEL_MAXIMO and self.j.xp >= self.j.xp_proximo():
            self.j.xp -= self.j.xp_proximo()
            self.subir_nivel()

    def ferir(self, n, motivo=""):
        n = int(n)
        if n <= 0:
            return
        self.j.hp = max(1, self.j.hp - n)
        self.dizer(f"Você perde {n} de vida{motivo}. ({self.j.hp}/{self.j.max_hp})", "vermelho")

    def curar(self, n):
        c = self.j.curar(n)
        if c:
            self.dizer(f"+{c} de vida. ({self.j.hp}/{self.j.max_hp})", "verde")

    def restaurar_recurso(self, n):
        j = self.j
        ganho = max(0, min(int(n), j.max_rec - j.rec))
        j.rec += ganho
        if ganho:
            self.dizer(f"+{ganho} de {j.nome_recurso}.", "azul")

    def dar(self, item, qtd=1):
        self.j.consumiveis[item] = self.j.consumiveis.get(item, 0) + qtd
        self.dizer(f"Você obteve: {CONSUMIVEIS[item]['nome']} x{qtd}.", "verde")

    def dar_flechas(self, n):
        if self.j.classe != "arqueiro" or n <= 0:
            return
        self.j.flechas += n
        self.dizer(f"+{n} flechas. (total: {self.j.flechas})", "verde")

    def mudar_reputacao(self, d):
        antes = self.j.reputacao
        self.j.reputacao = max(-50, min(50, antes + d))
        if self.j.reputacao > antes:
            self.dizer("Sua fama de herói se espalha. (reputação +)", "verde")
        elif self.j.reputacao < antes:
            self.dizer("Histórias sombrias sobre você começam a circular. (reputação -)", "vermelho")

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

    def evento_forcado(self, contexto):
        if self.forcados:
            return self.forcados.pop(0)
        return None

    # ================================================================ inimigos e combate
    def nivel_inimigo(self, bonus=0):
        n = (self.j.nivel + self.rng.choice([-1, 0, 0, 0, 1]) + (self.loc["perigo"] - 2) // 2
             + self.corrupcao // 40 + bonus)
        return max(1, min(12, n))

    def inimigo(self, familia, bonus=0, afixo=None, nome_unico=None, nivel=None):
        return criar(self.rng, familia, nivel or self.nivel_inimigo(bonus), afixo, nome_unico)

    def afixo_aleatorio(self):
        p = 0.10 + self.loc["perigo"] * 0.03 + self.corrupcao / 400
        if self.j.nivel <= 1 or not self.chance(p):
            return None
        if self.corrupcao >= 30 and self.chance(self.corrupcao / 150):
            return "corrompido"
        return self.sortear(["feroz", "robusto", "agil", "venenoso", "anciao", "flamejante"])

    def familias_locais(self):
        familias = list(BIOMAS[self.bioma]["familias"])
        if self.corrupcao >= 40:
            familias.append("cria_vazio")
        if self.corrupcao >= 70:
            familias.append("abominacao")
        if self.noite and self.bioma in ("ruinas", "pantano", "planicie"):
            familias.append("espectro")
        return familias

    def grupo(self, familia=None, n=None, bonus=0):
        familia = familia or self.sortear(self.familias_locais())
        f = FAMILIAS[familia]
        if n is None:
            lo, hi = f["grupo"]
            n = self.rng.randint(lo, hi)
            if self.j.nivel <= 2:
                n = 1 if self.chance(0.7) else min(n, 2)
            elif self.j.nivel <= 4:
                n = min(n, 2)
        grupo = [self.inimigo(familia, bonus, self.afixo_aleatorio()) for _ in range(n)]
        if n == 1 and f["grupo"][1] == 1 and self.j.nivel >= 3 and self.chance(0.2):
            outra = self.sortear(BIOMAS[self.bioma]["familias"])
            if FAMILIAS[outra]["grupo"][1] > 1:
                grupo.append(self.inimigo(outra, bonus))
        return grupo

    def combate(self, inimigos, emboscada=None, pode_fugir=True, titulo=None):
        r = Combate(self, inimigos, emboscada, pode_fugir, titulo).executar()
        if r == "derrota":
            causa = f"Você tombou diante de {tx.lista_natural([e.nome for e in inimigos])}."
            if self.hardcore:
                self.fim_de_jogo(causa)
            self.dizer(causa, "vermelho+negrito")
            raise Derrota()
        if r == "fuga" and not self.nemesis:
            elite = next((e for e in inimigos if e.vivo and (e.afixo or e.unico) and not e.chefe
                          and e.familia in FAMILIAS and not e.chave), None)
            if elite:
                nome = elite.nome.split(",")[0] if elite.unico else tx.nome_proprio(self.rng)
                self.nemesis = {"familia": elite.familia, "afixo": elite.afixo or "feroz", "nome": nome,
                                "nivel": elite.nivel + 1, "pronto": self.passos + 4, "vezes": 0}
                self.dizer("Enquanto foge, você ouve um rugido às suas costas. Algo te marcou como presa. "
                           "Você ainda vai rever essa criatura...", "magenta")
        return r

    def registrar_abates(self, derrotados):
        self.estatisticas["abates"] += len(derrotados)
        for e in derrotados:
            if e.chave == "nemesis":
                self.nemesis = None
                self.dizer("Seu nêmesis finalmente tomba. Você sente um peso sair dos ombros.", "verde+negrito")
                self.ganhar_ouro(30 + 10 * self.j.nivel)
            for c in self.contratos:
                if c.get("concluido"):
                    continue
                if c["tipo"] == "caca" and e.familia == c["familia"] and self.loc["id"] == c["local"]:
                    c["feito"] += 1
                    if c["feito"] >= c["total"]:
                        c["concluido"] = True
                        self.dizer(f"Contrato concluído: {c['desc']} Receba a recompensa em qualquer vila.", "verde")
                elif c["tipo"] == "alvo" and e.chave == c["chave"]:
                    c["concluido"] = True
                    self.dizer(f"Contrato concluído: {c['desc']} Receba a recompensa em qualquer vila.", "verde")

    def saque_de_combate(self, derrotados):
        elites = sum(1 for e in derrotados if e.afixo or e.unico)
        chefe = any(e.chefe for e in derrotados)
        if self.chance(0.3 + 0.1 * elites):
            self.dar(self.sortear(["pocao_vida", "pocao_vida", "tonico", "antidoto", "bandagem"]))
        if self.j.classe == "arqueiro" and any(e.familia in ("bandido", "mercenario") for e in derrotados) \
                and self.chance(0.5):
            self.dizer("Você encontra uma aljava com flechas entre os pertences dos inimigos.", "verde")
            self.dar_flechas(self.rng.randint(3, 8))
        if chefe or self.chance(0.07 + 0.2 * elites):
            self.oferecer_equip(gerar_equip(self.rng, self.j.classe, self.j.nivel, qualidade=1 if chefe else 0))

    # ================================================================ equipamento e itens
    def oferecer_equip(self, item):
        self.dizer(f"Você encontrou: {item['nome']} [{NOMES_SLOT[item['slot']]}] — {descrever_bonus(item['bonus'])}",
                   "amarelo+negrito")
        atual = self.j.equip[item["slot"]]
        if atual:
            self.dizer(f"  Equipado agora: {atual['nome']} — {descrever_bonus(atual['bonus'])}", "cinza")
        op = self.menu("O que fazer com o item?", [
            ("Equipar agora", "equipar"),
            ("Guardar na mochila (para vender ou usar depois)", "guardar") if len(self.j.mochila) < LIMITE_MOCHILA
            else None,
            ("Deixar para trás", "deixar"),
        ])
        if op == "equipar":
            self.equipar(item)
        elif op == "guardar":
            self.j.mochila.append(item)
            self.dizer("Guardado na mochila.", "cinza")

    def equipar(self, item):
        j = self.j
        antigo = j.equip[item["slot"]]
        j.equip[item["slot"]] = item
        if item in j.mochila:
            j.mochila.remove(item)
        if antigo:
            if len(j.mochila) < LIMITE_MOCHILA:
                j.mochila.append(antigo)
            else:
                self.dizer(f"Mochila cheia: {antigo['nome']} fica para trás.", "cinza")
        j.recalcular()
        self.dizer(f"Você equipa {item['nome']}.", "verde")

    def usar_consumivel(self, k):
        j = self.j
        if not j.tem(k):
            return False
        j.consumiveis[k] -= 1
        nome = CONSUMIVEIS[k]["nome"]
        if k == "pocao_vida":
            c = j.curar(j.max_hp * 0.4)
            self.dizer(f"Você bebe a {nome}. (+{c} vida)", "verde")
        elif k == "tonico":
            ganho = min(j.max_rec - j.rec, j.max_rec // 2)
            j.rec += ganho
            self.dizer(f"Você bebe o {nome}. (+{ganho} {j.nome_recurso})", "azul")
        elif k == "antidoto":
            j.remover("veneno")
            self.dizer("O veneno deixa seu corpo.", "verde")
        elif k == "bandagem":
            j.remover("sangramento")
            c = j.curar(10)
            self.dizer(f"Você enfaixa as feridas. (+{c} vida)", "verde")
        else:
            j.consumiveis[k] += 1
            self.dizer("Isso não tem uso agora.", "cinza")
            return False
        return True

    # ================================================================ progressão
    def subir_nivel(self):
        j = self.j
        j.nivel += 1
        cresc = dict(CLASSES[j.classe]["cresc"])
        if j.spec:
            for k, v in SPECS[j.spec]["cresc"].items():
                cresc[k] = cresc.get(k, 0) + v
        for k, v in cresc.items():
            j.base[k] += v
        j.recalcular()
        j.hp = j.max_hp
        j.rec = j.max_rec
        if j.companheiro:
            j.companheiro["max_hp"] += 5
            j.companheiro["atk"] += 1.5
            j.companheiro["hp"] = j.companheiro["max_hp"]
        self.ui.titulo(f"NÍVEL {j.nivel}!", "verde+negrito")
        self.dizer("Seus ferimentos se fecham e você se sente mais forte.", "verde")
        self._aprender_habilidades()
        if j.nivel >= 4 and not j.spec and f"encruzilhada_{j.classe}" not in self.forcados:
            self.forcados.append(f"encruzilhada_{j.classe}")
            self.dizer("Você sente que uma encruzilhada se aproxima em seu caminho...", "magenta")

    def _aprender_habilidades(self):
        j = self.j
        for h in habilidades_ate(j.classe, j.spec, j.nivel):
            if h not in j.habilidades:
                j.habilidades.append(h)
                self.dizer(f"Nova habilidade: {HABILIDADES[h]['nome']} — {HABILIDADES[h]['desc']}", "amarelo+negrito")

    def especializar(self, spec):
        j = self.j
        j.spec = spec
        for k, v in SPECS[spec]["bonus"].items():
            j.base[k] += v
        j.recalcular()
        j.hp = j.max_hp
        j.rec = j.max_rec
        self.ui.titulo(f"VOCÊ AGORA É {SPECS[spec]['nome'].upper()}", "magenta+negrito")
        self.dizer(SPECS[spec]["desc"], "magenta")
        self._aprender_habilidades()
        if spec == "patrulheiro":
            self.escolher_companheiro()

    def escolher_companheiro(self, tipo=None):
        if tipo is None:
            tipos = list(COMPANHEIROS)
            esc = self.ui.escolher("Qual animal atende ao seu chamado?",
                                   [f"{COMPANHEIROS[t]['nome']} — {COMPANHEIROS[t]['desc']}" for t in tipos])
            tipo = tipos[esc]
        c = COMPANHEIROS[tipo]
        nv = self.j.nivel
        nome = self.ui.perguntar(f"Como vai chamar seu {c['nome'].split()[0].lower()}? (Enter para '{c['nome']}')",
                                 c["nome"])
        hp = int(c["hp"] * (1 + 0.15 * (nv - 1)))
        self.j.companheiro = {"nome": nome, "tipo": tipo, "max_hp": hp, "hp": hp,
                              "atk": c["atk"] * (1 + 0.2 * (nv - 1)), "agi": c["agi"],
                              "alcance": c["alcance"], "crit": c["crit"]}
        self.dizer(f"{nome} agora caminha ao seu lado.", "verde+negrito")

    # ================================================================ tempo e clima
    def rolar_clima(self):
        pesos = PESOS_CLIMA.get(self.bioma, PESOS_CLIMA["padrao"])
        self.clima = self.rng.choices(list(pesos), weights=list(pesos.values()))[0]

    def avancar_periodo(self):
        self.passos += 1
        self.periodo += 1
        if self.periodo == 3:
            self.dizer("A noite cai. Criaturas mais perigosas rondam no escuro.", "magenta")

    def novo_dia(self):
        self.dia += 1
        self.periodo = 0
        restantes = sum(1 for l in self.mundo["locais"] if l["tipo"] == "covil" and not l["guardiao"]["derrotado"])
        self.rolar_clima()
        self.rumores = [r for r in self.rumores if r["expira"] >= self.dia]
        self.impulsos = {}
        for r in self.rumores:
            if r.get("evento"):
                self.impulsos[r["evento"]] = self.impulsos.get(r["evento"], 1) * 3
        self.ui.separador()
        self.dizer(f"Amanhece o dia {self.dia}. {CLIMAS[self.clima]['desc']}", "amarelo")
        self.corromper(1 + restantes, silencioso=True)

    def descansar(self, fracao):
        j = self.j
        j.curar(j.max_hp * fracao)
        j.rec = j.max_rec
        j.efeitos = {}
        if j.companheiro:
            j.companheiro["hp"] = j.companheiro["max_hp"]

    # ================================================================ início
    def novo_jogo(self):
        self.ui.titulo("CRIAÇÃO DE PERSONAGEM")
        nome = self.ui.perguntar("Qual é o seu nome, aventureiro(a)?", "Aventureiro")
        self.dizer()
        self.dizer("Escolha sua classe. No nível 4 ela se ramifica em uma de duas especializações:", "ciano")
        classes = list(CLASSES)
        for c in classes:
            d = CLASSES[c]
            specs = " | ".join(SPECS[s]["nome"] for s in d["specs"])
            self.dizer(f"  {d['nome']} → {specs}", d["cor"] + "+negrito")
            self.dizer(f"    {d['desc']}", "cinza")
        esc = self.ui.escolher("Sua classe:", [CLASSES[c]["nome"] for c in classes])
        self.iniciar(nome, classes[esc])
        self.introducao()

    def iniciar(self, nome, classe):
        self.j = Jogador(nome, classe)
        self.mundo = gerar_mundo(self.rng)
        self.loc["visitado"] = True
        self.rolar_clima()
        self.j.equip["arma"] = gerar_equip(self.rng, classe, 1, "arma", qualidade=-2)
        self.j.recalcular()
        self.j.hp = self.j.max_hp

    def introducao(self):
        a = self.antagonista
        self.ui.titulo("O REINO À BEIRA DO VAZIO")
        self.narrar(f"Há cem anos uma Fenda se abriu no coração do reino. Dela fala {a['nome']}, {a['origem']}.")
        self.narrar("Três guardiões monstruosos, corrompidos pela Fenda, guardam os Sigilos que selam o caminho até "
                    f"a {self.mundo['locais'][-1]['nome']}, onde {a['curto']} aguarda.")
        self.narrar("A cada dia que passa a corrupção cresce. Se chegar a 100%, tudo estará perdido. "
                    "Derrotar os guardiões faz a sombra recuar.")
        self.narrar(f"Você, {self.j.nome}, {self.j.nome_classe.lower()}, parte da vila de {self.loc['nome']}.")
        self.dizer("Dica: explore, aceite contratos, ouça rumores. Suas escolhas voltarão para você — "
                   "para o bem ou para o mal.", "cinza")
        self.pausar()

    # ================================================================ ciclo principal
    def rodar(self):
        try:
            while True:
                try:
                    self.tela()
                except Derrota:
                    self.resgate()
        except FimDeJogo:
            return

    def resgate(self):
        """Fora do modo hardcore, cair em combate custa ouro e tempo (e o tempo alimenta a corrupção)."""
        j = self.j
        self.estatisticas["quedas"] += 1
        locais = self.mundo["locais"]
        from .mundo import _distancias
        dist = _distancias(locais, self.loc["id"])
        vila = min((l for l in locais if l["tipo"] == "vila"), key=lambda l: dist.get(l["id"], 99))
        p = self.npc()
        self.ui.titulo("TUDO ESCURECE...", "vermelho+negrito")
        self.narrar(f"Você acorda numa cama de palha em {vila['nome']}, com o corpo enfaixado. {p['um'].capitalize()} "
                    f"{p['prof']} {p['traco']} te encontrou desacordado na estrada e te arrastou até "
                    f"aqui. Dois dias se passaram.", "cinza")
        perda = self.perder_ouro(j.ouro * 0.3)
        if perda:
            self.dizer("Parte do seu ouro sumiu enquanto você estava desacordado.", "cinza")
        self.mundo["atual"] = vila["id"]
        vila["visitado"] = True
        j.efeitos = {}
        j.rec = j.max_rec
        if j.companheiro:
            j.companheiro["hp"] = j.companheiro["max_hp"]
        j.hp = max(j.hp, int(j.max_hp * 0.4))
        self.novo_dia()
        self.novo_dia()
        self.pausar()

    def cabecalho(self):
        j = self.j
        loc = self.loc
        ui = self.ui
        ui.titulo(f"Dia {self.dia} · {PERIODOS[min(self.periodo, 3)]} · {CLIMAS[self.clima]['nome']}"
                  f"   |   Corrupção {self.corrupcao}%", "amarelo")
        tipo = {"vila": "Vila", "selvagem": BIOMAS[loc["bioma"]]["nome"], "covil": BIOMAS[loc["bioma"]]["nome"],
                "cidadela": "Cidadela"}[loc["tipo"]]
        ui.dizer(f" {loc['nome']} — {tipo} · Perigo {tx.estrelas(loc['perigo'])}", "negrito")
        ui.dizer(f" {j.nome}, {j.nome_classe} Nv.{j.nivel}  (XP {j.xp}/{j.xp_proximo()})  "
                 f"Sigilos {len(j.sigilos)}/3", "ciano")
        linha = (f" Vida {ui.barra(j.hp, j.max_hp, 14)} {j.hp}/{j.max_hp}   {j.nome_recurso} {j.rec}/{j.max_rec}"
                 f"   Ouro {j.ouro}")
        if j.classe == "arqueiro":
            linha += f"   Flechas {j.flechas}"
        ui._imprimir(linha)
        if j.companheiro:
            c = j.companheiro
            ui._imprimir(f" {c['nome']} {ui.barra(c['hp'], c['max_hp'], 8, 'ciano')} {c['hp']}/{c['max_hp']}")
        ui.separador()

    def tela(self):
        if self.periodo > 3:
            self.exausto()
        self.cabecalho()
        tipo = self.loc["tipo"]
        if tipo == "vila":
            self.menu_vila()
        else:
            self.menu_selvagem()

    def opcoes_comuns(self):
        return [
            ("Viajar", "viajar"),
            ("Personagem e inventário", "personagem"),
            ("Mapa", "mapa"),
            ("Diário (contratos, rumores, aliados)", "diario"),
            ("Salvar jogo", "salvar"),
            ("Sair do jogo", "sair"),
        ]

    def executar_comum(self, op):
        acoes = {"viajar": self.viajar, "personagem": self.personagem, "mapa": self.mapa,
                 "diario": self.diario, "salvar": self.salvar, "sair": self.sair}
        acoes[op]()

    def menu_selvagem(self):
        loc = self.loc
        opcoes = []
        if loc["tipo"] == "covil" and not loc["guardiao"]["derrotado"]:
            opcoes.append((f"Enfrentar {loc['guardiao']['nome']} (guardião)", "chefe"))
        if loc["tipo"] == "cidadela":
            opcoes.append((f"Invadir o salão do trono e enfrentar {self.antagonista['curto']}", "final"))
        opcoes.append(("Explorar a região" + (" (à noite é mais perigoso)" if self.noite else ""), "explorar"))
        opcoes.append(("Acampar e descansar até o amanhecer", "acampar"))
        op = self.menu("O que você faz?", opcoes + self.opcoes_comuns())
        if op == "chefe":
            self.enfrentar_guardiao()
        elif op == "final":
            self.batalha_final()
        elif op == "explorar":
            self.explorar()
        elif op == "acampar":
            self.acampar()
        else:
            self.executar_comum(op)

    def menu_vila(self):
        j = self.j
        preco_dormir = self.preco(8 + 2 * j.nivel)
        faltando = j.max_hp - j.hp
        preco_templo = self.preco(max(1, faltando // 3)) if faltando else 0
        opcoes = [
            ("Passear pela vila", "passear"),
            (f"Taverna: dormir até amanhã ({preco_dormir} ouro)", "dormir"),
            (f"Taverna: pagar uma bebida e ouvir rumores ({self.preco(3)} ouro)", "rumores"),
            ("Mercado", "loja"),
            ("Mural de contratos", "mural"),
            (f"Templo: tratar ferimentos ({preco_templo} ouro)", "templo") if faltando else None,
        ]
        op = self.menu(f"Você está em {self.loc['nome']}. O que faz?", opcoes + self.opcoes_comuns())
        if op == "passear":
            if not eventos.disparar(self, "vila"):
                self.dizer("A vila segue sua rotina. Nada de especial acontece.", "cinza")
            self.avancar_periodo()
            self.pausar()
        elif op == "dormir":
            self.dormir_taverna(preco_dormir)
        elif op == "rumores":
            self.ouvir_rumores()
        elif op == "loja":
            self.loja()
        elif op == "mural":
            self.mural()
        elif op == "templo":
            if self.j.ouro < preco_templo:
                self.dizer("Você não tem ouro suficiente.", "vermelho")
            else:
                self.perder_ouro(preco_templo)
                self.curar(faltando)
                self.dizer("Um clérigo trata suas feridas com unguentos e orações.", "verde")
        else:
            self.executar_comum(op)

    def preco(self, base):
        fator = 1 - self.j.reputacao / 200
        return max(1, int(round(base * fator)))

    def exausto(self):
        self.ui.separador()
        if self.loc["tipo"] == "vila":
            self.dizer("Exausto, você pede abrigo num estábulo e dorme sobre o feno.", "cinza")
            self.descansar(0.5)
            self.novo_dia()
        else:
            self.dizer("Você está exausto demais para continuar. É preciso acampar.", "cinza")
            self.acampar()

    # ================================================================ ações no mundo
    def explorar(self):
        self.ui.separador()
        self.dizer(self.ambiente(), "cinza")
        if not eventos.disparar(self, "explorar"):
            self.dizer("Você vasculha a área, mas não encontra nada digno de nota.", "cinza")
        self.avancar_periodo()
        self.pausar()

    def acampar(self):
        self.ui.separador()
        self.dizer("Você junta gravetos, acende uma pequena fogueira e se enrola na capa.", "cinza")
        if self.chance(0.45):
            eventos.disparar(self, "acampamento")
        self.descansar(0.6)
        self.novo_dia()
        self.pausar()

    def dormir_taverna(self, preco):
        if self.j.ouro < preco:
            self.dizer("Sem ouro suficiente. O taverneiro aponta para a porta.", "vermelho")
            return
        self.perder_ouro(preco)
        self.dizer("Uma cama de verdade, uma refeição quente. Você dorme como pedra.", "verde")
        self.descansar(1.0)
        self.novo_dia()
        self.pausar()

    def viajar(self):
        origem = self.loc
        opcoes = []
        for loc, dist in vizinhos(self.mundo, origem):
            if loc["tipo"] == "vila":
                desc = "vila"
            elif loc["tipo"] == "cidadela":
                desc = "CIDADELA" + ("" if len(self.j.sigilos) >= 3 else " — selada")
            else:
                desc = BIOMAS[loc["bioma"]]["nome"]
                if loc["tipo"] == "covil" and (loc["visitado"] or self.flag(f"conhecido:{loc['id']}")):
                    desc += ", covil" + (" (derrotado)" if loc["guardiao"]["derrotado"] else "")
            marca = "" if loc["visitado"] else " · inexplorado"
            opcoes.append((f"{loc['nome']} ({desc}) — {dist} trecho{'s' if dist > 1 else ''}{marca}",
                           (loc, dist)))
        opcoes.append(("Voltar", None))
        destino = self.menu("Para onde?", opcoes)
        if not destino:
            return
        loc, dist = destino
        if loc["tipo"] == "cidadela" and len(self.j.sigilos) < 3:
            self.dizer(f"Uma muralha de sombras bloqueia o caminho. Você precisa dos três Sigilos "
                       f"({len(self.j.sigilos)}/3).", "magenta")
            return
        for trecho in range(dist):
            if self.periodo > 3:
                self.dizer("A noite está avançada demais para seguir viagem.", "cinza")
                self.acampar()
            if trecho >= dist / 2:
                self.mundo["atual"] = loc["id"]
            self.ui.separador()
            self.dizer(f"Viagem para {loc['nome']} — trecho {trecho + 1}/{dist}.", "ciano")
            if self.chance(0.65):
                eventos.disparar(self, "viagem")
            else:
                self.dizer(self.ambiente() + " A viagem segue sem incidentes.", "cinza")
            self.avancar_periodo()
        self.chegar(loc)

    def chegar(self, loc):
        self.mundo["atual"] = loc["id"]
        primeira = not loc["visitado"]
        loc["visitado"] = True
        if self.chance(0.5):
            self.rolar_clima()
        self.ui.separador()
        self.dizer(f"Você chega a {loc['nome']}.", "amarelo+negrito")
        if primeira and loc["tipo"] != "vila":
            self.dizer(self.ambiente(), "cinza")
        if loc["tipo"] == "covil" and not loc["guardiao"]["derrotado"]:
            g = loc["guardiao"]
            self.dizer(f"Este é o covil de {g['nome']}. Um dos Sigilos está aqui.", "magenta")
        if loc["tipo"] == "cidadela":
            self.dizer(f"Os três Sigilos ardem em sua mão e a muralha de sombras se abre. "
                       f"{tx.maiuscula(self.antagonista['curto'])} sabe que você chegou.", "magenta+negrito")
        if loc["tipo"] == "vila":
            self.receber_contratos()
            if self.chance(0.35):
                eventos.disparar(self, "vila")
        self.pausar()

    # ================================================================ vila: rumores, loja, mural
    def ouvir_rumores(self):
        chave = f"rumores:{self.dia}:{self.loc['id']}"
        if self.flag(chave, 0) >= 2:
            self.dizer("Os fregueses já contaram tudo o que sabiam hoje.", "cinza")
            return
        preco = self.preco(3)
        if self.j.ouro < preco:
            self.dizer("Sem ouro nem para uma caneca.", "vermelho")
            return
        self.perder_ouro(preco)
        self.marcar(chave, self.flag(chave, 0) + 1)
        ouvir_rumor(self)

    def estoque(self):
        chave = f"{self.loc['id']}:{self.dia // 3}"
        if chave not in self.lojas:
            prefixo = f"{self.loc['id']}:"
            self.lojas = {k: v for k, v in self.lojas.items() if not k.startswith(prefixo)}
            itens = [gerar_equip(self.rng, self.j.classe, self.j.nivel + self.rng.choice([0, 0, 1])) for _ in range(4)]
            self.lojas[chave] = itens
        return self.lojas[chave]

    def loja(self):
        while True:
            j = self.j
            self.ui.separador()
            self.dizer(f"MERCADO — seu ouro: {j.ouro}", "amarelo+negrito")
            itens = self.estoque()
            opcoes = []
            for k in ("pocao_vida", "tonico", "antidoto", "bandagem", "bomba_fumaca", "pena_fenix"):
                c = CONSUMIVEIS[k]
                opcoes.append((f"{c['nome']} — {self.preco(c['preco'])} ouro (você tem {j.consumiveis.get(k, 0)})",
                               ("consumivel", k)))
            if j.classe == "arqueiro":
                opcoes.append((f"Feixe de 10 flechas — {self.preco(8)} ouro (você tem {j.flechas})", ("flechas",)))
            for it in itens:
                opcoes.append((f"{it['nome']} [{NOMES_SLOT[it['slot']]}] {descrever_bonus(it['bonus'])} — "
                               f"{self.preco(it['preco'])} ouro", ("equip", it)))
            if j.mochila:
                opcoes.append(("Vender itens da mochila", ("vender",)))
            opcoes.append(("Sair do mercado", None))
            op = self.menu("Comprar o quê?", [(o[0].replace("Sair do mercado", "Voltar"), o[1]) for o in opcoes])
            if op is None:
                return
            if op[0] == "vender":
                self.vender()
                continue
            preco = self.preco({"consumivel": lambda: CONSUMIVEIS[op[1]]["preco"], "flechas": lambda: 8,
                                "equip": lambda: op[1]["preco"]}[op[0]]())
            if j.ouro < preco:
                self.dizer("Ouro insuficiente.", "vermelho")
                continue
            if op[0] == "equip" and len(j.mochila) >= LIMITE_MOCHILA:
                self.dizer("Sua mochila está cheia.", "vermelho")
                continue
            self.perder_ouro(preco)
            if op[0] == "consumivel":
                self.dar(op[1])
            elif op[0] == "flechas":
                self.dar_flechas(10)
            else:
                itens.remove(op[1])
                self.oferecer_equip_comprado(op[1])

    def oferecer_equip_comprado(self, item):
        if self.menu(f"Equipar {item['nome']} agora?", [("Sim", True), ("Não, guardar na mochila", False)]):
            self.equipar(item)
        else:
            self.j.mochila.append(item)

    def vender(self):
        j = self.j
        opcoes = [(f"{it['nome']} — {descrever_bonus(it['bonus'])} — vende por {it['preco'] // 2}", it)
                  for it in j.mochila]
        it = self.menu("Vender o quê?", opcoes + [("Voltar", None)])
        if it:
            j.mochila.remove(it)
            self.ganhar_ouro(it["preco"] // 2)

    def gerar_contrato(self):
        j = self.j
        selvagens = [l for l in self.mundo["locais"] if l["tipo"] in ("selvagem", "covil")]
        vilas = [l for l in self.mundo["locais"] if l["tipo"] == "vila" and l["id"] != self.loc["id"]]
        tipo = self.sortear(["caca", "caca", "alvo", "alvo", "entrega"])
        cid = self.novo_id()
        ouro = int((25 + 12 * j.nivel) * self.rng.uniform(0.9, 1.3))
        xp = 20 + 12 * j.nivel
        if tipo == "entrega" and vilas:
            dest = self.sortear(vilas)
            objeto = self.sortear(["um baú lacrado", "uma carta com selo de cera negra", "um frasco de remédio",
                                   "um embrulho que se mexe às vezes", "as escrituras de uma fazenda",
                                   "um anel de noivado"])
            return {"id": cid, "tipo": "entrega", "destino": dest["id"], "objeto": objeto, "ouro": ouro, "xp": xp,
                    "desc": f"Levar {objeto} até {dest['nome']}."}
        loc = self.sortear(selvagens)
        fam = self.sortear(BIOMAS[loc["bioma"]]["familias"])
        f = FAMILIAS[fam]
        if tipo == "alvo":
            nome = tx.nome_proprio(self.rng)
            return {"id": cid, "tipo": "alvo", "local": loc["id"], "familia": fam, "nome": nome,
                    "chave": f"alvo:{cid}", "ouro": int(ouro * 1.5), "xp": int(xp * 1.5),
                    "desc": f"Caçar {nome}, {tx.artigo(f['g'], False)} {f['nome']} enorme que aterroriza "
                            f"{loc['nome']}."}
        total = self.rng.randint(2, 4)
        return {"id": cid, "tipo": "caca", "local": loc["id"], "familia": fam, "total": total, "feito": 0,
                "ouro": ouro, "xp": xp, "desc": f"Eliminar {total} {f['plural']} em {loc['nome']}."}

    def mural(self):
        vid = str(self.loc["id"])
        oferta = self.ofertas.get(vid)
        if not oferta or self.dia - oferta["dia"] >= 3:
            oferta = {"dia": self.dia, "lista": [self.gerar_contrato() for _ in range(3)]}
            self.ofertas[vid] = oferta
        while True:
            self.ui.separador()
            self.dizer(f"MURAL DE CONTRATOS — ativos: {len(self.contratos)}/3", "amarelo+negrito")
            opcoes = [(f"{c['desc']} (recompensa: {c['ouro']} ouro, {c['xp']} XP)", c) for c in oferta["lista"]]
            c = self.menu("Aceitar qual contrato?", opcoes + [("Voltar", None)])
            if not c:
                return
            if len(self.contratos) >= 3:
                self.dizer("Você já tem contratos demais.", "vermelho")
                continue
            oferta["lista"].remove(c)
            self.contratos.append(c)
            self.dizer("Contrato aceito.", "verde")
            if c["tipo"] == "alvo":
                self.marcar(f"conhecido:{c['local']}")
            if c["tipo"] == "entrega":
                self.plantar("pacote_suspeito", 3, contrato=c["id"])

    def receber_contratos(self):
        for c in list(self.contratos):
            entregue = c["tipo"] == "entrega" and c["destino"] == self.loc["id"]
            if entregue or c.get("concluido"):
                self.contratos.remove(c)
                self.dizer(f"Recompensa de contrato: {c['desc']}", "verde+negrito")
                self.ganhar_ouro(c["ouro"])
                self.mudar_reputacao(3)
                self.ganhar_xp(c["xp"])

    def contrato_alvo_aqui(self):
        for c in self.contratos:
            if c["tipo"] == "alvo" and c["local"] == self.loc["id"] and not c.get("concluido"):
                return c
        return None

    # ================================================================ telas de informação
    def personagem(self):
        while True:
            j = self.j
            self.ui.titulo(f"{j.nome} — {j.nome_classe} nível {j.nivel}")
            self.dizer(f"Vida {j.hp}/{j.max_hp}   {j.nome_recurso} {j.rec}/{j.max_rec}   Ataque {j.atk}   "
                       f"Defesa {j.defesa}   Agilidade {j.agi}   Poder {j.poder}")
            self.dizer(f"Reputação: {j.reputacao:+d}   Ouro: {j.ouro}" +
                       (f"   Flechas: {j.flechas}" if j.classe == "arqueiro" else ""))
            self.dizer("Equipamento:", "ciano")
            for slot, it in j.equip.items():
                self.dizer(f"  {NOMES_SLOT[slot]}: " + (f"{it['nome']} ({descrever_bonus(it['bonus'])})" if it
                                                        else "—"))
            self.dizer("Habilidades: " + ", ".join(HABILIDADES[h]["nome"] for h in j.habilidades), "ciano")
            cons = [f"{CONSUMIVEIS[k]['nome']} x{v}" for k, v in j.consumiveis.items() if v > 0]
            self.dizer("Bolsa: " + (", ".join(cons) if cons else "vazia"), "ciano")
            if j.mochila:
                self.dizer(f"Mochila ({len(j.mochila)}/{LIMITE_MOCHILA}): " +
                           ", ".join(it["nome"] for it in j.mochila), "ciano")
            if j.companheiro:
                c = j.companheiro
                self.dizer(f"Companheiro: {c['nome']} — vida {c['hp']}/{c['max_hp']}, ataque {int(c['atk'])}", "ciano")
            op = self.menu("", [
                ("Usar item da bolsa", "usar"),
                ("Equipar item da mochila", "equipar") if j.mochila else None,
                ("Voltar", None),
            ])
            if op is None:
                return
            if op == "usar":
                itens = [k for k in ("pocao_vida", "tonico", "antidoto", "bandagem") if j.tem(k)]
                k = self.menu("Usar:", [(CONSUMIVEIS[k]["nome"], k) for k in itens] + [("Voltar", None)])
                if k:
                    self.usar_consumivel(k)
            else:
                it = self.menu("Equipar:", [(f"{it['nome']} [{NOMES_SLOT[it['slot']]}] "
                                             f"{descrever_bonus(it['bonus'])}", it) for it in j.mochila]
                               + [("Voltar", None)])
                if it:
                    if it["classe"] and it["classe"] != j.classe:
                        self.dizer("Você não sabe usar isso.", "vermelho")
                    else:
                        self.equipar(it)

    def mapa(self):
        self.ui.titulo("MAPA CONHECIDO")
        locais = self.mundo["locais"]
        conhecidos = {l["id"] for l in locais if l["visitado"]}
        for l in locais:
            if l["visitado"]:
                conhecidos |= {int(i) for i in l["con"]}
        for l in locais:
            if l["id"] not in conhecidos:
                continue
            marca = " ◄ você está aqui" if l["id"] == self.loc["id"] else ""
            if l["tipo"] == "vila":
                tipo = "vila"
            elif l["tipo"] == "cidadela":
                tipo = "CIDADELA"
            else:
                tipo = BIOMAS[l["bioma"]]["nome"]
                if l["tipo"] == "covil" and (l["visitado"] or self.flag(f"conhecido:{l['id']}")):
                    tipo += ", covil" + (" ✓" if l["guardiao"]["derrotado"] else "")
            self.dizer(f"{l['nome']} ({tipo}) {tx.estrelas(l['perigo'])}{marca}",
                       "amarelo+negrito" if marca else ("negrito" if l["visitado"] else "cinza"))
            if l["visitado"]:
                ligacoes = [f"{locais[int(i)]['nome']} ({d})" for i, d in l["con"].items()]
                self.dizer("    ↳ " + ", ".join(ligacoes), "cinza")
        self.pausar()

    def diario(self):
        self.ui.titulo("DIÁRIO")
        a = self.antagonista
        self.dizer(f"Inimigo final: {a['nome']}, {a['origem']}.", "magenta")
        self.dizer(f"Sigilos: {len(self.j.sigilos)}/3   Corrupção: {self.corrupcao}%   Dia {self.dia}", "magenta")
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
        if self.aliados_finais:
            self.dizer("Aliados para a batalha final: " + ", ".join(x["nome"] for x in self.aliados_finais), "verde")
        self.pausar()

    # ================================================================ chefes
    def enfrentar_guardiao(self):
        loc = self.loc
        gspec = loc["guardiao"]
        t = GUARDIOES[gspec["bioma"]][gspec["idx"]]
        self.ui.titulo(gspec["nome"].upper(), "vermelho+negrito")
        self.narrar(t["intro"], "vermelho")
        chave = f"guardiao:{loc['id']}"
        if self.flag(f"fraqueza:{chave}"):
            self.dizer("Você se lembra do que ouviu sobre o ponto fraco desta criatura.", "verde")
        if not self.menu("Não haverá como fugir depois de começar.", [("Lutar!", True), ("Recuar por enquanto",
                                                                                         False)]):
            return
        nivel = max(loc["perigo"] + 1, self.j.nivel + 1)
        chefe = instanciar_guardiao(gspec, nivel)
        chefe.chave = chave
        r = self.combate([chefe], pode_fugir=False, titulo=f"GUARDIÃO: {gspec['nome']}")
        if r == "vitoria":
            gspec["derrotado"] = True
            self.j.sigilos.append(loc["bioma"])
            self.estatisticas["chefes"] += 1
            self.ui.titulo(f"SIGILO OBTIDO ({len(self.j.sigilos)}/3)", "amarelo+negrito")
            self.dizer("Uma runa ardente se grava na palma da sua mão.", "amarelo")
            self.corromper(-15)
            self.mudar_reputacao(5)
            if len(self.j.sigilos) >= 3:
                self.dizer(f"Os três Sigilos pulsam juntos. O caminho para {self.mundo['locais'][-1]['nome']} "
                           f"está aberto!", "magenta+negrito")
        self.avancar_periodo()
        self.pausar()

    def batalha_final(self):
        a = self.antagonista
        j = self.j
        self.ui.titulo(a["nome"].upper(), "magenta+negrito")
        falas = {
            "guerreiro": "Tanto aço, tanta coragem. Eu também empunhei uma espada, um dia.",
            "arqueiro": "Você mira bem. Mas como se acerta o que não tem coração?",
            "mago": "Você sente, não sente? O poder do Vazio chamando por você. Somos iguais.",
        }
        self.narrar(f"No topo da escadaria, {a['curto']} te espera num trono de pedra rachada.", "magenta")
        self.narrar(f"\"{j.nome}. {falas[j.classe]}\"", "magenta+negrito")
        if j.reputacao <= -20:
            self.narrar("\"E que reputação a sua! Matou, roubou, mentiu. Junte-se a mim — você já está no "
                        "meio do caminho.\"", "magenta")
        if j.reputacao >= 20:
            self.narrar("\"Herói do povo, é? Vamos ver se as preces deles te salvam.\"", "magenta")
        self.pausar()

        guarda = self.inimigo("cavaleiro_sombrio", nome_unico=tx.nome_proprio(self.rng), nivel=j.nivel + 1)
        self.dizer("Um cavaleiro de armadura negra se coloca entre vocês.", "vermelho")
        self.combate([guarda], pode_fugir=False, titulo="O ÚLTIMO GUARDA")

        chefe = instanciar_antagonista(a, max(j.nivel + 1, 8), self.corrupcao)
        if self.aliados_finais:
            self.ui.separador("verde")
            self.dizer("Mas você não está só.", "verde+negrito")
            dano_max = int(chefe.max_hp * 0.45)  # os aliados ajudam, mas o golpe final é seu
            for al in self.aliados_finais:
                self.narrar(al["texto"], "verde")
                if al["efeito"] == "dano":
                    perda = min(int(chefe.max_hp * al["valor"]), dano_max - (chefe.max_hp - chefe.hp))
                    if perda > 0:
                        chefe.hp -= perda
                        self.dizer(f"  ({a['curto']} perde {perda} de vida)", "verde")
                elif al["efeito"] == "cura":
                    j.hp = j.max_hp
                    self.dizer("  (vida restaurada)", "verde")
                elif al["efeito"] == "forca":
                    atual = j.efeito("fortalecido")
                    bonus = min(0.3, (atual["v"] if atual else 0) + 0.1)
                    j.aplicar("fortalecido", 99, bonus)
                    j.efeitos["fortalecido"]["v"] = bonus
                    self.dizer(f"  (seu dano aumenta em {int(bonus * 100)}% nesta batalha)", "verde")
            self.pausar()
        j.hp = max(j.hp, j.max_hp // 2)
        self.combate([chefe], pode_fugir=False, titulo="O FIM DE TODAS AS COISAS")
        self.vitoria()

    # ================================================================ finais
    def resumo(self):
        e = self.estatisticas
        j = self.j
        self.dizer(f"{j.nome}, {j.nome_classe} nível {j.nivel} — {self.dia} dias de jornada.", "ciano")
        self.dizer(f"Inimigos derrotados: {e['abates']}  ·  Guardiões: {e['chefes']}  ·  "
                   f"Eventos vividos: {e['eventos']}  ·  Ouro ganho: {e['ouro_ganho']}  ·  "
                   f"Quedas: {e.get('quedas', 0)}", "ciano")
        self.dizer(f"Semente do mundo: {self.seed} (use --seed para jogar o mesmo reino de novo)", "cinza")

    def fim_de_jogo(self, motivo):
        self.ui.titulo("FIM DE JOGO", "vermelho+negrito")
        self.narrar(motivo, "vermelho")
        self.resumo()
        self.pausar()
        raise FimDeJogo()

    def vitoria(self):
        j = self.j
        a = self.antagonista
        self.ui.titulo("VITÓRIA", "amarelo+negrito")
        self.narrar(f"{tx.maiuscula(a['curto'])} se desfaz como cinza ao vento. A Fenda se fecha com um "
                    f"suspiro que ecoa por todo o reino.", "amarelo")
        epilogos = {
            "paladino": "Os templos acendem velas em seu nome. Você se torna o escudo do reino.",
            "berserker": "Bardos cantam sobre a fúria que nem o Vazio conseguiu conter.",
            "patrulheiro": "Você volta às matas, onde cada árvore parece saudar seu retorno.",
            "sombra": "Ninguém sabe ao certo quem salvou o reino. É exatamente como você prefere.",
            "piromante": "Por anos, o céu sobre a Fenda brilha em tons de brasa. Sua marca.",
            "necromante": "Os vivos te temem, os mortos te agradecem. Você aprendeu a conviver com os dois.",
        }
        self.narrar(epilogos.get(j.spec, "Você volta para casa, mais velho do que os dias de viagem explicam."))
        if j.reputacao >= 20:
            self.narrar("Em cada vila por onde passa, crianças brincam de ser você.")
        elif j.reputacao <= -20:
            self.narrar("O reino está salvo, mas as portas se fecham quando você passa. Heróis nem sempre são amados.")
        if self.corrupcao >= 70:
            self.narrar("A vitória veio tarde: cicatrizes do Vazio marcarão estas terras por gerações.")
        elif self.corrupcao <= 25:
            self.narrar("A vitória veio a tempo: em poucas estações, nem parece que a sombra esteve aqui.")
        self.resumo()
        self.pausar()
        raise FimDeJogo()

    # ================================================================ salvar / carregar
    def sair(self):
        op = self.menu("Sair do jogo?", [("Salvar e sair", "salvar"), ("Sair sem salvar", "sair"),
                                         ("Cancelar", None)])
        if op is None:
            return
        if op == "salvar":
            self.salvar()
        raise FimDeJogo()

    def caminho_save(self):
        slug = re.sub(r"[^a-z0-9]+", "_", self.j.nome.lower()).strip("_") or "heroi"
        return os.path.join(self.pasta_saves, f"{slug}.json")

    def salvar(self):
        os.makedirs(self.pasta_saves, exist_ok=True)
        estado = self.rng.getstate()
        dados = {
            "versao": VERSAO_SAVE,
            "seed": self.seed,
            "rng": [estado[0], list(estado[1]), estado[2]],
            "jogador": self.j.para_dict(),
        }
        for campo in ("mundo", "dia", "periodo", "clima", "corrupcao", "passos", "flags", "historico", "contagem",
                      "impulsos", "sementes", "rumores", "contratos", "ofertas", "lojas", "nemesis",
                      "aliados_finais", "forcados", "proximo_id", "estatisticas", "hardcore"):
            dados[campo] = getattr(self, campo)
        caminho = self.caminho_save()
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False)
        self.dizer(f"Jogo salvo em {caminho}.", "verde")

    @classmethod
    def carregar(cls, ui, caminho, pasta_saves="saves"):
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
        g = cls(ui, dados["seed"], pasta_saves)
        r = dados.pop("rng")
        g.rng.setstate((r[0], tuple(r[1]), r[2]))
        g.j = Jogador.de_dict(dados.pop("jogador"))
        dados.pop("versao", None)
        dados.pop("seed", None)
        for campo, valor in dados.items():
            setattr(g, campo, valor)
        return g
