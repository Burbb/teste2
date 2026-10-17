# roadmapIDEIAS — The Unquiet

Revisão 2 — 09/10/2026. Plano de design e desenvolvimento atualizado após leitura estática do jogo refatorado (versão 1.46.0, commit d8d65b9778e85bb7eb8118fdd7a84acfd17e80ac).

## Plano operacional atual — 17/10/2026

Para as próximas entregas de arte, interface, clareza do combate e serviços, seguir
[23 — Plano de arte, interface e combate](23-PLANO-DE-ARTE-INTERFACE-E-COMBATE.md).
Ele consolida a ordem aprovada por Jean e diferencia implementação, direção aprovada e hipóteses.
O resumo em [docs/ROADMAP.md](../docs/ROADMAP.md) aponta para ele. Os documentos anteriores preservam o histórico;
sua data de revisão não é o estado atual do jogo.

Referência desta atualização: produção 1.110.0; lote de cabeça/capuz e luvas de couro solicitado, ainda em proposta;
em seguida, clareza do consumo de recurso, protótipos de dado/iniciativa/turnos e consulta aos testes de atributos.
A discussão futura da campanha está em [22 — Ilse e a água](22-HISTORIA-ILSE-E-A-AGUA-RASCUNHO.md), como rascunho.

## Direção e escopo acordados

RPG de campanha em fantasia sombria, por turnos, com história escrita, mundo que responde a decisões, companheiros e liberdade de build. Preservar cenários minimalistas, cards, texto, som e telas interativas.

**Primeiro capítulo (11/10/2026):** o Vale do Turvo é o primeiro capítulo completo, para validação. Depois da
primeira entrega da E7 vem a avaliação integrada dele; a E8 fica adiada; a campanha maior continua como direção (veja
[01](01-VISAO.md), "Direção", e [07](07-ETAPAS.md), "Ordem atual").

**Três classes iniciais: Guerreiro, Arqueiro e Mago.** Reaproveitar as seis especializações existentes: Paladino, Berserker, Patrulheiro, Sombra, Piromante e Necromante. A sugestão anterior de reduzir a duas classes foi substituída pela decisão de Jean.

**Tecnologia:** manter Python no motor e HTML/CSS/JavaScript na interface local. A revisão não encontrou necessidade de migração. Não planejar troca de linguagem, framework ou engine como pré-requisito.

## Como seguir

Para uma nova conta ou sessão, começar por [00 — Comece aqui: continuidade](00-COMECE-AQUI.md). O arquivo preserva as passagens de contexto desde a versão 1.47.1; consultar os registros recentes e o plano 23 para o ponto de partida atual.

1. Ler [01 — Visão](01-VISAO.md) e [09 — Base existente](09-BASE-EXISTENTE.md).
2. Para o trabalho atual, escolher a próxima entrega do [23 — Plano de arte, interface e combate](23-PLANO-DE-ARTE-INTERFACE-E-COMBATE.md); consultar [07 — Etapas](07-ETAPAS.md) para os marcos de campanha e a E9.
3. Consultar os temas pertinentes e [10 — Decisões](10-DECISOES.md).
4. Usar um pedido de [08 — Trabalho com Claude](08-TRABALHO-COM-CLAUDE.md).
5. Validar tecnicamente e jogar antes de ampliar.
6. Registrar o resultado e revisar a próxima entrega.

