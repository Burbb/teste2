# 27 — A forja: especificação do sistema (reforço, materiais, encantamento, transferência)

Documento de referência da etapa 4. Ele descreve o sistema inteiro como está hoje, sem precisar da conversa nem dos
históricos de protótipo. Atualizado em 28/10/2026, conferido contra o código do protótipo
(`ferramentas/prototipos/reforco`: `regras.py`, `encanto.py`, `demo.py`, `tela/reforco.js`) e o de produção
(`rpg/sistemas/servicos.py`).

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
anel e amuleto. As peças podem ser do herói, dos companheiros ou da bolsa. Uma peça que ninguém do grupo sabe usar é
recusada ("Ninguém do grupo usa peças de …"); a de um companheiro fora do grupo, também. **[Substituído]** Antes, só
arma, peito, escudo e tomo.

### 1.2 O que cresce [Aprovado: a peça inteira; Provisório: a fórmula]
**A peça inteira:** todas as linhas, da base e dos afixos. O reforço não mexe nas gravações. **[Substituído]** a
escolha Fio ou Runas da arma do Guerreiro e o reforço só da linha da base.

**Correção matemática** (o que tinha de mudar, independente do equilíbrio):
- **Forma fechada.** O ganho do +N sai sempre da peça original (`bonus_base`), sem passar pelos níveis do meio. Cair e
  subir de novo dá exatamente o número do nível, sem deriva (testado com quedas e subidas em sequência).
- **Sem +1 imposto a toda linha.** Uma linha pequena pode passar passos sem subir. Só a linha principal da arma sobe
  ao menos 1 por passo, e só do +1 ao +4 (a faixa aprovada, em que cada passo se sente).
- **Meio para baixo nos valores pequenos.** O ganho é arredondado com o meio para baixo (1,5 → 1). Com o meio para
  cima, uma aljava de Agilidade 1 ia a 3 no +4.
- **Porcentagens com teto.** Crítico e roubo de vida crescem por soma (abaixo), sem passar do teto por peça. O teto
  de crítico do personagem (60%) continua no motor. As peças não têm resistências hoje.
- **Sem regra especial por espaço.** Saiu o dobro que os apoios tinham do +1 ao +4: o afixo se mistura à base na
  mesma linha, e o Tomo da Coruja ia de Poder 5 a 13 já no +4.

**A fórmula** [Provisório]. Um + vale "a mesma peça alguns níveis acima". Os passos valem 1,5 nível de peça do +1 ao
+4, 1 do +5 ao +8 e 0,75 do +9 ao +12; L(N) é a soma até +N, e o +12 soma 13.
- Linha fixa de valor v numa peça de nível n: ganho(N) = arredonda(v ÷ escala(n) × 0,75 × L(N)), com
  escala(n) = 1,5 + 0,75 × n, a do gerador.
- Crítico e roubo de vida: + 0,25 ponto por nível de peça, como os afixos do gerador. O teto por peça é 15% de
  crítico e 10% de roubo de vida.

**Exemplos reais do catálogo** (`simular.py`), comparados com a substituta, uma base comum do gerador 6 e 12 níveis
acima, no +0:

| Peça | +0 | +4 | +8 | +12 | Substituta (base comum do gerador), nível +6 / +12 |
|---|---|---|---|---|---|
| Martelo Enferrujado (nível 1, comum) | Ataque: 2 | 6 | 9 | 11 | Machado de Aço: 7; Machado Rúnico: 14 |
| Martelo de Aço (nível 6, comum) | Ataque: 6 | 10 | 13 | 16 | Machado Rúnico: 13; Machado Rúnico: 18 |
| Pranto Sangrento (nível 12, raro) | Ataque/Crítico/Defesa: 12/6/5 | 17/7/7 | 21/8/9 | 23/9/10 | Machado Rúnico: 18/0/0; Machado Rúnico: 23/0/0 |
| Grimório de Aço do Vampiro (nível 6, incomum) | Poder/Roubo de vida: 6/4 | 10/5 | 13/6 | 16/7 | Varinha Rúnica: 13/0; Varinha Rúnica: 18/0 |
| Arco Longo de Ferro (nível 4, comum) | Ataque/Agilidade: 3/1 | 7/2 | 8/3 | 9/3 | Arco Longo Temperado: 8/2; Arco Longo Rúnico: 13/4 |
| Cota de Malha de Ferro (nível 1, comum) | Defesa/Vida: 1/4 | 3/12 | 4/17 | 5/21 | Peitoral de Aço: 5/14; Peitoral Rúnico: 9/27 |
| Cicatriz da Fenda (nível 6, raro) | Defesa/Vida/Crítico: 7/29/4 | 12/51/5 | 16/65/6 | 18/76/7 | Peitoral Rúnico: 9/25/0; Peitoral Rúnico: 13/36/0 |
| Broquel de Aço (nível 3, comum) | Defesa/Vida: 1/2 | 2/4 | 3/6 | 4/7 | Escudo Temperado: 3/5; Escudo Rúnico: 5/8 |
| Escudo Temperado da Águia (nível 8, incomum) | Defesa/Vida/Agilidade: 3/4/4 | 5/6/6 | 6/8/8 | 7/9/9 | Escudo Rúnico: 5/7/0; Escudo Rúnico: 7/10/0 |
| Tomo da Coruja (nível 6, incomum) | Poder/Mana: 5/5 | 9/9 | 11/11 | 13/13 | Tomo: 4/12; Tomo: 5/18 |
| Aljava Rasgada (nível 2, comum) | Agilidade/Ataque: 1/1 | 2/2 | 3/3 | 4/4 | Aljava Reforçada: 1/1; Aljava Rúnica: 3/3 |
| Cicatriz Sangrenta (nível 7, raro) | Agilidade/Ataque/Espinhos/Regeneração/Roubo de vida: 1/1/6/2/4 | 2/2/10/3/5 | 2/2/13/4/6 | 2/2/15/5/7 | Aljava Rúnica: 3/3/0/0/0; Aljava Rúnica: 4/4/0/0/0 |
| Barbuta de Ferro (nível 4, comum) | Defesa/Vida: 1/2 | 2/4 | 3/5 | 3/6 | Elmo Temperado: 2/5; Elmo Rúnico: 3/8 |
| Luva de Seda de Lã Negra dos Espinhos (nível 6, incomum) | Poder/Defesa/Espinhos: 1/1/6 | 2/2/10 | 2/2/13 | 3/3/16 | Luva de Seda Rúnica: 2/1/0; Luva de Seda Rúnica: 3/1/0 |
| Aro do Carniceiro (nível 3, incomum) | Vida por abate: 5 | 11 | 15 | 18 | Anel do Carniceiro: 9; Anel do Carniceiro: 14 |
| Brasa Faminta (nível 8, raro) | Agilidade/Crítico: 4/4 | 6/5 | 8/6 | 9/7 | Talismã do Carniceiro: 0/0; Talismã do Carniceiro: 0/0 |

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

### 3.2 Tiers, repetição e nível total [Aprovado; Provisório: o teto]
- **Tiers:** Essência I, II e III ocupam um sulco cada e contribuem com 1, 2 e 3 níveis do efeito.
- **Repetição:** permitida na mesma peça e entre peças. **[Substituído]** a regra "a mesma essência não entra duas
  vezes na mesma peça".
- **Nível total:** cada efeito é resolvido **uma vez** pelo nível total, a soma das peças que **o próprio personagem
  veste**. A bolsa e as peças dos outros não contam. Exemplos:
  - duas Brasas I dão Brasa 2;
  - Brasa II + Brasa I dão Brasa 3;
  - Eco III + Eco II no tomo e Eco II na arma somam Eco 7, que vira 5 pelo teto.
- **Teto de 5 níveis por efeito** (hipótese de teste). O que passa não conta.
- **Não existe um "nível da gravação":** o nível é sempre o total de quem veste.

### 3.3 Gravar, substituir, perder [Aprovado]
- **Gravar:** consome 1 essência do tier escolhido e 30 de ouro, com reputação. Nunca falha.
- **Substituir:** gravar num sulco ocupado custa o mesmo e apaga a gravação anterior. A essência antiga não volta e
  não há extração. A tela pede confirmação e diz o que sai.
- **Peça e dono:** a gravação é da peça e vai com ela quando ela troca de dono.
- **Desmontar** perde as gravações. A confirmação lista quais ("Perde as gravações: Brasa II, Eco I.").
- **Compatibilidade por essência:**
  - Brasa e Carrasco: arma;
  - Eco: arma, tomo e escudo;
  - Vigília: peito, escudo e tomo;
  - Revide: peito e escudo;
  - Geada: peito.

## 4. As seis essências [Provisório: as tabelas]

