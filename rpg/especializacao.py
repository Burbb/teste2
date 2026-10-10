"""A escolha da especialização, explicada: o que cada caminho dá e tira, calculado para o herói de agora.

A prévia é feita numa CÓPIA do herói, com a mesma conta que a escolha de verdade usa (`aplicar_bonus`, `animal`): o que a
tela mostra antes é o que o herói fica depois. Consultar não mexe no herói, na comitiva, no sorteio nem no save.

    previa(j, spec)      tudo o que a tela de escolha mostra de um caminho
    beneficios(j, spec)  o que o caminho dá além dos números (passiva, testes, resistências, o animal); o Grimório usa
    limites(spec)        onde o caminho rende menos (tirado das habilidades e dos estados) e o que o catálogo declara
    texto_resumo / texto_detalhe   o mesmo, em linhas, para o modo texto
"""

import copy

from . import balanceamento as bal
from .classes import COMPANHEIROS, SPECS
from .dados import TRACOS_FICHA
from .entidades import nome_stat
from .estados import ESTADOS
from .habilidades import Aplicar, Dano, HABILIDADES, Salva, Se, descricao_habilidade
from .regras import NOMES_TESTE

ORDEM_STATS = ("max_hp", "max_rec", "atk", "defesa", "agi", "poder")
# O que as chaves de modificador que uma especialização declara (`mods` em classes.py) querem dizer para quem joga.
MODS_TEXTO = {
    "resiste_terror": lambda v: f"Resiste ao grito de terror em {v * 100:.0f}% das vezes (a fé não vacila).",
}
PLURAL_TRACO = {"morto-vivo": "mortos-vivos", "demonio": "demônios", "corrompido": "corrompidos", "etereo": "etéreos",
                "planta": "plantas", "construto": "construtos", "blindado": "blindados", "voador": "voadores"}
NOME_TIPO = {"sagrado": "sagrado", "sombra": "de sombra", "fogo": "de fogo", "gelo": "de gelo", "arcano": "arcano"}


def _num(x):
    return f"{x:.1f}".replace(".", ",").replace(",0", "")


def _sinal(v):
    return ("+" if v > 0 else "−") + _num(abs(v))


# ---------------------------------------------------------------------- a conta da escolha (a mesma de verdade)
def aplicar_bonus(j, spec):
    """Os bônus fixos da especialização no herói (Progressao.especializar e a prévia usam esta)."""
    j.spec = spec
    for k, v in SPECS[spec]["bonus"].items():
        j.base[k] += v
    j.recalcular()


def animal(tipo, nivel):
    """O companheiro animal chamado no nível dado (Progressao.escolher_companheiro e a prévia usam esta)."""
    c = COMPANHEIROS[tipo]
    hp = int(c["hp"] * (1 + bal.ANIMAL_VIDA_POR_NIVEL * (nivel - 1)))
    return {"tipo": tipo, "max_hp": hp, "hp": hp, "atk": c["atk"] * (1 + bal.ANIMAL_ATK_POR_NIVEL * (nivel - 1)),
            "agi": c["agi"], "alcance": c["alcance"], "crit": c["crit"]}


def copia_especializada(j, spec):
    """Uma cópia do herói já com a especialização (o herói real não muda)."""
    c = copy.deepcopy(j)
    aplicar_bonus(c, spec)
    c.hp, c.rec = c.max_hp, c.max_rec
    return c


# ---------------------------------------------------------------------- o que o caminho dá e tira
def beneficios(j, spec):
    """O que o caminho dá além dos números de atributo: a passiva, os testes, as resistências, o animal."""
    from .talentos import PASSIVAS
    s, linhas = SPECS[spec], []
    p = PASSIVAS.get(spec)
    if p:
        linhas.append(f"{p['nome']} (passiva): {p['desc']}")
    for chave, v in s.get("mods", {}).items():
        if chave in MODS_TEXTO:
            linhas.append(MODS_TEXTO[chave](v))
    if s.get("testes"):
        linhas.append("Nos testes: " + ", ".join(f"{NOMES_TESTE[t]} {_sinal(b)}" for t, (_, b) in s["testes"].items())
                      + ".")
    agi = s["bonus"].get("agi", 0)
    if agi > 0:  # a mesma conta do golpe (grimorio.chance_critico, combate.atacar): Agilidade vira crítico e esquiva
        linhas.append(f"Agilidade {_sinal(agi)}: +{_num(agi * bal.CRITICO_POR_AGI * 100)}% de chance de crítico e "
                      f"+{_num(agi * bal.ESQUIVA_POR_AGI * 100)}% de esquiva (até os tetos de sempre).")
    fera = getattr(j, "companheiro", None)
    if s.get("companheiro") and fera:
        linhas.append(f"{fera['nome']} ({COMPANHEIROS[fera['tipo']]['nome']}) luta ao seu lado todo turno; a Ordem da "
                      "Fera muda com o animal.")
    elif s.get("companheiro"):
        linhas.append("Um animal luta ao seu lado todo turno: lobo, falcão ou urso. Você escolhe ao confirmar; o animal "
                      "é para sempre, e a Ordem da Fera muda com ele.")
    return linhas


