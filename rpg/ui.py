"""Interface de terminal: cores, menus, barras e um "jogador robô" para testes."""

import os
import sys
import textwrap
import time

LARGURA = 76

CORES = {
    "reset": "\033[0m",
    "negrito": "\033[1m",
    "fraco": "\033[2m",
    "italico": "\033[3m",
    "vermelho": "\033[31m",
    "verde": "\033[32m",
    "amarelo": "\033[33m",
    "azul": "\033[34m",
    "magenta": "\033[35m",
    "ciano": "\033[36m",
    "branco": "\033[37m",
    "cinza": "\033[90m",
}


def _suporta_cor():
    if os.environ.get("NO_COLOR"):
        return False
    if not sys.stdout.isatty():
        return False
    if os.name == "nt":
        os.system("")  # habilita sequências ANSI no Windows 10+
    return True


COR_EFEITO = {
    "ouro": "amarelo", "perda": "vermelho", "xp": "ciano", "dano": "vermelho", "cura": "verde",
    "item": "verde", "rep": "magenta", "teste_ok": "verde+negrito", "teste_falha": "vermelho+negrito",
    "ferimento": "vermelho+negrito", "info": "cinza", "nivel": "amarelo+negrito", "aprova": "verde",
    "desaprova": "magenta",
}


class LimiteBot(Exception):
    """O jogador robô atingiu o número máximo de decisões."""


