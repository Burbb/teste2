# 16 — Saque do Vale e a primeira entrega da E7

Diagnóstico do saque do Vale do Turvo e especificação do primeiro item único com efeito de build (E7). Nada do jogo
mudou para isto: o saque foi medido por uma ferramenta nova (`python -m tests.saque_vale`), e o item não foi
implementado. **Os números, a candidata e as propostas de ajuste são propostas até a avaliação de Jean** (seção 6).

Versão do jogo medida: 1.62.5.

## 1. Resumo

**Saque.**
- Num Vale completo, o herói recebe em média 6,4 baús e uns 19 suprimentos de bolsa sem comprar nenhum. Metade
  desses suprimentos sai de baús.
- Gasta a maior parte das poções e dos tônicos. Antídoto, unguento e bomba de fumaça quase não são usados e se
  acumulam.
- No fim, a bolsa vale mais de 300 de ouro a preço de tabela, mais do que o ouro na mão. Suprimento não se vende e a
  bolsa não tem limite: o excesso não tem para onde ir.
- O que mais gera baús são os **inimigos com nome**, que sempre deixam um: 53% dos baús. Mais da metade deles são
  alvos de contrato do mural.
- O equipamento é sempre da classe do herói. Metade a três quartos melhora o que ele veste, conforme a origem.
- A pressão na mochila foi pequena com o roteiro medido, que vende tudo a cada visita à vila.

**Duas propostas pequenas** (seção 3):
- *aplicada na campanha na 1.62.6:* um suprimento por baú, em vez de um ou dois. A medida antes e depois está em 3.1;
- *complemento, não aplicado:* antídoto, unguento ou bomba que o herói já carrega vira ouro no baú.

**E7.** Recomendo o **Broquel do Vigia**, um escudo único do Guerreiro (seção 4).
- Com o escudo erguido, ele devolve cada golpe corpo a corpo que acerta o herói (**Revide**, 30% do Ataque).
- Usa o gatilho `golpe_recebido` que já existe. Não precisa de evento nem de chave nova de combate.
- Dá ao Erguer Escudo um papel além da defesa: contra dois ou mais inimigos corpo a corpo, erguer o escudo primeiro
  passa a valer mais do que repetir o Golpe Pesado. Contra um inimigo só ou contra magia, não muda nada.
- Vem do esqueleto de guarda do ossuário, uma vez, antes da escolha sobre Ilse.

## 2. Diagnóstico do saque do Vale

### 2.1 Como foi medido

A ferramenta `tests/saque_vale.py` joga o Vale inteiro com um robô e conta o que entra e o que sai. Ela não muda o
jogo: só usa as mesmas regras das telas (comprar, vender, aceitar contrato, abrir baú). A descrição completa do
roteiro está no topo do arquivo. Em resumo:

- **Vila:**
  - abre os baús;
  - aceita até dois contratos de caça no nível do herói;
  - compra comida até 5 dias;
  - compra no mercado a peça que melhora o equipamento;
  - veste o que melhora e vende o resto da mochila;
  - completa a lista de compras: tochas 4, poções 2, bandagens 2, antídoto 1, aljava cheia;
  - dorme na taverna com a vida abaixo de 75%.
- **Fora da vila:**
  - acampa à noite ou com a vida abaixo de 85%;
  - faz a ação de missão do lugar;
  - caça o contrato do lugar;
  - explora N vezes por visita, só onde o nível do lugar não passa o do herói;
  - antes das salas da capela, sobe até o nível 3, e antes do fundo, até o 4.
- **Roteiros:**
  - "direto": explora uma vez por visita;
  - "explorador": explora três vezes por visita e passa pelo Charco dos Juncos.
- **Desfechos:**
  - "descansada": fala com Vó Berta, solta as correntes, faz o rito e recebe a herança;
  - "destruida": luta até o fim, sem soltar as correntes.
  - A postura diante de Caspar é sorteada.
- **Luta:**
  - o lutador da arena (`tests/arena.py`);
  - usa antídoto com veneno, bandagem com sangramento e tônico com o recurso abaixo de 25%;
  - foge abaixo de 35% da vida sem poção, com a bomba de fumaça se tiver.
- **Equipamento achado:** veste se melhora; senão, guarda para vender.
  - "Melhora" usa a soma dos bônus com os pesos do preço (`PESO_PRECO`), sem o atributo de ataque que a classe não
    usa.
- **Eventos, conversas e especialização:** escolhas ao acaso.
- **Fim do percurso:** a Febre concluída (no rito, com a herança), a Vigília decidida, ou o dia 45.

**Amostra:**
- 480 percursos: 3 classes × 2 desfechos × 2 roteiros × 40 sementes.
- 136 percursos completos: Guerreiro 65, Arqueiro 53, Mago 18.
- As tabelas abaixo são dos **completos**, salvo onde diz.
- O mesmo herói, na mesma semente, joga igual até a escolha sobre Ilse. A diferença entre os desfechos é pareada.

Reproduzir: `python -m tests.saque_vale --sementes 40` (cerca de 50 segundos). A saída traz as mesmas tabelas para
todos os percursos e só para os completos.

### 2.2 Limitações

