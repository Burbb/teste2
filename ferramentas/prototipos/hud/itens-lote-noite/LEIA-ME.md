# O lote da noite: calça de couro, aljava, atributos e doca (propostas, nada no jogo)

**Pedido de Jean (18/10/2026, deixado para a noite):** voltar aos itens, com a skill de criação dos sprites
(`.claude/skills/arte-itens-fenda`).
- Fazer a calça de couro, de acordo com o resto do conjunto de couro.
- Refazer a aljava.
- Refazer os ícones dos atributos e os do menu inferior (a doca).

Uma peça por vez, com calma, sem substituir nada no jogo.

Cada peça é um script em `ferramentas/arte/desenhar_<peça>_pixel.py` (o método de `pixel_comum.py`), que grava a
proposta numa pasta daqui. O jogo não lê nada desta pasta e nenhum arquivo de `rpg/` mudou.

**`fotografar.mjs <peça>`** fotografa atual × proposta nos lugares onde a peça fica parada, nas janelas normal
(1500×950) e baixa (1280×720), com o jogo intacto:
- a página recebe os arquivos da proposta no lugar dos do jogo (`page.route`);
- uma peça sem papel em `icones.js` (a calça) ganha o papel só naquela página.

Pela skill, cada peça começa pelo 32 (o tamanho mais visto), para Jean avaliar a leitura no jogo; o 64 é o 32 ampliado
2× (como no couro aprovado); os 40 e 48 se derivam das mesmas medidas depois da aprovação do 32 (os scripts gravam a
prévia com `--intermediarios`).

## As decisões de Jean (18/10/2026)

- **A calça de couro:** o 32 foi aprovado. Os 40 e 48 estão prontos (rodada 2, abaixo), e os quatro tamanhos aguardam a
  avaliação de Jean.
- **A aljava:** refinar a leitura, principalmente no topo. A refinada está abaixo; os 40 e 48 aguardam a aprovação.
- **Os atributos e a doca:** as propostas perderam volume, personalidade e leitura dos materiais e ficam aqui como
  alternativas não escolhidas. **Correção de Jean (18/10/2026):** os ícones atuais de atributos e da doca são
  placeholders e continuam pendentes de substituição por pixel art de verdade; não foi decidido mantê-los. A skill
  ganhou a orientação de que símbolos da interface não precisam copiar equipamentos (a bota da Agilidade pode ter pose
  própria).

## 1. A Calça de Couro (`calca_couro`)

`ferramentas/arte/desenhar_calca_couro_pixel.py`; proposta em `calca_couro/proposta/` (32 e 64).

**Hoje:** não tem desenho da família. O jogo mostra o sprite 16×16 da calça recolorido (`S.calca_couro` em
`sprites-dados.js`). A Calça de Viagem (`calca_tecido`) está igual, mas não entrou neste lote.

**O desenho:**
- **Do conjunto de couro:** as rampas de `couro_r2.py` (couro, borda, cordão, desgaste), a luz em faixas chapadas (clara
  à esquerda, escura na beira da direita), o contorno comum.
- **O objeto:** um par de pernas de frente, como a perneira de ferro, que é o vizinho no mesmo espaço:
  - o cós de couro escuro de borda;
  - a braguilha amarrada com o cordão em zigue-zague do gibão;
  - as pernas afunilando, com o vão em V do gancho à barra;
  - um remendo costurado em cada joelho, dentro da perna;
  - um ponto de desgaste e o barrado escuro.
- **A perna da direita** fica um tom abaixo (a luz vem da esquerda).
- **13 cores.**

**Rodadas descartadas:**
- **1:** larga e quadrada, lia como bermuda; as costuras do joelho atravessavam a perna como faixas.
- **2 (a proposta):** pernas mais altas, o vão em V e o remendo dentro da perna.

**Conferido (`calca_couro/capturas/`, `calca_couro/ficha-atual-x-proposta-1500.png`):**
- **Na ficha (32 px):** lê como calça ao lado do capuz, do gibão e da bota.
- **No Inventário (40 px):** o espaço mostra o 32 menor (o 40 vem depois da aprovação).
- Sem erros.

**Para a integração:**
- o papel `calca_couro` em `ITEM` e `TAMANHOS` de `icones.js`;
- os 40 e 48 (a prévia pede retoque no remendo do joelho);
- se a fonte final for no Aseprite, como o resto do couro, as camadas saem das mesmas medidas.

## 2. A aljava (`aljava`)

`ferramentas/arte/desenhar_aljava_pixel.py`; proposta em `aljava/proposta/` (32, 64 e 24).

**Os papéis:**
- o equipamento secundário do Patrulheiro (a Aljava e a Aljava dos Mil Corvos);
- o ícone das flechas no topo, em 24 px (`RECURSO` em `icones.js`), um tamanho parado com arquivo próprio.

O mercado desenha a sua aljava em código (`telas/mercado.js`, a banca); ela não muda aqui.

**O desenho:**
- **O tubo:** de couro do conjunto, em pé, inclinado 22° para a direita (a 45° ele deitava e ocupava pouco do quadro);
  luz em faixas pela direção da superfície.
- **Os detalhes de couro:** a boca com a borda escura acesa em cima, duas cintas costuradas, o fundo arredondado mais
  escuro e uma alça de couro em arco do lado da sombra.
- **As flechas:** três, com a pena para cima, como se guardam; haste de madeira clara, penas claras e uma parda.
- **13 cores.**

**Rodadas descartadas:**
- **1:** a 45°, curta e deitada.
- **2:** em pé, mas o fundo encostava na borda (o contorno dava a volta na grade e aparecia no alto) e as penas se
  juntavam numa mancha.
- **3:** a origem subiu e as flechas abriram em leque.
- **4 (a proposta, pedido de Jean: as hastes legíveis como na aljava pintada original):**
  - a madeira ganhou um tom claro, para a haste ler contra o contorno;
  - as flechas saem mais da boca, com a madeira à vista antes da pena;
  - a pena virou um bloco claro de ~2 px, com a nervura de madeira por dentro;
  - a pena parda ficou clara o bastante para o carvão;
  - o tubo encurtou um pouco para caber.

**Conferido (`aljava/capturas/`, `topo-atual-x-proposta-1500.png`, `ficha-atual-x-proposta-1500.png`):**
- **Na ficha (32):** é da família do couro, mais sóbria que a atual pintada (sem a cinta dourada nem a fivela).
- **No topo (24):** reconhecível, mas mais discreta que a atual, que é mais colorida (vale olhar no jogo).
- **No Inventário (40):** continua a atual (o 40 vem depois).
- Sem erros.

## 3. Os ícones dos atributos (alternativa recusada; os atuais são placeholders pendentes)

`ferramentas/arte/desenhar_atributos_pixel.py`; proposta em `atributos/proposta/` (24 e 32, cada um na sua grade, nas
mesmas medidas).

**Os lugares e os papéis:**
- **Na ficha e no Inventário:** em 24, o mais visto.
- **Na luta:** a bota da Agilidade é também o comando Fugir, em 32 (`ACAO.fuga` em `icones.js`). Trocar a bota troca
  os dois.

**O desenho:** ficam os conceitos que já se leem, redesenhados na grade com rampas por material, luz de cima e da
esquerda em faixas e o contorno comum. Saem os degradês suaves das peças pintadas.
- **Ataque:** a espada na diagonal, com a lâmina de aço (o fio aceso do lado da luz), a guarda e o pomo de latão e a
  empunhadura de couro com o cordão.
- **Defesa:** o escudo de bico com a face de aço em duas metades pela aresta do meio (a esquerda acesa), a borda de
  latão e dois cravos.
- **Agilidade:** a bota de couro do conjunto (as rampas da bota, a dobra de camurça, a tira com a fivela, a sola) e
  três riscos de movimento de latão.
- **Poder:** a chama roxa em três línguas, nascendo de uma base redonda, com o miolo claro embaixo.

**Rodadas descartadas:**
- **1:** pequenas e magras no quadro de 24.
- **2:** a chama como uma gota de borda ondulada, que lia como cristal.
- **3 (a proposta):** formas maiores, ocupando o quadro como as atuais; o escudo com três faixas de luz por metade; a
  chama em três línguas.

**Conferido** (`atributos/capturas/`, `atributos-ficha-atual-x-proposta.png`, `fugir-atual-x-proposta.png`, 1500×950 e
1280×720, sem erros):
- **O que melhorou:** os quatro são legíveis em 24 e da mesma família pixel do couro. A bota é a mesma do conjunto.
- **O que pode ser pior:** são mais chapados que os atuais (menos volume e brilho). A chama, em 24, perde o halo de
  fogo da atual e lê mais como chama estilizada. O Fugir muda junto.

