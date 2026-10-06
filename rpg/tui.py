"""Interface moderna com Textual.

O jogo continua escrito como um programa "de terminal" que chama
ui.dizer()/ui.escolher(). Aqui ele roda numa thread separada; cada chamada é
repassada para o app Textual, que mostra um log rolável, opções clicáveis
(ou teclas 1-9) e um painel lateral fixo com status, combate e mapa.
"""

import queue
from collections import deque

from rich.markup import MarkupError, escape
from rich.console import Group
from rich.rule import Rule
from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Footer, Header, Input, OptionList, RichLog, Static
from textual.widgets.option_list import Option

from . import comitiva, mapa, sobrevivencia
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


def _efeitos(c):
    return ", ".join(f"{ef.get('r', NOMES_EFEITOS.get(n, n))}({ef['t']})" for n, ef in c.efeitos.items())


def painel_vitais(g):
    """Faixa logo acima das opções: o que importa para a próxima decisão."""
    j = g.j
    t = Text()
    t.append("Vida ", style="bold")
    _barra(t, j.hp, j.max_hp, 16, "green" if j.hp > j.max_hp * 0.35 else "red")
    t.append(f" {j.hp}/{j.max_hp}   ")
    t.append(f"{j.nome_recurso} ", style="bold")
    _barra(t, j.rec, j.max_rec, 10, "bright_blue")
    t.append(f" {j.rec}/{j.max_rec}   ")
    if j.classe == "arqueiro":
        t.append(f"Flechas {j.flechas}   ", style="yellow")
    comida = "red bold" if j.provisoes <= 1 else "yellow"
    t.append(f"Comida {j.provisoes}d", style=comida)
    t.append(f"   Tochas {j.consumiveis.get('tocha', 0)}", style="red bold" if not j.tem("tocha") else "yellow")
    t.append(f"   Poções {j.consumiveis.get('pocao_vida', 0)}", style="yellow")
    males = sobrevivencia.descrever(j)
    if males:
        t.append("\n⚠ " + " · ".join(males), style="red bold")
    return t


def painel_combate(g):
    cb = g.combate_ativo
    if not cb:
        return None
    j = g.j
    t = Text()
    t.append(f"⚔ COMBATE — turno {cb.turno}\n", style="bold red")
    t.append(f"{'Você':<22}", style="bold")
    _barra(t, j.hp, j.max_hp, 16, "green")
    t.append(f" {j.hp}/{j.max_hp}")
    if j.efeitos:
        t.append(f"  {_efeitos(j)}", style="magenta")
    for a in cb.aliados:
        if a.vivo:
            t.append(f"\n{a.nome[:21]:<22}", style="cyan")
            _barra(t, a.hp, a.max_hp, 16, "cyan")
            t.append(f" {a.hp}/{a.max_hp}")
    for e in cb.inimigos_vivos():
        t.append(f"\n{e.nome[:21]:<22}", style="red")
        _barra(t, e.hp, e.max_hp, 16, "red")
        t.append(f" {e.hp}/{e.max_hp}")
        if e.carregando:
            t.append("  ⚠ PREPARANDO GOLPE", style="bold yellow")
        if e.efeitos:
            t.append(f"  {_efeitos(e)}", style="magenta")
    return t


def painel_status(g):
    j = g.j
    t = Text()
    t.append(f"{j.nome}", style="bold")
    t.append(f" · {j.nome_classe} Nv.{j.nivel}\n", style="cyan")
    t.append(f"XP {j.xp}/{j.xp_proximo()}", style="grey58")
    if j.pontos_talento:
        t.append(f"   ★ {j.pontos_talento} talento(s)!", style="bold yellow")
    t.append(f"\nOuro {j.ouro}   Reputação {j.reputacao:+d}\n", style="yellow")
    if j.companheiro:
        c = j.companheiro
        t.append(f"{c['nome'][:12]:<12} ")
        _barra(t, c["hp"], c["max_hp"], 12, "cyan")
        t.append(f" {c['hp']}/{c['max_hp']}\n")
    for m in comitiva.estado(g):
        t.append(f"{m['nome'].split()[-1][:12]:<12} ")
        _barra(t, m["hp"], m["max_hp"], 12, "cyan")
        t.append(f" {m['nivel']}" + (" · ferido" if m["ferido"] else "") + "\n",
                 style="green" if m["aprovacao"] >= 15 else "red" if m["aprovacao"] <= -15 else "grey58")
    t.append(f"\nDia {g.dia} · {PERIODOS[min(g.periodo, 3)]} · {CLIMAS[g.clima]['nome']}\n")
    t.append("Corrupção ")
    _barra(t, g.corrupcao, 100, 16, "magenta")
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
    return t


