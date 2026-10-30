---
name: arte-cenas-fenda
description: Construir, revisar, avaliar ou integrar um interior (cenário interno de um lugar: a forja, a curandeira, o templo, a taverna, uma casa, uma loja) ou outro ambiente de cena, e os personagens animados dentro dele, em The Unquiet (Crônicas da Fenda), no quadro de cima das cenas (telas/cenas.js, telas/cena-forja.js), do levantamento do lugar à candidata no protótipo e à integração. Use sempre que a tarefa for um interior novo ou refeito, um personagem de cena trabalhando (o ferreiro, a curandeira, o taverneiro, os fregueses), a animação de uma atividade, a comparação de candidatas de ambiente ou a consolidação da fonte em Aseprite de uma cena, mesmo que o Jean não cite a skill. Não serve para ícones e itens (arte-itens-fenda e as skills de cada objeto), retratos de carta nem regras de serviço.
---

# Interiores e personagens animados de cena

O processo que levou a forja do Vau, depois de várias candidatas, à H aprovada pelo Jean em oficina, enquadramento,
corpo, estilo e movimento (a H2 é a H com o olho ajustado), e depois ao golpe final do ferreiro ("Corpo desce", na
fonte e no jogo em 28/10/2026). Ele ajuda a fazer e a conferir uma cena; quem aprova é o Jean, no jogo. O estudo de
caso, com as fontes e o que cada candidata ensinou, está em [forja.md](forja.md): use-o como exemplo, não como regra (as
medidas, o ciclo de 53 quadros, a martelada e a paleta são da forja). A curandeira (em avaliação) está em
[curandeira.md](curandeira.md): o caso da atuação de um trabalho delicado (seção 5b).

O que se quer evitar de novo: a imagem gerada reduzida e usada sem transposição artística, o personagem fora do estilo
do jogo, os apoios desconectados, a anatomia confusa e as correções da animação descobertas tarde.

## O fluxo de um interior (11 passos)

Cada passo fecha antes do seguinte; as seções abaixo detalham.

1. **Levantamento do lugar** (seção 1): o que o jogo estabelece, quem trabalha ali e quando (os estados da história:
   quem atende em cada momento), os serviços, os objetos que o ofício precisa, a circulação.
2. **Composição** (seção 1): a câmera pela atividade, a escala do personagem, as áreas de trabalho e os pontos de
   interação (os rótulos fora do personagem e da ação).
3. **Referências separadas** (seção 2): uma referência de composição discutida com o Jean de um lado; as cenas
   aprovadas do jogo, de outro, como a referência canônica do acabamento. A referência gerada orienta a construção,
   mas não prova que a perspectiva dela está certa: o desenho precisa da conferência própria (seção 3a).