def _passos(h):
    """Todos os blocos de uma habilidade, os de dentro também (para ler o tipo do dano e os estados que ela põe)."""
    def ver(passos):
        for p in passos:
            yield p
            if isinstance(p, Dano):
                yield from ver(p.depois)
            elif isinstance(p, (Se, Salva)):
                yield from ver(p.passos)
    return list(ver(h.get("passos", [])))


def _da_especializacao(spec):
    return [h for _, h in SPECS[spec]["habilidades"]]


def _tipos(spec):
    """Os tipos de dano das habilidades do caminho (o que não é físico)."""
    tipos = []
    for h in _da_especializacao(spec):
        for p in _passos(HABILIDADES[h]):
            if isinstance(p, Dano) and p.tipo not in ("fisico",) and p.tipo not in tipos:
                tipos.append(p.tipo)
    return tipos


def _contra(tipo, melhor):
    """Os traços contra os quais um tipo de dano rende mais (melhor=True) ou menos, com o fator."""
    lista = []
    for t, tr in TRACOS_FICHA.items():
        f = tr.get("tipo", {}).get(tipo)
        if f is not None and (f > 1 if melhor else f < 1):
            lista.append((PLURAL_TRACO.get(t, t), f))
    return lista


def _fatores(lista):
    return ", ".join(f"{nome} {'imunes' if f == 0 else '×' + _num(f)}" for nome, f in lista)


def forte_contra(spec):
    return [f"Dano {NOME_TIPO.get(t, t)}: rende mais contra {_fatores(_contra(t, True))}."
            for t in _tipos(spec) if _contra(t, True)]


def limites(spec):
    """Onde o caminho rende menos: o tipo de dano contra quem resiste, os estados que não pegam em todos (do catálogo de
    estados) e o que a especialização declara (`limites` em classes.py)."""
    linhas = [f"Dano {NOME_TIPO.get(t, t)}: rende menos contra {_fatores(_contra(t, False))}."
              for t in _tipos(spec) if _contra(t, False)]
    vistos = set()
    for h in _da_especializacao(spec):
        for p in _passos(HABILIDADES[h]):
            efeito = p.efeito if isinstance(p, Aplicar) else None
            imunes = ESTADOS.get(efeito, {}).get("imunes") if efeito else None
            if imunes and efeito not in vistos:
                vistos.add(efeito)
                linhas.append(f"{efeito.capitalize()} ({HABILIDADES[h]['nome']}) não afeta {imunes}.")
    return linhas + list(SPECS[spec].get("limites", []))


# ---------------------------------------------------------------------- a prévia
def _habilidade(c, h, nivel_hab):
    from .talentos import custo_habilidade
    d = HABILIDADES[h]
    return {"id": h, "nome": d["nome"], "icone": d["icone"], "nivel": nivel_hab, "agora": nivel_hab <= c.nivel,
            "custo": custo_habilidade(c, h), "recurso": c.nome_recurso, "flechas": d.get("flechas", 0),
            "desc": descricao_habilidade(h, c), "linhas": d["linhas"](c)}


