---
name: arte-luvas-fenda
description: Construir, revisar ou avaliar luvas e manoplas em pixel art em The Unquiet (Crônicas da Fenda), da manopla básica do equipamento a luvas de couro, de tecido, de malha, de placas, reais ou de fim de jogo. Use junto da arte-itens-fenda sempre que o objeto for uma luva, uma manopla ou outro equipamento das mãos, para escolher o caminho (a transposição fiel de uma referência visual que o Jean escolheu, ou a adaptação de uma base pronta, como a M5 da glove_04 da Dungeon Crawl Stone Soup, CC0), preservar mãos, dedos, polegares e proporções e só então cuidar do material e do acabamento. Não serve para anéis, braceletes soltos, armas nem o punho cerrado dos ícones de atributo.
---

# Luvas em pixel art

A manopla passou por muitas tentativas até a aprovada (a M5, `53d28893`): três rodadas desenhadas por medidas num
script (`c5fd33b`, `89be986`, `9509530`), uma à mão no Aseprite, um lote de seis construções independentes e duas
adaptações do Idylwild's Armory. Quase todos os erros foram de **anatomia** (os dedos, o polegar, a palma, a proporção
entre a mão e o punho), e não de material. O que resolveu foi **partir de um desenho de mão que já funciona**, em vez de
reconstruir a mão a partir de uma descrição: primeiro adaptando uma luva pronta (a M5), depois transpondo fielmente uma
referência visual escolhida pelo Jean (a L7, pelo processo das botas B3). Esta skill reúne isso.

**Como usar com a skill geral:** ela complementa a `arte-itens-fenda`, que continua valendo inteira: antes de desenhar,
a política de tamanhos, o fluxo do Aseprite pelo MCP, conferir, entregar. Aqui fica só o que é próprio de luva. Ela não
aprova nada: termina numa proposta com fotos, e o Jean decide.

**O que é regra e o que é exemplo:** a regra é **não inventar a anatomia**: a mão vem de um desenho pronto (a referência
escolhida ou uma base adaptada) e é preservada. A anatomia da M5 **não é mais obrigatória**: ela é um caminho, não o
molde de toda luva. Os materiais, a paleta, as tiras e a malha de cada luva são escolhas daquela luva. O detalhe da M5,
da L7 e das tentativas recusadas está em [exemplos.md](exemplos.md).

## Onde as luvas estão

