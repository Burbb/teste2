# 04 — Habilidades, talentos e transformações

## Base pronta

habilidades.py combina blocos de dano, estado, condições, cura, roubo, buffs e rajadas. Os blocos executam e descrevem. Mecânicas particulares podem usar funções próprias.

modificadores.py reúne talentos, passivas, efeitos declarados da classe/especialização e itens. Há eventos como início da luta, golpe recebido, ataque básico, morte e abate. estados.py declara efeitos por etapas do golpe.

Usar essa estrutura antes de acrescentar regras específicas no combate.

## Quantidade e função

Cerca de 300 habilidades é ambição futura, sem compromisso neste ciclo. Adicionar uma habilidade quando cria decisão, resolve uma lacuna ou completa uma combinação.

Verbos: marcar, proteger, interromper, acumular, consumir, sacrificar, converter recurso e executar. Combustão já é exemplo de consumo de efeito; usar como referência de ciclo interessante.

## Talentos

| Tipo | Situação | Próximo uso |
|---|---|---|
| Atributo/passiva simples | Existe | Sustentar equipamentos e recursos |
| Condicional/gatilho | Existe | Incentivar comportamentos distintos |
| Modificador de habilidade | Existe parcialmente | Custo, duração, intensidade e chance |
| Transformação estrutural | Falta forma geral | Mudar alvo, passos ou comportamento |
| Ativa desbloqueada por talento | Falta integração geral | Aprendizado, menu e persistência |

Não recriar Contra-ataque, Frenesi ou Imortal para demonstrar passivas condicionais. Reaproveitar exemplos e adicionar somente o que falta à build.

## Habilidade efetiva — extensão proposta

Atualmente execução consulta diretamente HABILIDADES[id]. Uma transformação geral precisa resolver a versão efetiva para aquele personagem.

Ela deve informar alvo, custo, passos/comportamento, descrição, preview e apresentação de forma consistente. Definir prioridade/incompatibilidade de modificadores. Não alterar o catálogo global de forma que a build de um personagem afete outra sessão ou teste.

Demonstrar primeiro uma transformação simples. Só adicionar hooks novos quando um efeito concreto exigir.

## Alvos

Seleção normal de magias está organizada em inimigo, todos os inimigos e próprio personagem. Poções e a comitiva já têm caminhos de cura em aliados.

Magias selecionáveis em aliado único/todos os aliados precisam de extensão no fluxo de habilidade, no motor e na interface. Fazer isso se uma habilidade aprovada exigir; não inventar nova classe de suporte agora.

## Árvore

Layout já aceita mais ramos/camadas e nós lado a lado. Disponibilidade atual usa principalmente nível, spec e rank máximo; conexões desenhadas não são pré-requisitos de compra.

Quando houver dependências reais, acrescentar requisitos, exclusões e validação de ciclos. Preservar compra e árvore existentes. Não transformar uma linha visual em regra por suposição.

Descrições de talentos/gatilhos ainda têm números escritos à mão. Conferir coerência ao mudar regras; descrição calculada pode ser introduzida para os efeitos novos mais complexos.

## Preparação

Se adotada, manter lista de aprendidas e lista de preparadas. Migrar saves antigos com uma seleção válida, preservar ataques básicos e evitar preparar habilidade não aprendida.

Grimório, menu e atalhos devem explicar disponibilidade. Não confundir limite de preparação com perda de habilidades aprendidas.

## Especificação mínima

Id, fantasia, aquisição, alvo, custo, escala, estados, papel na build, modificadores compatíveis, descrição efetiva e feedback. Toda habilidade deve ter uma situação de uso preferível às alternativas.

## Validação

Preview/descrição/execução concordam. Equipar e retirar transformações funciona. Conjuntos incompatíveis são resolvidos explicitamente. Gatilhos não geram ciclos infinitos. Alvos mortos ou inválidos são tratados. Todos os seis caminhos recebem atenção antes da conclusão da campanha, sem exigir animação exclusiva para cada magia.