- **O robô não joga como uma pessoa.**
  - Ele bebe poção abaixo de 35% da vida. As partidas reais guardadas (versões 1.11 a 1.21, mundo gerado) usaram de
    zero a três poções em 6 a 33 lutas. Uma pessoa provavelmente acumula **mais** poções do que o robô.
  - Ele vende tudo a cada visita à vila, então a mochila nunca passou de 4 itens. Quem guarda itens para comparar
    sente mais a mochila.
  - Ele abre os baús assim que chega a um lugar seguro. Quem junta baús e abre vários de uma vez ("Baús ×N") vê muitos
    suprimentos de uma vez só.
- **72% dos percursos não terminam.** A maioria morre de fome nos níveis 1 e 2: o ouro do começo é curto, e o robô
  não sai dessa espiral.
  - O Mago é o mais frágil. No nível 1, perde para dois bandidos mesmo atacando primeiro.
  - Isso pesa mais no robô do que numa pessoa, mas é um sinal sobre o começo do Vale. Fica registrado em 2.7, sem
    proposta aqui.
  - Os percursos completos são os que passaram do começo. É neles que se vê o saque de um Vale inteiro.
- **Contratos e exploração são do roteiro.**
  - Quem não aceita contratos recebe menos baús (veja 2.3).
  - Quem explora mais recebe mais de tudo: compare "direto" e "explorador".
- **O mago completo tem pouca amostra:** 18 percursos.

### 2.3 Baús: frequência e origem

Por percurso completo: média de 6,4 baús, mediana 6, de 3 a 11.

| Origem | Por percurso | Parte | Tipo |
|---|---|---|---|
| Inimigo com nome (alvo de contrato) | 1,85 | 29% | sempre dá baú; quantos aparecem depende do roteiro |
| Inimigo com nome (viagem e exploração) | 1,58 | 25% | sempre dá baú; aparece por sorteio (nêmesis, líder de bando, o líder sorteado de um grupo) |
| Sacristia | 1,0 | 16% | fixo (missão) |
| Guardiã (Ilse) | 1,0 | 16% | fixo (chefe), nos dois desfechos |
| Sorteado (luta comum ou de elite) | 1,0 | 15% | sorteio (`BAU_COMUM` 3%, `BAU_ELITE` 12% por elite) |

- **Recompensa fixa:** 2 baús por Vale (a sacristia e a guardiã).
- **Garantido por regra:** todo inimigo com nome deixa baú (`saque_de_combate`: `chefe or unico`), em média 3,4 por
  Vale. É a maior fonte, e o roteiro de contratos a dobra.
- **Sorteado:** 1 baú por Vale.
- **Cada baú dá:**
  - ouro;
  - 1,5 suprimento em média (`BAU_SUPRIMENTOS`, de 1 a 2);
  - um equipamento em 48% das vezes.

### 2.4 Suprimentos: o que entra, o que se gasta, o que sobra

Média por percurso completo:

| Item | Início | Baú | Luta | Evento | Comprado | Gasto | No fim | A compra do roteiro |
|---|---|---|---|---|---|---|---|---|
| Poção de Vida | 2,0 | 2,3 | 0,5 | 2,1 | 1,3 | 5,1 | 3,0 | até 2 |
| Bandagem | 2,0 | 1,9 | 1,2 | 0,6 | 1,1 | 2,8 | 4,0 | até 2 |
| Tônico Restaurador | 0,1 | 1,1 | 0,6 | 0,7 | — | 1,8 | 0,7 | — |
| Antídoto | — | 1,0 | 0,5 | 0,7 | 0,6 | 0,3 | 2,5 | até 1 |
| Unguento de Prata | — | 1,2 | — | 0,4 | — | 0,1 | 1,4 | — |
| Bomba de Fumaça | — | 1,2 | — | 0,9 | — | 0,6 | 1,5 | — |
| Tocha | 3,0 | 1,1 | 1,1 | — | 7,3 | 9,9 | 2,6 | até 4 |

"Luta" junta as lutas comuns e as da missão.

- **Poção e tônico se gastam.** Entram cerca de 8 poções (com 1,3 comprada) e 5 se gastam. As 3 que sobram ficam
  perto do que o roteiro mantém.
- **Os situacionais se acumulam.**
  - Antídoto: entram 2,8, gastam-se 0,3.
  - Unguento: entram 1,6, gastam-se 0,1.
  - Bomba: entram 2,1, gastam-se 0,6.
  - Saem quase todos de baú (3,4 por Vale) e de eventos.
- **Bandagens sobram um pouco:** 4 no fim, contra as 2 que o roteiro mantém.
- **No fim do Vale,** a bolsa tem de 11 a 22 suprimentos, 327 de ouro a preço de tabela. O ouro na mão é 211.
- **Não há saída para o excesso.**
  - Suprimento não se vende: o mercado compra só equipamento da mochila.
  - A bolsa não tem limite.
  - Nos percursos que morreram de fome, a bolsa tinha em média 4,6 suprimentos (39 de ouro a preço de tabela) que
    não viram comida.
- **Os baús guardam pouco do que se gasta.** Do que sai de baú, só 2,4 por Vale chegam quando o herói já tem 3 ou mais
  do mesmo item. Quase tudo isso são bandagens e tochas, que o roteiro compra.
  - O excesso não é "o mesmo item de novo". São itens de uso raro, um ou dois de cada, que ficam.

