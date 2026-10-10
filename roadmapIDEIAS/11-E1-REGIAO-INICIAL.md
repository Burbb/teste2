# 11 — E1: proposta da primeira região (Vale do Turvo)

Revisão 2 — 10/10/2026, sobre a versão 1.47.1. Proposta de design: nada aqui está implementado nem aprovado. Nomes de lugares e pessoas são provisórios. A campanha, os Sigilos, a cronologia, o protagonista, a derrota e a transição do procedural estão em [12-E1-CAMPANHA.md](12-E1-CAMPANHA.md).

Legenda:
- **[existe]**: conferido no código da 1.47.1.
- **[hipótese]**: Jean aceitou como hipótese de trabalho.
- **[proposta]**: depende da aprovação de Jean.

**Revisão 2:**
- "Dar descanso" ganhou investigação e ações próprias.
- Destruir ficou defensável.
- A guardiã e Caspar viraram dois eixos independentes.
- A causa da febre foi detalhada.
- Ficou definido quem atende e resgata enquanto Marta está doente.

## 1. Resumo da recomendação

O herói volta ao Vau do Turvo, onde uma febre se espalha desde que o poço secou e uma fonte nova apareceu. A água da fonte passa por uma capela afundada. Lá, o corpo de Ilse, afogada como bruxa pela própria vila há cerca de 55 anos, virou o canal por onde um Sigilo rachado vaza a Fenda.

A região tem **duas decisões independentes**:

| Eixo | Pergunta | Opções |
|---|---|---|
| **A guardiã** | O que fazer com Ilse? | **Destruir** ou **Dar descanso** |
| **Caspar** | O que fazer com a caça à bruxa e com a perseguição à Yara? | **Apoiar**, **Denunciar** ou **Calar** |

Qualquer combinação é possível: dá para destruir a guardiã e ainda denunciar Caspar. As consequências se somam elemento por elemento na vila. Não há capítulo por combinação.

Peças existentes que a região aproveita [existe]:
- o evento da Yara, que já fala em poço seco, febre e moleiro;
- a guardiã Bruxa Afogada, que invoca afogados;
- a Pele do Penitente ("Ninguém sabe quem ela era");
- as etiquetas de reação da comitiva;
- `plantar`/`colher`;
- os serviços da vila.

## 2. Mapa da região [proposta]

| Lugar | Tipo/bioma | Papel | Nível típico |
|---|---|---|---|
| **Vau do Turvo** | vila | Casa do herói; a Fonte Nova; Marta de cama; Caspar na praça | — |
| **Charco dos Juncos** | pântano | Yara na fogueira; sapos, sanguessugas; afogados à noite | 1–2 |
| **Bosque do Moinho** | floresta | Moinho, represa, comporta e o canal que leva à capela; lobos, bandidos | 2–3 |
| **Morro da Forca** | planície | **Opcional.** A árvore da forca antiga; bandidos | 2–3 |
| **Capela Afogada** | covil (ruínas/pântano) | Masmorra linear de três salas e a guardiã | 3–4 |
| **Estrada de Varn** | saída | Fechada até o fim; leva à região 2 | — |

```
           Morro da Forca (opcional)
                 │
Charco ─── Vau do Turvo ─── Bosque do Moinho ─── Capela Afogada
dos Juncos       │            (represa, canal)
           Estrada de Varn (fechada)
```

## 3. Personagens locais [proposta]

| Personagem | Quem é | Função |
|---|---|---|
| **Marta** | Curandeira da vila; escreveu a carta (laço com o herói: ver [12](12-E1-CAMPANHA.md), seção 3) | Motivo pessoal; de cama até a febre acabar |
| **Pita** | Aprendiz de Marta, menina de uns 14 anos | Atende pela curandeira e organiza o resgate enquanto Marta está doente |
| **Irmão Caspar** | Pregador itinerante, ex-irmão da catedral; perdeu a mulher para a febre | Chefia a caça à bruxa. Não é o clérigo do templo: o templo continua funcionando como hoje |
| **Vó Berta** | Velha da taverna; tinha oito anos quando a vila afogou Ilse; o pai dela segurou a corda | Testemunha; guarda a fita de Ilse e a vergonha da família |
| **Anselmo** | Moleiro; ergueu a represa e abriu o canal no ano passado | Causa material, sem saber; opcional como cena, essencial como fato |
| **Ilse, a Afogada** | Guardiã da capela e do Sigilo do Turvo, afogada como bruxa | A guardiã Bruxa Afogada existente, com nome e história |

