# Protótipo do combate e dos atributos

Quatro versões jogáveis, isoladas, para comparar. **Não é integração:** o jogo não carrega nada desta pasta (um teste
confere), as regras de produção, a campanha e a forja não mudaram, e os números são de teste, não catálogo nem
balanceamento.

- **v4 (26/10/2026, a atual):** um refinamento pequeno da v3 pela seção 3.9 do
  [25](../../../roadmapIDEIAS/25-ETAPA4-REFORCO-E-ENCANTAMENTO.md): sem a Marca, com o Golpe Oportuno do Morel e a
  Chuva de Brasas. `motor4/` e `tela4/`. Folha: `folha-v4.png`. O que testar: [ROTEIRO.md](ROTEIRO.md).
- **v3 (26/10/2026, preservada):** `motor3/` e `tela3/`, em `/v3/`. Descrita logo abaixo da v4.
- **v2** em `/v2/` e **v1** em `/v1/`, preservadas, descritas no fim.

## Abrir

Dê dois cliques em `demo.bat` (ou rode `python ferramentas/prototipos/combate-atributos/servidor.py` na raiz). A v4
abre em http://127.0.0.1:8781/ na tela **Preparar**; a v3, a v2 e a v1 ficam nos botões do topo. Os resultados vão
para uma pasta temporária nova a cada execução; os saves do jogo não são lidos nem tocados. Teclado: `P` Preparar,
`Enter` luta, número escolhe ação e alvo, `Esc` volta, `R` reinicia.

## v4 · o que mudou

| | Decisão (seção 3.9) | Valor provisório desta rodada |
|---|---|---|
| Ataques básicos | Não ler a frequência de básicos, sozinha, como falta de recurso ou de opções: o Jean termina com básicos quando a vitória está garantida | Nada rebalanceado por isso |
| Marca do Morel | Retirada da candidata; as versões anteriores continuam com ela; a produção não muda | — |
| No lugar da Marca | O Jean pediu uma habilidade nova para testar (a seção 3.9 dizia para não preencher a vaga por obrigação; registrado). Escolhi um golpe de efeito imediato, não uma preparação nem uma Marca renomeada | **Golpe Oportuno**: físico, arma + nível + Força × 1,2, 15 de Vigor, +60% em quem está atordoado ou preparando um golpe. Concorre com o Golpe no Joelho diante de uma preparação: desfazer ou aproveitar |
| Fogo em área | Uma habilidade comum de área: pouco dano, uma camada de Queimadura em cada inimigo, garantida (sem imunidades novas; a resistência ao fogo reduz o dano, não a aplicação), mais cara que a Brasa, disputando pontos e espaço | **Chuva de Brasas**: fogo, foco + nível + Intelecto × 0,35, tier 2 (2 pontos), 22 de Vigor (a Brasa custa 12), 1 pilha em cada inimigo |
| Papéis do fogo | Brasa concentrada e econômica; Chuva prepara o grupo; Combustão consome um alvo; Conflagração (ultimate, 1×/luta) consome todos | A Brasa, a Combustão e a Conflagração da v3 já cumpriam os papéis e ficaram iguais (conferido antes de mexer) |
| Kit sugerido da Chama | — | Brasa, Chuva de Brasas, Combustão, Proteger, Conflagração (10 pontos; a Lâmina Rúnica saiu do sugerido para caber) |

Também: a Tempestade Rúnica dizia "+100% em quem está marcado"; sem a Marca, ficou "atordoado ou queimando" (o mesmo
efeito para o que ainda existe). Os eventos de dano ganharam o valor e a fonte, para a comparação somar o dano direto e
o periódico sem contar nada duas vezes; nas janelas menores, a descrição das ações disponíveis foi para a dica (o
"previsto" continua no botão), porque oito ações não cabiam a 1280×720. Nada mais mudou: atributos, recurso, os outros
encontros e as outras habilidades são os da v3.

## v4 · a Queimadura conferida

**O que já estava certo (v3):** a Brasa soma uma pilha (até 3) e renova os 3 pingos; cada pingo tira pilhas × pingo
cru × (1 − resistência ao fogo do alvo); a Combustão e a Conflagração somam 200% do que ainda pingaria (cru) e apagam a
Queimadura, sem pingos depois; quem não queima leva só o golpe base da Conflagração.

**A comparação, jogada de verdade** (a mesma build Chama, INT 9, reserva 67; alvos parados nos testes t6, t7 e t8; os
companheiros só se defendem; as Queimaduras pingam até apagar ou ser consumidas; a tabela aparece em Preparar):

| Situação | Sequência de Jean | Ações | Custo | Direto | Periódico | Total |
|---|---|---|---|---|---|---|
| Um alvo (Soldado) | Brasa → Combustão | 2 | 32 | 40 | 4 | **44** |
| | Brasa → Brasa → Combustão | 3 | 44 | 71 | 13 | **84** |
| | Chuva → Combustão (área num alvo só) | 2 | 42 | 35 | 4 | 39 |
| | Chuva e esperar | 1 | 22 | 6 | 12 | 18 |
| Grupo (três lobos) | Chuva → Conflagração | 2 | 52 | 96 | 12 | **108** |
| | Brasa em cada um (3) → Conflagração | 4 | 66 | 84 | 24 | 108 |
| | Chuva e esperar | 1 | 22 | 15 | 36 | 51 |
| Resistência (dois Cães, fogo 60%) | Chuva → Conflagração | 2 | 52 | 27 | 4 | 31 |
| | Brasa → Combustão | 2 | 32 | 17 | 2 | 19 |

- **Num alvo só, a Brasa continua melhor** (44 por 32 de Vigor contra 39 por 42 com a Chuva).
- **No grupo, a Chuva faz em 2 ações o que três Brasas fazem em 4**, mais barato, e deixa a Conflagração pronta antes
  de expirar.
- **Contra resistência**, a Queimadura pega em todos, mas o fogo rende um terço: a preparação para o inimigo importa.
- A **reserva básica** da Chama (67) comporta Chuva + Conflagração (52) no primeiro turno e no seguinte. Num encontro
  normal (o 3, sem condição de teste) a sequência funciona: a Chuva no turno 1, a Conflagração no turno 2 consome as
  Queimaduras do Xamã, do Soldado e do Afogado (teste e roteiro do navegador).
- Conferido nos testes: a camada em cada inimigo mesmo com resistência; a previsão igual ao dano real (direto e por
  pingo); o teto de 3 pilhas; a expiração depois de 3 pingos; o consumo por alvo; nenhum pingo depois da explosão; o
  dano perdido pelos alvos igual à soma dos eventos (nada contado duas vezes); o inimigo morto antes da explosão sem
  erro e sem dano contado; a ultimate uma vez só; o clique duplo recusado.

## v4 · o que observei e o que não mudou

- **Os básicos do Jean** (arquivo `resultados(3).json`, seção 3.9): o Baluarte contra o Bruto usou quatro Avanços nas
  primeiras cinco rodadas e depois básicos enquanto o recurso subia; a Chama contra o Xamã usou cinco Brasas e duas
  Combustões, sem nenhum básico do protagonista. Com o relato dele (básicos por conveniência quando a vitória está
  garantida), isso não indica falta de recurso nem de opções. **Nada foi rebalanceado por isso**; recursos e duração das
  lutas são os da v3.
