"""Dados estáticos do mundo: biomas, criaturas, afixos, clima e chefes."""

BIOMAS = {
    "floresta": {
        "nome": "Floresta",
        "lugares": [("Wood", "m"), ("Grove", "m"), ("Forest", "f"), ("Glade", "f"), ("Vale", "m")],
        "familias": ["lobo", "aranha", "bandido", "javali", "ent_jovem", "caido"],
        "ambiente": [
            "Corpos pendem dos galhos mais altos. Os corvos já levaram os olhos.",
            "O canto dos pássaros cessa de repente. O silêncio aqui tem dentes.",
            "Raízes cobrem ossos humanos, como se a floresta os estivesse digerindo devagar.",
            "Um cheiro de carne podre vem de algum lugar entre as árvores.",
            "Marcas de garras na casca, na altura da sua cabeça. Recentes.",
            "Um boneco de palha amarrado a uma árvore, com um pedaço de cabelo humano.",
        ],
        "abertura": [
            "Entre os troncos grossos", "Atrás de uma moita espinhosa",
            "Na curva de um riacho", "Sob um carvalho partido por um raio",
        ],
    },
    "pantano": {
        "nome": "Pântano",
        "lugares": [("Fen", "m"), ("Mire", "m"), ("Marsh", "m"), ("Bog", "m"), ("Swamp", "m")],
        "familias": ["afogado", "sapo", "bruxa_brejo", "sanguessuga", "bandido", "carnical"],
        "ambiente": [
            "Bolhas sobem da água escura. Às vezes, junto delas, sobe um dedo.",
            "Moscas cobrem um cavalo inchado meio afundado no lodo.",
            "A lama suga suas botas a cada passo, como se quisesse ficar com você.",
            "Luzes pálidas dançam sobre a água parada. Os afogados também se lembram de casa.",
            "Árvores mortas se erguem do lodo como mãos pedindo ajuda.",
            "Algo grande desliza sob a superfície e some. O silêncio volta pesado.",
        ],
        "abertura": [
            "Entre os juncos altos", "Da água turva", "Sobre um tronco apodrecido",
            "Atrás de uma cortina de musgo pendente",
        ],
    },
    "montanha": {
        "nome": "Montanhas",
        "lugares": [("Peak", "m"), ("Pass", "m"), ("Ridge", "f"), ("Gorge", "f"), ("Cliffs", "m")],
        "familias": ["harpia", "troll", "lobo_gelido", "grifo", "bandido", "cao_infernal"],
        "ambiente": [
            "O vento uiva entre as rochas e traz um cheiro de sangue velho.",
            "Um acampamento de mineiros abandonado. As panelas ainda têm comida congelada.",
            "Lá embaixo, as nuvens cobrem o vale. Aqui em cima, só você e os abutres.",
            "O ar rarefeito queima seus pulmões. Cada passo custa.",
            "Uma trilha de pegadas na neve termina de repente. Sem corpo. Sem sangue.",
            "Ossos roídos espalhados pela trilha estreita. Alguns ainda vestem botas.",
        ],
        "abertura": [
            "De uma fenda na rocha", "Do alto de um rochedo",
            "Atrás de uma curva estreita da trilha", "De uma caverna escura",
        ],
    },
    "planicie": {
        "nome": "Planícies",
        "lugares": [("Fields", "m"), ("Meadow", "f"), ("Plains", "f"), ("Hill", "f"), ("Road", "f")],
        "familias": ["bandido", "javali", "lobo", "cultista", "mercenario", "caido"],
        "ambiente": [
            "Uma fazenda queimada. Na porta do celeiro, alguém riscou: NÃO ABRA.",
            "Corvos disputam algo no meio do trigo podre. É melhor não olhar.",
            "Forcas na beira da estrada, com seus frutos balançando ao vento.",
            "Uma carroça tombada. Os bois foram devorados ainda presos aos arreios.",
            "Um moinho range sozinho. Dentro, alguém chora — ou algo imita choro.",
            "Uma vala comum mal coberta. A terra se mexe de leve.",
        ],
        "abertura": [
            "Do meio do capim alto", "Atrás de uma carroça tombada",
            "De trás de uma colina", "Na beira da estrada",
        ],
    },
    "ruinas": {
        "nome": "Ruínas",
        "lugares": [("Ruins", "f"), ("Necropolis", "f"), ("Fortress", "f"), ("Temple", "m"), ("Catacombs", "f")],
        "familias": ["esqueleto", "espectro", "golem", "cultista", "rato", "carnical", "caido"],
        "ambiente": [
            "Colunas quebradas se erguem como costelas de um deus morto.",
            "Nas paredes, nomes riscados à unha por quem ficou preso aqui.",
            "Seus passos ecoam em corredores que não deveriam ser tão longos.",
            "Um frio que não vem do vento sobe pelas suas costas. Algo respira no escuro.",
            "Ossos estalam sob suas botas. Pequenos demais para serem de adultos.",
            "Um altar coberto de sangue seco. E sangue não tão seco por cima.",
        ],
        "abertura": [
            "De trás de uma coluna caída", "Das sombras de uma cripta",
            "De uma passagem secreta", "Do alto de uma escadaria ruída",
        ],
    },
    "cidadela": {
        "nome": "Cidadela",
        "lugares": [("Citadel", "f")],
        "familias": ["cultista", "espectro", "cavaleiro_sombrio", "cria_vazio", "abominacao", "cao_infernal"],
        "ambiente": [
            "O céu aqui é da cor de uma ferida. Não há sol, nem estrelas, nem esperança.",
            "As paredes pulsam devagar, como carne viva.",
            "Vozes sussurram seu nome de dentro das pedras. Algumas são de gente que você conheceu.",
        ],
        "abertura": ["De um corredor de obsidiana", "Das sombras do salão", "De trás de um altar profanado"],
    },
}

