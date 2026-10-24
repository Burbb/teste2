# Roadmap

Onde estamos e para onde vamos. Atualize a cada etapa concluída.

## A meta

Um RPG de texto com a liberdade de Baldur's Gate: árvores de talentos enormes, centenas de habilidades,
especializações e especializações de elite, história com ramificações e personagens fixos, cidades e masmorras,
e cada partida diferente da anterior. Para chegar lá, primeiro um núcleo que aguenta escala.

## Refatoração do núcleo (antes de expandir)

Cada etapa mantém o gabarito de regressão idêntico: nada de jogo muda, só onde as coisas moram.

| Etapa | O quê | Situação |
|---|---|---|
| **A** | Habilidades como dados: blocos que executam e se descrevem; Grimório gerado; conta de crítico única | ✅ feito |
| **B** | Modificadores e gatilhos: talentos e passivas de especialização declaram "+x% de dano corpo a corpo", "ao matar", "no início da luta"... e o combate só pergunta `mod`/`disparar`. Zero `tal("...")` fora de `talentos.py` (eram 28 talentos em 5 arquivos). Chaves validadas por teste. Falta: itens e estados como fontes (hoje `especial()`), e as verificações de spec fora do combate (testes de atributo, eventos). | ✅ feito |
| **C** | Catálogo de estados (`rpg/estados.py`): nome, ícone e cor, mal ou bênção, dano por turno, perda de turno, imunidade, resistência, camadas e descrição. `aplicar` e `processar_efeitos` genéricos; a tela recebe ícones e dicas do motor; o Grimório descreve pelo catálogo. Falta: o efeito dos estados na conta de dano (fortalecido, guarda, marcado...) ainda é perguntado à mão em `atacar`; vira modificador junto com os itens. | ✅ feito |
| **D** | Rede de segurança: validador de conteúdo (toda referência entre catálogos existe: habilidades de famílias, afixos e fases, famílias dos biomas, lore, eventos, sprites dos ícones); o gabarito guarda também o estado que a tela recebe. Corrige os números que a auditoria achou errados na tela. Feito: `tests/test_conteudo.py`; linhas `ESTADO` no gabarito; clima como dado (`CLIMAS` com `dano`/`esquiva`/`queimadura`); custo, queimadura, tique, esquiva, selos do clima e bestiário lendo a conta do motor; Reviver com `quando`. | ✅ feito |
| **E** | Habilidades e talentos sem teto: árvore de talentos montada pelos dados (ramo + camada, sem limite de camadas nem de talentos lado a lado; `NIVEL_CAMADA`); ícone, cor, animação e realce nos catálogos (saíram `HAB_ICONE`, `ICONE_TALENTO`, os casos por nome em `batalha.js` e os nomes em `realce.js`); memória por luta genérica (`cb.memoria`, `uma_vez_por_luta`). Fica para quando os talentos vierem em massa: gatilhos montados com os blocos das habilidades (hoje são funções curtas, declaradas no talento), para a descrição sair dos números como no Grimório. | ✅ feito |
| **F** | Itens como dados: catálogo de consumíveis do qual saem todas as listas (uso na luta e fora, em aliado, mercado, ícone, contador do topo; a tela recebe o catálogo no estado); bases e únicos com ícone (fim da regex no nome), único com id fixo, item com nível; nomes raros concordando em gênero. Fica para o saque em massa: os nomes de espaço, raridade e atributo ainda repetidos em `telas/itens.js` (a comparação de itens é feita na tela). | ✅ feito |
| **G** | Inimigos como dados: regras da família na ficha (`nivel_min`, `escolta`, `revive`, `flechas`, `lore`); `noite` nos biomas; afixos com `sorteio` e `fenda`; catálogo de traços (`TRACOS_FICHA`: a conta de dano, o ícone e o retrato da criatura, que a tela recebia por funções em JS); guardiões com id estável no save. Fica para depois: dar às habilidades de inimigo ids próprios (hoje o Grito de Guerra do bandido divide o id com o do guerreiro; a animação já vem pelo `anim`). | ✅ feito |
| **H** | Estrutura: `combate.py` e `comitiva.py` em pacotes por responsabilidade (cada companheiro declara a própria ação em `ACOES`; as preces da Odette e a proteção do Morel na ficha); opções de sistema com meta (a tela não reconhece mais pelo texto); um escape de HTML só (`Texto.html`); auxiliares do front-end num lugar só (pontilhado, mistura de cores, `pct`, sprite); `telas.js` virou `telas/`, uma tela por arquivo, cada uma registrada no painel pelo tipo. O gabarito ganhou 6 sequências de lutas com companheiros (nenhuma partida de robô lutava com eles). `batalha.js` fica inteiro por ora: é uma tela só, o palco da luta. | ✅ feito |
| **I** | Mundo e narrativa como dados: flags com nome, facções, reputação por facção, missões com etapas; eventos e diálogos com condições e consequências declaradas; ramos alcançáveis. | quando a história começar |

