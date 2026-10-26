# 25 — Etapa 4: reforço, encantamento e identidade da progressão

Atualizado em 26/10/2026 após o debate com Jean sobre reforço e materiais. **Esta revisão altera somente documentação.** A forja H2 encerrou a etapa 3; combate e comitiva estão integrados até a 1.213.0. A etapa 4 continua aberta, agora com direção aprovada para um protótipo de reforço e materiais.

Esta revisão substitui a recomendação de aprovar a arquitetura A em bloco. A pesquisa, o levantamento da versão 1.210.0 e as propostas anteriores estão preservados no apêndice histórico. **Em caso de conflito, prevalecem as decisões e os estados descritos abaixo.** Números, receitas e fluxos do apêndice não são especificação de implementação.

## 1. Orientação geral do projeto — acordada com Jean

**O que existe no código mostra como o jogo funciona hoje, não determina como ele deverá funcionar no futuro.** Boa parte dos sistemas nasceu como uma base inicial para permitir jogar e testar. Ainda precisa de identidade, revisão e desenvolvimento.

Isso vale, entre outros, para:

- habilidades, talentos, especializações e sua progressão;
- comitiva, companheiros, suas habilidades, progressão, controle e participação no combate;
- atributos, prefixos, sufixos, afixos, propriedades de equipamento e sua variedade;
- reforço, encantamento, raridades, recompensas e economia;
- passagem do tempo, manhã, noite, turnos de dia e suas consequências;
- “Explorar região” e “Passear pela vila”, ainda muito preliminares;
- Bestiário e outros sistemas cuja presença no jogo não significa design definitivo.

Não preservar uma mecânica apenas porque ela já foi implementada. Não limitar novas propostas aos modificadores que o motor já suporta. Espinhos, regeneração e os demais efeitos atuais são exemplos disponíveis, não uma lista obrigatória, completa ou intocável.

Ao propor mudanças, distinguir:
1. funcionamento atual, confirmado no código;
2. identidade e experiência desejadas;
3. hipótese de design;
4. decisão expressamente aprovada;
5. implementação e validação.

**Abertura de design não é autorização para redesenhar tudo agora.** As revisões seguem o escopo combinado. Aprovações específicas de arte, interface e comportamento continuam valendo até serem revistas explicitamente; esta orientação não reabre automaticamente entregas aprovadas.

## 2. A campanha atual não é o tamanho-alvo

A primeira campanha continuará girando em torno da Ilse, mas acontecimentos, caminhos entre eles, dificuldades, atividades e duração serão ampliados e revistos. Jean relata concluir a versão atual em cerca de meia hora ou menos; isso é uma observação pessoal sobre o estado atual, não uma duração-alvo nem uma medida de jogador novo.

Não dimensionar toda a progressão para os atuais níveis, dias, locais, quantidade de lutas ou saldo final do Vale. Também não inventar uma duração futura como se estivesse aprovada.

Os dados atuais servem como diagnóstico e ponto de comparação. O orçamento futuro deverá considerar entradas e gastos de recursos ao longo da progressão, oportunidades de melhoria e necessidades concorrentes. **Saldo final de ouro não equivale a ouro total obtido nem a capacidade total de investimento.**

## 3. Camadas de construção do personagem — direção acordada

| Camada | Papel desejado |
|---|---|
| Classe e habilidades | Definir as ações e ferramentas disponíveis durante a luta. |
| Kit equipado | Escolher quais habilidades aprendidas levar e como elas se complementam. |
| Talentos e desenvolvimento de habilidades | Investir numa maneira de jogar e modificar o uso das habilidades. |
| Equipamento e suas propriedades | Oferecer descobertas, combinações e possibilidades de build. |
| Reforço | Aumentar a potência e prolongar a utilidade de uma peça escolhida, dentro do potencial a definir para ela. |
| Encantamento | Adaptar uma peça à maneira de lutar ou a um desafio. |
| Propriedade excepcional de item | Dar à descoberta rara uma identidade que possa orientar ou transformar uma build. |

Essas camadas podem compartilhar atributos e interagir. A intenção é evitar que todas repitam o mesmo aumento numérico sem decisões distintas. Não se exige que todo efeito seja complexo: ferramentas simples, baratas e confiáveis também têm valor.

### 3.1 Kit limitado e investimentos

**Acordado como direção:** o jogador escolhe um conjunto limitado de habilidades e onde investir seus pontos; não terá acesso simultâneo e irrestrito a tudo.

**Hipótese a definir:** até seis habilidades, incluindo uma ultimate. A interpretação inicial é cinco habilidades e uma ultimate, mas o número, a reserva desse espaço e as regras da ultimate ainda não estão fechados.

Aprender/desenvolver e equipar são decisões distintas. Aprender uma habilidade não deve significar obrigação de mantê-la no kit para sempre. Onde e com que condições o kit pode ser trocado continua aberto; troca fora de combate em lugar seguro é uma sugestão, não uma regra aprovada.

O limite de espaços sozinho não resolve equilíbrio: habilidades precisam competir por utilidades diferentes, custos, condições, confiabilidade e sinergias. A proposta permite habilidades fortes e divertidas, mas exige escolhas de kit e investimento; não garante equilíbrio apenas por limitar a quantidade.

### 3.2 Pequenos caminhos por habilidade

Jean propôs caminhos curtos de investimento associados a habilidades: avançar uma casa por vez, com modificadores que podem alterar sua utilização e favorecer conjuntos diferentes de habilidades.

**Hipótese:** até três melhorias numa sequência por habilidade. Ainda não estão definidos quantidade, custos, requisitos, disponibilidade de pontos, ramificações alternativas ou possibilidade de redistribuição. Não transformar automaticamente todas as habilidades em árvores idênticas de três casas.

A habilidade inicial deve ser funcional. Investimentos podem aprofundar sua proposta e mudar decisões em combate, sem fazer todos os caminhos serem uma taxa obrigatória para a habilidade começar a funcionar. Algumas habilidades podem exigir pouco investimento e servir de apoio; outras podem concentrar a build.

A ultimate terá sua identidade discutida: aquisição, disponibilidade, preparação, custo e oportunidade de uso. Nada disso está definido.

### 3.3 Identidade do combate — acordada

O combate deve ser divertido e desafiador, com **adaptação da própria combinação ao que os inimigos estão fazendo**, em vez de depender principalmente de executar uma sequência fixa sem reagir.

A apresentação por cartas não exige inventar posicionamento, distância, cones ou linhas para obter variedade. A profundidade pode vir de tempo, alvo, preparação, consumo de estados, recursos, compromissos, respostas e combinações curtas. Habilidades individualmente compreensíveis podem produzir decisões variadas quando interagem.

Preparações importantes dos inimigos devem ser sinalizadas, criando oportunidades de resposta; não é obrigatório revelar todo ataque comum. O grau exato de informação ainda será definido. Golpes devastadores precisam oferecer sinalização e possibilidade de reação, não apenas eliminar um personagem de surpresa. Inimigos simples continuam tendo lugar; a dificuldade não deve depender só de aumentar vida e dano.

Interromper, proteger, curar ou concentrar ataques podem ser respostas concorrentes à mesma ameaça. Ações, recursos e oportunidades limitados devem impedir que o grupo resolva sempre tudo ao mesmo tempo.

Os exemplos conversados (consumir queimadura, sacrificar servo, preparar contra-ataque, coordenar animal e herói etc.) ilustram possibilidades; **não são habilidades ou efeitos aprovados para implementação**.

### 3.4 Comitiva e progressão dos companheiros — acordadas

- O sistema atual de companhia/comitiva é um esboço, como os demais sistemas descritos na seção 1.
- **Grupo ativo: protagonista e no máximo dois companheiros em batalha.** Invocações e pets não ocupam essas duas vagas. Isso não aprova quantidade ilimitada de invocações/pets: seus limites permanecem abertos.
- **Controle direto dos companheiros principais pelo jogador.** A quantidade de opções e sua apresentação deverão manter o ritmo da luta.
- **Companheiros ganham níveis e desenvolvem habilidades.** Sua progressão deve ampliar possibilidades de uso, não apenas aumentar números.
- Companheiros mantêm identidade própria e um conjunto de decisões menor que o do protagonista. Não precisam repetir uma árvore ou ficha de igual complexidade; habilidades de apoio podem ser poderosas mesmo com poucas opções.
- O caminho exato de experiência, desbloqueios, escolhas de desenvolvimento e redistribuição ainda será definido. Evitar que deixar alguém fora do grupo o torne inviável ou exija repetir batalhas fracas para recuperá-lo; o mecanismo de recuperação não está decidido.
- Controle de animais e invocações é uma decisão separada. Ordens simples, comportamento automático ou comandos coletivos são possibilidades, ainda sem escolha.

**Morte e consequências:** companheiros não morrem permanentemente por uma derrota ou queda em batalha. Morte permanente pode ocorrer por rumo da história e consequências narrativas das decisões do jogador. Essa exceção não autoriza transformar uma queda comum em batalha em morte permanente. Durante a luta, o companheiro caído fica incapacitado e deixa de agir. Só retorna por uma habilidade de ressurreição de alto custo ou por um item realmente escasso; sem isso, permanece incapacitado até o fim da batalha. Ao retornar, conserva sua posição original na ordem e não recupera turnos perdidos. Valores, vida ao retornar, limites de uso e o caso de retornar antes ou depois da própria vez precisam ser especificados no teste. Recuperação, ferimentos e custos após a batalha continuam em aberto. Esta decisão trata dos companheiros; não altera por si só as regras de morte do protagonista ou dos modos de dificuldade.

### 3.5 Ordem das ações, turnos e rodadas — acordados

**Turnos individuais intercalados, com a ordem próxima visível.** Herói, companheiros e inimigos têm suas próprias vezes. Não é um turno coletivo em que todos os aliados agem antes de todos os inimigos; “intercalados” também não obriga alternância estrita aliado–inimigo.

**A Agilidade define a ordem inicial quando a batalha começa. Essa ordem permanece fixa durante toda a batalha**, repetindo-se nas rodadas seguintes. Não recalcular iniciativa a cada rodada nem reordenar personagens em consequência de mudanças de Agilidade durante a luta. Agilidade não concede ações extras neste modelo.

Distinguir na documentação, nos dados e na interface:

- **Turno individual:** a vez de um combatente.
- **Rodada:** o ciclo geral, que termina quando todos tiveram sua vez, inclusive quem não pôde agir por atordoamento ou outro impedimento.

Cada combatente tem uma vez por rodada. Perder a ação não deixa a rodada esperando por ele nem cria uma ação a recuperar depois. Os detalhes de derrota, saída, retorno, invocações e pets ainda precisam ser definidos: não inserir automaticamente um recém-chegado com ações adicionais ou reordenar os participantes existentes.

O modelo de rodada dá uma referência comum para efeitos, mas **não determina que todos os buffs, defesas e condições expirem no fim da rodada**. Durações devem dizer seu marco claramente: por exemplo, próximo turno do portador ou fim da rodada. A ordem de aplicação e expiração ainda precisa ser especificada por categoria de efeito, evitando o termo ambíguo “turno” para dois relógios diferentes.

Continuam abertos: desempates, quantidade de próximas posições mostradas, momento exato de leitura da Agilidade inicial (incluindo efeitos anteriores ao combate) e regras para participantes que entram ou saem durante a luta. A decisão não redefine os outros usos da Agilidade fora da iniciativa.

Aceleradores, atrasos ou trocas de posição na ordem não são uma extensão aprovada: contrariariam a ordem fixa combinada. Interrupções de preparações podem ser estudadas sem alterar a posição do alvo na sequência.

### 3.6 Estrutura do turno — direção aprovada

