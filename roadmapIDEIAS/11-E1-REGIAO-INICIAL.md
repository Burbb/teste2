# 11 — E1: proposta da primeira região (Vale do Turvo)

Proposta de design, 10/10/2026, sobre a versão 1.47.1 (commit `622b1b6`). Nada aqui está implementado nem aprovado. Nomes de lugares e pessoas são provisórios. O arco da campanha, a cronologia, a derrota e a transição do procedural estão em [12-E1-CAMPANHA.md](12-E1-CAMPANHA.md).

Legenda usada abaixo:
- **[existe]**: conferido no código da 1.47.1.
- **[hipótese]**: Jean aceitou como hipótese de trabalho, sem decisão definitiva.
- **[proposta]**: depende da aprovação de Jean.

## 1. Resumo da recomendação

O herói volta para casa, uma vila de beira-rio onde uma febre se espalha. Um pregador culpa uma "bruxa" e quer queimá-la. A causa verdadeira é a água: o riacho desviado pelo moinho passa agora por uma capela antiga, afundada no brejo. Ali repousa uma mulher que a própria vila afogou como bruxa há duas gerações. A Fenda a deformou, e ela guarda um Sigilo.

A missão principal tem duas soluções no fundo da capela:
- **Destruir** a Afogada: combate completo, com ajuda opcional do pregador.
- **Dar descanso** a ela: chamá-la pelo nome verdadeiro, descoberto na região.

Na volta, a vila mostra o que o jogador escolheu: fogueira e pregador fortalecido, ou memorial e pregador desacreditado. As duas soluções dão o primeiro Sigilo e abrem a estrada para a segunda região.

Por que esta região: ela aproveita conteúdo que já existe e combina entre si.
- O evento da Yara já fala em "gado morto, poço seco, crianças com febre" e no "moleiro que desviou o riacho" (`eventos/comitiva.py`, `yara_na_fogueira`) [existe].
- A Bruxa Afogada já é guardiã do pântano e invoca afogados (`dados.py`, `GUARDIOES["pantano"]`) [existe].
- A Pele do Penitente já tem a história "Ninguém sabe quem ela era" (`itens.py`) [existe].
- O tema, uma vila que repete um crime antigo, liga a Yara (quase queimada), a Odette (culpa e verdade) e a primeira revelação sobre os Sigilos.

## 2. Mapa da região [proposta]

| Lugar | Tipo/bioma | Papel | Nível típico |
|---|---|---|---|
| **Vau do Turvo** | vila | Casa do herói; febre; pregador; Marta (irmã e curandeira) | — |
| **Charco dos Juncos** | pântano | Yara na fogueira; sapos, sanguessugas; afogados à noite | 1–2 |
| **Bosque do Moinho** | floresta | O moinho e o canal desviado que leva à capela; lobos, bandidos | 2–3 |
| **Morro da Forca** | planície | **Opcional.** A árvore da forca antiga; pistas; bandidos | 2–3 |
| **Capela Afogada** | covil (ruínas/pântano) | Masmorra linear de três salas e a guardiã | 3–4 |
| **Estrada de Varn** | saída | Fechada até o fim; leva à segunda região | — |

```
           Morro da Forca (opcional)
                 │
Charco ─── Vau do Turvo ─── Bosque do Moinho ─── Capela Afogada
dos Juncos       │                  (canal)
           Estrada de Varn (fechada)
```

A Capela só entra no mapa depois de uma pista: o canal no Bosque, o rastro da água ou a conversa certa. Todo personagem acha o canal explorando o Bosque, então essa descoberta nunca depende de classe.

## 3. Personagens locais [proposta]

| Personagem | Quem é | Função |
|---|---|---|
| **Marta** | Irmã do herói, curandeira da vila; escreveu a carta | Motivo pessoal; está de cama com a febre; quem resgata o herói quando ele cai |
| **Irmão Caspar** | Pregador, ex-irmão da catedral; perdeu a família na febre | Culpa a "bruxa"; oferece bênção em troca de destruir a Afogada; reconhece a Odette |
| **Vó Berta** | Velha da taverna; era menina quando afogaram a mulher | Guarda o nome verdadeiro (Ilse) e a culpa da família |
| **Anselmo** | Moleiro que desviou o riacho no ano passado | Causa material; opcional |
| **Ilse, a Afogada** | Mulher afogada como bruxa na época da Primeira Fenda | Guardiã do Sigilo (a Bruxa Afogada existente com nome e história) |

Nenhum deles é antagonista puro. Caspar é sincero e está de luto. Anselmo só queria moer mais trigo. A vila errou por medo, como a turba da Yara.

## 4. Missão principal: "A Febre do Turvo" [proposta]

### Etapas

