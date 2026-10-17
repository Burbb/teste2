# 23 — Plano de arte, interface, combate e próximos sistemas

Atualização aprovada por Jean em **17/10/2026, horário de Brasília**.

Este é o plano operacional de sequência para as próximas entregas de **The Unquiet**. Consolida a conversa de
direção de arte e os acréscimos de clareza do combate. A visão geral está em [docs/ROADMAP.md](../docs/ROADMAP.md);
a passagem de sessão, em [00-COMECE-AQUI.md](00-COMECE-AQUI.md).

**Aprovar a direção ou a ordem não aprova automaticamente um protótipo, um desenho ou uma regra de jogo.**
Executar a entrega solicitada por Jean, apresentar a proposta quando previsto e registrar o que de fato entrou.
Não iniciar todo o plano numa única tarefa. As etapas técnicas A–I e a validação E9 mantêm seus próprios critérios.

## Estado de referência

- Produção consultada: **1.110.0**, integração do gibão e das botas em `3c63546`.
- Branch: `claude/tender-einstein-tx3tjl`.
- Referência documental posterior consultada: `ab3a2b6`, diagnóstico da duração dos testes.
- Leitura estática nesta organização; nenhum teste ou percurso do navegador foi executado por esta atualização.
- **Cabeça e mãos (couro e tecido): aprovados visualmente por Jean em 17/10/2026, ainda não integrados.** O capuz
  de couro revisado (rodada 2), a luva de couro com braçadeira (rodada 1), a luva de seda (rodada 2) e o capuz de
  tecido da rodada 3 (`1c061e1`), em `ferramentas/prototipos/hud/couro2-aseprite/`. Pendentes, numa entrega separada:
  os tamanhos 40 e 48 derivados da fonte aprovada e a integração, incluindo a compatibilidade dos itens dos saves
  antigos (proposta de migração no `LEIA-ME.md` da proposta).

### Base já consolidada

A HUD de ferro e carvão, os seletores de Habilidades e Itens em faixas, os retratos dos heróis e da comitiva, a
fogueira como cena do topo e as cenas da Capela Afogada já estão no jogo. Permanecem como referência; não são pedidos
para refazer essas entregas.

Itens já trabalhados/integrados incluem martelo, Pena de Fênix, escudo, Unguento de Prata, machado, Bomba de Fumaça,
arco, cajado, orbe, grimório de equipamento, varinha, gibão e botas. Isto não significa que todo o catálogo nem todos
os usos dos sprites estejam migrados. Conferir `Icones` e os catálogos antes de cada lote.

## Ordem imediata

| Ordem | Entrega | Situação e limite |
|---|---|---|
| 1A | Concluir o lote de cabeça/capuz e luvas de couro e tecido | 32 e 64 aprovados visualmente; 40, 48 e integração (com os saves antigos) pendentes, entrega separada |
| 1B | Corrigir a sequência visual do consumo de recurso e mostrar o bloqueio de vida máxima por ferimentos | Prioridade de clareza; reproduzir e avaliar a apresentação |
| 1C | Prototipar dado mais visível, iniciativa e indicação dos turnos; facilitar consulta aos testes de atributos | Direção aprovada; composição e movimento ainda serão avaliados |
| 1D | Retomar os lotes de equipamentos e demais ícones | Pequenos grupos por função; aproveitar os componentes aprovados |
| 2–9 | Telas, serviços, cenários, habilidades e campanha | Sequência detalhada abaixo |

A etapa 1 não precisa terminar todo o catálogo antes de tratar um defeito de compreensão no combate.
Concluir o lote em andamento antes de iniciar outra exploração visual.

## 1. Itens, ícones e clareza do combate

### 1.1. Linguagem visual e processo dos itens

- Preservar a atmosfera dos cenários minimalistas, com formas legíveis, materiais convincentes e luz com origem.
- Os placeholders não obrigam o novo desenho a repetir cores ou recortes arbitrários. Preservar o tipo, a função
  e os materiais definidos nos dados; qualquer mudança de conteúdo deve ser discutida separadamente.
- Equipamento inicial pode ter arte bem acabada, com construção simples e poucos adornos.
- A representação do objeto no cenário e na HUD pode ter enquadramento e detalhe diferentes, mas deve manter
  identidade: forma principal, materiais, partes importantes e cores reconhecíveis.