| Arquivo | Conteúdo |
|---|---|
| [00-COMECE-AQUI.md](00-COMECE-AQUI.md) | Contexto para nova sessão, estado atual, correções recentes e primeira entrega |
| [01-VISAO.md](01-VISAO.md) | Identidade, pilares e destino dentro do escopo |
| [02-MUNDO-E-NARRATIVA.md](02-MUNDO-E-NARRATIVA.md) | Campanha, cenas, missões e estados do mundo |
| [03-CLASSES-E-BUILDS.md](03-CLASSES-E-BUILDS.md) | Três classes, seis especializações e limites da evolução |
| [04-HABILIDADES-E-TALENTOS.md](04-HABILIDADES-E-TALENTOS.md) | Reuso, habilidades efetivas, preparação e árvores |
| [05-ITENS-E-RECOMPENSAS.md](05-ITENS-E-RECOMPENSAS.md) | Afixos, únicos, efeitos, reforço e ritmo do saque |
| [06-JORNADA-E-APRESENTACAO.md](06-JORNADA-E-APRESENTACAO.md) | Sobrevivência, morte, comitiva e tecnologia |
| [07-ETAPAS.md](07-ETAPAS.md) | Entregas da primeira região até a campanha completa |
| [08-TRABALHO-COM-CLAUDE.md](08-TRABALHO-COM-CLAUDE.md) | Pedidos prontos, limites e registro |
| [09-BASE-EXISTENTE.md](09-BASE-EXISTENTE.md) | O que existe, o que estender e evidências |
| [10-DECISOES.md](10-DECISOES.md) | Decisões pendentes, sugestões e momento de decidir |
| [11-E1-REGIAO-INICIAL.md](11-E1-REGIAO-INICIAL.md) | E1: proposta da primeira região (Vale do Turvo), missão, comitiva, recompensas e percurso |
| [12-E1-CAMPANHA.md](12-E1-CAMPANHA.md) | E1: linha do tempo, Sigilos, protagonista, arco da campanha, finais, derrota, transição e o que decidir antes da E2 |
| [13-PENDENCIAS-FORA-DA-CAMPANHA.md](13-PENDENCIAS-FORA-DA-CAMPANHA.md) | Divergências entre documentação e código, e texto do prólogo; fora da campanha |
| [14-E5-DIAGNOSTICO-CLASSES.md](14-E5-DIAGNOSTICO-CLASSES.md) | E5: diagnóstico das três classes e seis especializações (sistemas conferidos, promessas × código, fichas, builds, progressão) e as prioridades da E5 |
| [15-E6-TRANSFORMACAO.md](15-E6-TRANSFORMACAO.md) | E6: a transformação de habilidade (a especificação; as decisões de Jean, o implementado na 1.62.0, o medido e o que falta jogar) |
| [16-E7-ITEM-E-LOOT.md](16-E7-ITEM-E-LOOT.md) | O saque do Vale medido (baús, suprimentos, equipamento, ouro), duas propostas de ajuste e a especificação da primeira entrega da E7 (o Broquel do Vigia), com as decisões pendentes |
| [17-E9-VALIDACAO-DO-VALE.md](17-E9-VALIDACAO-DO-VALE.md) | E9: avaliação integrada do Vale (percurso completo, encerramento, começo, ritmo e progressão), os achados por prioridade, as propostas, o roteiro de Jean e a ficha para jogadores novos; a partida de Jean, a recuperação, a nota da comitiva e o fim do capítulo (1.64.0), medidos antes e depois |
| [18-E9-ABERTURA-GUIADA.md](18-E9-ABERTURA-GUIADA.md) | E9: especificação da abertura guiada da campanha (caixa "Mostrar tutorial", a luta curta na despensa, Morel previsível, os quadros de orientação, mouse e teclado, salvar e carregar, escopo mínimo, critérios do teste) e a investigação de como a noite é percebida |
| [19-MERCADO.md](19-MERCADO.md) | O mercado com abas (Suprimentos, Equipamentos, Vender), a lista que rola sozinha, os motivos vindos do motor e a banca em pixel art (1.71.0); o acabamento das quantidades e do esgotado (1.73.0); a faixa única e a vendinha do Vale (1.74.0); a luz pelos períodos, a mão e a venda em grade (1.75.0) |
| [20-CENA-INTERATIVA-OSSUARIO.md](20-CENA-INTERATIVA-OSSUARIO.md) | As cenas interativas da Capela Afogada: o ossuário com o sarilho (1.72.0); o mapa dos cinco ambientes e seus gatilhos, o exterior, o salão alagado e a escada do ossuário (1.76.0); a cena no topo (1.77.0), a luz e as criaturas (1.78.0), a navegação entre as salas e os pontos sem nome fixo (1.79.0); a água atrás dos bancos, a referência de iluminação, o lodo no fundo e a saída para acampar (1.79.1 a 1.81.0); a sacristia e o fundo planejados |
| [21-DIAGNOSTICO-ATAQUES-EM-AREA.md](21-DIAGNOSTICO-ATAQUES-EM-AREA.md) | Os ataques em área dos inimigos: quem tem (só a Varredura dos guardiões) e quando usa, como os inimigos escolhem o alvo, o que protege o grupo hoje, quanto a comitiva apanha (medido), os candidatos coerentes e a recomendação de habilidade anunciada; só diagnóstico (1.82.0) |
| [22-HISTORIA-ILSE-E-A-AGUA-RASCUNHO.md](22-HISTORIA-ILSE-E-A-AGUA-RASCUNHO.md) | Discussão futura de Ilse, água e responsabilidade da vila; rascunho, sem mudança de cânone |
| [23-PLANO-DE-ARTE-INTERFACE-E-COMBATE.md](23-PLANO-DE-ARTE-INTERFACE-E-COMBATE.md) | Plano operacional atual: itens/ícones, clareza do combate, telas, serviços, cenários, habilidades e campanha; estados e próxima sequência |

## Estados e evidências

- **Decidido:** direção e escopo escolhidos por Jean.
- **Existe:** implementação observada na revisão; não significa validação nesta sessão.
- **Parcial:** infraestrutura útil, mas a experiência completa ainda falta.
- **Proposto:** desenho a testar ou escolher.
- **Concluído:** entrega implementada e validada com evidência registrada.
- **Futuro:** fora do ciclo inicial de campanha.

Não há porcentagens de conclusão nem testes declarados como aprovados sem execução. A revisão leu código e testes, mas não executou o jogo ou a suíte. A refatoração estrutural está entregue; conferir a validação atual com Claude.

## Limites da documentação

A revisão inicial de 09/10/2026 ficou restrita a Markdown em `roadmapIDEIAS/`. A organização aprovada em
17/10/2026 acrescenta o plano 23 e atualiza também o resumo correspondente em `docs/ROADMAP.md`, preservando as
etapas técnicas e as ideias anteriores.

Estes documentos não concedem autorização automática para implementar o plano inteiro. Seguir os guias técnicos e
o código atual quando Jean solicitar uma entrega; a atualização de documentação não altera regras, arte ou versão.

Mais classes, centenas de habilidades e várias gerações de evolução permanecem direção futura. A validação E9 do
Vale e das três classes atuais continua aberta.
