# 1E.4: o mapa e o minimapa da campanha (23/10/2026; levantamento e primeiro lote; nada no jogo)

**Pedido do Jean:** levantar os caminhos, os símbolos dos lugares, a posição do jogador, as marcas de missão e contrato,
os estados, os tamanhos e os compartilhamentos do mapa e do minimapa, priorizando a campanha; depois, um primeiro lote
pequeno de protótipos, só aqui, aguardando a avaliação. Navegação, áreas de clique, destinos, regras de viagem,
descoberta e progressão não mudam. Produção consultada: **1.199.3**.

## As folhas

- **`levantamento.png`**: onde o mapa aparece (a página e o mapa grande a 1920×945), o minimapa e o mapa grande em
  tamanho real, as peças de hoje em contexto e ampliadas sem suavizar, e o resumo do que se achou.
- **`pecas.png`**: as peças novas a 1× e a 4×, ao lado dos ícones de lugar aprovados com que convivem.
- **`comparacao.png`**: atual × direção A × direção B, nas três situações da campanha, com os mesmos dados (o minimapa a
  2×, o mapa grande a 1×, o lugar atual a 2×) e a legenda.
- As capturas inteiras, a 1920×945: `capturas/atual/`, `capturas/proposta-a/` e `capturas/proposta-b/` (para cada
  situação: `-pagina`, `-mundo`, `-mini`, `-mapa`, `-grande`, `-janela`), com o `registro.json` de cada bateria (o
  canvas nativo e exibido, os símbolos, os botões, os centros, o console).

## Como o mapa funciona (o que o levantamento conferiu no código)

- **O desenho é um só, `rpg/web/static/mapa.js` (`MapaPx.criar`)**, para o minimapa do painel do mundo
  (`app/paineis.js`, `desenharMundo`), o mapa grande (M ou o atalho Mapa; `desenharMapaGrande`) e o mapa na página
  (o sistema Mapa do motor, `app/escolhas.js`, `mapaNaPagina`). Os dados vêm de `rpg/web/estado.py`
  (`mapa_conhecido`): os lugares visitados e os vizinhos deles, com `tipo`, `bioma`, `visitado`, `atual`, `distancia`
  (só os vizinhos do lugar atual), `nivel`, `descricao` e `covil`; as estradas com `atual` (toca o lugar atual) e
  `percorrida` (as duas pontas visitadas).
- **O terreno** é pintado por pixel num canvas (as manchas do bioma, a névoa pontilhada, os enfeites), tingido pela
  hora; **as estradas** são linhas de Bresenham de 1 px com a sombra; **os símbolos** são os sprites 16×16 do jogo
  (`sprites-dados.js`), desenhados no canvas em 14 (minimapa) ou 16 (mapa grande). Por cima, em HTML, os botões dos
  lugares (28 e 40 px: a área de clique e a dica), o "!" das marcas e os nomes.
- **A escolha do desenho:** `MapaPx.sprite` (covil ativo → `covil`, vencido → `vencido`, vila → `vila`, senão o bioma).
  O tipo `saida` da campanha (a Estrada de Varn) cai no bioma (planície). A mesma escolha serve a lista de Caminhos
  (`Icones.lugar`, os ícones aprovados de 32 e 40), o Diário (a missão e os contratos, o sprite 16), as opções de
  viagem do menu (o sprite 16) e a legenda (os nove sprites 16).
- **Os tamanhos a 1920×945:** o minimapa é um canvas de 224×128 exibido em 284×162 (**×1,27**); o mapa grande, de
  352×201 exibido em 928×530 (**×2,64**). O símbolo fica com ~18 px no minimapa e ~42 no mapa grande; o "!" tem 11 px de
  letra no minimapa e 14 no grande. Não há zoom: `enquadrar` ajusta o quadro aos lugares conhecidos (com os cinco
  lugares do Vale, os dois mapas mostram o mesmo quadro).
- **Os estados que existem:** o lugar atual (o anel que cresce e some a cada 1,5 s, e o nome em ouro; no minimapa, só o
  nome do lugar atual aparece); o destino clicável (o tracejado de ouro pulsando); o destacado (o contorno, ao passar o
  mouse na lista de Caminhos ou no rastreador); o conhecido não visitado (60% de opacidade, a névoa no terreno, o nome
  apagado); o perigo (o nome em vermelho quando o nível é 2 ou mais acima do seu); as estradas daqui (ouro), percorrida
  (bege) e só conhecida (pontilhada escura); a marca "!" (missão ou contrato, a mesma); o covil ativo e o vencido (só no
  procedural). **Não existem:** a missão concluída no mapa (a marca some, a missão fica no Diário), o lugar bloqueado (a
  cidadela "selada" e a saída fechada só no texto da dica e da lista).