def painel_mapa(g, largura, altura):
    t = texto_de(mapa.renderizar(g, largura, altura))
    t.append("\nCaminhos daqui:", style="grey58")
    for loc, dist in sorted(g.mundo_vizinhos(), key=lambda v: v[0]["id"]):
        nv = "" if loc["tipo"] == "vila" else f" Nv.{mapa.nivel_regiao(loc, g.corrupcao)}"
        t.append(f"\n{loc['id'] + 1:>2} {mapa.glifo(g, loc)} {loc['nome'][:26]}{nv} → {dist}",
                 style="bold" if loc["visitado"] else "grey58")
    return t


CHIPS = {
    "ouro": "bold black on dark_goldenrod", "perda": "bold white on dark_red", "xp": "bold black on cyan",
    "dano": "bold white on red3", "cura": "bold black on green3", "item": "bold black on chartreuse3",
    "rep": "bold white on magenta", "teste_ok": "bold black on green3", "teste_falha": "bold white on red3",
    "ferimento": "bold white on dark_red", "info": "black on grey70", "nivel": "bold black on gold1",
    "aprova": "black on pale_green3", "desaprova": "white on medium_purple4",
}
# Paleta da prosa: texto neutro de livro; cores só para ênfase, mais suaves que as do terminal clássico.
PROSA = {
    None: "grey85", "amarelo": "grey93", "branco": "grey93", "cinza": "italic grey58", "vermelho": "indian_red1",
    "verde": "pale_green3", "magenta": "plum2", "ciano": "light_sky_blue1", "azul": "light_slate_blue",
}


def estilo_prosa(cor):
    if not cor:
        return PROSA[None]
    partes = cor.split("+")
    base = PROSA.get(partes[0], PROSA[None])
    extras = " ".join(ESTILOS[p] for p in partes[1:] if p in ESTILOS)
    return f"{base} {extras}".strip()


COR_CENA = {"combate": "red", "local": "gold1", "menu": "cyan", "evento": "bright_white", "chefe": "red",
            "morte": "red", "vitoria": "gold1", "titulo": "gold1"}
VELOCIDADES = {"instantaneo": 0, "rapido": 320, "normal": 140, "lento": 70}


def cabecalho_cena(titulo, subtitulo, tipo):
    cor = COR_CENA.get(tipo, "bright_white")
    t = Text()
    t.append("◆ ", style=cor)
    t.append(titulo.upper(), style=f"bold {cor}")
    if subtitulo:
        t.append("\n" + subtitulo, style="italic grey50")
    t.append("\n")
    return t


