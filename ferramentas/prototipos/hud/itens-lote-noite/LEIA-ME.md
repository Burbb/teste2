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
