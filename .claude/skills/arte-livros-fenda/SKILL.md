---
name: arte-livros-fenda
description: Construir, revisar ou avaliar livros em pixel art em The Unquiet (Crônicas da Fenda), fechados, entreabertos ou abertos, tanto livros de equipamento (o grimório, o tomo) quanto ícones de livro da interface (o Grimório e o Diário da doca, o Habilidades da luta). Use junto da arte-itens-fenda sempre que o objeto for um livro, para escolher as referências, resolver capa, contracapa, lombada e bloco de folhas como um objeto só num ângulo coerente, e só então decorar. Não serve para pergaminhos soltos, mapas ou placas.
---

# Livros em pixel art

Os livros erraram mais que qualquer outro objeto da família. Foram cinco candidatos até o grimório do equipamento
(1.108.0) e três rodadas até o Grimório da doca (1.126.0), quase sempre por **construção**, e não por cor ou detalhe.
Esta skill reúne o que esses erros ensinaram.

**Como usar com a skill geral:** ela complementa a `arte-itens-fenda`, que continua valendo inteira: antes de desenhar,
o fluxo do Aseprite pelo MCP, conferir, entregar. Aqui fica só o que é próprio de livro. Ela também não aprova nada:
termina numa proposta com fotos, e o Jean decide.

**O que é regra e o que é exemplo:** os princípios abaixo valem para qualquer livro. As soluções de cada livro
aprovado (o ângulo, as cores, o emblema, a fita, o fecho ou a falta dele) estão em [exemplos.md](exemplos.md) e são
exemplos de raciocínio, não regras.

## As referências

- **Uma referência principal de construção e perspectiva.** Escolha uma imagem (ou peça ao Jean que diga qual) e tire
  dela o ângulo, quais faces aparecem e como elas se ligam. Todo o resto da construção obedece a ela.
- **As secundárias, cada uma com um papel dito por escrito:** a identidade (os materiais, o elemento mágico), a
  simplificação (como poucas formas explicam o livro), o acabamento. Uma secundária não traz o ângulo dela junto.
- **Não misture perspectivas.** Um livro com a capa de uma referência e as folhas de outra vira o "bloco com tampa" ou
  a lombada de um lado com as folhas do outro (ver os problemas abaixo).
- **Se faltar uma referência citada no pedido,** diga isso na entrega. Não invente o que ela mostraria.
- **Referência não é sprite:** nada dela é reduzido nem copiado (a regra geral da `arte-itens-fenda`).

## A construção: um objeto só

Um livro fechado tem quatro partes ligadas: a **capa da frente**, a **contracapa**, a **lombada**, que liga as duas, e
o **bloco de folhas**, contido entre elas. Antes de qualquer cor, responda por escrito:

1. **O ângulo:** de onde se olha. A partir dele, quais faces aparecem: no máximo três num objeto em caixa (a frente e
   duas laterais vizinhas).
   - Se a lombada aparece à esquerda, a beira das folhas do lado oposto (a da direita) não aparece.
   - As folhas aparecem só no lado que o ângulo mostra (embaixo, em cima ou do lado), e sempre entre as duas capas.
2. **A espessura:** duas capas finas, de espessura plausível, e o bloco de folhas, que é a maior parte da grossura.
3. **O recuo:** as folhas ficam um pouco para dentro das beiras das capas (a esquadria). Nas faces que aparecem, a
   beira de cada capa, a fileira de folhas e a beira da contracapa formam camadas paralelas.
4. **A lombada:** liga a beira da capa da frente à da contracapa, redonda ou reta, com o sulco da dobradiça entre ela e
   a capa da frente.
5. **A sobreposição:** o que está na frente cobre o que está atrás, sempre pelo mesmo ângulo. A capa da frente cobre
   as folhas, e as folhas cobrem a contracapa.

**Confira os volumes sem decoração.** Grave uma versão só com as capas, a lombada e as folhas, sem emblema, moldura,
ferragem nem fita, e olhe em tamanho real: o livro tem que se ler como livro já assim. Se não se lê, a decoração não
vai salvá-lo. No Grimório da doca, a etapa `construcao` do script grava exatamente isso.

**Livro entreaberto e aberto** (critérios próprios; o que já foi validado está em [exemplos.md](exemplos.md)):
- **O aberto:** dois blocos de folhas ligados pela dobra do meio.
  - As páginas são superfícies curvas: sobem da dobra e caem na beira, e a dobra escurece um pouco de cada lado, sem
    virar uma faixa.
  - A capa aparece por baixo e em volta, e as camadas das folhas, nas beiras.
  - Validado num caso: o Diário da doca (1.125.0).
- **O entreaberto:** a capa levantada tem que continuar presa à lombada, e o bloco de folhas tem espessura. Não pode
  parecer uma folha solta apoiada numa capa.
  - **Nenhum entreaberto foi aprovado até agora.** Os dois candidatos foram recusados (ver os exemplos). Trate esta
    pose como não validada e confira a construção com mais cuidado.

