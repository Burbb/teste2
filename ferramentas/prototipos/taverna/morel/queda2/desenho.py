"""O desenho dos volumes da queda de braço na vista de detalhe (protótipo): a profundidade por pixel.

Cada volume (o braço em cápsula, o tampo, uma face do tronco) é projetado pela câmera de `juntas.py`; cada pixel fica
com a superfície mais perto da câmera e vai para a camada dela. Assim as camadas da fonte não se sobrepõem e a ordem
delas não decide quem passa na frente: decide a profundidade, pose a pose (o nosso antebraço na frente do dele na
disputa; o braço de quem vence por cima da mão de quem perde nos fins).

As cores saem de uma função de quem desenha (`cor(normal, t, ponto)`): no estudo, cores lisas por parte; no
acabamento, o tom do material pela luz (`tom`). Nada disso é a arte: o estudo confere a construção, e o acabamento é
revisto no tamanho real e retocado à mão onde a fórmula não basta."""
import math

import juntas as J

W, H = 320, 96
# a luz da cena: a vela (do nosso lado, a oeste) e a lareira (a oeste, longe): da esquerda e da frente, um pouco de cima
LUZ = J._un((-0.55, 0.5, -0.67))


class Tela:
    def __init__(self):
        self.prof = {}    # (x, y) -> a profundidade da superfície que ficou
        self.cor = {}     # (x, y) -> (r, g, b, a)
        self.camada = {}  # (x, y) -> o nome da camada

    def ponto(self, x, y, z, cor, camada):
        if not (0 <= x < W and 0 <= y < H):
            return
        q = (x, y)
        if z < self.prof.get(q, 1e9):
            self.prof[q], self.cor[q], self.camada[q] = z, cor, camada

    def camadas(self):
        out = {}
        for q, c in self.camada.items():
            out.setdefault(c, {})[q] = self.cor[q]
        return out


def _raio(px, py):
    """A direção do raio da câmera pelo meio do pixel (px, py)."""
    D0, D1 = J._DESLOCA
    return J._un(J._add(J._mul(J._FRENTE, J.FOCO), J._add(J._mul(J._DIREITA, px + 0.5 - D0),
                                                         J._mul(J._CIMA, -(py + 0.5 - D1)))))


def capsula(tela, camada, a, b, ra, rb, cor, passo=0.35):
    """Uma cápsula de a a b (cm), raio de ra a rb: esferas ao longo do eixo, cada pixel com a normal da esfera."""
    L = math.dist(a, b)
    n = max(1, int(L / passo))
    for k in range(n + 1):
        t = k / n
        c = J._add(a, J._mul(J._sub(b, a), t))
        r = ra + (rb - ra) * t
        sx, sy, z = J.tela(c)
        pr = r * J.FOCO / z
        for y in range(math.floor(sy - pr) - 1, math.ceil(sy + pr) + 2):
            for x in range(math.floor(sx - pr) - 1, math.ceil(sx + pr) + 2):
                dx, dy = (x + 0.5 - sx) / pr, (y + 0.5 - sy) / pr
                d2 = dx * dx + dy * dy
                if d2 > 1:
                    continue
                dz = math.sqrt(1 - d2)
                # a normal no espaço: para a direita e para cima da tela, e de volta para a câmera
                normal = J._un(J._add(J._mul(J._DIREITA, dx), J._add(J._mul(J._CIMA, -dy), J._mul(J._FRENTE, -dz))))
                tela.ponto(x, y, z - r * dz, cor(normal, t, c), camada)