- **Uma ação principal por turno:** atacar, usar habilidade, defender ou usar consumível. Usar cura/consumível também disputa a oportunidade de atacar. Custos particulares, reações e exceções ainda não estão especificados; não acrescentar ações gratuitas por inferência.
- **Ataque básico útil:** opção confiável e econômica que continua tendo função depois dos primeiros níveis.
- **Defender como resposta real:** direção aprovada de reduzir o dano até o próximo turno daquele personagem, permitindo responder a ameaças anunciadas sem exigir uma composição específica. Valor da redução e marco preciso de expiração (por exemplo, início do próximo turno) continuam por definir.
- **Preparações perigosas com oportunidade de resposta:** sinalização deve permitir alguma reação real antes da resolução; avisar quando ninguém pode responder não basta.
- Evitar multiplicar ações pequenas obrigatórias antes de encerrar a vez. Cada turno deve concentrar uma decisão relevante.

### 3.7 Atributos do personagem e valores de combate — direção acordada

**Atributos representam capacidades do personagem dentro e fora das lutas; valores derivados mostram de forma direta o desempenho em combate.** As duas camadas devem coexistir com clareza: o jogador constrói capacidades e enxerga o resultado de atributos, equipamento, classe e efeitos sem precisar fazer contas manualmente.

Os atuais Ataque, Poder, Agilidade e Defesa não são uma lista definitiva de atributos primários. Ataque e proteção, por exemplo, podem ser resultados de outras escolhas. A relação exata será definida; não substituir ou renomear campos automaticamente.

- Atributos devem ter presença na aventura, nos testes e nas alternativas de resolução, além da luta.
- Situações podem admitir capacidades diferentes ou soluções por ferramenta, informação ou decisões anteriores. Não é obrigatório oferecer todas as alternativas em toda situação.
- Evitar que interação social seja uma única barreira de Carisma para todo conteúdo.
- Atributos não impõem personalidade: pouco conhecimento não obriga o personagem a ser bobo; pouca capacidade social não impede escolher uma fala inteligente. As decisões continuam com o jogador.
- A ficha deve mostrar claramente valores úteis como vida, proteção e desempenho ofensivo, mesmo quando derivados de outras capacidades.
- Baldur’s Gate 3 foi uma referência conceitual para capacidades dentro e fora do combate, não uma aprovação para copiar seus seis atributos, sua escala ou a conversão em modificadores.
- Não tentar tornar todos os atributos igualmente úteis a todas as classes; buscar mais de uma combinação razoável e evitar investimentos sem função.
- Habilidades, talentos e propriedades de equipamento continuam responsáveis por parte importante da identidade da build; não concentrar todas as escolhas nos atributos.

**Lista inicial aceita para o protótipo:** Força, Agilidade, Constituição, Intelecto, Percepção, Vontade e Presença. É uma base de trabalho para validar funções, não garantia de que sete atributos permanecerão na versão final. Distribuição de pontos, escala, progressão, fórmulas e valores continuam abertos; não introduzir agora uma camada extensa de perícias.

A decisão de Agilidade definir a iniciativa inicial fixa continua válida; discutir nomes ou derivações não autoriza ordem dinâmica nem ações extras.

#### Revisão após o primeiro teste — decisões de 25/10/2026

O primeiro protótipo foi entregue e jogado por Jean. **As decisões abaixo ainda não foram implementadas nele.** Substituem a direção anterior de concentrar atributos em efeitos indiretos e as funções da primeira lista de teste; a produção continua intacta.

**Potência e atributos:** atributos ofensivos devem contribuir diretamente para o dano correspondente, junto com arma/equipamento, nível e habilidade. Um investimento ofensivo precisa resultar numa melhora compreensível no combate. Não é obrigatório que todo atributo ou todo item aumente dano: sobrevivência, suporte e utilidade continuam valiosos. Evitar tanto um atributo que concentre todas as funções quanto distribuições diferentes que sejam indistinguíveis ao jogar. Especializar-se é válido; não se promete desempenho equivalente de qualquer distribuição.

**Sem desbloqueios por atingir X de atributo.** Retirar as regras do primeiro teste como Força 5 conceder imunidade a atordoamento, Constituição 5 encurtar sangramento, Percepção 5 ativar bônus de ponto fraco ou Vontade 5 transformar terror em outro efeito. Cada ponto deve contribuir gradualmente para a capacidade correspondente. Tetos de segurança não são desbloqueios; arredondamento não deve criar degraus artificiais de identidade nem esconder o benefício do investimento.

Mudanças de comportamento, imunidades temporárias e transformações de habilidades pertencem principalmente a habilidades, talentos e propriedades especiais de equipamentos. Não concedê-las automaticamente por pontuação de atributo.

| Capacidade | Direção atual | O que permanece aberto |
|---|---|---|
| Força | Potência física apropriada e esforço físico na aventura | Fórmula, peso e relação com armas/habilidades e rompimento de proteção |
| Agilidade | Ordem inicial fixa e capacidades físicas de coordenação na aventura | Outros usos precisam de justificativa; não acumular dano, crítico, esquiva e iniciativa automaticamente |
| Constituição | Vida e resistência corporal graduais | Pesos e tratamento de sangramento, veneno e doença |
| Intelecto | Participação na potência sobrenatural correspondente e compreensão/conhecimento | Mapeamento de magia, cura e invocações; não concentrar automaticamente dano, cura, eficiência e controle no mesmo atributo |
| Percepção | Precisão/vulnerabilidades e observação na aventura | Função ofensiva distinta e gradual, sem esconder ameaças essenciais |
| Vontade | Candidata ligada a determinação e resistência a controle | Precisa justificar sua utilidade; fórmula, abrangência e permanência ainda em validação |
| Presença | **Somente cenário, interações e situações fora do combate** | Distribuição/progressão e relação com o orçamento dos atributos de combate |

**Presença não escala dano, cura, buffs, Grito de Comando ou qualquer outro efeito de combate.** Pode servir à persuasão, negociação, intimidação e liderança narrativa, sem impor personalidade nem bloquear todo diálogo por um único teste. Não obrigar a comprar acesso narrativo sacrificando eficácia de luta sem uma decisão explícita sobre os orçamentos. No próximo teste, mantê-la fora do orçamento de combate; isso não fecha o sistema final de progressão social.

**Tenacidade:** direção a testar como chance de resistir a controles, com teto inferior à imunidade. Distinguir chance de resistir, redução de duração e resistência corporal; não juntar tudo num único benefício. Definir aplicação pelo atacante e resistência do alvo, mostrar a chance final e não contá-la duas vezes. Vontade é candidata a contribuir, não uma fórmula aprovada. A defesa contra uma ameaça não deve depender só de vencer um sorteio: proteger, defender ou outra resposta deliberada continua necessária.

**Duração:** não dar aumento percentual universal de duração por atributo. Em rodadas discretas, passar de duas para três é um salto grande. Um turno extra pode ser modificador explícito de uma habilidade, talento ou item especial, com alcance e custo próprios; não significa implementar esses efeitos agora.

**Leitura da build:** mostrar o resultado real da distribuição: dano previsto por habilidade, cura/proteção quando cabível, vida, recurso/custos, iniciativa, crítico e resistências. Informar a origem dos ganhos e comparar com a mesma arma, nível e alvo. Mudar atributos e não conseguir perceber a diferença é um problema do teste, mesmo quando as fórmulas estão corretas.

#### Contribuição dos companheiros fora da luta — acordada

Companheiros podem contribuir contextualmente em situações da aventura, permitindo complementar capacidades do protagonista. Não usar automaticamente o maior atributo do grupo em todo teste.

Um companheiro pode interpretar uma inscrição ou ajudar numa tarefa quando a situação permitir. Não escolhe pelo protagonista numa conversa íntima, numa decisão pessoal ou numa consequência narrativa que pertença a ele. A interação social não deve virar um imposto obrigatório de Presença no herói para acessar todo o conteúdo.

Não implementar agora revisão geral de diálogos, testes ou campanha. O protótipo pode demonstrar o princípio em exemplos isolados, identificados como provisórios; integração narrativa depende de trabalho posterior.

#### Retorno do teste e próxima iteração

Jean achou a luta divertida e aceitou o aumento de duração. Usou bastante ataque básico para reservar recurso a ameaças e cura; não percebeu claramente as diferenças entre as builds. Isso é diagnóstico de experiência, não aprovação dos custos ou prova de equilíbrio. Comparações de poucas partidas também sofrem influência de aprendizagem.

Na rodada anterior, a entrega definida foi uma **segunda versão isolada do protótipo**, preservando a primeira para comparação. Ela já foi entregue e jogada; a próxima iteração segue a seção 3.8. Deve testar potência ligada a atributos, benefícios graduais, Presença fora do combate e melhor leitura das builds. Rever a economia de recurso para permitir habilidades proativas e respostas de emergência sem transformar o básico numa espera obrigatória; não eliminar a necessidade de escolher quando gastar.

Jean reafirmou a intenção de selecionar habilidades com um orçamento de pontos, custos por tier e no máximo uma ultimate. Quantidade de pontos, tiers, limite de espaços (até seis continua hipótese), habilidades disponíveis e custos não estão fechados. Pontos de montar o kit, pontos de aprender/desenvolver e recurso gasto durante a luta são conceitos distintos.

**Hipótese operacional para esta iteração:** Ataque básico, Defender e Usar item são comandos básicos fora dos slots e pontos do kit; continuam consumindo a ação principal. Isso permite avaliar Defender sem cobrar uma vaga de habilidade. O protótipo não deve tratar essa configuração como catálogo definitivo. Um montador pequeno de kit pode testar pontos/tiers com poucas habilidades, incluindo opções baratas e fortes, sem construir ainda árvores completas ou o Grimório.

Preservar as decisões de turnos, companheiros, ameaças e ressurreição. A derrota imediata quando o protagonista cai, os desempates e a inserção de invocados do primeiro teste são hipóteses operacionais, não novas aprovações implícitas. Nenhuma revisão autoriza integração no jogo, reforço/encantamento completo ou expansão da campanha.

#### Segunda versão do protótipo — entregue para avaliação (26/10/2026)

Detalhes, fórmulas, ajustes dos inimigos e achados no [LEIA-ME](../ferramentas/prototipos/combate-atributos/LEIA-ME.md); o que comparar no [ROTEIRO](../ferramentas/prototipos/combate-atributos/ROTEIRO.md). A primeira versão continua jogável ao lado (`/v1/`). Nada integrado na produção.

- **Decisões aplicadas (desta seção):** Força e Intelecto entram direto na potência física e sobrenatural; nenhum desbloqueio por pontuação; benefícios graduais com tetos; Presença fora do orçamento e sem efeito de combate (o Grito de Comando ficou com bônus fixo); Tenacidade com teto e chance final mostrada; Agilidade só na ordem fixa; kit com pontos por tier e no máximo uma ultimate; Atacar, Defender e Usar item fora do kit, gastando a ação.
- **Hipóteses implementadas (provisórias, para avaliar):** escala 1–10 e 30 pontos de combate; +1 de potência por ponto de Força/Intelecto; crítico 2% e ponto fraco +4% por ponto de Percepção; 4 de vida e −4% de sangramento por ponto de Constituição; Tenacidade 4% por ponto de Vontade, até 40%, menos a aplicação do atacante, num sorteio só; 10 pontos de kit, até 6 espaços, tiers de 1, 2, 3 e 4 pontos; recurso 60, começa com 40, +8 por turno e +8 no básico; ultimate por Ímpeto (3, ganho com inimigo caído e ameaça desfeita ou aparada); interrupção uma vez por inimigo (depois a preparação é firme); quatro builds de teste (Força, Precisão, Runa, Baluarte) e uma comparação de arma e foco.
- **Resultados observados (poucas partidas, sem prova de equilíbrio):** as builds mudaram a escolha na mesma luta (quem matar primeiro, quem segura a ameaça, que golpe usar contra a guarda); gastar recurso desde o início não deixou o grupo sem resposta na primeira ameaça e criou custo na segunda; guardar recurso só alongou as lutas no teste automático; lutas de 9 a 15 rodadas nos encontros 2 e 3. A observar: a Percepção contra ponto fraco quase empata com a Força; o encontro 1 ficou curto; o Baluarte arrasta mais; a hora do Juramento.