1. **Chegada.** A febre, Marta de cama, Caspar pregando no poço. Objetivo no Diário: "Descobrir de onde vem a febre."
2. **Investigar.** Em qualquer ordem: o poço, o Charco (Yara), o Bosque (canal), a taverna (Vó Berta). Encontrar o canal revela a Capela.
3. **Preparar (opcional).** Aceitar o pacto de Caspar (bênção contra a Afogada) e/ou descobrir o nome dela.
4. **Capela Afogada.** Três salas e a guardiã. A escolha final acontece aqui.
5. **Retorno.** Cena na praça, de acordo com o desfecho. Marta se recupera. Serviços mudam.
6. **Conclusão.** O Sigilo aponta para fora do vale e a Estrada de Varn abre.

### As duas soluções

| | **Destruir** | **Dar descanso** |
|---|---|---|
| Requisito | Nenhum (solução geral, sempre disponível) | Saber o nome "Ilse" (fonte sempre disponível: o registro na sacristia, sala 2) |
| Variante | Com o pacto de Caspar: a bênção enfraquece a guardiã | Com a Vó Berta junto: a guardiã para mais cedo |
| Luta | Guardiã completa, com as duas fases | Luta até a 1ª fase; ao dizer o nome, ela para e entrega o Sigilo |
| Custo | Caspar ganha força na vila; caçadores de bruxas depois | Sem bênção, enfrenta a guardiã inteira até o meio; Caspar vira inimigo |
| Etiquetas da comitiva | `purificar`, `fe` | `honestidade`, `misericordia`, `curiosidade` |

As etiquetas já existem em `comitiva/catalogo.py` [existe]. Com elas, a Odette fica dividida (gosta de fé e purificação, mas também de verdade e misericórdia), a Yara reage forte e o Morel quase não se importa.

### Fontes do nome "Ilse"

Basta uma das fontes abaixo. As outras são atalhos ou dão bônus.

| Fonte | Acesso |
|---|---|
| Registro de batismo na sacristia (sala 2) | **Geral**: todo personagem passa por ela |
| Vó Berta na taverna | Carisma, ou pagar uma bebida, ou ter a Odette presente (Berta se abre com uma irmã da Igreja) |
| Yara presente no Charco ou na Capela | Ela "ouve" o nome na água |
| Mago: eco no poço | Teste de Arcano |
| Arqueiro: nome entalhado na árvore da forca | Teste de Percepção no Morro da Forca |

## 5. A masmorra: Capela Afogada [proposta]

Masmorra **linear**: uma sequência de salas dentro do lugar, sem mapa interno. Salas vencidas ficam vencidas no save.

| Sala | Conteúdo | Reaproveita |
|---|---|---|
| 1. Nave alagada | Afogados e sanguessugas; escuridão (tochas importam) | Famílias `afogado`, `sanguessuga`; regras de luz |
| 2. Sacristia | Registro com o nome; dois cultistas com a marca do bispo (gancho da campanha) | Família `cultista`; evento com menu |
| 3. Ossuário | Esqueletos; descanso curto antes do fundo (uma vez) | Família `esqueleto` |
| Fundo | Ilse, a Bruxa Afogada; a escolha | Guardião `bruxa_afogada` com as fases |

Atalhos de classe (sempre opcionais):
- **Guerreiro:** erguer a comporta do moinho (Força) esvazia parte da nave e a sala 1 tem metade dos inimigos.
- **Arqueiro:** seguir o rastro da água (Percepção) revela uma entrada lateral que pula a sala 1.
- **Mago:** ler a inscrição do selo (Arcano) revela o que é o Sigilo antes da luta e tira um traço de resistência da guardiã.

## 6. Oportunidades das três classes fora da luta [proposta]

Cada classe tem pelo menos uma oportunidade na missão principal. Nenhuma é obrigatória.

| Classe | Oportunidade | Etapa |
|---|---|---|
| Guerreiro | Força para soltar a Yara [existe]; comporta do moinho; acalmar a turba na volta (Força/Vontade) | 2, 4, 5 |
| Arqueiro | Rastrear a água até a capela; nome na árvore da forca; caçar comida para os doentes (reputação) | 2, 3, 4 |
| Mago | Assustar a turba com magia [existe]; analisar a água do poço (prova que não é bruxaria); ler o selo | 2, 4 |

A especialização (nível 4) [existe]: a encruzilhada de cada classe dispara no descanso depois de atingir o nível. Na região ela deve acontecer perto do fim, provavelmente no acampamento depois da Capela. Proposta para a E1: não mudar as encruzilhadas agora; amarrá-las a lugares fica para a E5.

## 7. Comitiva [proposta, sobre conteúdo existente]

