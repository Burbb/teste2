---
name: arte-aneis-fenda
description: Construir, revisar ou avaliar anéis em pixel art em The Unquiet (Crônicas da Fenda), do anel básico do começo do jogo a acessórios especiais. Use junto da arte-itens-fenda sempre que o objeto for um anel, para seguir as referências do Jean, resolver o aro (a faixa de fora, a parede de dentro, as bordas, o que fica na frente) na perspectiva preferida antes de pedra, engaste ou ornamento, e comparar com a referência principal. Não serve para amuletos, braceletes nem coroas.
---

# Anéis em pixel art

O anel levou três rodadas até o aprovado (1.140.0), sempre por **construção e ângulo**, e não por cor ou detalhe: o
aro achatado visto de cima, depois o aro em pé com a abertura inclinada para o lado errado. Esta skill reúne o que
essas rodadas ensinaram.

**Como usar com a skill geral:** ela complementa a `arte-itens-fenda`, que continua valendo inteira: antes de desenhar,
a política de tamanhos, o fluxo do Aseprite pelo MCP, conferir, entregar. Aqui fica só o que é próprio de anel. Ela não
aprova nada: termina numa proposta com fotos, e o Jean decide.

**O que é regra e o que é exemplo:** os princípios abaixo valem para qualquer anel. As escolhas do anel aprovado (o
ouro, o ziguezague gravado, a largura da faixa) estão em [exemplos.md](exemplos.md) e são exemplos de raciocínio, não
regras.

## As referências

Ficam em `ferramentas/arte/referencias/aneis/` (os PNGs originais; inspecione os pixels sem suavizar, ampliando por
vizinho mais próximo). O Jean as mandou em 19/10/2026 como de um mesmo artista; a autoria e a origem não foram
informadas (não invente). O registro anterior, na skill geral, continua em
[../arte-itens-fenda/referencias-aneis.md](../arte-itens-fenda/referencias-aneis.md).

- **A principal: `sample (2).png`** (64×64), o anel dourado isolado. Define a **perspectiva, a inclinação, a
  proporção da abertura e a distribuição da espessura**. Todo anel comum obedece a ela no ângulo.
- **As secundárias: `prancha-aneis-jean.png`, `EqoGsE.png`, `FB77t9.png`**, as pranchas do mesmo artista. Servem para
  o **acabamento** (o metal, os chanfros, o contraste, os reflexos), a **variedade de construção** (larguras, engastes,
  relevos, formas temáticas) e os **ornamentos e efeitos** dos acessórios especiais. Uma secundária não traz o ângulo
  dela junto.
- **Referência não é sprite:** nada dela é reduzido nem copiado (a regra geral da `arte-itens-fenda`).

## A perspectiva preferida

O aro **em pé, visto de três quartos e inclinado**, com a **abertura alongada subindo da esquerda para a direita** (o
eixo comprido do vão vai de baixo à esquerda para cima à direita). Ela dá continuidade visual à família de anéis; não
obriga todos a terem o mesmo metal, cor, largura, gema ou gravação.

## A construção: o aro antes de tudo

Um anel é uma **faixa de metal fechada** (um cilindro curto, oco). Antes de qualquer cor, responda por escrito quais
partes aparecem e onde:

- **A faixa de fora** do lado de perto: a face larga, em cima e à esquerda na perspectiva preferida.
- **A parede de dentro**: a face interna do lado de trás, vista pela abertura (embaixo e à direita), mais escura em
  cima, onde o próprio aro faz sombra, e mais clara embaixo, onde pega luz.
- **As bordas**: as duas beiras da faixa, que separam a face de fora da de dentro; numa faixa fina, uma linha clara de
  1 px ao longo do vão e da beirada.
- **O que está perto e o que está longe**: o trecho de perto passa na frente do de trás; o vão (o fundo aparecendo)
  fica entre a borda de perto e a parede de dentro do lado de trás.
- **A espessura**: a largura da faixa e a parede têm de ser legíveis; uma parede grossa vira um anel de borda grossa
  (um tubo), uma faixa estreita demais vira um fio.

**Resolva o aro sem decoração primeiro:** a silhueta, o vão e as faces numa cor só, depois a luz. Pedra, engaste e
ornamento só entram com o aro aprovado na comparação.

## Comparar com a referência

- **Lado a lado e na mesma escala:** a referência principal reduzida ao tamanho da proposta (e ampliada junto com ela,
  por vizinho mais próximo). Compare a **silhueta de fora**, o **formato e a inclinação do vão**, a **distribuição das
  faces** (onde aparece a faixa de fora, onde a parede de dentro) e **quais trechos ficam na frente**. Girar uma
  proposta pronta não resolve: confira essas quatro coisas.
- **O modelo 3D e as medidas ajudam, não decidem:** o aro como um cilindro curto projetado no quadro dá a perspectiva
  e a espessura coerentes em todo tamanho, e a busca do ângulo pela sobreposição da silhueta e do vão com a referência
  acha rápido a família certa. Mas dois eixos espelhados dão a mesma silhueta com as faces trocadas, e a nota pode
  preferir uma parede grossa que a referência não tem: quem decide é a comparação visual.

