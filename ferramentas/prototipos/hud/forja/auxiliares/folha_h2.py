"""A folha do ajuste do rosto (H para H2): o olho um pixel mais para trás, com a órbita mais escura entre a ponte do nariz e
o olho. Antes e depois nas poses do alto, do golpe e do rebote, no tamanho do jogo a 1920 (3×) e ampliado (8×), e a
cena inteira no jogo (fotografar.mjs com VERSOES=h,h2). Grava ../folha-rosto-h2.png.

    python ferramentas/prototipos/hud/forja/auxiliares/folha_h2.py
"""
import pathlib

from PIL import Image

from folha_f import montar
from folha_g import CAP, modulo, q_de, rotulo

AQUI = pathlib.Path(__file__).resolve().parent
Ch, Ch2 = modulo("h", "cena"), modulo("h2", "cena")


def main():
    linhas = []
    for nome, rot in [("alto", "no alto"), ("golpe", "no golpe"), ("volta", "no rebote (a recuperação)")]:
        ims = []
        for C, v in ((Ch, "H"), (Ch2, "H2")):
            im = C.quadro(q_de(C, nome), com_faiscas=False).imagem().convert("RGB")
            ims.append((rotulo(im.crop((146, 22, 190, 58)).resize((132, 108), Image.NEAREST), v), ""))
            ims.append((rotulo(im.crop((154, 26, 178, 46)).resize((192, 160), Image.NEAREST), v + " 8×"), ""))
        linhas.append((f"{rot}: antes (H) e depois (H2), no tamanho do jogo a 1920 (3×) e a 8×", ims))
    no_jogo = [(Image.open(CAP / f"1920-{v}-forja.png").convert("RGB").crop((850, 220, 1110, 440)), v.upper()) for v in ("h", "h2")]
    linhas.append(("no jogo, a 1920 (a captura da tela, sem ampliar; um quadro qualquer do ciclo)", no_jogo))
    montar("O rosto do ferreiro, H para H2: o olho um pixel mais para trás, a órbita entre a ponte do nariz e o olho, a "
           "sobrancelha logo acima (o resto igual)", linhas, AQUI.parent / "folha-rosto-h2.png")


if __name__ == "__main__":
    main()
