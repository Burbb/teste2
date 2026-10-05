"""Interface moderna com Textual.

O jogo continua escrito como um programa "de terminal" que chama
ui.dizer()/ui.escolher(). Aqui ele roda numa thread separada; cada chamada é
repassada para o app Textual, que mostra um log rolável, opções clicáveis
(ou teclas 1-9) e um painel lateral fixo com status, combate e mapa.
"""

import queue

from rich.markup import MarkupError, escape
from rich.rule import Rule
from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Input, OptionList, RichLog, Static
from textual.widgets.option_list import Option

from . import mapa
from .combate import NOMES_EFEITOS
from .dados import CLIMAS, PERIODOS
from .ui import UI

TECLAS = "1234567890abcdefghijklmnopqrstuvwxyz"
ESTILOS = {
    "vermelho": "red", "verde": "green", "amarelo": "yellow", "azul": "bright_blue", "magenta": "magenta",
    "ciano": "cyan", "branco": "white", "cinza": "grey58", "negrito": "bold", "italico": "italic", "fraco": "dim",
}


def estilo(cor):
    return " ".join(ESTILOS[c] for c in cor.split("+")) if cor else ""


def texto_de(linhas):
    """Converte linhas de pedaços (texto, cor) em um Text do Rich."""
    t = Text()
    for i, linha in enumerate(linhas):
        if i:
            t.append("\n")
        for pedaco, cor in linha:
            t.append(pedaco, style=estilo(cor))
    return t


def _barra(t, atual, maximo, largura, cor):
    cheio = min(largura, round(largura * max(0, atual) / maximo)) if maximo else 0
    t.append("█" * cheio, style=cor)
    t.append("░" * (largura - cheio), style="grey30")


def painel_status(g):
    j = g.j
    t = Text()
    t.append(f"{j.nome}", style="bold")
    t.append(f" · {j.nome_classe} Nv.{j.nivel}\n", style="cyan")
    t.append(f"XP {j.xp}/{j.xp_proximo()}", style="grey58")
    if j.pontos_talento:
        t.append(f"   ★ {j.pontos_talento} talento(s)!", style="bold yellow")
    t.append("\nVida  ")
    _barra(t, j.hp, j.max_hp, 18, "green")
    t.append(f" {j.hp}/{j.max_hp}\n")
    t.append(f"{j.nome_recurso:<5} ")
    _barra(t, j.rec, j.max_rec, 18, "bright_blue")
    t.append(f" {j.rec}/{j.max_rec}\n")
    extra = f"   Flechas {j.flechas}" if j.classe == "arqueiro" else ""
    t.append(f"Ouro {j.ouro}{extra}   Reputação {j.reputacao:+d}\n", style="yellow")
    if j.companheiro:
        c = j.companheiro
        t.append(f"{c['nome'][:12]:<12} ")
        _barra(t, c["hp"], c["max_hp"], 12, "cyan")
        t.append(f" {c['hp']}/{c['max_hp']}\n")
    t.append(f"\nDia {g.dia} · {PERIODOS[min(g.periodo, 3)]} · {CLIMAS[g.clima]['nome']}\n")
    t.append("Corrupção ")
    _barra(t, g.corrupcao, 100, 18, "magenta")
    t.append(f" {g.corrupcao}%\n")
    t.append("Sigilos ")
    t.append("◆" * len(j.sigilos), style="bold yellow")
    t.append("◇" * (3 - len(j.sigilos)), style="grey50")
    loc = g.loc
    t.append(f"\n\n[{loc['id'] + 1}] {loc['nome']}\n", style="bold")
    desc = mapa.descricao(g, loc)
    if loc["tipo"] != "vila":
        desc += f" · inimigos Nv.{g.nivel_local()}"
    t.append(desc, style="grey58")

    cb = g.combate_ativo
    if cb:
        t.append("\n\n⚔ COMBATE", style="bold red")
        for a in cb.aliados:
            if a.vivo:
                t.append(f"\n{a.nome[:14]:<14} ", style="cyan")
                _barra(t, a.hp, a.max_hp, 10, "cyan")
                t.append(f" {a.hp}")
        for e in cb.inimigos_vivos():
            t.append(f"\n{e.nome[:14]:<14} ", style="red")
            _barra(t, e.hp, e.max_hp, 10, "red")
            t.append(f" {e.hp}")
            if e.carregando:
                t.append(" ⚠", style="bold yellow")
            if e.efeitos:
                t.append("\n  " + ", ".join(ef.get("r", NOMES_EFEITOS.get(n, n)) for n, ef in e.efeitos.items()),
                         style="magenta")
        if j.efeitos:
            t.append("\nVocê: " + ", ".join(ef.get("r", NOMES_EFEITOS.get(n, n)) for n, ef in j.efeitos.items()),
                     style="magenta")
    return t