4. **O espaço antes dos objetos** (seção 3a): o piso, os planos, a circulação e os apoios, conferidos com os móveis e
   as pessoas escondidos, antes de detalhar; as paredes laterais e os cantos pela mesma projeção (seção "Paredes
   laterais e cantos").
5. **Desenho na grade real** (seção 3): silhuetas e volumes primeiro, nos pixels do jogo; materiais e detalhes depois.
6. **Personagem** (seção 4): identidade (só o que o jogo estabelece), proporções, perspectiva e leitura no tamanho de
   uso. A construção do corpo e dos membros (o estudo com formas simples, os comprimentos fixos, o escorço, a roupa por
   cima, as passagens) segue a skill `arte-personagens-fenda`.
7. **Atividade** (seções 5 e 5b): a atividade e os apoios por escrito, quem conduz, acompanha e fica, as poses-chave
   do corpo inteiro, os contatos e a trajetória da ferramenta antes de completar o ciclo; a geometria do alcance
   (seção 5a).
8. **Animação** (seções 5 e 5b): uma rotina com pausas e intenção, as passagens escalonadas, os apoios preservados, o
   ritmo da atividade (não o de outra cena) e a passagem limpa do fim para o começo; a pose parada para o movimento
   reduzido. Limpeza, quantidade de quadros e atuação conferidas em separado.
9. **Conferência no contexto** (seção 3, último item): a cena junto da HUD, dos serviços e dos rótulos, nas resoluções
   suportadas.
10. **Fonte final** (seção 6): o arquivo editável como autoridade, a exportação reproduzível, os retoques protegidos.
11. **Integração**: só a candidata aprovada, conferida no jogo real (seção "Três aprovações").

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

## 3a. O espaço antes dos objetos (o templo B, 28/10/2026)

A primeira passada da B transpôs a distribuição da referência mas perdeu as superfícies que explicavam a
profundidade: tudo pisava na linha em que o piso começava, e o piso, em fiadas desencontradas como uma parede, lia
como um muro baixo. Mesa, armário, porta e clérigo pareciam grudados na parede. Antes de desenhar os objetos:

1. **O piso sozinho.** Desenhe as paredes, o piso e as elevações sem os móveis nem as pessoas (uma função como
   `so_o_espaco()`) e olhe no tamanho do jogo: o piso tem de ler horizontal. Juntas transversais mais juntas no fundo
   e mais abertas na frente; as longitudinais convergindo para o fundo (numa câmera de frente). Fiadas desencontradas
   de largura igual são parede, não chão. Não precisa de perspectiva rígida: coerente com a câmera e legível.
2. **Onde a parede encontra o piso** é uma linha só, atrás de tudo; o que se encosta nela pisa logo à frente; o que
   está mais perto pisa mais embaixo. Deixe chão à vista entre as coisas (o pé da mesa, a barra da roupa, o pé do
   banco) onde ele explica a posição delas.
3. **Elevação só onde ela existe** (o presbitério, um estrado): o piso de cada degrau claro (horizontal), a frente
   escura (vertical). Não invente um degrau para justificar um objeto mal apoiado.
4. **Cada objeto apoiado**: tampo (o claro de cima e a espessura), pernas até o piso, base ou rodapé; o que pesa (o
   altar) tem base mais larga. As portas têm soleira; a entrada liga o vão ao piso de dentro.
5. **As sobreposições**, também durante a animação: em cada cruzamento, decida o que está à frente (a roupa e o pé da
   mesa não se tocam; uma conta pode conferir que nenhum pixel da figura cai nas pernas em nenhuma pose do ciclo).
6. **Sombra de contato** de um pixel, só depois da geometria: ela confirma o apoio, não o cria.
7. **O primeiro plano** enquadra pelos cantos; uma silhueta que esconde os apoios ou faz uma barra sem função sai.

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

Braços, ombros e mãos em ação (o braço que encurta, gruda no peito ou some atrás da roupa): o método está na skill
`arte-personagens-fenda` (o caso de Morel na taverna, 29/10/2026). Aqui fica o que é próprio da cena.

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
  peça na bigorna) e redesenhe cada pose inteira a partir desses apoios. Quando o esforço pede (a martelada), o corpo
  participa (os joelhos dobram, o quadril desce, o tronco inclina, a barriga achata, o cabelo e a barba acompanham)
  **sem separar o tronco das pernas** e sem uma metade deslizar por cima da outra; quando não pede, o tronco firme é
  parte da pose (seção 5b, "Quanto do corpo participa").
- **Mantenha conectado o que a ação exige:** a mão fechada na tenaz, a tenaz presa na peça, a peça apoiada; o
  balanço do corpo não arrasta o objeto. Um movimento deliberado do objeto (virar a peça) é um momento à parte,
  sempre acompanhado pela mão.
- **O ritmo aprovado é diferente das coordenadas e das poses:** pode-se manter o ritmo e reconstruir as poses. E o
  ritmo de uma ação (53 quadros de 100 ms, a martelada) não é padrão para outras.
- **Confira ciclos completos:** os quadros intermediários, a passagem do fim para o começo, a repetição, o movimento
  reduzido (uma pose parada coerente), e que sair e entrar de novo não acumule relógios.
- **Um acontecimento do motor na cena** (o pagamento na mesa de Morel, 30/10/2026): o motor decide e conta (a cobrança,
  o resultado); a cena só desenha uma vez por acontecimento que ele mandou, e repetir a mensagem não repete o efeito. O
  que ele deixa na cena fica até ela acabar (as moedas não somem), e quem estava na rotina reage só o que o fato pede,
  com as poses que já existem (a colher volta ao descanso pelo caminho mais curto, os olhos vão ao que caiu).

## 5b. A atuação, passo a passo (a curandeira, 28/10/2026)

Na curandeira, o braço do pilão ficou limpo, com 12 poses a 100 ms, e o resultado foi robótico; a resposta que funcionou
lá (os ombros e a cabeça acompanhando o esforço do pilão) foi depois aplicada como regra no taverneiro da G4, onde não
havia esforço, e leu como o corpo inteiro limpando a caneca. Nenhum dos dois erros é "mexer pouco" ou "mexer muito": é não decidir, pela atividade, quem mexe e
quanto. Faça isso nesta ordem e por escrito, antes dos quadros intermediários.

**Quanto do corpo participa** (o Jean, 29/10/2026): uma ação natural não exige movimento do corpo inteiro. A
participação depende do **esforço**, do **alcance**, dos **apoios** e da **intenção**; as partes estáveis também fazem
parte da atuação (é o tronco firme que deixa a mão trabalhar). Três casos diferentes:
- **Martelar** (o ferreiro): esforço grande e golpe longo; os joelhos, o quadril, o tronco e os ombros participam, e a
  cabeça acompanha o golpe.
