# Fontes em Aseprite

Os ícones cuja fonte final é um `.aseprite` em camadas, desenhado no Aseprite (pelo MCP ou à mão). O jogo nunca lê
nada daqui: só os PNGs exportados para `rpg/web/static/hud/icones/`.

## As fontes finais

| Peça | Arquivos | Camadas (de baixo para cima) | No jogo desde |
|---|---|---|---|
| varinha | `varinha/varinha-32.aseprite`, `-40`, `-48`, `-64` (RGBA, 1 quadro, fundo transparente) | pomo, empunhadura, anel, haste, taca, pedra, garras, contorno | 1.109.0 |
| gibao (peito de couro) | `gibao/gibao-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** (sem fonte própria) | forro, corpo, abas, pala, bordas, fecho, costuras, contorno | 1.110.0 |
| bota (botas de couro) | `bota/bota-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** (sem fonte própria) | tras, tras_dobra, tras_sola, frente, frente_dobra, frente_sola, tira, detalhes, contorno | 1.110.0 |
| capuz (capuz de couro) | `capuz/capuz-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | capa, capuz, interior, borda, cordao, desgaste, contorno | 1.112.0 |
| luva (luva de couro com braçadeira) | `luva/luva-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | bracadeira, luva, cordao, desgaste, contorno | 1.112.0 |
| capuz_tecido (capuz de tecido) | `capuz_tecido/capuz_tecido-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | capa, capuz, interior, borda, contorno | 1.112.0 |
| luva_seda (luva de seda) | `luva_seda/luva_seda-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | punho, luva, brilho, contorno | 1.112.0 |
| calca_couro (Calça de Couro do Arqueiro) | `calca_couro/calca_couro-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | pernas, remendo, cos, barra, braguilha, desgaste, contorno | 1.119.0 |
| attr-ataque (o ícone de Ataque) | `attr-ataque/attr-ataque-24.aseprite`, `-32`; **o 64 é o 32 ampliado 2×** | lamina, guarda, cabo, pomo, contorno | 1.120.0 |
| attr-defesa (o ícone de Defesa) | `attr-defesa/attr-defesa-24.aseprite`, `-32`; **o 64 é o 32 ampliado 2×** | face, borda, bossa, contorno | 1.120.0 |
| attr-poder (o ícone de Poder) | `attr-poder/attr-poder-24.aseprite`, `-32`; **o 64 é o 32 ampliado 2×** | chama, miolo, faisca, contorno | 1.123.0 |
| atalho-inventario (o Inventário da doca) | `atalho-inventario/atalho-inventario-36.aseprite`, `-32` | rolo, bolsos, corpo, aba, cinta, fivela, contorno | 1.124.0 |
| vital-vida (a Vida do topo) | `vital-vida/vital-vida-20.aseprite` | coracao, brilho, contorno | 1.130.0 |
| vital-mana (a Mana do topo) | `vital-mana/vital-mana-20.aseprite` | gota, brilho, contorno | 1.130.0 |
| vital-vigor (o Vigor do topo) | `vital-vigor/vital-vigor-20.aseprite` | pulso, dedos, polegar, dobras, contorno | 1.131.0 |
| vital-foco (o Foco do topo) | `vital-foco/vital-foco-20.aseprite` | anel, marcas, centro, contorno | 1.131.0 |
| moedas (o Ouro do topo e do balcão) | `moedas/moedas-24.aseprite`, `-32` | pilha, topo, moeda, contorno | 1.132.0 (o 32, 1.133.0) |
| provisoes (as Provisões do topo e do mercado) | `provisoes/provisoes-24.aseprite`, `-32` | carne, osso, contorno | 1.132.0 |
| moeda (a moeda avulsa dos preços e dos ganhos) | `moeda/moeda-16.aseprite`, `-32` | espessura, beira, anel, face, contorno | 1.134.0 |
| tocha (a tocha do topo, da bolsa e de 16) | `tocha/tocha-16.aseprite`, `-24`, `-32` | cabo, pano, chama, contorno | 1.135.0 (o 16, 1.136.0) |
| bandagem (a Bandagem) | `bandagem/bandagem-16.aseprite`, `-24`, `-32` | tira, corpo, face, contorno | 1.138.0 |
| pocao (a Poção de Vida e o comando Itens) | `pocao/pocao-16.aseprite`, `-24`, `-32` | vidro, liquido, rolha, brilho, contorno | 1.138.0 |
| tonico (o Tônico Restaurador) | `tonico/tonico-16.aseprite`, `-32` | vidro, liquido, rolha, brilho, contorno | 1.138.0 |
| calca_tecido (a Calça de Viagem do Mago) | `calca_tecido/calca_tecido-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | pernas, dobras, barra, cintura, cordao, contorno | 1.138.0 |
| manto (o Manto do Mago, também Túnica, Veste Rúnica e Manto de Cinzas) | `manto/manto-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | mangas, corpo, forro, gola, debrum, faixa, fecho, contorno | 1.138.0 |
| anel (o anel: Anel, Sinete, Aro e o Anel do Último Rei; o vazio) | `anel/anel-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | dentro, fora, gravacao, borda, brilho, contorno | 1.140.0 |
| chapeu (o Chapéu Pontudo do Mago) | `chapeu/chapeu-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | aba, copa, dobras, fita, contorno | 1.141.0 |
| besta (a Besta Leve do Arqueiro) | `besta/besta-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | coronha, empunhadura, corda, arco, metal, contorno | 1.143.0 |
| espada (a espada do Guerreiro: a Espada, o Montante, a arma vazia e o Atacar) | `espada/espada-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | empunhadura, pomo, guarda, lamina, contorno | 1.145.0 |
| maca (a Maça do Guerreiro) | `maca/maca-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | cabo, empunhadura, cabeca, contorno | 1.145.0 |
| cota (o desenho `armadura` do Guerreiro: Cota de Malha, Peitoral, Couraça, Brigantina; o peito vazio) | `cota/cota-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | malha, couro, ferragem, contorno | 1.146.0 |
| manopla (a Manopla do Guerreiro e os raros dela; as mãos vazias): **a L7**, a transposição da referência escolhida pelo Jean (`ferramentas/arte/referencias/Luvas/luvas-par-recorte.png`; **a origem e a licença do recorte, com marca d'água, ainda não foram esclarecidas: pendência aberta, sem licença atribuída**) | `manopla/manopla-32.aseprite`; **o 40 e o 48 são o 32 centrado num quadro transparente (4 e 8 px), o 64 é o 32 ampliado 2×** | guia (a redução da referência, oculta, fora da exportação), couro, malha, contorno | 1.151.0 |
| (histórico) a M5, a manopla da 1.147.0 à 1.150.0, **adaptação de arte externa CC0**: a `glove_04` da Dungeon Crawl Stone Soup (a origem, a autoria e a licença em `ferramentas/arte/externas/cc0_hand_wear_icons/LEIA-ME.md`) | `historico/manopla-m5/manopla-32.aseprite`, `-40`, `-48` (fora da exportação) | original (oculto), malha, couro | 1.147.0 |
| elmo (o Elmo, o Capacete e a Barbuta do Guerreiro; a cabeça vazia e a reserva da cabeça): **o C1**, o capacete com malha, a transposição da imagem gerada do Jean (`ferramentas/arte/referencias/capacete/capacete-malha-gerada.webp`) | `elmo/elmo-32.aseprite`; **o 40 e o 48 são o 32 centrado num quadro transparente (4 e 8 px), o 64 é o 32 ampliado 2×** | guia (a redução da referência, oculta, fora da exportação), interior, malha, aco, couro, contorno | 1.153.0 |
| (histórico) o elmo de frente da 1.148.0 à 1.152.0 (a rodada 4) | `historico/elmo-r4/elmo-32.aseprite`, `-40`, `-48` (fora da exportação) | interior, calota, faces, tiras, contorno | 1.148.0 |
| perneiras (o desenho `calca` do Guerreiro: a Perneira e a Greva; as pernas vazias e a reserva das pernas): **a P7**, a transposição da segunda imagem gerada do Jean (`ferramentas/arte/referencias/calça/perneiras-gerada-2.webp`), com as laterais suavizadas | `perneiras/perneiras-32.aseprite`; **o 40 e o 48 são o 32 centrado num quadro transparente (4 e 8 px), o 64 é o 32 ampliado 2×** | guia (a redução da referência, oculta, fora da exportação), malha, aco, couro, contorno | 1.152.0 |
| (histórico) a P4, as perneiras da 1.148.0 à 1.151.0 (a calça de malha com as placas de ferro nas coxas) | `historico/perneiras-p4/perneiras-32.aseprite`, `-40`, `-48` (fora da exportação) | malha, placas, cinto, contorno | 1.148.0 |
| botas-ferro (o desenho `bota_ferro` do Guerreiro: a Bota Ferrada; os pés vazios), a transposição da referência gerada do Jean (`ferramentas/arte/referencias/botas/`) com o acabamento A1 (os reflexos contidos; a referência de acabamento `Botas de ferro em pixel art.png`) | `botas-ferro/botas-ferro-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | guia (a redução da referência, oculta, fora da exportação), interior, couro, aco, contorno | 1.154.0 |
| (histórico) a B3, as botas de ferro da 1.150.0 à 1.153.0 (o acabamento polido) | `historico/botas-ferro-b3/botas-ferro-32.aseprite`, `-40`, `-48` (fora da exportação) | guia, interior, couro, aco, contorno | 1.150.0 |
| contador-flechas (a flecha ao lado da quantidade de flechas na carta do Arqueiro, `Icones.contadorFlechas`): a F2, a ponta de aço, a haste e as penas na traseira (as referências em `ferramentas/arte/referencias/icones/`) | `contador-flechas/contador-flechas-16.aseprite` (só o 16) | haste, penas, amarrado, ponta, contorno | 1.155.0 |
| estado-firme (o ícone do estado Firme, `Icones.estado("firme")`): a R2, a corrente rompida (as referências em `ferramentas/arte/referencias/icones/`) | `estado-firme/estado-firme-16.aseprite` (só o 16) | elos, contorno | 1.155.0 |
| estado-guarda (o ícone do estado Em guarda, `Icones.estado("guarda")`): o G1, o escudo de ferro | `estado-guarda/estado-guarda-16.aseprite` (só o 16) | face, aro, contorno | 1.156.0 |
| estado-esquiva (o ícone do estado Esquiva, `Icones.estado("esquiva")`): a E6 corrigida, a figura em movimento copiada da referência `ferramentas/arte/referencias/icones/esquiva-figura-movimento.png` (**a origem e a licença da referência não foram informadas: pendência aberta**) | `estado-esquiva/estado-esquiva-16.aseprite` (só o 16) | riscos, figura, contorno | 1.157.0 |
| estado-sangramento (o ícone do estado Sangramento, `Icones.estado("sangramento")`): a gota grande e a pequena atrás | `estado-sangramento/estado-sangramento-16.aseprite` (só o 16) | gotas, contorno | 1.158.0 |
| estado-maldito (o ícone do estado Maldição, `Icones.estado("maldito")`): a caveira roxa de olhos acesos | `estado-maldito/estado-maldito-16.aseprite` (só o 16) | cranio, olhos, contorno | 1.158.0 |
| estado-marcado (o ícone do estado Marcado, `Icones.estado("marcado")`): o alvo de anéis | `estado-marcado/estado-marcado-16.aseprite` (só o 16) | aneis, contorno | 1.158.0 |
| estado-furtivo (o ícone do estado Furtivo, `Icones.estado("furtivo")`): o capuz com os olhos | `estado-furtivo/estado-furtivo-16.aseprite` (só o 16) | capuz, rosto, olhos, contorno | 1.158.0 |
| estado-furia (o ícone do estado Fúria, `Icones.estado("furia")`): o rosto vermelho de raiva | `estado-furia/estado-furia-16.aseprite` (só o 16) | rosto, sobrancelhas, olhos, contorno | 1.158.0 |
| estado-queimadura (o ícone do estado Chamas, `Icones.estado("queimadura")`): a chama dominante com duas línguas menores (a R2) | `estado-queimadura/estado-queimadura-16.aseprite` (só o 16) | chama, miolo, contorno | 1.159.0 |
| estado-fortalecido (o ícone do estado Fortalecido, `Icones.estado("fortalecido")`): a espada em pé e a seta verde subindo (a R2) | `estado-fortalecido/estado-fortalecido-16.aseprite` (só o 16) | espada, seta, contorno | 1.159.0 |
| estado-enfraquecido (o ícone do estado Enfraquecido, `Icones.estado("enfraquecido")`): a espada para baixo e a seta roxa descendo (a R2) | `estado-enfraquecido/estado-enfraquecido-16.aseprite` (só o 16) | espada, seta, contorno | 1.159.0 |
| estado-frenesi (o ícone do estado Frenesi, `Icones.estado("frenesi")`): as três garras vermelhas crescentes (a primeira rodada) | `estado-frenesi/estado-frenesi-16.aseprite` (só o 16) | garras, contorno | 1.159.0 |
| estado-veneno (o ícone do estado Veneno, `Icones.estado("veneno")`): a gota verde sem a poça (a `estado-veneno-gota2` da terceira rodada) | `estado-veneno/estado-veneno-16.aseprite` (só o 16) | gota, contorno | 1.160.0 |
| estado-atordoado (o ícone do estado Atordoado, também o congelado, `Icones.estado("atordoado")`): as três estrelinhas em arco (a `estado-atordoado-estrelas`) | `estado-atordoado/estado-atordoado-16.aseprite` (só o 16) | estrelas, contorno | 1.160.0 |
| estado-barreira (o ícone do estado Barreira, `Icones.estado("barreira")`): o golpe na película (a `estado-barreira-impacto`) | `estado-barreira/estado-barreira-16.aseprite` (só o 16) | pelicula, impacto, contorno | 1.160.0 |
| estado-provocando (o ícone do estado Provocando, `Icones.estado("provocando")`): a figura branca com as três setas vermelhas convergindo (a `estado-provocando-claro`, o acabamento do busto do `b17ab3dd`) | `estado-provocando/estado-provocando-16.aseprite` (só o 16) | figura, setas, contorno | 1.161.0 |
| estado-iniciativa (o ícone do estado Iniciativa, `Icones.estado("iniciativa")`): a exclamação dourada de barra larga (a `estado-iniciativa-cunha` da terceira rodada) | `estado-iniciativa/estado-iniciativa-16.aseprite` (só o 16) | exclamacao, contorno | 1.161.0 |
| retrato-afogado (a cabeça do Afogado, `Icones.criatura("afogado")`, pela família): de frente e magro, metade do rosto até o osso (a `afogado-cranio`, opção C da terceira rodada, sem retoque) | `retrato-afogado/retrato-afogado-16.aseprite` (o 32 e o 48 são o 16 ×2 e ×3, `DERIVADOS`) | roupa, pele, osso, rosto, cabelo | 1.162.0 |
| retrato-ilse (a cabeça da Ilse da capela, `Icones.criatura("ilse")`, pela chave): a transposição da referência gerada (a `ilse-r3`, com o olho claro 1 px para a esquerda) | `retrato-ilse/retrato-ilse-16.aseprite` (o 32 e o 48 são o 16 ×2 e ×3, `DERIVADOS`) | guia (a referência reduzida, oculta: fora da exportação), vestido, rosto, algas | 1.162.0 |
| retrato-lobo (a cabeça do Lobo, `Icones.criatura("lobo")`, pela família): de frente, com o começo do pescoço (o `lobo-a-base` da segunda rodada, sem três sobras soltas) | `retrato-lobo/retrato-lobo-16.aseprite` (o 32 e o 48 são o 16 ×2 e ×3, `DERIVADOS`) | pelagem, focinho, detalhes | 1.163.0 |
| retrato-bandido (a cabeça do Bandido, `Icones.criatura("bandido")`, pela família): o capuz, a máscara vermelha e a faca (o `bandido-faca` da segunda rodada, sem retoque) | `retrato-bandido/retrato-bandido-16.aseprite` (o 32 e o 48 são o 16 ×2 e ×3, `DERIVADOS`) | capuz, pele, mascara, rosto, faca, mao | 1.163.0 |
| retrato-urso (o Urso Pardo do patrulheiro, `Icones.animal("urso")`, pelo tipo): de frente, severo (o `urso-t2`, a transposição da referência gerada) | `retrato-urso/retrato-urso-16.aseprite` (o 32 é o 16 ×2, `DERIVADOS`) | guia (a referência reduzida, oculta: fora da exportação), pelagem, focinho, detalhes | 1.164.0 |
| figura-lobo (o Lobo Cinzento deitado na fogueira, `Icones.figuraAnimal("lobo")`, pelo tipo; o urso e o falcão com as figuras deles desde a 1.176.0): o corpo da r5 com a cabeça em três quartos para o jogador (a `animal-lobo-c2`, sem retoque) | `figura-lobo/figura-lobo-16.aseprite` (só o 16; a cena o desenha na escala dela) | guia (a referência reduzida, oculta), corpo, cabeca, detalhes | 1.170.0 |
| figura-urso (o Urso Pardo sentado na fogueira, `Icones.figuraAnimal("urso")`, pelo tipo): o corpo inteiro, a cabeça larga e o focinho curto, o corcunda, as patas de base larga (a `animal-urso-r4` do `acampamento_atacar`, sem retoque) | `figura-urso/figura-urso-16.aseprite` (só o 16) | corpo, cabeca, detalhes | 1.176.0 |
| figura-falcao (o Falcão Peregrino no toco, na fogueira, `Icones.figuraAnimal("falcao")`, pelo tipo): a ave pousada de frente, o capuz escuro, o peito claro, o toco embaixo (a `animal-falcao` do `acampamento_atacar`, sem retoque) | `figura-falcao/figura-falcao-16.aseprite` (só o 16) | toco, corpo, cabeca, detalhes | 1.176.0 |
| retrato-falcao (o Falcão Peregrino do patrulheiro, `Icones.animal("falcao")`, pelo tipo): de perfil, a máscara escura (o `falcao-t2`) | `retrato-falcao/retrato-falcao-16.aseprite` (o 32 é o 16 ×2, `DERIVADOS`) | guia (oculta), plumagem, mascara, peito, bico, olho | 1.164.0 |
| retrato-troll (o Troll da montanha, `Icones.criatura("troll")`, pela família; o Rei Troll fora): de carne, em três quartos (o `troll-1` da segunda rodada, sem retoque) | `retrato-troll/retrato-troll-16.aseprite` (o 32 e o 48 são o 16 ×2 e ×3, `DERIVADOS`) | guia (a referência reduzida, oculta), roupa, pele, presas, rosto | 1.166.0 |
| retrato-rei-troll (o Rei Troll, `Icones.criatura("rei_troll")`, pelo id do guardião): o Troll 2 de frente com a coroa dourada (o `rei-troll-ouro2`, sem retoque) | `retrato-rei-troll/retrato-rei-troll-16.aseprite` (o 32 e o 48 são o 16 ×2 e ×3, `DERIVADOS`) | guia (oculta), roupa, pele, presas, rosto, coroa | 1.167.0 |
| retrato-aranha (a Aranha gigante, `Icones.criatura("aranha")`, pela família, com as invocadas; a Rainha fora): de perto, as quelíceras e as presas curtas (a `aranha-2b`, sem retoque) | `retrato-aranha/retrato-aranha-16.aseprite` (o 32 e o 48 são o 16 ×2 e ×3, `DERIVADOS`) | guia (oculta), patas, corpo, quelíceras, presas, olhos | 1.167.0 |
| retrato-sapo (o Sapo-touro gigante, `Icones.criatura("sapo")`, pela família): de frente, a cabeçorra com a sobrancelha pesada e a boca caindo (a `sapo-a` dos quatro pares, sem retoque) | `retrato-sapo/retrato-sapo-16.aseprite` (o 32 e o 48 são o 16 ×2 e ×3, `DERIVADOS`) | corpo, barriga, olhos, manchas | 1.171.0 |
| retrato-sanguessuga (a Sanguessuga gigante, `Icones.criatura("sanguessuga")`, pela família): empinada, a ventosa de dentes sobre o corpo em anéis (a `sanguessuga-a`, sem retoque) | `retrato-sanguessuga/retrato-sanguessuga-16.aseprite` (o 32 e o 48, `DERIVADOS`) | agua, corpo, boca | 1.171.0 |
| retrato-cultista (o Cultista, `Icones.criatura("cultista")`, pela família, com os fiéis do Profeta e os da sacristia): o capuz vermelho-escuro de frente com a marca violeta (o `cultista-a` dos quatro pares, sem retoque) | `retrato-cultista/retrato-cultista-16.aseprite` (o 32 e o 48, `DERIVADOS`) | manto, rosto, marca | 1.172.0 |
| retrato-bruxa (a Bruxa do pântano, `Icones.criatura("bruxa")`, pela família `bruxa_brejo`): o chapéu de aba mole e o sorriso banguela (a `bruxa-b3` da segunda rodada, sem retoque) | `retrato-bruxa/retrato-bruxa-16.aseprite` (o 32 e o 48, `DERIVADOS`) | xale, cabelo, rosto, chapeu | 1.172.0 |
| retrato-rato (o Rato gigante, `Icones.criatura("rato")`, pela família): de frente com a cabeça baixa, os incisivos (o `rato-r2` da segunda rodada, sem retoque) | `retrato-rato/retrato-rato-16.aseprite` (o 32 e o 48, `DERIVADOS`) | corpo, pele, dentes, olhos | 1.172.0 |
| retrato-javali (o Javali selvagem, `Icones.criatura("javali")`, pela família): de frente em investida, as presas grossas em arco (o `javali-a3` da terceira rodada, sem retoque) | `retrato-javali/retrato-javali-16.aseprite` (o 32 e o 48, `DERIVADOS`) | corpo, focinho, presas, olhos | 1.173.0 |
| retrato-carnical (o Carniçal, `Icones.criatura("carnical")`, pela família): de frente, a boca aberta com a arcada e o sangue (o `carnical-a3`, sem retoque) | `retrato-carnical/retrato-carnical-16.aseprite` (o 32 e o 48, `DERIVADOS`) | corpo, rosto, boca | 1.173.0 |
| retrato-espectro (o Espectro, `Icones.criatura("espectro")`, pela família): o capuz de névoa com a cavidade e o olho único, o pano continuando até a borda de baixo (o `espectro-ap` da terceira rodada, sem retoque; o corpo inteiro fica para a arte de cenário, pela referência `Espectro do Manto Inflado.png`) | `retrato-espectro/retrato-espectro-16.aseprite` (o 32 e o 48, `DERIVADOS`) | nevoa, vazio | 1.174.0 |
| retrato-esqueleto (o Esqueleto, `Icones.criatura("esqueleto")`, pela família, com os do ossuário e os que o Lich invoca): o guarda morto, a caveira sob o elmo de ferro com o nasal e a ferrugem, a malha nos ombros (o `esqueleto-e1r` do `esqueleto_novo`, sem retoque) | `retrato-esqueleto/retrato-esqueleto-16.aseprite` (o 32 e o 48, `DERIVADOS`) | ombros, cranio, elmo, cavidades | 1.175.0 |
| retrato-mercenario (o Mercenário, `Icones.criatura("mercenario")`, pela família, com o Invicto da ponte e o Theodore dos Cães de Ferro): o chapéu de ferro de aba larga, os olhos na sombra da aba, a barba por fazer, o gibão ocre e a malha nos ombros (o `mercenario-ma` do `mercenario_lobo_gelido`, sem retoque) | `retrato-mercenario/retrato-mercenario-16.aseprite` (o 32 e o 48, `DERIVADOS`) | roupa, rosto, elmo | 1.179.0 |
| retrato-lobo-gelido (o Lobo Gélido, `Icones.criatura("lobo_gelido")`, pela família): a construção do Lobo, a pelagem clara azulada, os olhos de gelo e a juba de pontas brancas (o `lobo-gelido-la`, sem retoque) | `retrato-lobo-gelido/retrato-lobo-gelido-16.aseprite` (o 32 e o 48, `DERIVADOS`) | pelagem, focinho, detalhes | 1.179.0 |
| retrato-rainha-aracnidea (a Rainha Aracnídea, `Icones.criatura("rainha_aracnidea")`, pelo id da guardiã; as aranhas que ela invoca no retrato da Aranha): de frente e enorme, o abdome com a ampulheta vermelha, as presas vermelhas (a `rainha-a`, sem retoque) | `retrato-rainha-aracnidea/retrato-rainha-aracnidea-16.aseprite` (o 32 é o 16 ×2, `DERIVADOS`; só a carta da luta) | patas, corpo, marca, presas, olhos | 1.168.0 |
| martelo (o Martelo do Guerreiro): **só o 40 e o 48**; o 32 e o 64 são a grade de `rpg/web/static/desenhos.js` | `martelo/martelo-40.aseprite`, `-48` | cabo, empunhadura, pomo, colar, cabeca, contorno | 1.149.0 |
| diadema (o Diadema do Mago, também a Coroa dos Afogados por ora; o desenho `coroa`) | `diadema/diadema-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | aro, placa, gema, contorno | 1.144.0 |
| sandalia (a Sandália do Mago, o par) | `sandalia/sandalia-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | tras_sola, tras_palmilha, tras_tiras, frente_sola, frente_palmilha, frente_tiras, contorno | 1.142.0 |
| amuleto (o amuleto: Amuleto, Talismã, Pingente e Medalhão; o vazio) | `amuleto/amuleto-32.aseprite`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | cordao, argola, engaste, pedra, brilho, contorno | 1.140.0 |
| antidoto (o Antídoto) | `antidoto/antidoto-16.aseprite`, `-32` | vidro, liquido, rolha, brilho, contorno | 1.139.0 |
| frasco_vazio (o topo sem poções) | `frasco_vazio/frasco_vazio-24.aseprite` | vidro, rolha, brilho, contorno | 1.139.0 |
| tocha_apagada (o topo sem tochas e o risco "Sem luz") | `tocha_apagada/tocha_apagada-16.aseprite`, `-24` | cabo, pano, queimado, contorno, fumaca | 1.136.0 |
| atalho-salvar (o Salvar da doca) | `atalho-salvar/atalho-salvar-36.aseprite`, `-32` | tampa, corpo, latao, seta, contorno | 1.129.0 |
| atalho-sair (o Sair da doca) | `atalho-sair/atalho-sair-36.aseprite`, `-32` | arco, passagem, seta, contorno | 1.129.0 |
| atalho-bestiario (o Bestiário da doca) | `atalho-bestiario/atalho-bestiario-36.aseprite`, `-32` | chifres, cranio, contorno | 1.128.0 |
| atalho-talentos (os Talentos da doca) | `atalho-talentos/atalho-talentos-36.aseprite`, `-32` | galhos, nos, contorno | 1.127.0 |
| atalho-comitiva (a Comitiva da doca) | `atalho-comitiva/atalho-comitiva-36.aseprite`, `-32` | tras_esquerda, tras_direita, frente, contorno | 1.127.0 |
| atalho-grimorio (o Grimório da doca e o Habilidades da luta) | `atalho-grimorio/atalho-grimorio-36.aseprite`, `-32` | contracapa, folhas, lombada, capa, emblema, cravos, fita, contorno | 1.126.0 |
| atalho-diario (o Diário da doca) | `atalho-diario/atalho-diario-36.aseprite`, `-32` | capa, paginas, anotacoes, fita, pena, contorno | 1.125.0 |
| atalho-mapa (o Mapa da doca) | `atalho-mapa/atalho-mapa-36.aseprite`, `-32` | espessura, papel, vincos, terreno, percurso, destino, contorno | 1.124.0 |
| aljava (a aljava do Patrulheiro e as flechas do topo) | `aljava/aljava-24.aseprite`, `-32`, `-40`, `-48`; **o 64 é o 32 ampliado 2×** | alca, couro, cintas, latao, boca, hastes, penas, contorno | 1.122.0 |
| attr-agilidade (a Agilidade e o Fugir) | `attr-agilidade/attr-agilidade-24.aseprite`, `-32`; **o 64 é o 32 ampliado 2×** | rastros, sola, bota, dobra, tira, fivela, contorno | 1.121.0 |

