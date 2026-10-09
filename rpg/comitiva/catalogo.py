"""Os companheiros (quem são, o que valorizam, o que dizem), as reações às escolhas e os gritos da luta."""



LIMITE = 2  # companheiros ao mesmo tempo (fora o animal do patrulheiro)


COMPANHEIROS = {
    "odete": dict(
        nome="Irmã Odette", curto="Odette", g="f", titulo="clériga desertora", papel="cura",
        preces=2,  # curas por luta (luta.py: a ação dela)
        desc="Fugiu da catedral na noite em que a Fenda se abriu. Fecha feridas; não perdoa crueldade.",
        base=dict(hp=30, atk=4, poder=6, defesa=3, agi=4), cresc=dict(hp=6, atk=0.6, poder=1.2, defesa=0.6),
        valores={"misericordia": 3, "generosidade": 2, "fe": 3, "honestidade": 2, "purificar": 2, "honra": 1,
                 "diplomacia": 1, "crueldade": -4, "ganancia": -2, "trapaca": -2, "sacrilegio": -4,
                 "magia_proibida": -3, "violencia": -1},
        aprova={
            "misericordia": "Odette toca seu braço de leve. \"Ainda existe gente boa neste reino. Às vezes eu esqueço.\"",
            "generosidade": "\"Moedas não descem com a gente para a cova\", diz Odette, quase sorrindo.",
            "fe": "Odette reza junto, baixinho. Pela primeira vez em dias, a voz dela não treme.",
            "honestidade": "\"A verdade custa caro\", diz Odette. \"Mas é a única moeda que não enferruja.\"",
            "purificar": "Odette faz o sinal da Luz sobre as cinzas. \"Que fique queimado.\"",
            None: "Odette acena com a cabeça, em silêncio.",
        },
        desaprova={
            "crueldade": "Odette desvia o olhar. \"Eu fugi de muita coisa. Não vou fugir de dizer que isso foi errado.\"",
            "ganancia": "\"Ouro\", Odette cospe a palavra. \"Foi por ouro que o bispo vendeu as relíquias. Lembra do que veio depois?\"",
            "sacrilegio": "Odette empalidece. \"Os mortos não se defendem. Por isso mesmo merecem respeito.\"",
            "magia_proibida": "\"Isso é a voz da Fenda\", sussurra Odette, apertando o rosário. \"Eu já ouvi essa voz. Não a deixe entrar.\"",
            "trapaca": "Odette não diz nada. Mas não olha mais para você pelo resto do caminho.",
            "violencia": "\"Precisava disso?\", pergunta Odette, limpando o sangue de alguém que nem conhecia.",
            None: "Odette aperta os lábios.",
        },
        partida="Odette para no meio da estrada. \"Prometi a mim mesma que nunca mais ficaria parada vendo o mal "
                "acontecer. Ficar com você é ficar parada.\" Ela se vira e vai embora, sem pressa, sem olhar para trás.",
        ocioso={
            "alto": ["Odette remenda sua capa sem que você peça. \"Assim o frio entra menos. Não discuta.\"",
                     "\"Quando tudo isso acabar\", diz Odette, \"quero ver uma igreja com as portas abertas. Só isso.\""],
            "medio": ["Odette conta as bandagens que restam. \"Poucas. Tente não sangrar tanto.\"",
                      "Odette olha para o norte, para onde ficava a catedral. Não diz nada."],
            "baixo": ["Odette responde com uma palavra só. Depois, nem isso.",
                      "\"Estou aqui pelos feridos que encontramos no caminho\", diz Odette. \"Não por você.\""],
        },
    ),
    "morel": dict(
        nome="Bastian Morel", curto="Morel", g="m", titulo="mercenário", papel="escudo",
        protege=dict(chance=0.3, leal=0.4, a_partir=45),  # chama a atenção dos inimigos (mais quando leal)
        desc="Ex-capitão de uma companhia que não existe mais. Luta por ouro, segura a linha e odeia covardes.",
        base=dict(hp=52, atk=8, poder=0, defesa=6, agi=3), cresc=dict(hp=9, atk=1.5, poder=0, defesa=1.0),
        valores={"coragem": 3, "pragmatismo": 2, "honra": 2, "ganancia": 1, "violencia": 1, "fuga": -4,
                 "cautela": -1, "generosidade": -1, "autoridade": -2, "trapaca": -1, "fe": -1},
        aprova={
            "coragem": "Morel solta uma gargalhada rouca. \"Isso! Os Cães de Ferro teriam gostado de você.\"",
            "pragmatismo": "\"Cabeça fria\", aprova Morel. \"Herói morto não paga dívida nenhuma.\"",
            "ganancia": "Morel conta as moedas junto com você, de olho. \"Agora sim estamos conversando.\"",
            "honra": "Morel bate o punho no peito, à moda antiga. \"Palavra dada. Ainda existe isso.\"",
            "violencia": "\"Rápido e sujo\", diz Morel, limpando a lâmina. \"Do jeito que funciona.\"",
            None: "Morel resmunga algo que soa como aprovação.",
        },
        desaprova={
            "fuga": "\"Correndo de novo?\" Morel não esconde o desprezo. \"Conheço esse caminho. Ele não acaba bem.\"",
            "cautela": "Morel boceja, alto. \"Se for para fugir de toda sombra, melhor virar pastor de cabras.\"",
            "generosidade": "\"Caridade não enche a barriga de ninguém\", resmunga Morel. \"Muito menos a minha.\"",
            "autoridade": "Morel cospe no chão. \"Guarda, nobre, bispo. Tudo a mesma laia. Nunca dobre o joelho.\"",
            "fe": "\"Rezar\", Morel ri sem graça. \"Rezei a noite toda na Ponte de Varn. Ninguém respondeu.\"",
            "trapaca": "\"Trapaça é para quem não sabe lutar\", diz Morel, e se afasta um passo.",
            None: "Morel cruza os braços.",
        },
        partida="Morel pendura a espada nas costas e cospe no chão. \"Já servi a gente pior. Mas não por esse "
                "preço.\" Ele se vai, e leva consigo o que acha que você lhe deve.",
        ocioso={
            "alto": ["Morel afia a sua lâmina junto com a dele, sem perguntar. \"Fio cego mata o dono primeiro.\"",
                     "\"Sabe\", diz Morel, olhando o fogo, \"faz tempo que não confio as costas a ninguém.\""],
            "medio": ["Morel conta e reconta as moedas da bolsa, como quem reza.",
                      "\"Mais um dia vivo\", diz Morel, e bebe à saúde de ninguém."],
            "baixo": ["Morel dorme com a mão no punho da espada. Virado para você.",
                      "\"O soldo\", diz Morel. Só isso. Duas vezes por dia."],
        },
    ),
    "yara": dict(
        nome="Yara", curto="Yara", g="f", titulo="bruxa do brejo", papel="maldicao",
        desc="Quase queimada como bruxa. A Fenda fala com ela, e às vezes ela responde.",
        base=dict(hp=26, atk=3, poder=9, defesa=2, agi=5), cresc=dict(hp=5, atk=0.4, poder=1.7, defesa=0.4),
        valores={"magia_proibida": 3, "curiosidade": 3, "rebeldia": 3, "misericordia": 1, "diplomacia": 1,
                 "fe": -2, "autoridade": -3, "purificar": -3, "crueldade": -2, "fanatismo": -4, "violencia": -1},
        aprova={
            "magia_proibida": "Os olhos de Yara brilham. \"Você sentiu, não sentiu? Poder não é bom nem mau. É só poder.\"",
            "curiosidade": "Yara ri, encantada. \"Finalmente alguém que abre as portas em vez de pregá-las.\"",
            "rebeldia": "\"Bem feito\", diz Yara. \"Quem manda nunca é quem sangra.\"",
            "misericordia": "Yara observa você em silêncio. Depois, baixinho: \"Ninguém fez isso por mim antes de você.\"",
            "diplomacia": "\"Palavras também são feitiços\", sussurra Yara. \"Você sabe usar.\"",
            None: "Yara sorri de canto.",
        },
        desaprova={
            "fe": "Yara revira os olhos. \"Foi rezando que eles empilharam a lenha em volta de mim.\"",
            "autoridade": "\"Obedecer\", repete Yara, como quem prova algo azedo. \"Quase virei cinza por gente obediente.\"",
            "purificar": "Yara encara as chamas com raiva. \"Queimar o que não se entende. Conheço bem esse costume.\"",
            "crueldade": "Yara se afasta de você. \"Os aldeões que me amarraram também achavam que estavam certos.\"",
            "fanatismo": "Yara treme. Por um instante, você vê nos olhos dela a fogueira que quase a levou.",
            "violencia": "\"Tanto sangue por tão pouco\", diz Yara, enojada.",
            None: "Yara estreita os olhos.",
        },
        partida="Yara some numa noite sem lua. De manhã, só há um círculo de cinzas onde ela dormia, e um cheiro "
                "de coisa queimada que não é lenha.",
        ocioso={
            "alto": ["Yara trança ervas no seu cabelo enquanto você cochila. \"Contra pesadelos. Funciona. Às vezes.\"",
                     "\"Antes de você\", diz Yara, \"eu achava que ia morrer sozinha no brejo. Agora acho que vou morrer acompanhada. É uma melhora.\""],
            "medio": ["Yara fala com um sapo por um bom tempo. O sapo parece concordar.",
                      "Yara desenha símbolos na terra e apaga antes que você consiga ler."],
            "baixo": ["Yara dorme longe da fogueira. E longe de você.",
                      "\"Não se preocupe\", diz Yara, sem sorrir. \"Eu ainda não decidi nada.\""],
        },
    ),
}


