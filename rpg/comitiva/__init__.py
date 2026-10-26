"""Comitiva: companheiros de jornada com valores, opinião, história própria e lugar no combate.

Cada companheiro tem VALORES (o que admira e o que despreza). As escolhas do
jogador carregam ETIQUETAS (misericórdia, ganância, magia proibida...). Quando
você escolhe, cada companheiro reage conforme seus valores: a APROVAÇÃO sobe ou
desce, e às vezes ele diz o que pensa. Aprovação alta deixa o companheiro mais
forte e abre a parte final da história dele; aprovação baixa demais o faz ir
embora (e alguns não vão em paz).

Os três companheiros discordam entre si de propósito: agradar a todos é
impossível, e é isso que dá peso às escolhas.

Em partes:

    catalogo.py   quem são os companheiros, as reações às escolhas, os gritos da luta
    grupo.py      quem está no grupo, entrar e sair, aprovação, o que o tempo cobra
    conversas.py  as conversas de cada um, as falas da noite, o carinho no animal
    luta.py       a comitiva na luta (o kit de cada companheiro, que você controla na vez dele: KITS)
    fogueira.py   a cena do acampamento e o menu da comitiva
    tela.py       o que a tela mostra (estado, explicação da aprovação)
    ficha.py      o equipamento e os atributos de cada um; vestir, tirar e trocar peças (a regra única)

Quem usa importa daqui (`from rpg import comitiva`; `comitiva.reagir(...)`).
"""

from .catalogo import LIMITE, COMPANHEIROS, REACOES, NIVEIS, GRITOS, CARINHO, ATALHOS_FOGUEIRA
from .grupo import (
    dados, membros, membro, presente, AUSENCIAS, fora, junto, reserva, na_reserva, disponivel, nome, flexao, nivel, lealdade, atributos,
    atualizar_vida_maxima, recrutar, sair, oferecer_vaga, para_acampamento, chamar, dispensar, mudar_aprovacao,
    reagir, reagir_escolha, verificar_partidas, partir, amanhecer, depois_do_amanhecer, comer, pagar_soldo,
    soldo_devido,
    parte_do_xp, descansar, cuidar)
from .conversas import CONVERSAS, AVULSAS, conversa, avulsa, proxima_conversa, conversar, falar, noite, fala_ociosa, carinho
from .tela import explicar_aprovacao, estado
from .luta import preparar_combate, alvo_inimigo, gritar, KITS, ATAQUE, encerrar_combate
from .fogueira import fogueira, menu
from . import ficha

__all__ = ["LIMITE", "COMPANHEIROS", "REACOES", "NIVEIS", "GRITOS", "CARINHO", "ATALHOS_FOGUEIRA", "dados", "membros",
           "membro", "presente", "AUSENCIAS", "fora", "junto", "reserva", "na_reserva", "disponivel", "nome", "flexao", "nivel", "lealdade", "atributos",
           "atualizar_vida_maxima", "recrutar", "sair", "oferecer_vaga", "para_acampamento", "chamar", "dispensar",
           "mudar_aprovacao", "reagir", "reagir_escolha", "verificar_partidas", "partir", "amanhecer", "depois_do_amanhecer",
           "comer", "pagar_soldo", "soldo_devido", "parte_do_xp", "descansar", "cuidar", "CONVERSAS", "AVULSAS", "conversa", "avulsa", "proxima_conversa",
           "conversar", "falar", "noite", "fala_ociosa", "carinho", "explicar_aprovacao", "estado", "preparar_combate",
           "alvo_inimigo", "gritar", "KITS", "ATAQUE", "encerrar_combate", "fogueira", "menu", "ficha"]
