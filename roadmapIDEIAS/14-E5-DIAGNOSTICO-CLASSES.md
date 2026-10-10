# 14 — E5: diagnóstico das três classes e das seis especializações

Revisão 1 — 10/10/2026. Jogo na versão 1.56.0 (commit `adaa93a`). **Entrega só de análise e design:** nenhum código,
atributo, habilidade, talento, item ou save foi alterado.

**Atualização 1.57.0:** a P1 foi implementada (seção 10). As seções 1 a 9 continuam como o diagnóstico da 1.56.0; onde
a 1.57 mudou o que elas dizem (o golpe preparado no Vale), a seção 10 diz o que vale agora.

**Atualização 1.58.0:** a P3 foi implementada (seção 11): a encruzilhada compara os dois caminhos e o Grimório explica
imunidades, a Marca, a Combustão e o caminho.

**Atualização 1.59.0:** a P2 começou por uma habilidade só, o Tiro Duplo do Patrulheiro (seção 12). Onde as seções 1 a 9
dizem que ele "nunca ganha do Tiro Certeiro", isso vale para a 1.58 e antes. Drenar Vida, Desaparecer e Passo Ágil não
mudaram.

**Avaliação sobre a 1.59.0 (só medida, nenhum código mudou):** Drenar Vida, Desaparecer e Passo Ágil em lutas inteiras
(seção 13). Drenar Vida e Desaparecer têm função; o Passo Ágil não, e a seção 13.5 recomenda a única mudança que mostrou
papel sem virar a ação de todo turno.

**Fechamento (sobre a 1.59.0, nenhum código mudou):** o desvio do Passo Ágil foi validado com outras sementes e **não**
foi incorporado. Usado repetidamente, ele vira a ação padrão contra inimigos sozinhos (seção 14). A E5 fica concluída
tecnicamente; a validação de Jean jogando fica registrada à parte.

**Cuidado ao ler as comparações de dano (seções 1, 4 e 9).** Somar o dano de sequências contra um alvo de treino não
demonstra que uma habilidade é inútil quando o valor dela é defesa, cura ou efeito sobre aliados. Erguer Escudo,
Barreira, Passo Ágil, Grito de Guerra (o enfraquecer), Marcar Presa (que vale para os golpes de todos) e Desaparecer
(a esquiva) só se medem no momento em que servem. A P1 mostrou isso com o golpe preparado (seção 10.4). Os "botões
dominados" da seção 4 continuam hipótese de design para a P2, que não está autorizada.

Legenda usada em todo o documento:

- **[código]** comportamento conferido no código (o arquivo vem citado);
- **[medido]** número calculado pelas próprias funções do jogo (método na seção 9);
- **[promessa]** o que uma descrição do jogo ou um documento promete e o sistema não faz (ou faz menos);
- **[hipótese]** leitura de design ainda não testada jogando nem medida;
- **[proposta]** mudança sugerida, **não aprovada**.

## 1. Resumo

1. **Para Guerreiro e Arqueiro, a melhor ação de quase todo turno é a mesma.** As lutas do Vale duram de 3 a 5
   turnos [medido], e Vigor e Foco não apertam: o Guerreiro regenera 6 por turno (+2 com o ataque básico) para um
   Golpe Pesado de 10; o Arqueiro, 5 (+2) para um Tiro Certeiro de 8 [código]. As ações de preparo (Grito de
   Guerra, Marcar Presa, Desaparecer) rendem **menos** que repetir o golpe principal numa luta de 3 turnos contra um
   alvo [medido]. O ataque básico quase nunca é a melhor escolha.
2. **O motor já tem momentos de decisão que o Vale não mostra.** O golpe preparado ("Defenda-se, ou atordoe
   para interromper!"), com as respostas de cada classe (Investida, Erguer Escudo, Lança de Gelo, Barreira, Passo
   Ágil, o urso), **não aparece em nenhuma luta do Vale**. Nos biomas do Vale, só o ent jovem prepara golpe, e ele pede
   região de nível 3; o Bosque é nível 2, e a noite sobe o nível dos inimigos, não as espécies [código:
   `sistemas/confronto.py`].
3. **O Mago é a única classe em que o recurso pesa:** mana regenera 3 por turno, só 20% volta depois da luta, e
   Meditar custa o turno [código]. É também a classe com a troca mais clara já no nível 1 (Lança de Gelo rende mais por
   mana; Bola de Fogo, mais por turno).
4. **Há botões dominados ou anulados na faixa 4–6:** Golpe Pesado no Paladino (o Golpe Sagrado tem a mesma média e
   cura); Tiro Duplo no Patrulheiro (menos dano que o Tiro Certeiro, mais Foco, duas flechas); Drenar Vida no
   Necromante (menos dano que a Bola de Fogo, e metade contra mortos-vivos); Desaparecer no Sombra (com o tiro seguinte,
   menos que dois tiros). O laço de acender e detonar do Piromante só supera repetir Bola de Fogo a partir do nível 6
   (Ignição) e em lutas de 4 turnos ou mais [medido].
5. **O Vale é dos mortos-vivos:** quatro das cinco lutas fixas da capela e a guardiã têm mortos-vivos [código]. Isso
   quase dobra o Golpe Sagrado (×1,7), anula o veneno do Sombra (imune) e corta pela metade o dano de sombra do Necromante.
6. **A liberdade de build hoje é pequena.** Cada especialização tem três talentos (4 a 5 pontos), e no nível 12 o herói
   tem pontos para quase toda a árvore (11 de nível, mais um por Sigilo, contra 15 a 16 no total) [código]. Escolher
   talento é escolher a ordem, não abrir mão. O equipamento só soma atributos; nenhum item único usa os modificadores e
   gatilhos que o sistema já aceita para itens [código]. As únicas exclusões reais são a especialização e o animal do
   Patrulheiro.
