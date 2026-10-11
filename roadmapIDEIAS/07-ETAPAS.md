# 07 — Etapas até a campanha desejada

Plano proposto, sem datas. Cada etapa é dividida em tarefas pequenas e depende de pedido de Jean. Não executar o documento inteiro automaticamente.

## Ordem atual (decisão de Jean, 11/10/2026)

1. **A primeira entrega da E7** (o Broquel do Vigia, 1.63.0) e a validação de Jean jogando.
2. **A avaliação integrada do Vale do Turvo** (o trabalho pertinente da E9, antecipado). O Vale é o primeiro capítulo
   completo: resolução do conflito local e encerramento reconhecível. Os outros exemplos da E7 (Arqueiro, Mago) vêm
   depois dela, se a avaliação os pedir.
3. **A E8 (raças e origens) fica adiada explicitamente.** Ela não é requisito da avaliação do Vale.
4. **As regiões seguintes (E10)** dependem da avaliação do Vale. O esboço da campanha maior continua como direção
   ([12](12-E1-CAMPANHA.md)); as expansões não são obrigação anterior à primeira versão de teste.

A duração não está definida: ela se mede com jogadores novos (E9, "Medir a primeira partida"). O histórico das etapas
abaixo fica como estava; o estado de cada uma diz o que mudou.

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
**Estado:** primeira entrega na 1.50.0: registro da missão, cena de abertura, objetivo no Diário e no rastreador, exame da Fonte Nova (etapa `fonte` → `canal`). Segunda na 1.51.0: o canal no Bosque (`canal` → `capela`), o exterior da Capela Afogada e as cenas da missão com Continuar explícito. Terceira na 1.52.0: o interior (nave, sacristia, ossuário) e soltar as correntes (D2) como preparo. Quarta na 1.53.0: Vó Berta e a fita, a guardiã com Destruir ou Dar descanso (o rito garantido) e o desfecho único. Na 1.54.0, a volta ao Vau conclui a missão. A comporta e a bênção não existem.
**Entrega:** uma missão com etapas, objetivos no Diário e duas soluções.
**Tarefas:** ids/estados; transições; cenas explícitas; recompensas únicas; apresentação.
**Pronto:** dois percursos concluem, falhas previstas não travam e save/load mantém progresso.
**Não fazer:** forçar tudo ao formato de contrato de caça ou converter todas as cenas antigas.

## E4 — Consequência local e comitiva

**Depende:** E3.
**Estado:** primeira consequência na 1.54.0 (a Fonte Nova, a frase do Vau, Pita e Marta na curandeira). Na 1.55.0, Caspar e a decisão pública (Apoiar, Denunciar com prova, Calar), com a situação da Yara e a reação da comitiva por etiquetas. Na 1.56.0, a consolidação: a Yara barrada fica de fato fora do Vau (não luta, não opina, não conversa nem é cuidada ali; volta na estrada), o encontro no Charco depois da denúncia, a conversa da Yara sobre a praça e os textos corrigidos. **Critério mínimo atendido** (registro da 1.56.0 no 00). Adiado, sem ser requisito: bênção, sementes, taverna, mercado, Charco à noite, comporta, Odette e Caspar, Anselmo, a cena da vigília, falas próprias de Odette e Morel. Falta Jean jogar.
**Entrega:** mudar um estado da vila e refletir em diálogo/serviço; integrar uma reação/conversa de companheiro.
**Pronto:** retornar e recarregar o save revela a mesma consequência; a escolha tem efeito percebido.
**Não fazer:** facções em massa ou simulação de rotina de todos os NPCs.
**Condicional:** reputação por facção só se o conflito escolhido realmente precisar.

## E5 — Diagnosticar e aprofundar as três classes

