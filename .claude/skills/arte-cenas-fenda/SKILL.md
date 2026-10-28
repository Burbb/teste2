---
name: arte-cenas-fenda
description: Construir, revisar, avaliar ou integrar um interior (cenário interno de um lugar: a forja, a curandeira, o templo, a taverna, uma casa, uma loja) ou outro ambiente de cena, e os personagens animados dentro dele, em The Unquiet (Crônicas da Fenda), no quadro de cima das cenas (telas/cenas.js, telas/cena-forja.js), do levantamento do lugar à candidata no protótipo e à integração. Use sempre que a tarefa for um interior novo ou refeito, um personagem de cena trabalhando (o ferreiro, a curandeira, o taverneiro, os fregueses), a animação de uma atividade, a comparação de candidatas de ambiente ou a consolidação da fonte em Aseprite de uma cena, mesmo que o Jean não cite a skill. Não serve para ícones e itens (arte-itens-fenda e as skills de cada objeto), retratos de carta nem regras de serviço.
---

# Interiores e personagens animados de cena

O processo que levou a forja do Vau, depois de várias candidatas, à H aprovada pelo Jean em oficina, enquadramento,
corpo, estilo e movimento (a H2 é a H com o olho ajustado), e depois ao golpe final do ferreiro ("Corpo desce", na
fonte e no jogo em 28/10/2026). Ele ajuda a fazer e a conferir uma cena; quem aprova é o Jean, no jogo. O estudo de
caso, com as fontes e o que cada candidata ensinou, está em [forja.md](forja.md): use-o como exemplo, não como regra (as
medidas, o ciclo de 53 quadros, a martelada e a paleta são da forja).

O que se quer evitar de novo: a imagem gerada reduzida e usada sem transposição artística, o personagem fora do estilo
do jogo, os apoios desconectados, a anatomia confusa e as correções da animação descobertas tarde.

## O fluxo de um interior (10 passos)

Cada passo fecha antes do seguinte; as seções abaixo detalham.

1. **Levantamento do lugar** (seção 1): o que o jogo estabelece, quem trabalha ali e quando (os estados da história:
   quem atende em cada momento), os serviços, os objetos que o ofício precisa, a circulação.
2. **Composição** (seção 1): a câmera pela atividade, a escala do personagem, as áreas de trabalho e os pontos de
   interação (os rótulos fora do personagem e da ação).
3. **Referências separadas** (seção 2): a imagem de composição de um lado; as cenas aprovadas do jogo, de outro, como a
   referência canônica do acabamento.
4. **Desenho na grade real** (seção 3): silhuetas e volumes primeiro, nos pixels do jogo; materiais e detalhes depois.
5. **Personagem** (seção 4): identidade (só o que o jogo estabelece), proporções, perspectiva e leitura no tamanho de
   uso.
6. **Atividade** (seção 5): as poses-chave, os contatos e a trajetória da ferramenta antes de completar o ciclo; a
   geometria do alcance (seção 5a).
7. **Animação** (seção 5): o corpo participando quando a ação pede, os apoios preservados, o ritmo da atividade (não o
   de outra cena) e a passagem limpa do fim para o começo; a pose parada para o movimento reduzido.
8. **Conferência no contexto** (seção 3, último item): a cena junto da HUD, dos serviços e dos rótulos, nas resoluções
   suportadas.
9. **Fonte final** (seção 6): o arquivo editável como autoridade, a exportação reproduzível, os retoques protegidos.
10. **Integração**: só a candidata aprovada, conferida no jogo real (seção "Três aprovações").

Caminhos relativos à raiz do repositório. O que já está documentado em outro lugar não se repete aqui:
- as fontes em Aseprite, o `pintar.lua`, a montagem e a exportação em lote: `ferramentas/arte/aseprite/LEIA-ME.md`;
- o Playwright local e as fotos no jogo: a memória "Playwright local" e `tests/navegador/cenarios.py`;
- as entregas sem vídeo (folhas e demonstração no navegador; vídeo só com pedido do Jean): a memória "Entregas sem
  vídeos";
- objetos que também são itens (uma espada na parede que é a do jogo): as skills de itens.

## Três aprovações diferentes

Aprovar a **referência** (a imagem que orienta), aprovar a **candidata** (o desenho no protótipo) e **autorizar a
integração** são três decisões do Jean, em momentos diferentes. Nenhuma implica a outra: uma candidata aprovada ainda
espera o pedido de integrar, e uma referência aprovada não aprova o que for feito a partir dela.