- O Golpe Oportuno cria uma escolha nova diante de uma preparação: o Joelho desfaz (e talvez atordoe); o Oportuno
  aproveita (+60%) e deixa a preparação sair. O atordoamento do próprio Joelho acaba no turno do inimigo, antes da
  próxima vez de Morel: na prática o bônus vem das preparações (ou de um atordoamento que não seja dele). Falta ver
  se ele vira obrigação, como a Marca virou.
- Limitações: a comparação usa alvos parados (o dano que os inimigos fariam não entra); só a Chama tem o conjunto de
  fogo; os números continuam provisórios.

## Verificar

```
python -m unittest discover -s ferramentas/prototipos/combate-atributos/testes -t ferramentas/prototipos/combate-atributos
PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/combate-atributos/auxiliares/conferir4.mjs
python ferramentas/prototipos/combate-atributos/auxiliares/folha.py v4
```

Os testes da v4 (11, `testes/test_regras4.py`) cobrem a Marca fora só da v4, o Golpe Oportuno (bônus e previsão igual
ao real), a Chuva (papel no kit, camada em cada inimigo com resistência, previsão do golpe e do pingo, pilhas, teto,
expiração), a Conflagração (consumo por alvo, nada depois, nada contado duas vezes, alvo morto antes), a sequência num
encontro normal com a reserva básica, a comparação mostrando os papéis e o servidor com a v4 na raiz e a v3 em `/v3/`.
O roteiro `conferir4.mjs` confere tudo na tela a 1920×945 e a 1280×720 (com o que a v3 já conferia: previsão, ultimate,
gestos, reinício, movimento reduzido) e grava `capturas/v4-*.png`. Os roteiros da v3, da v2 e da v1 continuam
(`conferir3.mjs` em `/v3/`, `conferir2.mjs` em `/v2/`, `conferir.mjs` em `/v1/`).

## Arquivos

- `motor4/` (a v3 copiada com as mudanças acima e a comparação do fogo, `comparar_fogo`), `tela4/` (por cima de
  `tela3/demo.css`), `testes/test_regras4.py`, `auxiliares/conferir4.mjs`, `folha-v4.png`.
- `servidor.py` serve as quatro versões (`/` e `/api4/`, `/v3/` e `/api3/`, `/v2/` e `/api2/`, `/v1/` e `/api/`).

---

## A terceira versão (26/10/2026, preservada para comparar)

Em http://127.0.0.1:8781/v3/ (o botão v3 no topo da v4).

### v3 · primeiro, as ameaças do Bruto (investigação)

O arquivo de sessão do Jean (v2) tinha as duas lutas contra o Bruto com 12 rodadas e **zero preparações**. Reproduzi
antes de mexer em número:

- **A causa:** na v2 a preparação estava presa ao **número da rodada** (2, 5, 8, 11). O Bruto é o último da ordem,
  então todo aliado age antes dele em toda rodada. Um atordoamento nessas rodadas fazia ele perder a vez, e a
  preparação daquela rodada **não acontecia** (não ficava para depois). Nas lutas do Jean, o Golpe no Joelho e o Golpe
  de Escudo foram usados 4 vezes cada luta: o ciclo inteiro sumiu. Reproduzido com um roteiro que atordoa o Bruto nas
  rodadas 2, 5, 8 e 11: 0 preparações, 0 desfeitas, derrota na rodada 7 (os besteiros nunca pararam).
- **Não era falha de telemetria das preparações** (elas não existiram), **mas havia uma lacuna:** os controles
  aplicados em **inimigos** não eram contados; só os sofridos pelos aliados. Por isso o arquivo dizia "0 sofridos".
- **O atordoamento do Morel "100% das vezes"** que o Jean notou bate com os números da v2: o Joelho aplica 10%
  contra 15% de Tenacidade do Bruto (5% de chance de resistir) e 5% dos besteiros (0%).
- **A regra "firme depois da primeira interrupção"** nunca entrou em jogo nessas lutas (nada foi interrompido; tudo
  foi impedido antes). Ela não era necessária para o problema e foi **retirada** na v3.

**O que mudou na v3:** a preparação conta os **turnos em que o inimigo age** (o Bruto prepara no 2º turno dele e
depois a cada 3); turno perdido não conta, então **atordoar adia, não apaga**, e o adiamento é registrado.
Interromper desfaz a preparação sempre, a não ser num golpe **específico ininterruptível, sinalizado**: o Bruto abaixo
da metade da vida prepara o Golpe Esmagador "furioso", que não se desfaz e o deixa firme até soltar. A Tenacidade do
Bruto subiu para 30% (o Joelho tem 20% de chance de não atordoá-lo). Os resultados guardam cada ameaça (quem, quando,
alvo, ininterruptível, resultado, rodada do fim, dano, se foi aparada), os adiamentos e os controles dos dois lados.

### v3 · o que está decidido e foi aplicado (seção 3.8)

| Decisão | Na v3 |
|---|---|
| Toda habilidade diz tipo, escala e defesa | Na lista do kit (linha embaixo do nome), no mouse sobre o golpe, na Ficha da luta ("os golpes desta vez") e na tabela de dano |
| Tipo e escala são eixos distintos | Corte Preciso: físico, arma + nível + Força, ignora 3 de proteção. Lâmina Rúnica: arcano, foco + nível + Intelecto, ignora 10% de resistência arcana. Avanço do Baluarte: físico, nível + 25% da vida máxima |
| Dano sobrenatural não ignora toda defesa | Arcano e fogo enfrentam a resistência do tipo (o Xamã resiste 30% ao arcano; o Cão de Brasa 60% ao fogo) |
| Resistências por tipo, com teto, vindas do equipamento | Arcano e fogo, teto 60%; o manto do protagonista (Salamandra: fogo 35%; Rúnico: arcano 35%); aparece na ficha e na carta |
| Resistência a dano separada da Tenacidade | A Tenacidade só entra no sorteio do controle; a resistência só no dano |
| Baluarte com contribuição ofensiva própria | Avanço do Baluarte: dano pela vida máxima, e ele puxa os golpes de alvo único até o próximo turno (sem redução) |
| Vontade aumenta a reserva | Recurso máximo = 40 + 4 × nível + 3 × Vontade; começa cheio. Não dá regeneração nem resistência |
| Reserva e regeneração distintas | Reserva: o máximo, cheio no começo. Regeneração: +6 por turno e +6 no ataque básico |
| Combinação aplicar e consumir queimadura | Brasa (põe Queimadura) e Combustão (consome), na especialização de demonstração "Lâmina e Chama" |
| Especialização soma ao repertório | "Lâmina e Chama" aparece junto das habilidades do Guerreiro; o kit mistura as duas |
| Kit trocado fora da luta | A tela Preparar é o "fora da luta" (como cidade ou acampamento); nada de acampamento implementado |
| Ultimate sem Ímpeto, uma vez por luta | Disponível desde o início, gasta a ação e 30 de recurso, uma vez por combatente; queda e retorno não devolvem. Odette ganhou uma ultimate (Luz Restauradora) para testar isso com companheira |
| A interface diz o estado da ultimate | Carta e ação: disponível / falta recurso / já usada nesta luta; Preparar e Ficha: "sem ultimate equipada" |

