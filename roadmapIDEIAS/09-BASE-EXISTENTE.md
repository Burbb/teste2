# 09 — Base existente e limites da expansão

Revisão estática da versão 1.46.0, commit d8d65b9778e85bb7eb8118fdd7a84acfd17e80ac. Código e testes foram lidos; jogo e suíte não foram executados nesta revisão. Conferir mudanças posteriores antes de usar este diagnóstico.

## Avaliação

Base adequada para continuar. Motor separado da apresentação, catálogos extensíveis, sistemas organizados e persistência versionada. Não há necessidade demonstrada de trocar linguagem ou interface.

Separar arquivo melhora manutenção, mas os mixins de Jogo/Combate ainda compartilham estado e dependências. Expansão deve preservar contratos claros; não presumir independência total.

## Matriz de reuso

| Sistema | Evidência | Situação para o plano |
|---|---|---|
| Classes e specs | rpg/classes.py, entidades.py, sistemas/progressao.py | Três classes/seis caminhos; uma etapa de spec |
| Habilidades | rpg/habilidades.py | Blocos reutilizáveis + funções particulares |
| Passivas/gatilhos | rpg/modificadores.py, talentos.py | Prontos para efeitos conhecidos; hooks novos sob demanda |
| Estados | rpg/estados.py, combate/golpe.py | Catálogo inclui etapas do cálculo de golpe |
| Árvore | talentos.py, web/static/telas/talentos.js | Layout flexível; requisitos além de nível/spec/rank faltam |
| Itens | itens.py: fonte_item, unico_de, ficha | Modificadores/gatilhos suportados; efeitos complexos ainda precisam de conteúdo e descrição |
| Reforço | sistemas/servicos.py | Arma/peito/secundária até +5, previsível |
| Campanha/mapa | mundo.py, jogo.py, sistemas/navegacao.py | Grafo reutilizável; início procedural e convenções posicionais |
| Eventos | eventos/motor.py | Condições/pesos/repetição; cenas principais precisam de avanço explícito |
| Consequências | sistemas/recompensas.py: plantar/colher | Acontecimentos futuros já persistidos |
| Missões | sistemas/contratos.py, eventos/comitiva.py | Progresso de contratos e arcos pessoais; modelo geral falta |
| Comitiva | rpg/comitiva/ | Valores, confiança, conversas, luta e fogueira |
| Reputação | jogador.reputacao | Global; facções ainda precisam de modelo |
| Identidade | Jogador/init/criação | Classe/spec; raça/origem não modeladas no núcleo revisado |
| Preparação | combate/heroi.py usa j.habilidades | Sem separação aprendidas/preparadas |
| Saves | sistemas/persistencia.py, migracoes.py | JSON, migrações e gravação temporária |
| Derrota | Jogo.resgate e modo hardcore/brando | Reaproveitar; definir experiência da campanha |
| Apresentação | ponte/estado, static/telas/, batalha.js | Preservar; efeitos enviados como ações/dados |

## Pontos que exigem extensão

1. Trajetória de evolução: spec único não representa várias etapas.
2. Talentos dependentes/exclusivos: conexões visuais não validam compra.
3. Habilidade efetiva: execução consulta catálogo direto; transformação precisa de regra compartilhada.
4. Habilidades ativas em aliados: seletor normal ainda não é geral.
5. Ficha de item: bônus/lore não descrevem automaticamente gatilhos próprios.
6. Missões e estados narrativos: funções/flags dispersas precisam de organização para campanha.
7. Classes novas: geração de itens ainda possui regras explícitas para as três existentes; não basta acrescentar uma entrada em CLASSES.

Nem todos precisam ser resolvidos antes da primeira região. Fazer somente os usados por conteúdo aprovado.

## Documentação técnica parcialmente desatualizada

docs/ROADMAP.md ainda descreve itens com especial() e estados perguntados manualmente no golpe. O código revisado já integra itens em fontes e estados em no_golpe.

Consultar implementação antes de pedir tarefa que aparece como pendente. Não reabrir B/C só pelo texto antigo. Não modificar a documentação técnica como efeito incidental deste roadmap.

## Rede de segurança

Há validador de referências/ícones, testes de habilidades, estados e modificadores, simulações, replay, telemetria, testes web e gabarito de partidas. Gabarito inclui sequências de luta com companheiros.

Existência dos testes não é prova de passagem nesta sessão nem cobertura exaustiva. Campanha pede novos cenários relevantes: soluções, estados incompatíveis, conclusão única, continuidade e save/load. Builds pedem testes de interação escolhidos.

## Manutenção e desempenho

Catálogos maiores podem ser separados por classe/região preservando imports públicos. Telas continuam dependentes de ordem de scripts. batalha.js grande não exige migração.

Não alegar capacidade para qualquer volume sem medição. Priorizar legibilidade e comportamento; medir lentidão real antes de cachear modificadores ou reestruturar o runtime.
