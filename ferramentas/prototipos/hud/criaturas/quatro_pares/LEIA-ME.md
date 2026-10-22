# Os quatro pares da madrugada (22/10/2026, 1E.3; propostas, nada no jogo)

**Pedido de Jean:** escolher, sem depender de resposta, oito entidades ainda sem retrato próprio aprovado, em quatro
pares, e fazer duas direções visuais distintas para cada uma, na linguagem dos retratos aprovados; nada integrado.

## A escolha

Critério: as famílias frequentes que ainda usam um desenho genérico inadequado (o `fera`, o rosto de lobo; o `humano`,
o bandido de lenço; a `caveira`; o `etereo`), a variedade entre os pares e as relações com chefes e invocações. O plano
23 não registra ordem para depois do Esqueleto. O Esqueleto (E1r em avaliação), os chefes e os aliados ficam fora.

| Par | Criaturas (família) | Hoje | Onde aparecem | Por quê |
|---|---|---|---|---|
| 1 | Sapo-touro gigante (`sapo`), Sanguessuga gigante (`sanguessuga`) | `fera` (o rosto de lobo) | o pântano (o Charco do Vale), os eventos de bioma; a sanguessuga no Salão Alagado da campanha, com o afogado | as duas mais frequentes do brejo do Vale, e o rosto de lobo não tem nada delas |
| 2 | Cultista (`cultista`), Bruxa do pântano (`bruxa_brejo`) | `humano` (o bandido) | o cultista nas planícies, ruínas e cidadela, os fiéis que o Profeta das Cinzas invoca, os dois de capa escura da sacristia; a bruxa no pântano (e a anciã de um evento) | os dois conjuradores humanos; separar do Bandido sem virar o mesmo rosto com acessórios |
| 3 | Carniçal (`carnical`), Espectro (`espectro`) | `caveira`; `etereo` | o pântano e as ruínas; o espectro também nas planícies e na cidadela e num evento de classe | os mortos-vivos frequentes do Vale depois do Afogado e do Esqueleto: um de carne, um de névoa |
| 4 | Javali selvagem (`javali`), Rato gigante (`rato`) | `fera` | o javali na floresta e nas planícies (e num evento de classe); o rato nas ruínas (o bando de três de um evento) | as feras mais comuns que ainda são o lobo |

**O alcance numa futura integração (pela família, `RETRATO_FAMILIA`):** cada desenho vale para a família, com os
afixos, os líderes de nome próprio e os invocados dela (os fiéis do Profeta pelo cultista; os dois de capa escura da
sacristia, que são cultistas). **Ficam de fora:** os chefes (o Profeta das Cinzas, a Hidra do Brejo, a Bruxa Afogada e
os outros guardiões), o antagonista, os servos aliados e os aliados; nenhum herda a arte de uma família.

## Processo (o mesmo para os quatro pares)

- As grades à mão em `auxiliares/grades.py` (a silhueta, os volumes, depois o detalhe), julgadas cedo na caixa da carta
  ao lado dos retratos aprovados; as fontes no Aseprite pelo conector (`pintar.lua`; releitura das camadas contra a
  grade, 0 diferentes; o composto do editor igual à soma das camadas) em `fontes/<id>/<id>-16.aseprite`; a exportação
  conferida (`auxiliares/exportar.py`: o PNG exportado pela linha de comando igual à grade, o @2x exato, o 32 e o 48 em
  blocos inteiros com os @2x).
- As fotos a 1920×945 (`auxiliares/fotografar.mjs`, `PAR=<n>`): uma luta com as duas criaturas e o Bestiário com elas,
  os mesmos dados em cada modo; as propostas trocadas só na página (protótipo), nas cartas inimigas e nos cartões pelo
  nome. Sem erro nem aviso no console.
- A folha de cada par (`python auxiliares/prancha.py <n>`): a carta (atual × A × B, tamanho real e 2×), o Bestiário,
  a fileira com retratos aprovados e a 12×.

## Par 1, o pântano: o sapo-touro gigante e a sanguessuga gigante (`par1.png`)

- **Os dados:** o sapo (fera; veneno, agarrar; "a língua é mais rápida que uma flecha, e o couro é venenoso ao toque");
  a sanguessuga (fera; drenar; "lentas e nojentas; sozinhas são inofensivas; em bando, secam um homem").
- **Sapo A, de frente** (`sapo-a`; corpo, barriga, olhos, manchas): a cabeçorra larga enchendo a carta, os olhos
  saltados sob a sobrancelha pesada, com a pupila horizontal, a boca de ponta a ponta caindo nos cantos, as manchas
  laranja do veneno, a papada clara. **Sapo B, de perfil** (`sapo-b`): o papo inchado, o olho alto, a boca comprida, a
  pata da frente.