- Usar a skill `.claude/skills/arte-itens-fenda/`, as fontes editáveis e o fluxo verificado do Aseprite/MCP.

**Processo atual, sem obrigar redesenho em todas as resoluções:**

| Uso/tamanho | Padrão para os próximos itens |
|---|---|
| 32 | Arte principal, avaliada no tamanho real e no jogo |
| 64 | Testar e preferir ampliação exata 2× quando aprovada, sem suavização |
| 40 e 48 | Derivar da fonte aprovada; retocar contorno, espessura e detalhe apenas quando a escala fracionária prejudicar a leitura |
| Versão maior específica | Exceção quando o ganho visual justificar; comparar antes de aprovar |
| @2x | Duplicação exata dos pixels de cada arquivo final |

Gibão e botas são o exemplo aprovado do 64 derivado do 32. As fontes de 40 e 48 deste lote permanecem as aprovadas.
Os 64 trabalhados separadamente ficam no histórico. **Não substituir retroativamente os 64 dos itens anteriores**:
fazer uma comparação própria no saque antes de decidir.

O jogo depende dos PNGs de produção, não do editor, do MCP ou de pastas de protótipos. Mapear imagens pelo papel no
`Icones`; um sprite compartilhado entre equipamento e habilidade não autoriza trocar os dois usos de uma vez.

### 1.2. Lotes de arte a completar

| Grupo | Escopo |
|---|---|
| Equipamentos | Fechar cabeça, mãos e pernas de couro e tecido, armas e demais lacunas reais do catálogo |
| Objetos da bolsa | Consumíveis e itens restantes; estados vazios/esgotados quando houver uso real |
| Atributos | Ataque, Defesa, Agilidade e Poder |
| Vida e recursos | Ícones de HP, Mana, Vigor, Foco, ouro, flechas e demais recursos do topo |
| Navegação | Ícones dos caminhos/destinos e símbolos internos do mapa; auditar os dois contextos |
| Interface e ações | Ícones remanescentes da doca, ficha, opções e ações; conferir o que já está aprovado antes de refazer |
| Criaturas | Mobs, chefes e pets/animais; aparência compatível com o mundo e leitura nas cartas, painéis e cenários pertinentes |
| Talentos | Ícones que expressem a função e se distingam na árvore; não alterar os efeitos para combinar com o desenho |
| Habilidades e estados | Articular com a etapa 8; não refazer em massa agora os ícones de poderes cujo conceito poderá mudar |

Este é um levantamento de escopo, não a afirmação de que todos esses ícones estão ausentes ou ruins.
Criaturas e retratos exigem avaliação própria; o processo dos objetos não obriga a mesma resolução de origem para
todo rosto ou sprite. Reconhecimento, identidade e peso visual no tamanho de uso continuam sendo os critérios.

**Capa de Patrulha:** ganhará desenho próprio no lote de capas. Na 1.110.0 compartilha temporariamente o gibão,
como registrado no roadmap. Conferir também os demais compartilhamentos de bases e únicos para não transformar
uma limitação antiga de mapeamento numa regra artística permanente.

### 1.3. Prioridade: consumo do recurso antes das consequências

**Relato de Jean:** ao usar uma magia, o roubo de vida aparece antes de a Mana diminuir, criando um intervalo entre
a execução e a percepção do custo.

**O que foi conferido no código:** `rpg/combate/heroi.py`, em `menu_habilidades`, desconta recurso e flechas antes
de executar a habilidade. O lance de ação é emitido em `rpg/combate/luta.py`; a ponte e `batalha.js` apresentam a
sequência. Isso é leitura estática, não reprodução do defeito nem prova da causa exata na interface.

**Resultado desejado:** ação confirmada → custo percebido no início da execução → golpe/efeito → consequências,
respeitando a ordem real do motor para roubo de vida, espinhos, contra-ataques, mortes e curas.

- Reproduzir e observar as barras do topo e da carta; localizar o momento em que cada atualização chega.
- Não antecipar custo enquanto a mira ainda pode ser cancelada.
- Não mudar contas, sorteios, gatilhos ou ordem das reações para maquiar a apresentação.
- Evitar pausas adicionais, redesenhos de barras sem mudança real e descontos visuais duplicados.
- Conferir habilidades de alvo único, área, cura/buff e custos combinados do Arqueiro, quando pertinentes;
  cancelamento, repetição rápida, movimento reduzido e a ação seguinte.
