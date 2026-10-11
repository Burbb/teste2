# 17 — Avaliação integrada do Vale (E9): diagnóstico e roteiro de validação

Primeira entrega da E9 antecipada (decisão de Jean, 11/10/2026): diagnóstico do Vale do Turvo como primeiro capítulo
e preparação da validação humana. **Nada do jogo mudou.** Regras, números e recompensas ficam como estão na 1.63.0
até Jean decidir. As propostas abaixo são propostas.

**A E9 não está concluída.** A validação técnica não substitui Jean jogando nem as partidas de jogadores novos
(seção 9).

## 1. Resumo

**Antes de liberar o capítulo para teste, resolver:**

1. **A fome pode prender o save** (seção 4.5). Na campanha, a queda em combate leva ao resgate, mas a fome e a
   infecção matam. O save automático fica na véspera da morte. Sem comida, sem ouro e sem o que vender, não há saída
   razoável: o jogador perde a partida inteira. Nos percursos do robô, 424 de 540 passaram por "sem comida e sem
   ouro para comprar"; 162 morreram sem sair dele. O resgate piora: custa dois dias, e os dois dias comem
   provisões. A decisão estava registrada para Jean "antes da E9" ([12](12-E1-CAMPANHA.md), seção 6) e agora é
   urgente.
2. **O capítulo não termina para quem joga** (seção 3.3). Depois das duas missões, nada diz que a primeira parte
   acabou. A única pista é a Estrada de Varn fechada. Proposta: uma cena curta, uma vez, no Vau, com o que mudou.
3. **O companheiro come, e ninguém avisa antes** (seção 4.4). Cada companheiro gasta uma provisão por dia. A
   pergunta "Levar X com você?" não diz isso; só a dica do contador de provisões. Pelo critério editorial, o custo
   vem na nota da escolha.

**Confirmar com Jean jogando, antes de mexer em número:** o começo (níveis 1 e 2) é estruturalmente apertado. Uma
luta comum paga cerca de 1 de ouro e custa cerca de duas noites de comida para sarar. Num lugar do nível do herói,
com a vida cheia e duas poções, o herói de nível 1 perde de 10% a 22% das lutas no Charco, conforme a classe (o
Mago é o pior). Nenhuma estratégia simples do robô resolve (seção 4.3). O robô joga pior que uma pessoa em pontos
conhecidos (seção 4.4), então a medida diz "apertado", não "quanto".

**O que funciona, pela medida:**
- o percurso completo fecha com as três classes e os dois caminhos de Ilse, com as três posturas na praça;
- salvar e carregar mantém o estado em todos os pontos de mudança de missão medidos;
- a derrota para Ilse não perde a missão: o resgate devolve ao Vau, e ela espera inteira;
- nenhum bloqueio de jogo foi reproduzido. Os percursos que param são de fome, infecção ou do limite de dias do
  próprio robô.

## 2. Como foi avaliado

Reaproveitei as ferramentas que já existiam e acrescentei três opções à régua do Vale (`tests/saque_vale.py`). Ela
continua sem mudar o jogo: só joga e conta.

| Ferramenta | O que mostrou aqui |
|---|---|
| `tests.saque_vale` (o robô do Vale) | Percursos inteiros, por classe, desfecho e roteiro. Novo: a trajetória de cada percurso (dia, lugar, ouro, comida, fome, vida, nível, comitiva, ação), as pausas, as escolhas e os encontros |
| `--estrategia` | O começo com outras regras de compra, recrutamento e contrato (seção 4.3) |
| `--roteiros nivel6` | Quem explora três vezes por visita e só desce ao fundo no nível 6 |
| `--economia` | Uma luta comum do começo, no jogo de verdade: o que custa e o que paga |
| testes de missão | `test_campanha`, `test_missoes`, `test_caspar`, `test_retorno`, `test_guardia`, `test_yara_vau`, `test_broquel`, `test_golpe_preparado` |
| fumaça do navegador | Os cenários da capela, do sarilho, da guardiã, do retorno, da praça, de Caspar, da Yara e do Broquel |

