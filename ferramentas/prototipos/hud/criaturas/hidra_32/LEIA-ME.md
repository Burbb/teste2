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