# Nomes próprios em inglês (o texto do jogo continua em português).
SUFIXOS_LUGAR = [
    "of the Raven", "of Laments", "of the Old Moon", "of the Fallen King", "of Bones", "of Silver",
    "of Ashes", "of the White Wolf", "of Whispers", "of Mist", "of the Oath",
    "of a Thousand Voices", "of Echoes", "of the Serpent", "of the Hanged", "of the Last Watch",
    "of the Broken Bell", "of the Witches", "of the Giant", "of the Dawn",
]

VILA_PREFIXOS = ["Stone", "White", "Black", "Grey", "Cold", "Old", "Ash", "Oak", "Raven", "Gold"]
VILA_SUFIXOS = ["ford", "vale", "hollow", "watch", "haven", "stead", "moor", "brook", "fall", "gate"]

# Traços alteram o dano recebido conforme tipo e alcance do ataque.
TRACOS = {
    "fera": "Fera: instintiva e rápida.",
    "humano": "Humano: astuto, pode fugir ou negociar.",
    "voador": "Voador: resiste a golpes corpo a corpo, vulnerável a ataques à distância.",
    "blindado": "Blindado: resiste a dano físico, vulnerável a magia.",
    "morto-vivo": "Morto-vivo: imune a veneno, fraco contra sagrado, resiste a sombra.",
    "etereo": "Etéreo: armas físicas atravessam seu corpo; arcano e sagrado o ferem.",
    "planta": "Planta: queima com facilidade.",
    "construto": "Construto: imune a veneno e sangramento, sensível ao arcano.",
    "gigante": "Gigante: difícil de atordoar.",
    "corrompido": "Corrompido: tocado pelo Vazio; sagrado o fere, sombra o alimenta.",
    "conjurador": "Conjurador: usa magia.",
    "demonio": "Demônio: cria do Inferno; o sagrado o queima, o fogo pouco o fere.",
}