**Amostras:**
- 480 percursos com o roteiro de sempre (3 classes × 2 desfechos × "direto" e "explorador" × 40 sementes);
- 540 percursos de ritmo (3 classes × 2 desfechos × "direto", "explorador" e "nivel6" × 30 sementes), com as
  trajetórias;
- 7 estratégias do começo × 3 classes × 2 desfechos × 40 sementes, no roteiro "direto";
- 60 lutas por classe, lugar e equipamento na conta da luta.

**O que o robô sabe e o que não sabe.** Ele não tem recurso de graça nem conhecimento antecipado. Mas:
- luta com a política da arena (`tests/arena.py`), razoável, não ótima;
- foge só abaixo de 35% da vida sem poção;
- caça contrato no nível do herói desde o nível 1;
- acampa até 85% da vida;
- vende toda a mochila a cada visita e nunca tira o que está vestido para vender;
- tem um limite de 45 dias, que não existe no jogo.

Por isso, cada achado abaixo diz se foi **reproduzido** no jogo, se é **hipótese** a confirmar jogando, ou se é
**limitação do roteiro**.

## 3. Percurso completo e encerramento

### 3.1 O que foi conferido

| Ponto | Como | Resultado |
|---|---|---|
| Da criação à resolução local, três classes | Percursos completos do robô | Fecha com as três. Completos no roteiro "direto": Guerreiro 29 de 60, Arqueiro 19, Mago 8. O resto para de fome, infecção ou no dia 45 (seção 4) |
| Os dois caminhos de Ilse | Desfecho "descansada" (Vó Berta, correntes, rito, herança) e "destruida" | Os dois fecham nas três classes |
| As três posturas na praça | Postura sorteada | Apoiar, Denunciar e Calar aparecem nos completos das três classes |
| Objetivos e Diário | Testes de missão; fumaça | A etapa avança, o Diário mostra a etapa, a Vigília "aguardando" e as "Concluídas" |
| Consequências | `test_retorno`, `test_caspar`, `test_yara_vau`; fumaça (retorno, praça, Yara) | Fonte Nova, a frase do Vau, Pita, Marta, a praça, a situação da Yara |
| Caspar e a comitiva | `test_caspar`, `test_custos_protecao`; fumaça | As reações e a saída de quem não aceita a postura |
| Recompensas pendentes | `test_retorno` (herança), `test_broquel` (ferreiro) | A herança espera no Vau; o Broquel vem no ossuário ou, num save antigo, na forja |
| Sair e voltar aos lugares | Trajetórias | O robô sai e volta à capela e ao Bosque várias vezes por percurso, sem perder etapa |
| Derrota | Trajetórias; `test_guardia` | A queda leva ao Vau. A missão fica onde estava. Ilse volta inteira, e o herói tenta de novo |
| Salvar e carregar | Novo nesta entrega, abaixo | Idêntico em todos os pontos |

**Salvar e carregar nos pontos relevantes.** Em 12 percursos completos (as três classes, os dois caminhos), o robô
salvou e carregou num jogo novo a cada mudança de etapa da Febre, da Vigília, de conclusão ou de lugar: de 17 a 20
pontos por percurso, 220 ao todo. Todos os campos do save, o herói e o estado do sorteio saíram idênticos.

### 3.2 Reproduzido, hipótese e limitação

- **Reproduzido:**
  - a fome prende o save (seção 4.5);
  - nenhum marco de fim do capítulo (seção 3.3);
  - o custo do companheiro fora da escolha (seção 4.4).
- **Hipótese, a confirmar jogando:**
  - o Guerreiro no caminho "destruir" perdeu para Ilse até quatro vezes num percurso (média de 1,0 a 1,9 descidas por
    classe e caminho, no nível 4). O resgate mantém a missão, então não é bloqueio. Se uma pessoa também cair
    várias vezes, a dúvida passa a ser de clareza: o jogo diz o bastante sobre o que preparar?
  - o Mago chega ao fundo bem mais tarde (nível 4 por volta do dia 22, contra o 18 e o 19 das outras classes).
