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
- **As flechas:** três, com a pena para cima, como se guardam; haste de madeira, penas claras e uma pena escura.
- **14 cores** no 32 e 16 no 24.

**Rodadas descartadas:**
- **1:** a 45°, curta e deitada.
- **2:** em pé, mas o fundo encostava na borda (o contorno dava a volta na grade e aparecia no alto) e as penas se
  juntavam numa mancha.
- **3 (a proposta):** a origem subiu e as flechas abriram em leque.

**Conferido (`aljava/capturas/`, `topo-atual-x-proposta-1500.png`, `ficha-atual-x-proposta-1500.png`):**
- **Na ficha (32):** é da família do couro, mais sóbria que a atual pintada (sem a cinta dourada nem a fivela).
- **No topo (24):** reconhecível, mas mais discreta que a atual, que é mais colorida (vale olhar no jogo).
- **No Inventário (40):** continua a atual (o 40 vem depois).
- Sem erros.