A régua de cada etapa de D a H: o gabarito passa sem atualizar (refatoração pura). Quando a etapa só acrescenta
campos ao que a tela recebe, o gabarito muda e se confere que, tirando os campos novos, as partidas são idênticas.
Correção de jogo fica em commit separado, com o diff explicado.

Auditoria que motivou D–H (1.45): com o núcleo já em dados (A–C), o que trava "conteúdo em massa" são as bordas:
o teto da árvore de talentos, listas copiadas à mão entre arquivos (consumíveis, espaços, biomas, ícones), regras
especiais escritas na lógica (`familia == "caido"`, `cid == "morel"`, regex no nome do item) e arquivos que fazem
coisas demais (`combate.py`, `comitiva.py`, `telas.js`, `batalha.js`).

## Equilíbrio (1.13)

Réguas para mexer na dificuldade com números: o simulador por especialização e nível (`tests.equilibrio`), o
replay das partidas de verdade (`tests.replay`, com a do Xatuba em `tests/runs/`) e o `--dev N`. Primeiro ajuste:
base um pouco mais dura e a curva bem mais dura do meio para o fim (defesa que perde força contra inimigos de nível
alto, ataque e vida dos inimigos com curva, equipamento crescendo menos, XP mais lento e menor de inimigos fracos).
Em 1.14, o padrão virou hardcore com metas declaradas (em COMO_CRIAR): grupos maiores cedo, companheiro que custa
caro (mais inimigos e mais vida neles), inimigos mais duros desde a base, curva do meio mais forte e a do fim mais
plana (menos pico, mais desgaste); Paladino menos invulnerável, Barreira do mago crescendo com o Poder, servo do
Necromante que provoca. O simulador mede também "lutas até descansar".
Em 1.15: dano geral do herói ×0,9 e dos inimigos ×1,1; a iniciativa dá +25% no primeiro golpe (era crítico
garantido); a taverna devolve 35% da vida (era 65%), deixando o templo como a cura de verdade.
Pendente: passe por especialização (Paladino ainda fácil; Sombra, Piromante e Necromante duras no fim); um modo
mais brando para quem quiser; um robô de mapa que jogue partidas inteiras com juízo, para medir o ritmo de nível.

## Depois do núcleo

- Sistemas gerais (não de uma classe): reputação por facção, missões encadeadas, diálogo com testes de atributo
  como opções, consequências que voltam dias depois.
- Conteúdo: história fixa, personagens, mapa, cidades, masmorras com mapa interno.
- Classes: árvores grandes, novas especializações, elites.

## Apresentação, arte e clareza do combate (atualizado em 21/10/2026)

A sequência aprovada por Jean está detalhada em
[23 — Plano de arte, interface e combate](../roadmapIDEIAS/23-PLANO-DE-ARTE-INTERFACE-E-COMBATE.md).
Consultar esse documento antes de escolher a próxima entrega. Aprovar a ordem não aprova automaticamente
protótipos, desenhos ou regras e não autoriza executar todo o plano de uma vez.

