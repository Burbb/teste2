# 08 — Trabalho com Claude

## Primeiro pedido — E1, apenas planejamento

> Leia roadmapIDEIAS/README.md, 01-VISAO.md, 07-ETAPAS.md, 09-BASE-EXISTENTE.md e 10-DECISOES.md, além dos guias técnicos atuais. A refatoração terminou; informe a evidência de validação atual sem iniciar outra refatoração geral. Vamos manter Guerreiro, Arqueiro e Mago e suas seis especializações existentes. Trabalhe somente na E1: proponha uma região pequena com vila, áreas externas, masmorra, conflito local, duas soluções, consequência ao retornar e integração da comitiva. Esboce também o arco de início, meio e fim da campanha, sem escrever todos os capítulos. Não altere código nem comportamento. Se eu autorizar salvar o plano, use somente roadmapIDEIAS. Liste as decisões de design que preciso resolver e as entregas pequenas seguintes. Mantenha Python e a interface HTML/CSS/JS.

## Pedido de implementação — preencher antes

> Trabalhe somente em [subtarefa] da etapa [E#]. Objetivo: [comportamento]. Leia [documentos pertinentes] e os guias atuais. Reaproveite [sistema]. Fora do escopo: [limites]. Preserve [comportamentos]. Confira primeiro o código atual: não reconstrua algo pronto. Implemente apenas o solicitado, trate persistência quando necessária e valide com os checks pertinentes do projeto. Mostre como eu testo jogando e identifique limitações. Não execute a próxima etapa, não mude tecnologia e não atualize gabaritos para encobrir alterações incidentais.

## Pedidos pequenos de referência

| Etapa | Exemplo de uma única entrega |
|---|---|
| E2 | Carregar o mapa fixo aprovado preservando viagem e save |
| E3 | Persistir etapas da missão aprovada e exibir objetivo no Diário |
| E4 | Refletir resultado da missão em uma fala e um serviço da vila |
| E5 | Avaliar o ciclo do Piromante e propor ajuste sem implementar |
| E6 | Resolver uma transformação aprovada em execução e Grimório |
| E7 | Implementar um único aprovado usando gatilhos e descrição completa |
| E8 | Persistir uma origem e reconhecer uma opção de diálogo aprovada |
| E10 | Implementar somente o próximo trecho já especificado |
| E11 | Acrescentar um epílogo decorrente de uma decisão registrada |

Nenhum exemplo concede autorização por si só. Jean escolhe a etapa e a entrega.

## Cartão de tarefa

- Etapa/subtarefa e objetivo.
- Problema concreto e exemplo antes/depois.
- Sistema existente a reaproveitar.
- Regras de design decididas.
- Dependências e decisões ausentes.
- Arquivos/sistemas envolvidos e fora do escopo.
- Estado persistente/migração, se aplicável.
- Critérios de conclusão e verificações pertinentes.
- Cenário para Jean jogar.

## Registro após entrega

- Commit/versão e escopo.
- Validação técnica: o que foi executado e resultado.
- Avaliação de Jean: diversão, clareza, atrito e escolhas.
- Decisão: manter, ajustar ou retirar.
- Pendências e próxima subtarefa.

A leitura estática que originou esta revisão não substitui resultados de testes.

## Disciplina

Uma tarefa por vez. Diferenciar refatoração, mudança de regra e conteúdo. Não criar abstração sem primeiro caso concreto. Não repetir testes aprovados sem mudança ou preocupação nova. Seguir checks obrigatórios atuais para implementação.

Efeitos novos devem aparecer na interface e no save quando necessário. Uma chave declarada precisa ser consumida de fato; validar também comportamento, não apenas presença no catálogo.

## Responsabilidades

Jean decide direção e avalia jogando. Claude implementa o que Jean solicitar. ChatGPT refina design e revisa estrutura. Esta atualização está autorizada somente a editar/criar Markdown em roadmapIDEIAS; nenhum outro arquivo do projeto foi autorizado nesta tarefa.

## Como tratar decisões ausentes

Escolhas técnicas rotineiras podem seguir os padrões do projeto. Decisões que mudam a experiência — morte, quantidade preparada, raça, história, herança de classe — devem ser propostas claramente e resolvidas com Jean antes de implementar o comportamento dependente.

Exemplos provisórios não são nomes, lore, números ou regras definitivos.
