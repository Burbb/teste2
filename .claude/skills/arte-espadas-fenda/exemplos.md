# A espada aprovada e as tentativas recusadas

Exemplos de raciocínio, não regras: a diagonal, o latão, a largura e a ponta centrada são escolhas desta espada, pela
referência principal (a espada de aço da direita de `ferramentas/arte/referencias/espada/espadasample.png`). O histórico
completo está em `ferramentas/prototipos/hud/itens-lote-noite/LEIA-ME.md` ("O remake do ferro") e as pastas das rodadas
em `ferramentas/prototipos/hud/itens-lote-noite/espada_maca/`.

## A espada básica (aprovada no `0fcfe18`; o 40 e o 48 no `441787e`, em avaliação)

Vale para as bases Espada e Montante, para a silhueta da arma vazia e para o comando Atacar do Guerreiro.

- **A composição:** na diagonal das armas da família (o pomo embaixo à esquerda, a ponta em cima à direita), com o ferro
  do machado aprovado, o latão do escudo na guarda e o couro do arco na empunhadura.
- **As proporções, medidas na referência:** a lâmina em cerca de 2/3 do comprimento, de largura constante; a guarda com
  cerca de 1,6 vez a largura da lâmina; a empunhadura curta; o pomo de aço. No 32, a lâmina um pouco mais larga que a
  da referência, para ter presença.
- **A ponta:** na referência, o vértice fica praticamente no eixo e os dois gumes fecham juntos, em linha quase reta,
  num trecho de cerca de **duas vezes a meia largura** da lâmina. No desenho, a meia largura cai em linha reta, igual dos
  dois lados, até o vértice no eixo (`larg(u) = ML · (U1 − u) / LT`, com `LT` = 4,6 nas medidas do quadro de 32). Uma
  varredura do comprimento e do vértice achou as combinações que terminam num pixel sobre o eixo sem degrau; das duas
  famílias, o **fechamento longo** (larguras no fim 1, 2, 4, 4, 5) ganhou do curto (1, 3, 4, 5), que deixava um degrau
  no gume de cima.
- **A luz:** o corte da lâmina no corpo é `8 8 5 3 3` (o fio claro, o plano médio, o escuro). No fechamento, os tons
  pela posição de cada pixel na sua linha: o fio claro até o vértice, que é o tom mais claro; o escuro até a linha antes
  do vértice; o médio no meio quando cabe.
- **O 40 e o 48:** a mesma construção, com o vértice ajustado por grade (36,2 no 32, 36,3 no 40, 36,05 no 48) para a
  ponta terminar num pixel sobre o eixo e descer sem degrau (larguras no fim 1, 2, 4, 5, 6, 6, 7), e a luz por linha em
  toda a lâmina, na proporção do corte do 32 (a regra em medidas fixas deixava o fio fino no 48).

## As tentativas recusadas

### A cunha (a rodada 1, `796edd2`; em `espada_maca/rodada1/`)

A lâmina larga na base, afinando por um trecho longo até a ponta. **O defeito:** sem um corpo de largura constante, a
lâmina lia como uma cunha, e não como uma espada; os gumes não eram paralelos.

### A agulha (a rodada 2, `87c12eb`; em `espada_maca/rodada2_ponta_antiga/`)

O corpo já regular, mas a largura caindo em **rampa reta** do começo da ponta até o vértice, num trecho longo. **O
defeito:** no pixel, o corpo terminava e sobrava 1 px por várias linhas, como um biquinho acrescentado.

### A ponta rombuda (`723cf8d`; em `espada_maca/rodada2_ponta_r2/`)

Os gumes por fórmula, o de cima quase reto e o de baixo em curva. **Os defeitos:** de luz, o fio claro parava uma linha
antes do vértice e os últimos pixels eram do plano médio e do escuro (uma "tampa" escura); de forma, o gume de baixo
fechava rápido demais e deixava o fim largo. A lâmina parecia cortada.

### O fechamento deslocado (`3962b93`; em `espada_maca/rodada2_ponta_r3/`)

A ponta desenhada pixel a pixel, com o fio claro até o vértice e o plano escuro acabando antes, mas com o gume de cima
reto e só o de baixo avançando (a receita anotada da rodada anterior). **O defeito:** o vértice ficou cerca de 1 px fora
do eixo no 32, com uma mudança brusca de direção perto do fim; uma ponta válida, mas diferente da referência. A receita
("um gume reto, o outro avançando") era a leitura de um detalhe da referência, aplicada como regra; a forma da
referência é a dos dois gumes fechando juntos.

## O que ficou de método

- Medir antes de desenhar: o eixo da lâmina, o desvio do vértice em relação a ele e as larguras por linha no fim.
- Resolver a silhueta numa cor, com o eixo numa camada auxiliar (o estudo em `espada_maca/fontes/estudo/`), e só depois
  o fio e os planos.
- Julgar a espada inteira em tamanho real, não só o último pixel.
- Desconfiar de receitas que fixam um lado ou pedem para mexer só nos últimos pixels: comparar com a referência.