Limite de dois companheiros ao mesmo tempo [existe, `LIMITE = 2`]. Os três podem ser encontrados no vale; quem sobra espera no acampamento [existe]. A região acrescenta **uma cena local por companheiro, no máximo**. Os arcos em três atos continuam como estão e terminam nas regiões seguintes.

| Companheiro | Encontro (existente) | Na região | Arco pessoal depois |
|---|---|---|---|
| **Yara** | `yara_na_fogueira`: a turba no Charco | Centro do conflito: a "bruxa" de Caspar. Se for salva, ouve o nome na água. Se for queimada (opção existente), a missão continua pelas fontes gerais | Voz de Ulook e círculo negro: região 3 |
| **Odette** | `odete_na_estrada`: o moribundo na estrada | Caspar a reconhece da catedral; ela decide se encara ou foge (uma cena) | Mãe de Thomas: vila da região 2 |
| **Morel** | `morel_na_taverna`: oferta de 40 ouro | Opina na escolha (pragmatismo); pode treinar a milícia na volta | Theodore (nível ≥ 5): região 2 |

Na campanha, os encontros precisam acontecer em lugar e momento previsíveis: a Yara no Charco na primeira visita, o Morel na primeira ida à taverna. Hoje eles dependem de peso, dia e bioma sorteados. O texto e as escolhas desses eventos ficam como estão.

## 8. Recompensas [proposta]

| Origem | Recompensa | Observação |
|---|---|---|
| Guardiã (as duas soluções) | **Sigilo** e ponto de talento | Sistema existente (`chefes.py`) |
| Destruir | **Pele do Penitente** (único existente, armadura de qualquer classe) | A história "Ninguém sabe quem ela era" combina com quem nunca soube o nome |
| Destruir com pacto | Ouro de Caspar; desconto no templo | Serviço existente |
| Dar descanso | Herança da família de Berta: um raro da classe do herói (gerador existente) | Um único novo só se a primeira versão pedir; pode ser cortado |
| Dar descanso | Desconto na curandeira (Marta e Berta) | Serviço existente |
| Salas e Bosque | Saque comum e mágico; baú trancado na sacristia | Sistema existente de saque e baú |
| Contrato opcional | Caça aos lobos do Bosque no mural | Contratos existentes |

## 9. Consequências ao voltar [proposta]

| Onde | Antes | Depois de Destruir | Depois de Dar descanso |
|---|---|---|---|
| Praça | Caspar prega no poço | Fogueira com os ossos; Caspar conduz a vigília | Pedra com o nome de Ilse junto ao poço; Caspar foi embora |
| Curandeira | Fechada: "Marta está de cama" | Aberta | Aberta, com desconto |
| Templo | Normal | Bênção mais barata (Caspar agradece) | Frio com o herói (preço normal, fala seca) |
| Taverna | Rumores da febre | Canção sobre quem matou a bruxa | Vó Berta conta a história inteira |
| Mercado | Pouco estoque de provisões | Normal | Normal |
| Comitiva | — | Yara desaprova muito; Odette aprova, mas fica inquieta | Yara aprova muito; Odette aprova |
| Semente para depois | — | Caçadores de bruxas na região 2 (evento existente `cacadores_de_bruxas`) | Caspar volta como pregador do Vazio (evento existente `pregador_do_vazio`) |

"Curandeira fechada" e o motivo aparecem na vila pelo mesmo mecanismo de `predios_fechados` [existe]. As duas sementes usam `plantar`/`colher` [existe].

## 10. Conteúdo opcional (pouco)

- **Morro da Forca:** uma área curta, uma pista e um encontro.
- **O canal do moleiro:** cobrar Anselmo (Força ou Carisma) muda o estoque de provisões no mercado. Uma escolha só.
- **Contrato de caça** no mural (lobos do Bosque).
- **Eventos aleatórios existentes** nas áreas externas, filtrados por bioma e nível, como hoje.

## 11. Percurso do jogador

1. **Prólogo:** a carta da Marta ("A febre voltou. Não venha."). Chegada ao Vau do Turvo ao anoitecer.
2. **Vila:** Marta de cama, curandeira fechada, Caspar pregando. Taverna: Vó Berta e, se quiser, o Morel.
3. **Charco dos Juncos:** a fogueira da Yara. Salvar (Força, Carisma, Arcano, ouro) ou deixar.
4. **Estrada ou Bosque:** encontro com a Odette (pode acontecer em qualquer ponto depois do 2º dia).
5. **Bosque do Moinho:** o canal desviado leva à Capela. Atalhos opcionais de guerreiro e arqueiro.
6. **Opcional:** pacto com Caspar; Vó Berta; Morro da Forca; contrato; moleiro.
7. **Capela Afogada:** nave, sacristia (nome e cultistas), ossuário, Ilse. Destruir ou dar descanso.
8. **Retorno:** cena na praça conforme o desfecho; Marta melhora; serviços e falas mudam; a comitiva reage.
9. **Acampamento:** encruzilhada (nível 4) e conversas existentes.
10. **Saída:** o Sigilo aponta para Varn; a estrada abre. Fim da região.

