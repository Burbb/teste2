# 21 — Ataques em área dos inimigos: diagnóstico (sobre a 1.82.0, sem mudar o jogo)

Pedido de Jean (13/10/2026): avaliar se inimigos mais fortes poderiam ameaçar melhor a comitiva com ataques em área,
para dar variedade e importância à proteção do grupo. Nesta entrega, só o levantamento: quem já tem ataque em área e
quando usa, como os inimigos escolhem o alvo e quanto ameaçam os companheiros, quem seriam os candidatos coerentes, e
se o ataque deveria ser uma habilidade anunciada. **Nada foi implementado nem teve o dano mudado.**

Fontes: `rpg/inimigos.py` (as habilidades e o juízo de quando cada uma faz sentido), `rpg/combate/turnos.py` (a vez
dos inimigos e o alvo), `rpg/comitiva/luta.py` (quem protege), `rpg/dados.py` (famílias, guardiões e afixos),
`rpg/missoes.py` (os inimigos da capela e Ilse). Medição: `python -m tests.area_inimigos` (seção 4).

## 1. Quem já tem ataque em área

Só existe um golpe em área inimigo: a **Varredura** (`_varredura`): 80% do golpe em você e em cada aliado vivo
(comitiva, animal, servo), sem aviso. A tela anima como golpe em área (`agindo(..., area=True)`).

| Quem tem | Onde aparece |
|---|---|
| Ent Ancião, Hidra do Brejo, Rei Troll, Dragão de Gelo, Senhor da Guerra, Golem Primordial | guardiões de covil do mundo gerado (6 dos 10) |
| O antagonista | a Cidadela |

Nenhum inimigo comum, nenhum afixo e nada do Vale do Turvo tem golpe em área: os inimigos do Charco, do Bosque e
da capela (esqueletos, afogados, sanguessugas) e a própria Ilse (a Bruxa Afogada, que é a ficha do guardião do
pântano sem Varredura) atacam um alvo por vez. O que age sobre o grupo inteiro hoje é de outro tipo: Uivo e Grito de
Guerra fortalecem o bando inimigo; Invocar traz reforços.

**Quando é usada:** na vez do inimigo, um chefe tenta uma habilidade com 45% de chance (comum: 35%). Entre as que
fazem sentido agora (`quando`), sorteia uma; a Varredura sempre faz sentido. Com o alvo a um golpe da morte, só
valem as que ferem, e a Varredura fere. Sozinho (sem comitiva, animal nem servo), metade das vezes ela desiste e o
inimigo dá o ataque básico. Medido: 1,4 a 1,6 vez por luta de guardião (de 17 a 19 turnos), cerca de 8% das vezes em
que o guardião age.

## 2. Como os inimigos escolhem o alvo

`Combate.escolher_alvo_inimigo`, nesta ordem:

1. Um aliado provocando (o urso do Patrulheiro, rugindo): sempre o alvo; para um chefe, metade das vezes.
2. Quem protege (Morel, `protege` na ficha): 30% das vezes, 40% com aprovação 45 ou mais; chefes, a metade disso.
3. Com aliados por perto: 25% de chance de um aliado ao acaso (45% com o urso na luta; chefes, 15%).
4. Senão, você.

A habilidade de um alvo usa esse alvo; a Varredura ignora o alvo e atinge todos de uma vez.

## 3. O que protege o grupo hoje

- **Do herói, nada protege os aliados.** Erguer Escudo, Passo Ágil, Barreira Arcana e Desaparecer são todos em si
  mesmo. O guerreiro não cobre ninguém; o mago não estende a barreira.
- **Da comitiva:** Morel atrai golpes (e recebe metade do dano dos companheiros em lutas comuns, tabela abaixo);
  Odette cura quem está abaixo de 40%; o urso provoca; o servo do Necromante atrai golpes.
- **Itens:** poções e bandagens podem ir num companheiro durante a luta.
- **Contra golpe anunciado:** o Golpe Esmagador (esmagar) já avisa um turno antes; atordoar interrompe; guarda,
  barreira e esquiva reduzem ou evitam (só para quem os usa: você).