## 1. O levantamento (antes de desenhar)

- **O que o jogo diz do lugar e de quem está nele:** o texto, o serviço, a entrada e a saída, o que já existe na vila
  (o prédio, o som). Não invente nome, passado nem espécie; uma direção de aparência ("como um ferreiro anão") é
  aparência, não história.
- **O uso da cena:** as atividades (quem trabalha, onde, com o quê), a circulação (por onde se entra e sai), os pontos
  de interação (o que se clica e o que cada um faz, os nomes à vista) e o foco visual (onde o olho deve ir primeiro).
- **O enquadramento** vem da atividade e de quantas pessoas há na cena: um ofício de perto (a forja: um homem, a
  bigorna, a fornalha) pede uma câmera mais próxima; um salão com várias pessoas (a taverna) pede uma vista mais
  distante, com os rostos simplificados na escala dela. **Não iguale a altura em pixels** de pessoas de cenas com
  câmeras diferentes: o ferreiro da forja tem ~55 px e a Ilse, ~25, e os dois estão certos. Confira, sim, a
  proporção entre o personagem, os móveis e a arquitetura dentro da mesma cena.
- **O quadro:** as cenas usam 320 de largura (o pixel do jogo); a altura é a das paisagens (72) ou mais, se a
  composição pedir (a forja usa 96, com a vista crescendo na proporção, sem esticar). Uma altura nova precisa ser
  conferida com os cartões e controles embaixo, nas duas janelas.

## 2. As referências: composição × acabamento

Separe as duas:
- **Referência de composição e anatomia** (pode ser uma imagem gerada, uma foto, um quadro do Jean): perspectiva,
  volumes, proporções, distribuição dos objetos, relação entre personagem e mobília, luz geral. Guarde o original sem
  alteração em `ferramentas/arte/referencias/<lugar>/` com a origem e o hash num LEIA-ME.
- **Referência de acabamento** são as cenas aprovadas do jogo (a capela, a prisão da Ilse, a cidade, o mercado e as
  que vierem): o tamanho e o agrupamento dos pixels, a construção de pedra, madeira e metal, a quantidade de textura,
  os contornos e as sombras, o contraste, a simplificação de objetos e de pessoas. Fotografe-as no jogo, no tamanho
  real (`ferramentas/prototipos/hud/forja/auxiliares/estilo.mjs` faz isso), e leia o código delas
  (`rpg/web/static/telas/cenas.js`, `telas/mercado.js`).

O que essas cenas compartilham hoje: cada material em dois ou três tons chapados; a pedra em blocos regulares com as
juntas um tom abaixo, quase sem textura; a madeira com a aresta acesa e o lado escuro; o metal com o brilho de um
pixel; os objetos lidos pela silhueta e pelo valor, quase sem contorno preto; a luz feita por cima (o halo quente em
anéis em volta da fonte e a sala escurecendo em degraus pontilhados longe dela); as figuras sem contorno, com o olho de
um pixel. Aplique o que é comum; não copie o que é de uma cena só (o céu da cidade, a água da Ilse).

**A redução automática** de uma imagem de referência pode servir de guia (de posição e de luz), nunca de fundo: ela
dá manchas, não objetos. **Contar cores ou tirar contornos não prova coerência:** compare as cenas lado a lado, no
tamanho de uso.

## 3. Construir o ambiente

- Organize os objetos **por função** (o lugar do trabalho, o do material, o da entrada, o do armazém) e dê profundidade
  por sobreposição (o esteio na frente da parede, as silhuetas de primeiro plano), pela luz (o quente da fonte, o frio
  da porta) e pelos materiais. A oficina deve parecer usada: ferramentas penduradas, carvão, a tina, o pano na bancada.
- **Riqueza por objetos reconhecíveis, não por manchas pequenas.** Nem a sala vazia e chapada, nem a textura miúda
  sem forma.
- Cada objeto **apoiado ou preso a algo**: o que pende tem prego, gancho ou corrente; o que está de pé tem base; nada
  encosta em outro por acaso (as pontas das espadas tocando as barras da bancada) e nada flutua. Estruturas fazem
  sentido de construção: uma mão-francesa sai do esteio e sobe até a viga; a coifa e a chaminé ficam no eixo da boca
  da fornalha.
