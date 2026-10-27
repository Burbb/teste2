---
name: texto-regras-fenda
description: Escrever, revisar ou conferir o texto de regras de The Unquiet (Crônicas da Fenda): a descrição de habilidades, estados, atributos, itens e ações da luta, as dicas (tooltips) e as linhas do Grimório. Use quando uma entrega cria ou muda uma regra que aparece na tela, quando o Jean pede revisão de descrições ou de dicas, ou antes de fechar uma entrega de combate ou progressão. Não serve para narrativa, diálogos nem lore (esses seguem o critério editorial do roadmapIDEIAS/07-ETAPAS.md).
---

# Texto de regras de The Unquiet

Vale para o texto que diz **o que uma coisa faz no jogo**. A cena, a fala e o lore seguem o
[critério editorial](../../../roadmapIDEIAS/07-ETAPAS.md#critério-editorial); esta skill não as encurta.

## Três registros, três lugares

| Registro | Onde aparece | O que leva |
|---|---|---|
| **Descrição mecânica** | `desc` da habilidade (`rpg/habilidades.py`, `rpg/comitiva/luta.py`), a carta da ação na luta, a linha do menu de texto | O efeito, em quem, quanto, por quanto tempo e a condição. Uma ou duas frases. |
| **Dica de consulta** | as `linhas` do Grimório, a dica do atributo na ficha, a dica do estado na carta | A conta (escala, fórmula, valor de agora), os tetos, as exceções. Abre com o mouse ou o foco do teclado. |
| **Narrativa** | `Dizer` na luta, eventos, cenas | O que se vê e ouve. Não é a regra: não repete números da descrição. |

O custo, o recurso, o alvo e o tipo de dano já aparecem no componente (a carta: "14 de Mana · Alvo: Inimigo único ·
fogo"). A descrição não os repete, salvo quando o alvo é parte da frase ("a todos os inimigos").

## Critérios

- Responder direto: **o que faz, em quem, em que condição**. Verbo concreto no começo ("Causa", "Aplica", "Consome",
  "Reduz", "Cura"), na 3ª pessoa do indicativo.
- Frases curtas. Sem introdução, sem autoelogio ("poderoso", "devastador", "o golpe mais caro"), sem conselho de
  estratégia ("ideal para…", "use quando…").
- Manter os números de decisão: porcentagem do atributo que escala, chance, duração, camadas, teto, condição.
- Distinguir: **dano imediato** ("Causa"), **dano periódico** ("por turno do alvo"), **aplicar** um estado,
  **acumular** camadas ("até 3 camadas") e **consumir** ("Consome a Queimadura").
- Duração sempre com o dono do turno: "por 2 turnos seus", "por 3 turnos dele (do alvo)". O estado conta no começo do
  turno de quem o carrega.
- Sabor fica fora da regra: a frase de cena vai no `Dizer`, não na `desc`.

## Resumo à vista, conta na consulta (1.211.1)

Cada página e cada dica em três camadas, sem misturar:
- **descrição principal**: o efeito e o alvo (a `desc`);
- **resumo numérico**: o dano de agora (a faixa), o custo, a duração e as camadas que importam para escolher, e a
  restrição que muda a escolha ("não pode ser esquivado", uma vez, no resumo);
- **detalhes de cálculo**: a fórmula, o crítico, o ganho por ponto, os talentos e as exceções, na consulta "Como é
  calculado" (abre por clique e teclado). No código: `_efeito(texto, detalhe=...)`; a fórmula entre parênteses com
  "×" sai sozinha do resumo e vai para o detalhe; `golpe(..., sem_esquiva=True)` no lugar da nota repetida.

Na dica de um atributo, primeiro o que ele dá agora (com o valor), depois o que cada ponto rende, por fim o teste do
d20. Conceito derivado (Tenacidade, crítico) tem a explicação própria, num elemento com a dica dele.

**Mesmo nome, números diferentes (1.213.0).** Quando um atributo e o valor que ele alimenta têm o mesmo nome (AGI e a
Agilidade de luta), a dica diz qual é qual e mostra o caminho de um ao outro: base, modificadores, total. Nada de
"Agora:" como rótulo; o benefício aparece uma vez, com o número.

| Antes | Depois |
|---|---|
| AGI 4: "Agora: Agilidade 3 (3,6% de esquiva)." / "Cada ponto: +1 de Agilidade (esquiva, ordem dos turnos e fuga)." | "Soma 4 à Agilidade (+1 por ponto). Com equipamento +1 e ferimentos e fome −37%, a Agilidade de luta é 3." |
| Agilidade 3 (painel): "Abaixo do normal: Perna torcida −30%, ... (sem isso, 5)." / "Vem do atributo Agilidade (+1 por ponto) e do nível." | "Ferimentos e fome: Perna torcida −30%, Mordida dilacerada −10% → 3 na luta." / "Esquiva: 3,6% de chance por golpe (...)" / "De onde vem: atributo Agilidade 4 + equipamento 1 = 5." |

Os números vêm da mesma conta do motor (`web/estado.composicao`: `Jogador.totais` e as penalidades), nunca de uma
conta paralela na tela.

Nada de condição vaga: "resiste muito" vira a regra de verdade ("a resistência do alvo ao fogo reduz o dano por
turno"; "só quem é imune ao fogo não pega fogo"). Se a regra do código for a vaga, conserte a regra, não o texto.

## Telas de serviço: dado, não narração (forja, 10/2026)

Numa janela de serviço (reforçar, desmontar, e depois encantar), o texto é **rótulo e número**, não frase. A tela já
mostra a peça, o dono e o resultado; o texto só nomeia o que cada número é e diz o que falta.

| Situação | Assim | Não assim |
|---|---|---|
| Reforço de agora e o próximo | "+1 → +2" | "Reforço +1 de 4; o próximo leva a +2." |
| Ganho | "Ataque 4 → 5" | "+1 Ataque (o Golpe passa de 8 para 8,7)" na ação |
| Custo | ícone · "Ouro · Custo 50 · Tem 355" (cada número com o seu rótulo) | "50 (tem 355)", "50 / 355" (qual é qual?) |
| Falta | "Faltam 2 Fragmentos", "Falta 1 Fragmento" | "Falta 2 Fragmentos de Têmpera para este reforço. Consiga mais em baús." |
| Desmontar | nome da peça · "Recebe 1 Fragmento de Têmpera" · "Destrói a peça." · Confirmar | "A peça some. No mercado, ela vende por 12 de ouro." |
| Venda | "Venda: [moeda] 56", secundário | "venda no mercado" (recomendação) |
| Serviço que não existe | não aparece | um cartão apagado "Encantar: as regras estão em conversa" |
| Sem efeito possível | "Anéis e amuletos não recebem reforço." | a justificativa de design ("valem pelos afixos") |

- Observação de protótipo (o que é teste, o que é provisório) mora na faixa da demonstração ou na documentação, nunca na
  tela do jogador. Medição de teste (o dano contra um alvo fixo) fica numa área fechada e marcada "teste".
- O botão diz a ação ("Reforçar", "Desmontar", "Confirmar"); o motivo do bloqueio fica ao lado, numa linha.
- Nada de fala de personagem para explicar regra (o ferreiro não justifica o sistema).
- As propriedades da peça continuam inteiras na ficha: limpar a escrita não esconde dado necessário à escolha.

## Critérios gerais para telas de sistema (forja, 27/10/2026)

Valem para todo sistema novo com quantidades, custos e regras na tela (forja, encantamento, desmontagem, e os que
vierem). São critérios, não uma lista de palavras proibidas: a mesma palavra pode servir numa frase e sobrar numa
legenda solta.

- **Quantidade de um item ou material:** o nome (ou o ícone) e `×N`, juntos e na mesma linha: "Brasa ×2",
  "Fragmento de Têmpera ×3". Não uma linha avulsa embaixo ("Tem 2"): ela separa o número do que ele conta.
  "Tem" continua válido numa frase ou ao lado do custo ("Custo 35 · Tem 360").
- **Custo:** o recurso e o número junto da ação que gasta (o ícone e "30" ao lado do Gravar), não num parágrafo.
- **Descrição de efeito:** o efeito, a condição e o limite, nessa ordem; o limite numa linha própria quando existe
  ("Ao abater um inimigo, recupera 25% do recurso máximo." / "Até 2 vezes por luta.").
- **Sem repetir o que a tela já mostra:** se o encaixe mostra a essência que entra, o nome aparece uma vez (no bloco da
  regra), não também numa legenda do lado; se o botão está indisponível, o motivo aparece uma vez, junto dele.
- **Mesmos termos e formatos em todas as telas:** a mesma coisa com o mesmo nome e o mesmo formato na forja, no
  Inventário, nas dicas e no mercado ("Sulcos" e os mesmos encaixes; "Brasa" com a mesma cor e o mesmo texto).
- **Alinhamento:** regra em texto corrido alinhada à esquerda, num bloco de largura controlada (uma linha muito larga e
  centrada vira legenda solta). Títulos e resultados curtos ("GRAVADO", "+3", "Sai Brasa · Entra Carrasco") podem ser
  centralizados.
- **Títulos de seção, não rótulos colados:** uma seção "Encantamentos" com o nome de cada essência como título e o
  efeito embaixo, em vez de "Gravação" grudado no nome ("GravaçãoCarrasco").
- **O motivo de indisponível à vista:** junto da ação, sem depender do mouse ("Incompatível com peitorais", "Falta 1
  Essência de Eco"). A dica pode repetir; não pode ser o único lugar.
- **Compatibilidade:** na dica do material ou do item, a lista do que aceita, em plural e com "e" no fim:
  "Compatível com: armas, focos e escudos". Junto da ação bloqueada, o caso específico da peça escolhida, sem ponto
  final: "Incompatível com peitorais". Não a regra inteira do lado do botão ("Geada grava em peito."), nem a lista
  geral no lugar do motivo.
- **Troca que apaga algo:** dizer o que sai e o que entra antes de confirmar ("Sai Brasa · Entra Carrasco" /
  "Brasa se perde."), sem aviso repetido pelo resto da janela.

| Antes | Depois |
|---|---|
| Dica: "Brasa" / (regra) / "Tem 2" numa linha à parte | "Brasa ×2" no título; a regra embaixo |
| Regra centralizada numa linha larga, com uma segunda linha curta | Bloco à esquerda: **Brasa** / efeito / limite |
| Ficha: "GravaçãoCarrasco" + texto | Seção "Encantamentos": "Carrasco" (título) / efeito |
| "Substituir Brasa por Carrasco?" + "A gravação Brasa se perde." | "Sai Brasa · Entra Carrasco" / "Brasa se perde." |
| Dica: "Grava em arma, foco, escudo."; motivo: "Geada grava em peito." | Dica: "Compatível com: armas, focos e escudos"; motivo: "Incompatível com peitorais" |

## Fichas de item: leitura rápida, completa (forja, 28/10/2026)

A ficha de um item é lida em segundos (comparar, escolher) e consultada às vezes (como funciona). As duas coisas não
disputam o mesmo espaço.

- **Ordem:** o nome do item é o título. Tipo e raridade vêm numa linha secundária. Atributos e afixos ficam um por
  linha, curtos. Depois vêm os sulcos e as gravações, e por fim o resto (venda, lore).
- **Sulcos legíveis, vazios também:** os encaixes na quantidade real da peça, e os nomes das gravações com o tier numa
  linha só ("Brasa II · Brasa I · Carrasco I").
- **Uma linha por efeito, não um bloco por gravação:** o nome do efeito com o nível, em negrito do corpo do texto (nada
  de fonte de título), seguido do resumo mecânico e do limite em tom secundário. Essências repetidas somam num efeito
  só: "Brasa 3", e não três blocos de Brasa.
- **Contribuição × total:** numa peça vestida, o nível é o total de quem veste, com a parte desta peça entre
  parênteses quando difere ("Eco 5 … (5 desta peça · 7 em Odette, teto 5)"). Na bolsa, o que a peça dá sozinha. O
  nível que a peça fornece nunca se confunde com o nível do personagem.
- **O que decide fica à vista:** o gatilho, o número, o limite e a condição estão no resumo ("Ao abater um inimigo,
  recupera 15% do recurso máximo. Até 2 vezes por luta."). Vai para os detalhes o que explica o termo ou a conta: o
  alvo, as interações, "não vale nos tiques".
- **Detalhes por clique e teclado:** um "Como funcionam" que abre com Enter, nunca só com o mouse em cima. Nas dicas,
  que somem, os detalhes não aparecem; a ficha do Inventário, a forja e o achado os têm.
- **Comparação separada:** o que muda ao trocar é um bloco próprio (o jogo já faz), não misturado às linhas da peça.
- **Números do motor:** os textos de cada nível saem da tabela implementada (`encanto.texto`). Mudou a tabela, mudou
  o texto; nada de número copiado de uma rodada antiga.

| Antes | Depois |
|---|---|
| "Eco" (título grande) / "Ao abater um inimigo, recupera 25% do recurso máximo." / "Até 2 vezes por luta." (bloco de três linhas por gravação) | "Eco 1 Ao abater um inimigo, recupera 15% do recurso máximo. Até 2 vezes por luta." (uma linha; o número é o da tabela do nível 1) |
| Duas gravações de Revide: dois blocos iguais | "Revide 5 Ao receber um golpe corpo a corpo, 35% de chance de revidar com 60% do Ataque. No máximo 2 vezes por rodada. (3 desta peça · 6 em Morel, teto 5)" |
| "No máximo 1 vez por turno seu." (a regra contava a rodada) | "No máximo 1 vez por rodada." |

**Referências examinadas (28/10/2026):**
- **Last Epoch:** a captura da prévia da ficha 0.7.1 (fórum oficial, "Social_Tooltip_1"). Nome em destaque, tipo menor
  embaixo, um afixo por faixa curta; os detalhes atrás de ALT/CTRL, com os botões visíveis na própria ficha; a
  comparação ("Stat changes if equipped") num bloco separado, em verde e vermelho.
- **Path of Exile:** a ficha da Mageblood (poewiki). Nome e base em duas linhas, filetes separando o implícito dos
  afixos, cada afixo uma frase mecânica numa linha, o texto de sabor por último, em itálico.
- **Grim Dawn:** as notas da versão 1.2.1.0, citadas pelo designer no fórum oficial. A ficha passou a esconder por
  padrão o detalhe de componentes, aprimoramentos e habilidades (Ctrl mostra), com uma opção de ficha detalhada, para
  reduzir o inchaço.
- **Diablo IV:** só o texto das notas da temporada "Loot Reborn" (menos afixos, mais claros). As capturas não foram
  examinadas: o post oficial pedia data de nascimento, e a cópia da Icy Veins estava atrás de uma checagem da
  Cloudflare.

## Vocabulário (etapa 4)

- **turno** (ou **vez**): a ação de um combatente na ordem. **Rodada**: todos agiram (inclusive quem perdeu a vez).
  Nunca "turno" no sentido de rodada.
- **dano físico / mágico**: mágico é todo golpe que não é físico (fogo, gelo, arcano, sagrado, sombra).
- **Tenacidade** (da Vontade): chance de resistir a atordoar, congelar e prender. **Resistência elemental** é outra
  coisa: reduz o dano de um tipo. Não misturar.
- Estados pelo nome da tela, com maiúscula quando é o nome do estado: Queimadura, Sangramento, Veneno, Fragilizado,
  Defesa quebrada. O particípio concorda com quem recebe ("Odette fica envenenada").
- **Atordoar**: perde a próxima vez (e o golpe que preparava). "Congelar" e "prender" são o mesmo estado, com outro
  rótulo; a descrição diz o efeito ("perde a próxima vez").
- **Ultimate**: o componente mostra a marca ("Ultimate · 1 vez por luta"). A descrição não começa com "Ultimate:".

## Conferir contra a regra implementada

1. Leia a definição: os blocos (`Dano(mult, stat, tipo, esquiva)`, `Aplicar(estado, turnos, valor, chance)`,
   `Acender`, `Roubo`, `Curar`) ou a função (`fn`). A `desc` não pode prometer o que o bloco não faz, nem calar o que
   ele faz (a Prece de Odette limpa males com aprovação 75 ou mais).
2. Compare com as linhas do Grimório do mesmo herói: os dois têm de dizer a mesma coisa com os mesmos termos.
   O script de conferência gera todas de uma vez (um herói de cada especialização no nível 6, `grimorio.dados`).
3. Número que muda com o herói (o que o Meditar devolve) vem de `desc_fn` ou das `linhas`: a tela não calcula.
4. Rode o jogo e leia a carta da luta e a página do Grimório na resolução do Jean.

## Fontes consultadas (outubro de 2026)

- **Slay the Spire**, tradução PT-BR (repositório `paulohauck/slaythespire-ptbr-localization`, `cards.json`):
  imperativo, com o número no lugar marcado (`!D!`, `!M!`): "Cause !D! de dano. Aplique !M! de Vulnerabilidade.";
  "Ganhe !B! de Proteção."; condição explícita: "Se o inimigo estiver Envenenado, cause !D! de dano novamente.";
  a operação dita pelo verbo: "Dobre o Veneno de um inimigo."
- **Path of Exile**, texto oficial em PT-BR (poedb.tw/pt): a frase de efeito separada das linhas de mecânica, uma por
  linha: "60% de chance de Envenenar ao Acertar"; "Duração base é de 1 segundo".
- Revisões anteriores do projeto: as dicas da 1.202.1 e 1.202.3 (vida máxima bloqueada, ferimentos, bandagem,
  achado): dizer o que reduz e quanto, e como volta.

Em comum: o efeito primeiro, um número por ideia, a condição como condição ("Se acertar,"), o detalhe da conta na
consulta. Daqui saiu a escolha do indicativo ("Causa") em vez do imperativo, para combinar com a voz das dicas que o
jogo já tem.

## Antes e depois (1.211.0)

| Antes | Depois |
|---|---|
| Descarga: "220% de dano arcano num alvo: o golpe mais caro do mago." | "Causa 220% do Poder em dano arcano." |
| Bola de Fogo: "150% de dano de fogo; costuma acender o alvo (as chamas acumulam até 3 camadas)." | "Causa 150% do Poder em dano de fogo. Se acertar, 60% de chance de aplicar 1 camada de Queimadura (até 3)." |
| Conflagração: "Ultimate: fogo em todos; as chamas de cada um explodem." | "Causa 70% do Poder em dano de fogo a todos os inimigos e consome a Queimadura de cada um, como a Combustão. Não pode ser esquivada." |
| Tiro Imobilizador: "…60% de chance de prender o alvo…" (e o Grimório dizia "atordoar") | "…Se acertar, 60% de chance de atordoar o alvo: ele perde a próxima vez e o golpe que preparava." |
| Grimório: "quebrar a defesa de o alvo (−40%) por 2 turnos dele." | "Reduz a defesa do alvo em 40% por 2 turnos dele." |
| Prece (Odette): "Cura 220% do Poder + 12% da vida máxima do aliado." | "Cura o aliado em 220% do Poder + 12% da vida máxima dele. Com a aprovação de Odette em 75 ou mais, também remove os males." |
