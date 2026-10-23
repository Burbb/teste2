# A Hidra do Brejo: o estudo nativo de 32 e a proposta de 16 (23/10/2026, protótipo; nada no jogo)

**Pedido do Jean:** as propostas anteriores (a H1, a H2 e a `hidra-t`) foram recusadas: pareciam fantoches, cabecinhas na
ponta de pescoços finos. Uma construção nova pelo caminho do Dragão: primeiro em 32 nativos, depois a adaptação à mão para
16. Direção obrigatória: **as três cabeças de réptil olhando para o mesmo lado, a esquerda**; cabeças fortes, com focinho,
mandíbula e testa convincentes; pescoços grossos ligados à criatura; expressão de predador adulto. A construção recusada
não foi usada; os arquivos dela ficam em `chefes_e_especiais/`.

## O que vem do jogo

A guardiã do pântano (`hidra_do_brejo`): 140 de vida, `fera`; Regenerar, Veneno, Mordida Sangrenta, Varredura. "A água
ferve. Uma, duas, três cabeças de serpente emergem, sibilando em uníssono." Só aparece na carta da luta (32); hoje sai do
sprite `fera`. **Para uma integração futura:** um papel pelo id da guardiã (`RETRATO_GUARDIAO`), como o Dragão de Gelo.

## Como foi feito

- **A referência:** `ferramentas/arte/referencias/icones/Hidra do pântano de três cabeças-1.png` dá o material (as escamas
  verdes, o olho âmbar), a anatomia (o focinho longo, a testa pesada, a mandíbula, a boca aberta com a presa) e a expressão.
  **A orientação dela não vale:** lá as cabeças olham para lados diferentes; o Jean corrigiu, todas para a esquerda. A guia
  (`guias/hidra-guia-32.png` e `-16.png`, o recorte de 1220 px a partir de (20, 40), reduzido por média) fica oculta nas
  fontes e só serviu para o material e as proporções.
- **O estudo nativo de 32** (`hidra-n32`), pintado em três partes, da cabeça de trás para a da frente (`pintar` em
  `grade.py`): a cabeça de cima (B), atrás, menor; a da direita (C), atrás, no meio, em parte escondida pela principal; e a
  principal (A), na frente, embaixo e à esquerda, a maior. Os pescoços grossos descem para a direita e se juntam embaixo.
  1. a primeira passada acertou a composição, mas a cabeça principal ficou redonda, de desenho animado, e a boca aberta
     lia como um sorriso;
  2. refeitas como crânios de réptil: o focinho longo e chato, a crista da testa acesa, o lábio superior com as presas, a
     boca em cunha (alta na frente, fechando para trás), a mandíbula forte, a sombra do pescoço embaixo;
  3. o olho da principal ("âmbar, pupila, âmbar") lia como óculos; virou um olho só, âmbar com a pupila, sob uma sombra
     da testa (a mesma sombra nas outras duas: o olhar de predador).
- **A proposta de 16** (`hidra-n16`), redesenhada à mão com o 32 reduzido a 2:1 como mapa. Na primeira passada, a cabeça
  de cima virou uma mancha (o focinho sumiu) e a da direita, um volume com olho; as duas foram redesenhadas como cunhas de
  focinho, com a linha de cima acesa, o olho sob a sombra e a linha da boca.
- **As fontes, pelo Aseprite em lote** (`python auxiliares/grade.py ..` e `python auxiliares/exportar.py --montar`; o
  conector sem editor, a janela aberta do Jean não foi tocada): 0 diferentes na releitura; reabertas com as camadas guia
  (oculta), escamas, boca, olhos e contorno; a exportação igual ao composto, alfa só 0 ou 255, os derivados em blocos
  inteiros que voltam ao original.
- **As fotos** (`auxiliares/fotografar.mjs`, `capturas/`), pela guardiã na luta (`CHEFE=hidra_do_brejo`, com um sapo), a
  1920×945, com os mesmos dados nos quatro modos (o jogo, a T, o N32 e o N16), sem erro no console. **A folha:**
  `comparacao.png`.

## A minha leitura (quem decide é o Jean)

- **Conferência técnica** (as fontes, a exportação, a transparência e as ampliações) passou; isso não é aprovação visual.
- **O N32** lê na carta como três cabeças de réptil olhando para a esquerda, a principal dominante com a boca entreaberta
  e as presas, as duas de trás em alturas diferentes, e os pescoços grossos ligados num corpo só: nada de fantoche. As
  cabeças ainda são um pouco quadradas, e a de trás à direita aparece pouco (o olho e a boca).
- **O N16 preservou** as três cabeças distintas, todas para a esquerda, cada uma com o olho, a principal com a boca aberta
  e a presa, e os pescoços grossos. **Perdeu** o focinho longo das duas de trás (viram cunhas curtas), a crista da testa e
  a forma da mandíbula da principal; o conjunto fica mais apertado e a 1× é uma massa verde com três olhos. Não é fiel ao
  N32 só por ter três cabeças: as de trás leem como cabeças de réptil só a 2× e a 3×.
- **Na fileira:** o N16 tem o grão dos vizinhos; o N32 destoa, como os outros estudos de 32.

# A segunda construção de 32: N32B (23/10/2026, protótipo; nada no jogo)

**Pedido do Jean:** nenhum dos dois aprovado. As três cabeças estão na direção certa, mas continuam parecendo barras
horizontais sobre pescoços, e o problema já está no 32 (não é só perda na redução). Refazer a construção das cabeças, só
em 32, numa cópia (o N32 e o N16 ficam); **sem nova adaptação para 16**, para avaliar a anatomia antes.