**Depende:** E1; integrar ao percurso de E4.
**Estado:** diagnóstico entregue (só design, 1.56.0) em [14-E5-DIAGNOSTICO-CLASSES](14-E5-DIAGNOSTICO-CLASSES.md): fichas das três classes e das seis especializações, liberdade de build, progressão e três prioridades. Na 1.57.0, a **P1**: no ossuário e no sarilho, um inimigo prepara o Golpe Esmagador existente (abre a luta preparando), com o aviso e a ficha à vista; resultados na seção 10 do 14. Na 1.58.0, a **P3**: a encruzilhada compara os dois caminhos (o que dá, limites, números feitos numa cópia do herói; olhar não escolhe) e o Grimório explica imunidades, a Marca, a Combustão e o caminho (seção 11 do 14). Falta Jean jogar as duas. Na 1.59.0, a **P2 começou pelo Tiro Duplo**: o 2º disparo vai no outro inimigo mais ferido. Ele ganha com um quase morto e outro de pé, ou com dois feridos ao alcance de um disparo, e perde para o Tiro Certeiro (alvo resistente, dois inteiros) e para a Chuva (três ou mais), sem mudar números (seção 12 do 14). Drenar Vida, Desaparecer e Passo Ágil foram avaliados em lutas inteiras, sem mudar o jogo (seção 13 do 14): o Drenar Vida sustenta contra vivos quando ferido (armadilha contra mortos-vivos, já avisada); o Desaparecer não muda o Vale, mas depois abre com crítico contra dois inimigos resistentes; o Passo Ágil não tem vantagem relevante. O desvio do Passo Ágil foi validado e rejeitado: responde bem à preparação, mas usado repetidamente vira a ação padrão contra inimigos sozinhos (seção 14 do 14); o Passo Ágil fica como era. A guardiã da capela, medida por caminho, é vencida pelas três classes (Sombra e Piromante, os mais duros). **Critério mínimo atendido; concluída tecnicamente.** Adiado, sem ser requisito: um Passo Ágil com limite de repetição, a sinergia Desaparecer–Execução, Sombra e Piromante contra a guardiã no nível 4, a preparação de habilidades. Falta Jean jogar.
**Entrega:** fichas curtas de Guerreiro/Arqueiro/Mago e seis especializações, com ciclo, forças, fraquezas e lacunas.
**Tarefas:** aproveitar habilidades/talentos; integrar encruzilhadas; adicionar conteúdo apenas para lacunas reais.
**Pronto:** três classes atravessam a região; seis caminhos avaliados em cenários direcionados.
**Não fazer:** recriar passivas condicionais, adicionar classes ou evoluções sucessivas sem design.

## Entre a E5 e a E6: clareza da campanha (teste de Jean)

**Origem:** o primeiro teste real de Jean no Vale. O avanço para a E6 ficou pausado para esta frente.
**Estado:** primeira entrega na 1.60.0 (registro no 00):
- as correntes viraram uma ação só, com o como escolhido dentro (à mão, o método da classe ou voltar sem gastar nada);
- as ações da missão vêm primeiro no menu do lugar, marcadas "Missão"; os contratos, "Contrato";
- o frasco do lodo diz que é a prova para a decisão sobre Caspar;
- o Diário segue a ordem objetivo e lugar, o mais recente, caminhos e preparos, histórico. O rito aparece como caminho opcional e a Vigília diz quando aguarda a febre;
- um cartão compacto de atualização da missão por cena;
- os textos do Vale e da capela foram simplificados.

Nenhuma regra, custo, teste, encontro, recompensa ou número mudou.

Na 1.60.1, uma revisão de apresentação e texto, depois do teste de Jean. O critério adotado vale daqui em diante:
- **Ações fáceis de comparar.** O nome de cada ação é curto e começa pelo que se faz ("Soltar as correntes", "Descer ao fundo alagado", "Recolher uma amostra do lodo"), sem explicação entre parênteses.
- **Custos e riscos claros antes da escolha.** Ficam numa nota discreta embaixo da ação, junto com o teste: flecha gasta, luta que vem, o que acontece se falhar. Não se esconde consumo nem se transforma consequência conhecida em surpresa, e não se diz "sempre funciona" quando ainda é preciso vencer uma luta.
- **Porta ou ação, à vista** (1.60.2). Uma ação que leva a outra escolha, de onde se pode voltar, tem uma seta discreta no fim; a que age na hora não tem. O menu do lugar vem em grupos: Missão, Contratos e, depois de um fio, o de sempre. O passo que leva a história adiante fica por último entre os da missão. Nada de aviso de "decisão sem volta": quem diz isso é a própria escolha, lá dentro, com o risco na nota.
- **Leitura** (1.60.3).
  - Fonte pixel ou gótica só em título e rótulo curto. Frase se lê numa fonte de texto, em tamanho bom, com tinta escura e sem itálico em letra pequena.
  - Os papéis do Diário e as notas das opções usam a Alegreya Sans, irmã da Alegreya da história.
  - O cartão de novidade é uma nota dentro da história, na fonte dela, e não um papel por cima.
  - A Pixeloid Sans fica na "Fonte: pixel".