## O que se achou

**Defeitos de leitura**
1. **A posição do jogador** não tem marca permanente: o anel some, e na maior parte do tempo só o nome em ouro diz onde
   você está. No minimapa noturno no Bosque, o nome cai ao lado do quadrado do Vau (`levantamento.png`, seção 2).
2. **A escala fracionária** (×1,27 e ×2,64) faz pixels de larguras diferentes nas estradas, no pontilhado e nos
   símbolos.
3. **Os símbolos do minimapa** saem borrados (o 16 desenhado em 14 com suavização, depois ampliado); a Capela e a
   Estrada de Varn quase somem.
4. **As estradas** atravessam o símbolo; a só conhecida (Bosque → Capela) quase não aparece no escuro; **a saída
   fechada parece um destino aberto** (a estrada em ouro e o tracejado de "clique para viajar"; o clique leva ao aviso).
5. **Missão e contrato com a mesma marca**, um "!" de texto numa caixa de ouro presa ao canto do botão (não do desenho).

**Provisórios** (nunca passaram por aprovação): os nove sprites 16 do mapa (a família de antes da HUD), o traço das
estradas, o "!" em CSS, o anel e o tracejado. **Aprovados que já servem ao mapa:** os ícones de lugar da família da HUD
(`lugar-*-32/40`, da `assets4c`), hoje só na lista de Caminhos; o atalho Mapa da doca. O mapa e a lista mostram o mesmo
lugar com dois desenhos diferentes.

**Prioridade** (frequência × problema; o minimapa está sempre à vista): 1) a posição do jogador; 2) os caminhos (a
escala, os estados, a saída fechada); 3) os símbolos dos lugares; 4) as marcas de missão e contrato. **Depois**: o
Diário e as opções de viagem com o mesmo desenho do mapa, a legenda só com o que existe, a missão concluída e o perigo
também no símbolo, o nome do lugar atual no minimapa que encosta num vizinho.

**Dependências do procedural** (para o levantamento da retirada): o covil (ativo e vencido) e a cidadela só existem lá,
com a "selada" da descrição; a legenda lista os nove desenhos dos dois modos; `MapaPx.sprite` cai no bioma para a
`saida` da campanha; `GLIFO_TIPO`/`GLIFO_BIOMA` (`rpg/mapa.py`, a interface de texto) e o `covil` de `estado.py`. Ao
retirar o procedural, isso sai ou muda junto; a campanha precisa de um desenho e de um estado próprios para a saída (o
`fechado` existe no motor, `campanha.py`, mas não chega à tela como campo: o protótipo o reconhece pela descrição).

## O primeiro lote (proposta; aguardando o Jean)

Quatro elementos, escolhidos pelos defeitos acima e pela frequência: **a posição, os caminhos, os símbolos dos
lugares e as marcas de missão e contrato**. Uma proposta principal por elemento; uma segunda direção só na posição.

1. **A escala inteira (a base de tudo):** o canvas na resolução do pixel do mapa, **×2 no minimapa (142×81 → 284×162)
   e ×3 no mapa grande (309×177 → 927×531)**: o mesmo espaço (o mapa grande fica com 1 px a menos de largura e 1 a
   mais de altura), pixels iguais, o pontilhado e as estradas limpas. Na integração, o lado do canvas sai da largura do
   painel (o protótipo já mede o contêiner).
2. **Os caminhos, como conjunto:** a estrada começa e acaba na borda do símbolo; **daqui** (ouro), **percorrida**
   (bege, contínua), **só conhecida** (tracejada, mais clara que hoje, visível no escuro) e **para a saída fechada**
   (pontilhada, apagada, com a **cancela** na ponta e o tracejado de destino em cinza, sem pulsar). O clique continua lá:
   viajar para a Estrada de Varn continua dando o aviso de que está fechada.
3. **Os símbolos dos lugares:** os **ícones aprovados da família** (`lugar-*`), os mesmos da lista de Caminhos, **1:1**:
   o **40 no mapa grande** e o **32 no minimapa**, posicionados em pixel inteiro, com a mesma opacidade de "conhecido
   não visitado". **Nenhum desenho novo:** pela skill de itens, testei antes o reaproveitamento da arte aprovada em
   tamanho nativo; o 32 coube no minimapa e lê melhor que o 16 borrado, então não fiz o 24 previsto. O covil vira a
   caverna da família (a mesma da lista); o vencido, sem ícone na família, fica o sprite do jogo (só procedural).
4. **As marcas, desenhadas à mão** (`auxiliares/grade.py`, montadas no Aseprite em lote), uma para cada mapa:
   - **missão**: a plaqueta de ouro com o "!" (11×14; 9×11 no minimapa);
   - **contrato**: o cartaz do mural, o papel com o lacre vermelho e as linhas (11×14; 9×11);
   - presas ao canto do **símbolo**, a missão primeiro e o contrato ao lado quando os dois caem no mesmo lugar.
