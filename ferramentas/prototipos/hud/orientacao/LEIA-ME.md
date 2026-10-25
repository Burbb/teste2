# Os quadros de orientação do tutorial: levantamento, duas propostas e a B refinada (etapa 2, 24/10/2026; protótipo)

**Integrada na 1.207.0 (25/10/2026):** a R aprovada pelo Jean está no jogo (`06-talentos-avisos.css` e a ordem dos
botões em `app/orientacao.js`). Conferido com os mesmos roteiros: os 14 casos nas duas janelas com as medidas iguais às
da R (posição, seta, tamanho, 0 px sobre o controle) e os quadros iguais pixel a pixel (as diferenças das fotos são o
pulso do contorno, a luta correndo e, na ficha, o aviso de talento novo); `gestos.mjs` passa com o Tab na ordem da
leitura. Desde então, "hoje" nos roteiros é a R; `PROPOSTA=r` serve o jogo como está.

Os quadros de hoje continuam no jogo. As propostas são só o acabamento (`orientacao.css`, por cima das regras de
`06-talentos-avisos.css`, valendo com `html[data-orientacao="a"]`, `"b"` ou `"r"`): a posição, a seta, o contorno do controle,
os véus, a sequência, os textos e os gestos são os de `app/orientacao.js` e `rpg/abertura.py`, sem mudança. A folha
comparativa: `folha-orientacao.png` (tamanho real). A demonstração: `demo.bat`.

## O levantamento (como funcionam hoje)

**Quem decide:** o motor (`rpg/abertura.py`, `proxima` e `apresentacao`) diz qual orientação vale e o texto; a tela
(`app/orientacao.js`) acha o controle e desenha o quadro, a seta, o contorno pulsando devagar em volta do controle e um
véu leve nas colunas e na doca. Uma por vez; depois de um "Entendi", a próxima espera a cena seguinte.

| grupo | quais | o alvo (`ancora`) | onde o quadro mora | controles |
|---|---|---|---|---|
| a abertura | A0 (revelar o texto), AL (acelerar a animação) | o Continuar; nenhum (AL) | a faixa da página; na luta, a faixa abaixo da arena, sem seta | AL: Entendi; A0 passa ao seguir |
| a luta guiada | C1–C3 (Habilidades, escolher, alvo), C4 (o que a habilidade gastou), o ícone de efeito | o botão, a linha, a mira; a barra; o ícone na carta (com a haste) | a faixa reservada abaixo da arena (ou ao lado da janelinha aberta) | C1–C3 pela ação; C4 Entendi |
| a vila | V1 (o mural), V2 (o Templo ou a Taverna), V3 (provisões), V4 (Comitiva), V5 (Explorar) | o prédio; as provisões no topo; a doca; a opção do menu | os prédios: a faixa abaixo do cenário; o topo: logo abaixo; a doca e o menu: a faixa de baixo | V3, V4: Entendi; os outros pela ação |
| os contratos | K1 (aceitar), K2 (o aceito), K3 (a opção do contrato), K4 (cumprido) | o cartaz do Mural; o cartão na coluna da direita; a opção | acima do cartaz; dentro da coluna, acima ou abaixo do cartão | K2, K4: Entendi |
| o resto | E1 (o achado), T1 (Talentos), N1 (a noite), B1 (o baú), A1 (a velocidade do texto) | a janela do achado; a doca; os riscos do lugar; o baú na bolsa; o botão Texto no topo | abaixo da janela; a faixa de baixo; dentro da coluna; logo abaixo do topo | T1, N1, A1: Entendi |
| feridas e fogueira | F1–F4 (o ferimento, a bandagem, a Curandeira), D1–D3 (dormir) | a bolsa, o ferimento, o serviço, o dormir da fogueira | encostado no controle | D1, D3: Entendi |

