# 27 — A forja: especificação do sistema (reforço, materiais, encantamento, transferência)

Documento de referência da etapa 4. Ele descreve o sistema inteiro como está hoje, sem precisar da conversa nem dos
históricos de protótipo. Atualizado em 28/10/2026 (18ª versão do protótipo), conferido contra o código do
protótipo (`ferramentas/prototipos/reforco`: `regras.py`, `encanto.py`, `demo.py`, `tela/reforco.js`) e o de
produção (`rpg/sistemas/servicos.py`).

**Fonte única.** As regras vigentes estão aqui. O [25](25-ETAPA4-REFORCO-E-ENCANTAMENTO.md) guarda a pesquisa, o
debate e as rodadas, e aponta para cá. O [LEIA-ME do protótipo](../ferramentas/prototipos/reforco/LEIA-ME.md) guarda o
que mudou em cada versão. Se algum dos dois divergir deste documento, vale este.

**Como ler as marcas:**
- **[Aprovado]**: decisão do Jean.
- **[Protótipo]**: implementado e testado no protótipo.
- **[Provisório]**: número ou hipótese para avaliar jogando.
- **[Produção]**: o que o jogo tem hoje.
- **[Adiado]**: fica para depois.
- **[Substituído]**: decisão antiga que não vale mais.

**Estado da etapa 4:** aberta. Nada do protótipo foi integrado. O equilíbrio está em avaliação: o Jean quer julgar a
dificuldade jogando uma campanha mais completa.

---

## 0. O que existe em produção [Produção]

O ferreiro do jogo (`Servicos.ferreiro`, `rpg/sistemas/servicos.py`) reforça só a arma, o peito e o apoio do herói.
Cada passo melhora uma linha: Ataque (Poder no mago), Defesa no peito, e no apoio a linha da classe. O passo soma 12% do
valor (no mínimo 1), vai até +5, é garantido e custa 40 × (nível + 1)^1,6 de ouro. Não há materiais, gravação,
desmontagem nem transferência. **Tudo o que segue é o protótipo**, que substituirá esse ferreiro quando integrado.

## 1. Reforço

### 1.1 Elegibilidade [Aprovado]
**Todo espaço de equipamento** recebe reforço: arma, peito, cabeça, mãos, pernas, pés, apoio (escudo, tomo e aljava),
anel e amuleto. As peças podem ser do herói, dos companheiros ou da bolsa. **Classe e nível restringem vestir, não o
serviço [Aprovado, 16ª]:** a peça que ninguém do grupo sabe usar (a arma de arqueiro num grupo sem arqueiro) recebe
reforço, com a prévia calculada da própria peça; vestir continua recusado. A peça de um companheiro fora do grupo é
recusada. **[Substituído]** Antes, só arma, peito, escudo e tomo; e, até a 15ª, a peça sem usuário era recusada
("Ninguém do grupo usa peças de …").

### 1.2 O que cresce [Aprovado: a peça inteira; Provisório: a fórmula]
**A peça inteira:** todas as linhas, da base e dos afixos. O reforço não mexe nas gravações. **[Substituído]** a
escolha Fio ou Runas da arma do Guerreiro e o reforço só da linha da base.

**Correção matemática** (o que tinha de mudar, independente do equilíbrio):
- **Forma fechada.** O ganho do +N sai sempre da peça original (`bonus_base`), sem passar pelos níveis do meio. Cair e
  subir de novo dá exatamente o número do nível, sem deriva (testado com quedas e subidas em sequência).
- **Todo sucesso melhora a peça de verdade [Aprovado: a regra, 16ª].** Até a 15ª, o ganho de cada linha era
  arredondado a inteiro e uma linha pequena passava passos sem subir: a conta tinha ganho em todo passo (nenhum passo
  zerado na varredura do gerador), mas o arredondamento escondia um quarto a um terço dos passos de acessórios, elmos,
  luvas e botas (o Cajado de Ferro do +10 ao +11: Poder 8,6 → 9,2, os dois 9). Agora:
  - **Precisão de cada propriedade** (`regras.PRECISAO`) [Protótipo]: Ataque, Poder, Defesa, Agilidade, Espinhos,
    Vida por turno e Vida por abate com uma casa; Crítico e Roubo de vida em décimos de ponto; Vida e Mana inteiras
    (reservas de pontos). A tela mostra a casa só quando existe ("2,7", "5").
  - **Garantia:** um passo em que nenhuma linha mudaria entrega o próximo degrau à linha mais perto dele; nunca mais de
    um degrau à frente da conta (testado em todos os espaços). Só peças de Vida e Mana chegam a usá-la.
  - **Não é +1 em toda linha:** cada linha cresce na sua proporção; uma linha pequena sobe décimos.
  - **A cadeia:** a casa chega aos atributos do herói e dos companheiros e à luta (dano, defesa e esquiva usam o número
    com a casa). Espinhos, Vida por turno e Vida por abate são pontos de vida inteiros: a fração se acumula a cada
    disparo (2,6 por turno cura 2, 3, 3, 2, 3…). Sem peça fracionária, os números do jogo são os de antes. [Protótipo:
    `demo.decimais_na_luta`; na integração, levar para `entidades` e `comitiva`.]
  - **Peça toda no teto:** nenhuma do gerador chega (o teto é por peça). Se chegar, o reforço é recusado sem cobrar
    ("Sem ganho: Crítico no máximo desta peça."). **[Proposta, não implementada]** a peça nessa situação passa a crescer
    pela linha fixa mais próxima da base (Ataque na arma, Defesa no resto), sem elevar o teto de %.
  - Só a linha principal da arma sobe ao menos 1 por passo, e só do +1 ao +4 (a faixa aprovada).
- **Meio para baixo nos valores pequenos.** O arredondamento, na precisão da linha, é com o meio para baixo (0,25 →
  0,2; 1,5 → 1 numa linha inteira). Com o meio para cima, uma aljava de Agilidade 1 saltava.
- **Porcentagens com teto.** Crítico e roubo de vida crescem por soma (abaixo), sem passar do teto por peça. O teto
  de crítico do personagem (60%) continua no motor. As peças não têm resistências hoje.
- **Sem regra especial por espaço.** Saiu o dobro que os apoios tinham do +1 ao +4: o afixo se mistura à base na
  mesma linha, e o Tomo da Coruja ia de Poder 5 a 13 já no +4.

**A fórmula** [Provisório]. Um + vale "a mesma peça alguns níveis acima". Os passos valem 1,5 nível de peça do +1 ao
+4, 1 do +5 ao +8 e 0,75 do +9 ao +12; L(N) é a soma até +N, e o +12 soma 13.
- Linha fixa de valor v numa peça de nível n: ganho(N) = arredonda(v ÷ escala(n) × 0,75 × L(N)) na precisão da
  linha, com escala(n) = 1,5 + 0,75 × n, a do gerador.
- Crítico e roubo de vida: + 0,25 ponto por nível de peça, como os afixos do gerador. O teto por peça é 15% de
  crítico e 10% de roubo de vida.

**Exemplos reais do catálogo** (`simular.py`), comparados com a substituta, uma base comum do gerador 6 e 12 níveis
acima, no +0:

