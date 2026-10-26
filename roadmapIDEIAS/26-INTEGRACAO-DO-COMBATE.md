# 26 — Integração do combate na campanha (etapa 4, 1.211.0)

Autorização: seção 3.10 do [25](25-ETAPA4-REFORCO-E-ENCANTAMENTO.md) (commits `196572af`, `bdf80b48`). Este documento
guarda as escolhas da integração, o catálogo provisório, as medidas e o roteiro de teste. **Números e catálogo são
provisórios**; a estrutura é a aprovada. Os protótipos (`ferramentas/prototipos/combate-atributos/`) ficam como
histórico: o jogo não depende deles. **A etapa 4 continua aberta** (reforço e encantamento completos não começaram).

## Como o combate era (antes da integração)

Fases fixas por volta: a sua ação → aliados (comitiva automática, animal, servos) → inimigos; o recurso do herói
regenerava no fim da volta. Atributos derivados (`max_hp`, `atk`, `defesa`, `agi`, `poder`, `max_rec`) vinham da
classe, do nível, dos talentos e do equipamento; a Agilidade dava esquiva e crítico. Todas as habilidades aprendidas
ficavam sempre na luta. Os companheiros agiam sozinhos. Os inimigos já preparavam golpes (`carregando`), e atordoar
desfazia a preparação.

## A estrutura integrada

- **Ordem fixa por turnos individuais.** No começo da luta, todos (você, a comitiva, o animal, os inimigos) entram
  numa ordem pela Agilidade (desempate: Percepção, depois aliado antes de inimigo, depois a ordem de entrada) que não
  muda. Cada um tem a sua vez; a rodada termina quando todos tiveram a vez, inclusive quem a perdeu. Quem entra no meio
  (servo invocado, criatura chamada) vai para o fim da ordem e age a partir da rodada seguinte. A tela mostra a ordem
  na placa da rodada (quem age, quem já passou, quem está fora, quem espera); o terminal, numa linha "Ordem:".
- **Uma ação principal por vez**: Atacar, Defender, Usar item (fora do kit) ou uma habilidade do kit. Defender: −40%
  de dano até o começo da próxima vez de quem defendeu.
- **Comitiva controlada**: na vez de Odette, Morel ou Yara, você escolhe a ação (ataque, Defender, item da bolsa do
  grupo, as habilidades dela), com a mesma roda da sua vez, ao lado da carta dela. Cada uma tem o recurso dela (Fé,
  Vigor, Mana: 40, cheio a cada luta, +5 por rodada). O animal do Patrulheiro e os servos continuam automáticos (o
  controle deles é decisão separada, 3.4 do 25).
- **Kit**: as habilidades aprendidas ficam no Grimório; o kit é o que vai para a luta: 8 pontos, 5 espaços, no máximo
  uma ultimate (comum 1, avançada 2, ultimate 3). Troca-se na vila e na fogueira: na tela, o botão "Levar no kit" ou
  "Tirar do kit" na página da habilidade no Grimório; no texto, a linha "Kit de habilidades". Aprender uma habilidade
  a põe no kit se couber; senão, avisa e ela espera no Grimório.
- **Ultimate**: uma vez por luta, desde o nível 6, gasta a vez e recurso; cair e voltar não devolve o uso; a luta
  seguinte a devolve.
- **Atributos graduais** (Força, Agilidade, Constituição, Intelecto, Percepção, Vontade; Presença só fora da luta),
  somados aos derivados de antes, que continuam sendo a conta do golpe. Sem desbloqueio por pontuação.
- **Tipos de dano e defesas**: o físico encontra a Defesa; os elementos encontram a resistência do alvo (os
  multiplicadores que os inimigos já tinham). A Tenacidade (Vontade) é a chance de resistir a atordoar, congelar e
  prender, separada da resistência a dano. A carta da ação mostra o tipo ("· fogo").

## Escolhas operacionais (provisórias)

