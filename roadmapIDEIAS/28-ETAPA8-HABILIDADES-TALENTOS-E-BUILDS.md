# 28 — Etapa 8: habilidades, talentos, builds e Grimório como um sistema (estudo)

Pedido do Jean, 31/10/2026, depois da taverna integrada (1.220.0). **Entrega de pesquisa e concepção: nada daqui
muda regras, telas ou conteúdo do jogo.** Os números são provisórios e servem só para os exemplos funcionarem; nenhuma
proposta deste documento é regra aprovada.

"Etapa 8" aqui é a do [plano 23](23-PLANO-DE-ARTE-INTERFACE-E-COMBATE.md) (habilidades, Grimório, árvore, ícones e
animações), não a E8 de raças e origens do [07](07-ETAPAS.md).

Como ler:

| Seção | O que tem | Natureza |
|---|---|---|
| 0 | O encaminhamento das etapas 6, 8 e 9 | Registro da decisão do Jean |
| 1 | As descobertas e as decisões a tomar | Resumo |
| 2 | O jogo que temos, medido no código da 1.220.0 | Diagnóstico (evidência) |
| 3 | As referências e o que cada uma ensina | Pesquisa (evidência externa) |
| 4 | Possibilidades além de dano e cura, o cronômante incluído | Proposta exploratória |
| 5 | Talentos e habilidades juntos | Proposta exploratória |
| 6 | Estruturas para o sistema inteiro e a recomendação | Proposta com recomendação |
| 7 | Builds diante dos mesmos encontros | Simulação de design (números inventados) |
| 8 | O que a campanha e a tela precisam oferecer | Requisitos para a etapa 9 e a arte |
| 9 | As decisões pendentes | Para o Jean |
| 10 | O protótipo pequeno proposto | Proposta |

A pergunta que guia tudo: **essas combinações mudam o que o jogador percebe, planeja, arrisca e decide durante a luta,
e continuam interessantes quando o plano dá errado?**

---

## 0. O encaminhamento: a etapa 8 antes da 9, as cenas de eventos depois das histórias

**Decisão do Jean (31/10/2026):** trabalhar a etapa 8 (habilidades, talentos, builds e Grimório) antes da etapa 9
(expansão e reescrita da campanha). As cenas de eventos ficam para depois de as histórias deles estarem definidas.

O plano 23 já punha a 8 antes da 9; o que muda é **o que fica esperando**:

| Etapa | Pendência | Antes | Agora |
|---|---|---|---|
| 5 | Interiores (templo, curandeira, taverna) | Os três integrados (1.218.0 a 1.220.0); falta a avaliação do Jean | Igual. Não reabrir as artes aprovadas |
| 6 | Cenários dos lugares (bosques, charcos, ruínas) e entornos de acampamento | Pendente | **Pode seguir** quando o Jean pedir: lugares que a reescrita mantém não dependem da história de um evento. Conferir antes, lugar a lugar, se ele continua na campanha |
| 6 | Cenas de acontecimentos (Caspar na praça e outros) | Pendente, "conferir a permanência dos acontecimentos" | **Esperam a etapa 9 definir as histórias.** Não produzir cena de acontecimento antes disso |
| 7 | Eventos recorrentes da estrada | Pendente | Mesma lógica das cenas de acontecimento, a confirmar com o Jean: os eventos que a reescrita mantém podem ganhar cena; os que vão mudar esperam |
| 8 | Sistemas, Grimório, árvore, ícones e animações | Pendente | **Agora**, começando por este estudo. Ícones e telas esperam o sistema escolhido (decisão de 19/10/2026) |
| 9 | Campanha | Rascunho em [22](22-HISTORIA-ILSE-E-A-AGUA-RASCUNHO.md) | Depois da 8. A 9 recebe da 8 os requisitos de encontros (seção 8 deste documento) |

Consequência prática para a etapa 6: ela se divide. A parte dos **lugares** fica disponível; a parte das **cenas de
acontecimento** sai da fila até a 9. A etapa 8 também passa a ditar parte do que a 9 precisa conter (inimigos com
intenção, encontros que pedem respostas diferentes, lugares para experimentar builds); ver a seção 8.

---

## 1. Resumo: o que descobri e o que precisamos decidir

### Descobertas

1. **O gargalo não está nas habilidades do herói; está no lado do inimigo.** Das 17 famílias que aparecem no Vale,
   só 3 avisam uma ação antes (o Golpe Esmagador do ent jovem, do golem e do mercenário), além das duas variantes da
   capela. O resto sorteia: 35% de chance por vez de usar uma habilidade (45% nos chefes), alvo sorteado, sem aviso.
   Sem saber o que o inimigo vai fazer, interromper, proteger, adiar, enganar e reagir não têm o que responder; sobra
   escolher o maior dano por recurso. **Quase todas as ideias interessantes deste estudo dependem de ameaças legíveis.**
2. **Muitas habilidades são a mesma decisão com outro nome.** Investida (45% de atordoar), Lança de Gelo (35% de
   congelar) e Tiro Imobilizador (60% de atordoar) são "dano num alvo com chance de ele perder a vez". Marcar Presa,
   Runa da Fragilidade, Quebra-Guarda e Flecha Perfurante são "o alvo recebe mais dano por alguns turnos". Erguer
   Escudo, Passo Ágil, Barreira Arcana, Égide Rúnica e Desaparecer são "eu tomo menos dano por um tempo". O catálogo
   tem 45 habilidades de classe e especialização, mas cerca de dez decisões distintas (a tabela da seção 2.5).
3. **Os talentos são quase todos números.** Dos 34 talentos, 19 são só "+x" de atributo, dano, crítico, custo ou
   duração. Os que mudam a maneira de jogar estão longe: a Prisão de Gelo no nível 4; Armadilheiro no 6; Rei dos
   Mortos, Coração Ardente, Imortal, Matilha e Assassino no 9, que o capítulo atual não alcança.
4. **O capítulo termina por volta do nível 4** (3,9 a 4,3 nas medidas do [17](17-E9-VALIDACAO-DO-VALE.md)). A
   especialização chega no 4, a ultimate no 6 e as camadas fortes no 6 e no 9: **a maior parte do sistema de build
   nunca entra em jogo hoje.** O que o jogador experimenta é a classe com 2 a 6 habilidades e 2 ou 3 pontos de talento
   percentuais.
5. **O recurso não cria escolha dentro de uma luta comum.** Ele volta cheio a cada luta, regenera por rodada e o
   ataque básico devolve um pouco; uma luta comum dura 4 a 7 rodadas. O documento 26 já mediu: o Golpe Pesado dura a
   luta inteira. O recurso limita o pico, não a sequência.
6. **O motor está pronto para mais do que usa.** Passos declarados (`habilidades.py`), modificadores e gatilhos
   (`modificadores.py`, `disparar`), versões de habilidade por herói (`efetiva`, a Prisão de Gelo), preparação dos
   inimigos (`carregando`), ordem fixa com a vez de cada um, a regra do Firme contra travar em sequência. Falta pouco
   de infraestrutura e muito de conteúdo com propósito.
7. **A melhor fantasia temporal cabe sem mexer na ordem dos turnos.** A ordem fixa foi aprovada ([25](25-ETAPA4-REFORCO-E-ENCANTAMENTO.md),
   3.5, que recusa aceleradores e trocas de posição). Um cronômante pode atuar sobre o **relógio das preparações**
   (adiantar, atrasar, precipitar um golpe carregado) e sobre o **estado guardado** de um combatente (a Âncora), sem
   trocar ninguém de lugar. Trocar a ordem continua possível, mas reabre aquela decisão.

### Recomendação, em uma frase

**Ameaça legível, resposta escolhida:** inimigos que declaram as ações que importam (com relógio e travas nos golpes
fortes), um catálogo organizado por *o que a habilidade mexe* (o golpe, o relógio, o alvo, a vez, o estado, o corpo) e
builds feitas de **kit + uma versão escolhida por habilidade + um ou dois princípios de especialização**, com os bônus
numéricos saindo da árvore para atributos e equipamento. Detalhes e concessões na seção 6.

### Decisões que precisamos tomar (lista completa na seção 9)

1. Quanto da intenção inimiga mostrar (todas as ações, só as fortes, ou o tipo de ação sem números).
2. Se a ordem dos turnos continua fixa (recomendado) ou se uma escola pode alterá-la por uma rodada.
3. A estrutura dos talentos: versões por habilidade (recomendado), selos encaixáveis ou a árvore ampliada.
4. O kit: pontos por tier ou só espaços, e onde a ultimate entra.
5. Quando a ultimate e a especialização chegam, dado que o capítulo termina perto do nível 4.
6. Como os chefes respondem a controle (travas e "abalado" no lugar de imunidade, recomendado).
7. Se o cronômante é uma especialização nova, uma escola de magia do Mago, ou só um teste de conceito.

---

## 2. O jogo que temos (diagnóstico na 1.220.0)

Lido no código (`rpg/habilidades.py`, `rpg/kit.py`, `rpg/talentos.py`, `rpg/estados.py`, `rpg/combate/turnos.py`,
`rpg/inimigos.py`, `rpg/dados.py`, `rpg/classes.py`) e nos documentos [14](14-E5-DIAGNOSTICO-CLASSES.md),
[15](15-E6-TRANSFORMACAO.md), [17](17-E9-VALIDACAO-DO-VALE.md), [21](21-DIAGNOSTICO-ATAQUES-EM-AREA.md),
[25](25-ETAPA4-REFORCO-E-ENCANTAMENTO.md) e [26](26-INTEGRACAO-DO-COMBATE.md). A medida do catálogo foi um script
descartável sobre os dados do jogo (os passos de cada habilidade), não uma partida.

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
- **Versões por herói (E6):** um talento libera outra ficha de uma habilidade (`VARIANTES`, `efetiva(u, h_id)`), que se
  escolhe no Grimório em lugar seguro. Só um caso: a Prisão de Gelo, versão da Lança de Gelo.
- **Modificadores e gatilhos:** talentos, passivas, classe, especialização e itens declaram `mods`, `mults` e
  `gatilhos` (início da luta, golpe recebido, golpe fatal, ataque básico, abate, morte); o combate só pergunta `mod` e
  `disparar`.
- **Estados com regras declaradas:** duração, tique, perder a vez, imunes, resistência por sorteio (chefes e gigantes
  resistem metade do atordoamento), camadas (Queimadura até 3) e o **Firme** depois de perder a vez (não se trava em
  sequência).
- **Preparação inimiga:** o Golpe Esmagador (`carregando`, ×2,2) avisa uma vez antes; atordoar no meio desfaz o golpe.
- **Combinações que existem:** Brasa ou Chuva de Brasas → Combustão ou Conflagração; Quebra-Guarda → Golpe Pesado;
  Mirar → Tiro Certeiro; Investida → Golpe Oportuno de Morel; Runa da Fragilidade → Descarga ou Nevasca.

### 2.2 O que é provisório ou só planejado

- **Todos os números** do kit (8/5/3), custos, multiplicadores, recurso da comitiva, Defender 40%, Tenacidade, e o
  próprio catálogo ([26](26-INTEGRACAO-DO-COMBATE.md), "Provisório").
- **O Golpe Oportuno de Morel:** falta o Jean dizer se vira obrigação, como a Marca virou ([25](25-ETAPA4-REFORCO-E-ENCANTAMENTO.md), 3.9).
- **Pequenos caminhos por habilidade:** hipótese do Jean de até três melhorias por habilidade, sem custos nem
  ramificações definidos ([25](25-ETAPA4-REFORCO-E-ENCANTAMENTO.md), 3.2).
- **Ultimate:** aquisição, disponibilidade e identidade em aberto (3.2 do 25).
- **Grimório e árvore visuais:** a tela antiga funciona, mas não está no patamar atual; ícones de habilidade e talento
  esperam o sistema (plano 23, etapa 8).
- **Alvo em aliado** para habilidades do herói: só existe pela comitiva e por Proteger; o fluxo geral não existe
  ([04](04-HABILIDADES-E-TALENTOS.md), "Alvos").
- **Pré-requisitos na árvore:** as linhas desenhadas não são regra de compra ([04](04-HABILIDADES-E-TALENTOS.md), "Árvore").
- **Controle de animais e servos:** continuam automáticos; decisão separada (3.4 do 25).
- **Ataques em área anunciados:** recomendados no [21](21-DIAGNOSTICO-ATAQUES-EM-AREA.md), não feitos.

### 2.3 O que limita o design por decisão intencional

