"""Versões do formato do save e as migrações entre elas.

Cada vez que o formato muda (campo novo, campo renomeado, estrutura diferente), sobe-se VERSAO_SAVE e
acrescenta-se uma função `_vN_para_vN1` em MIGRACOES. Um save antigo passa por todas, em ordem, até
chegar à versão atual; assim nenhum código do jogo precisa se defender de saves velhos.
"""

VERSAO_SAVE = 4

# Tudo o que o estado da partida guarda além do jogador, da semente e do gerador aleatório.
CAMPOS_SAVE = ("mundo", "dia", "periodo", "clima", "passos", "flags", "historico", "contagem",
               "impulsos", "sementes", "rumores", "contratos", "ofertas", "lojas", "nemesis", "forcados",
               "proximo_id", "estatisticas", "hardcore", "bestiario", "lendas", "registro",
               "arquivo_run", "comitiva", "reserva")

ESPACOS_EQUIP = ("cabeca", "amuleto", "armadura", "maos", "arma", "secundaria", "pernas", "pes", "anel1", "anel2")


class SaveIncompativel(Exception):
    """O save é de uma versão do jogo mais nova do que esta (ou não é um save)."""


def _v1_para_v2(d):
    """Junta num lugar só as correções que o carregamento fazia aos poucos para saves antigos."""
    for loc in d["mundo"]["locais"]:  # mapas antigos não tinham coordenadas
        loc.setdefault("x", 0.03 + 0.9 * (loc["perigo"] - 1) / 4 if loc["id"] else 0.03)
        loc.setdefault("y", 0.08 + 0.84 * ((loc["id"] * 5) % 11) / 10)
    j = d["jogador"]
    j.setdefault("talentos", {})
    j.setdefault("pontos_talento", max(0, j["nivel"] - 1))
    j.setdefault("provisoes", 4)
    j.setdefault("fome", 0)
    j.setdefault("ferimentos", [])
    for s in ESPACOS_EQUIP:  # saves antigos tinham só arma, armadura e amuleto
        j["equip"].setdefault(s, None)
    d.setdefault("comitiva", [])
    d.setdefault("reserva", [])
    return d


def _v2_para_v3(d):
    """A corrupção do reino saiu do jogo (1.16)."""
    d.pop("corrupcao", None)
    return d


def _v3_para_v4(d):
    """O baú da sacristia passou a ser recolhido pela ação (1.85.0). Quem venceu a sacristia antes já o recebeu na
    vitória, aberto ou gasto depois: fica "recolhido", para não vir outro (não se deduz pela bolsa)."""
    m = ((d.get("mundo") or {}).get("missoes") or {}).get("febre_do_turvo")
    if m and (m.get("etapa") in ("ossuario", "fundo", "retorno") or m.get("desfecho") or m.get("concluida")):
        m.setdefault("bau", "recolhido")
    return d


MIGRACOES = {1: _v1_para_v2, 2: _v2_para_v3, 3: _v3_para_v4}


def migrar(dados):
    """Leva um save de qualquer versão antiga até VERSAO_SAVE."""
    if not isinstance(dados, dict) or "jogador" not in dados or "seed" not in dados:
        raise SaveIncompativel("Este arquivo não é um save de Crônicas da Fenda.")
    versao = dados.get("versao", 1)
    if versao > VERSAO_SAVE:
        raise SaveIncompativel(f"Este save é de uma versão mais nova do jogo (formato {versao}; "
                               f"este jogo lê até o {VERSAO_SAVE}). Atualize o jogo para continuar.")
    while versao < VERSAO_SAVE:
        dados = MIGRACOES[versao](dados)
        versao += 1
    dados["versao"] = versao
    return dados
