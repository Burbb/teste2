# Os seis chefes restantes e os três retratos especiais (23/10/2026, propostas; nada no jogo)

**Pedido do Jean (o lote da noite):** depois da integração da Árvore Anciã R2b (1.190.0) e do Golem Primordial R1b
(`../chefes_arvore_golem/`), duas propostas de cada um dos seis chefes restantes e dos três retratos especiais, só no
protótipo. O aprendizado da rodada anterior vale como direção: o retrato pode mostrar o rosto de perto, com partes
continuando para fora do quadro. Nenhuma variante de fase. O Bandido do chapéu e o Esqueleto E2 continuam reservados:
consultados, não atribuídos (o Lich não usa capuz, que é a marca do E2; o Senhor da Guerra não usa chapéu).

## O que vem do jogo (conferido no código)

| Criatura | Onde e como | Números e habilidades | Textos |
|---|---|---|---|
| **Hidra do Brejo** (`hidra_do_brejo`, guardiã do pântano) | carta da luta, pelo id | 140 de vida; `fera`; Regenerar, Veneno, Mordida Sangrenta, Varredura | "A água ferve. Uma, duas, três cabeças de serpente emergem, sibilando em uníssono." Fase 2: "Onde uma cabeça foi cortada, duas novas brotam!" Rumor: "Escamas do tamanho de escudos boiam na água. E três trilhas paralelas de lodo." |
| **Dragão de Gelo** (`dragao_de_gelo`, montanha) | carta da luta | 130; `voador`; Mordida Gélida, Golpe Esmagador, Grito de Terror, Varredura; resiste ao gelo, fraco ao fogo | "Um dragão serpentino de escamas azul-gelo desdobra as asas sobre você." Fase 2: "O dragão inspira fundo e o ar congela ao seu redor!" |
| **Senhor da Guerra** (`senhor_da_guerra`, planície) | carta da luta | 130; `humano`, `blindado`; Golpe Sujo, Golpe Esmagador, Invocar (bandidos), Grito de Guerra, Varredura | "Um homem de armadura remendada com troféus de seus inimigos aguarda." Fase 2: "Ele joga fora o escudo e pega um machado em cada mão." Rumor: "Estacas com elmos espetados marcam a trilha." |
| **Profeta das Cinzas** (`profeta_das_cinzas`, planície) | carta da luta | 115; `humano`, `conjurador`; Bola de Sombra, Cura, Invocar (cultistas), Maldição | "Um círculo de fiéis entoa cânticos ao redor de um homem cego que chora cinzas." Fase 2: "O Profeta abre os braços e o Vazio responde ao seu chamado!" Rumor: "Cinzas caem do céu limpo. Cânticos distantes." |
| **Bruxa Afogada** (`bruxa_afogada`, pântano) | carta da luta | 110; `morto-vivo`, `conjurador`; Maldição, Bola de Sombra, Invocar (afogados), Drenar | "Uma mulher de pele azulada flutua sobre o charco, cabelos de algas escorrendo, cantando uma canção de ninar." Fase 2: "O canto vira um grito." |
| **Lich Menor** (`lich_menor`, ruínas) | carta da luta | 115; `morto-vivo`, `conjurador`; Bola de Sombra, Maldição, Invocar (esqueletos), Drenar | "Um esqueleto coroado ergue os olhos de um grimório. Duas chamas verdes acendem nas órbitas." Fase 2: "esmaga uma joia e sua forma se torna translúcida". |
| **Espantalho Possuído** (`eventos/biomas.py`, `espantalho`; família `ent_jovem`, origem `espantalho`) | carta inimiga da luta | os números da árvore desperta | "Um espantalho no meio de um milharal. Você poderia jurar que, há um momento, ele estava olhando para o outro lado." Com fogo: "A palha pega fogo e algo lá dentro GRITA." |
| **Mímico** (`eventos/comuns.py`, `bau_abandonado`; família `golem`, origem `mimico`) | carta inimiga da luta | os números do golem; Agarrão e Mordida Sangrenta | "O baú abre... uma BOCA. Dentes, língua, e uma fome antiga. É um mímico!" |
| **Servo esquelético** (o "Esqueleto (Invocado)" do Erguer Servo; `habilidades.py`) | carta aliada da luta, hoje no sprite `caveira` (`batalha.js`) | a vida e o ataque pelo Poder do Necromante; entra Provocando | "Você ergue um esqueleto dos ossos de um inimigo caído" (ou "da própria terra"). **O mesmo tipo `servo` vale para o inimigo que o talento Rei dos Mortos ergue** ("Lobo (servo)"): uma integração precisa decidir se ele também ganha esse retrato. |

**Tamanhos:** todos só aparecem na carta da luta (32), nenhum no Bestiário: o 16 e o 32, com os @2x (nenhum 48).

## A interpretação e as propostas

Os nove arquivos de grade em `auxiliares/grades.py`; as camadas de cada um dizem o que é (as escamas, a boca, os olhos;
a armadura, o rosto, a barba, os troféus; o manto, o crânio, a coroa, as chamas...).

- **Hidra:** **H1, as três cabeças** (de frente, a do meio maior e as duas laterais mais altas, os pescoços se juntando);
  **H2, a serpente de perto** (de perfil, achatada, a boca aberta com a língua bifurcada, a segunda cabeça atrás e a
  terceira cortada pela borda).
- **Dragão:** **D1, a cabeça de perfil** (o focinho longo, os chifres para trás, o olho pálido, o pescoço descendo);
  **D2, de frente** (os chifres grossos para trás, a faixa das órbitas, o focinho comprido com as narinas e as presas).