- Manter o gabarito sem alteração de partidas; se for necessário ampliar dados de apresentação, explicar o diff.

### 1.4. Protótipo: dado e tirinha mais visíveis

Jean gosta do dado e da tirinha existentes. A direção aprovada é experimentar uma posição de maior destaque,
preferencialmente no centro da coluna principal durante a resolução, preservando sua identidade.

- Nome do teste, dificuldade, dado, bônus e total devem ser compreensíveis.
- A emoção vem da antecipação e do resultado, com som e destaque curtos; não de prolongar todas as rolagens.
- Preservar a consequência e a leitura do evento; não acrescentar um Continuar obrigatório só para fechar o dado.
- Não cobrir texto, controles ou informações necessárias à decisão.
- Não sortear novamente, fabricar quase-sucessos nem alterar a ordem do RNG para a animação.
- Conferir mouse, teclado, clique rápido, janela baixa, movimento reduzido e reentrada/carregamento quando aplicável.

A posição e a duração exatas ainda dependem do protótipo. Não mover todas as notificações para o centro.

### 1.5. Protótipo: iniciativa e passagem dos turnos

**Iniciativa:** destaque breve de entrada e indicador compacto no topo da arena enquanto a oportunidade estiver
disponível, com uma mensagem como “Sua ação extra”. A proposta de card permanentemente no centro não foi escolhida.

O comportamento atual é uma ação extra só do herói; comitiva e animal entram depois. O estado e o bônus vêm do
motor e cessam na oportunidade correta. Não manter “Iniciativa” depois de consumida nem sugerir benefício de toda a
comitiva ou da luta inteira. Se mostrar o bônus, usar o valor real e suas condições.

**Turnos:** testar um aviso curto “Turno N”, que desaparece, mais uma indicação discreta do número atual.
- Definir claramente o ciclo contado, distinguindo turno do combate de cada ator agindo.
- Partir da numeração e dos eventos reais; não criar um contador paralelo de animação.
- A abertura de iniciativa, os turnos perdidos e a entrada/saída de aliados não podem gerar anúncio duplicado.
- Não bloquear ações nem acrescentar uma espera a cada turno.
- Não cobrir cartas, vida, mira ou seletores.

Dado, iniciativa e turno podem compartilhar uma família visual, com intensidades distintas. Conferir que avisos não
se empilham sobre o mesmo ponto da tela nem competem com dano e efeitos.

### 1.6. Consulta aos testes de atributos

**Direção aprovada:** tornar consultáveis o bônus atual e sua composição numa seção “Testes” da ficha detalhada,
sem colocar seis novos números permanentemente na HUD principal.

Estes são testes derivados, não seis novos atributos distribuíveis. O estado já prepara `testes` com `mod` e
`partes` em `rpg/web/estado.py`; auditar o acesso atual antes de criar uma segunda fonte.

| Teste | Regra atual consultada em `rpg/sistemas/testes.py` |
|---|---|
| Força | Nível e contribuição do Ataque |
| Destreza | Nível e contribuição da Agilidade, com fator próprio |
| Arcano | Nível e contribuição do Poder |
| Percepção | Nível, contribuição da Agilidade e bônus aplicáveis de classe/especialização |
| Vontade | Nível e contribuição da Defesa, com fator próprio |
| Carisma | Nível e contribuição da Reputação |

Bônus específicos de classe/especialização e penalidades se aplicam conforme os dados. Hoje o Arqueiro tem +3 em
Percepção e o Patrulheiro acrescenta +2; a escuridão penaliza Percepção e Destreza. A contribuição dos atributos tem
retorno decrescente, e a dificuldade também progride com o nível.

Esses números são constatação da versão consultada, não valores para copiar à mão na interface. Mostrar os dados
reais do motor, incluindo penalidades. Explicar a relação com os atributos e o nível, sem prometer que cada +1 de
Agilidade dá sempre +1 em todo teste. Preservar a regra do d20 e as exceções de 1/20 naturais.

### 1.7. Vida máxima reduzida por ferimentos

**Pedido adicional de Jean (17/10/2026):** tornar visível a capacidade de vida perdida por ferimento. A barra deve
poder estar cheia até o limite atual sem parecer que o personagem está com toda a sua capacidade saudável.
Exemplo sugerido: 45 de vida, limite atual de 45, capacidade sem a penalidade de 65.