- **Sanguessuga A, empinada** (`sanguessuga-a`; água, corpo, boca): a ventosa redonda com o anel de dentes, de frente,
  sobre o corpo gordo em anéis com a faixa avermelhada, saindo da água. **Sanguessuga B, em curva** (`sanguessuga-b`):
  o corpo saindo da água e subindo, a cabeça com a boca de dentes para a esquerda.
- **Na bancada:** o primeiro sapo de frente era simpático demais (um sapo de desenho, o verde do Troll): passou ao
  oliva do lodo, com a sobrancelha pesada e a boca caindo; o olho do perfil lia como uma coroa. A primeira sanguessuga
  de frente era uma boia; depois, um disco num caule, como uma flor; a de curva sumia de tão fina.
- **A minha preferência:**
  - **sapo: o A.** Forte: lê como sapo à primeira vista e tem a cara emburrada de ameaça. Limite: a papada clara é
    larga e puxa o olho para baixo do rosto.
  - **sanguessuga: a A.** Forte: a ventosa de dentes, a ameaça e a identidade (uma sanguessuga, não um verme comum).
    Limite: o corpo em anéis, reto, lembra um pouco um barril. A B lê como verme, mas o zigue-zague da faixa puxa para
    uma cobra.

## Par 2, os conjuradores humanos: o cultista e a bruxa do pântano (`par2.png`)