## 4. Os ícones da doca (alternativa recusada; os atuais são placeholders pendentes)

`ferramentas/arte/desenhar_doca_pixel.py`; proposta em `doca/proposta/` (36 e 32, nas mesmas medidas). Uma função
por ícone, desenhados um a um.

**Os lugares:**
- A doca usa o 36 (o 32 é para janelas mais estreitas; mesmo a 1280×720, ela usa o 36).
- O Grimório é também o comando Habilidades da luta (`ACAO.grimorio`): trocar um troca os dois.

**O desenho:** ficam os conceitos que já se leem, redesenhados na grade, com rampas por material e o contorno comum.
- **Talentos:** três nós de latão ligados.
- **Grimório:** o livro roxo com a lombada de nervuras, as folhas, os cantos e o fecho de ferro, o losango de latão e
  a pedra violeta.
- **Inventário:** a mochila nas rampas do conjunto de couro, com a alça, a aba, as alças de carregar, os bolsos e a
  tira com a fivela.
- **Mapa:** o pergaminho dobrado em três, o caminho tracejado e o X vermelho.
- **Diário:** o livro aberto sobre a capa de couro, com as linhas e a pena.
- **Bestiário:** o crânio de chifres.
- **Salvar:** o baú escuro com o aro de latão e a seta de ferro descendo.
- **Sair:** o arco de pedra com as juntas, a passagem escura com a luz no chão e a seta laranja saindo.

**Rodadas descartadas:** na 1, os chifres do Bestiário ficaram curtos e a seta do Salvar pequena; a mochila não
tinha as alças. Isso foi corrigido na 2, a proposta.

**Conferido** (`doca/capturas/`, `doca-atual-x-proposta-1500x950.png` e `-1280x720.png`, sem erros):
- **O que melhorou:** os oito são legíveis na doca e da mesma família pixel do couro.
- **O que pode ser pior:** mais chapados que os pintados.
  - No 36, as linhas do diário caem entre os pixels (aparecem só no 32).
  - Os nós dos Talentos têm um sombreado granulado.
  - O mapa tem menos textura de papel.

## Rodada 2 da calça: os 40 e 48, e a fonte em camadas

O 32 aprovado e o 64 (o 32 ampliado 2×) ficam iguais, pixel a pixel. Os dois intermediários saem da mesma construção
em `desenhar_calca_couro_pixel.py`.

**As formas em degraus, nas mesmas alturas relativas:**
- o quadril com a largura do cós até a linha 16 (do 32) e a perna recuada 1 depois;
- a fenda do gancho, escura e fechada, de 12 a 24;
- o vão aberto de 24 à barra.

A afunilada contínua da prévia punha o degrau em outra altura em cada grade: o vão mudava de proporção, e no 48 a
fenda tinha um fio transparente.

**A luz e os detalhes:** a luz pelas mesmas faixas; as costuras do remendo, o cordão da braguilha e o contorno ficam
com 1 px; o desgaste é um ponto. A fenda fica com 2 px no 40 e 3 no 48 (a proporção do 32).

**A fonte em camadas, como no couro:** `calca_couro/fontes/calca_couro-32/40/48.aseprite`.
- **As camadas** (de baixo para cima): pernas, remendo, cos, barra, braguilha, desgaste, contorno.
- **A montagem:** a linha de comando do Aseprite (`montar_fontes.sh` e `montar_fontes.lua`), com as listas por camada
  do script (`--listas`) e o `pintar.lua` de sempre. Cada camada foi relida sem diferença.
- **A conferência** (`conferir_fontes.py`): o composto de cada `.aseprite` é igual, pixel a pixel, à proposta, e o 64
  é o 32 ampliado 2×.
- **Na integração:** as fontes vão para `ferramentas/arte/aseprite/calca_couro/` com `64: (32, 2)` em `DERIVADOS`.

**Conferido a 1920×945** (`calca_couro/tamanhos-inventario-e-saque-atual-x-proposta.png`, atual × proposta):
- **O Inventário:** o 40.
- **O cartão do saque:** o 64 no achado e o 48 no "você usa". O cenário `vila` ganhou `VESTIDO=<desenho>`, para vestir
  uma calça e compará-la.
- **A ficha:** o 32.
- **Sem erros.**

## Rodada 5 da aljava: o refinamento do topo

**O pedido:** a rodada 4 ficou mais fina e escura que a atual e, no topo (24), perdeu presença.

**O 24 ganhou simplificações próprias do mesmo objeto (`PERFIL[24]`):**
- o tubo mais largo e mais inclinado, ocupando o quadro;
- o couro um degrau mais claro;
- a boca e a cinta com a borda acesa do lado da luz;
- uma cinta só;
- sem a alça (a 24 ela virava um risco escuro solto);
- as três flechas mais curtas, para caber no quadro, com as hastes claras e separadas e as penas em blocos.

**O 32 não mudou.** Na ficha ele já funcionava, e o 64 continua o 32 ampliado 2×.

**A rodada 4** fica em `aljava/rodada4/`.

**Conferido a 1920×945** (`aljava/atual-x-anterior-x-refinada.png`): no topo e na ficha, a atual, a anterior (rodada 4)
e a refinada. No topo, a refinada tem presença parecida com a atual. Sem erros.

## A calça de couro integrada (1.119.0)

Os quatro tamanhos do `ee0f01a` foram aprovados e estão no jogo, sem mudança de desenho. Como entraram:
- **As fontes:** `ferramentas/arte/aseprite/calca_couro/`.
- **A exportação:** `DERIVADOS`, com o 64 como o 32 ampliado 2×.
- **O papel:** `TAMANHOS` e `ITEM` em `icones.js`.

O desenho vale para todas as calças de couro do Arqueiro (Rasgada, Curtida, Reforçada e as raras com nome, como
"Mordida Antiga"); não há único de pernas. Os saves já guardam `icone: "calca_couro"` (conferido em quatro saves de
Jean), sem migração. A Calça de Viagem do Mago continua com o sprite.