## A decoração: no plano onde está

Só depois dos volumes aprovados:

- **Cada enfeite acompanha o plano onde está aplicado:**
  - a moldura, o emblema e as cantoneiras ficam no plano da capa;
  - as nervuras, na lombada;
  - o fecho, na beira e na capa.
  - Num livro em perspectiva, desenhe-os nas coordenadas da face, e não da tela, para inclinarem junto dela. Um
    emblema "de frente" sobre uma capa inclinada parece colado por cima.
- **O emblema no centro da área útil da capa:** a área útil é o que sobra depois de tirar a faixa junto da lombada (o
  sulco e a quina), a moldura e o lugar reservado ao fecho. Centralize nela, e não no quadro do ícone, e deixe folga
  visível entre o emblema, a moldura e o fecho.
- **O espaço das ferragens é reservado antes:**
  - o fecho, as cantoneiras e os cravos têm lugar marcado antes do emblema;
  - o fecho tem que parecer preso a uma beira e sobreposto à capa: a tira sai de trás e deita sobre a frente;
  - fecho, fita e cravos são escolhas de composição, não uma lista obrigatória. Se não sobra espaço para um fecho que
    se leia, fica sem fecho.
- **A luz em poucos planos:** o couro é fosco (a regra de material da skill geral).
  - O alto e o lado da luz ficam mais claros, a beira oposta na sombra, com o sulco da dobradiça escuro e uma quina
    acesa junto dele.
  - As folhas ficam num creme separado do couro.
  - O elemento mágico pode ter a luz própria, mas pequena e no lugar dele.

## Os tamanhos

- **A mesma construção em todos:** o mesmo ângulo, a mesma espessura e o mesmo recuo. A simplificação por grade é
  esperada (menos linhas de folha, emblema mais simples, um cravo de 1 px, um detalhe que sai); mudar o ângulo ou as
  proporções num tamanho, não.
- **Julgue pelo tamanho real:** primeiro o reconhecimento e o volume, depois o detalhe. A ampliação serve para achar
  o pixel, não para aprovar.
- **Os usos reais:** confira todos. Um livro da interface pode ter dois papéis: o Grimório da doca é também o
  Habilidades da roda da luta, em 32.

## As ferramentas

- **O modelo 3D simples:** é útil e funcionou duas vezes, mas não é obrigatório. O livro vira capas, folhas e lombada
  em coordenadas próprias, cada pixel vem da face mais à frente e a decoração é desenhada nas coordenadas da face.
  Exemplos: `ferramentas/arte/desenhar_grimorio_fechado_pixel.py` (o equipamento) e
  `ferramentas/prototipos/hud/itens-lote-noite/doca_r3/auxiliares/grimorio_livro.py` (a doca). Desenhar à mão na
  grade também vale (o Diário foi assim), desde que as perguntas da construção estejam respondidas.
- **A grade, as camadas e o Aseprite:**
  - a grade à mão, com o mapa de camadas quando as cores se repetem entre partes, é lida por
    `ferramentas/prototipos/hud/itens-lote-noite/agilidade_aljava_ref/grades.py`;
  - a pintura no Aseprite pelo MCP passa pelo `pintar.lua`, como na seção "Desenhar no Aseprite" da `arte-itens-fenda`
    e em `ferramentas/arte/aseprite/LEIA-ME.md`;
  - as camadas úteis de um livro costumam ser contracapa, folhas, lombada, capa e as decorações, uma camada cada, com o
    contorno por cima.
- **A exportação:** pelo `ferramentas/arte/exportar_aseprite.py` (`--fontes=` para uma proposta, `--conferir` para a
  integração).

## Os problemas que já apareceram

Confira um por um antes de entregar:

- **A capa que dobra como um L:** a capa e uma "lateral" formam um canto vivo, como uma caixa, sem a espessura das
  folhas entre a capa e a contracapa.
- **As folhas num ângulo que não é o do livro:** por exemplo, a lombada à esquerda e a beira das folhas à direita, ou
  as folhas sem a contracapa por trás.
- **O livro que parece um bloco com tampa:** uma caixa grossa com uma placa por cima, sem capas finas nem folhas entre
  elas.
- **O emblema fora do plano:** de frente sobre uma capa inclinada, grande demais ou deslocado para um lado.
- **O fecho esmagado contra a decoração:** a tira encostando no emblema ou na moldura, sem folga, ou a tira que não
  parece presa a nenhuma beira.
- **A folha solta no entreaberto:** a página plana apoiada numa capa levantada, sem ligação com a lombada.
- **A dobra como faixa no aberto:** uma faixa escura larga no meio, e a escrita em colunas que parece tabela.

## A entrega

A da `arte-itens-fenda`, com mais três coisas:
- os volumes sem decoração ao lado do resultado, quando a construção mudou;
- as rodadas anteriores guardadas;
- a comparação da produção com os candidatos, com os mesmos dados, em tamanho real e ampliada.

Pare para a avaliação. Integração só do que o Jean aprovou.
