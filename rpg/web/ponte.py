"""WebUI: a mesma interface UI do jogo, mas cada chamada vira uma mensagem JSON para o navegador.

O jogo roda numa thread própria e chama ui.dizer()/ui.escolher() como sempre.
As mensagens vão para um Canal (lido pelo servidor HTTP via SSE); as respostas
do jogador voltam por uma fila. A lógica de "cenas" (página nova, Continuar)
é a mesma da interface Textual.
"""

import json
import queue
import re
import threading

from ..ui import InterfaceGrafica, UI
from .estado import estado

TESTE = re.compile(r"\((Força|Destreza|Arcano|Percepção|Vontade|Carisma) ([+-]\d+) no d20\)")


class Canal:
    """Registro de mensagens com cursor. Quem conecta depois recebe a cena atual de novo."""

    def __init__(self):
        self.mensagens = []
        self.inicio_cena = 0
        self.cond = threading.Condition()
        self.encerrado = False

    def publicar(self, msg):
        with self.cond:
            msg["seq"] = len(self.mensagens)
            if msg["t"] == "nova_cena":
                self.inicio_cena = msg["seq"]
            self.mensagens.append(msg)
            self.cond.notify_all()

    def encerrar(self):
        with self.cond:
            self.encerrado = True
            self.cond.notify_all()

    def ponto_de_entrada(self):
        """Onde um navegador recém-conectado começa: a cena atual, e o último estado antes dela."""
        with self.cond:
            ultimo_estado = None
            for m in reversed(self.mensagens[:self.inicio_cena]):
                if m["t"] == "estado":
                    ultimo_estado = m
                    break
            return self.inicio_cena, ultimo_estado

    def esperar(self, cursor, timeout=15):
        with self.cond:
            if cursor >= len(self.mensagens) and not self.encerrado:
                self.cond.wait(timeout)
            return self.mensagens[cursor:], self.encerrado