A varinha é a aprovada pelo Jean (commit `451ff11`): a haste com o mesmo perfil nos quatro tamanhos e a pedra
compacta (quadrada, de cantos cortados) também no 32. A camada `garras` do 32 fica vazia (lá a garra é um pixel da
taça). As rodadas, as tentativas descartadas e as fotos estão em `ferramentas/prototipos/hud/varinha-aseprite/`
(histórico: os `.aseprite` de lá são cópias das rodadas, não a fonte).

O gibão e as botas são os aprovados pelo Jean na rodada 2 (commit `9d49726`). Neste lote, **o 32 é a fonte do 64**:
o 64 do jogo é o 32 final ampliado exatamente 2× por vizinho mais próximo, sem retoque (a escolha do Jean depois de
comparar no cartão do saque). Os 64 desenhados à parte (`historico/gibao-64-trabalhado.aseprite`,
`historico/bota-64-trabalhado.aseprite`) ficam como histórico, fora da exportação. As rodadas estão em
`ferramentas/prototipos/hud/couro-aseprite/`.

A cabeça e as mãos de couro e de tecido são as aprovadas pelo Jean (registro em `df01f5a`): o capuz de couro revisado
(rodada 2), a luva de couro com braçadeira (rodada 1), a luva de seda (rodada 2) e o capuz de tecido da rodada 3
(`1c061e1`); os 32 são cópias exatas dessas fontes e o 64 de cada um é o 32 ampliado 2×. Os 40 e 48 (rodada 4) saem da
mesma construção de cada peça, escrita para qualquer grade (`ferramentas/prototipos/hud/couro2-aseprite/auxiliares/
couro2_r4.py`, que no 32 reproduz o aprovado pixel a pixel), pintados pelo `pintar.lua`. As rodadas estão em
`ferramentas/prototipos/hud/couro2-aseprite/`.

