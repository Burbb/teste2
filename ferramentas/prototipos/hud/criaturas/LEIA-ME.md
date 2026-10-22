# O levantamento visual das criaturas (bloco 1E.3, 21/10/2026)

Pedido de Jean: levantar inimigos comuns, elites e chefes (inclusive os da campanha), animais aliados, invocações e
companheiros; o que precisa de arte nova, onde cada um aparece e o que compartilha desenho. **Só levantamento: nada
desenhado nem integrado.** Os 17 ícones de estado (1.161.0) e os retratos aprovados ficam como estão.

Arquivos:
- `levantamento.md`: a tabela por entidade (gerada por `auxiliares/levantamento.py` a partir dos dados do jogo) e as
  contagens;
- `tracos.png`: os 9 desenhos de criatura que existem hoje, em 1×, 2× (carta), 3× (Bestiário e mural) e 10×, com a
  lista de quem usa cada um;
- `compartilhamentos.png`: os casos que mais pesam, recortados das capturas;
- `referencias.png`: o que já foi aprovado e serve de estilo;
- `capturas/`: as fotos a 1920×945 com os arquivos do jogo e saves temporários (`auxiliares/fotografar.mjs`, os
  cenários de `tests/navegador/cenarios.py`; o `covil` ganhou `BESTIARIO`, só para abrir o Bestiário com criaturas) e
  `registro.json`, com o tamanho medido de cada retrato na tela.

## Como o jogo escolhe o desenho de uma criatura (conferido no código)

- **Inimigo:** o motor manda `retrato` pelos **traços**, não pela espécie (`dados.retrato`: o primeiro traço da ordem
  `RETRATOS` que a criatura tem; sem nenhum, a `caveira`). A tela desenha o sprite de 16×16 com esse nome
  (`batalha.js`, `icone(c)`; `sprites-dados.js`).
- **Animal do Patrulheiro:** `fera` (lobo e urso) ou `voador` (falcão), pelo `tipo` (`batalha.js` e `app/paineis.js`).
- **Invocação aliada (`tipo` servo):** `caveira`, venha de onde vier (o esqueleto do Erguer Servo e o inimigo que se
  ergue pelo talento).
- **Herói e companheiros:** `Icones.cabeca`/`retrato` com os desenhos de `retratos.js` (aprovados); só eles saem desse
  caminho.
- **Cenas:** a Ilse (fundo da capela, 1.84.0) e os dois vultos da sacristia (1.83.0) são figuras desenhadas em código
  em `telas/cenas.js`, no método dos cenários; na luta, as cartas deles voltam ao retrato do traço.

## Contagens

- **57 entidades levantadas**: 27 famílias (incluindo o servo esquelético, que não aparece como inimigo), 10
  guardiões, Ilse, os vultos da sacristia, o antagonista do mundo gerado (8 nomes, uma entidade), 3 animais, 2 tipos de
  invocação aliada, 6 invocações de chefe (que usam a arte da família), 3 companheiros e 3 heróis.
- **9 desenhos únicos de criatura** para as 51 entidades que não são herói nem companheiro: `caveira` (14), `fera`
  (12), `humano` (10), `voador` (4), `etereo` (3), `demonio` (3), `planta` (2), `construto` (2), `corrompido` (1).
  Os nomes únicos (Theodore, os nêmesis, as lendas, os chefes de bando) e os afixos não mudam o desenho.
- **Arte de criatura aprovada: nenhuma na carta.** Os 9 sprites vêm do commit que criou a interface em pixel art
  (`9c66a8e3`) e não têm registro de aprovação nem fonte em camadas: são o desenho provisório que ficou. Aprovados e a
  preservar: os retratos dos 3 heróis (1.91.0, o Guerreiro antes) e dos 3 companheiros (1.92.0, `7560ce7c`), e as
  figuras de cena da Ilse e da sacristia.

## Contextos e tamanhos (medidos a 1920×945)