Ninguém aqui é vilão puro:
- Caspar está de luto e acredita no que prega.
- Anselmo queria moer mais trigo.
- Ilse é vítima e também é perigo real: os afogados que ela levanta já mataram dois pescadores este ano.

## 4. Como a febre acontece e como acaba [proposta]

### A cadeia de causas

1. **O Sigilo.** Há cerca de 58 anos, a Igreja deixou o Sigilo do Turvo na cripta da capela, aos cuidados de Ilse (ver [12](12-E1-CAMPANHA.md), seção 4).
2. **O crime.** Nos anos de medo depois da Primeira Fenda, a vila afogou Ilse como bruxa. Ela foi presa com correntes às mós velhas do moinho, no fundo da cripta, com o Sigilo ainda no peito. A capela foi abandonada e o brejo a cobriu.
3. **A rachadura.** Desde a Reabertura, há cerca de 3 anos, os Sigilos estão sob esforço e racharam. O do Turvo vaza a Fenda por onde está preso: o corpo de Ilse. A cripta era água parada e fechada; o vazamento ficava ali. Os sapos do brejo nascem deformados; Ilse desperta.
4. **O canal.** No ano passado, Anselmo represou o riacho e abriu um canal para mover o moinho com mais força. O canal cortou o muro da cripta afundada, e a água agora entra limpa, atravessa o corpo de Ilse e sai do outro lado.
5. **A Fonte Nova.** Com o riacho represado, o trecho da vila baixou e **o poço secou** (texto existente da Yara). Na mesma época, a água que atravessa a cripta brotou numa fonte nova perto da vila. A vila a recebeu como bênção e passou a beber dela.
6. **A febre.** Quem bebe da Fonte Nova adoece: febre, unhas escuras, sonhos com água. Velhos, crianças e quem cuida dos doentes, como Marta, adoecem mais. À noite, a água que passa por Ilse levanta afogados no Charco.

Em resumo: **fonte da contaminação** (Sigilo rachado e corpo de Ilse) + **caminho** (canal → cripta → Fonte Nova) + **quem bebe** (a vila, sem o poço).

Compatibilidade: o texto atual da Yara ("o poço secou porque o moleiro desviou o riacho", "a febre vem do poço, não dela", "água parada") [existe] continua verdadeiro. Ele só não conhece a parte sobrenatural. Ajustar uma palavra ("do poço" → "da água") é opcional e fica para a implementação.

### O que encerra a febre

| Ação | Efeito |
|---|---|
| Tirar o Sigilo do corpo de Ilse (as duas soluções da guardiã) | Corta a **fonte**: a água volta a ficar limpa em poucos dias e a febre acaba |
| Fechar a comporta do canal (ação opcional, antes ou depois) | Corta o **caminho**: a água para de passar pela cripta, o riacho volta e o poço enche de novo em alguns dias; o moinho perde força |

Diferença entre as soluções da guardiã:
- **Destruir** rompe o corpo à força. O lodo acumulado nele sai de uma vez: a Fonte Nova corre escura por uma noite, a febre piora (Marta inclusive) e depois some em uns 3 dias. **Se a comporta estiver fechada antes, o golpe fica preso na cripta e não há piora.**
- **Dar descanso** solta o Sigilo sem romper o corpo. O lodo assenta e a água limpa em uns 2 dias, sem piora.

Não há relógio fatal [proposta]. Os dias que passam deixam a febre visível (Marta mais fraca, falas da vila, estoque do mercado), mas ninguém nomeado morre por prazo.

### Informações essenciais e onde aparecem

As cenas obrigatórias abaixo carregam tudo o que o jogador precisa entender. Mesmo que todas as opcionais sejam cortadas, a história continua compreensível.

| Informação | Cena obrigatória |
|---|---|
| A febre começou quando o poço secou e surgiu a Fonte Nova | Chegada: Marta de cama |
| O moleiro represou o riacho e abriu um canal rumo ao brejo | Bosque do Moinho: o canal é o caminho até a capela |
| O canal atravessa a capela afundada e sai na Fonte Nova | Capela, sala 1: o muro rompido por onde a água entra |
| Uma guardiã foi afogada ali como bruxa; o que ela guardava | Capela, sala 2: registro da sacristia |
| Homens com a marca do bispo procuram o Sigilo | Capela, sala 2: os cultistas |
| A água escura sai do corpo dela, onde está o Sigilo | Capela, fundo |
| A febre acaba; a Fonte limpa | Retorno |

