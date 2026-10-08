"""Trava do estilo pixel art da interface (ver docs/ARQUITETURA.md, "A interface web").

Nos arquivos já migrados para os materiais em pixel ficam proibidos: canto arredondado, degradê radial ou liso (todo
degradê tem de ter paradas duras, cada faixa encostando na anterior), sombra borrada (também guardada em variável),
desfoque, cor translúcida (rgba, hex com alfa, opacidade parada), filtro de cor e borda grossa (moldura dentro de
moldura, inclusive outline e borda em texels). Os arquivos que ainda não migraram ficam em PENDENTES; cada passo da
migração tira os seus da lista, e o teste avisa quando um pendente já está limpo (a lista só encolhe).
"""

import pathlib
import re
import unittest

ESTATICO = pathlib.Path(__file__).resolve().parent.parent / "rpg" / "web" / "static"
CSS = sorted((ESTATICO / "css").glob("*.css"))
JS = sorted(p for p in [*ESTATICO.glob("*.js"), *(ESTATICO / "app").glob("*.js")] if p.name != "sprites-dados.js")

PENDENTES = {
    "01-base.css", "02-hud.css", "03-batalha.css", "04-pagina.css", "05-paineis.css", "06-talentos-avisos.css",
    "07-titulo-responsivo.css", "08-mercado.css", "09-comitiva.css", "10-contratos.css", "12-acoes-combate.css",
}
PENDENTES_JS = {"telas.js"}  # filtros de cor em animações feitas pelo JS

FILTRO = r"\b(grayscale|sepia|hue-rotate|brightness|saturate|contrast|invert|opacity|drop-shadow)\(|filter\s*:\s*url\("
PROIBIDO = {
    "canto arredondado": r"border(-[a-z]+)*-radius\s*:(?!\s*(0(px|%|em|rem)?\s*)+[;}!])|clip-path\s*:[^;{}]*(circle|ellipse|\bround\b)",
    "degradê radial": r"radial-gradient\(",
    "ruído vetorial": r"feTurbulence",
    "desfoque": r"blur\(",
    "cor translúcida": r"\b(rgba|hsla)\(|color-mix\(|\b(rgb|hsl|hwb|lab|lch|oklab|oklch)\([^)]*/",
    "filtro de cor": FILTRO,
}
NUMERO = re.compile(r"^-?(\d+\.?\d*|\.\d+)[a-z%]*$")
ZERO = re.compile(r"^-?(0+(\.0*)?|\.0+)[a-z%]*$")