def painel_mapa(g, largura, altura):
    t = texto_de(mapa.renderizar(g, largura, altura))
    t.append("\nCaminhos daqui:", style="grey58")
    for loc, dist in sorted(g.mundo_vizinhos(), key=lambda v: v[0]["id"]):
        nv = "" if loc["tipo"] == "vila" else f" Nv.{mapa.nivel_regiao(loc, g.corrupcao)}"
        t.append(f"\n{loc['id'] + 1:>2} {mapa.glifo(g, loc)} {loc['nome'][:26]}{nv} → {dist}",
                 style="bold" if loc["visitado"] else "grey58")
    return t


class TextualUI(UI):
    hud = True

    def __init__(self, app):
        super().__init__(cor=False, rapido=True)
        self.app = app
        self.respostas = queue.Queue()
        self.jogo = None

    # Saída ------------------------------------------------------------
    def _enviar(self, conteudo):
        self.app.call_from_thread(self.app.escrever, conteudo)

    def pintar(self, texto, cor):
        texto = escape(texto)
        return f"[{estilo(cor)}]{texto}[/]" if cor else texto

    def _imprimir(self, linha):
        try:
            self._enviar(Text.from_markup(linha))
        except MarkupError:
            self._enviar(Text(linha))

    def dizer(self, texto="", cor=None):
        self._enviar(Text(str(texto), style=estilo(cor)))

    def titulo(self, texto, cor="amarelo+negrito"):
        self._enviar(Rule(Text(texto, style=estilo(cor)), style=estilo(cor.split("+")[0])))

    def separador(self, cor="cinza"):
        self._enviar(Rule(style="grey30"))

    def desenhar(self, linhas):
        self._enviar(texto_de(linhas))

    # Entrada ----------------------------------------------------------
    def _esperar(self):
        resposta = self.respostas.get()
        if resposta is None:
            raise SystemExit(0)
        return resposta

    def atualizar_hud(self):
        g = self.jogo
        if g and g.j and g.mundo:
            self.app.call_from_thread(self.app.atualizar_hud, painel_status(g), painel_mapa(g, 46, 15))

    def escolher(self, pergunta, opcoes):
        if pergunta:
            self.dizer(pergunta, "ciano+negrito")
        self.atualizar_hud()
        self.app.call_from_thread(self.app.mostrar_opcoes, opcoes)
        i = self._esperar()
        self.dizer(f"  › {opcoes[i]}", "cinza")
        return i

    def perguntar(self, pergunta, padrao=""):
        self.app.call_from_thread(self.app.pedir_texto, pergunta, padrao)
        return self._esperar() or padrao

    def pausar(self):
        pass  # o log fica na tela; não é preciso pausar