# Escolhas dos eventos que mexem com a opinião da comitiva: (evento, opção) -> etiquetas.
REACOES = {
    ("circulo_de_fadas", "dancar"): ("curiosidade",), ("circulo_de_fadas", "trocar"): ("curiosidade",),
    ("circulo_de_fadas", "chutar"): ("violencia",), ("circulo_de_fadas", "nao"): ("cautela",),
    ("colmeia_selvagem", "fogo"): ("violencia",),
    ("luzes_fantasmas", "seguir"): ("curiosidade",), ("luzes_fantasmas", "resistir"): ("cautela",),
    ("cabana_da_bruxa", "atacar"): ("fanatismo", "violencia"), ("cabana_da_bruxa", "futuro"): ("curiosidade",),
    ("ninho_de_grifo", "pegar"): ("ganancia", "crueldade"), ("ninho_de_grifo", "domar"): ("coragem",),
    ("espantalho", "fogo"): ("violencia",), ("espantalho", "examinar"): ("curiosidade", "coragem"),
    ("fazenda_em_apuros", "ajudar"): ("generosidade", "misericordia"), ("fazenda_em_apuros", "nao"): ("pragmatismo",),
    ("biblioteca_ruida", "runas"): ("curiosidade",), ("biblioteca_ruida", "forca"): ("violencia", "sacrilegio"),
    ("golem_adormecido", "lutar"): ("coragem",), ("golem_adormecido", "gema"): ("ganancia",),
    ("sussurros_na_nevoa", "falar"): ("misericordia",), ("sussurros_na_nevoa", "prece"): ("fe", "misericordia"),
    ("sussurros_na_nevoa", "prender"): ("magia_proibida", "crueldade"), ("sussurros_na_nevoa", "nao"): ("cautela",),
    ("duelo_de_honra", "aceitar"): ("coragem", "honra"), ("duelo_de_honra", "recusar"): ("cautela",),
    ("veterano_cicatrizes", "treinar"): ("coragem",),
    ("aldeia_assombrada", "consagrar"): ("fe", "coragem", "purificar"), ("aldeia_assombrada", "nao"): ("cautela",),
    ("os_enfermos", "curar"): ("misericordia", "fe"), ("os_enfermos", "remedio"): ("generosidade",),
    ("os_enfermos", "nao"): ("pragmatismo",),
    ("tentacao_do_juramento", "recusar"): ("honestidade", "fe"), ("tentacao_do_juramento", "aceitar"): ("ganancia",),
    ("tentacao_do_juramento", "prender"): ("honestidade", "autoridade"),
    ("chamado_do_sangue", "nuas"): ("violencia", "coragem"), ("chamado_do_sangue", "resistir"): ("cautela",),
    ("contrato_da_irmandade", "aceitar"): ("ganancia",), ("contrato_da_irmandade", "nao"): ("honestidade",),
    ("contrato_da_irmandade", "matar"): ("crueldade", "ganancia"),
    ("contrato_da_irmandade", "poupar"): ("misericordia", "pragmatismo"),
    ("bolsos_alheios", "roubar"): ("trapaca", "ganancia"),
    ("anomalia_arcana", "absorver"): ("magia_proibida", "curiosidade"), ("anomalia_arcana", "estabilizar"): ("purificar",),
    ("grimorio_perdido", "ler"): ("magia_proibida", "curiosidade"), ("grimorio_perdido", "queimar"): ("purificar", "fe"),
    ("aprendiz_em_apuros", "ensinar"): ("generosidade",), ("aprendiz_em_apuros", "entrar"): ("coragem",),
    ("cacadores_de_bruxas", "falar"): ("diplomacia",), ("cacadores_de_bruxas", "lutar"): ("rebeldia", "violencia"),
    ("cacadores_de_bruxas", "fugir"): ("fuga",),
    ("elemental_selvagem", "absorver"): ("magia_proibida",), ("elemental_selvagem", "lutar"): ("violencia",),
    ("incendio", "dominar"): ("coragem",), ("incendio", "evacuar"): ("misericordia", "generosidade"),
    ("incendio", "nao"): ("crueldade",),
    ("cemiterio_antigo", "aprender"): ("magia_proibida", "curiosidade"), ("cemiterio_antigo", "nao"): ("fe",),
    ("aldeoes_temerosos", "ajudar"): ("generosidade", "honestidade"),
    ("aldeoes_temerosos", "assustar"): ("crueldade", "trapaca"),
    ("encontro_hostil", "atacar"): ("coragem",), ("encontro_hostil", "evitar"): ("cautela",),
    ("encontro_hostil", "conversar"): ("diplomacia",),
    ("viajante_ferido", "pocao"): ("misericordia", "generosidade"), ("viajante_ferido", "bandagem"): ("misericordia",),
    ("viajante_ferido", "prece"): ("fe", "misericordia"), ("viajante_ferido", "cacar"): ("coragem", "misericordia"),
    ("viajante_ferido", "roubar"): ("crueldade", "ganancia", "trapaca"), ("viajante_ferido", "ignorar"): ("pragmatismo",),
    ("mercador_golpista", "exigir"): ("honestidade",), ("mercador_golpista", "ajudar"): ("misericordia", "generosidade"),
    ("mercador_golpista", "licao"): ("violencia", "crueldade"),
    ("bau_abandonado", "nao"): ("cautela",),
    ("santuario_antigo", "rezar"): ("fe",), ("santuario_antigo", "oferenda"): ("fe", "generosidade"),
    ("santuario_antigo", "saquear"): ("sacrilegio", "ganancia"),
    ("acampamento_bandidos", "atacar"): ("coragem", "violencia"), ("acampamento_bandidos", "roubar"): ("trapaca", "ganancia"),
    ("acampamento_bandidos", "acordo"): ("diplomacia", "pragmatismo"), ("acampamento_bandidos", "evitar"): ("cautela",),
    ("crianca_perdida", "levar"): ("misericordia", "generosidade"), ("crianca_perdida", "indicar"): ("misericordia",),
    ("crianca_perdida", "ignorar"): ("crueldade",),
    ("cadaver_aventureiro", "revistar"): ("ganancia", "pragmatismo"), ("cadaver_aventureiro", "enterrar"): ("fe", "misericordia"),
    ("jogo_de_dados", "trapacear"): ("trapaca",),
    ("cacadores_de_recompensa", "lutar"): ("coragem",), ("cacadores_de_recompensa", "pagar"): ("pragmatismo",),
    ("pacote_suspeito", "recusar"): ("honestidade",), ("pacote_suspeito", "vender"): ("ganancia",),
    ("peregrinos", "ouvir"): ("fe",), ("peregrinos", "doar"): ("generosidade", "fe"),
    ("refugiados", "escoltar"): ("misericordia", "coragem"), ("refugiados", "doar"): ("generosidade",),
    ("refugiados", "nao"): ("pragmatismo",),
    ("caravana_atacada", "ajudar"): ("coragem", "misericordia"), ("caravana_atacada", "esperar"): ("ganancia", "crueldade"),
    ("tumulo_do_heroi", "honrar"): ("fe", "honra"), ("tumulo_do_heroi", "cavar"): ("sacrilegio", "ganancia"),
    ("visitante_misterioso", "dividir"): ("generosidade", "misericordia"), ("visitante_misterioso", "mandar"): ("cautela",),
    ("ladrao_noturno", "soltar"): ("misericordia",), ("ladrao_noturno", "entregar"): ("autoridade",),
    ("sussurros_do_vazio", "recusar"): ("purificar",), ("sussurros_do_vazio", "ouvir"): ("magia_proibida",),
    ("briga_de_taverna", "separar"): ("coragem",), ("briga_de_taverna", "entrar"): ("violencia",),
    ("briga_de_taverna", "roubar"): ("trapaca", "ganancia"),
    ("festival", "vigilia"): ("fe",), ("festival", "poco"): ("violencia", "coragem"),
    ("pregador_do_vazio", "debater"): ("coragem", "honestidade"), ("pregador_do_vazio", "seguir"): ("curiosidade", "coragem"),
    ("mendigo_misterioso", "dar"): ("generosidade",), ("mendigo_misterioso", "refeicao"): ("generosidade", "misericordia"),
    ("guarda_desconfiado", "pagar"): ("autoridade",), ("guarda_desconfiado", "argumentar"): ("diplomacia", "rebeldia"),
    ("guarda_desconfiado", "cela"): ("autoridade",),
}