Ou seja: contra um ataque em área, hoje a única resposta é matar mais rápido e curar depois. Não existe uma decisão de
proteger o grupo no momento do golpe.

## 4. Quanto ameaçam os companheiros (medido)

`python -m tests.area_inimigos` (30 lutas por classe em cada linha; Berserker, Patrulheiro e Piromante dos heróis da
arena de equilíbrio, cada um com um companheiro de aprovação 30; a região um nível abaixo do herói e o guardião um
acima, como no equilíbrio). Os guardiões com e sem a Varredura são os mesmos, com as mesmas sementes.

| Luta | Lutas | Vitórias | Dano na comitiva | Companheiro cai | Turnos | Varreduras/luta | Dano da comitiva vindo da Varredura |
|---|---|---|---|---|---|---|---|
| nv 3, comuns | 90 | 96% | 35% | 12% | 7.3 | 0.0 | 0% |
| nv 3, comuns, com Odette | 30 | 97% | 32% | 7% | 7.3 | 0.0 | 0% |
| nv 3, comuns, com Morel | 30 | 100% | 49% | 3% | 4.9 | 0.0 | 0% |
| nv 3, comuns, com Yara | 30 | 90% | 31% | 27% | 9.8 | 0.0 | 0% |
| nv 3, guardião | 90 | 29% | 28% | 8% | 18.7 | 1.5 | 34% |
| nv 3, guardião sem a Varredura | 90 | 32% | 24% | 12% | 19.2 | 0.0 | 0% |
| nv 5, comuns | 90 | 83% | 44% | 21% | 7.9 | 0.0 | 0% |
| nv 5, comuns, com Odette | 30 | 87% | 43% | 10% | 7.1 | 0.0 | 0% |
| nv 5, comuns, com Morel | 30 | 77% | 48% | 27% | 9.0 | 0.0 | 0% |
| nv 5, comuns, com Yara | 30 | 87% | 41% | 27% | 7.7 | 0.0 | 0% |
| nv 5, guardião | 90 | 53% | 33% | 17% | 16.7 | 1.6 | 42% |
| nv 5, guardião sem a Varredura | 90 | 60% | 29% | 17% | 17.9 | 0.0 | 0% |
| nv 8, comuns | 90 | 70% | 41% | 21% | 7.1 | 0.0 | 0% |
| nv 8, comuns, com Odette | 30 | 73% | 37% | 13% | 6.6 | 0.0 | 0% |
| nv 8, comuns, com Morel | 30 | 63% | 49% | 30% | 7.0 | 0.0 | 0% |
| nv 8, comuns, com Yara | 30 | 73% | 34% | 20% | 7.7 | 0.0 | 0% |
| nv 8, guardião | 90 | 40% | 32% | 17% | 17.3 | 1.4 | 37% |
| nv 8, guardião sem a Varredura | 90 | 53% | 29% | 19% | 18.7 | 0.0 | 0% |

Leitura (o robô da arena luta sem fugir e sem a decisão de uma pessoa: as vitórias servem para comparar linhas, não
como a dificuldade do jogo):

- **A comitiva já apanha bastante sem área nenhuma.** Em lutas comuns, de 31% a 49% do dano dos inimigos vai para o
  companheiro (Morel, que atrai, perto da metade; Odette e Yara, de 31% a 43%), e ele termina a luta caído em 3% a
  30% das vezes. Mais pressão sobre a comitiva não é uma lacuna: ela já existe, só não é uma decisão.
- **A Varredura muda pouco a parte da comitiva** (mais 3 a 4 pontos), mas é de onde vem um terço a quatro décimos do
  dano que o companheiro recebe nos guardiões. Ela pesa mais em **você**: como atinge todos com 80%, o total que sai
  dela passa de um golpe inteiro, e acerta você sempre (o golpe de um alvo vai para um aliado em parte das vezes).
  Com ela, os guardiões vencem mais vezes (nv 5: 47% contra 40% das lutas; nv 8: 60% contra 47%).