- **Limitação do roteiro:**
  - os percursos que param no dia 45 param pelo limite do robô, não do jogo;
  - o robô oscila entre o Bosque e o Vau quando a comida está no fim e a comitiva tem dois: compra 5 dias, e a
    comitiva come 3 por noite. O jogo não força isso;
  - o robô não testa o modo texto nem a leitura. A fumaça e os cenários cobrem a tela, não a compreensão.

### 3.3 O jogador percebe que o capítulo terminou?

**Hoje, não.** Depois de concluir a Febre e a Vigília:
- o Diário move as duas para "Concluídas";
- o Vau mostra a frase da praça e a Fonte Nova;
- a Estrada de Varn continua fechada, com o texto "esta saída abre numa próxima parte da campanha", que só aparece
  se o jogador tentar ir até ela.

Nada fala do fim. O jogador fica no Vau com o mesmo menu de antes e pode concluir que falta alguma coisa ou que o
jogo travou.

**Proposta (a menor, com a apresentação que existe; não implementada):** uma cena, uma vez, ao entrar no Vau com as
duas missões concluídas.
- **Forma:** a cena de missão que já existe (cartão com título, narração e Continuar), como as cenas do retorno.
- **Conteúdo:** só o que já está decidido no jogo:
  - a Fonte (a febre acabou);
  - a linha de Ilse (`caspar.linha_ilse`);
  - a de Caspar (`caspar.LINHA_CASPAR`);
  - a da Yara (`caspar.linha_yara`), se houver.
  Essas linhas já aparecem no Diário. A cena junta numa tela, com uma frase de fecho.
- **O que diz no fim, claro:** "A primeira parte da história termina aqui. A Estrada de Varn abre na próxima parte.
  Você pode continuar explorando o Vale." Sem antecipar o que vem em Varn.
- **Fica no Diário:** uma linha "Primeira parte concluída".
- **Não fazer:** cena nova de história, epílogo, recompensa, abrir Varn.

## 4. O começo (níveis 1 e 2)

### 4.1 O que se vê

Em 480 percursos do roteiro de sempre, param antes do fim: Guerreiro 91 de 160, Arqueiro 100, Mago 140. Quase todos
no nível 1 ou 2 e quase todos de fome:

| Classe | Completos | Fome | Infecção | Dia 45 (robô) | Nível ao parar (os mais comuns) |
|---|---|---|---|---|---|
| Guerreiro | 69 | 70 | 8 | 13 | 1 (38), 2 (30), 3 (12) |
| Arqueiro | 60 | 75 | 4 | 21 | 1 (32), 2 (26), 3 (20) |
| Mago | 20 | 91 | 20 | 29 | 1 (50), 2 (38), 3 (26) |

**A primeira queda vem cedo.** Em 410 dos 540 percursos de ritmo o herói cai pelo menos uma vez. A primeira queda é,
em média, no dia 6,6, e 238 delas no nível 1. A ação antes da queda:
- caçar contrato: 133;
- acampar (emboscada): 116;
- explorar: 80;
- viajar: 48.

**Um caso, passo a passo** (Guerreiro, semente 4, "direto"):
- dia 1: 10 de ouro e 5 de comida depois das compras;
- dia 2: caça o contrato do Charco e cai. Acorda no Vau no dia 4: perdeu 30% do ouro e comeu 2 provisões;
- dia 4: cai de novo na estrada; acorda no Vau no dia 6 com 1 provisão e 3 de ouro;
- dia 7: sem comida;
- dia 9: terceira queda; acorda no Vau com 2 dias de fome e 3 de ouro (a provisão custa 4);
- dia 12: morre de fome no Charco, no nível 1.

### 4.2 A conta de uma luta

Uma luta comum, no jogo de verdade: o herói de partida (ou com o equipamento básico do nível), vida cheia, duas
poções, contra o grupo que o lugar sorteia (`--economia`, 60 lutas por linha).