**Estado confirmado nesta atualização (23/10/2026):** produção **1.200.0** (a 1E.4 integrada na 1.200.0: o mapa, o minimapa, a Viagem e o Diário na linguagem nova, os cinco lugares da campanha em grade nativa, e o bloqueio da viagem vindo da regra; a Ilse com a ficha dela, pelo id, na 1.199.3; o antagonista no gênero do título na 1.199.2; a família `esqueleto_servo` removida na 1.199.1; o Barqueiro do Charco preparado na branch `claude/barqueiro-do-charco`, fora da produção e suspenso, porque o Jean pretende retirar o modo procedural no futuro, depois de um levantamento próprio, ficando só a campanha; o Lich Menor na 1.199.0, pelo id do guardião; o Profeta das Cinzas na 1.198.0, pelo id do guardião; a Hidra do Brejo na 1.197.0, pelo id da guardiã; o servo esquelético na 1.196.0, pelo retrato que o Erguer Servo dá ao invocado; o Espantalho Possuído na 1.195.0, pela origem; o Senhor da Guerra na 1.194.0; o Dragão de Gelo na 1.193.0; o Mímico na 1.192.0, pela origem; o Golem Primordial na 1.191.0; a Árvore Anciã na 1.190.0; a Árvore Desperta e o Golem de pedra na 1.189.0; a Abominação na 1.188.0; o Cavaleiro Sombrio na 1.187.0, com o Último Guarda; o Cão infernal na 1.186.0; a Cria do Vazio na 1.185.0; a Harpia e o Xamã Caído na 1.184.0; o Grifo na 1.183.0; o Caído na 1.182.0; o Mercenário e o Lobo Gélido na 1.179.0; o ícone do Esgotado do mercado na 1.180.0; as árvores vivas renomeadas, Árvore Desperta e Árvore Anciã, com a migração dos saves, na 1.181.0; a fala da Pita depois do último tratamento na 1.181.1; antes, da 1.175.0 à 1.178.0, o Esqueleto, o urso e o falcão da fogueira, o cajado do Mago e correções de interface). A 1D está concluída: **31
equipamentos-base** finais (as variantes e os compartilhamentos provisórios ficam separados, ainda abertos). Na 1E, o
**contador de flechas** e os **17 estados** estão concluídos; o **Afogado, a Ilse, o Lobo e o Bandido** estão integrados,
e os **três animais do patrulheiro** (Urso, Falcão e Lobo Cinzento) concluídos. **A 1E concluída para a campanha** (a 1E.4 na 1.200.0; os retratos só do procedural suspensos). **Agora: a etapa 2.** As etapas 2–9 seguem,
com habilidades, talentos, Grimório e árvore juntos na etapa 8.

Histórico (19/10/2026): produção remota 1.145.0, espada e maça integradas em `ed967d1`; a 1D estava fechando os
equipamentos, com o elmo e a cota como o próximo par.

**Concluído:** clareza de custo, vida bloqueada, iniciativa/turnos e rolagem central; consulta aos testes;
atributos, nove atalhos da doca, principais recursos/consumíveis e grande parte dos equipamentos. A HUD de ferro e
carvão e os menus de pincelada continuam; o estudo com pintura permanente nas colunas/topo não foi escolhido.
A migração das artes e seus usos específicos consta no plano 23; não contar pintura reduzida como pixel art final.