### 3.8 Revisão após Jean jogar a v2 — direção aprovada para a v3

Esta seção prevalece sobre hipóteses da v2 em conflito. **Aprovação para testar numa terceira versão isolada, não para integrar nem fechar números.**

**Retorno:** Jean percebeu mais diferença entre builds, principalmente pelas habilidades levadas no kit. Considera válida uma build defensiva, mesmo não tendo jogado de Baluarte. Gostou da possibilidade de guerreiro com dano sobrenatural. Rejeitou o Ímpeto atual: não conseguiu usar ultimate.

O arquivo de sessão enviado por Jean contém quatro vitórias (6, 12, 12 e 10 rodadas), nenhuma ultimate usada; três dessas partidas tinham uma equipada e a de Precisão não. As duas lutas de 12 rodadas contra o Bruto registram zero preparações. Investigar comportamento e telemetria antes de concluir que as ameaças ou sua geração de Ímpeto funcionaram. Os totais não mostram quando houve recurso insuficiente; não inferir isso só por gasto acumulado.

**Tipo, escala e defesa:** toda habilidade deve explicitar o tipo de dano, o atributo/valor que aumenta sua potência e como interage com defesas. São eixos distintos: tipo determina resistência enfrentada; escala determina ganho ofensivo. Exemplos ilustrativos: Corte Preciso físico com Força e penetração definida; Lâmina Rúnica arcana com Intelecto; uma habilidade física de Baluarte com parcela da vida máxima. Nomes, coeficientes e penetração são de teste. Não tornar todo dano sobrenatural automaticamente imune a toda defesa.

**Resistências elementais:** testar redução percentual por elemento, vinda de equipamento e visível na ficha, com teto. Preparar-se para o elemento de uma região/chefe deve ter valor; não estabelecer como obrigação atingir todos os tetos no fim da campanha. Lista final de elementos, tetos, vulnerabilidades, penetração e ordem de cálculo continuam abertos. Resistência a dano não substitui Tenacidade contra controle. A próxima versão demonstra poucos tipos suficientes para avaliar, sem gerar catálogo de loot completo.

**Baluarte:** testar primeiro uma habilidade ofensiva própria que escale parcialmente com vida máxima. Não converter vida em bônus universal de dano. Ela deve contribuir para vencer sem fazer Constituição dominar simultaneamente ataque e sobrevivência. Talentos, itens excepcionais ou resposta baseada em dano bloqueado são possibilidades futuras, não entregas obrigatórias desta rodada.

**Reserva e sustentação:** nível e classe devem fornecer recurso básico suficiente para uma sequência central de habilidades. Testar Vontade aumentando recurso máximo, além da Tenacidade em avaliação. Não acrescentar Sabedoria agora, nem conceder automaticamente regeneração e resistência mágica a Vontade. Reserva sustenta uma sequência intensa; regeneração sustenta a luta longa. Fórmulas, recuperação entre lutas e pesos continuam provisórios. Investimento extra pode prolongar/repetir combinações; não deve ser requisito para o kit básico funcionar.

**Kit e especialização:** manter habilidades da classe inicial disponíveis depois da especialização; esta acrescenta possibilidades, não substitui todo o repertório. Cidades e acampamentos, fora de combate, são a direção inicial para trocar kit. Não implementar esses locais na campanha nesta rodada. Ampliar o teste por poucas combinações completas (por exemplo aplicar/consumir queimadura), não por dezenas de habilidades isoladas. Progressão de aprendizado/talentos e números de pontos/slots continuam abertos.

**Ultimate:** retirar Ímpeto na v3. Testar uma utilização por combatente por combate da ultimate equipada, disponível desde o início, consumindo ação e recurso com custo viável. Continua no máximo uma equipada. Sem recarga por dormir, abates ou sorte; não exigir espera em rodadas para liberar. Momento de uso deve vir do efeito e das oportunidades: preparação, proteção, estados acumulados ou ataque. Se usar sempre na abertura dominar, rever efeito/custo antes de criar outra trava geral. Não significa que todos os companheiros já tenham ultimate. Voltar de incapacitação não reinicia o uso da mesma luta.

**Escopo:** preservar v1/v2 como comparação; criar v3, verificar dados reais versus previsões e registrar hipóteses. Não integrar produção, redesenhar HUD final, expandir narrativa nem implementar reforço/encantamento completo. A imunidade permanente a interrupção após o primeiro uso continua hipótese não aprovada: investigar junto das ameaças do Bruto, sem declará-la regra definitiva.

#### Terceira versão do protótipo — entregue para avaliação (26/10/2026)

Detalhes no [LEIA-ME](../ferramentas/prototipos/combate-atributos/LEIA-ME.md); o que testar no [ROTEIRO](../ferramentas/prototipos/combate-atributos/ROTEIRO.md). v1 e v2 continuam jogáveis (`/v1/`, `/v2/`). Nada integrado.

- **Investigação das ameaças do Bruto (resultado):** as duas lutas do arquivo de Jean registraram zero preparações porque, na v2, a preparação estava presa ao número da rodada; o Bruto é o último da ordem, e o Golpe no Joelho e o Golpe de Escudo caíram nas rodadas de preparação, fazendo-o perder a vez e apagando o ciclo (reproduzido). Não foi falha da contagem das preparações; havia, sim, uma lacuna: controles aplicados em inimigos não eram contados. O atordoamento "100%" do Morel batia com 5% de chance de resistir. A regra "firme depois da primeira interrupção" nunca entrou em jogo e não era necessária: retirada.
- **Decisões aplicadas (desta seção):** tipo, escala e defesa explícitos por habilidade; dano arcano enfrenta resistência, não ignora tudo; resistências por tipo com teto, vindas do equipamento, separadas da Tenacidade; habilidade ofensiva do Baluarte pela vida máxima sem bônus global; Vontade aumentando a reserva; reserva e regeneração distintas; combinação aplicar/consumir queimadura numa especialização que soma ao repertório; kit trocado fora da luta; ultimate sem Ímpeto, uma utilização por luta, desde o início, com recurso, sem devolver por queda e retorno.
- **Hipóteses numéricas (provisórias):** preparação por turno agido (atordoar adia); golpe específico ininterruptível sinalizado (Bruto abaixo da metade da vida); Tenacidade do Bruto 30%; resistências arcano e fogo com teto 60%, manto de 35%; ordem de cálculo potência → habilidade → consumo → bônus somados → crítico → Guarda → reduções → uma defesa do tipo → mínimo 1 → escudo; ponto fraco 3% por ponto de Percepção; recurso 40 + 4 × nível + 3 × Vontade, cheio no início, +6 por turno e +6 no básico; Avanço do Baluarte = nível + 25% da vida máxima; Queimadura em pilhas (até 3) de 30% da potência por 3 pingos, Combustão +200% do restante; ultimate 30 de recurso; Fúria e Tempestade com golpe base menor e +100% contra quem prepara ou tem estado; Odette com uma ultimate para testar queda e retorno.
- **Resultados observados (poucas partidas, sem prova de equilíbrio):** o Avanço deu ao Baluarte uma decisão própria (puxar o Golpe Esmagador e ainda bater), com custo real em vida; a combinação de Queimadura precisou de 3 pingos para preparar dois alvos para a Conflagração; o manto de fogo reduziu à metade o fogo recebido por Jean no encontro dos Cães e não muda os outros; com a ultimate disponível desde o início, Fúria e Tempestade valiam mais na abertura até o efeito mudar; depois, sem dominância clara na medição automática, e o Juramento rende mais na hora da ameaça; as ameaças do Bruto aparecem (3 a 4 por luta) com interrupções, resoluções e adiamentos registrados. A observar: encontro 1 curto com a reserva cheia; o Baluarte mais lento; se tipo e defesa ficaram claros sem poluir os botões.


### 3.9 Retorno de Jean sobre a v3 — rodada local aprovada

**Leitura dos ataques básicos:** Jean esclareceu que, quando considera a vitória garantida, termina usando ataques básicos por conveniência. Frequência alta de básicos não prova falta de recurso, opções ou interesse. Observar momento e recurso disponível, junto do relato. No arquivo `resultados(3).json`, Baluarte contra o Bruto usa quatro Avanços nas primeiras cinco rodadas e depois básicos com recurso crescente; Chama contra o Xamã usa cinco Brasas e duas Combustões, sem básico do protagonista. São exemplos de experiência, não prova geral de equilíbrio.

**Marca do Morel:** retirar da próxima candidata do protótipo. Jean considera a habilidade uma preparação repetitiva que vira obrigação. Não substituir por bônus equivalente renomeado nem preencher a vaga por obrigação. Isso não proíbe toda mecânica futura de marca nem autoriza remover conteúdo de produção.

**Completar o conjunto de fogo:** testar uma habilidade comum de área que cause pouco dano direto e aplique uma camada de Queimadura em cada inimigo válido, garantida salvo imunidade explícita. Resistência a fogo reduz o dano e não ganha automaticamente uma segunda função de impedir aplicação. Não criar imunidades novas só para esta rodada.

Papéis aprovados para o teste:
- Brasa: aplicação concentrada e econômica num alvo.
- Nova habilidade de área: preparação de vários alvos, custo maior que Brasa e espaço/pontos no kit.
- Combustão: consumir Queimadura de um alvo.
- Conflagração (ultimate): consumir Queimadura de todos os inimigos afetados, uma vez por combate.

Nome, tier, custos e coeficientes da habilidade nova são provisórios. Manter utilidade da Brasa contra alvo único. Conferir a sequência de preparar o grupo e consumir antes da expiração, com resistência calculada corretamente e sem duplicar dano já ocorrido.

**Escopo:** rodada pequena e isolada, preservando a v3 para comparação. Remover a Marca, completar o conjunto de fogo e registrar a observação sobre os básicos. Demais regras, encontros e economia ficam como estão salvo correção necessária e explicada. Não integrar produção, revisar todas as classes nem declarar a etapa 4 concluída.

#### Quarta versão do protótipo — entregue para avaliação (26/10/2026)

Detalhes no [LEIA-ME](../ferramentas/prototipos/combate-atributos/LEIA-ME.md); o que testar no [ROTEIRO](../ferramentas/prototipos/combate-atributos/ROTEIRO.md). A v3 continua jogável em `/v3/` (e v2, v1). Nada integrado.

- **Decisões aplicadas (desta seção):** a leitura dos ataques básicos registrada, sem rebalancear recurso nem duração por causa deles; a Marca retirada da candidata (as versões anteriores e a produção não mudam); a habilidade de fogo em área com uma camada de Queimadura garantida em cada inimigo, sem imunidade nova, a resistência reduzindo só o dano; os papéis de Brasa, área, Combustão e Conflagração mantidos (Brasa, Combustão e Conflagração da v3 já os cumpriam e ficaram iguais).
- **Sobre a vaga da Marca:** esta seção pedia para não preenchê-la por obrigação; na conversa da entrega, Jean pediu uma habilidade nova para testar no lugar. Foi feita como golpe de efeito imediato, não como preparação nem Marca renomeada, e segue em teste.
- **Valores provisórios:** Chuva de Brasas (fogo, foco + nível + Intelecto × 0,35, tier 2, 22 de recurso, 1 pilha em cada inimigo); Golpe Oportuno do Morel (físico × 1,2, 15 de recurso, +60% em quem está atordoado ou preparando); kit sugerido da Chama: Brasa, Chuva, Combustão, Proteger, Conflagração.
- **Resultados observados (alvos parados, mesma build):** num alvo, Brasa → Combustão rende 44 por 32 de recurso e a Chuva → Combustão 39 por 42 (a Brasa continua melhor); no grupo de três, Chuva → Conflagração faz 108 em 2 ações (52) e três Brasas → Conflagração os mesmos 108 em 4 ações (66); contra 60% de fogo, a Queimadura pega e o dano cai para cerca de um terço. A reserva básica da Chama (67) comporta a sequência, que funciona num encontro normal antes da expiração. Falta Jean dizer se o Golpe Oportuno vira obrigação como a Marca.