| Classe | Lugar | Equipamento | Vitórias | Derrotas | Vida perdida | Poções gastas | Ouro | Ferimento | Noites para sarar |
|---|---|---|---|---|---|---|---|---|---|
| Guerreiro | Charco | de partida | 73% | 13% | 48% | 0,67 | 1,2 | 10% | 2,1 |
| Guerreiro | Charco | vestido | 82% | | 36% | 0,58 | 1,3 | 10% | 1,7 |
| Guerreiro | Bosque | de partida | 63% | 22% | 55% | 0,73 | 0,0 | 30% | 2,4 |
| Guerreiro | Bosque | vestido | 80% | | 41% | 0,62 | 0,6 | 20% | 1,9 |
| Arqueiro | Charco | de partida | 80% | 10% | 46% | 0,47 | 1,2 | 18% | 2,0 |
| Arqueiro | Charco | vestido | 88% | | 33% | 0,37 | 1,3 | 13% | 1,6 |
| Arqueiro | Bosque | de partida | 67% | 25% | 53% | 0,62 | −0,2 | 28% | 2,3 |
| Arqueiro | Bosque | vestido | 80% | | 42% | 0,45 | 0,5 | 18% | 2,0 |
| Mago | Charco | de partida | 72% | 22% | 52% | 0,45 | 1,4 | 27% | 2,2 |
| Mago | Charco | vestido | 80% | | 39% | 0,43 | 1,5 | 25% | 1,8 |
| Mago | Bosque | de partida | 58% | 35% | 59% | 0,55 | 0,5 | 28% | 2,5 |
| Mago | Bosque | vestido | 60% | | 53% | 0,57 | 0,5 | 33% | 2,3 |

O que não é vitória nem derrota é fuga. As derrotas foram contadas só com o equipamento de partida.

**A conta:**
- a luta paga cerca de 1 de ouro (as feras quase não deixam);
- sarar custa duas noites acampado, uma provisão por boca por noite: uns 8 de ouro para o herói sozinho;
- metade das lutas gasta uma poção (40 de ouro);
- nos níveis 1 e 2, lutar dá XP e perde dinheiro. O que paga a viagem são os contratos, os eventos e os baús, e
  quem para viu de 0,2 a 0,4 baú e ganhou de 36 a 65 de ouro no total.

### 4.3 Estratégias simples de um jogador informado

Mudei só as regras do robô que uma pessoa mudaria sabendo o que o jogo já mostra. Nenhum recurso de graça, nenhum
conhecimento do que vem. Completos em 40 percursos, roteiro "direto", caminho "descansada":

| Estratégia | O que muda | Guerreiro | Arqueiro | Mago |
|---|---|---|---|---|
| atual | (o roteiro de sempre) | 19 | 17 | 6 |
| comida do grupo | leva 3 dias de comida por boca | 21 | 13 | 7 |
| poupar | e, antes do nível 3, só compra equipamento para espaço vazio | 16 | 18 | 8 |
| só depois do 3 | comida do grupo, e só aceita companheiro a partir do nível 3 | 16 | 14 | 8 |
| cuidadoso | comida do grupo, poupar e companheiro a partir do 3 | 15 | 16 | 9 |
| só bando | comida do grupo, e só caça de bando (nenhum alvo com nome) | 15 | 5 | 5 |
| contrato depois do 3 | comida do grupo, e nenhum contrato antes do nível 3 | 12 | 10 | 7 |

**Nenhuma resolve.** As diferenças estão dentro do ruído de 40 sementes, exceto uma: fugir dos contratos piora,
porque eles são a renda do começo.

### 4.4 O que é do robô e o que persiste

**É do robô (uma pessoa provavelmente faz melhor):**
- caçar o contrato com nome no nível 1, com a vida pela metade (na trajetória, uma caça leva o Mago de 92% a 3% da
  vida);
- fugir tarde (abaixo de 35%);
- vender toda a mochila sem guardar um item para a fome;
- nunca tirar o equipamento vestido para vender numa emergência;
- oscilar entre o Bosque e o Vau com a comida no fim.

