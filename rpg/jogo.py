"""Estado do jogo, ciclo principal e ações do jogador."""

import random

from . import eventos
from . import texto as tx
from .classes import CLASSES, SPECS
from .dados import BIOMAS, CLIMAS, FAMILIAS, PERIODOS
from .entidades import Jogador
from .itens import CONSUMIVEIS, gerar_equip
from . import comitiva
from . import sobrevivencia
from . import telemetria
from .telemetria import registrar
from .mundo import gerar_mundo
from .regras import (AMBIENTE_VILA, LIMITE_MOCHILA, NIVEL_MAXIMO, NIVEL_MIN_FAMILIA, NOMES_SLOT, NOMES_TESTE,
                     Derrota, FimDeJogo)
from .migracoes import VERSAO_SAVE
from .balanceamento import PRECO_FLECHAS
from .sistemas.testes import Testes
from .sistemas.recompensas import Recompensas
from .sistemas.confronto import Confronto
from .sistemas.inventario import Inventario
from .sistemas.progressao import Progressao
from .sistemas.tempo import Tempo
from .sistemas.bestiario import Bestiario
from .sistemas.servicos import Servicos
from .sistemas.loja import Loja
from .sistemas.contratos import Contratos
from .sistemas.navegacao import Navegacao
from .sistemas.chefes import Chefes
from .sistemas.finais import Finais
from .sistemas.persistencia import Persistencia


# O resto do código importa constantes e exceções daqui; elas moram em regras.py.
__all__ = ["Jogo", "Derrota", "FimDeJogo", "AMBIENTE_VILA", "LIMITE_MOCHILA", "NIVEL_MAXIMO", "NIVEL_MIN_FAMILIA",
           "NOMES_SLOT", "NOMES_TESTE", "PRECO_FLECHAS", "VERSAO_SAVE"]