## O metal

- **Poucos planos de luz largos** (a luz da família: de cima e da esquerda), contraste e **reflexos agrupados**, não
  pontilhados soltos; a face de dentro mais escura que a de fora; um chanfro claro nas beiras dá a espessura da faixa.
- **Sem pixel solto:** a limpeza (`limpar` do `pixel_comum`) face a face, para não misturar a face de fora com a de
  dentro.
- **O material vem dos dados e da família:** o ouro, a prata, o ferro ou a cor da gema são escolhas de cada anel.

## Anéis básicos e avançados

- **Os básicos** (as bases comuns do começo do jogo): o aro na perspectiva preferida, com o acabamento das referências
  e, no máximo, um ornamento leve (uma gravação simples, um engaste pequeno). Nada de aura, partícula ou ornamento de
  item lendário.
- **Os avançados** (um único, um especial): as pranchas podem orientar engastes, relevos, formas temáticas e efeitos
  visuais, desde que **o aro continue reconhecível** e o efeito apoie a identidade da peça. Confira sempre no tamanho
  real e no contexto do jogo.
- **Não imponha efeitos a todo item raro nem acrescente animações automaticamente.** As soluções com efeitos ainda não
  foram validadas no jogo: a primeira que vier é uma proposta como as outras.
- **Ornamento no plano da faixa:** uma gravação acompanha a curva da faixa (desenhada nas coordenadas do aro, não por
  cima do pixel); feita no modelo, numa segunda passada, para a linha sair contínua e não em tracinhos.

## Os tamanhos

A política da `arte-itens-fenda`: comece pelo **tamanho principal de uso** (o 32 do equipamento, na ficha), resolva a
perspectiva nele e só então derive os outros (40 e 48 pela mesma construção; o 64 como o 32 ampliado 2×). A mesma
construção em todos: a simplificação por grade é esperada (um chanfro que vira 1 px, um ornamento mais simples); mudar
o ângulo ou as proporções num tamanho, não. Julgue pelo tamanho real; a ampliação serve para achar o pixel.

Os espaços vazios do anel usam o mesmo arquivo, apagado (`VAZIO` em `icones.js`): confira a silhueta do vazio junto.

## As ferramentas

- **O modelo do aro:** `ferramentas/prototipos/hud/itens-lote-noite/anel_amuleto/auxiliares/aro.py` (o cilindro
  curto: a face de fora, a de dentro e as bordas projetadas, a luz, o chanfro, a gravação; `liso` sem ela) e
  `ajuste_aro.py` (a busca do ângulo pela sobreposição com `sample (2).png` reduzida a 32).
- **O Aseprite pelo MCP:** a pintura pelo `ferramentas/arte/aseprite/pintar.lua`, como na seção "Desenhar no Aseprite"
  da `arte-itens-fenda` e em `ferramentas/arte/aseprite/LEIA-ME.md`; o composto do editor conferido pelo código de
  `ferramentas/prototipos/hud/itens-lote-noite/bandagem_pocao/auxiliares/soma.lua` (e `soma.py` nos PNGs).
- **As camadas úteis de um anel:** dentro, fora, gravacao (ou engaste e pedra), borda, brilho, contorno por cima.
- **A exportação:** `ferramentas/arte/exportar_aseprite.py` (`--fontes=` para uma proposta; `--conferir` na
  integração; o 64 pelo `DERIVADOS`).
- **As fotos:** `ferramentas/prototipos/hud/itens-lote-noite/fotografar.mjs anel_amuleto` (a ficha e o Inventário do
  Mago com um anel vestido e o outro vazio, o saque com a comparação; `ROTULO`, `PASTA`, `SO_ATUAL`, `SO_PROPOSTA` para
  comparar rodadas).

## Os problemas que já apareceram

Confira um por um antes de entregar:

- **O aro achatado, visto de cima:** largo e baixo, com a abertura quase redonda; sem presença no espaço e fora do
  ângulo preferido.
- **A abertura inclinada para o lado oposto:** o vão de cima à esquerda para baixo à direita (o eixo espelhado); a
  silhueta parece certa, as faces ficam trocadas.
- **A fresta:** o eixo virado demais para o lado, o vão vira uma fenda e o anel parece um bracelete grosso.
- **A borda grossa:** a parede larga demais faz um anel de borda (um tubo), longe da linha fina da referência.
- **A luz barrenta:** tons médios e escuros demais na face de fora; o metal perde o contraste.
- **As faixas de tom soltas:** o chanfro e o brilho virando listras e pontos na face de fora (resolvido com planos
  largos e a limpeza face a face).
- **A gravação em tracinhos:** a linha partida, que lê como trinca ou sujeira (resolvida desenhando a gravação numa
  segunda passada no modelo).

## A entrega

A da `arte-itens-fenda`, com mais três coisas:
- a comparação **referência × rodadas anteriores × nova**, ampliada e em tamanho real;
- as rodadas anteriores guardadas;
- o anel no jogo a 1920×945 (a ficha, o Inventário com um espaço vazio e o saque), com os mesmos dados.

Pare para a avaliação. Integração só do que o Jean aprovou.