**O conector, a linha de comando e as sessões (diagnóstico de 21/10/2026).** São três peças: o bridge (um processo
`node .../aseprite-mcp-bridge/dist/index.js` que cada sessão do Claude sobe pelo `stdio`, escutando
`ws://127.0.0.1:6515`), a extensão do Aseprite (Aseprite MCP Pro 1.0.0, que disca para a 6515 e tenta de novo a cada
3 s) e o editor aberto. O que foi confirmado:

- **"Connection closed" ao abrir uma sessão:** só um bridge pode escutar a 6515. Se outra sessão do Claude, mesmo
  parada (por exemplo, uma de antes de uma troca de conta), ainda tem o bridge dela, o desta sessão sai na hora com
  `listen EADDRINUSE 127.0.0.1:6515`, e o painel mostra "Connection closed". Diagnóstico: `Get-NetTCPConnection
  -LocalPort 6515` dá o processo que escuta; o pai dele (`Win32_Process`, `ParentProcessId`) diz de qual `claude.exe` ele
  é. Recuperação: encerrar só aquele `node` do bridge (nunca todos os `node`), e reconectar o `aseprite-bridge` pelo
  `/mcp` da sessão que vai usar.
- **A linha de comando derrubava o editor:** cada `aseprite -b` (o exportador, a conferência, a montagem das fontes)
  carregava a extensão, que também discava para a 6515; o bridge adota o cliente mais novo e fecha o anterior, o do
  editor. Corrigido por um ajuste local na extensão instalada: sem interface (`app.isUIAvailable` falso) ela não conecta.
