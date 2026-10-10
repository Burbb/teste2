# 00 — Comece aqui: continuidade do projeto

Registro de passagem de contexto — 09/10/2026 (horário de Brasília).

Este arquivo permite continuar o projeto em uma nova conta ou sessão sem depender das conversas anteriores. É um ponto de entrada; os documentos temáticos detalham o plano. Atualize o estado ao concluir entregas relevantes, sem marcar proposta como decisão ou leitura como teste executado.

## 1. Repositório e referência

| Campo | Referência desta passagem |
|---|---|
| Jogo | Crônicas da Fenda |
| Repositório | Burbb/teste2 |
| Branch de trabalho | `claude/tender-einstein-tx3tjl` |
| Versão do jogo consultada | 1.47.1, em `rpg/__init__.py` |
| Commit do jogo consultado | `602d3aa1e5e1c954d12393d421cca99af06e47b4` |
| Revisão estrutural do roadmap | Leitura estática da 1.46.0, registrada em 09-BASE-EXISTENTE |
| Próximo passo recomendado | E1: especificar primeira região e arco da campanha |

O commit acima é a referência anterior à inclusão deste documento, não uma promessa de que será sempre o HEAD. Confira branch, versão e commits posteriores antes de trabalhar. Preserve alterações existentes no ambiente; não descarte trabalho para alinhar a cópia.

A nova conta recebe o que estiver no GitHub. Conversas antigas, arquivos não enviados, saves locais e registros de partidas não são transferidos automaticamente. Não presumir acesso a eles nem inventar o conteúdo ausente.

## 2. Quem faz o quê e qual jogo queremos

Jean é o criador, designer e jogador que avalia a experiência. Claude ajuda a implementar as entregas solicitadas; ChatGPT ajuda a refinar design e revisar o projeto. Converse em português, diretamente, e explique o comportamento que muda e como Jean pode experimentar.

O projeto começou como RPG de texto procedural e cresceu com cenários minimalistas, combate representado por cards, talentos, contratos, mercado, acampamento e companheiros. A intenção agora é construir uma campanha escrita com início, desenvolvimento e fim, escolhas reconhecidas pelo mundo e liberdade de build.

Baldur's Gate 3 é uma referência de liberdade e consequências; Diablo/PoE, de builds e equipamento; Lineage 2, de identidade e evolução de classe. São referências de experiência, não metas de quantidade ou escala de produção. O trabalho é de Jean com assistência de IA, por entregas pequenas.

### Decisões consolidadas

- Manter Guerreiro, Arqueiro e Mago como as três classes iniciais deste ciclo.
- Preservar os seis caminhos existentes: Guerreiro → Paladino/Berserker; Arqueiro → Patrulheiro/Sombra; Mago → Piromante/Necromante.
- Preservar a identidade visual dos cenários, cards e telas interativas; usar as capturas do README principal como referência do que existe.
- Reaproveitar a comitiva existente: Odette, Morel e Yara.
- Continuar com o motor Python e a interface local HTML/CSS/JavaScript. Não há necessidade demonstrada de migração.
- Validar uma primeira região pequena antes de expandir a campanha por trechos.
- Não exigir centenas de habilidades, novas classes ou múltiplas gerações de especialização neste ciclo.

Raças/origens, tamanho da campanha, modelo de derrota, preparação de habilidades e evoluções adicionais têm decisões pendentes. Consulte [10-DECISOES.md](10-DECISOES.md) quando a entrega depender delas. Exemplos e limites propostos não são aprovações de Jean.

## 3. Ordem de leitura e fontes

1. [CLAUDE.md](../CLAUDE.md): convenções, responsabilidades do motor/interface e verificações do projeto.
2. [README principal](../README.md): como iniciar o jogo, experiência atual e capturas da interface.
3. [README do roadmap](README.md) e [01-VISAO.md](01-VISAO.md): direção e escopo.
4. [09-BASE-EXISTENTE.md](09-BASE-EXISTENTE.md): reuso e limites identificados, considerando a data da revisão.
5. [07-ETAPAS.md](07-ETAPAS.md), [10-DECISOES.md](10-DECISOES.md) e [08-TRABALHO-COM-CLAUDE.md](08-TRABALHO-COM-CLAUDE.md): entrega atual, decisões e forma de trabalhar.
6. [docs/ARQUITETURA.md](../docs/ARQUITETURA.md), [docs/COMO_CRIAR.md](../docs/COMO_CRIAR.md) e documentos temáticos pertinentes à tarefa.

O README principal descreve o jogo disponível, inclusive o mundo procedural e o hardcore. O roadmap descreve a direção futura; não interpretar essa diferença como autorização para trocar imediatamente o comportamento.

[docs/ROADMAP.md](../docs/ROADMAP.md) trata da evolução técnica; `roadmapIDEIAS` trata da campanha e do design. Há notas técnicas antigas já identificadas em 09-BASE-EXISTENTE. Confira a implementação antes de reconstruir algo listado como pendente.

A revisão de 09-BASE-EXISTENTE foi estática e anterior às correções abaixo. Serve de mapa de investigação, não de certificação do estado atual.

## 4. O que mudou depois da revisão estrutural

Três commits posteriores à atualização do roadmap foram consultados. Os comportamentos abaixo são referências para evitar regressões, especialmente ao integrar narrativa, navegação e recompensas.

