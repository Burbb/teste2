"""Cenário só do protótipo (não é teste nem jogo): a campanha do lado de fora da Capela Afogada, à noite, com a
comitiva, pronta para acampar. Sobe o servidor do jogo como os cenários de tests/navegador/cenarios.py:

    python ferramentas/prototipos/acampamento/cenario_acampamento.py capela_fora

CLASSE (padrão mago), COMITIVA (padrão "morel,odete"), RESERVA (padrão "yara"), FERIDO (quem está ferido), PERIODO
(padrão 3, noite), CLIMA (padrão limpo), FERA=1 (o lobo do patrulheiro: CLASSE=arqueiro). PROTOTIPO=1 (padrão) serve o jogo com o
acampamento do protótipo (acampamento-no-jogo.js colado ao fim de telas/fogueira.js, numa cópia da pasta static);
PROTOTIPO=0, o jogo como está. Sair leva ao título.
"""

import argparse
import os
import shutil
import sys
import tempfile

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, RAIZ)

from tests.navegador import cenarios as C  # noqa: E402
from rpg import comitiva as cm, missoes  # noqa: E402
from rpg.jogo import FimDeJogo, Jogo  # noqa: E402


def capela_fora(ui):
    from rpg.__main__ import menu_principal
    pasta = tempfile.mkdtemp()
    g = Jogo(ui, seed=5, pasta_saves=pasta, hardcore=False)
    ui.jogo = g
    g.iniciar("Jean", os.environ.get("CLASSE", "mago"), "turvo")
    missoes.registro(g, "febre_do_turvo").update(
        etapa="capela", cenas=["abertura", "capela_exterior"], sala="exterior",
        pistas=["agua_do_leste", "represa", "canal_da_capela"])
    ativos = [c for c in os.environ.get("COMITIVA", "morel,odete").split(",") if c]
    reserva = [c for c in os.environ.get("RESERVA", "yara").split(",") if c]
    for c in reserva + ativos:
        cm.recrutar(g, c)
    for c in reserva:
        cm.para_acampamento(g, c, silencioso=True)
    if os.environ.get("FERA"):  # o animal do patrulheiro, como o jogo dá na especialização
        from rpg import especializacao
        g.j.companheiro = {"nome": "Cinza", **especializacao.animal("lobo", g.j.nivel)}
    for c in os.environ.get("FERIDO", "").split(","):
        if cm.membro(g, c):
            cm.membro(g, c)["ferido"] = True
    j = g.j
    j.provisoes = 3
    j.recalcular()
    j.hp = max(1, j.max_hp // 2)  # com o que recuperar: o Acampar aparece
    for l in g.mundo["locais"]:
        l["visitado"] = l["chave"] in ("vau_do_turvo", "charco_dos_juncos", "bosque_do_moinho", "capela_afogada")
    g.mundo["atual"] = next(l["id"] for l in g.mundo["locais"] if l["chave"] == "capela_afogada")
    g.dia, g.periodo, g.clima = 5, int(os.environ.get("PERIODO", "3")), os.environ.get("CLIMA", "limpo")
    try:
        g.rodar()
    except FimDeJogo:
        pass
    ui.jogo = None
    menu_principal(ui, argparse.Namespace(seed=1, saves=pasta, brando=False))


def servir_prototipo():
    """Uma cópia da pasta static com o protótipo colado ao fim de telas/fogueira.js; o servidor passa a ler dela. O
    jogo (rpg/web/static) não muda."""
    from rpg.web import servidor
    copia = os.path.join(tempfile.mkdtemp(), "static")
    shutil.copytree(servidor.PASTA, copia)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "acampamento-no-jogo.js"), encoding="utf-8") as f:
        extra = f.read()
    with open(os.path.join(copia, "telas", "fogueira.js"), "a", encoding="utf-8") as f:
        f.write("\n" + extra)
    servidor.PASTA = copia


C.CENARIOS["capela_fora"] = capela_fora
if __name__ == "__main__":
    if os.environ.get("PROTOTIPO", "1") != "0":
        servir_prototipo()
    C.main()
