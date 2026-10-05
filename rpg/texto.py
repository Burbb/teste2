"""Geração procedural de nomes e pequenas utilidades de texto."""

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


def descrever_grupo(inimigos):
    """'dois lobos e uma aranha gigante feroz'."""
    simples = {}
    partes = []
    for ini in inimigos:
        if ini.unico or ini.afixo:
            partes.append(ini.desc)
        else:
            chave = ini.familia
            simples.setdefault(chave, []).append(ini)
    for lista in simples.values():
        ini = lista[0]
        if len(lista) == 1:
            partes.insert(0, ini.desc)
        else:
            partes.insert(0, f"{numero(len(lista), ini.g)} {ini.plural}")
    return lista_natural(partes)


def estrelas(n, total=5):
    return "★" * n + "☆" * (total - n)


def aposto(nome):
    """'Irdor, a Bruxa Afogada' vira 'Irdor, a Bruxa Afogada,' para continuar a frase corretamente."""
    return f"{nome}," if "," in nome else nome


def maiuscula(texto):
    return texto[:1].upper() + texto[1:] if texto else texto
