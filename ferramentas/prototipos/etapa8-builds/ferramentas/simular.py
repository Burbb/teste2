"""Um jogador automático simples (aleatório com bom senso) para conferir o motor do X1: nenhuma luta trava, as cadeias
terminam e a duração das lutas fica num intervalo jogável. Não mede qualidade de build (quem joga é o Jean).

    python ferramentas/simular.py [partidas por par]"""
import random
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from motor import conteudo as C  # noqa: E402
from motor import montagem as M  # noqa: E402
from motor.combate import Combate  # noqa: E402


def escolher(cb, rng):
    c = cb.c[cb.aguardando]
    acoes = [a for a in cb.acoes() if a["disponivel"]]
    feridos = [x for x in cb.vivos("aliado") if x.vida < x.vida_max * 0.5]
    if c.id == "odete":
        if feridos and any(a["id"] == "prece" for a in acoes):
            return "prece", min(feridos, key=lambda x: x.vida).id
        a = rng.choice([a for a in acoes if a["id"] in ("bastao", "bencao")])
    elif c.id == "morel":
        a = rng.choice([a for a in acoes if a["id"] in ("atacar", "oportuno")])
    else:
        if cb.pode_sair_furia() and not cb.motivo_sair_furia() and c.vida < c.vida_max * 0.4:
            cb.sair_furia()
        uteis = [a for a in acoes if a["id"] != "defender"]
        a = rng.choice(uteis)
    alvos = a["alvos"]
    if a["alvo"] == "inimigo":  # não sacrifica as próprias invocações por acaso
        alvos = [x for x in alvos if cb.c[x].lado == "inimigo"] or alvos
    alvo = rng.choice(alvos) if a["alvo"] in ("inimigo", "aliado", "aliado_outro") else None
    return a["id"], alvo


def partida(m, enc, semente, rng):
    cb = Combate(m, enc, semente)
    while not cb.fim:
        acao, alvo = escolher(cb, rng)
        r = cb.agir(acao, alvo)
        assert r["ok"], r
    return cb


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    print(f"{'build':22} " + " ".join(f"{e:>19}" for e in C.ENCONTROS if not e.startswith("_")))
    for ex in C.EXEMPLOS:
        m = M.de_exemplo(ex["id"])
        linha = []
        for enc in [e for e in C.ENCONTROS if not e.startswith("_")]:
            v, rod, elos, sobra = 0, 0, 0, 0
            for s in range(n):
                cb = partida(m, enc, 1000 + s, random.Random(s))
                v += cb.fim == "vitoria"
                rod += cb.rodada
                sobra += sum(x.vida for x in cb.c.values() if x.lado == "aliado") / sum(
                    x.vida_max for x in cb.c.values() if x.lado == "aliado")
                elos = max(elos, max(x["elos"] for x in cb.cadeias))
            linha.append(f"{100 * v // n:3}% r{rod / n:4.1f} v{100 * sobra / n:3.0f}% e{elos:<2}")
        print(f"{ex['nome']:22} " + " ".join(f"{x:>19}" for x in linha))


if __name__ == "__main__":
    main()