- **O editor que não voltava:** depois de perder a conexão (o bridge caiu ou foi substituído), a extensão podia ficar com
  um socket que nunca abria nem avisava o fechamento, e o temporizador não discava mais (70 s sem nenhuma tentativa,
  medido). O mesmo ajuste recria a conexão depois de dois ciclos desconectado.

O ajuste local fica em `%APPDATA%\Aseprite\extensions\aseprite-mcp-pro\plugin.lua` (só a máquina do Jean; não é do
repositório). O original e a diferença estão no bridge: `Tools\aseprite-mcp-bridge\backups\plugin.lua.orig` e
`Tools\aseprite-mcp-bridge\patches\0002-extensao-sem-conexao-em-lote-e-reconexao.patch`. Reinstalar ou atualizar a
extensão desfaz o ajuste: reaplique o patch. O editor só carrega a extensão ao abrir.

Conferido depois do ajuste, com o editor reaberto e um bridge na 6515 (MCP pelo stdio → bridge → WebSocket →
extensão): `get_version` (1.0.0, 121 comandos), `list_open_sprites`, a captura de uma cópia temporária, o `pintar.lua`
pelo `execute_script` com a releitura (os dois pixels pintados e nenhum outro mudado na captura), e uma exportação
`aseprite -b` no meio, seguida de `get_version` logo depois, a 1 s e a 4 s, sem nenhuma desconexão (o lote não tenta
mais conectar). Cuidado: o `close_sprite` por nome falha quando o Aseprite guardou o caminho curto do Windows
(`JEANWR~1`); feche pelo documento ativo, conferido antes com o `list_open_sprites` (o campo é `is_active`).