7. **A encruzilhada não explica a escolha.** No nível 4, no primeiro descanso, cada caminho aparece numa linha ("o
   Juramento da Luz (cura, poder sagrado)"), sem habilidades, sem passiva, sem custos (o Berserker perde 2 de Defesa) e
   sem dizer que Paladino, Patrulheiro e Sombra não têm passiva. A escolha é irreversível [código].
8. **No Vale (níveis 1 a 4) cabem as classes e as duas primeiras habilidades de cada especialização.** As habilidades de
   nível 7 (Julgamento, Fúria Cega, Fúria da Natureza, Execução, Fênix, Maldição) e os talentos de nível 6 e 9 ficam
   fora: só se avaliam por cenários direcionados.

**Recomendação (seção 8):** começar por dar ao Vale os momentos de decisão que o motor já tem: um golpe preparado em
duas lutas fixas da capela, com dados existentes, sem mexer em números de classe e sem mudar o gabarito. Depois, a
encruzilhada que explica (barata) e o papel de cada botão dominado (mexe no equilíbrio).

## 2. O que existe: sistemas conferidos

### 2.1 Recurso por classe [código, medido]

Sem talentos nem equipamento (`classes.py`, `balanceamento.py`, `combate/heroi.py`, `combate/luta.py`):

| Classe | Máximo (nv 3 / 5 / 8) | Regenera por turno | Ataque básico que acerta | Depois da luta | Ação principal |
|---|---|---|---|---|---|
| Guerreiro | 34 / 38 / 44 | 6 | +2 | +50% | Golpe Pesado, 10 |
| Arqueiro | 29 / 33 / 39 | 5 | +2 | +50% | Tiro Certeiro, 8 e uma flecha |
| Mago | 50 / 70 (Piromante), 60 (Necromante) / 85, 75 | 3 | +2 a +4 | +20% | Bola de Fogo, 14 |

- Guerreiro com Golpe Pesado todo turno gasta 4 por turno: de 38, aguenta uns 9 turnos. Luta típica: 3 a 5.
- Arqueiro com Tiro Certeiro todo turno gasta 3 por turno: uns 11 turnos. As **flechas** pesam entre lutas (20 no
  começo, 30 na aljava, 35% recolhidas depois da vitória, 1,4 de ouro cada no mercado); sem flecha, o ataque vira uma
  adaga corpo a corpo de 60%.
- Mago Piromante no nível 5 com Bola de Fogo todo turno gasta 11 por turno: umas 6 Bolas e depois Meditar (recupera
  6 + 12% do máximo e gasta o turno). Entre lutas, só 20% volta: o Tônico e o descanso viram parte do jogo.

### 2.2 O golpe [código: `combate/golpe.py`, `combate/eficacia.py`, `grimorio.py`]

- **Esquiva:** Agilidade × 1,2% (até 40%), mais buffs e clima (até 60%).
- **Crítico:** 5% + Agilidade × 1% + o extra da habilidade + talentos (até 60%); multiplica ×1,6, ou ×2,3 quando
  furtivo; Golpe Sombrio soma ao multiplicador.
- **Defesa:** dano × P / (P + Defesa × 6). P é 100 nos golpes do herói e cresce com o nível do inimigo nos golpes dele.
- **Traços que mudam escolhas:**

  | Traço | Efeito no dano |
  |---|---|
  | Voador | Corpo a corpo ×0,7; à distância ×1,25 |
  | Blindado | Físico ×0,75; o resto ×1,15 |
  | Morto-vivo | Sagrado ×1,7; sombra ×0,5; veneno 0 |
  | Etéreo | Físico ×0,75; arcano e sagrado ×1,3 |
  | Planta | Fogo ×1,5 |
  | Construto | Veneno 0; arcano ×1,2 |
  | Demônio | Sagrado ×1,5; fogo ×0,8 |
  | Corrompido | Sagrado ×1,4; sombra ×0,6 |

- O herói causa 90% do dano calculado (`DANO_HEROI`), com ±15% de sorteio. O Grimório mostra a média já com isso.

### 2.3 Estados [código: `estados.py`]

- **Em você ou nos aliados:**
  - guarda: dano recebido −x;
  - fortalecido, fúria, frenesi: cada um multiplica o dano, e eles se somam lado a lado;
  - esquiva;
  - barreira: absorve dano;
  - furtivo: o próximo golpe é crítico garantido;
  - provocando: os inimigos atacam quem provoca (chefes, metade das vezes);
  - firme: quem acabou de perder o turno não perde o seguinte.
- **Nos inimigos:**
  - veneno: não pega em mortos-vivos nem construtos;
  - sangramento: não pega em construtos nem etéreos;
  - queimadura: até 3 camadas; não pega em quem resiste muito ao fogo; a chuva enfraquece;
  - maldito: dano por turno e Defesa −40%;
  - atordoado: perde o turno; chefes e gigantes resistem metade das vezes; **interrompe um golpe preparado**;
  - enfraquecido: −25% de dano;
  - marcado: +x de dano **de todos**, inclusive comitiva e animal.

### 2.4 Talentos, modificadores e pontos [código: `talentos.py`, `modificadores.py`, `sistemas/progressao.py`]

- **Pontos:** um por nível (11 do 2 ao 12) e um por guardião derrotado (Sigilo). Camadas da árvore: níveis 2, 4, 6 e 9.
- **Total de pontos que cabem na árvore de cada classe:**

  | Classe | Base (nv 2) | Tronco (nv 4–6) | Especialização (nv 4, 6, 9) | Total |
  |---|---|---|---|---|
  | Guerreiro | 8 | 3 | Paladino 4, Berserker 4 | 15 |
  | Arqueiro | 8 | 3 | Patrulheiro 5, Sombra 5 | 16 |
  | Mago | 8 | 3 | Piromante 4, Necromante 4 | 15 |

  No nível 12, com um Sigilo, o herói tem 12 pontos: faltam 3 ou 4 para completar a árvore.
- **Tipos de talento:**
  - **Número:** Pele de Ferro, Golpe Brutal, Fôlego, Olho de Águia, Pés Leves, Aljava Funda, Mente Vasta, Potência
    Arcana, Canalização, Mira Firme, Eficiência, Laço Animal, Brasas Eternas, Pacto Sombrio, Luz Curativa, Sede
    Insaciável.
  - **Gatilho ou condição:** Contra-ataque, Aura de Proteção, Martírio, Imortal, Frenesi, Tiro de Abertura, Pontas
    Venenosas, Armadilheiro, Assassino, Coração Ardente, Rei dos Mortos.
  - **Muda uma habilidade em número:** Muralha, Escudo Rúnico, Ignição, Legião de Ossos, Golpe Sombrio, Matilha.
- **Nenhum talento muda alvo, passos ou comportamento de uma habilidade** (a transformação é a E6). As linhas da árvore
  são desenho, não pré-requisito.

### 2.5 Equipamento [código: `itens.py`]

- **Bases por classe:** arma e peças só da própria classe. Itens gerados somam atributos (arma: Ataque ou Poder; peças:
  Defesa, Vida, o atributo principal).
- **Afixos especiais**, que viram modificadores: roubo de vida, crítico, espinhos, vida por turno, vida por abate.
- **15 itens únicos, todos só com atributos e especiais.** `fonte_item` já aceita `mods`, `mults` e `gatilhos` declarados
  num único, no mesmo formato dos talentos; **nenhum único usa** isso.
- Na luta, trocar de arma gasta o turno, e só há armas da própria classe. Não existe "segunda arma com outro papel".

### 2.6 Inimigos que pedem decisão [código: `inimigos.py`, `dados.py`, `combate/turnos.py`]

| Comportamento | O que pede do jogador | Quem tem |
|---|---|---|
| **Golpe Esmagador** (prepara um turno, ×2,2, com aviso) | Atordoar para interromper, ou se proteger (guarda, barreira, esquiva) | Ent jovem (nv 3+), troll, mercenário, golem, cavaleiro sombrio, abominação; guardiões troll e dragão |
| Cura (o mais ferido, a cada 3 turnos) | Matar o curandeiro primeiro | Cultista, bruxa do brejo (nv 2+) |
| Uivo ou grito de guerra (+30% nos aliados dele) | Prioridade de alvo | Lobo, lobo gélido, mercenário |
| Reviver | Prioridade de alvo | Xamã caído |
| Roubar e fugir com o ouro | Matar o ladrão antes | Bandido |
| Teia, agarrão (perde o turno) | Prevenção (matar, se proteger) | Aranha, afogado, sapo |

**No Vale:**

- **Charco** (pântano, nível 1): afogado, sapo, sanguessuga, bandido, carniçal; à noite, também o espectro. A bruxa do
  brejo (nv 2+) não aparece: a espécie depende do nível da região, e a noite só sobe o nível dos inimigos
  (`sistemas/confronto.py`).
- **Bosque** (floresta, nível 2): lobo, aranha, bandido, javali, caído (demônio). O ent jovem (nv 3+) não aparece.
- **Capela, lutas fixas** (`missoes.py`):
  - afogado e duas sanguessugas;
  - dois cultistas;
  - dois esqueletos;
  - dois afogados no sarilho;
  - a guardiã: morta-viva, conjuradora, invoca afogados.
- **Capela, encontros ao acaso** (ruínas, nível 3): esqueleto, cultista, rato, carniçal; espectro (nv 3) e, à noite,
  mais espectros.
- Fora o bando de cultistas, que pede matar quem cura, **o golpe preparado, a decisão defensiva mais clara do motor, não
  aparece em nenhuma luta do Vale.**

### 2.7 Especialização [código: `classes.py`, `talentos.py`, `eventos/classe.py`, `sistemas/progressao.py`]

- Chega no nível 4, na primeira noite de descanso; é irreversível; vem com bônus fixos de atributo, duas habilidades no
  nível 4 e uma no 7.
- **Passiva:** só Berserker (Pacto de Sangue), Piromante (Chama Viva) e Necromante (Colheita) têm.
  - O Paladino tem resistência ao grito de terror (60%) e bônus em testes, mas como `mods` da especialização, que não
    aparecem no Grimório.
  - O Patrulheiro tem o animal, escolhido uma vez, sem troca.
  - O Sombra não tem nada além de atributos.
- **A escolha:** uma linha por caminho no menu do evento. Depois, a festa "você agora é" mostra as habilidades novas. A
  árvore de talentos já mostra os dois ramos antes do nível 4 ("especialização no nível 4"), mas a encruzilhada não
  aponta para ela.

### 2.8 Duração das lutas [medido]

Cada especialização no nível 5 (talentos ao acaso, equipamento sorteado no nível, sem comitiva) contra duplas de
nível 3 do próprio Vale, 40 lutas por linha, robô de `tests/arena.py`:

| Especialização | Mortos-vivos (afogado + carniçal): turnos, vida perdida | Vivos (lobo + bandido): turnos, vida perdida |
|---|---|---|
| Paladino | 4,1 · 4% | 4,5 · 5% |
| Berserker | 3,9 · 13% | 3,0 · 7% |
| Patrulheiro | 3,9 · 15% | 3,0 · 6% |
| Sombra | **7,6 · 32%** | 4,3 · 15% |
| Piromante | 6,5 · 35% | 4,8 · 18% |
| Necromante | 5,1 · 17% | 3,8 · 7% |

Vitórias: 98% a 100% em todas as linhas: **a taxa de vitória não separa nada aqui**. O que se lê:

- as lutas duram de 3 a 5 turnos;
- contra mortos-vivos, o Sombra leva o dobro de turnos;
- o Paladino perde quase nada.

O Piromante sai mal, mas o robô joga Inferno com dois inimigos e nunca detona (seção 9). Esse número diz mais do robô
que da especialização.

## 3. Promessas × código

| Onde | Promete | O que o código faz |
|---|---|---|
| Patrulheiro (descrição) | "domina armadilhas" | Um talento de nível 6 (Armadilheiro): um inimigo começa preso e sangrando. Nenhuma armadilha como ação [promessa] |
| 03-CLASSES | Arqueiro com "posicionamento narrado" | O combate não tem posição nem distância; alcance é só o tipo do golpe [promessa] |
| Sombra (descrição) | "Furtividade" | Furtivo = o próximo golpe é crítico garantido (×2,3), por até 3 turnos; Desaparecer dá também esquiva +50% por 1 turno. Os inimigos continuam mirando você normalmente [código] |
| Desaparecer | "Próximo ataque é crítico devastador" | É, mas o turno gasto pesa: Desaparecer e Tiro Certeiro rendem 56; dois Tiros Certeiros, 65 (nível 5) [medido] |
| Combustão (Grimório) | "Detonando 3 camadas novas: média 92" (Piromante 5) | Mostra o melhor caso, que pede três Bolas acesas e a detonação logo em seguida. Nas lutas de 3 a 5 turnos o comum é 1 ou 2 camadas, com 1 ou 2 turnos restantes, e o Grimório não mostra esse caso [código, medido] |
| Piromante (descrição) | "explosões em cadeia" | Coração Ardente, talento de nível 9 [código] |
| Necromante (descrição) | "amaldiçoa" | Maldição, só no nível 7 [código] |
| Erguer Servo | "atrai os golpes" | Só enquanto provoca (2 turnos); depois, os inimigos atacam algum aliado em 25% das vezes, como qualquer aliado [código] |
| Tiro Duplo | "Dois disparos de 90%" | Correto; cada disparo usa a chance de crítico comum (o Tiro Certeiro tem +30%). Não há situação em que renda mais que o Tiro Certeiro [medido] |
| Paladino | resistência ao terror | Existe (60%), mas invisível: não aparece no Grimório nem na escolha [código] |
| Flecha Envenenada, Pontas Venenosas (Grimório) | veneno por turno | O texto não diz que veneno não pega em mortos-vivos nem construtos; a luta diz "não é afetado" na hora [código] |
| 04-HABILIDADES | "Combustão já é exemplo de consumo de efeito" | É, mas só se paga a partir do nível 6 com Ignição e em lutas de 4 turnos ou mais (seção 4, Piromante) [medido] |

O resto das descrições confere com a execução: os números do Grimório saem dos mesmos blocos que o combate usa
(`habilidades.py`).

## 4. Fichas

Os números de dano são médias do Grimório (sem crítico, já com os 90%) ou somas medidas num alvo de treino com Defesa 3
e sem esquiva (seção 9), sem talentos nem equipamento. Servem para comparar opções entre si, não como dano real numa luta.

### 4.1 Guerreiro (níveis 1 a 3)

- **Fantasia e estilo:** muita vida e defesa, corpo a corpo, aguenta o tranco. No nível 3: vida 78, Ataque 15,
  Defesa 8.
- **Decisões recorrentes:**
  - Golpe Pesado: 170%, média 22, custa 10;
  - Investida: 120%, média 16, 45% de atordoar, custa 12;
  - Erguer Escudo: −50% de dano por 2 turnos, custa 8;
  - Grito de Guerra: +30% de dano por 3 turnos e 80% de enfraquecer cada inimigo por 2 turnos, custa 14.
- **Recurso:** não aperta (seção 2.1). O ataque básico (100%) nunca vale mais que o Golpe Pesado (170%) por 10 de Vigor
  que volta no turno seguinte.
- **Forças:** vida, defesa, o Escudo.
- **Fraquezas e situações ruins:**
  - voadores (corpo a corpo ×0,7);
  - etéreos e blindados (físico ×0,75);
  - sem nenhum ataque à distância;
  - sem cura própria antes do Paladino.
- **Identidade:** Golpe Pesado e Erguer Escudo. Os talentos de base são números (Pele de Ferro, Golpe Brutal, Fôlego).
- **Equipamento:** arma dá Ataque; escudo dá Defesa e Vida; espinhos combinam com Escudo e Contra-ataque (tronco, nv 4).
- **Fora do combate:**
  - Força: soltar a Yara na fogueira; o sarilho da capela, sem a luta dos afogados;
  - eventos de classe: duelo de honra, queda de braço, veterano, ferreiro itinerante;
  - leituras próprias da Fonte, do canal e da sacristia.
- **Sequência concreta** (nível 3, lobo + bandido):
  1. Golpe Pesado no bandido (que rouba e foge).
  2. Golpe Pesado de novo.
  3. Golpe Pesado no lobo.

  O Vigor vai de 34 a uns 22 e nunca falta.
- **Quando seria melhor outra ação:**
  - Se o lobo uivou (+30% nos aliados dele), matá-lo primeiro.
  - Se um inimigo prepara o Golpe Esmagador (fora do Vale: troll, mercenário, golem): Investida (45% de interromper e
    ainda bate) ou Escudo (−50% certo).
  - Grito de Guerra no primeiro turno só compensa com três ou mais inimigos, ou luta longa. Contra um alvo, Grito e dois
    Golpes Pesados somam 51; três Golpes Pesados, 58 [medido]. O enfraquecer, que é defesa, não entra nessa conta.
- **Dominância:** o Golpe Pesado é a ação de quase todo turno. As respostas (Investida, Escudo) existem, mas o Vale não
  cria o momento delas (seção 2.6).

### 4.2 Paladino (Guerreiro, a partir do nível 4)

- **Fantasia e estilo:** o Juramento da Luz; cura a si mesmo e fere mortos-vivos, corrompidos e demônios. No nível 5:
  vida 113, Ataque 19, Poder 10, Defesa 14.
- **Decisões:**
  - Golpe Sagrado: 130% do Ataque + 80% do Poder, sagrado, cura 20% do dano;
  - Prece: cura 25% da vida + Poder (38 no nv 5) e tira veneno, sangramento, maldição e fraqueza;
  - Erguer Escudo;
  - no nível 7, Julgamento Divino: em todos os inimigos, sagrado, sem esquiva.
- **Recurso:** o Vigor continua sobrando (Golpe Sagrado 15, Prece 20).
- **Forças:** o Vale inteiro. O Golpe Sagrado contra morto-vivo soma 42; o Golpe Pesado, 25 [medido]. A Prece limpa a
  maldição e o dreno dos afogados e da bruxa. Defesa alta.
- **Fraquezas:**
  - nenhum dano em grupo antes do 7;
  - nada contra voadores;
  - sem passiva visível.
- **Identidade:** Golpe Sagrado, Prece. Talentos: Luz Curativa (+25% de cura por ponto), Aura de Proteção (começa a luta
  com barreira de 1,5 × Poder), Martírio (uma vez por luta, abaixo de 25% de vida, cura 40%). Tronco: Contra-ataque,
  Muralha.
- **Equipamento:** Égide do Mártir e Pele do Penitente (a recompensa de Destruir a guardiã), com espinhos.
- **Fora do combate:**
  - Carisma +2: a denúncia de Caspar;
  - Vontade +3;
  - resistência ao terror;
  - eventos: aldeia assombrada, os enfermos, a tentação do juramento.
- **Sequência** (nível 5, dois esqueletos do ossuário):
  1. Golpe Sagrado no primeiro esqueleto.
  2. Golpe Sagrado de novo; ele cai.
  3. e 4. O mesmo no segundo.

  Prece só abaixo de metade da vida ou com maldição.
- **Quando outra ação:** Escudo diante de golpe preparado; Prece quando a vida e os males pedem; Julgamento (nv 7) com
  dois ou mais inimigos.
- **Dominância:** **o Golpe Pesado fica obsoleto.** Média 29 nos dois no nível 5 (25 = 25 medido no alvo de treino), e o
  Golpe Sagrado ainda cura e quase dobra contra o que o Vale tem. O botão continua no menu sem situação própria.

### 4.3 Berserker (Guerreiro, a partir do nível 4)

- **Fantasia e estilo:** o Pacto de Sangue; quanto mais ferido, mais forte. No nível 5: vida 106, Ataque 25,
  Defesa 9 (−2 da especialização).
- **Decisões:**
  - Sede de Sangue: 140%, rouba 40% do dano e abre sangramento;
  - Redemoinho: 110% em cada inimigo, custa 22;
  - Golpe Pesado;
  - no nível 7, Fúria Cega: custa 15% da vida e nenhum Vigor; +60% de dano por 3 turnos e ataca com 130%.
- **Recurso de verdade:** a **vida**.
  - Pacto de Sangue: até +60% de dano, proporcional à vida perdida.
  - A decisão é ficar ferido para bater mais ou se curar pelo roubo.
- **Forças:** sustentação (roubo), dano em grupo (Redemoinho), crescimento com a vida perdida.
- **Fraquezas:**
  - Defesa menor;
  - risco quando a vida já está baixa;
  - sangramento não pega em construtos nem etéreos.
- **Identidade:** Sede de Sangue, Redemoinho, Fúria Cega. Talentos: Sede Insaciável (5% de todo dano volta como vida, por
  ponto), Frenesi (cada abate +10% de dano por ponto, até três vezes), Imortal (uma vez por luta, sobrevive a um golpe
  fatal com 1 de vida e entra em fúria).
- **Equipamento:** roubo de vida e vida por abate (Lamento de Gharbad), crítico (O Açougueiro).
- **Fora do combate:** o chamado do sangue, a fúria noturna.
- **Sequência** (nível 5, lobo + bandido + javali):
  1. Redemoinho nos três.
  2. Sede de Sangue no mais ferido.
  3. Sede de Sangue de novo, ou Golpe Pesado para acabar.

  Com Frenesi, a ordem dos abates importa: matar o mais fraco primeiro rende carga.
- **Quando outra ação:**
  - Golpe Pesado quando o alvo vai cair de qualquer jeito (o sangramento se perde);
  - Escudo diante de golpe preparado, se a vida está baixa demais para o Pacto valer o risco.
- **Dominância:**
  - Sede de Sangue × 3 = 101 contra Golpe Pesado × 3 = 98 [medido]; a Sede ainda rouba vida. Domina o Golpe Pesado,
    menos contra construtos e etéreos.
  - [hipótese, medir no nv 7–9] A Fúria Cega, de custo zero em Vigor e paga com vida que o roubo devolve, pode virar a
    abertura de toda luta.

### 4.4 Arqueiro (níveis 1 a 3)

- **Fantasia e estilo:** ágil e preciso, à distância; gasta flechas. No nível 3: vida 68, Ataque 13, Agilidade 11.
- **Decisões:**
  - Tiro Certeiro: 170% com +30% de crítico, média 19, crítico em 46% dos tiros;
  - Marcar Presa: o alvo recebe +25% de dano **de todos** por 3 turnos, custa 6;
  - Chuva de Flechas: 100% em cada inimigo, uma flecha por inimigo, custa 20;
  - Passo Ágil: esquiva +30% por 2 turnos.
- **Recurso:** o Foco não aperta; as flechas pesam entre lutas (seção 2.1).
- **Forças:** voadores (×1,25 à distância); crítico alto; esquiva.
- **Fraquezas:**
  - menos vida e defesa que o Guerreiro;
  - blindados e etéreos (físico);
  - sem flecha, vira adaga de 60%.
- **Identidade:** Tiro Certeiro, as flechas. Talentos de base: Olho de Águia, Pés Leves, Aljava Funda.
- **Equipamento:** arma dá Ataque e Agilidade; aljava; crítico (Ventre da Tempestade, Aljava dos Mil Corvos).
- **Fora do combate:**
  - Percepção +3;
  - eventos: rastro de caça, madeira para flechas, competição de tiro, corda encharcada na chuva, falcão mensageiro;
  - o sarilho por Destreza (gasta uma flecha);
  - leituras próprias da Fonte e do canal.
- **Sequência** (nível 3, uma harpia, voadora):
  1. Tiro Certeiro.
  2. Tiro Certeiro.
  3. Tiro Certeiro.

  O Guerreiro bateria com 70% nela.
- **Quando outra ação:**
  - Marcar Presa no primeiro turno só compensa com mais gente batendo no mesmo alvo (comitiva, animal) ou com luta
    longa. Sozinho, contra um alvo em 3 turnos: Marcar e dois tiros somam 51; três tiros, 61 [medido].
  - Chuva de Flechas com três ou mais inimigos.
  - Passo Ágil diante de golpe preparado (o golpe pode ser esquivado).
- **Dominância:** o Tiro Certeiro é a ação de quase todo turno.

### 4.5 Patrulheiro (Arqueiro, a partir do nível 4)

- **Fantasia e estilo:** guardião das matas, luta ao lado de um animal. No nível 5: vida 96, Ataque 19, Defesa 10.
- **O animal age sozinho todo turno:**
  - o lobo pode abrir sangramento (30%);
  - o urso pode atordoar (15%); com ele no grupo, os inimigos miram algum aliado 45% das vezes, contra 25% sem ele;
  - o falcão tem crítico 25% e ataca à distância.
- **Decisões:**
  - Ordem da Fera, que muda com o animal:
    - urso, "Proteger!": 100% e provoca por 2 turnos, recebendo 30% menos;
    - lobo, "Dilacerar!": 160% e sangramento forte por 4 turnos;
    - falcão, "Os olhos!": 100% sem esquiva e enfraquece por 2 turnos.
  - Tiro Duplo;
  - no nível 7, Fúria da Natureza: 130% em todos, sangramento e cura o animal.
- **Recurso:** Foco sobrando; o animal ferido fica fora até o descanso.
- **Forças:** dois atacantes por turno; o urso protege; Marcar Presa rende mais (o animal também bate no marcado).
- **Fraquezas:**
  - o animal frágil (o falcão);
  - Tiro Duplo sem papel.
- **Identidade:** o animal e a Ordem da Fera. Talentos: Laço Animal (+20% de vida e ataque do animal por ponto),
  Armadilheiro (nv 6), Matilha (nv 9: o animal ataca duas vezes).
- **Fora do combate:** Percepção +2; o companheiro fareja; o círculo dos druidas.
- **Sequência** (nível 5, urso, contra um troll; fora do Vale):
  1. Marcar Presa.
  2. O troll prepara o Golpe Esmagador: Ordem da Fera, e o urso provoca e recebe menos.
  3. Tiro Certeiro.
  4. Tiro Certeiro.
- **Quando outra ação:**
  - com lobo, a Ordem num alvo de muita vida (o sangramento forte precisa de turnos);
  - com falcão, a Ordem em quem bate mais forte.
- **Dominância:** **Tiro Duplo nunca ganha do Tiro Certeiro.** Soma 27 contra 30 no nível 5 [medido], custa 10 de Foco
  contra 8, e duas flechas contra uma.

### 4.6 Sombra (Arqueiro, a partir do nível 4)

- **Fantasia e estilo:** furtividade, venenos e execuções. No nível 5: vida 94, Ataque 20, Agilidade 19 (crítico 24% de
  base).
- **Decisões:**
  - Desaparecer: o próximo golpe é crítico ×2,3, e esquiva +50% por 1 turno;
  - Flecha Envenenada: 100% e veneno de 12,8 por turno durante 4 turnos;
  - no nível 7, Execução: 120%, ou 320% com o alvo abaixo de 35% de vida, com +20% de crítico.
- **Recurso:** Foco sobrando. Assassino (nv 9) devolve metade dele por abate.
- **Forças:** contra vivos e lutas longas, a Flecha Envenenada. Em 4 turnos, Flecha Envenenada e três Tiros Certeiros
  somam 160; quatro Tiros Certeiros, 131 [medido]. Crítico alto.
- **Fraquezas:**
  - **o Vale.** Contra mortos-vivos a mesma sequência soma 115, abaixo dos 131 de só atirar [medido], e as lutas
    duram o dobro (seção 2.8);
  - construtos;
  - nenhuma passiva;
  - o laço que dá nome à especialização só fecha no nível 9.
- **Identidade:** Desaparecer, Flecha Envenenada, Execução. Talentos: Pontas Venenosas (o ataque básico envenena 20% das
  vezes por ponto), Golpe Sombrio (+20% no multiplicador do crítico por ponto), Assassino (abate: metade do Foco e
  furtivo).
- **Fora do combate:** contrato da Irmandade, bolsos alheios.
- **Sequência** (nível 8, um carniçal ferido e um bandido):
  1. Desaparecer.
  2. Execução no carniçal, já abaixo de 35%: 320%, crítico ×2,3. Com Assassino (nv 9), o abate devolve Foco e furtivo.
  3. Execução ou Tiro Certeiro no bandido.
- **Quando outra ação:**
  - contra vivos com muita vida, Flecha Envenenada primeiro;
  - contra mortos-vivos, só Tiro Certeiro.
- **Dominância:** no nível 4–6, **Desaparecer não se paga em dano**. Desaparecer e Tiro Certeiro somam 56; dois Tiros
  Certeiros, 65 [medido]. Vale como defesa, pela esquiva de um turno. [hipótese] Pontas Venenosas é o único talento que
  torna o ataque básico uma opção real, e de novo não contra mortos-vivos.

### 4.7 Mago (níveis 1 a 3)

- **Fantasia e estilo:** frágil e devastador; explora fraquezas. No nível 3: vida 58, Poder 17, Defesa 5, mana 50.
- **Decisões:**
  - Bola de Fogo: 150% fogo, média 22, 60% de acender, custa 14;
  - Lança de Gelo: 130% gelo, média 19, 35% de congelar (interrompe golpe preparado), custa 10;
  - Barreira Arcana: absorve 20% da vida + 60% do Poder, 2 turnos, custa 20;
  - Meditar.
- **Recurso:** **pesa** (seção 2.1).
  - Lança de Gelo rende mais por mana (1,9 de dano por ponto contra 1,6 da Bola).
  - Bola de Fogo rende mais por turno.
  - O ataque básico (Dardo Arcano, 100%) devolve mana e às vezes é a escolha certa.
- **Forças:** escolhe o elemento (planta e ent: fogo ×1,5; etéreo e construto: arcano); à distância.
- **Fraquezas:** vida e defesa baixas; mana que não volta entre lutas.
- **Identidade:** as três magias e Meditar. Talentos de base: Mente Vasta, Potência Arcana, Canalização.
- **Equipamento:** Poder, mana (Tomo), roubo (Tomo do Nome Esquecido).
- **Fora do combate:**
  - Vontade +2;
  - Arcano: assustar a turba da fogueira, o sarilho;
  - a análise do lodo (prova forte contra Caspar);
  - eventos: anomalia arcana, linha ley, grimório perdido, aprendiz em apuros.
- **Sequência** (nível 3, lobo + bandido, mana 50):
  1. Bola de Fogo no bandido.
  2. Lança de Gelo no lobo (mais barata).
  3. Bola de Fogo no que sobrou.

  Se a próxima luta vem logo, terminar com o Dardo, que devolve mana.
- **Quando outra ação:** Barreira quando dois inimigos batem em você; Meditar abaixo de um terço da mana, se a luta já está
  ganha.
- **Dominância:** nenhuma clara. **É a classe com mais decisões por turno hoje.**

### 4.8 Piromante (Mago, a partir do nível 4)

- **Fantasia e estilo:** a Chama Viva, com queimaduras +25%. No nível 5: Poder 26, mana 70.
- **Decisões:**
  - Bola de Fogo;
  - Combustão: detona as chamas, e o que ainda arderia vira dano, mais forte com camadas;
  - Inferno: 60% em todos, média 14 em cada, 50% de acender, custa 35;
  - no nível 7, Fênix: 250% e cura 20% da vida.
- **Recurso:** mana pesa. A Combustão custa o mesmo que a Bola (14).
- **O laço acender e detonar** [medido]:

  | Nível | Sequência | Dano somado |
  |---|---|---|
  | 5, sem Ignição | Bola, Bola, Combustão | 96 |
  | 5, sem Ignição | Bola × 3 | 102 |
  | 6, com Ignição (a Bola sempre acende) | Bola, Bola, Combustão (3 turnos) | 127 |
  | 6, com Ignição | Bola × 3 | 125 |
  | 6, com Ignição | Bola × 3 e Combustão (4 turnos) | **194** |
  | 6, com Ignição | Bola × 4 | 172 |

  **O laço só se paga a partir do nível 6 e em lutas de 4 turnos ou mais**: chefes, alvos de muita vida.
- **Forças:**
  - plantas e ent (fogo ×1,5);
  - lutas longas;
  - grupos com o Inferno, na hipótese de três ou mais inimigos [hipótese].
- **Fraquezas:**
  - quem resiste muito ao fogo é imune à queimadura (o cão infernal);
  - chuva enfraquece as chamas;
  - frágil.
- **Identidade:** Combustão. Talentos: Brasas Eternas (queimadura +20% por ponto e um turno a mais), Ignição (nv 6),
  Coração Ardente (nv 9: quem morre pelo fogo explode).
- **Fora do combate:** elemental selvagem, incêndio.
- **Sequência** (nível 6, Ignição, a guardiã):
  1. Bola.
  2. Bola.
  3. Bola.
  4. Combustão com três camadas.
  5. Meditar, se a mana pede.
  6. Recomeçar.
- **Quando outra ação:**
  - Lança de Gelo, mais barata, para economizar mana;
  - Barreira quando ela invoca afogados;
  - Inferno só com três ou mais inimigos.
- **Dominância:**
  - Antes do 6, repetir Bola de Fogo é sempre igual ou melhor que preparar a Combustão.
  - O Grimório anuncia a Combustão pelo melhor caso (92 no nível 5), que a luta comum quase nunca alcança.

### 4.9 Necromante (Mago, a partir do nível 4)

- **Fantasia e estilo:** o Sussurro do Túmulo; drena vida, amaldiçoa e ergue servos. No nível 5: vida 88, Poder 24,
  mana 60.
- **Colheita:** cada inimigo que cai devolve 5 de mana.
- **Decisões:**
  - Drenar Vida: 120% sombra, rouba 40%, média 25;
  - Erguer Servo: 36 de vida, provoca 2 turnos, máximo 1 servo; custa 22;
  - no nível 7, Maldição: em todos, 40% do Poder por turno durante 4 turnos, Defesa −40%; custa 18.
- **Recurso:** mana pesa, aliviada pela Colheita em grupos.
- **Forças:**
  - o servo segura os golpes nos primeiros turnos;
  - sustentação pelo dreno;
  - a Maldição (nv 7), que não erra e tira Defesa para todos os golpes, da comitiva também.
- **Fraquezas:**
  - **o Vale:** Drenar Vida contra morto-vivo soma 11 [medido];
  - corrompidos (sombra ×0,6);
  - até o nível 7, a melhor magia de dano continua sendo a Bola de Fogo da classe: 29 contra 22 do Drenar Vida [medido].
- **Identidade:** Erguer Servo, Drenar Vida, Maldição. Talentos: Pacto Sombrio (Drenar Vida cura +10% e servos +15% de
  vida, por ponto), Legião de Ossos (nv 6, um servo a mais), Rei dos Mortos (nv 9: o primeiro inimigo a cair levanta
  como servo).
- **Fora do combate:** cemitério antigo, aldeões temerosos.
- **Sequência** (nível 5, dois afogados):
  1. Erguer Servo; os afogados batem nele.
  2. Bola de Fogo.
  3. Bola de Fogo.
  4. Drenar Vida só se a vida pede (contra morto-vivo, metade).
- **Quando outra ação:** Drenar Vida contra vivos quando a vida está baixa; Barreira se o servo caiu.
- **Dominância:**
  - No 4–6, a especialização se sente pelo servo; o dreno perde para a Bola de Fogo.
  - [hipótese, medir no nv 7–9] A Maldição, barata, sem esquiva e em todos, pode virar a primeira ação de toda luta.

## 5. Liberdade de build

| Especialização | Configuração A | Configuração B | Já é possível? | Muda decisões? |
|---|---|---|---|---|
| Paladino | **Bastião:** Muralha, Contra-ataque, Aura, Martírio; espinhos (Égide, Pele do Penitente). O Escudo vira ataque: segurar o golpe e revidar | **Cruzado:** Golpe Brutal, Luz Curativa; Golpe Sagrado todo turno | Sim, as duas | Pouco. O Contra-ataque é 15 a 30% de 70%. Na prática, o Golpe Sagrado continua sendo a ação de todo turno nas duas |
| Berserker | **Sangue:** Sede Insaciável, roubo de vida, Imortal; ficar ferido para o Pacto e não se curar | **Matança:** Frenesi, Redemoinho, vida por abate; a ordem dos abates importa | Sim, as duas | **Sim:** A pede administrar a própria vida; B, escolher quem matar primeiro. É o melhor caso atual |
| Patrulheiro | **Guardião:** urso; a Ordem protege; você atira com calma | **Caçador:** lobo ou falcão; a Ordem é dano ou fraqueza | Sim. **Exclusiva e irreversível** (o animal) | **Sim:** a Ordem da Fera muda de papel |
| Sombra | **Veneno:** Pontas Venenosas, Flecha Envenenada; desgaste, o básico envenena | **Execução:** Golpe Sombrio, Desaparecer, Execução, Assassino | A no 4–6, anulada contra mortos-vivos. **B só no 7 a 9** | Sim, quando existe: A pede manter o alvo vivo e envenenado; B, esperar o limiar de 35% |
| Piromante | **Detonação:** Ignição, Brasas; acender e detonar | **Área:** Inferno, Coração Ardente | A a partir do 6; B a partir do 9 | Sim, mas o que decide é o encontro (um alvo × grupo), não a build. No 12, as duas se juntam |
| Necromante | **Ossos:** Legião, Pacto (servos), Rei dos Mortos; os servos seguram, você conjura | **Dreno:** Pacto (dreno), Escudo Rúnico, Eficiência; sustentação pelo Drenar Vida | A parcial no 6, completa no 9. B é só número | A muda decisões (manter servos de pé); B não |

**Leitura geral [código]:**

- **Os pontos convergem.** No 12, cada herói tem quase toda a árvore. As configurações diferem pela **ordem** de compra
  e pelo **equipamento**, não por abrir mão de algo.
- **O equipamento não cria configuração.** Atributos e cinco afixos especiais; nenhum único com efeito próprio.
- **Exclusões reais:** só a especialização e o animal do Patrulheiro.

**O que exigiria conteúdo novo [proposta, não para agora]:**

- escolhas exclusivas na árvore (dois talentos de uma camada, um só);
- únicos com gatilhos;
- habilidade efetiva por transformação (E6).

## 6. Progressão e apresentação

### 6.1 As três faixas

| Faixa | No Vale? | O que se experimenta | Onde avaliar o resto |
|---|---|---|---|
| 1 a 3 | Sim (Charco 1–2, Bosque 2–3) | As classes; talentos de base (números) | Jogando |
| 4 a 6 | Em parte. Capela 3–4, guardiã 4; a especialização no primeiro descanso depois do 4 | Duas habilidades da especialização; talentos da camada 2 (nv 4). A camada 3 (nv 6: Ignição, Legião, Armadilheiro, Aura, Frenesi, Golpe Sombrio) só se o herói passar do 5 | Jogando, até o 5; cenários direcionados |
| 7 a 11 | Não | Habilidades de nível 7; talentos de nível 9 (Martírio, Imortal, Matilha, Assassino, Coração Ardente, Rei dos Mortos) | Cenários direcionados: `tests/navegador/cenarios.py capela` (CLASSE, NIVEL), `tests.equilibrio --spec`, `tests/arena.py` |

### 6.2 Perguntas da entrega

- **A especialização muda perceptivelmente o modo de jogar?**
  - Sim: Berserker (a vida como recurso), Patrulheiro (o animal no turno), Necromante (o servo).
  - Pouco no 4–6: Paladino (o Golpe Sagrado troca o Golpe Pesado), Piromante (o laço só no 6), Sombra (o Vale anula o
    veneno).
- **A escolha explica vantagens e custos?** Não.
  - Uma linha por caminho.
  - Sem habilidades, sem passiva (nem a falta dela), sem bônus nem custos de atributo, sem forte e fraco contra.
  - A informação existe no jogo (catálogo, Grimório, árvore), mas não na hora da escolha.
- **O jogador entende efeitos, sinergias e limitações?**
  - Em parte. O Grimório mostra números reais e de onde vêm (bom).
  - Faltam:
    - imunidades (veneno contra mortos-vivos e construtos);
    - o caso comum da Combustão;
    - que a Marca vale para os golpes de todos;
    - a passiva invisível do Paladino.
- **Talentos e equipamento oferecem alternativas compreensíveis?**
  - Os talentos são claros, mas quase todos numéricos e todos alcançáveis.
  - O equipamento compara bem (atributos), mas não oferece alternativa de jogo.
- **Barreiras desnecessárias para experimentar:**
  - especialização, animal e pontos são irreversíveis;
  - a especialização só chega no descanso;
  - o 7–11 pede uma campanha longa ou cenário de teste.

  A preparação de habilidades e a reespecialização continuam propostas (03 e 04); nada disso entra agora.

## 7. Prioridades para a E5

### P1. Momentos de decisão no Vale, com o que o motor já tem — **recomendada primeiro**

- **Problema concreto:**
  - Guerreiro e Arqueiro repetem a mesma ação quase todo turno (seção 1).
  - As respostas que cada classe tem (Investida, Erguer Escudo, Lança de Gelo, Barreira, Passo Ágil, a Ordem do urso,
    Desaparecer) quase nunca têm o seu momento: o golpe preparado não aparece em nenhuma luta do Vale (seção 2.6).
- **Comportamento desejado:**
  - Duas lutas fixas da capela têm um inimigo que prepara o Golpe Esmagador existente, com o aviso existente.
  - O jogador vê o golpe vindo e escolhe como responder.
  - O bando de cultistas, que já cura, continua sendo a luta de "quem matar primeiro".
- **Exemplo de decisão que passaria a existir** (no ossuário, um esqueleto prepara o golpe):
  - **Guerreiro:** Investida (45% de interromper, e ainda bate) ou Escudo (−50%, certo).
  - **Arqueiro:** Passo Ágil (esquiva), a Ordem do urso (Patrulheiro) ou tentar matar antes.
  - **Mago:** Lança de Gelo (35%, barata) ou Barreira (absorve, cara).
  - Em todos, a escolha depende da vida de agora e da chance.
- **Estruturas reaproveitadas:**
  - `inimigos.py`: a habilidade `esmagar`, `carregando`, o aviso;
  - `combate/turnos.py`: atordoar interrompe;
  - `estados.py`: firme, guarda, barreira, esquiva;
  - `missoes.py`: as lutas fixas (`g.grupo` nas salas);
  - a ficha da luta e o bestiário, que já listam as habilidades do inimigo.
- **Custo:** baixo, dados da campanha nas cenas da capela.
  - Hoje o inimigo escolhe a habilidade ao acaso (35% por turno). Se for preciso que o golpe apareça com certeza na luta
    que ensina, entra um gancho pequeno ("abre com o golpe preparado"), só se a medição mostrar que ele não aparece.
- **Risco:** a capela fica mais dura (um golpe de ×2,2). Mede-se nas três classes no nível 3–4 antes e depois. O gabarito
  não muda (a campanha não está nele).
- **Como verificar:**
  - teste unitário: a luta fixa traz o inimigo que prepara; atordoar interrompe; a guarda reduz;
  - cenário de navegador da capela com captura do aviso;
  - `tests/arena.py` nas lutas da capela por classe (vitória e vida perdida, antes e depois);
  - Jean jogando as três classes e dizendo se o momento aparece e se a escolha pesa.

### P2. Um papel para cada botão dominado (faixa 4–6)

- **Problema concreto:**
  - Golpe Pesado no Paladino;
  - Tiro Duplo no Patrulheiro;
  - Drenar Vida no Necromante;
  - Desaparecer no Sombra (seção 4).

  Cada um ocupa o menu sem uma situação em que seja a melhor escolha.
- **Comportamento desejado:** cada habilidade com uma situação preferível, ajustando o que existe, sem criar novas.
  [proposta, uma por botão, a escolher e medir]:
  - **Tiro Duplo:** a segunda flecha vai no outro inimigo mais ferido, quando houver. Decisão: um tiro forte num alvo,
    ou acabar com dois feridos.
  - **Drenar Vida:** devolve também mana, parte do dano. Decisão: dano agora (Bola de Fogo) ou sustentar mana e vida
    para a luta longa.
  - **Desaparecer:** furtivo também tira você da mira por um turno, e os inimigos miram aliados (comitiva, animal,
    servo) quando houver. Decisão: proteger-se agora ou atirar.
  - **Golpe Pesado no Paladino:** **não mexer.** É uma habilidade da classe que a especialização supera, comum no gênero.
    O excesso de botões é assunto da preparação de habilidades (proposta futura).
  - **O Sombra no Vale:** aceitar o veneno como fraqueza contra mortos-vivos, mas dizê-lo na escolha e no Grimório (P3);
    nada de veneno que pega em quem é imune.
- **Exemplo de decisão:** o Patrulheiro com dois lobos feridos escolhe entre o Tiro Certeiro no maior e o Tiro Duplo que
  termina os dois.
- **Estruturas reaproveitadas:**
  - os blocos de `habilidades.py` (Salva, Dano, Se, Roubo, Buff, Codigo);
  - a escolha de alvo dos inimigos (`escolher_alvo_inimigo`);
  - o Grimório, que se descreve sozinho a partir dos blocos.
- **Custo e risco:** médio. Muda partidas do mundo gerado: o gabarito precisa de `--atualizar` intencional, com a
  transcrição conferida, e o ciclo de balanceamento do COMO_CRIAR (equilíbrio antes e depois).
- **Como verificar:**
  - as sequências da seção 9 antes e depois: cada botão ganha numa situação nomeada e perde fora dela;
  - Grimório e execução concordam;
  - `tests.equilibrio --spec` das especializações tocadas.

### P3. Encruzilhada e Grimório que explicam

- **Problema concreto:**
  - escolha irreversível sem informação (seção 2.7);
  - imunidades invisíveis;
  - Combustão anunciada pelo melhor caso;
  - Marca sem dizer que vale para todos;
  - a passiva do Paladino oculta.
- **Comportamento desejado:**
  - Na encruzilhada, cada caminho mostra:
    - bônus e custos de atributo (a Defesa −2 do Berserker);
    - a passiva, ou "sem passiva";
    - as habilidades do 4 e do 7 com a descrição calculada para o herói;
    - os talentos do ramo;
    - forte contra e fraco contra (o Sombra: veneno não pega em mortos-vivos e construtos).
  - No Grimório:
    - "não afeta mortos-vivos e construtos" no veneno;
    - a Combustão com o caso de uma camada ao lado do melhor caso;
    - a resistência ao terror do Paladino como passiva visível.
- **Exemplo de decisão:** o Arqueiro no Vale lê que a Flecha Envenenada não pega nos afogados e pondera o Patrulheiro
  com conhecimento, não por sorte.
- **Estruturas reaproveitadas:**
  - `SPECS`, `PASSIVAS`, o `desc_fn` e as `linhas` das habilidades;
  - o catálogo de estados (campo `imune`);
  - os dados da árvore (`talentos.dados_arvore`);
  - o menu com meta (a tela gráfica desenha cartões);
  - a festa "você agora é" (`celebracoes.js`), que já desenha habilidades;
  - o Grimório.
- **Custo:** baixo.
- **Risco:** no modo texto, a encruzilhada aparece nas transcrições do gabarito. Manter o texto das opções e pôr o detalhe
  no painel da tela gráfica, ou atualizar o gabarito de propósito.
- **Como verificar:**
  - teste de que cada caminho mostra os números do próprio catálogo;
  - captura da encruzilhada das três classes em 1500 e 1280 px;
  - Grimório com as linhas novas.

### Fora das três prioridades (registrado, não pedido)

- **Vigor e Foco que pesam** (custo × regeneração × duração das lutas): é a raiz da repetição do Guerreiro e do Arqueiro,
  mas mexe na curva das duas classes inteiras. Medir antes, com uma ferramenta que olhe as decisões (quantas vezes a
  melhor ação muda de um turno para o outro), não a taxa de vitória.
- Itens únicos com efeito próprio (a estrutura existe em `fonte_item`).
- Escolhas exclusivas na árvore.
- Preparação de habilidades e reespecialização.
- Transformação de habilidade (E6).

## 8. Proposta concreta da primeira implementação (P1)

**Escopo:** só a campanha, na capela. Nenhum número de classe, habilidade, talento ou item muda.

1. **Ossuário:** um dos dois esqueletos vira o "Esqueleto de Guarda", com a habilidade existente de preparar o Golpe
   Esmagador.
2. **Sarilho** (a onda de afogados de quem solta as correntes à mão, ou de quem falha o atalho): um dos afogados vira
   o "Afogado Inchado", que também prepara o golpe. Com isso, quem paga a luta do sarilho tem a decisão que o atalho
   da classe poupa.
3. **A guardiã** não muda nesta entrega: o rito já é a decisão dela.
4. **A ficha da luta e o bestiário** listam o golpe como habilidade do inimigo; o aviso na hora continua o de sempre.
5. **Previsibilidade:** primeiro só os dados. Se na medição o golpe não aparecer na maioria das lutas, entra o gancho
   mínimo "abre com o golpe preparado" (um campo no inimigo, lido por `agir_inimigo`), testado.
6. **Medição, antes e depois:**
   - as lutas da capela para Guerreiro, Arqueiro e Mago no nível 3 e no 4 (vitória, vida perdida, turnos);
   - quantas vezes o golpe preparado aparece;
   - com que ação a luta foi respondida (o robô defende quando vê o golpe preparado; seção 9).
7. **Pronto:**
   - teste unitário das duas lutas;
   - cenário de navegador com a captura do aviso;
   - verificações do CLAUDE.md;
   - registro no 00 com a rota curta: entrar na capela com cada classe e responder ao golpe de dois jeitos.

**Por que primeiro:**

- É a menor mudança que cria decisão de combate para as três classes no lugar onde Jean testa.
- Não toca nos números das classes nem no gabarito.
- Deixa pronto o cenário em que P2 e P3 serão medidos e vistos.

A P3 vem logo depois (barata e sem equilíbrio); a P2, por último, porque mexe no equilíbrio do mundo gerado.

## 9. Método e limites

Scripts de leitura, rodados fora do repositório (nenhum entrou no jogo):

1. **Orçamento de recurso:** herói montado por `rpg.dev.subir_ate` (os níveis como no jogo), sem talentos nem
   equipamento; atributos, máximo, regeneração e custos (`talentos.custo_habilidade`).
2. **Números do Grimório:** as `linhas` de cada habilidade (`habilidades.py`), as mesmas que o Grimório desenha, por
   especialização, nos níveis 3, 5 e 8.
3. **Sequências:** um alvo de treino (`Inimigo` com vida enorme, Defesa 3, Agilidade 0: sem esquiva).
   - Para cada sequência: a função da habilidade (`HABILIDADES[h]["fn"]`) e, entre uma ação e outra, o começo da vez do
     alvo (`Combate.processar_efeitos`: tique dos estados e duração).
   - Média de 2000 sorteios; sem talentos nem equipamento, salvo onde diz (Ignição).
   - Não entram aliados, buffs dos inimigos nem a sua defesa: mede só o dano entregue.
4. **Lutas do Vale** (tabela 2.8):
   - robô de `tests/arena.py`;
   - especialização no nível 5, talentos ao acaso (`dev.gastar_talentos`), equipamento sorteado no nível
     (`dev.vestir`), sem comitiva;
   - inimigos de nível 3 (afogado + carniçal; lobo + bandido);
   - 40 lutas por linha, sementes 0 a 39.

**Limites do robô:**

- Usa a habilidade de alvo único **mais cara** disponível e a de área mais cara com dois ou mais inimigos.
- Buffs em si mesmo ao acaso (40%).
- Cura abaixo de metade da vida; se protege quando ferido ou diante de golpe preparado.
- Mira o inimigo mais ferido.
- Não planeja: não acende para detonar, não escolhe a hora da Marca, não usa a Ordem da Fera pelo animal, não guarda
  Desaparecer para a Execução.

Por isso as tabelas do robô servem para **duração das lutas e efeito dos inimigos**, nunca para dizer que uma decisão é
boa; **taxa de vitória não é qualidade de decisão**. As comparações de decisão deste documento vêm das sequências (3),
que são exatas para o que medem e não dizem nada sobre o resto da luta.

**O que falta medir** (marcado como hipótese no texto):

- Fúria Cega e Maldição como ações dominantes no 7–9;
- o Inferno contra três ou mais inimigos;
- a Marca com comitiva e animal;
- o Contra-ataque na configuração Bastião.

## 10. P1 implementada: o golpe preparado na capela (1.57.0)

### 10.1 O que mudou

- **Ossuário:** um dos dois esqueletos é o **Esqueleto de Guarda**. **Sarilho** (a onda de afogados de quem solta as
  correntes à mão ou falha o atalho): um dos dois afogados é o **Afogado Inchado**.
- **A variante:** a mesma criatura da espécie (nível, vida, afixo e sorteio iguais aos de antes), com o Golpe Esmagador
  que o troll e o mercenário já têm (`inimigos.py`: `esmagar`):
  - prepara num turno e bate ×2,2 no seguinte;
  - atordoar interrompe;
  - guarda, barreira e esquiva reduzem ou evitam.

  `missoes.grupo_ossuario` e `missoes.grupo_sarilho` montam os grupos; `missoes._que_prepara` faz a variante.
- **A regra explícita, a menor que resolveu** (`combate/turnos.py`, `agir_inimigo`): a variante tem `abre_com =
  "esmagar"`.
  - Na primeira ação em que preparar faz sentido, ela prepara, sem sorteio. Com o herói a um golpe da morte, ela bate,
    como as outras habilidades que não ferem, e prepara depois.
  - Depois disso, o golpe fica no sorteio de sempre.
  - Só a campanha põe esse campo: os esqueletos e afogados do mundo gerado, a guardiã e todos os outros inimigos não
    mudam, e o sorteio deles é o mesmo (gabarito idêntico).
- **A ficha:**
  - Na tela gráfica, a ficha da carta (passar o mouse) tem a linha "⚠ Prepara um golpe esmagador (×2,2): avisa um
    turno antes. Atordoar interrompe; guarda, barreira e esquiva reduzem ou evitam." (`estado.py`: campo `nota`, só
    quando a criatura tem).
  - No modo texto, o Analisar mostra a mesma linha.
  - O aviso da luta é o de sempre: a faixa "⚠ prepara um golpe devastador" na carta, a frase "(Defenda-se, ou atordoe
    para interromper!)" e, no texto, "<< preparando golpe! >>".
