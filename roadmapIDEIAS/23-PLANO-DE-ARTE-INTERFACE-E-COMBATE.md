# 23 — Plano de arte, interface, combate e próximos sistemas

Plano inicial aprovado por Jean em **17/10/2026**; sequência e prioridades atualizadas por ele em
**19/10/2026, horário de Brasília**.

Este é o plano operacional de sequência para as próximas entregas de **The Unquiet**. Consolida a conversa de
direção de arte e os acréscimos de clareza do combate. A visão geral está em [docs/ROADMAP.md](../docs/ROADMAP.md);
a passagem de sessão, em [00-COMECE-AQUI.md](00-COMECE-AQUI.md).

**Aprovar a direção ou a ordem não aprova automaticamente um protótipo, um desenho ou uma regra de jogo.**
Executar a entrega solicitada por Jean, apresentar a proposta quando previsto e registrar o que de fato entrou.
Não iniciar todo o plano numa única tarefa. As etapas técnicas A–I e a validação E9 mantêm seus próprios critérios.

## Estado de referência — 21/10/2026

- Produção: **1.186.0** na branch `claude/tender-einstein-tx3tjl` (22/10/2026: o Cão infernal P1 pela família na 1.186.0; a Cria do Vazio A2 pela família na 1.185.0; a Harpia T2 e o Xamã Caído X1r2 pela família na 1.184.0; o Grifo GA3 pela família na 1.183.0; 23/10/2026: o Caído CA pela família, com os que o
  xamã ergue; 22/10/2026: o Mercenário MA e o Lobo Gélido LA pela
  família na 1.179.0; o caixote no motivo "Esgotado" do mercado na 1.180.0; o ent jovem e o Ent Ancião renomeados para
  Árvore Desperta e Árvore Anciã, com a migração dos saves, na 1.181.0; a fala da Pita depois do último tratamento na
  1.181.1. Antes: o Esqueleto E1r pela família na 1.175.0,
  o urso e o falcão na fogueira na 1.176.0, o cajado no Atacar do Mago na 1.177.0; a mochila e o mercado sem o "tudo é
  ganho" e a marca de contrato com o cursor normal na 1.177.1 e 1.177.2; a curandeira aberta depois de tratar na
  1.178.0). Antes, o Espectro (1.174.0) e as correções da 1.174.1 à 1.174.6.
- **Etapa 1D concluída:** os **31 equipamentos-base** estão finais desde a 1.150.0, com os acabamentos das luvas L7
  (1.151.0), das perneiras P7 (1.152.0), do capacete C1 (1.153.0) e das botas A1 (1.154.0). **Fora dessa contagem, e
  ainda abertos:** as variantes (os únicos e raros com desenho próprio) e os compartilhamentos provisórios (a Capa de
  Patrulha no gibão, o Chapéu de Couro no capuz, a Coroa dos Afogados no Diadema), a nomenclatura da Sandália e do
  Diadema, e a origem e a licença das referências da L7 e da Esquiva.
- **Etapa 1E em andamento.** Concluídos: o **contador de flechas** da carta do Arqueiro (1.155.0) e os **17 estados**
  do catálogo (1.155.0 a 1.161.0). Criaturas com retrato próprio: o **Afogado e a Ilse** (1.162.0), o **Lobo e o
  Bandido** (1.163.0) e os **três animais do patrulheiro** (o Urso Pardo e o Falcão Peregrino na 1.164.0; o Lobo
  Cinzento, com o mesmo retrato do Lobo inimigo, na 1.165.0), o **Troll da montanha** (1.166.0, pela família), o
  **Rei Troll** (1.167.0, pelo id do guardião) e a **Aranha gigante** (1.167.0, pela família, com as invocadas) e a
  **Rainha Aracnídea** (1.168.0, pelo id da guardiã); depois, pela família, o Sapo e a Sanguessuga (1.171.0), o
  Cultista, a Bruxa e o Rato (1.172.0), o Javali e o Carniçal (1.173.0), o Espectro (1.174.0) e o Esqueleto (1.175.0,
  com os invocados do Lich); o urso e o falcão também na fogueira (1.176.0); o Mercenário e o Lobo Gélido (1.179.0).
  A relação do que falta
  está em "A frente de criaturas em 22/10/2026", no item 1.12. O Bandido do chapéu está reservado como conceito de um possível chefe, fora do jogo.
- **Agora: 1E.3, as demais criaturas, os chefes e as invocações** (as outras ainda saem dos traços: o `fera`, o
  `humano`, a caveira e os outros sprites de 16×16; o levantamento em `ferramentas/prototipos/hud/criaturas/`).
  **Depois: 1E.4**, os caminhos e os símbolos internos do mapa e do minimapa. Em seguida, as **etapas 2–9** como estão
  abaixo, com as habilidades, os talentos, o Grimório e a árvore juntos na etapa 8.
- A HUD principal de ferro e carvão e os menus de pincelada continuam aprovados; o estudo da HUD com pintura permanente
  (1.11) não foi escolhido.

## Estado de referência anterior — 19/10/2026 (histórico)

- Produção confirmada no remoto nesta atualização: **1.146.0**, a cota integrada (depois da espada e da maça, 1.145.0).
- Branch: `claude/tender-einstein-tx3tjl`; esta atualização documental vem depois da integração publicada pela outra
  sessão. Não altera sua arte nem suas verificações.
- **Agora: etapa 1D, fechamento dos equipamentos.** Espada e maça aprovadas nos quatro tamanhos e integradas.
  A cota foi integrada na 1.146.0, a manopla na 1.147.0, o elmo e as perneiras na 1.148.0, o 40/48 do martelo na
  1.149.0 e as botas de ferro na 1.150.0: **os 31 equipamentos-base estão concluídos**.
- Dos 31 desenhos básicos de equipamento: **31 finais** (1.150.0). Continuam as pendências fora da contagem: as
  variantes (os únicos e raros com desenho próprio) e os compartilhamentos provisórios (a Capa de Patrulha no gibão, o
  Chapéu de Couro no capuz, a Coroa dos Afogados no Diadema). A manopla trocada pela L7 na 1.151.0 (a M5 virou
  histórico), **com a origem e a licença do recorte de referência ainda por investigar** (pendência aberta). As
  perneiras trocadas pela P7 na 1.152.0 (a P4 virou histórico) e o elmo pelo capacete com malha C1 na 1.153.0 (o elmo
  de frente virou histórico); as botas de ferro ganharam o acabamento A1 na 1.154.0 (a B3 virou histórico).
- A sequência aprovada passa a ser: **fechar os itens → 1E (flechas e estados primeiro; depois inimigos/pets e
  caminhos/minimapa) → retomar as etapas 2–9**. Ícones de habilidades e talentos serão tratados com seus sistemas,
  Grimório e árvore na etapa 8; não entram numa produção em massa antes disso.
- A HUD principal de ferro e carvão e os menus de pincelada continuam aprovados. O estudo da HUD com pintura
  permanente (1.11) não foi escolhido e não está autorizado para integração.
- Atualização documental: leitura dos arquivos e decisões de Jean; nenhum desenho, código de jogo ou regra mudou.

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
| 1A | Concluir o lote de cabeça/capuz e luvas de couro e tecido | Integrado na 1.112.0 (32, 40, 48, 64; os saves antigos pela migração v5); falta Jean conferir jogando |
| 1B | Corrigir a sequência visual do consumo de recurso e mostrar o bloqueio de vida máxima por ferimentos | Feito: 1.114.1 (o custo) e 1.115.0 (a vida bloqueada) |
| 1C | Prototipar dado mais visível, iniciativa e indicação dos turnos; facilitar consulta aos testes de atributos | Feito: 1.116.0/1.116.1 (iniciativa e turnos), 1.117.0 (a rolagem no centro), 1.118.0 (os testes na ficha) |
| 1D | Fechar equipamentos e objetos da bolsa; concluir ícones gerais já trabalhados | **Concluída** (31 equipamentos-base finais na 1.150.0; acabamentos até a 1.154.0; variantes e compartilhamentos provisórios separados, ainda abertos). Histórico: atributos, nove atalhos da doca e principais recursos/consumíveis integrados. Espada e maça integradas (1.145.0), a cota (1.146.0), a manopla (1.147.0), o elmo e as perneiras (1.148.0), o 40/48 do martelo (1.149.0) e as botas de ferro (1.150.0): os 31 equipamentos-base concluídos. Conferir usos residuais antes de fechar o lote |
| 1E | Desvio visual após os itens: flechas, buffs/estados, inimigos, pets, caminhos e minimapa | **Agora (21/10).** Contador de flechas (1.155.0) e 17 estados (1.155.0–1.161.0) concluídos; Afogado, Ilse, Lobo e Bandido (1.162.0–1.163.0) e os três animais do patrulheiro (1.164.0–1.165.0) integrados; em andamento, 1E.3: as demais criaturas, os chefes e as invocações; depois 1E.4: caminhos e símbolos do mapa/minimapa. Histórico: aprovado como sequência em 19/10. Começar pela contagem de flechas do Arqueiro e por Firme; critérios no item 1.12. **A flecha da carta (F2) e o Firme (R2) no jogo desde a 1.155.0.** Talentos e habilidades ficam para a etapa 8 |
| 2–9 | Telas, serviços, cenários, habilidades e campanha | Sequência detalhada abaixo |

A etapa 1 não precisa terminar todo o catálogo antes de tratar um defeito de compreensão no combate.
Concluir o lote em andamento antes de iniciar outra exploração visual. A nova prioridade de flechas e estados
não interrompe o par já solicitado; abre a etapa 1E, antes de criaturas e navegação.

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
| Vida e recursos | HP, Mana, Vigor, Foco, ouro e demais recursos já migrados; **a contagem de flechas do Arqueiro tem prioridade na 1E**, distinta da aljava do topo já aprovada |
| Navegação | Ícones dos caminhos/destinos e símbolos internos do mapa; auditar os dois contextos |
| Interface e ações | Ícones da ficha, opções e ações (a doca foi concluída na 1.129.0); conferir o que já está aprovado antes de refazer |
| Criaturas | Mobs, chefes e pets/animais; aparência compatível com o mundo e leitura nas cartas, painéis e cenários pertinentes |
| Talentos | Ícones e revisão visual da árvore juntos na etapa 8, após definir o sistema; não alterar efeitos para combinar com o desenho |
| Buffs e estados | **Prioridade da etapa 1E**, começando por Firme; separar os símbolos dos estados existentes dos ícones de habilidades que os aplicam |
| Habilidades | Ícones e animações com os sistemas e o Grimório na etapa 8; não refazer em massa poderes cujo conceito poderá mudar |

Este é um levantamento de escopo, não a afirmação de que todos esses ícones estão ausentes ou ruins.
Criaturas e retratos exigem avaliação própria; o processo dos objetos não obriga a mesma resolução de origem para
todo rosto ou sprite. Reconhecimento, identidade e peso visual no tamanho de uso continuam sendo os critérios.

**Capa de Patrulha:** ganhará desenho próprio no lote de capas. Na 1.110.0 compartilha temporariamente o gibão,
como registrado no roadmap. Conferir também os demais compartilhamentos de bases e únicos para não transformar
uma limitação antiga de mapeamento numa regra artística permanente.

### 1.2.1. Conferência dos equipamentos das classes (19/10/2026, na 1.140.0; corrigida no mesmo dia)

Só os equipamentos (armas, apoios, roupas, armaduras e acessórios), um desenho por linha; os únicos só onde
compartilham a imagem. Fontes: os dados (`rpg/itens.py`: `ARMAS`, `ARMADURAS`, `PECAS`, `AMULETOS`, `ANEIS`,
`UNICOS`), os papéis em `rpg/web/static/icones.js` (`ITEM`, `VAZIO`, `ACAO`, `TAMANHOS`) e `desenhos.js`, a fonte real
de cada arquivo (o `.aseprite`, o `desenhar_*_pixel.py`, a redução de `familia_ferro.py`) e o histórico dos arquivos no
git. Os materiais e os afixos não mudam a imagem e não entram como pendência. "Está integrado", "tem PNG de 32" ou "é
feito em código" não provam nada sozinhos: vale de onde o arquivo sai.

**A correção (decisão do Jean, 19/10/2026):** a primeira versão desta tabela contou a família de ferro como aprovada,
com uma dúvida. Ela é **placeholder**: as sete peças abaixo são reduções da arte pintada das folhas da HUD 4 pixel,
aprovada para uso na 1.89.0, anterior ao padrão atual de pixel art, e precisam ser refeitas nele. A aprovação de uso
de antes não vale como arte final.

**A fonte das peças de ferro, uma a uma** (histórico da auditoria na 1.140.0; a tabela abaixo registra as
substituições posteriores, incluindo espada e maça na 1.145.0):
- `elmo`, `cota`, `manopla`, `perneiras`, `botas-ferro`, `maca`, `espada`: os arquivos do jogo saem de
  `ferramentas/arte/familia-ferro/<peça>.png` (a pintura recortada) pela redução "paleta" de `familia_ferro.py`;
  `familia_ferro.py --conferir` refaz todos os tamanhos e dá "tudo igual", e os PNGs de 32 não mudaram desde o commit
  da HUD de ferro (`58c20d8`). Nenhuma delas tem desenho próprio refeito depois. **Derivadas da pintura.**
- `escudo`: está na pintura e na conta da escala da família, mas o arquivo do jogo sai de `desenhar_escudo_pixel.py`,
  desenhado na grade de cada tamanho (1.94.0, `bbeda6a`); é uma das duas referências do método na skill
  `arte-itens-fenda`. **Desenho próprio, no padrão atual.**
- `machado`: não está na pintura; `desenhar_machado_pixel.py`, na grade de cada tamanho (1.99.0, `85547a5`).
  **Desenho próprio, no padrão atual.**
- `martelo`: não está na pintura; uma grade de 32 em `desenhos.js`, desenhada à mão no experimento de resolução
  (1.93.0, `d34b8a4`). Não é derivado da pintura, mas não tem arquivo de 40 (o Inventário o mostra em 32) e o 48 é a
  2× reduzida pelo navegador, o que a skill chama de herança, não de padrão. **Decisão do Jean (19/10/2026): o desenho
  aprovado fica preservado**; a pendência era só completar o 40 e o 48 mantendo a construção dele, sem redesenho
  (feito: aprovados no `244cdbd4` e integrados na 1.149.0, em arquivo; o 32 e o 64 continuam em `desenhos.js`). A
  execução fica para outra entrega.