## Exportar os PNGs e os @2x

    python ferramentas/arte/exportar_aseprite.py varinha             # grava no jogo (só na integração ou num ajuste aprovado)
    python ferramentas/arte/exportar_aseprite.py varinha <pasta>     # grava numa pasta qualquer (uma proposta)
    python ferramentas/arte/exportar_aseprite.py varinha --conferir  # compara com os do jogo, byte a byte e pixel a pixel

    python ferramentas/arte/exportar_aseprite.py gibao               # o gibão: 32, 40, 48 das fontes e o 64 derivado
    python ferramentas/arte/exportar_aseprite.py todas --conferir    # todas as peças: reproduz e compara os 24 arquivos

O 1× sai da linha de comando do Aseprite (`-b <fonte> --save-as <png>`: o composto das camadas visíveis); o @2x é a
duplicação exata do 1× (vizinho mais próximo, pelo Pillow), como o `salvar` de `../pixel_comum.py`. O executável vem
de `ASEPRITE=<executável>`, de `aseprite` no PATH ou do lugar de instalação comum (Steam). Na integração da 1.109.0, os
oito arquivos exportados saíram idênticos, byte a byte, aos aprovados.

Os tamanhos derivados são explícitos por peça na tabela `DERIVADOS` do exportador (lado: lado da fonte e fator
inteiro): no gibão e nas botas, `64: (32, 2)`. O derivado sai do PNG exportado da fonte, ampliado pelo vizinho mais
próximo, e o @2x dele é a duplicação exata. Uma peça fora da tabela (a varinha) exporta cada fonte que tem. O
`--conferir` reproduz todos os arquivos numa pasta temporária, compara com os do jogo e confere que cada derivado,
reduzido pegando um pixel de cada bloco, volta exatamente à fonte. Na integração da 1.110.0, os dezesseis arquivos do
couro saíram idênticos, byte a byte, aos escolhidos.

