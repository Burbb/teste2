"""As moedas do pagamento na mesa de Morel (protótipo): a fonte, a folha e o lançamento.

    python ferramentas/prototipos/taverna/morel/moedas/moedas.py --criar    # a fonte, das grades (só se não existir)
    python ferramentas/prototipos/taverna/morel/moedas/moedas.py            # exporta para camadas/morel-vista/

**O desenho** é à mão, em grade (um caractere por pixel, abaixo), na escala da vista (a cabeça de Morel tem 21 px: uma
moeda de uns 2,5 cm tem 3 px): a moeda deitada (o tampo de cima aceso pelo lado da vela, a borda da frente escura), a
inclinada (de quina, girando), a de pé (só a borda) e a sombra de contato (o tampo escurecido, meio transparente, para
servir na madeira clara e na escura). `--criar` pinta as grades em `moedas.aseprite`, cada desenho numa célula de 4×4;
depois a fonte é a autoridade (retoque no editor; o script não a sobrescreve) e a exportação lê dela.

**O lançamento** (calculado aqui; a arte não): um punhado de cinco moedas, jogadas de quem está sentado diante de Morel,
entra pela borda de baixo do quadro, voa por cima da borda da mesa girando (deitada, de quina, de pé), cai no tampo
entre a vela e a tigela, dá um pulinho (2 px, depois 1) e escorrega 1 ou 2 px; uma cai de pé, rola um pouco e tomba.
A sombra corre no tampo embaixo de cada uma enquanto ela voa por cima dele e encosta quando ela assenta. As moedas não
somem: a última imagem fica na mesa até a cena acabar. Um tique é o relógio da cena (100 ms).

**A reação de Morel** (`reacao` no JSON): a colher para e volta ao descanso pelo caminho mais curto entre as poses que
já existem (descendo, se ele estava descendo; desfazendo a subida, se subia), os olhos ficam nas moedas enquanto elas
caem e ele conta, depois ele olha para quem pagou e volta a comer. Só a reação que o pagamento pede: as poses são as da
vista aprovada (`repousa` com os olhos baixos, `olha`), nenhuma nova.

Saídas: `camadas/morel-vista/moedas.png` (a folha: as células da fonte) e `moedas.json` (os quadros do lançamento, a
imagem final, a reação)."""
import json
import pathlib
import subprocess
import sys
import tempfile

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[4]
sys.path.insert(0, str(RAIZ / "ferramentas" / "arte"))

from exportar_aseprite import aseprite  # noqa: E402

FONTE = AQUI / "moedas.aseprite"
SAIDA = AQUI.parents[1] / "camadas" / "morel-vista"
PINTAR = RAIZ / "ferramentas" / "arte" / "aseprite" / "pintar.lua"
CELULA = 4

# a paleta: o latão da vista (o c09a40 já está na cena), aceso pelo lado da vela; a sombra é o tampo escurecido
CORES = {"L": "e8c46a", "M": "c09a40", "m": "9a7630", "d": "6a5020", "s": "1e1008a0", "t": "1e100860"}
# as grades, desenhadas à mão (o "." não pinta)
DESENHOS = {
    "deitada": ["LMm",
                "mdd"],
    "inclinada": ["LM",
                  "Mm",
                  "md"],
    "pe": ["M",
           "m",
           "d"],
    "sombra": ["sss"],        # embaixo da moeda deitada, encostada
    "sombra_alta": ["tt"],    # no tampo, embaixo da moeda que voa por cima dele
}
ORDEM = list(DESENHOS)


def _lista():
    """As grades na tela da fonte, uma célula por desenho, como texto do pintar.lua."""
    pts = []
    for i, nome in enumerate(ORDEM):
        for y, linha in enumerate(DESENHOS[nome]):
            for x, ch in enumerate(linha):
                if ch != ".":
                    pts.append(f"{i * CELULA + x},{y},{CORES[ch]}")
    return ";".join(pts)


def criar():
    if FONTE.exists():
        sys.exit(f"{FONTE.name} já existe e é a autoridade (retoques no editor); apague-a para criar de novo.")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        dados = tmp / "moedas.lua"
        dados.write_text(f'return "{_lista()}"', encoding="utf-8")
        lua = tmp / "criar.lua"
        lua.write_text(
            'local P = dofile(app.params["pintar"])\n'
            f'local s = Sprite({CELULA * len(ORDEM)}, {CELULA}, ColorMode.RGB)\n'
            's.layers[1].name = "moedas"\n'
            'print(P.pintar_arquivo("moedas", app.params["dados"]))\n'
            's:saveAs(app.params["saida"])\n', encoding="utf-8")
        r = subprocess.run([aseprite(), "-b", "--script-param", f"pintar={PINTAR}", "--script-param", f"dados={dados}",
                            "--script-param", f"saida={FONTE}", "--script", str(lua)], capture_output=True, text=True)
        print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr)


