# 17 — Avaliação integrada do Vale (E9): diagnóstico e roteiro de validação

Avaliação integrada do Vale do Turvo como primeiro capítulo (a E9 antecipada, decisão de Jean, 11/10/2026).

- **Primeira entrega (seções 1 a 12):** o diagnóstico e a preparação da validação humana, sobre a 1.63.0, sem mudar o
  jogo.
- **Segunda entrega, 1.64.0 (seções 13 a 16):** a partida de Jean como evidência humana, a recuperação no modo
  Resgate da campanha, o custo dos companheiros na escolha e o encerramento do capítulo. Dano, vida dos inimigos,
  habilidades, preços, recompensas, regeneração e recursos iniciais não mudaram.
- **Terceira entrega, 1.65.0 (seção 17):** interface, retorno visual e texto, a partir do que Jean encontrou jogando;
  a investigação dos toques que pareciam não responder; os rótulos dos prédios (não reproduzido). Nada de equilíbrio.
- **Quinta entrega, 1.65.4 e 1.66.0 (seção 20):** a noite e a tocha ditas antes da luta; a primeira implementação
  da abertura guiada ([18](18-E9-ABERTURA-GUIADA.md), seção 12).
- **Acabamento, 1.66.1 e 1.66.2 (seção 21):** os riscos da capela em indicadores; os quadros da abertura parados,
  mais discretos, com "Entendi" e "Encerrar tutorial" ([18](18-E9-ABERTURA-GUIADA.md), seção 13).
- **Ajustes pontuais, 1.66.3 (seção 22):** C4, V1 e o Mural, a fogueira e a fome fora da barra
  ([18](18-E9-ABERTURA-GUIADA.md), seção 14).
- **A segunda parte da abertura, 1.66.4 e 1.67.0 (seção 23):** os últimos detalhes e V2–V5, E1, T1, N1
  ([18](18-E9-ABERTURA-GUIADA.md), seções 14.1 e 15).
- **Interação e feedback, 1.67.1 (seção 24):** o alvo à vista, a comitiva, a noite, textos, a fuga, as teclas e
  adiantar o texto ([18](18-E9-ABERTURA-GUIADA.md), seção 16).
- **Os ciclos básicos, 1.68.0 (seção 25):** o primeiro atendimento grátis do templo, um contrato do mural ao
  pagamento, o primeiro baú, os selos e adiantar a apresentação ([18](18-E9-ABERTURA-GUIADA.md), seção 17).
- **Revisão pontual, 1.68.1 (seção 26):** textos curtos, os ícones de efeito, adiantar separado, a seta no alvo e a
  derrota no cenário de teste ([18](18-E9-ABERTURA-GUIADA.md), seção 18).
- **Três correções, 1.68.2 (seção 27):** o contrato aceito logo na volta à vila, o Entendi no quadro da animação e a
  sequência da derrota ([18](18-E9-ABERTURA-GUIADA.md), seção 19).
- **Quarta entrega, 1.65.2 e 1.65.3 (seção 19):** a partida da Quibia lida; os contratos pagos depois do resgate; o
  ×N dos baús em destaque. A especificação da abertura guiada fica em [18](18-E9-ABERTURA-GUIADA.md).
- **Correção 1.65.1 (seção 18):** os três pontos que faltaram na mensagem cortada: a percepção do Mago na água, o nome
  da Yara antes de o herói conhecê-la, e duas Lanças de Gelo nos turnos da iniciativa. Nada de equilíbrio.

**A E9 não está concluída.** A validação técnica e a partida de Jean não substituem as partidas de jogadores novos
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
| 1 | Bloqueio ou perda de progresso | A fome e a infecção matam na campanha; o save automático fica na véspera | Reproduzido (4.5); 162 de 540 percursos | Fome e infecção levam ao resgate na campanha (4.6, 1) | **Feito na 1.64.0** (seção 14) |
| 2 | Bloqueio ou perda de progresso | O resgate come dois dias de provisões, e isso leva a outro resgate | Reproduzido (4.1, 4.5) | O resgate do Vau não come a bolsa (4.6, 2) | **Feito na 1.64.0** |
| 3 | Clareza e coerência | O capítulo não termina para quem joga | Reproduzido (3.3) | Cena curta de fim de capítulo no Vau (3.3) | **Feito na 1.64.0** |
| 4 | Clareza e coerência | O custo do companheiro não aparece na escolha | Reproduzido (4.4) | Nota "Consome 1 provisão por dia." | **Feito na 1.64.0** |
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
| `covil` com `EVENTO=odete_na_estrada` | Odette na estrada (mundo gerado), com a nota do custo ao aceitar |
| `resgate` | A recuperação (1.64.0): acampar no Charco derruba o herói; `CAUSA=fome` ou `infeccao`, `COMITIVA=0` para ir sozinho |

Na 1.64.0, o cenário `praca` no Vau abre no fim do capítulo: é o que um save já concluído recebe.

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

## 13. A partida de Jean (1.63.0, mago, PARAIBATRON)

Evidência humana da E9, de um jogador experiente que conhece o jogo. **Não é validação de jogador novo nem conclusão
da etapa.** Fonte: o registro da partida (`.jsonl`) e o relatório (`.md`) que Jean anexou. Semente 179558948, modo
Resgate, 9 dias, nível 3, partida em andamento.