Mantido: ordem fixa pela Agilidade, turnos individuais, rodadas, uma ação principal, companheiros controlados,
ressurreição. **Hipóteses operacionais (não decisões):** a queda do protagonista encerra a luta; o desempate da
ordem; o invocado no fim da ordem agindo a partir da rodada seguinte; Atacar, Defender e Usar item fora do kit.

### v3 · fórmulas e números provisórios

**A ordem da conta de um golpe** (a mesma na previsão e no golpe, numa função só):
1. potência = base (arma, foco ou nada) + nível + Σ coeficiente × atributo (ou × vida máxima);
2. × o multiplicador da habilidade;
3. + o que a habilidade consome (Combustão: 200% do dano cru que a Queimadura ainda faria);
4. × (1 + a soma dos bônus: comando, marca, ponto fraco, estado do alvo, alvo preparando);
5. × 1,5 se crítico;
6. × 0,5 se o golpe é físico e o alvo tem Guarda;
7. × (1 − as reduções do alvo aliado: defender 40%, desafio 25%, juramento 50%);
8. **uma** defesa, a do tipo: físico − (proteção − o que ignora, mínimo 0); arcano e fogo × (1 − (resistência −
   penetração), entre 0 e 60%);
9. arredonda, mínimo 1; o Escudo de Luz absorve depois.

A Queimadura pinga o valor cru × (1 − resistência ao fogo de quem queima). Nada desconta duas vezes: a proteção não
toca o arcano nem o fogo, a resistência não toca o físico (há teste).

| Atributo | Dá | Conta |
|---|---|---|
| Força | Dano físico (das habilidades que escalam com ela) | +1 de potência por ponto |
| Intelecto | Dano arcano e de fogo | +1 de potência por ponto |
| Percepção | Crítico e ponto fraco | 2%/ponto (até 25%); +3%/ponto contra ponto fraco (até 30%; era 4%) |
| Constituição | Vida e resistência corporal | 4 de vida/ponto; −4% de Sangramento/ponto (até 40%) |
| Vontade | Recurso máximo e Tenacidade | +3 de recurso/ponto; 4%/ponto de Tenacidade (até 40%) |
| Agilidade | Ordem | só a ordem inicial |
| Presença | Fora da luta | nada na luta |

**O kit:** 10 pontos, até 6 espaços, tier 1 = 1, 2 = 2, 3 = 3, ultimate = 4, no máximo uma.

| Origem | Tier 1 | Tier 2 | Tier 3 | Ultimate (30 de recurso, 1×/luta) |
|---|---|---|---|---|
| Guerreiro | Corte Preciso (10), Proteger (15), Grito de Comando (15) | Golpe Pesado (25), Golpe de Escudo (30), **Avanço do Baluarte** (20) | Desafio (25) | Fúria do Campeão (físico em todos, +100% em quem prepara, desfaz as interrompíveis), Juramento (grupo −50% e sem controle por um turno) |
| Lâmina e Chama (demonstração) | **Brasa** (12) | Lâmina Rúnica (20), **Combustão** (20) | — | Tempestade Rúnica (arcano em todos, +100% em marcado, atordoado ou queimando), **Conflagração** (fogo em todos, consome as Queimaduras) |

**A Queimadura:** cada Brasa põe 1 pilha (até 3); cada pilha pinga 30% da potência de fogo de quem pôs, no início dos
3 próximos turnos do alvo. A Combustão (e a Conflagração) soma 200% do que ainda pingaria e apaga a Queimadura.

**As builds** (nível 3; Espada comum 5, Amuleto simples 3, Manto de viagem; os mesmos companheiros):

| | Força | Precisão | Runa | Chama | Baluarte |
|---|---|---|---|---|---|
| FOR AGI CON INT PER VON | 9 3 7 1 4 6 | 6 8 4 1 9 2 | 2 5 5 9 4 5 | 2 6 5 9 3 5 | 5 2 9 1 3 10 |
| Vida / recurso / ordem (enc. 2) | 86 / 70 / 5º | 74 / 58 / 1º | 78 / 67 / 3º | 78 / 67 / 1º | 94 / 82 / 5º |
| Kit sugerido | Golpe Pesado, Proteger, Comando, Golpe de Escudo, Fúria | Corte, Golpe Pesado, Comando, Proteger, Golpe de Escudo, Desafio (sem ultimate) | Lâmina, Corte, Proteger, Golpe de Escudo, Tempestade | Brasa, Combustão, Proteger, Lâmina, Conflagração | Avanço, Desafio, Proteger, Juramento |

**A combinação no Bruto parado** (tabela em Preparar quando a build tem Brasa ou Combustão; Chama, INT 9):

| Sequência | Turnos | Custo | Bruto | Cão (fogo 60%) |
|---|---|---|---|---|
| Brasa e esperar os 3 pingos | 3 | 12 | 23 | 10 |
| Combustão sozinha | 1 | 20 | 10 | 4 |
| Brasa → Combustão | 2 | 32 | 44 | 17 |
| Brasa → Brasa → Combustão | 3 | 44 | 84 | 32 |
| Lâmina Rúnica × 2 (comparação) | 2 | 40 | 56 | 52 |

Preparar a combinação rende mais por recurso e por luta longa; a Lâmina rende mais por turno e não depende do alvo
ficar vivo. Contra o Cão, o fogo quase some: a preparação para o inimigo importa.

**O Avanço do Baluarte e a Constituição** (Golpe Pesado e Avanço no Bruto, trocando pontos de Força por Constituição):

| CON / FOR | Vida | Atacar | Golpe Pesado | Avanço |
|---|---|---|---|---|
| 5 / 9 | 78 | 17 | 31 | 23 |
| 7 / 7 | 86 | 14 | 27 | 25 |
| 9 / 5 | 94 | 12 | 24 | 27 |

Cada ponto de Constituição dá +1 ao Avanço e +4 de vida; cada ponto de Força dá +1,8 ao Golpe Pesado e +1 a todo golpe
com a arma. A Constituição não domina ataque e sobrevivência ao mesmo tempo: o Baluarte troca o dano de arma pelo
Avanço, que ainda puxa os golpes para ele.

#### Os encontros: o que mudou nos inimigos desde a v2

| Inimigo | Mudança | Por quê |
|---|---|---|
| Todos com preparação | Cadência por turno agido (primeiro, cada) em vez de número de rodada | A investigação acima |
| Bandido Bruto | Tenacidade 15% → 30%; abaixo de 50% da vida, o Esmagador vem ininterruptível (sinalizado) | O Joelho não podia ser 100%; um golpe específico que pede outra resposta |
| Xamã Caído | Resistência arcana 30%; a Garra virou arcana (12) | Testar a resistência e o manto rúnico |
| Cão de Brasa (novo, encontro 4) | 140 de vida, fogo 60%, Mordida em brasa (fogo 11), Sopro de Brasa (fogo 16 no grupo + Queimadura 4) | O inimigo para comparar com e sem resistência e a Chama contra a Runa |
| Regra "firme depois da 1ª interrupção" | Retirada | Não aprovada e não necessária |

