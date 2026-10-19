# Os frascos (a família da Poção de Vida; o tônico e o antídoto no lote seguinte): cada um é um perfil de revolução
# (a meia-largura do vidro em cada altura), com o mesmo vidro, a mesma luz (de cima e da esquerda) e o mesmo jeito de
# mostrar o líquido: o nível com a superfície clara, o vidro vazio escuro em cima, a beira clara da espessura do vidro,
# o brilho agrupado em cima à esquerda e um reflexo vertical. Cada variante muda a silhueta, o fechamento e o líquido.
# Uso: python frasco.py <variante> <16|24|32> [silhueta] [<pasta>]. Grava a prévia e as listas em <pasta>/<N>/.
import math, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6] / "ferramentas" / "arte"))
from pixel_comum import grade, contornar, imagem, listas_camadas

VAR = sys.argv[1]; N = int(sys.argv[2]); ETAPA = "silhueta" if "silhueta" in sys.argv[3:] else "final"
SAIDA = pathlib.Path(next((a for a in sys.argv[3:] if a != "silhueta"), "."))
K = N / 32
RAMPAS = {
    "v": ["#1C2028", "#2E3440", "#56606E", "#8C98A8", "#CED8E2", "#F4F8FA"],     # o vidro (do fundo escuro ao brilho)
    "r": ["#360410", "#5E0C18", "#8A1422", "#B41E2C", "#DC3E40", "#FF9C90"],     # o líquido vermelho
    "k": ["#4A2E18", "#6E4826", "#946238", "#B88452"],                           # a cortiça
}
# as variantes: o perfil (lista de trechos de cima para baixo), o nível do líquido, a rampa do líquido e o fechamento
def bola(cy, r, achata=0.9):
    return lambda y: math.sqrt(max(0.0, r * r - (y - cy) ** 2)) if y <= cy + r * achata else 0.0
VARIANTES = {
    "pocao": dict(cx=16.0, partes=[("rolha", 1.6, 5.6, lambda y: 2.8), ("boca", 5.6, 7.4, lambda y: 3.8),
                                   ("gargalo", 7.4, 11.2, lambda y: 2.5), ("corpo", 11.2, 30.4, bola(20.2, 10.2))],
                  nivel=15.8, liquido="r", centro=(16.0, 20.2), raio=10.2),
}
V = VARIANTES[VAR]; CX = V["cx"] * K
mat, tom, fixo, X, Y = grade(N)
cam = np.full((N, N), "", dtype=object)
parte = np.full((N, N), "", dtype=object); meia = np.zeros((N, N))
for nome, y0, y1, w in V["partes"]:
    for y in range(N):
        py = (y + 0.5) / K
        if y0 <= py < y1:
            wy = w(py) * K
            dentro = np.abs(X[y] - CX) <= max(wy, 0.0) if wy > 0 else np.zeros(N, bool)
            novo = dentro & (parte[y] == "")
            parte[y][novo] = nome; meia[y][novo] = wy
# o gargalo e o corpo se juntam: a largura do corpo nunca fica menor que a do gargalo onde eles se encontram
forma = parte != ""
if ETAPA == "silhueta":
    mat[forma] = "v"; tom[forma] = 3; cam[forma] = "vidro"