| Assunto | Escolha |
|---|---|
| Atributos iniciais | 24 pontos nos seis de combate. Guerreiro FOR 6 AGI 3 CON 5 INT 2 PER 3 VON 5; Arqueiro FOR 5 AGI 6 CON 3 INT 2 PER 6 VON 2; Mago FOR 1 AGI 4 CON 3 INT 9 PER 3 VON 4. Presença 3. No nível 1, os totais são os de antes (Vida, Ataque, Agilidade, recurso) |
| Subir de nível | +2 pontos de atributo, distribuídos quando você quiser, fora da luta: o "+" na ficha (Inventário) ou "Atributos" no texto. Não interrompe o fim da luta. A Presença sobe 1 a cada 3 níveis, sozinha |
| Conta dos derivados | Ataque = classe + nível + Força; Poder = classe + nível + Intelecto; Vida = classe + nível + 4 × Constituição; Recurso máx. = classe + nível + 3 × Vontade; Agilidade = classe + nível + Agilidade. Crítico +1% por ponto de Percepção; Tenacidade 4% por ponto de Vontade (teto 40%). Defesa: classe e equipamento |
| Esquiva | A Agilidade continua dando a esquiva de sempre (1,2% por ponto, teto 40%), além da ordem. A primeira versão tirava a esquiva do herói; a medida mostrou o Arqueiro (Sombra) caindo de 89% para 60% de vitórias nas lutas comuns, e ela voltou |
| Testes do d20 | Cada teste pelo seu atributo: Força, Destreza (Agilidade), Arcano (Intelecto), Percepção, Vontade; Carisma pela Presença acima de 3 e a Reputação. ×1,5 deixa o bônus perto do de antes; ferimento e fome que tiram do Ataque, da Agilidade ou do Poder tiram também do teste |
| Recurso entre lutas | Volta ao máximo no fim de cada luta (a reserva de uma luta). A vida não volta: descanso, poções, curandeira |
| Companheiro caído | Fica fora até descansar (dormir na vila ou na fogueira), como já era. Na luta, volta só pelo Reerguer de Odette (30 de Fé, uma vez por luta, 30% da vida) ou pela Pena de Fênix (40% da vida), no mesmo lugar da ordem: se a vez dele já passou na rodada, age na seguinte |
| Protagonista caído | Como era: a Pena de Fênix e a proteção levantam sozinhas; senão, derrota (resgate, ou fim no hardcore). Os modos de dificuldade não mudaram |
| Ultimate numa nova luta | Disponível de novo |
| Fim de luta arrastado (debandada) | Desde a 1.212.0: só numa luta comum (sem título de cena, com saída, 2+ inimigos), avaliada no fim da rodada, com metade ou mais do grupo morta, você com 40% da vida ou mais, os que sobram somando até 15% da vida inicial e todos inofensivos; então, 50% de chance por rodada. Quem foge dá XP, mas não ouro, espólio nem abate. Detalhes em "Ajustes da 1.212.0" |
| Saves | Formato 7. O save antigo ganha os atributos iniciais mais os pontos dos níveis já subidos (pela preferência da classe) e a Presença dos níveis; a base é refeita para os totais ficarem iguais; Inferno vira Chuva de Brasas e Fênix vira Conflagração; o herói aprende o repertório novo do nível dele; o kit é montado com o que couber. Conferido nos 38 saves de `~/.cronicas_da_fenda` (só leitura, nenhum arquivo alterado): todos migram, e os da versão 6 mantêm os mesmos totais |

## Conversões (nada morto em silêncio)

- **Crítico**: vinha da Agilidade; agora vem da Percepção (1% por ponto). O Arqueiro trocou 2 pontos iniciais de
  Agilidade por Percepção (a base de Agilidade subiu 2 para a esquiva do nível 1 ser a mesma). A Sombra, que tirava o
  crítico da Agilidade da especialização, ganhou +6% de crítico de especialização (aparece na escolha do caminho).
- **Inferno e Fênix** saíram do catálogo (o conjunto de fogo do Piromante é Brasa, Combustão, Chuva de Brasas e
  Conflagração). Os saves trocam um pelo outro.
- **A comitiva automática** (`comitiva.agir`) saiu: a vez dela é sua. A Prece de Odette continua limpando os males
  com aprovação 75 ou mais (está na descrição).
- **Pés Leves** (+2 de Agilidade por ponto) continua valendo esquiva, ordem e fuga; a descrição diz isso.
- **"Turno" na tela** virou "Rodada" (a placa, o registro, o terminal); "turno" é a vez de cada um.
- **O Tiro Imobilizador** dizia "prender" e fazia atordoar: agora diz atordoar.
- **O robô dos testes e o simulador** escolhem a ação pela meta (`acao`), não pela posição; o kit dos níveis de teste
  é montado por papel (`kit.sugerido`), o robô faz o combo de fogo e joga pela comitiva (Odette cura e levanta, Morel
  interrompe e aproveita, Yara amaldiçoa o chefe).

## Repertório provisório