- **Os dados:** o cultista (humano, conjurador; bola de sombra, cura, grito de terror; "servos da Fenda; curam uns aos
  outros"); a bruxa do pântano (humana, conjuradora; maldição, bola de fogo, cura; "vendem curas, maldições e às vezes
  as duas coisas no mesmo frasco"). **O alcance:** o cultista vale para a família, os fiéis do Profeta das Cinzas e os
  dois de capa escura da sacristia (são cultistas); o Profeta, o antagonista e os outros humanos ficam fora. A bruxa vale
  para a família (a anciã do evento inclusive); a Bruxa Afogada (guardiã) e a Ilse ficam fora.
- **Cultista A, encapuzado** (`cultista-a`; manto, rosto, marca): o capuz vermelho-escuro de frente, o rosto na
  sombra, a marca violeta da Fenda na testa e a faixa no peito. **Cultista B, sem capuz** (`cultista-b`): a cabeça
  raspada com a cicatriz ritual em fenda, o olhar fixo, a boca fina, o manto com a faixa violeta.
- **Bruxa A, a velha do chapéu** (`bruxa-a`; xale, cabelo, rosto, chapéu): a aba mole com o musgo, o cabelo grisalho
  dos lados, um olho branco, a boca pequena, o xale. **Bruxa B, encapuzada com o frasco** (`bruxa-b`; capuz, rosto,
  frasco): o capuz do brejo, o sorriso torto e o frasco verde de rolha erguido na mão.
- **Na bancada:** o cultista sem capuz e as bruxas tinham a boca de três pixels escuros, que lia como boca aberta
  (susto ou riso): viraram uma linha fina, uma boca pequena e um sorriso torto; a primeira bruxa de chapéu tinha o
  cabelo branco confundido com o rosto, e a primeira com o frasco parecia uma moça de cabelo verde segurando uma folha.
- **A minha preferência:**
  - **cultista: o A.** Forte: a silhueta do capuz vermelho e a marca da Fenda dizem "seita" de longe e separam do
    Bandido cinza. Limite: o rosto é pequeno e quase não tem expressão; a ameaça vem do conjunto.
  - **bruxa: a B.** Forte: o frasco verde conta o "cura e veneno" da descrição, e a figura não repete o capuz do
    Bandido nem o do cultista (a cor e o frasco). Limite: o rosto é pálido e redondo, mais sinistro pelo sorriso que
    pela forma. A A tem a silhueta mais clássica (o chapéu), mas o rosto e o cabelo ainda se misturam a 32 px.

## Par 3, os mortos-vivos: o carniçal e o espectro (`par3.png`)

- **Os dados:** o carniçal (morto-vivo; devorar, mordida sangrenta; "mortos famintos que devoram os caídos no meio da
  luta para fechar as próprias feridas"); o espectro (morto-vivo, etéreo; drenar, grito de terror; "lâminas atravessam
  seu corpo; magia arcana e fé o ferem de verdade"). **O alcance:** cada um pela família (com os afixos, como o espectro
  flamejante de um evento); o Lich Menor (que ganha o etéreo na fase 2), a Bruxa Afogada, o cavaleiro sombrio e os
  servos aliados ficam fora. As cores separam os dois do Afogado (verde-azulado) e da Ilse (o rosto azul).
- **Carniçal A, de frente** (`carnical-a`; corpo, rosto, boca): a pele lívida cinza-violácea, o crânio sem pelo, os
  olhos fundos e amarelo-doentes, a mandíbula comprida com os dentes tortos e o sangue, os ombros magros. **Carniçal B,
  de perfil** (`carnical-b`): a cabeça baixa e comprida mordendo, os dentes e o sangue para a esquerda, o dorso curvado.
- **Espectro A, o capuz de névoa** (`espectro-a`; névoa, vazio): o rosto vazio com um ponto de olho pálido, os farrapos
  se desfazendo embaixo. **Espectro B, o grito** (`espectro-b`): o rosto comprido, os olhos em fenda, a boca esticada
  do grito de terror, os braços em fiapos.
- **Na bancada:** os dentes do primeiro carniçal de frente, alternados, viravam uma grade (passaram a grupos tortos);
  o primeiro espectro do grito era um fantasminha de lençol, de desenho animado, e a névoa estava clara demais.
- **A minha preferência:**
  - **carniçal: o A.** Forte: a fome (a mandíbula com sangue) e o olho doente leem a 32 px; é um morto de carne, não
    uma caveira. Limite: o rosto de frente é largo e lembra um pouco um macaco.
  - **espectro: o A.** Forte: a silhueta do capuz que se desfaz é imediata e diferente de todo o resto da fileira; o
    vazio do rosto é a ameaça. Limite: o ponto de olho único lê como um ciclope. O B tem a ação (o grito), mas ainda é
    leve demais, mais assombração simpática que ameaça.

## Par 4, as feras comuns: o javali selvagem e o rato gigante (`par4.png`)

- **Os dados:** o javali (fera; investida; "teimosos e brutais; a investida de um javali derruba até cavaleiros"); o
  rato (fera; mordida sangrenta, veneno; "onde há um, há vinte; mordidas sujas que infeccionam"; em grupos de dois a
  quatro). **O alcance:** cada um pela família (o javali robusto de um evento inclusive); o lobo, a aranha, os animais
  do herói e os chefes ficam fora.
- **Javali A, de frente em investida** (`javali-a`; corpo, focinho, presas, olhos): a cabeça baixa, a crina eriçada e
  as orelhas pontudas, os olhinhos vermelhos, o focinho em disco com as narinas, as presas subindo dos lados. **Javali
  B, de perfil** (`javali-b`): o focinho e a presa para a esquerda, a crina no dorso, as patas curtas.
- **Rato A, de perto** (`rato-a`; corpo, pele, dentes, olhos): as orelhas rosadas, os olhos vermelhos, o focinho, os
  incisivos amarelos, os bigodes. **Rato B, o corpo inteiro agachado** (`rato-b`): o dorso curvado, o olho vermelho,
  os dentes, a cauda pelada enrolada.
- **Na bancada:** o primeiro javali de frente era um rosto de macaco (as presas pareciam braços): o focinho em disco
  passou para o centro, com as presas ao lado; o primeiro rato de frente era um camundongo (as orelhonas).
- **A minha preferência:**
  - **javali: o A.** Forte: o focinho de porco com as presas e os olhinhos vermelhos dizem javali e ameaça de frente,
    como a investida. Limite: a cabeça é larga e baixa, e a 32 px a crina vira uma borda escura sem forma.
  - **rato: o B.** Forte: a silhueta de rato inteiro (o dorso, a cauda pelada) é a mais reconhecível e diferente dos
    outros retratos, e combina com o bando. Limite: pequeno na caixa e de perfil, perde o olho e os dentes; a ameaça
    vem do número. O A tem os dentes e o olhar, mas de frente lembra um morcego ou um gato.

## A prancha geral e a situação (22/10/2026)

`geral.png` (`python auxiliares/geral.py`): os 16 candidatos na caixa da carta e a 3×, com o nome, o id e a minha
preferência em dourado; embaixo, os retratos integrados do jogo.

| Criatura | Candidatos | Minha preferência | Situação |
|---|---|---|---|
| Sapo-touro gigante | `sapo-a`, `sapo-b` | A | proposta em avaliação |
| Sanguessuga gigante | `sanguessuga-a`, `sanguessuga-b` | A | proposta em avaliação |
| Cultista | `cultista-a`, `cultista-b` | A | proposta em avaliação |
| Bruxa do pântano | `bruxa-a`, `bruxa-b` | B | proposta em avaliação |
| Carniçal | `carnical-a`, `carnical-b` | A | proposta em avaliação |
| Espectro | `espectro-a`, `espectro-b` | A | proposta em avaliação |
| Javali selvagem | `javali-a`, `javali-b` | A | proposta em avaliação |
| Rato gigante | `rato-a`, `rato-b` | B | proposta em avaliação |

Nada integrado; nenhuma regra, atributo, habilidade nem desenho compartilhado foi mudado para as fotos.