Novos testes: **t5 · ultimate, queda e retorno** (Odette usa a Luz, cai, volta com a Pena: continua gasta) e **t6 ·
Queimadura e Combustão** (um Soldado parado, sem Guarda, com 400 de vida, para comparar as sequências).

### v3 · o que observei

Joguei à mão o encontro 2 com o **Baluarte** (até a rodada 4; o jogador automático terminou: vitória na 9) e o
encontro 3 com a **Chama** (até a rodada 3; vitória na 10), e comparei os mantos com a mesma build, kit e semente.

- **O Avanço deu ao Baluarte uma decisão própria.** Na rodada 3, o Esmagador mirava Odette (38 de vida, 35 previstos).
  Em vez do Joelho do Morel, usei o Avanço no Bruto: 27 de dano, e o golpe veio para Jean (33; 30% de resistir ao
  atordoamento, e resistiu). O custo apareceu na rodada 1: o mesmo Avanço puxou três golpes para Jean (32 de dano).
  É uma troca de vida por dano e proteção, não um bônus de graça.
- **A combinação pediu planejamento e mostrou o risco.** Com a Queimadura de 2 pingos (o primeiro valor), o Xamã já
  tinha parado de queimar quando a Conflagração ficou pronta: mudei para 3 pingos de 30%. Depois, Brasa no Xamã (rodada
  1), Brasa no Soldado (rodada 2) e Conflagração na rodada 3: 18 + 29 + 9 de dano por 30 de recurso, no momento em que
  as duas Queimaduras estavam vivas.
- **O manto importa contra o inimigo certo:** no encontro 4, o dano de fogo em Jean caiu de 50 para 26 com o Manto de
  salamandra (mesma build, kit e semente); contra os outros encontros, nada muda.
- **A ultimate e a abertura:** com a reserva cheia, Fúria e Tempestade valiam mais na abertura. Mudei o efeito (golpe
  base menor, +100% contra quem prepara ou tem estado), não a regra. Na medição automática, abrir com a ultimate passou
  a encurtar o encontro 2 em uma rodada, mas aumentou o dano recebido nos encontros 3 e 4 (e o Juramento na abertura
  piorou o encontro 3: 189 de dano contra 127 na hora da ameaça). Não há dominância clara; falta ver com uma pessoa.
- **As ameaças do Bruto agora aparecem:** 3 a 4 anunciadas por luta no encontro 2, com interrupções, resoluções,
  desfeitas por queda e 1 a 2 adiamentos por atordoamento, tudo nos resultados.
- **O jogador automático** (regra fixa, só ordem de grandeza): vence os quatro encontros com as cinco builds; encontros
  2 e 3 em 8 a 15 rodadas; o Baluarte é o mais lento (13–15). O encontro 1 continua curto (3 rodadas, com a reserva
  cheia).
- **Para o Jean confirmar:** se o tipo e a defesa ficaram claros sem poluir os botões (estão no mouse e na Ficha); se o
  Avanço faz o Baluarte querer ser jogado; se a combinação vale o tempo; se a ultimate de uso único tem hora; se o
  encontro 1 ficou curto demais com a reserva cheia.

### v3 · limitações

- O jogador automático não prova equilíbrio, e ele usa pouco as ultimates "na hora" (as condições dele são simples).
- Só o protagonista monta o kit e só ele tem equipamento; os companheiros têm kits fixos (Odette com uma ultimate).
- Três tipos de dano; sem vulnerabilidades, sem resistência física percentual, sem catálogo de elementos.
- A cura continua sem atributo; o rompimento de proteção só no Corte e na Guarda do Golpe Pesado.
- As peças são de laboratório: sem loot, forja ou encantamento.

### Verificar (v3)

```
python -m unittest discover -s ferramentas/prototipos/combate-atributos/testes -t ferramentas/prototipos/combate-atributos
PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/combate-atributos/auxiliares/conferir3.mjs
python ferramentas/prototipos/combate-atributos/auxiliares/folha.py v3
```

Os testes da v3 (21, `testes/test_regras3.py`) cobrem: a previsão igual ao dano real por tipo e alvo (físico, arcano,
fogo; Bruto, Xamã, Cão, Soldado); resistência e penetração na ordem e no teto; nada descontado duas vezes; o manto
reduzindo só o tipo dele; toda habilidade de dano com tipo, escala e defesa; a Vontade aumentando só a reserva e a
Tenacidade; a combinação feita só com a reserva básica (Vontade 1, sem ataque básico); a Combustão somando e
consumindo; o Avanço pela vida sem mexer nos outros golpes; nenhum desbloqueio e Presença fora; a ultimate disponível
desde o início, uma vez, "já usada" depois, falta de recurso, e a queda e o retorno sem devolver; as ameaças do Bruto
(atordoar adia e é registrado, interrupção registrada e sem "firme" geral, o furioso ininterruptível); o recurso antes
e depois na linha do tempo; o kit; ordem, rodada, retorno, gestos; e o servidor com as três versões. O roteiro
`conferir3.mjs` confere tudo isso na tela a 1920×945 e a 1280×720 e grava `capturas/v3-*.png`.

### Arquivos (v3)

- `motor3/conteudo.py`, `motor3/regras.py`, `tela3/` (index, demo.js, demo.css por cima da v1 e da v2).
- `servidor.py` (as três versões: `/` e `/api3/`, `/v2/` e `/api2/`, `/v1/` e `/api/`), `demo.bat`, `ROTEIRO.md`,
  `testes/`, `auxiliares/` (conferir.mjs, conferir2.mjs, conferir3.mjs, folha.py), `capturas/`, `folha.png`,
  `folha-v2.png`, `folha-v3.png`.

---

## A segunda versão (26/10/2026, preservada para comparar)

Em http://127.0.0.1:8781/v2/.

### v2 · o que está decidido e foi aplicado

| Decisão (25, seção 3.7) | Na v2 |
|---|---|
| Atributos ofensivos entram direto no dano | Potência física = arma + nível + **Força**; sobrenatural = foco + nível + **Intelecto**. O dano é a potência × a habilidade |
| Nem todo atributo dá dano | Constituição (vida, resistência corporal), Vontade (Tenacidade) e Agilidade (ordem) não somam dano |
| Sem desbloqueio por atingir X | Saíram: Força 5 contra atordoar, Constituição 5 no sangramento, Percepção 5 no ponto fraco, Vontade 5 no terror. Cada ponto soma igual até o teto (um teste confere ponto a ponto) |
| Mudança de comportamento em habilidade, não em atributo | O Desafio (puxa as ameaças), o Juramento (o grupo sem controle por um turno) e o Golpe de Escudo (interromper) são habilidades do kit |
| Agilidade: ordem inicial fixa, sem ação extra | Igual à v1 |
| Presença só fora da luta, fora do orçamento | 1 a 10 à parte dos 30 pontos; nenhum efeito na luta (um teste confere: a mesma luta com Presença 1 e 10 sai igual). O Grito de Comando agora dá +30% fixo |
| Tenacidade gradual, com teto, chance mostrada, sem contar duas vezes | Ver a fórmula abaixo; a carta da ameaça mostra a chance final; um sorteio por controle |
| Sem aumento universal de duração | Nenhum atributo mexe em duração |
| Kit com pontos por tier, até uma ultimate | 10 pontos, até 6 espaços, tier 1 = 1, tier 2 = 2, tier 3 = 3, ultimate = 4, no máximo uma |
| Atacar, Defender e Usar item fora do kit (hipótese) | Fora dos espaços e dos pontos; os três gastam a ação. Marcados como "básico" na luta |
| Pontos de kit ≠ aprender ≠ recurso da luta | A tela Preparar diz isso; aprender/desenvolver não está implementado |
| O resto do combate combinado | Ordem fixa, rodadas, uma ação por turno, ameaças com resposta, queda sem morte, retorno na posição sem recuperar a vez, marcos explícitos: como na v1, com os mesmos testes |

