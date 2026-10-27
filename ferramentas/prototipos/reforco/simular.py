"""A progressão do reforço até +12 (12ª versão do protótipo): simula o caminho de +0 até +8, +10 e +12, com as quedas
e a recuperação dos níveis perdidos, e mostra o ganho em peças reais do gerador.

    python ferramentas/prototipos/reforco/simular.py            # a curva atual (regras.py)
    python ferramentas/prototipos/reforco/simular.py --dura     # a alternativa mais dura, para comparar

Cada caminho tem um orçamento de tentativas (ORCAMENTO): quem não chega dentro dele é contado à parte, e os percentis
dizem só de quem chegou, com a fração que não chegou ao lado (nada de simulação cortada como se todos tivessem
terminado). Preços sem a reputação.
"""

import os
import random
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import regras as R  # noqa: E402

RARIDADES = ("comum", "magico", "raro", "lendario")
NOMES_RAR = {"comum": "Comum", "magico": "Incomum", "raro": "Raro", "lendario": "Lendário"}
ALVOS = (8, 10, 12)
ORCAMENTO = 20000  # tentativas por caminho
CAMINHOS = 4000


def chances(rar, dura=False):
    if not dura:
        return {k: R.chance({"raridade": rar}, k) for k in range(1, R.LIMITE + 1)}
    alto = {5: 50, 6: 47, 7: 44, 8: 41, 9: 38, 10: 35, 11: 32, 12: 30}  # a alternativa: a pena inteira (4/8/12)
    return {k: (R.chance({"raridade": rar}, k) if k <= 4 else alto[k] - R.PENA_RARIDADE[rar]) for k in range(1, R.LIMITE + 1)}


def caminho(rng, ch, alvo):
    """Tenta de +0 até `alvo`: (tentativas, ouro, fragmentos, quedas), ou None se o orçamento acabou antes."""
    n = tent = ouro = frag = quedas = 0
    while n < alvo:
        if tent >= ORCAMENTO:
            return None
        tent += 1
        ouro += R.OURO[n]
        frag += R.FRAGMENTOS[n]
        if rng.random() * 100 < ch[n + 1]:
            n += 1
        else:
            n = max(0, n - 1)
            quedas += 1
    return tent, ouro, frag, quedas


def esperado(ch, alvo):
    """A média exata de tentativas de +0 até `alvo` (a cadeia: subir de k-1 para k custa (1 + (1-p) E[k-1]) / p)."""
    e, total = 0.0, 0.0
    for k in range(1, alvo + 1):
        p = ch[k] / 100
        e = (1 + (1 - p) * (e if k > 1 else 0)) / p
        total += e
    return total


def pct(v, q):
    return v[min(len(v) - 1, int(q * len(v)))]


def fmt(x):
    return f"{x:,.0f}".replace(",", ".")


def tabela(dura=False):
    rng = random.Random(12)
    print(f"Chances do +5 ao +12 ({'alternativa dura' if dura else 'curva atual'}):")
    for rar in RARIDADES:
        ch = chances(rar, dura)
        print(f"  {NOMES_RAR[rar]:9} " + " ".join(f"+{k}:{ch[k]}%" for k in range(5, R.LIMITE + 1)))
    print(f"\n{CAMINHOS} caminhos por raridade, até {fmt(ORCAMENTO)} tentativas cada; mediana · 90% · 99% de quem chegou\n")
    print("| Raridade | Alvo | Média exata | Tentativas | Ouro | Fragmentos | Quedas | Não chegou |")
    print("|---|---|---|---|---|---|---|---|")
    for rar in RARIDADES:
        ch = chances(rar, dura)
        for alvo in ALVOS:
            res = [caminho(rng, ch, alvo) for _ in range(CAMINHOS)]
            ok = [r for r in res if r]
            col = [sorted(r[i] for r in ok) for i in range(4)]
            fora = len(res) - len(ok)
            cel = [" · ".join(fmt(pct(c, q)) for q in (0.5, 0.9, 0.99)) if c else "—" for c in col]
            print(f"| {NOMES_RAR[rar]} | +{alvo} | {fmt(esperado(ch, alvo))} | {cel[0]} | {cel[1]} | {cel[2]} | {cel[3]} | "
                  f"{fora} de {CAMINHOS} ({100 * fora / CAMINHOS:.1f}%) |")
    print("\nCaminho feliz (um passo de cada, sem falhar): " + "; ".join(
        f"+{a}: {fmt(R.nominal(a)[0])} de ouro e {R.nominal(a)[1]} fragmentos" for a in ALVOS))


def ganhos():
    """O ganho em peças reais do gerador, do +1 ao +12, e uma base comum nova mais adiante, para comparar."""
    from rpg import itens
    rng = random.Random(3)
    exemplos = [("guerreiro", "arma", 1, "comum"), ("guerreiro", "arma", 6, "comum"), ("guerreiro", "arma", 12, "raro"),
                ("mago", "arma", 6, "magico"), ("guerreiro", "armadura", 1, "comum"), ("guerreiro", "armadura", 6, "raro"),
                ("guerreiro", "secundaria", 3, "comum"), ("mago", "secundaria", 6, "magico")]
    print("\n| Peça | Base | +4 | +8 | +12 | Base comum nova do gerador, nível +6 / +12 |")
    print("|---|---|---|---|---|---|")
    for classe, slot, nivel, rar in exemplos:
        it = itens.gerar_equip(rng, classe, nivel, slot=slot, raridade=rar)
        ls = [s for s, _, _ in R.linhas(it)]
        base = it.get("bonus_base") or it["bonus"]
        b = lambda x: "/".join(str(x.get(s, 0)) for s in ls)  # noqa: E731
        com = lambda n: "/".join(str(base.get(s, 0) + R.ganho_total(it, n)[s]) for s in ls)  # noqa: E731
        novas = []
        for mais in (6, 12):  # o que o gerador dá mais adiante (o material sobe com o nível)
            o = itens.gerar_equip(random.Random(7), classe, nivel + mais, slot=slot, raridade="comum")
            novas.append(f"{o['nome']}: {b(o['bonus'])}")
        nomes = "/".join(R.NOMES.get(s, s) for s in ls)
        print(f"| {it['nome']} (nível {nivel}, {NOMES_RAR[rar].lower()}) | {nomes} {b(base)} | {com(4)} | {com(8)} | {com(12)} | {'; '.join(novas)} |")


if __name__ == "__main__":
    tabela("--dura" in sys.argv)
    if "--dura" not in sys.argv:
        ganhos()