**Conclusão:** a impressão de "consumíveis demais" tem fundamento. O volume é alto: metade dos suprimentos achados
vem de baús, e 1,5 por baú. O excesso que fica é de itens situacionais. Poções e tônicos não são o problema.

### 2.5 Equipamento: achado, utilizável e melhoria

Média por percurso completo:

| Classe | Baú | Luta | Luta da missão | Evento | Missão (fixo) | Melhora o vestido |
|---|---|---|---|---|---|---|
| Guerreiro | 3,2 | 4,8 | 1,5 | 1,7 | 1,0 | baú 73%, luta 50%, evento 67% |
| Arqueiro | 3,1 | 3,8 | 1,8 | 1,9 | 1,0 | baú 68%, luta 62%, evento 70% |
| Mago | 2,3 | 3,8 | 1,6 | 2,0 | 1,0 | baú 74%, luta 50%, evento 67% |

- **Todo equipamento achado é da classe do herói.** `gerar_equip` usa a classe, e os únicos de outras classes ficam
  fora do sorteio. Não há "item que não serve".
- **Raridade:**
  - de baú: cerca de 40% comuns, 30% mágicos, 22% raros e 6% lendários;
  - de luta comum: cerca de 65% comuns.
- **A recompensa fixa da missão quase sempre melhora o que se veste** (91% a 94%):
  - a herança de Vó Berta (raro da classe) ou a Pele do Penitente (lendário).
- **O trabalho de comparar e vender:**
  - por Vale, uns 12 cartões de item, cada um uma decisão;
  - de 7 a 12 vendas;
  - de 6 a 8 compras de equipamento no mercado (esta só no roteiro);
  - um terço a metade dos cartões não melhora nada: é só trabalho de olhar e vender.
- **Por que a melhoria parece alta:** o herói começa só com a arma. Os primeiros achados preenchem espaços vazios.
- **O que se perderia trocando suprimentos por equipamento comum:**
  - um cartão a mais por baú;
  - em mais da metade das vezes, para olhar e vender.
  - Por isso nenhuma das propostas abaixo faz essa troca.

### 2.6 Bolsa, venda e ouro

Média por percurso completo:

| Classe | Desfecho | Ouro: entrou (maiores fontes) | Saiu (maior) | Vendas | No fim |
|---|---|---|---|---|---|
| Guerreiro | descansada | lutas 212, baús 190, eventos 138, contratos 107 | mercado 476 | 172 | 260 |
| Guerreiro | destruida | lutas 199, baús 177, eventos 130, contratos 88 | mercado 347 | 72 | 245 |
| Arqueiro | descansada | lutas 203, baús 177, eventos 124, contratos 107 | mercado 480 | 161 | 203 |
| Arqueiro | destruida | lutas 191, baús 161, eventos 132, contratos 82 | mercado 390 | 102 | 181 |
| Mago | descansada | lutas 188, baús 153, eventos 111, contratos 79 | mercado 457 | 125 | 108 |
| Mago | destruida | lutas 163, baús 128, eventos 117, contratos 66 | mercado 319 | 62 | 121 |

- **O ouro dos baús é a segunda fonte** (cerca de 25% do que entra).
- **No começo, o ouro é curto.** No fim, sobra. A espiral de fome do robô acontece nos níveis 1 e 2, antes dos
  baús e dos contratos maiores.
- **A mochila (12 espaços) não apertou** com este roteiro: no máximo 3 ou 4 itens, nada deixado para trás.

### 2.7 Classes e desfechos

- **Entre as classes, o saque é parecido.**
  - O Mago recebe um pouco menos de baús e de suprimentos porque completa menos e explora menos, não por regra.
  - Todas recebem itens da própria classe.
- **Entre os desfechos, o saque é quase o mesmo.**
  - Os achados por Vale ficam entre 18 e 20 nos dois.
  - A guardiã dá baú nos dois.
  - Muda a recompensa fixa: o raro da classe (descanso) ou a Pele do Penitente (destruir).
  - As diferenças de "comprados" e "vendidos" vêm do roteiro: o descanso passa mais vezes pela vila (Vó Berta e a
    herança) e por isso compra e vende mais.
- **Registrado, sem proposta aqui:** o começo do Vale derruba o robô, em especial o Mago (11% dos percursos de Mago
  terminam, contra 41% dos de Guerreiro). É assunto de dificuldade e economia do começo (E9), não de saque. Precisa
  de confirmação jogando.

## 3. Propostas de ajuste do saque

Nenhuma muda frequência de baús, economia de ouro ou recompensas fixas. As duas mexem só no que o baú tira da lista
de suprimentos. A medida antes e depois é feita com `tests.saque_vale` e com o ciclo do COMO_CRIAR.

**Estado:**
- A P1 foi **aplicada na 1.62.6**, só na campanha. O resultado está em 3.1.
- A P2 não foi aplicada (decisão de Jean).
- Falta Jean jogar.

### P1. Um suprimento por baú — aplicada na campanha (1.62.6)

- **O que muda:** `sortear_bau` tira **um** suprimento da lista (`BAU_SUPRIMENTOS`), em vez de um ou dois. A lista e o
  resto do baú (ouro, chance de equipamento) ficam iguais.