- **No jogo hoje: a M5** (1.147.0), a luva de malha de ferro adaptada da `glove_04` da Dungeon Crawl Stone Soup.
  - **A origem:** `ferramentas/arte/externas/cc0_hand_wear_icons/original/glove-dcss/32x32/glove/glove_04.png`, arte dos
    **artistas do Dungeon Crawl Stone Soup** (esforço coletivo; mantenedor Chris Hamons; a lista de artistas no pacote
    original), do pacote "Dungeon Crawl 32x32 tiles" (https://opengameart.org/node/12210), **CC0**, desenhada em 32,
    reunida na coleção "CC0 Hand Wear Icons" montada por AntumDeluge (https://opengameart.org/content/cc0-hand-wear-icons).
    O registro completo está em `ferramentas/arte/externas/cc0_hand_wear_icons/LEIA-ME.md`.
  - **As fontes finais:** `ferramentas/arte/aseprite/manopla/manopla-32.aseprite`, `-40`, `-48` (camadas `original`
    oculta, `malha`, `couro`) e os PNGs `rpg/web/static/hud/icones/manopla-32.png`, `-40`, `-48`, `-64` (o 64 é o 32 ×2,
    pelo `DERIVADOS` do exportador). O 32 aprovado no `53d28893`, o 40, o 48 e o 64 no `2d18ce15`; o histórico da
    adaptação fica em `ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/malha_dcss/`.
  - **O crédito acompanha:** no `LEIA-ME.md` das externas e no das fontes (`ferramentas/arte/aseprite/LEIA-ME.md`).
- **A direção escolhida (20/10/2026): a L7**, o par de luvas de couro com a malha nas costas da mão e nos punhos, pela
  referência que o Jean escolheu (`ferramentas/arte/referencias/Luvas/luvas-par-recorte.png`, a forma; a
  `luvas-par-gerada.webp`, os volumes; os papéis no `LEIA-ME.md` de lá). **O sprite de 32 aguarda avaliação**, só no
  protótipo (`ferramentas/prototipos/hud/itens-lote-noite/luvas_l7/`); a M5 continua no jogo até o Jean decidir. O
  recorte tem marca d'água (um "©" e uma linha clara): a licença precisa ser esclarecida antes de qualquer integração.

## Os dois caminhos

### A. Transpor uma referência visual escolhida (o padrão quando o Jean escolhe um desenho)

O processo das botas B3 (`botas_ferro/b3/`) e da L7. A referência é o alvo visual: **não reinterprete** nem volte a outra
luva como molde. Se houver duas imagens (um recorte que define o desenho e uma imagem que esclarece os volumes), a forma
do recorte prevalece.

1. **Guarde a referência original** em `ferramentas/arte/referencias/Luvas/`, com o papel de cada imagem no `LEIA-ME.md`
   (o que define a forma, o que só esclarece os volumes, a origem e a autoria como foram informadas, sem inventar).
2. **Prepare uma guia proporcional para 32, sem esticar:** meça a referência. Se ela é pixel art ampliada, ache o
   tamanho do pixel e a fase da grade (a autocorrelação das bordas) e recupere a grade nativa (a cor mediana do miolo de
   cada célula, fora do borrão); se a grade nativa cabe no 32, use-a 1:1, só deslocada para centrar (a L7); se é maior,
   reduza a caixa do desenho proporcionalmente (a B3: ~58 px nativos em 30). Tire o fundo e a marca d'água de fora do
   desenho. A guia vai para o Aseprite como a camada `guia`, oculta.
3. **Adapte à paleta do conjunto:** cada pixel na cor mais perto (pela distância de cor) das rampas do conjunto (o
   ferro, o couro) e do contorno. Não use limiares de luminosidade fixos: eles clareiam ou escurecem tudo.
4. **Ajuste os pixels à mão,** cada ajuste com o porquê no script: o halo do fundo que sai, a beira que vira contorno
   (o desenho todo contornado com 1 px), a separação entre as luvas, os dedos e os polegares, o que a marca d'água
   estragou (refeito pelos vizinhos e pela imagem dos volumes).
5. **A malha simplificada pela escala:** o tom do volume (a média da vizinhança de malha na guia) com o xadrez de um tom
   acima e um abaixo, como na cota e na M5. Não tente encaixar cada anel da imagem ampliada.
6. **A fonte no Aseprite** em camadas úteis (a guia oculta, fora da exportação; o couro; a malha ou o metal; o contorno).

### B. Adaptar uma base pronta (o caminho da M5)

Para uma luva de outro material sobre uma mão que já funciona: uma cópia da base com a camada `original` oculta, e a
troca de material por regra sobre a cópia, sem mover pixel (o `manopla_perneiras/auxiliares/malha_dcss.lua` da M5: o tom
pela luminosidade do original, o contorno e as linhas dos dedos mantidos, o ornamento trocado pelo tom dos vizinhos), com
o acabamento à mão onde a regra não basta. Uma base nova precisa de licença clara (como na escolha `2f91cf62`) e da
confirmação do Jean antes de adaptar.

### O que os dois preservam

- a **pose** e a **composição** (uma luva ou o par, como no desenho escolhido);
- a **construção da mão**: as costas da mão, a linha dos nós, a mão que não é um bloco;
- os **dedos**: comprimentos diferentes, separados pelo contorno ou por um pixel de sombra, sem hastes nem ganchos;
- o **polegar**: a base perto do pulso, apontando para outra direção, ligado à mão;
- as **proporções**: a mão domina, o punho é curto; a presença ao lado do elmo, da cota, das perneiras e das armas.

## O acabamento: o que pode mudar

Separado da construção, numa ou mais camadas:

- **O material:** couro (fosco, a luz só da forma), tecido (fosco, as dobras pela sombra), malha (o xadrez de dois tons
  vizinhos, como a cota), placas (o metal com reflexo localizado; os reforços nas costas da mão, nos nós ou no punho).
  Os reforços podem mudar de lugar e de forma, desde que não apaguem a separação dos dedos.
- **Metais, cores e ornamentos:** ferro, aço, latão, ouro, prata; a cor do couro ou do tecido; bordados, gemas,
  ferragens, rebites, tiras e fivelas. Cada material tem a sua rampa e a sua regra de luz (a da `arte-itens-fenda`).
- **O nível do equipamento:** a luva **simples**, a **real** (metais nobres, bordado, uma gema) e a de **fim de jogo**.
  Quanto mais decorada, mais cuidado com os dedos: a decoração fica nas costas da mão e no punho.
- **Efeitos** (fogo, energia, gelo, sombra): possibilidades futuras, preservando a leitura da luva. Nenhum foi validado
  no jogo; não acrescente efeitos nem animações por conta própria.

O jogo diz o que a luva é (`rpg/itens.py`): o acabamento mostra isso, sem brilho mágico que o item não tem.

## Os tamanhos, a exportação e a avaliação

- **O 32 primeiro**, avaliado no jogo; o 64 = 32 ×2; o 40 e o 48 só depois da aprovação, pelo mesmo caminho na grade de
  cada tamanho (na B3: a guia com a caixa na proporção do 32, o contorno por dentro e os ajustes de cada grade; na M5: o
  `malha_dcss.lua` com `N`). O 32 aprovado não passa de novo pelo processo.
- **Exportar:** `python ferramentas/arte/exportar_aseprite.py <id> <pasta proposta> --fontes=<pasta fontes>` (a guia e
  a `original` ocultas ficam fora); confira o composto do editor contra o PNG (`bandagem_pocao/auxiliares/soma.lua` e
  `soma.py`) e contra a grade, e os @2x.
- **Avaliar em tamanho real:** a prancha sobre o carvão junto do elmo, da cota, das perneiras e das armas, com a
  referência e a ampliação sem suavização (`bandagem_pocao/auxiliares/montar.py`: `luvas_l7`, `malha_dcss`,
  `m5_tamanhos`); no jogo a 1920×945, pelo `ferramentas/prototipos/hud/itens-lote-noite/fotografar.mjs` (`luvas_l7`,
  `m5_tamanhos`): a ficha, o Inventário (40) e o saque (64 e o "você usa" em 48). Julgue pelo 1×.

## Os usos da manopla

O desenho `manopla` é a base Manopla do Guerreiro, os raros que usam o desenho da base e a silhueta das mãos vazias de
todas as classes (`VAZIO`). A habilidade Grito de Guerra usa o sprite `manopla` do jogo noutro papel e fica com ele; o
desenho de reserva das mãos sem base (`ICONE_ESPACO`) é a luva de couro. Trocar a manopla não troca esses outros papéis.

## A entrega

A da `arte-itens-fenda`, com mais três coisas:
- a comparação **referência (ou base original) × proposta**, em tamanho real e ampliada;
- o registro da origem, da autoria e da licença da referência ou da base (no `LEIA-ME.md` das referências ou das
  externas), com o que ainda falta esclarecer;
- a luva no jogo a 1920×945, ao lado do conjunto aprovado.

Pare para a avaliação. Integração só do que o Jean aprovou.
