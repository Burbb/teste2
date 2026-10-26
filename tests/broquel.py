"""Régua do Broquel do Vigia (E7): lutas inteiras do Guerreiro com cinco jeitos de usar o Erguer Escudo, comparando o
Broquel com o mesmo escudo sem o efeito, com um escudo raro e com a Égide do Mártir.

    python -m tests.broquel                       # os experimentos do Vale (níveis 4 e 5)
    python -m tests.broquel --exp talentos        # Contra-ataque, Muralha, Fôlego, espinhos, cura por dano (nível 6)
    python -m tests.broquel --exp comitiva        # com um companheiro (nível 5)
    python -m tests.broquel --exp posterior       # nível 9 contra o nível 8 (cenário artificial: fora do Vale)
    python -m tests.broquel --lutas 40            # lutas por célula (padrão 40: 4 heróis × 10 sementes)

Cada célula usa os mesmos heróis e as mesmas sementes em todas as variantes (pareado). O herói começa cada luta
inteiro, com 2 poções; não foge. As políticas (o que o robô faz com o escudo; o resto é o lutador da arena, sem os
botões de defesa, com poção abaixo de 35% e cura própria abaixo de 50%):
    atacar      nunca ergue o escudo
    abertura    ergue no primeiro turno, depois ataca
    manter      ergue sempre que não está em guarda (renova quando acaba)
    todo_turno  ergue em todo turno em que o Vigor dá
    preparado   ergue só quando um inimigo prepara o golpe
Colunas: vitórias, turnos, vida perdida (da vida máxima), poções gastas, Vigor no fim, a parte do dano do herói que
veio do Revide, a parte dos turnos do herói em guarda e os impasses (lutas que passam de 50 turnos)."""

import argparse
import copy
import random
import statistics

from rpg import comitiva, dev, missoes
from rpg.comitiva import COMPANHEIROS as MEMBROS
from rpg.inimigos import instanciar_guardiao
from rpg.itens import UNICOS_POR_ID, fazer_unico, gerar_equip

from tests import arena

POLITICAS = ("atacar", "abertura", "manter", "todo_turno", "preparado")
ESCUDOS = ("broquel", "sem_efeito", "raro", "egide")
DEFESAS = ("erguer_escudo",)
LIMITE_TURNOS = 50


class Impasse(Exception):
    pass


class Politica(arena.LutadorUI):
    def __init__(self, rng, politica="atacar"):
        super().__init__(rng)
        self.politica = politica
        self.acoes = self.em_guarda = 0

    def escolher(self, pergunta, opcoes):
        if pergunta == "Este é o momento do rito.":
            return 0  # dar descanso (o cenário "Ilse, rito")
        return super().escolher(pergunta, opcoes)

    def _decidir(self, cb, metas):
        j = cb.j
        if cb.turno > LIMITE_TURNOS:
            raise Impasse()
        self.acoes += 1
        self.em_guarda += bool(j.efeito("guarda"))
        self._plano = self._alvo = None
        itens = next((m["itens"] for m in metas if m.get("acao") == "itens"), [])
        habs = [m for m in next((m["habilidades"] for m in metas if m.get("acao") == "habilidades"), []) if m["pode"]]
        if j.hp < 0.35 * j.max_hp and any(m.get("usar_item") == "pocao_vida" and not m.get("motivo") for m in itens):
            self._plano = "pocao_vida"
            return "itens"
        cura = next((m["habilidade"] for m in habs if m["habilidade"] in arena.CURAS), None)
        if cura and j.hp < 0.5 * j.max_hp:
            self._plano = cura
            return "habilidades"
        vivos = cb.inimigos_vivos()
        quer = {"atacar": False, "abertura": self.acoes_luta == 1, "manter": not j.efeito("guarda"),
                "todo_turno": True, "preparado": any(e.carregando for e in vivos)}[self.politica]
        if quer and any(m["habilidade"] == "erguer_escudo" for m in habs):
            self._plano = "erguer_escudo"
            return "habilidades"
        h = self._habilidade(cb, [m for m in habs if m["habilidade"] not in DEFESAS])
        if h:
            self._plano = h
            return "habilidades"
        return "atacar"

    @property
    def acoes_luta(self):
        return self.acoes - self._inicio_luta


# ---------------------------------------------------------------- o herói e as variantes
BASE = {4: {"golpe_brutal": 2, "pele_ferro": 1}, 5: {"golpe_brutal": 2, "pele_ferro": 1, "folego": 1},
        6: {"golpe_brutal": 2, "pele_ferro": 1}, 9: {"golpe_brutal": 3, "pele_ferro": 2, "folego": 1}}
# Um talento da especialização em cada nível, igual em todas as variantes (cura própria do Paladino; cura por dano
# do Berserker).
DA_SPEC = {"paladino": {"luz_curativa": 1}, "berserker": {"sede_insaciavel": 1}}
TALENTOS = {  # o experimento de talentos (nível 6: 5 pontos, 3 da base e 2 aqui)
    "sem": {"folego": 2}, "contra1": {"contra_ataque": 1, "folego": 1}, "contra2": {"contra_ataque": 2},
    "muralha": {"muralha": 1, "folego": 1}, "muralha+contra1": {"muralha": 1, "contra_ataque": 1},
}


