"""Habilidades como dados.

Cada habilidade é uma ficha (nome, custo, alvo, descrição curta) e uma lista de **passos**: blocos pequenos
que sabem duas coisas, *executar* na luta e *se descrever* no Grimório. Assim o número existe num lugar só:
o "170%" do Golpe Pesado é o mesmo que o combate usa e o que o livro mostra.

    "golpe_pesado": hab("Golpe Pesado", 10, "inimigo", "170% de dano físico.",
                        [Dano(1.7, rotulo="Golpe Pesado")]),

Os blocos:
    Dano      um golpe (no alvo ou em todos); `depois` roda para cada alvo atingido
    Se        condição sobre o último golpe: "acertou", "vivo", "acertou_vivo"
    Aplicar   um estado num inimigo (sangramento, atordoado...), com chance; `direto` não anuncia
    Buff      um estado em você (guarda, fortalecido, esquiva...)
    Acender   queimadura (camadas, duração e valor do mago)
    Roubo     cura parte do dano causado, com o sangue voltando na tela
    CurarPeloDano / Curar / LimparMales
    Dizer     a frase da habilidade (aceita {alvo}, {cura}, {turnos})
    Salva     os golpes de dentro saem juntos na tela (rajada)
    Codigo    o escape para o que não cabe nos blocos, com execução e descrição lado a lado

Habilidades muito particulares (Redemoinho, Ordem da Fera, Combustão...) usam `fn` e `linhas` próprios,
mas continuam aqui, ao lado das outras: quem mexe numa habilidade mexe num lugar só.

Regra de ouro ao criar blocos: a ordem dos sorteios (rng) tem de ser a mesma de um código escrito à mão,
para o gabarito de regressão continuar idêntico quando nada de jogo mudou.
"""

from . import balanceamento as bal

NOME_STAT = {"atk": "Ataque", "poder": "Poder", "agi": "Agilidade", "max_hp": "Vida máx.", "defesa": "Defesa"}


def _pct(x):
    return f"{x * 100:.0f}%"


def _num(x):
    return f"{x:.1f}".replace(".", ",").replace(",0", "")


# ---------------------------------------------------------------------- valores que dependem do herói
class Escala:
    """Um número que cresce com o herói: soma de atributo × fator, com um mínimo. Sabe se escrever."""

    def __init__(self, minimo=0, **fatores):
        self.minimo, self.fatores = minimo, fatores

    def valor(self, u):
        total = 0
        for stat, f in self.fatores.items():
            total += getattr(u, stat) * f
        return max(self.minimo, total)

    def texto(self):
        return " + ".join(f"{NOME_STAT.get(k, k)} × {_pct(f)}" for k, f in self.fatores.items())


class Tal:
    """Base + um tanto por ponto de talento (ex.: Erguer Escudo dura 2 turnos + 1 por ponto de Muralha)."""

    def __init__(self, base, talento, por_ponto):
        self.base, self.talento, self.por = base, talento, por_ponto

    def valor(self, u):
        return self.base + self.por * u.tal(self.talento)


def valor(x, u):
    return x.valor(u) if hasattr(x, "valor") else x


# ---------------------------------------------------------------------- a execução
class Contexto:
    """O que os passos de uma habilidade compartilham enquanto ela acontece."""

    def __init__(self, cb, u, alvo):
        self.cb, self.u, self.alvo = cb, u, alvo
        self.atual = alvo    # o alvo do golpe mais recente (em área, muda a cada inimigo)
        self.dano = 0        # o dano do golpe mais recente
        self.cura = 0        # a última cura (para frases como "+{cura} vida")
        self.turnos = None   # a duração do último Buff (para "por {turnos} turnos")


def executar(passos, cb, u, alvo):
    ctx = Contexto(cb, u, alvo)
    for p in passos:
        p.executar(ctx)


def descrever(passos, u):
    linhas = []
    for p in passos:
        linhas += p.linhas(u)
    return linhas