**Hipóteses operacionais mantidas (não decididas):** a queda do protagonista encerra a luta em derrota; o desempate
da ordem (Percepção, depois aliado antes de inimigo, depois a entrada); o invocado entra no fim da ordem e age a partir
da rodada seguinte. A tela e o registro dizem "hipótese operacional" onde aparecem.

### v2 · fórmulas provisórias

Escala de 1 a 10; o protagonista distribui **30 pontos** nos seis atributos de combate. Presença à parte.

| Atributo | O que dá | Conta |
|---|---|---|
| Força | Dano físico | potência física = arma + nível + FOR (+1 por ponto) |
| Intelecto | Dano sobrenatural | potência sobrenatural = foco + nível + INT (+1 por ponto). Não dá cura, desconto nem controle |
| Percepção | Crítico e ponto fraco | crítico 2% por ponto (até 25%), dano ×1,5; contra quem tem ponto fraco, +4% de dano por ponto (até +40%) |
| Constituição | Vida e resistência corporal | vida = classe + 6 × nível + 4 × CON; sangramento −4% por ponto (até −40%) |
| Vontade | Tenacidade | 4% por ponto (até 40%) |
| Agilidade | Ordem | só a ordem inicial |
| Presença | Fora da luta | nada na luta |

- **Tenacidade:** chance final de resistir a um controle = Tenacidade do alvo − aplicação de quem controla (nunca
  abaixo de 0). O Golpe Esmagador e os golpes de interromper aplicam 10%; o Grito de Terror, 0%. Um sorteio por
  controle; não reduz duração nem dano. Teto 40%: nunca imunidade. O Juramento (habilidade) impede o controle por um
  turno.
- **Interromper** desfaz a preparação sempre (resposta deliberada, sem sorte); só o atordoamento depois pode ser
  resistido. Um inimigo interrompido uma vez prepara **firme** depois: não se desfaz de novo (para a interrupção não
  responder a toda ameaça).
- **Defender** −40%, **Desafio** −25% e **Juramento** −50%, todos até o início do próximo turno de quem usou; são da
  regra ou da habilidade, sem atributo.
- **Cura:** 16 + 2 × nível + o símbolo sagrado (Odette: 26), sem atributo nesta versão; o atributo da cura está aberto.
- **Dano de um golpe aliado:** potência × habilidade → comando → marca → ponto fraco → crítico → guarda (metade, só
  físico) → − proteção (mínimo 1) → escudo. A previsão da tela e o golpe usam a **mesma função** (teste: em dezenas de
  golpes das quatro builds, o dano real é o previsto, normal ou crítico).

#### O recurso (revisto junto: custos, reserva, recuperação)

Máximo 60, começa com **40** (era 30), recupera **8 no início de cada turno** (novo) e mais 8 no ataque básico (era 10).
Custos: 10 a 15 nas baratas, 20 a 30 nas fortes. A ultimate não gasta recurso: pede **3 de Ímpeto**, que sobe quando
um inimigo cai ou uma ameaça é desfeita ou aparada (defendida, protegida, desafiada, escudada) e zera ao usar.

#### As builds (mesmo nível 3, Espada comum, Amuleto simples, proteção 3, mesmos companheiros)

| | Força | Precisão | Runa | Baluarte |
|---|---|---|---|---|
| Proposta | bate forte com a arma e aguenta; age tarde | age primeiro e acerta pontos fracos e críticos | luta com a lâmina rúnica: Intelecto no lugar da Força | segura as ameaças: muita vida e Tenacidade, dano menor |
| FOR AGI CON INT PER VON | 9 3 7 1 4 6 | 6 8 4 1 9 2 | 2 5 5 9 4 5 | 5 2 9 1 3 10 |
| Vida / ordem (enc. 2) | 86 / 5º | 74 / 1º | 78 / 3º | 94 / 5º |
| Potência física / sobrenatural | 17 / 7 | 14 / 7 | 10 / 15 | 13 / 7 |
| Crítico / ponto fraco / Tenacidade | 8% / +16% / 24% | 18% / +36% / 8% | 8% / +16% / 20% | 6% / +12% / 40% |
| Kit sugerido (10 pontos) | Golpe Pesado, Proteger, Comando, Golpe de Escudo, Fúria do Campeão | Corte Preciso, Golpe Pesado, Comando, Proteger, Golpe de Escudo, Desafio | Lâmina Rúnica, Corte Preciso, Proteger, Golpe de Escudo, Tempestade Rúnica | Desafio, Proteger, Comando, Corte Preciso, Juramento |
| Dano no Bruto (normal / crítico) | Golpe Pesado 33 / 51 | Golpe Pesado 32 / 49 | Lâmina Rúnica 28 / 42 | Corte Preciso 17 / 26 |

**O kit do protagonista:** tier 1 (1 ponto): Corte Preciso (10, ignora 3 de proteção), Proteger (15), Grito de
Comando (15, +30%). Tier 2 (2): Golpe Pesado (25), Lâmina Rúnica (20, sobrenatural, a Guarda não reduz), Golpe de
Escudo (30, interrompe). Tier 3 (3): Desafio (25). Ultimate (4, uma): Fúria do Campeão (físico em todos), Tempestade
Rúnica (sobrenatural em todos), Juramento (grupo −50% e sem controle por um turno). Odette e Morel têm kits fixos
menores (Odette: Lampejo, Curar, Escudo de Luz, Reerguer; Morel: Golpe no Joelho, Marcar) e os mesmos básicos.

**Equipamento para comparar uma peça:** Espada comum 5, reforçada 7, de mestre 9; Amuleto simples 3, rúnico 6. Em
Preparar, a tabela "Trocando só uma peça" mostra cada golpe do kit com cada opção, na mesma build, nível e alvo.

#### Os encontros: o que mudou nos inimigos (para não creditar a uma build o que foi do inimigo)

Os mesmos três encontros e os mesmos testes da v1, mais o **t5 · Ímpeto pronto** (começa com a ultimate cheia, para
experimentar). Ajustes, todos porque o grupo mudou, não para favorecer uma build:

| Inimigo | Vida v1 → v2 | Dano v1 → v2 | Outras mudanças |
|---|---|---|---|
| Lobo / Lobo Alfa | 26 → 56 / 40 → 85 | 8 → 9; Bote 20 → 22 | sangramento 8 por pingo, 2 pingos |
| Bandido Bruto | 110 → 250 | 14 → 15; Esmagador 34 → 36 | Esmagador a cada 3 rodadas (era 2); aplica 10% |
| Besteiro (2) | 32 → 64 | 13 | — |
| Xamã Caído | 65 → 140 | 9 → 12 | Terror aplica 0% |
| Soldado Morto | 50 → 110 | 14 → 18 | sem "firme" (Tenacidade 35%) |
| Afogado | 20 → 36 | 8 → 10 | — |

A vida subiu porque o dano do grupo subiu com os atributos (a potência física da Força passou de 11 para 17) e porque o
Jean aceitou lutas mais longas; o dano subiu um pouco porque a vida do grupo subiu (Jean 58–73 → 74–94). A Agilidade dos
inimigos está na escala 1–10. Todos os inimigos têm Tenacidade (0% a 35%).

### v2 · o que observei

Joguei à mão o encontro 2 com a **Precisão** (vitória na rodada 9) e com o **Baluarte** (até a rodada 4, depois o
jogador automático terminou: vitória na 14), e o encontro 3 com a **Runa** (até a rodada 3; vitória na 9).

- **As builds mudaram a escolha.** Com a Precisão, Jean age primeiro: matei os besteiros nas rodadas 1–3 com Golpe
  Pesado (um crítico de 37). Com o Baluarte, Jean age depois de todos, mas o Desafio puxou o Esmagador para ele (24 de
  dano em vez de 35 em Odette, 30% de resistir, e resistiu): a ameaça virou problema do tanque, não da curandeira. Com a
  Runa, a Lâmina (28) ignora a Guarda do Soldado (o ataque comum dá 4); matei o xamã antes do Grito sair, e a build
  pedia guardar Vigor para a Lâmina (Jean ficou com 4).
- **Proativo e emergência ao mesmo tempo.** Gastei Vigor desde a rodada 1 e não faltou resposta na primeira ameaça. O
  custo apareceu na segunda: o Golpe Pesado da rodada 5 deixou Jean com 11 de Vigor quando o Esmagador veio firme; sem
  Proteger nem Desafio, Odette se cobriu com o Escudo de Luz. Na terceira, a resposta foi matar o Bruto antes (34 de
  vida, Golpe Pesado + o golpe de Morel). Cada ameaça pediu uma resposta diferente.
- **O jogador automático** (regra fixa, só ordem de grandeza): gastando sem reserva, vence os encontros 2 e 3 em 9–15
  rodadas; guardando 40 de reserva, as mesmas lutas levam 2 a 4 rodadas a mais e o ataque básico passa de ~25% para
  ~50% das ações. Gastar não é punido; guardar alonga. Ignorando as ameaças, o dano recebido no encontro 2 vai de
  ~100–175 para ~185–315, com quedas, e o Baluarte perde.
- **Possível dominância a observar:** contra o Bruto (ponto fraco), a Precisão quase empata com a Força no Golpe
  Pesado (32 contra 33) porque o ponto fraco dá +36%; contra alvo sem ponto fraco, a Força ganha com folga. É bom
  para a Precisão ter seu alvo, mas +4% por ponto pode ser muito.
- **A ultimate** chegou na rodada 5–6 nas lutas longas (dois inimigos caídos ou uma ameaça desfeita e um caído). No
  encontro 1 (3–4 rodadas) quase nunca chega. O Juramento ficou sem uso pelo jogador automático: falta ver se uma
  pessoa acha a hora dele.
- **O que corrigi jogando:** o nome do inimigo aparecia como "livre" na faixa com uma build pronta; "Defendenda" no
  feminino (o mesmo erro existia na v1, corrigido nas duas); o grupo não cabia na coluna a 1280×720 com Ímpeto e
  estados (as barras e as fichas ficaram mais baixas nessa altura).
- **Para o Jean confirmar:** se a diferença entre as builds agora se sente (é o objetivo da rodada); se o encontro 1
  ficou curto demais (3–4 rodadas); se o Baluarte, que leva 13–15 rodadas, arrasta.

### v2 · limitações

- O jogador automático escolhe por regra fixa; não prova equilíbrio. As partidas à mão são poucas e com aprendizagem.
- Só o protagonista monta o kit; os companheiros têm kits fixos. Sem talentos, caminhos por habilidade, aprender ou
  trocar o kit em lugar seguro.
- O atributo da cura e a fórmula do rompimento de proteção ficam abertos; a Guarda só some com golpes físicos.
- Duas preparações ganham Ímpeto em dobro quando o inimigo cai preparando (a ameaça desfeita e a queda): anotado, não
  corrigido.
- O equipamento é só para comparar uma peça; não há loot, forja ou encantamento.

### Verificar (v2)

```
python -m unittest discover -s ferramentas/prototipos/combate-atributos/testes -t ferramentas/prototipos/combate-atributos
PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/combate-atributos/auxiliares/conferir2.mjs
PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/combate-atributos/auxiliares/conferir.mjs
python ferramentas/prototipos/combate-atributos/auxiliares/folha.py v2
```

Os testes da v2 (27, em `testes/test_regras2.py`) cobrem: a Força e o Intelecto somando +1 de potência por ponto; os
benefícios graduais ponto a ponto, sem degrau e sem imunidade; Presença sem efeito na luta (a mesma luta com 1 e 10);
o Comando sem Presença; a Tenacidade (a chance mostrada é a usada, a aplicação desconta uma vez, um sorteio, o Juramento
impede, o Proteger leva o golpe sem sorteio); o kit (orçamento, espaços, uma ultimate, básicos fora); o recurso por
turno e no básico; a previsão igual ao dano real nas quatro builds e na ameaça; a ficha igual à luta; a arma aumentando
o resultado; e o que a v1 já garantia (ordem, vez perdida, retorno antes e depois da posição, inimigo derrubado antes
da preparação, a mesma vez duas vezes, a invocação). O roteiro `conferir2.mjs` confere a 1920×945 e a 1280×720 a tela
Preparar e a luta (sem rolagem nem corte, o grupo inteiro na coluna), a previsão no alvo igual ao dano real, a chance
de resistir na ameaça, a ultimate, o teclado, a tecla segurada, o clique duplo, o reinício, o movimento reduzido e o
botão da v1, e grava `capturas/v2-*.png`.

### Arquivos (v2)

- `motor2/conteudo.py` (atributos, builds, kit, equipamento, recurso, inimigos, encontros, a situação) e
  `motor2/regras.py` (as regras, a ficha, a comparação); `tela2/` (index, demo.js, demo.css por cima de
  `tela/demo.css`).
- `servidor.py` (as duas versões: `/` e `/api2/` a v2, `/v1/` e `/api/` a v1; os estáticos do jogo só leitura),
  `demo.bat`, `ROTEIRO.md`, `testes/`, `auxiliares/` (conferir.mjs, conferir2.mjs, folha.py), `capturas/`,
  `folha.png`, `folha-v2.png`.

---

## A primeira versão (25/10/2026, preservada para comparar)