- **Limpar uma caneca** (o taverneiro da G4): pouco esforço e alcance curto; conduzem a mão do pano e a mão que segura
  a caneca (pequenos ajustes de pega); acompanham o antebraço, o cotovelo e o ombro do pano (o alcance e a pressão,
  1 px); o tronco fica; a cabeça olha o trabalho, parada. O pano segue o contato e a gravidade, sem balanço.
- **Olhar para alguém** é uma ação própria, com a sua hora (uma pausa, um som, alguém que chega): os olhos sobem e a
  cabeça vai junto. Não é consequência de cada gesto da mão; a cabeça não "acompanha" uma passada de pano.

Diminuir igualmente a amplitude de tudo não resolve: decida parte por parte o que precisa mexer e o que dá
estabilidade.

1. **A atividade e os apoios.** Uma frase do que a pessoa faz ("mói ervas, olha a mistura, cheira uma pitada, volta a
   moer") e a lista do que não se mexe enquanto ela faz (os pés, a barra da saia, o almofariz no tampo, a mão que
   segura a borda, o pé do pilão dentro da boca).
2. **Quem conduz, quem acompanha, quem fica**, numa tabela por trecho da rotina, pelo esforço e pelo alcance (o
   quadro acima). Na curandeira, moendo (a pedra aperta e o pilão vai longe do corpo): conduz a mão no pilão;
   acompanham o cotovelo (sai do comprimento fixo do braço), os ombros (1 px à frente quando o pilão vai longe, 1 px
   abaixo onde a pedra aperta) e a cabeça (um quadro depois dos ombros, porque ela olha a mistura que aperta); ficam o
   quadril e a saia. Olhando a
   mistura: conduz o tronco; o quadril vai para trás, a saia acompanha no alto, a barra fica. O que fica parado é uma
   decisão, não um esquecimento.
3. **O alcance decide o corpo.** Braço com comprimentos fixos (ombro-cotovelo, cotovelo-mão) e o cotovelo calculado;
   se a mão não alcança o ponto, o desenho falha (um `assert`) em vez de esticar o braço. Quem não alcança leva o corpo
   junto, e é daí que o tronco participa de verdade (se a mão alcança sem ele, o tronco fica). Se a geometria força uma postura ruim, mude a cena, não o pixel: a
   Pita, de pé no chão, trabalhava com o almofariz na altura do peito e o braço esticado na altura do ombro; um
   banquinho de madeira (ela sobe nele para alcançar a bancada da Marta) e 2 px mais perto resolveram.
4. **Poses-chave do corpo inteiro**, numa folha de trabalho com a figura completa (pés até a cabeça) em cada uma,
   também as partes que ficam paradas (é na figura inteira que se vê se o que fica dá apoio ao que mexe): o
   início, as pontas do gesto, a pausa, o contato com cada objeto. A ferramenta com tamanho fixo em todas (o pilão é um
   vetor de comprimento constante, desenhado linha a linha com a mesma espessura).
5. **Uma rotina, não um laço.** Uma atividade tem trechos com intenção e pausas: trabalhar algumas vezes, desacelerar,
   conferir, fazer outra coisa pequena com o mesmo material, voltar. Escolha uma ação secundária que os objetos da cena
   já sustentam e que o alcance permite sem caminhar (na curandeira, a pitada levada ao nariz). O fim emenda no começo
   por uma pose em que a ferramenta já está igual (a pega deixa o pilão onde a pose 1 do giro o tem). A linha do tempo
   sai da fonte (um JSON gerado), não é repetida na tela.
6. **As passagens:** em cada troca de trecho, uma parte vai na frente e as outras chegam depois (a mão antes do corpo,
   o corpo antes da cabeça, a cabeça vira por último), entre as partes que participam daquele trecho; nenhuma pose
   troca tronco, quadril, cabeça e mão de uma vez.
   Meça quanto cada parte anda de um tique para o outro (≤ 1 px no corpo, a mão um pouco mais); a contagem de pixels
   mudados serve para achar candidatos a pulo, mas engana (deslocar o tronco 1 px muda muitos pixels e lê como
   movimento pequeno).
7. **Personagens diferentes, a mesma lógica:** o ritmo e a postura de cada um saem do que o jogo estabelece, com
   contenção (Marta aperta nas pontas da volta e olha com mais tempo; Pita se inclina mais perto e é um pouco mais
   ligeira). Nada de fragilidade ou agitação inventadas.