def _sem_comentarios(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def _fecha(texto, inicio):
    """Índice logo depois do parêntese que fecha o aberto antes de `inicio`."""
    nivel, i = 1, inicio
    while i < len(texto) and nivel:
        nivel += {"(": 1, ")": -1}.get(texto[i], 0)
        i += 1
    return i


def _partes(valor, sep=","):
    """Separa por vírgula (ou espaço) fora de parênteses: camadas de sombra, paradas de um degradê, tokens."""
    partes, nivel, atual = [], 0, ""
    for ch in valor:
        nivel += {"(": 1, ")": -1}.get(ch, 0)
        if nivel == 0 and (ch.isspace() if sep == " " else ch == sep):
            if atual.strip():
                partes.append(atual.strip())
            atual = ""
        else:
            atual += ch
    if atual.strip():
        partes.append(atual.strip())
    return partes


def _eh_comprimento(token):
    return bool(NUMERO.match(token)) or token.startswith(("calc(", "var(--P", "var(--px", "var(--borda"))


def _sombra_borrada(valor):
    for camada in _partes(valor):
        comprimentos = [t for t in _partes(camada, " ") if t != "inset" and _eh_comprimento(t)]
        if len(comprimentos) >= 3 and not ZERO.match(comprimentos[2]) and comprimentos[2] != "calc(var(--P) * 0)":
            return camada
    return None


def _sombras_borradas(css):
    achados = []
    declaradas = list(re.finditer(r"\b(box-shadow|text-shadow)\s*:\s*([^;{}]+)", css))
    for m in declaradas:
        camada = _sombra_borrada(m.group(2))
        if camada:
            achados.append(f"{m.group(1)}: {camada[:60]}")
    # a sombra guardada numa variável (--sombra-texto: 0 2px 8px ...) e usada em box-shadow/text-shadow
    nomes = {n for m in declaradas for n in re.findall(r"var\((--[\w-]+)", m.group(2))}
    for m in re.finditer(r"(--[\w-]+)\s*:\s*([^;{}]+)", css):
        if m.group(1) in nomes:
            camada = _sombra_borrada(m.group(2))
            if camada:
                achados.append(f"{m.group(1)}: {camada[:60]}")
    return achados


def _degrades_lisos(css):
    """Todo degradê precisa de paradas duras: cada parada depois da primeira começa em 0 (o CSS prende na anterior) ou
    exatamente onde a anterior terminou."""
    achados = []
    for m in re.finditer(r"\b(repeating-)?(linear|conic)-gradient\(", css):
        partes = _partes(css[m.end():_fecha(css, m.end()) - 1])
        if partes and re.match(r"^(to |from |at |-?\d*\.?\d+(deg|turn|rad|grad)\b)", partes[0]):
            partes = partes[1:]
        elif len(partes) > 1 and len(_partes(partes[0], " ")) == 1 and partes[0].startswith(("var(", "calc(")) \
                and all(len(_partes(p, " ")) > 1 for p in partes[1:]):
            partes = partes[1:]  # ângulo em var() ou calc()
        anterior = None
        for i, parada in enumerate(partes):
            posicoes = _partes(parada, " ")[1:]
            if i and (not posicoes or not (ZERO.match(posicoes[0]) or posicoes[0] == anterior)):
                achados.append(css[m.start():m.start() + 70])
                break
            anterior = posicoes[-1] if posicoes else "0"
    return achados


def _bordas_grossas(css):
    """Moldura dentro de moldura: borda ou outline de 3px ou mais, ou de 2 texels ou mais."""
    achados = []
    for m in re.finditer(r"\b(outline|border(-(top|right|bottom|left|inline|block)(-start|-end)?)?)(-width)?\s*:\s*([^;{}]+)", css):
        valor = m.group(6)
        grossos = [n for n in re.findall(r"(?<![\w.])(\d*\.?\d+)px", valor) if float(n) >= 3]
        texels = [n for n in re.findall(r"var\(--P\)\s*\*\s*(\d*\.?\d+)", valor) if float(n) >= 2]
        if (grossos or texels) and "none" not in valor:
            achados.append(f"{m.group(1)}: {valor[:50]}")
    return achados


def _hex_com_alfa(css):
    """Hex com alfa parcial (#0d0b0a80) mistura cores; alfa 0 (o transparente de um xadrez) ou cheio, não."""
    return [m.group(0) for m in re.finditer(r"#([0-9a-fA-F]{4}|[0-9a-fA-F]{8})\b", css)
            if m.group(1)[len(m.group(1)) // 4 * 3:].lower() not in ("0", "f", "00", "ff")]


def _opacidade_parada(css):
    """Opacidade fracionária fora de animação mistura cores fora da paleta (use um véu pontilhado)."""
    sem_animacoes = re.sub(r"@keyframes[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", css)
    return [m.group(0) for m in re.finditer(r"(?<![\w-])opacity\s*:\s*0?\.\d+", sem_animacoes)]


def violacoes_css(texto):
    css = _sem_comentarios(texto)
    achados = [f"{nome}: {m.group(0)[:50]}" for nome, padrao in PROIBIDO.items() for m in re.finditer(padrao, css)]
    achados += [f"sombra borrada: {a}" for a in _sombras_borradas(css)]
    achados += [f"degradê liso: {a}" for a in _degrades_lisos(css)]
    achados += [f"borda grossa: {a}" for a in _bordas_grossas(css)]
    achados += [f"cor translúcida: {a}" for a in _opacidade_parada(css) + _hex_com_alfa(css)]
    return achados


def violacoes(arquivo):
    return violacoes_css(arquivo.read_text(encoding="utf-8"))


def filtros_js(arquivo):
    """Filtros de cor aplicados pelo JS (el.animate, style.filter): também misturam cores fora da paleta."""
    return [m.group(0)[:60] for m in re.finditer(r"filter[\"']?\s*[:=]\s*[\"'`][^\"'`]*?(" + FILTRO + ")",
                                                 arquivo.read_text(encoding="utf-8"))]


class TestEstiloPixel(unittest.TestCase):
    def test_arquivos_migrados_seguem_o_pixel(self):
        sujos = {a.name: violacoes(a)[:6] for a in CSS if a.name not in PENDENTES and violacoes(a)}
        sujos.update({a.name: filtros_js(a)[:6] for a in JS if a.name not in PENDENTES_JS and filtros_js(a)})
        self.assertEqual(sujos, {}, "estilo liso num arquivo já migrado (ou volte-o a PENDENTES, com o motivo)")

    def test_pendentes_so_encolhem(self):
        limpos = sorted(a.name for a in CSS if a.name in PENDENTES and not violacoes(a))
        limpos += sorted(a.name for a in JS if a.name in PENDENTES_JS and not filtros_js(a))
        self.assertEqual(limpos, [], "estes já estão limpos: tire-os da lista de pendentes")
        existem = {a.name for a in CSS} | {a.name for a in JS}
        self.assertEqual(sorted((PENDENTES | PENDENTES_JS) - existem), [], "pendente que não existe")

    def test_letras_da_paleta(self):
        """Toda var(--p-<letra>) no CSS e no mostruário existe na PALETA dos sprites (que a publica no :root)."""
        sprites = (ESTATICO / "sprites.js").read_text(encoding="utf-8")
        bloco = re.search(r"const PALETA = \{(.*?)\};", sprites, re.S).group(1)
        letras = set(re.findall(r"\b(\w):\s*\"#[0-9a-fA-F]{6}\"", bloco))
        fontes = CSS + [ESTATICO.parent.parent.parent / "tests" / "navegador" / "mostruario.html"]
        usadas = {(f.name, l) for f in fontes for l in re.findall(r"--p-(\w)\b", f.read_text(encoding="utf-8"))}
        self.assertEqual(sorted(u for u in usadas if u[1] not in letras), [])

    def test_a_trava_pega_o_estilo_liso(self):
        casos = {
            "canto arredondado": ".a { border-radius: 4px; }",
            "canto redondo no recorte": ".a { clip-path: inset(0 round 6px); }",
            "sombra borrada": ".a { box-shadow: 0 2px 8px var(--p-k); }",
            "sombra borrada em variável": ":root { --sombra-texto: 0 2px 8px #000; } .a { text-shadow: var(--sombra-texto); }",
            "degradê sem posições": ".a { background: linear-gradient(#000, #111); }",
            "degradê liso com posições": ".a { background: linear-gradient(#000 0%, #fff 100%); }",
            "máscara lisa": ".a { mask-image: linear-gradient(to bottom, transparent 0, #000 38%); }",
            "rgba": ".a { color: rgba(0, 0, 0, .5); }",
            "hex com alfa": ".a { color: #0d0b0a80; }",
            "cor com barra": ".a { color: rgb(0 0 0 / 50%); }",
            "opacidade parada": ".a { opacity: 0.5; }",
            "filtro": ".a { filter: brightness(1.5); }",
            "filtro invert": ".a { filter: invert(1); }",
            "outline grosso": ".a { outline: 3px dashed var(--p-E); }",
            "borda em texels": ".a { border: calc(var(--P) * 3) solid var(--p-k); }",
        }
        for nome, css in casos.items():
            with self.subTest(nome):
                self.assertTrue(violacoes_css(css), f"a trava deixou passar: {css}")

    def test_a_trava_aceita_o_pixel(self):
        casos = {
            "canto zerado": ".a { border-radius: 0px; } .b { border-radius: 0 0 0 0; } .c { border-radius: 0; }",
            "placa": (".a { box-shadow: inset var(--P) var(--P) 0 var(--p-d), 0 var(--P) 0 var(--p-k); "
                      "border: var(--borda) solid var(--p-k); }"),
            "sulco": ".a { background: linear-gradient(var(--p-k) 0 50%, var(--p-d) 0); }",
            "faixas": ".a { background: linear-gradient(180deg, var(--c1) 0 30%, var(--c2) 30% 72%, var(--c3) 72%); }",
            "xadrez": ".a { background: repeating-conic-gradient(#000 0 25%, #0000 0 50%); }",
            "ângulo em variável": ".a { background: linear-gradient(var(--ang), #000 0 50%, #111 0); }",
            "ângulo em grad": ".a { background: linear-gradient(100grad, #000 0 50%, #111 0); }",
            "borda de um texel com folga": ".a { border-width: calc(var(--P) + 0.01px); border: 1.5px solid #000; }",
            "contorno sem desfoque": ".a { text-shadow: var(--P) 0 0 var(--p-k), 0 calc(var(--P) * -1) 0em #000; }",
            "opacidade na animação": "@keyframes x { from { opacity: 0.5; } to { opacity: 1; } }",
        }
        for nome, css in casos.items():
            with self.subTest(nome):
                self.assertEqual(violacoes_css(css), [])


if __name__ == "__main__":
    unittest.main()