Uma luta jogável com a direção do [25 — Etapa 4](../../../roadmapIDEIAS/25-ETAPA4-REFORCO-E-ENCANTAMENTO.md),
seções 1 a 8. **Não é integração:** o jogo não carrega nada desta pasta (um teste confere), as regras de produção
não mudaram e os números são de teste, não catálogo nem balanceamento da campanha.

### Abrir e jogar (v1)

- Pelo mesmo `demo.bat`: a v1 fica em http://127.0.0.1:8781/v1/ (o botão **v1** no topo da v2).
- No topo: **Encontro** (os três encontros e os quatro casos de teste), **Construção** (A, B, C ou a livre),
  **Reiniciar** (`R`). **Comparar** mostra os valores derivados das construções lado a lado e monta a livre; **Fora da
  luta** é a situação de aventura; **Resultados** lista as lutas da sessão.
- Na luta: a carta de ouro é quem age. **Número** escolhe a ação; se ela pede alvo, as cartas válidas ganham um
  número (clique ou tecle). `Esc` volta. Uma ação indisponível diz o motivo no lugar da descrição.
- Os resultados ficam numa pasta temporária nova a cada execução (o caminho aparece em Resultados). Os saves do jogo
  não são lidos nem tocados. A construção livre e a última escolha ficam no navegador.

### O que foi respeitado do 25

| Decisão | No protótipo |
|---|---|
| Protagonista + dois companheiros controlados diretamente | Jean, Odette e Morel; o jogador escolhe a ação de cada um na vez dele |
| Agilidade define a ordem, fixa a luta inteira; sem ação extra | A ordem é calculada uma vez no começo (Agilidade; empate: Percepção, depois aliado antes de inimigo, depois a ordem de entrada) e não muda nem se a Agilidade mudar |
| Turnos individuais intercalados; rodada termina depois de todos, inclusive quem perdeu a vez | A faixa da ordem marca quem já foi, quem age, quem está fora e o fim da rodada |
| Uma ação principal por turno | Uma ação (habilidade, ataque, defesa ou item) e a vez passa |
| Ataque básico útil; defesa até o próximo turno | O ataque básico recupera 10 de recurso; Defender vale até o **início** do próximo turno de quem defendeu |
| Ameaças importantes anunciadas, com chance real de resposta | A preparação é anunciada na vez do inimigo e resolve na vez seguinte dele: todos os aliados agem uma vez no meio. A carta mostra alvo, dano previsto (e se o alvo defender), efeito e quando resolve |
| Sem morte de companheiro; volta por ressurreição cara ou item escasso | Caído = pulado na ordem. Volta só por Reerguer (45–50 de Fé, uma vez por luta) ou pela Pena de Fênix (uma na bolsa, só no teste 2) |
| Volta na posição original, sem recuperar vez perdida | Se a posição dele nesta rodada ainda não passou, age nela; se já passou (pulada), só na próxima |
| Pets e invocações | Só do lado inimigo: entram no fim da ordem e agem a partir da rodada seguinte |
| Os sete atributos com valores derivados | Força, Agilidade, Constituição, Intelecto, Percepção, Vontade e Presença; a Ficha e o Comparar mostram cada valor com a conta |
| Potência pela habilidade, nível e equipamento; atributos modulam | O dano é arma + nível × a habilidade. Nenhum atributo soma dano direto; eles mudam ordem, crítico, ponto fraco, defesa, resistências, custo, ruptura de guarda e comando |
| Companheiro contribui fora da luta sem decidir pelo protagonista | "A laje do ossuário": Morel ajuda a erguer (com barulho), Odette lê a inscrição; tocar a laje continua sendo escolha de Jean |

### Os relógios e os marcos

- **Turno** é a vez de um combatente; **rodada** é a ordem inteira, uma vez cada.
- No **início do turno** de alguém expira o que dura "até o início do próximo turno" dele (Defendendo; Protegido e
  Protegendo, pelo turno de quem protege) e o sangramento pinga 4.
- **Atordoado** e **Aterrorizado**: a próxima vez é perdida (gasta ao começar o turno). Uma preparação do inimigo
  atordoado se desfaz.
- **Abalado** (o terror com Vontade 5+): −25% de dano no próximo turno do portador; acaba no fim desse turno.
- **Escudo de Luz, Marcado, Comandado**: até o **fim da rodada seguinte** à aplicação (ou gastos antes, no golpe).
- **Guarda** (Soldado Morto): enquanto houver, o dano cai pela metade; o golpe comum rompe 1, o Golpe Pesado rompe a
  Força de quem bate.
- O protagonista caído é derrota. Inimigo derrotado antes da vez dele: a preparação não sai.

### Fórmulas provisórias

Escala de 1 a 8; o protagonista distribui **24 pontos**; os companheiros têm atributos próprios. **5 é o limiar** das
regras de sim/não.

| Atributo | O que muda | Conta |
|---|---|---|
| Força | Golpe Pesado rompe Guarda; aguentar golpe que atordoa | rompe = FOR; FOR 5+ não fica atordoado |
| Agilidade | Posição na ordem | só a ordem, uma vez |
| Constituição | Vida; sangramento | vida = classe + 6 × nível + 5 × (CON − 3); CON 5+ sangra 1 vez em vez de 2 |
| Intelecto | Custo das habilidades | −5% por ponto acima de 3, até −25% (sem encarecer abaixo de 3) |
| Percepção | Crítico; ponto fraco | 5% + 4% × (PER − 3), até 25%, dano × 1,5; PER 5+ aproveita ponto fraco (+25%) |
| Vontade | Defender; terror | Defender reduz 40% + 5% × (VON − 3), até 65%; VON 5+ só fica abalado |
| Presença | Grito de Comando | +15% + 5% × (PRE − 3) no próximo golpe do aliado; tira o terror |

Dano de um golpe aliado: (arma + nível) × habilidade → comando → marca → abalado → ponto fraco → crítico → guarda
(metade) → defesa do alvo → − proteção (mínimo 1) → escudo. Os inimigos não têm crítico; a previsão da ameaça usa a
mesma conta.

### As três construções (mesmo nível 3, arma 8, proteção 3, mesmos companheiros)

| | A · Força e Constituição | B · Agilidade e Percepção | C · Vontade e Presença |
|---|---|---|---|
| Atributos | FOR 7 AGI 2 CON 6 INT 2 PER 2 VON 3 PRE 2 | FOR 3 AGI 6 CON 3 INT 2 PER 6 VON 2 PRE 2 | FOR 3 AGI 3 CON 3 INT 3 PER 2 VON 6 PRE 4 |
| Vida | 73 | 58 | 58 |
| Ordem (encontro 1) | 5º | 1º | 5º |
| Crítico / ponto fraco | 1% / não | 17% / sim | 1% / não |
| Defender | 40% | 35% | 55% |
| Terror / atordoar / sangrar | perde a vez / aguenta / 1 vez | perde a vez / atordoado / 2 | abalado / atordoado / 2 |
| Golpe Pesado rompe / Comando | 7 / +10% | 3 / +10% | 3 / +20% |

### O conteúdo

- **Jean** (Guerreiro): Atacar, Golpe Pesado (25), Proteger (15), Grito de Comando (20), Defender.
- **Odette** (curandeira): Bastão, Curar (20 → 18 com INT 5), Escudo de Luz (15 → 14), Reerguer (50 → 45, uma vez),
  Defender.