| Limite | Onde foi decidido | O que impede | O que ainda deixa |
|---|---|---|---|
| Sem posicionamento, distância, cones ou linhas | 25, 3.3 | Empurrar, flanquear, áreas desenhadas | Tempo, alvo, preparação, consumo de estados, recursos, compromissos, respostas |
| Ordem fixa durante a luta; sem aceleradores, atrasos ou trocas de posição | 25, 3.5 | Haste/Slow à moda de Final Fantasy, "agir de novo" | Interromper preparações sem mexer na posição; perder a vez |
| Uma ação principal por vez; sem ações gratuitas por inferência | 25, 3.6 | Combos de várias ações num turno | Reações, desde que explicitamente especificadas |
| Kit limitado, troca fora da luta | 25, 3.1 e 3.10 | Ter tudo na mão; trocar no meio da luta | Escolher antes, adaptar entre lutas |
| Uma ultimate equipada, uma vez por luta, sem Ímpeto | 25, 3.8 | Ultimate como recompensa de acumular | Ultimate como virada escolhida |
| Preparações perigosas sinalizadas com chance real de resposta | 25, 3.3 e 3.6 | Golpe devastador de surpresa | Pressão anunciada |
| Marca do Morel recusada: preparação repetitiva que vira obrigação | 25, 3.9 | Habilidades-pedágio antes do dano | Marcas que criam uma escolha, não uma taxa |
| Tenacidade como chance, não imunidade binária | 26, pesquisa | Controle certo em todo inimigo | Controle confiável com custo ou condição |
| Grupo ativo: herói e até dois companheiros | 25, 3.4 | Grupos grandes | Sinergias de três |
| Companheiro caído só volta por ressurreição cara ou item escasso | 25, 3.4 | Reviver barato e repetido | Uma volta como ultimate |

### 2.4 O que é só limitação da implementação atual (e pode mudar)

- **A intenção inimiga é invisível e sorteada na hora** (`turnos.agir_inimigo`): habilidade com 35%/45% de chance,
  escolha ao acaso entre as que fazem sentido, alvo sorteado (`escolher_alvo_inimigo`: o provocador; o tanque da
  comitiva; um aliado ao acaso com 25% de chance, ou 15% nos chefes; senão você). Decidir a intenção um turno antes e
  mostrá-la é uma mudança de motor razoável (a habilidade já tem `quando`; falta guardar a escolha).
- **Só um golpe preparado existe** (`esmagar`), sempre igual (×2,2, uma vez de espera). Preparações de cura, invocação,
  maldição ou área não existem.
- **Interromper é binário:** atordoar desfaz o golpe inteiro, ou nada. Não há meio-termo (enfraquecer, adiar).
- **Chefes resistem por sorteio** (metade das vezes) ao atordoamento; não há uma regra que os deixe agir sempre e,
  ainda assim, ser moldados.
- **Durações contam em "turnos do portador"**, o que já é preciso, mas não há marcos de "fim da rodada" para efeitos
  adiados.
- **Talentos não mudam relações entre habilidades** (só `transforma` numa habilidade, um caso).
- **Não há reação armada pelo jogador** (o Contragolpe é a única, e é passiva: revida golpe corpo a corpo).
- **Não há alvo em aliado** para as defesas do herói (Barreira, Égide, Erguer Escudo só em você).
- **O ataque básico é idêntico em toda build** (o golpe da classe e a devolução de recurso).

### 2.5 Medidas

**O catálogo** (45 habilidades de classe e especialização; o tier é o do kit):

| Estrutura | Quantas | Exemplos |
|---|---|---|
| Só dano | 7 | Golpe Pesado, Tiro Certeiro, Tiro Duplo, Lâmina Rúnica, Descarga, Julgamento, Rajada |
| Dano + estado com chance ou garantido | 15 | Investida, Lança de Gelo, Tiro Imobilizador, Bola de Fogo, Sede de Sangue, Flecha Sangrenta, Flecha Envenenada, Quebra-Guarda, Flecha Perfurante, Brasa, Chuva de Brasas, Nevasca, Golpe Sagrado, Drenar Vida, Fúria da Natureza |
| Sem dano (buff, marca, defesa, recurso, invocação) | 23 | Erguer Escudo, Passo Ágil, Barreira, Égide, Desaparecer, Mirar, Marcar Presa, Runa, Grito de Guerra, Proteger, Contragolpe, Prece, Meditar, Erguer Servo, Maldição... |

Dano por ponto de recurso (multiplicador × 100 / custo), só onde a conta é direta: Tiro Certeiro 21, Tiro Duplo 18,
Golpe Pesado 17, Lança de Gelo 13, Flecha Sangrenta 12,5, Lâmina Rúnica 11,4, Bola de Fogo 10,7, Investida 10, Flecha
Perfurante 10, Descarga 9,2, Golpe Sagrado 8,7, Drenar Vida 8,6, Quebra-Guarda 7,9, Brasa 7,5, Tiro Imobilizador 6,7.
Com o recurso cheio a cada luta, a habilidade de topo de cada classe tende a ser o botão padrão; as outras precisam de
um motivo de situação, e esse motivo quase sempre é "o inimigo vai fazer algo" (que hoje não se vê).

**As decisões reais escondidas no catálogo** (agrupando o que faz a mesma coisa):

| Decisão | Habilidades que a oferecem | Quando ela importa hoje |
|---|---|---|
| Bater forte num alvo | Golpe Pesado, Tiro Certeiro, Descarga, Lâmina Rúnica, Tiro Duplo, Rajada | Sempre (o padrão) |
| Bater em todos | Redemoinho, Chuva de Flechas, Nevasca, Chuva de Brasas, ultimates de área | 2+ inimigos |
| Tirar a vez de alguém (com chance) | Investida, Lança de Gelo, Tiro Imobilizador, Nevasca, Golpe no Joelho (Morel) | Só contra preparação, porque o resto do turno inimigo é desconhecido |
| Fazer o alvo receber mais | Marcar Presa, Runa da Fragilidade (herói e Yara), Quebra-Guarda, Flecha Perfurante, Maldição | Lutas longas (chefe) |
| Eu tomar menos | Erguer Escudo, Passo Ágil, Barreira, Égide, Desaparecer, Defender | Golpe preparado; vida baixa |
| Outro tomar no meu lugar | Proteger (herói e Morel), Erguer Servo, Ordem da Fera (urso) | Aliado ferido |
| Acumular e detonar | Brasa/Chuva → Combustão/Conflagração | O único ciclo de duas etapas que muda a ordem das ações |
| Dano ao longo do tempo | Sangramento, Veneno, Queimadura, Maldição | Lutas longas; imunes (mortos-vivos, construtos) |
| Trocar vida por algo | Fúria Cega, Pacto de Sangue, Sede de Sangue | Berserker |
| Recurso | Meditar, Sifão, ataque básico | Mago, raramente |

**Os inimigos do Vale** (biomas planície, pântano, floresta e ruínas: 17 famílias):

| Habilidade inimiga | Famílias | Avisa antes? |
|---|---|---|
| Drenar, Veneno, Golpe Sujo, Mordida Sangrenta | 3 cada | Não |
| Golpe Esmagador (`esmagar`) | 3 (ent jovem, golem, mercenário) + as duas variantes da capela | **Sim** |
| Agarrar, Cura, Grito de Terror, Investida | 2 cada | Não |
| Teia, Roubo, Maldição, Bola de Fogo, Devorar, Esfera Sombria, Regenerar, Uivo, Grito de Guerra | 1 cada | Não |

Respostas que o jogo já sabe dar a cada ameaça: matar primeiro quem cura; atordoar ou se proteger contra o golpe
preparado; Prece contra os males. As outras ameaças são ruído: chegam sem aviso e não pedem uma resposta específica.

**O alcance do capítulo:** o nível no fim do Vale é 3,9 a 4,3 nos percursos medidos depois da 1.64.0
([17](17-E9-VALIDACAO-DO-VALE.md), seção 15, a tabela do ritmo); um ponto de talento por nível, mais os de guardiões. No nível 4 o herói tem uns 3 pontos (os
níveis 2, 3 e 4) e os de guardiões, quase todos gastos na camada de nível 2 (só números), e acabou de escolher a
especialização.

### 2.6 O que muda a maneira de jogar e o que tende a ser redundante

**Muda a maneira de jogar** (decisões que dependem do que acontece na luta):

- **Combustão e Conflagração:** acender agora, detonar depois; a ordem das ações importa e o momento de detonar é
  escolha (expiração, resistência, quantos alvos acesos).
- **Interromper o Golpe Esmagador** (Investida, Lança, Imobilizador, Prisão de Gelo, Golpe no Joelho): a única ameaça
  que pede resposta, por isso as lutas da capela com golpe preparado foram as primeiras a dar função a essas
  habilidades ([14](14-E5-DIAGNOSTICO-CLASSES.md), seção 10).
- **Prisão de Gelo × Lança de Gelo:** a única versão escolhida; troca dano por certeza, e serve num tipo de luta.
- **Proteger:** decidir quem apanha.
- **Execução:** o limiar de 35% cria um momento.
- **Tiro Duplo:** o segundo disparo vai no mais ferido; muda a escolha de alvo.
- **Rei dos Mortos, Erguer Servo, Ordem da Fera:** a luta ganha um corpo a mais, com regras próprias.
- **Defender:** resposta universal ao golpe anunciado, sem composição específica.

**Tende a ser redundante:**

- As três habilidades de "chance de tirar a vez" (Investida, Lança de Gelo, Tiro Imobilizador) diferem pela chance e
  pelo dano, não pela decisão. Contra inimigos que não preparam nada, perder a vez é só dano a menos recebido.
- Os quatro "alvo recebe mais" com números parecidos. Marcar Presa sofre o problema que levou a Marca do Morel a ser
  recusada: um turno de pedágio antes do dano.
- As cinco defesas pessoais: escolher entre elas é escolher um número.
- Proteger e Runa da Fragilidade repetidos na comitiva (Morel e Yara) e no herói.
- Mirar → Tiro Certeiro: dois turnos para um crítico; com o recurso sobrando, vira rotina.
- Os talentos de camada 1 (Pele de Ferro, Golpe Brutal, Fôlego, Olho de Águia, Pés Leves, Mente Vasta, Potência
  Arcana, Canalização): bônus sem decisão; o único que muda o comportamento é a Aljava Funda (as flechas).

**Na luta real**, com inimigos que não avisam, a sequência ideal de cada classe se repete: o Guerreiro usa o Golpe
Pesado e se protege quando avisado; o Arqueiro, o Tiro Certeiro; o Mago alterna Bola de Fogo e Lança. O robô do
simulador joga exatamente assim e ganha 82% a 97% das lutas comuns ([26](26-INTEGRACAO-DO-COMBATE.md)). Isso não
prova o que uma pessoa faz, mas mostra que a regra simples basta.

---

## 3. Pesquisa: o que outros sistemas ensinam

Critério: escolhi referências pelo mecanismo que sustenta a decisão, não pela fama. Para cada uma, o que é
verificável e de onde. Fontes de desenvolvedor ou oficiais primeiro; wikis de fãs quando a regra é observável no jogo,
marcadas como tal. Não reproduzo números de balanceamento delas: não se aplicam.

### 3.1 Slay the Spire (Mega Crit, 2019): a intenção do inimigo

- **Mecanismo:** um ícone sobre cada inimigo mostra a próxima ação (ataque com o dano e o número de golpes, defesa,
  buff, debuff). A intenção é a verdade: o inimigo faz o que mostrou, salvo se você mudar a situação (matar, enfraquecer
  e assim reduzir o número mostrado). Cada turno vira uma pergunta concreta: "ele vai bater 18; eu bloqueio, mato ou
  aceito?"
- **Habilidades e modificadores:** as cartas e as relíquias mudam *quanto* e *como* você responde a uma intenção
  conhecida (bloquear muito, enfraquecer para reduzir o golpe, matar antes).
- **Builds:** arquétipos surgem de cartas que compartilham uma moeda (Força, veneno, bloqueio retido, cartas
  exauridas) e de relíquias que mudam regras.