8. **O ritmo de uma parte combina com o resto da atuação.** Mais poses no braço não deixam a animação mais coerente:
   na terceira passada da curandeira, o braço girava em 12 poses de um tique enquanto o corpo mudava de 1 px em 1 px
   de vez em quando, e o braço parecia de outro jogo (contínuo demais, como um vídeo sobre pixel art). O que funcionou
   (quarta passada): poucas poses escolhidas pela expressão (7 por volta, não 12), cada uma sustentada de 2 a 3
   tiques, e o tempo concentrado no momento de esforço (a pressão longe do corpo dura 4 a 6 tiques, e a cabeça termina
   de descer no meio dela, porque ali o esforço pede). Mantenha a duração da ação: redistribua, não acelere. O relógio da
   cena continua a 100 ms (o fogo, a troca de pose); é a pose que segura mais tempo.
9. **Conferência em três camadas, separadas:** a **limpeza técnica** (pixels soltos, buracos, a manga ligada ao braço,
   nenhum pedaço do avental virando braço, a ferramenta do mesmo tamanho) no zoom; a **quantidade de quadros e o
   ritmo** na linha do tempo; a **atuação** (o que a pessoa está fazendo, onde ela olha, se o corpo reage na medida do
   esforço, sem mexer o que deveria dar apoio, se as pausas têm intenção, se a volta ao começo some) na sequência tique a tique e no jogo, no tamanho real. Passar
   na primeira não diz nada das outras duas.

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
- **A identidade se confere com as outras versões do personagem no jogo** (o retrato, a figura pequena, a carta), não só
  com a referência da cena: Morel na mesa tinha uma ombreira, e o retrato e a figura têm duas (30/10/2026). Liste o que
  elas mostram (o equipamento, a arma, as marcas do rosto, as cores) e o que a cena acrescenta, antes de fechar.
- **A articulação também se confere no acabamento:** uma junta no lugar certo ainda pode ler como peça encaixada pela
  silhueta ou pela luz (o ombro e o cotovelo de Morel comendo, 30/10/2026: a manga em duas cápsulas). Confira cada pose
  sozinha e o ciclo em sequência, antes e depois lado a lado, e as poses que outra ação reaproveita; o método está na
  `arte-personagens-fenda` (passo 7 e "Uma articulação certa que ainda parece mecânica").
- **Construção não é acabamento:** o que se calcula (as juntas, os volumes, a perspectiva, as sobreposições) é a guia
  oculta da fonte; o acabamento é desenhado por cima, com a cena aprovada ao lado, na linguagem dela (a queda de braço,
  30/10/2026: os volumes calculados e iluminados foram recusados por parecerem um modelo 3D em baixa resolução; o
  detalhe na `arte-personagens-fenda`, "O estudo de construção e o acabamento são etapas diferentes").
- **A interface que passa por cima da cena entra na composição:** o dado dos testes, os balões, a faixa de resultado.
  Confira a cena com ela no tamanho real (a captura inteira, não um recorte, que pode cortar o que não está cortado).
- **Conferência técnica separada da avaliação artística:** "53 de 53 quadros iguais" ou "tudo certo" no roteiro de
  fotos prova que funciona, não que está bonito. A avaliação é no tamanho de uso, ao lado das cenas aprovadas.
- **Cada candidata nova numa pasta própria**, preservando a anterior, com folhas de comparação (antes × depois na
  mesma interface e com os mesmos dados; a candidata ao lado das cenas aprovadas; os detalhes das correções) e a
  demonstração no navegador para o movimento.
- Registre no LEIA-ME do protótipo e na continuidade o que foi reconstruído, o que ainda vem de outra fonte e o que
  continua limitado, sem chamar de aprovado o que não foi.

## A câmera vem antes da animação (o encontro com Morel, 30/10/2026)

Uma queda de braço refeita várias vezes não fechava porque a câmera da cena (a vista diante do balcão) não era a de
um adulto sentado à mesa: o braço do jogador precisava atravessar a mesa. A saída foi trocar a cena, não a pose:
- **Primeira pessoa:** a câmera nos olhos de quem senta; o horizonte na altura dos olhos de quem está do outro lado;
  o tampo de cima e a borda do nosso lado fora do quadro; o personagem grande. Um gesto nosso futuro (a mão, o
  antebraço) entra pela borda de baixo, sem o braço até o ombro.
- **A proporção da referência** se resolve sem esticar, sem achatar e sem recuar a câmera: ela entra no tamanho dela
  na altura da cena, e o lugar continua nas laterais.
- **Onde a perspectiva da imagem gerada não fecha** (as fiadas de uma parede contradizendo o tampo visto de cima),
  a construção vence e a diferença fica registrada.
- **A redução mapeada nas paletas não serve de arte,** nem segmentada por material: o pontilhado da redução, as cores
  vazando de um material para outro, o rosto ruidoso. Ela fica como guia oculta; o personagem é desenhado de novo, por
  partes, na escala nova (a cabeça numa grade à mão no jeito da aprovada, os braços pela manga aprovada).