| Contexto | Pedido | Tamanho na tela | Observação |
|---|---|---|---|
| Carta da luta (inimigo, animal, servo) | `S(retrato, 2)` | 32×32 numa caixa de 36 | o contexto mais visto; até 6 inimigos e 5 aliados ao mesmo tempo |
| Carta da luta (herói, companheiro) | `Icones.cabeca(id, 32)` | 32×32 (grade 16×16 a 2×) | a mesma caixa: a referência de leitura |
| Bestiário | `S(retrato, 3)` | 48×48 | o desconhecido sai escurecido (silhueta) |
| Mural de contratos | `S(retrato, 3)` | 48×48 | a entrega usa o saco |
| Rastreador de contratos | `S(retrato, 2)` | 32×32 | |
| Painel da Comitiva (o animal) | `spr(fera/voador, 2)` | 32×32 | ao lado das cabeças aprovadas da comitiva |
| Faixa de mestre caçador | `S(retrato, 3)` | 48×48 | |
| Ficha do inimigo (hover) | os ícones de traço | 16 a 2× | o `fera`, o `humano`, a `caveira`... são também os ícones dos traços |

Todos os retratos de criatura são **cabeças** de 16×16 ampliadas por fator inteiro (2× e 3×). O espaço real é o da
cabeça (como os retratos de carta aprovados do herói e da comitiva), não o do corpo inteiro: a caixa da carta é
quadrada e pequena, e o Bestiário e o mural só ampliam o mesmo desenho.

## Problemas encontrados

1. **Um desenho para muitas espécies.** O rosto de lobo (`fera`) serve a 12 entidades: o Lobo inimigo, a Aranha
   gigante, o Javali, o Sapo, a Sanguessuga, o Rato, a Rainha Aracnídea, a Hidra **e o Urso Pardo e o Lobo Cinzento do
   próprio herói**. Na mesma luta, o urso aliado e o lobo inimigo têm o mesmo rosto (`compartilhamentos.png`).
2. **A caveira de fallback.** O troll só tem o traço `gigante`, que não tem retrato: o Troll da montanha e o **Rei
   Troll** aparecem como caveira. A caveira também é o afogado, o esqueleto, o carniçal, o cavaleiro sombrio, o Lich e
   os servos invocados (14 entidades).
3. **A guardiã da campanha sem rosto na luta.** A Ilse tem arte de cena aprovada no fundo da capela, mas a carta dela
   na luta é a mesma caveira do esqueleto e do afogado. **Resolvido na 1.162.0** para a Ilse e o Afogado (abaixo).
4. **O humano genérico.** O bandido de lenço vermelho é também o cultista, o mercenário, a bruxa do pântano, os chefes
   humanos (o Senhor da Guerra, o Profeta das Cinzas) e o antagonista. Os vultos de capa escura da sacristia viram, na
   carta, o mesmo bandido.
5. **Troca de desenho no meio da luta.** Na fase 2, o Lich ganha o traço `etereo`, e a carta dele passa de caveira a
   fantasma.
6. **Mudança de dado, não só de arte.** Hoje o desenho sai dos traços (`dados.retrato`). Dar rosto a uma espécie vai
   pedir, na integração, um papel novo pela família (como foi o `ESTADO` dos estados), sem mexer nos traços nem nas
   regras; isso fica para quando houver um desenho aprovado.

## Referências aproveitáveis e lacunas

- **Aproveitáveis:** os retratos de carta aprovados do herói e da comitiva (cabeça e ombros em 16×16 a 2×, poucos
  planos, a luz da esquerda; `retratos.js`), a Ilse e os vultos da sacristia (as cores e a silhueta das figuras do
  mundo), os 17 ícones de estado (contorno de 1 px e o peso no chip) e o Bestiário da doca (o crânio de fera, 1.128.0).
- **Lacunas:** não há referência visual de nenhuma espécie (lobo, bandido, afogado, aranha, esqueleto...). Para o
  primeiro par, uma referência do Jean (como foi para os itens de ferro e a Esquiva) ajudaria a fixar a direção.

## Recomendação para começar

**Lobo e Bandido.** São os inimigos mais frequentes do Vale (o bandido aparece no Charco, no Bosque e no Vau; o lobo no
Bosque e nas planícies; os dois também nos eventos), e cada um é o dono de um dos dois desenhos mais compartilhados
(`fera` e `humano`). Com os dois, o padrão sai em uma fera e em um humano: a cabeça de 16×16 a 2×, na mesma linguagem
dos retratos de carta aprovados. Liberar o `fera` do lobo também prepara a separação do urso e do falcão do herói.

**Composição:** cabeça (e o começo dos ombros), de frente ou em três quartos, numa grade de 16×16 desenhada para a
carta (32 px na tela) e vista também a 3× no Bestiário e no mural, como os retratos de carta do herói e da comitiva. Não
corpo inteiro: o espaço é a caixa quadrada de 36 px.

