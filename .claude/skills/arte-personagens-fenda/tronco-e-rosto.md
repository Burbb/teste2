# Estudo: o tronco sob os braços e o rosto em pequenos movimentos (Morel no canto, 30/10/2026)

Material de apoio da seção "O tronco sob os braços e o rosto em pequenos movimentos" do [SKILL.md](SKILL.md). As
medidas são do caso de Morel (a cabeça de 28 px, o ombro em x 138 e 206); o que se leva para outra figura é a ordem e o
que cada passo confere.

## As fontes vistas (e o que cada uma deu)

| Fonte | O que foi visto | O que se aproveitou |
|---|---|---|
| Proko, *Anatomy of the Rib Cage* (texto e figuras da página) | a caixa torácica como ovo com planos | o topo mais estreito que a base, inclinado para a frente; a fúrcula onde as clavículas se encontram; sem o topo inclinado, o pescoço vira um "pirulito" espetado no tronco |
| Proko, *How to Draw Shoulder Muscles: Form* (as notas da aula) | a descrição do redondo maior e do grande dorsal | o redondo maior é o calombo do contorno junto da axila, e o grande dorsal desce dele num ângulo longo: o lado do tronco abaixo da axila é uma curva própria, não a continuação do braço |
| Captura do Gwent em *The Witcher 3* (a referência de ponto de vista, `ferramentas/arte/referencias/cenarios internos/`), uma imagem 3D com a perspectiva e a anatomia coerentes | o adversário sentado, de frente, com os cotovelos fora e os antebraços no tampo | o tronco mais estreito que a abertura dos cotovelos; a gola apoiada nos ombros, em volta do pescoço, com a barba por cima; os ombros arredondados, sem quina; o espaço entre o braço e o tronco mostrando o que está atrás |
| A vista aprovada diante do balcão (`camadas/morel-vista/parada.png`), a referência de acabamento | o mesmo Morel, noutra escala | o fundo aparece entre o braço da colher e o tronco; as lapelas sobem em diagonal até a barba; o colete arredondado em cima, sem faixa entre ele e a barba |
| A imagem gerada do canto | o casaco, o colete e a barba | o colete vermelho subindo até a barba, a gola do casaco em pé dos lados; o tronco largo dela (o casaco cheio) não foi seguido: como ela, ele enchia o espaço entre os braços |

O que **não** veio de fonte vista: a curva das tiras (dedução da câmera: a frente de um cilindro visto de cima fica mais
baixa) e a mastigação de 1 px (dedução da escala; o estudo de comer da Animation Mentor, já na skill, só diz que a
cabeça e o tronco participam).

## O tronco (`ferramentas/prototipos/taverna/morel/canto/tronco_estudo.py`)

1. **As medidas pela cabeça, não pelo cabelo:** a cabeça de Morel tem 28 px com o cabelo e a barba; o crânio, uns 24. A
   caixa torácica de um homem grande, na frente, mede uns 2,2 a 2,4 crânios: 58 a 62 px. As juntas dos ombros estão a
   68 px: o tronco é mais estreito que elas, e os braços saem por fora. A primeira candidata tinha 92 px.
2. **A caixa torácica:** um ovo de topo mais estreito, inclinado; a câmera olha de cima, então o peito é o que mais se
   vê. Mais larga embaixo, sem cintura marcada: Morel é robusto e está curvado para a tigela; a barriga continua o
   volume até o tampo (a largura cai 1 px, não 10).
3. **O contorno, linha a linha, decidido à mão:** o trapézio descendo da gola em curva côncava; o ombro convexo por
   cima do deltoide (escondido pelas ombreiras e pela raiz do braço, mas é ele que dá a forma quando os braços somem);
   a axila onde o contorno de dentro do braço encontra o lado do tronco; abaixo dela, o lado da caixa torácica.
4. **Os braços sobre o tronco:** a raiz do braço cobre o ombro; abaixo da axila, onde o braço se afasta (o cotovelo
   pousado para fora), o fundo aparece. Do lado do braço que desce mais rente, o vão é de 1 a 4 px; do lado do braço da
   colher, um triângulo maior. Isso é o limite do tronco, não um buraco a tapar.
5. **A roupa sobre os volumes:** o casaco aberto acompanha o tronco; a gola em pé envolve o pescoço (um cilindro grosso
   atrás da barba) e aparece dos dois lados dela; as lapelas descem em diagonal até as bordas do colete; o colete fecha
   até a garganta e a barba passa por cima dele. Do lado da vela, a borda de dentro da lapela acesa; do outro, a
   espessura dela faz sombra no colete.
6. **A conferência:** com braços, ombreiras e objetos ocultos (o tronco lê como tronco: ombros redondos, axilas, lados
   próprios?) e com tudo à vista em repouso, com a colher na boca e olhando (o braço que cruza o peito não revela nada
   faltando atrás dele: o tronco é desenhado inteiro).

## O rosto em pequenos movimentos

**A causa da fenda (a primeira candidata):** a variante `mastiga` copiava a grade da cabeça e descia 1 px todas as
linhas da boca para baixo; o vão de uma linha que ficava era preenchido só no meio (x 6 a 22 da grade), então dos dois
lados da barba ficava a parede à mostra, uma faixa de fundo atravessando o rosto. Não era sombra: era deslocamento de
recorte com área descoberta. Quatro das 20 poses usavam essa variante (as três da descida e a de repouso mastigando), e
a reação ao pagamento passa por elas quando a rotina recomeça.

**O que foi feito:** a variante é uma grade inteira (35 linhas): o bigode e as bochechas ficam; a boca, fechada e um
pouco mais curta, desce 1 px com o queixo; a barba de baixo ganha uma linha inteira, com o contorno dos lados
continuando. Alternando com a cabeça de repouso, lê como a mandíbula trabalhando dentro de uma cabeça só.

**A conferência:** uma conta por linha, em cada uma das 20 poses, procura pixels de fundo entre o contorno esquerdo e
o direito da cabeça, da gola e do tronco; e a sequência no tamanho real e ampliada (`revisao-mastigacao.png`).

## Ainda hipótese (espera o olho do Jean)

- Se 1 px de mandíbula lê como mastigar no tamanho do jogo, ou some (a alternativa seria a bochecha ganhar 1 px de
  sombra no lado da vela na pose de mastigar).
- Se a gola em pé lê como gola no tamanho real, ou só como mais casaco.
- Se o vão entre o braço da colher e o tronco lê como espaço, ou como um buraco na roupa.
- Se a curva de 1 px das tiras se percebe.
