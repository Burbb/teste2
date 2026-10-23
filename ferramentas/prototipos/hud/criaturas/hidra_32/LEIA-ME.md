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

# A reconstrução pela nova referência: N32D (23/10/2026, protótipo; nada no jogo)

**Pedido do Jean:** reconstruir a Hidra com a nova referência como direção principal (deixada por ele em
`ferramentas/arte/referencias/icones/Hidra tríplice do pântano em pixel art.png`; a origem e o SHA-256 no LEIA-ME de lá),
uma proposta nova em 32 nativos, preservando o N32C e as anteriores; sem adaptar para 16 nem integrar. Copiar a composição
(três cabeças para a esquerda, a principal maior e à frente), o crânio arredondado atrás do olho, a sobrancelha pesada, o
focinho projetado, a mandíbula com espessura ligada ao pescoço, e a separação entre as cabeças.

- **A guia** (`guias/hidra-d-guia-32.png` e `-16.png`): a imagem inteira reduzida por média, oculta na fonte; mediu as
  posições (a ponta do focinho de cima em x8, o olho dela por volta de (13, 4); a ponta da da direita em x21, o olho em
  (25, 10); a principal com o crânio entre as linhas 10 e 13, o olho em (10, 16), a ponta do focinho em x0, a boca aberta
  nas linhas 20 a 24 e a mandíbula até a 28). O desenho é à mão, com as cores agrupadas.
- **A paleta** (`PALETA_D`, só deste desenho): a oliva da referência, com o intervalo de valor aberto (o topo aceso, as
  sombras fundas); a primeira versão, com os verdes próximos demais, apagava a modelagem.
- **O N32D** (`hidra-n32d`, `GRADE_32D`), à mão, em partes, de trás para a frente: a cabeça de cima, o pescoço dela, a da
  direita, o pescoço dela, o pescoço da principal e a principal.
  1. a primeira passada acertou a composição, mas os dentes viraram uma grade de blocos brancos na principal e dentões
     quadrados nas de trás, e os ventres dos pescoços de trás viraram listras: **os dentes simplificados** (duas presas em
     cima e uma embaixo na principal, uma presa em cada uma de trás) e os ventres de trás mais discretos;
  2. o contorno da principal arredondado (a ponta do focinho e o crânio atrás do olho) e os planos marcados (o topo do
     focinho aceso, a sobrancelha acesa com a sombra embaixo, o olho na sombra);
  3. **o que não funcionou:** o pescoço da principal só aparecia nas últimas linhas; atrás da mandíbula se viam os
     pescoços de trás, e a cabeça parecia solta. O pescoço dela ficou largo, saindo de trás da mandíbula e da nuca, na
     frente dos outros dois;
  4. o contorno que fechava a nuca de cada cabeça (e as fazia parecer caixas) saiu: a nuca continua no pescoço; a
     separação entre as cabeças fica no contorno da frente, na sobreposição e na sombra.
- **A fonte, pelo Aseprite em lote** (`python auxiliares/exportar.py --montar hidra-n32d`; o conector sem editor, a janela
  aberta do Jean não foi tocada): 0 diferentes na releitura; reaberta com a guia oculta e as camadas na ordem; a
  exportação igual ao composto, alfa 0/255, o @2x em blocos inteiros. A paleta por desenho (`PALETAS`) não mudou as
  anteriores: as grades e as listas regravadas iguais, o N32C reexportado igual.
- **A foto** (`MODOS=n32d`), pela guardiã na luta, a 1920×945, com os mesmos dados e a mesma caixa da carta, sem erro no
  console. **A folha:** `reconstrucao.png` (`python auxiliares/prancha.py --d`: a referência nova, o N32C × o N32D na
  mesma carta, a carta a 2×, a fileira e o diagnóstico a 8×).

## A minha leitura do N32D (quem decide é o Jean)

- **Segue a referência:** a composição (a principal grande embaixo e à frente, uma cabeça no alto e outra à direita, todas
  para a esquerda), a principal com o crânio arredondado, a sobrancelha, o focinho com a narina, a boca aberta com as
  presas e a mandíbula grossa ligada ao pescoço, e as duas de trás reconhecíveis como cabeças (focinho, olho, presa).
- **Ainda falta:** a oliva da referência é escura, e a 1× o N32D contrasta menos com o fundo da carta que o N32C; as
  cabeças de trás ainda têm a ponta do focinho reta; os pescoços de trás são faixas simples. Aguarda a avaliação do 32
  antes de qualquer adaptação para 16.

# A adaptação do N32D para 16: N16D (23/10/2026, protótipo; candidata em avaliação, nada no jogo)

