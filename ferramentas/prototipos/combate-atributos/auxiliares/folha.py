"""A folha compacta do protótipo de combate e atributos: as capturas que conferir.mjs grava (capturas/1920-*.png),
reduzidas lado a lado com um rótulo, numa imagem só para ver de relance.

    python ferramentas/prototipos/combate-atributos/auxiliares/folha.py      # grava folha.png na pasta do protótipo
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
PROTO = AQUI.parent
CAPT = PROTO / "capturas"
QUADROS = [("1920-2-ameaca", "1 · O Bote anunciado: alvo, dano previsto, quando resolve"),
           ("1920-3-alvo", "Escolha de alvo (clique ou número; Esc volta)"),
           ("1920-5-esmagador", "2 · O Golpe Esmagador: várias respostas"),
           ("1920-7-terror", "3 · Grito de Terror: A perde a vez (Vontade 3); Odette só abala"),
           ("1920-4-ficha", "Ficha: atributos e o que mudam, com a conta"),
           ("1920-11-comparar", "Comparar A, B, C e a livre"),
           ("1920-8-retorno-antes", "Teste: Pena antes da posição de Morel"),
           ("1920-9-retorno-depois", "Teste: Reerguer depois da posição"),
           ("1920-12-fora-da-luta", "Fora da luta: o companheiro acrescenta")]
COLUNAS, LARGURA, MARGEM, ROTULO = 3, 760, 16, 30


def fonte(t):
    for nome in ("C:/Windows/Fonts/georgia.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"):
        try:
            return ImageFont.truetype(nome, t)
        except OSError:
            pass
    return ImageFont.load_default()


def main():
    ims = [(Image.open(CAPT / f"{n}.png").convert("RGB"), r) for n, r in QUADROS if (CAPT / f"{n}.png").exists()]
    alt = round(LARGURA * ims[0][0].height / ims[0][0].width)
    linhas = (len(ims) + COLUNAS - 1) // COLUNAS
    folha = Image.new("RGB", (COLUNAS * (LARGURA + MARGEM) + MARGEM, 60 + linhas * (alt + ROTULO + MARGEM)), (18, 17, 16))
    d = ImageDraw.Draw(folha)
    d.text((MARGEM, 16), "Protótipo de combate e atributos (nada no jogo) · 1920×945", fill=(242, 201, 76), font=fonte(26))
    for k, (im, rotulo) in enumerate(ims):
        x = MARGEM + (k % COLUNAS) * (LARGURA + MARGEM)
        y = 60 + (k // COLUNAS) * (alt + ROTULO + MARGEM)
        d.text((x, y + 4), rotulo, fill=(232, 220, 190), font=fonte(18))
        folha.paste(im.resize((LARGURA, alt), Image.LANCZOS), (x, y + ROTULO))
    folha.save(PROTO / "folha.png", optimize=True)
    print(PROTO / "folha.png", folha.size)


if __name__ == "__main__":
    main()
