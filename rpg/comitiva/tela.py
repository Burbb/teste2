"""O que a tela mostra da comitiva: o estado de cada um e a explicação da aprovação."""

from .catalogo import COMPANHEIROS
from .grupo import lealdade, membros, nivel
from .conversas import CONVERSAS, proxima_conversa


def explicar_aprovacao(g, m):
    """O que a barra de aprovação significa para este companheiro, agora."""
    d = COMPANHEIROS[m["id"]]
    a = m["aprovacao"]
    rotulo, _ = nivel(m)
    linhas = [f"Vai de −100 a +100. Agora: {a:+d} ({rotulo}).",
              f"Sobe quando você faz o que {d['curto']} admira ({', '.join(_valores(d, True))}); "
              f"desce com o que despreza ({', '.join(_valores(d, False))}).",
              f"Em combate, luta com {lealdade(m) * 100:.0f}% da força (de 60% a 135%, conforme a confiança)."]
    prox = next((req for etapa, req, _ in CONVERSAS.get(m["id"], []) if etapa == m["conversas"]), None)
    if prox and a < prox["aprov"]:
        linhas.append(f"A próxima conversa só se abre com aprovação {prox['aprov']:+d} ou mais.")
    elif prox and m["dias"] < prox["dias"]:
        linhas.append("A próxima conversa precisa de mais alguns dias juntos.")
    if a <= -15:
        linhas.append("Abaixo de −40, vai embora (e nem todos vão em paz).")
    elif a >= 75:
        linhas.append("Lealdade máxima: a história pessoal pode chegar ao fim e há bônus no combate.")
    return linhas


def _valores(d, bons):
    nomes = {"misericordia": "misericórdia", "fe": "fé", "honestidade": "honestidade", "crueldade": "crueldade",
             "sacrilegio": "sacrilégio", "magia_proibida": "magia proibida", "coragem": "coragem",
             "pragmatismo": "pragmatismo", "honra": "honra", "fuga": "fugir", "autoridade": "autoridade",
             "caridade": "caridade", "curiosidade": "curiosidade", "rebeldia": "rebeldia", "fanatismo": "fanatismo",
             "purificar": "purificar", "violencia": "violência", "ganancia": "ganância"}
    itens = sorted(d["valores"].items(), key=lambda kv: -kv[1] if bons else kv[1])
    return [nomes.get(k, k.replace("_", " ")) for k, v in itens if (v > 0) == bons][:3]


def estado(g, quem=None):
    lista = []
    for m in (membros(g) if quem is None else quem):
        d = COMPANHEIROS[m["id"]]
        rotulo, classe = nivel(m)
        lista.append({"id": m["id"], "nome": d["nome"], "titulo": d["titulo"], "desc": d["desc"],
                      "hp": m["hp"], "max_hp": m["max_hp"],
                      "aprovacao": m["aprovacao"], "nivel": rotulo, "classe": classe, "ferido": m["ferido"],
                      "papel": d["papel"], "conversa": bool(proxima_conversa(g, m)) and m["ultima_conversa"] != g.dia,
                      "aprovacao_info": explicar_aprovacao(g, m)})
    return lista