# nome, plural, gênero, atributos base (nível 1), traços, habilidades, xp, ouro, tamanho de grupo
FAMILIAS = {
    "lobo": dict(nome="lobo", plural="lobos", g="m", hp=20, atk=6, defesa=2, agi=6, poder=0,
                 tracos=["fera"], habs=["mordida_sangrenta", "uivo"], xp=12, ouro=(0, 2), grupo=(1, 3)),
    "aranha": dict(nome="aranha gigante", plural="aranhas gigantes", g="f", hp=18, atk=6, defesa=2, agi=7, poder=0,
                   tracos=["fera"], habs=["teia", "veneno"], xp=13, ouro=(0, 2), grupo=(1, 2)),
    "bandido": dict(nome="bandido", plural="bandidos", g="m", hp=24, atk=7, defesa=3, agi=5, poder=0,
                    tracos=["humano"], habs=["roubar", "golpe_sujo"], xp=14, ouro=(4, 12), grupo=(1, 3)),
    "javali": dict(nome="javali selvagem", plural="javalis selvagens", g="m", hp=28, atk=7, defesa=4, agi=3, poder=0,
                   tracos=["fera"], habs=["investida"], xp=13, ouro=(0, 1), grupo=(1, 2)),
    "ent_jovem": dict(nome="ent jovem", plural="ents jovens", g="m", hp=40, atk=8, defesa=7, agi=1, poder=0,
                      tracos=["planta", "blindado"], habs=["esmagar", "regenerar"], xp=22, ouro=(0, 3), grupo=(1, 1)),
    "afogado": dict(nome="afogado", plural="afogados", g="m", hp=26, atk=7, defesa=3, agi=2, poder=3,
                    tracos=["morto-vivo"], habs=["agarrar", "drenar"], xp=15, ouro=(1, 6), grupo=(1, 3)),
    "sapo": dict(nome="sapo-touro gigante", plural="sapos-touro gigantes", g="m", hp=30, atk=6, defesa=3, agi=4, poder=0,
                 tracos=["fera"], habs=["veneno", "agarrar"], xp=14, ouro=(0, 1), grupo=(1, 2)),
    "bruxa_brejo": dict(nome="bruxa do brejo", plural="bruxas do brejo", g="f", hp=24, atk=4, defesa=2, agi=5, poder=9,
                        tracos=["humano", "conjurador"], habs=["maldicao", "bola_fogo", "cura"], xp=20, ouro=(6, 15),
                        grupo=(1, 1), ataque="sombra"),
    "sanguessuga": dict(nome="sanguessuga gigante", plural="sanguessugas gigantes", g="f", hp=16, atk=5, defesa=1, agi=3,
                        poder=0, tracos=["fera"], habs=["drenar"], xp=9, ouro=(0, 0), grupo=(2, 3)),
    "harpia": dict(nome="harpia", plural="harpias", g="f", hp=20, atk=7, defesa=2, agi=9, poder=0,
                   tracos=["voador"], habs=["grito_terror", "mordida_sangrenta"], xp=15, ouro=(1, 5), grupo=(1, 3)),
    "troll": dict(nome="troll da montanha", plural="trolls da montanha", g="m", hp=55, atk=10, defesa=5, agi=1, poder=0,
                  tracos=["gigante"], habs=["esmagar", "regenerar"], xp=30, ouro=(2, 10), grupo=(1, 1),
                  resist={"fogo": 1.4}),
    "lobo_gelido": dict(nome="lobo gélido", plural="lobos gélidos", g="m", hp=24, atk=7, defesa=3, agi=6, poder=0,
                        tracos=["fera"], habs=["mordida_gelida", "uivo"], xp=15, ouro=(0, 2), grupo=(1, 3),
                        resist={"gelo": 0.5, "fogo": 1.3}),
    "grifo": dict(nome="grifo", plural="grifos", g="m", hp=38, atk=9, defesa=4, agi=7, poder=0,
                  tracos=["voador", "fera"], habs=["investida", "mordida_sangrenta"], xp=26, ouro=(0, 4), grupo=(1, 1)),
    "cultista": dict(nome="cultista", plural="cultistas", g="m", hp=22, atk=5, defesa=2, agi=4, poder=8,
                     tracos=["humano", "conjurador"], habs=["bola_sombra", "cura", "grito_terror"], xp=16,
                     ouro=(3, 10), grupo=(1, 3), ataque="sombra"),
    "mercenario": dict(nome="mercenário", plural="mercenários", g="m", hp=32, atk=8, defesa=5, agi=4, poder=0,
                       tracos=["humano", "blindado"], habs=["esmagar", "golpe_sujo", "grito_guerra"], xp=18,
                       ouro=(5, 15), grupo=(1, 2)),
    "esqueleto": dict(nome="esqueleto", plural="esqueletos", g="m", hp=22, atk=7, defesa=4, agi=3, poder=0,
                      tracos=["morto-vivo"], habs=["investida"], xp=13, ouro=(0, 4), grupo=(1, 3)),
    "espectro": dict(nome="espectro", plural="espectros", g="m", hp=20, atk=4, defesa=1, agi=8, poder=8,
                     tracos=["morto-vivo", "etereo"], habs=["drenar", "grito_terror"], xp=17, ouro=(0, 6),
                     grupo=(1, 2), ataque="sombra"),
    "golem": dict(nome="golem de pedra", plural="golens de pedra", g="m", hp=60, atk=10, defesa=9, agi=0, poder=0,
                  tracos=["construto", "blindado"], habs=["esmagar"], xp=30, ouro=(0, 5), grupo=(1, 1)),
    "rato": dict(nome="rato gigante", plural="ratos gigantes", g="m", hp=12, atk=4, defesa=1, agi=6, poder=0,
                 tracos=["fera"], habs=["mordida_sangrenta", "veneno"], xp=6, ouro=(0, 1), grupo=(2, 4)),
    "cavaleiro_sombrio": dict(nome="cavaleiro sombrio", plural="cavaleiros sombrios", g="m", hp=45, atk=11, defesa=7,
                              agi=3, poder=5, tracos=["morto-vivo", "blindado"], habs=["esmagar", "drenar"], xp=32,
                              ouro=(5, 20), grupo=(1, 1)),
    "abominacao": dict(nome="abominação", plural="abominações", g="f", hp=60, atk=11, defesa=4, agi=2, poder=0,
                       tracos=["corrompido", "gigante"], habs=["esmagar", "veneno", "regenerar"], xp=35,
                       ouro=(2, 12), grupo=(1, 1)),
    "cria_vazio": dict(nome="cria do Vazio", plural="crias do Vazio", g="f", hp=26, atk=8, defesa=2, agi=7, poder=7,
                       tracos=["corrompido", "etereo"], habs=["bola_sombra", "drenar"], xp=20, ouro=(0, 5),
                       grupo=(1, 2), ataque="sombra"),
    "caido": dict(nome="caído", plural="caídos", g="m", hp=13, atk=5, defesa=1, agi=6, poder=0,
                  tracos=["demonio"], habs=["golpe_sujo"], xp=7, ouro=(0, 3), grupo=(2, 4)),
    "xama_caido": dict(nome="xamã caído", plural="xamãs caídos", g="m", hp=18, atk=3, defesa=1, agi=5, poder=7,
                       tracos=["demonio", "conjurador"], habs=["bola_fogo", "reviver", "reviver"], xp=16,
                       ouro=(2, 8), grupo=(1, 1), ataque="fogo"),
    "cao_infernal": dict(nome="cão infernal", plural="cães infernais", g="m", hp=26, atk=8, defesa=3, agi=7, poder=6,
                         tracos=["demonio", "fera"], habs=["mordida_sangrenta", "bola_fogo"], xp=18, ouro=(0, 2),
                         grupo=(1, 3), resist={"fogo": 0.3, "gelo": 1.3}),
    "carnical": dict(nome="carniçal", plural="carniçais", g="m", hp=30, atk=8, defesa=3, agi=4, poder=0,
                     tracos=["morto-vivo"], habs=["devorar", "mordida_sangrenta"], xp=17, ouro=(0, 4), grupo=(1, 2)),
    "esqueleto_servo": dict(nome="servo esquelético", plural="servos esqueléticos", g="m", hp=18, atk=6, defesa=3,
                            agi=3, poder=0, tracos=["morto-vivo"], habs=[], xp=0, ouro=(0, 0), grupo=(1, 1)),
}