# ---------------------------------------------------------------------- os blocos
class Dano:
    def __init__(self, mult, stat="atk", tipo="fisico", alcance="corpo", crit_extra=0.0, bonus=None, rotulo=None,
                 esquiva=True, em="alvo", depois=(), grimorio=None, nota=None):
        self.mult, self.stat, self.tipo, self.alcance = mult, stat, tipo, alcance
        self.crit_extra, self.bonus, self.rotulo, self.esquiva = crit_extra, bonus, rotulo, esquiva
        self.em, self.depois, self.grimorio, self.nota = em, list(depois), grimorio, nota

    def executar(self, ctx):
        cb, u = ctx.cb, ctx.u
        alvos = cb.inimigos_vivos() if self.em == "todos" else [ctx.alvo]
        for t in alvos:
            ctx.dano = cb.atacar(u, t, self.mult, tipo=self.tipo, alcance=self.alcance, stat=self.stat,
                                 crit_extra=self.crit_extra, bonus=valor(self.bonus, u) if self.bonus else 0,
                                 rotulo=self.rotulo, pode_esquivar=self.esquiva)
            ctx.atual = t
            for p in self.depois:
                p.executar(ctx)

    def linhas(self, u):
        from .grimorio import golpe
        rotulo = self.grimorio or ("Em cada inimigo" if self.em == "todos" else "Dano")
        nota = self.nota or (None if self.esquiva else "Não pode ser esquivado.")
        linha = golpe(u, self.mult, stat=self.stat, alcance=self.alcance, tipo=self.tipo,
                      bonus=valor(self.bonus, u) if self.bonus else 0.0,
                      bonus_txt=self.bonus.texto() if self.bonus else None, crit_extra=self.crit_extra,
                      rotulo=rotulo, nota=nota)
        return [linha] + descrever(self.depois, u)


class Se:
    CONDICOES = {
        "acertou": lambda ctx: ctx.dano,
        "vivo": lambda ctx: ctx.atual.vivo,
        "acertou_vivo": lambda ctx: ctx.dano and ctx.atual.vivo,
    }

    def __init__(self, condicao, *passos, mostrar=True):
        self.condicao, self.passos, self.mostrar = condicao, list(passos), mostrar

    def executar(self, ctx):
        if self.CONDICOES[self.condicao](ctx):
            for p in self.passos:
                p.executar(ctx)

    def linhas(self, u):
        return descrever(self.passos, u) if self.mostrar else []


def _efeito(texto):
    return {"tipo": "efeito", "texto": texto}


def _chance(c, texto):
    """'45% de chance de ' + texto, ou o texto com maiúscula quando é certo."""
    return f"{_pct(c)} de chance de {texto}" if c < 1 else texto[0].upper() + texto[1:]


# Como cada estado se descreve no Grimório (o catálogo completo de estados vem na Etapa C).
def _texto_estado(efeito, turnos, v, escala, chance, todos, rotulo):
    t = f"{turnos} turno{'s' if turnos != 1 else ''}"
    quem = "cada inimigo" if todos else "o alvo"
    origem = f" ({escala})" if escala else ""
    if efeito == "atordoado":
        if rotulo == "congelado":
            return _chance(chance, f"congelar {quem} (perde o próximo turno).")
        return _chance(chance, f"atordoar {quem} por {t}.")
    if efeito == "sangramento":
        return _chance(chance, f"sangramento: {_num(v)} por turno, {t}{origem}.")
    if efeito == "veneno":
        return _chance(chance, f"veneno: {_num(v)} por turno, {t}{origem}.")
    if efeito == "enfraquecido":
        return _chance(chance, f"enfraquecer {quem} por {t} (causa −25% de dano).")
    if efeito == "marcado":
        return f"{quem[0].upper() + quem[1:]} recebe +{_pct(v)} de dano de todos por {t}."
    if efeito == "maldito":
        return (f"{'Todos os inimigos' if todos else 'O alvo'}: {_num(v)} de dano por turno, {t}{origem}, "
                "e −40% de defesa.")
    return _chance(chance, f"{efeito} por {t}.")


class Aplicar:
    """Um estado num inimigo. `em`: "atual" (o alvo do golpe) ou "todos". `direto`: sem anúncio nem lance."""

    def __init__(self, efeito, turnos, valor=0, chance=1.0, rotulo=None, acumula=False, em="atual", direto=False):
        self.efeito, self.turnos, self.valor, self.chance = efeito, turnos, valor, chance
        self.rotulo, self.acumula, self.em, self.direto = rotulo, acumula, em, direto

    def executar(self, ctx):
        cb, u = ctx.cb, ctx.u
        alvos = cb.inimigos_vivos() if self.em == "todos" else [ctx.atual]
        for t in alvos:
            if self.direto:
                t.aplicar(self.efeito, self.turnos, valor(self.valor, u))
            else:
                cb.aplicar(t, self.efeito, self.turnos, valor=valor(self.valor, u), chance=self.chance,
                           rotulo=self.rotulo, acumula=self.acumula)

    def linhas(self, u):
        escala = self.valor.texto() if isinstance(self.valor, Escala) else ""
        return [_efeito(_texto_estado(self.efeito, self.turnos, valor(self.valor, u), escala, self.chance,
                                      self.em == "todos", self.rotulo))]