**O que o registro mostra:**
- **Nível 3 no dia 5** (o evento "nivel" do dia 5).
- **Dez lutas: sete vitórias, duas fugas, uma derrota.** As fugas, nos dias 1 e 2, no nível 1: o Espantalho Possuído
  (elite, emboscada já na saída do Vau, deixou o herói com 12 de 42) e Jormus, o sapo ancião (um alvo com nome).
  Jormus foi vencido no dia 3, com Morel.
- **O ossuário vencido começando com 36/58 de vida e 19/42 de mana** (a concussão do dia 6 baixou o máximo de mana). A
  luta chegou a deixar o herói com 11 de vida; Odette terminou com 1.
- **Ilse enfrentada no nível 3, antes da especialização (que vem no 4), começando com 38/58 de vida e 39/42 de mana.**
  Antes, uma poção fora da luta; dentro, um tônico. Quinze turnos, derrota.
- **Habilidades e recursos usados:** Lança de Gelo (21 vezes), Bola de Fogo (13), Meditar (6), Barreira (5) e o Dardo
  Arcano; duas fugas; Morel e Odette na comitiva desde o dia 3 (522 de dano dos dois no total; Odette curou o herói em
  várias lutas).
- **Depois do resgate, 94 de ouro:** a derrota custou 40 (30% de 134). Havia dinheiro para comprar comida. Mas os
  dois dias do resgate passaram sem provisões: a fome subiu para 1 e depois 2, a vida máxima caiu de 58 para 46, e
  Morel e Odette perderam 6 de aprovação por dia, com fome.

**O que o registro não mostra:** a vida que restou a Ilse. Na luta contra ela, o herói causou 141 de dano e a comitiva
160, somando 301 contra os 265 de vida de Ilse. Mas esse total inclui os afogados que ela invoca (os dois do fim, de 45
cada, estavam vivos), e o registro não separa o dano por alvo. **"Quase matei Ilse" é a impressão de Jean jogando; o
registro não confirma nem desmente.**

**O complemento da mesma partida** (o registro até o dia 19, mandado depois; mesmo herói e mesma semente):
- **19 dias, nível 6, Piromante desde o dia 9** (nível 4). Talentos: Potência Arcana 3, Prisão de Gelo, Escudo Rúnico,
  Ignição;
- **30 lutas: 27 vitórias, 2 fugas (as dos dias 1 e 2), 1 derrota (a primeira contra Ilse)**;
- **Ilse vencida no dia 14, na segunda tentativa,** no nível 5, começando com 83 de vida, em 10 turnos (184 de dano do
  herói e 122 da comitiva). O desfecho foi destruí-la, mesmo com a fita já recolhida no dia 13;
- **a febre concluída no dia 15; diante de Caspar, calar-se**;
- **o ouro sobe depois do começo:** 37 no dia 10, 200 no dia 12, 403 no dia 19. Passou fome em três dias: o 8 e o 9,
  depois do resgate, e o 16.

**O que isso acrescenta ao robô:**
- uma pessoa experiente avança bem, entrando nas lutas ferida e com poucos recursos: usa fuga, Meditar, Barreira e a
  comitiva, coisas que o robô usa pouco ou mal;
- o problema da recuperação aparece também com gente: os dois dias do resgate puseram fome no herói e na comitiva,
  mesmo com ouro no bolso (seção 4.5). O robô, sozinho, não basta para decidir reduzir a dificuldade, e Jean decidiu
  não reduzir.

## 14. O que mudou na 1.64.0

**Recuperação no modo Resgate da campanha:**
- **a fome e a infecção que zerariam a vida levam ao resgate,** como a queda em combate (`Finais.cair_sem_luta`). A
  noite termina (o quadro do amanhecer mostra o que a fome ou a febre tirou) e então vem o resgate
  (`Derrota.causa`: "fome" ou "infeccao");
- **o hardcore e o mundo gerado ficam como eram:** a fome e a infecção encerram a partida; o hardcore apaga o save;
- **o custo é o de antes:** 30% do ouro e dois dias;
- **os dois dias encerram a emergência** (`Jogo.resgate_campanha`):
  - o herói e a comitiva comem na casa de Marta: os dias passam com refeição (como a taverna), sem gastar a bolsa;
  - a fome zera; a infecção é tratada; as feridas abertas ficam enfaixadas (não infeccionam);
  - os outros ferimentos seguem as regras de sempre (uma fratura continua sarando pelos dias);
  - os atributos são recalculados, e a vida fica entre 40% e o máximo;
  - **nada derruba de novo durante o próprio tratamento** (`resgatando`): uma queda, uma recuperação, uma cobrança;
- **quem cuida:** Marta, se a água já limpou e ela está de pé; senão, Pita, na casa de Marta
  (`consequencias.marta_de_pe`, conferido depois dos dois dias);
- **a apresentação:** o título "Tudo escurece...", a causa numa linha (só para fome e infecção: a de combate já disse
  diante de quem o herói tombou), um quadro de amanhecer só para os dois dias, e então o despertar: onde, quem cuidou,
  que a comitiva comeu junto, a infecção limpa (se houver) e o ouro perdido. O tratamento é aplicado antes do texto,
  para o painel já mostrar o herói tratado quando a narração diz isso;