- Desenhe em código com o desenho escolhido (o método das cenas do jogo: retângulos, grades, a luz por cima) ou à mão
  no Aseprite; nos dois casos, **cada objeto é construído**, não recortado da referência.
- **Valide a cena com a interface e os serviços:** os nomes dos pontos fora do personagem e da ação, os cartões à
  vista sem rolar e sem rolagem vazia, a entrada, a saída e a volta, o Esc, o Tab chegando aos pontos.

## 4. O personagem de cena

- **Anatomia e silhueta legíveis antes do detalhe.** Leia a referência ampliada com a grade do jogo por cima para
  tirar as medidas (a cabeça, o tronco, as pernas, os pés); depois, construa.
- **No estilo das figuras do jogo** (três tons por material, sem contorno, o olho de um pixel, as mãos simples, sem
  dedos), com o detalhe que a escala da cena permite. Confira lado a lado com as figuras aprovadas, nos pixels da tela.
- **O rosto se decide no tamanho real**, não na ampliação: separe sobrancelha, órbita e ponte do nariz; o olho não
  pode encostar no escuro do nariz. Teste variantes mínimas e confira em várias poses.
- A barba, o cabelo e as roupas têm volume próprio (raiz, massa, ponta); não viram uma placa.

## 5. A animação

- **Estude movimento de verdade** (um GIF, um vídeo do Jean, uma animação de jogo) e registre o que foi observado
  quadro a quadro e o que foi só lido numa página ou visto numa imagem parada.
- **Poses, apoios e contatos antes do polimento.** Decida o que fica parado (os pés no chão, a mão na ferramenta, a
  peça na bigorna) e redesenhe cada pose inteira a partir desses apoios: o corpo participa (os joelhos dobram, o
  quadril desce, o tronco inclina, a barriga achata, o cabelo e a barba acompanham) **sem separar o tronco das pernas**
  e sem uma metade deslizar por cima da outra.
- **Mantenha conectado o que a ação exige:** a mão fechada na tenaz, a tenaz presa na peça, a peça apoiada; o
  balanço do corpo não arrasta o objeto. Um movimento deliberado do objeto (virar a peça) é um momento à parte,
  sempre acompanhado pela mão.
- **O ritmo aprovado é diferente das coordenadas e das poses:** pode-se manter o ritmo e reconstruir as poses. E o
  ritmo de uma ação (53 quadros de 100 ms, a martelada) não é padrão para outras.
- **Confira ciclos completos:** os quadros intermediários, a passagem do fim para o começo, a repetição, o movimento
  reduzido (uma pose parada coerente), e que sair e entrar de novo não acumule relógios.

## 5a. Ferramenta, braço e contato (o golpe do ferreiro, 28/10/2026)

O que as três passadas do golpe ensinaram (o histórico em [forja.md](forja.md)). Valem para qualquer personagem com uma
ferramenta: o pilão no almofariz, a faca na tábua, a concha no caldeirão.

- **Comprimento, distância e alcance:** antes de desenhar, meça na grade a distância do ombro ao ponto de contato e
  compare com o braço mais a ferramenta. Se braço e ferramenta passam dessa distância, o braço dobra e o ombro sobe
  (lia como "ombro levantado"); se não alcançam, a mão estica num ângulo impossível. A saída é geométrica: encurtar a
  ferramenta, aproximar ou baixar o corpo (o quadril e os joelhos), mover o objeto. Retocar o pixel não resolve.
- **Punho, cotovelo e ferramenta:** o cotovelo dobra para um lado só, o punho continua o antebraço, e a ferramenta sai
  da mão na direção do golpe. Mão colada ao corpo com o cotovelo para trás e o cabo de pé leu como "guidão de moto" e
  não dá para fazer de verdade.
- **Não esconda o contato nas conferências:** a pose em que a ferramenta toca o objeto é a que decide; nada de recorte,
  rótulo, faísca ou primeiro plano por cima dela na folha ou na foto de conferência.
- **Não confie em rotação automática:** girar em código o desenho de uma ferramenta em pixel art dá degraus e pixels
  soltos nos ângulos fora de 0°, 45° e 90° (a cabeça do martelo "fora do lugar", o cabo desalinhado). Nas poses que
  aparecem (o contato, o alto), desenhe a ferramenta à mão, alinhada à grade, com o cabo entrando reto no olho.
- **Movimento e leitura, não só igualdade técnica:** "a exportação saiu igual à candidata" prova a cópia, não o gesto.
  Veja o ciclo correndo no tamanho do jogo e pergunte o que a pessoa está fazendo.