- **A cena antiga não se apaga:** fica preservada e com a destinação registrada (a vista do balcão, para a Vó Berta).

## Paredes laterais e cantos (o canto de Morel, 30/10/2026)

Na primeira candidata do canto, a parede da esquerda tinha um ponto de fuga próprio, escolhido para imitar as fiadas
suaves da imagem gerada, e lia como outra parede de frente com textura inclinada; o tampo atravessava a parede. O
estudo, as fontes vistas e a construção estão em [paredes-laterais.md](paredes-laterais.md). O tronco e o rosto da
figura no mesmo quadro são da `arte-personagens-fenda` ("O tronco sob os braços e o rosto em pequenos movimentos").

**Princípios gerais:**
- **A projeção antes das inclinações:** o horizonte é a altura dos olhos da câmera; numa câmera de frente para a parede
  do fundo (um ponto), tudo o que corre em profundidade foge para o mesmo ponto: as tábuas do piso ou do tampo e as
  linhas horizontais das paredes laterais. Ponto próprio para uma parede só se a sala não for retangular (decisão
  registrada). Nenhuma viga ou fiada ganha uma inclinação escolhida isoladamente.
- **Acima e abaixo do horizonte:** o que está acima desce em direção ao fundo, o que está abaixo sobe, o que está na
  altura dos olhos fica horizontal; mais longe do horizonte, mais inclinado. As verticais continuam verticais.
- **O encontro das paredes** é uma vertical; o que é contínuo na construção continua no canto na mesma altura (as
  fiadas, a viga que vira o canto).
- **A diminuição em profundidade:** espaçamentos iguais na parede (blocos, vigas, esteios) encurtam para o fundo pela
  profundidade, não por um passo fixo; a parede perto de nós tem fiadas e blocos maiores.
- **As faces que aparecem dizem a altura do olho:** uma viga acima do olho mostra a face de baixo; abaixo, a de cima; um
  esteio mostra a face voltada para o ponto de fuga.
- **Os móveis respeitam a parede:** um tampo que passa do ponto em que a parede está naquela profundidade entra nela;
  encoste o móvel (o encontro foge para o ponto) ou termine-o antes.
- **Confira o espaço sozinho**, com as guias (o horizonte, o ponto, as fugas) numa camada oculta, e sem elas no tamanho
  real; pedra e madeira no mesmo plano (as juntas e as vigas pela mesma conta). A luz reforça o espaço, não o constrói.
- **Uma referência gerada se verifica:** meça as fugas dela sobre a guia; se as linhas de uma parede não passam no ponto
  do resto da imagem (ou contradizem a altura do olho que o tampo mostra), ela orienta a composição, não a perspectiva.

**Neste caso** (o exemplo; as medidas são da cena de Morel): [canto-parede-lateral.png](exemplos/canto-parede-lateral.png)
(em cima, a primeira candidata; embaixo, a revisada: o espaço sozinho, com as guias da sala e a cena inteira). O
horizonte em y 22 e o ponto em x 170 já eram os do tampo; a lateral passou a fugir para eles, com as fiadas de 10 px no
canto e uns 23 na borda, os blocos de 7 a 36 px pela profundidade, a travessa virando o canto, a mesa encostada.

**Ainda hipótese** (espera a avaliação do Jean): se a convergência forte lê como o canto de uma sala pequena, ou pede o
canto mais para a esquerda (fugas mais suaves); se a mesa encostada lê bem com o castiçal junto dela.

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

## Erros que aconteceram na curandeira

| Erro | O que causou | Como evitar |
|---|---|---|
| O trabalho robótico com o braço limpo | só o braço em 12 poses, sem decidir quem acompanha o esforço e o alcance | a tabela de quem conduz, acompanha e fica; o alcance fixo levando o corpo quando a mão não chega (5b) |
| O taverneiro limpando a caneca com o corpo inteiro (a primeira G4) | o tronco e a cabeça descendo a cada passada, por regra, enquanto a mão do pano andava 1 a 2 px | a mão do pano conduz uma volta na caneca, o cotovelo e o ombro do pano acompanham 1 px, a mão da caneca ajusta a pega; o tronco e a cabeça ficam; olhar os fregueses é uma ação à parte, na pausa (5b, "Quanto do corpo participa") |
| Mais quadros sem melhorar | o mesmo gesto isolado subdividido | uma rotina com desaceleração, pausa e ação secundária (5b, passo 5) |
| O braço da menina como uma barra no ombro | a bancada de adulto: o almofariz na altura do peito dela | mudar a cena (o banquinho), não esticar o braço (5b, passo 3) |
| Os maços como pinhatas | o mesmo saco simétrico em cores diferentes, o nó em bloco | cada planta pela silhueta dela, à mão: o barbante e as voltas da amarração, os talos, o leque, a espiga, a cabeça redonda, o cacho de bolinhas |
| O braço "contínuo demais" perto do corpo | 12 poses de um tique no braço, o corpo em passos raros de 1 px | poucas poses expressivas sustentadas, o tempo na pressão (5b, passo 8) |
| O corpo "quebrando" quadro a quadro (o clérigo do templo B) | a inclinação feita fatiando o tronco linha a linha sobre uma cintura parada | numa figura pequena, o tronco e a cabeça inclinam como um bloco e a roupa absorve, da cintura à barra parada; um degrau de mais de 1 px no contorno é sinal de encaixe |
| Móveis e pessoas grudados na parede (o templo B) | tudo pisando na linha onde o piso começava; o piso em fiadas de parede | o espaço sozinho primeiro; a parede encontrando o piso atrás de tudo, chão à vista entre as coisas (3a) |
| A roupa misturada ao pé da mesa | a barra do hábito encostada na perna, o hábito no mesmo marrom da madeira | 2 px de chão entre eles; o hábito noutro valor; a conta das sobreposições em todo o ciclo (3a) |
| O pescoço solto do vestido | a grade da cabeça desenhada sem olhar onde começa o tronco | o pescoço da grade cai no colo do vestido em todas as poses da cabeça |