- **O companheiro cair não depende dela:** de 8% a 19% com ou sem, dentro do que varia entre as amostras.
- **Nada disso existe no primeiro capítulo:** no Vale (níveis 1 a 4), nenhum inimigo tem golpe em área.

## 5. Candidatos coerentes (inimigos fortes)

Coerentes pela ficha e pelo nível (todos fora do Vale, a não ser o último):

| Inimigo | Nível mínimo | Por que cabe | Forma sugerida |
|---|---|---|---|
| Troll (comum) | 4 | gigante, clava; o Rei Troll já tem a Varredura | golpe amplo anunciado, no lugar de um dos turnos de Golpe Esmagador |
| Golem | 4 | construto pesado | pisão que treme o chão (anunciado), em vez de um segundo golpe preparado |
| Abominação | 6 | corrompido, gigante, já envenena | vômito ácido: veneno em todos, pouco dano direto |
| Cavaleiro Sombrio | 6 | lâmina longa, blindado | corte em arco anunciado |
| Cão infernal | 3 | demônio de fogo | sopro em leque: queimadura em todos, com dano baixo (nível 3 pede cuidado) |
| Ilse (guardiã do Vale) | — | a canção de ninar já está na cena | a canção como efeito no grupo (enfraquecido ou atordoar curto), anunciada; só depois de jogar o fim do capítulo |

Não recomendados: lobos, aranhas, bandidos, sapos, sanguessugas, ratos, esqueletos e afogados (comuns e frequentes:
área neles seria dano espalhado em toda luta, sem decisão); a Bruxa do Brejo (nível 2, aparece cedo e já cura e
amaldiçoa).

## 6. Habilidade anunciada, não ataque básico frequente

**Recomendação: anunciada.** Um golpe em área deveria seguir o modelo do Golpe Esmagador, que o jogo já tem (o inimigo
avisa um turno antes, `carregando`; a ficha diz o que interrompe): o inimigo prepara, a carta e o texto dizem que vai
atingir todos, e a pessoa tem um turno para responder. Rara (um uso a cada tantos turnos), só em quem é forte (elite,
guardião, comuns de nível 4 ou mais).

Por quê:

- Um ataque básico frequente em área espalha dano em toda luta: a comitiva cai mais e o descanso e a cura ficam
  mais caros, sem que a pessoa tenha feito nada de diferente. É "enfraquecer a comitiva sem avaliação".
- Anunciado, ele cria a decisão que falta hoje (seção 3): atordoar para interromper, afastar ou curar quem está baixo,
  ou proteger o grupo.
- A Varredura atual dos guardiões é o contrário disso (sem aviso, sorteada entre as outras habilidades): é a primeira
  candidata a virar anunciada, sem mudar quem a tem.

**Condição para a proteção do grupo importar:** hoje não há uma ação do herói que proteja os aliados (seção 3). Antes
de aumentar a pressão em área, vale decidir qual será essa ação, por exemplo, uma das habilidades de proteção que já
existem se estendendo à comitiva por talento (o escudo do guerreiro cobrindo quem está atrás, a barreira do mago em
outro alvo), ou uma ordem a Morel ("cobrir o grupo") quando o inimigo prepara o golpe. Sem isso, o ataque anunciado
só ensina a matar mais rápido.

## 7. Próximos passos propostos (nada feito)

1. Jean decide se quer a pressão em área e em que ordem: (a) a Varredura dos guardiões passa a ser anunciada; (b)
   uma ação de proteção do grupo para o herói (ou para Morel); (c) um ou dois candidatos da seção 5.
2. Cada passo medido antes e depois com `python -m tests.area_inimigos`, `python -m tests.equilibrio` e
   `python -m tests.replay`, como os outros números de dificuldade (docs/COMO_CRIAR.md).
3. Nada disso no Vale enquanto a E9 estiver aberta.