## 5. Missão principal: "A Febre do Turvo" [proposta]

1. **Chegada.** Febre, Marta de cama, Pita atendendo, Caspar na praça. Diário: "Descobrir de onde vem a febre."
2. **Investigar.** Em qualquer ordem: o Charco (Yara), o Bosque (canal), a taverna (Vó Berta), o poço (mago).
3. **Capela Afogada.** Salas 1 a 3, com a escolha de preparo para "Dar descanso" na sala 3.
4. **A guardiã.** Destruir ou Dar descanso.
5. **Retorno.** A praça: o momento de Caspar. Consequências.
6. **Conclusão.** A febre acaba; o Sigilo aponta para Varn; a estrada abre.

## 6. Eixo 1: a guardiã

### Destruir

**Requisito:** nenhum. É a solução geral, disponível assim que se chega ao fundo.

**Preparos opcionais:**
- **Bênção de Caspar** (água benta): a guardiã começa a luta enfraquecida. Pedi-la é conversa, não promessa de apoio; o eixo de Caspar continua aberto.
- **Comporta fechada:** sem piora da febre.

**Vantagens:**
- é rápido;
- não depende de confiar numa morta furiosa;
- não exige envolver ninguém da vila;
- com preparo, é a luta mais segura;
- dá a Pele do Penitente, item forte para qualquer classe.

**Riscos:** a luta completa, com as duas fases da guardiã [existe].

**Custos:**
- sem a comporta fechada, uma noite pior de febre;
- os afogados do Charco ainda aparecem por alguns dias;
- o que Ilse sabe sobre os Sigilos se perde: o jogador aprende só pelo registro e, depois, na região 2.

**Por que é defensável:** Ilse está matando gente hoje. Um rito pode falhar. A vila precisa de água limpa agora. Ninguém que destrói a guardiã é tratado pelo jogo como cruel; Odette, por exemplo, aprova a purificação.

### Dar descanso

Exige três ações próprias, além de saber o nome:

| Passo | O que é | Caminho geral | Atalhos |
|---|---|---|---|
| **D1. A verdade** | Quem era Ilse, por que foi afogada, onde está presa e o que ela usava | Sacristia (nome e acusação) **e** Vó Berta, que, diante do nome, conta das correntes e das mós e entrega a fita de Ilse | Yara presente (ouve na água); mago: eco no poço (Arcano); arqueiro: nome entalhado no Morro da Forca (Percepção) |
| **D2. Soltar o corpo** | No ossuário, o sarilho velho prende as correntes às mós | Soltar à mão: leva tempo, faz barulho e atrai uma onda de afogados (uma luta a mais) | Guerreiro: Força; mago: Arcano (o ferro apodrece); arqueiro: tiro no pino da trava (Destreza) |
| **D3. O rito** | Diante da guardiã, com a fita e o nome | A luta começa normalmente. Quando ela cai à metade, em vez da 2ª fase aparece "Devolver o nome e a fita": ela para, larga o Sigilo e afunda em paz | — |

**Falhas:**
- Sem D1, a opção não aparece.
- Sem D2, ela tenta e não consegue sair das correntes, e a luta segue para a 2ª fase: vira Destruir.
- Usar a bênção de Caspar fere a morta e impede o rito. Quem pega a bênção escolheu destruir.

**Vantagens:**
- a água limpa sem piora;
- os afogados do Charco param na hora;
- Ilse fala antes de afundar: explica o que é um Sigilo, que eles são três e que o bispo quer juntá-los;
- a família de Berta dá uma herança;
- Yara e Odette aprovam.

**Riscos e custos:**
- mais dias, logo mais dias de febre;
- uma luta a mais no caminho geral do D2;
- enfrentar a primeira fase sem bênção;
- tochas e suprimentos;
- risco real de falhar e cair em Destruir no fim;
- Berta pede que o nome do pai dela fique fora da história.

### Sem equivalência artificial

As duas soluções não dão recompensas iguais nem têm o mesmo peso moral:
- **Dar descanso** é mais justo com Ilse e custa mais ao herói.
- **Destruir** é a escolha prudente para os vivos, e o custo recai sobre a memória de Ilse e sobre o que se deixa de saber.