class Buff:
    """Um estado em você mesmo (silencioso: a frase vem num Dizer)."""

    def __init__(self, efeito, turnos, valor=0):
        self.efeito, self.turnos, self.valor = efeito, turnos, valor

    def executar(self, ctx):
        ctx.turnos = valor(self.turnos, ctx.u)
        ctx.u.aplicar(self.efeito, ctx.turnos, valor(self.valor, ctx.u))

    def linhas(self, u):
        t = valor(self.turnos, u)
        v = valor(self.valor, u)
        dur = f"{t} turno{'s' if t != 1 else ''}"
        if self.efeito == "guarda":
            return [_efeito(f"Dano recebido −{_pct(v)} por {dur}.")]
        if self.efeito == "fortalecido":
            return [_efeito(f"Seu dano +{_pct(v)} por {dur}.")]
        if self.efeito == "esquiva":
            base = min(bal.ESQUIVA_MAX_AGI, u.agi * bal.ESQUIVA_POR_AGI)
            return [_efeito(f"Esquiva +{_pct(v)} por {dur}: de {_pct(base)} para {_pct(min(bal.MAX_ESQUIVA, base + v))} "
                            f"(teto de {_pct(bal.MAX_ESQUIVA)}).")]
        if self.efeito == "furtivo":
            from .grimorio import mult_critico
            return [_efeito(f"O próximo ataque é crítico garantido de ×{_num(mult_critico(u, furtivo=True))}.")]
        return [_efeito(f"{self.efeito} por {dur}.")]


class Acender:
    """Queimadura do mago: duração e valor vêm do combate (Poder, piromante, Brasas); acumula em camadas."""

    def __init__(self, chance, chance_talento=None):
        self.chance, self.chance_talento = chance, chance_talento

    def _chance(self, u):
        return 1.0 if self.chance_talento and u.tal(self.chance_talento) else self.chance

    def executar(self, ctx):
        cb, u = ctx.cb, ctx.u
        cb.aplicar(ctx.atual, "queimadura", cb.duracao_queimadura(u), valor=cb.valor_queimadura(u),
                   chance=self._chance(u), acumula=True)

    def linhas(self, u):
        from .grimorio import _queimadura
        return [_queimadura(u, self._chance(u))]


class Roubo:
    """Cura uma fração do dano do último golpe e mostra o sangue voltando do alvo."""

    def __init__(self, fracao, rotulo):
        self.fracao, self.rotulo = fracao, rotulo

    def executar(self, ctx):
        u = ctx.u
        ctx.cura = u.curar(ctx.dano * valor(self.fracao, u))
        ctx.cb.curou(u, ctx.cura, "roubo", fonte=ctx.atual, rotulo=self.rotulo)

    def linhas(self, u):
        return [_efeito(f"Rouba {_pct(valor(self.fracao, u))} do dano causado como vida.")]


class CurarPeloDano:
    """Cura uma fração do dano causado (sem o sangue na tela: é luz, não roubo). `talento`: (id, +x por ponto)."""

    def __init__(self, fracao, talento=None):
        self.fracao, self.talento = fracao, talento

    def _fator(self, u):
        return 1 + self.talento[1] * u.tal(self.talento[0]) if self.talento else None

    def executar(self, ctx):
        u, f = ctx.u, self._fator(ctx.u)
        ctx.cura = u.curar(ctx.dano * self.fracao * f if f is not None else ctx.dano * self.fracao)

    def linhas(self, u):
        f = self._fator(u)
        return [_efeito(f"Cura {_pct(self.fracao * (f if f is not None else 1))} do dano causado.")]


class Curar:
    """Cura um valor (uma Escala sobre o herói), com bônus de talento opcional: (id, +x por ponto)."""

    def __init__(self, quanto, talento=None):
        self.quanto, self.talento = quanto, talento

    def _valor(self, u):
        v = valor(self.quanto, u)
        return v * (1 + self.talento[1] * u.tal(self.talento[0])) if self.talento else v

    def executar(self, ctx):
        ctx.cura = ctx.u.curar(self._valor(ctx.u))

    def linhas(self, u):
        origem = f" ({self.quanto.texto()})" if isinstance(self.quanto, Escala) else ""
        return [_efeito(f"Cura {int(self._valor(u))} de vida{origem}.")]


class LimparMales:
    def executar(self, ctx):
        ctx.u.limpar_negativos()

    def linhas(self, u):
        return [_efeito("Remove os males (veneno, sangramento, maldição, fraqueza).")]


class Dizer:
    """A frase da habilidade. `se="cura"`: só quando houve cura."""

    def __init__(self, texto, cor="", se=None):
        self.texto, self.cor, self.se = texto, cor, se

    def executar(self, ctx):
        if self.se == "cura" and not ctx.cura:
            return
        ctx.cb.dizer(self.texto.format(alvo=ctx.alvo.nome if ctx.alvo else "", cura=ctx.cura, turnos=ctx.turnos),
                     self.cor)

    def linhas(self, u):
        return []


