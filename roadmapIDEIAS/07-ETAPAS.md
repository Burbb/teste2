# 07 — Etapas até a campanha desejada

Plano proposto, sem datas. Cada etapa é dividida em tarefas pequenas e depende de pedido de Jean. Não executar o documento inteiro automaticamente.

## E0 — Base refatorada: entregue estruturalmente

**Estado:** reorganização observada na 1.46.0. Na 1.47.1 (10/10/2026), suíte, gabarito, pyflakes e fumaça passaram; detalhes no registro de [00-COMECE-AQUI](00-COMECE-AQUI.md).
**Ação:** Claude informa commit e evidência da validação atual. Conferir 09-BASE-EXISTENTE.
**Não fazer:** repetir refatoração geral ou reconstruir sistemas que já existem.
**Saída:** ponto de partida conhecido e verificações pertinentes em dia.

## E1 — Especificar primeira região e arco da campanha

**Depende:** E0.
**Estado:** proposta em [11-E1-REGIAO-INICIAL](11-E1-REGIAO-INICIAL.md) e [12-E1-CAMPANHA](12-E1-CAMPANHA.md), aguardando aprovação de Jean.
**Entrega:** documento de design com uma vila, poucas áreas externas, uma masmorra, conflito local e encerramento; pequeno esboço do início, meio e fim da campanha.
**Incluir:** Guerreiro/Arqueiro/Mago, oportunidades narrativas das classes, integração dos companheiros existentes, duas soluções de missão, consequência ao retornar e loot pertinente.
**Decisões:** cronologia, duração aproximada do trecho, condições de especialização e modelo provisório de derrota.
**Pronto:** percurso completo descrito, alternativas gerais acessíveis e limites claros.
**Não fazer:** implementar código, inventar todas as raças ou escrever todos os capítulos.

## E2 — Carregar uma região fixa

**Depende:** E1.
**Estado:** protótipo entregue na 1.48.0 (commit `2661b59`): começo da campanha, mapa fixo do Vale do Turvo (sem o Morro da Forca), viagem, descoberta, Estrada de Varn fechada, modo resgate/hardcore no save. Validação técnica feita; falta Jean jogar. Detalhes no registro de [00-COMECE-AQUI](00-COMECE-AQUI.md).
**Entrega:** uma forma de iniciar o mapa escrito reaproveitando navegação, descoberta, clima e desenho.
**Tarefas pequenas:** contrato dos locais; seleção/carregamento; adaptação mínima de pressupostos de início/final; persistência.
**Pronto:** viajar, retornar e salvar/carregar funciona com as três classes.
**Não fazer:** apagar o procedural antecipadamente, trocar toda identidade de local ou criar editor universal.

## E3 — Missão encadeada mínima

**Depende:** E2.
**Notas aprovadas:** bênção, rito garantido e comporta parcial, em [11-E1-REGIAO-INICIAL](11-E1-REGIAO-INICIAL.md), seção 19.
**Estado:** primeira entrega na 1.50.0: registro da missão, cena de abertura, objetivo no Diário e no rastreador, exame da Fonte Nova (etapa `fonte` → `canal`). Segunda na 1.51.0: o canal no Bosque (`canal` → `capela`), o exterior da Capela Afogada e as cenas da missão com Continuar explícito. Salas internas, comporta, guardiã, Caspar e desfechos não começaram.
**Entrega:** uma missão com etapas, objetivos no Diário e duas soluções.
**Tarefas:** ids/estados; transições; cenas explícitas; recompensas únicas; apresentação.
**Pronto:** dois percursos concluem, falhas previstas não travam e save/load mantém progresso.
**Não fazer:** forçar tudo ao formato de contrato de caça ou converter todas as cenas antigas.

## E4 — Consequência local e comitiva

**Depende:** E3.
**Entrega:** mudar um estado da vila e refletir em diálogo/serviço; integrar uma reação/conversa de companheiro.
**Pronto:** retornar e recarregar o save revela a mesma consequência; a escolha tem efeito percebido.
**Não fazer:** facções em massa ou simulação de rotina de todos os NPCs.
**Condicional:** reputação por facção só se o conflito escolhido realmente precisar.

## E5 — Diagnosticar e aprofundar as três classes