| Peça | +0 | +4 | +8 | +12 | Substituta (base comum do gerador), nível +6 / +12 |
|---|---|---|---|---|---|
| Martelo Enferrujado (nível 1, comum) | Ataque: 2 | 6 | 8,7 | 10,7 | Machado de Aço: 7; Machado Rúnico: 14 |
| Martelo de Aço (nível 6, comum) | Ataque: 6 | 10,5 | 13,5 | 15,7 | Machado Rúnico: 13; Machado Rúnico: 18 |
| Pranto Sangrento (nível 12, raro) | Ataque/Crítico/Defesa: 12/6/5 | 17,1/7,5/7,1 | 20,6/8,5/8,6 | 23,1/9,2/9,6 | Machado Rúnico: 18/0/0; Machado Rúnico: 23/0/0 |
| Grimório de Aço do Vampiro (nível 6, incomum) | Poder/Roubo de vida: 6/4 | 10,5/5,5 | 13,5/6,5 | 15,7/7,2 | Varinha Rúnica: 13/0; Varinha Rúnica: 18/0 |
| Arco Longo de Ferro (nível 4, comum) | Ataque/Agilidade: 3/1 | 7/2 | 8/2,7 | 9,5/3,2 | Arco Longo Temperado: 8/2; Arco Longo Rúnico: 13/4 |
| Cota de Malha de Ferro (nível 1, comum) | Defesa/Vida: 1/4 | 3/12 | 4,3/17 | 5,3/21 | Peitoral de Aço: 5/14; Peitoral Rúnico: 9/27 |
| Cicatriz da Fenda (nível 6, raro) | Defesa/Vida/Crítico: 7/29/4 | 12,2/51/5,5 | 15,7/65/6,5 | 18,4/76/7,2 | Peitoral Rúnico: 9/25/0; Peitoral Rúnico: 13/36/0 |
| Broquel de Aço (nível 3, comum) | Defesa/Vida: 1/2 | 2,2/4 | 3/6 | 3,6/7 | Escudo Temperado: 3/5; Escudo Rúnico: 5/8 |
| Escudo Temperado da Águia (nível 8, incomum) | Defesa/Vida/Agilidade: 3/4/4 | 4,8/6/6,4 | 6/8/8 | 6,9/9/9,2 | Escudo Rúnico: 5/7/0; Escudo Rúnico: 7/10/0 |
| Tomo da Coruja (nível 6, incomum) | Poder/Mana: 5/5 | 8,7/9 | 11,2/11 | 13,1/13 | Tomo: 4/12; Tomo: 5/18 |
| Aljava Rasgada (nível 2, comum) | Agilidade/Ataque: 1/1 | 2,5/2,5 | 3,5/3,5 | 4,2/4,2 | Aljava Reforçada: 1/1; Aljava Rúnica: 3/3 |
| Cicatriz Sangrenta (nível 7, raro) | Agilidade/Ataque/Espinhos/Regeneração/Roubo de vida: 1/1/6/2/4 | 1,7/1,7/10/3,3/5,5 | 2,1/2,1/12,7/4,2/6,5 | 2,4/2,4/14,7/4,9/7,2 | Aljava Rúnica: 3/3/0/0/0; Aljava Rúnica: 4/4/0/0/0 |
| Barbuta de Ferro (nível 4, comum) | Defesa/Vida: 1/2 | 2/4 | 2,7/5 | 3,2/6 | Elmo Temperado: 2/5; Elmo Rúnico: 3/8 |
| Luva de Seda de Lã Negra dos Espinhos (nível 6, incomum) | Poder/Defesa/Espinhos: 1/1/6 | 1,7/1,7/10,5 | 2,2/2,2/13,5 | 2,6/2,6/15,7 | Luva de Seda Rúnica: 2/1/0; Luva de Seda Rúnica: 3/1/0 |
| Aro do Carniceiro (nível 3, incomum) | Vida por abate: 5 | 11 | 15 | 18 | Anel do Carniceiro: 9; Anel do Carniceiro: 14 |
| Brasa Faminta (nível 8, raro) | Agilidade/Crítico: 4/4 | 6,4/5,5 | 8/6,5 | 9,2/7,2 | Talismã do Carniceiro: 0/0; Talismã do Carniceiro: 0/0 |

Na 15ª, os mesmos +12 eram inteiros (a Barbuta de Ferro 3/6, a Brasa Faminta 9/7): a conta não mudou, só deixou de
esconder a fração.

**Hipótese de equilíbrio** (separada da correção):
- Uma peça do começo no +12 fica abaixo da base 12 níveis acima, que ainda pode ser reforçada: o Martelo Enferrujado
  +12 tem Ataque 11, o Machado Rúnico do nível 13 tem 14.
- Uma peça melhor ganha mais por passo (o Pranto Sangrento). Uma boa peça dura, mas não vence tudo o que vem depois.
- **A conferir jogando:** as peças com muitos afixos fortes (anéis de Vida por abate, luvas de Espinhos) crescem
  todas as linhas.

### 1.3 Chances, custos e falha [Provisório; Aprovado: as regras]
**Regras aprovadas:**
- o +1 é garantido;
- sucesso sobe um nível; falha desce um, até +0;
- a peça nunca quebra;
- cada tentativa cobra uma vez o custo do nível pretendido, dê certo ou não;
- limite +12, sem proteção, garantia acumulada nem destruição.

| Tentar | Chance (comum / incomum / raro / lendário) | Ouro | Fragmentos |
|---|---|---|---|
| +1 | 100% | 20 | 1 |
| +2 | 85 / 81 / 77 / 73% | 35 | 1 |
| +3 | 70 / 66 / 62 / 58% | 55 | 2 |
| +4 | 55 / 51 / 47 / 43% | 80 | 2 |
| +5 | 52 / 50 / 48 / 46% | 110 | 3 |
| +6 | 50 / 48 / 46 / 44% | 145 | 3 |
| +7 | 48 / 46 / 44 / 42% | 185 | 4 |
| +8 | 46 / 44 / 42 / 40% | 230 | 4 |
| +9 | 44 / 42 / 40 / 38% | 280 | 5 |
| +10 | 42 / 40 / 38 / 36% | 335 | 5 |
| +11 | 40 / 38 / 36 / 34% | 395 | 6 |
| +12 | 38 / 36 / 34 / 32% | 460 | 6 |

O ouro tem o desconto ou acréscimo da reputação. A raridade tira 4/8/12 pontos até o +4 e 2/4/6 acima. **Não
recalibrar** por causa das simulações (decisão do Jean): a dificuldade será julgada jogando. A simulação fica em
`simular.py` (mediana do +12: 164 tentativas num comum, 676 num lendário) e no LEIA-ME.

### 1.4 Recuperação
Valem só os níveis que a peça conserva; as tentativas perdidas não contam.
- **Desmontar** (só peças da bolsa) devolve metade dos fragmentos nominais desses níveis, arredondada para cima, mais
  o material da própria peça: comum 0, incomum 1, raro 2, lendário 3.
- **Vender** devolve 25% do ouro nominal desses níveis, somado ao preço da peça.

Testado: qualquer sequência de tentativas seguida de desmontar ou vender deixa o grupo com menos do que gastou.

## 2. Materiais

### 2.1 Armazenamento [Protótipo]
Os materiais são pilhas do grupo, fora dos 12 espaços da bolsa, de até 99 cada. Ficam no save (`materiais`) e
aparecem na seção "Materiais" do Inventário. São dois tipos: **Fragmento de Têmpera** (reforço) e **Essência de
<efeito> I, II ou III** (gravação), 18 essências no total.

### 2.2 Fontes no protótipo [Protótipo; Provisório: as chances]

| Fonte | Fragmentos | Essências |
|---|---|---|
| Luta comum (o saque real, `saque_de_combate`) | 25% de chance de 1 (+15% por elite) | 6% (+20% por elite): a da criatura, no tier do nível dela |
| Chefe | 2 sempre (3 do nível 6 em diante) | 1 sempre, da criatura, **um tier acima** |
| Baú | 50% de chance de 1 | 25%: uma qualquer, no tier do nível do herói |
| Desmontagem | metade dos fragmentos nominais e o material da peça (1.4) | as gravações se perdem |
| Recompensa de teste (início da demonstração) | 12 (1 com os casos) | 2 de cada essência I |

