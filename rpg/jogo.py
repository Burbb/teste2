"""Estado do jogo, ciclo principal e ações do jogador."""

import random

from . import campanha
from .campanha import INICIO
from . import abertura, consequencias, criacao, missoes
from . import eventos
from . import texto as tx
from .classes import CLASSES, SPECS
from .dados import BIOMAS, CLIMAS, FAMILIAS, PERIODOS
from .entidades import Jogador
from .itens import CONSUMIVEIS, EM_ALIADO, USAVEIS_FORA, gerar_equip
from . import comitiva
from . import sobrevivencia
from . import telemetria
from .telemetria import registrar
from .regras import (AMBIENTE_VILA, LIMITE_MOCHILA, NIVEL_MAXIMO, NOMES_SLOT, NOMES_TESTE,
                     Derrota, FimDeJogo)
from .migracoes import VERSAO_SAVE
from . import balanceamento as bal
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
__all__ = ["Jogo", "Derrota", "FimDeJogo", "AMBIENTE_VILA", "LIMITE_MOCHILA", "NIVEL_MAXIMO",
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
        self.na_fogueira = False  # em volta do fogo, à noite: um dos lugares seguros para abrir um baú
        self.na_estrada = False  # entre um lugar e outro: a tela desenha a estrada (a região), não a vila de partida ou de chegada
        self.titulo_espolio = None
        self.frase_espolio = None
        self.nemesis = None
        self.forcados = []
        self.proximo_id = 1
        self.combate_ativo = None
        self.queda_pendente = None  # a fome ou a infecção derrubou o herói nesta noite (só a campanha com resgate)
        self.resgatando = False     # os dois dias do resgate: nada derruba de novo enquanto ele é tratado
        self.amanhecer_adiado = None  # nesses dias, o que a comitiva diz ao amanhecer (o soldo) espera o herói acordar
        self.autosalvar = False  # ligado pelo menu principal quando há uma pessoa jogando
        self.comitiva = []
        self.reserva = []  # companheiros que esperam no acampamento
        self.evento_atual = None
        self.sem_luz = False
        self.luz_na_sala = None  # a tocha acesa na última luta de sala (só para a arte; não vai no save)
        self.luz_onde = None     # a sala em que ela continua acesa na página (missoes._acender)
        self.espolio_aberto = None  # o quadro de espólio sendo juntado (tela gráfica; ver Recompensas.abrir_espolio)
        self.ambiente_visto = None  # (lugar, dia, período) da última frase de ambiente da vila (ver menu_vila)
        self.registro = []
        self.arquivo_run = None
        self.bestiario = {}
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
    def campanha(self):
        """O id da região da campanha ("turvo"); None antes de o jogo começar."""
        return self.mundo.get("campanha") if self.mundo else None

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
        """opcoes: lista de (rótulo, chave[, meta]) ou None (opção que não aparece). Meta `indisponivel` (o motivo):
        a opção aparece, mas não pode ser escolhida (falta o item que ela gasta, por exemplo)."""
        self.fechar_espolio()  # o que se ganhou aparece antes de a pessoa escolher de novo
        validas = [o for o in opcoes if o]
        rotulos = [self._anotar_teste(o[0]) for o in validas]
        metas = [o[2] if len(o) > 2 else None for o in validas]
        if not self.ui.notas_proprias:  # a nota da opção (custo, risco), a seta de quem abre outra escolha e o motivo
            # de uma indisponível: a tela gráfica desenha os três; o texto os junta ao rótulo
            rotulos = [r + (" ›" if m and m.get("abre") else "") + (f" — {m['nota']}" if m and m.get("nota") else "")
                       + (f" — {' '.join(x['linha'] for x in m['riscos'])}" if m and m.get("riscos") else "")
                       + (f" — indisponível: {m['indisponivel']}" if m and m.get("indisponivel") else "")
                       for r, m in zip(rotulos, metas)]
        self.ui.meta_opcoes = metas if any(metas) else None
        try:
            esc = self.ui.escolher(pergunta, rotulos)
            while metas[esc] and metas[esc].get("indisponivel"):  # a tela não deixa; o texto explica e pergunta de novo
                self.dizer(metas[esc]["indisponivel"], "cinza")
                esc = self.ui.escolher(pergunta, rotulos)
        finally:
            self.ui.meta_opcoes = None
        chave = validas[esc][1]
        if self.evento_atual and self.comitiva:
            comitiva.reagir_escolha(self, self.evento_atual, chave)
        return chave

    # A proteção que levanta você uma vez ao cair em combate (a flag `bencao_fenix`): o valor guarda de onde ela veio
    # ("santuario", "mendigo"); um save de antes guarda só True, e aí a origem fica sem nome (ORIGEM_PROTECAO[None]).
    AVISO_PROTECAO = "Proteção: se cair em combate, você se levanta uma vez"

    def receber_protecao(self, origem):
        self.marcar("bencao_fenix", origem)
        self.ui.efeito(self.AVISO_PROTECAO, "protecao")

    def custo_item(self, item, qtd=1):
        """A meta de uma opção que gasta um consumível: a nota com o que ela usa e quanto você tem, ou, faltando, a
        opção indisponível com o motivo (ela continua à vista)."""
        from .itens import CONSUMIVEIS
        nome, tem = CONSUMIVEIS[item]["nome"].lower(), self.j.consumiveis.get(item, 0)
        if tem >= qtd:
            return {"nota": f"Usa {qtd} {nome} da bolsa (você tem {tem}).", "gasta": item}
        return {"indisponivel": f"Você não tem {nome} na bolsa.", "gasta": item}

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
    def novo_jogo(self, regiao=INICIO):
        """Criação do personagem: nome, classe, o modo (resgate ou hardcore) e o tutorial; a campanha começa na região
        dada (campanha.py). Na tela gráfica, numa tela só (criacao.py); no texto, uma pergunta por vez. Devolve False se
        a pessoa voltou ao título."""
        escolha = self._criacao_na_tela(regiao) if self.ui.criacao_na_tela else self._criacao_em_perguntas(regiao)
        if escolha is None:
            return False
        nome, classe, self.hardcore, tutorial = escolha
        self.iniciar(nome, classe, regiao)
        abertura.comecar(self, tutorial)
        self.introducao_campanha()
        return True

    def _criacao_na_tela(self, regiao):
        """A tela anda pelas etapas e devolve tudo junto; o motor confere (a resposta que não serve volta à tela)."""
        d = criacao.dados(regiao)
        while True:
            resposta = self.ui.criar_personagem(d)
            if isinstance(resposta, dict) and resposta.get("voltar"):
                return None
            escolha = criacao.conferir(resposta)
            if escolha:
                return escolha

    def _criacao_em_perguntas(self, regiao):
        """No texto: o nome, a classe e o modo, com o tutorial numa pergunta depois (ler_caixa)."""
        self.ui.cena("Criação de personagem", campanha.nome(regiao), "menu")
        nome = self.ui.perguntar("Qual é o seu nome, aventureiro(a)?", "Aventureiro", voltar=True)
        if nome is None:
            return None
        self.dizer()
        self.dizer(f"Escolha sua classe. No nível {bal.NIVEL_ESPECIALIZACAO} ela se ramifica em uma de duas "
                   "especializações:", "ciano")
        classes = list(CLASSES)
        for c in classes:
            d = CLASSES[c]
            specs = " | ".join(SPECS[s]["nome"] for s in d["specs"])
            self.dizer(f"  {d['nome']} → {specs}", d["cor"] + "+negrito")
            self.dizer(f"    {d['desc']}", "cinza")
        while True:
            classe = self.menu("Sua classe:", [(CLASSES[c]["nome"], c) for c in classes] + [("Voltar", None, {"voltar": True})])
            if classe is None:
                return None
            # A caixa "Mostrar tutorial", marcada, junto da escolha do modo (no texto, uma pergunta depois): liga só as
            # orientações; a abertura é a mesma.
            self.ui.caixa = {"id": "tutorial", "rotulo": "Mostrar tutorial", "marcada": True,
                             "pergunta": "Mostrar as orientações do tutorial?"}
            try:
                modo = self.menu("Se você cair (em combate, de fome ou de infecção):", [
                    ("Resgate: alguém da vila te encontra e cuida de você (perde parte do ouro e dois dias)", "resgate"),
                    ("Hardcore: a morte é permanente e o save é apagado", "hardcore"),
                    ("Voltar", None, {"voltar": True}),
                ])
                tutorial = self.ui.ler_caixa() if modo else None
            finally:
                self.ui.caixa = None
            if modo:
                return nome, classe, modo == "hardcore", tutorial

    def iniciar(self, nome, classe, regiao=INICIO):
        self.j = Jogador(nome, classe)
        self.mundo = campanha.montar_mundo(regiao)
        self.loc["visitado"] = True
        self.rolar_clima()
        self.j.equip["arma"] = gerar_equip(self.rng, classe, 1, "arma", qualidade=-2)
        self.j.recalcular()
        self.j.hp = self.j.max_hp
        registrar(self, "inicio", nome=nome, classe=classe, seed=self.seed, hardcore=self.hardcore,
                  stats=telemetria.instantaneo(self.j), campanha=regiao)

    def introducao_campanha(self):
        """Prólogo provisório do protótipo: diz onde se está, o modo escolhido e o que ainda não existe. A história
        da região (Marta, a febre, a capela) entra com a missão, na E3."""
        r = campanha.REGIOES[self.campanha]
        self.ui.cena(r["nome"], "protótipo da campanha", "evento")
        self.narrar(f"A estrada termina no {self.loc['nome']}, uma vila de beira-rio no fundo do vale. Você, "
                    f"{self.j.nome}, {self.j.nome_classe.lower()}, chega com "
                    f"{tx.plural(self.j.provisoes, 'dia')} de comida e {tx.plural(self.j.ouro, 'moeda')}.")
        self.dizer("Protótipo: o mapa do vale e o começo da missão da região. O resto da história e os encontros "
                   "escritos chegam nas próximas entregas; por ora, o vale tem os encontros de sempre.", "ciano")
        if self.hardcore:
            self.dizer("Hardcore: a morte é permanente e o save é apagado.", "vermelho+negrito")
        else:
            self.dizer("Resgate: se você cair em combate, de fome ou de infecção, alguém da vila te encontra e cuida "
                       "de você, ao custo de parte do ouro e de dois dias.", "amarelo")
        self.dizer("A Estrada de Varn, ao sul, segue fechada por enquanto.", "cinza")
        self.dizer("Dica: compre provisões e tochas antes de sair e trate feridas abertas com bandagens.", "cinza")
        self.ui.continuar()

    # ================================================================ ciclo principal
    def rodar(self):
        try:
            while True:
                try:
                    self.tela()
                except Derrota as d:
                    self.resgate(d.causa)
        except FimDeJogo:
            return

    def resgate(self, causa="combate"):
        """Fora do modo hardcore, cair custa ouro e tempo. causa (Derrota.causa): "combate", "fome" ou "infeccao". O
        resgate também encerra a emergência (resgate_campanha)."""
        self.estatisticas["quedas"] += 1
        missoes.saiu_da_capela(self)  # quem volta à capela depois do resgate chega por fora
        self.resgate_campanha(causa)

    # A queda que a campanha explica: a fome e a infecção (a de combate já disse diante de quem o herói tombou).
    QUEDA_SEM_LUTA = {
        "fome": "A fome vence: as pernas falham e você cai no caminho.",
        "infeccao": "A febre da ferida infeccionada sobe de vez, e você apaga.",
    }

    def resgate_campanha(self, causa):
        """A queda na campanha (combate, fome ou infecção): alguém do Vau acha o herói e o leva para a casa de Marta.
        Custa 30% do ouro e dois dias. Mas os dois dias encerram a emergência: o herói e
        a comitiva comem lá (as provisões da bolsa ficam), a fome passa, a infecção é tratada e as feridas abertas,
        enfaixadas (não infeccionam). Os outros ferimentos seguem as regras de sempre. Quem cuida é Marta, se a água
        já limpou e ela está de pé; senão, Pita (consequencias.marta_de_pe). Uma queda, uma recuperação, uma
        cobrança: durante os dois dias, nada derruba o herói de novo (resgatando)."""
        j = self.j
        locais = self.mundo["locais"]
        from .mundo import _distancias
        dist = _distancias(locais, self.loc["id"])
        vila = min((l for l in locais if l["tipo"] == "vila"), key=lambda l: dist.get(l["id"], 99))
        self.mundo["atual"] = vila["id"]
        vila["visitado"] = True
        infeccao = sobrevivencia.tem(j, "infeccao")
        juntos = " e à comitiva" if comitiva.membros(self) else ""
        self.ui.cena("Tudo escurece...", None, "evento")
        if causa in self.QUEDA_SEM_LUTA:
            self.narrar(self.QUEDA_SEM_LUTA[causa], "vermelho")
        # O tratamento e os dois dias vêm antes do texto: quando ele diz o que aconteceu, o painel já mostra o herói
        # tratado, no Vau, dois dias depois (o quadro do amanhecer abre o despertar).
        j.fome = 0
        j.ferimentos = [f for f in j.ferimentos if f["id"] != "infeccao"]
        for f in j.ferimentos:
            if sobrevivencia.FERIMENTOS[f["id"]].get("aberto"):
                f["tratado"] = True
        j.recalcular()
        j.efeitos = {}
        j.rec = j.max_rec
        if j.companheiro:
            j.companheiro["hp"] = j.companheiro["max_hp"]
        j.hp = min(j.max_hp, max(j.hp, int(j.max_hp * 0.4)))
        self.resgatando = True
        self.amanhecer_adiado = {"famintos": [], "soldo": False}
        try:
            self.novo_dia(descanso=0, refeicao=True, quadro=False)  # um quadro só, no fim dos dois dias
            self.novo_dia(descanso=1, refeicao=True)
        finally:
            self.resgatando = False
            adiado, self.amanhecer_adiado = self.amanhecer_adiado, None
        marta = consequencias.marta_de_pe(self)  # depois dos dois dias: a água pode ter limpado neles
        quem = "Marta" if marta else "Pita"
        self.narrar("Alguém do Vau te acha desacordado e te leva para a casa de Marta. " +
                    ("Você acorda na mesma cama em que ela cuidou de você anos atrás. " if marta else
                     "Você acorda numa esteira, ao lado da cama em que ela ainda está doente. ") +
                    f"Dois dias se passaram. {quem} trocou as faixas e deu caldo a você{juntos}.")
        if infeccao:
            self.narrar(f"{quem} abriu e limpou a ferida infeccionada, e a febre passou.")
        perda = self.perder_ouro(j.ouro * 0.3, destino="resgate")
        if perda:
            self.dizer("Parte do seu ouro sumiu enquanto você estava desacordado.", "cinza")
        registrar(self, "resgate", causa=causa, perda=perda)
        # Só agora, acordado na casa de Marta e com o ouro que sobrou, a comitiva fala do amanhecer: o soldo de Morel,
        # se o sétimo dia caiu nos dois dias do resgate (antes, ele cobrava com o herói ainda caído na estrada).
        comitiva.depois_do_amanhecer(self, adiado["famintos"], adiado["soldo"])
        self.pausar()

    def contexto_cena(self):
        return (f"{self.loc['nome']} • Dia {self.dia} • {PERIODOS[min(self.periodo, 3)]} • "
                f"{CLIMAS[self.clima]['nome']}")

    def cabecalho(self):
        j = self.j
        loc = self.loc
        ui = self.ui
        tipo = "Vila" if loc["tipo"] == "vila" else BIOMAS[loc["bioma"]]["nome"]
        # O nível-base da região; à noite, o que ela soma vem ao lado, sem trocar o número (seção 8 do 18).
        perigo = ("" if loc["tipo"] == "vila" else f" • inimigos Nv.{self.nivel_local()}"
                  + (f" (+{bal.NOITE_NIVEL} à noite)" if self.noite else ""))
        sala = missoes.sala_atual(self)  # dentro da capela, a sala em que se está
        if sala and sala != "exterior":
            tipo += f" • {missoes.NOME_SALA[sala]}"
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
        for r in sobrevivencia.riscos_do_lugar(self, missoes.tem_salas(self)):
            ui.dizer(f" {r['texto']}", "amarelo")
        ui.separador()

    def tela(self):
        if self.autosalvar:
            try:
                self.salvar(silencioso=True)
            except OSError:
                pass
        if self.periodo > 3:
            self.exausto()
        if missoes.cena_pendente(self):  # a cena de missão deste lugar e desta etapa (só na campanha, uma vez)
            return
        if abertura.cena_pendente(self):  # o pedido do taverneiro (a despensa), uma vez, na campanha nova
            return
        self.cabecalho()
        tipo = self.loc["tipo"]
        if tipo == "vila":
            # Quem chega viajando já recebeu (chegar). Quem acorda aqui depois de um resgate, ou carrega um save feito
            # na vila com contrato cumprido e ainda não pago, recebe agora, na página da vila, depois do resgate.
            self.receber_contratos()
            self.menu_vila()
        else:
            self.menu_selvagem()

    def opcoes_comuns(self):
        """As opções de sistema de todo lugar. A meta `sistema` diz qual é cada uma: a tela gráfica monta a doca por
        ela (nunca pelo texto, que pode mudar)."""
        pontos = self.j.pontos_talento
        carta = (self.comitiva or self.reserva) and any(c["conversa"] for c in comitiva.estado(self))
        return [
            ("Viajar", "viajar", {"predio": "estrada"}),
            ("Talentos" + (f"  ★ {tx.plural(pontos, 'ponto')} para gastar!" if pontos else ""), "talentos",
             {"sistema": "talentos", "pontos": pontos}),
            ("Personagem e inventário", "personagem", {"sistema": "inventario"}),
            *self.opcoes_atributos(),  # os pontos da subida de nível (etapa 4): o "+" da ficha, ou uma linha
            ("Comitiva" + ("  ✉ alguém quer conversar" if carta else ""), "comitiva",
             {"sistema": "comitiva", "carta": bool(carta)}) if self.comitiva or self.reserva else None,
            ("Mapa", "mapa", {"sistema": "mapa"}),
            ("Diário (contratos, rumores)", "diario", {"sistema": "diario"}),
            ("Bestiário", "bestiario", {"sistema": "bestiario"}),
            ("Salvar jogo", "salvar", {"sistema": "salvar"}),
            ("Sair do jogo", "sair", {"sistema": "sair"}),
        ] + self.opcoes_bolsa() + self.opcoes_conversa()

    USAVEIS_FORA = USAVEIS_FORA  # o catálogo diz (itens.py: uso)

    def opcoes_bolsa(self):
        """Na tela gráfica, a bolsa do painel lateral é clicável: cada consumível vira uma opção escondida."""
        if not self.ui.bolsa_clicavel:
            return []
        opcoes = []
        for k in self.USAVEIS_FORA:
            if self.j.tem(k):
                # a pilha de baús abre inteira (Inventario.usar_consumivel): o rótulo diz quantos
                rotulo = (f"Abrir os {self.j.consumiveis[k]} baús trancados" if k == "bau" and self.j.consumiveis[k] > 1
                          else f"{'Abrir' if k == 'bau' else 'Usar'} {CONSUMIVEIS[k]['nome']}")
                opcoes.append((rotulo, ("usar", k), {"usar": k}))
                if k in EM_ALIADO:
                    opcoes += [(f"Usar {CONSUMIVEIS[k]['nome']} em {comitiva.nome(m['id'])}", ("usar_em", k, m["id"]),
                                {"usar": k, "em": m["id"]}) for m in comitiva.junto(self)]
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
        if op == "comitiva" or isinstance(op, tuple) and op[0] == "falar":
            abertura.visto(self, "V4")  # a comitiva aberta (a tela ou a conversa): o quadro que a apontava não volta
        if isinstance(op, tuple) and op[:2] == ("usar", "bau"):
            abertura.visto(self, "B1")  # o primeiro baú aberto: daqui, o saque e a comparação seguem como sempre
        if isinstance(op, tuple):  # o painel lateral: a bolsa e o ✉ da comitiva
            if op[0] == "falar":
                comitiva.falar(self, op[1])
            elif op[0] == "usar":
                if self.usar_consumivel(op[1]) and op[1] == "bandagem":
                    abertura.visto(self, "F2")  # a ferida enfaixada: o estado "tratado" dela mostra o resultado
            elif op[0] == "versao":
                self.trocar_versao(op[1], op[2])
            elif op[0] == "kit":
                self.mexer_kit(op[1])
            elif op[0] == "atributo":
                self.gastar_atributo(op[1])
            else:
                self.usar_em_companheiro(op[1], op[2])
            return
        acoes = {"viajar": self.viajar, "personagem": self.personagem, "comitiva": lambda: comitiva.menu(self), "talentos": self.menu_talentos, "atributos": self.menu_atributos, "bestiario": self.ver_bestiario, "mapa": self.mapa,
                 "diario": self.diario, "salvar": self.salvar, "sair": self.sair}
        acoes[op]()

    def menu_selvagem(self):
        missoes.mostrar_cena(self)  # na capela, o ambiente desenhado no topo (tela gráfica): antes de qualquer texto
        # Primeiro o que a missão pede aqui, depois os contratos, depois o de sempre: a tela marca cada grupo.
        opcoes = missoes.opcoes(self)
        for c in self.contratos_aqui():
            if c["tipo"] == "alvo":
                rotulo = f"Rastrear {c['nome']} (contrato)"
            else:
                rotulo = f"Caçar {FAMILIAS[c['familia']]['plural']} (contrato, {c['feito']}/{c['total']})"
            opcoes.append((rotulo, f"cacar:{c['id']}", {"cacar": c["id"]}))
        opcoes += missoes.passagens(self)  # na capela: as salas vizinhas já vencidas (só a vista muda)
        if missoes.pode_explorar(self):  # dentro da capela, não: explorar a região é do lado de fora
            opcoes.append(("Explorar a região" + (" (à noite é mais perigoso)" if self.noite else ""), "explorar"))
        # Dentro da capela, acampar é sair primeiro (sair_para_acampar): a fogueira nunca fica dentro de uma sala.
        dentro = missoes.sala_atual(self) not in (None, "exterior")
        opcoes.append(("Sair e acampar" if dentro else "Acampar e descansar até o amanhecer", "acampar"))
        if missoes.pode_explorar(self):
            abertura.motivo_explorar(self, "morel")  # com Morel junto, ele conta onde está o dinheiro (uma vez)
        if self.contratos_aqui():
            abertura.visto(self, "K2")  # chegou ao lugar do contrato: o quadro que mostrava onde ele fica não volta
        abertura.dica_texto(self, "fora")  # na interface de texto, a orientação da vez numa linha
        antes = abertura.proxima(self)
        op = self.menu("O que você faz?", opcoes + self.opcoes_comuns())
        abertura.depois_do_menu(self, antes, op)
        if isinstance(op, str) and op.startswith("cacar:"):
            c = next((c for c in self.contratos if f"cacar:{c['id']}" == op), None)
            if c:
                self.cacar(c)
        elif isinstance(op, tuple) and op[0] == "missao":
            missoes.executar(self, op[1], op[2])
        elif isinstance(op, tuple) and op[0] == "capela":
            missoes.ir_na_capela(self, op[1])
        elif op == "explorar":
            self.explorar()
        elif op == "acampar":
            missoes.sair_para_acampar(self)
            self.acampar()
        else:
            self.executar_comum(op)

    def menu_vila(self):
        j = self.j
        preco_dormir = abertura.preco_dormir(self)
        broquel = missoes.broquel_no_ferreiro(self)
        # Cada serviço diz a que prédio da vila pertence (na tela gráfica, a vila é um lugar com prédios clicáveis).
        # Os que se escolhem diante do prédio (a taverna, o templo) levam o rótulo curto, o preço, o que dão e o tempo
        # que gastam: a tela os desenha em cartões. Os outros abrem a tela do serviço direto.
        opcoes = [
            ("Passear pela vila", "passear", {"tempo": "1 período"}),
            (f"Taverna: dormir até amanhã ({preco_dormir} ouro)", "dormir",
             # O cartão mostra o custo, o que volta e as provisões em linhas curtas (os números da conta de descansar).
             {"predio": "taverna", "servico": "dormir", "curto": "Dormir até o amanhecer", "preco": preco_dormir,
              "linhas": [{"icone": "moeda", "rotulo": "Custo", "texto": f"{preco_dormir} ouro"},
                         *self.linhas_descanso("taverna")], **self.motivo_pagar(preco_dormir)}),
            (f"Taverna: pagar uma bebida e ouvir rumores ({self.preco(3)} ouro)", "rumores",
             {"predio": "taverna", "servico": "rumores", "curto": "Uma bebida e os rumores", "preco": self.preco(3),
              "efeito": "O que se conta nas mesas", **self.motivo_rumores()}) if not abertura.caneca(self) else
            ("Taverna: uma bebida e os rumores (por conta da casa)", "rumores",
             {"predio": "taverna", "servico": "rumores", "curto": "Uma bebida e os rumores", "preco": 0,
              "efeito": "A primeira caneca é por conta da casa", **self.motivo_rumores()}),
            ("Mercado", "loja", {"predio": "mercado"}),
            ("Mural de contratos", "mural", {"predio": "mural"}),
            *self.opcoes_templo(),
            ("Curandeira: tratar ferimentos e infecções", "curandeiro", {"predio": "curandeiro"}) if j.ferimentos else None,
            # A oferta única do broquel (saves de antes da E7) divide o balcão da forja com o reforço: dois cartões.
            ("Ferreiro: reforçar arma ou armadura", "ferreiro",
             {"predio": "ferreiro", **({"curto": "Reforçar arma ou armadura", "efeito": "Arma, peito e apoio, até +5"}
                                       if broquel else {})}),
            ("Ferreiro: o broquel que trouxeram da capela", "broquel",
             {"predio": "ferreiro", "servico": "broquel", "curto": "O broquel que trouxeram da capela",
              "efeito": "Do ossuário da Capela Afogada. Sem custo"}) if broquel else None,
            *missoes.opcoes(self),  # o passo da missão que se dá aqui (campanha), como "Examinar a fonte nova"
            *abertura.opcoes(self),  # a despensa adiada e o homem do canto (campanha nova)
            *self.opcoes_versao(),  # a troca de versão de uma habilidade transformada (o botão do Grimório)
            *self.opcoes_kit(),  # montar o kit (etapa 4): os botões do Grimório, ou uma linha no texto
        ]
        # A frase da vila aparece na chegada e quando o tempo passa, não a cada volta ao menu (do mercado, do
        # inventário). O sorteio segue a cada volta: com a mesma semente, a partida continua a mesma.
        ambiente = consequencias.ambiente(self, self.sortear(AMBIENTE_VILA))  # o Vau da campanha (o sorteio segue igual)
        if self.ambiente_visto != (self.loc["id"], self.dia, self.periodo):
            self.ambiente_visto = (self.loc["id"], self.dia, self.periodo)
            self.dizer(ambiente, "cinza")
            abertura.dica_texto(self, "vila")  # na interface de texto, a orientação do Mural numa linha
        antes = abertura.proxima(self)  # a orientação da vez quando o menu abriu (cumpre-se pela resposta)
        op = self.menu(f"Você está em {self.loc['nome']}. O que faz?", opcoes + self.opcoes_comuns())
        abertura.depois_do_menu(self, antes, op)
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
        elif op == "broquel":
            missoes.broquel_do_ferreiro(self)
            self.pausar()
        elif isinstance(op, tuple) and op[0] == "templo":
            self.balcao_templo(op[1:])
        elif isinstance(op, tuple) and op[0] == "missao":
            missoes.executar(self, op[1], op[2])
        elif isinstance(op, tuple) and op[0] == "abertura":
            abertura.executar(self, op[1])
        else:
            self.executar_comum(op)

    # ================================================================ ações no mundo
    def explorar(self):
        # Dentro da capela, explorar não existe (a opção nem aparece): um pedido atrasado ou de atalho não faz nada,
        # sem gastar tempo, tocha nem sorteio.
        if not missoes.pode_explorar(self):
            return False
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
