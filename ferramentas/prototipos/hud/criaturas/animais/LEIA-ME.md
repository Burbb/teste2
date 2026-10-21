# Os animais do patrulheiro: o Urso, o Falcão e o Lobo Cinzento (proposta, 21/10/2026)

**Pedido de Jean:** duas propostas do Urso e duas do Falcão, e um teste de reaproveitamento: o retrato do Lobo
integrado na 1.163.0, exatamente como está, no lugar do desenho do Lobo Cinzento aliado. Só no protótipo: nada
integrado; os sprites `fera` e `voador`, os mapeamentos, as regras, as habilidades e os atributos iguais. O Lobo e o
Bandido (1.163.0, `29307375`) e os outros retratos aprovados ficam como estão.

## Os dados e os usos

- **Os três animais** (`classes.COMPANHEIROS`, chamados no nível 4 do patrulheiro, `Progressao.escolher_companheiro`):
  o Lobo Cinzento (`lobo`: "equilibrado; morde e faz o inimigo sangrar"), o Falcão Peregrino (`falcao`: "frágil, mas
  veloz e certeiro; ótimo contra voadores") e o Urso Pardo (`urso`: "lento e resistente; atrai golpes e às vezes
  atordoa"). O jogador pode dar outro nome; a espécie fica no `tipo`.
- **Onde aparece o retrato** (conferido no código): a **carta aliada na luta** (`batalha.js`, `icone(c)`: o `voador`
  para o falcão, o `fera` para o lobo e o urso; 32 px, o 16 a 2×) e o **ícone do animal no painel da comitiva**
  (`app/paineis.js`, `.membro.fera`: o mesmo sprite a 2×, 32 px). A figura de 16 px no acampamento (`telas/acampamento.js`)
  é um desenho de cena, não um retrato, e fica fora; a escolha do animal no nível 4 é só texto.
- **Hoje:** o Lobo Cinzento e o Urso usam o mesmo `fera` (o rosto de lobo de olhos vermelhos, também da aranha, do
  javali, do rato e das outras feras inimigas); o Falcão usa o `voador`, que é um morcego de olhos vermelhos (também da
  harpia e dos outros voadores).

## As propostas

Cabeças de 16×16 no formato dos retratos de carta aprovados (sem contorno, cores agrupadas, a luz da esquerda), vistas a
2×; nenhuma grade maior.

- **Urso A, de frente** (`urso-a`; pelagem, focinho, detalhes): a cabeça larga que enche o quadro, as orelhas pequenas e
  redondas nos cantos com o fundo escuro, a sombra da testa sobre os olhos pequenos, o focinho claro com o nariz, as
  bochechas de pelo, e embaixo o pescoço que desce para trás, sem ombros nem peito (a lição do lobo).
- **Urso B, de perfil** (`urso-b`; as mesmas camadas): virado para a esquerda, o focinho comprido na cor do pelo com a
  ponta clara e o nariz, a linha da boca, a orelha redonda, a nuca e o pescoço grosso indo para a direita. Na bancada, a
  mandíbula clara parecia uma boca aberta (como o bico do Lobo B): ficou na cor do pelo.
- **Falcão A, a cabeça de perfil** (`falcao-a`; plumagem, peito, bico, olho): em close, virado para a esquerda: o
  capacete cinza-escuro, a faixa escura descendo do olho (o "bigode" do peregrino), o anel amarelo do olho, a cera
  amarela e o bico curvo cinza com a ponta escura, a garganta creme e o começo do peito com poucas pintas; a nuca e o
  pescoço em cinza-azulado.
- **Falcão B, três quartos com a asa** (`falcao-b`; as mesmas camadas): a cabeça menor no alto à esquerda, com o mesmo
  capacete, o anel do olho e o bico curvo, e embaixo o peito pintado e a asa dobrada em cinza-azulado à direita. Na
  bancada, uma versão de frente com os dois olhos lia como coruja, e o peito em xadrez como pinguim.
- **Lobo Cinzento, o reaproveitamento:** o `retrato-lobo-16.png` do jogo (1.163.0) sem nenhuma mudança, posto pela página
  no lugar do `fera` na carta aliada e no painel.

## Processo e conferência

- As grades em `auxiliares/grades.py`; as fontes **no editor pelo MCP** (`pintar.lua`, 0 diferentes na releitura) em
  `fontes/<id>/<id>-16.aseprite`; a exportação com a conferência (`auxiliares/exportar.py`: o 1× igual à grade, @2x
  exato, alfa 0/255) em `proposta/`. Os auxiliares são os do par anterior (`../lobo_bandido/auxiliares/`), adaptados.
- Fotos a 1920×945 (`auxiliares/fotografar.mjs`), com os mesmos dados para cada animal: o patrulheiro nível 4 com o
  animal numa luta contra um lobo, um bandido e uma aranha (o cenário `tutorial` com `NIVEL`, `ANIMAL` e `GRUPO`), o
  palco e a página inteira (o painel da comitiva). A troca é só na página, na carta aliada do animal e no ícone do painel;
  o lobo inimigo integrado fica do outro lado, como no jogo. Sem erro nem aviso no console (`capturas/registro.json`).
- As folhas: `urso.png`, `falcao.png` e `lobo-cinzento.png` (a carta e o painel em tamanho real e a 2×, a caixa a 3×,
  a 12×, a luta inteira) e `animais.png` (a fileira dos três, atual e propostas, junto do Morel, da Odette, do herói e do
  Lobo e do Bandido inimigos), por `python auxiliares/prancha.py`.

## Avaliação (a minha leitura em tamanho real; quem aprova é o Jean)

- **Urso A (minha preferência):** lê como urso na hora (as orelhas redondas, o focinho claro, o volume) e se separa bem
  do lobo. Limite: de frente e com a cabeça enchendo o quadro, fica simpático, perto de um ursinho; o pescoço quase não
  aparece, porque a cabeça é larga.
- **Urso B:** tem mais o peso do animal (a nuca e o pescoço grosso) e é diferente de todos os outros retratos. Limite:
  a 2× o focinho de perfil é pequeno, e a cabeça erguida lembra o Lobo B que não foi escolhido.
- **Falcão A (minha preferência):** a cabeça grande deixa o bico curvo, o capacete e o anel amarelo legíveis no tamanho
  da carta; diz "falcão", não "pássaro". Limite: mostra pouco do corpo, e o peito pintado é só uma faixa embaixo.
- **Falcão B:** mostra a ave (a asa dobrada, o peito), mais elegante. Limite: a cabeça menor perde o bico e o anel a
  2×; a leitura de falcão depende do capacete escuro.
- **Lobo Cinzento reaproveitado:** o retrato serve ao animal sem mudança e é muito melhor que o `fera` de olhos
  vermelhos para um companheiro. Limite: numa luta contra lobos, o aliado e os inimigos ficam com o mesmo rosto; a
  distinção vem só da posição da carta, da borda e do nome. Para mim, funciona; se incomodar, o caminho é um detalhe
  de cor (uma coleira), não outro desenho.

## A transposição das referências geradas (21/10/2026)

**Pedido de Jean:** um candidato de Urso e um de Falcão transpostos das duas imagens geradas na conversa, que ele deixou
em `ferramentas/arte/referencias/icones/` (registradas no `LEIA-ME.md` de lá), pelo mesmo processo da Ilse: a construção,
as proporções e a expressão da referência na grade de 16, agrupando as cores e tirando o detalhe que não cabe. As
propostas A e B ficam; o Lobo Cinzento não muda. Nada integrado.

- **Urso t** (`urso-t`; pelagem, focinho, detalhes e a guia oculta): de frente, a expressão severa da referência: as
  orelhas redondas com o fundo escuro, a testa clara, as órbitas fundas em sombra com o ponto âmbar do olho, a sombra
  das sobrancelhas descendo para dentro, o focinho claro e forte, o nariz escuro, uma faixa clara, a boca fechada numa
  linha e o queixo; a cabeça larga como na referência, e embaixo o pescoço que recua para o corpo fora do quadro (os
  ombros de pelo da referência saíram). Na bancada: as orelhas quadradas ficaram redondas, e o nariz colado na boca, que
  parecia boca aberta, ganhou a faixa clara entre os dois.
- **Falcão t** (`falcao-t`; plumagem, máscara, peito, bico, olho e a guia oculta): de perfil para a esquerda, o bico curto
  cinza-azulado com o gancho escuro, a cera amarela, o anel amarelo à esquerda e embaixo do olho, a máscara escura que
  envolve o olho e segue para a nuca (sem descer pela bochecha), o alto da cabeça claro, o queixo e a garganta creme, o
  peito com poucas pintas, a nuca e a asa em cinza-azulado com a mancha clara. Na bancada, o amarelo dos dois lados do
  olho lia como óculos: o anel ficou só à esquerda e embaixo.
- **Processo:** a referência reduzida a 16×16 por média (`guias/<id>-guia-16.png`) para medir onde cai cada parte, e a
  grade redesenhada à mão (`auxiliares/grades.py`: `URSO_T`, `FALCAO_T`, com letras próprias para não mudar as cores das
  propostas anteriores). As fontes pelo MCP (`pintar.lua`, 0 diferentes na releitura; a guia por `Image{fromFile=...}`,
  oculta); o composto do editor com os mesmos pixels opacos das camadas visíveis (196 e 177); a exportação conferida
  (igual à grade, @2x exato; o 2× e o 3× por vizinho mais próximo voltam ao 16). Fotos a 1920×945 com os mesmos dados
  (`ANIMAIS=urso,falcao SO=t node auxiliares/fotografar.mjs ...`, o modo `t`), sem erro nem aviso no console.
- **A folha:** `transposicao.png` (`python auxiliares/prancha.py t`): a referência, a guia, A anterior × t (1×, a carta,
  a 12×), a carta aliada e o painel da comitiva (tamanho real, 2× e a caixa a 3×) e a fileira com os retratos aprovados.

**Avaliação (a minha leitura a 32 px; quem aprova é o Jean):**

- **Urso t:** a expressão severa passa para a carta (as órbitas fundas e a testa franzida), e o urso fica mais selvagem
  que o A, que era um ursinho. A boca fechada e o focinho forte leem; as orelhas são pequenas a 2×. Sem pixel solto.
  Limite: a cabeça enche o quadro de lado a lado, como na referência, e o pescoço quase não aparece; o nariz grande puxa
  a atenção.
- **Falcão t:** a cabeça e o bico de gancho leem melhor que no A, e a máscara indo para a nuca dá o olhar atento; o
  queixo e a garganta ficam limpos. Limite: a 2× o anel amarelo e a cera ficam a um pixel um do outro (o olho depende
  do ponto preto entre eles), e as pintas do peito são poucas.

## O último ajuste localizado (21/10/2026)

**Pedido de Jean:** sobre os candidatos do `cf859322`, que ficam como o antes (`urso-t`, `falcao-t`): no falcão, um pixel
amarelo fechando o canto de trás do olho, sem engrossar o anel; no urso, só a boca e o acabamento do focinho (a linha
clara embaixo da boca, junto do focinho arredondado, sugeria um sorriso), com a boca fechada mais neutra e firme. Nada
integrado.

- **Falcão t2** (`falcao-t2`): (7,5) passa da máscara para o amarelo do anel (`#d89a1c`, na camada `olho`); o olho fica
  fechado pelo amarelo à frente, embaixo e atrás, e a máscara continua para a direita a partir de (8,5). O bico, a
  garganta e o resto iguais.
- **Urso t2** (`urso-t2`): o queixo embaixo da boca, (6..8,13), passa do claro do focinho para o tom médio; os cantos da
  boca, (4,12) e (11,12), ficam no tom médio (saem do pelo) e (10,12) no claro, de modo que a linha da boca fica reta e o
  focinho guarda o volume dos lados. A cabeça, os olhos, as orelhas e a paleta iguais.
- **Processo:** as fontes do `t` abertas pelo MCP e gravadas como `fontes/urso-t2/` e `fontes/falcao-t2/` (a guia continua oculta); só os
  pixels mudados pintados pelo `pintar.lua` (0 diferentes na releitura), apagando da camada antiga quando a camada muda;
  o composto do editor com os mesmos pixels opacos (196 e 177). A exportação conferida (igual à grade `URSO_T2` e
  `FALCAO_T2`, @2x exato, 2× e 3× exatos); o `t2` difere do `t` só nos pixels acima.
- **A folha:** `ajuste.png` (`python auxiliares/prancha.py ajuste`): antes × depois na caixa da carta em tamanho real e
  a 3×, junto do Morel, da Odette, do herói, do Lobo e do Bandido, e a 12× com os pixels mudados marcados.

**Avaliação (a 32 px; quem aprova é o Jean):** no urso, a boca lê fechada e reta, e o queixo não sorri mais; a mudança é
pequena a 2×, mas a expressão fica mais séria, e o focinho continua com volume. No falcão, o olho volta a ser um olho
delimitado, como no A, e se separa da máscara; o risco é o amarelo dos dois lados lembrar um pouco os óculos da primeira
passada, o que a 32 px não acontece porque o anel de baixo e o preto do olho ficam entre eles.