class TextualUI(UI):
    """Ponte entre a thread do jogo e o app. Organiza o texto em cenas (páginas)."""

    hud = True

    def __init__(self, app):
        super().__init__(cor=False, rapido=True)
        self.app = app
        self.respostas = queue.Queue()
        self.jogo = None
        self.escolhas_na_cena = 0
        self.novo_desde_escolha = False
        self.ultimo = None  # tipo do último bloco enviado: "prosa", "chip", "outro"

    # Saída ------------------------------------------------------------
    def _enviar(self, conteudo, revelar=False, chip=False, tipo="outro"):
        rapido = bool(self.jogo and self.jogo.combate_ativo)
        if not rapido and ((tipo == "prosa" and self.ultimo in ("prosa", "chip"))
                           or (tipo == "chip" and self.ultimo == "prosa")):
            self.app.call_from_thread(self.app.adicionar, Text(""), False, False, rapido)  # respiro entre blocos
        self.app.call_from_thread(self.app.adicionar, conteudo, revelar, chip, rapido)
        self.novo_desde_escolha = True
        self.ultimo = tipo

    def pintar(self, texto, cor):
        texto = escape(texto)
        return f"[{estilo(cor)}]{texto}[/]" if cor else texto

    def _imprimir(self, linha):
        try:
            self._enviar(Text.from_markup(linha))
        except MarkupError:
            self._enviar(Text(linha))

    def dizer(self, texto="", cor=None):
        self._enviar(Text(str(texto), style=estilo_prosa(cor)), revelar=True, tipo="prosa")

    def narrar(self, texto, cor=None):
        self.dizer(texto, cor)

    def titulo(self, texto, cor="amarelo+negrito"):
        self._enviar(Rule(Text(f" {texto} ", style=estilo(cor)), style=estilo(cor.split("+")[0])))

    def separador(self, cor="cinza"):
        self._enviar(Text(""))

    def desenhar(self, linhas):
        self._enviar(texto_de(linhas))

    def efeito(self, texto, tipo="info"):
        self._enviar(Text(f" {texto} ", style=CHIPS.get(tipo, CHIPS["info"])), chip=True, tipo="chip")

    def cena(self, titulo, subtitulo=None, tipo="evento"):
        if tipo == "combate":
            t = Text()
            t.append("\n⚔ ", style="red")
            t.append(titulo.upper(), style="bold red")
            if subtitulo:
                t.append(f" · {subtitulo}", style="italic grey58")
            self._enviar(t)
            self.ultimo = "outro"
            return
        cabecalho = cabecalho_cena(titulo, subtitulo, tipo)
        if self.escolhas_na_cena > 0:
            if self.novo_desde_escolha:
                self._continuar()
            self.app.call_from_thread(self.app.nova_cena, cabecalho)
            self.escolhas_na_cena = 0
            self.novo_desde_escolha = False
        else:
            # A cena anterior era só uma introdução (ex.: "Explorando"): o novo título a substitui,
            # e o texto de introdução continua na mesma página.
            self.app.call_from_thread(self.app.trocar_cabecalho, cabecalho)
        self.ultimo = "outro"

    def novo_turno(self, n):
        self.app.call_from_thread(self.app.novo_turno, n)

    # Entrada ----------------------------------------------------------
    def _esperar(self):
        resposta = self.respostas.get()
        if resposta is None:
            raise SystemExit(0)
        return resposta

    def atualizar(self):
        self.atualizar_hud()

    def atualizar_hud(self):
        g = self.jogo
        if g and g.j and g.mundo:
            self.app.call_from_thread(self.app.atualizar_hud, painel_status(g), painel_mapa(g, 40, 14),
                                      painel_vitais(g), painel_combate(g))

    def escolher(self, pergunta, opcoes):
        titulo = pergunta or "O que você faz?"
        if len(titulo) > 60:  # perguntas longas são parte da história: vão para a página
            self.dizer(titulo, "ciano")
            titulo = "O que você faz?"
        self.atualizar_hud()
        self.app.call_from_thread(self.app.mostrar_opcoes, opcoes, titulo)
        i = self._esperar()
        self.app.call_from_thread(self.app.adicionar, Text(f"› {opcoes[i]}", style="italic grey58"), False,
                                  False, False)
        self.escolhas_na_cena += 1
        self.novo_desde_escolha = False
        return i

    def _continuar(self):
        self.atualizar_hud()
        self.app.call_from_thread(self.app.mostrar_opcoes, ["Continuar ▸"], "")
        self._esperar()
        self.novo_desde_escolha = False
        self.escolhas_na_cena += 1  # quem tocou em Continuar já leu: a próxima cena abre página nova

    def perguntar(self, pergunta, padrao=""):
        self.app.call_from_thread(self.app.pedir_texto, pergunta, padrao)
        resposta = self._esperar() or padrao
        self.escolhas_na_cena += 1
        self.novo_desde_escolha = False
        return resposta

    def pausar(self):
        if self.novo_desde_escolha:
            self._continuar()