## Erros que apareceram na taverna (candidata A, 29/10/2026)

Uma cena com muita gente: as mesmas regras de uma figura, multiplicadas, e o que só aparece com várias. O caso está em
`ferramentas/prototipos/taverna/LEIA-ME.md`.

| Erro | O que causou | Como evitar |
|---|---|---|
| Alguém atravessando o tampo ou o balcão | o corpo e as mãos numa camada só | duas camadas por figura: o corpo atrás do móvel, as mãos e o que seguram na frente; entre as duas, uma camada só com os móveis da frente (tirada do fundo já iluminado) |
| A mão "alcançando" com o braço esticado além do possível | os alvos postos onde a pose pedia, sem medir | o braço com comprimento fixo pela régua do lugar e o `assert` do alcance; a correção é aproximar a pessoa ou recuar o alvo, não esticar o braço |
| A figura espelhada inclinando para trás | a inclinação somada em coordenadas do mundo numa figura desenhada no espaço dela | a pose no espaço da figura: +x é sempre para a frente, para onde ela olha |
| Duas pessoas da mesma mesa gesticulando juntas | as fases espalhadas ao acaso | quem conversa ou joga tem rotinas do mesmo comprimento e a mesma fase, desenhadas para se revezar; conferir por conta (nenhum passo com os dois falando ou mexendo) |
| A vela na frente do rosto de quem está atrás da mesa | o castiçal sempre no meio do tampo | o objeto do móvel sai da frente do rosto: a vela na ponta da mesa |
| Uma figura sumindo contra a parede escura | cabelo, roupa e parede no mesmo valor | o que se lê de longe (a cabeça, o avental) num valor diferente do fundo atrás dele |
| O fogo como um gráfico de barras | retângulos de alturas diferentes | línguas que afinam para cima, a ponta pendendo, a lenha e as brasas embaixo e o caldeirão na frente das chamas |
| A porta aberta contradizendo a vila | a rua de dia, com neve, da referência | uma vista de fora só se o interior acompanhar a hora e o tempo; senão, a porta fechada |
| O nome de um ponto cobrindo uma cabeça | o balão posto em cima do objeto pequeno no piso | conferir os balões com as pessoas no lugar, nas duas resoluções; o balão vai onde não há rosto nem mão |

**A candidata B (estudo estático, 29/10/2026)**, depois da A não aprovada:

| Erro da A | Como a B resolveu |
|---|---|
| Um banner com figuras pequenas: tudo na mesma faixa de profundidade | o ponto de fuga dentro do quadro e muita profundidade (11 px/m no fundo, 34 na borda de baixo): quem está na frente fica três vezes maior, na mesma régua; mesas em três distâncias |
| Pessoas estreitas, iguais, de perfil | cada figura à mão numa grade, com porte e ângulo próprios (de frente, três quartos, costas, perfil); acertar três representativas no tamanho real antes de fazer as outras |
| O balcão enorme perto de quem está atrás | o balcão na régua de quem atende (1,05 m), mais perto da câmera que a parede do fundo |
| Piso, móveis, roupas e fundo no mesmo marrom | cada material num valor: a pedra fria e escura, o reboco claro, os móveis mais quentes que o piso, as roupas em cores contidas e diferentes |
| Tábuas radiando de um ponto de fuga dentro do quadro viram tracejado nas laterais | as tábuas paralelas ao fundo, mais juntas longe, e as emendas correndo para o ponto de fuga |
| Um alçapão aberto (e barris deitados com o tampo para a sala) lendo como caixote e rodas | a entrada como porta (baixa, entreaberta, com o escuro na fresta); os barris em pé, de lado |
| O cenário mais alto empurrando os cartões para trás da doca | o balcão compacto com o interior (a fala numa linha, os cartões em duas colunas, o Voltar na célula livre) e a rolagem refeita quando a página muda; conferir que cada cartão e o Voltar ficam acima da doca sem rolar |