- **o prólogo e a escolha do modo** dizem agora "se você cair em combate, de fome ou de infecção". A frase "a fome e
  uma infecção sem tratamento ainda encerram a partida" saiu;
- **nenhuma provisão extra nem benefício econômico novo.**

**O custo dos companheiros:** a opção "Aceitar X na comitiva" traz a nota "Consome 1 provisão por dia.", no padrão
das notas (na tela, embaixo da opção; no texto, junto do rótulo). Sem janela de confirmação nem explicação depois.
Com a comitiva cheia, a troca não leva a nota: quem chega come no lugar de quem vai para o acampamento, e o gasto não
muda. A nota vale também no mundo gerado (o gabarito mudou só nessa linha, nas ofertas da Yara e do Morel).

**O encerramento do capítulo** (`rpg/capitulo.py`):
- depois de concluir "A Febre do Turvo" e responder a Caspar, uma cena no Vau, uma vez, na próxima tela de lá (nunca
  no meio de luta, serviço ou evento). Título "O Vale do Turvo", subtítulo "fim do primeiro capítulo";
- quatro frases do estado de agora: a Fonte e Marta (sem antecipar: com a água escura ou limpando, Marta continua de
  cama), Ilse, Caspar e Yara. Não repetem a frase da vila que aparece logo depois;
- o aviso discreto: "Este é o fim do capítulo disponível. Você pode continuar explorando o Vale.";
- se a herança de Vó Berta ainda espera, a cena lembra, e a ação continua na taverna;
- **na interface:** o rastreador mostra "Capítulo · O Vale do Turvo · Primeiro capítulo concluído", no lugar da
  missão; o Diário abre com a mesma linha;
- não abre a Estrada de Varn, não cria missão nova, não dá recompensa;
- **um save que já tinha tudo resolvido** recebe a cena na próxima visita ao Vau, sem repetir a volta ao Vau nem a
  praça.

**Verificado:**
- `tests/test_recuperacao.py` (20 testes): queda em combate, fome, infecção, as duas juntas, a comitiva comendo,
  sem comida, sem ouro e sem nada para vender (vinte noites seguidas: cada queda uma recuperação, nenhum fim de jogo),
  a guarda contra queda durante o tratamento, o hardcore e o mundo gerado, salvar e carregar depois da recuperação, um
  quadro de amanhecer só, o texto uma vez, Marta ou Pita, o prólogo e a nota;
- `tests/test_capitulo.py` (12 testes): uma vez, logo depois da praça, nem antes nem fora do Vau nem numa luta, os
  desfechos, a Fonte no estado de agora, nada repetido da frase da vila, a herança, o rastreador e o Diário, o save já
  concluído;
- os testes antigos de Caspar e da Yara que esperavam "nenhuma cena" depois da praça agora esperam o fim do capítulo;
- a fumaça com o cenário novo `resgate` e o fim do capítulo no cenário de Caspar, a 1500 e 1280 px;
- gabarito: só a nota do recrutamento mudou (conferido com as transcrições lado a lado), atualizado.

## 15. O começo antes e depois (as mesmas políticas)

Mesmas sementes, mesmo robô e mesmas estratégias da seção 4. "Antes" é a 1.63.0; "depois", a 1.64.0. O robô para no
dia 45: no jogo, esse limite não existe.

**Ritmo: "direto", "explorador" e "nível 6", 30 sementes, os dois caminhos (540 percursos):**

| Classe | | Completos | Fim de jogo | Parou no dia 45 | Chegou à capela | Chegou ao fundo | Nível no fim | Quedas | Dias com fome | Resgates por fome ou infecção |
|---|---|---|---|---|---|---|---|---|---|---|
| Guerreiro | antes | 70 | 88 | 22 | 158 | 88 | 3,4 | 1,6 | 2,1 | — |
| Guerreiro | depois | 89 | 0 | 91 | 170 | 120 | 4,3 | 3,1 | 3,3 | 0,40 |
| Arqueiro | antes | 54 | 90 | 36 | 160 | 74 | 3,4 | 1,5 | 2,3 | — |
| Arqueiro | depois | 47 | 0 | 133 | 168 | 82 | 3,9 | 3,0 | 4,4 | 0,67 |
| Mago | antes | 16 | 125 | 39 | 144 | 36 | 2,7 | 2,9 | 3,2 | — |
| Mago | depois | 23 | 0 | 157 | 158 | 52 | 3,8 | 5,4 | 4,0 | 0,41 |
| Todas | antes | 140 | 303 | 97 | 462 | 198 | 3,2 | 2,0 | 2,5 | — |
| Todas | depois | 159 | 0 | 381 | 496 | 254 | 4,0 | 3,9 | 3,9 | 0,49 |

**Estratégias do começo ("direto", "descansada", 40 sementes; completos de 40):**

| Estratégia | Guerreiro antes → depois | Arqueiro | Mago |
|---|---|---|---|
| atual | 19 → 27 | 17 → 17 | 6 → 14 |
| comida do grupo | 21 → 30 | 13 → 18 | 7 → 16 |
| cuidadoso | 15 → 15 | 16 → 13 | 9 → 11 |