- **Critério editorial** (1.60.4; consolidado na 1.62.1, na seção [Critério editorial](#critério-editorial), que vale daqui em diante).
- **Conhecimento conforme as descobertas.** As telas e o Diário só mostram o que o personagem já descobriu, atribuído a quem ensinou. O rito aparece como o que Vó Berta contou, só depois da conversa com ela. Antes disso, o Diário mostra as perguntas que as pistas abrem, sem a receita. A finalidade da amostra do lodo aparece no Diário de Caspar, como o que se pode mostrar à praça.

**Próximas entregas** (cada uma é uma entrega à parte, nenhuma é requisito da E6):
1. **A bandagem da Odette** — *feita na 1.61.0.* A opção diz o que gasta ("Usa 1 bandagem da bolsa (você tem N)"). Sem bandagem, ela fica à vista, desabilitada e com o motivo escrito. O mesmo vale para "Deixar remédios na porta" (poção de vida).
2. **A proteção do mendigo** — *feita na 1.61.0.* Um aviso quando ela chega e outro na luta quando ela levanta você. A frase muda conforme a origem (mendigo, santuário, ou neutra num save antigo). Não aparece como item na bolsa.
3. **"Continuar → Exausto → Continuar"** — *reproduzido e corrigido na 1.61.0.* No mato, o segundo Continuar não tinha nada novo para ler. Na vila, a faixa "Exausto" passava por cima do texto do evento anterior.
4. **A dívida do Morel** — *pendente.* Uma dívida de verdade: pagamento depois e uma proposta de juros. Hoje a conversa sugere mais do que o jogo guarda.
5. **Revisão de loot** — *diagnosticada em 11/10/2026* ([16](16-E7-ITEM-E-LOOT.md), seções 2 e 3; medida com
   `python -m tests.saque_vale`).
   - O volume de suprimentos é alto: metade sai de baús, 1,5 por baú. O excesso que fica é de itens situacionais
     (antídoto, unguento, bomba), sem saída: não se vendem e a bolsa não tem limite.
   - **Um suprimento por baú, aplicado na campanha na 1.62.6** (o mundo gerado não muda).
     - Medido antes e depois, no 16, seção 3.1: suprimentos de baú de 9,7 para 6,3 por Vale; poções no fim de 3,0
       para 2,4.
     - O situacional repetido virar ouro fica de reserva.
     - O começo do jogo (fome, poucos baús) não muda e fica registrado para a E9.
     - Falta Jean jogar.

## E6 — Demonstrar transformação de habilidade

**Depende:** E5.
**Estado:** **implementada na 1.62.0** e validada tecnicamente (seções 11 a 13 do [15](15-E6-TRANSFORMACAO.md)). A
**Prisão de Gelo** é um talento do tronco do Mago (nível 4, 1 ponto) que libera outra versão da Lança de Gelo: 16 de
mana, 70% de dano de gelo sem esquiva, congela sem sorteio, salvo `firme`, chefes e gigantes. A compra é definitiva; a
versão se troca no Grimório, na vila ou no acampamento. A ficha se resolve por herói (`efetiva`), sem tocar no catálogo.
Medida em lutas inteiras: tem papel próprio (o inimigo forte que prepara o golpe) e não domina (equivalente em 80% das
células, nunca melhor em grupo, a repetição pior contra chefes e gigantes, nenhum impasse). Falta Jean jogar (seção 14
do 15).
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
**Estado:**
- **Primeira entrega implementada na 1.63.0:** o Broquel do Vigia (Guerreiro, apoio).
  - Com o escudo erguido, devolve cada golpe corpo a corpo que acerta o herói (Revide, 30% do Ataque).
  - O Contra-ataque tem prioridade sobre o Revide.
  - Vem do ossuário, uma vez. O ferreiro do Vau o oferece uma vez a saves antigos.
- **Medido** em lutas inteiras ([16](16-E7-ITEM-E-LOOT.md), seção 5.3): cria a decisão de erguer o escudo contra
  grupos corpo a corpo, sem dominar inimigo único, conjuradores nem Ilse; nenhum abuso relevante.
- **Falta Jean jogar:** os cenários `broquel` e `muralha`.
- **Não feitos:** os exemplos para Arqueiro e Mago. Ficam para depois da avaliação integrada do Vale.

## E8 — Introduzir identidade em escopo pequeno

**Depende:** E3–E4 e escolhas de 10-DECISOES.
**Entrega:** raça/origem em conjunto pequeno, com reconhecimento real.
**Proposta de limite:** duas raças e duas origens para primeiro teste; nomes e quantidade dependem de Jean.
**Tarefas:** catálogo e criação; persistência; uma oportunidade e uma repercussão por identidade ofertada.
**Pronto:** repetir com outra identidade muda oportunidades sem bloquear a história obrigatória.
**Não fazer:** campanhas independentes por combinação. Na região inicial, classe pode provar o padrão antes de raça/origem.
**Estado:** **adiada explicitamente** (decisão de Jean, 11/10/2026). Não é requisito da avaliação do Vale nem da
primeira versão de teste. Volta ao plano por decisão de Jean, depois da avaliação.

## E9 — Validar a região completa

**Depende:** E2–E8; extensões condicionais apenas se adotadas.
**Entrega:** percurso integrado e avaliação de preparação, loot, relações, combate e derrota.
**Pronto:** conclusão local com três classes; ramificações persistentes; consequências claras; motivos para repetir.
**Registrar:** evidência técnica e feedback de Jean.
**Decisão:** consolidar ou ajustar antes de ampliar. Raça/origem podem ser adiadas explicitamente, sem ficar falsamente marcadas como prontas.
**Não fazer:** adicionar sistemas para encobrir ritmo ruim.
**Estado (11/10/2026):** **antecipada,** como avaliação integrada do Vale do Turvo, o primeiro capítulo completo,
logo depois da primeira entrega da E7. A dependência da E8 cai: raças e origens estão adiadas (veja a E8).
**Primeira entrega feita (diagnóstico, sem mudar o jogo):** [17](17-E9-VALIDACAO-DO-VALE.md). Antes de liberar o
capítulo para teste: a fome e a infecção que prendem o save, o marco de fim do capítulo e a nota do custo do
companheiro (seção 7 do 17). **Não concluída:** falta Jean jogar (seção 8 do 17) e os jogadores novos (seção 9).

**O que já está registrado para ela:**
- o começo do Vale derruba o robô (fome nos níveis 1 e 2, quase sem ouro, sem poção), em especial o Mago
  ([16](16-E7-ITEM-E-LOOT.md), seções 2.7 e 3.1). Precisa ser confirmado com gente jogando antes de qualquer número.
  Diagnosticado no [17](17-E9-VALIDACAO-DO-VALE.md), seção 4: o que é do robô e o que persiste;
- a P2 do saque (situacional repetido vira ouro), de reserva;
- a validação de Jean jogando das entregas da E3 à E7, que nenhuma medida substitui.

**Medir a primeira partida** (em aberto: como medir ainda não foi decidido; nada implementado):
- com jogadores novos, que não conhecem a solução:
  - tempo total;
  - leitura;
  - combate;
  - exploração;
  - conteúdo opcional;
  - dificuldades de navegação (onde a pessoa se perde, volta, relê ou desiste);
- não substituem essa medida:
  - os dias do jogo;
  - as partidas do robô (`tests.saque_vale`);
  - os percursos de quem já conhece a solução;
- a duração que sair dela orienta o escopo. Não se acrescenta conteúdo só para aumentar a duração.

## E10 — Completar a campanha por trechos

**Depende:** E9.
**Entrega:** novas regiões/capítulos na quantidade definida em E1 e revisada após a experiência.
**Estado (11/10/2026):** depende da avaliação do Vale. O esboço de quatro regiões continua como direção, não como
obrigação anterior à primeira versão de teste (o Vale como capítulo completo).
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

## Critério editorial

Vale para todo texto novo ou revisto (campanha, eventos, opções, avisos, telas) e entra na revisão de cada entrega.
Consolida o da 1.60.4 e o da E6 (1.62.1).

**Cada camada tem um papel:**
- a **cena** descreve o que o personagem percebe;
- a **alternativa** expressa a ação, curta e começando pelo que se faz;
- a **nota** informa custo, requisito ou restrição relevante, numa linha discreta junto da opção, e não no meio da
  narração;
- o **resultado** apresenta o que aconteceu;
- a **confirmação** informa o que mudou, só quando isso ainda não estiver evidente na interface. Quando a própria tela
  já mostra a mudança (a página do Grimório marcando a versão "Em uso"), não há confirmação.

**Evitar:**
- repetir a mesma informação em duas camadas: a nota repetindo a cena, o resultado repetindo a alternativa, um aviso
  repetindo a frase ou o cartão de logo antes;
- narrar o clique que o jogador acabou de fazer;
- explicar "como o jogo funciona" no meio da história, quando a interface já mostra ou a escolha não precisa disso.

**Preservar**, sempre explícito antes da escolha: consumo de itens, recursos, testes, imunidades, indisponibilidade (com
o motivo), escolhas de fato permanentes, restrições importantes como luta sem fuga, e o que se aprendeu em conversa.
Clareza não vira ocultação de regra: nada de remoção geral de avisos.

**Nada de condição interna disfarçada de narração.** Porcentagem de vida, limiar de fase, etapa da missão e outros
estados do motor não viram frase da cena ("Ilse vacila à metade"). O número útil fica na interface (a barra de vida, o
Diário); a cena descreve o que acontece ("O canto de Ilse falha").

**Evidência como evidência.** O texto separa o que se observa, o que se supõe e o que prova algo, conforme o que o
personagem tem naquele momento. Uma amostra e um caminho de água sustentam um argumento; não demonstram ausência de
magia nem garantem que a praça aceite.

**Não antecipar** inimigos, consequências ou soluções que o personagem ainda não conhece. A nota diz o que se percebe
antes de agir ("barulhento", "o eixo range alto"), não o que vem depois. Nada de porcentagem inventada nem de obstáculo
físico criado só para justificar uma regra.

**Linguagem direta**, com a atmosfera da história: o nome do lugar com maiúsculas (a Fonte Nova), a referência genérica
com minúsculas (a fonte); a palavra comum no lugar da rara quando a rara não acrescenta nada ("o dono do moinho").

**Claro e concreto como padrão** (consolidado em 11/10/2026, decisão de Jean):
- **Frases de efeito e metáforas** entram quando acrescentam algo compreensível à cena ou à voz do personagem.
- **Informação importante não vira linguagem enigmática:** quem morreu, o que custou, o que mudou. A morte do homem
  diante de Odette é dita, não sugerida.
- **Isso não é cortar toda expressão literária.** A atmosfera e a voz de cada personagem ficam.
- **Diálogos respeitam o personagem, o contexto e a ação efetiva do jogador.** A fala depois de uma escolha reage ao
  que o herói de fato fez e ao resultado; quem só perguntou o nome não ouve agradecimento por ter ajudado.

### Levantamento da 1.62.1 (pendente, nada implementado)

Leitura direcionada dos textos da campanha, das notas e dos avisos de ação, pelo critério acima. Cada caso diz arquivo,
trecho, motivo e sugestão. Uma entrega à parte decide quais aplicar.

**Problemas claros:**
1. **A fita repetida.** `rpg/missoes.py:607`, `g.ui.efeito("Fita de Ilse", "item")`. O cartão da missão, logo depois,
   já diz "Você tem a fita de Ilse": são duas confirmações seguidas. Sugestão: tirar o aviso.
2. **O frasco do lodo repetido.** `rpg/caspar.py:356`, `g.ui.efeito("Frasco do lodo", "item")`. A narração ("enche um
   frasco com o lodo") e o cartão ("Uma amostra do lodo") já dizem o mesmo. Sugestão: tirar o aviso.
3. **"Isso a praça vai entender."** *Feito na 1.62.2*, com a leitura do lodo reescrita pela causa aprovada.
   `rpg/caspar.py:354`, na análise do mago. A frase antecipa para que a amostra serve,
   e o lodo pode ser recolhido antes de Caspar acusar alguém (etapa "antes"), quando o personagem nem sabe da praça.
   Sugestão: tirar a frase.
4. **"Responder depois", três vezes.**
   - `rpg/caspar.py:277`: "… Dá para responder depois.", logo acima da opção "Ainda não: responder depois";
   - `rpg/caspar.py:287`: "Você pode responder a Caspar na praça do Vau quando quiser.", depois de escolhê-la. O
     menu ("Ir à praça responder a Caspar") e o Diário já mostram isso.

   Sugestão: tirar as duas frases e manter "Para denunciar Caspar, falta prova: …", que é indisponibilidade com motivo.
5. **A frase da vila repete a cena de volta.** `rpg/consequencias.py` (`FRASES`, chamada em `rpg/jogo.py:517`). Ao
   chegar depois da guardiã, a cena "De Volta ao Vau" e a da praça descrevem a Fonte Nova, a vigília e onde Yara
   espera; o menu da vila, em seguida, repete quase palavra por palavra. Sugestão: depois de uma cena de missão na
   vila, marcar a frase do lugar como vista (`ambiente_visto`) até o período mudar.
6. **A nota de "à mão" conta o que vem depois.** `rpg/missoes.py:553`, `NOTA_MAO = "Demorado e barulhento: o eixo
   range, e o som corre pela água da capela inteira."`. O resultado repete a frase, e o comentário do próprio código
   pede o contrário. Sugestão: "Demorado e barulhento: o eixo range alto."
7. **O recuo do sarilho diz o errado.** `rpg/missoes.py:406`, "A sala continua por vencer. Dá para voltar quando
   quiser.", também usado no sarilho (`:511`). Ali o ossuário já foi vencido; o que fica são as correntes, e a narração
   acabou de dizer isso. Sugestão: no sarilho, sem essa linha.
8. **O cartão de Vó Berta antecipa a conversa.** `rpg/missoes.py:796`, `"efeito": "Ela estava lá quando a vila afogou
   Ilse"`. É o que só a conversa revela. Sugestão: o que se percebe, por exemplo "A mais velha da taverna; viveu no
   Vau a vida toda."
9. **"Mandar para o acampamento" dito duas vezes.** `rpg/comitiva/fogueira.py:127`, "{nome} pega as coisas e volta para
   o acampamento. Quando você montar a fogueira, vai estar lá.", seguido do aviso "{nome} vai esperar no acampamento".
   Sugestão: só o aviso, como na fogueira.
10. **O ganho de atributo repetido entre parênteses**, depois do selo de `bonus_permanente`. Quando o teto corta o
    ganho, os parênteses ainda contradizem o motor.
    - `rpg/eventos/classe.py:544`, "(+8 Mana máxima)";
    - `rpg/eventos/classe.py:548`, "(+2 Poder)";
    - `rpg/eventos/classe.py:595`, "(+4 Mana máxima, mana restaurada)";
    - `rpg/eventos/comuns.py:312`, "(+5 vida máxima)";
    - `rpg/eventos/comuns.py:326`, "(+1 permanente)".

    Sugestão: tirar os parênteses; na `:595`, manter só "mana restaurada".
11. **O rito comemorado como derrota.** Dando descanso a Ilse, a festa diz "Guardião derrotado!"
    (`telas/celebracoes.js:220`) e "Ilse, a Bruxa Afogada caiu" (`:265`). Sugestão: o motor manda um rótulo de
    desfecho, e a festa mostra "Ilse descansou".
12. **A Vigília quando Yara já morreu.** `rpg/caspar.py`, objetivo "Caspar acusa Yara…". No ramo em que Yara morreu na
    fogueira, Caspar acusa "mais de uma", não ela. Sugestão: objetivo pelo ramo, ou "Caspar culpa uma bruxa pela febre".
13. **Custo dentro do rótulo**, contra o critério de 1.60.1:
    - `rpg/eventos/classe.py:527`, "Absorver a energia (arriscado)";
    - `rpg/eventos/classe.py:588`, "Meditar sobre ela (passa o tempo)";
    - `rpg/eventos/comitiva.py:620`, "(−1 provisão)".

    Sugestão: o custo na `nota`.

**Continuidade e "brejo" (1.62.4):**
- *Feito:*
  - Odette fala conforme o que o herói fez: ajudou, ficou até o fim sem conseguir, ou só perguntou o nome. A morte
    do homem fica dita com clareza. (Na 1.62.5, perguntar passou a voltar ao menu; veja o fluxo abaixo.)
  - Na fogueira de Yara, na campanha, Caspar é chamado pelo nome do começo ao fim, e não mais de "o pregador" nas
    falas seguintes.
  - O narrador e o Diário deixaram de usar "a moça do brejo" como apelido e "na beira do brejo" para um lugar que não
    existe no mapa. Ficam Yara, o Charco dos Juncos ou "do lado de fora".
- *Mantido de propósito:*
  - "brejo" na voz de Caspar ("a bruxa do brejo"), nas falas e cenas de Yara dentro do Charco, e na geografia da
    capela (o canal corre pelo brejo até ela);
  - o título de Yara na comitiva, "bruxa do brejo". Escolha de estilo: é o mesmo nome da família de inimigos "bruxa do
    brejo".
- *Escolha de estilo, registrada:* depois da luta com os Cães de Ferro (`teodoro_ruivo`), a cena não diz se Theodore
  morreu, e "Não fica claro se fala da luta ou da ponte" comenta a cena em vez de mostrá-la.

**Fluxo (registrado na 1.62.4, corrigido na 1.62.5):**
- **Odette na estrada.** `rpg/eventos/comitiva.py`, `odete_na_estrada`.
  - Era: "Perguntar quem ela é" estava no mesmo menu das formas de ajudar. Escolhida, a cena terminava: o homem
    morria, e não havia como ajudar depois de saber o nome dela.
  - Agora:
    - ela diz o nome sem tirar as mãos da ferida ("O resto, depois. Ele ainda respira.") e as ações voltam, sem a
      pergunta;
    - perguntar não gasta tempo, item nem sorteio, e não muda reputação, aprovação nem o encontro. Não dá para
      repetir;
    - ajudar, revistar e seguir têm os mesmos custos, testes e efeitos. A fala da oferta acompanha a ação final e o
      resultado. Só perguntar já não leva à oferta: a oferta vem de ajudar;
    - o narrador só chama a mulher de Odette depois que ela diz o nome ("A mulher se levanta" ao revistar sem
      perguntar; "Odette começa a rezar" ao seguir depois de perguntar).

**Escolhas de estilo:**
14. **Recuo nas salas.** `rpg/missoes.py:406`, "Dá para voltar quando quiser.". É meta-texto, e a ação continua no
    menu. Sugestão: ficar com "A sala continua por vencer."
15. **A denúncia repete a alternativa.** `rpg/caspar.py:304`, "A febre veio do que todos beberam, não de uma moça no
    brejo.", depois da opção "a febre veio da água, não da Yara". Sugestão: ficar com o caminho da água.
16. **O momento do rito.** `rpg/missoes.py:662`, "(dar descanso)" e "(destruir)" no rótulo. Sugestão: rótulos sem
    parênteses e, na segunda, a nota "Sem volta: a luta segue até destruí-la."
17. **Odette.** `rpg/eventos/comitiva.py:117`, "(Odette procura a mãe de Thomas. Talvez você a encontre em alguma
    vila.)". A primeira frase repete a fala dela; a segunda é a única pista da missão pessoal. Sugestão: só a dica, ou
    mostrá-la na tela da Comitiva.
18. **"Moleiro".** `rpg/eventos/comitiva.py:408` e `:442`, depois de a pista passar a "o dono do moinho". Na fala de
    Yara (`:442`), a palavra combina com a voz dela. Sugestão: na narração (`:408`), "o dono do moinho".
19. **"Se acertar" na Prisão de Gelo.** A linha do Grimório vem de `Se.PREFIXO`, em `rpg/habilidades.py:173`, e fica ao
    lado de "Não pode ser esquivado." Sugestão: sem o prefixo quando o golpe não se esquiva.
20. **O contrato em andamento no espólio.** "Eliminar 3 javalis em …" e, ao lado, "2/3 javalis selvagens". Sugestão:
    só "2/3" à direita.

## Critério geral

Registrar feito, validado tecnicamente e validado jogando separadamente. Refatoração pura preserva comportamento; mudanças intencionais são identificadas e seguem os guias técnicos. Não ampliar suíte por rotina nem atualizar gabarito para ocultar alterações incidentais.
