---
name: arte-personagens-fenda
description: Construir, revisar ou animar o corpo de um personagem em pixel art em The Unquiet (Crônicas da Fenda), sobretudo braços, ombros e mãos em ação (comer, beber, trabalhar com uma ferramenta, apoiar-se numa mesa ou balcão), em figuras de cena (a taverna, a forja, a curandeira, o templo) ou em outra figura de corpo inteiro ou meio corpo. Use quando um braço "fica estranho", encurta ou estica entre quadros, gruda no peito, some atrás de uma ombreira ou da roupa, quando uma figura nova precisa de poses-chave ou passagens, ou antes de animar um gesto que leva a mão a algum lugar, mesmo que o Jean não cite a skill. Complementa a arte-cenas-fenda (o ambiente, a atividade, quem conduz e acompanha); não serve para ícones, itens nem retratos de carta.
---

# A construção do personagem e dos membros

O mesmo defeito voltou três vezes: o braço do ferreiro (o "guidão", o ombro levantado), o dos jogadores de tabuleiro
(o braço como barra no ombro) e o de Morel na vista da taverna (a colher indo à boca com o braço que encolhia de 18 para
7 px, o cotovelo no meio do peito, a raiz do braço escondida pela ombreira, o braço de apoio como uma faixa escura só).
Cada rodada corrigiu a pose da vez; esta skill registra o **método** que resolveu o de Morel (29/10/2026), aplicado e
conferido, para não recomeçar a cada personagem. A arte-cenas-fenda continua valendo para o lugar, a atividade e a
atuação (quem conduz, acompanha e fica: seção 5b de lá); aqui fica como o corpo se constrói e se move.

Os números de Morel (os comprimentos, os 30° da câmera, os raios da manga) são do caso dele; o que se leva para outro
personagem é a ordem dos passos e o que cada um confere.

## O erro de construção (o caso de Morel, v2)

Os sintomas eram da pose; as causas, de construção:
- **Anatomia:** o ombro estava 12 px abaixo de onde deveria (y 47 em vez de 35, no fim da ombreira), então o braço de
  cima não tinha de onde sair; o cotovelo ia 23 px para dentro, até o meio do peito, o que um ombro parado não permite.
- **Escorço sem pista:** o braço passava de 18 para 7 px de um quadro para o outro sem nada dizer que ele apontava
  para quem olha (nem o cotovelo maior, nem a sobreposição).
- **Sobreposição:** braço e antebraço no mesmo tom, sem dizer qual passava na frente; a ombreira grande cobria a cabeça
  do úmero e metade do braço.
- **Roupa:** a manga era uma cápsula de um tom só, sem a dobra do cotovelo; no braço de apoio, a manga de cima (no
  corpo) e o antebraço (na mesa) tinham os mesmos valores escuros e liam como uma faixa contínua.
- **Tempo:** a mão saltava 9 a 11 px a cada 200 ms, o cotovelo também.

## As fontes consultadas (e o que cada uma deu)

Vistas de verdade (imagens, folhas, sequências), não só resumos de busca:

| Fonte | O que foi visto | O que se aproveitou |
|---|---|---|
| Slynyrd, Pixelblog 17 e 49 (anatomia humana; *41-Poses.gif*, *139-Action_Poses.gif*, *Man_Pose_Process*) | as folhas quadro a quadro: o esqueleto de linhas e juntas, o boneco por cores, a roupa por último | o boneco colorido por segmento (o braço de trás num tom mais escuro), a barra das clavículas com o ombro na ponta, os braços fora da silhueta do tronco quando possível, o antebraço na frente do peito separado só por um tom, sem contorno |
| Clip Studio, Dani Puente, *How to Draw an Arm* (os desenhos do braço esticado, dobrado e girado) | as proporções desenhadas e os braços dobrados | braço 5, antebraço 4, mão 3 (em 12); o cotovelo na altura da última costela; o antebraço mais cheio perto do cotovelo; erguer o braço levanta a clavícula e move a escápula |
| Proko, os ossos do ombro | os desenhos da cintura escapular | a clavícula é a única ligação do braço com o tronco: o ombro sobe e avança quando a mão vai para cima e para a frente |
| Rubenstein, o braço | as proporções e o deltoide | o deltoide é um triângulo por cima da junta; o braço de cima é mais longo que o antebraço |
| Animation Mentor, Gleb Sitnichenko, *How to Animate Believable Eating Motions* | o texto da aula (o vídeo não abriu) | os estágios do gesto: pegar, levar, "a cabeça vai ao encontro da mão", a pausa curta antes da boca, mastigar com a cabeça e o tronco participando |
| Estudo de Kobe sobre levar a colher à boca (biomecânica) | o resumo e as medidas | perto da boca, o ombro abre (o cotovelo vai para fora) e o cotovelo dobra mais; depois, o inverso |
| Mark Rothko, *Seated Figure with Elbows on Table* (National Gallery of Art) | o desenho | sentado à mesa, o cotovelo fica embaixo, o antebraço sobe quase vertical até o queixo e a cabeça desce |

