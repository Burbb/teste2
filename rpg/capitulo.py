"""O fim do primeiro capítulo (E9): o Vale do Turvo termina quando a febre acabou e a praça teve a resposta a Caspar.

Uma cena curta no Vau, uma vez, na próxima vez em que o herói está no menu de lá (missoes.cena_pendente: nunca no meio
de uma luta, de um serviço ou de um evento). Ela diz como ficaram a Fonte (e Marta), Ilse, Caspar e Yara, cada um numa
frase do estado de agora, e avisa que este é o fim do capítulo disponível e que o Vale continua aberto. Não abre a
Estrada de Varn, não dá nada e não decide nada; a herança de Vó Berta, se ainda espera, continua na taverna.

Um save que já tinha tudo resolvido recebe a cena do mesmo jeito, na próxima visita ao Vau. A cena fica guardada nas
cenas vistas da Vigília (a última missão a terminar), como as outras cenas de missão. missoes.py registra a cena no
fim dele; daqui, missoes e o resto só se importam na hora de usar.
"""

FEBRE, VIGILIA = "febre_do_turvo", "vigilia_de_caspar"
TITULO = "O Vale do Turvo"
SUBTITULO = "fim do primeiro capítulo"
AVISO = "Este é o fim do capítulo disponível. Você pode continuar explorando o Vale."


def concluido(g):
    """As duas missões do Vale estão concluídas (o capítulo acabou, com ou sem a cena já vista)."""
    from . import missoes
    if g.campanha != "turvo":
        return False
    f, v = missoes.registro(g, FEBRE), missoes.registro(g, VIGILIA)
    return bool(f and v and f.get("concluida") and v.get("concluida"))


def para_tela(g):
    """O que o rastreador e o Diário mostram depois do fim do capítulo, ou None."""
    if not concluido(g):
        return None
    return {"nome": TITULO, "texto": "Primeiro capítulo concluído.", "nota": "Você pode continuar explorando o Vale."}


# ------------------------------------------------------------------ a cena
# Uma frase por eixo, do estado de agora. Não repete a frase da vila (consequencias.FRASES e caspar.FRASE_PRACA, que o
# menu do Vau mostra logo depois) nem conta o que ainda não aconteceu: com a Fonte escura ou limpando, Marta segue de
# cama.
FONTE = {
    ("descansada", "limpando"): "A água da Fonte Nova está clareando. Marta ainda está de cama.",
    ("destruida", "escura"): "A água da Fonte Nova ainda está escura, e Marta piorou com ela.",
    ("destruida", "limpando"): "A água da Fonte Nova já não corre preta, mas ainda não está limpa. Marta ainda está de "
                               "cama.",
}
FONTE_LIMPA = "A água da Fonte Nova está limpa de novo, e Marta voltou a atender na cabana."

CASPAR = {
    "apoiar": "Toda noite, a vigília de Caspar reúne a vila na praça.",
    "denunciado": "Caspar foi embora do Vau, e ninguém acende vela por ele.",
    "denuncia_falhou": "Caspar ficou no Vau, mas a vigília dele acabou.",
    "calar": "Ninguém desmentiu Caspar, e a praça continua dele.",
}


def _ilse(f, postura):
    if f["desfecho"] == "descansada":
        return "Ilse descansa no fundo da capela, com a fita de Berta entre os dedos."
    if postura == "apoiar":
        return "Os ossos de Ilse foram queimados na praça, na vigília de Caspar."
    return "Os ossos de Ilse ficaram no fundo da capela, sem nome."


def _yara(g, postura):
    from . import caspar
    onde = caspar.situacao_yara(g)
    livre = postura in ("denunciado", "denuncia_falhou")
    if onde == "morta":
        return "Yara morreu na fogueira de Caspar." + (" A praça sabe agora que ela não trouxe a febre."
                                                      if postura == "denunciado" else "")
    if onde in ("grupo", "reserva"):
        return {"apoiar": "Yara continua com você, mas a vigília não a deixa entrar no Vau.",
                "denunciado": "Yara anda livre pelo Vau.",
                "denuncia_falhou": "Yara pode entrar no Vau, mas é vigiada.",
                "calar": "Yara entra no Vau, mas evita a praça."}[postura]
    if onde == "recusou":
        return "Yara vive no Charco dos Juncos" + (", e ninguém mais a procura." if livre else
                                                  ", e a vigília ainda fala dela.")
    return ("Ninguém mais procura a moça do brejo que Caspar acusava." if livre else
            "A vigília ainda procura a moça do brejo que Caspar acusa." if postura == "apoiar" else
            "Caspar ainda culpa a moça do brejo pela febre.")


def linhas(g):
    """As frases da cena, na ordem: a Fonte, Ilse, Caspar e Yara."""
    from . import consequencias, missoes
    f, v = missoes.registro(g, FEBRE), missoes.registro(g, VIGILIA)
    postura = v["desfecho"]
    fonte = FONTE.get((f["desfecho"], consequencias.estado_fonte(g)), FONTE_LIMPA)
    return [fonte, _ilse(f, postura), CASPAR[postura], _yara(g, postura)]


def _cena(g, mid):
    from . import missoes
    g.ui.cena(TITULO, SUBTITULO, "vitoria")
    fonte, ilse, caspar, yara = linhas(g)
    g.narrar(f"{fonte} {ilse}")
    g.narrar(f"{caspar} {yara}")
    g.dizer(AVISO, "cinza")
    if missoes.heranca_pendente(missoes.registro(g, FEBRE)):
        g.dizer("Vó Berta ainda espera você na taverna.", "amarelo")


CENA = dict(missao=VIGILIA, id="fim_do_capitulo", lugar="vau_do_turvo", etapas=("praca",), fn=_cena, confirmar=True,
            pode=concluido)
