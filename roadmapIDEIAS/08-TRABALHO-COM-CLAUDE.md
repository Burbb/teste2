# 08 — Como trabalhar com Claude parte por parte

## Primeiro passo

Depois da refatoração, começar por E1: especificação da região. Ainda não criar seis classes, remover o procedural ou alterar o modelo de morte.

## Pedido inicial — planejamento

> Leia roadmapIDEIAS/README.md, 01-VISAO.md e 07-ETAPAS.md, além dos guias técnicos atuais do projeto. Quero trabalhar somente na E1: especificar uma região pequena que demonstre o RPG de campanha desejado. Nesta tarefa, não altere código nem o comportamento do jogo. Confira primeiro o que já existe e proponha um conflito local, percurso, alternativas, duas classes de teste, companheiros e consequências. Use nomes e exemplos provisórios quando não houver definição minha. Liste as decisões que dependem de mim e as tarefas pequenas necessárias. Não execute as outras etapas.

## Modelo para uma implementação autorizada por Jean

> Trabalhe apenas em [entrega específica], da etapa [E#]. Leia [arquivos de design pertinentes] e os guias técnicos atuais. Objetivo: [comportamento concreto]. Reaproveite [sistema existente]. Fora do escopo: [limites]. Preserve [comportamentos necessários]. Antes de implementar, confira o estado atual e explique dependências ou decisões ausentes. Não amplie a tarefa para outros sistemas. Valide com os checks pertinentes e descreva como eu testo jogando. Não atualize gabaritos para encobrir mudanças incidentais.

Esse modelo não concede autorização por si só: Jean precisa escolher e solicitar a implementação.

## Cartão de tarefa

- Etapa e objetivo:
- Problema observado:
- Comportamento desejado:
- Exemplo antes/depois:
- Dependências:
- Conteúdo e sistemas envolvidos:
- Fora do escopo:
- Critérios de conclusão:
- Como Jean testa:
- Decisões ainda abertas:

## Registro após jogar

- O que foi entregue:
- O que funcionou:
- O que ficou confuso:
- Onde houve repetição/atrito:
- Decisão: manter, ajustar ou retirar:
- Próxima tarefa pequena:

## Estados de uma ideia

**Ambição:** destino possível.
**Proposta:** desenho a testar.
**Decidido:** escolhido por Jean.
**Implementado:** presente no jogo, com validação técnica.
**Validado jogando:** passou pelo teste da experiência.

Não confundir esses estados. Exemplos deste conjunto de documentos não são lore, classes, números ou regras definitivos.

## Disciplina de escopo

- Uma entrega pequena por vez.
- Separar refatoração, conteúdo e balanceamento quando possível.
- Consultar os arquivos atuais antes de assumir que algo falta.
- Não criar infraestrutura genérica sem uso concreto.
- Usar checks do projeto para regras; jogar para avaliar experiência.
- Consolidar resultados antes de expandir quantidade.
- Atualizações destes documentos devem preservar o que foi decidido e identificar revisões.

## Divisão de trabalho

Jean define direção, avalia escolhas e joga.
Claude implementa tarefas autorizadas no estado atual do projeto.
ChatGPT organiza e refina design; nesta entrega, está autorizado somente a acrescentar esta pasta de documentos, sem modificar arquivos existentes.