NIVEIS = [(-40, "prestes a partir", "partindo"), (-15, "desconfiad{a}", "baixo"), (15, "neutr{a}", "neutro"),
          (45, "confia em você", "bom"), (75, "leal", "alto"), (101, "devotad{a}", "maximo")]


CARINHO = {
    "lobo": ["{n} deita a cabeça no seu joelho e fecha os olhos. O rabo bate devagar no chão.",
             "Você coça atrás das orelhas de {n}. Ele solta um suspiro longo de cachorro velho."],
    "urso": ["{n} rola de barriga para cima, esperando. Você coça. O chão treme com o ronco de satisfação.",
             "Você encosta na lateral quente de {n}. Ele te puxa com a pata, como se você fosse um filhote."],
    "falcao": ["{n} desce do galho para o seu braço e esfrega a cabeça na sua bochecha. Raro, para um falcão.",
               "Você alisa as penas do peito de {n}. Ele arrepia tudo, finge que não gostou, e fica."],
}


# O que dá para fazer no acampamento além da fogueira (a própria fogueira faz as vezes da Comitiva; viajar, só de dia).
ATALHOS_FOGUEIRA = ("talentos", "personagem", "mapa", "diario", "bestiario", "salvar", "sair")


# Falas curtas no meio da luta: aparecem em balões, uma por turno no máximo.
GRITOS = {
    "odete": {"cura": ["Fica de pé. Ainda não é hora.", "Respira. Eu tô aqui.", "A Mãe não te quer ainda."],
              "ataque": ["Que a luz te encontre!", "Perdoa. Mas vai doer."]},
    "morel": {"ataque": ["Vem, vem!", "Isso é pelo soldo.", "Olha pra mim, desgraçado!"],
              "atordoa": ["Fica aí no chão.", "Escudo na cara. Funciona sempre."]},
    "yara": {"maldicao": ["Eu vejo teu fio... e corto.", "Tua sorte acabou."],
             "ataque": ["Queima por dentro.", "Hm. Frágil."]},
}