# Afixos dão variedade: o mesmo lobo pode ser feroz, ancião ou corrompido.
AFIXOS = {
    "feroz": dict(m="feroz", f="feroz", atk=1.3, xp=1.3),
    "robusto": dict(m="robusto", f="robusta", hp=1.5, xp=1.3),
    "agil": dict(m="ágil", f="ágil", agi=5, xp=1.2),
    "venenoso": dict(m="venenoso", f="venenosa", habs=["veneno"], xp=1.2),
    "anciao": dict(m="ancião", f="anciã", hp=1.4, atk=1.2, defesa=1.3, xp=1.8, ouro=2.0),
    "corrompido": dict(m="corrompido", f="corrompida", hp=1.2, atk=1.2, tracos=["corrompido"], habs=["drenar"], xp=1.5),
    "flamejante": dict(m="flamejante", f="flamejante", habs=["bola_fogo"], poder=6, resist={"fogo": 0.3, "gelo": 1.4},
                       xp=1.4),
}

CLIMAS = {
    "limpo": {"nome": "Céu limpo", "desc": "O céu está limpo."},
    "nublado": {"nome": "Nublado", "desc": "Nuvens cinzentas cobrem o céu."},
    "chuva": {"nome": "Chuva", "desc": "Uma chuva fina e persistente cai. (fogo -20%, gelo +10%)"},
    "nevoa": {"nome": "Névoa", "desc": "Uma névoa densa engole tudo a poucos passos. (esquiva +5%)"},
    "tempestade": {"nome": "Tempestade", "desc": "Trovões rasgam o céu. (ataques à distância -15%)"},
    "neve": {"nome": "Neve", "desc": "Flocos de neve caem em silêncio. (gelo +20%, fogo -15%)"},
}
PESOS_CLIMA = {
    "padrao": {"limpo": 40, "nublado": 25, "chuva": 15, "nevoa": 10, "tempestade": 6},
    "montanha": {"limpo": 30, "nublado": 20, "nevoa": 15, "tempestade": 10, "neve": 25},
    "pantano": {"limpo": 15, "nublado": 25, "chuva": 25, "nevoa": 30, "tempestade": 5},
    "cidadela": {"tempestade": 60, "nevoa": 40},
}