class UI:
    interativo = True
    extra_resposta = None  # dados extras que a interface mandou junto da escolha (ex.: quantidade)
    meta_opcoes = None  # dados extras de cada opção (local de viagem, talento...), para interfaces gráficas
    notas_proprias = False  # a interface mostra a `nota` de uma opção à parte (senão o jogo a junta ao rótulo)

    # O que a interface sabe fazer. O motor pergunta por isto, nunca "que tela é esta?".
    hud = False               # há um painel fixo com vida, recursos e inimigos: o texto não repete
    letras_nos_alvos = True   # "Lobo A", "Lobo B": no texto, a letra é o que diferencia os alvos no menu
    analisar_no_menu = True   # "Analisar inimigos" como ação (sem ficha ao passar o mouse na carta)
    numerar_destinos = True   # "[3] ▲ Floresta": o número e o glifo ligam a opção ao mapa em caracteres
    fogueira_sozinho = False  # a cena da fogueira aparece mesmo sem ninguém da comitiva
    bolsa_clicavel = False    # os consumíveis do painel viram opções escondidas no menu do lugar
    conversa_no_painel = False  # o ✉ da comitiva no painel abre a conversa direto (opção escondida no menu do lugar)
    conquistas_na_tela = False  # nível, Sigilo, contrato cumprido, espólio, amanhecer, atributo para sempre e a
                                # chegada num lugar viram um momento na tela (celebrar): o texto não repete o que
                                # ela mostra
    surpresa_na_tela = False  # a surpresa do começo da luta (a sua iniciativa ou a deles) é animada nas cartas
                              # (o lance "surpresa"): o texto não a anuncia

    def __init__(self, cor=None, rapido=False):
        self.cor = _suporta_cor() if cor is None else cor
        self.rapido = rapido

    # ------------------------------------------------------------ saída
    def pintar(self, texto, cor):
        if not self.cor or not cor:
            return texto
        prefixo = "".join(CORES[c] for c in cor.split("+"))
        return f"{prefixo}{texto}{CORES['reset']}"

    def _imprimir(self, linha):
        print(linha)

    def dizer(self, texto="", cor=None):
        if not texto:
            self._imprimir("")
            return
        for paragrafo in str(texto).split("\n"):
            recuo = " " * (len(paragrafo) - len(paragrafo.lstrip()))
            linhas = textwrap.wrap(paragrafo, LARGURA, subsequent_indent=recuo) or [""]
            for linha in linhas:
                self._imprimir(self.pintar(linha, cor))

    def narrar(self, texto, cor=None):
        """Como dizer(), mas com uma pequena pausa dramática."""
        self.dizer(texto, cor)
        if not self.rapido:
            time.sleep(0.25)

    def titulo(self, texto, cor="amarelo+negrito"):
        self._imprimir("")
        self._imprimir(self.pintar("═" * LARGURA, cor))
        self._imprimir(self.pintar(texto.center(LARGURA), cor))
        self._imprimir(self.pintar("═" * LARGURA, cor))

    def separador(self, cor="cinza"):
        self._imprimir(self.pintar("─" * LARGURA, cor))

    def barra(self, atual, maximo, largura=16, cor="verde"):
        cheio = round(largura * max(0, atual) / maximo) if maximo else 0
        cheio = min(largura, cheio)
        return self.pintar("█" * cheio, cor) + self.pintar("░" * (largura - cheio), "cinza")

    # ------------------------------------------------------------ estrutura narrativa
    def cena(self, titulo, subtitulo=None, tipo="evento"):
        """Começa uma nova cena (um "momento" da história)."""
        cor = {"combate": "vermelho+negrito", "chefe": "vermelho+negrito", "morte": "vermelho+negrito",
               "local": "amarelo+negrito", "titulo": "amarelo+negrito", "vitoria": "amarelo+negrito"}.get(tipo, "ciano+negrito")
        self._imprimir("")
        self._imprimir(self.pintar(f"◆ {titulo.upper()}", cor))
        if subtitulo:
            self._imprimir(self.pintar(f"  {subtitulo}", "cinza"))
        self._imprimir("")

    def efeito(self, texto, tipo="info", item=None):
        """Consequência mecânica (ouro, vida, testes...), separada da prosa. item: o id do que se ganhou (poção,
        comida, flechas...), para a tela gráfica mandar o ícone até onde ele mora."""
        self._imprimir("   " + self.pintar(f"▸ {texto}", COR_EFEITO.get(tipo)))

    def missao_atualizada(self, cartoes):
        """O que uma ação ou cena mudou nas missões, junto, no fim do texto: o que se descobriu ou fez e o objetivo
        novo. Cada cartão: missao, nome, itens, objetivo (ou None), nova, concluida (missoes.anotar_novidades)."""
        for c in cartoes:
            estado = " (missão nova)" if c["nova"] else " (concluída)" if c["concluida"] else ""
            self.dizer(f"◆ Diário: {c['nome']}{estado}", "ciano")
            for item in c["itens"]:
                self.dizer(f"   + {item}", "ciano")
            if c["objetivo"]:
                self.dizer(f"   Objetivo: {c['objetivo']}", "ciano")

    def rolagem(self, atributo, cd, d20, mod, total, sucesso):
        """Resultado de um teste de atributo (a interface web anima o dado)."""
        extra = " · crítico!" if d20 == 20 else " · desastre!" if d20 == 1 else ""
        self.efeito(f"{atributo} {total} contra {cd} — {'SUCESSO' if sucesso else 'FALHA'} (d20 {d20} {mod:+d}){extra}",
                    "teste_ok" if sucesso else "teste_falha")

    def novo_turno(self, n):
        self._imprimir(self.pintar(f"── turno {n} ──", "cinza"))

    def atualizar(self):
        """O estado mudou (um golpe, uma cura): interfaces com painel podem redesenhar."""

    def fim_combate(self, resultado):
        """O combate acabou: interfaces gráficas podem mostrar o último golpe antes do resultado."""

    def lance(self, tipo, **dados):
        """Um lance de combate (ação, golpe, cura...) com quem e em quem, para interfaces que animam as cartas.
        O texto do lance já foi (ou será) dito; as interfaces de texto não precisam de nada aqui."""

    def iniciar_salva(self):
        """Golpes em área vão começar: interfaces gráficas seguram o que chegar até a salva ser animada."""

    def fim_salva(self):
        """A salva foi enviada: o que ficou guardado pode sair."""

    def detalhe(self, texto, cor=None):
        """Linha mecânica de combate (dano, esquiva, efeito aplicado). Interfaces gráficas a mostram miúda,
        porque a animação já conta o que aconteceu."""
        self.dizer(texto, cor)

    def fala(self, cid, nome, texto):
        """Um companheiro fala. Interfaces gráficas mostram um balão saindo do retrato."""
        self.dizer(texto, "cinza")

    def opiniao(self, cid, nome, delta):
        """Um companheiro aprova ou desaprova algo."""
        intensidade = " muito" if abs(delta) >= 8 else ""
        verbo = "aprova" if delta > 0 else "desaprova"
        self.efeito(f"{nome} {verbo}{intensidade}", "aprova" if delta > 0 else "desaprova")

    def celebrar(self, tipo, dados):
        """Momentos de conquista (nível, Sigilo, especialização...): interfaces gráficas fazem festa."""

    def painel(self, tipo, dados):
        """Telas como Diário e Bestiário: interfaces gráficas desenham os dados; as de texto ignoram."""
        return False

    def arvore_talentos(self, dados):
        """Interfaces gráficas desenham a árvore; as de texto usam o desenho em caracteres."""

    # ------------------------------------------------------------ jeitos de mostrar
    # O motor entrega o conteúdo; cada interface decide como aparece. Aqui, o jeito do texto.
    def desenhar_mapa(self, grande, linhas):
        """O mapa do mundo. `linhas()` desenha em caracteres. Devolve True se a interface tem mapa próprio."""
        self.desenhar(linhas())
        return False

    def mostrar_talentos(self, dados, linhas, subtitulo):
        """A árvore de talentos. `dados()` para quem desenha a árvore; `linhas()` para o desenho em caracteres."""
        self.cena("Talentos", subtitulo, "menu")
        self.desenhar(linhas())
        self.dizer("verde = aprendido · amarelo = disponível · cinza = bloqueado", "cinza")

    def talento_aprendido(self, nome, rank, maximo):
        self.dizer(f"Você aprendeu {nome} ({rank}/{maximo}).", "verde+negrito")

    def reacao_animal(self, dados, texto, cor):
        """O animal reage a um carinho. `texto` é a frase pronta para quem não desenha balão."""
        self.celebrar("carinho", dados)
        self.dizer(texto, cor)

    def boas_vindas(self, nome):
        """Ao carregar um save."""
        self.dizer(f"Bem-vindo de volta, {nome}.", "verde")

    def desenhar(self, linhas):
        """Desenha um bloco de linhas, cada uma uma lista de pedaços (texto, cor)."""
        for linha in linhas:
            self._imprimir("".join(self.pintar(t, c) for t, c in linha).rstrip())

    # ------------------------------------------------------------ entrada
    def escolher(self, pergunta, opcoes):
        """Mostra opções numeradas e devolve o índice escolhido."""
        if pergunta:
            self.dizer(pergunta, "ciano")
        for i, opcao in enumerate(opcoes, 1):
            self._imprimir(f"  {self.pintar(str(i) + ')', 'amarelo')} {opcao}")
        while True:
            try:
                resposta = input(self.pintar("> ", "amarelo")).strip()
            except EOFError:
                raise SystemExit(0)
            if resposta.isdigit() and 1 <= int(resposta) <= len(opcoes):
                return int(resposta) - 1
            self.dizer("Digite o número de uma das opções.", "cinza")

    def perguntar(self, pergunta, padrao="", voltar=False):
        """Texto livre. Com voltar=True, a interface pode devolver None (a pessoa desistiu); aqui nunca."""
        try:
            resposta = input(self.pintar(f"{pergunta} ", "ciano")).strip()
        except EOFError:
            raise SystemExit(0)
        return resposta or padrao

    def pausar(self):
        try:
            input(self.pintar("  [Enter para continuar]", "cinza"))
        except EOFError:
            raise SystemExit(0)

    def continuar(self, confirmar=False):
        """Um Continuar de verdade, mesmo onde a pausa da tela gráfica viraria a página sozinha: o fim do prólogo,
        que quem começa precisa ler no seu tempo antes de a vila aparecer. `confirmar`: a cena pede confirmação
        explícita (as cenas de missão); na tela gráfica, o clique ou a tecla que adiantou o texto não a fecha."""
        self.pausar()