**Persiste com decisões razoáveis** (as estratégias da seção 4.3 e a conta da 4.2 mostram isso):
- uma luta comum dá prejuízo nos níveis 1 e 2;
- o herói de nível 1, inteiro e com poções, perde uma luta comum em cada 5 a 10 no lugar mais fácil;
- o resgate custa 30% do ouro **e** dois dias de comida, justo quando falta as duas coisas;
- o companheiro dobra ou triplica o consumo de comida, e o jogador só descobre pelo contador;
- dormir na taverna custa de 10 a 12 de ouro e cura 35%; acampar custa uma provisão (4) e cura 30%. A cama da vila
  só vale pelo risco de emboscada.

**O companheiro come, e a escolha não diz.** A pergunta do recrutamento ("Levar X com você?", em
`rpg/comitiva/grupo.py`) tem "Aceitar" e "Recusar", sem nota de custo. Pelo critério editorial (07), o custo vem na
nota da alternativa.

### 4.5 A armadilha: fome, resgate e save automático

**Reproduzido.** Com o save automático ligado (como numa partida de verdade), a semente 4 do Guerreiro acaba assim:
o save fica no Charco, dia 12, de manhã, com 2 de vida em 39, 5 dias de fome, nenhuma provisão, 3 de ouro, a mochila
vazia e só a arma de partida. A próxima noite mata (a fome tira 20% da vida máxima por dia).

**Como se chega lá:**
- a queda em combate leva ao resgate: 30% do ouro e dois dias, e os dois dias comem provisões (`novo_dia` duas
  vezes);
- a fome e a infecção chamam `fim_de_jogo`, mesmo na campanha. Fora do modo hardcore, o save não é apagado, mas o
  save automático já está na véspera, e o sorteio salvo repete a mesma noite;
- a saída que sobra é tirar a arma de partida e vendê-la (7 de ouro) para comprar comida. O jogo permite, mas não
  sugere, e o herói fica sem arma.

**Medido** (540 percursos de ritmo):
- 424 ficaram sem comida e sem ouro para comprar, nas três classes (Guerreiro 132, Arqueiro 127, Mago 165);
- 262 voltaram a ter comida;
- 162 morreram sem voltar, em média 5 dias depois;
- todos os 303 percursos parados passaram por esse estado;
- os parados caíram, em média, 2,4 vezes; os completos, 0,9.

**O jogo avisa, mas o aviso não protege.** O prólogo da campanha diz: "A fome e uma infecção sem tratamento ainda
encerram a partida; o último save continua lá". O último save é o automático, da véspera. O [12](12-E1-CAMPANHA.md)
(seção 6) já registrava que um resgate sem comida pode emendar em morte por fome, e supunha que uma pessoa compra
comida. A medida mostra que o caminho até lá passa por quedas no nível 1 e por resgates que comem a comida, não só
por esquecer de comprar.

**Por que é prioridade:** é perda de progresso. Numa partida de uma hora ou mais, o jogador perde tudo por uma regra
que a campanha anunciou como recuperável ("resgate como padrão", [12](12-E1-CAMPANHA.md), seção 6).

### 4.6 Propostas para o começo

Pequenas, só onde a evidência sustenta. **Nenhuma aplicada.** A ordem é a de prioridade.

1. **Decidir a fome e a infecção na campanha** (pendência do 12, seção 6). Recomendação: na campanha fora do
   hardcore, a fome e a infecção que matariam levam ao resgate, como a queda. O custo do resgate fica. Assim, a regra
   "na campanha, a derrota se recupera" vale para tudo.
2. **O resgate do Vau não come a bolsa.** Na casa de Marta, alguém dá de comer. Os dois dias passam (o tempo do
   mundo segue), mas sem gastar provisões, como a refeição da taverna. Com a proposta 1, isso evita que o resgate
   leve direto a outro resgate.
3. **A nota do recrutamento:** "Come 1 provisão por dia". Uma linha, na nota da alternativa.
4. **Depois de Jean jogar, se o começo ainda apertar:** olhar o ouro das feras ou o preço da cama do Vau. Isso é
   número de balanceamento: vai pelo ciclo do COMO_CRIAR, com `tests.equilibrio` e `tests.replay` antes e depois.

**Não propor agora:** mudar a dificuldade das lutas do nível 1, dar ouro ou comida de partida, ou mudar contratos.
Primeiro ver se as propostas 1 a 3 e uma pessoa jogando mudam o quadro.