Em cada tabela, **só uma dimensão cresce** com o nível; o gatilho, o alvo, a duração e o limite ficam. "Rodada" é
quando todos agiram (`cb.turno` no motor); "turno" é a vez de um combatente. Nenhum efeito secundário dispara outro: o
tique de uma Queimadura, um Revide ou outra reação não aciona gravação nenhuma. Invocações não vestem peças e não
contam como portador.

| Nível | Brasa (chance) | Carrasco (dano a mais) | Eco (recurso) | Vigília (barreira) | Revide (chance) | Geada (chance) |
|---|---|---|---|---|---|---|
| 1 | 25% | +20% | 15% | 10% | 15% | 15% |
| 2 | 32% | +25% | 20% | 13% | 20% | 20% |
| 3 | 39% | +30% | 25% | 16% | 25% | 25% |
| 4 | 46% | +35% | 30% | 19% | 30% | 30% |
| 5 | 53% | +40% | 35% | 22% | 35% | 35% |

- **Brasa** (arma):
  - **Gatilho e alvo:** um golpe do portador que acerta um inimigo; atinge esse inimigo.
  - **Efeito:** aplica 1 camada de Queimadura, até 3. O valor é 25% do maior entre Ataque e Poder (mínimo 2), com a
    duração da Queimadura do herói (2 turnos quando o portador é um companheiro).
  - **Limite:** 1 aplicação por rodada. Em área ou em golpes múltiplos, vale a primeira que pegar.
  - **Interações:** soma camadas com a Queimadura do Mago; o tique não dispara a Brasa; chefes recebem igual.
- **Carrasco** (arma):
  - **Gatilho e alvo:** cada golpe do portador num inimigo abaixo de 35% da vida.
  - **Efeito:** o dano a mais da tabela.
  - **Limite:** nenhum; vale em cada alvo de um golpe em área.
  - **Interações:** multiplica com os outros bônus; não vale nos tiques nem nas reações; chefes recebem igual.
- **Eco** (arma, tomo, escudo):
  - **Gatilho e alvo:** um inimigo cai pelo golpe do portador; recupera o próprio portador.
  - **Efeito:** a porcentagem da tabela da Mana, do Vigor ou do Foco máximos.
  - **Limite:** 2 vezes por luta, fixo, para não virar recurso sem fim.
  - **Interações:** cada inimigo derrubado num golpe em área conta uma vez, dentro do limite.
- **Vigília** (peito, escudo, tomo):
  - **Gatilho:** o começo da luta.
  - **Efeito:** a barreira da tabela, por 3 turnos do portador.
  - **Limite:** 1 vez por luta.
  - **Interações:** não soma com outra barreira; vale a maior (a Aura de Proteção).
- **Revide** (peito, escudo):
  - **Gatilho e alvo:** um golpe corpo a corpo de inimigo que acerta o portador; revida em quem bateu.
  - **Efeito:** um golpe de 60% do Ataque.
  - **Limite:** 1 resposta por golpe e **2 por rodada**, para não virar um ciclo com muitos atacantes.
  - **Interações:** o revide não aciona outro revide nem a Brasa; não responde a golpes à distância nem a tiques; um
    golpe em área que pega o portador conta como um golpe.
- **Geada** (peito):
  - **Gatilho e alvo:** um golpe corpo a corpo de inimigo que acerta o portador; congela quem bateu.
  - **Efeito:** o atacante perde a próxima vez.
  - **Limite:** 1 vez por luta.
  - **Interações:** chefes e gigantes resistem metade das vezes (a regra do Atordoado).

Os textos da ficha saem dessas tabelas (`encanto.texto`). Exemplo no nível 1: "Eco 1 Ao abater um inimigo, recupera
15% do recurso máximo. Até 2 vezes por luta."

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
  pilha cheia (99) recusa.

## 7. Herói e companheiros
- **Peças de todos:** a forja mostra as peças do herói, de cada companheiro e da bolsa, em abas por dono.
- **Nível total:** é de cada personagem, pelas peças que ele veste.
- **Na ficha:** uma peça vestida mostra o total de quem a veste. Uma peça na bolsa mostra só o que ela dá.
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

## 9. Fluxos da interface [Protótipo]
- **Abas e espaço da janela:** Reforçar, Encantar, Transferir e Desmontar, na mesma janela e na mesma bancada. A
  peça fica no eixo, os materiais à esquerda, o ganho (ou a essência, ou os destinos) à direita, e o botão no pé.