- **Efeito esperado** (por Vale completo, a partir da seção 2):
  - suprimentos de baú: de 9,7 para cerca de 6,4;
  - situacionais de baú: de 3,4 para cerca de 2,2;
  - suprimentos achados no total: de cerca de 19 para cerca de 16.
  - Poções de baú caem de 2,3 para cerca de 1,5. Ainda sobram poções no fim (2,2 em média).
- **Por que esta:**
  - ataca o volume, que é o que se percebe ao abrir baús;
  - é um número só;
  - não troca suprimento por equipamento e não cria tela.
- **Custo:** o baú fica um pouco menos generoso. O ouro e o equipamento continuam sendo o que o baú traz de mais
  relevante.

### P2. Situacional repetido vira ouro — complemento, só se a P1 não bastar

- **O que muda:** quando o suprimento sorteado for antídoto, unguento ou bomba de fumaça e o herói já tiver pelo menos
  um, o baú dá o equivalente em ouro, metade do preço de tabela:
  - antídoto 7;
  - unguento 15;
  - bomba 17.
  - O quadro do baú mostra só o ouro somado.
- **Efeito esperado:**
  - −1,8 situacional por Vale;
  - cerca de +20 de ouro por Vale.
  - O herói continua recebendo o primeiro de cada um.
- **Por que só depois:** é uma regra que depende da bolsa e precisa ser explicada (por que o baú deu ouro e não o
  antídoto). Se a P1 resolver a impressão de excesso, não é preciso.

### 3.1 A P1 medida, antes e depois (1.62.5 e 1.62.6)

**Como ficou:**
- Na campanha, `sortear_bau` tira um suprimento só (`BAU_SUPRIMENTOS_CAMPANHA = 1`). O sorteio de quantos deixou de
  acontecer.
- O mundo gerado continua com um ou dois (`BAU_SUPRIMENTOS = (1, 2)`), na mesma ordem do sorteio. O gabarito não
  mudou: as partidas dele são do mundo gerado.
- Ouro, chance de equipamento, frequência de baús e recompensas fixas ficam iguais.

**Como medi:** `python -m tests.saque_vale --sementes 40`, com o mesmo roteiro, antes e depois. São 480 percursos de
cada lado. O resto do sorteio muda com a mudança, então cada percurso não é pareado; os percursos seguem caminhos um
pouco diferentes.

**Percursos completos, média por Vale:**

| | Antes (136 completos) | Depois (150) |
|---|---|---|
| Baús | 6,4 | 6,4 |
| Suprimentos de baú | 9,7 | 6,3 |
| Suprimentos achados (sem compra) | 18,4 a 19,7 | 15,2 a 18,8 |
| Gastos (com tochas) | 19 a 24 | 19 a 23,5 |
| Na bolsa no fim | 10,9 a 19,0 | 10,4 a 16,7 |
| Poções no fim | 3,0 | 2,4 |
| Antídoto / unguento / bomba no fim | 2,5 / 1,4 / 1,5 | 2,1 / 1,1 / 1,1 |

**Entrada, consumo e estoque por item** (completos, média por Vale; antes → depois):
- **Poção de Vida:**
  - de baú: 2,3 → 1,4;
  - gastas: 5,1 → 4,9;
  - no fim: 3,0 → 2,4.
- **Bandagem:** de baú 1,9 → 1,3; gastas 2,8 → 2,7; no fim 4,0 → 3,7.
- **Tônico:** de baú 1,1 → 0,7; gastos 1,8 → 1,5; no fim 0,7 → 0,6.
- **Situacionais** (antídoto, unguento, bomba):
  - de baú: 3,4 → 2,0;
  - gastos: 1,0 → 1,1;
  - no fim: 5,4 → 4,3.

**Por classe** (completos; antes → depois):
- **Guerreiro:**
  - achados 18,4–19,7 → 15,2–16,3;
  - na bolsa no fim 13,8–19,0 → 11,7–16,7;
  - completos 65 → 70.
- **Arqueiro:**
  - achados 18,4–19,6 → 15,3–15,7;
  - no fim 12,4–18,0 → 10,4–15,2;
  - completos 53 → 60.
- **Mago:**
  - achados 18,3–18,8 → 17,1–18,8;
  - no fim 10,9–15,8 → 12,6–15,0;
  - completos 18 → 20. A amostra é pequena e não sustenta uma conclusão.

**O começo do jogo, com os interrompidos** (todos os percursos; antes → depois):

| Classe | Completos | No dia 45 | Parados (fome / infecção) | Nível ao parar | Na bolsa ao parar | Ouro ao parar |
|---|---|---|---|---|---|---|
| Guerreiro | 65 → 70 | 11 → 12 | 84 (74 / 10) → 78 (70 / 8) | 1,6 → 1,6 | 4,5 → 4,2 | 2,5 → 2,6 |
| Arqueiro | 53 → 60 | 23 → 21 | 84 (82 / 2) → 79 (75 / 4) | 2,0 → 1,9 | 4,2 → 4,5 | 1,8 → 2,1 |
| Mago | 18 → 20 | 30 → 29 | 112 (96 / 16) → 111 (91 / 20) | 1,7 → 1,8 | 5,0 → 5,1 | 2,2 → 1,5 |