**Direção para o protótipo:** a largura útil representa a capacidade sem as penalidades de vida máxima em questão;
dentro dela, distinguir três situações:

| Parte da barra | Significado |
|---|---|
| Preenchida | Vida que o personagem tem agora |
| Vazia e recuperável | Dano que pode ser curado até o limite atual |
| Bloqueada, no fim | Capacidade indisponível enquanto o ferimento/penalidade durar |

A parte bloqueada precisa de um tratamento próprio (por exemplo, hachura, tom dessaturado e marca de limite), além
de cor, para não parecer apenas dano comum. Definir o desenho no protótipo, com a linguagem da HUD atual.

| Exemplo | Vida atual | Limite atual | Capacidade sem a penalidade | Recuperável por cura | Bloqueada |
|---|---|---|---|---|---|
| Cheio até o limite do ferimento | 45 | 45 | 65 | 0 | 20 |
| Ferido e também com dano | 30 | 45 | 65 | 15 | 20 |
| Sem penalidade nem dano | 65 | 65 | 65 | 0 | 0 |

Jean sugeriu “45/65” mesmo quando cheio até o limite. Esse formato pode ser testado, **acompanhado da indicação
“−20 de vida máxima” ou “Limite atual: 45”** e da área bloqueada, para não prometer uma cura impossível.
A dica deve explicar vida atual, limite atual, capacidade sem a penalidade e a causa; o texto definitivo e sua
posição ainda dependem de avaliação. Uma barra apenas vazia com “45/65” não comunica sozinha a restrição.

- Os limites e a causa vêm do motor. A capacidade de referência acompanha nível, equipamentos, talentos e as
  regras atuais; não é um valor fixo da criação do personagem nem uma reconstrução aproximada na interface.
- Conferir fome e outras penalidades acumuladas antes de decidir quais entram na capacidade de referência.
  A soma visual deve explicar os valores reais, sem atribuir todo bloqueio a um único ferimento por suposição.
- Conferir as barras e números do topo, da carta do herói e dos demais contextos que apresentem sua vida.
  Não aplicar automaticamente a mesma representação a inimigos, pets e companheiros sem requisito e dados.
- A cura comum preenche só a parte recuperável; a apresentação não muda as regras de cura, tratamento ou vida
  concedida ao remover uma penalidade. Recurso Mana/Vigor/Foco não é abrangido automaticamente por este pedido.
- Conferir dano, cura no limite, tratamento, fome se aplicável, troca de equipamento, evolução e salvar/carregar;
  janela baixa, teclado/dicas e movimento reduzido.
- Preservar o estado após cada evento e evitar pulos ou animações de “ganho de vida” sem ganho real.

Entra na prioridade **1B**, junto da clareza do consumo de recurso, antes dos protótipos de avisos de 1C.
Ainda é uma direção documentada: não houve implementação nem teste do protótipo nesta atualização.

### 1.8. Protótipo: os comandos da luta na linguagem do seletor (pendente de avaliação)

**Pedido de Jean (17/10/2026):** aproximar Atacar, Habilidades, Itens e Fugir do seletor D refinado (Clair Obscur como
referência de tratamento; o seletor do jogo como referência de implementação), com uma variação de acabamento contido
das cartas e uma amostra só nas escolhas de um lugar selvagem (Explorar, Acampar, Viajar).

**Feito, só no protótipo** (`ferramentas/prototipos/hud/comandos/`, `fotografar_comandos.mjs`, `comparar_comandos.py`;
detalhes e fotos no `LEIA-ME.md` de `ferramentas/prototipos/hud/`): os comandos como faixas curtas de pincel com as
pontas do próprio seletor, tecla, ícone e nome numa peça só, os estados do seletor e o aberto em latão; as cartas com
uma aresta só de latão na vez do herói; a amostra da exploração em faixas que acompanham a altura do texto. Conferido
em 1500×950, 1280×720 e 1920×1080 (e a exploração também a 125%), de dia, à noite, com comitiva e vários inimigos.

**Ainda não é decisão:** o jogo não mudou; integrar, ajustar ou descartar depende da avaliação de Jean. As perdas
anotadas (as faixas somem à noite, a folga menor até os inimigos em 1280×720, o peso maior das faixas na exploração)
entram nessa avaliação. Não virar regra de skill antes disso.

