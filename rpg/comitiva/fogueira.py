"""A fogueira: a cena do acampamento com a comitiva em volta do fogo e o menu da comitiva."""

from .catalogo import ATALHOS_FOGUEIRA, COMPANHEIROS, LIMITE
from .grupo import chamar, fora, membro, membros, na_reserva, nivel, nome, para_acampamento, reserva
from .conversas import carinho, conversar, fala_ociosa, falar, proxima_conversa
from .tela import estado


def fogueira(g, intro=None):
    """O acampamento à noite: quem anda com você e quem espera na reserva, em volta do fogo.
    Conversar, trocar quem vai junto amanhã e, por fim, dormir. Devolve True se houve conversa de história.
    Em volta do fogo é um lugar seguro: dá para abrir os baús (g.na_fogueira)."""
    g.na_fogueira = True
    try:
        return _fogueira(g, intro)
    finally:
        g.na_fogueira = False


def _fogueira(g, intro):
    conversou = False
    ociosos = set()
    primeira = True
    while True:
        ms, rs = membros(g), reserva(g)
        g.ui.cena("Fogueira", g.contexto_cena(), "menu")
        # A frase da noite é parte da tela: quem a desenha mostra de novo a cada volta (carinho, trocar quem vai),
        # senão a página encolhe e pula; no texto, ela sai só uma vez.
        dados = {"ativos": estado(g), "reserva": estado(g, reserva(g)), "limite": LIMITE,
                 "clima": g.clima, "bioma": g.loc["bioma"], "intro": intro}
        fera = getattr(g.j, "companheiro", None)
        if fera:  # o animal do patrulheiro dorme junto do fogo
            dados["fera"] = {"nome": fera["nome"], "tipo": fera["tipo"], "hp": fera["hp"], "max_hp": fera["max_hp"]}
        if not g.ui.painel("acampamento", dados):
            if intro and primeira:
                g.dizer(intro, "cinza")
            for m in ms + rs:
                onde = "na comitiva" if m in ms else "no acampamento"
                g.dizer(f"{nome(m['id'])} ({onde}) — vida {m['hp']}/{m['max_hp']} · {nivel(m)[0]}", "cinza")
        primeira = False
        opcoes = []
        for m in ms + rs:
            tem = proxima_conversa(g, m) and m["ultima_conversa"] != g.dia
            if tem or m["id"] not in ociosos:
                opcoes.append((f"Conversar com {nome(m['id'])}" + ("  ✉" if tem else ""), ("falar", m["id"]),
                               {"conversar": m["id"]}))
        for m in rs:
            if len(ms) < LIMITE:
                opcoes.append((f"Levar {nome(m['id'])} amanhã", ("chamar", m["id"]), {"chamar": m["id"]}))
            else:
                for a in ms:
                    opcoes.append((f"Levar {nome(m['id'])} no lugar de {nome(a['id'])}", ("trocar", m["id"], a["id"]),
                                   {"chamar": m["id"], "sai": a["id"]}))
        for m in ms:
            opcoes.append((f"Deixar {nome(m['id'])} no acampamento", ("reservar", m["id"]), {"reservar": m["id"]}))
        if getattr(g.j, "companheiro", None):
            opcoes.append((f"Fazer carinho em {g.j.companheiro['nome']}", ("carinho", None), {"carinho": "fera"}))
        opcoes.append(("Dormir até o amanhecer", None, {"dormir": True}))
        # Em volta do fogo é a hora de cuidar das coisas: talentos, inventário, diário, salvar (a doca acende)...
        opcoes += [o for o in g.opcoes_comuns() if o and o[1] in ATALHOS_FOGUEIRA]
        # ...e de fazer curativos: a bolsa do painel funciona aqui (bandagem, poção, unguento).
        opcoes += g.opcoes_bolsa()
        op = g.menu("", opcoes)
        if op is None:
            return conversou
        if isinstance(op, str):
            g.executar_comum(op)
            continue
        acao, cid = op[0], op[1]
        if acao in ("usar", "usar_em"):
            g.executar_comum(op)
            continue
        if acao == "carinho":
            carinho(g)
            continue
        m = membro(g, cid) or na_reserva(g, cid)
        if acao == "falar":
            if conversar(g, m):
                conversou = True
            else:
                ociosos.add(cid)
                g.ui.fala(cid, nome(cid), fala_ociosa(g, m))
        elif acao == "chamar":
            chamar(g, cid)
        elif acao == "trocar":
            para_acampamento(g, op[2], silencioso=True)
            chamar(g, cid)
        elif acao == "reservar":
            para_acampamento(g, cid)


def menu(g):
    while True:
        ms = membros(g)
        g.ui.cena("Comitiva", f"{len(ms)}/{LIMITE} companheiros", "menu")
        if not ms:
            rs = reserva(g)
            g.dizer("Ninguém caminha com você agora." + (
                f" {' e '.join(nome(m['id']) for m in rs)} espera{'m' if len(rs) > 1 else ''} no acampamento: "
                "monte a fogueira para chamar." if rs else " Por enquanto."), "cinza")
            g.pausar()
            return
        painel = {"membros": estado(g), "limite": LIMITE, "reserva": estado(g, reserva(g))}
        for m in ([] if g.ui.painel("comitiva", painel) else ms):
            d = COMPANHEIROS[m["id"]]
            rotulo, _ = nivel(m)
            situacao = " · FERID" + ("A" if d["g"] == "f" else "O") + ", fora de combate até descansar" if m["ferido"] else ""
            situacao += f" · {fora(g, m)['curto']}" if fora(g, m) else ""
            g.dizer(f"{d['nome']}, {d['titulo']} — vida {m['hp']}/{m['max_hp']} · {rotulo}{situacao}")
            g.dizer(d["desc"], "cinza")
        opcoes = []
        for m in [m for m in ms if not fora(g, m)]:  # quem espera lá fora conversa quando vocês se encontrarem
            novidade = "  (tem algo a dizer)" if proxima_conversa(g, m) and m["ultima_conversa"] != g.dia else ""
            opcoes.append((f"Conversar com {nome(m['id'])}{novidade}", ("falar", m["id"]), {"conversar": m["id"]}))
        for m in ms:
            opcoes.append((f"Mandar {nome(m['id'])} para o acampamento", ("acampamento", m["id"]),
                           {"acampamento": m["id"]}))
        opcoes.append(("Voltar", None))
        op = g.menu("", opcoes)
        if op is None:
            return
        acao, cid = op
        if acao == "falar":
            falar(g, cid)
        else:
            g.narrar(f"{nome(cid)} pega as coisas e volta para o acampamento. Quando você montar a fogueira, "
                     "vai estar lá.", "cinza")
            para_acampamento(g, cid)