- **O diagnóstico:** no N32, cada cabeça era um empilhamento de faixas de cor (o topo aceso, o meio, a linha do lábio, a
  faixa vermelha da boca), com a mesma altura da nuca à ponta do focinho: uma barra.
- **O N32B** (`hidra-n32b`, `GRADE_32B` em `grade.py`), à mão, em passadas:
  1. cada cabeça como uma cunha: o crânio alto atrás e a ponta do focinho baixa, a cabeça principal maior e um pouco
     inclinada para baixo. **O que não funcionou:** a testa em rampa lisa fez da principal uma cúpula (cara de tartaruga);
  2. a anatomia de réptil: o alto do crânio mais baixo e chato, o calombo da testa pesando sobre um olho maior e mais à
     frente, o degrau entre a testa e o focinho, a narina na ponta;
  3. o volume sem escamas: a mandíbula baixa (a abertura da boca é uma cunha alta na frente, com o canto descendo, sem
     sorriso), o fundo da boca escuro, a sombra sob o lábio, uma linha de contorno marcando o músculo da mandíbula, e o
     pescoço da principal como uma peça própria, saindo de trás da mandíbula;
  4. as duas de trás refeitas com a mesma anatomia (o calombo sobre o olho, o focinho afinando, a linha da boca), menores e
     um tom mais escuras, separadas da principal por sobreposição, contorno e sombra. A de cima encosta no alto do crânio
     da principal; a da direita espia por trás da nuca dela. Os pescoços continuam cortados na borda de baixo.
- **A fonte, pelo Aseprite em lote** (`python auxiliares/exportar.py --montar hidra-n32b`; o conector sem editor, a janela
  aberta do Jean não foi tocada): 0 diferentes na releitura; reaberta com a guia oculta e as camadas na ordem; a
  exportação igual ao composto, alfa 0/255, o @2x em blocos inteiros. O N32 e o N16 reexportados saíram iguais.
- **A foto** (`MODOS=n32b`), pela guardiã na luta, a 1920×945, com os mesmos dados, sem erro no console. **A folha:**
  `construcao-32.png` (`python auxiliares/prancha.py --b`: a referência, o N32 × o N32B na mesma carta, a carta a 2×, a
  fileira e o diagnóstico).

## A minha leitura do N32B (quem decide é o Jean)

- **Melhorou:** a principal domina e tem crânio, testa pesada sobre o olho, focinho projetado e mandíbula; a boca aberta lê
  como mordida, não como sorriso; as de trás leem como cabeças (testa, olho, focinho), não como faixas; os pescoços são
  grossos e da mesma criatura.
- **Ainda falta:** as de trás são pequenas e a da direita aparece pouco (o olho, a testa e a linha da boca); os planos
  ainda são poucos (um verde médio grande na bochecha da principal); a 1× é uma massa de três cabeças com a boca vermelha.
  A adaptação para 16 espera a avaliação desta anatomia.

# A correção da cabeça principal: N32C (23/10/2026, protótipo; nada no jogo)

**Pedido do Jean:** no N32B, a cabeça maior ainda tinha a testa descendo numa rampa contínua até o nariz, uma bochecha
grande, um perfil de cachorro ou dinossauro de desenho e uma boca comprida que sugeria sorriso. Corrigir só essa cabeça,
numa cópia (o N32, o N16 e o N32B ficam), pela referência: separar crânio, sobrancelha, focinho e mandíbula, sem tratar a
"cunha" como forma obrigatória. As duas de trás, a composição e a paleta como estavam; só em 32, sem textura.

- **O que mudou** (`hidra-n32c`, a parte `A3` e a `GRADE_32C` em `grade.py`; as partes `B2`, `C2` e `PESCOCO2` do N32B,
  sem mudança):
  - **o focinho** é um bloco horizontal de topo chato, com a narina na ponta, e **um degrau nítido** sobe dele até o alto
    do crânio (antes, uma rampa);
  - **a sobrancelha** é uma linha escura e pesada sobre o olho, que fica no encontro do focinho com o crânio, na sombra;
  - **a bochecha** ficou pequena, atrás do canto da boca;
  - **a mandíbula** é um bloco à parte, inclinado para baixo a partir do canto, embaixo do olho, com a presa de baixo; a
    boca abre em ângulo, não numa faixa comprida.
- **Na bancada:** o fundo da boca em vermelho virou um triângulo vermelho que dominava a carta; ficou escuro (o vermelho
  escuro e o preto atrás), com o vermelho só na língua.
- **A fonte, pelo Aseprite em lote** (`python auxiliares/exportar.py --montar hidra-n32c`; o conector sem editor, a janela
  aberta do Jean não foi tocada): 0 diferentes na releitura; reaberta com a guia oculta e as camadas na ordem; a
  exportação igual ao composto, alfa 0/255, o @2x em blocos inteiros. O N32B reexportado saiu igual.
- **A foto** (`MODOS=n32c`), pela guardiã na luta, a 1920×945, com os mesmos dados e a mesma caixa da carta, sem erro no
  console. **A folha:** `cabeca-principal.png` (`python auxiliares/prancha.py --c`: a cabeça da referência, o N32B × o
  N32C na mesma carta, a carta a 2×, a fileira e o diagnóstico a 8×).

## A minha leitura do N32C (quem decide é o Jean)

- **Melhorou:** o perfil da principal lê como réptil (o focinho reto e projetado, o degrau da testa, o olho sob a
  sobrancelha, a mandíbula separada e a boca aberta de predador), e não mais como cachorro de desenho; a bochecha não
  domina mais.
- **Ainda falta:** o alto do crânio é uma placa comprida e chata até a nuca (a referência tem o crânio mais arredondado
  atrás do olho); a mandíbula é fina perto do queixo; a 1× a boca aberta é o que mais aparece. As cabeças de trás seguem
  como no N32B.
