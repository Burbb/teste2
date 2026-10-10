# roadmapIDEIAS — Crônicas da Fenda

Revisão 2 — 09/10/2026. Plano de design e desenvolvimento atualizado após leitura estática do jogo refatorado (versão 1.46.0, commit d8d65b9778e85bb7eb8118fdd7a84acfd17e80ac).

## Direção e escopo acordados

RPG de campanha em fantasia sombria, por turnos, com história escrita, mundo que responde a decisões, companheiros e liberdade de build. Preservar cenários minimalistas, cards, texto, som e telas interativas.

**Três classes iniciais: Guerreiro, Arqueiro e Mago.** Reaproveitar as seis especializações existentes: Paladino, Berserker, Patrulheiro, Sombra, Piromante e Necromante. A sugestão anterior de reduzir a duas classes foi substituída pela decisão de Jean.

**Tecnologia:** manter Python no motor e HTML/CSS/JavaScript na interface local. A revisão não encontrou necessidade de migração. Não planejar troca de linguagem, framework ou engine como pré-requisito.

## Como seguir

Para uma nova conta ou sessão, começar por [00 — Comece aqui: continuidade](00-COMECE-AQUI.md). O arquivo registra a versão 1.47.1, as correções posteriores à revisão estática e o ponto de partida recomendado.

1. Ler [01 — Visão](01-VISAO.md) e [09 — Base existente](09-BASE-EXISTENTE.md).
2. Escolher uma entrega de [07 — Etapas](07-ETAPAS.md).
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
| [12-E1-CAMPANHA.md](12-E1-CAMPANHA.md) | E1: cronologia, protagonista, arco da campanha, finais, derrota e transição do procedural |
| [13-PENDENCIAS-FORA-DA-CAMPANHA.md](13-PENDENCIAS-FORA-DA-CAMPANHA.md) | Divergências entre documentação e código, e texto do prólogo; fora da campanha |

## Estados e evidências

- **Decidido:** direção e escopo escolhidos por Jean.
- **Existe:** implementação observada na revisão; não significa validação nesta sessão.
- **Parcial:** infraestrutura útil, mas a experiência completa ainda falta.
- **Proposto:** desenho a testar ou escolher.
- **Concluído:** entrega implementada e validada com evidência registrada.
- **Futuro:** fora do ciclo inicial de campanha.

Não há porcentagens de conclusão nem testes declarados como aprovados sem execução. A revisão leu código e testes, mas não executou o jogo ou a suíte. A refatoração estrutural está entregue; conferir a validação atual com Claude.

## Limites da atualização

Somente Markdown em roadmapIDEIAS. Nenhum arquivo fora desta pasta pode ser alterado por esta tarefa. Os documentos não concedem ao Claude autorização automática para implementar o plano inteiro. Seguir os guias técnicos atuais quando Jean solicitar uma implementação.

Não substituir docs/ROADMAP.md: ele trata da evolução técnica e contém notas que podem estar desatualizadas. O código atual deve ser conferido antes de cada tarefa.

Seis classes iniciais, centenas de habilidades e várias gerações de evolução permanecem ideias futuras. O resultado deste ciclo é uma campanha completa e consistente com as três classes atuais, não a reprodução da escala de Baldur's Gate ou Path of Exile.
