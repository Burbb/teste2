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

### O Sair alinhado (1.130.1)

O desenho não mudou: o ícone anda 4 px para a direita na doca (CSS), para a porta ficar sobre a palavra; a seta sai
para a direita sem tirar a porta do centro. `doca_r5/sair-alinhado.png`: a doca antes e depois em tamanho real e a
ampliação 4×.

## Vida e recursos: Vigor e Foco (`vigor_foco/`)

**Proposta, nada no jogo:** só as imagens dos dois ícones do topo (20, o único uso: `Icones.vital`); barras,
números, cores funcionais, regras e animações ficam como estão. O custo das habilidades usa outros sprites (`chama`,
`olho`), num papel separado, e não muda.

- **O Vigor, o punho em chamas:** pela ideia da referência do Jean (a chama e o punho cerrado, sem o coração) e pelas
  referências de punho dele. O punho de frente, com os quatro dedos separados por linhas, os nós em alturas
  diferentes, o polegar atravessado e o antebraço abrindo para baixo, num dourado de pele que conversa com o vigor;
  três línguas de fogo saindo dos nós, laranja e mais quentes junto da mão. A chama só em cima: as rodadas em que ela
  envolvia o punho liam como um rosto com cabelo e foram descartadas antes da entrega.
- **O Foco, o alvo:** a concentração (os anéis concêntricos) e a precisão (as quatro marcas curtas da mira), no
  **verde** da barra de foco (`#b8f0a0`, `#62b86e`, `#1f4a25`). A estrela atual é violeta, a cor do Poder; o alvo
  devolve a cor funcional do Foco e tem silhueta redonda, diferente da estrela, da chama, da gota, do coração e do
  punho.
- **As recusadas, guardadas:** o raio com volume (a primeira proposta do Vigor, antes da ideia do Jean) em
  `vigor_foco/recusados/vigor-raio/` (fonte, PNG e auxiliar) e a mira de anel fino em `recusados/foco-mira/` (o
  contorno entupia os vãos de dentro, e a silhueta lembrava a estrela).
- **As fontes:** `vigor_foco/fontes/vital-vigor/vital-vigor-20.aseprite` (camadas chama, punho, contorno) e
  `vital-foco/vital-foco-20.aseprite` (anel, marcas, centro, contorno).
- **As operações:**
  - *cálculos fora do editor:* `vigor_foco/auxiliares/vigor.py` (o punho à mão, pixel a pixel, e a chama por regra) e
    `foco.py` (os anéis e as marcas por regra); gravam as listas `.lua` e a prévia na pasta em que rodam;
  - *Lua pelo `execute_script`:* o documento de 20×20 com as camadas, a pintura pelo `pintar.lua` (cada pixel relido;
    0 diferentes, 0 fora da tela) e o `saveAs`, um ícone por vez;
  - *ferramentas do conector:* a captura do editor.
- **A exportação:** `python ferramentas/arte/exportar_aseprite.py vital-vigor|vital-foco
  ferramentas/prototipos/hud/itens-lote-noite/vigor_foco/proposta --fontes=ferramentas/prototipos/hud/itens-lote-noite/vigor_foco/fontes`;
  o composto é igual à captura do editor e às listas, e o @2x é a duplicação exata.
- **As fotos (1920×945):** `fotografar.mjs vigor_foco` (Guerreiro, o Vigor) e `vigor_foco_arqueiro` (Arqueiro, o
  Foco). `vigor_foco/vigor-foco-topo.png` junta os topos atual e proposto em tamanho real, a ampliação 6× e os quatro
  símbolos juntos sobre o fundo da HUD.

### O Vigor, rodada 2: o punho cerrado refeito no Aseprite

O punho de `1a1dae3` foi recusado: lia como mão aberta, com os dedos levantados (as quatro barras verticais). Refeito
no Aseprite pelo MCP, da construção aos retoques, com o punho resolvido antes do fogo; o Foco ficou como estava.

- **A referência de construção:** o punho cerrado de frente pela palma (o ✊): os quatro dedos dobrados num bloco
  mais largo que alto, os nós em degrau (o médio mais alto, o mínimo mais baixo), as dobras entre eles só em sombra
  e curtas, a dobra escura onde os dedos entram, o polegar deitado atravessando pela frente, com a ponta separada
  das pontas dos dedos, a palma e o pulso mais estreito.
- **As etapas, no mesmo `.aseprite`:** a construção numa cor só com o contorno (conferida em 20); as partes em
  camadas com a luz de cima e da esquerda (pulso, dedos, polegar, dobras, contorno); um retoque na ponta do polegar;
  o fogo numa camada embaixo de tudo. Duas tentativas de fogo foram descartadas por voltarem a ler como cabeça: as
  línguas nos dois cantos de cima (orelhas) e a chama em volta do topo (cabelo, com os nós virando sobrancelhas). O
  punho desceu 2 px (o pulso ficou com 4 linhas) e foi 2 px para a esquerda; o fogo ficou como **uma labareda só,
  atrás do lado direito**, mais alta que o punho, laranja do vigor e mais quente junto da mão: secundária, sem
  cobrir a mão nem sair das pontas dos dedos.
- **A fonte:** `vigor_foco/fontes/vital-vigor/vital-vigor-20.aseprite` (camadas chama, pulso, dedos, polegar,
  dobras, contorno). A proposta anterior está em `vigor_foco/recusados/vigor-punho-r1/` (fonte, PNGs, auxiliar e a
  foto do topo).
- **As operações:** *cálculos fora do editor:* `vigor_foco/auxiliares/punho/` (`grade.py`, que passa uma grade de
  letras para as listas por camada; `e1_construcao.py`, `e2_partes.py` e `e3_chama.py`, as três etapas, rodadas na
  própria pasta e nessa ordem; `ver.py`, a captura do editor em 1× e 10×); *Lua pelo `execute_script`:* o documento,
  as camadas, a pintura pelo `pintar.lua` (cada pixel relido; 0 diferentes, 0 fora da tela), a limpeza das cels ao
  refazer uma etapa e o `saveAs`; *ferramentas do conector:* a captura do editor a cada etapa.
- **A exportação:** `exportar_aseprite.py vital-vigor ... --fontes=...`; o composto é igual à captura do editor e às
  listas das camadas, e o @2x é a duplicação exata.
- **As fotos:** `ROTULO=punho-r2 SO_PROPOSTA=1 JANELAS=1920x945 node .../fotografar.mjs vigor_foco` (o Guerreiro).
  `vigor_foco/vigor-punho-r2.png`: o topo no jogo, o antes e o depois em tamanho real e 6×, as etapas no Aseprite e
  os quatro símbolos juntos.

### O Vigor, rodada 3: o punho sem fogo

O Jean escolheu o punho sem fogo para o Vigor. A mão da rodada 2 (`2c4bf85`) ficou como estava (os dedos dobrados, o
polegar, o pulso e a luz, pixel a pixel); só saiu a labareda e o punho voltou para o meio do quadro.

- **Na fonte em camadas, pelo MCP:** a camada chama foi apagada, e os pixels do contorno dela, tirados da camada de
  contorno (`pintar.lua`, com alfa 00); as camadas andaram 2 px para a direita e 2 para cima (`cel.position`, numa
  transação), desfazendo o deslocamento feito para a labareda; a base do pulso, que deixou de encostar na beira,
  fechou com uma linha de contorno (11 pixels). Camadas: pulso, dedos, polegar, dobras, contorno.
- **O alinhamento:** o punho ocupa x 2..16 e y 4..18, com o centro em (9,6; 11,6), como a Mana (9,6; 11,5); a Vida e o
  Foco ficam em x 10. A mão não cresceu: ao lado dos outros três, em tamanho real, a presença é parecida (15 px de
  largura, contra 16 da gota e 18 e 19 do coração e do alvo).
- **Conferido:** o PNG é igual à captura do editor, o @2x é exato, e cada pixel do punho é o da rodada 2 deslocado
  (os únicos novos são os do fecho do pulso). `auxiliares/punho/` refaz o desenho: `e2_partes.py` e depois
  `e3_sem_fogo.py` (a etapa do fogo saiu daqui e ficou no histórico).
- **O histórico com fogo:** `vigor_foco/recusados/vigor-punho-r2-fogo/` (a fonte com a camada chama, os PNGs, os
  auxiliares e a foto do topo).
- **As fotos (1920×945):** `ROTULO=punho-r3 SO_PROPOSTA=1 ... fotografar.mjs vigor_foco` (o Guerreiro). O Foco foi
  fotografado de novo no Arqueiro e é o mesmo, pixel a pixel, da apresentação anterior. `vigor_foco/vigor-punho-r3.png`
  junta o topo do Guerreiro (no jogo, com fogo, sem fogo), o do Arqueiro (no jogo e com o Foco), a ampliação 6× e os
  quatro símbolos juntos.

### Integrados: o Vigor e o Foco (1.131.0)

O punho sem fogo de `4eea5b6` e o alvo de `1a1dae3`, sem retoque. As fontes foram para
`ferramentas/arte/aseprite/vital-vigor/` e `vital-foco/`; os quatro arquivos do jogo (20 e @2x) são idênticos, byte a
byte, aos aprovados, e o exportador os reproduz (`--conferir`). Os papéis em `Icones` (`VITAL`) não mudaram; o único
uso é o topo. Com eles, os quatro ícones das barras do topo estão em pixel art.

## Vida e recursos: Ouro e Provisões (`ouro_provisoes/`)

**Proposta, nada no jogo.** Os atuais (`moedas-24`, `provisoes-24`) são placeholders; as propostas não os copiam.