- **O ciclo inteiro, não a pose mais bonita:** confira os quadros intermediários, o fim do golpe, a volta e a passagem
  para o começo; o defeito do ferreiro estava no fim do golpe, não na subida aprovada.

## 6. As fontes e a validação

- **Fontes editáveis e organizadas** (o ambiente, o personagem e as poses, as ferramentas, o fogo e a luz, o primeiro
  plano em camadas separadas) e **exportações reproduzíveis**. Depois que a fonte existe, ela é a autoridade: o script
  que a gerou não pode sobrescrevê-la sem um pedido explícito (`--refazer`), e a exportação lê dela.
- **Retoque aprovado vai para a fonte antes da integração:** uma correção feita no desenho do protótipo (em código)
  entra na fonte por um script que troca só a camada certa e confere o que salvou (na forja, `consolidar_gesto.py` e
  `aseprite/trocar_camada.lua`); depois, o script antigo que geraria a fonte recusa rodar sem a opção que descarta os
  retoques (`desenhar_h2.py --refazer` pede `--sem-os-retoques`), e o de consolidar não sobrescreve um retoque à mão
  sem `--forcar`. Confira o ciclo exportado contra a candidata aprovada, quadro a quadro, e veja as outras camadas
  saírem iguais.
- **Conferência técnica separada da avaliação artística:** "53 de 53 quadros iguais" ou "tudo certo" no roteiro de
  fotos prova que funciona, não que está bonito. A avaliação é no tamanho de uso, ao lado das cenas aprovadas.
- **Cada candidata nova numa pasta própria**, preservando a anterior, com folhas de comparação (antes × depois na
  mesma interface e com os mesmos dados; a candidata ao lado das cenas aprovadas; os detalhes das correções) e a
  demonstração no navegador para o movimento.
- Registre no LEIA-ME do protótipo e na continuidade o que foi reconstruído, o que ainda vem de outra fonte e o que
  continua limitado, sem chamar de aprovado o que não foi.

## Erros que aconteceram na forja (e como evitá-los)

| Erro | O que causou | Como evitar |
|---|---|---|
| A barba como uma massa única ("um saco no rosto") | a barba pintada como uma placa de cor, sem raiz nem ponta | raiz nas bochechas e no queixo, volume próprio, a trança ou a ponta separada |
| As botas enormes, o pé atravessando o toco | a bota desenhada maior que a escala e por cima de outro objeto | medir os pés na referência; nenhuma parte cobre o que está mais à frente |
| As pernas descoladas do corpo | a metade de cima subindo 1 px como peça rígida | redesenhar a pose inteira a partir dos pés: os joelhos e o quadril absorvem |
| A espada arrastada pelo tronco | a tenaz desenhada presa ao tronco, não à peça | a peça e a tenaz paradas; só a mão e o corpo se acomodam |
| A mão sem contato com a tenaz | a tenaz terminando no contorno da luva | as hastes entram na mão, os dedos fecham por cima e por baixo |
| O fundo derivado demais da imagem gerada | a redução limpa usada como fundo | construir cada objeto na linguagem das cenas aprovadas; a redução só como guia |
| Objetos no ar, mãos-francesas sem sentido, a coifa torta | desenho sem pensar em apoio e construção | conferir cada objeto: onde se apoia, onde se prende, em que eixo |
| O ferreiro fora do estilo do jogo | contorno escuro, muitos tons, textura miúda | comparar com as figuras aprovadas nos pixels da tela antes de polir |
| O olho grudado no nariz | o escuro do olho cercado de pele clara junto da ponte | órbita entre a ponte e o olho, decidir no tamanho real |
| O fim do golpe como "guidão" | a mão colada ao corpo, o cotovelo para trás, o cabo de pé | punho e cotovelo na direção do golpe; o braço vai à frente (5a) |
| O ombro levantado no contato | braço e cabo mais longos que a distância do ombro à peça | medir o alcance; baixar o corpo ou encurtar a ferramenta (5a) |
| A cabeça do martelo com pixels fora do lugar | a ferramenta girada em código em qualquer ângulo | desenhar à mão nas poses de contato, alinhada à grade (5a) |
| O retoque aprovado só no protótipo | a correção feita no desenho em código, fora da fonte | consolidar na fonte e travar os scripts antigos antes de integrar (6) |
