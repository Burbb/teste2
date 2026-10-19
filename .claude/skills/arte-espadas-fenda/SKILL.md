---
name: arte-espadas-fenda
description: Construir, revisar ou avaliar espadas em pixel art em The Unquiet (Crônicas da Fenda), da espada básica do equipamento a lâminas especiais. Use junto da arte-itens-fenda sempre que o objeto for uma espada ou outra arma de lâmina longa (o montante, um sabre, uma lâmina curva), para seguir as referências do Jean, resolver a silhueta, as proporções entre lâmina e empunhadura, a continuidade dos gumes e a formação da ponta antes do acabamento, e comparar com a referência principal. Não serve para machados, maças, martelos, adagas de arremesso nem armas de haste.
---

# Espadas em pixel art

A espada básica levou duas rodadas e quatro pontas até a aprovada (`0fcfe18`): a primeira lâmina parecia uma cunha, e a
ponta foi uma agulha, depois rombuda, depois deslocada para um lado. Quase todos os erros foram de **forma** (a silhueta,
o eixo, o fechamento dos gumes), e não de cor. Esta skill reúne o que essas rodadas ensinaram.

**Como usar com a skill geral:** ela complementa a `arte-itens-fenda`, que continua valendo inteira: antes de desenhar,
a política de tamanhos, o fluxo do Aseprite pelo MCP, conferir, entregar. Aqui fica só o que é próprio de espada. Ela
não aprova nada: termina numa proposta com fotos, e o Jean decide.

**O que é regra e o que é exemplo:** os princípios abaixo valem para qualquer espada. As escolhas da espada aprovada (a
diagonal, o latão da guarda, a paleta, a largura da lâmina, a ponta centrada, as contagens de pixels de cada grade)
estão em [exemplos.md](exemplos.md) e são **exemplos de raciocínio, não regras universais**. Outra referência pode pedir
uma lâmina curva, uma ponta assimétrica, uma guarda grande ou nenhuma guarda.

