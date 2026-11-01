# 29 — Etapa 8: o combate numa grade (estudo de viabilidade e protótipo tático)

**31/10/2026.** Pedido do Jean: pausar a expansão do catálogo do X1 e investigar se transformar o combate de cards num
combate tático com movimento numa grade (referência: Dofus) abre builds mais interessantes, mantendo a apresentação
simples e o resto do jogo como está. **Estudo e protótipo isolado; o combate do jogo não mudou (1.220.0). A direção
espacial está em avaliação**: nada aqui é decisão.

Ligações: o [28](28-ETAPA8-HABILIDADES-TALENTOS-E-BUILDS.md) (o X1 e os sistemas de builds), o
[plano 23](23-PLANO-DE-ARTE-INTERFACE-E-COMBATE.md) (etapa 8) e a [continuidade](00-COMECE-AQUI.md). Protótipo:
[`ferramentas/prototipos/etapa8-tatico/`](../ferramentas/prototipos/etapa8-tatico/LEIA-ME.md) (`demo.bat`).

| Seção | O que tem | Natureza |
|---|---|---|
| 0 | A pergunta e a resposta provisória | Resumo |
| 1 | O combate do jogo hoje | Diagnóstico |
| 2 | Dofus e outras referências | Pesquisa |
| 3 | O que depende de quê | Análise |
| 4 | As regras provisórias do protótipo | Hipótese de trabalho |
| 5 | A economia da vez, comparada | Análise com dados |
| 6 | A fuga repetida | Investigação com dados |
| 7 | Habilidades e talentos espaciais | O que entrou e o que ficou de fora |
| 8 | Encontros e inimigos | O que entrou e como se comportam |
| 9 | Comparação com os cards | Método e primeiras observações |
| 10 | Riscos, observados e não observados | Análise |
| 11 | Impacto e trabalho, se seguirmos | Estimativa |
| 12 | O que avaliar jogando | Para o Jean |

---

## 0. A pergunta e a resposta provisória

**A pergunta:** o espaço cria decisões e possibilidades de build que tornam o jogo melhor, sem comprometer a clareza e
o ritmo?

**O que o protótipo já mostra** (tecnicamente; a graça só jogando):
- **Papéis novos aparecem sem número novo:** afastar uma ameaça (Golpe de Escudo), trazer quem está longe (Corrente),
  fechar um caminho (Sentinela, Muralha de Fogo), proteger quem está ao lado (Guarda-costas, Proteger), abrir espaço
  (Explosão de Calor), escapar de um golpe preparado saindo das casas marcadas. No cards, quase todos esses papéis
  seriam "dano com um estado".
- **Talentos mudam o uso do espaço:** Chamas Seletivas tira o medo de acertar Morel com a área; Labareda o aumenta;
  Arremesso transforma o empurrão em arma contra dois; Âncora faz o Berserker segurar uma linha; Caçador o faz atravessar
  o campo depois de um abate. É diferente de "mais alcance".
- **O custo é real:** cerca de 2,4 comandos por vez, contra 1 nos cards; lutas mais longas contra o troll (15 a 24
  rodadas contra 8 a 13 no X1) e na passagem; inimigos que passam 16% a 22% das vezes só se aproximando no campo aberto;
  congestionamento na passagem.
- **A fuga repetida era dominante** com "andar depois de agir" (recuar e atacar vencia com mais vida que lutar). A causa
  foi achada e a regra padrão mudou (seção 6). Ela continua forte contra o troll lento e os lobos frágeis.

**Resposta provisória:** o espaço cria decisões que os cards não têm, sobretudo nas funções de **posição** (afastar,
trazer, bloquear, proteger, escapar) e nos **talentos que mudam essas funções**. Ele não resolve a variedade sozinho e
cobra em comandos, duração e conteúdo (cada habilidade e cada inimigo precisa ser pensado de novo). A decisão depende
de você jogar e dizer se os comandos a mais viram decisão ou trabalho.