Pesquisa (1.211.0, para o tamanho e os papéis, não para copiar): RPGs por turnos com classes fixas dão 8 a 10
habilidades por classe ao longo do jogo e um conjunto menor por especialização, com uma habilidade forte limitada. A
ordem visível de Final Fantasy X (a lista de quem age) inspirou a placa da ordem
([gamerguides](https://www.gamerguides.com/final-fantasy-x-hd/guide/introduction/gameplay/battle-system),
[jegged](https://jegged.com/Games/Final-Fantasy-X/Tips-and-Tricks/CTB-Window.html)); a quebra de Octopath Traveler,
a vulnerabilidade e o interromper ([gamerguides](https://www.gamerguides.com/octopath-traveler/guide/the-basics/game-mechanics/battle-system));
os estados numéricos de Slay the Spire (Vulnerável, Fraco, Proteção), estados claros com números
([wiki](https://slay-the-spire.fandom.com/wiki/Vulnerable)); a moral de Battle Brothers, o inimigo que foge quando a
luta está perdida (fórum, não confirmado); a frustração com o controle binário de Divinity: Original Sin 2, o motivo de
a Tenacidade ser uma chance (fórum de jogadores).

O catálogo, como está no jogo (gerado de `rpg/habilidades.py`; "Kit" é o custo em pontos do kit, "Custo" o do
recurso na luta; a aquisição é o nível em que se aprende, por subida de nível):

| Habilidade | Quem, nível | Alvo | Tipo | Escala | Custo | Kit | Papel | O que faz |
|---|---|---|---|---|---|---|---|---|
| Golpe Pesado | Guerreiro 1 | um inimigo | físico | Ataque | 10 | 1 (comum) | dano num alvo | Causa 170% do Ataque em dano físico. |
| Erguer Escudo | Guerreiro 1 | você | — | — | 8 | 1 (comum) | defesa | Reduz o dano recebido em 50% por 2 turnos seus. |
| Investida | Guerreiro 2 | um inimigo | físico | Ataque | 12 | 1 (comum) | dano num alvo | Causa 120% do Ataque em dano físico. Se acertar, 45% de chance de atordoar o alvo: ele perde a próxima vez. |
| Lâmina Rúnica | Guerreiro 2 | um inimigo | arcano | Poder | 14 | 2 (avançada) | dano num alvo | Causa 160% do Poder em dano arcano. |
| Grito de Guerra | Guerreiro 3 | você | — | — | 14 | 2 (avançada) | apoio/controle | Aumenta o seu dano em 30% por 3 turnos seus. Cada inimigo tem 80% de chance de ficar enfraquecido (−25% de dano) por 2 turnos dele. |
| Proteger | Guerreiro 3 | um aliado | — | — | 8 | 1 (comum) | apoio/controle | Até a sua próxima vez, os golpes contra o aliado escolhido acertam você. |
| Contragolpe | Guerreiro 5 | você | — | — | 8 | 1 (comum) | apoio/controle | Até a sua próxima vez, você revida cada golpe corpo a corpo recebido com 60% do Ataque. |
| Quebra-Guarda | Guerreiro 5 | um inimigo | físico | Ataque | 14 | 2 (avançada) | dano num alvo | Causa 110% do Ataque em dano físico. Se acertar, reduz a defesa do alvo em 40% por 2 turnos dele. |
| Égide Rúnica | Guerreiro 6 | você | — | — | 12 | 2 (avançada) | defesa | Cria uma barreira que absorve 10 + 140% do Poder em dano por 2 turnos seus. Não acumula. |
| Golpe Sagrado | Paladino 4 | um inimigo | sagrado | Ataque | 15 | 1 (comum) | dano num alvo | Causa 130% do Ataque + 80% do Poder em dano sagrado. Se acertar, cura você em 20% do dano causado. |
| Prece | Paladino 4 | você | — | — | 20 | 1 (comum) | defesa | Cura 25% da sua vida máxima + 100% do Poder e remove os males (veneno, sangramento, maldição, fraqueza). |
| Julgamento Divino | Paladino 6 | todos os inimigos | sagrado | Ataque | 36 | 3 (ultimate) | ultimate | Causa 120% do Ataque + 100% do Poder em dano sagrado a todos os inimigos. Não pode ser esquivado. |
| Sede de Sangue | Berserker 4 | um inimigo | físico | Ataque | 12 | 1 (comum) | dano num alvo | Causa 140% do Ataque em dano físico. Se acertar, rouba 40% do dano como vida e aplica Sangramento por 3 turnos do alvo. |
| Redemoinho | Berserker 4 | todos os inimigos | físico | Ataque | 22 | 2 (avançada) | área | Gira 5 vezes; cada giro causa 22% do Ataque em dano físico a todos os inimigos. |
| Fúria Cega | Berserker 6 | um inimigo | físico | Ataque | 0 | 3 (ultimate) | ultimate | Custa 15% da sua vida máxima. Aumenta o seu dano em 60% por 3 turnos seus e ataca o alvo com 130% do Ataque. |
| Tiro Certeiro | Arqueiro 1 | um inimigo | físico | Ataque | 8 | 1 (comum) | dano num alvo | Causa 170% do Ataque em dano físico, com +30% de chance de crítico. |
| Marcar Presa | Arqueiro 1 | um inimigo | — | — | 6 | 1 (comum) | dano num alvo | O alvo recebe 25% mais dano de todos os golpes (os seus, os da comitiva e os do animal) por 3 turnos dele. |
| Chuva de Flechas | Arqueiro 2 | todos os inimigos | físico | Ataque | 20 | 2 (avançada) | área | Causa 100% do Ataque em dano físico a todos os inimigos. Gasta 1 flecha por inimigo. |
| Mirar | Arqueiro 2 | você | — | — | 4 | 1 (comum) | apoio/controle | O seu próximo ataque é crítico. |
| Passo Ágil | Arqueiro 3 | você | — | — | 6 | 1 (comum) | defesa | Aumenta a sua esquiva em 30% por 2 turnos seus (a esquiva total vai até 60%). |
| Tiro Imobilizador | Arqueiro 3 | um inimigo | físico | Ataque | 12 | 2 (avançada) | dano num alvo | Causa 80% do Ataque em dano físico. Se acertar, 60% de chance de atordoar o alvo: ele perde a próxima vez e o golpe que preparava. |
| Flecha Perfurante | Arqueiro 5 | um inimigo | físico | Ataque | 12 | 2 (avançada) | dano num alvo | Causa 120% do Ataque em dano físico. Se acertar, reduz a defesa do alvo em 30% por 2 turnos dele. |
| Flecha Sangrenta | Arqueiro 5 | um inimigo | físico | Ataque | 8 | 1 (comum) | dano num alvo | Causa 100% do Ataque em dano físico. Se acertar, aplica Sangramento por 3 turnos do alvo. |
| Rajada | Arqueiro 6 | um inimigo | físico | Ataque | 16 | 2 (avançada) | dano num alvo | Dispara 3 vezes; cada disparo causa 60% do Ataque em dano físico a um inimigo sorteado. |
| Tiro Duplo | Patrulheiro 4 | um inimigo | físico | Ataque | 10 | 1 (comum) | dano num alvo | Dispara 2 vezes, 90% do Ataque cada: o 1º no alvo, o 2º no inimigo mais ferido. Sozinho, os dois no alvo. |
| Ordem da Fera | Patrulheiro 4 | um inimigo | físico | Ataque do animal | 12 | 1 (comum) | dano num alvo | O animal age por ordem sua: o urso protege você, o lobo dilacera o alvo, o falcão o cega. |
| Fúria da Natureza | Patrulheiro 6 | todos os inimigos | físico | Ataque | 32 | 3 (ultimate) | ultimate | Causa 130% do Ataque em dano físico a todos os inimigos, com 50% de chance de Sangramento em cada um, e cura o animal por completo. |
| Desaparecer | Sombra 4 | você | — | — | 10 | 1 (comum) | apoio/controle | O seu próximo ataque é crítico de ×2,3, e a sua esquiva aumenta em 50% por 1 turno seu. |
| Flecha Envenenada | Sombra 4 | um inimigo | físico | Ataque | 10 | 1 (comum) | dano num alvo | Causa 100% do Ataque em dano físico. Se acertar, aplica Veneno por 4 turnos do alvo. Não afeta mortos-vivos nem construtos. |
| Execução | Sombra 6 | um inimigo | físico | Ataque | 16 | 3 (ultimate) | ultimate | Causa 320% do Ataque em dano físico se o alvo estiver com até 35% da vida; acima disso, 120%. |
| Bola de Fogo | Mago 1 | um inimigo | fogo | Poder | 14 | 1 (comum) | dano num alvo | Causa 150% do Poder em dano de fogo. Se acertar, 60% de chance de aplicar 1 camada de Queimadura (até 3). |
| Meditar | Mago 1 | você | — | — | 0 | 1 (comum) | recurso | Recupera mana: 6 + 12% do máximo. |
| Lança de Gelo | Mago 2 | um inimigo | gelo | Poder | 10 | 1 (comum) | dano num alvo | Causa 130% do Poder em dano de gelo. Se acertar, 35% de chance de congelar o alvo: ele perde a próxima vez. |
| Runa da Fragilidade | Mago 2 | um inimigo | — | — | 8 | 1 (comum) | dano num alvo | O alvo recebe 30% mais dano mágico (todo golpe que não é físico) por 3 turnos dele. |
| Barreira Arcana | Mago 3 | você | — | — | 20 | 2 (avançada) | defesa | Cria uma barreira que absorve 20% da sua vida máxima + 60% do Poder em dano por 2 turnos seus. Não acumula. |
| Sifão | Mago 3 | um inimigo | arcano | Poder | 10 | 1 (comum) | dano num alvo | Causa 110% do Poder em dano arcano. Se derrubar o alvo, recupera 15 de mana. |
| Nevasca | Mago 5 | todos os inimigos | gelo | Poder | 22 | 2 (avançada) | área | Causa 70% do Poder em dano de gelo a todos os inimigos. Cada um tem 20% de chance de congelar. |
| Descarga | Mago 6 | um inimigo | arcano | Poder | 24 | 2 (avançada) | dano num alvo | Causa 220% do Poder em dano arcano. |
| Brasa | Piromante 4 | um inimigo | fogo | Poder | 8 | 1 (comum) | dano num alvo | Causa 60% do Poder em dano de fogo e aplica 1 camada de Queimadura (até 3). Não pode ser esquivada. |
| Combustão | Piromante 4 | um inimigo | fogo | Poder + Queimadura | 14 | 2 (avançada) | dano num alvo | Consome a Queimadura do alvo e causa, em dano de fogo, o que ela ainda causaria, com +60% e +20% por camada. Sem Queimadura, causa 80% do Poder. |
| Chuva de Brasas | Piromante 5 | todos os inimigos | fogo | Poder | 18 | 2 (avançada) | área | Causa 35% do Poder em dano de fogo a todos os inimigos e aplica 1 camada de Queimadura em cada um. Não pode ser esquivada. |
| Conflagração | Piromante 6 | todos os inimigos | fogo | Poder + Queimadura | 30 | 3 (ultimate) | ultimate | Causa 70% do Poder em dano de fogo a todos os inimigos e consome a Queimadura de cada um, como a Combustão. Não pode ser esquivada. |
| Drenar Vida | Necromante 4 | um inimigo | sombra | Poder | 14 | 1 (comum) | dano num alvo | Causa 120% do Poder em dano de sombra. Se acertar, rouba 40% do dano como vida. |
| Erguer Servo | Necromante 4 | você | — | — | 22 | 2 (avançada) | apoio/controle | Invoca um servo esqueleto que provoca os inimigos por 2 turnos dele. No máximo 1 de cada vez (mais com talentos). |
| Maldição | Necromante 6 | todos os inimigos | — | — | 18 | 3 (ultimate) | ultimate | Amaldiçoa todos os inimigos por 4 turnos deles: 40% do Poder em dano por turno e −40% de defesa. |

A comitiva (kit fixo, recurso próprio de 40): **Odette** — Prece (14, cura o aliado; com aprovação 75+, limpa os
males), Escudo de Luz (12, barreira no aliado), Reerguer (30, levanta um caído, uma vez por luta); **Morel** — Golpe
no Joelho (15, 70% de atordoar), Golpe Oportuno (10, +60% em atordoado ou em quem prepara), Proteger (8); **Yara** —
Maldição (12, −25% de dano do alvo; pelo Vazio, também Maldição), Runa da Fragilidade (10, +25% de dano mágico), Seta
Sombria (16).

### Combos e alternativas

| Classe | Combo | Como funciona |
|---|---|---|
| Guerreiro | Quebra-Guarda → Golpe Pesado | A defesa do alvo cai 40% por 2 turnos dele; o golpe de 170% vem em seguida |
| Guerreiro | Investida → Golpe Oportuno (Morel) | O atordoado perde a vez e o golpe preparado; o Oportuno rende +60% nele |
| Guerreiro (rúnico) | Égide Rúnica + Lâmina Rúnica | O caminho do Intelecto: barreira e golpe arcano que crescem com o Poder |
| Arqueiro | Mirar → Tiro Certeiro | Crítico garantido no tiro de 170% |
| Arqueiro | Flecha Perfurante ou Marcar Presa → Rajada | Defesa −30% ou +25% de dano de todos antes dos três disparos |
| Arqueiro | Tiro Imobilizador em quem prepara | Atordoa (60%) e desfaz o golpe preparado |
| Mago | Runa da Fragilidade → Descarga ou Nevasca | +30% de dano mágico antes do golpe |
| Piromante | Brasa ou Chuva de Brasas → Combustão ou Conflagração | Camadas de Queimadura (até 3) e a detonação |
| Mago | Lança de Gelo em quem prepara | 35% de congelar: perde a vez e o golpe preparado |

Independentes: Golpe Pesado, Tiro Certeiro, Bola de Fogo, Descarga rendem sozinhos. Economia: Meditar, Sifão (+15 de
mana ao derrubar), o ataque básico (devolve recurso), Defender (sem custo).

## Ritmo

Medido em 1.211.0. A luta comum dura de 4 a 7 rodadas; com guardião, de 12 a 20. O que mudou no tempo:

| Luta (velocidade normal, decisão simulada de 0,6 s) | Decisões | Animação | Total |
|---|---|---|---|
| Guerreiro nv 4 contra 3 lobos, sozinho, antes | 6 | 19,8 s | 27,3 s |
| O mesmo, agora | 4 | 21,8 s | 25,2 s |
| Guerreiro nv 6 com Odette e Morel contra 3 lobos, agora | 12 | 21,5 s | 32,7 s |
| Mago nv 6 com Odette e Morel contra 2 bandidos e 1 cultista, agora | 12 | 21,9 s | 32,9 s |

- **As decisões triplicam com a comitiva** (você escolhe por ela): num jogador real, que leva 2 ou 3 s por escolha,
  é isso que alonga a luta, não a animação. A animação de uma luta fica em 20 a 22 s.
- **O fim arrastado**: a debandada tira a caçada do último inimigo fraco (nas lutas comuns de 2+ inimigos).
- Nenhum número de vida ou de dano dos inimigos mudou nesta entrega: o tamanho das lutas está nas tabelas abaixo, para
  a decisão de ajuste com o Jean jogando.

### Equilíbrio (python -m tests.equilibrio --lutas 12, com comitiva; média dos níveis 1 a 12, antes → agora)

| Caminho | Vitórias, lutas comuns | Vitórias, guardiões | Rodadas, comuns | Rodadas, guardiões |
|---|---|---|---|---|
| Paladino | 97% → 96% | 58% → 61% | 6,8 → 6,2 | 22,2 → 19,7 |
| Berserker | 99% → 97% | 60% → 64% | 5,3 → 5,7 | 19,2 → 17,3 |
| Patrulheiro | 96% → 97% | 49% → 56% | 5,3 → 5,6 | 14,7 → 15,1 |
| Sombra | 87% → 88% | 36% → 32% | 6,0 → 6,7 | 13,9 → 16,8 |
| Piromante | 83% → 82% | 43% → 47% | 5,6 → 6,2 | 10,9 → 12,8 |
| Necromante | 92% → 90% | 64% → 50% | 6,2 → 6,2 | 12,3 → 15,6 |

O robô do simulador joga o combo de fogo (acende até 2 camadas e detona) e joga pela comitiva como uma pessoa; sem
isso, o Piromante caía para 36%. O Necromante perde contra guardiões: a Fênix (250% num alvo, repetível) saiu, a
ultimate é uma por luta e o kit de 8 pontos com ela deixa só Barreira, Drenar Vida e Erguer Servo; não compensei. Sem
comitiva (`--sozinho`): Sombra 35% → 26% e Necromante 56% → 37% contra guardiões; os outros, perto de antes.
**Pendente para decidir com o Jean**: o orçamento do kit (8 pontos com uma ultimate de 3 sobra 5 para 4 espaços) e o
dano do Necromante contra chefes.

## O gabarito (por que as 24 partidas mudaram)

A primeira diferença de cada partida, conferida contra a 1.210.1 (as transcrições das duas versões, linha a linha):
- **as partidas de texto** mudam na primeira luta (a despensa): o lance `rodada` e o separador "rodada" no lugar de
  "turno"; depois disso, a ordem dos sorteios da luta é outra e tudo segue diferente;
- **as da tela gráfica** mudam no catálogo de estados mandado à tela (os estados novos: defendendo, protegido,
  retaliando, mirando, defesa quebrada, fragilizado);
- **as da comitiva** mudam na subida de nível (o aviso dos pontos de atributo) e, na luta, na vez de cada companheiro.

Procurei nas transcrições novas, fora dos lances, por "None", chaves soltas, "de o", particípio sem concordância e
erros: nada. As linhas novas mais comuns são as da integração (rodada, ordem, Defender, a vez da comitiva, o kit, os
atributos). O gabarito revelou um erro, corrigido antes de atualizar: o herói começava com o recurso pela metade.

## Roteiro de teste (para o Jean)

1. **Campanha nova** (qualquer classe): a despensa já é no combate novo. Repare na placa embaixo da arena ("Rodada 1"
   e a ordem), no botão **Defender** (tecla 2) e em **Habilidades** (tecla 3), que agora mostra só o kit.
2. **Subir de nível**: aparece "2 pontos de atributo" no painel; clique, ou abra o Inventário (I): o "+" ao lado de
   cada sigla. Passe o mouse (ou o Tab) numa sigla para ver o que ela dá agora.
3. **O kit**: na vila ou acampado, abra o Grimório (P). Cada página diz "No kit" ou "Fora do kit", o custo em pontos e
   o botão para levar ou tirar; o resumo ("Kit: 6/8 pontos, 4/5 habilidades") fica no topo. Fora da vila e da
   fogueira, o botão some e a página diz onde se troca.
4. **A comitiva**: com Odette ou Morel, a vez deles abre a mesma roda ao lado da carta deles. Odette cura e levanta;
   Morel atordoa e aproveita; a barra de Fé, Vigor ou Mana fica na carta.
5. **Lutas seguidas e chefe, num cenário de teste** (luta preparada; o nível não é o ritmo da campanha):
   `python -m tests.navegador.cenarios integracao` (abre a URL no navegador). Variáveis: `CLASSE=mago ESPEC=piromante
   NIVEL=6 LUTA=chefe CAIDO=morel PENAS=1`. Depois de cada luta: a seguinte sem descanso (vida e caídos continuam), a
   mesma de novo com tudo cheio, ou seguir jogando (acampe para trocar o kit).
6. **O que volta entre lutas**: o recurso volta cheio; a vida não; o companheiro caído fica fora até dormir; a
   ultimate volta.
7. **Combos**: Brasa → Combustão (Piromante), Mirar → Tiro Certeiro, Quebra-Guarda → Golpe Pesado, Investida →
   Golpe Oportuno de Morel.

**Provisório**: todos os números (pontos e espaços do kit, custos, multiplicadores, recurso da comitiva, Tenacidade,
Defender 40%, a debandada a 25%), o catálogo e o Golpe Oportuno. Saves antigos migram (testado nos seus, só leitura).

## Ajustes da 1.212.0 (depois do teste do Jean)

### Queimadura contra resistência

- **O que estava errado:** o código tornava imune à Queimadura quem tinha resistência ao fogo abaixo de 0,5 (o Cão
  infernal, ×0,24, e o afixo flamejante, ×0,3), e o texto dizia "não pega em quem resiste muito ao fogo". O dano por
  turno de quem pegava fogo não passava pela resistência. As duas coisas contrariavam a decisão: resistência reduz o
  dano; só a imunidade explícita impede.
- **Agora:** a Queimadura pega em todos, salvo quem é imune ao fogo (eficácia 0, uma regra explícita do inimigo, que a
  ficha dele mostra como "imune"; hoje nenhum inimigo é). O valor guardado é o de quem acendeu; o tique de cada turno
  passa pela eficácia do alvo uma vez (`estados.dano_do_tique`, a mesma conta mostrada na carta); a Combustão e a
  Conflagração consomem a Queimadura e detonam o valor guardado, e o golpe delas aplica a resistência uma vez
  (`Combate.atacar`). Testado: duas camadas que ardem 10 por turno num alvo comum ardem 2 num Cão infernal; a Combustão num alvo de
  resistência 0,5 causa a metade; o imune ao fogo não pega fogo.

### Descrição, resumo e cálculo

O Grimório mostra o resumo à vista (a faixa de dano, "não pode ser esquivado" uma vez, o que acontece com os números
de agora) e a conta em "Como é calculado", que abre por clique e teclado (fórmula, crítico, ganho por ponto, talentos,
exceções). A carta da ação na luta mostra a descrição e a faixa de dano, sem o crítico. A dica de um atributo começa
pelo que ele dá agora; o crítico e a Tenacidade têm dica própria (as células "Crítico" e "Tenacidade"). A skill
`texto-regras-fenda` registra os critérios.

### Atributos e kit fora do Inventário

- **Ficha lateral:** comparei a linha fixa com os seis atributos e o botão expansível, a 1920×945 e a 1280×720. A
  linha de sete colunas aperta o painel (as siglas e o "+" se encostam a 1280); ficou o **botão "Atributos"**, com
  "· +2" ligado aos pontos livres, que abre um quadro em duas fileiras com os valores, as dicas, o crítico, a
  Tenacidade e o "+" (apagado na luta). O mesmo desenho e os mesmos dados da ficha do Inventário.
- **Kit na barra:** entre a vida e o recurso e os indicadores, uma fileira com as habilidades do kit (ícone, dica com
  nome, custo e efeito; a ultimate com a borda de ouro e o ◆). Fora da luta, o clique abre a página dela no Grimório,
  que só oferece a troca na vila e na fogueira. Na luta a barra não aparece (as ações seguem na roda, na sua vez). Sem
  espaço (1280×720), vira "Kit · N habilidades", que abre a mesma lista; kit vazio diz "Kit vazio".

### Debandada

**Como era (1.211.0):** avaliada depois de cada vez; com 2+ inimigos, a luta com saída e sem título de cena, alguém já
morto, nenhum vivo chefe, preparando golpe, invocando ou com piso, e os vivos somando até 25% da vida inicial do grupo:
todos fugiam na hora. Efeitos: contavam como derrotados, então davam XP, ouro, **espólio do corpo** (contra o que este
documento dizia) e **contavam como abate** nos contratos de caça, no bestiário (mestre caçador), nas estatísticas e no
nêmesis.

**Como é (1.212.0):** avaliada no fim da rodada; exige metade ou mais do grupo morta, você com 40% da vida ou mais e os
que sobram somando até 15% da vida inicial; cada sobrevivente tem de ser inofensivo: sem golpe preparado, sem invocar,
sem habilidade que sustente o grupo (uivo, grito, cura, regenerar, reviver, maldição, teia...), sem regra própria
(chefe, único, elite com afixo, piso, o que a vitória sobre ele mostra) e sem poder derrubar ninguém do seu lado nem
com um crítico (`dano_previsto` × 1,6 contra a vida de cada um). Cumprido tudo, 50% de chance por rodada. Quem foge dá
XP (o encontro foi vencido); não dá ouro nem espólio e não conta como abate; o texto diz isso na hora ("Quem foge não
deixa espólio nem conta como abate nos contratos."). Missões e lutas de cena não debandam (têm título próprio ou
`ao_vencer`).

**Frequência**, nas mesmas lutas comuns com saída (6 caminhos, níveis 2, 4, 6 e 8, 10 lutas cada, as mesmas sementes e o
mesmo robô; `python -m tests.debandada` e `python -m tests.debandada antes`): das 172 lutas com 2+ inimigos, a debandada
acontecia em **140 (81%)**; agora, em **11 (6%)**. Testes de unidade cobrem quando acontece e quando não (golpe
preparado, ameaça de derrubar com pouca vida, quem sustenta, elite, chefe, cena, você ferido, muita vida restante) e as
consequências (abates, contrato, espólio, ouro, XP). **Ideia guardada, não feita:** quem foge volta depois (um encontro
com os fugitivos).

### Golpe Pesado

Sem mudança de número. Ele dura uma luta comum inteira (6 a 7 seguidos com o Vigor do nível 1 a 5; uma luta comum
tem 4 a 7 rodadas) porque o recurso volta cheio a cada luta e regenera 6 por rodada: é a economia, não o golpe. No
nível 1 é a única habilidade de dano do Guerreiro. Contra golpe preparado, as ferramentas próprias (Erguer Escudo,
Defender, Investida) existem; não achei evidência de que ele domine onde área, controle ou proteção deveriam valer. Se
o Jean quiser menos repetição, a alavanca é a economia do recurso entre lutas, não o Golpe Pesado.

### Limites das medidas anteriores

As tabelas de equilíbrio acima (1.211.0) são do simulador (`tests.equilibrio`): um robô (`tests/arena.py`) que escolhe
pela regra simples (a habilidade mais cara, área com 2+ inimigos, defesa quando ferido, o combo de fogo), com o kit
montado sozinho por papel (`kit.sugerido`), a comitiva jogada pelo robô (Odette cura, Morel interrompe, Yara amaldiçoa),
12 lutas comuns e 6 guardiões por nível, sem saída (então sem debandada), sem talentos escolhidos com intenção e com
equipamento sorteado. Mostram direção e tamanho, não o jogo de uma pessoa. Continuam provisórios, sem compensação neste
lote: a esquiva restaurada da Agilidade, o crítico da Sombra, o orçamento do kit (8 pontos) e o Necromante contra
guardiões.

### O gabarito na 1.212.0

Conferido contra a 1.211.0, partida por partida: as 12 de texto do Guerreiro, do Arqueiro e da comitiva saíram
**idênticas** (nenhuma debandada nem Queimadura em alvo resistente nelas); as 3 do Mago em texto mudam só na linha da
Queimadura do Grimório (impressa na tela de personagem); as 12 da tela mudam só no estado do herói mandado à tela (a
ordem nova das linhas da dica de atributo, o kit, o crítico e a Tenacidade, o resumo e o cálculo do Grimório), com o
mesmo número de linhas. Nenhuma jogada mudou.

### Proposta: gerenciamento da comitiva

No protótipo, separado do jogo: [ferramentas/prototipos/comitiva-gerenciamento](../ferramentas/prototipos/comitiva-gerenciamento/LEIA-ME.md)
(abas com retratos, a mesma janela para todos, a bolsa do grupo, o equipamento de cada um, a comparação com o
selecionado, as dependências reais e a regra proposta para os atributos dos companheiros). Aguarda avaliação.

## Andamento

- [x] Motor: ordem fixa, rodadas, Defender, comitiva controlada, kit, ultimate, atributos, Tenacidade
- [x] Repertório provisório das três classes (catálogo acima)
- [x] Interface: ordem na placa, roda de quem age, ultimate, kit no Grimório, atributos na ficha
- [x] Continuidade entre lutas, ritmo medido, saves (formato 7)
- [x] Escrita das regras revista (skill `texto-regras-fenda`)
- [x] Ajustes da 1.212.0: Queimadura, leitura, atributos e kit à vista, debandada
- [ ] Jean jogar; decidir o orçamento do kit e o dano do Necromante contra chefes
- [ ] Avaliar a proposta da comitiva (protótipo)