**A tabela, por situação:**

| Desenho | Bases (e únicos) que usam a imagem | Situação | Sustentação | Atenção |
|---|---|---|---|---|
| `espada` | Espada, Montante (Guerreiro) | Arte final, padrão atual (o remake do ferro, integrada na 1.145.0) | `aseprite/espada/` (1.145.0) | Também é o comando de ataque da luta (`ACAO`) e a silhueta da arma vazia (`VAZIO`), de todas as classes; o ícone do atributo Ataque é outro desenho |
| `maca` | Maça (Guerreiro) | Arte final, padrão atual (o remake do ferro, integrada na 1.145.0) | `aseprite/maca/` (1.145.0) | — |
| `elmo` | Elmo, Capacete, Barbuta (Guerreiro) | Arte final, padrão atual (**o C1**, o capacete com malha, a transposição da imagem gerada do Jean, `referencias/capacete/capacete-malha-gerada.webp`: o 32 do `b6af648f`; o 40 e o 48 são o mesmo 32 centrado em quadros transparentes, como na L7 e na P7; o 64 = 32 ×2; integrado na 1.153.0); o elmo de frente (a rodada 4, 1.148.0) é histórico | `aseprite/elmo/` (1.153.0; a rodada 4 em `aseprite/historico/elmo-r4/`) | Também a silhueta da cabeça vazia, de todas as classes (`VAZIO`), e a reserva da cabeça (`ICONE_ESPACO`) |
| `armadura` → `cota` | Cota de Malha, Peitoral, Couraça, Brigantina (Guerreiro) | Arte final, padrão atual (o remake do ferro, integrada na 1.146.0) | `aseprite/cota/` (1.146.0) | Também a silhueta da armadura vazia (`VAZIO`); a camisa de malha representa pior o Peitoral e a Couraça (de placa) |
| `manopla` | Manopla (Guerreiro) | Arte final, padrão atual (**a L7**, o par de luvas de couro com a malha, a transposição da referência escolhida pelo Jean, `referencias/Luvas/luvas-par-recorte.png`: o 32 do `c7639438`; o 40 e o 48 são o mesmo 32 centrado em quadros transparentes, do `fa9711bb`; o 64 = 32 ×2; consolidada no `63f5c81e`, integrada na 1.151.0); **pendente: a origem e a licença do recorte** (com marca d'água; não informadas, a investigar; a L7 não é CC0); a M5 (1.147.0, da `glove_04` da Dungeon Crawl, CC0) é histórico | `aseprite/manopla/` (1.151.0; a M5 em `aseprite/historico/manopla-m5/`) | Também a silhueta das mãos vazias (`VAZIO`); a habilidade Grito de Guerra usa o sprite `manopla` noutro papel e não muda; o crédito da M5 no `LEIA-ME.md` das fontes e em `externas/cc0_hand_wear_icons/` |
| `calca` → `perneiras` | Perneira, Greva (Guerreiro) | Arte final, padrão atual (**a P7**, a transposição da segunda imagem gerada do Jean, `referencias/calça/perneiras-gerada-2.webp`, com as laterais suavizadas: o 32 do `6dc582e3`; o 40 e o 48 são o mesmo 32 centrado em quadros transparentes, como na L7; o 64 = 32 ×2; integrada na 1.152.0); a P4 (1.148.0) é histórico; a P1 e a P6 ficam no protótipo como alternativas não escolhidas | `aseprite/perneiras/` (1.152.0; a P4 em `aseprite/historico/perneiras-p4/`) | Também a silhueta das pernas vazias (`VAZIO`) e o desenho de reserva das pernas (`ICONE_ESPACO`) |
| `bota_ferro` → `botas-ferro` | Bota Ferrada (Guerreiro) | Arte final, padrão atual (a forma da B3, a transposição da referência gerada do Jean, **com o acabamento A1**: os reflexos contidos e o aço no tom médio; 32 e 64 = 32 ×2 do `945a54a8`, 40 e 48 do `3c41c7a0`; integrada na 1.154.0); a B3 polida (1.150.0) é histórico; a B1 e a B2 ficam no protótipo como tentativas | `aseprite/botas-ferro/` (1.154.0; a B3 em `aseprite/historico/botas-ferro-b3/`) | Também a silhueta dos pés vazios (`VAZIO`) |
| `martelo` | Martelo (Guerreiro) | Arte final, padrão atual (o 32 e o 64 da grade aprovada; o 40 e o 48 do `244cdbd4`, integrados na 1.149.0) | grade de 32 em `desenhos.js` (1.93.0); o 40 e o 48 em `aseprite/martelo/` (1.149.0) | Desenho próprio, não da pintura; o Golpe Pesado, o traço Gigante e o ferreiro usam o sprite 16×16 "martelo" do jogo, outro desenho |
| `besta` | Besta Leve (Arqueiro) | Arte final, padrão atual (integrada na 1.143.0) | `aseprite/besta/` (1.143.0) | Uma das quatro armas do Arqueiro |
| `chapeu` | Chapéu Pontudo (Mago) | Arte final, padrão atual (integrada na 1.141.0) | `aseprite/chapeu/` (1.141.0) | Um terço das cabeças do Mago |
| `coroa` → `diadema` | Diadema (Mago); único Coroa dos Afogados | Arte final, padrão atual (integrada na 1.144.0) | `aseprite/diadema/` (1.144.0) | A Coroa dos Afogados: compartilhamento provisório (pede arte própria); o sprite `coroa` da reputação fica |
| `sandalia` | Sandália (Mago, a única base dos pés dele) | Arte final, padrão atual (integrada na 1.142.0) | `aseprite/sandalia/` (1.142.0) | Nomes dos materiais de tecido num desenho de couro: pendência de nomenclatura |
| `escudo` | Escudo, Broquel; únicos Égide do Mártir, Broquel do Vigia | Arte final, padrão atual | `desenhar_escudo_pixel.py` (1.94.0) | Também a silhueta da secundária vazia (`VAZIO`) |
| `machado` | Machado; únicos Lamento de Gharbad, O Açougueiro | Arte final, padrão atual | `desenhar_machado_pixel.py` (1.99.0) | — |
| `arco` | Arco Curto, Longo, Recurvo; únicos Ventre da Tempestade, Sussurro do Vazio | Arte final, padrão atual | `desenhar_arco_pixel.py` (1.101.0) | — |
| `aljava` | Aljava; único Aljava dos Mil Corvos | Arte final, padrão atual | `aseprite/aljava/` (1.122.0) | Também o recurso de flechas do topo |
| `gibao` | Gibão de Couro, Colete Acolchoado, Capa de Patrulha; único Pele do Penitente | Arte final, padrão atual | `aseprite/gibao/` (1.110.0) | A Capa de Patrulha: compartilhamento provisório |
| `capuz` | Capuz, Chapéu de Couro (Arqueiro) | Arte final, padrão atual | `aseprite/capuz/` (1.112.0) | O Chapéu de Couro: compartilhamento provisório |
| `luva` | Braçadeira; único Mãos do Estrangulador | Arte final, padrão atual | `aseprite/luva/` (1.112.0) | — |
| `calca_couro` | Calça de Couro (Arqueiro) | Arte final, padrão atual | `aseprite/calca_couro/` (1.119.0) | — |
| `bota` | Bota de Caça; único Botas do Andarilho Morto | Arte final, padrão atual | `aseprite/bota/` (1.110.0) | — |
| `cajado` | Cajado; único Cajado da Peste | Arte final, padrão atual | `desenhar_cajado_pixel.py` (1.106.0) | — |
| `varinha` | Varinha | Arte final, padrão atual | `aseprite/varinha/` (1.109.0) | — |
| `orbe` | Orbe (arma), Foco Arcano (apoio); único Olho do Abismo | Arte final, padrão atual | `desenhar_orbe_pixel.py` (1.107.0) | Arma e apoio na mesma imagem desde a integração |
| `livro` | Grimório (arma), Tomo (apoio); único Tomo do Nome Esquecido | Arte final, padrão atual | `desenhar_livro_pixel.py` (1.108.0) | Arma e apoio na mesma imagem desde a integração |
| `capuz_tecido` | Capuz (Mago) | Arte final, padrão atual | `aseprite/capuz_tecido/` (1.112.0) | — |
| `luva_seda` | Luva de Seda | Arte final, padrão atual | `aseprite/luva_seda/` (1.112.0) | — |
| `manto` | Manto, Túnica, Veste Rúnica; único Manto de Cinzas | Arte final, padrão atual | `aseprite/manto/` (1.138.0) | Compartilhamento mantido por decisão do Jean |
| `calca_tecido` | Calça de Viagem; único Mordida do Túmulo | Arte final, padrão atual | `aseprite/calca_tecido/` (1.138.0) | — |
| `anel` | Anel, Sinete, Aro; único Anel do Último Rei | Arte final, padrão atual | `aseprite/anel/` (1.140.0) | Compartilhamento mantido |
| `amuleto` | Amuleto, Talismã, Pingente, Medalhão | Arte final, padrão atual | `aseprite/amuleto/` (1.140.0) | Compartilhamento mantido |

**A contagem:** 31 desenhos de equipamento.
- **Arte final aprovada no padrão atual:** 31 (o escudo, o machado, a espada, a maça, o martelo, a cota, a manopla, o
  elmo, as perneiras e as botas de ferro e os 21 do
  Arqueiro, do Mago e dos acessórios; o Chapéu Pontudo entrou na 1.141.0, a Sandália na 1.142.0, a Besta Leve na
  1.143.0, o Diadema na 1.144.0, a espada e a maça na 1.145.0, a cota na 1.146.0, a manopla na 1.147.0, o elmo e as
  perneiras na 1.148.0, o 40 e o 48 do martelo na 1.149.0, as botas de ferro na 1.150.0; a manopla trocada pela L7 na
  1.151.0; as perneiras pela P7 na 1.152.0; o elmo pelo C1 na 1.153.0; o acabamento A1 das botas na 1.154.0).
- **Placeholder integrado, pendente de remake:** nenhum (desde a 1.150.0). O equipamento-base do Guerreiro está
  concluído: o escudo, o machado, a espada, a maça, o martelo, a cota, a manopla, o elmo, as perneiras e as botas de
  ferro são finais.
- **Desenho inexistente:** nenhum (desde a 1.144.0, todo desenho de equipamento das classes tem arte no jogo).
- **Arte aprovada com tamanhos pendentes:** nenhuma (o 40 e o 48 do martelo entraram na 1.149.0).
- **Compartilhamento provisório aceito** (a peça usa o desenho de outra até ganhar o seu): a Capa de Patrulha no gibão
  (o lote de capas), o Chapéu de Couro no capuz e o único Coroa dos Afogados no Diadema. Os compartilhamentos do manto, do anel, do amuleto, do orbe e do livro
  são definitivos, não pendência. As silhuetas apagadas dos espaços vazios (`VAZIO`) vêm do elmo, da cota, da manopla,
  das perneiras, das botas de ferro e da espada para todas as classes: mudam junto quando essas peças forem refeitas.

Nenhuma proposta pendente de equipamento na data da conferência. Depois dela, a Sandália e o Chapéu Pontudo entraram
em proposta (abaixo, "O par do Mago"): o chapéu foi integrado na 1.141.0 e a sandália na 1.142.0; depois, a Besta
Leve (1.143.0) e o Diadema (1.144.0).

**O levantamento depois da 1.144.0 (19/10/2026):** os 31 desenhos de equipamento das classes existem no jogo. **Não
estão concluídos:** as **sete peças de ferro** do Guerreiro (espada, maça, elmo, cota, manopla, perneiras, botas de
ferro), que continuam placeholders, reduções da arte pintada, pendentes de remake no padrão atual; e o **martelo**, com
o desenho aprovado preservado e a pendência separada de completar o 40 e o 48 sem redesenho. Ficam também os
compartilhamentos provisórios (a Capa de Patrulha, o Chapéu de Couro, a Coroa dos Afogados) e a pendência de
nomenclatura (a Sandália e o Diadema com os materiais de tecido nos nomes). **O próximo par, decidido pelo Jean: a
espada e a maça** (o começo do remake do ferro).

**O remake do ferro, 1: a espada e a maça (proposta do 32, 19/10/2026; nada no jogo).** Em
`ferramentas/prototipos/hud/itens-lote-noite/espada_maca/` (o registro completo no `LEIA-ME.md` do lote):
- **Os usos:** `espada` vale para as bases Espada e Montante (nenhum único), para a silhueta da arma vazia de todas as
  classes (`VAZIO`) e para o comando Atacar do Guerreiro na roda da luta (`ACAO`; `icone_ataque` da classe, a mesma
  espada qualquer que seja a arma). O ícone do atributo Ataque é outro arquivo (`attr-ataque`, aprovado) e não muda. O
  sprite 16×16 `espada` (estados, talentos, habilidades, selos) também é outro e não muda. `maca` vale só para a base
  Maça.
- **Só o 32 e o 64 (= 32 ×2):** os 40 e 48 ficam para depois da aprovação da forma. Uma futura integração da espada
  muda também a arma vazia e o Atacar.
- **A rodada 2 (19/10/2026; nada no jogo).** O Jean reavaliou a espada da rodada 1 (`796edd2`): a lâmina larga na
  base, afinando por um trecho longo, lembrava uma cunha; o pedido de completar os tamanhos dela foi substituído pela
  rodada 2. A maça da rodada 1 tinha a cabeça estreita e alongada, com uma faixa clara que lembrava uma ponta. As duas
  da rodada 1 estão guardadas em `espada_maca/rodada1/` como tentativas não escolhidas.
  - **A espada, pela referência** (`ferramentas/arte/referencias/espada/`, a hierarquia no `LEIA-ME.md` de lá; a
    principal é `espadasample.png`, a espada de aço da direita): a lâmina comprida de largura constante, os gumes
    paralelos e contínuos, a ponta formada no último quarto, dois planos e a aresta, a guarda curta de latão, o pomo de
    aço.
  - **A maça:** a cabeça redonda e pesada (a massa e a proporção com o cabo do placeholder antigo, sem a pintura dele),
    cinco aletas curtas e separadas, a luz pelo volume (o bulbo como esfera), sem a faixa clara.
  - Uma skill de espadas fica para depois de um resultado validado.
  - **Depois da avaliação (19/10/2026):** a maça da rodada 2 foi aprovada (o 32 e o 64 ficam sem retoque) e ganhou o 40 e
    o 48 em proposta, com as aletas no mesmo formato do 32 (botões rombudos com a junção escura). Na espada, só a ponta
    voltou: o trecho final parecia um biquinho acrescentado (uma agulha depois do corpo); a ponta corrigida (os gumes
    convergindo sem degrau, como na referência) está em avaliação, com o 40 e o 48 dela aguardando.
  - **A ponta, terceira tentativa (19/10/2026):** a do `723cf8d` tirou a agulha, mas ficou rombuda (o fio claro acabava
    antes do vértice e o último pixel era escuro, uma "tampa"). Refeita pixel a pixel no 32 (o diagnóstico no
    `LEIA-ME.md` do lote); em avaliação. Ainda não vira regra: a skill de espadas espera o resultado aprovado.
  - **A ponta, quarta forma (19/10/2026):** a terceira era válida, mas diferente da referência (o fechamento deslocado
    para um lado, com uma mudança brusca de direção no fim). O Jean trocou a abordagem: em vez de um gume reto e o
    outro avançando, os dois gumes convergindo de forma contínua para uma ponta alinhada com a lâmina. Refeita assim
    (regra simétrica no eixo, o vértice sobre o eixo); **aprovada** (`0fcfe18`). **Os quatro tamanhos das duas peças foram aprovados por Jean em 19/10 e integrados na 1.145.0**
    (os 40/48 da espada em `441787e`; os da maça em `723cf8d`; fontes em
    `ferramentas/arte/aseprite/espada/` e `maca/`). O aprendizado
    virou a skill `arte-espadas-fenda` (`.claude/skills/`), complementar à `arte-itens-fenda`.

**A ordem recomendada (separada da contagem):** primeiro a **Sandália e o Chapéu Pontudo**, que são o placeholder
mais frequente do Mago e fecham o vestuário de tecido dele, já com capuz, luva, calça e manto aprovados como referência
do material. Fazer esse par antes não declara o Guerreiro concluído. Depois, a Besta Leve e o Diadema, e o remake do
ferro como um lote próprio (as sete peças têm de conviver entre si, com o escudo e o machado, e mudam as silhuetas dos
espaços vazios), na ordem que o Jean decidir.

**O martelo (decisão do Jean, 19/10/2026):** o desenho aprovado é preservado. A pendência é completar o 40 e o 48
mantendo a construção da grade de 32; não há autorização para redesenhá-lo, e ele não entra no lote do ferro. A
execução fica para outra entrega.

**O par do Mago: a Sandália e o Chapéu Pontudo (19/10/2026).** Em
`ferramentas/prototipos/hud/itens-lote-noite/sandalia_chapeu/` (o registro completo no `LEIA-ME.md` do lote):
- **O alcance de uma futura troca:** os desenhos `sandalia` (a Sandália, a única base dos pés do Mago) e `chapeu` (o
  Chapéu Pontudo, uma das três cabeças) não têm papel em `Icones` hoje e não são usados por nenhum único, símbolo,
  habilidade ou estado; os espaços vazios da cabeça e dos pés continuam com o elmo e as botas de ferro (`VAZIO`). Os
  materiais (Puído, de Linho, de Lã Negra, Bordado, Rúnico) só mudam o nome. Integrar pede o papel em `ITEM` e
  `TAMANHOS` e o 64 em `DERIVADOS`, nada mais.
- **O Chapéu Pontudo: aprovado sem retoque (`b361a47`) e integrado na 1.141.0** (fontes em
  `ferramentas/arte/aseprite/chapeu/`; 32, 40, 48 e o 64 = 32 ×2).
- **A Sandália: a rodada 1 (de perfil, a gaiola de tiras) foi recusada:** as tiras viraram arcos verticais e o conjunto
  parecia uma armação sobre a sola. A rodada 2 é o par em três quartos, visto um pouco de cima, pela referência do Jean
  (`ferramentas/arte/referencias/botas/`); **aprovada nos quatro tamanhos (`b9ec78a`) e integrada na 1.142.0** (fontes em
  `ferramentas/arte/aseprite/sandalia/`; 32, 40, 48 e o 64 = 32 ×2).
- **Os nomes dos materiais (registrado, sem mudar regra):** a Sandália recebe os materiais de tecido (`MATERIAIS_TECIDO`:
  "Sandália de Lã Negra", "Sandália de Linho", "Sandália Bordada"), mas o desenho é de couro, como uma sandália de
  viagem. **Pendência de nomenclatura** (não impediu a integração visual; nomes e materiais mantidos na 1.142.0):
  decidir depois se a base ganha materiais próprios (couro) ou se os nomes ficam.

**A Besta Leve e o Diadema (19/10/2026).** A Besta Leve foi aprovada sem retoque (`63a7a85`) e integrada na 1.143.0
(fontes em `ferramentas/arte/aseprite/besta/`); o Diadema voltou para uma revisão de apresentação, e a rodada 2 foi
aprovada sem retoque (`731ab5c`) e integrada na 1.144.0 (fontes em `ferramentas/arte/aseprite/diadema/`). Em
`ferramentas/prototipos/hud/itens-lote-noite/besta_diadema/` (o registro completo no `LEIA-ME.md` do lote):
- **O alcance de uma futura troca:**
  - `besta`: só a base Besta Leve (uma das quatro armas do Arqueiro, com os materiais de metal: "Besta Leve
    Enferrujada", "de Aço"...); nenhum único, símbolo ou espaço vazio (a arma vazia é a espada de ferro).
  - `coroa`: a base Diadema (uma das três cabeças do Mago, materiais de tecido nos nomes: "Diadema de Lã Negra") e o
    único Coroa dos Afogados (base Diadema, lendário, de qualquer classe; "Achada na cabeça de um rei no fundo do
    pântano"). O mesmo sprite `coroa` é o símbolo da reputação (`S("coroa")` no Inventário e `Icones.miudo` nos ganhos
    de contrato, fora do mapa `ITEM`): a troca do equipamento não o muda. O espaço vazio da cabeça é o elmo de ferro.
- **A decisão proposta para o Diadema:** um desenho comum (o diadema) para a base e para a Coroa dos Afogados por ora;
  **a Coroa dos Afogados pede arte própria no futuro** (o nome e a história são de uma coroa de rei afogado, lendária,
  e o diadema de latão é uma peça simples). Nenhum dado mudou e nenhum item foi criado.
- **Os nomes:** o Diadema leva os materiais de tecido ("Diadema de Lã Negra"), mas o desenho é de latão: a mesma
  pendência de nomenclatura da Sandália.
- **O Diadema, rodada 2 (integrada na 1.144.0):** a rodada 1 ficou achatada (no tamanho real, uma elipse dourada com um ponto
  no meio; a frente pouco visível) e está guardada em `besta_diadema/diadema_r1/`. A rodada 2 vira a peça de frente,
  pela imagem que o Jean mandou para o ângulo: a face da frente da faixa à mostra, a face de dentro do lado de trás
  escura por cima dela, a ponta com a gema; o latão e a gema violeta ficam. O compartilhamento com a Coroa dos Afogados
  continua provisório, e o símbolo da reputação não muda.

**O levantamento depois da 1.145.0 (19/10/2026):** a espada e a maça passaram a arte final. Continuam pendentes os
remakes do elmo, da cota, da manopla, das perneiras e das botas de ferro (placeholders, reduções da arte pintada; também
as silhuetas dos espaços vazios) e o 40 e o 48 do martelo aprovado. **O próximo par, decidido pelo Jean: o elmo e a
cota** (não começado).

**A cota integrada na 1.146.0 (19/10/2026):** aprovada pelo Jean nos quatro tamanhos (o 32 e o 64 do `119f479`, o 40 e
o 48 do `998373c`), sem retoque: as fontes em `ferramentas/arte/aseprite/cota/`, `DERIVADOS` com o 64 = 32 ×2, os 8
arquivos do jogo idênticos byte a byte aos aprovados (`exportar_aseprite.py cota --conferir` os reproduz). Os papéis já
existiam (`ITEM` e `VAZIO`), sem mudança: as quatro bases do peito do Guerreiro e a silhueta do peito vazio de todas as
classes. Conferido a 1920×945 com os saves temporários: o saque (64 e 48), equipar e guardar, a ficha (32), o
Inventário (40) e o peito vazio (tirar com dois cliques).

**O remake do ferro, 2: o elmo e a cota (proposta do 32, 19/10/2026; nada no jogo).** Em
`ferramentas/prototipos/hud/itens-lote-noite/elmo_cota/` (o registro completo no `LEIA-ME.md` do lote):
- **Os usos:** `elmo` vale para o Elmo, o Capacete e a Barbuta (nenhum único), para a silhueta da cabeça vazia de todas
  as classes e para o desenho de reserva de um item de cabeça sem base reconhecida (`ICONE_ESPACO`). `cota` (o desenho
  `armadura` nos dados) vale para a Cota de Malha, o Peitoral, a Couraça e a Brigantina (nenhum único), para a silhueta
  do peito vazio e para o desenho de reserva do peito.
- **A limitação registrada:** uma cota de malha só para quatro bases de construções diferentes (malha, peitoral de
  placa, couraça, brigantina de placas rebitadas). Sem criar variantes nesta entrega; um desenho por base fica como
  possibilidade futura, para o Jean decidir.
- **Só o 32 e o 64 (= 32 ×2):** o 40 e o 48 depois da aprovação. Uma futura integração muda também as silhuetas da
  cabeça e do peito vazios.
- **A rodada 2 (19/10/2026), pelas referências do Jean** (`ferramentas/arte/referencias/capacete/` e `peitoral/`, os
  papéis no `LEIA-ME.md` de cada pasta): o elmo da rodada 1 não foi aprovado (a parte de baixo parecia um bloco, a
  abertura em T desenhada na superfície, a faixa de latão rígida atravessando a peça). O capacete recomeçou pela
  principal (o capacete aberto de frente, um pouco virado: a calota com a tira, a faixa da testa em curva, o nariz, as
  faces longas, o fundo escuro com o vazio abaixo); a cota foi ajustada pela principal do peito (a camisa de malha de
  aço: a gola na malha, as mangas e a barra em dentes, o volume escurecendo nos lados). A rodada 1 está guardada em
  `elmo_cota/rodada1/`. A cota de malha continua compartilhada: representa melhor a Cota de Malha, razoavelmente a
  Brigantina (uma armadura flexível de tronco) e pior o Peitoral e a Couraça, que são de placa (as couraças de aço da
  prancha ficam como referência de uma variante futura).
- **Depois da avaliação (19/10/2026):** a cota da rodada 2 foi aprovada (o 32 e o 64 sem retoque) e ganhou o 40 e o 48
  em proposta. O elmo voltou para uma rodada 3, pela mesma referência: a faixa quase horizontal, as laterais como barras
  verticais e uma faixa escura atravessando a abertura (uma "travessa") foram refeitas pelas medidas da referência.
- **A rodada 4 do elmo (19/10/2026):** nova referência principal, `capacete/elmo-frente-jean.webp` (a coluna da
  direita): o capacete em pé e de frente, eixo vertical e nariz centralizado, substituindo a inclinação da rodada 3. A
  cota aprovada e os tamanhos dela ficaram intocados.

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

**Feito e integrado (1.114.1, 17/10/2026).** Diagnóstico demonstrado: o motor desconta antes de agir (depois da mira
confirmada), mas a ponte web só mandava o estado junto de um texto. O recurso pago chegava à tela depois da animação do
golpe (alvo único) ou só no fim da salva (área), e a cura de uma salva podia vir antes do custo. Medido quadro a quadro
(`ferramentas/prototipos/hud/custo-recurso/`): na Drenar Vida, o custo aparecia 666 ms depois da confirmação, contra
132 ms do começo da ação; na Chuva de Flechas, 1012 ms, depois da salva inteira. Correção: `ui.atualizar()` logo depois
do desconto (habilidades e a flecha do ataque básico). O custo agora chega no quadro do começo da ação (208 e 74 ms).
A mira continua sem pagar; não mudam contas, sorteios, a ordem dos lances nem o gabarito.
`tests/test_custo_na_tela.py` (Mana, Vigor, Foco e flechas, área, cancelar e executar) falha sem a correção.
Fica para a avaliação: um sinal próprio de "pago" na carta (hoje o número e a barra só descem).

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

**Protótipo (17/10/2026, nada no jogo; `ferramentas/prototipos/hud/rolagem/`):** uma alternativa só, nos testes de
atributo fora da luta. A mesma mensagem `rolagem` do motor, sem sortear nada:
- **o teste:** a área principal (sem as colunas laterais) escurece, mais no centro; no meio, o nome do teste e a
  dificuldade;
- **a rolagem:** o dado de sempre, 2×, girando, com a tirinha em pincel embaixo ("d20 + 2", "precisa de 10 ou mais",
  as parcelas do estado);
- **o resultado:** o dado pousa, a conta fecha e aparece a faixa de resultado. Sucesso: marfim inteira, e o contorno de
  latão se fecha. Falha: carvão rasgada, o texto caído. Crítico e Desastre, idem, com mais peso;
- **a consequência:** o grupo desce até a tirinha de sempre no texto, e só então ela vem.

O ritmo é o de hoje (da tirinha à consequência: 1627–1631 ms, atual e proposta), sem clique novo. Pular corta; no
instantâneo, ao refazer a página e na luta, a rolagem de sempre; movimento reduzido sem deslocamento. Comparado com os
mesmos dados (o baú abandonado, Percepção 12: sucesso por 1 e falha por 1) a 1920×945. "Precisa de N" é derivado na
tela; na integração viria do motor.

**Aprovado por Jean e integrado na 1.117.0** (17/10/2026):
- **No jogo:** `app/rolagem.js` (a função `rolagem`, que saiu de `pagina.js`) e `20-rolagem.css`. As variáveis do pincel
  valem também em `.rolagem-centro` (`18-seletor-habilidades.css`). Nada da pasta de protótipos, que fica como histórico
  das alternativas.
- **"Precisa de N ou mais" vem do motor:** `Testes.precisa_no_dado(cd, mod)` (o menor d20 que passa, com o 20 e o 1),
  enviado por `teste()` em `ui.rolagem(..., precisa=)`. A tela só escreve a frase. `tests/test_rolagem.py` confere o
  número contra a regra, valor por valor, e contra o resultado de 200 testes. Sorteios, bônus, dificuldades e
  resultados iguais: o gabarito não mudou.
- **Conferido no jogo** (`ferramentas/prototipos/hud/rolagem/integracao.mjs`, 1920×945):
  - os mesmos sucesso e falha por 1, com "precisa de 10 ou mais" do motor;
  - da tirinha à consequência, 1628–1633 ms (o protótipo: 1627–1631);
  - pular tira o centro em ~110 ms; no texto instantâneo, nada no centro; movimento reduzido no mesmo tempo.
- **Fica para depois:** o redesenho artístico do dado vai para o acabamento visual da HUD (seção 2), junto dos
  efeitos de raridade e da subida de nível. Esta entrega não redesenha o dado.

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

**Protótipo (17/10/2026, em avaliação; nada no jogo):** `ferramentas/prototipos/hud/turnos/`.
- **A fonte é o motor:** a mensagem `turno` (`ui.novo_turno`, uma vez por volta, no começo da sua vez; comitiva,
  animal e servos não geram) e `estado.combate.turno`; o lance `surpresa` (de `j`: a sua iniciativa; de um inimigo: a
  emboscada, o golpe livre do mais ágil antes do turno 1); o estado `iniciativa` na sua carta, com o texto do motor
  (+25% no primeiro golpe); e o golpe com `bonus_motivo: "Iniciativa!"`, que a consome. O turno 1 com a iniciativa é só
  seu, e ela passa sem golpe se o turno livre for gasto noutra coisa.
- **A proposta:**
  - um anúncio em faixa de pincel: "Turno N"; "Iniciativa!" com "Turno 1 · só você age agora" e o bônus real;
    "Emboscada!" com quem ataca;
  - uma placa para consulta: o turno de agora e, enquanto vale, "Iniciativa: +25% no 1º golpe", que termina em
    "usada" ou "passou";
  - o lugar é medido para nunca cobrir carta, comando, mira, seletor ou o aviso da cena: dentro da faixa dos comandos,
    na luta cheia; abaixo da arena, na pequena;
  - nada segura a vez (a camada não recebe o mouse); com movimento reduzido, sem deslocamento e com mais tempo.
- **Conferido:** produção × proposta com os mesmos dados, em lutas reais (iniciativa, emboscada, luta cheia com
  comitiva, servos e Maldição em área), em 1280×720, 1500×950 e com movimento reduzido. Um anúncio por mensagem de turno
  do motor (mais a emboscada), nada coberto, e a vez clicável no mesmo tempo da produção. Há vídeos, e `abrir.mjs` abre
  a luta numa janela para jogar.
- **Novo no cenário de teste:** `EMBOSCADA` e `LUTA_APOS_ESCOLHA` (a luta começa com a página aberta, a surpresa ao
  vivo).
- **Para decidir:**
  - o anúncio cobre o começo do registro por ~1 s na luta pequena;
  - anunciar todo turno ou só o primeiro e a iniciativa.

  Falta Jean avaliar. Dado e consulta aos atributos não começaram.

**Aprovado por Jean e integrado na 1.116.0** (17/10/2026):
- **No jogo:** `turnos.js` e `19-turnos.css` (o anúncio, a placa, o lugar medido, nada esperando, o movimento
  reduzido), chamados por `paineis.aplicarEstado`, `pagina.turno` e a fila de lances; nada da pasta de protótipos.
- **O turno perdido:** o catálogo de estados ganhou `perde_turno`. O anúncio diz "Turno N · Preso na teia: você perde
  este turno", e a roda não aparece nesse turno; a contagem segue a do motor.
- **O estouro de pixels antes da luta:** eram as partículas da festa de nível, disparadas mesmo quando a festa passava
  sem cerimônia (a página relendo a cena, ou o texto instantâneo). O som e as partículas passaram para depois dessa
  linha, nas festas de nível, de Sigilo e de especialização. A festa ao vivo fica igual, e nada a substitui.
- **Conferido em lutas reais:** iniciativa, emboscada, sem vantagem, luta cheia com comitiva e servos, preso na teia;
  1280×720 e 1500×950; normal e reduzido. Um anúncio por mensagem de turno, nada coberto, 0 partículas no carregamento
  (antes, 720).
- **Gabarito:** só o campo novo `perde_turno` no catálogo (as 9 partidas web); nenhuma partida, lance ou sorteio.

**Ajuste na 1.116.1** (17/10/2026, direção de Jean, integrado direto):
- **A placa e o anúncio parados no golpe final:** a arena chega perto (zoom) e treme no impacto; os dois são interface e
  se medem pelo layout, não pelo retângulo na tela. Medido quadro a quadro: a arena se move até 55–64 px; a placa e o
  anúncio, 0 px. O zoom, a tremida e o impacto ficam iguais.
- **O anúncio num lugar só:** no centro da área de combate, na borda de cima, logo acima das cartas e dos comandos,
  numa linha ("Turno 2"; "Iniciativa! | Turno 1 · Só você age"; "Emboscada! | Lobo ataca antes de você"; "Turno 2 |
  Preso na teia: você perde este turno"). O bônus da iniciativa fica na placa.
- **Por que ali:** entre os grupos não há lugar na luta pequena; a roda ocupa a faixa inteira (de 77 a 269 px a
  1280×720), e qualquer altura ali esconde algum comando. Encaixar o anúncio nos vãos mudava o lugar e estreitava o
  texto a cada composição. A borda de cima é a mesma em todas as lutas.
- **Conferido:** luta pequena e cheia, 1280×720 e 1500×950, iniciativa, emboscada, turno perdido, golpe final,
  movimento reduzido e redimensionar. Nada coberto (comandos, cartas, placa, registro, texto do topo), nada cortado; a
  vez clicável segue em 9–33 ms.

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

**Feito e integrado (1.118.0, 17/10/2026).** São seis testes derivados (Força, Destreza, Arcano, Percepção, Vontade,
Carisma), não atributos próprios: o bônus de cada um soma metade do nível, a parte de um atributo da ficha (Ataque,
Agilidade, Poder, Defesa, ou a Reputação, no Carisma), o bônus de classe ou especialização e a situação (sem luz).

**O que já estava claro e ficou:**
- a etiqueta da escolha ("PER +2"), com as parcelas na dica;
- a rolagem no centro (1.117.0), com a conta, as parcelas e "precisa de N".

**As lacunas resolvidas:**
- **Nenhum lugar com os seis juntos e a composição.** Os totais estavam espalhados nas dicas de Ataque, Defesa,
  Agilidade, Poder e Reputação, sem dizer de onde vinham. Agora há uma linha "Testes do d20" na ficha, embaixo dos
  atributos (os seis números ficam só na dica). Para cada teste, a dica mostra:
  - o bônus do personagem;
  - de onde vem (nível, atributo, classe);
  - para que serve;
  - se o atributo de origem está abaixo do normal, o porquê (ferimento, fome).
  O rodapé dá a regra do 20 e do 1 e o ajuste da dificuldade pelo nível.
- **A escuridão aparecia como valor do personagem.** Ela entrava nos totais das dicas dos atributos. O motor agora
  separa as partes fixas (`partes_fixas_teste`) da situação (`situacao_teste`); a soma e o sorteio não mudam. A
  escuridão só aparece como "Agora: escuridão −4 → +9", enquanto vale; na dica da escolha, como "(agora)".
- **O total repetido nas dicas dos atributos.** Cada uma diz só a parte daquele atributo ("Nos testes, a Agilidade dá
  +7 em Destreza e +6 em Percepção"); o total fica em Testes do d20.
- **A chance da dica da escolha era calculada na tela.** Agora vem do motor (`chance_teste_media`, pela regra do teste
  e `precisa_no_dado`, na dificuldade típica `CD_MEDIA`).

**Conferido:**
- `tests/test_testes_ficha.py` compara o mostrado com o motor nestes casos: básico; arqueiro patrulheiro de nível 5
  (classe e nível); sem luz; perna torcida.
- Uma captura na janela principal (1920×945).
- Gabarito: nas 9 partidas web, só o estado do herói (os campos novos dos testes e a redação de cinco linhas das dicas).
  Partidas, lances e sorteios iguais.

**Para outra entrega:** o painel do mundo diz "Escuro e sem tocha: Percepção e Destreza −4" antes de você agir, quando
a penalidade ainda não vale (ela entra ao explorar, caçar ou viajar sem tocha). Isso pode merecer um "ao agir".

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

**Protótipo (17/10/2026, em avaliação; nada no jogo):** `ferramentas/prototipos/hud/vida-bloqueada/`.
- **Os números vêm do motor:** o saudável de `Jogador.totais()` (base, talentos, equipamento); o limite, de `max_hp`;
  as fontes, de `sobrevivencia.fontes_penalidade` (corte, mordida, queimadura e fome, que se multiplicam; a perda de
  cada uma na ordem da conta, somando exatamente o bloqueado).
- **A barra mede a vida saudável:** preenchido, o vazio de sempre e, no fim, o trecho bloqueado em hachura diagonal,
  com a marca de limite em latão saindo da barra. O número é `vida/saudável`; no topo, uma etiqueta com a hachura, o
  cadeado e `−N`; a dica explica cada fonte e o que a devolve. Sem penalidade, a barra de sempre.
- **Conferido:** os três estados em 1280×720 (e o limite em 1500×950); uma rodada de luta (a carta só desce); a
  Curandeira (o motor devolve a parte do ferimento como vida, e o bloqueio some); vestir uma peça com +vida máxima (o
  saudável e o limite sobem juntos). A tela fecha com o estado ponto a ponto.
- **Pendências:** a linha "Em você" do uso de itens; integrar em `estado.py`, `paineis.js` e `batalha.js` se aprovado.
  O recurso (costelas, concussão) fica fora, como pedido.

**Aprovado por Jean e integrado na 1.115.0** (17/10/2026):
- **Motor:** `sobrevivencia.vida_bloqueio` (o saudável, o limite, as fontes na ordem da conta e as frases da dica);
  o estado leva `heroi.vida_bloqueio`.
- **Topo e carta:** a barra do herói mede a vida saudável, com o número `vida/saudável`. A etiqueta "−N de vida
  máxima" (amostra da hachura e cadeado, com a dica das fontes) fica na linha das condições, não na coluna dos
  números.
- **Barras estáveis:** o lugar da gota dos ferimentos fica guardado sem ferimento, então as barras do topo têm o mesmo
  comprimento com e sem penalidade (242 px em 1280×720, 302 px em 1500×950, medidos).
- **Coerência dos textos:** "Em você" mostra `93/146 · cura até 104`. O motivo da poção no limite diz o limite e as
  causas (antes: "Sua vida já está cheia." a 104/146). O efeito do Templo diz `(104/146: o limite de agora)`.
- **Regras intactas:**
  - a poção parou no limite (93 → 104);
  - a Curandeira devolveu a parte do corte como vida (91 → 106);
  - vestir a peça subiu o saudável e o limite (146/131 → 171/154);
  - a carta só desce na luta.
- **Gabarito:** mudou só a apresentação: o campo novo no estado, o efeito do Templo e o motivo da poção; nenhuma
  partida, lance ou sorteio (`ferramentas/prototipos/hud/vida-bloqueada/LEIA-ME.md`, "A integração").
- **Fica fora:** as reduções do máximo de Mana, Vigor e Foco. Falta Jean jogar.

### 1.8. Os comandos da luta na linguagem do seletor (integrados na 1.111.0)

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

**Aprovado por Jean (17/10/2026) e integrado na 1.111.0**, junto da solução das lutas cheias (o achado acima):
- **No jogo, sem depender do protótipo:** os comandos em faixas (`15-hud-luta.css`, "a roda de ações"), o carvão mais
  presente à noite, os estados, as cartas contidas, o aviso da cena numa faixa própria e as escolhas de um lugar
  selvagem em faixas (`18-seletor-habilidades.css`, no fim; o motor marca a opção de explorar). As pontas de pincel
  valem para o seletor, a roda e as escolhas. Nenhuma outra tela ganhou faixas.
- **As lutas cheias:** aliados, comandos e inimigos em áreas próprias (`batalha.js`, `distribuir`): a sua fileira
  sempre numa coluna, a faixa dos comandos reservada, os inimigos à direita, em duas colunas só onde cabem fora da
  faixa (1920×1080), numa coluna mais alta nas janelas menores, e a arena cresce. A mira e o Voltar ficam na faixa dos
  comandos. Quem sai no meio da luta deixa a vaga até o próximo lance. Quem foi invocado e cai sai da arena, dos dois
  lados (antes só o servo do herói saía): os mortos de um guardião que invoca não se acumulam em cartas.
- **Os maiores grupos reais** (o robô de `tests/arena.py`, 1.800 lutas): até 6 aliados (necromante com a comitiva de 2,
  a Legião de Ossos e o Rei dos Mortos; a comitiva tem no máximo 2 companheiros, o cenário com três é artificial), até
  6 inimigos num bando (caídos à noite com a comitiva e o xamã de escolta), até 4 vivos com um guardião que invoca (a
  aranha-rainha chegou a 10 cartas numa luta longa antes desta entrega, com os mortos acumulados).
- **Conferido** (`ferramentas/prototipos/hud/fotografar_lutas_cheias.mjs`, o jogo de antes num checkout do `5795a9a` e o
  de agora, com os mesmos dados; registro no `LEIA-ME.md` de `ferramentas/prototipos/hud/`, "A integração"): 5 lutas
  (poucos com um alvo derrotado, a noite com Erguer Servo, 5 lobos com a comitiva e o lobo do patrulheiro, o maior real
  6 × 6, os nomes mais longos) em 1280×720, 1500×950 e 1920×1080; antes, os comandos (e às vezes a própria mira) cobriam
  cartas em 7 das 9 combinações cheias; depois, nada cobre nada em nenhuma das 15. Abrir, alternar e fechar menus não mexe em carta nem
  rolagem; a saída e a entrada SIMULADAS de um inimigo não mexem nas outras cartas; mouse, teclado, cliques depressa,
  tecla segurada e movimento reduzido como antes (a roda agora não anima com movimento reduzido).
- **Limite conhecido:** em 1280×720, numa luta de 5 ou 6 inimigos com os efeitos à mostra, a arena fica alta e sobram
  ~120 a 160 px para o registro; o seletor de Habilidades abre com uma fileira à vista e rola dentro (como já fazia
  quando faltava altura). Uma saída possível, ainda não proposta: os efeitos na linha do nome nas lutas cheias.

### 1.9. As escolhas da página em faixas (integradas na 1.113.0)

**Pedido de Jean:** as faixas, que a 1.111.0 limitou ao lugar selvagem, como a apresentação comum das escolhas
narrativas e das ações da página. **Integrado (1.113.0; a regra pela função na 1.113.1):** as escolhas narrativas, as
da partida em andamento fora da luta, ganham as faixas (o lugar, a vila, os eventos e diálogos com os testes de
atributo, as cenas da missão, a viagem), sem depender do lugar, do texto nem de marca do motor; o título, a lista de
saves e a criação do personagem (antes da partida) ficam de fora, a criação para a etapa própria; a etiqueta do teste, a seta ›, a secundária e a
indisponível legíveis no carvão e no marfim. Ficam com o próprio tratamento: a luta, o título, as confirmações, o
achado, a doca, os caminhos, os prédios da vila e as telas desenhadas (mercado, Inventário, fogueira, serviços). O
mapa dos usos e a conferência (14 casos reais, antes × depois, conteúdo igual nas 26 comparações) estão em
`ferramentas/prototipos/hud/escolhas-faixas/LEIA-ME.md`. Falta Jean jogar.

### 1.10. A composição compacta das lutas cheias (integrada na 1.114.0; histórico do protótipo abaixo)

**Pedido de Jean:** nas lutas cheias em 1280×720, todas as habilidades à vista sem rolar, com a descrição legível,
sem perder o que a 1.111.0 aprovou. **Só no protótipo** (`ferramentas/prototipos/hud/compacta/`, detalhes, medidas e
comparações no `LEIA-ME.md` de lá); o jogo não mudou. Os grupos reais conferidos no código: até 6 aliados e 6
inimigos. Duas alternativas contra a produção, com os mesmos dados, em 1280×720, 1500×950 e 1920×1080:
- **A, arena compacta** (os efeitos na linha do nome, o seletor em três colunas): a luta maior continua rolando (5 de
  7) e, com 3 ou 4 efeitos, os nomes das cartas são cortados. Descartada como regra; os efeitos na linha do nome
  ficam fora.
- **B, seletor na ficha** (quando a lista inteira não cabe embaixo, ele abre sobre a coluna da ficha do herói, numa
  coluna): 7 de 7 habilidades e 5 de 5 itens em todos os casos, a descrição de 150 a 179 px, a arena intocada; nas
  lutas pequenas e nas janelas maiores, igual à produção. Custos: cobre a ficha enquanto aberto; nomes em duas ou
  três linhas na coluna estreita (o custo de dois recursos do patrulheiro).
- **Recomendação:** B. **Limite que fica:** com muitos efeitos em 1280×720 o registro encolhe (0 a 33 px no caso
  simulado extremo), porque a arena cresce; é outra entrega, se aparecer jogando. Falta Jean avaliar.

**Rodada 2 (17/10/2026), B aprovada como direção; só no protótipo** (`ferramentas/prototipos/hud/compacta/rodada2/`):
- **O custo numa linha própria na coluna da ficha (b2): escolhido.** Nenhum nome do arqueiro em três linhas, os custos
  numa coluna, o Voltar na linha do título, a descrição igual ou maior; mesma letra. Corrigido também o que a rodada 1
  deixou passar: o seletor ficava na tela durante a mira. A ficha coberta fica inerte, o Tab vai do seletor à arena, e
  redimensionar acompanha a ficha sem perder a examinada, o foco ou o lugar das cartas.
- **O registro sem espaço é real:** o robô (1.200 lutas, `compacta/efeitos_reais.py`) mostra as 6 cartas de um bando
  de caídos com efeito ao mesmo tempo com 5 das 6 especializações, já no turno 2 ou 3. Com os efeitos de um momento
  real, sobram 19 a 51 px em 1280×720. Proposta: nas lutas que deixariam menos de 140 px, o registro vai, para a luta
  inteira, para a coluna do mundo (~13 linhas), por cima do minimapa, da missão e dos caminhos. Compromissos: esses
  três cobertos durante a luta; linhas mais estreitas; nada muda abaixo de 1100 px.
- **Achado de regra, sem mudar nada:** o necromante chega a 7 aliados, porque o Senhor dos Mortos dispara de novo
  quando o xamã revive um caído (`talentos._senhor_mortos`, `len(cb.mortos) == 1`).
- **Recomendação:** integrar a b2 e o registro na coluna do mundo juntos. Falta Jean avaliar.

**Aprovado por Jean e integrado na 1.114.0** (a correção do Rei dos Mortos antes, na 1.113.2, em commit próprio):
- **O seletor (`app/escolhas.js`, `dispor`):** abre embaixo da arena quando cabe; senão, sobre a ficha, com o custo
  embaixo do nome e o Voltar no título. A ficha fica inerte, a mira o tira, e redimensionar o dispõe de novo sem
  fechar (a examinada e o foco ficam).
- **O registro (`app/paineis.js`, `acomodarRegistro`):** a conta é feita no começo da luta e a cada novo tamanho de
  janela. Na falta de espaço, vai para a coluna do mundo; sem ela (abaixo de 1100 px), para a da ficha; sem nenhuma
  (abaixo de 920 px), fica embaixo com 240 px, e a página rola. Efeitos entrando e saindo não o mudam de lugar, e o fim
  da luta devolve tudo.
- **Os grupos:** depois da correção, 6 × 6 é ao mesmo tempo o limite das regras e o maior grupo visto pelo robô.
- **Conferido:** igual ao protótipo aprovado com os mesmos dados; a passagem 1500 → 1280 → 1050 → 900 → 1280 → 1500
  com a luta em andamento; teclado e movimento reduzido (`ferramentas/prototipos/hud/compacta/integracao/LEIA-ME.md`).
- **Limitações:** abaixo de 920 px o seletor e o registro pedem a rolagem da página; entre 920 e 1100 px o seletor
  aberto cobre o registro. Falta Jean jogar.

### 1.11. Estudo: a nova direção visual da HUD principal (não escolhido: fica a HUD de produção)

**Pedido de Jean (17/10/2026):** a aparência do conjunto (topo, ficha, cartas, coluna do mundo, relação com os
comandos e o seletor aprovados), só no protótipo, a partir de uma imagem de referência dele (carvão e tinta, marfim,
borda externa gasta, contornos que se desfazem antes de fechar) e de Clair Obscur pela hierarquia. Uma proposta.

**O estudo** (`ferramentas/prototipos/hud/direcao/`; decisões e compromissos no LEIA-ME de lá):
- **As colunas:** sem as molduras de ferro e os rebites. Ficam carvão com a borda externa gasta (uma máscara de
  pincel em CSS) sobre um fundo quente.
- **O contorno aberto:** dois cantos e traços que se apagam, nas colunas, nos retratos, nas cartas, nos rastros e nos
  caminhos.
- **A tipografia:** nomes do herói e do lugar em serifa marfim; títulos de seção em versal espaçada.
- **O latão:** só em detalhe (a vez, o nível, o talento, a missão).
- **A seleção:** a faixa de marfim aprovada, que continua a marca mais forte.
- **A dica "Testes do d20":** nomes em marfim, totais em latão, penalidades em vermelho queimado, e só as duas regras
  do d20 em destaque no rodapé.

**Conferido:** atual × proposta com os mesmos dados a 1920×945 (a exploração, com a dica, e a luta, com o seletor e
a mira), sem erros, com as interações de pé. Nada mudou de lugar. Falta Jean avaliar; o jogo e a versão continuam os
da 1.118.0.

**Avaliação de Jean (17/10/2026):** a proposta ficou longe da referência. Antes de estender o visual, mudar o método.

**Prova de fidelidade da coluna da ficha** (`ferramentas/prototipos/hud/direcao/ficha/`, em avaliação, nada no jogo).
A referência foi salva como `direcao/referencia.png`, e o método mudou:
- **A comparação:** lado a lado com a referência na mesma escala, também ampliada a 2× na borda.
- **A arte decorativa:** imagem própria, de um gerador reproduzível (`gerar_arte.py`): o carvão com variação discreta e
  a borda rasgada (manchas grandes, fibras, trechos que se desfazem, respingos), mais o papel gasto da margem.
- **O CSS:** só o conteúdo (retrato de 120 px, nome de 40 px, atributos de 26 px com ícones de 32, títulos em versal
  espaçada, o fio vertical).

A coluna ficou com 348 px, ganha da margem; o centro e a arena seguem com 1088 px. A proposta anterior ficou como
estava. Os compromissos e o que ainda difere estão no LEIA-ME de lá.

**Rodada 2 (18/10/2026):** a decoração passou a ser a pintura de Jean
(`direcao/Painel vertical em tinta escura.png`), aplicada como está.
- **O encaixe:** escala 0,5 exata, numa peça própria atrás da coluna, transbordando a caixa para a área escura sólida
  ficar por trás do conteúdo. Nenhuma mancha foi atenuada.
- **O conteúdo:** a mesma composição da rodada 1.
- **A rodada 1:** preservada para comparar.

**Avaliação de Jean (18/10/2026):** a ficha com a pintura está aprovada como base visual.

**O conjunto** (`ferramentas/prototipos/hud/direcao/conjunto/`, em avaliação, nada no jogo): a direção estendida ao
topo, ao centro e ao mundo, com peças derivadas da pintura (`derivar_pecas.py`), sem esticar pinceladas.
- **A periferia:** o desgaste fica nos lados de fora (a ficha e o mundo, com a pintura espelhada).
- **O centro:** carvão liso do miolo da pintura, sem moldura, com emendas retas e escuras; o cenário como
  protagonista.
- **O topo e a doca:** sem ferro.
- **O resto do acabamento:**
  - contornos abertos em retratos, cartas, missão, caminhos e na mira;
  - o mapa com o rasgo da pintura;
  - nomes e títulos em marfim;
  - o título do seletor grande e espaçado;
  - a seleção marfim como o destaque mais forte.
- **Conferido:** a 1920×945, na exploração e na luta (seletor, mira e golpe). O centro tem o mesmo tamanho, nada rola,
  nada deu erro.
- **A peça que falta:** uma pintura horizontal no mesmo material para a borda do topo.

**O topo pintado** (18/10/2026; `ferramentas/prototipos/hud/direcao/topo/`, em avaliação, nada no jogo):
- **A decoração:** a pintura horizontal de Jean (`direcao/topo.png`), recortada sem esticar. A barra fica com 46 px e as
  pontas do rasgo descem ~22 px sobre as colunas.
- **A atenuação:** as manchas bege das pontas foram escurecidas só atrás dos textos.
- **Os estados:** a vida máxima bloqueada e a habilidade indisponível foram conferidas, legíveis e com os motivos do
  motor.

**Decisão de Jean (18/10/2026), depois de jogar as duas versões: fica a HUD de produção.** A direção com pintura nas
colunas e no topo não será integrada.
- **O estudo** (`ferramentas/prototipos/hud/direcao/`: a proposta, a ficha nas duas rodadas, o conjunto, o topo, a
  comparação jogável e as pinturas `Painel vertical em tinta escura.png` e `topo.png`) fica guardado como estudo não
  escolhido para a HUD principal. Pode servir de referência para outras telas, mas nenhum reaproveitamento está
  aprovado automaticamente.
- **A aprovação da ficha** valia só como base do estudo. Ela não autoriza integrar a ficha isolada nem transferir
  tipografia, espaçamentos, cores ou outras partes do protótipo para a produção.
- **Continuam em produção e aprovados:** a HUD atual e os menus de pincelada (comandos da luta, os seletores de
  Habilidades e Itens, as escolhas narrativas em faixas).
- **Pendência independente que ficou só no protótipo:** o refinamento de cores da dica "Testes do d20". Era nomes em
  marfim, totais em latão, parcelas com mais contraste, penalidades em vermelho queimado e, no rodapé, só "20 sempre
  passa" e "1 sempre falha" em destaque. Na produção (1.118.0) a dica tem os números do motor, mas o nome e o total
  vêm juntos num negrito só e o rodapé inteiro fica em amarelo. Está em `direcao/direcao.js` e no fim de
  `direcao/conjunto/conjunto.css`. Fazer numa entrega própria, se Jean pedir; não vem junto com a HUD.

**Situação anterior (18/10/2026, antes da decisão): em avaliação, sem aprovação para integrar.**
- **A ficha:** aprovada como base do estudo.
- **A tela inteira:** a decisão continua aberta. A dúvida é se a pintura permanente combina com a pixel art ou chama
  mais atenção que o mundo.
- **Os menus de pincelada:** os comandos, o seletor e as escolhas continuam aprovados e em produção.
- **A comparação jogável:** `ferramentas/prototipos/hud/direcao/comparar/` (produção × protótipo com uma cópia do save
  de Jean).

### 1.12. Desvio visual após os itens — flechas, estados, criaturas e navegação (etapa 1E)

**Decisão de Jean (19/10/2026):** depois de fechar os itens, tratar estes símbolos antes de retomar a sequência
das telas e dos serviços. Criaturas e navegação já constavam no escopo de 1.2, mas sem esta ordem. Buffs e estados
agora têm prioridade independente dos ícones de habilidades. Esta seção organiza o trabalho, não aprova desenhos.

**Ordem do bloco:**

| Ordem | Entrega | Resultado e limites |
|---|---|---|
| 1E.1 | **Contagem de flechas do Arqueiro — prioridade** | **Concluída na 1.155.0** (a F2). Ícone próprio legível junto do número, principalmente na carta de combate; conferir também custos e outros contadores para decidir os usos. Preservar quantidade, avisos de poucas/zero, dicas e áreas de clique |
| 1E.2 | **Buffs e estados, começando por Firme — prioridade** | **Concluída: os 17 estados, 1.155.0–1.161.0.** Auditar o catálogo e os usos reais, trabalhar em pequenos grupos por função; símbolos reconhecíveis em tamanho real e distintos entre si, sem depender só da cor |
| 1E.3 | **Inimigos e pets/animais** | **Em andamento:** Afogado e Ilse (1.162.0), Lobo e Bandido (1.163.0), os três animais do patrulheiro (1.164.0–1.165.0); faltam as demais criaturas, os chefes e as invocações. Ícones/retratos usados em cartas, painéis e Bestiário, conforme os usos de cada criatura. Mobs, chefes e pets em lotes pequenos; preservar identidade e silhueta reconhecíveis. Não refazer os retratos aprovados do herói e da comitiva por extensão |
| 1E.4 | **Caminhos/destinos e ícones do minimapa/mapa** | **Depois da 1E.3.** Auditar os dois contextos; linguagem coerente para lugares, serviços, perigos e marcadores que realmente existam. Conferir estados visitado/atual/bloqueado quando aplicáveis, sem alterar geografia, regras ou navegação |

**Flechas — distinguir os papéis antes de desenhar:** na produção consultada, a aljava de equipamento e do recurso
do topo já é a arte aprovada da 1.122.0. A contagem na carta ainda usa `S("flecha", 1)` em `batalha.js`
(`.carta-flechas`). Isso é um uso visual próprio; não implica rejeitar a aljava nem substituir automaticamente
projéteis e todos os usos de `flecha`. Levantar também os indicadores de custo antes de decidir os compartilhamentos.

**Firme — significado antes do símbolo:** `rpg/estados.py` usa hoje o `cadeado`, família `protecao`, para a proteção
temporária após perder o turno; a dica informa que não pode ser atordoado/congelado agora. Jean considera o cadeado
pouco representativo. Procurar uma imagem de recuperação/estabilidade ou resistência temporária a nova perda de
turno, distinta de ganho de Defesa, Guarda e atordoamento. O desenho final continua em aberto: apresentar proposta
em tamanho real e no conjunto dos estados, sem mudar nome, duração, imunidades ou outras regras para adequá-las à arte.

**Primeiro par proposto (20/10/2026, em avaliação, nada integrado):** a flecha da carta do Arqueiro (F1) e o Firme (R1),
em 16 px, em `ferramentas/prototipos/hud/itens-lote-noite/flechas_firme/` (o levantamento, as referências e as fotos no
`LEIA-ME.md` do lote). A troca futura atinge só esses dois papéis: um desenho próprio para `.carta-flechas` e um ícone
próprio para o estado `firme`; a aljava, os outros usos de `flecha` e os outros cadeados ficam. Segunda rodada (20/10/2026): a F2 (as penas na traseira, menores, sem madeira atrás) e a R2 (sem as faíscas, o furo dos elos mais legível), **aprovadas e integradas na 1.155.0** por papéis próprios (`Icones.contadorFlechas` e `Icones.estado`), com o sprite `flecha` e o `cadeado` intactos nos outros papéis. Os outros estados e o resto do bloco 1E continuam com os sprites do jogo.

**Levantamento dos estados (20/10/2026, `rpg/estados.py`).** Todo ícone de estado aparece em 16 px de arte (~18 px de tela
a 1920×945, pelo zoom da HUD) em dois lugares da luta: o chip da carta (`.ef`, com os turnos) e o selo do estado que
chega (`.faixa-acao.selos`, ▲/▼); a família pinta o brilho da carta (`com-<família>`) e a borda do chip. O Grimório e a
orientação descrevem os estados por texto. "Compartilha" lista os outros papéis do mesmo sprite (as habilidades e os
talentos com o mesmo `icone`, e outros usos na interface): trocar o desenho de um estado é sempre por papel próprio
(`Icones.estado`), nunca no sprite.

| Estado | Efeito real | Ícone atual | Compartilha | Arte |
|---|---|---|---|---|
| Em guarda (`guarda`, +) | dano recebido −v% em todo golpe que acerta (Erguer Escudo: −50% por 2 turnos; Ordem da Fera: −30% no animal); ativa o Revide do Broquel do Vigia | `escudo` | Erguer Escudo; os talentos Aura de Proteção, Escudo Rúnico, Muralha e Pele de Ferro; o escudo/apoio vazio e outros usos (todos ficam com o sprite) | **final** (G1, 1.156.0, `estado-guarda`) |
| Fortalecido (`fortalecido`, +) | dano causado +v% | `estado-fortalecido` (próprio) | nenhum (a `espada` ficou em: Investida; Contra-ataque, Golpe Brutal; o elemento físico e outros) | **final** (1.159.0; a R2 do `39f85d92`, sem retoque) |
| Fúria (`furia`, +) | dano causado +v% (soma com o Fortalecido) | `estado-furia` (próprio) | nenhum (o `machado` ficou em: Redemoinho) | **final** (1.158.0; a proposta do `b17ab3dd`, sem retoque) |
| Frenesi (`frenesi`, +) | cada abate soma dano até o fim da luta | `estado-frenesi` (próprio) | nenhum (o `raio` ficou em: Julgamento Divino) | **final** (1.159.0; as garras do `b17ab3dd`, sem retoque) |
| Iniciativa (`iniciativa`, +) | o primeiro golpe deste turno sai +v% mais forte | `estado-iniciativa` (próprio) | nenhum (a `bota` ficou em: a reserva dos pés (a bota de couro)) | **final** (1.161.0; a barra larga da terceira rodada, `69c6ded3`; o estouro guardado como não escolhido, sem retoque) |
| Esquiva (`esquiva`, +) | +v na chance de esquiva, até o teto (Passo Ágil: +30% por 2 turnos; Desaparecer: +50% por 1) | `estado-esquiva` (próprio) | nenhum (a `folha` ficou na Fúria da Natureza, no Pés Leves, no Antídoto e na Agilidade das celebrações e do Inventário) | **final** (a E6 corrigida, 1.157.0; a origem e a licença da referência pendentes; as tentativas E1 a E5 no protótipo) |
| Barreira (`barreira`, +) | absorve v de dano | `estado-barreira` (próprio) | nenhum (o `escudo_azul` ficou em: Barreira Arcana) | **final** (1.160.0; o golpe na película da terceira rodada, `33f97dde`; a cúpula e a parede guardadas como não escolhidas, sem retoque) |
| Furtivo (`furtivo`, +) | o próximo ataque é crítico garantido | `estado-furtivo` (próprio) | nenhum (o `olho` ficou em: Marcar Presa; Canalização, Olho de Águia; a névoa e outros) | **final** (1.158.0; a proposta do `b17ab3dd`, sem retoque) |
| Provocando (`provocando`, +) | os inimigos atacam ele | `estado-provocando` (próprio) | nenhum (a `caveira` ficou em: Execução, Fúria Cega; Assassino, Colheita, Golpe Sombrio, Imortal, Legião de Ossos, Rei dos Mortos; derrota, fome e outros) | **final** (1.161.0; o busto do `b17ab3dd` com a figura branca do `9e4ec85a`, sem retoque) |
| Firme (`firme`, +) | depois de um atordoamento ou congelamento, não pode ser atordoado nem congelado de novo naquele turno | `estado-firme` (próprio) | nenhum (o `cadeado` ficou nos outros papéis) | **final** (R2, 1.155.0) |
| Veneno (`veneno`, −) | dano por turno | `estado-veneno` (próprio) | nenhum (a `gota_verde` ficou em: Flecha Envenenada; os serviços) | **final** (1.160.0; a gota sem a poça da terceira rodada, `69c6ded3`, sem retoque) |
| Sangramento (`sangramento`, −) | dano por turno | `estado-sangramento` (próprio) | nenhum (a `gota` ficou em: Sede de Sangue; Pacto Sombrio, Pontas Venenosas, Sede Insaciável; os ferimentos e os serviços) | **final** (1.158.0; a proposta do `b17ab3dd`, sem retoque) |
| Chamas (`queimadura`, −) | dano por turno; a Combustão detona o que falta arder | `estado-queimadura` (próprio) | nenhum (a `chama` ficou em: Bola de Fogo; Brasas Eternas, Chama Viva, Coração Ardente, Frenesi, Ignição; o Vigor, o Poder e a Pena de Fênix) | **final** (1.159.0; a R2 do `805c238d`, sem retoque) |
| Maldição (`maldito`, −) | dano por turno e −40% de defesa | `estado-maldito` (próprio) | nenhum (a `gota_roxa` ficou em: Drenar Vida) | **final** (1.158.0; a proposta do `b17ab3dd`, sem retoque) |
| Atordoado (`atordoado`, −; também "congelado") | perde o próximo turno; depois fica Firme | `estado-atordoado` (próprio) | nenhum (a `estrela` ficou em: Combustão; Eficiência, Luz Curativa; dezenas de usos genéricos da estrela) | **final** (1.160.0; as três estrelinhas da terceira rodada, `33f97dde`, sem retoque) |
| Enfraquecido (`enfraquecido`, −) | dano causado −25% | `estado-enfraquecido` (próprio) | nenhum (o `osso` ficou em: Erguer Servo) | **final** (1.159.0; a R2 do `805c238d`, sem retoque) |
| Marcado (`marcado`, −) | recebe mais dano de todos | `estado-marcado` (próprio) | nenhum (a `flecha` ficou em: Tiro Certeiro; Mira Firme, Tiro de Abertura; o custo das habilidades, a orientação, o elemento "à distância", os projéteis) | **final** (1.158.0; a proposta do `b17ab3dd`, sem retoque) |

**Os 14 restantes (21/10/2026, lote da madrugada):** uma proposta por estado em sete lotes, só no protótipo, em
`ferramentas/prototipos/hud/itens-lote-noite/estados_restantes/` (as folhas `lote1.png` a `lote7.png`, a prancha
`geral.png` com os 17, as tentativas guardadas e a avaliação no `LEIA-ME.md` da pasta). **Aprovados por Jean e
integrados na 1.158.0, sem retoque:** Sangramento, Maldição, Marcado, Furtivo e Fúria (o chip e o selo; o Marcado não
tem selo de chegada no jogo, porque as duas fontes dele aplicam o estado direto). Os outros nove seguem no protótipo,
numa segunda rodada de ajustes: as alternativas novas ao lado dos candidatos preservados (as folhas `rodada2-*.png` e a prancha `geral.png`, 21/10/2026), em avaliação. **Integrados na 1.159.0, sem retoque:** as Chamas (R2), o Fortalecido (R2), o Enfraquecido (R2) e o Frenesi (as garras da primeira rodada). O Fortalecido e o Frenesi não têm selo de chegada no jogo (o Grito de Guerra dispensa o selo; o uivo, o grito dos inimigos e o talento aplicam direto). **Integrados na 1.160.0, sem retoque (a terceira rodada):** o Veneno (a gota sem a poça), o Atordoado (as três estrelinhas, estático, também no congelado) e a Barreira (o golpe na película); os três com selo de chegada. **Integrados na 1.161.0, sem retoque:** o Provocando (a figura branca do `9e4ec85a` com as três setas da composição original) e a Iniciativa (a barra larga; o estouro guardado como não escolhido). **Os 17 estados do catálogo estão concluídos** (conferido: 17 em `rpg/estados.py`, 17 no `ESTADO` de `icones.js`, todos com o 16 e o @2x); a prancha final em `estados_restantes/estados-final.png`.

**Primeiro par de estados (20/10/2026):** Em guarda (G1, o escudo de ferro), **integrado na 1.156.0**; Esquiva
(E1, a rajada de vento, recusada por lembrar um símbolo meteorológico; E2, os crescentes, recusada por não comunicar
evasão; a E6, a figura em movimento copiada da referência e corrigida, **integrada na 1.157.0**), em 16 px, em `ferramentas/prototipos/hud/itens-lote-noite/estados_guarda_esquiva/`.

**Levantamento de inimigos, chefes, animais e invocações (1E.3, 21/10/2026; em andamento, nada desenhado):** em
`ferramentas/prototipos/hud/criaturas/` (o `LEIA-ME.md`, a tabela `levantamento.md`, as folhas `tracos.png`,
`compartilhamentos.png` e `referencias.png`, as capturas a 1920×945). O desenho de uma criatura sai dos **traços**
(`dados.retrato`), não da espécie: 57 entidades, 51 delas com desenho de criatura servidas por **9 sprites de 16×16**
(`caveira` 14, `fera` 12, `humano` 10, `voador` 4, `etereo` 3, `demonio` 3, `planta` 2, `construto` 2, `corrompido` 1),
todos do commit inicial da interface em pixel art, sem registro de aprovação. Aprovados e preservados: os retratos dos
heróis e da comitiva (`retratos.js`) e as figuras de cena da Ilse e da sacristia. Problemas: o mesmo rosto de lobo no
Lobo inimigo, na Aranha e no Urso do herói; o troll e o Rei Troll na caveira (o traço `gigante` não tem retrato); a Ilse
com a caveira genérica na carta; o bandido como todo humano (os vultos da sacristia, os chefes, o antagonista). O
espaço real é a **cabeça** de 16×16 (a carta a 2×, 32 px; o Bestiário e o mural a 3×). Recomendação do primeiro par:
**Lobo e Bandido** (os mais frequentes do Vale, donos dos dois desenhos mais compartilhados); em seguida Afogado e Ilse.
A escolha fica com o Jean.

**Primeiro par escolhido pelo Jean (21/10/2026): o Afogado e a carta da Ilse** (proposta, nada no jogo), em
`ferramentas/prototipos/hud/criaturas/afogado_ilse/`: cabeças de 16×16 no formato dos retratos de carta aprovados,
fontes pelo MCP, a folha `afogado-ilse.png` com as cartas na luta a 1920×945, o Bestiário e a Ilse com a cena dela.
Segunda rodada (21/10/2026, proposta): a Ilse com fios de alga soltos e na frente do rosto (`ilse-r2`) e o Afogado B,
com outra construção do rosto (`afogado-b`); as primeiras preservadas; a folha `afogado-ilse-r2.png`.
Terceira rodada (21/10/2026, proposta): a Ilse transposta da referência gerada (`ilse-r3`) e três Afogados livres na
escala da comitiva (`afogado-cabelo`, `afogado-perfil`, `afogado-cranio`); a folha `afogado-ilse-r3.png`.
**No jogo desde a 1.162.0:** o Afogado C (pela família) e a Ilse R3 com o olho ajustado (pela chave da capela),
`dados.retrato` e `Icones.criatura`; as outras criaturas continuam pelos traços (o par seguinte fica com o Jean).
**Segundo par (21/10/2026, proposta): o Lobo e o Bandido**, duas direções de cada em
`ferramentas/prototipos/hud/criaturas/lobo_bandido/` (o lobo de frente e de perfil; o desertor e a salteadora), as
folhas `lobo.png` e `bandido.png`; o alcance previsto só nas famílias `lobo` e `bandido`. Segunda rodada: o Lobo A
com a base de quadrúpede (e o ajuste do olhar) e três Bandidos novos (o brutamontes, o do chapéu, o da faca); as
folhas `lobo-r2.png` e `bandido-r2.png`.
**No jogo desde a 1.163.0:** o Lobo "só a base" (com a limpeza de três sobras) e o Bandido da faca, pela família.
**Reservado:** o Bandido do chapéu, conceito para um possível chefe futuro, fora do jogo (sem chefe, nome, história,
atributos nem mapeamento); fonte, PNGs e prévia em `ferramentas/prototipos/hud/criaturas/lobo_bandido/` (a seção
"Conceito reservado" do `LEIA-ME.md`).
**Os animais do patrulheiro (21/10/2026, proposta):** duas direções do Urso Pardo e do Falcão Peregrino e o teste do
retrato do Lobo integrado no Lobo Cinzento aliado, em `ferramentas/prototipos/hud/criaturas/animais/`; a carta aliada e
o painel da comitiva são os usos reais. O `fera` e o `voador` continuam; nada aprovado. A transposição das duas
referências geradas (`urso-t`, `falcao-t`; as referências em `ferramentas/arte/referencias/icones/`), a folha
`transposicao.png`; o último ajuste (`urso-t2`, `falcao-t2`, a folha `ajuste.png`).
**No jogo desde a 1.164.0:** o Urso Pardo e o Falcão Peregrino do patrulheiro (o `t2` de cada), pelo tipo do animal,
na carta aliada e no painel da comitiva; o Lobo Cinzento continua no `fera`.
**No jogo desde a 1.165.0:** o Lobo Cinzento com o mesmo arquivo do Lobo inimigo (`retrato-lobo`), sem redesenho, pelo
tipo do animal; o mesmo rosto é de propósito (o lado, o nome e a borda separam os papéis). **Os três animais do
patrulheiro estão concluídos.** O `fera` das outras criaturas e a figura do acampamento continuam.
**O par seguinte (21/10/2026, proposta): a Aranha Gigante e o Troll**, duas direções de cada em
`ferramentas/prototipos/hud/criaturas/aranha_troll/` (a aranha de frente e de lado em ameaça; o troll de frente e de
perfil com a corcunda), as folhas `aranha.png` e `troll.png`; o alcance previsto só nas famílias `aranha` e `troll` (a
Rainha Aracnídea e o Rei Troll fora). Segunda rodada: três de cada pelas referências geradas (a aranha de frente; o
troll de carne), as folhas `aranha-r2.png` e `troll-r2.png`.
**No jogo desde a 1.166.0:** o Troll da montanha (o `troll-1`, em três quartos), pela família; o Rei Troll continua na
caveira e a Aranha no protótipo.
**Propostas (21/10/2026):** o Rei Troll a partir do Troll 2 (a coroa de sucata, não escolhida; a coroa dourada pela
referência gerada, `rei-troll-ouro`, sem mexer no rosto) e a Aranha 2B (as quelíceras e as presas reconstruídas, os
olhos pequenos); as folhas `rei-aranha.png` e `rei-coroa.png`. O ajuste das pontas da coroa (`rei-troll-ouro2`, a
folha `rei-pontas.png`).
**No jogo desde a 1.167.0:** o Rei Troll (`rei-troll-ouro2`, pelo id do guardião) e a Aranha gigante (`aranha-2b`, pela
família, com as que a Rainha invoca); a Rainha Aracnídea continua no `fera`.
**O par seguinte (21/10/2026, proposta): a Rainha Aracnídea e o Esqueleto**, duas de cada em
`ferramentas/prototipos/hud/criaturas/rainha_esqueleto/`; o alcance previsto: a Rainha pelo id do guardião, o Esqueleto
pela família (o servo aliado do Necromante e os chefes mortos-vivos fora); as folhas `rainha.png` e `esqueleto.png`.
**No jogo desde a 1.168.0:** a Rainha Aracnídea (`rainha-a`, sem retoques, pelo id da guardiã; as aranhas que ela
invoca continuam com o retrato da Aranha gigante); a folha `rainha-final.png`. O Esqueleto segue no protótipo: o
A2 (o A desenvolvido pela referência gerada do Jean; a folha `esqueleto-a2.png`) e o A2n (o nariz refeito;
`esqueleto-a2n.png`, a base aprovada); sobre ele, o sorriso contido e o marcado (S1 e S2, `esqueleto-sorriso.png`),
não aprovados; o C, a nova direção pela segunda referência gerada, não aprovado (o sorriso de comercial); o C2, com a boca refeita pelas
caveiras pequenas de referência (`esqueleto-c.png`), também não; **refeito do zero** em
`ferramentas/prototipos/hud/criaturas/esqueleto_novo/` (três direções: o guarda morto de elmo, o encapuzado, a caveira
nua em três quartos; a folha `esqueleto-novo.png`). **Escolhida a E1** (o guarda morto) para o esqueleto básico, com
a aba do elmo limpa (`esqueleto-e1r`); continua no protótipo. **Conceito reservado:** a E2 (o encapuzado), para um
possível mago esqueleto, com a fonte e os PNGs em `esqueleto_novo/`; sem espécie, habilidades nem mapeamento. A E3 não
foi escolhida.

**Pendências registradas (21/10/2026, pedido do Jean; levantamento antes de desenhar):**
- **A figura do animal no acampamento, por tipo de animal** (o lobo, o urso e o falcão do patrulheiro): conferir se
  cada um já escolhe uma figura própria, os caminhos, os tamanhos e os compartilhamentos, e propor a atualização de cada
  uma na linguagem da cena, com a identidade dos retratos aprovados. Não desenhar nem integrar antes da avaliação.
- **O ícone do comando Atacar do Arqueiro:** testar o arco de equipamento aprovado no tamanho real do comando; conferir
  o desenho que o comando usa com uma Besta equipada, sem mudar essa regra; uma conferência rápida dos ataques básicos
  das três classes para achar outros desenhos antigos que ficaram fora da revisão (só registrar, sem ampliar o lote).
- **O levantamento (21/10/2026; `ferramentas/prototipos/hud/acampamento_atacar/`, a folha `levantamento.png`):** na
  fogueira, o lobo e o urso recebem o mesmo sprite `fera` (a cabeça de lobo do traço) e o falcão o `voador` (o
  morcego); a proposta é uma figura de 16×16 de corpo inteiro por animal, num papel próprio pelo tipo (os sprites dos
  traços não mudam). No Atacar, o ícone é da classe (`icone_ataque`), e com a Besta continua o `arco`; o arco aprovado
  (`arco-32`) cabe exato no comando e lê melhor que o sprite (teste só na página). Na conferência, o **Atacar do Mago**
  também usa o sprite antigo (`cajado`); a página do ataque básico no Grimório fica com os ícones de habilidade (etapa
  8). Nada desenhado nem integrado.
- **No jogo desde a 1.169.0:** o arco aprovado (`arco-32`, o arquivo do equipamento) no Atacar do Arqueiro, pelo papel
  `ACAO` (o ícone continua o da classe: com a Besta, o mesmo arco); o Tiro Duplo e o contrato de caça continuam com o
  sprite. O cajado do Mago segue em teste no protótipo.
- **Propostas (21/10/2026; nada no jogo):** os três animais do acampamento (o lobo deitado, o urso sentado, o falcão no
  toco; 16×16 de corpo inteiro, conferidos na cena) e o teste do cajado aprovado no Atacar do Mago; a folha
  `ferramentas/prototipos/hud/acampamento_atacar/animais-cajado.png`. A seleção futura pelo tipo, num papel próprio.
  Segunda rodada do lobo (a anatomia e a pose) e do urso (refeito como urso pardo sentado); a folha `rodada2.png`.
  Terceira rodada, pelas duas referências geradas do Jean (o lobo deitado, o urso sentado), com as guias ocultas; a
  folha `rodada3.png`. Quarta rodada, o refinamento na cena (o lobo com os claros contínuos e o nariz; o urso com a
  cabeça larga, o focinho curto, o corcunda, as patas de base larga e a coxa num volume); a folha `rodada4.png`. O lobo r5, mais alto (a cabeça maior, o tronco grosso); a folha
  `lobo-r5.png`. A cabeça da r5 não foi aprovada: três cabeças de companheiro sobre o mesmo corpo (c1, perfil
  suave; c2, três quartos para o jogador; c3, livre); a folha `lobo-cabecas.png`.
- **No jogo desde a 1.170.0:** o lobo c2 na fogueira, pelo tipo do animal (o papel `FIGURA_ANIMAL`, `figura-lobo-16`);
  o urso e o falcão continuam nos sprites `fera` e `voador`, em avaliação.
- **Os quatro pares seguintes (22/10/2026, propostas; nada no jogo),** escolhidos pela frequência e pelo desenho
  genérico inadequado de hoje, duas direções de cada, em `ferramentas/prototipos/hud/criaturas/quatro_pares/`: o
  sapo-touro gigante e a sanguessuga gigante (o pântano, hoje o `fera`); o cultista e a bruxa do pântano (os
  conjuradores, hoje o `humano`); o carniçal e o espectro (os mortos-vivos, hoje a `caveira` e o `etereo`); o javali
  selvagem e o rato gigante (as feras comuns, hoje o `fera`). As folhas `par1.png` a `par4.png` e a prancha `geral.png`;
  o alcance (pela família; os chefes, o antagonista e os aliados fora) no `LEIA-ME.md` da pasta. **A situação em
  22/10/2026:** integrado, o lobo na fogueira (1.170.0); em avaliação, o Esqueleto E1r, o urso r4, o falcão, o cajado do
  Mago e os 16 candidatos (`criaturas/pendencias/pendencias.png`); conceitos reservados, o Esqueleto E2 e o Bandido do
  chapéu.
- **No jogo desde a 1.171.0:** o Sapo-touro gigante A e a Sanguessuga gigante A, pela família (`RETRATO_FAMILIA`), na
  carta, no Bestiário, no mural e no rastro; a Hidra do Brejo (guardiã) e as outras feras continuam pelos traços.
- **A segunda rodada (22/10/2026, propostas; nada no jogo),** em `ferramentas/prototipos/hud/criaturas/segunda_rodada/`:
  três capuzes do cultista, três rostos da bruxa, o carniçal com a boca refeita, o espectro de olho único, o javali de
  presas grandes e três reconstruções do rato; as folhas por criatura e as minhas preferências (o cultista c1, a bruxa
  b1, o rato r1) no `LEIA-ME.md` da pasta. Em avaliação, com o Esqueleto E1r, o urso, o falcão e o cajado.
- **No jogo desde a 1.172.0:** o Cultista A (o original; os capuzes c1 a c3 ficam como alternativas não escolhidas),
  a Bruxa do pântano B3 (o sorriso banguela) e o Rato gigante r2 (de frente, a cabeça baixa), pela família; o cultista
  também nos fiéis do Profeta e nos dois de capa escura da sacristia. O Profeta, o mercenário e as outras feras
  continuam pelos traços.
- **A terceira rodada (22/10/2026, propostas; nada no jogo),** em `ferramentas/prototipos/hud/criaturas/terceira_rodada/`:
  o carniçal A3 (a bochecha direita recolhida), o javali A3 (as presas em arco) e o espectro M (o retrato pela
  referência do manto inflado, a direção corporal escolhida); as folhas de antes × depois.
- **No jogo desde a 1.173.0:** o Javali selvagem A3 e o Carniçal A3, pela família; o esqueleto, o cavaleiro sombrio, o
  Lich e as outras feras continuam pelos traços. O espectro M não foi escolhido.
- **O espectro AP (22/10/2026, proposta; nada no jogo):** o A original com o pano continuando até a borda de baixo (só
  as linhas 11 a 15); a referência do manto inflado fica como conceito do corpo para a arte de cenário; a comparação
  `terceira_rodada/espectro-ap.png`. O AP2: sem as dobras escuras de baixo e com a cavidade mais larga
  (`espectro-ap2.png`).
- **No jogo desde a 1.174.0:** o Espectro AP (o A com o pano até a borda de baixo, sem retoques), pela família; a cria
  do Vazio e o Lich (na fase 2) continuam no `etereo`. O A, o M e o AP2 ficam como histórico; a referência do manto
  inflado fica registrada para a futura arte de cenário.

**A frente de criaturas em 22/10/2026 (na 1.174.6; conferido em `dados.retrato` com as 27 famílias e os 10 guardiões
do catálogo):**
- **Integrados (25):** pela família, o Afogado, o Lobo, o Bandido, o Troll da montanha, a Aranha gigante, o Sapo-touro,
  a Sanguessuga, o Cultista, a Bruxa do pântano, o Rato, o Javali, o Carniçal, o Espectro, o Esqueleto, o Mercenário e
  o Lobo Gélido, o Caído, o Grifo, a Harpia, o Xamã Caído, a Cria do Vazio e o Cão infernal (22; o Esqueleto E1r na 1.175.0, com os que o Lich invoca; o Mercenário MA e o Lobo Gélido LA
  na 1.179.0, com o Invicto da ponte e o Theodore; o MB e o LB guardados como não escolhidos; o Caído CA na 1.182.0, com
  os que o xamã ergue; o Grifo GA3 na 1.183.0, com o feroz do ninho; o GA e o GA2 como histórico; a Harpia T2 e o Xamã
  Caído X1r2 na 1.184.0, com os afixos e o xamã que escolta o bando de caídos; a Cria do Vazio A2 na 1.185.0, com as
  que o antagonista invoca; o Cão infernal P1 na 1.186.0, com os afixos); pela chave da capela, a Ilse; pelo id do guardião, o Rei Troll e
  a Rainha Aracnídea. Os animais do patrulheiro (o Urso Pardo, o Falcão Peregrino e o Lobo Cinzento) na carta aliada e
  no painel; os três também na fogueira, pelo tipo (o lobo c2 na 1.170.0, o urso r4 e o falcão na 1.176.0). O cajado
  aprovado no Atacar do Mago (1.177.0).
- **Fora das criaturas, na 1.180.0:** o ícone do **Esgotado** do mercado (o caixote, papel próprio `MOTIVO`; o cesto
  guardado como não escolhido; o cadeado continua nos outros motivos e usos).
- **Propostas aguardando o Jean (22/10/2026, na 1.186.0; nenhuma autorizada), a quinta rodada da Cidadela:** a
  **Abominação C3** aceita visualmente pelo Jean (preservada sem retoques; a integração ainda não autorizada) e o
  **Cavaleiro Sombrio P4**, o P3 refinado pela construção da carta do Guerreiro (o elmo maior, a viseira em V, a base
  escura separando do gorjal) (`criaturas/cidadela/`, a folha `cavaleiro-p4.png`). O P3 e o T2 são as direções
  preferidas do Jean, nenhum aprovado. Histórico, não escolhidos: a Abominação A, B, C, C2, D e E e o Cavaleiro A, A2,
  B, T, P1 e P2. Histórico, não escolhidos, em
  `criaturas/fenda/`: o Cão A, B, T, N, N2, RA, RB, RC, RA2, RA3, P2 e P3 (a P1 foi a escolhida), a Cria A e B. A cria que o antagonista
  invoca é da família `cria_vazio` e usará o mesmo retrato. Histórico, não escolhidos: as Harpias HA, HB, H1 a H3 e a
  T, o GB, o GA e o GA2 (`criaturas/harpia_grifo/`, `criaturas/rodada_23_10/`), o CB, o XA e o XB
  (`criaturas/caidos/`), os Xamãs X1, X2, X3 e o X1r. Uso previsto de cada um: pela própria família (a carta, o
  Bestiário, o mural, o rastreador, a faixa do mestre caçador); o Dragão de Gelo continua no `voador`.
- **Nomenclatura (1.181.0, aprovada pelo Jean):** o **ent jovem** é a **Árvore Desperta** e o **Ent Ancião**, a **Árvore
  Anciã** (árvores vivas: "árvores que acordaram com raiva"; o guardião, "uma árvore milenar"). Os ids `ent_jovem` e
  `ent_anciao`, os números, as habilidades e as regras ficam; os saves antigos passam pela migração v5 → v6.
- **Ainda nos desenhos genéricos dos traços (levantado em `dados.retrato` na 1.184.0):**
  - **4 famílias inimigas:** a Árvore Desperta (`planta`), o golem de pedra (`construto`), o cavaleiro sombrio
    (`caveira`) e a abominação (`corrompido`). A cria do Vazio tem o retrato dela desde a 1.185.0, com as que o
    antagonista invoca; o cão infernal, desde a 1.186.0 (nenhuma família fica mais no `demonio`).
  - **8 guardiões:** a Árvore Anciã, a Hidra do Brejo, a Bruxa Afogada, o Dragão de Gelo, o Senhor da Guerra, o Profeta
    das Cinzas, o Lich Menor (o `etereo` na fase 2) e o Golem Primordial.
  - **O antagonista** (família `antagonista`, só no mundo gerado): sem retrato próprio, no `humano` pelo traço
    `conjurador`.
  - **À parte, do lado do herói:** o servo do Necromante (o "Esqueleto (Invocado)" do Erguer Servo e o inimigo erguido
    pelo Rei dos Mortos) é um aliado de `tipo` servo, sem família, desenhado na `caveira` pela tela; a família
    `esqueleto_servo` do catálogo não é criada por nenhum código.
- **Compartilhamentos deliberados:** o Lobo Cinzento aliado com o retrato do Lobo (1.165.0; o lado, o nome e a borda
  separam os papéis); os invocados com o retrato da família que os invoca ou a que pertencem (os afogados da Ilse, as
  aranhas da Rainha, os lobos e bandidos líderes e invocados); os fiéis do Profeta e os dois de capa escura da sacristia
  com o Cultista.
- **Conceitos reservados (fora do jogo, sem espécie, regra nem mapeamento):** o Esqueleto E2 (um possível mago
  esqueleto) e o Bandido do chapéu (um possível chefe).
- **Próximos pares recomendados (a escolha é do Jean):** os três primeiros estão no jogo (o mercenário e o lobo
  gélido, 1.179.0; o caído e o xamã caído, 1.182.0 e 1.184.0; o grifo e a harpia, 1.183.0 e 1.184.0). O quarto, a cria do
  Vazio e o cão infernal, também (1.185.0 e 1.186.0). **O próximo: a abominação** (a última criatura da Fenda sem
  retrato) **com o cavaleiro sombrio** (os dois da Cidadela); depois, a Árvore Desperta com o golem de pedra. Os guardiões genéricos ficam para pares próprios, um chefe por vez, depois dos comuns.

O atalho **Mapa** da doca já foi concluído; esta frente trata dos símbolos internos de caminhos e mapas.
Não afirmar que só restam talentos e habilidades após este bloco sem conferir os consumíveis, variantes e
compartilhamentos provisórios ainda registrados. A Capa de Patrulha, o Chapéu de Couro e a Coroa dos Afogados continuam
com a pendência de arte própria; Sandália e Diadema, com a de nomenclatura. Esses registros não autorizam variantes
ou mudanças de dados por iniciativa do agente.

**Fluxo:** levantamento dos usos reais → proposta em pequenos lotes → avaliação de Jean → tamanhos e integração.
Usar os tamanhos de cada contexto, sem aplicar automaticamente a grade de equipamento a rostos, estados ou minimapa.
Reaproveitar bancadas e capturas; a janela principal é 1920×945. Não reabrir a matriz de resoluções em cada desenho.
Habilidades e talentos ficam na etapa 8, junto dos respectivos sistemas e telas.

## 2. Telas de leitura, criação, carregamento e celebrações

**Lembrete para o futuro estudo da HUD — pen.dev (experimento `9769305`):** antes de escolher ferramentas para
uma composição nova, consultar [o relatório e a bancada](../ferramentas/prototipos/hud/pen-composicao/LEIA-ME.md).
O teste comparou reprodução e ajuste de um seletor existente; o CSS direto foi mais rápido, e o pen.dev não entra
como etapa obrigatória do fluxo. A criação de uma composição inédita no canvas ainda não foi avaliada e pode ser
retomada como experimento opcional, inclusive pelo agente; não depende de Jean querer editar manualmente.
O arquivo `seletor.pen`, os assets e as comparações estão preservados na mesma pasta. Este lembrete não autoriza
redesenho global nem integração de uma nova HUD.

- **Subida de nível:** preservar a boa organização das informações, redesenhando o acabamento para a linguagem atual.
  Manter a sensação de conquista com som, luz e movimento, sem depender do feixe suave com aparência renderizada.
  Testar feixes e partículas em pixel art e tags/faixas para os ganhos; posição e formato ainda são propostas.
- **Celebrações e raridade:** harmonizar o tratamento dos efeitos, com intensidade proporcional ao acontecimento.
  Respeitar movimento reduzido sem fazer o aviso desaparecer antes de poder ser percebido.
- **O dado dos testes:** o redesenho artístico do d20 (hoje o SVG de sempre, 2× no centro desde a 1.117.0, item 1.4)
  entra neste acabamento visual da HUD, junto dos efeitos de raridade e da subida de nível. A apresentação central, o
  ritmo e as faixas de sucesso e falha já aprovados ficam.
- **Grimório da interface:** aparência do livro aberto, páginas, leitura e navegação serão revistas **com o sistema
  de habilidades na etapa 8**, para evitar uma rodada só de acabamento antes de redefinir o conteúdo da tela.
- **Carregar jogo e fichas dos saves:** revisar o visual antigo da lista e das fichas, com identificação clara da
  partida e ações legíveis. Preservar os dados, a compatibilidade dos saves e a semântica de carregar/excluir;
  não confundir o menu com o atalho Salvar da doca, já concluído.
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

## 8. Habilidades, Grimório, árvore de talentos, animações e liberdade de build

**Decisão de Jean (19/10/2026):** produzir os ícones de habilidades e talentos junto da revisão dos respectivos
sistemas e telas, evitando arte para conceitos prestes a mudar. O visual antigo do Grimório e da árvore não está
no patamar atual do jogo e precisa de uma revisão própria; isso não aprova uma mudança de regras por si só.

- **Grimório da interface:** revisar o livro aberto, páginas, hierarquia, leitura, seleção e navegação de acordo com
  o sistema validado. É uma tela diferente do item Grimório e do atalho da doca, cujos desenhos estão aprovados.
- **Árvore de talentos:** revisar estrutura visual, conexões, nós e estados (disponível, adquirido e bloqueado),
  explicações e seleção. Preservar o suporte técnico a árvores extensíveis; aparência nova não define tiers,
  quantidade ou efeitos dos talentos.
- **Ícones de habilidades e talentos:** criar em lotes após estabilizar o conceito e a função de cada grupo;
  reconhecer função e identidade em tamanho real. O atalho Talentos da doca já está pronto e não é este escopo.
- Revisar animações de habilidades e efeitos, com leitura das fontes, alvos, custos e consequências. Os símbolos
  dos buffs/estados existentes são prioridade anterior (1E); reaproveitar os aprovados e só reabrir os afetados por
  mudança real de sistema.
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
- Mudança visual: usar a janela principal de Jean (1920×945 na área do jogo) e conferir o componente afetado;
  mouse, teclado e movimento reduzido conforme o contexto. Não abrir uma bateria de resoluções a cada entrega.
  Corrigir impedimentos de uso e registrar adaptações gerais para a consolidação, conforme o CLAUDE.md.
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

## Próxima passagem de trabalho — atualizada em 22/10/2026

1. **Concluídos:** os 31 equipamentos-base (1D); na 1E, o contador de flechas e os 17 estados; 24 criaturas com retrato
   (22 famílias, a Ilse, o Rei Troll e a Rainha Aracnídea); o ícone do Esgotado do mercado e os três animais do patrulheiro (na carta, no painel e na
   fogueira); o cajado no Atacar do Mago. As variantes e os compartilhamentos provisórios ficam abertos, separados.
2. **Agora, 1E.3:** as demais criaturas, os chefes e as invocações, em pares pequenos escolhidos pelo Jean, pelo mesmo
   caminho (o retrato por família, por chave ou pelo tipo, sem trocar o sprite compartilhado). O Mercenário, o Lobo
   Gélido e o Esgotado integrados (1.179.0, 1.180.0); o Caído CA (1.182.0); o Grifo GA3 (1.183.0); a Harpia T2 e o Xamã
   Caído X1r2 (1.184.0); a Cria do Vazio A2 (1.185.0); o Cão infernal P1 (1.186.0). **Aguardando o Jean:** a
   avaliação do Cavaleiro P4 (a Abominação C3 aceita visualmente), a sexta rodada
   (`criaturas/cidadela/`); depois, a Árvore Desperta com o golem de
   pedra e os chefes, sem começar antes do pedido. A relação em "A frente de criaturas em 22/10/2026" (item 1.12). O Esqueleto E2 e o Bandido do
   chapéu estão reservados.
3. **Depois, 1E.4:** os caminhos/destinos e os símbolos internos do mapa e do minimapa.
4. **Retomar a etapa 2** e **seguir 3–7**, como na sequência abaixo; **etapa 8** com habilidades, talentos, Grimório e
   árvore no mesmo ciclo; **etapa 9**, a campanha; **depois do plano**, a avaliação de refatoração.

## Próxima passagem de trabalho — sequência aprovada em 19/10/2026 (histórico)

1. **Espada e maça concluídas na 1.145.0** (`ed967d1`) e a cota na 1.146.0, sem retoques nos aprovados.
2. **Agora, fechar o equipamento básico restante:** a manopla integrada na 1.147.0, o elmo e as perneiras na 1.148.0;
   o 40 e o 48 do martelo na 1.149.0; as botas de ferro na 1.150.0: **os 31 equipamentos-base concluídos**. Conferir objetos da bolsa e
   usos residuais para saber o que de fato falta, preservando compartilhamentos aceitos.
3. **Abrir a etapa 1E:** contagem de flechas do Arqueiro primeiro; buffs/estados com Firme; depois inimigos e pets;
   caminhos e símbolos internos do minimapa/mapa. Não interromper o par em andamento nem redesenhar peças já aprovadas
   por extensão.
4. **Retomar a etapa 2:** telas antigas e acabamento — menu de carregar/fichas dos saves, criação de personagem,
   livro narrativo da capela, dado, subida de nível, celebrações e raridade. Grimório e árvore de talentos ficam
   consolidados com a etapa 8.
5. **Seguir 3–7:** interior da forja; protótipo de reforço/encantamento; serviços da vila; cenários e acampamentos;
   eventos recorrentes.
6. **Etapa 8:** sistemas de habilidades e talentos, Grimório e árvore, ícones e animações no mesmo ciclo, com
   protótipos e decisões de regras ainda necessários.
7. **Etapa 9:** expansão/revisão da campanha. A etapa técnica I entra quando o trabalho de narrativa a exigir.
8. **Depois do plano:** retomar a avaliação de refatoração/manutenção acordada na conversa, guiada por um diagnóstico
   do código então existente; sem antecipar uma limpeza geral durante os lotes de arte.

**Pendências independentes, sem ampliar a próxima entrega:** refinamento de cores da dica "Testes do d20" (1.11,
só no protótipo); redação do aviso da escuridão antes de agir (1.6); artes próprias dos compartilhamentos provisórios
e nomenclatura da Sandália/Diadema. A E9, testes com jogadores e impedimentos de compreensão continuam sendo
tratados ao longo do projeto, sem esperar a última etapa.

Esta ordem atualiza a sequência anterior. Não autoriza executar todo o plano numa tarefa nem aprova automaticamente
protótipos, desenhos ou regras. O plano não altera o jogo por si só.