- **Sem mudança:**
  - quantidade de inimigos, progressão, recompensas, vitória, fuga, derrota e resgate;
  - a guardiã;
  - atributos, regeneração, habilidades, talentos, itens e imunidades.
- Também saiu o aviso antigo do ossuário ("Protótipo: o fundo da capela fica para a próxima parte da missão.").

### 10.2 Frequência: o momento de responder

Conta-se uma **oportunidade** quando o herói tem uma ação para escolher com o golpe pendente e o preparador vivo. Não
conta quando o herói está atordoado, ou quando o preparador morre antes.

Robô de `tests/arena.py`; herói da campanha nos níveis 3 e 4 (no 4, ainda sem especialização: ela chega no descanso);
talentos ao acaso; equipamento sorteado no nível; um companheiro (aprovação 30); de dia, com tocha; vida e recurso
cheios; 150 lutas por linha.

| Comportamento | Lutas com ao menos uma oportunidade |
|---|---|
| Golpe só no sorteio de sempre (35% de chance de usar habilidade, dividida entre as do inimigo) | 33% a 58% |
| Com a regra (abre preparando) | **97% a 100%** |

Com a regra, há de 1,3 a 1,8 preparações por luta: a primeira garantida, as outras pelo sorteio.

Sem o companheiro (lutas mais longas, com o mesmo sorteio), o sorteio sozinho dava 37% a 69%. A regra entrou porque
metade das lutas sem o momento não é previsível. Nem a vida nem a duração dos inimigos mudaram para isso.