Depois da mudança, os percursos interrompidos:
- abriram em média só de 0,2 a 0,4 baú;
- ganharam de 36 a 65 de ouro no total;
- pararam **sem nenhuma poção**, com 4 a 5 suprimentos que não viram comida;
- lutaram de 9 a 10 vezes e caíram de 1,7 a 3,1 vezes.

**Conclusão:**
- A P1 tira o que pretendia: cerca de um terço dos suprimentos de baú. O excesso no fim diminui, sem faltar poção a
  quem completa (2,4 no fim, depois de gastar 4,9).
- O excesso de situacionais diminui, mas não some: 4,3 por Vale no fim. A P2 continua de reserva.
- **O começo do jogo não depende dos baús.** Quem para quase não viu baú, e a mudança não mexeu nele. A pequena alta
  de completos fica dentro do ruído do sorteio.
- Os recursos do começo não bastam para o robô: ele para sem poção, quase sem ouro e com fome. Os 150 que completam
  não provam que bastam. Pode ser um limite do robô (seção 2.2), mas fica registrado como problema aberto do começo
  (E9), sem ajuste nesta entrega.

**Não proposto, registrado:** os inimigos com nome sempre deixam baú (53% dos baús). Se, depois da P1, Jean ainda
achar que há baús demais, o ponto de ajuste é este. Por exemplo, o alvo de contrato daria baú com a chance de elite. Isso
mexe na frequência, que este pedido deixou de fora.

## 4. E7: a primeira entrega

### 4.1 Escopo

O 05 e o 07 pedem:
- um único com efeito relevante para uma build, com ficha completa;
- aquisição;
- feedback na luta;
- economia;
- reforço funcionando.

Depois, poucos exemplos para os três estilos. Ficam de fora:
- avalanche de saque;
- catálogo de únicos em massa;
- reforço feito do zero.

O que o diagnóstico da E5 (14, seção 1) deixou para resolver:
- o Guerreiro e o Arqueiro repetem o golpe principal quase todo turno;
- as ações de preparo rendem menos em lutas curtas;
- o Erguer Escudo só vale contra o golpe preparado.

O Mago já recebeu a transformação da E6.

### 4.2 As candidatas

| | A. Broquel do Vigia | B. Aljava do Rastreador | C. Manopla do Juramento |
|---|---|---|---|
| Classe e espaço | Guerreiro, apoio (escudo) | Arqueiro, apoio (aljava) | Guerreiro, mãos |
| Efeito | Com o escudo erguido, devolve cada golpe corpo a corpo que acerta o herói (30% do Ataque) | Contra o alvo marcado, o ataque básico não gasta flecha e devolve 2 de Foco | Atordoar quem prepara um golpe devolve o Vigor gasto e deixa o próximo golpe crítico |
| Decisão que cria | Escudo primeiro contra 2+ inimigos corpo a corpo; Golpe Pesado contra um só ou contra magia | Marcar e atirar básico em luta longa ou com poucas flechas | Investida em vez de Golpe Pesado quando alguém prepara |
| Onde aparece no Vale | Toda luta com grupo corpo a corpo: lobos, javalis, esqueletos, afogados, bandidos | Só em luta longa (chefe) ou com a aljava no fim. As lutas comuns duram de 3 a 5 turnos, e o Foco não aperta (14, 2.1) | Só nas duas lutas fixas com golpe preparado na capela |
| O que o motor já tem | Gatilho `golpe_recebido`, estado `guarda`, golpe de reação (`reacao=True`) | Gatilho `ataque_basico`, estado de marca | Nada para "interrompeu"; precisa de evento novo e de um estado de "próximo golpe crítico" |
| Extensões | Nenhuma de combate; só apresentação e a regra de não somar com o Contra-ataque | Nenhuma de combate | Um evento e um estado |
| Risco | Escudo permanente com Muralha (a medir) | Efeito invisível em lutas curtas | Raro demais para justificar um item |

**Recomendada: A.**
- É a única que cria uma decisão em lutas comuns do Vale.
- Torna perceptível um botão que hoje quase não se usa.
- Não pede evento nem chave nova de combate.
- A B é a melhor ideia para o Arqueiro numa segunda entrega, se o Foco e as flechas passarem a apertar.
- A C fica para quando o golpe preparado aparecer fora da capela.

### 4.3 Broquel do Vigia (especificação)

**Identidade.**
- Nome: "Broquel do Vigia". Id fixo: `broquel_do_vigia`.
- Escudo do vigia da capela: o esqueleto de guarda do ossuário, o que prepara o golpe esmagador (P1 da E5).
- Lore (sem explicar a regra): "Ficou preso ao braço do vigia da capela muito depois de a carne ir embora."
- Ícone: `escudo`. Base: "Broquel" (já existe em `PECAS["secundaria"]["guerreiro"]`).

**Espaço e classe.** Apoio (`secundaria`), só o Guerreiro: é a única classe que usa escudo.

**Bônus (propostos).**
- Catálogo: `{"defesa": 0.6, "max_hp": 4}`, escalado por `fazer_unico`:
  - nível 3: Defesa 2, Vida 7;
  - nível 4: Defesa 2, Vida 8;
  - nível 5: Defesa 2, Vida 9.
- Fica perto de um escudo raro do mesmo nível (no nível 4, em média Defesa 1,8 e Vida 5, mais um afixo) e bem abaixo
  da Égide do Mártir (no nível 4: Defesa 5, Vida 20, espinhos 7).