**Morte evitada não é progresso.** Dos 303 percursos que antes morriam de fome ou infecção, com a mesma semente:
- **39 completaram** o capítulo;
- **264 pararam no dia 45 do robô,** a maioria na capela (155) ou ainda no canal (38), nos níveis 2 e 3, com 5,9
  quedas em média;
- 134 passaram da etapa em que morriam, e 240 subiram de nível além do que tinham.

A recuperação tirou a perda da partida inteira e mais gente chega à capela e ao fundo. Mas a maior parte dos percursos
salvos gira em quedas: a média de quedas dobrou (2,0 → 3,9), e quase todas são de combate (só 0,49 por percurso vêm de
fome ou infecção). **A economia do começo não foi resolvida por esta entrega,** e não era o objetivo.

## 16. O que continua e o que falta

**Um caso concreto de bloqueio econômico, com o robô: o arqueiro sem ouro e sem flechas.**
- O percurso (arqueiro, semente 10, "direto", "descansada"): começa com 20 flechas e 10 de ouro depois das compras;
  cai já na primeira noite, acampado no Charco; no dia 12 está com 2 flechas e 0 de ouro; **a partir do dia 19, sem
  flechas e sem ouro,** luta de adaga ("Golpe de Adaga — sem flechas!") no Charco por mais de 25 dias, caindo de
  tempos em tempos, com 0 ou 1 de ouro. O nível 2 vem no dia 21; no dia 45 ainda não entrou na capela.
- Não é a fome: os resgates o alimentam. É o círculo flecha → luta → ouro: sem flecha, a luta rende pouco e derruba;
  sem ouro, não há flecha (1,4 de ouro cada).
- Entre os 540 percursos depois, 66 tiveram dois ou mais resgates por fome ou infecção; nenhum completou. Metade deles
  é de arqueiros (34), e 34 dos 66 não ganharam nível depois do dia 20; o ouro médio nos últimos dez dias foi 3,3.
- **Não sei se uma pessoa cai nisso.** Uma pessoa guarda flechas, foge antes e não caça o alvo com nome no nível 1. O
  robô faz o contrário.
- **A menor solução, se Jean jogando confirmar** (nada aplicado; não mexe em preço nem em renda das lutas): o resgate
  devolver ao arqueiro um punhado de flechas recolhidas do lugar da queda, ou o mercado do Vau aceitar trocar flechas
  por um item da bolsa. Recomendo esperar a partida de um arqueiro antes de decidir.

**Os outros que giram:** guerreiros e magos que param no dia 45 caem sobretudo em combate, na capela, onde o robô
insiste nas salas no nível 3. É a dificuldade das lutas, que Jean decidiu preservar, somada à política do robô (seção
4.4). Não há, nesses, uma situação sem saída: sempre há luta possível, ouro de contrato e o Charco no nível 1.

**Riscos que ficam:**
- a recuperação deixa o herói em 40% da vida, com fome zerada e sem comida na bolsa. Quem não tem ouro precisa ganhar
  ao menos 4 antes da terceira noite de fome. O jogo agora não acaba, mas pode girar devagar;
- o capítulo termina sem marco para quem não responde a Caspar ("Ainda não"): a cena espera a resposta. É coerente
  (o conflito local não acabou), mas vale ver se alguém fica na dúvida;
- a ordem do resgate mostra o quadro do amanhecer antes do texto do despertar. Na tela gráfica, ficou claro; no modo
  texto, a linha "Amanhece o dia N" vem antes de "Dois dias se passaram".

**Falta:**
- Jean jogar a 1.64.0 (roteiro curto abaixo);
- os jogadores novos, com a ficha da seção 9;
- decidir, depois disso, os números do começo (seção 6, achados 5, 6 e 9) e o caso do arqueiro.

**Roteiro curto para Jean (1.64.0):**
1. `python -m tests.navegador.cenarios resgate` e acampar: a fome derruba, o resgate alimenta e trata. Repetir com
   `CAUSA=infeccao`. Conferir se o texto e o painel contam a mesma coisa, sem repetir.
2. `python -m tests.navegador.cenarios covil` com `EVENTO=odete_na_estrada`: a nota "Consome 1 provisão por dia." ao
   aceitar.
3. `python -m tests.navegador.cenarios praca` (com `POSTURA` e `YARA` à escolha): o fim do capítulo, o rastreador e o
   Diário.
4. Uma partida nova até o fim do capítulo, de preferência com o Arqueiro, anotando como na seção 8.1.

## 17. Interface, retorno visual e texto (1.65.0)

Entrega pedida por Jean depois de jogar: interface, retorno e texto, com uma investigação de congelamento. Nada de
equilíbrio, economia, recompensa ou dificuldade mudou. A proposta do Arqueiro sem flechas (seção 16) continua
esperando a partida dele.

**O que mudou:**
- **Mercador ambulante:** sem ouro, as compras ficam à vista e indisponíveis; depois do exame (legítimo, com o preço
  novo, ou malsucedido) há a compra e "Despedir-se". Antes, sem ouro, o evento acabava sem resposta. Sorteios iguais.