**Logo depois (sugestão):** Afogado e Ilse (a carta), que separam a caveira dos mortos-vivos da campanha e dão à
guardiã um rosto coerente com a arte de cena dela. O troll e o Rei Troll (a caveira por falta de traço) são uma
correção pequena e visível para um lote seguinte.

A escolha do par e da direção é do Jean; nada foi começado.

## Integrados

- **1.162.0: o Afogado e a Ilse** (o primeiro par, `afogado_ilse/`): o Afogado C (`afogado-cranio`) pela família e a
  Ilse R3 (`ilse-r3`, com o olho 1 px para a esquerda) pela chave da capela, em `dados.retrato` e `Icones.criatura`. O
  esqueleto, o carniçal, o cavaleiro sombrio, o Lich, os servos e o guardião genérico da Bruxa Afogada continuam com a
  caveira; as outras criaturas continuam pelos traços. Os problemas 1, 2, 4 e 5 continuam abertos.
- **1.163.0: o Lobo e o Bandido** (o segundo par, `lobo_bandido/`): o Lobo de frente com o começo do pescoço e o
  Bandido do capuz, da máscara e da faca, pela família. O `fera` continua no animal do herói, no lobo gélido e nas
  outras feras, e o `humano` nos outros humanos: o problema 1 e o 4 ficam menores, não resolvidos.
- **1.164.0: o Urso Pardo e o Falcão Peregrino do patrulheiro** (`animais/`, o `urso-t2` e o `falcao-t2`): pelo tipo
  do animal, na carta aliada e no painel da comitiva. O `fera` e o `voador` dos inimigos continuam.
- **1.165.0: o Lobo Cinzento do patrulheiro** com o mesmo arquivo do Lobo inimigo (`retrato-lobo`), pelo tipo do
  animal: os três animais do patrulheiro concluídos. O mesmo rosto dos dois lados é de propósito.
- **1.166.0: o Troll da montanha** (`aranha_troll/`, o `troll-1`, de carne, pela referência gerada): pela família. O
  Rei Troll (guardião) continua na caveira; a Aranha segue no protótipo.
- **1.167.0: o Rei Troll e a Aranha gigante** (`aranha_troll/`): o Rei (o Troll 2 com a coroa dourada) pelo id do
  guardião; a Aranha (a 2B) pela família, com as que a Rainha invoca. A Rainha Aracnídea continua no `fera`.
- **1.168.0: a Rainha Aracnídea** (`rainha_esqueleto/`, a `rainha-a`, sem retoques): pelo id da guardiã; as aranhas
  que ela invoca continuam com o retrato da Aranha gigante. O Esqueleto segue no protótipo.

## Em proposta


## Em proposta

- **A Aranha Gigante e o Troll** (`aranha_troll/`, 21/10/2026): duas propostas de cada (a aranha de frente e de lado
  em ameaça; o troll de frente e de perfil com a corcunda), com o alcance previsto pelos dados (só as famílias `aranha`
  e `troll`; a Rainha Aracnídea e o Rei Troll ficam fora). Segunda rodada: três de cada pelas referências geradas
  (a aranha de frente; o troll de carne). Nada integrado.

- **A Rainha Aracnídea e o Esqueleto** (`rainha_esqueleto/`, 21/10/2026): duas propostas de cada (a Rainha de frente e
  descendo pelo fio; o Esqueleto de frente e em três quartos), com o alcance previsto e os papéis do esqueleto
  separados (o inimigo, os invocados pelo Lich, o servo aliado, os chefes). A Rainha A entrou na 1.168.0; o Esqueleto
  continua em proposta: o A2 (o A desenvolvido pela referência gerada, `esqueleto-a2.png`) e o A2n (o mesmo com o nariz refeito,
  `esqueleto-a2n.png`, a base aprovada); sobre ele, o sorriso contido (S1) e o marcado (S2),
  `esqueleto-sorriso.png`, não aprovados; o C, a nova direção pela segunda referência gerada, não aprovado (o sorriso de comercial);
  o C2, com a boca de caveira (`esqueleto-c.png`), aguarda o Jean.

## Reservado

- **O Bandido do chapéu** (`lobo_bandido/`, a segunda rodada): conceito guardado para um possível chefe futuro, fora
  do jogo; os caminhos no `LEIA-ME.md` da pasta.