| Commit / versão | Correções e comportamento a preservar |
|---|---|
| [81bf2f2 — 1.46.1](https://github.com/Burbb/teste2/commit/81bf2f2aca34156a6fe878683d8aeb2990ab599a) | Página do lugar volta após eventos sem escolha; elementos da vila fecham ao sair da cena; balão do prédio aceita clique; pular golpe final libera câmera lenta. |
| [da57773 — 1.47.0](https://github.com/Burbb/teste2/commit/da577734d664e2129cdf214c574e5582d7baadfd) | Evento de viagem ocorre na estrada e chegada respeita leitura/transição; espólio espera Continuar; passiva de especialização aparece no Grimório; Esqueleto invocado entra antes do lance seguinte. Também há ajustes na fogueira, legibilidade e eventos da comitiva. |
| [602d3aa — 1.47.1](https://github.com/Burbb/teste2/commit/602d3aa1e5e1c954d12393d421cca99af06e47b4) | Item encontrado surge no centro e depois abre comparação com o equipado; espaço final reservado evita pulos; apresentação respeita a velocidade escolhida e o modo sem cerimônia. |

**Evidência disponível:** as mensagens desses commits descrevem testes e conferências. O último relata passagem de fumaça, testes e gabarito; o commit 1.47.0 explica atualização intencional do gabarito e replay idêntico.

**Limite desta passagem:** ChatGPT leu os documentos, metadados e mensagens dos commits; não executou o jogo, a suíte ou o navegador. Resultados históricos relatados não comprovam o estado de outra cópia nem de mudanças futuras. Seguir os checks atuais de CLAUDE.md nas implementações e registrar o resultado efetivamente observado.

## 5. Estado e primeira entrega

| Frente | Estado registrado |
|---|---|
| Refatoração estrutural | Entregue segundo os guias e a leitura registrada; não reabrir uma refatoração geral sem problema concreto. |
| Correções recentes | Implementadas nos três commits acima, com validação relatada nas mensagens. |
| E1 — região e arco | Proposta em [11](11-E1-REGIAO-INICIAL.md) e [12](12-E1-CAMPANHA.md). Aprovados por Jean para o protótipo: os quatro lugares e as ligações (Morro da Forca adiado), campanha como novo início, resgate como padrão e hardcore opcional. O resto aguarda aprovação. |
| E2 — região fixa | **Protótipo entregue na 1.48.0** (commit `2661b59`): início da campanha, mapa fixo, viagem, descoberta e save. Validado tecnicamente; falta Jean jogar. |
| E3 — missão mínima | Entregas na 1.50.0 a 1.54.0 (registros abaixo): da Fonte Nova ao canal, à capela, ao interior, a Vó Berta, à guardiã (Destruir ou Dar descanso) e à volta ao Vau, que conclui a missão. A bênção e a comporta não existem. Falta Jean jogar. |
| E4 — consequência local | Na 1.54.0, a Fonte Nova, a frase do Vau, Pita e Marta. Na 1.55.0, Caspar: a acusação, a praça (Apoiar, Denunciar com prova, Calar), a situação da Yara e as reações da comitiva. Na 1.56.0, a consolidação: a Yara barrada fica de fato fora do Vau, o encontro no Charco depois da denúncia, a conversa da Yara sobre a praça e os textos que contradiziam o Vau. **O critério mínimo da E4 (07-ETAPAS) está atendido**; as outras ideias do 11 (bênção, sementes, mercado, taverna, Charco à noite, Odette e Caspar, Anselmo, a cena da vigília) ficam adiadas, não são requisito. Falta Jean jogar. |
| E5 — classes | Diagnóstico (só design) em [14](14-E5-DIAGNOSTICO-CLASSES.md), sobre a 1.56.0. **P1 implementada na 1.57.0:** o golpe preparado em duas lutas fixas da capela (seção 10 do 14). **P3 implementada na 1.58.0:** a encruzilhada compara os dois caminhos e o Grimório explica (seção 11 do 14). A P2 não começou (não está autorizada). A E5 **não** está concluída. A validação da E4 jogando, por Jean, fica registrada à parte. |
| E6–E11 | Plano de trabalho futuro; infraestrutura existente não equivale a etapas concluídas. Notas aprovadas para a E3 na seção 19 do [11](11-E1-REGIAO-INICIAL.md). |
| Bugs ainda abertos | Nenhum bug aberto específico foi informado para registro nesta passagem. Isso não comprova ausência de bugs. |
| Polimento antes da E3 | Entregue na 1.48.1 (registro abaixo): leitura, item achado, balcão do templo, palco da luta. Falta Jean conferir jogando. |
| Baús abertos juntos | Entregue na 1.49.0 (registro abaixo), separado da E3. Falta Jean conferir jogando. |
| Feedback pendente | Jean conferir o polimento da 1.48.1 jogando. |

### Primeiro trabalho recomendado: E1

Comece resumindo o que entendeu, o que já existe e o que precisa ser decidido. Proponha uma região com uma vila, poucas áreas externas, uma masmorra, conflito local, duas soluções e uma consequência visível ao retornar. Inclua oportunidades das três classes, integração da comitiva e um esboço do início, meio e fim da campanha.

A primeira entrega é de design. Não implementar código, mudar comportamento, criar todas as raças ou escrever todos os capítulos nessa tarefa. Use o pedido de E1 em [08-TRABALHO-COM-CLAUDE.md](08-TRABALHO-COM-CLAUDE.md). Se Jean pedir outra entrega explicitamente, registre a mudança de prioridade.

Resolver decisões quando forem necessárias. Escolhas técnicas rotineiras seguem os padrões existentes; escolhas que mudam a experiência precisam ser apresentadas a Jean. Não interromper o planejamento com todas as perguntas futuras de uma vez.

## 6. Escopo de cada sessão

A autorização desta passagem foi criar documentação de continuidade em `roadmapIDEIAS`; ela não autoriza modificar arquivos do jogo.

Para o Claude que continuará: o pedido atual de Jean define a entrega autorizada. Quando ele solicitar implementação, trabalhe apenas nessa tarefa e siga os guias técnicos. Não interpretar a restrição desta edição documental como proibição permanente contra implementações futuras solicitadas, nem interpretar o roadmap como autorização para executar todas as etapas.

Uma tarefa por vez. Reaproveite o que existe, preserve persistência e apresentação quando aplicável, e identifique mudanças intencionais de regra. Não atualizar gabarito para ocultar regressão nem adicionar abstração sem caso concreto.

Para iniciar o jogo, siga o README principal: `python jogar.py`. Para validação, siga os comandos e condições atuais de CLAUDE.md; se algum check não puder ser executado, informe a limitação e não declare aprovação.

## 7. Registro de continuidade após cada entrega

Acrescente um registro curto, ou atualize a tabela de estado, com:

- Etapa e subtarefa; o que foi implementado ou apenas planejado.
- Commit/versão e branch.
- Verificações executadas, resultado e limitações.
- Feedback de Jean jogando, separado da validação técnica.
- Decisões aprovadas, propostas ainda abertas e bugs reproduzíveis.
- Próxima entrega concreta e dependências.

Para um bug: versão, classe/spec, cena, passos, esperado, observado e seed/save/captura quando disponíveis. Não exigir todos esses dados para começar a investigar um problema claramente descrito.

Esta passagem registra o ponto de partida. Não marcar a campanha ou uma etapa como pronta apenas porque o sistema de suporte já existe.

## 8. Registros

### 10/10/2026 — Conferência da base (E0) e proposta da E1

- **Branch e versão:** `claude/tender-einstein-tx3tjl`, 1.47.1. Depois de `602d3aa` só entrou `622b1b6`, que acrescenta Markdown em `roadmapIDEIAS`; nenhum código mudou.
- **Validação técnica executada (Claude, nuvem):**
  - `python -m unittest discover -s tests`: 104 testes OK; 1 pulado (`textual` não instalado);
  - `python -m tests.gabarito`: OK;
  - `pyflakes rpg tests`: só o aviso conhecido em `rpg/eventos/__init__.py`;
  - `tests/navegador/fumaca.mjs`: 66 checagens OK, "tudo certo".
- **Não executado:**
  - `tests.equilibrio` e `tests.replay`;
  - jogar e ver telas.

  As correções da 1.46.1–1.47.1 estão cobertas só até onde a fumaça e o gabarito chegam.
- **Planejado (E1, só design):**
  - [11-E1-REGIAO-INICIAL.md](11-E1-REGIAO-INICIAL.md): região;
  - [12-E1-CAMPANHA.md](12-E1-CAMPANHA.md): campanha, cronologia, protagonista, derrota, transição.
- **Registrado à parte:** divergências entre documentação e código e o texto do prólogo em [13-PENDENCIAS-FORA-DA-CAMPANHA.md](13-PENDENCIAS-FORA-DA-CAMPANHA.md). Não fazem parte da campanha.
- **Hipóteses aceitas por Jean (não definitivas):**
  - resgate como derrota na campanha, com hardcore opcional;
  - procedural preservado até a validação, sem obrigação de manter duas experiências completas.
- **Aguardam aprovação de Jean:** a seção 8 de [12-E1-CAMPANHA.md](12-E1-CAMPANHA.md).
- **Feedback jogando:** nenhum nesta entrega.
- **Próxima entrega:** depois da aprovação (ou ajuste) da E1, a E2: carregar o Vale do Turvo como região fixa, preservando viagem e save.

### 10/10/2026 — E1, revisão 2 (só design)

- **Pedido de Jean:**
  - "Dar descanso" com investigação e ações próprias;
  - Destruir defensável;
  - guardiã separada da postura diante de Caspar;
  - causa da febre detalhada;
  - laço com Marta tratado como proposta;
  - lógica dos Sigilos;
  - linha do tempo.
- **Feito:** [11](11-E1-REGIAO-INICIAL.md) e [12](12-E1-CAMPANHA.md) reescritos:
  - dois eixos independentes, com consequências que se somam;
  - Dar descanso em três passos (verdade, soltar o corpo, rito), com falha que vira Destruir;
  - cadeia Sigilo → Ilse → canal → Fonte Nova;
  - informações essenciais só em cenas obrigatórias;
  - Pita atende e resgata enquanto Marta está doente;
  - Sigilos como pregos do selo;
  - linha do tempo com testes de idade.
- **Nada implementado; nenhuma decisão nova aprovada.** O que decidir antes da E2, antes da E3 e antes da região 2 está na seção 8 do [12](12-E1-CAMPANHA.md).

### 10/10/2026 — E2, primeira entrega (protótipo do Vale do Turvo)

- **Etapa:** E2, só o começo da campanha e o mapa fixo, com navegação e persistência. Implementado.
- **Commit e versão:** `2661b59`, 1.48.0, branch `claude/tender-einstein-tx3tjl`.
- **O que entrou:**
  - opção "Campanha" no título;
  - criação com escolha de modo: resgate (padrão) ou hardcore, gravado no save;
  - prólogo provisório;
  - mapa fixo em `rpg/campanha.py`: Vau do Turvo, Charco dos Juncos (Nv.1), Bosque do Moinho (Nv.2) e Capela Afogada (Nv.3), mais a Estrada de Varn como saída fechada;
  - viagem, descoberta (a Capela aparece depois do Bosque), clima, paisagens e mapa reaproveitados;
  - 5 eventos que falam do vilão sorteado ficam fora da campanha; os outros continuam;
  - legado entre partidas e rumor de lore só no mundo gerado;
  - save `turvo_<nome>.json` com `mundo.campanha`.
- **Verificações executadas:**
  - `unittest discover -s tests`: 116 OK, 1 pulado (`textual` ausente);
  - `tests.gabarito`: OK, idêntico, sem atualizar;
  - `pyflakes`: só o aviso conhecido;
  - `fumaca.mjs`: 77 checagens OK, com o cenário novo "campanha";
  - testes novos em `tests/test_campanha.py`;
  - capturas do Playwright conferidas: título, saves, criação, prólogo, vila, viagem, saída fechada, bosque, capela, charco, mapa grande e vila em 1280 px.
- **Não executado:** `tests.equilibrio` e `tests.replay` (nenhum número de balanceamento mudou).
- **Limitações conhecidas:**
  - fome e infecção encerram a partida também no modo resgate ([12](12-E1-CAMPANHA.md), seção 6);
  - quem resgata ainda é um NPC sorteado;
  - na campanha, a tela do mapa ainda se chama "Mapa do reino" e a legenda mostra cidadela e covil;
  - a vila usa os serviços e o mural genéricos (contratos só de caça e alvo, no vale);
  - os encontros da comitiva continuam aleatórios (os fixos são da E4).
- **Fora desta entrega, de propósito:** missão, rito, eixos, Caspar, Marta, encontros fixos da comitiva, finais e Morro da Forca.
- **Feedback de Jean jogando:** pendente.
- **Próxima entrega:** só por pedido de Jean. A candidata natural é a E3 (missão mínima), que depende das decisões "antes da E3" da seção 8 do [12](12-E1-CAMPANHA.md).

### 10/10/2026 — Polimento antes da E3 (1.48.1)

- **Feedback de Jean jogando a 1.48.0:**
  - jogou o protótipo até o dia 14, nível 5 e meio, e enfrentou Theodore;
  - provocou uma derrota em outro save, e o resgate o devolveu à cidade após dois dias;
  - pediu quatro ajustes (abaixo). A abertura conjunta de baús fica para uma entrega separada.
- **Implementado** (só o autorizado):
  1. **Leitura:** a guarda em que um clique não vira a página (`GUARDA_LEITURA`, `pagina.js`) caiu de 700 para 550 ms.
     - Medido no navegador: um clique 450 ms depois do resultado antes era ignorado (a página esperava a leitura toda, 5,7 s) e agora vira na hora.
     - A 300 ms continua ignorado: o clique que termina o texto não vira a página junto.
  2. **Item achado:** o motor manda os rótulos dos botões com o cartão (`acoes` no painel `achado`), e a janela os reserva invisíveis desde o começo.
     - Antes, com o espaço vazio, a moldura ia de 342 para 405 px de largura quando os botões chegavam, e em todos os casos crescia 10 px de altura.
     - Medido quadro a quadro em raro/comum, com e sem equipamento no espaço: agora um tamanho e uma posição só.
  3. **Templo:** depois de cuidar de alguém, o motor mantém o balcão (`balcao_templo`) com o ouro, os preços e só quem ainda precisa. Sem ninguém, o balcão diz "O templo está em silêncio…" e fica o Voltar à vila. A vila reabre o balcão sem afastar a câmera nem repetir o som.
  4. **Palco da luta:** a arena só cresce durante a luta e cresce em ~320 ms; as cartas deslizam até o lugar novo (`acomodar` em `batalha.js`, desvio em `top`/`left`, pixel inteiro).
     - Antes: Erguer Servo fazia a arena saltar 59 px e uma carta 29 px num quadro; Maldição fazia uma carta saltar 48 px.
     - Agora: no máximo 10–11 px de arena e 4–7 px de carta por quadro, inclusive com cinco inimigos (duas colunas).
     - A roda de ações usa o lugar final da carta do herói.
- **Gabarito atualizado de propósito**, com as transcrições conferidas:
  - todas divergem logo depois de uma escolha de templo (a pergunta nova "Mais alguém precisa de cuidados?");
  - antes disso, a única diferença é a chave `acoes` nos painéis de item achado;
  - as 6 sequências de comitiva e 4 partidas ficaram idênticas.
- **Verificações:**
  - `unittest`: 118 OK, 1 pulado (`textual`);
  - `tests.gabarito`: OK;
  - `pyflakes`: só o aviso conhecido;
  - `fumaca.mjs`: 81 checagens OK. Checagens novas: moldura do achado estável, templo no balcão, palco sem pulo na Bola de Fogo. A do palco falha no código antigo (16 px) e passa no novo (2 px);
  - um passo intermitente do cenário da campanha foi reforçado (esperar o título se redesenhar);
  - testes novos em `tests/test_vila.py`.
- **Observação, sem mudança:** um clique dentro da guarda é descartado, e a página espera a leitura inteira até um segundo clique. Se isso ainda pesar, a próxima medida seria guardar esse clique para quando a guarda acabar. Decisão de Jean.
- **Não executado:** `tests.equilibrio` e `tests.replay` (nenhuma regra de combate ou número mudou).

### 10/10/2026 — Baús abertos juntos (1.49.0), entrega separada da E3

- **Pedido de Jean:** com vários baús, um clique na pilha abre todos os que estavam nela, num quadro só ("Baús ×N"), e depois cada equipamento com as decisões de sempre.
- **Implementado:**
  - `usar_consumivel("bau")` tira a pilha inteira da bolsa antes de qualquer sorteio e chama `abrir_baus(n)`;
  - com um baú, é o `abrir_bau` de sempre (mesmo quadro "baú aberto");
  - com vários, cada baú passa por `sortear_bau` (o mesmo sorteio e a mesma ordem de um baú aberto sozinho), dentro de um quadro de espólio só;
  - o quadro manda `baus` e a lista `equipamentos` (nome como na janela do item, raridade, ícone), e a tela mostra "Baús ×N" com o ouro e os suprimentos somados e os equipamentos listados ("a seguir, um por um");
  - depois, cada equipamento abre na janela dele (`oferecer_equip`): comparar, equipar, guardar ou deixar, com a regra de mochila cheia aplicada a cada um na hora;
  - rótulos: "Abrir os N baús trancados" na bolsa; "Baú Trancado (abre os N)" no inventário do modo texto; a dica da bolsa diz "Clique para abrir os N de uma vez".
- **Preservado:**
  - lugar seguro (fora dele não abre nenhum e nada é registrado);
  - sem custo nem passagem de tempo;
  - um evento `bau` por baú e um `consumivel` por baú na telemetria;
  - um segundo clique (ou Enter) logo depois não abre nada de novo;
  - mouse, Enter e botão direito pelo mesmo caminho.
- **Comparação com a abertura um por um** (`tests/test_baus.py`): a partir do mesmo estado e do mesmo sorteio, abrir 4 baús juntos e abrir os 4 um depois do outro deram o mesmo ouro, a mesma bolsa, a mesma mochila, os mesmos registros de cada baú e o mesmo estado final do sorteio. Conferido em 4 sementes, no modo texto e no gráfico.
- **Conferido no navegador** (capturas):
  - 1 baú: "baú aberto", como antes;
  - 4 baús: um quadro, +113 de ouro somado, 4 suprimentos, 2 equipamentos listados, depois 2 janelas;
  - 5 baús com a mochila com uma vaga: a 1ª janela guarda e a 2ª oferece "Deixar para trás (mochila cheia)";
  - 3 baús pelo teclado (Enter duas vezes): um quadro só e a pilha vazia;
  - em todos, a moldura de cada janela de item ficou estável.
- **Verificações:**
  - `unittest`: 124 OK, 1 pulado (`textual`);
  - `tests.gabarito`: OK, sem atualizar (o caminho de um baú ficou idêntico; nenhuma partida dos robôs abria mais de um);
  - `pyflakes`: só o aviso conhecido;
  - `fumaca.mjs`: 87 checagens OK em 3 rodadas seguidas, com o cenário novo "baus".
- **Correção de teste:** a falha intermitente do cenário da campanha era do próprio teste. O ajudante `esperar` clica em qualquer `.continuar`, e o "Confirmar" do nome também é um. O reforço da entrega anterior não tratava isso; agora o campo do nome é esperado sem cliques.
- **Observação, sem mudança:** a janela do item mostra "Mochila cheia: equipar deixa o item antigo para trás" mesmo quando o espaço do corpo está vazio (texto que já existia; equipar ali não deixa nada para trás).
- **Não executado:** `tests.equilibrio` e `tests.replay` (nenhum número mudou).

### 10/10/2026 — E3, primeira entrega (1.50.0)

- **Pedido de Jean:**
  - registrar a missão "A Febre do Turvo";
  - cena curta de abertura sobre a febre e a água;
  - objetivo no Diário e no rastreador;
  - primeiro passo real da investigação (examinar a Fonte Nova, com a pista do canal).

  Sem parentesco com Marta, passado do herói nem cronologia: continuam pendentes.
- **Implementado:**
  - `rpg/missoes.py`: a missão como dados, com id `febre_do_turvo`, etapas explícitas (`fonte` → `canal`), objetivo e lugar de cada etapa e uma pista (`agua_do_leste`).
    - O estado vai em `mundo.missoes` (`etapa`, `cenas`, `pistas`).
    - `avancar` só anda a partir da etapa certa e registra `missao` na telemetria.
  - Cena de abertura (sem Marta): toca uma vez, no menu do Vau do Turvo, na etapa `fonte`. Nunca toca em luta, viagem ou evento, nem em outro lugar.
  - "Examinar a Fonte Nova": opção do menu da vila na etapa `fonte`, com o ícone e o losango das opções de contrato.
    - Texto geral mais uma linha por classe; a mesma pista para as três.
    - Passa a etapa a `canal` e guarda a pista.
    - Sem recompensa e sem passagem de tempo.
  - Diário: um quadro "Missão" acima dos contratos, com o objetivo, o lugar e as pistas. No texto, as mesmas linhas.
  - Rastreador: uma seção "Missão" acima de "Contratos", no mesmo molde.
    - Quando o passo está disponível ali, o cartão chama ("Examinar a Fonte Nova ▸") e o clique o faz.
    - O lugar do objetivo ganha o "!" no mapa e a linha na dica do lugar.
  - O prólogo do protótipo diz que a missão começou.
- **Saves da campanha de antes (1.48–1.49):** ao carregar, a missão entra na etapa `fonte`, sem cenas vistas (`campanha.ajustar_save`). Personagem, bolsa, mapa descoberto, lugar e dia não mudam. A abertura toca na próxima vez em que a pessoa estiver no Vau, e o objetivo já aparece no Diário. Sem nova versão do save: o mundo gerado não muda.
- **Procedural:** sem missões, sem a chave no estado da tela e sem quadro no Diário. Gabarito idêntico.
- **Verificações:**
  - `unittest`: 131 OK, 1 pulado (`textual`). Novos em `tests/test_missoes.py`: as três classes iniciam e avançam; repetir não anda nem duplica; Diário, estado da tela e lugar concordam; save preserva; save antigo da campanha; cena respeita lugar, luta e estrada; procedural sem missão;
  - `tests.gabarito`: OK, sem atualizar;
  - `pyflakes`: só o aviso conhecido;
  - `fumaca.mjs`: 90 checagens OK em 2 rodadas, com a missão no cenário da campanha;
  - navegador, com capturas em 1500 e 1280 px (guerreiro e mago): abertura, vila com a opção e o rastreador, Diário antes e depois, exame, "!" do Vau para o Bosque, rastreador no mesmo lugar antes e depois (sem salto) e recarregar a página.
- **Limitações:**
  - na etapa `canal` ainda não há o que fazer no Bosque (próxima entrega);
  - a missão não tem fim nem recompensa ainda;
  - o objetivo não reage à comporta, a Caspar ou à Yara;
  - os encontros da comitiva seguem aleatórios.
- **Não executado:** `tests.equilibrio` e `tests.replay` (nenhum número mudou).

### 10/10/2026 — E3, segunda entrega (1.51.0)

- **Pedido de Jean:** investigar o canal no Bosque do Moinho e chegar ao exterior da Capela Afogada; corrigir o "fim da tarde" fixo no exame da fonte; cenas da missão sem avanço por tempo, com Continuar explícito e sem que o clique que adianta o texto feche a cena; "Pistas" vira "O que você sabe:" no Diário.
- **Implementado:**
  - `rpg/missoes.py`: nova etapa `capela` (objetivo "Investigar a Capela Afogada…", lugar `capela_afogada`) e duas pistas (`represa`, `canal_da_capela`). Cenas e ações viraram dicionários com `missao`, `id`, `lugar`, `etapas`, `fn` e `confirmar`.
  - "Seguir a água e examinar o canal": ação do Bosque na etapa `canal`, no menu do lugar selvagem (o `menu_selvagem` agora recebe as opções de missão). Mostra a represa, o leito velho seco (por isso o poço secou), o canal novo e a comporta como cenário, e a capela no brejo com o canal entrando por um rombo no muro. Uma linha por classe. Não fala de Ilse, do Sigilo nem da causa sobrenatural. Guarda as duas pistas e passa a etapa a `capela`.
  - Exterior da Capela Afogada: cena curta, uma vez, na etapa `capela`, que retoma o canal seguido desde o moinho. Termina com o aviso de protótipo: o interior abre numa próxima parte. A etapa continua `capela`.
  - Visitar antes não adianta nem consome nada: a ação e a cena esperam a etapa delas.
  - Exame da fonte: "fria demais para" segue o período (manhã, tarde, anoitecer, noite).
  - Leitura: cada cena e ação da missão declara `confirmar=True`. O fim delas chama `ui.continuar(confirmar=True)`, e a ponte manda `continuar` com `confirmar: true`. A tela não vira a página por tempo; o botão chega apagado e só aceita depois da guarda de leitura (550 ms); cada toque dentro dela a estende em 350 ms (a mesma regra do quadro do espólio) e a tecla segurada não conta. As outras cenas não mudaram (o `continuar` sem o campo segue igual).
  - Diário: o rótulo "Pistas" virou "O que você sabe:" (tela e modo texto); o campo interno continua `pistas` e o save não muda. Sem nada descoberto, o rótulo não aparece.
- **Saves:** os da 1.50 (etapa `fonte` ou `canal`) seguem de onde pararam, com as pistas. Os da 1.48–1.49 continuam ganhando a missão na primeira etapa.
- **Procedural:** sem missões; gabarito idêntico.
- **Verificações:**
  - `unittest`: 138 OK, 1 pulado (`textual`). Novos: as três classes vão da fonte ao exterior da capela; visitas antecipadas; toda cena e ação pede confirmação; a fonte respeita a hora; save da etapa `canal` continua e guarda a cena da capela; "O que você sabe:" no Diário; na ponte, o `continuar` marcado só nas cenas que pedem e a volta ao lugar sem virar por tempo;
  - `tests.gabarito`: OK, sem atualizar;
  - `pyflakes`: só o aviso conhecido;
  - `fumaca.mjs`: 99 checagens OK em 3 rodadas. Novo cenário `missao` (mago no Bosque, etapa `canal`): clique e Enter em rajada com o texto correndo não fecham a cena; deixada aberta 6,5 s, não fecha; depois do Continuar, objetivo e "!" vão para a capela; Diário com as três descobertas. No cenário da campanha: a abertura fica aberta esperando o Continuar; no instantâneo, o Enter martelado não fecha o exame da fonte;
  - navegador, com capturas em 1500 e 1280 px: canal, Diário, viagem ao exterior da capela (com um evento no caminho) e a cena da capela aberta por 7 s.
- **Limitações:**
  - na capela ainda não há o que fazer: as salas, a comporta acionável, Ilse, o rito, Caspar e os encontros fixos da comitiva ficam para depois;
  - a missão não tem fim nem recompensa;
  - cronologia e vínculo com Marta seguem pendentes.
- **Não executado:** `tests.equilibrio` e `tests.replay` (nenhum número mudou).

### 10/10/2026 — Correção: tela incompleta ao carregar (1.51.1)

- **Relato de Jean:** depois dos passos novos da missão, salvou, saiu e carregou de novo. No Bosque do Moinho só apareceu o centro (arte, título, opções); painéis, rastreador e doca voltaram depois de acampar.
- **Causa:** ao voltar para o título, a tela apaga o estado do herói (`estado = null`, classe `sem-heroi`), mas a ponte (`rpg/web/ponte.py`) guardava o último estado enviado e só manda um estado diferente dele. Carregando o mesmo save logo depois de salvar, o estado era idêntico e nunca era reenviado; a primeira ação que mudava algo (acampar) o trazia de volta. Valia para a campanha e para o mundo gerado. Carregar direto do título, sem ter jogado antes na mesma sessão, e recarregar a página não tinham o problema.
- **Correção:** a cena de título faz a ponte esquecer o último estado (`WebUI.cena`, tipo `titulo`). O lugar carregado chega já com o estado, na primeira apresentação. Posição, dia, recursos e progresso não mudam (o save não é tocado).
- **Verificações:**
  - `unittest`: 139 OK, 1 pulado (`textual`). Novo em `test_web`: título entre duas apresentações do mesmo estado manda o estado de novo (falha sem a correção);
  - `tests.gabarito`: OK, sem atualizar;
  - `pyflakes`: só o aviso conhecido;
  - `fumaca.mjs`: 104 checagens OK em 2 rodadas. Novo cenário `recarga` (save da campanha no Bosque, noite de chuva, etapa `capela`, e um do mundo gerado): logo que as opções aparecem, sem clicar em nada, confere painel do herói, doca, mapa, missão e lugar/dia; depois salvar, sair e carregar o mesmo save; recarregar a página; e carregar o save do mundo gerado. Sem a correção, a checagem de salvar-sair-carregar falha.
- **Limitações:** nenhuma conhecida.

### 10/10/2026 — E3, terceira entrega: o interior da Capela Afogada (1.52.0)

- **Pedido de Jean:** nave, sacristia e ossuário como sequência pequena, com os sistemas existentes; soltar o corpo (D2) como preparo, separado de conhecer o nome; sair e voltar; salas, descobertas e preparos no save; derrota, fuga ou abandono não contam; nada duplicado; termina antes de Ilse. Junto, registrar as decisões de narrativa (cronologia 60/3, Marta, Ilse, a Fenda e o título, a direção temática do selo).
- **Implementado (`rpg/missoes.py`):**
  - novas etapas `sacristia`, `ossuario` e `fundo`, cada uma com objetivo no Diário e no rastreador; o lugar de todas é a capela;
  - cada sala é uma ação do menu da capela (sem mapa interno): **nave** (1 afogado e 2 sanguessugas; a água entra pelo rombo, atravessa a nave, desce pela fenda e sai rumo à vila: é a água da Fonte Nova), **sacristia** (2 cultistas com uma marca queimada no pulso, sem dizer quem os mandou; o livro da capela com o nome de Ilse, a acusação, a inocência dela segundo o padre e o Sigilo do Turvo que foi para a água com ela; uma linha por classe; um baú trancado) e **ossuário** (2 esqueletos; o sarilho, as correntes e as mós). As lutas usam `grupo` no nível do lugar, como as outras; a capela é ruína, então cada sala acende uma tocha;
  - só a vitória avança a etapa e dá o que a sala tem. Fuga: "a sala continua por vencer". Derrota: o resgate de sempre, com a missão intacta. O baú vem junto com o avanço, então não se repete;
  - **soltar as correntes** (D2), na etapa `fundo`: o caminho geral serve a qualquer classe (demora um período, faz barulho e chama 2 afogados; só com a vitória as correntes descem); o atalho da classe é um teste (Força, Arcano, Destreza com 1 flecha; CD 13 mais a escala de nível) que poupa a luta quando passa e cai no caminho geral quando falha;
  - novo campo `preparos` na missão (`corpo_solto`), separado das `pistas`. Saber o nome de Ilse é pista; o rito não fica preparado (D1 ainda pede Vó Berta, e o D3 é a próxima entrega);
  - Diário: "O que você já fez:" abaixo de "O que você sabe:" (tela e texto);
  - saves da 1.50–1.51 ganham `preparos` vazio ao carregar (`missoes.completar`, chamado por `campanha.ajustar_save`).
- **Dificuldade:** sem mudança de números. Evidência (robô da arena, 6 heróis por especialização e nível, capela no nível 3, de dia, com comitiva), vitórias por luta isolada:

  | Herói | Comum das ruínas | Nave | Sacristia | Ossuário | Onda (correntes) |
  |---|---|---|---|---|---|
  | Nv 2 | 72% | 56% | 50% | 67% | 67% |
  | Nv 3 | 69% | 86% | 75% | 72% | 75% |
  | Nv 4 | 97% | 97% | 94% | 100% | 100% |
  | Nv 5 | 94% | 100% | 100% | 100% | 100% |

  No nível 3–4, as salas ficam na faixa das lutas comuns do lugar. Emendar as quatro sem descanso só é viável do nível 4 em diante (cai em 39% no 4, 17% no 5); como dá para sair, acampar e voltar, não ajustei. No nível 2, a sacristia (dois cultistas) pesa mais; a capela já aparece como "Nível 3" no mapa.
- **Verificações:**
  - `unittest`: 147 OK, 1 pulado (`textual`). Novos em `test_missoes`: as três classes atravessam a capela; fuga e derrota não vencem a sala (e o resgate preserva a missão); fuga na sacristia não dá o baú; atalho da classe passando e falhando; correntes sem vitória ficam presas; arqueiro sem flechas só tem o caminho geral; save no interior e save sem `preparos`; Diário com "O que você já fez";
  - `tests.gabarito`: OK, sem atualizar;
  - `pyflakes`: só o aviso conhecido;
  - `fumaca.mjs`: 110 checagens OK em 2 rodadas. Novo cenário `capela` (guerreiro nível 5, nave já vencida): a sacristia pela tela, com luta, livro e Continuar; objetivo do ossuário; baú na bolsa; salvar, sair e carregar lá dentro (sala vencida continua vencida, baú não se repete, tela inteira); Diário com Ilse e o Sigilo e sem preparo;
  - navegador, com capturas em 1500 e 1280 px: guerreiro e arqueiro atravessaram nave, sacristia, ossuário e correntes (à mão), acampando quando feridos; o mago caiu na onda das correntes, foi resgatado no Vau e a missão ficou como estava (correntes ainda presas); os três atalhos (Força, Arcano, Destreza) passaram pela tela.
- **Limitações:**
  - o fundo (Ilse), o rito durante a luta, a bênção de Caspar, o julgamento na praça, a cura da febre e a Estrada de Varn não existem; o objetivo para em "Descer ao fundo alagado";
  - D1 (Vó Berta e a fita) não existe: o nome vem só da sacristia;
  - atalho do arqueiro de pular a nave (doc 11, seção 10) e o descanso curto do ossuário não foram feitos;
  - o texto trata Ilse como guardiã do Sigilo em vida, como no doc 11/12 (e que se tornou a guardiã depois de afogada): confirmar com Jean;
  - os textos antigos com "cem anos" e "se abriu"/"abriu" seguem iguais (tarefa própria).
- **Não executado:** `tests.equilibrio` e `tests.replay` (nenhum número de balanceamento mudou; a medição acima usa a mesma arena).

### 10/10/2026 — E3, quarta entrega: Vó Berta, a fita e a guardiã (1.53.0)

- **Pedido de Jean:** conversa com Vó Berta depois da sacristia; a fita; os requisitos do Dar descanso visíveis; o confronto com a Bruxa Afogada existente, Destruir sem preparo e o rito com preparo completo; uma regra para o limiar que resista a dano alto, vários golpes, efeitos periódicos, comitiva e invocações sem tirar força de quem destrói; desfecho único com o Sigilo e a recompensa; Pele do Penitente ou a herança de Berta; objetivo de voltar ao Vau. Confirmou Ilse: em vida, a custódia do Sigilo; afogada, a Bruxa Afogada; a culpa é da vila. A bênção de Caspar fica para quando ele entrar.
- **Implementado:**
  - **Vó Berta** (`missoes._berta`): cartão "Falar com Vó Berta" no balcão da taverna do Vau, como os serviços, depois de saber de Ilse e enquanto a fita não foi entregue. Ela conta o que viu (a vila inteira; o pai dela segurou a corda), sugere que Ilse descansaria com o nome, a fita e as pedras soltas, e entrega a fita. Conhecimento (`verdade_de_ilse`, `nome_e_fita`) e objeto (`preparos: fita`) ficam separados; a conversa não se repete.
  - **Requisitos do rito** (`REQUISITOS_DESCANSO`): a verdade (sacristia e Berta), a fita e o corpo solto. O Diário mostra "Para dar descanso a Ilse, em vez de destruí-la:" com ✓/○ e onde conseguir o que falta, desde a sacristia até o desfecho. A descida ao fundo diz o que falta e só oferece o rito com tudo pronto; sem isso, as opções são "Lutar para destruí-la" e "Voltar por enquanto".
  - **O confronto** (`missoes._fundo`): Ilse é a guardiã Bruxa Afogada existente (`instanciar_guardiao`, com as fases e as invocações), no nível de guardião do lugar (região 3 + 1). Como todo guardião, não dá para fugir depois de começar. Derrota leva ao resgate, sem desfecho, com salas e preparos intactos; a próxima tentativa cria a guardiã de novo, inteira.
  - **A regra do limiar** (`Inimigo.piso` em `entidades.py`, `Combate.checar_limiares`):
    - só vale quando a pessoa escolhe tentar o rito antes da luta. Quem escolhe destruir luta sem piso nenhum, como qualquer guardião;
    - com o rito escolhido, a vida dela tem um piso no limiar da 1ª fase (metade). Toda atribuição de vida passa por ele: golpe forte, vários golpes, efeito periódico, comitiva, servo invocado, espinhos, execução. O que passaria do piso fica `retido`;
    - o momento do rito vem uma vez, no primeiro ponto seguro (fim da sua vez, fim da vez dos aliados, ou antes de qualquer inimigo agir, ela inclusive);
    - "Dizer o nome dela e devolver a fita": a luta acaba em paz (ela e o que chamou da água afundam) e conta como vitória. "Desistir do rito e seguir lutando": o piso sai, o dano retido cai na hora (pode matá-la) e a luta segue para a 2ª fase. Quem desiste não perde nada do que a build fez;
    - a escolha e o efeito são do motor (`missoes._momento_do_rito`); a tela só mostra as opções.
  - **Desfecho** (`missoes._resolver`): `desfecho` guardado antes de tudo ("destruida" ou "descansada"), uma vez. Nos dois, o Sigilo e a recompensa de progressão de guardião (`Chefes.receber_sigilo`, extraído do covil: Sigilo, reputação +5, ponto de talento, festa) e o espólio normal da luta. Destruir: a Pele do Penitente (`itens.fazer_unico`). Dar descanso: o relato curto de Ilse (o Sigilo é um de três; os três seguram fechada uma porta; há mãos procurando juntá-los; sem nomes) e, de volta à taverna, "Contar a Vó Berta": a herança, um raro da classe (`gerar_equip(..., raridade="raro")`), uma vez.
  - Etapa nova `retorno`: "Voltar ao Vau do Turvo com o Sigilo." Ao chegar, nada mais acontece por ora.
  - "custódia do Sigilo" no texto da sacristia (pista) e no relato; o crime fica com a vila.
  - Saves: `completar` acrescenta `desfecho: None` aos saves da 1.50–1.52; correntes soltas e pistas ficam.
- **Dificuldade:** sem mudança de números. Arena (6 heróis por especialização e nível, com comitiva, de dia), vitórias:

  | Herói | Destruir | Rito (até a metade) | Guardião comum nível 4 |
  |---|---|---|---|
  | Nv 3 | 0% | 25% | 0% |
  | Nv 4 | 56% | 81% | 67% |
  | Nv 5 | 92% | 97% | 92% |
  | Nv 6 | 97% | 100% | 100% |

  Ilse fica na faixa dos outros guardiões do mesmo nível. O rito pede metade da luta: o custo dele é a preparação (Berta, as correntes e a onda de afogados), não a luta.
- **Verificações:**
  - `unittest`: 161 OK, 1 pulado (`textual`). Novo `tests/test_guardia.py` (14), com lutas de verdade pelo robô da arena: Berta só depois da sacristia e uma vez; o Diário com o que falta; o piso contra golpe enorme, vários golpes, efeito periódico, servo, espinhos, comitiva e execução, com o momento uma vez; desistir devolve o retido e o rito encerra a luta; as três classes dão descanso e destroem sem preparo; preparado e mesmo assim destrói; desistir no momento destrói; voltar por enquanto não resolve; derrota não resolve e a guardiã volta inteira; save depois do desfecho não repete Sigilo, descida nem herança; destruir não tem herança; save da 1.52 mantém as correntes;
  - `tests.gabarito`: OK, sem atualizar (os refactors do covil e do único preservam a ordem do sorteio);
  - `pyflakes`: só o aviso conhecido;
  - `fumaca.mjs`: 116 checagens. Novo cenário da guardiã: a descida oferece o rito; o momento chega com ela exatamente na metade (83/166); o relato com "custódia"; desfecho, Sigilo e objetivo; salvar, sair e carregar sem repetir nada. A checagem antiga do templo (cenário da vila, mundo gerado) falhou em 4 de 13 rodadas completas: o estado capturado mostrou a tela ainda no Mercado, porque o Esc da checagem chegava enquanto o mercado se redesenhava depois da recompra (nesse instante, o Esc só adianta o texto). Era uma corrida do teste, não do jogo; a checagem agora espera a tela parar antes do Esc. Depois da correção: 116 checagens OK em 3 rodadas completas seguidas;
  - navegador, com capturas em 1500 px: Berta na taverna, conversa e Diário; descida sem preparo (arqueiro); o rito (guerreiro); desistir no momento (mago); os desfechos e a volta.
- **Limitações:**
  - nada acontece ao chegar ao Vau além da herança de quem deu descanso: o julgamento de Caspar, as consequências na vila (a febre, a Fonte, os afogados do Charco) e Varn ficam para depois;
  - a bênção de Caspar não existe (adiada);
  - os atalhos de D1 (Yara, mago no poço, arqueiro no Morro da Forca) não existem; a verdade vem só da sacristia e de Berta;
  - observado, não mudado: um Esc dado enquanto uma tela de serviço se redesenha só adianta o texto e se perde (a pessoa precisa apertar de novo).

### 10/10/2026 — Fim da E3 e primeira consequência da E4 (1.54.0)

- **Pedido de Jean:** cena de volta ao Vau, uma vez, coerente com o desfecho; concluir "A Febre do Turvo" (fora da lista ativa e do mapa, no Diário com conclusão, desfecho, descobertas e preparos); a herança de Berta valendo antes e depois; a Fonte Nova e uma fala local pelo desfecho e pelos dias; Pita e Marta no atendimento; uma diferença pequena e visível entre os desfechos; o texto natural da interrupção do rito; registrar o Esc perdido como pendência.
- **Implementado:**
  - **Volta ao Vau** (`missoes._retorno`, cena `retorno`, etapa `retorno`): toca uma vez, ao chegar ao Vau. Conta o que se vê agora (a Fonte, Pita ou Marta), pelo desfecho e pelos dias desde ele, e conclui a missão (`concluida` = o dia). Volta cedo ou tarde, o texto acompanha o estado da água. Quem deu descanso e ainda não recebeu a herança vê Vó Berta na janela da taverna.
  - **Conclusão:** a missão concluída sai do rastreador e do "!" do mapa (`missoes.cartoes` devolve só as ativas; `cartoes(g, todas=True)` para o Diário). O Diário mostra "concluída", a conclusão com o desfecho, a linha da Fonte, o que se sabe, o que se fez e, se for o caso, "Vó Berta ainda espera você na taverna." No texto, as mesmas linhas.
  - **Herança:** "Contar a Vó Berta" continua no balcão da taverna depois da conclusão, até ser entregue; uma vez só. Quem a recebeu antes (saves da 1.53) não a vê de novo.
  - **A Fonte Nova** (`rpg/consequencias.py`): o estado sai do desfecho, de `dia_desfecho` (guardado na missão) e de `g.dia`. Dar descanso: "limpando" por 2 dias, sem piora, depois "limpa". Destruir: "escura" no dia do confronto (a noite pior), "limpando" até o 3º dia, depois "limpa". A comporta não existe como ação e não conta como fechada.
  - **Fala local:** no Vau, depois do desfecho, a frase de ambiente da vila passa a falar da Fonte e de quem bebe dela (o sorteio da frase continua, para o mundo gerado não mudar). A diferença entre os desfechos, quando a água limpa: com o descanso, uma fita desbotada amarrada na pedra da fonte, que ninguém tira; com a destruição, a vila que não fala da capela.
  - **Marta e Pita:** a abertura da missão (partidas novas) apresenta Marta, que anos atrás tirou o herói de uma febre de estrada, sem cobrar, e Pita, a aprendiz que atende enquanto ela está de cama. Na curandeira do Vau, quem atende e o que diz vêm do motor (`consequencias.atendente`): Pita enquanto a água não limpa (com a noite pior, se foi destruída), Marta depois. Preço, ferimentos e tratamento são os de sempre; no balcão sem ferimento, a frase é de quem está lá. Fora do Vau da campanha, a curandeira de sempre.
  - **Rito interrompido:** "Sem o rito, os golpes que ela vinha aguentando chegam de uma vez: N de dano." (rótulo do golpe: "O rito se desfaz"). A conta e a devolução do dano não mudaram.
  - **Pendência:** o Esc perdido durante o redesenho de uma tela de serviço ficou registrado em [13](13-PENDENCIAS-FORA-DA-CAMPANHA.md), item 10.
- **Saves:** os da 1.53 já resolvidos (etapa `retorno`, sem `dia_desfecho` nem `concluida`) ganham o dia do desfecho como o dia em que forem carregados, e a volta ao Vau os conclui normalmente. `concluida`, `dia_desfecho` e a herança pendente vão no save.
- **Procedural:** sem consequências (sem campo novo no estado da tela); gabarito idêntico.
- **Verificações:**
  - `unittest`: 176 OK, 1 pulado (`textual`). Novo `tests/test_retorno.py` (15): a volta conclui uma vez nos dois desfechos (rastreador e mapa vazios, Diário completo); volta imediata e tardia; herança depois e antes de concluir; destruir sem herança; a Fonte e quem atende dia a dia nos dois desfechos; a frase da vila difere e só vale no Vau; a frase no menu da vila; antes do desfecho, Pita e a vila de sempre; a curandeira com o preço e o tratamento de sempre (Pita e Marta); mundo gerado sem consequências; saves (conclusão, Fonte, herança pendente; save da 1.53 na etapa `retorno`); o texto novo do rito;
  - `tests.gabarito`: OK, sem atualizar;
  - `pyflakes`: só o aviso conhecido;
  - `fumaca.mjs`: 123 checagens OK em 2 rodadas completas. Novo cenário `retorno` (descanso, mesmo dia): a cena e o Continuar; a missão fora do rastreador e do mapa; a frase da Fonte; Pita na curandeira; o Diário com a conclusão e a herança pendente; a herança uma vez; salvar, sair e carregar sem repetir a cena;
  - navegador, com capturas em 1500 e 1280 px: destruir no mesmo dia (Fonte escura, Pita e a noite pior), descanso no mesmo dia (herança na taverna) e descanso 5 dias depois (Fonte limpa com a fita, Marta atendendo).
- **Limitações:**
  - Caspar, o julgamento na praça, a bênção, a perseguição à Yara, as sementes da região seguinte e novos encontros da comitiva não existem; a Estrada de Varn segue fechada;
  - a consequência é só esta: a Fonte, a frase do Vau e quem atende. Mercado, Charco e afogados não mudam;
  - partidas em andamento (já passadas da abertura) conhecem Marta e Pita pela curandeira e pela volta ao Vau, não pela abertura.

### 10/10/2026 — E4: Caspar e a decisão pública (1.55.0)

- **Pedido de Jean:** corrigir textos que davam por passada uma noite ainda futura; apresentar Caspar e a acusação contra a Yara na investigação, e uma introdução adequada a saves com Ilse resolvida; o segundo eixo (Apoiar, Denunciar com prova, Calar), independente de Ilse; a consequência na praça e nas falas, com Ilse, Caspar e Yara tratados à parte; comitiva sem recrutar, ressuscitar nem duplicar; a febre concluída não reabre; nada repete ao voltar ou carregar.
- **Aprovado × proposta (como foi seguido):**
  - **aprovado por Jean nesta entrega e antes** (10-DECISOES): os dois eixos independentes; Caspar apresentado no Vau antes da resolução; a introdução para saves já resolvidos; as três posturas; a prova com caminho para qualquer classe, que não se perde; a consequência na praça; a bênção adiada; Varn fechada;
  - **da proposta do [11](11-E1-REGIAO-INICIAL.md), seção 7, seguida sem acréscimo de regra:** a prova geral (o frasco do lodo da cripta, coletável no fundo, e o canal) e a forte (a análise do mago, as ervas da Yara); o teste de Carisma com que a praça recebe a denúncia, facilitado pela prova forte; o que cada postura faz (Apoiar: vigília, reputação, a Yara não entra no Vau; Denunciar aceita: Caspar vai embora, a Yara livre, reputação, aprovação da Yara; Denunciar recusada: Caspar fica sem vigília, a vila olha torto, a Yara entra mas vigiada; Calar: tudo como estava); da seção 8, o destino dos ossos de Ilse (queimados se Caspar foi apoiado, sem nome se destruída) e a pedra com o nome (descanso);
  - **calibragem minha, a confirmar:** reputação +3 (apoiar), +3 (denúncia aceita), −2 (recusada), 0 (calar); dificuldade de Carisma 13, ou 10 com a prova forte (mais a escala de nível de todo teste); +5 de aprovação da Yara com a denúncia aceita; etiquetas da comitiva (apoiar: fanatismo e autoridade; denunciar: honestidade e rebeldia; calar: cautela);
  - **não feito, continua proposta:** a cena da vigília barrando a Yara antes da decisão (linha "Vila" da seção 7), Odette reconhecendo Caspar (seção 11), Anselmo e a prova dele (seção 14), as sementes (caçadores de bruxas, pregador do Vazio).
- **Implementado:**
  - **Tempo:** os textos da volta ao Vau, da frase da vila, da curandeira e do Diário dependem de quantas noites passaram desde o confronto (`consequencias.noites`, a partir de `g.dia`). No mesmo dia, nada fala de noite passada ("ninguém piorou desde que a água mudou", "a Marta piorou quando a água escureceu", "vai ser uma noite longa"); a partir do dia seguinte, as falas da noite valem. Prazos da Fonte e de Marta iguais.
  - **Missão "A Vigília de Caspar"** (`rpg/caspar.py`), ao lado da febre: escondida no começo; acusação (objetivo sem marcador); praça (objetivo com o "!" no Vau); concluída com a postura.
  - **A acusação:** na investigação (febre entre `capela` e `fundo`, sem desfecho), ao estar no Vau: Caspar, de luto, acusa a Yara. O texto segue onde ela está: desconhecida ou que recusou, no grupo (Caspar a vê), na reserva, morta na fogueira ("e a febre não passou"). Nada se decide aqui.
  - **A praça:** depois da volta ao Vau (a cena da febre vem antes), uma vez: Caspar reivindica o fim da febre (pela destruição ou pelas velas, conforme o desfecho) e cobra a Yara. Quem não o conheceu na investigação (ou vem de um save resolvido) o conhece aqui. Opções: Apoiar, Denunciar (só com a prova; sem ela, o jogo diz o que falta), Calar e "Ainda não", que deixa a ação "Ir à praça responder a Caspar" até a decisão.
  - **A prova:** "Recolher um frasco do lodo da cripta (prova)" no fundo da capela, desde chegar ao fundo até a decisão, inclusive com Ilse resolvida (saves antigos). O mago o analisa ao recolher (prova forte); a Yara no grupo na hora da decisão também conta como forte. O Diário mostra o que falta, como no rito.
  - **Consequência:** a frase do Vau junta a Fonte e a praça (vigília com velas, praça vazia, Caspar pregando para menos gente, ou como antes) e, com a Yara barrada no grupo, que ela espera do lado de fora, na beira do brejo. O Diário da missão concluída traz três linhas separadas: Ilse, Caspar e Yara.
  - **Yara:** barrada só com Caspar apoiado; continua no grupo ou na reserva, à vista no painel, e o jogo diz onde ela fica. Desconhecida, segue acusada (e procurada, com a vigília) ou deixa de ser procurada (com a denúncia). Morta, a linha diz isso. Nenhum recrutamento novo.
  - **A fogueira do brejo** (`yara_na_fogueira`, existente): no Vale, o pregador tem nome (Irmão Caspar); depois de denunciado (aceito ou não), o evento não acontece mais. Com Apoiar ou Calar ele continua possível, coerente com a perseguição. No mundo gerado, nada muda.
  - **Comitiva:** reage pelo `cm.reagir` existente, só quem anda com você agora; a Yara reage com força a Apoiar (desaprova muito).
  - **Saves:** missões novas da região entram ao carregar (`campanha.ajustar_save`); com a guardiã já resolvida, a missão de Caspar vai direto para a praça (`caspar.sincronizar`). A febre concluída não reabre.
- **Divergências encontradas, não mudadas:**
  - a fogueira da Yara pode acontecer no Bosque (bioma floresta), não só no Charco como diz o 11;
  - a fala da Yara "A febre vem do poço, não dela" (opção de Carisma) segue com "poço"; o 11 sugeria "da água" (opcional);
  - frases sorteadas da vila, do mundo gerado, aparecem no Vau antes da guardiã e não combinam com a campanha (ex.: "O padre foi o primeiro a fugir", sendo que há templo com clérigo e Caspar não é padre da vila);
  - a "Yara não entra no Vau" é mostrada em texto: mecanicamente ela continua no grupo (luta e conversa); a proposta dizia "fica no acampamento".
- **Verificações:**
  - `unittest`: 196 OK, 1 pulado (`textual`). Novo `tests/test_caspar.py` (20): a acusação uma vez, só na investigação e no Vau, conforme a Yara; a praça sem prova (sem denúncia, responder depois); o lodo antes e depois da guardiã, e a análise do mago; a Yara no grupo como prova forte; responder depois pela ação; destruir + denunciar; descanso + apoiar com a Yara no grupo (barrada, continua no grupo); destruir + apoiar (ossos queimados); denúncia recusada; calar com a Yara morta; a prova forte facilita; a comitiva reage só quem anda junto; a decisão não repete; save guarda a decisão; save da 1.54 resolvido; mundo gerado; textos do mesmo dia sem noite passada e do dia seguinte com ela;
  - `tests.gabarito`: OK, sem atualizar;
  - `pyflakes`: só o aviso conhecido;
  - `fumaca.mjs`: 129 checagens OK em 2 rodadas completas (e uma terceira dentro do `unittest`). Novo cenário de Caspar (destruir + denunciar, com prova e a Yara no grupo); o de retorno passa pela praça ("Ainda não") e confere o texto do mesmo dia;
  - navegador, com capturas em 1500 e 1280 px: a acusação na investigação (rastreador sem marcador), a praça, apoiar com a Yara no grupo (reação dela, frase da vila, Diário em três linhas).
- **Limitações:** bênção adiada; Varn fechada; sem sementes nem conteúdo da região 2; taverna, mercado e Charco não mudam com a decisão; Odette e Morel só reagem pelas etiquetas (sem falas próprias de Caspar).

### 10/10/2026 — E4: consolidação antes das classes (1.56.0)

- **Pedido de Jean:** entrega curta, sem região nova e sem mexer na interface além do necessário: (1) não perder a chance de conhecer a Yara quando a denúncia acaba com a fogueira; (2) fazer a "Yara não entra no Vau" valer de fato, sem dispensá-la nem mandá-la à reserva; (3) corrigir textos que brigam com a campanha (a febre "do poço", frases do mundo gerado no Vau), sem revisão literária geral; (4) uma conversa curta da Yara sobre a decisão pública, sem segunda recompensa; manter os números da 1.55.0 e medir as chances da denúncia; parar antes da E5.
- **Aprovado × proposta (como foi seguido):**
  - **pedido por Jean nesta entrega:** o encontro no Charco depois da perseguição, uma vez, sem sorteio, com a apresentação e a `oferecer_vaga` existentes; a Yara barrada continua na comitiva, espera fora do Vau e volta na estrada; o painel explica; luta, reações, conversas e serviços respeitam a ausência; a conversa distingue apoio, denúncia aceita, recusada e silêncio, e o que ela viu ou soube; o texto da febre fala da água e da Fonte Nova; o procedural igual;
  - **calibragem minha, a confirmar:** a aprovação com que a Yara do Charco começa (+5 com a denúncia aceita, +3 com a recusada; na fogueira vai de −2 a +12 conforme o resgate); a conversa não mexe na aprovação (a reação da praça já veio);
  - **leitura minha, sem regra nova:** a ausência vale só para a Yara barrada que anda com você (na reserva ela já está no acampamento); quem a conheceu depois da praça só puxa a conversa num dia seguinte (não junto com a apresentação); as conversas continuam só em lugar seguro (vila ou acampamento), então a Yara barrada fala dela no acampamento.
- **Implementado:**
  - **Ausência** (`comitiva.grupo`): `AUSENCIAS` (regras registradas pela campanha), `fora(g, m)` (o porquê, ou None) e `junto(g)` (quem está de fato do seu lado). `caspar._fora_do_vau`: a Yara barrada que anda com você, no Vau e fora da estrada. Quem está fora não entra na luta (nem no "fica de fora" do duelo), não reage às escolhas (`reagir`), não divide a experiência, não paga o custo do Vazio, não aparece no templo, nem como alvo da bolsa (painel, menu e uso), e não puxa conversa ali (✉, menu da Comitiva, noite). Continua em `g.comitiva`, com vida, aprovação, dias e história; come das provisões como antes.
  - **A praça:** a comitiva reage antes de a decisão ser guardada, então a Yara que estava na praça reage a Apoiar antes de ficar do lado de fora. A missão anota onde ela estava (`yara_na_praca`).
  - **Painel:** o cartão da Yara no painel fica esmaecido (o mesmo visual do ferido) com a explicação na dica; na aba Comitiva, "· espera fora do Vau". A frase da vila já dizia onde ela fica.
  - **O Charco** (`caspar._yara_no_charco`, cena da missão de Caspar): depois da denúncia (aceita ou recusada), com a Yara ainda disponível, a primeira chegada ao Charco toca "A Moça do Brejo": ela livre, separando ervas; sabe da praça; a apresentação e a fala dos sapos da fogueira; `oferecer_vaga` (inclusive com a comitiva cheia). Recusar marca "recusou". A praça avisa que ela vive no Charco, e o Diário também. Não toca com a Yara morta, no grupo, na reserva, que recusou, dispensada ou que foi embora, nem com Apoiar ou Calar (a fogueira continua possível), nem no mundo gerado.
  - **Conversa da praça** (`comitiva.conversas`: conversas avulsas, fora da história pessoal, que não contam etapa e ficam anotadas no membro): uma vez, quando a Yara pode conversar; oito falas (quatro posturas × viu na praça ou soube depois) e duas respostas por postura, sem mudar aprovação.
  - **Textos:** na campanha, a opção de Carisma da fogueira vira "A febre vem da água da Fonte Nova, não dela.", o sucesso fala da Fonte que brotou quando o poço secou, e "deixar" termina com a febre que continua. No Vau, três frases sorteadas do mundo gerado (a peste, o padre que fugiu, o pregador do fim) são trocadas por equivalentes do Vau, sem mudar o sorteio (`consequencias.ambiente`). O procedural fica como estava.
- **Chances da denúncia (números da 1.55.0, sem mudar):** Carisma = d20 + nível/2 + reputação/10 (+2 do paladino); dificuldade 13, ou 10 com a prova forte, mais 1 a cada dois níveis acima do primeiro; 20 natural passa, 1 natural falha. Reputação de 0 a 9 (sem bônus):

  | Nível | Guerreiro, Arqueiro, Mago: geral | forte | Paladino: geral | forte |
  |---|---|---|---|---|
  | 3 | 40% | 55% | — | — |
  | 4 | 45% | 60% | 55% | 70% |
  | 5 | 40% | 55% | 50% | 65% |
  | 6 | 45% | 60% | 55% | 70% |

  Reputação 10 a 19: +5 pontos; de −1 a −10: −5. As três classes têm o mesmo Carisma; a diferença está em quem tem a prova forte: o mago sempre (analisa o lodo), os outros só com a Yara no grupo na hora. Conferido com o próprio `g.teste` (20 mil rolagens no nível 4: 45,2% e 60,3%).
- **Verificações:**
  - `unittest`: 219 OK, 1 pulado (`textual`). Novo `tests/test_yara_vau.py` (23): denunciar antes de conhecê-la e encontrá-la no Charco (aceita e recusada), recusar no Charco, comitiva cheia, nenhum encontro para quem já tem destino (morta, grupo, reserva, recusou, dispensada, partiu), nem com Apoiar/Calar ou antes da praça; save sem repetir o encontro; a Yara barrada fora do Vau (na comitiva, painel, sem conversa; não luta, não opina, sem templo nem bolsa; volta na estrada e fora do Vau; save); as quatro posturas da conversa por viu/soube, uma vez, sem aprovação nem etapa; quem a conheceu no Charco fala noutro dia; save sem repetir a conversa; a fogueira com a Fonte na campanha e o poço no procedural; o ambiente do Vau sem padre nem peste, e o do procedural igual;
  - `tests.gabarito`: OK, sem atualizar;
  - `pyflakes`: só o aviso conhecido;
  - `fumaca.mjs`: 137 checagens OK. Novo cenário da Yara (barrada no Vau e de volta no Charco; livre no Charco, aceitar, salvar, carregar sem repetir). Novo cenário `praca` em `tests/navegador/cenarios.py` (POSTURA, YARA, LUGAR);
  - navegador, com capturas em 1500 px: o Vau com a Yara esmaecida e a dica; a aba Comitiva; a chegada ao Charco com o ✉; a conversa no acampamento; "A Moça do Brejo" e a entrada na comitiva.
- **Critério mínimo da E4 (07-ETAPAS):** a vila muda de estado e isso aparece em diálogo e serviço (a Fonte, a praça, Pita e Marta na curandeira); um companheiro reage e conversa (a Yara na praça e na conversa; Odette e Morel por etiquetas); voltar e recarregar mostram a mesma consequência; a escolha se percebe. **Atendido.**
- **Adiado, não é requisito da E4:** bênção de Caspar; sementes (caçadores de bruxas, pregador do Vazio); a cena da vigília barrando a Yara antes da decisão; Odette reconhecendo Caspar; Anselmo e a prova dele; taverna (canção, história de Berta), mercado e desconto da curandeira; o Charco à noite; a comporta; falas próprias de Odette e Morel sobre Caspar; a fogueira só no Charco (hoje também no Bosque).
- **Limitações:** a Yara barrada come das provisões e entra no ensopado da taverna como antes (ela continua na comitiva); a conversa da praça só existe para a Yara; Varn fechada.
- **Como testar (rota curta):** campanha nova; investigue até a capela sem encontrar a Yara (se a fogueira aparecer, deixe para outra partida); recolha o lodo no fundo; resolva Ilse; no Vau, denuncie Caspar; vá ao Charco: "A Moça do Brejo"; aceite; num dia seguinte, no acampamento, o ✉ da Yara traz a conversa da praça. Noutra partida, com a Yara no grupo, apoie Caspar: no Vau o cartão dela esmaece e explica; viaje ao Charco e ela volta ao seu lado; acampe para a conversa. Salve e carregue no meio: nada repete.

### 10/10/2026 — E5: diagnóstico das classes (só design, sobre a 1.56.0)

- **Pedido de Jean:** começar a E5 pela análise e pelo design, sem alterar código, atributos, habilidades, talentos, itens nem saves; diagnosticar as três classes e as seis especializações separando código conferido, promessa, hipótese e proposta; fichas; liberdade de build; progressão e apresentação; até três prioridades com a primeira recomendada; parar antes de mexer no jogo. A E4 atende ao critério mínimo tecnicamente; a validação de Jean jogando fica registrada à parte.
- **Entregue:** [14-E5-DIAGNOSTICO-CLASSES.md](14-E5-DIAGNOSTICO-CLASSES.md); índice (README) e estado da E5 no 07 atualizados. Nenhum arquivo fora de `roadmapIDEIAS` mudou.
- **Achados principais:**
  - Guerreiro e Arqueiro repetem a mesma ação quase todo turno. As lutas do Vale duram 3 a 5 turnos, e Vigor e Foco quase não apertam. Ações de preparo (Grito, Marcar, Desaparecer) rendem menos que repetir o golpe principal em 3 turnos.
  - O golpe preparado (com aviso, interrompido por atordoar), a decisão defensiva mais clara do motor, não aparece em nenhuma luta do Vale.
  - O Mago é a única classe em que o recurso pesa.
  - Botões dominados na faixa 4–6: Golpe Pesado (Paladino), Tiro Duplo, Drenar Vida, Desaparecer. O laço de acender e detonar do Piromante só se paga a partir do 6 (Ignição) e em lutas de 4+ turnos.
  - O Vale é de mortos-vivos: favorece o Paladino e anula o veneno do Sombra e metade do dano do Necromante.
  - Liberdade de build pequena: 3 talentos por especialização; no 12, pontos para quase toda a árvore. Equipamento só de atributos: nenhum único usa os gatilhos que o sistema aceita.
  - A encruzilhada é irreversível e não mostra habilidades, passiva nem custos.
- **Prioridades propostas (nenhuma aprovada):**
  - **P1, recomendada primeiro:** momentos de decisão no Vale. O golpe preparado existente em duas lutas fixas da capela (ossuário e sarilho), só dados da campanha, sem mexer em números de classe nem no gabarito.
  - **P3:** encruzilhada e Grimório que explicam.
  - **P2:** um papel para cada botão dominado; mexe no equilíbrio e no gabarito.
- **Verificações:** só leitura. Os números saem das próprias funções do jogo: Grimório, uma sequência de ações num alvo de treino com 2000 sorteios e lutas do robô de `tests/arena.py`. Condições e limites do robô estão na seção 9 do 14; taxa de vitória não foi usada como medida de decisão. Os scripts ficaram fora do repositório. Testes, gabarito e fumaça não rodaram de novo: nada no jogo mudou desde `adaa93a`.
- **Limitações:**
  - Fúria Cega e Maldição como ações dominantes no 7–9, o Inferno contra grupos e a Marca com comitiva estão marcados como hipótese a medir.
  - Os seis caminhos não foram jogados em cenários direcionados.
- **Próximo passo:** Jean decide se aprova a P1 (ou outra ordem); só então implementar.

### 10/10/2026 — E5, P1: o golpe preparado na capela (1.57.0)

- **Pedido de Jean:** implementar só a P1 da E5. Criar momentos de decisão nas lutas da capela com o golpe preparado e as respostas que já existem, sem só aumentar a dificuldade.
  - No ossuário, um dos dois esqueletos prepara; no sarilho, um dos dois afogados.
  - Preservar quantidade de inimigos, missão, recompensas e vitória.
  - Não mexer na guardiã, em atributos, regeneração, habilidades, talentos, itens nem imunidades; o procedural fica igual.
  - Aviso legível durante a escolha; ficha fiel à variante.
  - Medir a frequência antes e, se raro, usar a menor regra explícita.
  - Comparar continuar atacando, defender, interromper e eliminar antes.
  - Antes e depois para as três classes nos níveis 3 e 4.
  - Registrar que comparações de dano isoladas não provam inutilidade de defesa, cura ou efeitos sobre aliados.
  - Tirar o aviso antigo do ossuário. Parar antes da P3.
- **Implementado:**
  - **Variantes da campanha** (`missoes.grupo_ossuario`, `grupo_sarilho`, `_que_prepara`): o Esqueleto de Guarda e o Afogado Inchado.
    - É a mesma criatura sorteada antes (nível, vida, afixo e o sorteio seguinte iguais), com a habilidade existente `esmagar`.
    - A ficha tem uma `nota`.
  - **A regra** (`combate/turnos.py`, `agir_inimigo`): quem tem `abre_com` (só as variantes) prepara na primeira ação em que faz sentido, sem sorteio.
    - Com o herói a um golpe da morte, espera, como as outras habilidades que não ferem.
    - Depois, o sorteio de sempre.
  - **A ficha:** na tela gráfica, a dica da carta mostra a nota (`estado._ficha_inimigo`, só quando há nota; `batalha.js`, `10-contratos.css`). No modo texto, o Analisar mostra a mesma linha.
  - **O aviso:** o de sempre (a faixa na carta, a frase, o "<< preparando golpe! >>" do texto).
  - **Aviso antigo:** saiu o "Protótipo: o fundo da capela fica para a próxima parte da missão.".
  - **Cenário de teste:** `tests/navegador/cenarios.py`, cenário `capela`, aceita `SEMENTE`.
- **Resultados** (detalhes e condições na seção 10 do 14):
  - **Frequência**, em lutas com o herói podendo responder (robô, um companheiro, níveis 3 e 4): o golpe só no sorteio dava 33% a 58% das lutas. **Com a regra, 97% a 100%.**
  - **Antes e depois (robô):**
    - Nível 4: vitórias iguais ou −4 pontos, vida perdida igual, cerca de um turno a mais.
    - Nível 3: −4 a −18 pontos de vitória; o pior caso é o Mago no sarilho.
    - O robô se defende toda vez e o Guerreiro dele ataca com Investida. Com um herói que só ataca com a habilidade principal, a diferença fica entre 0 e 4 pontos.
  - **Respostas:** nenhuma é sempre a melhor.
    - **Guerreiro:** o Escudo corta o golpe pela metade e custa um turno. A Investida interrompe 0,5 vez por luta no nível 3 (45% **se acertar**); se falha, o golpe vem inteiro.
    - **Mago:** sem resposta, o golpe tira de 32% a 43% da vida. A Barreira o reduz a 4–11%, por 20 de mana. A Lança de Gelo interrompe às vezes (35% se acertar).
    - **Arqueiro:** não tem como interromper antes da especialização. O Passo Ágil só reduz em média; matar o preparador primeiro rende mais.
- **Verificações:**
  - `unittest`: 228 OK, 1 pulado. Novo `tests/test_golpe_preparado.py` (9).
  - `tests.gabarito`: OK, idêntico, sem atualizar.
  - `pyflakes`: só o aviso conhecido.
  - `fumaca.mjs`: 142 checagens OK, com o cenário novo do golpe preparado.
  - Fuga e derrota conferidas numa luta real do ossuário.
  - Navegador: capturas em 1500 e 1280 px (Guerreiro com Escudo e com Investida, nos casos em que interrompe e em que falha; Mago com Lança; Arqueiro com Passo Ágil no sarilho); o aviso medido quadro a quadro.
- **Limitações:**
  - Em 1280 px, a faixa de ação de outro inimigo pode cobrir a linha do aviso por até 1,5 s quando a vez chega; é a faixa comum, que some sozinha.
  - O herói atordoado perde a vez de responder; é raro, mas acontece.
  - O bestiário da espécie não fala da variante; a ficha da carta fala.
  - A E5 não está concluída.
- **Como testar (rota curta):**
  1. Com o Guerreiro na capela, desça ao ossuário. No primeiro turno, ataque o Esqueleto comum.
  2. O Esqueleto de Guarda prepara: a carta dele avisa. Passe o mouse para ler a ficha. Responda com Erguer Escudo e veja o golpe sair pela metade.
  3. Salve antes de descer, carregue e repita a luta respondendo com Investida no Esqueleto de Guarda: se atordoar, o golpe se perde; se não, ele vem inteiro.
  4. Opcional: solte as correntes à mão e veja o Afogado Inchado no sarilho fazer o mesmo.

### 10/10/2026 — E5, P3: a encruzilhada e o Grimório que explicam (1.58.0)

- **Pedido de Jean:** implementar só a P3 da E5, sem P2, habilidade nova, reespecialização nem preparação de habilidades, e sem mexer em números de equilíbrio.
  - Na escolha de especialização, comparar os dois caminhos antes de confirmar: estilo, habilidades de agora e a futura (com o nível), o que o caminho dá, atributos, limites. Detalhes acessíveis sem páginas obrigatórias. Dizer que a escolha é definitiva.
  - Olhar não aplica; confirmar aplica uma vez; voltar compara de novo. Narração preservada.
  - Números das funções de verdade, numa cópia; consultar não muda atributos, recursos, aprovação, sorteio nem save.
  - Grimório: imunidade ao veneno, a Marca para os aliados, a Combustão com uma e três camadas, o terror do Paladino, defesa e chances "se acertar". Sem prometer o que não existe.
  - O aviso do golpe preparado coberto em 1280 px, sem espera nova.
  - Modo texto com a mesma informação; gabarito só com mudanças de texto.
  - Registrar que a P1 não comprovou utilidade do Passo Ágil. Parar antes da P2.
- **Implementado** (detalhes na seção 11 do 14):
  - **`rpg/especializacao.py`** (novo): `aplicar_bonus` e `animal`, que a escolha de verdade passou a usar; `previa`, a conta feita numa cópia do herói; a página do caminho no Grimório.
  - **`SPECS[...]["limites"]`** (`classes.py`): o que cada caminho não faz, em texto.
  - **A escolha** (`eventos/classe.py`): comparar → olhar de perto → Confirmar ou Voltar (Esc). Tela nova `telas/especializacao.js` (dois cartões, o detalhe num `<details>`); no modo texto, o resumo e o detalhe.
  - **Estados** (`estados.py`): campo `imunes`; textos da guarda, esquiva, furtivo e marcado.
  - **Habilidades** (`habilidades.py`): o "Se acertar" nas linhas condicionadas; a Combustão com três exemplos; descrições de Investida, Marcar Presa, Lança de Gelo e Flecha Envenenada.
  - **Grimório:** regras gerais só quando servem; a página do caminho; `grimorio.texto` na tela de personagem do modo texto.
  - **O aviso:** `03-batalha.css`, a carta de quem prepara por cima na vez do herói.
- **Passo Ágil:** a P1 não comprovou utilidade nos encontros medidos (pior que atirar ou matar o preparador antes). Fica como questão para a P2.
- **Verificações:**
  - `unittest`: 236 OK, 1 pulado. Novo `tests/test_especializacao.py` (8).
  - `tests.gabarito`: atualizado de propósito. Só textos mudaram (descrições curtas, Grimório, tela de personagem do texto, uma quebra de linha). Tirando esses textos, as 24 transcrições ficam idênticas: escolhas, opções, lances e sorteio.
  - `pyflakes`: só o aviso conhecido.
  - `fumaca.mjs`: 148 checagens OK, com o cenário novo da encruzilhada e a checagem de que nada cobre o aviso do golpe preparado.
  - Navegador em 1500 e 1280 px: as três classes, os seis caminhos confirmados, olhar e voltar sem efeito, prévia igual ao herói depois, as páginas do Grimório.
- **Limitações:**
  - A habilidade do nível 7 aparece com os números do nível de agora (a tela diz isso).
  - A Ordem da Fera na prévia não sabe o animal, que só se escolhe ao confirmar.
  - A E5 não está concluída.
- **Como testar (rota curta):**
  1. `python -m tests.navegador.cenarios encruzilhada` (com `CLASSE=arqueiro`, por exemplo) e abra o endereço.
  2. Compare os dois cartões. Abra "Olhar de perto" num, leia os números, aperte Esc e veja os cartões de novo, sem nada mudado na ficha.
  3. Confirme um caminho e confira na ficha os atributos que a prévia prometeu.
  4. Abra o Grimório: a página do caminho no fim da lista; com o Arqueiro, Marcar Presa; com o Mago Piromante, a Combustão.