class Jogo(Testes, Recompensas, Confronto, Inventario, Progressao, Tempo, Bestiario, Servicos, Loja, Contratos,
           Navegacao, Chefes, Finais, Persistencia):
    """O estado da partida e o ciclo principal. Cada sistema (loja, contratos, combate...) vive no seu
    módulo em rpg/sistemas/ e entra aqui como mixin."""

    def __init__(self, ui, seed=None, pasta_saves="saves", hardcore=True):
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
        self.recompra = []  # o que você vendeu nesta visita ao mercado: dá para desfazer pelo mesmo preço (não vai no save)
        self.nemesis = None
        self.aliados_finais = []
        self.forcados = []
        self.proximo_id = 1
        self.combate_ativo = None
        self.autosalvar = False  # ligado pelo menu principal quando há uma pessoa jogando
        self.comitiva = []
        self.reserva = []  # companheiros que esperam no acampamento
        self.evento_atual = None
        self.sem_luz = False
        self.espolio_aberto = None  # o quadro de espólio sendo juntado (tela gráfica; ver Recompensas.abrir_espolio)
        self.ambiente_visto = None  # (lugar, dia, período) da última frase de ambiente da vila (ver menu_vila)
        self.registro = []
        self.arquivo_run = None
        self.bestiario = {}
        self.lendas = []
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
        self.fechar_espolio()
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

    def confirmar(self, pergunta, opcoes, perigo=False):
        """Confirmar algo que a pessoa pediu pela tela (abandonar um contrato, viajar para onde é perigoso). A tela
        gráfica pergunta numa janela própria, por cima de tudo, em vez de no pé da página, onde a pergunta ficava
        esquecida enquanto a pessoa clicava em outra coisa; o texto pergunta como sempre.
        opcoes: [(rótulo, True|False)], na ordem em que aparecem. perigo: o "sim" tem consequência (fica vermelho)."""
        return self.menu(pergunta, [(r, v, {"confirmar": "sim" if v else "nao", **({"perigo": True} if v and perigo else {})})
                                    for r, v in opcoes])

    def menu(self, pergunta, opcoes):
        """opcoes: lista de (rótulo, chave) ou None (opção indisponível)."""
        self.fechar_espolio()  # o que se ganhou aparece antes de a pessoa escolher de novo
        validas = [o for o in opcoes if o]
        rotulos = [self._anotar_teste(o[0]) for o in validas]
        metas = [o[2] if len(o) > 2 else None for o in validas]
        self.ui.meta_opcoes = metas if any(metas) else None
        try:
            esc = self.ui.escolher(pergunta, rotulos)
        finally:
            self.ui.meta_opcoes = None
        chave = validas[esc][1]
        if self.evento_atual and self.comitiva:
            comitiva.reagir_escolha(self, self.evento_atual, chave)
        return chave

    def _anotar_teste(self, rotulo):
        """'(Destreza)' vira '(Destreza +3)': mostra quanto você soma ao dado."""
        if not self.j or "(" not in rotulo:
            return rotulo
        for attr, nome in NOMES_TESTE.items():
            marca = f"({nome})"
            if marca in rotulo:
                mod = self.mod_teste(attr)
                rotulo = rotulo.replace(marca, f"({nome} {mod:+d} no d20)")
        return rotulo

    def ambiente(self):
        return self.sortear(BIOMAS[self.bioma]["ambiente"])

    # ================================================================ início
    def novo_jogo(self):
        """Criação do personagem. Devolve False se a pessoa voltou ao título."""
        self.ui.cena("Criação de personagem", None, "menu")
        nome = self.ui.perguntar("Qual é o seu nome, aventureiro(a)?", "Aventureiro", voltar=True)
        if nome is None:
            return False
        self.dizer()
        self.dizer("Escolha sua classe. No nível 4 ela se ramifica em uma de duas especializações:", "ciano")
        classes = list(CLASSES)
        for c in classes:
            d = CLASSES[c]
            specs = " | ".join(SPECS[s]["nome"] for s in d["specs"])
            self.dizer(f"  {d['nome']} → {specs}", d["cor"] + "+negrito")
            self.dizer(f"    {d['desc']}", "cinza")
        classe = self.menu("Sua classe:", [(CLASSES[c]["nome"], c) for c in classes] + [("Voltar", None, {"voltar": True})])
        if classe is None:
            return False
        self.iniciar(nome, classe)
        self.introducao()
        return True

    def iniciar(self, nome, classe):
        self.j = Jogador(nome, classe)
        self.mundo = gerar_mundo(self.rng)
        self.loc["visitado"] = True
        self.rolar_clima()
        self.j.equip["arma"] = gerar_equip(self.rng, classe, 1, "arma", qualidade=-2)
        self.j.recalcular()
        self.j.hp = self.j.max_hp
        self.preparar_legado()
        registrar(self, "inicio", nome=nome, classe=classe, seed=self.seed, hardcore=self.hardcore,
                  stats=telemetria.instantaneo(self.j))

    def introducao(self):
        a = self.antagonista
        self.ui.cena("O reino à beira do Vazio", "prólogo", "evento")
        self.narrar("Não houve profecia. Não há escolhido. Há cem anos uma Fenda se abriu sob a catedral, e desde "
                    "então o reino apodrece devagar, como um corpo que ainda não percebeu que morreu.", "cinza")
        self.narrar(f"Do outro lado fala {a['nome']}, {a['origem']}.")
        self.narrar("Três guardiões, deformados pela Fenda, guardam os Sigilos que selam o caminho até "
                    f"a {self.mundo['locais'][-1]['nome']}. Cavaleiros melhores que você já tentaram. Os corvos "
                    "ainda se lembram do gosto deles.")
        self.narrar(f"Você, {self.j.nome}, {self.j.nome_classe.lower()}, parte de {self.loc['nome']} com "
                    f"{tx.plural(self.j.provisoes, 'dia')} de comida, {tx.plural(self.j.ouro, 'moeda')} e nenhuma "
                    "garantia de voltar.")
        self.dizer("A fome mata. Feridas infeccionam. A noite cega. E a morte é permanente.", "vermelho+negrito")
        estatua = self.flag("estatua")
        if estatua:
            self.narrar(f"Na praça da vila há uma estátua nova: {estatua['nome']}, {estatua['nome_classe'].lower()}, "
                        f"que derrotou {estatua['antagonista']} em outra era. O povo olha para você com "
                        f"esperança. (reputação +5)", "amarelo")
        elif self.flag("tumulo"):
            t = self.flag("tumulo")
            self.narrar(f"Dizem que, em algum lugar destas terras, está o túmulo de {t['nome']}, quem tentou "
                        f"antes de você.", "cinza")
        self.dizer("Dica: compre provisões e tochas antes de sair, trate feridas abertas com bandagens e não vá "
                   "aonde o mapa diz que os inimigos são fortes demais. Suas escolhas voltarão para você.", "cinza")
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
        """Fora do modo hardcore, cair em combate custa ouro e tempo."""
        j = self.j
        self.estatisticas["quedas"] += 1
        locais = self.mundo["locais"]
        from .mundo import _distancias
        dist = _distancias(locais, self.loc["id"])
        vila = min((l for l in locais if l["tipo"] == "vila"), key=lambda l: dist.get(l["id"], 99))
        p = self.npc()
        self.ui.cena("Tudo escurece...", None, "evento")
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
        self.novo_dia(descanso=0)
        self.novo_dia(descanso=1)
        self.pausar()

    def contexto_cena(self):
        return (f"{self.loc['nome']} • Dia {self.dia} • {PERIODOS[min(self.periodo, 3)]} • "
                f"{CLIMAS[self.clima]['nome']}")

    def cabecalho(self):
        j = self.j
        loc = self.loc
        ui = self.ui
        tipo = {"vila": "Vila", "selvagem": BIOMAS[loc["bioma"]]["nome"], "covil": BIOMAS[loc["bioma"]]["nome"],
                "cidadela": "Cidadela"}[loc["tipo"]]
        perigo = "" if loc["tipo"] == "vila" else f" • inimigos Nv.{self.nivel_local()}"
        ui.cena(loc["nome"], f"{tipo}{perigo} • Dia {self.dia} • {PERIODOS[min(self.periodo, 3)]} • "
                             f"{CLIMAS[self.clima]['nome']}", "local")
        if ui.hud:
            return  # o painel lateral já mostra o resto
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
        males = sobrevivencia.descrever(j)
        ui.dizer(f" Provisões {j.provisoes}  Tochas {j.consumiveis.get('tocha', 0)}"
                 + (f"  |  {', '.join(males)}" if males else ""), "vermelho" if males else "cinza")
        ui.separador()

    def tela(self):
        if self.autosalvar:
            try:
                self.salvar(silencioso=True)
            except OSError:
                pass
        if self.periodo > 3:
            self.exausto()
        self.cabecalho()
        tipo = self.loc["tipo"]
        if tipo == "vila":
            self.menu_vila()
        else:
            self.menu_selvagem()

    def opcoes_comuns(self):
        pontos = self.j.pontos_talento
        return [
            ("Viajar", "viajar", {"predio": "estrada"}),
            ("Talentos" + (f"  ★ {tx.plural(pontos, 'ponto')} para gastar!" if pontos else ""), "talentos"),
            ("Personagem e inventário", "personagem"),
            ("Comitiva" + ("  ✉ alguém quer conversar" if any(
                c["conversa"] for c in comitiva.estado(self)) else ""), "comitiva") if self.comitiva or self.reserva else None,
            ("Mapa", "mapa"),
            ("Diário (contratos, rumores, aliados)", "diario"),
            ("Bestiário", "bestiario"),
            ("Salvar jogo", "salvar"),
            ("Sair do jogo", "sair"),
        ] + self.opcoes_bolsa() + self.opcoes_conversa()

    USAVEIS_FORA = ("bandagem", "unguento", "pocao_vida", "tonico", "antidoto")

    def opcoes_bolsa(self):
        """Na tela gráfica, a bolsa do painel lateral é clicável: cada consumível vira uma opção escondida."""
        if not self.ui.bolsa_clicavel:
            return []
        opcoes = []
        for k in self.USAVEIS_FORA:
            if self.j.tem(k):
                opcoes.append((f"Usar {CONSUMIVEIS[k]['nome']}", ("usar", k), {"usar": k}))
                if k in ("bandagem", "pocao_vida"):
                    opcoes += [(f"Usar {CONSUMIVEIS[k]['nome']} em {comitiva.nome(m['id'])}", ("usar_em", k, m["id"]),
                                {"usar": k, "em": m["id"]}) for m in comitiva.membros(self)]
                    if self.j.companheiro:  # o animal do patrulheiro também
                        opcoes.append((f"Usar {CONSUMIVEIS[k]['nome']} em {self.j.companheiro['nome']}",
                                       ("usar_em", k, "fera"), {"usar": k, "em": "fera"}))
        return opcoes

    def opcoes_conversa(self):
        """Na tela gráfica, o ✉ de quem quer conversar (no painel da comitiva) abre a conversa direto, sem passar
        pela tela da Comitiva: cada conversa que espera vira uma opção escondida no menu do lugar."""
        if not self.ui.conversa_no_painel:
            return []
        return [(f"Conversar com {comitiva.nome(c['id'])}", ("falar", c["id"]), {"conversar": c["id"]})
                for c in comitiva.estado(self) if c["conversa"]]

    def executar_comum(self, op):
        if isinstance(op, tuple):  # o painel lateral: a bolsa e o ✉ da comitiva
            if op[0] == "falar":
                comitiva.falar(self, op[1])
            elif op[0] == "usar":
                self.usar_consumivel(op[1])
            else:
                self.usar_em_companheiro(op[1], op[2])
            return
        acoes = {"viajar": self.viajar, "personagem": self.personagem, "comitiva": lambda: comitiva.menu(self), "talentos": self.menu_talentos, "bestiario": self.ver_bestiario, "mapa": self.mapa,
                 "diario": self.diario, "salvar": self.salvar, "sair": self.sair}
        acoes[op]()

    def menu_selvagem(self):
        loc = self.loc
        opcoes = []
        if loc["tipo"] == "covil" and not loc["guardiao"]["derrotado"]:
            opcoes.append((f"Enfrentar {loc['guardiao']['nome']} (guardião)", "chefe"))
        if loc["tipo"] == "cidadela":
            opcoes.append((f"Invadir o salão do trono e enfrentar {self.antagonista['curto']}", "final"))
        for c in self.contratos_aqui():
            if c["tipo"] == "alvo":
                rotulo = f"Rastrear {c['nome']} (contrato)"
            else:
                rotulo = f"Caçar {FAMILIAS[c['familia']]['plural']} (contrato, {c['feito']}/{c['total']})"
            opcoes.append((rotulo, f"cacar:{c['id']}", {"cacar": c["id"]}))
        opcoes.append(("Explorar a região" + (" (à noite é mais perigoso)" if self.noite else ""), "explorar"))
        opcoes.append(("Acampar e descansar até o amanhecer", "acampar"))
        op = self.menu("O que você faz?", opcoes + self.opcoes_comuns())
        if isinstance(op, str) and op.startswith("cacar:"):
            c = next((c for c in self.contratos if f"cacar:{c['id']}" == op), None)
            if c:
                self.cacar(c)
        elif op == "chefe":
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
        # Cada serviço diz a que prédio da vila pertence (na tela gráfica, a vila é um lugar com prédios clicáveis).
        # Os que se escolhem diante do prédio (a taverna, o templo) levam o rótulo curto, o preço, o que dão e o tempo
        # que gastam: a tela os desenha em cartões. Os outros abrem a tela do serviço direto.
        opcoes = [
            ("Passear pela vila", "passear", {"tempo": "1 período"}),
            (f"Taverna: dormir até amanhã ({preco_dormir} ouro)", "dormir",
             {"predio": "taverna", "servico": "dormir", "curto": "Dormir até amanhã", "preco": preco_dormir, "tempo": "até amanhã",
              "efeito": f"Descanso, {j.nome_recurso.lower()} de volta e ensopado para todos"}),
            (f"Taverna: pagar uma bebida e ouvir rumores ({self.preco(3)} ouro)", "rumores",
             {"predio": "taverna", "servico": "rumores", "curto": "Uma bebida e os rumores", "preco": self.preco(3),
              "efeito": "O que se conta nas mesas"}),
            ("Mercado", "loja", {"predio": "mercado"}),
            ("Mural de contratos", "mural", {"predio": "mural"}),
            *self.opcoes_templo(),
            ("Curandeira: tratar ferimentos e infecções", "curandeiro", {"predio": "curandeiro"}) if j.ferimentos else None,
            ("Ferreiro: reforçar arma ou armadura", "ferreiro", {"predio": "ferreiro"}),
        ]
        # A frase da vila aparece na chegada e quando o tempo passa, não a cada volta ao menu (do mercado, do
        # inventário). O sorteio segue a cada volta: com a mesma semente, a partida continua a mesma.
        ambiente = self.sortear(AMBIENTE_VILA)
        if self.ambiente_visto != (self.loc["id"], self.dia, self.periodo):
            self.ambiente_visto = (self.loc["id"], self.dia, self.periodo)
            self.dizer(ambiente, "cinza")
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
        elif op == "curandeiro":
            self.curandeiro()
        elif op == "ferreiro":
            self.ferreiro()
        elif isinstance(op, tuple) and op[0] == "templo":
            self.templo(*op[1:])
        else:
            self.executar_comum(op)

    # ================================================================ ações no mundo
    def explorar(self):
        self.ui.cena("Explorando", self.contexto_cena(), "evento")
        self.narrar(self.ambiente(), "cinza")
        sobrevivencia.acender_tocha(self)
        try:
            if not eventos.disparar(self, "explorar"):
                self.dizer("Você vasculha a área, mas não encontra nada digno de nota.", "cinza")
        finally:
            self.sem_luz = False
        self.avancar_periodo()
        self.pausar()