**Tier pelo nível do conteúdo:** I até o nível 4, II do 5 ao 8, III do 9 em diante.

**Fonte identificável** (quem quer um efeito sabe o que caçar):

| Essência | Criaturas |
|---|---|
| Brasa | cão infernal, cultista, caído, xamã caído |
| Carrasco | bandido, mercenário, cavaleiro sombrio, carniçal |
| Eco | espectro, bruxa do brejo, cria do vazio, harpia |
| Vigília | golem, ent jovem, troll, esqueleto |
| Revide | javali, grifo, abominação, rato, aranha |
| Geada | lobo gélido, afogado, sapo, sanguessuga, lobo |

O registro de cada material (`registrar`, evento "material") guarda a origem: luta, chefe, baú, teste. Os botões de
teste da faixa são separados.

### 2.3 Planejado [Adiado]
- Quests e contratos como fonte de essências e fragmentos, sem expansão narrativa neste lote.
- Tiers superiores ligados ao conteúdo avançado da campanha ampliada.
- Os números das fontes dependem da campanha ampliada e estão em definição.
- Sem fusão de essências (decisão desta rodada).

## 3. Encantamento (gravação)

### 3.1 Sulcos [Aprovado; Provisório: a distribuição]
Cada peça gravável (arma, peito, escudo, tomo) nasce com 1 a 3 **sulcos**. O número é sorteado uma vez, pela própria
peça (a semente vem do nome, nível, raridade e base, sem gastar o sorteio do jogo). Fica guardado nela: não muda ao
salvar, carregar, trocar de dono ou abrir uma ficha.

| Raridade | 1 sulco | 2 sulcos | 3 sulcos |
|---|---|---|---|
| Comum | 75% | 25% | — |
| Incomum | 50% | 40% | 10% |
| Raro | 25% | 50% | 25% |
| Lendário | — | 50% | 50% |

As outras peças (cabeça, mãos, pernas, pés, aljava, anel, amuleto) recebem reforço, mas não gravação. **[Provisório]**

### 3.2 Tiers, repetição e limite [Aprovado: o modelo; Provisório: os valores e os limites]
- **Tiers:** Essência I, II e III são **versões de potência diferente do mesmo efeito**. Cada uma tem o seu valor (a
  tabela da seção 4) e ocupa um sulco.
- **Repetição:** permitida na mesma peça e entre peças. Repetir soma **só a propriedade que cresce** daquela essência
  (a chance da Brasa, do Revide e da Geada; a magnitude do Carrasco, do Eco e da Vigília), até um **limite próprio de
  cada efeito**. O gatilho, o alvo, a duração, o dano do golpe e a frequência não mudam com a repetição.
- **Uma vez por personagem:** cada efeito dispara uma vez, pela soma das peças que **o próprio personagem veste**
  (não uma vez por cópia). A bolsa e as peças dos outros não contam. Os limites de ativação continuam (por rodada, por
  luta, sem reação em cadeia, sem recuperação sem fim).
- **Exemplos:**
  - Brasa I sozinha: 20% de chance; Brasa II: 28%; Brasa III: 36%;
  - duas Brasas I: 40%; Brasa II + Brasa I: 48%;
  - Brasa III + Brasa III: 72%, que vira 60% (o limite da Brasa);
  - Eco II na arma e Eco III + Eco II no tomo de Odette: 15 + 20 + 15 = 50%, que vira 35% (o limite do Eco).
- **A ficha da peça mostra o que a peça fornece** (as gravações dela somadas, até o limite). O total de quem veste
  aparece na prévia do Encantar, quando outra peça dele também soma ou o limite corta; não substitui a descrição.
- **[Substituído]** O modelo da 13ª e 14ª versões: tiers que contribuíam com 1, 2 e 3 níveis de um efeito único, nível
  total de 1 a 5 por personagem e teto de 5 ("Eco 4 em Jean"). Não existe mais nível de efeito.

### 3.3 Gravar, substituir, perder [Aprovado]
- **Gravar:** consome 1 essência do tier escolhido e 30 de ouro, com reputação. Nunca falha.
- **Substituir:** gravar num sulco ocupado custa o mesmo e apaga a gravação anterior. A essência antiga não volta e
  não há extração. A tela pede confirmação e diz o que sai.
- **A mesma gravação:** a mesma essência no mesmo tier sobre ela mesma (Carrasco III sobre Carrasco III) não muda
  nada; o motor recusa sem cobrar ("Já gravado."), e a tela mostra o motivo no lugar do botão. Outro tier da mesma
  essência é uma substituição normal.
- **Peça vestida e requisito:** se a gravação deixaria a peça acima do nível de quem a veste, o motor recusa sem cobrar
  ("Requer nível 9"; a tela mostra "Nível 9" em vermelho no "Requer:" do pé, e o nível de quem veste na dica). Na
  bolsa, a peça pode ser preparada para depois (a prévia diz "A peça passa a requerer nível 9"). Nada é
  tirado do corpo sozinho, e ninguém fica com o benefício sem cumprir o requisito.
- **Remover sem substituir [Candidata, 18ª]:** escolher um sulco ocupado e remover a gravação; o sulco fica vazio.
  A essência se perde e nada volta (nem a essência, nem material). Nesta candidata, não custa nada. A confirmação
  identifica a essência e a perda ("Remover? Brasa I se perde."). Um pedido só remove uma vez (o clique duplo e a
  tecla segurada não repetem; o motor recusa o pedido repetido e a gravação que mudou desde que a tela a mostrou).
  Depois, tudo segue as gravações que ficaram: o efeito somado em quem veste, os limites da soma, o requisito de nível
  da peça (que pode cair), a ficha, as prévias, os sulcos e as bordas de luz das gravações. Não mudam o reforço, os
  atributos da peça nem as outras gravações.
- **Peça e dono:** a gravação é da peça e vai com ela quando ela troca de dono.
- **Desmontar** perde as gravações. A confirmação lista quais ("Perde as gravações: Brasa II, Eco I.").
- **Compatibilidade por essência:**
  - Brasa e Carrasco: arma;
  - Eco: arma, tomo e escudo;
  - Vigília: peito, escudo e tomo;
  - Revide: peito e escudo;
  - Geada: peito.

### 3.4 Requisito de nível [Aprovado: as regras; Provisório: a tabela]
- **Dois números diferentes:** o **nível da base** (`nivel` no item) é o nível em que a peça foi gerada e decide a força
  dela (a escala, o material); o **requisito** é o nível mínimo para usá-la.
- **Requisito do equipamento:** o nível da base menos 1, nunca menos de 1. O jogo gera o achado no nível do herói ou um
  acima (`gerar_equip(..., g.j.nivel + 1)`), então o achado de agora serve agora; uma peça de uma região mais alta
  espera. Exemplos do protótipo: a espada inicial (base 2) pede o 1; a substituta de base 7 pede o 6.
- **Requisito de cada tier:** Essência I, nível 1; II, nível 5; III, nível 9. É a mesma faixa do conteúdo que dá cada
  tier (`tier_do_nivel`: I até o 4, II do 5 ao 8, III do 9); o chefe dá um tier acima, que fica para depois.
- **A peça gravada** pede o maior entre o requisito dela e o das gravações. O reforço sozinho não muda o requisito.
- **Quem veste:** o nível real de quem vai vestir, o herói ou o companheiro (no jogo, os companheiros crescem com o
  nível do herói). Abaixo do requisito, vestir é bloqueado com o motivo curto ("Requer nível 9.") em todos os caminhos:
  o Inventário (clique duplo, menu, arrastar, troca entre personagens), o achado ("Guardar na mochila (requer nível
  7)"), o mercado e a troca de arma na luta.