## O método (11 passos, nesta ordem)

1. **O gesto e o que fica.** Uma frase do gesto ("tira uma colherada, leva à boca, mastiga com a mão pousada") e os
   apoios: o quadril no assento, o braço de apoio no tampo, a tigela no lugar. O que fica parado é decisão.
2. **Proporções pela cabeça, na grade.** Meça a cabeça na grade (Morel: 21 px) e tire dela o resto: o ombro (a cabeça
   do úmero) uns 4 px abaixo do alto do ombro, a largura dos ombros, o braço de cima (Morel: 28 px), o antebraço (22),
   do pulso à ponta da ferramenta (12). Sentado à mesa, o braço caído leva o cotovelo à altura do tampo: confira isso
   antes de qualquer pose (se não bate, a mesa ou o banco estão na altura errada).
3. **O estudo de construção no Aseprite, com formas simples.** Uma fonte à parte com a cabeça, o pescoço, a caixa
   torácica (um ovo), as clavículas e as cabeças dos úmeros, os braços em cápsulas de cores diferentes (o de cima, o
   antebraço, a mão; o braço do fundo num tom mais escuro), o plano da mesa e o objeto. Numa camada `guia`, os ossos em
   linha e as juntas em cruz. Uma pose-chave por quadro, com o nome na etiqueta. Nada de textura, roupa ou equipamento.
4. **Comprimento físico fixo, comprimento na tela livre.** As poses-chave dizem onde ficam o ombro, o pulso e a ponta da
   ferramenta *no espaço* (com profundidade); o cotovelo sai da cinemática inversa de dois ossos, para o lado que o
   gesto pede (o `polo`). Ninguém posiciona o cotovelo na tela à mão: é aí que ele ia parar no meio do peito. A tabela
   mostra o comprimento projetado de cada osso em cada pose: o braço de Morel tem 28 px de pé ao lado do corpo e 16 na
   boca, porque aponta para quem olha; isso é escorço, e precisa de pistas no desenho (passo 7). Ferramenta rígida: a
   colher é um vetor de comprimento fixo a partir do pulso, não uma ponta solta. Script de referência:
   `ferramentas/prototipos/taverna/morel/estudo-construcao/juntas.py`.
5. **Deixe a geometria dizer o que é possível.** Com a mão no queixo, os comprimentos de Morel não deixam o cotovelo
   descer e abrir para fora ao mesmo tempo; as saídas eram (a) aceitar o cotovelo à frente, abaixo do ombro, num V de
   uns 30°, com a mão um pouco à frente do queixo; ou (b) curvar o tronco e baixar a cabeça uns 8 px. Escolha
   conscientemente (Morel ficou com a; a cabeça desce 3 px ao encontro da colher) e registre por quê. Se nenhuma
   serve, mude a cena (a altura da mesa, a distância), não o pixel.
6. **O ombro e o tronco participam quando o gesto pede, e só o quanto pede.** Uma ação natural não exige o corpo
   inteiro: a participação vem do esforço, do alcance, dos apoios e da intenção, e as partes estáveis também fazem
   parte da atuação. Em Morel, a mão vai à boca, mais alto que o ombro: o ombro sobe e entra 1 px (a clavícula sobe e
   avança), o corpo desce 1 px para a tigela e a cabeça vai ao encontro da colher (a boca é o alvo do gesto). No
   taverneiro da G4, a mão do pano trabalha na altura das mãos, sem esforço: só o cotovelo e o ombro do pano acompanham
   (1 px) e o tronco e a cabeça ficam; olhar os fregueses é outra ação, na pausa. Na martelada do ferreiro, o esforço
   leva o corpo todo. Nunca prenda a junta do ombro embaixo de uma peça de equipamento na altura errada.