# ------------------------------------------------------------------ o lançamento
# cada moeda: onde assenta (o canto de cima da deitada), de onde sai (o chão embaixo da mão, abaixo do quadro), o tique
# em que sai da mão, quantos tiques voa, o último escorregão (dx, dy) e se cai de pé e rola
MOEDAS = [
    dict(fim=(163, 83), sai=(178, 106), t0=0, voo=5, escorrega=(-1, 0)),
    dict(fim=(170, 86), sai=(183, 106), t0=0, voo=4, escorrega=(1, 0)),
    dict(fim=(176, 81), sai=(186, 106), t0=1, voo=5, escorrega=(0, 0)),
    dict(fim=(182, 85), sai=(190, 106), t0=1, voo=4, escorrega=(1, 0)),
    dict(fim=(181, 79), sai=(188, 106), t0=2, voo=5, rola=(3, -1)),
]
ALTO = 15        # a altura da curva sobre o chão, no meio do voo (px na tela)
SOLTA = 10       # a altura da mão quando solta (a mão fica embaixo, fora do quadro)
GIRO = ["deitada", "inclinada", "pe", "inclinada"]
TAMPO = (63, 91)  # as linhas do tampo na tela: a sombra só aparece nele


def _trajeto(i, m):
    """A moeda tique a tique: (desenho, x, y, sombra) do canto de cima do desenho; a sombra no chão embaixo dela."""
    (fx, fy), (sx, sy), n = m["fim"], m["sai"], m["voo"]
    rola = m.get("rola")
    # onde ela toca o tampo pela primeira vez: antes do pulinho e do escorregão (ou do rolar)
    if rola:
        tx, ty = fx - rola[0], fy - rola[1]
    else:
        ex, ey = m["escorrega"]
        tx, ty = fx - ex, fy - ey + 1
    q = [None] * m["t0"]
    for k in range(1, n + 1):  # o voo: o chão vai da mão ao toque, a altura é uma parábola que começa na mão
        u = k / n
        gx, gy = sx + (tx - sx) * u, sy + (ty - sy) * u
        h = SOLTA * (1 - u) + ALTO * 4 * u * (1 - u)
        des = GIRO[(k + i) % 4] if k < n else ("pe" if rola else "deitada")
        q.append((des, round(gx), round(gy - h), (round(gx), round(gy)) if h > 1 else None))
    if rola:  # caiu de pé: rola na direção do arremesso e tomba
        for k in range(1, rola[0] + 1):
            q.append(("pe", tx + k, round(ty + rola[1] * k / rola[0]), None))
        q += [("inclinada", fx, fy - 1, None), ("deitada", fx, fy, None)]
        return q
    q += [("inclinada", tx, ty - 2, (tx, ty)), ("deitada", tx, ty - 1, None),  # o pulinho de 2 px e o de 1
          ("deitada", tx, ty - 1, None)]
    if (ex, ey) != (0, 0):
        q.append(("deitada", tx + ex, ty - 1 + ey, None))  # o escorregão
    q.append(("deitada", fx, fy, None))
    return q


def lancamento():
    trajetos = [_trajeto(i, m) for i, m in enumerate(MOEDAS)]
    n = max(len(t) for t in trajetos)
    quadros = []
    for k in range(n):
        q = []
        for t in trajetos:
            p = t[min(k, len(t) - 1)]
            if p is None:
                continue
            des, x, y, sombra = p
            if sombra and TAMPO[0] <= sombra[1] <= TAMPO[1]:
                q.append(["sombra_alta", sombra[0], sombra[1] + 1])
            elif des == "deitada" and k >= len(t) - 1:
                q.append(["sombra", x + 1, y + 2])  # encostada: um pixel abaixo, do lado oposto à vela
            q.append([des, x, y])
        quadros.append(q)
    return quadros


# ------------------------------------------------------------------ a reação de Morel
# os índices das poses da vista (morel/vista/exportar.py): 0 e 1 recolhem, 2 a 8 sobem, 9 é a boca, 10 a 16 descem,
# 17 repousa (os olhos baixos), 18 mastiga, 19 olha
REPOUSA, OLHA = 17, 19


def _volta(p):
    """As poses do caminho mais curto da pose p ao descanso, sem salto maior que o das passagens que já existem."""
    if 9 <= p <= 16:
        return list(range(p + 1, 17))     # descendo (ou na boca): termina de descer
    if 2 <= p <= 8:
        return list(range(p - 1, 1, -1)) + [0]  # subindo: desfaz a subida e pousa a colher na tigela
    return []                              # 0, 1, 17, 18, 19: já está embaixo


def reacao(quadros):
    return {
        "volta": {str(p): _volta(p) for p in range(20)},
        # enquanto as moedas caem e ele conta (os olhos nelas), depois o olhar para quem pagou, e de volta à tigela
        "depois": [[REPOUSA, len(quadros) + 10], [OLHA, 14], [REPOUSA, 4]],
    }


def exportar():
    with tempfile.TemporaryDirectory() as tmp:
        png = pathlib.Path(tmp) / "moedas.png"
        subprocess.run([aseprite(), "-b", str(FONTE), "--save-as", str(png)], capture_output=True, text=True)
        folha = Image.open(png).convert("RGBA")
    SAIDA.mkdir(parents=True, exist_ok=True)
    folha.save(SAIDA / "moedas.png", optimize=True)
    quadros = lancamento()
    dados = {"celula": CELULA, "desenhos": {n: [i, len(DESENHOS[n][0]), len(DESENHOS[n])] for i, n in enumerate(ORDEM)},
             "quadros": quadros, "reacao": reacao(quadros)}
    with open(SAIDA / "moedas.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, separators=(",", ":"))
    print(f"camadas/morel-vista: moedas.png e moedas.json ({len(MOEDAS)} moedas, {len(quadros)} tiques)")


if __name__ == "__main__":
    criar() if "--criar" in sys.argv else exportar()