- **Não muda:** as regras de evolução dos companheiros; quem já veste uma peça acima do nível (um save antigo) não a
  perde sozinho.

## 4. As seis essências [Provisório: os valores e os limites]

Cada essência tem um valor por tier e um limite para a soma de quem veste. Só a propriedade da tabela cresce; o
gatilho, o alvo, a duração e a frequência ficam. "Rodada" é quando todos agiram (`cb.turno` no motor); "turno" é a vez
de um combatente. Nenhum efeito secundário dispara outro: o tique de uma Queimadura, um Revide ou outra reação não
aciona gravação nenhuma. Invocações não vestem peças e não contam como portador.

| Essência | O que soma | I | II | III | Limite da soma |
|---|---|---|---|---|---|
| Brasa | chance de Queimadura | 20% | 28% | 36% | 60% |
| Carrasco | dano a mais | 15% | 22% | 30% | 50% |
| Eco | recurso por abate | 10% | 15% | 20% | 35% |
| Vigília | barreira (% da vida) | 8% | 11% | 14% | 25% |
| Revide | chance de revidar | 12% | 18% | 24% | 40% |
| Geada | chance de congelar | 12% | 18% | 24% | 40% |

Critério das tabelas: o tier maior vale mais; uma gravação sozinha nunca chega ao limite; três do tier III sempre
passam dele (o limite corta a repetição extrema). O tier I fica perto do antigo nível 1 e o III perto do antigo nível
3; o limite fica perto do antigo nível 5.

- **Brasa** (arma):
  - **Gatilho e alvo:** um golpe do portador que acerta um inimigo; atinge esse inimigo.
  - **Efeito:** com a chance da soma, aplica 1 camada de Queimadura, até 3. O valor é 25% do maior entre Ataque e Poder
    (mínimo 2), com a duração da Queimadura do herói (2 turnos quando o portador é um companheiro).
  - **Limite:** 1 aplicação por rodada. Em área ou em golpes múltiplos, vale a primeira que pegar.
  - **Interações:** soma camadas com a Queimadura do Mago; o tique não dispara a Brasa; chefes recebem igual.
- **Carrasco** (arma):
  - **Gatilho e alvo:** cada golpe do portador num inimigo abaixo de 35% da vida.
  - **Efeito:** o dano a mais da soma.
  - **Limite:** nenhum por frequência; vale em cada alvo de um golpe em área.
  - **Interações:** multiplica com os outros bônus; não vale nos tiques nem nas reações; chefes recebem igual.
- **Eco** (arma, tomo, escudo):
  - **Gatilho e alvo:** um inimigo cai pelo golpe do portador; recupera o próprio portador.
  - **Efeito:** a porcentagem da soma da Mana, do Vigor ou do Foco máximos.
  - **Limite:** 2 vezes por luta, fixo, para não virar recurso sem fim.
  - **Interações:** cada inimigo derrubado num golpe em área conta uma vez, dentro do limite.
- **Vigília** (peito, escudo, tomo):
  - **Gatilho:** o começo da luta.
  - **Efeito:** a barreira da soma, por 3 turnos do portador.
  - **Limite:** 1 vez por luta.
  - **Interações:** não soma com outra barreira; vale a maior (a Aura de Proteção).
- **Revide** (peito, escudo):
  - **Gatilho e alvo:** um golpe corpo a corpo de inimigo que acerta o portador; revida em quem bateu.
  - **Efeito:** com a chance da soma, um golpe de 60% do Ataque (o dano não cresce com a repetição).
  - **Limite:** 1 resposta por golpe e **2 por rodada**, para não virar um ciclo com muitos atacantes.
  - **Interações:** o revide não aciona outro revide nem a Brasa; não responde a golpes à distância nem a tiques; um
    golpe em área que pega o portador conta como um golpe.
- **Geada** (peito):
  - **Gatilho e alvo:** um golpe corpo a corpo de inimigo que acerta o portador; congela quem bateu.
  - **Efeito:** com a chance da soma, o atacante perde a próxima vez.
  - **Limite:** 1 vez por luta.
  - **Interações:** chefes e gigantes resistem metade das vezes (a regra do Atordoado).

Os textos saem do valor de cada tier (`encanto.texto`). Exemplo: "Revide II · Ao receber um golpe corpo a corpo, 18% de
chance de revidar com 60% do Ataque. No máximo 2 vezes por rodada."

## 5. Transferência de reforço [Aprovado: as regras para testar; Provisório: o custo e a perda]

**Requisitos:**
- mesma raridade e mesmo tipo de peça;
- a operação precisa aumentar o reforço do destino; senão é recusada ("O destino não sobe: recebe +X, já tem +Y.").

**Resultado (garantido):**
- **Origem:** fica +0, mas continua existindo, com os atributos originais, os afixos, os sulcos e as gravações.
- **Destino:** recebe o nível da origem **menos 2**, que **substitui** o dele (não soma).
- **Exemplo:** origem +10 e destino +2 ficam origem +0 e destino +8.

**O que não se move:** afixos, sulcos e gravações.

**Custo:** o preço de uma tentativa do nível que o destino recebe (receber +8 custa 230 de ouro, com reputação).
Cobrado uma vez por pedido. A confirmação mostra os dois resultados e o preço.

**A brecha "reforçar a mais barata e transferir":** **não existe** no protótipo.
- O custo de uma tentativa depende só do nível pretendido, não da peça nem do espaço.
- A chance depende da raridade, e a transferência exige a mesma raridade.
- Reforçar outra peça do mesmo tipo e raridade custa o mesmo que reforçar o destino, e a transferência ainda perde 2
  níveis e cobra o preço.
- Por isso não há compensação extra. Se o custo um dia variar com a peça (o nível da peça, a base), a compensação
  passa a ser necessária: cobrar a diferença de custo nominal entre as duas.

**Sem duplicar investimento:**
- A venda e a desmontagem usam os níveis que cada peça conserva. A origem +0 não devolve nada do reforço que perdeu.
- O destino devolve só pelo nível que tem, que é menor que o da origem.
- Transferências sucessivas perdem 2 níveis a cada vez.
- Testado: a soma da venda e da desmontagem das duas peças cai depois da transferência; o mesmo pedido não cobra
  duas vezes.

## 6. Venda e desmontagem
- **Venda (no mercado do jogo):** metade do preço da peça. O preço inclui 25% do ouro nominal dos níveis que ela
  conserva. As gravações não mudam a venda.
- **Desmontagem:** só peças da bolsa. Rende metade dos fragmentos nominais dos níveis conservados, arredondada para
  cima, mais o material da peça. A confirmação diz que o equipamento será destruído e lista as gravações perdidas. A
  pilha cheia (99) recusa. Depois de desmontar, a tela mostra o que chegou (seção 9).

## 7. Herói e companheiros
- **Peças de todos:** a forja mostra as peças do herói, de cada companheiro e da bolsa, em abas por dono.
- **A soma das essências:** é de cada personagem, pelas peças que ele veste.
- **Na ficha:** a peça mostra o que ela fornece, igual na bolsa e no corpo. O total de quem veste fica na prévia do
  Encantar (quando outra peça dele também soma ou o limite corta).
- **Requisito:** o nível de quem vai vestir (seção 3.4).
- **Companheiro fora do grupo:** não pode ter peças reforçadas (`motivo_indisponivel`).

## 8. Salvamento, identidade e persistência
- **Identidade:** cada peça tem um id estável (`uid`, "p7"), dado na primeira vez que a forja a vê. A tela pede pelo
  id, nunca pelo nome: duas peças de mesmo nome são diferentes.