else:
    cxp, cyp, R = V["centro"][0] * K, V["centro"][1] * K, V["raio"] * K
    nx = np.where(meia > 0, (X - CX) / np.maximum(meia, 0.5), 0)
    ny = np.clip((Y - cyp) / R, -1, 1)
    nz = np.sqrt(np.clip(1 - nx ** 2 - ny ** 2 * 0.6, 0, 1))
    luz = (-0.62 * nx - 0.55 * ny + 0.56 * nz)                     # de cima e da esquerda, um pouco de frente
    nivel = V["nivel"] * K
    vidro = forma & (parte != "rolha")
    liquido = vidro & (parte == "corpo") & (Y >= nivel)
    # a borda de dentro do vidro: o pixel do vidro que encosta no lado de fora (a espessura)
    fora = ~forma
    beira = np.zeros_like(forma)
    for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        beira |= np.roll(np.roll(fora, b, 0), a, 1)
    beira &= vidro
    # o líquido: tons pela luz da forma, a superfície clara no nível, mais fundo embaixo e à direita
    tl = np.where(luz > 0.66, 4, np.where(luz > 0.3, 3, np.where(luz > -0.08, 2, 1)))
    tl = np.where((Y >= nivel) & (Y < nivel + 1), 4, tl)
    tl = np.where(ny > 0.78, np.maximum(tl - 1, 0), tl)
    m = liquido & ~beira
    mat[m] = V["liquido"]; tom[m] = tl[m]; cam[m] = "liquido"
    # o vidro vazio (acima do nível e o gargalo): escuro por dentro, a beira clara do lado da luz
    vazio = vidro & ~liquido & ~beira
    mat[vazio] = "v"; tom[vazio] = np.where(nx[vazio] < -0.3, 3, 2); cam[vazio] = "vidro"
    tb = np.where(nx < -0.1, 4, np.where(nx < 0.5, 3, 2))
    tb = np.where((parte == "boca"), np.where(nx < 0, 4, 3), tb)
    mat[beira] = "v"; tom[beira] = tb[beira]; cam[beira] = "vidro"
    # a beira de baixo do corpo, sob o líquido: o vidro tinge de vermelho escuro (o líquido aparece pela espessura)
    fundo = beira & (parte == "corpo") & (Y >= nivel) & (nx > -0.35)
    mat[fundo] = V["liquido"]; tom[fundo] = np.where(ny[fundo] > 0.5, 1, 2); cam[fundo] = "liquido"
    # a rolha: a cortiça mais clara à esquerda e em cima
    rolha = parte == "rolha"
    tr = np.where(nx < -0.35, 3, np.where(nx < 0.35, 2, 1))
    tr = np.where(Y < (V["partes"][0][1] + 1.0) * K, np.minimum(tr + 1, 3), tr)
    mat[rolha] = "k"; tom[rolha] = tr[rolha]; cam[rolha] = "rolha"
    # o brilho: uma mancha clara em cima à esquerda do corpo e um reflexo vertical do lado da luz
    bx, by = cxp - 0.47 * R, cyp - 0.42 * R
    tam = 2 if N >= 32 else 1
    for (x, y) in [(int(bx), int(by))] + ([(int(bx), int(by) + 1), (int(bx) + 1, int(by))] if tam > 1 else []):
        if forma[y, x]:
            mat[y, x] = "v"; tom[y, x] = 5; cam[y, x] = "brilho"
    xr = int(cxp - 0.72 * R)
    for y in range(int(cyp - 0.05 * R), int(cyp + 0.42 * R) + 1):
        if 0 <= xr < N and forma[y, xr] and not beira[y, xr]:
            mat[y, xr] = "v" if not liquido[y, xr] else V["liquido"]
            tom[y, xr] = 4 if not liquido[y, xr] else 5
            cam[y, xr] = "brilho"
mat[:, -1] = ""; mat[-1, :] = ""; mat[:, 0] = ""; mat[0, :] = ""
contornar(mat)
cam[(mat == "c")] = "contorno"
img = imagem(mat, tom, RAMPAS)
pasta = SAIDA / str(N); pasta.mkdir(parents=True, exist_ok=True)
img.save(pasta / f"{VAR}_{ETAPA}_{N}.png")
if ETAPA == "final":
    listas_camadas((img, cam), pasta, ["vidro", "liquido", "rolha", "brilho", "contorno"])
print("\n".join("".join("#" if mat[y, x] == "c" else (mat[y, x] + str(tom[y, x])) if mat[y, x] else ".." for x in range(N)) for y in range(N)))
