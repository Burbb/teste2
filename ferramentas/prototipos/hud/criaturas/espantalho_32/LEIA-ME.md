# O Espantalho Possuído: o estudo nativo de 32 e a proposta de 16 (23/10/2026, protótipo; nada no jogo)

**Pedido do Jean:** depois do Dragão de Gelo (o N16 integrado na 1.193.0), o mesmo caminho para o Espantalho. Primeiro
uma versão nativa de 32 pela referência; depois a adaptação à mão para 16, com o 32 como mapa. A transposição T
(`chefes_e_especiais/`, `espantalho-t`) era uma base conceitual aceita, não uma arte aprovada; a construção dela podia ser
corrigida. A T e as versões anteriores (E1, E2) ficam como estão.

## O que vem do jogo

O Espantalho Possuído do evento do milharal (`eventos/biomas.py`, `espantalho`): os números da árvore desperta (a família
`ent_jovem`), marcado com a origem `espantalho` (`Inimigo.origem`), que hoje o deixa no sprite dos traços (a planta, ou o
corrompido perto da Fenda) em vez do retrato da Árvore Desperta. Só aparece na carta da luta (32). "Um espantalho no meio
de um milharal. Você poderia jurar que, há um momento, ele estava olhando para o outro lado." **Para a integração futura:**
um papel próprio pela origem já existente (como o Mímico, `RETRATO_ORIGEM`), com o retrato da Árvore Desperta e as regras
compartilhadas intactos.

## Como foi feito

- **As referências:** `ferramentas/arte/referencias/icones/Espantalho possuído em pixel art-5.png` (a forma e a expressão:
  de três quartos para a esquerda, o chapéu pontudo velho com a ponta caída e a aba larga despencando à direita, a cabeça
  de estopa inclinada, os olhos fundos de brasa sob dobras em ângulo, a boca costurada torta, a corda e a palha em leque na
  gola, o casaco escuro); os retratos aprovados (a paleta, a luz de cima e da esquerda, o contorno).
- **As guias** (`guias/espantalho-guia-32.png` e `-16.png`, a camada `guia` oculta nas duas fontes): o recorte de 1200 px a
  partir de (27, 27), reduzido por média; mediram as posições, não ditaram os pixels.
- **O estudo nativo de 32** (`espantalho-n32`), à mão, em quatro passadas:
  1. a construção: o chapéu dominando o alto (a copa com a ponta caída para a direita, a faixa escura, a aba larga com a
     borda acesa, a aba despencando pela direita até o ombro), a estopa embaixo da sombra da aba, as sobrancelhas de dobra
     descendo para o centro, as órbitas pretas com as brasas (o olho direito uma linha abaixo: a cabeça inclinada), a boca
     costurada, a corda e a gola;
  2. **o que não funcionou:** a estopa alternando claro e escuro como textura e a palha num xadrez de pontos. A estopa foi
     refeita em planos (a esquerda clara, a direita na sombra, a dobra da costura no meio) e a palha em fios contínuos em
     leque;
  3. o volume do saco amarrado: dobras convergindo para a corda, a palha em feixes de 2 px, os ombros do casaco;
  4. a boca: reta, com os dois cantos caídos, lia mais triste que cruel; torta, subindo à direita (um esgar), ficou.
- **A proposta de 16** (`espantalho-n16`), redesenhada à mão com o 32 reduzido a 2:1 como mapa. **A primeira passada perdeu
  a expressão:** os olhos viraram dois quadrados laranja (espanto, não ameaça), e a cabeça, uma caixa escura. A correção foi
  na distribuição das formas, sem textura: cada olho virou uma órbita preta com uma brasa só, o canto de dentro escuro, e a
  sobrancelha desce para o centro; a estopa clara voltou à bochecha esquerda e ao meio do rosto; o canto direito da boca
  sobe.
- **As fontes, pelo Aseprite em lote** (`python auxiliares/exportar.py --montar`; o conector continua sem editor, a janela
  aberta não foi tocada): 0 diferentes na releitura de cada camada; reabertas, com as camadas guia (oculta), casaco,
  estopa, chapéu, palha, costura, olhos e contorno. A exportação é igual ao composto; alfa só 0 ou 255; o @2x do 32 (64) e
  o 32 e o 64 do 16 em blocos inteiros que voltam ao original.
- **As fotos** (`auxiliares/fotografar.mjs`, `capturas/`), pelo evento real (o `cenario_excecoes.py` de
  `chefes_e_especiais`), a 1920×945, com os mesmos dados nos quatro modos (o jogo, a T, o N32 e o N16), sem erro no
  console. **A folha:** `comparacao.png` (a carta em tamanho real e a 2×, a fileira com os aprovados e o diagnóstico).

## A minha leitura (quem decide é o Jean)

- **O N32** é o mais próximo da referência: o chapéu velho com a aba caída, a cabeça inclinada, as brasas sob as dobras e a
  boca torta dão o espantalho cruel e inquietante; a palha lê como palha. A estopa ainda tem um pouco de granulado.