**Depende:** E1; integrar ao percurso de E4.
**Entrega:** fichas curtas de Guerreiro/Arqueiro/Mago e seis especializações, com ciclo, forças, fraquezas e lacunas.
**Tarefas:** aproveitar habilidades/talentos; integrar encruzilhadas; adicionar conteúdo apenas para lacunas reais.
**Pronto:** três classes atravessam a região; seis caminhos avaliados em cenários direcionados.
**Não fazer:** recriar passivas condicionais, adicionar classes ou evoluções sucessivas sem design.

## E6 — Demonstrar transformação de habilidade

**Depende:** E5.
**Entrega:** uma transformação simples, resolvida de forma consistente para execução e apresentação.
**Tarefas:** especificar efeito; resolver habilidade efetiva; integrar custo/alvo/descrição; validar equipar/retirar ou aprender.
**Pronto:** resultado e Grimório concordam e outra build/sessão não é afetada.
**Não fazer:** centenas de transformações ou alteração global do catálogo.
**Extensões condicionais:** preparação, pré-requisitos reais, talento ativo e alvos aliados somente quando o conteúdo aprovado precisar; decidir regras antes.

## E7 — Conectar equipamento à build

**Depende:** E5; E6 quando o item transformar habilidade.
**Entrega:** um único com efeito relevante e ficha completa, depois poucos exemplos para os três estilos.
**Tarefas:** usar fonte_item/gatilhos; descrever efeito; aquisição; feedback; economia.
**Pronto:** o jogador entende o efeito e pode reconsiderar a build; reforço existente continua funcionando.
**Não fazer:** criar reforço do zero, avalanche de drop ou catálogo de únicos em massa.

## E8 — Introduzir identidade em escopo pequeno

**Depende:** E3–E4 e escolhas de 10-DECISOES.
**Entrega:** raça/origem em conjunto pequeno, com reconhecimento real.
**Proposta de limite:** duas raças e duas origens para primeiro teste; nomes e quantidade dependem de Jean.
**Tarefas:** catálogo e criação; persistência; uma oportunidade e uma repercussão por identidade ofertada.
**Pronto:** repetir com outra identidade muda oportunidades sem bloquear a história obrigatória.
**Não fazer:** campanhas independentes por combinação. Na região inicial, classe pode provar o padrão antes de raça/origem.

## E9 — Validar a região completa

**Depende:** E2–E8; extensões condicionais apenas se adotadas.
**Entrega:** percurso integrado e avaliação de preparação, loot, relações, combate e derrota.
**Pronto:** conclusão local com três classes; ramificações persistentes; consequências claras; motivos para repetir.
**Registrar:** evidência técnica e feedback de Jean.
**Decisão:** consolidar ou ajustar antes de ampliar. Raça/origem podem ser adiadas explicitamente, sem ficar falsamente marcadas como prontas.
**Não fazer:** adicionar sistemas para encobrir ritmo ruim.

## E10 — Completar a campanha por trechos

**Depende:** E9.
**Entrega:** novas regiões/capítulos na quantidade definida em E1 e revisada após a experiência.
**Para cada trecho:** especificar → implementar → testar alternativas → jogar → integrar consequências.
**Incluir:** continuidade de decisões, progressão dos seis caminhos, histórias pessoais, missões opcionais, equipamento e conflitos locais.
**Pronto:** história tem início, desenvolvimento e fim alcançáveis pelas três classes; capítulos reutilizam estruturas.
**Não fazer:** aumentar classes para preencher lacunas de conteúdo ou produzir capítulos em lote sem validação.

## E11 — Final, epílogos e consolidação

**Depende:** E10.
**Entrega:** confronto/conclusão com contexto, fechamento de arcos e epílogos baseados em decisões relevantes.
**Tarefas:** resolver destinos de lugares/companheiros; validar combinações selecionadas; revisar começo/meio/fim, economia, builds, clareza e save.
**Pronto:** campanha completa e consistente; seis especializações viáveis; escolhas reconhecidas; ausência de bloqueios conhecidos nos percursos validados.
**Não fazer:** final distinto para cada flag ou prometer cobertura exaustiva de toda combinação.

## Depois: expansão opcional

Evoluções avançadas, mais classes, catálogo muito maior, armazenamento e novas telas. Só entrar após decisão de Jean e evidência de necessidade. Manter três classes como escopo deste ciclo.

## Critério geral

Registrar feito, validado tecnicamente e validado jogando separadamente. Refatoração pura preserva comportamento; mudanças intencionais são identificadas e seguem os guias técnicos. Não ampliar suíte por rotina nem atualizar gabarito para ocultar alterações incidentais.