- O valor do Broquel está no efeito, não nos números.

**Efeito: Revide.**
- **Quando:**
  - o herói está em guarda (o estado `guarda`, que hoje só o Erguer Escudo põe no herói);
  - um inimigo vivo o acerta com um golpe corpo a corpo (`alcance == "corpo"`).
- **O que faz:** o herói devolve um golpe de **30% do Ataque** nesse inimigo.
  - É um golpe de verdade: pode ser esquivado, pode ser crítico e soma o dano corpo a corpo de talentos e estados.
  - Vai na tela como reação, com o nome "Revide" na cabeça do herói, como o Contra-ataque.
- **Conta:**
  - golpe absorvido por barreira (acertou);
  - golpe preparado corpo a corpo (o escudo corta metade e o Revide responde).
- **Não conta:**
  - golpe esquivado;
  - golpe à distância (a Esfera Sombria, a Bola de Fogo, o ataque básico de quem tem mais Poder que Ataque, como os
    cultistas e Ilse);
  - golpe num aliado (comitiva, animal);
  - golpe que derruba o herói (o gatilho só roda com ele de pé).
- **Limites:**
  - um Revide por golpe recebido;
  - o Revide não gera outro Revide nem outra reação;
  - não conta como ataque básico.
  - Sem teto por rodada. A alavanca, se a medida pedir: no máximo dois por rodada inimiga.
- **Custo:** nenhum próprio. Usa o Erguer Escudo (8 de Vigor, 2 turnos; com Muralha, 4 de Vigor e 3 turnos).

**Quando vale equipá-lo, e o que se perde.**
- **Vale:**
  - contra grupos corpo a corpo: lobos, javalis, esqueletos, afogados, bandidos;
  - diante do golpe preparado corpo a corpo;
  - para quem já tem Muralha.
- **Não vale:**
  - contra um inimigo só (o turno do escudo custa um Golpe Pesado);
  - contra conjuradores e atiradores;
  - com comitiva que puxa os golpes para si: menos golpes no herói, menos Revide.
- **O que se perde ao tirar o escudo anterior:**
  - de um escudo comum ou mágico: quase nada, pelos números;
  - de um raro: o afixo dele;
  - da Égide do Mártir: 3 de Defesa, 12 de Vida e 7 de espinhos no nível 4. É a troca mais clara entre defesa passiva
    (Égide) e defesa que pede o botão (Broquel).

**Aquisição e os dois desfechos.**
- **Onde:**
  - no ossuário, depois da vitória sobre o esqueleto de guarda;
  - para o Guerreiro, uma vez.
  - "No braço do esqueleto de guarda ficou um broquel de ferro escuro, ainda preso pela correia." Depois, o cartão do
    item, com as regras de sempre: equipar, guardar ou deixar para trás com a mochila cheia, como a Pele do Penitente.
- **Nível do item:** o do lugar mais um (o vigia), limitado ao nível do herói mais dois, como a Pele.
- **Sem sorteio:** fica fora do sorteio de lendários (`sorteio=False` no catálogo). Só vem do ossuário. Não depende de
  sequência de sorteios e não se duplica.
- **Os dois desfechos:** vem antes da escolha, então serve aos dois.
  - **Na descida:** Ilse ataca quase sempre com magia à distância, e o Revide não a alcança. A exceção é o Toque
    Drenante, que é corpo a corpo e o Revide responde. Os afogados que ela chama lutam corpo a corpo, e é neles que o
    Broquel rende. Erguer o escudo quando os afogados sobem é a decisão da luta.
    - No rito, isso ajuda a aguentar até o momento do nome sem pressa.
    - No destruir, abre caminho até ela.
  - **Destruir dá a Pele do Penitente**, que traz espinhos. Pele e Broquel combinam: os espinhos ferem quem bate, e o
    Revide responde. Dá uma build de "muralha" depois do Vale.
  - **Dar descanso dá a herança, um raro da classe.** Se a herança vier escudo, a comparação com o Broquel aparece ali
    mesmo.
- **Saves já avançados:** num save de Guerreiro em que o ossuário já foi vencido e o item ainda não foi dado (a marca
  `e7:broquel_do_vigia` não existe), o ferreiro do Vau o oferece uma vez.
  - Uma opção no balcão: "Ferreiro: o broquel que trouxeram da capela", sem custo.
  - A marca é gravada quando o cartão do item aparece, por qualquer dos dois caminhos. Não há segunda cópia.
  - Saves de outras classes, ou de antes do ossuário, não mudam.

**Descrição, comparação e feedback.**
- **Ficha do item** (cartão do saque, mercado, mochila, inventário):
  - uma linha nova, "Efeito", na cor do lendário, embaixo dos bônus: "Revide: com o escudo erguido, você devolve cada
    golpe corpo a corpo que te acerta (30% do Ataque)."
  - Na comparação, o cartão do escudo vestido aparece ao lado, como hoje. O Efeito mostra o que o Broquel acrescenta;
    os bônus mostram o que se perde.
- **Grimório, na página do Erguer Escudo,** enquanto o Broquel está vestido: "Com o Broquel do Vigia: devolve cada
  golpe corpo a corpo que te acerta enquanto o escudo está erguido (30% do Ataque)."