| Etapa | Entregas | Situação |
|---|---|---|
| **1A** | Capuzes e luvas de couro/tecido, tamanhos e saves | **Concluída**, 1.112.0 |
| **1B** | Custo no início da ação e vida máxima bloqueada | **Concluída**, 1.114.1 e 1.115.0 |
| **1C** | Iniciativa/turnos, rolagem no centro e testes na ficha | **Concluída**, 1.116.0–1.118.0 |
| **1D** | Equipamentos, objetos da bolsa e ícones gerais | **Concluída**: 31 equipamentos-base finais (1.150.0; acabamentos até a 1.154.0); variantes e compartilhamentos provisórios separados, ainda abertos |
| **1E** | Desvio visual depois dos itens | **Concluída para a campanha na 1.200.0** (a 1E.4: o mapa, o minimapa, a Viagem e o Diário). Histórico: contador de flechas (1.155.0) e 17 estados (1.155.0–1.161.0) concluídos; Afogado, Ilse, Lobo e Bandido integrados (1.162.0–1.163.0); os três animais do patrulheiro concluídos (1.164.0–1.165.0); o Troll da montanha (1.166.0), o Rei Troll e a Aranha (1.167.0); a Rainha Aracnídea (1.168.0); o arco no Atacar do Arqueiro (1.169.0); o lobo na fogueira (1.170.0); o sapo e a sanguessuga (1.171.0); o cultista, a bruxa e o rato (1.172.0); o javali e o carniçal (1.173.0); o espectro (1.174.0); em andamento as demais criaturas, os chefes e as invocações (1E.3); depois caminhos e símbolos do mapa/minimapa (1E.4) |
| **2** | Menu de carregar e fichas dos saves, criação, livro da capela, dado, subida de nível, celebrações e raridade | Pendente; Grimório e árvore passam ao mesmo ciclo dos sistemas na etapa 8 |
| **3** | Interior da forja e ferreiro | Pendente; começar com as regras atuais |
| **4** | Protótipo de reforço e encantamento | Hipóteses; chances, custos, riscos e limites não aprovados |
| **5** | Interiores do Templo, Curandeira e Taverna | Pendente |
| **6** | Cenários dos lugares, entornos de acampamentos e cenas principais | Pendente; conferir a permanência dos acontecimentos |
| **7** | Cenas dos eventos recorrentes da estrada | Pendente |
| **8** | Habilidades/build, Grimório, árvore de talentos, ícones e animações | Pendente; definir/validar sistemas e produzir os ícones no mesmo ciclo, evitando arte para conceitos prestes a mudar |
| **9** | Expansão e reescrita da campanha, Ilse e a água | Rascunho em [22](../roadmapIDEIAS/22-HISTORIA-ILSE-E-A-AGUA-RASCUNHO.md), não cânone |
| **Depois** | Avaliação de refatoração/manutenção | Retomar por diagnóstico do código então existente; não interromper os lotes com limpeza geral |

**Prioridades novas de 19/10 (histórico; resolvidas: o contador de flechas na 1.155.0, o Firme e os outros 16 estados
até a 1.161.0):** o ícone da contagem de flechas na carta do Arqueiro ainda usa o sprite antigo
`flecha`, distinto da aljava já aprovada do topo. O estado Firme ainda usa `cadeado`; revisar sua representação da
proteção temporária contra nova perda de turno. Desenhos finais a avaliar; preservar regras e números.
Os demais buffs/estados não ficam esperando a revisão de habilidades. Criaturas e navegação já estavam no escopo;
agora têm uma posição explícita. O menu de carregar/fichas e a revisão visual da árvore também ficam registrados.

**Estado dos equipamentos (atualizado em 21/10):** os **31 desenhos-base são finais** desde a 1.150.0 (o histórico de
19/10 dizia 25 finais, com cinco peças de ferro e o 40/48 do martelo pendentes).
Compartilhamentos provisórios continuam registrados (Capa de Patrulha, Chapéu de Couro, Coroa dos Afogados), assim
como a nomenclatura da Sandália/Diadema. Não afirmar que só restam talentos e habilidades sem conferir o catálogo.

**Processo:** fontes editáveis e PNGs de produção independentes do protótipo; referência principal e comparação em
tamanho real; tamanhos conforme o contexto. Preservar os aprovados. Usar a janela principal de Jean e evidência
dirigida à alteração, sem repetir matrizes de resoluções ou baterias desnecessárias. Seguir o CLAUDE.md e evitar
rodar a mesma fumaça duas vezes por acidente.