As recompensas diferem em natureza:
- Destruir: segurança, rapidez e um item forte.
- Dar descanso: conhecimento, paz no Charco e uma herança.

## 7. Eixo 2: Caspar e a perseguição à Yara

| Momento | Cena | Opções |
|---|---|---|
| **Charco** | A fogueira da Yara [existe]; Caspar é o homem de batina remendada | As opções existentes (Força, Carisma, Arcano, ouro, deixar) |
| **Vila** (só se a Yara estiver na comitiva) | A vigília de Caspar barra a entrada da Yara na praça | Enfrentar (Carisma ou Força); deixá-la no acampamento (reserva existente); ignorar e entrar assim mesmo (a vila fica fria com o herói) |
| **Retorno** (sempre) | Caspar reivindica o fim da febre como vitória sobre a bruxaria | **Apoiar**, **Denunciar** ou **Calar** |

**Denunciar exige prova.** Opções:
- **geral:** um frasco do lodo da cripta, sempre coletável no fundo, mais o canal;
- **mais forte:** a análise do mago, as ervas da Yara, ou Anselmo admitindo o canal (cena opcional).

O teste de Carisma diz como a praça recebe a denúncia; a prova mais forte facilita.

| Postura | O que acontece |
|---|---|
| **Apoiar** | Caspar conduz a vigília e a vila gosta do herói (reputação +). A Yara não entra mais no Vau (fica no acampamento quando o grupo está na vila). Semente: caçadores de bruxas na região 2 |
| **Denunciar, com sucesso** | Caspar perde a praça e vai embora. Yara anda livre. Reputação + com a maioria. Semente: Caspar volta como pregador do Vazio |
| **Denunciar, com falha** | Caspar fica, sem a vigília; a vila dividida olha torto para o herói. Yara entra, mas é vigiada. Sem semente |
| **Calar** | Caspar segue como estava. A Yara continua barrada se estava. Sem semente |

Os eventos de caçadores de bruxas e de pregador do Vazio já existem [existe]. As sementes usam `plantar`/`colher` [existe].

## 8. Consequências ao voltar: soma dos dois eixos [proposta]

Cada eixo controla os seus elementos. Não há texto por combinação.

| Elemento da vila | Controlado por | Resultado |
|---|---|---|
| Fonte Nova | Guardiã (e comporta) | Escura uma noite (Destruir sem comporta) ou limpa |
| Ilse | Guardiã | Destruir: os ossos são queimados (se Caspar foi apoiado) ou enterrados sem nome. Dar descanso: pedra com o nome junto à fonte |
| Charco à noite | Guardiã | Afogados por alguns dias (Destruir) ou nenhum (Dar descanso) |
| Praça | Caspar | Vigília (Apoiar), praça vazia (Denunciar) ou como estava (Calar) |
| Yara na vila | Caspar | Barrada ou livre |
| Taverna | Os dois | Canção da caça à bruxa (Apoiar) ou a história de Berta (Dar descanso), uma fala curta cada |
| Curandeira | Marta curada | Marta volta ao serviço. Com Dar descanso, desconto (gratidão de Berta) |
| Mercado | Febre e comporta | Estoque baixo de provisões durante a febre. Comporta fechada: farinha mais cara por uns dias |

Exemplo: **Destruir + Denunciar.** A guardiã foi destruída e a Fonte limpou; os ossos foram enterrados sem nome; Caspar foi embora; a Yara anda livre; o herói tem a Pele do Penitente.

## 9. A masmorra: Capela Afogada [proposta]

Masmorra linear, sem mapa interno. Salas vencidas ficam vencidas no save.

| Sala | Conteúdo | Reaproveita |
|---|---|---|
| 1. Nave alagada | O muro rompido pelo canal; afogados e sanguessugas; escuridão | Famílias `afogado`, `sanguessuga`; luz |
| 2. Sacristia | Registro (nome, acusação, nota sobre "o Sigilo do Turvo"); dois cultistas com a marca do bispo; baú trancado | `cultista`; baú existente |
| 3. Ossuário | Esqueletos; o sarilho das correntes (D2); descanso curto, uma vez | `esqueleto` |
| Fundo | Ilse; frasco de lodo (prova); a escolha | Guardião `bruxa_afogada` com as fases [existe] |

## 10. As três classes fora da luta [proposta]