### 10.3 Antes e depois (robô, com um companheiro)

Vitórias · vida perdida · turnos. "Antes": os dois inimigos comuns. "Depois": com a variante e a regra.

| Classe, nível | Ossuário antes | Ossuário depois | Sarilho antes | Sarilho depois |
|---|---|---|---|---|
| Guerreiro 3 | 92% · 45% · 9,8 | 88% · 48% · 11,1 | 92% · 46% · 10,5 | 83% · 51% · 12,2 |
| Guerreiro 4 | 99% · 29% · 7,2 | 99% · 28% · 8,3 | 99% · 27% · 7,6 | 99% · 27% · 8,9 |
| Arqueiro 3 | 88% · 50% · 7,9 | 77% · 56% · 9,3 | 87% · 49% · 8,9 | 77% · 54% · 10,1 |
| Arqueiro 4 | 97% · 31% · 6,0 | 95% · 35% · 7,7 | 99% · 29% · 6,5 | 95% · 31% · 8,0 |
| Mago 3 | 80% · 52% · 8,2 | 75% · 52% · 9,8 | 85% · 46% · 9,3 | 67% · 59% · 10,8 |
| Mago 4 | 97% · 26% · 6,4 | 97% · 26% · 8,1 | 99% · 24% · 6,9 | 95% · 25% · 8,7 |