def escudo(tipo, nivel, rng):
    if tipo == "broquel":
        return fazer_unico(UNICOS_POR_ID["broquel_do_vigia"], nivel)
    if tipo == "sem_efeito":  # os mesmos números, sem o único (sem o Revide)
        it = fazer_unico(UNICOS_POR_ID["broquel_do_vigia"], nivel)
        it.pop("unico")
        it.update(nome="Broquel sem efeito", raridade="raro")
        return it
    if tipo == "egide":
        return fazer_unico(UNICOS_POR_ID["egide_do_martir"], nivel)
    return gerar_equip(rng, "guerreiro", nivel, "secundaria", raridade="raro")


def heroi(spec, nivel, semente, tipo_escudo, talentos=None, pele=False, membros=0, politica="atacar"):
    g = arena.novo_jogo(semente, "guerreiro")
    g.ui.__class__ = Politica
    g.ui.politica, g.ui.acoes, g.ui.em_guarda, g.ui._inicio_luta = politica, 0, 0, 0
    dev.subir_ate(g, nivel, spec=spec)
    j = g.j
    j.talentos.clear()
    j.pontos_talento = 0
    for t, r in {**BASE[nivel], **DA_SPEC[spec], **(talentos or {})}.items():
        j.talentos[t] = r
    rng = random.Random(semente)
    dev.vestir(g, rng, nivel)
    j.equip["secundaria"] = escudo(tipo_escudo, nivel, random.Random(semente * 7 + 1))
    if pele:
        j.equip["armadura"] = fazer_unico(UNICOS_POR_ID["pele_do_penitente"], nivel)
    j.recalcular()
    j.hp, j.rec = j.max_hp, j.max_rec
    j.consumiveis = {"pocao_vida": 2}
    g.comitiva = []
    for k in range(membros):
        m = comitiva.recrutar(g, list(MEMBROS)[(semente + k) % len(MEMBROS)])
        m["aprovacao"] = 30
    return g


# ---------------------------------------------------------------- os encontros
def cenarios(nivel):
    n = max(1, nivel - 1)

    def bando(fam, k, nv=n):
        return lambda g: [g.inimigo(fam, nivel=nv) for _ in range(k)]

    def preparado(fam, nome, nv):
        def f(g):
            grupo = [g.inimigo(fam, nivel=nv) for _ in range(2)]
            missoes._que_prepara(grupo[0], nome)
            return grupo
        return f

    def ilse(rito):
        def f(g):
            spec = {"bioma": "pantano", "id": "ilse", "nome": "Ilse, a Bruxa Afogada", "g": "f", "base": "Bruxa Afogada"}
            chefe = instanciar_guardiao(spec, 4)
            if rito:
                chefe.piso = max(1, int(chefe.max_hp * chefe.fases[0]["limiar"]))
                chefe.ao_limiar = lambda cb, e: missoes._momento_do_rito(g, cb, e)
            return [chefe]
        return f

    return {
        "1 bandido": bando("bandido", 1), "3 lobos": bando("lobo", 3), "3 esqueletos": bando("esqueleto", 3),
        "2 bandidos + cultista": lambda g: bando("bandido", 2)(g) + bando("cultista", 1)(g),
        "2 cultistas": bando("cultista", 2),
        # As lutas fixas da capela, no nível dela (3); depois do Vale, no nível do cenário.
        "ossuário (golpe preparado)": preparado("esqueleto", "Esqueleto de Guarda", 3 if nivel <= 5 else n),
        "sarilho (afogados)": preparado("afogado", "Afogado Inchado", 3 if nivel <= 5 else n),
        "Ilse, rito": ilse(True), "Ilse, destruir": ilse(False),
    }


# ---------------------------------------------------------------- medir
def lutar(g, criar, semente):
    """Uma luta do herói salvo, inteiro; devolve o que a tabela precisa."""
    ui = g.ui
    ui._inicio_luta = ui.acoes
    guarda_antes, acoes_antes = ui.em_guarda, ui.acoes
    j = g.j
    try:
        r = arena.lutar(g, lambda: criar(g), seed=semente)
    except Impasse:
        return {"impasse": True, "vitoria": False}
    tel = next(e for e in reversed(g.registro) if e["t"] == "combate")
    feitos = ui.acoes - acoes_antes
    return {"impasse": False, "vitoria": r["resultado"] == "vitoria", "turnos": tel["turnos"],
            "vida": r["vida_perdida"], "pocoes": 2 - j.consumiveis.get("pocao_vida", 0),
            "vigor": max(0, j.rec) / j.max_rec, "dano": tel["dano_causado"],
            "revide": tel["dano_por_hab"].get("Revide", 0), "guarda": (ui.em_guarda - guarda_antes) / max(1, feitos)}


