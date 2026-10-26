"""Os dados da proposta de gerenciamento da comitiva (protótipo; nada disto está no jogo).

Vem do motor: o herói (Guerreiro paladino nível 5, vestido como o jogo vestiria), os companheiros com a vida, o Ataque,
o Poder, a Defesa e a Agilidade de hoje (comitiva.atributos) e itens de verdade na bolsa (itens.gerar_equip), com a
ficha que a tela já mostra (web/estado._item).

DADOS TEMPORÁRIOS (proposta, marcados na tela): o equipamento de cada companheiro, a classe de peças que cada um usa,
os atributos deles e a sugestão de distribuição. Rodar de novo dá o mesmo arquivo (sementes fixas).

    python ferramentas/prototipos/comitiva-gerenciamento/gerar_dados.py   (na raiz do repositório)
"""

import json
import os
import random
import sys
import tempfile

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, RAIZ)

from rpg import comitiva as cm  # noqa: E402
from rpg.comitiva.luta import RECURSO  # noqa: E402
from rpg import dev  # noqa: E402
from rpg.itens import gerar_equip  # noqa: E402
from rpg.jogo import Jogo  # noqa: E402
from rpg.ui import BotUI  # noqa: E402
from rpg.web.estado import _item, heroi as ficha_heroi  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))

# A proposta: que peças cada companheiro usa (as de uma classe e as sem classe). Odette luta com bastão e fé (as do
# mago); Morel, com arma e escudo (as do guerreiro); Yara, com magia (as do mago).
CLASSE_PECAS = {"odete": "mago", "morel": "guerreiro", "yara": "mago"}
# Os atributos propostos (24 pontos, como o herói), pela identidade de cada um; a sugestão de distribuição, ciclando.
ATRIBUTOS = {
    "odete": dict(forca=2, agilidade=3, constituicao=4, intelecto=7, percepcao=3, vontade=5),
    "morel": dict(forca=7, agilidade=3, constituicao=7, intelecto=1, percepcao=3, vontade=3),
    "yara": dict(forca=1, agilidade=4, constituicao=3, intelecto=8, percepcao=5, vontade=3),
}
SUGESTAO = {"odete": ["vontade", "intelecto", "constituicao"], "morel": ["constituicao", "forca", "vontade"],
            "yara": ["intelecto", "percepcao", "vontade"]}
PONTOS_POR_NIVEL = 1  # proposta: a metade do herói (os companheiros não viram cópias dele)
ESPACOS = ("cabeca", "amuleto", "armadura", "maos", "arma", "secundaria", "pernas", "pes", "anel1", "anel2")


def peca(rng, classe, nivel, slot, raridade=None):
    for _ in range(40):
        it = gerar_equip(rng, classe, nivel, slot=slot, raridade=raridade)
        if it["slot"] == slot or (slot.startswith("anel") and it["slot"] == "anel"):
            return it
    return None


def montar():
    g = Jogo(BotUI(random.Random(1)), seed=11, pasta_saves=tempfile.mkdtemp(), hardcore=False)
    g.iniciar("Jean", "guerreiro", "turvo")
    dev.subir_ate(g, 5, spec="paladino")
    dev.vestir(g, random.Random(3), 5)
    for cid in ("odete", "morel", "yara"):
        cm.recrutar(g, cid)
    rng = random.Random(21)
    # a bolsa do grupo: a mochila de hoje (12 espaços), com peças das três classes e sem classe
    bolsa = []
    for classe, slot, rar in (("guerreiro", "arma", "magico"), ("mago", "arma", "magico"), ("guerreiro", "secundaria", None),
                              (None, "armadura", "raro"), ("mago", "cabeca", None), (None, "anel", "magico"),
                              ("arqueiro", "arma", None), (None, "pes", None)):
        it = peca(rng, classe or "guerreiro", 5, slot, rar)
        if it and classe is None:
            it["classe"] = None
        if it:
            bolsa.append(it)
    h = ficha_heroi(g)
    personagens = [{
        "id": "j", "nome": h["nome"], "titulo": f"{h['titulo']} · nível {h['nivel']}", "retrato": "j", "classe": "guerreiro",
        "pecas": "guerreiro", "recurso": h["recurso"], "equip": h["equip"], "derivados": h["atributos"],
        "atributos": {a["id"]: a["valor"] for a in h["atributos_base"]}, "temporario": False, "disponivel": True,
    }]
    for k, m in enumerate(cm.junto(g) + cm.reserva(g)):
        cid = m["id"]
        base = cm.atributos(g, m)
        equip = {s: None for s in ESPACOS}
        # TEMPORÁRIO: duas peças vestidas, para a comparação ter o que comparar
        for slot in ("arma", "armadura"):
            it = peca(random.Random(100 + k * 10 + len(slot)), CLASSE_PECAS[cid], 4, slot)
            if it:
                equip[slot] = _item(it, RECURSO[cid])
        personagens.append({
            "id": cid, "nome": cm.nome(cid), "titulo": cm.COMPANHEIROS[cid]["titulo"], "retrato": cid,
            "classe": CLASSE_PECAS[cid], "pecas": CLASSE_PECAS[cid], "recurso": RECURSO[cid], "equip": equip,
            "derivados": {"Ataque": round(base["atk"], 1), "Defesa": base["defesa"], "Agilidade": base["agi"],
                          "Poder": round(base["poder"], 1)},
            "vida": [m["hp"], m["max_hp"]],
            "atributos": dict(ATRIBUTOS[cid]), "sugestao": SUGESTAO[cid],
            "pontos": PONTOS_POR_NIVEL * (g.j.nivel - 1), "temporario": True,
            "disponivel": not m.get("ferido"),
        })
    # um caído (TEMPORÁRIO): Yara ferida, para mostrar o personagem indisponível
    personagens[-1]["disponivel"] = False
    personagens[-1]["indisponivel"] = "Ferida: fora das lutas até descansar. O equipamento dela pode ser trocado."
    return {"personagens": personagens, "bolsa": [_item(it, "Vigor") for it in bolsa], "limite": 12,
            "pontos_por_nivel": PONTOS_POR_NIVEL}


if __name__ == "__main__":
    dados = montar()
    with open(os.path.join(AQUI, "dados.json"), "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=1)
    print("dados.json:", len(dados["personagens"]), "personagens,", len(dados["bolsa"]), "itens na bolsa")