Mexeu numa fonte? Exporte para uma pasta, confira em tamanho real (`../prancha.py`) e no jogo
(`../fotografar_itens.mjs`, `SO=varinha`), e só então grave no jogo.

## Pintar pelo MCP: `pintar.lua`

`pintar.lua` é o caminho de pintura verificado para o conector `aseprite-mcp-bridge` (extensão 1.0.0), pelo
`execute_script`:

    local P = dofile("<raiz>/ferramentas/arte/aseprite/pintar.lua")
    return P.pintar("haste", "12,30,7A3824;13,29,974B31")     -- ou P.pintar_arquivo("haste", "<lista>.lua")
    return P.ler("haste")                                      -- os opacos da camada, em coordenadas do documento
    return P.camadas()                                         -- ordem, nome, visibilidade, pixels de cada camada

Por que não o `put_pixels` do conector (medido em 16/10/2026): ele descarta em silêncio o pixel fora do retângulo da
cel (a cel que o lápis do Aseprite cria, uma cel deslocada ou parcialmente fora da tela) e responde com o total
pedido; e escreve sem gerar desfazer. O `pintar.lua` cria uma imagem que cobre a cel antiga e a tela, copia o conteúdo
no mesmo lugar do documento, pinta por cima e troca a imagem da cel numa transação (um passo de desfazer); recusa e
lista o pixel fora da tela; relê cada pixel depois de gravar.

Cuidados: as listas entram por `dofile` (um `.lua` que só faz `return "<lista>"`); `io.open` e `sprite:saveCopyAs`
para PNG num `execute_script` abrem uma janela do Aseprite e travam o conector. Para exportar, use a ferramenta
`export_png` do conector ou o `exportar_aseprite.py`.

A Calça de Couro (1.119.0) é a aprovada pelo Jean no commit `ee0f01a`. As camadas saem de
`ferramentas/arte/desenhar_calca_couro_pixel.py --listas` e foram montadas pela linha de comando do Aseprite
(`ferramentas/prototipos/hud/itens-lote-noite/calca_couro/montar_fontes.sh`, com o `pintar.lua`). Os oito arquivos do
jogo são idênticos, pixel a pixel, aos aprovados, e `exportar_aseprite.py calca_couro --conferir` os reproduz byte a
byte.

## Montar as fontes a partir de um script de desenho (1.120.0)

Quando o desenho nasce num script de `ferramentas/arte/` (o método de `pixel_comum.py`), a fonte em camadas sai dele:

    python ferramentas/arte/desenhar_attr_ataque_pixel.py <pasta> --listas   # as listas por camada (pixel_comum.listas_camadas)
    python ferramentas/arte/montar_fontes.py attr-ataque <pasta>/listas      # aseprite/attr-ataque/attr-ataque-<lado>.aseprite
    python ferramentas/arte/exportar_aseprite.py attr-ataque --conferir      # o composto exportado = o jogo, byte a byte

- **As listas:** o script marca a camada de cada pixel (as `CAMADAS` dele). `listas_camadas` grava um `.lua` por
  camada e a ordem (`ordem.txt`).
- **A montagem:** `montar_fontes.py` roda o Aseprite em lote (`aseprite/montar_camadas.lua`, com o `pintar.lua`) para
  cada tamanho e mostra a releitura de cada camada.
- **Os espaços no caminho:** com um espaço no caminho do script, o Aseprite não o executa e não avisa. O
  `montar_fontes.py` copia o `.lua` para uma pasta temporária e passa o `pintar.lua` por parâmetro.
- **Na integração da 1.120.0:** os doze arquivos de Ataque e Defesa exportados das fontes saíram idênticos, pixel a
  pixel, aos aprovados (`b8637d0`).
- **A calça de couro:** foi montada pela versão de protótipo deste fluxo (`itens-lote-noite/calca_couro/`).

## A Agilidade (1.121.0)

A bota em passada é a aprovada pelo Jean (`e9b0499`, a sola corrigida). As fontes vieram do protótipo
(`ferramentas/prototipos/hud/itens-lote-noite/agilidade_aljava_ref/`), desenhadas em grade à mão e pintadas no editor
pelo `pintar.lua`. Os seis arquivos exportados delas são idênticos, byte a byte, aos aprovados, e
`exportar_aseprite.py attr-agilidade --conferir` os reproduz.

## A aljava (1.122.0)

**A origem:** é a direção nova, feita a partir da referência do Jean (`ferramentas/prototipos/hud/itens-lote-noite/
agilidade_aljava_ref/`):
- 24 e 32 aprovados em `ea3835f`;
- 40 e 48, derivados da construção do 32, em `fb403f5`;
- o 64 é o 32 ampliado 2×.

**As fontes:** desenhadas em grade à mão e pintadas no editor pelo `pintar.lua`. Os dez arquivos exportados delas são
idênticos, byte a byte, aos aprovados.

**O script antigo:** `desenhar_aljava_pixel.py` é a direção anterior, guardada como histórico, e só grava numa pasta.

## O Poder (1.123.0)

