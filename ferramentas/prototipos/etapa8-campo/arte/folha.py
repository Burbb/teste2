"""Campo Livre 8: a folha comparável dos modelos dos heróis (os do Campo Livre 7 e os novos, a candidata), na paleta
sóbria, com as poses lado a lado: parado, as duas passadas, preparo, golpe, recuo. Em cima, no tamanho real do jogo (a
1920 × 1080 o campo é ampliado 3×: a faixa de cima está em 3×, sem suavizar, sobre o chão sóbrio, com um soldado de cada
equipe ao lado para a escala); embaixo, os novos ampliados 6× para ver o pixel.

    python ferramentas/prototipos/etapa8-campo/arte/folha.py [saída.png]

As grades vêm do protótipo (tela/sprites.js, sprites8.js) pelo Node; a figura é montada aqui com o Pillow."""
import json
import pathlib
import subprocess
import sys

from PIL import Image, ImageDraw

AQUI = pathlib.Path(__file__).resolve().parent
TELA = (AQUI.parent / "tela").as_uri() + "/"
POSES = ["parado", "andarA", "andarB", "preparo", "golpe", "recuo"]
HEROIS = ["guerreiro", "mago", "morel", "odette", "lider"]

JS = f"""
const S = await import("{TELA}sprites.js"), A = await import("{TELA}sprites7.js"), N = await import("{TELA}sprites8.js");
const pal = A.PALETAS.sobria, eq = A.EQUIPES_ARTE.sobria;
function grades(mod, cores) {{
  const def = mod.pernas || "juntas";
  const q = {{
    parado: S.montar(mod, "parado", def), andarA: S.montar(mod, mod.andarA ? "andarA" : "parado", mod.pernas ? def : "abertas"),
    andarB: S.montar(mod, mod.andarB ? "andarB" : "parado", mod.pernas ? def : "cruzadas"), preparo: S.montar(mod, "preparo", def),
    golpe: S.montar(mod, "golpe", mod.heroi ? "abertas" : def), recuo: S.montar(mod, mod.recuo ? "recuo" : "parado", def),
  }};
  const out = {{}};
  for (const [p, l] of Object.entries(q)) out[p] = l.map((linha) => [...linha].map((ch) => ch === "." ? null : (cores[ch] || pal[ch] || S.PALETA[ch])));
  return out;
}}
const r = {{ antigos: {{}}, novos: {{}}, soldados: [grades(S.MODELOS.soldado, eq[0]), grades(S.MODELOS.soldado, eq[1])] }};
for (const t of {json.dumps(HEROIS)}) {{
  const eqt = t === "lider" ? 1 : 0;
  r.antigos[t] = grades(S.MODELOS[t], S.MODELOS[t].cores || eq[eqt]);
  r.novos[t] = grades(N.MODELOS_NOVOS[t], N.MODELOS_NOVOS[t].cores || eq[eqt]);
}}
console.log(JSON.stringify(r));
"""


def imagem(grade):
    h, w = len(grade), max(len(l) for l in grade)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y, linha in enumerate(grade):
        for x, cor in enumerate(linha):
            if cor:
                im.putpixel((x, y), tuple(int(cor[i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    return im


def main():
    saida = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI.parent / "capturas" / "cl8-folha-modelos.png"
    dados = json.loads(subprocess.run(["node", "--input-type=module", "-e", JS], capture_output=True, text=True, check=True).stdout)
    chao = (86, 102, 74, 255)
    celula = 22
    # 1) no tamanho do jogo (3×): uma linha por herói, antigo | novo, as seis poses, um soldado de cada equipe no fim
    linhas = []
    for t in HEROIS:
        faixa = Image.new("RGBA", (celula * (len(POSES) * 2 + 3), celula), chao)
        for i, p in enumerate(POSES):
            for k, conj in enumerate(["antigos", "novos"]):
                im = imagem(dados[conj][t][p])
                faixa.alpha_composite(im, (celula * (i + k * (len(POSES) + 1)) + 2, celula - im.height - 2))
        for k in range(2):
            im = imagem(dados["soldados"][k]["parado"])
            faixa.alpha_composite(im, (celula * (len(POSES) * 2 + 1 + k) + 4, celula - im.height - 2))
        linhas.append(faixa)
    real = Image.new("RGBA", (linhas[0].width, celula * len(linhas)), chao)
    for i, f in enumerate(linhas):
        real.alpha_composite(f, (0, i * celula))
    real = real.resize((real.width * 3, real.height * 3), Image.NEAREST)
    # 2) os modelos novos ampliados 6×: o pixel
    novos = Image.new("RGBA", (celula * len(POSES), celula * len(HEROIS)), chao)
    for j, t in enumerate(HEROIS):
        for i, p in enumerate(POSES):
            im = imagem(dados["novos"][t][p])
            novos.alpha_composite(im, (celula * i + 2, celula * (j + 1) - im.height - 2))
    novos = novos.resize((novos.width * 6, novos.height * 6), Image.NEAREST)
    grande = Image.new("RGBA", (real.width, novos.height), chao)
    grande.alpha_composite(novos, (0, 0))
    folha = Image.new("RGBA", (real.width, real.height + 54 + grande.height), (40, 38, 44, 255))
    d = ImageDraw.Draw(folha)
    d.text((6, 6), "No tamanho do jogo (3x): Campo Livre 7 | candidata nova (parado, passadas, preparo, golpe, recuo) | soldados", fill=(230, 220, 200, 255))
    folha.alpha_composite(real, (0, 24))
    d.text((6, real.height + 30), "Os modelos novos ampliados 6x (parado, passadas, preparo, golpe, recuo)", fill=(230, 220, 200, 255))
    folha.alpha_composite(grande, (0, real.height + 54))
    saida.parent.mkdir(parents=True, exist_ok=True)
    folha.convert("RGB").save(saida)
    print(saida)


if __name__ == "__main__":
    main()
