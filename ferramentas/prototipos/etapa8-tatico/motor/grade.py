"""A geometria da arena do protótipo tático (nada no jogo): casas, distância, linha de visão, caminhos e áreas.

Regras provisórias (seção 4 do roadmapIDEIAS/29-ETAPA8-COMBATE-TATICO.md):
- **Casas quadradas, movimento só nas quatro direções** (sem diagonal). Distância = soma das diferenças de coluna e
  linha (casas a percorrer sem obstáculos); por isso o alcance desenha um losango, como em Dofus.
- **Rocha** bloqueia passagem e visão; **água funda** bloqueia passagem e deixa ver através.
- **Linha de visão:** o segmento entre os centros das duas casas. Ela é bloqueada por uma rocha ou por uma unidade em
  qualquer casa que o segmento atravesse (fora a de origem e a do alvo). Quando o segmento passa exatamente por um canto,
  só bloqueia se as duas casas do canto bloquearem.
- **Caminhos:** cada passo custa 1; sair de uma casa vizinha a um inimigo custa 1 a mais (zona de controle, quando
  ligada). Atravessa-se aliados, não inimigos; não se termina numa casa ocupada."""
from heapq import heappop, heappush

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
DIRS8 = DIRS + ((1, 1), (1, -1), (-1, 1), (-1, -1))


def distancia(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def alinhado(a, b):
    return a != b and (a[0] == b[0] or a[1] == b[1])


def direcao(a, b):
    """A direção (passo unitário nas quatro direções) de a para b; em diagonal, a do eixo maior."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    if abs(dx) >= abs(dy) and dx:
        return (1 if dx > 0 else -1, 0)
    if dy:
        return (0, 1 if dy > 0 else -1)
    return (0, 0)


def atravessadas(a, b):
    """As casas que o segmento entre os centros de a e b atravessa, sem a e b. Um canto exato aparece como um par
    ("canto", c1, c2)."""
    x0, y0 = a
    x1, y1 = b
    nx, ny = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x1 > x0 else -1
    sy = 1 if y1 > y0 else -1
    x, y, ix, iy = x0, y0, 0, 0
    out = []
    while ix < nx or iy < ny:
        t = (1 + 2 * ix) * ny - (1 + 2 * iy) * nx
        if t == 0:
            out.append(("canto", (x + sx, y), (x, y + sy)))
            x, y, ix, iy = x + sx, y + sy, ix + 1, iy + 1
        elif t < 0:
            x, ix = x + sx, ix + 1
        else:
            y, iy = y + sy, iy + 1
        out.append((x, y))
    if out and out[-1] == (x1, y1):
        out.pop()
    return out


class Arena:
    def __init__(self, largura, altura, rochas=(), agua=()):
        self.largura, self.altura = largura, altura
        self.rochas = set(map(tuple, rochas))
        self.agua = set(map(tuple, agua))

    def dentro(self, c):
        return 0 <= c[0] < self.largura and 0 <= c[1] < self.altura

    def chao(self, c):
        """Casa onde se pode estar (dentro, sem rocha nem água)."""
        return self.dentro(c) and c not in self.rochas and c not in self.agua

    def vizinhas(self, c, oito=False):
        return [(c[0] + dx, c[1] + dy) for dx, dy in (DIRS8 if oito else DIRS) if self.dentro((c[0] + dx, c[1] + dy))]

    def visao(self, a, b, ocupadas):
        """Se a vê b. `ocupadas`: as casas com unidades (bloqueiam a visão no meio do caminho)."""
        def bloqueia(c):
            return c in self.rochas or c in ocupadas
        for passo in atravessadas(a, b):
            if passo[0] == "canto":
                if bloqueia(passo[1]) and bloqueia(passo[2]):
                    return False
            elif bloqueia(passo):
                return False
        return True

    def caminhos(self, origem, pm, ocupantes, lado, saida=None, evitar=None):
        """Dijkstra a partir de `origem`. `ocupantes`: {casa: lado}. Devolve {casa: (custo real, anterior)} das casas
        alcançáveis com até `pm` (pm=None: sem limite), contando também as ocupadas por aliados (atravessáveis), que a
        tela e a IA filtram ao escolher onde parar. `saida(casa)`: o custo a mais para sair da casa (a zona de
        controle). `evitar(casa)`: um custo de preferência (a IA foge do fogo), que ordena os caminhos sem mudar o
        custo real."""
        inimigos = {c for c, l in ocupantes.items() if l != lado}
        def custo_saida(c):
            return saida(c) if saida else 0
        melhor = {origem: (0, 0, None)}
        fila = [(0, 0, origem)]
        while fila:
            pref, real, c = heappop(fila)
            if melhor[c][:2] != (pref, real):
                continue
            extra = custo_saida(c)
            for v in self.vizinhas(c):
                if not self.chao(v) or v in inimigos:
                    continue
                r = real + 1 + extra
                if pm is not None and r > pm:
                    continue
                p = pref + 1 + extra + (evitar(v) if evitar else 0)
                atual = melhor.get(v)
                if atual is None or p < atual[0] or (p == atual[0] and r < atual[1]):
                    melhor[v] = (p, r, c)
                    heappush(fila, (p, r, v))
        return {c: (r, ant) for c, (p, r, ant) in melhor.items()}

    @staticmethod
    def rota(tabela, destino):
        out = []
        c = destino
        while c is not None:
            out.append(c)
            c = tabela[c][1]
        return out[::-1]

    # ------------------------------------------------------------ áreas
    def cruz(self, centro, raio=1):
        return [(x, y) for x in range(centro[0] - raio, centro[0] + raio + 1)
                for y in range(centro[1] - raio, centro[1] + raio + 1)
                if distancia((x, y), centro) <= raio and self.dentro((x, y))]

    def linha_perpendicular(self, origem, centro, tamanho=3):
        """Uma linha de `tamanho` casas centrada em `centro`, perpendicular à direção de origem para centro."""
        d = direcao(origem, centro)
        p = (d[1], d[0]) if d != (0, 0) else (1, 0)
        meio = tamanho // 2
        return [c for c in ((centro[0] + p[0] * k, centro[1] + p[1] * k) for k in range(-meio, tamanho - meio))
                if self.dentro(c)]