class WebUI(InterfaceGrafica, UI):
    hud = True

    def __init__(self, canal=None):
        super().__init__(cor=False, rapido=True)
        self.canal = canal or Canal()
        self.respostas = queue.Queue()
        self.jogo = None
        self.pergunta_id = 0
        self.escolhas_na_cena = 0
        self.novo_desde_escolha = False
        # Um "pausar" do motor só vira Continuar se depois vier mais história, uma luta ou outra cena. Se o que vem é
        # o menu do lugar (o fim de um evento), não: a tela dá o tempo de ler e vira a página para o lugar.
        self.pausa_pendente = False
        self.tipo_cena = None
        self.ultimo_estado = None
        self.ultimo_titulo = None
        self._segurando = None  # durante uma salva de golpes: o que chegar espera a animação

    # Salva de golpes (área): tudo o que o jogo mandar enquanto ela acontece (estado, falas, avisos) só sai
    # depois do lance "salva"; senão a tela mostraria o resultado antes da animação começar.
    def iniciar_salva(self):
        if self._segurando is None:
            self._segurando = []

    def fim_salva(self):
        guardadas, self._segurando = self._segurando or [], None
        for m in guardadas:
            if m["t"] == "estado":
                continue  # o estado é recalculado no fim, de uma vez
            self._enviar(**m)
        self.enviar_estado()

    # ------------------------------------------------------------ saída
    def _enviar(self, t, **dados):
        if self._segurando is not None and not (t == "lance" and dados.get("tipo") == "salva"):
            self._segurando.append({"t": t, **dados})
            return
        if self.pausa_pendente and t in ("texto", "efeito", "rolagem", "bloco", "mapa", "subtitulo", "separador"):
            self.pausa_pendente = False
            self._continuar()
        self.canal.publicar({"t": t, **dados})
        if t in ("texto", "efeito", "rolagem", "bloco", "mapa", "painel", "celebrar"):
            self.novo_desde_escolha = True

    def enviar_estado(self):
        e = estado(self.jogo) if self.jogo else None
        if e is None:
            return
        chave = json.dumps(e, sort_keys=True, ensure_ascii=False)
        if self._segurando is not None:
            return  # a salva ainda não foi animada
        if chave != self.ultimo_estado:
            self.ultimo_estado = chave
            self._enviar("estado", estado=e)

    def _imprimir(self, linha):
        self._enviar("texto", texto=str(linha), cor=None, mono=True)

    def dizer(self, texto="", cor=None):
        texto = str(texto)
        if texto.strip():
            self._enviar("texto", texto=texto, cor=cor)
            self.enviar_estado()

    def narrar(self, texto, cor=None):
        self.dizer(texto, cor)

    def titulo(self, texto, cor="amarelo+negrito"):
        self._enviar("subtitulo", texto=texto)

    def separador(self, cor="cinza"):
        self._enviar("separador")

    def desenhar(self, linhas):
        self._enviar("bloco", linhas=[[[t, c] for t, c in linha] for linha in linhas])

    def mostrar_mapa(self, grande=False):
        self.enviar_estado()
        self._enviar("mapa", grande=grande)

    def efeito(self, texto, tipo="info", item=None):
        if item:
            self._enviar("efeito", texto=texto, tipo=tipo, item=item)
        else:
            self._enviar("efeito", texto=texto, tipo=tipo)
        self.enviar_estado()  # a HUD reage junto com a etiqueta

    def atualizar(self):
        self.enviar_estado()

    def missao_atualizada(self, cartoes):
        """O cartão de novidade da missão vai inteiro, dentro do texto (o Diário e o rastreador também se atualizam)."""
        self._enviar("missao", cartoes=cartoes)
        self.enviar_estado()

    def lance(self, tipo, **dados):
        self._enviar("lance", tipo=tipo, **dados)

    def detalhe(self, texto, cor=None):
        texto = str(texto)
        if texto.strip():
            self._enviar("texto", texto=texto, cor=cor, detalhe=True)
            self.enviar_estado()

    def fala(self, cid, nome, texto):
        self._enviar("fala", cid=cid, nome=nome, texto=texto)
        self.novo_desde_escolha = True

    def opiniao(self, cid, nome, delta):
        self._enviar("opiniao", cid=cid, nome=nome, delta=delta)
        self.enviar_estado()

    def fim_combate(self, resultado):
        self._enviar("fim_combate", resultado=resultado)

    def celebrar(self, tipo, dados):
        self.enviar_estado()
        self._enviar("celebrar", tipo=tipo, dados=dados)

    def painel(self, tipo, dados):
        self.enviar_estado()
        self._enviar("painel", tipo=tipo, dados=dados)
        return True

    def arvore_talentos(self, dados):
        self._enviar("talentos", arvore=dados)

    def rolagem(self, atributo, cd, d20, mod, total, sucesso):
        self._enviar("rolagem", atributo=atributo, cd=cd, d20=d20, mod=mod, total=total, sucesso=sucesso)

    def cena(self, titulo, subtitulo=None, tipo="evento"):
        if tipo == "titulo":
            # A tela de título apaga o herói da tela (o estado de lá vira nulo). A ponte esquece junto: carregar em
            # seguida o mesmo save (salvar, sair, carregar) dá o mesmo estado, que tem de ir de novo; antes, a
            # comparação o descartava e a tela ficava sem painéis, doca e mapa até a primeira ação mudar algo.
            self.ultimo_estado = None
        # O menu do lugar logo depois da chegada a ele é a mesma página: o que se leu ao chegar fica junto das opções.
        mesmo_lugar = tipo == "local" and self.tipo_cena == "local" and titulo == self.ultimo_titulo
        # A cena nova abre página nova quando houve escolha nesta, ou quando ela terminou com uma pausa (o evento da
        # noite, o "Exausto": ninguém escolheu nada, mas o texto pede leitura antes de seguir).
        pagina_nova = tipo != "combate" and (self.escolhas_na_cena > 0 or (self.pausa_pendente and not mesmo_lugar))
        # Telas de menu que se redesenham (inventário, mercado) não param para "Continuar".
        mesma_tela = tipo == "menu" and titulo == self.ultimo_titulo
        ler_antes = pagina_nova and (self.novo_desde_escolha or self.pausa_pendente) and not mesma_tela
        # O fim de um evento (ou de uma luta) que cai direto no lugar não pede Continuar: a tela deixa o texto o tempo
        # de ler e vira a página sozinha. O estado do lugar (a arte, o painel, o mapa) vai junto com a página nova:
        # mandado antes, a cidade aparecia enquanto ainda se lia o que aconteceu na estrada.
        virar = ler_antes and tipo == "local"
        if not virar:
            self.enviar_estado()
        if tipo != "combate":
            self.tipo_cena = tipo
        if tipo == "combate":
            if self.pausa_pendente:
                self.pausa_pendente = False
                self._continuar()
            self._enviar("combate", titulo=titulo, subtitulo=subtitulo)
            return
        if pagina_nova:
            if ler_antes:
                self.pausa_pendente = False
                if virar:
                    self._enviar("nova_cena", titulo=titulo, subtitulo=subtitulo, tipo=tipo, virar=True)
                    self.ultimo_titulo = titulo
                    self.escolhas_na_cena = 0
                    self.novo_desde_escolha = False
                    self.enviar_estado()
                    return
                self._continuar()
            self._enviar("nova_cena", titulo=titulo, subtitulo=subtitulo, tipo=tipo)
            self.ultimo_titulo = titulo
            self.escolhas_na_cena = 0
            self.novo_desde_escolha = False
        else:
            # A cena anterior era só uma introdução, sem nada a ler antes de seguir (ou é o mesmo lugar): o novo título
            # a substitui na mesma página.
            self.pausa_pendente = False
            self._enviar("cabecalho", titulo=titulo, subtitulo=subtitulo, tipo=tipo)
            self.ultimo_titulo = titulo

    def novo_turno(self, n):
        self.enviar_estado()
        self._enviar("turno", n=n)

    def fim(self, texto=""):
        self._enviar("fim", texto=texto)
        self.canal.encerrar()

    # ------------------------------------------------------------ entrada
    def _perguntar(self, t, **dados):
        self.pausa_pendente = False  # a pergunta aparece embaixo do texto: ela mesma é a pausa
        self.enviar_estado()
        self.pergunta_id += 1
        pid = self.pergunta_id
        self._enviar(t, id=pid, **dados)
        while True:
            pid_resp, valor = self.respostas.get()
            if pid_resp is None:
                raise SystemExit(0)
            if pid_resp == pid:
                return valor

    def responder(self, pid, valor):
        """Chamado pelo servidor quando o navegador responde."""
        self.respostas.put((pid, valor))

    def escolher(self, pergunta, opcoes):
        pergunta = pergunta or ""
        # Perguntas longas são parte da história e vão para a página. A da confirmação (viagem perigosa, abandonar um
        # contrato) não: ela mora na janela, em cima dos botões.
        confirmacao = bool(self.meta_opcoes) and all(m and m.get("confirmar") for m in self.meta_opcoes)
        if len(pergunta) > 60 and not confirmacao:
            self.dizer(pergunta, "ciano")
            pergunta = ""
        itens = []
        metas = self.meta_opcoes or [None] * len(opcoes)
        for texto, meta in zip(opcoes, metas):
            m = TESTE.search(texto)
            item = {"texto": TESTE.sub("", texto).strip() if m else texto}
            if m:
                item["teste"] = {"atributo": m.group(1), "mod": int(m.group(2))}
            if meta:
                item["meta"] = meta
            itens.append(item)
        while True:
            i = self._perguntar("opcoes", pergunta=pergunta, opcoes=itens)
            self.extra_resposta = None
            if isinstance(i, dict):  # {"i": 3, "qtd": 5}: a escolha e o que veio junto
                self.extra_resposta = i
                i = i.get("i")
            if isinstance(i, int) and not isinstance(i, bool) and 0 <= i < len(opcoes):
                break
        meta, texto = itens[i].get("meta") or {}, itens[i]["texto"]
        # Voltar (a palavra sozinha: "Voltar por onde veio" é história) e escolher talento na árvore são navegação, não
        # decisões da história; o que se escolhe numa janela (o item achado, uma confirmação) a própria janela mostra.
        # Nenhum deles vira eco na página nem entra no histórico.
        navegacao = (texto == "Voltar" or meta.get("voltar") or meta.get("talento") or meta.get("achado")
                     or meta.get("confirmar") or meta.get("sistema"))  # abrir uma tela da doca também
        self._enviar("escolhido", texto=texto, navegacao=bool(navegacao))
        self.escolhas_na_cena += 1
        self.novo_desde_escolha = False
        return i

    def _continuar(self, confirmar=False):
        self._perguntar("continuar", **({"confirmar": True} if confirmar else {}))
        self.novo_desde_escolha = False
        self.escolhas_na_cena += 1  # quem tocou em Continuar já leu: a próxima cena abre página nova

    def perguntar(self, pergunta, padrao="", voltar=False):
        resposta = self._perguntar("pergunta", pergunta=pergunta, padrao=padrao, voltar=voltar)
        if voltar and isinstance(resposta, dict) and resposta.get("voltar"):
            self.escolhas_na_cena += 1
            self.novo_desde_escolha = False
            return None
        resposta = (str(resposta).strip() if resposta is not None else "") or padrao
        self._enviar("escolhido", texto=resposta)
        self.escolhas_na_cena += 1
        self.novo_desde_escolha = False
        return resposta

    def continuar(self, confirmar=False):
        self.pausa_pendente = False
        # O botão aparece já; tocado, a próxima cena abre página nova. Com `confirmar` (cena de missão), a tela só o
        # aceita depois de uma guarda curta: o clique ou a tecla que adiantou o texto não fecha a cena junto.
        self._continuar(confirmar)

    def pausar(self):
        if self.novo_desde_escolha:
            if self.tipo_cena == "menu":
                self._continuar()  # numa tela de menu (bestiário, diário) a pausa é a tela aberta, esperando o Voltar
            else:
                self.pausa_pendente = True