**Avaliação de Jean (17/10/2026):** direção visual aprovada (faixas curtas de pincel; tecla, ícone e nome juntos, sem
o nicho preto; os ícones; as cartas contidas; as faixas da exploração). **Rodada 2, só no protótipo:** o carvão dos
comandos mais presente à noite (um tom acima, quase opaco, com um fio de luz no alto); a opção de duas linhas da
exploração numa pincelada só (as pontas escalam pela altura; a ação real da Capela com os riscos embaixo, 81 px); o
aviso da cena ("Inimigos +1 nível") numa faixa própria no canto direito da arena, sem cobrir o Fugir. Conferido antes ×
depois nas três janelas, de dia, à noite, com o bando (comitiva cheia e 5 lobos). **Achado anterior ao protótipo:**
com 5 inimigos em 1280×720 e 1500×950, os comandos e a caixa da mira ficam sobre cartas inimigas (o jogo de hoje já
faz isso); pede uma entrega própria. Detalhes no `LEIA-ME.md` de `ferramentas/prototipos/hud/` ("Rodada 2").
Pendente: a avaliação final de Jean; nada entrou no jogo.

## 2. Telas de leitura, criação e celebrações

- **Subida de nível:** preservar a boa organização das informações, redesenhando o acabamento para a linguagem atual.
  Manter a sensação de conquista com som, luz e movimento, sem depender do feixe suave com aparência renderizada.
  Testar feixes e partículas em pixel art e tags/faixas para os ganhos; posição e formato ainda são propostas.
- **Celebrações e raridade:** harmonizar o tratamento dos efeitos, com intensidade proporcional ao acontecimento.
  Respeitar movimento reduzido sem fazer o aviso desaparecer antes de poder ser percebido.
- **Grimório da interface:** aparência do livro aberto, páginas, leitura e navegação.
- **Livro narrativo da capela:** apresentação imersiva do relato. É outro objeto/contexto que o grimório equipado.
  A revisão visual não autoriza reescrever a história agora.
- **Criação de personagem:** clareza e apresentação. Retratos adicionais por classe, quantidade, seleção e possível
  recoloração continuam em aberto; não iniciar um editor completo de rosto/corpo por suposição.
- Revisar componentes antigos restantes por evidência, preservando os já aprovados.

## 3. Interior da forja

Criar o ambiente e o ferreiro como cena própria, tomando a capela como referência de atmosfera, iluminação e
interação. Começar com as regras existentes. A arte não depende de aprovar primeiro um sistema novo de reforço.

## 4. Protótipo do reforço e encantamento

Objetivo: decisões compreensíveis e uma resolução prazerosa, com feedback visual e sonoro.

**Hipóteses, não regras fechadas:** reforçar melhora atributos físicos; encantar acrescenta propriedade especial;
materiais podem ser encontrados na aventura; poucos tipos iniciais; reforços iniciais garantidos e risco mais tarde;
começar investigando sem destruição nem perda dos reforços já conquistados.

Chances, custos, limites, perdas e fontes dos materiais precisam de protótipo e avaliação. Mostrar custo, chance e
consequência de forma clara; a animação celebra o resultado real. Brilhos e marcas de +1/+2 etc. devem comunicar
estado, não tornar toda a bolsa um conjunto de efeitos permanentes. Não confundir cor do encantamento com raridade.

## 5. Interiores dos serviços da vila

Criar **Templo/igreja, Curandeira e Taverna**. A Taverna faz parte desta etapa por pedido explícito de Jean.
Cada interior terá composição e identidade próprias, preservando serviços, disponibilidade, tutorial e regras até
que uma mudança de sistema seja solicitada. Não fazer três cópias da capela.

## 6. Cenários do mapa e acontecimentos principais

Revisar bosques, charcos, ruínas e demais lugares conforme o que o texto descreve. Incluir os entornos próprios do
acampamento que ainda usam a paisagem genérica de cada lugar; o entorno da capela já foi feito.

Criar cenas para acontecimentos relevantes, como Caspar na praça. Antes de produzir uma cena cara, conferir se o
acontecimento será mantido na revisão da campanha. A futura história informa essa seleção sem exigir reescrever toda
a campanha antes de melhorar os lugares existentes.

## 7. Eventos recorrentes da estrada

Representar mercadores, viajantes vendendo objetos, pessoas feridas e outros eventos frequentes. Preferir
composições reutilizáveis com variações coerentes quando isso evitar trabalho repetido. Preservar escolhas e
consequências; cenário interativo não precisa virar exploração por movimento.