class Salva:
    """Os golpes de dentro saem juntos na tela (o Tiro Duplo como rajada)."""

    def __init__(self, hab, *passos):
        self.hab, self.passos = hab, list(passos)

    def executar(self, ctx):
        with ctx.cb.salva(self.hab):
            for p in self.passos:
                p.executar(ctx)

    def linhas(self, u):
        return descrever(self.passos, u)


class Codigo:
    """Escape: um passo em código, com a descrição ao lado."""

    def __init__(self, fn, linhas=None):
        self.fn, self._linhas = fn, linhas

    def executar(self, ctx):
        self.fn(ctx)

    def linhas(self, u):
        return self._linhas(u) if self._linhas else []


def hab(nome, custo, alvo, desc, passos=None, fn=None, linhas=None, **extra):
    """A ficha de uma habilidade. Com `passos`, a execução e o Grimório saem dos mesmos blocos; com `fn` e
    `linhas`, a habilidade é escrita à mão (e as duas funções ficam juntas, logo abaixo)."""
    h = dict(nome=nome, custo=custo, alvo=alvo, desc=desc, **extra)
    if passos is not None:
        h["passos"] = passos
        h["fn"] = lambda cb, u, a, _p=passos: executar(_p, cb, u, a)
        h["linhas"] = lambda u, _p=passos: descrever(_p, u)
    else:
        h["fn"], h["linhas"] = fn, linhas
    return h


def crit_extra(h):
    """O maior bônus de crítico dos golpes da habilidade (para a ficha explicar a taxa real)."""
    maior = 0.0

    def ver(passos):
        nonlocal maior
        for p in passos:
            if isinstance(p, Dano):
                maior = max(maior, p.crit_extra)
                ver(p.depois)
            elif isinstance(p, (Se, Salva)):
                ver(p.passos)
    ver(h.get("passos", []))
    return maior or h.get("crit_extra", 0.0)


# ====================================================================== habilidades escritas à mão
# --- Guerreiro
GIROS_REDEMOINHO = 5


def _redemoinho(cb, u, alvo):
    """Cinco giros rápidos; cada um corta todos os inimigos ao mesmo tempo com 22% do golpe (110% no total)."""
    cb.dizer("Você gira a arma num arco brutal!", "ciano")
    total = {}
    for giro in range(GIROS_REDEMOINHO):
        vivos = cb.inimigos_vivos()
        if not vivos:
            break
        cb.lance("giro", de=cb.uid(u), n=giro + 1)
        for ini in vivos:
            total[ini] = total.get(ini, 0) + cb.atacar(u, ini, 1.1 / GIROS_REDEMOINHO, detalhar=False)
    partes = [f"{ini.nome} {d}" for ini, d in total.items()]
    if partes:
        cb.detalhe("Redemoinho: " + ", ".join(partes) + " de dano.", "amarelo")


def _linhas_redemoinho(u):
    from .grimorio import golpe
    return [golpe(u, 1.1, rotulo=f"Em cada inimigo ({GIROS_REDEMOINHO} giros de {_pct(1.1 / GIROS_REDEMOINHO)})")]


def _furia_cega(cb, u, alvo):
    custo = int(u.max_hp * 0.15)
    u.hp = max(1, u.hp - custo)
    u.aplicar("fortalecido", 3, 0.6)
    cb.dizer(f"Você morde o próprio lábio até sangrar e deixa a fúria tomar conta. (-{custo} vida, dano +60%)",
             "vermelho+negrito")
    cb.atacar(u, alvo, 1.3, rotulo="Fúria Cega")


def _linhas_furia_cega(u):
    from .grimorio import golpe
    return [_efeito(f"Custa {int(u.max_hp * 0.15)} de vida (15% da máxima)."), _efeito("Seu dano +60% por 3 turnos."),
            golpe(u, 1.3, extra=1.6, extra_txt="Fúria", rotulo="Golpe (já com a Fúria)")]


# --- Arqueiro
# A fera já ataca sozinha no turno dela; a ordem é o que ela não faz por conta própria, e muda com o animal.
ORDENS_FERA = {
    "urso": ("Proteger!", "O urso avança sobre o alvo (100%) e ruge: por 2 turnos, os inimigos atacam ele "
             "(chefes, metade das vezes), e ele recebe 30% menos dano."),
    "lobo": ("Dilacerar!", "O lobo morde a garganta do alvo (160%) e abre um sangramento forte por 4 turnos."),
    "falcao": ("Os olhos!", "O falcão mergulha nos olhos do alvo (100%, não pode ser esquivado): "
               "o alvo fica enfraquecido (−25% de dano) por 2 turnos."),
}
DESC_ORDEM = "Uma ordem que o animal não faz sozinho: o urso protege, o lobo dilacera, o falcão cega."