## 5. Ritmo, progressão e saque

Contagens dos percursos completos de ritmo. **Não são duração.** Dia do jogo e tempo de teste não dizem quanto uma
pessoa leva.

| Roteiro | Lutas | Viagens | Pausas de leitura | Escolhas fora da luta | Delas, rotina | Cartões de item | Outras escolhas |
|---|---|---|---|---|---|---|---|
| direto | 21–24 | 23–34 | 78–104 | 158–210 | 95–129 | 10–12 | 47–70 |
| explorador | 26–34 | 25–34 | 99–126 | — | — | 13–14 | 61–82 |
| nível 6 | 34–38 | 32–40 | 125–143 | — | — | 16–19 | — |

"Rotina" são as escolhas que se repetem a cada visita: comprar comida, dormir, acampar, seguir viagem. "Outras" são
eventos, conversas, missão e especialização. As faixas vão da classe com menos à classe com mais.

**Repetição:**
- dos eventos vividos, 29% são repetidos no roteiro "direto" (10,8 de 37) e cerca de 50% no "nível 6" (36 de 71).
  Os que mais voltam: encontro hostil, olhos na escuridão, visitante misterioso, ladrão noturno;
- a família de inimigos mais comum é de 22% a 26% das lutas de um percurso.

**Progressão** (dia mediano em que o robô chega a cada nível, todos os percursos que chegam):

| Classe | Nível 2 | Nível 3 | Nível 4 | Nível 5 | Nível 6 |
|---|---|---|---|---|---|
| Guerreiro | 3 | 8 | 19 | 28 | 39,5 |
| Arqueiro | 3 | 7 | 18 | 29 | 38,5 |
| Mago | 4 | 13 | 22,5 | 34,5 | 43 |

- do 3 ao 4 são cerca de dez dias de jogo, e é a espera mais longa antes do fundo. O nível 4 para o fundo é regra do
  robô, não do jogo. Uma pessoa pode descer antes;
- o nível 6 fica no fim do capítulo, só para quem explora muito. Chegaram 28 Guerreiros, 16 Arqueiros e 5 Magos de
  180 cada.

**Nível 6, Muralha e Broquel:**
- dos 17 Guerreiros que completaram no roteiro "nível 6", 5 tinham a Muralha (o robô escolhe talento ao acaso) e 4
  usavam o Broquel no fim;
- o robô compara equipamento pela soma dos bônus. O Broquel tem bônus de raro e vale pelo Revide, que o robô não
  enxerga. Ele troca o Broquel por um escudo de bônus maior;
- isso diz que o valor do Broquel está só no efeito e no cartão. Se Jean também trocar o Broquel sem pensar, a
  dúvida é se a comparação "▲ Revide / ▼ sem Revide" pesa o bastante. É para observar, não para mudar agora.

**Saque** (medido na E7, [16](16-E7-ITEM-E-LOOT.md), seção 3.1): depois de um suprimento por baú na campanha, os
suprimentos de baú caíram de 9,7 para 6,3 por Vale e as poções no fim, de 3,0 para 2,4. O começo não mudou: quem para
viu menos de meio baú.

**Leitura:** de 78 a 143 pausas por Vale completo. Não sei quanto disso cansa; é o que Jean e os jogadores novos
dizem (ficha, seção 9).

## 6. Achados por prioridade