- **Na peça:**
  - `reforco`;
  - `bonus_base` e `preco_base`, a peça original, para a forma fechada;
  - `encantos`, uma entrada por sulco: None no vazio; "brasa", "brasa:2" e "brasa:3" para os tiers.
- **Gravações antigas** (só "brasa") continuam válidas como tier I.
- **No save:** os materiais entram no save.
- **Peças sem sulcos** (um save antigo) ganham os delas ao carregar, uma vez.
- **Pedidos repetidos:** reforço, gravação e transferência carregam um id de pedido; o mesmo id não age duas vezes.
- **Numeração dos resultados:** cada resultado da forja tem um número que só cresce (`forja_seq`), também depois dos
  cenários de teste que limpam o último resultado; a tela espera o número que o motor anuncia (`proximo_id`). Antes,
  os cenários reiniciavam a contagem e o reforço seguinte acontecia sem a cena.

## 9. Fluxos da interface [Protótipo]
- **Uma janela para as quatro operações:** Reforçar, Encantar, Transferir e Desmontar usam a mesma moldura, do mesmo
  tamanho, com o mesmo cabeçalho e o Fechar no mesmo lugar; trocar de aba não move a janela. O cabeçalho leva só as
  abas, o saldo de ouro e o Fechar. As listas rolam por dentro. Reforçar e o resultado em destaque são a referência
  das outras abas.
- **Formatos comuns das quatro abas [Protótipo, 16ª]** (a skill `texto-regras-fenda`; componentes `requerHtml`,
  `botaoAcao`, `peAcao`):
  - o que a operação consome: "Requer:" e cada material como **disponível/necessário** ("14/2"), a falta em vermelho no
    próprio valor; a dica (mouse e teclado) diz a ordem dos números e quanto falta. O nível, quando é requisito da
    operação, entra no mesmo grupo ("Nível 5", vermelho quando impede);
  - o ouro gasto fica **dentro do botão**, numa área reservada à direita ("Transferir · [moeda] 335", sem "Custo"); o
    valor não muda a largura do botão nem move o nome; em vermelho quando falta;
  - a confirmação não move a ação: a pergunta aparece em cima, o Cancelar num espaço reservado ao lado e a perda na
    nota (Transferir, Substituir, Desmontar);
  - o motivo do bloqueio aparece uma vez: o que já está marcado no valor não volta numa nota (o motivo por extenso fica
    no `title` e no rótulo acessível do botão).
- **Reforçar:**
  - o aquecimento corre na bancada;
  - na revelação, o resultado sai da bancada para a apresentação em destaque, com o véu: o nome com o nível, a peça
    com os efeitos, as propriedades antes → depois, os símbolos dos sulcos (as descrições das gravações, que não
    mudam, ficam para a inspeção), "SUCESSO" ou "FALHOU" e o OK;
  - o SUCESSO e o OK ficam mais abaixo, com espaço de leitura, e o OK fora do lugar do Reforçar atrás (a 1920 e a
    1280); "OK" é o rótulo, e o Enter, uma marca discreta;
  - o resultado fica até OK, Enter ou Esc.