**O robô exagera a perda.**

- Ele usa a habilidade de alvo único mais cara: o Guerreiro ataca com Investida, não com Golpe Pesado.
- Ele se defende **toda vez** que vê o golpe preparado: o Mago gasta 20 de mana de Barreira em cada um.
- Ele nunca tenta interromper de propósito nem escolhe o alvo para matar o preparador primeiro.

Com um herói que só ataca com a habilidade principal (seção 10.4), a mesma luta quase não muda:

| Herói roteirizado | Antes | Depois |
|---|---|---|
| Guerreiro 3, ossuário | 98% · 38% · 5,8 | 96% · 38% · 5,7 |
| Arqueiro 3, ossuário | 98% · 38% · 5,5 | 94% · 35% · 5,4 |
| Mago 3, ossuário | 88% · 49% · 5,6 | 85% · 50% · 5,4 |

Com a resposta certa, o resultado até melhora: o Mago que se defende fica com 88% · 44%.

### 10.4 As respostas comparadas (herói roteirizado, com um companheiro)

**O herói roteirizado** (não o robô):

- ataca o inimigo mais ferido com a habilidade principal (Golpe Pesado, Tiro Certeiro, Bola de Fogo; sem mana, Lança de
  Gelo e depois o Dardo);
- bebe poção abaixo de 35% de vida;
- muda **só** a resposta ao golpe pendente.

Mesmos heróis, inimigos e sementes em cada resposta; 200 lutas por linha.

**Respostas comparadas:**

- **atacar:** ignora o aviso.
- **defender:** Erguer Escudo, Passo Ágil ou Barreira.
- **interromper:** Investida ou Lança de Gelo no preparador. O Arqueiro não tem como atordoar antes da especialização.
- **eliminar:** todo golpe no preparador desde o primeiro turno.

Na tabela, "Golpe" é a média de um golpe que acertou o herói (em % da vida máxima). O golpe também pode cair num
companheiro: o alvo é escolhido na hora de bater.

**Ossuário** (o sarilho dá o mesmo desenho):

| Classe, nível | Resposta | Vitórias · vida perdida · turnos | Golpe | Interrompidos por luta | Preparador morto com o golpe pendente, por luta |
|---|---|---|---|---|---|
| Guerreiro 3 | atacar | 96% · 38% · 5,7 | 27% | 0,04 | 0,28 |
| | defender (Escudo) | 96% · 37% · 6,8 | 14% | 0,04 | 0,03 |
| | interromper (Investida) | 98% · 35% · 5,9 | 28% | **0,53** | 0,20 |
| | eliminar | 96% · 38% · 5,8 | 27% | 0,04 | 0,32 |
| Guerreiro 4 | atacar / defender / interromper / eliminar | 100% · 22% / 21% / 22% / 23% | 21% / 10% / 23% / 22% | 0,01 / 0,02 / 0,34 / 0,01 | 0,42 / 0,04 / 0,30 / 0,47 |
| Arqueiro 3 | atacar | 94% · 35% · 5,4 | 30% | 0,04 | 0,39 |
| | defender (Passo Ágil) | 93% · 41% · 6,6 | 20% | 0,03 | 0,02 |
| | eliminar | 94% · 36% · 5,4 | 32% | 0,03 | **0,43** |
| Arqueiro 4 | atacar / defender / eliminar | 99% · 23% / 100% · 25% / 99% · 22% | 26% / 17% / 27% | — | 0,56 / 0,07 / **0,66** |
| Mago 3 | atacar | 85% · 50% · 5,4 | **43%** | 0,05 | 0,30 |
| | defender (Barreira) | 88% · 44% · 6,6 | **11%** | 0,07 | 0,09 |
| | interromper (Lança de Gelo) | 87% · 48% · 5,6 | 39% | **0,30** | 0,24 |
| | eliminar | 84% · 52% · 5,4 | 41% | 0,04 | 0,33 |
| Mago 4 | atacar / defender / interromper / eliminar | 96% · 32% / 99% · 22% / 98% · 31% / 96% · 33% | 32% / 4% / 32% / 32% | 0,06 / 0,05 / 0,21 / 0,02 | 0,46 / 0,07 / 0,42 / 0,48 |

**Leitura:** nenhuma resposta é sempre a melhor. Cada uma tem um custo que dá para entender.

- **Guerreiro:**
  - O Escudo corta o golpe pela metade, mas a luta dura um turno a mais.
  - A Investida interrompe 0,5 vez por luta no nível 3 e 0,3 no 4: 45% **se acertar**, e no nível 4 o esqueleto
    esquiva mais.
  - Quando a Investida falha, o golpe vem inteiro. No navegador, um crítico tirou 43 de 90.
- **Arqueiro:**
  - Antes da especialização não tem como interromper.
  - O Passo Ágil só reduz em média (30% de esquiva a mais) e custa o turno; sai pior que só atirar.
  - Matar o preparador antes é a melhor média no nível 4.
- **Mago:**
  - É quem mais sofre sem responder: o golpe tira de 32 a 43% da vida.
  - A Barreira quase anula o golpe, a 20 de mana.
  - A Lança de Gelo interrompe de 0,2 a 0,3 vez por luta (35% **se acertar**), mais barata, com risco.
- **Momento perdido:** o herói atordoado (Investida do esqueleto, agarrão do afogado) perde a vez de responder. Aconteceu
  em 2 das 8 sementes testadas no navegador. Nas medições, de 0 a 3% das lutas ficaram sem nenhuma oportunidade.

### 10.5 Na tela

Conferido com Playwright:

- capturas em 1500 e 1280 px;
- Guerreiro com Escudo e com Investida (uma semente em que interrompe, outra em que falha);
- Mago com Lança de Gelo;
- Arqueiro com Passo Ágil no sarilho.

**O que a tela mostra:**

- **Quem prepara:** a carta dele tem a faixa amarela piscando "⚠ prepara um golpe devastador".
  - Ela aparece de 0,5 a 0,9 s **antes** de as ações abrirem e fica até o golpe sair ou ser interrompido. Medido quadro
    a quadro, nas velocidades normal e rápida.
  - O registro destaca a frase "(Defenda-se, ou atordoe para interromper!)".
- **A ficha** (passar o mouse na carta) diz o que a variante faz.
- **Interrompido:** "Atordoado, Esqueleto de Guarda perde o golpe que preparava!", a faixa sai e o atordoado aparece na
  carta.
- **Limitação (corrigida na 1.58.0, seção 11.4):** em 1280 px, a faixa de ação de outro inimigo (por exemplo,
  "Investida") podia cobrir a linha do aviso por até 1,5 s logo que a vez chegava.

### 10.6 Verificações

- `tests/test_golpe_preparado.py` (9 testes):
  - os grupos das duas salas;
  - o sorteio igual ao de `g.grupo`;
  - o mundo gerado sem variante;
  - abre preparando, uma vez, e atordoar interrompe;
  - a guarda reduz o golpe;
  - a um golpe da morte, espera;
  - a ficha e o Analisar;
  - a ficha do mundo gerado sem nota;
  - as salas usam a variante e a missão segue, sem o aviso antigo.
- Fuga e derrota conferidas numa luta real do ossuário: a sala continua por vencer; a derrota sai para o resgate, ou
  para o fim no hardcore.
- `fumaca.mjs`: cenário novo do golpe preparado (o aviso na escolha, a ficha, a Investida que interrompe). O cenário
  `capela` aceita `SEMENTE`.
- Gabarito idêntico, sem atualizar.

### 10.7 O que fica para depois

- **P3:** a encruzilhada e o Grimório que explicam. Feita na 1.58.0 (seção 11).
- **P2:** um papel para cada botão dominado. Não autorizada; a ressalva do começo deste documento vale para ela.
- O Arqueiro sem como interromper antes da especialização é um fato do conteúdo de agora, não um defeito a corrigir
  nesta entrega.

## 11. P3 implementada: a encruzilhada e o Grimório que explicam (1.58.0)

Nenhum número de equilíbrio mudou. Sem P2, sem habilidade nova, sem reespecializar, sem preparar habilidades.

### 11.1 A escolha de especialização

- **Fluxo** (`eventos/classe.py`, `_escolher_caminho`): a narração de cada classe fica como era. No fim dela, em vez das
  duas opções diretas:
  1. **comparar:** os dois caminhos lado a lado;
  2. **olhar de perto** um deles: o mesmo resumo, com os números abertos e o botão Confirmar;
  3. **Confirmar** aplica uma vez; **Voltar (Esc)** volta à comparação, quantas vezes quiser.
  - "A escolha é definitiva: não há como trocar de caminho depois." aparece nas duas telas.
  - A comitiva reage à escolha confirmada, não ao olhar (as chaves de olhar e voltar não são de evento).
- **Cada caminho mostra** (`rpg/especializacao.py`, `previa`):
  - o estilo de jogo (a descrição do `SPECS`);
  - atributos antes → depois, com o que muda por nível;
  - as duas habilidades de agora e a do nível 7, com custo e a descrição;
  - **o que o caminho dá:** a passiva quando há; a resistência ao terror e os testes do Paladino; o animal do
    Patrulheiro; o crítico e a esquiva que a Agilidade +5 do Sombra rende; contra quem o dano do caminho rende mais;
  - **limites:** contra quem o dano rende menos, as imunidades dos estados que as habilidades aplicam (o veneno do
    Sombra não pega em mortos-vivos nem construtos) e os limites escritos de cada caminho (`SPECS[...]["limites"]`:
    o Berserker arrisca a vida, o Desaparecer não tira da mira, as armadilhas são talento);
  - **detalhe, fechado por padrão:** os números de cada habilidade (as mesmas linhas do Grimório), os três animais e os
    talentos do ramo.
- **De onde vêm os números:** da conta de verdade, feita numa **cópia** do herói (`copia_especializada`: `deepcopy` e o
  mesmo `aplicar_bonus` que a escolha usa). A habilidade do nível 7 vem "com os números de hoje", e a tela diz isso.
- **Modo texto:** o resumo dos dois caminhos, depois o detalhe do que se olha; as perguntas dizem o que se escolhe.

### 11.2 O Grimório

- **Imunidades:** o catálogo de estados ganhou o campo `imunes` (veneno: mortos-vivos e construtos; sangramento:
  construtos e etéreos; queimadura: quem resiste muito ao fogo). A descrição de cada habilidade e do talento Pontas
  Venenosas o mostra.
- **"Se acertar":** as linhas de efeito que dependem do golpe acertar começam assim (Investida, Lança de Gelo, Flecha
  Envenenada, a mordida do lobo). Uma regra geral, só quando o herói tem uma habilidade assim, explica o resto: a chance
  só vale no acerto; atordoar ou congelar faz perder um golpe preparado; chefes e gigantes resistem.
- **Defesa:** a guarda diz que vale também contra o golpe preparado; a esquiva, que é uma chance a cada golpe; o
  Desaparecer, que os inimigos continuam mirando você. Uma regra geral compara guarda, barreira e esquiva diante do
  golpe preparado.
- **Marcar Presa:** "+25% de dano de todos os golpes: os seus, os da comitiva e os do animal".
- **Combustão:** três exemplos:
  - sem chamas;
  - 1 camada, acesa no turno anterior;
  - 3 camadas, com a condição escrita: três Bolas de Fogo seguidas que acenderam, detonadas logo depois.
  - A nota diz a chance de a Bola acender agora.
  - Um teste confere os dois exemplos contra o golpe de verdade (3000 sorteios, dentro de 3%).
- **O caminho como página:** depois de escolher, o Grimório tem a página do caminho (o que dá, o bônus, os limites). A
  resistência ao terror do Paladino fica visível ali.
- **Modo texto:** a tela de personagem troca a linha "Habilidades: ..." pelo Grimório em uma linha por habilidade, e as
  regras gerais.

### 11.3 O que não foi prometido

O Desaparecer não tira da mira, as armadilhas do Patrulheiro são o talento Armadilheiro (um inimigo começa a luta preso)
e não uma habilidade, e o servo do Necromante só atrai golpes nos dois primeiros turnos. Os textos dizem isso; nada foi
acrescentado ao combate.

### 11.4 O aviso do golpe preparado

Na sua vez, a carta de quem prepara fica por cima da faixa de ação de outro inimigo (`03-batalha.css`, só enquanto a
carta do herói está na vez). Sem espera nova e sem mudar animação. Conferido em 1280 px, e o `fumaca.mjs` agora checa
que nada cobre o aviso.

### 11.5 Passo Ágil: questão aberta para a P2

Nos encontros medidos na P1 (seção 10.4), o Passo Ágil **não** mostrou utilidade: só reduz o golpe em média e custa o
turno, e saiu pior que só atirar ou matar o preparador antes. Isso não prova que seja inútil em outros encontros, mas a
P1 não comprovou utilidade. **Respondida na seção 13.4:** em lutas inteiras, no Vale e depois, ele não tem vantagem
relevante.

### 11.6 Verificações

- `tests/test_especializacao.py` (8 testes):
  - os seis caminhos comparáveis;
  - os exemplos pedidos (Berserker com Defesa −2, Paladino com terror e testes, o animal, o veneno do Sombra);
  - a prévia igual ao herói depois de escolher, com talentos e equipamento;
  - a prévia não muda herói, sorteio, comitiva nem saves;
  - olhar, voltar e confirmar uma vez (nada muda até confirmar; a aprovação da comitiva só depois);
  - a tela gráfica recebe o painel;
  - os textos do Grimório;
  - a Combustão como a execução.
- **Gabarito atualizado de propósito.** Mudaram só textos:
  - as descrições curtas de Investida, Marcar Presa, Lança de Gelo, Flecha Envenenada e Pontas Venenosas;
  - o Grimório no estado do herói;
  - a tela de personagem do modo texto;
  - uma quebra de linha a mais no modo texto, porque a descrição ficou mais longa.
  - Tirando esses textos, as 24 transcrições ficam iguais linha a linha: mesmas escolhas, mesmo número de opções,
    mesmos lances e mesmo sorteio. As partidas do gabarito não chegam à encruzilhada.