PERIODOS = ["Manhã", "Tarde", "Anoitecer", "Noite"]

# Guardiões: três deles guardam os Sigilos que abrem o caminho até a Cidadela.
GUARDIOES = {
    "floresta": [
        dict(base="Arachnid Queen", g="f", hp=120, atk=10, defesa=4, agi=8, poder=6, tracos=["fera"],
             habs=["teia", "veneno", "invocar"], invoca="aranha", resist={"fogo": 1.4},
             intro="Teias grossas como cordas cobrem as árvores. Algo enorme desce do alto, com olhos demais para contar.",
             fases=[dict(limiar=0.5, texto="A rainha guincha e seus filhotes despencam das copas!",
                         atk=1.2, habs=["mordida_sangrenta"])]),
        dict(base="Elder Ent", g="m", hp=160, atk=12, defesa=8, agi=1, poder=4, tracos=["planta", "blindado"],
             habs=["esmagar", "regenerar", "agarrar", "varredura"], resist={"fogo": 1.6},
             intro="A floresta inteira parece se mover. Uma árvore milenar abre olhos de seiva âmbar e fala com voz de terremoto.",
             fases=[dict(limiar=0.4, texto="A casca do Ent racha e uma luz verde e furiosa escapa das fendas!",
                         atk=1.3, defesa=0.7, habs=["investida"])]),
    ],
    "pantano": [
        dict(base="Bog Hydra", g="f", hp=140, atk=10, defesa=4, agi=4, poder=4, tracos=["fera"],
             habs=["regenerar", "veneno", "mordida_sangrenta", "varredura"],
             intro="A água ferve. Uma, duas, três cabeças de serpente emergem, sibilando em uníssono.",
             fases=[dict(limiar=0.5, texto="Onde uma cabeça foi cortada, duas novas brotam!", atk=1.35)]),
        dict(base="Drowned Witch", g="f", hp=110, atk=6, defesa=3, agi=6, poder=12, tracos=["morto-vivo", "conjurador"],
             habs=["maldicao", "bola_sombra", "invocar", "drenar"], invoca="afogado", ataque="sombra",
             intro="Uma mulher de pele azulada flutua sobre o charco, cabelos de algas escorrendo, cantando uma canção de ninar.",
             fases=[dict(limiar=0.5, texto="O canto vira um grito. Mãos podres emergem da água ao seu redor!",
                         poder=1.3, habs=["grito_terror"])]),
    ],
    "montanha": [
        dict(base="Troll King", g="m", hp=170, atk=13, defesa=6, agi=1, poder=0, tracos=["gigante"],
             habs=["esmagar", "regenerar", "investida", "varredura"], resist={"fogo": 1.4},
             intro="Sobre um trono de ossos de gigante, um troll colossal usa uma coroa feita de um elmo amassado.",
             fases=[dict(limiar=0.45, texto="O Rei Troll arranca uma rocha do chão e ruge de fúria!", atk=1.3)]),
        dict(base="Ice Wyrm", g="m", hp=130, atk=11, defesa=5, agi=6, poder=8, tracos=["voador"],
             habs=["mordida_gelida", "esmagar", "grito_terror", "varredura"], resist={"gelo": 0.3, "fogo": 1.4},
             intro="O pico inteiro treme. Um dragão serpentino de escamas azul-gelo desdobra as asas sobre você.",
             fases=[dict(limiar=0.5, texto="O wyrm inspira fundo e o ar congela ao seu redor!", atk=1.25,
                         habs=["investida"])]),
    ],
    "planicie": [
        dict(base="Warlord", g="m", hp=130, atk=11, defesa=7, agi=4, poder=0, tracos=["humano", "blindado"],
             habs=["golpe_sujo", "esmagar", "invocar", "grito_guerra", "varredura"], invoca="bandido",
             intro="Um acampamento fortificado. No centro, um homem de armadura remendada com troféus de seus inimigos aguarda.",
             fases=[dict(limiar=0.5, texto="\"Ninguém me derruba!\" Ele joga fora o escudo e pega um machado em cada mão.",
                         atk=1.35, defesa=0.7)]),
        dict(base="Ash Prophet", g="m", hp=115, atk=6, defesa=3, agi=5, poder=12, tracos=["humano", "conjurador"],
             habs=["bola_sombra", "cura", "invocar", "maldicao"], invoca="cultista", ataque="sombra",
             intro="Um círculo de fiéis entoa cânticos ao redor de um homem cego que chora cinzas.",
             fases=[dict(limiar=0.5, texto="O Profeta abre os braços e o Vazio responde ao seu chamado!",
                         poder=1.3, habs=["drenar"])]),
    ],
    "ruinas": [
        dict(base="Lesser Lich", g="m", hp=115, atk=5, defesa=4, agi=4, poder=13, tracos=["morto-vivo", "conjurador"],
             habs=["bola_sombra", "maldicao", "invocar", "drenar"], invoca="esqueleto", ataque="sombra",
             intro="Num salão de colunas tombadas, um esqueleto coroado ergue os olhos de um grimório. Duas chamas verdes acendem nas órbitas.",
             fases=[dict(limiar=0.5, texto="O lich esmaga uma joia em sua mão e sua forma se torna translúcida!",
                         tracos=["etereo"], poder=1.2)]),
        dict(base="Primordial Golem", g="m", hp=180, atk=13, defesa=11, agi=0, poder=0, tracos=["construto", "blindado"],
             habs=["esmagar", "investida", "varredura"],
             intro="Runas se acendem no chão. O que você pensava ser uma parede se levanta: um golem do tamanho de uma casa.",
             fases=[dict(limiar=0.5, texto="As placas de pedra caem e o núcleo pulsante do golem fica exposto!",
                         defesa=0.4, atk=1.25)]),
    ],
}