- **Encantar** (sem ficha lateral; a peça se inspeciona com o mouse e o teclado):
  - **a peça e os sulcos:** o nome, o dono, o desenho e um botão por sulco, com o ícone e o tier da essência dentro;
    vazio, ocupado e escolhido se distinguem. Retirar a peça: o molde ou a miniatura;
  - **a essência:** primeiro a família (o ícone e o nome; a 1280, só o ícone), depois o tier I, II ou III: o símbolo
    com o tier no canto de cima à direita e a quantidade no canto de baixo, fora do símbolo;
  - **a prévia**, calculada no motor (`demo.previsao`): a essência escolhida com o efeito dela (o valor do tier), numa
    substituição só os valores que mudam, com o nome do efeito ("Brasa 40% → 60% · limite", "Carrasco 15% → —"), o
    total de quem veste só quando o limite corta ("Total em Jean …") e a troca ("Sai Carrasco I · entra Brasa II"); o
    limite aparece no próprio valor final ("60% · limite") e, só quando nada muda porque já estava no limite, uma nota
    curta ("Brasa já está no limite (60%)"); na bolsa, quando o requisito da peça sobe, "A peça passa a requerer nível
    9". **[Substituído, 16ª]** "Brasa nesta peça", a linha de quem veste sempre que outra peça somava e "Requer nível 5
    (Jean: 4). Na bolsa, pode gravar."; **[Substituído, 17ª]** "Limite 60%: 8% não valem" (a conta do que sobra);
  - o pé fixo: "Requer: [essência] 3/1" (e "Nível 5" numa peça vestida, quando a gravação sobe o requisito), o botão
    Gravar ou Substituir com o preço dentro; substituir pede confirmação no mesmo lugar, numa frase só ("Substituir?
    Carrasco I se perde.", sem repetir a perda na nota); a mesma gravação aparece como
    "Já gravado", sem o "Requer:", e não cobra;
  - a gravação concluída aparece na mesma apresentação em destaque, sem suspense, com a gravação nova em destaque
    (o efeito dela) e a que saiu.
- **Transferir** (duas peças):
  - origem e destino em dois encaixes do mesmo tamanho, ligados por um conduto; o reforço de agora na etiqueta do
    ícone e, embaixo, "Após transferir" e só o nível previsto (a origem +0 em vermelho, o destino em verde; o rótulo
    Origem/Destino e o texto continuam, a cor não é o único sinal); o preço dentro do botão Transferir;
  - clicar num encaixe abre a lista de escolha: ícone, nome, raridade, reforço e dono (duas peças de mesmo nome se
    distinguem por isso e pelo id). Com a origem escolhida, os destinos possíveis vêm primeiro e os outros dizem por
    quê ("Nenhum destino" na origem que não tem para onde ir);
  - trocar a origem limpa o destino que deixou de servir, com uma linha dizendo isso, e reabre a lista dos destinos;
  - a confirmação mantém os dois encaixes (os dois resultados) e o Transferir no mesmo lugar e tamanho (medido a 1920 e
    a 1280); só acrescenta a pergunta e o Cancelar; as regras ("o destino recebe o nível da origem menos 2", "afixos, sulcos e gravações ficam em cada
    peça") saíram da tela e continuam aqui, na seção 5, e na ajuda;
  - a cena (1,4 s): a origem acende, a luz corre pelo conduto, a origem perde o acabamento e o destino recebe o nível
    e o acabamento; depois, "Transferência concluída" num véu fechado (a bancada atrás não disputa a leitura), com o
    destino em destaque (o novo nível em verde) e a origem com +0 em vermelho, até o OK. Sem suspense e sem a explosão
    do reforço máximo. Com movimento reduzido, o resultado parado. Adiantar não dispensa nem repete; fechar a janela
    não desfaz nem duplica; a cena só representa a transação já resolvida;
  - depois do OK, as escolhas se limpam (nenhum par novo é escolhido sozinho) e o foco volta ao encaixe da origem.
- **Desmontar:** o nome da peça como título, "No mercado, vende por X." e a confirmação no pé ("Destruir a peça?",
  as gravações perdidas na nota, o Desmontar no mesmo lugar); a transformação é curta, sem celebração.
  - **O recebimento [Protótipo, 17ª]:** a prévia mostra a peça e o que vai sair ("×10" ao lado do material); depois da
    transformação, o encaixe da peça fica vazio, o título diz o nome com o reforço e "Desmontado", e, ao lado do
    material, o que chegou ("+10", em verde) e o saldo novo ("Fragmentos: 30"), que acende uma vez. A prévia e o
    recebido se distinguem pelo sinal (× do que vai sair, + do que entrou), pelo encaixe vazio e pelo título. Com
    movimento reduzido, o recebido aparece parado, no mesmo lugar. Fica até a próxima escolha de peça.
  - **A fluidez [Corrigido, 18ª]:** a transformação parecia ter poucos quadros. As causas: o efeito corria a 15 quadros
    por segundo (o ritmo das celebrações); as animações do CSS andavam em degraus (11 a 13 quadros por segundo); e a
    volta do motor desenha a forja mais de uma vez, e cada redesenho parava o efeito no meio do voo e recomeçava as
    animações. Agora o efeito tem palco e relógio próprios (um quadro a cada atualização da tela; medido: 16 ms entre
    quadros), os fragmentos voam numa curva até o saco do material, que fica à vista, e as animações seguem o tempo já
    decorrido (um redesenho continua de onde estava). O +N e o saldo novo acendem quando os fragmentos chegam (antes,
    o saldo de antes). Duração: 1 s (antes, 0,7). Sem OK e sem celebração; uma cobrança só (conferido com clique duplo).
- **Entrada da forja [17ª]:** os quatro serviços numa grade 2 × 2 (antes, três numa linha e um sozinho embaixo).
  **[Corrigido, 18ª]** a regra da forja do jogo (`#cena.com-ambiente .forja .servicos`, com um id) vencia a de duas
  colunas, e a entrada continuava três e um; agora vale o 2 × 2. Os textos dos cartões ficam os de antes, sem a marca
  "(laboratório)" no Encantar (observação de protótipo não vai para a tela do jogador).
- **Remover a gravação [Candidata, 18ª]** (regra na seção 3.3): no Encantar, embaixo dos sulcos, "Remover gravação"
  (só com um sulco ocupado escolhido; o lugar fica reservado). A confirmação no pé, como a da substituição: a pergunta
  numa frase ("Remover? Brasa I se perde."), o Remover no lugar da ação e o Cancelar ao lado; Esc cancela. A prévia
  mostra o que cai ("Brasa 20% → —"; o total de quem veste quando outra peça dele também soma; "A peça passa a
  requerer nível 4" quando o requisito cai). Depois, o sulco vazio apaga a cor da essência uma vez.
- **A doca dentro da forja [Produção, 1.214.0]:** os atalhos da barra de baixo (Inventário, Comitiva, Grimório…)
  funcionam também nas telas de serviço (a forja, o mercado, a taverna, o templo): o atalho volta ao lugar e abre a
  tela pedida. Antes, eram recusados fora do menu do lugar, o que não fazia sentido para o jogador (pedido do Jean).
  O motor marca o Voltar dessas telas com `lugar: True`.
- **A vida ao entrar na forja [Corrigido, 17ª]:** entrar na forja do protótipo tirava vida (Jean 65 → 60, Morel
  85 → 79). A causa: a comparação hipotética da ficha (`demo.comparar`, que veste e desveste a peça para medir a
  diferença) cortava a vida no máximo sem a peça e não a devolvia. Agora a comparação guarda a vida antes e a repõe
  depois. A forja de produção não tinha o defeito (conferido: três entradas e saídas sem mudar vida, máximo, dia nem
  período). Teste pelo caminho real (`TestEntrarNaForja`).
- **A troca de tela sem piscar [16ª]:** a cada pedido, o motor redesenha a forja como uma cena nova (a página se limpa)
  e manda o painel em seguida. Até a 15ª, o painel era calculado entre as duas mensagens, e numa máquina lenta o
  navegador pintava a oficina sem a janela ("às vezes", 10 a 16 ms aqui; reproduzido com 80 ms). Agora o motor calcula
  o painel antes de anunciar a cena, e a tela segura a janela antiga, parada e sem cliques, até a nova estar montada.
- **Gestos:**
  - as confirmações só aceitam o clique depois de 400 ms;
  - o segundo clique de um clique duplo (`event.detail` 2) não age; do terceiro em diante é uma ação nova. Antes,
    todo clique com `detail` acima de 1 era tratado como o resto do gesto, e quem clicava de novo no mesmo lugar logo
    depois do OK (o Windows segue contando 3, 4, 5…) ficava travado até parar de clicar;
  - não há pausa por tempo depois de dispensar (saíram os 450 ms que engoliam qualquer clique): o resto do gesto é só
    o 2º clique do duplo e o clique que o Espaço gera ao soltar a tecla que dispensou;
  - a tecla segurada não repete;
  - o gesto que adianta a cena não dispensa o resultado;
  - cada tentativa é uma cobrança e um resultado;
  - conferido na 16ª por cobrança e por resultado (não só pela contagem de cliques): clique duplo no Reforçar compra
    uma vez; OK com clique duplo e triplo no mesmo ponto fecha sem comprar; o Reforçar logo depois do OK compra na
    hora; quatro cliques seguidos compram uma vez e o resultado fica até o OK; depois, um clique novo compra; Enter
    segurado fecha sem comprar; Enter segurado no Reforçar compra uma vez;
  - Esc revela, cancela a confirmação e fecha, nessa ordem.

## 10. Linguagem visual [Protótipo]
- **Raridade:** a cor da borda do encaixe e do nome.
- **Reforço:** o acabamento sobre o desenho da peça.
  - +1 a +4: o reflexo; o +4 com contorno dourado. O contorno segue só a silhueta de fora da peça (o furo do anel não
    ganha contorno por dentro).
  - +5 a +8: turquesa, safira, ametista e rubi.
  - +9 a +12: o veio multicolorido em pixel, com brilhos.
  - O +N fica no canto do encaixe e, nas dicas, colorido pelo nível.
- **Reflexo:** passa por cima do desenho sem modo de mistura; com mistura, a 125% e 150% de escala o navegador
  amostrava o desenho de outro jeito e a peça parecia se mexer (a Manopla de Ferro +2).
- **Veio (+5 a +12) e contorno (+4 a +12):** cada passo do veio é um quadro pronto (o desenho, as faixas misturadas
  em "overlay" e o recorte pela peça, pintados num canvas fora da tela na resolução do desenho) mostrado como imagem
  por cima da peça; o contorno também é uma imagem. Guardados por desenho e nível. **A causa do tremor no resultado
  (15ª):** a mistura do veio era do CSS (`mix-blend-mode: overlay`); com ela, o navegador compunha a peça num grupo à
  parte e a reamostrava, e no resultado em destaque o desenho ficava borrado (a 125%, quase todo) e o borrão mudava
  quando o reflexo, os brilhos ou o passo do veio entravam, como se a peça tremesse. Com a mistura no canvas mostrado
  na tela, a 125% o canvas ainda saía suavizado (a posição do resultado não cai num pixel inteiro, e o navegador
  encaixa no pixel a imagem, não o canvas); como imagem, fica nítido. Medido no resultado (blocos de um pixel do
  desenho que não são de uma cor só, mediana dos quadros): a 125%, Couraça +10 de 89% para 1%, Martelo +12 de 83% para
  0%, Machado +5 de 68% para 0%; a 150%, Couraça de 90% para 0%; a 100%, Couraça de 65% para 0%. O que ainda mistura
  é a passada do reflexo, que é o efeito. Depois do impacto, a silhueta e os pixels da peça ficam parados; só o
  reflexo, os raios, as partículas e as cores do veio andam. Também corrigido: quando o resultado abria antes de o
  desenho carregar, o veio tomava a largura na tela (80) pela do desenho (40) e as faixas saíam com meio pixel da peça.
- **Alinhamento do resultado:** o conjunto é deslocado por `left`/`top` (layout) até a peça cair num pixel inteiro do
  aparelho, não por `translate`.
- **Gravação:** um rastro de luz na cor da essência percorre a borda do encaixe.
- **Tier:** I, II ou III numa etiqueta no canto de cima à direita do símbolo da essência, na linguagem da etiqueta do
  reforço (+N): placa escura, aresta de latão, 13 px a 1920 e 12 px a 1280, fora do desenho; nos materiais, na seleção
  da forja, nos sulcos, nas fichas e no espólio; a quantidade fica noutro canto. **[Substituído, 16ª]** o selo de 9 px.
- **Botões: o acabamento A [Aprovado, 17ª]:** ferro encaixado (planos chapados, cantos em degrau, luz curta na
  aresta de cima, base escura). Pressionar afunda a face sem mover o botão; o foco é um anel de latão por dentro. Na
  forja: as ações, o Cancelar, o OK, o Fechar, as abas, os donos, as famílias, os tiers e os sulcos. Na produção
  (1.214.0, `css/27-ferro.css`): os Caminhos, os serviços dos lugares (Mercado, a entrada do ferreiro, a taverna), a
  doca, os cartões do Bestiário e da Comitiva (com a barra), as abas do Inventário, "Distribuir pela sugestão" e os
  "+" dos atributos (uma plaquinha de latão). **[Rejeitado, 17ª]** o B (presilhas de latão), retirado do protótipo.
  **[Em revisão, 18ª]** a aplicação no conjunto do jogo não agradou ao Jean (o aviso de talento, os cabeçalhos da
  forja e da taverna, o Voltar à vila, o Olhar de perto): superfícies lisas, degradês genéricos e bordas finas. A
  aprovação do botão A não fecha a aplicação; a candidata abaixo desenvolve a direção.
- **Placas de metal da bancada [Candidata, 18ª]** (só na demonstração: `tela/placas.css`, "Botões e painéis" no
  painel de testes): a família de controles a partir das placas que já existem na bancada. Ferro escuro com a textura
  discreta da chapa, a construção em pixel, latão contido. A regra que separa as funções: **o que se aperta tem
  espessura** (a face, a aresta de cima acesa e, embaixo, a lateral da placa: o vinco, 3 px escuros e a aresta de
  baixo pegando luz; pressionar afunda a face e a lateral some); **o que só informa é fixado** (a placa rente, borda de
  2 px com chanfro e, quando é grande, um rebite de 4 × 4 pixels em cada canto); **o que guarda número ou tecla fica
  num nicho** (o ouro do cabeçalho, a tecla do Continuar). Tamanhos: cabeçalhos e cartões grandes com rebites e cantos
  de 3 degraus; botões médios com a placa simples; pequenos (abas, doca, o "+") sem rebite. Estados: mouse (a face
  clareia, a aresta acende), pressionado, foco (anel de latão de 2 px por dentro), selecionado (o fio de latão em cima,
  a face quente, a placa assentada) e indisponível (o ferro frio, sem luz nem lateral). Componentes: os Caminhos, os
  serviços e os cabeçalhos dos lugares (a forja, a taverna, o templo, a curandeira, o mercado), o Voltar à vila, o
  aviso de pontos de talento (com uma tira de latão), a doca, as abas e os botões do Inventário, os cartões da
  Comitiva (em relevo) e do Bestiário (fixados), o Olhar de perto e o Confirmar da Encruzilhada, e o Continuar da festa
  da especialização (só esse: `.festa.fb2-spec .continuar`). A 1280, a mesma altura do acabamento de hoje.
  **Segunda passada (18ª), pela referência de composição do Jean** (uma imagem gerada: vale a composição e a família,
  não o acabamento, os ícones nem os textos): os rebites pela escala (os cartões grandes de serviço com um em cada
  canto, numa camada que o mouse e a pressão não apagam; os Caminhos e os cartões da Comitiva com um pino de 2 × 2
  pixels; os botões, as abas e a doca sem nada); a barra de baixo como um suporte contínuo (uma placa só com a
  espessura, os atalhos rentes sobre ela separados por um vinco, um vão escuro entre os grupos; a tela aberta afundada
  e quente com o fio de latão embaixo); o aviso de talento com o "▸" num fim separado por um vinco; a hierarquia do
  serviço (o ícone no nicho, o nome, a linha secundária). A barra fica 4 px mais alta que hoje; os cartões da forja, 1
  px.
- **Armaduras do +9 ao +12 [Candidatas A, B e C, 18ª]** (painel de testes, "Armaduras +9 a +12", e a vitrine: as
  cinco peças do herói do +8 ao +12): o feixe da 17ª ficou discreto demais (do +8 para o +9 parecia perder força). As
  três partem da faixa do +8, que fica exatamente como está: a mesma força da mistura, a mesma largura (3 pixels e o
  pixel claro atrás) e a mesma frequência (uma faixa a cada 18 diagonais, um passo a cada 70 ms), e a passada
  periódica do reflexo volta, na cor da alternativa. **A · passadas alternadas:** uma cor por faixa, na ordem do nível
  (+9 rubi e âmbar; +10 mais o azul; +11 mais a esmeralda; +12 mais o violeta), nunca várias cores numa faixa.
  **B · cor gradual:** todas as faixas na mesma cor, que passa devagar para a seguinte (três faixas por cor). **C ·
  reflexo principal e secundário:** a faixa na cor principal e, logo atrás, um reflexo de 1 px (2 no +11 e +12) na
  secundária: as cores da celebração do nível (+9 rubi e âmbar; +10 laranja e azul; +11 âmbar e esmeralda; +12 âmbar
  e violeta). Nas três, o nível cresce pelas cores, pela força (+11 e +12) e pelos pontos de brilho (1 a 4, como nas
  armas); o +12 tem o pixel claro em marfim. Armas e joias não mudam. Com movimento reduzido, paradas.
- **Armaduras do +9 ao +12: o feixe [Substituído, 18ª; fica no painel para comparar]:** capacete, peito, luvas, pernas e botas, em vez do veio de faixas
  largas: o **feixe**, linhas diagonais de 1 px na mesma força do veio do +8 (a sutileza dele), estreito, com as cores
  ligadas ao nível (+9 rubi e âmbar; +10 mais o azul; +11 mais o esmeralda; +12 marfim, rubi, âmbar, esmeralda, azul e
  violeta), passando pela peça. O contorno aprovado fica; a passada larga do reflexo não passa nelas. Armas, joias,
  escudos, tomos e aljavas continuam com o veio. O +8 fica exatamente como estava. O ciclo vem de um relógio comum
  com um desvio fixo pelo lugar da peça. O veio anterior fica no painel de testes para comparar. **[Rejeitados,
  17ª]** o A (brilho nas bordas) e o B (reflexo estreito) da 16ª.
- **Celebração do +9 ao +12 [Candidata, 17ª]:** as cores ligadas ao acabamento da peça, uma dominante e uma
  secundária (+9 rubi e âmbar; +10 laranja e azul; +11 âmbar e esmeralda; +12 âmbar e violeta), o prisma só em alguns
  estilhaços, a grandeza pela forma (leques de raios, alcance, estrela, anéis). O +8 e os de baixo não mudam (pedido
  do Jean). A anterior fica no painel de testes. **[Rejeitada, 17ª]** a paleta da 16ª (violeta e ouro sem ligação com
  a peça), que incomodava a partir do +9. **Referência para um +13 [Guardado]:** o ouro da candidata da 16ª no +12
  (ouro, âmbar e marfim) fica no painel ("Ouro ref. +13") como referência, caso o limite um dia passe do +12; nenhum
  +13 foi criado.
- **Fichas** (a hierarquia das fichas do Diablo IV, com a arte do jogo), nesta ordem:
  1. o nome e o reforço ("Martelo de Aço +3");
  2. o tipo e a raridade; a base sai dos parênteses do título e vai para esta linha ("Machado · Lendário", sem
     "(Machado)" no nome);
  3. os atributos e afixos;
  4. os sulcos (os vazios também, com o tier no canto) e os efeitos da peça: o nome com os tiers numa linha pequena
     ("Brasa III + II") e, embaixo, o gatilho, o efeito e o limite; acima do limite, "Limite 60%.";
  5. "Requer nível N", à direita, em vermelho quando falta;
  6. o resto (a comparação, o motivo de não usar, a venda, o texto de sabor).
  "Detalhes" abre por clique ou teclado: uma frase por essência (a condição ou a interação que muda a decisão, e até
  quanto a repetição soma). Sem rodapés "Clique para…" nas dicas; no Inventário, a peça marcada não abre a dica por
  cima da ficha ao lado.
- **Dicas na janela:** quando a ficha cresce depois de abrir (os sulcos entram depois), a dica sobe até caber acima da
  doca e do fim da tela; maior que o espaço, rola por dentro, sem diminuir a letra.
- **Seleção e foco:** os cantos de latão e o anel de foco não mudam com o acabamento.

## 11. Casos de teste e exemplos

**Testes automáticos** (`ferramentas/prototipos/reforco/testes`, 65):
- todo passo de todo espaço, do +0 ao +12, melhora alguma linha, sem casa que o motor não usa e sem passar um degrau da
  conta; a peça sem portador recebe reforço; a peça toda no teto não cobra; a fração na ficha e na luta; o painel de
  testes;
- reforço em todos os espaços, sem cair, com a arma sentindo cada passo até o +4;
- forma fechada sem deriva;
- tetos de %;
- transferência (resultado, conservação, cobrança única, nada se cria, cadeia);
- cada tier com o seu valor; repetição igual e misturada, na mesma peça e entre peças, até o limite; só o que se veste
  conta;
- textos pelo valor do tier; a ficha com o que a peça fornece; a prévia da troca e do limite;
- requisitos: a tabela, a peça gravada, vestir bloqueado em todos os caminhos (herói e companheiro), o achado acima do
  nível, a gravação em peça vestida recusada sem cobrar e a preparação na bolsa;
- o saque real dando materiais pela criatura;
- Carrasco pela tabela; Revide pela soma até o limite e no máximo 2 por rodada; Eco até 2 por luta;
- lutas de verdade;
- salvar e carregar;
- entrar e sair da forja pelo caminho real sem mudar a vida (17ª);
- remover a gravação: sem custo, sem devolver, uma vez por pedido, com a soma, o requisito, a ficha e a prévia
  recalculados (18ª, `TestRemover`).

**Cenários da faixa da demonstração** (só no save temporário):
- **Níveis altos (teste):** peças de +4 a +12, duas com três gravações; e (16ª) Jean com capacete, luvas, pernas e
  botas de ferro do +9 ao +12 e Odette com um peito de tecido escuro no +11, para os acabamentos das armaduras.
- **Painel de testes (16ª):** nível, classe e especialização (reiniciam o cenário pelo caminho do jogo); ouro,
  fragmentos e essências por tier (aplicam na sessão, validados); as candidatas visuais (botões, armaduras, paleta).
- **Essências (teste):** vestidas, só tier I (o grupo está no nível 4):
  - Jean: Brasa I + Brasa I + Carrasco I na arma (Brasa 40%); Vigília I + Revide I + Geada I no peito;
  - Odette: Eco I na arma e Eco I + Eco I no tomo (Eco 30%, entre peças);
  - Morel: três Revides I (36%);
  - na bolsa, preparadas: o Martelo de Aço com Brasa III + Brasa II (64%, o limite corta; requer o 9) e a Couraça com
    Vigília II (requer o 5);
  - 3 essências de cada tier.
- **Nível +4 (teste):** o grupo sobe 4 níveis pelo caminho do jogo (`dev.subir_ate`), sem a festa: duas vezes levam do
  4 ao 12, para ver os requisitos de II e III atendidos.
- **Transferência (teste):** na bolsa, uma arma comum +10, outra +2 (com Brasa, sem destino possível), um peito
  incomum +6 e outro +0; o Martelo de Ferro de Jean e o de Morel têm o mesmo nome.
- Os demais: Sucesso e Falha (teste), Comparação e Luta de teste.

**Exemplo completo:** Jean (nível 4) veste a arma com Brasa I + Brasa I + Carrasco I (Brasa 40%). Ao escolher Brasa
II para o terceiro sulco (onde está Carrasco I), a prévia diz o efeito da Brasa II (28% de chance), "Brasa 40% →
60% · limite", "Carrasco 15% → —" e "Sai Carrasco I · entra Brasa II"; o pé diz "Requer: [Brasa
II] 3/1 · Nível 5" com o nível em vermelho, e o botão "Substituir · [moeda] 30" fica bloqueado. No nível 5, a mesma gravação passa e, na luta, cada golpe que acerta tem 60% de chance de Queimadura, no
máximo 1 vez por rodada.

## 12. Pendências para integrar e assuntos futuros
- **Equilíbrio em avaliação:** chances e custos do +5 ao +12 e o ouro (alto para a campanha curta); as tabelas das
  essências (os valores por tier e os limites) e os requisitos de nível; as fontes e as chances de material. Julgar
  jogando a campanha ampliada.
- **Integração:**
  - trocar o ferreiro de produção (seção 0);
  - levar regras, materiais e save para o motor;
  - os textos para `rpg/` e a skill;
  - a arte própria dos materiais e das essências por tier (os ícones são provisórios, e os de 16 e 24 px são
    reduzidos).
- **Sons:** adiados até a interface estar satisfatória como 1.0.
- **Elevação da base de peças excepcionais:** pendente (subir o nível base de uma peça única), fora deste lote.
- **Fontes futuras da campanha:** quests e contratos, e os tiers do conteúdo avançado.
- **A conferir:** peças de muitos afixos fortes crescendo todas as linhas; gravação nos outros espaços (hoje não).
- **Decisões substituídas** (registradas para não voltarem): o limite +4; a escolha Fio ou Runas; o reforço só da
  base; o dobro dos apoios; "a mesma essência não repete"; um efeito por essência gravada; o nível total de 1 a 5
  com teto (agora, cada tier com o seu valor e a soma até o limite de cada efeito).
- **Candidatas da 18ª a avaliar (Jean), todas no painel de testes da demonstração:** as armaduras do +9 ao +12 (A,
  B ou C); as placas de metal da bancada (antes de outra aplicação ampla na produção); remover a gravação sem
  substituir (e se a remoção deve custar algo); o gesto do martelo do ferreiro (`hud/forja/h2/candidata_gesto.py`,
  "Ferreiro: gesto candidato"). A celebração do +9 ao +12 está aceita por enquanto; a Odette continua pendente.
- **Integração da fração:** os atributos com casa decimal e o acúmulo de Espinhos, Vida por turno e Vida por abate
  estão no protótipo (`demo.decimais_na_luta`); na integração, vão para `entidades`, `comitiva` e a luta, com o
  gabarito atualizado de propósito.
- **Peça toda no teto:** a proposta (crescer pela linha fixa mais próxima da base) espera decisão. **[Não aprovada,
  17ª; registrada, sem implementar]** dar um atributo adicional quando todas as propriedades da peça atingem o teto.
- **Mercado:** a peça acima do nível não se equipa ali (o motor recusa), mas o texto do jogo ainda diz "não é para a
  sua classe" (mercado.js, produção); a corrigir na integração.
