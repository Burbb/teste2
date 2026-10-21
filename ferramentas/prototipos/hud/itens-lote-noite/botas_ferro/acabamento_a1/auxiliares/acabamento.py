"""A1, o teste de um acabamento mais contido nas botas B3 (20/10/2026, pedido do Jean), sobre uma cópia da fonte final
(ferramentas/arte/aseprite/botas-ferro/botas-ferro-32.aseprite, em fontes/A1/A1-32.aseprite). A forma da B3 continua: a
silhueta, a pose, o tamanho, a sobreposição do par, as placas, as tiras, as fivelas, as solas e o contorno; só os tons do
aço mudam, e nenhum pixel muda de camada.
A referência de acabamento (ferramentas/arte/referencias/botas/Botas de ferro em pixel art.png) orienta só a paleta, os
reflexos e a divisão dos planos: o aço dela fica no tom médio (o 5 é o mais comum, 3 e 4 nas sombras, poucos 7 e 8),
enquanto a B3 se divide entre muito escuro e muito claro, o que dá a aparência polida e arredondada. As regras, nesta
ordem, cada uma com o porquê:
  1. o quase branco (8) sai: na beira da placa vira o aço claro do conjunto (7); dentro, o 6;
  2. o 7 fica só como brilho curto na beira de uma placa (encostado no contorno, no vão, no couro ou numa junta escura);
     dentro da placa vira 6 (as manchas grandes de brilho são o que arredonda e pule a placa); e curto: numa fileira de
     7 seguidos na beira, ficam os 2 da esquerda (de onde vem a luz), os outros viram 6 (a faixa contínua lia como aro
     polido);
  3. o 6 de dentro da placa desce para 5: com o 7 virando 6, a face acesa e a vizinha ficavam no mesmo tom e o cano
     perdia a divisão dos planos; assim a face acesa (6) continua separada da do lado (5), como na referência;
  4. a sombra de dentro da placa (o 3 que não encosta numa junta, no contorno, no vão nem no couro) sobe para 4, para o
     corpo da placa ficar no tom médio sem escurecer a peça; as juntas (o 2 e o 1) e as sombras de sobreposição (o 3 junto
     de uma junta) ficam.
Depois, os AJUSTES à mão (o que as regras não resolvem bem), cada um com o porquê. Grava grades/A1.txt e
listas/acabamento/aco.lua para o pintar.lua.
    python acabamento.py <pasta da A1>
O 40 e o 48 (o 32 aprovado no 945a54a8): as mesmas regras sobre as grades de 40 e 48 da B3 do jogo (grades/B3-jogo-N.txt,
conferidas iguais aos PNGs do jogo), sem mudar a forma; só o comprimento do brilho curto acompanha a escala (2 px no 32 e
no 40, 3 no 48). Grava grades/A1-N.txt e listas/acabamento-N/aco.lua.
    python acabamento.py <pasta da A1> 40|48
"""
import pathlib
import sys

FERRO = ["0e0f11", "1a1c20", "282b31", "383c44", "4c5159", "646a73", "848b94", "b0b6bd", "e4e8ec"]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 32
CURTO = {32: 2, 40: 2, 48: 3}[N]   # o brilho curto: quantos 7 seguidos ficam na fileira
AJUSTES = {}   # (x, y): (o tom novo, o porquê)


def borda(g, x, y):
    """O pixel encosta (pelos lados) no contorno, no fundo, no vão escuro, no couro ou numa junta escura (o 2 ou o 1)?"""
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        X, Y = x + dx, y + dy
        c = g[Y][X] if 0 <= X < N and 0 <= Y < N else "."
        if not c.isdigit() or c in "012": return True
    return False


def junta(g, x, y):
    return any(0 <= x + dx < N and 0 <= y + dy < N and g[y + dy][x + dx] in "012"
               for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


def acabar(g):
    out = [l[:] for l in g]
    for y in range(N):
        for x in range(N):
            c = g[y][x]
            if not c.isdigit(): continue
            novo = c
            if c == "8": novo = "7" if borda(g, x, y) else "6"
            elif c == "7" and not borda(g, x, y): novo = "6"
            elif c == "6" and not borda(g, x, y): novo = "5"
            elif c == "3" and not borda(g, x, y) and not junta(g, x, y): novo = "4"
            out[y][x] = novo
    for y in range(N):                       # o brilho curto: no máximo CURTO px de 7 seguidos na fileira
        corrida = 0
        for x in range(N):
            corrida = corrida + 1 if out[y][x] == "7" else 0
            if corrida > CURTO: out[y][x] = "6"
    for (x, y), (t, _) in AJUSTES.items(): out[y][x] = t
    mudou = [(x, y, g[y][x], out[y][x]) for y in range(N) for x in range(N) if out[y][x] != g[y][x]]
    return out, mudou


if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    sufixo = "" if N == 32 else f"-{N}"
    g = [list(l) for l in (base / f"grades/B3-jogo{sufixo}.txt").read_text(encoding="utf-8").split("\n")[:N]]
    out, mudou = acabar(g)
    (base / f"grades/A1{sufixo}.txt").write_text("\n".join("".join(l) for l in out) + "\n", encoding="utf-8")
    d = base / f"listas/acabamento{sufixo}"; d.mkdir(parents=True, exist_ok=True)
    (d / "aco.lua").write_text('return "' + ";".join(f"{x},{y},{FERRO[int(n)]}" for x, y, _, n in mudou) + '"\n',
                               encoding="utf-8")
    from collections import Counter
    print(len(mudou), "pixels;", dict(Counter(f"{a}>{n}" for _, _, a, n in mudou)))
    print("\n".join(f"{y:2d} {''.join(l)}" for y, l in enumerate(out)))
