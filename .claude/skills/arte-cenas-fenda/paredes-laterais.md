# Estudo: paredes laterais e cantos (o canto de Morel, 30/10/2026)

Material de apoio da seção "Paredes laterais e cantos" do [SKILL.md](SKILL.md). As medidas (o horizonte em y 22, o ponto
em x 170, o canto em x 95) são da cena de Morel; o que vale para outra cena é a ordem e as conferências.

## As fontes vistas (e o que cada uma deu)

| Fonte | O que foi visto | O que se aproveitou |
|---|---|---|
| Proko, *Project: Build a 1-Point Room* (as notas da aula) | o quarto como uma caixa vista por dentro | o horizonte é a altura dos olhos; as arestas que correm em profundidade vão ao ponto de fuga; desenhar as arestas de trás e os cantos "por transparência" para acertar a perspectiva; as verticais se aproximam conforme recuam |
| Guias de perspectiva de um ponto para interiores (Art Projects for Kids, Art in Context) | os passos da sala em um ponto | o que está acima e abaixo do horizonte vai para o mesmo ponto; as paredes laterais saem dos cantos da parede do fundo na direção do ponto |
| Captura do Gwent em *The Witcher 3* (a referência de ponto de vista; imagem 3D, perspectiva correta) | o tampo, as tábuas e o fundo, numa câmera de quem está sentado | as tábuas do tampo convergem para um ponto atrás do adversário, na altura dos olhos; as prateleiras e tábuas do fundo acima do olho descem em direção a esse ponto |
| A imagem gerada "Encontro com Morel na taverna" | a parede da esquerda | as fiadas dela descem para o canto também abaixo do olho (como se o horizonte estivesse abaixo do tampo), o que contradiz o tampo visto de cima: ela não prova a perspectiva, só a composição |

## O que estava errado na primeira candidata

A parede da esquerda tinha um ponto de fuga próprio, longe (x 600), escolhido para as fiadas ficarem suaves como na
imagem gerada: um "pano em ângulo". Com isso, as fiadas e as vigas quase horizontais, de alturas iguais da esquerda ao
canto, liam como outro plano de frente, uma parede frontal com textura inclinada. E o tampo continuava até a borda da
esquerda, passando do ponto em que a parede está naquela profundidade (a mesa entrava na parede).

## A construção (`ferramentas/prototipos/taverna/morel/canto/espaco.py`)

1. **A câmera de um ponto:** a parede do fundo de frente (as fiadas horizontais); o horizonte na altura dos olhos; o
   ponto de fuga onde as tábuas do tampo já convergiam. A parede da esquerda é a lateral do cômodo, a 90° da do fundo:
   as linhas horizontais dela correm em profundidade, então vão para **o mesmo ponto**.
2. **O encontro das paredes:** uma vertical (atrás do esteio do canto). No canto, as fiadas da lateral têm a altura das
   do fundo (17, 27, 37...), e a viga de cima é a travessa do fundo virando o canto, na mesma altura.
3. **As fugas:** cada linha da lateral passa pela altura dela no canto e pelo ponto; `_y_lateral(x, y_canto)`. Acima do
   horizonte, descem para o canto; abaixo, sobem; quanto mais longe do horizonte, mais inclinadas. As fiadas crescem
   para a esquerda (mais perto de nós): 10 px no canto, uns 23 na borda.
4. **A diminuição em profundidade:** blocos de comprimento igual na parede encurtam para o canto pela distância
   (1/profundidade, com uma distância focal escolhida: uns 64° de campo na largura da cena), não por um passo fixo:
   7 px no canto, 36 na borda. A junta vertical continua vertical.
5. **As faces que o olho vê:** a viga acima do olho mostra a face de baixo (na sombra), a do meio, abaixo do olho, a de
   cima (acesa pela vela); o esteio à esquerda do ponto mostra a face da direita, o da direita, a da esquerda.
6. **A mesa:** a borda de lá do tampo encontra a parede onde a parede está àquela profundidade; a mesa encosta no canto,
   e a linha do encontro também foge para o ponto (`_y_mesa_parede`), com 1 px de sombra de contato na parede.
7. **As guias** (o horizonte, o ponto, o canto, as fugas da viga, das fiadas e da mesa) numa camada oculta da fonte
   (`construcao`), fora da exportação; a folha `revisao-parede.png` mostra o espaço sozinho, com as guias e a cena.

## Ainda hipótese (espera o olho do Jean)

- Se a convergência forte da parede (a parede perto de nós, a viga de cima saindo do quadro) lê como o canto de uma
  sala pequena ou se pede o canto um pouco mais para a esquerda (uma parede mais longe, fugas mais suaves).
- Se a mesa encostada na parede lê bem com o castiçal perto dela.
- Se a viga do meio (só na lateral) faz sentido como construção ou sobra.
