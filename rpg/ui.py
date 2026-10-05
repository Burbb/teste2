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


class LimiteBot(Exception):
    """O jogador robô atingiu o número máximo de decisões."""


class UI:
    interativo = True

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

    def perguntar(self, pergunta, padrao=""):
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

    def perguntar(self, pergunta, padrao=""):
        return padrao or "Robô"

    def pausar(self):
        pass
