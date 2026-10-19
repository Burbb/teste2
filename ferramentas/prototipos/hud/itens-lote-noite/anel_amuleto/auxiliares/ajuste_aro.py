# A busca do ângulo do anel (rodada 3): o aro como um cilindro curto (o mesmo modelo do aro.py), projetado no quadro
# de 32, comparado com a referência principal (ferramentas/arte/referencias/aneis/sample (2).png reduzida a 32 pela
# maioria em blocos 2x2): a silhueta de fora e o vão (o fundo que aparece pela abertura), medidos pela sobreposição.
# Imprime os melhores parâmetros; quem decide é a comparação lado a lado com a referência.
# Uso: python ajuste_aro.py
import pathlib, sys
import numpy as np
from PIL import Image
from scipy import ndimage

RAIZ = pathlib.Path(__file__).resolve().parents[6]


def referencia():
    a = np.asarray(Image.open(RAIZ / "ferramentas/arte/referencias/aneis/sample (2).png").convert("RGBA"))[:, :, 3] > 128
    a32 = a.reshape(32, 2, 32, 2).mean(axis=(1, 3)) >= 0.5
    lab, n = ndimage.label(~a32)
    borda = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    furo = np.isin(lab, [l for l in range(1, n + 1) if l not in borda])
    return a32 | furo, furo


def projetar(eixo, R, parede, larg, cx, cy, N=32, K=1.0, passo=0.18):
    """As faces visíveis do aro: a matriz de rótulos (0 vazio, 1 fora, 2 dentro, 3 borda) e as normais."""
    eixo = np.asarray(eixo, float); eixo /= np.linalg.norm(eixo)
    u = np.cross(eixo, [0.0, 0.0, 1.0]); u /= np.linalg.norm(u); v = np.cross(eixo, u)
    th = np.arange(0, 2 * np.pi, passo / (R * K))
    t = np.arange(-larg / 2, larg / 2 + 1e-6, passo / K)
    rr = np.arange(R - parede, R + 1e-6, passo / K)
    rad = np.cos(th)[:, None] * u + np.sin(th)[:, None] * v                      # (nθ, 3)
    pts, nor, rot = [], [], []
    for raio, sinal, r_ in ((R, 1, 1), (R - parede, -1, 2)):
        p = raio * rad[:, None, :] + t[None, :, None] * eixo                     # (nθ, nt, 3)
        pts.append(p.reshape(-1, 3)); nor.append(np.repeat(sinal * rad, len(t), axis=0)); rot.append(np.full(p.shape[0] * p.shape[1], r_))
    for lado in (1, -1):
        p = rr[None, :, None] * rad[:, None, :] + lado * larg / 2 * eixo
        pts.append(p.reshape(-1, 3)); nor.append(np.tile(lado * eixo, (p.shape[0] * p.shape[1], 1))); rot.append(np.full(p.shape[0] * p.shape[1], 3))
    P = np.concatenate(pts); Nn = np.concatenate(nor); L = np.concatenate(rot)
    ix = np.floor((cx + P[:, 0]) * K).astype(int); iy = np.floor((cy + P[:, 1]) * K).astype(int)
    ok = (ix >= 0) & (ix < N) & (iy >= 0) & (iy < N)
    ix, iy, z, Nn, L = ix[ok], iy[ok], P[ok, 2], Nn[ok], L[ok]
    ordem = np.argsort(z)                                                         # o mais perto por último: ele fica
    rot_ = np.zeros((N, N), int); nrm = np.zeros((N, N, 3))
    rot_[iy[ordem], ix[ordem]] = L[ordem]; nrm[iy[ordem], ix[ordem]] = Nn[ordem]
    return rot_, nrm


def mascaras(rot_):
    cheio = rot_ > 0
    lab, n = ndimage.label(~cheio)
    borda = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    furo = np.isin(lab, [l for l in range(1, n + 1) if l not in borda])
    return cheio | furo, furo


def iou(a, b):
    return (a & b).sum() / max(1, (a | b).sum())


if __name__ == "__main__":
    rc, rf = referencia()
    ys, xs = np.nonzero(rc); ccx, ccy = xs.mean() + 0.5, ys.mean() + 0.5
    rng = np.random.default_rng(1)
    melhores = []
    for _ in range(int(sys.argv[1]) if len(sys.argv) > 1 else 6000):
        d = rng.normal(size=3); d[2] = abs(d[2]); d /= np.linalg.norm(d)
        R = rng.uniform(11.5, 15.5); larg = rng.uniform(0.25, 0.75) * R; parede = rng.uniform(0.08, 0.2) * R
        rot_, _ = projetar(d, R, parede, larg, ccx, ccy, passo=0.4)
        c, f = mascaras(rot_)
        if c.sum() == 0:
            continue
        nota = iou(c, rc) + 1.5 * iou(f, rf)
        melhores.append((nota, d.round(3).tolist(), round(R, 2), round(parede, 2), round(larg, 2)))
    melhores.sort(reverse=True)
    for m in melhores[:8]:
        print(m)