A chama violeta é a da rodada 2, aprovada pelo Jean (`c0dbab8`, `ferramentas/prototipos/hud/itens-lote-noite/poder_r2/`).
Foi desenhada em grade à mão e pintada no editor pelo `pintar.lua`. Os seis arquivos exportados das fontes são
idênticos, byte a byte, aos aprovados, e `exportar_aseprite.py attr-poder --conferir` os reproduz. O
`desenhar_attr_poder_pixel.py` é o candidato anterior, não aprovado, e fica como histórico: só grava numa pasta.

## O Inventário e o Mapa da doca (1.124.0)

Os primeiros atalhos da doca em pixel art: a mochila e o mapa dobrado da rodada 2. Jean os aprovou no `c02e566`, e eles
estão em `ferramentas/prototipos/hud/itens-lote-noite/doca_r2/`.

**As fontes:** o 36 (o da doca) e o 32 (as janelas estreitas), sem tamanho derivado. Foram desenhadas em grade à mão;
a camada de cada pixel vem do mapa de camadas, e a pintura no editor foi pelo `pintar.lua`.

**Conferido:** os oito arquivos exportados delas são idênticos, byte a byte, aos aprovados, e
`exportar_aseprite.py atalho-inventario --conferir` (e `atalho-mapa`) os reproduz. O `desenhar_doca_pixel.py` é a
primeira proposta, recusada, e fica como histórico.

## O Diário da doca (1.125.0)

O livro aberto com a pena e a fita é o da rodada 3 da doca, aprovado pelo Jean no `666b806`
(`ferramentas/prototipos/hud/itens-lote-noite/doca_r3/`). Tem o 36 e o 32, sem derivado. Os quatro arquivos exportados
das fontes são idênticos, byte a byte, aos aprovados, e `exportar_aseprite.py atalho-diario --conferir` os reproduz.

## O Grimório da doca (1.126.0)

O livro violeta fechado e inclinado, com a estrela de latão, é a rodada 3 da doca, aprovada pelo Jean no `61dcb81`
(`ferramentas/prototipos/hud/itens-lote-noite/doca_r3/`; o modelo do livro está em `auxiliares/grimorio_livro.py`).
- **Os usos:** o atalho da doca e o comando Habilidades da roda da luta (`ACAO.grimorio`, o 32).
- **Conferido:** os quatro arquivos exportados das fontes são idênticos, byte a byte, aos aprovados, e
  `exportar_aseprite.py atalho-grimorio --conferir` os reproduz.
- **As rodadas recusadas** estão no protótipo: `doca_r3/grimorio_r1/` e `grimorio_r2/`.

## Os Talentos e a Comitiva da doca (1.127.0)

Os dois são da rodada 4 da doca, aprovada pelo Jean no `4deb386` (`ferramentas/prototipos/hud/itens-lote-noite/doca_r4/`).
- **Os arquivos:** os oito exportados das fontes são idênticos, byte a byte, aos aprovados, e `exportar_aseprite.py
  <peça> --conferir` os reproduz.
- **A Comitiva:** ganhou papel próprio em `Icones` (`ATALHO`, `TAMANHOS`). O contorno dela está desenhado na camada
  `contorno`, também entre as figuras.

## O Bestiário da doca (1.128.0)

O crânio de fera com chifres foi aprovado pelo Jean no `e373618` (`ferramentas/prototipos/hud/itens-lote-noite/doca_r5/`).
- **As fontes:** são as `.aseprite` editadas no editor pelo MCP. As rodadas 3 e 4 (a parte de baixo e a ligação entre o
  focinho e a arcada) foram retocadas nelas, e as grades do protótipo ficam como histórico.
- **Conferido:** os quatro arquivos exportados são idênticos, byte a byte, aos aprovados, e
  `exportar_aseprite.py atalho-bestiario --conferir` os reproduz.

## O Salvar e o Sair da doca (1.129.0): a doca concluída

O baú aberto e o arco de pedra foram aprovados pelo Jean (`a872915`, reapresentados sem mudança no `682b189`;
`ferramentas/prototipos/hud/itens-lote-noite/doca_r5/`).
- **Conferido:** os oito arquivos exportados das fontes são idênticos, byte a byte, aos aprovados.
- **A doca:** com eles, os nove atalhos estão em pixel art: Talentos, Grimório, Inventário, Comitiva, Mapa, Diário,
  Bestiário, Salvar e Sair.

## A Vida e a Mana do topo (1.130.0)

O coração (`a914f18`) e a gota sem o miolo aceso (`f02566d`) foram aprovados pelo Jean
(`ferramentas/prototipos/hud/itens-lote-noite/vida_mana/`; a gota da rodada 1 em `vida_mana/mana_r1/`).
- **O uso:** só o topo, em 20 (`Icones.vital`); não há outro tamanho.
- **Conferido:** os quatro arquivos exportados das fontes são idênticos, byte a byte, aos aprovados.
- **Os auxiliares** que geraram as listas por camada ficam em `vida_mana/auxiliares/` (`vida.py`, `mana.py`).

## O Vigor e o Foco do topo (1.131.0): os quatro recursos concluídos

O punho cerrado sem fogo (`4eea5b6`) e o alvo verde (`1a1dae3`, reapresentado sem mudança no `4eea5b6`) foram
aprovados pelo Jean (`ferramentas/prototipos/hud/itens-lote-noite/vigor_foco/`; as rodadas recusadas em
`vigor_foco/recusados/`).
- **O uso:** só o topo, em 20 (`Icones.vital`); não há outro tamanho.
- **Conferido:** os quatro arquivos exportados das fontes são idênticos, byte a byte, aos aprovados.
- **Os auxiliares** que geraram as listas por camada ficam em `vigor_foco/auxiliares/` (`punho/`: `e2_partes.py` e
  depois `e3_sem_fogo.py`; `foco.py`).
- **Com eles,** os quatro ícones das barras do topo (Vida, Mana, Vigor, Foco) estão em pixel art.

## O Ouro e as Provisões (1.132.0)

A pilha de moedas e o pernil sem barbantes foram aprovados pelo Jean no `33d8a6c`
(`ferramentas/prototipos/hud/itens-lote-noite/ouro_provisoes/`; a versão com barbantes em `ouro_provisoes/recusados/`).
- **As fontes:** `moedas/moedas-24.aseprite` (camadas pilha, topo, moeda, contorno) e `provisoes/provisoes-24.aseprite`,
  `-32` (carne, osso, contorno).
- **Os usos:** o Ouro no topo, em 24; as Provisões no topo, em 24, e no cartão do mercado, em 32 nativo (`TAMANHOS`
  [24, 32]).
