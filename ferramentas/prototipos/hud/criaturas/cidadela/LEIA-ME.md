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
