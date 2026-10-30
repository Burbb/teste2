"""A cena de Morel comendo no canto da taverna (protótipo): as camadas de cada pose e a fonte em Aseprite.

    python ferramentas/prototipos/taverna/morel/canto/cena.py --previa <pasta>   # as 20 poses recompostas em PNG
    python ferramentas/prototipos/taverna/morel/canto/cena.py --criar            # monta canto.aseprite (só se não
                                                                                 # existir; --refazer descarta retoques)

**A fonte** `canto.aseprite` (320×96, 20 quadros, um por pose, com a etiqueta do nome; as poses e a ordem são as da
vista aprovada, para a linha do tempo e a reação ao pagamento continuarem as mesmas) tem as camadas, de baixo para
cima: `guia` (a referência reduzida, no lugar dela, oculta e fora da exportação), `parede` (as duas paredes, os
esteios, a travessa), `espada`, `morel_corpo` (o tronco), `morel_cabeca`, `mesa` (o tampo), `objetos` (o castiçal, a
vela, a caneca, o pão, a tigela), `morel_esquerdo` (o braço que descansa, a mão e a ombreira escura), `morel_braco`
(o braço da colher, a mão, a colher e a ombreira clara), `chamas` (a chama da vela, nos quatro primeiros quadros) e
`juntas` (um pixel de cor por junta, oculta) e `construcao` (oculta: a perspectiva da sala, com o horizonte, o ponto
de fuga e as fugas da parede da esquerda e da mesa, e a construção do tronco, com o ovo da caixa torácica, o pescoço,
as clavículas, as juntas dos ombros e as axilas). Depois de montada, a fonte é a autoridade: `exportar.py` só lê dela.

**O que se move, pose a pose** (`juntas.py`): o braço da colher (o cotovelo pela cinemática, a colher rígida); o tronco
e a cabeça descem 1 px para a tigela enquanto ele come e a cabeça vai ao encontro da colher na boca (até 3 px); a
ombreira clara acompanha a junta do ombro; o braço que descansa acompanha o tronco no ombro, com a mão parada no
tampo. A cabeça: os olhos na tigela, a boca aberta para a colher, o queixo mastigando, o olhar para quem está à mesa."""
import pathlib
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[4]
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(RAIZ / "ferramentas" / "arte"))

import espaco as ES  # noqa: E402
import juntas as J  # noqa: E402
import morel as MO  # noqa: E402
import objetos as OB  # noqa: E402
import tronco_estudo as TE  # noqa: E402

FONTE = AQUI / "canto.aseprite"
REFERENCIA = RAIZ / "ferramentas" / "arte" / "referencias" / "cenarios internos" / "Encontro com Morel na taverna.png"
CAMADAS = ["guia", "parede", "espada", "morel_corpo", "morel_cabeca", "mesa", "objetos", "morel_esquerdo",
           "morel_braco", "chamas", "juntas", "construcao"]
OCULTAS = ("guia", "juntas", "construcao")
# o braço que descansa (na tela, à direita): o ombro embaixo da ombreira escura, o cotovelo pousado para fora, a mão
# espalmada no tampo ao lado da tigela (a mão não se move; o ombro acompanha o tronco)
ESQ = dict(S=(206, 46), E=(221, 67), W=(209, 74), M=(202, 75))


def _img(px):
    a = np.zeros((ES.H, ES.W, 4), np.uint8)
    for (x, y), c in px.items():
        if 0 <= x < ES.W and 0 <= y < ES.H:
            a[y, x] = c
    return Image.fromarray(a, "RGBA")


def _pixels(img):
    a = np.array(img)
    ys, xs = np.nonzero(a[:, :, 3])
    return {(int(x), int(y)): tuple(int(v) for v in a[y, x]) for y, x in zip(ys, xs)}


def guia():
    """A referência reduzida (240×96, no tamanho dela) no lugar em que a cena a transpõe."""
    ref = Image.open(REFERENCIA).convert("RGBA").resize((240, 96), Image.BOX)
    g = Image.new("RGBA", (ES.W, ES.H), (0, 0, 0, 0))
    g.paste(ref, (ES.OX, 0))
    return g


def estaticas():
    """As camadas que não mudam: as paredes e os esteios, o tampo, os objetos."""
    parede = Image.new("RGBA", (ES.W, ES.H), (0, 0, 0, 0))
    ES.parede_fundo(parede)
    ES.parede_lateral(parede)
    ES.esteio(parede, *ES.CANTO)
    ES.esteio(parede, *ES.ESTEIO_DIR)
    mesa = Image.new("RGBA", (ES.W, ES.H), (0, 0, 0, 0))
    ES.tampo(mesa)
    obj = Image.new("RGBA", (ES.W, ES.H), (0, 0, 0, 0))
    OB.objetos(obj)
    return dict(parede=parede, mesa=mesa, objetos=obj)


def chamas(q):
    im = Image.new("RGBA", (ES.W, ES.H), (0, 0, 0, 0))
    OB.chama(im, q)
    return im


