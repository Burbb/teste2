# O Dragão de Gelo em 32×32 nativos (23/10/2026, um teste; nada no jogo)

**Pedido do Jean:** testar se a grade de 16 é uma parte importante do problema das transposições (reduzir uma
referência grande a 16×16 e reconstruí-la tem mudado anatomia, proporções e expressão), sem transformar a hipótese numa
mudança do projeto. Uma proposta trabalhada, só no protótipo: a fonte com 32×32 pixels desenhados nessa resolução (não o
16 ampliado), o @2x como a ampliação exata para 64, a carta com os mesmos 32×32 de hoje (sem mexer na caixa, no layout
nem nas áreas de clique). O exportador de produção e os outros retratos não mudaram.

## O que vem do jogo

O Dragão de Gelo (`dragao_de_gelo`, guardião da montanha; 130 de vida, `voador`; Mordida Gélida, Golpe Esmagador, Grito
de Terror, Varredura; resiste ao gelo, fraco ao fogo; "Um dragão serpentino de escamas azul-gelo desdobra as asas sobre
você."). Hoje, na carta da luta, o sprite do traço `voador`. Só aparece na carta (32).

## Como foi feito (o caminho real)

- **As referências:** `ferramentas/arte/referencias/icones/Cabeça ancestral de dragão de gelo-2.png` (a anatomia, o
  enquadramento, a direção da cabeça e a expressão; é pixel art de uns 62 px de lado, ampliada), os retratos aprovados (a
  paleta, o contraste, a luz de cima e da esquerda, o contorno escuro) e as tentativas recusadas (a D1, a D2 e a `dragao-t`,
  só para achar os problemas: a cabeça arredondada e a boca simplificada, com cara de fantoche).
- **A guia** (`guias/dragao-guia-32.png`, a camada `guia` oculta na fonte): o recorte quadrado de 1200 px a partir de
  (27, 27), reduzido a 32 por média (37,5 px por pixel). Serviu de mapa de posições; não ditou os pixels.
- **O desenho, à mão na grade de 32** (`auxiliares/grade.py`, uma letra por pixel, 13 cores). As tentativas no
  caminho, e por que foram refeitas:
  1. os planos marcados à mão nas medidas (o crânio, a testa, o focinho, a mandíbula, os chifres, o pescoço), depois o
     acabamento linha por linha;
  2. **recusada por mim:** a primeira cabeça saiu uma caixa de topo plano, com os chifres finos espetados e a garganta
     preenchendo o canto de baixo, o mesmo aspecto de fantoche;
  3. **a construção refeita pela referência:** a cabeça como uma cunha inclinada para a frente e para baixo; o topo do
     crânio numa placa clara que vira o chifre da frente (uma lâmina de 5 a 7 px na base) e o de trás na mesma direção; a
     testa pesada e clara sobre o olho, com o vinco escuro embaixo; o olho âmbar inclinado; o focinho projetado com a
     narina e o lábio de cima aceso; a boca subindo para trás até o canto sob a bochecha, a presa atravessando a linha; a
     mandíbula afinando até o queixo, com o fundo aparecendo embaixo dela; o pescoço atrás, mais escuro, com as duas juntas
     diagonais da referência e a crista em placas que saem contra o fundo;
  4. **as correções que vieram olhando na caixa:** o pescoço em tons soltos virou ruído; as placas da crista em faixas
     horizontais viraram um pente; os espinhos finos, uma barbatana; juntas demais deixaram o pescoço listrado. O pescoço
     foi escurecido um tom para a cabeça dominar.
- **A fonte, pelo Aseprite em lote** (`python auxiliares/exportar.py --montar`; o conector do MCP continua sem editor, e
  a janela aberta do Aseprite do Jean não foi tocada): `ferramentas/arte/aseprite/montar_camadas.lua` com `n=32` e o
  `pintar.lua`, cada camada relida pixel a pixel (0 diferentes, 0 fora da tela); a guia escondida depois; reaberta, 32×32,
  as camadas guia (oculta), cabeça, chifres, crista, boca, dentes, olho e contorno. A exportação do Aseprite (o composto)
  é igual à grade; alfa só 0 ou 255; o @2x (64) em blocos 2×2 que voltam ao 32. **De passagem:** o Aseprite da máquina
  tem uma extensão da PixelLab instalada, que escreve erros na linha de comando; não foi usada nem mexida.
- **As fotos** (`auxiliares/fotografar.mjs`, `capturas/`): a luta com o guardião e um lobo gélido (os mesmos dados nos
  três modos: o jogo de hoje, a `dragao-t` no arquivo de 32 que ela teria e a N32), o retrato entrando com o mesmo elemento
  que o `Icones.criatura(…, 32)` monta. Sem erro no console.
- **O zoom da HUD, medido:** o `--px` do jogo põe o retrato em pixels inteiros do aparelho. A 1920×945 a 100%, o retrato
  ocupa 32×32 px de tela; a 1536×756 a 125%, 25,6 px de CSS = 32 px do aparelho. Os dois desenhos ficam em escala inteira
  (o N32 a 1:1, o 16 a 2:1); a 150%, o navegador pega o @2x (64). Não há escala fracionada para deformar o 32.
- **A folha:** `comparacao.png` (a luta a 100% e a 125% em tamanho real, a carta a 2×, a fileira com o Grifo, o Lobo
  Gélido e outros aprovados, e o diagnóstico: a referência, a guia e os dois desenhos sem suavização).

## A minha leitura (quem decide é o Jean)

Julgado primeiro na carta, em tamanho real:

- **O rosto e a expressão ficaram mais claros?** A forma, sim: a 1× a N32 lê como uma cabeça de dragão adulto (os chifres
  para trás, a testa sobre o olho, o focinho, a mandíbula, a crista), e a `dragao-t` ao lado lê como um bloco. A
  expressão, só em parte: o olho tem 5 px (3 de largura, 2 de altura) e a presa 2 de largura; a ameaça vem mais da silhueta e da testa baixa
  do que do olhar.
- **A referência foi preservada melhor?** Sim, claramente: a cunha, a direção dos chifres, a testa, a mandíbula com o
  fundo embaixo e a crista estão onde a referência põe. Ficaram de fora as placas pequenas das bochechas e a curva da
  presa.
- **Os pixels menores combinam com os vizinhos?** Não inteiramente. A 1× a diferença é pequena, mas a 3× fica evidente:
  ao lado do Lobo Gélido e do Grifo (16 ×2), o Dragão tem um grão duas vezes mais fino e parece mais detalhado e mais
  "ocupado" que o resto. Num retrato só, ele destoa como de outro conjunto; se o 32 nativo virasse regra para os chefes, a
  diferença seria de família, não de um desenho.
- **Houve ganho de forma ou só de textura?** Principalmente de forma: o ganho que se vê a 1× é a silhueta e a construção.
  Parte do miolo (as placas da testa, as juntas do pescoço) é textura que a 1× vira granulado azul, e não acrescenta
  leitura.

**Conclusão do teste:** a grade de 16 é uma parte importante do problema. Em 32, a construção da referência coube sem
deformar, e a 16 ela não coube. O custo é a densidade diferente dos vizinhos. Nada integrado; nenhuma rodada nova aberta.
