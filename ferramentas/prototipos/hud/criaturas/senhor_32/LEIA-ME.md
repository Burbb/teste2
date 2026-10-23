# O Senhor da Guerra: o estudo nativo de 32 e a proposta de 16 (23/10/2026, protótipo; nada no jogo)

**Pedido do Jean:** a S2 deu a direção (o veterano caolho com personalidade), mas a transposição seguinte (`senhor-t`,
recusada) não deixou o rosto compreensível. O caminho do Dragão e do Espantalho: primeiro em 32 nativos, com a cabeça
dominando o quadro e só o busto necessário; depois a adaptação à mão para 16, preservando proporções e planos, com olho,
venda, nariz, boca e barba legíveis, a venda sem virar um quadrado enorme e o olho sem virar um ponto branco arregalado. A
tentativa recusada não foi usada como base; a S2, a T e as outras propostas de `chefes_e_especiais/` ficam como estão.

## O que vem do jogo

O guardião da planície (`senhor_da_guerra`): 130 de vida, `humano` e `blindado`; Golpe Sujo, Golpe Esmagador, Invocar
(bandidos), Grito de Guerra, Varredura. "Um homem de armadura remendada com troféus de seus inimigos aguarda." Só aparece na
carta da luta (32); hoje sai do sprite `humano`. **Para a integração futura:** um papel pelo id do guardião, como o Dragão
de Gelo (`RETRATO_GUARDIAO`).

## Como foi feito

- **As referências:** `ferramentas/arte/referencias/icones/Senhor da guerra caolho-3.png` (a anatomia, a perspectiva e a
  expressão: a cabeça raspada em três quartos para a esquerda, a testa pesada sobre o olho visível semicerrado, a venda com
  a tira subindo pela testa e seguindo até a orelha, a cicatriz atravessando acima e abaixo da venda, o nariz largo, o
  bigode, a boca de cantos caídos, o lábio de baixo, a barba cheia); os retratos aprovados (a pele do Mercenário, a luz de
  cima e da esquerda, o contorno).
- **As guias** (`guias/senhor-guia-32.png` e `-16.png`, a camada `guia` oculta nas duas fontes): o recorte de 880 px a
  partir de (230, 190), reduzido por média (o alto da cabeça sai do quadro); mediram as posições, não ditaram os pixels.
- **O estudo nativo de 32** (`senhor-n32`), à mão:
  1. a primeira construção, num quadro mais aberto (a cabeça inteira, o machado na borda): lia como o caolho, mas o machado
     com 4–5 px virou uma lasca cinza ambígua e saiu (fica o manto de pele nos ombros); a barba em fios verticais virou
     listras;
  2. **o que não funcionou, apontado pelo Jean:** "um bebê de barba e tapa-olho". O crânio liso e redondo dominando o
     quadro, a pele clara e uniforme, o olho pequeno e as bochechas macias davam proporção de criança;
  3. a correção pela anatomia de adulto, num quadro mais perto: o alto da cabeça fora do quadro (menos cúpula), duas rugas
     na testa, o osso da sobrancelha aceso com a sobrancelha escura descendo para o nariz e o olho fundo na sombra (o branco
     apagado e a íris sob a pálpebra pesada), a maçã do rosto, o nariz largo projetando à esquerda com a narina, os sulcos
     ao lado do nariz, a boca de cantos caídos sob o bigode, o lábio de baixo aceso, a barba em tufos e a pele mais curtida.
- **A proposta de 16** (`senhor-n16`), redesenhada à mão com o 32 reduzido a 2:1 como mapa: a venda arredondada de 4×3
  (com o contorno), a tira em diagonal da testa até a venda e da venda até a orelha, a cicatriz em dois trechos, o olho de
  2 px (o branco apagado e a íris) logo abaixo da sobrancelha, o nariz em diagonal com a ponta e a narina, o bigode, a boca
  de três pixels com os cantos descendo, o lábio de baixo e a barba. Alguns realces soltos que salpicavam o rosto foram
  apagados.
- **As fontes, pelo Aseprite em lote** (`python auxiliares/grade.py ..` e `python auxiliares/exportar.py --montar`; o
  conector continua sem editor, a janela aberta do Jean não foi tocada): 0 diferentes na releitura de cada camada; reabertas,
  com as camadas guia (oculta), manto, pele, barba, cicatriz, traços (o preto do olho e da boca), venda e contorno. A
  exportação é igual ao composto; alfa só 0 ou 255; os derivados em blocos inteiros que voltam ao original.
- **As fotos** (`auxiliares/fotografar.mjs`, `capturas/`), pelo guardião na luta (`CHEFE=senhor_da_guerra`, com um
  bandido), a 1920×945, com os mesmos dados nos cinco modos (o jogo, a S2, a T, o N32 e o N16), sem erro no console.
  **A folha:** `comparacao.png` (a referência e a guia, a luta em tamanho real, a carta a 2×, a fileira com os aprovados e o
  diagnóstico).

## A minha leitura (quem decide é o Jean)

- **O N32** é o mais próximo da referência: um veterano duro, com a testa pesada, o olho fundo e severo, a venda que se
  entende (a tira, o tapa-olho e a volta até a orelha), a cicatriz, o nariz e a boca de cantos caídos. A barba ainda é a
  parte mais granulada.
- **O N16 preservou** a cabeça raspada cortada no alto, a venda arredondada com a tira, a cicatriz, o olho sob a
  sobrancelha (não arregalado), o nariz, a boca e a barba separados, e o manto. **Perdeu** as rugas da testa, a maçã do
  rosto e os sulcos do nariz; a venda, por proporção, é a mancha mais forte do rosto, e o rosto lê mais duro que severo.
  Lê melhor que a T: os traços estão no lugar e a venda se encaixa na cabeça.
- **Na fileira:** o N16 tem o grão dos vizinhos; o N32 destoa, como os outros estudos de 32.

## No jogo (1.194.0): o N16, pelo id do guardião

- **Decisão do Jean:** o N16 aprovado para integrar, sem retoques; o N32, a S1, a S2 e a `senhor-t` ficam como estudos.
- **A fonte de produção:** `ferramentas/arte/aseprite/retrato-senhor-da-guerra/retrato-senhor-da-guerra-16.aseprite`,
  copiada byte a byte da fonte do N16 em `f105fd10`; o 32 da carta é o 16 ×2 (`DERIVADOS`). A exportação saiu igual byte a
  byte à proposta (o 16, o 32 e os @2x), e o `--conferir`, tudo igual.
- **No jogo:** `retrato-senhor-da-guerra` pelo id `senhor_da_guerra` (`RETRATO_GUARDIAO`); o mercenário, o bandido e os
  outros humanos com os deles; o Profeta das Cinzas e o antagonista no sprite `humano`. Nenhuma regra mudou.
- **Conferido com os arquivos de produção** (`capturas-1194/`, `auxiliares/fotografar_jogo_senhor.mjs`): o guardião na
  luta com o Mercenário e o Bandido, cada um com o seu arquivo, sem erro no console e sem pedido ao protótipo. A folha
  `../../integracoes-22-10/integracoes-1194.png`.