- **O que impede a solução universal:** inimigos desenhados em conjunto com as cartas para testar estratégias
  diferentes; o designer Anthony Giovannetti diz que queriam inimigos que testassem estratégias de maneiras diferentes
  para nenhuma abordagem dominar ([Game Developer, 2020](https://www.gamedeveloper.com/disciplines/road-to-the-igf-mega-crit-games-i-slay-the-spire-i-)).
  A palestra do GDC 2019 sobre o balanceamento por métricas é dele ([GDC Vault](https://www.gdcvault.com/browse/gdc-19/play/1025731)).
- **Depende do que não temos:** do baralho e da mão sorteada (a variação de cada turno vem das cartas); nós temos um
  kit fixo.
- **Adaptação:** a intenção é o mecanismo mais transferível de todo este estudo. Sem mão sorteada, a variação de cada
  turno precisa vir **da intenção e das respostas concorrentes** (vários inimigos com intenções diferentes; recurso e
  uma ação só).

### 3.2 Into the Breach (Subset Games, 2018): ameaça anunciada e manipulável

- **Mecanismo:** todo ataque inimigo é anunciado um turno antes, com o alvo; o jogador não tem sorte nas próprias
  ações. Justin Ma: queriam menos aleatoriedade que em FTL, que cada morte parecesse culpa do jogador, e o resultado
  "começa a parecer um quebra-cabeça" ([Game Developer, 23/02/2018](https://www.gamedeveloper.com/game-platforms/road-to-the-igf-subset-games-i-into-the-breach-i-)).
- **Habilidades:** a maior parte das armas não mata: empurra, puxa, bloqueia, troca o alvo do ataque anunciado.
  Responder a uma ameaça conhecida vale mais que dano.
- **Builds:** cada esquadrão é um conjunto de verbos de manipulação; os pilotos e melhorias mudam o verbo.
- **Impede a solução universal:** mais ameaças por turno do que ações para resolvê-las; objetivos que obrigam a
  aceitar perdas.
- **Depende do que não temos:** do tabuleiro. Empurrar o inimigo para o ataque do outro é posicionamento.
- **Adaptação:** sem tabuleiro, manipular a ameaça vira **redirecionar o alvo** (chamariz, proteção), **mudar o
  momento** (adiar, precipitar) e **reduzir a ameaça** (quebrar travas, enfraquecer). Tudo isso exige o alvo e o momento
  visíveis.

### 3.3 Sea of Stars (Sabotage, 2023): travas em vez de interromper ou nada

- **Mecanismo:** quando um inimigo prepara um feitiço, aparecem sobre ele um contador de turnos e "travas", cada uma
  de um tipo de dano. Acertar com o tipo quebra a trava; cada trava quebrada enfraquece o golpe; todas quebradas o
  cancelam. O diretor, Thierry Boulanger, descreveu a primeira versão: era ótimo quebrar as travas, mas frustrante ficar
  com uma sobrando, então acrescentaram a indicação de força que diminui a cada trava
  ([entrevista, God is a Geek, 2023](https://www.godisageek.com/2023/10/sea-of-stars-nearly-had-a-skate-park-style-boating-mini-game)).
  Também há golpes que atrasam a vez do inimigo (guias de terceiros).
- **Habilidades:** o tipo de dano de cada habilidade ganha uma segunda função (quebrar a trava certa), além do dano.
- **Builds:** a composição do grupo decide quais travas você quebra bem.
- **Impede a solução universal:** travas variadas pedem tipos variados; o contador limita o tempo.
- **Depende do que não temos:** os golpes com tempo de botão (reflexo). As travas em si não dependem.
- **Adaptação:** **o meio-termo que falta ao nosso interromper.** Um golpe preparado de chefe com 2 ou 3 travas
  (físico, gelo, sagrado...) deixa de ser "atordoou ou não": cada ação conta, o chefe ainda age, e o tipo de dano vira
  decisão além da tabela de fraquezas.

### 3.4 Final Fantasy X (Square, 2001): a ordem visível e manipulável

- **Mecanismo:** a janela de ordem mostra as próximas vezes; Haste e Slow mudam a frequência de alguém; os golpes de
  atraso empurram a próxima vez do alvo; cada ação tem um peso que define quando a próxima vez volta. Guias de fãs
  documentam as contas ([FFX-Info](https://grayfox96.github.io/FFX-Info/game-mechanics/ctb),
  [jegged](https://jegged.com/Games/Final-Fantasy-X/Tips-and-Tricks/CTB-Window.html)).
- **Habilidades e builds:** velocidade e atraso viram recurso; a festa de "Delay Buster" trava chefes.
- **Impede a solução universal:** pouco, no jogo original: atrasar repetidamente deixava inimigos sem agir; chefes
  imunes eram a resposta, e imunidade binária é justamente o que queremos evitar.
- **Depende do que não temos:** ordem recalculada a cada ação. A nossa é fixa por decisão (25, 3.5).
- **Adaptação:** a ordem visível já entrou (a placa da rodada). Manipular a ordem conflita com a decisão; o que se pode
  aproveitar é **mexer no relógio de uma preparação** (quantas vezes do inimigo faltam), que não troca ninguém de lugar.
  O risco de travar inimigos para sempre é a lição a guardar.

### 3.5 Octopath Traveler (Square Enix, 2018): quebra e reserva

- **Mecanismo:** cada inimigo tem escudos que caem com acertos nas fraquezas; com zero, ele "quebra": perde a próxima
  ação e recebe mais dano, e o escudo volta cheio depois. O "Boost" guarda pontos por turno para reforçar uma ação
  depois. Fontes de terceiros ([GamerGuides](https://www.gamerguides.com/octopath-traveler/guide/the-basics/game-mechanics/battle-system)).
- **Habilidades e builds:** o tipo de cada ação importa para quebrar; guardar ou gastar o Boost é uma escolha de tempo.
- **Impede a solução universal:** o escudo se recompõe; chefes têm mais escudos; fraquezas escondidas até descobertas.
- **Depende do que não temos:** nada essencial.
- **Adaptação:** dois aprendizados: (1) **o controle que se reconstrói** (o chefe quebra, perde uma ação, e volta a
  exigir trabalho) é melhor que imunidade; (2) **guardar para depois** é uma decisão de tempo que cabe na ordem fixa.

### 3.6 Wildfrost (Deadpan Games, 2023): contadores visíveis e congelar o relógio

- **Mecanismo:** cada unidade tem um contador; a cada turno ele desce 1 e a unidade age ao chegar a zero. A "Neve" para
  o contador. Alguns inimigos resistem à Neve ([Wildfrost Wiki](https://wildfrostwiki.com/Getting_Started); wiki de fãs).
- **Habilidades:** muitas cartas mexem no contador (o seu ou o do inimigo) em vez de causar dano.
- **Impede a solução universal:** inimigos resistentes, contadores curtos demais para parar todos.
- **Depende do que não temos:** a ordem é o contador, e o contador muda; a nossa ordem não muda.
- **Adaptação:** **o contador vale para a preparação, não para a vez.** Um golpe preparado com "2" em cima, que desce a
  cada vez do inimigo, é legível e manipulável (adiar, precipitar) sem mudar a ordem.

### 3.7 Guild Wars (ArenaNet, 2005): barra de oito, muitas habilidades, uma elite

- **Mecanismo:** cada personagem leva no máximo 8 habilidades, no máximo uma elite, trocadas só fora das áreas de
  combate (cidades e postos), de um repertório de centenas, combinando duas profissões
  ([Guild Wars Wiki, oficial](https://wiki.guildwars.com/wiki/Skill); o acesso ao wiki hoje pede conta, a regra foi
  conferida pelo índice da página). Interrupções só valem contra o que tem tempo de ativação
  ([Interrupt effect](https://wiki.guildwars.com/wiki/Interrupt_effect)).
- **Habilidades e modificadores:** os atributos da profissão aumentam famílias de habilidades; a barra é a build.
- **Builds:** a combinação de oito é o que cria arquétipos; a elite ancora a identidade.
- **Impede a solução universal:** contramedidas (interromper, remover maldições, punir quem age demais) e o tamanho da
  barra. Mesmo assim, a comunidade convergia em poucas barras dominantes: muitas habilidades não garantem muitas builds.
- **Depende do que não temos:** tempo real, reflexo para interromper.
- **Adaptação:** o nosso kit é a mesma ideia em escala menor. O aprendizado é o aviso: **o tamanho do repertório não
  produz variedade; as contramedidas e as situações produzem.**

### 3.8 Darkest Dungeon 1 e 2 (Red Hook, 2016 e 2023): quatro de sete, marcas e caminhos

- **Mecanismo:** cada herói tem 7 habilidades de combate e leva 4, trocadas fora da luta
  ([wiki oficial](https://darkestdungeon.wiki.gg/wiki/Heroes_(Darkest_Dungeon))). A **marca** faz a maioria dos
  inimigos preferir o marcado; habilidades do grupo rendem mais contra marcados
  ([Mark](https://darkestdungeon.wiki.gg/wiki/Mark)). No 2, os **caminhos** de cada herói mudam atributos e
  habilidades, com forças e fraquezas, escolhidos numa encruzilhada
  ([Red Hook, notícia oficial](https://store.epicgames.com/news/first-major-darkest-dungeon-ii-update-draws-from-original-beasties-and-more)).
- **Habilidades e modificadores:** a marca é uma relação entre duas habilidades de personagens diferentes (quem marca,
  quem aproveita) e com o inimigo (quem prefere bater no marcado). Isso é o oposto da Marca recusada do Morel: lá era
  pedágio; aqui é uma isca com risco (o marcado apanha mais).
- **Builds:** a mesma classe joga diferente pelo caminho e pelas quatro habilidades escolhidas.
- **Impede a solução universal:** a posição (que nós não temos) e o estresse.
- **Adaptação:** quatro de sete é praticamente o nosso kit. O **caminho com fraqueza** é o modelo das versões de
  habilidade com perda (seção 5). A **marca como isca** é um uso de marca que não é taxa.

### 3.9 Path of Exile (Grinding Gear Games): suportes que mudam a entrega

- **Mecanismo:** gemas de suporte ligadas a uma habilidade mudam o comportamento dela (lançar como armadilha, como
  mina, repetir o feitiço) e cobram mais recurso; algumas são incompatíveis entre si (um feitiço com Armadilha não pode
  ter Eco) ([wiki de fãs, Support gem](https://www.poewiki.net/wiki/Support_gem);
  [Trap Support](https://www.poewiki.net/wiki/Trap_support)).
- **Habilidades e modificadores:** o modificador é universal (serve em muitas habilidades) e ocupa um espaço limitado.
- **Builds:** a mesma habilidade vira ferramentas diferentes pela entrega.
- **Impede a solução universal:** espaços escassos, custo multiplicado, incompatibilidades.
- **Depende do que não temos:** tempo real, quantidade de golpes por segundo, loot massivo.
- **Adaptação:** **mudar a entrega** é poderoso no nosso formato também: "agora" × "na próxima vez do alvo" × "quando o
  gatilho acontecer" (reação). Um "selo de tocaia" que transforma qualquer golpe em reação é a tradução direta. O
  risco é a perda de identidade (todo mundo com o mesmo selo); seção 5.

### 3.10 Diablo IV (Blizzard): ramos por habilidade, revistos em 2026

- **Mecanismo:** cada habilidade tem melhorias; até 2026, uma melhoria e depois a escolha entre duas. A revisão de
  abril de 2026 transformou a árvore em ramos por habilidade em que "as melhorias que você escolhe mudam a maneira de
  jogar"; exemplo da Blizzard: o Rend do Bárbaro pode virar fogo, mandar ondas ou alcançar longe, conforme o ramo
  ([Xbox Wire, 22/04/2026](https://news.xbox.com/en-us/2026/04/22/diablo-4-skill-tree-overhaul/)). O motivo dado: a
  árvore antiga era "mais do mesmo" para veteranos.
- **Habilidades e modificadores:** o modificador mora na habilidade; escolher um ramo fecha o outro.
- **Builds:** a mesma habilidade de base em pontos de chegada diferentes.
- **Impede a solução universal:** a exclusão entre ramos e os pontos.
- **Depende do que não temos:** o espaço e a velocidade do combate de ação.
- **Adaptação:** é a forma mais próxima da hipótese do Jean ("pequenos caminhos por habilidade", 25, 3.2) e da Prisão
  de Gelo. O próprio estúdio confirma o problema que queremos evitar: melhorias que só somam número envelhecem.

### 3.11 D&D 5e (Wizards of the Coast): concentração, preparar uma ação e reação

- **Mecanismo:** **concentração**: um conjurador sustenta só um efeito de cada vez; sofrer dano pode quebrá-lo;
  começar outro encerra o primeiro. **Preparar (Ready):** gastar a ação para agir depois, quando um gatilho declarado
  acontecer, usando a reação, até o começo da sua próxima vez; uma reação por rodada
  ([SRD 5.1, oficial](https://media.wizards.com/2016/downloads/DND/SRD-OGL_V5.1.pdf)).
- **Habilidades e modificadores:** a concentração limita os controles mais fortes sem precisar de imunidade.
- **Builds:** o conjurador de controle aceita a fragilidade da concentração; o de dano não.
- **Impede a solução universal:** um efeito sustentado de cada vez; a reação única.
- **Depende do que não temos:** o mestre que interpreta gatilhos. Nós precisamos de gatilhos fechados numa lista.
- **Adaptação:** **a concentração é a regra-mãe dos controles fortes** (um sustentado por personagem, que cai se ele
  levar golpe forte) e **preparar uma ação** é a base da reação armada (seção 4).

### 3.12 Legends of Runeterra (Riot): velocidade de resposta

- **Mecanismo:** feitiços têm velocidades: instantâneos que não dão chance de resposta, rápidos que respondem a outros,
  lentos que só saem na sua iniciativa e que o oponente pode responder
  ([suporte oficial da Riot](https://support-legendsofruneterra.riotgames.com/hc/articles/360036067293)).
- **Adaptação:** a ideia útil é **classificar o que pode ser respondido**: um golpe preparado responde-se; um ataque
  comum não. Isso organiza a intenção (o que mostra contador e travas) e as reações (o que elas podem pegar).

### 3.13 Shin Megami Tensei (Atlus): a economia de ações

- **Mecanismo:** cada lado tem um número de "turnos de pressão" por rodada; acertar uma fraqueza ou um crítico gasta
  meio turno (ganha-se ação); errar ou acertar uma resistência gasta mais
  ([Megami Tensei Wiki](https://megatenwiki.com/wiki/Press_Turn_System); wiki de fãs). Vale para os inimigos também.
- **Adaptação:** **com cuidado.** Ações extras geram a sequência que se repete e o risco de ciclos; o nosso "uma ação
  por vez" foi decidido. O que serve é a ideia de **pagar a ação com outra coisa**: agir agora e perder a próxima vez
  (seção 4, Ímpeto Temerário), sem gerar ação de graça.

### 3.14 Chained Echoes (Matthias Linda, 2022): um estado compartilhado

- **Mecanismo:** uma barra comum ao grupo sobe com as ações e desce com defender e trocar; na faixa certa, mais dano e
  menos dano recebido; acima, o contrário ([guia de terceiros](https://gameranx.com/features/id/429682/article/chained-echoes-how-to-lower-heat-overdrive-system-explained/)).
- **Crítica registrada:** parte dos jogadores acha que ela elimina estratégia porque se escolhe o que mantém a barra na
  faixa; é um alerta para qualquer "mantenha X no ponto ideal": vira a sequência automática.
- **Adaptação:** não recomendo um medidor global. Fica o alerta.

### 3.15 Síntese: seis lições

1. **Intenção visível antes de verbos novos.** Sem saber o que vem, interromper, proteger e enganar não têm motivo
   (Slay the Spire, Into the Breach).
2. **Interromper em graus.** Travas e atrasos fazem cada ação contar e deixam o chefe agir (Sea of Stars, Octopath,
   Wildfrost). Imunidade binária é o remendo que queremos evitar (Final Fantasy X).
3. **Modificar a habilidade, não o número.** Versões e suportes mudam o que a habilidade faz (Diablo IV, Path of
   Exile, Darkest Dungeon 2). Limitar por exclusão, não por custo.
4. **Variedade vem das situações e das contramedidas, não do tamanho do catálogo** (Guild Wars).
5. **Controle forte sustentado e frágil** (concentração), **reação declarada e paga** (preparar a ação).
6. **Desconfiar de medidores para manter no ponto ideal e de ações extras** (Chained Echoes, Megami Tensei).

| Referência | Depende de algo que não temos? | O que trazemos |
|---|---|---|
| Slay the Spire | Mão sorteada | Intenção |
| Into the Breach | Tabuleiro | Ameaça anunciada e manipulável (alvo e momento) |
| Sea of Stars | Reflexo nos golpes | Travas |
| Final Fantasy X | Ordem recalculada | Só a lição do risco; relógio da preparação |
| Octopath | — | Controle que se reconstrói; guardar para depois |
| Wildfrost | Ordem por contador | Contador na preparação |
| Guild Wars | Tempo real | Barra pequena, contramedidas |
| Darkest Dungeon | Posição | Quatro de sete; marca como isca; caminho com fraqueza |
| Path of Exile | Ação em tempo real | Mudar a entrega |
| Diablo IV | Ação | Ramos por habilidade |
| D&D 5e | Mestre | Concentração; preparar a ação |
| Runeterra | Duas pessoas | O que pode ser respondido |
| Megami Tensei | — | Pagar ação com ação (com cuidado) |
| Chained Echoes | — | Alerta contra o ponto ideal |

---

## 4. Possibilidades além de causar dano e curar

### 4.1 O que uma habilidade pode mexer

Organizar o catálogo pelo objeto da ação, não pelo elemento:

| Mexe em | Verbos | Já existe | Depende de intenção visível? |
|---|---|---|---|
| **O golpe** | dano, área, crítico, executar | Muito | Não |
| **O relógio** (das preparações) | interromper, atrasar, adiantar, precipitar, quebrar trava | Interromper binário | Sim |
| **O alvo** | proteger, redirecionar, chamariz, ilusão, provocar | Proteger, servo, urso | Sim, para valer |
| **A vez** | reação armada, guardar a ação, agir agora e pagar depois, efeito adiado | Contragolpe (passivo) | Em parte |
| **O estado** | aplicar, consumir, converter, transferir, roubar, dissipar | Aplicar, consumir (fogo) | Não |
| **O corpo** | vida como custo, sacrifício de servo, voltar ao estado guardado | Fúria Cega, Pacto | Não |
| **O recurso** | recuperar, emprestar, transferir à comitiva | Meditar, Sifão | Não |

As colunas de cima (golpe) estão cheias; as do meio (relógio, alvo, vez) estão quase vazias. É ali que estão as
decisões que mudam de luta para luta.

### 4.2 A base que as outras propostas pedem: a ameaça legível

Não é uma habilidade; é a mudança no lado do inimigo que dá sentido às respostas. Proposta:

- **Cada inimigo decide a próxima ação no fim da vez dele** (ou no começo da luta, para a primeira) e ela aparece
  sobre a carta: um ícone do tipo (golpe, golpe forte, preparação, apoio aos seus, feitiço em você, invocação), uma
  seta para o alvo e, só nas preparações, o contador e as travas.
- **A intenção se mantém**, salvo três gatilhos fechados: o alvo caiu (escolhe outro pela regra de sempre), o inimigo
  perdeu a vez, ou uma habilidade a mudou (redirecionar, chamariz). Isso garante que a informação é verdadeira.
- **Golpes comuns mostram o alvo sem número**; os números ficam na consulta (decisão a confirmar: 25, 3.3 diz que não é
  obrigatório revelar todo ataque comum).
- **Preparação com relógio:** "2" desce a cada vez do inimigo; com "0" o golpe sai. **Travas:** 0 a 3 tipos (físico,
  gelo, sagrado, arcano...). Cada trava quebrada tira uma parte do golpe; todas, cancela.
- **Chefes não perdem a vez por atordoamento:** ficam **abalados** (a preparação recua 1 no relógio, ou uma trava
  cai). Assim o chefe sempre age, e mesmo assim é moldável.

Exige do motor: guardar `intencao` no inimigo (habilidade, alvo, relógio, travas), escolher no fim da vez, um ponto de
reavaliação, lances novos para a tela. **Muda a ordem dos sorteios** (o gabarito muda de propósito). O que fica
repetitivo: se todo inimigo prepara, a luta vira contar relógios; preparações devem ser poucas por luta (uma a cada
duas ou três rodadas, e só nos inimigos de peso).

### 4.3 Explorando o cronômante

As provocações do Jean, examinadas uma a uma. Nenhuma é habilidade aprovada.

#### Voltar um turno atrás

O que "voltar" pode significar, e o que cada versão faz:

| Versão | O que restaura | O que o jogador sabe depois | O inimigo repete? | Problema |
|---|---|---|---|---|
| A. A luta inteira | Tudo, inclusive os sorteios | Tudo o que viu | Se o sorteio volta igual, sim; se não, é sortear de novo | Vira tentativa infinita até o resultado bom; quebra a regra de que o motor decide; gabarito impossível |
| B. A luta inteira, sem os sorteios | Vida, estados e recursos de todos | Tudo | Não (o sorteio continua de onde estava) | Um "desfazer" geral: o jogador apaga erros sem custo de decisão; confuso de ler (tudo muda de uma vez) |
| C. Um combatente | Vida e estados de um só, ao ponto marcado | Tudo | Não | **Compreensível e limitado. Recomendada.** |
| D. A última ação de alguém | Desfaz o efeito de uma ação | Tudo | O inimigo perde a ação | Um "cancelar" disfarçado; difícil de descrever com golpes que têm vários efeitos |

**Proposta: a Âncora** (versão C).

- **O que o jogador faz:** na sua vez, ancora um combatente (você, um aliado ou um inimigo). A carta dele ganha um selo
  de âncora e uma sombra da barra de vida no valor de agora. Em qualquer vez sua nas duas rodadas seguintes, **Puxar a
  âncora** (outra ação) devolve a vida e os estados dele aos do momento da âncora. Recurso, cargas de preparação,
  ultimate usada e quem caiu não voltam. Depois de puxar, ou se as duas rodadas passarem, a âncora some.
- **O que observa:** a sombra na barra mostra a diferença entre o agora e o guardado; ela diz, sem conta, se puxar
  ajuda ou atrapalha.
- **Quando vale:** num aliado, antes de um golpe preparado que vai pegá-lo (o seguro). Num inimigo, quando ele vai se
  curar ou se fortalecer mais do que você vai feri-lo: a Bruxa do Brejo, o troll que regenera, o lobo que vai uivar.
- **Quando não vale:** num inimigo que você está ferindo bem (puxar devolve a vida dele); contra golpes pequenos e
  constantes (duas ações para desfazer pouco); quando a ameaça é um estado que não pega no ancorado.
- **O que sacrifica:** duas ações (ancorar e puxar), uma delas sem efeito imediato; e o risco de as duas rodadas
  passarem sem a situação certa.
- **Comitiva e inimigos:** ancorar Morel antes de ele proteger alguém; ancorar o inimigo que Yara amaldiçoou é ruim
  (puxar tira a maldição). Inimigos que limpam os próprios males (cura) e os que se fortalecem viram alvos naturais.
- **Interface:** o selo de âncora na carta; a sombra na barra de vida; os ícones dos estados guardados em cinza ao lado.
  Ao puxar: a barra "rebobina" (a animação corre de trás para frente), os estados somem ou voltam.
- **Motor:** uma cópia de `hp` e `efeitos` do combatente, a validade em rodadas, um lance `ancora` e um `puxar`.
  Simples; a cópia não pode guardar referências (o `por` do Protegido aponta para outro combatente).
- **Abuso e confusão:** a Âncora vira uma cura de duas ações; o limite é **uma Âncora por luta** na versão comum, e
  puxar nunca passa da vida máxima atual. Se as escolas um dia se abrirem (seção 6.1, alternativa 3), ancorar a si mesmo
  antes de pagar um custo em vida (a Fúria Cega) e puxar desfaria o custo; nesse caso, **o custo em vida não volta**.
  A ultimate pode levantar um caído (a Hora Revivida, seção 7), coerente com "ressurreição de alto custo" (25, 3.4).
  Não há como tentar até dar certo: o sorteio nunca volta.

#### Acelerar a resolução de um golpe carregado

Três alvos para a mesma ideia, com decisões diferentes:

- **Adiantar o seu golpe carregado.** Se o herói tem habilidades que carregam (sai na próxima vez, mais fortes), a
  Pressa faz uma delas sair agora. Decisão: pagar a Pressa para ganhar uma vez, ou esperar.
- **Adiantar o golpe carregado de um aliado** (Morel preparando o Golpe no Joelho, se ganhar uma versão carregada): o
  benefício vai para a comitiva, e a escolha é de quem acelerar.
- **Precipitar o golpe carregado do inimigo** (a provocação mais rica). O golpe preparado sai **agora**, no alvo que a
  intenção mostra, com as travas que ainda restam. Vale quando o alvo está pronto para receber (Defender ativo,
  Barreira, Proteger, a ilusão na frente) e as defesas vão expirar antes do relógio; ou quando o inimigo está
  fortalecido por pouco tempo e o fortalecimento acabaria antes. Não vale com o alvo desprotegido. Sacrifica: a sua
  ação inteira, sem dano. É o verbo que faz o cronômante *escolher a hora* da ameaça, sem mudar a ordem de ninguém.

#### Usar a aceleração para beneficiar a comitiva

A Pressa num aliado não pode virar uma ação a mais (decisão 25, 3.6, e risco de ciclos). Versões que respeitam isso:

- **A próxima ação do aliado custa metade do recurso** (útil para a Reerguer de Odette, 30 de Fé).
- **Os efeitos que o aliado aplicar na próxima vez duram uma vez a mais** (o atordoar de Morel não; o Escudo de Luz de
  Odette sim).
- **O relógio de uma preparação do aliado desce 1.**

#### Uma ilusão que aparece como outro card

Proposta: **o Duplo**.

- **O que é:** uma carta translúcida, de borda tracejada, ao lado do original (você ou um aliado). Não age, não tem
  vez na ordem (não gera ação). Tem uma regra: **o primeiro golpe dirigido ao original que não seja em área vai no
  Duplo**, que se desfaz. O golpe é perdido inteiro, seja um ataque comum ou um golpe preparado de ×2,2.
- **O que muda nas decisões:** com a intenção visível, você sabe que o golpe forte vai na Odette na vez do troll; pôr o
  Duplo nela anula aquele golpe por completo, ao contrário de uma barreira, que absorve um valor fixo. Contra três
  lobos mordendo, o Duplo some na primeira mordida: pouco valor. Ele é a resposta à ameaça **grande e única**.
- **Interação com inimigos:** golpes em área desfazem o Duplo sem efeito nenhum; inimigos que **percebem** (espectros,
  conjuradores; um traço declarado e mostrado na ficha) ignoram o Duplo. Quem bateu no Duplo fica **exposto** por uma
  vez (recebe +x% de dano), porque se comprometeu com o vazio: dá à comitiva um motivo para agir logo depois.
- **Versões (seção 5):** o Duplo Imitador repete, na vez do original, a última habilidade dele com dano baixo, sem
  efeitos (risco de ação extra: só a parte do dano, uma vez); a Troca, que põe o original "oculto" e o Duplo no lugar
  por uma rodada (os golpes dirigidos a ele vão no Duplo, mais de um).
- **Interface:** a carta do Duplo entra com um tremor; a seta da intenção do inimigo se curva para ele quando ele vai
  receber; ao se desfazer, a carta se parte em fragmentos. A ficha diz "Desfaz-se no primeiro golpe dirigido a X. Não
  pega golpes em área."
- **Motor:** um combatente sem vez (fora da ordem), alvo válido de redirecionamento (`redirecionar` já existe para o
  Proteger), um traço `percebe`, o estado `exposto`.
- **Abuso:** um Duplo a cada vez em quem vai levar o golpe forte trava o chefe. Limites: custo alto, um Duplo por vez em
  campo, e o chefe com a habilidade de golpe preparado pode ter "percebe" na fase final.

**Versão sem magia:** o **Engodo** da Sombra (a capa numa estaca, o chapéu na moita). A mesma regra, com o alvo
limitado a você. A fantasia é outra; a decisão é a mesma, e isso é aceitável quando a classe tem outras ferramentas
distintas (seção 7).

#### Alterar a ordem dos turnos por um ou dois turnos

**Conflita com a decisão 25, 3.5** ("aceleradores, atrasos ou trocas de posição na ordem não são uma extensão
aprovada"). Se o Jean quiser reabrir, a versão mínima:

- **Troca de Vez:** dois combatentes do seu lado trocam de posição **só nesta rodada**; na seguinte, a ordem volta. Não
  cria ações, não tira ações. Vale para pôr Odette antes do inimigo que vai bater no ferido; não vale quando os dois já
  passaram.
- **Exige:** a placa da rodada mostrar a troca (as duas cartas com uma seta curva e "só nesta rodada"); o motor
  reordenar a rodada corrente sem tocar na ordem base.
- **Risco:** confusão sobre "de quem é a vez agora" e combinações com Adiar que somem com a vez de alguém.

**Recomendação:** manter a ordem fixa e entregar a fantasia pelo **relógio das preparações** (Retardar, Precipitar,
Pressa) e pela Âncora. A ordem continua uma referência estável para tudo, e o cronômante continua sendo quem decide a
hora.

### 4.4 Outras possibilidades, com e sem magia

**Reação armada (a Tocaia).** *Sem magia; Arqueiro.*
- **Faz:** gasta a vez para apontar um inimigo e escolher um gatilho de uma lista fechada: "quando ele começar a
  preparar", "quando ele atacar um aliado", "quando ele usar uma habilidade de apoio" (cura, uivo, grito). Se o gatilho
  acontecer antes da sua próxima vez, o tiro sai na hora, antes da ação do inimigo; se o gatilho for a preparação, o
  tiro também quebra uma trava ou atordoa (num comum).
- **Vale:** quando a intenção mostra o que vem (atirar no xamã antes da cura); contra quem vai preparar na próxima vez.
- **Não vale:** quando ninguém vai disparar o gatilho (você perdeu a vez); quando a ameaça é ataque comum disperso.
- **Sacrifica:** a vez presente por uma vez condicional.
- **Comitiva:** pareia com Morel (ele atordoa o que a Tocaia não pegou).
- **Interface:** na sua carta, o ícone de arco tenso e um fio fino até a carta do alvo, com o gatilho escrito em uma
  palavra ("ao preparar"); quando dispara, a faixa "Tocaia!" sobre a sua carta, antes da faixa do inimigo.
- **Motor:** um ponto de interrupção antes de `agir_inimigo` executar (e antes de começar a preparação), uma lista de
  reações armadas por rodada, prioridade entre várias, profundidade 1 (a reação não dispara outra reação).
- **Abuso:** armar sempre e nunca agir "de verdade": a reação precisa ser mais fraca que o tiro comum fora do gatilho
  certo, e uma reação por personagem por rodada.

**Relógio: Retardar.** *Gelo ou Tempo.* Em vez de tirar a vez, o relógio da preparação do alvo sobe 1. O inimigo age
normalmente (ataque comum) e o golpe forte espera. Contra chefes, é o controle que nunca deixa o chefe sem agir. Quando
não vale: num alvo sem preparação, não faz nada (a ficha diz isso; a carta fica apagada na escolha de alvo).

**Ímpeto Temerário.** *Sem magia; Berserker.* Agir de novo agora e **perder a próxima vez**. Não gera ação: empresta
uma. Vale para matar antes de uma preparação sair, ou para fechar uma luta. Não vale quando o inimigo vai golpear você
na rodada em que você estará sem vez. A carta mostra "sem vez na próxima rodada" e a placa da ordem risca a sua
próxima posição. Risco: com a Âncora ou com o Duplo cobrindo a vez perdida, vira duas ações por rodada; uma regra
geral resolve (seção 5.6).

**Efeito adiado (o Prenúncio).** *Tempo ou Sombra.* Um efeito marcado que acontece no começo da próxima vez do alvo,
mais forte que o imediato. Vale contra quem não vai morrer antes; não vale se outro aliado o matar antes (desperdício)
ou se ele se limpar. Junta com Retardar (o golpe forte do inimigo espera e o Prenúncio cai antes) e com o Duplo.

**Sustentação.** *Regra para controles fortes, de qualquer escola.* Um controle contínuo (prender, silenciar,
acorrentar) dura enquanto o conjurador o sustenta: um sustentado por personagem; ele se rompe se o conjurador sofrer um
golpe acima de x% da vida ou perder a vez. A comitiva passa a proteger o conjurador. É a concentração do D&D aplicada
ao nosso controle.

**Sacrifício e conversão (Necromante).** O **Pagar com Ossos**: desfaz um servo para absorver o próximo golpe dirigido
a você ou a um aliado (o golpe inteiro, como o Duplo, mas o servo precisava existir e custou uma ação antes). A
**Colheita Rubra**: os sangramentos e venenos de um inimigo viram vida para o servo, encerrando o dano por turno. O
necromante passa a decidir *quando gastar* o que construiu.

**Juramento.** *Sagrado; Paladino.* Jurar proteger um aliado até a sua próxima vez: o primeiro golpe dirigido a ele vai
em você **e** você revida com dano sagrado; se nenhum golpe vier, o próximo golpe sagrado seu rende mais. Diferente do
Proteger (que só desvia), cria a pergunta "o inimigo vai mesmo bater nela?" e recompensa os dois resultados com coisas
diferentes.

**Conversão de estados.** *Arcano.* Trocar um estado por outro de mesmo tipo: o Fortalecido do inimigo (o uivo) vira
Enfraquecido; a Queimadura de um alvo resistente vira Fragilizado. Vale contra o bando que se fortaleceu; não vale no
começo da luta.

**Cópia.** *Arcano ou Sombra.* Copiar o último estado positivo que um inimigo ganhou (roubar o uivo). Cópia de
habilidade inimiga completa fica fora do núcleo: a variedade de habilidades inimigas é pequena, e copiar dano não muda
decisão.

### 4.5 O que não recomendo

- **Ações extras por acerto ou por fraqueza** (Megami Tensei): gera a sequência ideal e ciclos.
- **Medidor de grupo "no ponto ideal"** (Chained Echoes): vira a escolha automática.
- **Voltar a luta inteira:** salvamento escondido.
- **Marcas que só preparam dano** (a Marca recusada): pedágio.
- **Imunidade de chefe a todo controle:** remove as escolhas justamente onde elas importam mais.

---

## 5. Talentos e habilidades juntos

### 5.1 O princípio

Uma habilidade de base é **funcional e simples**. Um caminho de modificação a transforma numa **ferramenta diferente**,
com uma perda declarada. A build é feita das ferramentas escolhidas e das relações entre elas, não da soma de bônus.

### 5.2 Exemplos completos

Números de exemplo, sem medida.

#### Investida (Guerreiro, comum)

**Base:** 120% do Ataque; se acertar, 45% de chance de atordoar (o alvo perde a próxima vez).

| Caminho | O que faz | Decisão que cria | O que deixa de ser possível |
|---|---|---|---|
| **Contratempo** | 110%; não atordoa; o relógio da preparação do alvo sobe 1 (num chefe também) | "Atraso o golpe forte agora ou bato no outro?" Previsível, funciona em chefe | Tirar a vez de quem não prepara |
| **Arremetida de Escudo** | 80%; atordoa sempre se o alvo estiver preparando; você fica em guarda até a sua próxima vez | Interromper com certeza, mas só no momento certo; protege você | Usar como golpe de dano; atordoar no resto da luta |
| **Corrida de Guarda** | 100%; você passa a proteger o aliado que o alvo mirava (pela intenção) | Uma ação que bate e protege, se a intenção apontar para um aliado | Atordoar; proteger quem você escolher (é quem o inimigo escolheu) |

O Contratempo pertence a uma build de relógio; a Arremetida, a uma de interrupção; a Corrida, a uma de proteção. Os
três jogam a mesma luta de jeitos diferentes (seção 7).

#### Lança de Gelo (Mago, comum)

**Base:** 130% do Poder em gelo; 35% de congelar.

| Caminho | O que faz | Decisão | Perde |
|---|---|---|---|
| **Prisão de Gelo** (existe) | 70%, não se esquiva, congela sempre (chefes resistem metade) | Controle certo contra quem prepara | Dano |
| **Geada** | 100%; não congela; o relógio da preparação do alvo sobe 1 e ele fica Lento (os efeitos que aplica duram 1 a menos) | Controle que não falha e funciona em chefe | Tirar a vez |
| **Estilhaço** | 90%; contra congelado, consome o gelo e causa +150% | Um ciclo de dois passos com Nevasca ou Prisão (congelar e quebrar) | Congelar com a própria Lança |

#### Tiro Certeiro (Arqueiro, comum)

**Base:** 170% do Ataque, +30% de crítico.

| Caminho | O que faz | Decisão | Perde |
|---|---|---|---|
| **Tocaia** | Vira reação armada (seção 4.4): 150% quando o gatilho acontece; sem gatilho, nada | Ler a intenção e apostar | O tiro garantido |
| **Tiro de Desarme** | 100%; quebra uma trava de qualquer tipo | O Arqueiro como quebrador de travas | Dano |
| **Tiro que Atravessa** | 140%; se o alvo estiver protegido por outro inimigo (guarda-costas, escudo), acerta o protegido e o protetor | Uma resposta a inimigos que se protegem | Crítico extra |

#### Erguer Servo (Necromante, avançada)

**Base:** um esqueleto que provoca os inimigos por 2 vezes dele.

| Caminho | O que faz | Decisão | Perde |
|---|---|---|---|
| **Servo Escudo** | Sem provocar; pode ser desfeito na sua vez para absorver o próximo golpe dirigido a alguém | Guardar o servo para a hora certa | Desviar os golpes pequenos |
| **Servo Pira** | Ao cair, explode e espalha os males que o necromante aplicou no alvo que o derrubou | Mandar o servo para morrer no lugar certo | A proteção |
| **Servo da Cova** | Ergue um morto da luta no lugar de um esqueleto (o primeiro que cair), com uma habilidade dele | Matar primeiro quem vale a pena erguer | Escolher a hora (depende de alguém cair) |

#### Combustão (Piromante, avançada)

**Base:** consome a Queimadura do alvo e causa o que ainda causaria, com bônus.

| Caminho | O que faz | Decisão | Perde |
|---|---|---|---|
| **Pavio Curto** | Não detona agora: a detonação acontece no começo da próxima vez do alvo, com +50% (efeito adiado) | Tempo; e o risco de o alvo se limpar ou morrer antes | O dano imediato |
| **Contágio** | Detona e passa metade das camadas para outro inimigo | Manter o fogo vivo no grupo | Parte do dano |
| **Brasa no Escudo** | Detona e converte o dano em barreira em você | O Piromante que se defende com o que acendeu | O dano no alvo pela metade |

### 5.3 Estruturas comparadas

| Estrutura | Como funciona | Vantagens | Problemas |
|---|---|---|---|
| **A. Árvore ampliada** (o que temos) | Ramos por classe e especialização, camadas por nível, ranks | Já existe, a tela já existe, fácil de adicionar | Tende a números; a ordem de compra é óbvia; transformações espalhadas |
| **B. Versões por habilidade** (Diablo IV, E6) | Cada habilidade tem 2 ou 3 versões exclusivas; escolhe-se uma em lugar seguro | O modificador mora onde se usa; a perda é visível; identidade da classe preservada | Muito conteúdo (cada versão é uma ficha); a tela precisa comparar bem |
| **C. Selos encaixáveis** (Path of Exile) | Poucos modificadores universais que se põem numa habilidade do kit | Combinações livres; pouco conteúdo para muitas combinações | Perde a identidade (todo mundo com o mesmo selo); combinações quebradas; leitura difícil |
| **D. Disciplinas** (Guild Wars) | Escolas mecânicas que atravessam classes; a classe dá acesso a algumas | Fantasias novas sem classes novas | Grande; dilui as classes; precisa de muito catálogo |
| **E. Especialização com princípios** (Darkest Dungeon 2) | A especialização dá uma ou duas regras que mudam relações ("seus atrasos também quebram uma trava") | Poucas regras com muito efeito; forte identidade | Risco de uma regra obrigatória; pouca escolha se for só uma |

**Recomendação: B como núcleo, com uma camada pequena de E.** Cada habilidade importante ganha versões; cada
especialização ganha um ou dois **princípios** (regras de relação); os bônus numéricos saem da árvore para os atributos
e o equipamento. **C** pode entrar pelo equipamento (um anel que dá a uma habilidade a entrega "em reação"), com
limite de um por item, sem virar uma árvore. **D** serve como lente para organizar o catálogo (a escola do relógio, a
do sangue), não como sistema.

A hipótese do Jean ("até três melhorias numa sequência por habilidade", 25, 3.2) cabe assim: **uma casa de base (a
habilidade funciona), uma bifurcação (escolher a versão), um refinamento da versão escolhida.** Três casas, com a
escolha no meio.

### 5.4 As tensões, uma a uma

**Talentos interessantes × praticamente obrigatórios.** Um talento é obrigatório quando melhora o que você faria de
qualquer jeito, sem custo (Golpe Brutal, Eficiência). Remédio: versões **trocam** uma coisa por outra; os bônus puros
saem da árvore. Teste: para cada versão, descrever a luta em que a base é melhor. Se não existe, a versão é obrigatória.

**Liberdade de combinação × identidade da classe.** Versões ficam presas à habilidade (identidade preservada); os
princípios ficam presos à especialização. A liberdade vem de qual versão de cada uma e do kit. Selos universais (C)
são o que mais dilui; por isso ficam no equipamento, raros.

**Sinergia entre personagens × dependência de uma comitiva.** As relações devem passar por **estados e situações
compartilhados**, não por nomes: "contra atordoado", "contra quem prepara", "em quem está protegido", "contra
exposto". Assim, o Golpe Oportuno de Morel funciona com qualquer fonte de atordoar, e o herói que não tem Morel
encontra a mesma situação por outra fonte. Combos com nome próprio (só A com B) ficam para a ultimate dupla, se um dia
entrar.

**Especialização × adaptação.** O kit é a adaptação (troca entre lutas em lugar seguro); as versões são a
especialização (trocadas também em lugar seguro, sem custo, como a Prisão de Gelo hoje). O que custa caro mudar são os
princípios e os pontos de atributo. Encontros variados (seção 8) dão motivo para adaptar.

**Escolhas acessíveis × combinações avançadas.** A base de cada habilidade é sempre boa sozinha. As versões aparecem
uma de cada vez, a partir do nível em que a habilidade já foi usada algumas vezes, com a comparação lado a lado
(como a Prisão de Gelo faz). Os princípios chegam com a especialização.

**Experimentar e refazer.** Versões e kit: grátis em lugar seguro. Princípios: trocáveis no templo ou com um mestre, a
um custo (ouro, um dia). Pontos de atributo: a redistribuição já foi discutida para a comitiva; o herói pode ter o
mesmo mecanismo. **Não obrigar uma campanha nova para corrigir uma escolha mal explicada** ([03](03-CLASSES-E-BUILDS.md)).

**Ciclos infinitos, controle permanente, geração ilimitada de ações.** Regras gerais na 5.6.

### 5.5 Preservar a fantasia poderosa sem eliminar as decisões

Uma build forte deve **resolver muito bem um tipo de problema** e **pagar por isso noutro**. O Relojoeiro trava golpes
preparados como ninguém, e sofre contra enxames de golpes comuns. O Pavio derrete grupos acesos, e precisa de tempo e
sofre contra quem se limpa ou resiste. A fantasia está em ver o seu tipo de problema chegar e resolvê-lo com elegância;
a decisão continua porque nenhum encontro bem desenhado é só do seu tipo.

Sinais de que uma build eliminou as decisões: a mesma sequência em toda luta; a ultimate sempre na abertura; um
inimigo que nunca age; uma habilidade usada mais de metade das vezes. São as medidas do protótipo (seção 10).

### 5.6 Regras gerais contra abuso

1. **Profundidade 1 nos gatilhos:** um efeito disparado por gatilho não dispara outros gatilhos (o Coração Ardente já
   segue isso com `explodindo`).
2. **No máximo uma vez extra por combatente por rodada**, venha de onde vier (Ímpeto Temerário, Pressa, reação).
3. **Uma reação armada por personagem por rodada;** reações não reagem a reações.
4. **Controle forte é sustentado** (um por personagem, rompe com golpe forte ou perda de vez).
5. **Perder a vez deixa Firme** (já existe) e **chefes não perdem a vez:** ficam abalados.
6. **Âncora, Duplo e sacrifícios: um em campo de cada vez** por personagem.
7. **Efeitos sobre o relógio têm limite:** uma preparação não pode ser adiada mais de 2 vezes; depois disso ela fica
   **inadiável** (aparece na carta).

---

## 6. Estruturas para o sistema completo

### 6.1 Três alternativas coerentes

**Alternativa 1: o mínimo (manter e refinar).** Kit como está; mais versões em habilidades escolhidas; árvore atual
podada (fora os bônus). Intenção só para preparações (como hoje, com contador). Barata; resolve parte da redundância;
não muda a leitura do inimigo comum.

**Alternativa 2: ameaça legível e versões (recomendada).** Intenção para todos os inimigos (tipo e alvo; números só nas
preparações), relógio e travas nos golpes fortes, chefes abalados em vez de atordoados. Catálogo reorganizado por
verbo, com as redundâncias fundidas. Cada habilidade importante com 2 versões e um refinamento. Um ou dois princípios
por especialização. Bônus numéricos nos atributos e no equipamento. Custo: motor do inimigo, catálogo, Grimório novo.

**Alternativa 3: escolas abertas.** As escolas (Relógio, Sangue, Guarda, Caça, Fogo, Gelo, Sombra, Luz) atravessam as
classes; a classe dá acesso a três; a especialização, a uma quarta. Selos universais. Máxima liberdade e fantasias
novas sem classes novas (o cronômante seria uma escola). Custo alto e diluição das classes; recomendo guardar como
direção de longo prazo.

### 6.2 A recomendação, elemento por elemento

| Elemento | Proposta | Núcleo ou depois |
|---|---|---|
| **Aprendizado** | Por nível, como hoje, e por **achado na campanha** (um mestre, um livro, um evento), para a etapa 9 ter recompensas de build | Núcleo (por nível); achados na 9 |
| **Preparo no Grimório** | O kit, trocado em lugar seguro; a escolha das versões na mesma página, lado a lado | Núcleo |
| **Kit** | 5 espaços + 1 espaço de ultimate separado. Os pontos por tier saem (o problema medido no 26: a ultimate come o orçamento). O tier passa a dizer a complexidade, não a potência | Decisão do Jean |
| **Talentos** | Versões por habilidade (escolha exclusiva + refinamento); princípios da especialização; a árvore guarda só o que muda regra | Núcleo: as versões de 4 a 6 habilidades por classe; o resto depois |
| **Recursos** | Manter cheio a cada luta (simples; já decidido como continuidade). A economia dentro da luta vem do custo das habilidades de relógio e alvo, mais caras que dano, e do ataque básico útil | Núcleo |
| **Tiers** | Comum: simples e confiável, sempre útil. Avançada: interage com intenção, relógio ou estados. Ultimate: uma virada que quebra uma regra uma vez (Hora Parada, Hora Revivida). A comum não é a avançada mais fraca: é a versão barata e certa de outra decisão | Núcleo |
| **Ultimate** | Chega com a especialização (nível 4 hoje), não no 6: senão o capítulo não a mostra. Uma por especialização no começo; outras pela campanha | Decisão do Jean |
| **Controles** | Firme depois de perder a vez (existe); chefes abalados; travas; sustentação para controles longos; Tenacidade como chance para os comuns | Núcleo: abalado e travas |
| **Tipos de magia** | Cada tipo com uma identidade mecânica além da fraqueza (tabela abaixo) | Núcleo: fogo, gelo, físico, sagrado; o resto depois |
| **Equipamento** | Peças que mudam regras de uma habilidade ou de um comando (o Broquel do Vigia já faz isso com o Revide); raros e únicos podem liberar uma versão. Bônus numéricos que saíram da árvore vão para cá e para os atributos | Depois do núcleo, junto da E7 |
| **Comitiva** | Cada companheiro como um verbo do grupo: Morel interrompe e protege; Odette sustenta e levanta; Yara enfraquece e dissipa. Versões para eles depois (25, 3.4: um conjunto menor). Relações por estado, não por nome | Núcleo: tirar as duplicatas (Proteger, Runa); versões depois |

**Identidades mecânicas por tipo** (proposta):

| Tipo | Identidade | Exemplo |
|---|---|---|
| Físico (força) | Quebrar: defesa, travas, guarda | Quebra-Guarda, Golpe que Racha |
| Físico (precisão) | Momento: crítico, reação, executar | Tocaia, Execução |
| Fogo | Acumular e detonar, com espera | Brasa → Combustão |
| Gelo | Mexer no relógio: retardar, prender | Geada, Prisão |
| Sagrado | Compromisso: juramentos, proteger e punir | Juramento |
| Sombra | Trocar vida, recurso e estados | Drenar, Pagar com Ossos |
| Arcano | Mexer nas regras: dissipar, converter, copiar | Conversão |
| Sangue | Vida como recurso; agir agora e pagar depois | Fúria Cega, Ímpeto Temerário |
| Tempo (escola nova) | O relógio e o estado guardado | Retardar, Precipitar, Âncora |

### 6.3 Concessões da recomendação

- **Muda a ordem dos sorteios** de toda luta (a intenção é decidida antes): o gabarito muda, e as medidas de
  equilíbrio precisam ser refeitas.
- **Mais leitura por turno:** cada carta inimiga com um ícone. Precisa caber a 1280×720 (seção 8).
- **Conteúdo:** cada versão é uma ficha, uma descrição e, depois, um ícone.
- **O inimigo comum fica menos surpreendente.** Compensa-se com intenções que mudam por gatilhos declarados (o
  mercenário que muda de alvo quando ferido) e com encontros mistos.
- **A ordem fixa limita a fantasia temporal** ao relógio e ao estado guardado.

### 6.4 Uma estrutura mais simples resolveria?

Parcialmente. Só a Alternativa 1 com a intenção das preparações já dá função às habilidades de interromper e proteger
e funde as redundâncias. **O que ela não resolve** é a decisão nos encontros comuns (os inimigos que não preparam
continuam sorteando) e a variedade entre builds da mesma classe. Se o protótipo mostrar que a intenção de todos pesa
demais na leitura, a Alternativa 1 é o recuo natural.

---

## 7. Builds funcionando (simulação de design)

**Números inventados para a narração; nada medido.** Os encontros usam inimigos que existem, com a ameaça legível da
seção 4.2 (intenção, relógio e travas inventados para eles).

### 7.1 As builds

Formato: habilidades do kit (versão escolhida), princípio, condição principal, escolhas na luta, fraquezas, comitiva.

**G1 — Guerreiro Baluarte** (Paladino)
- **Kit:** Proteger, Investida (Corrida de Guarda), Erguer Escudo (versão que cobre o aliado protegido), Golpe
  Sagrado, Juramento; ultimate: Julgamento.
- **Princípio:** "quem você protege não pode ser atordoado".
- **Condição:** ser o alvo. A intenção diz quem vai apanhar; ele decide quem cobrir.
- **Escolhas:** cobrir quem vai levar o golpe forte, ou bater; o Juramento é aposta (vai bater nela ou não?).
- **Fraquezas:** golpes em área (proteger não cobre área); inimigos que se curam (o dano é baixo).
- **Comitiva:** Yara livre para amaldiçoar; Odette economiza a cura.

**G2 — Guerreiro Quebrador** (Berserker)
- **Kit:** Golpe Pesado (Golpe que Racha: quebra 2 travas físicas, 120%), Investida (Contratempo), Quebra-Guarda,
  Grito de Guerra, Ímpeto Temerário; ultimate: Fúria Cega.
- **Princípio:** "cada trava que você quebra dá +10% de dano até o fim da luta (até 3)".
- **Condição:** inimigos que preparam.
- **Escolhas:** atrasar ou quebrar; gastar o Ímpeto para matar antes do relógio.
- **Fraquezas:** travas mágicas (gelo, sagrado) que ele não quebra; enxames sem preparação.
- **Comitiva:** Morel interrompe o que ele não alcança; Yara quebra a trava mágica (pela maldição).

**M1 — Mago Pavio** (Piromante)
- **Kit:** Brasa, Chuva de Brasas, Combustão (Pavio Curto), Barreira, Lança de Gelo (Estilhaço); ultimate: Conflagração.
- **Princípio:** "a detonação adiada não pode ser limpa".
- **Condição:** tempo para acender.
- **Escolhas:** quando acender, quando detonar, se adiar.
- **Fraquezas:** resistência ao fogo (o Cão infernal); lutas curtas; alvos que morrem antes da detonação.
- **Comitiva:** Morel segura o golpe forte enquanto o fogo cresce.

**M2 — Cronômante Relojoeiro** (proposta de especialização ou escola do Mago)
- **Kit:** Lança de Gelo (Geada), Retardar, Precipitar, Pressa, Barreira; ultimate: **Hora Parada** (até a sua próxima
  vez, os relógios de todos os inimigos não descem e os seus aliados não perdem a vez; uma vez por luta).
- **Princípio:** "atrasar uma preparação quebra também uma trava".
- **Condição:** inimigos que preparam e um aliado que aguenta.
- **Escolhas:** atrasar até o momento em que as defesas estão prontas, ou precipitar agora contra a defesa pronta.
- **Fraquezas:** quase nenhum dano próprio; inimigos sem preparação; golpes inadiáveis (depois de 2 atrasos).
- **Comitiva:** depende de alguém para causar dano (Morel, Yara); em compensação, deixa o grupo sem sustos.

**M3 — Cronômante Eco**
- **Kit:** Âncora, Prenúncio, Bola de Fogo, Duplo, Meditar; ultimate: **Hora Revivida** (um aliado que caiu nesta luta
  volta com a vida da última âncora posta nele; uma vez por luta).
- **Princípio:** "puxar a âncora de um aliado devolve também 10 de recurso a ele".
- **Condição:** saber onde o dano vai cair (intenção) e aceitar ações sem efeito imediato.
- **Escolhas:** ancorar quem; puxar agora ou esperar a próxima ameaça; o Duplo no golpe forte.
- **Fraquezas:** dano constante e espalhado; inimigos que percebem (o Duplo); muito tempo para valer.
- **Comitiva:** substitui parte do trabalho de Odette (seguro em vez de cura).

**A1 — Arqueiro de Tocaia** (Patrulheiro; sem magia)
- **Kit:** Tiro Certeiro (Tocaia), Tiro Imobilizador (versão "Tiro no Gatilho": sempre interrompe, só em quem prepara),
  Tiro Duplo, Passo Ágil, Ordem da Fera; ultimate: Fúria da Natureza.
- **Princípio:** "quando a Tocaia dispara, a fera ataca o mesmo alvo".
- **Condição:** inimigos de apoio e de preparação.
- **Escolhas:** armar ou atirar; qual gatilho.
- **Fraquezas:** intenções que mudam; inimigos que só atacam comum.
- **Comitiva:** quem tem Proteger cobre o turno em que ele não atirou.

**A2 — Sombra do Engodo** (sem magia)
- **Kit:** Engodo, Desaparecer, Flecha Envenenada, Mirar, Tiro Certeiro; ultimate: Execução.
- **Princípio:** "o inimigo que bate no Engodo fica exposto por 2 vezes, e a Execução conta exposto como abaixo de 35%".
- **Condição:** um golpe grande e único para enganar.
- **Escolhas:** pôr o Engodo antes do golpe certo; executar o exposto ou o ferido.
- **Fraquezas:** área; percebedores; enxames.
- **Comitiva:** ela abre, Morel e Yara aproveitam o exposto.

**N1 — Necromante Ossário**
- **Kit:** Erguer Servo (Servo Escudo), Drenar Vida, Pagar com Ossos, Colheita Rubra, Bola de Fogo; ultimate:
  Maldição.
- **Princípio:** "cada servo desfeito dá ao próximo servo +20% de vida".
- **Condição:** construir antes, gastar na hora.
- **Escolhas:** quando erguer, quando sacrificar.
- **Fraquezas:** abertura lenta; área destrói servos.
- **Comitiva:** pouca dependência; Odette fica livre.

### 7.2 Mesma classe, jogos diferentes; fantasias diferentes, jogos diferentes

- **G1 e G2** são Guerreiros: um decide **quem apanha**, o outro decide **quando o golpe forte sai**. Contra o mesmo
  mercenário, o Baluarte cobre Odette e deixa o golpe sair; o Quebrador racha as travas e o golpe sai fraco.
- **M2 e A1** respondem a preparações, mas o Relojoeiro **adia** (o golpe vem depois, mais fraco) e a Tocaia **mata ou
  corta antes** (precisa adivinhar o gatilho).
- **M3 e A2** usam ilusão, mas o Eco aposta no **seguro** (a Âncora) e a Sombra no **contra-ataque** (exposto).
- **M1 e N1** constroem antes de colher, mas o fogo **cresce sozinho** (o tempo ajuda) e os ossos **custam ações** (o
  tempo atrapalha).

### 7.3 Os encontros

- **E1 — O mercenário e dois bandidos** (Bosque, nível 3–4). O mercenário prepara o Golpe Esmagador (relógio 2, travas
  físico e físico), grita para fortalecer os bandidos; os bandidos roubam ouro e dão golpes sujos.
- **E2 — O ent jovem e duas aranhas** (Bosque à noite, nível 4). O ent prepara (relógio 1, trava gelo) e regenera; as
  aranhas lançam teia (prende uma vez) e envenenam.
- **E3 — A Bruxa Afogada, fase 2** (Charco, guardiã). Maldição, Esfera Sombria, invoca afogados; na fase 2 prepara a
  **Canção de Ninar** (área: enfraquece o grupo e atordoa quem estiver abaixo de 30%; relógio 2, travas sagrado e
  gelo; é o que o [21](21-DIAGNOSTICO-ATAQUES-EM-AREA.md) sugere para ela).

### 7.4 Trechos de combate

**E1 com o Baluarte (G1), Odette e Morel.**
Rodada 1: a intenção do mercenário mostra "Grito" (apoio); a dos bandidos, golpe em Odette e golpe em você. Você põe o
Juramento em Odette. O bandido B bate nela: o golpe vai em você e você revida com luz. Rodada 2: o mercenário começa a
preparar o Golpe Esmagador, relógio 2, seta em Odette. Você usa Proteger nela e Erguer Escudo (a versão que cobre o
protegido). **O plano falha:** o bandido A rouba 14 de ouro e foge para a moita; a intenção do mercenário muda para
você, porque Odette está protegida (o gatilho declarado "alvo protegido": ele escolhe outro). Você está em guarda, então
o golpe vem em cheio no escudo: 31 em vez de 70. Morel atordoa o bandido B. O Baluarte não matou nada em três
rodadas, mas ninguém caiu.

**E1 com o Quebrador (G2), Odette e Morel.**
Rodada 1: você ignora os bandidos e usa o Golpe que Racha no mercenário, antes mesmo de ele preparar (as travas só
aparecem com a preparação; o golpe causa dano, e o bônus do princípio não vem). **O plano falha:** o mercenário
grita, e os bandidos fortalecidos derrubam Morel pela metade. Rodada 2: o mercenário prepara (relógio 2, duas travas
físicas). Agora sim: Golpe que Racha quebra as duas, +20% para você. O golpe vai sair "sem travas", fraco. Você gasta o
Ímpeto Temerário para matar o bandido mais ferido antes de o relógio zerar e fica sem a vez da rodada 3. O golpe fraco
sai em Odette (12). Na rodada 4, você volta com +20% e o mercenário cai em duas.

**E2 com o Relojoeiro (M2), Odette e Morel.**
Rodada 1: o ent prepara (relógio 1, trava de gelo, seta em Morel). Você usa Geada nele: relógio 2 e a trava de gelo
quebra (o princípio). **O plano falha:** a aranha A lança teia em você: preso, você perde a rodada 2. O relógio do ent
desce para 1; Morel, vendo a seta nele, defende. Rodada 3: você está Firme; o relógio está em 1 e o golpe sairia na
vez do ent, depois da próxima vez de Morel, quando o Defender dele já terá acabado. Você usa Precipitar: o golpe sai
agora, em Morel ainda defendendo (−40%), sem a trava de gelo (sem a parte congelante). 19 de dano em vez de 50. O ent ficou sem preparação; as aranhas continuam; o Relojoeiro não tem dano para
elas e a luta fica longa: é a fraqueza da build.

**E2 com o Pavio (M1), Odette e Yara.**
Rodada 1: Chuva de Brasas acende os três. Rodada 2: o ent prepara (seta em Odette); você precisa decidir entre
detonar (Pavio Curto no ent: só sai na próxima vez dele, depois do golpe) e se proteger. **A combinação normalmente boa
é abandonada:** detonar no ent agora não impede o golpe. Você usa a Lança de Gelo (Estilhaço não serve: ninguém está
congelado) com 35% de congelar e erra o congelamento. Odette defende. O golpe sai (34). Rodada 3: Pavio Curto na
aranha mais acesa; ela morre antes da detonação, morta por Yara: **o fogo se perde**. Rodada 4: Conflagração no ent e
na aranha que sobrou.

**E3 com o Eco (M3), Odette e Morel.**
Fase 2: a Bruxa prepara a Canção (relógio 2, travas sagrado e gelo). Odette está em 28%: a Canção vai atordoá-la.
Rodada 1: você ancora Odette (28%). Morel ataca. Odette se cura (61%). Rodada 2: você põe o Duplo em Odette. **O plano
falha:** a Canção é em área: o Duplo se desfaz sem efeito (a regra está na ficha, e você leu tarde). A Canção enfraquece
todos e não atordoa ninguém (Odette passou dos 30% pela cura). A Âncora ficou inútil (puxar a levaria de volta a 28%).
Rodada 3: os afogados invocados batem em Odette (22%). Você puxa a âncora: 28%, um pouco melhor. A build salvou pouco
porque a ameaça era a área.

**E3 com a Tocaia (A1), Odette e Yara.**
Fase 2: a Bruxa tem intenção "invocar". Você arma a Tocaia "ao usar habilidade de apoio" na Bruxa. Ela invoca; o tiro
sai antes, 150%, mas a invocação não é interrompida (a Tocaia só interrompe preparação). **Plano corrigido:** na
rodada seguinte, a Bruxa começa a preparar a Canção; você arma "ao preparar" na rodada 3 e erra a leitura: a Bruxa
amaldiçoa (não prepara de novo, a Canção já está em curso). A Tocaia não dispara. Na rodada 4 você usa o Tiro no
Gatilho (interrompe quem prepara, sempre): a Canção não sai, mas a Bruxa é chefe, então fica **abalada**: o relógio
volta a 2 e uma trava (sagrado) quebra. Yara amaldiçoa; a fera ataca. A luta segue com a Canção sempre ameaçando, mas
nunca saindo.

### 7.5 O que os trechos mostram

- **Decisões diferentes diante da mesma ameaça:** o golpe preparado do mercenário foi coberto (G1), quebrado (G2),
  adiado e precipitado (M2) e atirado antes (A1).
- **Planos que falham** por intenção que muda, área, teia, alvo que morre antes, gatilho errado.
- **Combinações abandonadas:** o Pavio não detona no ent; o Duplo não serve contra a Canção; o Relojoeiro não tem dano
  para as aranhas.
- **O chefe age sempre**, e mesmo assim cada build o molda.
- **O que ainda não sabemos:** se ler a intenção de cinco cartas por turno é agradável ou pesado; se a Tocaia frustra
  (perder a vez por erro de leitura); se o Relojoeiro é divertido sem dano. É o que o protótipo mede.

---

## 8. A campanha e a apresentação

### 8.1 Que inimigos e situações dão uso a essas possibilidades

| Arquétipo de inimigo | Dá motivo a | Existe hoje? |
|---|---|---|
| **O que prepara** (golpe forte com relógio e travas) | Interromper, atrasar, precipitar, quebrar, proteger, Duplo, Tocaia | Sim, só o Golpe Esmagador |
| **O que sustenta o bando** (cura, uivo, grito) | Matar primeiro, Tocaia de apoio, Âncora no inimigo, conversão de estados | Sim, sem aviso |
| **O que protege outro** (guarda-costas) | Tiro que Atravessa, quebrar guarda, escolher o alvo | Não |
| **O que invoca** | Área, matar o invocador, Servo da Cova | Sim |
| **O enxame** (muitos golpes pequenos) | Área, Baluarte; castiga Duplo e Relojoeiro | Sim (ratos, lobos, aranhas) |
| **O que reage** (espinhos, revide, fica mais forte ao apanhar) | Atacar com cuidado, proteger, usar estados em vez de golpes | Não |
| **O que percebe** (ignora ilusões, vê o oculto) | Força o ilusionista a ter plano B | Não |
| **O que se limpa** (remove males) | Pune o Pavio e as maldições; premia a detonação certa | Parcial (a cura não limpa) |
| **O que muda de intenção quando ferido ou protegido** | Torna a leitura um jogo (não uma tabela) | Não |
| **Chefe com fases e uma ameaça inadiável por fase** | Garante que nenhuma build trave tudo | Fases existem; inadiável não |

Uma habilidade sem pelo menos dois desses arquétipos no capítulo em que ela fica disponível não deve entrar: ela vai
parecer criativa no documento e nunca será usada.

### 8.2 O que a etapa 9 precisa considerar

- **Variedade de encontros:** cada região com pelo menos um encontro de cada um destes: enxame, preparação, apoio,
  guarda-costas, e um chefe com ameaça inadiável. Encontros mistos (um de cada) são os que pedem builds adaptadas.
- **Apresentação gradual dos sistemas:** a intenção desde a primeira luta (a despensa já é guiada); o relógio e as travas
  na primeira luta da capela (onde já há golpe preparado); as versões de habilidade no primeiro lugar seguro depois do
  nível 2; a especialização e a ultimate perto do fim do primeiro capítulo, para o jogador usá-las antes do chefe.
- **Acesso a habilidades e talentos:** pela subida de nível e por **achados com história** (o livro do padre na
  sacristia, a Vó Berta que ensina uma versão de proteção, o mercenário que ensina o Ímpeto). A reescrita da campanha
  é a hora de pôr esses pontos.
- **Oportunidades de experimentar:** trocas grátis em lugar seguro; um espaço de treino sem risco (o pátio do templo, o
  Morel desafiando para um treino na taverna, já que a queda de braço está lá); lutas opcionais que favorecem builds
  diferentes (o charco à noite para quem atrasa; o enxame do porão para quem tem área).
- **O nível no fim do capítulo:** se continuar perto do 4, os sistemas de build precisam aparecer até o 4; se o
  capítulo crescer, a etapa 9 decide onde cada um aparece.

### 8.3 A leitura visual

O jogador precisa distinguir, sem abrir descrições:

| Estado escolhido | Como aparece (proposta) | Animação |
|---|---|---|
| **Intenção** | Ícone pequeno sobre a carta (golpe, preparação, apoio, feitiço, invocação) e seta fina até o alvo | A seta se desenha quando a vez anterior termina |
| **Carregamento** (preparação) | Ícone de preparação com o número do relógio; as travas em quadradinhos coloridos pelo tipo, abaixo | O número desce com um tique; a trava quebra em lascas |
| **Inadiável** | O relógio com contorno vermelho | Um pulso único quando fica inadiável |
| **Efeito adiado** (Prenúncio, Pavio Curto) | Um selo sobre a carta do alvo com uma ampulheta e "na próxima vez" | O selo brilha no começo da vez do alvo e estoura |
| **Reação armada** (Tocaia) | Na carta de quem armou: o ícone do gatilho; um fio pontilhado até o alvo | O fio fica tenso quando o gatilho está para acontecer; a faixa "Tocaia!" corta a vez do inimigo |
| **Ilusão** (Duplo, Engodo) | Carta translúcida, borda tracejada, ao lado do original | Entra com tremor; parte-se em fragmentos |
| **Âncora** | Selo de âncora; sombra da barra de vida no valor guardado | Ao puxar, a barra rebobina |
| **Relógio alterado** (atrasar, precipitar) | O número do relógio com uma seta para cima (atrasado) ou o ícone de golpe pulando para "agora" | O número sobe com um tique para trás; o precipitado acelera a animação do golpe |
| **Sustentado** | Uma linha entre conjurador e alvo | A linha se rompe quando cai |
| **Abalado** (chefe) | O ícone de abalado e a trava que caiu | Tremor curto na carta |
| **Exposto** | Ícone de alvo aberto | — |
| **Vez perdida por empréstimo** (Ímpeto) | A próxima posição riscada na placa da rodada | — |

Regras de leitura:

- **Uma camada por informação:** a intenção sobre a carta; os estados embaixo (como hoje); o relógio junto da
  intenção; as relações (fios, setas) entre cartas.
- **Os números ficam na consulta,** salvo o relógio e o dano previsto das preparações.
- **Caber a 1280×720:** ícones de 16 px a ×2 sobre cartas de inimigo; cinco inimigos com intenção, sem sobrepor.
- **Movimento reduzido:** os mesmos estados, sem as animações de passagem; o relógio e as travas mudam por troca de
  ícone.
- **Ícones de habilidade e talento** (etapa 8) só depois do sistema escolhido, em lotes por escola.

Nada disso é asset final; é a lista do que a tela precisa dizer.

---

## 9. Decisões pendentes (para o Jean)

| # | Decisão | Opções | Recomendação |
|---|---|---|---|
| 1 | Quanto da intenção inimiga mostrar | (a) só as preparações, como hoje; (b) tipo e alvo de todas, números só nas preparações; (c) tudo com números | **(b)** |
| 2 | A ordem dos turnos | (a) fixa (25, 3.5); (b) Troca de Vez numa escola, só por uma rodada | **(a)**, com a fantasia temporal no relógio |
| 3 | A estrutura de talentos | (a) árvore ampliada; (b) versões por habilidade + princípios; (c) selos; (d) escolas abertas | **(b)**; selos só em itens |
| 4 | O kit | (a) 8 pontos e 5 espaços; (b) 5 espaços + ultimate separada; (c) 4 espaços + ultimate (mais apertado) | **(b)** |
| 5 | Quando chegam especialização e ultimate | (a) 4 e 6, como hoje; (b) as duas no 4; (c) depende do tamanho da 9 | **(b)** enquanto o capítulo termina perto do 4 |
| 6 | Chefes e controle | (a) resistência por sorteio, como hoje; (b) abalados (relógio e trava) | **(b)** |
| 7 | O cronômante | (a) especialização nova do Mago; (b) escola do Mago, acessível às duas especializações; (c) só conceito de teste | **(c)** no protótipo; decidir depois de jogar |
| 8 | As redundâncias atuais | Fundir (uma "chance de tirar a vez" por classe; um "alvo recebe mais"; defesas pessoais com função distinta) | Fundir na mesma entrega do núcleo |
| 9 | Talentos numéricos da árvore | (a) manter; (b) mover para atributos e equipamento | **(b)** |
| 10 | O Golpe Oportuno de Morel | (a) manter; (b) virar a relação por estado ("contra atordoado ou abalado") | **(b)** se ele virar obrigação |
| 11 | Reações armadas | (a) não ter; (b) só do Arqueiro; (c) uma por classe | **(b)** no protótipo |
| 12 | Etapa 7 (eventos da estrada) | Esperar a 9 como as cenas de acontecimento, ou seguir | Esperar, pela mesma lógica |

---

## 10. O protótipo proposto

**Um protótipo isolado em `ferramentas/prototipos/etapa8-builds/`**, no molde do `combate-atributos` (a mesma
arena, o jogo não muda). O objetivo é testar as três dúvidas que mais mudam a direção, não o sistema inteiro.

### 10.1 As dúvidas

1. **A intenção de todos os inimigos ajuda ou pesa?** (decisão 1)
2. **Builds da mesma classe jogam de fato diferente diante do mesmo encontro?** (a pergunta central)
3. **Controle em graus (relógio, travas, abalado) mantém o chefe ativo e as respostas interessantes?** (decisão 6)

### 10.2 O conteúdo, só o necessário

- **Inimigos:** os três encontros da seção 7.3, com intenção, relógio e travas; o chefe com uma ameaça inadiável na
  fase 2.
- **Builds:** G1 Baluarte e G2 Quebrador (mesma classe), M2 Relojoeiro (o cronômante, sem a Âncora e o Duplo, que
  ficam para uma segunda rodada se o relógio for aprovado) e A1 Tocaia (reação).
- **Versões:** Investida (Contratempo, Corrida de Guarda), Golpe Pesado (Golpe que Racha), Lança de Gelo (Geada),
  Tiro Certeiro (Tocaia), Tiro Imobilizador (Tiro no Gatilho). Os princípios das quatro builds.
- **Comitiva:** Odette e Morel, como no jogo.
- **Tela:** a intenção sobre as cartas, o relógio, as travas, o fio da Tocaia. Ícones provisórios (símbolos simples),
  sem arte final.
- **Registro:** cada luta grava as ações por rodada, a intenção mostrada e o que aconteceu (como o
  `resultados.json` do protótipo de combate).

### 10.3 O que observaríamos

| Observação | Como medir | Aprova se | Rejeita se |
|---|---|---|---|
| A leitura da intenção | O Jean diz, sem abrir a ficha, o que cada inimigo vai fazer; o tempo por decisão | Acerta quase sempre; decisões no tempo de hoje | Precisa abrir fichas; decisões muito mais lentas |
| Builds da mesma classe diferentes | As ações do G1 e do G2 no mesmo encontro, por rodada | Distribuições claramente diferentes; respostas diferentes à mesma ameaça | Mesma sequência com nomes diferentes |
| Mudança de plano | Rodadas em que a ação escolhida não é a "padrão" da build, por causa da intenção | Pelo menos uma por luta, nos encontros mistos | Nenhuma: a build executa a sequência ideal |
| O chefe age | Proporção de vezes do chefe em que ele agiu | A maior parte; a ameaça inadiável sai pelo menos uma vez | Chefe travado; ou o controle não serve para nada |
| A Tocaia | Disparos certos × perdidos; o relato do Jean | Errar a leitura parece justo | Frustração; ou nunca vale a pena |
| O Relojoeiro sem dano | Duração das lutas; o relato | Lutas um pouco mais longas, sem sustos | Lutas arrastadas; parece não fazer nada |
| Dominância | A habilidade mais usada de cada build | Abaixo de metade das ações | Uma habilidade domina |

Se a intenção pesar, o recuo é a decisão 1(a): a intenção só nas preparações (Alternativa 1). Se as builds da mesma
classe jogarem igual, o problema está nas versões e nos princípios, e não adianta seguir para o catálogo inteiro.

### 10.4 Fora do protótipo

A Âncora, o Duplo, o Engodo, os servos, o Pavio e o Grimório visual ficam para depois, se a direção for aprovada. Nada
entra no jogo nesta rodada.
