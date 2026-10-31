# 28 — Etapa 8: habilidades, talentos, builds e Grimório como um sistema (estudo)

**Revisão 2 — 31/10/2026.** Pedido do Jean depois de ler a primeira versão: usá-la como base, mas sem aprovar a
arquitetura nem o protótipo; ampliar além das respostas a preparações inimigas, reabrir a ordem dos turnos para análise,
aprofundar a construção das builds e os talentos, rever a regra das cadeias, corrigir as contradições das
demonstrações, separar a progressão desejada do capítulo provisório e redesenhar o protótipo.

**Entrega de pesquisa e concepção: nada daqui muda regras, telas ou conteúdo do jogo.** O jogo integrado (1.220.0)
continua como está. Os números são inventados para os exemplos funcionarem. **A arquitetura recomendada está pendente
de avaliação do Jean**; nenhuma proposta deste documento é regra aprovada.

"Etapa 8" é a do [plano 23](23-PLANO-DE-ARTE-INTERFACE-E-COMBATE.md) (habilidades, Grimório, árvore, ícones e
animações), não a E8 de raças e origens do [07](07-ETAPAS.md).

Como ler (cada seção diz a sua natureza):

| Seção | O que tem | Natureza |
|---|---|---|
| 0 | O encaminhamento das etapas 6, 7, 8 e 9 | Decisões do Jean |
| 1 | O que mudou desde a primeira versão, descobertas e decisões | Resumo |
| 2 | O jogo que temos, medido no código da 1.220.0 | Diagnóstico (evidência) |
| 3 | As referências e o que cada uma ensina | Pesquisa (evidência externa) |
| 4 | Regras de referência dos exemplos | Hipótese de trabalho (resolve as contradições da primeira versão) |
| 5 | Maneiras de jogar: responder, construir, arriscar, sustentar | Exploração |
| 6 | A ordem dos turnos, reaberta | Análise comparativa |
| 7 | A construção das builds e o papel dos talentos | Exploração e comparação de estruturas |
| 8 | Cadeias, abusos e o que conta como profundidade | Análise e proposta |
| 9 | A progressão, separada do capítulo atual | Proposta |
| 10 | O sistema completo: alternativas e recomendação | Recomendação pendente de avaliação |
| 11 | Builds diante dos mesmos encontros | Simulação de design (números inventados) |
| 12 | A campanha e a apresentação | Requisitos para a etapa 9 e a arte |
| 13 | As decisões que precisam do Jean | Para avaliação |
| 14 | O protótipo revisado | Proposta, não implementada |
| A | A primeira versão: o que foi substituído | Histórico |

A pergunta que guia tudo: **essas combinações mudam o que o jogador percebe, planeja, arrisca e decide durante a luta,
e continuam interessantes quando o plano dá errado?**

---

## 0. O encaminhamento: a etapa 8 antes da 9, as cenas de eventos depois das histórias

**Decisões do Jean (31/10/2026):** trabalhar a etapa 8 antes da etapa 9 (expansão e reescrita da campanha); as cenas
de eventos ficam para depois de as histórias deles estarem definidas. **Confirmado na revisão 2:** as cenas dos eventos
da estrada (etapa 7) também esperam a 9.

| Etapa | Pendência | Situação |
|---|---|---|
| 5 | Interiores (templo, curandeira, taverna) | Os três integrados (1.218.0 a 1.220.0); falta a avaliação do Jean. Não reabrir as artes aprovadas |
| 6 | Cenários dos lugares e entornos de acampamento | **Podem seguir** quando pedidos, conferindo, lugar a lugar, se ele continua na campanha |
| 6 | Cenas de acontecimentos (Caspar na praça e outros) | **Esperam a etapa 9** definir as histórias |
| 7 | Cenas dos eventos recorrentes da estrada | **Esperam a etapa 9** (confirmado pelo Jean) |
| 8 | Sistemas, Grimório, árvore, ícones e animações | **Agora**, por este estudo. Ícones e telas esperam o sistema escolhido (decisão de 19/10/2026) |
| 9 | Campanha | Depois da 8. Recebe da 8 os requisitos de encontros e de progressão (seções 9 e 12) |

---

## 1. Resumo da revisão 2

### 1.1 O que mudou em relação à primeira recomendação

| Assunto | Primeira versão | Revisão 2 | Por quê |
|---|---|---|---|
| Centro da profundidade | Ameaças legíveis (intenção, relógio, travas) explicavam quase tudo | São **um módulo entre quatro estilos**: responder, construir, arriscar, sustentar a comitiva | Builds que constroem o próprio mecanismo funcionam contra inimigos que não preparam nada (seções 5 e 11) |
| Talentos | Uma versão por habilidade e um ou dois princípios; números fora da árvore | **Árvore de regras por etiqueta**, com versões em poucas habilidades e números que disputam o orçamento | Versões são locais demais: não criam relações entre habilidades, e é isso que distingue builds da mesma especialização (seção 7) |
| Vocabulário de combinação | Pares feitos um para o outro (Brasa → Combustão) | **Produtos compartilhados**: estados, fichas, corpos, runas, o ambiente da luta, que várias fontes produzem e várias consomem | Combinações que ninguém desenhou como par (seção 7.4) |
| Ordem dos turnos | Manter fixa | **Reaberta.** Duas intervenções merecem teste (transferir a sua vez a um aliado; adiar a própria vez nesta rodada); mexer na posição de inimigos e gerar ações, não | O ganho e a perda de cada uma estão na seção 6 |
| Cadeias de gatilhos | Profundidade 1: efeito disparado não dispara nada | **Uma vez por cadeia, por efeito e por alvo**; quem gera recurso ou vez, uma vez por rodada | A profundidade 1 proíbe justamente as reações em cadeia que fazem uma build (seção 8) |
| Medida de dominância | Uma habilidade em mais da metade das ações | **A escolha depende do estado?** (alvo, momento, preparo, consequência) | Uma habilidade central pode concentrar decisões (seção 8.5) |
| Progressão | Especialização e ultimate no nível 4 | **Separada do capítulo:** escolhas de build desde os primeiros níveis, aprofundadas por fases; o que depende da 9 está marcado | O capítulo vai crescer (seção 9) |
| Demonstrações | Cinco contradições com as próprias regras | **Regras de referência primeiro** (seção 4), exemplos refeitos sobre elas e falhas classificadas por tipo | Pedido do Jean (seção 11) |
| Protótipo | Testava respostas ao mesmo contador | **Quatro experimentos separáveis**, com uma build que responde e outra que constrói, montagem e troca de talentos reais, encontros favoráveis e desfavoráveis | Seção 14 |

### 1.2 Descobertas que continuam valendo (diagnóstico, seção 2)

1. Só 3 das 17 famílias do Vale avisam uma ação; as outras sorteiam habilidade e alvo sem aviso.
2. O catálogo tem 45 habilidades de classe e especialização e cerca de dez decisões distintas.
3. 19 dos 34 talentos são só números; os que mudam o jogo ficam no nível 6 ou 9, e o capítulo termina perto do 4.
4. O recurso volta cheio a cada luta; ele limita o pico, não a sequência.
5. O motor já tem o que a maioria das propostas pede: passos declarados, gatilhos, versões por herói, preparação dos
   inimigos, o Firme, o clima afetando dano e esquiva, a regra de uma resposta por golpe.

### 1.3 Descobertas novas desta rodada

1. **Builds que constroem precisam de uma moeda própria e de um limite visível** (os orbes do Defect, as fichas de
   Darkest Dungeon II, o sangue e os ossos de Inscryption). O limite (espaços, teto de fichas, anulação entre fichas
   opostas) é o que cria a decisão de quando gastar. Seção 3.
2. **O nosso jogo já tem um "ambiente da luta" sem mapa:** o clima muda esquiva, dano por tipo e apaga queimaduras
   (`combate/golpe.py`, `estados._clima_apaga`). Habilidades que criam ou consomem um ambiente (névoa, óleo, água rasa)
   são a tradução das superfícies de jogos com mapa, sem posicionamento. Seção 5.
3. **Transferir uma vez não é gerar uma ação.** Passar a vez a um aliado (o "Baton Pass" de Persona 5) ou adiar a
   própria vez (o "Delay" de Pathfinder 2) mudam a sequência sem mudar quantas ações cada lado tem; é aí que está o
   ganho tático com risco controlado. Seção 6.
4. **Jogos de regras complexas impedem laços, não cadeias.** O Magic trata o laço de ações obrigatórias como empate e
   deixa as cadeias finitas acontecerem; combinações finitas e fortes (Corrupção + Galho Morto em Slay the Spire) são
   lembradas como o melhor do jogo. Seção 8.

### 1.4 A recomendação revisada, em uma frase (pendente de avaliação)

**Um vocabulário de produtos compartilhados** (estados, fichas, corpos, runas, ambiente) **sobre o qual uma árvore de
regras por etiqueta constrói estilos diferentes dentro da mesma especialização**, com versões em poucas habilidades,
números que disputam o orçamento, ameaças legíveis como módulo independente e duas intervenções delimitadas na ordem
dos turnos para testar. Detalhes e concessões na seção 10.

### 1.5 O que precisa da avaliação do Jean (lista completa na seção 13)

1. A estrutura dos talentos: árvore de regras por etiqueta, versões e princípios, ou selos.
2. Quanto da intenção inimiga mostrar, e se ela entra antes ou depois dos talentos.
3. Se a ordem dos turnos ganha as duas intervenções delimitadas.
4. A regra das cadeias.
5. As fases da progressão (o que vem cedo, o que vem com a especialização, o que a 9 decide).
6. O protótipo: quais dos quatro experimentos, e em que ordem.

---

## 2. O jogo que temos (diagnóstico na 1.220.0)

Lido no código (`rpg/habilidades.py`, `rpg/kit.py`, `rpg/talentos.py`, `rpg/estados.py`, `rpg/combate/turnos.py`,
`rpg/combate/golpe.py`, `rpg/inimigos.py`, `rpg/dados.py`, `rpg/classes.py`) e nos documentos
[14](14-E5-DIAGNOSTICO-CLASSES.md), [15](15-E6-TRANSFORMACAO.md), [17](17-E9-VALIDACAO-DO-VALE.md),
[21](21-DIAGNOSTICO-ATAQUES-EM-AREA.md), [25](25-ETAPA4-REFORCO-E-ENCANTAMENTO.md) e
[26](26-INTEGRACAO-DO-COMBATE.md). A medida do catálogo foi um script descartável sobre os dados do jogo (os passos de
cada habilidade), não uma partida.

### 2.1 O que já funciona no jogo

- **Ordem fixa por Agilidade**, turnos individuais, rodadas; quem entra no meio vai para o fim e age na rodada
  seguinte. A placa da rodada mostra a ordem.
- **Uma ação principal por vez:** Atacar, Defender (−40% até a sua próxima vez), Usar item ou uma habilidade do kit.
- **Kit** separado do Grimório: 8 pontos, 5 espaços, uma ultimate (comum 1 ponto, avançada 2, ultimate 3); troca na
  vila e na fogueira. A ultimate vale uma vez por luta, desde o nível 6.
- **Comitiva controlada:** você escolhe a ação de Odette, Morel e Yara, cada um com um kit fixo de três habilidades e
  recurso próprio de 40.
- **Habilidades como dados:** blocos que executam e se descrevem (`Dano`, `Se`, `Aplicar`, `Buff`, `Acender`, `Roubo`,
  `Curar`...), com `fn` própria para as particulares (Combustão, Redemoinho, Ordem da Fera, Execução, Erguer Servo).
- **Versões por herói (E6):** um talento libera outra ficha de uma habilidade (`VARIANTES`, `efetiva(u, h_id)`),
  escolhida no Grimório em lugar seguro. Um caso: a Prisão de Gelo, versão da Lança de Gelo.
- **Modificadores e gatilhos:** talentos, passivas, classe, especialização e itens declaram `mods`, `mults` e
  `gatilhos` (início da luta, golpe recebido, golpe fatal, ataque básico, abate, morte); o combate só pergunta `mod` e
  `disparar`.
- **Estados com regras declaradas:** duração, tique, perder a vez, imunes, resistência por sorteio (chefes e gigantes
  resistem metade do atordoamento), camadas (Queimadura até 3) e o **Firme** depois de perder a vez.
- **Preparação inimiga:** o Golpe Esmagador (`carregando`, ×2,2) avisa uma vez antes; atordoar no meio desfaz o golpe.
- **Clima na luta:** muda a esquiva, o dano por tipo e por alcance, e a chuva apaga parte da Queimadura
  (`combate/golpe.py`, `estados._clima_apaga`). É um ambiente global que ninguém controla.
- **Uma resposta por golpe:** o Contra-ataque e o Revide do Broquel marcam o golpe como `respondido`, e o segundo não
  dispara (`talentos._contra_ataque`, `itens.py`). É uma regra anti-laço que já existe, em pequeno.
