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

O README principal descreve o jogo disponível (desde a 1.206.0, só a campanha; o mundo procedural saiu: [24](24-RETIRADA-DO-PROCEDURAL.md)). O roadmap descreve a direção futura; não interpretar essa diferença como autorização para trocar imediatamente o comportamento.

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

### 20/10/2026 (data do computador local) — O martelo em 40 e 48 no jogo (1.149.0)

- **Decisão de Jean:** o 40 e o 48 do martelo aprovados (`244cdbd4`); integrar sem retoque, preservando o 32 e o 64.
- **Feito:** as fontes em `ferramentas/arte/aseprite/martelo/`; os 4 PNGs idênticos aos aprovados e reproduzidos pelo
  exportador; `icones.js` usa o arquivo nos lados que ele tem (o 40 no Inventário, o 48 no "você usa"), e o desenho em
  código no 32 e no 64. Conferido a 1920×945 (saque, equipar e guardar, ficha, Inventário). Os outros papéis do martelo
  (Golpe Pesado, Gigante, ferreiro) continuam com o sprite do jogo.
- **Continua:** as botas de ferro (a B1, `725b2695`, em avaliação). Equipamento: 30 de 31 finais.

### 20/10/2026 (data do computador local) — As botas de ferro, a B2 (proposta do 32)

- **Decisão de Jean:** a B1 (`725b2695`) não escolhida; refazer pela referência nova (o par em pixel art à direita da
  imagem que ele mandou): armadura pesada, peças rígidas articuladas, as duas botas distintas pela posição e pelo ângulo.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/botas_ferro/`): a B2, uma grade à mão aplicada
  no Aseprite em camadas; composto = exportação = prévia; 32 e 64 = 32 ×2; a prancha `botas-ferro-b2.png` e a ficha
  `botas-ferro-b2-ficha.png` (1920×945). A B1 preservada como tentativa não escolhida.
- **Pendente:** salvar a imagem da referência em `ferramentas/arte/referencias/botas/botas-ferro-ref.png` (veio anexada
  na conversa; os papéis já estão no `LEIA-ME.md` de lá). Aguardando avaliação; nada integrado; a versão continua 1.149.0.

### 20/10/2026 (data do computador local) — As botas de ferro, a B3 (a transposição da referência gerada)

- **Pedido de Jean:** a imagem gerada que ele mandou é a referência principal e o alvo visual; transpor fielmente para
  32 (e o 64 = 32 ×2), sem reinterpretar, na paleta do conjunto.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/botas_ferro/b3/`): a referência salva em
  `ferramentas/arte/referencias/botas/` (o original, com o `LEIA-ME.md`); a redução proporcional como guia, o rascunho
  na paleta e os ajustes à mão (`auxiliares/`); a fonte em camadas no Aseprite (a guia oculta, interior, couro, aço,
  contorno); composto = exportação = grade; a prancha `botas-ferro-b3.png` e a ficha `botas-ferro-b3-ficha.png`.
  B1 e B2 preservadas como tentativas.
- **Aguardando avaliação.** Nada integrado; a versão continua 1.149.0.

### 20/10/2026 (data do computador local) — A B3 das botas aprovada em 32; o 40, o 48 e o 64 (proposta)

- **Decisão de Jean:** a B3 (`5a4f75bd`) aprovada em 32; o 32 e o 64 sem retoques; completar o 40 e o 48.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/botas_ferro/b3/`): o 40 e o 48 pelo mesmo
  caminho do 32 (a guia da referência, o rascunho na paleta, o contorno por dentro e os ajustes à mão de cada grade);
  fontes em camadas; composto = exportação = grade; @2x exatos; o 32 e o 64 idênticos ao aprovado. Conferidos no
  Inventário e no saque a 1920×945 (`b3-tamanhos.png`, `b3-tamanhos-no-jogo.png`).
- **Aguardando avaliação.** Nada integrado; a versão continua 1.149.0.

### 20/10/2026 (data do computador local) — As luvas, a L7 (proposta do 32)

- **Pedido de Jean:** uma nova proposta de luvas pelo processo das botas B3, a partir do recorte de um par que ele
  escolheu (a forma) e de uma imagem gerada (os volumes); sem a mão da M5 como molde.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/luvas_l7/`): as referências em
  `ferramentas/arte/referencias/Luvas/` (o recorte tem marca d'água: a licença a esclarecer antes de integrar); a grade
  nativa do recorte na escala 1:1 como guia, a paleta do conjunto e os ajustes; a fonte em camadas; composto = exportação
  = grade; a prancha `luvas-l7.png` e a ficha `luvas-l7-ficha.png`. A skill `arte-luvas-fenda` atualizada: os dois
  caminhos (transpor uma referência escolhida, adaptar uma base pronta), a anatomia da M5 deixa de ser obrigatória, a M5
  documentada como histórico e como a luva do jogo, a L7 como a direção escolhida e ainda em avaliação.
- **Aguardando avaliação.** A M5 continua no jogo; nada integrado.

### 20/10/2026 (data do computador local) — As botas de ferro no jogo (1.150.0): os 31 equipamentos-base concluídos

- **Decisão de Jean:** a B3 aprovada nos quatro tamanhos (32 e 64 do `5a4f75bd`, 40 e 48 do `61545bd7`); integrar sem
  retoque.
- **Feito:** as fontes em `ferramentas/arte/aseprite/botas-ferro/`, `DERIVADOS` com o 64 = 32 ×2; os 8 PNGs do jogo
  idênticos aos aprovados e reproduzidos pelo exportador; o `familia_ferro.py` produz só o baú. Conferido a 1920×945
  (saque, equipar e guardar, ficha, Inventário, pés vazios). **Os 31 equipamentos-base estão concluídos.**
- **Continua:** as variantes (únicos e raros com desenho próprio) e os compartilhamentos provisórios (a Capa de Patrulha,
  o Chapéu de Couro, a Coroa dos Afogados); a L7 das luvas em avaliação (a M5 do jogo não muda). A próxima etapa do
  plano (1E) não começou.

### 20/10/2026 (data do computador local) — A L7, a limpeza localizada (proposta)

- **Decisão de Jean:** a L7 aprovada como direção; só limpar os pixels, sem mudar a silhueta, a pose, os dedos nem a
  malha, com a imagem gerada como referência de acabamento.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/luvas_l7/`): 55 pixels mudados direto na
  fonte em camadas (`auxiliares/limpeza.py`, cada um com o porquê); a versão anterior em `anterior_8a844975/`; composto =
  exportação = grade; o 64 = 32 ×2; a folha `luvas-l7-limpeza.png`. Sem 40 e 48; nada integrado; a M5 continua no jogo.
- **Pendente:** a origem e a licença do recorte (com marca d'água), antes de qualquer integração.

### 20/10/2026 (data do computador local) — A L7, o retoque localizado (proposta)

- **Pedido de Jean:** retocar a palma da esquerda, um quadradinho cinza no punho e o encontro da palma com o pulso,
  preservando a forma.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/luvas_l7/`): 21 pixels na fonte em camadas
  (`auxiliares/retoque.py`, cada um com o porquê): a dobra da base do polegar contínua, o canto da malha do punho no
  xadrez, a costura do pulso lisa; o antes em `anterior_10772117/`; composto = exportação = grade; o 64 = 32 ×2; a folha
  `luvas-l7-retoque.png`. Sem 40 e 48; nada integrado; a licença do recorte continua pendente.

- **Mais um retoque (20/10/2026):** o pixel perdido e a ponta de sombra na beira esquerda do punho da luva da esquerda
  (2 pixels, `auxiliares/retoque2.py`; o antes em `anterior_ba650ddd/`; a folha `luvas-l7-retoque-ba650ddd.png`).

- **E o pixel prata (20/10/2026):** na borda da malha da direita, junto da faixa do pulso, virou contorno preto (1 pixel;
  o antes em `anterior_9a9e2281/`; a folha `luvas-l7-retoque-9a9e2281.png`).

### 20/10/2026 (data do computador local) — A L7 aprovada no 32; o 40, o 48 e o 64 (proposta)

- **Decisão de Jean:** a L7 aprovada visualmente no 32 (`c7639438`); completar o 40 e o 48, o 32 e o 64 preservados.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/luvas_l7/`): o 40 e o 48 do 32 final como
  autoridade (`auxiliares/tamanhos.py`: o vizinho mais próximo, as linhas com 1 px na direção da espessura, a malha na
  grade de cada tamanho, 8 ajustes à mão); fontes em camadas; composto = exportação = grade; @2x exatos; o 32 e o 64
  idênticos ao aprovado. Conferidos no Inventário e no saque a 1920×945 (`l7-tamanhos.png`, `l7-tamanhos-no-jogo.png`).
- **Aguardando avaliação.** A M5 continua no jogo; a licença do recorte continua pendente; a versão continua 1.150.0.

### 20/10/2026 (data do computador local) — A L7 em 40 e 48, a revisão da forma (proposta)

- **Pedido de Jean:** o 40 e o 48 do `aeb5ad75` perderam parte da leitura da mão do 32; revisar, com o 32 e o 64
  preservados.
- **Feito, só no protótipo** (`ferramentas/prototipos/hud/itens-lote-noite/luvas_l7/`): a comparação à mesma altura
  achou a causa (as linhas de dentro forçadas a 1 px); as linhas de dentro passaram a vir do 32 pelo vizinho mais próximo,
  com ajustes à mão (7 no 40, 17 no 48); o antes em `anterior_aeb5ad75/`; composto = exportação = grade; @2x exatos; o 32
  e o 64 idênticos ao aprovado; conferido no Inventário e no saque a 1920×945; a folha `l7-revisao-40-48.png`.
- **Aguardando avaliação.** A M5 continua no jogo; a licença do recorte continua pendente.

### 20/10/2026 (data do computador local) — A L7 em 40 e 48, a réplica do 32 (proposta)

- **Pedido de Jean:** réplicas idênticas do 32 no 40 e no 48, comparadas pixel a pixel (ele circulou o dedo mínimo da
  direita e o alto dos dedos da esquerda).
- **Feito, só no protótipo:** o 40 e o 48 são o 32 pelo vizinho mais próximo, puro (cada pixel igual ao do 32 de que
  vem); as tentativas com regras em `anterior_aeb5ad75/` e `anterior_fd60dd2c/`; fontes em camadas; composto =
  exportação; @2x exatos; o 32 e o 64 do `c7639438` intactos; conferido no Inventário e no saque; a folha
  `l7-revisao-40-48-fd60dd2c.png`. A skill registra a regra de réplica.
- **Aguardando avaliação.** A M5 continua no jogo; a licença do recorte continua pendente.

- **O teste do 32 centrado (20/10/2026):** o 32 aprovado, sem redimensionar, no centro dos espaços de 40 e 48
  (`luvas_l7/alternativa_32/`), ao lado da réplica no Inventário e no saque (`l7-centrado-no-jogo.png`,
  `l7-centrado-espacos.png`). Aguardando avaliação; nada integrado.

### 20/10/2026 (data do computador local) — A L7: a proposta visual consolidada; as skills dos tamanhos

- **Decisão de Jean:** a L7 com o 32 centrado nos espaços de 40 e 48 (`fa9711bb`); encerradas as tentativas de redesenho
  desses tamanhos.
- **Feito:** a proposta da L7 consolidada (`luvas_l7/proposta/`: o 32 na ficha, o 32 centrado nos quadros de 40 e 48, o
  64 = 32 ×2; as versões redesenhadas guardadas como histórico em `anterior_aeb5ad75/`, `anterior_fd60dd2c/` e
  `anterior_9cd3f340/`). As skills `arte-itens-fenda` e `arte-luvas-fenda` com o aprendizado (o espaço não determina o
  tamanho do desenho; testar antes a arte-base nativa ou ampliada por fator inteiro; versões próprias quando melhoram, sem
  obrigação; comparar a adaptação com o original centrado; aprovar pelo tamanho real; os equipamentos já aprovados em 40
  e 48 continuam válidos); as de espadas e anéis sem a exigência do 40 e do 48 próprios.
- **Continua:** a integração da L7 espera a origem e a licença do recorte; a M5 continua no jogo; a versão continua
  1.150.0. Nenhum desenho novo começado.

### 20/10/2026 (data do computador local) — As perneiras, a P6 (proposta do 32)

- **Pedido de Jean:** uma nova proposta das perneiras pelo processo das botas B3, com a imagem gerada que ele mandou como
  referência principal (`ferramentas/arte/referencias/calça/perneiras-gerada.webp`); só o 32 e o 64 = 32 ×2.
- **Feito:** a P6 em `ferramentas/prototipos/hud/itens-lote-noite/perneiras_p6/` (a guia reduzida sem esticar, a grade
  montada à mão por parte sobre ela, a fonte `fontes/P6/P6-32.aseprite` em camadas com a guia oculta, a prancha `p6.png`
  e a ficha a 1920×945 em `p6-ficha.png`); as simplificações e as diferenças da referência no `LEIA-ME.md` do lote.
- **Continua:** a P4 no jogo; a P6 em avaliação, sem integrar; a L7 das luvas espera a origem e a licença do recorte; a
  versão continua 1.150.0.

### 20/10/2026 (data do computador local) — As luvas L7 no jogo (1.151.0)

- **Decisão de Jean:** integrar a L7 visualmente aprovada, a consolidada no `63f5c81e` (o 32 do `c7639438`; o 40 e o 48
  com o mesmo 32 centrado, do `fa9711bb`; o 64 = 32 ×2), sem retoques e sem as versões redesenhadas. **A origem e a
  licença do recorte de referência (com marca d'água) ficam para investigar depois: pendência aberta; a L7 não herda a
  licença CC0 da M5.**
- **Feito:** a fonte em camadas em `ferramentas/arte/aseprite/manopla/manopla-32.aseprite`; a M5 em
  `aseprite/historico/manopla-m5/` (fora da exportação, com o crédito CC0 preservado); o `exportar_aseprite.py` deriva o
  40 e o 48 pelo 32 centrado (`CENTRO`, 4 e 8 px) e o 64 pelo ×2, e o `--conferir` verifica o miolo e a beira
  transparente; os 8 PNGs do jogo idênticos, byte a byte, aos da proposta. Os usos não mudaram (`ITEM` e `VAZIO` das
  mãos; o Grito de Guerra continua com o sprite do jogo). Conferido no jogo a 1920×945: o saque (64, "você usa" em 48),
  equipar e guardar, a ficha (32), o Inventário (40) e as mãos vazias.
- **Continua:** as perneiras P6 em avaliação (a P4 no jogo); nenhum desenho novo começado.

### 20/10/2026 (data do computador local) — As perneiras, a P7 (alternativa do 32)

- **Pedido de Jean:** uma alternativa P7 das perneiras com a segunda imagem gerada como referência principal
  (`ferramentas/arte/referencias/calça/perneiras-gerada-2.webp`), sem partir da P6; só o 32 e o 64 = 32 ×2.
- **Feito:** a P7 em `ferramentas/prototipos/hud/itens-lote-noite/perneiras_p7/` (a guia reduzida sem esticar, a grade à
  mão na ordem silhueta, volume, textura, com as larguras do quadril, da coxa, do joelho e do tornozelo; a fonte
  `fontes/P7/P7-32.aseprite` em camadas com a guia oculta; as folhas `p7.png` e `p7-ficha.png`, P6 × P7 a 1920×945); as
  simplificações no `LEIA-ME.md` do lote.
- **Continua:** a P4 no jogo; a P6 e a P7 em avaliação; a luva L7 no jogo com a origem e a licença do recorte pendentes;
  a versão continua 1.151.0.

### 20/10/2026 (data do computador local) — A P7, as laterais suavizadas (proposta)

- **Pedido de Jean:** suavizar só as laterais da P7 do `3cb041db` (liam como placas ou apetrechos de metal separados);
  a construção, o cinto, as joelheiras e a separação das pernas preservados; só o 32, o 64 = 32 ×2.
- **Feito:** o retoque localizado (`perneiras_p7/auxiliares/retoque.py`, 66 pixels) na fonte: a beira das coxas e das
  canelas no volume da malha, as juntas escuras incorporadas, a asa acima da canela reduzida a uma linha; o antes em
  `perneiras_p7/anterior_3cb041db/`; as folhas `p7-retoque.png` e `p7-retoque-ficha.png`.
- **Continua:** a P4 no jogo; a P6 e a P7 em avaliação; a versão continua 1.151.0.

### 20/10/2026 (data do computador local) — As perneiras P7 no jogo (1.152.0)

- **Decisão de Jean:** integrar a P7 suavizada do `6dc582e3`, sem retoques; o 40 e o 48 pela solução da L7 (o 32
  centrado em quadros transparentes).
- **Feito:** a fonte em `ferramentas/arte/aseprite/perneiras/perneiras-32.aseprite`; a P4 em
  `aseprite/historico/perneiras-p4/`; o `DERIVADOS` das perneiras com o `CENTRO` (40 e 48) e o ×2 (64); o 32 e o 64
  idênticos aos aprovados, os centros do 40 e do 48 iguais ao 32. Os usos não mudaram (`ITEM`, `VAZIO`, `ICONE_ESPACO`).
  Conferido no jogo a 1920×945: o saque, equipar e guardar, a ficha, o Inventário e as pernas vazias.
- **Continua:** a luva L7 com a origem e a licença do recorte pendentes; em seguida, a proposta do capacete com malha
  (só no protótipo).

### 20/10/2026 (data do computador local) — O capacete com malha, o C1 (proposta do 32)

- **Pedido de Jean:** uma proposta separada de um capacete com malha, com a imagem gerada dele como referência principal
  (`ferramentas/arte/referencias/capacete/capacete-malha-gerada.webp`); só o 32 e o 64 = 32 ×2.
- **Feito:** o C1 em `ferramentas/prototipos/hud/itens-lote-noite/capacete_malha/` (a guia reduzida sem esticar, a grade à
  mão pela silhueta e pelas partes, a fonte `fontes/C1/C1-32.aseprite` em camadas com a guia oculta, as folhas `c1.png` e
  `c1-ficha.png`); as simplificações no `LEIA-ME.md` do lote.
- **Continua:** o elmo do jogo sem mudança; o C1 em avaliação; a versão continua 1.152.0.

### 20/10/2026 (data do computador local) — O capacete C1 no jogo (1.153.0)

- **Decisão de Jean:** integrar o C1 do `b6af648f`, sem retoques; o 40 e o 48 pela solução da L7 (o 32 centrado).
- **Feito:** a fonte em `ferramentas/arte/aseprite/elmo/elmo-32.aseprite`; o elmo de frente em
  `aseprite/historico/elmo-r4/`; o `DERIVADOS` do elmo com o `CENTRO` e o ×2; o 32 e o 64 idênticos aos aprovados, os
  centros do 40 e do 48 iguais ao 32. Os usos não mudaram (`ITEM`, `VAZIO`, `ICONE_ESPACO`). Conferido no jogo a 1920×945:
  o saque, equipar e guardar, a ficha, o Inventário e a cabeça vazia.
- **Continua:** em seguida, o teste de acabamento das botas B3 (só no protótipo).

### 20/10/2026 (data do computador local) — As botas, a A1: o acabamento contido (proposta)

- **Pedido de Jean:** testar só o acabamento da B3 (a forma aprovada), mais contido, para aproximá-la do C1, da cota e
  da P7, com a nova imagem gerada como referência de acabamento (`ferramentas/arte/referencias/botas/Botas de ferro em
  pixel art.png`); só o 32 e o 64 = 32 ×2.
- **Feito:** a A1 em `ferramentas/prototipos/hud/itens-lote-noite/botas_ferro/acabamento_a1/` (80 pixels de aço na cópia
  da fonte: sem quase brancos, os 7 só como brilhos curtos nas beiras, o corpo das placas no tom médio com a divisão dos
  planos, as juntas e as sombras das sobreposições mantidas; as folhas `a1.png` e `a1-ficha.png`).
- **Continua:** a B3 no jogo, a A1 aguardando a escolha visual; a versão continua 1.153.0.

### 20/10/2026 (data do computador local) — A A1 em 40 e 48 (proposta)

- **Decisão de Jean:** o acabamento do 32 da A1 (`945a54a8`) aprovado; o mesmo tratamento nas fontes de 40 e 48 da B3.
- **Feito:** o 40 e o 48 pelas mesmas regras (só os tons do aço; 135 e 213 pixels), as cópias das fontes pintadas, o 32
  e o 64 idênticos aos aprovados; as folhas `a1-tamanhos.png` e `a1-tamanhos-no-jogo.png` (o Inventário e o saque).
- **Continua:** a B3 no jogo; a A1 completa aguardando a avaliação; a versão continua 1.153.0.

### 20/10/2026 (data do computador local) — A flecha da carta (F1) e o Firme (R1) (proposta)

- **Pedido de Jean:** o primeiro par do desvio visual (1E): o ícone da quantidade de flechas na carta do Arqueiro e um
  símbolo próprio para o Firme, com as referências geradas em `ferramentas/arte/referencias/icones/`.
- **Feito:** o levantamento (os dois aparecem em 16 px na luta; o `flecha` e o `cadeado` têm outros papéis, que ficam;
  o Firme é o turno depois de um atordoamento ou congelamento, sem nova trava, sem bônus de Defesa); a F1 e o R1 em 16 px
  em `ferramentas/prototipos/hud/itens-lote-noite/flechas_firme/`, com as fontes em camadas e as fotos na luta a
  1920×945; o cenário `covil` dos testes de navegador aceita `EFEITOS` e `EFEITOS_INIMIGO`.
- **Continua:** nada integrado; a versão continua 1.153.0. Não começados: inimigos, pets, caminhos, talentos,
  habilidades.

### 20/10/2026 (data do computador local) — As botas A1 no jogo (1.154.0)

- **Decisão de Jean:** integrar os quatro tamanhos da A1 (32 e 64 do `945a54a8`, 40 e 48 do `3c41c7a0`), sem retoques.
- **Feito:** as fontes da A1 em `ferramentas/arte/aseprite/botas-ferro/`; a B3 em `aseprite/historico/botas-ferro-b3/`;
  os 8 PNGs do jogo idênticos aos aprovados; os usos sem mudança (`ITEM`, `VAZIO`). Conferido no jogo a 1920×945: o
  saque, equipar e guardar, a ficha, o Inventário e os pés vazios.
- **Continua:** o Firme (R1) e a flecha da carta (F1) em ajuste no protótipo.

### 20/10/2026 (data do computador local) — A flecha F2 e o Firme R2 (proposta)

- **Pedido de Jean:** o Firme sem as faíscas e com o interior dos elos mais legível; a flecha com as penas na traseira,
  menores e sem madeira atrás, pela flecha simples da prancha "Arrows" (mandada na conversa).
- **Feito:** a R2 e a F2 em `ferramentas/prototipos/hud/itens-lote-noite/flechas_firme/` (fontes em camadas, @2x), com a
  F1 e a R1 preservadas; a folha `rodada2.png` com a carta na luta a 1920×945, atual × rodada 1 × rodada 2.
- **Continua:** nada integrado da flecha nem do Firme; a versão continua 1.154.0.

### 20/10/2026 (data do computador local) — A flecha da carta (F2) e o Firme (R2) no jogo (1.155.0)

- **Decisão de Jean:** integrar a F2 e a R2 do `bc849647`, sem retoques, cada uma só no seu papel.
- **Feito:** as fontes em `ferramentas/arte/aseprite/contador-flechas/` e `estado-firme/`; os PNGs de 16 e @2x idênticos
  aos aprovados; em `icones.js`, o papel `ESTADO` (`Icones.estado`) e o `Icones.contadorFlechas`, chamados por
  `batalha.js` no chip e no selo dos estados e na `.carta-flechas`, com volta ao sprite do jogo sem desenho. O `flecha`
  e o `cadeado` ficam nos outros papéis. Conferido no jogo a 1920×945.
- **Continua:** os outros estados e o resto do bloco 1E (inimigos, pets, caminhos) não começados.

### 20/10/2026 (data do computador local) — O levantamento dos estados; Em guarda (G1) e Esquiva (E1) (proposta)

- **Pedido de Jean:** o levantamento dos estados no plano 23 e o primeiro par de ícones de estados, Em guarda e Esquiva,
  só no protótipo.
- **Feito:** a tabela dos 17 estados no plano 23 (o efeito real, o ícone, os compartilhamentos e a situação: o Firme
  final, o Em guarda e a Esquiva em proposta, os outros pendentes; todos em 16 px no chip e no selo); o G1 (o escudo de
  ferro) e o E1 (a rajada de vento) em `ferramentas/prototipos/hud/itens-lote-noite/estados_guarda_esquiva/`, com as
  fontes em camadas e a carta na luta a 1920×945.
- **Continua:** nada integrado; a versão continua 1.155.0. Não começados: os outros estados, inimigos, pets.

### 20/10/2026 (data do computador local) — O Em guarda G1 no jogo (1.156.0)

- **Decisão de Jean:** integrar o G1 do `118725b6`, sem retoques, só no estado Em guarda.
- **Feito:** a fonte em `ferramentas/arte/aseprite/estado-guarda/`; o PNG de 16 e o @2x idênticos aos aprovados; o papel
  `ESTADO.guarda` em `icones.js` (o chip e o selo); o sprite `escudo` intacto nos outros papéis. Conferido no jogo a
  1920×945.
- **Continua:** a Esquiva numa rodada 2 (só no protótipo).

### 21/10/2026 (data do computador local) — A Esquiva: as alternativas E3 e E4 (proposta)

- **Pedido de Jean:** a E2 recusada (guardada); duas alternativas de conceito em 16 px: a bota dando um passo e outra
  solução de desviar de um ataque; conferir as duas curvas que apareceram no lugar do escudo e da Esquiva.
- **Feito:** a E3 (a bota) e a E4 (a figura que sai do lugar, com o fantasma) em
  `ferramentas/prototipos/hud/itens-lote-noite/estados_guarda_esquiva/`, a E2 como histórico; a prancha nova pelo nome de
  cada ícone (as duas curvas eram de um visualizador de rascunho que montava por posição; o jogo nunca mapeou a Esquiva).
- **Continua:** a Esquiva fora de produção (a folha do jogo) até a avaliação; a versão continua 1.156.0.

### 21/10/2026 (data do computador local) — A Esquiva: a E5 recusada e a E6, a cópia da referência (proposta)

- **Pedido de Jean:** uma Esquiva com figura humana pela referência de movimento que ele mandou; a pose à mão (E5) foi
  recusada durante a rodada, com o pedido de copiar a referência "1 pra 1".
- **Feito:** a E6 (a silhueta da referência reduzida e limpa à mão, numa cor chapada com o contorno) e a E5 como
  histórico, em `ferramentas/prototipos/hud/itens-lote-noite/estados_guarda_esquiva/`; a folha `esquiva-e6.png` com a
  carta a 1920×945 (a folha, a E3, a E6). A referência em `ferramentas/arte/referencias/icones/`, com a origem e a
  licença pendentes.
- **Continua:** nenhuma Esquiva aprovada; a versão continua 1.156.0.

### 21/10/2026 (data do computador local) — A Esquiva E6 no jogo (1.157.0)

- **Decisão de Jean:** integrar a E6 corrigida do `df6a433d`, sem retoques, só no estado Esquiva.
- **Feito:** a fonte em `ferramentas/arte/aseprite/estado-esquiva/`; o PNG de 16 e o @2x idênticos aos aprovados; o papel
  `ESTADO.esquiva` em `icones.js` (o chip e o selo, nítidos); a `folha` intacta nos outros papéis. Conferido no jogo a
  1920×945: o chip e o selo de chegada (o Passo Ágil). A origem e a licença da referência continuam pendentes.
- **Continua:** os outros estados (Fortalecido, Fúria, Frenesi, Iniciativa, Barreira, Furtivo, Provocando e os
  negativos) com os sprites do jogo; não começados.

### 21/10/2026 (data do computador local) — Os estados restantes, lote 2: Chamas e Maldição (proposta)

- **Feito:** as três línguas de fogo (Chamas) e a caveira roxa de olhos acesos (Maldição) em
  `estados_restantes/` (fontes, `lote2.png` com o herói contra cultistas e os lobos em chamas a 1920×945).
- **Continua:** nada aprovado; a versão continua 1.157.0.

### 21/10/2026 (data do computador local) — Os estados restantes, lote 3: Atordoado e Enfraquecido (proposta)

- **Feito:** a espiral dourada (Atordoado, também o congelado) e a espada para baixo com a seta roxa descendo
  (Enfraquecido) em `estados_restantes/`, com as tentativas guardadas (a órbita com estrelas, a espada partida, as
  setinhas); `lote3.png` com os lobos e o herói a 1920×945.
- **Continua:** nada aprovado; a versão continua 1.157.0.

### 21/10/2026 (data do computador local) — Os estados restantes, lote 4: Marcado e Furtivo (proposta)

- **Feito:** o alvo de anéis (Marcado) e o capuz com os olhos (Furtivo) em `estados_restantes/`, a mira guardada como
  tentativa; `lote4.png` com os lobos marcados e o herói furtivo a 1920×945.
- **Continua:** nada aprovado; a versão continua 1.157.0.

### 21/10/2026 (data do computador local) — Os estados restantes, lote 5: Barreira e Provocando (proposta)

- **Feito:** a figura dentro da bolha azul (Barreira) e a figura com três setas vermelhas descendo sobre ela
  (Provocando) em `estados_restantes/`, com as tentativas guardadas (a bolha vazia, a esfera, as setas dos lados);
  `lote5.png` com o Mago e o esqueleto do Necromante a 1920×945. Os dois são os mais frágeis da noite (avaliação no
  `LEIA-ME.md` da pasta).
- **Continua:** nada aprovado; a versão continua 1.157.0.

### 21/10/2026 (data do computador local) — Os estados restantes, lote 6: Fortalecido e Iniciativa (proposta)

- **Feito:** a espada com a seta dourada subindo (Fortalecido) e a exclamação com raios (Iniciativa, sugestão do Jean),
  com a bota da Agilidade em 16 px como alternativa da Iniciativa, em `estados_restantes/`; `lote6.png` a 1920×945.
- **Continua:** nada aprovado; a versão continua 1.157.0.

### 21/10/2026 (data do computador local) — Os estados restantes, lote 7: Fúria e Frenesi (proposta)

- **Feito:** o rosto vermelho de raiva (Fúria) e as três garras crescentes (Frenesi) em `estados_restantes/`;
  `lote7.png` com o Berserker fortalecido, em fúria e em frenesi ao mesmo tempo, a 1920×945.
- **Continua:** nada aprovado; a versão continua 1.157.0. Falta a prancha geral dos 17.

### 21/10/2026 (data do computador local) — Os estados restantes: a prancha geral e a avaliação (proposta)

- **Feito:** os sete lotes entregues (commits `051a4fc1`, `6cc75359`, `560a0cd2`, `1d9e8752`, `bc4035bd`, `ca37990a`,
  `72f5360d`); a prancha `geral.png` com os 17 estados; a conferência técnica dos 26 desenhos (fonte reaberta = proposta
  = grade, @2x exato); a avaliação no `LEIA-ME.md` de `estados_restantes/`; a tabela do plano 23 marca os 14 como
  proposta.
- **Pendências:** o conector do Aseprite (MCP) não conectou nesta sessão (as fontes saíram pela linha de comando; se o
  Jean preferir, reconectar o `aseprite-bridge` antes da próxima rodada); a origem e a licença das referências antigas
  continuam como estavam; a exclusão local de `ferramentas/arte/referencias/capacete/elmo-frente-jean.webp`, feita pelo
  Jean, continua fora dos commits.
- **Próximo passo:** o Jean avaliar as folhas `lote1.png` a `lote7.png` e `geral.png`; aprovar, pedir retoque ou outra
  construção por estado. Nada integrado; a versão continua 1.157.0.

### 21/10/2026 (data do computador local) — Sangramento, Maldição, Marcado, Furtivo e Fúria no jogo (1.158.0)

- **Decisão de Jean:** integrar os cinco aprovados nas versões da prancha geral do `b17ab3dd`, sem retoques, só nos
  estados.
- **Feito:** as fontes em `ferramentas/arte/aseprite/estado-<id>/` (sangramento, maldito, marcado, furtivo, furia); os
  PNGs de 16 e o @2x pelo `exportar_aseprite.py`, idênticos byte a byte aos aprovados (`todas --conferir`: tudo igual);
  o papel `ESTADO` em `icones.js` (o chip e o selo); os sprites `gota`, `gota_roxa`, `flecha`, `olho` e `machado`
  intactos nos outros papéis. Conferido no jogo a 1920×945 com os arquivos de produção (os chips e os selos de chegada
  pela roda: Sede de Sangue, a Maldição do Necromante, Desaparecer, Fúria Cega); o Marcado não tem selo de chegada no
  jogo (o Marcar Presa e o evento da estrada aplicam direto, sem lance). Folha:
  `estados_restantes/integracao-1.158.0.png`.
- **Continua:** os outros nove estados numa segunda rodada no protótipo.

### 21/10/2026 (data do computador local) — A segunda rodada dos estados, grupo 1: Veneno, Chamas, Atordoado e Enfraquecido (proposta)

- **Pedido de Jean:** refinar os nove não aprovados só no protótipo, preservando as versões anteriores.
- **Feito:** a gota verde caindo na poça (alternativa do Veneno; a recomendação continua a serpente), a chama dominante
  (Chamas), a guarda equilibrada (Enfraquecido) e o teste opcional da rotação do selo do Atordoado (uma volta em 90°,
  respeitando o movimento reduzido; não aplicado ao jogo), em `estados_restantes/` (`rodada2-lote1.png` a
  `rodada2-lote3.png`, `rodada2-atordoado-gira.png`). O MCP do Aseprite continua fora; as fontes saíram pela linha de
  comando, com a releitura e a conferência da exportação.
- **Continua:** nada novo aprovado; a versão continua 1.158.0.

### 21/10/2026 (data do computador local) — A segunda rodada dos estados, grupo 2: Barreira, Provocando, Fortalecido, Iniciativa e Frenesi (proposta)

- **Feito:** a figura de corpo inteiro na bolha preenchida (Barreira), a figura de braços abertos com três setas
  separadas (Provocando), a seta verde com a guarda equilibrada (Fortalecido), o golpe rápido com brilho na ponta
  (Iniciativa; a exclamação preservada) e as três divisas crescentes (Frenesi; as garras preservadas), em
  `estados_restantes/` (`rodada2-lote5.png` a `rodada2-lote7.png`); a prancha `geral.png` atualizada, com os
  integrados, os candidatos preservados e as alternativas novas identificados; a avaliação no `LEIA-ME.md` da pasta.
- **Pendências:** o conector do Aseprite (MCP) não conectou nesta sessão (para usá-lo de novo: reconectar o
  `aseprite-bridge` pelo `/mcp` e, se preciso, reabrir o Aseprite, porque a linha de comando derruba o canal do editor
  aberto); a exclusão local de `ferramentas/arte/referencias/capacete/elmo-frente-jean.webp`, feita pelo Jean, continua
  fora dos commits.
- **Próximo passo:** o Jean avaliar os nove (as folhas `rodada2-*` e `geral.png`) e decidir o giro do selo do
  Atordoado. Nada novo integrado; a versão continua 1.158.0. Inimigos, pets e outras etapas não começados.

### 21/10/2026 (data do computador local) — Chamas, Fortalecido, Enfraquecido e Frenesi no jogo (1.159.0)

- **Decisão de Jean:** integrar sem retoques as Chamas R2 (`805c238d`), o Fortalecido R2 (`39f85d92`), o Enfraquecido
  R2 (`805c238d`) e o Frenesi das três garras da primeira rodada (`b17ab3dd`; não as divisas da R2).
- **Feito:** as fontes em `ferramentas/arte/aseprite/estado-<id>/` (queimadura, fortalecido, enfraquecido, frenesi), os
  PNGs de 16 e @2x idênticos byte a byte aos aprovados (`todas --conferir`: tudo igual); o papel `ESTADO` em
  `icones.js`; os sprites `chama`, `espada`, `osso` e `raio` nos outros usos. Conferido no jogo a 1920×945 com os
  arquivos de produção (os chips e os selos das Chamas e do Enfraquecido); o Fortalecido e o Frenesi não têm selo de
  chegada no jogo. O MCP do Aseprite continuou conectado depois das exportações em lote. Folha:
  `estados_restantes/integracao-1.159.0.png`.
- **Continua:** Veneno, Iniciativa, Atordoado e Barreira em novas alternativas; Provocando pendente, sem mudança.

### 21/10/2026 (data do computador local) — A terceira rodada: Veneno, Iniciativa, Atordoado e Barreira (proposta)

- **Feito:** a gota do Veneno sem a poça (a serpente preservada e recomendada); três exclamações para a Iniciativa (a
  barra larga, o estouro, a inclinada com rastro); três conceitos estáticos para o Atordoado (as estrelinhas, a
  ampulheta parada, o elmo rachado); três Barreiras sem pessoa (a cúpula, a parede que para a flecha, o golpe na
  película). Fontes montadas **no editor pelo MCP**, exportação conferida, o conector de pé depois das exportações em
  lote. Folhas `rodada3-<estado>.png` e a prancha `geral.png` com integrados, alternativas não escolhidas e propostas
  em avaliação; a avaliação no `LEIA-ME.md` de `estados_restantes/`.
- **Continua:** nada destes aprovado; Provocando pendente, sem mudança; a versão continua 1.159.0. Inimigos, pets e
  outras etapas não começados.

### 21/10/2026 (data do computador local) — Veneno, Atordoado e Barreira no jogo (1.160.0)

- **Decisão de Jean:** integrar sem retoques, da terceira rodada, a gota verde sem a poça (Veneno), as três
  estrelinhas estáticas (Atordoado) e o golpe na película (Barreira); a cúpula e a parede da Barreira ficam guardadas
  como não escolhidas.
- **Feito:** as fontes em `ferramentas/arte/aseprite/estado-<id>/` (veneno, atordoado, barreira), os PNGs de 16 e @2x
  idênticos byte a byte aos aprovados (`todas --conferir`: tudo igual); o papel `ESTADO` em `icones.js`; os sprites
  `gota_verde`, `estrela` e `escudo_azul` nos outros usos. Conferido no jogo a 1920×945 com os arquivos de produção:
  os chips (a Barreira também ao lado do Em guarda) e os três selos de chegada (Flecha Envenenada, Prisão de Gelo,
  Barreira Arcana). Folha: `estados_restantes/integracao-1.160.0.png`.
- **Continua:** Iniciativa (A e B finalistas) e Provocando (o acabamento do busto, no protótipo) em avaliação.

### 21/10/2026 (data do computador local) — Provocando: o acabamento do busto (proposta)

- **Feito:** o candidato do `b17ab3dd` (o busto com as setas convergindo) com a figura em branco e uma sombra contida no
  pescoço e na beira direita, no lugar dos quatro cinzas modelados; a mesma silhueta e as mesmas setas
  (`estado-provocando-claro`, fonte pelo MCP). Folha `estados_restantes/rodada3-provocando.png` (original × ajuste na
  carta a 1920×945) e a prancha `geral.png`.
- **Continua em avaliação:** Provocando (o ajuste) e Iniciativa (as finalistas A, a barra larga, e B, o estouro, sem
  mudança). A versão continua 1.160.0. Nenhuma outra etapa começada.

### 21/10/2026 (data do computador local) — Provocando e Iniciativa no jogo (1.161.0): os 17 estados concluídos

- **Decisão de Jean:** integrar sem retoques o Provocando (a figura branca do `9e4ec85a`, com as três setas da
  composição original) e a Iniciativa (a opção A da terceira rodada, a exclamação de barra larga; o estouro B fica como
  alternativa não escolhida).
- **Feito:** as fontes em `ferramentas/arte/aseprite/estado-provocando/` e `estado-iniciativa/`; os PNGs de 16 e @2x
  idênticos byte a byte aos aprovados (`todas --conferir`: tudo igual); o papel `ESTADO` em `icones.js`; a `caveira` e a
  `bota` nos outros usos. Conferido no jogo a 1920×945 com os arquivos de produção e saves temporários: o chip do
  Provocando no esqueleto do Necromante e no urso do Patrulheiro, o selo pela Ordem da Fera (o urso, junto do Em
  guarda), o chip da Iniciativa e o selo da surpresa numa emboscada real (`EMBOSCADA=jogador`, a luta começada com a
  página aberta). Nenhum aviso ou comportamento foi acrescentado para as fotos.
- **Os 17 estados concluídos:** 17 no catálogo (`rpg/estados.py`), 17 no `ESTADO`, todos com arquivo; a prancha final
  `estados_restantes/estados-final.png` (os 17, identificados, com a versão e a origem) e a geral `geral.png`.
- **Continua:** o bloco 1E segue com inimigos, pets, caminhos e minimapa, **não começados**; a versão é 1.161.0.

### 21/10/2026 (data do computador local) — O levantamento visual das criaturas (1E.3, só levantamento)

- **Pedido de Jean:** levantar inimigos, chefes, animais, invocações e companheiros, os usos, os tamanhos e os
  compartilhamentos, com folhas de contato e capturas; recomendar o primeiro par. Nada desenhado nem integrado.
- **Feito:** `ferramentas/prototipos/hud/criaturas/` (o `LEIA-ME.md` com as conclusões, a tabela gerada `levantamento.md`,
  as folhas `tracos.png`, `compartilhamentos.png` e `referencias.png`, as capturas a 1920×945 e o `registro.json` com os
  tamanhos medidos). O cenário `covil` dos testes de navegador ganhou `BESTIARIO` (só para abrir o Bestiário com
  criaturas). Contagem: 57 entidades, 9 desenhos únicos de criatura (pelos traços), nenhum com registro de aprovação.
- **Recomendação (aguarda o Jean):** Lobo e Bandido, como cabeças de 16×16 para a carta (2×) e o Bestiário (3×), no
  padrão dos retratos de carta aprovados; depois Afogado e Ilse.
- **Continua:** a frente 1E.3 em andamento; caminhos, minimapa, talentos e habilidades não começados. Versão 1.161.0.

### 21/10/2026 (data do computador local) — Criaturas, primeiro par: o Afogado e a carta da Ilse (proposta)

- **Decisão de Jean:** começar pelo Afogado e pela carta da Ilse.
- **Feito:** as duas cabeças de 16×16 no formato dos retratos de carta aprovados (sem contorno, cabeça e ombros até a
  base), a Ilse transposta da figura da cena com a mesma paleta; fontes montadas no editor pelo MCP, exportação
  conferida; a folha `ferramentas/prototipos/hud/criaturas/afogado_ilse/afogado-ilse.png` com as cartas na luta a
  1920×945 (o Afogado ao lado do esqueleto; a Ilse na luta real do fundo da capela), o Bestiário e as duas ao lado do
  Morel e da Odette. A avaliação no `LEIA-ME.md` da pasta.
- **Continua:** nada aprovado; a versão continua 1.161.0. A integração vai pedir um papel do retrato pela espécie e
  pelo chefe (sem mexer nos traços).

### 21/10/2026 (data do computador local) — Criaturas, segunda rodada: a Ilse com fios de alga e o Afogado B (proposta)

- **Pedido de Jean:** refinar a Ilse (mais volume de algas, com fios soltos mas juntos, não um maço, e fios na frente
  do rosto) e fazer uma alternativa do Afogado (o atual lia como "carinha surpresa": testa, bochechas, mandíbula,
  inchaço e assimetria), preservando a primeira proposta. Só no protótipo.
- **Feito:** `ilse-r2` e `afogado-b` ao lado das primeiras (`ilse`, `afogado`, intactas), fontes pelo MCP, exportação
  conferida; a folha `ferramentas/prototipos/hud/criaturas/afogado_ilse/afogado-ilse-r2.png` (a Ilse da cena, as
  cartas a 2× e a caixa a 3× ao lado do Morel e da Odette, a luta e o Bestiário a 1920×945). A avaliação no `LEIA-ME.md`.
- **Continua:** nada aprovado; a versão continua 1.161.0. Mapeamentos, regras, arte de cena e produção intactos.

### 21/10/2026 (data do computador local) — Criaturas, terceira rodada: a Ilse transposta e três Afogados (proposta)

- **Pedido de Jean:** transpor para 16×16 a imagem gerada na conversa que ele guardou em
  `ferramentas/arte/referencias/icones/Retrato pixelado azul com algas soltas.png` (a cena continua a referência de
  identidade e paleta) e fazer três Afogados livres, com construções diferentes, na linguagem da comitiva; as versões
  anteriores ficam como histórico.
- **Feito:** `ilse-r3` (com a referência reduzida numa camada guia oculta) e `afogado-cabelo`, `afogado-perfil`,
  `afogado-cranio`, na escala da comitiva; fontes pelo MCP, exportação conferida; a folha
  `ferramentas/prototipos/hud/criaturas/afogado_ilse/afogado-ilse-r3.png` (a referência, a cena e a transposta; os três
  lado a lado; todos ao lado do Morel e da Odette; a luta, o Bestiário e a carta da Ilse a 1920×945). A avaliação no
  `LEIA-ME.md` da pasta; a referência registrada no `LEIA-ME.md` de `referencias/icones/`.
- **Continua:** nada aprovado; a versão continua 1.161.0. Mapeamentos, regras, arte de cena e produção intactos.

### 21/10/2026 (data do computador local) — Criaturas, o primeiro par no jogo: o Afogado C e a Ilse R3 (1.162.0)

- **Decisão de Jean:** o Afogado C (`afogado-cranio`) sem retoques e a Ilse R3 com o olho 1 px para a esquerda; as
  outras alternativas ficam no protótipo como histórico.
- **Feito:** fontes em `ferramentas/arte/aseprite/retrato-afogado/` e `retrato-ilse/` (16; o 32 e o 48 derivados ×2
  e ×3); `dados.retrato` escolhe pela chave (a Ilse) e pela família (o Afogado) antes dos traços; `Icones.criatura`
  na luta, no Bestiário, no mural e no rastro dos contratos e na faixa do mestre caçador. Teste novo
  `tests/test_retratos.py`; o cenário `tutorial` ganhou `CONTRATO_FAMILIA`. A folha
  `ferramentas/prototipos/hud/criaturas/afogado_ilse/afogado-ilse-final.png`.
- **Continua:** as outras criaturas seguem pelos traços (o levantamento: o rosto de lobo compartilhado, o troll na
  caveira, o humano genérico, o Lich que troca de desenho). O próximo par é decisão do Jean.

### 21/10/2026 (data do computador local) — Criaturas, segundo par: o Lobo e o Bandido (proposta)

- **Pedido de Jean:** duas propostas distintas de cada, só no protótipo, para escolher a direção.
- **Feito:** em `ferramentas/prototipos/hud/criaturas/lobo_bandido/`: o Lobo A (de frente) e B (de perfil), o
  Bandido A (o desertor, a cabeça raspada e o lenço no pescoço) e B (a salteadora de capuz); fontes pelo MCP,
  exportação conferida; as folhas `lobo.png` e `bandido.png` (a carta e o Bestiário a 1920×945 com os mesmos dados,
  a fileira com o Morel, a Odette e o herói, a 12×). O alcance previsto (só as famílias `lobo` e `bandido`; o
  `fera` do animal do herói e das outras feras e o `humano` dos outros humanos continuam) e a avaliação no
  `LEIA-ME.md` da pasta. Minha preferência: Lobo A e Bandido A.
- **Continua:** nada aprovado; a versão continua 1.162.0. O Afogado e a Ilse intactos.

### 21/10/2026 (data do computador local) — Criaturas, segundo par, segunda rodada (proposta)

- **Pedido de Jean:** o Lobo A continua, com a base refeita (o começo do pescoço de um quadrúpede no lugar dos ombros
  e do peito) e um ajuste discreto no olhar e no focinho; três Bandidos novos com ameaça (o A e o B ficam como
  histórico).
- **Feito:** `lobo-a-base` e `lobo-a-ajustado`; `bandido-brutamontes`, `bandido-chapeu` e `bandido-faca`; fontes pelo
  MCP, exportação conferida; as folhas `lobo-r2.png` e `bandido-r2.png` em
  `ferramentas/prototipos/hud/criaturas/lobo_bandido/` (a carta e o Bestiário a 1920×945 com os mesmos dados, a
  fileira com os retratos aprovados, a 12×). Minha preferência: o Lobo ajustado e o Bandido da faca.
- **Continua:** nada aprovado; a versão continua 1.162.0.

### 21/10/2026 (data do computador local) — Criaturas, o segundo par no jogo: o Lobo e o Bandido (1.163.0)

- **Decisão de Jean:** o Lobo "só a base" (não o ajustado), com a limpeza de três sobras soltas, e o Bandido da faca
  sem retoques; o Bandido do chapéu guardado como conceito para um possível chefe (fora do jogo).
- **Feito:** fontes em `ferramentas/arte/aseprite/retrato-lobo/` e `retrato-bandido/`; `RETRATO_FAMILIA` com `lobo` e
  `bandido`, `CRIATURA` com os dois; `tests/test_retratos.py` com as famílias e os vizinhos que continuam no traço. As
  folhas `lobo-limpeza.png` e `lobo-bandido-final.png` em `ferramentas/prototipos/hud/criaturas/lobo_bandido/`; o
  conceito reservado no `LEIA-ME.md` de lá ("Conceito reservado").
- **Continua:** as outras criaturas seguem pelos traços (o `fera` do animal do herói e das outras feras, o `humano`
  dos outros humanos, a caveira do troll). O próximo par é decisão do Jean.

### 21/10/2026 (data do computador local) — Os animais do patrulheiro (proposta)

- **Pedido de Jean:** duas propostas do Urso Pardo e duas do Falcão Peregrino, e o teste do retrato do Lobo integrado,
  sem mudança, no lugar do Lobo Cinzento aliado; só no protótipo.
- **Feito:** em `ferramentas/prototipos/hud/criaturas/animais/`: `urso-a` (de frente), `urso-b` (de perfil),
  `falcao-a` (a cabeça de perfil) e `falcao-b` (três quartos com a asa); fontes pelo MCP, exportação conferida; as
  folhas `urso.png`, `falcao.png`, `lobo-cinzento.png` e `animais.png` (a carta aliada e o painel da comitiva a
  1920×945 com os mesmos dados, a 3× e a 12×; a fileira com os retratos aprovados). Os usos reais (a carta aliada e o
  painel; a figura do acampamento fica fora) e a avaliação no `LEIA-ME.md` da pasta. Minha preferência: o Urso A, o
  Falcão A e o Lobo reaproveitado.
- **Continua:** nada aprovado; a versão continua 1.163.0. O `fera` e o `voador` iguais.

### 21/10/2026 (data do computador local) — Os animais do patrulheiro: a transposição das referências (proposta)

- **Pedido de Jean:** um candidato de Urso e um de Falcão transpostos das duas imagens geradas que ele deixou em
  `ferramentas/arte/referencias/icones/`, pelo processo da Ilse; o Lobo Cinzento intacto.
- **Feito:** `urso-t` e `falcao-t` em `ferramentas/prototipos/hud/criaturas/animais/` (a guia oculta nas fontes),
  fontes pelo MCP, exportação conferida; a folha `transposicao.png` (a referência, A anterior × t na carta aliada e
  no painel a 1920×945, a 3×, a 12×, a fileira com os retratos aprovados). As referências registradas no `LEIA-ME.md`
  de `referencias/icones/`.
- **Continua:** nada aprovado; a versão continua 1.163.0.
- **Último ajuste (pedido de Jean):** `falcao-t2` (o amarelo fechando o canto de trás do olho) e `urso-t2` (a boca reta
  e o queixo sem a linha clara), sobre os `t`, que ficam; a folha `ajuste.png`. Nada aprovado.

### 21/10/2026 (data do computador local) — O Urso e o Falcão do patrulheiro no jogo (1.164.0)

- **Decisão de Jean:** o Urso t2 e o Falcão t2 do `ca36d71d`, sem retoques; o Lobo Cinzento como está.
- **Feito:** fontes em `ferramentas/arte/aseprite/retrato-urso/` e `retrato-falcao/` (a guia oculta; o 32 derivado ×2);
  o papel `ANIMAL` em `icones.js` pelo tipo do animal, na carta aliada e no painel da comitiva; `tests/test_retratos.py`
  com os dois. A folha `ferramentas/prototipos/hud/criaturas/animais/final.png`.
- **Continua:** o Lobo Cinzento no `fera`; o `fera` e o `voador` dos inimigos e a figura do acampamento iguais. O
  próximo trabalho de criaturas é decisão do Jean.

### 21/10/2026 (data do computador local) — O Lobo Cinzento no jogo e os resumos do plano (1.165.0)

- **Decisão de Jean:** o Lobo Cinzento aliado com exatamente o retrato do Lobo inimigo (1.163.0), sem redesenho; e os
  resumos do plano 23 e do `docs/ROADMAP.md` em dia com as entregas.
- **Feito:** `lobo: "retrato-lobo"` no `ANIMAL` de `icones.js` (o mesmo arquivo, sem cópia); a carta aliada e o
  painel iguais ao teste aprovado; a folha `ferramentas/prototipos/hud/criaturas/animais/lobo-cinzento-final.png`.
  **Os três animais do patrulheiro estão concluídos.** No plano 23, o estado de referência de 21/10 (o de 19/10 como
  histórico), a tabela da ordem imediata, a situação de cada parte da 1E e a próxima passagem de trabalho; no
  ROADMAP, o estado e a tabela.
- **Agora:** 1E.3, as demais criaturas, os chefes e as invocações (o próximo par é decisão do Jean); depois 1E.4, os
  caminhos e os símbolos do mapa/minimapa; depois as etapas 2–9, com habilidades, talentos, Grimório e árvore na 8.

### 21/10/2026 (data do computador local) — 1E.3: a Aranha Gigante e o Troll (proposta)

- **Pedido de Jean:** duas direções de cada, só no protótipo; o Rei Troll fora.
- **Feito:** em `ferramentas/prototipos/hud/criaturas/aranha_troll/`: `aranha-a` (de frente), `aranha-b` (de lado em
  ameaça), `troll-a` (de frente) e `troll-b` (de perfil com a corcunda); fontes pelo MCP, exportação conferida (com o
  32 e o 48 derivados); as folhas `aranha.png` e `troll.png` (a carta e o Bestiário a 1920×945 com os mesmos dados, a
  fileira com os retratos aprovados, a 12×). O alcance previsto e a avaliação no `LEIA-ME.md` da pasta. Minha
  preferência: a Aranha A e o Troll A.
- **Continua:** nada aprovado; a versão continua 1.165.0.
- **Segunda rodada (pedido de Jean; o A e o B não escolhidos, como histórico):** três de cada pelas duas referências
  geradas que ele deixou em `ferramentas/arte/referencias/icones/`: `aranha-1` a `-3` e `troll-1` a `-3` (o troll de
  carne), com a guia oculta nas fontes; as folhas `aranha-r2.png` e `troll-r2.png`. Minha preferência: a Aranha 2 e o
  Troll 1. Nada aprovado.

### 21/10/2026 (data do computador local) — O Troll da montanha no jogo (1.166.0)

- **Decisão de Jean:** o Troll 1 (em três quartos, de carne) do `4d43ce10`, sem retoques, pela família `troll`; o Rei
  Troll fora.
- **Feito:** a fonte em `ferramentas/arte/aseprite/retrato-troll/` (a guia oculta; o 32 e o 48 derivados ×2 e ×3);
  `RETRATO_FAMILIA` e `CRIATURA` com o troll; `tests/test_retratos.py` com o troll e o Rei na caveira; o cenário
  `tutorial` ganhou `CHEFE`. A folha `ferramentas/prototipos/hud/criaturas/aranha_troll/troll-final.png`.
- **Continua:** o Rei Troll e a Aranha no protótipo; a Rainha Aracnídea fora.

### 21/10/2026 (data do computador local) — O Rei Troll e a Aranha 2B (propostas)

- **Pedido de Jean:** o Rei Troll a partir do Troll 2 (a coroa de sucata, recusada; depois a coroa dourada pela
  referência gerada que ele mandou, sem mexer no rosto) e a Aranha 2 reconstruída (as quelíceras, as presas curtas e
  escuras, os olhos pequenos, as patas ligadas ao corpo).
- **Feito:** `rei-troll` (a sucata), `rei-troll-ouro` (a coroa dourada numa camada própria sobre o Troll 2) e
  `aranha-2b`, em `ferramentas/prototipos/hud/criaturas/aranha_troll/`; as folhas `rei-aranha.png` e `rei-coroa.png`;
  a referência da coroa guardada em `ferramentas/arte/referencias/icones/`.
- **Continua:** nada aprovado; o Rei e a Aranha fora de produção; a versão continua 1.166.0.
- **Ajuste das pontas (pedido de Jean):** `rei-troll-ouro2`, só as três pontas da coroa dourada (as dos lados subindo,
  a do meio em triângulo, os vãos abertos), o resto igual; a folha `rei-pontas.png`. Nada aprovado.

### 21/10/2026 (data do computador local) — O Rei Troll e a Aranha gigante no jogo (1.167.0)

- **Decisão de Jean:** o Rei Troll com a coroa `rei-troll-ouro2` e a Aranha 2B, sem retoques.
- **Feito:** fontes em `ferramentas/arte/aseprite/retrato-rei-troll/` e `retrato-aranha/` (conferidas contra as
  propostas antes de gravar); o Rei pelo id do guardião (`RETRATO_GUARDIAO`, o `guardiao` em `instanciar_guardiao`), a
  Aranha pela família (com as invocadas); a Rainha Aracnídea no `fera`; `tests/test_retratos.py`; o cenário `tutorial`
  ganhou `INVOCADOS`. A folha `ferramentas/prototipos/hud/criaturas/aranha_troll/rei-aranha-final.png`.
- **Continua:** a 1E.3 com as demais criaturas (o próximo par é decisão do Jean).

### 21/10/2026 (data do computador local) — 1E.3: a Rainha Aracnídea e o Esqueleto (proposta)

- **Pedido de Jean:** duas propostas de cada, só no protótipo; os papéis do esqueleto verificados separadamente.
- **Feito:** em `ferramentas/prototipos/hud/criaturas/rainha_esqueleto/`: `rainha-a` (de frente e enorme), `rainha-b`
  (descendo pelo fio), `esqueleto-a` (de frente) e `esqueleto-b` (em três quartos); fontes pelo MCP, exportação
  conferida (a Rainha só o 32; o Esqueleto o 32 e o 48); as folhas `rainha.png` e `esqueleto.png` (a carta, o
  Bestiário, a Rainha ao lado da Aranha, os papéis do esqueleto, a fileira, a 12×). O alcance e a avaliação no
  `LEIA-ME.md` da pasta. Minha preferência: a Rainha A e o Esqueleto A.
- **Continua:** nada aprovado; a versão continua 1.167.0.

### 21/10/2026 (data do computador local) — A Rainha Aracnídea no jogo (1.168.0)

- **Decisão de Jean:** a Rainha A, sem retoques (o abdome e a marca vermelha inclusive), pelo id estável da guardiã.
- **Feito:** a fonte em `ferramentas/arte/aseprite/retrato-rainha-aracnidea/` (só o 32 derivado, a carta da luta;
  `DERIVADOS`); os PNGs idênticos aos da proposta; `RETRATO_GUARDIAO` com a Rainha; as aranhas comuns e as invocadas
  continuam com o retrato da Aranha gigante; `tests/test_retratos.py`. A luta com as aranhas invocadas, com os arquivos
  reais, na folha `ferramentas/prototipos/hud/criaturas/rainha_esqueleto/rainha-final.png`.
- **Continua:** o Esqueleto no protótipo.

### 21/10/2026 (data do computador local) — O Esqueleto A2, só no protótipo

- **Pedido de Jean:** o Esqueleto A melhorado pela referência gerada na conversa (guardada como o original em
  `ferramentas/arte/referencias/icones/Esqueleto frontal em pixel art.png`), em 16×16 nativos, no Aseprite pelo
  conector com a guia oculta; A × nova na carta e no Bestiário; nada no jogo.
- **Feito:** `esqueleto-a2` em `ferramentas/prototipos/hud/criaturas/rainha_esqueleto/` (a guia, a grade, a fonte em
  camadas, a exportação conferida, as fotos `MODOS=a,a2` e a folha `esqueleto-a2.png`); o processo e a minha leitura
  no `LEIA-ME.md` da pasta. Registrada a exclusão de `referencias/capacete/elmo-frente-jean.webp`, feita e autorizada
  pelo Jean.
- **Continua:** a avaliação do A2 pelo Jean; a versão continua 1.168.0; o servo aliado, o Lich e os outros
  mortos-vivos fora.

### 21/10/2026 (data do computador local) — O nariz do Esqueleto A2 (A2n), só no protótipo

- **Pedido de Jean:** a cavidade nasal do A2 (`2d7cacb3`) virou um risco estreito; refazer só essa região, compacta e
  mais ou menos triangular como na referência, separada das órbitas e da boca.
- **Feito:** `esqueleto-a2n` (seis pixels nas linhas 8 e 9, retocados na cópia da fonte pelo conector; releitura,
  exportação e ampliações conferidas; o A2 intacto) e a folha compacta `esqueleto-a2n.png`, em
  `ferramentas/prototipos/hud/criaturas/rainha_esqueleto/`.
- **Continua:** a avaliação do Jean; nada no jogo (a versão continua 1.168.0; a Rainha integrada, os outros retratos
  intactos).

### 21/10/2026 (data do computador local) — O sorriso do Esqueleto (S1 e S2), só no protótipo

- **Decisão de Jean:** o A2n (`ee82b54a`) é a base; agora o sorriso macabro de caveira (a orientação anterior de evitar
  sorriso deixa de valer nesse ponto), só na boca e na mandíbula, em duas variações.
- **Feito:** `esqueleto-s1` (contido) e `esqueleto-s2` (marcado), retocados em cópias da fonte do A2n pelo conector
  (releitura, composto, exportação e ampliações conferidos; o A2n intacto), e a folha `esqueleto-sorriso.png`, em
  `ferramentas/prototipos/hud/criaturas/rainha_esqueleto/`.
- **Continua:** a escolha do Jean; nada no jogo (a versão continua 1.168.0).

### 21/10/2026 (data do computador local) — O animal no acampamento e o comando Atacar: levantamento

- **Pedido de Jean:** registrar as duas pendências no plano 23 e levantar os caminhos, tamanhos e compartilhamentos; o
  teste do arco aprovado no Atacar do Arqueiro; o desenho com a Besta, sem mudar a regra; a conferência dos três
  ataques básicos. Nada desenhado nem integrado.
- **Feito:** `ferramentas/prototipos/hud/acampamento_atacar/` (o `LEIA-ME.md` com o resultado e a proposta dos três
  animais; a folha `levantamento.png`); as pendências e o resultado no plano 23; o cenário `fogueira` aceita
  `FERA=urso` e `FERA=falcao`.
- **Achados:** o urso aparece como o lobo (o mesmo `fera`) e o falcão como o morcego (`voador`); o Atacar do Arqueiro e
  o do Mago usam os sprites antigos; com a Besta, o Atacar continua o `arco`.
- **Continua:** a avaliação do Jean (a proposta dos animais, o arco no Atacar, o cajado do Mago).

### 21/10/2026 (data do computador local) — O arco no Atacar do Arqueiro (1.169.0)

- **Decisão de Jean:** o teste do arco aprovado; integrar com o arquivo existente, preservando a escolha pela classe
  (com a Besta também).
- **Feito:** `ACAO.arco` em `icones.js`; conferido no jogo com o arco e com a Besta (`ferramentas/prototipos/hud/
  acampamento_atacar/capturas-1169/`); a versão 1.169.0.
- **Continua:** o cajado no Atacar do Mago (teste no protótipo), os animais do acampamento (proposta) e o Grimório na
  etapa 8.

### 21/10/2026 (data do computador local) — Os animais do acampamento e o cajado do Mago, só no protótipo

- **Pedido de Jean:** uma figura por animal (o lobo deitado, o urso sentado, o falcão no toco), conferida na cena; o
  cajado aprovado testado no Atacar do Mago.
- **Feito:** `animal-lobo`, `animal-urso`, `animal-falcao` em `ferramentas/prototipos/hud/acampamento_atacar/` (as
  fontes pelo conector, a exportação conferida, as fotos na fogueira) e o teste do cajado; a folha `animais-cajado.png`.
- **Continua:** a avaliação do Jean; a seleção futura pelo tipo num papel próprio; o Grimório na etapa 8.

### 21/10/2026 (data do computador local) — O Esqueleto C, pela segunda referência gerada, só no protótipo

- **Decisão de Jean:** S1 e S2 não aprovados; a nova referência (`ferramentas/arte/referencias/icones/Caveira
  esquelética sombria em pixel art.png`) é a principal do rosto inteiro; as anteriores ficam como histórico.
- **Feito:** `esqueleto-c` (a guia oculta, a fonte pelo conector, a exportação e os derivados conferidos) e a folha
  `esqueleto-c.png`, em `ferramentas/prototipos/hud/criaturas/rainha_esqueleto/`.
- **Continua:** a avaliação do Jean; nada no jogo.

### 21/10/2026 (data do computador local) — O Esqueleto C2: a boca de caveira, só no protótipo

- **Jean, sobre a C:** sorriso de propaganda de TV, não de caveira; pesquisar referências.
- **Feito:** pesquisadas as caveiras pequenas do OpenGameArt (CC0; os dentes em tom médio entre o maxilar e a
  mandíbula claros, os cantos nas cavidades); `esqueleto-c2` com só a boca refeita (a C preservada), retocado pelo
  conector e conferido; a folha `esqueleto-c.png` com a referência × C × C2.
- **Continua:** a avaliação do Jean; nada no jogo.

### 21/10/2026 (data do computador local) — O Esqueleto do zero, três direções, só no protótipo

- **Pedido de Jean:** o C2 não agradou; refazer do zero, combinando com a estética do jogo, sem relação com as
  tentativas anteriores; três variações.
- **Feito:** `ferramentas/prototipos/hud/criaturas/esqueleto_novo/`: E1 (o guarda morto, de elmo e malha), E2 (o
  encapuzado) e E3 (a caveira nua em três quartos); as fontes pelo conector, a exportação conferida, a folha
  `esqueleto-novo.png`. Minha preferência: a E1.
- **Continua:** a escolha do Jean; nada no jogo (a versão continua 1.169.0).

### 21/10/2026 (data do computador local) — E1 escolhida; o lobo e o urso, segunda rodada (só no protótipo)

- **Decisões de Jean:** a E1 (o guarda morto) é a direção do esqueleto básico, com a ponta direita da aba do elmo
  limpa; a E2 guardada como conceito reservado para um possível mago esqueleto (sem espécie, habilidades nem
  mapeamento); a E3 não escolhida. O lobo refinado (o pescoço, o volume do corpo, as patas, a cauda); o urso refeito
  como urso pardo sentado. O falcão e o cajado como estão.
- **Feito:** `esqueleto-e1r` (um pixel), `animal-lobo-r2` e `animal-urso-r2` pelo conector, conferidos na cena; a
  folha `ferramentas/prototipos/hud/acampamento_atacar/rodada2.png`.
- **Continua:** a avaliação do Jean; nada no jogo (a versão continua 1.169.0).

### 21/10/2026 (data do computador local) — O lobo e o urso pelas referências geradas (só no protótipo)

- **Pedido de Jean:** refazer os dois pelas referências geradas que ele deixou em `ferramentas/arte/referencias/icones/`
  (`Lobo cinzento deitado em pixel art-1.png`, `Urso-pardo sentado em pixel art-2.png`), a direção de anatomia, pose e
  proporções.
- **Feito:** as guias, `animal-lobo-r3` e `animal-urso-r3` pelo conector (a guia oculta), conferidos na fogueira; a
  folha `ferramentas/prototipos/hud/acampamento_atacar/rodada3.png`. As rodadas anteriores, o falcão, a E1r e o
  cajado preservados.
- **Continua:** a avaliação do Jean; nada no jogo (a versão continua 1.169.0).

### 22/10/2026 (data do computador local) — O lobo e o urso, quarta rodada (só no protótipo)

- **Pedido de Jean:** refinar a r3 (`23bb15bb`) pela leitura na cena: no lobo, os claros (a coxa, o peito, as patas) e
  o nariz; no urso, a cabeça de urso, as patas com peso e a coxa num volume.
- **Feito:** `animal-lobo-r4` e `animal-urso-r4` pelo conector, conferidos na fogueira; a folha
  `ferramentas/prototipos/hud/acampamento_atacar/rodada4.png`. A r3, o falcão, a E1r, o cajado e a produção intactos.
- **Continua:** a avaliação do Jean; nada no jogo (a versão continua 1.169.0).

### 22/10/2026 (data do computador local) — O lobo r5, mais alto (só no protótipo)

- **Pedido de Jean:** o lobo r4 achatado demais; mais altura, a cabeça maior, o tronco mais grosso, o pescoço curto.
- **Feito:** `animal-lobo-r5` (onze linhas) pelo conector, com uma guia na nova escala; conferido na fogueira com o urso
  r4; a folha `ferramentas/prototipos/hud/acampamento_atacar/lobo-r5.png`. O urso r4, o falcão e o resto intactos.
- **Continua:** a avaliação do Jean; nada no jogo (a versão continua 1.169.0).

### 22/10/2026 (data do computador local) — As cabeças do lobo (só no protótipo)

- **Jean:** a cabeça da r5 não aprovada; uma carinha de companheiro, três alternativas sobre o corpo da r5.
- **Feito:** `animal-lobo-c1` (perfil suave), `-c2` (três quartos para o jogador) e `-c3` (livre), pelo conector, na
  fogueira; a folha `ferramentas/prototipos/hud/acampamento_atacar/lobo-cabecas.png`. Minha escolha: a c2.
- **Continua:** a escolha do Jean; nada no jogo (a versão continua 1.169.0).

### 22/10/2026 (data do computador local) — O Lobo Cinzento na fogueira (1.170.0)

- **Decisão de Jean:** o lobo c2 (`53425098`), sem retoques, pelo tipo do animal; o urso e o falcão em avaliação.
- **Feito:** a fonte em `ferramentas/arte/aseprite/figura-lobo/`, os PNGs idênticos aos aprovados; o papel
  `FIGURA_ANIMAL` e `Icones.figuraAnimal` em `icones.js`, pedidos por `acampamento.js`; o teste em
  `tests/test_retratos.py`; conferido na cena real (`ferramentas/prototipos/hud/acampamento_atacar/capturas-1170/`).
- **Continua:** o urso e o falcão do acampamento; as outras cabeças e rodadas do lobo como histórico.

### 22/10/2026 (data do computador local) — A madrugada: o lobo integrado, as pendências e os quatro pares

- **Pedido de Jean (autônomo, sem parar entre os lotes):** concluir a integração do lobo c2; reunir as propostas
  pendentes; escolher e propor quatro pares de criaturas, duas direções de cada; não integrar candidatos novos nem
  começar o mapa.
- **Feito:** o lobo na fogueira (1.170.0, `ff3656b1`); a folha das pendências (`82fae140`); os quatro pares, um commit
  por par (`81281da3` o sapo e a sanguessuga; `eb379a31` o cultista e a bruxa; `b2c82032` o carniçal e o espectro;
  `3943634f` o javali e o rato), com as fontes pelo conector, as fotos a 1920×945 e as folhas; a prancha geral e os
  registros.
- **Minhas preferências:** sapo A, sanguessuga A, cultista A, bruxa B, carniçal A, espectro A, javali A, rato B (os
  pontos fortes e os limites no `LEIA-ME.md` de `quatro_pares/`).
- **Continua:** a avaliação do Jean (o Esqueleto E1r, o urso r4, o falcão, o cajado e os 16 candidatos); depois, 1E.4.

### 22/10/2026 (data do computador local) — O sapo e a sanguessuga no jogo (1.171.0)

- **Decisão de Jean:** o Sapo-touro gigante A e a Sanguessuga gigante A, sem retoques; os outros candidatos continuam
  em proposta (o cultista, a bruxa, o carniçal, o espectro, o javali e o rato com novas rodadas pedidas).
- **Feito:** as fontes em `ferramentas/arte/aseprite/retrato-sapo/` e `retrato-sanguessuga/`, os PNGs idênticos aos
  aprovados, `RETRATO_FAMILIA` e o papel `CRIATURA`, o teste; conferido na luta e no Bestiário.

### 22/10/2026 (data do computador local) — A segunda rodada das criaturas (só no protótipo)

- **Pedido de Jean:** três capuzes do cultista, três rostos da bruxa, o carniçal com a boca refeita, o espectro de olho
  único, o javali de presas grandes e três reconstruções do rato, sem parar entre os pares.
- **Feito:** `ferramentas/prototipos/hud/criaturas/segunda_rodada/` (as fontes pelo conector, a exportação conferida,
  as fotos com as seis criaturas, as folhas `cultista.png`, `bruxa.png`, `carnical.png`, `espectro.png`, `javali.png` e
  `rato.png`). Minhas preferências: o cultista c1, a bruxa b1, o rato r1; o carniçal, o espectro e o javali com uma
  proposta cada.
- **Continua:** a avaliação do Jean; nada novo no jogo (a versão continua 1.171.0); o Esqueleto E1r, o urso, o falcão e
  o cajado como estavam.

### 22/10/2026 (data do computador local) — O cultista, a bruxa e o rato no jogo (1.172.0)

- **Decisão de Jean:** o Cultista A original, a Bruxa B3 e o Rato r2, sem retoques; o carniçal A2 (a bochecha), o
  javali A2 (a curva das presas) e o espectro (o retrato com os ombros, pela referência nova) seguem no protótipo.
- **Feito:** as fontes de produção, os PNGs idênticos aos aprovados, `RETRATO_FAMILIA` e o papel `CRIATURA`, o teste;
  conferido na luta e no Bestiário.

### 22/10/2026 (data do computador local) — A terceira rodada: o carniçal, o javali e o espectro (só no protótipo)

- **Pedido de Jean:** a bochecha direita do carniçal A2; a curva das presas do javali A2; o espectro pela referência
  nova do manto inflado (a direção corporal escolhida), no retrato com a cabeça e o começo dos ombros.
- **Feito:** `ferramentas/prototipos/hud/criaturas/terceira_rodada/` (`carnical-a3`, `javali-a3`, `espectro-m`; as
  fontes pelo conector, a guia oculta do espectro, as fotos e as folhas de antes × depois); a referência registrada.
- **Continua:** a avaliação do Jean; nada novo no jogo (a versão continua 1.172.0).

### 22/10/2026 (data do computador local) — O javali e o carniçal no jogo (1.173.0)

- **Decisão de Jean:** o Javali A3 e o Carniçal A3, sem retoques; o espectro volta ao A, só com o pano continuando
  até a borda de baixo (no protótipo).
- **Feito:** as fontes de produção, os PNGs idênticos aos aprovados, `RETRATO_FAMILIA` e o papel `CRIATURA`, o teste, o
  gabarito atualizado (só o valor do retrato); conferido na luta e no Bestiário.

### 22/10/2026 (data do computador local) — O espectro AP (só no protótipo)

- **Decisão de Jean:** o espectro M não foi escolhido; o A com o pano continuando até a borda de baixo, sem mudar a
  cabeça; a referência do manto inflado fica como conceito do corpo.
- **Feito:** `espectro-ap` numa cópia da fonte do A (só as linhas 11 a 15; conferido no editor e na exportação) e a
  comparação `ferramentas/prototipos/hud/criaturas/terceira_rodada/espectro-ap.png`.
- **Continua:** a avaliação do Jean; a versão continua 1.173.0.

### 22/10/2026 (data do computador local) — O espectro AP2 (só no protótipo)

- **Pedido de Jean:** tirar as duas dobras escuras de baixo do AP e alargar a abertura do capuz, com o olho no lugar.
- **Feito:** `espectro-ap2` numa cópia da fonte do AP (26 pixels, só na cavidade e nas dobras; conferido no editor e na
  exportação); a comparação `ferramentas/prototipos/hud/criaturas/terceira_rodada/espectro-ap2.png`.
- **Continua:** a avaliação do Jean; a versão continua 1.173.0.

### 22/10/2026 (data do computador local) — O espectro no jogo (1.174.0)

- **Decisão de Jean:** o Espectro AP (`d4f34b5e`), sem retoques; não o AP2.
- **Feito:** a fonte em `ferramentas/arte/aseprite/retrato-espectro/`, os PNGs idênticos ao escolhido,
  `RETRATO_FAMILIA` e o papel `CRIATURA`, o teste, o gabarito (só o valor do retrato); conferido na carta e no Bestiário.
- **Continua:** o Esqueleto E1r, o urso e o falcão do acampamento e o cajado em avaliação; a próxima criatura fica com o
  Jean.

### 22/10/2026 (data do computador local) — Correções de interface, a fome e a frente de criaturas (1.174.1 a 1.174.6)

- **Pedido do Jean:** sete itens (a conversa com o Inventário aberto, o "tudo é ganho" do saque, o Continuar dos
  relatórios, o cursor dos Testes do d20, a fome e a vida bloqueada, o Voltar do Bestiário, a relação das criaturas).
- **Feito, um commit por assunto:** 1.174.1, a carta ✉ numa tela da doca fecha a tela e abre a conversa na hora (antes
  ficava guardada até fechar a tela; o mesmo caminho para todos os companheiros); 1.174.2, o saque sem a linha do espaço
  vazio; 1.174.3, o espólio (relatório da luta e dos baús) fecha no primeiro gesto novo, sem os 900 ms de guarda, pela
  regra do Gesto; 1.174.4, os Testes do d20 com o cursor normal; 1.174.5, **defeito** da fome: comprar ou achar comida
  com fome não recalculava o herói (a vida máxima e os atributos seguiam reduzidos, o bloqueio sem causa, até dormir),
  agora recalcula na hora, sem mudar número de balanceamento (o gabarito mudou só a partir da comida com fome);
  1.174.6, o Bestiário com o Voltar no topo (só na tela; o motor e o gabarito iguais). Regressões em
  `tests/navegador/cliques_seguidos.mjs` (seções 4 e 5), na fumaça (anéis, vila) e em `tests/test_vida_bloqueio.py`.
- **A frente de criaturas** no plano 23 (item 1.12, "A frente de criaturas em 22/10/2026"): integrados, propostas
  aguardando, genéricos, compartilhamentos, reservados e os pares recomendados.
- **Anotado, sem mexer:** a linha "tudo é ganho" nas dicas da mochila e do mercado; o amanhecer de noite ruim ignora
  clique e tecla por 500 ms; nível, especialização e contratos ignoram só o teclado por 600 ms; a marca de contrato no
  texto com `cursor: help`; o cenário `fogueira` com `CONVERSA=1` quebra se houver alguém na `RESERVA` (`cm.membro` não
  acha quem está no acampamento).
- **Continua:** o Esqueleto E1r, o urso e o falcão do acampamento e o cajado em avaliação; o próximo par fica com o Jean.

### 22/10/2026 (tarde, data do computador local) — Integrações, correções, o Esgotado, o par novo e o nome do Ent (1.175.0 a 1.178.0)

- **Retomada em outra conta:** a sessão anterior parou por limite de uso com três commits locais sem push (1.175.0 a
  1.177.0); conferidos e mantidos, sem refazer.
- **Integrados (aprovados pelo Jean, sem retoque):** o Esqueleto E1r pela família, com os invocados do Lich (1.175.0; o
  servo aliado do Necromante, o servo esquelético, o cavaleiro sombrio e o Lich continuam na caveira); o urso r4 e o
  falcão na fogueira, pelo tipo (1.176.0; o lobo c2 e os retratos da carta e do painel iguais); o cajado aprovado no
  Atacar do Mago, pela classe (1.177.0; o Grimório fica para a etapa 8). O gabarito mudou só no valor do retrato
  (caveira → esqueleto) na 1.175.0.
- **Correções, um commit por assunto:** 1.177.1, a mochila e o mercado sem o "tudo é ganho" no espaço vazio (como o
  saque; nos anéis, só a troca com o anel vestido); 1.177.2, a marca de contrato no texto com o cursor normal (é
  informação com dica; a dica e o rótulo ficam); o cenário `fogueira` com `CONVERSA=1` e alguém na `RESERVA`: o defeito
  era só da preparação do cenário (`cm.membro` não acha quem espera no acampamento), o fluxo do jogo estava certo
  (conferido: as duas conversas, o "Levar", dormir), com regressão em `tests/test_cenarios.py`; 1.178.0, a curandeira
  continua aberta depois de tratar (a tela se redesenha com vida, ouro e ferimentos de agora; sem nada para tratar, a
  fala de quem atende e só o Voltar; o resultado numa confirmação curta, "Corte profundo: tratado", 2,4 s, com o "−N
  ouro" de sempre; o clique triplo não trata nem cobra o ferimento seguinte, pela regra do Gesto). Preços, eficácia e
  regras de cura iguais; entrar saudável continua no balcão fechado.
- **Verificações sobre o código final:** `unittest` (647, a fumaça pulada no comando), o gabarito idêntico, o pyflakes só
  com o aviso conhecido e a fumaça inteira (378 conferências, tudo certo), uma vez cada.
- **Em avaliação (protótipo, nada no jogo):** o ícone do Esgotado do mercado (`itens-lote-noite/esgotado/`: não é
  estado, é o motivo do suprimento sem estoque, a 16×16 no cartão, hoje no `cadeado` compartilhado; A, o caixote vazio;
  B, o cesto vazio); o Mercenário (MA, o chapéu de ferro; MB, a coifa de malha) e o Lobo Gélido (LA, o lobo da geada;
  LB, o lobo da nevasca), em `criaturas/mercenario_lobo_gelido/`. As fontes saíram do Aseprite em lote
  (`montar_camadas.lua`): o conector desta sessão estava sem a porta 6515, presa pelo bridge da sessão anterior; só
  aquele node foi encerrado, e o `aseprite-bridge` daqui precisa ser religado pelo `/mcp`.
- **O Ent (só levantamento, nada renomeado):** no jogo são **árvores vivas**, não espíritos: o ent jovem é "árvores que
  acordaram com raiva" (planta, blindado; Preparar Golpe e Regenerar; queima com fogo), da floresta, nível 3+; o Ent
  Ancião é o guardião do covil da floresta, "uma árvore milenar" que abre os olhos e fala, com Agarrar e Varredura, e na
  fase 2 a casca racha e solta uma luz verde. O Espantalho Possuído usa os números do ent jovem. **Três pares**
  (recomendo o primeiro): **Árvore Desperta / Árvore Anciã** (o "acordaram" da descrição e o "milenar" do covil);
  **Árvore Furiosa / Árvore Milenar** (a raiva da descrição e a idade da introdução); **Árvore Jovem / Árvore Anciã** (a
  mesma relação de idade de hoje, a tradução mais conservadora). **Alcance da troca:** os ids `ent_jovem` e
  `ent_anciao` ficam (família, Bestiário, contratos, `BIOMAS`, retrato, guardião); mudam o `nome`, o `plural` e o
  gênero (`g` de "m" para "f": os afixos concordam, "Árvore Desperta Feroz") em `FAMILIAS`, o `base` e o `g` em
  `GUARDIOES["floresta"]`, a fala da fase 2 ("A casca do Ent racha"), a chave de `sinais_do_guardiao`
  (`eventos/comuns.py`, pelo `base`) e o `NOMES_ANTIGOS` de `tests/replay.py`. **Saves:** o guardião gravado guarda o
  `nome` ("<Nome>, o Ent Ancião") e o `base` (os sinais do covil dependem dele), e os contratos guardam o texto
  ("Eliminar 3 ents jovens em …", "Caçar <Nome>, o ent jovem enorme…"): a troca pede uma migração (`migracoes.py`) que
  reescreva esses textos pelo id. O gabarito muda nos nomes, de propósito.
- **Anotado, sem mexer:** o amanhecer de noite ruim ignora clique e tecla por 500 ms; nível, especialização e contratos
  ignoram só o teclado por 600 ms; depois de tratar o último ferimento com a Pita, a fala dela ("Se precisar de
  cuidados, sou eu que atendo") é a do prédio fechado, escrita para quem chega.
- **Continua:** o Jean escolhe o Esgotado, o Mercenário, o Lobo Gélido e o nome do Ent; o próximo par e o mapa não foram
  começados.

### 22/10/2026 (noite, data do computador local) — O Mercenário, o Lobo Gélido, o Esgotado e as árvores (1.179.0 a 1.181.1)

- **Aprovados pelo Jean, sem retoque, e integrados:** o Mercenário MA (o chapéu de ferro) e o Lobo Gélido LA (o lobo da
  geada), pela família, com os usos dela (o Invicto da ponte, os guardas do nobre, a escolta, o Theodore dos Cães de
  Ferro; os afixos; a carta, o Bestiário, o cartaz do mural e o rastreador dos contratos), na 1.179.0; o Senhor da Guerra
  (guardião) e o antagonista continuam no `humano`. O caixote vazio no motivo "Esgotado" do mercado, na 1.180.0: o
  motor manda `motivo_id: "esgotado"`, a tela desenha o papel `MOTIVO`; o cadeado continua nos outros motivos, no
  Salvar, no bloqueio de vida e no talento trancado; o Firme continua com a corrente. O MB, o LB e o cesto ficam
  guardados como não escolhidos. Os PNGs do jogo idênticos byte a byte às propostas; `exportar_aseprite.py todas
  --conferir`: tudo igual ao jogo. Conferido com os arquivos de produção a 1920×945
  (`criaturas/mercenario_lobo_gelido/capturas-1179/`), sem pedido a `ferramentas/` (o cenário `covil` ganhou
  `CONTRATOS=` para os contratos de caça dessas famílias, que não existem no Vale).
- **Os nomes (1.181.0, aprovados):** o ent jovem é a **Árvore Desperta** (plural "árvores despertas", feminino) e o Ent
  Ancião, a **Árvore Anciã**. Os ids `ent_jovem` e `ent_anciao`, os números, as habilidades e as regras ficam. O nome
  vem do catálogo (`FAMILIAS`, `GUARDIOES`); a fala da fase 2 ("A casca da árvore racha"), os sinais do covil e o
  `NOMES_ANTIGOS` do replay acompanham; o Espantalho Possuído, que usa os números da árvore, continua no masculino. O
  texto dos contratos saiu para `contratos.desc_caca` e `desc_alvo`, os mesmos da geração e da migração.
- **Saves antigos (formato 5 → 6, `migracoes._v5_para_v6`):** o guardião gravado (o nome com o artigo, o `base`, o
  gênero), os rumores que citam o nome antigo dele e o texto dos contratos de árvores (aceitos e no mural) são refeitos
  pelo catálogo; ids, progresso e quantidade não mudam, e rodar de novo não muda nada. **Conferido num save gravado pela
  1.178.0** (semente 9): "Vharnar, o Ent Ancião" → "Vharnar, a Árvore Anciã" (também na luta); o rumor; o contrato 23
  (1/4) "Eliminar 4 ents jovens em Bosque da Névoa." → "Eliminar 4 árvores despertas em Bosque da Névoa."; o do mural
  "Caçar Vhararmus, um ent jovem enorme…" → "uma árvore desperta enorme…"; salvar e carregar de novo deu o mesmo save.
  Num jogo novo, a carta e o Bestiário dizem "Árvore desperta". Testes em `tests/test_nomes_arvores.py`.
- **A fala da Pita (1.181.1):** depois do último tratamento, "Pronto. Por aqui, terminamos." na cabana, que continua
  aberta com o Voltar/Esc; quem chega saudável continua vendo a fala de chegada no prédio; a Marta e a curandeira de
  fora do Vau, como antes.
- **O gabarito** mudou só em três coisas, investigadas linha a linha contra as transcrições da 1.178.0: o campo
  `motivo_id` nos dados do mercado, o retrato `humano` → `mercenario` (partidas web) e a versão 5 → 6 do save final;
  nenhuma linha a mais ou a menos, nenhuma escolha, lance ou número. Nenhuma partida do gabarito encontra árvores ou
  lobos gélidos.
- **O conector do Aseprite:** a porta 6515 livre; o `aseprite-bridge` desta sessão continua desligado (religar pelo
  `/mcp`). Não foi preciso editar no Aseprite: as fontes aprovadas foram copiadas sem retoque.
- **A folha:** `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1181.png`.
- **Continua:** o próximo par (a harpia e o grifo é a recomendação) e o mapa esperam o pedido do Jean.

### 22/10/2026 (madrugada seguinte, data do computador local) — Dois pares da 1E.3: a Harpia e o Grifo, o Caído e o Xamã

- **Pedido do Jean:** dois pares, duas propostas por criatura (oito candidatos), só no protótipo, sem parar entre eles.
- **Feito, nada no jogo:** a Harpia (HA, a que grita; HB, a de perfil com a asa) e o Grifo (GA, a águia-leão; GB, o de
  asas abertas) em `ferramentas/prototipos/hud/criaturas/harpia_grifo/`; o Caído (CA, o que ri; CB, o que se esgueira)
  e o Xamã Caído (XA, o do crânio; XB, o do capuz) em `criaturas/caidos/`. Folhas por criatura (atual × A × B, a carta e
  o Bestiário em tamanho real, a fileira com os aprovados, a 12× com a grade) e `criaturas/oito_candidatos.png`.
- **O que define cada um** (dos dados): a harpia, "metade mulher, metade abutre"; o grifo, o rei dos céus que protege o
  ninho (também a mãe do evento do ninho); os caídos são **diabretes** (o traço `demonio`, "cria do Inferno"), covardes
  e em bando, e o xamã é o pequeno feiticeiro deles, que cospe fogo e levanta os caídos. Nenhum invoca outra entidade;
  o Dragão de Gelo (`voador`) e o Cão infernal (`demonio`) ficam fora.
- **A minha preferência (não é aprovação):** HA, GA, CA e XA; as razões e as limitações no tamanho real nos LEIA-MEs.
- **Conferências:** as fontes em camadas pelo Aseprite em lote, com releitura (0 diferentes); o composto exportado
  igual à grade, o @2x exato, o 32 e o 48 em blocos inteiros; as fotos a 1920×945 nos modos atual, A e B, trocados só na
  página, sem erro no console. Nenhum arquivo do jogo mudou.
- **O conector do Aseprite:** indisponível nesta sessão ("Connection closed", sem ferramentas; a porta 6515 livre,
  nenhum processo a encerrar; religar pelo `/mcp`). As fontes saíram pelo fluxo documentado em lote.
- **Anotado, sem mexer:** na luta, "Falcão Peregrino rosna ao seu lado." (o verbo do lobo para o falcão).
- **Continua:** o Jean escolhe os quatro; os chefes, as outras criaturas e o mapa não foram começados.

### 23/10/2026 (data do computador local) — O Caído no jogo (1.182.0) e a rodada do Grifo, da Harpia e do Xamã

- **Integrado (aprovado pelo Jean, sem retoque):** o Caído CA, o que ri, pela família, com os que o xamã ergue (o
  Reviver levanta o mesmo caído morto, com o mesmo retrato; conferido em `tests/test_retratos.py`). O Xamã Caído e o
  Cão infernal continuam no sprite de demônio. Os seis PNGs idênticos byte a byte à proposta; conferido com os arquivos
  de produção na carta, no Bestiário, no cartaz e no rastreador (`criaturas/caidos/capturas-1182/`), sem pedido a
  `ferramentas/`. Folha: `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1182.png`.
- **O gabarito** mudou só no retrato `demonio` → `caido` (134 vezes, nas partidas web), investigado contra as
  transcrições da 1.181; nada mais.
- **Verificações sobre o código final:** `unittest` (a fumaça pulada no comando), o gabarito, o pyflakes e uma fumaça
  inteira (o resultado no commit da integração).
- **No protótipo, aguardando o Jean (`criaturas/rodada_23_10/`):** o Grifo GA2 (a ponta do bico limpa: uma ponta
  escura só, no gancho); três Harpias do zero (H1, a abutre de rosto humano; H2, a da asa erguida; H3, a de bico); três
  Xamãs da cabeça do Caído CA (X1, o velho do capuz; X2, o do cajado; X3, o das penas). Minha preferência: GA2, H1 e X2
  (as razões e as limitações no LEIA-ME). A HA, a HB, o XA e o XB ficam como histórico.
- **O conector do Aseprite:** ainda indisponível (religar pelo `/mcp`); as fontes em camadas pelo Aseprite em lote,
  com releitura.
- **Continua:** a escolha do Jean; outras criaturas, chefes e o mapa não foram começados.

### 22/10/2026 (data do computador local) — A segunda rodada da Harpia, do Grifo e do Xamã (nada no jogo)

- **Retomada noutra conta:** a branch em `3efb488c`; a única alteração local era a referência nova da Harpia, sem
  rastreio. Produção continua na 1.182.0; nada deste lote foi para o jogo.
- **A avaliação do Jean:** nenhuma Harpia aprovada (a H3 e a HA, as mais próximas, ficam como histórico); a nova
  referência gerada (`ferramentas/arte/referencias/icones/Harpia vulturina em pixel art.png`, registrada no LEIA-ME
  das referências) é a principal; o GA2 ficou com a ponta reta; o X1 é a direção do Xamã, ainda não autorizado.
- **No protótipo, aguardando o Jean (`criaturas/rodada_23_10/`, a segunda seção do LEIA-ME):** a **Harpia T**, a
  transposição da referência pela guia proporcional oculta (o recorte de 1000 px reduzido por média); o **Grifo GA3**,
  dois pixels na linha 8 (a ponta escura desce da extremidade); o **Xamã X1r**, a cabeça do X1 igual e o colar num U
  pequeno sob o queixo. As folhas `harpia-t.png`, `grifo-ga3.png` e `xama-x1r.png`. Minha leitura: a T traz a
  construção da referência, mas a 32 lê mais como mulher de cabelo selvagem do que como abutre; o gancho é sutil; o
  X1r é uma melhora contida, e o X1 continua disponível.
- **O conector do Aseprite funcionou:** o bridge desta sessão escutava a 6515 e o Aseprite estava fechado; aberto o
  Aseprite, conectou. Fontes pelo conector (`pintar.lua`, 0 diferentes), a exportação igual à grade. Fotos a 1920×945
  no modo `d`, sem erro no console.
- **Continua:** a escolha do Jean; outras criaturas, chefes e o mapa não foram começados.

### 22/10/2026 (data do computador local) — O Grifo no jogo (1.183.0) e a terceira passada do Xamã e da Harpia

- **Integrado (aprovado pelo Jean, sem retoque):** o Grifo GA3, pela família, também o feroz do ninho; a Harpia e o
  Dragão de Gelo continuam no `voador`. A fonte em `ferramentas/arte/aseprite/retrato-grifo/` e os seis PNGs
  idênticos byte a byte à proposta; conferido no jogo na carta, no Bestiário, no cartaz e no rastreador
  (`criaturas/rodada_23_10/capturas-1183/`), sem pedido a `ferramentas/`. Folha:
  `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1183.png`. O GA e o GA2 ficam como histórico.
- **O gabarito** saiu idêntico (nenhuma das 24 partidas encontra um grifo); não foi atualizado.
- **Verificações sobre o código final:** `unittest` (654; a fumaça pulada no comando), o gabarito, o pyflakes e uma
  fumaça inteira (378 ok).
- **No protótipo, aguardando o Jean (`criaturas/rodada_23_10/`, a terceira seção do LEIA-ME):** o **Xamã X1r2** (a
  pintura branca dos olhos, em diagonal de um lado e reta do outro, agora reta dos dois; dois pixels) e a **Harpia
  T2** (o olhar severo sem a mancha escura no olho; as penas em três tufos longos). As folhas `xama-x1r2.png` e
  `harpia-t2.png`.
- **Continua:** a avaliação do Xamã e da Harpia; outras criaturas, chefes e o mapa não foram começados.

### 22/10/2026 (data do computador local) — A Harpia e o Xamã Caído no jogo (1.184.0)

- **Integrados (aprovados pelo Jean, sem retoque):** a Harpia T2 e o Xamã Caído X1r2, as fontes do `b3f95e28`, pela
  família, com os afixos e o xamã que escolta o bando de caídos. O Dragão de Gelo continua no `voador`, o cão infernal
  no `demonio`; o Grifo GA3 e o Caído CA não mudam. Fontes em `ferramentas/arte/aseprite/retrato-harpia/` (a guia
  oculta) e `retrato-xama-caido/`; exportados numa pasta temporária e comparados byte a byte com as propostas antes de
  gravar no jogo. Conferido no jogo (`criaturas/rodada_23_10/capturas-1184/`): a Harpia ao lado do Grifo, o Xamã ao lado
  dos Caídos, o Bestiário, os cartazes e o rastreador; nenhum pedido a `ferramentas/`. Folha:
  `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1184.png`.
- **O gabarito** mudou só no retrato `demonio` → `xama_caido` (2 estados de combate e 5 painéis do Bestiário da
  `arqueiro-42-web`), comparado campo a campo com as transcrições da 1.183; nenhuma partida encontra uma harpia.
- **Verificações sobre o código final:** `unittest` (655), o gabarito, o pyflakes e uma fumaça inteira.
- **Ainda genéricos:** 7 famílias (Árvore Desperta, golem de pedra, cavaleiro sombrio, servo esquelético, abominação,
  cria do Vazio, cão infernal) e 8 guardiões; a lista no plano 23. **Recomendado a seguir:** o cão infernal e a cria do
  Vazio (as criaturas da Fenda ainda sem retrato).
- **Continua:** a escolha do próximo par pelo Jean; nenhum desenho novo nem o mapa começados.

### 22/10/2026 (data do computador local) — O Cão infernal e a Cria do Vazio: duas propostas de cada (nada no jogo)

- **Estado conferido:** a branch em `fa7d526b`, sem alterações locais; produção na 1.184.0.
- **Levantado antes de desenhar (`ferramentas/prototipos/hud/criaturas/fenda/LEIA-ME.md`):** a identidade e os usos das
  duas. A cria que o antagonista invoca é criada pela mesma família `cria_vazio`, com "(invocado)" no nome, e usará o
  mesmo retrato. As pendências: o servo do Necromante é um aliado de `tipo` servo (na `caveira`), separado das famílias
  inimigas (a família `esqueleto_servo` não é criada por nenhum código); o antagonista fica no `humano`, pelo traço
  `conjurador`.
- **No protótipo, aguardando o Jean (`criaturas/fenda/`):** o Cão infernal A (o que rosna de perfil) e B (o mastim de
  cabeça baixa); a Cria do Vazio A (o caco da Fenda) e B (a fera que anda). As folhas `cao.png` e `cria.png`. Minha
  preferência: o A e a A (as razões e as limitações no LEIA-ME).
- **Processo:** grades à mão; fontes pelo conector do Aseprite (0 diferentes; o composto = as camadas); a exportação
  igual à grade, @2x exato, 32 e 48 em blocos inteiros. Fotos a 1920×945 nos modos atual, a e b (inclusive as crias
  invocadas pelo antagonista, num cenário só do protótipo), sem erro no console.
- **Continua:** a escolha do Jean; outras criaturas, chefes e o mapa não foram começados.

### 22/10/2026 (data do computador local) — A Cria A2 e o Cão T (nada no jogo)

- **Estado conferido:** a branch em `b3780adf`; a única alteração local era a referência nova do Cão, sem rastreio
  (agora registrada no LEIA-ME das referências). Produção na 1.184.0.
- **No protótipo, aguardando o Jean (`criaturas/fenda/`, a segunda seção do LEIA-ME):** a **Cria A2** (a A com um plano
  de luz em cada caco e o escuro fundo junto da fissura) e o **Cão T** (a transposição da referência gerada pela guia
  proporcional oculta). As folhas `cria-a2.png` e `cao-t.png`. Minha leitura: a A2 ganha volume sem perder o ar
  etéreo; o T lê bem a 48, mas a 32 fica pesado e o "cão" depende do nariz e da boca.
- **Processo:** fontes pelo conector do Aseprite (0 diferentes; o composto = as camadas visíveis; a guia oculta);
  exportação igual à grade, @2x exato, 32 e 48 em blocos inteiros; fotos no modo `c`, sem erro no console.
- **Continua:** a escolha do Jean; outras criaturas, chefes e o mapa não foram começados.

### 22/10/2026 (data do computador local) — A Cria do Vazio no jogo (1.185.0) e o Cão N (nada no jogo)

- **Estado conferido:** a branch em `265a9820`, sem alterações locais.
- **Integrada (aprovada pelo Jean, sem retoque):** a Cria do Vazio A2, a fonte do `71e2c80d`, pela família, com os
  afixos, o "Gato do Vazio" e as crias que o antagonista invoca; o antagonista continua no `humano` e o etéreo sozinho
  no `etereo`. Fonte em `ferramentas/arte/aseprite/retrato-cria-vazio/`; exportada numa pasta temporária e comparada
  byte a byte com a proposta antes de gravar. Conferida no jogo (`criaturas/fenda/capturas-1185/`): a luta, a
  invocação, o Bestiário, o cartaz e o rastreador; nenhum pedido a `ferramentas/`. Folha:
  `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1185.png`.
- **O gabarito** saiu idêntico (nenhuma partida encontra uma cria); não foi atualizado.
- **Verificações sobre o código final:** `unittest`, o gabarito, o pyflakes e uma fumaça inteira (378 ok).
- **No protótipo, aguardando o Jean:** o **Cão N** (`criaturas/fenda/`, a terceira seção do LEIA-ME), a construção nova
  depois da recusa do T, resolvida a 32 px; a folha `cao-n.png` (T × N com o Lobo, o Lobo Gélido e o Caído).
- **Continua:** a avaliação do Cão; outras criaturas, chefes e o mapa não foram começados.

### 22/10/2026 (data do computador local) — O retoque do rosto do Cão: o N2 (nada no jogo)

- **Estado conferido:** a branch em `0c17200d`, sem alterações locais; produção na 1.185.0 (a Cria do Vazio integrada
  não mudou). A fonte do N conferida contra a grade antes do retoque.
- **No protótipo, aguardando o Jean (`criaturas/fenda/`, a quarta seção do LEIA-ME):** o **Cão N2**, só as linhas 7 a 14
  do N: o nariz como ponta sólida (o risco era o brilho sobre um nariz negro que sumia), o lábio levantado com a gengiva
  e a abertura estreita com as presas de obsidiana, a mandíbula separada do pescoço por uma sombra. A folha
  `cao-n2.png` (N × N2). Limitação: o rosnado é contido (a boca é pequena) e o focinho continua curto.
- **Processo:** o retoque numa cópia da fonte em camadas pelo conector do Aseprite (0 diferentes; o composto = as
  camadas); exportação igual à grade, @2x exato, 32 e 48 em blocos inteiros; fotos no modo `e`, sem erro no console.
- **Continua:** a avaliação do Cão; outras criaturas, chefes e o mapa não foram começados.

### 22/10/2026 (data do computador local) — Três rosnados do Cão: RA, RB e RC (nada no jogo)

- **Estado conferido:** a branch em `b63a6d73`, sem alterações locais; produção na 1.185.0.
- **No protótipo, aguardando o Jean (`criaturas/fenda/`, a quinta seção do LEIA-ME):** uma cabeça nova (o crânio sobe e
  recua, o focinho ganha 7 a 8 pixels; era o crânio herdado que espremia o focinho) com três rosnados: **RA**, a bocarra
  aberta; **RB**, o lábio repuxado; **RC**, a cabeça baixa. A folha `cao-r.png` (N2 × as três). Minha preferência: a RB;
  a limitação a 32 é a gengiva lida como faixa reta e os dentes pequenos.
- **Processo:** fontes pelo conector do Aseprite (0 diferentes; o composto = as camadas); exportação igual à grade, @2x
  exato, 32 e 48 em blocos inteiros; fotos nos modos `f`, `g` e `h`, sem erro no console.
- **Continua:** a escolha do Jean; outras criaturas, chefes e o mapa não foram começados.

### 22/10/2026 (data do computador local) — A boca da RA refeita: a RA2 (nada no jogo)

- **Estado conferido:** a branch em `a148f693`, sem alterações locais; produção na 1.185.0. A fonte da RA conferida
  contra a grade antes do retoque.
- **No protótipo, aguardando o Jean (`criaturas/fenda/`, a sexta seção do LEIA-ME):** a **RA2**, só as linhas 7 a 11 da
  RA: a gengiva levantada, a cavidade escura contínua em cunha, uma presa de cima dominante e afunilada com o reflexo
  frio, os dentes de baixo sugeridos no fundo escuro, o calor no fundo, a mandíbula pesada. A folha `cao-ra2.png`.
  Limitação a 32: a frente da cavidade encosta no fundo escuro da caixa na borda esquerda.
- **Processo:** o retoque numa cópia da fonte em camadas pelo conector do Aseprite (0 diferentes; o composto = as
  camadas); exportação igual à grade, @2x exato, 32 e 48 em blocos inteiros; fotos no modo `i`, sem erro no console.
- **Continua:** a avaliação do Cão; outras criaturas, chefes e o mapa não foram começados.

### 22/10/2026 (data do computador local) — Os dentes da RA2 refeitos: a RA3 (nada no jogo)

- **Estado conferido:** a branch em `c36bec5c`, sem alterações locais; produção na 1.185.0.
- **No protótipo, aguardando o Jean (`criaturas/fenda/`, a sétima seção do LEIA-ME):** a **RA3**, só as linhas 8 a 10 da
  RA2: a presa de cima saindo do maxilar com a face iluminada em cinza de obsidiana e a de baixo menor, mais atrás,
  saindo da mandíbula (na RA2, a presa quase negra sumia e a boca parecia banguela). A folha `cao-ra3.png`. Limitação a
  32: a presa de baixo é um pixel discreto.
- **Processo:** o retoque numa cópia da fonte em camadas pelo conector do Aseprite (0 diferentes; o composto = as
  camadas); exportação igual à grade, @2x exato, 32 e 48 em blocos inteiros; fotos no modo `j`, sem erro no console.
- **Continua:** a avaliação do Cão; outras criaturas, chefes e o mapa não foram começados.

### 22/10/2026 (data do computador local) — Três bocas cheias do Cão: P1, P2 e P3 (nada no jogo)

- **No protótipo, aguardando o Jean (`criaturas/fenda/`, a oitava seção do LEIA-ME):** sobre a cabeça da RA3, **P1** (a
  bocarra de presas), **P2** (a boca fechada com as presas por fora) e **P3** (o lábio repuxado com a fileira irregular
  de presas). A folha `cao-p.png`. Minha preferência: a P3.
- **Processo:** fontes pelo conector do Aseprite (0 diferentes; o composto = as camadas); exportação igual à grade, @2x
  exato, 32 e 48 em blocos inteiros; fotos nos modos `k`, `l` e `m`, sem erro no console.

### 22/10/2026 (data do computador local) — O Cão infernal no jogo (1.186.0)

- **Estado conferido:** a branch em `e5c14698`, sem alterações locais; a fonte e os PNGs da P1 iguais aos do commit.
- **Integrado (aprovado pelo Jean, sem retoque):** o Cão infernal P1, pela família, com os afixos. Nenhuma família nem
  guardião do catálogo fica mais no sprite `demonio` (ele fica como reserva). Fonte em
  `ferramentas/arte/aseprite/retrato-cao-infernal/`; exportada numa pasta temporária e comparada byte a byte com a P1
  antes de gravar. Conferido no jogo (`criaturas/fenda/capturas-1186/`): a carta com os caídos e o xamã, o Bestiário com a
  faixa do mestre caçador, o cartaz e o rastreador; nenhum pedido a `ferramentas/`. Folha:
  `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1186.png`. As outras tentativas ficam como histórico.
- **O gabarito** saiu idêntico (nenhuma partida encontra um cão infernal); não foi atualizado.
- **Verificações sobre o código final:** `unittest`, o gabarito, o pyflakes e uma fumaça inteira.
- **Continua:** o próximo par recomendado é a abominação com o cavaleiro sombrio; nada começado antes do pedido.

### 22/10/2026 (data do computador local) — A Abominação e o Cavaleiro Sombrio: duas propostas de cada (nada no jogo)

- **Estado conferido:** a branch em `78398623`, sem alterações locais; produção na 1.186.0.
- **Levantado antes de desenhar (`ferramentas/prototipos/hud/criaturas/cidadela/LEIA-ME.md`):** os textos, os traços,
  as habilidades e os encontros das duas; o Cavaleiro também é o Último Guarda antes do antagonista (a mesma família).
  O que vem do jogo e o que é interpretação estão separados no LEIA-ME.
- **No protótipo, aguardando o Jean:** a Abominação A (a boca costurada) e B (o brutamontes curvado); o Cavaleiro
  Sombrio A (o elmo fechado) e B (a espada e a crista). As folhas `abominacao.png` e `cavaleiro.png`. Minha
  preferência: a A e o B.
- **Processo:** grades à mão; fontes pelo conector do Aseprite (0 diferentes; o composto = as camadas); a exportação
  igual à grade, @2x exato, 32 e 48 em blocos inteiros; fotos a 1920×945 nos modos atual, a e b, sem erro no console.
- **Continua:** a escolha do Jean; outras criaturas, chefes e o mapa não foram começados.

### 22/10/2026 (data do computador local) — A segunda rodada da Cidadela: três Abominações e o Cavaleiro A2 (nada no jogo)

- **Estado conferido:** a branch em `fe58c880`, igual ao remoto, sem alterações locais; produção na 1.186.0.
- **Decisão do Jean sobre a primeira rodada:** a Abominação A e B e o Cavaleiro B recusados; o Cavaleiro A aceito só como
  direção para refinar; nenhum retrato autorizado para integração.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/cidadela/LEIA-ME.md`, "A segunda rodada"):
  a Abominação C (a mandíbula torta), D (as duas cabeças) e E (os espinhos de obsidiana) e o Cavaleiro A2 (o elmo mais
  largo e curto, o gorjal ligando às ombreiras em placas). As folhas `abominacao-cde.png` e `cavaleiro-a2.png`. Minha
  preferência: a C e o A2; as limitações no tamanho real estão no LEIA-ME.
- **Processo:** grades à mão, rascunhadas a 32, 48 e 12×; as fontes pelo Aseprite em lote (o conector estava sem editor;
  a janela aberta não foi tocada), 0 diferentes na releitura; a exportação igual à grade, @2x exato, 32 e 48 em blocos
  inteiros; fotos a 1920×945 em `capturas-2/`, sem erro no console. A primeira rodada ficou como estava.
- **Verificações:** só o protótipo mudou (nada em `rpg/` nem em `tests/`): o pyflakes e a sintaxe do roteiro das fotos;
  a suíte, o gabarito e a fumaça não foram rodados, porque o jogo não mudou.
- **Continua:** a escolha do Jean; outras criaturas, chefes e o mapa não foram começados.

### 22/10/2026 (data do computador local) — A terceira rodada da Cidadela: a Abominação C2 e o Cavaleiro T (nada no jogo)

- **Estado conferido:** a branch em `e4d384e5`, igual ao remoto; a única alteração local era a referência nova, deixada
  pelo Jean em `ferramentas/arte/referencias/icones/Cavaleiro sombrio do Vazio.png` (guardada sem alteração, a origem no
  LEIA-ME de lá).
- **Decisão do Jean:** a Abominação C como direção (sem aprovação para integração); a imagem gerada como a referência
  principal do Cavaleiro; A, A2 e B como histórico.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/cidadela/LEIA-ME.md`, "A terceira
  rodada"): a C2 (a boca enorme e torta saindo da carne, com as bochechas e a mandíbula caindo à direita) e o T (a
  transposição da referência, com a guia oculta na fonte). As folhas `abominacao-c2.png` e `cavaleiro-t.png`; as
  limitações no tamanho real no LEIA-ME.
- **Processo:** grades à mão; as fontes pelo Aseprite em lote (o conector sem editor), 0 diferentes na releitura, a guia
  escondida depois da montagem; a exportação igual à grade (sem a guia), @2x exato, 32 e 48 em blocos inteiros; fotos a
  1920×945 nos modos `c2` e `t`, sem erro no console.
- **Verificações:** só o protótipo mudou: o pyflakes e a sintaxe do roteiro das fotos; a suíte, o gabarito e a fumaça
  não foram rodados, porque o jogo não mudou.
- **Continua:** a escolha do Jean; nada integrado; outras criaturas, chefes e o mapa não foram começados.

### 22/10/2026 (data do computador local) — A quarta rodada da Cidadela: a Abominação C3 e o Cavaleiro T2 (nada no jogo)

- **Estado conferido:** a branch em `3b719569`, igual ao remoto, sem alterações locais.
- **Avaliação do Jean:** a C2 caída demais (a orientação de mandíbula muito torta substituída por "deformação monstruosa
  com estrutura legível"); no T, o busto aprovado como base e o elmo sem a perspectiva da referência.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/cidadela/LEIA-ME.md`, "A quarta rodada"):
  a C3 (a partir da C: a boca enorme centralizada, sustentada pelas bochechas, o lábio de cima com volume) e o T2 (o busto
  do T, o elmo refeito: a ponta à esquerda, a quina da testa ao queixo, a lateral larga, a fenda subindo pela lateral, o
  violeta apagado fora do centro). As folhas `abominacao-c3.png` e `cavaleiro-t2.png`; C, C2 e T como histórico.
- **Processo:** grades à mão; as fontes pelo Aseprite em lote (o conector sem editor), 0 diferentes na releitura, a guia
  do T2 oculta; a exportação igual à grade, @2x exato, 32 e 48 em blocos inteiros; fotos a 1920×945 nos modos `c3` e
  `t2`, sem erro no console.
- **Verificações:** só o protótipo mudou: o pyflakes e a sintaxe do roteiro das fotos; a suíte, o gabarito e a fumaça
  não foram rodados, porque o jogo não mudou.
- **Continua:** a escolha do Jean; nada integrado; nenhuma outra criatura começada.

### 22/10/2026 (data do computador local) — A quinta rodada da Cidadela: três Cavaleiros novos (nada no jogo)

- **Estado conferido:** a branch em `9464b59e`, igual ao remoto, sem alterações locais.
- **Avaliação do Jean:** a Abominação C3 aceita visualmente, preservada sem retoques (a integração não foi autorizada);
  do Cavaleiro T2 ficam a capa e as ombreiras; o elmo, o gorjal e o peito refeitos em três propostas diferentes, a
  referência gerada só como apoio do material.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/cidadela/LEIA-ME.md`, "A quinta rodada"):
  P1, o grande elmo de frente; P2, o bico de perfil, olhando para a esquerda (a minha preferência); P3, a cabeça baixa
  afundada no gorjal alto. A capa e as ombreiras iguais às do T2 nas três. A folha `cavaleiro-p.png`.
- **Processo:** grades à mão; as fontes pelo Aseprite em lote (o conector sem editor), 0 diferentes na releitura; a
  exportação igual à grade, @2x exato, 32 e 48 em blocos inteiros; fotos a 1920×945 nos modos `p1`, `p2` e `p3`, sem
  erro no console.
- **Verificações:** só o protótipo mudou: o pyflakes e a sintaxe do roteiro das fotos; a suíte, o gabarito e a fumaça
  não foram rodados, porque o jogo não mudou.
- **Continua:** a escolha do Jean entre os três; nada integrado; nenhuma outra criatura começada.

### 22/10/2026 (data do computador local) — A sexta rodada da Cidadela: o Cavaleiro P4 (nada no jogo)

- **Estado conferido:** a branch em `85ae4571`, igual ao remoto, sem alterações locais.
- **Pedido do Jean:** o P3 e o T2 como direções preferidas (nenhum aprovado); refinar o P3 pela construção do retrato
  aprovado do Guerreiro (`GUERREIRO_CARTA`, `rpg/web/static/retratos.js`), com o capacete mais presente e separado do
  gorjal.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/cidadela/LEIA-ME.md`, "A sexta rodada"):
  o P4, com o elmo maior (a cúpula e a crista do P3, dois planos), a viseira em V, a base escura, o gorjal estreito em
  meio-tom, as ombreiras e o peito do P3; sem brilho. A folha `cavaleiro-p4.png`, com o Guerreiro, o T2, o P3 e o P4.
- **Processo:** grade à mão; a fonte pelo Aseprite em lote (o conector sem editor), 0 diferentes na releitura; a
  exportação igual à grade, @2x exato, 32 e 48 em blocos inteiros; fotos a 1920×945 no modo `p4`, sem erro no console.
- **Verificações:** só o protótipo mudou: o pyflakes e a sintaxe do roteiro das fotos; a suíte, o gabarito e a fumaça
  não foram rodados, porque o jogo não mudou.
- **Continua:** a avaliação do Jean; nada integrado; nenhuma outra criatura começada.

### 22/10/2026 (data do computador local) — O Cavaleiro Sombrio no jogo (1.187.0): o P3, pela família

- **Estado conferido:** a branch em `468d4d6e`, igual ao remoto, sem alterações locais; produção na 1.186.0.
- **Decisão do Jean:** o P3 original aprovado para integração, sem retoques (não o P4); a Abominação C3 fica intacta,
  fora do jogo.
- **No jogo (1.187.0):** `retrato-cavaleiro-sombrio` (16, 32, 48 e os @2x) pela família `cavaleiro_sombrio`
  (`RETRATO_FAMILIA`; o papel `CRIATURA` em `icones.js`), com os afixos e o Último Guarda, que é da família. A `caveira`
  continua com a Bruxa Afogada, o Lich Menor e o servo do Necromante; nenhuma regra mudou.
- **A fonte:** a do P3, e depois, a pedido do Jean na mesma entrega, a do **P3b** (o P3 com os cantos de baixo
  completados: 4 pixels na linha 15, que na caixa pareciam pedaços faltando), copiada byte a byte para
  `ferramentas/arte/aseprite/retrato-cavaleiro-sombrio/`; o 32 e o 48 em `DERIVADOS`; o P3 fica como histórico. Exportados numa pasta temporária e iguais byte a byte à proposta antes de gravar; `--conferir`: tudo igual.
- **Conferido com os arquivos de produção** (`criaturas/cidadela/capturas-1187/`): a luta, o Último Guarda, o
  Bestiário com a faixa do mestre caçador, o cartaz e o rastreador; sem erro no console, nenhum pedido a `ferramentas/`.
  A folha `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1187.png`.
- **Testes:** o cavaleiro pela família, com afixo e como o Último Guarda; os testes que diziam que ele ficava na caveira
  foram ajustados (os outros mortos-vivos sem retrato continuam nela).
- **Verificações sobre o código final:** `unittest` (658, 1 pulado: a fumaça, rodada à parte), o gabarito (idêntico,
  sem atualizar), o pyflakes (só o aviso conhecido) e a fumaça inteira (378 ok, tudo certo; o código não mudou depois
  dela, só os PNGs do retrato).
- **Continua:** a integração da Abominação C3, quando o Jean pedir; outras criaturas, chefes e o mapa não foram começados.

### 22/10/2026 (data do computador local) — A Abominação no jogo (1.188.0): a C3, pela família

- **Estado conferido:** a branch em `85cd419e`, igual ao remoto, sem alterações locais; produção na 1.187.0.
- **Decisão do Jean:** a C3 aprovada para integração, sem retoques; o Cavaleiro P3b da 1.187.0 encerrado.
- **No jogo (1.188.0):** `retrato-abominacao` (16, 32, 48 e os @2x) pela família `abominacao`, com os afixos. O sprite
  `corrompido` continua para quem só tiver o traço; nenhuma regra nem atributo mudou.
- **A fonte:** a da C3, copiada byte a byte para `ferramentas/arte/aseprite/retrato-abominacao/`; o 32 e o 48 em
  `DERIVADOS`. Exportados numa pasta temporária e iguais byte a byte à proposta antes de gravar; `--conferir`: tudo igual.
- **Conferido com os arquivos de produção** (`criaturas/cidadela/capturas-1188/`): a luta, o Bestiário com a faixa do
  mestre caçador, o cartaz e o rastreador; sem erro no console, nenhum pedido a `ferramentas/`. A folha
  `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1188.png`.
- **Testes:** a abominação pela família, com os afixos (o corrompido também); a Árvore Desperta corrompida continua no
  sprite `corrompido`.
- **Verificações sobre o código final:** `unittest` (659, 1 pulado: a fumaça, rodada à parte), o gabarito (idêntico,
  sem atualizar), o pyflakes (só o aviso conhecido) e a fumaça inteira (378 ok, tudo certo).
- **Continua:** as propostas da Árvore Desperta e do golem de pedra (em seguida, num commit separado).

### 22/10/2026 (data do computador local) — A Árvore Desperta e o golem de pedra: duas propostas de cada (nada no jogo)

- **Estado:** depois da integração da Abominação (1.188.0, `1975fdf9`), num commit separado.
- **Levantado antes de desenhar (`ferramentas/prototipos/hud/criaturas/arvore_golem/LEIA-ME.md`):** os textos, os
  traços, as habilidades, os biomas e os eventos das duas. O Espantalho Possuído é criado da família `ent_jovem` e o
  Mímico da família `golem`: herdariam o retrato pela família (a decidir na integração). O `planta` e o `construto`
  continuam com a Árvore Anciã e o Golem Primordial, que ficam para uma rodada própria.
- **No protótipo, aguardando o Jean:** a Árvore A1 (os galhos nus) e A2 (a copa pesada); o golem G1 (a cantaria) e G2
  (o rochedo). As folhas `arvore.png` e `golem.png`. Minha preferência: a A2 e o G2; as limitações no LEIA-ME.
- **Processo:** grades à mão; as fontes pelo Aseprite em lote (o conector sem editor), 0 diferentes na releitura; a
  exportação igual à grade, @2x exato, 32 e 48 em blocos inteiros; fotos a 1920×945 nos modos atual, a e b, sem erro no
  console.
- **Verificações proporcionais (nenhum código do jogo mudou):** o pyflakes dos auxiliares, a sintaxe do roteiro das
  fotos e as grades regravadas iguais às gravadas.
- **Continua:** a escolha do Jean; nada integrado; os chefes e o mapa não foram começados.

### 22/10/2026 (data do computador local) — A Árvore Desperta pelas referências e o Golem G2r (nada no jogo)

- **Estado conferido:** a branch em `91c954d8`, igual ao remoto; as únicas alterações locais eram as duas referências
  novas deixadas pelo Jean em `ferramentas/arte/referencias/icones/` (guardadas sem alteração; a origem no LEIA-ME de lá).
- **Avaliação do Jean:** a A1 e a A2 recusadas; a Árvore pelas duas referências geradas (a 2, a "velha séria", é a
  preferida); o G2 bem encaminhado, só a separação da cabeça.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/arvore_golem/LEIA-ME.md`, "A segunda
  rodada"): a T1 (pela referência 1) e a T2 (pela referência 2), com as guias ocultas; o G2r ao lado do G2. As folhas
  `arvore-t.png` e `golem-g2r.png`; as limitações no tamanho real no LEIA-ME.
- **Registrado:** o Espantalho Possuído e o Mímico precisam de uma decisão própria antes de qualquer integração por
  família.
- **Processo:** grades à mão medidas nas guias; as fontes pelo Aseprite em lote (o conector sem editor), 0 diferentes na
  releitura, a guia oculta; a exportação igual à grade, @2x exato, 32 e 48 em blocos inteiros; fotos a 1920×945, sem erro
  no console.
- **Verificações proporcionais (nenhum código do jogo mudou):** o pyflakes dos auxiliares, a sintaxe do roteiro das
  fotos e as grades regravadas iguais às gravadas.
- **Continua:** a escolha do Jean; nada integrado; os chefes e o mapa não foram começados.

### 23/10/2026 (data do computador local) — A Árvore Desperta e o Golem de pedra no jogo (1.189.0)

- **Estado conferido:** a branch em `95d135a6`, igual ao remoto, sem alterações locais; produção na 1.188.0.
- **Decisão do Jean:** a Árvore T1 (a transposição da referência 1) e o Golem G2 original aprovados, sem retoques; o
  Espantalho Possuído e o Mímico conservam a aparência de antes nesta entrega.
- **No jogo (1.189.0):** `retrato-arvore-desperta` e `retrato-golem` (16, 32, 48 e os @2x) pelas famílias, com os afixos
  e os líderes. O Espantalho e o Mímico ganham a `origem` do inimigo (marcada no evento, só o retrato lê) e seguem pelos
  traços; a família, os números, o Bestiário, os contratos e o nêmesis deles ficam como antes. O `planta` e o `construto`
  continuam com a Árvore Anciã e o Golem Primordial.
- **As fontes:** cópias byte a byte (a da Árvore com a guia oculta, conferida); exportadas numa pasta temporária e
  iguais byte a byte às propostas antes de gravar; `--conferir`: tudo igual.
- **Conferido com os arquivos de produção** (`criaturas/arvore_golem/capturas-1189/`): a luta, o Bestiário com a faixa do
  mestre caçador, o cartaz e o rastreador; o Espantalho e o Mímico pelos eventos reais, nos sprites de antes. A folha
  `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1189.png`.
- **Gabarito:** uma partida mudou (`mago-42-web`), investigada antes de atualizar: só o campo `"retrato"` de um contrato
  de alvo da família `golem` ("Serorthas"), de `"construto"` para `"golem"`, em 3 linhas (o estado dos contratos e dois
  painéis); com as duas famílias tiradas do mapa, a transcrição volta ao hash antigo. As outras 23 idênticas. Atualizado.
- **Testes:** a árvore e o golem pela família, com os afixos e o líder; os guardiões nos traços; o Espantalho e o Mímico
  pelos eventos reais (com um jogo de mentira), nos traços; um golem comum com o nome "Mímico" continua no golem.
- **Verificações sobre o código final:** `unittest` (661, 1 pulado: a fumaça, rodada à parte), o gabarito (atualizado
  como acima), o pyflakes (só o aviso conhecido) e a fumaça inteira (378 ok, tudo certo).
- **Pendências à parte:** o Espantalho Possuído e o Mímico (um desenho próprio ou ficar nos traços).
- **Falta na frente de criaturas:** os 8 guardiões, o antagonista, o servo do Necromante e as duas pendências; depois, a
  1E.4 (o mapa). Nada começado.

### 23/10/2026 (data do computador local) — Os primeiros chefes: a Árvore Anciã e o Golem Primordial (nada no jogo)

- **Estado conferido:** a branch em `d582eee9`, igual ao remoto, sem alterações locais; produção na 1.189.0.
- **Levantado antes de desenhar (`ferramentas/prototipos/hud/criaturas/chefes_arvore_golem/LEIA-ME.md`):** os números,
  as habilidades, as entradas, as fases e os rumores dos dois guardiões; o retrato de um guardião só aparece na carta da
  luta (pelo id, como o Rei Troll e a Rainha), então os derivados são o 16 e o 32.
- **No protótipo, aguardando o Jean:** a Árvore Anciã AA1 (o rosto-rei) e AA2 (a árvore imensa); o Golem Primordial GP1
  (a parede que se levanta) e GP2 (o ídolo). As folhas `anciaa.png` e `primordial.png`, com a luta de cada guardião ao
  lado do comum correspondente. Minha preferência: a AA1 e o GP2; as limitações no LEIA-ME.
- **Processo:** grades à mão; as fontes pelo Aseprite em lote (o conector sem editor), 0 diferentes na releitura; a
  exportação igual à grade, @2x exato, o 32 em blocos inteiros; fotos a 1920×945, sem erro no console.
- **Verificações proporcionais (nenhum código do jogo mudou):** o pyflakes dos auxiliares, a sintaxe do roteiro das
  fotos e as grades regravadas iguais às gravadas.
- **Continua:** a escolha do Jean; os outros chefes, o antagonista, o servo, o Espantalho, o Mímico e o mapa não foram
  começados.

### 23/10/2026 (data do computador local) — Os dois guardiões pelas referências em close (nada no jogo)

- **Estado conferido:** a branch em `256480d7`, igual ao remoto; as únicas alterações locais eram as duas referências
  deixadas pelo Jean em `ferramentas/arte/referencias/icones/` (guardadas sem alteração; a origem no LEIA-ME de lá).
- **Pedido do Jean:** refazer a Árvore Anciã e o Golem Primordial em close, pelas referências; no meio da rodada, três
  tentativas de copiar cada uma e, depois, mais três a partir da tentativa 2.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/chefes_arvore_golem/LEIA-ME.md`, "A
  segunda rodada"): R1 (pela guia limpa), R2 (por volumes) e R3 (pelas linhas) de cada; R2a, R2b e R2c de cada. As
  folhas `anciaa-r.png`, `primordial-r.png`, `anciaa-r2.png` e `primordial-r2.png`. Minha preferência: a R2b de cada um;
  as limitações no LEIA-ME. A AA1, a AA2, o GP1 e o GP2 ficam como histórico.
- **Processo:** grades à mão medidas nas guias (ocultas nas fontes); as fontes pelo Aseprite em lote (o conector sem
  editor), 0 diferentes na releitura; a exportação igual à grade, @2x exato, o 32 em blocos inteiros; fotos a 1920×945,
  sem erro no console.
- **Verificações proporcionais (nenhum código do jogo mudou):** o pyflakes dos auxiliares, a sintaxe do roteiro das
  fotos e as grades regravadas iguais às gravadas.
- **Continua:** a escolha do Jean; nada integrado; os outros chefes, o antagonista, o servo, o Espantalho, o Mímico e o
  mapa não foram começados.

### 23/10/2026 (data do computador local) — A Árvore Anciã no jogo (1.190.0): a R2b, pelo id da guardiã

- **Estado conferido:** a branch em `2af22748`, igual ao remoto, sem alterações locais (uma worktree de outra sessão,
  `interesting-curran-366911`, não foi tocada); produção na 1.189.0.
- **Decisão do Jean:** a `anciaa-r2b` aprovada, sem retoques (o lote da noite: a Árvore, o Golem R1 refinado, os seis
  chefes restantes e os três especiais; só a Árvore entra no jogo).
- **No jogo (1.190.0):** `retrato-arvore-ancia` (16 e 32, com os @2x; sem 48, que o guardião não usa) pelo id
  `ent_anciao` (`RETRATO_GUARDIAO`). A Árvore Desperta T1 e o Espantalho Possuído como estavam; nenhuma regra mudou.
- **A fonte:** a da R2b, copiada byte a byte (a guia oculta, conferida); exportada numa pasta temporária e igual byte a
  byte à proposta antes de gravar; `--conferir`: tudo igual.
- **Conferido com os arquivos de produção** (`criaturas/chefes_arvore_golem/capturas-1190/`): a guardiã na luta com a
  Árvore Desperta e o lobo; o Espantalho pelo evento real. A folha
  `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1190.png`.
- **Testes:** a Árvore Anciã pelo id, em qualquer nome próprio; a comum e o Espantalho como estavam; o teste dos
  guardiões passa a ler o `RETRATO_GUARDIAO` (o id `ent_anciao` não é o nome do retrato).
- **Verificações sobre o código final:** `unittest` (662, 1 pulado: a fumaça, rodada à parte), o gabarito (idêntico, sem
  atualizar: nenhuma das 24 partidas encontra a Árvore Anciã), o pyflakes (só o aviso conhecido) e a fumaça inteira
  (378 ok, tudo certo).

### 23/10/2026 (data do computador local) — O lote da noite: o Golem R1b, os seis chefes e os três especiais (nada no jogo)

- **Depois da integração da Árvore Anciã (1.190.0, `3ae2613f`)**, em commits separados: o Golem Primordial R1b
  (`a35b469a`) e as 18 propostas do lote.
- **O Golem R1b** (`ferramentas/prototipos/hud/criaturas/chefes_arvore_golem/`, a folha `primordial-r1b.png`): a R1 com a
  laje da sobrancelha mais pesada e as órbitas mais fundas; os pontos de luz e o resto do rosto da R1.
- **Os seis chefes e os três especiais** (`ferramentas/prototipos/hud/criaturas/chefes_e_especiais/LEIA-ME.md`, com o
  que vem do jogo, a interpretação, a preferência e a limitação de cada um): a Hidra (H1, H2), o Dragão de Gelo (D1, D2),
  o Senhor da Guerra (S1, S2), o Profeta das Cinzas (P1, P2), a Bruxa Afogada (B1, B2), o Lich Menor (L1, L2), o
  Espantalho Possuído (E1, E2), o Mímico (M1, M2) e o servo esquelético (SV1, SV2). As folhas dos pares, a dos especiais e
  a prancha geral `candidatos.png`. Todos só na carta da luta: o 16 e o 32.
- **Achado registrado:** o tipo `servo` também é o do inimigo que o talento Rei dos Mortos ergue ("Lobo (servo)"); uma
  integração do retrato do servo precisa decidir se ele vale para os dois.
- **Processo:** grades à mão; as fontes pelo Aseprite em lote (o conector sem editor; a janela aberta não foi tocada), 0
  diferentes na releitura; a exportação igual à grade, @2x exato, o 32 em blocos inteiros; fotos a 1920×945 nos modos
  atual, a e b (os chefes pelo `CHEFE=`, o Espantalho e o Mímico pelos eventos reais, o servo pelo `SERVOS=1`), sem erro
  no console.
- **Verificações proporcionais (nenhum código do jogo mudou depois da 1.190.0):** o pyflakes dos auxiliares, a sintaxe
  dos roteiros das fotos e as grades regravadas iguais às gravadas.
- **Continua:** a avaliação do Jean; nada integrado além da Árvore Anciã; o antagonista e o mapa não foram começados.

### 23/10/2026 (data do computador local) — O Golem Primordial no jogo (1.191.0): a R1b, pelo id do guardião

- **Estado conferido:** a branch em `81238296`, igual ao remoto; as únicas alterações locais eram sete referências novas
  deixadas pelo Jean em `ferramentas/arte/referencias/icones/` (guardadas no commit das transposições).
- **Decisão do Jean:** a `primordial-r1b` aprovada, sem retoques (a única integração desta rodada).
- **No jogo (1.191.0):** `retrato-golem-primordial` (16 e 32, com os @2x) pelo id `golem_primordial`. O golem de pedra
  comum e o Mímico como estavam; nenhuma regra mudou.
- **A fonte:** a da R1b, copiada byte a byte (a guia oculta, conferida); exportada numa pasta temporária e igual byte a
  byte à proposta antes de gravar; `--conferir`: tudo igual.
- **Conferido com os arquivos de produção** (`criaturas/chefes_arvore_golem/capturas-1191/`): o guardião na luta com o
  golem comum e o esqueleto; o Mímico pelo evento real. A folha
  `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1191.png`.
- **Verificações sobre o código final:** `unittest` (663, 1 pulado: a fumaça, rodada à parte), o gabarito (idêntico, sem
  atualizar: nenhuma das 24 partidas encontra o Golem Primordial), o pyflakes (só o aviso conhecido) e a fumaça inteira
  (378 ok, tudo certo).

### 23/10/2026 (data do computador local) — A segunda rodada dos chefes e especiais (nada no jogo) e a Bruxa Afogada suspensa

- **Estado conferido:** a integração do Golem Primordial no `05f06fdb` (1.191.0), no remoto; a produção não mudou depois.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/chefes_e_especiais/LEIA-ME.md`, "A segunda
  rodada"): as transposições pelas sete referências novas (`hidra-t`, `dragao-t`, `senhor-t`, `profeta-t`,
  `espantalho-t`; as referências guardadas sem alteração, a origem e o SHA-256 no LEIA-ME delas), a boca do servo
  (`servo-sv2b`, a referência 7 só na boca e na mandíbula) e os refinamentos locais (`lich-l1b`, `mimico-m1b`). As folhas
  `transposicoes1-hidra-dragao.png`, `transposicoes2-senhor-profeta-espantalho.png` e
  `refinamentos-servo-lich-mimico.png`; as limitações no LEIA-ME.
- **A Bruxa Afogada:** os desenhos suspensos; o levantamento (na campanha, a ficha `bruxa_afogada` é a Ilse) e três
  conceitos de substituição (a minha recomendação, o Barqueiro do Charco) no mesmo LEIA-ME. Nada removido, renomeado ou
  migrado.
- **Verificações proporcionais (nenhum código do jogo mudou):** o pyflakes dos auxiliares, a sintaxe do roteiro das
  fotos, as grades regravadas iguais às gravadas (as 18 da primeira rodada idênticas), 0 diferentes na releitura das
  fontes, a guia oculta conferida, as fotos sem erro no console.
- **Continua:** a escolha do Jean; a decisão da Bruxa Afogada; na integração do servo, separar pela origem o esqueleto
  do Erguer Servo do inimigo que o Rei dos Mortos ergue. O antagonista e o mapa não foram começados.

### 23/10/2026 (data do computador local) — O Mímico no jogo (1.192.0): o M1, pela origem

- **Estado conferido:** a branch em `52c758fd`, igual ao remoto, sem alterações locais (a worktree de outra sessão,
  `interesting-curran-366911`, não foi tocada).
- **Decisão do Jean:** o M1 original aprovado, sem retoques (não o M1b); a M1b e a M2 ficam como alternativas.
- **No jogo (1.192.0):** `retrato-mimico` (16 e 32, com os @2x) pela origem que o evento marca (`RETRATO_ORIGEM` em
  `dados.py`). A família, os números, os contratos e o Bestiário continuam os do golem; o golem de pedra comum continua
  com o dele; nenhuma regra mudou.
- **A fonte:** a do M1 (`743ecfae`), copiada byte a byte; exportada numa pasta temporária e igual byte a byte à proposta
  antes de gravar; `--conferir`: tudo igual.
- **Conferido com os arquivos de produção** (`criaturas/chefes_e_especiais/capturas-1192/`): o Mímico pelo evento real e o
  golem de pedra na luta. A folha `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1192.png`.
- **Testes:** o Mímico pela origem (o nome exibido não decide; a família continua a do golem); os testes do Espantalho e
  do Golem Primordial passam a esperar o retrato do Mímico pela origem.
- **Verificações sobre o código final:** `unittest` (664, 1 pulado: a fumaça, rodada à parte), o gabarito (idêntico, sem
  atualizar), o pyflakes (só o aviso conhecido) e a fumaça inteira (378 ok, tudo certo).

### 23/10/2026 (data do computador local) — O Dragão de Gelo em 32×32 nativos (um teste; nada no jogo) e as decisões da segunda rodada

- **Pedido do Jean:** depois do Mímico (1.192.0, `19d78a77`), um teste controlado: se a grade de 16 é parte do problema
  das transposições, sem virar mudança geral. Uma proposta do Dragão de Gelo desenhada em 32 nativos, só no protótipo.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/dragao_32/LEIA-ME.md`, a folha
  `comparacao.png`): a fonte de 32 à mão (a referência como guia oculta, só para medir), pelo Aseprite em lote
  (`montar_camadas.lua` com `n=32`; 0 diferentes na releitura; a guia oculta conferida), o @2x de 64 exato. Na carta, os
  mesmos 32 px: o `--px` da HUD põe o retrato em 32 px do aparelho a 100% e a 125%.
- **A minha leitura:** ganho de forma e de fidelidade à referência (a cunha, os chifres, a testa, a mandíbula, a crista);
  a expressão só em parte (o olho tem 5 px); o grão mais fino destoa dos vizinhos de 16 ×2, pouco a 1× e muito a 3×; parte
  do miolo é textura que vira granulado.
- **As decisões da segunda rodada** (registradas em `chefes_e_especiais/LEIA-ME.md`): a Hidra e o Senhor da Guerra
  recusados; o Profeta aceito no visual, preservado, sem integrar; o Espantalho em avaliação; o próximo servo sem elmo nem
  armadura; o Lich sem nova aprovação; a Bruxa Afogada sem substituição autorizada. Nada redesenhado.
- **Verificações proporcionais (nenhum código do jogo mudou):** o pyflakes dos auxiliares, a sintaxe do roteiro das
  fotos, a grade regravada igual à gravada, a fonte reaberta (32×32, as camadas na ordem, a guia oculta) e as fotos sem
  erro no console.
- **Parado para a avaliação do teste:** nenhuma criatura nova, nenhuma integração do Dragão, o mapa não começado; a
  PixelLab não foi instalada nem contratada (o Aseprite da máquina já tem uma extensão dela, que não foi usada).

### 23/10/2026 (data do computador local) — O refino leve do Dragão N32 e o teste em 16 (nada no jogo)

- **Estado conferido:** a branch em `cf8d9bfe`, igual ao remoto, sem alterações locais.
- **Decisão do Jean:** o Dragão N32 muito bem recebido; a direção escolhida. Antes da integração, um refino leve numa
  cópia, com o N32 preservado; e, a pedido dele, um teste do mesmo dragão em 16 a partir do 32.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/dragao_32/LEIA-ME.md`, a folha `refino.png`):
  o N32R (a bochecha e o pescoço em planos agrupados, o claro concentrado no alto da testa, o olho mais estreito sob a
  testa; 74 pixels diferentes do N32) e o N16 (redesenhado à mão, com o N32R como mapa). O N32 saiu idêntico (a fonte e o
  PNG, byte a byte).
- **A minha leitura:** o refino é discreto a 1× (menos granulado, o olhar mais severo); o N16 mantém o desenho bem mais que a
  T antiga, mas perde a projeção do focinho e fica mais genérico.
- **Verificações proporcionais (nenhum código do jogo mudou):** o pyflakes dos auxiliares, a sintaxe do roteiro das fotos,
  as grades regravadas iguais às gravadas, as fontes reabertas (o lado, as camadas na ordem, a guia oculta), 0 diferentes
  na releitura, as exportações iguais ao composto, os derivados em blocos inteiros e as fotos sem erro no console.
- **Parado para a avaliação:** nenhuma criatura nova, nenhum retrato aprovado mexido, o Dragão não integrado, o mapa não
  começado.

### 23/10/2026 (data do computador local) — O Dragão de Gelo no jogo (1.193.0): o N16, pelo id do guardião

- **Estado conferido:** a branch em `a9549b5b`, igual ao remoto, sem alterações locais.
- **Decisão do Jean:** o N16 aprovado, sem retoques (o redesenho em 16 a partir do estudo nativo de 32); o N32 e o N32R
  ficam como estudos no protótipo.
- **No jogo (1.193.0):** `retrato-dragao-de-gelo` (16 e 32, com os @2x) pelo id `dragao_de_gelo` (`RETRATO_GUARDIAO`). O
  grifo, a harpia e o sprite `voador` dos outros como estavam; nenhuma regra mudou.
- **A fonte:** a de 16 do N16 (`a9549b5b`), copiada byte a byte; exportada numa pasta temporária e igual byte a byte à
  proposta antes de gravar; `--conferir`: tudo igual.
- **Conferido com os arquivos de produção** (`criaturas/dragao_32/capturas-1193/`): o guardião na luta com o lobo gélido e
  o grifo. A folha `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1193.png`.
- **Testes:** o Dragão pelo id; os testes do grifo e da harpia passam a conferir o voador sem retrato próprio; o teste dos
  guardiões inclui o dragão.
- **Verificações sobre o código final:** `unittest` (665, 1 pulado: a fumaça, rodada à parte), o gabarito (idêntico, sem
  atualizar), o pyflakes (só o aviso conhecido) e a fumaça inteira (378 ok, tudo certo).

### 23/10/2026 (data do computador local) — O Espantalho em 32 nativos, adaptado à mão para 16 (nada no jogo)

- **Estado:** depois da integração do Dragão de Gelo (1.193.0, `247fc4f0`); só protótipo.
- **Pedido do Jean:** o caminho do Dragão para o Espantalho: a construção nativa de 32 pela referência (o espantalho
  diabólico guardado no projeto) e a adaptação à mão para 16, com o 32 como mapa. A T era uma base conceitual, não arte
  aprovada; ela e as versões anteriores ficam.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/espantalho_32/LEIA-ME.md`, a folha
  `comparacao.png`): o `espantalho-n32` (o chapéu velho com a ponta caída e a aba despencando à direita, a cabeça de estopa
  inclinada, as brasas sob as dobras, a boca costurada torta, a palha em leque) e o `espantalho-n16`. Fontes separadas para
  os dois, em camadas, com as guias ocultas.
- **A minha leitura:** o N16 preservou o chapéu, a estopa contra a sombra da aba, as brasas nas órbitas, a boca costurada e
  a palha; perdeu a inclinação da cabeça, o torto forte da boca e as dobras do saco. A primeira passada em 16 tinha
  perdido a expressão (os olhos em quadrados laranja); foi corrigida na distribuição das formas.
- **O processo** fica registrado como alternativa promissora para retratos difíceis, não como obrigação (o LEIA-ME das
  criaturas e o plano 23). Na integração futura, o Espantalho terá um papel próprio pela origem já existente, com o
  retrato da Árvore Desperta e as regras compartilhadas intactos.
- **Verificações proporcionais (nenhum código do jogo mudou):** o pyflakes dos auxiliares, a sintaxe do roteiro das fotos,
  as grades regravadas iguais às gravadas, as fontes reabertas (o lado, as camadas na ordem, a guia oculta), 0 diferentes
  na releitura, as exportações iguais ao composto, os derivados em blocos inteiros e as fotos sem erro no console.
- **Parado para a avaliação do Espantalho:** nada integrado, nenhuma criatura nova, o mapa não começado.

### 23/10/2026 (data do computador local) — O refino do Espantalho: N32R e N16R (nada no jogo)

- **Estado conferido:** a branch em `6796be1c`, igual ao remoto, sem alterações locais (retomada noutra conta).
- **Pedido do Jean:** o N16 perdeu a expressão (a cabeça frontal e retangular, os olhos como pontos acesos, a boca sem a
  costura, a palha numa faixa); refinar em cópias, com a referência guardada como autoridade de forma e expressão. Durante
  o trabalho, o Jean sugeriu puxar a arte para cima (o rosto maior, parte do chapéu fora) e dispensou a aba caída (o
  chapéu pode ser mais reto).
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/espantalho_32/LEIA-ME.md`, a folha
  `refino.png`): o `espantalho-n32r` (o estudo de 32 no quadro novo) e o `espantalho-n16r` (redesenhado à mão com ele como
  mapa). A T, o N32 e o N16 intactos.
- **A minha leitura:** o rosto afunilado, a testa e as órbitas oblíquas, a costura torta e os dois tufos de palha
  sobreviveram ao 16; os pontos da costura e parte da inclinação se perderam, e as brasas ainda são o ponto mais forte a
  3×.
- **Verificações proporcionais (nenhum código do jogo mudou):** o pyflakes dos auxiliares, as grades e as listas antigas
  regravadas iguais, as fontes novas reabertas (o lado, as camadas na ordem, a guia oculta), 0 diferentes na releitura, as
  exportações iguais ao composto (as antigas reexportadas byte a byte iguais), os derivados em blocos inteiros e as fotos
  sem erro no console. O conector do Aseprite estava sem editor; as fontes saíram pelo Aseprite em lote, sem tocar na
  janela aberta.

### 23/10/2026 (data do computador local) — O Senhor da Guerra em 32 nativos, adaptado à mão para 16 (nada no jogo)

- **Estado:** depois do refino do Espantalho (`93c6c2b1`); só protótipo.
- **Pedido do Jean:** o caminho do Dragão e do Espantalho para o Senhor da Guerra (a S2 deu a direção; a T foi recusada
  por não ter um rosto compreensível): o estudo de 32 pela referência guardada (`Senhor da guerra caolho-3.png`), com a
  cabeça dominando o quadro, e a adaptação à mão para 16 com olho, venda, nariz, boca e barba legíveis.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/senhor_32/LEIA-ME.md`, a folha
  `comparacao.png`): o `senhor-n32` e o `senhor-n16`. A S2 e a T ficam como estão.
- **Durante o trabalho:** a primeira construção lia, nas palavras do Jean, como "um bebê de barba e tapa-olho"; a correção
  veio da anatomia de adulto (o alto da cabeça fora do quadro, rugas, a sobrancelha pesada sobre o olho fundo, o nariz
  largo, a pele curtida, a barba em tufos). O machado, com 4–5 px na borda, saiu; fica o manto de pele.
- **A minha leitura:** a venda com a tira, a cicatriz, o olho semicerrado, o nariz, a boca e a barba sobreviveram ao 16; as
  rugas, a maçã do rosto e os sulcos se perderam, e a venda é a mancha mais forte do rosto.
- **Verificações proporcionais (nenhum código do jogo mudou):** o pyflakes dos auxiliares, a sintaxe do roteiro das fotos,
  as fontes reabertas (o lado, as camadas na ordem, a guia oculta), 0 diferentes na releitura, as exportações iguais ao
  composto, os derivados em blocos inteiros e as fotos sem erro no console. As fontes pelo Aseprite em lote (o conector
  sem editor; a janela aberta do Jean não foi tocada).
- **Parado para a avaliação dos dois:** nada integrado, a Bruxa Afogada intocada, nenhuma criatura nova, o mapa não
  começado.

### 23/10/2026 (data do computador local) — O Senhor da Guerra no jogo (1.194.0): o N16, pelo id do guardião

- **Estado conferido:** a branch em `f105fd10`, igual ao remoto; a única alteração local era um
  `ferramentas/arte/referencias/icones/caido-avatar-512.png` que não é desta sessão, preservado e fora do commit.
- **Decisão do Jean:** o N16 aprovado, sem retoques; o N32 e as propostas anteriores ficam como estudos.
- **No jogo (1.194.0):** `retrato-senhor-da-guerra` (16 e 32, com os @2x) pelo id `senhor_da_guerra`
  (`RETRATO_GUARDIAO`). O mercenário, o bandido e os outros humanos como estavam; o Profeta das Cinzas e o antagonista no
  `humano`; nenhuma regra mudou.
- **A fonte:** a de 16 do N16 (`f105fd10`), copiada byte a byte; a exportação igual byte a byte à proposta; `--conferir`:
  tudo igual.
- **Conferido com os arquivos de produção** (`criaturas/senhor_32/capturas-1194/`): o guardião na luta com o Mercenário e
  o Bandido. A folha `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1194.png`.
- **Testes:** o Senhor pelo id (e o mercenário, o bandido, o Profeta e o humano genérico como estavam); os testes que
  esperavam o Senhor no `humano` passam a esperar o retrato dele; o teste dos guardiões inclui o Senhor.
- **Verificações sobre o código final:** `unittest` (666, 1 pulado: a fumaça, rodada à parte), o gabarito (idêntico, sem
  atualizar), o pyflakes (só o aviso conhecido) e a fumaça inteira (378 ok, tudo certo).

### 23/10/2026 (data do computador local) — A passagem no rosto do Espantalho: N16R2 (nada no jogo)

- **Estado:** depois da integração do Senhor da Guerra (1.194.0, `d750988a`); só protótipo.
- **Pedido do Jean:** no N16R, o chapéu, o enquadramento, a palha e o corpo funcionam; o rosto não (os olhos pareciam
  desalinhados por acidente, as brasas eram pontos numa máscara lisa, a sombra das órbitas e a costura perderam a malícia
  do N32R). Uma cópia, só no rosto, com o N32R como referência.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/espantalho_32/LEIA-ME.md`, a folha
  `ajuste.png`): o `espantalho-n16r2`, só as linhas 7 a 10 mudadas: os olhos na mesma linha (a inclinação fica na aba), as
  sobrancelhas se encontrando sobre o nariz, as brasas dentro de fendas (a do lado da sombra mais apagada), a sombra
  marrom embaixo, as bochechas com volume e o canto da costura subindo. O N16R intacto.
- **A minha leitura:** os olhos leem como intencionais e a ameaça voltou pela carranca; os pontos da costura não cabem no
  16, e a brasa do lado aceso ainda é o pixel mais forte a 3×.
- **Verificações proporcionais (nenhum código do jogo mudou):** o pyflakes dos auxiliares, a sintaxe do roteiro das fotos,
  as grades e as listas antigas regravadas iguais, a fonte nova reaberta (o lado, as camadas na ordem, a guia oculta), 0
  diferentes na releitura, a exportação igual ao composto (o N16R reexportado igual), os derivados em blocos inteiros e a
  foto sem erro no console, com a mesma caixa da carta. As fontes pelo Aseprite em lote.
- **Parado para a avaliação do Espantalho:** nada integrado, nenhuma criatura nova, o mapa não começado.

### 23/10/2026 (data do computador local) — O Espantalho Possuído no jogo (1.195.0): o N16R2, pela origem

- **Estado conferido:** a branch em `bdef5a8a`, igual ao remoto; a única alteração local era o
  `ferramentas/arte/referencias/icones/caido-avatar-512.png` que não é desta sessão, preservado e fora do commit.
- **Decisão do Jean:** o N16R2 aprovado, sem retoques; as outras versões ficam como estudos.
- **No jogo (1.195.0):** `retrato-espantalho` (16 e 32, com os @2x) pela origem `espantalho` (`RETRATO_ORIGEM`), como o
  Mímico; a família, os números e as regras continuam os da árvore desperta, e a árvore desperta comum continua com o
  retrato dela.
- **A fonte:** a de 16 do N16R2 (`bdef5a8a`), copiada byte a byte; a exportação igual byte a byte à proposta;
  `--conferir`: tudo igual.
- **Conferido com os arquivos de produção** (`criaturas/espantalho_32/capturas-1195/`): o Espantalho pelo evento real e a
  árvore desperta comum na luta. A folha `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1195.png`.
- **Testes:** o Espantalho pela origem (perto e longe da Fenda, o mesmo retrato); os que esperavam o Espantalho nos traços
  passam a esperar o retrato dele; uma origem sem retrato continua nos traços.
- **Verificações sobre o código final:** `unittest` (667, 1 pulado: a fumaça, rodada à parte), o gabarito (idêntico, sem
  atualizar), o pyflakes (só o aviso conhecido) e a fumaça inteira (378 ok, tudo certo).

### 23/10/2026 (data do computador local) — A Hidra do Brejo em 32 nativos, adaptada à mão para 16 (nada no jogo)

- **Estado:** depois da integração do Espantalho (1.195.0, `bf5fb2e2`); só protótipo.
- **Pedido do Jean:** uma construção nova (as anteriores pareciam fantoches): as três cabeças de réptil olhando para a
  esquerda (a orientação corrigida por ele; a referência guardada dá o material, a anatomia e a expressão), fortes, com
  pescoços grossos; primeiro em 32, depois à mão em 16.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/hidra_32/LEIA-ME.md`, a folha
  `comparacao.png`): o `hidra-n32` e o `hidra-n16`. A H1, a H2 e a `hidra-t` ficam.
- **A minha leitura:** o N32 lê como três cabeças de réptil com pescoços grossos, a principal dominante; o N16 guarda as
  três cabeças, os olhos, a boca da principal e os pescoços, mas as de trás perdem o focinho longo e a principal perde a
  crista e a mandíbula; a 1× é uma massa verde com três olhos.
- **Verificações proporcionais (nenhum código do jogo mudou):** o pyflakes dos auxiliares, a sintaxe do roteiro das fotos,
  as fontes reabertas (o lado, as camadas na ordem, a guia oculta), 0 diferentes na releitura, as exportações iguais ao
  composto, alfa 0/255, os derivados em blocos inteiros e as fotos sem erro no console. As fontes pelo Aseprite em lote.

### 23/10/2026 (data do computador local) — O servo esquelético em 32 nativos, adaptado à mão para 16 (nada no jogo)

- **Estado:** depois da Hidra (`8b94eecb`); só protótipo.
- **Pedido do Jean:** um desenho próprio para o servo, sem elmo, capuz ou armadura (não o Esqueleto inimigo com os olhos
  recoloridos), primeiro em 32, depois à mão em 16; e conferir a distinção entre o servo do Erguer Servo e as criaturas
  que o Rei dos Mortos ergue, documentando a seleção, sem mudar regras nem integrar mapeamentos.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/servo_32/LEIA-ME.md`, a folha
  `comparacao.png`): o `servo-n32` e o `servo-n16`. A SV1, a SV2 e a SV2b ficam; o Esqueleto E2 continua reservado.
- **A distinção, conferida no código:** os dois são aliados do tipo `"servo"` e hoje caem no sprite `caveira`; o erguido
  não guarda a espécie. A integração vai precisar de uma origem própria para o Erguer Servo e de o Rei dos Mortos passar o
  retrato da criatura que caiu (o LEIA-ME do servo detalha). Demonstrado só no protótipo, numa luta com os dois servos.
- **A minha leitura:** o N32 lê como um crânio nu de servo, separado do inimigo de elmo; o N16 guarda o crânio, o violeta
  escuro, os dentes e as clavículas, e perde as costelas, a inclinação das órbitas e a forma da mandíbula.
- **Verificações proporcionais (nenhum código do jogo mudou):** o pyflakes dos auxiliares, a sintaxe do roteiro das fotos,
  as fontes reabertas (o lado, as camadas na ordem, a guia oculta), 0 diferentes na releitura, as exportações iguais ao
  composto, alfa 0/255, os derivados em blocos inteiros e as fotos sem erro no console. As fontes pelo Aseprite em lote.
- **Parado para a avaliação da Hidra e do servo:** só o Espantalho entrou no jogo (1.195.0); nenhuma criatura nova, a
  substituição da Bruxa Afogada e o mapa não começados.

### 23/10/2026 (data do computador local) — A Hidra: a segunda construção de 32, N32B (nada no jogo)

- **Estado conferido:** a branch em `84b42070`, igual ao remoto; o `caido-avatar-512.png` que não é desta sessão continua
  fora dos commits.
- **Decisão do Jean:** a Hidra e o servo não aprovados. Na Hidra, as cabeças ainda parecem barras horizontais já no 32;
  refazer só a construção de 32, numa cópia, sem adaptar para 16.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/hidra_32/LEIA-ME.md`, a folha
  `construcao-32.png`): o `hidra-n32b`, as três cabeças em cunha (o crânio chato atrás, o calombo da testa sobre o olho, o
  focinho projetado, a boca aberta em cunha com o canto descendo, a mandíbula baixa), as duas de trás menores e mais
  escuras, separadas por sobreposição e contorno, e os pescoços grossos. O N32 e o N16 intactos.
- **Verificações proporcionais:** o pyflakes dos auxiliares, a sintaxe do roteiro das fotos, a grade igual ao rascunho, a
  fonte reaberta (o lado, as camadas na ordem, a guia oculta), 0 diferentes na releitura, a exportação igual ao composto,
  o @2x em blocos inteiros, as anteriores reexportadas iguais e a foto sem erro no console.

### 23/10/2026 (data do computador local) — O servo: o ajuste local do N16, N16B (nada no jogo)

- **Estado:** depois da segunda construção de 32 da Hidra (`83cd006c`); só protótipo.
- **Decisão do Jean:** o servo não aprovado; o crânio descoberto e a distinção do inimigo funcionam. Ajustar só os dentes,
  a mordida e a mandíbula e recuperar a inclinação das órbitas do N32, numa cópia do N16.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/servo_32/LEIA-ME.md`, a folha `ajuste.png`):
  o `servo-n16b`, só as linhas das órbitas e da boca mudadas: os dentes em dois grupos sobre uma mordida escura contínua,
  os de baixo em grupo, as órbitas descendo para o nariz. O N16 e o N32 intactos.
- **Verificações proporcionais:** o pyflakes dos auxiliares, a sintaxe do roteiro das fotos, a fonte reaberta (o lado, as
  camadas na ordem, a guia oculta), 0 diferentes na releitura, a exportação igual ao composto, os derivados em blocos
  inteiros, as anteriores reexportadas iguais e a foto sem erro no console, na mesma caixa da carta.
- **Parado para a avaliação da Hidra (N32B) e do servo (N16B):** nada integrado, a Hidra sem nova adaptação para 16,
  nenhum outro personagem, o mapa não começado.

### 23/10/2026 (data do computador local) — A Hidra: a correção da cabeça principal, N32C (nada no jogo)

- **Estado conferido:** a branch em `3dfa9293`, igual ao remoto; o `caido-avatar-512.png` continua fora dos commits.
- **Pedido do Jean:** no N32B, a cabeça maior tinha a testa em rampa até o nariz, uma bochecha grande, um perfil de
  cachorro ou dinossauro de desenho e uma boca que sugeria sorriso; corrigir só ela, numa cópia, em 32, pela referência.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/hidra_32/LEIA-ME.md`, a folha
  `cabeca-principal.png`): o `hidra-n32c`, a cabeça principal reconstruída (o focinho horizontal, o degrau até a testa, a
  sobrancelha pesada sobre o olho, a bochecha pequena, a mandíbula à parte e a boca aberta em ângulo, com o fundo escuro).
  As cabeças de trás, a composição e a paleta como no N32B; o N32, o N16 e o N32B intactos.
- **Verificações proporcionais:** o pyflakes dos auxiliares, a sintaxe do roteiro das fotos, a grade igual ao rascunho, a
  fonte reaberta (o lado, as camadas na ordem, a guia oculta), 0 diferentes na releitura, a exportação igual ao composto,
  o @2x em blocos inteiros, o N32B reexportado igual e a foto sem erro no console, na mesma caixa da carta.
- **Parado para a avaliação:** o servo N16B segue em avaliação, sem mudança; nada integrado, sem adaptação para 16,
  nenhum outro personagem.

### 23/10/2026 (data do computador local) — A Hidra reconstruída pela nova referência: N32D (nada no jogo)

- **Estado conferido:** a branch em `e72dbcc5`, igual ao remoto; a nova referência deixada pelo Jean
  (`Hidra tríplice do pântano em pixel art.png`) registrada com a origem e o SHA-256; o `caido-avatar-512.png` continua
  fora dos commits.
- **Pedido do Jean:** uma construção nova em 32 pela nova referência (a composição, o crânio arredondado, a sobrancelha,
  o focinho, a mandíbula ligada ao pescoço e a separação das cabeças), preservando o N32C e as anteriores; sem 16.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/hidra_32/LEIA-ME.md`, a folha
  `reconstrucao.png`): o `hidra-n32d`, com a paleta oliva da referência e os dentes simplificados.
- **A minha leitura:** segue a referência na composição e na anatomia da principal, e as de trás leem como cabeças; a
  oliva escura contrasta menos com a carta a 1× que o N32C.
- **Verificações proporcionais:** o pyflakes dos auxiliares, a sintaxe do roteiro das fotos, a grade igual ao rascunho, as
  grades e as listas anteriores regravadas iguais, a fonte reaberta (o lado, as camadas na ordem, a guia oculta), 0
  diferentes na releitura, a exportação igual ao composto, o @2x em blocos inteiros e a foto sem erro no console.
- **Parado para a avaliação do 32:** sem adaptação para 16; o servo N16B e a produção intactos; nada integrado.

### 23/10/2026 (data do computador local) — O servo esquelético no jogo (1.196.0): o N16B, com a distinção dos servos

- **Estado conferido:** a branch em `a7503ed9`, igual ao remoto; o `caido-avatar-512.png` continua fora dos commits.
- **Decisão do Jean:** o N16B aprovado, sem retoques; o Esqueleto (Invocado) do Erguer Servo com o crânio nu, a criatura
  erguida pelo Rei dos Mortos com o retrato da criatura que morreu, por identificação persistente (não pelo nome).
- **No jogo (1.196.0):** `retrato-servo-esqueletico` (16 e 32, com os @2x). `Aliado.retrato`, dado por quem invoca: o Erguer
  Servo dá `servo_esqueletico`; o Rei dos Mortos, o retrato da criatura que caiu. A ficha da carta repassa, a tela desenha.
  O tipo, as regras, os atributos e o comportamento como antes; os aliados não são salvos (só existem na luta).
- **A fonte:** a de 16 do N16B (`3dfa9293`), copiada byte a byte; a exportação igual byte a byte à proposta;
  `--conferir`: tudo igual.
- **Conferido no jogo com os arquivos de produção** (`criaturas/servo_32/capturas-1196/`): o Esqueleto (Invocado), o Lobo
  (servo) e o esqueleto inimigo na mesma luta, cada um com o seu retrato. A folha
  `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1196.png`.
- **Testes:** `tests/test_servos.py` (os dois caminhos reais, o nome que não decide, o aliado sem retrato e a tela).
- **Verificações sobre o código final:** `unittest` (671, 1 pulado: a fumaça, rodada à parte), o gabarito (idêntico, sem
  atualizar), o pyflakes (só o aviso conhecido) e a fumaça inteira, uma vez (378 ok, tudo certo). Durante a fumaça, só uma
  quebra de linha mudou em `estado.py` (o teste que confere o texto da ficha repassando a origem); o comportamento é o
  mesmo, e a suíte e o gabarito rodaram depois dela.

### 23/10/2026 (data do computador local) — A Hidra: a adaptação do N32D para 16, N16D (candidata em avaliação)

- **Estado:** depois da integração do servo (1.196.0, `a1b731c2`); só protótipo.
- **Decisão do Jean:** o N32D aprovado como base da adaptação e preservado; uma fonte nova em 16, à mão, pelo processo do
  Dragão.
- **No protótipo, candidata em avaliação** (`ferramentas/prototipos/hud/criaturas/hidra_32/LEIA-ME.md`, a folha
  `adaptacao-16.png`): o `hidra-n16d`, com as três cabeças para a esquerda, a principal maior e à frente (o focinho, a
  sobrancelha, a boca e a mandíbula) e os pescoços contínuos; os dentes simplificados e o alto das de trás aceso.
- **A minha leitura:** preserva as três cabeças e a principal; perde o crânio arredondado, e a cabeça da direita é a que
  menos se destaca do fundo da carta.
- **Verificações proporcionais (nenhum código do jogo mudou):** o pyflakes dos auxiliares, a sintaxe do roteiro das fotos,
  a grade igual ao rascunho, a fonte reaberta (o lado, as camadas na ordem, a guia oculta), 0 diferentes na releitura, a
  exportação igual ao composto, os derivados em blocos inteiros, o N32D reexportado igual e a foto sem erro no console.
- **Parado para a avaliação:** nada integrado além do servo; nenhuma criatura nova, o mapa não começado.

### 23/10/2026 (data do computador local) — A Hidra: o ajuste da presa de cima, N16D2 (em avaliação)

- **Estado conferido:** a branch em `158699f4`, igual ao remoto; o `caido-avatar-512.png` continua fora dos commits.
- **Pedido do Jean:** o N16D agradou; recuar a presa de cima da principal, que fazia uma barra branca na ponta do focinho,
  numa cópia.
- **No protótipo, em avaliação** (`ferramentas/prototipos/hud/criaturas/hidra_32/LEIA-ME.md`, a folha `presa.png`): o
  `hidra-n16d2`, só as linhas 10 e 11 mudadas (a presa com um pixel, uma coluna para dentro, sob o maxilar, com o escuro
  da boca até a ponta). O N16D intacto; o servo integrado como estava.
- **Verificações proporcionais:** o pyflakes dos auxiliares, a sintaxe do roteiro das fotos, a fonte reaberta (o lado, as
  camadas na ordem, a guia oculta), 0 diferentes na releitura, a exportação igual ao composto, os derivados em blocos
  inteiros, o N16D reexportado igual e a foto sem erro no console.

### 23/10/2026 (data do computador local) — A Hidra do Brejo no jogo (1.197.0): o N16D2, pelo id da guardiã

- **Estado conferido:** a branch em `dc4d9b21`, igual ao remoto; o `caido-avatar-512.png` continua fora dos commits.
- **Decisão do Jean:** o N16D2 aprovado, sem retoques; as outras versões ficam como estudos.
- **No jogo (1.197.0):** `retrato-hidra-do-brejo` (16 e 32, com os @2x) pelo id `hidra_do_brejo` (`RETRATO_GUARDIAO`). O
  sapo, a sanguessuga e as outras feras como estavam; nenhuma regra mudou.
- **A fonte:** a de 16 do N16D2 (`dc4d9b21`), copiada byte a byte, com a guia oculta; a exportação numa pasta temporária
  igual byte a byte à proposta antes da cópia; depois, `--conferir`: tudo igual.
- **Conferido com os arquivos de produção** (`criaturas/hidra_32/capturas-1197/`): a guardiã na luta com o Sapo-touro e a
  Sanguessuga. A folha `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1197.png`.
- **Testes:** a Hidra pelo id (o sapo e a fera genérica como estavam); os que esperavam a Hidra no `fera` passam a esperar o
  retrato dela; o teste dos guardiões inclui a Hidra.
- **Verificações sobre o código final:** `unittest` (672, 1 pulado: a fumaça, rodada à parte), o gabarito (idêntico, sem
  atualizar), o pyflakes (só o aviso conhecido) e a fumaça inteira, uma vez (378 ok, tudo certo).
- **O que falta na frente de criaturas** (a lista na mensagem desta entrega): sem propostas em avaliação; as decisões de
  identidade (a Bruxa Afogada do covil, o antagonista, a família `esqueleto_servo` sem uso no código); e os desenhos não
  começados (o Profeta das Cinzas, com o visual aceito e não integrado, o Lich Menor sem nova aprovação, a Bruxa Afogada
  e o antagonista). O mapa (1E.4) não começado.

### 23/10/2026 (data do computador local) — O Profeta das Cinzas no jogo (1.198.0): a profeta-t, pelo id do guardião

- **Estado conferido:** a branch em `ed52f453`, igual ao remoto; o `caido-avatar-512.png` continua fora dos commits.
- **Decisão do Jean:** a `profeta-t` (o visual aceito, guardado aguardando integração) integrada sem retoques.
- **No jogo (1.198.0):** `retrato-profeta-das-cinzas` (16 e 32, com os @2x) pelo id `profeta_das_cinzas`
  (`RETRATO_GUARDIAO`). Os cultistas que ele invoca e o antagonista como estavam; nenhuma regra mudou.
- **A fonte:** a de 16 da `profeta-t` (`6820bd3e`), copiada byte a byte, em camadas, com a guia oculta; a exportação numa
  pasta temporária igual byte a byte à proposta antes da cópia; depois, `--conferir`: tudo igual.
- **Conferido com os arquivos de produção** (`criaturas/chefes_e_especiais/capturas-1198/`): o Profeta com um Cultista e
  um Bandido. A folha `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1198.png`.
- **Testes:** o Profeta pelo id; as duas asserções que usavam o Profeta como "humano sem retrato" passam a usar um guardião
  humano sem id; o teste dos guardiões inclui o Profeta.
- **Verificações sobre o código final:** `unittest` (673, 1 pulado: a fumaça, rodada à parte), o gabarito (idêntico, sem
  atualizar), o pyflakes (só o aviso conhecido) e a fumaça inteira, uma vez (378 ok, tudo certo).
- **A classificação das pendências, corrigida:** o Profeta tinha o visual aceito aguardando integração (não um desenho
  por começar), agora integrado; o Lich Menor tem propostas (L1, L1b, L2) aguardando decisão; a Bruxa Afogada e o
  antagonista continuam pendentes de identidade; a família `esqueleto_servo` (no catálogo, sem uso no código) fica como
  pendência técnica, sem remover nem criar conteúdo para ela; o Esqueleto E2 e o Bandido do chapéu continuam reservados.

### 23/10/2026 (data do computador local) — O Lich Menor: a comparação da L1, da L1b e da L2 para a decisão

- **Estado:** depois da integração do Profeta (1.198.0, `39a656e4`); só protótipo, nada redesenhado.
- **Pedido do Jean:** a L1 agradou como base; rever o que a L1b mudou e escolher a final, com a L2, ao lado do Esqueleto
  inimigo e do servo aliado.
- **A folha** `ferramentas/prototipos/hud/criaturas/chefes_e_especiais/lich-decisao.png`: as três na mesma luta, a
  1920×945, com os mesmos dados; a carta a 2×; a fileira; o diagnóstico a 12× e as 11 diferenças da L1b sobre a L1 (a
  boca, a mandíbula e o oco das maçãs). As fontes: `fontes/lich-l1`, `fontes/lich-l1b` e `fontes/lich-l2` (a L1 e a L2 de
  `743ecfae`; a L1b de `6820bd3e`).
- **Aguardando o Jean:** a escolha entre a L1, a L1b e a L2. Nenhuma outra criatura e o mapa não começados.

### 23/10/2026 (data do computador local) — O Lich Menor em 32 nativos, adaptado à mão para 16 (nada no jogo)

- **Estado conferido:** a branch em `2188d001`, igual ao remoto; o `caido-avatar-512.png` continua fora dos commits.
- **Pedido do Jean:** o Lich pelo caminho do Dragão, com a L1b como base de identidade (a coroa antiga, o crânio exposto,
  os olhos verdes e o manto violeta): primeiro em 32 nativos, resolvendo o crânio (na L1b, uma placa), as órbitas, o nariz,
  a boca, a coroa e o manto; depois à mão em 16. Sem livro nem acessórios.
- **No protótipo, aguardando o Jean** (`ferramentas/prototipos/hud/criaturas/lich_32/LEIA-ME.md`, a folha
  `comparacao.png`): o `lich-n32` e o `lich-n16`, com fontes separadas. A L1, a L1b e a L2 intactas.
- **A minha leitura:** o N32 lê como um rei-morto severo em close, distinto do servo e do Esqueleto; o N16 guarda a coroa,
  o crânio afunilado, o olhar contido e o manto, e perde as têmporas, o oco das maçãs e o halo das órbitas.
- **Verificações proporcionais (nenhum código do jogo mudou):** o pyflakes dos auxiliares, a sintaxe do roteiro das fotos,
  as grades iguais ao rascunho, as fontes reabertas (o lado, as camadas na ordem), 0 diferentes na releitura, as
  exportações iguais ao composto, alfa 0/255, os derivados em blocos inteiros e as fotos sem erro no console.
- **Parado para a avaliação das duas versões:** nada integrado, nenhuma outra criatura, o mapa não começado.

### 23/10/2026 (data do computador local) — O Lich Menor no jogo (1.199.0): o N16, pelo id do guardião, nas duas fases

- **Estado conferido:** a branch em `fcb20bfd`, igual ao remoto; o `caido-avatar-512.png` continua fora dos commits.
- **Decisão do Jean:** o N16 aprovado, sem retoques; o N32 como estudo.
- **No jogo (1.199.0):** `retrato-lich-menor` (16 e 32, com os @2x) pelo id `lich_menor` (`RETRATO_GUARDIAO`). Na fase 2 o
  Lich ganha o traço etéreo e o retrato continua o dele (o id vem antes dos traços); os esqueletos que ele invoca, com o
  da família. Nenhuma regra mudou.
- **A fonte:** a de 16 do N16 (`fcb20bfd`), copiada byte a byte; a exportação numa pasta temporária igual byte a byte à
  proposta antes da cópia; depois, `--conferir`: tudo igual.
- **Conferido com os arquivos de produção** (`criaturas/lich_32/capturas-1199/`): as duas fases, com o Esqueleto, o
  esqueleto invocado e o servo. A folha `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1199.png`.
- **Testes:** o Lich pelo id nas duas fases (pelo `checar_fase` de verdade) e os invocados pela família; as asserções que
  esperavam o Lich no `etereo` e na `caveira` passam a esperar o retrato dele, e o guardião sem id continua no traço.
- **Verificações sobre o código final:** `unittest` (674, 1 pulado: a fumaça, rodada à parte), o gabarito (idêntico, sem
  atualizar), o pyflakes (só o aviso conhecido) e a fumaça inteira, uma vez (378 ok, tudo certo).
- **As próximas decisões (do Jean, antes de qualquer desenho):** a identidade do substituto da Bruxa Afogada nos covis
  (hoje o id `bruxa_afogada` do covil do pântano é a Ilse) e a do antagonista do mundo gerado. Pendência técnica, sem
  mudança: a família `esqueleto_servo`, sem uso. Reservados: o Esqueleto E2 e o Bandido do chapéu.

### 23/10/2026 (data do computador local) — As identidades pendentes, em texto: o Barqueiro, o antagonista e o `esqueleto_servo`

- **Estado conferido:** a branch em `8d9a8bec` (1.199.0), igual ao remoto; o `caido-avatar-512.png` continua fora dos
  commits.
- **Pedido do Jean:** só investigação e propostas em texto, antes de qualquer desenho. O registro:
  `ferramentas/prototipos/hud/criaturas/identidades/LEIA-ME.md`.
- **O Barqueiro do Charco** (o substituto proposto da Bruxa Afogada nos covis): o barqueiro que afundou e continua
  atravessando os afogados; velho, encharcado, o pano de rede até o nariz, os olhos claros à mostra, a lanterna verde
  iluminando de baixo. As regras da ficha inteiras; mudam a `base`, o `g`, a `intro`, o texto da fase, o rumor e o
  retrato. **A separação da Ilse:** a ficha nova na mesma posição da lista (o sorteio não muda), a Ilse num catálogo de
  únicos (atenção ao `idx=1` do `spec` dela), o texto da fase dela preservado, a migração v6→v7 dos covis e dos rumores, os
  testes da Ilse intactos.
- **O antagonista:** só no mundo gerado; título (8, 3 femininos), nome e origem (5) sorteados à parte; o canon visual é
  pouco (foi humano, deixou de ser; o trono de pedra rachada; a forma imensa no fim). Três direções: A, o humano que a
  Fenda está apagando (recomendada); B, o rasgo; C, o soberano de pedra. Um retrato por título contradiria os outros sete;
  o único tem de ser neutro de título e de gênero. **Achado independente:** o gênero do texto não acompanha o título
  (o lore da taverna, o `eco_do_vazio`, duas origens).
- **A família `esqueleto_servo`:** no catálogo desde o primeiro commit, nunca criada (o Erguer Servo sempre usou o aliado
  com números próprios); fora dos saves e dos sorteios. Recomendação: remover numa correção, ajustando o
  `test_retratos`.
- **Verificações:** só documentos; nenhum código, save, arte ou mapa mudou.
- **As decisões abertas (do Jean):** o Barqueiro e a separação com migração; a direção do antagonista; a remoção do
  `esqueleto_servo`; os textos de gênero do antagonista. Reservados: o Esqueleto E2 e o Bandido do chapéu.

### 23/10/2026 (data do computador local) — As decisões das identidades: três correções no jogo, o Barqueiro preparado à parte, dois estudos em 32

- **Estado conferido:** a branch em `ec2d12b2`, igual ao remoto; o `caido-avatar-512.png` continua fora dos commits.
- **No jogo:**
  - **1.199.1:** a família `esqueleto_servo` removida (nenhum uso real: o servo do Necromante é um aliado sem família, e
    o Rei dos Mortos não a usa); o gabarito idêntico.
  - **1.199.2:** o antagonista no gênero do título sorteado: as origens nas duas formas (o mesmo sorteio, as mesmas
    chamadas ao `rng`), e o eco do Vazio, a história da taverna e a fala do veterano concordando só no que se refere a
    ele. `tests/test_antagonista.py` confere os 8 títulos com as 5 origens. **O gabarito mudou de propósito:** 12 partidas,
    só nas palavras ("uma heroína", "nascida", "ela"), conferido linha a linha. Saves antigos ficam com o texto que
    gravaram.
  - **1.199.3:** a Ilse com a ficha dela (`dados.GUARDIOES_UNICOS`, id `ilse`), sem o `idx=1`, fora do sorteio; as regras,
    o texto da fase, o rito e o retrato iguais; o covil não mudou; o gabarito idêntico.
- **Preparado fora da produção:** a branch `claude/barqueiro-do-charco` (1.200.0 lá, `2311a9ef`): a ficha
  `barqueiro_do_charco` na posição da Bruxa, com as mesmas regras e os textos novos; o save formato 7 (os covis com a
  Bruxa, pelo id ou pela posição, e os rumores passam ao Barqueiro com o mesmo nome próprio; o progresso fica; refazer não
  muda nada; a campanha carrega igual). `tests/test_barqueiro.py`. O gabarito dela atualizado: o save em formato 7 e a
  guardiã da semente 42 ("Jorra, o Barqueiro do Charco"), conferido campo a campo. **Falta o retrato aprovado** para
  juntar à produção.
- **Os estudos em 32 nativos, aguardando o Jean** (sem 16, sem integração): `criaturas/barqueiro_32/` e
  `criaturas/antagonista_32/`, com as fontes em camadas, as fotos na luta a 1920×945 e as folhas `comparacao.png`. As
  limitações visuais estão em cada LEIA-ME (o Barqueiro perto do Afogado na cor e a rede como pontilhado a 1×; o
  antagonista com a moldura de cabelo que lembra o capuz do Profeta e o rasgo que pode ler como corte).
- **Verificações sobre o código final da produção (1.199.3):** `unittest` (685, 1 pulado: a fumaça, rodada à parte), o
  gabarito idêntico, o pyflakes (só o aviso conhecido) e a fumaça inteira, uma vez (378 ok, "tudo certo"). Na branch do
  Barqueiro: `unittest`, o gabarito atualizado e o pyflakes.
- **Mudança de direção (Jean, 23/10/2026):** o modo "Novo jogo" procedural deve sair no futuro, ficando só a campanha. A retirada não entra agora: pede um levantamento próprio, porque o modo pode compartilhar código com a campanha. **Suspensos** (o que ainda não tinha começado): a adaptação para 16 e a integração do Barqueiro e do antagonista, o retrato do Barqueiro na branch e a junção da branch `claude/barqueiro-do-charco` (com a migração v6→v7 dos covis) à produção. Os estudos e a branch ficam preservados como estão. Os retratos exclusivos do modo procedural não bloqueiam o plano.
- **Útil à campanha:** a Ilse com a ficha dela (1.199.3) e a remoção do `esqueleto_servo` (1.199.1). **Só do procedural:** o gênero do antagonista (1.199.2), a branch do Barqueiro com a migração dos covis e os dois estudos.
- **Parado:** nenhuma criatura nova, o mapa não começado; a retirada do procedural fica para um levantamento próprio.

### 23/10/2026 (data do computador local) — A 1E.4: o levantamento do mapa e do minimapa e o primeiro lote (nada no jogo)

- **Estado conferido:** a branch em `9a296675`, igual ao remoto; o `caido-avatar-512.png` continua fora dos commits; a
  branch `claude/barqueiro-do-charco` e os estudos suspensos não foram tocados. Produção: **1.199.3** (não mudou).
- **O levantamento** (`ferramentas/prototipos/hud/mapa/`, o LEIA-ME e `levantamento.png`, capturas da campanha a
  1920×945): o mapa é um desenho só (`mapa.js`) para o minimapa, o mapa grande e o mapa na página, nos dois modos; os
  símbolos são os sprites 16 antigos, enquanto a lista de Caminhos já usa os ícones de lugar aprovados. Defeitos: a
  posição do jogador sem marca permanente, a escala fracionária (×1,27 e ×2,64), os símbolos do minimapa borrados, as
  estradas cortando os símbolos e a só conhecida quase invisível, a saída fechada com cara de destino aberto, a mesma
  marca "!" para missão e contrato. A ordem sugerida, os estados e as dependências do procedural no item 1.12 do
  plano 23 ("A 1E.4 em 23/10/2026").
- **O primeiro lote, em avaliação** (`pecas.png`, `comparacao.png`, atual × A × B com os mesmos dados): a escala
  inteira, os caminhos por estado com a cancela, os ícones aprovados de lugar no mapa (40 e 32; sem desenho novo), as
  marcas de missão e de contrato desenhadas à mão e o "você está aqui" em duas direções (A, a seta, recomendada; B, o
  herói na plaqueta). O protótipo é uma cópia do `mapa.js` servida só nas fotos; o jogo não mudou.
- **O Aseprite:** o conector desta sessão não subiu (nada escutava a 6515; o editor aberto com um documento do Jean
  respondia "editor not connected"); a janela não foi tocada e as fontes saíram em lote (`auxiliares/montar.lua`).
- **Verificações:** só arquivos de protótipo e de registro mudaram (nenhum do jogo); mesmo assim, `unittest` (685, 1 pulado: a fumaça, rodada à parte), o gabarito idêntico, o pyflakes (só o aviso conhecido) e a fumaça inteira ("tudo certo"). Nas fotos do protótipo, nenhum erro nem aviso no console.
- **Aguardando o Jean:** escolher entre A e B e aprovar (ou não) cada elemento do lote; a integração e o Diário/as
  opções de viagem com o mesmo desenho ficam para depois da escolha.

### 23/10/2026 (data do computador local) — A 1E.4 revisada: a direção B, a barricada, as fontes dos ícones de lugar e o estado fechado (nada no jogo)

- **Estado conferido:** a branch em `f7e9fe29`, igual ao remoto; o `caido-avatar-512.png` fora dos commits; nenhum
  arquivo do jogo mudou (produção **1.199.3**).
- **A escolha do Jean:** a direção **B** (o herói na plaqueta) é a principal; a **A** (a seta) fica preservada como
  alternativa no protótipo.
- **A revisão, em `ferramentas/prototipos/hud/mapa/`** (o LEIA-ME, seção "A revisão depois da escolha do Jean"):
  - a **cancela** refeita como barricada de madeira envelhecida (postes e tábuas em X, sem pintura); uma passada com
    duas travessas lia como banco e ficou fora;
  - a **plaqueta B** com a figura 16 da classe, conferida com o Guerreiro, o Mago e o Arqueiro; sem espaço acima (a
    Capela no minimapa), ela vai para o lado do lugar; a missão e o contrato do lugar atual vão para o lado dela; o nome
    e o símbolo ficam livres. A seta A é cortada pela borda nesse caso (anotado, sem mexer);
  - a **presença no mapa grande:** um 48 dos ícones de lugar pelo mesmo processo do 32 e do 40 (`lugares48.py`), em
    comparação (`presenca-lugares.png`); recomendado, condicionado à decisão sobre as fontes;
  - **as fontes dos ícones de lugar** (`origem-lugares.png`): os 16 arquivos do jogo são reduções "paleta", por fator
    não inteiro, dos recortes de uma folha de referência anexada na HUD 4 pixel (`assets4p/original/`, 14/10/2026), que
    imita pixel art sem grade nativa; cada tamanho é uma redução própria; o processo os refaz idênticos hoje. Não há
    fonte em grade; nada foi redesenhado;
  - **o estado fechado:** vem do `loc["fechado"]` (os `fechados` da região, pela chave, em `campanha.py`), que a viagem
    já usa; a integração pede um campo de bloqueio no `estado.py` pela mesma regra (mais a cidadela selada no
    procedural), distinto do só conhecido e do não vizinho.
- **Verificações:** nenhuma mudança no jogo desde a bateria completa da entrega anterior (unittest, gabarito, pyflakes e
  fumaça "tudo certo"); nas 13 rodadas de fotos da proposta, cliques, destinos, estados e rótulos iguais ao jogo e
  nenhum erro ou aviso no console; as peças novas conferidas pixel a pixel (fonte reaberta, exportado = grade).
- **Aguardando o Jean:** avaliar a revisão (a barricada, a plaqueta, o 40 ou o 48) e decidir o que fazer com a origem
  dos ícones de lugar antes da integração.

### 23/10/2026 (data do computador local) — A 1E.4: a vila e a floresta em grade nativa (nada no jogo)

- **Estado conferido:** a branch em `5ee3f7f7`, igual ao remoto; o `caido-avatar-512.png` fora dos commits; nenhum
  arquivo do jogo mudou (produção **1.199.3**).
- **Decisões do Jean:** a plaqueta B (o retrato da classe) fica; a cancela de madeira aprovada; os caminhos e as marcas
  do protótipo como base; os símbolos de lugar serão reconstruídos em grade nativa, começando pela vila e pela
  floresta, só no protótipo.
- **Feito** (`ferramentas/prototipos/hud/mapa/`, o LEIA-ME e `nativos.png`): a vila e a floresta à mão em 32×32 (o
  minimapa) e adaptadas à mão em 48×48 (o mapa grande; o 32 em 1:1 ficou pequeno diante da plaqueta), fontes em
  camadas pelo Aseprite em lote, o @2x por duplicação exata; o nome do lugar perto da borda procura um lugar livre (a
  Capela no minimapa: nome, plaqueta e ruínas na mesma linha). Recomendação: 32 no minimapa, 48 no mapa grande.
- **Verificações:** o jogo não mudou desde a bateria completa (unittest, gabarito, pyflakes, fumaça "tudo certo"); nas
  rodadas de fotos, cliques, destinos, estados e rótulos iguais ao jogo, sem erro no console; as quatro peças
  conferidas pixel a pixel.
- **Aguardando o Jean:** validar o acabamento da vila e da floresta; os outros lugares e a integração depois.

### 23/10/2026 (data do computador local) — A 1E.4: a vila e a floresta aprovadas; o pântano, as ruínas e a planície em avaliação (nada no jogo)

- **Estado conferido:** a branch em `681f3abf`, igual ao remoto; o `caido-avatar-512.png` fora dos commits; nenhum
  arquivo do jogo mudou (produção **1.199.3**).
- **Aprovadas pelo Jean, sem retoques:** a vila e a floresta nativas, 32 no minimapa e 48 no mapa grande, do commit
  `094bb80a` (as fontes `lugar-vila-n32/n48` e `lugar-floresta-n32/n48` em `ferramentas/prototipos/hud/mapa/fontes/`; os
  PNGs conferidos iguais nesta rodada).
- **Feito** (o LEIA-ME do mapa e `cinco.png`): o pântano, as ruínas e a planície/saída à mão em 32 e 48, fontes em
  camadas, o @2x por duplicação exata; de bioma, porque o procedural também os usa (a barricada continua marca
  separada da saída fechada). O nome do Bosque à noite agora fica sob as próprias árvores, longe do quadrado do Vau
  (a folga dos outros lugares e a posição livre mais longe deles), sem perder a Capela.
- **Ressalva registrada:** o arco das ruínas novas lê mais como pilares quebrados que como arcada.
- **Verificações:** o jogo não mudou desde a bateria completa (unittest, gabarito, pyflakes, fumaça "tudo certo"); nas
  fotos, cliques, destinos, estados e rótulos iguais ao jogo, sem erro no console; as seis peças novas conferidas pixel a
  pixel; a vila e a floresta aprovadas intactas.
- **Aguardando o Jean:** avaliar os três símbolos novos; depois, a integração do conjunto com o campo de bloqueio da
  regra real da viagem. Os símbolos só do procedural ficam fora.

### 23/10/2026 (data do computador local) — A 1E.4: a planície refinada e a Viagem e o Diário com o mesmo desenho (nada no jogo)

- **Estado conferido:** a branch em `c42a6343`, igual ao remoto; o `caido-avatar-512.png` fora dos commits; nenhum
  arquivo do jogo mudou (produção **1.199.3**).
- **Aprovados pelo Jean, sem retoques:** o pântano e as ruínas nativos, 32 e 48, do commit `c7bd2348` (as fontes
  `lugar-pantano-n32/n48` e `lugar-ruinas-n32/n48` em `ferramentas/prototipos/hud/mapa/fontes/`); a vila e a floresta
  continuam aprovadas (`094bb80a`). Os oito PNGs conferidos iguais.
- **Feito** (o LEIA-ME do mapa e `lote3.png`): a planície refinada à mão em 32 e 48 (`lugar-planicie-n32b/n48b`, a
  anterior preservada): os morros em planos, a passagem de terra em curva, duas árvores folhosas espaçadas. E os dois
  itens seguintes da 1E.4, escolhidos por serem os usos pendentes do lugar fora do mapa: **a Viagem** (o mapa da página
  na linguagem nova; as opções "Para onde?" com o símbolo de 32 e as marcas) e **o Diário** (a missão e o contrato com
  o símbolo de 32 e as marcas do mapa no lugar do "!"), em cópias das telas servidas só nas fotos.
- **Verificações:** o jogo não mudou desde a bateria completa (unittest, gabarito, pyflakes, fumaça "tudo certo"); nas
  fotos, cliques, destinos, estados e rótulos iguais ao jogo, sem erro no console; as peças novas conferidas pixel a
  pixel.
- **Aguardando o Jean:** a planície refinada e as duas propostas. Depois, a integração do conjunto na produção, com o
  campo de bloqueio da regra real da viagem; em seguida, a etapa 2 do plano.

### 23/10/2026 (data do computador local) — A 1E.4 integrada (1.200.0): o mapa, a Viagem e o Diário na linguagem nova, com o bloqueio da regra da viagem

- **Estado conferido:** a branch em `a452794b`, igual ao remoto antes do lote; o `caido-avatar-512.png` fora dos commits;
  os estudos e a seta A preservados no protótipo (`ferramentas/prototipos/hud/mapa/`).
- **No jogo (1.200.0):**
  - **o bloqueio pela regra da viagem:** `mapa.bloqueio(g, loc)` ("fechado", o `fechado` da campanha, nunca pelo nome;
    "selada", a cidadela sem os três Sigilos), usado pela viagem (na mesma ordem: a saída antes da confirmação do
    perigo, a cidadela depois) e pela tela (o campo `bloqueio` de cada lugar). `tests/test_bloqueio.py`. **O gabarito
    mudou só por esse campo novo** no estado da tela (as 9 partidas "web"): sem ele, as 24 transcrições saem idênticas
    às guardadas, e o campo só aparece como null nelas;
  - **as peças:** as fontes aprovadas em `ferramentas/arte/aseprite/mapa-*` (a vila e a floresta de `094bb80a`; o
    pântano e as ruínas de `c7bd2348`; a planície refinada de `05af61c5`; a plaqueta, a de lado, as marcas e a cancela
    do protótipo), exportadas para `hud/icones/mapa-*` pelo `exportar_aseprite.py` (a plaqueta a 2× como derivado
    exato); as 20 iguais, pixel a pixel, às propostas, os @2x exatos, o `--conferir` igual;
  - **o mapa (`mapa.js`):** a escala inteira (×2 no minimapa, ×3 no mapa grande e no da Viagem), os cinco símbolos em 32
    e 48, a plaqueta do herói (de lado perto da borda), as marcas, a cancela e o destino bloqueado sem o convite, as
    estradas por estado, os nomes no lugar livre (em duas linhas quando aperta; menores no minimapa estreito), a
    legenda só com o que existe; as opções de destino e o Diário (e o mural, o mesmo cartaz) com o símbolo de 32 e as
    marcas no lugar do "!"; o contrato com "2 trechos · Nv.1" na segunda linha.
- **Conferido** (`ferramentas/prototipos/hud/mapa/capturas/producao*`, a folha `integracao.png`): com os arquivos de
  produção, a 1920×945, de dia e à noite, com as três classes; a Capela na borda; a missão e o contrato no lugar atual e
  em outros; os nomes; os botões alinhados aos símbolos; o mapa grande, o minimapa, a Viagem, o Diário e o mural; o
  zoom de 125% e a janela de 1280×720; o procedural funcionando. Os mesmos lugares, destinos, estados, botões e rótulos
  acessíveis do jogo anterior; sem erro no console. O fotógrafo julga o `/responder` pelo fetch na página (o Chromium
  marca o 204 desse POST como ERR_ABORTED mesmo quando ele termina bem, também no jogo anterior); as outras falhas de
  rede contam.
- **Verificações sobre o código final:** `unittest` (689, 1 pulado: a fumaça, rodada à parte), o gabarito (atualizado só
  pelo campo `bloqueio`, explicado acima), o pyflakes (só os avisos conhecidos de `rpg/eventos/__init__.py`) e a fumaça
  inteira ("tudo certo", 378 ok; o teste da marca do contrato no texto agora confere a peça do mapa, o cursor normal e
  a dica; uma primeira rodada pegou o cursor da marca nova, corrigido no CSS).
- **Pendências reais:** a lista de Caminhos do painel com os ícones de lugar antigos (fora do pedido aprovado); os
  símbolos só do procedural (os antigos); o zoom não inteiro do navegador.
- **Agora:** a etapa 2. O primeiro lote recomendado: a subida de nível com as celebrações e a raridade (o escopo no
  item 1.12 do plano 23). Nada começado.

### 23/10/2026 (data do computador local) — A lista de Caminhos com os símbolos nativos (1.200.1)

- **Estado conferido:** a branch em `4eebba8f`, igual ao remoto; o `caido-avatar-512.png` fora dos commits.
- **No jogo (1.200.1):** a lista de Caminhos do painel do mundo usa o mesmo símbolo de 32 do minimapa (1:1; antes, o
  ícone antigo esticado a 40), com as marcas do mapa (a missão, o contrato) ao lado do nome e a cancela no destino que a
  viagem recusa (`MapaPx.bloqueioHTML`, com o porquê na dica). Os lugares só do mundo gerado sem peça nova ficam com o
  ícone de 32 da família. O nome longo quebra dentro da coluna; os cliques, o destaque no mapa ao passar o mouse e as
  regras de viagem iguais.
- **Conferido** (`ferramentas/prototipos/hud/mapa/capturas/caminhos*`): 1920×945 (o Vau com a saída fechada e o
  contrato no Bosque, o Bosque à noite, a Capela, o procedural) e 1280×720 (o painel rola até os Caminhos, como antes),
  com um nome longo; sem erro no console.
- **Verificações sobre o código final:** `unittest` (689, 1 pulado), o gabarito idêntico, o pyflakes (só os avisos
  conhecidos) e a fumaça inteira, uma vez.

### 23/10/2026 (data do computador local) — Etapa 2, o primeiro lote em avaliação (protótipo)

- **Estado conferido:** a branch em `9fe39e55` (1.200.1), igual ao remoto; o `caido-avatar-512.png` fora dos commits.
- **Nada no jogo.** A subida de nível, as celebrações e a raridade como protótipo em
  `ferramentas/prototipos/hud/celebracoes/` (o levantamento, as decisões e as limitações no LEIA-ME; as cópias de
  `celebracoes.js` e `achado.js` servidas só nas fotos). Atual × proposta com os mesmos dados (cenários de teste: um
  nível, dois níveis seguidos, quatro raridades), a 1920×945 e a 1280×720, com movimento reduzido, clique duplo,
  teclado e clique rápido; folhas estáticas e vídeos.
- **Limitações:** o Sigilo, a especialização e as fagulhas da vitória sem cenário fotografado; o som igual; a aura do
  achado pequena a 1920.
- **Agora:** a avaliação do Jean. Depois, a integração do que for aprovado. O carregar jogo e a criação de personagem
  continuam esperando o levantamento da retirada do procedural; os retratos suspensos e o Grimório, parados.

### 24/10/2026 (data do computador local) — Etapa 2, segunda rodada: três direções (protótipo)

- **Estado conferido:** a branch em `db97777e`, igual ao remoto; o jogo igual à 1.200.1; o `caido-avatar-512.png` fora
  dos commits.
- **Nada no jogo.** A primeira proposta (o Brilho) ficou contida demais para o Jean; fica como histórico. Três
  direções novas em `ferramentas/prototipos/hud/celebracoes/v2/`, montadas por `auxiliares/montar_v2.py`: A ·
  Relicário (cerimonial), B · Estouro (explosivo) e C · Estandarte (faixa de palco). Referências, decisões, cenários e
  limitações no LEIA-ME do protótipo.
- **Demonstração:** `demo.bat` (painel em http://127.0.0.1:8765/): cada cenário nas três direções, no jogo atual e na
  primeira proposta, com troca de classe e saves temporários. Folhas e vídeos em `capturas-v2/`.
- **Conferido:** 1920×945 e 1280×720, movimento reduzido, clique rápido, clique duplo, teclado, textos longos (uma
  simulação identificada); o som é o atual (não ouvido nesta máquina: só o sincronismo pelos tempos).
- **Agora:** a escolha do Jean entre A, B e C (ou a mistura). Depois, a integração. O carregar jogo e a criação de
  personagem continuam esperando o levantamento da retirada do procedural; os retratos suspensos e o Grimório, parados.

### 24/10/2026 (data do computador local) — Etapa 2, o refinamento de A e B (protótipo)

- **Nada no jogo.** O Jean escolheu refinar A (Relicário) e B (Estouro), sem misturar; a C fica reservada; as versões
  anteriores viram histórico. A2 e B2 em `ferramentas/prototipos/hud/celebracoes/v2/` (o que mudou no LEIA-ME): itens
  no tamanho de uso (64), informação sem molduras repetidas, a especialização com o nome protagonista, a comparação
  numa peça só, comum e mágico mais contidos, sustentação mais baixa depois da entrada.
- **Para avaliar:** o painel (`demo.bat`, http://127.0.0.1:8765/) com A2 e B2 em destaque; quatro vídeos sem áudio em
  `ferramentas/prototipos/hud/celebracoes/para-avaliacao/`; a folha `capturas-refino/folha-refino.png`.
- **Agora:** a avaliação do Jean (os vídeos vão também para outra avaliação externa). Carregar jogo e criação de
  personagem, os retratos suspensos e o Grimório continuam parados.

### 24/10/2026 (data do computador local) — Etapa 2: duas apresentações e o piloto do Piromante (protótipo)

- **Decisão do Jean:** Relicário e Estouro ficam como duas apresentações disponíveis, o **Estouro como padrão
  pretendido**; a troca entre elas vai para as futuras opções do jogo. Nada integrado.
- **No protótipo** (`ferramentas/prototipos/hud/celebracoes/`, cópias A3 e B3; A2 e B2 como histórico): o clarão
  concentrado na origem, os botões em ferro escuro com aresta de latão, o acento azul parado do mágico, a base preta
  irregular do título do Estouro, o miolo escuro do selo do item. A identidade separada da apresentação
  (`v2/identidade.js`), piloto só no Piromante: o nome em ouro e laranja com a borda incandescente e chamas em pixel
  nascendo do contorno das letras.
- **Registrado para depois:** os ícones antigos das habilidades, para a etapa do Grimório; as outras especializações,
  depois da avaliação do piloto e da conferência do catálogo; na integração, o id da especialização e o ícone da
  habilidade nova no evento da festa.
- **Para avaliar:** o painel (`demo.bat`, http://127.0.0.1:8765/) com B3 e A3 em destaque; os vídeos `r3-*.webm` sem
  áudio em `para-avaliacao/`; as folhas em `capturas-r3/`; os gestos em `auxiliares/gestos.mjs`.

### 24/10/2026 (data do computador local) — Etapa 2: aprovações, o selo do Estouro e as identidades (protótipo)

- **Aprovado pelo Jean:** A3 e B3 visualmente (com a ressalva do selo dos itens no Estouro) e o Piromante nas duas
  apresentações. Continuam valendo: Relicário e Estouro como duas apresentações, o Estouro como padrão pretendido, a
  troca entre elas para as futuras opções do jogo.
- **No protótipo** (A4 e B4, cópias; A3 e B3 como referência aprovada): o selo dos itens do Estouro com a proximidade e
  o miolo colorido da B2 e só uma separação escura pequena em volta do sprite; as identidades das seis
  especializações (`v2/identidades.js`; a direção de cada uma no LEIA-ME): fogo, luz, sangue, folhas, sombra e almas,
  com forma e movimento próprios, só na celebração da especialização.
- **Para avaliar:** o painel (`demo.bat`, http://127.0.0.1:8765/) com uma linha por especialização; os vídeos `r4-*.webm`
  sem áudio em `para-avaliacao/` (o antes × depois dos itens e as especializações por apresentação); as folhas em
  `capturas-r4/`. Nada integrado: a integração espera esta avaliação.

### 24/10/2026 (data do computador local) — Etapa 2: duas identidades por especialização (protótipo)

- **Aprovado pelo Jean:** o Estouro B4 e o Relicário A4 como apresentações (o Estouro como padrão pretendido; a
  alternância para as futuras opções) e o Piromante nas duas. Não mudam.
- **Candidatas (nada integrado):** duas identidades para Paladino, Berserker, Patrulheiro, Sombra e Necromante, em
  `ferramentas/prototipos/hud/celebracoes/v2/identidades2.js`, nas duas apresentações (`estouro5a/5b`,
  `relicario5a/5b`): Luz do alto / Asas; O nome sangra / Garras; Vendaval / Clareira; Corte / Invisível; Erguer /
  Almas. Direção, referências e limitações no LEIA-ME.
- **Para avaliar:** o painel (`demo.bat`, http://127.0.0.1:8765/); os vídeos `r5-*.webm` sem áudio em
  `para-avaliacao/`; as folhas em `capturas-r5/`. Esperando a escolha de uma identidade por especialização.

### 24/10/2026 (data do computador local) — Etapa 2: as candidatas finais das especializações (protótipo)

- **Aprovado (preservado):** o Estouro B4 e o Relicário A4 como apresentações; o Piromante nas duas.
- **Escolhidas pelo Jean como base:** Paladino, a luz da 1 com as penas da 2; Berserker, a 2 (Garras); Sombra, a 2
  com o corte da 1; Patrulheiro, a 1 (Vendaval); Necromante, a 1 (Erguer).
- **Candidatas finais (nada integrado):** a versão "c" de `v2/identidades2.js`, em `estouro5c` e `relicario5c`: a luz
  do Paladino em faixas amplas translúcidas, o sangue líquido do Berserker, a sequência da Sombra (olhos → nome → corte
  → recomposição), o Patrulheiro todo em verde (a origem do castanho, corrigida) e a fumaça escura do Necromante.
- **Para avaliar:** o painel (`demo.bat`, http://127.0.0.1:8765/), os vídeos `r6-*.webm` sem áudio em
  `para-avaliacao/`, as folhas em `capturas-r6/`.

### 24/10/2026 (data do computador local) — Etapa 2: o sangue do Berserker e a luz do Paladino (protótipo)

- **Aprovados (preservados):** Necromante, Sombra e Patrulheiro da sexta rodada (a versão final "c"), nas duas
  apresentações; o Piromante; o Estouro B4 e o Relicário A4.
- **Pendentes:** Berserker e Paladino, com três alternativas de detalhe cada, em `estouro5d/e/f` e `relicario5d/e/f`:
  o sangue (A gotas pequenas, B filetes, C volumes variados: acumula, escorre, forma a gota, rompe, cai e some, sem
  poças) e a luz (A contínua atrás do nome, B vitral, C centro menos intenso), sem o recorte preto. Nada integrado.
- **Para avaliar:** o painel (`demo.bat`), os vídeos `r7-*.webm` sem áudio em `para-avaliacao/`, as folhas em
  `capturas-r7/`. Esperando a escolha de um sangue e de uma luz.

### 24/10/2026 (data do computador local) — Etapa 2: as celebrações integradas (1.201.0)

- **Integração concluída (no jogo):** a subida de nível, os achados e as raridades, o Sigilo e as especializações, em
  `rpg/web/static/celebracoes/` (`fx.js`, `festa.js`, `estouro.js`, `relicario.js`, `identidades.js`,
  `especializacoes.js`). Versões: o Estouro B4 (padrão) e o Relicário A4; o Piromante (o piloto); Necromante, Sombra e
  Patrulheiro da sexta rodada (`6a1b774b`); o Berserker com o sangue A e o Paladino com a luz B (o vitral), da sétima
  (`59da1c8f`). O motor manda o `id` da especialização e o `icone` da habilidade nova na festa. Saíram a festa antiga
  do nível, do Sigilo e da especialização, a cerimônia antiga do saque (o feixe da `Sensacao`) e o CSS delas.
- **Futura opção do jogo (registrada, sem tela):** a apresentação Estouro ou Relicário (`Festa.usar`).
- **Reservado só para o desenvolvimento:** o Paladino A, a luz contínua (o modo `"continua"` em `especializacoes.js`;
  a fonte e as capturas no protótipo).
- **Conferido no jogo real** (as duas apresentações): nível, dois níveis seguidos, as quatro raridades, a comparação,
  o Sigilo, as seis especializações e um texto longo, em 1920×945 e 1280×720 e com o movimento reduzido; gestos (30
  verificações em cada apresentação); os sons chamados sem erro (não ouvidos nesta máquina). Verificações: o
  `unittest`, o gabarito (atualizado: só os campos novos da festa), o pyflakes e a fumaça.
- **Correção feita na integração (sem mudar a aparência):** os botões reservados do achado (invisíveis, guardando o
  lugar) não tinham as medidas do acabamento novo, e a janela crescia 3 px quando os botões chegavam (já no B4 do
  protótipo); a fumaça pegou e agora a janela nasce no tamanho final. A fumaça passou a ler a ficha do achado ao lado
  do cartão (a regra do Broquel, a troca por espaço de anel).
- **Depois:** o próximo lote da etapa 2, o redesenho do d20 (em avaliação desde 24/10/2026; abaixo).

### 24/10/2026 (data do computador local) — Etapa 2: o d20 em avaliação (protótipo, nada no jogo)

- **Onde:** `ferramentas/prototipos/hud/d20/` (LEIA-ME com o levantamento, as propostas e as verificações; as folhas
  `folha-1920.png` e `folha-1280.png`; a prancha `pranchas/construcao.png`). Base: a 1.201.0, intacta.
- **Demonstração:** `demo.bat` ou `python ferramentas/prototipos/hud/d20/auxiliares/demo.py`, painel em
  http://127.0.0.1:8766/ (o jogo atual, A e B em cada caso; saves temporários).
- **As propostas:** A · Marfim (o dado de osso, o número entalhado, a conta numa tirinha em quatro casas) e B · Vidro
  (o dado de vidro violeta, o número aceso, frente a frente: bônus/total × dificuldade). Recomendação: A.
- **Conferido:** os casos reais (o baú abandonado pelo Explorar; a semente decide o d20 do motor) e o laboratório
  (SIMULAÇÃO, o 20 e o 1 que decidem contra a conta), a 1920×945 e a 1280×720, com o movimento reduzido; gestos
  (pular por clique e Esc, cliques rápidos e tecla segurada sem atravessar, texto instantâneo); o número do dado igual,
  pixel a pixel, ao desenhado com o d20 da mensagem.
- **Preferência permanente de entrega (Jean, 24/10/2026):** sem vídeos, salvo pedido explícito; capturas, folhas
  comparativas e uma demonstração no navegador.
- **Agora:** a escolha do Jean entre A e B (nada integrado). Não começados: o livro da capela, as outras telas, a
  retirada do procedural.

### 24/10/2026 (data do computador local) — Correções de interface, o d20 integrado, as dicas e o baú em avaliação (1.201.1 a 1.202.1)

- **Retomada noutra conta:** a branch `claude/tender-einstein-tx3tjl` limpa e igual ao remoto (`17957e17`); o PNG
  pessoal `ferramentas/arte/referencias/icones/caido-avatar-512.png`, não rastreado, preservado.
- **Correções no jogo:**
  - 1.201.1, a lista de saves: o Voltar entrava 40 ms por opção contando os cartões dos saves (com 38 saves, 1,5 s
    invisível); agora conta só os botões à vista, e o Esc volta na lista de saves e na escolha da classe;
  - 1.201.2, o selo de raridade vazio: o CSS do Relicário, carregado junto, pintava o texto do selo do Estouro na cor
    do fundo; as regras dele valem só nele. **Mágico passa a se chamar Incomum** (Comum → Incomum → Raro → Lendário;
    o id `magico` fica, sem migração; "Incomum" não tinha uso);
  - 1.201.3, a janela antiga piscando ao Guardar/Equipar: a janela perdia o id `#sobre-achado` no começo do
    esmaecer e voltava ao desenho antigo por ~230 ms; agora sai com o id, sem receber cliques;
  - 1.201.4, a ficha do achado sem nada no espaço: o tipo e os números num bloco debaixo do nome (sem a área larga);
    a comparação em três colunas sem mudança;
  - 1.201.5, o Urso Pardo do abrigo da tempestade (um javali robusto renomeado) com o retrato do urso pela `origem`
    (o mesmo caminho do Espantalho e do Mímico); números, família e comportamento do javali robusto.
- **O d20 (1.202.0):** as três apresentações aprovadas pelo Jean, o **Clássico (o padrão)**, o **Marfim** e o
  **Vidro**, à escolha na **Ajuda (F1), "Dado dos testes"**; guardada também em disco (`preferencias/tela.json`, ao
  lado dos saves: a porta muda a cada abertura e o armazenamento do navegador com ela), volta ao reabrir o jogo; sem
  escolha válida, o Clássico. **O seletor é provisório e vai para o menu de configurações** quando ele existir.
  Independe de Estouro/Relicário. De passagem: Enter e Espaço nos botões da Ajuda apertam o botão (antes, com uma
  pergunta de opção única atrás, respondiam a pergunta).
- **As dicas (1.202.1):** revisão focada nos textos de orientação (a dica da vida bloqueada, os ferimentos, a noite,
  o achado e as linhas da Ajuda), sem diálogos nem lore.
- **O baú em avaliação (só no protótipo):** `ferramentas/prototipos/hud/bau/` (LEIA-ME, `folha-propostas.png`,
  `folha-contexto.png`): A, a identidade de sempre; B, o baú trancado com o cadeado. Esperando a escolha.
- **Preferência permanente de entrega (Jean):** sem vídeos, salvo pedido explícito; capturas compactas, poucas folhas
  com os mesmos dados no antes e depois, e uma demonstração no navegador quando a interação precisa ser testada.
- **Verificações:** o `unittest` (o teste de estilo pegou o `21-d20.css`, que estende a rolagem aprovada e foi para
  `FORA_DA_TRAVA`), o gabarito (atualizado duas vezes, só nos textos: "Incomum" e as dicas, conferido trocando os
  textos antigos pelos novos), o pyflakes e a fumaça (693 testes ok, 1 pulado; fumaça "tudo certo"). A fumaça pediu
  dois ajustes no roteiro: a janela do achado que sai agora esmaece com o id, então o roteiro ignora a `.saindo` (o
  jogador também não clica nela); e a frase nova da noite (N1). As telas a 1920×945 e 1280×720 e o movimento reduzido.
- **Achado registrado, sem mexer:** a velocidade do texto, o som e o "Destacar interações" ficam só no navegador; como a
  porta muda a cada abertura, eles também não voltam ao reabrir o jogo. Levar para o arquivo de preferências junto do
  menu de configurações.
- **Não começados:** o livro da capela, a retirada do procedural e outras frentes.

### 24/10/2026 (data do computador local) — Preferências persistentes, dicas mais claras, o lendário e a A2 do baú (1.202.2 a 1.202.4)

- **Preferências (1.202.2, no jogo):** a velocidade do texto, o som e o "Destacar interações" passaram a ficar no
  mesmo arquivo do d20 (`preferencias/tela.json`, ao lado dos saves; independente dos saves da campanha), pela mesma
  rota e por um ajudante só (`preferir`, em `app/nucleo.js`). Cada uma é gravada sem mexer nas outras; na abertura,
  as guardadas valem mais que as do navegador; sem arquivo (ou com valor inválido), os padrões de antes. Conferido
  abrindo o jogo três vezes em portas diferentes com o navegador zerado. **Para conferir:** mude o texto (V), o som
  (S), o destaque (F4) e o dado (F1), feche e abra o jogo; o arquivo fica em `~/.cronicas_da_fenda/preferencias/`.
- **Dicas (1.202.3, no jogo):** a dica da vida bloqueada diz o que reduz a vida máxima e quanto ("Um ferimento e a
  fome reduzem sua vida máxima de 60 para 49. Curas param em 49.") e como o limite volta ("depois de alguns dias de
  descanso, ou na hora, na Curandeira"; a fome, comendo); a bandagem explicada na dica dela ("Não recupera vida nem a
  vida máxima: o ferimento continua até sarar."); o primeiro ferimento com os dias reais.
- **O achado lendário (1.202.4, no jogo):** conferido durante a entrada, a 1920×945 e 1280×720: as pontas dos raios
  encostavam no "+" dos atributos; só no lendário sem comparação, a coluna se afasta 12 px a mais.
- **O baú (só no protótipo):** o Jean escolheu o A como direção. A **A2**, o refino (a tampa abaulada, a três quartos
  evidente, os planos de luz e um 48 próprio para a pilha), em `ferramentas/prototipos/hud/bau/` (`folha-a2.png`);
  A, B e o placeholder ficam como histórico. **Aguarda a avaliação; nada integrado.**
- **Verificações:** o `unittest` (695 ok, 1 pulado), o gabarito (atualizado só nos textos da vida bloqueada e da
  bandagem, conferido trocando os textos antigos pelos novos), o pyflakes e a fumaça.
- **Não começados:** o livro da capela e a retirada do procedural.

### 24/10/2026 (data do computador local) — O baú A integrado (1.203.0)

- **Retomada noutra conta:** a branch `claude/tender-einstein-tx3tjl` limpa e igual ao remoto (`77f959db`, a 1.202.4);
  o PNG pessoal `ferramentas/arte/referencias/icones/caido-avatar-512.png`, não rastreado, preservado. Os trabalhos da
  1.202.2 a 1.202.4 (as preferências, as dicas, o lendário) conferidos nos registros, sem refazer.
- **Decisão do Jean:** o **A original da primeira rodada** (`a997955e`: a tampa abaulada em três quartos, as cintas de
  ferro, o espelho de latão). A A2, o refino, **não foi aprovada**; ela, o B e o placeholder ficam como histórico.
- **No jogo (1.203.0):** `rpg/web/static/hud/icones/bau-*.png`, exportados da fonte copiada sem retoque para
  `ferramentas/arte/aseprite/bau/bau-32.aseprite`; o 48 da pilha é o 32 centrado (menor que o do placeholder, como
  aceito) e o 64 o 32 ×2 (`DERIVADOS`). Saiu sozinho da conferência da família de ferro (tem fonte no Aseprite).
- **Conferido:** os seis arquivos iguais, pixel a pixel, aos de `ferramentas/prototipos/hud/bau/propostas/bau-a/`;
  `exportar_aseprite.py todas --conferir` e `familia_ferro.py --conferir` sem diferença; no jogo (o cenário `baus`), a
  bolsa (32) e a pilha "Baús abertos ×3" (48), a 1920×945 e a 1280×720, só com os arquivos de `/static/hud/icones/`
  (nenhum pedido ao protótipo, nenhum erro): `ferramentas/prototipos/hud/bau/folha-integracao.png`.
- **Sem mudança:** o Mímico, o quadro do espólio, as regras e o sorteio dos baús.
- **O próximo da etapa 2:** o livro narrativo da capela (o levantamento, registrado à parte, abaixo).

### 24/10/2026 (data do computador local) — Etapa 2: o livro narrativo da capela, o levantamento (nada no jogo)

- **Onde:** `ferramentas/prototipos/hud/livro-capela/` (LEIA-ME e `folha-atual.png`, a 1920×945 e a 1280×720 pelo
  cenário `capela`, `ETAPA=ossuario LIVRO=0 SALA=sacristia`). Só o levantamento: nada redesenhado nem implementado;
  textos e regras intocados.
- **Hoje:** lê-se na sacristia depois da luta (menu ou ponto "Livro"), nas etapas ossuário, fundo e retorno (e depois
  do fim); a primeira leitura grava `ilse` e `sigilo_do_turvo` (o nome da guardiã, a pergunta que leva à Berta, o
  primeiro requisito do descanso); reler não muda nada; fecha por botão, Esc, Enter, espaço ou véu. A tela é a casca do
  Grimório antigo (CSS, filete dourado), 860×360 nas duas janelas.
- **Problemas observados:** a casca não é a linguagem aprovada; outro objeto que o registro castanho da cena; metade das
  páginas vazia; o salto de anos entre as entradas não se vê na tela (o modo texto tem "Algumas páginas adiante:"); o
  Fechar por fora da moldura. À parte, para uma correção separada: o atalho da missão no painel aponta para "Ler o
  livro da capela" mesmo com o objetivo "Descer ao ossuário" e depois de ler; o Histórico repete a linha a cada leitura.
- **Escopo proposto:** o registro aberto em pixel art (couro castanho como na cena, lombada, blocos de folhas), o papel
  com grão e as duas tintas, a marca do salto de tempo sem texto novo, o tamanho pelo texto, o Fechar dentro da moldura
  de ferro, CSS separado do Grimório, a abertura em poucos quadros. Duas variantes na proposta.
- **Agora:** a decisão do Jean sobre o escopo. Não começados: a retirada do procedural e outras frentes.

### 24/10/2026 (data do computador local) — Etapa 2: o livro da capela, três propostas (protótipo, nada no jogo)

- **Onde:** `ferramentas/prototipos/hud/livro-capela/` (LEIA-ME, seção "As três propostas"; `folha-propostas.png`;
  demonstração em `demo.bat`, painel em http://127.0.0.1:8767/, com saves temporários). O livro de hoje continua no
  jogo; nada integrado.
- **A direção do Jean:** ler algo escrito por uma pessoa daquele mundo; o registro que termina em confissão. A
  referência foi a tipografia de Pentiment (a letra como voz de quem escreve), sem a estética dele. Sem autor, data,
  assinatura nem fato novo: o autor é "o padre" (a pista `ilse`), sem nome.
- **As propostas:** A · registro pautado (outra tinta e outro começo na segunda entrada); B · registro que vira
  confissão (a mesma mão, mais depressa, na segunda); C · leitura próxima (uma entrada por vez, Anterior/Próxima e as
  setas). Letra: Fondamento (OFL 1.1, Fontsource 5.3.0, licença em `fontes/`). O livro em pixel art pelo método das
  cenas, com o couro da sacristia; o texto em HTML.
- **Conferido:** as três e o livro de hoje a 1920×945 e 1280×720 no cenário `capela`; as mesmas pistas e o mesmo
  cartão na primeira leitura, nada na releitura; os gestos (teclado, Tab, véu, nada atravessando, movimento reduzido)
  em `auxiliares/gestos.mjs`. `unittest` (695 ok, 1 pulado) e pyflakes; o jogo não mudou.
- **Recomendação:** C, com a mão da B. **À parte, para avaliação:** a nota da interface "Algumas páginas adiante:"
  antes da segunda entrada (a frase que o modo texto já usa), porque a cronologia não fica clara só pela apresentação.
- **Continuam separados:** o atalho da missão que aponta para o livro e a linha repetida no Histórico.
- **Agora:** a escolha do Jean. Não começados: a retirada do procedural e outras frentes.

### 24/10/2026 (data do computador local) — O livro da capela: a A refinada (protótipo, nada no jogo)

- **A decisão do Jean:** a A como base; esta rodada é só a aparência. **O texto e a história do livro serão revistos
  depois, na frente narrativa da campanha**; o conteúdo atual fica como amostra de leitura, sem mudança e sem
  explicação nova de tempo, data ou autoria.
- **A refinada** (`ferramentas/prototipos/hud/livro-capela/`, LEIA-ME, seção "A refinada"; `folha-a2.png`): o papel com
  o centro calmo e o desgaste nas beiras e na dobra (`livro-a2.png`); a letra apoiada na pauta pela métrica da
  Fondamento, com a pauta desenhada pelo bloco de texto, em qualquer texto e quebra (na A, a linha de base ficava 2 px
  acima). Iguais à A: as duas páginas, a fonte, a pauta e a margem, o couro e as medidas, as tintas, o vazio da
  esquerda. A, B e C intactas.
- **Conferido** a 1920×945 e 1280×720 no cenário `capela`: desvio 0 px em todas as linhas, também com textos de teste
  longos, acentuados e maiores que a página (rola com a pauta junto; `auxiliares/pauta.mjs`); foco, fechar, véu, as
  teclas do menu isoladas, as mesmas pistas (`auxiliares/gestos.mjs`). O jogo não mudou.
- **Demonstração:** `demo.bat`, http://127.0.0.1:8767/ ("A refinada" ao lado de A, B, C e do livro de hoje).
- **Agora:** a avaliação do Jean; nada integrado. Não começados: a retirada do procedural e outras frentes.

### 24/10/2026 (data do computador local) — A base dos livros aprovada; o livro da capela deteriorado (candidata)

- **Aprovada pelo Jean:** a A refinada (`831a1bbb`) é a **base visual dos livros do jogo**: as duas páginas, a
  Fondamento, a pauta alinhada pela métrica da fonte, as margens, o couro e a leitura. Guardada limpa e separada em
  `ferramentas/prototipos/hud/livro-capela/` (`livro-a2.png`, `.lv-regua`, `medirTopo`). Não troca outras telas.
- **Candidata, só no protótipo:** o livro da capela deteriorado (`desenhar_capela.py`, `livro-capela.png` e as máscaras;
  `folha-capela.png`): pedaços arrancados mostrando a folha de baixo, o couro ou nada; um rasgo entrando pela beira;
  três níveis de água na esquerda e um na direita; manchas de bolor junto da encadernação e nas quinas; o couro escuro,
  gasto e sem um canto. O rasgo tira papel, pauta e tinta juntos e só trechos ("nem" 5%, "do" 26%); Ilse, Sigilo e as
  outras essenciais intactas, as mesmas letras tocadas a 1920 e a 1280.
- **Conferido:** `dano.mjs` (as palavras tocadas, o texto real e textos de teste maiores rolando), `pauta.mjs`
  (`PROPOSTA=capela`: desvio 0, a rolagem), `gestos.mjs` (foco, fechar, véu, as teclas do menu, as mesmas pistas). Limite
  registrado: o dano é da página; um texto novo pede o `dano.mjs` de novo. O jogo não mudou.
- **Demonstração:** `demo.bat`, http://127.0.0.1:8767/. **Agora:** a avaliação do Jean; nada integrado. O conteúdo
  narrativo continua para a frente narrativa da campanha.

### 24/10/2026 (data do computador local) — O livro integrado (1.204.0)

- **Aprovados pelo Jean:** a A refinada (`831a1bbb`) como base visual dos livros e a capela deteriorada (`5147ec85`) no
  livro da sacristia, com uma correção antes: as três colônias de bolor no couro da faixa de baixo (pontos soltos além
  da borda da capa) saíram, e o bolor só pinta sobre papel ou couro opacos (conferido pixel a pixel).
- **No jogo:** `telas/livro.js` (`Telas.lerLivro`, `Telas.fecharLivro`), `css/22-livro.css` (dentro da trava do estilo
  pixel), `static/livros/` (a base, a capela e as máscaras), a Fondamento e a licença em `static/fontes/`. O documento
  declara o acabamento (`LIVRO_DA_CAPELA["acabamento"] = "capela"`); sem seletor do jogador. O livro antigo (em
  `cenas.js`, com o CSS dele e o `.grimorio-fechar`, que só ele usava) saiu. O Grimório e as outras telas não mudaram.
  Receita para outros livros: `docs/COMO_CRIAR.md`, "Um documento para ler".
- **Conferido:** `conferir_jogo.mjs` no jogo de produção, a 1920×945 e a 1280×720 (só arquivos de produção; o
  acabamento; a pauta com desvio 0; o dano tirando só trechos, as essenciais intactas; um texto maior rolando com a
  pauta e o dano presos à página; Esc e as teclas do menu); a fumaça (primeira leitura, cartão, releitura, foco, Esc).

### 24/10/2026 (data do computador local) — As pendências do livro (1.204.1)

- **Reproduzidas no jogo antes de corrigir** (cenário `capela`, o livro por ler): com o objetivo "Descer ao ossuário",
  o atalho do painel da missão dizia "Ler o livro da capela ▸" antes e depois de ler (o painel pega a primeira opção da
  missão no menu, e o livro e o baú vêm antes); o Histórico ganhava uma linha "Leu o livro da capela" a cada abertura.
- **Corrigidas:** as ações ao lado do objetivo (o livro e o baú da sacristia) levam `atalho=False` e ficam fora do
  atalho (continuam no menu, na mesma ordem, e no ponto da cena: a releitura fica); o motor manda `primeira` com o livro
  e só a primeira leitura entra no Histórico. Sem mudança de save, de pistas, de requisitos nem de recompensas.
- **Regressões:** `test_missoes` (as metas do menu, `primeira` só na descoberta, a pista uma vez) e a fumaça (o atalho
  "Descer ao ossuário" e uma linha no Histórico, também depois de reler).
- **Fica como está, de propósito:** na etapa do fundo, "Soltar as correntes" vem antes de "Descer ao fundo" e é o
  atalho; é um preparo do caminho do descanso, não uma ação lateral como o livro. Se o Jean preferir o atalho no
  "Descer ao fundo", é marcar `atalho=False` nela.

### 24/10/2026 (data do computador local) — Etapa 2: o que resta (levantamento, nada mudado)

- **Onde:** `ferramentas/prototipos/hud/levantamento-etapa2/` (LEIA-ME, `folha-levantamento.png`, as fotos e os dois
  roteiros que as tiram). Sobre a 1.204.1, no jogo a 1920×945.
- **Já substituído:** a subida de nível, as celebrações e a raridade, o d20, o baú, o livro; antes deles, a HUD de ferro
  (painéis, doca, mapa, Diário, Bestiário, Comitiva, Inventário, mercado, mural, serviços, Ajuda, Histórico,
  confirmação, viagem, fogueira, luta).
- **Destoa ainda:** as faixas de passagem (a de Vitória a cada luta; a tarja por cima das colunas, o sprite antigo, o
  subtítulo miúdo) e os quadros de orientação da abertura guiada (o botão chapado); detalhes menores no texto narrado.
- **Adiado** (retirada do procedural): o título, os saves, a criação de personagem. **Etapa 8:** Grimório e Talentos.
- **Recomendação:** o próximo lote são as faixas de passagem, num lote só, em protótipo com duas variantes; depois, a
  orientação. A etapa 2 não está concluída. Não começados: a retirada do procedural e outras frentes.

### 24/10/2026 (data do computador local) — As faixas de passagem: duas direções (protótipo, nada no jogo)

- **Onde:** `ferramentas/prototipos/hud/faixas/` (LEIA-ME, `folha-faixas.png`, as fotos em tamanho real, a
  demonstração em `demo.bat`, painel em http://127.0.0.1:8768/, com saves temporários). As faixas de hoje no jogo.
- **Os usos reais levantados:** Vitória (1 s, toda luta), Guardião (1,5 s), Mestre caçador (1,8 s), Você caiu/morreu
  (2,2 s, a única que se adianta), Exausto (2,3 s), Saindo da capela (2,6 s; o texto até 155 letras), a chegada à
  comitiva (1,5 s). A sequência real: Guardião → Mestre caçador → espólio → subida de nível → achado.
- **As direções:** A · a faixa integrada ao palco; B · emblema e anúncio. As duas dentro do palco, o subtítulo a 18–19
  px (hoje 15–17), os ícones da família, quatro pesos pela forma e pelo movimento. Só o desenho muda: os tempos, os
  sons e a ordem são os de hoje (os mesmos tempos medidos nas três versões); cliques e teclas nas faixas não escolhem
  nada na tela seguinte; o movimento reduzido mostra a faixa inteira, parada.
- **Recomendação:** A (a mais leve para a Vitória repetida, apoiada no palco; a 1280 com folga). **À parte:** o adiantar
  não encurta as faixas (só a queda olha o `pular`); hoje, o Guardião e o Mestre ficam ~0,1 s um sobre o outro.
- **Agora:** a escolha do Jean; nada integrado. Não começados: os quadros do tutorial, o menu inicial, o Grimório e a
  retirada do procedural.

### 24/10/2026 (data do computador local) — As faixas: a original refinada (protótipo, nada no jogo)

- **A decisão do Jean:** a faixa de hoje fica como base; A e B, histórico (não aprovadas para integração).
- **A candidata R** (`ferramentas/prototipos/hud/faixas/`, LEIA-ME no topo, `folha-original-refinada.png`, a linha "R"
  na demonstração): a mesma tarja larga atravessando a tela, o título de 80 px, os tempos, os sons e as partículas de
  hoje; o subtítulo de 15–17 para 20–21 px, com espaço e quebra de linha; a espada aprovada (espelhada à direita) e o
  "Sair" da doca; a tarja em pixel, com as pontas em degraus de borda dura (sem pontilhado sobre o texto das colunas);
  o acento breve do marco na entrada; a queda e o cansaço entrando descendo; a troca limpa (a anterior sai em 100 ms).
  A caveira e a lua continuam as de hoje (não há aprovados que correspondam).
- **Conferido** no jogo, a 1920×945 e a 1280×720: os mesmos tempos da de hoje na sequência real (Guardião → Mestre →
  espólio → nível → achado); no máximo uma faixa inteira por vez (hoje, duas); cliques e teclas não atravessam; o
  movimento reduzido com a faixa inteira e parada. `unittest` e pyflakes; o jogo não mudou.
- **Pendências separadas:** o adiantar das faixas; as duas `@keyframes faixa` com o mesmo nome (`03` e `06`).
- **Agora:** a avaliação do Jean; nada integrado.

### 24/10/2026 (data do computador local) — As faixas integradas (1.205.0)

- **Aprovada pelo Jean:** a original refinada (R, `6d8f5f76`), levada ao jogo sem retoques: `faixa` em
  `telas/celebracoes.js` (a tarja em pixel num canvas, os pesos, o acento do marco, a troca limpa) e `css/23-faixas.css`
  (dentro da trava do estilo pixel). O CSS antigo da faixa saiu de `06`. A original, A e B ficam no protótipo.
- **A colisão de nome:** as duas `@keyframes faixa` (`03-batalha.css` e `06`) separadas; os rótulos da luta
  (`.faixa-acao`) usam `faixa-acao`, com o desenho que já se via (o de `06`, que valia também ali; a de `03` nunca
  chegava à tela): `auxiliares/sonda_faixa_acao.mjs` mediu 9 variantes × 10 instantes, iguais antes e depois.
- **Conferido no jogo:** os sete usos a 1920×945 e 1280×720 (iguais ao protótipo aprovado, até 0,2% de pixels de
  diferença, da cena atrás); a sequência Guardião → Mestre → espólio → nível → achado com os mesmos tempos de antes;
  no máximo uma faixa inteira por vez; cliques e teclas não atravessam; o movimento reduzido. `unittest` (696 ok, 1
  pulado), gabarito sem atualizar (nenhuma diferença), pyflakes e fumaça.
- **Continua pendente, à parte:** o adiantar das faixas (só a queda olha o `pular`).

### 24/10/2026 (data do computador local) — Os quadros de orientação: duas propostas (protótipo, nada no jogo)

- **Onde:** `ferramentas/prototipos/hud/orientacao/` (LEIA-ME com o levantamento; `folha-orientacao.png`; `demo.bat`,
  painel em http://127.0.0.1:8769/, com estado temporário: os seus saves e o tutorial deles não são tocados).
- **O levantamento:** os quadros por grupo (a abertura, a luta guiada, a vila, os contratos, o achado e os outros,
  feridas e fogueira), o alvo de cada um, onde moram, os controles ("Entendi" nas informativas, "Encerrar tutorial"
  em todos) e quando reaparecem.
- **As propostas (só o acabamento, por CSS):** A · o quadro da HUD; B · a chamada contextual. Os nove casos nas três
  versões, a 1920×945 e a 1280×720: dentro da janela, cobrindo 0 px do controle; os gestos iguais aos de hoje.
- **Recomendação:** B (a ligação com o controle mais clara). Registrados à parte: a ordem do Tab contrária à leitura
  (como hoje) e o N1 a 1280 de hoje sobre o nome do lugar.
- **Agora:** a escolha do Jean; nada integrado. Não começados: o menu inicial, a retirada do procedural, o Grimório.

### 24/10/2026 (data do computador local) — Tutorial R, aviso de talento, a retirada do procedural (1.206.0)

- **Tutorial (protótipo, aguardando o Jean):** a B refinada, R (`ferramentas/prototipos/hud/orientacao/`, segunda
  rodada no LEIA-ME; `folha-orientacao.png`, hoje × B × R; `demo.bat`): o ouro envelhecido só na seta e num traço
  junto dela, o "Entendi" no botão da HUD, o Tab na ordem da leitura. O V1 e a luta guiada C1–C4 entraram nos casos
  (`JA_VISTAS` no cenário `tutorial`). Corrigido no jogo (1.205.1): o quadro do C2 cobria a linha da habilidade.
- **Aviso de ponto de talento (protótipo, aguardando o Jean):** confirmado o acabamento antigo (a estrela e a seta de
  sprite ampliadas, o brilho que atravessa; a 1280, duas linhas; Enter não abria). A candidata R em
  `ferramentas/prototipos/hud/aviso-talento/` (`folha-aviso.png`). O Continuar da subida de nível ficou fora.
- **A retirada do modo procedural (1.206.0):** o levantamento, as decisões e o que fica para a expansão em
  [24-RETIRADA-DO-PROCEDURAL.md](24-RETIRADA-DO-PROCEDURAL.md). Só a campanha: o título com "Novo jogo" (a campanha),
  "Carregar" e "Sair"; o save do mundo gerado aparece marcado e não abre (mensagem curta; o arquivo fica).
- **Telas iniciais (protótipo, aguardando o Jean):** o levantamento e a criação em cartões, R
  (`ferramentas/prototipos/hud/telas-iniciais/`, `folha-telas-iniciais.png`, `demo.bat` na porta 8770). O título e o
  save recusado ficam como estão; os cartões dos saves, registrados para a consolidação da HUD.
- **Conferido:** `unittest` (682 ok, 1 pulado), o gabarito novo (as 24 partidas na campanha; as transcrições
  conferidas antes de atualizar), pyflakes e fumaça (tudo certo); as telas iniciais a 1920×945 e 1280×720.
- **A ordem combinada:** fechar o tutorial, o aviso de talento e as telas iniciais (título, saves, criação); depois a
  forja. O reforço/encantamento e a expansão narrativa não começam antes do pedido.

### 25/10/2026 (data do computador local) — Tutorial R e aviso de talento R no jogo (1.207.0); a criação em etapas (R2)

- **Retomada em outra conta:** conferidos a branch (`claude/tender-einstein-tx3tjl`, igual ao remoto), o remoto
  (`Burbb/teste2`) e as alterações locais (só `ferramentas/arte/referencias/icones/caido-avatar-512.png`, pessoal, fora
  do Git e preservado). As fontes finais foram as dos registros da rodada anterior: a R de `orientacao/orientacao.css`
  (com a troca da ordem dos botões do cenário) e a R de `aviso-talento/aviso.css` (com o HTML do `cenario_aviso.py`).
- **Integrados na 1.207.0, aprovados pelo Jean:** os quadros de orientação na B refinada (R): o fundo escuro, o ouro
  envelhecido na seta, no traço junto dela e no contorno do controle, o "Entendi" no botão da HUD, o Tab na ordem da
  leitura; textos, gatilhos, sequência e comandos sem mudança. O aviso de ponto de talento R: o botão da HUD com o ícone
  dos Talentos da doca e a seta dentro, um `<button>` (Enter e espaço abrem). Saíram a estrela, a seta de fora, o brilho e
  o sprite `seta_esq`. O "Continuar" da subida de nível ficou fora, por decisão do Jean.
- **Conferido:** as fotos de referência da R tiradas pelos roteiros dos protótipos antes de integrar e as do jogo depois:
  os 14 quadros (mural, luta guiada C1–C4, bordas, doca, achado) nas duas janelas com as medidas iguais e 0 px sobre o
  controle, `gestos.mjs` (o clique no quadro não escolhe nada, Enter no Entendi fecha só ele); o aviso com 1, 3 e 12
  pontos numa linha, sumido sem pontos, com o foco visível. `unittest` (682 ok, 1 pulado), gabarito sem mudança (a
  mudança é só visual), pyflakes e fumaça (tudo certo).
- **Criação de personagem (protótipo, aguardando o Jean):** a criação em etapas R2
  (`ferramentas/prototipos/hud/telas-iniciais/`, segunda rodada no LEIA-ME; `folha-criacao-r2.png`, R × R2 com os mesmos
  dados; `demo.bat`, porta 8770, botão R2): uma área própria sobre a paisagem do título, "Nome → Classe → Modo", o resumo
  no rodapé, cartões de classe com o retrato, a frase, o ataque e o recurso e as especializações discretas, o modo pelas
  consequências da queda, o tutorial logo abaixo e "Começar campanha"; escolher separado de avançar. Conferida no jogo
  (`criacao_r2.mjs`, as duas janelas, tudo certo, três campanhas começadas). O que é só da demonstração e o que a
  integração pede está no LEIA-ME. A R fica para comparar.
- **Pendências reais das telas iniciais:** a aprovação e a integração da criação; os cartões e a lista do "Carregar
  jogo", ainda no acabamento antigo, sem proposta. O título e o save recusado ficam como estão.
- **A etapa 2 não está encerrada.** Próximo passo: o Jean avalia a R2; aprovada, integrar a criação; depois, a proposta
  dos cartões dos saves e a revisão por evidência dos componentes antigos restantes; então a forja. Não começados (sem
  pedido): a forja, o reforço/encantamento, o Grimório, a expansão narrativa.

### 25/10/2026 (data do computador local) — A criação em etapas no jogo (1.208.0); o "Carregar jogo" em avaliação

- **Integrada na 1.208.0, aprovada pelo Jean, sem retoques:** a criação em etapas (R2). O motor manda tudo numa
  pergunta só (`rpg/criacao.py`; as frases curtas em `classes.py`) e confere a resposta; a tela (`app/criacao.js`,
  `css/24-criacao.css`) anda por Nome → Classe → Modo e responde uma vez, no "Começar campanha". O texto e o robô
  (gabarito, testes) seguem com as perguntas de sempre. Saíram as adaptações da demonstração e a caixa marcável da tela
  gráfica (sem uso). A espera por tempo do Avançar saiu: a tecla segurada passa pelo `Gesto` e o clique duplo pelo
  `detail`; um Enter novo responde na hora. Sem escolha de gênero; os nomes das classes como estão.
- **Conferido:** `criacao.mjs` (protótipo das telas iniciais) no jogo, 1920×945 e 1280×720: as três classes, os dois
  modos, o tutorial ligado e desligado, o nome longo com acento, avançar/voltar/preservar, o Enter segurado, o clique
  duplo, uma resposta só ao motor, a campanha com o que se escolheu, e salvar e carregar a campanha criada. Testes novos
  em `tests/test_criacao.py`; `test_web` responde à pergunta nova; a fumaça passa pela criação nova. Gabarito sem
  mudança (as partidas usam `iniciar`, não a criação).
- **"Carregar jogo" (protótipo, aguardando a aprovação visual do Jean):** o levantamento e a proposta R em
  `ferramentas/prototipos/hud/carregar-jogo/` (a pasta não se chama `saves/` porque o `.gitignore` protege as pastas de
  saves pessoais; `folha-saves.png`; `demo.bat`, porta 8772, saves temporários e simulados, identificados). A janela da
  família da criação, uma coluna que rola, o Voltar no rodapé junto com a lista, a especialização e a missão em
  andamento, o que não abre dito em texto, o teclado pelos cartões.
- **Pendências reais da etapa 2:** a aprovação e a integração do "Carregar jogo"; o tempo da lista que cresce com o
  número de saves (~9 ms por save, a leitura do motor), registrado; a revisão por evidência dos componentes antigos
  restantes. O "Continuar" da subida de nível fica fora, por decisão do Jean. Não começados (sem pedido): a forja, o
  reforço/encantamento, o Grimório, a expansão narrativa.

### 25/10/2026 (data do computador local) — O Carregar jogo no jogo (1.209.0); a etapa 2 concluída; a forja começada

- **Integrado na 1.209.0, aprovado pelo Jean, sem redesenho:** o Carregar jogo R (`telas/saves.js`,
  `css/25-carregar.css`; a especialização e a missão em andamento em `resumo_save`). Os dois ajustes pedidos: o nome
  cortado com a dica inteira no mouse e no foco do teclado; o foco inicial na partida mais recente que abre (sem
  nenhuma, no Voltar). Sem índice paralelo dos saves (~9 ms por save no motor, decisão do Jean). Os saves pessoais, os do
  mundo gerado e os danificados: tratados como antes, nada apagado nem convertido.
- **Conferido:** `carregar-jogo/auxiliares/conferir.mjs` nas duas janelas (sem saves, uma, dez, 22, a mais recente que
  não abre, nenhuma que abre; Tab, setas, Home/End, Esc, Enter, clique duplo, a dica do nome); criar, salvar e carregar
  uma campanha nova pela lista (`telas-iniciais/auxiliares/criacao.mjs`). `unittest` (689), gabarito sem mudança,
  pyflakes, fumaça.
- **A etapa 2, concluída no escopo acordado** (`ferramentas/prototipos/hud/revisao-etapa2/LEIA-ME.md`): as entregas da
  1.201.0 à 1.209.0; os dois defeitos achados (a janela de saves escondendo a mensagem do save que não abre; a dica
  sumindo na rolagem), corrigidos na 1.209.0. **Exceções explícitas:** adiados por decisão do Jean (o "Continuar" da
  subida de nível, os tempos e o adiantar das faixas, o menu de configurações, a migração dos saves do mundo gerado);
  reservados (o Grimório e os Talentos, etapa 8; a narrativa, etapa 9); opcional (a dica de adiantar e o fio de leitura).
- **A etapa 3 começada (protótipo, aguardando o Jean):** o levantamento da forja e duas direções, A · a bancada de
  trabalho e B · o interior da oficina, no jogo pelo sistema de ambientes da capela (`ferramentas/prototipos/hud/forja/`,
  `folha-forja.png`, `demo.bat` na porta 8775, campanha temporária). Recomendação: B. Sem integração; o reforço e o
  encantamento (etapa 4), outros interiores, o Grimório e a expansão narrativa não começaram.

### 25/10/2026 (data do computador local) — A forja: a B refinada (R), com o ferreiro forjando (protótipo)

- **O Jean escolheu desenvolver a B** (A e B ficam como histórico). A candidata R em
  `ferramentas/prototipos/hud/forja/forja-r.js` (LEIA-ME, seção "A B refinada (R)"; `folha-forja-r.png`, B × R no jogo;
  `folha-movimento.png`, as poses e o ciclo; `demo.bat`, porta 8775): a oficina por zonas (a entrada fria, a tina, a
  bigorna e os martelos, a fornalha com o carvão, as tenazes e a fuligem, o armazém) e o ferreiro novo, gordo, de barba
  grande e cabelo grisalho, forjando uma espada num ciclo de 5,3 s (o alto segurado, a descida rápida, o golpe com o
  tronco afundando, as faíscas no contato, o rebote, a pausa da tenaz); com movimento reduzido, a pose parada.
- **Pesquisa:** o André de Dark Souls (um GIF do Tenor) e o Blacksmith Craft da Craftpix, observados quadro a quadro;
  as outras referências só pela página, registradas como tal.
- **Conferido no jogo** nas duas janelas (os pontos, os cartões, o reforço, a saída e a volta, sem relógio novo ao
  entrar de novo, o movimento reduzido). **Aguarda o Jean; nada integrado.** Não começados: o reforço/encantamento,
  outros interiores, o Grimório, a expansão narrativa; a etapa 2 segue concluída.

### 25/10/2026 (data do computador local) — A forja F: a transposição fiel da referência (protótipo)

- **O pedido:** o Jean gostou do ritmo e da fluidez da R, não do desenho do ferreiro, e mandou uma imagem gerada como a
  referência principal da aparência (guardada sem alteração em `ferramentas/arte/referencias/forja/`, com a origem e o
  hash no LEIA-ME de lá). A R continua a referência do ritmo e da demonstração.
- **A candidata F** (`ferramentas/prototipos/hud/forja/forja-f.js` e `f/`; LEIA-ME da forja, seção "A transposição fiel
  (F)"; `folha-forja-f.png`, referência × F e R × F no jogo; `folha-movimento-f.png`; `demo.bat`, porta 8775, o botão F
  primeiro): a composição da referência num quadro de 320×96 (as paisagens são 72; a vista cresce na proporção, só no
  cenário da demonstração), o fundo pela redução da referência limpa em superpixels, o ferreiro desenhado à mão em
  grades (careca, gordo e forte, o rosto separado da barba, a barba em mechas afunilando numa trança com a presilha, o
  avental na barriga; as mãos simples, sem dedos, e o antebraço da tenaz grosso, pedidos do Jean durante a entrega),
  as poses refeitas à mão na linha do tempo da R (53 quadros de 100 ms). Fonte em camadas: `f/aseprite/forja-f.aseprite`
  (o `desenhar_f.py` não a sobrescreve sem `--refazer`; o `exportar_f.py` tira dela as camadas do jogo).
- **Conferido no jogo** nas duas janelas (os pontos e os nomes fora do ferreiro, os cartões, o reforço, a saída e a
  volta, o Esc, sem relógio novo, o movimento reduzido; dois ciclos fotografados quadro a quadro: um relógio só, a
  100 ms). A 1280, sobram 15 px de rolagem abaixo dos cartões (à vista). **Aguarda o Jean; nada integrado.** Não
  começados: o reforço/encantamento, outros interiores, o Grimório, a expansão narrativa.

### 25/10/2026 (data do computador local) — A forja G: a F corrigida, na arte do jogo (protótipo)

- **O pedido:** a F não foi aprovada. O Jean manteve o design do ferreiro e pediu a animação corrigida (os pés no chão,
  as pernas ligadas, a mão presa à tenaz e à espiga, a lâmina parada) e o cenário reconstruído na linguagem dos
  ambientes aprovados (a capela, a prisão da Ilse, a cidade, o mercado). A imagem gerada vale só para a composição.
- **A candidata G** (`ferramentas/prototipos/hud/forja/g/`, `forja-g.js`; LEIA-ME da forja, seção "A G"; as folhas
  `folha-forja-g.png`, `folha-estilo-g.png`, `folha-correcoes-g.png`, `folha-movimento-g.png`; `demo.bat`, o botão G
  primeiro): as causas dos defeitos achadas na F e corrigidas (o tronco dividido no cotovelo, as botas menores longe do
  toco, a tenaz parada e presa à mão); a oficina inteira redesenhada em `g/oficina_g.py`, sem nada da redução; a coifa
  simétrica, sem objetos no ar e com as mãos-francesas do esteio até a viga (correções do Jean no caminho). A F fica
  como estava.
- **Conferido no jogo** nas duas janelas (os pontos, os cartões, o reforço, a saída e a volta, o Esc, sem relógio novo,
  o movimento reduzido; dois ciclos quadro a quadro, um relógio só a 100 ms; sem rolagem vazia a 1280). **Aguarda o
  Jean; nada integrado.** Não começados: o reforço/encantamento, outros interiores, o Grimório, a expansão narrativa.

### 25/10/2026 (data do computador local) — A forja H: o ferreiro no estilo do jogo, o corpo inteiro animado (protótipo)

- **O pedido:** na G, as pernas se descolavam e a metade de cima deslizava sobre a de baixo; o Jean pediu uma animação
  de corpo de verdade e o ferreiro conferido com o estilo do mercador e da Ilse.
- **A candidata H** (`ferramentas/prototipos/hud/forja/h/`, `forja-h.js`; LEIA-ME da forja, seção "A H"; as folhas
  `folha-forja-h.png`, `folha-estilo-h.png`, `folha-corpo-h.png`, `folha-movimento-h.png`; `demo.bat`, o botão H
  primeiro): o ferreiro em três tons chapados sem contorno (o padrão da FIGURA do mercador), cada pose redesenhada
  inteira a partir dos apoios parados (as botas, a luva na tenaz): os joelhos dobram, o quadril desce, o tronco inclina,
  a barriga achata, a trança balança. Correções do Jean no caminho: a perna quadrada sobre a bota e o bloco da túnica.
- **Conferido no jogo** nas duas janelas (tudo certo; um relógio só; sem rolagem vazia). **Em aberto, decisão do
  Jean:** o ferreiro (~55 px, a escala da referência) é bem maior na tela que a Ilse e o mercador. **Aguarda o Jean;
  nada integrado.** Não começados: o reforço/encantamento, outros interiores, o Grimório, a expansão narrativa.

### 25/10/2026 (data do computador local) — A forja H aprovada em parte, a H2 (o olho) e a skill de interiores

- **O Jean aprovou na H** a oficina, o enquadramento, o corpo, a barriga, o estilo e o movimento, e manteve a escala do
  ferreiro. **A H2** (`ferramentas/prototipos/hud/forja/h2/`, `forja-h2.js`, `folha-rosto-h2.png`; `demo.bat`, o botão
  H2 primeiro) ajusta só o olho: um pixel mais para trás, a órbita entre a ponte do nariz e o olho, decidido no tamanho
  real nas poses do alto, do golpe e do rebote. Conferida no jogo nas duas janelas. **Aguarda o Jean; nada integrado.**
- **A skill `arte-cenas-fenda`** (`.claude/skills/arte-cenas-fenda/SKILL.md` e `forja.md`): o processo dos interiores e
  dos personagens animados de cena (as três aprovações, o levantamento, a referência de composição separada da de
  acabamento, a construção do ambiente, a escala por enquadramento, a animação pelos apoios, as fontes e a validação,
  os erros da forja). A skill de itens aponta para ela. A taverna é um uso futuro; a ordem do plano não mudou (depois
  da forja, a etapa 4, o reforço e o encantamento).

### 25/10/2026 (data do computador local) — A forja H2 no jogo (1.210.0); a etapa 3 concluída

- **O Jean aprovou a H2 para integração.** No jogo desde a 1.210.0: a oficina, o ferreiro e o rosto da H2, as poses, o
  ritmo, o fogo e as faíscas, os pontos Ferreiro (leva aos cartões de reforço) e Saída (o Voltar), o balcão compacto.
  O motor manda a cena antes do balcão (`servicos.cena_forja`); a arte vem em camadas prontas (`static/cenas/forja/`,
  `telas/cena-forja.js`) exportadas da fonte da H2 (`exportar_h2.py --jogo`); a vista aceita o quadro de 96 só para
  essa cena (`vista.js`, `css/26-forja.css`). O jogo não carrega nada do protótipo. Preços, ganhos, o limite +5 e as
  regras do reforço não mudaram.
- **Conferido:** a produção desenha os mesmos 53 quadros da H2, em sequência, a 1920×945 e a 1280×720; o roteiro de
  fotos da forja (pontos, cartões, reforço de verdade, saída, volta, Esc, Tab, movimento reduzido, sem relógio novo, sem
  rolagem vazia); as outras cenas com a altura de sempre; a suíte; o gabarito (as 9 partidas da tela gráfica mudaram só
  pelo painel novo da cena da forja: tirando essas linhas, batem com o gravado; atualizado); a fumaça.
- **Próximo:** a etapa 4 (reforço e encantamento), começando pela pesquisa e pela proposta de design, sem regra nova.

### 25/10/2026 (data do computador local) — A etapa 4 começada: a pesquisa e a proposta do reforço e do encantamento

- **O documento:** [25 — Etapa 4](25-ETAPA4-REFORCO-E-ENCANTAMENTO.md). O jogo de hoje (confirmado no código): o
  reforço em 3 espaços, +1 a +5, sem falha, sempre **+1 por nível** no intervalo da campanha, 1.283 de ouro por peça
  (a partida do Jean que fechou a região terminou com ~400), perdido ao trocar ou vender; nenhum encantamento ou
  material. A pesquisa (cinco jogos e o Místico do Diablo III, com as fontes e as versões) e a satisfação sem alegação
  neurológica.
- **A recomendação (arquitetura A):** o reforço melhora a base inteira da peça (hipótese 20% por nível, mín. +1),
  garantido, mais barato (hipótese 25–140), e passa para a peça nova do mesmo espaço; o encantamento grava uma
  essência escolhida (os 11 afixos que já existem, tirados de desmanchar peças incomuns e raras, mais 6 de
  especialização achados na campanha), uma por peça, trocável, contando uma vez só no corpo. Sem falha, destruição ou
  perda.
- **Aguarda as decisões do Jean** (seção 9: a arquitetura, os espaços, a regra do ganho, a passagem do reforço, o
  desmanche, as essências de especialização, onde mora o encantamento, os custos). Nada implementado; nenhum número
  integrado; outros interiores não começaram.

### 25/10/2026 (data do computador local) — A forja: a tina na frente do esteio (1.210.1)

- O Jean notou o esteio do meio passando na frente da tina d'água, que está mais perto de quem olha. Causa: no fundo, a
  tina era desenhada antes dos esteios. Corrigida a ordem na fonte (`h2/oficina_h2.py`), a fonte refeita
  (`desenhar_h2.py --refazer`, sem retoque no Aseprite a perder) e as camadas do jogo reexportadas (`exportar_h2.py
  --conferir --jogo`, 53 de 53). Conferido no jogo; suíte, gabarito, pyflakes e fumaça. Só a arte do fundo mudou.

### 25/10/2026 (data do computador local) — O protótipo isolado do combate e dos atributos

- **O que é:** uma luta jogável com a direção das seções 1 a 8 do [25](25-ETAPA4-REFORCO-E-ENCANTAMENTO.md), em
  `ferramentas/prototipos/combate-atributos/` (`demo.bat`, porta 8781). O jogo não carrega nada dele (um teste confere);
  as regras de produção, a forja e a campanha não mudaram. Detalhes, fórmulas e achados no
  [LEIA-ME](../ferramentas/prototipos/combate-atributos/LEIA-ME.md).
- **As regras testadas:** Jean, Odette e Morel controlados diretamente; ordem pela Agilidade calculada uma vez
  (desempate: Percepção, aliado, entrada); uma ação por turno; rodada fechando depois de todos, inclusive quem perdeu a
  vez; Defender até o início do próximo turno; ameaças anunciadas numa vez do inimigo e resolvidas na seguinte, com
  alvo, dano previsto e quando; caído pulado, volta por Reerguer ou Pena de Fênix na mesma posição, sem recuperar a
  vez; invocações no fim da ordem, agindo na rodada seguinte.
- **Os atributos (provisórios):** escala 1–8, 24 pontos do protagonista, limiar 5. Nenhum soma dano direto (a
  potência é arma + nível × habilidade): Força rompe guarda e aguenta atordoar; Agilidade só a ordem; Constituição
  vida e sangramento; Intelecto custo; Percepção crítico e ponto fraco; Vontade defesa e terror; Presença o Comando.
  Três construções (A Força/Constituição, B Agilidade/Percepção, C Vontade/Presença) e uma livre, com o mesmo nível,
  equipamento e companheiros; Comparar e Resultados mostram o que mudou.
- **Conteúdo:** três encontros com semente (os lobos e o Bote; o Bruto e o Golpe Esmagador com dois besteiros; o
  xamã com afogados e o Grito de Terror, e o Soldado Morto com guarda), quatro casos de teste com a condição
  artificial na tela (atordoado, retorno antes e depois da posição, inimigo derrubado antes da preparação) e uma
  situação fora da luta com a contribuição dos companheiros.
- **Conferido:** 26 testes dirigidos; o roteiro do navegador a 1920×945 e a 1280×720 (sem rolagem nem corte,
  teclado, tecla segurada, clique duplo, reinício, movimento reduzido) com as capturas e a `folha.png`; o encontro 2
  jogado à mão com a B e os três medidos por um jogador automático em três estilos.
- **Achados para o Jean avaliar:** a ameaça anunciada abre várias respostas reais; o Golpe no Joelho era dominante a
  20 e foi a 30; o recurso decide quando gastar; C sofre no encontro 2 se não defender e comandar na hora; o encontro
  3 é o mais leve. Nada disso é balanceamento.
- **A etapa 4 não está concluída.** Aguarda a avaliação do Jean do protótipo e as decisões do 25 antes de reforço e
  encantamento; nada a integrar.

### 26/10/2026 (data do computador local) — A segunda versão do protótipo de combate e atributos

- **Por quê:** o Jean jogou a primeira, gostou do combate e aceitou lutas mais longas, mas guardou recurso com o ataque
  básico e não sentiu a diferença entre as builds. A revisão da seção 3.7 do [25](25-ETAPA4-REFORCO-E-ENCANTAMENTO.md)
  (commit `9d6f1860`) virou a segunda versão, isolada, em `ferramentas/prototipos/combate-atributos/` (`motor2/`,
  `tela2/`). A primeira continua jogável ao lado (`/v1/`), com as regras congeladas.
- **Decisões aplicadas:** Força e Intelecto entram direto no dano; sem desbloqueio por pontuação; benefícios graduais
  com tetos; Presença fora do orçamento e sem efeito de combate; Tenacidade com teto e chance mostrada; kit com pontos
  por tier e até uma ultimate; Atacar, Defender e Usar item fora do kit (hipótese desta iteração).
- **Hipóteses implementadas (provisórias):** a escala 1–10 e 30 pontos; as fórmulas, o recurso (começa com 40, +8 por
  turno e +8 no básico), o Ímpeto da ultimate, a interrupção uma vez por inimigo, quatro builds de teste e a comparação
  de uma peça. Os inimigos ganharam vida e um pouco de dano (registrado no LEIA-ME, para não creditar a uma build).
- **Conferido:** 53 testes do protótipo (26 da v1, 27 da v2); os dois roteiros do navegador a 1920×945 e a 1280×720
  (teclado, tecla segurada, clique duplo, reinício, movimento reduzido); partidas à mão com Precisão, Baluarte e Runa;
  medição automática em três estilos (sem reserva, com reserva, ignorando ameaças).
- **Observado:** as builds mudam a escolha na mesma luta; gastar cedo não deixa sem resposta à primeira ameaça e cria
  custo na segunda; guardar só alonga. A observar: Percepção contra ponto fraco quase empata com Força; o encontro 1
  curto; o Baluarte longo; a hora do Juramento.
- **Para o Jean:** o [ROTEIRO](../ferramentas/prototipos/combate-atributos/ROTEIRO.md) do que comparar e a
  `folha-v2.png`. **A etapa 4 não está concluída**; nada a integrar.

### 26/10/2026 (data do computador local) — A terceira versão do protótipo de combate e atributos

- **Por quê:** o Jean jogou a v2: sentiu mais a diferença entre builds (sobretudo pelo kit), gostou do guerreiro de dano
  sobrenatural, achou o Baluarte válido e rejeitou o Ímpeto (não conseguiu usar a ultimate). A seção 3.8 do
  [25](25-ETAPA4-REFORCO-E-ENCANTAMENTO.md) (commit `6d5b6c80`) virou a v3, isolada (`motor3/`, `tela3/`), com a v1 e a
  v2 jogáveis ao lado (`/v1/`, `/v2/`).
- **Investigado primeiro:** as lutas contra o Bruto com zero preparações no arquivo do Jean. Causa reproduzida: na v2 a
  preparação estava presa ao número da rodada, e os atordoamentos nessas rodadas (o Bruto é o último da ordem)
  apagavam o ciclo. Havia também uma lacuna de telemetria (controles em inimigos não contados). O atordoamento "100%" do
  Morel batia com 5% de chance de resistir. A regra "firme depois da primeira interrupção" foi retirada.
- **Decisões aplicadas:** tipo, escala e defesa por habilidade; resistências por tipo com teto (arcano e fogo), do
  equipamento, separadas da Tenacidade; o Avanço do Baluarte pela vida máxima; Vontade na reserva; reserva e
  regeneração distintas; Brasa e Combustão numa especialização de demonstração que soma ao Guerreiro; ultimate sem
  Ímpeto, uma vez por luta, desde o início, com recurso.
- **Hipóteses numéricas:** listadas no LEIA-ME e no 25 (preparação por turno agido, golpe ininterruptível sinalizado do
  Bruto furioso, ordem de cálculo, coeficientes, recurso, Queimadura de 3 pingos, ultimate de 30). Inimigos alterados e
  por quê: tabela no LEIA-ME; novo encontro 4 (Cães de Brasa, fogo 60%) e testes t5 (ultimate, queda e retorno) e t6
  (combinação num alvo parado).
- **Conferido:** 74 testes do protótipo (26 da v1, 27 da v2, 21 da v3); os três roteiros do navegador a 1920×945 e a
  1280×720; partidas à mão (Baluarte no encontro 2, Chama no 3) e comparações controladas (o manto no encontro 4, a
  Constituição no Avanço, a ultimate na abertura ou na hora).
- **Para o Jean:** o [ROTEIRO](../ferramentas/prototipos/combate-atributos/ROTEIRO.md) e a `folha-v3.png`. **A etapa 4
  não está concluída**; nada a integrar.

### 26/10/2026 (data do computador local) — A quarta versão do protótipo de combate (refinamento da v3)

- **Pedido:** a seção 3.9 do [25](25-ETAPA4-REFORCO-E-ENCANTAMENTO.md) (commit `1a6135e8`): registrar a leitura dos
  ataques básicos, retirar a Marca do Morel e completar o conjunto de fogo com uma habilidade de área. Na conversa, o
  Jean pediu também uma habilidade nova para o Morel no lugar da Marca.
- **Feito:** `motor4/` e `tela4/` (a v4 abre na raiz; a v3 em `/v3/`, intacta). Sem a Marca; o Golpe Oportuno do Morel
  (+60% em quem está atordoado ou preparando); a Chuva de Brasas (pouco fogo em área e uma camada de Queimadura em cada
  inimigo, 22 de recurso, tier 2). Brasa, Combustão e Conflagração ficaram como na v3, que já cumpria os papéis.
  Recurso, duração e os outros encontros não mudaram por causa dos básicos finais.
- **Conferido:** a comparação do fogo jogada de verdade (um alvo, grupo, resistência: ações, custo, direto,
  periódico, total), aparecendo em Preparar; 85 testes do protótipo (11 da v4); o roteiro do navegador da v4 a
  1920×945 e a 1280×720, e os da v3, v2 e v1 nas rotas novas.
- **Para o Jean:** o [ROTEIRO](../ferramentas/prototipos/combate-atributos/ROTEIRO.md) e a `folha-v4.png`. **A etapa 4
  não está concluída**; nada a integrar.

### 26/10/2026 (data do computador local) — O combate integrado na campanha (1.211.0)

- **Pedido:** a seção 3.10 do [25](25-ETAPA4-REFORCO-E-ENCANTAMENTO.md) (commits `196572af`, `bdf80b48`): a estrutura
  aprovada do protótipo dentro da campanha, com um repertório provisório por classe, a continuidade entre lutas, o
  ritmo e a escrita das regras. Tudo no [26](26-INTEGRACAO-DO-COMBATE.md): escolhas, conversões, catálogo, combos,
  medidas, o gabarito e o roteiro de teste.
- **Feito no jogo:** ordem fixa pela Agilidade e rodadas (a placa mostra a ordem); Defender; a vez de Odette, Morel e
  Yara com a roda (recurso próprio, kit fixo, Reerguer); a Pena de Fênix num companheiro caído; o kit (8 pontos, 5
  espaços, uma ultimate) no Grimório, na vila e na fogueira; a ultimate uma vez por luta, desde o nível 6; os seis
  atributos e a Presença, com pontos para distribuir na ficha; os testes do d20 pelos atributos; o recurso cheio no fim
  de cada luta; a debandada nas lutas comuns; o fogo do Piromante (Brasa, Combustão, Chuva de Brasas, Conflagração;
  saíram Inferno e Fênix); o caminho rúnico do Guerreiro (Lâmina e Égide Rúnicas); saves no formato 7.
- **Escrita:** a skill `texto-regras-fenda` (.claude/skills), com fontes (Slay the Spire em PT-BR, Path of Exile em
  PT-BR oficial), critérios, vocabulário e antes/depois; o catálogo inteiro revisto contra o comportamento (o Tiro
  Imobilizador dizia "prender" e atordoava; "defesa de o alvo"; durações sem dono; a Prece de Odette não dizia que limpa
  os males).
- **Medido e corrigido:** sem a esquiva da Agilidade, a Sombra caía de 89% para 60% de vitórias; a esquiva voltou, o
  crítico do herói passou para a Percepção (Arqueiro com mais Percepção, Sombra com +6% de crítico). Com comitiva, os
  caminhos ficaram perto de antes; o Necromante contra guardiões cai (64% → 50%: Fênix fora, ultimate uma por luta),
  registrado para decidir. O gabarito achou o recurso inicial pela metade (corrigido).
- **Conferido:** 707 testes (18 novos da integração), o gabarito atualizado (24 partidas, motivos no 26), pyflakes, a
  fumaça; as telas a 1920×945 e 1280×720, teclado e movimento reduzido; os 38 saves do Jean migrados só em leitura.
- **Para o Jean:** o roteiro no [26](26-INTEGRACAO-DO-COMBATE.md#roteiro-de-teste-para-o-jean). **A etapa 4 continua
  aberta** (reforço e encantamento completos não começaram).

### 26/10/2026 (data do computador local) — Ajustes depois do teste do Jean (1.212.0) e a proposta da comitiva

- **Pedido:** o retorno do Jean sobre a integração: a Queimadura contra resistência, a leitura das descrições, os
  atributos e o kit à vista, a debandada menos frequente, o Golpe Pesado (observar), e a proposta de gerenciamento da
  comitiva no protótipo.
- **Integrado (1.212.0):**
  - **Queimadura:** a regra antiga (resistência abaixo de 0,5 tornava imune; o tique ignorava a resistência) estava no
    código e no texto. Agora pega em todos, salvo imunidade explícita; a resistência reduz o tique e a detonação, uma
    vez cada.
  - **Leitura:** resumo à vista e "Como é calculado" no Grimório; a carta da luta sem o crítico; a dica de atributo
    pelo que ele dá agora; crítico e Tenacidade com dica própria. A skill `texto-regras-fenda` ganhou os critérios.
  - **Ficha lateral:** o botão "Atributos" (· +N com pontos), com o quadro dos atributos (a linha fixa apertava o
    painel). **Kit na barra:** a fileira do kit (recolhe em "Kit · N" na janela estreita); o clique abre o Grimório, que
    só troca na vila e na fogueira.
  - **Debandada:** no fim da rodada, com a luta decidida e os que sobram inofensivos; 50% por rodada. Quem foge dá XP,
    mas não ouro, espólio nem abate (antes contava como abate e dava espólio). Frequência nas mesmas lutas: 81% → 6%
    (`python -m tests.debandada`).
  - **Golpe Pesado:** sem mudança; a repetição vem da economia do recurso (registrado no 26).
- **Proposta (fora do jogo):** `ferramentas/prototipos/comitiva-gerenciamento/` (abas com retratos, a bolsa do
  grupo, o equipamento de cada um e a comparação com o selecionado, as dependências reais, a regra proposta para os
  atributos dos companheiros). Aguarda avaliação.
- **Provisório, sem compensação neste lote:** a esquiva da Agilidade, o crítico da Sombra, o orçamento do kit, o
  Necromante contra guardiões. Os limites das medidas estão no [26](26-INTEGRACAO-DO-COMBATE.md#limites-das-medidas-anteriores).
- **Conferido:** os testes (24 da integração), o gabarito (motivos no 26: só apresentação), pyflakes, a fumaça; as
  telas a 1920×945 e 1280×720.

### 26/10/2026 (data do computador local) — A comitiva no Inventário e os refinamentos da HUD (1.213.0)

- **Pedido:** integrar o gerenciamento da comitiva aprovado (com os ajustes de interação) e refinar a HUD: o botão
  Atributos, a Agilidade 3 e 4, o kit na barra.
- **Integrado:**
  - **Janela do grupo:** o Inventário com as abas de retrato; bolsa do grupo (os mesmos 12); equipamento individual;
    comparação com o selecionado; um clique escolhe, dois equipam, o botão direito abre o menu, arrastar funciona; tudo
    por uma regra única no motor (`comitiva/ficha.py`), com troca inteira ou nenhuma.
  - **Atributos dos companheiros:** iniciais pela identidade, 1 ponto livre por nível do herói, a sugestão só quando o
    jogador pede. As peças e os pontos valem na luta (incluindo os bônus especiais).
  - **Saves no formato 8;** quem sai da comitiva devolve as peças à bolsa (o que não cabe vira achado).
  - **Agilidade:** a causa (três conceitos com um nome) e as dicas com a conta; **Atributos** com o acabamento dos
    Testes do d20; **kit** em quadrados da HUD, recolhendo só quando transborda.
- **Provisório:** os atributos iniciais e o ponto por nível dos companheiros; a classe de peças de cada um.
- **Conferido:** os testes (15 novos da comitiva), o gabarito (motivos no 26), pyflakes, a fumaça; as telas a
  1920×945 e 1280×720. Roteiro curto no [26](26-INTEGRACAO-DO-COMBATE.md#roteiro-de-teste-1213-uns-5-minutos).

### 26/10/2026 (data do computador local) — Protótipo de reforço, materiais e desmontagem (etapa 4)

- **Pedido:** um protótipo jogável para investir numa peça, sentir a melhora, comparar uma substituta e decidir entre
  manter, passar a um companheiro, vender ou desmontar (25, seções 4 e 5, commit 01f4521e do Jean).
- **Feito (isolado, sem integração):** `ferramentas/prototipos/reforco/` (`demo.bat`): o jogo num save temporário, a
  forja com o balcão novo (a peça, o passo, o custo, a posse e a falta, a comparação na luta, a substituta, a venda e a
  desmontagem com confirmação), a seção Materiais no Inventário, a recompensa de teste e o baú como fontes.
- **Hipóteses (provisórias):** arma/peito/apoio; Fio ou Runas na arma do Guerreiro; 1,5 nível de peça por +, piso
  de +1 na arma; limite +4; 305 de ouro e 10 fragmentos até o +4; desmontar devolve metade dos fragmentos e o da
  peça; vender devolve 25% do ouro. Detalhes no LEIA-ME e no 25 (5.5).
- **Para depois:** elevação de base (exemplo numérico), encantamento, arte e som, fontes na campanha, a aljava.
- **Conferido:** 15 testes do protótipo; a tela a 1920×945 e 1280×720 (duplo clique, confirmação, Esc, falta de
  recurso); o jogo de produção não carrega a pasta. Aguarda a avaliação do Jean antes de integrar.

### 26/10/2026 (data do computador local) — Reforço: a janela por serviço e as duas direções visuais (protótipo)

- **2ª versão:** depois do teste do Jean (a página rolava, a arte piscava, ouro e fragmentos sumiam), cada serviço
  abre uma janela própria sobre a coluna do meio; o pisca saiu com o recolhimento da arte.
- **3ª versão:** a mesma estrutura em duas direções, A · Bancada e B · Arsenal, com planos de ferro, encaixes e
  botões de estados claros; escrita de interface (rótulo e número); "Encantar" fora até existir; a comparação de
  teste fechada e marcada. Pesquisa visual em Soul Knight Prequel e Elona Mobile (registrada no LEIA-ME). v1 e v2
  guardadas em `tela/historico/`. Regras e números iguais. Aguarda a avaliação visual do Jean antes de integrar.

### 26/10/2026 (data do computador local) — Reforço: a A · Bancada escolhida e refinada (protótipo)

- **Decisão do Jean:** a direção A · Bancada. A A anterior e a B ficam em `tela/historico/v3`.
- **Candidata em avaliação (4ª versão):** a chapa rebitada com os encaixes ligados (materiais → peça no suporte →
  resultado) e a ação no pé; a ficha mais larga só com nome, dono e propriedades (a afetada destacada pelo valor); Fio e
  Runas como as duas opções do visor; as marcas só contam o reforço; "Reforço máximo +4" sem botão; a confirmação no
  ferro (Cancelar · Desmontar, o vermelho no aviso e na ação); o retorno curto do reforço.
- **Conferido** a 1920×945 e 1280×720: o fluxo com recursos (um passo por ação, custo e próximo preço, seleção e foco
  mantidos), Fio e Runas, falta, limite, nome longo, seleção vazia, desmontar cancelado e confirmado. Não integrado.

### 26/10/2026 (data do computador local) — Reforço: a regra muda para chance (decisão do Jean)

- **Direção aprovada:** o reforço deixa de ser garantido (25, 5.6). O primeiro é garantido; os seguintes têm chance
  que cai com o nível pretendido e, menos, com a raridade; sucesso +1, falha −1 (não abaixo de +0); a peça nunca
  quebra; afixos, especiais e Fio/Runas ficam. As regras do reforço garantido ficam como histórico, substituídas.
- **Nesta rodada (protótipo, nada em produção):** percentuais e custos recalibrados, animação de aquecimento, sucesso e
  falha na bancada, acabamento e clareza dos estados. Resultados no fim desta entrada quando prontos.
- **Feito (5ª versão do protótipo):** chances 100/85/70/55% (−4 por raridade), 20/35/55/80 de ouro e 1/1/2/2
  fragmentos por tentativa (simulação no LEIA-ME: mediana de 6 a 10 tentativas de +0 a +4; no 90%, 14 a 24); a cena de
  forja com sucesso e falha, adiantável e resolvida uma vez; a chapa, o molde e os condutos refeitos; casos de teste
  na faixa. 22 testes; conferido a 1920×945 e 1280×720. Aguarda avaliação; não integrado.

### 26/10/2026 (data do computador local) — Reforço: a 6ª versão da bancada (protótipo)

- **Pedido:** refinar a bancada só no protótipo, sem mudar chances, custos e consequências da 5ª: os dados mais
  diretos e um desfecho com presença. Retomada de uma sessão interrompida (o trabalho estava só no disco).
- **Feito:** materiais como ícone e quantidade; "+1 → +2", o ganho e a chance numa linha; a ajuda (i) com a falha e o
  custo por tentativa; Ataque ou Poder na arma do Guerreiro; a cena com aquecimento e o desfecho pela FX do Estouro
  ("SUCESSO +N" / "FALHOU +N"), recortado no leito, mais forte no +3 e no +4; a volta à próxima oferta. A 5ª fica em
  `tela/historico/v5`.
- **Corrigido na conferência:** o clarão pontilhado que cobria a bancada (o impacto ficou em volta da peça e do
  resultado), o nome da ficha que mostrava o nível novo no aquecimento, o Enter que não adiantava a cena.
- **Conferido:** sequência contínua de sucesso e falha a 1920×945 e 1280×720, cobrança única, os dados da mesma
  tentativa em todos os quadros, falta, reforço máximo, movimento reduzido, teclado e mouse; folha nova. Aguarda a
  avaliação visual do Jean; não integrado.

### 26/10/2026 (data do computador local) — Reforço: a 7ª versão da bancada (protótipo)

- **Pedido:** corrigir composição, estados e efeitos da candidata, sem mudar regras, chances, custos nem o limite +4.
- **Candidata (7ª versão):** nível, peça, chance e Reforçar num eixo (medido igual em todos os estados, nas duas
  resoluções); a mesma bancada em oferta, cena, falta, máximo e peça sem reforço; na cena, os dados da tentativa e os
  valores de antes na ficha; sem a faixa do resultado; ficha compacta; a comparação de teste na faixa do protótipo;
  efeitos soltos além da bancada, com a leitura por cima; falha sóbria; movimento reduzido parado com selo e
  contorno; o reflexo do reforço na silhueta da peça (+1 claro, +2 verde, +3 azul, +4 dourado). A 6ª fica em
  `tela/historico/v6`.
- **Ideias registradas (não feitas):** laranja para um eventual +5; luz numa borda própria para o encantamento.
- **Conferido:** a sequência real até o máximo a 1920×945 (mouse) e 1280×720 (teclado), cobrança única, nada revelado
  antes da hora, o efeito sem interceptar cliques, falta, máximo, movimento reduzido; folha nova. Referências (Epic
  Seven, Ragnarok Origin, Guardian Tales) aplicadas pelos princípios indicados: não achei capturas nesta rodada.
  Aguarda a avaliação visual do Jean; não integrado.
- **Ajuste pedido pelo Jean (7ª versão):** o reflexo passa em todo slot da peça reforçada (forja, Inventário, ficha
  lateral), sozinho: 2 s depois de a peça aparecer e então a cada ~3 s, defasado entre as peças; parado com movimento
  reduzido; pausado durante a cena. Só na demonstração.

### 27/10/2026 (data do computador local) — Forja: a 8ª versão e o encantamento de laboratório (protótipo)

- **Pedido:** dois lotes, sem parar no plano: o acabamento do reforço e da desmontagem (regras, chances, custos e +4
  iguais) e um protótipo jogável de encantamento (proposta de laboratório). Durante a rodada, o Jean decidiu: as peças
  podem ter mais de um espaço de gravação, sorteado no drop; a ordem é Reforçar, Encantar, Desmontar.
- **Lote 1 (feito):** a desmontagem na mesma bancada (eixo e dimensões do reforço), a confirmação no pé, a
  transformação em fragmentos e a seleção vazia depois; o golpe seco no +3/+4, o contorno aceso do máximo, a falha
  legível a 1280, o desfecho dominando, o reduzido assentado; o reflexo nos níveis reais, como luz no material, e a
  luz baixa do +4; sons do jogo (não ouvidos). Corrigidos: a desmontagem de peça única e o clique duplo que atravessava
  a janela num redesenho. Na produção, só o Inventário sem a instrução (1.213.2).
- **Lote 2 (hipóteses):** Encantar na forja; sulcos de 1 a 3; 1 essência + 30 de ouro, sem falha; substituir apaga o
  sulco, com confirmação; seis essências (Brasa, Carrasco, Eco, Vigília, Revide, Geada) ligadas à luta só na
  demonstração; a borda de luz por gravação; a luta de teste na faixa. Regras no 25 (5.7) e no LEIA-ME.
- **Conferido:** 34 testes do protótipo; a 1920×945 e 1280×720, cobrança única, fechar no meio sem repetir, teclado,
  clique duplo, reduzido; folhas `folha.png` e `folha-encantar.png`. Nada integrado; a avaliação é do Jean.

### 27/10/2026 (data do computador local) — Forja: a 9ª versão, consistência visual e de interação (protótipo)

- **Pedido:** corrigir defeitos de uso (sprite borrado, efeito do reforço sumindo, tremor que não reinicia), mostrar os
  sulcos nas fichas, arrumar o texto do encantamento, atualizar a skill de texto, retirar a peça da bancada, refinar a
  borda luminosa; sem mudar regras nem redesenhar a bancada.
- **Corrigido (causas no LEIA-ME e no 25, 5.8):** a regra da HUD que deixava o desenho em `auto`, esticado a 1,8×; as
  telas que liam o "+N" no nome (a peça única não termina nele); o impacto que dependia de atraso zero do temporizador;
  os sulcos nas fichas e dicas (achado, Inventário, Equipado, mercado, forja), sorteados uma vez; o texto e a altura fixa
  do encantamento; retirar a peça; a borda em pixel; a linha de raridade após desmontar; a forja parada na luta de teste.
- **Skill:** `texto-regras-fenda` com os critérios gerais (×N, custo junto da ação, efeito/condição/limite, sem repetir,
  mesmos termos, alinhamento) e exemplos.
- **Conferido:** 36 testes do protótipo; a 1920×945 e 1280×720, a reprodução completa do efeito, os quadros nítidos,
  mouse, teclado e movimento reduzido; folhas novas. Nada integrado.

### 27/10/2026 (data do computador local) — Forja: a 10ª versão, a bancada com o título e o resultado até o OK (protótipo)

- **Pedido:** uma candidata pela referência do Jean (sem a ficha lateral; nome com o nível, dono e sulcos no topo; a
  chance e a falha junto da ação), o impacto do nível (entorno escurecido, contenção, número como marca quente), o
  resultado mantido até OK/Enter/Esc e as pendências de interação e dados; sem mudar regras, sem 3×, sem som, sem vídeo.
- **Corrigido (causas no LEIA-ME e no 25, 5.9):** retirar pela miniatura; o texto de compatibilidade; rastros mais
  longos; o efeito que piscava (a aparência só voltava no ciclo seguinte ao redesenho); as dicas pela peça exata, nunca
  pelo nome; os sulcos nascendo com a peça (o mercado e o saque importavam a criação pelo nome); os sulcos no achado; o
  véu da cena que escurecia a bancada junto.
- **Conferido:** 37 testes do protótipo; a 1920×945 e 1280×720, a sequência contínua da mesma tentativa, os gestos,
  casos (nome longo, peça única, máximo, falta), movimento reduzido, peças homônimas, saque real, salvar e carregar pela
  interface; folhas novas. A 9ª em `tela/historico/v9`.
- **Adiado:** a revisão de som, para quando a interface estiver satisfatória como 1.0.
- **Próximo:** a avaliação do Jean. Nada integrado.

### 27/10/2026 (data do computador local) — Forja: a 11ª versão, o resultado em destaque (protótipo)

- **Pedido:** o sucesso não pode escurecer com o resto; os feixes rodando até o OK; nada da estética antiga de botão,
  nem em teste; "Sucesso" maior, embaixo, entre a peça e o OK; o molde sem o corte seco no efeito.
- **Feito (causas no LEIA-ME e no 25, 5.10):** o recorte do véu medido depois do desenho (antes ficava 0×0 e cobria
  a bancada); raios contínuos e mais calmos depois do impacto; o banner no pé; o disco em degraus no lugar do quadrado;
  `.botao-janela` em todas as ações da forja (e a colisão `#texto .perigo`). A 10ª em `tela/historico/v10`.
- **Conferido:** 1920×945 e 1280×720, sequência contínua, +3, falha, movimento reduzido, gestos; testes do projeto.
- **Depois, pelo retorno do Jean:** a linha de raridade sai do resultado de sucesso e usa as cores do jogo (o
  lendário do protótipo era roxo); a oferta com o nome do recurso de quem leva a peça (dizia sempre "Mana").
- **Próximo:** a avaliação do Jean. Nada integrado; som adiado para a 1.0.

### 27/10/2026 (data do computador local) — Forja: a 12ª versão, o resultado em destaque, o +12 e o acabamento (protótipo)

- **Pedido:**
  - o resultado separado da bancada, também na gravação;
  - **autorizado o +12** (as mesmas regras);
  - **a peça inteira melhora** (sem Fio ou Runas);
  - a progressão visual do +1 ao +12 (referência: MU Online);
  - a explosão em outras cores e mais forte nos níveis altos.
- **Feito (LEIA-ME e 25, 5.11):**
  - a apresentação do resultado na linguagem do achado (reforço e gravação);
  - a curva do +5 ao +12, com `simular.py` (percentis e os casos que não chegam);
  - o ganho linha por linha;
  - o acabamento em pixel do +5 ao +12 em todas as telas;
  - o botão "Níveis altos (teste)".
- **A 11ª** está em `tela/historico/v11`.
- **Conferido:**
  - 1920×945 e 1280×720: a sequência da mesma tentativa, +5, +10, +12, falha, gravação e substituição, gestos,
    movimento reduzido, salvar e carregar;
  - os testes do projeto.
- **Decisões abertas:** o ouro do +5 ao +12 não cabe na campanha curta (ligá-lo à renda da campanha ampliada); as
  fontes de fragmento.
- **Próximo:** a avaliação do Jean. Nada integrado; som adiado para a 1.0.

### 28/10/2026 (data do computador local) — Forja: a 13ª versão e a especificação consolidada (protótipo)

- **Pedido:**
  - reforço em todo espaço;
  - essências com tiers e repetição;
  - sulcos e fontes de material;
  - transferência de reforço;
  - fichas compactas;
  - um documento que explique o sistema inteiro.
- **Feito:**
  - **[roadmapIDEIAS/27-FORJA-ESPECIFICACAO.md](27-FORJA-ESPECIFICACAO.md):** a fonte única das regras, conferida
    contra o código, separando aprovado, protótipo, provisório, produção, adiado e substituído; o 25 aponta para ele;
  - o ganho em forma fechada, sem deriva, sem +1 imposto e com tetos de %;
  - as seis tabelas das essências de 1 a 5, com o teto de 5;
  - materiais do saque real (pela criatura) e dos chefes;
  - a aba Transferir;
  - as fichas e a skill de texto.
- **A 12ª** está em `tela/historico/v12`.
- **Conferido:** 46 testes do protótipo; as duas resoluções; os testes do projeto.
- **Decisões abertas:** o equilíbrio (chances, ouro, tabelas, teto), que o Jean vai julgar jogando; as fontes da
  campanha ampliada.
- **Próximo:** a avaliação do Jean. Nada integrado; som adiado; a etapa 4 continua aberta.


### 27/10/2026 (data do computador local) — Forja: a 14ª versão, uma janela só e a transferência entre duas peças (protótipo)

- **Pedido:**
  - o reforço que às vezes acontecia sem cena;
  - o contorno do anel por dentro;
  - a Manopla de Ferro +2 se mexendo na passada do reflexo;
  - a mesma janela para as quatro abas;
  - o Encantar em duas áreas;
  - a transferência entre duas peças, com cena curta;
  - fichas uniformes e a skill com critérios gerais.
- **Feito (LEIA-ME do protótipo e 27, seções 3.3, 8, 9 e 10):**
  - a numeração dos resultados que só cresce (os cenários de teste a reiniciavam e a tela ignorava o resultado);
  - o contorno pela silhueta de fora;
  - o reflexo sem modo de mistura (a 125% e 150% de escala, a peça parecia se mexer);
  - a janela única, com o cabeçalho só com abas, ouro e Fechar;
  - o Encantar com sulcos, família, tier e prévia pelos números do motor;
  - a mesma gravação recusada sem cobrar ("Já gravado");
  - a transferência com origem, conduto e destino, listas de escolha, a cena e o resultado até o OK;
  - fichas com o tier no sulco, o teto entre parênteses e "Detalhes" curtos; sem rodapés "Clique para…";
  - a skill `texto-regras-fenda` com os critérios gerais da rodada.
- **A 13ª** está em `tela/historico/v13`.
- **Conferido:** 47 testes do protótipo; as duas resoluções; os testes do projeto.
- **Próximo:** a avaliação do Jean. Nada integrado; som adiado; a etapa 4 continua aberta.

### 27/10/2026 (data do computador local) — Forja: a 15ª versão, tiers com potência própria e requisitos de nível (protótipo)

- **Pedido:**
  - essências: I, II e III como potências do mesmo efeito, repetição somando a propriedade que cresce até um limite
    por efeito (substitui a soma de níveis até 5);
  - requisito de nível para equipamento e para cada tier, em todos os caminhos de vestir;
  - o tier no ícone; o Encantar sem as contas antigas;
  - fichas na ordem das referências do Diablo IV que o Jean mandou;
  - o resultado do reforço enxuto; a transferência simplificada;
  - dois defeitos: o Reforçar que não respondia depois do OK e a peça tremendo no resultado.
- **Feito (LEIA-ME do protótipo e 27, seções 3.2 a 3.4, 4, 7, 9 e 10):**
  - tabelas provisórias por tier e limites por efeito; requisitos (equipamento = base − 1; I/II/III = 1/5/9);
  - o bloqueio em todos os caminhos, a gravação em peça vestida recusada sem cobrar e a preparação na bolsa;
  - a prévia do Encantar calculada no motor; o selo do tier; as fichas e as dicas dentro da janela;
  - o OK fora do lugar do Reforçar; a transferência com "Após transferir";
  - **gestos:** só o 2º clique de um duplo é o resto do gesto (o `detail > 1` travava cliques seguidos);
  - **tremor:** a mistura do veio pelo CSS fazia o navegador reamostrar a peça; agora o veio é uma sequência de
    quadros prontos, mostrados como imagem (medido: a 125%, a Couraça +10 de 89% para 1% de blocos borrados);
  - a skill `texto-regras-fenda` com os critérios gerais de tier, prévia e contexto.
- **A 14ª** está em `tela/historico/v14`.
- **Conferido:** 52 testes do protótipo; as duas resoluções; o tremor a 100%, 125% e 150%; os testes do projeto.
- **Próximo:** a avaliação do Jean. Nada integrado; som adiado; a etapa 4 continua aberta.

### 28/10/2026 (data do computador local) — Forja: a 16ª versão, ganho real em todo reforço e candidatas visuais (protótipo)

- **Pedido:** texto e HUD com formatos comuns e a revisão como parte do processo; etiquetas de tier legíveis;
  disponível/necessário nos materiais e o ouro no botão; duas candidatas de botão com o preço dentro e a confirmação
  sem mover a ação; todo reforço válido com ganho real; reforço de peças sem portador; a piscada ao reforçar e os
  gestos; a paleta da celebração (corrigido pelo Jean: só do +9 ao +12); dois acabamentos para armaduras do +9 ao
  +12; o painel de testes.
- **Feito (LEIA-ME do protótipo, 16ª; 27, seções 1.1, 1.2, 3.3, 9, 10, 11 e 12):**
  - **regra:** precisão por propriedade (uma casa em Ataque, Poder, Defesa, Agilidade, Espinhos e curas; décimos em
    Crítico e Roubo de vida; Vida e Mana inteiras), a garantia de um degrau, a fração até a ficha e a luta (Espinhos e
    curas acumulam a fração), a peça toda no teto recusada sem cobrar, o reforço sem portador;
  - **causas:** o ganho zero era o arredondamento a inteiro (nenhum passo zerado na conta); a piscada era a cena nova
    limpando a página antes de o painel chegar (reproduzida com atraso; o motor agora calcula antes e a tela segura a
    janela antiga);
  - **tela:** `requerHtml`, `botaoAcao` e `peAcao` nas quatro abas; a etiqueta do tier; "Brasa I ×2"; os botões A e
    B; os acabamentos A e B; a paleta candidata; o painel de testes (só na demonstração);
  - **skill `texto-regras-fenda`:** o fluxo de quatro passos para todo texto novo e a tabela dos formatos comuns;
    `CLAUDE.md` aponta para ela.
- **A 15ª** está em `tela/historico/v15`.
- **Conferido:** 61 testes do protótipo; as duas resoluções; os gestos por cobrança; a piscada com e sem a correção;
  os acabamentos a 100%, 125% e 150% e no movimento reduzido; os testes do projeto. A tela inteira do Inventário não
  foi capturada (a ficha foi conferida pelas dicas).
- **Decisões abertas (Jean):** botões A ou B; acabamento das armaduras A ou B; a paleta candidata; a proposta para a
  peça toda no teto. **Próximo:** a avaliação do Jean. Nada integrado; som adiado; a etapa 4 continua aberta.

### 28/10/2026 (data do computador local) — Forja: a 17ª versão; o acabamento A, a doca e os defeitos na produção (1.214.0)

- **Pedido:** a perda de vida ao entrar no ferreiro (prioridade); um acabamento novo e sutil para as armaduras do +9 ao
  +12 (o +8 intacto); a celebração do +9 ao +12 ligada ao acabamento (o ouro do +12 guardado para um eventual +13);
  o recebimento na desmontagem; o botão A (aprovado) nos outros componentes do jogo; textos; o preço do Mercado sem
  ouro; o pixel azul e o item borrado no achado; candidatas de arte do ferreiro e do busto da Odette; o nível dos
  companheiros na luta. E a pergunta do Jean: os atalhos da barra de baixo recusados em lugares sem sentido (dentro
  da forja). Sim, fazia sentido revisar: agora funcionam.
- **Protótipo (LEIA-ME, 17ª; 27, seções 6, 9, 10, 11 e 12):**
  - **a vida:** a comparação hipotética da ficha cortava a vida no máximo sem a peça e não a devolvia; agora guarda e
    repõe (teste pelo caminho real). A produção não tinha o defeito;
  - **visual:** o B saiu; o feixe nas armaduras (candidata); a celebração ligada ao acabamento (candidata); o
    recebimento na desmontagem; a entrada 2 × 2. O A e o B das armaduras e a paleta da 16ª foram rejeitados;
  - **texto:** o limite no valor ("60% · limite"), a substituição numa frase, "Materiais" sem a explicação.
- **Produção (1.214.0, um commit por assunto):**
  - **a doca nas telas de serviço:** o motor marca o Voltar da forja, do mercado, da taverna e do templo
    (`lugar: True`) e a doca aceita o atalho ali (volta ao lugar e abre a tela);
  - **Mercado:** o preço fica à vista (em vermelho) quando falta ouro, com o motivo embaixo;
  - **luta:** o nível dos companheiros no cartão ("Nv.6");
  - **achado:** a peça ficava borrada a 125% (posição fracionária numa camada composta); agora assenta no pixel do
    aparelho depois da cerimônia (349 → 0 pixels diferentes do arquivo a 125%);
  - **textos:** "Brejo" virou "Alagado" e a Hidra, "do Pântano" (os ids ficaram; o replay traduz os nomes antigos);
    sem "Curas param em N" e sem os rodapés que explicam o clique (Inventário, Mercado, serviços, painéis, Comitiva,
    fogueira, talentos);
  - **acabamento A** (`css/27-ferro.css`): Caminhos, serviços, Mercado, doca, cartões da Comitiva (sem o rodapé) e do
    Bestiário (o que falta descobrir como estado bloqueado, com o cadeado), abas do Inventário, "Distribuir pela
    sugestão" e os "+";
  - **gabarito atualizado de propósito:** as diferenças são o `lugar` no Voltar, o `sem_ouro` no Mercado, o `nivel`
    dos companheiros, o `falta` do Bestiário e a dica sem "Curas param em N".
- **Candidatas de arte (não aplicadas):** o ferreiro (`hud/forja/h2/candidata_ferreiro.py`: o cabo atravessando a mão
  no sobe2, a nuca, o calcanhar da bigorna à frente da barriga; a perspectiva da bigorna vista de cima e o ferreiro
  atrás dela são intencionais) e o busto da Odette (`hud/odette-busto/`: ombros de 38 para 32 pixels, o hábito abrindo
  devagar; o rosto igual), com as folhas.
- **Não reproduzido:** o pixel azul depois do achado (LEIA-ME da forja, 17ª: o que foi testado e as hipóteses).
- **Conferido:** 62 testes do protótipo; 728 do projeto, gabarito, pyflakes e a fumaça; capturas a 1920×945 e
  1280×720 nas telas afetadas. Não foi feita a bateria inteira de resoluções.
- **Decisões abertas (Jean):** o feixe das armaduras; a paleta da celebração; as candidatas do ferreiro e da Odette;
  o estado bloqueado do Bestiário. Som adiado; a etapa 4 continua aberta.

### 28/10/2026 (data do computador local) — Forja: a 18ª versão; armaduras A, B e C, desmontagem fluida, remover gravação, placas da bancada e o gesto do ferreiro (protótipo)

- **Pedido:** revisar a direção visual dos botões e painéis (a aplicação do botão A no jogo não agradou), a partir das
  placas de metal da bancada, como candidata no protótipo; três alternativas jogáveis para as armaduras do +9 ao +12
  (o +8 intacto); a fluidez da desmontagem; remover a gravação sem substituir; o gesto do martelo do ferreiro. Sem
  vídeos nem folhas: as candidatas ficam na demonstração.
- **Decisões (Jean, neste pedido):** a celebração do +9 ao +12 aceita por enquanto (sem mudar as cores); a remoção
  gratuita nesta candidata, a essência perdida, nada devolvido; o pixel azul continua não reproduzido.
- **Candidatas (protótipo; o painel de testes troca cada uma):**
  - **armaduras A · passadas alternadas, B · cor gradual, C · reflexo principal e secundário**, com a vitrine das
    cinco peças do +8 ao +12; o feixe da 17ª substituído (fica para comparar);
  - **placas de metal da bancada** (`tela/placas.css`): o que se aperta tem espessura, o que informa é fixado com
    rebites, número e tecla em nicho; os Caminhos, os serviços e cabeçalhos, o Voltar à vila, o aviso de talento, a
    doca, o Inventário, a Comitiva, o Bestiário, a Encruzilhada e o Continuar da festa da especialização. O botão A de
    produção fica como está até a escolha (em revisão);
  - **remover a gravação** (27, 3.3 e 9);
  - **o gesto do ferreiro** (`hud/forja/h2/candidata_gesto.py`): a pegada na ponta do cabo, o martelo armado atrás da
    cabeça, a descida em arco; sem integrar.
- **Corrigido (protótipo):** a desmontagem (o efeito a 15 quadros por segundo, as animações em degraus e os
  redesenhos que paravam o efeito; agora ~60 quadros por segundo e contínua nos redesenhos).
- **Conferido:** 65 testes do protótipo; a suíte do projeto, o gabarito, o pyflakes e a fumaça; no navegador, a
  1920×945 e a 1280×720, com teclado e movimento reduzido, os estados das placas um a um e a escala de 125% nas
  armaduras. Não conferido: o Bestiário com criaturas e o Caminho fechado (LEIA-ME do protótipo, 18ª).
- **Pendências (Jean):** A, B ou C; as placas (antes de outra aplicação ampla na produção); a remoção (e se deve
  custar); o gesto do ferreiro; a Odette. Nada integrado; som adiado; a etapa 4 continua aberta.

### 28/10/2026 (data do computador local) — O pixel azul do achado (1.214.1)

- **Pedido:** o Jean mostrou com uma captura o pixel azul que via depois do achado de uma peça incomum (antes,
  registrado como não reproduzido: a procura tinha sido por uma sobra do efeito animado).
- **Causa:** o enfeite parado do incomum no achado, desde a 1.201.0 (`celebracoes/estouro.js` e `relicario.js`, o
  acento azul do mágico da etapa 2): um fio azul de 64 × 3 px e um losango de pixels embaixo do desenho. Não era sobra
  de animação: era desenho de propósito, mas se lia como sobra do efeito.
- **Correção:** o enfeite saiu nas duas apresentações; o brilho breve da cerimônia fica, e o selo "Incomum" e o nome
  em azul marcam a raridade. Reproduzido no jogo (cenário "vila", o achado já sai incomum): antes, o fio e o losango
  embaixo da couraça; depois, só a peça, no Estouro e no Relicário.
- **Conferido:** a suíte, o gabarito, o pyflakes e a fumaça.

### 28/10/2026 (data do computador local) — Placas da bancada, segunda passada; a tecla da doca pressionada (1.214.2)

- **Pedido:** uma referência de composição (imagem gerada) para a candidata de interface: os quatro serviços da forja
  em 2 × 2, as placas como família comum, a barra de baixo contínua com divisões claras, a hierarquia ícone, nome e
  linha secundária. Não vale como acabamento: em pixel, arestas retas ou em degrau, poucos tons, rebites pela escala;
  os ícones, os números e os textos são os do jogo.
- **Protótipo:** a entrada da forja em 2 × 2 de verdade (a regra `#cena.com-ambiente .forja .servicos` do jogo vencia
  a de duas colunas desde a 17ª), sem "(laboratório)" no Encantar; os rebites pela escala; a doca como suporte
  contínuo; o aviso de talento com o fim separado (27, seção 10; LEIA-ME do protótipo, 18ª).
- **Produção (1.214.2):** a tecla do atalho da doca caía embaixo do nome com o botão pressionado (o acabamento A da
  1.214.0 descia todos os filhos do botão, inclusive a tecla posicionada no canto); agora desce tudo menos a tecla.
- **Conferido:** 1920 e 1280 (a barra 4 px mais alta que hoje), os estados das partes novas; a suíte, o gabarito, o
  pyflakes, os testes do protótipo e a fumaça.

### 28/10/2026 (data do computador local) — Ferreiro: o fim do golpe; o pulo da doca

- **Avaliação do Jean:** a subida do martelo na candidata ficou certa; o fim do golpe, com a mão colada ao corpo e o
  cotovelo dobrado para trás, ainda lia como guidão (e não dá para fazer de verdade). E os atalhos da barra de baixo
  davam uma "puladinha" ao clicar.
- **Ferreiro (candidata, `hud/forja/h2/candidata_gesto.py`):** no contato com a espada, o braço estendido para a
  frente, a mão à frente do corpo e o cabo descendo em ângulo até a lâmina (o golpe, a volta, o repouso e o ajuste).
  Na demonstração, pelo painel ("Ferreiro: gesto candidato"). Nada integrado.
- **A puladinha:** era a tecla do atalho caindo para baixo do nome com o botão pressionado, corrigida na 1.214.2
  (antes desta avaliação). Conferido com o código atual: pressionar desce só o ícone e o nome 1 px, e um clique de
  verdade não mexe a barra em nenhum quadro (Grimório, Inventário, Comitiva).

### 28/10/2026 (data do computador local) — Ferreiro: o ombro no fim do golpe (candidata, 3ª passada)

- **Avaliação do Jean:** o braço melhorou muito, mas no fim do golpe o ombro ainda parecia levantado, como se,
  perto demais da bigorna, ele não conseguisse esticar o braço (o martelo grande demais ou o corpo perto demais).
- **Causa:** a geometria. O contato fica só 7 px abaixo do ombro e 21 px à frente dele; com o cabo de 12,5 px, braço
  e cabo passavam dessa distância e o braço dobrava; e, mesmo esticado, ele só alcança quase na horizontal.
- **Candidatas (painel, "Ferreiro"):** **Corpo desce** (a padrão: o corpo acompanha o golpe, com o quadril e os
  joelhos mais baixos e o ombro 2 px abaixo; o braço vai para a frente e para baixo, encurtado pela perspectiva, e a
  mão termina junto da bigorna) e **Braço reto** (o braço esticado em linha até o contato). O cabo passa a 10 px em
  todas as poses. A subida aprovada fica. Nada integrado.

### 28/10/2026 (data do computador local) — Ferreiro: o martelo limpo no golpe (candidata, 4ª passada)

- **Avaliação do Jean:** o gesto está bom (a direção "Corpo desce"); no golpe, os pixels da cabeça do martelo estavam
  fora do lugar (a face que bate e a parte de cima) e o cabo desalinhado com a cabeça.
- **Causa e correção:** a cabeça vinha de um desenho em código que a gira em qualquer ângulo; com o cabo quase deitado,
  saíam degraus. Nas quatro poses com o martelo na lâmina, a cabeça agora é desenhada à mão, alinhada à grade, e o
  cabo entra reto no olho. O martelo no ar não mudou. Nada integrado: falta a aprovação para levar à fonte em Aseprite.

### 28/10/2026 (data do computador local) — A forja integrada no jogo (1.216.0)

- **Pedido do Jean:** fechar e integrar o lote aprovado da forja e da interface. Aprovados: Reforçar, Encantar, remover
  gravação, Transferir e Desmontar com as regras atuais; as placas da bancada nos usos revisados; armaduras +9 a +12
  em **B · Gradual**; o ferreiro "Corpo desce" com o martelo corrigido; a Odette com o busto mais estreito; as
  celebrações atuais; o Bestiário e o Caminho fechado (conferidos por ele).
- **Dois retoques antes (protótipo, `db7ef6fe`):** o rótulo da prévia não encosta mais no número ("Ataque 12,2 →
  12,7"; no componente compartilhado); o encaixe do ícone dos serviços virou um rebaixo da chapa, longe dos rebites,
  com o ícone do mesmo tamanho.
- **Fontes consolidadas:** o gesto do ferreiro na fonte Aseprite (`ba1c4727`; a fonte é a autoridade, os scripts
  antigos recusam sobrescrever), a Odette na grade de `retratos.js` (`df16b1f4`, 1.215.0).
- **Integrado (1.216.0):**
  - motor em `rpg/forja` (`regras`, `encanto`, `oficina`, `fracao`); o ferreiro do Vau é a forja ("Ferreiro: a
    forja"); sem a tela gráfica, só o reforço por lista;
  - materiais no save e nas fontes reais (lutas, chefes, baús, desmontagem); nada de recompensa de teste na campanha;
  - save no formato 9: materiais, sulcos e a peça do ferreiro anterior refeita no mesmo +N pelas regras novas (a
    decisão está no 27, seção 8);
  - a fração nos atributos e na luta; o requisito de nível em todos os caminhos de vestir; o mercado com o motivo do
    motor ("Requer nível 9." ou a classe);
  - a tela (`telas/forja.js`, `css/28-forja.css`, `css/29-placas.css`) sem a faixa, o painel de testes, os casos
    forçados nem os seletores; armaduras B, celebrações atuais e placas sempre ligadas.
- **Ficou no protótipo:** as alternativas (armaduras A · Alternadas, preservada para uma troca futura sem opção para
  o jogador, e C; o feixe e o veio anteriores; paletas e celebrações antigas), o painel de testes e os cenários. A
  demonstração tira os arquivos de produção da página e liga o laboratório por cima.
- **Equilíbrio:** sem recalibrar; a economia, as chances e os requisitos ficam para o Jean avaliar jogando. **Som:**
  adiado.
- **Gabarito:** atualizado de propósito. As 18 partidas do herói são iguais até a primeira ida ao ferreiro (o
  ferreiro anterior dava lugar à forja); as 6 da comitiva, iguais sem o sorteio de materiais. O resto vem do sorteio
  dos materiais no saque e nos baús (desloca o `rng`), dos campos novos (materiais, reforço, requisito, gravações,
  efeitos), do nome da opção e do motivo no painel do mercado.
- **Conferido:** a suíte (com os testes novos da forja e do save), o gabarito, o pyflakes, os testes do protótipo e a
  fumaça; no navegador, pelo cenário `forja` (`python -m tests.navegador.cenarios forja`), em 1920 × 945 e 1280 × 720 e
  com movimento reduzido: a entrada, o reforço (ganho fracionário), a gravação, a remoção, a transferência, a
  desmontagem, os materiais no Inventário, o duplo clique e o Enter segurado cobrando uma vez, sem perder vida ao
  entrar e sem erros no console.
- **Aberto:** a arte própria dos materiais; as fontes de essência III e de fragmentos para o reforço alto dependem da
  campanha ampliada; a 1280 × 720 a segunda fileira da entrada pede rolagem (para a consolidação da HUD).

### 28/10/2026 (data do computador local) — O interior da curandeira: candidata A (protótipo)

- **Pedido do Jean:** começar a etapa dos interiores pela curandeira, com a câmera próxima da forja e a identidade de
  um lugar de tratamento com ervas (bancada, almofariz, ervas secando, panos e água, um fogo modesto, espaço de
  circulação), sem laboratório de mago; Pita e Marta conforme a história, sem as duas trabalhando juntas nem Marta
  acamada; a referência `A herbalista e o almofariz.png` só como composição. Só no protótipo.
- **Feito:** `ferramentas/prototipos/curandeira` (o LEIA-ME tem o levantamento, a escala, o gesto e o que a conferência
  corrigiu). O ambiente e as figuras desenhados em código na grade de 320×96, na linguagem da forja; o gesto de moer no
  almofariz pelos apoios, contido, com a pose parada; a cena no sistema de ambientes só na página da demonstração, com o
  serviço de produção sem mudar. A referência guardada em `ferramentas/arte/referencias/cenarios internos/` (a pasta
  que o Jean renomeou; o LEIA-ME com a origem e o hash).
- **Estados (a faixa da demonstração, num save temporário):** Pita com Marta de cama; Pita na noite da água escura (os
  baldes e a fervura forte); Marta de pé. E a pose parada.
- **Conferido:** no navegador, a 1920×945 e a 1280×720 (os três estados, a pose parada, o ponto de quem atende, um
  tratamento, a volta à vila, sem erros no console). Esperando a avaliação do Jean; nada integrado; templo e taverna não
  começados.

### 28/10/2026 (data do computador local) — Curandeira: a botica e o braço (protótipo, segunda passada)

- **Avaliação do Jean:** gostou do cenário, mas o achou genérico ("um mato e potes genéricos"); pediu personalidade,
  aura de mandinga e alquimia com coisas naturais, sem bruxaria. O braço do almofariz tinha poucos quadros perto do
  ferreiro, com um pedaço do avental virando braço e sujeira de geração.
- **Feito (só no protótipo):** o braço refeito quadro a quadro (formas cheias, a manga no pano do vestido, o punho em
  volta do pilão, 12 poses a 100 ms); a botica (a cobra no âmbar, as sanguessugas, a raiz, os cogumelos, as tinturas,
  as velas, o alambique sobre a lamparina, o crânio de cervo, a estrela de palha e o amuleto da porta, o caldeirão).
  O LEIA-ME do protótipo detalha. Conferido no jogo nas duas resoluções. Esperando o Jean; nada integrado.

### 28/10/2026 (data do computador local) — Curandeira: as ervas, a rotina e os rostos (protótipo, terceira passada)

- **Avaliação do Jean:** manter a composição, a personalidade e os objetos de alquimia natural. Os maços pendurados
  pareciam pinhatas; Pita e Marta mexiam só o braço (robótico, e mais quadros do mesmo gesto não bastam). Pediu uma
  pequena rotina de trabalho com pausas e intenção, o corpo participando pela atividade (sem balanço constante), e a
  skill corrigida para o erro não voltar. Durante a rodada: rosto e cabelo mais bonitinhos, com traços simples como os
  do ferreiro.
- **Feito (só no protótipo, `ferramentas/prototipos/curandeira`):** os maços à mão por planta (sálvia, lavanda, réstia
  de alho, bagas, camomila, com barbante e amarração); a rotina (moer, desacelerar, olhar a mistura, a pitada levada ao
  nariz, pegar o pilão de novo) com o braço de comprimento fixo levando o corpo, as passagens escalonadas e a volta ao
  começo sem salto; Marta e Pita no ritmo de cada uma; Pita num banquinho (a bancada é a de Marta); os rostos e o
  cabelo refeitos, o pescoço ligado ao vestido. A segunda passada fica em `anterior/camadas` (botão "Passada anterior"
  na faixa). O LEIA-ME do protótipo detalha.
- **Skill `arte-cenas-fenda`:** a seção 5b (a atuação passo a passo: atividade e apoios, quem conduz, acompanha e fica,
  o alcance decidindo o corpo, poses-chave do corpo inteiro, rotina, passagens, conferência em três camadas), os erros
  da curandeira e o estudo de caso `curandeira.md`.
- **Conferido:** no jogo, a 1920×945 e a 1280×720 (os três estados, a vista quadro a quadro, a pose parada, um
  tratamento, sair e voltar sem acumular relógio, sem erros no console). Esperando o Jean; nada integrado; templo e
  taverna não começados.

### 28/10/2026 (data do computador local) — A cabana aberta sem ferimento (1.217.0) e a moagem pausada (protótipo)

- **Pedido do Jean:** o refinamento final da candidata da curandeira (preservar cenário, ingredientes, personalidade e
  rotina; sem decoração nova nem caminhada) e a separação entre acesso ao lugar e disponibilidade dos serviços, como
  decisão geral do projeto. Também registrar o papel futuro dos interiores e a alquimia.
- **No jogo (1.217.0):**
  - a curandeira entra no menu da vila também sem ferimento: a cabana abre, a área do serviço diz "Nenhum ferimento a
    tratar." e a cena, os pontos e o Voltar continuam; tratar o último não tira o jogador dela. A fala de quem atende
    sem ferimento ficou sem a regra repetida (Marta e a curandeira de sempre só erguem os olhos; Pita mantém a dela).
    O quadro F3 do tutorial só se marca ao entrar com o que tratar;
  - os ferimentos dizem o atributo antes do valor, em todo lugar (cartão, dica e aviso): "Vida máxima −10%",
    "Defesa −25%, Vigor máximo −15%";
  - levantamento dos outros: mercado, forja e taverna já abriam sempre; o templo sem ninguém a cuidar já mostrava o
    balcão com a frase; nenhum fechamento narrativo nesses lugares. Só a curandeira mudou;
  - o clique duplo num cartão trata um só (a guarda do `Gesto` já cobria; conferido de novo).
  - **Gabarito** atualizado de propósito: a opção da curandeira aparece no menu da vila sem ferimento (o robô escolhe
    por posição e segue outro caminho dali) e o texto novo dos ferimentos.
- **No protótipo:** a moagem em 7 poses sustentadas, com a pressão longe do corpo de 4 a 6 tiques, na mesma duração; a
  mão alcançando o cabo antes de pegar o pilão. A terceira passada fica em `anterior/terceira` ("Moagem anterior").
- **Registros:** a decisão do acesso, o papel futuro dos interiores e a alquimia guardada em
  [10](10-DECISOES.md) e em [docs/ROADMAP.md](../docs/ROADMAP.md); a skill de cenas com o passo do ritmo (5b, 8).
- **Conferido:** a suíte, o gabarito, o pyflakes e a fumaça; no jogo, pela demonstração, a 1920×945 e a 1280×720 (os
  cartões, o clique duplo, o último pelo teclado, ouro, ferimento e vida máxima, os três estados sem ferimento, sair e
  voltar sem acumular relógio, a pose parada, sem erros no console). A curandeira continua candidata; templo e taverna
  não começados.

### 28/10/2026 (data do computador local) — A curandeira no jogo (1.218.0) e o templo em protótipo (duas candidatas)

- **Pedido do Jean:** integrar fielmente a curandeira aprovada (cenário, ingredientes, Pita com o banquinho e Marta, a
  rotina, a moagem da quarta passada, os estados, a pose parada, os cartões), sem revisão nova; corrigir a concordância
  de "Mordida dilacerada: tratado" no componente; e começar o templo (Curandeira → Templo → Taverna). Durante a rodada:
  uma segunda candidata do templo a partir da referência que ele adicionou (`Interior do Templo da Vila.png`).
- **No jogo:**
  - **concordância** (commit próprio): as mensagens de ferimento concordam pelo artigo do `curto` de cada um
    (`sobrevivencia.concordar`, `possessivo`): "Mordida dilacerada: tratada", "Costelas quebradas: tratadas",
    "Concussão: curada", "Sua mordida dilacerada está vermelha";
  - **a cabana (1.218.0):** a arte em `static/cenas/curandeira` exportada da fonte nova
    (`ferramentas/prototipos/curandeira/aseprite/curandeira.aseprite`, `fonte.py`), `telas/cena-curandeira.js`,
    `css/30-curandeira.css` e `servicos.cena_curandeira` (o motor diz quem atende e a água; só no Vau da campanha). A
    1.217.0 ficou: entrar sem ferimento, continuar depois do último, o tutorial, os preços e os efeitos.
  - **Gabarito** atualizado de propósito nos dois commits: as mensagens de ferimento; o painel da cena nas partidas da
    tela gráfica.
- **Conferido:** a suíte, o gabarito, o pyflakes e a fumaça (385, com a cena da cabana); no jogo real (cenários
  `tutorial` e `retorno`), a 1920×945 e a 1280×720: os três estados, cartões, clique duplo, teclado, atalho M, Esc,
  sair e voltar com um relógio só, movimento reduzido, só arquivos de produção, sem erros; a cena de produção igual à
  candidata pixel a pixel em todos os tiques dos três estados. Limites: fora do Vau da campanha, a curandeira segue
  sem ambiente; a tela da curandeira não tem atalho de número (nunca teve).
- **Templo (`ferramentas/prototipos/templo`, só no protótipo):** o levantamento (o clérigo cansado, de mãos firmes;
  unguentos e orações; o herói e a comitiva; o primeiro atendimento grátis; o templo em silêncio quando ninguém
  precisa; as janelas da fachada acesas em amarelo quente) e duas candidatas jogáveis: **A**, a nave de lado (o clérigo
  enrola ataduras na mesa dos unguentos, ~42 px), e **B**, da referência do Jean (a nave de frente para o altar sob o
  arco; o clérigo dobra panos, ~31 px; sem os símbolos gerados). O interior entra no lugar da vila aproximada; o balcão
  e os cartões são os de sempre. Conferido na demonstração nas duas resoluções. A taverna não foi começada.

### 28/10/2026 (data do computador local) — Templo B: o piso, os planos e os apoios (protótipo, segunda passada)

- **Avaliação do Jean:** a B é a direção do templo (a A fica como histórico); a composição está boa. O problema era a
  perspectiva e o apoio: o piso da direita parecia a frente de um degrau, os móveis e o clérigo pareciam flutuar ou
  estar grudados na parede, e a roupa do clérigo se misturava ao pé da mesa. Integração não autorizada.
- **Feito (só no protótipo, `ferramentas/prototipos/templo/b`):** o espaço construído e conferido antes dos objetos: o
  piso contínuo com as juntas convergindo para o fundo, a parede encontrando o piso atrás de tudo, a elevação só no
  presbitério (os degraus com o piso claro e a frente escura, o altar como bloco com base), cada objeto com o seu apoio
  (tampo, espessura, pernas, rodapé, soleira) e chão à vista entre eles, as sombras de contato depois, o primeiro plano
  só nos cantos; o clérigo com 2 px de chão entre o hábito e o pé da mesa, o hábito em outro valor, e a conta das
  sobreposições nas 8 poses. A demonstração abre na B.
- **Skill `arte-cenas-fenda`:** a seção 3a (o espaço antes dos objetos) e o passo 4 do fluxo: a referência de
  composição discutida com o Jean, o piso, os planos, a circulação e os apoios validados antes do detalhe, as
  sobreposições conferidas durante a animação; a referência gerada não prova a própria perspectiva.
- **Conferido:** o espaço sozinho e a cena ampliados; as poses; no jogo, pela demonstração, nas duas resoluções (o
  interior, os pontos, os serviços, as duas candidatas, a Saída e o Esc, ninguém precisando, sem ouro, o relógio, a pose
  parada, sem erros no console). Esperando a avaliação do Jean.

### 28/10/2026 (data do computador local) — Templo B: cada coisa com um motivo (protótipo, terceira passada)

- **Avaliação do Jean:** gostou; pediu que tudo na tela tenha motivo para estar ali (os postes com "braços" só em
  alguns e tortos, chamas soltas, a porta que lia como sarrafo, os vasos pretos avulsos), com um primeiro plano que
  traga mais a igreja de uma cidade mediana sem atrapalhar a vista.
- **Feito (só no protótipo):** as mãos-francesas retas e coerentes em todos os postes; as chamas soltas viraram a vela
  no pires em cima do armário e duas arandelas de ferro com vela; a folha da porta da rua aberta, de quina, com tábuas,
  ferragens e argola; a toalha num cravo; no primeiro plano, as pontas da fileira de bancos mais próxima no lugar dos
  vasos. O LEIA-ME do protótipo tem a tabela. Conferido no jogo nas duas resoluções. Integração não autorizada.

### 28/10/2026 (data do computador local) — Templo B: construção e identidade dos objetos (protótipo, quarta passada)

- **Pedido do Jean:** preservar a composição e o piso; estrutura de madeira coerente, portas reconhecíveis, fogo com
  suporte e recipiente, primeiro plano com propósito, a luz quadriculada da entrada; poucos objetos legíveis, podendo
  remover o que não ajuda.
- **Feito (só no protótipo):** os postes de madeira saíram (o frechal agora apoia em mísulas de pedra); a porta da rua
  em arco de pedra, com o lado de fora e a luz no piso chapados (sem xadrez); a porta lateral com dobradiças e argola;
  o castiçal de chão com os copos; o fogareiro do incenso em tigela com as brasas (a vela solta saiu); a toalha e a
  caixinha do armário saíram; o primeiro plano saiu (as pontas de banco não se alinhavam com os blocos). Conferido no
  jogo nas duas resoluções. Integração não autorizada.

### 28/10/2026 (data do computador local) — Templo B: o arco, as vigas e os bancos (protótipo, quinta passada)

- **Pedido do Jean:** antes de integrar, o encontro das vigas com o arco (apoio real, não recorte) e os bancos (tábuas
  retas, espessura consistente, a mesma perspectiva); no arco, a passagem do pilar para a curva e a espessura interna.
- **Feito (só no protótipo):** as vigas terminam antes do arco, cada ponta numa mísula; o arco nasce na imposta, sobre
  o pilar, com a face e o intradorso (a espessura continuando pelo lado de dentro dos pilares); os bancos e a passadeira
  pela mesma perspectiva do piso, com o encosto de duas tábuas retas. Conferido no jogo nas duas resoluções. Integração
  não autorizada.

### 28/10/2026 (data do computador local) — Templo B: os bancos na escala do clérigo (protótipo, sexta passada)

- **Pergunta do Jean:** a altura dos bancos em relação ao clérigo. Medidos pela conta de distância do piso, tinham
  ~0,45 m (metade de um banco real).
- **Feito (só no protótipo):** os bancos passam a sair de medidas em metros na escala do clérigo (0,90 m no encosto,
  0,45 m no assento); as fileiras vieram para mais perto, para os degraus aparecerem pelo corredor, e o bloco da
  direita acaba antes do pé da mesa. Conferido no jogo nas duas resoluções. Integração não autorizada.

### 28/10/2026 (data do computador local) — Templo B: a simetria no eixo da nave (protótipo, sétima passada)

- **Pergunta do Jean:** por que os bancos de um lado eram mais compridos (não era perspectiva: o bloco da direita
  tinha sido encurtado por causa da mesa). Ele autorizou mexer no que fosse preciso para a simetria.
- **Feito (só no protótipo):** os dois blocos de bancos iguais e curtos (o da direita, o espelho exato do da esquerda),
  com a passagem livre da porta da rua; as colunas e o arco no eixo (estavam 1 px fora); as mísulas, as pontas das
  vigas e as arandelas espelhadas. Conferido por conta (a forma espelhada sem pixel fora) e no jogo nas duas
  resoluções. Integração não autorizada.

### 28/10/2026 (data do computador local) — Templo B: o corpo do clérigo sem quebra (protótipo, oitava passada)

- **O que o Jean notou:** o corpo do clérigo se quebrava quadro a quadro (o encaixe aparecia).
- **Feito (só no protótipo):** a inclinação deixou de fatiar o tronco: o tronco e a cabeça inclinam como um bloco e o
  hábito absorve, da cintura à barra parada; uma pose de passagem entre a pega e o erguer. Conferido pose a pose (o
  contorno sem degraus) e no jogo nas duas resoluções. A lição foi para a tabela de erros da skill de cenas.

### 29/10/2026 (data do computador local) — O templo no jogo (1.219.0)

- **Integrada a candidata B aprovada**, com a oitava passada (o corpo do clérigo sem quebra) e sem ornamento novo: a
  fonte em Aseprite (`ferramentas/prototipos/templo/aseprite/templo.aseprite`, criada por `fonte.py --criar`, que não
  a sobrescreve; os scripts antigos não tocam nela), exportada para `rpg/web/static/cenas/templo/` e conferida contra a
  candidata (4 de 4 camadas e a rotina iguais).
- **No jogo:** o motor manda a cena (`servicos.cena_templo`, em `estado.local.interiores`, só na vila); diante do
  templo, a vista mostra o interior no lugar da vila aproximada (`app/vila.js`) e a Saída da cena é o Voltar à vila do
  balcão (`telas/cenas.js`). Serviços, preços, o primeiro atendimento grátis, os cuidados da comitiva, o acesso sem
  ninguém precisando e a permanência depois do atendimento, como antes.
- **Conferido:** a cena do jogo igual à candidata pixel a pixel nos 62 tiques; o ciclo completo, os contatos, o
  movimento reduzido, a entrada e a saída, o teclado, o clique duplo, só arquivos de produção, nas duas janelas.
  `unittest`, gabarito (só entrou `estado.local.interiores`, conferido linha a linha), pyflakes e fumaça (388).

### 29/10/2026 (data do computador local) — A taverna: a primeira candidata (protótipo, nada no jogo)

- **Pedido do Jean:** a primeira candidata jogável da taverna, pela referência "Taverna medieval entre fogo e sombras"
  (`ferramentas/arte/referencias/cenarios internos`): a câmera um pouco mais longe que a do templo, muitas mesas
  ocupadas, atividades reconhecíveis e circulação; a organização da referência corrigida; os serviços e eventos que
  existem; Morel no canto só quando o estado permite; nada de sistema novo.
- **Feito, só no protótipo** (`ferramentas/prototipos/taverna`, LEIA-ME com o roteiro; `demo.bat`, porta 8795, save
  temporário): a sala de frente (a porta da rua fechada à esquerda, o balcão com o barril e as prateleiras, três mesas
  ocupadas, a lareira com o caldeirão, a escada com a galeria dos quartos, o canto de Morel debaixo dela, o alçapão da
  despensa); nove pessoas em atividades com pausas e fases próprias (os jogadores e a conversa se revezam); Morel pela
  figura do jogo, só enquanto pode ser encontrado ali; os pontos levando aos cartões que existem (Taverneiro à bebida,
  Escada ao Dormir, Despensa e Homem do canto só com o cartão deles, Saída à vila). O botão Protótipo na barra do alto
  troca o estado (despensa, homem do canto, Morel conhecido, recrutado, sem ouro) e liga a pose parada.
- **Conferido no jogo** nas duas janelas: os pontos e os cartões em cada estado, o Tab e o Enter, a Saída e o Esc, um
  relógio só ao entrar de novo, o movimento reduzido parado com os pontos valendo, a barra do alto sem nada coberto,
  sem erros no console. As lições foram para a tabela de erros da skill de cenas.
- **Para integrar (se aprovada):** a cena e a regra de Morel no motor, `servicos: "<serviço>"` aceito pelo
  `telas/cenas.js` e a fonte em Aseprite. **A etapa 5 continua aberta;** som, equilíbrio e expansão narrativa adiados.

### 29/10/2026 (data do computador local) — A comparação de peças na casa decimal (1.219.1, produção)

- **O defeito:** num achado real, o Orbe de Aço com 4 de Poder contra o equipado com 7,6 mostrava
  "−3,5999999999999996 Poder". A comparação (`telas/itens.js`, `Telas.linhasTroca`: o caminho único do achado, do
  Inventário, do mercado e da forja) escrevia a subtração em ponto flutuante crua.
- **A correção:** a diferença na precisão das peças (uma casa, a de `forja/regras.limpo`), com a vírgula e o menos
  tipográfico ("▼ −3,6 Poder"); o percentual colado ("▲ +3,3% crítico"); o que sobra abaixo da casa é zero (a linha
  some, sem "−0"). Só a escrita; os valores das peças e as contas de combate não mudam.
- **Conferido:** com fichas reais do motor e na fumaça (positiva, negativa, inteira, fracionária, percentual, quase
  zero); `unittest` (797), gabarito sem mudança, pyflakes, fumaça.

### 29/10/2026 (data do computador local) — A taverna B: o estudo estático (protótipo, nada no jogo)

- **Pedido do Jean:** a A não foi aprovada visualmente (as pessoas estreitas, parecidas, de perfil; as mesas na mesma
  faixa; o balcão enorme; as prateleiras em fila; tudo marrom; a escada sem o acesso aos quartos; um banner no tamanho
  da HUD). Uma segunda candidata estática, a sala e as pessoas primeiro, a animação depois da aprovação.
- **Feito, só no protótipo** (`ferramentas/prototipos/taverna/b`, LEIA-ME com o roteiro; `demo.bat` abre na B, a A
  fica no botão Protótipo): a câmera mais funda (o ponto de fuga no quadro, 11 a 34 px por metro), a parede do balcão
  mais perto e o salão fundo, as mesas em três distâncias; oito pessoas à mão, de frente, três quartos, costas e
  perfil, com a cadeira vazia e passagens livres; a escada até a galeria com as portas dos quartos; a despensa como a
  porta baixa entreaberta; os materiais por valor. Morel com a aparência do jogo, presente e recrutado pela mesma
  hipótese da A (`demo.morel_no_canto`).
- **O balcão embaixo** (só na demonstração): o topo numa linha e os cartões em duas colunas, com o Voltar à vila na
  célula livre, e a rolagem refeita quando a página muda: tudo acima da doca, sem rolar, nas duas janelas.
- **Conferido no jogo** nas duas janelas: os pontos nos objetos certos e os cartões de cada um, Morel presente e
  recrutado, a troca de candidata, o teclado, a Saída e o Esc, um relógio só, o movimento reduzido, sem erros no
  console. **Aguarda o Jean** antes de animar o elenco novo ou integrar; som, equilíbrio e narrativa adiados.

### 29/10/2026 (data do computador local) — A taverna C: o estudo estático em avaliação (protótipo, nada no jogo)

- **Pedido do Jean:** a B melhorou sobre a A, mas não foi aprovada: profundidade exagerada (a diferença de três vezes
  entre a frente e o fundo não leu bem; não é uma exigência), o fundo pequeno demais (Morel com 3 a 4 px de cabeça),
  objetos com cara de esboço. Prioridades: a escada e a galeria como estrutura, o enquadramento e os grupos, os
  personagens, o volume e os materiais. Ainda estático.
- **Feito, só no protótipo** (`ferramentas/prototipos/taverna/c`; `demo.bat` abre na C, a B e a A no botão
  Protótipo; o LEIA-ME tem o roteiro e os limites): a régua contida (13 a 30 px por metro), o balcão e Morel na faixa
  do meio (cabeças de 6); a escada com o pilar do pé, os degraus, o banzo e o corrimão até o patamar, que é o esteio da
  galeria; a galeria com o piso visto de cima, a testeira, as mãos-francesas e as portas inteiras; três pessoas na
  mesa comprida da esquerda, dois jogando na redonda, a cadeira vazia, a passagem livre no meio; as pessoas à mão com
  cabeça, pescoço, tronco, braços e mãos separados; a lareira em planos; a luz em faixas lisas.
- **Conferido no jogo** nas duas janelas: os pontos nos objetos certos e os cartões de cada um, Morel presente e
  recrutado, a troca de candidata, o teclado, a Saída e o Esc, um relógio só, o movimento reduzido, os cartões e o
  Voltar acima da doca, sem erros no console.
- **Os limites que ficam:** o velho do fogo com 4 px de cabeça; a cicatriz de Morel em dois pixels; a perspectiva
  forçada do piso da galeria. **Estudo estático em avaliação, sem integração:** a animação do elenco e a integração
  esperam o Jean; som, equilíbrio e narrativa adiados.

### 29/10/2026 (data do computador local) — A taverna D: os conjuntos refeitos (protótipo, estudo estático, nada no jogo)

- **Pedido do Jean:** a C melhorou a organização, mas não foi aprovada; o maior problema era a relação entre a pessoa,
  o assento e a mesa (Morel longe do espaldar, o jogador de amarelo suspenso, a cadeira vazia grande e atravessando o
  tampo, o homem de marrom misturado ao balcão, o freguês de costas em barra, a caneca do taverneiro numa mancha, o
  velho do fogo sem pose); também os degraus, o piso da galeria, a boca da lareira, o balcão, as prateleiras, as faixas
  no reboco, a direita fundida e a narração da praça embaixo do interior.
- **Feito, só no protótipo** (`ferramentas/prototipos/taverna/d`; `demo.bat` abre na D, a C, a B e a A no botão
  Protótipo; o LEIA-ME tem o roteiro e os compromissos): cada conjunto refeito junto (o assento, a orientação, o
  alcance, a atividade); a escada de piso largo e menos íngreme; a galeria com o piso claro e o guarda-corpo discreto;
  a lareira com a boca funda; o balcão com a borda grossa; as prateleiras com poucos objetos de silhueta própria; a luz
  contínua, sem anéis; dentro da taverna, a narração da vila sai da página (fica a frase da taverna, uma vez).
- **Conferido:** técnico (no jogo, as duas janelas): os pontos e os cartões, Morel presente e recrutado, a troca de
  candidata (a C fotografada no mesmo estado), a narração da vila fora da taverna e de volta na vila, os cartões e o
  Voltar acima da doca, teclado, Saída, Esc, relógio, movimento reduzido, console. Artístico: no tamanho real e ampliado
  sem suavização, cada conjunto com o apoio, a orientação e o alcance legíveis; a avaliação final é do Jean.
- **A lição** foi para a skill de cenas: quem senta se constrói junto do móvel e da atividade. **Estudo estático em
  avaliação, sem integração;** a animação do elenco espera a aprovação; som, equilíbrio e narrativa adiados.

### 29/10/2026 (data do computador local) — A taverna E: a sala reconstruída numa projeção só (protótipo, estudo estático)

- **Mudança de direção (pedido do Jean):** a D melhorou os apoios, mas a escala e a perspectiva não convenciam (Morel e
  a mesa dos jogadores em escalas diferentes; a parede frontal e os tampos em graus diferentes). **A composição da C e
  da D deixou de ser uma restrição**, porque os ajustes locais não resolveram a coerência espacial: a câmera, a
  profundidade e a distribuição dos grupos podiam mudar, mantendo a identidade do lugar (o balcão, as mesas ocupadas,
  a lareira, a escada com a galeria, a despensa, o canto de Morel) e uma vista geral só.
- **Feito, só no protótipo** (`ferramentas/prototipos/taverna/e`; `demo.bat` abre na E, da D à A no botão
  Protótipo; o LEIA-ME tem o roteiro e os compromissos): primeiro o estudo de construção (uma projeção para tudo, as
  paredes do lado encontrando o piso, os móveis como caixas projetadas, uma figura de referência em pé e sentada em
  vários lugares); depois as pessoas à mão no ponto que a projeção dá a cada assento (Morel maior, num banco robusto,
  na mesma régua); a mesa comprida e a redonda na mesma faixa da sala, Morel contra a parede da direita, a passagem
  livre no meio; o acabamento da D (as prateleiras, a luz contínua, o contexto da taverna sem a narração da praça).
- **Conferido:** técnico (no jogo, as duas janelas): os pontos e os cartões, Morel presente e recrutado, a troca de
  candidata (a D fotografada no mesmo estado), a narração da praça fora da taverna, os cartões e o Voltar acima da
  doca, teclado, Saída, Esc, relógio, movimento reduzido, console. Artístico: no tamanho real e ampliado sem
  suavização; a avaliação é do Jean. **Compromissos:** as pessoas um pouco menores que as da frente da D (cabeças de 5
  a 6 px); os degraus em paralelogramo; as portas dos quartos com o alto debaixo da viga.
- **Possibilidade futura, sem compromisso:** um salão geral com aproximações para conversas ou atividades específicas;
  nada implementado.
- **A lição** foi para a skill de cenas: com vários grupos, validar uma escala e uma câmera comuns antes de detalhar
  cada conjunto. **Estudo estático em avaliação, sem integração;** a animação espera a aprovação.

### 29/10/2026 (data do computador local) — A taverna F: a nova referência aprovada (protótipo, estudo estático)

- **Pedido do Jean:** uma nova referência visual aprovada ("Taverna medieval entre brasas e sombras", guardada em
  `ferramentas/arte/referencias/cenarios internos`, com o papel no LEIA-ME de lá) passa a definir a composição, as
  poses e a relação entre pessoas e móveis; o acabamento segue o jogo; a E fica como histórico.
- **Feito, só no protótipo** (`ferramentas/prototipos/taverna/f`; `demo.bat` abre na F, da E à A no botão Protótipo;
  o LEIA-ME tem o roteiro, as diferenças em relação à referência e os compromissos): a referência medida na grade do
  jogo (não reduzida); a projeção da E com a câmera dela (14 a 28 px por metro, o olho a 3 m); o estudo de construção
  com a figura de referência; as pessoas à mão no ponto de cada assento; Morel na cadeira robusta de espaldar com a
  mesa individual inteira; a escada subindo até o patamar e a galeria com as portas inteiras; o piso de lajes.
- **Conferido:** técnico (no jogo, as duas janelas): os pontos e os cartões, Morel presente e recrutado, "Homem do
  canto" antes de conhecido, a troca de candidata (a E fotografada no mesmo estado), a narração da praça fora da
  taverna, os cartões e o Voltar acima da doca, teclado, Saída, Esc, relógio, movimento reduzido, console. Artístico:
  no tamanho real e ampliado sem suavização; a avaliação é do Jean.
- **Diferenças em relação à referência:** a galeria na altura que a projeção dá, a mesa de Morel inteira, Morel com a
  aparência do jogo, sem estandartes, tapete e cabeça de cervo, a porta da rua fechada. **Compromissos:** as pessoas da
  frente um pouco menores que na imagem; o gesto da mão no queixo pequeno; o fundo com cabeças de 5 px.
  **Estudo estático em avaliação, sem integração.**

### 29/10/2026 (data do computador local) — A taverna: a prova de qualidade dos jogadores (protótipo, nada no jogo)

- **Pedido do Jean:** interromper as reconstruções completas (a F fica como histórico, sem aprovação nem integração) e
  descobrir quanto do problema vem da resolução: os dois jogadores, a mesa e os banquinhos em duas grades nativas, no
  mesmo lugar da tela, com a mesma câmera, composição, poses, luz e paleta. A experiência não autoriza mudar a
  resolução dos interiores.
- **Feito** (`ferramentas/prototipos/taverna/prova`, LEIA-ME com o método, as medidas e as conclusões; `demo.bat` abre
  na prova, com Grade A, Grade B e Isolado no botão Protótipo): A em 66×42 e B em 132×84, as duas no recorte R da sala
  (x 174, y 42), desenhadas à mão em cada grade (nenhuma é a outra ampliada); os móveis pela projeção da F; a luz da
  sala no ponto de cada pixel. A F ganhou a chave `SEM_RODA`, desligada por padrão (as camadas dela não mudaram).
- **Medido no jogo:** a 1920×945, 219,4×139,6 px (3,325 px por pixel da A, 1,66 da B); a 1280×720, 146×92,8 px (2,21 e
  1,11); sem suavização. A escala não inteira deixa os pixels da B irregulares a 1920 (1 ou 2 px).
- **Conclusões (o LEIA-ME tem os detalhes):** na A, os dois sentados, os móveis, as pernas e o braço estendido leem; o
  braço dobrado e o tabuleiro ficam no limite. Na B, o gesto, a peça na mão, o tabuleiro e o volume do joelho e das
  botas leem; ela destoa um pouco da sala em volta (o grão mais fino). Nas duas, os troncos ainda retos, as roupas com
  poucas dobras e o contraste com o fundo escuro.
- **Parado aqui:** o padrão de qualidade é escolha do Jean antes de aplicá-lo ao resto da sala; nada reconstruído,
  animado ou integrado.
