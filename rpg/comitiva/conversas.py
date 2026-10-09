"""As conversas de cada companheiro (registradas por eventos/comitiva.py), as falas da noite e o carinho no animal."""

from ..telemetria import registrar
from .catalogo import CARINHO, COMPANHEIROS
from .grupo import membro, membros, nivel, nome


CONVERSAS = {}  # cid -> lista de (etapa, requisitos, função); preenchida por eventos/comitiva.py


def conversa(cid, etapa, dias=0, aprov=-100, cond=None):
    """Registra a conversa número `etapa` de um companheiro."""
    def deco(fn):
        CONVERSAS.setdefault(cid, []).append((etapa, dict(dias=dias, aprov=aprov, cond=cond), fn))
        CONVERSAS[cid].sort(key=lambda c: c[0])
        return fn
    return deco


def proxima_conversa(g, m):
    for etapa, req, fn in CONVERSAS.get(m["id"], []):
        if etapa != m["conversas"]:
            continue
        if m["dias"] < req["dias"] or m["aprovacao"] < req["aprov"]:
            return None
        if req["cond"] and not req["cond"](g, m):
            return None
        return fn
    return None


def conversar(g, m):
    fn = proxima_conversa(g, m)
    if fn and m["ultima_conversa"] != g.dia:
        m["ultima_conversa"] = g.dia
        g.ui.cena(f"Conversa com {nome(m['id'])}", g.contexto_cena(), "evento")
        fn(g, m)
        m["conversas"] += 1
        registrar(g, "comitiva", acao="conversa", id=m["id"], etapa=m["conversas"])
        return True
    return False


def falar(g, cid):
    """Puxar conversa com alguém da comitiva: a conversa que espera, ou uma fala à toa se não há nenhuma."""
    m = membro(g, cid)
    if not conversar(g, m):
        g.ui.fala(cid, nome(cid), fala_ociosa(g, m))


def noite(g):
    """No acampamento, alguém da comitiva pode puxar conversa. Devolve True se houve conversa."""
    pendentes = [m for m in membros(g) if proxima_conversa(g, m) and m["ultima_conversa"] != g.dia]
    if pendentes and g.chance(0.65):
        return conversar(g, g.sortear(pendentes))
    return False


def fala_ociosa(g, m):
    _, classe = nivel(m)
    faixa = "alto" if classe in ("bom", "alto", "maximo") else "baixo" if classe in ("baixo", "partindo") else "medio"
    return g.sortear(COMPANHEIROS[m["id"]]["ocioso"][faixa])


def carinho(g):
    """Uma vez por noite: o animal do patrulheiro acorda animado e entra na próxima luta com +15% de dano.
    (A vida ele já recupera dormindo; o carinho é o laço.)"""
    f = g.j.companheiro
    if f.get("carinho") == g.dia:
        texto = f"{f['nome']} já dorme encostado em você, roncando baixinho."
        g.ui.reacao_animal({"nome": f["nome"], "texto": texto, "repetido": True}, texto, "cinza")
        return
    f["carinho"] = g.dia
    f["animado"] = True
    texto = g.sortear(CARINHO.get(f["tipo"], CARINHO["lobo"])).format(n=f["nome"])
    efeito = "Amanhã, na primeira luta, ele entra animado: +15% de dano."
    g.ui.reacao_animal({"nome": f["nome"], "texto": texto, "efeito": efeito},
                       f"{texto} ({efeito[0].lower()}{efeito[1:-1]})", "verde")
