"""O kit: as habilidades que o herói leva para a luta (etapa 4; roadmapIDEIAS/25, 3.1 e 3.10, e 26).

Três coisas separadas:
- **aprender** (`Jogador.habilidades`, o Grimório): sobe de nível, aprende as da classe e da especialização;
- **o kit** (`Jogador.kit`): o que vai para a luta, dentro de um orçamento de pontos (por tier) e de espaços, com no
  máximo uma ultimate; troca-se fora da luta, na vila e na fogueira;
- **o recurso** (Vigor, Foco, Mana): o que cada habilidade gasta na luta.

Atacar, Defender e Usar item não entram no kit nem no orçamento: são comandos de toda vez.

Números provisórios: 8 pontos, 5 espaços; tier comum 1, avançada 2, ultimate 3.
"""

from .habilidades import HABILIDADES

PONTOS = 8
ESPACOS = 5
PONTOS_TIER = {1: 1, 2: 2, "ultimate": 3}
NOME_TIER = {1: "comum", 2: "avançada", "ultimate": "ultimate"}


def tier(h_id):
    h = HABILIDADES[h_id]
    return "ultimate" if h.get("ultimate") else h.get("tier", 1)


def pontos(kit):
    return sum(PONTOS_TIER[tier(h)] for h in kit)


def ultimate(kit):
    return next((h for h in kit if HABILIDADES[h].get("ultimate")), None)


def motivo_kit(j, kit):
    """Por que esse kit não vale (ou None)."""
    if any(h not in j.habilidades for h in kit):
        return "Só habilidades que você já aprendeu."
    if len(set(kit)) != len(kit):
        return "Habilidade repetida."
    if len(kit) > ESPACOS:
        return f"No máximo {ESPACOS} habilidades."
    if sum(1 for h in kit if HABILIDADES[h].get("ultimate")) > 1:
        return "No máximo uma ultimate."
    if pontos(kit) > PONTOS:
        return f"O kit custa {pontos(kit)} pontos; o orçamento é {PONTOS}."
    return None


def motivo_incluir(j, h_id):
    """Por que essa habilidade não cabe no kit de agora (ou None)."""
    if h_id in j.kit:
        return None
    return motivo_kit(j, list(j.kit) + [h_id])


def ajustar(j, completar=False):
    """Garante que o kit é válido (tira o que não se aprendeu ou não cabe). Com completar, enche com as aprendidas que
    couberem, na ordem do Grimório (o save de antes do kit)."""
    kit = [h for h in (getattr(j, "kit", None) or []) if h in j.habilidades and h in HABILIDADES]
    while kit and motivo_kit(j, kit):
        kit.pop()
    if completar:
        for h in j.habilidades:
            if h not in kit and h in HABILIDADES and not motivo_kit(j, kit + [h]):
                kit.append(h)
    j.kit = kit
    return kit


def incluir_se_couber(j, h_id):
    """A habilidade recém-aprendida entra no kit se couber; senão fica no Grimório (troca-se na vila ou na fogueira).
    Devolve True se entrou."""
    if h_id in j.kit or motivo_incluir(j, h_id):
        return False
    j.kit = list(j.kit) + [h_id]
    return True


def alternar(j, h_id):
    """Põe ou tira uma habilidade do kit. Devolve o motivo se não couber (o kit fica como estava)."""
    if h_id in j.kit:
        j.kit = [h for h in j.kit if h != h_id]
        return None
    m = motivo_incluir(j, h_id)
    if m:
        return m
    j.kit = list(j.kit) + [h_id]
    return None


def resumo(j):
    return {"pontos": pontos(j.kit), "max_pontos": PONTOS, "espacos": len(j.kit), "max_espacos": ESPACOS,
            "ultimate": ultimate(j.kit)}


def papel(h_id):
    """O papel de uma habilidade para o kit montado sozinho: ultimate, defesa (proteção ou cura em você), recurso
    (o Meditar), area, alvo (dano num inimigo) ou apoio (o resto: marcar, enfraquecer, ordens)."""
    from .habilidades import Dano, blocos
    h = HABILIDADES[h_id]
    if h.get("ultimate"):
        return "ultimate"
    if h_id == "meditar":
        return "recurso"
    if h["alvo"] == "todos":
        return "area"
    passos = blocos(h)
    fere = any(isinstance(b, Dano) for b in passos) if h.get("passos") is not None else True  # fn própria: fere
    if h["alvo"] == "inimigo" and fere:
        return "alvo"
    if h["alvo"] == "proprio" and h.get("familia") in ("protecao", "cura", "sagrado", "arcano") and h_id != "erguer_servo":
        return "defesa"
    return "apoio"


def sugerido(j):
    """Um kit montado sozinho, para os níveis de teste (dev.subir_ate) e os robôs: como uma pessoa montaria, por papel
    (a ultimate, uma defesa, duas da especialização, o recurso do mago, o dano num alvo mais caro, uma área) e o resto
    pelo custo, enquanto couber. Na ordem do Grimório."""
    from .classes import SPECS
    validas = [h for h in j.habilidades if h in HABILIDADES]
    por_custo = sorted(validas, key=lambda h: (-HABILIDADES[h]["custo"], -validas.index(h)))
    da_spec = [h for _, h in SPECS[j.spec]["habilidades"]] if getattr(j, "spec", None) else []
    identidade = sorted([h for h in validas if h in da_spec and papel(h) != "ultimate"],
                        key=lambda h: (pontos([h]), HABILIDADES[h]["custo"]))[:2]
    ordem = []
    for p in ("ultimate", "defesa", "spec", "recurso", "alvo", "area", "alvo"):
        if p == "spec":
            ordem += [h for h in identidade if h not in ordem]
            continue
        ordem += [h for h in por_custo if papel(h) == p and h not in ordem][:1]
    ordem += [h for h in por_custo if h not in ordem]
    escolhidas = []
    for h in ordem:
        if not motivo_kit(j, escolhidas + [h]):
            escolhidas.append(h)
    j.kit = [h for h in validas if h in escolhidas]
    return j.kit
