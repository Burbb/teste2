# A Abominação e o Cavaleiro Sombrio (22/10/2026, propostas; nada no jogo)

**Pedido do Jean:** o próximo par do plano 23, duas propostas distintas de cada, só no protótipo, depois de consultar os
dados e os textos das duas. Produção na 1.186.0; nenhum candidato autorizado para integração.

## O que vem do jogo (conferido no código)

**Abominação** (`abominacao`, `rpg/dados.py`): "Carne costurada pela corrupção. Ninguém sabe o que ela foi antes."
Traços `corrompido` ("tocado pelo Vazio") e `gigante` ("difícil de atordoar"); o Golpe Esmagador (avisa antes), o Veneno
e o Regenerar ("As feridas se fecham diante dos seus olhos"); 60 de vida, agilidade 2, sozinha, a partir do nível 6;
vive na Cidadela ("as paredes pulsam devagar, como carne viva") e é a última criatura da Fenda (`CRIATURAS_DA_FENDA`,
perigo 5). Hoje no sprite `corrompido`, que só ela usa.

**Cavaleiro Sombrio** (`cavaleiro_sombrio`): "Guerreiros que juraram lealdade ao Vazio e não puderam morrer depois."
Traços `morto-vivo` e `blindado` ("resiste a dano físico"); o Golpe Esmagador e o Toque Drenante; sozinho, a partir do
nível 6; vive na Cidadela. Também é **o Último Guarda** antes do antagonista (`sistemas/chefes.py`: "Um cavaleiro de
armadura negra se coloca entre vocês.", com nome próprio, da mesma família). Hoje no sprite `caveira`.

**Usos de uma futura integração:** pela família, os dois na carta da luta (32), no Bestiário (48), no cartaz e no
rastreador dos contratos e na faixa do mestre caçador; o Cavaleiro também como o Último Guarda (a mesma família, o mesmo
retrato). **O que continua nos sprites compartilhados:** o `corrompido` ficaria sem usuário no catálogo (reserva); a
`caveira` segue com a Bruxa Afogada e o Lich Menor (guardiões), o servo aliado e a família `esqueleto_servo`.

**Interpretação artística (minha):** a Abominação como duas carnes (a pálida e a roxa do hematoma, a cor da corrupção)
unidas por costuras, com poucas marcas fortes; o Cavaleiro como aço escuro com as bordas claras (não só escuro), o elmo
fechado sem rosto e a capa vinho, com um ponto violeta do Vazio na viseira da A.

## As propostas

**Abominação** (camadas carne, hematoma, costura, olhos).
- **A, a boca costurada** (`abominacao-a`): de frente, a cabeça disforme, metade roxa e inchada com o olho fechado,
  metade pálida com um olho pequeno, a costura subindo pela testa, a boca fechada a pontos, os ombros pesados.
- **B, o brutamontes curvado** (`abominacao-b`): de três quartos, a corcunda costurada com o hematoma subindo à
  direita, a cabeça pequena e baixa à esquerda com a mandíbula torta, o punho enorme na frente (o golpe esmagador).
- **Na bancada:** a primeira A, sem cabeça (a massa bicolor com a costura), lia como um saco ou um pêssego; a primeira B,
  com o braço erguido, como uma massa com um periscópio; uma B com o rosto no peito, redonda, ficou fofa, e depois
  quadrada demais. O rosto legível (A) e a silhueta curvada com a cabeça pequena (B) resolveram.

**Cavaleiro Sombrio** (camadas capa, armadura, viseira e, na B, espada).
- **A, o elmo fechado** (`cavaleiro-a`): de frente, a viseira em T com um ponto violeta, as ombreiras largas com o brilho
  nas bordas, a capa vinho entre elas.
- **B, a espada e a crista** (`cavaleiro-b`): o elmo com a crista de crina vinho caindo para trás, a espada de ponta
  para baixo à frente (o pomo, o punho, a guarda e a lâmina), as ombreiras e a capa.

## A minha leitura (quem escolhe é o Jean)

- **Abominação: prefiro a A.** O rosto lê na carta (as duas carnes, o olho fechado, a boca costurada) e não se confunde
  com o Carniçal (pálido de boca aberta), o Afogado (meio crânio) nem o Troll (verde). **Limitação:** as duas metades
  bem divididas podem lembrar uma máscara.
  - B: a silhueta mais de criatura (a corcunda, a cabeça pequena, o punho); **limitação:** a 32 o rosto é pequeno e a
    massa rosada lê como um volume disforme sem expressão.
- **Cavaleiro: prefiro a B.** A espada à frente faz dele um combatente e a crista dá a silhueta; o elmo fechado o separa
  do Esqueleto de Guarda (a caveira à mostra) e do Mercenário (o rosto à mostra). **Limitação:** a crista vinho e a
  capa são discretas no escuro, e a lâmina é fina.
  - A: o ícone mais limpo, com a viseira em T forte; **limitação:** sem arma, fica estático, como uma armadura vazia.

## Processo

- As grades à mão em `auxiliares/grades.py`; as fontes pelo conector do Aseprite (`pintar.lua`, 0 diferentes na
  releitura; o composto 191, 178, 160 e 163 = a soma das camadas); sem guia (nenhuma referência externa). A exportação
  (`python auxiliares/exportar.py`): igual à grade, o @2x exato, o 32 e o 48 em blocos inteiros do 16.
- As fotos a 1920×945 (`auxiliares/fotografar.mjs`, os modos atual, a e b, trocados só na página pelo nome): a luta da
  abominação (com o carniçal e o troll), a do cavaleiro (com o esqueleto e o mercenário) e o Bestiário; sem erro no
  console.
- As folhas (`python auxiliares/prancha.py`): `abominacao.png` e `cavaleiro.png`, com o jogo de hoje × A × B na carta
  (real e 2×) e no Bestiário (48), a fileira com os aprovados e a 12×.

# A segunda rodada (22/10/2026, propostas; nada no jogo)

**Decisão do Jean sobre a primeira:** a Abominação A e B e o Cavaleiro B recusados; o Cavaleiro A aceito só como direção
para refinar. Nenhum retrato autorizado para integração; os desenhos da primeira rodada ficam como estavam (as fontes,
as grades, as fotos em `capturas/` e as folhas `abominacao.png` e `cavaleiro.png`).

**O que não funcionou na primeira (registro):** o rosto dividido em duas cores (lia como máscara), a boca regular costurada,
a massa rosada sem anatomia legível (a B), o centro do Cavaleiro alto e estreito (o elmo comprido, a fenda até o queixo,
o pescoço fino) e as ombreiras como duas bolas soltas.

## A Abominação: três construções novas (`abominacao-c`, `-d`, `-e`)

Cada uma com um traço dominante e a corrupção no corpo, com poucos elementos. A paleta nova (`abominacao2`): a carne
morta com as sombras frias e o Vazio nas cores da Cria do Vazio.
- **C, a mandíbula torta** (camadas carne, boca, dentes, costura, olhos): a cabeça é quase só a boca; a mandíbula foi
  costurada torta (os dois pontos na dobradiça da esquerda), abre mais funda à direita; quatro presas desiguais; dentro,
  o Vazio no lugar da garganta, com o brilho no fundo.
- **D, as duas cabeças** (carne, cabeca, enxerto, rosto): o brutamontes com os braços e os ombros, e uma segunda cabeça,
  pálida, de outra pessoa (os olhos fundos e a boca aberta), enxertada no ombro por uma faixa de carne violeta: a
  corrupção é o que as une.
- **E, os espinhos** (carne, espinhos, rosto): o corpo curvado, com quatro lascas de obsidiana do Vazio rompendo os ombros
  e as costas (o brilho onde rasgam a carne), o rosto com as órbitas fundas e os olhos acesos, a boca fechada.
- **Na bancada (rascunhos, não guardados):** o primeiro desenho de cada um saiu como uma caixa com rosto de mascote (olhos
  amarelos e uma fileira de dentes); a fenda no peito ficou como uma joia, e a cabeça afundada sumia; a mandíbula reta
  virou um pote; os espinhos assimétricos leram como chifres. Resolveram: a cabeça subordinada ao traço dominante, as
  órbitas escuras, os braços separados do tronco e os espinhos em quatro.

## O Cavaleiro A2 (`cavaleiro-a2`), o A refinado

Camadas capa, armadura, viseira (a paleta do A, mais o meio-tom da sombra do elmo e o vão entre as placas). O elmo mais
largo (10 px) e mais curto, a fenda vertical só até a metade; a base do elmo abre num gorjal que liga às ombreiras;
cada ombreira é uma placa com a borda acesa e uma lâmina embaixo, cobrindo a borda do peitoral, que tem a quina no meio;
o corpo mais escuro que o elmo, a capa vinho atrás das ombreiras. Sem arma, sem crista, sem rosto. Na bancada: o
primeiro A2, claro e quadrado, lia como uma geladeira; o seguinte, com o peito estreito entre duas fendas, repetia o
centro alongado; a metade de sombra do elmo um passo mais clara separou a cabeça do corpo a 32.

## A minha leitura (quem escolhe é o Jean)

- **Abominação: prefiro a C.** A boca torta é o traço que se reconhece na carta a 32, ameaça sem precisar de detalhe e
  é dela (o Carniçal tem a boca vertical e vermelha; o Troll, verde, as presas para cima). **Limitação no tamanho real:**
  os dois pontos da costura na dobradiça quase não aparecem a 32 e podem passar por lascas de dente; o corpo fica
  reduzido aos ombros embaixo.
  - D: a ideia mais legível de "ninguém sabe o que ela foi antes"; **limitação:** a 32 a cabeça principal é pequena e o
    enxerto tem 3 px, quem carrega a leitura é a cabeça pálida.
  - E: a silhueta mais forte; **limitação:** a 32 os espinhos podem ler como chifres, perto do Caído e do Xamã Caído.
- **Cavaleiro: o A2.** O busto fica sólido e as placas se entendem; **limitação no tamanho real:** o corpo escuro se
  aproxima do fundo da carta e a leitura vem do elmo e das bordas das placas; a fenda em T é mais curta que a do A, que
  tinha a marca vertical mais forte.

## Processo da segunda rodada

- As grades à mão em `auxiliares/grades.py`, rascunhadas e conferidas a 32, 48 e 12× antes da fonte; as quatro grades
  da primeira rodada saem idênticas.
- As fontes pelo Aseprite em lote (`python auxiliares/exportar.py --montar <id>`: o `montar_camadas.lua` com o
  `pintar.lua`, 0 diferentes e 0 fora da tela na releitura de cada camada), porque o conector estava sem editor e a
  janela aberta do Aseprite não foi tocada. A exportação do Aseprite (o composto das camadas) igual à grade, o @2x exato,
  o 32 e o 48 em blocos inteiros.
- As fotos a 1920×945 em `capturas-2/` (`MODOS=atual,a,c,d,e,a2`; o A2 refotografado depois do ajuste do elmo), sem erro
  no console; as folhas `abominacao-cde.png` (o jogo de hoje × C × D × E) e `cavaleiro-a2.png` (o jogo de hoje × o A
  original × o A2), com a carta (real e 2×), o Bestiário (48), a fileira com os aprovados (real e 3×) e a 12×.

# A terceira rodada (22/10/2026, propostas; nada no jogo)

**Pedido do Jean:** a Abominação C escolhida como direção (sem aprovação para integração), para refinar a ligação da
mandíbula com a cabeça e o volume das bochechas; o Cavaleiro passa a ter uma referência principal, a imagem gerada
`ferramentas/arte/referencias/icones/Cavaleiro sombrio do Vazio.png` (a origem registrada no LEIA-ME de lá). A, A2 e B
ficam como histórico; a segunda rodada e as fotos dela continuam como estavam.

## A Abominação C2 (`abominacao-c2`), a C refinada

Camadas carne, boca, dentes, olhos. A boca continua enorme e torta, mas sai da carne: a abertura fica dentro do rosto
(colunas 4 a 13), com a bochecha acesa à esquerda e a da direita na sombra; o lábio de cima pesa sobre a abertura; o
canto esquerdo fica alto (linha 8) e a mandíbula cai à direita até a linha 13, com o lábio de baixo aceso em diagonal.
As presas desiguais (a de cima à esquerda, longa; uma pequena à direita; uma de baixo; a grande da direita); o brilho do
Vazio só no fundo, do lado da garganta. Os dois pontos da costura saíram: a mandíbula agora se prende pela carne, e eles
liam como lascas de dente. Na bancada: a primeira C2, com a boca reta, virou um sorriso largo; a segunda, inclinada,
encolheu a boca; a terceira devolveu o tamanho (a abertura uma coluna antes e alta à direita).

## O Cavaleiro T (`cavaleiro-t`), a transposição da referência

- **A guia** (`guias/cavaleiro-t-guia-16.png`, a camada `guia` oculta na fonte, fora da exportação): o recorte quadrado
  de 1200 px a partir de (27, 54) da referência (1254×1254, ampliada; não é grade nativa), reduzido a 16 por média (75 px
  por pixel). A fonte é montada em lote e a guia é escondida em seguida (`exportar.py --montar`); a exportação igual à
  grade confirma que ela ficou fora.
- **Medido e redesenhado à mão:** a ponta do elmo nas colunas 7 e 8 (linha 0) e o elmo já na largura toda na linha 3
  (colunas 4 a 12); a frente acesa à esquerda, com a borda clara descendo da ponta, e a lateral escura com a emenda das
  placas (coluna 10); a viseira estreita subindo para a direita (linha 6 nas colunas 4 a 8, linha 5 nas 9 a 11), com a
  borda acesa logo abaixo e o violeta em (7,6); a quina na coluna 5 descendo até o queixo (linha 10); o gorjal escuro
  com a borda acesa em diagonal, subindo para a direita; as ombreiras em duas placas, a da esquerda maior e mais acesa; a
  capa vinho atrás dos ombros; o peitoral com a borda de cima acesa.
- **Simplificado de propósito:** as várias divisões do gorjal e do peito viram uma borda em diagonal de cada; os reflexos
  ficam nas bordas de cima das placas.
- A paleta (`cavaleiro_t`): a da referência, com seis valores de aço (do vão à borda clara), o violeta e dois vinhos.
- **Na bancada:** a primeira deixava a quina como uma faixa clara do topo ao peito (o centro alongado de novo) e a
  viseira sumia; a segunda afinava o alto como um cone; o elmo foi alargado na linha 3, a fenda ganhou a borda acesa e o
  gorjal perdeu o ruído.

## A minha leitura (quem escolhe é o Jean)

- **C2:** a mandíbula parece presa ao rosto e a boca continua o traço da carta; **limitação no tamanho real:** a 32 a
  bochecha da direita, na sombra, quase se funde com a borda, e o conjunto lê mais como uma cabeça só do que como cabeça
  e ombros.
- **T:** a pose, a ponta do elmo, a viseira inclinada e a capa vêm da referência; **limitação no tamanho real:** é o
  retrato mais escuro da fileira, e a 32 a viseira lê sobretudo pelo ponto violeta, porque a fenda tem 1 px.

## Processo da terceira rodada

- As grades à mão em `auxiliares/grades.py` (as de antes saem idênticas); as fontes pelo Aseprite em lote (o conector
  continuou sem editor; a janela aberta não foi tocada), 0 diferentes e 0 fora da tela na releitura de cada camada,
  inclusive a guia; a exportação igual à grade, o @2x exato, o 32 e o 48 em blocos inteiros.
- As fotos a 1920×945 nos modos `c2` e `t`, em `capturas-2/` (os mesmos cenários das anteriores), sem erro no console;
  as folhas compactas `abominacao-c2.png` (a C × a C2) e `cavaleiro-t.png` (a referência, a guia e o T a 12×; o jogo de
  hoje × o T na carta e no Bestiário; a fileira).

# A quarta rodada (22/10/2026, propostas; nada no jogo)

**Avaliação do Jean:** a C2 exagerou a assimetria (a bochecha esquerda volumosa, o canto direito caído demais, a
expressão caída, a mandíbula sem ligação); a orientação de mandíbula muito torta fica substituída por "deformação
monstruosa com estrutura legível". No T, o busto (os ombros, a capa e a parte de baixo) foi bem recebido; o elmo perdeu a
perspectiva da referência (o topo para um lado, a viseira para outro, o ponto violeta central como um olho de ciclope).
C, C2 e T ficam como histórico; as cópias novas são `abominacao-c3` e `cavaleiro-t2`.

## A Abominação C3 (`abominacao-c3`), de novo a partir da C

Camadas carne, boca, dentes, olhos. A boca enorme (dez colunas, como na C) fica centralizada sob o rosto e sustentada dos
dois lados por bochechas de carne; o lábio de cima ganha volume (aceso, pesando sobre a abertura, os cantos de cima
arredondados) e o de baixo é grosso e desigual. A irregularidade fica nos dentes (a presa longa à esquerda, uma pequena
em cima, uma de baixo e a grande da direita), na espessura da carne e nos cantos (o da direita uma linha mais largo); o
brilho do Vazio continua no fundo da garganta. Na bancada: a primeira C3 centralizou a boca mas a encolheu; a segunda
devolveu o tamanho e deixou o lábio de cima como uma linha reta que recortava; a terceira deu espessura ao lábio.

## O Cavaleiro T2 (`cavaleiro-t2`), o busto do T com o elmo refeito

Camadas guia (a mesma do T, oculta), capa, armadura, viseira. Da linha 8 para baixo é o T. O elmo foi resolvido primeiro
sem o brilho, pela referência: a ponta à esquerda (colunas 5 e 6), o topo descendo para a direita até a nuca; a quina
frontal na coluna 5, da testa ao queixo, com a frente estreita e acesa à esquerda dela; a lateral larga à direita, mais
escura, com a emenda das placas na coluna 9; a fenda atravessando a frente na linha 6 e subindo pela lateral na linha 5,
com a borda acesa embaixo; a base apoiada no gorjal do T. Por último, o brilho: um pixel violeta apagado (`u`) dentro da
fenda, na lateral, fora do centro.

## A minha leitura (quem escolhe é o Jean)

- **C3:** a boca continua o traço da carta e agora parece presa ao rosto, sem cair; **limitação no tamanho real:** com
  a boca centralizada e as bochechas dos dois lados, o rosto fica mais simétrico e um pouco menos monstruoso que a C.
- **T2:** a 32 e a 48 se percebe que ele olha para a esquerda, como na referência; **limitação no tamanho real:** o
  violeta apagado quase some a 32, e a viseira lê pela fenda escura e pela borda acesa.

## Processo da quarta rodada

- As grades à mão em `auxiliares/grades.py` (as de antes saem idênticas); as fontes pelo Aseprite em lote (o conector
  continuou sem editor; a janela aberta não foi tocada), 0 diferentes e 0 fora da tela na releitura de cada camada;
  a guia do T2 oculta (conferido na fonte: `guia=false`); a exportação igual à grade, o @2x exato, o 32 e o 48 em blocos
  inteiros.
- As fotos a 1920×945 nos modos `c3` e `t2`, em `capturas-2/` (os mesmos cenários e enquadramentos), sem erro no console.
- As folhas compactas `abominacao-c3.png` (a C × a C2 × a C3) e `cavaleiro-t2.png` (a referência, a guia e o T2 a 12×;
  a orientação no tamanho do retrato: a referência reduzida, o T e o T2 a 32 e 48; o T × o T2 na carta e no Bestiário; a
  fileira).

# A quinta rodada (22/10/2026, propostas; nada no jogo)

**Avaliação do Jean:** a Abominação C3 aceita visualmente, preservada sem retoques (ainda sem autorização para integrar).
No Cavaleiro, a capa vinho e as ombreiras do T2 ficam; o elmo, o gorjal e o peito são refeitos em três propostas
realmente diferentes, com liberdade de direção, perspectiva, proporção e tipo de elmo. A referência gerada deixa de ser
molde e fica como apoio do material e da atmosfera (sem guia nesta rodada). T2 e as anteriores ficam como histórico.

## Os três Cavaleiros (`cavaleiro-p1`, `-p2`, `-p3`)

Camadas capa, armadura, viseira, na paleta do T (`cavaleiro_t`). A capa e as ombreiras são as do T2, pixel a pixel
(conferido: 0 pixels diferentes nas ombreiras e na capa das três). A armadura foi resolvida sem o brilho; o violeta entrou
depois, só onde ajudou a expressão.
- **P1, o grande elmo** (sem brilho): de frente, o topo chato visto um pouco de cima, as duas fendas descendo para o
  centro (o olhar severo) com a barra do nariz e a quina até a base, a metade direita na sombra; o elmo assentado numa
  borda escura, o gorjal em duas lâminas retas, o peito com a quilha acesa no meio e a fralda embaixo.
- **P2, o bico:** de perfil, olhando para a esquerda: o bacinete com o bico da viseira projetado, a fenda ao longo do
  bico com um ponto violeta apagado perto da ponta, a nuca arredondada à direita descendo até o gorjal; o gorjal e o peito
  em placas diagonais, acompanhando a cabeça.
- **P3, a cabeça baixa:** a cúpula pequena com a crista acesa no meio (diz para onde a cabeça baixa aponta), a lateral
  direita escura, afundada num gorjal alto de borda acesa; a fenda baixa com dois pontos violeta apagados (o olhar de
  baixo); o peito largo e liso, com a borda de cima e a fralda.
- **Na bancada:** o primeiro P1, com as fendas retas, lia como um rosto de robô; o primeiro P3 era um ovo liso sobre um
  bloco (a crista, a lateral escura e as lâminas do gorjal resolveram), e uma versão dele tinha deslocado a borda da capa.

## A minha leitura (quem escolhe é o Jean)

- **Prefiro o P2.** É o que mais claramente olha para algum lugar, e o bico dá uma silhueta que não se confunde com o
  Esqueleto de Guarda nem com o Mercenário. **Limitação no tamanho real:** a 32 o bico tem 2 a 3 px e a fenda é fina; o
  ponto violeta quase não aparece.
- **P1:** o mais pesado e frontal; **limitação:** a 32 as duas fendas com a barra podem ler como um rosto de máscara ou
  de robô, e é o mais claro dos três.
- **P3:** o mais ameaçador pela postura; **limitação:** a cabeça pequena afundada perde a presença do elmo na carta, e
  os dois pontos violeta leem como olhos.

## Processo da quinta rodada

- As grades à mão em `auxiliares/grades.py` (as de antes saem idênticas); as fontes pelo Aseprite em lote (o conector
  continuou sem editor; a janela aberta não foi tocada), 0 diferentes e 0 fora da tela na releitura de cada camada; a
  exportação igual à grade, o @2x exato, o 32 e o 48 em blocos inteiros.
- As fotos a 1920×945 nos modos `p1`, `p2` e `p3`, em `capturas-2/` (os mesmos cenários e enquadramentos), sem erro no
  console; a folha compacta `cavaleiro-p.png` (o T2 × P1 × P2 × P3 na carta, real e 2×, no Bestiário e na fileira com os
  aprovados; a 12×).

# A sexta rodada (22/10/2026, proposta; nada no jogo)

**Pedido do Jean:** o P3 e o T2 são as direções preferidas (nenhum aprovado). Refinar o P3 mantendo o peso do busto, a
capa e as ombreiras, com o capacete mais definido, usando como referência de construção o retrato aprovado do Guerreiro
protagonista (não o ícone de equipamento do elmo). O problema do P3: o capacete pequeno e afundado, e a faixa clara do
gorjal dominando a cabeça. A Abominação C3 continua aceita visualmente, sem retoques.

## A referência: a carta do Guerreiro

`GUERREIRO_CARTA` em `rpg/web/static/retratos.js` (16×16, paleta `FERRO_LA`; aprovada no `retrato-teste.html`). O que
se aproveita da construção: o elmo grande (12 colunas por 11 linhas), dois planos de metal (o aceso à esquerda e a
sombra à direita) separados por uma nervura central, uma faixa de reforço acima da fresta, a fresta atravessando a
frente e a gola escura embaixo, que separa a cabeça do corpo. Não foi feita pesquisa externa: a carta do Guerreiro
bastou como solução legível no mesmo tamanho.

## O Cavaleiro P4 (`cavaleiro-p4`), o P3 refinado

Camadas capa, armadura, viseira (a paleta `cavaleiro_t`). Adaptado ao inimigo, sem recolorir o Guerreiro:
- **O elmo** maior e mais presente: 10 colunas, das linhas 0 a 9, com a cúpula e a crista do P3 (a nervura clara só na
  crista, para não formar a cruz de reforço do Guerreiro), a frente acesa à esquerda e a sombra à direita, uma linha de
  reforço escura acima da viseira.
- **A viseira em V:** as pontas de dentro mais baixas que as de fora, cortada pela emenda dos planos, dando o olhar
  bravo e de frente.
- **A separação:** a base do elmo é uma linha escura (linha 10); embaixo, o gorjal estreito em meio-tom (linha 11), sem a
  faixa clara do P3; depois, o peito.
- **O que ficou do P3:** as ombreiras e as linhas 12 a 15 (o peito) iguais pixel a pixel; a capa com um pixel movido de
  (3,8) para (2,8), para abrir espaço ao elmo maior.
- **Sem brilho:** os dois pontos violeta nas pontas da fenda leram como dois olhos (como no P3) e não melhoraram a
  expressão.
- **Na bancada:** o primeiro P4 tinha o rosto do elmo uma linha mais curto; o segundo cresceu, mas a nervura clara com a
  faixa da testa formou uma cruz grande, parecida demais com a do Guerreiro; o terceiro (o escolhido) apagou a faixa e
  deixou a nervura clara só na crista.

## A minha leitura (quem escolhe é o Jean)

- **P4:** a cabeça tem presença parecida com a do T2 e fica separada do gorjal e do peito; a viseira em V diz para onde
  ele olha. **Limitação no tamanho real:** a 32 a metade direita da fenda some no metal escuro, e a viseira lê pela
  metade acesa; o elmo continua menor que o do Guerreiro (10 colunas contra 12), para caber as ombreiras pesadas.

## Processo da sexta rodada

- A grade à mão em `auxiliares/grades.py` (as de antes saem idênticas); a fonte pelo Aseprite em lote (o conector
  continuou sem editor; a janela aberta não foi tocada), 0 diferentes e 0 fora da tela na releitura de cada camada; a
  exportação igual à grade, o @2x exato, o 32 e o 48 em blocos inteiros.
- As fotos a 1920×945 no modo `p4`, em `capturas-2/` (os mesmos cenários e enquadramentos), sem erro no console; a folha
  compacta `cavaleiro-p4.png` (o T2 × o P3 × o P4 na carta, real e 2×, e no Bestiário; a fileira com os aprovados e o
  Guerreiro, real e 3×; a 12× do Guerreiro, do T2, do P3 e do P4).

# A integração do Cavaleiro Sombrio (1.187.0): o P3

**Decisão do Jean:** o P3 original aprovado para integração, sem retoques (não o P4). A leitura dele, segundo o Jean,
é a de uma cabeça aparentemente exposta com a parte de baixo do rosto coberta por uma proteção; é uma interpretação do
desenho, não um pedido para mudar o desenho nem a descrição no jogo. O A, o A2, o B, o T, o T2, o P1, o P2 e o P4 ficam
como histórico; a Abominação C3 continua aceita visualmente e intacta, fora do jogo.

- **A fonte:** primeiro a do P3 (`fontes/cavaleiro-p3/`, sem alteração desde o `6e255ec4`), copiada byte a byte e
  conferida (os seis iguais à proposta). Na mesma entrega, vendo o cartaz do mural, o Jean pediu para completar os
  pedaços que faltavam nos cantos de baixo: o **P3b** (`cavaleiro-p3b`) é o P3 com a linha 15 completa (a lâmina de baixo
  da ombreira esquerda até a borda, colunas 0 a 2, e a coluna 15 da direita, nos tons das lâminas; 4 pixels, nada mais).
  O P3 fica como histórico. A fonte do P3b (camadas capa, armadura, viseira; 0 diferentes na releitura) foi copiada byte a
  byte para `ferramentas/arte/aseprite/retrato-cavaleiro-sombrio/retrato-cavaleiro-sombrio-16.aseprite`; o 32 e o 48
  registrados em `DERIVADOS` (`exportar_aseprite.py`), com os @2x.
- **Antes de gravar no jogo:** exportados numa pasta temporária e comparados com a proposta (`proposta/cavaleiro-p3b-*`):
  os seis arquivos iguais byte a byte. Depois de gravar, o `--conferir`: tudo igual ao jogo, o 32 e o 48 em blocos
  inteiros que reduzem ao 16.
- **No jogo:** pela família (`RETRATO_FAMILIA` em `rpg/dados.py`; o papel `CRIATURA` e os tamanhos em
  `rpg/web/static/icones.js`), com os afixos e o Último Guarda (`sistemas/chefes.py` o cria da família
  `cavaleiro_sombrio`, com nome próprio). O sprite `caveira` continua compartilhado com a Bruxa Afogada, o Lich Menor
  (pelos traços) e o servo do Necromante; nenhuma regra mudou.
- **Conferido com os arquivos de produção** (`auxiliares/fotografar_jogo.mjs`, `capturas-1187/`, a 1920×945, nada
  trocado na página): o cavaleiro na luta com o esqueleto e o mercenário; o Último Guarda (o cavaleiro de nome próprio,
  pelo `auxiliares/cenario_guarda.py`, que o cria como `chefes.py`); o Bestiário com a faixa do mestre caçador; o cartaz
  do mural e o rastreador do contrato. Todos com `retrato-cavaleiro-sombrio-32/48`, nenhum pedido a `ferramentas/`, sem
  erro no console. A folha `../integracoes-22-10/integracoes-1187.png`.

# A integração da Abominação (1.188.0): a C3

**Decisão do Jean:** a C3 aprovada para integração, sem retoques. A, B, C, C2, D e E ficam como histórico; o Cavaleiro
P3b da 1.187.0 fica como está.

- **A fonte:** `fontes/abominacao-c3/abominacao-c3-16.aseprite` (sem alteração desde o `961e574a`), copiada byte a byte
  para `ferramentas/arte/aseprite/retrato-abominacao/retrato-abominacao-16.aseprite` (camadas carne, boca, dentes,
  olhos); o 32 e o 48 em `DERIVADOS` (`exportar_aseprite.py`), com os @2x.
- **Antes de gravar no jogo:** exportados numa pasta temporária e comparados com a proposta (`proposta/abominacao-c3-*`):
  os seis iguais byte a byte. Depois, o `--conferir`: tudo igual ao jogo, o 32 e o 48 em blocos inteiros do 16.
- **No jogo:** pela família (`RETRATO_FAMILIA`; o papel `CRIATURA` em `icones.js`), com os afixos (o afixo corrompido
  também: a família vem antes dos traços). O sprite `corrompido` não perde uso: fica para quem tiver o traço sem retrato
  próprio (o afixo corrompido na Árvore Desperta, no golem e nos guardiões que seguem pelos traços); nenhuma regra nem
  atributo mudou.
- **Conferido com os arquivos de produção** (`auxiliares/fotografar_jogo_abominacao.mjs`, `capturas-1188/`, a 1920×945,
  nada trocado na página): a abominação na luta com o troll, o carniçal e o cavaleiro; o Bestiário com a faixa do mestre
  caçador; o cartaz e o rastreador. Todos com `retrato-abominacao-32/48`, nenhum pedido a `ferramentas/`, sem erro no
  console. A folha `../integracoes-22-10/integracoes-1188.png`.
