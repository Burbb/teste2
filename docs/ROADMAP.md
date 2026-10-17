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

## Apresentação, arte e clareza do combate (plano atualizado em 17/10/2026)

A sequência aprovada por Jean está detalhada em
[23 — Plano de arte, interface e combate](../roadmapIDEIAS/23-PLANO-DE-ARTE-INTERFACE-E-COMBATE.md).
Consultar esse documento antes de escolher a próxima entrega. A ordem está aprovada; os protótipos e as regras
ainda em aberto precisam de avaliação própria. Este plano não autoriza executar todas as etapas de uma vez.

**Referência consultada:** 1.110.0 (`3c63546`), com o diagnóstico dos testes em `ab3a2b6`.
Já estão no jogo a HUD nova, os seletores de Habilidades e Itens em faixas, os retratos, a fogueira como cena do
topo e a Capela Afogada. O martelo, Pena de Fênix, escudo, unguento, machado, bomba, arco, cajado, orbe, grimório,
varinha, gibão e botas já receberam arte trabalhada; conferir as lacunas reais no catálogo e no `Icones`.

| Etapa | Próximas entregas | Situação |
|---|---|---|
| **1A** | Concluir candidatos de cabeça/capuz e luvas da família de couro | Pedido enviado; ainda depende da proposta e avaliação |
| **1B** | Sincronizar o consumo visual de Mana/Vigor/Foco com o início da habilidade e mostrar a vida máxima bloqueada por ferimentos | Prioridade de clareza; reprodução e protótipo |
| **1C** | Prototipar dado/tirinha mais visíveis, iniciativa, passagem dos turnos e consulta aos testes de atributos | Direção aprovada; apresentação a avaliar |
| **1D** | Completar equipamentos e ícones de atributos, HP/recursos, ouro/flechas/bolsa, navegação/mapa, interface, talentos, mobs e pets | Lotes pequenos; habilidades/estados articulados com a etapa 8 |
| **2** | Level up e celebrações, Grimório aberto, livro narrativo da capela e criação de personagem | Proposta |
| **3** | Interior da forja e ferreiro, inicialmente com as regras atuais | Proposta |
| **4** | Protótipo de reforço e encantamento | Hipóteses, sem chances, custos, riscos ou limites finais aprovados |
| **5** | Interiores do Templo, da Curandeira **e da Taverna** | Proposta |
| **6** | Cenários dos lugares, entornos do acampamento e cenas principais da campanha | Proposta; conferir a permanência dos acontecimentos antes de produzir |
| **7** | Cenas dos eventos recorrentes da estrada | Proposta |
| **8** | Preparação de habilidades, novas habilidades, ícones e animações | Hipóteses a validar, incluindo proteção do grupo e ataques em área dos inimigos |
| **9** | Expansão e reescrita da campanha, a partir de Ilse e da água | Rascunho em [22](../roadmapIDEIAS/22-HISTORIA-ILSE-E-A-AGUA-RASCUNHO.md), não cânone implementado |

**Padrão atual dos itens:** 32 como fonte principal; 64 ampliado exatamente 2× quando aprovado; 40/48 derivados com
retoques necessários à leitura. Versão maior redesenhada é uma exceção avaliada, não uma obrigação. Gibão e botas
são o exemplo integrado (1.110.0). Os 64 dos itens anteriores ficam intactos até uma comparação própria.
Preservar a construção do mesmo objeto entre tamanhos; placeholder não é molde obrigatório.

**Clareza do combate:** o motor já desconta recurso antes da habilidade; investigar o atraso percebido na tela sem
mudar contas ou reações. Dado e tirinha preservados em uma apresentação mais visível; iniciativa com destaque de
entrada e indicador compacto enquanto vale; “Turno N” breve e número discreto. Evitar bloqueios, avisos sobrepostos
e contagem paralela. Percepção e Destreza são testes derivados: mostrar bônus e composição na ficha detalhada,
junto dos demais testes, usando dados do motor; não criar novos atributos distribuíveis.

**Vida máxima reduzida:** no protótipo de 1B, distinguir vida atual, dano recuperável e capacidade bloqueada pelo
ferimento. A barra pode usar a capacidade saudável como referência; “45/65” com limite atual 45 deve mostrar os 20
bloqueados e explicar a restrição, sem sugerir que uma cura comum os recupera. Valores vêm do motor e acompanham
equipamentos, nível e penalidades reais. Detalhes no item 1.7 do plano 23; não altera regras de cura ou tratamento.

**Hipóteses guardadas:** reforçar atributos físicos e encantar uma propriedade; poucos materiais encontrados no
mundo; investigar reforços iniciais garantidos e risco mais tarde, inicialmente sem destruir a peça ou perder
reforços. Preparar até seis habilidades na vila/acampamento, com no máximo uma elite; Atacar, Itens e Fugir fora
desses espaços. Pontos/tiers, quantidade final, formato e posição na HUD dependem de protótipo.

A referência dos serviços e cenários continua sendo a Capela Afogada: luz reconhecível, animação discreta e
interação coerente com o desenho. Fundos próprios dos demais acampamentos ficam na etapa 6.
A E9 e a validação com jogadores novos seguem abertas ao longo do plano.

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