---

## 1. O combate do jogo hoje

| Parte | Onde | O que faz hoje | O espaço mudaria |
|---|---|---|---|
| A luta e a ordem | `rpg/combate/luta.py` (523 linhas), `turnos.py` (136) | Ordem fixa pela Agilidade; uma ação por vez; inimigos sorteiam habilidade e alvo (`escolher_alvo_inimigo`: provocador, tanque, chance de aliado) | A vez ganha movimento; a IA passa a navegar e escolher casas |
| O golpe | `combate/golpe.py` (321) | Dano, esquiva, clima, espinhos, a resposta única por golpe | Alcance, visão e área antes do golpe; o resto continua |
| O herói | `combate/heroi.py` (544), `rpg/habilidades.py` (1036) | Habilidades como blocos (`Dano`, `Aplicar`, `Acender`, `Se`...) sem alcance nem área (a área é "todos os inimigos") | Cada habilidade precisa de alcance, linha, visão e forma de área |
| Talentos | `rpg/talentos.py` (385), `modificadores.py` | Números, gatilhos, versões | Os gatilhos continuam; entram regras espaciais |
| Comitiva | `rpg/comitiva/luta.py` (201) | Odette e Morel com kits fixos, controlados pelo jogador | Três a posicionar (mais as invocações): mais comandos por rodada |
| Inimigos | `rpg/inimigos.py` (426), `dados.py` | 17 famílias; 3 preparam o Golpe Esmagador (`carregando`) | Cada família precisa de papel de movimento (perto, longe, puxa, protege) |
| A tela | `rpg/web/static/batalha.js` (1251), `turnos.js` (236) | Cartas em fileiras, a placa da ordem, a doca de ações | A grade vira o centro; as cartas saem ou viram fichas na grade |

**O que se reaproveita:** a ordem dos turnos, o dano e as defesas, os estados e as camadas, as fichas, os gatilhos e a
regra das cadeias (28, 15.2), os recursos, as preparações (viram casas marcadas), a comitiva controlada pelo jogador, o
gabarito como ferramenta (as transcrições mudariam todas).
**O que precisa ser refeito:** a escolha de alvo (passa a depender de alcance e visão), a IA inteira, as áreas, a tela de
luta, e a definição de cada habilidade.

---

## 2. Dofus e outras referências

