"""A comitiva antes da batalha final."""

from .grupo import membros, sair


def antes_da_batalha_final(g):
    """A comitiva diante do fim. Devolve inimigos extras (traições), se houver."""
    extras = []
    for m in membros(g):
        cid = m["id"]
        if cid == "yara" and m.get("caminho") == "vazio" and m["aprovacao"] < 40:
            g.narrar("Yara dá um passo à frente, e não para. Atravessa o salão até o trono e se vira para você. "
                     "Os olhos dela agora são dois poços sem fundo.", "magenta")
            g.narrar("\"Desculpe\", diz ela, e parece sincera. \"Ele me prometeu o que você nunca prometeu: "
                     "que eu nunca mais teria medo.\"", "magenta+negrito")
            sair(g, "yara", "traiu")
            extras.append("yara")
        elif m["aprovacao"] >= 45:
            falas = {
                "odete": "Odette aperta seu ombro. \"Desta vez eu não vou fugir.\"",
                "morel": "Morel desembainha a espada e se põe um passo à sua frente. \"Segura a linha. Eu seguro você.\"",
                "yara": "Yara entrelaça os dedos nos seus por um instante. \"Ele vai tentar falar comigo. Não deixa.\"",
            }
            g.narrar(falas[cid], "verde")
    if g.flag("yara_com_ulook") and "yara" not in extras:
        g.narrar("Ao lado do trono, uma figura conhecida, de olhos negros. Yara. Ela encontrou quem a ouvisse.",
                 "magenta")
        extras.append("yara")
    return extras