- **Senhor da Guerra:** **S1, o elmo e o troféu** (o elmo com o protetor de nariz, a barba, a cicatriz, a caveira presa
  na ombreira); **S2, o veterano caolho** (a cabeça raspada e marcada, a venda no olho, a barba pesada, o manto de pele e
  a lâmina do machado atrás do ombro).
- **Profeta das Cinzas:** **P1, o cego encapuzado** (o capuz cinza de cinzas, a venda branca, as lágrimas de cinza, a
  boca aberta no cântico, o violeta do Vazio na roupa); **P2, os olhos brancos** (a cabeça raspada, os olhos brancos
  virados, as cinzas escorrendo, as mãos erguidas nos cantos).
- **Bruxa Afogada:** **B1, a cantora** (de frente, a pele azul, os olhos fechados, a boca aberta no canto, as algas
  emoldurando o rosto); **B2, a cabeça na água** (a linha da água no meio do quadro, os olhos brancos, os cabelos de algas
  espalhados na superfície, o reflexo embaixo).
- **Lich Menor:** **L1, o rei-esqueleto** (de frente, a coroa fina, as chamas verdes nas órbitas, a gola alta do manto,
  o fecho de ouro; sem capuz); **L2, o grimório** (o crânio coroado olhando para baixo, o livro aberto e a mão de osso
  embaixo, a luz verde do livro).
- **Espantalho Possuído:** **E1, o saco com chapéu** (o chapéu de palha, os olhos costurados em X, a boca costurada, a
  gola de palha); **E2, a brasa dentro** (o saco amarrado no alto com a palha saindo, os buracos dos olhos e da boca com a
  brasa de "algo lá dentro").
- **Mímico:** **M1, o baú de frente** (a tampa erguida com os dentes, a língua para fora, as ferragens e o fecho); **M2, o
  baú mordendo** (em três quartos, a tampa aberta como uma mandíbula, os dentes e a língua para fora à esquerda).
- **Servo esquelético:** **SV1, o crânio erguido** (o crânio nu com o violeta do Necromante nas órbitas e as costelas;
  sem elmo, para separar do inimigo); **SV2, o E1 sob o feitiço** (a construção do Esqueleto aprovado, com o violeta nas
  órbitas).
- **Na bancada:** a primeira H1 tinha a cabeça do meio como um goblin sorrindo; a primeira H2 lia como um tiranossauro;
  três D2 não chegaram a uma frente convincente (um gato, um inseto, um boi); o L2 com a luz do livro na largura toda virou
  uma barra verde.

## A minha leitura (quem escolhe é o Jean)

| Criatura | Prefiro | Limitação concreta no tamanho real |
|---|---|---|
| Hidra | **H2** (lê como serpente e mostra as outras cabeças atrás) | a 32 as cabeças de trás são só manchas escuras; na H1, a cabeça do meio ainda lembra um goblin |
| Dragão | **D1** (cabeça de dragão reconhecível e pesada) | a 32 o olho pálido quase some; a D2 continua fraca (lê como um boi de frente) |
| Senhor da Guerra | **S2** (o caolho tem a personalidade mais forte) | a venda e a cicatriz ficam no mesmo lado e a 32 viram uma mancha; o S1 fica perto do Mercenário |
| Profeta | **P1** (a venda e as cinzas contam o cego que chora cinzas) | o capuz lembra o do Cultista na forma; as lágrimas de cinza têm 1 px |
| Bruxa Afogada | **B2** (a cabeça na água é só dela) | a 32 a água ocupa meio quadro e o rosto fica pequeno; a B1 fica perto da Ilse |
| Lich | **L1** (a coroa e a gola leem como um rei morto) | o rosto da caveira é retangular e a 32 parece sorrir |
| Espantalho | **E1** (o chapéu e os X leem como espantalho na hora) | os X dos olhos viram um xadrez a 32 |
| Mímico | **M1** (o baú com boca é inconfundível) | a língua rosa é a cor mais forte do quadro e domina a carta |
| Servo | **SV2** (coerente com o Esqueleto e com o violeta do Necromante) | a 32 o violeta dos olhos são 2 px, e ele ainda pode ser lido como o esqueleto inimigo |

## Processo

- As grades à mão em `auxiliares/grades.py`, rascunhadas e julgadas a 32 na caixa ao lado dos aprovados; sem guia.
- As fontes pelo Aseprite em lote (`python auxiliares/exportar.py --montar`; o conector continua sem editor, a janela
  aberta do Aseprite não foi tocada): 0 diferentes e 0 fora da tela na releitura de cada camada; a exportação do Aseprite
  (o composto) igual à grade, o @2x exato, o 32 em blocos inteiros (só o 32: o uso real).
- As fotos a 1920×945 (`auxiliares/fotografar.mjs`, os modos atual, a e b, trocados só na página pelo nome, nas cartas
  inimigas e aliadas): cada guardião pelo `CHEFE=` com um comum da região; o Espantalho e o Mímico pelos eventos reais
  (`auxiliares/cenario_excecoes.py`); o servo pelo `SERVOS=1`. Sem erro no console.
- As folhas (`python auxiliares/prancha.py`): `par1-hidra-dragao.png`, `par2-senhor-profeta.png`, `par3-bruxa-lich.png`,
  `especiais.png` (a luta em tamanho real e a carta a 2×, a fileira com os aprovados, a 12×) e `candidatos.png` (a
  prancha geral dos 18 e do Golem R1b, identificados).