def _tipo_fera(u):
    fera = getattr(u, "companheiro", None)
    return fera.get("tipo") if isinstance(fera, dict) else getattr(fera, "tipo", None)


def _desc_ordem(u):
    tipo = _tipo_fera(u)
    return ORDENS_FERA[tipo][1] if tipo in ORDENS_FERA else DESC_ORDEM


def _comando_fera(cb, u, alvo):
    fera = cb.companheiro
    grito = ORDENS_FERA.get(fera.tipo, ("Agora!",))[0]
    cb.dizer(f"\"{grito}\" — {fera.nome} obedece na hora!", "ciano")
    if fera.tipo == "urso":
        cb.atacar(fera, alvo, 1.0, alcance="corpo", rotulo="Proteger")
        fera.aplicar("provocando", 2)
        fera.aplicar("guarda", 2, 0.3)
        cb.lance("buff", em=cb.uid(fera), efeitos=["provocando", "guarda"], rotulo="Provocando", hab="provocar")
        cb.dizer(f"{fera.nome} ruge e se põe na frente. Os inimigos só têm olhos para ele.", "ciano")
    elif fera.tipo == "lobo":
        if cb.atacar(fera, alvo, 1.6, alcance="corpo", rotulo="Dilacerar"):
            cb.aplicar(alvo, "sangramento", 4, valor=max(3, fera.atk * 0.55))
    else:
        if cb.atacar(fera, alvo, 1.0, alcance="corpo", rotulo="Os olhos", pode_esquivar=False):
            cb.aplicar(alvo, "enfraquecido", 2)


def _linhas_comando_fera(u):
    fera = getattr(u, "companheiro", None)
    if not fera:
        return [_efeito("Urso: provoca os inimigos e protege. Lobo: dilacera e faz sangrar. Falcão: cega (enfraquece).")]
    f = fera if isinstance(fera, dict) else {"nome": fera.nome, "atk": fera.atk, "tipo": fera.tipo}
    mult = 1.6 if f["tipo"] == "lobo" else 1.0
    linhas = [_efeito(f"{f['nome']} ataca: {int(f['atk'] * mult * 0.85)}–{int(f['atk'] * mult * 1.15)} de dano "
                      f"(ataque dele {_num(f['atk'])} × {round(mult * 100)}%).")]
    if f["tipo"] == "urso":
        linhas.append(_efeito("Provoca por 2 turnos: os inimigos atacam o urso (chefes, metade das vezes), "
                              "e ele recebe 30% menos dano."))
    elif f["tipo"] == "lobo":
        linhas.append(_efeito(f"Sangramento forte: {_num(max(3, f['atk'] * 0.55))} por turno, 4 turnos."))
    else:
        linhas.append(_efeito("Não pode ser esquivado. O alvo fica enfraquecido (−25% de dano) por 2 turnos."))
    return linhas


def _req_fera(cb):
    if not cb.companheiro or not cb.companheiro.vivo:
        return "Seu companheiro não está em condições de lutar."
    return None


def _curar_fera(ctx):
    cb = ctx.cb
    if cb.companheiro and cb.companheiro.vivo:
        cb.companheiro.curar(cb.companheiro.max_hp)
        cb.dizer(f"{cb.companheiro.nome} se ergue revigorado.", "verde")


def _execucao(cb, u, alvo):
    mult = 1.2
    if alvo.hp <= alvo.max_hp * 0.35:
        mult = 3.2
        cb.dizer("Você vê a abertura perfeita...", "magenta")
    cb.atacar(u, alvo, mult, alcance="distancia", crit_extra=0.2, rotulo="Execução")


def _linhas_execucao(u):
    from .grimorio import golpe
    return [golpe(u, 1.2, alcance="distancia", crit_extra=0.2, rotulo="Alvo com mais de 35% de vida"),
            golpe(u, 3.2, alcance="distancia", crit_extra=0.2, rotulo="Alvo abaixo de 35% de vida")]


# --- Mago
def ganho_meditar(u):
    return 6 + int(u.max_rec * 0.12)


def _meditar(cb, u, alvo):
    ganho = min(u.max_rec - u.rec, ganho_meditar(u))
    u.rec += ganho
    cb.dizer(f"Você fecha os olhos e respira fundo. (+{ganho} mana)", "azul")
    cb.recuperou(u, ganho, "Meditar")


def _valor_barreira(u):
    return int((u.max_hp * 0.15 + u.poder * 0.2) * (1.3 if u.tal("escudo_reflexo") else 1))


def _barreira(cb, u, alvo):
    v = _valor_barreira(u)
    u.remover("barreira")  # não acumula
    u.aplicar("barreira", 2 + u.tal("escudo_reflexo"), v)
    cb.dizer(f"Runas brilhantes giram ao seu redor. (absorve {v} de dano)", "azul")