- **O N16 preservou** a silhueta do chapéu (a ponta caída e a aba despencando à direita), a cabeça de estopa clara contra a
  sombra da aba, as órbitas escuras com as brasas e as sobrancelhas para o centro, a boca costurada e a gola de palha em
  leque. **Perdeu** a inclinação da cabeça (os dois olhos na mesma linha), o torto forte da boca, as dobras do saco e a
  corda distinta; a expressão fica mais "olhar fixo que brilha" do que crueldade. Ainda assim lê melhor que a T: o olhar
  ameaça em vez de espantar, e a figura tem chapéu de espantalho, não um telhado.
- **Na fileira:** o N16 tem o mesmo grão dos vizinhos; o N32 destoa, como o estudo do Dragão.

# O refino: N32R e N16R (23/10/2026, protótipo; nada no jogo)

**Pedido do Jean:** o processo trouxe melhora, mas o N16 perdeu a expressão: a cabeça frontal e retangular, os olhos como
pontos acesos numa máscara, a boca sem a costura torta, a palha numa faixa de blocos. Refinar em cópias, com a referência
como autoridade de forma e expressão; o N32 como base, ajustável onde ajudar o 16. **Durante o trabalho, o Jean sugeriu**
puxar a arte para cima (parte do chapéu sai do quadro, o rosto ganha espaço) e **dispensou a aba caída** ("algo bem
abstrato"; a linha marrom cortando e a parte caída ficavam feias): o chapéu pode ser mais reto. A T, o N32 e o N16 ficam
como estavam (as fontes, as grades, as listas e os PNG conferidos iguais).

- **O quadro novo:** o recorte de 980 px a partir de (170, 150) (antes, 1200 a partir de (27, 27)); a ponta da copa e as
  pontas da aba saem pelas bordas e o rosto passa de ~14 para ~17 px de largura no 32. As guias novas
  (`guias/espantalho-r-guia-32.png` e `-16.png`, reduzidas por média como as antigas) ficam ocultas nas fontes.
- **O N32R** (`espantalho-n32r`), à mão, em passadas:
  1. no quadro antigo, a cabeça afunilada e a aba em diagonal; o rosto ainda pequeno;
  2. no quadro novo: o rosto largo na testa afunilando até o queixo, a borda esquerda acesa, o lado direito na sombra, as
     órbitas oblíquas descendo para o centro sob as dobras da testa (o olho direito uma linha abaixo: a cabeça inclinada),
     as brasas de um pixel, a boca numa costura torta (a linha sobe e desce, os pontos cruzando em tom mais claro, o canto
     direito subindo num esgar);
  3. **o que não funcionou:** a palha em fios paralelos repetidos voltou a ser uma fileira; virou dois tufos em leque com
     o vão da corda no meio. A aba caída (uma faixa cortando e a parte caindo do nada) saiu, a pedido do Jean: o chapéu
     ficou com a copa pontuda inclinada, a faixa e uma aba reta, um pouco mais baixa à direita, com a borda de baixo gasta;
  4. a órbita esquerda, que lia como um buraco grande, virou uma fenda oblíqua.
- **O N16R** (`espantalho-n16r`), redesenhado à mão com o N32R reduzido a 2:1 como mapa. Na primeira passada, as brasas
  laranja de um pixel de 16 (2×2 na carta) voltaram a ser pontos acesos e a palha, um xadrez de blocos; a brasa passou ao
  vermelho escuro dentro da órbita, a costura subiu uma linha (encostada no queixo, sumia no contorno) e a palha virou dois
  tufos separados pela corda.
- **As fontes, pelo Aseprite em lote** (`python auxiliares/exportar.py --montar espantalho-n32r espantalho-n16r`; o
  conector continua sem editor, a janela aberta do Jean não foi tocada): 0 diferentes na releitura de cada camada; reabertas,
  com a guia oculta e as camadas na ordem. As camadas por posição ficaram em `CORTES` (`grade.py`): a corda da gola na
  palha, a faixa do chapéu no chapéu.
- **As fotos** (`MODOS=atual,n16,n32r,n16r`), pelo evento real, a 1920×945, com os mesmos dados, sem erro no console (a
  foto do jogo saiu igual pixel a pixel à anterior). **A folha:** `refino.png` (a referência no quadro novo e a guia, a luta
  com as propostas anteriores e as novas, a carta a 2×, a fileira com os aprovados, o diagnóstico sem suavização).

## A minha leitura do refino (quem decide é o Jean)

- **Sobreviveu à adaptação:** o afunilamento do rosto até o queixo, a testa larga e acesa à esquerda com o lado direito na
  sombra, as órbitas oblíquas com as brasas contidas (o olho direito mais baixo), a costura torta com o canto subindo, os
  dois tufos de palha e o chapéu pontudo e gasto. Na carta, o N16R lê como um rosto de estopa com raiva, não como uma
  máscara de olhos acesos; o N32R é o mais próximo da referência.
- **Ainda se perde no 16:** os pontos da costura (no 16 a boca é uma linha torta com um degrau, sem os pontos
  cruzados), a inclinação fica só na diferença de uma linha entre os olhos e na aba, e as brasas, mesmo escuras, ainda são
  o ponto mais forte do rosto a 3×. O enquadramento mais perto deixou o chapéu menos alto que no N16: ele lê como chapéu
  pela aba e pela faixa, a ponta da copa fica fora.
- **Na fileira:** o N16R tem o grão dos vizinhos; o N32R, mais fino, destoa como os outros estudos de 32.

# A passagem no rosto: N16R2 (23/10/2026, protótipo; nada no jogo)

**Pedido do Jean:** o chapéu, o enquadramento, a palha e o corpo do N16R funcionam; o rosto não. Os olhos pareciam
desalinhados por acidente, as brasas liam como pontos numa máscara lisa, e a sombra das órbitas e a costura perderam a
malícia do N32R. Uma cópia (`espantalho-n16r2`), só no rosto; o N16R fica como estava (a fonte e os PNG conferidos iguais).

- **O que mudou:** só as linhas 7 a 10 (`GRADE_16R2` em `grade.py`), com o N32R como referência de expressão.
  - **Os olhos na mesma linha.** No 16, uma linha de diferença entre os olhos é metade da altura de uma órbita e lia como
    erro; a inclinação do rosto continua na aba (um pixel mais baixa à direita), onde ela cabe.
  - **A sombra oblíqua:** as sobrancelhas descem dos cantos de fora até se encontrar sobre o nariz (a carranca do N32R), e
    as brasas ficam no canto de dentro de fendas escuras, embaixo dela. A da direita, do lado da sombra, num vermelho mais
    apagado (`x`, `8a2414`): a perspectiva e a luz, não a simetria de uma máscara.
  - **As bochechas:** a sombra embaixo dos olhos em marrom, não em preto, e a bochecha direita mais clara, com volume.
  - **A boca:** a costura quebrada, com o canto direito subindo (o esgar), sobre a estopa.
- **Na bancada:** com os olhos alinhados e as duas brasas no vermelho vivo, o rosto virou uma caveira simétrica de dois
  pontos (a própria máscara); com o preto embaixo das brasas, as órbitas viraram buracos de caveira. As duas coisas saíram.
- **A fonte, pelo Aseprite em lote** (`python auxiliares/exportar.py --montar espantalho-n16r2`; o conector sem editor, a
  janela aberta do Jean não foi tocada): 0 diferentes na releitura; reaberta com a guia oculta e as camadas na ordem; a
  exportação igual ao composto; os derivados em blocos inteiros.
- **A foto** (`MODOS=n16r2`), pelo evento real, a 1920×945, com a mesma caixa da carta do N16R, sem erro no console.
  **A folha:** `ajuste.png` (o N16R × o N16R2 na mesma luta, o N32R ao lado, a carta a 2×, a fileira com os aprovados e o
  diagnóstico, com as linhas mudadas marcadas).

## A minha leitura da passagem (quem decide é o Jean)

- **Melhorou:** os olhos leem como intencionais, a carranca dá a ameaça e as brasas ficam dentro da sombra; a costura
  sobe num esgar; o rosto tem bochechas, não uma placa lisa.
- **Ainda é limite do 16:** os pontos cruzados da costura do N32R não cabem (a boca é uma linha quebrada), e a brasa do
  lado aceso, mesmo dentro da fenda, continua o pixel mais forte do rosto a 3×.

## No jogo (1.195.0): o N16R2, pela origem

- **Decisão do Jean:** o N16R2 aprovado para integrar, sem retoques; a E1, a E2, a T, o N32, o N16, o N32R e o N16R ficam
  como estudos.
- **A fonte de produção:** `ferramentas/arte/aseprite/retrato-espantalho/retrato-espantalho-16.aseprite`, copiada byte a
  byte da fonte do N16R2 em `bdef5a8a`; o 32 da carta é o 16 ×2 (`DERIVADOS`). A exportação saiu igual byte a byte à
  proposta (o 16, o 32 e os @2x), e o `--conferir`, tudo igual.
- **No jogo:** `retrato-espantalho` pela origem `espantalho` (`RETRATO_ORIGEM`), como o Mímico; a família `ent_jovem`, os
  números e as regras continuam os da árvore desperta, e a árvore desperta comum continua com o retrato dela.
- **Conferido com os arquivos de produção** (`capturas-1195/`, `auxiliares/fotografar_jogo_espantalho.mjs`): o Espantalho
  pelo evento real do milharal e uma árvore desperta comum na luta, cada um com o seu arquivo, sem erro no console e sem
  pedido ao protótipo. A folha `../../integracoes-22-10/integracoes-1195.png`.