**A candidata C (estudo estático, 29/10/2026)**, depois da B não aprovada:

| Erro da B | Como a C resolveu |
|---|---|
| Profundidade exagerada: a frente três vezes maior que o fundo, Morel com 3 a 4 px de cabeça | a profundidade não é uma meta: a régua contida (13 a 30 px/m) e as pessoas importantes na faixa do meio (cabeça de 6); o balcão e o canto vêm para a frente junto com quem está neles, não só o sprite |
| A escada como uma diagonal de riscos; a galeria sem piso | a estrutura inteira: o pilar do pé no chão, os degraus (o piso claro, o espelho escuro), o banzo grosso, o corrimão; o pilar do patamar como esteio da galeria; o piso da galeria visto de cima entre as portas e o guarda-corpo (pode ser um pouco forçado para ler), a testeira com as pontas das vigas, as mãos-francesas |
| A lareira como um bloco cinza | os planos: a laje no piso, a boca com as faces de dentro e o fundo, a verga com a prateleira, a coifa que só abre embaixo, a chaminé estreita; o caldeirão pequeno e alto, para o fogo aparecer |
| A cabeça alta demais, o corpo afundando atrás do balcão | medir a altura dos ombros pela régua (1,45 m em pé) e caber a cabeça com a barba em 0,25 a 0,3 m; o pescoço em pele entre a barba e a gola |
| O pontilhado da luz fazendo anéis no reboco | faixas lisas de escuro; o pontilhado só onde ele ajuda |

**A lição geral da candidata D (29/10/2026): quem senta se constrói junto do móvel e da atividade.** Na C as figuras
estavam certas uma a uma e erradas em conjunto (Morel na ponta do banco longe do espaldar, um jogador sem assento, um
homem sentado na mesa e no balcão ao mesmo tempo, uma cadeira vazia maior que as ocupadas e com o encosto
atravessando o tampo). Para cada pessoa sentada, nesta ordem e com os móveis desenhados primeiro sozinhos:

1. **o assento:** onde o quadril pousa (a altura de 0,45 m na régua do lugar), e de que lado está o encosto;
2. **a orientação:** para onde ficam o quadril, o tronco e as pernas, coerentes com o assento e com quem está em volta;
3. **o alcance:** do ombro à mão, no máximo o braço (0,6 m na régua); se não alcança, aproximar o assento ou a mesa;
4. **a atividade:** o objeto na mão ou no tampo (a caneca, a colher na tigela, a peça no tabuleiro), visível;
5. **as sobreposições:** quem está atrás do tampo, desenhado antes dele, mostra embaixo o que o apoia (as coxas, as
   canelas, os pés do banquinho); nada atravessa o tampo nem esconde justamente a parte que explica o apoio; a figura
   não encosta em outro móvel que a confunda (o balcão atrás das pernas de quem senta na cabeceira);
6. **a escala dos móveis vazios** é a dos ocupados.

Não é preciso mostrar todas as pernas e articulações: as partes visíveis explicam a pose sem contradição.

**A lição da candidata E (29/10/2026): com vários grupos, uma escala e uma câmera comuns antes de cada conjunto.** Da
B à D, cada conjunto foi corrigido no seu lugar, e eles continuavam sem concordar (Morel e a mesa ao lado em escalas
diferentes; a parede frontal e os tampos, cada um num grau). O que resolveu:

1. **Uma projeção para tudo**, numa função (`P(X, Z, H)`): o piso, as paredes, os tampos, os assentos, os degraus, a
   galeria e as pessoas saem dela. Uma perspectiva simplificada vale, desde que seja a mesma em toda a cena (a face de
   cima de uma mesa e a do piso da galeria aparecem pela mesma conta).
2. **Os móveis como caixas projetadas** (a face de cima, a da frente, a do lado que olha para o meio), não desenhados
   cada um com o seu grau.
3. **Uma figura de referência** (1,75 m, em pé e sentada) em vários lugares da sala, antes das pessoas: na porta, no
   balcão, no pé da escada, debaixo da galeria, em cada assento. Portas, degraus, tampos e bancos conferidos contra ela.
   A altura da cabeça ou a linha dos pés sozinhas não provam a perspectiva: o conjunto precisa convencer no tamanho do
   jogo.
4. **Só então as pessoas**, à mão, no ponto que a projeção dá ao assento de cada uma; as diferenças de porte (Morel
   maior, num banco robusto) vêm depois, sobre a mesma régua.