### 3.10 Estrutura aprovada e integração autorizada após a v4

Jean aprovou seguir para o jogo real, testando chefe e lutas consecutivas na campanha, sem exigir outra rodada isolada. Relatou que as lutas parecem longas; reduzir trechos repetitivos e a demora após o confronto já estar decidido é objetivo da integração, sem atribuir seu uso de básicos a falta de recurso.

**Autorização atual:** integrar a estrutura de combate descrita nas seções 3.3–3.9, adaptada às classes e sistemas reais, e criar repertório provisório pesquisado. Esta seção substitui as restrições anteriores de “somente protótipo” para esse escopo. Não aprova automaticamente todos os valores, habilidades e exceções introduzidos pelo laboratório.

Estrutura aprovada: iniciativa inicial fixa por Agilidade; turnos individuais e rodadas; uma ação principal; até dois companheiros principais controláveis; queda e ressurreição conforme acordado; kit limitado por orçamento e espaços; comandos básicos fora do kit; escalas e tipos explícitos; atributos graduais; resistências; combinações de estados; até uma ultimate equipada, uma utilização por combate, sem Ímpeto. Presença continua somente na aventura. Fórmulas, custos, tetos, slots, pontos e catálogo permanecem ajustáveis.

**Classes reais — esclarecimento expresso de Jean:** manter as habilidades arcanas do Guerreiro do laboratório, incluindo Lâmina Rúnica e as demais opções arcanas pertinentes, permitindo a build de guerreiro mágico com Intelecto. Retirar dele somente o conjunto de fogo (Brasa, Chuva de Brasas, Combustão e Conflagração) e levá-lo ao repertório apropriado de Mago/Piromante, respeitando aprendizado e especialização. Não eliminar o Guerreiro arcano ao adaptar as classes reais; isso também não libera todo o catálogo entre classes.

**Repertório provisório:** referência inicial de cerca de 8–10 habilidades comuns por classe, contando existentes pertinentes; aprendizado progressivo, não todas no nível inicial. Especializações acrescentam conjuntos menores próprios e ultimate, sem retirar as habilidades iniciais. Pesquisar referências por função e escolher efeitos compatíveis com combate sem posicionamento. Buscar ao menos duas combinações por classe, opções econômicas e ferramentas independentes; não criar rotações obrigatórias. Quantidade é alvo de trabalho, não quota para encher com efeitos redundantes. Talentos completos, catálogo final e arte nova não fazem parte desta autorização.

**Continuidade obrigatória:** antes de integrar, escolher e documentar regras provisórias explícitas para vida, recursos, companheiros caídos, consumíveis e disponibilidade da ultimate entre combates; aprendizado e troca de kit nas cidades/acampamentos. Claude pode resolver escolhas operacionais coerentes com as decisões e testá-las, sem apresentar números como design final. Não deixar a campanha depender do reinício cheio do laboratório.

**Integração completa no escopo:** adaptar inimigos, companheiros reais, pets/invocações existentes, equipamentos/afixos, progressão, interface e modos suportados onde dependam do combate, sem criar novos subsistemas desnecessários. Tratar saves deliberadamente, sem apagar arquivos pessoais ou prometer compatibilidade não testada. Preservar narrativa e aprovações visuais, salvo mudanças de interface necessárias ao funcionamento.

**Validação:** percursos reais com as três classes, ao menos um chefe e sequência de encontros sem reinício artificial. Medir rodadas, ações e tempo ativo separadamente de animações/pausas; registrar fase final de baixo risco quando observável. Lutas comuns podem ser curtas; desafios podem durar mais. Comparar mesmas condições e investigar diferenças de gabarito. A integração não encerra a etapa 4 nem autoriza implementar reforço/encantamento completo, árvores extensas de talentos ou expansão narrativa.

## 4. Vida útil das peças — direção acordada

O caminho escolhido é **um meio-termo entre substituição constante e levar qualquer peça indefinidamente**, com espaço para apego a boas descobertas.

Distinguir três situações de uso, sem criar novas raridades automaticamente:

- **Peça de passagem:** atende à necessidade atual e depois é substituída.
- **Boa peça especializada:** combina propriedades úteis e pode justificar investimento por várias aventuras.
- **Peça excepcional:** traz uma linha ou modificador particular capaz de orientar a seleção de habilidades, talentos e outros equipamentos.

**As peças capazes de sustentar esse apego longo precisam ser de fato raras.** Nem toda peça deve acompanhar a campanha indefinidamente apenas por ter recebido reforços. Uma descoberta excepcional pode justificar meios especiais ou mais caros de continuar relevante; a mecânica desses meios está aberta.

A raridade exata dessas descobertas, suas fontes e sua correspondência com as categorias atuais ainda serão definidas. Não confundir “rara” no sentido de pouco frequente com uma decisão automática sobre o tier chamado Raro.

A build deve poder começar a funcionar com habilidades e talentos. Um item excepcional pode transformá-la ou abrir uma variação desejada, sem obrigar o jogador a esperar por um drop específico para conseguir jogar sua proposta básica.

## 5. Reforço, materiais e encantamento — decisões de 26/10/2026

As decisões abaixo substituem os pontos antes abertos correspondentes; não aprovam a antiga arquitetura A em bloco.

### 5.1 Reforço e vida útil — aprovados como direção

- O reforço melhora a função principal da peça: dano físico e/ou potência arcana nas armas conforme sua identidade; proteção nas armaduras; propriedade principal definida para cada tipo de apoio.
- Não aumentar automaticamente todos os atributos, afixos, crítico, roubo de vida ou modificadores especiais junto com o reforço. O mapeamento por tipo de peça será explicitado e testado.
- Separar qualidade da base e nível de reforço. Uma peça inicial reforçada pode competir por um período com uma nova base melhor, mas nem toda peça inicial deve acompanhar indefinidamente a campanha.
- Peças excepcionais poderão elevar sua base em momentos posteriores da campanha, mediante investimento e material mais raro, preservando a identidade que sustenta a build. É uma direção futura aprovada, não serviço a implementar nesta rodada. Critérios de elegibilidade, marcos, tratamento do reforço existente e custos permanecem abertos.
- Reforço comum garantido, sem falha, quebra ou perda de níveis.
- Ao substituir uma peça, desmontá-la permite recuperar parte dos materiais investidos no reforço. O jogador também pode guardar para outro companheiro ou vender. Não transferir automaticamente o +N para a substituta.
- Percentuais de recuperação, materiais próprios da peça, eventual recuperação de ouro, preços, fórmulas, espaços elegíveis e limites ainda precisam de teste. +5/+10 e 20% não são decisões finais.
- A espada que faz Lâmina Rúnica atingir um segundo alvo foi um exemplo de peça excepcional; não constitui aprovação de novo item ou habilidade.

### 5.2 Materiais — categoria aprovada

Adicionar materiais como categoria pequena e funcional, conforme a necessidade real dos serviços, sem dezenas de ingredientes antecipados.

Três funções estão identificadas, não três materiais específicos já definidos:
1. reforço comum: ouro mais material de reforço;
2. elevação futura de bases excepcionais: material mais raro ligado a avanço e desafios;
3. encantamento: materiais ou essências a definir junto do sistema.

- Materiais compartilhados pelo grupo, contados em pilhas numa seção “Materiais” do inventário, fora dos 12 espaços da bolsa.
- Aparecem nas recompensas com nome, ícone e quantidade. A forja mostra posse, custo e falta; a descrição informa uso e fontes conhecidas.
- Exploração, recompensas e desmontagem podem fornecer materiais. Desmontar não será a única fonte: quem ainda não tem equipamento sobrando precisa poder experimentar reforço.
- Ouro continua relevante e concorre com outros gastos. Não balancear apenas pelo saldo ao fim do Vale atual.
- Não criar mineração, coleta manual ou profissões nesta rodada. Não criar material por classe ou slot sem escolha relevante que justifique.
- Quantidades, nomes, fontes concretas, raridade e desbloqueios são hipóteses para avaliar, não conteúdo aprovado da campanha.

### 5.3 Encantamento — direção preservada, regras adiadas

Encantar adapta a peça à build ou a um desafio; não deve apagar facilmente propriedades excepcionais. Não limitar efeitos ao catálogo atual.

Continuam para debate com Jean: quantidade por peça, efeitos e combinações, descoberta/receitas, consumo e recuperação de essências, remoção/substituição e local do serviço. Não implementar o sistema nem os dezessete efeitos do apêndice por inferência.

### 5.4 Próxima entrega — protótipo isolado

Jean testou o inventário da comitiva na 1.213.0 e relatou que está funcionando bem até aqui; a frente pode seguir. Isso não declara todos os números de combate definitivos.

Próximo lote: verificar implicações no catálogo atual e construir um protótipo jogável de reforço garantido, materiais compartilhados e desmontagem com recuperação parcial. Fórmulas, custos e quantidades devem estar identificados como provisórios e comparados com exemplos reais de equipamento e combate, incluindo companheiros.

A demonstração deve permitir investir numa peça, comparar uma substituta, escolher guardar/vender/desmontar e verificar a recuperação. Usar saves temporários; manter o jogo de produção intacto até avaliação. A elevação de base excepcional fica descrita com exemplos numéricos, sem um serviço funcional nesta rodada; encantamento segue para conversa própria.

Usar a forja e componentes aprovados, sem redesenhar ambiente, personagem ou inventário inteiro e sem arte/cerimônia final antes das regras. Não gerar vídeos sem pedido.

Registrar escolhas de teste, resultados e pendências no LEIA-ME, no plano e na continuidade. A etapa 4 permanece aberta.

## 6. Pontos que a proposta anterior precisa resolver

1. **Arredondamento e ganho:** incremento percentual arredondado a cada nível pode deixar atributos pequenos sem crescer; mínimo +1 pode causar ganho relativo excessivo. Comparar resultados acumulados e exemplos de bases diferentes antes de escolher fórmula.
2. **Consumo de encantamento:** perder uma essência rara ao trocar equipamento pode recriar o receio de investir. Remover gratuitamente não significa experimentar gratuitamente se a essência é destruída.
3. **Economia:** considerar fluxo de ganhos e gastos, não só saldo de uma partida. Não usar o robô aleatório como representação da experiência humana.
4. **Espaços e acúmulo:** resolver a abrangência dos serviços e evitar escolhas sem benefício, como aplicar um segundo efeito que não conta sem explicação prévia.
5. **Variedade:** não aprovar dezessete essências apenas porque há código para elas. Primeiro definir experiências e escolhas desejadas; depois selecionar exemplos para teste. Um protótipo pequeno não limita o catálogo final.
6. **Gestos:** um clique duplo ou tecla segurada não pode comprar duas melhorias, mesmo que ainda existam recursos. Uma segunda compra requer nova ação deliberada, preservando compras sucessivas intencionais.
7. **Comparação de builds:** verificar escolhas dominantes e interações entre kit, talentos e equipamento; não depender apenas de reduzir valores de efeitos existentes.

## 7. Referências e método de decisão

A pesquisa original permanece útil como repertório, não como arquitetura obrigatória. ARPGs e MMOs podem inspirar aspectos específicos, mas não determinam o volume de loot, materiais, repetição ou ritmo da nossa campanha por turnos.

