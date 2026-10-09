# 02 — Mundo, campanha e consequências

## Base que existe

Mapa em grafo, viagem, descoberta, clima, eventos condicionais, flags persistentes, consequências futuras por plantar/colher, contratos e histórias pessoais da comitiva. Tudo pode ser reaproveitado.

O início ainda chama gerar_mundo. Locais usam ids numéricos associados à posição na lista; existem convenções de vila inicial no índice zero e Cidadela no final. A campanha fixa precisa respeitar ou adaptar essas dependências explicitamente.

## Transição proposta

1. Definir uma região escrita.
2. Permitir carregá-la sem reconstruir mapa e viagem.
3. Separar cenas obrigatórias de encontros variáveis.
4. Implementar uma missão com duas soluções e consequência local.
5. Preservar caminhos de teste do modo atual durante a transição.
6. Retirar ou relegar o procedural somente quando a campanha puder substituí-lo.

Não é necessário trocar todos os ids do jogo de uma vez. Usar identificadores narrativos estáveis e uma forma consistente de resolver os locais quando a campanha exigir. Não depender do nome exibido como identidade de missão ou NPC.

## Cenas e eventos

Eventos atuais são funções registradas com contexto, condição, peso e repetição. Isso funciona para encontros e pequenas cenas. Histórias principais não devem depender apenas de uma rolagem para avançar.

Introduzir condições explícitas de disponibilidade, lugar e etapa para cenas escritas. Reutilizar a interface de cena/menu e os efeitos existentes. O mecanismo de eventos forçados também precisa respeitar o contexto necessário ao novo conteúdo; não presumir que ele já é um diretor completo de campanha.

Não converter todas as histórias existentes para um novo formato antes de demonstrar uma missão. Dados para requisitos/etapas/consequências podem conviver inicialmente com funções de cenas.

## Missão mínima

| Campo | Finalidade |
|---|---|
| Id estável | Reconhecer no save, Diário e condições |
| Estado/etapa | Disponível, ativa, etapa atual, concluída ou falhada |
| Condições | Quando aparece e quais soluções podem ser escolhidas |
| Objetivos | O que falta fazer, com texto claro |
| Transições | Qual ação leva a qual etapa |
| Resultado | Solução adotada e consequências persistentes |
| Recompensa | Evitar pagamento duplicado |
| Diário | Mostrar estado e objetivo corretos |

Contratos são um caso existente de objetivo e progresso; reaproveitar apresentação e funções úteis, sem forçar toda missão narrativa a caber em caça/alvo/entrega.

## Estados locais e facções

Escolher poucos estados por conflito. Exemplo provisório: uma vila protegida por soldados, sob influência de contrabandistas ou abandonada em parte. Cada estado muda falas, serviços, personagens ou caminhos.

Reputação atual é um número global. Reputação por facção é extensão futura próxima, a implementar apenas quando o conflito da região realmente usar duas relações diferentes. Definir como convive com a reputação global, sem apagá-la incidentalmente.

## Liberdade viável

Compartilhar pontos principais da história. Variar solução, custo, companhia e consequência. Uma ponte bloqueada pode ser atravessada por negociação, conhecimento militar, magia ou exploração. As alternativas podem levar à mesma cidade, em condições diferentes.

Classe pode oferecer ferramenta; origem, conhecimento ou contato; raça, relação cultural. Nem todo personagem precisa ver uma opção exclusiva em toda cena.

Oferecer ao menos uma solução geral para os objetivos obrigatórios. Falha de teste pode gerar complicação ou rota alternativa. Não prender uma classe por não possuir uma ferramenta exclusiva.

## Conteúdo e cronologia

Definir conflito central, regras da Fenda, cronologia e interesses dos personagens. Na base revisada, o prólogo fala em cem anos desde a abertura e Odette narra ter presenciado aquela noite: tratar como decisão de lore pendente.

Incluir personagens com objetivos próprios, lugares com hábitos e consequências percebidas ao retornar. Não exigir rotina simulada de todos os NPCs.

## Validação

Cobrir soluções alternativas, ordem diferente de objetivos, retorno após conclusão, pagamento único e save/load. Diário, cenas e serviços devem concordar. Testar a missão com as três classes, preservando alternativas acessíveis.

Ao ampliar capítulos, incluir decisões anteriores nos encontros e epílogos; não criar um final independente para cada combinação de flags.