def medir(spec, nivel, tipo, politica, criar, lutas, **extra):
    res = []
    herois = 4
    for h in range(herois):
        semente = 1000 * nivel + 97 * h + (0 if spec == "paladino" else 13)
        g = heroi(spec, nivel, semente, tipo, politica=politica, **extra)
        salvo = copy.deepcopy(g.j), copy.deepcopy(g.comitiva)
        for k in range(lutas // herois):
            g.j, g.comitiva = copy.deepcopy(salvo[0]), copy.deepcopy(salvo[1])
            g.clima, g.periodo = "limpo", 1
            res.append(lutar(g, criar, semente * 31 + k))
    return res


def resumo(res):
    ok = [r for r in res if not r["impasse"]]
    dano = sum(r["dano"] for r in ok)
    return {"vit": 100 * sum(r["vitoria"] for r in res) / len(res),
            "turnos": statistics.mean(r["turnos"] for r in ok) if ok else 0,
            "vida": 100 * statistics.mean(r["vida"] for r in ok) if ok else 0,
            "pocoes": statistics.mean(r["pocoes"] for r in ok) if ok else 0,
            "vigor": 100 * statistics.mean(r["vigor"] for r in ok) if ok else 0,
            "revide": 100 * sum(r["revide"] for r in ok) / dano if dano else 0,
            "guarda": 100 * statistics.mean(r["guarda"] for r in ok) if ok else 0,
            "impasses": sum(r["impasse"] for r in res)}


def linha(rot, s):
    return (f"| {rot} | {s['vit']:.0f}% | {s['turnos']:.1f} | {s['vida']:.0f}% | {s['pocoes']:.2f} | {s['vigor']:.0f}% | "
            f"{s['revide']:.0f}% | {s['guarda']:.0f}% | {s['impasses']} |")


CABECALHO = ("| {} | Vitórias | Turnos | Vida perdida | Poções | Vigor no fim | Revide (do dano) | Em guarda | Impasses |\n"
             "|---|---|---|---|---|---|---|---|---|")


def tabela(titulo, celulas, lutas, primeira="Escudo · política"):
    print(f"\n#### {titulo}\n")
    print(CABECALHO.format(primeira))
    for rot, args in celulas:
        print(linha(rot, resumo(medir(*args[:5], lutas, **args[5]))))


def exp_vale(lutas, nivel_lista=(4, 5)):
    for nivel in nivel_lista:
        for spec in ("paladino", "berserker"):
            for nome, criar in cenarios(nivel).items():
                celulas = []
                for tipo in ("broquel", "sem_efeito", "raro", "egide"):
                    for pol in POLITICAS:
                        if tipo in ("raro", "egide") and pol not in ("atacar", "preparado", "manter"):
                            continue
                        celulas.append((f"{tipo} · {pol}", (spec, nivel, tipo, pol, criar, {})))
                tabela(f"{spec.capitalize()} nível {nivel} — {nome}", celulas, lutas)


def exp_talentos(lutas, nivel=6, artificial=False):
    escolhidos = ("1 bandido", "3 lobos", "2 bandidos + cultista", "2 cultistas", "ossuário (golpe preparado)")
    for spec in ("paladino", "berserker"):
        for nome in escolhidos:
            criar = cenarios(nivel)[nome]
            celulas = []
            for tal, talentos in TALENTOS.items():
                for tipo in ("broquel", "sem_efeito"):
                    for pol in ("atacar", "manter", "todo_turno", "preparado"):
                        celulas.append((f"{tal} · {tipo} · {pol}", (spec, nivel, tipo, pol, criar, {"talentos": talentos})))
            for tipo in ("broquel", "sem_efeito"):  # os espinhos da Pele do Penitente, com Muralha e Contra-ataque
                for pol in ("atacar", "manter"):
                    celulas.append((f"muralha+contra1 + Pele · {tipo} · {pol}",
                                    (spec, nivel, tipo, pol, criar, {"talentos": TALENTOS["muralha+contra1"], "pele": True})))
            sufixo = " (artificial: fora do Vale)" if artificial else ""
            tabela(f"{spec.capitalize()} nível {nivel}{sufixo} — {nome}", celulas, lutas, "Talentos · escudo · política")


def exp_comitiva(lutas, nivel=5):
    for spec in ("paladino", "berserker"):
        for nome in ("1 bandido", "3 lobos", "2 bandidos + cultista", "Ilse, destruir"):
            criar = cenarios(nivel)[nome]
            celulas = [(f"{tipo} · {pol}", (spec, nivel, tipo, pol, criar, {"membros": 1}))
                       for tipo in ("broquel", "sem_efeito") for pol in ("atacar", "abertura", "manter", "preparado")]
            tabela(f"{spec.capitalize()} nível {nivel}, com um companheiro — {nome}", celulas, lutas)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--exp", default="vale", choices=("vale", "talentos", "comitiva", "posterior"))
    p.add_argument("--lutas", type=int, default=40)
    a = p.parse_args()
    if a.exp == "vale":
        exp_vale(a.lutas)
    elif a.exp == "talentos":
        exp_talentos(a.lutas)
    elif a.exp == "comitiva":
        exp_comitiva(a.lutas)
    else:
        exp_talentos(a.lutas, nivel=9, artificial=True)


if __name__ == "__main__":
    main()