def _combustao(cb, u, alvo):
    """Detona as chamas do alvo: tudo o que a queimadura ainda causaria vira dano agora, e mais um pouco.
    Sem chamas, é um estalo fraco. O jogo é acender (Bola de Fogo, Inferno) e escolher a hora de explodir."""
    restante = cb.restante_queimadura(alvo)
    camadas = cb.camadas(alvo)
    if restante:
        alvo.remover("queimadura")
        cb.dizer(f"As chamas em {alvo.nome} explodem{' de uma vez' if camadas > 1 else ''}!", "vermelho")
        cb.atacar(u, alvo, 1.0, tipo="fogo", alcance="distancia", stat="poder",
                  bonus=restante * (bal.COMBUSTAO_BASE + bal.COMBUSTAO_POR_CAMADA * camadas),
                  crit_extra=0.05 * camadas, rotulo=f"Combustão ×{camadas}" if camadas > 1 else "Combustão")
    else:
        cb.atacar(u, alvo, 0.8, tipo="fogo", alcance="distancia", stat="poder", rotulo="Combustão")


def _linhas_combustao(u):
    from .combate import Combate
    from .grimorio import golpe
    v = Combate.valor_queimadura(None, u)
    t = Combate.duracao_queimadura(None, u)
    cheio = v * t * bal.MAX_CHAMAS
    bonus = cheio * (bal.COMBUSTAO_BASE + bal.COMBUSTAO_POR_CAMADA * bal.MAX_CHAMAS)
    return [golpe(u, 0.8, stat="poder", alcance="distancia", tipo="fogo", rotulo="Sem chamas no alvo"),
            golpe(u, 1.0, stat="poder", alcance="distancia", tipo="fogo", bonus=bonus,
                  bonus_txt=f"{bal.MAX_CHAMAS} camadas recém-acesas", crit_extra=0.05 * bal.MAX_CHAMAS,
                  rotulo=f"Detonando {bal.MAX_CHAMAS} camadas novas",
                  nota="O que as chamas ainda queimariam × (1,6 + 0,2 por camada). Quanto mais camadas e "
                       "mais cedo, maior a explosão.")]


def _vida_servo(u):
    return (u.poder * 1.2 + 8) * (1 + 0.15 * u.tal("pacto_sombrio"))


def _erguer_servo(cb, u, alvo):
    servos = [a for a in cb.aliados if getattr(a, "tipo", "") == "servo" and a.vivo]
    maximo = 1 + u.tal("exercito")
    if len(servos) >= maximo:
        cb.dizer("Você não consegue controlar mais servos. O esforço se perde no ar.", "cinza")
        return
    origem = "dos ossos de um inimigo caído" if cb.mortos else "da própria terra"
    cb.dizer(f"Você ergue um servo esquelético {origem}!", "magenta")
    cb.invocar_aliado("Servo Esquelético", hp=int(_vida_servo(u)), atk=int(u.poder * 0.3) + 2, tipo="servo")


# ====================================================================== o catálogo
SANGRAMENTO = Escala(minimo=2, atk=0.3)