Ritmo de nível proposto: chega no 1, cerca de 2 depois do Charco, 3 depois do Bosque, 4 na Capela. Os números serão calibrados com `tests.equilibrio` na implementação.

## 12. Sistemas reaproveitados

| Necessidade | Sistema existente |
|---|---|
| Lugares, viagem, mapa, clima, noite | Grafo do `mundo`, `sistemas/navegacao.py`, `mapa.js`, `vista.js` |
| Encontros nas áreas | Famílias de inimigos, biomas, eventos aleatórios |
| Guardiã e Sigilo | `bruxa_afogada` em `GUARDIOES`, `sistemas/chefes.py` |
| Cenas com escolhas e testes | `menu`, `teste`, `combate`, eventos |
| Reação da comitiva | `REACOES`, etiquetas, aprovação, cartões na tela |
| Consequência futura | `plantar`/`colher` |
| Estado da vila na tela | `predios_fechados`, serviços da taverna, templo e curandeira, estoque do mercado |
| Objetivo à vista | Diário e rastreador de contratos como modelo de apresentação |
| Recompensas | Únicos, gerador de raros, baú, espólio, ouro, XP, reputação |
| Derrota | `Jogo.resgate` (modo brando) [hipótese] |
| Save | `persistencia.py`, `migracoes.py` |

## 13. Extensões necessárias (mínimas, para E2 a E4)

Cada item cita onde o código atual decide a questão. Fazer só o que a região usa.

1. **Começar a campanha** (E2): hoje o início sempre gera o mundo (`jogo.py:199`) e o prólogo cita `locais[-1]` e a morte permanente (`jogo.py:212–221`). A campanha precisa de outro início e outro prólogo, sem mexer no procedural.
2. **Região como dados** (E2): locais no mesmo formato do `mundo`, com id narrativo estável e nível fixo. Hoje o nível vem do `perigo` do lugar (`mundo.py:242`). Itens a decidir:
   - onde fica o nível declarado;
   - como a Estrada de Varn fica fechada;
   - o que fazer com as convenções de vila no índice 0 e Cidadela no fim.
3. **Cenas presas a lugar e etapa** (E3): hoje os eventos são sorteados por peso e `evento_forcado` ignora o contexto (`sistemas/recompensas.py:254`). A missão precisa de uma cena que roda quando se entra no lugar X na etapa Y.
4. **Registro de missão** (E3): id, etapa, desfecho e recompensa paga, salvos no save com migração (`VERSAO_SAVE` hoje é 3). O Diário mostra o objetivo.
5. **Masmorra linear** (E3): salas em sequência dentro de um lugar, com progresso no save. Sem mapa interno.
6. **Estado da vila** (E4): falas, `predios_fechados`, preço e estoque reagindo ao desfecho.
7. **Encontros previsíveis da comitiva** (E4): os mesmos eventos, com gatilho de lugar e etapa na campanha.
8. **Resgate com quem resgata** (E4 ou E9): Marta em vez de um NPC sorteado (`jogo.py:248`).

Fora da região 1: facções, raças e origens, preparação de habilidades, transformações, pré-requisitos de talento, novas evoluções.

## 14. O que cortar se o escopo crescer

Em ordem:
1. Morro da Forca (a pista do arqueiro vai para a Capela).
2. O canal do moleiro (Anselmo vira só uma fala).
3. A cena de Caspar reconhecendo a Odette.
4. Atalhos de classe além de um por classe.
5. A variante com pacto (fica só Destruir ou Dar descanso).
6. A herança da família de Berta como item próprio (usa o gerador de raros).
7. Contrato no mural.

Não cortar:
- as duas soluções;
- a consequência visível na volta;
- o save e o carregamento no meio da missão;
- uma solução geral para cada etapa obrigatória;
- o percurso completo com as três classes.

## 15. Riscos e perguntas para a implementação

- **Tamanho:** quatro lugares e três salas já pedem várias cenas escritas. A primeira implementação pode ser só vila, Charco, Bosque e Capela.
- **Tempo:** proposta sem prazo duro para a febre. Dias passam e a vila mostra a doença, mas ninguém morre por relógio. Um prazo puniria o resgate e a exploração.
- **Yara queimada:** a missão continua. É preciso conferir que nenhuma fala posterior presume a Yara viva.
- **Dificuldade:** a Bruxa Afogada hoje entra no nível da região + 1 (`chefes.py:13`). No nível 4, com ou sem bênção, precisa de medição.