- **Navegador**, nas três classes, em 1500 e 1280 px:
  - comparar, olhar de perto, Voltar (Esc) e confirmar;
  - os seis caminhos confirmados;
  - o herói igual depois de olhar e voltar;
  - os atributos depois de confirmar iguais aos da prévia;
  - as páginas do Grimório (o caminho, a Combustão, a Marca, a Investida, a Lança).
  - `fumaca.mjs` ganhou o cenário da encruzilhada; `cenarios.py` ganhou `encruzilhada` (CLASSE, NIVEL).

## 12. P2, primeira habilidade: o Tiro Duplo (1.59.0)

Só o Tiro Duplo mudou. Custo (10 de Foco), flechas (2) e coeficientes (dois disparos de 90%) ficaram como eram: as
medidas abaixo mostram que eles sustentam o papel, então nenhum número foi proposto nem alterado.

### 12.1 O comportamento

- O 1º disparo vai no alvo que você escolhe.
- O 2º (`Dano(..., em="outro")`, `habilidades.segundo_alvo`):
  - havendo outro inimigo de pé, vai nele;
  - havendo vários, no **mais ferido** (`habilidades.mais_ferido`);
  - restando só o 1º alvo, volta nele;
  - sem ninguém de pé, não sai, e a luta acaba como sempre.
- A morte do 1º alvo não cancela o 2º disparo, que segue para outro inimigo.
- **O critério "mais ferido"** é o que o jogo já usa na cura dos inimigos e nas preces da Odette: a **menor fração de
  vida** (vida ÷ vida máxima). No empate, o primeiro na ordem da luta (a carta mais à esquerda; no texto, A antes de B).
- Cada disparo é um golpe próprio, com crítico, esquiva, a Marca e o abate no alvo dele.
  - O Tiro de Abertura vale só para o 1º.
  - Cada abate dispara os efeitos uma vez.
- As 2 flechas e os 10 de Foco saem uma vez, no começo, como antes. Se o 1º derruba o último inimigo, o 2º não sai, mas
  as duas flechas já foram (e entram na conta de recolher no fim da luta).
- **Na tela**, a rajada é a de sempre: duas flechas quase juntas, cada uma voando para a carta que acerta. O registro
  diz quem recebeu cada tiro ("[Tiro Duplo (1)] Você atinge Alfa", "[Tiro Duplo (2)] Você atinge Gama"); a queda do 1º
  aparece entre os dois.
- **Descrição curta, Grimório e prévia** dizem o mesmo. O Grimório tem a linha de dano ("Cada um dos 2 disparos") e uma
  linha de para onde vai o 2º. A prévia da especialização usa as mesmas linhas.

### 12.2 Como foi medido

- **Execução real:** o menu de habilidades do combate (`fase_jogador`), com um roteiro que escolhe a ação e o alvo.
- **Herói:** Patrulheiro nos níveis 4, 5, 6 e 9.
  - Sem talentos: os pontos ficam guardados, porque Mira Firme e Olho de Águia valem igual para as três habilidades e
    o Tiro de Abertura distorceria o 1º golpe.
  - Equipamento de `dev.vestir` com semente fixa.
  - Nível 4: Ataque 20, Agilidade 16, crítico 21%, Foco 31 (+5 por turno). Nível 6: Ataque 29, crítico 26%. Nível 9:
    Ataque 36, crítico 38%.
- **Luta `sozinho`** (sem o animal), com inimigos um nível abaixo e sem afixo.
- **As mesmas sementes** para as três habilidades: 3000 por linha numa ação, 1000 na luta inteira.
- **Alvo do jogador:**
  - o inimigo com menos vida, para o Tiro Certeiro e o 1º do Tiro Duplo;
  - o inteiro, nos cenários 7 a 9, para ver o 2º terminar o ferido.
- **Duas medidas:**
  - **Uma ação:** dano que conta (sem o excesso além da vida) e abates.
  - **A luta inteira** repetindo a ação, com Disparo quando falta Foco e inimigos parados:
    - turnos para limpar;
    - **ações inimigas**: a soma, turno a turno, dos inimigos que seguem de pé e agiriam. É o que a luta custa em vida;
    - Foco e flechas gastos.
- **Antes:** a 1.58.0, na mesma régua; lá os dois disparos iam no mesmo alvo.
- Script fora do repositório; a seção 9 descreve o método e os limites.

### 12.3 Resultados (nível 4; o 6 é parecido)

Cada célula: turnos para limpar / ações inimigas / Foco na luta. Entre colchetes, uma ação: dano, abates.

| Cenário | Tiro Certeiro | Tiro Duplo antes | **Tiro Duplo agora** | Chuva de Flechas |
|---|---|---|---|---|
| 1 inimigo resistente (troll) | **4,41 / 3,41 / 35** [28,6] | 4,78 / 3,78 / 48 [25,8] | 4,78 / 3,78 / 48 [25,8] | 7,75 / 6,75 / 62 |
| 2 feridos (lobos a 35%) | 2,18 / 1,27 / 17 [0,92] | 2,10 / 1,15 / 21 [0,96] | 1,61 / 0,73 / 16 [1,30] | **1,27 / 0,28 / 20** [1,77] |
| 2 com bastante vida (bandidos) | **4,41 / 4,60 / 35** | 4,33 / 4,49 / 43 | 4,16 / 5,75 / 42 | 5,19 / 6,56 / 47 |
| 3 lobos inteiros | **5,33 / 7,66 / 43** | 6,03 / 8,95 / 52 | 5,12 / 8,53 / 49 | 5,27 / 8,78 / 47 |
| 4 lobos inteiros | 7,08 / 13,75 / 56 | 8,17 / 16,11 / 63 | 7,17 / 15,53 / 59 | **6,13 / 13,22 / 55** |
| 3 lobos a 35% | 3,26 / 3,52 / 26 | 3,14 / 3,29 / 31 | 2,35 / 2,09 / 23 | **1,37 / 0,40 / 21** |
| 1º cai no 1º disparo (lobo a 8% + lobo inteiro) | 2,86 / 1,95 / 23 | 2,99 / 1,99 / 30 | **2,33 / 1,42 / 23** | 3,03 / 2,12 / 35 |
| 2º derruba (1º no inteiro, outro a 12%) | 2,86 / 1,95 / 23 | 2,97 / 2,94 / 30 | **2,32 / 1,38 / 23** | 3,00 / 2,06 / 35 |
| 2º pode errar (1º num lobo, harpia a 30%) | 2,90 / 2,03 / 23 | 2,98 / 2,95 / 30 | **2,36 / 1,48 / 24** | 3,06 / 2,17 / 35 |

**Com pouco Foco** (a luta começa com 15, depois de outra; a Chuva fica fora de alcance no 1º turno):

| Cenário (nível 4) | Tiro Certeiro | Tiro Duplo agora | Chuva de Flechas |
|---|---|---|---|
| 2 feridos | 2,18 / 1,27 / 17 | **1,61 / 0,73 / 16** | 2,15 / 1,23 / 20 |
| 2 com bastante vida | **4,78 / 4,98 / 30** | 4,72 / 6,22 / 32 | 6,06 / 7,51 / 40 |
| 3 lobos a 35% | 3,26 / 3,52 / 24 | **2,41 / 2,15 / 21** | 2,26 / 2,35 / 20 |

**Nos níveis 5 e 9**, os lobos a 35% já não caem com um disparo de 90%.

- **2 feridos, nível 5:**
  - Tiro Duplo: 1,98 turnos e 1,39 ações inimigas;
  - Tiro Certeiro: 2,21 turnos e 1,32 ações inimigas.
- **2 feridos, nível 9:** o Tiro Duplo faz 1,53 ações inimigas, o Tiro Certeiro 1,36.
- **Um quase morto e outro de pé:** o Tiro Duplo continua o melhor, nos níveis 5 e 9 (2,66 a 2,74 turnos, contra 3,18 a 3,48).

### 12.4 O papel demonstrado

- **O Tiro Duplo é preferível** quando há dois alvos e cada um está ao alcance de um disparo de 90%. Isso inclui um
  inimigo quase morto e outro de pé: o 1º termina, o 2º não se perde.
  - Nesses casos é o melhor em turnos e em ações inimigas, com o Foco do Tiro Certeiro e a metade do da Chuva.
  - Com menos de 20 de Foco, é o melhor também com dois ou três feridos.
- **Outra habilidade continua melhor:**
  - **Um alvo resistente:** o Tiro Certeiro (mais dano, menos Foco, uma flecha).
  - **Dois inimigos com bastante vida:** o Tiro Certeiro. O Tiro Duplo espalha o dano, o primeiro abate demora, e a
    luta custa mais ações inimigas (5,75 contra 4,60).
  - **Três ou mais, com Foco para isso:** a Chuva de Flechas. Com três inteiros, o Tiro Certeiro empata ou ganha (menos ações inimigas).
  - **Dois feridos fora do alcance de um disparo** (nível 5 e 9 acima): o Tiro Certeiro, por pouco.
- Não virou a melhor ação de todo turno.
- A decisão se lê na tela: a vida nas cartas e a faixa de dano do Grimório (12–16 por disparo no nível 4).

### 12.5 No simulador e no replay

Mexe pouco, porque o robô quase não escolhe o Tiro Duplo:

- com dois ou mais inimigos, ele usa a Chuva;
- com o animal de pé, prefere a Ordem da Fera, que é mais cara.

`tests.equilibrio --spec patrulheiro --lutas 150`, lutas comuns, antes → agora:

| Nv | Vitórias | Turnos | Vida perdida | Seus turnos p/ matar |
|---|---|---|---|---|
| 4 | 100% → 100% | 4,6 → 4,6 | 16% → 16% | 3,6 → 3,6 |
| 5 | 91% → 93% | 5,9 → 5,7 | 25% → 24% | 5,4 → 5,2 |
| 6 | 93% → 93% | 6,5 → 6,4 | 23% → 23% | 5,6 → 5,5 |
| 8 | 91% → 89% | 6,3 → 6,0 | 26% → 26% | 4,8 → 4,7 |
| 10 | 92% → 93% | 5,2 → 5,2 | 18% → 18% | 4,3 → 4,3 |
| 12 | 91% → 91% | 5,2 → 5,1 | 23% → 23% | 4,6 → 4,5 |

- **Simulador:** dentro do ruído; as lutas ficam um pouco mais curtas. Os guardiões são 6 por nível e oscilam como
  antes.
- **Sem comitiva** (`--sozinho`, 30 lutas): praticamente igual (diferenças de 0,1 turno e 1 ponto de vida perdida).
- **`tests.replay`:**
  - Xatuba (Patrulheiro): 89% → 88% de vitórias do robô, 7,0 → 6,9 turnos;
  - Fuckerson (Patrulheiro): igual.
- **Gabarito: não mudou.** O arqueiro do robô não passa do nível 2 em nenhuma das 24 partidas, então a mudança, que
  vale também no mundo gerado, não aparece nelas.

### 12.6 Limitações

- **"Mais ferido" é por fração de vida, não por vida que falta.** Um inimigo grande a 30% recebe o 2º disparo antes de
  um pequeno a 40% com menos vida. É o critério que o jogo já usa; o Grimório diz isso.
- **Um 1º disparo que erra não é repetido no mesmo alvo** quando há outro de pé: o 2º vai no outro. Antes, ele repetia
  no mesmo alvo.
- **As duas flechas saem** mesmo quando o 1º derruba o último inimigo, como antes.
- **O papel depende da vida dos inimigos:** com um disparo de 90% que não derruba, os dois feridos ficam para o Tiro
  Certeiro. Não há aviso de "ao alcance"; a decisão é do jogador, pela vida e pela faixa de dano.
- **As medidas usam inimigos parados e herói sem talentos:** servem para comparar as três habilidades nas mesmas
  condições, não para dizer quanto uma luta real custa.

### 12.7 Verificações

- **`tests/test_tiro_duplo.py`** (10 testes), pelo menu do combate:
  - o critério e o desempate;
  - sem outro inimigo, o mesmo alvo; sem ninguém, nada;
  - um disparo em cada inimigo, com Foco e flechas uma vez e o registro com quem recebeu;
  - sozinho, os dois no mesmo alvo;
  - o 1º cai e o 2º segue;
  - dois abates sem duplicar;
  - o último cai no 1º e a luta acaba;
  - o 2º pode errar;
  - a Marca e o Tiro de Abertura no alvo certo;
  - descrição, Grimório e prévia.
- **`test_habilidades`:** o 2º disparo não conta como linha de dano própria.
- **Navegador, em 1500 e 1280 px:**
  - o 1º derruba Alfa e o 2º vai em Gama, o mais ferido;
  - com os três de pé, o 1º em Beta (a escolha) e o 2º em Gama (o crítico no alvo certo);
  - a rajada, o registro, as flechas (20 → 18) e o Foco (33 → 23);
  - o Grimório e a prévia da encruzilhada.
  - `cenarios.py` ganhou `tiro_duplo` (NIVEL, VIDAS); `fumaca.mjs` ganhou o cenário.

### 12.8 O que fica para depois

Drenar Vida, Desaparecer e Passo Ágil, na ordem que Jean decidir. O Passo Ágil continua como questão aberta (seção 11.5).
Avaliados na seção 13.

## 13. P2: Drenar Vida, Desaparecer e Passo Ágil em lutas inteiras (avaliação, sobre a 1.59.0)

Só medida e diagnóstico. Nenhum código, número ou save mudou. As propostas desta seção **não estão aprovadas**: recuperar
mana com o Drenar Vida e mudar a mira em furtividade continuam propostas da seção 7, e a mudança do Passo Ágil (13.5)
também.

### 13.1 Método

- **Lutas inteiras pelo combate de verdade:** os inimigos agem com a IA do jogo, até vitória ou derrota.
  - O robô de `tests/arena.py` não decide. Um roteiro fixo escolhe ação e alvo a cada vez (as regras estão abaixo de
    cada tabela).
  - A medição usa o `Combate` do jogo e um roteiro em `escolher`. Os scripts ficaram fora do repositório.
- **Herói fixo por linha:**
  - O nível e os talentos estão na tabela.
  - **Equipamento:** o de `dev.vestir`, na semente (de 40) cuja vida e cujo ataque principal ficam mais perto da
    mediana. Um herói típico, sem item único que decida a luta. Os itens desse sorteio trazem 3% a 4% de roubo de vida,
    que vale para todo golpe em todos os roteiros.
  - Sem poções, de dia, tempo limpo. Arqueiros com 40 flechas.
  - O Patrulheiro luta sem o animal, para medir só o Passo Ágil.
- **Fichas:**

| Herói | Vida | Ataque principal | Agilidade | Defesa | Recurso (+/turno) | Talentos |
|---|---|---|---|---|---|---|
| Arqueiro 3 | 73 | Ataque 15 | 14 | 8 | Foco 29 (+5) | nenhum |
| Patrulheiro 4 | 96 | Ataque 20 | 15 | 15 | Foco 39 (+5) | nenhum |
| Sombra 4 | 96 | Ataque 21 | 20 | 15 | Foco 39 (+5) | nenhum |
| Sombra 7 | 130 | Ataque 33 | 27 | 26 | Foco 48 (+5) | Golpe Sombrio 2/2 |
| Sombra 9 | 151 | Ataque 40 | 32 | 26 | Foco 55 (+5) | Golpe Sombrio 2/2, Assassino |
| Necromante 4 | 88 | Poder 25 | 9 | 11 | Mana 58 (+3) | nenhum, ou Pacto Sombrio 2/2 |
| Necromante 7 | 143 | Poder 40 | 15 | 16 | Mana 76 (+3) | Pacto Sombrio 2/2, Legião de Ossos |