ANTAGONISTAS = [
    ("Lord of Terror", "m"), ("Queen of Flies", "f"), ("Devourer of Souls", "m"),
    ("Defiled Archbishop", "m"), ("Mother of Broods", "f"), ("Herald of the Void", "m"),
    ("Plague Bride", "f"), ("Hanged King", "m"),
]
ORIGENS_ANTAGONISTA = [
    "que um dia foi um herói como você, até cravar uma pedra do Inferno na própria testa para aprisionar um demônio — e perder",
    "que vendeu a cidade inteira ao Vazio em troca de não morrer, e cumpriu o contrato rua por rua",
    "nascido do último suspiro de um deus que os homens deixaram de adorar",
    "o bispo que abriu as catacumbas da catedral procurando Deus e encontrou outra coisa",
    "que abriu a Fenda há cem anos e agora quer atravessá-la por completo, arrastando o mundo junto",
]
NOMES_CIDADELA = ["Black Tower", "Broken Citadel", "Throne of the Void", "Bastion of Ashes", "Obsidian Crown"]

# Anotações do bestiário (reveladas ao encontrar cada criatura).
LORE = {
    "lobo": "Caçam em matilha e uivam para chamar as outras. Um lobo sozinho raramente está sozinho.",
    "aranha": "Tecem armadilhas entre as árvores. Seu veneno paralisa antes de matar.",
    "bandido": "Desertores, camponeses arruinados e gente pior. Gostam mais do seu ouro do que de lutar.",
    "javali": "Teimosos e brutais. A investida de um javali derruba até cavaleiros.",
    "ent_jovem": "Árvores que acordaram com raiva. Madeira verde queima mal — mas queima.",
    "afogado": "Os que o pântano não devolveu. Agarram e puxam para o fundo.",
    "sapo": "A língua é mais rápida que uma flecha, e o couro é venenoso ao toque.",
    "bruxa_brejo": "Vendem curas, maldições e às vezes as duas coisas no mesmo frasco.",
    "sanguessuga": "Lentas e nojentas. Sozinhas são inofensivas; em bando, secam um homem.",
    "harpia": "Metade mulher, metade abutre, inteira cruel. Difíceis de acertar com uma espada.",
    "troll": "Regeneram quase tudo — menos o fogo. Fique longe quando ele recuar para golpear.",
    "lobo_gelido": "O frio da montanha mora dentro deles. Odeiam fogo mais que qualquer coisa.",
    "grifo": "Rei dos céus das montanhas. Protege o ninho até a morte.",
    "cultista": "Servos da Fenda. Curam uns aos outros: derrube o curandeiro primeiro.",
    "mercenario": "Armadura boa, moral flexível. Lutam pelo maior lance.",
    "esqueleto": "Ossos animados por ódio antigo. Veneno não faz nada; luz sagrada faz muito.",
    "espectro": "Lâminas atravessam seu corpo. Magia arcana e fé o ferem de verdade.",
    "golem": "Pedra e runas. Lento, mas cada golpe é uma avalanche. A magia racha a pedra.",
    "rato": "Onde há um, há vinte. Mordidas sujas que infeccionam.",
    "cavaleiro_sombrio": "Guerreiros que juraram lealdade ao Vazio e não puderam morrer depois.",
    "abominacao": "Carne costurada pela corrupção. Ninguém sabe o que ela foi antes.",
    "cria_vazio": "Pedaços da Fenda que aprenderam a andar. Surgem quando a corrupção cresce.",
    "caido": "Diabretes covardes que atacam em bando, rindo. Mate o xamã primeiro, ou eles voltam.",
    "xama_caido": "Pequeno feiticeiro dos caídos. Cospe fogo e ergue os irmãos mortos do chão.",
    "cao_infernal": "Cães de brasa com dentes de obsidiana. O fogo é a casa deles.",
    "carnical": "Mortos famintos que devoram os caídos no meio da luta para fechar as próprias feridas.",
}