| # | Prioridade | Achado | Evidência | Proposta | Antes de liberar? |
|---|---|---|---|---|---|
| 1 | Bloqueio ou perda de progresso | A fome e a infecção matam na campanha; o save automático fica na véspera | Reproduzido (4.5); 162 de 540 percursos | Fome e infecção levam ao resgate na campanha (4.6, 1) | **Sim** |
| 2 | Bloqueio ou perda de progresso | O resgate come dois dias de provisões, e isso leva a outro resgate | Reproduzido (4.1, 4.5) | O resgate do Vau não come a bolsa (4.6, 2) | **Sim**, junto com o 1 |
| 3 | Clareza e coerência | O capítulo não termina para quem joga | Reproduzido (3.3) | Cena curta de fim de capítulo no Vau (3.3) | **Sim** |
| 4 | Clareza e coerência | O custo do companheiro não aparece na escolha | Reproduzido (4.4) | Nota "Come 1 provisão por dia" (4.6, 3) | **Sim** (uma linha) |
| 5 | Ritmo e equilíbrio | Nos níveis 1 e 2, lutar dá prejuízo, e o herói inteiro perde de 10% a 22% das lutas no Charco | Medido (4.2); persiste nas estratégias (4.3) | Ver com Jean depois de 1 a 4; número só pelo ciclo do COMO_CRIAR | Não: confirmar jogando |
| 6 | Ritmo e equilíbrio | O Mago fica bem atrás no começo (6 a 9 completos em 40) | Medido (4.1, 4.3) | O mesmo do 5 | Não: confirmar jogando |
| 7 | Ritmo e equilíbrio | Eventos repetidos: 29% num Vale direto, cerca de 50% para quem explora muito | Medido (5) | Nenhuma agora. Se Jean sentir a repetição, sortear sem repetir enquanto houver outro | Não |
| 8 | Ritmo e equilíbrio | Do nível 3 ao 4, cerca de dez dias de jogo | Medido (5), com a regra do robô | Nenhuma agora | Não |
| 9 | Acabamento | A cama do Vau rende menos que acampar | Contas (4.4) | Ver junto com o 5 | Não |
| 10 | Acabamento | O Broquel vale só pelo efeito, e a comparação por bônus o esconde | Medido (5) | Observar Jean | Não |

## 7. Antes de liberar o capítulo para teste

1. **Jean decide** a fome e a infecção na campanha e o resgate sem comer a bolsa (achados 1 e 2).
2. **Implementar** o que for decidido, a cena de fim de capítulo (achado 3) e a nota do recrutamento (achado 4).
   Com testes, gabarito e fumaça. Medir de novo o começo com `tests.saque_vale` (a mesma amostra) e registrar aqui.
3. **Jean joga** o capítulo inteiro (seção 8), e a ficha vai para os primeiros jogadores novos (seção 9).
4. **Só então** decidir números do começo (achados 5, 6 e 9).

## 8. Roteiro para Jean jogar

### 8.1 Partida nova completa (experiência e ritmo)

- Comece uma campanha nova pelo menu, com a classe que quiser. Jogue até o fim do capítulo, sem cenários.
- Jogue como jogaria, sem tentar testar nada. Se travar, morrer ou cansar, isso é a informação.
- Uma segunda partida, depois, com outra classe e o outro caminho de Ilse. Se puder, o Mago numa delas.
- Anote, de preferência na hora:
  - **dúvida:** onde não soube o que fazer, para onde ir ou o que uma escolha ia custar;
  - **repetição:** o que cansou (luta, evento, viagem, compra, texto);
  - **dificuldade:** onde caiu ou quase caiu, e se entendeu por quê;
  - **falta de retorno:** onde fez algo e a tela não mostrou o que mudou;
  - **fim:** quando percebeu que o capítulo acabou, se percebeu.
- Não precisa cronometrar. Se quiser, anote só a hora de começo e de fim, e as pausas longas.

### 8.2 Cenários direcionados (comparar e conferir ramos)

`python -m tests.navegador.cenarios <nome>`:

| Cenário | Para quê |
|---|---|
| `capela` | As salas da capela e o golpe preparado (`CLASSE`, `NIVEL`) |
| `capela` com `ETAPA=fundo` | A luta com Ilse: `PREPARO=pronto` para o rito, sem `PREPARO` para destruir |
| `retorno` | A volta ao Vau com Ilse resolvida: Fonte Nova, herança, as frases (`DESFECHO=descansada` ou `destruida`) |
| `praca` | Depois da resposta a Caspar (`POSTURA=apoiar`, `denunciado`, `denuncia_falhou` ou `calar`; `YARA=grupo`) |
| `broquel` | O escudo e o ataque, com e sem o Revide |
| `muralha` | A Muralha com o Contra-ataque, no nível 6 |
| `covil` com `EVENTO=odete_na_estrada` | Odette na estrada (mundo gerado) |