- **O Ouro do balcão (1.133.0):** o seu ouro no mercado e nos serviços (`.ouro-loja`, 32) passou do sprite `moedas` do
  jogo para a pilha aprovada, com uma fonte de 32 (`moedas/moedas-32.aseprite`, as mesmas quatro camadas) derivada da
  construção do 24: as medidas escaladas por 4/3 e as moedas da pilha com 3 px de altura em vez de 2. As listas saem do
  `ouro_provisoes/auxiliares/ouro.py final 32` (que no 24 reproduz o aprovado pixel a pixel), pintadas pelo
  `pintar.lua` (0 diferentes, 0 fora da tela); o composto do editor, as listas e o exportado são iguais, e o @2x é a
  duplicação exata. Sem retoque.
- **Conferido:** os seis arquivos exportados das fontes são idênticos, byte a byte, aos aprovados, e
  `exportar_aseprite.py moedas|provisoes --conferir` os reproduz.
- **Os auxiliares** que geraram as listas por camada ficam em `ouro_provisoes/auxiliares/` (`ouro.py`, `pernil.py`).

## A moeda avulsa (1.134.0)

A moeda de frente, com a espessura embaixo à direita, foi aprovada pelo Jean no `c00d0cf`, nos dois tamanhos
(`ferramentas/prototipos/hud/itens-lote-noite/moeda_tocha/`).
- **Os usos:** em 16, os preços, os custos, o prêmio e os ganhos dos contratos, o chip e o aviso de ouro e as moedas
  que voam até o topo; em 32, o espólio e a moeda que o ladrão leva. A pilha do saldo (`moedas`) não muda.
- **Conferido:** os quatro arquivos exportados das fontes são idênticos, byte a byte, aos aprovados, e
  `exportar_aseprite.py moeda --conferir` os reproduz.
- **Os auxiliares** que geraram as listas por camada ficam em `moeda_tocha/auxiliares/` (`moeda.py <16|32>`).

## A tocha (1.135.0)

A rodada 2, com a chama refinada, foi aprovada pelo Jean no `1c6a2c2` (`ferramentas/prototipos/hud/itens-lote-noite/
moeda_tocha/`; a rodada 1 em `moeda_tocha/tocha_r1/`).
- **Os usos:** o topo (24) e, em 32, o cartão do mercado, a bolsa, o espólio e o voo até a bolsa. Só esses tamanhos:
  os 48 e 64 antigos saíram do jogo, sem uso. A tocha em 16 (o chip, o aviso, as escolhas) continua o sprite do jogo.
- **Conferido:** os quatro arquivos exportados das fontes são idênticos, byte a byte, aos aprovados, e
  `exportar_aseprite.py tocha --conferir` os reproduz.
- **Os auxiliares** que geraram as listas por camada ficam em `moeda_tocha/auxiliares/` (`tocha.py <24|32>`, a
  rodada 2; a 1 em `tocha_r1/tocha_r1.py`).

## A tocha em 16 e a tocha apagada (1.136.0)

As três variantes do `ef71aa3` foram aprovadas pelo Jean (`ferramentas/prototipos/hud/itens-lote-noite/moeda_tocha/
variantes/`).
- **Os usos:** a tocha em 16, o chip e o aviso de um item ganho, o ícone das escolhas que a gastam, o risco "−1
  tocha" e o aviso de escuro do painel do lugar; a apagada em 24, o topo sem tochas (no lugar do sprite em 32), e em
  16, o risco "Sem luz" e o aviso do lugar sem tocha. O 24 e o 32 da
  tocha não mudaram.
- **Conferido:** os seis arquivos exportados das fontes são idênticos, byte a byte, aos aprovados, e
  `exportar_aseprite.py tocha --conferir` e `tocha_apagada --conferir` os reproduzem (com o 24 e o 32).
- **Os auxiliares:** `moeda_tocha/auxiliares/tocha.py <16|24|32> [apagada]`.

## A Bandagem, a Poção de Vida, o Tônico, a Calça de Viagem e o Manto (1.138.0)

Aprovados pelo Jean sem retoque: a Bandagem e a Poção no `211b8e2`, o Tônico no `d401a92`, a Calça de Viagem e o Manto
no `c63f84b` (`ferramentas/prototipos/hud/itens-lote-noite/bandagem_pocao/`, `tonico_antidoto/`, `calca_manto/`).
- **Conferido:** os 46 arquivos exportados das fontes são idênticos, byte a byte, aos aprovados (o 64 da calça e do
  manto pelo `DERIVADOS`), e o `--conferir` de cada peça os reproduz.
- **Na família de ferro:** a bandagem, a poção e o tônico passaram a ter fonte aqui e saem sozinhos do
  `familia_ferro.py` (continuam na conta da escala do grupo).
- **Os auxiliares:** `bandagem_pocao/auxiliares/bandagem.py`, `frasco.py` (a família de frascos), `calca_manto/auxiliares/tecido.py`.

## O Antídoto e o frasco vazio (1.139.0)

O Antídoto com a base plana e o frasco vazio foram aprovados pelo Jean no `b872544` (`tonico_antidoto/`,
`bandagem_pocao/variantes/`).
- **Os usos:** o Antídoto em 32 nos consumíveis e em 16 pelo item (o chip, o aviso, as escolhas); o frasco vazio no
  topo sem poções (24, `RECURSO`). Os 48 e 64 antigos do Antídoto saíram (sem uso).
- **Conferido:** os seis arquivos exportados das fontes são idênticos, byte a byte, aos aprovados, e o `--conferir` os
  reproduz.
- **Os auxiliares:** `bandagem_pocao/auxiliares/frasco.py antidoto|frasco_vazio <N>`.

## O anel e o amuleto (1.140.0)

O anel da rodada 3 (com o ziguezague gravado) e o amuleto violeta da rodada 2 foram aprovados pelo Jean no `9ae59a9`
(`ferramentas/prototipos/hud/itens-lote-noite/anel_amuleto/`; a alternativa lisa do anel em `rodada3_liso/` e as rodadas
recusadas em `rodada1/` e `rodada2/` ficam como histórico).
- **Os usos:** o anel para o Anel, o Sinete, o Aro e o Anel do Último Rei; o amuleto para o Amuleto, o Talismã, o
  Pingente e o Medalhão; os espaços vazios com as mesmas imagens, apagadas. 32, 40, 48 e o 64 = 32 ×2 (`DERIVADOS`).
- **Conferido:** os 16 arquivos exportados das fontes são idênticos, byte a byte, aos aprovados, e o `--conferir` os
  reproduz; os dois saíram sozinhos da conferência da família de ferro (fonte no Aseprite).
- **Os auxiliares:** `anel_amuleto/auxiliares/aro.py <N>` (o anel: o aro como um cilindro curto; `ajuste_aro.py`, a
  busca do ângulo pela referência principal) e `joias.py amuleto <N>`. As referências permanentes:
  `ferramentas/arte/referencias/aneis/`.