def previa(j, spec):
    """O que o caminho dá ao herói de agora, calculado numa cópia já especializada."""
    from .talentos import NIVEL_CAMADA, TALENTOS
    s = SPECS[spec]
    c = copia_especializada(j, spec)
    atributos = []
    for k in ORDEM_STATS:
        antes, depois = getattr(j, k), getattr(c, k)
        if depois != antes:
            atributos.append({"stat": nome_stat(k, j.nome_recurso), "delta": depois - antes, "antes": antes,
                              "depois": depois})
    por_nivel = [f"{nome_stat(k, j.nome_recurso)} {_sinal(v)}" for k, v in s.get("cresc", {}).items()]
    habilidades = [_habilidade(c, h, nv) for nv, h in s["habilidades"]]
    futuras = [x["nivel"] for x in habilidades if not x["agora"]]
    talentos = [{"nome": t["nome"], "nivel": NIVEL_CAMADA[t["camada"]], "max": t["max"], "desc": t["desc"]}
                for t in TALENTOS[j.classe] if t["spec"] == spec]
    return {
        "id": spec, "nome": s["nome"], "estilo": s["desc"],
        "atributos": atributos, "por_nivel": por_nivel,
        "habilidades": habilidades,
        "referencia": (f"Números no seu nível de agora ({j.nivel}), já com o caminho. "
                       + (f"A habilidade do nível {min(futuras)} vem com os números de hoje: eles sobem com o nível."
                          if futuras else "")).strip(),
        "beneficios": beneficios(c, spec) + forte_contra(spec),
        "animais": ([dict(animal(t, j.nivel), nome=COMPANHEIROS[t]["nome"], desc=COMPANHEIROS[t]["desc"])
                     for t in COMPANHEIROS] if s.get("companheiro") else []),
        "limites": limites(spec),
        "talentos": talentos,
    }


# ---------------------------------------------------------------------- o modo texto
def _linha(l):
    if l["tipo"] == "dano":
        return f"{l['rotulo']}: {l['min']}–{l['max']} (média {l['medio']}), crítico {l['critico']} em {l['chance_critico']}%"
    return l["texto"]


def texto_resumo(p):
    """O resumo de um caminho em linhas curtas: o que se compara."""
    linhas = [f"{p['nome'].upper()} — {p['estilo']}"]
    if p["atributos"]:
        linhas.append("  Atributos: " + ", ".join(f"{a['stat']} {_sinal(a['delta'])} ({a['antes']} → {a['depois']})"
                                                  for a in p["atributos"])
                      + (f". Por nível, a mais: {', '.join(p['por_nivel'])}." if p["por_nivel"] else "."))
    agora = [x for x in p["habilidades"] if x["agora"]]
    depois = [x for x in p["habilidades"] if not x["agora"]]
    linhas.append("  Agora: " + "; ".join(f"{x['nome']} ({x['custo']} {x['recurso'].lower()}): {x['desc'].rstrip('.')}"
                                         for x in agora) + ".")
    for x in depois:
        linhas.append(f"  No nível {x['nivel']}: {x['nome']} ({x['custo']} {x['recurso'].lower()}): {x['desc']}")
    for b in p["beneficios"]:
        linhas.append(f"  + {b}")
    for b in p["limites"]:
        linhas.append(f"  − {b}")
    return linhas


def texto_detalhe(p):
    """Os números das habilidades e os talentos do caminho: o que se lê antes de confirmar."""
    linhas = [p["referencia"]]
    for x in p["habilidades"]:
        quando = "agora" if x["agora"] else f"no nível {x['nivel']}"
        linhas.append(f"{x['nome']} ({quando}, {x['custo']} {x['recurso'].lower()}):")
        linhas += [f"  {_linha(l)}" for l in x["linhas"]]
    for a in p["animais"]:
        linhas.append(f"{a['nome']}: vida {a['max_hp']}, ataque {_num(a['atk'])}. {a['desc']}")
    if p["talentos"]:
        linhas.append("Talentos do caminho:")
        linhas += [f"  {t['nome']} (nível {t['nivel']}, até {t['max']}): {t['desc']}" for t in p["talentos"]]
    return linhas


# ---------------------------------------------------------------------- o Grimório
def pagina_grimorio(j):
    """A página do caminho no Grimório: o que ele dá além das habilidades (e onde rende menos)."""
    if not j.spec:
        return None
    s = SPECS[j.spec]
    bonus = ", ".join(f"{nome_stat(k, j.nome_recurso)} {_sinal(v)}" for k, v in s["bonus"].items())
    por_nivel = ", ".join(f"{nome_stat(k, j.nome_recurso)} {_sinal(v)}" for k, v in s.get("cresc", {}).items())
    linhas = [{"tipo": "efeito", "texto": b} for b in beneficios(j, j.spec) + forte_contra(j.spec)]
    linhas.append({"tipo": "efeito", "texto": f"Bônus do caminho: {bonus}." + (f" Por nível, a mais: {por_nivel}."
                                                                            if por_nivel else "")})
    linhas += [{"tipo": "efeito", "texto": f"Limite: {x}"} for x in limites(j.spec)]
    return {"id": "caminho", "nome": s["nome"], "icone": HABILIDADES[s["habilidades"][0][1]]["icone"],
            "rotulo": "Caminho", "passiva": True, "custo": 0, "alvo": "", "desc": s["desc"], "linhas": linhas}

