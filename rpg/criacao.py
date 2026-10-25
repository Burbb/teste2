"""A criação do personagem numa tela só (a tela gráfica: app/criacao.js). O motor manda tudo o que ela mostra, pronto
(os textos, as classes com o ataque, o recurso e as especializações, os modos, o tutorial), e confere o que volta. A
tela anda pelas etapas (Nome → Classe → Modo) e só responde no "Começar campanha" (ou no Voltar da primeira etapa). A
interface de texto continua com as perguntas de sempre (Jogo.novo_jogo)."""

from . import balanceamento as bal
from . import campanha
from .classes import CLASSES, SPECS

NOME_PADRAO = "Aventureiro"
NOME_MAX = 40
ALCANCE = {"corpo": "corpo a corpo", "distancia": "à distância"}
# Se você cair: as consequências da derrota em cada modo (Jogo.resgate e a morte do hardcore); o Resgate é o padrão.
MODOS = [
    {"id": "resgate", "nome": "Resgate", "linhas": ["Alguém da vila te encontra e cuida de você.",
                                                    "Custa parte do ouro e dois dias."]},
    {"id": "hardcore", "nome": "Hardcore", "linhas": ["A morte é permanente.", "O save é apagado."]},
]


def dados(regiao=campanha.INICIO):
    """Tudo o que a tela da criação mostra. O recurso é o do nível 1 (o total e o que a luta devolve por rodada)."""
    classes = [{
        "id": c, "nome": d["nome"], "frase": d["frase"],
        "ataque": {"nome": d["ataque"][0], "alcance": ALCANCE[d["ataque"][1]], "icone": d["icone_ataque"]},
        "recurso": {"nome": d["recurso"], "total": d["base"]["max_rec"], "regen": d["base"]["regen"]},
        "specs": [SPECS[s]["nome"] for s in d["specs"]], "nivel_spec": bal.NIVEL_ESPECIALIZACAO,
    } for c, d in CLASSES.items()]
    return {
        "regiao": campanha.nome(regiao),
        "nome": {"pergunta": "Qual é o seu nome, aventureiro(a)?", "padrao": NOME_PADRAO, "max": NOME_MAX},
        "classes": classes,
        "modo": {"pergunta": "Se você cair (em combate, de fome ou de infecção):", "padrao": "resgate", "opcoes": MODOS},
        "tutorial": {"rotulo": "Mostrar tutorial", "marcada": True,
                     "nota": "Orientações curtas nas primeiras ações. A Ajuda (F1) desliga ou religa."},
    }


def conferir(resposta):
    """A resposta da tela ({"nome", "classe", "modo", "tutorial"}) como (nome, classe, hardcore, tutorial), ou None se
    não serve (a tela pergunta de novo). O nome em branco vira o padrão; mais longo que o campo, é cortado."""
    if not isinstance(resposta, dict) or resposta.get("classe") not in CLASSES:
        return None
    if resposta.get("modo") not in {m["id"] for m in MODOS}:
        return None
    nome = str(resposta.get("nome") or "").strip()[:NOME_MAX].strip() or NOME_PADRAO
    return nome, resposta["classe"], resposta["modo"] == "hardcore", bool(resposta.get("tutorial", True))