- **Na luta:**
  - o selo de "em guarda" ganha a dica "revida golpes corpo a corpo";
  - cada Revide é um golpe de reação com o nome "Revide";
  - no texto: "[Revide] Você atinge o esqueleto: 5 de dano."
- **Telemetria:** o Revide entra no dano por habilidade ("Revide"), para medir quanto rende.
- **Critério editorial:**
  - o custo é o do Erguer Escudo, já explícito no botão;
  - o Efeito diz a condição: escudo erguido, corpo a corpo;
  - a confirmação é o próprio golpe na tela, sem frase extra.

**Interações.**
- **Talentos do Guerreiro:**
  - **Contra-ataque:** não somam no mesmo golpe. Com o escudo erguido, responde o Revide (certo, 30%); sem escudo,
    vale o Contra-ataque de sempre (chance de 15% por ponto, 70%). Pede uma linha no gatilho do Contra-ataque.
  - **Muralha:** um turno a mais de guarda e 4 de Vigor a menos, então mais Revide por Vigor. É a combinação principal,
    e o risco a medir.
  - **Golpe Brutal:** o dano corpo a corpo vale no Revide. **Pele de Ferro, Fôlego:** nada de especial.
  - **Paladino:**
    - Aura de Proteção: o golpe absorvido pela barreira ainda é revidado;
    - Martírio: roda antes do Revide (ordem 10 contra 15).
  - **Berserker:**
    - Pacto de Sangue aumenta o Revide, mas o escudo diminui o quanto ele fica ferido: uma tensão de build, de
      propósito;
    - Sede Insaciável cura com o Revide;
    - Frenesi conta o abate por Revide;
    - Imortal roda antes, no golpe fatal.
- **Espinhos** (Pele do Penitente, afixos): valem os dois no mesmo golpe. Os espinhos são passivos e o Revide é um
  golpe.
- **Transformação ativa (E6):** o Guerreiro não tem nenhuma hoje. O Revide lê o estado `guarda`, não o id da
  habilidade. Uma futura variante do Erguer Escudo que ponha `guarda` mantém o Revide; uma que não ponha, não.
- **Comitiva:** golpes na comitiva não geram Revide. O Broquel rende mais sozinho ou com quem não puxa os golpes. Fica
  dito no Efeito ("que te acerta").
- **Invocações:**
  - invocados inimigos (os afogados de Ilse, os esqueletos de um conjurador) são inimigos e recebem Revide;
  - o Guerreiro não tem invocação própria;
  - o animal do Patrulheiro e os servos do Necromante não usam o equipamento do herói.

**Equipar, retirar, reforçar, vender e salvar.**
- **Equipar e retirar:** o efeito vem de `fonte_item` sobre o que está vestido. Entra e sai com o item, fora da luta.
- **Reforçar:** o ferreiro reforça o apoio. O nome ganha "+N" e a Defesa sobe. O efeito continua, porque o único é
  reconhecido pelo id (`unico_de`).
- **Vender:** pelo preço do lendário (cerca de 50 no nível 4), com a recompra da mesma visita. Vendido, não volta: não
  há segunda cópia.
- **Salvar e carregar:** o save guarda o item com o id. O efeito sai do catálogo e não é gravado. Num save de antes da
  E7, o item não existe e nada muda (a não ser a oferta do ferreiro, descrita acima).

**Abuso, acumulação, ciclos e isolamento (o que os testes precisam cobrar).**
- **Repetição:** o escudo sempre de pé (Muralha: 4 de Vigor para 3 turnos, com o Vigor voltando 6 por turno) é o
  risco. A medida diz se o Broquel vira a escolha de toda luta. Se virar, a alavanca é o teto por rodada ou 25%.
- **Acumulação:**
  - o efeito tem uma fonte só (um espaço, um item, sem sorteio);
  - o Contra-ataque não soma no mesmo golpe;
  - não há outra fonte de Revide.
- **Ciclos:** o Revide é reação. Ele não dispara Revide, Contra-ataque nem `ataque_basico`, e inimigo nenhum reage a
  reação. Abater com Revide dispara `abate` uma vez, como qualquer golpe.
- **Isolamento:**
  - outro herói, outro save, a comitiva e os inimigos não têm o efeito;
  - a arena e o replay não mudam, porque o item não entra no sorteio.

### 4.4 Extensões necessárias

1. **Catálogo:**
   - o único ganha `efeito` (texto da ficha) e `sorteio=False` (fora do sorteio de lendários, filtrado em `_unico`);
   - `gatilhos` e `ordem` já existem.
2. **Contra-ataque:** o gatilho do talento não age quando o Revide já respondeu ao golpe (`dados["revidou"]`).
3. **Apresentação:**
   - `itens.ficha` leva o `efeito`, e a tela o desenha no cartão;
   - o Grimório mostra o efeito de item ligado a uma habilidade (no catálogo, `realca: "erguer_escudo"`);
   - o selo da guarda ganha a dica.
4. **Aquisição:** o ossuário oferece o item ao Guerreiro (com a marca); o ajuste de save e a opção única do ferreiro.
5. **Telemetria:** o Revide no dano por habilidade.

Nenhum evento, chave de `mod` ou estado novo de combate.