- **Combinações que existem:** Brasa ou Chuva de Brasas → Combustão ou Conflagração; Quebra-Guarda → Golpe Pesado;
  Mirar → Tiro Certeiro; Investida → Golpe Oportuno de Morel; Runa da Fragilidade → Descarga ou Nevasca.

### 2.2 O que é provisório ou só planejado

- **Todos os números** do kit (8/5/3), custos, multiplicadores, recurso da comitiva, Defender 40%, Tenacidade, e o
  próprio catálogo ([26](26-INTEGRACAO-DO-COMBATE.md), "Provisório").
- **O Golpe Oportuno de Morel:** falta o Jean dizer se vira obrigação, como a Marca virou ([25](25-ETAPA4-REFORCO-E-ENCANTAMENTO.md), 3.9).
- **Pequenos caminhos por habilidade:** hipótese do Jean de até três melhorias por habilidade (25, 3.2).
- **Ultimate:** aquisição, disponibilidade e identidade em aberto (25, 3.2).
- **Grimório e árvore visuais:** funcionam, mas não estão no patamar atual; ícones esperam o sistema.
- **Alvo em aliado** para habilidades do herói: só pela comitiva e por Proteger ([04](04-HABILIDADES-E-TALENTOS.md)).
- **Pré-requisitos na árvore:** as linhas desenhadas não são regra de compra ([04](04-HABILIDADES-E-TALENTOS.md)).
- **Controle de animais e servos:** automáticos; decisão separada (25, 3.4).
- **Ataques em área anunciados:** recomendados no [21](21-DIAGNOSTICO-ATAQUES-EM-AREA.md), não feitos.

### 2.3 O que limita o design por decisão intencional

| Limite | Onde foi decidido | Situação nesta revisão |
|---|---|---|
| Sem posicionamento, distância, cones ou linhas | 25, 3.3 | Mantido |
| Ordem fixa; sem aceleradores, atrasos ou trocas de posição | 25, 3.5 | **Reaberta para análise** pelo pedido do Jean (seção 6); nada muda no jogo |
| Uma ação principal por vez; sem ações gratuitas por inferência | 25, 3.6 | Mantido; a seção 6 separa transferir de gerar ação |
| Kit limitado, troca fora da luta | 25, 3.1 e 3.10 | Mantido |
| Uma ultimate equipada, uma vez por luta, sem Ímpeto | 25, 3.8 | Mantido |
| Preparações perigosas sinalizadas com chance real de resposta | 25, 3.3 e 3.6 | Mantido |
| Marca do Morel recusada: preparação repetitiva que vira obrigação | 25, 3.9 | Mantido; o critério vale para qualquer pedágio |
| Tenacidade como chance, não imunidade binária | 26, pesquisa | Mantido |
| Grupo ativo: herói e até dois companheiros | 25, 3.4 | Mantido |
| Companheiro caído só volta por ressurreição cara ou item escasso | 25, 3.4 | Mantido |

### 2.4 O que é só limitação da implementação atual (e pode mudar)

- **A intenção inimiga é invisível e sorteada na hora** (`turnos.agir_inimigo`): habilidade com 35% de chance (45% nos
  chefes), escolha ao acaso entre as que fazem sentido, alvo sorteado (`escolher_alvo_inimigo`: o provocador; o tanque
  da comitiva; um aliado ao acaso com 25% de chance, 15% nos chefes; senão você).
- **Só um golpe preparado existe** (`esmagar`), sempre igual (×2,2, uma vez de espera).
- **Interromper é binário:** atordoar desfaz o golpe inteiro, ou nada.
- **Chefes resistem por sorteio** (metade das vezes) ao atordoamento.
- **Talentos não mudam relações entre habilidades** (só `transforma` numa habilidade, um caso).
- **Não há moeda de combate além do recurso:** nada se acumula para gastar depois, fora as camadas de Queimadura.
- **O clima não é escolha de ninguém** (o jogador o vê, mas não o cria nem o consome).
- **Não há alvo em aliado** para as defesas do herói.
- **O ataque básico é igual em toda build** (o golpe da classe e a devolução de recurso).

### 2.5 Medidas

**O catálogo** (45 habilidades de classe e especialização):

| Estrutura | Quantas | Exemplos |
|---|---|---|
| Só dano | 7 | Golpe Pesado, Tiro Certeiro, Tiro Duplo, Lâmina Rúnica, Descarga, Julgamento, Rajada |
| Dano + estado com chance ou garantido | 15 | Investida, Lança de Gelo, Tiro Imobilizador, Bola de Fogo, Sede de Sangue, Flecha Sangrenta, Flecha Envenenada, Quebra-Guarda, Flecha Perfurante, Brasa, Chuva de Brasas, Nevasca, Golpe Sagrado, Drenar Vida, Fúria da Natureza |
| Sem dano (buff, marca, defesa, recurso, invocação) | 23 | Erguer Escudo, Passo Ágil, Barreira, Égide, Desaparecer, Mirar, Marcar Presa, Runa, Grito de Guerra, Proteger, Contragolpe, Prece, Meditar, Erguer Servo, Maldição... |

Dano por ponto de recurso (multiplicador × 100 / custo), onde a conta é direta: Tiro Certeiro 21, Tiro Duplo 18,
Golpe Pesado 17, Lança de Gelo 13, Flecha Sangrenta 12,5, Lâmina Rúnica 11,4, Bola de Fogo 10,7, Investida 10, Flecha
Perfurante 10, Descarga 9,2, Golpe Sagrado 8,7, Drenar Vida 8,6, Quebra-Guarda 7,9, Brasa 7,5, Tiro Imobilizador 6,7.

**As decisões escondidas no catálogo:**

| Decisão | Habilidades que a oferecem | Quando ela importa hoje |
|---|---|---|
| Bater forte num alvo | Golpe Pesado, Tiro Certeiro, Descarga, Lâmina Rúnica, Tiro Duplo, Rajada | Sempre (o padrão) |
| Bater em todos | Redemoinho, Chuva de Flechas, Nevasca, Chuva de Brasas, ultimates de área | 2+ inimigos |
| Tirar a vez de alguém (com chance) | Investida, Lança de Gelo, Tiro Imobilizador, Nevasca, Golpe no Joelho (Morel) | Só contra preparação |
| Fazer o alvo receber mais | Marcar Presa, Runa da Fragilidade (herói e Yara), Quebra-Guarda, Flecha Perfurante, Maldição | Lutas longas |
| Eu tomar menos | Erguer Escudo, Passo Ágil, Barreira, Égide, Desaparecer, Defender | Golpe preparado; vida baixa |
| Outro tomar no meu lugar | Proteger (herói e Morel), Erguer Servo, Ordem da Fera (urso) | Aliado ferido |
| Acumular e detonar | Brasa/Chuva → Combustão/Conflagração | O único ciclo de duas etapas |
| Dano ao longo do tempo | Sangramento, Veneno, Queimadura, Maldição | Lutas longas |
| Trocar vida por algo | Fúria Cega, Pacto de Sangue, Sede de Sangue | Berserker |
| Recurso | Meditar, Sifão, ataque básico | Mago, raramente |

**Os inimigos do Vale** (biomas planície, pântano, floresta e ruínas: 17 famílias):

| Habilidade inimiga | Famílias | Avisa antes? |
|---|---|---|
| Drenar, Veneno, Golpe Sujo, Mordida Sangrenta | 3 cada | Não |
| Golpe Esmagador (`esmagar`) | 3 (ent jovem, golem, mercenário) + as duas variantes da capela | **Sim** |
| Agarrar, Cura, Grito de Terror, Investida | 2 cada | Não |
| Teia, Roubo, Maldição, Bola de Fogo, Devorar, Esfera Sombria, Regenerar, Uivo, Grito de Guerra | 1 cada | Não |

**O alcance do capítulo:** o nível no fim do Vale é 3,9 a 4,3 nos percursos medidos depois da 1.64.0
([17](17-E9-VALIDACAO-DO-VALE.md), seção 15, a tabela do ritmo); um ponto de talento por nível, mais os de guardiões.
No nível 4 o herói tem uns 3 pontos, quase todos gastos na camada de nível 2 (só números).

### 2.6 O que muda a maneira de jogar e o que tende a ser redundante

**Muda a maneira de jogar:** Combustão e Conflagração (acender agora, detonar depois); interromper o Golpe Esmagador;
Prisão de Gelo × Lança de Gelo; Proteger; o limiar da Execução; o segundo disparo do Tiro Duplo; Rei dos Mortos,
Erguer Servo e Ordem da Fera (um corpo a mais com regras próprias); Defender.

**Tende a ser redundante:** as três "chances de tirar a vez"; os quatro "alvo recebe mais" (Marcar Presa com o mesmo
problema de pedágio que levou a Marca do Morel a ser recusada); as cinco defesas pessoais; Proteger e Runa repetidos na
comitiva e no herói; Mirar → Tiro Certeiro como rotina; os talentos de camada 1.

**Na luta real**, a sequência ideal de cada classe se repete (o robô do simulador joga assim e ganha 82% a 97% das
lutas comuns, [26](26-INTEGRACAO-DO-COMBATE.md)). Isso não prova o que uma pessoa faz; mostra que a regra simples
basta. **A causa não é só a falta de aviso dos inimigos** (a primeira versão deste estudo exagerou isso): é também a
falta de qualquer coisa que o herói construa ao longo da luta e possa gastar, converter ou arriscar.

---

## 3. Pesquisa: o que outros sistemas ensinam

Critério: referências escolhidas pelo mecanismo que sustenta a decisão. Fontes de desenvolvedor ou oficiais primeiro;
wikis de fãs quando a regra é observável no jogo, marcadas como tal. Não reproduzo números de balanceamento.

### 3.1 a 3.14: as referências da primeira rodada (mantidas)