5. **O "você está aqui", permanente** (o anel que some sai):
   - **direção A, a seta** de ouro apontando para o lugar, com um balanço de 2 px (19×17; 13×12 no minimapa);
   - **direção B, o herói na plaqueta**: a figura 16 aprovada da classe (`retratos.js`) numa moldura de ouro com a ponta
     (20×22; no mapa grande a 2×, a moldura e a figura juntas). As marcas do lugar atual vão para o lado da plaqueta.
   - A escolha visual relevante: **A** é um sinal neutro, pequeno, que não disputa com o símbolo; **B** diz *quem* está
     ali e liga o mapa ao herói, mas é maior e esconde mais terreno. A minha recomendação é **A**: o minimapa é pequeno
     e o símbolo do lugar é que precisa aparecer; a seta resolve a dúvida sem pôr outro retrato na tela.
6. **A legenda** do mapa grande: só o que o mapa conhecido mostra (os ícones da família em 32) e as marcas (a seta, a
   missão, o contrato, a saída fechada), no lugar dos nove sprites dos dois modos.

**O que melhorou:** o lugar atual se acha na hora, nos dois mapas e à noite; os símbolos são os da lista (o mesmo lugar,
o mesmo desenho) e leem no minimapa; as estradas não cortam os desenhos; a saída fechada não parece aberta; missão e
contrato se distinguem. **Limitações:** no mapa grande, o ícone de 40 tem margens próprias e o lugar parece um pouco
menor que o sprite antigo esticado a ~42 px; as marcas novas são pixel art 1:1 sobre ícones pintados (a mesma convivência
dos estados sobre os retratos); a "!" da missão lembra o ícone da Iniciativa da luta (contextos diferentes); no
minimapa noturno, o nome do lugar atual ainda encosta no quadrado do vizinho (a seta desfaz a dúvida); o Diário, as
opções de viagem e o "!" do texto do Diário (`MARCA_MAPA`) continuam com o desenho de hoje.

**Conferido:** em todas as situações, nas duas direções, os mesmos lugares, os mesmos destinos clicáveis, os mesmos
estados (`atual`, `clicavel`, `tem-contrato`; a proposta só acrescenta `fechado`), os mesmos botões (28 e 40 px) e os
mesmos rótulos acessíveis do jogo; nenhum erro ou aviso no console; o procedural continua funcionando com a proposta
(`procedural-covil`). As peças: a fonte reaberta com as camadas na ordem (corpo, marca, contorno), 0 diferentes na
releitura, o exportado igual à grade, alfa só 0 ou 255, o @2x em blocos inteiros que voltam ao original.

## Como refazer

    python auxiliares/grade.py ..                 # as grades e as listas das peças
    python auxiliares/exportar.py --montar        # as fontes (Aseprite em lote) e proposta/*.png, conferidas
    # as fotos (PLAYWRIGHT_BROWSERS_PATH e PLAYWRIGHT_MODULO como na fumaça):
    node auxiliares/fotografar.mjs <raiz> capturas/atual
    PROTOTIPO=1 POS=a node auxiliares/fotografar.mjs <raiz> capturas/proposta-a
    PROTOTIPO=1 POS=b node auxiliares/fotografar.mjs <raiz> capturas/proposta-b
    python auxiliares/folhas.py                   # levantamento.png, pecas.png, comparacao.png

O protótipo (`prototipo/mapa.js`) é uma cópia do `mapa.js` da 1.199.3 com a proposta, servida no lugar do do jogo só na
página das fotos (`page.route`); a legenda da proposta entra por `MapaPx.legenda`. O jogo não lê nada daqui.

**O Aseprite:** o conector desta sessão não subiu (ninguém escutava a porta 6515; o editor aberto, com um documento do
Jean, respondia "editor not connected"). Não toquei na janela nem encerrei processos: as fontes saíram pelo caminho em
lote documentado (`auxiliares/montar.lua`, o `montar_camadas.lua` para peças w×h, com o `pintar.lua`).

## Para a integração (só do que o Jean aprovar)

O `mapa.js` da proposta mostra o caminho; a integração faria: o `fechado` como campo em `estado.py`; as peças em
`hud/icones/` (pelo `exportar_aseprite.py`, com as fontes em `ferramentas/arte/aseprite/`), registradas em `Icones`; o
CSS em `05-paineis.css`; a legenda nova em `app/paineis.js`; e, numa entrega à parte, o Diário, as opções de viagem e o
`MARCA_MAPA` com o mesmo desenho.