def elipsoide(tela, camada, centro, eixos, semi, cor):
    """Um elipsoide (o peito, um punho): `eixos` três direções ortogonais, `semi` os semieixos (cm). Cada pixel pelo
    raio da câmera que o atravessa; a cor por `cor(normal, local)`, com `local` nas coordenadas do elipsoide (-1 a 1)."""
    cam = J.CAMERA
    R = max(semi)
    sx, sy, z = J.tela(centro)
    pr = R * J.FOCO / max(z - R, 1.0)
    oc = J._sub(cam, centro)
    o = [J._dot(oc, e) / s for e, s in zip(eixos, semi)]
    for py in range(max(0, math.floor(sy - pr) - 1), min(H, math.ceil(sy + pr) + 2)):
        for px in range(max(0, math.floor(sx - pr) - 1), min(W, math.ceil(sx + pr) + 2)):
            dw = _raio(px, py)
            d = [J._dot(dw, e) / s for e, s in zip(eixos, semi)]
            a = sum(v * v for v in d)
            b = 2 * sum(u * v for u, v in zip(o, d))
            c = sum(u * u for u in o) - 1
            disc = b * b - 4 * a * c
            if disc < 0:
                continue
            s = (-b - math.sqrt(disc)) / (2 * a)
            if s <= 0:
                continue
            local = [u + v * s for u, v in zip(o, d)]
            normal = J._un(J._add(J._add(J._mul(eixos[0], local[0] / semi[0]), J._mul(eixos[1], local[1] / semi[1])),
                                  J._mul(eixos[2], local[2] / semi[2])))
            p = J._add(cam, J._mul(dw, s))
            tela.ponto(px, py, J._dot(J._sub(p, cam), J._FRENTE), cor(normal, local), camada)


def plano_y(tela, camada, y0, dentro, cor):
    """Um plano horizontal (y = y0, cm) onde `dentro(x, z)`; a cor por `cor(x, z)`."""
    cam = J.CAMERA
    for py in range(H):
        for px in range(W):
            d = _raio(px, py)
            if abs(d[1]) < 1e-6:
                continue
            s = (y0 - cam[1]) / d[1]
            if s <= 0:
                continue
            p = J._add(cam, J._mul(d, s))
            if dentro(p[0], p[2]):
                tela.ponto(px, py, J._dot(J._sub(p, cam), J._FRENTE), cor(p[0], p[2]), camada)


def plano_x(tela, camada, x0, dentro, cor):
    """Um plano vertical de leste a oeste fixo (x = x0): a ponta da mesa, por exemplo."""
    cam = J.CAMERA
    for py in range(H):
        for px in range(W):
            d = _raio(px, py)
            if abs(d[0]) < 1e-6:
                continue
            s = (x0 - cam[0]) / d[0]
            if s <= 0:
                continue
            p = J._add(cam, J._mul(d, s))
            if dentro(p[1], p[2]):
                tela.ponto(px, py, J._dot(J._sub(p, cam), J._FRENTE), cor(p[1], p[2]), camada)


def plano_z(tela, camada, z0, dentro, cor):
    """Um plano vertical de norte a sul fixo (z = z0): o balcão ao fundo, a frente do tronco."""
    cam = J.CAMERA
    for py in range(H):
        for px in range(W):
            d = _raio(px, py)
            if abs(d[2]) < 1e-6:
                continue
            s = (z0 - cam[2]) / d[2]
            if s <= 0:
                continue
            p = J._add(cam, J._mul(d, s))
            if dentro(p[0], p[1]):
                tela.ponto(px, py, J._dot(J._sub(p, cam), J._FRENTE), cor(p[0], p[1]), camada)


def cotovelo(ombro, pulso, polo, braco, antebraco):
    """Cinemática inversa de dois ossos: o cotovelo dobrando para `polo`."""
    d = J._sub(pulso, ombro)
    dist = min(J._norma(d), braco + antebraco - 0.01)
    u = J._un(d)
    a = (braco ** 2 - antebraco ** 2 + dist ** 2) / (2 * dist)
    h = math.sqrt(max(braco ** 2 - a * a, 0))
    lado = J._un(J._sub(polo, J._mul(u, J._dot(polo, u))))
    return J._add(J._add(ombro, J._mul(u, a)), J._mul(lado, h))


def luz(normal):
    """O quanto a superfície encara a luz (-1 a 1)."""
    return J._dot(normal, LUZ)