**Conferido no jogo de produção, a 1920×945:** a ficha (32), o Inventário (40) e o saque (64 no achado, 48 no "você
usa"), sem erros.

## Rodada 6 da aljava: hastes e penas

**O pedido:** a rodada 5 lembrava uma bolsa de tacos de golfe; as pontas pareciam cabeças engrossadas (as penas eram
um bloco claro de 2 px).

**A reconstrução** (`desenhar_aljava_pixel.py`, com medidas próprias do 32 e do 24):
- **As hastes:** de 1 px, traçadas na grade.
- **As penas:** palhetas de 1 px dos dois lados da haste, que continua em madeira pelo meio; a flecha do meio tem as
  penas vermelhas, para separar as três.
- **O entalhe:** 1 px escuro além das penas, no 32.
- **A boca:** uma elipse em perspectiva, com o aro de couro aceso (o lábio da frente também) e o fundo escuro; as
  flechas saem de dentro dela.
- **A alça:** fica no 32 e sai do 24.

O 64 é o 32 ampliado 2×. A rodada 5 está em `aljava/rodada5/`, com o script dela.

**Conferido a 1920×945:** no topo e na ficha, a atual, a rodada 5 e a 6, sem erros. A comparação foi substituída pela
da rodada 7 (abaixo); a rodada 6 está em `aljava/rodada6/`.

## Ataque e Defesa, a rodada nova (`ataque_defesa/`)

Um script por ícone, que é a fonte editável, pelo fluxo da skill:
- `ferramentas/arte/desenhar_attr_ataque_pixel.py`;
- `ferramentas/arte/desenhar_attr_defesa_pixel.py`.

A proposta recusada (`desenhar_atributos_pixel.py`) fica como histórico.

**Os tamanhos:**
- **24:** o mais usado (a ficha e o Inventário), desenhado na própria grade.
- **32:** desenhado também. É a fonte do 64.
- **64:** o selo da festa de atributo permanente; é o 32 ampliado 2×. Hoje o placeholder não tem 64, e o selo usa o
  `32@2x`.

**Ataque:** uma espada de lâmina larga na diagonal, que ocupa o quadro.
- **A lâmina de aço em dois planos:** a face da luz clara, a da sombra escura, a aresta do meio acesa e o fio claro;
  um brilho especular na metade de baixo.
- **A guarda de latão:** um cilindro de través, acesa em cima, com as pontas arredondadas.
- **A empunhadura:** couro enrolado em faixas inclinadas.
- **O pomo:** uma esfera de latão, sombreada pela luz da família, com o ponto de brilho.

**Defesa:** um escudo de bico abaulado. A face de aço é sombreada pela normal de uma superfície curva, em faixas da
rampa:
- **A luz:** a esquerda de cima acende, a direita vira para a sombra, com um reflexo largo em cima à esquerda.
- **A borda de latão chanfrada:** a quina de fora acesa do lado da luz e a sombra dela sobre o aço.
- **A bossa no centro:** uma cúpula com brilho e a sombra embaixo à direita.

**Conferido a 1920×945** (`ataque_defesa/ataque-defesa-atual-x-proposta.png`, atual × proposta): a ficha (24), o
Inventário (24) e os dois selos (64), sem erros. Agilidade, Poder e os oito da doca ficam para os próximos pares.

## Ataque e Defesa integrados (1.120.0)

Jean aprovou os dois da comparação anterior; entraram sem retoque.

**As fontes em camadas:**
- **Ataque:** `ferramentas/arte/aseprite/attr-ataque/attr-ataque-24/32.aseprite` (lâmina, guarda, cabo, pomo,
  contorno).
- **Defesa:** `ferramentas/arte/aseprite/attr-defesa/attr-defesa-24/32.aseprite` (face, borda, bossa, contorno).

**O fluxo:** o script de cada ícone (`--listas`) e o montador genérico `ferramentas/arte/montar_fontes.py`. O 64 do
selo é o 32 ampliado 2× (`DERIVADOS`), e `TAMANHOS` em `icones.js` ganhou o 64.

**Conferido:**
- os doze arquivos exportados das fontes são idênticos aos aprovados (`b8637d0`);
- `exportar_aseprite.py todas --conferir` reproduz o jogo;
- na produção, a 1920×945: a ficha e o Inventário (24) e o selo de atributo permanente (64), sem erros.

Agilidade, Poder e os oito da doca continuam placeholders, pendentes em pares.

## Rodada 7 da aljava: só as flechas

**O pedido:** na rodada 6, as pontas ainda pareciam garfos ou argolas. O recipiente de couro fica igual; só as flechas
mudam.

**As flechas:**
- **Duas no lugar de três:** separam melhor. Uma tem as penas claras e a outra vermelhas.
- **As penas:** contínuas, desenhadas linha a linha a partir do fim da haste e centradas no pixel da haste daquela
  linha.
  - No 32, a meia-largura por linha é 0, 1, 2, 2, 1: o entalhe e depois uma folha de cada lado.
  - No 24, 1, 1, 1.
  - Como as hastes são inclinadas, as linhas deslocam e a forma fica diagonal. Os dois lados são simétricos, sem dentes
    soltos.
  - Por que linha a linha: a palheta medida na direção da flecha caía sobre os pixels da própria haste num dos lados e
    virava uma bandeira.
- **A haste:** de madeira, à vista entre as penas e a boca.
- **O entalhe:** só no 32, como 1 px escuro da haste além das penas (sem o "U").

O 64 é o 32 ampliado 2×.

**Conferido a 1920×945** (`aljava/antes-x-depois-rodada7.png`): o topo (24) e a ficha (32), antes (rodada 6) ×
depois, sem erros. Os 40 e 48 e a integração aguardam a aprovação.

## Rodada 8 da aljava: os intermediários 40 e 48

A rodada 7 (`5689148`) foi aprovada em 24 e 32, com o 64 ampliado 2×. Esses arquivos continuam iguais, pixel a
pixel.

**A derivação:** os 40 e 48 saem da construção aprovada do 32, pela função `_derivado` do script. As posições e os
comprimentos são multiplicados por n/32:
- **O que fica igual:** o recipiente, as duas flechas (a clara e a vermelha), as hastes à vista e a alça.
- **O que continua com 1 px:** a haste, a palheta das penas, a alça, o entalhe e o contorno.
- **As penas:** uma linha a mais por tamanho (40: 0,1,2,2,2,1; 48: 0,1,2,3,3,2,1).

**As fontes em camadas** (couro, borda, boca, hastes, penas, contorno) ficam no protótipo, em
`aljava/fontes/aljava/aljava-24/32/40/48.aseprite`, porque a aljava ainda não está no jogo. Elas são montadas pelo
fluxo de sempre, que ganhou a opção `--fontes=<pasta>` para propostas:

    python ferramentas/arte/desenhar_aljava_pixel.py <proposta> --listas
    python ferramentas/arte/montar_fontes.py aljava <proposta>/listas --fontes=<pasta>
    python ferramentas/arte/exportar_aseprite.py aljava <saida> --fontes=<pasta>

**A conferência:** os oito PNGs exportados das fontes são iguais à proposta, e o 64 sai do 32 (`DERIVADOS`). Na
integração, as fontes vão para `ferramentas/arte/aseprite/aljava/`.

**Conferido a 1920×945** (`aljava/intermediarios-inventario-e-saque.png`, atual × proposta): o 40 no Inventário, e o
48 no "você usa" do saque, ao lado do 64 no achado. O cenário `vila` usou `VESTIDO=aljava` e `ACHADO=aljava`. Sem
erros. A integração aguarda a avaliação.

## Agilidade e Poder, as propostas novas (`agilidade_poder/`)

Um script por ícone, pela skill, com o acabamento de Ataque e Defesa como referência:
- `ferramentas/arte/desenhar_attr_agilidade_pixel.py`;
- `ferramentas/arte/desenhar_attr_poder_pixel.py`.

**As fontes em camadas** ficam no protótipo (`agilidade_poder/fontes/`), montadas pelo fluxo de sempre com
`--fontes=`. Os doze PNGs exportados das fontes são iguais à proposta, e o 64 é o 32 ampliado 2× (`DERIVADOS`).

**Agilidade:** uma bota de couro em pleno passo, com pose própria (não é a bota do equipamento).
- **A pose:** inclinada para a frente, o calcanhar no ar e a ponta descendo (o impulso).
- **O volume:** o cano como cilindro, a dobra de camurça, a tira com a fivela, o peito do pé aceso, o brilho na ponta,
  a sola e o salto.
- **O movimento:** três rastros de velocidade atrás, claros junto da bota e apagando para trás.
- **As camadas:** rastros, sola, bota, dobra, tira, contorno.

A Agilidade é também o comando Fugir da luta (32, `ACAO.fuga`): trocar um troca os dois.

**Rodadas descartadas da Agilidade:**
- **1:** o cano inclinava para trás, e a bota parecia chutar; o couro estava claro demais.
- **2:** os rastros encostavam na borda, e o contorno voltava pela grade.
- **3:** deslocada para a esquerda.
- **4 (pedido de Jean):** o giro comia a ponta, que ficava com um corte reto. Agora o pé e a sola são uma forma só:
  o peito do pé desce do cano até um bico arredondado, o fundo sobe um pouco na ponta, e a sola acompanha a curva.

**Poder:** uma chama violeta viva.
- **A forma:** três línguas que ondulam, nascendo de uma base redonda, e faíscas soltas (uma no 24, duas no 32).
- **A luz:** sem desfoque. As camadas aninhadas são a silhueta da chama encolhida para a base, com uma rampa de
  deslocamento de matiz (do índigo da beira ao violeta, ao magenta-lilás e ao núcleo branco rosado); o lado de trás de
  cada camada fica um tom abaixo.
- **As camadas:** chama, núcleo, faíscas, contorno.

**Rodada descartada do Poder:** na 1, o núcleo era pequeno e o roxo chapado.

**Conferido a 1920×945** (`agilidade_poder/agilidade-poder-atual-x-proposta.png`):
- **Os quatro atributos juntos:** na ficha (24), com Ataque e Defesa já integrados e sem mudança.
- **Os outros usos:** o Fugir na roda da luta (32) e os selos de Agilidade e Poder (64).
- **Erros:** nenhum.
- **O que pode ser pior:**
  - A Agilidade ocupa menos o quadro que o placeholder e fica menor no selo.
  - A chama tem menos brilho que o placeholder pintado, mas lê como fogo vivo, e não como cristal ou gota.

Nada disto entrou no jogo, e os mapeamentos não mudaram. A doca fica para os próximos pares.

## Agilidade e aljava a partir das referências (`agilidade_aljava_ref/`)

**O pedido:** Jean mandou duas imagens de referência (`agilidade_aljava_ref/referencias/`: a bota e a aljava) e pediu
para refazer as duas peças por elas. Nenhuma proposta anterior fica aprovada para integração, nem a aljava da rodada 7;
as rodadas antigas ficam como histórico. Poder continua em avaliação (`agilidade_poder/`).

**Como foi feito** (as três operações, separadas):
- **Cálculos auxiliares fora do editor:** a silhueta das referências medida numa grade, só para as proporções, e um
  rascunho das regiões (polígonos e elipses postos à mão). Nada da referência foi reduzido para virar o desenho.
- **O desenho na grade:** cada tamanho redesenhado pixel a pixel em texto (`agilidade_aljava_ref/grades/`: uma letra
  por pixel, que diz a cor e a camada). `grades.py` acrescenta o contorno e grava as listas de cada camada.
- **No Aseprite, pelo MCP:** as camadas pintadas pelo `pintar.lua` (`execute_script`, nunca o `put_pixels`), com a
  releitura de cada pixel sem diferença, e salvas em `agilidade_aljava_ref/fontes/`. O composto do editor confere com
  as grades nos quatro arquivos.
- **A exportação:** `exportar_aseprite.py <peça> agilidade_aljava_ref/proposta --fontes=agilidade_aljava_ref/fontes`.
  Os doze PNGs saem iguais às grades, e o 64 é o 32 ampliado 2×.

**Agilidade (24 e 32, mesma bota e mesma pose):**
- **A silhueta:** a da referência, com o cano largo e a dobra de couro na abertura (a boca escura à vista). O tornozelo
  desce reto até o peito do pé, que só então avança, longo e baixo, até o bico redondo. O salto é um bloco sob o
  calcanhar, e a sola grossa desce para a ponta (o calcanhar no ar: a passada).
- **A luz:** a dobra é o plano mais claro, e embaixo dela fica a sombra no cano. O cano é um cilindro com um vinco
  claro. O calcanhar é aceso, e o bico tem um brilho.
- **Os detalhes:** a tira escura com a fivela quadrada vazada; os riscos de velocidade atrás, sem contorno, claros junto
  da bota (três no 24, quatro no 32).
- **As camadas:** rastros, sola, bota, dobra, tira, fivela, contorno.

**Aljava (32 primeiro; o 24 do topo simplificado):**
- **O recipiente:** um tubo de couro avermelhado, inclinado como na referência, com a base redonda e a faixa de luz à
  esquerda.
- **A boca:** elíptica, com o fundo escuro, a parede de trás acesa por dentro e a borda da frente com luz em cima.
- **As cintas:** duas, escuras e com a beira acesa, uma abaixo da boca e outra perto da base, com o latão (a argola em
  cima, o rebite embaixo). A alça pende do lado de fora; só no 32.
- **As flechas:** três, como na referência, em leque, para separar. A da esquerda e a da direita têm penas claras, e
  a do meio, vermelhas. As hastes claras aparecem entre a boca e as penas.
  - **As penas:** largas atrás, junto do entalhe, e afinando para a frente.
  - **O contorno:** as hastes ficam sem ele. Com o contorno, o fundo entre flechas a 1–2 px virava uma mancha escura.
- **No 24:** as mesmas três flechas, com as penas mais curtas e sem a alça (não cabe com fundo entre ela e o corpo).
- **As camadas:** alca, couro, cintas, latao, boca, hastes, penas, contorno.

**Conferido a 1920×945** (`agilidade_aljava_ref/agilidade-aljava-atual-x-proposta.png`), sem erros:
- a Agilidade na ficha (24), no Fugir da luta (32) e no selo (64);
- a aljava na ficha (32) e no topo (24).

O tamanho real sobre o carvão, ao lado de Ataque, Defesa, da aljava atual e da bota do equipamento, está em
`agilidade_aljava_ref/prancha-carvao.png`.

**O que pode ser pior:**
- No 24, as penas das flechas da esquerda e do meio ficam a 1 px uma da outra.
- A boca da aljava 24 fica quase toda coberta pelas hastes.
- A bota tem mais pixels soltos de ruga no cano que Ataque e Defesa têm de detalhe.

Nada disto entrou no jogo. Os 40 e 48 da aljava ficam para depois da aprovação desta direção.

### Agilidade: a junção da sola (rodada 2 das referências)

**O pedido:** a bota nova está boa, e o calcanhar levantado fica. O problema era a faixa preta entre o couro e a sola:
o degrau ali fazia o salto parecer um bloco solto do pé. Só a sola, o salto e a faixa do couro junto deles mudam, no 24 e no
32; o cano, a dobra, a tira, a fivela, o bico e os riscos estão iguais pixel a pixel.

**O ajuste:**
- **O perfil contínuo:** a base desce do salto para o arco e depois para a frente, uma linha por trecho (no 32, a cada 4
  a 6 px), sem o degrau escuro no arco.
- **A sola:** 2 px na frente e no arco. O salto tem a beira de cima acesa e a face da frente na sombra (4 linhas no 32,
  3 no 24).
- **As cores:** o quase preto da sola (`21160F`) virou marrons profundos (`2E2016`, `4A3628`, `6E5442`). A junção com o
  couro é 1 px do marrom escuro do couro, não uma fenda preta.

O 64 é o 32 novo ampliado 2×. O antes (os PNGs da rodada 1) está em `agilidade_aljava_ref/rodada1_sola/`. Conferido a
1920×945, antes × depois na ficha, no Fugir e no selo (`agilidade_aljava_ref/agilidade-sola-antes-x-depois.png`); a
ampliação está em `agilidade-sola-ampliada.png`.

### Aljava: os 40 e 48 da nova direção

**O pedido:** Jean aprovou a aljava nova em 24 e 32 (`ea3835f`), e o 64 é o 32 ampliado 2×. Faltavam os
intermediários. Os arquivos aprovados não mudaram (os 24, 32 e 64 exportados de novo são idênticos aos do commit).

**Como saíram** (`agilidade_aljava_ref/auxiliares/gen_n.py`, que reproduz as grades 40 e 48):
- **A construção:** a do 32 (o `corpo.py`, com o tubo, a base redonda, a boca e as cintas) medida na grade do tamanho.
- **As partes feitas à mão no 32:** a alça, o latão e o caminho das três flechas, levados para a grade por n/32, com as
  regras que o 32 seguiu (a borda da frente da boca acesa, as cintas com a beira de cima acesa e a de baixo escura).
- **No 40 e no 48:** o latão ganha 2×2 px. As penas crescem com a grade (5 linhas no 40, 6 no 48), largas atrás e
  afinando para a frente, e a pena de cá ganha 1 px atrás. As hastes continuam sem contorno e à vista entre a boca e as
  penas.

As fontes em camadas estão em `fontes/aljava/aljava-40/48.aseprite`, pintadas pelo `pintar.lua` no editor. O composto
do editor e os PNGs exportados são iguais às grades.

**Conferido a 1920×945** (`agilidade_aljava_ref/aljava-40-48.png`), sem erros:
- o 40 no Inventário;
- o 48 no cartão compacto do saque, ao lado do 64.

`fotografar.mjs aljava_ref` ganhou o Inventário e o saque.

### Integradas: Agilidade (1.121.0) e aljava (1.122.0)

Jean aprovou as duas sem novos retoques.

**As fontes finais** saíram de `agilidade_aljava_ref/fontes/` para `ferramentas/arte/aseprite/attr-agilidade/` e
`aljava/`, e o exportador as reproduz (`exportar_aseprite.py <peça> --conferir`). O que ficou aqui é o histórico do
processo: as grades, as listas, os auxiliares, as prévias e as propostas.

**Conferido:** os dezesseis arquivos do jogo são idênticos, byte a byte, aos aprovados (`e9b0499`, `ea3835f` e
`fb403f5`).

## Poder, rodada 2 (`poder_r2/`)

**O pedido:** o candidato `35262ca` ficou estreito e rígido, e as divisões verticais lembravam cristal. A direção pedida
é uma chama de energia com a base encorpada e luminosa, o miolo claro cercado de violetas cada vez mais escuros e as
línguas assimétricas, de recortes curvos.

**Como foi feito:**
- **O desenho na grade:** o 24 primeiro, tom a tom (`auxiliares/mao24.py`). O 32 repete a mesma silhueta na grade
  dele, com os tons pela mesma lógica e retoques à mão (`auxiliares/mao32.py`).
- **As grades:** em `grades/`. O `../agilidade_aljava_ref/grades.py --pasta=poder_r2` grava as listas das camadas.
- **No Aseprite, pelo MCP:** as camadas pintadas pelo `pintar.lua`, sem diferença na releitura, e salvas em
  `fontes/attr-poder/`. O composto do editor e a captura dele batem com as grades.
- **A exportação:** `exportar_aseprite.py attr-poder poder_r2/proposta --fontes=poder_r2/fontes`. O 64 é o 32 ampliado
  2×.

**A chama:**
- **A forma:** uma gota de base larga e redonda. A língua principal sobe, se estreita e curva a ponta para a direita.
  A língua da direita, menor, abre para fora, e à esquerda há uma lambida curta colada ao corpo e uma faísca solta.
- **A luz, sem desfoque:** o miolo creme (`FFF4DC`) fica baixo, onde a chama é mais quente. Em volta, os anéis seguem o
  rosa-lilás, o magenta e o violeta até o índigo da beira, e a luz do miolo sobe pelo eixo da língua principal. O lado
  de trás fica um tom abaixo, e a base termina em índigo escuro.
- **As camadas:** chama (os violetas da beira), miolo (os claros), faisca, contorno.

**Conferido a 1920×945**, com os mesmos dados (`poder_r2/poder-atual-x-anterior-x-nova.png`), sem erros: o atual, o
candidato anterior e a nova proposta na ficha, com os quatro atributos (Ataque, Defesa e Agilidade já os do jogo), e
no selo. O tamanho real sobre o carvão está em `poder_r2/prancha-carvao.png`.

**O que pode ser pior:** sem o halo suave do placeholder, a chama ocupa um pouco menos o selo. No 24, a lambida da
esquerda é só um degrau da silhueta.

Nada disto entrou no jogo.

### Integrado: Poder (1.123.0)

Jean aprovou a rodada 2 (`c0dbab8`). As fontes saíram de `poder_r2/fontes/` para `ferramentas/arte/aseprite/attr-poder/`,
e os seis arquivos do jogo são idênticos, byte a byte, aos aprovados. O que ficou em `poder_r2/` é o histórico do
processo. Com o Poder, os quatro atributos estão concluídos.

## Ataque e Defesa, rodada 2 (`ataque_defesa_r2/`)

**O pedido:** uma exploração nova, sobretudo da espada (a silhueta, a proporção entre lâmina, guarda e empunhadura, os
planos de luz do aço e a presença no tamanho pequeno), e um escudo com volume, espessura e leitura imediata. Os
atuais (1.120.0) continuam no jogo.

**Como foi feito:**
- **O desenho na grade:** o 24 primeiro, avaliado a cada passo em tamanho real ao lado dos atuais; o 32 com a mesma
  construção (`auxiliares/`: `e24c.py`, `e32.py`, `d24.py`, `d32.py`).
- **As camadas no Aseprite, pelo MCP:** pintadas pelo `pintar.lua`, sem diferença na releitura, e salvas em `fontes/`.
  O composto do editor e a exportação (`exportar_aseprite.py <peça> ... --fontes=ataque_defesa_r2/fontes`) são iguais
  às grades; o 64 é o 32 ampliado 2×.

**A espada** (camadas: lamina, guarda, cabo, pomo, contorno):
- **A construção:** a 45°, nas diagonais da grade (`x+y` constante é uma linha de pixels paralela à lâmina). Cada plano
  do aço é uma linha inteira, sem degrau solto: o bisel aceso, o plano claro com o brilho, o sulco escuro até dois
  terços da lâmina, o plano escuro e o bisel escuro.
- **As proporções:** a lâmina é mais longa que a atual e afina em ponta aguda. A guarda é mais curta, com o miolo
  engrossado e as pontas viradas para a lâmina, e o cabo de couro tem as voltas à vista. O pomo é redondo.
- **As tentativas:** a primeira, de 4 linhas, ficou fina e fraca; a segunda tinha a ponta quadrada e a guarda longa.

**O escudo** (camadas: face, aro, lado, bossa, contorno):
- **A forma:** um escudo de cavaleiro um pouco virado. A espessura aparece à direita como uma faixa de latão escuro,
  com a beira acesa.
- **A face:** aço convexo, com a luz numa faixa que segue o contorno, o brilho só no alto e o escuro para a direita e
  para a ponta.
- **O aro e a bossa:** o aro de latão tem 1 px, e a bossa em domo é acesa em cima, com a sombra no aço.
- **A tentativa:** a primeira, por regras, ficou quadrada, com o aro grudado na espessura e a face listrada.

**Conferido a 1920×945**, com os mesmos dados (`ataque_defesa_r2/ataque-defesa-atual-x-nova.png`), sem erros:
- **Os quatro atributos juntos:** na ficha e no Inventário.
- **Os selos:** de Ataque e de Defesa.
- **O tamanho real sobre o carvão:** em `ataque_defesa_r2/prancha-carvao.png`.

**O que pode ser pior:**
- No 24, a espada nova é mais esbelta: pesa menos que a atual, embora leia melhor como espada.
- O escudo virado ocupa menos largura que o atual.

Nada disto entrou no jogo.

**Decisão de Jean:** os Ataque e Defesa do jogo (1.120.0) ficam. A rodada 2 acima é uma alternativa guardada, não
escolhida. Os quatro atributos estão concluídos.

## A doca, rodada 2: Inventário e Mapa (`doca_r2/`)

**O pedido:** dois atalhos por vez, começando pelo Inventário e pelo Mapa. A primeira proposta (`doca/`) foi recusada:
a mochila parecia uma maleta, e o mapa, um tríptico chapado.

**Os tamanhos:** a doca usa o 36 (`Icones.atalho`, o `--s` da imagem); o 32 é para janelas estreitas. O 36 foi feito
primeiro, e o 32 tem a mesma construção.

**Como foi feito:**
- **O desenho na grade:** os auxiliares estão em `doca_r2/auxiliares/`. A mochila foi pintada à mão região por região
  (`m36h.py`, `m32h.py`), depois de um rascunho por regras que virava um saco sem construção. O mapa tem os painéis por
  geometria e o percurso, o X e o terreno à mão (`mapa.py`, `mapa32.py`).
- **As cores e as camadas:** como as cores do couro se repetem entre as partes, a camada de cada pixel vem de um
  segundo mapa (`grades/<peça>-<lado>-camadas.txt`, feito por `auxiliares/camadas.py`). O `grades.py` ganhou essa
  leitura, e as peças antigas dão as mesmas listas.
- **No Aseprite, pelo MCP:** as camadas pintadas pelo `pintar.lua`, sem diferença na releitura, e salvas em
  `doca_r2/fontes/`. O composto do editor e a exportação (`exportar_aseprite.py <peça> doca_r2/proposta
  --fontes=doca_r2/fontes`) são iguais às grades.

**A mochila** (camadas: rolo, bolsos, corpo, aba, cinta, fivela, contorno), no couro do conjunto aprovado:
- **A forma:** é mais alta que larga, com os ombros redondos e o fundo cheio.
- **A aba:** a dobra de cima é acesa, e a borda de baixo, em U, é escura e faz sombra no corpo.
- **O fechamento:** a cinta do meio passa por uma fivela de latão vazada, com o pino.
- **Os bolsos:** dos lados, bojudos, com a abinha acesa e a costura junto do corpo. As costuras dos painéis do corpo
  dão o volume.
- **O cobertor:** verde-oliva, enrolado em cima, preso por duas tiras de couro e com as pontas em espiral. É o que dá
  silhueta e cara de viajante.

**O mapa** (camadas: espessura, papel, vincos, terreno, percurso, destino, contorno):
- **A forma:** dobrado em sanfona, em três painéis inclinados. O de cima e o de baixo sobem e descem juntos (o
  zigue-zague), alternando a luz: os painéis que sobem para a direita estão acesos, e o do meio, na sombra.
- **O volume:** os vincos (a dobra de dentro escura, a de fora acesa) e a espessura do papel embaixo.
- **O que diz "mapa", sem símbolos miúdos:**
  - o percurso tracejado em vermelho, com 2 px (o traço e a sombra), subindo até um X de 5×5;
  - duas manchas grandes de terreno: um bosque verde e um lago azul.
- **A diferença do Diário e do Grimório:** é papel dobrado, sem lombada nem capa.

**Conferido a 1920×945**, sem erros:
- **A doca inteira:** atual × proposta (`doca_r2/doca-atual-x-proposta-1920x945.png`).
- **Os recortes do Inventário e do Mapa** (`doca_r2/inventario-mapa-recortes.png`): em tamanho real e ampliados 3×,
  normais e com a tela aberta.
- **O estado selecionado:** com o Inventário aberto, aparece o sublinhado de latão. Com o Mapa aberto, a tela do mapa
  escurece a página inteira, doca junto, no atual e na proposta.
- O `fotografar.mjs` ganhou a peça `doca_r2` e as fotos `doca-inventario` e `doca-mapa`.

**O que pode ser pior:**
- A mochila em couro claro destaca menos que o placeholder avermelhado.
- O mapa dobrado é mais alto e mais estreito que o atual.

Nada disto entrou no jogo, e os outros seis atalhos não foram começados.

### Integrados: Inventário e Mapa (1.124.0)

Jean aprovou os dois sem retoque (`c02e566`). As fontes saíram de `doca_r2/fontes/` para
`ferramentas/arte/aseprite/atalho-inventario/` e `atalho-mapa/`, e os oito arquivos do jogo são idênticos, byte a
byte, aos aprovados. O que ficou em `doca_r2/` é o histórico do processo. Os outros seis atalhos ficam para os
próximos pares.

## A doca, rodada 3: Grimório e Diário (`doca_r3/`)

**O pedido:** o próximo par, só no protótipo, com o Inventário e o Mapa integrados como referência de acabamento.

**Os tamanhos de fato usados:**
- a doca usa o 36 (o 32 nas janelas estreitas);
- o Grimório é também o comando Habilidades da roda da luta (`ACAO.grimorio`, `Icones.acao`, 32).

Nenhum outro tamanho foi feito. Os mapeamentos não mudaram.

**Como foi feito:** o 36 primeiro, conferido em tamanho real a cada passo, e o 32 com a mesma construção
(`doca_r3/auxiliares/`).
- **As camadas:** cada pixel guarda a seção do desenho que o pintou (`rotulos.py`), e isso gera o mapa de camadas.
- **No Aseprite, pelo MCP:** as camadas pintadas pelo `pintar.lua`, sem diferença na releitura, e salvas em
  `doca_r3/fontes/`. O composto do editor e a exportação são iguais às grades.

**O Grimório** (camadas: contracapa, paginas, lombada, capa, cantoneiras, fecho, gema, contorno): o livro fechado em
pé, um pouco virado. Os materiais vêm do grimório do equipamento: o couro violeta, o latão e as folhas creme.
- **A lombada:** redonda, com três nervuras e o sulco da dobradiça.
- **A capa:** acesa em cima à esquerda, com a moldura em relevo e as cantoneiras de latão.
- **O volume:** o bloco de páginas à vista à direita, e a contracapa na espessura.
- **O fecho:** uma tira de couro com a fivela de latão.
- **O elemento mágico:** uma gema violeta luminosa num engaste em losango.
- **A tentativa:** na primeira, a lombada se confundia com a capa.

**O Diário** (camadas: capa, paginas, anotacoes, fita, pena, contorno): o livro aberto, largo e baixo, visto um pouco
de cima.
- **As páginas:** em arco, altas no meio de cada página e fundas na dobra, que escurece em 2 px de cada lado. As
  camadas das folhas aparecem nas beiras.
- **A capa e as anotações:** a capa de couro marrom fica à vista embaixo e nos lados. As anotações são poucas linhas de
  tinta clara, de tamanhos diferentes, acompanhando a curva.
- **A fita:** vermelha, saindo da dobra.
- **A pena:** a pluma é afunilada e recortada, num branco frio contra o papel creme, com a sombra dela na página.
- **As tentativas:**
  - a dobra era uma faixa larga, e a escrita, uma tabela;
  - a pena, uma lâmina cinza; depois, branca sobre branco.
- **A diferença do Grimório:** a silhueta (deitado e aberto × em pé e fechado), a composição (pena e fita × gema e
  fecho) e a cor (couro marrom e papel × couro violeta).

**Conferido a 1920×945**, sem erros (`fotografar.mjs doca_r3` e `doca_r3_luta`):
- **A doca inteira:** atual × proposta (`doca_r3/doca-atual-x-proposta-1920x945.png`).
- **Os recortes** em tamanho real e ampliados 3× (`doca_r3/grimorio-diario-recortes.png`), normais e com cada tela
  aberta. Com o Diário aberto, aparece o sublinhado de latão. Com o Grimório aberto, a doca não marca o atalho, no
  atual e na proposta.
- **O Habilidades na roda da luta** (`doca_r3/habilidades-luta.png`).

**O que pode ser pior:**
- O Grimório no couro violeta-avermelhado do equipamento tem menos contraste com o fundo escuro da doca que o atual,
  azulado.
- O Diário é mais largo que o atual.

Nada disto entrou no jogo.

### Integrado: o Diário (1.125.0)

Jean aprovou o Diário sem retoque (`666b806`). As fontes saíram de `doca_r3/fontes/` para
`ferramentas/arte/aseprite/atalho-diario/`, e os quatro arquivos do jogo são idênticos, byte a byte, aos aprovados. O
Grimório continua no protótipo, em refinamento.

### O Grimório, rodada 2 (`doca_r3/`)

**O pedido:**
- a perspectiva não convencia: a capa quase de frente, a lombada à esquerda e as folhas à direita, que só se veriam
  olhando pelo outro lado;
- o emblema estava grande e deslocado, com o fecho apertado contra ele;
- faltavam poucos planos de luz na capa.

**O candidato anterior** está guardado em `doca_r3/grimorio_r1/`: os PNGs, as fontes e as grades.

**A construção** (`auxiliares/gb36.py`, `gb32.py`):
- **Um objeto só, visto de cima e da esquerda:** a profundidade vai para cima e para a esquerda (5 a 6 px). Ficam à
  vista três faces:
  - a capa da frente;
  - a lombada, que é a face da esquerda, redonda, com as três nervuras inclinadas como a profundidade;
  - a borda de cima das folhas, entre a beira acesa da capa da frente e a da contracapa.
- **A lateral direita:** some, porque daqui não se vê.
- **Os volumes primeiro:** a etapa `volumes` do script grava só eles.
- **As ferragens depois:** a moldura em relevo e as cantoneiras.
- **O emblema e o fecho:**
  - o emblema ficou menor (o losango de 7 px) e centrado no plano útil da capa, entre a moldura do lado da lombada e o
    fecho, com folga dos dois lados;
  - a tira sai de trás da beira da direita (1 px por fora, na sombra), deita sobre a capa e termina na placa de latão
    com o pino.
- **A luz da capa:** três planos: o alto e o lado da lombada mais claros, o meio e a beira oposta na sombra. A quina
  junto da lombada é acesa.

**Os arquivos:** o 36 e o 32 com a mesma construção, as camadas pintadas pelo `pintar.lua` no editor e o composto e a
exportação iguais às grades.

**Conferido a 1920×945** (`doca_r3/grimorio-antes-x-depois.png`), sem erros: antes × depois em tamanho real, na doca
(36) e no Habilidades da luta (32), e ampliados 4×.

**O que pode ser pior:**
- No tamanho real, o emblema menor vira mais um ponto de luz que um desenho.
- A lombada larga deixa o livro mais pesado à esquerda.

### O Grimório, rodada 3: recomeçado pela referência (`doca_r3/`)

**O pedido:** recomeçar a geometria. A rodada 2 parecia um bloco com tampa.
- **As referências:** a principal, de construção, é um livro marrom inclinado com o símbolo laranja e a fita. A prancha
  com o livro de olhos e o estrelado serve de acabamento. Os dois livros violeta citados como referência de identidade
  e de simplificação não vieram anexados.
- **O que fica guardado:** a rodada 1 em `doca_r3/grimorio_r1/`, e a 2 em `doca_r3/grimorio_r2/` (com os scripts dela).

**A construção** (`auxiliares/grimorio_livro.py <36|32> [construcao]`): o livro é um objeto 3D simples numa projeção
só, a da referência.
- **O ângulo:** o livro está girado (a borda de cima sobe para a direita), e a profundidade vai para baixo e para a
  esquerda.
- **As faces à vista:**
  - a capa da frente;
  - a lombada redonda à esquerda, unindo as duas capas;
  - o bloco de folhas embaixo, recuado das beiras das capas;
  - a espessura das duas capas finas e a contracapa por trás das folhas.
- **Como se desenha:** cada pixel vem da face mais à frente naquele ponto, com amostragem de 4×4. A etapa
  `construcao` grava só os volumes, sem enfeite.
- **A decoração:** desenhada no espaço do livro, para seguir a mesma perspectiva:
  - duas nervuras na lombada e a moldura em baixo relevo;
  - o emblema, uma estrela de quatro pontas de latão luminoso com halo no couro, centrado no plano útil da capa;
  - quatro cravos;
  - a fita saindo das folhas.
  - Não tem fecho, para não disputar espaço com o emblema.
- **A luz:** poucos planos: o alto e o lado da lombada mais claros, a beira oposta escura e a quina junto do sulco
  acesa.
- **Os tamanhos:** o 36 e o 32 saem do mesmo modelo, na mesma projeção.

**As camadas:** contracapa, folhas, lombada, capa, emblema, cravos, fita, contorno. Foram pintadas pelo `pintar.lua`
no editor, e o composto e a exportação são iguais às grades.

**Conferido a 1920×945**, com os mesmos dados (`doca_r3/grimorio-producao-r2-r3.png`), sem erros: a produção, a
rodada 2 e a rodada 3, na doca (36) e no Habilidades da luta (32), em tamanho real e ampliados.

**O que pode ser pior:**
- O livro inclinado ocupa o quadro na diagonal e fica um pouco menor que o atual.
- No 32, o halo do emblema é só um pequeno disco mais claro.

### Integrado: o Grimório (1.126.0)

Jean aprovou a rodada 3 sem retoque (`61dcb81`). As fontes saíram de `doca_r3/fontes/` para
`ferramentas/arte/aseprite/atalho-grimorio/`, e os quatro arquivos do jogo são idênticos, byte a byte, aos aprovados.
Vale para o atalho da doca e para o comando Habilidades da luta. As rodadas 1 e 2 ficam em `doca_r3/grimorio_r1/` e
`grimorio_r2/`.

## A doca, rodada 4: Talentos e Comitiva (`doca_r4/`)

**O pedido:** o próximo par. A Comitiva não estava na contagem dos oito atalhos.
- **Os usos e os tamanhos:** a doca usa o 36 (o 32 nas janelas estreitas).
- **A Comitiva:** só aparece quando há companheiro (`SISTEMA` em `app/nucleo.js`). Ela não tem papel em `Icones`: cai no
  sprite 16×16 `humano`, que é também personagem e inimigo. O desenho novo é um arquivo próprio, `atalho-comitiva`, e o
  `humano` não muda.
- **O selo de pontos:** cobre o alto à esquerda do ícone dos Talentos (`.atalho .selo`).
- **Na proposta:** o papel da Comitiva (`TAMANHOS` e `ATALHO`) entra só na página do protótipo (`papel_atalho` em
  `fotografar.mjs`). O jogo não muda.

**A Comitiva** (`auxiliares/comitiva.py`; camadas: tras_esquerda, tras_direita, frente, contorno):
- **A composição:** três viajantes, um à frente e dois um pouco atrás.
- **Os viajantes:**
  - o da frente: capuz e manto verde, com o broche de latão;
  - o de trás à esquerda: chapéu de copa alta e aba larga, com o casaco de couro;
  - o de trás à direita: ombreiras de metal e a capa vermelho-escura.
- **O desenho:** os rostos são simples, com dois olhos, e cada figura tem o contorno próprio. O da frente separa as de
  trás.
- **As tentativas:**
  - a primeira tinha uma faixa escura no rosto, que lembrava a máscara de um bandido, e corpos sem ombros, como peças
    de xadrez;
  - a segunda tinha um cajado, que cortava o rosto do viajante de chapéu.

**Os Talentos** (`auxiliares/talentos.py`; camadas: galhos, nos, contorno):
- **A forma:** uma árvore de latão. O tronco é grosso embaixo e sobe com uma leve curva, e os dois galhos curvos saem
  em alturas diferentes (os caminhos).
- **A luz:** a beira virada para cima e para a esquerda acesa.
- **Os nós:** medalhões. Os conquistados (a raiz, o alto e o da direita) têm uma gema verde-água acesa; o não
  escolhido (à esquerda, onde o selo cobre) fica com o encaixe vazio.
- **As tentativas:**
  - a primeira, com galhos retos e simétricos, parecia um candelabro, e os nós acesos se confundiam com o latão;
  - a segunda, simétrica, parecia um tridente.

**As fontes:** em camadas, pintadas pelo `pintar.lua` no editor. O composto e a exportação são iguais às grades. O
`grades.py` aceita o contorno desenhado na grade (a Comitiva tem contornos por dentro, entre as figuras).

**Conferido a 1920×945** (`doca_r4/doca-atual-x-proposta-1920x945.png` e `doca_r4/talentos-comitiva-recortes.png`), sem
erros:
- **A doca completa:** no tutorial, com companheiro e pontos de talento (o selo ★ sobre os Talentos).
- **Os recortes**, em tamanho real e ampliados 3×, na fogueira:
  - sem pontos;
  - com a Comitiva aberta (o sublinhado de latão);
  - com os Talentos abertos (a tela da árvore escurece a página, no atual e na proposta).

**O que pode ser pior:**
- No 32, os rostos das figuras de trás ficam com 2 a 3 px.
- Com o selo de pontos, a árvore perde o nó vazio, mas mantém o tronco, os galhos e os nós acesos.

Nada disto entrou no jogo.

### Integrados: os Talentos e a Comitiva (1.127.0)

Jean aprovou os dois sem retoque (`4deb386`).
- **As fontes:** saíram de `doca_r4/fontes/` para `ferramentas/arte/aseprite/atalho-talentos/` e `atalho-comitiva/`.
- **Os arquivos:** os oito do jogo são idênticos, byte a byte, aos aprovados.
- **A Comitiva:** ganhou papel próprio em `Icones`. O `papel_atalho` do `fotografar.mjs` fica para outras propostas.

## A doca, rodada 5: Bestiário, Salvar e Sair (`doca_r5/`)

**O pedido:** os três últimos atalhos, um de cada vez, só no protótipo. Os três só servem à doca (`ATALHO`), no 36 e no
32.

**O Bestiário** (`auxiliares/bestiario.py`; camadas: chifres, cranio, contorno): o crânio de uma criatura, de frente.
- **O que o faz criatura:** os chifres grossos em C, com anéis e a luz na beira, e as órbitas inclinadas (o canto de
  fora sobe), fundas e separadas pela ponte do nariz, com o sobrolho aceso.
- **O volume do osso:** as têmporas afundadas e as maçãs largas, o focinho afinando, a cavidade do nariz em V invertido
  e o osso marfim em poucos planos.
- **A boca, depois do retorno do Jean** (a parte de baixo, com uma referência da internet): a arcada de cima e a de
  baixo, com os dentes na grade do tamanho (dente de 2 px, fenda de 1), a linha escura da boca e o queixo arredondado,
  um degrau para dentro das maçãs.
- **A primeira versão:** uma barra fina com duas presas soltas, guardada em `doca_r5/bestiario_r1/`.

**O Salvar** (`auxiliares/salvar.py`; camadas: tampa, corpo, latao, seta, contorno): o baú aberto, inteiro à vista.
- **O baú:** a tampa para trás, com as tábuas de dentro e a beira de latão; a boca escura com a borda acesa; a frente de
  madeira com as cintas e a fechadura.
- **A seta:** de aço, descendo para dentro da boca. Ela é contida, para não esconder o baú, e fria, para se separar da
  madeira, do latão e do Sair.
- **A tentativa:** a tampa inclinada parecia um telhado, e a boca tinha só 1 px.

**O Sair** (`auxiliares/sair.py`; camadas: arco, passagem, seta, contorno): o arco de pedra de uma passagem.
- **O arco:** as pedras em aduelas e fiadas, acesas em cima à esquerda.
- **A profundidade do vão:** o fundo escuro e o chão de pedra, com a parede de dentro à direita, clara junto da face e
  separada por uma junta escura.
- **A seta:** laranja, saindo para a direita com contorno próprio.
- **A diferença do Salvar:** a silhueta (arco em pé, contra baú largo), a direção da seta (para fora, contra para
  dentro) e a cor (quente, contra fria).

**As fontes:** em camadas, pintadas pelo `pintar.lua` no editor. O composto e a exportação são iguais às grades.

**Conferido:**
- **Sobre o carvão:** o tamanho real, ao lado dos atuais e dos aprovados (`doca_r5/prancha-carvao.png`).
- **Na doca, a 1920×945, sem erros:** atual × proposta (`doca_r5/doca-atual-x-proposta-1920x945.png`) e os recortes em
  tamanho real e 3× (`doca_r5/bestiario-salvar-sair-recortes.png`).
- **O Salvar e o Sair:** não foram clicados (não mudam na foto).

**O que pode ser pior:**
- O crânio é mais frontal e simétrico que o placeholder.
- A seta do Salvar ocupa o alto do baú e cobre o meio da tampa.

Nada disto entrou no jogo.

### O Bestiário, rodada 3: a parte de baixo, no Aseprite

**O pedido de Jean:** com uma referência de crânio de fera, refazer a parte de baixo. Os dentes em poucos grupos claros,
separados por sombra e presos ao maxilar; a silhueta alongada; sem a base virar uma barra horizontal com duas pontas.
Ele também pediu que o trabalho fosse no Aseprite.

**Como foi feito**, só nas linhas de baixo (do nariz para baixo):
- **No editor, pelo MCP:**
  - a fonte em camadas (`doca_r5/fontes/atalho-bestiario/`) foi aberta no editor;
  - as linhas de baixo das camadas `cranio` e `contorno` foram apagadas e repintadas pelo `pintar.lua` (operações em
    Lua, com o alpha 00 para apagar);
  - a captura do editor foi conferida a cada tamanho, e as fontes foram salvas.
- **O desenho:** as linhas foram desenhadas à mão, uma por uma (`auxiliares/bestiario_boca36.py` e `bestiario_boca32.py`).
  Um cálculo auxiliar as converte nas listas (`bestiario_boca_listas.py`).
- **A fonte final:** é o `.aseprite`. As grades de `doca_r5/grades/` ficam com a rodada 2 do Bestiário.

**A construção:**
- **O focinho:** longo, afinando até a arcada, com a cavidade do nariz maior (6 px) e a lâmina de osso no meio.
- **A arcada:** a linha da gengiva na sombra.
- **Os dentes:** em quatro grupos pendurados nela: uma presa longa em cada canto, curvando para dentro, e dois dentes
  curtos no meio. As fendas entre eles são de sombra marrom presa ao osso, e o contorno só aparece abaixo.
- **O resto do crânio:** não mudou.

**As rodadas guardadas:** a 1 (a barra com duas presas) em `doca_r5/bestiario_r1/`, e a 2 (as duas fileiras de dentes
com o queixo) em `doca_r5/bestiario_r2/`. A comparação das três está em `doca_r5/bestiario-rodadas.png`.

**Conferido:** o composto do editor, os PNGs exportados e os @2x são iguais. As fotos da doca a 1920×945 foram refeitas.

### O Bestiário, rodada 4: a ligação entre o focinho e a arcada (no Aseprite)

**O pedido de Jean:** a rodada 3 está boa; refinar só a passagem dos planos largos do focinho para as faixas
verticais dos dentes, que começavam todas na mesma altura e marcavam uma linha de encaixe.

**O retoque:** feito direto nas fontes finais (`doca_r5/fontes/atalho-bestiario/`), só na camada `cranio`, pelo
`pintar.lua`, com as linhas desenhadas à mão (`auxiliares/bestiario_ligacao.py`). As grades antigas não foram usadas.
- **A luz:** os planos do focinho continuam até a raiz dos dentes. O lado da luz segue claro nos dentes da esquerda, e
  a sombra da direita desce para os dentes da direita.
- **As fendas:** a do meio começa uma linha mais acima (a gengiva) e as dos lados uma linha abaixo, o que quebra o
  alinhamento horizontal. As fendas continuam inteiras, sem pixel solto.
- **Nos dois tamanhos:** a mesma regra em cada grade, nas linhas 28 a 31 do 36 e 23 a 26 do 32.
- **O que não mudou:** 14 pixels no 36 e 12 no 32 mudaram de tom, e nenhum de transparência. A silhueta e o resto do
  crânio estão iguais.

**A rodada 3:** guardada em `doca_r5/bestiario_r3/` (os PNGs e as fontes).

**Conferido:** os PNGs exportados e os @2x batem com o editor. Antes × depois na doca a 1920×945, em tamanho real e
4× (`doca_r5/bestiario-ligacao-antes-x-depois.png`). O Salvar e o Sair seguem como apresentados.

### Integrado: o Bestiário (1.128.0)

Jean aprovou a rodada 4 sem retoque (`e373618`). As fontes finais editadas saíram de `doca_r5/fontes/` para
`ferramentas/arte/aseprite/atalho-bestiario/`, e os quatro arquivos do jogo são idênticos, byte a byte, aos aprovados. O
Salvar e o Sair continuam no protótipo.

### Integrados: o Salvar e o Sair (1.129.0); a doca concluída

Jean aprovou os dois sem retoque (`a872915`, reapresentados no `682b189`).
- **As fontes:** saíram de `doca_r5/fontes/` para `ferramentas/arte/aseprite/atalho-salvar/` e `atalho-sair/`.
- **Os arquivos:** os oito do jogo são idênticos, byte a byte, aos aprovados.
- **A doca:** os nove atalhos estão em pixel art.

## Vida e recursos: Vida e Mana (`vida_mana/`)

A primeira dupla do grupo Vida e recursos (etapa 1D). **Proposta, nada no jogo:** só as imagens dos dois ícones; as
barras, os preenchimentos, os números, as cores funcionais, as regras e as animações ficam como estão.

- **Os usos:** só o topo (`app/paineis.js`, `Icones.vital`), em 20 px; o `TAMANHOS` registra só o 20, e nenhum outro
  lugar pede outro tamanho. Desenhados direto na grade de 20, sem reduzir de um maior.
- **A Vida, o coração:** silhueta de coração cheia, com os dois lobos e a ponta; o vermelho da vida em quatro faixas
  de tom (luz de cima e da esquerda, a volta de baixo e da direita mais funda), o brilho no lobo da esquerda e um
  reflexo pequeno no da direita; o contorno comum.
- **A Mana, a gota:** uma gota de energia líquida, com a ponta curvando um pouco e o fundo redondo, no azul da barra
  de mana (`#a8c4ff`, `#4d74e0`, `#1c2a6b` na rampa), o miolo aceso e o reflexo em crescente do lado da luz; sem halo
  em volta. Ela se separa do raio do Vigor (dourado), da estrela do Foco e da chama do Poder (violeta) pela forma e
  pela cor, e do cristal facetado atual por ser líquida.
- **As fontes:** `vida_mana/fontes/vital-vida/vital-vida-20.aseprite` (camadas coracao, brilho, contorno) e
  `vital-mana/vital-mana-20.aseprite` (gota, brilho, contorno).
- **As operações:**
  - *cálculos fora do editor:* as grades e as listas por camada em `vida_mana/auxiliares/vida.py` e `mana.py` (o tom
    por regra e os brilhos à mão; gravam as listas `.lua` e a prévia na pasta em que rodam);
  - *Lua pelo `execute_script`:* o documento de 20×20 com as camadas e a pintura pelo `pintar.lua`
    (`pintar_arquivo`, cada pixel relido; 0 diferentes, 0 fora da tela), e o `saveAs`;
  - *ferramentas do conector:* a captura do editor e a lista de documentos abertos.
- **A exportação:** `python ferramentas/arte/exportar_aseprite.py vital-vida|vital-mana
  ferramentas/prototipos/hud/itens-lote-noite/vida_mana/proposta --fontes=ferramentas/prototipos/hud/itens-lote-noite/vida_mana/fontes`;
  o composto exportado é igual, pixel a pixel, ao que as listas pediam, e o @2x é a duplicação exata.
- **As fotos (1920×945):** `node ferramentas/prototipos/hud/itens-lote-noite/fotografar.mjs vida_mana` (uma partida
  de Mago na capela, que mostra a Vida e a Mana; a proposta troca só os dois arquivos pela página).
  `vida_mana/vida-mana-topo.png` junta o topo atual e o proposto em tamanho real e a ampliação 8× sobre o fundo real;
  as capturas ficam em `vida_mana/capturas/`.

### Vida aprovada; a Mana, rodada 2: sem o miolo aceso

O Jean aprovou o coração como está em `a914f18` (sem alterações). Na gota, pediu para tirar só o bloco quadrado de luz
do centro: o reflexo em crescente já diz o brilho. Vida e Mana continuam no protótipo e entram juntas depois da
conferência da gota.

- **O que mudou:** só os 16 pixels do bloco (4×4, de x 8 a 11 e y 11 a 14), na camada gota, agora no 4 e no 3 da rampa
  que continuam a diagonal do azul em volta. O reflexo, a sombra de baixo, a silhueta, o contorno e os outros pixels
  ficam iguais.
- **Como:** em `auxiliares/mana.py`, o tom do corpo perdeu o miolo; a diferença contra a rodada 1 (exatamente o bloco)
  foi pintada pelo `pintar.lua` na fonte em camadas (16 escritos, 0 diferentes na releitura, 0 fora da tela) e salva.
  O PNG exportado é igual à captura do editor e às listas, e o @2x é a duplicação exata. O coração exportado continua
  idêntico, byte a byte, ao de `a914f18`.
- **A rodada 1 guardada:** `vida_mana/mana_r1/` (a fonte, os PNGs e o auxiliar).
- **As fotos:** `ROTULO=gota-r2 SO_PROPOSTA=1 JANELAS=1920x945 node .../fotografar.mjs vida_mana` (o mesmo roteiro e a
  mesma partida de Mago; os dois topos só diferem no bloco 4×4). `vida_mana/mana-r2-antes-depois.png` mostra o antes
  e o depois em tamanho real e a ampliação 8× sobre o fundo real.

### Integradas: a Vida e a Mana (1.130.0)

O coração de `a914f18` e a gota de `f02566d`, sem retoque. As fontes foram para `ferramentas/arte/aseprite/vital-vida/`
e `vital-mana/`; os quatro arquivos do jogo (20 e @2x) são idênticos, byte a byte, aos aprovados, e o exportador os
reproduz (`--conferir`). Os papéis em `Icones` (`VITAL`) não mudaram; o único uso é o topo.