- **Os controles:** "Entendi" (nas informativas) fecha só o quadro e marca a orientação como vista; Enter e espaço
  nele não escolhem nada no jogo. "Encerrar tutorial" desliga todas (a Ajuda, F1, religa). O clique e o toque no
  quadro são dele (não adiantam texto nem escolhem ação).
- **Reaparecer:** as que se cumprem pela ação continuam até a ação; as informativas não voltam depois do "Entendi" (o
  motor confirma no próximo estado); o AL volta na próxima luta se a luta acabou com ele à vista.
- **Os casos da comparação** (`auxiliares/cenarios_orientacao.py`, pelo cenário `tutorial` dos testes, com estado
  temporário): A1 (no alto), B1 (lateral esquerda, curto), K2 e N1 (lateral direita, o N1 longo), V2 (na página), V4
  e T1 (embaixo, a doca), E1 (abaixo da janela do achado), AL (na luta, sem seta). O V1 e a luta guiada (C1–C4) não
  entram: o cenário `tutorial` já parte com eles vistos.

## As duas propostas

**A · o quadro da HUD.** Uma caixa compacta na face de ferro aprovada (o mesmo cinza dos botões, o fio claro em cima),
um aro de 1 px de latão escuro e a sombra dura, sem moldura grossa. O "Entendi" é o botão da HUD (a família do
Continuar, menor: a face de ferro e o aro de latão, acende no foco); "Encerrar tutorial" é o secundário, em texto,
à esquerda. A seta e a haste em latão. O texto de 15 para 16 px.

**B · a chamada contextual.** Mais leve: a base escura sem aro e uma barra de latão do lado de onde está o controle
(a ligação visual com ele), com a seta cheia da mesma cor, maior que a de hoje, encostando no controle. O "Entendi"
continua um botão dourado (a chamada é interativa, não uma dica de mouse); "Encerrar tutorial" em texto, à esquerda.
O texto de 15 para 16 px.

Nas duas: os atalhos e os nomes em destaque (o negrito do motor, em latão claro ou ouro); o foco com um contorno de 2
px; o contorno do controle mais firme (2 px), com o pulso devagar de hoje; nenhuma animação nova e nenhuma espera.

## Conferido (no jogo de verdade, `auxiliares/`)

- `fotografar.mjs`: os nove casos nas três versões (hoje, A, B), a 1920×945 e a 1280×720, com o mesmo estado: o
  quadro dentro da janela em todos e cobrindo 0 px do controle explicado em todos (`capturas/medidas.json`). As
  fotos completas saem de novo pelo roteiro (a pasta guarda só as medidas; a folha, os recortes em tamanho real).
- `gestos.mjs`, nas três: um clique no texto do quadro não escolhe nada; o Tab chega ao "Entendi" e ao "Encerrar
  tutorial", com o foco visível; Enter no "Entendi" fecha só o quadro (o menu continua o mesmo); "Encerrar
  tutorial" faz o quadro sumir sem escolher nada.

## A avaliação (recomendação: B)

- **B** — o ganho: a ligação com o controle é a mais clara (a barra e a seta douradas do lado dele), a base é leve
  para uma instrução curta, e o "Entendi" dourado é a ação principal sem dúvida. A limitação: perto de outros
  elementos dourados (o contorno do controle, os cartões acesos da coluna), a barra pode somar dourado demais numa
  coluna cheia (o N1 e o K2).
- **A** — o ganho: é a mais "da casa" (a face de ferro e o botão da família do Continuar). A limitação: numa coluna de
  ferro, o quadro de ferro se parece com o resto da coluna e se destaca menos; a ligação com o controle fica só na
  seta.

## Registrado à parte (não mexido)

- A ordem do Tab segue o código (o "Entendi" primeiro), enquanto na tela, nas duas propostas, o "Encerrar tutorial"
  fica à esquerda: a leitura e o Tab andam em sentidos contrários (hoje acontece o mesmo, com o "Entendi" à direita).
  Resolvido na R (segunda rodada, abaixo).