**Hipóteses guardadas:** reforço de atributos físicos e encantamento de propriedades, com materiais e riscos a
validar; preparação de habilidades em vila/acampamento, hipótese de até seis com no máximo uma elite, sem decidir
quantidade, tiers, custos, pontos ou formato da HUD de antemão. A Capela Afogada continua referência de atmosfera
para os serviços/cenários. A etapa técnica I entra quando a narrativa a exigir; E9 e testes com jogadores seguem
abertos ao longo do plano.

## Ideias guardadas (não agora)

- Domar o grifo como quarto animal do Patrulheiro (com Ordem própria).
- Comida para o animal (descartado por ora: provisões ficariam apertadas demais).
- Ícones próprios para cada habilidade (entra na etapa 8 do plano de apresentação).
- Retratos do herói por classe (proposta da HUD experimental, 10/2026): uma seleção pequena, de início dois retratos
  por classe, escolhidos na criação do personagem. Só cosmético (nada de regra, número ou recoloração), no mesmo
  desenho da ficha, do topo e da carta da luta (busto e cabeça). Fora por ora: a tela de escolha na criação, os
  retratos por especialização e os seis retratos.
  Direção aprovada (10/2026): o Guerreiro de capacete fechado, sem rosto, desenhado em código no estilo dos cenários
  (um desenho só para o busto, a cabeça do topo e a carta; o teste em `ferramentas/prototipos/hud/retrato-teste.html`).
  No jogo desde a 1.90.0 (`rpg/web/static/retratos.js`); o Mago (capuz azul alto) e o Arqueiro (capuz verde curto com
  a aljava) desde a 1.91.0, em todos os lugares do herói (ficha, topo, carta, Inventário, fogueira, saves). Os
  companheiros (Morel, Odette, Yara) desde a 1.92.0, em todos os lugares deles (painel, Comitiva, carta e reação na
  luta, faixa de quem chega, aviso, chip de aprovação, fogueira); o Morel com o busto grande em 80×80. Cartas de
  combate (comparadas em `ferramentas/prototipos/hud/cartas-teste.html`): o critério é leitura, identidade e peso
  parecidos em 32 px, não a mesma resolução de origem nem a mesma proporção entre cabeça e ombros (os heróis, Odette e
  Yara com a carta de 16×16 a ×2; o Morel, desde a 1.96.0, com a figura de 16×16 da fogueira a ×2); vale para
  personagens futuros. Quantos
  retratos haverá e como o jogador vai
  personalizar o herói continuam em aberto (nem seleção, nem recoloração, nem diferença por gênero, nem as outras
  classes por enquanto); o retrato não segue o elmo equipado nem os atributos.
- Um desenho próprio para a Capa de Patrulha (peito do Arqueiro): desde a 1.110.0 ela usa o desenho do gibão de
  couro (um colete), como as outras bases do peito do Arqueiro; uma capa não é um colete. Sem mudar dados nem regras
  até lá.
- "Ordens" leves para a comitiva.
- Aliados na batalha final, repaginado (o sistema antigo saiu na 1.45: cada evento somava um aliado que tirava vida
  do chefe num texto antes da luta, invisível no resto do jogo). Se voltar: poucos aliados, ganhos por arcos
  inteiros (a comitiva, uma vila salva), que aparecem de verdade na luta final (carta na arena, uma ação ou
  habilidade própria), com o compromisso visível no Diário e a promessa cobrada (quem foi abandonado não vem).
- Armazém para guardar mais coisa, quando a gama de itens crescer (junto com o saque de ARPG: mais drop, mais
  variedade). Como Titan Quest (a Caravana) e Diablo/Path of Exile/Grim Dawn: só nas vilas, nunca no acampamento
  (a mochila de 12 é a tensão da viagem), e o mesmo conteúdo em todas as vilas (uma carroça de caravaneiro leva
  suas coisas de uma para outra). Outro nome que não "baú", para não confundir com o Baú Trancado (o saque que se
  abre na vila ou na fogueira, que fica). Junto dele, "Vender o lixo" no mercado (o jogo marca o que é comum e
  pior que o equipado, você desmarca o que quiser), com um plin por item.