class AppRPG(App):
    TITLE = "Crônicas da Fenda"
    SUB_TITLE = "um RPG de texto onde nenhuma jornada é igual"
    CSS = """
    #principal { width: 1fr; }
    #log { height: 1fr; border: round $primary; padding: 0 1; scrollbar-size-vertical: 1; }
    #opcoes { height: auto; max-height: 16; border: round $accent; }
    #entrada { display: none; border: round $accent; }
    #lateral { width: 52; }
    #status { height: auto; border: round $secondary; padding: 0 1; }
    #mapa { height: 1fr; border: round $secondary; padding: 0 1; }
    """
    BINDINGS = [
        Binding("ctrl+q", "quit", "Sair"),
        Binding("pageup", "rolar(-1)", "Rolar ↑", show=False),
        Binding("pagedown", "rolar(1)", "Rolar ↓", show=False),
    ]

    def __init__(self, args, menu_principal):
        super().__init__()
        self.args = args
        self.menu_principal = menu_principal
        self.ui = TextualUI(self)
        self.n_opcoes = 0

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="principal"):
                yield RichLog(id="log", wrap=True, markup=False, highlight=False, max_lines=4000)
                yield OptionList(id="opcoes")
                yield Input(id="entrada")
            with Vertical(id="lateral"):
                yield Static(Text("Bem-vindo, aventureiro.", style="grey58"), id="status")
                yield Static(id="mapa")
        yield Footer()

    def on_mount(self):
        self.query_one("#status").border_title = "Herói"
        self.query_one("#mapa").border_title = "Mapa"
        self.query_one("#opcoes").border_title = "O que fazer? (tecle o número/letra ou clique)"
        self.run_worker(self._executar_jogo, thread=True, exit_on_error=True)

    def _executar_jogo(self):
        try:
            self.menu_principal(self.ui, self.args)
        except SystemExit:
            pass
        self.call_from_thread(self.exit)

    # Chamados pela thread do jogo (via call_from_thread) --------------
    def escrever(self, conteudo):
        self.query_one("#log", RichLog).write(conteudo, expand=True)

    def mostrar_opcoes(self, opcoes):
        lista = self.query_one("#opcoes", OptionList)
        lista.clear_options()
        rotulos = []
        for i, o in enumerate(opcoes):
            tecla = TECLAS[i] if i < len(TECLAS) else " "
            rotulos.append(Option(Text.assemble((f"{tecla} ", "bold yellow"), o)))
        lista.add_options(rotulos)
        lista.highlighted = 0
        lista.display = True
        lista.focus()
        self.n_opcoes = len(opcoes)

    def pedir_texto(self, pergunta, padrao):
        self.escrever(Text(pergunta, style="cyan bold"))
        self.query_one("#opcoes", OptionList).display = False
        entrada = self.query_one("#entrada", Input)
        entrada.placeholder = padrao or "digite e aperte Enter"
        entrada.value = ""
        entrada.display = True
        entrada.focus()

    def atualizar_hud(self, status, mapa_texto):
        self.query_one("#status", Static).update(status)
        self.query_one("#mapa", Static).update(mapa_texto)

    # Eventos da interface ---------------------------------------------
    def _responder(self, indice):
        lista = self.query_one("#opcoes", OptionList)
        lista.clear_options()
        self.n_opcoes = 0
        self.ui.respostas.put(indice)

    def on_option_list_option_selected(self, evento: OptionList.OptionSelected):
        if self.n_opcoes:
            self._responder(evento.option_index)

    def on_input_submitted(self, evento: Input.Submitted):
        entrada = self.query_one("#entrada", Input)
        entrada.display = False
        self.query_one("#opcoes", OptionList).display = True
        self.ui.respostas.put(evento.value.strip())

    def on_key(self, evento):
        if self.n_opcoes and evento.character and evento.character in TECLAS:
            i = TECLAS.index(evento.character)
            if i < self.n_opcoes:
                evento.stop()
                self._responder(i)

    def action_rolar(self, direcao):
        log = self.query_one("#log", RichLog)
        log.scroll_page_up() if direcao < 0 else log.scroll_page_down()

    def action_quit(self):
        self.ui.respostas.put(None)
        self.exit()