- **Encontros:**
  - **O Vale**, com inimigos de nível 3, o da capela. O Sombra e o Necromante só existem a partir do nível 4.
    - o ossuário e o sarilho como na missão: dois esqueletos ou dois afogados, um deles com o golpe preparado
      (`missoes._que_prepara`). São mortos-vivos;
    - três lobos (o bosque);
    - a bruxa do brejo com um sapo (o charco).
  - **Depois do Vale** (mundo gerado), com inimigos um nível abaixo do herói:
    - três bandidos;
    - um mercenário (blindado, com o golpe preparado do próprio catálogo) e um bandido;
    - dois carniçais (mortos-vivos);
    - um troll um nível acima (luta longa, regenera, golpe preparado);
    - o guardião da floresta (só para o Necromante).
- **Condições:** vida cheia; ferido (começa com 45%); por um fio (25%, só no Necromante 4); com aliado (Morel, o escudo
  da comitiva, aprovação 30).
- **Medidas:**
  - vitórias, que dizem o risco de derrota;
  - vida no fim, com derrota contando como 0;
  - "por um fio": vitória com menos de 15% de vida;
  - turnos, recurso no fim e usos de cada habilidade.
  - No Drenar Vida, também a cura que chegou, a cura cheia e o dano além da vida do alvo.
- **Amostra:**
  - 600 lutas por linha, com as mesmas sementes para todos os roteiros de um mesmo encontro e condição.
  - Diferenças de até 4 pontos de vitória são ruído.
  - Os casos perto disso foram refeitos com outras sementes e 3000 lutas. Um deles, o troll, caiu: está marcado.

### 13.2 Drenar Vida

**Roteiros** (o alvo é sempre o inimigo com menos vida):

- **Bola:** Bola de Fogo sempre (o Dardo, quando falta mana). É a alternativa que o diagnóstico chamou de dominante.
- **Drenar sempre:** Drenar Vida no lugar da Bola.
- **Drenar <60%:** Drenar Vida quando a vida está abaixo de 60%; acima, Bola.
- **Barreira <50%:** Barreira Arcana abaixo de 50%, se não tiver uma; no resto, Bola.
- **Servo + …:** ergue o servo no 1º turno e segue o roteiro.
- No nível 7, todos os roteiros abrem com a Maldição contra grupos (depois do servo, nos que erguem servo).

**Necromante 4, sem talentos, sozinho.** Cada célula: vitórias (vida no fim).

| Encontro | Vida inicial | Bola | Drenar sempre | Drenar <60% | Barreira <50% | Servo + Bola | Servo + Drenar <60% |
|---|---|---|---|---|---|---|---|
| Ossuário (mortos-vivos) | cheia | 100% (69%) | 76% (26%) | 98% (69%) | 100% (70%) | 100% (72%) | 100% (73%) |
| | 45% | 81% (19%) | 13% (2%) | 13% (2%) | **93%** (37%) | 83% (23%) | 54% (14%) |
| | 25% | 39% | 3% | 3% | **80%** | 44% | 18% |
| Sarilho (mortos-vivos) | 45% | 92% (25%) | 14% (3%) | 14% (3%) | **98%** (41%) | 82% (22%) | 57% (14%) |
| 3 lobos (vivos) | cheia | 87% (33%) | 98% (74%) | 99% (56%) | 96% (44%) | 98% (66%) | 99% (70%) |
| | 45% | 12% (2%) | 80% (35%) | 80% (34%) | 74% (22%) | 75% (19%) | **88%** (39%) |
| | 25% | 2% | 48% | 48% | 41% | 41% | **64%** |
| Bruxa + sapo (vivos) | cheia | 99% (59%) | 99% (83%) | 100% (67%) | 99% (60%) | 100% (74%) | 100% (76%) |
| | 45% | 61% (12%) | 90% (48%) | 90% (46%) | 88% (30%) | 88% (26%) | **96%** (50%) |
| | 25% | 20% | 72% | 72% | 63% | 58% | **87%** |

**Necromante 7, Pacto Sombrio 2/2 e Legião de Ossos, sozinho.** Vitórias.

| Encontro | Vida inicial | Bola | Drenar sempre | Drenar <60% | Barreira <50% | Servo + Bola | Servo + Drenar <60% |
|---|---|---|---|---|---|---|---|
| 3 bandidos | cheia | 97% (53%) | 100% (87%) | 100% (73%) | 100% (57%) | 99% (62%) | 100% (77%) |
| | 45% | 28% | 57% | 57% | 65% | 41% | **74%** |
| Mercenário + bandido | 45% | 69% | 84% | 84% | **94%** | 85% | 92% |
| 2 carniçais (mortos-vivos) | 45% | 21% | 16% | 16% | 59% | **67%** | 50% |
| Troll (luta longa) | 45% | 45% | 63% | 61% | 51% | 68% | **80%** |
| Guardião da floresta | cheia | 46% (14%) | 43% | 60% | 48% | 73% | **77%** (42%) |
| | 45% | 4% | 17% | 17% | 2% | 12% | **33%** |

- **Pacto Sombrio 2/2 no nível 4** (cura 60% em vez de 40%):
  - **3 lobos, ferido:** Drenar 93% contra 12% da Bola; servo e Drenar, 97%.
  - **Ossuário, ferido:** Drenar 30% contra 81% da Bola.
- **Com Morel e vida cheia:** todos os roteiros ganham 100%. O Drenar só muda a vida no fim (3 lobos: 96% contra 78%).

**A cura de verdade** (nível 4, "Drenar sempre"):

| Situação | Cura cheia (40% do dano) | Recebida | Perdida por vida cheia | Vinda do dano além da vida do alvo |
|---|---|---|---|---|
| 3 lobos, vida cheia | 54,1 | 40,3 | 26% | 22% |
| 3 lobos, ferido | 48,8 | 47,0 | 4% | 21% |
| Bruxa + sapo, ferido | 47,2 | 45,2 | 4% | 15% |
| 3 lobos, vida cheia, com Morel | 53,7 | 23,1 | 57% | 23% |

- **O golpe que passa da vida:** o Drenar Vida cura sobre o **dano inteiro**, não sobre a vida que o alvo tinha. Num
  lobo com 1 de vida, cura o mesmo que num inteiro (8,4 no nível 4) [código: `Roubo` usa o dano devolvido por `atacar`,
  que não para na vida do alvo; o roubo de vida dos itens e a Sede de Sangue seguem a mesma regra].
  - Isso responde por 15% a 23% da cura nas lutas medidas.
  - Somado à Colheita (+5 de mana por abate), faz do Drenar um bom golpe de misericórdia.
- **Contra mortos-vivos**, o dano de sombra sai pela metade, e a cura também: num esqueleto, 9,6 de dano e 3,6 de
  cura, contra 21,9 e 8,4 num lobo.
- **Mana não é o limite:** em todas as linhas, o Necromante termina com 35% a 87% da mana.

**Leitura:**

- **Função útil demonstrada:** sustentar a luta contra vivos quando a vida já baixou.
  - **No Vale** (bosque e charco), ferido, o Drenar transforma derrota em vitória:
    - 3 lobos: 12% → 80%;
    - bruxa e sapo: 61% → 90%;
    - com 25% de vida: 2% → 48% e 20% → 72%.
  - **Depois:** bandidos 28% → 57%; troll 45% → 63%; guardião, de vida cheia, 46% → 60%.
  - Com o servo, ele é a melhor combinação medida contra vivos e nas lutas longas.
- **Armadilha contra mortos-vivos:**
  - No ossuário e no sarilho do Vale, ferido, o Drenar faz 13–14%, contra 81–92% da Bola; ali a resposta é a
    Barreira (93–98%).
  - Nos carniçais do nível 7, 16%; a resposta é o servo (67%) ou a Barreira (59%).
  - O jogo já diz isso (limites do caminho e Grimório: "Dano de sombra rende menos contra mortos-vivos ×0,5").
- **De vida cheia e sem perigo:** não muda o resultado. Perde um quarto da cura sozinho e mais da metade com aliado.
  Contra 3 lobos, porém, já ganha da Bola desde o começo (98% contra 87%): a luta com vários vivos desgasta.
- **Dano menor que o da Bola** não é defeito aqui: o valor dele é a vida que devolve na hora em que ela falta.

### 13.3 Desaparecer

**Roteiros** (o ataque é o Tiro Certeiro; a Flecha Envenenada fica de fora porque não pega em mortos-vivos):

- **Atacar:** o inimigo com menos vida.
- **Atacar quem prepara:** quem prepara um golpe; sem ninguém preparando, o de maior ataque.
- **Desaparecer no preparo:** Desaparecer quando alguém prepara; o tiro furtivo seguinte vai em quem prepara.
- **Desaparecer no 1º turno:** a abertura; o tiro furtivo vai no mais perigoso.
- **Desaparecer <50%:** Desaparecer abaixo de 50% de vida, quando não está furtivo nem esquivo.
- **Desaparecer guardado para a Execução** (nível 7 em diante): espera alguém cair abaixo de 35%, desaparece e executa.
- **Passo Ágil no 1º turno:** a esquiva sozinha, para separar o efeito dela do efeito do crítico.
- No nível 7, todos os roteiros usam a Execução em quem está abaixo de 35%.

| Herói, encontro | Vida inicial | Atacar | Atacar quem prepara | Desaparecer no preparo | Desaparecer 1º turno | Desaparecer <50% | Passo Ágil 1º turno | Desaparecer p/ Execução |
|---|---|---|---|---|---|---|---|---|
| Sombra 4, ossuário | cheia | 100% (94%) | 100% | 100% (89%) | 100% (94%) | 100% | — | — |
| | 45% * | 97% (49%) | 97% | 92% | 98% (51%) | 98% (52%) | 92% | — |
| Sombra 4, sarilho | 45% | 99% | 99% | 96% | 99% | 100% | — | — |
| Sombra 4, 3 lobos | 45% * | 92% | 92% | 92% | 93% | 94% | 86% | — |
| Sombra 4, bruxa + sapo | 45% | 94% | 76% | 94% | 84% | 82% | — | — |
| Sombra 7, 3 bandidos | 45% * | 75% | 75% | 75% | 76% | 73% | 72% | 70% |
| Sombra 7, mercenário + bandido | 45% | 85% | 71% | 84% | 74% | 62% | — | 78% |
| Sombra 7, 2 carniçais | cheia * | 99% (70%) | 99% | 99% | **100% (79%)** | 99% | 98% | 97% |
| | 45% * | 69% (21%) | 68% | 69% | **83% (31%)** | **84% (32%)** | 62% | 55% |
| Sombra 7, troll | 45% * | 66% | 64% | 67% | 62% | 54% | 59% | 49% |
| Sombra 9 (Assassino), 3 bandidos | cheia | 96% | 96% | 96% | 98% | 95% | — | 95% |
| Sombra 9 (Assassino), troll | cheia | 94% | 94% | 93% | 93% | 86% | — | 85% |

\* refeito com outras sementes e 3000 lutas. Nas colunas que foram refeitas, a tabela traz o número da repetição; nas
outras, o da primeira rodada (600 lutas). Na primeira rodada, o troll dava 70% contra 63–64% para o Desaparecer no
preparo: era ruído.

- **Com Morel**, nos níveis 4 e 7: todos os roteiros ganham 99–100%, e a diferença fica só na vida no fim (±3 pontos).

**Leitura:**

- **No Vale: sem vantagem relevante.**
  - O Sombra 4 vence o Vale de vida cheia em todo roteiro.
  - Ferido, a abertura com Desaparecer empata com atacar (dentro de 1–2 pontos). No preparo, perde de 4 a 5.
  - Contra a bruxa (magia), a abertura perde 10 pontos.
- **Depois do Vale: função restrita, mas legítima.**
  - Contra **dois inimigos resistentes, com vida a menos**, a abertura com o crítico das sombras derruba um deles cedo.
    Contra os carniçais, 69% → 83% (confirmado em 3000 lutas).
  - O ganho é do **crítico**, não da esquiva: o Passo Ágil no mesmo turno faz 62%.
  - De vida cheia, o mesmo encontro só ganha vida no fim (70% → 79%).
  - Contra grupos de inimigos fracos (bandidos) e contra o troll sozinho, não muda nada.
- **A esquiva de +50% por 1 turno:** sem evidência de valor. Não muda o golpe preparado (troll e mercenário empatam).
- **A sinergia com a Execução:** hipótese sem evidência. Guardar o Desaparecer para executar piorou em todo encontro
  medido (troll ferido: 49% contra 66%). O Assassino (nível 9) não mudou isso.
- **Priorizar o inimigo perigoso** nem sempre é a resposta: contra o mercenário blindado, ferido, atacá-lo primeiro
  ganha 71%, contra 85% de matar o bandido antes.

### 13.4 Passo Ágil

**Roteiros:** atacar; Passo Ágil quando alguém prepara; Passo Ágil no 1º turno; Passo Ágil sempre que há 2 ou mais
inimigos (mantém o efeito); Passo Ágil abaixo de 50%.

| Herói, encontro | Vida inicial | Atacar | Passo no preparo | Passo 1º turno | Passo com 2+ | Passo <50% |
|---|---|---|---|---|---|---|
| Arqueiro 3, ossuário | cheia | 95% (48%) | 87% (34%) | 89% | 77% | 87% |
| | 45% | 40% | 21% | 20% | 13% | 6% |
| Arqueiro 3, sarilho | cheia | 96% | 89% | 91% | 76% | 84% |
| | 45% | 43% | 24% | 22% | 12% | 7% |
| Arqueiro 3, 3 lobos | cheia | 76% | 76% | 63% | 39% | 52% |
| Arqueiro 3 com Morel, ossuário | cheia | 100% (77%) | 100% (72%) | — | 99% (66%) | 100% |
| Patrulheiro 4 (sem o animal), ossuário | 45% | 94% | 85% | 86% | 73% | 67% |
| Patrulheiro 4, 3 lobos | 45% | 87% | 87% | 77% | 56% | 55% |
| Sombra 7, troll | 45% | 66% | 66% | 59% | — | 43% |
| Sombra 9, troll | cheia | 94% | 91% | — | — | 80% |

**Leitura: sem vantagem relevante nas situações avaliadas,** no Vale e depois, com ou sem aliado.

- O Passo Ágil troca um ataque por 30% de esquiva em duas vezes de inimigo.
- Os inimigos medidos tiram pouco por golpe perto do que um Tiro Certeiro a menos custa em duração. Até diante do golpe
  preparado, atacar ganha.
- Com vida baixa, ele piora mais: a luta fica mais longa, e cada vez a mais é uma chance a mais de morrer.
- **O que sobra é a proteção de um tiro só:** não há situação medida em que ele seja a melhor escolha.

### 13.5 Recomendações