- **Opção indisponível:** riscada em vermelho, com o motivo curto embaixo ("Ouro insuficiente"), em todas as
  indisponíveis.
- **Toques que pareciam não responder** (investigado no navegador, com cliques nas coordenadas, normal e instantâneo):
  - o Continuar das cenas de missão: a proteção contra clique duplo e tecla segurada continua, mas o botão fica
    apagado enquanto ela segura (antes, a rajada segurava o botão já aceso). Causa: a proteção;
  - o acampamento: depois de "Conversar", a fala leva ~1,6 s para ser apresentada, e o "Dormir" à vista ignorava o
    toque. Agora o toque em Dormir, Conversar, levar ou deixar alguém e carinho fica guardado e vale quando o menu
    volta (nunca o segundo toque de um clique duplo, nem compra, venda ou uso). Causa: processamento e apresentação.
- **Menu inicial:** ↑/↓ e Enter, o mouse leva o foco junto, e a opção em foco fica em ouro com um losango discreto.
- **Nome na ficha:** o nome que não cabe ao lado do retrato ganha uma linha própria em cima ("PARAIBATRON" inteiro a
  1500 e 1280 px); só uma palavra que nem assim cabe desce ao passo de pixel seguinte.
- **"Com fome":** o selo fica na ponta da barra de vida (antes saía da caixa e era cortado).
- **Árvore de talentos:** títulos curtos ("Base", o nome da classe, "sua especialização", "caminho não
  escolhido"); sem "para todos" nem "passe o mouse".
- **Combate:**
  - os balões da comitiva ficam 1,6 s + 35 ms por letra (até 6 s; eram 2,6 s + 45 ms, até 8 s);
  - a Odette diz "Fica comigo. Respira." no lugar de "A Mãe não te quer ainda.";
  - a entrada do servo do Necromante tem um som curto, só na entrada de verdade;
  - o espólio: o XP vem ~600 ms depois do ouro (eram ~830).
- **Texto:** "fonte nova" vira descrição (a abertura não diz mais que a vila a chamou assim); "brejo" vira "pântano"
  no terreno e "Charco dos Juncos" (ou "o Charco", nas falas) para o lugar da Yara.
- **Pedidos de Jean no meio da entrega:**
  - a teia da aranha voa até o alvo e, quando não prende, a carta diz "não pegou";
  - na bolsa, o item que trata algo agora pulsa e diz o quê ("Trata: queimadura grave."); a bandagem sem nada para
    tratar avisa que só cura 8 de vida;
  - o mural pisca, com "clique: contratos", até a primeira visita (guardado no navegador).

**Não reproduzido: os rótulos dos prédios que subiram.** Procurei em duas sessões de 260 passos ao acaso pela vila
(prédios, menus, mapa, viagens), nas velocidades normal e instantânea, e num percurso dirigido (taverna, Diário,
inventário, redimensionar 1500 ↔ 1280, zoom de 125%): o desvio entre a posição dos rótulos e a conta certa ficou
sempre em 0. **Hipótese** (sem mudança feita, como pedido): os rótulos são calculados no primeiro quadro e no fim da
transição de altura da paisagem; se a vila montar com a paisagem escondida ou numa mudança de altura sem transição
(a coluna do meio mudando de largura sem a janela mudar), o cálculo usa uma altura menor e os rótulos sobem até a
próxima montagem. Se acontecer de novo, anotar o que veio antes (luta, carregar, abrir um painel).

**Verificado:** testes (novos: o mercador, o retorno visual da teia e da bolsa), gabarito (cada mudança conferida lado
a lado antes de atualizar: só a escolha extra do mercador, o motivo, a nota do recrutamento, o subtítulo do tronco, a
fala da Odette, "bruxa do pântano" e os campos da bolsa), pyflakes, fumaça, e as telas a 1500 e 1280 px.

**Para Jean conferir:**
1. Um mercador sem ouro (`EVENTO=mercador_ambulante OURO=0 python -m tests.navegador.cenarios covil`).
2. O acampamento: conversar com a Odette e logo tocar em Dormir (`python -m tests.navegador.cenarios resgate`, acampar).
3. O menu inicial só com o teclado.
4. Uma luta contra aranhas (`LUTA=aranha VIDA=60 NIVEL_LUTA=2 QUANTOS=3 python -m tests.navegador.cenarios covil`).
5. Uma ferida aberta e a bandagem na bolsa, antes e depois de usar (o cenário `resgate` com `CAUSA=infeccao`).
6. Uma partida nova: o mural piscando no começo (num navegador que nunca o abriu).


## 18. Os três pontos que faltaram (1.65.1)

A mensagem de Jean da 1.65.0 chegou cortada; estes três pontos completam o pedido. Nada de equilíbrio, economia,
recompensa ou dificuldade mudou.

**1. A percepção do Mago na água.** "Uma palavra apagada, cada vez mais perto" não dizia o que o Mago sente. Agora:
- na fonte nova: "Você põe a mão na água e sente magia nela, fraca e de um tipo que você não reconhece. Ela não nasce
  aqui: chega com a água, do leste.";
- no canal: "Perto da represa, a água é só água. Rumo ao pântano, você volta a sentir nela a magia da fonte nova, mais
  forte a cada passo.";
- diante da capela (frase nova, só do Mago): "Junto ao muro da capela, essa magia é a mais forte do caminho, e vem lá
  de dentro."

Nenhuma delas diz a causa (Ilse, o Sigilo): isso continua no fundo da capela e no lodo.

**2. O nome da Yara.** Quem ainda não a conhece (`caspar.conhece_yara`: ela não está no grupo nem na reserva, não
recusou a vaga e não morreu) não ouve o nome dela:
- na acusação, Caspar fala de "uma moça no Charco dos Juncos", sem o nome;
- o objetivo da Vigília, no cartão e no Diário: "Caspar acusa uma mulher de causar a febre." O objetivo de uma etapa
  agora pode ser uma função do jogo (`missoes.objetivo`): quando ela se apresenta (na fogueira ou no Charco), o Diário
  passa a dizer "Caspar acusa Yara de causar a febre.";
- as referências próximas também: a praça (a apresentação de Caspar e "Agora falta a do Charco"), o título do que
  mostrar à praça ("e não da mulher acusada"), a opção de denunciar ("não da moça do Charco") e a linha do Diário
  depois da decisão ("A moça do Charco: você não a conhece. ...");
- a fala da Yara sobre a praça a que ela não foi diz "Caspar me acusou diante da vila inteira" (não mais "disse o meu
  nome": quem estava lá não ouviu o nome).

Ficam como estavam: quem a conhece, a tem no grupo ou na reserva, e quem a deixou morrer. **Observação:** quem a deixou
queimar na fogueira nunca ouviu o nome dela, mas o Diário diz "Yara: morreu na fogueira de Caspar."; ficou assim, como
pedido (preservar o caso da morte).

**3. Iniciativa, congelamento e Firme.** Reproduzido em Python e no navegador (cenário `gelo`, Mago nível 4 com a
iniciativa, contra um lobo de muita vida e sem esquiva; semente 17: as duas primeiras Lanças congelam):

| Momento | O lobo | A tela antes | A tela agora |
|---|---|---|---|
| 1ª Lança (turno da surpresa) | congelado, 1 turno | "Lobo fica congelado!" | igual |
| 2ª Lança (o turno seguinte, antes de o lobo agir) | continua congelado, 1 turno (não soma) | "Lobo fica congelado!" e o selo "congelado" de novo | "Lobo já está congelado: não soma, perde só o próximo turno." e o selo "já congelado" |
| Vez do lobo | perde a ação; fica firme até a próxima vez dele | "Lobo está congelado e perde o turno!" | igual |
| 3ª Lança | não congela (firme) | "acabou de se soltar e não fica congelado de novo" | igual |
| Vez seguinte do lobo | age | | |

- **A regra está certa e ficou:** congelar de novo antes da primeira ação do inimigo não soma duração (a duração é a
  maior das duas, 1); o Firme só entra depois de o inimigo perder a ação de fato, e impede que ele perca duas ações
  seguidas. A Lança (35%) e a Prisão (sempre) seguem a mesma regra.
- **A divergência era de apresentação:** a segunda Lança anunciava um congelamento novo que não mudava nada; quem via
  dois "congelado" esperava duas ações perdidas. Corrigido na tela e no registro (vale para qualquer trava: atordoado,
  preso). Os sorteios continuam na mesma ordem (o gabarito não mudou).
- A terceira Lança só mostra "firme" quando o sorteio de 35% congelaria; quando ele falha, o golpe sai sem aviso de
  congelamento, como sempre.

**Verificado:** testes (novos: o nome antes e depois de conhecê-la, a praça sem o nome, as duas Lanças na iniciativa),
gabarito sem mudança, pyflakes, fumaça, e as telas da luta a 1500 e 1280 px.

**Para Jean conferir:**
1. O Mago na fonte nova (`CLASSE=mago ETAPA=fonte LUGAR=vau_do_turvo python -m tests.navegador.cenarios capela`,
   "Examinar a fonte nova") e no canal até a capela (`python -m tests.navegador.cenarios missao`, "Seguir a água e
   examinar o canal").
2. A acusação de Caspar sem conhecer a Yara, e o Diário depois dela (`CLASSE=mago ETAPA=capela LUGAR=vau_do_turvo
   python -m tests.navegador.cenarios capela`: a cena toca ao abrir).
3. Duas Lanças seguidas com a iniciativa (`python -m tests.navegador.cenarios gelo`; `PRISAO=prisao` para a Prisão).


## 19. A partida da Quibia e duas correções (1.65.2 e 1.65.3)

### 19.1 A partida (registros de 11/10/2026, 1.65.0, Mago piromante, modo resgate, 25 dias, nível 5)

Os arquivos ficaram como vieram. Separo o que Jean contou, o que o registro mostra e o que é leitura minha.

**Observações da sessão (contadas por Jean):** ela não percebeu Habilidades até Jean apontar; não entendeu de início
que o cenário da vila era clicável; passou a seguir contratos depois de uma dica; concluiu dois contratos, caiu, e só
recebeu saindo do Vau e voltando.

**Fatos do registro:**
- As quatro primeiras lutas (dias 2 a 5) só com o ataque básico (Dardo Arcano); a primeira Bola de Fogo é a quinta
  luta (dia 5, à noite). Depois, a Bola de Fogo vira a habilidade mais usada (16 vezes).
- 20 lutas, 7 derrotas e 5 resgates. O Salão Alagado derrotou duas vezes: dia 3 de manhã, nível 2 (Afogado nv 2 e
  duas sanguessugas nv 3) e dia 19 à noite, nível 5 (Afogado nv 4 e duas sanguessugas nv 5, uma Flamejante).
- À noite, 4 lutas e 2 derrotas; de dia, 16 e 3 (na tabela do registro).
- Morel entrou no dia 17, pelo evento da taverna (`morel_na_taverna`); Odette não aparece.
- Os eventos do contexto "explorar" aparecem no dia 16 e no 24; antes, o registro tem viagens, chegadas e lutas.
- Contratos: 178 de ouro (41% do que entrou). O registro não tem uma linha para contrato pago; o ouro sobe ao chegar
  ao Vau nos dias 8 (+23), 17 (+87) e 21 (+32, depois do resgate do mesmo dia, saindo para o Bosque e voltando).
- Nenhum dia com fome; quatro costelas quebradas (no dia 13, na briga de taverna e no festival; no dia 14, na estrada
  e na capela).

**Hipóteses (não confirmadas por uma pessoa só):** a falta de Habilidades nas primeiras lutas explica parte das
derrotas cedo; a capela no nível 2 foi cedo demais e nada na tela disse isso com força; a exploração e a taverna
apareceram tarde porque nada as apresenta. Uma jogadora não dá a frequência no público.

### 19.2 Contratos depois do resgate (1.65.2)

**Reproduzido** nos quatro caminhos: o resgate da campanha (combate, fome, infecção) e o do mundo gerado no modo
brando. **Causa:** só a chegada viajando (`chegar`) chamava `receber_contratos`; os dois resgates põem o herói na vila
direto. O gabarito tinha o mesmo caso (guerreiro-42: cai em Ribeira Fria com um contrato cumprido e nunca recebe).

**Correção:** o menu da vila recebe os contratos cumpridos ainda não pagos, na página da vila, depois do texto do
resgate e da cena de missão pendente. Sem viagem nem evento de chegada. Cada contrato sai da lista ao pagar (uma
vez); a cobrança do resgate continua sobre o ouro de antes; ouro, XP, reputação e o quadro dos contratos são os de
sempre. Um save na vila com contrato cumprido e não pago recebe na primeira volta do menu.

**Conferido:** nenhum, um e dois contratos em cada queda; salvar e carregar depois do pagamento (não paga de novo);
o save antigo; fora da vila não paga; o mundo gerado brando; na tela, resgate → cena de Caspar → página do Vau com o
quadro dos contratos, sem sobreposição, a 1500 e 1280 px. Gabarito: só guerreiro-42 mudou (o pagamento, e a partida
segue outro caminho depois dele).

### 19.3 Baús abertos juntos (1.65.3)

Antes, o número só estava no rótulo pequeno ("BAÚS ×3"). Agora o quadro abre com a pilha (um ícone por baú, até
cinco, caindo um sobre o outro) e o ×N grande ao lado; o rótulo vira "baús abertos". Um baú fica como era. O N é o
que o motor abriu (os baús que saíram da bolsa); a fumaça confere o número e os ícones contra a bolsa antes do clique.
Sorteios, recompensas e a janela de cada equipamento iguais; gabarito sem mudança; conferido a 1500 e 1280 px com 1, 2
e 3 baús.

### 19.4 Para Jean conferir

1. O resgate com contratos cumpridos: `CONTRATOS=2 python -m tests.navegador.cenarios resgate` (acampar; depois da
   cena de Caspar, o quadro dos contratos no Vau). `CAUSA=infeccao` para a infecção.
2. Os baús: `python -m tests.navegador.cenarios baus` (três) e `BAUS=2` ou `BAUS=1`.
3. A proposta da abertura guiada: [18](18-E9-ABERTURA-GUIADA.md).


## 20. Riscos da noite e abertura guiada (1.65.4 e 1.66.0)

**1.65.4, a noite e a tocha ditas antes da luta** (com o tutorial ligado ou não; encontros, atributos, horários,
consumo e dificuldade iguais): a nota das salas da capela e das escolhas que levam à luta (tocha, ou o inimigo que
ataca primeiro sem ela; à noite, +1 nível e +10% de dano, e na guardiã só o dano); o nível-base do lugar com o que a
noite soma ao lado; o consumo real de tocha no painel; a dica da noite sem prometer bando maior onde o tamanho é fixo;
o texto de quem entra sem luz numa sala (certo) separado do de fora (provável). O detalhe está na seção 8 do 18.
Gabarito: as 24 partidas mudam só no texto; escolhas, lances e herói conferidos idênticos.

**1.66.0, a abertura guiada (escopo mínimo):** a caixa "Mostrar tutorial", a despensa da taverna, a caneca por conta
da casa, a oportunidade de sentar com Morel, os quadros da primeira luta (C1–C4) e do Mural (V1), "Dispensar
orientações" e a Ajuda (F1). Medida, caminhos e limitações na seção 12 do 18. Gabarito: só uma linha de estado nova
nas transcrições da tela; escolhas, lances e herói idênticos.

**Para Jean conferir:** o roteiro está na resposta da entrega e na seção 12 do 18 (as três classes, com e sem tutorial,
e os caminhos de Morel).

## 21. Acabamento da abertura e os riscos da capela (1.66.1 e 1.66.2)

Pedido de Jean antes da segunda parte do tutorial; regras, custos, recompensas, sorteio e dificuldade iguais (gabarito
sem diferença).

**1.66.1:** na capela, o nome da ação em destaque e, embaixo, indicadores com ícone: "−1 tocha"; sem tocha, "Sem luz:
inimigo age primeiro", em vermelho; à noite, a lua com "+1 nível · +10% dano" (na guardiã, "+10% dano"). A dica traz o
detalhe. O sarilho mostra só o que vale para cada atalho.

**1.66.2:** o destaque é um contorno fino com brilho lento (parado com movimento reduzido); os quadros da luta ficam
numa faixa parada fora das cartas, das ações e do texto; o C4 aparece depois do golpe, em linhas (nome, custo com a
cor e o ícone do recurso, o Atacar da classe), com "Entendi" e "Encerrar tutorial"; a cena depois da despensa espera o
Continuar e o taverneiro aponta o mural de contratos. Detalhe, conferência e limitações na seção 13 do 18.

## 22. Ajustes pontuais de apresentação (1.66.3)

Os últimos ajustes da primeira parte da abertura, antes da segunda e dos testes humanos, sem mudar regras nem
equilíbrio: os ícones do C4 alinhados ao texto; o V1 com o texto "Clique no mural para ver os contratos disponíveis.",
num quadro abaixo do cenário que não cobre o prédio; o balão do Mural sem "clique: contratos"; a fogueira com a
instrução, o contador, quem vai e quem fica escritos e a nota do acampamento junto da decisão; a fome numa linha de
condições embaixo das barras, com o efeito de agora na dica. Detalhe e limitações na seção 14 do 18.

## 23. A segunda parte da abertura guiada (1.66.4 e 1.67.0)

**1.66.4:** a fome numa etiqueta compacta (a de "Morrendo de fome" acende mais); a nota do acampamento só no menu de
cada companheiro, junto da decisão; os avisos do lugar com cor pela hierarquia (noite em amarelo, tocha neutra, falta
de luz em vermelho).

**1.67.0:** os quadros que faltavam, um por vez e só quando fazem sentido: recuperar na vila (o serviço que resolve e
cabe no bolso), as provisões na primeira escolha de destino, o primeiro companheiro, explorar na primeira ocasião fora
da vila (com o motivo dito uma vez, pelo taverneiro ou por Morel), a primeira comparação de equipamento, o primeiro
ponto de talento e a primeira noite fora da vila. Regras, encontros, recompensas e sorteio iguais; o jogo é o mesmo
com e sem tutorial. Detalhe, conferência e limitações na seção 15 do 18.

**A E9 continua aberta:** o teste técnico não mostra que uma pessoa nova entendeu os sistemas (seção 11 do 18).

## 24. Interação, posicionamento e feedback (1.67.1)

Correções pedidas por Jean depois da 1.67.0, cada uma reproduzida antes: o quadro que apontava para "Explorar a
região" fora da área visível (e trocava de lugar durante a leitura), o V4 que falava do botão Comitiva apontando o
cartão, o texto da noite, "hábito chamuscado" e o uivo dos lobos, a fuga sem retorno além da linha verde, as teclas
que abriam e não fechavam (T, I, C, D, B) e a guarda do Continuar que cliques repetidos prolongavam sem fim. Regras,
sorteio e equilíbrio iguais. Detalhe na seção 16 do 18.

## 25. Os ciclos básicos (1.68.0)

O que faltava para quem começa entender os sistemas de todo dia, pela própria partida: a primeira cura do templo de
graça (autorizada por Jean, uma vez por personagem, na campanha), um contrato acompanhado do mural ao pagamento, o
primeiro baú, o que os selos das cartas fazem e como adiantar a apresentação sem pular nada do jogo. Nada é dado ou
forçado para o tutorial; combate, sorteio e equilíbrio iguais. Detalhe na seção 17 do 18.

## 26. Revisão pontual (1.68.1)

Pedido de Jean depois da 1.68.0: quadros com explicação demais na mesma frase, "selo" em vez de ícone, o adiantar
misturando quatro assuntos, setas que paravam longe do contrato, do baú e do ícone de efeito, o quadro do sangramento
sobre a lista de Habilidades e a derrota na luta preparada do cenário `tutorial`, que parava o teste. Tudo reproduzido
antes (a derrota, no console do servidor; as setas, nas capturas e nas medidas); regras, sorteio e equilíbrio iguais.
Detalhe na seção 18 do 18.

## 27. Três correções (1.68.2)

Pedido de Jean depois da 1.68.1: o quadro do contrato aceito só aparecia depois de Passear (reproduzido no fluxo real:
o A1 ainda pendente vinha antes na fila), o quadro da animação sem Entendi e a derrota sem sinal do resultado (a vila
clara com o herói em 0). Regras, sorteio e equilíbrio iguais. Detalhe na seção 19 do 18.

**A E9 continua aberta** até a validação com jogadores novos.