- **Reforçar:**
  - o aquecimento corre na bancada;
  - na revelação, o resultado sai da bancada para a apresentação em destaque, com o véu, o nome com o nível, a peça,
    as propriedades antes → depois, "SUCESSO" ou "FALHOU" e o OK;
  - o resultado fica até OK, Enter ou Esc.
- **Encantar:**
  - um botão por essência (a quantidade soma os tiers);
  - o tier se escolhe ao lado da previsão, que mostra "Nesta peça 3 → 6 · Jean 3 → 5", o efeito no nível novo e o
    aviso quando parte (ou tudo) passa do teto;
  - substituir pede confirmação;
  - a gravação concluída aparece na mesma apresentação em destaque, sem suspense.
- **Transferir:** a peça escolhida é a origem; à direita, os destinos possíveis, cada um com "+2 → +8" ou o motivo de
  não poder; a confirmação mostra os dois resultados e o preço.
- **Desmontar:** a confirmação no pé, com as perdas; a transformação é curta, sem celebração.
- **Gestos:**
  - as confirmações só aceitam o clique depois de 400 ms;
  - o segundo clique de um clique duplo não age;
  - a tecla segurada não repete;
  - o gesto que adianta a cena não dispensa o resultado;
  - o resto do gesto que dispensa não chega à bancada;
  - Esc revela, cancela a confirmação e fecha, nessa ordem.

## 10. Linguagem visual [Protótipo]
- **Raridade:** a cor da borda do encaixe e do nome.
- **Reforço:** o acabamento sobre o desenho da peça.
  - +1 a +4: o reflexo; o +4 com contorno dourado.
  - +5 a +8: turquesa, safira, ametista e rubi.
  - +9 a +12: o veio multicolorido em pixel, com brilhos.
  - O +N fica no canto do encaixe e, nas dicas, colorido pelo nível.
- **Gravação:** um rastro de luz na cor da essência percorre a borda do encaixe. A ficha mostra os sulcos (os vazios
  também), os nomes com o tier e um efeito por linha; os detalhes ficam em "Como funcionam", por clique ou teclado.
- **Seleção e foco:** os cantos de latão e o anel de foco não mudam com o acabamento.

## 11. Casos de teste e exemplos

**Testes automáticos** (`ferramentas/prototipos/reforco/testes`, 45):
- reforço em todos os espaços, sem cair, com a arma sentindo cada passo até o +4;
- forma fechada sem deriva;
- tetos de %;
- transferência (resultado, conservação, cobrança única, nada se cria, cadeia);
- tiers que somam, e só o que se veste conta;
- teto;
- textos por nível;
- a ficha com o total;
- o saque real dando materiais pela criatura;
- Carrasco pela tabela; Revide pelo nível total e no máximo 2 por rodada; Eco até 2 por luta;
- lutas de verdade;
- salvar e carregar.

**Cenários da faixa da demonstração** (só no save temporário):
- **Níveis altos (teste):** peças de +4 a +12, duas com três gravações.
- **Essências (teste):**
  - Jean: Brasa II + Brasa I + Carrasco I (Brasa 3); Vigília III + Revide II + Geada I;
  - Odette: Eco 7, acima do teto;
  - Morel: Revide II;
  - 3 essências de cada tier.
- **Transferência (teste):** na bolsa, uma arma comum +10, outra +2 (com Brasa), um peito incomum +6 e outro +0.
- Os demais: Sucesso e Falha (teste), Comparação e Luta de teste.

**Exemplo completo:** Jean veste a arma com Brasa II + Brasa I (Brasa 3). Na bolsa, uma armadura com Vigília III não
conta. Ao gravar Brasa III no terceiro sulco, a previsão diz "Nesta peça 3 → 6 · Jean 3 → 5" e avisa que 1 nível passa
do teto. Na luta, cada golpe que acerta tem 53% de chance de Queimadura, no máximo 1 vez por rodada.

## 12. Pendências para integrar e assuntos futuros
- **Equilíbrio em avaliação:** chances e custos do +5 ao +12 e o ouro (alto para a campanha curta); as tabelas das
  essências e o teto 5; as fontes e as chances de material. Julgar jogando a campanha ampliada.
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
  base; o dobro dos apoios; "a mesma essência não repete"; um efeito por essência gravada (agora, pelo nível total).