- A 1280×720, o N1 de hoje abre acima da coluna e cobre o nome do lugar; nas propostas (um pouco mais altas) ele
  desce para baixo dos riscos. É o posicionamento de sempre escolhendo pelo espaço, não um defeito novo.

## Segunda rodada: a B refinada (R), a candidata

O Jean escolheu a direção B e pediu uma candidata só, refinada, comparada com a B original no mesmo cenário. A A fica
como histórico (as regras dela seguem no `orientacao.css`; a folha da primeira rodada, no histórico do git).

**R · o que muda da B.** A composição leve fica (uma base escura, sem caixa de ferro, a ligação do lado do controle). O
acabamento vem para a linguagem aprovada:
- o fundo escuro com o fio de cima (o do ferro dos botões, sem a face de ferro) e a borda preta de 1 px;
- o ouro envelhecido (`#b8913f`) só onde aponta: a seta, um traço curto (2 × 26 px) junto dela, dentro da borda, a
  haste e o contorno do controle; a barra inteira da B saiu (somava dourado demais numa coluna cheia, o N1 e o K2);
- os nomes em destaque em ouro claro envelhecido;
- o "Entendi" é o botão principal da HUD (a família do Continuar, menor: a face de ferro, a aresta de latão, acende
  com o mouse e o foco) no lugar do botão dourado chapado;
- o "Encerrar tutorial", texto sublinhado à esquerda, **vem antes no código**: a ordem do Tab segue a leitura (na
  integração, a troca da ordem em `botoes()` de `app/orientacao.js`; no protótipo, o cenário serve o arquivo com a
  troca). No C4, o foco continua indo sozinho para o "Entendi"; o Shift+Tab volta ao "Encerrar tutorial".
Textos, gatilhos, sequência, posição e o pulso do contorno: os de hoje.

**Os casos que faltavam.** O V1 (o mural) e a luta guiada (C1–C4) entram pelo cenário `tutorial` com
`JA_VISTAS` (as orientações com que ele parte; `tests/navegador/cenarios.py`), numa partida de teste com saves
temporários; o C2–C4 avançam pela ação (`fotografar.mjs`, `PASSOS`; `gestos.mjs` faz o mesmo caminho até o C4).

**Conferido.** `fotografar.mjs`: os 14 casos (A1, V1, V2, B1, K2, V4, T1, N1, AL, E1, C1–C4) em hoje, B e R, a 1920×945
e a 1280×720: o quadro dentro da janela em todos e cobrindo 0 px do controle explicado em todos (depois da correção
abaixo). `gestos.mjs` (hoje, B, R): o clique no quadro não escolhe nada; o Tab chega aos dois botões, com o foco
visível; Enter no "Entendi" fecha só o quadro; "Encerrar tutorial" some sem escolher nada; no C4 o foco já está no
"Entendi". Só na R a ordem do Tab segue a leitura (hoje e na B, o "Entendi" vem primeiro e fica à direita). A folha:
`folha-orientacao.png` (hoje × B × R).

**Corrigido no jogo (defeito demonstrado nesta rodada).** No C2 (escolher a habilidade), a janelinha de Habilidades é
larga demais para o quadro caber de qualquer lado; empurrado para dentro da faixa, ele cobria a parte de baixo da linha
explicada (cerca de 20 px, nos de hoje e nas propostas, nas duas janelas). Agora, sem lado com espaço, o quadro desce
para logo abaixo da linha, com a seta para ela (`app/orientacao.js`).

**Avaliação.** O ganho: a mesma leitura imediata da B, sem a barra que somava dourado, e um "Entendi" que é visivelmente
o botão do jogo. A limitação: com o ouro só na seta, a ligação com o controle depende mais dela; nos quadros de seta
longa até o alvo (o C1, o C3), a seta é o único ponto dourado, como hoje.