| Classe | Oportunidades |
|---|---|
| Guerreiro | Soltar a Yara (Força) [existe]; fechar a comporta sozinho (Força); D2 por Força; enfrentar a vigília de Caspar |
| Arqueiro | Rastrear a água até a entrada lateral (pula a sala 1); nome no Morro da Forca (D1); D2 com um tiro; caçar comida para os doentes |
| Mago | Assustar a turba (Arcano) [existe]; analisar a Fonte Nova (D1 e prova forte para Denunciar); D2 por Arcano; ler o selo antes da luta |

Toda etapa obrigatória e as duas soluções de cada eixo têm um caminho geral. Os atalhos economizam tempo, luta ou recursos; nenhum é exigido.

A especialização (nível 4) [existe] fica como está: a encruzilhada dispara no descanso. Amarrá-la a um lugar fica para a E5.

## 11. Comitiva [proposta, sobre conteúdo existente]

Limite de dois por vez, com a reserva no acampamento [existe]. No máximo uma cena local por companheiro. Os arcos em três atos continuam como estão.

| Companheiro | Encontro (existe) | Na região | Arco depois |
|---|---|---|---|
| **Yara** | `yara_na_fogueira` | Alvo de Caspar; ajuda no D1 e na prova; reage forte aos dois eixos. Se morrer na fogueira (opção existente), tudo continua pelos caminhos gerais | Voz de Ulook e círculo negro: região 3 |
| **Odette** | `odete_na_estrada` | Caspar a reconhece da catedral (cena curta e cortável). Aprova Destruir (purificação) e Dar descanso (verdade, misericórdia); aprova Denunciar (honestidade) | Mãe de Thomas: região 2 |
| **Morel** | `morel_na_taverna` | Pragmático: prefere Destruir. Não gosta de autoridade, então não se opõe a Denunciar. Pode ajudar a fechar a comporta | Theodore (nível ≥ 5): região 2 |

## 12. Marta doente: quem atende e quem resgata [proposta]

**Atendimento.** O serviço da curandeira **nunca fecha** enquanto há ferimento para tratar. Fechar o serviço impediria tratar infecção, que mata [existe: `sobrevivencia`, `servicos.curandeiro`]. Pita atende com as mesmas regras e preços, e Marta orienta da cama (só o texto muda). Quando Marta sara, ela volta ao serviço; o desconto da seção 8 vale a partir daí.

**Resgate.** Na região 1, quem cai é encontrado por gente da vila chamada por Pita e acorda na casa de Marta, com as perdas do resgate atual (`jogo.py:248`). Depois da cura, Marta assume. Fora do vale vale o resgate genérico existente.

**Templo.** Continua com o clérigo e o serviço atuais [existe]. Caspar não o administra.

## 13. Recompensas [proposta]

| Origem | Recompensa |
|---|---|
| Guardiã (sempre) | **Sigilo** e ponto de talento [existe] |
| Destruir | **Pele do Penitente** (único existente; armadura de qualquer classe) |
| Dar descanso | Herança da família de Berta: raro da classe do herói (gerador existente); o relato de Ilse sobre os Sigilos |
| Apoiar Caspar | Reputação na vila |
| Denunciar com sucesso | Reputação; aprovação da Yara |
| Salas e Bosque | Saque comum e mágico; baú trancado na sacristia [existe] |
| Opcional | Contrato de caça no mural [existe] |

## 14. Conteúdo opcional (pouco)

- **Morro da Forca:** área curta, atalho de arqueiro para o D1.
- **Anselmo e a comporta:** a cena com o moleiro. A comporta em si pode ser acionada sem a cena.
- **Contrato de caça** no mural.
- **Eventos aleatórios existentes** nas áreas externas.

## 15. Percursos revisados (exemplos)

**A. Rápido e prudente: Destruir + Apoiar**

Vila → Charco (salva a Yara) → Bosque → pede a bênção a Caspar → Capela → destrói Ilse → noite pior de febre → praça: apoia Caspar.

Resultado: ossos queimados, vigília, Yara barrada no Vau (desaprova), reputação alta, Pele do Penitente. Semente: caçadores de bruxas.

**B. Prudente com a vila, justo com a Yara: Destruir + Denunciar**

Vila → Charco → Bosque (fecha a comporta) → Capela → destrói Ilse sem piora da febre → recolhe o lodo → praça: denuncia.