- **Morel** (mercenário): Golpe, Golpe no Joelho (30: desfaz a preparação e atordoa quem não é firme), Marcar (10),
  Defender.
- Itens: Poção de Vida (1 por encontro); Pena de Fênix (só no teste 2).
- **Encontro 1 · Os lobos da estrada** (tutorial): Lobo Alfa (anuncia o Bote: 20 de dano e sangramento) e Lobo.
- **Encontro 2 · O bruto anunciado**: Bandido Bruto (110 de vida, ponto fraco; anuncia o Golpe Esmagador a cada duas
  rodadas: 34 e atordoa) e dois Besteiros.
- **Encontro 3 · O xamã e o soldado**: Xamã Caído (chama Afogados nas rodadas 1, 4, 7, até 2; anuncia o Grito de
  Terror) e Soldado Morto (Guarda 6, firme, ponto fraco).
- **Testes** (a faixa vermelha diz a condição artificial): 1 · Jean começa atordoado (perde a vez, a rodada fecha);
  2 · Morel caído e Jean com Agilidade 6 e uma Pena (volta antes da posição: age na mesma rodada); 3 · Morel caído e
  Odette com Fé cheia (Reerguer depois da posição: só na próxima); 4 · Lobo Alfa com 8 de vida, Agilidade 1 e o Bote
  já preparado (derrubado antes, o Bote não sai).

### Reproduzir e comparar

- Cada encontro tem semente fixa: as mesmas escolhas dão a mesma luta. Para comparar construções, jogue o mesmo
  encontro com A, B e C (o seletor reinicia) e abra **Resultados**: rodadas, quedas, dano por personagem, preparações
  que saíram e que foram desfeitas, e as ações usadas.
- **Comparar** põe as três construções e a livre lado a lado, com o que difere em destaque e a ordem do encontro 1.
- Medição por um jogador automático (`python` com as regras; não substitui jogar): três estilos em cada encontro.

| Encontro / construção | Sensato | Sem o Golpe no Joelho | Ignorando as ameaças |
|---|---|---|---|
| 1 · A / B / C | vitória em 3 / 3 / 3 | 3 / 3 / 3 | 3 / 3 / 3 |
| 2 · A / B / C | 10 / 8 / derrota na 5 | 10 / 10 / derrota na 5 | 10 com 2 quedas / derrota na 5 / derrota na 5 |
| 3 · A / B / C | 6 / 7 / 6 | 7 / 10 / 7 | 7 / 10 / 7 |

### O que observei jogando

Joguei o encontro 2 com a B à mão até o fim (vitória na rodada 6) e li os registros dos outros:

- **Decisões reais.** O Golpe Esmagador anunciado em Odette (25 de vida, 33 previstos) abriu cinco respostas
  diferentes: Joelho de Morel, Proteger de Jean (ele levaria 31 e ficaria atordoado: FOR 3), Defender de Odette (16),
  Escudo de Luz nela (17 e atordoada), Curar antes. Usei o Escudo numa rodada e o Joelho na outra. O recurso pesa: o
  Golpe Pesado de Jean deixa 5 de Vigor e só o ataque básico nas duas vezes seguintes; gastar cedo ou guardar para
  Proteger é uma escolha.
- **Opção dominante (corrigida).** Na primeira calibragem o Golpe no Joelho a 20 desfazia toda preparação: o jogador
  automático nunca deixou uma sair. A 30, Morel desfaz uma, talvez duas por luta; depois precisa de outra resposta.
  Ainda é a resposta mais limpa contra o Bruto; vale observar se continua a primeira escolha sempre.
- **As construções mudam o jogo.** A aguenta o Esmagador (FOR 7) e rompe a guarda do Soldado de uma vez; B age
  primeiro, pega o ponto fraco do Bruto e critica, mas cai atordoada e sangra o dobro; C defende 55%, só fica abalada
  no grito e comanda melhor. C sofreu no encontro 2 com o jogador automático (derrota): sem Força e sem iniciativa, ela
  depende de Defender e Comandar na hora certa, o que a heurística não faz.
- **Repetição e espera.** O Soldado Morto com a guarda que só caía com o Golpe Pesado virou 4 rodadas de 2–4 de dano;
  agora o golpe comum também rompe 1. Ainda há rodadas de ataque básico quando o Vigor zera: é o lugar para observar se
  arrasta.
- **Informação.** A previsão de dano na carta da ameaça bate com o dano real (teste). O que faltava apareceu jogando e
  foi corrigido: nomes iguais (Besteiro 1 e 2), concordância (Odette atordoada), o Abalado que expirava antes de valer.
  Não há dica de "respostas possíveis" na carta: o jogador deduz pelas ações; vale ver se o Jean sente falta.
- **O encontro 3 ficou o mais leve** (sem quedas em nenhum estilo). As prioridades competem (derrubar o xamã antes do
  grito, os afogados, o soldado), mas sem punição forte; é o primeiro número a mexer se a sensação for de folga.

### Limitações

- Números de teste; o jogador automático escolhe por regra fixa, não como uma pessoa, e serve para ordens de
  grandeza.
- Sem animação de ataque nem números flutuando: a vida muda na carta (com o −N ao lado) e o registro mostra a conta de
  cada golpe. Os eventos novos chegam em sequência no registro (sem animação com movimento reduzido).
- Os inimigos escolhem o alvo do golpe comum ao acaso (com semente) e o da preparação pelo mais ferido; não há
  provocação.
- Sem talentos, equipamento trocável, níveis, ultimate, pets aliados ou fuga. A ficha dos companheiros é fixa.
- A situação fora da luta é uma só, sem consequência depois.

### Verificar

```
python -m unittest discover -s ferramentas/prototipos/combate-atributos/testes -t ferramentas/prototipos/combate-atributos
PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/combate-atributos/auxiliares/conferir.mjs
python ferramentas/prototipos/combate-atributos/auxiliares/folha.py
```

Os testes (26) cobrem: a ordem calculada uma vez e os desempates; a invocação no fim e agindo na rodada seguinte; a
vez perdida e o fim da rodada; a defesa, o escudo, a marca e o abalado expirando no marco certo; o inimigo derrotado
antes da preparação; o Joelho; a previsão igual ao dano real; a queda e a volta antes e depois da posição; a mesma
vez enviada duas vezes; reiniciar sem acumular; os derivados iguais ao estado real; o servidor; o jogo sem nada do
protótipo. O roteiro do navegador confere a 1920×945 e a 1280×720 (sem rolagem, sem corte, teclado, tecla segurada,
clique duplo, reinício, movimento reduzido) e grava `capturas/`; a `folha.png` junta as principais.

### Arquivos

- `motor/conteudo.py` (grupo, construções, habilidades, inimigos, encontros, testes, a situação) e `motor/regras.py`
  (as regras e o estado para a tela).
- `servidor.py` (a API e os arquivos; os estáticos do jogo só leitura), `tela/` (index, demo.js, demo.css), `demo.bat`.
- `testes/`, `auxiliares/conferir.mjs`, `auxiliares/folha.py`, `capturas/`, `folha.png`.