def pose(p):
    """As camadas de Morel numa pose de `juntas.poses()`."""
    dy = p["dy"]
    corpo = MO.tronco(dy)
    c = dict(espada=_img(MO.espada(dy)), morel_corpo=_img(corpo),
             morel_cabeca=_img(MO.cabeca(p["cabeca"], dy + p["dyc"])))
    # o braço que descansa: o ombro desce com o tronco, a mão fica
    S = (ESQ["S"][0], ESQ["S"][1] + dy)
    esq, _ = MO.braco(S, ESQ["E"], ESQ["W"], corpo)
    esq.update(MO.mao(ESQ["M"], 8.0, 5.0))
    esq.update(MO.ombreira_esquerda(dy))
    c["morel_esquerdo"] = _img(esq)
    dir_, ante = MO.braco(p["S"], p["E"], p["W"], corpo)
    # a ombreira clara por cima da manga, mas atrás do antebraço quando ele sobe na frente do ombro
    for q, cor in MO.ombreira_direita(p["S"]).items():
        if q not in ante:
            dir_[q] = cor
    # a mão em volta do cabo: o centro um pouco além do pulso, na direção da colher; a colher sai dela
    d = p["dir_colher"]
    mao = (p["W"][0] + d[0] * 5, p["W"][1] + d[1] * 5)
    dir_.update(MO.colher((p["W"][0] + d[0] * 7, p["W"][1] + d[1] * 7), p["T"]))
    dir_.update(MO.mao(mao, 7.0, 6.0))
    c["morel_braco"] = _img(dir_)
    jj = {}
    for k, cor in (("S", (255, 64, 64, 255)), ("E", (48, 255, 96, 255)), ("W", (48, 128, 255, 255)),
                   ("T", (255, 224, 48, 255))):
        jj[(round(p[k][0] - 0.5), round(p[k][1] - 0.5))] = cor
    c["juntas"] = _img(jj)
    return c


def construcao():
    """A guia oculta da construção: a perspectiva da sala e, por cima, a do tronco (na pose de repouso)."""
    im = ES.guia_perspectiva()
    with tempfile.TemporaryDirectory() as tmp:
        arq = pathlib.Path(tmp) / "tronco.png"
        TE.guia(arq)
        im.alpha_composite(Image.open(arq).convert("RGBA"))
    return im


def quadros():
    """[(nome, {camada: Image})] na ordem de juntas.ROTEIRO."""
    fixas = estaticas()
    g = guia()
    fixas["construcao"] = construcao()
    out = []
    for i, p in enumerate(J.poses()):
        c = dict(fixas, guia=g, **pose(p))
        c["chamas"] = chamas(i % 4) if i < 4 else Image.new("RGBA", (ES.W, ES.H), (0, 0, 0, 0))
        out.append((p["nome"], c))
    return out


def compor(c, com_chama=True):
    im = Image.new("RGBA", (ES.W, ES.H), (0, 0, 0, 0))
    for n in CAMADAS:
        if n in OCULTAS or (n == "chamas" and not com_chama):
            continue
        im.alpha_composite(c[n])
    return im


_MONTAR = r'''
local D = dofile(app.params["dados"])
local s = Sprite(320, 96, ColorMode.RGB)
s.layers[1].name = D.camadas[1]
for i = 2, #D.camadas do local l = s:newLayer(); l.name = D.camadas[i] end
for i = 2, #D.quadros do s:newEmptyFrame() end
local n = 0
for i, nome in ipairs(D.quadros) do
  local t = s:newTag(i, i); t.name = nome
  s.frames[i].duration = 0.1
  for j, c in ipairs(D.camadas) do
    local arq = app.params["pasta"] .. "/" .. c .. "-" .. (i - 1) .. ".png"
    local f = io.open(arq, "r")
    if f then
      f:close()
      s:newCel(s.layers[j], s.frames[i], Image{ fromFile = arq }, Point(0, 0))
      n = n + 1
    end
  end
end
for _, l in ipairs(s.layers) do
  if D.ocultas[l.name] then l.isVisible = false end
end
s:saveAs(app.params["saida"])
print("montada: " .. n .. " células")
'''


def criar(refazer=False):
    from exportar_aseprite import aseprite
    if FONTE.exists() and not refazer:
        sys.exit(f"{FONTE.name} já existe e é a autoridade; use --refazer para descartar os retoques e montar de novo.")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        nomes = []
        for i, (nome, c) in enumerate(quadros()):
            nomes.append(nome)
            for camada in CAMADAS:
                if c[camada].getbbox():
                    c[camada].save(tmp / f"{camada}-{i}.png")
        dados = tmp / "dados.lua"
        dados.write_text("return {camadas={" + ",".join(f'"{c}"' for c in CAMADAS) + "}, quadros={"
                         + ",".join(f'"{q}"' for q in nomes) + "}, ocultas={"
                         + ",".join(f'["{c}"]=true' for c in OCULTAS) + "}}", encoding="utf-8")
        lua = tmp / "montar.lua"
        lua.write_text(_MONTAR, encoding="utf-8")
        r = subprocess.run([aseprite(), "-b", "--script-param", f"dados={dados}", "--script-param", f"pasta={tmp}",
                            "--script-param", f"saida={FONTE}", "--script", str(lua)], capture_output=True, text=True)
        ok = [x for x in r.stdout.splitlines() if x.startswith("montada")]
        if not ok or not FONTE.exists():
            sys.exit(f"o Aseprite não montou a fonte:\n{r.stdout}{r.stderr}")
        print(ok[0], f"({len(nomes)} poses)")


def previa(saida):
    saida = pathlib.Path(saida)
    saida.mkdir(parents=True, exist_ok=True)
    for i, (nome, c) in enumerate(quadros()):
        compor(c).save(saida / f"{i:02d}-{nome}.png")
    print(f"prévia em {saida}")


if __name__ == "__main__":
    if "--previa" in sys.argv:
        previa(sys.argv[-1])
    elif "--criar" in sys.argv or "--refazer" in sys.argv:
        criar("--refazer" in sys.argv)