HABILIDADES = {
    # Guerreiro
    "golpe_pesado": hab("Golpe Pesado", 10, "inimigo", "170% de dano físico.",
                        [Dano(1.7, rotulo="Golpe Pesado")]),
    "erguer_escudo": hab("Erguer Escudo", 8, "proprio", "Reduz o dano recebido pela metade por 2 turnos.", [
        Buff("guarda", Tal(2, "muralha", 1), 0.5),
        Dizer("Você ergue o escudo e firma os pés. (dano recebido -50% por {turnos} turnos)", "ciano")]),
    "investida": hab("Investida", 12, "inimigo", "120% de dano, 45% de chance de atordoar.", [
        Dano(1.2, rotulo="Investida", depois=[Se("acertou", Aplicar("atordoado", 1, chance=0.45))])]),
    "grito_guerra": hab("Grito de Guerra", 14, "proprio", "+30% de dano por 3 turnos e enfraquece inimigos.", [
        Dizer("Você solta um grito de guerra que faz o chão tremer!", "ciano"),
        Buff("fortalecido", 3, 0.3),
        Aplicar("enfraquecido", 2, chance=0.8, em="todos")]),
    "golpe_sagrado": hab("Golpe Sagrado", 15, "inimigo", "Dano sagrado que cura você em 35% do dano.", [
        Dano(1.3, tipo="sagrado", bonus=Escala(poder=0.8), rotulo="Golpe Sagrado", depois=[
            Se("acertou", CurarPeloDano(0.35, talento=("luz_curativa", 0.25)),
               Dizer("A luz fecha suas feridas. (+{cura} vida)", "verde", se="cura"))])]),
    "prece": hab("Prece", 20, "proprio", "Cura 30% da vida + poder e remove males.", [
        Curar(Escala(max_hp=0.3, poder=1.5), talento=("luz_curativa", 0.25)),
        LimparMales(),
        Dizer("Você reza em voz baixa. Uma luz quente te envolve. (+{cura} vida, males removidos)", "verde")]),
    "julgamento": hab("Julgamento Divino", 28, "todos", "Luz sagrada atinge todos os inimigos.", [
        Dizer("Você ergue a arma aos céus. Colunas de luz caem sobre seus inimigos!", "amarelo+negrito"),
        Dano(1.2, tipo="sagrado", bonus=Escala(poder=1), alcance="distancia", esquiva=False, em="todos")]),
    "sede_sangue": hab("Sede de Sangue", 12, "inimigo", "140% de dano, rouba vida e causa sangramento.", [
        Dano(1.4, rotulo="Sede de Sangue", depois=[
            Se("acertou", Roubo(0.4, rotulo="Sede de Sangue"),
               Aplicar("sangramento", 3, valor=SANGRAMENTO),
               Dizer("Você bebe a fúria do golpe. (+{cura} vida)", "verde", se="cura"))])]),
    "redemoinho": hab("Redemoinho", 16, "todos", "Atinge todos os inimigos com 110% de dano.",
                      fn=_redemoinho, linhas=_linhas_redemoinho),
    "furia_cega": hab("Fúria Cega", 0, "inimigo", "Sacrifica 15% da vida: +60% de dano por 3 turnos e ataca.",
                      fn=_furia_cega, linhas=_linhas_furia_cega),
    # Arqueiro
    "tiro_certeiro": hab("Tiro Certeiro", 8, "inimigo", "170% de dano, +30% chance de crítico.",
                         [Dano(1.7, alcance="distancia", crit_extra=0.3, rotulo="Tiro Certeiro")], flechas=1),
    "marcar_presa": hab("Marcar Presa", 6, "inimigo", "O alvo recebe +25% de dano por 3 turnos.", [
        Aplicar("marcado", 3, 0.25, direto=True),
        Dizer("Você estuda os movimentos de {alvo} e encontra os pontos fracos. (+25% dano recebido)", "ciano")]),
    "chuva_flechas": hab("Chuva de Flechas", 14, "todos", "Atinge todos os inimigos (3 flechas).", [
        Dizer("Você dispara uma saraivada de flechas para o alto...", "ciano"),
        Dano(1.0, alcance="distancia", em="todos")], flechas=3),
    "passo_agil": hab("Passo Ágil", 6, "proprio", "+30% de esquiva por 2 turnos (a esquiva total não passa de 60%).", [
        Buff("esquiva", 2, 0.3),
        Dizer("Você se move em zigue-zague, difícil de acertar. (+30% esquiva, até o teto de 60%)", "ciano")]),
    "tiro_duplo": hab("Tiro Duplo", 10, "inimigo", "Dois disparos de 90%.", [
        Salva("tiro_duplo",  # as duas flechas saem quase juntas, numa rajada só
              Dano(0.9, alcance="distancia", rotulo="Tiro Duplo (1)", grimorio="Cada um dos 2 disparos"),
              Se("vivo", Dano(0.9, alcance="distancia", rotulo="Tiro Duplo (2)"), mostrar=False))], flechas=2),
    "comando_fera": hab("Ordem da Fera", 12, "inimigo", DESC_ORDEM, fn=_comando_fera, linhas=_linhas_comando_fera,
                        desc_fn=_desc_ordem, req=_req_fera),
    "furia_natureza": hab("Fúria da Natureza", 25, "todos", "130% em todos, sangramento e cura o companheiro.", [
        Dizer("Você assobia. A mata responde: vento, espinhos e flechas em uníssono!", "verde+negrito"),
        Dano(1.3, alcance="distancia", em="todos", depois=[
            Se("vivo", Aplicar("sangramento", 3, valor=SANGRAMENTO, chance=0.5))]),
        Codigo(_curar_fera, lambda u: [_efeito("Cura o companheiro animal por completo.")])], flechas=4),
    "desaparecer": hab("Desaparecer", 10, "proprio", "Próximo ataque é crítico devastador; +esquiva.", [
        Buff("furtivo", 3, 1),
        Buff("esquiva", 1, 0.5),
        Dizer("Você se funde às sombras. Seu próximo ataque será crítico.", "magenta")]),
    "flecha_envenenada": hab("Flecha Envenenada", 10, "inimigo", "Dano e veneno forte por 4 turnos.", [
        Dano(1.0, alcance="distancia", rotulo="Flecha Envenenada", depois=[
            Se("acertou", Aplicar("veneno", 4, valor=Escala(minimo=3, atk=0.45, agi=0.2)))])], flechas=1),
    "execucao": hab("Execução", 16, "inimigo", "320% de dano se o alvo estiver abaixo de 35% de vida.",
                    fn=_execucao, linhas=_linhas_execucao, flechas=1, crit_extra=0.2),
    # Mago
    "bola_fogo": hab("Bola de Fogo", 14, "inimigo",
                     "150% de dano de fogo; costuma acender o alvo (as chamas acumulam até 3 camadas).", [
                         Dano(1.5, tipo="fogo", alcance="distancia", stat="poder", rotulo="Bola de Fogo", depois=[
                             Se("acertou", Acender(0.6, chance_talento="ignicao"))])]),
    "meditar": hab("Meditar", 0, "proprio", "Recupera mana (6 + 12% do máximo).", fn=_meditar,
                   linhas=lambda u: [_efeito(f"Recupera {ganho_meditar(u)} de mana (6 + 12% do máximo). Gasta o turno.")],
                   desc_fn=lambda u: f"Recupera {ganho_meditar(u)} de mana (6 + 12% do máximo). Não custa nada, mas gasta o turno."),
    "lanca_gelo": hab("Lança de Gelo", 10, "inimigo", "130% de dano de gelo, pode congelar.", [
        Dano(1.3, tipo="gelo", alcance="distancia", stat="poder", rotulo="Lança de Gelo", depois=[
            Se("acertou", Aplicar("atordoado", 1, chance=0.35, rotulo="congelado"))])]),
    "barreira": hab("Barreira Arcana", 20, "proprio", "Escudo que absorve dano por 2 turnos (não acumula).",
                    fn=_barreira,
                    linhas=lambda u: [_efeito(f"Absorve {_valor_barreira(u)} de dano por {2 + u.tal('escudo_reflexo')} "
                                              "turnos (15% da vida máxima + Poder × 20%). Não acumula.")]),
    "inferno": hab("Inferno", 35, "todos", "60% de dano de fogo em todos (pode errar); pode acender cada um.", [
        Dizer("O chão se abre em chamas sob seus inimigos!", "vermelho+negrito"),
        Dano(0.6, tipo="fogo", alcance="distancia", stat="poder", em="todos", depois=[
            Se("acertou_vivo", Acender(0.5))])]),
    "combustao": hab("Combustão", 14, "inimigo", "Detona as chamas do alvo: o que a queimadura ainda causaria vira "
                     "dano na hora (mais forte com várias camadas).", fn=_combustao, linhas=_linhas_combustao),
    "fenix": hab("Fênix", 40, "inimigo", "250% de dano de fogo e cura 20% da vida.", [
        Dizer("Asas de fogo se abrem às suas costas. Você se torna a própria chama!", "amarelo+negrito"),
        Dano(2.5, tipo="fogo", alcance="distancia", stat="poder", rotulo="Fênix"),
        Curar(Escala(max_hp=0.2)),
        Dizer("O fogo renova sua carne. (+{cura} vida)", "verde", se="cura")]),
    "drenar_vida": hab("Drenar Vida", 14, "inimigo", "Dano sombrio que cura 40% do causado.", [
        Dano(1.2, tipo="sombra", alcance="distancia", stat="poder", rotulo="Drenar Vida", depois=[
            Se("acertou", Roubo(Tal(0.4, "pacto_sombrio", 0.1), rotulo="Drenar Vida"),
               Dizer("A vitalidade roubada flui para você. (+{cura} vida)", "verde", se="cura"))])]),
    "erguer_servo": hab("Erguer Servo", 22, "proprio", "Invoca um esqueleto aliado (máx. 1, mais com talentos).",
                        fn=_erguer_servo,
                        linhas=lambda u: [_efeito(f"Invoca um servo com {int(_vida_servo(u))} de vida e "
                                                  f"{int(u.poder * 0.3) + 2} de ataque (no máximo "
                                                  f"{1 + u.tal('exercito')} ao mesmo tempo).")]),
    "maldicao": hab("Maldição", 18, "todos", "Amaldiçoa todos: dano contínuo e -40% de defesa.", [
        Aplicar("maldito", 4, valor=Escala(minimo=3, poder=0.4), em="todos"),
        Dizer("Você pronuncia palavras que não deveriam existir. Seus inimigos murcham.", "magenta")]),
}


def descricao_habilidade(h_id, u):
    """A descrição com os números do herói, quando a habilidade sabe calculá-los (ex.: quanto o Meditar devolve)."""
    h = HABILIDADES[h_id]
    return h["desc_fn"](u) if h.get("desc_fn") else h["desc"]
