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
