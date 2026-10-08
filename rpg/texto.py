"""Geração procedural de nomes e pequenas utilidades de texto."""

import re

INICIOS = [
    "Ar", "Bel", "Cor", "Dra", "El", "Fen", "Gal", "Hal", "Ir", "Jor", "Kal", "Lor",
    "Mor", "Nar", "Or", "Par", "Quel", "Ral", "Sar", "Tor", "Ul", "Val", "Xar", "Zor",
    "Vhar", "Ser", "Bran", "Thal", "Gor", "Ves", "Ash", "Myr",
]
MEIOS = ["a", "e", "i", "o", "an", "en", "ar", "or", "il", "ul", "ae", "ir", "ag"]
FINS = [
    "dor", "nar", "ric", "mus", "thas", "goth", "wen", "lia", "ra", "vek", "mir",
    "dan", "ros", "zar", "nil", "ok", "eth", "ion", "kra", "mund", "ys",
]

NOMES_M = [
    "Aldo", "Bento", "Caio", "Dário", "Edgar", "Fausto", "Gaspar", "Heitor", "Ícaro",
    "Joaquim", "Lauro", "Mateus", "Nestor", "Otávio", "Rufino", "Silvano", "Tobias",
    "Vicente", "Baltasar", "Custódio", "Elias", "Florêncio",
]
NOMES_F = [
    "Alba", "Benta", "Clara", "Dália", "Elvira", "Flora", "Glória", "Helena", "Inês",
    "Joana", "Lúcia", "Marta", "Nina", "Olívia", "Rosa", "Sabina", "Teresa", "Violeta",
    "Amélia", "Brites", "Constança", "Isaura",
]
PROFISSOES = [
    ("ferreiro", "ferreira"), ("caçador", "caçadora"), ("mercador", "mercadora"),
    ("pastor", "pastora"), ("escriba", "escriba"), ("peregrino", "peregrina"),
    ("lenhador", "lenhadora"), ("curandeiro", "curandeira"), ("menestrel", "menestrel"),
    ("soldado desertor", "soldada desertora"), ("alquimista", "alquimista"),
    ("pescador", "pescadora"), ("monge", "monja"), ("cartógrafo", "cartógrafa"),
]
TRACOS = [
    "de olhar desconfiado", "com uma cicatriz no queixo", "que fala baixo demais",
    "de sorriso fácil", "com as mãos trêmulas", "que cheira a fumaça", "de voz rouca",
    "com um tapa-olho", "que não para de olhar para trás",
    "com roupas finas demais para a estrada", "de barba trançada",
    "com um corvo no ombro", "que masca raízes o tempo todo", "de olhos muito claros",
]

NUMEROS = {1: ("um", "uma"), 2: ("dois", "duas"), 3: ("três", "três"), 4: ("quatro", "quatro")}


def nome_proprio(rng, partes=None):
    partes = partes or rng.choice([2, 2, 3])
    nome = rng.choice(INICIOS)
    for _ in range(partes - 2):
        nome += rng.choice(MEIOS)
    nome += rng.choice(FINS)
    return nome[0].upper() + nome[1:].lower()


def npc(rng):
    g = rng.choice("mf")
    prof = rng.choice(PROFISSOES)
    return {
        "nome": rng.choice(NOMES_M if g == "m" else NOMES_F),
        "g": g,
        "prof": prof[0] if g == "m" else prof[1],
        "traco": rng.choice(TRACOS),
        "o": "o" if g == "m" else "a",
        "um": "um" if g == "m" else "uma",
        "ele": "ele" if g == "m" else "ela",
        "dele": "dele" if g == "m" else "dela",
    }


def numero(n, g="m"):
    if n in NUMEROS:
        return NUMEROS[n][0 if g == "m" else 1]
    return str(n)


def artigo(g, definido=True):
    if definido:
        return "o" if g == "m" else "a"
    return "um" if g == "m" else "uma"


def lista_natural(itens):
    itens = list(itens)
    if not itens:
        return ""
    if len(itens) == 1:
        return itens[0]
    return ", ".join(itens[:-1]) + " e " + itens[-1]


PLURAL_ADJ = {"feroz": "ferozes", "ágil": "ágeis", "ancião": "anciões", "anciã": "anciãs"}


def plural_adjetivo(adj):
    return PLURAL_ADJ.get(adj, adj + "s")


def descrever_grupo(inimigos):
    """'dois lobos e uma aranha gigante feroz'; 'duas harpias flamejantes' (e não 'uma harpia flamejante e uma
    harpia flamejante')."""
    from .dados import AFIXOS
    grupos, unicos = {}, []
    for ini in inimigos:
        if ini.unico:
            unicos.append(ini.desc)
        else:
            grupos.setdefault((ini.familia, ini.afixo), []).append(ini)
    partes = []
    for (_, afixo), lista in grupos.items():
        ini = lista[0]
        if len(lista) == 1:
            partes.append(ini.desc)
        else:
            adj = f" {plural_adjetivo(AFIXOS[afixo][ini.g])}" if afixo else ""
            partes.append(f"{numero(len(lista), ini.g)} {ini.plural}{adj}")
    return lista_natural(partes + unicos)


# Formas que concordam com o grupo: um homem, uma mulher, homens (ou misto), só mulheres.
_FORMAS = {"eles": ("ele", "ela", "eles", "elas"), "os": ("o", "a", "os", "as"),
           "deles": ("dele", "dela", "deles", "delas"), "-los": ("-lo", "-la", "-los", "-las")}


def concordar(frase, grupo, **campos):
    """A frase concordando em número e gênero com quem está em cena, como nas localizações profissionais (que
    marcam a frase em vez de escrever "eles" para um lobo sozinho). Marcadores:

        {eles} ele/ela/eles/elas   {os} o/a/os/as   {deles} dele/dela/deles/delas   {-los} -lo/-la/-los/-las
        {vira|viram}  a forma do singular ou do plural (um lado pode ficar vazio: {| ao mesmo tempo})
        {grupo}       "dois lobos e uma aranha gigante"     {nome}  qualquer campo passado por nome

    Inicial maiúscula no marcador ({Eles}, {Grupo}) sai com maiúscula. O plural é feminino só se todos forem."""
    um = len(grupo) == 1
    i = (0 if um else 2) + (1 if all(getattr(e, "g", "m") == "f" for e in grupo) else 0)

    def trocar(m):
        chave = m.group(1)
        if "|" in chave:
            return chave.split("|")[0 if um else 1]
        if chave in campos:
            return str(campos[chave])
        forma = descrever_grupo(grupo) if chave.lower() == "grupo" else _FORMAS[chave.lower()][i]
        return maiuscula(forma) if chave[0].isupper() else forma
    return re.sub(r"\{([^{}]*)\}", trocar, frase)


def plural(n, um, varios=None):
    """'1 trecho', '3 trechos', '0 trechos': o plural certo, nunca com o s entre parênteses. Quando o plural não é só
    acrescentar s, ele vai junto: plural(n, "flecha intacta", "flechas intactas")."""
    return f"{n} {um if n == 1 else varios or um + 's'}"


def estrelas(n, total=5):
    return "★" * n + "☆" * (total - n)


def aposto(nome):
    """'Irdor, a Bruxa Afogada' vira 'Irdor, a Bruxa Afogada,' para continuar a frase corretamente."""
    return f"{nome}," if "," in nome else nome


def maiuscula(texto):
    return texto[:1].upper() + texto[1:] if texto else texto