**Decisão do Jean:** o N32D (`a7503ed9`) aprovado como base da adaptação, preservado intacto; uma fonte nova em 16, pelo
processo do Dragão (o 32 orienta as posições e os volumes; a adaptação é resolvida à mão na grade de 16). A ordem do que
preservar: as três cabeças para a esquerda; a principal maior, à frente e embaixo; o focinho, a sobrancelha, a boca e a
mandíbula dela; a separação das menores e a continuidade dos pescoços.

- **O N16D** (`hidra-n16d`, `GRADE_16D` em `grade.py`, com a paleta oliva do N32D), à mão, por partes (a cabeça de cima, o
  pescoço dela, a da direita, o pescoço dela, o pescoço da principal e a principal), com o N32D reduzido a 2:1 como mapa:
  - a principal: o alto do crânio e a sobrancelha acesos, a sombra sobre o olho, o focinho com a narina, o lábio, a boca
    aberta (o fundo escuro com a língua), a mandíbula acesa e a sombra embaixo; o pescoço saindo de trás da mandíbula, o
    ventre claro embaixo;
  - as de trás: cada uma com o alto aceso, a sombra da testa sobre o olho, o focinho e uma presa.
- **Na bancada:** três presas de 2×2 na principal viravam blocos brancos demais na carta; ficaram uma em cima e uma embaixo.
  As cabeças de trás sumiam um pouco contra o fundo escuro da carta; o alto delas ficou aceso.
- **A fonte, pelo Aseprite em lote** (`python auxiliares/exportar.py --montar hidra-n16d`; o conector sem editor, a janela
  aberta do Jean não foi tocada): 0 diferentes na releitura; reaberta com a guia oculta (`guias/hidra-d-guia-16.png`) e as
  camadas na ordem; a exportação igual ao composto, alfa 0/255, o 32 da carta e os @2x em blocos inteiros. O N32D
  reexportado saiu igual.
- **A foto** (`MODOS=n16d`), pela guardiã na luta, a 1920×945, com os mesmos dados e a mesma caixa da carta do N32D, sem
  erro no console. **A folha:** `adaptacao-16.png` (`python auxiliares/prancha.py --e`: a referência, o N32D × o N16D na
  mesma carta, a carta a 2×, a fileira e o diagnóstico).

## A minha leitura do N16D (quem decide é o Jean)

- **Preservou:** as três cabeças distintas, todas para a esquerda; a principal maior, embaixo e à frente, com o olho sob a
  sobrancelha, a boca aberta e a mandíbula; as de trás com olho e presa; os pescoços contínuos, o da principal com o ventre.
- **Perdeu:** o crânio arredondado da principal vira um degrau; a narina e a língua são de um pixel; as cabeças de trás têm o
  focinho curto, e a da direita é a que menos se destaca do fundo; a 1× o conjunto é uma massa oliva com três olhos e a boca.

# O ajuste da presa de cima: N16D2 (23/10/2026, protótipo; em avaliação, nada no jogo)

**Pedido do Jean:** o N16D agradou; só a presa de cima da principal ficou na ponta do focinho, uma barra branca vertical.
Recuar para dentro da boca, reduzir a altura se preciso, nascendo sob o maxilar com um espaço escuro até a ponta; sem
acrescentar dentes, numa cópia (o N16D fica).

- **O que mudou** (`hidra-n16d2`, `GRADE_16D2` em `grade.py`): só as linhas 10 e 11. A presa ocupava a coluna da ponta
  (x1) nas duas linhas; agora a linha 10 é só o lábio, e a presa tem um pixel, na linha 11, recuada uma coluna (x2), com o
  vermelho escuro da boca em x1, entre ela e a ponta. A cabeça, a expressão, a mandíbula, a presa de baixo, as outras duas
  cabeças e os pescoços como no N16D.
- **A fonte, pelo Aseprite em lote** (`python auxiliares/exportar.py --montar hidra-n16d2`): 0 diferentes na releitura;
  reaberta com a guia oculta e as camadas na ordem; a exportação igual ao composto, o 32 da carta e os @2x em blocos
  inteiros. O N16D reexportado saiu igual.
- **A foto** (`MODOS=n16d2`), na mesma luta e na mesma caixa da carta, sem erro no console. **A folha:** `presa.png`
  (`python auxiliares/prancha.py --f`: o N16D × o N16D2, a carta a 2×, a fileira e o diagnóstico).
- **A minha leitura:** na carta a 32 px, a barra branca da ponta some; a presa fica como um ponto claro dentro da boca, e a
  ponta do focinho volta a ler como focinho.