Resultado: ossos enterrados sem nome, Caspar vai embora, Yara livre, Pele do Penitente. Semente: pregador do Vazio.

**C. O caminho longo: Dar descanso + Denunciar**

Vila → Charco → Bosque → Capela até a sacristia (nome) → volta à taverna (Berta, fita, correntes) → Capela, ossuário (solta as correntes; luta a mais) → Ilse até a metade → rito → Ilse explica os Sigilos → praça: denuncia com a prova.

Resultado: pedra com o nome, Charco calmo, herança de Berta, Yara e Odette aprovam muito. Mais dias de febre no caminho.

Em todos: a febre acaba, Marta sara, o Sigilo aponta para Varn e a estrada abre.

## 16. Sistemas reaproveitados

| Necessidade | Sistema existente |
|---|---|
| Lugares, viagem, mapa, clima, noite | Grafo do `mundo`, `sistemas/navegacao.py`, `mapa.js`, `vista.js` |
| Encontros | Famílias de inimigos, biomas, eventos aleatórios |
| Guardiã, fases, Sigilo | `bruxa_afogada`, `sistemas/chefes.py` |
| Cenas, testes, lutas | `menu`, `teste`, `combate`, eventos |
| Comitiva | Eventos de encontro, `REACOES`, aprovação, reserva no acampamento |
| Consequências futuras | `plantar`/`colher`; eventos `cacadores_de_bruxas` e `pregador_do_vazio` |
| Vila | Serviços da taverna, templo, curandeira e mercado; `predios_fechados` |
| Recompensas | Únicos, gerador de raros, baú, espólio, reputação |
| Derrota | `Jogo.resgate` [hipótese] |
| Save | `persistencia.py`, `migracoes.py` |

## 17. Extensões necessárias (mínimas, para E2 a E4)

1. **Começar a campanha** (E2): outro início e outro prólogo, sem mexer no procedural (`jogo.py:197–237`).
2. **Região como dados** (E2): locais com id estável, nível fixo e saída fechada.
3. **Cenas presas a lugar e etapa** (E3): hoje `evento_forcado` ignora o contexto (`sistemas/recompensas.py:254`).
4. **Registro de missão** (E3): etapa, desfecho de cada eixo, recompensas pagas; migração do save (`VERSAO_SAVE` 3).
5. **Masmorra linear** (E3): salas em sequência com progresso salvo.
6. **Rito no meio da luta de chefe** (E3): ao passar o limiar da 1ª fase, oferecer uma ação em vez de entrar na 2ª. As fases já têm `limiar` [existe]; falta o gancho que pergunta ao jogador.
7. **Estado da vila** (E4): falas e serviços segundo os dois eixos; Yara barrada na praça usando a reserva.
8. **Encontros previsíveis da comitiva** (E4): os mesmos eventos, com gatilho de lugar e etapa.
9. **Resgate e atendimento locais** (E4): Pita e Marta no lugar do NPC sorteado (`jogo.py:248`) e da curandeira genérica.

## 18. O que cortar se o escopo crescer

Em ordem:
1. Morro da Forca (o atalho do arqueiro para o D1 vai para a Capela).
2. A cena com Anselmo (a comporta continua acionável).
3. A cena de Caspar reconhecendo a Odette.
4. A vigília que barra a Yara antes do retorno (o eixo Caspar fica só no Charco e no retorno).
5. Atalhos de classe além de um por classe.
6. A noite pior de febre do Destruir (a diferença fica nos afogados do Charco e no relato de Ilse).
7. Contrato no mural.

Não cortar:
- as cenas obrigatórias da seção 4;
- os dois eixos com suas opções;
- os três passos do Dar descanso;
- a consequência visível na volta;
- o save no meio da missão;
- o caminho geral para as três classes.

## 19. Riscos

- **Tamanho:** dois eixos e três passos já pedem bastante texto. A implementação pode começar com vila, Charco, Bosque e Capela.
- **Dificuldade:** a guardiã entra no nível da região + 1 (`chefes.py:13`). No nível 4 é preciso medir com e sem bênção, e o Dar descanso parando à metade.
- **Yara morta:** nenhuma fala posterior pode presumir a Yara viva; o eixo Caspar continua no retorno.
- **Clareza:** o jogador precisa saber, antes do fundo, que existe outro jeito. O registro da sacristia e o relato de Berta devem sugerir isso sem dizer como.
