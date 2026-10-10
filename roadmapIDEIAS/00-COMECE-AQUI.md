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
| E3 — missão mínima | Entregas na 1.50.0, 1.51.0 e 1.52.0 (registros abaixo): da Fonte Nova ao canal, à Capela Afogada e ao seu interior (nave, sacristia, ossuário, soltar as correntes). O fundo (Ilse), o rito, a comporta, Caspar e os desfechos ainda não. Falta Jean jogar. |
| E4–E11 | Plano de trabalho futuro; infraestrutura existente não equivale a etapas concluídas. Notas aprovadas para a E3 na seção 19 do [11](11-E1-REGIAO-INICIAL.md). |
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