- **Os usos, conferidos:**
  - **Ouro** (`moedas`): só o topo, em 24 (`Icones.recurso`, a quantidade de ouro; sem ouro, a bolsa vazia do jogo). O
    ouro do mercado e dos serviços (`ouro-loja`) usa o sprite `moedas` do jogo, outro papel: fica como está (lacuna
    registrada, não tratada aqui).
  - **Provisões** (`provisoes`, papel do desenho `pernil` em `RECURSO`): o topo, em 24, e o cartão "Provisões (1 dia)"
    do mercado, em 32 (pelo `Icones.porDesenho`). Hoje o 32 é o @2x do 24 reduzido pelo navegador; a proposta tem um
    32 próprio. Sem comida, o topo mostra o osso (`osso-24`), que não muda.
  - **O que são as Provisões nos dados:** comida de viagem contada em dias (`provisoes`; o mercado vende "Provisões
    (1 dia)"; acabou, vem a fome). O desenho do jogo para elas é o `pernil` (os relatórios, o mercado).
- **O Ouro (24):** uma pilha de moedas vista um pouco de cima, a de cima de face e as juntas entre elas nas laterais,
  e uma moeda apoiada na frente, com a beira em relevo e o sulco do anel. Poucos planos de luz (a face de cima, a
  lateral em degradê, a beira), sem brilho solto. Camadas: pilha, topo, moeda, contorno.
- **As Provisões (24 e 32):** o pernil, a coxa de carne curada com o osso; a casca com a luz de cima e da esquerda em
  faixas e o brilho na parte larga, o osso no creme do osso do topo (o par: o pernil quando há comida, o osso quando
  acaba). A mesma construção nos dois tamanhos (um modelo ao longo de um eixo diagonal). Distinto da mochila (sem
  saco), da aljava e das poções; a massa embaixo à esquerda, ao contrário da tocha vizinha. Camadas: carne, osso,
  contorno.
- **As rodadas:** o pernil tinha dois barbantes cruzando a carne; o Jean não gostou e eles saíram (a camada apagada
  na fonte e a casca completada embaixo). A versão com barbante fica em `ouro_provisoes/recusados/provisoes-barbante/`
  (os PNGs, o script e as fotos; a fonte é a mesma, sem a camada).
- **As etapas no Aseprite, pelo MCP:** a silhueta numa cor só, conferida em tamanho real; os materiais e a luz; os
  retoques (no Ouro, a rampa mais saturada, a face de cima sem o claro quase branco, a moeda da frente mais redonda e
  com aro; no pernil, a luz no lado certo, o fundo redondo e a saída dos barbantes). Tudo pelo `pintar.lua` (cada
  pixel relido; 0 diferentes, 0 fora da tela), com a limpeza das cels a cada refação.
- **As fontes:** `ouro_provisoes/fontes/moedas/moedas-24.aseprite` e `fontes/provisoes/provisoes-24.aseprite`, `-32`.
  Os auxiliares em `ouro_provisoes/auxiliares/` (`ouro.py silhueta|final`, `pernil.py <24|32> [silhueta]`, `ver.py`)
  reproduzem as exportações.
- **A exportação:** `exportar_aseprite.py moedas|provisoes ... --fontes=...`; o composto é igual à captura do editor
  e o @2x é a duplicação exata.
- **As fotos (1920×945):** `node .../fotografar.mjs ouro_provisoes` (o mercado, o Guerreiro: o topo e o cartão das
  Provisões; a foto nova `mercado` do roteiro recorta o cartão de cada desenho da peça fora do topo; a proposta
  registra o 32 só na página, pelo `papel_tamanhos`). `ouro_provisoes/ouro-provisoes.png` junta o topo e o cartão em
  tamanho real, as ampliações e a prancha sobre o carvão (`prancha-carvao.png`).
- **Limitações:** na integração, o `TAMANHOS` de `provisoes` passa a [24, 32]; o Ouro do mercado e dos serviços
  continua no sprite do jogo.
- **Integrados na 1.132.0, sem retoque** (aprovados no `33d8a6c`): as fontes foram para `ferramentas/arte/aseprite/moedas/`
  e `provisoes/`; os seis arquivos do jogo são idênticos, byte a byte, aos da proposta. As fotos com os arquivos de
  produção a 1920×945 estão em `ouro_provisoes/capturas/no-jogo-1.132.0-*` (`SO_ATUAL=1`): os ícones batem pixel a
  pixel com as fotos da proposta, e o cartão das Provisões carrega o `provisoes-32.png`.
- **O Ouro do balcão (1.133.0):** o seu ouro no mercado e nos serviços (ferreiro, curandeira, templo, taverna; 32 px)
  passou a ser a pilha aprovada, num 32 derivado da construção do 24 (`ferramentas/arte/aseprite/moedas/moedas-32.aseprite`,
  `ouro.py final 32`). Antes e depois a 1920×945 em `ouro_provisoes/capturas/ouro-loja/` (o mercado e o ferreiro
  inteiros; o recorte do ouro nos cinco; `ouro-loja-antes-depois.png`): medidas, textos e posições iguais.

## Vida e recursos: a moeda avulsa e a tocha (`moeda_tocha/`)

**Proposta, nada no jogo.** Uma peça por vez, primeiro a moeda e depois a tocha; aguardam a avaliação do Jean.

- **Os usos, conferidos:**
  - **A moeda avulsa** (o sprite `moeda` do jogo, 16×16; não tem papel em `Icones`): em 16, os preços dos cartões do
    mercado e dos serviços, a linha "Custo" da taverna, a dica de venda e recompra, o prêmio dos cartazes do mural, os
    ganhos do pagamento de contratos (o CSS pede 32 para `.festa .ganho`, mas o `--s` do próprio `<img>` vale e ele fica
    em 16), o chip de ouro do relatório e as moedas que voam até o ouro do topo (`moedasPara`, de 1 a 0,6 no caminho);
    em 32, a linha de Ouro do espólio e a moeda que o ladrão leva na luta (`projetil`, animação). Tamanhos: 16 e 32.
  - **A tocha** (`tocha`, papel de consumível e de recurso): o topo (24), o cartão do mercado, a bolsa do Inventário, o
    espólio e o voo até a bolsa (32). Os 48 e 64 do jogo não aparecem parados em lugar nenhum: a proposta tem só 24 e
    32. O tremular do topo (`app/controles.js`) só troca os sprites do jogo e não age sobre os arquivos (como hoje).
- **A moeda (16 e 32):** a moeda da frente da pilha aprovada (`moedas-24`), sozinha e de frente: o mesmo ouro, as
  mesmas regras de luz (a beira em relevo clara, o sulco do anel fundo, a face) e a espessura aparecendo embaixo à
  direita, que dá volume e a distingue da pilha do saldo. Sem cunhagem: no 16 não cabe com clareza, e o 32 é a mesma
  construção. Camadas: espessura, beira, anel, face, contorno.
- **A tocha (24 e 32):** a tocha simples de aventureiro, o placeholder não foi seguido: o cabo de madeira em
  diagonal, a cabeça de pano encerado enrolado (as voltas em faixas de tom) e a chama subindo reta, uma gota de base
  redonda com a ponta ondulando e duas línguas soltas, o miolo quente embaixo (perto do pano) e as beiras de cima
  escurecendo para o vermelho. Camadas: cabo, pano, chama, contorno.
- **As rodadas da tocha (no desenho, antes do Aseprite):** a primeira chama saiu branca demais e em forma de lâmina, e
  a cabeça lia como uma porca; a gota com o miolo menor e a cabeça mais larga resolveram. Depois, a chama escondida
  atrás do pano (torta para a direita) e a ponta de 1 px (um pavio) foram corrigidas subindo a base e encurtando a
  ponta.
- **As etapas:** as listas por camada saem de `moeda_tocha/auxiliares/moeda.py <16|32>` e `tocha.py <24|32>` (cálculo
  fora do editor; `silhueta` dá a etapa numa cor só), conferidas em tamanho real pela `prancha.py`; a pintura no
  Aseprite pelo MCP com o `pintar.lua` (operações em Lua; 0 diferentes, 0 fora da tela em todas as camadas); salvar
  pelo editor. Fontes em `moeda_tocha/fontes/moeda/moeda-16.aseprite`, `-32` e `fontes/tocha/tocha-24.aseprite`, `-32`.
- **A exportação:** `exportar_aseprite.py moeda|tocha moeda_tocha/proposta --fontes=moeda_tocha/fontes`; os quatro
  compostos são iguais, pixel a pixel, à captura do editor e às listas, e os @2x são a duplicação exata.
- **As fotos (1920×945, os mesmos dados nos dois modos):** `node .../fotografar.mjs moeda` (o mercado: os preços; o
  ferreiro; o chip e o voo das moedas, pelo `efeito` do jogo; o espólio e o pagamento de um contrato, pelo
  `Telas.celebrar`; o mural) e `... tocha` (o topo, o cartão do mercado, a bolsa do Inventário). A moeda ganha o papel
  só na página da proposta: o `sprites.js` servido com o `Sprites.img("moeda")` trocado pelo arquivo da proposta
  (`papel_sprite`). As folhas `moeda_tocha/moeda-no-jogo.png` e `tocha-no-jogo.png` (atual × proposta, em tamanho real)
  e a prancha `moeda_tocha/prancha-carvao.png` saem do `auxiliares/montar.py`.
- **A avaliar:** a moeda proposta lê como moeda (aro e face) nos preços, no chip e no voo, onde a atual é uma mancha
  amarela; no espólio a atual, a 32, lê quase como uma pilha. A tocha proposta é mais leve que a atual no topo (o cabo
  mais fino e a chama menor que a bola de fogo atual), em troca do pano e da chama em línguas.
- **Limitações:** a moeda que o ladrão leva na luta (32, `projetil`) não foi fotografada (pede uma luta com ladrão).
  Integrar a moeda pede um papel novo em `Icones` e trocar o `S("moeda", …)` dos lugares acima, sem tocar no sprite
  (o mapa e as cenas não o usam). A tocha apagada do topo e o chip "tocha" do relatório (o sprite 16×16) ficam com o
  do jogo.
- **A moeda integrada na 1.134.0, sem retoque** (aprovada no `c00d0cf`): as fontes foram para
  `ferramentas/arte/aseprite/moeda/`; os quatro arquivos do jogo são idênticos, byte a byte, aos da proposta. O papel é
  o `Icones.moeda`. As fotos com os arquivos de produção a 1920×945 (`moeda_tocha/capturas/moeda/no-jogo-1.134.0-*`, o
  roteiro com `SO_ATUAL=1`): nos preços, no ferreiro, no chip, no espólio, no pagamento de contrato e no mural, os
  pixels da moeda são os mesmos da proposta. O ladrão, que faltava: uma luta contra bandidos até um roubar
  (`moeda_tocha/auxiliares/ladrao.mjs`); as seis moedas que voam até ele são o `moeda-32.png`
  (`no-jogo-1.134.0-1920x945-ladrao.png`), com o mesmo movimento.
- **A tocha, rodada 2: só a chama refinada (proposta, nada no jogo).** O cabo, o pano, a paleta e o tamanho no topo
  ficaram aprovados; o Jean pediu a chama sem a faixa horizontal larga (sobretudo no 32), com línguas de alturas e
  curvas desiguais e a passagem do miolo claro menos quadrada, sem halo. O Jean gostou também da rodada 1: as duas
  ficam para comparar.
  - **O que mudou:** o calor da gota principal segue o eixo curvo da língua (mais forte perto do eixo e embaixo, perto
    do pano), em vez de anéis em volta de um ponto: os tons sobem em línguas, sem atravessar a chama na mesma altura,
    e o miolo claro vira uma gota alongada. A ponta principal em S virando à esquerda; a língua da esquerda alta e
    abrindo para fora; a da direita curta. Onde as línguas cruzam a principal, vale a principal (sem pontos escuros
    por dentro). O fogo continua saindo da beira de cima do pano.
  - **No Aseprite pelo MCP:** nas fontes `moeda_tocha/fontes/tocha/tocha-24.aseprite` e `-32`, as cels de `chama` e
    `contorno` saíram e foram repintadas pelo `pintar.lua` (0 diferentes, 0 fora da tela); `cabo` e `pano` não foram
    tocados (as listas são as mesmas da rodada 1). Listas pelo `auxiliares/tocha.py <24|32>` (agora a rodada 2).
  - **Conferido:** os compostos exportados são iguais à captura do editor e às listas; os @2x exatos.
  - **A rodada 1 guardada inteira** em `moeda_tocha/tocha_r1/` (as fontes, os PNGs, as fotos, a folha e o script
    `tocha_r1.py`).
  - **As fotos (1920×945, os mesmos dados):** `ROTULO=rodada2 node .../fotografar.mjs tocha` e
    `SO_PROPOSTA=1 ROTULO=rodada1 PASTA=moeda_tocha/tocha_r1/proposta ...`; a folha `moeda_tocha/tocha-no-jogo.png`
    (o jogo, a rodada 1, a rodada 2: o topo, o cartão do mercado e a bolsa) e a prancha `prancha-carvao.png`.
- **A tocha integrada na 1.135.0, sem retoque** (a rodada 2, aprovada no `1c6a2c2`): as fontes foram para
  `ferramentas/arte/aseprite/tocha/`; os quatro arquivos do jogo são idênticos, byte a byte, aos da proposta; o
  `TAMANHOS` passou a [24, 32] e os 48 e 64 antigos saíram (sem uso). Fotos com os arquivos de produção a 1920×945
  (`moeda_tocha/capturas/tocha/no-jogo-1.135.0-*`): no topo, no cartão do mercado e na bolsa, os pixels da tocha são
  os mesmos da rodada 2; o recebimento de uma tocha (`auxiliares/tocha_voo.mjs`, o `efeito` do jogo) voa o
  `tocha-32.png` do chip até o topo, no movimento de sempre (`moeda_tocha/tocha-voo-1.135.0.png`). O chip, o aviso e
  as escolhas mostram a tocha em 16, o sprite do jogo: não há arquivo desse tamanho.

## As variantes da tocha: o 16 e a apagada (`moeda_tocha/variantes/`)

**Proposta, nada no jogo.** Aguardam a avaliação do Jean; o 24 e o 32 integrados (1.135.0) não mudam.

- **Os usos, conferidos:**
  - **a tocha em 16** (o sprite `tocha` do jogo, sem papel em `Icones`): o chip de um item ganho no texto, o aviso
    flutuante (o mesmo, numa tela), o risco "−1 tocha" da escolha que entra numa sala escura da capela à noite e o
    ícone das escolhas que gastam o item (`escolhas.js`, `meta.gasta`);
  - **a apagada** (`tocha_apagada`, o estado "sem tochas": o contador em 0, em alerta): o topo (hoje o sprite 16×16
    ampliado a 32, maior que os vizinhos de 24) e o risco "Sem luz: inimigo age primeiro" das mesmas escolhas (16).
    Tamanhos da proposta: 24 (o topo, como os outros recursos) e 16.
- **O 16:** a mesma construção da tocha aprovada na grade de 16 (o `tocha.py 16`, sem retoque: a redução já manteve
  o cabo de 2 px, o pano com as voltas e a chama com três pontas de alturas diferentes e o miolo claro). Camadas: cabo,
  pano, chama, contorno.
- **A apagada:** o mesmo cabo e o mesmo pano da aprovada, sem chama; a ponta de cima do pano queimada (quase preta)
  e dois fios curtos de fumaça cinza subindo, com um vão entre eles e mais fracos em cima, sem contorno (vapor). É o
  significado do sprite do jogo (a tocha que se apagou). Camadas: cabo, pano, queimado, contorno, fumaca. A primeira
  fumaça (um fio longo) parecia um gancho e depois uma vareta; os dois fios curtos resolveram.
- **As etapas:** listas pelo `auxiliares/tocha.py <16|24|32> [apagada]` (o 24 e o 32 aprovados saem iguais, pixel a
  pixel), pintadas no Aseprite pelo MCP com o `pintar.lua` (0 diferentes, 0 fora da tela); fontes em
  `variantes/fontes/tocha/tocha-16.aseprite` e `variantes/fontes/tocha_apagada/tocha_apagada-16.aseprite`, `-24`;
  exportadas pelo `exportar_aseprite.py tocha|tocha_apagada variantes/proposta --fontes=variantes/fontes` (o composto
  igual à captura do editor e às listas, os @2x exatos).
- **As fotos (1920×945, os mesmos dados):** `fotografar.mjs tocha16` (o aviso numa tela, o chip na vila),
  `tocha16_risco` e `tocha_apagada` (a capela à noite, com 2 tochas e sem tochas). O roteiro ganhou o papel de sprite
  por tamanho (`papel_sprite`: só os tamanhos que a proposta tem) e o recurso do topo só na página (`papel_recurso`).
  Folhas `variantes/tocha16-no-jogo.png`, `apagada-no-jogo.png` e a prancha `variantes/prancha-carvao.png`
  (`montar.py variantes`).
- **Na integração:** um papel em `Icones` para a tocha em 16 e para a apagada (o `RECURSO` do topo e os 16 do chip, do
  aviso e dos riscos, que hoje vêm do `spr`); o tremular do topo (`controles.js`) só troca os sprites e não muda.
- **As variantes integradas na 1.136.0, sem retoque** (aprovadas no `ef71aa3`): as fontes foram para
  `ferramentas/arte/aseprite/tocha/` (o 16, junto do 24 e do 32) e `tocha_apagada/`; os seis arquivos do jogo são
  idênticos, byte a byte, aos da proposta. Os papéis: a apagada no `RECURSO` do topo (24) e o `Icones.miudo` para os
  16 pedidos pelo nome (o chip, o aviso, o item e os riscos das escolhas). Fotos com os arquivos de produção a 1920×945
  (`variantes/capturas/*/no-jogo-1.136.0-*`, o roteiro com `SO_ATUAL=1`): o aviso e o topo sem tochas são idênticos às
  fotos da proposta; no chip e nos riscos, os pixels da tocha são os mesmos. A caixa do recurso no topo e a escolha
  têm as mesmas medidas de antes (só o ícone do topo passou de 32 para 24). Na conferência apareceu mais um uso de 16,
  o aviso de escuro do painel do lugar (`risco-lugar`, com e sem tocha): entrou no mesmo papel
  (`no-jogo-1.136.0-1920x945-riscos-lugar.png`).

## Lote da noite de 19/10, lote 1: a Bandagem e a Poção de Vida (`bandagem_pocao/`)

**Proposta, nada no jogo, não aprovada.** Os atuais são placeholders da família de ferro; as propostas os reinterpretam.

- **Os usos, conferidos:**
  - **a Poção de Vida** (`pocao`): o topo (24), a bolsa da ficha, o Inventário, o mercado, o espólio, o voo e as
    escolhas que a usam (32) e o comando **Itens** da roda da luta (`ACAO.pocao`, 32: papel compartilhado, a mesma
    imagem); em 16, o sprite `pocao` do chip, do aviso e do ícone das escolhas;
  - **a Bandagem** (`bandagem`): o topo (24), os mesmos usos de consumível (32) e o sprite de 16;
  - os arquivos 48 e 64 das duas não aparecem parados em lugar nenhum (só o baú usa 48). Tamanhos da proposta: 16, 24, 32.
- **A Bandagem:** um rolo de linho deitado, um cilindro quase horizontal com as bordas paralelas; a face da ponta
  virada para a luz, com uma espiral só, solta e em tom de pano, e o miolo (não anéis escuros: nada de rosca); duas
  bordas de volta no corpo, suaves e inclinadas, com a sombra e a beira clara da espessura que sobrepõe; a ponta solta
  deitada para a direita, a face larga clara, a dobra e o corte desfiado (dobra e desfiado só no 32). Camadas: tira,
  corpo, face, contorno.
- **A Poção de Vida:** um balão redondo de vidro (o perfil de revolução de `auxiliares/frasco.py`, a base da família de
  frascos): o líquido vermelho até perto de dois terços, a superfície clara marcando o nível, o vidro vazio escuro em
  cima com a beira clara (a espessura), o fundo tingido pelo líquido, o brilho agrupado em cima à esquerda e um reflexo
  vertical; o gargalo, o anel da boca e a rolha de cortiça. Camadas: vidro, liquido, rolha, brilho, contorno.
- **As tentativas descartadas** (em `bandagem_pocao/recusados/`): a bandagem com a espiral forte e o corpo subindo
  (parecia uma concha de caracol; antes, a tira estreita fazia um martelo) e a poção com o balão menor (pouca presença
  no espaço de 32 ao lado da bandagem e da tocha). A primeira poção também saiu rosada; o vermelho foi aprofundado.
- **As etapas:** listas pelos auxiliares (`bandagem.py <N>`, `frasco.py pocao <N>`, com `silhueta` para a etapa numa
  cor), conferidas pela `prancha.py`; pintura no Aseprite pelo MCP com o `pintar.lua` (0 diferentes, 0 fora da tela);
  fontes em `bandagem_pocao/fontes/bandagem/bandagem-16|24|32.aseprite` e `fontes/pocao/pocao-16|24|32.aseprite`;
  exportação pelo `exportar_aseprite.py <peça> bandagem_pocao/proposta --fontes=bandagem_pocao/fontes`. O composto do
  editor confere com o exportado e com a prévia por um código de conferência (`auxiliares/soma.lua` no editor,
  `soma.py` nos PNGs); os @2x são exatos.
- **As fotos (1920×945, os mesmos dados):** `fotografar.mjs bandagem_pocao` (o topo, a bolsa da ficha e os cartões do
  mercado, o aviso e o chip de cada item ganho, a bolsa do Inventário; o 16 pelo `papel_sprite`, só na página) e
  `bandagem_pocao_luta` (a roda da luta). O roteiro ganhou as fotos `aviso-item` e `chip-item` (a lista em `itens`).
  Folha `bandagem_pocao/bandagem_pocao-no-jogo.png` e prancha `bandagem_pocao/prancha-carvao.png`
  (`bandagem_pocao/auxiliares/montar.py bandagem_pocao`).
- **A decidir na avaliação:** o comando Itens da roda da luta muda junto com a poção (o papel é a mesma imagem); o
  frasco vazio do topo (sem poções) continua o sprite do jogo e pediria a sua variante, como a tocha apagada.

## Lote da noite de 19/10, lote 2: o Tônico Restaurador e o Antídoto (`tonico_antidoto/`)

**Proposta, nada no jogo, não aprovada.** A mesma família de frascos da nova Poção de Vida (`bandagem_pocao/`).

- **Os dados e os usos, conferidos:** o **Tônico Restaurador** recupera metade da mana, do vigor ou do foco (o sprite
  `pocao_azul`; o arquivo `tonico`, hoje em 32, 48, 64); o **Antídoto** cura veneno e vale na luta (o sprite `folha`;
  o arquivo `antidoto`, 32, 48, 64). Os dois: 32 nos usos de consumível (o mercado, a bolsa, o espólio, o voo, as
  escolhas) e 16 no chip, no aviso e nas escolhas. Os 48 e 64 atuais não aparecem parados. **Os sprites de 16 são
  compartilhados:** o `pocao_azul` é também o ícone de custo da Mana (`RECURSO_ICONE`) e a Mana da celebração, e a
  `folha` é a Agilidade da celebração e do Inventário. Um 16 integrado viria pelo id do item, não pelo nome do sprite.
- **A família:** o perfil de revolução, o vidro, a luz e a leitura do nível do `frasco.py`; cada um com a sua silhueta
  e o seu fechamento, não só a cor:
  - **o Tônico:** a garrafa alta de paredes retas e ombros redondos, a rolha larga, o líquido azul (a cor que já o
    identifica) quase cheio;
  - **o Antídoto:** o frasco estreito em tubo, o fundo arredondado, o gargalo comprido e a boca lacrada com cera de
    abelha que escorre pelo gargalo; o líquido verde (a cor de hoje). Nada de folha nem símbolo: o lacre é só o
    fechamento. No 16, o tubo um pouco mais largo (com a largura do 32 o líquido ficaria com 1 px; a versão estreita
    em `recusados/antidoto-16-estreito/`).
- **As etapas:** listas pelo `bandagem_pocao/auxiliares/frasco.py tonico|antidoto <16|32>` (o gerador da família
  ganhou a garrafa reta, o reflexo pela largura do vidro e o lacre de cera; a poção sai igual, pixel a pixel), pintura
  no Aseprite pelo `pintar.lua` (0 diferentes, 0 fora da tela); fontes em `tonico_antidoto/fontes/tonico/` e
  `antidoto/` (16 e 32); exportação pelo `exportar_aseprite.py --fontes=`; o composto do editor confere pelo
  `soma.lua`; @2x exatos. A primeira pintura saiu com o antídoto nas duas peças (as listas das duas na mesma pasta);
  refeita com uma pasta por variante.
- **As fotos (1920×945, os mesmos dados):** `fotografar.mjs tonico_antidoto` (os cartões do mercado, o espólio com os
  dois achados, o aviso e o chip de cada um); o `papel_sprite` aceita o sprite que serve um arquivo de outro nome. Folha
  `tonico_antidoto/tonico_antidoto-no-jogo.png` e prancha `tonico_antidoto/prancha-carvao.png`.

## Lote da noite de 19/10, lote 3: a Calça de Viagem e o Manto do Mago (`calca_manto/`)

**Proposta, nada no jogo, não aprovada.** As duas peças existem nos dados e são de tecido (nenhuma substituição).

- **Os dados, conferidos:** a **Calça de Viagem** é a calça do Mago (`PECAS["pernas"]["mago"]`, o desenho
  `calca_tecido`; também a base do único Mordida do Túmulo); hoje é o sprite 16×16 da perneira recolorido e não tem
  papel em `Icones`. O **Manto** (o desenho `manto`) é de **três bases do Mago — Manto, Túnica e Veste Rúnica** — e do
  único Manto de Cinzas; também só o sprite. Os materiais do Mago são de tecido (Puído, de Linho, de Lã Negra, Bordado,
  Rúnico). Usos de equipamento: 32 (a ficha, a mochila do mercado, as dicas), 40 (o corpo e a mochila do Inventário),
  48 (o "você usa" do saque) e 64 (o cartão do saque).
- **Compartilhamento a separar (os dados não mudaram):** um manto aberto na frente não é uma túnica (fechada, vestida
  pela cabeça) nem uma veste rúnica. A proposta é um desenho por base: o Manto (este, a frente aberta mostrando o forro),
  a Túnica (a mesma lã, fechada, só a faixa e a gola) e a Veste Rúnica (a veste longa com o debrum de runas bordadas),
  com o `icone` de cada base em `ARMADURAS["mago"]` e a migração dos saves. Na foto do saque, o item vestido é uma
  Túnica Puída com o desenho do manto.
- **A Calça de Viagem:** a lã azul-acinzentada do capuz de tecido aprovado (a mesma rampa), solta, as pernas abrindo um
  pouco e franzindo sobre as faixas de linho enroladas nos tornozelos (a calça de quem viaja), o cordão com o laço na
  cintura no lugar do cinto, vincos leves nas coxas e no joelho; sem costura nem remendo: o que a separa da calça de
  couro. Camadas: pernas, dobras, barra, cintura, cordao, contorno.
- **O Manto:** a veste vista de frente, construída por partes: a gola fechada com o broche de latão, o tronco que afina
  até a cintura, a faixa de pano com a ponta do nó, a saia que abre até a barra com duas pregas, a frente aberta da
  cintura à barra mostrando o forro escuro (a frente e o fundo) com o debrum claro da seda da luva, e as mangas largas
  saindo dos ombros, separadas do corpo por uma costura escura, com o vão escuro da boca. Camadas: mangas, corpo, forro,
  gola, debrum, faixa, fecho, contorno.
- **Tamanhos:** 32 (a arte principal), 40 e 48 da mesma construção (as medidas em frações do quadro, sem retoque), o 64
  é o 32 ampliado 2× (a política da skill; na integração, `DERIVADOS` no exportador).
- **As etapas:** `calca_manto/auxiliares/tecido.py <calca|manto> <N> [silhueta]`, conferido pela `prancha.py`; a
  primeira rodada saiu com as faixas pretas (a letra da rampa de linho era a do contorno no `pixel_comum`) e com as
  mangas sumindo no corpo do manto; refeito em partes. Pintura no Aseprite pelo `pintar.lua` (0 diferentes, 0 fora da
  tela); fontes em `calca_manto/fontes/calca_tecido/` e `manto/` (32, 40, 48); exportação pelo `exportar_aseprite.py
  --fontes=`; o composto do editor confere pelo `soma.lua`; @2x exatos.
- **As fotos (1920×945, os mesmos dados):** `fotografar.mjs calca_manto` (a ficha e o Inventário de um Mago vestindo
  as duas, `VESTIR`; o saque do Manto) e `calca_manto_saque_calca` (o saque da calça); o roteiro ganhou `papeis`
  (vários papéis de item só na página). Folha `calca_manto/calca_manto-no-jogo.png` e prancha
  `calca_manto/prancha-carvao.png` (com a calça de couro, o capuz e a luva de seda para comparar).

## Integração na 1.138.0: a Bandagem, a Poção de Vida, o Tônico, a Calça de Viagem e o Manto

**No jogo, sem retoque** (aprovados no `211b8e2`, `d401a92` e `c63f84b`). As fontes foram para `ferramentas/arte/aseprite/`;
os 46 arquivos do jogo são idênticos, byte a byte, aos das propostas. Os papéis: a calça e o manto no `ITEM`; a
bandagem e a poção também no `Icones.miudo`; o 16 de um consumível pelo id do item (`Icones.pequeno`: o chip, o aviso,
o item e o gasto das escolhas), o que deixa o sprite do Tônico (`pocao_azul`) como a Mana e o Unguento. A Poção segue
como o comando Itens da luta e o Manto segue compartilhado (decisões do Jean).
- **Conferido a 1920×945 com os arquivos do jogo** (`*/capturas/no-jogo-1.138.0-*`, o roteiro com `SO_ATUAL=1`): o
  topo, a bolsa e os cartões do mercado, o aviso e os chips, a roda da luta, o espólio, a ficha, o Inventário e o saque
  saem com os ícones das propostas (as diferenças que sobram são o fade do aviso, os raios do saque e o antialiasing dos
  números; o Antídoto, que não entrou, e os consumíveis antigos nas fotos da proposta da calça e do manto).
- **As interações, com os saves temporários dos cenários** (`bandagem_pocao/auxiliares/interacoes.mjs`): comprar um
  Tônico, uma Poção e uma Bandagem no mercado (85 de ouro, os preços somados; as quantidades sobem uma cada; a bolsa da
  ficha e o topo nos arquivos novos) e vestir o Manto achado pelo "Equipar agora" (64 e 48 no saque, 32 na ficha). Sem
  erro no console.

## Em avaliação depois da 1.138.0: a base do Antídoto e o frasco vazio

**Propostas, nada no jogo, não aprovadas.**

- **O Antídoto, rodada 2 (`tonico_antidoto/`): só a base.** O Jean pediu uma base curta e plana, que fique de pé numa
  mesa, com os cantos de baixo arredondados, sem mudar o resto. No `frasco.py`, o corpo do antídoto termina mais cedo
  e arredonda em 2 px em vez de 4,6 (o fundo afunilado virou uma base plana com a última linha um pixel mais estreita de
  cada lado). Só as linhas da base mudaram (14 e 15 no 16; 28 a 31 no 32); o corpo estreito, o gargalo, o lacre, o
  líquido e o acabamento são os mesmos. As fontes (`tonico_antidoto/fontes/antidoto/`) repintadas no Aseprite pelo
  `pintar.lua` (0 diferentes, 0 fora da tela); o exportado confere com o editor e com a prévia, @2x exatos. A versão
  anterior inteira (as fontes e os PNGs) em `tonico_antidoto/recusados/antidoto-base-redonda/`. Antes × depois no jogo
  a 1920×945 (`fotografar.mjs antidoto_base`, com `SO_PROPOSTA=1` e `ROTULO=antes` + `PASTA=` a versão anterior, ou
  `ROTULO=depois`): `tonico_antidoto/antidoto-base-antes-depois.png`; ampliado: `antidoto-base-prancha.png`.
- **O frasco vazio (`bandagem_pocao/variantes/`):** o estado do topo quando as poções acabam (`frasco_vazio`; hoje o
  sprite 16×16 em 32, maior que os vizinhos). A variante `frasco_vazio` do `frasco.py` é a Poção de Vida aprovada sem o
  líquido (o mesmo balão, o gargalo, a boca, a rolha, o vidro com a beira clara e o brilho); só o 24, o tamanho do topo
  (não há outro uso). Fonte em `variantes/fontes/frasco_vazio/frasco_vazio-24.aseprite` (vidro, rolha, brilho,
  contorno), pelo `pintar.lua`; exportado conferido, @2x exato. No topo a 1920×945 (`fotografar.mjs frasco_vazio`, o
  cenário `covil` na vila com `BOLSA=pocao_vida=0`; `frasco_cheio` com 2 poções): `variantes/frasco-cheia-vazia.png`
  (com poções | sem poções hoje | sem poções, a proposta) e `variantes/prancha-carvao.png`. Na integração, o papel é o
  `RECURSO` do topo em 24.
- **Integrados na 1.139.0, sem retoque** (aprovados no `b872544`): as fontes do Antídoto e do frasco vazio foram para
  `ferramentas/arte/aseprite/antidoto/` e `frasco_vazio/`; os seis arquivos do jogo são idênticos, byte a byte, aos das
  propostas. O 16 do Antídoto vem pelo item (`Icones.pequeno`); a `folha` segue como a Agilidade. Conferido a 1920×945
  com os arquivos do jogo: o cartão do mercado e o aviso de ganho idênticos às fotos aprovadas
  (`tonico_antidoto/capturas/no-jogo-1.139.0-*`); com o save temporário do cenário `tutorial`
  (`bandagem_pocao/auxiliares/frasco_topo.mjs`, fotos em `bandagem_pocao/variantes/capturas/integracao/`): o topo sem
  poções (o frasco vazio em 24), a compra de uma Poção no mercado (o topo passa para a poção, 1) e o gole pela bolsa (a
  vida de 30 para 51, o topo volta ao frasco vazio), a caixa do recurso com as mesmas medidas nos três estados e na
  versão anterior (que mostrava o sprite em 32); o Antídoto comprado aparece na bolsa (32).

## O anel e o amuleto (`anel_amuleto/`)

**Proposta, nada no jogo, não aprovada.** Os atuais são placeholders da família de ferro (32, 40, 48, 64).

- **Os dados, conferidos:** o desenho `anel` é das bases **Anel, Sinete e Aro** e do único **Anel do Último Rei** ("O
  reino caiu. O anel não."); o `amuleto`, das bases **Amuleto, Talismã, Pingente e Medalhão** (nenhum único). Os
  acessórios não têm material no nome (só os afixos). **Os espaços vazios** do amuleto e dos dois anéis usam os mesmos
  arquivos, apagados (`VAZIO`, a classe `fantasma`): a troca alcança também essas silhuetas (32 no corpo, 48 no "você
  usa" do saque). Usos: 32 (a ficha, a mochila do mercado), 40 (o Inventário), 48 e 64 (o saque).
- **O anel:** o aro de latão (a rampa do aro do escudo aprovado) visto de três quartos, um pouco de cima: a abertura
  vazada (o fundo aparece), a parede de dentro do lado de trás, mais escura (a espessura), o lado de fora em poucos
  planos de luz com o brilho agrupado em cima à esquerda, e um engaste pequeno com uma granada no alto (a identidade no
  tamanho real). Camadas: aro, parede, brilho, engaste, pedra, contorno. Uma primeira versão com o aro menor ficou em
  `recusados/anel-menor/` (pouca presença no espaço de 32).
- **O amuleto:** um medalhão redondo de latão (a borda em relevo, o sulco, o campo plano e o botão do meio), a argola
  no alto e o cordão de couro em gota, que passa pela argola e fecha o laço do colar (nada solto). Serve ao Amuleto,
  ao Talismã, ao Pingente e ao Medalhão sem símbolo que prometa efeito. Camadas: cordao, argola, medalhao, brilho,
  contorno.
- **Tamanhos:** 32 (a arte principal), 40 e 48 da mesma construção, 64 = 32 ampliado 2× (na integração, `DERIVADOS`
  como a calça e o manto). O cordão fica com 1 px também no 48.
- **As etapas:** `anel_amuleto/auxiliares/joias.py <anel|amuleto> <N> [silhueta]`; as rodadas do desenho: o anel grosso
  com a abertura pequena e o engaste borrado; o amuleto com o cordão chato (um chapéu) e o campo do medalhão como uma
  pepita, refeitos com o laço em gota e os tons limpos. Pintura no Aseprite pelo `pintar.lua` (0 diferentes, 0 fora da
  tela); fontes em `anel_amuleto/fontes/anel/` e `amuleto/` (32, 40, 48); exportação pelo `exportar_aseprite.py
  --fontes=`; o composto do editor confere (`soma.lua`); @2x exatos.
- **As fotos (1920×945, os mesmos dados):** `fotografar.mjs anel_amuleto` (a ficha e o Inventário do Mago com um anel
  vestido e o outro espaço vazio; o saque do anel) e `anel_amuleto_saque_amuleto`. Folha
  `anel_amuleto/anel_amuleto-no-jogo.png` e prancha `anel_amuleto/prancha-carvao.png` (com os atuais e o escudo).
- **Alcance proposto e limitações:** trocar o desenho para todas as bases e o único, e as silhuetas dos vazios junto
  (são a mesma imagem). O **Aro** (um aro liso, pelo nome) e o **Sinete** (um anel de selo) recebem um anel com uma
  pedra; o Anel do Último Rei combina com o engaste. Se o Jean quiser o Aro liso e o Sinete com o selo, a proposta é
  um desenho por base (sem mudar os dados nesta rodada). No espaço de 32, o anel é mais baixo que os outros
  equipamentos (um aro em perspectiva é largo e achatado).

### O anel e o amuleto, rodada 2 (`anel_amuleto/`)

**Propostas, nada no jogo, aguardando avaliação.** A rodada 1 (o anel achatado com a granada e o medalhão) **não foi
escolhida**: guardada inteira em `anel_amuleto/rodada1/` (as fontes, os PNGs e o gerador `joias_rodada1.py`).

- **A referência:** a prancha de anéis do Jean, guardada em `ferramentas/arte/referencias/aneis/prancha-aneis-jean.png`
  e documentada na skill (`.claude/skills/arte-itens-fenda/referencias-aneis.md`: o ângulo preferido para os anéis, a
  construção separada dos efeitos, sem regra de cor, gema ou poder), e o sample de um aro liso de ouro que ele mandou
  durante o trabalho (o acabamento).
- **O anel:** o aro em pé, de três quartos e inclinado, com a abertura elíptica em diagonal; modelado como um cilindro
  curto (a face de fora, a de dentro e as duas bordas projetadas, cada pixel com a superfície mais perto: a perspectiva
  e a espessura coerentes em todo tamanho), `anel_amuleto/auxiliares/aro.py <N>`. No ouro das moedas aprovadas (claro
  e saturado como o sample), a face de fora em poucos tons com o chanfro claro nas bordas e o meio mais fundo, a face de
  dentro laranja escura, o reflexo agrupado. Sem pedra nem decoração (o anel básico). As rodadas do desenho: o eixo
  virado demais para o lado (uma fresta, um bracelete grosso), depois a luz barrenta; o sample trouxe o ouro e o
  chanfro. Camadas: dentro, fora, borda, brilho, contorno.
- **O amuleto:** a gema violeta alongada (um cabochão) num engaste de latão contido, a argola encaixada no alto e o
  mesmo cordão de couro em gota da rodada 1 passando por ela. A gema em poucos planos (a luz em cima à esquerda, o
  violeta fundo embaixo, a beira mais funda), o reflexo agrupado e um brilho de dentro do lado oposto; o contraste
  pedra × metal do placeholder, sem halo nem runa. Camadas: cordao, argola, engaste, pedra, brilho, contorno.
- **Tamanhos:** 32, 40 e 48 da mesma construção; o 64 é o 32 ampliado 2×. Fontes em `anel_amuleto/fontes/anel/` e
  `amuleto/`, pelo `pintar.lua` (0 diferentes, 0 fora da tela); o composto do editor confere (`soma.lua`); @2x exatos.
- **As fotos (1920×945, os mesmos dados):** produção × anterior × nova (`ROTULO=nova`; `SO_PROPOSTA=1 ROTULO=anterior
  PASTA=anel_amuleto/rodada1/proposta`); o laço do saque do roteiro passou a seguir `ROTULO`, `SO_ATUAL` e
  `SO_PROPOSTA`. Folha `anel_amuleto/anel_amuleto-no-jogo.png` e prancha `anel_amuleto/prancha-carvao.png`.
- **O alcance segue o da rodada 1:** os compartilhamentos atuais (Anel, Sinete, Aro e o Anel do Último Rei; Amuleto,
  Talismã, Pingente e Medalhão; os vazios com a mesma imagem), sem mudar os dados.

### O anel, rodada 3 (`anel_amuleto/`); o amuleto da rodada 2 aprovado

- **O amuleto da rodada 2 foi aprovado** (a gema violeta no engaste de latão); as fontes e os PNGs dele
  (`anel_amuleto/fontes/amuleto/`, `proposta/amuleto-*`) ficam como estão, sem retoque, à espera da integração.
- **O anel da rodada 2 não foi escolhido** (a abertura inclinada para o lado oposto ao da referência): guardado em
  `anel_amuleto/rodada2/` (os PNGs, as fontes, `aro_rodada2.py`, a folha e a prancha dela).
- **As referências:** os PNGs originais em `ferramentas/arte/referencias/aneis/`, com a hierarquia na skill
  (`referencias-aneis.md`): a principal é `sample (2).png` (a perspectiva, a inclinação, a abertura e a espessura); as
  secundárias são as pranchas do mesmo artista (o metal e o acabamento).
- **A construção (rodada 3):** o mesmo modelo do aro (um cilindro curto), com o ângulo e as proporções achados pela
  sobreposição com a referência principal reduzida a 32 (`auxiliares/ajuste_aro.py`: a silhueta e o vão sobrepõem
  0,93 e 0,97; das duas famílias de eixo com a mesma silhueta, ficou a que põe as faces como na referência: a de fora
  larga em cima e à esquerda, a de dentro embaixo e à direita). A parede afinada à mão (1,4), porque na referência a
  borda é uma linha fina: a correspondência visual decidiu, não a nota. Comparação lado a lado na mesma escala:
  `anel_amuleto/anel-referencia-r2-r3.png` (ampliado e em tamanho real).
- **O metal:** o ouro das moedas aprovadas em poucos planos largos (a face de fora em três, o chanfro de 1 px nas
  beiras, a face de dentro escura em cima e clara embaixo, as bordas claras, o reflexo agrupado), limpo face a face
  pelo `limpar` do `pixel_comum`. **O ornamento leve** (o Jean liberou durante o trabalho): um ziguezague gravado no meio
  da face de fora, que acompanha a curva da faixa (feito numa segunda passada, para a linha sair contínua). A versão lisa
  (`aro.py <N> liso`) ficou como alternativa em `anel_amuleto/rodada3_liso/`.
- **Tamanhos:** o 32 resolvido primeiro; 40 e 48 da mesma construção; 64 = 32 ×2. Fontes em `anel_amuleto/fontes/anel/`
  (dentro, fora, gravacao, borda, brilho, contorno), pelo `pintar.lua`; o composto do editor confere (`soma.lua`); @2x
  exatos.
- **As fotos (1920×945):** produção × rodada 2 × rodada 3 na ficha, no Inventário (com o anel vazio) e no saque
  (`anel_amuleto/anel_amuleto-no-jogo.png`; `fotografar.mjs anel_amuleto` com `SO_PROPOSTA=1 ROTULO=rodada3`) e a
  prancha `anel_amuleto/prancha-carvao.png`.
- **Integrados na 1.140.0, sem retoque** (aprovados no `9ae59a9`): o anel da rodada 3 (com o ziguezague) e o amuleto
  violeta da rodada 2. As fontes foram para `ferramentas/arte/aseprite/anel/` e `amuleto/`; os 16 arquivos do jogo são
  idênticos, byte a byte, aos da proposta; o 64 é o 32 ×2 (`DERIVADOS`). Os compartilhamentos seguem (o anel: Anel,
  Sinete, Aro, o Anel do Último Rei; o amuleto: Amuleto, Talismã, Pingente, Medalhão) e os vazios acompanham. Conferido
  a 1920×945 com os arquivos do jogo (`anel_amuleto/capturas/no-jogo-1.140.0-*`): a ficha e o Inventário idênticos às
  fotos aprovadas; e, com os saves temporários (`auxiliares/equipar.mjs`, `capturas/integracao/`): um anel achado com o
  Anel 1 ocupado e o Anel 2 vazio, a comparação do saque e "Equipar no Anel 2 (vazio)" (os dois espaços ocupados na
  ficha e no Inventário), e um Talismã equipado pela comparação. Sem erro no console. A alternativa lisa fica como
  histórico.

## A Sandália e o Chapéu Pontudo do Mago (`sandalia_chapeu/`)

**Pedido de Jean (19/10/2026):** o par seguinte da conferência dos equipamentos (plano 23, seção 1.2.1), uma peça por
vez, só no protótipo, com a skill `arte-itens-fenda` e as fontes no Aseprite pelo MCP. Referências do conjunto: o capuz
de tecido, a luva de seda, o manto e a calça de viagem aprovados; os placeholders não são copiados. **Nada no jogo.**

**Antes de desenhar:**
- **Os dados:** a Sandália (`("Sandália", "f", "sandalia")`) é a única base dos pés do Mago; o Chapéu Pontudo
  (`("Chapéu Pontudo", "m", "chapeu")`) é uma das três cabeças (com o Capuz e o Diadema). Os materiais de tecido (Puído,
  de Linho, de Lã Negra, Bordado, Rúnico) só mudam o nome e a força. Nenhum único usa estes desenhos.
- **Hoje:** os dois não têm papel em `Icones`; o jogo mostra os sprites 16×16 ampliados (`S.chapeu` e `S.sandalia`, a
  bota recolorida). Nenhum outro papel (símbolo, habilidade, estado, retrato) usa esses sprites; os espaços vazios da
  cabeça e dos pés são do elmo e das botas de ferro (`VAZIO`) e não mudam.
- **Os tamanhos:** 32 na ficha e nas dicas, 40 no corpo e na mochila do Inventário, 48 no "você usa" do saque, 64 no
  cartão do saque.

**A construção** (`auxiliares/mago.py`: as medidas no quadro de 32, a mesma em 32, 40 e 48; o 64 é o 32 ×2):
- **A Sandália:** de lado e um pouco de cima, com a ponta à esquerda (como as botas de couro). A sola grossa de couro (a
  rampa das botas aprovadas), com a palmilha clara aparecendo por cima. As tiras formam a gaiola do pé e se prendem nas
  beiras da sola: a alça dos dedos, a do peito do pé (cada uma sobe da beira de perto, passa por cima e desce na de
  longe, a perna de trás mais escura), as duas que sobem até o anel do tornozelo (da frente e de trás do calcanhar) e o
  anel. Por dentro das alças e do anel aparece o fundo: o espaço do pé, vazio. Um laço de linho cru (o das faixas da
  calça) fecha o anel. Camadas: sola, palmilha, tiras, no, contorno.
- **O Chapéu Pontudo:** de frente e um pouco de cima. A aba larga em perspectiva (a elipse, com a beira da frente
  caindo um pouco à direita e a espessura embaixo; a parte de trás mais escura), a copa de lã (a rampa do capuz de
  tecido) em cone, com a luz da esquerda em faixas pela posição através da copa, subindo inclinada e tombando a ponta
  para a direita; o vinco onde o pano dobra e duas dobras descendo; a fita de linho cru na base, curvando com a elipse.
  Sem estrela nem brilho. Camadas: aba, copa, dobras, fita, contorno.
- **Rodadas descartadas da sandália (só na bancada, sem arquivo):** a vista de três quartos com o pé em perspectiva
  achatava a palmilha e as tiras viravam um bloco; a vista de cima (a sola inteira) lia como palmilha solta. A de lado
  com a gaiola foi a que mostrou o vazio do pé no 32.

**O Aseprite (pelo MCP):** as listas de cada camada (`previa/<peça>/<N>/listas/`) pintadas pelo `pintar.lua` num
`execute_script` (0 diferenças na releitura, 0 fora da tela), salvas em `fontes/<peça>/<peça>-<N>.aseprite`. Reabertas,
o código do composto (`bandagem_pocao/auxiliares/soma.lua`) é igual ao dos PNGs exportados pelo
`exportar_aseprite.py <peça> sandalia_chapeu/proposta --fontes=sandalia_chapeu/fontes` e ao da prévia (`soma.py`), nos
seis. Os @2x são a duplicação exata e o 64 é o 32 ×2 (feito à parte, porque `DERIVADOS` do exportador só ganha as
duas peças na integração).

**As fotos (1920×945, `fotografar.mjs sandalia_chapeu` e `sandalia_chapeu_saque_chapeu`):**
- `sandalia_chapeu-no-jogo.png`: atual × proposta na ficha (32), no Inventário (40) e nos cartões do saque de cada um
  (64 e 48), com os mesmos dados; sem erro no console.
- `conjunto-mago-32.png`: o conjunto de tecido lado a lado em 32 (tamanho real e a 3×); `prancha-carvao.png`: os tamanhos
  das duas peças em 1×, com as aprovadas ao lado.
- **A cena da ficha:** o `tutorial` com `CLASSE=mago` e `VESTIR` (o Chapéu, o Manto, a Calça, a Sandália e a Luva de
  Seda). A `capela` não aplica o `VESTIR` (ela veste pelo `dev.vestir` com o sorteio fixo): no lote da calça e do manto,
  as duas peças apareceram porque o sorteio já as dava.

**Para a avaliação:**
- **O que melhorou:** as duas peças ganham construção e material do conjunto; o chapéu se lê de longe pela silhueta
  (a aba e a ponta tombada) e combina com o capuz e o manto; a sandália mostra a sola, a espessura, as tiras e o vazio.
- **O que pode pedir ajuste:** a sandália é baixa e larga, e no 32 da ficha tem menos massa que as peças vizinhas; o
  anel do tornozelo vira uma faixa escura no 32 (a abertura só aparece a partir do 40). Ela é de couro (o material de
  uma sandália de viagem), embora os nomes venham dos materiais de tecido ("Sandália de Lã Negra").
- **Para a integração (só depois da aprovação):** o papel `sandalia` e `chapeu` em `ITEM` e `TAMANHOS`, as fontes em
  `ferramentas/arte/aseprite/`, `DERIVADOS` com o 64 = 32 ×2, `exportar_aseprite.py --conferir`.

### O Chapéu Pontudo no jogo (1.141.0) e a Sandália, rodada 2 (`sandalia_chapeu/`)

**Decisão de Jean (19/10/2026):** o Chapéu Pontudo do `b361a47` aprovado sem retoque e integrado na 1.141.0 (`0235c25`;
fotos com os arquivos do jogo em `capturas/integracao/`). A Sandália da rodada 1 foi recusada: ficou quase de perfil,
as tiras viraram arcos verticais e o conjunto parecia uma armação sobre a sola.

**A rodada 1 guardada** em `sandalia_chapeu/rodada1/` (a proposta, as fontes, a prévia e as fotos dela). Para refazer as
fotos dela: `PASTA=sandalia_chapeu/rodada1/proposta ROTULO=rodada1 SO_PROPOSTA=1 fotografar.mjs sandalia_r2`.

**A rodada 2** (`auxiliares/sandalia_par.py`; proposta em `rodada2/`), pela referência do Jean
(`ferramentas/arte/referencias/botas/`, a imagem gerada que ele mandou; a origem não foi informada): o par de sandálias
em três quartos, visto um pouco de cima, com a ponta embaixo à esquerda e o calcanhar em cima à direita.
- **Uma sandália primeiro** (`rodada2/previa/<N>/sandalia_uma_final_<N>.png`), por formas no quadro de 32:
  - a palmilha clara (o couro cru) com o contorno de um pé, larga nos dedos e redonda no calcanhar;
  - a sola baixa, com a espessura embaixo e a beira de baixo mais escura;
  - as duas tiras do pé, largas e inclinadas: cada uma sobe da beira de perto (meio-tom), passa por cima do espaço do pé
    (o alto, claro) e desce na beira de longe (escura), uma curva só; a sombra de cada tira cai na palmilha à direita;
  - o tornozelo: a tira larga em volta (a metade de longe escura, a de perto clara em cima), presa pela frente e pelo
    calcanhar, com o vão por onde a perna entraria (o calcanhar da palmilha aparece lá embaixo).
- **O par:** a de trás é a mesma, deslocada para cima e para a esquerda e um tom mais escura; o contorno da da frente
  passa por cima dela e separa as duas. Vazias, sem pé.
- **Da referência ficou:** a palmilha visível, a sola baixa com espessura, as tiras largas e inclinadas, o tornozelo alto e
  a separação entre as duas. **Não ficou:** o vermelho (o couro é o das botas aprovadas) e parte das tiras (no 32,
  duas no pé e uma no tornozelo).
- **Tentativas descartadas (só na bancada):** o modelo em 3D com as tiras em arco levantava as tiras e cobria a
  palmilha, e as peças viravam um bloco; as tiras como paralelogramos retos viravam dentes e o tornozelo, uma caixa.
- **Tamanhos:** a mesma construção em 32, 40 e 48 (as medidas no quadro de 32); 64 = 32 ×2. Camadas: tras_sola,
  tras_palmilha, tras_tiras, frente_sola, frente_palmilha, frente_tiras, contorno.
- **O Aseprite (pelo MCP):** as listas pintadas pelo `pintar.lua` (0 diferenças na releitura, 0 fora da tela), fontes em
  `rodada2/fontes/sandalia/`; reabertas, o composto do editor (`soma.lua`) é igual aos PNGs exportados pelo
  `exportar_aseprite.py sandalia rodada2/proposta --fontes=rodada2/fontes` e à prévia; @2x exatos; 64 = 32 ×2.

**As fotos (1920×945, `fotografar.mjs sandalia_r2`):** atual (o jogo, com o chapéu integrado e o sprite da sandália) ×
rodada 1 × rodada 2 na ficha, no Inventário e no saque, com os mesmos dados (`sandalia-r2-no-jogo.png`;
`capturas/r2/`); o conjunto do Mago em tamanho real e a 3× (`conjunto-mago-32.png`); a prancha da rodada 2
(`rodada2/prancha-carvao.png`). Sem erro no console.

**Para a avaliação:** o par ocupa o espaço como as botas vizinhas e se lê como sandálias nos três lugares; no 32, as
tiras e o vão do tornozelo são simplificados, e a de trás aparece sobretudo pela ponta e pelo tornozelo.

**Os nomes dos materiais (registrado, sem mudar regra):** a Sandália recebe os materiais de tecido
(`MATERIAIS_TECIDO`: "Sandália de Lã Negra", "Sandália de Linho", "Sandália Bordada"...), mas o desenho é de couro.
Fica para decidir se a base ganha materiais próprios ou se os nomes ficam.

**Integrada na 1.142.0, sem retoque** (aprovada no `b9ec78a`): a Sandália da rodada 2. As fontes foram para
`ferramentas/arte/aseprite/sandalia/`; os 8 arquivos do jogo são idênticos, byte a byte, aos da proposta; o 64 é o 32 ×2
(`DERIVADOS`). Conferida a 1920×945 com os arquivos do jogo e os saves temporários (`sandalia_chapeu/auxiliares/
equipar.mjs`; `capturas/integracao/no-jogo-1.142.0-*`): o saque, equipar (os atributos mudam como a comparação do
cartão) e guardar (nada muda no corpo), a ficha e o Inventário. Os nomes e materiais ficaram como estão (pendência de
nomenclatura no plano 23).

## A Besta Leve e o Diadema (`besta_diadema/`)

**Pedido de Jean (19/10/2026):** o par seguinte, uma peça por vez, só no protótipo, com a skill `arte-itens-fenda` e as
fontes no Aseprite pelo MCP. Os atuais (os sprites 16×16) são placeholders e não foram copiados. **Nada no jogo.**

**Antes de desenhar (os dados e os usos):**
- **A Besta Leve** (`("Besta Leve", "f", "besta")`): uma das quatro armas do Arqueiro, com os materiais de metal
  (`MATERIAIS`: Enferrujada, de Ferro, de Aço, Temperada, Rúnica). Nenhum único; o sprite `besta` não tem outro papel;
  a arma vazia é a espada de ferro (`VAZIO`).
- **O Diadema** (`("Diadema", "m", "coroa")`): uma das três cabeças do Mago, com os materiais de tecido nos nomes. O
  desenho `coroa` vale também para o único **Coroa dos Afogados** (base Diadema, lendário, `classe=None`, +Vida,
  regeneração e Defesa; "Achada na cabeça de um rei no fundo do pântano. Ele não estava morto."). O sprite `coroa` é
  ainda o símbolo da reputação (`S("coroa")` no Inventário; `Icones.miudo("coroa")` nos ganhos de contrato, sem papel em
  `MIUDO`): um papel em `ITEM` não o muda. A cabeça vazia é o elmo de ferro.
- **Tamanhos:** 32 na ficha, 40 no Inventário, 48 no "você usa" do saque, 64 no cartão.

**A construção** (`auxiliares/desenho.py`; as medidas no quadro de 32, a mesma em 32, 40 e 48; o 64 é o 32 ×2):
- **A Besta Leve:** deitada, vista de cima, na diagonal das armas aprovadas (a soleira embaixo à esquerda, a frente em
  cima à direita). A coronha de madeira (o teixo do arco aprovado), larga na soleira e estreita na frente, com a face
  clara em cima, a espessura embaixo e o sulco do virote; o arco de aço atravessado na frente, perpendicular à coronha,
  com as pontas puxadas para trás; a corda (a do arco) das pontas até a noz de latão no meio da coronha: o V da besta
  armada, que a separa do arco (uma curva com a corda reta), do cajado e do martelo (sem o arco atravessado); a
  empunhadura de couro atrás da noz, a alavanca do gatilho por baixo e o estribo de aço na ponta. Sem virote (o sulco
  basta e o 32 fica mais limpo). Camadas: coronha, empunhadura, corda, arco, metal, contorno.
- **O Diadema:** de frente e um pouco de cima. O aro de latão (o do broche do manto) numa chapa fina e baixa, a elipse
  larga: a face de fora na frente, clara na beira de cima, com o reflexo à esquerda, e o lado de trás mais escuro; o
  fundo aparece pelo meio. Na frente, a ponta: uma placa estreita que sobe acima da borda de trás, com a gema violeta (a
  do amuleto aprovado) num engaste. Camadas: aro, placa, gema, contorno.
- **Rodadas descartadas do diadema (só na bancada):** com a chapa alta e o aro visto muito de cima, ele virava uma
  bandeja ou uma máscara; a camada da face de dentro saiu vazia com a chapa fina e foi tirada. As prévias de
  `previa/diadema/<N>/listas/` ainda têm um `dentro.lua` vazio dessa tentativa (a remoção ficou para o Jean).

**O Aseprite (pelo MCP):** as listas pintadas pelo `pintar.lua` (0 diferenças na releitura, 0 fora da tela), salvas em
`fontes/<peça>/<peça>-<N>.aseprite`; reabertas, o composto (`soma.lua`) é igual aos PNGs exportados pelo
`exportar_aseprite.py <peça> besta_diadema/proposta --fontes=besta_diadema/fontes` e à prévia, nos seis; @2x exatos; o
64 é o 32 ×2.

**As fotos (1920×945, `fotografar.mjs besta`, `diadema` e `coroa_afogados`):** atual × proposta com os mesmos dados
(`besta_diadema-no-jogo.png`): o Arqueiro com a besta na mão (o `tutorial` com `ARMA=besta`) e o Mago com o diadema
(`VESTIR`) na ficha (32) e no Inventário (40); os cartões do saque (64 e 48) da besta, do diadema e da Coroa dos
Afogados. Sem erro no console. O `fotografar.mjs` aceita agora `peca` num papel (o desenho `coroa` com o arquivo
`diadema`). As fileiras em tamanho real: `fileira-arqueiro-32.png` (a besta com o arco, a aljava, o capuz, o gibão e
o machado) e `fileira-mago-32.png` (o diadema com o Chapéu Pontudo, o capuz, o amuleto, o anel e o manto);
`prancha-carvao.png`, os quatro tamanhos das duas.

**Para a avaliação:**
- **A besta:** se lê como besta no 32 pelo arco atravessado e pelo V da corda, com a madeira e o couro do arco aprovado.
- **O diadema:** se lê como aro com a ponta e a gema, mas tem menos massa que os vizinhos (a chapa fina ocupa pouca área
  do espaço); na ficha fica pequeno ao lado do chapéu.
- **A Coroa dos Afogados** usa o mesmo desenho na proposta; a arte própria dela fica registrada como necessidade futura.
- **Para a integração (só depois da aprovação):** os papéis `besta` e `coroa` (→ `diadema`) em `ITEM` e `TAMANHOS`,
  as fontes em `ferramentas/arte/aseprite/`, `DERIVADOS` com o 64 = 32 ×2.

**A Besta Leve integrada na 1.143.0, sem retoque** (aprovada no `63a7a85`): as fontes foram para
`ferramentas/arte/aseprite/besta/`; os 8 arquivos do jogo são idênticos, byte a byte, aos da proposta; o 64 é o 32 ×2
(`DERIVADOS`). Conferida com os arquivos do jogo e os saves temporários (`capturas/integracao/no-jogo-1.143.0-*`): o
saque, equipar (os atributos mudam como a comparação do cartão), guardar, a ficha e o Inventário.

### O Diadema, rodada 2 (`besta_diadema/`)

**Pedido de Jean (19/10/2026):** o latão e a gema violeta funcionam, mas a apresentação da rodada 1 ficou achatada: no
tamanho real, uma elipse dourada com um ponto central, e a frente da peça pouco visível. Mostrar mais a face da frente e
menos o aro visto de cima, ganhar presença pela apresentação e pelos planos, sem engrossar a chapa toda nem virar uma
coroa grande. Durante o trabalho, o Jean mandou uma imagem de referência para o ângulo ("mais assim talvez?"): uma
coroa vista de frente, com a faixa da frente grande e a borda de cima aparecendo pouco.

**A rodada 1 guardada** em `besta_diadema/diadema_r1/` (a proposta, as fontes, a prévia e o script daquela versão,
`auxiliares/desenho_rodada1.py`, que a reproduz pixel a pixel).

**A rodada 2** (`auxiliares/desenho.py`, a mesma construção em 32, 40 e 48; o 64 é o 32 ×2): de frente, um pouco de
cima. A faixa de latão é um cilindro baixo visto quase de frente (a elipse de cima com pouca altura): a face de fora
em curva, em duas faixas de luz (clara à esquerda), com a beira de cima acesa e o reflexo à esquerda, a beira de baixo
na sombra; por cima dela, pela boca, a face de dentro do lado de trás, escura (uma rampa própria, o latão na sombra), e
uma fresta do vão no 32; a borda de trás, uma linha fina. Na frente, a ponta estreita sobe da faixa com a gema violeta
no engaste. Uma ponta só e a chapa fina: a presença vem da face da frente, não de uma chapa mais grossa. Camadas: aro,
placa, gema, contorno. **Tentativas da bancada:** as contas de latão dos lados da ponta sumiam no 32 e saíram; com a face
de dentro no tom do latão, a peça parecia uma torta, e a sombra passou para a rampa escura.

**O Aseprite (pelo MCP):** as listas pintadas pelo `pintar.lua` (0 diferenças na releitura, 0 fora da tela), em
`fontes/diadema/`; o composto do editor (`soma.lua`) é igual aos PNGs exportados e à prévia nos três; @2x exatos; o
64 é o 32 ×2.

**As fotos (1920×945, `fotografar.mjs diadema` e `coroa_afogados`, com `ROTULO=antes PASTA=besta_diadema/diadema_r1/
proposta` e `ROTULO=depois`):** atual (o sprite) × antes × depois com os mesmos dados (`diadema-r2-no-jogo.png`): a
ficha (32), o Inventário (40), o saque do Diadema e o da Coroa dos Afogados (64 e 48). Sem erro no console. O símbolo da
reputação na ficha é igual nas três (o sprite `coroa`, fora do mapa de equipamento). A fileira do Mago em tamanho real
(`fileira-mago-32.png`, as duas rodadas com o Chapéu Pontudo, o capuz, o amuleto, o anel e o manto) e a prancha dos
tamanhos (`diadema-prancha-carvao.png`).

**Para a avaliação:** a face da frente aparece e a peça ocupa mais o espaço; continua mais larga que alta (é um aro), e
no 32 o oco de dentro lê como sombra.

**O Diadema integrado na 1.144.0, sem retoque** (a rodada 2, aprovada no `731ab5c`): as fontes foram para
`ferramentas/arte/aseprite/diadema/`; os 8 arquivos do jogo são idênticos, byte a byte, aos da proposta; o 64 é o 32 ×2
(`DERIVADOS`). O papel é `coroa` → `diadema` (o Diadema e, por ora, a Coroa dos Afogados); a reputação continua com o
sprite. Conferido com os arquivos do jogo e os saves temporários (`capturas/integracao/no-jogo-1.144.0-*`).

## O remake do ferro, 1: a espada e a maça (`espada_maca/`)

**Pedido de Jean (19/10/2026):** começar o remake da família de ferro (placeholders, reduções da arte pintada) pela
espada e pela maça, uma peça por vez, só no protótipo, com a skill `arte-itens-fenda` e o Aseprite pelo MCP. O escudo e
o machado aprovados são as referências de material, luz, contorno e acabamento; os atuais não precisam ser reproduzidos.
Sem efeitos mágicos. Primeiro o 32 e o 64 (= 32 ×2); os 40 e 48 depois da aprovação da forma. **Nada no jogo.**

**Os usos (antes de desenhar):**
- `espada`: as bases Espada e Montante (sem únicos); a silhueta apagada da arma vazia de todas as classes (`VAZIO`); o
  comando Atacar do Guerreiro na roda da luta (`ACAO`: o `icone_ataque` da classe é sempre a espada, qualquer que seja
  a arma). O ícone do atributo Ataque é o `attr-ataque` (aprovado, outro arquivo) e fica como está; o sprite 16×16
  `espada` (estados, talentos, habilidades, selos de atributo) também é outro.
- `maca`: só a base Maça.

**A construção** (`auxiliares/desenho.py`): na diagonal da família (o pomo embaixo à esquerda, a ponta em cima à
direita), as medidas num sistema que segue a arma (u ao longo do eixo, v através; a metade de cima na luz). O ferro do
machado (o cinza neutro), o latão do escudo, o freixo do cabo do machado, o couro do arco.
- **A espada:** a lâmina larga de dois gumes em dois planos (o de cima claro, com o gume aceso; o de baixo na sombra),
  o sulco no plano claro, a ponta afilada e acesa, o talão junto da guarda; a guarda de latão reta, com as pontas
  curvadas para a lâmina; a empunhadura de couro com as voltas; o pomo de latão redondo. Camadas: empunhadura, pomo,
  guarda, lamina, contorno.
- **A maça:** a cabeça de aço em bulbo (um ovo ao longo do eixo), dividida em três gomos pelas aletas (a da frente clara
  no meio, a de cima na luz, a de baixo na sombra), com os vãos escuros recortando a ponta de cima em dentes curtos e
  uma ponta curta no alto; o colar de aço; o cabo de freixo; a empunhadura de couro; o botão de latão no pé. Camadas:
  cabo, empunhadura, cabeca, contorno.
- **Tentativas descartadas (só na bancada):** a espada com a guarda de aço e o plano de baixo escuro perdia presença (a
  guarda sumia, a lâmina afinava); a maça com as aletas de perfil saindo do miolo parecia uma pá e, com três aletas
  largas, um machado de dois gumes; com cinco gomos, um garfo (no 32 os vãos ocupavam quase metade da cabeça).
- **Um cuidado do método:** o `limpar` do `pixel_comum` apaga linhas diagonais de 1 pixel (cada pixel fica cercado por
  outro tom); o sulco, os vãos das aletas e as voltas da empunhadura vão em `fixo`.

**O Aseprite (pelo MCP):** as listas do 32 pintadas pelo `pintar.lua` (0 diferenças na releitura, 0 fora da tela), em
`fontes/<peça>/<peça>-32.aseprite`; reabertas, o composto (`soma.lua`) é igual ao PNG exportado pelo
`exportar_aseprite.py <peça> espada_maca/proposta --fontes=espada_maca/fontes` e à prévia; o 64 é o 32 ×2; @2x exatos.

**As fotos (1920×945, `fotografar.mjs espada`, `espada_luta` e `maca`):** atual × proposta com os mesmos dados
(`espada_maca-no-jogo.png`): o Guerreiro com a espada e com a maça na mão (o `tutorial` com `ARMA`), a ficha (32), o
Inventário (40), o saque (64 e 48) e a roda da luta com o Atacar. Sem erro no console. Como a proposta só tem o 32 e o
64, a página trata as duas peças com os tamanhos [32, 64] (`papel_tamanhos`): o Inventário mostra o 32 (como o jogo faz
com um tamanho sem arquivo) e o "você usa" do saque reduz o 64 para 48 no navegador; os dois se resolvem com os
intermediários. A fileira em tamanho real (`fileira-guerreiro-32.png`: a espada e a maça com o machado, o escudo, o
ícone de Ataque e os placeholders atuais) e a prancha (`prancha-carvao.png`, com as silhuetas).

**Para a avaliação:**
- **A espada:** presença no tamanho real (a lâmina larga, a guarda de latão), coerente com o escudo e o machado; fica
  mais larga e mais curta que o ícone de Ataque, que continua o mesmo.
- **A maça:** se separa do machado (sem lâmina de um lado) e do martelo (sem bloco atravessado), mas no 32 a cabeça em
  bulbo com os gomos ficou estreita e pode ler como lança ou tocha; a leitura imediata ainda não está garantida.

### A espada e a maça, rodada 2 (`espada_maca/`)

**Pedidos de Jean (19/10/2026):**
- **A maça:** recuperar peso e reconhecimento. A da rodada 1 tinha a cabeça estreita e alongada, com uma faixa clara
  que lembrava uma ponta metálica ou lâmina. O placeholder antigo é a referência da proporção entre cabeça e cabo e da
  massa arredondada (sem reduzir nem copiar a pintura); o escudo e o machado, do material, da luz e do acabamento. Volume
  mais redondo, aletas ou saliências curtas e bem separadas, a luz acompanhando o volume; poucos elementos claros.
- **A espada:** refeita também (o complemento substitui a aprovação e o pedido de tamanhos da rodada 1). A lâmina da
  rodada 1, larga na base e afinando por um trecho longo, lembrava uma cunha. Pela referência que o Jean pôs em
  `ferramentas/arte/referencias/espada/` (a hierarquia no `LEIA-ME.md` de lá): uma espada básica com o corpo alongado e
  regular, os gumes contínuos e a ponta aguda de formação clara; sem ponta cortada ou arredondada, sem uma faixa clara
  que engula a face, sem espessura demais junto da guarda. Sem efeitos.
- Só o 32 e o 64 (= 32 ×2); os intermediários depois da aprovação. Nada no jogo.

**A rodada 1 guardada** em `espada_maca/rodada1/` (a proposta, as fontes, a prévia, as fotos, as folhas e o script
daquela versão, `auxiliares/desenho_rodada1.py`, que a reproduz pixel a pixel).

**A rodada 2** (`auxiliares/desenho.py`):
- **A espada:** as proporções medidas na espada de aço da referência (a lâmina em cerca de 2/3 do comprimento, de
  largura constante, afinando só no último quarto até a ponta; a guarda com cerca de 1,6 vez a largura da lâmina; a
  empunhadura curta), adaptadas à grade de 32 (a lâmina um pouco mais larga que a da referência, para ter presença).
  Os planos: o de cima na luz, com o gume aceso; a aresta no meio; o de baixo um tom abaixo, o gume de baixo na sombra;
  a ponta acesa até o vértice. A guarda curta de latão (o do escudo), a empunhadura de couro com as voltas, o pomo de
  aço. Na bancada, o plano de cima saiu primeiro quase branco (a faixa que engole a face) e desceu um tom.
- **A maça:** o bulbo redondo (o raio perto do da bola do placeholder) com cinco aletas curtas e separadas (a da
  ponta, duas nos lados, duas embaixo, junto do cabo); o bulbo sombreado como esfera pela luz da família (faixas
  largas, o brilho agrupado em cima à esquerda), cada aleta no tom da direção para onde aponta, a junção com o bulbo
  escura; o colar, o cabo de freixo, a empunhadura de couro e o botão de latão.
- Camadas: a espada, empunhadura, pomo, guarda, lamina, contorno; a maça, cabo, empunhadura, cabeca, contorno.

**O Aseprite (pelo MCP):** as listas do 32 pintadas pelo `pintar.lua` (0 diferenças na releitura, 0 fora da tela), em
`fontes/<peça>/<peça>-32.aseprite`; o composto (`soma.lua`) é igual ao PNG exportado e à prévia; o 64 é o 32 ×2; @2x
exatos.

**As fotos e as folhas (1920×945, `fotografar.mjs espada`, `espada_luta` e `maca`, com `ROTULO=rodada2` e, para a
rodada 1, `PASTA=espada_maca/rodada1/proposta ROTULO=rodada1 SO_PROPOSTA=1`):**
- `espada-referencia-r1-r2.png`: a referência × a rodada 1 × a rodada 2, em tamanho real sobre o carvão e ampliadas na
  mesma escala, sem suavização;
- `espada-no-jogo.png`: atual × rodada 1 × rodada 2 na ficha (32), no saque (64 e 48) e no Atacar da luta (32);
- `maca-no-jogo.png`: atual × rodada 1 × rodada 2 na ficha, no Inventário e no saque;
- `fileira-guerreiro-32.png`: as três maças, as duas espadas, o escudo e o machado em tamanho real e a 3×;
  `prancha-carvao.png`, com as silhuetas. Sem erro no console.
- Como antes, a proposta só tem o 32 e o 64: o Inventário mostra o 32 e o "você usa" do saque reduz o 64 para 48.

**Para a avaliação:** a espada segue a construção da referência (a lâmina regular, a ponta formada) e fica mais fina e
mais comprida que a rodada 1; a maça recuperou a massa redonda do placeholder e lê como maça no 32, com as aletas
curtas no lugar dos espinhos.

### A ponta da espada e os tamanhos da maça (`espada_maca/`)

**Decisões de Jean (19/10/2026):** a maça da rodada 2 (`87c12eb`) está aprovada; o 32 e o 64 dela ficam sem retoque, e
faltam o 40 e o 48. Na espada, falta só a ponta: o corpo da lâmina terminava e sobrava um trecho fino, como uma agulha
(um biquinho acrescentado). Retocar o trecho final para os gumes convergirem continuamente até a extremidade, com os
planos do aço acompanhando, pela espada de aço de `espadasample.png`; o resto da espada (corpo, guarda, empunhadura,
pomo, paleta) fica. Durante o trabalho, o Jean pediu cuidado com a maça: as aletas (as pontinhas da cabeça) precisam
ter o mesmo formato em todos os tamanhos.

**A ponta (só o 32 e o 64 = 32 ×2; o 40 e o 48 da espada esperam a aprovação deste ajuste):**
- **Antes** (guardada em `espada_maca/rodada2_ponta_antiga/`: os PNGs e a fonte): a largura caía em rampa reta do começo
  da ponta até o vértice; no pixel, o corpo terminava e sobrava 1 px por um trecho comprido.
- **Uma tentativa na bancada:** o perfil curvo simétrico (cheio no começo, fechando rápido no fim) tirou a agulha, mas
  arredondou a ponta.
- **Depois** (`auxiliares/desenho.py`, a função `gumes`): como na referência, a ponta é assimétrica: o gume de cima
  segue quase reto até perto do fim e o de baixo sobe em curva até encontrá-lo, com o vértice um pouco acima do eixo; a
  ponta começa um pouco antes (30,0 em vez de 31,2) e vai até 36,8. Os planos seguem os gumes (o meio entre eles divide
  o plano claro do escuro; a aresta acompanha o meio e para antes do vértice); o vértice aceso.

**A maça em 40 e 48:** a mesma construção, mas o polígono das aletas que, na grade de 32, sai como um botão rombudo de
cerca de 2 pixels (o topo claro e 1 pixel escuro na base), sai pontudo e fino nas grades maiores, que desenham a forma
com mais fidelidade. Nos tamanhos maiores, a aleta é um botão retangular rombudo na proporção que o 32 mostra (cerca de 2
pixels de saliência e 2 a 3 de largura no 32) e a junção escura tem 1 pixel; o caminho do 32 ficou exatamente o
aprovado (o PNG e o código de conferência não mudaram).

**O Aseprite (pelo MCP):** a espada 32 e a maça 40 e 48 pintadas pelo `pintar.lua` (0 diferenças, 0 fora da tela); o
composto do editor é igual aos PNGs exportados e à prévia; a maça 32 e 64 são as aprovadas, byte a byte; @2x exatos; o
64 da espada é o 32 ×2.

**As fotos e as folhas (1920×945):**
- `espada-ponta-antes-depois.png`: a referência × antes × depois em tamanho real, a espada inteira ampliada na mesma
  escala e a ponta recortada e ampliada, sem suavização;
- `espada-ponta-no-jogo.png`: antes (`rodada2`) × depois (`ponta_nova`) no saque, no Atacar e na ficha
  (`fotografar.mjs espada` e `espada_luta`, `ROTULO=ponta_nova SO_PROPOSTA=1`);
- `maca-tamanhos-no-jogo.png`: atual × a maça com os quatro tamanhos no Inventário (40), no saque (64 e o 48 do "você
  usa") e na ficha (`fotografar.mjs maca_tamanhos`, `ROTULO=tamanhos SO_PROPOSTA=1`);
- `prancha-carvao.png`: a maça nos quatro tamanhos, a espada nova e a ponta antiga. Sem erro no console.

### A ponta da espada, terceira tentativa (`espada_maca/`)

**Pedido de Jean (19/10/2026):** a correção do `723cf8d` tirou a agulha, mas a extremidade ficou rombuda: o fio claro
terminava antes da ponta e deixava uma pequena "tampa" escura, e a lâmina parecia cortada. Uma ponta aguda formada
pela convergência contínua dos gumes, com os planos do aço acompanhando o fechamento, como na espada de aço de
`espadasample.png`; podendo reconstruir um trecho maior do fim da lâmina (sem ficar preso aos últimos pixels), sem a
agulha nem a ponta arredondada ou truncada; o resto da espada fica. Guardar a tentativa anterior e registrar o
diagnóstico e a solução, para a futura skill de espadas (que só vem depois de um resultado aprovado; isto ainda não é
regra).

**O histórico das pontas (todas em `espada_maca/`):**
1. `rodada2_ponta_antiga/` (a rodada 2, `87c12eb`): a largura em rampa reta até o vértice; no pixel, o corpo acabava e
   sobrava 1 px por um trecho comprido: a **agulha**.
2. `rodada2_ponta_r2/` (`723cf8d`): os gumes por fórmula (o de cima quase reto, o de baixo em curva). Na grade de 32 o
   resultado foi a **ponta rombuda**: o fio claro (o tom 8) parava uma linha antes do vértice, os dois últimos pixels
   eram do plano médio e do escuro (5 e 3), e o gume de baixo fechava junto com o de cima, deixando o fim largo.
3. A nova (`proposta/`): desenhada pixel a pixel no 32.

**O diagnóstico, pela leitura dos pixels da referência** (a espada de aço da direita de `espadasample.png`, 64 px):
- o **fio claro do gume de cima corre sem interrupção até o último pixel**, e o vértice é claro;
- o plano escuro de baixo é que se estreita e **acaba uma linha antes do vértice**; o plano médio some antes dele;
- o gume de cima segue reto; **o de baixo avança devagar** no fim (no 64, a borda de baixo fica parada por várias
  linhas), e é isso que fecha a lâmina contra o de cima, num trecho longo (cerca de um quarto da lâmina).
- O erro de forma e o de luz eram separáveis: a silhueta da ponta rombuda já fechava rápido demais (forma), e o fio
  parando antes do vértice com o pixel final escuro fazia a "tampa" (luz).

**A solução (no `auxiliares/desenho.py`, o bloco `PONTA` do 32):** as linhas 0 a 6 da lâmina refeitas. O corte da
lâmina no corpo é `# 8 8 5 3 3 #` (o fio de 2 px, o plano médio, o plano escuro). Na ponta a largura cai um pixel a cada
duas linhas (5, 4, 4, 3, 3, 2, 1): o gume de cima segue reto, o de baixo avança meio pixel por linha; o plano médio some
primeiro (8 8 5 3 → 8 8 3), o escuro acaba uma linha antes do vértice (8 3 → 8), e o vértice é o tom 8. O contorno vem
da regra comum (`contornar`), e a etapa da silhueta usa o mesmo desenho. Uma tentativa na bancada com o gume de baixo
parado por quatro linhas fazia a ponta parecer dobrar para cima; o fechamento de meio pixel por linha resolveu.

**O Aseprite (pelo MCP):** a fonte `fontes/espada/espada-32.aseprite` repintada pelo `pintar.lua` (0 diferenças, 0 fora
da tela); o composto do editor é igual ao PNG exportado e à prévia; o 64 é o 32 ×2; @2x exatos. A maça (os quatro
tamanhos) não mudou.

**As folhas (1920×945):**
- `espada-ponta3.png`: a referência × a agulha × a rombuda × a nova, em tamanho real sobre o carvão, a silhueta da
  ponta numa cor e a ponta com a luz, ampliadas sem suavização;
- `espada-ponta3-no-jogo.png`: a rombuda (as fotos `ponta_nova`) × a nova (`ponta3`) no saque, no Atacar e na ficha
  (`fotografar.mjs espada` e `espada_luta`, `ROTULO=ponta3 SO_PROPOSTA=1`). Sem erro no console.

O 40 e o 48 da espada esperam a aprovação desta ponta; quando vierem, o ajuste do 32 não se aplica a eles (o bloco
`PONTA` é só da grade de 32), e a ponta deles terá de seguir o mesmo diagnóstico.

### A ponta da espada, quarta forma (`espada_maca/`)

**Pedido de Jean (19/10/2026):** a ponta do `3962b93` é válida, mas diferente da referência: o fechamento ficou
deslocado para um lado, com uma mudança brusca de direção perto da extremidade. **Mudança de abordagem:** o pedido
substitui as receitas anteriores (manter um gume reto e fazer só o outro avançar), que levaram a outro formato. O alvo
é o fechamento visual da espada de aço de `espadasample.png`: os dois gumes convergindo de forma contínua para uma ponta
alinhada com a direção da lâmina, sem exigir simetria perfeita pixel a pixel. Resolver primeiro a forma (a silhueta numa
cor, com o eixo da lâmina numa camada auxiliar), depois o fio e os planos; conferir a espada inteira em tamanho real e
a ponta ampliada; o resto da espada e a maça intocados.

**A medição (antes de desenhar):**
- **O eixo:** no 32, o miolo da lâmina vai de `x = 29 − y` a `33 − y` em cada linha; o eixo passa em `x = 31 − y`
  (nas coordenadas das bordas, `x + y = 32`).
- **O desvio do vértice em relação ao eixo** (através da lâmina): a referência, −0,7 px no 64 (menos de meio pixel no
  32, quase no eixo); a agulha, 0; a rombuda, −0,35; a terceira (`3962b93`), **−1,06 px no 32**: era o deslocamento que
  o Jean viu.
- **O perfil dos gumes da referência no fim:** os dois andam juntos em direção ao eixo, em linha quase reta, por um
  comprimento de cerca de **duas vezes a meia largura** da lâmina (no 64, cerca de 7 px), o de baixo um pouco mais
  rápido só no último pixel. Um fechamento curto e simétrico, nem o longo nem o de um lado só.

**A solução (no `auxiliares/desenho.py`; o bloco `PONTA` da terceira tentativa saiu):**
- **A forma:** a lâmina é a faixa em torno do eixo, e no fechamento a meia largura cai em linha reta até zero no
  vértice, igual dos dois lados (`larg(u) = ML · (U1 − u) / LT`). Um estudo fora do script variou o comprimento do
  fechamento: com 3,5 a ponta acabava em 2 px (truncada); com 4,2 e 5, num pixel sobre o eixo; com um perfil curvo,
  arredondava. No script, uma varredura do comprimento (`LT`) e do vértice (`U1`) procurou as combinações que terminam
  num pixel sobre o eixo e cujas larguras descem sem degrau. Ficaram duas famílias, ambas com o vértice uma linha
  antes do da terceira tentativa (o Jean permitiu encurtar): **o fechamento curto** (larguras 1, 3, 4, 5; `LT` 3,6 a
  4,2), que deixava um degrau de 3 px no gume de cima perto do fim, e **o fechamento longo** (1, 2, 4, 4, 5; `LT` 4,4 a
  5,4). **Escolhido: o longo, `U1 = 36,2`, `LT = 4,6`.**
- **O fio e os planos:** no fechamento, os tons pela posição de cada pixel na sua linha (a lâmina é diagonal, e cada
  linha da grade é um corte dela, como o `8 8 5 3 3` do corpo): o fio claro junto do gume de cima até o vértice, o plano
  escuro junto do de baixo até a linha antes do vértice, o médio no meio quando cabe; o vértice no tom 8. Na primeira
  passada, os tons pela coordenada normalizada deixavam o plano escuro sumir três linhas antes e um tom intermediário
  solto.

**O Aseprite (pelo MCP):** a fonte `fontes/espada/espada-32.aseprite` repintada pelo `pintar.lua` (0 diferenças, 0 fora
da tela); o composto do editor é igual ao PNG exportado e à prévia; o 64 é o 32 ×2; @2x exatos. O estudo da forma fica
em `fontes/estudo/espada-32-eixo.aseprite`: a silhueta numa cor (camada `silhueta`) e o eixo da lâmina numa camada
auxiliar (`eixo`), separado da fonte que se exporta. A maça (os quatro tamanhos) não mudou.

**A prancha** (`espada-ponta4.png`): a referência × a anterior (`3962b93`) × a nova, a espada inteira em tamanho real
sobre o carvão, a silhueta da ponta numa cor com o eixo marcado e o acabamento, ampliados sem suavização. As fotos das
telas não foram repetidas nesta rodada.

**O histórico das pontas:** `rodada2_ponta_antiga/` (a agulha), `rodada2_ponta_r2/` (a rombuda, `723cf8d`),
`rodada2_ponta_r3/` (a terceira, `3962b93`, com o script daquela versão em `desenho_ponta_r3.py.txt`), `proposta/` (a
quarta). Para a futura skill de espadas, depois de um resultado aprovado: medir o eixo e o desvio do vértice; fechar os
dois gumes juntos; e tratar a forma (silhueta e eixo) separada da luz (o fio e os planos por linha).

### A espada em 40 e 48 (`espada_maca/`)

**Decisão de Jean (19/10/2026):** a espada do `0fcfe18` está aprovada; o 32 e o 64 ficam sem retoque; faltam o 40 e o
48, com as proporções, os materiais e a construção da lâmina, e a ponta com o fechamento aprovado (os gumes convergindo
continuamente, o vértice alinhado com a lâmina, os planos acompanhando), adaptando os pixels de cada grade sem repetir a
contagem do 32.

**A construção:** a mesma do 32, nas medidas do quadro de 32 (o comprimento do fechamento `LT` = 4,6, a mesma
proporção). Duas adaptações por grade:
- **O vértice (`U1`) por grade:** a posição exata do vértice muda onde a ponta cai nos pixels. A primeira geração do 40
  terminava com 2 pixels (achatada) e a do 48 saltava de 2 para 5 de largura (um degrau no gume de cima). Uma varredura
  da posição do vértice, com o comprimento fixo, escolheu em cada grade o valor que termina num pixel sobre o eixo e
  desce sem degrau, o mais perto do aprovado: 36,2 no 32 (o aprovado), 36,3 no 40 e 36,05 no 48. As larguras no fim:
  32, 1, 2, 4, 4, 5; 40 e 48, 1, 2, 4, 5, 6, 6, 7.
- **A luz por linha em toda a lâmina nos maiores:** a regra dos planos do corpo, escrita em medidas fixas, deixava o fio
  claro fino no 48 e o plano médio dominando (a lâmina opaca). No 40 e no 48, a lâmina toda usa a proporção do corte do
  32 (`8 8 5 3 3`: o fio em 2/5 da largura, o médio em 1/5, o escuro em 2/5), a mesma regra que já fazia o fechamento.
  O 32 ficou com a regra aprovada (o PNG e o código de conferência não mudaram).

**O Aseprite (pelo MCP):** o 40 e o 48 pintados pelo `pintar.lua` (0 diferenças, 0 fora da tela), em
`fontes/espada/`; o composto do editor é igual aos PNGs exportados e à prévia; @2x exatos; o 32 e o 64 são os aprovados,
e a maça (os quatro tamanhos) não mudou.

**As folhas:** `espada-tamanhos.png` (os quatro tamanhos ampliados e a ponta de cada grade); `espada-tamanhos-no-jogo.png`
(atual × a espada com os quatro tamanhos no Inventário, em 40, na comparação do saque, em 64 e 48, e na ficha;
`fotografar.mjs espada_tamanhos`, `ROTULO=tamanhos SO_PROPOSTA=1`). Sem erro no console.

**A espada e a maça integradas na 1.145.0, sem retoque** (a espada: o 32 e o 64 do `0fcfe18`, o 40 e o 48 do
`441787e`; a maça: a rodada 2 do `87c12eb`, o 40 e o 48 do `723cf8d`; os PNGs e as fontes do protótipo conferidos contra
esses commits antes da cópia). As fontes foram para `ferramentas/arte/aseprite/espada/` e `maca/`; os 16 arquivos do
jogo são idênticos, byte a byte, aos aprovados; o 64 é o 32 ×2 (`DERIVADOS`). O `familia_ferro.py` passa a deixá-las de
fora (detecta as fontes) e continua "tudo igual" para as peças que ainda gera. Conferido com os arquivos do jogo e os
saves temporários (`espada_maca/auxiliares/integracao.mjs` e `sandalia_chapeu/auxiliares/equipar.mjs`; fotos em
`espada_maca/capturas/integracao/`): a ficha (32), o Inventário (40), a arma tirada com dois cliques (a silhueta da
arma vazia, na ficha e no Inventário), o Atacar da luta, o saque (64 e 48), equipar e guardar.

## O remake do ferro, 2: o elmo e a cota (`elmo_cota/`)

**Pedido de Jean (19/10/2026):** depois da integração da espada e da maça, o próximo par, uma peça por vez, só no
protótipo, com a skill `arte-itens-fenda` e o Aseprite pelo MCP. O escudo, o machado e as armas novas como referências de
metal, luz, contorno e acabamento; os atuais (reduções da arte pintada) orientam o conceito, sem ser reproduzidos. O
elmo: silhueta reconhecível, a calota em volume, a abertura do rosto resolvida, o interior vazio, poucos planos, sem
ornamento de lendário. A cota: primeiro o volume (a gola, os ombros, as mangas, a barra); a malha em grupos que sigam o
volume, sem ruído uniforme nem tricô; couro e ferragens onde fizerem sentido. Só o 32 e o 64; nada no jogo.

**Os usos (antes de desenhar):**
- `elmo`: o Elmo, o Capacete e a Barbuta (nenhum único); a silhueta da cabeça vazia de todas as classes (`VAZIO`); o
  desenho de reserva de um item de cabeça sem base reconhecida (`ICONE_ESPACO` em `rpg/itens.py`).
- `cota` (o desenho `armadura` nos dados): a Cota de Malha, o Peitoral, a Couraça e a Brigantina (nenhum único); a
  silhueta do peito vazio de todas as classes; o desenho de reserva do peito.
- **A limitação:** os nomes das quatro bases do peito são de construções diferentes (malha; peitoral e couraça de placa;
  brigantina de placas rebitadas sob tecido). O desenho segue o conceito do atual (a cota de malha, o primeiro nome) e
  serve às quatro por ora; uma variante por base fica para o Jean decidir (os dados não mudaram).

**A construção** (`auxiliares/desenho.py`; as medidas no quadro de 32):
- **O elmo:** uma barbuta de ferro, de frente e um pouco virada para a esquerda: a calota arredondada, sombreada como
  um volume pela luz da família (faixas largas, o brilho só no alto à esquerda, a lateral que vira para trás na
  sombra), a crista no alto com a sombra ao lado, a faixa da testa de latão com três rebites, a borda de baixo contínua e
  um tom abaixo (a chapa virando para dentro), a abertura em T (o vão dos olhos sob a faixa e o vão do rosto descendo),
  escura, com a parede de dentro um pouco mais clara embaixo: o interior vazio. Camadas: calota, interior, faixa,
  contorno.
- **A cota:** de frente, o volume primeiro (a gola, os ombros, as mangas curtas abrindo, o corpo até a barra); a malha
  como anéis numa grade deslocada (o alto de cada anel um tom acima do volume, a base logo abaixo um tom abaixo, a cada
  2 px na fileira e meio passo ao lado na fileira seguinte), sobre a luz do volume (clara à esquerda, mais escura à
  direita, as mangas e os lados embaixo dos braços na sombra); a gola de couro com o vão escuro do pescoço, as barras
  de couro nos punhos e embaixo, o cinto de couro com a fivela de ferro. Camadas: malha, couro, ferragem, contorno.
- **Tentativas da bancada:** o primeiro elmo tinha um recorte embaixo, entre a frente e a nuca, que lia como pernas, e
  uma abertura pequena; a primeira malha, em faixas horizontais, lia como placas (lamelar), e foi trocada pelos anéis
  em grade deslocada. Os anéis e a crista vão em `fixo` (a limpeza apagaria os pontos isolados).

**O Aseprite (pelo MCP):** as listas do 32 pintadas pelo `pintar.lua` (0 diferenças, 0 fora da tela), em
`fontes/<peça>/<peça>-32.aseprite`; o composto do editor é igual ao PNG exportado e à prévia; o 64 é o 32 ×2; @2x exatos.

**As fotos e as folhas (1920×945, `fotografar.mjs elmo_cota` e `elmo_cota_saque_cota`):** atual × proposta com os mesmos
dados (`elmo_cota-no-jogo.png`): a ficha e o Inventário do Guerreiro com os dois vestidos (`VESTIR`, no `tutorial`), o
saque do elmo e o da cota (o Peitoral de Aço do Lobo, comparado com uma Couraça: a mesma imagem para as duas bases); a
fileira em tamanho real com o escudo, a espada, a maça, o machado e os atuais (`fileira-guerreiro-32.png`); a prancha.
Sem erro no console. Como só há o 32 e o 64, o Inventário mostra o 32 e o "você usa" do saque reduz o 64.

**Para a avaliação:** o elmo se lê como elmo já no 32 (a abertura em T e a faixa de latão); a cota se lê como camisa de
malha com couro, mas no 32 a malha fica fina, quase uma textura; e, por ser malha, representa menos bem o Peitoral, a
Couraça e a Brigantina.

### O capacete e o peito, rodada 2, pelas referências (`elmo_cota/`)

**Pedido de Jean (19/10/2026):** rever o elmo e o peito pelas referências que ele pôs em
`ferramentas/arte/referencias/capacete/` e `peitoral/`, uma peça por vez, começando pelo capacete; escolher uma referência
principal de construção para cada peça e registrar o que vem das secundárias, sem misturar perspectivas; o escudo e as
armas continuam orientando o acabamento. O capacete do `6d5c8fa` não foi aprovado: a parte de baixo parecia um bloco, a
abertura em T parecia desenhada na superfície e a faixa de latão ficava rígida atravessando a peça ("reconhecer um
capacete não basta"); recomeçar pela referência (a calota, as partes que protegem o rosto e as laterais, a profundidade
da abertura, a espessura das bordas, os planos de luz pelo volume), sem precisar manter a barbuta, o T, a crista ou o
latão. O peito: a cota tinha a base mais aproveitável; ajustar pela referência, o volume antes da textura, sem misturar
construções; o desenho continua compartilhado. Só o 32 e o 64; a pasta `calça` (para as perneiras) não entrou.

**A escolha das referências** (os papéis no `LEIA-ME.md` de cada pasta; os objetos das pranchas foram separados pela
transparência e numerados por fila para escolher):
- **O capacete:** principal, o capacete aberto de frente, um pouco virado (o 62.º da prancha `5+N9Nb.png`). Dele vêm a
  construção (a calota com a tira vertical, a faixa da testa em curva, a tira que vira o protetor do nariz, as faces
  laterais descendo até embaixo, o fundo escuro do interior até cerca de 3/4 da altura e o vazio abaixo) e o ângulo (a
  frente à esquerda do meio, a face da esquerda estreita, quase de perfil, e a da direita larga). Das secundárias (o
  106.º e o 107.º, abertos parecidos): a espessura da borda e a faixa seguindo a curva. A pintura de bronze não vem: o
  material é o ferro da família.
- **O peito:** principal, a camisa de malha de aço de frente (o 103.º da prancha `etbij8.png`). Dela vêm a gola na
  própria malha com o vão escuro do pescoço, os ombros caindo nas mangas curtas que abrem, o corpo abrindo um pouco para
  baixo, a malha escurecendo nos lados e nas axilas, o cinto de couro com fivela, a barra e as mangas em dentes. Das
  secundárias (o 3.º e o 100.º): como as fileiras da malha seguem o volume. As couraças de aço (o 7.º, o 54.º, o 87.º)
  ficam registradas para uma variante futura do Peitoral e da Couraça.

**A rodada 1 guardada** em `elmo_cota/rodada1/` (a proposta, as fontes, a prévia, as fotos, as folhas e o script
daquela versão, `auxiliares/desenho_rodada1.py`, que a reproduz pixel a pixel).

**A rodada 2** (`auxiliares/desenho.py`):
- **O capacete:** a calota em volume pela luz da família, um tom abaixo das tiras (na referência, as tiras e a faixa são
  o mais claro); a tira vertical na linha da frente (à esquerda do meio) virando o protetor do nariz, clara à esquerda e
  escura à direita; a faixa da testa em curva (mais baixa na frente, que está mais perto), com a beira de cima clara e a
  de baixo escura (a espessura); as faces laterais, a da esquerda estreita e na luz, a da direita larga e na sombra, com
  a beira de fora clara e a de dentro escura, a barra virando para dentro; o fundo do interior escuro, um pouco mais
  claro junto da borda de trás, até cerca de 3/4 da altura, e o vazio abaixo entre as faces: o capacete vazio. Camadas:
  interior, calota, faces, tiras, contorno.
- **A cota:** o volume primeiro (o alto do peito mais claro, a luz da esquerda, os lados e as axilas na sombra, as
  mangas a da esquerda na luz e a da direita na sombra, abaixo do cinto um tom abaixo); a malha em anéis numa grade
  deslocada por cima (a da rodada 1); a gola na própria malha, com a beira clara e o vão escuro (o lado de dentro das
  costas); a barra e as mangas acabando em dentes; o cinto de couro com a fivela de ferro. Saíram a gola, os punhos e a
  barra de couro da rodada 1. Camadas: malha, couro, ferragem, contorno.
- **Tentativas da bancada:** o primeiro capacete desta rodada saiu simétrico e atarracado (a calota grande, a abertura
  rasa); com as proporções e o ângulo da referência, ficou com as faces longas e o vazio abaixo. A tira vertical saía da
  calota no alto; a calota tinha uma área branca grande que competia com as tiras e desceu um tom.

**O Aseprite (pelo MCP):** as listas do 32 pintadas pelo `pintar.lua` (0 diferenças, 0 fora da tela), em
`fontes/<peça>/<peça>-32.aseprite`; o composto do editor é igual ao PNG exportado e à prévia; o 64 é o 32 ×2; @2x exatos.

**As folhas:** `elmo_cota-referencias-r1-r2.png` (a referência principal × a rodada 1 × a nova, em tamanho real sobre o
carvão, com o escudo e as armas aprovadas ao lado, e ampliadas sem suavização); `elmo_cota-r2-no-jogo.png` (uma captura
de cada no jogo a 1920×945: a ficha com os dois e o saque de cada um; `fotografar.mjs elmo_cota` e
`elmo_cota_saque_cota`, `ROTULO=rodada2 SO_PROPOSTA=1`). Sem erro no console.

**As bases do peito:** a cota de malha representa melhor a Cota de Malha; razoavelmente a Brigantina (armadura flexível de
tronco); pior o Peitoral e a Couraça, que são de placa. Sem variantes nem mudança de dados nesta entrega.

### O elmo, rodada 3, e a cota em 40 e 48 (`elmo_cota/`)

**Decisões de Jean (19/10/2026):** a cota do `119f479` está aprovada; faltam o 40 e o 48 (o 32 e o 64 sem retoque; o
compartilhamento entre as quatro bases continua, com a limitação registrada). O elmo melhorou, mas precisa de mais uma
rodada pela mesma referência: na rodada 2 a faixa da testa estava quase horizontal e as laterais pareciam duas barras
verticais, enquanto a referência tem curvas e uma inclinação que explicam o volume; a faixa escura dentro da abertura
parecia uma travessa ligando as laterais. Reavaliar as proporções e a perspectiva do objeto inteiro (não inclinar a
imagem pronta) e separar o interior sombreado, a espessura das bordas e o vazio.

**O elmo da rodada 2 guardado** em `elmo_cota/elmo_r2/` (os PNGs, a fonte, a prévia e o script daquela versão).

**A leitura da referência, medida pixel a pixel** (o capacete aberto da caixa `(147, 479, 191, 532)` de
`ferramentas/arte/referencias/capacete/5+N9Nb.png`):
- **A abertura:** o interior escuro é só uma sombra curta logo abaixo da faixa (o lado de dentro da calota); abaixo dela,
  entre as faces, já é vazio (o fundo). A "travessa" da rodada 2 era o fundo escuro descendo demais.
- **A inclinação:** a peça está um pouco girada: a faixa sobe da esquerda para a direita (umas 3 linhas na referência)
  com uma leve curva; as faces não são verticais: a da esquerda desce entrando para a direita e é mais longa, a da
  direita é mais curta.
- **As proporções:** mais alta que larga; a calota em pouco mais de 1/3 da altura; o nariz longo (até cerca de 2/3); as
  faces ocupando a metade de baixo.
- **O volume:** as tiras e a faixa são o mais claro, separadas da calota por uma emenda escura.

**A rodada 3** (`auxiliares/desenho.py`): as formas definidas **nas coordenadas da referência** (a calota como uma elipse
girada como a faixa, a faixa pela curva medida, a tira e o nariz, as duas faces como quadriláteros inclinados, a sombra
do lado de dentro) e levadas ao quadro de 32 na mesma proporção (a escala 0,70); a luz depois: a calota pela luz da
família um tom abaixo das tiras, a emenda escura junto da tira e da faixa, a faixa com a beira de cima acesa e a de
baixo escura (a espessura), as faces com a beira de dentro clara (a da esquerda na luz, a da direita na sombra) e as
pontas escurecendo, o nariz claro à esquerda; a sombra do lado de dentro curta e o vazio abaixo. Na bancada, as faces
saíram finas demais na primeira passada e a calota escura; alargadas e clareadas, com as tiras ainda como o mais claro.

**A cota em 40 e 48:** a mesma construção; duas adaptações: a malha e os dentes da barra na grade de pixels de cada
tamanho (os anéis do mesmo tamanho em pixels, em vez de esticar com a escala; no 32 é o mesmo que antes) e, nos
maiores, o alto do peito mais claro só nos topos dos anéis (no 40 a área clara virava um retângulo de borda reta). O 32 e
o 64 são os aprovados, byte a byte.

**O Aseprite (pelo MCP):** o elmo 32 e a cota 40 e 48 pintados pelo `pintar.lua` (0 diferenças, 0 fora da tela); o
composto do editor é igual aos PNGs exportados e à prévia; @2x exatos; o 64 do elmo é o 32 ×2.

**As folhas:** `elmo-referencia-r2-r3.png` (a referência × a rodada 2 × a nova: em tamanho real sobre o carvão, a
silhueta numa cor e o acabamento, ampliados sem suavização); `cota-tamanhos-no-jogo.png` (atual × a cota com os quatro
tamanhos no Inventário, em 40, e no saque, em 64 e o "você usa" em 48; `fotografar.mjs cota_tamanhos`, `ROTULO=tamanhos
SO_PROPOSTA=1`); `prancha-carvao.png`. Sem erro no console.

### O elmo, rodada 4, em pé e de frente (`elmo_cota/`)

**Pedido de Jean (19/10/2026):** a coluna da direita de uma imagem que ele gerou a partir da nossa folha da rodada 3 é a
nova referência principal (`ferramentas/arte/referencias/capacete/elmo-frente-jean.webp`, o papel no `LEIA-ME.md` da
pasta). Ela substitui a orientação de acompanhar a inclinação: o capacete em pé e de frente, eixo vertical, nariz
centralizado, laterais equilibradas; a luz pode ser assimétrica, a construção é alinhada. Redesenhar na grade de 32 (a
referência não é reduzida), preservando a calota arredondada, a espessura da faixa, a abertura vazia e a separação das
faces. No meio da rodada: "tem que ter esse detalhe pra dentro que fecha no rosto" (o pé de cada face virando para
dentro). Só o 32 e o 64 (= 32 ×2); a cota aprovada e os tamanhos dela intocados.

**O elmo da rodada 3 guardado** em `elmo_cota/elmo_r3/` (a proposta, a fonte, a prévia e o script daquela versão).

**A rodada 4** (`auxiliares/desenho.py`, tudo simétrico em torno de x = 16): a calota como meia elipse; a faixa da testa
de 2 px, um pouco mais larga que a calota (a aba); a tira vertical e o nariz de 2 px no eixo, o nariz até a linha 20;
uma sombra curta do lado de dentro logo abaixo da faixa e o vazio abaixo; as faces medidas por um polígono só (a
distância ao eixo e a altura) espelhado: a beira de dentro quase reta, a de fora larga sob a faixa e entrando para
baixo, e o pé virando para dentro, na direção do nariz. A luz (de cima e da esquerda) assimétrica: a calota em
facetas, clara à esquerda da tira e escura à direita, com a emenda escura do lado da sombra; a tira e o nariz o mais
claro; a faixa com a beira de cima acesa e a de baixo escura; as faces com o lado de dentro aceso, a beira de fora
escura, o alto do pé claro e a ponta escurecendo; a face da esquerda mais clara. Na bancada, as faces saíram retas na
primeira passada (barras) e passaram a afinar para baixo; depois o pé para dentro, pedido pelo Jean.

**O Aseprite (pelo MCP):** as listas pintadas pelo `pintar.lua` num documento novo, cinco camadas (interior, calota,
faces, tiras, contorno; 0 diferenças, 0 fora da tela), em `fontes/elmo/elmo-32.aseprite`; o composto do editor é igual
ao PNG exportado e à prévia (o código 1641977722); o 64 é o 32 ×2; @2x exatos. A cota não foi reexportada (os arquivos
dela não mudaram).

**A folha:** `elmo-referencia-r3-r4.png` (a rodada 3 e a nova em tamanho real sobre o carvão, o 32 e o 64; a referência,
reduzida só para a folha, e as duas ampliadas 8× sem suavização).

### A cota no jogo (1.146.0)

**Aprovada por Jean (19/10/2026)** nos quatro tamanhos e integrada sem retoque: o 32 e o 64 do `119f479`, o 40 e o 48 do
`998373c` (os PNGs e as fontes do protótipo conferidos contra esses commits antes da cópia). As fontes em
`ferramentas/arte/aseprite/cota/`; `DERIVADOS` com o 64 = 32 ×2; os 8 arquivos do jogo idênticos, byte a byte, aos
aprovados, e `exportar_aseprite.py cota --conferir` os reproduz; o `familia_ferro.py` a reconhece pela fonte e não a
grava mais. Os papéis já existiam: o desenho `armadura` (Cota de Malha, Peitoral, Couraça, Brigantina) e a silhueta do
peito vazio.

**Conferido no jogo** a 1920×945 com os arquivos do jogo e os saves temporários (`elmo_cota/capturas/integracao/`): o
saque com a cota em 64 e o "você usa" em 48, "Equipar agora" (veste o achado e guarda o antigo) e "Guardar na mochila",
a ficha (32), o Inventário (40) e o peito vazio depois de tirar a armadura com dois cliques, na ficha e no Inventário
(`sandalia_chapeu/auxiliares/equipar.mjs guerreiro armadura armadura 1.146.0 cota` e
`elmo_cota/auxiliares/integracao.mjs`). Sem erro no console.

### O elmo em 40 e 48 (`elmo_cota/`)

**Decisão de Jean (19/10/2026):** o elmo da rodada 4 (`b4e920d`) aprovado em 32 e 64; fazer o 40 e o 48 mantendo a
construção frontal, o alinhamento, a abertura e as faces que fecham para dentro, adaptando os pixels a cada grade. Sem
integrar.

**O 40 e o 48** saem do mesmo `auxiliares/desenho.py` (as medidas no quadro de 32), com três adaptações de grade; o 32
continua idêntico ao aprovado, pixel a pixel:
- **A beira de fora das faces com 1 px em todo tamanho** (no 48 ela saía de 1 ou 2 px conforme a linha, um serrilhado).
- **A cintura antes do pé**, desenhada nos dois lados: no 32 a beira de dentro da face recua 1 px por umas três linhas
  e o pé volta para dentro (é o que faz o pé ler como um gancho fechando sobre o rosto); no 40 e no 48 esse recuo saía
  de um lado só ou de uma linha só (um entalhe), e agora tem a mesma altura proporcional nos dois.
- **A simetria:** uma medida que cai bem no centro de um pixel (a ponta da faixa, a beira da face) arredondava para um
  lado só; fica o pixel que existe dos dois lados. As silhuetas dos três tamanhos são simétricas.

**O Aseprite (pelo MCP):** o 40 e o 48 pintados pelo `pintar.lua` em documentos novos com as cinco camadas (0
diferenças, 0 fora da tela), em `fontes/elmo/elmo-40.aseprite` e `-48`; o composto do editor é igual aos PNGs
exportados e à prévia; @2x exatos. O 32 e o 64 da proposta não mudaram.

**As fotos** (`fotografar.mjs elmo_tamanhos`, `ROTULO=tamanhos`, 1920×945): o Inventário (40) e o saque (64 e o "você
usa" em 48), atual × tamanhos, em `elmo-tamanhos-no-jogo.png`; a prancha `prancha-carvao.png` com o elmo e a cota nos
quatro tamanhos. Sem erro no console.

### A manopla e as perneiras, o remake do ferro, 3 (`manopla_perneiras/`)

**Pedido de Jean (19/10/2026):** o próximo par, só propostas: confirmar bases, únicos, tamanhos e compartilhamentos (os
espaços vazios também); abrir as referências (a pasta `calça`, examinada, versionada se usada); uma principal de
construção por peça; a família de materiais e acabamento do elmo, da cota, do escudo e das armas aprovados, sem
obrigação de seguir os placeholders. A manopla: uma luva de armadura reconhecível, com volume, polegar, dedos articulados
e o punho bem separado; a forma antes das divisões e dos rebites. As perneiras: proteção de pernas com volume,
articulações e sobreposições coerentes, sem virar uma calça recolorida. Vazias. Só o 32 e o 64 (= 32 ×2).

**Os usos (nada muda nesta entrega):**
- `manopla`: a base Manopla do Guerreiro (nenhum único; os raros, como "Fome Negra (Manopla de Ferro)", usam o desenho
  da base) e a silhueta das mãos vazias de todas as classes (`VAZIO`). A habilidade Grito de Guerra usa o sprite
  `manopla` do jogo noutro papel e fica com ele. O desenho de reserva das mãos sem base (`ICONE_ESPACO`) é a luva de
  couro, não a manopla.
- `perneiras` (o desenho `calca` nos dados): a Perneira e a Greva do Guerreiro (nenhum único), a silhueta das pernas
  vazias (`VAZIO`) e o desenho de reserva das pernas (`ICONE_ESPACO`: `calca`).
- Tamanhos no jogo: 32 (ficha, mochila), 40 (Inventário), 48 ("você usa" do saque), 64 (cartão do saque).

**As referências** (os papéis no `LEIA-ME.md` de cada pasta, agora versionadas):
- **A manopla:** principal, o par de manoplas de placas de aço de `referencias/Luvas/tQXl+6.png` (a caixa `(534, 148, 594,
  202)`): os dedos em segmentos, a placa dos nós, a placa da mão abaulada, o polegar de lado, o punho em lâminas que
  abrem. Uma só manopla, de pé e pelas costas da mão, como as luvas da família.
- **As perneiras:** a 1.ª passada usou a calça de placas de `referencias/calça/jA2fex.png` (a caixa `(421, 554, 465,
  619)`) e saiu como uma calça: cinto, faltas e pernas com corpo de pano. **Jean recusou** ("ta muito calça... é uma
  armadura de ferro"), mandou na conversa uma imagem de perneiras de placas e pediu para esquecer a pasta `calça` para
  isso. A 1.ª passada está guardada em `manopla_perneiras/perneiras_r1/` (o script e a prévia).

**O desenho** (`auxiliares/desenho.py`, as medidas no quadro de 32):
- **A manopla:** os quatro dedos de 2 px com 1 px de vão (o do meio o mais comprido), cada um um cilindro aceso à
  esquerda, com duas juntas escuras e a ponta na luz; o polegar saindo da beira esquerda na altura da mão, em dois
  segmentos; a placa dos nós com a beira de cima acesa e a sombra sobre a mão; a placa da mão pela luz da esfera; o
  pulso estreito na sombra; o punho em duas lâminas que abrem (a beira de cima acesa, a sombra da lâmina de cima sobre a
  de baixo, a barra virando). Sem rebites. Camadas: punho, mao, dedos, contorno. Na bancada: os dedos de 2,6 de largura
  colavam (o vão não pegava pixel), o punho em sino largo e o polegar levantado faziam um troféu; a luz do `cilindro`
  saía da direita (o sinal trocado) e foi corrigida.
- **As perneiras (rodada 2):** uma placa no meio, no alto, ligando as pernas; cada perna uma cadeia de placas abauladas,
  uma sobre a outra (o coxote alongado com a ponta do quadril para cima e para fora, a joelheira mais larga e saliente,
  a greva mais fina e comprida, o tornozelo abrindo um pouco), cada uma pela luz da esfera com a beira de baixo escura
  sobre a seguinte; os entalhes entre as placas na silhueta; o vão aberto desde o alto (o arco). Sem cinto, sem couro.
  A perna da direita um tom abaixo. Camadas: grevas, joelhos, coxotes, centro, contorno.

**O Aseprite (pelo MCP):** as listas do 32 pintadas pelo `pintar.lua` em documentos novos (0 diferenças, 0 fora da
tela), em `fontes/<peça>/<peça>-32.aseprite`; o composto do editor é igual aos PNGs exportados e à prévia; o 64 é o 32
×2; @2x exatos. (O Aseprite tinha fechado no meio da entrega; reaberto, o conector voltou.)

**As folhas:** `manopla_perneiras-familia.png` (em tamanho real sobre o carvão ao lado do elmo, da cota, da espada, da
maça e do escudo; o 64; as duas e a 1.ª passada das perneiras ampliadas 8×); `manopla_perneiras-no-jogo.png` (a ficha
com as duas vestidas e o saque de cada uma, atual × proposta, a 1920×945; `fotografar.mjs manopla_perneiras` e
`manopla_perneiras_saque_perneiras`). O "você usa" em 48 ainda vem do 32 ×2 reduzido pela página (sem o 48 na proposta).
Sem erro no console.

### A manopla e as perneiras, refeitas pelas referências novas (`manopla_perneiras/`)

**Decisão de Jean (19/10/2026):** as propostas do `c5fd33b` não foram aprovadas; refazer as duas pelas referências
novas, que orientam a construção (não só os detalhes por cima do desenho anterior). Só no protótipo, 32 e 64 (= 32 ×2).
- **A manopla:** na recusada, os dedos pareciam hastes retas presas a uma peça mecânica. Principal: `referencias/Luvas/
  2.webp` (a manopla isolada de perfil, os dedos à esquerda, o punho à direita): a construção da mão, a articulação do
  polegar e a sobreposição das placas; os dedos com curvatura natural e as placas acompanhando; o punho ligado à mão
  como uma luva vestível, com espessura e volume. Secundária: a prancha Raven Fantasy (`Luvas/1.gif`), para a
  simplificação de ícone. Sem todos os rebites.
- **As perneiras:** a recusada parecia pernas robóticas (coxas, joelhos e canelas separados). Principal: o conjunto de
  placas prateadas da 3.ª linha, última coluna de `referencias/calça/2.png`; a prancha de armaduras `calça/1.gif` de
  apoio. Um equipamento coerente, com ligações e sobreposições compreensíveis; o cinto, as tiras ou um suporte discreto
  podem voltar (a restrição anterior caiu); sem joelheiras como pequenas esferas.

**As recusadas guardadas** em `manopla_perneiras/recusadas_c5fd33b/` (a proposta, as fontes, as prévias, as capturas,
as folhas e o script daquela versão, `desenho_c5fd33b.py.txt`); a 1.ª passada das perneiras (a calça) continua em
`perneiras_r1/`.

**O desenho** (`auxiliares/desenho.py`, refeito; uma peça por vez, a silhueta numa cor e os volumes antes da luz):
- **A manopla**, de perfil e um pouco inclinada (a manchete mais alta), pelas proporções da referência: os dedos em um
  terço do comprimento, a mão em um quarto, o pulso estreito, a manchete o resto. Os quatro dedos como faixas de 2 a 2,5
  px que saem dos nós e curvam para baixo nas pontas (o terceiro o mais longo); cada um por cima do de baixo, com a
  linha escura onde se cruzam (como na referência); uma junta discreta no meio de cada dedo e a ponta um tom abaixo; o
  polegar saindo de baixo da mão, largo na base, com a dobra no meio. As costas da mão com a placa em relevo (a quina de
  cima acesa, a de baixo e a da direita escuras); a faixa do pulso escura com uma tira acesa (a luva entrando na
  manchete); a manchete em cone, acesa por cima, abrindo só cerca de 1,4 vez e terminando arredondada na beira da boca.
  Camadas: punho, mao, dedos, contorno. **Na bancada:** a construção levada da referência por uma escala só deixava os
  dedos com 1,7 px (um bloco); girar a peça 18 graus apagava os vãos de 1 px entre os dedos (pontos soltos); com as
  proporções na grade e a inclinação nas medidas, os dedos ficaram separados. A manchete larga em sino lia como um
  megafone e foi reduzida; as duas juntas por dedo viravam um xadrez no 32 e ficou uma.
- **As perneiras**, de frente: o cinto de couro com a fivela de ferro; a placa do meio em ponta, clara, com a beira
  escura por cima das coxas; cada perna contínua, um cilindro aceso à esquerda (a faixa clara no terço da esquerda, como
  na referência), com o contorno de fora em degraus onde as placas se sobrepõem (o coxote sai além do cinto, a lâmina de
  baixo entra, a asa da joelheira sai, a greva entra e afina, a beira do tornozelo sai um pouco); a joelheira larga por
  cima do fim do coxote e do começo da greva, abaulada pela luz da esquerda com um reflexo curto, a asa de fora um tom
  abaixo; as linhas de sobreposição finas, de 1 px. A perna da direita um tom abaixo. Camadas: grevas, coxotes,
  joelhos, meio, cinto, contorno. **Na bancada:** o contorno liso lia como calça; com os degraus, como placas; a
  joelheira e o coxote em faixas horizontais acesas viravam barras (o risco dos segmentos separados) e passaram ao
  volume pela luz.

**O Aseprite (pelo MCP):** as listas do 32 pintadas pelo `pintar.lua` em documentos novos (0 diferenças, 0 fora da
tela), em `fontes/<peça>/<peça>-32.aseprite`; o composto do editor é igual aos PNGs exportados e à prévia (manopla
78892166, perneiras 671966350); o 64 é o 32 ×2; @2x exatos.

**A folha:** `manopla_perneiras-r3.png`: as duas em tamanho real sobre o carvão ao lado do elmo, da cota, da espada, da
maça e do escudo; o 64; as duas ampliadas 6× sem suavização ao lado das recusadas do `c5fd33b`; e a ficha a 1920×945,
atual × a rodada nova (`fotografar.mjs manopla_perneiras_ficha`, `ROTULO=rodada3`). Sem erro no console.

### A manopla e as perneiras, rodada 4 (`manopla_perneiras/`)

**Pedido de Jean (19/10/2026):** outra rodada das duas, só no protótipo, pelas imagens que ele mandou (guardadas como
`referencias/calça/perneiras-jean.webp` e `referencias/Luvas/manopla-jean.webp`; os papéis nos `LEIA-ME.md`).
- **As perneiras:** a ligação melhorou, mas o metal ainda parecia arredondado e macio, e os joelhos pareciam inchaços.
  Placas com faces, arestas e espessura; reflexos definidos contra planos escuros; a joelheira organizada por uma
  aresta, resultado da construção (não um risco por cima); sombras onde uma placa cobre a outra. Ficam o conjunto
  inteiro, o cinto e a continuidade.
- **A manopla:** os dedos pareciam ganchos de garra mecânica e a manchete dominava. A mão primeiro (costas, dedos
  levemente dobrados, polegar ligado, pulso), depois as placas; não precisa mostrar todos os dedos; a manchete
  equilibrada com a mão.

**A rodada anterior guardada** em `manopla_perneiras/rodada3_89be986/` (a proposta, as fontes, as prévias, a captura,
a folha e o script, `desenho_89be986.py.txt`).

**As perneiras** (`auxiliares/desenho.py`): mais estreitas, como na referência (as pernas afastadas logo abaixo da placa
do meio); o metal em planos, não pela luz de esfera: cada placa com uma faixa de reflexo definida no terço da
esquerda, um plano médio e a beira da direita escura; as lâminas (a do quadril, a de cima da joelheira, a curta abaixo
dela, a tornozeleira) com a sombra de 1 px da placa de cima e a espessura acesa; a joelheira em losango com a aresta
vertical e a horizontal e quatro faces (a de cima à esquerda clara, a de cima à direita média, as de baixo escuras), as
asas em ponta passando do contorno da perna, a beira escura só embaixo; a lâmina do coxote em volta dela escurecida
(recolhida atrás), para a joelheira ficar na frente; a placa do meio em duas faces; o cinto com a boca escura em cima;
uma correia de couro em diagonal no vão. **Na bancada:** a joelheira feita por regra se misturava com as faixas do
coxote (o mesmo tom, sem contorno); no 32 ela foi desenhada à mão (9 × 7 px). As correias enchendo o vão juntavam as
pernas num bloco; ficou uma tira.

**A manopla:** pelas costas da mão, de lado; **três dedos** no 32 (o indicador, o médio e o anelar com o mínimo por
trás), de 3 px com 1 px de vão, levemente dobrados, o do meio o mais longo, cada um aceso em cima e escuro embaixo, com
duas juntas discretas e a ponta na luz; o polegar embaixo, ligado à base da mão, com uma junta; a placa das costas da
mão em pentágono com a ponta para os dedos; os anéis do pulso; a manchete menor (mais baixa e mais curta), acesa em
cima, com a costura no meio e a beira da boca. **Na bancada:** com quatro dedos de 2 px ficava um pente de linhas
escuras; com três de 3 px, dedos.

**O Aseprite (pelo MCP):** as listas do 32 pintadas pelo `pintar.lua` em documentos novos (0 diferenças, 0 fora da
tela), em `fontes/<peça>/<peça>-32.aseprite`; o composto do editor é igual aos PNGs exportados e à prévia (manopla
609699151, perneiras 377480868); o 64 é o 32 ×2; @2x exatos.

**A folha:** `manopla_perneiras-r4.png`: antes (`89be986`) × depois em tamanho real junto das peças de ferro aprovadas;
cada peça ampliada 6× sem suavização com a referência ao lado (reduzida só para a folha); a ficha a 1920×945, antes ×
depois (`fotografar.mjs manopla_perneiras_ficha`, `ROTULO=rodada4`). Sem erro no console.

