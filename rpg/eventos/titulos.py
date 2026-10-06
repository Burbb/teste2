"""Títulos de cena de cada evento (aparecem no topo da página)."""

TITULOS = {
    "odete_na_estrada": "A irmã de vigília", "odete_a_mae": "A mãe de Thomas", "morel_na_taverna": "O cão de ferro",
    "teodoro_ruivo": "A Varn Bridge", "yara_na_fogueira": "A fogueira", "yara_sonambula": "Pés descalços",
    "yara_circulo_negro": "O círculo negro", "discussao_fe_e_bruxaria": "Fé e bruxaria", "discussao_pao": "O pão",
    "discussao_mao_na_espada": "A mão na espada",
    "encontro_hostil": "Algo se move", "nemesis_retorna": "O caçador volta", "alvo_contrato": "A presa do contrato",
    "viajante_ferido": "Sangue na estrada", "viajante_grato": "Um rosto conhecido",
    "mercador_ambulante": "A carroça colorida", "mercador_golpista": "O golpista atolado",
    "bau_abandonado": "Um baú esquecido", "santuario_antigo": "O santuário", "acampamento_bandidos": "Fumaça no mato",
    "bandido_poupado": "Velhos conhecidos", "crianca_perdida": "Choro na trilha",
    "cadaver_aventureiro": "Quem veio antes", "ervas_medicinais": "Ervas", "jogo_de_dados": "Dados e fogueira",
    "visao_do_vazio": "O olho do Vazio", "ladrao_fugitivo": "O ladrão", "cacadores_de_recompensa": "Cabeça a prêmio",
    "pacote_suspeito": "A encomenda", "sinais_do_guardiao": "Rastros de algo enorme", "peregrinos": "Peregrinos",
    "refugiados": "Os que fogem", "caravana_atacada": "Caravana sob ataque", "tesouro_escondido": "A pedra dos três riscos",
    "fera_lendaria": "A fera das histórias", "mercador_raro": "A tenda roxa", "tumulo_do_heroi": "Um túmulo",
    "circulo_de_fadas": "O anel de cogumelos", "colmeia_selvagem": "A colmeia", "luzes_fantasmas": "Luzes na água",
    "cabana_da_bruxa": "A cabana sobre palafitas", "avalanche": "Avalanche", "ninho_de_grifo": "O ninho",
    "espantalho": "O espantalho", "fazenda_em_apuros": "A fazenda", "armadilha_antiga": "Armadilha",
    "biblioteca_ruida": "A biblioteca em ruínas", "golem_adormecido": "O golem adormecido",
    "abrigo_da_tempestade": "Abrigo", "sussurros_na_nevoa": "Sussurros na névoa", "eco_do_vazio": "Ecos",
    "encruzilhada_guerreiro": "A encruzilhada", "encruzilhada_arqueiro": "A encruzilhada",
    "encruzilhada_mago": "A encruzilhada", "duelo_de_honra": "Duelo na ponte", "veterano_cicatrizes": "O veterano",
    "ferreiro_itinerante": "A bigorna sobre rodas", "aldeia_assombrada": "A aldeia sem luz",
    "os_enfermos": "A casa marcada", "tentacao_do_juramento": "A oferta", "chamado_do_sangue": "O chamado do sangue",
    "furia_noturna": "Fúria", "queda_de_braco": "Queda de braço", "rastro_de_caca": "Rastro fresco",
    "madeira_para_flechas": "Freixos", "falcao_mensageiro": "O falcão", "corda_encharcada": "Corda molhada",
    "competicao_de_tiro": "A competição", "companheiro_fareja": "Faro", "circulo_dos_druidas": "O círculo de pedras",
    "contrato_da_irmandade": "Penas negras", "irmandade_cobra": "A Irmandade cobra", "bolsos_alheios": "Bolsos alheios",
    "anomalia_arcana": "Anomalia", "grimorio_perdido": "O livro que pulsa", "linha_ley": "Linha ley",
    "aprendiz_em_apuros": "O aprendiz", "aprendiz_grato": "Mestre!", "cacadores_de_bruxas": "Tochas e forcados",
    "elemental_selvagem": "Fogo selvagem", "incendio": "Incêndio", "cemiterio_antigo": "O cemitério esquecido",
    "aldeoes_temerosos": "Portas que se fecham", "olhos_na_escuridao": "Olhos na escuridão",
    "visitante_misterioso": "Um visitante", "ladrao_noturno": "Passos no escuro", "ladrao_redimido": "Um aviso",
    "sonho_profetico": "Um sonho", "ceu_estrelado": "Estrelas", "sussurros_do_vazio": "A voz na fogueira",
    "companheiro_de_vigia": "Vigília", "briga_de_taverna": "Briga na taverna", "festival": "Candlewatch",
    "pregador_do_vazio": "O pregador", "familia_grata": "Gratidão", "mendigo_misterioso": "O mendigo",
    "guarda_desconfiado": "Guardas", "pedido_de_socorro": "Um pedido",
}


def titulo(evento_id):
    return TITULOS.get(evento_id, evento_id.replace("_", " ").capitalize())