class InterfaceGrafica:
    """O jeito de uma interface gráfica (a tela web, e o robô do gabarito quando a imita): cartas clicáveis
    em vez de letras, mapa e árvore desenhados por ela, reações em balões. Vai antes de UI na herança."""
    notas_proprias = True

    letras_nos_alvos = False   # cada inimigo é uma carta; o alvo se escolhe clicando
    analisar_no_menu = False   # a ficha do inimigo aparece ao passar o mouse na carta
    numerar_destinos = False   # o mapa é clicável e desenha os próprios ícones
    fogueira_sozinho = True    # a fogueira desenhada é o momento de respirar do dia, mesmo sozinho
    bolsa_clicavel = True
    conversa_no_painel = True
    conquistas_na_tela = True
    surpresa_na_tela = True

    def desenhar_mapa(self, grande, linhas):
        self.mostrar_mapa(grande)
        return True

    def mostrar_talentos(self, dados, linhas, subtitulo):
        # a árvore abre por cima, como o Grimório: a página do lugar fica como estava
        self.arvore_talentos(dados())

    def talento_aprendido(self, nome, rank, maximo):
        pass  # o próprio talento festeja na árvore (som, faíscas, aviso)

    def reacao_animal(self, dados, texto, cor):
        self.celebrar("carinho", dados)  # vira um balão sobre o animal, não um aviso solto

    def boas_vindas(self, nome):
        pass  # o próprio lugar aparece


class BotUI(UI):
    """Joga sozinho escolhendo opções ao acaso. Usado pelos testes de simulação."""

    interativo = False

    def __init__(self, rng, max_decisoes=500, verboso=False):
        super().__init__(cor=False, rapido=True)
        self.rng = rng
        self.max_decisoes = max_decisoes
        self.decisoes = 0
        self.verboso = verboso

    def _imprimir(self, linha):
        if self.verboso:
            print(linha)

    def escolher(self, pergunta, opcoes):
        self.decisoes += 1
        if self.decisoes > self.max_decisoes:
            raise LimiteBot()
        if pergunta:
            self.dizer(pergunta)
        # O robô evita sair do jogo para explorar mais conteúdo.
        validas = [i for i, o in enumerate(opcoes) if not o.startswith("Sair")]
        escolha = self.rng.choice(validas or list(range(len(opcoes))))
        if self.verboso:
            print(f"  [robô] -> {opcoes[escolha]}")
        return escolha

    def perguntar(self, pergunta, padrao="", voltar=False):
        return padrao or "Robô"

    def pausar(self):
        pass