Incluir referências de escopo e ritmo mais próximos, como RPGs por turnos com preparação, exploração e recursos limitados. Não exigir correspondência exata de estética ou gênero para aproveitar uma ideia.

Na conversa, **Battle Brothers** acrescentou o exemplo de materiais de criaturas associados a melhorias com funções específicas. Fonte primária: [Dev Blog #103: Crafting](https://battlebrothersgame.com/dev-blog-103-crafting/). A aplicação sugerida ao nosso projeto é ligar descobertas e melhorias à aventura, sem copiar seu sistema completo. **Stoneshard** foi indicado como referência a aprofundar, não como sistema já escolhido.

As generalizações do apêndice sobre aleatoriedade, destruição e satisfação são avaliações da pesquisa inicial, não leis de design nem prova de que uma mecânica só funciona em determinado gênero. Verificar versões e fontes antes de usar mudanças de outros jogos como justificativa decisiva.

**Marco anterior concluído:** integrar a estrutura da seção 3.10 e testar na campanha. **Próximo passo atual:** protótipo de reforço, materiais e desmontagem, no escopo da seção 5.4.

**Integração feita na 1.211.0** (26/10/2026): o combate da seção 3.10 está na campanha, com o repertório provisório,
a continuidade entre lutas e o ritmo medido. Escolhas, conversões, catálogo, medidas e roteiro no
[26](26-INTEGRACAO-DO-COMBATE.md). Jean já jogou e pediu os ajustes registrados a seguir; o orçamento do kit e o desempenho do Necromante contra chefes continuam provisórios. Reforço e encantamento completos continuam fora.

**Ajustes da 1.212.0** (26/10/2026), depois do teste do Jean: a Queimadura contra resistência, a leitura das
descrições, os atributos e o kit à vista, a debandada rara e a observação do Golpe Pesado ([26](26-INTEGRACAO-DO-COMBATE.md#ajustes-da-1212-depois-do-teste-do-jean)).
**Comitiva integrada na 1.213.0** (26/10/2026): equipamento individual, atributos com 1 ponto livre por nível do
herói e a sugestão sob pedido, a bolsa do grupo e uma regra única para vestir e trocar peças, na janela do Inventário
([26](26-INTEGRACAO-DO-COMBATE.md#a-comitiva-integrada-e-os-refinamentos-da-hud-1213)). Números provisórios.

Depois de definida a direção suficiente, o Claude poderá verificar implicações técnicas, testar hipóteses numéricas e construir um protótipo isolado e pequeno. O catálogo e o combate atuais servirão de casos de teste, sem limitar as possibilidades futuras.

## 8. Estado das decisões

| Assunto | Estado |
|---|---|
| Sistemas existentes como rascunhos, não limites definitivos | Acordado; orientação geral do projeto |
| Expansão e revisão da campanha centrada na Ilse | Direção acordada; duração e conteúdo por definir |
| Combate de preparação, resposta e adaptação aos inimigos | Direção acordada |
| Preparações inimigas importantes sinalizadas | Direção acordada; grau de informação aberto |
| Comitiva atual como esboço | Acordado |
| Protagonista + até dois companheiros ativos | Acordado; pets e invocações fora dessas vagas |
| Controle direto dos companheiros principais | Acordado |
| Níveis e desenvolvimento de habilidades dos companheiros | Direção acordada; regras e valores abertos |
| Sem morte permanente de companheiros por batalha | Acordado; exceção somente narrativa |
| Retorno à luta por ressurreição de alto custo ou item escasso | Acordado; números e limites abertos |
| Retorno na posição original, sem recuperar turnos perdidos | Acordado |
| Protótipo isolado de combate antes da forja | Ciclo v1–v4 concluído e estrutura integrada na 1.211.0; ajustes até 1.213.0 no documento 26 |
| Turnos individuais intercalados e ordem próxima visível | Acordado |
| Agilidade define a ordem inicial | Acordado; desempates e detalhes de leitura abertos |
| Ordem fixa durante toda a batalha | Acordado; sem ações extras por Agilidade |
| Rodada termina após todos terem sua vez, incluindo ações perdidas | Acordado |
| Uma ação principal por turno | Direção aprovada |
| Ataque básico útil e defesa até o próximo turno do personagem | Direção aprovada; valores e marcos precisos abertos |
| Controle e limite de pets/invocações | Em debate |
| Atributos para capacidades dentro e fora do combate | Direção acordada |
| Valores derivados para leitura clara do desempenho em combate | Direção acordada |
| Força, Agilidade, Constituição, Intelecto, Percepção, Vontade e Presença | Lista inicial aceita para teste; permanência final sujeita à validação |
| Funções dos atributos | Revisadas após teste na seção 3.7; Presença somente fora do combate, Vontade em validação |
| Contribuição contextual de companheiros na aventura | Acordado; sem substituir decisões pessoais do protagonista |
| Evitar atributo único obrigatório por classe | Princípio acordado, aplicado a físicos e sobrenaturais |
| Atributos ofensivos contribuindo diretamente para dano | Acordado; fórmulas e pesos provisórios no próximo teste |
| Desbloqueios ou imunidades por atingir X de atributo | Rejeitados; retirar do protótipo |
| Presença somente no cenário e nas interações | Acordado; sem efeito de combate |
| Tenacidade gradual com teto, sem imunidade automática | Direção de teste; na segunda versão: 4% por ponto de Vontade até 40%, menos a aplicação do atacante (hipótese, não aprovada) |
| Comandos básicos fora dos slots e pontos do kit | Aprovado para integração; consomem ação |
| Orçamento de seleção de habilidades por tier, até uma ultimate | Direção acordada; na segunda versão: 10 pontos, até 6 espaços, tiers de 1 a 4 pontos, Ímpeto rejeitado após teste; v3 usa uma ultimate por combate (demais números provisórios) |
| Kit limitado e investimento seletivo | Direção acordada |
| Cinco habilidades + uma ultimate | Hipótese, não número fechado |
| Caminhos curtos de modificadores por habilidade | Direção acordada; três passos é hipótese |
| Peças de passagem e descobertas excepcionais duradouras | Direção acordada |
| Peças que orientam builds serem realmente pouco frequentes | Direção acordada; taxas e tiers abertos |
| Reforço, encantamento e propriedade excepcional com papéis distintos | Direção acordada |
| Arquitetura A anterior, 20%, +5, preços e 17 essências | Proposta histórica, não aprovada em bloco |
| Reforço garantido e função principal da peça | Direção aprovada; fórmula, slots e limites para teste |
| Desmontagem e recuperação parcial de materiais de reforço | Aprovadas como direção; taxas provisórias; sem transferência automática do +N |
| Materiais do grupo fora dos 12 espaços | Aprovado; seção Materiais, ouro + material no reforço |
| Elevação de base de peças excepcionais | Direção futura aprovada; não implementar nesta rodada |
| Encantamento, essências e receitas | Debate posterior; sem implementação autorizada |
| Próxima entrega | Protótipo isolado da seção 5.4; avaliação antes da produção |
| Tipos de dano, escalas e resistências explícitos | Direção aprovada para v3; fórmulas e catálogo provisórios |
| Vontade aumentando reserva de recurso | Aprovado para teste; sem Sabedoria nova nem regeneração automática |
| Baluarte com habilidade baseada parcialmente em vida | Aprovado para teste, não bônus universal |
| Ultimate uma vez por combate, sem Ímpeto | Aprovado para teste; ação e custo de recurso viável |
| Habilidades iniciais mantidas após especialização | Direção aprovada |
| Troca de kit em cidades/acampamentos fora de combate | Aprovada para integração; regras operacionais documentadas |
| Integração do combate e repertório provisório | Autorizada após v4, no escopo da seção 3.10; sem arte final nova ou sistemas fora dele |

## Apêndice — pesquisa e proposta inicial, preservadas como histórico

O texto abaixo registra o levantamento e as hipóteses anteriores à revisão com Jean. Seus trechos “recomendo”, “para nós”, “primeiro protótipo” e “o que depende do Jean” pertencem àquela rodada e não substituem o estado atual acima. Os dados de código são um retrato da 1.210.0; os exemplos numéricos não são o alvo futuro da campanha.

<details>
<summary>Abrir levantamento, fontes e arquitetura inicial (histórico)</summary>

# 25 — Etapa 4: reforço e encantamento (pesquisa e proposta)

25/10/2026. Pesquisa e proposta de design, **sem implementação**: nada aqui mudou regra, número ou tela do jogo. Os
números são hipóteses para o primeiro protótipo, não balanceamento aprovado. Destruição de item e perda de melhoria não
estão propostas. As decisões que dependem do Jean estão na seção 9.

## 1. Resumo

- **Hoje** o ferreiro reforça só a arma, o peito e o apoio, de +1 a +5, sem falha, por ouro. No intervalo da campanha
  atual (itens de nível 1 a ~6), **todo reforço dá +1**: a regra "12% do bônus, no mínimo 1" nunca passa do mínimo. Os
  cinco reforços de uma peça custam 1.283 de ouro; a partida do Jean que fechou a região terminou com ~400. O reforço é
  perdido inteiro ao trocar ou vender a peça (o preço do item não muda). Não existe encantamento, material nem
  essência.
- **A pesquisa** (Elden Ring, Last Epoch, Path of Exile, Diablo IV, Lineage II e o Místico do Diablo III) aponta que
  melhorar equipamento satisfaz quando a meta é clara, o resultado é previsível o bastante para planejar, a escolha
  muda a build e o investimento não evapora. Aleatoriedade funciona como tempero (o que achar, o que desmanchar), não
  como a moeda da melhoria. Os sistemas com perda (Lineage II) ou rolagem sem fim (Diablo IV antes do Season 11) geraram
  frustração e foram, no caso do Diablo IV, revistos para menos sorte.
- **A identidade recomendada:** o **reforço** melhora a **base** da peça, por ouro, garantido, e o investimento pode
  ser **passado** para a peça nova do mesmo espaço; o **encantamento** grava **uma propriedade escolhida** na peça,
  vinda de uma **essência** que o jogador tira de itens que desmancha na forja (ou acha na campanha, as das
  especializações). Um encantamento por peça, trocável, sem sorteio no resultado.
- **O primeiro protótipo** cabe na forja que já existe: reforço com a regra nova, a passagem do reforço, o desmanche e
  o encantamento com as 11 essências dos afixos que o jogo já tem, mais 3 a 6 essências de especialização. Valida-se
  com o Jean jogando a região.

## 2. O jogo hoje (confirmado no código, 1.210.0)

### 2.1 O reforço

`rpg/sistemas/servicos.py`, `Servicos.pecas_da_forja` e `Servicos.ferreiro`:

| O quê | Como é |
|---|---|
| Espaços | arma, peito (`armadura`) e apoio (`secundaria`); os outros sete espaços (cabeça, mãos, pernas, pés, amuleto, dois anéis) não |
| Atributo | arma: Ataque (Poder no Mago); peito: Defesa; apoio: Defesa (Guerreiro), Ataque (Arqueiro), Poder (Mago). Pela classe, não pela especialização |
| Ganho | `max(1, round(bônus atual do atributo × 0,12))`. Com os bônus da campanha (1 a ~8), sempre **+1** |
| Custo | `preco(40 × (reforço + 1)^1,6)`: 40, 121, 231, 367, 524 (−desconto da reputação); 1.283 do +0 ao +5 |
| Limite | +5; no limite, o cartão diz "No limite (+5)" |
| Falha | nenhuma |
| Onde fica | `item["reforco"]`; o ganho entra em `item["bonus"][atributo]`; o nome ganha " +N" (o id do único fica) |
| Ao trocar ou vender | o reforço vai junto com a peça; a venda paga `preco // 2`, e o `preco` não muda com o reforço: o investimento se perde |
| Raridade | não muda nada (a mesma regra para comum, incomum, raro e lendário) |

Na tela, um cartão por peça com o ganho e o preço; sem ouro, "Ouro insuficiente." (o motor manda o motivo); a forja
tem a cena da oficina desde a 1.210.0.

### 2.2 Os itens

`rpg/itens.py`:

- **Espaços:** 10 (cabeça, amuleto, peito, mãos, arma, apoio, pernas, pés, anel 1, anel 2). Bases por classe (o
  Guerreiro com espada, machado, maça, montante e martelo; o Arqueiro com arcos e besta; o Mago com cajado, varinha,
  orbe e grimório) e por material, que sobe com o nível (Enferrujado 0,75 → Rúnico 1,2).
- **Força da base:** `1,5 + 0,75 × nível` × material. Uma arma de nível 3 de Aço dá Ataque 4; de nível 6, 6 a 7. As
  peças complementares valem 65% disso, repartido em dois atributos.
- **Atributos:** Ataque, Poder, Defesa, Agilidade, Vida máx., recurso máx. (Vigor, Foco, Mana).
- **Afixos** (`AFIXOS_ITEM`, 11): do Urso (Vida), da Águia (Agilidade), do Lobo (Ataque), da Coruja (Poder), da
  Tartaruga (Defesa), da Fonte (recurso), do Vampiro (roubo de vida), da Precisão (crítico), dos Espinhos, da
  Regeneração, do Carniceiro (vida ao abater). Os cinco últimos viram modificadores do combate (`fonte_item`).
- **Raridades:** comum (0 afixo; 1 em anel e amuleto), incomum (1), raro (2 ou 3, nome sorteado), lendário (um dos 16
  únicos do catálogo, com lore e às vezes uma regra própria, como o Revide do Broquel do Vigia).
- **Como chegam:** espólio de luta (15%, 20% de elite, quase sempre comum), baús, eventos, recompensas de missão (a
  Pele do Penitente, o Broquel), o mercado (4 peças a cada 3 dias, no nível do herói ±1, puxadas para o comum).
  Vende-se por metade do preço. A mochila tem 12 espaços.

### 2.3 O ouro e a campanha

- **Fontes:** lutas, baús, contratos, eventos (o mundo é pobre: fica 75% do ouro achado). **Gastos:** mercado
  (suprimentos e peças), taverna, templo, curandeira, comitiva, resgate (30% do ouro), ferreiro.
- **A campanha hoje** é uma região (o Vale do Turvo: o Vau, o Charco, o Bosque, a Capela Afogada; a Estrada de Varn
  fechada), com inimigos de nível 1 a 3. A única medida de partida inteira por pessoa é a do Jean registrada no
  [17](17-E9-VALIDACAO-DO-VALE.md) (o Piromante): **19 dias, nível 6, 30 lutas, a febre concluída no dia 15, 37 de ouro
  no dia 10, 200 no dia 12, 403 no dia 19**, passando fome em três dias. Os registros mais longos de `tests/runs/` são
  do modo procedural que saiu na 1.206.0 (servem só de ordem de grandeza: numa delas, 181 de ouro no ferreiro em 4
  reforços). **A duração em horas não está medida** ([12](12-E1-CAMPANHA.md): "vem de partidas de jogadores novos").
- **Uma simulação isolada com o robô do gabarito** (24 partidas, 2.500 decisões) não serve para a economia: ele escolhe
  ao acaso, fica nos níveis 1 a 3 e gasta quase todo o ouro na taverna. Fica registrado como limite, não como dado.

### 2.4 Com o que uma melhoria conversa

- **O dano** cresce em linha com o atributo que a habilidade usa (`base = atributo × mult + bônus`, depois a defesa do
  alvo). Um herói com 20 a 25 de Ataque ganha ~4–5% de dano por +1. A Defesa reduz o dano recebido por `p / (p +
  defesa × fator)`.
- **Especializações:** o Paladino usa Poder (o Golpe Sagrado soma 0,8 do Poder, a Prece cura pelo Poder) mas o reforço
  da arma do Guerreiro dá Ataque; o Necromante (servos pelo Poder), o Piromante (queimaduras pelo Poder), o Berserker
  (dano quanto mais ferido), o Patrulheiro (o animal) e o Sombra (críticos, veneno) têm modificadores próprios.
- **Estruturas aproveitáveis já no motor:** os modificadores dos talentos (`mods`, `mults`, `gatilhos`:
  `cura_luz`, `servo_vida`, `queimadura_dano`, `queimadura_turnos`, `mult_critico`, `laco_animal`, `escudo_turnos`,
  `barreira_turnos`, `dano_ferido`, `dano_corpo`, `dano_distancia`, `critico`, `roubo_vida`...), que um item já pode
  carregar (`fonte_item`, os únicos com `mods`/`gatilhos`); o vocabulário dos afixos; o registro dos eventos do
  ferreiro na telemetria.
- **Intenção registrada (não é código):** "reforços iniciais garantidos e risco mais tarde; começar sem destruição nem
  perda" ([23](23-PLANO-DE-ARTE-INTERFACE-E-COMBATE.md), item 4); "manter reforço separado de raridade; não acrescentar
  destruição ou falha aleatória como padrão" ([05](05-ITENS-E-RECOMPENSAS.md)); "preservar categorias e +5 existentes;
  revisar economia" ([10](10-DECISOES.md)).

## 3. As referências

Cinco jogos escolhidos pelo contraste, mais o Místico do Diablo III. As regras mudam por versão: está dito de que
versão cada fonte fala, e o que veio de fonte secundária está marcado.

### 3.1 Elden Ring (FromSoftware, 2022) — melhoria determinística por materiais, afinidade trocável

- **O que decide:** qual arma levar adiante (as pedras de forja são escassas no começo) e, à parte, a Cinza de Guerra
  e a afinidade (Pesada, Afiada, Mágica...), que muda a habilidade e o atributo de que a arma tira dano.
- **O que paga:** pedras de forja de cada faixa e runas. As armas comuns vão a +25 (12 pedras por três níveis, a última
  da Pedra Antiga de Dragão); as especiais a +10, uma Pedra Sombria por nível. Os sinos dos mineiros liberam a compra
  ilimitada das pedras comuns. ([Fextralife, Upgrade Materials](https://eldenring.wiki.fextralife.com/Upgrade+Materials);
  [wiki.gg, Somber Smithing Stone](https://eldenring.wiki.gg/wiki/Somber_Smithing_Stone))
- **O que ganha e arrisca:** o ganho é certo e mostrado antes; não há falha nem perda. As Cinzas de Guerra se aplicam
  num Lugar de Graça e "podem ser reutilizadas sem custo"; aplicar uma nova tira a anterior.
  ([Fextralife, Ashes of War](https://eldenring.wiki.fextralife.com/Ashes+of+War))
- **Por que continua:** cada pedra achada é um passo visível rumo a uma meta conhecida; a afinidade deixa experimentar
  build sem pagar de novo.
- **O problema no uso repetido:** a escassez das pedras do fim prende o jogador a uma arma; mudar de ideia tarde custa
  caro (a melhoria não passa de uma arma para outra).
- **Para nós:** sim à melhoria certa, mostrada antes, e à troca livre do que é "jeito" (afinidade ≈ encantamento). Não
  ao número de faixas e materiais: a campanha é curta.

### 3.2 Last Epoch (Eleventh Hour Games) — afixos escolhidos com um orçamento por item

- **O que decide:** qual afixo pôr ou subir de nível na peça, com o fragmento (shard) daquele afixo.
- **O que paga:** fragmentos (vindos de desmanchar ou de achar) e o **Potencial de Forja** do item, um orçamento que
  cada ação gasta num valor sorteado dentro de uma faixa mostrada; em zero, o item não aceita mais nada. Runas e
  glifos mudam a ação (a Runa de Remoção tira um afixo ao acaso e devolve fragmentos; o Glifo da Esperança dá 25% de
  não gastar potencial). Não destrói o item (só a Runa de Estilhaçar, escolhida, transforma o item em fragmentos).
  ([Maxroll, Beginner Crafting Guide](https://maxroll.gg/last-epoch/resources/beginner-crafting-guide), atualizado
  em 27/03/2026; secundária: não achei a página oficial acessível)
- **Como entende o resultado:** sabe o que vai mudar (o afixo escolhido sobe um nível); a sorte fica no quanto do
  orçamento sai.
- **Por que continua:** os fragmentos dão uso a tudo o que cai; ver a peça "crescer" do jeito planejado.
- **O problema:** o orçamento acaba no meio do plano e o item "morre" para a forja; muitos tipos de fragmento enchem o
  inventário; os glifos e runas pedem leitura de guia.
- **Para nós:** sim à **escolha do afixo** e a **desmanchar para obter o material daquele afixo** (o que cai passa a
  importar). Não ao orçamento sorteado, nem a vários tipos de glifo e runa.

### 3.3 Path of Exile (Grinding Gear Games, o primeiro) — rerrolagem aleatória e bancada determinística

- **O que decide:** que moeda usar no item: o Orbe do Caos refaz os modificadores ao acaso; a **bancada** acrescenta
  um modificador escolhido de uma lista, por um preço fixo em moedas, e tirá-lo custa um Orbe de Purificação.
  ([PoE Wiki, Crafting](https://www.poewiki.net/wiki/Craft); [Maxroll, PoE crafting resources](https://maxroll.gg/poe/resources/crafting-resources);
  a página da bancada da PoE Wiki recusou o acesso automático nesta pesquisa, os detalhes da bancada vêm das buscas)
- **O que paga e arrisca:** moedas que também são a moeda de troca entre jogadores; a rerrolagem pode piorar a peça.
- **Por que continua:** o "e se desta vez" da rolagem, e a bancada para fechar a peça com o que falta.
- **O problema:** sem uma meta, a rerrolagem vira caça-níquel; o sistema completo exige estudo externo; a economia do
  jogo (troca entre jogadores) não existe no nosso.
- **Para nós:** a **bancada** é o modelo útil (o efeito escolhido, o preço fixo, tirar e pôr de novo). A rerrolagem
  aleatória como forma principal de melhorar, não.

### 3.4 Diablo IV (Blizzard) — temperar, maestria e encantar, e a revisão para menos sorte

- **Season 4 / patch 1.4.0 (maio de 2024):** os itens passaram a ter menos afixos, mais fortes; a **Têmpera** acrescenta
  afixos com Manuais reutilizáveis, mas o afixo saía **sorteado** entre os do manual, com poucas tentativas por item; a
  **Maestria** (masterworking) sobe a peça por postos, e os postos 4, 8 e 12 aumentavam **um afixo ao acaso** em 25%; a
  partir do 1.4.0 a maestria "não falha mais"; reiniciar a maestria não devolve o material. O **Encantar** (com a
  Ocultista) troca um afixo, com custo de ouro que cresce. ([Dexerto, notas do 1.4.0](https://www.dexerto.com/diablo/diablo-4-patch-notes-1-4-0-itemization-crafting-2676111/);
  [Icy Veins, Masterworking](https://icy-veins.com/d4/guides/masterworking-guide); [Mobalytics, rerolagem](https://mobalytics.gg/blog/diablo-4/occult-affix-rerolling-guide/);
  secundárias: as notas oficiais da Blizzard não abriram nesta pesquisa)
- **Season 11 (fim de 2025):** a Têmpera passou a deixar **escolher** o afixo da receita, com cargas restauráveis sem
  limite; a Maestria virou uma "Qualidade" até 20, sobe de 2 a 5 por vez, e só o bônus final ainda sorteia.
  ([Icy Veins, Season 11](https://www.icy-veins.com/d4/news/huge-diablo-4-vendor-crafting-changes-in-season-11/);
  [GameLuster, PTR do Season 11](https://gameluster.com/diablo-4-season-11-ptr-tempering-masterworking-overhaul/);
  as datas das fontes não batem entre si)
- **O problema que a própria revisão aponta:** a sorte em cima de um investimento caro (a têmpera errada, o afixo
  errado no posto 12, o custo que dobra) frustrava; a correção foi deixar escolher.
- **Para nós:** a direção da revisão (escolha no lugar de sorteio no resultado) e a lição dos custos que dobram. Não os
  vários sistemas empilhados (têmpera, maestria, encantar, santificação) numa campanha curta.

### 3.5 Lineage II (NCSOFT) — reforço com falha e perda, para analisar os problemas

- **As regras clássicas** (variam por crônica e servidor): reforço seguro até +3 (+4 na armadura de corpo inteiro);
  acima disso, cerca de 70% de sucesso; na falha com o pergaminho comum o item vira cristais (é destruído); com o
  pergaminho abençoado (raro) volta a +0. ([StrategyWiki, Lineage II/Items](https://strategywiki.org/wiki/Lineage_II/Items);
  [Ludo, Enchanting](https://www.ludo.guide/guide/lineage-ii/enchanting-augmenting/enchanting-upgrading-equipment);
  oficial: [lineage2.com](https://lineage2.com/news/vengeance-promotion-aden) mostra pergaminhos com "nível seguro"
  por tipo de acessório)
- **O que o jogador sente:** o número alto vira troféu e o risco vira espetáculo; mas o medo de perder faz o jogador
  parar no nível seguro ou depender de itens raros/pagos de proteção, e uma perda apaga horas.
- **Por que funciona lá e não aqui:** num MMO, o item é também status social e há um mercado entre jogadores; numa
  campanha de um jogador, sem esse mercado, a perda só tira progresso.
- **Para nós:** o "nível seguro" e o abençoado mostram que até os sistemas com risco precisaram de proteção. **Não
  recomendo falha, destruição nem perda** (seção 5).

### 3.6 O Místico do Diablo III (Reaper of Souls, 2014) — encantar uma propriedade

- **A regra:** troca-se **uma** propriedade da peça; depois disso as outras ficam travadas; cada troca mostra opções e
  **o original continua entre elas**, então nunca se piora a peça. ([Diablo Wiki, Enchant](https://di.diablowiki.net/Enchant);
  [mp1st sobre o anúncio](https://mp1st.com/news/diablo-3-mystic-artisan-new-weapon-enchantments-detailed);
  secundárias, sobre o blog da Blizzard de 2013)
- **Para nós:** "uma propriedade mexível por peça" e "nunca piorar" são boas travas.

### 3.7 Comparação

| | Escolhe o resultado? | Paga com | Pode perder? | O investimento passa para outra peça? | Problema no uso repetido |
|---|---|---|---|---|---|
| Elden Ring | sim (melhoria certa; afinidade escolhida) | pedras por faixa + runas | não | não (a melhoria fica na arma) | escassez prende a uma arma |
| Last Epoch | sim (o afixo); o orçamento sorteia | fragmentos + potencial do item | o item pode "acabar" para a forja | não | o orçamento acaba no meio do plano |
| Path of Exile | bancada sim; orbes não | moedas (também de troca) | a peça pode piorar | não | caça-níquel sem meta |
| Diablo IV S4 | pouco (sorteio no resultado) | manuais, materiais, ouro crescente | a peça "perde" as tentativas | não | frustração; revisto no S11 |
| Lineage II | não (sucesso ou falha) | pergaminhos | sim: o item ou o +N | não | medo, parar no seguro |
| Diablo III (Místico) | escolhe entre opções, o original fica | materiais + ouro | não | não | rolar até sair a ideal |

## 4. Satisfação e expectativa

"Dopamina" é usada aqui como a palavra do dia a dia para **expectativa, satisfação e recompensa**; não se afirma nada
sobre o cérebro. O que a pesquisa de motivação em jogos sustenta e serve para decidir:

- **Autonomia e competência** predizem o prazer e a vontade de continuar jogando (Ryan, Rigby e Przybylski, 2006,
  [doi:10.1007/s11031-006-9051-8](https://www.doi.org/10.1007/S11031-006-9051-8)). Para nós: o jogador **escolhe** o que
  melhorar e **entende** por que ficou mais forte.
- **A proximidade da meta acelera o esforço** (o efeito do gradiente da meta: Kivetz, Urminsky e Zheng, 2006,
  [doi:10.1509/jmkr.43.1.39](https://business.columbia.edu/faculty/research/goal-gradient-hypothesis-resurrected-purchase-acceleration-illusionary-goal)).
  Para nós: metas curtas e visíveis (o próximo +1, a essência que falta), não um sistema sem fim.
- **Recompensa aleatória** prende pela incerteza, mas é a mesma alavanca dos caça-níqueis; uma "garantia depois de N
  tentativas" (pity) remenda a frustração sem tirar o problema. Para nós: **não** usar sorteio no resultado da melhoria.

Como cada coisa pedida aparece:

| Pedido | Como a proposta produz |
|---|---|
| Meta compreensível | o próximo nível do reforço e a essência que se quer, com o número antes de pagar |
| Expectativa antes | o cartão mostra antes/depois; a essência guardada é uma promessa ("tenho Vampiro, falta a peça certa") |
| Escolha com consequência | o encantamento é um só por peça: qual propriedade, em qual peça |
| Progresso perceptível | a ficha e o nome (+N) mudam; o golpe seguinte mostra o número maior |
| Propriedade sobre a peça | o reforço passa para a peça nova; o encantamento é escolha do jogador |
| Resultado claro | o que mudou, exatamente, uma vez, sem esconder chance |
| Experimentar sem medo | trocar o encantamento custa pouco; o reforço não se perde |

**Determinístico × aleatório:** o determinístico dá planejamento e confiança; o risco é ficar sem surpresa. A surpresa
fica onde já está e é boa: **o que cai** (a raridade, os afixos) e, agora, **que essência um item desmanchado dá**.
**Frustração e repetição:** custos que dobram (Diablo IV) e materiais demais (Last Epoch) aparecem no uso longo; numa
campanha curta, poucos tipos e custos que crescem devagar. **Fora da proposta:** pressão diária, espera artificial,
grind obrigatório, chance escondida.

## 5. A identidade dos dois sistemas

A hipótese inicial ("o reforço melhora a base; o encantamento acrescenta ou modifica propriedades") **funciona** com os
nossos itens, com dois ajustes: o reforço olha **a base da peça** (todos os atributos dela, não só um escolhido pela
classe), e o encantamento usa o **vocabulário que o jogo já tem** (os afixos e os modificadores dos talentos).

### 5.1 Reforço — "a peça mais forte"

| Pergunta | Alternativas | Recomendação |
|---|---|---|
| Espaços | (a) os 3 de hoje; (b) as 7 peças de armadura e arma; (c) todos os 10 | **(a), por ora.** Mais espaços viram obrigação antes de jogar; o encantamento cobre o resto. Rever quando a campanha crescer |
| Atributos | (a) um por espaço e classe (hoje); (b) todos os atributos da base da peça, em proporção | **(b):** a base inteira cresce (a arma do Arqueiro, Ataque e Agilidade; o peito, Defesa e Vida; o tomo, Poder e Mana); o Mago e o Arqueiro deixam de ficar com metade da peça |
| Ganho | (a) 12% mín. 1 (sempre +1 na campanha); (b) uma porcentagem fixa da base, mín. 1 no principal | **(b), hipótese 20% da base por nível**, mín. 1 no atributo principal |
| Progressão e limite | — | +1 a +5 (preservar); sem requisito de nível |
| Custo | (a) ouro; (b) ouro + material; (c) material | **(a) ouro**, mais barato que hoje (hipótese abaixo): a campanha é curta; material só se o protótipo mostrar sobra de ouro |
| Falha | (a) nenhuma; (b) risco acima de um nível seguro | **(a) nenhuma** (a intenção registrada e a pesquisa) |
| Raridade | (a) igual para todas; (b) limite por raridade | **(a)**, separado da raridade (como registrado no [05](05-ITENS-E-RECOMPENSAS.md)) |
| Ao trocar de peça | (a) perde; (b) passa para a peça nova do mesmo espaço, pagando uma parte; (c) a venda devolve parte | **(b) "passar o reforço"**: o ferreiro tira o +N da peça velha e põe na nova do mesmo espaço, por metade do que foi pago no último nível. A peça velha volta a +0 |

### 5.2 Encantamento — "a peça do meu jeito"

| Pergunta | Alternativas | Recomendação |
|---|---|---|
| Tipos de efeito | numérico; condicional; utilitário; ligado a habilidade | **numéricos** (os 11 afixos que já existem) e **ligados a especialização** (os modificadores dos talentos); condicionais e utilitários depois |
| Quantos por peça | 1; vários; por raridade | **1 por peça**, em qualquer raridade (o lendário inclusive) |
| De onde vem | escolha direta numa lista; sorteio; descoberta; combinação | **descoberta + escolha:** a forja grava a **essência** que você tem; as essências comuns saem de **desmanchar** peças com aquele afixo; as de especialização, de lugares da campanha |
| Trocar, tirar, rerrolar, passar | — | **trocar** sobrescreve (a essência antiga se perde; a nova é gasta); **tirar** de graça; **sem rerrolagem**; não passa de peça para peça (o reforço passa; o encantamento é da peça) |
| Acúmulo | — | o **mesmo encantamento conta uma vez só no corpo** (duas peças com Vampiro: vale uma); soma com os afixos naturais da peça, com os tetos que o combate já tem (crítico máx. 60%) |
| Com passivas e afixos | — | usa as mesmas chaves (`roubo_vida`, `critico`, `cura_luz`...): o jogador lê o mesmo nome no Grimório, na ficha e na forja |
| Contra o bônus universal | — | cada encantamento tem **espaços permitidos** (a arma: os ofensivos; o peito: os defensivos; o apoio: qualquer um), o valor é o de um afixo do nível da peça (não mais), e os de especialização só valem com aquela especialização |

### 5.3 Economia e progressão

- **Ouro:** o reforço e a passagem do reforço; o encantamento cobra um pouco de ouro (o trabalho do ferreiro).
- **Essências:** um tipo por afixo (11), contadas no herói (não ocupam a mochila de 12). Saem de **desmanchar** na forja
  uma peça incomum ou rara (1 essência por afixo dela; o comum não dá nada) — no lugar de vender por metade do preço:
  é a escolha entre ouro e possibilidade. As de especialização (poucas) vêm de lugares da campanha (a capela, os
  guardiões).
- **Quando abre:** o reforço, desde a primeira visita (como hoje); o desmanche e o encantamento, na primeira volta ao
  Vau depois do Bosque (ou de um primeiro incomum desmanchado): o jogador já tem o que gravar.
- **Experimentar sem comprometer a partida:** tirar o encantamento é de graça; passar o reforço custa metade de um
  nível; nada se perde por acaso.
- **Drops interessantes:** toda peça incomum/rara que não serve vira uma essência possível; o mercado continua
  vendendo peças (quem compra para desmanchar paga mais que a essência vale: a hipótese de custo cuida disso).
- **Não virar obrigação:** só 3 espaços reforçáveis; o encantamento é um por peça e escolhido; custos que cabem no ouro
  de uma região sem tirar a comida e as poções.

## 6. As arquiteturas e a recomendação

| | A. Base + essências escolhidas (recomendada) | B. Melhoria do espaço + bancada fixa | C. Risco crescente com proteção |
|---|---|---|---|
| Reforço | da peça, passa para a nova do mesmo espaço | do **espaço** (o +N fica na mão, vale para qualquer arma vestida) | da peça, garantido até +3, chance de voltar 1 nível acima |
| Encantamento | essência de afixo, de desmanchar ou da campanha, 1 por peça | lista fixa na forja, comprada por ouro, 1 por peça | igual à A |
| A favor | propriedade da peça; o que cai importa; escolha clara | simples; trocar de arma nunca custa | emoção no número alto |
| Contra | um tipo novo de coisa (essência) | a peça perde identidade; o drop importa menos; a lista fixa vira "a melhor da lista" | medo de perder; contraria a intenção registrada |

**Recomendo a A.** A B é a mais simples, mas tira o que a pesquisa mostra que segura o uso (a peça "minha", o drop que
vira possibilidade); a C reintroduz o problema que o Lineage II e o Diablo IV tiveram de remendar.

### 6.1 As regras propostas (A)

**Reforço:** nos espaços arma, peito e apoio; +1 a +5; garantido; cada nível soma **20% da base da peça** em cada
atributo de base, arredondado, com **mínimo +1 no atributo principal** (a base é o que a peça tem sem os afixos: um
campo novo `base`, gravado ao gerar o item). Custo em ouro, hipótese: **25, 45, 70, 100, 140** (380 do +0 ao +5,
contra 1.283 hoje). **Passar o reforço:** para outra peça do mesmo espaço, por metade do último nível pago (de +3 para a
nova: 35 de ouro); a velha volta a +0.

**Desmanchar:** na forja, uma peça incomum ou rara da mochila vira as essências dos afixos dela (uma de cada); a peça
some (é uma ação escolhida, com o que se perde mostrado antes, não uma falha). Comum e lendário não se desmancham
(o lendário é raro demais para virar material sem querer).

**Encantar:** escolher a peça vestida, escolher uma essência que se tem e que o espaço aceita, ver antes/depois, pagar
(hipótese: **15 de ouro + a essência**). O valor é o de um afixo daquele tipo no **nível da peça** (a mesma conta de
`_afixos`). Um por peça; gravar outro sobrescreve; tirar é de graça. O mesmo encantamento conta uma vez só no corpo.

### 6.2 O conjunto inicial

| Essência | Efeito (nível da peça 3; 6) | Espaços | Suporte |
|---|---|---|---|
| do Urso | +11; +17 Vida | peito, apoio | já existe (afixo) |
| da Tartaruga | +2; +3 Defesa | peito, apoio | já existe |
| da Águia | +2; +3 Agilidade | arma, apoio | já existe |
| do Lobo | +2; +3 Ataque | arma, apoio | já existe |
| da Coruja | +2; +3 Poder | arma, apoio | já existe |
| da Fonte | +8; +11 de recurso | peito, apoio | já existe |
| do Vampiro | +3%; +4% roubo de vida | arma | já existe (modificador) |
| da Precisão | +3%; +4% crítico | arma | já existe (modificador) |
| dos Espinhos | +4; +6 espinhos | peito | já existe (modificador) |
| da Regeneração | +2; +2 de vida por turno | peito | já existe (modificador) |
| do Carniceiro | +5; +7 de vida ao abater | arma | já existe (modificador) |
| **Luz** (Paladino) | Golpe Sagrado e Prece curam +15% | arma, apoio | modificador `cura_luz` existe; a ligação item → encantamento é regra nova |
| **Sangue** (Berserker) | +10% do Pacto de Sangue (`dano_ferido`) | arma | idem |
| **Laço** (Patrulheiro) | o animal +10% de vida e ataque (`laco_animal`) | apoio | idem |
| **Sombra** (Sombra) | críticos +10% de dano (`mult_critico`) | arma | idem |
| **Brasa** (Piromante) | queimaduras +10% de dano (`queimadura_dano`) | arma, apoio | idem |
| **Ossos** (Necromante) | servos +10% de vida (`servo_vida`) | arma, apoio | idem |

Os valores dos afixos saem da conta que o jogo já usa (base × (1 + 0,3 × nível); os percentuais, base + 0,25 × nível).
Os de especialização ficam em ~metade de um ponto do talento parecido; só funcionam com a especialização (fora dela, a
forja não deixa gravar).

### 6.3 Exemplos (itens do catálogo, nível de peça 3)

| Classe | Peça | Antes | Proposta | Depois |
|---|---|---|---|---|
| Guerreiro (Paladino) | Espada de Aço do Lobo (base Ataque 4; afixo +2) | Ataque 6 | reforço +2 (20% de 4 = 0,8 → +1 por nível) e encantamento Luz | Ataque 8; curas da Luz +15% |
| Guerreiro | Brigantina de Ferro (base Defesa 2, Vida 7) | Defesa 2, Vida 7 | reforço +1 (Defesa +1 mín.; Vida 7 × 20% = +1) e Urso | Defesa 3, Vida 19 |
| Arqueiro | Arco Longo de Ferro (base Ataque 3, Agilidade 1) | Ataque 3, Agilidade 1 | reforço +2 (Ataque +1 por nível; Agilidade 0,2 → 0) e Precisão | Ataque 5, Agilidade 1, +3% crítico |
| Arqueiro (Patrulheiro) | Aljava Curtida (base Agilidade 1, Ataque 1) | Agilidade 1, Ataque 1 | encantamento Laço | o animal +10% de vida e ataque |
| Mago (Piromante) | Cajado de Aço da Coruja (base Poder 4; afixo +2) | Poder 6 | reforço +1 e Brasa | Poder 7; queimaduras +10% |
| Mago | Tomo (base Poder 1, Mana 4) | Poder 1, Mana 4 | reforço +2 (Poder +1 por nível; Mana 4 × 20% = +1 por nível) e Fonte | Poder 3, Mana 14 |

Um herói de nível 3 tem Ataque/Poder perto de 15–17: +2 nele são ~12% de dano. Hoje, o mesmo +2 custa 161 de ouro; na
hipótese, 70.

### 6.4 Implicações para as especializações

- O **Paladino** ganha a Luz e, pela base inteira, nada muda no Ataque da arma; o Poder dele vem do encantamento da
  Coruja ou do apoio.
- O **Berserker** tende ao Vampiro/Sangue na arma: risco de sustentação demais com o roubo do talento Sede Insaciável;
  o teto "um por corpo" e o valor de meio talento seguram, mas é o primeiro a observar.
- O **Patrulheiro** encanta o apoio (a aljava) para o animal: a aljava deixa de ser só Agilidade.
- O **Sombra** soma Precisão (crítico) e Sombra (dano crítico): o par mais forte da lista; o crítico tem teto (60%).
- O **Piromante** e o **Necromante** ganham uma escolha real no apoio (Brasa/Ossos × Fonte/Coruja).

### 6.5 Riscos

- **Exploração:** comprar no mercado para desmanchar (o mercado tem 4 peças a cada 3 dias e puxadas para o comum: o
  custo de compra fica acima do valor da essência); passar o reforço para uma peça barata e vendê-la (a peça vendida
  não leva preço maior; a venda não devolve o reforço).
- **Acúmulo:** roubo de vida (talento + afixo + encantamento), crítico com dano crítico. Medir no protótipo com a
  ficha mostrando o total de cada um.
- **Escolha dominante:** a essência ofensiva na arma tende a ganhar sempre; os espaços permitidos e os de
  especialização são a primeira defesa; se continuar dominante, baixar o valor dela, não acrescentar sorte.
- **Peso na campanha curta:** com o reforço mais barato, o começo pode ficar fácil demais; medir com o
  `tests.equilibrio` antes e depois, como manda o [COMO_CRIAR](../docs/COMO_CRIAR.md).

## 7. A jornada e o feedback (depois das regras)

Fluxo na forja (texto; a tela vem depois da aprovação das regras):

1. **Entrar:** a cena da oficina; o balcão com três ações: **Reforçar**, **Encantar**, **Desmanchar** (as duas últimas
   aparecem quando abrem).
2. **Escolher a peça:** a lista das peças que a ação aceita, cada uma com o estado (+N, o encantamento atual); as que
   não dá mostram o motivo (no limite +5, espaço sem reforço, sem essência que sirva).
3. **Entender:** antes e depois, número por número, só o que muda; o custo; o que se perde (a essência gasta; a peça
   desmanchada; a velha que volta a +0).
4. **Confirmar:** um botão com o custo escrito. Sem ouro ou essência, o motivo no lugar do botão, e o clique não
   gasta nada.
5. **Resultado:** a ficha da peça com o que mudou destacado, uma vez; o nome com o +N.
6. **Continuar ou sair:** a seleção fica na mesma peça (para seguir no +N seguinte); a Saída e o Esc de sempre.

Casos: ouro ou essência insuficiente (o motivo, nada gasto); item no limite ou incompatível (o cartão diz por quê);
cancelar (voltar à lista sem gastar); várias melhorias seguidas (a seleção preservada, o custo novo na hora); clique
duplo ou rápido (o motor processa uma ação por pedido: o segundo clique chega com o estado novo e é recusado se não
couber); teclado (as mesmas ações por Tab e Enter); movimento reduzido (o resultado sem animação, só o destaque).

Papel do feedback (sem desenhar ainda):

| Momento | O que comunica |
|---|---|
| Seleção | qual peça e o que acontecerá com ela |
| Expectativa | o antes/depois e o custo, antes de pagar; o ferreiro já está trabalhando na cena (a animação ambiente não é o resultado) |
| Confirmação | um som e um destaque curtos de que pagou e mudou; o ouro desce na hora |
| O que mudou | só os números que mudaram, com a cor da melhora |
| Separar ambiente de resultado | a martelada contínua é o lugar; o resultado é uma marca própria na peça, que não se confunde com ela |

Não decido aqui o tamanho de uma celebração: primeiro as regras e o fluxo.

## 8. O primeiro protótipo e a validação

O mínimo para jogar:

1. **Motor, atrás de uma opção do cenário de demonstração** (sem mudar a produção): o campo `base` no item novo (e,
   para os itens antigos, a base calculada pela regra de geração), a regra de reforço nova, a passagem do reforço, o
   desmanche, as essências no herói, o encantamento com os 11 afixos e os 6 de especialização (as fontes de
   especialização, no protótipo, entregues por um comando do cenário).
2. **Tela mínima** com as três ações no balcão da forja, usando os cartões que já existem (sem arte nova).
3. **Telemetria:** cada reforço, passagem, desmanche e encantamento, com o ouro e a essência.

Validação:

- **Técnica:** testes de regra (o ganho pela base, a passagem, o teto "um por corpo", os motivos), o gabarito sem
  mudança fora do protótipo, `tests.equilibrio` com e sem as melhorias (o quanto sobe a vitória por nível).
- **Do Jean:** jogar a região com cada classe (ou a classe que quiser), com as perguntas: entendeu o que cada ação faz
  antes de pagar? alguma escolha pareceu obrigatória? sobrou ou faltou ouro? alguma essência dominou? o desmanche fez
  os drops valerem mais?
- **Critério para seguir:** as escolhas variam entre as partidas e as classes, o ouro não aperta a comida, nenhuma
  essência é sempre a melhor, e o Jean consegue explicar cada resultado.

## 9. O que depende do Jean

1. **A arquitetura:** A (recomendada), B ou C.
2. **Os espaços do reforço:** os 3 de hoje (recomendado) ou todos os de arma e armadura.
3. **A regra do ganho:** 20% da base inteira (recomendado) ou manter "o atributo da classe".
4. **Passar o reforço** para a peça nova (recomendado) ou a venda devolver parte.
5. **O desmanche como fonte das essências** (recomendado) ou essências achadas/compradas.
6. **As essências de especialização:** quais entram no primeiro protótipo e onde a campanha as entrega.
7. **Onde mora o encantamento:** a forja (recomendado para o protótipo) ou outro lugar da vila.
8. **Os custos** como hipótese para o protótipo (25–140 no reforço, 15 no encantamento).

Nada disso foi implementado. Depois das decisões, o protótipo da seção 8, e só depois a aparência e o ritmo do
resultado.

</details>