7. **Vista a figura sobre a construção, como uma roupa só.** A estrutura (as juntas, os segmentos) orienta o movimento;
   o acabamento une os segmentos. A manga é **uma forma** do ombro ao punho, não um braço e um antebraço encaixados: no
   ombro, sem calota acima da linha do ombro do tronco (o alto da manga continua a inclinação do casaco, o deltoide
   por baixo); no cotovelo, o lado de fora numa curva e o de dentro comprimido numa dobra curta, com o pixel aceso da
   crista, nunca uma quina ou um traço que divida as duas partes. **Unir não é fundir:** por dentro da dobra, quando o
   braço dobra muito, o antebraço passa na frente do bíceps e continua uma forma própria, com a luz dele e a sombra que
   faz no braço (a sobreposição); só o lado de fora vira curva; a luz de uma superfície só, o grupo de luz passando
   do braço para o antebraço pela curva. O antebraço pode ficar mais escuro, mas aos poucos e alguns pixels depois da
   junta, nunca um tom inteiro de uma vez exatamente nela. O antebraço que cruza na frente projeta sombra no braço; o
   punho da manga escuro no fim; a sombra de um pixel, do lado oposto à luz, no que está embaixo (o peito, a mesa).
   **Sem contorno escuro em volta**, e sem esconder a junta com mancha escura ou pontilhado. Equipamento não esconde a
   raiz do braço: a ombreira cobre o alto do deltoide, não metade do braço, e fecha o alto do ombro (sem couro
   aparecendo acima da placa). No braço que se move, ela é curta (uma calota que acompanha a junta do ombro em cada
   pose) e fica atrás do antebraço e da mão quando eles sobem na frente do ombro (Morel levando a colher à boca, com a
   ombreira direita que o retrato do jogo tem).