| Habilidade | Classificação | Recomendação |
|---|---|---|
| Drenar Vida | **Função útil demonstrada**: sustentar contra vivos quando ferido; lutas longas. Armadilha contra mortos-vivos, já avisada pelo jogo | **Manter.** Mana não é o problema (termina com 35–87%): a proposta de recuperar mana não tem motivo medido. A cura sobre o dano inteiro é a regra de todo roubo de vida; se Jean quiser, o Grimório pode dizê-lo ("conta o golpe inteiro"), sem mudar número. |
| Desaparecer | **No Vale: sem vantagem relevante. Depois: função restrita, mas legítima** (abertura com crítico contra dois inimigos resistentes, ferido: +14 pontos) | **Manter.** Tirar da mira em furtividade não tem motivo medido: a parte defensiva atual (esquiva) não mostrou valor, e o que funciona é o crítico. A sinergia com a Execução fica como hipótese sem evidência. |
| Passo Ágil | **Sem vantagem relevante nas situações avaliadas** | **Ajustar**, com a menor mudança que mostrou papel (abaixo). |

**Hipóteses testadas para o Passo Ágil**, só no script (o jogo não mudou), com os mesmos roteiros e 1500 lutas:

| Variante | Arqueiro 3, ossuário, cheia: atacar 94% | Patrulheiro 4, ossuário, 45%: atacar 95% | Sombra 7, troll, 45%: atacar 60% | Sombra 7, 3 bandidos, 45%: atacar 76% | Risco de virar a ação de todo turno |
|---|---|---|---|---|---|
| Hoje (+30% por 2 turnos), no preparo | 87% | 85% | 63% | 76% | — |
| +50% por 2 turnos, no preparo | 92% | 90% | 63% (já estava no teto de 60%) | 76% | não |
| **Desvia o próximo golpe** que acertaria, por 2 turnos (um só, sem teto), no preparo | 94% | 93% | **79%** | 76% | não: usado sempre com 2+ inimigos, faz 47%, contra 76% |
| Esquiva +30% e um Disparo junto (como se não gastasse o turno), com 2+ inimigos | 95% | 95% | 60% | **81%** | **sim**: com 3 lobos, 87% contra 77% de atacar; vira o que se aperta sempre |

- **O problema concreto:** o Passo Ágil é a única resposta do Arqueiro ao golpe preparado antes da especialização, e a
  resposta defensiva das três especializações. Ele não paga o turno em nenhum encontro medido. Esquiva por chance,
  mesmo maior, não resolve: quem ganha é sempre atacar.
- **A menor mudança que mostrou papel:** trocar a chance pelo **desvio de um golpe**.
  - O próximo golpe esquivável que acertaria o herói nas duas vezes seguintes dos inimigos erra. Um só, e o teto de
    esquiva não conta.
  - Custo (6 de Foco), duração e nome iguais.
- **Papel que ela daria:** responder ao golpe preparado de **um inimigo forte sozinho**. Contra o troll, ferido, 60% →
  79%. O troll, o mercenário, o ent, o golem, o cavaleiro sombrio e a abominação têm o Golpe Esmagador no mundo gerado.
- **O que ela não faria:**
  - **No Vale** continua sem vantagem: no ossuário empata, e com o arqueiro 3 ferido piora (19% contra 40%). Ali, o que
    resolve é matar mais rápido.
  - **Contra grupos** não muda nada.
  - **Usada todo turno**, piora a luta: não vira a melhor ação de todo turno.
- **Riscos:**
  - É uma regra nova de golpe: um estado que se gasta ao evitar um golpe, como a barreira se gasta ao absorver.
  - Muda a ficha e o Grimório das três especializações do Arqueiro.
  - Mexe nas lutas do robô de `tests/equilibrio`, que usa o Passo Ágil diante do golpe preparado. O gabarito não muda:
    o arqueiro do robô não passa do nível 2.
  - O teto de esquiva (60%) deixa de valer para esse golpe.
- **Como verificar:**
  - os mesmos roteiros, antes e depois, no Vale e nos encontros do nível 7, incluindo mercenário e guardião, que esta
    avaliação não mediu com a variante;
  - "Passo no preparo" melhor que atacar só contra um inimigo forte sozinho;
  - "Passo com 2+" e "Passo no 1º turno" piores que atacar em todo encontro;
  - o equilíbrio do Patrulheiro e do Sombra antes e depois.
- **Rejeitada:** não gastar o turno (a última linha da tabela). Rende, mas vira a ação de todo turno.

### 13.6 A próxima implementação

**Uma só, se Jean quiser continuar a P2:** o desvio do Passo Ágil (13.5). **Validado e rejeitado na seção 14.**

- Drenar Vida e Desaparecer já cumprem funções e ficam como estão.
- Se Jean preferir não mexer no Passo Ágil, a parte da P2 sobre estes três botões pode ser encerrada. Ele fica
  registrado como sem vantagem relevante, e a decisão vai para a proposta de preparação de habilidades (fora da E5).

### 13.7 Limites

- **Roteiros fixos:** uma pessoa varia mais.
  - Uma política que mistura Barreira, Drenar e servo pode render mais que as medidas.
  - O teste de "ferido" começa a luta ferido, em vez de chegar lá dentro dela.
- **Herói:** um só por nível, com equipamento mediano, sem poções e sem Meditar.
- **Aliado:** só Morel; Odette (cura) e Yara não foram medidas.
- **Guardiã da capela:** fora; o rito tem regras próprias.
- **Variantes do Passo Ágil:** uma semente só, de 1500 lutas. O ganho contra o troll (+19) passa do ruído, mas precisa
  da verificação de 13.5 antes de qualquer decisão.

## 14. Validação do desvio do Passo Ágil e fechamento da E5 (sobre a 1.59.0)

**Decisão: o desvio não entra no jogo.** Ele faz o que se propôs (responder ao golpe preparado), mas usado repetidamente
vira a ação padrão contra inimigos sozinhos. Pelo critério de Jean, a avaliação se encerra com os resultados, sem outra
mecânica nesta entrega. O Passo Ágil continua como era (+30% de esquiva por 2 turnos). Drenar Vida e Desaparecer ficam
como estão.

### 14.1 Resultados medidos

**Regra validada**, a pedida por Jean:

- custa 6 de Foco e gasta o turno;
- desvia o próximo golpe esquivável que acertaria o herói, durante dois turnos pela contagem dos estados;
- evita um golpe só, não acumula ao reaplicar e não traz o antigo +30%;
- a esquiva natural vem antes e não gasta o desvio.

**Método:**

- Os roteiros da seção 13: atacar o mais fraco; Passo Ágil quando alguém prepara; Passo Ágil sempre que não está
  valendo ("repetido").
- Sementes novas e 1200 lutas por linha, pelo combate de verdade (IA dos inimigos).
- Antes (a regra de hoje) e agora (o desvio), na mesma régua.
- **Heróis em condições reais**, sem talentos e com o equipamento mediano da seção 13:
  - Arqueiro 3 com Morel;
  - Patrulheiro 4 e 7 com o lobo;
  - Patrulheiro 7 com o lobo e Morel;
  - Sombra 7 sozinho.
- **Encontros:**
  - do Vale: ossuário, sarilho e 3 lobos;
  - de depois: troll, mercenário sozinho, mercenário e bandido, o guardião da floresta (o 2º do catálogo, que tem o
    golpe preparado) e 3 bandidos.
- **O guardião** entrou com limite de 200 turnos (300 lutas por linha): passou disso, conta como **impasse**, porque com
  o desvio repetido algumas lutas não acabam.

**Vitórias:**

| Herói, encontro | Vida inicial | Atacar | Passo no preparo: hoje → desvio | Passo repetido: hoje → desvio (turnos) |
|---|---|---|---|---|
| Arqueiro 3 com Morel, ossuário | 45% | 85% | 77% → **90%** | 61% → **93%** (10,9) |
| Arqueiro 3 com Morel, sarilho | 45% | 86% | 81% → **93%** | 66% → **94%** (11,9) |
| Arqueiro 3 com Morel, 3 lobos | 45% | 54% | 54% → 54% | 30% → 30% |
| Patrulheiro 4 com o lobo, ossuário / sarilho / lobos | 45% | 99% / 100% / 98% | sem mudança | 95% → 91% / 96% → 90% / 91% → 29% |
| Patrulheiro 7 com o lobo, troll | 45% | 71% | 70% → **86%** | 52% → **100%** (12,6) |
| Patrulheiro 7 com o lobo, mercenário + bandido | 45% | 90% | 88% → 93% | 73% → 95% (12,9) |
| Patrulheiro 7 com o lobo, guardião | cheia | 15% | 19% → 28% | 7% → **83%** (100 turnos; 16% de impasse) |
| Patrulheiro 7 com o lobo, 3 bandidos | 45% | 76% | 76% → 76% | 61% → 34% |
| Patrulheiro 7 com o lobo e Morel, troll | 45% | 85% | 83% → 93% | 79% → **100%** |
| Patrulheiro 7 com o lobo e Morel, guardião | 45% | 6% | 6% → 11% | 1% → **63%** (113 turnos; 35% de impasse) |
| Sombra 7 sozinho, troll | 45% | 42% | 50% → **70%** | 31% → **100%** (16,8) |
| Sombra 7 sozinho, mercenário sozinho / + bandido | 45% | 97% / 71% | 97% → 99% / 70% → 78% | 83% → 100% / 51% → 81% |
| Sombra 7 sozinho, guardião | 45% | 1% | 1% → 1% | 0% → **91%** (87 turnos; 9% de impasse) |
| Sombra 7 sozinho, 3 bandidos | 45% | 55% | 55% → 55% | 41% → 22% |

De vida cheia, no Vale e contra o mercenário, atacar e responder à preparação ganham 99–100% antes e depois. Repetir o
Passo com desvio contra lobos ou bandidos cai para 50–56%.

**Leitura:**

- **O papel proposto existe.** Responder à preparação com o desvio rende mais que atacar e mais que o Passo de hoje:
  - contra o troll, +8 a +28 pontos sobre atacar;
  - contra o guardião, +5 a +13 (de vida cheia ou com aliado; ferido e sozinho, nada);
  - no Vale, só com aliado e ferido: +5 a +7.
  - Contra grupos de inimigos fracos não muda nada: o desvio se gasta no primeiro golpe que vier.
- **Mas vira a ação padrão contra um inimigo sozinho.**
  - Com um atacante, há um golpe por rodada, e o desvio pega esse golpe. O Passo custa 6 de Foco e o Foco volta 5 por
    turno, então o herói desvia quase toda rodada e ataca só de vez em quando.
  - Contra o troll, repetir chega a 100% de vitórias; contra o guardião, a 83–91%, contra 1–15% atacando.
  - As lutas passam de 80 a 110 turnos, e de 9% a 35% delas não acabam: o guardião regenera mais do que apanha.
  - Com Morel e ferido, repetir também ganha no Vale (93% contra 85% no ossuário): o herói segura os golpes enquanto o
    aliado luta.
- **Conclusão:** o ganho em situações apropriadas se sustenta, mas a condição "sem virar a ação padrão" não. Pelo
  pedido de Jean, a mudança não entra.

### 14.2 Conferência técnica (feita na cópia de trabalho, depois descartada)

A regra foi implementada e conferida antes da decisão. Nada disso está no repositório.

- **Motor:**
  - um estado "desvio" no catálogo e uma etapa nova do golpe ("desvia"), depois da esquiva natural e da imunidade, só
    em golpe esquivável;
  - o fim sem uso avisado no registro e na carta.
- **Tela:** "desviou!" na carta e o ícone com os turnos.
- **10 testes passaram:**
  - consumo uma vez;
  - esquiva natural sem consumo;
  - expiração;
  - reaplicação sem acumular;
  - golpe preparado;
  - ataque não esquivável;
  - vários golpes numa salva;
  - dano por turno;
  - herói atordoado;
  - aliado não gasta.
- **Navegador, em 1500 e 1280 px:**
  - o golpe preparado desviado;
  - outro esqueleto, agindo antes, gasta o desvio, e o golpe preparado acerta.
- **Duração real:** aplicado na vez do herói, o estado vale na vez inteira dos inimigos naquele turno e na do turno
  seguinte; some no começo da segunda vez seguinte do herói. São duas rodadas completas dos inimigos, não duas ações
  individuais. Essa contagem é a mesma de todos os estados do herói, incluindo o Passo de hoje.
- **Um achado do motor:** a luta não tem limite de turnos. Hoje nenhuma habilidade produz uma luta sem fim. Qualquer
  defesa garantida e repetível pode produzir, e isso vale para propostas futuras.

### 14.3 A travessia do Vale: a guardiã por caminho

Para o critério "três classes atravessam a região", a guardiã da capela (Ilse, nível 4) foi medida na versão atual pelo
método da E3 (1.53.0).

- Seis heróis por especialização e nível, com talentos e equipamento sorteados, um membro da comitiva e as poções do
  começo.
- Robô da arena, caminho "destruir" (a luta inteira); 150 lutas por linha.

| Especialização | Nível 4 | Nível 5 |
|---|---|---|
| Paladino | 83% | 100% |
| Berserker | 81% | 96% |
| Patrulheiro | 85% | 97% |
| Necromante | 54% | 98% |
| Piromante | 22% | 66% |
| Sombra | 26% | 50% |

- **Leitura:** as três classes passam; cada uma tem ao menos um caminho que passa no nível 4 ou 5.
- **Os mais duros:** Sombra e Piromante. Isso já estava registrado (COMO_CRIAR: "Sombra, Piromante e Necromante as mais
  duras").
- **O que alivia:** o rito, que encerra a luta na metade, e jogar melhor que o robô.
- **O que não serve de régua:** sem talentos e sem poções, com um herói só, a mesma guardiã fica em 0–19%. Ninguém chega
  lá assim no jogo.

### 14.4 O critério mínimo da E5

**"Pronto: três classes atravessam a região; seis caminhos avaliados em cenários direcionados."**

- **Três classes atravessam a região:** atendido tecnicamente.
  - As salas da capela com golpe preparado (seção 10), as lutas do Vale (seção 13) e a guardiã (14.3).
  - O robô e os roteiros são a régua; a validação de Jean jogando fica registrada à parte, como na E4.
- **Seis caminhos avaliados em cenários direcionados:** atendido.
  - Paladino, Berserker e Piromante: as sequências e fichas das seções 4 e 9, a Combustão conferida contra a execução
    (seção 11) e a guardiã (14.3).
  - Patrulheiro: o Tiro Duplo (seção 12) e o Passo Ágil (seções 13 e 14).
  - Sombra e Necromante: as lutas inteiras da seção 13.
- **A E5 está concluída tecnicamente.** Falta Jean jogar: a P1 (o golpe preparado), a P3 (a encruzilhada e o
  Grimório), o Tiro Duplo e os seis caminhos.

### 14.5 Adiado, sem ser requisito da E5

- **Passo Ágil:** segue sem vantagem relevante.
  - Uma versão futura precisa limitar a repetição: recarga, ou não reaplicar logo depois de gastar.
  - Precisa também ser medida com o mesmo roteiro "repetido" e com um limite de turnos.
- **Desaparecer:** a sinergia com a Execução fica como hipótese sem evidência; tirar da mira em furtividade, como
  proposta sem motivo medido.
- **Drenar Vida:**
  - o Grimório pode dizer que a cura conta o golpe inteiro, sem mudar número;
  - recuperar mana, como proposta sem motivo medido.
- **Equilíbrio:** Sombra e Piromante contra a guardiã do Vale no nível 4. É assunto de equilíbrio, não autorizado
  nesta etapa.
- **Preparação de habilidades:** o excesso de botões, o Golpe Pesado no Paladino.
- **Limite de turnos no combate:** só se alguma mecânica futura permitir luta sem fim.
- **Tiro Duplo:** as limitações da seção 12.6.

