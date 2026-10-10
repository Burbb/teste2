# 14 — E5: diagnóstico das três classes e das seis especializações

Revisão 1 — 10/10/2026. Jogo na versão 1.56.0 (commit `adaa93a`). **Entrega só de análise e design:** nenhum código,
atributo, habilidade, talento, item ou save foi alterado.

**Atualização 1.57.0:** a P1 foi implementada (seção 10). As seções 1 a 9 continuam como o diagnóstico da 1.56.0; onde
a 1.57 mudou o que elas dizem (o golpe preparado no Vale), a seção 10 diz o que vale agora.

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
- **Limitação:** em 1280 px, a faixa de ação de outro inimigo (por exemplo, "Investida") pode cobrir a linha do aviso por
  até 1,5 s logo que a vez chega. É a faixa comum de todas as ações, que some sozinha; depois o aviso fica limpo.

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

- **P3:** a encruzilhada e o Grimório que explicam.
- **P2:** um papel para cada botão dominado. Não autorizada; a ressalva do começo deste documento vale para ela.
- O Arqueiro sem como interromper antes da especialização é um fato do conteúdo de agora, não um defeito a corrigir
  nesta entrega.