8. **Simplifique para a grade, sem perder o porte.** Três tons por material, mão em bolinha de pele (a memória "mãos de
   cena sem dedos"). Confira a grossura: a primeira aplicação em Morel saiu com braços de 9 px e ele ficou franzino; com
   11 px (ombro e manga de couro) o porte voltou.
9. **Valide as poses-chave antes das passagens.** A folha com o estudo em cima e as mesmas poses vestidas embaixo, no
   tamanho real e ampliada sem suavização. Se uma chave não lê (na primeira tentativa de Morel, braço e antebraço
   empilhados na mesma vertical na boca), volte ao passo 4 ou 5 antes de desenhar uma passagem.
10. **Passagens interpoladas no espaço, medidas na tela.** As passagens saem das chaves no espaço (o cotovelo
    recalculado em cada uma), com facilidade nas pontas (mais perto da chave na saída e na chegada). Meça quanto a mão,
    o cotovelo e a ponta da ferramenta andam de um desenho para o seguinte (Morel: até 6 px na mão e no cotovelo; a
    ponta da colher até 10, porque gira) e o corpo (até 1 px). O tempo segue o das cenas aprovadas (a curandeira, o
    balcão): as poses das pontas seguram 2 tiques, as passagens do meio 1, a pose de contato mais (a boca, 6); nada de
    um tique em todos os desenhos (lê como vídeo). Confira as trajetórias numa folha (o cotovelo, o pulso, a ponta da
    ferramenta, um ponto por pose, antes e depois) e a emenda do fim com o começo.
11. **Avalie no jogo, no tamanho real.** A cena correndo, nas duas resoluções, a pose parada do movimento reduzido, os
    contatos (a colher entra na boca e no caldo sem atravessar a barba, a roupa nem a mesa) e o que a arte-cenas-fenda
    pede da conferência (pontos, teclado, Esc, console, relógios). Separe a conferência técnica (medidas, passos,
    contatos) da avaliação artística (lê como um homem comendo?), que é do Jean.

## Os exemplos desta rodada

- [morel-antes-depois.png](exemplos/morel-antes-depois.png): a v2 e a atual, na boca e descansando. **Problema:** na v2,
  o braço da colher sai de baixo da ombreira, o cotovelo vai ao peito e o antebraço sobe de lá para fora; descansando,
  o braço de apoio é uma faixa escura do ombro à mesa. **Solução:** o ombro no lugar, o braço em escorço com o cotovelo
  logo abaixo dele e o antebraço indo para dentro, até o queixo; o braço de apoio em três partes (a ombreira por cima,
  o braço caído, o antebraço deitado num tom mais escuro que o tampo).
- [morel-construcao.png](exemplos/morel-construcao.png): em cima, as cinco poses-chave do estudo (recolher, levantar,
  boca, retornar, repousar) com as juntas; embaixo, as mesmas vestidas na vista. **Problema:** a v2 foi desenhada
  direto na roupa, pose a pose. **Solução:** as chaves conferidas nas formas simples e só então vestidas.
- [morel-trajetorias.png](exemplos/morel-trajetorias.png): uma volta da colher, à esquerda a v2, à direita a atual (o
  cotovelo em verde, o pulso em azul, a ponta da colher em amarelo). **Problema:** na v2 o cotovelo atravessa em linha
  reta até o meio do peito e a mão sobe em 4 saltos. **Solução:** o cotovelo faz uma curva curta para a frente e volta;
  a mão sobe num arco em passos de até 6 px.

As fontes do caso: `ferramentas/prototipos/taverna/morel/estudo-construcao/` (o estudo `morel-construcao.aseprite`,
`juntas.py` e `vestir.lua`, que refaz o braço vestido da fonte pixel a pixel) e `morel/vista/morel-vista.aseprite`
(as juntas de cada quadro na camada `guia`, um pixel de cor por junta).

## O estudo de construção e o acabamento são etapas diferentes

O **estudo de construção** verifica o que não se vê de longe: o apoio, o alcance, os comprimentos, as articulações, o
espaço do movimento, as sobreposições pela profundidade. Ele pode (e deve) ser calculado: juntas pela cinemática,
volumes simples com profundidade, cores lisas por parte. O **acabamento** traduz essa construção para a linguagem do
jogo, e não é a construção iluminada. Na queda de braço (30/10/2026), os volumes do estudo com a luz em degraus e um
pontilhado por cima foram recusados pelo Jean: pareciam um modelo 3D simplificado em baixa resolução (os braços como
tubos facetados com faixas regulares de luz, o peito um bloco com o vermelho aplicado como placa, a ombreira
arredondada sem a forma da cena aprovada, as articulações do boneco à mostra, o pontilhado igual em áreas grandes).
Por isso:
- a construção fica na fonte como **guia oculta** (camadas `guia`, fora da exportação), e o acabamento é **desenhado por
  cima**: silhuetas, mangas, dobras, sobreposições e grupos de luz escolhidos, com a cena aprovada ao lado (a folha de
  comparação lado a lado);
- da cena aprovada vêm a construção e o material da roupa (o couro em dois ou três tons em blocos, a aresta acesa do
  lado da luz; o colete sobre o corpo, a borda clara, a costura, as tiras que acompanham o peito), a forma dos acessórios
  (a ombreira em cunha, estreita e escura), a relação entre os braços, os ombros e o peito, o contraste, a paleta e o
  tamanho do pixel;
- textura e pontilhado são seletivos (a passagem da luz, um material que pede), não um filtro sobre tudo; e também não
  se chapa tudo: o detalhe é escolhido, os volumes continuam legíveis;
- mãos de cena simples (bolinhas ou formas sem dedos): numa pega, duas formas distinguíveis pela silhueta, pela
  sobreposição nos dois sentidos e pelo tom; o polegar, se preciso, numa indicação mínima.
A tentativa feita assim (`morel/queda3/`, a pose central) está **em avaliação**; não é exemplo resolvido.

### Uma articulação certa que ainda parece mecânica (Morel comendo, 30/10/2026)

A construção do braço de Morel (o ombro no lugar, o cotovelo pela cinemática, os comprimentos, o alcance da colher)
estava aprovada, e mesmo assim o Jean marcou o ombro como uma peça encaixada e o cotovelo como uma dobradiça. A causa
estava no acabamento, não na anatomia nem em guia exportada: o `vestir.lua` vestia o braço como duas cápsulas, cada uma
com faixas de luz paralelas às bordas; a do braço terminava numa calota redonda acima do ombro do tronco (uma forma
reta, sem braço), e o antebraço inteiro descia um tom de uma vez, na junta, com o vinco como um traço entre os dois.
**Uma articulação anatomicamente coerente pode parecer mecânica pela silhueta ou pela luz.**

O que foi feito (`morel/vista/manga.py`, aplicado às 20 poses; em avaliação pelo Jean): as mesmas juntas e os mesmos
raios; as duas cápsulas unidas numa forma só (uma união suave: o cotovelo de fora vira curva, o de dentro se fecha); o
alto da manga, fora do tronco, só até a linha do ombro (4 px acima da junta, descendo para fora); a luz pela distância
à borda da forma unida, em três tons e o realce só nos pontos mais acesos; o antebraço escurecendo meio tom, a partir de
3 px depois da junta; por dentro da dobra, o antebraço por cima do braço como forma própria, com a sombra dele no braço
(a primeira aplicação unia também por dentro, e nas poses de braço bem dobrado o antebraço sumiu no bíceps: o Jean
marcou "o antebraço esmagado, virando uma coisa só com o bíceps"); uma dobra de dois pixels por dentro do cotovelo, com o pixel aceso da crista (com três, perto da
boca, lia como um corte); a mão e a colher de antes, intactas (os contatos aprovados). O método, na ordem: (1) achar a
causa na fonte e na geração das poses; (2) resolver três poses-chave (a colher na tigela, subindo, na boca), paradas e
em sequência, antes e depois lado a lado; (3) aplicar ao ciclo inteiro e conferir **cada pose sozinha e na
sequência** (espessura que muda, luz que pisca ou desliza, marca que salta, contato perdido), inclusive as poses que
outra ação reaproveita (a reação ao pagamento); (4) gravar na fonte com os retoques numa lista no próprio script, para
uma regeneração não apagar as correções. A versão anterior fica no painel, no mesmo estado, para comparar.

O estudo de construção (o apoio, o alcance, as juntas) e a aprovação artística (a roupa, a silhueta, a luz) são
verificações diferentes: passar na primeira não diz nada da segunda. E isto não proíbe a automação: o cálculo continuou
gerando a manga; o que mudou foi o que ele desenha e a revisão antes de virar a arte.

## Dois corpos ligados por um contato (a queda de braço, 30/10/2026)

Quando duas figuras se seguram (uma queda de braço, um aperto de mão, puxar alguém), o contato é a junta que as duas
dividem. O caso: `ferramentas/prototipos/taverna/morel/queda2/` (`juntas.py`, `maos.py`, `estudo.py`, `poses.py`). A
primeira tentativa (`morel/queda/`, na câmera da conversa) não resolveu: a ação pequena, as mãos numa massa só, os
desfechos indo para perto e para longe da câmera. Ela fica como histórico, não como exemplo.

**O que o estudo demonstrou** (as poses estão em avaliação pelo Jean; o método vale para a construção):
- **A regra real decide o movimento, e o movimento decide a câmera.** Pela mesa e pelas regras da WAF, os cotovelos
  ficam quase alinhados (cerca de 38 cm um do outro, na direção de quem está sentado para quem está do outro lado), a
  pega é palma com palma, com os polegares em cima, e quem vence leva a mão do outro para a própria esquerda: os
  desfechos correm de lado. Uma câmera atrás de quem joga põe esse movimento em profundidade (escorço nos dois fins);
  ao longo da linha dos cotovelos, um antebraço esconde o outro na disputa; de lado demais, a mesa vira um losango no
  canto. Três quartos (50° do nosso lado, 30° acima) mostrou o V da disputa aberto e os dois fins para os lados do
  quadro, com o braço de quem perde deitado e comprido no tampo. Teste as câmeras em números, com esboços simples, antes
  de desenhar.
- **O contato só existe onde as duas cadeias alcançam:** com os apoios fixos (os cotovelos) e os comprimentos fixos, a
  mão comum anda num círculo; as poses-chave são pontos dele. Desenhe o círculo na guia, numa planta vista de cima (o
  espaço na mesa, o lado de cada fim, os objetos) e sobreposto à pose do meio (o quadro comporta o caminho?).
- **O que a tela põe por cima entra na composição:** o dado dos testes rola no meio do palco; a pega da disputa ficou
  no alto e à esquerda, fora dele nas duas janelas (medido: na arte, x 100 a 220 a partir de y 63 a 1920×945; x 70 a
  250 a partir de y 45 a 1280×720).
- **A pega se constrói antes de simplificar,** no mesmo espaço dos braços: os punhos (elipsoides), os dedos (cápsulas, um
  por dedo), os polegares; a nossa mão do lado dela, a dele do outro, os dedos de cada um dobrados sobre o dorso do
  outro. Nos fins, a mão de quem perde fica de dorso no tampo e passa um pouco do punho de quem vence (senão o punho de
  cima e o antebraço que vem da câmera a escondem).
- **Duas peles parecidas se separam pelo valor, não pelo contorno:** a de um mais escura e quente; um pixel de sombra da
  pele de quem está atrás onde uma parte passa atrás da outra (a mão do outro, outro dedo, o polegar por cima); os
  pontinhos que isso deixa saem numa limpeza; e o que explica a pega (os dedos dele sobre o nosso dorso, em listras,
  cada um com o lado de cima claro e o vão escuro) é retocado à mão por cima da construção. Sem isso, as duas mãos
  voltaram a ser uma massa.
- **Quem é quem até o ombro:** cor e material de cada braço (o couro dele, a lã nossa); o nosso braço sai pela borda do
  quadro na direção do ombro (o tronco fora dele), o dele chega ao peito, com o colete e a ombreira (a identidade).
- **Os objetos saem do caminho e voltam pelo mesmo caminho:** a tigela deslizada para longe dos dois fins, na mesa que a
  vista aprovada estabelece (a mesa termina perto da quina; foi a disputa que andou para oeste), e puxada de volta
  antes de comer.

**O que a avaliação já respondeu:** o volume calculado com o acabamento em degraus **não** segura a identidade de Morel
ao lado das cenas desenhadas à mão (a seção anterior); a câmera de 50° e 30° acima deixou o tampo e a parede dominarem
o quadro, e a terceira tentativa baixou a câmera (40° e 15°), aproximando a sensação da conversa. **Ainda hipótese:** se
as vitórias se reconhecem sem legenda no tamanho da HUD (elas esperam a pose central ser aprovada).

## Erros que já aconteceram

| Erro | Causa | O que fazer |
|---|---|---|
| O braço que encolhe e estica entre quadros | as juntas postas na tela pose a pose | comprimentos fixos no espaço e o cotovelo pela cinemática (passo 4) |
| O cotovelo no meio do peito | o ombro baixo demais, preso embaixo da ombreira | o ombro pela cabeça e pela clavícula (passos 2 e 6) |
| Braço e antebraço como uma peça só | o mesmo tom, sem sobreposição | o antebraço um tom abaixo, a sombra que ele projeta, o vinco do cotovelo (passo 7) |
| O braço de apoio como faixa escura | a manga e o antebraço com os mesmos valores, iguais à mesa | três partes com valores diferentes, a aresta clara e a sombra no tampo (passo 7) |
| A figura franzina depois da correção | volumes finos demais para o porte | conferir a grossura com a figura anterior (passo 8) |
| Braço e antebraço empilhados na mesma vertical | a mão perto demais do ombro, o cotovelo para dentro | escolher a solução geométrica pelo passo 5 |
| A colher que muda de tamanho | a ponta interpolada solta | a ferramenta rígida a partir do pulso (passo 4) |
| Saltos de 9 a 11 px a cada 200 ms | poucas poses, todas de 2 tiques | passagens no espaço, até ~6 px por desenho, o tempo das cenas aprovadas (passo 10) |
| O guidão do ferreiro, a barra do jogador (antes) | o alcance não medido | arte-cenas-fenda, seções 5a e 5b (o alcance decide o corpo) |
| O corpo inteiro limpando a caneca (a primeira G4) | o tronco e a cabeça movidos por regra a cada passada | a participação pelo esforço e pelo alcance (passo 6; arte-cenas-fenda, 5b) |
| As duas mãos de uma pega numa massa só (a primeira queda de braço) | tons de pele parecidos, a pega desenhada direto na escala da cena | a pega construída com formas simples e separada pelo valor (a pele de um mais escura, um pixel de sombra onde uma passa atrás da outra, os dedos em listras) |
| Os desfechos indo para perto e para longe da câmera (a primeira queda de braço) | a câmera escolhida pela cena anterior, não pelo movimento | a regra real do gesto diz para onde ele vai; a câmera é escolhida para esse movimento correr de lado |
| O acabamento parecendo um modelo 3D em baixa resolução (a segunda queda de braço) | os volumes da construção iluminados e pontilhados usados como a arte | a construção vira guia oculta; o acabamento é redesenhado por cima, pela cena aprovada (silhuetas, mangas, dobras, grupos de luz, textura só onde diz algo) |
| O ombro como peça encaixada, o cotovelo como dobradiça (Morel comendo, a terceira passada) | o braço vestido em duas cápsulas: a calota acima do ombro do tronco, o antebraço um tom abaixo exatamente na junta, as faixas de luz de cada segmento | uma manga só, sem calota, a luz contínua pela curva do cotovelo, o escurecimento depois da junta, uma dobra curta por dentro (passo 7) |