## 8. Habilidades, animações e liberdade de build

- Revisar ícones e animações de habilidades e efeitos, com leitura das fontes, alvos, custos e consequências.
- Prototipar preparação de habilidades em locais seguros: vila e acampamento.
- Hipótese inicial: até seis habilidades preparadas, no máximo uma elite, mantendo Atacar/Itens/Fugir separados.
- Quantidade de espaços, definição de elite/ult, custos por pontos, tiers, restrições e equilíbrio não estão fechados.
  A ideia de pontos é uma alternativa a avaliar, não outra regra para acumular automaticamente.
- Testar os ícones preparados na HUD, sua posição e formatos (inclusive losangos) antes de decidir layout.
- Novas habilidades fortes pedem custos, oportunidade e legibilidade compatíveis; não ampliar o catálogo em massa
  antes de validar o sistema.
- Retomar [21 — Ataques em área](21-DIAGNOSTICO-ATAQUES-EM-AREA.md): habilidades anunciadas para inimigos fortes e
  possibilidades de proteção do grupo precisam conversar. O diagnóstico existente não é implementação aprovada.

## 9. Expansão e reescrita da campanha

Trabalhar depois das prioridades anteriores. A discussão está preservada em
[22 — Ilse e a água](22-HISTORIA-ILSE-E-A-AGUA-RASCUNHO.md), como rascunho, não cânone implementado.

Direção em estudo: substituir o eixo dos Sigilos por uma história centrada em Ilse, água abundante sustentada pelo
sofrimento dela, o sacerdote e a responsabilidade da vila que descobre e aceita a troca. Desenvolver o vínculo com
Ilse antes da revelação e os papéis de Berta, Caspar, Yara e dos moradores. Decidir pistas, alternativas e consequências
sem uma solução perfeita automática.

Conferir dependências de livro, Diário, missões, flags e saves. A etapa técnica I (mundo e narrativa como dados)
volta à pauta quando essa expansão exigir; não é uma migração de engine.

## Validação e critérios transversais

- A E9 e os testes com jogadores novos continuam abertos; não esperar todo o plano terminar para observar compreensão,
  ritmo e dificuldade. Teste técnico não aprova arte nem substitui essa validação.
- Distinguir **relato**, **leitura estática**, **reprodução**, **protótipo aprovado**, **integração** e **teste executado**.
- Mudança visual: conferir no jogo, em janela normal e baixa, mouse, teclado e movimento reduzido conforme o contexto.
- Motor decide regras e números; interface apresenta. Mudanças só de apresentação preservam sorteios e consequências.
- Preservar os gabaritos; atualizar apenas após mudança intencional conferida, conforme o `CLAUDE.md`.
- Windows: gabarito e roteiros principais já foram compatibilizados. A confirmação de execução no Linux permanece
  separada do que só foi executado no Windows.
- **Duração dos testes já esclarecida:** no diagnóstico de `ab3a2b6`, sem Playwright a suíte levou ~52 s e a fumaça
  ~488 s. Com Playwright disponível, `unittest` já inclui a fumaça; não repeti-la em seguida sem motivo.
  Isso não autoriza remover verificações. Seguir a orientação atual do `CLAUDE.md`.
- Roteiros de fotografia ainda não portados para Windows são pendência de ferramentas; conferir quais já foram
  corrigidos e migrar os usados nos próximos lotes. Não assumir que o total antigo de 29 continua exato.
- RTK ficou como experimento opcional futuro de filtragem seletiva de saídas, não pré-requisito nem proxy de API
  aprovado para o projeto. Preservar logs completos para diagnóstico.
- Atualizar este plano quando uma entrega mudar de estado, mantendo propostas recusadas no histórico e o código
  atual como referência da implementação.

## Próxima passagem de trabalho

1. Lote de cabeça/capuz e luvas: aprovado visualmente; falta a entrega separada dos 40/48 e da integração.
2. Integrar apenas os desenhos aprovados.
3. Reproduzir e corrigir a percepção atrasada do custo de recurso e apresentar o bloqueio de vida máxima por ferimentos (1B).
4. Prototipar os avisos e a consulta aos testes (1C), sem ampliar regras.
5. Retomar os lotes de ícones (1D) e depois a etapa 2.

Esta ordem substitui a descrição antiga que deixava toda a clareza do combate para a grande etapa de habilidades.
O plano não altera o jogo por si só.