class AppRPG(App):
    TITLE = "Crônicas da Fenda"
    SUB_TITLE = "um RPG de texto onde nenhuma jornada é igual"
    CSS = """
    Screen { align: center top; }
    #raiz { width: 100%; max-width: 150; }
    #principal { width: 1fr; align-horizontal: center; }
    #cena { height: 1fr; max-width: 84; border: round $primary-darken-1; padding: 1 4; scrollbar-size-vertical: 1; }
    #historico { height: 1fr; display: none; border: round $warning; padding: 0 1; }
    #combate { height: auto; display: none; max-width: 84; border: heavy $error; padding: 0 1; }
    #vitais { height: auto; max-width: 84; border: round $warning-darken-1; padding: 0 1; }
    #opcoes { height: auto; max-height: 16; max-width: 84; border: round $accent; }
    #entrada { display: none; max-width: 84; border: round $accent; }
    #lateral { width: 46; }
    #status { height: auto; border: round $secondary; padding: 0 1; }
    #mapa { height: 1fr; border: round $secondary; padding: 0 1; }
    """
    BINDINGS = [
        Binding("ctrl+q", "quit", "Sair"),
        Binding("f2", "historico", "Histórico"),
        Binding("f3", "velocidade", "Velocidade do texto"),
    ]

    def __init__(self, args, menu_principal):
        super().__init__()
        self.args = args
        self.menu_principal = menu_principal
        self.ui = TextualUI(self)
        self.n_opcoes = 0
        self.partes = []          # [renderable, esmaecido, é_linha_de_etiquetas]
        self.fila = deque()       # (renderable, revelar, chip, rapido) ainda não exibidos
        self.revelando = None     # [Text, caracteres_mostrados, rapido]
        self.opcoes_pendentes = None
        self.velocidade = getattr(args, "velocidade", None) or "normal"

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="raiz"):
            with Vertical(id="principal"):
                with VerticalScroll(id="cena"):
                    yield Static(id="cena_texto")
                yield RichLog(id="historico", wrap=True, markup=False, highlight=False, max_lines=6000)
                yield Static(id="combate")
                yield Static(id="vitais")
                yield OptionList(id="opcoes")
                yield Input(id="entrada")
            with Vertical(id="lateral"):
                yield Static(Text("Bem-vindo, aventureiro.", style="grey58"), id="status")
                yield Static(id="mapa")
        yield Footer()

    def on_mount(self):
        self.query_one("#status").border_title = "Herói"
        self.query_one("#mapa").border_title = "Mapa"
        self.query_one("#vitais").border_title = "Condição"
        self.query_one("#historico").border_title = "Histórico (F2 para voltar)"
        self.set_interval(1 / 60, self._tick)
        self.run_worker(self._executar_jogo, thread=True, exit_on_error=True)

    def _executar_jogo(self):
        try:
            self.menu_principal(self.ui, self.args)
        except SystemExit:
            pass
        self.call_from_thread(self.exit)

    # Página da cena -----------------------------------------------------
    def adicionar(self, conteudo, revelar, chip, rapido):
        self.query_one("#historico", RichLog).write(conteudo, expand=True)
        self.fila.append((conteudo, revelar, chip, rapido))

    def nova_cena(self, cabecalho):
        self._revelar_tudo()
        self.partes = []
        self.query_one("#historico", RichLog).write(Rule(style="grey35"), expand=True)
        self.adicionar(cabecalho, False, False, False)
        self.fila[-1] = (cabecalho, False, "cabecalho", False)

    def trocar_cabecalho(self, cabecalho):
        self._revelar_tudo()
        self.query_one("#historico", RichLog).write(cabecalho, expand=True)
        for parte in self.partes:
            if parte[2] == "cabecalho":
                parte[0] = cabecalho
                self._renderizar()
                return
        self.partes.insert(0, [cabecalho, False, "cabecalho"])
        self._renderizar()

    def novo_turno(self, n):
        self._revelar_tudo()
        for p in self.partes:
            p[1] = True
        self.partes = self.partes[-30:]
        self.adicionar(Rule(Text(f" turno {n} ", style="grey62"), style="grey35"), False, False, False)

    def _fixar(self, conteudo, chip):
        if chip is True and self.partes and self.partes[-1][2] is True and not self.partes[-1][1]:
            linha = self.partes[-1][0].copy()
            linha.append("  ")
            linha.append_text(conteudo)
            self.partes[-1][0] = linha
        else:
            self.partes.append([conteudo, False, chip])

    def _cps(self, rapido):
        base = VELOCIDADES.get(self.velocidade, 140)
        return base * 3 if rapido else base

    def _tick(self):
        mudou = False
        if self.revelando is None:
            while self.fila:
                conteudo, revelar, chip, rapido = self.fila.popleft()
                mudou = True
                if revelar and isinstance(conteudo, Text) and self._cps(rapido) and len(conteudo) > 0:
                    self.revelando = [conteudo, 0.0, rapido]
                    break
                self._fixar(conteudo, chip)
        if self.revelando is not None:
            texto, n, rapido = self.revelando
            n += self._cps(rapido) / 60
            mudou = True
            if n >= len(texto):
                self._fixar(texto, False)
                self.revelando = None
            else:
                self.revelando[1] = n
        if mudou:
            self._renderizar()
        if self.opcoes_pendentes is not None and self.revelando is None and not self.fila:
            opcoes, titulo = self.opcoes_pendentes
            self.opcoes_pendentes = None
            self._exibir_opcoes(opcoes, titulo)

    def _revelar_tudo(self):
        if self.revelando is not None:
            self._fixar(self.revelando[0], False)
            self.revelando = None
        while self.fila:
            conteudo, _, chip, _ = self.fila.popleft()
            self._fixar(conteudo, chip)
        self._renderizar()

    def _renderizar(self):
        blocos = []
        for conteudo, esmaecido, _ in self.partes:
            if esmaecido and isinstance(conteudo, Text):
                conteudo = Text(conteudo.plain, style="grey35")
            blocos.append(conteudo)
        if self.revelando is not None:
            texto, n, _ = self.revelando
            blocos.append(texto[: int(n)])
        self.query_one("#cena_texto", Static).update(Group(*blocos))
        self.query_one("#cena", VerticalScroll).scroll_end(animate=False)

    # Opções ---------------------------------------------------------------
    def mostrar_opcoes(self, opcoes, titulo):
        lista = self.query_one("#opcoes", OptionList)
        lista.clear_options()
        self.n_opcoes = 0
        if self.revelando is not None or self.fila:
            lista.border_title = "… (qualquer tecla para adiantar o texto)"
            self.opcoes_pendentes = (opcoes, titulo)
        else:
            self._exibir_opcoes(opcoes, titulo)

    def _exibir_opcoes(self, opcoes, titulo):
        lista = self.query_one("#opcoes", OptionList)
        lista.clear_options()
        rotulos = []
        for i, o in enumerate(opcoes):
            tecla = TECLAS[i] if i < len(TECLAS) else " "
            rotulos.append(Option(Text.assemble((f"{tecla} ", "bold yellow"), o)))
        lista.add_options(rotulos)
        lista.highlighted = 0
        lista.border_title = titulo or "Enter para continuar"
        lista.display = True
        lista.focus()
        self.n_opcoes = len(opcoes)

    def pedir_texto(self, pergunta, padrao):
        self.adicionar(Text(pergunta, style="cyan bold"), False, False, False)
        self._revelar_tudo()
        self.query_one("#opcoes", OptionList).display = False
        entrada = self.query_one("#entrada", Input)
        entrada.placeholder = padrao or "digite e aperte Enter"
        entrada.value = ""
        entrada.display = True
        entrada.focus()

    def atualizar_hud(self, status, mapa_texto, vitais, combate):
        self.query_one("#status", Static).update(status)
        self.query_one("#mapa", Static).update(mapa_texto)
        self.query_one("#vitais", Static).update(vitais)
        painel = self.query_one("#combate", Static)
        painel.display = combate is not None
        if combate is not None:
            painel.update(combate)

    # Eventos da interface ---------------------------------------------
    def _responder(self, indice):
        lista = self.query_one("#opcoes", OptionList)
        lista.clear_options()
        lista.border_title = ""
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
        if evento.key in ("f2", "f3", "ctrl+q"):
            return
        if self.revelando is not None or self.fila:
            evento.stop()
            self._revelar_tudo()  # qualquer tecla adianta o texto
            return
        if self.n_opcoes == 1 and evento.key in ("space", "enter"):
            evento.stop()
            self._responder(0)
            return
        if self.n_opcoes and evento.character and evento.character in TECLAS:
            i = TECLAS.index(evento.character)
            if i < self.n_opcoes:
                evento.stop()
                self._responder(i)

    def on_click(self, evento):
        if self.revelando is not None or self.fila:
            self._revelar_tudo()

    def action_historico(self):
        cena = self.query_one("#cena")
        hist = self.query_one("#historico", RichLog)
        mostrar = not hist.display
        hist.display = mostrar
        cena.display = not mostrar
        if mostrar:
            hist.scroll_end(animate=False)

    def action_velocidade(self):
        ordem = ["normal", "rapido", "instantaneo", "lento"]
        self.velocidade = ordem[(ordem.index(self.velocidade) + 1) % len(ordem)]
        self.notify(f"Velocidade do texto: {self.velocidade}", timeout=2)

    def action_quit(self):
        self.ui.respostas.put(None)
        self.exit()