5. **A composição anterior não é sagrada:** quando os ajustes locais não resolvem a coerência, mude a câmera e a
   distribuição.

**A candidata F (29/10/2026): transpor uma referência aprovada para uma construção coerente.** Quando o Jean aprova uma
imagem gerada para a composição e as poses, ela orienta, mas não prova a construção: meça-a na grade do jogo (as
posições, os tamanhos, as cabeças), escolha a câmera da projeção que reproduz essas medidas, e construa a sala nessa
projeção. Onde a imagem não fecha (uma galeria baixa demais para a profundidade, uma mesa cortada pela borda, um
personagem com acessórios que não são dele), a construção e o jogo vencem, e a diferença é registrada.

**As candidatas G e H (29/10/2026): o balcão de perto.** Com muita gente na mesma vista, as figuras não convenciam; a
saída foi mudar a cena, não as figuras: uma câmera perto do balcão, uma atividade principal (o taverneiro limpando a
caneca), como na forja. Na mesma grade (320×96), a câmera de perto já dá espaço para o rosto e as mãos.

| Erro | O que causou | Como evitar |
|---|---|---|
| Os fregueses da frente como montes redondos e grandes (a primeira H) | as costas desenhadas como um polígono curvo, sem ombro, pescoço nem braço | construir o vulto por partes, como uma figura: a cabeça, o pescoço, a linha dos ombros, o tronco estreitando, o braço até o apoio; três tons escuros, não uma mancha |
| O pontilhado da luz na pele e na camisa | a luz da sala, em degraus pontilhados, aplicada também à figura | quem está no meio da cena recebe a luz num tom só; a modelagem fica nos planos do desenho |
| A cabeça encostando nas linhas da prateleira | uma prateleira contínua atrás da cabeça | a prateleira em duas partes, com o vão atrás da cabeça |
| A camisa chapada e os ombros como peças redondas (a limpeza da H) | a luz da figura trocada por um tom só, em tudo | o pontilhado também é tecido gasto e transição de volume: retocar por região (a testa, os antebraços, as dobras), só os pixels que atrapalham, com as cores que já estão ali (a G refinada, `taverna/g2/retoques.py`) |
| A cabeça do freguês de costas como uma bola grande sobre um ombro pequeno (a G) | a cabeça desenhada do tamanho de quem está perto, o ombro baixo e estreito | de costas, a cabeça afunda nos ombros e a capa sobe até o queixo; a cabeça cabe umas duas vezes e meia na largura dos ombros |
| O barril do lado errado e o fogo na frente do balcão (o estudo livre de Morel) | a outra vista do mesmo lugar distribuída para encher o quadro | antes de desenhar, um esquema da sala (o que fica em cada parede, de que lado) e da câmera; o objeto muda de lugar na imagem, não na sala; o que fica atrás de um móvel vai numa camada abaixo dele (o fogo abaixo do balcão) |
| O taverneiro pequeno demais ao fundo; a borda da mesa por cima do braço de Morel | a escala escolhida pelo quadro, não pelo móvel; a mesa desenhada por último | a escala pelo móvel junto da pessoa (o balcão de 1,05 m dá o corpo inteiro, mesmo escondido); o braço que pousa no tampo passa por cima da borda, numa camada acima da mesa |
| A colher lendo como um pedaço da mesa que se soltou (o canto de Morel) | a colher de madeira nos tons do tampo, pousada ao longo da borda dele (os contornos coincidindo) | outro material e valor contra o apoio (o metal da caneca), e a pose de descanso fora das linhas do cenário (dentro da tigela, não na borda do tampo) |
| A colher buscando comida na borda da tigela; o cotovelo em cima da caneca (o canto de Morel) | o ponto de contato posto onde a pose pedia; os objetos sem folga para o braço | o contato dentro do alvo (o caldo, pela perspectiva da boca da tigela); a colisão resolvida no espaço (a caneca e a trajetória), conferida por conta em todas as poses, nunca invertendo camadas |
| A parede da esquerda lendo como outra parede de frente (o canto de Morel) | um ponto de fuga próprio para ela, escolhido para imitar as fiadas suaves da imagem gerada; o tampo atravessando-a | as linhas da lateral para o ponto da sala, as fiadas do canto na altura das do fundo, a diminuição pela profundidade, a mesa encostada ("Paredes laterais e cantos") |
| O braço da colher como uma faixa de couro junto do tronco (a vista de Morel) | o braço desenhado como um contorno só, colado ao peito | o braço de cima, o cotovelo e o antebraço como peças com direções próprias (o cotovelo é uma junta, com a dobra de dentro em sombra), e uma separação do peito por silhueta, sobreposição ou sombra |