### 4.5 Como medir

Por lutas inteiras e por uso da decisão, não por dano total:

- **Heróis:**
  - Guerreiro nos níveis 3, 4 e 5, Paladino e Berserker;
  - equipamento mediano (`dev.vestir`);
  - com e sem Muralha e Contra-ataque;
  - sem comitiva e com um companheiro.
- **Escudo comparado:** o Broquel contra três alternativas do mesmo nível:
  - um escudo raro típico;
  - a Égide do Mártir;
  - nenhum escudo.
- **Situações:**
  - um inimigo corpo a corpo;
  - dois e três corpo a corpo;
  - misto (dois corpo a corpo e um conjurador);
  - só conjuradores;
  - o golpe preparado (esqueleto de guarda, afogado inchado);
  - Ilse com os afogados, no rito e no destruir;
  - e lutas emendadas (`equilibrio`, "Lutas até descansar").
- **Políticas do robô:**
  - o lutador de sempre;
  - o lutador que ergue o escudo primeiro com dois ou mais corpo a corpo vivos.
  - O Broquel tem de ganhar onde a decisão diz e não onde não diz.
- **Colunas:**
  - vitórias, turnos, vida perdida;
  - poções gastas, Vigor no fim;
  - quedas em sequência;
  - parte dos turnos com o escudo de pé (acima de 50% em todas as situações seria dominância).
- **O Vale inteiro:** `tests.saque_vale`, com o Broquel, para ver quantas vezes ele é vestido e quanto o Revide rende
  numa partida.
- **Antes e depois:** `tests.equilibrio --spec paladino,berserker` e `tests.replay` não devem mudar, porque o item não
  entra no sorteio. Se o gabarito mudar, só pela opção do ferreiro ou pelo ossuário na campanha.

### 4.6 Estimativa de um protótipo descartável

Antes de propor 30%, um protótipo fora do jogo (o item só na memória de um script, sem nada no repositório) mediu a
ordem de grandeza na arena. Setup:
- Guerreiro nível 4, `dev.vestir`, sem comitiva;
- 60 lutas por linha;
- três versões do herói:
  - o lutador de sempre, sem o item;
  - com o item, erguendo o escudo primeiro diante de dois ou mais corpo a corpo;
  - sem o item, erguendo o escudo primeiro.

| Situação | Sem o item | Item, escudo primeiro | Item + Muralha | Escudo primeiro sem o item |
|---|---|---|---|---|
| 1 lobo nível 4 | 3,6 turnos, 8% de vida | 3,5 turnos, 7% | 3,4 turnos, 6% | 3,6 turnos, 8% |
| 3 lobos nível 3 | 10,0 turnos, 44%, 58/60 | 7,7 turnos, 22%, 60/60 | 7,0 turnos, 15% | 14,3 turnos, 50%, 50/60 |
| 3 esqueletos nível 3 | 10,7 turnos, 47%, 50/60 | 8,9 turnos, 23%, 60/60 | 7,1 turnos, 13% | 13,2 turnos, 57%, 37/60 |
| 2 bandidos nível 4 | 8,1 turnos, 33% | 7,1 turnos, 20% | 6,7 turnos, 14% | 10,4 turnos, 34% |
| 2 cultistas (magia) | 8,1 turnos, 25% | igual | igual | igual |

- **A decisão só paga com o item.** Erguer o escudo primeiro sem o Broquel é pior em grupo.
- **Com 50% de Revide,** o protótipo derrubava a vida perdida contra três lobos para 15% sem Muralha. Por isso a
  proposta é 30%.
- **Com Muralha,** a vida perdida cai a 13%–15% em todos os grupos. É o ponto de atenção da medição de verdade.
- Isto é uma estimativa para escolher o número de partida, não a medição da entrega.

## 5. O que fica para depois

- **Na E7:**
  - um exemplo para o Arqueiro (a B, se o Foco ou as flechas passarem a pesar);
  - um para o Mago, que não dependa da Prisão de Gelo.
- **O começo do Vale** (2.7): fome e quedas nos níveis 1 e 2, em especial do Mago. É assunto de dificuldade (E9),
  confirmado jogando antes de qualquer número.
- **A saída para o excesso de suprimentos** (vender ou largar): só se as propostas do saque não bastarem. Vender
  suprimento é mais trabalho de comparar e vender, o que o próprio diagnóstico desaconselha.

## 6. Decisões pendentes (Jean)

1. **Saque:** aplicar a P1 (um suprimento por baú)? Depois de jogar com ela, decidir se a P2 é necessária.
2. **E7, a candidata:** o Broquel do Vigia (Guerreiro), ou começar pelo Arqueiro?
3. **E7, os números:**
   - Revide 30% do Ataque, sem teto por rodada;
   - bônus perto de um raro do mesmo nível.
4. **E7, a aquisição:** o ossuário (no meio do Vale, uma vez, antes da escolha sobre Ilse)? A alternativa é o ferreiro
   do Vau vender o Broquel desde o começo, por um preço: dá mais tempo de uso, mas pesa no ouro curto do começo.
5. **E7, o nome:** "Broquel do Vigia" e o efeito "Revide".
6. **Baús de inimigo com nome** (registrado, fora deste pedido): mexer na frequência só se, depois da P1, ainda houver
   baús demais.
