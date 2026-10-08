"""Trava do estilo pixel art da interface (ver docs/ARQUITETURA.md, "A interface web").

Nos arquivos de CSS já migrados para os materiais em pixel, ficam proibidos: canto arredondado, degradê radial ou
liso (todo degradê tem de ter paradas duras), sombra borrada, desfoque, cor translúcida, filtro de cor, ruído vetorial
e borda grossa (moldura dentro de moldura). Os arquivos que ainda não migraram ficam em PENDENTES; cada passo da
migração tira os seus da lista, e o teste avisa quando um pendente já está limpo (para a lista só encolher).
"""

import pathlib
import re
import unittest

ESTATICO = pathlib.Path(__file__).resolve().parent.parent / "rpg" / "web" / "static"
CSS = sorted((ESTATICO / "css").glob("*.css"))

PENDENTES = {
    "01-base.css", "02-hud.css", "03-batalha.css", "04-pagina.css", "05-paineis.css", "06-talentos-avisos.css",
    "07-titulo-responsivo.css", "08-mercado.css", "09-comitiva.css", "10-contratos.css", "12-acoes-combate.css",
}

PROIBIDO = {
    "canto arredondado": r"border(-[a-z]+)*-radius\s*:(?!\s*0\s*[;}!])",
    "degradê radial": r"radial-gradient\(",
    "ruído vetorial": r"feTurbulence",
    "desfoque": r"blur\(",
    "cor translúcida": r"\brgba\(|\bhsla\(|color-mix\(",
    "filtro de cor": r"\b(grayscale|sepia|hue-rotate|brightness|saturate|contrast|drop-shadow)\(",
    "borda grossa": r"\bborder(-(top|right|bottom|left))?(-width)?\s*:\s*[^;{}]*\b([3-9]|\d{2,})px",
}
NUMERO = re.compile(r"^-?(\d+\.?\d*|\.\d+)(px|em|rem)?$")


def _sem_comentarios(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def _partes(valor):
    """Separa por vírgula fora de parênteses (camadas de sombra, paradas de um degradê)."""
    partes, nivel, atual = [], 0, ""
    for ch in valor:
        if ch == "(":
            nivel += 1
        elif ch == ")":
            nivel -= 1
        if ch == "," and nivel == 0:
            partes.append(atual.strip())
            atual = ""
        else:
            atual += ch
    if atual.strip():
        partes.append(atual.strip())
    return partes


def _tokens(texto):
    """Palavras de primeiro nível (um calc(...) ou var(...) inteiro conta como uma)."""
    tokens, nivel, atual = [], 0, ""
    for ch in texto:
        if ch == "(":
            nivel += 1
        elif ch == ")":
            nivel -= 1
        if ch.isspace() and nivel == 0:
            if atual:
                tokens.append(atual)
            atual = ""
        else:
            atual += ch
    if atual:
        tokens.append(atual)
    return tokens


def _eh_comprimento(token):
    return bool(NUMERO.match(token)) or token.startswith("calc(") or token in ("var(--P)", "var(--px)", "var(--borda)")


def _sombras_borradas(css):
    achados = []
    for m in re.finditer(r"\b(box-shadow|text-shadow)\s*:\s*([^;{}]+)", css):
        for parte in _partes(m.group(2)):
            comprimentos = [t for t in _tokens(parte) if t != "inset" and _eh_comprimento(t)]
            if len(comprimentos) >= 3 and not re.fullmatch(r"-?0+(\.0+)?(px)?", comprimentos[2]):
                achados.append(f"{m.group(1)}: {parte[:60]}")
    return achados


def _degrades_lisos(css):
    """Todo degradê precisa de paradas duras: cada cor com posição (e as faixas encostando)."""
    achados = []
    for m in re.finditer(r"\b(repeating-)?(linear|conic)-gradient\(", css):
        inicio, nivel, i = m.end(), 1, m.end()
        while i < len(css) and nivel:
            nivel += {"(": 1, ")": -1}.get(css[i], 0)
            i += 1
        partes = _partes(css[inicio:i - 1])
        if partes and re.match(r"^(to |from |at |-?\d*\.?\d+(deg|turn|rad))", partes[0]):
            partes = partes[1:]
        if any(len(_tokens(p)) < 2 for p in partes):
            achados.append(css[m.start():m.start() + 70])
    return achados


def violacoes(arquivo):
    css = _sem_comentarios(arquivo.read_text(encoding="utf-8"))
    achados = [f"{nome}: {m.group(0)[:50]}" for nome, padrao in PROIBIDO.items() for m in re.finditer(padrao, css)]
    achados += [f"sombra borrada: {a}" for a in _sombras_borradas(css)]
    achados += [f"degradê liso: {a}" for a in _degrades_lisos(css)]
    return achados


class TestEstiloPixel(unittest.TestCase):
    def test_arquivos_migrados_seguem_o_pixel(self):
        sujos = {a.name: violacoes(a)[:6] for a in CSS if a.name not in PENDENTES and violacoes(a)}
        self.assertEqual(sujos, {}, "CSS já migrado com estilo liso (ou mova de volta para PENDENTES com motivo)")

    def test_pendentes_so_encolhem(self):
        limpos = sorted(a.name for a in CSS if a.name in PENDENTES and not violacoes(a))
        self.assertEqual(limpos, [], "estes já estão limpos: tire de PENDENTES")
        self.assertEqual(sorted(PENDENTES - {a.name for a in CSS}), [], "PENDENTES cita arquivo que não existe")

    def test_letras_da_paleta(self):
        """Toda var(--p-<letra>) no CSS e no mostruário existe na PALETA dos sprites (que a publica no :root)."""
        sprites = (ESTATICO / "sprites.js").read_text(encoding="utf-8")
        bloco = re.search(r"const PALETA = \{(.*?)\};", sprites, re.S).group(1)
        letras = set(re.findall(r"\b(\w):\s*\"#[0-9a-fA-F]{6}\"", bloco))
        fontes = CSS + [ESTATICO.parent.parent.parent / "tests" / "navegador" / "mostruario.html"]
        usadas = {(f.name, l) for f in fontes for l in re.findall(r"--p-(\w)\b", f.read_text(encoding="utf-8"))}
        self.assertEqual(sorted(u for u in usadas if u[1] not in letras), [])

    def test_o_lint_pega_o_que_deve(self):
        """O próprio lint: pega o estilo liso e deixa passar o pixel."""
        liso = ".a { border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,.5); background: linear-gradient(#000, #111); }"
        pixel = (".a { border-radius: 0; box-shadow: inset var(--P) var(--P) 0 var(--p-d), 0 var(--P) 0 var(--p-k); "
                 "background: linear-gradient(var(--p-k) 0 50%, var(--p-d) 0); border: var(--borda) solid var(--p-k); }")
        tmp = pathlib.Path(self._testMethodName)
        try:
            tmp.write_text(liso, encoding="utf-8")
            achados = violacoes(tmp)
            for esperado in ("canto arredondado", "cor translúcida", "sombra borrada", "degradê liso"):
                self.assertTrue(any(a.startswith(esperado) for a in achados), esperado)
            tmp.write_text(pixel, encoding="utf-8")
            self.assertEqual(violacoes(tmp), [])
        finally:
            tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