**3.1 Slay the Spire (Mega Crit): a intenção.** Um ícone sobre cada inimigo mostra a próxima ação (ataque com dano,
defesa, buff, debuff), e ela é verdadeira. Cada turno vira uma pergunta concreta. O designer Anthony Giovannetti diz que
queriam inimigos que testassem estratégias de maneiras diferentes para nenhuma dominar
([Game Developer, 2020](https://www.gamedeveloper.com/disciplines/road-to-the-igf-mega-crit-games-i-slay-the-spire-i-);
palestra do GDC 2019 sobre métricas: [GDC Vault](https://www.gdcvault.com/browse/gdc-19/play/1025731)). Depende da mão
sorteada; nós temos kit fixo. Traz: a intenção.

**3.2 Into the Breach (Subset Games): ameaça anunciada e manipulável.** Todo ataque inimigo é anunciado com o alvo;
Justin Ma: queriam menos aleatoriedade, que cada morte parecesse culpa do jogador, e o jogo "começa a parecer um
quebra-cabeça" ([Game Developer, 23/02/2018](https://www.gamedeveloper.com/game-platforms/road-to-the-igf-subset-games-i-into-the-breach-i-)).
Depende do tabuleiro (empurrar). Traz: redirecionar o alvo, mudar o momento, reduzir a ameaça.

**3.3 Sea of Stars (Sabotage): travas.** O inimigo que prepara mostra um contador e travas por tipo de dano; cada trava
quebrada enfraquece, todas cancelam. Thierry Boulanger contou que acrescentaram a indicação de força porque era
frustrante ficar com uma trava sobrando
([God is a Geek, 2023](https://www.godisageek.com/2023/10/sea-of-stars-nearly-had-a-skate-park-style-boating-mini-game)).
Traz: interromper em graus, o tipo de dano com uma segunda função.

**3.4 Final Fantasy X (Square): a ordem visível e manipulável.** Haste, Slow e golpes de atraso mudam quando cada um
age (guias de fãs: [FFX-Info](https://grayfox96.github.io/FFX-Info/game-mechanics/ctb),
[jegged](https://jegged.com/Games/Final-Fantasy-X/Tips-and-Tricks/CTB-Window.html)). Atrasar repetidamente deixava
inimigos sem agir; a resposta foi chefes imunes. Traz: a lição do risco.

**3.5 Octopath Traveler (Square Enix): quebra e reserva.** Escudos que caem com fraquezas, o inimigo quebrado perde
uma ação e o escudo volta; o Boost guarda pontos para reforçar depois
([GamerGuides](https://www.gamerguides.com/octopath-traveler/guide/the-basics/game-mechanics/battle-system), terceiros).
Traz: controle que se reconstrói; guardar para depois.

**3.6 Wildfrost (Deadpan Games): contadores e congelar o relógio.** Cada unidade age quando o contador chega a zero; a
Neve para o contador ([Wildfrost Wiki](https://wildfrostwiki.com/Getting_Started), fãs). Traz: o contador na
preparação.

**3.7 Guild Wars (ArenaNet): barra de oito, uma elite.** No máximo 8 habilidades e uma elite, trocadas fora das áreas
de combate, de centenas ([Guild Wars Wiki, oficial](https://wiki.guildwars.com/wiki/Skill); o wiki hoje pede conta, a
regra foi conferida pelo índice). Interrupções só valem contra o que tem tempo de ativação
([Interrupt effect](https://wiki.guildwars.com/wiki/Interrupt_effect)). A comunidade convergia em poucas barras: muitas
habilidades não garantem muitas builds.

**3.8 Darkest Dungeon (Red Hook): quatro de sete, marcas e caminhos.** 7 habilidades por herói, 4 levadas
([wiki oficial](https://darkestdungeon.wiki.gg/wiki/Heroes_(Darkest_Dungeon))); a marca faz a maioria dos inimigos
preferir o marcado ([Mark](https://darkestdungeon.wiki.gg/wiki/Mark)); no II, caminhos com forças e fraquezas
([Red Hook, notícia oficial](https://store.epicgames.com/news/first-major-darkest-dungeon-ii-update-draws-from-original-beasties-and-more)).
Traz: quatro de sete; marca como isca; caminho com fraqueza.

**3.9 Path of Exile (Grinding Gear Games): suportes que mudam a entrega.** Gemas de suporte mudam o comportamento da
habilidade ligada (armadilha, mina, eco), cobram mais e têm incompatibilidades
([Support gem](https://www.poewiki.net/wiki/Support_gem), [Trap Support](https://www.poewiki.net/wiki/Trap_support),
fãs). Traz: mudar a entrega (agora, depois, em reação).

**3.10 Diablo IV (Blizzard): ramos por habilidade.** A revisão de abril de 2026 trocou "mais do mesmo" por ramos em que
"as melhorias que você escolhe mudam a maneira de jogar" ([Xbox Wire, 22/04/2026](https://news.xbox.com/en-us/2026/04/22/diablo-4-skill-tree-overhaul/)).
Traz: modificador que mora na habilidade.

**3.11 D&D 5e (Wizards of the Coast): concentração e preparar a ação.** Um efeito sustentado de cada vez, que o dano
pode quebrar; preparar uma ação com gatilho até a próxima vez; uma reação por rodada
([SRD 5.1, oficial](https://media.wizards.com/2016/downloads/DND/SRD-OGL_V5.1.pdf)).

**3.12 Legends of Runeterra (Riot): velocidade de resposta.** Feitiços que podem ou não ser respondidos
([suporte oficial](https://support-legendsofruneterra.riotgames.com/hc/articles/360036067293)). Traz: classificar o que
se responde.

**3.13 Shin Megami Tensei (Atlus): a economia de ações.** Acertar fraqueza dá meia ação; errar tira
([Megami Tensei Wiki](https://megatenwiki.com/wiki/Press_Turn_System), fãs). Traz: com cuidado, pagar ação com ação.

**3.14 Chained Echoes (Matthias Linda): um medidor de grupo.** A barra que precisa ficar na faixa certa; parte dos
jogadores acha que ela vira a escolha automática
([guia de terceiros](https://gameranx.com/features/id/429682/article/chained-echoes-how-to-lower-heat-overdrive-system-explained/)).
Traz: o alerta contra "manter no ponto ideal".

### 3.15 Slay the Spire, o Defect: uma moeda própria com espaços

- **Mecanismo:** o personagem "canaliza" orbes em espaços (3 no começo). Cada orbe tem um efeito passivo a cada turno e
  um efeito ao ser "evocado". Canalizar com os espaços cheios evoca automaticamente um dos antigos para abrir lugar
  ([Slay the Spire Wiki, Orb](https://slaythespire.wiki.gg/wiki/Orb), fãs). O Foco aumenta passivo e evocação de todos
  ([Focus](https://slaythespire.wiki.gg/wiki/Focus)).
- **Por que dá decisão:** o jogador escolhe que orbes manter (passivo) e quando trocá-los pelo efeito forte (evocar); o
  espaço cheio força a escolha. O passivo trabalha **mesmo contra inimigos que não fazem nada de especial**: o ritmo é
  do próprio personagem.
- **Habilidades e modificadores:** cartas produzem orbes, outras os evocam, outras aumentam espaços ou o Foco; um
  "talento" (Foco) afeta todas as fontes de uma vez.
- **Impede a solução universal:** espaços limitados; o Foco disputa lugar com dano direto; inimigos que punem o tempo.
- **Adaptação:** **runas em órbita** do Mago (seção 5.2): 3 espaços, passivo por vez, liberar a mais antiga. Não
  depende de mapa nem de intenção inimiga.

### 3.16 Slay the Spire, o Watcher: posturas com risco

- **Mecanismo:** posturas: na Ira, causa e recebe o dobro de dano; ao sair da Calma, ganha energia; a Divindade, mais
  difícil de alcançar, triplica o dano e acaba no começo do próximo turno
  ([Slay the Spire Wiki, Stance](https://slaythespire.wiki.gg/wiki/Stance), fãs).
- **Por que dá decisão:** entrar na Ira é um risco que depende de quanto o inimigo vai bater; sair é tão importante
  quanto entrar. A postura é um estado do personagem que muda o valor de todas as outras ações.
- **Adaptação:** **a Postura de Fúria** do Berserker (seção 5.3), com a intenção inimiga (quando existir) dizendo o
  preço da aposta, e com um jeito de sair que vale alguma coisa.

### 3.17 Darkest Dungeon II: fichas de combate com anulação

- **Mecanismo:** fichas sob a vida do personagem (Bloqueio, Esquiva, Força, Crítico, Vulnerável, Fraco...), cada uma
  consumida pelo próximo acontecimento que a usa, com teto por tipo (1, 2 ou 3). **Pares opostos se anulam** (Bloqueio
  × Vulnerável, Força × Fraco), e algumas habilidades **invertem** fichas (Força vira Fraco, Bloqueio vira Vulnerável)
  ([Darkest Dungeon Wiki, oficial, Tokens](https://darkestdungeon.wiki.gg/wiki/Tokens)).
- **Por que dá decisão:** as fichas são um vocabulário comum: muitas habilidades produzem, muitas consomem, e as
  anulações fazem dar Bloqueio a um aliado Vulnerável ser uma escolha (anula em vez de somar).
- **Adaptação:** **fichas** no nosso jogo (seção 5.1 e regras na seção 4): Guarda, Força, Exposto, com teto e anulação.
  É o "produto compartilhado" que permite combinações que ninguém desenhou como par.

### 3.18 Inscryption (Daniel Mullins): sacrifício como custo, morte como moeda

- **Mecanismo:** cartas que custam "sangue", pago sacrificando criaturas suas; "ossos", ganhos sempre que uma criatura
  sua morre (por sacrifício ou combate), pagam outras cartas (guias de terceiros:
  [Prima Games](https://primagames.com/gaming/inscryption-beginners-guide-card-upgrades-vendors/2)).
- **Por que dá decisão:** a criatura fraca vale pelo que ela paga; morrer deixa de ser só perda.
- **Adaptação:** **ossos** do Necromante (seção 5.2): toda morte na luta dá um osso; sacrificar o servo dá mais. O
  carniçal que devora corpos (já existe: `_devorar` consome `cb.mortos`) vira um rival natural dessa moeda.

### 3.19 Persona 5 (Atlus): passar a vez

- **Mecanismo:** quem ganha uma ação extra ao derrubar um inimigo pode **passá-la** a um aliado, com bônus; não se pode
  passar de novo a quem já recebeu na mesma rodada
  ([Megami Tensei Wiki, Baton Pass](https://megatenwiki.com/wiki/Baton_Pass); [Ludo Guide](https://www.ludo.guide/guide/persona-5-royal/battle-mechanics), fãs).
- **Lição:** passar uma ação é diferente de criar uma; o limite "não volta a quem já recebeu" corta as cadeias.
- **Adaptação:** **Revezamento** (seção 6): você abre mão da sua vez e um aliado age agora; a vez dele, mais tarde,
  continua sendo dele. Sem a ação extra de Persona.

### 3.20 Pathfinder 2e (Paizo): adiar a própria vez

- **Mecanismo:** no começo da sua vez, você pode sair da ordem e voltar depois da vez de outro; a sua posição muda
  para a nova, de vez ([regras básicas, Roll20](https://roll20.net/compendium/pf2/Rules:Basic%20Actions); a regra
  oficial está nos Archives of Nethys, que a pesquisa não conseguiu abrir).
- **Lição:** esperar por informação tem valor (ver o inimigo agir antes) e não cria ação.
- **Adaptação:** **Esperar** (seção 6): adiar a sua vez para depois de um combatente desta rodada, **só nesta rodada**
  (a ordem base não muda, ao contrário do Pathfinder).

### 3.21 Magic: The Gathering (Wizards of the Coast): laços e cadeias

- **Mecanismo:** um laço de ações obrigatórias que ninguém pode interromper empata a partida; laços com uma ação
  opcional exigem que o jogador declare quantas vezes repete (regras abrangentes; o número da regra mudou entre versões:
  [MTG Wiki, Loop](https://mtg.wiki/page/Loop), fãs, sobre as regras oficiais).
- **Lição:** o jogo de regras mais carregado de gatilhos **não proíbe cadeias**; proíbe o laço infinito e deixa a
  cadeia finita acontecer.
- **Adaptação:** a regra das cadeias da seção 8.

### 3.22 Slay the Spire: a combinação forte e finita

- **Mecanismo:** Corrupção (habilidades custam 0 e se esgotam) com Galho Morto (cada carta esgotada põe uma nova na
  mão) e Sem Dor (cada carta esgotada dá bloqueio) geram uma cadeia longa, mas que termina (o baralho, a mão e a sorte
  limitam). Jogadores a tratam como uma das melhores combinações do Ironclad
  ([discussões de jogadores, Steam](https://steamcommunity.com/app/646570/discussions/0/1778262124930086284); fonte
  fraca, uso só como relato de recepção).
- **Lição:** uma combinação poderosa e rara, montada ao longo da partida, é recompensa, não defeito, desde que acabe e
  que não seja a única maneira de vencer.

### 3.23 O que a pesquisa nova muda ou sustenta

| Descoberta | Efeito na recomendação |
|---|---|
| Moedas próprias com espaços e teto (3.15, 3.17, 3.18) | **Muda:** a profundidade não depende só do inimigo; builds que constroem viram um eixo (seção 5) |
| Posturas com risco (3.16) | **Muda:** "arriscar para antecipar" ganha um mecanismo que não é dano puro |
| Fichas com anulação e inversão (3.17) | **Muda:** sustenta um vocabulário compartilhado, base das combinações não desenhadas como par (seção 7.4) |
| Passar e adiar a vez (3.19, 3.20) | **Muda:** a ordem fixa pode ganhar intervenções que não geram ação (seção 6) |
| Laços × cadeias (3.21, 3.22) | **Muda:** a regra de profundidade 1 sai (seção 8) |
| Intenção, travas (3.1, 3.3) | **Sustenta**, como módulo, não como centro |
| Diablo IV, Path of Exile (3.9, 3.10) | **Sustenta** versões e entregas, agora dentro de uma árvore de regras |

---

## 4. Regras de referência dos exemplos

**Hipótese de trabalho, não regra aprovada.** A primeira versão tinha exemplos que contradiziam as próprias regras. Aqui
as regras vêm antes; todas as demonstrações deste documento obedecem a elas. Cada uma pode ser recusada sozinha.

| # | Regra | Resolve |
|---|---|---|
| R1 | **Vez e ação.** Cada combatente tem uma vez por rodada e, nela, uma ação principal. Fichas, estados e passivas não gastam ação. Reações (Tocaia, Revide) acontecem na vez de outro: no máximo uma por personagem por rodada | O Baluarte que fazia duas ações numa rodada |
| R2 | **Intenção (módulo opcional).** No fim da vez de cada inimigo (e no começo da luta), ele escolhe a próxima ação e o alvo; a carta mostra o tipo e o alvo. **A ação se mantém. O alvo só muda por três motivos:** (a) o alvo caiu ou ficou inválido; (b) um efeito redireciona explicitamente (provocar, chamariz, ilusão); (c) uma **reação declarada** do inimigo, escrita na ficha dele e marcada com um ícone na carta (ex.: "ferido abaixo da metade: mira quem o feriu por último"). Proteger e Juramento **não mudam a intenção**: agem na resolução, levando o golpe para o protetor. Se a ação ficar impossível (não há corpo para devorar), o inimigo faz o ataque comum no mesmo alvo | As mudanças de alvo dos exemplos antigos, sem motivo declarado |
| R3 | **Preparação.** "Sai em N": o golpe sai na N-ésima vez seguinte do inimigo; o número desce no começo de cada vez dele. Nas vezes intermediárias ele age normalmente (ataque ou habilidade), sem preparar outra. **Travas:** k tipos de dano. A força do golpe é a fração de travas que restam (3 travas, 2 quebradas: sai com 1/3). **Todas quebradas: o golpe é cancelado** e a vez dele se perde recompondo-se. Uma ação quebra uma trava, salvo o que a habilidade disser | O Quebrador cujo golpe "saía fraco" com todas as travas quebradas |
| R4 | **Atrasar.** Uma preparação aceita **no máximo 2 atrasos**, de qualquer fonte (inclusive o abalado de R5); depois fica **inadiável** (o contorno vermelho). Atrasar uma inadiável não faz nada (a carta fica apagada na escolha de alvo) | A Canção adiada para sempre no exemplo da Tocaia |
| R5 | **Perder a vez.** Inimigo comum: atordoado perde a próxima vez e a preparação em curso; depois fica Firme (como hoje). **Chefe: fica abalado**: se tem preparação adiável, ela atrasa 1 (conta no limite de R4); senão, se tem trava, perde uma; senão, a próxima ação dele sai com −25%. O chefe sempre age | Chefes travados ou imunes |
| R6 | **Fichas.** Guarda (o próximo golpe recebido −50%), Força (o próximo golpe causado +50%), Exposto (o próximo golpe recebido +50%). Teto de 2 por tipo. Guarda e Exposto se anulam (uma de cada some); Força e Enfraquecido se anulam | Vocabulário comum (seções 5 e 7) |
| R7 | **Cadeias.** Um efeito disparado por gatilho acontece **no máximo uma vez por cadeia para o mesmo alvo**; efeitos que dão recurso ou vez, **uma vez por rodada** por fonte. Uma reação não responde a outra reação ao mesmo golpe (a regra `respondido` de hoje) | A profundidade 1 da primeira versão (seção 8) |
| R8 | **Ambiente da luta.** Um ambiente de cada vez, criado por habilidade (névoa, óleo, água rasa...); o novo substitui o anterior; dura até ser substituído ou consumido. O clima continua valendo por baixo | Seção 5.2 |
| R9 | **Ordem.** Fixa, salvo o que a seção 6 testar. Os exemplos que usam Revezamento ou Esperar dizem isso | — |
| R10 | **Versões.** Uma habilidade leva uma versão de cada vez. Quem leva Estilhaço não tem a Lança de Gelo base (e não congela com ela) | O Pavio com Estilhaço tentando congelar |

---

## 5. Maneiras de jogar: responder, construir, arriscar, sustentar

Quatro estilos, **não categorias**. Uma build mistura dois ou três; uma classe pode ter os quatro. Servem para
conferir se o sistema oferece mais de um jeito de enfrentar a mesma luta.

| Estilo | O que o jogador faz | De onde vem a decisão | Funciona contra quem não prepara nada? |
|---|---|---|---|
| **Responder** | Lê a ameaça e escolhe a resposta | Do inimigo (intenção, preparação, apoio) | Pouco: precisa de ameaças distintas |
| **Construir** | Junta algo ao longo da luta e escolhe quando gastar | Da própria moeda (camadas, runas, ossos, fichas, ambiente) | **Sim:** o ritmo é do personagem |
| **Arriscar** | Paga agora (vida, vez, defesa) para antecipar um resultado | Do preço da aposta e da pressa | Sim: o risco vem do dano que entra |
| **Sustentar ou transformar a comitiva** | Muda o que os aliados podem fazer ou o que lhes acontece | Das relações entre os três | Sim: depende de quem está em perigo |

### 5.1 Construir: moedas próprias

**Camadas no inimigo** (existe: Queimadura). O fogo acumula no alvo e alguém detona. Versões: detonar adiado, passar
camadas a outro, converter em barreira (seção 7).

**Fichas** (R6). Produtores e consumidores em várias classes:

| Produz | Consome ou converte |
|---|---|
| Guarda: Erguer Escudo dá Guarda a você ou a um aliado; Formação (Guerreiro) dá Guarda a quem está ao lado na ordem | Escudo Alto: consome todas as suas Guardas e causa dano por Guarda gasta (Defesa × 50% cada) |
| Força: Grito de Guerra dá Força a todos os aliados; o Peso do Golpe (talento) dá Força ao próximo aliado | Golpe Acumulado: consome as Forças do grupo inteiro num golpe só |
| Exposto: Quebra-Guarda, Engodo, Elo Rompido | Execução (Sombra): conta Exposto como "abaixo de 35%"; Golpe Oportuno de Morel |

Por que dá decisão: o teto (2) força o gasto; a anulação faz a mesma ficha valer coisas diferentes (dar Guarda a quem
está Exposto apaga o Exposto em vez de proteger mais).

### 5.2 Construir: três motores que não dependem do inimigo

**Runas em órbita (Mago).** Três espaços ao redor do mago, visíveis na carta dele.
- *Gravar* uma runa é a ação; cada runa tem um passivo **no fim de cada vez sua**: a de gelo dá 1 Guarda a quem
  você escolheu ao gravar; a de fogo põe 1 camada de Queimadura no alvo do seu último golpe; a de arcano devolve 4 de
  Mana.
- *Liberar* (outra ação) consome a runa mais antiga com o efeito forte: gelo, Guarda 2 em todos os aliados; fogo,
  140% do Poder no alvo e 2 camadas; arcano, a próxima habilidade custa 0.
- Gravar com os três espaços cheios libera a mais antiga sozinho (o Defect).
- **Decisões:** que runa manter girando, quando abrir mão do passivo pelo efeito forte, e evitar a liberação
  automática na hora errada.
- **Contra inimigos que não preparam:** a pressão é o dano que entra; as runas de gelo seguram o grupo enquanto as de
  fogo acendem. Contra uma luta muito curta, as runas não se pagam: é a fraqueza.

**Ossos como moeda (Necromante).** Toda morte na luta, de qualquer lado, dá 1 Osso (teto 5). **Pagar com Ossos**
(ação): desfaz um servo seu, que absorve o próximo golpe dirigido a um aliado escolhido, e dá 2 Ossos. Habilidades
que custam Ossos em vez de Mana: Lança de Osso (1: 150% do Poder num alvo), Erguer Servo de Ossos (2), Muralha de
Ossos (3: uma Guarda em cada aliado). A versão Servo Escudo do Erguer Servo não provoca: fica para ser gasto.
- **Decisões:** quando sacrificar o servo (ele protege; gasto, vira moeda e uma Guarda); o que comprar com os ossos.
- **Contra quem não prepara:** enxames alimentam a moeda; **um chefe sozinho a deixa passar fome** (só mortes de
  invocados e dos seus servos).
- **Rival natural:** o carniçal devora corpos (`_devorar`): cada corpo que ele come é um osso a menos, e a intenção
  dele ("devorar") avisa.

**O ambiente da luta (qualquer classe; R8).** Um ambiente de cada vez:
- *Névoa:* +15% de esquiva para todos (os dois lados).
- *Óleo:* o fogo acende 1 camada a mais; um golpe de fogo consome o óleo e causa dano em todos.
- *Água rasa:* gelo congela com mais chance; fogo perde força; raios (se existirem) atingem todos.
- *Cinzas:* sangramentos e venenos fecham mais devagar (duram 1 a mais).

Quem cria: Patrulheiro (Névoa da Mata), Piromante (Derramar Óleo), Mago de gelo (Charco Gelado), inimigos (a Bruxa
do Brejo cria Água rasa, e isso muda o valor do seu fogo). **Decisão:** substituir um ambiente que ajuda o inimigo, ou
explorá-lo. **Por que é novo:** é a superfície dos jogos com mapa, sem posição; e o clima já é a mesma coisa sem dono.

### 5.3 Arriscar: pagar agora para antecipar

**Postura de Fúria (Berserker).** Entrar é parte de uma habilidade (Rugido: 80% num alvo e entra em Fúria). Na
Fúria, você causa e recebe +50%. Sair acontece no fim de qualquer vez sua, por escolha, sem gastar ação, e dá +12 de
Vigor e 1 Guarda.
- **Decisão:** ficar na Fúria quando o dano que vai entrar é pequeno ou espalhado; sair antes do golpe forte ou quando
  a comitiva precisa de você inteiro.
- **Contra quem não prepara:** os lobos mordem muito e pouco: na Fúria, cada mordida dói mais, e a conta muda a cada
  uivo.

**Ímpeto Temerário.** Agir de novo agora e perder a sua próxima vez (seção 6: é transferir uma ação no tempo, não
gerar).

**Pagar com vida.** Habilidades que, sem recurso, podem ser pagas com vida (o talento Queimar a Si Mesmo do Piromante,
seção 7.2). A decisão é quanto da vida é sobra.

**Promessa (Paladino).** Uma promessa para a próxima rodada: "ninguém do grupo cai até o fim da próxima rodada".
Cumprida, cura o grupo e dá Força a todos; quebrada, você fica Enfraquecido por duas vezes suas. Constrói e arrisca ao
mesmo tempo; o inimigo não precisa preparar nada para ela ter tensão.

### 5.4 Sustentar ou transformar a comitiva

- **Elo de Vida (Paladino):** dois combatentes do seu lado dividem o dano que recebem (metade cada) por 3 rodadas.
  Decisão: com quem ligar o frágil. O Elo muda o valor das outras proteções (a seção 11 mostra o Proteger perdendo a
  vez para outra ação porque o Elo já repartia o golpe).
- **Revezamento (qualquer classe, se a decisão 3 abrir):** você abre mão da sua vez e um aliado age agora; a vez dele
  continua no lugar dela.
- **Ordem da Fera e servos com versões:** o animal ou o servo como uma peça que a build molda (o urso que protege, o
  servo que paga).
- **Transmutar (Mago arcano):** o próximo golpe de um aliado sai com o tipo de dano que você escolher (Morel batendo
  com gelo num alvo que resiste ao físico; Odette com fogo num alvo em Óleo).
- **Inverter (Arcano ou Sombra):** troca uma ficha ou estado pelo oposto: o Fortalecido do bando vira Enfraquecido, a
  Guarda do inimigo vira Exposto (as inversões de Darkest Dungeon II).
- **Repartir a cura (Odette, versão):** a Prece cura o alvo e põe 1 Guarda em quem está ligado a ele.

### 5.5 Responder (o que ficou da primeira versão)

Continuam como possibilidades, agora sob as regras da seção 4: interromper em graus (travas), atrasar (com o limite
de R4), precipitar o golpe preparado contra a defesa pronta, a Tocaia (reação armada), o Duplo e o Engodo (o primeiro
golpe dirigido ao original vai na ilusão; área desfaz sem efeito; quem "percebe" ignora), a Âncora (devolver vida e
estados de um combatente ao momento marcado, uma por luta; o sorteio nunca volta), o Juramento (o golpe dirigido ao
aliado vai em você, e você revida). Os detalhes de cada uma (o que se vê, o que se sacrifica, interface, motor e
abuso) estão na primeira versão (apêndice A) e continuam válidos onde não contradizem a seção 4.

### 5.6 Por que continuam interessantes contra inimigos que não preparam nada

A primeira versão deixava a impressão de que, sem preparações inimigas, nada sobrava. Contra três lobos, que só mordem
e uivam:

- **Construir** decide quando gastar: o Pavio acende todos e escolhe quem detonar antes de o uivo terminar; o Ossário
  ganha um osso a cada lobo morto e decide entre a Lança de Osso e a Muralha.
- **Arriscar** decide quanto pagar: a Fúria vale enquanto as mordidas são pequenas; o uivo muda a conta.
- **Sustentar** decide quem segura: o Elo divide as mordidas entre o herói e Odette; a Promessa aposta em ninguém cair.
- **Responder** perde força. É legítimo: a build que responde escolhe outro kit antes dessa luta, ou sofre nela.

O que torna a adaptação legítima (e não uma "falha" por usar mal a habilidade):

| Tipo | Exemplo | Conta como adaptação? |
|---|---|---|
| **Mudança provocada pelo combate** | O lobo morreu antes da detonação; a Bruxa curou o alvo aceso; o mercenário ferido mudou de alvo pela reação declarada | Sim, a principal |
| **Risco assumido** | Ficar na Fúria apostando que o sapo não ia agarrar; tentar o congelamento de 35% | Sim |
| **Informação incompleta** | Sem intenção visível, não saber se a Bruxa vai curar ou amaldiçoar; o próximo invocado | Sim |
| **Erro de leitura** | Usar o Duplo contra um golpe em área que a ficha diz ser em área | Existe, mas não demonstra profundidade |

---

## 6. A ordem dos turnos, reaberta

O pedido do Jean trouxe a alteração temporária da ordem; a decisão 25, 3.5 fica **reaberta para análise**. Nada muda no
jogo.

### 6.1 Três coisas diferentes

| Conceito | O que muda | Ações de cada lado na rodada | Exemplo |
|---|---|---|---|
| **Alterar a ordem** | Quem vem antes de quem | Iguais | Trocar duas posições |
| **Transferir uma ação** | Quem usa uma ação, ou quando | Iguais (alguém abre mão) | Revezamento; Esperar; Ímpeto Temerário |
| **Gerar uma ação** | Quantas ações um lado tem | Mais | "Agir de novo", a ação extra de Persona ou Megami Tensei |

### 6.2 As intervenções comparadas

| Intervenção | Benefício tático | Clareza | Custo de implementação | Risco de abuso |
|---|---|---|---|---|
| **Ordem fixa (hoje)** | Planejamento estável; tudo se refere a ela | Máxima | Nenhum | Nenhum |
| **Esperar:** adiar a sua vez para depois de um combatente, só nesta rodada | Ver o inimigo agir antes de decidir (útil sem intenção visível); curar depois do golpe, não antes | Boa, se a placa mostrar o lugar novo | Baixo (reordenar a rodada corrente) | Baixo: perde a vez se a rodada acabar |
| **Revezamento:** abrir mão da sua vez para um aliado agir agora | Pôr Odette antes do golpe; Morel atordoar antes de o inimigo agir | Boa | Baixo | Médio: com um aliado que age duas vezes (agora e na vez dele) seria geração de ação; **regras: só recebe quem ainda não agiu nesta rodada, e quem recebe perde a vez dele nesta rodada** (por isso é transferência); quem recebeu não repassa |
| **Trocar duas posições aliadas, nesta rodada** | Parecido com o Revezamento, menos flexível | Média (duas cartas trocam) | Baixo | Baixo |
| **Ímpeto Temerário:** agir agora de novo e perder a próxima vez | Fechar a luta ou matar antes de algo acontecer | Boa (a próxima posição riscada) | Baixo | Médio: pagar com uma vez que você perderia de qualquer jeito (atordoado). **Regra: a dívida é paga com a próxima vez que você de fato teria** |
| **Acelerar uma preparação aliada** (relógio do aliado −1) | Morel ou um golpe carregado do herói saem antes | Boa | Médio (preparações aliadas não existem hoje) | Baixo |
| **Atrasar a vez de um inimigo** na rodada (empurrar para o fim) | Muito forte: o golpe dele cai depois das suas defesas | Média | Baixo | **Alto:** combinado, deixa inimigos agindo depois de tudo, sempre; precisa de limite e de exceção para chefes |
| **Gerar ação** (agir de novo sem pagar) | O maior | Boa | Baixo | **Muito alto:** sequências que se repetem, laços com gatilhos |

### 6.3 O que ganhamos e perdemos

**Mantendo a ordem fixa sem exceções:** ganhamos clareza total, a placa como referência única, nenhum risco de laço de
vezes e combinações de tempo legíveis. Perdemos a fantasia temporal sobre as vezes (fica só o relógio das preparações),
a escolha de ordem dentro do grupo e uma ferramenta contra a informação incompleta (esperar para ver).

**Abrindo Esperar e Revezamento (transferências):** ganhamos uma decisão nova em toda luta, sem depender do inimigo
preparar algo; a comitiva passa a coordenar quem vai antes; o cronômante ganha a sua fantasia mais clara ("quem age
agora"). Perdemos parte da previsibilidade (a placa muda durante a rodada), e o motor precisa de uma ordem da rodada
separada da ordem base. Não perdemos o controle das ações: cada lado continua com o mesmo número delas.

**Abrindo intervenções sobre inimigos (atrasar a vez deles):** ganhamos muito poder tático e perdemos a garantia de que
o inimigo age quando a placa diz; é o caminho do Final Fantasy X, que acabou em chefes imunes. Não recomendo.

**Gerar ações:** não recomendo fora de uma ultimate (uma vez por luta), e mesmo ali só com a R7.

### 6.4 Recomendação (pendente)

Testar **Esperar** e **Revezamento** como experimento separado do protótipo (seção 14, X4), com a regra de que quem
recebe o Revezamento perde a vez dele na rodada. Manter a posição dos inimigos intocável, salvo pelo relógio das
preparações (R3, R4) e pelo abalado (R5). **O motivo não é preferir a estrutura atual:** essas duas são as únicas que
dão uma decisão nova em toda luta sem aumentar o número de ações.

---

## 7. A construção das builds e o papel dos talentos

### 7.1 Os tipos de nó que uma árvore pode ter

A primeira versão assumiu que árvore implica bônus numérico. Não implica. Uma árvore pode ter quatro tipos de nó:

| Tipo | O que faz | Exemplo | Quando sustenta escolhas | Quando é compra obrigatória |
|---|---|---|---|---|
| **[N] Número** | Soma a um atributo ou a uma família | +10 de Mana; queimaduras +20% | Quando disputa pontos com regras e define um eixo (crítico, reserva) | Quando melhora tudo o que você faria de qualquer jeito e nada compete com ele |
| **[R] Regra por etiqueta** | Muda o que **todas** as habilidades de uma etiqueta fazem (fogo, golpe, proteção, servo, runa, ficha, reação) | "Queimaduras com 3 camadas não expiram" | Quase sempre: cria relações entre habilidades | Raramente; vira obrigatória se a etiqueta for a única da especialização |
| **[V] Versão** | Troca o que uma habilidade faz | Combustão → Pavio Curto | Quando a base continua boa em outra luta | Quando a versão é estritamente melhor |
| **[P] Princípio** | Regra forte, exclusiva, uma por build | "Atrasar quebra uma trava" | Quando define um estilo e exclui outro | Quando a especialização só tem um |

**Teste de obrigatoriedade** para qualquer nó: existe uma build plausível, da mesma especialização, que não o
compraria? Se não existe, o nó é um imposto e deve virar parte da base.

**Uma melhoria não precisa perder algo** se disputa um orçamento real (pontos, espaços) com alternativas relevantes.
A perda só é necessária nas versões, porque elas não competem por pontos com outra coisa.

### 7.2 Exemplo completo: o Piromante, três builds da mesma especialização

**Hipótese de árvore** (números inventados; 7 pontos disponíveis no meio da campanha, 10 nós):

| Nó | Tipo | Efeito | Afeta |
|---|---|---|---|
| Fogo Paciente | R | Queimaduras com 3 camadas não expiram enquanto o alvo vive | Brasa, Chuva, Bola de Fogo, runa de fogo, Óleo |
| Pavio Curto | V (Combustão) | Detona no começo da próxima vez do alvo, com +50% | Combustão |
| Contágio | V (Combustão) | Detona e passa metade das camadas ao inimigo mais aceso depois dele | Combustão |
| Calor Partilhado | R | Golpe físico de aliado em alvo em chamas acende +1 camada | Morel, Odette, a fera |
| Fornalha Interior | R | Cada detonação dá 1 Calor (teto 3); com 3, a próxima habilidade de fogo custa 0 | Combustão, Conflagração, Óleo |
| Queimar a Si Mesmo | R | Sem Mana, habilidades de fogo podem ser pagas com vida (1 de vida por 1 de Mana); abaixo de 50% da vida, cada fonte de fogo acende +1 camada | Todas as de fogo |
| Cinza Fria | R (híbrido) | Congelar um alvo em chamas consome as camadas e causa o dano delas como gelo | Lança de Gelo, Prisão, Nevasca, runa de gelo |
| Derramar Óleo | V (Chuva de Brasas) | A Chuva cria o ambiente Óleo e não acende ninguém | Chuva de Brasas |
| Chama Viva+ | N | Queimaduras +20% | Todas |
| Reserva Ardente | N | +12 de Mana máxima | — |

**Build A — Pavio** (construir e esperar): Fogo Paciente, Pavio Curto, Calor Partilhado, Chama Viva+ e 2 pontos em
Reserva. Kit: Brasa, Chuva de Brasas, Combustão (Pavio Curto), Bola de Fogo, Lança de Gelo (base), ultimate
Conflagração. Joga devagar, com a comitiva acendendo junto.

**Build B — Fornalha** (construir e arriscar): Fornalha Interior, Queimar a Si Mesmo, Contágio, Derramar Óleo. Kit:
Brasa, Combustão (Contágio), Chuva (Derramar Óleo), Barreira, Meditar, ultimate Conflagração. Detona cedo e muitas
vezes, paga com vida quando falta Mana, e usa o Óleo para transformar uma detonação em área.

**Build C — Choque Térmico** (híbrida fogo e gelo): Cinza Fria, Fogo Paciente, Calor Partilhado. Kit: Brasa, Bola de
Fogo, Lança de Gelo (base), Nevasca, Barreira, ultimate Conflagração. Acende e congela; não leva a Combustão.

| Pergunta | Resposta no Piromante |
|---|---|
| **O que disputa os mesmos pontos** | Fogo Paciente × Fornalha Interior (ritmo lento × rápido); Pavio Curto × Contágio (exclusivas); Queimar a Si Mesmo × Reserva Ardente (duas respostas à falta de Mana) |
| **O que disputa os mesmos espaços** | Combustão × Nevasca (C não leva a Combustão); Barreira × Lança de Gelo; Meditar × Bola de Fogo |
| **Talentos que afetam várias habilidades** | Fogo Paciente, Calor Partilhado, Fornalha Interior, Queimar a Si Mesmo, Cinza Fria |
| **O que especializa** | Pavio Curto, Contágio, Fornalha Interior |
| **O que permite híbrido** | Cinza Fria (gelo vira detonação); Calor Partilhado (a comitiva vira fonte) |
| **Ferramentas úteis que ficam de fora** | A tem pouca defesa (sem Barreira); B fica sem Lança de Gelo (sem resposta a golpe preparado); C fica sem a detonação forte num alvo |
| **Como evolui** | Início (Mago 1–3): Bola de Fogo, Lança, Meditar, a primeira regra (Chama Viva+ ou Reserva). Especialização: Brasa e Combustão; a primeira escolha entre Fogo Paciente e Fornalha. Meio: a versão da Combustão, o Óleo, a ultimate. Fim: Cinza Fria ou Queimar a Si Mesmo, quando o catálogo de gelo do Mago já está no kit |

### 7.3 Outros exemplos, mais curtos

**O Necromante: Ossário × Pestilento.**

| | Ossário (construir e sacrificar) | Pestilento (transformar estados) |
|---|---|---|
| Nós-chave | [R] Colheita de Ossos; [V] Servo Escudo; [R] Pacto de Medula (sacrificar cura o necromante); [N] servos +vida | [R] Pestilência (os males do alvo que morre passam ao inimigo mais ferido); [R] Sangue Ruim (Drenar Vida num alvo envenenado converte o veneno em vida para você); [V] Maldição que se espalha |
| Kit | Erguer Servo (Escudo), Lança de Osso, Muralha de Ossos, Pagar com Ossos, Drenar Vida | Bola de Fogo, Runa da Fragilidade, Erguer Servo (Pira), Drenar Vida; ult. Maldição |
| Disputa | Os ossos entre Lança, Muralha e servo novo | Os males próprios × os de Yara (a Pestilência espalha qualquer mal, inclusive a maldição dela) |
| Fica de fora | Os males (pouco dano ao longo do tempo) | A moeda de ossos; a proteção do servo |
| Melhor contra | Enxames | Grupos médios com lutas longas |
| Pior contra | Chefe sozinho | Construtos e mortos-vivos (imunes a veneno) |


**O Berserker: Quebrador × Fúria.** O Quebrador responde (Golpe que Racha, Contratempo, [P] o Peso do Golpe: quebrar
uma trava dá Força ao próximo aliado da ordem). A Fúria arrisca (Rugido, [R] Sangue Quente: na Fúria, 15% de roubo de
vida em todo dano; [R] Sangue Frio: sair da Fúria dá a Guarda a um aliado em vez de a você; Redemoinho). Os dois
disputam o mesmo nó de 3 pontos ([P] Peso do Golpe × [R] Sangue Quente). O Quebrador perde contra enxames; a Fúria,
contra o sapo que agarra (preso na Fúria, você apanha +50% sem agir).

**O Patrulheiro: Tocaia × Matilha.** A Tocaia responde (reações armadas, [R] "quando a Tocaia dispara, a fera ataca o
mesmo alvo"). A Matilha sustenta (versões da Ordem da Fera: o urso protege um aliado escolhido, o lobo marca o alvo
como Exposto, o falcão tira uma ficha do inimigo; [R] Laço: o animal recebe as suas fichas de Força quando você não as
usa).

### 7.4 Produzir, consumir, converter, preservar, modificar: combinações sem par desenhado

O vocabulário comum (camadas, fichas, corpos e ossos, runas, ambiente, estados) permite combinações que nenhum dos dois
lados foi feito para fazer junto:

| Produz | Faz com o produto | Quem são (de fontes diferentes) |
|---|---|---|
| Exposto (Quebra-Guarda do Guerreiro) | Consome | Golpe Oportuno de Morel; Execução da Sombra |
| Guarda (runa de gelo do Mago) | Consome | Escudo Alto do Guerreiro (dano por Guarda gasta) |
| Água rasa (a Bruxa do Brejo, inimiga) | Explora | Lança de Gelo (congela com mais chance); prejudica o Pavio |
| Corpos (qualquer morte) | Converte | Ossos do Necromante; Devorar do carniçal (inimigo) |
| Queimadura (Calor Partilhado: Morel acende) | Converte | Cinza Fria (gelo detona o fogo) |
| Maldição (Yara) | Preserva e espalha | Pestilência do Necromante |
| Fortalecido (uivo dos lobos) | Inverte | Inverter (Arcano): vira Enfraquecido |
| Força (Grito de Guerra) | Modifica | Laço do Patrulheiro (passa à fera) |

Para isso funcionar, **as habilidades precisam declarar etiquetas** (`familia` e `tipo` já existem; faltariam
"produz", "consome", "ficha", "ambiente") e as regras de talento perguntam pela etiqueta, não pelo nome da habilidade.

### 7.5 Estruturas comparadas, sem presumir que árvore é número

| Estrutura | Liberdade | Identidade da classe | Relações entre habilidades | Custo de conteúdo | Leitura |
|---|---|---|---|---|---|
| **T1. Versões + 1 ou 2 princípios** (a primeira recomendação) | Baixa a média: cada versão é local | Alta | Fracas (só o princípio relaciona) | Alto (cada versão é uma ficha) | Boa (compara-se duas fichas) |
| **T2. Árvore de regras por etiqueta** | Alta | Alta, se as etiquetas forem da classe | **Fortes** | Médio (uma regra vale para várias habilidades) | Média: o nó precisa dizer quais habilidades afeta |
| **T3. Selos encaixáveis por habilidade** (Path of Exile) | Muito alta | Média: preservada se o conjunto de selos for da classe e as etiquetas limitarem onde cada selo cabe | Médias | Baixo | Difícil (duas camadas: habilidade e selo) |
| **T4. Híbrida: T2 com versões em poucas habilidades e números que disputam** | **Alta** | Alta | Fortes | Médio | Média, com a tela certa |
| **T5. Escolas abertas entre classes** | Máxima | Baixa | Fortes | Muito alto | Difícil |

**"Uma versão por habilidade e um ou dois princípios" basta?** O exemplo do Piromante mostra que não. Com só versões, A,
B e C seriam quase o mesmo kit com Combustões diferentes: Fogo Paciente, Calor Partilhado, Fornalha Interior, Queimar
a Si Mesmo e Cinza Fria são regras que atravessam habilidades, e são elas que separam as três builds. Versões continuam
úteis onde uma habilidade central muda de papel (a Combustão), mas não carregam a build sozinhas.

**Selos apagam a identidade?** Não necessariamente: um conjunto de selos por classe, que só cabem em habilidades com a
etiqueta certa (o "em reação" só em golpes do Arqueiro), preserva a identidade. O problema real dos selos no nosso jogo
é a leitura (o jogador consulta duas fichas para entender uma habilidade) e o kit pequeno (5 espaços: pouco onde
encaixar). Por isso ficam como forma de os **itens** mudarem habilidades, não como a estrutura principal.

### 7.6 As tensões, revistas

- **Interessantes × obrigatórios:** o teste da 7.1; números ficam quando disputam pontos com regras.
- **Liberdade × identidade:** etiquetas da classe; regras híbridas pontuais (Cinza Fria) que abrem a porta para a
  outra metade da classe, não para outra classe.
- **Sinergia × dependência da comitiva:** relações por produto (Exposto, Queimadura, Guarda), nunca pelo nome do
  companheiro. Calor Partilhado funciona com Morel, com Odette e com a fera.
- **Especialização × adaptação:** kit e versões grátis em lugar seguro; a árvore redistribuída num lugar com custo
  pequeno (seção 9.3).
- **Acessíveis × avançadas:** a base de cada habilidade é boa sozinha; as regras chegam uma por nível; os princípios
  com a especialização; as híbridas no fim.

---

## 8. Cadeias, abusos e o que conta como profundidade

### 8.1 Exemplos antes da regra

**Uma cadeia interessante que deve funcionar.** Piromante com Coração Ardente (inimigo morto por fogo explode e fere os
outros), três inimigos em chamas, dois quase mortos. A Combustão mata o primeiro; ele explode; a explosão (fogo) mata o
segundo; o segundo explode; o terceiro, ferido, sobrevive. **Hoje isso não acontece:** o código impede a segunda
explosão (`cb.memoria["explodindo"]` em `talentos._coracao_ardente`), que é a profundidade 1 na prática. A cadeia é
finita (cada inimigo só morre uma vez) e é exatamente a fantasia da build.

**Um ciclo infinito que precisa ser impedido.** Herói com Contra-ataque e um inimigo com espinhos que revidam: o golpe
do herói fere o inimigo, o espinho fere o herói, o Contra-ataque responde ao espinho, o espinho responde ao
Contra-ataque... Outro: "ao ganhar recurso, cure 5" e "ao ser curado, ganhe 3 de recurso". Os dois são laços que se
alimentam sem nada ser consumido.

**Uma combinação poderosa e finita, aceitável.** O Ossário com 5 ossos e dois servos, contra um enxame de ratos: dois
sacrifícios (4 ossos, duas Guardas), uma Muralha (3 ossos) e três Lanças de Osso em três vezes; cada rato morto devolve
um osso. A sequência é forte e longa, mas acaba (os ratos e os servos acabam) e foi construída ao longo da luta, com
riscos (os servos podiam cair antes, sem render).

### 8.2 As alternativas para controlar

| Alternativa | Deixa a cadeia do Coração Ardente? | Impede o laço dos espinhos? | Impede o laço cura–recurso? | Custo de entender |
|---|---|---|---|---|
| **Profundidade 1** (a primeira versão) | Não | Sim | Sim | Baixo, mas proíbe o que é bom |
| **Não recorrência: um efeito, uma vez por cadeia, por alvo** | **Sim** (cada inimigo explode uma vez) | Sim (o Contra-ataque não responde de novo ao mesmo par na mesma cadeia) | Sim: na segunda volta, os dois efeitos já aconteceram para o mesmo alvo (você) nesta cadeia | Médio |
| **Limite de ativações por rodada** (efeito X no máximo N vezes) | Sim, se N ≥ inimigos | Sim | Sim | Médio; números diferentes por efeito confundem |
| **Custo por ativação** | Sim | Só se o custo esgotar | Só se o custo esgotar | Alto (fica difícil prever) |
| **Incompatibilidades pontuais** | Sim | Só nos pares listados | Só nos pares listados | Alto (decorar exceções) |

### 8.3 Recomendação (pendente)

**R7: um efeito disparado acontece no máximo uma vez por cadeia para o mesmo alvo; efeitos que dão recurso ou vez,
uma vez por rodada por fonte.** A primeira parte segura laços sem matar cadeias; a segunda segura as economias, que são
onde os laços mais aparecem (recurso, vez). Incompatibilidade pontual só se as duas falharem num caso medido.

### 8.4 Como o jogador entende os limites sem decorar exceções

- **Duas frases, ensinadas uma vez** (na Ajuda e no primeiro gatilho que encadeia): "Cada efeito acontece uma vez por
  alvo em cada cadeia." "Efeitos que dão recurso ou vez: uma vez por rodada."
- **Um ícone padrão** nas fichas dos talentos que geram recurso ou vez (o relógio pequeno "1× por rodada").
- **A cadeia à vista:** cada elo aparece em sequência na tela, com um número pequeno ("cadeia 2", "cadeia 3"); quando
  um efeito para pela regra, a faixa diz "já aconteceu nesta cadeia" uma vez, em vez de silenciar.

### 8.5 Frequência de uso não é falta de profundidade

Uma habilidade central usada em 60% das ações pode conter muitas decisões: o alvo (qual lobo), o momento (antes ou
depois do uivo), o preparo (com Força ou sem), a consequência (matar ou deixar vivo para o servo). A Combustão do Pavio
é central e cheia de decisão. **O problema é a escolha não depender do estado da luta.**

Medidas melhores para o protótipo:
- **A escolha depende do estado?** Para a mesma build, comparar situações diferentes (vida, inimigos, produtos à mão) e
  ver se a ação, o alvo ou o momento mudam.
- **Alternativas próximas:** quantas vezes havia duas ou mais ações razoáveis (pela pergunta "o que mais você
  consideraria?", ou pelo valor estimado de cada uma).
- **O relato do Jean:** quantas vezes ele parou para pensar.

A frequência alta continua sendo um sinal a investigar, não uma reprovação.

---

## 9. A progressão, separada do capítulo atual

O capítulo atual termina perto do nível 4, mas a campanha vai crescer: não se fixa nada aqui pela altura do Vale.

### 9.1 O que deve acontecer cedo, e o que deve esperar

| Fase | O jogador já tem | Escolhas de build relevantes | Evitar |
|---|---|---|---|
| **Começo** (primeiras lutas, níveis 1–3) | 2 a 4 habilidades da classe, o kit montado | **A primeira regra de talento** (uma entre duas ou três que mudam o estilo: para o Mago, Runas ou Chama Viva+; para o Guerreiro, Formação ou Fúria contida); o primeiro produto da classe (fichas, camadas, runas) | Esconder a identidade até a especialização; dar todos os sistemas de uma vez |
| **Encruzilhada** (especialização, num marco da história) | Repertório da classe quase inteiro | A especialização; o primeiro princípio; uma ultimate | Especialização como só "mais números" |
| **Meio** | Especialização e alguns achados | Versões das habilidades centrais; regras que atravessam a especialização e a classe | Árvore que só soma |
| **Fim** | Quase tudo | Híbridos (Cinza Fria), segunda ultimate por achado, combinações raras | Obrigar a recomeçar para experimentar |

### 9.2 Momentos de acesso comparados

| Momento | A favor | Contra | Depende da etapa 9? |
|---|---|---|---|
| Especialização no nível 4 (hoje) | Simples; o capítulo atual a mostra | Preso a uma curva de nível que vai mudar | Sim |
| Especialização num **marco da história** (uma cena, um mestre) | Liga a build à narrativa; independe da curva | Exige o marco escrito | **Sim** |
| Ultimate com a especialização | O jogador usa a ultimate cedo | Ultimate perde peso se vier "de brinde" | Parcialmente |
| Ultimate por **achado** (missão, chefe, mestre) | Recompensa de campanha; várias ultimates possíveis | Quem não acha fica sem | Sim |
| Primeira regra de talento no nível 2 | Estilo desde o começo | Pouco repertório para a regra agir | Não |

**Proposta:** a primeira regra no nível 2 (independe da 9); a especialização num marco da história que a 9 define, com
a ultimate da especialização junto; ultimates e versões extras por achado. **O que a etapa 9 decide:** a curva de nível,
o marco da especialização, onde ficam os mestres e os livros, e quantas lutas existem entre um marco e outro.

### 9.3 Experimentar, redistribuir, descobrir

- **Kit e versões:** grátis em lugar seguro (como hoje).
- **Pontos de talento:** redistribuir num lugar com custo pequeno e motivo de história (o templo, um mestre), ou
  grátis até a especialização. A regra de [03](03-CLASSES-E-BUILDS.md) continua: não obrigar campanha nova para
  corrigir uma escolha mal explicada.
- **Descobrir:** habilidades e versões achadas pelo mundo (livro do padre na sacristia, a Vó Berta, o mercenário que
  ensina o Ímpeto) e não só pelo nível. Uma luta de treino sem risco (o desafio de Morel na taverna, onde a queda de
  braço já está) para experimentar a build montada.

---

## 10. O sistema completo: alternativas e recomendação (pendente de avaliação)

### 10.1 Três alternativas coerentes

**Alternativa 1 — Mínimo.** Kit como está; poucas versões; árvore podada; intenção só nas preparações. Barata; não cria
estilos novos.

**Alternativa 2 — Produtos e regras (recomendada para comparação prática).** O vocabulário comum (camadas, fichas,
ossos, runas, ambiente), a árvore T4 (regras por etiqueta, versões em poucas habilidades, números que disputam),
o kit em espaços com a ultimate à parte, a R7 para cadeias. Ameaças legíveis e intervenções na ordem como **módulos**
que se aprovam separadamente.

**Alternativa 3 — Escolas abertas.** As escolas atravessam as classes. Fica como direção de longo prazo.

### 10.2 A recomendação, elemento por elemento

| Elemento | Proposta | Módulo independente? | Núcleo ou depois |
|---|---|---|---|
| Vocabulário de produtos (fichas, camadas, ossos, runas, ambiente) | Etiquetas nas habilidades; poucos produtos por classe | Não: é a base | Núcleo: fichas e camadas; runas, ossos e ambiente depois do protótipo |
| Talentos | T4: regras por etiqueta, versões em habilidades centrais, números que disputam | Não | Núcleo |
| Kit | 5 espaços + espaço da ultimate (os pontos por tier saem) | Sim | Decisão do Jean |
| Intenção inimiga | Tipo e alvo para todos; números só nas preparações (R2) | **Sim** | Experimento X2 |
| Travas e chefes abalados | R3 a R5 | **Sim** | Experimento X3 |
| Ordem | Esperar e Revezamento (seção 6) | **Sim** | Experimento X4 |
| Cadeias | R7 | Não | Núcleo |
| Progressão | Seção 9 | Depende da 9 | Primeira regra no nível 2: núcleo; o resto na 9 |
| Equipamento | Itens que mudam regras de uma etiqueta (selos nos itens), números que saem da árvore | Sim | Depois do núcleo |
| Comitiva | Produtos compartilhados; versões dos companheiros depois; fundir duplicatas (Proteger, Runa) | Parcial | Fundir: núcleo |

### 10.3 Concessões

- **Mais conceitos para aprender:** fichas, produtos, ambiente. O mínimo para o começo é uma ficha e um produto por
  classe; o resto entra por fases (seção 9).
- **Etiquetas em todo o catálogo:** trabalho de dados, sem motor novo grande (os modificadores já perguntam por chave).
- **Leitura na carta:** fichas, runas e ambiente pedem espaço na HUD (seção 12).
- **Combinações não previstas:** mais combinações fortes aparecem; a R7 controla os laços, não as combinações fortes, e
  isso é intencional.
- **Se a intenção inimiga entrar,** a ordem dos sorteios muda e o gabarito e as medidas de equilíbrio precisam ser
  refeitos (vale também para qualquer mudança de regra de luta).

---

## 11. Builds diante dos mesmos encontros (simulação de design)

**Números inventados; nada medido.** Todos os trechos obedecem às regras da seção 4. Cada falha está marcada pelo tipo
(seção 5.6). A intenção inimiga (R2) aparece nos encontros porque está no experimento X2; as builds que constroem não
dependem dela.

### 11.1 As builds

| Build | Estilos | Kit (versão) | Talentos determinantes | Produto | Fraqueza |
|---|---|---|---|---|---|
| **Quebrador** (Berserker) | Responder | Golpe Pesado (Golpe que Racha: 120%, quebra até 2 travas físicas), Investida (Contratempo: atrasa 1), Quebra-Guarda, Sede de Sangue, Erguer Escudo; ult. Fúria Cega | [P] Peso do Golpe | Exposto, Força | Enxames sem preparação |
| **Fúria** (Berserker) | Arriscar | Rugido, Sede de Sangue, Redemoinho, Golpe Pesado, Ímpeto Temerário; ult. Fúria Cega | [R] Sangue Quente, [R] Sangue Frio | Fúria, Guarda ao sair | Quem agarra ou atordoa |
| **Pavio** (Piromante) | Construir | Brasa, Chuva de Brasas, Combustão (Pavio Curto), Bola de Fogo, Lança de Gelo (base); ult. Conflagração | [R] Fogo Paciente, [R] Calor Partilhado | Camadas | Lutas curtas; quem resiste ao fogo |
| **Ossário** (Necromante) | Construir, sacrificar | Erguer Servo (Servo Escudo), Lança de Osso, Muralha de Ossos, Pagar com Ossos, Drenar Vida; ult. Maldição | [R] Colheita de Ossos, [R] Pacto de Medula | Ossos, servos | Chefe sozinho; carniçal |
| **Elo** (Paladino) | Sustentar | Elo de Vida, Proteger (Muralha Viva: o protetor ganha 1 Guarda), Golpe Sagrado, Prece (Partilhada), Promessa; ult. Julgamento | [R] Luz Repartida (a sua cura também cura 30% no elo) | Guarda, cura repartida | Área; dano baixo |
| **Tocaia** (Patrulheiro) | Responder | Tiro Certeiro (Tocaia), Tiro Imobilizador (Tiro no Gatilho: sempre interrompe, só em quem prepara), Tiro Duplo, Passo Ágil, Ordem da Fera; ult. Fúria da Natureza | [R] a fera ataca o alvo da Tocaia quando ela dispara | — | Intenções simples (só ataque comum) |

A comitiva em todos: Odette e Morel, como no jogo.

### 11.2 Os encontros (inimigos que existem)

- **E1 — Três lobos** (nível 3). Mordida Sangrenta e Uivo (Fortalecido +30% em todos por 2 vezes deles). Nenhuma
  preparação. Enxame.
- **E2 — O mercenário e dois bandidos** (nível 3–4). O mercenário usa o Grito de Guerra (os aliados ficam
  Fortalecidos) e prepara o Golpe Esmagador ("sai em 1", travas físico, físico e sagrado). **Reação declarada na ficha:** abaixo da metade da
  vida, ele mira quem o feriu por último. Bandidos: Roubo e Golpe Sujo.
- **E3 — A Bruxa do Brejo, um bandido e um sapo** (Charco, nível 3). A Bruxa amaldiçoa, lança Bola de Fogo, cura o
  mais ferido a cada 3 rodadas e, nesta hipótese, cria **Água rasa** (R8). O sapo envenena e agarra (40% de prender).
  Nenhuma preparação.
- **E4 — A Bruxa Afogada, fase 2** (guardiã). Maldição, Esfera Sombria, invoca afogados; prepara a **Canção de Ninar**
  ("sai em 2", travas sagrado e gelo): enfraquece o grupo e atordoa quem estiver abaixo de 30% da vida.

### 11.3 Trechos

**E1 com a Fúria (arriscar).**
Ordem da rodada: você, lobo C, lobo A, Odette, lobo B, Morel.
Rodada 1: as intenções mostram o C uivando, o A mordendo você, o B mordendo Odette. Você usa o Rugido no A e entra na
Fúria, **sabendo** que o uivo vem antes das mordidas [risco assumido]. O C uiva; o A, Fortalecido, morde você na
Fúria (15); o B morde Odette. Rodada 2: as intenções novas põem A e B em você. Você usa o Redemoinho na Fúria: os três
ficam abaixo da metade e o C cai; Sangue Quente devolve 11 de vida. A e B mordem você (14 e 13). Odette, mordida na
rodada 1, está sangrando. Rodada 3: Odette, que ia curar você, precisa se curar [mudança provocada pelo combate].
Na sua vez, você usa a Sede de Sangue no A (que cai) e sai da Fúria no fim dela; Sangue Frio põe a Guarda em Odette,
o alvo da intenção do lobo B.

**E1 com o Ossário (construir).**
A mesma ordem do trecho anterior (você, lobo C, lobo A, Odette, lobo B, Morel).
Rodada 1: zero ossos. Você ergue o Servo Escudo (com Mana). O C uiva; A e B mordem Odette, que fica com 40% e
sangrando. Rodada 2: a intenção do lobo A, Fortalecido, é morder Odette de novo [mudança provocada pelo combate: a
mordida da rodada 1 a deixou no limite]. Na sua vez, Pagar com Ossos: o servo se desfaz, vai absorver essa mordida e
dá 2 ossos. Na vez de Morel, ele mata o lobo B: +1 osso pela Colheita (3 no total). Rodada 3: duas escolhas boas: a
Muralha (3 ossos: uma Guarda em cada aliado) ou três Lanças de Osso nas próximas vezes. Com dois lobos Fortalecidos
mordendo, você escolhe a Muralha. O C morre na vez de Morel: +1 osso, que vira a Lança da rodada 4.

**E1 com o Quebrador (desfavorável).**
Os lobos não preparam nada: o Contratempo fica apagado na escolha de alvo (nada a atrasar) e o Golpe que Racha é um
golpe de 120%. O Quebrador luta com a Sede de Sangue e o Erguer Escudo, e a luta demora uma rodada a mais que a da
Fúria. **Adaptação legítima, fora da luta:** na fogueira seguinte, ele troca o Contratempo pelo Redemoinho para as
matas, e volta a levar o Contratempo antes da capela.

**E2 com o Quebrador (responder).**
Ordem da rodada: mercenário, você, bandido A, Morel, Odette, bandido B.
Rodada 1: o mercenário grita (os bandidos ficam Fortalecidos). Você usa o Quebra-Guarda nele (nesta hipótese, deixa
o alvo Exposto). O bandido A rouba o seu ouro. Rodada 2: o mercenário prepara o Golpe Esmagador, "sai em 1", três
travas (físico, físico, sagrado), alvo Odette. Você usa o Golpe que Racha: quebra as duas físicas e consome o Exposto;
o golpe vai sair com 1/3 da força (R3). O Peso do Golpe dá Força a Morel, o próximo do grupo na ordem. O seu golpe
deixa o mercenário abaixo da metade, e a **reação declarada** na ficha dele troca o alvo da intenção para você
[mudança provocada pelo combate, prevista na ficha]. A trava sagrada sobra: Morel só bate físico, então usa a Força
no bandido A, que roubou e pode fugir. Rodada 3: o golpe do mercenário sai em você com 1/3 da força (11).

**E2 com o Pavio (construir).**
A mesma ordem do trecho anterior.
Rodada 1: Chuva de Brasas: os três com 1 camada. Morel bate no bandido B: Calor Partilhado, 2 camadas. Rodada 2: o
mercenário prepara, "sai em 1", alvo Odette, travas físico, físico e sagrado. O Pavio não tem nada físico nem sagrado.
Você tenta a Lança de Gelo base no mercenário: 35% de congelar, que num inimigo comum o atordoaria e desfaria a
preparação [risco assumido]. Não congela. Morel quebra uma trava física (2/3); o golpe dele no mercenário também o
acende (Calor Partilhado). Odette defende (vale até a próxima vez dela, que vem depois da do mercenário). Rodada 3: o
golpe sai com 2/3 em Odette, ainda defendendo (−40%). Você usa a Combustão (Pavio Curto) no bandido B, aceso com 2
camadas: a detonação vem no começo da vez dele, antes de ele agir, e ele cai. Rodada 4: Conflagração no mercenário
(aceso por Morel) e no bandido A. A preparação custou ao Pavio uma rodada inteira de aposta (a Lança); o resto da luta
foi o ritmo dele.

**E2 com o Elo (sustentar).**
A mesma ordem dos trechos anteriores.
Rodada 1: as intenções mostram o bandido A em você (roubo) e o B em Odette. Você liga Odette (frágil) e Morel (muita
vida) com o Elo de Vida, por 3 rodadas. Rodada 2: o mercenário prepara, "sai em 1", alvo Odette. A resposta de
costume é o Proteger (Muralha Viva): você levaria o golpe com uma Guarda (metade). Mas o Elo já reparte o golpe entre
Odette e Morel, metade cada, e Morel aguenta; o Proteger tiraria pouco de Odette e gastaria a sua vez. **A combinação
de costume perde para outra ação** [decisão de plano, não falha]. Você usa a Promessa ("ninguém do grupo cai até o fim
da próxima rodada"). Rodada 3: o golpe sai em Odette e é repartido: ela leva 22, Morel 22. O bandido B acerta um Golpe
Sujo nela (repartido também). Odette fica com 15% e ninguém cai [risco assumido: um crítico do bandido a derrubaria e
quebraria a Promessa]. No fim da rodada, a Promessa cumprida cura o grupo e dá Força a todos.

**E3 com o Pavio (construir, ambiente contrário).**
Este trecho é **sem a intenção visível** (o X2 desligado). Ordem: você, Bruxa, sapo, Morel, Odette, bandido.
Rodada 1: você acende os três com a Chuva de Brasas. A Bruxa cria Água rasa: o fogo perde força enquanto ela durar
(R8), e as camadas que você pôs valem menos [informação incompleta: com a intenção visível, você teria guardado a
Chuva]. Rodada 2: a Bruxa é a fonte da água e das curas; você troca de plano e usa a Bola de Fogo nela. Ela cura o
bandido (a cura não apaga a Queimadura). Rodada 3: a Lança de Gelo base, na Água rasa, congela o sapo com mais chance;
congela [mudança provocada pelo combate: o ambiente da inimiga virou o seu]. Acender e detonar fica para quando a água
sumir ou a Bruxa cair.

**E3 com a Fúria (arriscar e perder a aposta).**
Rodada 1: você usa o Rugido no bandido e entra na Fúria; a intenção do sapo é "agarrar" você [risco assumido: 40%
de prender]. Ele agarra: preso, você perde a sua vez da rodada 2, **ainda na Fúria** (só se sai no fim de uma vez
sua), e leva +50% da Bola de Fogo da Bruxa e do Golpe Sujo do bandido [o risco perdido]. Rodada 3: Firme, você age:
Sede de Sangue no sapo e, no fim da vez, sai da Fúria (a Guarda fica com você). Lição da build: contra quem prende,
entrar na Fúria cedo é caro.

**E4 com a Tocaia (responder contra chefe; R4 e R5).**
Ordem da rodada: Bruxa, você, Morel, Odette (e os afogados que ela chamar, no fim). Fase 2.
Rodada 1: na vez dela, a Bruxa Afogada prepara a Canção ("sai em 2", travas sagrado e gelo; nas vezes intermediárias
ela age normalmente, R3). Você usa o Tiro no Gatilho: ela é chefe, fica **abalada** (R5): a Canção atrasa 1 (sai em 3; primeiro
atraso). Rodada 2: a Canção desce para 2 e a Bruxa amaldiçoa Morel; a intenção seguinte dela é "invocar". Você arma
a Tocaia "ao usar habilidade de apoio". Rodada 3: na vez dela, a Canção desce para 1 e a Tocaia dispara antes da
invocação (150%); a invocação sai assim mesmo (a Tocaia não interrompe apoio). Na sua vez, o Tiro no Gatilho de novo:
abalada, segundo atraso; a Canção fica em 2 e **inadiável** (R4, contorno vermelho). Rodada 4: desce para 1. Morel
está com 28%, abaixo do limiar da Canção (30%), e Odette tem duas escolhas: curá-lo ou quebrar a trava sagrada com o
bastão, que é sagrado. Ela quebra a trava [risco assumido]: a Canção vai sair com metade da força, e, nesta hipótese,
com metade da força ela só atordoa abaixo de 15%. Rodada 5: a Canção sai com metade: o grupo fica Enfraquecido por
uma vez, e Morel, com 28%, não é atordoado [o atraso acabou; sobrou a resposta da comitiva].

### 11.4 O que os trechos mostram

- **Os quatro estilos jogam a mesma luta de jeitos diferentes**, e os que constroem, arriscam ou sustentam têm o que
  decidir contra os lobos e contra a Bruxa do Brejo, que não preparam nada.
- **Combinações abandonadas por razão legítima:** proteger o frágil com o Elo ativo; detonar na água; a Fúria contra
  quem prende; o Contratempo contra lobos (troca de kit fora da luta).
- **As falhas** vêm sobretudo de mudanças provocadas pelo combate e de riscos assumidos; a única por informação
  incompleta diz o que a intenção visível mudaria.
- **O chefe age e a sua ameaça sai**, mais fraca e mais tarde, porque o limite de atrasos funciona.
- **O que ainda não sabemos:** se o Elo é compreensível sem consultar a ficha a cada turno; se a Fúria fica divertida
  ou só arriscada; se o Ossário é lento demais no começo; se fichas, runas, ossos e ambiente juntos pesam na leitura.

---

## 12. A campanha e a apresentação

### 12.1 Que inimigos e situações dão uso às possibilidades

| Arquétipo de inimigo | Valoriza | Castiga | Existe hoje? |
|---|---|---|---|
| O que prepara (golpe forte) | Responder | Construir devagar | Só o Golpe Esmagador |
| O que sustenta o bando (cura, uivo, grito) | Responder, Inverter | Construir sem foco | Sim, sem aviso |
| Enxame | Construir (ossos, área), Arriscar (Fúria) | Responder; o Duplo | Sim |
| O que prende ou atordoa | Sustentar | Arriscar (Fúria) | Sim (sapo, aranha) |
| O que cria um ambiente | Quem explora ambientes | Quem depende do contrário | Não (proposta: a Bruxa do Brejo) |
| O que consome corpos | — | O Ossário | Sim (carniçal) |
| O que se limpa de males | Detonação rápida | Pavio, Pestilento | Não |
| O que protege outro (guarda-costas) | Quebrar guarda, Tiro que Atravessa | Foco num alvo | Não |
| O que reage (espinhos, fica mais forte ao apanhar) | Estados, proteção | Golpes muitos e fracos | Não |
| O que percebe (ignora ilusões) | — | Ilusões | Não |
| Chefe com fases e ameaça que se torna inadiável | Todos os estilos têm o que fazer | Nenhum resolve sozinho | Fases existem |

Uma habilidade sem pelo menos dois desses arquétipos onde ela fica disponível não deve entrar.

### 12.2 O que a etapa 9 precisa considerar

- **Encontros de cada arquétipo em cada região**, e encontros mistos (os que pedem adaptação).
- **Apresentação gradual:** a primeira ficha e o primeiro produto da classe nas primeiras lutas; ambientes e reações
  depois; a especialização num marco da história.
- **Acesso:** habilidades, versões e ultimates por achados com história, não só por nível.
- **Experimentar:** troca grátis em lugar seguro; uma luta de treino; lutas opcionais que favorecem estilos diferentes.
- **A curva de nível e o tamanho dos capítulos** decidem as fases da seção 9.

### 12.3 A leitura visual

| Estado | Como aparece (proposta) |
|---|---|
| Intenção (se X2 for aprovado) | Ícone sobre a carta e seta fina até o alvo; reação declarada com um ícone próprio |
| Preparação, "sai em N", travas | O número junto da intenção; travas em quadradinhos coloridos pelo tipo; inadiável com contorno vermelho |
| Fichas | Até 2 de cada tipo, embaixo da barra de vida, com a anulação animada (uma some contra a outra) |
| Camadas | Como hoje (o número na Queimadura) |
| Runas em órbita | Três encaixes ao redor do retrato do mago; a mais antiga com um contorno (é a próxima a sair) |
| Ossos | Contador no retrato do necromante, teto visível |
| Ambiente da luta | Uma faixa no fundo da arena (névoa, óleo, água) com o nome e o efeito na dica; o clima continua no canto |
| Postura (Fúria) | O contorno da carta em vermelho; "+50% causa e recebe" na dica |
| Elo | Uma linha entre as duas cartas ligadas |
| Reação armada | O ícone do gatilho e um fio pontilhado até o alvo |
| Esperar e Revezamento | A placa da rodada mostra a posição nova com uma seta curva, "só nesta rodada" |
| Cadeia | Um número pequeno em cada elo ("cadeia 2") e a faixa "já aconteceu nesta cadeia" quando parar |

Regras de leitura: uma camada por informação (sobre a carta, embaixo, entre cartas); os números na consulta, salvo
relógio, fichas e teto das moedas; caber a 1280×720; movimento reduzido sem as passagens. Nada disso é asset final.

---

## 13. As decisões que precisam do Jean

| # | Decisão | Opções | Recomendação (pendente) |
|---|---|---|---|
| 1 | Estrutura de talentos | T1 versões e princípios; T2 regras por etiqueta; T3 selos; **T4 híbrida**; T5 escolas | **T4**, comparada com T1 no protótipo (X1) |
| 2 | Vocabulário de produtos | Fichas e camadas só; mais runas, ossos e ambiente | Fichas e camadas no núcleo; os outros três no protótipo, uma classe cada |
| 3 | Intenção inimiga | Só preparações; tipo e alvo de todos; tudo com números | Tipo e alvo de todos, **como experimento separado** (X2) |
| 4 | Chefes e controle | Resistência por sorteio; abalado e travas | Abalado e travas, **experimento separado** (X3) |
| 5 | Ordem dos turnos | Fixa; Esperar e Revezamento; mais | Testar Esperar e Revezamento (X4); não mexer na posição de inimigos |
| 6 | Cadeias | Profundidade 1; R7; limites por efeito | **R7** |
| 7 | Progressão | Seção 9 | Primeira regra no nível 2; especialização num marco da história, com a ultimate |
| 8 | Kit | 8 pontos e 5 espaços; 5 espaços + ultimate à parte | 5 espaços + ultimate à parte |
| 9 | Redundâncias atuais | Fundir ou manter | Fundir junto com o núcleo |
| 10 | O cronômante | Especialização; escola; só conceito | Só conceito até X4 dizer se a ordem abre |

---

## 14. O protótipo revisado (proposta, não implementada)

Isolado em `ferramentas/prototipos/etapa8-builds/`, no molde do `combate-atributos`. O jogo integrado não muda.

### 14.1 Quatro experimentos separáveis

Cada um liga e desliga sozinho, para nenhum ser aprovado em pacote.

| # | Testa | Liga/desliga | Mantém igual |
|---|---|---|---|
| **X1** | Estrutura de talentos: T4 (regras por etiqueta + versões) contra T1 (versões + princípio) | A árvore usada na montagem | Encontros, inimigos, intenção |
| **X2** | Intenção visível (tipo e alvo) contra a de hoje (só a preparação avisa) | A exibição e a escolha antecipada | Builds, talentos |
| **X3** | Chefe abalado com travas contra resistência por sorteio | A regra do chefe | O resto |
| **X4** | Esperar e Revezamento contra a ordem fixa | Os dois comandos | O resto |

**Ordem sugerida:** X1 primeiro (é o que mais define a etapa 8 e não depende do inimigo), X2 com X1 ainda montado, X3 e
X4 depois, se o Jean quiser.

### 14.2 Builds e montagem

- **Duas especializações, duas builds cada,** para comparar dentro da mesma especialização:
  - **Berserker:** Quebrador (responde a ameaças) e Fúria (arrisca).
  - **Piromante:** Pavio e Fornalha (as duas constroem; diferem pelo ritmo e pelo risco).
- **Montagem real:** um orçamento de pontos (por exemplo, 7) e as árvores das duas estruturas (X1); o Jean monta a
  build antes de cada série e pode **remontar na fogueira entre encontros**, com o registro do que trocou e por quê.
- **Comitiva:** Odette e Morel.

### 14.3 Encontros compartilhados, favoráveis e desfavoráveis

Os mesmos para todas as builds, com inimigos que existem:

| Encontro | Favorece | Desfavorece |
|---|---|---|
| Três lobos | Fúria, Pavio | Quebrador |
| Mercenário e dois bandidos | Quebrador | Pavio (sem físico nem sagrado para as travas) |
| Bruxa do Brejo, bandido e sapo | Ninguém em especial (apoio, ambiente, prender) | Fúria (o sapo); Pavio (a água) |
| Troll (golpe preparado, regenera) sozinho | Quebrador | Fúria (golpe forte em quem está na Fúria) |

Um quinto, sorteado entre os comuns do Vale, para não haver só encontros escolhidos.

### 14.4 O que observaríamos

| Experimento | Observação | Aprova se | Rejeita se |
|---|---|---|---|
| X1 | Builds montadas e remontadas; o que o Jean diz da montagem | As duas builds da mesma especialização jogam diferente **e** o Jean troca nós entre encontros por um motivo da luta | As builds convergem; a montagem vira uma ordem óbvia de compra |
| X1 | A escolha depende do estado (seção 8.5) | Ações, alvos ou momentos mudam com a situação | A mesma sequência com a build certa, em qualquer encontro |
| X2 | Leitura e tempo por decisão | O Jean diz o que vem sem abrir fichas; decisões no tempo de hoje | Precisa abrir fichas; a luta fica lenta |
| X2 | Efeito nas builds que constroem | Ajuda pouco ou ajuda no tempo de gastar | Atrapalha (leitura demais para quem não responde) |
| X3 | O chefe age e a ameaça sai | O chefe age todas as vezes; a ameaça sai, enfraquecida ou atrasada | Chefe travado ou controle inútil |
| X4 | Uso e clareza | Esperar e Revezamento aparecem em parte das lutas, por motivo | Nunca usados; ou sempre usados (vira rotina); ou a placa confunde |
| Todos | Laços e cadeias (R7) | Nenhum laço; cadeias finitas acontecem e são lidas | Laço, ou cadeia silenciosa que o Jean não entende |

O registro grava, por rodada: o estado (vida, produtos, intenções), a ação, o alvo, e o que mudou; e, ao fim, a
montagem e as trocas.

### 14.5 Fora do protótipo

Âncora, Duplo, Engodo, Tocaia, runas, ossos, ambiente e Elo ficam para uma segunda rodada, se o X1 aprovar a estrutura.
O Grimório visual e os ícones esperam o sistema. Nada entra no jogo.

---

## A. A primeira versão: o que foi substituído

Preservado para histórico (o texto completo está no commit `12e32cfc`).

- **Recomendação de então:** "ameaça legível, resposta escolhida": intenção para todos os inimigos, relógio e travas
  nos golpes fortes, chefes abalados, catálogo por verbo, versões por habilidade, um ou dois princípios por
  especialização, números fora da árvore, ordem fixa, profundidade 1 nos gatilhos, especialização e ultimate no
  nível 4, protótipo de quatro builds respondendo ao mesmo tipo de ameaça.
- **O que continua:** o diagnóstico; a pesquisa da primeira rodada; a intenção, as travas e o abalado como
  possibilidades (agora módulos); as propostas detalhadas de Âncora, Duplo, Engodo, Tocaia, Precipitar, Retardar,
  Ímpeto Temerário, Sustentação e Juramento (descrições de interface, motor e abuso), válidas onde não contradizem a
  seção 4.
- **O que foi corrigido nas demonstrações:** o golpe do Quebrador que saía fraco com todas as travas quebradas (agora
  3 travas, 2 quebradas, 1/3); a Canção adiada para sempre (agora dois atrasos e inadiável); o Baluarte com duas ações
  numa rodada (o Proteger em versão que já dá a Guarda; uma ação por vez); o Pavio com Estilhaço tentando congelar
  (agora leva a Lança base); intenções que mudavam de alvo sem motivo (agora só pelos três motivos de R2).
