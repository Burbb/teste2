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
