# 00 — Comece aqui: continuidade do projeto

Registro de passagem de contexto — 09/10/2026 (horário de Brasília).

Este arquivo permite continuar o projeto em uma nova conta ou sessão sem depender das conversas anteriores. É um ponto de entrada; os documentos temáticos detalham o plano. Atualize o estado ao concluir entregas relevantes, sem marcar proposta como decisão ou leitura como teste executado.

**Plano operacional atual (17/10/2026):** [23 — Arte, interface e clareza do combate](23-PLANO-DE-ARTE-INTERFACE-E-COMBATE.md).
As referências antigas abaixo são históricas; conferir os registros recentes e o código antes da próxima entrega.

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
- A HUD de ferro é a interface padrão desde a 1.89.0 (molduras, superfície mais escura, ícones pela família de ferro;
  `docs/ARQUITETURA.md`, "A interface web"). Os cenários continuam a referência da arte do mundo: personagens e objetos
  novos preservam formas simples, cores contidas e características reconhecíveis; retratos podem ser desenhados pelo
  método dos cenários (grade de pixels em código), com mais detalhe só quando o tamanho deixa. O catálogo de ícones não
  é refeito de uma vez; o que ainda não tem desenho fica com o do jogo (lacunas em `docs/ARQUITETURA.md`).
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
| E5 — classes | Diagnóstico (só design) em [14](14-E5-DIAGNOSTICO-CLASSES.md), sobre a 1.56.0. **P1 implementada na 1.57.0:** o golpe preparado em duas lutas fixas da capela (seção 10 do 14). **P3 implementada na 1.58.0:** a encruzilhada compara os dois caminhos e o Grimório explica (seção 11 do 14). **P2 começada na 1.59.0, só pelo Tiro Duplo** (seção 12 do 14): o 2º disparo vai no outro inimigo mais ferido. **Drenar Vida, Desaparecer e Passo Ágil avaliados em lutas inteiras** (seção 13 do 14, sem mudar o jogo): os dois primeiros têm função. **O desvio do Passo Ágil foi validado e rejeitado** (seção 14): usado repetidamente, vira a ação padrão contra inimigos sozinhos; o Passo Ágil fica como era. **O critério mínimo da E5 (07-ETAPAS) está atendido**: as três classes atravessam o Vale (a guardiã medida por caminho) e os seis caminhos foram avaliados em cenários direcionados. A E5 está **concluída tecnicamente**; adiado, sem ser requisito: o Passo Ágil, a sinergia Desaparecer–Execução, Sombra e Piromante contra a guardiã no nível 4, a preparação de habilidades. Falta Jean jogar. A validação da E4 jogando, por Jean, fica registrada à parte. |
| Clareza da campanha | Pausa antes da E6, a partir do teste de Jean. **Primeira entrega na 1.60.0** (registro abaixo): ações da capela organizadas, Diário reorganizado, linguagem do Vale simplificada, cartão de atualização de missão. **Revisão na 1.60.1**: ações curtas com custo e risco numa nota, e o conhecimento conforme as descobertas (o critério está no 07). **Na 1.60.2**: porta ou ação à vista no menu e grupos. **Na 1.60.3**: o cartão de novidade como nota da história e o Diário na Alegreya Sans. **Na 1.60.4**: revisão editorial dos textos que antecipavam a resolução (critério no 07). **Na 1.61.0**: custo dos consumíveis nas opções, a proteção do mendigo e o fluxo da exaustão. Pendentes: a dívida do Morel e a revisão de loot. As próximas entregas estão listadas em [07](07-ETAPAS.md) ("Entre a E5 e a E6"), sem implementar. Falta Jean testar. |
| E6 — transformação | **Implementada na 1.62.0** (registro abaixo; seções 11 a 14 do [15](15-E6-TRANSFORMACAO.md)): a Prisão de Gelo, talento do tronco do Mago (nível 4) que libera outra versão da Lança de Gelo, trocada no Grimório na vila ou no acampamento. Medida em lutas inteiras: papel próprio contra o inimigo forte que prepara o golpe, sem dominar. **O critério mínimo da E6 (07-ETAPAS) está atendido tecnicamente.** Falta Jean jogar (seção 14 do 15), sobretudo golem e cavaleiro sombrio sozinhos. |
| Direção (11/10/2026) | **Decidido por Jean:** o Vale do Turvo é o primeiro capítulo completo, para validação; depois da primeira entrega da E7 vem a avaliação integrada do Vale (E9 antecipada); a E8 fica adiada; a campanha maior continua como direção, sem obrigação de expandir antes da primeira versão de teste. **Em aberto:** a duração, que vem de partidas de jogadores novos. Detalhes no [01](01-VISAO.md) ("Direção") e no [07](07-ETAPAS.md) ("Ordem atual"). |
| E7 — equipamento e build | **Primeira entrega implementada na 1.63.0:** o Broquel do Vigia, medido em lutas inteiras ([16](16-E7-ITEM-E-LOOT.md), seção 5). Antes, o saque do Vale foi medido e o baú da campanha passou a dar um suprimento (1.62.6). Falta Jean jogar (cenários `broquel` e `muralha`). Os exemplos para Arqueiro e Mago não foram começados. |
| E8 — raças e origens | **Adiada explicitamente** (11/10/2026). |
| E9 — avaliação do Vale | **Em andamento, não concluída.** Diagnóstico em [17](17-E9-VALIDACAO-DO-VALE.md) (seções 1 a 12). **Na 1.64.0** (seções 13 a 16): fome e infecção levam ao resgate na campanha, que alimenta herói e comitiva sem gastar a bolsa e trata a emergência; a nota "Consome 1 provisão por dia." ao aceitar um companheiro; o fim do capítulo no Vau, no rastreador e no Diário; a partida de Jean (mago) registrada como evidência humana. Dificuldade dos combates sem mudança. **Na 1.65.0** (seção 17): interface, retorno e texto (mercador, toques que se perdiam, menu inicial, nome na ficha, talentos, balões, servo, espólio, "fonte nova", pântano e Charco, a teia, a bolsa, o mural); os rótulos dos prédios não reproduziram. **Na 1.65.1** (seção 18): a percepção do Mago na água, o nome da Yara só depois de o herói conhecê-la, e a segunda Lança de Gelo antes de o inimigo agir dizendo "já congelado" (a regra do Firme confirmada, sem mudança). **Na 1.65.2 e 1.65.3** (seção 19): a partida da Quibia lida; os contratos cumpridos pagam na vila também depois do resgate; o ×N dos baús em destaque. **Na 1.65.4:** a noite e a tocha ditas antes da luta (capela e lugar). **Na 1.66.0:** a primeira implementação da abertura guiada ([18](18-E9-ABERTURA-GUIADA.md), seção 12): a caixa "Mostrar tutorial", a despensa, Morel previsível, C1–C4, V1 e a Ajuda (F1). **Na 1.66.1 e 1.66.2** (seção 13 do 18): os riscos da capela em indicadores com ícone junto da ação; o acabamento dos quadros (destaque fino e pulso lento, lugar parado fora das cartas, C4 em linhas com "Entendi", "Encerrar tutorial", a cena depois da despensa esperando o Continuar). **Na 1.66.3** (seção 14 do 18): os ícones do C4 alinhados, o V1 ("Clique no mural para ver os contratos disponíveis.") abaixo do cenário, sem "clique: contratos", a fogueira com o rodapé distribuído e a fome numa linha de condições embaixo das barras. **Na 1.66.4:** a fome em etiqueta, a nota do acampamento só no menu, as cores dos avisos do lugar. **Na 1.67.0** (seção 15 do 18): a segunda parte da abertura guiada (V2 recuperar, V3 provisões, V4 comitiva, V5 explorar, E1 equipamento, T1 talentos, N1 noite), uma por vez. **Na 1.67.1** (seção 16 do 18): o alvo trazido à vista, o V4 no botão Comitiva, o texto da noite, Odette e os lobos, a fuga com retorno visual e som, as teclas que abrem e fecham, e adiantar o texto sem guarda de tempo. **Na 1.68.0** (seção 17 do 18): o primeiro atendimento grátis do templo, um contrato do mural ao pagamento, o primeiro baú, os selos da luta e adiantar a apresentação. **Na 1.68.1** (seção 18 do 18): textos curtos ligados à ação, os efeitos das cartas como ícones (nome e efeito, a duração dita uma vez), adiantar separado pela ocasião (revelar, velocidade, animação), a seta encostando no alvo (contrato, baú, ícone, noite) e a derrota na luta preparada do cenário de teste indo ao resgate. Faltam os jogadores novos (ficha na seção 9) e Jean jogar a 1.64.0 (roteiro na seção 16). **Na 1.68.2** (seção 19 do 18): o quadro do contrato logo na volta à vila, o Entendi no quadro da animação e a derrota com faixa ("Você caiu" / "Você morreu"), som e o cenário escuro até o resgate. **Na 1.69.0** (seção 20 do 18): a queda vira direto para o resgate; o primeiro ferimento, a bandagem, a Curandeira (com o primeiro tratamento grátis) e o descanso na taverna e no acampamento, com os números das regras. **Na 1.69.1** (seção 21 do 18): o acabamento dos textos (o quadro ensina a ação, o cartão mostra custo e resultado, a Ajuda guarda os detalhes): Curandeira, Templo, o cartão Dormir e a fogueira em linhas curtas. **Na 1.70.0** (seção 22 do 18): a bandagem só enfaixa uma ferida aberta do herói (sem vida, sem comitiva; mudança de mecânica autorizada por Jean), o primeiro ferimento em três linhas e as flechas recolhidas no espólio. |
| E10–E11 | Plano de trabalho futuro; infraestrutura existente não equivale a etapas concluídas. A E10 depende da avaliação do Vale. Notas aprovadas para a E3 na seção 19 do [11](11-E1-REGIAO-INICIAL.md). |
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

### 10/10/2026 — E5, P2: o Tiro Duplo (1.59.0)

- **Pedido de Jean:** começar a P2 por uma habilidade só, o Tiro Duplo do Patrulheiro, sem mexer em outras habilidades, classes, regeneração, talentos, itens nem imunidades.
  - Dar a ele um papel distinto do Tiro Certeiro (concentra num alvo) e da Chuva de Flechas (o grupo inteiro), sem virar a melhor ação de todo turno.
  - O 1º disparo no alvo escolhido; o 2º no outro inimigo de pé, o mais ferido pelo critério existente (documentado, com desempate); sozinho, no mesmo alvo; a morte do 1º não cancela o 2º.
  - Sem segunda seleção de alvo nem infraestrutura geral de vários alvos.
  - Comparar antes com custo, flechas e coeficientes atuais, nos níveis 4–6 e em cenários direcionados; propor ajuste só se preciso.
  - Coerência entre execução, Grimório, descrição e prévia; conferir na tela; parar antes de Drenar Vida, Desaparecer e Passo Ágil.
- **Implementado** (detalhes na seção 12 do 14):
  - **`Dano(..., em="outro")`** (`habilidades.py`): o golpe vai em `segundo_alvo`, que é outro inimigo de pé, o mais ferido; sem outro, o próprio alvo; sem ninguém, nenhum.
  - **`mais_ferido`:** a menor fração de vida, o critério da cura dos inimigos e das preces da Odette. No empate, o primeiro na ordem da luta (a carta mais à esquerda).
  - **Tiro Duplo:** os dois disparos na mesma rajada (`Salva`), o 2º com `em="outro"`.
  - **Textos:** descrição curta nova; o Grimório ganhou a linha de para onde vai o 2º, e a prévia da encruzilhada usa as mesmas linhas. `docs/COMO_CRIAR.md` (tabela dos blocos) explica o `em="outro"`.
  - **Números:** custo, flechas e coeficientes não mudaram.
- **Resultados** (nível 4; tabelas dos níveis 4, 5, 6 e 9 na seção 12 do 14). Valores: turnos para limpar e ações inimigas.
  - **O Tiro Duplo ganha:**
    - **Um quase morto e outro de pé:** 2,33 turnos e 1,42 ações inimigas, contra 2,86 e 1,95 do Tiro Certeiro e 3,03 e 2,12 da Chuva, com o Foco do Tiro Certeiro.
    - **Dois feridos ao alcance de um disparo, com menos de 20 de Foco:** 1,61 e 0,73, contra 2,18 e 1,27 do Tiro Certeiro.
  - **Outra habilidade continua melhor:**
    - **Um alvo resistente:** o Tiro Certeiro (4,41 turnos, contra 4,78).
    - **Dois com bastante vida:** o Tiro Certeiro, porque concentrar derruba antes (4,60 ações inimigas, contra 5,75).
    - **Três ou mais, com Foco:** a Chuva.
    - **Dois feridos fora do alcance de um disparo** (níveis 5 e 9): o Tiro Certeiro, por pouco.
  - **Simulador e replay:** dentro do ruído; as lutas ficam um pouco mais curtas, e o robô quase não usa o Tiro Duplo.
- **Verificações:**
  - `unittest`: 246 OK, 1 pulado. Novo `tests/test_tiro_duplo.py` (10). O `test_habilidades` não conta o 2º disparo como linha de dano própria.
  - `tests.gabarito`: idêntico, sem atualizar. O arqueiro do robô não passa do nível 2 nas 24 partidas.
  - `pyflakes`: só o aviso conhecido.
  - `fumaca.mjs`: 151 checagens OK, com o cenário novo do Tiro Duplo.
  - `tests.equilibrio --spec patrulheiro` (30 e 150 lutas, com e sem comitiva) e `tests.replay`, antes e depois.
  - Navegador em 1500 e 1280 px:
    - um disparo em cada inimigo;
    - o 1º derruba e o 2º segue;
    - a rajada e o registro;
    - Foco e flechas;
    - o Grimório e a prévia.
- **Limitações:**
  - "Mais ferido" é por fração de vida: um grande a 30% recebe antes de um pequeno a 40%.
  - Um 1º disparo que erra não é repetido no mesmo alvo quando há outro de pé.
  - As duas flechas saem mesmo quando o 1º derruba o último.
  - Não há aviso de "ao alcance de um disparo": o jogador decide pela vida nas cartas e pela faixa de dano do Grimório.
  - A E5 não está concluída.
- **Como testar (rota curta):**
  1. `python -m tests.navegador.cenarios tiro_duplo` e abra o endereço. Alfa está quase morto, Beta inteiro e Gama a 40%.
  2. Use o Tiro Duplo em Alfa: o 1º derruba Alfa e o 2º vai em Gama. O registro diz quem recebeu cada tiro.
  3. Suba de novo e compare: o Tiro Certeiro em Alfa (derruba, mas Gama fica inteira), a Chuva de Flechas (acerta os três, por 20 de Foco).
  4. Com `VIDAS=1,1,1`, compare o Tiro Certeiro e o Tiro Duplo em lobos inteiros: o Duplo espalha e o primeiro abate demora.
  5. Grimório (P), página do Tiro Duplo: a faixa de dano e a linha de para onde vai o 2º.

### 10/10/2026 — E5, P2: avaliação de Drenar Vida, Desaparecer e Passo Ágil (sobre a 1.59.0, sem mudar o jogo)

- **Pedido de Jean:**
  - avaliar os três candidatos restantes da P2 em combate completo (dano, sobrevivência, recursos, aliados, duração), sem alterar gameplay nem números;
  - Drenar Vida contra as alternativas do Necromante: vida cheia, ferido, por um fio, luta longa, vivos e mortos-vivos, com e sem servo, cura real, abates e dano além da vida;
  - Desaparecer e Passo Ágil contra atacar e priorizar o perigoso: golpe preparado, vários atacantes, pouca vida, com e sem aliado, o ataque seguinte e as sinergias;
  - o risco de derrota, além das médias; o Vale separado do que vem depois; roteiros descritos, sem o robô julgando;
  - classificar, recomendar manter ou ajustar, e uma única próxima implementação, ou encerrar.
- **Entregue:** seção 13 do [14](14-E5-DIAGNOSTICO-CLASSES.md); respostas nas seções 11.5 e 12.8; estado no 07. Nenhum arquivo fora de `roadmapIDEIAS` mudou; scripts fora do repositório.
- **Método:**
  - lutas inteiras pelo combate do jogo, com a IA dos inimigos e roteiros fixos de decisão;
  - herói com equipamento mediano (semente perto da mediana de vida e ataque), talentos declarados, sem poções;
  - encontros do Vale (ossuário e sarilho com golpe preparado, lobos, bruxa e sapo) e de depois (bandidos, mercenário, carniçais, troll, guardião);
  - vida cheia, ferido (45%), por um fio (25%) e com Morel;
  - 600 lutas por linha; os casos perto do ruído refeitos com outras sementes e 3000 lutas.
- **Resultados:**
  - **Drenar Vida: função útil demonstrada.**
    - Ferido, contra vivos, salva a luta: 3 lobos, 12% → 80% de vitórias; bruxa e sapo, 61% → 90%; bandidos (nível 7), 28% → 57%; troll, 45% → 63%.
    - Com o servo é a melhor combinação contra vivos e nas lutas longas (guardião, de vida cheia: 77%, contra 46% só com Bola de Fogo).
    - Contra mortos-vivos é armadilha: no ossuário, ferido, 13%, contra 81% da Bola e 93% da Barreira. O jogo já avisa.
    - A cura conta o golpe inteiro, mesmo o que passa da vida do alvo (15–23% da cura); mana nunca falta.
  - **Desaparecer:**
    - No Vale, sem vantagem relevante: empata com atacar e perde no preparo.
    - Depois, função restrita, mas legítima: abertura com crítico contra dois inimigos resistentes, ferido (carniçais 69% → 83%, confirmado). O ganho vem do crítico, não da esquiva.
    - A sinergia com a Execução piorou em todo encontro: hipótese sem evidência.
  - **Passo Ágil: sem vantagem relevante** no Vale e depois, com ou sem aliado. Atacar ganha até diante do golpe preparado (ossuário, arqueiro 3: 95% contra 87%).
- **Recomendação:**
  - Manter Drenar Vida e Desaparecer: recuperar mana e mudar a mira em furtividade não têm motivo medido.
  - Ajustar só o Passo Ágil: trocar a chance de esquiva pelo **desvio de um golpe** (o próximo que acertaria, nas duas vezes seguintes dos inimigos).
    - Testado só no script: contra o troll ferido, 60% → 79%.
    - No Vale, sem efeito; usado todo turno, piora.
    - A variante "sem gastar o turno" foi rejeitada: vira a ação de todo turno.
    - Nada foi implementado.
- **Próximo passo:** Jean decide entre implementar o desvio do Passo Ágil (a única próxima implementação recomendada) ou encerrar esta parte da P2. A E5 continua aberta.

### 10/10/2026 — E5, P2: validação do desvio do Passo Ágil e fechamento da E5 (sobre a 1.59.0, sem mudar o jogo)

- **Pedido de Jean:**
  - fechar esta parte da P2 pelo Passo Ágil, sem mexer em Drenar Vida e Desaparecer;
  - validar o desvio com outras sementes antes de incorporá-lo: troll, mercenário sozinho e acompanhado, guardião com golpe preparado, ossuário ou sarilho, grupo fraco; atacar, responder à preparação e usar repetidamente; Patrulheiro com animal e Arqueiro com comitiva;
  - implementar só se houvesse vantagem nas situações apropriadas sem virar a ação padrão; senão, encerrar com os resultados, sem forçar outra mecânica;
  - informar se o critério mínimo da E5 está atendido, sem manter a etapa aberta por hipóteses.
- **Resultados medidos** (seção 14 do [14](14-E5-DIAGNOSTICO-CLASSES.md); 1200 lutas por linha, sementes novas, antes e depois na mesma régua):
  - **Responder à preparação com o desvio funciona.** Contra o troll, ferido: Sombra 7 vai de 42% (atacar) a 70%; Patrulheiro 7 com o lobo, de 71% a 86%. Contra o guardião, Patrulheiro 7: de 15% a 28%. No Vale, com Morel e ferido: de 85% a 90%. Contra grupos fracos, nada muda.
  - **Usado repetidamente, vira a ação padrão contra um inimigo sozinho.** Com um golpe por rodada, o desvio pega todos, e o Foco quase não acaba (6 por uso, 5 por turno). Troll: 100%. Guardião: 83–91%, contra 1–15% atacando, em 80 a 110 turnos, com 9–35% de lutas que não acabam.
  - **Decisão:** não incorporar. O Passo Ágil continua como era.
- **Conferência técnica (descartada com a regra):**
  - a regra foi implementada numa cópia de trabalho, com 10 testes (consumo uma vez, esquiva natural sem consumo, expiração, reaplicação sem acumular, golpe preparado, ataque não esquivável, vários golpes, dano por turno, atordoado, aliado);
  - no navegador: o golpe preparado desviado e outro inimigo gastando o desvio antes;
  - duração real: a vez inteira dos inimigos no turno em que se usa e no seguinte (duas rodadas completas, não duas ações);
  - nada disso ficou no repositório.
- **A travessia do Vale** (guardiã da capela pelo método da E3, versão atual, destruir), nível 4 / nível 5:
  - Paladino 83%/100%; Berserker 81%/96%; Patrulheiro 85%/97%; Necromante 54%/98%; Piromante 22%/66%; Sombra 26%/50%.
  - As três classes passam. Sombra e Piromante são os caminhos mais duros, como já se sabia.
- **Critério mínimo da E5:** atendido. Três classes atravessam a região (régua: robô e roteiros) e seis caminhos avaliados em cenários direcionados (seções 4, 9, 11, 12, 13 e 14 do 14). **E5 concluída tecnicamente.**
- **Adiado, sem ser requisito:**
  - um Passo Ágil com limite de repetição;
  - a sinergia Desaparecer–Execução;
  - o texto da cura do Drenar sobre o golpe inteiro;
  - Sombra e Piromante contra a guardiã no nível 4 (equilíbrio);
  - a preparação de habilidades;
  - um limite de turnos no combate, se alguma mecânica permitir luta sem fim.
- **Validação de Jean jogando:** registrada à parte. Falta jogar a P1, a P3, o Tiro Duplo e os seis caminhos.
- **Verificações:**
  - nenhum código mudou nesta entrega;
  - `unittest`, `pyflakes` e fumaça rodaram sobre a 1.59.0 antes do registro;
  - os scripts de medida ficaram fora do repositório.
- **Como testar (rota curta):**
  1. Com um Arqueiro no nível 3, desça ao ossuário (cenário `capela` com `CLASSE=arqueiro NIVEL=3 ETAPA=ossuario`).
  2. Quando o Esqueleto de Guarda avisar o golpe, use o Passo Ágil: é o de hoje (+30% de esquiva), uma chance, não uma garantia.
  3. Compare com atacar o esqueleto comum primeiro, como as medidas indicam.
  4. Com um Patrulheiro (encruzilhada ou `--dev 7`), use o Tiro Duplo num grupo ferido; e confira na Encruzilhada a comparação dos caminhos e no Grimório os textos da P3.

### 10/10/2026 — Clareza da campanha, primeira entrega (1.60.0)

- **Pedido de Jean** (a partir do teste real dele; o avanço para a E6 ficou pausado e o Passo Ágil não voltou):
  - organizar as ações da capela;
  - reorganizar o Diário;
  - simplificar a linguagem do Vale e da capela;
  - destacar as atualizações de missão;
  - registrar as próximas entregas sem implementar;
  - nenhuma mudança de equilíbrio.
- **As correntes viraram uma ação só** ("Soltar as correntes do sarilho (escolher como)"). Dentro dela:
  - a cena explica o sarilho (o eixo em que as correntes se enrolam) e diz que é um preparo opcional para o descanso de Ilse;
  - a pergunta oferece o jeito à mão (sempre funciona, chama os afogados), o método da classe (com o teste e o risco) e "Voltar sem mexer no sarilho";
  - voltar não gasta tempo, tocha, flecha nem sorteio: não há Continuar nem cartão, e a ação continua no menu (teste e fumaça conferem);
  - as duas formas deixam o mesmo preparo; regras, CD, encontros e recompensas não mudaram (as funções são as mesmas, só chamadas de dentro da escolha).
- **O menu do lugar.**
  - As ações da missão vêm primeiro, com borda dourada e a etiqueta "Missão"; os contratos levam a etiqueta "Contrato"; o resto fica como era.
  - O frasco do lodo diz para que serve. Antes da acusação de Caspar: "prova do que suja a água". Depois: "prova para a decisão sobre Caspar".
  - A descida ao fundo ficou "Descer ao fundo alagado e enfrentar a guardiã".
- **O Diário, por missão, nesta ordem:**
  1. o objetivo e o lugar;
  2. o mais recente, com o dia;
  3. caminhos e preparos. O rito aparece como "Caminho opcional: dar descanso a Ilse em vez de destruí-la. A missão termina pelos dois caminhos". A Vigília de Caspar mostra "Aguardando: Caspar só cobra a resposta quando a febre for resolvida" enquanto a febre não acaba;
  4. o histórico da investigação, fechado, do mais novo para o mais antigo, com o texto inteiro de cada descoberta.
- **O histórico é novo** (`historico` no registro da missão; o que mudou em cada ação ou cena, com o dia). Em saves de antes, o que já se sabia aparece num bloco "Antes deste registro (sem data)", sem datas inventadas.
- **O cartão de atualização.**
  - Depois de cada ação ou cena de missão, um cartão compacto dentro do texto (o mesmo papel do Diário). Ele junta o que se descobriu ou fez (nomes curtos) e o objetivo novo, quando muda.
  - Um cartão por cena, mesmo com várias pistas. Não é janela, não cobre as escolhas e não aparece no meio da luta (vem depois dela).
  - Carregar um save não repete nada: o cartão sai da diferença antes e depois da cena, não do estado.
  - As linhas soltas "Diário: ..." e o efeito "Diário atualizado" saíram, porque o cartão os substitui.
- **Textos.**
  - "nave" virou "salão principal" ou "salão alagado" (a cena "A Nave Alagada" é agora "O Salão Alagado");
  - "mós" virou "pedras de moinho"; "cripta", "fundo alagado"; "rombo" e "nicho", "buraco"; "adro", "pátio da frente";
  - o sarilho é explicado onde aparece;
  - objetivos e rótulos foram revistos: "o ossuário, a sala dos ossos", "a sacristia, atrás do altar".
  - Identificadores internos (`nave`, `correntes`, `fundo`...) e os acontecimentos não mudaram.
- **Verificações:**
  - `unittest`: 14 testes novos em `tests/test_clareza.py` (voltar sem gastar, um cartão por cena, fuga sem cartão, carregar sem repetir, histórico com dia, save antigo sem datas, rito opcional, Vigília aguardando, rótulo do lodo, ordem do menu); os testes da capela foram adaptados à escolha interna;
  - gabarito idêntico, sem atualizar (ele joga o mundo gerado, sem missões);
  - `pyflakes` limpo;
  - fumaça com o cenário novo do sarilho e os cartões da sacristia e do Diário;
  - capturas em 1500 e 1280 px (menu da capela, escolha do sarilho, cartão, Diário com histórico e a Vigília aguardando).
- **Próximas entregas:** registradas em [07](07-ETAPAS.md) ("Entre a E5 e a E6"), sem implementar: a bandagem da Odette, a proteção do mendigo, o fluxo "Continuar → Exausto → Continuar", a dívida do Morel e a revisão de loot.
- **Como testar (rota curta):** veja a mensagem da entrega. Em resumo:
  1. Comece a campanha e examine a Fonte Nova: aparece o cartão.
  2. Abra o Diário (D).
  3. Na capela, no fundo, abra "Soltar as correntes" e volte.
  4. Abra de novo e solte.
  5. Salve, carregue e confira que nada se repete.

### 10/10/2026 — Clareza da campanha, revisão (1.60.1)

- **Pedido de Jean** (depois de testar a 1.60.0): algumas telas explicavam diretamente como resolver a missão. Ações claras e informações vindas das descobertas do personagem; só apresentação e texto, sem tocar em regras, custos, testes, encontros, recompensas, progresso ou equilíbrio.
- **Menu da capela.**
  - As ações ficaram com nomes curtos: "Soltar as correntes", "Descer ao fundo alagado", "Recolher uma amostra do lodo", "Atravessar o salão alagado", "Descer ao ossuário".
  - A distinção visual da 1.60.0 continua: borda dourada, ícone e a etiqueta "Missão" das ações da missão.
  - A finalidade da amostra saiu do rótulo. Ela aparece no Diário de Caspar, como "o que pode mostrar à praça que a febre veio da água, e não de Yara".
- **Cena das correntes.**
  - O texto descreve o mecanismo: o eixo, a trava de ferro, as correntes e as pedras de moinho.
  - A ligação com o rito só aparece depois de Vó Berta, citando o que ela disse.
  - As opções: "Desenrolar as correntes à mão", o método da classe com o teste ("Arrancar a trava", "Apodrecer o ferro da trava", "Acertar o pino da trava") e "Deixar como está".
  - Custo e risco ficam numa nota embaixo de cada opção: a luta contra os afogados à mão, a flecha do arqueiro, o que acontece se o teste falhar. No modo texto, a nota vem depois de um travessão.
  - O arqueiro passou a ver o próprio bônus de Destreza, como as outras classes.
  - "Deixar como está" segue sem custo, sem tempo, sem sorteio e sem Continuar.
  - Saiu do ossuário a linha "As correntes podem ser soltas daqui… (não é obrigatório…)".
- **Diário.**
  - A lista do rito só aparece depois da conversa com Vó Berta, atribuída a ela ("Vó Berta contou que um afogado descansa quando alguém o chama pelo nome e o solta das pedras"), com ✓ no que já está feito.
  - O lugar das correntes só aparece para quem já viu o sarilho.
  - Antes de Berta, aparecem "Perguntas em aberto", tiradas das pistas que o personagem já tem: quem se lembra da noite do afogamento; o que as correntes prendem; quem são os homens marcados.
  - Um preparo feito antes de Berta continua em "O que você já fez".
  - Saíram as dicas entre parênteses, o "caminho opcional… termina pelos dois caminhos" e o "Aguardando… (A Febre do Turvo). Até lá, junte a prova". A Vigília agora diz "Aguardando o fim da febre: Caspar prometeu que, quando ela acabar, a vila vai saber de quem era a culpa".
  - Saves antigos: tudo sai das pistas e dos preparos registrados. Nada novo é inventado.
- **Descida ao fundo.** O aviso do que falta para o rito só aparece para quem ouviu Vó Berta, e cita o que ela contou. As opções da descida são as mesmas de antes.
- **Cartão de atualização.** O formato não mudou ("As correntes estão soltas"; o objetivo só quando muda). Mudaram os nomes curtos: "Vó Berta contou como um afogado descansa" e "Uma amostra do lodo do fundo da capela".
- **Verificações:**
  - `unittest` com testes novos: a cena sem o rito antes de Berta, as três classes deixando o mesmo preparo, o rito só depois de Berta, um preparo feito antes de Berta, a finalidade da amostra no Diário de Caspar;
  - gabarito idêntico, sem atualizar;
  - `pyflakes` limpo;
  - fumaça, três vezes seguidas sem falha. O auxiliar `esperar` da 1.60.0 aguardava às cegas a guarda do Continuar e gastava a guarda que outra checagem media; agora ele confere durante a espera;
  - capturas em 1500 e 1280 px: menu, sarilho das três classes, sarilho depois de Berta, Diário antes e depois de Berta.
- **Como testar (rota curta):**
  1. `python -m tests.navegador.cenarios capela` com `ETAPA=fundo`: veja o menu, abra "Soltar as correntes", compare as opções e escolha "Deixar como está".
  2. Abra o Diário: aparecem as perguntas em aberto e nenhuma receita.
  3. Repita com `PREPARO=berta`: a cena cita Vó Berta e o Diário mostra o que ela contou, com ✓ e ○.
  4. Salve e carregue: nada se repete.

### 11/10/2026 — Clareza da campanha: menu e leitura (1.60.2)

- **Pedido de Jean** (depois de testar a 1.60.1):
  - os "?" na frente das perguntas confundiam;
  - o texto do Diário, numa serifa fina sobre o pergaminho, cansa a vista: testar a Pixeloid Sans;
  - no menu da capela, "Soltar as correntes" e "Descer ao fundo alagado" pareciam decisões que se excluem, e não dava para saber qual opção abre mais escolhas e qual age na hora. Resolver pela linguagem da interface, sem avisos de "decisão sem volta".
- **Menu do lugar.**
  - As opções vêm em grupos. "Missão" e "Contratos" têm um rótulo pequeno, no estilo de "O que você faz?". As ações de sempre vêm depois de um fio tracejado.
  - Saiu a etiqueta "Missão" de cada linha. A borda dourada e o ícone continuam.
  - Quem abre outra escolha, de onde se volta, leva uma seta discreta no fim: "Soltar as correntes", "Descer ao fundo alagado" e "Ir à praça responder a Caspar". O frasco do lodo, que age na hora, não leva. No modo texto, a seta é um "›" depois do rótulo.
  - A descida ao fundo, o passo que leva a história adiante, fica por último entre as ações da missão.
  - Nenhum texto novo dizendo que uma coisa prepara a outra. Isso vem das descobertas, no Diário, como na 1.60.1.
- **Leitura.**
  - A Pixeloid Sans (GGBotNet, licença OFL, em `fontes/` com o `OFL-PixeloidSans.txt`) é a fonte dos papéis do Diário (a missão e o cartão de novidade) e das notas embaixo das opções.
  - Tamanho principal de 18px: a fonte tem 9 pixels por eme, e cada pixel da letra cai inteiro na tela. Sem itálico falso: o secundário fica na cor mais clara.
  - "Fonte: pixel", no topo, passou a usar a mesma Pixeloid Sans na história, para comparar com a Alegreya. A Pixelify Sans continua no repositório.
  - As perguntas em aberto usam marcadores comuns, sem os "?".
- **Regras:** nada mudou. Falhar o teste da classe nas correntes não trava nada: o rangido chama os afogados na hora, e quem os vence termina à mão na mesma cena. Quem foge sai com as correntes presas e pode voltar e escolher de novo, inclusive o método da classe. O arqueiro gasta uma flecha por tentativa.
- **Verificações:**
  - `unittest`: a ordem e as setas no menu, a seta no modo texto;
  - gabarito idêntico, sem atualizar;
  - `pyflakes` limpo;
  - fumaça: grupos, setas e nenhuma etiqueta por linha;
  - capturas em 1500 e 1280 px: o menu nas duas fontes, o sarilho das três classes, o Diário antes e depois de Berta e o histórico aberto.

### 11/10/2026 — Clareza da campanha: o cartão e o Diário (1.60.3)

- **Pedido de Jean:** achou feio o cartão de atualização na Pixeloid Sans e perguntou como os profissionais fariam. Aprovou a proposta, depois de ver antes e depois no jogo, e mandou a Alegreya Sans.
- **Critério** (a referência é Disco Elysium e Pentiment): a atualização da missão entra no fluxo do texto, na fonte da história, e se distingue por cor, por um rótulo em versalete e por um fio na margem. A fonte pixel ou gótica fica só em títulos e rótulos curtos.
- **Cartão de novidade.**
  - Saiu o papel claro com sombra. Ficou uma nota com um fio dourado na margem e um brilho leve atrás.
  - Em cima, "DIÁRIO ATUALIZADO" (ou "MISSÃO NOVA", "CONCLUÍDA") em versalete, e o nome da missão no gótico dourado.
  - Cada descoberta tem um losango dourado. Embaixo vem "OBJETIVO" em versalete e o objetivo em letra clara.
  - Usa a fonte da história: Alegreya, ou a Pixeloid na "Fonte: pixel".
- **Diário.**
  - O pergaminho fica. O texto passou para a Alegreya Sans (Regular e Bold, OFL), recortada para o alfabeto latino em woff2: 29 KB cada, com o `OFL-AlegreyaSans.txt`.
  - 18–19px, tinta escura, sem itálico. Os rótulos ("MAIS RECENTE · DIA 1", "PERGUNTAS EM ABERTO", "HISTÓRICO DA INVESTIGAÇÃO", os dias) em versalete.
  - As notas embaixo das opções usam a mesma Alegreya Sans.
- **Pixeloid Sans:** fica na "Fonte: pixel" e na seta de quem abre outra escolha.
- **Regras:** nada mudou.
- **Verificações:**
  - `unittest`, gabarito idêntico, `pyflakes` e fumaça;
  - capturas em 1500 e 1280 px: o cartão da sacristia, o Diário, o histórico aberto e o sarilho.

### 11/10/2026 — Clareza da campanha: revisão editorial (1.60.4)

- **Pedido de Jean:** uma revisão localizada dos textos que antecipavam a resolução de cenas ou explicavam demais o funcionamento do jogo, com prioridade para as correntes e o confronto com Ilse, além de quatro textos menores. Só apresentação: regras, custos, testes, encontros, recompensas e sorteios ficaram iguais. A apresentação da 1.60.3 (fontes, setas, grupos) não mudou.
- **Critério:** a cena apresenta indícios e acontecimentos, a alternativa descreve a ação, a interface comunica custos e restrições, o resultado revela o que aconteceu. O texto completo está no 07.
- **Correntes.** Os rótulos são os mesmos; só as notas mudaram.
  - À mão: "Demorado e barulhento: o eixo range, e o som corre pela água da capela inteira." Antes: "o rangido chama os afogados, e é preciso vencê-los para terminar".
  - Método da classe: "Silencioso, se a trava ceder. Se não ceder, o eixo range alto." Antes dizia quem vinha e que o resto era à mão.
  - O teste (FOR, ARC, DES com o bônus) e o "Gasta 1 flecha" do arqueiro continuam. O encontro continua garantido no motor: nada de chance nova.
  - O que acontece depois, a cena mostra (os afogados, "agora vai ter de ser à mão").
- **Fundo da capela.**
  - "Depois de começar, não há como recuar" saiu da frase da cena. A cena termina em "Ela ainda não se levantou da água.", e a pergunta é "O que você faz?".
  - A regra virou a nota "Sem fuga: a luta vai até o fim." nas duas opções que começam a luta (o rito e destruir). "Voltar por enquanto" fica sem nota.
  - Sem confirmação nem janela a mais. O aviso de Berta sobre o que falta para o rito continua.
- **Guardiões do mundo gerado.** "Não haverá como fugir depois de começar." deixou de ser a pergunta. Agora a pergunta é "O que você faz?", e a mesma nota fica em "Lutar!" (`tx.SEM_FUGA`, um texto só para os dois lugares). Nenhum obstáculo inventado.
- **Textos menores, com o custo na nota:**
  - "Levá-la até X" — Toma algumas horas do dia.
  - "Parar e fabricar flechas" — Toma algumas horas do dia.
  - "Entrar e curar os doentes" — Horas de esforço: cobra da sua vida.
  - O alerta de viagem perigosa continua dizendo o nível e o risco; as opções viraram "Não ir" e "Ir mesmo assim".
- **Gabarito.** Mudou em 8 partidas, só nos rótulos e nas notas dessas opções. As escolhas são as mesmas (índices iguais), e o resto das transcrições não mudou. Foi atualizado depois da comparação.
- **Verificações:**
  - `unittest` com testes novos: notas sem antecipar o inimigo; a regra na nota do guardião e da guardiã; recuar do guardião sem gastar sorteio nem tempo;
  - gabarito;
  - `pyflakes` limpo;
  - fumaça;
  - capturas em 1500 e 1280 px: correntes, descida até Ilse, guardião, alerta de viagem, criança perdida, flechas, Paladino com os doentes. Para isso, o cenário novo `covil` em `tests/navegador/cenarios.py`, com `EVENTO` opcional.

### 11/10/2026 — Custos de consumíveis, a proteção e a exaustão (1.61.0)

- **Pedido de Jean:** uma entrega limitada a três achados do teste dele. A apresentação da 1.60.x e o critério editorial ficam como estão. Regras, custos, tempo, recuperação, sorteios e equilíbrio não mudam.
- **Reproduzido** (fumaça e `scratchpad`, no navegador, 1500 e 1280 px):
  - **Exaustão no mato.** No fim de um evento à noite vinha o Continuar do evento, a faixa "Exausto" e um segundo Continuar na mesma página, sem nada novo para ler, antes da fogueira. Causa: a faixa contava como texto novo (`novo_desde_escolha`), e a fogueira pedia leitura antes de abrir.
  - **Exaustão na vila.** A faixa "Exausto" passava por cima do texto do evento anterior, antes do Continuar dele, e só depois vinha a cena "Exausto".
- **Implementado:**
  - **Custo do consumível na opção** (`Jogo.custo_item`).
    - Com o item: a nota "Usa 1 bandagem da bolsa (você tem N)", com o ícone do item.
    - Sem o item: a opção continua à vista, desabilitada (`disabled`, `aria-disabled`), apagada e com "Indisponível: Você não tem bandagem na bolsa." escrito, e não só a cor. Nem clique, nem tecla, nem atalho a escolhem (`responder` recusa).
    - No texto, ela aparece com "— indisponível: …"; se alguém digitar o número, o jogo diz o motivo e pergunta de novo. O robô nunca a escolhe (`BotUI`), e por isso as partidas do gabarito seguem as mesmas escolhas.
    - Vale para a bandagem da Odette e para "Deixar remédios na porta" (1 poção de vida). Os outros caminhos, testes e consequências desses eventos não mudaram, e a bandagem continua gastando exatamente uma.
  - **A proteção.**
    - Quando chega (`Jogo.receber_protecao`), aparece o aviso "Proteção: se cair em combate, você se levanta uma vez".
    - O mendigo não põe "algo no bolso": fica "um calor estranho no peito". O mistério sobre quem ele é continua.
    - A flag `bencao_fenix` guarda a origem (`mendigo`, `santuario`). Um save antigo guarda só `True`, e aí a frase é neutra.
    - Quando ela levanta você: a frase da origem (o santuário só quando veio dele); na tela de combate, a carta volta a ter vida com o rótulo "De pé outra vez" (lance de cura, modo `levantar`); e o aviso "A proteção se foi: você se levantou com metade da vida".
    - A Pena de Fênix ganhou a mesma animação ("Pena de Fênix") e continua vindo antes da bênção.
    - Chances, vida recuperada (metade), um uso só e prioridade iguais. A telemetria não conta o levantar como cura, então as medidas de equilíbrio não mudam.
  - **Exaustão.**
    - A faixa "Exausto" passa sem pedir leitura (`WebUI.FAIXAS_DE_PASSAGEM`): no mato, é um Continuar para o fim do evento, a faixa e a fogueira.
    - Na vila, a faixa vem já na página da cena "Exausto". O Continuar do evento anterior, quando há texto para ler, continua.
    - Tempo, descanso, custos e o quadro do amanhecer iguais. As cenas de missão continuam esperando o Continuar delas.
- **Pendente:** a dívida do Morel e a revisão de loot (07). Também fica de fora uma marca permanente da proteção no painel do herói: hoje o aviso aparece na chegada e na ativação, e não há lembrete no meio do caminho.
- **Gabarito.** Mudou em 11 partidas, só no esperado:
  - os rótulos e as metas da bandagem;
  - as frases e os avisos da proteção;
  - o lance de levantar;
  - a ordem da faixa "Exausto" na vila;
  - a origem na flag do save.

  As escolhas do robô são as mesmas. Foi atualizado depois da comparação.
- **Verificações:**
  - `unittest` com `tests/test_custos_protecao.py` (12 testes): custo e consumo exato, indisponível sem escolha (texto e robô), origens e frase neutra, a pena antes da bênção, um uso só, a faixa sem Continuar a mais, a ordem na vila;
  - gabarito;
  - `pyflakes` limpo;
  - fumaça, com o cenário novo de custos, proteção e exaustão;
  - capturas em 1500 e 1280 px. O cenário `covil` ganhou `PERIODO`, `LUGAR`, `BOLSA`, `PROTECAO` e `LUTA`.
- **Como testar (rota curta):**
  1. Sem bandagem: `python -m tests.navegador.cenarios covil` com `EVENTO=odete_na_estrada BOLSA=bandagem=0`. A ajuda aparece apagada, com o motivo; clique e a tecla 1 não fazem nada.
  2. Repita com `BOLSA=bandagem=2`: a nota diz o custo, e a bolsa fica com 1.
  3. A proteção: `EVENTO=mendigo_misterioso LUGAR=vila`, pague a refeição e veja o aviso. Depois, `PROTECAO=mendigo LUTA=troll`: ataque, caia e veja "De pé outra vez" e o aviso de que ela se foi.
  4. A exaustão: `PERIODO=3 LUGAR=selvagem SEMENTE=9`, explore e recuse o duelo. É um Continuar, a faixa "Exausto" e a fogueira.

### 11/10/2026 — E6: especificação de uma transformação de habilidade (só design, sobre a 1.61.0)

- **Pedido de Jean:**
  - retomar o roadmap pela E6, com a especificação de uma transformação pequena que crie alternativa de build e mude
    decisões na luta;
  - no máximo três candidatos e uma recomendação;
  - arquitetura mínima;
  - validação planejada;
  - só Markdown em `roadmapIDEIAS`.
- **Lido e conferido:**
  - o escopo da E6 (07), o 04 e o 14;
  - no código:
    - quem consulta `HABILIDADES[id]` (heroi, Grimório, tela, custo, progressão, encruzilhada, `Salva`);
    - como os talentos mexem em habilidades (só números);
    - as regras do atordoar (`firme`, chefes e gigantes resistem metade, interrupção do golpe preparado);
    - a escolha de alvo dos inimigos (aliados levam 25% dos ataques);
    - que talentos não se desfazem.
- **Candidatos (seção 3 do 15):**
  - **A. Lança de Gelo → Prisão de Gelo:** recomendado;
  - **B. Erguer Escudo → Desafio:** pouco valor hoje, porque os inimigos já miram o herói;
  - **C. Golpe Pesado → Golpe Varredor:** sem recurso que limite, viraria a ação de quase toda luta do Vale, como o
    desvio do Passo Ágil.
- **Recomendação (seção 4 do 15):** a **Prisão de Gelo**, pelo talento do tronco do Mago (nível 4, 1 ponto), no lugar
  da Lança de Gelo.
  - **O que faz:** 16 de mana; 70% de dano de gelo, sem esquiva; congela sem sorteio, salvo `firme`, chefes e gigantes.
    Todos os números são [proposta].
  - **A troca:** a Lança é o dano barato com 35% de controle; a Prisão, a resposta certa ao golpe preparado de um
    inimigo forte, mais cara e fraca em grupos.
  - **O que limita a repetição** vem do jogo de hoje: a mana, o `firme`, a resistência.
- **Arquitetura mínima (seção 6 do 15):**
  - a variante fora do catálogo aprendível (`VARIANTES`);
  - `efetiva(u, h_id)` por herói;
  - `transforma` nas fontes de modificadores;
  - as consultas diretas trocadas;
  - a descrição do talento calculada das duas fichas.

  Nenhum hook novo de combate; o catálogo global não muda.
- **Validação (seção 8 do 15):**
  - os cenários: alvo único com e sem preparo, gigante e chefe, grupo, com aliados, com servo, mana curta, ferido;
  - as políticas, incluindo "Prisão sempre", que é a repetição abusiva, com e sem aliados;
  - os testes de isolamento entre heróis;
  - o navegador;
  - Jean jogando no ossuário;
  - o equilíbrio antes e depois.
- **Para decidir antes de implementar (seção 10 do 15):** a candidata, os números, o lugar do talento, desfazer
  (definitivo com comparação e confirmação, ou esperar a E7 e fazer por item) e o nome e o ícone.
- **Verificações:** só Markdown em `roadmapIDEIAS` mudou (15 novo; README, 04, 07 e 00 atualizados). Nenhum código,
  teste ou save.

### 11/10/2026 — E6: a Prisão de Gelo (1.62.0)

- **Pedido de Jean:**
  - a Prisão de Gelo como a única transformação da E6;
  - os números iniciais: 16 de mana, 70% de dano de gelo, sem esquiva, sem o sorteio; o `firme` e a resistência de
    chefes e gigantes continuam;
  - validar numa cópia de trabalho, pelo combate real, antes de consolidar. Os cenários do 15, mais:
    - Canalização e Eficiência no máximo de cada nível;
    - a comitiva e o servo, com combinações de controle;
    - o uso repetido e a alternância entre a Prisão e ataques;
    - inimigos comuns, grupos, chefes e gigantes;
    - impasses, com limite de 200 turnos;
  - o talento no tronco, nível 4, 1 ponto;
  - a compra definitiva, com a versão trocada na vila ou no acampamento, sem tela nova;
  - a resolução por herói, sem mexer no catálogo;
  - um cenário curto de comparação;
  - não começar a E7, a dívida do Morel, a revisão de loot nem outras transformações.
- **Implementado** (seção 12 do 15):
  - `VARIANTES`, `efetiva`, `transforma` e o talento;
  - a troca: opção escondida na vila e na fogueira e o botão "Levar a …" no Grimório. No texto, uma linha do menu;
  - a árvore compara as duas versões com os números do herói;
  - o robô lutador usa a Prisão em quem prepara;
  - `PRISAO=prisao|lanca` no cenário `capela`.
- **Medido** (seção 13 do 15), em cerca de 441 mil lutas em 315 células, sem nenhum impasse:
  - a Prisão é relevantemente melhor em 18% das células, equivalente em 80% e pior em 2%;
  - contra o preparador único, o herói ferido vence 82% em vez de 71%, e os golpes preparados que acertam caem de
    0,2 para 0,02 por luta;
  - em grupos, nunca é melhor;
  - repetida, ela perde em grupo, gigante e chefe;
  - Canalização e Eficiência não mudam o quadro;
  - o ponto forte é o golem e o cavaleiro sombrio sozinhos. Se for demais jogando, o menor ajuste é o alvo ficar
    firme por 2 turnos depois da Prisão.
- **Equilíbrio e replay:**
  - `tests.equilibrio` do Piromante e do Necromante ficou dentro do ruído. Com 90 lutas, as lutas comuns do
    Piromante saem iguais (69,8% → 69,4%); os guardiões, 39% → 33% em 54 lutas;
  - o replay saiu idêntico;
  - antes de o robô aprender a Prisão, ele a usava como ataque principal, e os guardiões demoravam o dobro.
- **Gabarito:** atualizado de propósito.
  - Nas partidas sem Mago, só a linha do glossário de cores mudou ("Prisão de Gelo").
  - Nas do Mago, a divergência começa no nó novo da árvore. Nenhuma partida comprou ou usou a Prisão.
- **Verificações:** testes de unidade, gabarito, pyflakes e a fumaça do navegador. O navegador a 1500 e 1280 px mostra:
  - a página da Prisão com a troca na vila;
  - a página sem a troca na capela;
  - a árvore com os dois nós do tronco lado a lado;
  - a janelinha da luta com a Prisão (16);
  - o "congelado" na luta.
- **Como testar (rota curta):**
  1. `CLASSE=mago NIVEL=4 ETAPA=ossuario PRISAO=prisao python -m tests.navegador.cenarios capela`: desça ao ossuário
     e use a Prisão no Esqueleto de Guarda quando ele preparar o golpe.
  2. O mesmo com `PRISAO=lanca`: o mesmo herói, com a Lança.
  3. Com `LUGAR=vau_do_turvo`, abra o Grimório (P) na Prisão de Gelo e troque pelo botão.

### 11/10/2026 — E6: acabamento da troca e critério editorial (1.62.1)

- **Pedido de Jean:**
  - a troca de versão sem o aviso sobreposto, com a página confirmando ("Em uso", o botão com a outra versão);
  - o critério editorial consolidado no roadmap e citado no CLAUDE.md;
  - um levantamento dos casos restantes, sem reescrever tudo;
  - e, no meio da entrega, cinco ajustes pontuais vistos no teste.
- **A troca:**
  - **O problema:** o aviso cobria a vila, a escolha virava eco na página e pedia um Continuar, e até esse Continuar
    o Grimório ficava sem o botão.
  - **Agora, na tela gráfica**, a troca é silenciosa (`WebUI.escolher`, meta `versao`): sem eco, sem página nova na
    vila e sem Continuar. A fogueira, que se redesenha, abre página nova como depois de qualquer escolha.
  - **A página do Grimório confirma:** as duas versões ficam sempre na mesma ordem, a marca "Em uso" muda de linha, a
    página vira a da versão em uso (nome, custo, dano) e o botão oferece a outra ("Usar Lança de Gelo").
  - **No modo texto,** a opção "Grimório: usar a …" e a linha "Em uso: …".
  - **A compra:** a confirmação também caía atrás da árvore e sumia. Agora o nó diz antes da compra que a Prisão entra
    em uso, e só o texto confirma depois.
- **Ajustes pontuais:**
  - **A represa:** a pista diz "o dono do moinho fez uma represa no riacho, acima da roda".
  - **O objetivo da capela:** era "onde o canal do moinho entra no brejo" e virou "no brejo, aonde o canal do moinho
    leva". A geografia é a das pistas: o canal entra na capela por um buraco no muro. A versão mais longa repetia a
    pista mais recente no Diário.
  - **A Vigília:** o objetivo fica só com a acusação. A promessa já está no Diário, atribuída a Caspar ("Caspar
    prometeu que, quando ela acabar…").
  - **Fonte Nova:**
    - a abertura dá o nome ("A vila a chamou de Fonte Nova");
    - a prova diz "a Fonte Nova";
    - as referências genéricas ("a fonte") ficam em minúsculas.
  - **O contrato no espólio:** o nome do contrato, o estado curto ("Concluído") e, embaixo, menor, "Recompensa ao
    chegar a qualquer vila". O pagamento é automático na chegada, então não há ação a destacar.
- **O critério editorial:** consolidado no 07 (seção "Critério editorial") e citado no CLAUDE.md.
  - As camadas são cena, alternativa, nota, resultado e confirmação.
  - Evitar: repetir entre camadas, narrar o clique, explicar o jogo à toa, antecipar.
  - Preservar: custos, testes, imunidades, indisponibilidade, fuga.
- **Levantamento:** 13 problemas claros e 7 escolhas de estilo, no 07 ("Levantamento da 1.62.1"). Nada implementado.
- **Cenários:**
  - `combate` ganhou `FEITO`: `FEITO=2` fecha o contrato na luta;
  - `capela` ganhou `PONTOS`: pontos de talento sobrando.
- **Verificações:**
  - testes, gabarito, pyflakes e fumaça;
  - no navegador, a 1500 e 1280 px:
    - a troca nos dois sentidos, na vila e na fogueira;
    - salvar, sair e carregar mantém a escolha;
    - a compra na árvore;
    - os textos na abertura, no rastreador e no Diário;
    - o espólio com o contrato concluído e em andamento;
  - o modo texto, com a compra e a troca nos dois sentidos.
- **Não mudou:** equilíbrio, regras da transformação, missões e recompensas.

### 11/10/2026 — Três textos da capela e a leitura do lodo (1.62.2)

- **Pedido de Jean:** três ajustes pontuais de texto e coerência, e um acréscimo ao critério editorial.
- **A descida até Ilse.** A lembrança de Vó Berta fica, porque é conhecimento que o personagem já tem, mais curta:
  "Vó Berta disse que era preciso soltá-la das pedras. As correntes ainda a prendem." Depois de Berta, só as correntes
  podem faltar. O caso improvável de faltar outra coisa continua com a lista.
- **O lodo.** "Nenhum feitiço de ninguém" contradizia a causa aprovada: o Sigilo rachado vaza a Fenda pelo corpo de
  Ilse, e a água leva isso à vila.
  - **O mago observa** no lodo a mesma "palavra apagada" da Fonte Nova, velha e fria, e nenhuma mão por trás dela. A
    hipótese vem marcada como leitura dele: "pelo que você lê, vem do fundo da capela, e a água o leva". Saiu "Isso a
    praça vai entender".
  - **As outras classes** só recolhem o frasco, como antes.
  - **No Diário,** o título "No lodo, magia velha do fundo da capela, que ninguém lançou". A lista da prova virou "O que
    pode mostrar à praça para defender que…".
  - **Na denúncia,** a febre na água vira fala do herói, e a prova forte do mago diz o que ele leu.
  - **Diante da fogueira do brejo,** o herói contrapõe "a água, não uma moça do brejo", e não "água, não feitiço".
  - A força da prova e o teste de denúncia não mudaram.
- **O rito.** "Ilse vacila à metade" virou "O canto de Ilse falha". O resto da cena e o funcionamento do rito ficam
  como estavam.
- **O critério editorial** (07) ganhou duas regras:
  - nada de condição interna disfarçada de narração;
  - evidência como evidência: o que se observa, o que se supõe e o que prova algo.

### 11/10/2026 — Diário, baús e a leitura do lodo (1.62.3)

- **Pedido de Jean:** ajustes de clareza vistos jogando a 1.62.2.
- **O Diário:**
  - "o lugar fica marcado no mapa" e "os lugares ficam marcados no mapa" deram lugar ao mesmo "!" do mapa, ao lado do
    nome do destino;
  - o "!" só aparece quando o mapa marca o lugar: o objetivo da missão com destino e o contrato em andamento. O
    contrato cumprido e a Vigília, sem lugar, ficam sem;
  - o selo diz o que é ("marcado no mapa") ao passar o mouse e para leitores de tela.
- **A acusação:** "Caspar acusa Yara de causar a febre."
- **Os baús:** o rótulo dos equipamentos perdeu o "a seguir, um por um". Fica a quantidade ("2 equipamentos"); cada um
  continua vindo na janela dele para comparar.
- **O lodo:**
  - o Mago: "Você reconhece no lodo a mesma magia antiga da Fonte Nova. Ela parece vir do fundo da capela e chegar à
    vila pela água.";
  - o Diário: "O lodo contém a mesma magia antiga encontrada na Fonte Nova.";
  - a prova forte na denúncia diz o mesmo, sem concluir que ninguém lançou aquilo.
- **Ilse:** "Não deixe os três cair nas mãos de quem não entende o que eles mantêm fechado."
- **Não mudou:** regras, prova, teste de denúncia e o funcionamento do Diário, do mapa e dos baús.

### 11/10/2026 — Odette, missões concluídas no Diário e "brejo" (1.62.4)

- **Pedido de Jean:**
  - o encontro com Odette: a morte dita com clareza, as falas conforme a ação, e o fluxo de "perguntar" registrado à
    parte;
  - as missões concluídas recolhidas no Diário;
  - outros textos parecidos, o "brejo" estranho e a "Fonte Nova".
- **Odette:**
  - "Perguntar quem ela é": ela diz o nome e que não dá mais para salvá-lo, e o homem morre diante dos dois;
  - a fala da oferta acompanha a ação: quem ajudou ouve "Você vai para onde está a dor"; quem segurou e falhou, "Você
    ficou até o fim"; quem só perguntou, "Você parou para perguntar. A maioria nem para.";
  - aprovação, custos, reputação, reações e desfechos ficam iguais;
  - o fluxo (perguntar fecha a chance de ajudar) está registrado no 07, sem mudar.
- **O Diário:**
  - as missões em andamento vêm primeiro;
  - o que uma concluída ainda espera (a herança de Vó Berta) fica à vista, fora da seção recolhida;
  - as concluídas ficam em "Concluídas (N)", recolhida por padrão;
  - aberta, a missão concluída mostra o desfecho, o que mudou e o histórico. Sem "Mais recente" repetindo o desfecho e
    sem os preparos antigos, que estão no histórico;
  - o modo texto segue a mesma ordem;
  - saves e progresso não mudam: a organização vem do estado que já existia.
- **Textos:**
  - na campanha, Caspar é chamado pelo nome na fogueira de Yara;
  - "a moça do brejo" e "na beira do brejo" saíram do narrador e do Diário;
  - "brejo" fica na voz de Caspar, na de Yara e na geografia da capela;
  - "Fonte Nova": as 41 ocorrências usam o nome do lugar, e as referências genéricas usam "a fonte". Nada a corrigir.
- **Verificações:**
  - testes e gabarito;
  - a fumaça, com a leitura do Diário ajustada à nova ordem;
  - no navegador, a 1500 e 1280 px, nos três estados: uma em andamento com a herança pendente, uma em andamento sem
    herança, e todas concluídas. Cada um também depois de salvar e carregar;
  - o modo texto, nos testes.

### 11/10/2026 — Odette: perguntar o nome volta às ações (1.62.5)

- **Pedido de Jean:** "Perguntar quem ela é" revela o nome e devolve as ações, para ainda dar para ajudar. A
  resposta dela precisa servir para um homem que ainda pode ser salvo.
- **Como ficou:**
  - Odette responde sem tirar as mãos da ferida: "Odette. Irmã Odette." e "O resto, depois. Ele ainda respira.";
  - as ações voltam sem a pergunta, então a apresentação não se repete;
  - perguntar não muda tempo, item, sorteio, reputação, aprovação nem o encontro;
  - bandagem, oração, revistar e seguir têm os mesmos custos, testes e efeitos, e a fala da oferta segue a ação final
    e o resultado;
  - só perguntar já não leva à oferta;
  - o narrador só usa o nome depois que ela o diz ("A mulher se levanta" ao revistar sem perguntar).
- **Verificado:**
  - testes de perguntar e depois bandagem, oração (os dois resultados), seguir e revistar;
  - o estado intacto depois da pergunta, e o mesmo sorteio e o mesmo resultado perguntando antes ou não;
  - a pergunta não reaparece;
  - o modo texto;
  - no navegador, a 1500 e 1280 px. A fumaça confere a volta das ações.
- **Gabarito:** uma partida mudou (guerreiro, semente 42, modo texto). O robô revista o moribundo sem perguntar, e o
  narrador diz "A mulher se levanta" em vez de "Odette se levanta". Nada mais mudou.

### 11/10/2026 — Saque do Vale medido e a primeira entrega da E7 especificada

- **Pedido de Jean:**
  - diagnosticar a impressão de que os baús dão consumíveis demais, sem mudar distribuição, frequência, economia ou
    recompensas;
  - especificar a primeira entrega da E7, sem implementar.
- **O que existe agora:**
  - `tests/saque_vale.py`, uma régua: um robô joga o Vale inteiro e conta baús, suprimentos, equipamento, vendas e
    ouro. O roteiro está no topo do arquivo. Não muda o jogo;
  - o [16](16-E7-ITEM-E-LOOT.md), com o diagnóstico, duas propostas e a especificação.
- **Saque** (480 percursos, 136 completos):
  - 6,4 baús por Vale. Metade vem de inimigos com nome, que sempre deixam baú: alvos de contrato, nêmesis, líderes;
  - metade dos suprimentos achados sai de baús;
  - poções e tônicos se gastam; antídoto, unguento e bomba se acumulam;
  - no fim, a bolsa vale mais que o ouro na mão, e suprimento não se vende;
  - todo equipamento é da classe do herói.
- **Propostas, nenhuma aplicada:**
  - um suprimento por baú (recomendada);
  - se não bastar, o situacional repetido vira ouro.
- **E7:** recomendado o Broquel do Vigia. É um escudo único do Guerreiro: com o escudo erguido, devolve cada golpe
  corpo a corpo que acerta o herói (Revide, 30% do Ataque).
  - Vem do esqueleto de guarda do ossuário, uma vez, fora do sorteio.
  - Num save adiantado, o ferreiro do Vau o oferece uma vez.
  - Um protótipo descartável, só na memória de um script, serviu para escolher o número de partida.
- **Registrado, sem proposta:** o começo do Vale derruba o robô (fome nos níveis 1 e 2), em especial o Mago. Fica
  para a E9.
- **Decisões de Jean:** seção 6 do 16.
- **Verificado:** testes, gabarito (sem mudança), pyflakes, fumaça.

### 11/10/2026 — Um suprimento por baú na campanha (1.62.6)

- **Pedido de Jean:**
  - aplicar a P1 do [16](16-E7-ITEM-E-LOOT.md) só na campanha, mantendo ouro, chance de equipamento, frequência de
    baús e recompensas fixas;
  - medir antes e depois, com os percursos interrompidos na avaliação do começo.
- **Como ficou:**
  - na campanha, o baú dá um suprimento (`BAU_SUPRIMENTOS_CAMPANHA`);
  - o mundo gerado continua com um ou dois, com o mesmo sorteio.
- **Medido** (`tests.saque_vale`, 480 percursos de cada lado; tabelas no 16, seção 3.1):
  - nos completos, os suprimentos de baú caem de 9,7 para 6,3 por Vale;
  - poções no fim: de 3,0 para 2,4, depois de gastar 4,9;
  - situacionais no fim: de 5,4 para 4,3;
  - o começo não muda: quem para viu menos de meio baú e para sem poção, com fome e quase sem ouro. Isso fica
    registrado para a E9, sem ajuste.
- **Gabarito:** sem mudança (as partidas dele são do mundo gerado).
- **Régua:** a saída do `tests.saque_vale` ganhou a tabela do começo do jogo (todos os percursos, do que param, nível,
  bolsa e ouro ao parar, etapa alcançada).
- **Falta Jean jogar.**

### 11/10/2026 — Broquel do Vigia, a primeira entrega da E7 (1.63.0)

- **Pedido de Jean:**
  - implementar o Broquel do Vigia com a aquisição no ossuário e a oferta única do ferreiro aos saves antigos;
  - Revide de 30% como valor de partida;
  - o Contra-ataque com prioridade;
  - validar decisões e abuso em lutas inteiras.
- **Como ficou** (no [16](16-E7-ITEM-E-LOOT.md), seções 5.1 e 5.2):
  - **o Revide:** com o escudo erguido, cada golpe corpo a corpo que acerta o herói volta a quem bateu, com 30% do
    Ataque;
  - **o Contra-ataque vem antes:** se sair (mesmo esquivado), ocupa a resposta. Sem o Broquel, o talento é o de
    antes;
  - **a aquisição:** o Guerreiro recebe o broquel no ossuário, uma vez, fora do sorteio. Num save antigo que já
    venceu a sala, a forja do Vau o oferece uma vez. A marca impede que volte, guardado, deixado ou vendido;
  - **a apresentação:**
    - a regra no cartão;
    - "▲ Revide" ou "▼ sem Revide" na comparação;
    - a linha na página do Erguer Escudo, no Grimório;
    - o nome "Revide" sobre a carta do herói, a cada resposta.
- **Medido** (`python -m tests.broquel`, seção 5.3):
  - **contra grupos corpo a corpo:** erguer o escudo na abertura ou manter a guarda corta de 30% a 60% da vida
    perdida. Com o mesmo escudo sem o efeito, a guarda é pior;
  - **onde atacar continua melhor:** inimigo único, conjuradores e Ilse; a Égide muitas vezes empata só atacando;
  - **com Muralha (nível 6),** a guarda fica boa com ou sem o Revide; o Revide dá velocidade;
  - **renovar em todo turno** é sempre pior, e sem atacar a luta não termina contra quem ataca de longe. Isso
    acontece com ou sem o efeito;
  - nenhum abuso, e nenhum número mudou.
- **Verificado:**
  - `tests/test_broquel.py` (17 testes);
  - os testes de missão;
  - a fumaça com o cenário novo, a 1500 e 1280 px;
  - o modo texto;
  - gabarito, `tests.equilibrio --spec paladino --spec berserker` e `tests.replay` idênticos antes e depois.
- **Para Jean jogar:** `python -m tests.navegador.cenarios broquel` (escudo e ataque, com e sem o Revide) e `muralha`
  (Muralha com Contra-ataque).
- **Falta:**
  - a validação de Jean jogando;
  - os exemplos da E7 para Arqueiro e Mago, que não foram começados.

### 11/10/2026 — Direção depois da E7: o Vale como primeiro capítulo (planejamento)

- **Pedido de Jean:** um adendo de planejamento, sem ampliar a implementação, depois da primeira entrega da E7.
- **Decidido:**
  - **o Vale do Turvo é o primeiro capítulo completo,** para validação, com o conflito local resolvido e um
    encerramento reconhecível. Isso não define que o jogo final terá só essa região;
  - **depois da primeira entrega da E7, vem a avaliação integrada do Vale,** que antecipa o trabalho pertinente da
    E9;
  - **a E8 (raças e origens) fica adiada** explicitamente;
  - **a campanha maior continua como direção.** O esboço geral fica; as próximas regiões dependem da avaliação do
    Vale e não são obrigação anterior à primeira versão de teste;
  - **o texto claro e concreto é o padrão** (critério editorial no 07, linha nova no CLAUDE.md):
    - metáfora e frase de efeito só quando acrescentam algo compreensível;
    - nada de esconder informação importante em linguagem enigmática, sem eliminar a expressão literária;
    - diálogos conforme o personagem, o contexto e a ação efetiva.
- **Em aberto:**
  - **a duração.** Precisa de medida com jogadores novos: tempo total, leitura, combate, exploração, conteúdo
    opcional, dificuldades de navegação. Dias do jogo, partidas do robô e percursos de quem conhece a solução não
    valem como duração de uma primeira partida;
  - **como medir.** Nada foi implementado;
  - não se acrescenta conteúdo só para alongar.
- **Documentos:**
  - [01](01-VISAO.md), "Direção";
  - [07](07-ETAPAS.md): "Ordem atual", E8, E9, E10 e o critério editorial;
  - [10](10-DECISOES.md): tabela e registro;
  - [12](12-E1-CAMPANHA.md), o tamanho;
  - este quadro de estado;
  - CLAUDE.md.
- **Não mudou:**
  - nada no jogo;
  - nenhuma validação jogando foi marcada como feita: as entregas da E3 à E7 seguem esperando Jean jogar.

### 11/10/2026 — Avaliação integrada do Vale, primeira entrega da E9 (diagnóstico)

- **Pedido de Jean:**
  - avaliar o Vale como capítulo: o percurso completo e o encerramento, o começo (níveis 1 e 2), o ritmo, a
    progressão e o saque;
  - preparar a validação humana: um roteiro para Jean e uma ficha para jogadores novos;
  - não mudar regras, números ou recompensas, nem começar outros únicos ou regiões.
- **O que existe agora:**
  - o [17](17-E9-VALIDACAO-DO-VALE.md), com o diagnóstico, os achados por prioridade, as propostas, o roteiro de
    Jean e a ficha;
  - a régua do Vale (`tests/saque_vale.py`) com três opções novas: `--estrategia` (o começo com outras regras de
    compra, recrutamento e contrato), o roteiro `nivel6` e `--economia` (a conta de uma luta do começo). Cada
    percurso agora traz a trajetória, as pausas, as escolhas e os encontros.
- **Achados, por prioridade:**
  - **perda de progresso:** a fome e a infecção matam na campanha, e o save automático fica na véspera. O resgate
    come dois dias de provisões. Reproduzido; 162 de 540 percursos morreram sem sair de "sem comida e sem ouro";
  - **clareza:** o capítulo não tem marco de fim; o custo do companheiro (1 provisão por dia) não aparece na escolha;
  - **ritmo e equilíbrio:** nos níveis 1 e 2, lutar dá prejuízo, e o herói inteiro perde de 10% a 22% das lutas no
    Charco. Persiste com as estratégias simples, mas é para confirmar jogando antes de mexer em número. O Mago fica
    bem atrás. Eventos repetidos: 29% num Vale direto, cerca de 50% para quem explora muito;
  - **funciona:** o percurso fecha nas três classes, nos dois caminhos de Ilse e nas três posturas; salvar e
    carregar saiu idêntico em 220 pontos de 12 percursos; a derrota para Ilse não perde a missão.
- **Propostas, nenhuma aplicada:**
  - fome e infecção levam ao resgate na campanha;
  - o resgate do Vau não come a bolsa;
  - uma cena curta de fim de capítulo no Vau, com as linhas que já existem;
  - a nota "Come 1 provisão por dia" no recrutamento.
- **Decisões de Jean:** seção 10 do 17.
- **Verificado:** testes, gabarito (sem mudança), pyflakes, fumaça; as opções novas da régua rodadas.
- **Não mudou:** nada no jogo (1.63.0). A E9 **não** está concluída: falta Jean jogar e os jogadores novos.

### 11/10/2026 — Recuperação, custo da comitiva e fim do capítulo (E9, 1.64.0)

- **Pedido de Jean:**
  - incorporar a partida dele (mago, 1.63.0) à avaliação, separando o registro da impressão;
  - na campanha com resgate, fome e infecção levam ao resgate; os dois dias alimentam herói e comitiva sem gastar a
    bolsa e encerram a emergência; o custo do resgate continua;
  - a nota do custo do companheiro na opção de aceitar;
  - uma cena curta de fim de capítulo no Vau, uma vez;
  - preservar a dificuldade: nada de dano, vida, habilidades, preços, recompensas, regeneração ou recursos iniciais.
- **A partida de Jean** ([17](17-E9-VALIDACAO-DO-VALE.md), seção 13): confirmados no registro o nível 3 no dia 5, as
  dez lutas (7 vitórias, 2 fugas, 1 derrota), o ossuário com 36/58 de vida e 19/42 de mana, Ilse no nível 3 com 38/58,
  e 94 de ouro depois do resgate. A vida que restou a Ilse não está no registro.
- **Como ficou** (seção 14):
  - `Finais.cair_sem_luta` e `Derrota.causa`: a fome e a infecção viram queda na campanha com resgate; hardcore e
    mundo gerado como eram;
  - `Jogo.resgate_campanha`: Marta ou Pita, os dois dias com refeição, fome zerada, infecção tratada, feridas abertas
    enfaixadas, um quadro de amanhecer só, nenhuma queda durante o tratamento;
  - o prólogo e a escolha do modo dizem que fome e infecção também levam ao resgate;
  - `comitiva.oferecer_vaga`: a nota "Consome 1 provisão por dia.";
  - `rpg/capitulo.py`: a cena "O Vale do Turvo · fim do primeiro capítulo", e a linha "Primeiro capítulo concluído"
    no rastreador e no Diário; saves já concluídos recebem a cena na próxima visita ao Vau.
- **Medido** (seção 15): nenhum fim de jogo nos 540 percursos (antes, 303); completos de 140 para 159; mais percursos
  chegam à capela e ao fundo. Mas dos 303 salvos só 39 completam: o resto gira em quedas de combate até o dia 45 do
  robô. Morte evitada não é progresso: a economia do começo não foi resolvida por esta entrega.
- **Caso concreto que continua** (seção 16): o arqueiro sem ouro e sem flechas, lutando de adaga por semanas. Proposta
  registrada, nada aplicado; esperar a partida de um arqueiro.
- **Verificado:** `tests/test_recuperacao.py` e `tests/test_capitulo.py` novos; testes antigos de Caspar e Yara
  ajustados para o fim do capítulo; fumaça com o cenário `resgate` e o fim do capítulo, a 1500 e 1280 px; gabarito
  mudou só na nota do recrutamento (conferido e atualizado); pyflakes.
- **Para Jean:** o roteiro curto da seção 16 do 17.
- **Falta:** os jogadores novos; a E9 continua aberta.

### 11/10/2026 — Interface, retorno visual e texto (E9, 1.65.0)

- **Pedido de Jean:** os problemas que ele encontrou jogando, sem mexer em equilíbrio, economia, recompensa ou
  dificuldade; entregas pequenas, commits separados; a investigação dos toques que não respondiam.
- **Feito** ([17](17-E9-VALIDACAO-DO-VALE.md), seção 17):
  - o mercador ambulante sem ouro (compra à vista e indisponível, despedida);
  - a opção indisponível riscada em vermelho, com o motivo curto (pedido no meio);
  - os toques: o Continuar das cenas apagado enquanto a proteção segura; os toques do acampamento guardados até o
    menu voltar;
  - o menu inicial com teclado e foco visível; o nome longo na ficha; o selo "com fome" na barra; a árvore de
    talentos com títulos curtos;
  - os balões mais curtos, a fala da Odette, o som do servo, o espólio mais ágil;
  - "fonte nova" como descrição; "pântano" e "Charco dos Juncos" no lugar de "brejo";
  - pedidos no meio: a teia que voa e diz "não pegou"; a bolsa que pulsa e diz o que trata; a bandagem que avisa que
    só cura; o mural que pisca para quem nunca o abriu.
- **Não reproduzido:** os rótulos dos prédios que subiram (registrado com a hipótese, sem mudança).
- **A partida de Jean:** o complemento até o dia 19 registrado na seção 13 do 17.
- **Verificado:** testes, gabarito (cada diferença conferida), pyflakes, fumaça, telas a 1500 e 1280 px.
- **Falta:** Jean conferir (roteiro na seção 17 do 17) e os jogadores novos. A E9 continua aberta.

### 11/10/2026 — Os três pontos que faltaram (E9, 1.65.1)

- **Pedido de Jean:** completar a mensagem cortada da 1.65.0, sem mexer em equilíbrio, economia, recompensa ou
  dificuldade.
- **Feito** ([17](17-E9-VALIDACAO-DO-VALE.md), seção 18):
  - o Mago sente magia na água da fonte nova e a reconhece, mais forte, no canal e junto à capela, sem a causa;
  - quem não conhece a Yara não ouve o nome: Caspar acusa "uma moça no Charco dos Juncos", o Diário diz "Caspar acusa
    uma mulher de causar a febre." até ela se apresentar; a praça, a opção de denunciar e o Diário também. O objetivo
    de uma etapa pode ser uma função do jogo (`missoes.objetivo`);
  - duas Lanças de Gelo nos turnos da iniciativa: a regra está certa (não soma; o Firme entra depois da ação perdida;
    nunca duas seguidas) e ficou; a segunda Lança agora diz "já congelado" em vez de anunciar um congelamento novo.
- **Verificado:** testes, gabarito sem mudança, pyflakes, fumaça, telas da luta a 1500 e 1280 px; cenário novo `gelo`.
- **Falta:** Jean conferir (roteiro na seção 18 do 17) e os jogadores novos. A E9 continua aberta.

### 12/10/2026 — A partida da Quibia, duas correções e a abertura guiada especificada (E9, 1.65.2 e 1.65.3)

- **Pedido de Jean:** ler a partida da Quibia (sem mexer nos arquivos), corrigir os contratos depois do resgate e o
  destaque dos baús abertos juntos, e especificar a abertura guiada antes de implementar.
- **Feito:**
  - a Quibia em observações, fatos e hipóteses ([17](17-E9-VALIDACAO-DO-VALE.md), seção 19.1);
  - 1.65.2: os dois resgates punham o herói na vila sem passar por `chegar`, a única que pagava contratos; agora o
    menu da vila paga os cumpridos e não pagos (campanha e mundo gerado brando, saves antigos), uma vez, depois da
    cobrança do resgate. Gabarito: só guerreiro-42 mudou (o mesmo caso);
  - 1.65.3: a pilha de baús e o ×N grande no quadro; um baú fica como era;
  - [18](18-E9-ABERTURA-GUIADA.md): a abertura guiada (caixa "Mostrar tutorial", a despensa da taverna, Morel
    previsível, os quadros C1–C4 e V1–V5, E1, T1, N1, mouse e teclado, pular, fugir, perder, salvar e carregar, a
    primeira implementação mínima e os critérios do teste) e a investigação da noite (seção 8: o que avisa, o que não
    avisa ou avisa errado; encontros sem mudança).
- **Verificado:** testes (novos: os contratos depois do resgate), gabarito (a diferença conferida), pyflakes, fumaça,
  telas a 1500 e 1280 px.
- **Falta:** Jean revisar o 18 (decisões na seção 10 dele) antes da implementação; Jean conferir (roteiro na seção
  19.4 do 17); os jogadores novos. A E9 continua aberta.

### 12/10/2026 — Riscos da noite e a primeira parte da abertura guiada (E9, 1.65.4 e 1.66.0)

- **Pedido de Jean:** aprovou a especificação com ajustes (o XP dos ratos e a caneca como uma vez o serviço de bebida,
  taverneiro sem nome, Ajuda no topo e F1); pediu antes a correção da comunicação da noite e da tocha, em commit
  separado; e só o escopo mínimo da abertura.
- **Feito:**
  - 1.65.4: as notas da capela (tocha, emboscada certa sem luz, noite), o nível-base com o modificador da noite ao lado,
    o consumo de tocha no painel, a dica da noite corrigida ([18](18-E9-ABERTURA-GUIADA.md), seção 8);
  - o 18 ajustado antes de implementar (o Atacar pelas regras da classe e as flechas do Arqueiro; as provisões de
    todo amanhecer, comitiva e refeições; o que dormir na taverna devolve; C1–C4 curtos; a comparação com e sem
    tutorial; os critérios humanos);
  - 1.66.0: `rpg/abertura.py` e `app/orientacao.js`: a caixa, a despensa (dois ratos da despensa), a caneca, Morel
    pelo evento que existe e só se ele nunca apareceu, C1–C4, V1, dispensar e a Ajuda.
- **Medido:** a despensa em 6000 lutas simuladas (três classes, quatro formas de jogar): nenhuma derrota.
- **Verificado:** testes, gabarito (só texto e uma linha de estado; jogo idêntico), pyflakes, fumaça, telas a 1500 e
  1280 px com mouse e teclado.
- **Falta:** Jean conferir; um teste com uma pessoa nova (seção 11 do 18); a segunda parte da abertura. A E9 continua
  aberta.

### 12/10/2026 — Acabamento da abertura guiada e os riscos da capela (E9, 1.66.1 e 1.66.2)

- **Pedido de Jean:** antes da segunda parte do tutorial, o acabamento da 1.66.0, com regras, custos, recompensas,
  sorteio e dificuldade iguais: destaque mais fino e sem piscar; quadros parados na luta, fora das cartas e do texto;
  C4 depois do golpe, em linhas, com "Entendi" e "Encerrar tutorial"; a cena depois da despensa esperando o Continuar,
  com a fala do mural; os riscos da capela em indicadores com ícone.
- **Feito:**
  - 1.66.1: `sobrevivencia.riscos_sala` (tocha, sem luz, noite; na guardiã só o dano), os indicadores na escolha
    (`escolhas.js`), a interface de texto com as mesmas linhas, o topo sem quebrar a 1280 px;
  - 1.66.2: `app/orientacao.js` refeito (contorno com brilho lento, faixa reservada abaixo da arena ou acima das
    cartas, posição só quando o passo ou a tela muda, C2 ao lado da janelinha, C4 com "Entendi" e foco nele,
    "Encerrar tutorial"); o C4 em partes prontas do motor (`abertura._c4`); a cena da taverna com `continuar`.
- **Verificado:** testes, gabarito sem diferença nas duas, pyflakes, fumaça; telas nas três classes, mouse e teclado,
  1500 e 1280 px (golpes, C4, habilidade que acaba a luta, encerrar e religar, a cena, a capela de dia e de noite com
  e sem tocha, salvar e carregar).
- **Falta:** Jean conferir; a segunda parte da abertura; o teste com uma pessoa nova. A E9 continua aberta.

### 12/10/2026 — Ajustes pontuais de apresentação (E9, 1.66.3)

- **Pedido de Jean:** fechar os ajustes da primeira parte antes da próxima implementação e dos testes humanos: os
  ícones do C4, o texto e a posição do V1, a legenda "clique: contratos", o rodapé da fogueira e a fome fora da barra.
- **Feito:** o C4 com o valor na linha do texto; o V1 numa faixa abaixo do cenário, com o novo texto e um destaque só;
  o balão do Mural sem legenda; a fogueira com instrução, contador, quem vai, quem fica e a nota do acampamento (também
  no menu, junto da decisão); `sobrevivencia.condicoes` e a linha de condições do topo; o cenário `fogueira`.
- **Verificado:** testes, gabarito (só campos novos da tela; jogo idêntico, examinado antes de atualizar), pyflakes,
  fumaça; telas a 1500 e 1280 px, mouse e teclado (seção 14 do 18).
- **Falta:** Jean conferir; a segunda parte da abertura; o teste com uma pessoa nova. A E9 continua aberta.

### 12/10/2026 — Últimos detalhes e a segunda parte da abertura guiada (E9, 1.66.4 e 1.67.0)

- **Pedido de Jean:** dois ajustes pequenos (a fome em etiqueta; a nota do acampamento só junto da decisão; as cores
  dos avisos do lugar), entregues à parte; depois V2–V5, E1, T1 e N1, uma por vez, quando fazem sentido, sem passeio
  obrigatório pela tela.
- **Feito:**
  - 1.66.4: a etiqueta da fome (a grave acende mais), o rodapé da fogueira sem a nota, o `tipo` dos avisos do lugar;
  - 1.67.0: `abertura.proxima` (a ordem: o que a tela pede, depois recuperar e preparar antes de novidades), os
    ganchos (menus da vila e do lugar, viagem, item achado, talentos, comitiva, caneca), o motivo de explorar pelo
    taverneiro ou por Morel, o "Entendi" das informativas (`/orientacao` com `visto:ID`), os quadros sobre a paisagem
    fora da vila e nas faixas na vila, o cenário `tutorial`.
- **Verificado:** testes (inclusive o mesmo jogo com e sem tutorial nas três classes), gabarito (1.66.4: só campos
  novos, examinado; 1.67.0: sem diferença), pyflakes, fumaça; telas a 1500 e 1280 px, mouse e teclado.
- **Falta:** Jean conferir; o teste com uma pessoa nova (seção 11 do 18). A E9 continua aberta.

### 12/10/2026 — Interação, posicionamento e feedback (E9, 1.67.1)

- **Pedido de Jean:** duas entregas separadas; esta é a primeira (correções de interação e apresentação).
- **Feito:** o alvo da orientação trazido à vista (rolagem mínima, uma vez) e o quadro parado na faixa; o V4 no botão
  Comitiva; o texto da noite; "roupas chamuscadas" e o uivo dos lobos; a fuga com faixa, carta saindo e som (lance
  `fuga_heroi`); as teclas da doca que abrem e fecham; adiantar e Continuar separados pelo gesto, sem guarda de tempo.
- **Verificado:** testes, gabarito (só o lance da fuga e os dois textos; jogo idêntico), pyflakes, fumaça (com as
  conferências de adiantar reescritas para a regra nova), telas a 1500 e 1280 px.
- **Falta:** a segunda entrega (templo, contrato, baú, selos, adiantar a apresentação); Jean conferir; jogadores
  novos. A E9 continua aberta.

### 12/10/2026 — Os ciclos básicos da abertura guiada (E9, 1.68.0)

- **Pedido de Jean:** a segunda entrega: o primeiro atendimento grátis no templo (a única mudança de economia
  autorizada), um contrato do começo ao pagamento, o primeiro baú, os selos das cartas e adiantar a apresentação.
- **Feito:** `Jogo.templo_gratis`; K1–K4, B1, SF/S-/S+ e A1 em `abertura.py`, pelos estados reais (contratos, bolsa,
  efeitos), com os ganchos no Mural, no pagamento, na chegada, no baú e no turno do herói; as âncoras novas na tela.
- **Verificado:** testes, gabarito sem diferença, pyflakes, fumaça (um cenário dos ciclos), telas a 1500 e 1280 px.
- **Falta:** Jean conferir; jogadores novos. A E9 continua aberta.

### 12/10/2026 — Revisão pontual da abertura guiada (E9, 1.68.1)

- **Pedido de Jean:** textos do tutorial, posicionamento dos quadros e o erro de derrota no cenário de teste, sem
  ampliar o tutorial nem mexer em combate, economia, recompensas ou sorteio.
- **Feito:** K1, K2, K4 e B1 curtos e ligados à ação; os efeitos como ícones (nome do catálogo, `titulo`, e o efeito
  de agora; a duração uma vez); adiantar em três (A0 revelar o texto, A1 a velocidade, AL a animação da luta); o
  quadro encostado no controle nas colunas, no topo e no Mural, com a seta nele e acompanhando a rolagem; a haste até o
  ícone na luta e o quadro ao lado da janelinha de Habilidades; o B1 só quando o baú abre; o N1 nos riscos do lugar;
  `lutar()` nos cenários (a derrota vai ao resgate).
- **Verificado:** testes, gabarito (só o campo `apresentacao` e o texto da Iniciativa na carta; examinado), pyflakes,
  fumaça completa, telas a 1500 e 1280 px (com rolagem e Habilidades aberta), vitória, fuga e derrota na luta
  preparada.
- **Falta:** Jean conferir; jogadores novos. A E9 continua aberta.

### 12/10/2026 — Três correções da abertura guiada (E9, 1.68.2)

- **Pedido de Jean:** o quadro do contrato que só aparecia depois de Passear, o Entendi no quadro da animação e um
  sinal claro da derrota, sem ampliar o tutorial nem mexer em regras.
- **Feito:** o K2 primeiro na fila do menu (reproduzido: o A1 pendente vinha antes); o AL com Entendi, foco e sem
  sumir antes de ser lido; `celebrar("derrota")` em `Combate.fim` e a sequência na tela (carta, pulso, faixa, som,
  cenário escuro até o amanhecer do resgate ou o próximo menu); o cenário `tutorial` com HARDCORE, PENA e PROTECAO.
- **Verificado:** testes, gabarito (só a linha nova da derrota; examinado), pyflakes, fumaça completa, telas a 1500 e
  1280 px (resgate, hardcore, Pena, mendigo, vitória, fuga, tutorial desligado, recarregar).
- **Falta:** Jean conferir; jogadores novos. A E9 continua aberta.

### 13/10/2026 — Ferimentos, descanso e o fim da derrota (E9, 1.69.0)

- **Pedido de Jean:** concluir a transição da derrota e apresentar ferimentos, tratamentos e descanso; a mudança de
  economia autorizada é o primeiro tratamento grátis na curandeira.
- **Feito:** a cena do resgate (ou da morte) abre direto depois da queda (`WebUI.depois_da_queda`), com a queda em
  ~2,2 s; F1–F4 e D1–D3 em `abertura.py`; `abertura.curandeira_gratis` no `Servicos.curandeiro`; a dica da bandagem diz
  só a ferida que ela trata; a haste da seta nos prédios e nas opções; o cenário `tutorial` com FERIMENTOS, BANDAGENS e FOME.
- **Verificado:** testes, gabarito (só campos novos; examinado), pyflakes, fumaça completa, telas a 1500 e 1280 px.
- **Falta:** Jean conferir; jogadores novos. A E9 continua aberta.

### 13/10/2026 — Acabamento dos textos e da apresentação (E9, 1.69.1)

- **Pedido de Jean:** acabar os textos da 1.69.0 sem novas etapas nem mudança de regra, preço, grátis ou sorteio.
- **Feito:** F4 e D1 só com a ação; o V2 do Templo só com o Templo; o cartão Dormir e o D3 em linhas curtas
  (`Tempo.linhas_descanso`, a conta de `Tempo.descansar`); "nenhuma provisão é consumida" no lugar do ensopado; a nota
  de ferimentos corrigida (com comida, saram); o quadro da fogueira à esquerda do botão, sem cobrir a comitiva.
- **Verificado:** testes, gabarito (só o meta do Dormir; examinado), pyflakes, fumaça completa, telas a 1500 e 1280 px.
- **Falta:** Jean conferir; jogadores novos. A E9 continua aberta.

### 13/10/2026 — A bandagem só enfaixa (E9, 1.70.0)

- **Pedido de Jean:** tirar a vida da bandagem e restringi-la a enfaixar ferida aberta (mudança de mecânica
  autorizada); o primeiro ferimento sem "fica na ficha..."; as flechas recolhidas no espólio.
- **Feito:**
  - a bandagem enfaixa uma ferida aberta do herói por uso (`sobrevivencia.ferida_para_bandagem`), sem vida, sem
    sangramento, sem comitiva nem animal; apagada e com motivo quando não há ferida;
  - os textos, a Ajuda e o README;
  - o F1 em três linhas;
  - as flechas recolhidas como item do espólio (na tela).
- **Verificado:** testes (`test_bandagem.py` novo), gabarito (24 partidas divergem no uso da bandagem; examinado),
  equilíbrio e replay iguais, saque_vale medido, pyflakes, fumaça completa, telas a 1500 e 1280 px.
- **Falta:** Jean conferir; jogadores novos. A E9 continua aberta.

### 13/10/2026 — O soldo de Morel no resgate (E9, 1.70.1)

- **Achado de Jean:** caído no dia de pagar Morel, ele cobrava antes de o herói ser achado e levado à casa de Marta.
- **Feito:** reproduzido em teste; nos dias do resgate, a fala da comitiva ao amanhecer (fome, soldo) espera o herói
  acordar e perder o ouro do resgate (`Jogo.amanhecer_adiado`, `comitiva.soldo_devido`).
- **Verificado:** testes, gabarito igual sem atualizar, pyflakes, fumaça completa, tela a 1500 e 1280 px.
- **Falta:** Jean conferir. A E9 continua aberta.

### 13/10/2026 — Relato da partida de Sombra e o D2 (E9, 1.70.2)

- **Relato de Jean:** uma partida completa de arqueiro Sombra, terminada com tranquilidade (registro em
  `tests/runs/ze_do_lanca_sombra.jsonl`; 17, seção 32). É relato humano, não validação de jogadores novos.
- **Feito:** a rolagem para a opção destacada traz o menu inteiro (a arte se recolhe antes); o quadro espera a opção
  voltar à vista se a pessoa rolar para longe; o contorno fica cortado pela página (18, seção 23).
- **Verificado:** testes, gabarito, pyflakes, fumaça completa, tela em 1280/1500 × 800/950/700, com e sem comitiva,
  de dia e à noite.
- **Falta:** Jean conferir; jogadores novos. A E9 continua aberta.

### 13/10/2026 — O mercado com abas e a banca (1.71.0)

- **Pedido de Jean:** comprar, procurar equipamento e vender sem percorrer a página; a banca e o comerciante no estilo
  das paisagens, como um interior de perto.
- **Feito:** três abas (Suprimentos, Equipamentos, Vender) só da tela; só a lista rola; o motor manda o motivo de cada
  coisa que não se compra e separa "você tem" de "à venda"; a banca em pixel art com o mercador na bancada; o
  `Gesto` protege os cartões do mercado. Detalhe em [19](19-MERCADO.md).
- **Verificado:** testes (`test_mercado.py` novo), gabarito (só os campos novos do painel; examinado), pyflakes,
  fumaça completa (`cenarioMercado` novo), telas a 1500 e 1280 px, com altura reduzida e movimento reduzido.
- **Falta:** Jean conferir.

### 13/10/2026 — A primeira cena interativa: o ossuário e o sarilho (1.72.0)

- **Pedido de Jean:** começar a representação visual da campanha pela capela: o ossuário, com o sarilho clicável que
  enquadra o mecanismo e abre as alternativas de sempre; o motor resolve, a cena mostra o resultado.
- **Feito:** a sala desenhada na página da capela (depois do ossuário visto); o sarilho como ponto (mouse, teclado,
  nome sempre à vista) que faz a mesma ação do menu; a aproximação; a corrente que só desce depois de o preparo ser
  gravado, inclusive depois da luta; recarga e save sem repetir nada. Detalhe em [20](20-CENA-INTERATIVA-OSSUARIO.md).
- **Verificado:** testes (`test_cena_ossuario.py` novo), gabarito idêntico, pyflakes, fumaça completa
  (`cenarioSarilho` e `cenarioGuardia` ampliados), telas a 1500 e 1280 px com altura reduzida: classe, à mão, fuga,
  derrota, recarga, salvar e carregar, movimento reduzido.
- **Falta:** Jean conferir.

### 13/10/2026 — Acabamento do mercado (1.73.0)

- **Pedido de Jean:** com as abas aprovadas, refinar a banca e o mercador, a linha das quantidades e o cartão
  esgotado, sem mexer em preço, estoque, limite, reposição ou sorteio.
- **Feito:**
  - a banca mais aberta (parede do lado com janela, ponta do balcão, tampo com profundidade, lousa) e um mercador
    reconhecível (chapéu com fita, lenço, barba, avental, a mão apoiada no balcão, a luz da lamparina de um lado);
  - "Na bolsa: N · Estoque: N" (com "17/30" onde há capacidade);
  - "Esgotado" no cartão, com a reposição na dica, que no mercado também abre pelo foco do teclado.
  - Detalhe em [19](19-MERCADO.md), seção "Acabamento".
- **Verificado:** testes, gabarito (só o painel do mercado; examinado), pyflakes, fumaça completa, telas a 1500 e
  1280 px com altura reduzida e movimento reduzido.
- **Falta:** Jean conferir.

### 13/10/2026 — O mercado em faixa única e a vendinha do Vale (1.74.0)

- **Pedido de Jean:** a arte horizontal em todas as larguras, e uma loja que pertença ao Vale: grupos de mercadorias
  do jogo, com respiro, e um comerciante de roupa de trabalho rústica. Só composição e ambientação.
- **Feito:**
  - a faixa em cima da tela do mercado, em qualquer largura (96 px, ou 80 com a janela baixa, pixel 2×), e a lista com
    a largura toda;
  - a parede em vãos com grupos reconhecíveis (curativos, provisões, gibão e broquel, arco e aljava, tochas, cestos,
    ferramentas, caixotes e barril), porta, janela, dia e noite;
  - o comerciante mais velho, de túnica de lã, capuz caído, avental de couro gasto, cinto com bolsa e chaves;
  - a animação que não recomeça a cada compra.
  - Detalhe em [19](19-MERCADO.md).
- **Verificado:** testes, gabarito idêntico, pyflakes, fumaça completa, telas de 1100 a 1920 px, altura reduzida, dia,
  noite, movimento reduzido.
- **Falta:** Jean conferir.

### 13/10/2026 — Quatro ajustes no mercado (1.75.0)

- **Pedido de Jean:** tirar os dois tufos verdes sobre os frascos; a luz da janela pelos quatro períodos; a mão
  apoiada do comerciante; a aba Vender como a grade da mochila, com "Recomprar" só depois de vender.
- **Feito:**
  - os tufos saíram;
  - a janela, a porta e a lamparina seguem o período do jogo (manhã, tarde, anoitecer, noite);
  - a mão desce do cotovelo e se espalma no tampo;
  - Vender é a grade da mochila com "Mochila N/12" e o preço no canto de cada item, e a seção "Recomprar" separada
    só aparece depois da primeira venda.
  - Detalhe em [19](19-MERCADO.md).
- **Verificado:** testes, gabarito idêntico, pyflakes, fumaça completa, telas a 1500 e 1280 px com altura reduzida,
  os quatro períodos, o gesto quadro a quadro, mochila vazia/1/8/12, venda, recompra, mouse, teclado e dicas.
- **Falta:** Jean conferir.

### 13/10/2026 — A capela por partes: exterior, salão e escada (1.76.0)

- **Pedido de Jean:** corrigir a escada do ossuário, representar o exterior e o salão alagado, e mostrar o ambiente
  certo em cada momento da narrativa, sem mexer em regra nem antecipar a sacristia e o fundo.
- **Feito:**
  - a escada do ossuário em degraus de pedra, com a boca da descida separada do buraco das correntes;
  - o exterior e o salão (a partir do protótipo, sem o sarilho na nave);
  - os pontos "Buraco no muro" e "Sacristia" fazendo as ações do menu, e os sapos só de olhar;
  - a cena de cada momento: chegada e recuo por fora, entrada e vitória no salão (inquieto e quieto), a página do
    lugar pelo passo da missão.
  - Mapa dos cinco ambientes, gatilhos e planejamento em [20](20-CENA-INTERATIVA-OSSUARIO.md).
- **Verificado:** testes (`test_cenas_capela.py` novo), gabarito idêntico, pyflakes, fumaça completa
  (`cenarioCapelaFora` novo), telas a 1500 e 1280 px com altura reduzida, quatro períodos, três classes, fuga, salvar e
  carregar, movimento reduzido.
- **Falta:** Jean conferir; a sacristia e o fundo.

### 13/10/2026 — A capela no cenário principal (1.77.0)

- **Pedido de Jean:** a cena da capela no topo, no lugar das ruínas genéricas, sem imagem no texto; a luta no
  ambiente certo; os pontos fora de alcance na luta; tela baixa sem pulos.
- **Feito:** o ambiente desenhado na arte do topo (`Vista.usarAmbiente`), os pontos numa camada por cima dela, a luta
  do salão e a do ossuário com o próprio fundo, a arte inteira enquanto houver ambiente, o sarilho e a corrente no
  topo. Detalhe em [20](20-CENA-INTERATIVA-OSSUARIO.md).
- **Verificado:** testes, gabarito idêntico, pyflakes, fumaça completa, telas a 1500 e 1280 px com altura reduzida,
  movimento reduzido, recarregar.
- **Falta:** Jean conferir; as entregas 2 (luz e criaturas) e 3 (navegação).

### 13/10/2026 — Luz do ossuário e criaturas do salão (1.78.0)

- **Pedido de Jean:** tirar o facho pontilhado do alçapão e deixar a tocha como luz principal; tirar o afogado verde
  do salão; sanguessugas presas à madeira ou à linha d'água, sem flutuar.
- **Feito:** a tocha entre os nichos e o sarilho, com a sala escurecendo longe dela; o alçapão só com um cinza frio
  de dia; sanguessugas grudadas nos bancos e numa coluna, esticando devagar. Detalhe em [20](20-CENA-INTERATIVA-OSSUARIO.md).
- **Verificado:** testes, gabarito idêntico, pyflakes, fumaça completa, telas a 1280 px, dia e noite.
- **Falta:** Jean conferir.

### 13/10/2026 — Andar pela capela (1.79.0)

- **Pedido de Jean:** separar onde o personagem está do progresso da missão, andar entre as salas vencidas por
  pontos, menu e teclado sem repetir nada nem gastar nada, sacristia e fundo sem mostrar outra sala, pontos sem nome
  fixo (com destaque opcional) e os sapos com uma resposta curta.
- **Feito:** a sala no registro da missão (save antigo deduz pela etapa), as passagens entre salas vizinhas vencidas,
  cada ação da capela só na sala dela, recuo/resgate/viagem atualizando a sala, fundo neutro para a sacristia e o
  fundo, escada/brecha/descida como pontos, nomes só no mouse e no foco, "Destacar interações" (Ajuda e F4), a linha
  de perto dos sapos. Detalhe em [20](20-CENA-INTERATIVA-OSSUARIO.md).
- **Verificado:** testes (`TestNavegacao` novo), gabarito idêntico, pyflakes, fumaça completa (`cenarioCapelaSalas`
  novo), telas a 1500 e 1280 px com altura reduzida, três classes, movimento reduzido, salvar e carregar, derrota.
- **Falta:** Jean conferir; a arte da sacristia e do fundo (planejada). A E9 segue aberta.

### 13/10/2026 — Ajustes sobre a capela (1.79.1 a 1.81.0)

- **Pedido de Jean:** água do salão atrás dos bancos; a luz do ossuário como referência; o lodo recolhido no fundo;
  a saída da capela antes de acampar (manual e por exaustão).
- **Feito:** a camada dos bancos acima da água (1.79.1); a referência de iluminação no documento 20, com o mercado
  mantido como está (sem código); o lodo só no fundo, dentro da descida antes de Ilse e na página do fundo depois
  dela, sem começar a luta (1.80.0); "Sair e acampar" e a exaustão pela mesma saída, com a faixa que conta o caminho
  e a capela por fora no topo, amanhecendo do lado de fora (1.81.0). Detalhe em [20](20-CENA-INTERATIVA-OSSUARIO.md).
- **Verificado:** testes (`TestLodoNoFundo`, `TestSairParaAcampar` novos), gabarito idêntico, pyflakes, fumaça
  completa (`cenarioCapelaAcampar` novo), telas a 1500 e 1280 px, movimento reduzido.
- **Falta:** Jean conferir. A E9 segue aberta.

### 13/10/2026 — Explorar só do lado de fora da capela (1.81.1)

- **Pedido de Jean:** tirar "Explorar a região" das salas internas, com a mesma regra no motor e no tutorial.
- **Feito:** a opção só no exterior; `Jogo.explorar` não faz nada dentro (sem tempo, tocha nem sorteio); o quadro V5 e
  a fala de Morel esperam o lado de fora. Detalhe em [20](20-CENA-INTERATIVA-OSSUARIO.md).
- **Verificado:** testes, gabarito idêntico, pyflakes, fumaça completa, telas nas quatro salas e no exterior, salvar e
  carregar, tutorial ligado.
- **Falta:** Jean conferir. A E9 segue aberta.

### 13/10/2026 — Quatro correções: os dois anéis, o contrato do tutorial, os ratos e o ouro (1.82.0)

- **Pedido de Jean:** antes da arte da sacristia, corrigir quatro pontos da 1.81.1 e levantar (só levantar) os ataques
  em área dos inimigos. Trabalho retomado de uma sessão interrompida: nada dela estava no repositório (nem na pasta
  nem nos commits), então as quatro correções foram refeitas a partir da 1.81.1.
- **Feito:**
  - **Anéis:** a comparação mostra a troca com cada espaço ("Anel 1 · no lugar de…", ou "Anel 2 · vazio"), na janela
    do item achado, nas dicas da mochila e do mercado e no Shift; a janela empilha os dois anéis vestidos em cartões
    baixos ao lado do achado (cabe a 1280×620; mais baixo, rola por dentro). Equipar diz o espaço: "Substituir {anel}
    (Anel 1)" / "Equipar no Anel 2 (vazio)", um botão por espaço, teclas 1, 2. Da mochila (dois cliques ou botão
    direito, no inventário e no mercado), o anel vai para o espaço vazio; com os dois ocupados, um menu pergunta qual
    substituir (mouse e teclado); no texto, a mesma pergunta. Nada escolhe o "pior" por soma. Mochila e regras de
    equipar iguais. O inventário e a ficha de texto dizem "Anel 1" e "Anel 2".
  - **Contrato introdutório:** o K1 só aponta um contrato num lugar ligado direto à vila (pelo grafo das estradas),
    da oferta de sempre; o K2 aponta o mesmo contrato e só diz "Clique neste contrato para viajar até…" quando é uma
    viagem só; mais longe, diz por onde o caminho passa. Detalhe em [18](18-E9-ABERTURA-GUIADA.md), seção 24.
  - **Ratos da despensa:** o relatório da luta (o espólio, 12 XP) vem logo depois da vitória, antes da cena do
    taverneiro (antes, só depois dela e do Continuar). Seção 24 do [18](18-E9-ABERTURA-GUIADA.md).
  - **"Ouro insuficiente":** tentar um serviço ou compra sem ouro (forja, curandeira, taverna, templo, mercado: suprimento,
    peça e recompra) mostra um aviso curto dentro do próprio cartão, encostado no preço, sem cobrir o preço, o motivo
    escrito nem as outras opções; um só (clicar de novo troca), pelo mouse, Enter e as teclas de número. O texto é o
    motivo do motor ("Esgotado", "A aljava está cheia.", "Os fregueses já contaram tudo o que sabiam hoje."...). A
    tentativa não chega ao motor: não gasta ouro, item, tempo nem sorteio (antes, a tecla de número na taverna chegava
    ao motor e a volta ao menu da vila consumia um sorteio).
- **Verificado:** testes (558, com `test_aneis.py`, `test_ouro_insuficiente.py`, o relatório dos ratos e os K1/K2
  novos), pyflakes, fumaça completa (cenários novos: `cenarioAneis`, `cenarioOuroInsuficiente`; o K2 até a
  chegada no `cenarioCiclos`; a ordem dos ratos no `cenarioAbertura`). Gabarito examinado antes de atualizar: as 18
  partidas de mundo gerado mudam só no campo `motivo` novo das metas e dos painéis e em "Anel 1/Anel 2" na ficha de
  texto; nenhuma escolha nem sorteio mudou (comparado com as transcrições normalizadas). Telas a 1500×950, 1280×720,
  1280×620 e 1280×560: anéis com dois ocupados, um vazio e nenhum; a abertura dos ratos nas três classes, com e sem
  tutorial, atacando e acabando com a habilidade; forja, taverna, templo, curandeira e mercado sem ouro.
- **Visto e não mexido:** com o tutorial ligado e sem ouro para a cama, o quadro D1 ("Clique neste cartão para dormir
  aqui até o amanhecer.") ainda aparecia; resolvido na 1.82.1, logo abaixo.
- **Falta:** Jean conferir. A arte da sacristia e do fundo não começou. A E9 segue aberta.

### 13/10/2026 — Ataques em área dos inimigos: diagnóstico (sobre a 1.82.0, sem mudar o jogo)

- **Pedido de Jean:** levantar quem já tem ataque em área, como os inimigos escolhem alvos, quanto ameaçam a comitiva,
  candidatos coerentes, e se o ataque deveria ser anunciado. Sem implementar nem aumentar dano.
- **Feito:** [21](21-DIAGNOSTICO-ATAQUES-EM-AREA.md) e a medição `python -m tests.area_inimigos`. Resumo: só a
  Varredura (seis guardiões e o antagonista), sem aviso, cerca de 1,5 vez por luta de guardião; nada no Vale. A
  comitiva já recebe de 31% a 49% do dano dos inimigos em lutas comuns. O herói não tem como proteger os aliados.
  Recomendação: ataque em área como habilidade anunciada (o modelo do Golpe Esmagador), rara e só em inimigos fortes,
  e, antes disso, decidir uma ação de proteção do grupo.
- **Falta:** Jean decidir se e em que ordem (seção 7 do 21). A E9 segue aberta.

### 13/10/2026 — Os quadros do tutorial só apontam o que dá para pagar (1.82.1)

- **Pedido de Jean:** "Clique neste cartão para dormir" só quando o serviço pode ser usado naquele momento; sem ouro,
  o cartão, o preço e o "Ouro insuficiente" ficam, e o quadro fica pendente, sem segurar os outros. Conferir os outros
  quadros que mandam comprar ou tratar, preservar o grátis e não marcar como visto só porque faltou ouro.
- **Feito:** os quadros que mandam usar um serviço pago seguem a mesma regra dos cartões (o `motivo` do motor,
  `Servicos.motivo_pagar`):
  - **D1** (o cartão Dormir): só com ouro para a cama.
  - **F3** (a Curandeira na vila): só se algum tratamento dá para pagar (o primeiro grátis conta e continua dito).
  - **F4** (o cartão na cabana): aponta o primeiro ferimento que dá para tratar agora (o do F1, se der); sem nenhum,
    não aparece, e sair da cabana assim não o marca como visto (antes, marcava sempre).
  - **V2** já esperava o ouro; agora lê o mesmo motivo do cartão do templo e da taverna.
  - Os quadros só informativos (V3 "O Mercado vende mais", F2 sem bandagem "O Mercado vende bandagens; a Curandeira
    trata na hora") não apontam o serviço nem mandam usá-lo: ficaram como estavam.
- **Verificado:** testes (`TestSoOQueDaParaPagar` novo: os de D1, F3 e F4 falham sem a correção), gabarito idêntico,
  pyflakes, fumaça completa (no `cenarioOuroInsuficiente`, a taverna sem ouro sem o quadro e com ouro com ele); telas a
  1280×720 sem ouro (vila, taverna, curandeira: nenhum quadro, cartões com preço) e 1500×950 com ouro (F3, D1, F4).
- **Falta:** Jean conferir. A E9 segue aberta.

### 13/10/2026 — A sacristia desenhada (1.83.0)

- **Pedido de Jean:** completar as artes da Capela Afogada, a sacristia e depois o fundo com Ilse, em entregas e
  commits separados, sem mudar regra, custo, tempo, encontro, recompensa, equilíbrio ou história.
- **Feito (a sacristia):** a sala seca com a porta do salão (um degrau acima da água), as prateleiras reviradas, a
  janela alta com a escada de mão, o buraco do livro, o baú embaixo do pano e o alçapão; os momentos vindos do motor
  (entrada com os dois vultos e a lanterna, luta sem eles, vitória com a lanterna apagada e o livro fora do buraco,
  visita com o baú já levado); a luz da lanterna, depois a janela e a tocha de quem está ali; os pontos porta e alçapão
  (as mesmas ações do menu) e janela e livro (só olhar). Detalhe em [20](20-CENA-INTERATIVA-OSSUARIO.md).
- **Verificado:** testes (`TestSacristia` novo), gabarito idêntico, pyflakes, fumaça completa; telas nas três classes,
  1500 e 1280 px com altura reduzida, movimento reduzido, fuga, derrota, dia e noite.
- **Falta:** Jean conferir. Próxima entrega: o fundo alagado com Ilse. A E9 segue aberta.

### 13/10/2026 — O fundo alagado com Ilse (1.84.0)

- **Pedido de Jean:** a segunda arte da capela, separada da sacristia, sem mudar regra, custo, tempo, encontro,
  recompensa, equilíbrio ou história.
- **Feito:** a escada de pedra terminando na água, a água pela cintura, as duas pedras de moinho, as correntes do
  buraco do ossuário (presas, esticadas até os pulsos dela; soltas, frouxas, pelo preparo) e Ilse entre as pedras. O
  motor manda o momento (`missoes.cena_fundo`: descida, visita, luta, descanso, destruída) e os momentos dela pela
  celebração `ilse`, depois do texto que os conta: abrir os olhos e cantar, o canto que falha no rito, a fita, afundar
  com a água clara, desfazer-se com a água turva um instante. Na luta, ela é só a carta. A página do fundo tem a escada
  (subir ao ossuário) e o lodo (a ação de Caspar); depois do desfecho, o fundo sem ela. O fundo neutro saiu.
  Detalhe em [20](20-CENA-INTERATIVA-OSSUARIO.md).
- **Verificado:** testes (`TestFundo` novo), gabarito idêntico, pyflakes, fumaça completa; telas nas três classes,
  1500 e 1280 px com altura reduzida, movimento reduzido, dia e noite, com e sem tocha, destruição, descanso,
  desistência do rito, coleta do lodo sem luta, derrota, recarregar e carregar o save.
- **Falta:** Jean conferir as duas artes da capela. Nada de outras regiões nem dos ataques em área; a E9 segue aberta.

### 14/10/2026 — Acabamento das salas da capela (1.84.1 a 1.86.1)

- **Pedido de Jean:** acabamento sobre a 1.84.0: aproximação sem rótulos e destaques separados, a tábua da estante,
  continuidade entre os acontecimentos da mesma sala (e Ilse presente até a resolução), o livro na parede com a
  leitura, o texto e o cabelo de Ilse, o canto dela, o baú recolhido pela interação e a barra branca do modal.
- **Feito, em commits separados:** 1.84.1 (de perto sem a vista geral; F4, mouse e foco de teclado separados; Esc
  afasta), 1.85.0 (o livro no buraco com o relato num livro aberto; o baú no canto, recolhido pelo ponto ou pelo
  menu, com migração de saves antigos para formato 4; a tábua partida; a doca que levava Sair ao salão), 1.85.1 (a
  mesma sala sem saltos: a lanterna e a tocha coerentes, a resolução de Ilse logo depois da luta pelo gancho
  `ao_vencer`, a mistura curta de luz), 1.86.0 (a descida conta as correntes como estão; o cabelo escuro sobre o
  rosto; o canto, um canal só, e o grito da desistência), 1.86.1 (o cartão da comparação entra sem passar da borda
  da janela). Detalhe e o que foi reproduzido em [20](20-CENA-INTERATIVA-OSSUARIO.md).
- **Verificado:** testes, gabarito (só o número do formato nos saves mudou, na 1.85.0), pyflakes e fumaça completa
  em cada commit; telas e quadro a quadro como no documento 20.
- **Falta:** Jean conferir (e ouvir o canto). Nada de outras regiões, ataques em área ou exploração nova; a E9 segue
  aberta.

### 14/10/2026 — A lanterna, a música de Ilse e a descoberta pelo livro (1.86.2 a 1.88.0)

- **Pedido de Jean:** três ajustes sobre a 1.86.1, em commits separados.
- **Feito:** 1.86.2 (a lanterna da sacristia fica no chão, acesa, da luta à página; a luz não depende mais da tocha
  da luta), 1.87.0 (a música do fundo, composição própria na direção das Gnossiennes de Satie, e a página
  `tests/navegador/ouvir_canto.html` para ouvir e gravar), 1.88.0 (**a consulta ao livro agora determina o momento
  da descoberta**: a vitória só mostra o livro embrulhado; ler, pelo ponto, pelo menu ou no modo texto, registra uma
  vez as pistas de Ilse e do Sigilo; o livro em primeira pessoa do padre; antes de ler, a guardiã é a Bruxa Afogada e
  Berta não aparece; saves antigos mantêm o que já sabiam). Detalhe em [20](20-CENA-INTERATIVA-OSSUARIO.md).
- **Verificado:** testes, gabarito idêntico, pyflakes e fumaça completa em cada commit; a conferência técnica do áudio
  (gravado offline e medido) no documento 20.
- **Falta:** Jean conferir e ouvir (a avaliação musical é dele). Nada de outras regiões, ataques em área ou
  empacotamento; a E9 segue aberta.


### 14/10/2026 — Oito correções sobre a 1.88.0 (1.88.1 a 1.88.5)

- **Pedido de Jean:** oito correções da versão atual, cada uma reproduzida no fluxo real antes de mexer; depois, o
  protótipo da ficha do herói (registrado à parte, abaixo).
- **Reproduzido e corrigido:**
  - 1.88.1. *Lua:* a sombra da meia-lua era pintada com a cor do topo do céu, o que desenhava um quadrado à noite;
    agora a parte em sombra não se pinta e aparece o céu real (paisagens e períodos conferidos). *Iniciativa:* o
    quadro diz o turno extra antes dos inimigos, que a abertura é só do herói (comitiva e animal no turno seguinte) e
    o bônus do primeiro golpe com o número do motor. *Canto de Ilse:* começa quando o fundo aparece na descida (e na
    visita com ela), sem mudar a música; sem Ilse, sem canto; um canal só.
  - 1.88.2. *Anel no espaço vazio:* o motor diz para onde foi o antigo (nenhum, mochila, ficou para trás com a
    mochila cheia) e a tela só põe o selo quando houve antigo, no cartão do espaço certo (achado, inventário e
    mercado; os dois espaços).
  - 1.88.3. *Grito do cultista:* aplicado, o selo e o ícone no cartão; não aplicado, o motivo real do motor no alvo
    ("a fé não vacila", "resistiu", "imune"), via o lance `efeito_negado`. *Reações ao golpe:* gravei lances e tela
    quadro a quadro (normal e acelerado); a ordem já seguia o motor e não há defeito de regra. Faltava a origem: o
    roubo de vida diz o item, os espinhos acendem quem os tinha, e a regeneração e a vida por abate ganharam lance.
  - 1.88.4. *Compras rápidas:* de seis cliques rápidos só três chegavam ao motor (a pergunta ainda não tinha voltado,
    e a proteção de clique duplo e o redesenho comiam o resto). Agora cada clique num suprimento é um pedido, pelo id,
    numa fila que vai ao motor um de cada vez; o cartão bloqueado no meio (estoque, ouro, espaço) dá o aviso do motor
    e derruba o resto daquele suprimento; Esc, voltar ou outra pergunta descartam a fila. Equipamentos, venda e
    recompra continuam com a proteção por posição.
  - 1.88.5. *Segundo Continuar:* a varredura de partidas pela ponte achou o caso (o relatório e, depois, um Continuar
    numa página só com o registro da luta, por exemplo antes do "Exausto"), e o explorar comum ainda segurava a página
    da luta com o fio de leitura. Depois da vitória, se só vieram ganhos e faixas, a pausa não pede leitura: a página
    vira para o lugar. Narração nova (o evento que continua, a cena de missão, a noite que cai) mantém a leitura e o
    Continuar dela; subida de nível, comparação de equipamento e escolhas seguem como eram. O clique (ou o Enter) que
    fecha o relatório não escolhe nada no menu seguinte.
- **Verificado:** testes (com os novos `test_reacoes_tela`, `test_aneis` e os da página em `test_web`), gabarito
  (diferenças conferidas antes de atualizar: só `"antigo"` na celebração do anel e `"anim": "grito"` no grito),
  pyflakes e fumaça completa em cada commit; cenários novos de navegador `reacoes` e `relatorio`, e na fumaça as
  compras rápidas (estoque, espaço e ouro acabando no meio, Shift+clique, Esc com fila) e o relatório (clique duplo,
  Enter segurado, subida de nível).
- **Falta:** Jean conferir jogando. Nada de outras regiões, ataques em área ou empacotamento; a E9 segue aberta.

### 14/10/2026 — Protótipo da ficha do herói (experimento, sem versão)

- **Pedido de Jean:** depois das correções, um teste visual da ficha do herói como painel completo, separado do jogo:
  dados reais da ficha, hierarquia (identidade primeiro, títulos de seção menores), molduras e espaços bem definidos,
  ouro com moderação, assets desenhados em código, controles de demonstração, avaliação na composição real em 1500 e
  1280 px (com janela baixa).
- **Feito:** `ferramentas/prototipos/hud/` (abrir `index.html`, ou `abrir.bat` no Windows). Os dados saem do motor
  (`gerar_dados.py` grava o dicionário de `rpg.web.estado.heroi` para cada combinação dos controles); o entorno é o DOM
  do jogo fotografado num lugar real, com a paisagem do `vista.js`. Assets novos em `arte.js`: retrato do Guerreiro,
  moldura em nove partes, espaço de item e os ícones de espada, escudo, anel e poção (mapas de material com contorno,
  luz e sombra do mesmo pintor). Decisões e o que não convenceu no `LEIA-ME.md` da pasta; capturas em `capturas/`.
- **Verificado:** aberto e fotografado em 1500×950, 1280×800 e 1280×720 (sem texto cortado, foco visível ao rolar,
  dicas à direita do painel sem cobrir o elemento, sem erro no console, servido do disco e por http).
- **É experimento:** não aprovado nem migrado; o jogo, os saves e a versão não mudaram por causa dele. Nada de mercado,
  combate, mapa, Diário ou outras janelas. **Falta:** a avaliação de Jean.

### 14/10/2026 — Ficha do herói, segunda tentativa: assets de imagem (experimento, sem versão)

- **Pedido de Jean:** a mesma ficha com as peças de uma imagem de referência (moldura, retrato, espada, escudo, anel,
  poção), para ver se assets de imagem dão um salto de acabamento sobre os desenhados em código.
- **Feito:** em `ferramentas/prototipos/hud/`, a versão "Assets" ao lado da "Anterior" (mesmos dados, mesma janela;
  o controle Versão ou a tecla V alternam). `preparar_assets.py` recorta as peças da referência (guardada intacta em
  `assets/original/`), limpa o alfa (2.600 pontinhos e uma franja escura saíram; alfa só 0 e 255) e reduz: moldura em
  nove partes e retrato a 1/4 (um pixel da arte por pixel da tela), ícones a 32 px nos espaços e 24 px nos atributos.
  Superfície lisa sem textura atrás do texto, títulos e fios mais discretos, dourado só na raridade, no foco e no
  talento. A Anterior ficou idêntica pixel a pixel.
- **Avaliação** (no `LEIA-ME.md` da pasta): o retrato é um salto real; os ícones leem bem a 32 px, mas a borda suave
  destoa dos sprites do jogo na mesma fileira (e a espada não serve a 16 px); a moldura tem bom peso, mas é de aço
  azulado ao lado dos painéis de bronze; a pintura detalhada fica mais rica que o cenário minimalista. Só funcionaria
  no jogo com o catálogo e as molduras dos outros painéis no mesmo estilo.
- **Verificado:** 1500×950, 1280×800 e 1280×720, nas duas versões (nome longo, ferimentos, foco pelo teclado com a dica
  acompanhando a rolagem, sem texto cortado, sem erro no console). **É experimento:** nada migrado, versão do jogo
  igual. **Falta:** a avaliação de Jean.

### 14/10/2026 — HUD 3: molduras, superfícies e controles na composição inteira (experimento, sem versão)

- **Pedido de Jean:** uma terceira versão do protótipo com três folhas de referência (molduras, texturas e controles),
  aplicada à HUD inteira (topo, ficha, barras e recursos, cena, leitura e ações, mapa, missão e caminhos, doca, dicas e
  uma janela), para avaliar a linguagem visual na composição, não só na ficha.
- **Feito:** em `ferramentas/prototipos/hud/`, a versão "HUD 3" ao lado da Anterior e da Assets (mesmos dados, mesma
  janela). `preparar_hud3.py` recorta as folhas (intactas em `assets3/original/`), limpa o alfa, reduz tudo 4× (a mesma
  escala para as três folhas), monta as nove partes com o trecho de borda sem rebite, separa moldura e preenchimento das
  barras e emenda as texturas. O entorno é o jogo fotografado na campanha com missão e contratos, a cena de missão e a
  janela do anel (`fotografar_composicao3.mjs`, `cenario_hud3.py`); o topo agora é desenhado com o mesmo estado da
  ficha (os números batem nas três versões). Estados dos controles (normal, mouse, pressionado, selecionado,
  indisponível, foco) por forma e não só por cor.
- **Avaliação** (no `LEIA-ME.md` da pasta): melhoraram o peso e a hierarquia das molduras, a coerência entre as
  colunas, a leitura dos controles e o espaço útil (menos rolagem em todas as medidas). Ficaram desencontrados: o grão
  das peças (1 px por pixel) contra o da paisagem e dos sprites (2 a 3), o latão dos rebites em toda placa, o retrato e
  os ícones antigos nos nichos novos, o desenho interno do mapa e os títulos dourados no estilo antigo.
- **Verificado:** 1500×950, 1280×800 e 1280×720, mouse e teclado, nas duas composições; sem erro no console e sem texto
  cortado. **É experimento:** nada migrado; motor, saves, telas de produção e versão iguais. **Falta:** a avaliação de
  Jean.

### 14/10/2026 — HUD 4: moldura principal, carvão e controles leves (experimento, sem versão)

- **Pedido de Jean:** nova rodada sobre a HUD 3 (direção aprovada para seguir no experimento): a moldura da ficha da
  versão Assets nos painéis principais, sem engrossar o resto; a superfície de carvão em tudo, sem o marrom do centro;
  o nome do lugar uma vez só; a doca como barra única; espaços de equipamento mais legíveis; menos moldura interna e
  menos dourado decorativo; retrato e ícones atuais do jogo.
- **Feito:** `hud4.css` em `ferramentas/prototipos/hud/`, a versão "HUD 4" no alternador (mesmos dados). Uma moldura por
  coluna (o centro junta barras, cena e doca), controles internos feitos pela interface, estados por forma, o que o
  motor já distingue (missão, contrato, seta de submenu) com forma própria. Nenhum asset novo.
- **Avaliação** (no `LEIA-ME.md` da pasta): composição mais coerente, molduras com presença de estrutura, página com
  mais espaço (sem rolagem no lugar a 1500×950; 72 px contra 207 a 1280×720); as laterais perderam uns 20 px para a
  moldura. Desencontrados: o grão macio da moldura reduzida, o retrato ×5 e os anéis miúdos, a doca centrada com
  sobras, o topo ainda fino e o nome do lugar dependente do painel do mundo.
- **Verificado:** 1500×950, 1280×800 e 1280×720, nas três composições, controles de demonstração escondidos; sem erro no
  console nem texto cortado. **É experimento:** nada migrado; motor, saves e versão iguais. **Falta:** a avaliação de
  Jean.

### 14/10/2026 — HUD 4 completa: ícones e retrato de quatro folhas (experimento, sem versão)

- **Pedido de Jean:** completar a HUD 4 (molduras, carvão, doca e cenários aprovados) com quatro PNGs: atalhos,
  equipamentos e recursos, lugares e atributos, retrato de um Guerreiro de demonstração. Originais intactos, alfa
  conferido, normalização pela área visível, redução comparada em tamanho real; desenhos só nos tipos que existem
  (lacuna registrada, nada inventado); contraste dos botões centrais; combate e capela no protótipo.
- **Feito:** em `ferramentas/prototipos/hud/`, a versão "HUD 4 completa" no alternador (mesmos dados; a HUD 4 continua).
  `preparar_hud4c.py` (37 peças em `assets4c/`, folhas de redução em `assets4c/teste/`; média por área com nitidez
  leve, um arquivo por tamanho e o @2x), `icones4c.js` (troca pelo papel e pelo tipo do motor), `hud4c.css`,
  entornos Combate e Capela (`composicao4c.js`, fotografados dos cenários "muralha" e "capela" com o Guerreiro nível 6).
  Corrigido de passagem: a paisagem ficava vazia ao trocar de entorno.
- **Avaliação** (no `LEIA-ME.md` da pasta): os anéis se leem, Grimório e Diário se distinguem, bolsa e equipamento têm o
  mesmo peso, o retrato cabe no quadro sem rolagem a mais, e os botões se destacam do fundo. Perderam leitura: Talentos,
  Salvar, provisões, amuleto, a bota e o escudo dos atributos em 20 px, ruínas e pântano. Desencontrados: o Guerreiro de
  ferro fica metade com peças novas e metade com sprites (as peças novas são de couro: não há elmo, cota, manopla,
  perneira, bota ferrada nem maça/martelo), dois retratos do herói (ficha e topo), o grão pintado contra o pixel duro,
  o combate de produção, a pedra azul com o azul do "mágico".
- **Verificado:** 1500×950, 1280×800 e 1280×720, nas composições de lugar, missão, luta e capela, mouse e teclado,
  controles de demonstração escondidos; sem erro no console, sem texto cortado, sem ícone reescalado, rolagem igual à da
  HUD 4; versões anteriores iguais pixel a pixel nas regiões paradas. **É experimento:** nada migrado; motor, saves,
  telas de produção e versão iguais. **Falta:** a avaliação de Jean.

### 14/10/2026 — HUD 4 pixel: família de ferro, mesmo rosto e atributos sem caixas (experimento, sem versão)

- **Pedido de Jean:** quatro folhas novas, mais perto da pixel art dos cenários; preservar molduras e cenários; fechar
  a ficha do Guerreiro com as peças de ferro; o mesmo rosto no topo e na carta da luta; atributos sem as quatro caixas,
  em duas colunas; ícones novos na luta; contraste do texto da luta; redução que preserve contorno (sem o filtro macio).
- **Feito:** em `ferramentas/prototipos/hud/`, a versão "HUD 4 pixel" no alternador (mesmos dados; as anteriores
  ficam). `preparar_hud4p.py` (45 peças em `assets4p/`; cinco reduções comparadas; escolhida a "paleta": alfa duro e
  só cores do desenho), `icones.js` (as famílias da HUD 4 completa e da pixel, pelo papel e pelo tipo do motor),
  `hud4p.css` (atributos, cabeça no topo, luta). O registro da luta passou de 35% para 70% nos turnos anteriores.
- **Avaliação** (no `LEIA-ME.md` da pasta): a ficha do Guerreiro fecha numa família só, o contorno duro fica mais
  perto dos cenários, um rosto só na ficha, no topo e na carta, atributos mais limpos e sem corte em 1280. Ainda
  escuros ou pequenos: grimório, silhuetas vazias, talentos, anel grande, bota e manopla. Desencontrados: o martelo
  (sem desenho), Fugir, inimigos e cartas de produção, recursos vazios do topo, o retrato pintado ao lado dos sprites.
- **Verificado:** capturas estáticas em 1500×950, 1280×800 e 1280×720 (lugar, missão, capela, luta, nome longo, fome,
  ferimentos, contratos, anéis); exercitados no navegador dica por mouse e teclado, Esc, tecla V, troca de entorno e
  rolagem; animações não conferidas. HUD 4 completa igual pixel a pixel. **É experimento:** nada migrado; motor, saves,
  telas de produção e versão iguais. **Falta:** a avaliação de Jean.

### 14/10/2026 — HUD 4 pixel: acabamento e teste funcional no jogo (experimento, sem versão)

- **Pedido de Jean:** HUD 4 pixel aprovada como direção; acabar a luta (cartas e roda na linguagem da HUD, estados por
  forma, foco visível, Fugir com a bota), conferir os botões durante a interação, listar as lacunas separando arte de
  layout e ligar a HUD ao jogo de verdade como teste explícito, sem trocar a interface padrão nem entrar no save.
- **Feito (acabamento):** `hud4p-luta.css` (cartas, roda, janelinha), estados dos botões com `translate` (a animação
  de entrada prendia o transform), tamanhos que faltavam e `assets4p/exibicao/indice.js`.
- **Feito (ligação):** `python jogar.py --hud-experimental` (ou `HUD=experimental` nos cenários) faz o servidor servir
  `ferramentas/prototipos/hud/` em `/experimento/` e pôr `jogo/ligar.js` no fim da página padrão; único ponto fora da
  pasta (`rpg/__main__.py`, `rpg/web/__init__.py`, `rpg/web/servidor.py`, documentado em `docs/ARQUITETURA.md`).
  `jogo/papeis.js` troca os desenhos pelo papel; `jogo/jogo.css` veste o painel real do herói. O cenário `tutorial`
  ganhou `NOME` (para nome longo).
- **Verificado de verdade:** a fumaça inteira com a HUD experimental (356 conferências, tudo certo, depois de corrigir
  os 404 de tamanho e a janela do anel em 1280×720); fuga, painéis por tecla e mouse, estados dos botões, animações da
  luta quadro a quadro (normal e movimento reduzido), três janelas com nome longo, fome, ferimentos e missões (menos
  rolagem que a padrão). A fumaça padrão, os testes e o gabarito continuam iguais.
- **Lacunas** (no `LEIA-ME.md` da pasta): de arte, martelo e machado, os únicos com desenho próprio, as outras classes,
  unguento, bomba, pena de fênix, recursos vazios, inimigos, ícones de habilidade e efeito; de layout, só o que a
  interface padrão já faz (a faixa da mira cobrindo a carta de cima) e a barra de experiência de produção.
- **É experimento:** a interface padrão continua a padrão; nada migrado; versão igual. **Falta:** Jean jogar e avaliar.

### 14/10/2026 — HUD experimental: componentes uniformes, superfícies e teste de arte (experimento, sem versão)

- **Pedido de Jean:** base da HUD 4 pixel aprovada; uniformizar os componentes antigos (divisórias, experiência,
  comitiva, menus, mercado e serviços) e tirar a faixa "escolha o alvo" de cima da carta; comparar uma superfície mais
  escura; testar a coerência entre a arte do mundo e a HUD com o mercador e o baú da sacristia; só registrar os
  retratos por classe.
- **Feito (interface):** `jogo/materiais.js` (os anéis, bicos e fios do jogo pintados em ferro, pelas mesmas grades),
  `jogo/telas.css` (janelas principais com a moldura, componentes internos leves, títulos de seção na versal pequena,
  mercado e serviços, Diário e mural em carvão com os documentos de papel, Talentos), a mira no vão da arena
  (`hud4p-luta.css`); `jogo/superficies.css` e `jogo/desenvolvimento.js` (Ctrl+Alt+S, `&superficie=`; no protótipo,
  o painel de demonstração).
- **Feito (arte):** `arte-teste.js` (o mercador em busto 24×24 e o baú em 16×16, desenhados em código com as cores do
  mundo), `arte-teste.html` (os pares) e a ligação no jogo (o balcão do mercado, a bolsa, o baú que voa; Ctrl+Alt+A).
- **Verificado:** três janelas e movimento reduzido nos percursos pedidos; fumaça padrão e experimental (356, tudo
  certo); testes, gabarito e pyflakes. Medido: a superfície mais escura deixa a página no tom do chão da paisagem e os
  botões mais destacados; a transição quase não acrescenta.
- **Registrado:** retratos do herói por classe (dois por classe, cosméticos) em `docs/ROADMAP.md`, ideias guardadas.
- **É experimento:** a interface padrão continua a padrão; versão igual. **Falta:** Jean avaliar a superfície e os dois
  desenhos.

### 14/10/2026 — A HUD de ferro vira a interface padrão (1.89.0)

- **Pedido de Jean:** HUD aprovada; migrar para a interface padrão (sem `--hud-experimental`, sem depender de
  `ferramentas/prototipos/hud/`), superfície mais escura sem transição, doca um pouco mais escura, barras do topo com
  limite em telas largas, a animação de equipar com o ícone atual, baú marrom como o Baú Trancado geral, mercador no
  mercado; não mexer em combate, economia, conteúdo, sorteios nem saves.
- **Feito:** `css/14-hud.css`, `15-hud-luta.css` e `16-hud-telas.css` (as regras aprovadas, fora da trava de pixel de
  `test_estilo_pixel.py`), `static/hud/` (molduras, texturas e os ícones em tamanhos de uso), `static/icones.js`
  (`Icones`: o desenho de cada papel num lugar só; as telas pedem a ele e, sem desenho, usam o sprite do jogo),
  `sprites.js` publica anéis, bicos e fios em ferro (o protótipo pede bronze). A ligação experimental saiu do servidor,
  de `jogar.py` e dos cenários; os protótipos ficam como histórico.
- **Ajustes:** grupo das barras do topo até 400 px e centralizado (em 1920 e 2560 a coluna do meio para em ~1064 px);
  doca com véu mais escuro, estados conferidos; o voo de equipar, guardar e comprar-e-vestir usa o mesmo desenho da
  origem e do destino; o Baú Trancado é sempre o baú marrom (bolsa, relatório, voo), o baú físico da sacristia não
  mudou; o busto do mercador na banca, nas cores do homem do cenário.
- **Verificado:** 601 testes, gabarito sem diferença (nenhuma escolha, sorteio ou estado mudou), pyflakes, a fumaça
  inteira (356 conferências, nenhuma exceção no servidor; logs guardados). Percursos com captura em 1500×950, 1280×720,
  1280×620, 1920×1080 e 2560×1440, mouse, teclado e movimento reduzido. A exceção do servidor e a falha de teste da
  rodada anterior não reapareceram; a única falha desta rodada foi causada pela migração (`Icones.vazio(s)` caía na
  regra de plural sem parênteses) e foi corrigida.
- **Pendente:** lacunas de arte (em `docs/ARQUITETURA.md`), ícones de 16 px dentro das opções ainda do jogo, o duplo
  clique da ficha equipa sem voo (como antes), capturas do README da interface antiga. **Falta:** Jean conferir.

### 15/10/2026 — Topo alinhado ao começo da coluna (1.89.1)

- **Pedido de Jean:** migração aprovada; na janela maximizada, o grupo do topo centralizado deixava um vão grande à
  esquerda. Alinhar ao começo da coluna, mantendo as barras em até 400 px, os números junto das barras e os recursos
  juntos; nenhuma outra mudança de layout.
- **Feito:** `#hud-linha` passa de `center` para `flex-start` (`css/14-hud.css`). O retrato fica a 12 px da borda
  interna (o recuo do topo) em todas as larguras; a sobra vai para a direita.
- **Verificado:** Guerreiro, Mago e Arqueiro em 1280×720, 1920×1080 e 2560×1440 (barras de 384 a 400 px, 340 no
  Arqueiro em 1280, que tem um recurso a mais; número a 6 px da barra; recursos numa linha só; nada sobreposto);
  601 testes, gabarito sem diferença, pyflakes e fumaça (356, tudo certo).
- **A exceção do servidor, agora com rastro:** `BrokenPipeError` em `servidor.py` (`_arquivo` → `_responder` →
  `wfile.write`) ao servir um arquivo de `/static/`, no fim do cenário de compras rápidas da fumaça, entre a última
  conferência e o cenário seguinte. É o navegador do teste fechando a página com um arquivo ainda a caminho; o teste
  passa e o jogo não é afetado. Não mexi no servidor (fora desta entrega); se for para silenciar, o lugar é o
  `_responder` ignorar `BrokenPipeError`/`ConnectionResetError`. **Falta:** Jean conferir.

### 15/10/2026 — Teste do retrato: o Guerreiro de capacete fechado (experimento, sem versão)

- **Pedido de Jean:** o primeiro retrato do Guerreiro no estilo do mundo, com capacete fechado e sem rosto; um
  candidato para avaliação, desenhado em código, com busto, cabeça do topo e versão da carta a partir do mesmo
  desenho; no protótipo, sem substituir o de produção nem mexer em molduras, layout, ícones ou cenários.
- **Feito:** em `ferramentas/prototipos/hud/`, as peças `guerreiro` (40×40; o busto inteiro e os recortes de 64 e 48
  px) e `guerreiro-carta` (16×16) em `arte-teste.js`; `retrato-teste.html` (ampliado, tamanhos reais, fotografias);
  `fotografar_retrato.mjs` e `retrato-no-jogo.js` (o jogo de verdade fotografado com o candidato, em
  `capturas-retrato/`). `docs/ROADMAP.md` registra a direção; quantidade e personalização continuam em aberto.
- **Verificado:** capela, banca do mercado e luta, em 1500×950 e 1280×720, com o retrato de hoje e com o candidato
  (ficha 80/64, topo 48, carta 32; nenhum erro no console); as duas páginas do teste de arte abrem sem erro; testes,
  gabarito, pyflakes e fumaça. Avaliação no `LEIA-ME.md` da pasta. **Falta:** Jean avaliar.

### 15/10/2026 — Continuidade visual e acabamento (1.90.0)

- **Pedido de Jean:** quatro pontos, sem mexer em regras, custos, sorteios nem recompensas: o retrato aprovado do
  Guerreiro no jogo; as figuras do cenário que ficam na sala durante a luta; as barras que mexiam sem mudança de valor;
  o Continuar no metal da HUD.
- **Retrato:** o capacete fechado (39fff85) em `rpg/web/static/retratos.js`, com as mesmas grades, pintado por
  `Sprites.grade` (o mesmo pintor do busto do mercador, que perdeu o dele); `Icones.retrato`/`cabeca` pedem a ele: ficha
  80 px, janela baixa 64, topo 48, carta 32 (a versão de 16×16). Os PNG do retrato gerado saíram de `hud/icones/`.
  Mago e Arqueiro seguem com o sprite. Pixel a pixel também com a tela a 125%.
- **Figuras na luta:** os dois de capa escura da sacristia ficam na sala enquanto a carta de cada um está de pé: cada
  cultista leva a `figura` (`missoes.FIGURAS_SACRISTIA`), a carta a manda para a tela (`estado.combate`), e o vulto
  sai pela identidade, não pela posição nem pelo nome; caído, ele se desfaz no tempo da carta. Fuga e derrota não o
  tiram; a nova tentativa recomeça com os dois; recarregar no meio da luta mostra só quem está de pé. Ilse fica na
  água a luta inteira e só sai pelas cenas do desfecho; na mistura curta de uma troca de momento ela era coberta pela
  base de antes por uns 200 ms, e agora é desenhada por cima. Só esses encontros tinham figuras desenhadas.
- **Barras:** a causa era a medida da largura antes de redesenhar (o enchimento contra a barra inteira, com a borda):
  uma barra cheia media 98% e saía mais curta a cada estado novo (comprar uma tocha manda dois: 300 → 294 → 288 px, e
  enchia de novo). Agora a medida é contra o lado de dentro, com um encaixe de meio ponto.
- **Continuar:** o mesmo componente em todos os lugares (página, cenas, relatório, festas), no metal escuro: letra da
  interface em 20 px (era o título em 32), latão discreto, seta pequena parada, mouse, pressionado e foco distintos.
- **Verificado:** 602 testes, gabarito sem diferença (nenhuma escolha, sorteio ou estado do herói mudou), pyflakes,
  fumaça (356, nenhuma exceção no servidor). No navegador, em 1280×720 e maximizada (1920×969), com movimento normal e
  reduzido: o retrato nas quatro apresentações; a sacristia (um cai e o outro fica, pela identidade nos dois sentidos;
  fuga em quatro tentativas, nova tentativa, vitória; página recarregada); Ilse nos dois desfechos, amostrada de 100
  em 100 ms, sem quadro sem ela; as barras quadro a quadro em compras, abas, venda e inventário, e o feedback de
  poção, máximo pela fome, experiência e recurso; o Continuar na abertura e no espólio. **Falta:** Jean conferir.

### 15/10/2026 — Teclado no Continuar, carga na capela e o retrato no Inventário (1.90.1 e 1.90.2)

- **Continuar pelo teclado** (sem foco posto por código): na cena de texto, o foco começa na página, Tab chega ao botão
  em 9 toques e Shift+Tab volta, o anel aparece, Enter e espaço avançam uma vez; nada a corrigir. No espólio, o quadro
  não levava o foco (21 Tabs pela página escondida atrás). 1.90.1: o foco vai para o Continuar dele, Tab e Shift+Tab
  ficam nele, e fechado o quadro o foco volta; Enter e espaço fecham uma vez, sem escolha ao motor; com o mouse, o anel
  não aparece.
- **Carga real de save na capela:** antes do desfecho (no ossuário) e depois dele, nos dois caminhos (salvar no fundo,
  sair ao título, carregar): a mesma sala, Ilse ausente, a água escura ou clara, ouro, experiência, itens e o Sigilo
  iguais, e o desfecho não é contado de novo.
- **Inventário (1.90.2):** o meio dos espaços mostrava o desenho da classe com um halo atrás. Agora pede o retrato a
  `Icones.retrato` (o mesmo da ficha: o Guerreiro de capacete fechado, 80 px; 64 na janela baixa), sem halo; Mago e
  Arqueiro seguem com o desenho da classe. Folga até arma, escudo, mãos e anel: 22 px (30 na janela baixa).
- **Verificado:** 602 testes, gabarito sem diferença, pyflakes, fumaça (356, nenhuma exceção no servidor).

### 15/10/2026 — Teste dos retratos: Mago e Arqueiro (experimento, sem versão)

- **Pedido de Jean:** um candidato de Mago e um de Arqueiro, no protótipo, com o Guerreiro de capacete fechado como
  referência; sem substituir os retratos de produção.
- **Feito:** em `ferramentas/prototipos/hud/`, as peças `mago` e `arqueiro` em `arte-teste.js` (40×40, os recortes de
  64 e 48 px no mesmo enquadramento do Guerreiro e a carta de 16×16 de cada um); `retratos-classes.html` (a comparação
  dos três); `fotografar_retratos_classes.mjs` (o jogo de verdade, capela, vila e luta, em 1500×950 e 1280×720), com
  `retrato-no-jogo.js` agora pela classe do herói. Avaliação no `LEIA-ME.md` da pasta; `docs/ROADMAP.md` registra os
  dois em avaliação.
- **Verificado:** as fotografias do jogo (ficha 80/64, topo 48, carta 32 e 36 na vez; a mira pela tecla 1), as três
  páginas do teste de arte abrem sem erro, nenhum erro no console. O jogo não mudou. **Falta:** Jean avaliar.

### 15/10/2026 — Os retratos dos três heróis no jogo (1.91.0)

- **Pedido de Jean:** o Mago e o Arqueiro candidatos (a1c7b1d) aprovados; integrar sem mudar os desenhos, em todo lugar
  onde o herói aparece, com um mecanismo só de escolha; a fogueira com a mesma identidade; o "nível 5" do Patrulheiro
  sozinho na linha de baixo da ficha baixa.
- **Feito:** o Mago e o Arqueiro em `retratos.js`, com as mesmas grades (conferidas uma a uma contra o protótipo).
  `Icones` escolhe tudo: `retrato` (ficha, Inventário), `cabeca` (topo, carta, cartão do save) e o novo `figura` (o
  canvas de 16×16 da fogueira: a carta do herói, ou o sprite do jogo para quem ainda não tem retrato). A fogueira
  desenhava o retrato antigo de 16×16 (cabeça e ombros, não corpo inteiro): agora é a carta de cada classe, na mesma
  escala e no mesmo lugar. O cartão do save também pedia o sprite da classe direto e passou para `Icones`. O título da
  ficha e do Inventário mantém "nível 5" junto (espaço sem quebra): pode quebrar antes dele, não no meio.
- **Verificado:** as três classes em 1500×950 (movimento normal) e 1280×720 (movimento reduzido): ficha 80/64, topo 48,
  carta 36 na vez, Inventário, fogueira com Morel, Odette e Yara e o cartão do save; nenhum lugar com o desenho antigo,
  nenhum erro no console. 602 testes, gabarito sem diferença, pyflakes, fumaça (356, nenhuma exceção no servidor).
- **Não feito:** a E9 e a validação com jogadores novos continuam abertas. Os companheiros seguem com os sprites de
  sempre; os candidatos deles são a entrega seguinte, só no protótipo.

### 15/10/2026 — Teste da comitiva: Morel, Odette e Yara (experimento, sem versão)

- **Pedido de Jean:** um candidato de cada companheiro, só no protótipo, pelo método dos heróis e a partir do que o
  jogo diz deles; as peças para ficha, menus e carta; uma proposta para a fogueira; comparação ampliada, nos tamanhos
  reais, ao lado dos heróis e no jogo.
- **Feito:** em `ferramentas/prototipos/hud/`, as peças `morel`, `odette` e `yara` em `arte-teste.js` (40×40, o recorte
  da cabeça e a carta de 16×16); `comitiva-teste.html` (a comparação); `fotografar_comitiva.mjs` com
  `comitiva-no-jogo.js` (o jogo de verdade, hoje e com os candidatos, em `capturas-comitiva/`). Referências, proposta
  da fogueira (a carta de 16×16 como figura, como o herói) e avaliação no `LEIA-ME.md` da pasta.
- **Verificado:** fogueira com cada herói, painel, tela da Comitiva (tecla C e Tab) e duas lutas, em 1500×950 e
  1280×720; a página abre sem erro; nenhum erro no console. O jogo não mudou. **Falta:** Jean avaliar. A E9 e a
  validação com jogadores novos continuam abertas.

### 15/10/2026 — Teste da comitiva: revisão de Morel, Odette e Yara (experimento, sem versão)

- **Pedido de Jean:** manter a base e revisar só alguns traços, ainda no protótipo: o cabelo da Yara (assimétrico, mechas
  com lama, parte presa; depois, roxo), a cruz da Odette de volta, a cicatriz do Morel como marca e não faixa (depois,
  na diagonal); no meio, a espada do Morel com forma de espada e sem os pixels soltos (remendos, rebites, manchas do
  chamuscado). O texto do Morel ("de orelha a orelha") não mudou; o desenho não o segue ao pé da letra.
- **Feito:** as grades novas em `arte-teste.js`; a primeira versão guardada em `comitiva-v1.js` para comparar;
  `fotografar_comitiva.mjs` aceita `VERSOES` (hoje, v1, candidato) e fotografa também o passo à frente de um
  companheiro na luta; `comitiva-teste.html` mostra v1 × revisão. Detalhes e avaliação no `LEIA-ME.md` da pasta. A erva
  na gola da Yara foi testada e descartada (lia como broche).
- **Verificado:** fogueira com cada herói, painel, tela da Comitiva, lutas (vez do herói e companheiro agindo), em
  1500×950 e 1280×720; a página abre sem erro; nenhum erro no console. O jogo não mudou. **Falta:** Jean avaliar. A E9 e
  a validação com jogadores novos continuam abertas.

### 15/10/2026 — Experimento de resolução: martelo, Pena de Fênix e Morel 80×80 (experimento, sem versão)

- **Pedido de Jean:** antes de integrar a comitiva e de fazer o lote de itens, testar se outra resolução melhora a
  apresentação sem sair da linguagem dos cenários: um martelo e uma Pena de Fênix em 32×32 e em 64×64 (dois desenhos), e
  o Morel aprovado ao lado de uma versão de 80×80, com as versões próprias para os tamanhos menores. A mensagem chegou
  cortada nos critérios de avaliação ("reconhecimento rápido; leitura…"); completei com leitura de detalhe, o mesmo
  mundo e o custo.
- **Feito:** em `ferramentas/prototipos/hud/`, `resolucao-teste.js` (as amostras), `resolucao-teste.html` (a comparação
  com alternância no mesmo lugar), `resolucao-no-jogo.js` e `fotografar_resolucao.mjs` (o jogo de verdade, capela,
  mercado e luta, em `capturas-resolucao/`); o cenário `mercado` ganhou `AMOSTRAS=1` (um Martelo e uma Pena de Fênix).
  Avaliação e o custo da redução no `LEIA-ME.md` da pasta.
- **Recomendação:** itens em 32×32, e 64×64 só desenhado à parte para apresentação grande; retratos no 40×40 a 2× (o
  pixel dos cenários), trazendo do 80×80 a expressão e uma carta própria de 32×32.
- **Verificado:** a página nas duas versões, em 1500×950 e 1280×720, sem imagem quebrada nem erro; as fotografias do
  jogo sem erro no console. O jogo não mudou. **Falta:** Jean avaliar. A E9 e a validação com jogadores novos continuam
  abertas.

### 15/10/2026 — A carta pequena do Morel e a espada (experimento, sem versão)

- **Pedido de Jean:** fechar o experimento de resolução. Decidido: itens em 32×32 para bolsa, mochila e mercado; o
  Morel de 80×80 como candidato da apresentação grande; cabeça e carta com adaptação própria; "nunca reduzir" não vira
  regra geral. Corrigir a carta pequena do Morel (conferindo antes se o componente deforma), testar 32 contra 36 px,
  adaptar a cabeça e a ficha baixa; refazer a espada do Morel, encaixada nas costas e sem o cabo em zigue-zague.
- **Feito:** a carta nova de 32×32 perto da cabeça e a redução do 40 a 32 para comparar; a espada refeita no 40×40, no
  80×80 e nas cartas; a cabeça de 48 sem os pedaços da espada e a ficha baixa recortada para a espada caber inteira; as
  versões anteriores em `morel-anterior.js`; `resolucao-no-jogo.js` com a opção de manter o rosto inteiro na carta em
  foco e de trocar a carta do Morel companheiro; `fotografar_carta.mjs`; a seção nova no alto de
  `resolucao-teste.html`. Detalhes no `LEIA-ME.md` da pasta.
- **Verificado:** o componente não deforma (32×32 quadrado no nicho de 36); a ampliação de 1,12× é só da carta do
  herói, e o companheiro fica sempre em 32 px; com o rosto inteiro, todos os pixels iguais, em janela normal e baixa,
  com movimento normal e reduzido, e a mira pela tecla 1 continua; nenhum erro no console. O jogo não mudou.
- **Pendente:** Jean avaliar a carta pequena. A integração da comitiva e dos itens e o ajuste do texto da cicatriz
  (autorizado) continuam para depois. A E9 e a validação com jogadores novos continuam abertas.

### 15/10/2026 — O padrão das cartas de combate (experimento, sem versão)

- **Pedido de Jean:** fechar um padrão para os retratos nas cartas de combate, com os três heróis e os três
  companheiros juntos. Referência: o Morel "40 reduzido a 32" (a carta nativa de rosto aproximado foi rejeitada).
  Comparar as cartas atuais com reduções dos bustos aprovados e ajustar só quem destoar; testar o rosto do herói em
  32 px exatos e alinhado ao pixel na vez dele.
- **Feito:** em `ferramentas/prototipos/hud/`, `cartas-teste.js` (os seis em 32×32: a redução do busto; ajustes
  pontuais no visor do Guerreiro, na cruz, nos olhos e no véu da Odette, nos olhos da Yara), `cartas-no-jogo.js` (a
  troca na luta e o nicho do herói em foco em 36 px, rosto em 32, alinhado), `fotografar_cartas.mjs` e
  `cartas-teste.html`. O padrão de enquadramento registrado no `LEIA-ME.md` da pasta e no `docs/ROADMAP.md`.
- **Verificado:** três composições, anterior e candidata, em 1500×950 e 1280×720, com movimento normal e reduzido; o
  nicho e o rosto do herói em pixels inteiros; a tecla 1 e o Esc funcionando; nenhum erro no console. O jogo não mudou.
- **Decisões guardadas para a integração:** Morel grande em 80×80; a carta dele "40 reduzido a 32"; Odette e Yara
  revisadas aprovadas; o ajuste do texto da cicatriz (autorizado); martelo e Pena de Fênix de 32×32.
- **Falta:** Jean avaliar os seis antes da integração. A E9 e a validação com jogadores novos continuam abertas.

### 15/10/2026 — A comitiva no jogo (1.92.0)

- **Pedido de Jean:** fechar a escolha das cartas (heróis, Odette e Yara com a carta de 16×16 a 2×; o Morel com o busto
  reduzido a 32) e integrar Morel, Odette e Yara pelo `Icones` em todas as aparições; o rosto do herói em 32 px na vez
  dele, no pixel inteiro; o texto da cicatriz do Morel. Sem itens, sem telas novas, sem mudar regras.
- **Feito:** os três em `retratos.js` com um desenho por papel (busto, ficha baixa, cabeça, carta, figura), a escala
  saindo do tamanho do desenho; `Icones.cabeca` em 48, 32 ou 16 px e `Icones.figura` pela figura de 16×16; o painel, a
  tela da Comitiva, a carta e o cartão de reação, a faixa, o aviso, o chip de aprovação e a fogueira pedindo ao
  `Icones`. Na vez do herói, o nicho do retrato desfaz a ampliação da carta e vai ao pixel inteiro depois dos
  movimentos da arena (`Batalha.foco`, `css/15-hud-luta.css`). "Cicatriz de orelha a orelha" virou "uma cicatriz
  atravessa o rosto dele" (o gabarito mudou só nessa frase, em 13 partidas, e foi atualizado). O critério das cartas
  (leitura, identidade e peso, não a mesma resolução) registrado em `docs/ARQUITETURA.md`, `docs/ROADMAP.md` e no
  `LEIA-ME.md` do protótipo.
- **Verificado:** os três heróis com pares diferentes, em 1500×950 e 1280×720, com movimento normal e reduzido; o rosto
  do herói em 32 px no pixel inteiro, a mira e o Esc, o companheiro agindo, a reação, o painel, a Comitiva, o aviso, a
  faixa e a fogueira; nenhum sprite antigo dos três; 602 testes, gabarito, pyflakes, fumaça (356).
- **Achado, sem mexer:** com movimento reduzido a faixa de celebração some na hora (já era assim).
- **Falta:** Jean conferir. O martelo e a Pena de Fênix (32×32) ficam para o lote de itens. A E9 e a validação com
  jogadores novos continuam abertas.

### 15/10/2026 — O martelo e a Pena de Fênix no jogo (1.93.0)

- **Pedido de Jean:** integrar os dois itens de 32×32 escolhidos no experimento de resolução, pela estrutura normal e
  pelo `Icones`, sem mudar funcionamento, atributos, preços, estoque, sorteios nem recompensas; a Pena não pode tomar o
  lugar do ícone de Vigor por usar o mesmo sprite.
- **Feito:** `rpg/web/static/desenhos.js` (os itens desenhados em código, como os retratos), com as grades aprovadas;
  `Icones` entrega o martelo pelo desenho do equipamento e a Pena pelo id do consumível (nunca pelo desenho "chama",
  que é também o Vigor, o Poder e o fogo); em 32 e 64 px pixel a pixel, em 48 a versão a 2× reduzida pelo navegador.
  O cenário `vila` ganhou `ACHADO=martelo`.
- **Verificado** (`ferramentas/prototipos/hud/fotografar_itens.mjs`, `capturas-itens/`), em 1500×950 e 1280×720: a
  prateleira, a bolsa da ficha e do Inventário, a mochila da aba Vender, a dica com a comparação, o cartão do saque
  (64 px), o voo ao equipar (48 px) e o martelo no corpo; a pena só em espaços de item, o Vigor e o Poder com os
  deles. 602 testes, gabarito sem diferença, pyflakes, fumaça (356). O relatório da luta pede a imagem pela mesma
  chamada por id da bolsa (não fotografado: nenhum cenário garante a pena no espólio).

### 15/10/2026 — O menu inicial aberto sobre a paisagem (1.93.1)

- **Pedido de Jean:** no menu inicial, a paisagem animada visível atrás da composição; o título grande; as opções logo
  abaixo, leves (texto sobre a paisagem, sombra discreta, um indicador pequeno da escolhida); sem o painel opaco, a
  moldura externa e as placas de metal; sem slogan; as mesmas opções, fluxos, navegação e proteções; só no menu.
- **Feito:** `css/17-titulo.css`, só em `body.modo-titulo`: tira a moldura e o carvão do palco, troca o véu da página
  por uma sombra radial suave sem borda (atrás do título e das opções), o título em 80/96/112 px (múltiplos do pixel da
  fonte, conforme a janela) com um filete de latão embaixo, centralizado no palco mesmo quando passa da coluna de
  leitura; as opções sem face, textura nem relevo, centralizadas, em creme com sombra; a escolhida em latão claro, com o
  losango antes e um filete curto embaixo (forma, além da cor). O JS não mudou (o mouse continua levando o foco junto).
  A folha entrou em `FORA_DA_TRAVA` com as outras da HUD.
- **Verificado:** 1280×720, 1500×950 e 1920×1080 (parado, teclado, mouse), a lista de saves, a volta ao título depois
  de salvar e sair de uma partida (sem moldura, título em 112 px na janela grande), movimento reduzido; a criação de
  personagem (fora do menu) não mudou. Verificações do CLAUDE.md.
- **Falta:** Jean conferir.

### 15/10/2026 — A emenda entre cenário e leitura e as etiquetas ao redimensionar (1.93.2)

- **Pedido de Jean:** (1) a faixa escura entre o pontilhado do cenário e a superfície do texto; (2) os nomes dos
  prédios saindo de cima dos desenhos ao alternar entre maximizado e janela menor, sem recarregar.
- **Causas encontradas:** (1) a superfície da leitura estava só na `#pagina`; o que ficava na cena fora dela mostrava
  o carvão mais escuro do palco: a parte transparente da rampa pontilhada do chão e, durante a orientação da vila, a
  faixa que `orientacao.js` reserva entre o cenário e o texto (96 px, sem fundo; a faixa da captura de Jean). Na luta,
  o mesmo embaixo da arena. (2) A vila posicionava os prédios no evento `resize` da janela, quando a largura já é a
  nova, mas a altura do `#vista` ainda está no começo da transição (0,35 s); a escala saía da altura velha e não se
  refazia no fim. A capela recalculava no `transitionend` e estava certa; as duas copiavam a conta do desenho.
- **Feito:** a superfície da leitura passou para a `#cena` (fora do título e das telas de menu, que ficam como
  estavam), a página transparente por cima; nenhum efeito novo. `Vista.caixaDaArte()` é a conta única (a mesma do
  desenho, com os arredondamentos dele) e `Vista.aoRedimensionar` avisa a cada mudança de tamanho do canvas; a vila
  (camada, botões, balões, clique no cenário) e os pontos da cena usam as duas.
- **Verificado:** `tests/navegador/redimensionar.mjs` (novo): 7 alternâncias entre 1920×1009, 1280×720 e 1405×850 na
  mesma página; antes, até 173 px de erro na vila; agora 0 px na vila e na capela; mouse, clique no balão, clique no
  cenário, Enter e F4 depois delas. Fotos antes/depois da superfície (orientação, vila, evento, em 1920 e 1280) e da
  luta e do mercado. Verificações do CLAUDE.md.
- **Falta:** Jean conferir.

### 15/10/2026 — Experimento: itens, ícones e acabamento da roda (sem versão)

- **Pedido de Jean:** só no protótipo, machado, unguento e bomba de fumaça pelas descrições reais; espada, escudo e
  anel atuais ao lado de candidatos no estilo do mundo; Grimório e Talentos (doca), Ataque e Defesa (ficha) e Fugir
  (roda) nos tamanhos reais; uma alternativa de acabamento para a roda (nichos, placas, teclas, janelinhas e os seis
  estados) sem mudar disposição, fluxo, mira ou áreas clicáveis; comparar no jogo e avaliar.
- **Feito:** `ferramentas/prototipos/hud/` (desenhar_itens.py, itens-icones-teste.html, roda-alternativa.css, os dois
  roteiros de fotografia e a avaliação; o LEIA-ME explica). O cenário `tutorial` ganhou `VITRINE=1`. O jogo não mudou.
- **Recomendação:** integrar machado, unguento, escudo de madeira, Grimório, Talentos, Ataque, Fugir e o acabamento da
  roda; a bomba depois de clarear a bola; espada só com a família inteira; anel atual fica; Defesa opcional.
- **Falta:** Jean avaliar. Nada integrado.

### 15/10/2026 — O plano de apresentação e serviços no ROADMAP

- **Pedido de Jean:** registrar a sequência de 8 etapas (itens e ícones; Grimório, livro e criação; forja; protótipo
  de reforço e encantamento; Templo, Curandeira e Taverna; cenários do mapa e da campanha; eventos da estrada;
  preparação e animação de habilidades), separando o trabalho atual das propostas, com a Capela Afogada como
  referência e as hipóteses de reforço, encantamento e habilidades preparadas sem números nem implementação.
- **Feito:** `docs/ROADMAP.md`, seção "Apresentação e serviços (plano de 10/2026)"; "Ícones próprios para cada
  habilidade" das ideias guardadas aponta para a etapa 8.
- **Falta:** nada a implementar agora. Interiores, forja nova e sistema de habilidades não começaram.

### 15/10/2026 — Lote de itens recusado; teste do escudo (sem versão)

- **Decisão de Jean:** o lote de candidatos não foi aprovado (os atuais têm mais volume, personalidade e acabamento).
  Ficam os itens e ícones atuais e a Pena de Fênix; o acabamento alternativo da roda fica para avaliação separada.
- **Pedido:** um escudo só, com o atual como referência direta (mesmo escudo, materiais e enquadramento), buscando
  volume e acabamento; uma proposta, comparação no jogo, parar.
- **Feito:** `ferramentas/prototipos/hud/desenhar_escudo.py` (relevo iluminado, render em 8× e redução por tamanho),
  `escudo-teste/`, `fotografar_escudo.mjs`, `capturas-escudo/`, a seção no topo de `itens-icones-teste.html` e a
  avaliação. A produção não mudou.
- **Leitura:** o atual continua melhor em 32 px; o candidato ganha em 48 e 64 na construção do aro e da bossa.
- **Falta:** Jean avaliar.

### 15/10/2026 — O escudo refinado em pixel art (sem versão)

- **Pedido de Jean:** continuar com o candidato do escudo (a direção está próxima) e refinar a linguagem de pixel
  art, só no protótipo: cada tamanho na própria grade, luz e sombra em grupos de pixels, paleta organizada; comparar
  atual, anterior e refinado no jogo; avaliar e parar. Pedido no meio: o canto de baixo à direita estava gordo.
- **Feito:** `ferramentas/prototipos/hud/desenhar_escudo_pixel.py` (regras na grade, reproduzível) e `escudo-pixel/`;
  `fotografar_escudo.mjs` com as três versões; a seção do escudo e a avaliação em `itens-icones-teste.html`. O canto
  de baixo à direita (duas revisões): a lateral de 1 px pela diagonal e, sem o toque da parede do aro (em 64 virava
  um risco solto), o degrau escuro a volta toda. A produção não mudou.
- **Leitura:** melhorou a organização, a silhueta e a espessura, os reflexos do aro e a leitura em 32; ainda perde
  para o atual no reflexo do gomo (mais em 64) e na face de 64, mais clara e chapada.
- **Falta:** Jean avaliar. Depois, confirmar o método num segundo objeto antes de pensar numa skill.

### 15/10/2026 — Escudo final e Unguento de Prata: o método em dois objetos (sem versão)

- **Pedido de Jean:** o escudo refinado foi aprovado como base visual; uma passagem curta de acabamento (gomos de
  sombra mais escuros, reflexo do gomo mais presente em 48 e 64, o 32 preservado) e o método no Unguento de Prata,
  só no protótipo; comparar, registrar o processo e parar.
- **Feito:** `escudo-pixel/` final (o anterior em `escudo-pixel-v1/`; 32 igual); `pixel_comum.py` (as etapas comuns,
  o escudo refeito sobre ele sem mudar um pixel); `desenhar_unguento_pixel.py` → `unguento-pixel/` (32, 48, 64, com
  a identidade do atual: o pote de louça clara com rótulo, agora aberto mostrando a pasta); `fotografar_unguento.mjs`
  e `unguento-no-jogo.js` → `capturas-unguento/`; a seção no topo de `itens-icones-teste.html` com a avaliação; o
  processo (comum, por material, por tamanho, reutilizável) no LEIA-ME do protótipo. A produção não mudou.
- **Falta:** Jean avaliar. Nada de outros itens nem de skill antes disso.

### 15/10/2026 — Unguento: conceito novo; estudo da ocupação dos ícones (sem versão)

- **Decisão de Jean:** o escudo final está aprovado como referência (a revisão artística dele acabou). O pote de louça
  com rótulo lembrava embalagem moderna: o unguento vira um pote de cerâmica de boticário.
- **Feito, só no protótipo:**
  - `unguento-pixel/` com o conceito novo, em 32 e 64; o pote anterior ficou em `unguento-pixel-v1/`.
  - O estudo da ocupação:
    - `ocupacao_icones.py`, `ocupacao/` e `ocupacao-no-jogo.js`;
    - `fotografar_ocupacao.mjs`, com o cenário `VITRINE=2` (armadura vestida, sem o machado);
    - a medida de onde a folga nasce: a imagem é exibida em 32 px num espaço de 56 a 60, e os arquivos já são justos;
    - uma alternativa de 40 px, com arquivos nativos.
  - As duas coisas e a recomendação estão na primeira seção de `itens-icones-teste.html`. A produção não mudou.
- **Falta:** Jean avaliar. Se a ocupação de 40 for aprovada, faltam ainda:
  - os arquivos de 40 de todo o equipamento;
  - o acabamento do escudo em 40;
  - uma decisão para os sprites 16×16.

### 15/10/2026 — Escudo e unguento no jogo, equipamento em 40 px e a skill de arte (1.94.0, 1.95.0)

- **Pedido de Jean:** levar ao jogo o escudo final (com o cravo de 40 px corrigido) e o pote de cerâmica do unguento
  pelo `Icones`; o equipamento em 40 px no corpo e na mochila do Inventário; registrar o processo numa skill do
  projeto. Sem mudar regras, preços, estoque, recompensas ou sorteios; o lote recusado de candidatos não entra.
- **Entrou na produção:**
  - 1.94.0 (`bbeda6a`): o escudo final em 32, 48 e 64 (iguais ao aprovado) e o 40 com a sombra do cravo de cima à
    esquerda clareada (4 pixels, em `AJUSTES`); o Unguento de Prata em 32 e 64, achado só pelo id (a Curandeira
    continua com o desenho dela). Os scripts saíram do protótipo para `ferramentas/arte/` (`pixel_comum.py`,
    `desenhar_escudo_pixel.py`, `desenhar_unguento_pixel.py`), que gravam em `rpg/web/static/hud/icones/`.
  - 1.95.0 (`d498062`): `Icones.equipamento` mostra o equipamento em 40 px no Inventário quando há arquivo de 40; os
    40 da família pintada saem de `ferramentas/arte/familia_ferro.py` (as peças aprovadas em `familia-ferro/`, o
    processo de sempre; `--conferir` refaz os 32/48/64 do jogo iguais). Espaços, bordas, foco e áreas clicáveis não
    mudaram (nas fotos, só os ícones diferem).
  - A skill (`.claude/skills/arte-itens-fenda/SKILL.md`, com as soluções do escudo e do unguento em `exemplos.md`) e
    `ferramentas/arte/prancha.py` (tamanho real sobre o carvão). Nenhum item novo foi desenhado para testá-la.
- **Como usar a skill:** ela é descoberta pelo Claude Code ao abrir o repositório (conferido numa sessão nova: aparece
  na lista e é escolhida para pedidos de item ou ícone); à mão, `/arte-itens-fenda`. Ela ajuda a desenhar e a
  avaliar e termina na proposta com fotos; não aprova nada sozinha. As referências aprovadas são os arquivos do jogo
  (`rpg/web/static/hud/icones/escudo-*.png`, `unguento-*.png`); o histórico das rodadas fica no protótipo.
- **Continuam com o desenho de antes:** todos os outros itens e ícones da família de ferro (só ganharam o tamanho de
  40); o martelo e a Pena de Fênix (desenhos de 32, ficam em 32 no Inventário); as armas e peças de couro das outras
  classes, o machado, os únicos com desenho próprio, a bomba de fumaça e o resto das lacunas de
  `docs/ARQUITETURA.md` (sprites 16×16, em 32 no Inventário); as silhuetas dos espaços vazios (32; a do escudo agora
  é a do escudo novo, apagada).
- **Verificado:** `ferramentas/arte/fotografar_itens.mjs` em 1500×950 e 1280×720 (mercado com o unguento na
  prateleira e a compra, a dica do escudo na aba Vender, o cartão do saque com o escudo em 64 e o que se usa em 48, o
  voo ao equipar, o baú aberto com o unguento, o voo do unguento até a bolsa, a ficha, o Inventário em 40, a dica
  comparando os dois anéis, arrastar um anel para o Anel 2, dois cliques e Enter no "Substituir", i e Esc, o arqueiro
  com o martelo e os sprites antigos em 32, a Curandeira com o desenho dela), sem erro no console; 602 testes,
  gabarito sem diferença, pyflakes, fumaça (356), nas duas versões. `claude plugin validate .claude/skills`.
- **Falta:** Jean conferir jogando. Para depois, registrado no `docs/ROADMAP.md` sem executar: o Mago na fogueira
  (postura e silhueta), as versões pequenas e intermediárias do Morel (painel e luta, preservando o busto grande),
  novos lotes de itens. A E9 e a validação com jogadores novos continuam abertas.

### 15/10/2026 — Mago na fogueira e Morel pequeno (propostas); a skill e o ensaio da capela (sem versão)

- **Pedido de Jean:** com o escudo, o unguento e o Inventário em 40 aprovados (a etapa visual encerrada), duas
  propostas pequenas de personagem, só no protótipo, e dois registros: a skill distinguir os tamanhos parados das
  transformações das animações; guardar o ensaio particular da Capela Afogada.
- **Propostas** (commit `98c9af9`, em `ferramentas/prototipos/hud/personagens/`, explicadas no `LEIA-ME.md` do
  protótipo):
  - antes de desenhar, o levantamento do que cada componente usa: a figura de 16×16 (a fogueira; para os heróis, é a
    própria carta da luta), a carta de 32 px (luta, painel, aviso) e a cabeça de 48 (Comitiva, reação, quem chega);
  - o Mago na fogueira: uma figura só da fogueira, sentado, a cabeça no meio dos ombros, a base reta, as mãos no colo;
  - o Morel: a carta de 16×16 a 2× e a cabeça de 24×24 a 2×, desenhadas à mão como as dos outros (sem reduzir o busto
    e sem a carta de rosto aproximado recusada).
  - Atual × candidata no jogo, em 1500×950 e 1280×720 (`fotografar_personagens.mjs`), e a página
    `personagens-teste.html`. O busto de 80, a ficha baixa e a figura da fogueira do Morel, os retratos do Mago fora
    da fogueira e os outros personagens não mudaram.
- **Registros** (commit seguinte): a skill `arte-itens-fenda` separa a leitura parada (cada tamanho com arquivo nativo)
  das transformações das animações (o voo até a bolsa anima o arquivo de 32; o voo ao corpo encolhe o de 48), e diz
  que a redução do navegador que já existe é herança, não regra para itens novos; nenhuma animação mudou. O ensaio da
  Capela Afogada de 12/10/2026 estava no ambiente e foi guardado em `ferramentas/prototipos/capela-afogada-ensaio/`
  (página pronta, fontes, fotos, a régua das paisagens e o LEIA-ME com como abrir), como histórico; a capela de
  produção não foi tocada.
- **Verificado:** as fotos sem erro no console; os retratos nas mesmas posições e tamanhos nas duas versões; o ensaio
  da capela reconstruído a partir das fontes sai idêntico e abre direto do arquivo, sem erro; o unguento refeito pelo
  script continua igual ao do jogo; `claude plugin validate .claude/skills`. O jogo não mudou (sem versão).
- **Falta:** Jean avaliar as duas propostas. A E9 e a validação com jogadores novos continuam abertas.

### 15/10/2026 — O Morel pelas referências escolhidas e o Mago na fogueira (1.96.0 e 1.97.0)

- **Pedido de Jean:** recusar a carta e a cabeça novas do Morel (commit `98c9af9`), voltar aos desenhos que ele
  escolheu pelas capturas, corrigir só a espada da versão pequena, e integrar o Mago sentado na fogueira (aprovado),
  em commits separados.
- **Versões escolhidas e recusadas do Morel** (para nenhuma outra sessão trocar de novo):
  - **Escolhida, lugares pequenos:** a figura de 16×16 da fogueira (`MOREL_FIGURA` em `rpg/web/static/retratos.js`),
    agora também a carta de 32 px (luta, painel da comitiva, aviso) e o chip, a 2×; a única mudança de desenho é a
    espada (o punho reto num eixo só, a guarda centrada longe do rosto, a lâmina sumindo atrás da ombreira; 13 pixels,
    só nas colunas da espada).
  - **Escolhida, cabeça:** a de 48×48 a 1× (`MOREL_CABECA`), nos cartões da Comitiva, na reação "Morel aprova" e na
    faixa de quem chega. Sem mudança.
  - **Mantidos:** o busto de 80×80 e a ficha baixa de 64. Hoje nenhuma tela mostra o busto de um companheiro (o
    retrato grande da ficha e do Inventário é só do herói); a maior apresentação do Morel no jogo é a cabeça de 48.
  - **Recusadas:** a carta "40 reduzido a 32" (o busto antigo de 40×40, de cabeça pequena e traço fino; saiu de uso e
    de `retratos.js`, fica no histórico da 1.92.0) e os candidatos de 16×16 e 24×24 de `98c9af9` (no protótipo,
    marcados como recusados). Não fazer outra proposta de rosto do Morel sem pedido.
- **O Mago na fogueira** (1.97.0): o papel `fogueira` de `retratos.js`, pedido só por `Icones.figura` (o canvas da
  fogueira); a grade é a aprovada, pixel a pixel. A carta da luta, o topo, a ficha, o Inventário e o chip continuam com
  os desenhos de antes (conferido na página: a carta do herói, o topo e o chip de 16 com os de sempre, e o desenho da
  fogueira em nenhum outro lugar).
- **Verificado** nas duas versões: no jogo, em 1500×950 e 1280×720, a fogueira com o Mago sozinho e com a comitiva,
  o Morel na fogueira, na carta da luta (Guerreiro, Morel e Odette; Arqueiro e Morel) e no painel, a reação "Morel
  aprova", o aviso, a faixa de quem chega e a tela da Comitiva, nos mesmos lugares e tamanhos, sem erro no console;
  602 testes, gabarito sem diferença, pyflakes, fumaça (356).
- **Falta:** Jean conferir. A E9 e a validação com jogadores novos continuam abertas.

### 15/10/2026 — A aljava do Arqueiro e a lua da capela (1.97.1)

- **Pedido de Jean:** a aljava do Arqueiro não parecia estar nas costas (ficava em pé ao lado da cabeça, como um
  poste); revisar em todos os retratos do Arqueiro. Na primeira revisão (não enviada) ela ficou escondida demais; Jean
  pediu mais corpo, flechas mais detalhadas e o ângulo da alça que ele carrega. E, na capela de fora à noite, uns
  pixels de outra cor em volta da meia-lua.
- **A aljava** (`ARQUEIRO` e `ARQUEIRO_CARTA` em `rpg/web/static/retratos.js`; o roteiro em
  `ferramentas/prototipos/hud/arqueiro/aljava.py`): nas costas, na mesma diagonal da correia que cruza o peito (uns 45
  graus), a boca saindo por trás do ombro, com cinta, aro e duas flechas com as penas (clara em cima, escura embaixo) e
  o entalhe; o corpo some atrás do capuz e do ombro. Desenhada à mão, pixel a pixel (a 45 graus, a conta automática
  deixava as penas em xadrez). Mudam todos os papéis do Arqueiro (busto, busto baixo, cabeça, carta, figura); o resto
  do desenho e os outros personagens, não.
- **A lua** (`baseExterior` em `rpg/web/static/telas/cenas.js`): a sombra da lua em quarto era pintada com a cor do
  alto do céu, e onde o céu já é a faixa de baixo sobrava um bloco de outro tom. Agora a sombra não se pinta (o céu de
  verdade fica à vista), como a paisagem já fazia (`vista.js`). O ensaio guardado da capela tem o defeito antigo e fica
  como está (histórico).
- **Verificado:** no jogo, em 1500×950 e 1280×720, a ficha, o topo, o Inventário, a luta e a fogueira com o Arqueiro, e a
  lua da capela antes × depois; 602 testes, gabarito sem diferença, pyflakes, fumaça.
- **Falta:** Jean conferir.

### 15/10/2026 — Protótipo do acampamento do lado de fora da Capela Afogada (sem versão)

- **Pedido de Jean:** um protótipo visual do acampamento, com a composição mais próxima da qualidade das salas da capela,
  começando pelo lado de fora da Capela Afogada. Só protótipo: a fogueira de produção não muda até a avaliação. O fogo
  e a luz ficam; os personagens são os fechados na 1.97.0; nada de mecânica nova. (A mensagem chegou cortada em "Se
  alterar"; o protótipo não toca no motor nem nas regras.)
- **O que foi feito** (`ferramentas/prototipos/acampamento/`, com o `LEIA-ME.md`): a cena no topo, no lugar da paisagem,
  como as salas da capela (o quadro de 320×72 pela `Vista.usarAmbiente`, as figuras clicáveis por cima pela
  `Vista.caixaDaArte`); embaixo, só a frase, a instrução, o contador e quem vai e quem fica, e o palco com moldura sai.
  Três planos: longe, o céu da hora, a outra margem e a capela pequena afundada no brejo, apagada à esquerda; no meio,
  um teso de terra seca com o fogo da produção (o mesmo desenho, movimento e luz, levado para 166,60) e a roda, cada um
  num tronco, numa pedra ou na manta, com sombra no chão e um calor leve do lado do fogo; quem fica senta na beira da
  luz, perto da barraca, com penumbra; perto, o barranco escuro nos cantos de baixo. Objetos: a barraca, a mochila e o
  cobertor enrolado ao lado dela, o cantil encostado num tronco; nenhum clicável.
- **Como abrir:** `python ferramentas/prototipos/acampamento/cenario_acampamento.py capela_fora` (a cópia da pasta
  `static` com o protótipo; `PROTOTIPO=0` mostra o jogo como está).
- **Verificado** em 1500×950 e 1280×720 (`fotografar_acampamento.mjs`, em `capturas/`): atual × protótipo; o menu de um
  companheiro, deixar no acampamento e levar de volta (as figuras e o rodapé batem com quem está presente a cada vez),
  a ferida, a conversa e a volta, o Dormir até o amanhecer (a capela de fora volta), o Arqueiro com o lobo, o herói
  sozinho, manhã, crepúsculo e chuva; sem erro no console. Na janela baixa, a cena, o texto, quem vai e quem fica e a
  doca ficam à vista sem rolar.
- **Falta:** Jean avaliar. Fica para depois: outros lugares (cada um com o fundo desenhado à mão, na mesma organização)
  e a orientação D3, que aponta o "Dormir" dentro do texto (no protótipo ele mora na cena).

### 16/10/2026 — A fogueira na cena do topo (1.98.0)

- **Pedido de Jean:** integrar o protótipo aprovado do acampamento, preservando a arte e o funcionamento: a cena no
  topo, texto e comitiva embaixo, sem imagem duplicada nem a moldura antiga, a emenda em pontilhado direto até a
  leitura; o entorno do lugar (a capela só onde ela existe; nos outros, os fundos que já existem); nomes só com mouse,
  foco ou F4; o Dormir na cena, com a orientação D3 apontando para ele; nenhuma regra nova.
- **O que entrou:** `telas/acampamento.js` (o desenho: `Acampamento.montar`) e `telas/fogueira.js` (a tela, os
  pontos e o Dormir sobre a arte); o motor manda a chave do lugar nos dados da fogueira (`lugar`, só nos lugares da
  campanha; o gabarito não muda, porque as partidas dele são no mundo gerado). A `Vista` empresta o lugar sem ambiente
  (`paisagem`, `chuva`, `camadas`) e a capela empresta o contorno dourado (`Cenas.cantos`). Detalhes em
  `docs/ARQUITETURA.md` ("A fogueira").
- **Entornos:** a Capela Afogada com o entorno do protótipo (a capela pequena no brejo, à esquerda, a outra margem, a
  névoa); o Charco dos Juncos, o Bosque do Moinho e o mundo gerado com a própria paisagem do lugar (o céu da hora e
  as silhuetas do bioma: as árvores mortas do charco, os pinheiros do bosque) atrás do teso. **Futuro:** fundos
  desenhados para cada lugar (na mesma organização, `ENTORNOS`), na etapa de cenários.
- **Interações e tutorial:** os mesmos menus (conversar, deixar no acampamento, levar de volta, o carinho), a figura
  mudando de vaga com o estado; o ✉ de quem quer conversar no nome (no mouse) e no rodapé. O D3 mora na faixa logo
  abaixo da cena, com a haste até o Dormir (como os prédios da vila); um Dormir só. A orientação passou a medir o
  quadro longe da borda (encostado na direita, ele encolhia na medida e passava da faixa).
- **Verificado:** em 1500×950 e 1280×720, normal e reduzido: as três classes sozinhas e com a comitiva cheia
  (reserva, ferida, o lobo), a capela, o Charco e o Bosque, manhã, crepúsculo e chuva, mouse, F4, teclado,
  redimensionar, deixar e levar de volta, conversar, Dormir (a capela de fora volta), exaustão, sair da capela para
  acampar, recarregar a página na fogueira, o D3 (`ferramentas/arte/fotografar_acampamento.mjs`); a fumaça ganhou
  as conferências da cena e do D3.
- **Falta:** Jean conferir.

### 16/10/2026 — A barra de Foco e a carta de quem foge (1.98.1)

- **Pedido de Jean:** a barra de Foco do Arqueiro não aparecia na carta da luta e ficava branca na HUD; fugindo com
  sucesso, a carta do herói ficava parada um tempo no canto da tela em vez de sair inteira.
- **O Foco:** a HUD de ferro dá a cada barra uma imagem de enchimento (vida, Vigor, Mana, experiência); o Foco não
  tinha, e o enchimento ficava transparente (na HUD, aparecia só o rastro claro por baixo). Entrou
  `hud/enche-verde.png`, o azul da Mana com o tom levado ao verde do Foco (`ferramentas/arte/enche_verde.py`).
- **A fuga:** o estado que chega depois do lance da fuga redesenha a carta e remontava as classes dela, guardando só
  as de animação; a de quem já saiu (`escapando`, e `fugindo` do inimigo que foge) caía, e a carta acendia de novo
  onde a fuga a deixou, até a luta acabar (a fala do Morel desaprovando segurava esse fim). As duas passaram a ser
  guardadas.
- **Verificado:** a fumaça ganhou o cenário do Foco e da fuga (ele falha sem as correções e passa com elas); 602
  testes, gabarito sem diferença, pyflakes, fumaça.
- **Falta:** Jean conferir.

### 16/10/2026 — O machado e a Bomba de Fumaça em pixel art (proposta, sem versão)

- **Pedido de Jean:** lote pequeno pela skill `arte-itens-fenda`, só no protótipo: o machado e a Bomba de Fumaça,
  com a comparação no jogo (atual × proposta, 1500×950 e 1280×720). No meio, sobre a bomba: mais cara de bomba,
  mais personalidade, preta.
- **Feito:** os geradores `ferramentas/arte/desenhar_machado_pixel.py` (machado de barba de uma mão, 32/40/48/64) e
  `desenhar_bomba_pixel.py` (pote preto vidrado com pano, rede de cordão e pavio, só 32, o único tamanho parado
  dela); a proposta em `ferramentas/prototipos/hud/machado-bomba-pixel/`; as fotos e as pranchas em
  `capturas-machado-bomba/` (`fotografar_machado_bomba.mjs`, `comparar_machado_bomba.py`); os cenários ganharam
  `ARMA=<desenho>` (vila, mercado, tutorial) e `AMOSTRAS=3` no mercado. O registro completo, a leitura e o que falta
  estão em `ferramentas/prototipos/hud/LEIA-ME.md` ("O machado e a Bomba de Fumaça").
- **Nada mudou no jogo:** sem integração, regras, preços, estoque, efeitos, sorteios ou animações; a caveira continua
  nos papéis dela (conferido na lixeira em cada foto) e o machado do Redemoinho e da Fúria não muda.
- **Verificado:** testes, gabarito sem diferença, pyflakes e fumaça (os cenários novos só agem com as variáveis novas).
- **Falta:** Jean avaliar; a escolha de evento que gasta um item ainda usa o sprite 1× (outro papel); a roda de
  ações fica para a entrega separada.

### 16/10/2026 — O machado e a Bomba de Fumaça no jogo (1.99.0)

- **Pedido de Jean:** integrar os dois exatamente como aprovados no protótipo (`ee17544`), pela etapa de integração
  da skill `arte-itens-fenda`, sem mexer em regras, números nem animações.
- **Feito:** os arquivos em `rpg/web/static/hud/icones/` pelos dois scripts (`machado-32/40/48/64`, `bomba-32`, com
  os @2x), idênticos pixel a pixel aos aprovados; em `icones.js`, os tamanhos em `TAMANHOS`, `ITEM.machado`,
  `CONSUMIVEL.bomba_fumaca` e `SO_PELO_ID`. O machado vale para todo equipamento com o desenho "machado" (Lamento
  de Gharbad e O Açougueiro também); Redemoinho e Fúria continuam com o sprite; a caveira continua em todos os
  outros papéis (lixeira, retratos, Bestiário, derrota, fome). O jogo não lê nada da pasta de protótipos.
- **Conferido** (`ferramentas/arte/fotografar_itens.mjs`, `SO=machado`, 1500×950 e 1280×720, movimento normal e
  reduzido, sem erro no console): o machado em 32 na ficha, no mercado e na troca de arma da luta, em 40 no corpo e
  na mochila do Inventário, 48 e 64 no saque, o voo ao equipar; a dica com a comparação; comprar (1 → 2 na
  mochila), vender (10 → 9) e recomprar; a bomba na bolsa, na prateleira (comprar: 1 → 2), na janelinha de Itens, no
  quadro do baú (0 → 1 na bolsa) e no voo até a bolsa; `Icones.porDesenho("caveira")` continua vazio e a lixeira
  com a caveira. Testes, gabarito sem diferença, pyflakes, fumaça.
- **Continua registrado:** a escolha de evento que gasta um item mostra o sprite de 1× (`escolhas.js`,
  `meta.gasta`), para a revisão desses componentes; a avaliação da roda de ações, em entrega separada.

### 16/10/2026 — A roda de ações e os ícones pequenos das escolhas (proposta, sem versão)

- **Pedido de Jean:** avaliar o acabamento da roda com a alternativa guardada (sem o lote de ícones recusado) e achar
  por que as escolhas que gastam um item mostram o sprite antigo. Nada integrado: as duas propostas esperam a
  avaliação.
- **A roda:** o jogo já tem o tratamento da HUD 4 pixel desde a 1.92.0; a alternativa (`roda-alternativa.css`, com um
  passe: o foco voltou aos 2 px e a tecla acende em latão) refina mouse, tecla, pressionado e aberto. Fotos atual ×
  alternativa com os mesmos dados em `ferramentas/prototipos/hud/capturas-roda/`.
- **As escolhas:** `escolhas.js` usa o sprite 16×16 em `meta.gasta` (bandagem em `odete_na_estrada`, poção em
  `os_enfermos`; nenhum evento gasta a bomba hoje). Proposta: o papel `Icones.escolha(id, lado)`, só com arquivo
  nativo; amostras em 16 e 24 (`capturas-escolhas/`). Recomendação: 24 px (a bandagem de 16 não lê).
- O registro completo está em `ferramentas/prototipos/hud/LEIA-ME.md` ("A roda de ações e os ícones pequenos das
  escolhas").
- **Guardado para depois da etapa de itens (pedido de Jean):** o estudo visual do Grimório e do livro da capela.

### 16/10/2026 — O nome provisório: The Unquiet (1.100.0)

- **Pedido de Jean:** o novo nome provisório do jogo é **The Unquiet** ("Unquiet", sem o artigo, fica guardado como
  alternativa). **Crônicas da Fenda** era o nome provisório anterior; os registros antigos continuam com ele. O jogo
  segue em português; nada de tradução nesta entrega.
- **Feito:** o nome visível do produto: o título do menu inicial (`rpg/__main__.py`), a aba e o cabeçalho
  (`index.html`), a janela do aplicativo e a mensagem do terminal (`rpg/web/__init__.py`), a interface de terminal
  (`rpg/tui.py`), o aviso de save incompatível (`rpg/migracoes.py`), a descrição da linha de comando; o README e o
  CLAUDE.md registram o nome novo e o anterior. A Fenda do mundo do jogo continua com o nome dela. Não mudaram:
  repositório, pastas, módulos, identificadores, caminhos de saves, a skill `arte-itens-fenda` e os documentos
  históricos.
- **Conferido:** o menu inicial e o cabeçalho em 1500×950 e 1280×720, antes e depois: o título cabe numa linha (552 e
  460 px, a mesma altura), a composição é a mesma (a paisagem aberta, o título, o fio e as opções leves), o foco do
  teclado passa pelas opções, a aba mostra o nome novo, sem erro no console.

### 16/10/2026 — O arco e o cajado em pixel art (proposta, sem versão)

- **Pedido de Jean:** o lote seguinte de itens (`arte-itens-fenda`), só no protótipo: o arco e o cajado, com os
  tamanhos de uso e a comparação no jogo. Retorno no meio: a pedra do cajado precisava parecer presa na madeira.
- **Feito:** os geradores `ferramentas/arte/desenhar_arco_pixel.py` (arco de teixo de uma peça, empunhadura de
  couro, corda clara) e `desenhar_cajado_pixel.py` (carvalho, couro, ponteira de ferro e o cristal azul lapidado,
  cravado numa taça com garras), 32/40/48/64; a proposta em `ferramentas/prototipos/hud/arco-cajado-pixel/`; as fotos
  atual × proposta em `capturas-arco-cajado/`; os cenários ganharam `AMOSTRA` (mercado) e `CLASSE` (vila).
- **Nada mudou no jogo**: o Atacar da roda, o Tiro Duplo, o contrato e o Conjurador continuam com os sprites
  (conferido na roda das duas classes).
- O registro completo está em `ferramentas/prototipos/hud/LEIA-ME.md` ("O arco e o cajado").
- **Falta:** Jean avaliar. Guardados: o estudo do Grimório e do livro da capela (depois da etapa de itens).

### 17/10/2026 — O arco no jogo (1.101.0)

- **Decisão de Jean:** o arco aprovado como apresentado; o cajado volta para um ajuste do encaixe.
- **Feito:** `rpg/web/static/hud/icones/arco-32/40/48/64` (com os @2x) por `ferramentas/arte/desenhar_arco_pixel.py`,
  idênticos pixel a pixel aos da proposta; em `icones.js`, `TAMANHOS.arco` e `ITEM.arco` (os três arcos e os únicos
  Ventre da Tempestade e Sussurro do Vazio). O Atacar do Arqueiro na roda, o Tiro Duplo e o contrato de caça
  continuam com o sprite do jogo.
- **Conferido** (`ferramentas/arte/fotografar_itens.mjs`, `SO=arco`, 1500×950 e 1280×720, sem erro no console): 32 na
  ficha e no mercado, a dica com a comparação, 40 no corpo e na mochila, 64 e 48 no saque, o voo ao equipar; a roda
  com o Atacar no sprite.

### 17/10/2026 — O acabamento da roda de comandos (1.102.0)

- **Decisão de Jean:** o acabamento alternativo dos comandos da roda aprovado (Atacar, Habilidades, Itens, Fugir): a
  tecla encaixada, o fio de latão no mouse, o nome que afunda ao pressionar, a superfície mais escura. O painel que
  abre em Habilidades fica para as três propostas do seletor.
- **Feito:** em `css/15-hud-luta.css`, os botões da roda com os valores efetivos da alternativa apresentada (a folha de
  produção mais `roda-alternativa.css`), sem as regras da janelinha. Dimensões, posição, atalhos e funcionamento os
  mesmos.
- **Conferido:** `ferramentas/prototipos/hud/fotografar_roda.mjs` com `SAIDA` numa pasta à parte, o jogo integrado
  contra o jogo com a folha da alternativa por cima, na mesma luta: parada, mouse, pressionada e a comitiva saem
  pixel a pixel iguais; nos outros estados, a diferença é a do céu e do pulso da carta entre as fotos (e, no
  movimento reduzido, 1 px de posição da roda em uma das duas), e a janelinha, que não mudou.

### 17/10/2026 — Propostas: o encaixe do cajado, os ícones das escolhas em 24 px e o seletor de habilidades

Tudo no protótipo (`ferramentas/prototipos/hud/LEIA-ME.md`, as seções de mesmo nome); nada disso entrou no jogo.
- **O encaixe do cajado:** pelo retorno do Jean ("a base azul do cristal parece ultrapassar o alojamento de madeira"),
  a pedra entra na taça, a borda da frente cobre a base dela, as garras nascem da borda e uma sombra de contato separa
  o cristal da madeira; o resto do desenho é o mesmo. `desenhar_cajado_pixel.py` gravado em `cajado-encaixe/`; antes e
  depois em `capturas-cajado-encaixe/` (os arquivos, conferidos primeiro em 32 e 40, e o jogo). Espera aprovação.
- **Os ícones das escolhas em 24 px:** a poção e a bandagem de 24 (as do topo) e a bomba de 24, agora com a rede de
  cordão, nas opções reais (a bandagem de Odette, os remédios dos enfermos com e sem poção) e numa opção simulada para a
  bomba; a altura das opções não muda. Fotos em `capturas-escolhas-24/`. Espera a conferência da bandagem e da bomba.
- **O seletor de habilidades:** três estruturas para o painel de Habilidades (A lista integrada, B grade compacta,
  C losangos), com os mesmos dados e ícones, o mesmo caminho até o alvo, o motivo da indisponível escrito na linha.
  Fotografadas contra o jogo de hoje na mesma luta, em 1500×950 e 1280×720, com a comitiva, os nomes longos do
  Arqueiro e um teste de 10 habilidades (o jogo tem 7 no máximo); o caminho (abrir, Esc, teclado, alvo, Voltar)
  conferido nas 24 combinações. Recomendação: a B. Espera a escolha do Jean.
- **Continua como está no jogo:** o cajado (sprite antigo), os ícones das escolhas (sprite 16×16), o painel de
  Habilidades. `tests/navegador/cenarios.py` ganhou `NIVEL`, `ESPEC`, `HABILIDADES=todas`, `VIDA` e `REC` no tutorial
  (para as fotos).

### 17/10/2026 — Proposta: o seletor de habilidades D, faixas de tinta

- **Decisão de Jean:** a direção do seletor é a referência D (faixas de tinta e gravura); ela passa à frente das
  propostas A, B e C, que ficam guardadas para comparação. As integrações já aprovadas continuam autorizadas, em
  entregas separadas.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/LEIA-ME.md`, "O seletor de habilidades D"): o seletor da
  largura da arena, embaixo dela, por cima do registro; as habilidades em faixas carvão de pontas irregulares (três
  formas fixas pela posição), inclinadas 2°, em duas colunas na ordem das teclas; a examinada em marfim com a tecla
  em latão; foco do teclado com marca própria; pressionado, indisponível com o motivo escrito; "Habilidades" pequeno e
  "Esc · Voltar"; a entrada curta das faixas, sem atrasar a escolha; as setas andam pelas faixas. Sem a gravura do
  capacete.
- **Conferido:** o jogo de hoje e o D com os mesmos dados (três classes no nível 12 e um teste de 10 habilidades), em
  1500×950, 1920×1080 e 1280×720, com a comitiva, a dica, a indisponível, a mira e o Voltar; abrir e fechar não mexe
  nas cartas nem na rolagem; cliques rápidos, clique duplo, tecla segurada, clique durante a entrada e movimento
  reduzido. Fotos em `capturas-seletor-d/`.
- **Continua no jogo:** o seletor de hoje. Nenhuma regra, custo, habilidade, talento ou mira mudou. Espera a avaliação.

### 17/10/2026 — Proposta: a D refinada (bordas das faixas e fundo do seletor)

- **Decisão de Jean:** a D aprovada como base; antes de integrar, uma versão com pontas mais orgânicas (tinta e papel
  gasto) e um fundo integrado à página, com a D atual intacta para comparar.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/LEIA-ME.md`, "A D refinada"): `seletor/d2-faixas.css` por cima
  da D; as faixas recortadas por máscara de três peças (pontas desenhadas em SVG, escaladas só pela altura, e o meio
  esticado), três pontas de cada lado combinadas pela posição; o fundo com a mesma superfície da leitura da página,
  opaco e sem sombra, com um fio fino embaixo. O cenário tutorial ganhou `NIVEL_LUTA`.
- **Conferido:** D atual e refinada com os mesmos dados e o registro real por baixo (uma rodada jogada, a mesma
  semente), Guerreiro, Mago e Arqueiro, 1500×950 e 1280×720, parado, destaque, indisponível e movimento reduzido; o
  caminho, o foco e as áreas de clique iguais. Fotos em `capturas-seletor-d2/`.
- **Continua no jogo:** o seletor de hoje. Espera a escolha entre a D atual e a refinada.

### 17/10/2026 — O seletor de habilidades no jogo (1.103.0)

- **Decisão de Jean:** a D refinada aprovada como seletor padrão, com o visual e o funcionamento apresentados, e a
  meia linha do registro na borda de baixo resolvida.
- **Feito:** `app/escolhas.js` (a janelinha de Habilidades vira o seletor de faixas: posição embaixo da arena, duas
  colunas, título e "Esc · Voltar", marcação separada, setas, foco ao abrir pela tecla, dica ao lado, `bordaLimpa`)
  e `css/18-seletor-habilidades.css` (faixas, pontas, fundo, estados, entrada). A janelinha de Itens não mudou.
  Nenhuma regra, custo, habilidade, flecha ou sorteio mudou (gabarito idêntico). O componente está descrito em
  `docs/ARQUITETURA.md` ("O seletor de habilidades"), para reaproveitar se outro seletor pedir; o estilo não vai para
  outras telas por enquanto.
- **Conferido:** as três classes com comitiva e o teste de 10 habilidades, 1500×950 e 1280×720, registros de alturas
  diferentes; interações, mira, Voltar e reabrir; sem salto e sem texto cortado na borda. Capturas em
  `ferramentas/prototipos/hud/capturas-seletor-integrado/`.
- **Próximo:** o menu de Itens e os lotes de arte ficam para entregas posteriores.

### 17/10/2026 — Correções da luta e do mercado (1.103.1, 1.103.2, 1.104.0) e o protótipo de Itens

- **Avisos de combate acima da moldura (1.103.1):** os números, as faixas ("AAARGH!", o nome do golpe, "fraqueza!")
  e os selos de estado nasciam dentro da carta, e o palco (`overflow: hidden`) os cortava na moldura. Agora nascem
  numa camada da página (`.avisos-luta`, em `batalha.js`) que acompanha a carta, por cima da moldura e dentro da
  janela, sem pegar o mouse; somem como antes e todos saem com a luta. O cenário, as cartas e os estados
  permanentes continuam recortados. Duração, ordem, sons e quantidade iguais.
- **Cliques seguidos (1.103.2):** a causa do "abrir e fechar Habilidades rápido não responde": o navegador conta os
  cliques seguidos (2, 3...), e a proteção contra clique duplo (`Gesto`, `app/nucleo.js`) descartava todo clique
  com contagem 2 ou mais nos controles da roda; o botão só voltava a responder quando a contagem zerava (~0,5 s).
  Os botões que só abrem e fecham uma janelinha na mesma tela (Habilidades e Itens, `data-alterna`) aceitam cliques
  seguidos; o resto da proteção fica (o clique duplo numa habilidade continua sendo uma escolha só). Pelo retorno do
  Jean no meio da entrega, a mesma família de problema na venda e na comitiva: a venda da mochila ganhou a fila da
  compra de suprimentos (pela peça, não pela posição: clicar sem parar vende uma peça por clique), e as cartas ✉
  tocadas no meio de outra conversa esperam o próximo menu do lugar, na ordem (antes caíam no aviso de "lugar
  seguro"). `tests/navegador/cliques_seguidos.mjs` confere os três.
- **Descrição da habilidade dentro do seletor (1.104.0):** a dica lateral saiu das faixas; a descrição da examinada
  (mouse ou teclado) fica embaixo da coluna dela, num lugar reservado ao abrir (nada pula ao trocar), com as
  informações da dica de antes e o motivo; em janela baixa, uma área só embaixo das duas colunas (em duas partes, com
  o "Esc · Voltar" na linha do título), sem fazer a lista rolar com 7 nem com 10 habilidades. As outras telas
  continuam com as dicas de sempre.
- **Protótipo:** o menu de Itens em faixas (`ferramentas/prototipos/hud/LEIA-ME.md`, "O menu de Itens em faixas").
  Espera a avaliação; o menu de Itens do jogo não mudou.

### 17/10/2026 — O menu de Itens no jogo (1.105.0) e a venda com a grade parada (1.105.1)

- **Menu de Itens (1.105.0):** o protótipo aprovado entrou como apresentado: o mesmo seletor de faixas de
  Habilidades (`abrirJanela`, `.roda-janela.seletor`, `data-tipo`), com a quantidade à direita (na cor normal no item
  que não serve), o motivo do motor na faixa, a descrição embaixo da coluna, a troca de arma com a ficha e "turno", a
  poção indo para a mira dos aliados como antes, e "Nada na bolsa serve agora." quando nada serve. A janelinha antiga
  ao lado dos botões saiu. As fotos do jogo saem iguais às da proposta (comparadas pixel a pixel).
- **O Tônico** diz só o recurso da classe ("Recupera metade do Vigor / do Foco / da Mana."): `itens.descricao`, com
  o nome do recurso e o artigo vindos de `classes.py` (`artigo_recurso`). O gabarito mudou só nesse texto.
- **A venda (1.105.1):** a causa da instabilidade era a grade desenhada na ordem da mochila do motor (as peças
  escorregavam a cada venda e a fila adivinhava a peça pela assinatura, que não distingue peças iguais). Agora a
  aba Vender guarda um arranjo da visita: cada peça tem uma ficha e um espaço fixo; vender esvazia o espaço, a
  recompra e a peça que sai do corpo vão para o primeiro vazio, e sair do mercado volta à ordem de sempre.
- **Conferido:** Itens nas três classes (com comitiva, uma rodada antes), bolsa variada, poucos itens e vazia, em
  1500×950 e 1280×720, mouse, teclado, movimento reduzido, registro por baixo sem linha cortada
  (`fotografar_itens_faixas.mjs` → `capturas-itens-jogo/`); abrir e fechar rápido e a troca com Habilidades, e a
  venda (rápida, clique duplo, clique no vazio, troca de aba com venda a caminho, recompra, equipar, arrastar, sair)
  em `tests/navegador/cliques_seguidos.mjs`.
- **Esperando o Jean:** o encaixe do cajado (a revisão de 17/10 em `cajado-encaixe/` e `capturas-cajado-encaixe/`)
  e os ícones das escolhas em 24 px. Os próximos lotes de arte ficam para a etapa seguinte.

### 17/10/2026 — O cajado no jogo (1.106.0)

- **Decisão de Jean:** a revisão do encaixe (`cajado-encaixe/`) aprovada, sem outra rodada.
- **Entrou:** `cajado-32/40/48/64` (com os @2x) em `hud/icones/`, gravados por `desenhar_cajado_pixel.py`, idênticos
  byte a byte aos da proposta; `TAMANHOS.cajado` e `ITEM.cajado` em `icones.js` (os Cajados e o único Cajado da
  Peste). O Atacar do Mago na roda e o traço Conjurador dos inimigos continuam com o sprite do jogo.
- **Conferido** (`fotografar_itens.mjs`, SO=cajado, 1500×950 e 1280×720): ficha 32, mercado e dica de comparação 32,
  Inventário 40 (corpo e mochila), cartão do saque 64 e 48, voo ao equipar; a roda com o sprite.

### 17/10/2026 — Proposta: o orbe e o livro do Mago (protótipo, sem versão)

- **Pedido de Jean:** o orbe e o livro de equipamento pela skill `arte-itens-fenda`, só no protótipo.
- **Feito:** `ferramentas/arte/desenhar_orbe_pixel.py` (a esfera de vidro violeta na taça de latão com três garras,
  pescoço e pé; a reflexão separada da luz de dentro, sem aura) e `desenhar_livro_pixel.py` (o livro fechado de couro
  violeta, lombada com nervos, corte com a espessura das páginas, cantos e fecho de latão, sem símbolos), 32/40/48/64,
  gravados em `ferramentas/prototipos/hud/orbe-livro-pixel/`; atual × proposta em `capturas-orbe-livro/`, nas duas
  janelas (mercado, ficha, dica, Inventário, saque, voo, telas inteiras).
- **Continua como está no jogo:** o orbe e o livro com o sprite antigo; o Grimório da interface e o livro da capela
  (outra etapa). Espera a avaliação do Jean.

### 17/10/2026 — O orbe no jogo (1.107.0)

- **Decisão de Jean:** o orbe aprovado como apresentado; o livro precisa de outro conceito (o fechado lembra uma
  agenda de couro com fecho: pesado e genérico).
- **Entrou:** `orbe-32/40/48/64` (com os @2x) em `hud/icones/`, gravados por `desenhar_orbe_pixel.py`, idênticos byte
  a byte aos da proposta; `TAMANHOS.orbe` e `ITEM.orbe` em `icones.js` (a arma Orbe, o apoio Foco Arcano e o único
  Olho do Abismo; nenhum outro papel usa o desenho "orbe").
- **Conferido** (`fotografar_itens.mjs`, SO=orbe, 1500×950 e 1280×720): ficha 32, mercado e dica de comparação 32,
  Inventário 40 (corpo e mochila), cartão do saque 64 e 48, voo ao equipar; o livro e a varinha continuam com o sprite.

### 17/10/2026 — Proposta: o grimório entreaberto (o segundo conceito do livro; protótipo)

- **Pedido de Jean:** o livro fechado lembra uma agenda de couro com fecho; outra proposta: um grimório entreaberto
  em três quartos, fino, couro violeta apagado com a beira irregular, páginas envelhecidas com poucas marcas
  abstratas, uma fita como marcador e ferragens discretas, priorizando 32 e 40.
- **Feito:** `ferramentas/arte/desenhar_grimorio_pixel.py` (um modelo 3D do livro rasterizado em cada grade),
  gravado em `ferramentas/prototipos/hud/livro-entreaberto/`; o fechado intacto em `orbe-livro-pixel/`; as três
  versões (o jogo, o fechado, o entreaberto) em `capturas-livro/`, nas duas janelas.
- **Continua como está no jogo:** o livro com o sprite antigo. Espera a escolha do Jean.

### 17/10/2026 — Proposta: o grimório aberto, com duas páginas (o terceiro conceito do livro; protótipo)

- **Pedido de Jean:** o entreaberto parecia uma folha apoiada numa capa levantada; outra geometria: o livro aberto em
  diagonal, duas páginas num "V" suave ligadas pela dobra escura até a lombada, a curva das páginas em poucos planos,
  um bloco de folhas fino, a capa violeta na beira, a fita saindo entre as folhas, anotações numa página e um diagrama
  na outra (que funcione em 32 e 40).
- **Feito:** `ferramentas/arte/desenhar_grimorio_aberto_pixel.py` (um modelo 3D de polígonos planos rasterizado em
  cada grade), gravado em `ferramentas/prototipos/hud/livro-aberto/`; o fechado e o entreaberto intactos; as quatro
  versões (o jogo e os três candidatos) em `capturas-livro/`, nas duas janelas.
- **Continua como está no jogo:** o livro com o sprite antigo. Espera a escolha do Jean.

### 17/10/2026 — Proposta: o grimório de estudo (a pose do entreaberto pela referência do Jean; protótipo)

- **Pedido de Jean:** gostou mais do entreaberto que do aberto de duas páginas; refazer pela skill, se espelhando numa
  referência que ele mandou (capa gasta levantada, lombada redonda, bloco de folhas, página com anotações e diagrama
  de anéis, fita pendurada), com a angulação do entreaberto.
- **Feito:** `ferramentas/arte/desenhar_grimorio_estudo_pixel.py`, gravado em `ferramentas/prototipos/hud/livro-estudo/`;
  os candidatos anteriores intactos; as cinco versões em `capturas-livro/` (e os pares entreaberto × estudo), nas
  duas janelas.
- **Continua como está no jogo:** o livro com o sprite antigo. Espera a escolha do Jean.

### 17/10/2026 — Proposta: o grimório fechado da nova referência (só o 64; protótipo)

- **Pedido de Jean:** seguir com o grimório fechado de uma nova referência, do zero e pela skill, só em 64 (a pose
  diagonal de cima em três quartos, a capa violeta com espessura e planos de luz, a lombada redonda com reforços, o
  bloco de páginas envelhecido, o fecho lateral, o latão envelhecido e o crescente só como decoração); as propostas
  anteriores ficam como histórico.
- **Feito:** `ferramentas/arte/desenhar_grimorio_fechado_pixel.py`, gravado em
  `ferramentas/prototipos/hud/livro-fechado-ref/livro-64.png` (e o @2x); a prancha ao lado do escudo, do cajado e do
  orbe e o cartão do saque nas duas janelas em `capturas-livro-fechado/` (`fotografar_livro_fechado.mjs`).
- **Continua como está no jogo:** o livro com o sprite antigo. Espera a avaliação do 64 antes de 32, 40, 48 ou da
  integração.

### 17/10/2026 — Proposta: o acabamento do 64 do grimório fechado (protótipo)

- **Pedido de Jean:** a direção do fechado aprovada; antes dos outros tamanhos, refinar no 64 o volume e a luz da capa
  (planos para o couro abaulado, brilho nas arestas voltadas para a luz, sem faixa clara contínua, a sombra de contato
  mantida) e pôr o emblema no plano da capa, guardando o 64 de antes.
- **Feito:** `ferramentas/arte/desenhar_grimorio_fechado_pixel.py` (a capa em almofada com três planos, o fio da
  cabeça, o sulco da dobradiça, o brilho da lombada em trechos, o emblema em perspectiva com o crescente à mão),
  gravado em `ferramentas/prototipos/hud/livro-fechado-acabamento/`; o de antes intacto em `livro-fechado-ref/`; o
  antes × depois (em 1× e ampliado, ao lado do escudo, do cajado e do orbe, e no cartão do saque nas duas janelas) em
  `capturas-livro-fechado/` (`fotografar_livro_fechado.mjs` e `comparar_livro_fechado.py`).
- **Continua como está no jogo:** o livro com o sprite antigo. Espera a avaliação do 64 antes de 32, 40, 48 ou da
  integração.

### 17/10/2026 — Proposta: o emblema corrigido do grimório fechado (só o 64; protótipo)

- **Pedido de Jean:** a capa e a luz da revisão aprovadas (o corpo fica exatamente igual); refazer só o emblema a
  partir do da primeira proposta (crescente legível, folga entre crescente, ponto e contorno, orientação estilizada
  conversando com a capa, latão aplicado com luz discreta).
- **Feito:** o losango inclinado com lados em degraus regulares e o crescente da primeira proposta, inclinado, em
  `ferramentas/prototipos/hud/livro-fechado-emblema/`; o corpo conferido pixel a pixel contra a revisão (só o emblema
  e o sulco dele mudam); a revisão e o primeiro 64 intactos; as comparações `emblema-*` em `capturas-livro-fechado/`.
- **Continua como está no jogo:** o livro com o sprite antigo. Espera a avaliação do 64 antes de 32, 40, 48 ou da
  integração.

### 17/10/2026 — Proposta: o grimório fechado em 32, 40, 48 e 64 (protótipo)

- **Pedido de Jean:** o crescente do 64 pela correção dele no Aseprite (a ponta de baixo para dentro da abertura),
  também no gerador; depois as versões próprias de 32, 40 e 48 com o emblema simplificado por tamanho; os quatro sobre
  o carvão e nos usos reais (ficha, Inventário, mercado, saque, voo), nas duas janelas; tudo no protótipo.
- **Feito:** a correção lida da captura 8× (3 pixels) e posta no desenho do crescente; o 64 gerado confere com ela; o
  32, o 40 e o 48 desenhados na própria grade (o mesmo corpo, emblemas por tamanho) em
  `ferramentas/prototipos/hud/livro-fechado-tamanhos/`; as fotos e as pranchas em `capturas-livro-tamanhos/`
  (`fotografar_livro.mjs` com a versão "tamanhos" e `comparar_livro_tamanhos.py`); as pastas anteriores intactas.
- **Continua como está no jogo:** o livro com o sprite antigo. Espera a avaliação dos tamanhos pequenos antes da
  integração.

### 17/10/2026 — 1.108.0: o grimório fechado no jogo (aprovado e integrado)

- **Pedido de Jean:** o grimório fechado aprovado nos quatro tamanhos (com a correção do crescente); integrar
  exatamente esses desenhos, sem ajuste de arte, e conferir nos usos reais.
- **Entrou:** `rpg/web/static/hud/icones/livro-32/40/48/64.png` e os @2x, gravados por
  `ferramentas/arte/desenhar_grimorio_fechado_pixel.py` (sem pasta, grava no jogo), idênticos byte a byte aos
  aprovados em `ferramentas/prototipos/hud/livro-fechado-tamanhos/`; `Icones`: `TAMANHOS.livro` e `ITEM.livro`.
- **Alcance:** o desenho "livro" do equipamento: a arma Grimório (todos os materiais), o apoio Tomo e o único Tomo
  do Nome Esquecido. Ficam como estão (outros papéis, cada um na sua etapa): o talento Mente Vasta (o sprite "livro" na
  árvore), os atalhos do Diário e do Grimório (desenhos próprios), a roda da luta e o livro da capela (desenhado na
  cena). Regras, atributos, preços, estoque, recompensas e animações não mudaram.
- **Conferido** (`fotografar_itens.mjs`, SO=livro, que agora também vende, recompra e guarda o achado): ficha e mercado
  em 32 (venda, dica de comparação, vendido em Recomprar e recomprado), corpo e mochila do Inventário em 40, cartão do
  saque em 64 e 48, voo ao equipar a partir do 48 e o achado guardado na mochila em 40; em 1500×950 e 1280×720, sem
  erro no console.
- **Candidatos antigos do livro:** histórico, não aprovados (o fechado de antes, o entreaberto, o aberto e o de
  estudo); o aprovado é o grimório fechado.
- **Próximo:** um teste com Aseprite via MCP numa sessão local; nenhum outro lote começou.

### 16/10/2026 (data do computador local) — Aseprite pelo MCP e a proposta da varinha (protótipo, sem versão)

- **Onde:** feito primeiro na cópia local `C:\Users\Jean Wress\Desktop\packs\MEGABRAIN` (1.108.0, sem `.git`) e
  depois transferido para o clone `C:\Users\Jean Wress\Desktop\packs\teste2` (branch `claude/tender-einstein-tx3tjl`,
  a partir de `c98d02f`). A comparação das duas pastas (fora `.git`, `__pycache__` e `node_modules`): 73 arquivos só
  em MEGABRAIN, todos desta proposta, copiados e conferidos por sha256; um arquivo com conteúdo diferente (esta
  continuidade: só esta entrada); nenhum arquivo só no clone; 408 arquivos iguais a menos do fim de linha (o clone usa
  `core.autocrlf=true`, do Git do sistema). Nenhuma diferença ficou sem explicação; MEGABRAIN foi preservada inteira.
- **O teste da conexão:** o servidor `aseprite` (aseprite-mcp 0.6.0, registro em
  `C:\Users\Jean Wress\Tools\aseprite-mcp-INSTALACAO.md`) responde com o Aseprite 1.3.18.6 da Steam; um 1.3-rc2 antigo
  aberto ao mesmo tempo conectava sem responder. O arquivo do teste está em `C:\Users\Jean Wress\Tools\aseprite-mcp-teste\`.
- **Pedido de Jean:** o primeiro item real por esse fluxo: uma proposta de Varinha (curta e esguia, madeira com
  afilamento, empunhadura discreta, cristal âmbar pequeno num encaixe de metal envelhecido, sem aura), 32 e 64, só no
  protótipo; não mexer na skill compartilhada antes de avaliar o fluxo.
- **Feito:** `ferramentas/prototipos/hud/varinha-aseprite/` (os `.aseprite` editáveis, os PNGs e @2x, as pranchas e as
  fotos do jogo atual × proposta em 1500×950 e 1280×720: ficha e mercado em 32, cartão do saque em 64), com
  `fotografar_varinha.mjs` e `comparar_varinha.py`. O `LEIA-ME.md` da pasta lista cada operação feita pelo MCP, as
  limitações do conector (camadas, contorno, paleta, leitura sem alfa) e a avaliação. O Playwright foi instalado fora do
  jogo, em `C:\Users\Jean Wress\Tools\playwright`.
- **Decisão de Jean:** o 32 aprovado como está; o 64 só com um refinamento localizado no cristal e no encaixe; 40 e
  48 a fazer na própria grade; integração só depois da avaliação dos quatro tamanhos. Antes, testar um conector com
  controle de camadas (`rezaahmadn/aseprite-mcp-bridge`); a instalação e a retomada estão em
  `C:\Users\Jean Wress\Tools\aseprite-mcp-bridge-INSTALACAO.md`.
- **Continua como está no jogo:** a varinha com o sprite 16×16; `icones.js`, a skill e as regras não mudaram.

### 16/10/2026 (data do computador local) — O conector com camadas e a varinha em 32, 40, 48 e 64 (protótipo, sem versão)

- **Onde:** clone `teste2`, branch `claude/tender-einstein-tx3tjl`, sobre `d0b8af4` (1.108.0 na produção). Conector
  `aseprite-bridge` (rezaahmadn/aseprite-mcp-bridge, extensão 1.0.0), Aseprite 1.3.18.6 da Steam.
- **Pedido de Jean:** a etapa 3 do registro do conector (o teste de camadas), com a verificação dos limites do
  `put_pixels`; se passasse, a varinha: o 32 aprovado intacto, no 64 só a pedra âmbar e o encaixe (pedra sólida com
  facetas, assentada na taça, sem leitura de chama), o 40 e o 48 nativos, editáveis em camadas, fotos nos usos reais.
- **O conector:** camadas funcionam pelas ferramentas (criar, desenhar e ler pelo nome, renomear, reordenar, esconder,
  duplicar, apagar, desfazer/refazer, salvar/reabrir; a imagem composta chega visível). O `put_pixels` tem dois
  defeitos medidos: descarta em silêncio o pixel fora da cel (cel do lápis, deslocada ou fora da tela; coordenadas são
  do documento) e não gera desfazer. Solução verificada: `varinha-aseprite/auxiliares/pintar.lua` (imagem nova que
  cobre a cel e a tela, numa transação; recusa e lista o que fica fora da tela; um passo de desfazer). `io.open` e
  `saveCopyAs` para PNG num `execute_script` travaram o conector por 60 s: dados por `dofile`, PNG por `export_png`.
  Detalhes no `LEIA-ME.md` da proposta ("Rodada 2") e no registro do conector (fora do repositório).
- **Feito:** `ferramentas/prototipos/hud/varinha-aseprite/rodada2/`: os quatro `.aseprite` com 8 camadas (pomo,
  empunhadura, anel, haste, taca, pedra, garras, contorno), os PNGs, os @2x exatos, as pranchas e as fotos. O 32 é o
  aprovado pixel a pixel; no 64 só mudaram 66 pixels, da taça para cima (a pedra virou uma pedra lapidada quadrada de
  quatro faces, com o canto afundado na taça e uma garra); 40 e 48 na própria grade (pedra de 4×4 e 5×5). Listas de
  `auxiliares/varinha_r2.py`, escritas no Aseprite pelo `pintar.lua`/`montar.lua`. `fotografar_varinha.mjs` ganhou o
  Inventário, o voo e a escolha de versões; `comparar_varinha.py rodada2` monta as pranchas. A primeira rodada ficou
  intacta.
- **Conferido:** cada `.aseprite` reaberto: 8 camadas, composto igual ao PNG salvo e à prévia; fotos atual × rodada 1
  × rodada 2 em 1500×950 e 1280×720: ficha e mercado (Vender e dica) em 32, corpo e mochila do Inventário em 40, cartão
  do saque em 64 com o "você usa" em 48, o voo ao equipar; o relatório confirma arquivo e tamanho em cada lugar; sem
  erro no console.
- **Verificações:** `unittest`: 603 testes, 1 falha (o gabarito), 1 pulado. `tests.gabarito`: as 18 partidas
  DIFERENTE, e igual num checkout limpo de `c98d02f` (1.108.0): é do ambiente deste Windows, não desta entrega
  (suspeita não confirmada: o fim de linha CRLF do checkout, `core.autocrlf=true`). `pyflakes` não está instalado
  (`py_compile` e `node --check` nos arquivos novos). `fumaca.mjs` não roda neste Windows: calcula a raiz com
  `new URL(import.meta.url).pathname` (vira `/C:/Users/Jean%20Wress/...`, `cwd` inválido) e chama `python3`. Nada em
  `rpg/` mudou.
- **A avaliar com Jean:** a pedra quadrada do 64 (e a do 40 e do 48) tem outro corte que a ponta alongada do 32
  aprovado; em tamanho real as duas leem como "ponta âmbar". A de 4×4 do 40 é quase só um bloco com reflexo.
- **Continua como está no jogo:** a varinha com o sprite 16×16; `icones.js`, regras e versão não mudaram. Próximo:
  a avaliação dos quatro tamanhos pelo Jean; integração só depois dela.

### 16/10/2026 (data do computador local) — Varinha: o mesmo perfil de haste nos quatro tamanhos (protótipo, sem versão)

- **Feedback de Jean:** gostou da varinha; pediu a haste uniforme nos quatro tamanhos, na direção do 40 (reta, com
  afunilamento suave), sem barrigas nem mudanças de lado no trecho avermelhado, podendo ajustar o 32 aprovado;
  conferir a silhueta numa cor só e depois o desenho; preservar materiais, paleta, enquadramento e o resto.
- **Feito:** uma regra só (`varinha_r2.py`): a borda da sombra da haste reta do anel à taça, a haste começando na
  largura do anel e afinando num degrau só, do lado aceso, a ~53% do comprimento (32 3→2, 40 3→2, 48 4→3, 64 5→4),
  sem degrau de lado na entrada da taça. Mudaram: no 32, 8 pixels da haste e do contorno; no 48, a haste e 4 pixels
  do gargalo da taça; no 64, a haste (a barriga perto do anel e o zigue-zague do eixo saíram). O 40 não mudou.
  Pintado no Aseprite pelo `pintar.lua`, nos mesmos arquivos de `varinha-aseprite/rodada2/`.
- **Conferido:** a silhueta numa cor só e o desenho completo, antes e depois (`rodada2/capturas/haste-*.png`); os
  `.aseprite` reabertos (8 camadas, composto igual ao PNG e à prévia); @2x refeitos; fotos da rodada 2 refeitas em
  1500×950 e 1280×720 (ficha e mercado 32, Inventário 40, saque 64 e 48, voo), sem erro no console.
- **Continua como está no jogo:** a varinha com o sprite 16×16. Próximo: a avaliação do Jean; integração só depois.

### 16/10/2026 (data do computador local) — Varinha: a pedra do 32 no corte compacto (protótipo, sem versão)

- **Decisão de Jean:** a haste aprovada nos quatro tamanhos. Pedido: só o cristal do 32 no corte compacto do 40, 48
  e 64 (sem a ponta alongada; reflexo, âmbar e separação do suporte mantidos); nada mais muda.
- **Feito:** a pedra quadrada de 4×4 do 40 no 32 (`PEDRA32`), com o canto na taça, o reflexo e a garra de bronze da
  taça por cima. Só 28 pixels mudaram (pedra e contorno dela); haste, empunhadura, taça e os outros tamanhos intactos.
- **Conferido:** `.aseprite` reaberto (8 camadas, composto igual ao PNG), @2x, antes e depois em 1× sobre o carvão e no
  jogo (ficha, Vender e dica, 1500×950 e 1280×720), sem erro no console (`rodada2/capturas/pedra-32-*.png`).
- **Continua como está no jogo:** a varinha com o sprite 16×16. Próximo: a avaliação do Jean; integração só depois.

### 16/10/2026 (data do computador local) — Gabarito e fumaça no Windows (só testes, sem versão)

- **Onde:** clone `teste2`, Windows 10, Python 3.12.4, Node 22.15.0 (1.108.0 na produção). Feito sobre `9a13a35`;
  como a varinha ganhou `740de4e` e `451ff11` no meio, a correção foi reaplicada por cima deles (cherry-pick, juntando os dois
  registros desta continuidade) e integrada em `claude/tender-einstein-tx3tjl` por `merge --ff-only`. A varinha não
  entra neste commit.
- **Pedido:** as duas verificações do `CLAUDE.md` que não rodavam neste Windows (registro anterior): o gabarito
  DIFERENTE num checkout limpo e o `fumaca.mjs`; corrigir sem atualizar `tests/gabarito.json`.
- **Causa do gabarito:** não era o fim de linha. A pasta dos saves aparece no texto ("Jogo salvo em ...",
  "Registro parcial da partida: ...", "Registro da partida salvo em: ..."), que o `dizer` quebra em 76 colunas
  **antes** de o gravador trocar a pasta por `<PASTA>`. Nas transcrições de referência (Linux) a pasta é `/tmp/tmp` e
  oito letras (16 caracteres); aqui, `C:\Users\JEANWR~1\AppData\Local\Temp\tmp...` (cerca de 48) e com `\`: a linha
  quebra noutro ponto, o caminho se parte entre duas linhas, a troca falha e o nome aleatório da pasta entra na
  transcrição (e o `\rob.json` no lugar de `/rob.json`). Só as 18 partidas do robô salvam; as 6 da comitiva já batiam.
- **Feito:** `tests/gabarito.py`: o `Gravador` recebe a pasta e, no `dizer`, troca o caminho (com o resto dele, em
  barras normais) por `PASTA = "/tmp/tmp_PASTA__"`, do tamanho da pasta temporária do Linux; depois da quebra, `PASTA`
  vira `<PASTA>`. `tests/navegador/fumaca.mjs`: a raiz por `fileURLToPath`; e nos três roteiros de
  `tests/navegador` (`fumaca`, `cliques_seguidos`, `redimensionar`) o Python por `PYTHON=<executável>`, com `python`
  no Windows e `python3` nos outros. Nada em `rpg/` mudou (por isso sem versão).
- **Verificações, todas executadas só neste Windows:** `python -m tests.gabarito`: OK, as 24 partidas, com o
  `gabarito.json` intacto (os hashes de referência vieram do Linux; agora o Windows os reproduz). `unittest`: 603
  testes, OK (1 pulado). `fumaca.mjs`, `cliques_seguidos.mjs` e `redimensionar.mjs`: "tudo certo" (com
  `PLAYWRIGHT_BROWSERS_PATH` e `PLAYWRIGHT_MODULO` de `C:\Users\Jean Wress\Tools\playwright`); a fumaça repetida sobre
  `740de4e`; gabarito, `unittest` e pyflakes repetidos sobre `451ff11`. `python -m pyflakes rpg tests` (pyflakes 4.0.3, instalado
  com `pip install --user` no Python do sistema, o que o `CLAUDE.md` usa; o projeto não tem venv nem lista de
  desenvolvimento): só os 9 avisos de import de `rpg/eventos/__init__.py`, que o `CLAUDE.md` manda ignorar.
- **Não verificado:** o código novo do gabarito e dos roteiros não rodou no Linux nesta entrega. Pela construção, lá
  o marcador tem o mesmo tamanho da pasta real e o resultado deve ser o de antes; a próxima sessão na nuvem confirma
  com `python -m tests.gabarito` e a fumaça.
- **Em aberto, para uma entrega própria:** os roteiros de foto em `ferramentas/` (`arte/` e `prototipos/`), 29
  arquivos, ainda chamam `python3` direto (o `fotografar_varinha.mjs` já usa `PYTHON` ou `python`). Ficaram fora desta
  correção de propósito.

### 16/10/2026 (data do computador local) — 1.109.0: a varinha no jogo (aprovada e integrada)

- **Decisão de Jean:** a varinha aprovada nos quatro tamanhos, na versão de `451ff11` (a haste uniformizada e a pedra
  compacta do 32); integrar sem ajuste de desenho; guardar a fonte editável; registrar o fluxo na skill.
- **Entrou:** `rpg/web/static/hud/icones/varinha-32/40/48/64.png` e os @2x, exportados por
  `ferramentas/arte/exportar_aseprite.py varinha` das fontes finais em `ferramentas/arte/aseprite/varinha/` (os quatro
  `.aseprite` com as 8 camadas), idênticos byte a byte aos aprovados de `varinha-aseprite/rodada2/` (e o `--conferir`
  reproduz os oito); `Icones`: `TAMANHOS.varinha` e `ITEM.varinha` (o papel de equipamento, como o cajado, o orbe e o
  grimório; pedido sem arquivo igual, o mais perto).
- **Alcance:** só a arma-base Varinha do Mago (`rpg/itens.py`, desenho "varinha"), em todos os materiais e afixos.
  Nenhum único, apoio, habilidade, talento, ação da roda ou outro objeto usa o desenho "varinha" (procurado em `rpg/`);
  o sprite 16×16 continua em `sprites-dados.js`. Na luta, o Atacar do Mago continua com o sprite do cajado.
- **Fonte e fluxo:** `ferramentas/arte/aseprite/LEIA-ME.md` (as fontes, como exportar, o `pintar.lua`, que veio do
  protótipo, e os defeitos do `put_pixels`); `ferramentas/arte/exportar_aseprite.py` (Aseprite por `ASEPRITE`, PATH ou
  instalação comum; o 1× pela linha de comando, o @2x pela duplicação exata). O protótipo da varinha ficou como
  histórico (nenhum script dele grava no jogo; o LEIA-ME diz o papel de cada um). A skill `arte-itens-fenda` ganhou:
  um objeto só em todos os tamanhos (simplificação × mudança de construção), a silhueta numa cor só antes da cor,
  "Desenhar no Aseprite (pelo MCP)" e o exemplo da varinha em `exemplos.md`.
- **Conferido** (`ferramentas/arte/fotografar_itens.mjs`, `SO=varinha`, que agora também roda no Windows e conhece
  a varinha): ficha e mercado em 32 (Vender, dica de comparação, vendido em Recomprar e recomprado), corpo e mochila do
  Inventário em 40 (e o achado guardado na mochila em 40), cartão do saque em 64 com o equipado em 48, voo ao equipar a
  partir do 48, a roda da luta; em 1500×950 e 1280×720, sem erro no console. Preços (7 na venda), atributos, estoque,
  regras e animações não mudaram (em `rpg/`, só `icones.js`, a versão e os PNGs).
- **Verificações:** `unittest` 603 OK (1 pulado); `tests.gabarito` OK com o `gabarito.json` intacto; `pyflakes` só com
  os avisos de `rpg/eventos/__init__.py`; `fumaca.mjs`, `cliques_seguidos.mjs` e `redimensionar.mjs`: "tudo certo".
  Tudo neste Windows. `tests.equilibrio`/`replay` não rodaram (nenhum número mudou).
- **Próximo:** nenhum item começou; parar aqui.

### 16/10/2026 (data do computador local) — Proposta: o peitoral e as botas de couro em 32 e 64 (protótipo, sem versão)

- **Pedido de Jean:** o próximo lote, só no protótipo: o peito e os pés de couro em 32 e 64, no Aseprite pelo MCP
  com o `pintar.lua`; silhueta numa cor só antes da cor; comparar atual × candidato no jogo nas duas janelas; parar
  para a avaliação (sem integrar, sem versão, sem outras peças; 40 e 48 depois da aprovação).
- **Os dados:** `gibao` = Gibão de Couro, Capa de Patrulha e Colete Acolchoado (o peito do Arqueiro) e o único Pele do
  Penitente; `bota` = Bota de Caça e o único Botas do Andarilho Morto; materiais de couro (Rasgado a Rúnico). O
  sprite `bota` também é o estado Iniciativa (outro papel). Contradições anotadas para o Jean: a Capa de Patrulha
  com um desenho de colete; Tachonado e Rúnico sem tachas nem runas no desenho comum.
- **Feito:** `ferramentas/prototipos/hud/couro-aseprite/`: os `.aseprite` em camadas (o gibão com 8, as botas com 9),
  os PNGs e @2x de `rodada1/`, as pranchas, as fotos, os logs e o `LEIA-ME.md` com as escolhas. O gibão é um colete
  sem mangas com alças, decote mostrando o avesso, pala costurada, amarração, cintura e saia em abas; as botas, um par
  de perfil com cano dobrado, tira com fivela no tornozelo, peito do pé e sola com salto. Listas calculadas por
  `auxiliares/couro_r1.py` (polígonos na grade de cada tamanho); pintura pelo `pintar.lua`.
- **Ferramenta compartilhada:** `tests/navegador/cenarios.py` ganhou `VESTIR` e `AMOSTRA` para peças que não são
  arma (o sorteio das armas é o mesmo). Novos no protótipo: `fotografar_couro.mjs`, `comparar_couro.py`.
- **Conferido:** os `.aseprite` reabertos (camadas, dimensões, alfa só 0 e 255), a captura do editor igual ao PNG e à
  prévia; silhueta, carvão e as fotos atual × candidato (ficha e mercado 32, saque 64, telas inteiras) em 1500×950 e
  1280×720, sem erro no console; verificações do `CLAUDE.md` em `couro-aseprite/logs/verificacoes.log`.
- **Continua como está no jogo:** os sprites 16×16. Próximo: a avaliação do Jean.

### 16/10/2026 (data do computador local) — Peitoral e botas de couro: o fechamento do 32 e os tamanhos 40 e 48 (protótipo, sem versão)

- **Pedido de Jean:** preservar os desenhos; no gibão de 32 só o fechamento (os pontos pareciam botões): poucos traços
  conectados; depois o 40 e o 48 das duas peças com a construção aprovada.
- **Feito:** `ferramentas/prototipos/hud/couro-aseprite/rodada2/` (os oito `.aseprite` em camadas, PNGs e @2x),
  gerados por `auxiliares/couro_r2.py` (o `couro_r1.py` fica como histórico) e pintados pelo `pintar.lua`. O 64 das
  duas peças e as botas de 32 iguais à rodada 1 pixel a pixel; no gibão de 32 mudaram só 5 pixels: o cordão num
  zigue-zague contínuo dentro da fenda. O 40 segue a construção do 32 (cordão em zigue-zague, um corte na saia; botas
  com uma dobra); o 48, a do 64 simplificada (ilhós e cordão em X, três cortes; botas com duas dobras e fivela com
  furo).
- **Conferido:** silhueta numa cor só e cor nos quatro tamanhos; editáveis reabertos e captura do editor = PNG =
  prévia; no jogo, atual × rodada 2 nas duas janelas: ficha e mercado 32, Inventário 40, saque 64 com o 48 nativo ao
  lado e o voo, sem erro no console. Nenhuma ferramenta compartilhada mudou nesta rodada; verificações em
  `couro-aseprite/logs/verificacoes-r2.log`.
- **Comparação pedida (avaliação em aberto, a regra da skill não muda):** no cartão do saque, com os mesmos dados, o
  64 trabalhado × o 32 final ampliado exatamente 2× (vizinho mais próximo, sem retoque), das duas peças, nas duas
  janelas (`couro-aseprite/rodada2/capturas/x2-gibao.png`, `x2-bota.png`). Decide se o detalhe extra do 64 justifica o
  tratamento nos próximos itens.
- **Continua como está no jogo:** os sprites 16×16. Próximo: a avaliação do Jean.

### 16/10/2026 (data do computador local) — 1.110.0: o gibão e as botas de couro no jogo (aprovados e integrados)

- **Decisão de Jean:** o gibão e as botas aprovados; integrar a rodada 2 (commit `9d49726`) com esta escolha: 32, 40
  e 48 os aprovados; o 64 é o 32 final ampliado 2× por vizinho mais próximo, sem retoque; os 64 desenhados à parte
  ficam como histórico. A orientação da skill muda: a arte principal em 32 primeiro, ampliação inteira para os
  tamanhos maiores quando aprovada, tamanhos intermediários derivados da fonte, versão detalhada só com ganho visível.
- **Entrou:** `rpg/web/static/hud/icones/gibao-32/40/48/64.png` e `bota-32/40/48/64.png` com os @2x, exportados por
  `ferramentas/arte/exportar_aseprite.py` (agora com `DERIVADOS`: no gibão e nas botas, `64: (32, 2)`) das fontes em
  `ferramentas/arte/aseprite/gibao/` e `bota/` (32, 40, 48 em camadas); idênticos byte a byte aos escolhidos; reduzir
  o 64 pegando um pixel de cada bloco 2×2 devolve o 32 (conferido pelo `--conferir`, que reproduz e compara as três
  peças: varinha, gibão e botas). Os 64 desenhados à parte em `ferramentas/arte/aseprite/historico/`. `Icones`:
  `TAMANHOS.gibao`, `TAMANHOS.bota`, `ITEM.gibao`, `ITEM.bota`.
- **Alcance:** o desenho "gibao": Gibão de Couro, Capa de Patrulha e Colete Acolchoado (o peito do Arqueiro), em todos
  os materiais de couro (Rasgado, Curtido, Reforçado, Tachonado, Rúnico), e o único Pele do Penitente (também a
  recompensa da missão do Turvo); o desenho "bota": a Bota de Caça (os pés do Arqueiro), nos mesmos materiais, e o
  único Botas do Andarilho Morto. Ficam como estão: o estado Iniciativa (o sprite "bota" noutro papel) e o espaço vazio
  dos pés (a bota de ferro). A Capa de Patrulha segue com o desenho do gibão; um desenho próprio dela ficou registrado
  em `docs/ROADMAP.md` (ideias guardadas).
- **Skill e documentos:** `arte-itens-fenda` com o processo "Do 32 para os outros tamanhos" e o exemplo do couro
  (os itens aprovados antes ficam com os arquivos que têm; trocar algum pede comparação própria);
  `ferramentas/arte/aseprite/LEIA-ME.md` (o 32 é a fonte do 64 deste lote); `docs/ARQUITETURA.md`; o protótipo do
  couro marcado como histórico.
- **Ferramentas compartilhadas:** `tests/navegador/cenarios.py` ganhou `ACHADO_ID` (o achado é um único do catálogo);
  `ferramentas/arte/fotografar_itens.mjs` confere `SO=gibao,bota` (a peça vestida por `VESTIR`, e os dois únicos no
  cartão do saque).
- **Conferido** (`fotografar_itens.mjs`, `SO=gibao,bota`): ficha e mercado em 32 (Vender, dica de comparação, vendido
  em Recomprar e recomprado), corpo e mochila do Inventário em 40 (e o achado guardado na mochila), cartão do saque
  com o 64 derivado e o "você usa" em 48, voo ao equipar, a roda da luta, e o cartão do saque com a Pele do Penitente e
  as Botas do Andarilho Morto; em 1500×950 e 1280×720, sem erro no console. Preços, atributos, estoque, regras, áreas
  clicáveis e animações não mudaram (em `rpg/`, só `icones.js`, a versão e os PNGs). Logs em
  `ferramentas/prototipos/hud/couro-aseprite/logs/integracao-*.log`.
- **Próximo:** nenhuma peça começou; os 64 dos itens anteriores ficam como estão.

### 17/10/2026 (data do computador local) — Diagnóstico: a demora dos testes de unidade (só documentação, sem versão)

- **Pedido de Jean:** os testes de unidade passaram a levar ~9 min (antes ~1); medir sem atribuir a causa a outro
  processo, sem mudar critérios.
- **Medido** (Windows 10, Python 3.12.4, sozinho, sem fotos nem fumaça desta sessão em paralelo; o `python jogar.py`
  do Jean aberto desde 16/10 22:17 ficou aberto em todas as medições), com `ferramentas/diagnostico-testes/
  tempos_testes.py` (a mesma descoberta do `unittest discover -s tests`, um tempo por teste):
  - sem `PLAYWRIGHT_MODULO`: **52 s**, 603 testes, 1 pulado (o `test_navegador`); o grosso é o `test_simulacao`
    (44 s; `test_todo_evento_roda` 25 s, o gabarito 7 s);
  - só o `test_navegador`, com `PLAYWRIGHT_MODULO`: **488 s** (ele roda o `fumaca.mjs` inteiro: 48 cenários e 186
    esperas fixas que somam ~106 s).
  - 52 + 488 = 540 s: as rodadas de 542 a 547 s (16/10) tinham o `PLAYWRIGHT_MODULO` exportado antes do `unittest`,
    na mesma linha de comando; as de ~55 s, não.
- **Causa:** procedimento, não o jogo nem os testes: com o Playwright no ambiente, o `unittest` inclui a fumaça (por
  desenho), e a fumaça ainda era rodada de novo em seguida. Não há medida antiga da fumaça sozinha para dizer se ela
  mesma ficou mais lenta.
- **Feito:** a nota no `CLAUDE.md` (o `unittest` roda a fumaça quando acha o Playwright; não repetir), o medidor e as
  medições em `ferramentas/diagnostico-testes/` (`medicoes.log`, `tempos-sem-playwright.tsv`). Nenhum teste, espera
  ou critério mudou.

### 17/10/2026 (Brasília) — Plano operacional consolidado: arte, interface e clareza do combate

- **Pedido e aprovação de Jean:** organizar o documento do plano com a sequência já combinada e os novos pontos:
  ícones de atributos, HP/recursos/ouro/flechas/bolsa, talentos, caminhos/mapa, mobs e pets; dado mais visível;
  iniciativa e turnos claros; custo do recurso percebido antes das consequências; consulta aos testes de atributos.
- **Onde seguir:** [23 — Plano de arte, interface e combate](23-PLANO-DE-ARTE-INTERFACE-E-COMBATE.md), com resumo em
  `docs/ROADMAP.md` e entrada no índice desta pasta. O plano distingue direção aprovada, hipóteses e entrega
  implementada; as etapas técnicas e o histórico foram preservados.
- **Ordem imediata:** concluir/avaliar o lote de cabeça/capuz e luvas já solicitado; integrar só o aprovado;
  reproduzir/corrigir a percepção atrasada do custo de recurso; prototipar dado, iniciativa, turnos e acesso aos
  testes; retomar os lotes de ícones. Depois vêm telas/level up/livros/criação, forja visual, forja mecânica,
  Templo/Curandeira/Taverna, cenários, eventos, habilidades e campanha.
- **Direções:** iniciativa em indicador compacto no topo enquanto disponível, com entrada breve; “Turno N” breve
  e número discreto; preservar o dado e a tirinha sem Continuar extra. Percepção/Destreza são bônus derivados,
  consultáveis com a composição na ficha detalhada, não novos atributos distribuíveis.
- **Base:** produção 1.110.0; o couro usa 32 principal/64 derivado 2×, com 40/48 aprovados. Preservados os 64 dos
  itens anteriores até comparação própria. A E9 continua aberta. O diagnóstico dos ~9 min já está documentado:
  `unittest` com Playwright inclui fumaça; evitar repeti-la.
- **Escopo desta atualização:** quatro arquivos Markdown; leitura estática e revisão documental, sem executar testes
  ou navegador e sem mudar motor, interface, saves, arte ou versão. Os detalhes da história permanecem rascunho no 22.

### 17/10/2026 (data do computador local) — Proposta: o capuz e a luva com braçadeira de couro (protótipo, sem versão)

- **Pedido de Jean:** completar a família de couro do Arqueiro com a cabeça e as mãos, só no protótipo: o 32 como
  fonte, o 64 como o 32 ampliado 2× (sem 64 redesenhado por padrão); 40 e 48 depois da aprovação.
- **Os dados:** `capuz` = Capuz e Chapéu de Couro do Arqueiro (couro) e Capuz do Mago (tecido), sem único; `luva` =
  Braçadeira do Arqueiro (couro), Luva de Seda do Mago (tecido) e o único Mãos do Estrangulador. A peça do Arqueiro é
  uma braçadeira: a proposta é uma luva com braçadeira, que serve aos dois nomes. Contradições anotadas: o Chapéu de
  Couro com desenho de capuz; os itens de tecido do Mago com desenhos de couro. A habilidade Desaparecer usa o sprite
  `capuz` noutro papel e fica como está.
- **Feito:** `ferramentas/prototipos/hud/couro2-aseprite/` (os `.aseprite` do 32 em camadas, os PNGs, o 64 derivado,
  os @2x, as pranchas, as fotos, os logs e o `LEIA-ME.md`), com `fotografar_couro2.mjs` e `comparar_couro2.py`.
- **Conferido:** silhueta numa cor só e cor, carvão ao lado do gibão, das botas e dos aprovados; editáveis reabertos
  (captura do editor = PNG = prévia; alfa 0 e 255; o 64 é o 32 ampliado 2× exato); no jogo, atual × candidato na
  ficha e no mercado em 32, no cartão do saque com o 64 derivado e nas telas inteiras, em 1500×950 e 1280×720, sem
  erro no console. Verificações em `couro2-aseprite/logs/verificacoes.log`.
- **Continua como está no jogo:** os sprites antigos. Próximo: a avaliação do Jean.

### 17/10/2026 (Brasília) — Plano: mostrar a capacidade de vida bloqueada pelo ferimento

- **Pedido de Jean:** quando um ferimento reduz a vida máxima, manter perceptível a capacidade saudável na barra,
  inclusive quando o herói está cheio até o limite reduzido (exemplo: 45 de 65, com limite atual 45).
- **Direção registrada:** no item 1.7 do plano 23 e no resumo de `docs/ROADMAP.md`, como parte da prioridade 1B:
  distinguir preenchimento, dano recuperável e capacidade bloqueada no fim. A área bloqueada precisa de aparência
  própria e explicação, não apenas espaço vazio. Se mostrar 45/65, acompanhar do limite atual ou da redução.
- **Limites:** números e causas reais do motor, referência acompanhando equipamento/nível/penalidades; não mudar
  cura, tratamento ou estado do personagem. Conferir demais penalidades antes de atribuir toda redução a ferimentos.
  Protótipo e formato final ainda serão avaliados.
- **Escopo:** só documentação; nenhuma implementação ou teste de jogo executado nesta atualização.

### 17/10/2026 (data do computador local) — Proposta: o caimento do capuz de couro e os materiais separados (protótipo, sem versão)

- **Pedido de Jean:** a luva de couro com braçadeira aprovada visualmente (preservada); refazer o caimento do capuz de
  couro (a base parecia gorro/balaclava); propor um capuz de tecido e uma luva de seda para os itens de tecido do Mago.
- **Feito:** `ferramentas/prototipos/hud/couro2-aseprite/rodada2/` (o capuz de couro com a capa caindo em diagonal e
  dois vincos de dobra, sem aro; o capuz de tecido com pico macio, dobra fina na borda e pano pendurado em dobras
  verticais; a luva de seda justa, dedos separados, punho curto e o brilho da seda; a luva de couro copiada da rodada
  1, igual byte a byte), pintados no Aseprite pelo `pintar.lua`; o 64 é o 32 ampliado 2×.
- **Mapeamento:** hoje o desenho é escolhido só pelo nome do sprite, igual para as duas classes. Recomendado para a
  integração: dar às bases de tecido do Mago (Capuz, Luva de Seda) os desenhos `capuz_tecido` e `luva_seda` nos dados
  (só o ícone); a alternativa é o `Icones` receber o item. Não feito: espera a decisão do Jean. O Chapéu de Couro
  segue precisando de desenho próprio.
- **Conferido:** silhuetas e cor, carvão com o gibão e as botas, editáveis reabertos; no jogo, o Arqueiro com o couro e
  o Mago com o tecido (ficha e mercado 32, saque com o 64, telas inteiras) em 1500×950 e 1280×720, sem erro no
  console; verificações em `couro2-aseprite/logs/verificacoes-r2.log`.
- **Continua como está no jogo:** os sprites antigos. Próximo: a avaliação do Jean.

### 17/10/2026 (data do computador local) — Proposta: a passagem do capuz de tecido para a pala (protótipo, sem versão)

- **Avaliação de Jean da rodada 2:** aprovados visualmente a luva de couro com braçadeira, o capuz de couro revisado e
  a luva de seda (não tocados). O capuz de tecido pedia um último ajuste: a divisão horizontal e as dobras verticais
  paralelas faziam a pala parecer uma cortininha separada.
- **Feito:** `ferramentas/prototipos/hud/couro2-aseprite/rodada3/` (a silhueta desce do pescoço para os ombros sem
  degrau, os lados do capuz continuam nos planos da pala, só uma sombra curta sob a abertura, duas dobras abrindo do
  pescoço para fora, poucos planos de luz, a barra numa curva lisa sem franja; cabeça, abertura, borda, interior e
  paleta iguais), pintado no Aseprite pelo `pintar.lua`; o 64 é o 32 ampliado 2×. A rodada 2 ficou para comparação.
- **Investigado para a integração (não feito):** o desenho vai gravado no item (`icone`) e o save o guarda; trocar só
  os dados das bases do Mago não alcança os itens já salvos. Recomendado: os dados novos mais uma migração do save
  (v4 → v5) que percorre o save e troca `capuz`/`luva` por `capuz_tecido`/`luva_seda` nos itens de `classe` `mago` da
  cabeça e das mãos (detalhes no `LEIA-ME.md` da proposta).
- **Conferido:** editável reaberto (captura do editor = PNG = prévia = composto da linha de comando), o 64 exato; no
  jogo, rodada 2 × rodada 3 com o Mago (ficha e mercado 32, saque com o 64, telas inteiras) em 1500×950 e 1280×720,
  sem erro no console; verificações em `couro2-aseprite/logs/verificacoes-r3.log`.
- **Continua como está no jogo:** os sprites antigos. Próximo: a avaliação do Jean; depois, 40 e 48 e a integração.

### 17/10/2026 (data do computador local) — Escolha: capuzes e luvas de couro e tecido aprovados visualmente

- **Escolha de Jean:** aprovados visualmente o capuz de couro revisado (rodada 2), a luva de couro com braçadeira
  (rodada 1), a luva de seda (rodada 2) e o capuz de tecido da rodada 3 (`1c061e1`), todos em
  `ferramentas/prototipos/hud/couro2-aseprite/`, com o 64 como o 32 ampliado 2×.
- **Pendente, numa entrega separada:** os 40 e 48 derivados das fontes aprovadas e a integração no jogo, incluindo a
  compatibilidade dos itens dos saves antigos (a migração proposta no `LEIA-ME.md` da proposta). Nada entrou no jogo.

### 17/10/2026 (data do computador local) — Proposta: os comandos da luta na linguagem do seletor (protótipo, sem versão)

- **Pedido de Jean:** Atacar, Habilidades, Itens e Fugir na linguagem do seletor D refinado (Clair Obscur como
  referência de tratamento), mantendo disposição, ícones, atalhos, alternar dos menus e proteções; uma variação com as
  cartas mais contidas (a moldura dupla dourada do herói); uma amostra só nas escolhas de um lugar selvagem.
- **Feito, só no protótipo:** `ferramentas/prototipos/hud/comandos/` (as folhas, a ponte que reaproveita as pontas do
  seletor e a troca que marca a amostra), `fotografar_comandos.mjs` e `comparar_comandos.py`, com as fotos e as medidas
  em `capturas-comandos/`. Registro e avaliação no `LEIA-ME.md` de `ferramentas/prototipos/hud/` e no item 1.8 do
  plano 23.
- **Conferido:** as três lutas (dia, noite, Arqueiro) nas três janelas e nas três versões, os comportamentos (cliques
  depressa, tecla segurada, alternar, clique logo na volta, movimento reduzido) e cinco telas de exploração em quatro
  janelas; nada cobre carta, nada se mexe ao abrir ou fechar, nada cortado, sem erro no console. Nenhum texto real da
  exploração quebra de linha: a quebra foi vista num teste de esforço declarado (texto alongado só na foto). A fonte
  pixel ficou de fora (vai sair do jogo).
- **Continua no jogo:** os comandos, as cartas e as escolhas de hoje. Próximo: a avaliação do Jean.

### 17/10/2026 (data do computador local) — Ajustes: os comandos da luta antes da avaliação final (protótipo, sem versão)

- **Avaliação de Jean:** aprovada a direção visual dos comandos (faixas curtas de pincel, tecla, ícone e nome juntos,
  sem o nicho preto, os ícones), das cartas contidas e das faixas da exploração. Pedidos três ajustes, só no protótipo.
- **Feito, em `ferramentas/prototipos/hud/comandos/`:** o carvão dos comandos um tom acima e quase opaco, com um fio de
  luz no alto (a forma não some mais à noite); a faixa alta da exploração numa pincelada só (as pontas escalam pela
  altura; mais folga quando há riscos ou nota; as de uma linha iguais); o aviso "Inimigos +1 nível" numa faixa própria,
  no canto direito da arena, sem cobrir o Fugir (anterior ao protótipo). `fotografar_comandos.mjs` passou a comparar
  antes (`206f3e6`, lido do git) × depois e ganhou o bando (comitiva cheia e 5 lobos) e a Capela sem tocha.
- **Conferido:** quatro lutas em 1500×950, 1280×720 e 1920×1080, com todos os estados, alternar, mira e volta,
  comportamentos e movimento reduzido; seis telas de exploração em quatro janelas (o teste de esforço marcado como
  simulado). Cartas no mesmo lugar antes e depois; o aviso não toca nada; sem erro no console. Suíte (603, a fumaça
  não rodou: só arquivos do protótipo mudaram), gabarito e pyflakes OK.
- **Achado, anterior ao protótipo:** com 5 inimigos em 1280×720 e 1500×950, os comandos e a caixa da mira ficam sobre
  cartas inimigas; o jogo de hoje já faz isso. Entrega própria, a decidir.
- **Continua no jogo:** os comandos, as cartas e as escolhas de hoje; versão sem mudança. Próximo: a avaliação final do
  Jean. Os tamanhos 40/48 e a integração dos capuzes e luvas continuam numa entrega separada.

### 17/10/2026 (data do computador local) — Entrega: a HUD aprovada integrada e as lutas cheias (1.111.0)

- **Pedido de Jean:** integrar o acabamento aprovado do `5795a9a` depois de resolver as lutas cheias (comandos sobre
  cartas, mira cobrindo alvo), sem nova rodada estética.
- **Feito:** os comandos em faixas, as cartas contidas, o aviso da cena separado e as escolhas de um lugar selvagem
  em faixas, nas folhas do jogo (`15-hud-luta.css`, `18-seletor-habilidades.css`), sem depender do protótipo; a arena
  em três áreas (`batalha.js`, `distribuir`: a fileira do herói numa coluna, a faixa dos comandos reservada, os
  inimigos à direita, em duas colunas só onde cabem); a mira e o Voltar na faixa dos comandos; a vaga de quem sai no
  meio da luta; quem foi invocado e cai sai da arena dos dois lados (antes, só do lado do herói). O motor ganhou dois
  campos de apresentação: a opção de explorar marcada e o `invocado` no estado da luta.
- **Os maiores grupos reais:** 6 aliados (necromante) e 6 inimigos (o bando de caídos); a comitiva tem no máximo 2.
- **Conferido:** antes × depois com os mesmos dados (`ferramentas/prototipos/hud/fotografar_lutas_cheias.mjs`), 5 lutas
  × 3 janelas e 6 telas de exploração × 4 janelas; nada cobre nada depois; menus, mira, Voltar, a saída e a entrada
  simuladas e os comportamentos conferidos; sem erro no console. Suíte, fumaça, pyflakes e gabarito (atualizado: só
  os dois campos novos mudaram, 915 linhas, nenhuma escolha, sorteio ou texto).
- **Limite:** em 1280×720 com 5 ou 6 inimigos e efeitos, ~120 a 160 px de registro; o seletor rola dentro.
- **Próximo:** a avaliação do Jean jogando; os capuzes e luvas (entrega seguinte).

### 17/10/2026 (data do computador local) — Entrega: capuzes e luvas de couro e tecido (1.112.0)

- **Pedido de Jean:** o 40 e o 48 dos quatro desenhos aprovados, sem mudar o conceito, e a integração, com os saves
  antigos recebendo o desenho certo pelos dados do próprio equipamento.
- **Feito:** o 40 e o 48 da mesma construção de cada peça (`couro2_r4.py`, que no 32 reproduz os aprovados pixel a
  pixel; um retoque de grade só, no capuz de tecido), pintados no Aseprite pelo `pintar.lua`; as fontes finais em
  `ferramentas/arte/aseprite/<peça>/`; os 32 arquivos no jogo pelo exportador (o 64 é o 32 ampliado 2×); os papéis no
  `Icones`; o Capuz e a Luva de Seda do Mago com os desenhos de tecido (`itens.py`); `icone_de` decide pela classe do
  item quando ele não guarda o desenho; a migração v4 → v5 troca o desenho das peças de tecido do Mago guardadas antes
  (só o campo `icone`).
- **Conferido:** fontes reabertas iguais aos PNGs; 32 e 64 iguais aos aprovados; no jogo (`fotografar_itens.mjs`),
  32 na ficha e no mercado, 40 no Inventário, 64 e 48 no saque, voo, venda, recompra, luta e as Mãos do Estrangulador;
  a migração em testes (repetida sem mudança, um save v4 carregado e regravado) e em cópias dos 36 saves pessoais (16
  trocas, nenhuma no Arqueiro, nenhum erro); suíte, fumaça e pyflakes; o gabarito (só o nome do desenho e a versão do
  save mudaram).
- **Continua:** o Chapéu de Couro com o capuz (pede desenho próprio); a Desaparecer com o sprite. Commits separados: os
  desenhos e os dados (`ea8acb7`), a migração (o seguinte).
- **Próximo:** a avaliação do Jean jogando as duas entregas; nenhum outro lote começou.

### 17/10/2026 (data do computador local) — Entrega: as escolhas da página em faixas (1.113.0)

- **Pedido de Jean:** as faixas como a apresentação comum das escolhas narrativas e das ações da página, sem exceções
  por lugar, sem identificar pelo texto, sem marca nova nos eventos; regras e conteúdo das opções intactos.
- **Feito:** o mapa dos usos reais (`ferramentas/prototipos/hud/escolhas-faixas/levantar.mjs`); a lista de escolhas da
  página fora da luta e do título em faixas (`escolhas.js`; a marca `explorar` do motor saiu); no CSS, o teste de
  atributo, a seta ›, a secundária e a indisponível legíveis no carvão e no marfim.
- **Conferido:** 14 casos reais × 2 janelas, antes × depois: conteúdo igual nas 26 comparações, contraste das
  etiquetas no marfim de 7,1 a 12,7, teclado, mouse, pressionado, indisponível, a tecla do número; suíte, fumaça e
  pyflakes; o gabarito (808 linhas, só a marca `explorar` saindo; nenhum texto, escolha ou sorteio).
- **Fora desta entrega (decidido pela função):** mercado, confirmações, achado, doca, caminhos, prédios da vila,
  fogueira e o título continuam com o próprio tratamento.
- **Próximo:** Jean jogar; a composição compacta das lutas cheias segue em avaliação (protótipo, entrega à parte).

### 17/10/2026 (data do computador local) — Correção: as faixas pela função narrativa (1.113.1)

- **Alinhamento de Jean:** a criação do personagem fica como estava (a apresentação dela terá a etapa própria); a
  regra das faixas segue a função narrativa do controle, não só o uso da lista de escolhas.
- **Feito:** `escolhas.js` dá as faixas às escolhas da partida em andamento, fora da luta (há partida quando o motor
  manda o estado dela, só com herói e mundo). O título, a lista de saves e a criação ficam de fora sem exceção escrita.
- **Conferido:** os 13 casos narrativos com lista continuam em faixas, a criação (título e classe) sem faixas, a tecla
  do número, sem erro no console; suíte, gabarito (sem mudança), pyflakes e fumaça.
- **O tempo das baterias (registrado nos LEIA-ME):** as escolhas, 60 cenários em ~7 min (~6 s cada); a composição
  compacta, 39 cenários em ~12 min (15 a 21 s cada: a rodada de ataque, os dois menus, o mouse em cada habilidade).
  A "uma hora" estimada antes não se confirmou: as duas baterias juntas somam ~19 min.

### 17/10/2026 (data do computador local) — Protótipo: a composição compacta das lutas cheias (em avaliação)

- **Pedido de Jean:** nas lutas cheias em 1280×720, todas as habilidades à vista sem rolar e a descrição legível, sem
  perder o que a 1.111.0 aprovou; só protótipo, até duas alternativas.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/compacta/`): A, arena compacta (efeitos na linha do nome,
  seletor em três colunas); B, seletor sobre a coluna da ficha quando a lista inteira não cabe embaixo. Produção, A e B
  com os mesmos dados: 4 lutas reais (até 6 × 6, o máximo que as regras permitem) × 3 janelas, mais o teclado.
- **Resultado:** A corta os nomes das cartas com 3 ou 4 efeitos e não resolve a luta maior (5 de 7); B mostra 7 de 7
  habilidades e 5 de 5 itens em todos os casos, a descrição de 150 a 179 px, sem mexer na arena, e nas lutas pequenas é
  igual à produção. Nas três: menus e mira não mexem nem cobrem cartas, teclado e movimento reduzido certos.
- **Recomendado:** B. **Custos:** cobre a ficha enquanto aberto; nomes em duas ou três linhas na coluna estreita.
  **Limite:** o registro curto com muitos efeitos em 1280×720 (a arena cresce) fica para outra entrega.
- **Próximo:** Jean avaliar a 1.113.1 jogando e decidir a composição; nada integrado; nenhum outro lote nem a 1B.

### 17/10/2026 (data do computador local) — Protótipo: composição compacta, rodada 2 (em avaliação)

- **Pedido de Jean:** a B aprovada como direção; antes de integrar, o custo numa linha própria na coluna da ficha e a
  investigação do registro sem espaço. Só protótipo (`ferramentas/prototipos/hud/compacta/rodada2/`).
- **Custo embaixo do nome (b2): escolhido.** Nenhum nome em três linhas, custos alinhados, mesma letra, o Voltar no
  título, a descrição igual ou maior. Corrigido o seletor que ficava na tela durante a mira (rodada 1). Conferidos a
  ficha inerte, o Tab, o Esc, o clique fora, o redimensionar (examinada, foco e cartas no lugar) e o movimento reduzido.
- **Registro:** o robô (`compacta/efeitos_reais.py`, 1.200 lutas) mostra que o bando de caídos com efeito em todas as
  cartas é comum; com um momento real, sobram 19 a 51 px em 1280×720. Proposta: nessas lutas, o registro na coluna do
  mundo, decidido no começo (~13 linhas); cobre o minimapa, a missão e os caminhos durante a luta.
- **Achado de regra (não mudado):** o necromante chega a 7 aliados (o Senhor dos Mortos dispara de novo depois de o
  xamã reviver um caído).
- **Próximo:** Jean avaliar a b2 e o registro na coluna do mundo; integrar juntos se aprovados. Nenhuma outra etapa
  começou (nem a 1B, nem lote de arte).

### 17/10/2026 (data do computador local) — Rei dos Mortos (1.113.2) e a composição compacta integrada (1.114.0)

- **Pedido de Jean:** integrar a B refinada e o registro na coluna do mundo, fechar a adaptação ao redimensionamento e
  corrigir o Rei dos Mortos em commit separado.
- **Rei dos Mortos (1.113.2):** uma vez por combate (`uma_vez_por_luta`). O xamã reviver um caído não abre uma segunda
  vez; um combate novo ativa de novo. `tests/test_rei_dos_mortos.py` falha sem a correção. Gabarito sem mudança. Depois
  dela, 6 × 6 é o limite das regras e o maior grupo visto.
- **Integrado (1.114.0):**
  - o seletor sobre a ficha (`escolhas.js`, `dispor`): custo embaixo do nome, Voltar no título, ficha inerte, sai na
    mira, redispõe ao redimensionar sem fechar;
  - o registro ao lado (`paineis.js`, `acomodarRegistro`): na coluna do mundo; abaixo de 1100 px, na da ficha; abaixo
    de 920 px, embaixo com a página rolando.
- **Conferido** (`ferramentas/prototipos/hud/compacta/integracao/`):
  - igual ao protótipo aprovado com os mesmos dados;
  - a passagem 1500 → 1280 → 1050 → 900 → volta, com a luta em andamento;
  - teclado e movimento reduzido;
  - a suíte, o gabarito (sem mudança), o pyflakes e a fumaça uma vez.
- **Limitações:** abaixo de 920 px, a rolagem da página; entre 920 e 1100 px, o seletor aberto cobre o registro.
- **Próximo:** Jean jogar. Nada começou além disso (nem a 1B, nem lote de arte, nem a nova direção visual da HUD).

### 17/10/2026 (data do computador local) — Experimento: o pen.dev na composição da HUD (sem versão)

- **Pedido de Jean:** testar o pen.dev (plano gratuito, Windows, MCP com o Claude Code) para ver se compor num canvas
  editável facilita chegar ao resultado e levá-lo ao CSS. O mesmo ajuste em dois fluxos, num pedaço do seletor (duas
  faixas, nome longo, custo duplo, a descrição; 1280×720 e 1500×950; normal, destacada e indisponível).
- **Feito** (`ferramentas/prototipos/hud/pen-composicao/`, detalhes no LEIA-ME de lá):
  - uma bancada com o seletor real e as folhas do jogo, com fotos e medidas;
  - fluxo A, no CSS (cerca de 7 min);
  - fluxo B, no canvas pelo MCP e depois no CSS (cerca de 18 min).
  Os dois chegaram ao mesmo CSS.
- **Achados:**
  - a importação do localhost perde a tinta (pontas, inclinação, grão, tecla); fica fiel só reconstruindo com as
    peças do jogo como imagem;
  - reorganizar o componente apagou as personalizações das instâncias;
  - o código exportado não serve (inline, fonte na internet);
  - a tela de boas-vindas do app trava a importação até ser fechada.
- **Instalado e configurado:** Pen 1.2.18. O servidor MCP `pencil` está registrado só neste projeto (escopo local, fora
  do repositório), com o `aseprite-bridge` preservado; backup em `Tools\backups-config\`.
- **Recomendação:** restringir. O pen.dev não entra no fluxo; fica instalado só se Jean quiser propor arranjos à mão
  (o próximo teste possível: ele mexe no `seletor.pen` e eu levo ao CSS). A bancada é o que vale reaproveitar.
- **Próximo:** Jean avaliar. Nada entrou no jogo; nenhuma versão mudou.

### 17/10/2026 (data do computador local) — Etapa 1B: o custo do recurso na tela (1.114.1)

- **Pedido de Jean:** o efeito da habilidade (a cura da Drenar Vida) aparecia antes de a Mana ser paga.
- **Causa demonstrada:** o motor desconta antes de agir. A tela só recebia o recurso pago no primeiro texto da ação:
  depois do golpe, no alvo único, ou do fim da salva, em área.
- **Correção:** `ui.atualizar()` logo depois do desconto (`combate/heroi.py`: habilidades e a flecha do ataque
  básico).
- **Conferido:** a linha do tempo na página, antes e depois (`ferramentas/prototipos/hud/custo-recurso/`);
  `tests/test_custo_na_tela.py`; suíte, gabarito (sem mudança), pyflakes e fumaça.
- **Próximo:** o protótipo da vida bloqueada (entrega à parte); nada da 1C.

### 17/10/2026 (data do computador local) — Etapa 1B: protótipo da vida máxima bloqueada (em avaliação)

- **Pedido de Jean:** distinguir a vida de agora, a recuperável e a bloqueada pela redução da vida máxima.
- **Feito, só protótipo** (`ferramentas/prototipos/hud/vida-bloqueada/`):
  - os números saem das contas do motor (`totais()`, `max_hp`, `fontes_penalidade`; ferimentos e fome se multiplicam);
  - a barra mede a vida saudável, com o trecho bloqueado em hachura e a marca de limite;
  - o número `vida/saudável`, a etiqueta `−N` no topo e a dica com as fontes.
- **Conferido:**
  - os três estados (1280×720 e 1500×950);
  - uma rodada de luta;
  - a Curandeira, que devolve a parte do ferimento como vida;
  - vestir uma peça com +vida máxima;
  - a tela fecha com o estado, sem erro no console.
- **Próximo:** Jean avaliar. Nada da 1C nem lote de arte.

### 17/10/2026 (data do computador local) — Etapa 1B: a vida máxima bloqueada no jogo (1.115.0)

- **Pedido de Jean:** integrar a proposta aprovada (`e4fbd93`) com as barras do topo estáveis e a linha "Em você"
  coerente.
- **Feito:** `sobrevivencia.vida_bloqueio` no motor e `heroi.vida_bloqueio` no estado; a barra do herói mede a vida
  saudável no topo e na carta. A etiqueta "−N de vida máxima" vai para a linha das condições, e o lugar da gota dos
  ferimentos fica guardado (barras sempre de 242 px em 1280×720). "Em você", o motivo da poção e o Templo dizem o
  limite pelo nome.
- **Conferido** (`ferramentas/prototipos/hud/vida-bloqueada/integracao.mjs`):
  - os três estados em 1280×720 e 1500×950;
  - a poção para no limite;
  - a luta (a carta só desce);
  - a Curandeira devolve a parte do corte; vestir a peça;
  - o movimento reduzido;
  - a suíte, o pyflakes, o gabarito (só apresentação, investigado e atualizado) e a fumaça uma vez.
- **Próximo:** Jean jogar. Fora: as reduções do recurso máximo; nada da 1C.

### 17/10/2026 (data do computador local) — Etapa 1C: protótipo da iniciativa e dos turnos (em avaliação)

- **Pedido de Jean:** perceber a vantagem de iniciativa, enquanto ela vale, e o começo de cada turno; só protótipo.
- **Feito** (`ferramentas/prototipos/hud/turnos/`):
  - o anúncio em faixa ("Turno N", "Iniciativa!" com o bônus real, "Emboscada!");
  - a placa do turno de agora, com a linha da iniciativa até ela ser usada ou passar;
  - tudo comandado pelos acontecimentos do motor (a mensagem `turno`, o lance `surpresa`, o estado `iniciativa`, o
    golpe com `bonus_motivo`);
  - lugar medido, sem cobrir nada e sem segurar a vez.
- **Conferido:**
  - produção × proposta em lutas reais (iniciativa, emboscada, luta cheia com comitiva, servos e efeitos);
  - 1280×720, 1500×950 e movimento reduzido;
  - vídeos em `capturas/videos/`; `abrir.mjs` para jogar.
- **No cenário de teste:** `EMBOSCADA` e `LUTA_APOS_ESCOLHA`.
- **Próximo:** Jean avaliar (e testar a vida bloqueada). Nada integrado; dado e atributos não começaram.

### 17/10/2026 (data do computador local) — Etapa 1C: a iniciativa e os turnos no jogo (1.116.0)

- **Pedido de Jean:** integrar o protótipo aprovado (`5b519f0`) e tirar o estouro de pixels do começo da luta;
  conferir o turno com o herói atordoado.
- **Feito:**
  - `turnos.js` e `19-turnos.css` no jogo;
  - `perde_turno` no catálogo de estados: o turno perdido é anunciado como tal;
  - o estouro era a festa de nível relida sem cerimônia: o som e as partículas agora só saem quando a festa aparece.
- **Conferido** (`ferramentas/prototipos/hud/turnos/integracao.mjs`):
  - lutas reais em 1280×720 e 1500×950, normal e reduzido;
  - vídeos;
  - a suíte, o pyflakes, o gabarito (só o campo novo, investigado e atualizado) e a fumaça uma vez.
- **Próximo:** Jean jogar. Não começaram o dado, a consulta aos atributos nem outra mudança visual.

### 17/10/2026 (data do computador local) — Os avisos de turno: placa parada e anúncio num lugar só (1.116.1)

- **Pedido de Jean:** a placa parada durante o zoom e a tremida do golpe final; o anúncio centralizado, num lugar
  previsível, sem cobrir comandos, a placa ou o registro.
- **Feito:**
  - a placa e o anúncio se medem pelo layout e ficam parados no impacto (0 px; a arena, até 64 px);
  - o anúncio fica no centro da arena, na borda de cima, numa linha; a iniciativa diz "Turno 1 · Só você age", e o
    bônus fica na placa.
- **O compromisso:** entre os grupos não cabe sem cobrir comandos na luta pequena (a roda ocupa a faixa inteira); por
  isso a borda de cima, e numa linha.
- **Conferido:** `integracao.mjs` (luta pequena e cheia, 1280×720 e 1500×950, iniciativa, emboscada, turno perdido,
  golpe final, reduzido, redimensionar), a suíte, o pyflakes, o gabarito (sem mudança) e a fumaça uma vez.
- **Próximo:** Jean jogar. O dado e outras mudanças visuais não começaram.

### 17/10/2026 (data do computador local) — Protótipo: a rolagem narrativa no centro (plano 23, item 1.4)

- **Pedido de Jean:** mais destaque e expectativa nas rolagens de atributo (escolhas, diálogos e eventos), mantendo o
  dado, a tirinha e a animação; uma alternativa; só protótipo.
- **Feito** (`ferramentas/prototipos/hud/rolagem/`):
  - o grupo no centro da área principal (o teste e a dificuldade, o dado 2×, a tirinha em pincel, a faixa de resultado);
  - Sucesso em marfim inteiro; Falha em carvão rasgado;
  - o grupo desce até a tirinha do texto antes da consequência.
- **Conferido:**
  - mesmos dados nos dois modos (sucesso e falha por 1), 1920×945;
  - mesmo ritmo (1627–1631 ms);
  - pular, instantâneo e movimento reduzido;
  - uma gravação e quatro capturas.
  - O jogo não mudou: a suíte, o gabarito, o pyflakes e a fumaça não se aplicam (rodaram no mesmo código na 1.116.1).
- **Próximo:** Jean avaliar. Nada integrado; versão igual (1.116.1).

### 17/10/2026 (data do computador local) — A rolagem no centro, no jogo (1.117.0)

- **Pedido de Jean:** integrar o protótipo aprovado da rolagem (`ferramentas/prototipos/hud/rolagem/`), com o visual e
  o ritmo; "precisa de N ou mais" vindo do motor.
- **Feito:**
  - `app/rolagem.js` e `20-rolagem.css` no jogo;
  - `Testes.precisa_no_dado` no motor, mandado com a rolagem;
  - `tests/test_rolagem.py`.
- **Conferido:**
  - `integracao.mjs`: sucesso e falha por 1, 1920×945, o mesmo ritmo do protótipo, pular, instantâneo, reduzido;
  - a suíte, o pyflakes, o gabarito (igual) e a fumaça uma vez.
- **Registrado:** o redesenho do dado fica para o acabamento visual da HUD (plano 23, seção 2), com raridade e subida
  de nível.
- **Próximo:** Jean jogar. A consulta aos atributos (1.6) não começou.

### 17/10/2026 (data do computador local) — Os testes de atributo na ficha (1.118.0)

- **Pedido de Jean:** entender os valores dos testes (quanto, de onde vêm, para que servem), resolvendo só lacunas
  reais, sem redesenhar a ficha.
- **Feito:**
  - a linha "Testes do d20" na ficha, com a dica dos seis testes;
  - o motor separa as partes fixas da situação (a escuridão só aparece como "agora");
  - as dicas dos atributos dizem só a parte de cada um;
  - a chance da dica da escolha vem do motor.
- **Conferido:**
  - `tests/test_testes_ficha.py`;
  - uma captura a 1920×945;
  - a suíte, o pyflakes e a fumaça;
  - o gabarito, atualizado depois de investigar: só o estado do herói nas 9 partidas web.
- **Registrado para outra entrega:** o aviso do painel do mundo sobre a escuridão antes de agir.
- **Próximo:** Jean jogar. A nova HUD não começou.

### 17/10/2026 (data do computador local) — Estudo: a nova direção visual da HUD (em avaliação, nada no jogo)

- **Pedido de Jean:** uma proposta coerente e jogável da aparência da HUD principal a partir da imagem de referência
  dele; só protótipo.
- **Feito** (`ferramentas/prototipos/hud/direcao/`: `direcao.css`, `direcao.js` só para a dica dos testes,
  `fotografar.mjs`, `abrir.mjs`):
  - colunas de carvão com a borda gasta, sem o ferro;
  - contornos abertos;
  - nomes em serifa marfim;
  - latão só em detalhe;
  - o refinamento da dica "Testes do d20".
- **Conferido:**
  - atual × proposta a 1920×945, na exploração e na luta com o seletor e a mira;
  - sem erros, com as interações de pé;
  - nenhum arquivo do jogo mudou (a suíte, o gabarito e a fumaça valem os da 1.118.0).
- **Para a consolidação:** a largura a 1920, a borda de baixo da arena e as janelinhas da luta.
- **Próximo:** Jean avaliar. Versão de produção igual (1.118.0).

### 18/10/2026 (data do computador local) — Prova de fidelidade: a coluna da ficha (em avaliação, nada no jogo)

- **Pedido de Jean:** a proposta da HUD ficou longe da referência. Provar a linguagem só na coluna da ficha, com outro
  método, antes de estender.
- **Feito** (`ferramentas/prototipos/hud/direcao/ficha/`):
  - a referência salva (`direcao/referencia.png`) e comparada na mesma escala;
  - a arte por um gerador próprio (superfície com a borda rasgada e o papel da margem);
  - o conteúdo em CSS, com proporções e tipografia da referência;
  - a proposta anterior preservada.
- **Conferido:**
  - o centro com o mesmo tamanho e a ficha sem rolar;
  - dicas abrindo, sem erros;
  - nenhum arquivo do jogo mudou (a suíte, o gabarito e a fumaça valem os da 1.118.0).
- **Próximo:** Jean avaliar a linguagem. Só depois estender a outras áreas. Versão igual (1.118.0).

### 18/10/2026 (data do computador local) — Prova da ficha, rodada 2: a pintura de Jean (em avaliação, nada no jogo)

- **Pedido de Jean:** usar a textura dele (`direcao/Painel vertical em tinta escura.png`) como a decoração da ficha, no
  lugar da arte gerada.
- **Feito:**
  - `ficha/pintura.css` e `ficha/pintura.js`: a pintura numa peça à parte atrás da coluna, na escala 0,5 exata, sem
    esticar, transbordando a caixa para o conteúdo ficar sobre o escuro;
  - o fundo da tela em cinza quente escuro;
  - nenhuma mancha atenuada;
  - a rodada 1 preservada.
- **Conferido:**
  - o centro com o mesmo tamanho e sem rolagem;
  - as dicas abrindo, sem erros;
  - nenhum arquivo do jogo mudou.
- **Próximo:** Jean avaliar. Versão igual (1.118.0).

### 18/10/2026 (data do computador local) — Estudo: o conjunto da HUD na direção da ficha (em avaliação, nada no jogo)

- **Pedido de Jean:** estender a direção da ficha aprovada ao centro, ao mundo e ao topo, só no protótipo.
- **Feito** (`ferramentas/prototipos/hud/direcao/conjunto/`):
  - as peças derivadas da pintura (a espelhada para o mundo, o ladrilho de carvão, a máscara do rasgo);
  - `conjunto.css`: o desgaste na periferia, o centro calmo sem moldura, contornos abertos, marfim;
  - o ajuste local para a ficha não rolar na luta;
  - as rodadas anteriores preservadas.
- **Conferido:**
  - na exploração e na luta (seletor, mira e golpe), a 1920×945: sem erros, sem rolagem e com o centro do mesmo
    tamanho;
  - nenhum arquivo do jogo mudou.
- **A peça que falta:** uma pintura horizontal para a borda do topo.
- **Próximo:** Jean avaliar antes de integrar. Versão igual (1.118.0).

### 18/10/2026 (data do computador local) — Estudo: o topo pintado da HUD (em avaliação, nada no jogo)

- **Pedido de Jean:** concluir o topo com a pintura horizontal dele (`direcao/topo.png`), sem aumentar a barra;
  conferir a vida máxima bloqueada e a habilidade indisponível.
- **Feito** (`ferramentas/prototipos/hud/direcao/topo/`):
  - o recorte reproduzível (`derivar_topo.py`);
  - a pintura atrás dos textos;
  - as manchas das pontas atenuadas só atrás do texto;
  - o conjunto preservado.
- **Conferido:**
  - a barra com 46 px e o centro com 1088 px, sem rolagem e sem erros;
  - a vida bloqueada (105 de 146) legível na carta e na ficha;
  - as indisponíveis com "Vigor insuficiente", iguais no jogo;
  - nenhum arquivo do jogo mudou.
- **Próximo:** Jean avaliar. Versão igual (1.118.0).

### 18/10/2026 (data do computador local) — A nova HUD pausada para avaliação jogando (nada no jogo)

- **Situação:** a direção visual completa da HUD (`ferramentas/prototipos/hud/direcao/`: a ficha, o conjunto e o topo)
  está em avaliação, sem aprovação para integrar.
  - **A ficha:** aprovada como base do estudo.
  - **A tela inteira:** a decisão continua aberta. A dúvida é se a pintura permanente combina com a pixel art ou chama
    mais atenção que o mundo.
  - **Os menus de pincelada (comandos, seletor, escolhas):** continuam aprovados e em produção.
- **Feito:** a comparação jogável `ferramentas/prototipos/hud/direcao/comparar/jogar_comparacao.py producao|prototipo`.
  - Abre a janela de sempre com uma cópia do save atual (`turvo_dadad`), numa pasta de teste separada por versão
    (`%USERPROFILE%\.cronicas_da_fenda_teste_hud`).
  - O original fica intacto (conferido pelo hash).
  - O estudo entra só no processo do protótipo; nenhum arquivo do jogo muda.
- **Conferido:** o save real abre nas duas versões, sem erros; nada de arte nova, capturas ou vídeos.
- **Próximo:** Jean jogar as duas e decidir. Versão igual (1.118.0).

### 18/10/2026 (data do computador local) — Decisão: fica a HUD de produção (o estudo da nova HUD não será integrado)

- **Decisão de Jean, depois de jogar as duas versões:** prefere a HUD atual de produção. A direção com pintura nas
  colunas e no topo não será integrada.
- **Em produção e aprovados:** a HUD atual e os menus de pincelada (comandos, seletores de Habilidades e Itens,
  escolhas narrativas).
- **O estudo** (`ferramentas/prototipos/hud/direcao/`, com as pinturas): guardado, sem apagar, como estudo não
  escolhido para a HUD principal. Pode servir de referência para outras telas, sem reaproveitamento aprovado.
- **A aprovação da ficha** valia só como base do estudo: não autoriza integrá-la isolada nem transferir tipografia,
  espaçamentos, cores ou outras partes para a produção.
- **Pendência independente:** o refinamento de cores da dica "Testes do d20" ficou só no protótipo
  (`direcao/direcao.js` e o fim de `direcao/conjunto/conjunto.css`). Na produção a dica tem os números do motor, mas
  não essas cores nem o destaque só nas regras do 20 e do 1.
- **Próxima entrega do plano:** 1D, retomar os lotes de ícones (plano 23, tabela 1.2), em pequenos grupos por função.

### 18/10/2026 (data do computador local) — Lote de ícones da noite (1D): propostas, nada no jogo

- **Pedido de Jean:** com a skill `arte-itens-fenda`, uma peça por vez, sem substituir no jogo: a calça de couro do
  conjunto, a aljava, os atributos e a doca.
- **Feito** (`ferramentas/prototipos/hud/itens-lote-noite/`, scripts em `ferramentas/arte/desenhar_*_pixel.py`):
  - **A Calça de Couro:** hoje o sprite 16×16 recolorido. Proposta em 32, com o 64 ampliado 2×.
  - **A aljava:** proposta em 32, 64 e o 24 do topo. Na rodada 4, as hastes ficaram legíveis, a pedido de Jean.
  - **Os quatro atributos:** propostas em 24 e 32. A bota é também o comando Fugir.
  - **Os oito da doca:** propostas em 36 e 32. O Grimório é também o comando Habilidades.
- **Conferido:** atual × proposta nos lugares de cada peça (1500×950 e 1280×720), com o jogo intacto e sem erros; o
  LEIA-ME de lá tem, por peça, o que melhorou e o que pode ser pior.
- **Próximo:** Jean avaliar cada peça. Os 40 e 48 da calça e da aljava saem depois da aprovação do 32, e o papel da
  calça entra em `icones.js` na integração. Versão igual (1.118.0).

### 18/10/2026 (data do computador local) — Lote de ícones: a calça nos quatro tamanhos e a aljava refinada (propostas)

- **Decisões de Jean sobre o lote da noite:**
  - **A calça de couro:** o 32 aprovado.
  - **A aljava:** refinar a leitura no topo.
  - **Os atributos e a doca:** as propostas ficam como alternativas não escolhidas. (Corrigido depois por Jean: os
    ícones atuais são placeholders, pendentes de pixel art; não foi decidido mantê-los.) A skill `arte-itens-fenda`
    ganhou a orientação de que símbolos da interface não precisam copiar equipamentos.
- **Feito** (`ferramentas/prototipos/hud/itens-lote-noite/`, nada no jogo):
  - **A calça:** 40 e 48 da mesma construção em degraus (o 32 aprovado e o 64 iguais), mais a fonte em camadas
    (`calca_couro/fontes/*.aseprite`), conferida pixel a pixel.
  - **A aljava:** o 24 do topo refeito com simplificações próprias (mais largo, mais claro, sem a alça); o 32 sem
    mudança.
  - **O cenário `vila`:** ganhou `VESTIDO=<desenho>` (o "você usa" do saque).
- **Conferido:** a 1920×945, a calça no Inventário, no saque e na ficha, e a aljava atual × anterior × refinada no topo
  e na ficha. A suíte, o gabarito, o pyflakes e a fumaça uma vez.
- **Pendentes:**
  - Jean avaliar os quatro tamanhos da calça e a aljava refinada;
  - os 40 e 48 da aljava, depois da aprovação;
  - a integração das duas.
  Versão igual (1.118.0).

### 18/10/2026 (data do computador local) — A calça de couro no jogo (1.119.0); aljava e Ataque/Defesa em proposta

- **Pedido de Jean:**
  - integrar a calça de couro (os quatro tamanhos do `ee0f01a`);
  - refinar a aljava (as flechas pareciam cabeças engrossadas);
  - novos Ataque e Defesa em pixel art, um por vez.
  - Correção do registro: os ícones atuais de atributos e da doca são placeholders pendentes, não mantidos de vez.
- **Feito:**
  - **A calça no jogo:** as fontes em `ferramentas/arte/aseprite/calca_couro/`, `DERIVADOS` e `TAMANHOS`/`ITEM` em
    `icones.js`. Os oito arquivos são idênticos aos aprovados e a exportação se reproduz. Vale para todas as calças de
    couro do Arqueiro; os saves já usam `calca_couro`.
  - **A aljava, rodada 6:** hastes de 1 px, penas como palhetas, entalhe e a boca em perspectiva.
  - **Ataque e Defesa:** com volume (a espada em dois planos, o escudo abaulado), em 24 e 32, com o 64 do selo como o
    32 ampliado 2×.
- **Conferido:**
  - a 1920×945: a calça na produção (ficha, Inventário, saque), a aljava atual × rodada 5 × rodada 6, e Ataque e Defesa
    na ficha, no Inventário e no selo;
  - a suíte, o gabarito, o pyflakes e a fumaça uma vez.
- **Próximo:** Jean avaliar a aljava e Ataque/Defesa. Depois, Agilidade e Poder, e a doca em pares.

### 18/10/2026 (data do computador local) — Ataque e Defesa no jogo (1.120.0); aljava rodada 7 em proposta

- **Pedido de Jean:** integrar Ataque e Defesa (aprovados) sem retoque, com fontes em camadas; refinar só as flechas
  da aljava (as pontas pareciam garfos ou argolas).
- **Feito:**
  - **Ataque e Defesa no jogo:**
    - as fontes em `ferramentas/arte/aseprite/attr-ataque/` e `attr-defesa/` (24 e 32), montadas pelo fluxo novo
      (`--listas` no script do ícone e `ferramentas/arte/montar_fontes.py`);
    - o 64 do selo é o 32 ampliado 2× (`DERIVADOS`, `TAMANHOS`);
    - os doze arquivos são idênticos aos aprovados.
  - **A aljava, rodada 7:** duas flechas, as penas contínuas e simétricas linha a linha, a haste à vista, o entalhe só
    no 32. O recipiente não mudou.
- **Conferido:**
  - a 1920×945: Ataque e Defesa na ficha, no Inventário e no selo (produção), e a aljava antes × depois no topo e na
    ficha;
  - a suíte, o gabarito, o pyflakes e a fumaça uma vez.
- **Pendentes:**
  - a aljava (40, 48 e a integração) aguarda a avaliação;
  - Agilidade, Poder e a doca continuam placeholders, para os próximos pares.

### 18/10/2026 (data do computador local) — Aljava 40/48 e propostas de Agilidade e Poder (nada no jogo)

- **Pedido de Jean:** a aljava da rodada 7 (`5689148`) aprovada em 24, 32 e 64. Preparar os 40 e 48, e propor
  Agilidade e Poder, um por vez.
- **Feito:**
  - **A aljava:**
    - os 40 e 48 derivados da construção aprovada (`_derivado`); o 24, o 32 e o 64 continuam iguais;
    - as fontes em camadas no protótipo (`aljava/fontes/`);
    - `montar_fontes.py` e `exportar_aseprite.py` ganharam `--fontes=<pasta>` para propostas.
  - **Agilidade:** a bota de couro em passada, com rastros de velocidade.
  - **Poder:** a chama violeta viva em três línguas, com camadas aninhadas e faíscas.
  - Fontes em camadas e PNGs no protótipo (`agilidade_poder/`).
- **Conferido a 1920×945:**
  - a aljava no Inventário (40) e no saque (48 ao lado do 64);
  - Agilidade e Poder na ficha (os quatro juntos), no Fugir da luta e nos selos.
  - A suíte, o gabarito, o pyflakes e a fumaça uma vez.
- **Próximo:** Jean avaliar os intermediários da aljava e as propostas de Agilidade e Poder. A doca fica para os
  próximos pares. Versão igual (1.120.0).

### 18/10/2026 (data do computador local) — Agilidade e aljava refeitas pelas referências (nada no jogo)

- **Pedido de Jean:** refazer a Agilidade (a bota) e a aljava a partir de duas imagens de referência, no Aseprite pelo
  MCP. Nenhuma proposta anterior fica aprovada para integração, nem a aljava da rodada 7.
- **Feito** (`ferramentas/prototipos/hud/itens-lote-noite/agilidade_aljava_ref/`):
  - as grades desenhadas à mão (24 e 32 de cada peça);
  - as camadas pintadas no editor pelo `pintar.lua` e salvas como fontes `.aseprite`;
  - os PNGs exportados por `exportar_aseprite.py --fontes=`, iguais às grades (o 64 é o 32 ×2);
  - `fotografar.mjs` ganhou as peças `agilidade` e `aljava_ref`.
- **Conferido:**
  - a 1920×945: a Agilidade na ficha, no Fugir e no selo; a aljava na ficha e no topo;
  - a suíte, o gabarito e o pyflakes. A fumaça não foi repetida: nenhum arquivo do jogo mudou desde a última, que
    passou (`35262ca`).
- **Próximo:**
  - Jean avaliar as duas peças;
  - depois da aprovação, os 40 e 48 da aljava.
- **Continuam:** Poder em avaliação; a doca, para os próximos pares. A versão não mudou (1.120.0).

### 18/10/2026 (data do computador local) — A sola da Agilidade; os 40 e 48 da aljava nova (nada no jogo)

- **Pedido de Jean:**
  - Agilidade: refinar só a junção da sola e do salto (a faixa preta e o degrau);
  - aljava: a nova em 24 e 32 aprovada (`ea3835f`); preparar os 40 e 48.
- **Feito** (`ferramentas/prototipos/hud/itens-lote-noite/agilidade_aljava_ref/`):
  - **A bota:** a base em perfil contínuo e a sola em marrons profundos, com a junção de 1 px de marrom escuro. O
    resto da bota não mudou, e o antes está em `rodada1_sola/`.
  - **A aljava:** os 40 e 48 derivados da construção aprovada (`auxiliares/gen_n.py`), com as fontes em camadas.
  - Tudo pintado no Aseprite pelo MCP. A exportação é igual às grades, e os 24, 32 e 64 aprovados não mudaram.
- **Conferido:**
  - a 1920×945: a bota antes × depois na ficha, no Fugir e no selo; a aljava 40 no Inventário e a 48 no saque;
  - a suíte, o gabarito e o pyflakes. A fumaça não foi repetida: nenhum arquivo do jogo mudou desde `35262ca`.
- **Próximo:** Jean avaliar a sola e os 40/48. Depois, a integração do que ele aprovar.
- **Continuam:** Poder pendente; nenhum outro ícone começado. A versão não mudou (1.120.0).

### 18/10/2026 (data do computador local) — Agilidade (1.121.0) e aljava (1.122.0) no jogo

- **Pedido de Jean:** integrar as duas aprovadas, sem retoque, e apresentar de novo o candidato de Poder (sem
  redesenhar).
- **Feito:**
  - **As fontes finais:** foram para `ferramentas/arte/aseprite/attr-agilidade/` (24, 32) e `aljava/` (24, 32, 40,
    48); o 64 de cada uma é o 32 ampliado 2× (`DERIVADOS`). Os dezesseis arquivos do jogo são idênticos, byte a byte,
    aos aprovados (`e9b0499`, `ea3835f`, `fb403f5`), e `exportar_aseprite.py <peça> --conferir` os reproduz.
  - **Os mapeamentos não mudaram:**
    - a Agilidade é o atributo e o Fugir (`ACAO.fuga`); a bota do equipamento é outro desenho;
    - a aljava é toda Aljava do Patrulheiro (a comum, a única dos Mil Corvos, os saves pelo `icone`) e o recurso de
      flechas do topo.
  - **Os ajustes:** `TAMANHOS` ganhou o 64 da Agilidade. O `desenhar_aljava_pixel.py` antigo virou histórico (só grava
    numa pasta). O `fotografar.mjs` ganhou `SO_ATUAL=1` (o jogo sem troca nenhuma) e a peça `poder`.
- **Conferido:**
  - no jogo, sem injeção, a 1920×945 (`agilidade_aljava_ref/integradas-no-jogo.png`): a Agilidade na ficha, no Fugir
    e no selo; a aljava no topo, na ficha, no Inventário e no saque (48 e 64);
  - a suíte, o gabarito (sem diferença), o pyflakes e a fumaça uma vez.
- **Poder:** o candidato é o de `35262ca` (`ferramentas/prototipos/hud/itens-lote-noite/agilidade_poder/`, script
  `ferramentas/arte/desenhar_attr_poder_pixel.py`). Está mostrado ao lado do atual em `agilidade_poder/poder-atual-x-candidato.png`
  e aguarda a avaliação.
- **Próximo:** a decisão sobre Poder. A doca fica para os próximos pares.

### 18/10/2026 (data do computador local) — Poder, rodada 2 (nada no jogo)

- **Pedido de Jean:** refazer o Poder. O candidato `35262ca` ficou estreito, rígido e com ar de cristal. A direção é
  uma chama de energia com a base luminosa, o miolo claro e as línguas assimétricas.
- **Feito** (`ferramentas/prototipos/hud/itens-lote-noite/poder_r2/`):
  - o 24 e o 32 desenhados na grade;
  - as fontes em camadas pintadas no Aseprite pelo MCP;
  - a exportação reproduzível, igual às grades (o 64 é o 32 ×2);
  - o `grades.py` ganhou `--pasta` e a peça `attr-poder`.
- **Conferido:**
  - a 1920×945: o atual, o candidato anterior e a nova proposta, na ficha e no selo;
  - a suíte, o gabarito e o pyflakes. A fumaça não foi repetida: nenhum arquivo do jogo mudou desde a última, que
    passou (antes de `b266714`).
- **Próximo:** Jean avaliar o Poder. A doca vem depois. A versão não mudou (1.122.0).

### 18/10/2026 (data do computador local) — Poder no jogo (1.123.0): os quatro atributos concluídos

- **Pedido de Jean:** integrar o Poder da rodada 2 (`c0dbab8`) sem retoque e, depois, propor um novo Ataque e uma
  nova Defesa só no protótipo.
- **Feito:**
  - **As fontes:** foram de `poder_r2/fontes/` para `ferramentas/arte/aseprite/attr-poder/` (24, 32). O 64 é o 32
    ampliado 2× (`DERIVADOS`), e `TAMANHOS` ganhou o 64.
  - **Os arquivos:** os seis do jogo são idênticos, byte a byte, aos aprovados, e `exportar_aseprite.py attr-poder
    --conferir` os reproduz.
  - **O alcance:** só o atributo Poder (`ATRIBUTO`: a ficha, o Inventário e o selo). A "chama" do Vigor, da Pena de
    Fênix e das habilidades de fogo é outro desenho e ficou como estava.
  - O `desenhar_attr_poder_pixel.py` (o candidato anterior) virou histórico.
- **Conferido:**
  - no jogo, sem injeção, a 1920×945 (`poder_r2/poder-no-jogo.png`): a ficha, o Inventário e o selo;
  - a suíte, o gabarito (sem diferença), o pyflakes e a fumaça uma vez.
- **Ataque e Defesa, rodada 2:** só no protótipo (`ferramentas/prototipos/hud/itens-lote-noite/ataque_defesa_r2/`):
  - a espada nova a 45°, com sulco, ponta aguda e guarda curta;
  - o escudo virado, com a espessura à vista, a face convexa e a bossa;
  - 24 e 32 desenhados, fontes em camadas pintadas pelo MCP, exportação igual às grades (o 64 é o 32 ×2);
  - conferido a 1920×945 contra os atuais, na ficha, no Inventário e nos selos;
  - aguarda a avaliação; os atuais continuam no jogo.
- **Próximo:** Jean avaliar Ataque e Defesa. A doca vem depois. A versão continua 1.123.0.

### 18/10/2026 (data do computador local) — Os atributos concluídos; a doca, rodada 2: Inventário e Mapa (nada no jogo)

- **Decisão de Jean:**
  - Ataque e Defesa ficam os do jogo (1.120.0); a rodada 2 (`ataque_defesa_r2/`, `e96da95`) fica guardada como
    alternativa não escolhida;
  - os quatro atributos estão concluídos, com o Poder integrado na 1.123.0.
- **Pedido:** começar a doca, dois atalhos por vez: o Inventário (uma mochila de aventureiro) e o Mapa (um mapa físico).
- **Feito** (`ferramentas/prototipos/hud/itens-lote-noite/doca_r2/`):
  - **A mochila:** de couro, com a aba, a fivela, os bolsos e o cobertor enrolado.
  - **O mapa:** em sanfona, com o percurso tracejado até o X.
  - **Os arquivos:** o 36 primeiro e o 32 com a mesma construção, as fontes em camadas pintadas pelo MCP e a
    exportação igual às grades.
  - **As ferramentas:** o `grades.py` ganhou os mapas de camadas; o `fotografar.mjs` ganhou a doca com a tela aberta.
- **Conferido:**
  - a 1920×945: a doca inteira e os recortes em tamanho real e ampliados, normais e com a tela aberta;
  - a suíte, o gabarito e o pyflakes. A fumaça não foi repetida: nenhum arquivo do jogo mudou desde `2018add`.
- **Próximo:** Jean avaliar o Inventário e o Mapa. Os outros seis atalhos ficam para os próximos pares. A versão
  continua 1.123.0.

### 18/10/2026 (data do computador local) — Inventário e Mapa da doca no jogo (1.124.0)

- **Pedido de Jean:** integrar o Inventário e o Mapa da rodada 2 da doca (`c02e566`) sem retoque.
- **Feito:**
  - **As fontes:** foram de `doca_r2/fontes/` para `ferramentas/arte/aseprite/atalho-inventario/` e `atalho-mapa/`
    (36 e 32, sem derivado).
  - **Os arquivos:** os oito do jogo são idênticos, byte a byte, aos aprovados, e `exportar_aseprite.py <peça>
    --conferir` os reproduz.
  - **O alcance:** só os atalhos da doca (`ATALHO`, `Icones.atalho`); nenhum outro papel usa esses arquivos. O
    `desenhar_doca_pixel.py` (a primeira proposta) virou histórico.
- **Conferido:**
  - no jogo, sem injeção, a 1920×945 (`doca_r2/inventario-mapa-no-jogo.png`): a doca inteira, o Inventário aberto pela
    doca com o atalho selecionado e o Mapa aberto (o escurecimento da tela do mapa ficou como estava);
  - o tamanho, a posição, os textos e os cliques da doca não mudaram;
  - a suíte, o gabarito, o pyflakes e a fumaça uma vez.
- **Próximo:** os outros seis atalhos da doca, em pares.

### 18/10/2026 (data do computador local) — A doca, rodada 3: Grimório e Diário (nada no jogo)

- **Pedido de Jean:** o próximo par da doca, só no protótipo, com o Inventário e o Mapa (1.124.0) como referência.
- **Feito** (`ferramentas/prototipos/hud/itens-lote-noite/doca_r3/`):
  - **O Grimório:** fechado e em pé, com a lombada, as cantoneiras, o fecho, as páginas à vista e a gema.
  - **O Diário:** aberto, com as páginas em arco, as anotações, a pena e a fita.
  - **Os arquivos:** o 36 e o 32 (os tamanhos usados: a doca e o Habilidades da luta), as fontes em camadas pintadas
    pelo MCP e a exportação igual às grades.
  - **As ferramentas:** o `fotografar.mjs` ganhou as peças `doca_r3` e `doca_r3_luta`.
- **Conferido:**
  - a 1920×945: a doca inteira, os recortes normais e com a tela aberta, e o Habilidades na luta;
  - a suíte, o gabarito e o pyflakes. A fumaça não foi repetida: nenhum arquivo do jogo mudou desde `a8e38cd`.
- **Próximo:** Jean avaliar o Grimório e o Diário. Talentos, Bestiário, Salvar e Sair ficam para depois. A versão
  continua 1.124.0.

### 18/10/2026 (data do computador local) — O Diário da doca no jogo (1.125.0); o Grimório em refinamento

- **Pedido de Jean:** integrar o Diário (`666b806`) sem retoque; refinar o Grimório: a perspectiva, o emblema e o
  fecho, o volume da capa.
- **O Diário:**
  - as fontes foram para `ferramentas/arte/aseprite/atalho-diario/` (36 e 32);
  - os quatro arquivos do jogo são idênticos, byte a byte, aos aprovados, e o exportador os reproduz;
  - só o atalho da doca (`ATALHO`) usa o desenho.
  - Conferido no jogo, sem injeção, a 1920×945 (`doca_r3/diario-no-jogo.png`): a doca e o Diário aberto, com o atalho
    selecionado. A suíte, o gabarito, o pyflakes e a fumaça passaram uma vez.
- **O Grimório, rodada 2:** só no protótipo (`doca_r3/`); o anterior está em `doca_r3/grimorio_r1/`.
  - O livro passou a ser um objeto só, visto de cima e da esquerda: a capa, a lombada com as nervuras inclinadas e a
    borda das folhas entre as capas.
  - O emblema ficou menor e centrado, com o fecho preso à beira.
  - A capa tem poucos planos de luz.
  - Conferido antes × depois a 1920×945, na doca e no Habilidades.
  - Aguarda a avaliação.
- **Próximo:** Jean avaliar o Grimório. Talentos, Bestiário, Salvar e Sair ficam para depois.

### 18/10/2026 (data do computador local) — O Grimório da doca, rodada 3 (nada no jogo)

- **Pedido de Jean:** recomeçar o Grimório a partir das referências; a geometria primeiro (duas capas finas, o bloco
  de folhas entre elas, a lombada, um ângulo só), depois a identidade.
- **Feito** (`ferramentas/prototipos/hud/itens-lote-noite/doca_r3/`):
  - **A construção:** o livro modelado como um objeto 3D simples na projeção da referência principal (girado; a capa,
    a lombada à esquerda e as folhas embaixo), em `auxiliares/grimorio_livro.py`.
  - **A identidade:** o couro violeta, as nervuras, a moldura, a estrela de latão luminosa, os cravos e a fita.
  - **Os arquivos:** o 36 e o 32 do mesmo modelo, as fontes em camadas pintadas pelo MCP e a exportação igual às
    grades.
  - **Guardadas:** as rodadas 1 e 2, em `grimorio_r1/` e `grimorio_r2/`.
  - **As referências:** dos dois livros violeta citados, nenhum veio anexado.
- **Conferido:**
  - a produção × a rodada 2 × a rodada 3 a 1920×945, na doca e no Habilidades;
  - a suíte, o gabarito e o pyflakes. A fumaça não foi repetida: nenhum arquivo do jogo mudou desde `6742ba9`.
- **Próximo:** Jean avaliar o Grimório. Talentos, Bestiário, Salvar e Sair ficam para depois.

### 18/10/2026 (data do computador local) — O Grimório da doca no jogo (1.126.0); a skill de livros

- **Pedido de Jean:** integrar o Grimório da rodada 3 (`61dcb81`) sem retoque, e registrar o aprendizado numa skill de
  livros.
- **O Grimório:**
  - as fontes foram para `ferramentas/arte/aseprite/atalho-grimorio/` (36 e 32);
  - os quatro arquivos do jogo são idênticos, byte a byte, aos aprovados, e o exportador os reproduz;
  - vale para o atalho da doca e para o comando Habilidades da luta (`ACAO.grimorio`), sem mudança de mapeamento.
  - Conferido no jogo, sem injeção, a 1920×945 (`doca_r3/grimorio-no-jogo.png`). A suíte, o gabarito, o pyflakes e a
    fumaça passaram uma vez.
- **A skill de livros:** `.claude/skills/arte-livros-fenda/`, com `SKILL.md` e `exemplos.md`, para usar junto da
  `arte-itens-fenda` (que ganhou a indicação de consultá-la).
  - **Os princípios:** a referência principal e o papel de cada secundária; as quatro partes ligadas num ângulo só; os
    volumes sem decoração primeiro; a decoração no plano onde está; o emblema na área útil e o espaço do fecho
    reservado; o tamanho real.
  - **Os problemas recorrentes:** o L, as folhas no ângulo errado, o bloco com tampa, o emblema fora do plano, o fecho
    esmagado.
  - **Os exemplos:** o Grimório da doca, o Diário, o grimório do equipamento e os candidatos recusados, com os motivos.
    O entreaberto ficou marcado como não validado.
  - **Validada** pelo `quick_validate.py` do skill-creator, e os caminhos citados existem.
- **Próximo:** Talentos, Bestiário, Salvar e Sair, em pares. A versão é a 1.126.0.

### 18/10/2026 (data do computador local) — A doca, rodada 4: Talentos e Comitiva (nada no jogo)

- **Pedido de Jean:** o próximo par, só no protótipo: os Talentos e a Comitiva, um conceito novo de grupo de
  aventureiros no lugar do sprite de bandido.
- **Feito** (`ferramentas/prototipos/hud/itens-lote-noite/doca_r4/`):
  - **A Comitiva:** três viajantes (capuz, chapéu, ombreiras), num arquivo novo, `atalho-comitiva`. O papel entra só
    na página da proposta, e o sprite `humano` (personagem e inimigo) não muda.
  - **Os Talentos:** a árvore de latão com galhos curvos, os nós de gema e o caminho não escolhido.
  - **Os arquivos:** o 36 e o 32, as fontes em camadas pintadas pelo MCP e a exportação igual às grades.
  - **As ferramentas:** o `fotografar.mjs` ganhou o `papel_atalho` e as peças `doca_r4` e `doca_r4_telas`.
  - **O plano:** registra os nove atalhos da doca, com a Comitiva.
- **Conferido:**
  - a 1920×945: a doca com companheiro e o selo de pontos, e os recortes normais e com as telas abertas;
  - a suíte, o gabarito e o pyflakes. A fumaça não foi repetida: nenhum arquivo do jogo mudou desde `02c7f6d`.
- **Próximo:** Jean avaliar os Talentos e a Comitiva. Bestiário, Salvar e Sair ficam para depois. A versão continua
  1.126.0.

### 18/10/2026 (data do computador local) — Talentos e Comitiva no jogo (1.127.0); propostas de Bestiário, Salvar e Sair

- **Pedido de Jean:** integrar os Talentos e a Comitiva (`4deb386`) sem retoque, e depois propor o Bestiário, o Salvar
  e o Sair, só no protótipo, antes de parar.
- **A integração:**
  - as fontes foram para `ferramentas/arte/aseprite/atalho-talentos/` e `atalho-comitiva/` (36 e 32);
  - os oito arquivos do jogo são idênticos, byte a byte, aos aprovados, e o exportador os reproduz;
  - a Comitiva ganhou papel próprio em `Icones` (`ATALHO`, `TAMANHOS`). O sprite `humano` continua o de personagem e
    de inimigo, e o atalho continua aparecendo só com companheiro.
  - Conferido no jogo, sem injeção, a 1920×945 (`doca_r4/talentos-comitiva-no-jogo.png`): a doca com companheiro e o
    selo de pontos, a Comitiva aberta (selecionada) e os Talentos abertos. A suíte, o gabarito, o pyflakes e a fumaça
    passaram uma vez.
- **As propostas do Bestiário, do Salvar e do Sair:** só no protótipo
  (`ferramentas/prototipos/hud/itens-lote-noite/doca_r5/`).
  - **O Bestiário:** o crânio de criatura com chifres e a boca refeita pelo retorno do Jean, com a arcada e os dentes
    de cima e de baixo e o queixo.
  - **O Salvar:** o baú aberto com a seta de aço.
  - **O Sair:** o arco de pedra com o vão fundo e a seta laranja.
  - **Os arquivos:** o 36 e o 32, as fontes pintadas pelo MCP e a exportação igual às grades.
  - **Conferido:** sobre o carvão e na doca, a 1920×945. A suíte, o gabarito e o pyflakes passaram (a fumaça foi a da
    integração, porque o jogo não mudou depois).
- **Próximo:** Jean avaliar o Bestiário, o Salvar e o Sair. Com eles aprovados, a doca fica completa. A versão é a
  1.127.0.
- **O Bestiário, rodada 3:** a parte de baixo foi refeita no Aseprite, pela referência de crânio de fera do Jean.
  - **A forma:** o focinho longo e os dentes em grupos pendurados da arcada, presos por sombra, sem a barra com duas
    pontas.
  - **Guardadas:** as rodadas 1 e 2, em `doca_r5/`.
- **O Bestiário, rodada 4:** um retoque local no Aseprite, só a ligação entre o focinho e a arcada.
  - **O que mudou:** os planos de luz e sombra continuam até a raiz dos dentes, e as fendas começam em alturas
    diferentes. A silhueta não mudou.
  - **Guardada:** a rodada 3, em `doca_r5/bestiario_r3/`.
  - **Aguardam a avaliação:** o Bestiário, o Salvar e o Sair.

### 18/10/2026 (data do computador local) — O Bestiário da doca no jogo (1.128.0)

- **Pedido de Jean:** integrar o Bestiário de `e373618` sem retoque, a partir das fontes finais editadas, e
  reapresentar o Salvar e o Sair como estão.
- **Feito:**
  - as fontes foram para `ferramentas/arte/aseprite/atalho-bestiario/`;
  - os quatro arquivos do jogo são idênticos, byte a byte, aos aprovados, e o exportador os reproduz;
  - o papel é só o atalho (`ATALHO`). A "caveira" 16×16 dos retratos, da derrota e da fome não mudou.
- **Conferido:**
  - no jogo, sem injeção, a 1920×945 (`doca_r5/bestiario-no-jogo.png`): a doca e o Bestiário aberto, com o atalho
    selecionado;
  - a suíte, o gabarito, o pyflakes e a fumaça uma vez.
- **Continuam:** o Salvar e o Sair, no protótipo, aguardando a avaliação.

### 18/10/2026 (data do computador local) — O Salvar e o Sair no jogo (1.129.0): a doca concluída; propostas de Vida e Mana

- **Pedido de Jean:** integrar o Salvar e o Sair (`a872915`/`682b189`) sem retoque; depois propor a Vida e a Mana
  (grupo Vida e recursos), só no protótipo.
- **A integração:**
  - as fontes foram para `ferramentas/arte/aseprite/atalho-salvar/` e `atalho-sair/`;
  - os oito arquivos do jogo são idênticos, byte a byte, aos aprovados, e o exportador os reproduz;
  - só os atalhos da doca usam os desenhos;
  - os nove atalhos da doca estão concluídos, e o resumo da linha 1D do plano foi corrigido.
  - Conferido numa partida de teste, com os saves numa pasta temporária (`doca_r5/salvar-sair-no-jogo.png`): o Salvar
    grava, e o Sair abre a pergunta (não confirmada). A suíte, o gabarito, o pyflakes e a fumaça passaram uma vez.
- **As propostas de Vida e Mana:** só no protótipo (`ferramentas/prototipos/hud/itens-lote-noite/vida_mana/`), nada
  no jogo; aguardam a avaliação do Jean.
  - **Os usos:** só o topo, em 20 px; desenhadas direto em 20, sem outros tamanhos.
  - **A Vida:** um coração vermelho com volume (luz no lobo da esquerda, a volta de baixo mais funda).
  - **A Mana:** uma gota de energia líquida no azul da barra, com o miolo aceso e o reflexo em crescente, sem halo;
    separada do raio do Vigor, da estrela do Foco e da chama do Poder.
  - Pintadas no Aseprite pelo MCP (`pintar.lua`), exportadas pelo `exportar_aseprite.py --fontes=`, conferidas no
    topo de uma partida de Mago a 1920×945 (`vida_mana/vida-mana-topo.png`). Barras, números, cores e regras não
    mudaram.

### 18/10/2026 (data do computador local) — A Vida aprovada; a Mana sem o miolo aceso (proposta)

- **Pedido de Jean:** o coração de `a914f18` aprovado, sem alterações; na gota, tirar só o bloco quadrado de luz do
  centro, mantendo o reflexo, a sombra, a silhueta e o resto. Vida e Mana entram juntas depois da conferência.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/vida_mana/`): os 16 pixels do bloco viraram
  o azul em volta, na fonte em camadas, pelo MCP; o exportado confere com o editor e o @2x é exato. A rodada 1 está em
  `vida_mana/mana_r1/`; o antes e o depois no topo do Mago, em `vida_mana/mana-r2-antes-depois.png`. Nada no jogo.

### 18/10/2026 (data do computador local) — A Vida e a Mana no jogo (1.130.0); propostas de Vigor e Foco

- **Pedido de Jean:** integrar a Vida (`a914f18`) e a Mana (`f02566d`) sem retoque; depois propor o Vigor e o Foco, só
  no protótipo.
- **A integração:**
  - as fontes foram para `ferramentas/arte/aseprite/vital-vida/` e `vital-mana/`;
  - os quatro arquivos do jogo são idênticos, byte a byte, aos aprovados, e o exportador os reproduz;
  - o único uso é o topo (`Icones.vital`, 20 px); barras, preenchimentos, números, posição, regras e animações não
    mudaram.
- **As propostas de Vigor e Foco:** só no protótipo (`ferramentas/prototipos/hud/itens-lote-noite/vigor_foco/`),
  nada no jogo; aguardam a avaliação do Jean.
  - **O Vigor:** o punho cerrado com três línguas de fogo saindo dos nós, pela ideia e pelas referências de punho do
    Jean (o raio da primeira proposta ficou em `recusados/`).
  - **O Foco:** um alvo de anéis com as marcas da mira, no verde da barra de foco (a estrela atual é violeta, a cor
    do Poder).
  - Pintados no Aseprite pelo MCP, um por vez; exportados pelo `exportar_aseprite.py --fontes=`; fotos no topo do
    Guerreiro e do Arqueiro a 1920×945 e os quatro símbolos juntos (`vigor_foco/vigor-foco-topo.png`).

### 18/10/2026 (data do computador local) — O Sair alinhado na doca (1.130.1)

- **Pedido de Jean:** a porta do Sair parecia deslocada para a esquerda da palavra; alinhar o ícone opticamente, sem
  mudar desenho, tamanho, texto, espaço do botão nem área de clique.
- **Feito:** em `css/14-hud.css`, o desenho do Sair anda 4 px para a direita (`position: relative; left: 4px`, inteiro,
  sem borrar). A 1920×945, o centro da porta fica a 1,5 px do centro da palavra (antes, 5,5 px); a seta continua
  dentro do botão, e o botão, o texto e o clique ficaram com as mesmas medidas. Comparados 2, 3 e 4 px na doca real;
  antes e depois em `ferramentas/prototipos/hud/itens-lote-noite/doca_r5/sair-alinhado.png`.

### 18/10/2026 (data do computador local) — O Vigor refeito: o punho cerrado (proposta)

- **Pedido de Jean:** o punho de `1a1dae3` lia como mão aberta; refazer no Aseprite, primeiro o punho sem fogo
  (dedos dobrados num volume compacto, os nós, o polegar pela frente, o pulso), depois o fogo como elemento
  secundário. O Foco fica como está; nada nos símbolos integrados.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/vigor_foco/`): o punho de frente pela
  palma, num bloco mais largo que alto, com o polegar deitado na frente; o fogo como uma labareda atrás do lado
  direito (as versões com fogo dos dois lados ou em volta do topo voltavam a parecer uma cabeça). A proposta anterior
  está em `vigor_foco/recusados/vigor-punho-r1/`; o antes e o depois no topo do Guerreiro, as etapas e os quatro
  símbolos em `vigor_foco/vigor-punho-r2.png`. Nada no jogo.

### 18/10/2026 (data do computador local) — O Vigor sem fogo (proposta)

- **Pedido de Jean:** usar o punho da rodada 2 (`2c4bf85`) sem a labareda, recentrado no quadro, sem aumentar a mão;
  reapresentar o Foco inalterado para avaliar o par.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/vigor_foco/`): na fonte em camadas, pelo
  MCP, saiu a camada da chama e o contorno dela, o punho andou 2 px para a direita e 2 para cima, e a base do pulso
  fechou com o contorno; a mão é a mesma, pixel a pixel. A versão com fogo está em `recusados/vigor-punho-r2-fogo/`.
  Fotos no topo do Guerreiro e do Arqueiro a 1920×945 e os quatro símbolos em `vigor_foco/vigor-punho-r3.png`. Nada
  no jogo.

### 18/10/2026 (data do computador local) — O Vigor e o Foco no jogo (1.131.0): os quatro recursos do topo

- **Pedido de Jean:** integrar o Vigor (o punho sem fogo, `4eea5b6`) e o Foco (o alvo verde, `1a1dae3`) sem retoque, e
  parar depois desta integração.
- **A integração:**
  - as fontes foram para `ferramentas/arte/aseprite/vital-vigor/` e `vital-foco/`;
  - os quatro arquivos do jogo são idênticos, byte a byte, aos aprovados, e o exportador os reproduz;
  - o único uso é o topo (`Icones.vital`, 20 px); o custo das habilidades continua com os sprites do jogo, e barras,
    números, posições, áreas de interação e regras não mudaram;
  - os quatro ícones das barras do topo (Vida, Mana, Vigor, Foco) estão em pixel art.

### 18/10/2026 (data do computador local) — Propostas de Ouro e Provisões

- **Pedido de Jean:** Ouro e Provisões, uma peça por vez, só no protótipo, conferindo antes os usos e o que as
  Provisões representam.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/ouro_provisoes/`), nada no jogo:
  - **Ouro** (24, o único uso é o topo): uma pilha de moedas com uma moeda apoiada na frente.
  - **Provisões** (24 no topo e 32 no cartão do mercado, que hoje reduz o @2x do 24): o pernil curado com o osso,
    fazendo par com o osso do topo; os barbantes da primeira versão saíram a pedido do Jean (guardada em
    `recusados/`).
  - Desenhados em etapas no Aseprite pelo MCP; fotos a 1920×945 no mercado (topo e cartão) e a prancha sobre o carvão
    em `ouro_provisoes/ouro-provisoes.png`.
- **Limitações:** a integração precisa do 32 no `TAMANHOS` das Provisões; o ouro do mercado e dos serviços continua
  com o sprite do jogo.

### 18/10/2026 (data do computador local) — O Ouro e as Provisões no jogo (1.132.0)

- **Pedido de Jean:** integrar o Ouro e as Provisões do `33d8a6c` sem retoque, e parar depois desta integração.
- **A integração:**
  - as fontes foram para `ferramentas/arte/aseprite/moedas/` e `provisoes/`;
  - os seis arquivos do jogo são idênticos, byte a byte, aos aprovados, e o exportador os reproduz;
  - o **Ouro do topo** (24) é a pilha de moedas; o ouro do mercado e dos serviços (`ouro-loja`) continua com o sprite
    do jogo, uso pendente, não tratado aqui;
  - as **Provisões** (o pernil) estão no topo (24) e no cartão "Provisões (1 dia)" do mercado, agora no 32 nativo em
    vez do @2x do 24 reduzido; sem comida, o topo continua com o osso;
  - conferido a 1920×945 no mercado do Guerreiro, com saves temporários: medidas do cartão, dos botões e do topo iguais
    às de antes; a compra de 1 e de 2 Provisões dá os mesmos números de antes (4 → 5 → 7 dias; 300 → 296 → 288 de
    ouro), e o topo acompanha. Preços, quantidades e regras não mudaram.

### 18/10/2026 (data do computador local) — O Ouro no balcão do mercado e dos serviços (1.133.0)

- **Pedido de Jean:** trocar o ícone do seu ouro no mercado e nos serviços pelas moedas aprovadas, preservando a
  construção, os valores, os textos, o alinhamento e as áreas de clique; só os usos de dinheiro.
- **Os usos conferidos:** o saldo no topo do balcão (`.ouro-loja`, 32 px) no mercado e nos quatro serviços que mostram
  o seu ouro (ferreiro, curandeira, templo, taverna; `telas/mercado.js` e `topoBalcao` em `telas/servicos.js`). Usava o
  sprite `moedas` do jogo ampliado 2×; o sprite fica para os papéis dele, a troca é pelo `Icones.ouro`.
- **O desenho:** um 32 próprio, derivado da construção do 24 aprovado (as medidas escaladas e as moedas da pilha com
  3 px de altura), pintado no Aseprite pelo MCP (`ferramentas/arte/aseprite/moedas/moedas-32.aseprite`), sem retoque.
- **Conferido a 1920×945:** nos cinco lugares, as medidas do ouro, do ícone e do topo do balcão e o texto são iguais aos
  de antes (`ouro_provisoes/capturas/ouro-loja/`).
- **Dinheiro ainda com o desenho antigo** (o sprite `moeda`, uma moeda só, outro tamanho e outro papel): os preços do
  mercado e dos serviços (16), a linha de ouro do espólio, os ganhos da celebração, o prêmio do contrato, o chip de ouro
  do relatório e as moedas que voam até o topo.

### 18/10/2026 (data do computador local) — Propostas da moeda avulsa e da tocha

- **Pedido de Jean:** a moeda avulsa e a tocha, uma peça por vez, só no protótipo, no Aseprite pelo MCP.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/moeda_tocha/`), nada no jogo:
  - **a moeda avulsa** (16 e 32): a moeda da frente da pilha aprovada, sozinha, com a espessura embaixo à direita; nos
    preços, no mural, no chip e no voo das moedas (16), no espólio (32);
  - **a tocha** (24 e 32): cabo de madeira, cabeça de pano enrolado e chama em gota com línguas; no topo (24), no cartão
    do mercado e na bolsa (32). Os 48 e 64 da tocha atual não aparecem parados em nenhum lugar.
  - Fontes em camadas pintadas pelo `pintar.lua`; exportadas pelo `exportar_aseprite.py --fontes=` (o composto igual ao
    editor, os @2x exatos); fotos a 1920×945 atual × proposta com os mesmos dados (`moeda-no-jogo.png`,
    `tocha-no-jogo.png`) e a prancha sobre o carvão.
- **Limitações:** a moeda não tem papel em `Icones` (a página da proposta o recebe só nas fotos); a moeda do ladrão na
  luta não foi fotografada; a tocha proposta é mais leve que a atual no topo (ponto a avaliar).

### 18/10/2026 (data do computador local) — A moeda avulsa no jogo (1.134.0)

- **Pedido de Jean:** integrar a moeda avulsa do `c00d0cf` (16 e 32) sem retoque, com papel próprio no catálogo, nos
  usos mapeados; a pilha do saldo continua igual.
- **A integração:**
  - as fontes foram para `ferramentas/arte/aseprite/moeda/`; os quatro arquivos do jogo são idênticos, byte a byte, aos
    aprovados, e o exportador os reproduz;
  - o papel `Icones.moeda`: em 16, os preços do mercado e dos serviços, a linha "Custo", a dica de venda e recompra, o
    prêmio dos cartazes, os ganhos do pagamento de contratos, o chip e o aviso de ouro e as moedas que voam até o
    topo; em 32, o espólio e a moeda que o ladrão leva na luta. Valores, medidas e animações não mudaram;
  - conferido a 1920×945 com os arquivos de produção: a moeda sai com os mesmos pixels da proposta nos lugares
    fotografados, e o roubo do bandido leva seis `moeda-32.png` no voo de sempre.
- **Dinheiro ainda com o desenho do jogo:** nenhum uso de tela conhecido (o saldo é a pilha, o resto é a moeda avulsa).

### 19/10/2026 (data do computador local) — A tocha, rodada 2: a chama refinada (proposta)

- **Pedido de Jean:** refinar só a chama da tocha (o cabo, o pano e a presença no topo aprovados): sem a faixa
  horizontal larga, línguas desiguais, o miolo menos quadrado, sem halo; guardar a rodada 1, de que ele também gostou,
  para comparar e decidir.
- **Feito, só no protótipo** (`moeda_tocha/`), nada no jogo: o calor segue o eixo curvo de cada língua; a ponta em S,
  a língua da esquerda alta e aberta, a da direita curta. As fontes repintadas no Aseprite pelo MCP só nas camadas
  `chama` e `contorno`; a rodada 1 inteira em `moeda_tocha/tocha_r1/`.
- **Fotos:** o jogo, a rodada 1 e a rodada 2 no topo, no cartão do mercado e na bolsa, a 1920×945 com os mesmos dados
  (`moeda_tocha/tocha-no-jogo.png`), e a prancha sobre o carvão.

### 19/10/2026 (data do computador local) — A tocha no jogo (1.135.0)

- **Pedido de Jean:** integrar a tocha da rodada 2 (`1c6a2c2`, 24 e 32) sem retoque, e parar depois desta integração.
- **A integração:**
  - as fontes foram para `ferramentas/arte/aseprite/tocha/`; os quatro arquivos do jogo são idênticos, byte a byte,
    aos aprovados, e o exportador os reproduz;
  - o topo (24) e, em 32, o cartão do mercado, a bolsa, o espólio e o voo até a bolsa; os arquivos 48 e 64 antigos
    (placeholder, sem uso) saíram e o `TAMANHOS` ficou [24, 32]; o `familia_ferro.py` não grava mais a tocha;
  - conferido a 1920×945 com os arquivos de produção: no topo, no mercado e na bolsa, os pixels são os da rodada 2;
    o recebimento de uma tocha voa o arquivo novo do chip até o topo. Quantidades, preços, medidas e animações não
    mudaram.
- **Ainda com o desenho do jogo:** a tocha em 16 (o chip "+1 Tocha", o aviso e as escolhas que a gastam, o sprite
  16×16) e a tocha apagada do topo.
- **Achado independente, não tratado:** o `familia_ferro.py --conferir` acusa a aljava (8 arquivos) desde a 1.122.0,
  quando ela passou a vir do Aseprite sem entrar em `DESENHADOS`.

### 19/10/2026 (data do computador local) — Propostas da tocha em 16 e da tocha apagada

- **Pedido de Jean:** as variantes que faltavam da tocha, só no protótipo: o 16 como simplificação da aprovada e a
  apagada derivada dela (cabo e pano preservados, sem chama).
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/moeda_tocha/variantes/`), nada no jogo:
  - **o 16** (o chip, o aviso, o risco "−1 tocha" das escolhas): a mesma construção na grade de 16, sem retoque;
  - **a apagada** (24 no topo sem tochas, onde hoje o sprite aparece em 32; 16 no risco "Sem luz"): a ponta do pano
    queimada e dois fios de fumaça, sem cor de fogo.
  - Fontes em camadas pelo `pintar.lua`, exportação conferida, @2x exatos; fotos atual × proposta a 1920×945 com os
    mesmos dados e a prancha sobre o carvão.

### 19/10/2026 (data do computador local) — A conferência da família de ferro e a aljava (manutenção)

- **Pedido de Jean:** investigar a divergência da aljava no `familia_ferro.py --conferir` (registrada na 1.135.0) e,
  se viesse da migração para o Aseprite, fazer o gerador reconhecer essa origem.
- **A causa, confirmada:** até a 1.121 os arquivos da aljava do jogo eram exatamente a saída do gerador (conferido
  contra o `b266714^`); na 1.122.0 (`b266714`) eles passaram a sair das fontes do Aseprite, que o
  `exportar_aseprite.py aljava --conferir` reproduz byte a byte, mas o gerador continuou conferindo a peça antiga.
- **A correção:** o `familia_ferro.py` acha sozinho as peças do grupo com fonte no Aseprite (a aljava e a tocha, pelas
  pastas em `ferramentas/arte/aseprite/`); elas continuam na conta da escala do grupo (os 102 arquivos dele saem
  iguais), mas não são gravadas nem conferidas ali, e o `--conferir` indica o `exportar_aseprite.py <peça>
  --conferir` para elas. Nenhum arquivo de arte mudou; documentado em `docs/ARQUITETURA.md` e na skill
  `arte-itens-fenda`.

### 19/10/2026 (data do computador local) — A tocha em 16 e a tocha apagada no jogo (1.136.0)

- **Pedido de Jean:** integrar as três variantes do `ef71aa3` sem retoque.
- **A integração:**
  - as fontes foram para `ferramentas/arte/aseprite/tocha/` (o 16) e `tocha_apagada/`; os seis arquivos do jogo são
    idênticos, byte a byte, aos aprovados, e o exportador os reproduz; o 24 e o 32 da tocha não mudaram;
  - a tocha em 16 no chip e no aviso de um item ganho, no ícone das escolhas que a gastam, no risco "−1 tocha" e no
    aviso de escuro do painel do lugar (achado na conferência); a apagada no topo sem tochas (24, no lugar do sprite em
    32), no risco "Sem luz" e no aviso do lugar sem tocha (16). O papel novo `Icones.miudo`
    serve os 16 pedidos pelo nome (a moeda, a tocha, a apagada);
  - conferido a 1920×945 com os arquivos de produção: o ganho de uma tocha (aviso e chip), a escolha que consome uma e
    o estado sem tochas no topo e na escolha saem como nas fotos da proposta; a caixa do recurso e a escolha têm as
    mesmas medidas. Quantidades, regras, textos e áreas de interação não mudaram.
- **A tocha inteira em pixel art:** 16, 24 e 32 acesa e 16 e 24 apagada.

### 19/10/2026 (data do computador local) — A fonte de livro como única (1.137.0)

- **Pedido de Jean:** tirar a fonte pixel alternativa da história; a de livro fica como padrão único, sem o controle
  "Fonte" no topo, e quem tinha a preferência pixel salva passa sozinho para a de livro.
- **Feito:**
  - o botão "Fonte" saiu do topo (`index.html`) e o `alternarFonte` saiu de `app/controles.js`; ao iniciar, a
    preferência antiga `cdf-fonte` é apagada (protegido para armazenamento bloqueado);
  - em `css/11-tipografia.css`, as regras da `fonte-pixel` saíram; os tamanhos da prosa ficam os de sempre (21 px na
    folha, 20 nas escolhas, 18 nas secundárias);
  - a Pixeloid Sans negrito (`fontes/pixeloid-sans-bold.ttf`) saiu: era só da alternativa. A Pixeloid regular fica,
    porque é a da seta de quem abre outra escolha; a Pixelify Sans e a Jersey 15 ficam para o mostruário dos materiais
    (`tests/navegador/mostruario.html`). Logotipo e títulos (Alagard) não mudam.
  - Conferido a 1920×945 com a preferência antiga salva: a chave some, a prosa fica na Alegreya, nos mesmos tamanhos, e
    não há erro no console.

### 19/10/2026 (data do computador local) — Lote da noite, 1: propostas da Bandagem e da Poção de Vida

- **Pedido de Jean** (para a noite, com autonomia): três lotes, uma peça por vez, só no protótipo; nada integrado.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/bandagem_pocao/`), **não aprovado**:
  - **a Bandagem** (16, 24, 32): o rolo de linho deitado, a espiral solta na face, as voltas suaves e a tira solta;
  - **a Poção de Vida** (16, 24, 32): o balão de vidro com o líquido vermelho até dois terços, a superfície marcando o
    nível, a beira do vidro, o brilho agrupado e a rolha; é a base da família de frascos (`auxiliares/frasco.py`).
  - Fontes em camadas pelo `pintar.lua`, exportação conferida (o composto do editor pelo `soma.lua`), @2x exatos;
    fotos atual × proposta a 1920×945 e a prancha sobre o carvão.
- **A decidir:** o comando Itens da roda da luta é a mesma imagem da poção; o frasco vazio do topo continua o sprite.

### 19/10/2026 (data do computador local) — Lote da noite, 2: propostas do Tônico Restaurador e do Antídoto

- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/tonico_antidoto/`), **não aprovado**: a
  mesma família de frascos da nova Poção de Vida, com silhueta e fechamento próprios:
  - **o Tônico** (16, 32): a garrafa alta de paredes retas, a rolha larga, o líquido azul;
  - **o Antídoto** (16, 32): o tubo estreito de fundo redondo, lacrado com cera de abelha, o líquido verde.
- **A decidir:** os sprites de 16 (`pocao_azul`, `folha`) têm outros papéis (a Mana, a Agilidade): um 16 integrado
  pede o papel pelo id do item.

### 19/10/2026 (data do computador local) — Lote da noite, 3: propostas da Calça de Viagem e do Manto do Mago

- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/calca_manto/`), **não aprovado**, na lã do
  capuz de tecido aprovado:
  - **a Calça de Viagem** (32, 40, 48; 64 = 32 ×2): lã solta, as faixas de linho nos tornozelos, o cordão na cintura;
  - **o Manto** (32, 40, 48; 64 = 32 ×2): a veste com as mangas largas, a gola com o broche, a faixa, a frente aberta
    mostrando o forro.
- **A decidir:** o desenho `manto` vale hoje para três bases (Manto, Túnica, Veste Rúnica) e o Manto de Cinzas;
  proposta de um desenho por base (sem mudar os dados nesta rodada). As duas peças não têm papel em `Icones` hoje.
- **Os três lotes da noite** (Bandagem e Poção, Tônico e Antídoto, Calça e Manto) estão no protótipo, sem integração.

### 19/10/2026 (data do computador local) — A Bandagem, a Poção, o Tônico, a Calça de Viagem e o Manto no jogo (1.138.0)

- **Pedido de Jean:** integrar os cinco aprovados sem retoque; o Antídoto só com a base ajustada, no protótipo; e
  preparar o frasco vazio, também no protótipo.
- **A integração:**
  - as fontes foram para `ferramentas/arte/aseprite/` (bandagem, pocao, tonico, calca_tecido, manto); os 46 arquivos do
    jogo são idênticos, byte a byte, aos aprovados, e o exportador os reproduz; os 48 e 64 antigos da bandagem, da poção
    e do tônico saíram (sem uso);
  - os papéis: a calça e o manto como equipamento; a poção segue como o comando Itens da luta e o manto segue
    compartilhado (decisões do Jean); o 16 de um consumível vem pelo id do item (`Icones.pequeno`), o que preserva o
    sprite antigo do Tônico como a Mana e o Unguento;
  - conferido a 1920×945 com os arquivos do jogo (topo, mercado, bolsa, combate; ficha, Inventário, saque) e, com os
    saves temporários, a compra dos três consumíveis e o Manto vestido pelo saque. Regras, preços, atributos,
    quantidades, animações e áreas de interação não mudaram.
- **Em avaliação, fora do jogo:** o Antídoto (a base plana) e o frasco vazio do topo.

### 19/10/2026 (data do computador local) — Propostas: a base do Antídoto e o frasco vazio

- **Feito, só no protótipo, não aprovado:**
  - **o Antídoto** (16, 32; `tonico_antidoto/`): a base curta e plana com os cantos arredondados, o resto igual (só as
    linhas da base mudaram); a versão anterior em `tonico_antidoto/recusados/antidoto-base-redonda/`;
  - **o frasco vazio** (24; `bandagem_pocao/variantes/`): a Poção de Vida aprovada sem o líquido, para o topo sem poções
    (hoje o sprite em 32).
  - Fontes pelo `pintar.lua`, exportação conferida, @2x exatos; antes × depois do Antídoto no jogo e ampliado; cheia ×
    vazia no topo a 1920×945.

### 19/10/2026 (data do computador local) — O Antídoto e o frasco vazio no jogo (1.139.0)

- **Pedido de Jean:** integrar o Antídoto com a base plana e o frasco vazio do `b872544`, sem retoque.
- **A integração:**
  - as fontes foram para `ferramentas/arte/aseprite/antidoto/` e `frasco_vazio/`; os seis arquivos do jogo são
    idênticos, byte a byte, aos aprovados, e o exportador os reproduz; os 48 e 64 antigos do Antídoto saíram;
  - o Antídoto em 32 nos consumíveis e em 16 pelo item (a `folha` antiga segue como a Agilidade); o frasco vazio no
    topo sem poções, em 24, no lugar do sprite em 32;
  - conferido a 1920×945 com os arquivos do jogo e um save temporário: o Antídoto no mercado, na bolsa e no aviso de
    ganho; o topo sem poções, a compra (a passagem para com poções) e o gole (a volta), com a caixa do recurso igual.
    Preços, efeitos, quantidades e o comportamento do recurso não mudaram.
- **A família de frascos inteira em pixel art:** a Poção de Vida, o frasco vazio, o Tônico e o Antídoto.

### 19/10/2026 (data do computador local) — Propostas do anel e do amuleto

- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/anel_amuleto/`), **não aprovado**, no latão
  do escudo aprovado:
  - **o anel** (32, 40, 48; 64 = 32 ×2): o aro em três quartos com a abertura vazada, a parede de dentro e a granada no
    engaste;
  - **o amuleto** (32, 40, 48; 64 = 32 ×2): o medalhão com a borda em relevo e o botão, a argola e o cordão de couro em
    gota passando por ela.
- **Alcance e limitações:** o anel vale para Anel, Sinete, Aro e o Anel do Último Rei, e o amuleto para Amuleto,
  Talismã, Pingente e Medalhão; os espaços vazios usam a mesma imagem (mudam junto). O Aro (liso) e o Sinete (de selo)
  pediriam desenhos próprios, se o Jean quiser; os dados não mudaram.

### 19/10/2026 (data do computador local) — O anel e o amuleto, rodada 2 (propostas)

- **Pedido de Jean:** refazer os dois, só no protótipo: o anel pela prancha de referência (o aro em pé, de três
  quartos, a abertura em diagonal, a espessura), básico, sem pedra nem decoração; o amuleto com uma gema violeta num
  engaste de latão, o pingente alongado. Guardar a prancha como referência permanente.
- **Feito:** a prancha em `ferramentas/arte/referencias/aneis/` e na skill (`referencias-aneis.md`: o ângulo preferido
  dos anéis; os efeitos são exemplos para acessórios especiais). **A rodada 1 não foi escolhida** (guardada em
  `anel_amuleto/rodada1/`). **Aguardando avaliação:** o anel de ouro em pé, modelado como um cilindro curto, com o
  acabamento do sample que o Jean mandou (o chanfro nas bordas); o amuleto com a gema violeta alongada no engaste de
  latão e o cordão em gota. 32, 40, 48 e o 64 = 32 ×2; fotos produção × anterior × nova a 1920×945.

### 19/10/2026 (data do computador local) — O anel, rodada 3 (proposta); o amuleto aprovado

- **O amuleto da rodada 2 está aprovado** (a gema violeta no engaste de latão), sem retoque e ainda não integrado.
- **O anel da rodada 2 não foi escolhido** (guardado em `anel_amuleto/rodada2/`).
- **As referências:** os PNGs originais em `ferramentas/arte/referencias/aneis/`; a principal é `sample (2).png` (o
  ângulo, a abertura e a espessura), as pranchas do mesmo artista são secundárias (o acabamento). Hierarquia na skill.
- **Aguardando avaliação:** o anel da rodada 3, com o ângulo e as proporções da referência principal (o modelo do aro
  ajustado pela sobreposição da silhueta e do vão), o metal em poucos planos e um ornamento leve (um ziguezague gravado,
  liberado pelo Jean; a versão lisa como alternativa). 32, 40, 48 e o 64 = 32 ×2.

### 19/10/2026 (data do computador local) — O anel e o amuleto no jogo (1.140.0)

- **Pedido de Jean:** integrar o anel da rodada 3 (com o ziguezague) e o amuleto violeta da rodada 2, sem retoque; a
  alternativa lisa fica como histórico.
- **A integração:**
  - as fontes foram para `ferramentas/arte/aseprite/anel/` e `amuleto/`; os 16 arquivos do jogo (32, 40, 48 e o 64 =
    32 ×2) são idênticos, byte a byte, aos aprovados, e o exportador os reproduz;
  - os compartilhamentos seguem (o anel: Anel, Sinete, Aro, o Anel do Último Rei; o amuleto: Amuleto, Talismã,
    Pingente, Medalhão), e os espaços vazios acompanham, apagados;
  - conferido a 1920×945 com os arquivos do jogo e os saves temporários: a ficha e o Inventário com um anel vestido e o
    outro vazio, a comparação no saque e o anel equipado no espaço vazio, o amuleto equipado. Atributos, preços,
    regras, áreas de interação e animações não mudaram.

### 19/10/2026 (data do computador local) — A skill dos anéis (`arte-aneis-fenda`)

- **Pedido de Jean:** uma skill especializada em anéis, na organização da de livros, complementando a
  `arte-itens-fenda` (que agora indica consultá-la quando o objeto for um anel).
- **Feito:** `.claude/skills/arte-aneis-fenda/SKILL.md` (as referências e a hierarquia, sem duplicar os PNGs de
  `ferramentas/arte/referencias/aneis/`; a perspectiva preferida; a construção do aro antes de pedra, engaste ou
  ornamento; a comparação com a referência principal, com o modelo 3D e a sobreposição como ajuda; o metal; os anéis
  básicos e avançados, sem impor efeitos nem animações; os tamanhos; as ferramentas; os problemas já vistos; a entrega)
  e `exemplos.md` (a rodada 3 aprovada, a alternativa lisa e as rodadas recusadas, com os problemas). A autoria e a
  origem das referências não foram informadas e não estão inventadas. Nenhum anel novo.

### 19/10/2026 (data do computador local) — Conferência dos equipamentos que ainda pedem arte

- **Pedido de Jean:** um levantamento curto dos equipamentos das classes, para escolher o próximo par sem repetir
  trabalho aprovado; só documentação.
- **Feito:** a tabela por desenho no plano 23 (seção 1.2.1), cruzando os dados, os papéis em `Icones` e as fontes.
  **Arte ainda por fazer:** a Sandália (a única base dos pés do Mago), o Chapéu Pontudo, o Diadema (com o único Coroa
  dos Afogados) e a Besta Leve; o resto está aprovado e integrado, e nenhuma proposta está pendente.
- **Recomendação:** a Sandália e o Chapéu Pontudo (o placeholder mais frequente e o vestuário do Mago completo); depois
  a Besta Leve e o Diadema. **Dúvidas registradas, sem reabrir:** a família de ferro pintada (anterior ao método atual)
  e o martelo em código (sem 40, o 48 reduzido pelo navegador). A lista de lacunas da `docs/ARQUITETURA.md` foi
  corrigida (a calça de tecido saiu; a Besta Leve e a Coroa dos Afogados entraram). Nada no jogo mudou.

### 19/10/2026 (data do computador local) — Correção da conferência: a família de ferro é placeholder

- **Pedido de Jean:** a conferência anterior contou só quatro peças por fazer; a família de ferro derivada da arte
  pintada é placeholder e precisa ser refeita no padrão atual, mesmo aprovada para uso antes. Separar as situações,
  revisar o ferro peça a peça pela fonte real e corrigir o total. Só registros.
- **Feito:** a seção 1.2.1 do plano 23 reescrita, com a fonte de cada peça de ferro e quatro situações (mais "a
  decidir"). **Placeholder pendente de remake:** a espada, a maça, o elmo, a cota, a manopla, as perneiras e as botas de
  ferro, todas reduções da pintura (`familia_ferro.py --conferir`: tudo igual; os PNGs não mudaram desde `58c20d8`).
  **Desenho próprio no padrão atual:** o escudo (1.94.0) e o machado (1.99.0). **A decidir:** o martelo (grade de 32 em
  `desenhos.js`, não da pintura, mas sem 40 e com o 48 pelo navegador). **Inexistentes:** Besta Leve, Chapéu Pontudo,
  Diadema, Sandália. **Final:** 19 de 31; o Guerreiro não está concluído.
- **Ordem recomendada, à parte da contagem:** Sandália e Chapéu Pontudo primeiro; depois a Besta Leve, o Diadema e o
  remake do ferro como lote próprio (ele muda também as silhuetas dos espaços vazios e o comando de ataque). A lista de
  lacunas da `docs/ARQUITETURA.md` ganhou a família de ferro e o martelo. Nada no jogo mudou.

### 19/10/2026 (data do computador local) — A Sandália e o Chapéu Pontudo do Mago (proposta); a decisão do martelo

- **Pedido de Jean:** o par do Mago, uma peça por vez, só no protótipo, com a skill `arte-itens-fenda` e as fontes no
  Aseprite pelo MCP; e a decisão do martelo.
- **O martelo:** o desenho aprovado fica preservado; a pendência é completar o 40 e o 48 mantendo a construção, sem
  redesenho. Execução em outra entrega (plano 23, seção 1.2.1; a lacuna da `docs/ARQUITETURA.md` atualizada).
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/sandalia_chapeu/`), **não aprovado**:
  - **a Sandália** (32, 40, 48; 64 = 32 ×2): de lado, a sola grossa de couro com a palmilha, a gaiola de tiras (as
    alças dos dedos e do peito do pé, as subidas e o anel do tornozelo), vazia; um laço de linho no anel;
  - **o Chapéu Pontudo** (32, 40, 48; 64 = 32 ×2): a aba em perspectiva, a copa de lã em cone com a ponta tombada para
    a direita, o vinco e as dobras, a fita de linho na base.
  - Fontes em camadas pelo `pintar.lua`; o composto do editor, os PNGs exportados e a prévia conferem; @2x exatos.
  - Fotos a 1920×945 (ficha, Inventário, saque) e o conjunto de tecido lado a lado (`conjunto-mago-32.png`).
- **O alcance:** os dois desenhos não têm papel em `Icones` e nenhum outro uso (símbolo, único, vazio).
- **Achado da bancada:** o cenário `capela` não aplica `VESTIR`; as fotos deste par usam o `tutorial`.
- **Aguardando avaliação.** Nada integrado; o martelo e o próximo par não começaram.

### 19/10/2026 (data do computador local) — O Chapéu Pontudo no jogo (1.141.0)

- **Pedido de Jean:** integrar o Chapéu Pontudo do `b361a47` sem retoque; a Sandália volta para uma rodada 2 (a
  rodada 1, de perfil, foi recusada).
- **A integração:**
  - as fontes em camadas foram para `ferramentas/arte/aseprite/chapeu/` (32, 40, 48: aba, copa, dobras, fita,
    contorno); `DERIVADOS` do exportador com o 64 = 32 ×2;
  - os 8 arquivos do jogo (32, 40, 48, 64 e os @2x) são idênticos, byte a byte, aos aprovados, e
    `exportar_aseprite.py chapeu --conferir` os reproduz;
  - o papel `chapeu` em `ITEM` e `TAMANHOS` de `icones.js` (a base Chapéu Pontudo); o espaço vazio da cabeça continua
    com o elmo de ferro;
  - conferido a 1920×945 com os arquivos do jogo (`sandalia_chapeu/capturas/integracao/`, `fotografar.mjs
    chapeu_no_jogo` com `SO_ATUAL=1`): a ficha e o Inventário diferem das fotos aprovadas só no espaço da sandália
    (que continua com o sprite), e o saque é igual ao aprovado (a não ser 2 pixels do brilho animado). Regras, medidas,
    preços e funcionamento não mudaram.

### 19/10/2026 (data do computador local) — A Sandália, rodada 2 (proposta)

- **Pedido de Jean:** refazer a Sandália pela referência dele (`ferramentas/arte/referencias/botas/`): o par
  sobreposto em três quartos, visto um pouco de cima. A rodada 1 (de perfil) foi recusada e está guardada em
  `ferramentas/prototipos/hud/itens-lote-noite/sandalia_chapeu/rodada1/`.
- **Feito, só no protótipo** (`sandalia_chapeu/rodada2/`, `auxiliares/sandalia_par.py`), **não aprovado**: uma
  sandália primeiro (a palmilha clara com o contorno de um pé, a sola baixa com espessura, duas tiras largas e
  inclinadas que passam por cima do espaço do pé, o tornozelo com o vão), depois o par (a de trás deslocada e um tom mais
  escura, separada pelo contorno). Couro das botas aprovadas. 32, 40, 48 da mesma construção; 64 = 32 ×2; fontes em
  camadas pelo `pintar.lua`; composto, exportação e prévia conferem; @2x exatos.
- **Fotos a 1920×945:** atual × rodada 1 × rodada 2 na ficha, no Inventário e no saque (`sandalia-r2-no-jogo.png`) e o
  conjunto do Mago (`conjunto-mago-32.png`).
- **Registrado, sem mudar regra:** a Sandália usa os materiais de tecido nos nomes ("Sandália de Lã Negra"), mas é de
  couro.
- **Aguardando avaliação.** A sandália não foi integrada; nenhum outro item começou.

### 19/10/2026 (data do computador local) — A Sandália no jogo (1.142.0)

- **Pedido de Jean:** integrar a Sandália da rodada 2 (`b9ec78a`, aprovada nos quatro tamanhos) sem retoque, mantendo
  nomes e materiais; o espaço vazio dos pés continua com as botas de ferro.
- **A integração:**
  - as fontes em camadas foram para `ferramentas/arte/aseprite/sandalia/` (32, 40, 48: tras_sola, tras_palmilha,
    tras_tiras, frente_sola, frente_palmilha, frente_tiras, contorno); `DERIVADOS` com o 64 = 32 ×2;
  - os 8 arquivos do jogo são idênticos, byte a byte, aos aprovados, e `exportar_aseprite.py sandalia --conferir` os
    reproduz;
  - o papel `sandalia` em `ITEM` e `TAMANHOS` de `icones.js`; `VAZIO` dos pés intacto (`botas-ferro`);
  - conferido a 1920×945 com os arquivos do jogo e os saves temporários (`sandalia_chapeu/auxiliares/equipar.mjs`,
    fotos em `sandalia_chapeu/capturas/integracao/`): o saque (64 e 48), "Equipar agora" (Agilidade 5 → 8, Vida 60 →
    50, Mana 40 → 49, como a comparação do cartão; a vestida vai para a mochila; a ficha em 32 e o Inventário em 40, no
    corpo e na mochila) e "Guardar na mochila" (atributos e a vestida iguais; a achada na mochila). Sem erro no console.
    A ficha e o corpo do Inventário no `tutorial` são idênticos às fotos aprovadas da rodada 2 (o resto, só o
    antialiasing do texto); o saque, menos 2 pixels do brilho animado.
  - Preços, atributos, regras, medidas, áreas de clique e animações não mudaram; o jogo não lê nada de `ferramentas/`
    (as menções no `rpg/` são comentários).
- **Pendência de nomenclatura (registrada, sem mudar regra):** os nomes da Sandália vêm dos materiais de tecido
  ("Sandália de Lã Negra"), mas o desenho é de couro (plano 23).
- **O vestuário de tecido do Mago está completo** (capuz, Chapéu Pontudo, manto, luva de seda, calça de viagem,
  sandália); faltam o Diadema e a Besta Leve como desenhos inexistentes, o remake do ferro e o 40/48 do martelo.

### 19/10/2026 (data do computador local) — A Besta Leve e o Diadema (proposta)

- **Pedido de Jean:** o par seguinte, uma peça por vez, só no protótipo, com a skill `arte-itens-fenda` e o Aseprite pelo
  MCP. Sem integrar, sem o remake do ferro e sem o martelo.
- **Os dados e os usos:** a besta só vale para a base Besta Leve. O desenho `coroa` vale para o Diadema e para o único
  Coroa dos Afogados, e o sprite `coroa` é também o símbolo da reputação, que não muda com um papel de equipamento.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/besta_diadema/`), **não aprovado**:
  - **a Besta Leve** (32, 40, 48; 64 = 32 ×2): deitada na diagonal; a coronha de madeira, o arco de aço atravessado, a
    corda em V até a noz, a empunhadura de couro, o estribo;
  - **o Diadema** (32, 40, 48; 64 = 32 ×2): o aro de latão fino em perspectiva, a ponta da frente com a gema violeta.
  - Fontes em camadas pelo `pintar.lua`; composto, exportação e prévia conferem; @2x exatos.
  - Fotos a 1920×945 (ficha, Inventário, saque; o cartão da Coroa dos Afogados também) e as fileiras em tamanho real
    com as armas do Arqueiro e as peças do Mago.
- **Proposto para a Coroa dos Afogados:** o desenho comum por ora; a arte própria do único fica registrada como
  necessidade futura (plano 23). Nenhum dado mudou.
- **Aguardando avaliação.**

### 19/10/2026 (data do computador local) — A Besta Leve no jogo (1.143.0)

- **Pedido de Jean:** integrar a Besta Leve do `63a7a85` sem retoque; o Diadema volta para uma revisão do ângulo.
- **A integração:**
  - as fontes em camadas foram para `ferramentas/arte/aseprite/besta/` (32, 40, 48: coronha, empunhadura, corda, arco,
    metal, contorno); `DERIVADOS` com o 64 = 32 ×2;
  - os 8 arquivos do jogo são idênticos, byte a byte, aos aprovados, e `exportar_aseprite.py besta --conferir` os
    reproduz;
  - o papel `besta` em `ITEM` e `TAMANHOS` de `icones.js`; a arma vazia continua com a espada de ferro (`VAZIO`);
  - conferido a 1920×945 com os arquivos do jogo e os saves temporários (`sandalia_chapeu/auxiliares/equipar.mjs`, agora
    com a classe, o desenho, o espaço e a versão por argumento; fotos em `besta_diadema/capturas/integracao/`): o saque
    (64 e 48), "Equipar agora" (Ataque 13 → 15, Vida 60 → 73, como a comparação do cartão; a vestida vai para a
    mochila; a ficha em 32 e o Inventário em 40, no corpo e na mochila) e "Guardar na mochila" (nada muda no corpo; a
    achada na mochila). Sem erro no console. A ficha e o corpo do Inventário são idênticos às fotos aprovadas; no
    saque, só os raios animados atrás do ícone mudam.
  - Preços, atributos, regras, medidas, áreas de clique e animações não mudaram.

### 19/10/2026 (data do computador local) — O Diadema, rodada 2 (proposta)

- **Pedido de Jean:** rever o ângulo do Diadema (a rodada 1 ficou achatada), mostrando mais a face da frente, sem
  engrossar a chapa nem virar coroa grande; mandou uma imagem de referência de uma coroa de frente.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/besta_diadema/`), **não aprovado**: a faixa
  de latão vista de frente (a face da frente à mostra, a de dentro escura por cima, a ponta com a gema violeta); 32,
  40, 48 da mesma construção, 64 = 32 ×2; fontes em camadas pelo `pintar.lua`; composto, exportação e prévia conferem;
  @2x exatos. A rodada 1 está guardada em `besta_diadema/diadema_r1/`.
- **Fotos a 1920×945:** atual × antes × depois na ficha, no Inventário e nos saques do Diadema e da Coroa dos Afogados
  (`diadema-r2-no-jogo.png`), a fileira do Mago e a prancha. O símbolo da reputação não mudou.
- **Aguardando avaliação.** O compartilhamento com a Coroa dos Afogados segue provisório (a arte própria do único fica
  para o futuro).

### 19/10/2026 (data do computador local) — O Diadema no jogo (1.144.0)

- **Pedido de Jean:** integrar o Diadema da rodada 2 (`731ab5c`) sem retoque, mantendo o compartilhamento provisório
  com a Coroa dos Afogados, o símbolo da reputação, a cabeça vazia, os nomes, os materiais e as regras.
- **A integração:**
  - as fontes em camadas foram para `ferramentas/arte/aseprite/diadema/` (32, 40, 48: aro, placa, gema, contorno);
    `DERIVADOS` com o 64 = 32 ×2;
  - os 8 arquivos do jogo são idênticos, byte a byte, aos aprovados, e `exportar_aseprite.py diadema --conferir` os
    reproduz;
  - o papel no mapa de equipamento: `coroa` → `diadema` em `ITEM` (e `diadema` em `TAMANHOS`), para a base Diadema e,
    por ora, o único Coroa dos Afogados; o símbolo da reputação continua com o sprite `coroa` (`S` e `MIUDO`, fora de
    `ITEM`) e a cabeça vazia com o elmo de ferro;
  - conferido a 1920×945 com os arquivos do jogo e os saves temporários (`sandalia_chapeu/auxiliares/equipar.mjs`, agora
    também com o nome do arquivo por argumento; fotos em `besta_diadema/capturas/integracao/`): o saque (64 e 48),
    "Equipar agora" (Vida 50 → 51, como a comparação do cartão; o vestido vai para a mochila; a ficha em 32 e o
    Inventário em 40) e "Guardar na mochila" (nada muda no corpo). A ficha e o corpo do Inventário no `tutorial` são
    idênticos às fotos aprovadas; a reputação na ficha é igual à de antes; nos saques do Diadema e da Coroa dos Afogados,
    só os raios animados mudam. Sem erro no console. O jogo não lê nada de `ferramentas/`.
- **O levantamento:** os 31 desenhos de equipamento existem no jogo; continuam pendentes as sete peças de ferro
  (placeholders, remake) e o 40/48 do martelo (o desenho aprovado fica). A arte própria da Coroa dos Afogados e a
  pendência de nomenclatura seguem registradas.
- **Próximo par (decisão do Jean):** a espada e a maça. Não começado.

### 19/10/2026 (data do computador local) — O remake do ferro, 1: a espada e a maça (proposta do 32)

- **Pedido de Jean:** começar o remake do ferro pela espada e pela maça, uma peça por vez, só no protótipo; o escudo e o
  machado como referências; primeiro o 32 e o 64 (= 32 ×2), os 40 e 48 depois da aprovação da forma.
- **Os usos:** a espada é também a arma vazia de todas as classes e o Atacar do Guerreiro; o ícone do atributo Ataque é
  outro arquivo e não muda. A maça é só a base Maça.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/espada_maca/`), **não aprovado**: a espada (a
  lâmina larga em dois planos, a guarda e o pomo de latão, a empunhadura de couro) e a maça (o bulbo de aço em três gomos,
  com os dentes na ponta, o cabo de freixo); 32 e 64; fontes em camadas pelo `pintar.lua`; composto, exportação e
  prévia conferem; @2x exatos.
- **Fotos a 1920×945:** atual × proposta na ficha, no Inventário, no saque e no Atacar da luta, e a fileira em tamanho
  real com o machado, o escudo e o ícone de Ataque.
- **A avaliar com atenção:** a maça pode ler como lança ou tocha no 32.
- **Aguardando avaliação.** Nada integrado; a versão não mudou; as armaduras e o 40/48 do martelo não começaram.

### 19/10/2026 (data do computador local) — A espada e a maça, rodada 2 (proposta do 32)

- **Pedidos de Jean:** a maça precisa de peso e reconhecimento (a rodada 1 ficou estreita, com uma faixa clara de
  ponta); a espada foi reavaliada e também volta (a lâmina da rodada 1 lembrava uma cunha), pelas referências que ele
  pôs em `ferramentas/arte/referencias/espada/` (a principal: `espadasample.png`, a espada de aço da direita). O
  complemento substitui a aprovação e o pedido de tamanhos da espada do `796edd2`.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/espada_maca/`), **não aprovado**: a espada com
  a lâmina regular, os gumes paralelos e a ponta formada no último quarto, a guarda curta de latão e o pomo de aço; a
  maça com o bulbo redondo e cinco aletas curtas, a luz pelo volume. 32 e 64; fontes em camadas pelo `pintar.lua`;
  composto, exportação e prévia conferem; @2x exatos. A rodada 1 guardada em `espada_maca/rodada1/`.
- **As referências versionadas**, com o papel de cada uma no `LEIA-ME.md` da pasta. A skill de espadas fica para depois.
- **Fotos a 1920×945:** atual × rodada 1 × rodada 2 na ficha, no Inventário, no saque e no Atacar; a referência × as
  rodadas em tamanho real e ampliadas; a fileira com o escudo e o machado.
- **Aguardando avaliação.** Nada integrado; a versão não mudou; nenhuma outra peça começou.

### 19/10/2026 (data do computador local) — A ponta da espada e o 40/48 da maça (proposta)

- **Decisões de Jean:** a maça da rodada 2 (`87c12eb`) aprovada (32 e 64 sem retoque); na espada, só a ponta (parecia
  uma agulha acrescentada ao corpo). Pediu também que as aletas da maça mantenham o formato em todos os tamanhos.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/espada_maca/`), **não aprovado**:
  - a ponta da espada: o gume de cima quase reto e o de baixo subindo em curva até o vértice, como na referência; os
    planos seguindo os gumes; 32 e 64 (= 32 ×2); a ponta antiga guardada em `espada_maca/rodada2_ponta_antiga/`;
  - a maça em 40 e 48, com as aletas como botões rombudos na proporção do 32 e a junção escura de 1 pixel; o 32 e o 64
    aprovados idênticos, byte a byte.
  - Fontes em camadas pelo `pintar.lua`; composto, exportação e prévia conferem; @2x exatos.
- **Fotos a 1920×945:** a ponta antes × depois (tamanho real, ampliada e no saque, no Atacar e na ficha), junto da
  referência; a maça no Inventário (40), no saque (64 e 48) e na ficha.
- **Aguardando avaliação.** Nada integrado; a versão não mudou; nenhuma outra peça começou; a skill de espadas fica para
  depois.

### 19/10/2026 (data do computador local) — A ponta da espada, terceira tentativa (proposta)

- **Pedido de Jean:** a ponta do `723cf8d` ficou rombuda (o fio claro acabava antes e deixava uma "tampa" escura).
  Uma ponta aguda pela convergência contínua dos gumes, com os planos acompanhando, como na espada de aço de
  `espadasample.png`.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/espada_maca/`), **não aprovado**: as
  últimas linhas da lâmina no 32 desenhadas pixel a pixel (o fio claro até o vértice claro, o plano escuro acabando uma
  linha antes, o gume de baixo fechando meio pixel por linha); o 64 = 32 ×2; a fonte repintada pelo `pintar.lua`. A
  tentativa anterior guardada em `espada_maca/rodada2_ponta_r2/`. O diagnóstico e a solução estão no `LEIA-ME.md` do
  lote, como histórico para a futura skill de espadas (ainda não é regra).
- **Folhas a 1920×945:** a referência × as três pontas (tamanho real, silhueta e luz ampliadas) e a rombuda × a nova
  no saque, no Atacar e na ficha. A maça não mudou.
- **Aguardando avaliação.** Nada integrado; a versão não mudou; nenhuma outra peça começou.

### 19/10/2026 (data do computador local) — A ponta da espada, quarta forma (proposta)

- **Pedido de Jean:** a ponta do `3962b93` era válida, mas deslocada para um lado, com uma mudança brusca no fim.
  Mudança de abordagem: os dois gumes convergindo de forma contínua para uma ponta alinhada com a lâmina, como na espada
  de aço de `espadasample.png`; primeiro a forma, depois a luz.
- **Medido:** o vértice da terceira estava cerca de 1 px fora do eixo no 32; o da referência, praticamente no eixo, com
  um fechamento curto e simétrico (cerca de duas vezes a meia largura).
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/espada_maca/`), **não aprovado**: a meia
  largura caindo em linha reta, igual dos dois lados, até o vértice no eixo (o fechamento longo, larguras 1, 2, 4, 4,
  5, escolhido entre as combinações sem degrau); o fio e os planos por linha; o 64 = 32 ×2. Estudo da silhueta com o
  eixo numa camada auxiliar no Aseprite. A terceira tentativa guardada em `espada_maca/rodada2_ponta_r3/`.
- **Prancha:** a referência × a anterior × a nova (tamanho real, silhueta com o eixo e acabamento). A maça não mudou.
- **Aguardando avaliação.** Nada integrado; a versão não mudou; a skill de espadas fica para depois.

### 19/10/2026 (data do computador local) — A espada em 40 e 48 (proposta)

- **Decisão de Jean:** a espada do `0fcfe18` aprovada (32 e 64 sem retoque); completar o 40 e o 48 com o fechamento
  aprovado da ponta, adaptado a cada grade.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/espada_maca/`): a mesma construção, com o
  vértice ajustado por grade (para terminar num pixel sobre o eixo, sem degrau) e a luz da lâmina pela proporção do
  corte do 32 nos maiores; fontes pelo `pintar.lua`; composto, exportação e prévia conferem; @2x exatos. O 32, o 64 e a
  maça intocados.
- **Folhas a 1920×945:** os quatro tamanhos e a ponta de cada grade; atual × a espada no Inventário (40), no saque (64 e
  48) e na ficha.
- **Aguardando a avaliação final dos tamanhos** da espada e da maça antes de entrar no jogo. A versão não mudou.

### 19/10/2026 (data do computador local) — A skill das espadas (`arte-espadas-fenda`)

- **Pedido de Jean:** registrar o aprendizado da espada numa skill própria, na organização das de livros e anéis,
  complementar à `arte-itens-fenda` (que agora indica consultá-la quando o objeto for uma espada).
- **Feito:** `.claude/skills/arte-espadas-fenda/SKILL.md` (as referências de `ferramentas/arte/referencias/espada/` e a
  hierarquia, sem duplicar os PNGs; a silhueta e as proporções antes do acabamento; a continuidade dos gumes e a
  formação da ponta; a comparação com a referência pela silhueta e pelo eixo; os planos do aço; básicas e avançadas,
  com os efeitos como possibilidade futura; o Aseprite, a exportação e a avaliação em tamanho real) e `exemplos.md` (a
  espada aprovada e as recusadas: a cunha, a agulha, a rombuda e o fechamento deslocado, com os defeitos). Os
  princípios ficam separados das escolhas deste exemplo (a diagonal, o latão, a paleta, a largura, a ponta centrada, as
  contagens de pixels), e a skill registra que instruções prescritivas demais contribuíram para os desvios.

### 19/10/2026 (data do computador local) — A espada e a maça no jogo (1.145.0)

- **Pedido de Jean:** integrar a espada (32 e 64 do `0fcfe18`, 40 e 48 do `441787e`) e a maça (a rodada 2, com o 40 e
  o 48 do `723cf8d`) sem retoque.
- **A integração:**
  - os PNGs e as fontes do protótipo conferidos contra os commits aprovados; as fontes em camadas foram para
    `ferramentas/arte/aseprite/espada/` e `maca/`; `DERIVADOS` com o 64 = 32 ×2;
  - os 16 arquivos do jogo são idênticos, byte a byte, aos aprovados; `exportar_aseprite.py espada|maca --conferir` os
    reproduz;
  - os papéis já existiam: a espada vale para a Espada, o Montante, a silhueta da arma vazia (`VAZIO`) e o Atacar do
    Guerreiro (`ACAO`); a maça, para a Maça. O ícone do atributo Ataque (`attr-ataque`) não mudou;
  - o `familia_ferro.py` reconhece as duas pelas fontes no Aseprite e não as grava; a conferência dele continua "tudo
    igual" para o elmo, a cota, a manopla, as perneiras, as botas de ferro e o baú;
  - conferido a 1920×945 com os arquivos do jogo e os saves temporários: a ficha (32), o Inventário (40), a arma tirada
    (dois cliques no espaço, a silhueta apagada da espada na ficha e no Inventário), o Atacar da luta (32), o saque (64
    e 48), "Equipar agora" (a espada +2 de Ataque; a maça +1 de Ataque e +9 de Vigor, como a comparação do cartão) e
    "Guardar na mochila" (nada muda no corpo). Sem erro no console. O jogo não lê nada de `ferramentas/`.
  - Regras, nomes, atributos, medidas, áreas de clique e animações não mudaram.
- **O levantamento:** a espada e a maça passaram a arte final; continuam pendentes os remakes do elmo, da cota, da
  manopla, das perneiras e das botas de ferro, e o 40/48 do martelo.
- **Próximo par (decisão do Jean):** o elmo e a cota. Não começado.


### 19/10/2026 — Sequência do plano 23 atualizada por Jean: flechas/estados, criaturas e navegação

- Pedido explícito nesta conversa: depois de terminar os itens, priorizar o ícone da contagem de flechas do Arqueiro,
  os buffs/estados (especialmente Firme); depois ícones/retratos de inimigos e pets, caminhos e símbolos internos do
  minimapa/mapa. Criaturas/navegação já existiam no escopo, agora ordenados na nova **etapa 1E**, item 1.12.
- Confirmado na leitura: a carta usa `S("flecha", 1)`, separadamente da aljava aprovada; Firme usa `cadeado` no
  catálogo para proteção temporária após perder turno. Nenhum novo desenho nem mudança de regra foi aprovado aqui.
- Acrescentado o menu de carregar e as fichas dos saves à etapa 2. O Grimório da interface, a revisão visual da
  árvore e os ícones de habilidades/talentos ficam juntos dos respectivos sistemas na etapa 8.
- Atualizados o estado e a sequência do plano 23 e o resumo de `docs/ROADMAP.md`, preservando o histórico e o restante
  das etapas. A avaliação de refatoração/manutenção continua para depois do plano, por diagnóstico.
- Durante esta atualização, a outra sessão publicou **1.145.0**, espada e maça integradas em `ed967d1`. Reli os
  documentos novos e preservei essa integração, sua contagem de 25 artes finais, as fontes e os registros. Elmo/cota
  é o próximo par solicitado; não foi executado por esta atualização.
- **Outra sessão em andamento:** sincronizar este commit de documentação antes do próximo push, preservando as
  alterações locais. Esta atualização já vem depois da integração de espada/maça; não exige reaplicá-la.
- Somente três arquivos Markdown mudaram; nenhum código, sprite, teste, regra, versão ou save foi alterado.

### 19/10/2026 (data do computador local) — Sincronização e o remake do ferro, 2: o elmo e a cota (proposta do 32)

- **Sincronização:** o commit de documentação do Jean (`1882da5`, a ordem do plano 23 depois dos itens) trazido por
  avanço direto, antes do próximo push; a árvore local estava limpa, nada se perdeu, e a integração da espada e da maça
  (`ed967d1`) segue intacta.
- **Pedido de Jean:** o próximo par, o elmo e a cota, uma peça por vez, só no protótipo; o 32 e o 64 primeiro.
- **Os usos:** o elmo vale para o Elmo, o Capacete e a Barbuta, a cabeça vazia e o desenho de reserva da cabeça; a cota,
  para a Cota de Malha, o Peitoral, a Couraça e a Brigantina, o peito vazio e o desenho de reserva do peito.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/elmo_cota/`), **não aprovado**: o elmo (uma
  barbuta de ferro com a calota em volume, a crista, a faixa de latão com rebites e a abertura em T, o interior vazio) e
  a cota (a camisa de malha em anéis numa grade deslocada sobre o volume, a gola, os punhos e a barra de couro, o cinto
  com fivela de ferro). 32 e 64 (= 32 ×2); fontes em camadas pelo `pintar.lua`; composto, exportação e prévia
  conferem; @2x exatos.
- **Limitação registrada:** uma cota de malha só para as quatro bases do peito (malha, peitoral, couraça, brigantina);
  variantes ficam para o Jean decidir.
- **Fotos a 1920×945:** atual × proposta na ficha, no Inventário e nos saques; a fileira com o escudo e as armas.
- **Aguardando avaliação.** Nada integrado; a versão não mudou; manopla, perneiras, botas e o 40/48 do martelo não
  começaram.

### 19/10/2026 (data do computador local) — O capacete e o peito, rodada 2, pelas referências (proposta do 32)

- **Pedido de Jean:** rever o elmo e o peito pelas referências de `ferramentas/arte/referencias/capacete/` e
  `peitoral/` (o elmo da rodada 1 não foi aprovado: o bloco embaixo, o T na superfície, a faixa rígida). Escolher uma
  principal por peça, sem misturar perspectivas.
- **As escolhas:** o capacete aberto de frente, um pouco virado (o 62.º da prancha `5+N9Nb.png`); a camisa de malha de
  aço (o 103.º da `etbij8.png`). Os papéis de todas as imagens no `LEIA-ME.md` de cada pasta (versionadas agora, sem
  autoria inventada). A pasta `calça` não entrou nesta entrega.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/elmo_cota/`), **não aprovado**: o capacete
  recomeçado pela referência (a calota com a tira, a faixa em curva, o nariz, as faces longas, o fundo escuro com o vazio
  abaixo, o ângulo de três quartos) e a cota ajustada (a gola na malha, as mangas e a barra em dentes, o volume nos
  lados). 32 e 64 (= 32 ×2); fontes pelo `pintar.lua`; composto, exportação e prévia conferem; @2x exatos. A rodada 1
  guardada em `elmo_cota/rodada1/`.
- **A cota compartilhada** representa melhor a Cota de Malha, razoavelmente a Brigantina, pior o Peitoral e a Couraça.
- **Folhas:** a referência × a rodada 1 × a nova (tamanho real e ampliadas, com o escudo e as armas) e uma captura de
  cada no jogo a 1920×945.
- **Aguardando avaliação.** Nada integrado; a versão não mudou; nenhuma outra peça começou.

### 19/10/2026 (data do computador local) — O elmo, rodada 3, e a cota em 40 e 48 (proposta)

- **Decisões de Jean:** a cota do `119f479` aprovada (32 e 64 sem retoque); completar o 40 e o 48. O elmo volta para
  uma rodada 3 pela mesma referência (a faixa quase horizontal, as laterais como barras, a "travessa" na abertura).
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/elmo_cota/`), **não aprovado**: o elmo com as
  formas nas coordenadas da referência medida (a faixa inclinada e em curva, as faces inclinadas e de comprimentos
  diferentes, o nariz longo, a sombra curta do lado de dentro e o vazio abaixo), levadas ao 32 na mesma proporção; a
  cota em 40 e 48 com a malha na grade de pixels de cada tamanho. Fontes pelo `pintar.lua`; composto, exportação e
  prévia conferem; @2x exatos. O elmo da rodada 2 guardado em `elmo_cota/elmo_r2/`.
- **Folhas:** o elmo, a referência × a rodada 2 × a nova (tamanho real, silhueta e acabamento ampliados); a cota no
  Inventário (40) e no "você usa" do saque (48) a 1920×945.
- **Aguardando avaliação.** Nada integrado; a versão não mudou; nenhuma outra peça começou.

### 19/10/2026 (data do computador local) — O elmo, rodada 4, em pé e de frente (proposta)

- **Pedido de Jean:** nova referência principal do elmo (`ferramentas/arte/referencias/capacete/elmo-frente-jean.webp`,
  a coluna da direita): em pé e de frente, eixo vertical, nariz centralizado, laterais equilibradas; no meio da rodada,
  o pé das faces virando para dentro, fechando sobre o rosto.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/elmo_cota/`), **não aprovado**: o elmo
  redesenhado na grade de 32 (a calota arredondada, a faixa com espessura, a abertura vazia, as faces separadas com o pé
  para dentro), 32 e 64 (= 32 ×2); fonte pelo `pintar.lua`; composto, exportação e prévia conferem; @2x exatos. A
  rodada 3 guardada em `elmo_cota/elmo_r3/`. A cota aprovada e os tamanhos dela intocados.
- **Folha:** a referência × a rodada 3 × a nova, em tamanho real e ampliadas sem suavização.
- **Aguardando avaliação.** Nada integrado; a versão não mudou; nenhuma outra peça começou.

### 19/10/2026 (data do computador local) — 1.146.0: a cota do Guerreiro no jogo

- **Decisões de Jean:** o elmo da rodada 4 (`b4e920d`) aprovado em 32 e 64; a cota aprovada nos quatro tamanhos.
  Três entregas, uma por vez: integrar a cota; completar o 40 e o 48 do elmo (protótipo); propor a manopla e as
  perneiras (32 e 64).
- **Entrou no jogo:** a cota (o 32 e o 64 do `119f479`, o 40 e o 48 do `998373c`), sem retoque, para as quatro bases do
  peito do Guerreiro e a silhueta do peito vazio; fontes em `ferramentas/arte/aseprite/cota/`. Conferida no saque, na
  ficha, no Inventário e no peito vazio a 1920×945.
- **Continua antigo:** elmo, manopla, perneiras e botas de ferro (placeholders), o 40 e o 48 do martelo.
- **Verificações:** unittest (627, OK), gabarito OK, pyflakes (só o aviso conhecido), fumaça (tudo certo).

### 19/10/2026 (data do computador local) — O elmo em 40 e 48 (proposta)

- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/elmo_cota/`), **não aprovado**: o 40 e o 48
  do elmo aprovado (o 32 e o 64 do `b4e920d` intocados), com a mesma construção (a beira de fora com 1 px, a cintura e o
  pé para dentro nos dois lados, a silhueta simétrica). Fontes pelo `pintar.lua`; composto, exportação e prévia
  conferem; @2x exatos. Fotos no Inventário (40) e no "você usa" do saque (48) a 1920×945.
- **Aguardando avaliação.** O elmo não foi integrado; a versão continua 1.146.0.

### 19/10/2026 (data do computador local) — A manopla e as perneiras (proposta do 32)

- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/`), **não aprovado**: a
  manopla de placas (uma só, pelas costas da mão: dedos articulados, polegar, placa dos nós, punho em lâminas) pela
  referência de `referencias/Luvas/`; as perneiras como placas de ferro (rodada 2: a placa do meio, coxote com a ponta do
  quadril, joelheira, greva; o arco), pela imagem que o Jean mandou depois de recusar a 1.ª passada ("muito calça").
  32 e 64 (= 32 ×2); fontes pelo `pintar.lua`; composto, exportação e prévia conferem; @2x exatos.
- **Referências versionadas:** `referencias/Luvas/` e `referencias/calça/` (esta marcada como inadequada para armadura
  de ferro, por decisão do Jean).
- **Folhas:** a família em tamanho real e a ficha e o saque a 1920×945.
- **Aguardando avaliação.** Nada integrado; a versão continua 1.146.0. Botas, martelo e variantes não começaram.

### 19/10/2026 (data do computador local) — A manopla e as perneiras, refeitas (proposta do 32)

- **Decisão de Jean:** as propostas do `c5fd33b` recusadas (a manopla com dedos de hastes retas; as perneiras como
  pernas robóticas). Referências novas: `referencias/Luvas/2.webp` (principal da manopla) e `Luvas/1.gif` (Raven
  Fantasy, secundária); o conjunto prateado da 3.ª linha, última coluna de `referencias/calça/2.png` (principal das
  perneiras) e `calça/1.gif` (apoio). Cinto e tiras liberados; sem joelheiras como esferas.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/`), **não aprovado**: a
  manopla de perfil (dedos curvos sobrepostos, polegar articulado, placa da mão, pulso, manchete arredondada); as
  perneiras como uma peça (cinto, placa do meio, pernas contínuas com o contorno em degraus, joelheira larga com asa).
  32 e 64 (= 32 ×2); fontes pelo `pintar.lua`; composto, exportação e prévia conferem; @2x exatos. As recusadas em
  `recusadas_c5fd33b/`.
- **Folha:** `manopla_perneiras-r3.png` (tamanho real com a família, ampliadas, a ficha a 1920×945).
- **Aguardando avaliação.** Nada integrado; a versão continua 1.146.0; a cota e o elmo intocados. Botas, martelo e
  variantes não começaram.

### 19/10/2026 (data do computador local) — A manopla e as perneiras, rodada 4 (proposta do 32)

- **Pedido de Jean:** perneiras de armadura pesada (placas com faces e arestas, joelheira com aresta, não inchaço) e a
  manopla reconstruída pela mão (sem dedos de garra, a manchete equilibrada), pelas imagens que ele mandou
  (`referencias/calça/perneiras-jean.webp`, `referencias/Luvas/manopla-jean.webp`).
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/`), **não aprovado**: as
  perneiras em planos (faixas de reflexo, lâminas com sombra e espessura, joelheira em losango com asas desenhada à mão
  no 32); a manopla com três dedos de 3 px levemente dobrados, o polegar, a placa em pentágono, os anéis do pulso e a
  manchete menor. 32 e 64 (= 32 ×2); fontes pelo `pintar.lua`; composto, exportação e prévia conferem; @2x exatos. A
  rodada anterior em `rodada3_89be986/`.
- **Folha:** `manopla_perneiras-r4.png` (antes × depois com a família, ampliadas com a referência, a ficha).
- **Aguardando avaliação.** Nada integrado; a versão continua 1.146.0; a cota e o elmo intocados.

### 20/10/2026 (data do computador local) — A manopla e as perneiras, rodada 5: recomeço à mão (proposta do 32)

- **Decisão de Jean:** a rodada 4 (`9509530`) recusada nas duas; recomeçar do zero, desenhando no Aseprite desde a
  silhueta (sem gerar por fórmula). Perneiras pela armadura escura (`referencias/calça/perneiras-escuras.png`; a do
  tabardo, secundária), joelhos integrados ao perfil; manopla pela manopla lisa da prancha Raven (`Luvas/1.gif`, 2.ª
  linha, 4.ª coluna), a `2.webp` de apoio.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/`), **não aprovado**: as
  duas desenhadas pixel a pixel em grades à mão, aplicadas pelo `auxiliares/grade.lua` (o `pintar.lua`), etapa por etapa
  (silhueta, volumes). 32 e 64 (= 32 ×2); composto, exportação e @2x conferem. A rodada 4 em `rodada4_9509530/`.
- **Folha:** `manopla_perneiras-r5.png`.
- **Aguardando avaliação.** Nada integrado; a versão continua 1.146.0; a cota e o elmo intocados.

### 20/10/2026 (data do computador local) — O lote de exploração: cinco luvas e cinco pernas (só o 32)

- **Pedido de Jean:** nenhuma versão anterior da manopla e das perneiras aprovada; um lote de exploração com cinco
  luvas (L1 malha pela luva de malha nova, L2 placas pela Raven, L3 livre malha, L4 livre placas, L5 livre mista) e cinco
  pernas (P1 malha pela calça de malha nova, P2 placas por uma referência existente, P3 livre malha, P4 livre mista, P5
  livre placas), construções independentes, cinco dedos reconhecíveis, sem placa central até o tornozelo, sem joelhos
  inchados; vazias, sem botas. No meio: guias de mãos e luvas, o estudo da mão numa camada auxiliar antes do material,
  a recusa da mão em pá com dedos em franja, a pesquisa de referências (as luvas da Dungeon Crawl apontadas pelo Jean).
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/lote_exploracao/`), **não
  aprovado**: os dez candidatos em grades à mão aplicadas pelo `grade.lua` no Aseprite, em camadas (as luvas com o
  estudo da mão, oculto); 32 e @2x; composto = exportação. Pranchas `lote-luvas.png`, `lote-pernas.png`,
  `lote-favoritos-ficha.png` (favoritos: L3 e L2; P1 e P4; minha avaliação). Referências novas versionadas com papel.
- **Aguardando avaliação.** Nada integrado; a versão continua 1.146.0; a cota e o elmo intocados; botas, martelo e
  outros itens não começaram.
- **Depois do lote (20/10/2026):** o L6, a forma de mão de uma imagem que o Jean mostrou (só a forma da mão enluvada de
  pé, os quatro dedos curtos juntos em arco e o polegar no canto; sem detalhes nem cores dela), no lote, não aprovado.

### 20/10/2026 (data do computador local) — As luvas por adaptação de arte externa CC0 (proposta do 32)

- **Decisão de Jean:** mudar o método das luvas (nenhuma das do lote aprovada; P1 e P4 ficam como candidatas das
  pernas, sem mexer). Adaptar sprites existentes do pacote CC0 Idylwild's Armory sobre cópias: primeiro a paleta, depois
  o acabamento, sem redesenhar.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/adaptacao_idylwild/`),
  **não aprovado**: o pacote baixado e registrado (Idylwild, CC0 1.0, `ferramentas/arte/externas/idylwilds_armory/`);
  I1 (de `cloth_gloves`) e I2 (de `gauntlets`), cada uma com as camadas original (oculta), paleta e acabamento; 32 e @2x;
  composto = exportação. Prancha `adaptacao-idylwild.png`.
- **Aguardando avaliação.** Nada integrado; a versão continua 1.146.0.

### 20/10/2026 (data do computador local) — A escolha da base visual das luvas (sprites CC0 prontos)

- **Decisão de Jean:** I1 e I2 não aprovadas (histórico); escolher a base visual entre luvas prontas, sem modificar.
- **Feito:** a coleção CC0 Hand Wear Icons baixada e guardada com a origem (`ferramentas/arte/externas/cc0_hand_wear_icons/`);
  seis candidatas (B1 `leather_gloves` do Idylwild; B2 `glove_01`, B3 `gauntlet_01`, B4 `glove_03`, B5 `glove_04` e
  B6 `glove_05` da Dungeon Crawl; as três últimas apontadas pelo Jean) na prancha `manopla_perneiras/escolha_base/escolha-base-luvas.png`, com autor,
  origem, licença e resolução; nada desenhado nem adaptado. P1 e P4 intocadas.
- **Aguardando a escolha do Jean.** Nada integrado; a versão continua 1.146.0.

### 20/10/2026 (data do computador local) — As luvas em malha de ferro a partir de B4 e B5 (proposta do 32)

- **Decisão de Jean:** as bases B4 e B5 (`glove_03` e `glove_04` da Dungeon Crawl, CC0) escolhidas pela forma; trocar o
  material para malha de ferro, preservando a construção.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/malha_dcss/`), **não
  aprovado**: M4 e M5, sobre cópias (`auxiliares/malha_dcss.lua`: o tom pelo volume do original, a malha da cota na mão e
  no punho, os dedos lisos, o ouro e os rebites trocados pela malha, uma tira de couro na divisa do pulso); a silhueta
  idêntica à original; 32 e @2x; composto = exportação. Prancha `malha-dcss.png`. P1 e P4 intocadas.
- **Aguardando avaliação.** Nada integrado; a versão continua 1.146.0.

### 20/10/2026 (data do computador local) — A M5 aprovada em 32; o 40, o 48 e o 64 (proposta)

- **Decisão de Jean:** a M5 (a luva de malha adaptada da `glove_04` da Dungeon Crawl, CC0) aprovada em 32, `53d28893`.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/malha_dcss/`): o 40 e o 48
  pela mesma troca de material, na grade de cada tamanho; o 64 = 32 ×2; o 32 intocado. Conferidos no Inventário e no saque
  a 1920×945 (`m5-tamanhos.png`, `m5-tamanhos-no-jogo.png`). Aguardando avaliação; nada integrado; P1 e P4 intocadas.

### 20/10/2026 (data do computador local) — A skill das luvas (`arte-luvas-fenda`)

- **Pedido de Jean:** registrar o aprendizado das luvas numa skill própria, na organização das de livros, anéis e
  espadas, complementar à `arte-itens-fenda` (que agora indica consultá-la quando o objeto for uma luva ou uma manopla).
- **Feito:** `.claude/skills/arte-luvas-fenda/SKILL.md` (a base canônica: a mão da M5 aprovada, adaptada da `glove_04`
  da Dungeon Crawl Stone Soup, com os caminhos das fontes, a origem, a autoria e a licença CC0; a regra de partir dela,
  preservando a pose, a construção da mão, os dedos, o polegar e as proporções, sem redesenhar a anatomia; o acabamento
  separado: os materiais, os metais e ornamentos, os níveis simples, real e de fim de jogo, os efeitos como possibilidade
  futura; o fluxo em camadas no Aseprite, a exportação e a avaliação em tamanho real) e `exemplos.md` (a M5 e as
  recusadas: os dedos em hastes e em ganchos, o pente, os dedos fundidos, a mão em pá, a luva leve demais e o punho
  dominando; e a lição de que adaptar uma base pronta funcionou melhor que reconstruí-la). A malha, a paleta e a tira da
  M5 ficam como escolhas do exemplar. Nada no jogo; P1 e P4 intocadas.

### 20/10/2026 (data do computador local) — A manopla no jogo (1.147.0)

- **Decisão de Jean:** os tamanhos da M5 aprovados (`2d18ce15`); integrar sem retoque, com o 32 do `53d28893`.
- **Feito:** as fontes em `ferramentas/arte/aseprite/manopla/`, `DERIVADOS` com o 64 = 32 ×2; os 8 PNGs do jogo
  idênticos aos aprovados e reproduzidos pelo exportador; a origem e o crédito (Dungeon Crawl Stone Soup, CC0) nos
  `LEIA-ME.md` das externas e das fontes; a skill `arte-luvas-fenda` aponta para as fontes finais. Conferido a 1920×945
  (saque, equipar e guardar, ficha, Inventário, mãos vazias). O Grito de Guerra continua com o sprite do jogo.
- **Continua:** o elmo (40 e 48 em proposta), as perneiras (P1 e P4 em avaliação), as botas de ferro e o 40/48 do
  martelo. Equipamento: 27 de 31 finais.

### 20/10/2026 (data do computador local) — A P4 aprovada em 32; o 40, o 48 e o 64 (proposta); o elmo reapresentado

- **Decisão de Jean:** as perneiras serão a P4 do lote `90c69a89` (a malha com as placas nas coxas), aprovada em 32; a
  P1 fica guardada como alternativa não escolhida.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/p4_tamanhos/`): o 40 e o
  48 em grades à mão com a mesma construção, aplicadas no Aseprite pelo `grade.lua` (agora com o tamanho da grade); o 64
  = 32 ×2; o 32 intocado. Conferidos na ficha, no Inventário e no saque a 1920×945, com a cota e a manopla do jogo
  (`p4-tamanhos.png`, `p4-tamanhos-no-jogo.png`). O elmo reapresentado com a comparação do `3f9292a`, sem refazer.
- **Aguardando avaliação** dos tamanhos da P4 e do elmo. Nada integrado; a versão continua 1.147.0.

### 20/10/2026 (data do computador local) — O elmo e as perneiras no jogo (1.148.0)

- **Decisão de Jean:** os tamanhos da P4 e do elmo aprovados; integrar os dois sem retoque.
- **Feito:** as fontes em `ferramentas/arte/aseprite/elmo/` e `perneiras/`, `DERIVADOS` com o 64 = 32 ×2; os 16 PNGs do
  jogo idênticos aos aprovados e reproduzidos pelo exportador; o `familia_ferro.py` produz agora só as botas de ferro e o
  baú. Conferido a 1920×945 (saque, equipar e guardar, ficha, Inventário, cabeça e pernas vazias).
- **Continua:** as botas de ferro (o último placeholder do equipamento) e o 40/48 do martelo, na próxima entrega.
  Equipamento: 29 de 31 finais.

### 20/10/2026 (data do computador local) — As botas de ferro, a B1 (proposta do 32)

- **Pedido de Jean:** o último placeholder do equipamento; a bota de couro aprovada como apoio de construção, o conjunto
  de ferro como material; o 32 e o 64 = 32 ×2.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/botas_ferro/`): a B1, uma grade à mão aplicada
  no Aseprite em camadas (couro, bota de trás, bota da frente, contorno); composto = exportação = prévia; a prancha
  `botas-ferro.png` e a ficha `botas-ferro-ficha.png` (1920×945). Aguardando avaliação; nada integrado.

### 20/10/2026 (data do computador local) — O martelo em 40 e 48 (proposta)

- **Pedido de Jean:** completar o 40 e o 48 do martelo aprovado, sem mexer no 32 e no 64 do jogo.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/martelo/`): as medidas do 32 nas diagonais
  (`auxiliares/medidas.py`, que refaz o 32 aprovado) dão o rascunho; as grades do 40 e do 48 ajustadas à mão (o cabo do
  40, a empunhadura, o pomo); fontes em camadas no Aseprite; composto = exportação; @2x exatos. Conferidos no Inventário
  (40) e no saque (48, com o 64 do jogo) a 1920×945 (`martelo-tamanhos.png`, `martelo-tamanhos-no-jogo.png`).
- **Aguardando avaliação** do martelo e das botas de ferro (B1, `725b2695`). Nada integrado; a versão continua 1.148.0.