**Uma lição sobre as instruções:** parte dos desvios da espada básica veio de **instruções prescritivas demais**, tanto
nossas quanto das receitas anotadas a cada rodada ("um gume reto e o outro avançando", "preserve quase tudo, mexa só nos
últimos pixels"). Seguidas ao pé da letra, levaram a outro formato. Quando uma receita e a referência discordam, vale a
referência: compare a forma com ela, não com a receita.

## As referências

Ficam em `ferramentas/arte/referencias/espada/`, com o papel de cada uma no `LEIA-ME.md` de lá (não duplique os PNGs).
Inspecione os pixels sem suavizar, ampliando por vizinho mais próximo. O Jean as mandou em 19/10/2026; a autoria e a
origem não foram informadas (não invente).

- **A principal: `espadasample.png`** (128×64), duas espadas simples. Orientam a **construção**: a proporção entre a
  lâmina e a empunhadura, a continuidade dos gumes, os planos do aço e a formação da ponta. A espada de aço da direita
  é a referência da leitura da lâmina da espada básica.
- **As secundárias: `espadas.png`, `espadasvariacoes.png`, `espadasefeitos.png`**: a variedade de silhuetas (larguras,
  guardas, lâminas curvas e serrilhadas) e o acabamento; os ornamentos e os efeitos ficam para armas avançadas. Uma
  secundária não traz a construção dela para a espada básica.
- **Referência não é sprite:** nada dela é reduzido nem copiado (a regra geral da `arte-itens-fenda`). Meça
  proporções nela; desenhe na grade de cada tamanho.

## A construção: a silhueta antes de tudo

Resolva a espada numa cor só antes de qualquer luz:

- **As partes separadas:** a lâmina, a guarda, a empunhadura e o pomo, cada uma legível no tamanho real. A lâmina tem
  presença (não pode sumir), mas sem virar um bloco.
- **As proporções da referência:** meça nela a parte da lâmina no comprimento total, a largura da lâmina, a largura da
  guarda em relação à lâmina e o comprimento da empunhadura. Adapte à grade (uma lâmina um pouco mais larga no 32, por
  exemplo, para não sumir), mas parta das medidas, não do olho.
- **Os gumes contínuos:** numa lâmina reta, os dois gumes seguem a forma da lâmina sem ondular. A largura que muda ao
  longo do corpo (uma base larga afinando por um trecho longo) faz uma **cunha**.
- **A ponta é uma construção, não um acréscimo:** os gumes convergem até o vértice como continuação do corpo. Leia na
  referência **de que lado e em que comprimento** os gumes fecham e **onde o vértice fica em relação ao eixo** da lâmina.
  Na espada básica, os dois gumes fecham juntos, num trecho curto, e o vértice fica no eixo; outra referência pode ter
  outra resposta.
- **Os defeitos de ponta que já apareceram** (o detalhe em [exemplos.md](exemplos.md)): a **agulha** (o corpo acaba e
  sobra um trecho de 1 px), a **rombuda** (a lâmina parece cortada no fim), o **fechamento deslocado** (o vértice fora do
  eixo e uma mudança brusca de direção perto do fim).

## Comparar com a referência

- **Primeiro a silhueta, depois a luz:** compare a silhueta numa cor, ampliada sem suavização e na mesma escala da
  referência, antes de julgar o acabamento. Separe o problema de forma do de luz: a ponta rombuda tinha os dois.
- **O eixo como auxílio:** marque o eixo da lâmina numa camada auxiliar (no Aseprite, num arquivo de estudo separado da
  fonte que se exporta) e meça onde o vértice fica em relação a ele, na referência e na proposta. Num estudo, meça
  também as larguras por linha no fim da lâmina: elas mostram degraus e trechos de 1 px que o olho perde.
- **A espada inteira, não só o último pixel:** confira em tamanho real a espada toda e a ponta ampliada; julgue a ponta
  pela leitura do conjunto.
- **Medidas ajudam, não decidem:** uma varredura de parâmetros (o comprimento do fechamento, a posição do vértice) acha
  rápido as combinações sem degrau, mas a escolha final é pela comparação visual com a referência.

## Os planos do aço

- **Poucos planos:** o lado da luz (de cima e da esquerda, a luz da família), o plano médio, o lado da sombra; um fio
  claro no gume da luz. Uma faixa clara que engole a face inteira apaga a construção.
- **A luz segue a forma até a ponta:** o fio claro corre até o vértice, e os planos se estreitam junto com a lâmina. Se
  o fio acaba antes do vértice, sobra uma "tampa" escura, e a lâmina parece cortada.
- **Numa lâmina diagonal,** cada linha da grade é um corte da lâmina; distribuir os tons pela posição do pixel na linha
  mantém a proporção dos planos no corpo e no fechamento.
- **Sem pixel solto:** a limpeza (`limpar` do `pixel_comum`) apaga linhas diagonais de 1 px (um sulco, uma aresta, as
  voltas de uma empunhadura); marque essas linhas em `fixo`.
- **O material vem dos dados e da família:** aço, latão, couro, a cor de uma lâmina rúnica, cada um é escolha da espada.

## Espadas básicas e avançadas

- **As básicas** (as bases comuns): a construção limpa, sem efeito, aura, partícula ou gravação brilhante.
- **As avançadas** (únicos, armas mágicas): as pranchas secundárias mostram ornamentos, lâminas temáticas e efeitos
  (fogo, gelo, eletricidade, fumaça). São **possibilidades futuras**: o efeito apoia a identidade, sem tirar a leitura
  da lâmina, da guarda e da empunhadura. Nenhuma solução com efeito foi validada no jogo ainda; a primeira é uma
  proposta como as outras. Não acrescente efeitos nem animações por conta própria.

## Os tamanhos

A política da `arte-itens-fenda`: o 32 primeiro (o tamanho mais visto), avaliado no jogo; o 64 como o 32 ampliado 2×; o
40 e o 48 depois da aprovação, **pela mesma construção**. A ponta não se copia contando pixels: em cada grade, o fecho
dos gumes cai de um jeito; ajuste o que for preciso (uma fração de pixel na posição do vértice, a regra dos planos pela
proporção do corte) para manter a mesma forma e a mesma leitura. Confira a ponta de cada grade ampliada lado a lado.

## As ferramentas

- **O desenho:** um script no protótipo (o da espada básica: `ferramentas/prototipos/hud/itens-lote-noite/espada_maca/
  auxiliares/desenho.py`), as medidas num sistema que segue a arma (ao longo do eixo e através dele), no quadro de 32.
- **O Aseprite (pelo MCP):** as listas de cada camada pintadas pelo `ferramentas/arte/aseprite/pintar.lua` num
  `execute_script` (nunca o `put_pixels`); as camadas úteis de uma espada: empunhadura, pomo, guarda, lamina, contorno.
  O composto do editor conferido pelo `soma.lua` (`ferramentas/prototipos/hud/itens-lote-noite/bandagem_pocao/
  auxiliares/`) contra o PNG exportado e a prévia (`soma.py`).
- **A exportação:** `ferramentas/arte/exportar_aseprite.py` (`--fontes=` numa proposta; o 64 pelo `DERIVADOS` na
  integração); os @2x conferidos como duplicação exata.
- **As fotos e as folhas:** `ferramentas/prototipos/hud/itens-lote-noite/fotografar.mjs` (`espada`, `espada_luta`,
  `espada_tamanhos`; `ROTULO`, `PASTA`, `SO_PROPOSTA`) e `bandagem_pocao/auxiliares/montar.py` (as pranchas da ponta e
  dos tamanhos). Lembre que a espada é também o comando Atacar do Guerreiro e a silhueta da arma vazia.

## A entrega

A da `arte-itens-fenda`, com mais três coisas:
- a comparação **referência × rodada anterior × nova**, em tamanho real e ampliada, com a silhueta numa cor;
- as rodadas anteriores guardadas e o diagnóstico de cada uma registrado;
- a espada no jogo a 1920×945: a ficha, o Inventário, o saque e o Atacar.

Pare para a avaliação. Integração só do que o Jean aprovou.
