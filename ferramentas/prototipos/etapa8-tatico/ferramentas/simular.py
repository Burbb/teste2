"""Jogadores automáticos do protótipo tático, para conferir o motor e investigar a fuga repetida. Não medem a graça
do combate (quem joga é o Jean).

- "luta": escolhe, entre todas as casas alcançáveis e todas as ações, a que mais rende agora (dano, abates, cura),
  descontando o fogo amigo e as casas perigosas (marcadas por um golpe preparado, em chamas, e, para os frágeis,
  vizinhas de inimigos); anda até lá, age e encerra.
- "recuo": a mesma escolha, mas só aceita casas a 3 ou mais do inimigo mais perto quando pode, e depois da ação gasta
  o resto dos PM se afastando. É a verificação "dá para vencer sempre recuando e atacando?".

Cada tabela sai em três variantes de regra: zona de controle ligada ou desligada, e andar depois de agir ou não.

    python ferramentas/simular.py [partidas] [estratégias...]"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from motor import conteudo as C  # noqa: E402
from motor.combate import Combate  # noqa: E402
from motor.grade import distancia  # noqa: E402

VARIANTES = [(1, True), (0, True), (1, False)]


def _valor(cb, un, hid, casa):
    p = cb.previa(un, hid, casa)
    v = 0.0
    for uid, d in p["dano"].items():
        alvo = cb.u[uid]
        if alvo.lado == un.lado:
            v -= 1.5 * d
        else:
            v += d + (25 if d >= alvo.vida else 0)
    if hid == "prece":
        alvo = cb.em(casa)
        falta = alvo.vida_max - alvo.vida
        v += min(18, falta) * (2 if alvo.vida < alvo.vida_max * 0.5 else 0.5)
    if hid == "bencao":
        v += 4
    if hid in ("muralha_fogo", "sentinela", "guarda_costas", "proteger"):
        perto = [e for e in cb.vivos("inimigo") if distancia(e.pos, casa) <= 2]
        v += 6 * len(perto)
    if hid == "defender":
        v += 2
    if hid in ("golpe_escudo", "corrente", "explosao_calor"):
        v += 3
    if hid == "combustao":
        alvo = cb.em(casa)
        if not (alvo.queima or {}).get("camadas"):
            v -= 10
    return v - 0.02 * cb.custo_hab(un, hid)


def jogar_vez(cb, estrategia):
    un = cb.u[cb.aguardando]
    origem = un.pos
    mov = cb.movimentos(un)
    casas = [origem] + list(mov)
    inimigos = cb.vivos("inimigo")

    def longe(c):
        return min(distancia(c, e.pos) for e in inimigos) if inimigos else 9
    if estrategia == "recuo":
        casas = [c for c in casas if longe(c) >= 3] or casas
    perigo = set(cb.chamas) | {p for e in inimigos for p in (e.prep or {}).get("casas", [])}
    fragil = un.id == "odete" or (un.id == "heroi" and cb.spec == "piromante")

    def risco(c):
        return (30 if c in perigo else 0) + (6 * sum(1 for e in inimigos if distancia(e.pos, c) == 1) if fragil else 0)
    melhor = None
    for c in casas:
        un.pos = c
        for hid in un.kit:
            if cb.motivo(un, hid):
                continue
            for alvo in cb.alvos_validos(un, hid):
                v = _valor(cb, un, hid, alvo) - 0.01 * (mov[c]["custo"] if c in mov else 0) - risco(c)
                if estrategia == "recuo":
                    v += 0.5 * longe(c)
                if melhor is None or v > melhor[0]:
                    melhor = (v, c, hid, alvo)
    un.pos = origem
    if melhor:
        _, c, hid, alvo = melhor
        if c != origem:
            cb.mover(c)
        if not cb.fim and cb.aguardando == un.id:
            cb.agir(hid, alvo)
    if not cb.fim and cb.aguardando == un.id and inimigos and un.pm:
        mov = cb.movimentos(un)
        if estrategia == "recuo" and mov:
            c = max(mov, key=lambda c: (longe(c), -mov[c]["custo"]))
            if longe(c) > longe(un.pos):
                cb.mover(c)
        elif un.pos in perigo and mov:
            seguras = [c for c in mov if c not in perigo]
            if seguras:
                cb.mover(min(seguras, key=lambda c: mov[c]["custo"]))
    if not cb.fim and cb.aguardando == un.id:
        cb.encerrar()


def partida(spec, enc, semente, estrategia="luta", zona=None, talentos=(), mover_depois=None):
    cb = Combate(spec, enc, talentos, semente, zona, mover_depois=mover_depois)
    while not cb.fim:
        jogar_vez(cb, estrategia)
    return cb


def tabela(n, estrategia, zona=None, mover_depois=None):
    linhas = []
    for spec in C.HEROI:
        for enc in C.ENCONTROS:
            v = rod = vida = cmds = parado = sem = vezes = 0
            for s in range(n):
                cb = partida(spec, enc, 1000 + s, estrategia, zona, mover_depois=mover_depois)
                v += cb.fim == "vitoria"
                rod += cb.rodada
                g = [x for x in cb.u.values() if x.lado == "aliado" and not x.invocacao]
                vida += sum(x.vida for x in g) / sum(x.vida_max for x in g)
                cmds += cb.resumo()["comandos_por_vez"]
                parado += cb.m["inimigo_parado"]
                sem += cb.m["inimigo_sem_acao"]
                vezes += cb.m["vezes_inimigo"]
            linhas.append((spec, enc, 100 * v // n, rod / n, 100 * vida / n, cmds / n, 100 * sem / max(1, vezes),
                           100 * parado / max(1, vezes)))
    return linhas


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    estrategias = sys.argv[2:] or ["luta", "recuo"]
    for est in estrategias:
        for zona, depois in VARIANTES:
            print(f"\n== {est}, zona de controle {'ligada' if zona else 'desligada'}, "
                  f"{'anda depois de agir' if depois else 'agir encerra o movimento'} ({n} lutas por linha)")
            print(f"{'build':10} {'encontro':12} {'vitórias':>8} {'rodadas':>8} {'vida':>6} {'cmd/vez':>8} "
                  f"{'ini. sem ação':>13} {'ini. parado':>11}")
            for spec, enc, v, r, vida, cmds, sem, parado in tabela(n, est, zona, depois):
                print(f"{spec:10} {enc:12} {v:7}% {r:8.1f} {vida:5.0f}% {cmds:8.1f} {sem:12.0f}% {parado:10.0f}%")


if __name__ == "__main__":
    main()