**Dofus** (Ankama):
- **PA e PM:** cada personagem começa com **6 PA** (ações) e **3 PM** (casas de movimento); os feitiços custam PA,
  andar custa PM ([JeuxOnline, "Les bases du combat"](https://dofus.jeuxonline.info/article/1720/bases-combat)).
- **Tacle e fuga:** sair do contato com um inimigo custa PA e PM. Desde 2011 o cálculo é determinístico: a fração
  conservada é (Fuga + 2) / (2 × (Tacle + 2)); com valores iguais, perde-se a metade; vários tacleadores multiplicam. A
  razão dada pela Ankama: o sorteio antigo tornava o combate imprevisível e estático demais
  ([devblog "Tacle déterministe", JeuxOnline, 16/03/2011](https://dofus.jeuxonline.info/actualite/30452/devblog-tacle-deterministe)).
- **Empurrão:** o dano de empurrão depende da distância que faltou; quando o empurrado bate em outro, o segundo também
  leva, dividido por 2 ([MGG, nota de equilíbrio](https://www.millenium.org/news/141219.html)).
- **Feitiços:** alcance mínimo e máximo, "alcance modificável", "lançar em linha", com ou sem linha de visão; glifos
  (zonas no chão) e armadilhas; invocações com vida própria (fichas de feitiços na
  [Breakflip](https://www.breakflip.com/fr/dofus/guide/dofus-guide-des-sorts-et-variantes-du-sram-2230) e no
  [devblog das variantes, JeuxOnline](https://dofus.jeuxonline.info/actualite/53563/245-devblog-variantes-sorts)).
- **Limites do que conferi:** não achei uma fonte oficial atual com a regra exata de visão em cantos nem a fórmula de
  empurrão em vigor; as notas citadas são de versões passadas.

**Wakfu** (Ankama): a mesma família de regras; fugir do contato sofre o bloqueio, e **deslocamento forçado não sofre o
bloqueio** ([Wakfu Wiki, Block](https://wakfu.wiki.gg/wiki/Block); [Push](https://wakfu.wiki.gg/wiki/Push)).
**Into the Breach** (Subset Games): ataques inimigos avisados e empurrões que desfazem ameaças; os autores queriam que
toda perda parecesse culpa do jogador ([GDC 2019, design postmortem](https://www.gdcvault.com/play/1025772/-Into-the-Breach-Design);
[Game Developer](https://gamedeveloper.com/game-platforms/road-to-the-igf-subset-games-i-into-the-breach-i-)).
**Darkest Dungeon** (Red Hook): posição **sem grade**, em quatro fileiras; cada habilidade diz de que posição sai e
que posições atinge, e algumas movem o herói
([discussões e wiki da comunidade](https://darkestdungeon2.wiki.fextralife.com/Highwayman)). É a alternativa de menor
custo ao tabuleiro.
**Zona de controle** em táticos (Battle Brothers e outros): sair do alcance de um inimigo dá a ele um golpe livre
([fórum oficial de Battle Brothers](https://battlebrothersgame.com/?p=4150); [Wikipedia, "Zone of control"](https://en.wikipedia.org/wiki/Zone_of_control)).
**Divinity: Original Sin 2** (Larian): superfícies no chão que reaplicam estados a quem fica nelas
([dos2.wiki, Burning](https://dos2.wiki/wiki/Burning_(Status))).

**O que a pesquisa mudou nas escolhas:** a zona de controle entrou como +1 PM determinístico (o tacle de Dofus sem o
atributo); o empurrão contra unidade fere as duas (Arremesso); a água deixa ver e não passar (os obstáculos de Dofus
não bloqueiam todos a visão); os golpes preparados viraram casas marcadas (Into the Breach); a alternativa de fileiras
(Darkest Dungeon) ficou registrada como plano B barato (seção 11).

---

## 3. O que depende de quê

| Elemento de Dofus | Depende de | No protótipo | Por quê |
|---|---|---|---|
| Andar, casas alcançáveis | Movimento e posição | Sim | É o experimento |
| Alcance mínimo e máximo, em linha | Posição | Sim | Dá papéis (perto, longe, alinhado) |
| Linha de visão, obstáculos, unidades que tapam | Posição | Sim | Dá valor a onde parar e a quem fica na frente |
| Áreas (cruz, ao redor, linha) | Posição | Sim | Juntar e separar inimigos e aliados |
| Empurrar, puxar, colisão | Posição | Sim | Mudar a ameaça sem matar |
| Zonas no chão (glifos) | Posição e tempo | Sim (chamas) | Mudam caminhos |
| Invocações que ocupam casa | Posição | Sim (Sentinela) | Bloquear, oferecer alvo |
| Tacle e fuga como atributos | Posição e economia | Simplificado (+1 PM fixo) | Sem atributo novo |
| 6 PA e feitiços de 2 a 5 PA, vários por vez | Economia | **Não** | Multiplicaria ações e rebalancearia tudo (seção 5) |
| Limites de lançamento por vez e por alvo | Economia | Não | Só fazem sentido com vários lançamentos por vez |
| Roubo de PA e PM | Economia | Não | Idem; a Sentinela tira 1 PM, o mínimo para testar |
| Iniciativa, fase de posicionamento inicial | Ordem e preparação | Não | A ordem do jogo fica (pedido do Jean); posições iniciais fixas |
| Visão isométrica, sprites em 8 direções, altura | **Apresentação** | Não | Nada disso muda regra; a grade vista de cima testa as mesmas |
| Células em losango | Apresentação | Não | A grade quadrada com distância em casas dá o mesmo losango de alcance |

---

## 4. As regras provisórias do protótipo

Explícitas e pequenas; todas no código (`motor/conteudo.py`, `motor/grade.py`) e no quadro "Como funciona" da tela.

| Regra | Valor | Por quê |
|---|---|---|
| Arena | 9 × 7 casas; o grupo nas colunas 0 a 2, os inimigos nas 5 a 8 | Contato em uma ou duas rodadas, espaço para flanquear e recuar sem virar caminhada |
| A vez | **Uma ação principal e PM** (3 para o grupo; lobos 4; sapo e troll 2) | Preserva a economia atual; o movimento é a única decisão nova (seção 5) |
| Andar e agir | **Andar antes de agir; agir encerra o movimento** (padrão). A outra regra (andar também depois) fica num interruptor | A fuga repetida (seção 6) |
| Distância | Casas nas quatro direções (sem diagonal); o alcance desenha um losango | Como Dofus; sem a pergunta "diagonal custa quanto" |
| Visão | Segmento entre os centros; rocha e unidades no meio tapam; num canto exato, só tapa se as duas casas taparem | Simples de prever; quem fica na frente protege |
| Obstáculos | Rocha: bloqueia passagem e visão. Água: bloqueia passagem, deixa ver | Dois tipos já dão decisões diferentes (atirar por cima da água) |
| Ocupação | Uma unidade por casa; atravessa-se aliado, não inimigo; não se para em casa ocupada | Evita o grupo se trancar sozinho |
| Zona de controle | Sair de uma casa vizinha a um inimigo custa **1 PM a mais** (interruptor) | O tacle de Dofus, sem atributo |
| Empurrão | Na direção de quem empurra; parado por rocha, água, borda ou unidade: **6 de dano por casa que faltou**; não paga zona | Mudar a ameaça; usar o terreno |
| Puxão | Até ficar ao lado de quem puxa; para no primeiro bloqueio; sem dano de colisão | Trazer quem está atrás |
| Áreas | Atingem aliados, salvo o que a habilidade ou o talento diz (Redemoinho só inimigos; Chamas Seletivas) | O fogo amigo faz a posição do grupo importar |
| Chamas no chão | Criadas pela Muralha (e pelo Rastro); duram 2 rodadas (Fogo Eterno: a luta); quem entra ou começa a vez nelas: 4 de fogo e 1 camada, uma vez por vez | Zona que muda caminhos; a IA a evita |
| Golpe preparado | Marca o alvo e as casas vizinhas; na próxima vez do inimigo, atinge quem estiver nelas; atordoar interrompe | A resposta espacial: sair das casas |
| Ordem | A do jogo (Agilidade, fixa). Invocações não têm vez | Pedido do Jean; Revezamento e afins continuam fora |
| Invocação | Sentinela de Gelo ocupa uma casa, bloqueia passagem e visão; inimigos que começam a vez ao lado dela perdem 1 PM | Posição da invocação decide |
| Efeitos fora do espaço | Os do X1: dano, Queimadura, Guarda, Força, Exposto, Fortalecido, Enfraquecido, atordoar e Firme | Reaproveitados |

---

## 5. A economia da vez, comparada

| Hipótese | Como é | Ganha | Perde | Para o nosso jogo |
|---|---|---|---|---|
| A de hoje (cards) | Uma ação; sem movimento | Clareza, ritmo, 1 comando | Posição não existe | Base de comparação |
| **Ação + PM antes (escolhida)** | Andar e depois agir; agir encerra o movimento | Movimento é uma decisão por vez ("de onde agir"); ~2,4 comandos por vez | Não dá para bater e recuar | Preserva o X1 inteiro; mede só o espaço |
| Ação + PM antes e depois | Andar, agir, andar | Bater e recuar, reposicionar depois de ver o efeito | **Fuga dominante** (seção 6); mais comandos | Interruptor no protótipo para comparar |
| PA e PM (Dofus) | 6 PA, feitiços de 2 a 5, vários por vez | Combinações na mesma vez, muita expressão | Rebalanceia todo o catálogo e os recursos; mais comandos e mais tempo | Fora; seria outro projeto |
| Andar ou agir (Darkest Dungeon) | Cada vez é uma coisa | Mais simples | Andar vira perder a vez; posição sem grade é mais barata | Plano B (seção 11) |

---

## 6. A fuga repetida

**A verificação:** um jogador automático "recuo" escolhe só casas a 3 ou mais do inimigo mais perto quando pode, ataca
de lá e, se as regras permitem, gasta o resto dos PM se afastando. Comparado com o "luta" (o mesmo cálculo de valor,
sem a regra de distância). 12 lutas por linha, `ferramentas/simular.py`.

**Com "andar depois de agir" e zona de controle ligada (a primeira hipótese):**

| Piromante | Lutando: vitórias, vida no fim | Recuando: vitórias, vida no fim |
|---|---|---|
| Campo aberto | 100%, 93% | 100%, 62% |
| A passagem | 91%, 66% | 100%, 38% |
| Perto e longe | 100%, 53% | **100%, 75%** |
| O troll | 100%, 55% | 83%, 85% |

Na luta das prioridades, **recuar vencia com mais vida que lutar**: a fuga era dominante.

**As causas investigadas, antes de pensar em punição:**
1. **Zona de controle:** quase não muda nada (quem foge nunca fica vizinho de um inimigo). Desligada, os números ficam
   parecidos.
2. **Andar depois de agir:** é a causa. Com uma ação e 3 PM livres depois dela, atirar a 5 e recuar 3 por vez mantém
   qualquer inimigo de 3 PM longe para sempre. Em Dofus, quem faz isso paga PA por feitiço e enfrenta monstros com mais
   PM e alcance; com uma ação só, o recuo sai de graça.
3. **Velocidade e alcance:** o troll tem 2 PM e só bate de perto; os lobos têm 4 PM, mas são frágeis.

**A mudança, estrutural e não punitiva:** "agir encerra o movimento". Resultado com essa regra:

| Piromante recuando | Antes | Depois |
|---|---|---|
| Perto e longe | 100%, 75% | **16%, 3%** (a bruxa atira de longe e o sapo puxa) |
| A passagem | 100%, 38% | 58%, 28% |
| Campo aberto | 100%, 62% | 100%, 83% (os lobos frágeis morrem antes de chegar) |
| O troll | 83%, 85% | 100%, 94% (o troll, lento, nunca alcança ninguém) |

**O que fica:** recuar ainda vence contra o troll (2 PM, sem ataque à distância) e contra os lobos. As respostas
naturais seriam de conteúdo, não de regra: dar ao troll um ataque à distância (arremessar pedra) ou uma investida, ou
não deixar um gigante lento sozinho no campo aberto. Registrado como pendente (seção 10). O Berserker não foge (é corpo
a corpo): recuando, perde quase sempre.

---

## 7. Habilidades e talentos espaciais

**Berserker** (3 PM): Golpe Pesado (perto); **Investida** (avança em linha até o alvo, sem gastar PM e sem pagar a zona:
chegar); **Golpe de Escudo** (empurra 2, colisão: afastar e usar o terreno); **Corrente** (puxa em linha: trazer quem
está atrás); **Redemoinho** (as 8 casas ao redor, só inimigos: cercado, bater em todos); **Guarda-costas** (golpes contra
aliados vizinhos vêm para ele: proteger quem está perto).
**Piromante** (3 PM): **Bola de Fogo** (2 a 5, com visão); **Chuva de Brasas** (cruz no ponto, atinge aliados: juntar
inimigos, separar aliados); **Muralha de Fogo** (3 casas em chamas: fechar ou encarecer um caminho); **Combustão**
(cobrar camadas à distância); **Explosão de Calor** (empurra os 4 vizinhos, aliados também: abrir espaço);
**Sentinela de Gelo** (invocação que bloqueia passagem e visão e tira 1 PM de quem começa ao lado: fechar uma passagem).
**Morel:** Atacar; **Golpe Oportuno** (+60% em quem está **cercado**, com outro aliado ao lado do alvo, além de
atordoado ou preparando: flanquear); Proteger (só vale lado a lado). **Odette:** Bastão; **Luz** (2 a 4, com visão);
Prece e Bênção (até 3, com visão).

**Os talentos** (um de cada par), escolhidos por mudar o uso do espaço:

| Par | Opção A | Opção B | O que muda na posição |
|---|---|---|---|
| Berserker · linha de frente | **Âncora**: sair de perto de Jean custa +2 PM aos inimigos | **Caçador**: derrubar dá 3 PM, mesmo depois de agir | Segurar uma linha ou atravessar o campo |
| Berserker · empurrão | **Colisão Brutal**: colisão em dobro e atordoa | **Arremesso**: empurra 4; quem é atingido pelo empurrado leva o mesmo | Empurrar contra a parede ou contra outro inimigo |
| Piromante · área | **Chamas Seletivas**: a Chuva e a Explosão poupam aliados | **Labareda**: Chuva em 13 casas, aliados também | Lutar colado ao grupo ou arrumar o grupo para a área grande |
| Piromante · chão | **Rastro de Brasas**: a Bola põe fogo na casa do alvo | **Fogo Eterno**: a Muralha dura a luta | Fogo espalhado e pequeno, ou um muro permanente |
| Piromante · detonação | **Estouro**: quem morre em chamas explode nas casas vizinhas | **Combustão em Área**: a Combustão detona também os vizinhos do alvo | As duas premiam inimigos juntos, de jeitos diferentes |

**O que ficou de fora, e por quê:** a Lança de Gelo em linha e o Frio (mais um estado sem papel espacial novo); o
Fogo-fátuo e o Estandarte (a Sentinela já testa invocação com posição); teleporte (mobilidade pura: a Investida e o
Caçador já testam); armadilhas (uma zona no chão basta); cones e linhas de dano (a cruz e o "ao redor" já testam
formas); as ultimates (o espaço muda pouco nelas); o catálogo de 32 do X1 (não era o objetivo).

---

## 8. Encontros e inimigos

| Encontro | Objetivo | Equivalente no X1 |
|---|---|---|
| **Campo aberto** · três lobos (4 PM) | O movimento vira só aproximação? Recuar e atacar vence? | Três lobos |
| **A passagem** · o mercenário e dois bandidos | Uma parede de rocha com uma passagem e um trecho de água: segurar, fechar ou usar a passagem | O mercenário e dois bandidos |
| **Perto e longe** · a bruxa, o bandido e o sapo | A bruxa atira e cura de trás das rochas; o sapo puxa quem fica em linha; quem atacar primeiro | A bruxa, o bandido e o sapo |
| **O troll** | Um gigante lento que prepara um golpe em área | O troll sozinho |

As composições, a vida e o dano são os do X1; a força real muda com o espaço (seção 9).

**Como os inimigos agem** (`_ia_perto`, `_ia_longe`, `_ia_lingua`):
- **Perto** (lobo, bandido, mercenário, troll): o caminho mais barato até uma casa vizinha de um alvo (o grupo antes da
  Sentinela; depois, o mais ferido), evitando chamas quando o desvio é curto; sem caminho, a casa mais perto possível.
  Ao lado de alguém: golpe ou habilidade (uivo, grito, Golpe Esmagador, Golpe Sujo).
- **Longe** (bruxa): cura se alguém está abaixo de 60% (a cada 3 rodadas); senão, procura uma casa com visão de um alvo,
  longe do grupo, e atira.
- **Língua** (sapo): procura uma casa alinhada a 2 ou 3 de alguém, com visão, e puxa e morde; senão, vai até alguém.
- **Medido** (seção 9): nas lutas com a regra padrão, de 0% a 6% das vezes um inimigo nem anda nem age; de 3% a 22%
  das vezes ele anda sem chegar a agir. O maior "sem ação" é no campo aberto (aproximação) e na passagem
  (congestionamento: os bandidos ficam atrás do mercenário).

---

## 9. Comparação com os cards

**Como comparar:** o mesmo encontro nos dois protótipos. O X1 ganhou dois exemplos, "Comparar com o tático" (Berserker
e Piromante), com os equivalentes em cards dos kits táticos e sem talentos. O registro do tático guarda, por luta:
comandos (andar, agir, encerrar), comandos por vez, casas andadas, PM usados e disponíveis, vezes sem andar, PM pagos à
zona de controle, **tempo decidindo onde andar e tempo decidindo a ação** (cada comando leva o tempo desde o último
desenho), colisões e casas empurradas, áreas que pegaram aliados e vezes em que os inimigos não agiram.

**Primeiras observações** (jogadores automáticos; regra padrão; não medem graça):

| | Cards (X1, jogador aleatório) | Tático (jogador "luta") |
|---|---|---|
| Comandos por vez | 1 | 2,2 a 2,5 |
| Rodadas: lobos | 4 a 7 | 4 a 5 |
| Rodadas: mercenário | 6 a 9 | 9 a 14 |
| Rodadas: troll | 8 a 13 | 15 a 24 |
| Inimigos sem ação | 0% (sempre alcançam) | 3% a 22% |

O Berserker tático sofre na passagem (33% de vitórias para o jogador automático, que entra sozinho e fica cercado na
abertura). Isso é, ao mesmo tempo, um defeito do jogador automático e um sinal real: o espaço pune a falta de
coordenação que os cards não punem.

**O que observar jogando** (o seu pedido, ponto a ponto): as decisões novas; as habilidades com papéis mais distintos;
se os talentos mudam o uso do espaço; o tempo decidindo contra o tempo só deslocando; quantos comandos para uma
intenção; a clareza do alcance, da área e da visão; a comitiva e os inimigos; a duração e o ritmo. **Mais comandos,
mais regras e mais duração não contam como profundidade**: a pergunta é se cada comando a mais foi uma escolha.

---

## 10. Riscos, observados e não observados

| Risco | Observado? | Onde | Resposta possível |
|---|---|---|---|
| Aproximação obrigatória antes de lutar | Sim, pequeno | Campo aberto: 1 a 2 rodadas; 16% a 22% das vezes de inimigo sem ação | Arena pequena (9 × 7) e posições iniciais perto já ajudam; inimigos à distância no começo |
| Deslocamento sem decisão | A medir com você | O registro conta vezes sem andar e o tempo de andar | Se andar for só "chegar perto", tirar movimento de quem não precisa |
| Fuga dominante | Sim | Seção 6; resolvida em parte pela regra | Conteúdo: inimigos com alcance ou investida; não deixar o lento sozinho |
| Congestionamento | Sim | A passagem: os bandidos esperam atrás do mercenário | É também a graça da passagem; a IA poderia contornar pela água (não pode) ou esperar |
| Inimigos que andam mal | Não, no que medi | 0% a 6% parados; o teste automático falha se passar de 15% | A IA ainda é simples (não flanqueia de propósito, não protege a bruxa) |
| Batalhas longas | Sim | Troll 15 a 24 rodadas; passagem 9 a 14 | Números do X1 (vida do troll, regeneração) pensados para cards; ajustar se a direção seguir |
| Interface lotada em 1280 × 720 | Não | A grade 9 × 7 cabe com casas de ~76 px e o painel ao lado | Arena maior não caberia sem rolagem |

---

## 11. Impacto e trabalho, se seguirmos

| Área | Impacto | Reaproveita | Refaz |
|---|---|---|---|
| Habilidades | Todas ganham alcance, linha, visão e área; muitas ganham função espacial | Os blocos de efeito (dano, estado, camadas) | A definição de cada uma (45 de classe e especialização) |
| Talentos | Os gatilhos ficam; entram regras de espaço | `modificadores.mod/disparar` | Parte dos 34; novos espaciais |
| Comitiva | Três a posicionar e invocações | Kits, controle pelo jogador | O ritmo (3 vezes mais comandos) |
| Inimigos | Cada família ganha papel de movimento e alcance | Vida, dano, habilidades | A IA inteira; preparações viram áreas marcadas |
| Interface | A grade vira o centro da luta | Componentes de ficha, descrição, registro | `batalha.js` quase todo; a placa da ordem fica |
| Duração | Mais rodadas e mais comandos | — | Números de vida e dano por encontro |
| Arte | Precisa de marcadores (já servem) e, depois, de figuras vistas de cima; arenas com obstáculos | Retratos nas fichas; a paleta | Sem isometria: figuras pequenas de cima e arenas por bioma |
| Saves e campanha | Lutas não guardam posição: sem migração de save | Tudo fora da luta | Os encontros ganham mapas pequenos |
| Testes | O gabarito muda todo | A estrutura de testes | As transcrições |

**Se seguirmos, em etapas:** (1) o núcleo espacial no motor do jogo (arena, visão, caminhos, alcance) atrás de um
interruptor, sem mudar o catálogo; (2) a conversão do catálogo e dos talentos; (3) a IA por papel; (4) a tela de luta
com a grade; (5) os encontros da campanha com mapas pequenos (junto da etapa 9); (6) a arte. A etapa 9 (campanha)
dependeria disso.

**Plano B, mais barato:** posição sem grade, em fileiras (Darkest Dungeon): cada habilidade diz de onde sai e onde
atinge, empurrões trocam fileiras, áreas pegam fileiras. Mantém parte das funções (afastar, trazer, proteger, área) sem
navegação, IA de caminho nem mapas. Não foi prototipado.

---

## 12. O que avaliar jogando

Abra `ferramentas/prototipos/etapa8-tatico/demo.bat` (abre sozinho na porta livre e mostra a versão "Tático 1" no topo).
Compare com o X1 (`etapa8-builds/demo.bat`, exemplos "Comparar com o tático").

1. **Decisões novas:** em quantas vezes você parou para pensar onde ficar, e não só o que fazer?
2. **Papéis:** o Golpe de Escudo, a Corrente, a Sentinela, a Muralha, a Explosão de Calor viraram ferramentas
   diferentes, ou só "mais uma forma de dano"?
3. **Talentos:** trocar Chamas Seletivas por Labareda, ou Âncora por Caçador, mudou como você jogou?
4. **Comandos e tempo:** os comandos a mais (andar, depois agir, depois encerrar) foram escolhas ou burocracia?
5. **Clareza:** alcance, visão, área, casas marcadas e chamas se leem sem consultar nada?
6. **Ritmo:** as lutas ficaram longas demais (o troll)? A aproximação no campo aberto incomodou?
7. **Comitiva e inimigos:** posicionar três ficou pesado? Os inimigos pareceram espertos o bastante?
8. **As regras em teste:** jogue uma luta com "andar depois de agir" ligado e outra desligado; e com a zona de controle
   ligada e desligada. Qual combina com o jogo que você quer?

**A pergunta central continua aberta:** o espaço cria decisões e possibilidades de build que tornam este jogo melhor,
sem comprometer a clareza e o ritmo?