Exemplo: `ETAPA=fundo PREPARO=pronto CLASSE=mago NIVEL=4 python -m tests.navegador.cenarios capela`.

Nos cenários, anote só o que for do cenário: se a luta muda com a escolha, se o texto bate com o que você fez.

### 8.3 O que já sei que vai aparecer

Para não gastar anotação com o que já está na lista: a fome no começo (achados 1, 2 e 5), o fim sem marco (achado 3)
e o companheiro que come (achado 4). Se aparecerem, anote só se for diferente do que está aqui.

## 9. Ficha para jogadores novos

Para quem nunca jogou. Entregar depois da partida, não antes. As perguntas não dizem o que existe no jogo nem como
resolver.

```
Crônicas da Fenda: Vale do Turvo (versão ____)

1. Quanto tempo você jogou, mais ou menos? ____ (em quantas sessões? ____)
2. Que classe você escolheu? ______ Por quê? ______________________
3. Como terminou?
   ( ) cheguei ao fim da história   ( ) parei antes   ( ) morri e não continuei
   Se parou ou morreu: onde e por quê? ____________________________
4. Você achou que a história tinha terminado? ( ) sim  ( ) não  ( ) não sei
   O que te fez achar isso? ________________________________________
5. Além da história principal, o que você fez por conta própria?
   ________________________________________________________________
6. Em que momento você não soube o que fazer ou para onde ir?
   ________________________________________________________________
7. O que foi difícil? Você entendeu por que foi difícil?
   ________________________________________________________________
8. O que ficou repetitivo ou cansativo?
   ________________________________________________________________
9. Alguma escolha teve um resultado que você não esperava? Qual?
   ________________________________________________________________
10. Teve algum texto que você não entendeu ou pulou?
   ________________________________________________________________
11. Você jogaria de novo? Com o quê diferente?
   ________________________________________________________________
```

Se Jean puder sentar junto, vale mais olhar do que perguntar: onde a pessoa para, volta, relê ou desiste.

## 10. Decisões de Jean

| Decisão | Recomendação |
|---|---|
| Fome e infecção na campanha | Levar ao resgate, com o custo do resgate (4.6, 1) |
| O resgate do Vau e a comida | Os dois dias passam sem gastar provisões (4.6, 2) |
| O fim do capítulo | A cena curta no Vau, uma vez, com as linhas que já existem (3.3) |
| A nota do recrutamento | "Come 1 provisão por dia" |
| Números do começo | Depois de jogar com 1 a 4 aplicados |
| Como medir a primeira partida | A ficha da seção 9 e, se der, Jean junto olhando (10-DECISOES, "Como medir a primeira partida") |

## 11. Limitações

- O robô não lê, não se perde e não se cansa. Tudo de clareza e ritmo aqui é contagem, não experiência.
- A política de luta é a da arena: boa o bastante para comparar, não para dizer quanto uma pessoa perde.
- O limite de 45 dias é do robô.
- As estratégias usaram 40 sementes. Diferenças de 2 ou 3 percursos estão no ruído.
- A conta da luta usa o grupo sorteado pelo lugar, sem clima, sem noite e sem contrato.
- Nada aqui mede a leitura nem a duração. Isso vem da seção 9.

## 12. Para reproduzir

```
python -m tests.saque_vale --sementes 40                          # o roteiro de sempre (~50 s)
python -m tests.saque_vale --sementes 40 --roteiros direto --desfechos descansada --estrategia cuidadoso
python -m tests.saque_vale --sementes 30 --roteiros direto,explorador,nivel6
python -m tests.saque_vale --economia                             # a conta da luta (tabela 4.2)
```

As trajetórias, as pausas e os encontros estão em cada percurso que `medir` devolve (chaves `trajeto`, `pausas`,
`escolhas_fora`, `rotina`, `encontros`, `eventos`). A conta de "sem comida e sem ouro" e o salvar e carregar foram
feitos com scripts de uma vez, sobre essas chaves.
