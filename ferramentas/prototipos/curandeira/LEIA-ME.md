# Protótipo: o interior da curandeira (candidata A)

28/10/2026, quarta passada. **Só no protótipo, esperando a avaliação do Jean.** O jogo não carrega esta pasta; a cabana do jogo
continua a tela de sempre, sem ambiente. Nada do templo nem da taverna foi começado. Feito pelo fluxo da skill
`arte-cenas-fenda`.

## Abrir

Dê dois cliques em `demo.bat` (ou `python ferramentas/prototipos/curandeira/demo.py` na raiz). O jogo abre no navegador
num **save temporário** (uma pasta nova a cada vez; os saves do Jean não são lidos nem tocados), na porta 8793: o
Guerreiro no Vau, com a campanha começada, um corte e uma mordida para tratar e 120 de ouro. Entre na **curandeira pelo
prédio da vila**. A faixa do alto troca o estado da história e mostra a pose parada:

| Botão | O estado (no save temporário) | Quem atende e o que a cena mostra |
|---|---|---|
| **Pita (Marta de cama)** | a chegada: a missão sem desfecho | Pita no almofariz ("mói ervas no lugar de Marta, que está de cama"); a cortina dos fundos fechada, sem mostrar Marta |
| **Pita (a água escura)** | a noite em que a fonte corre escura (Destruir, no mesmo dia) | Pita no almofariz; a panela fervendo forte e dois baldes de água junto do fogão ("ferve água para os doentes") |
| **Marta (de pé)** | a água limpou (Dar descanso, três dias depois) | Marta, magra, de lenço e mangas arregaçadas, no almofariz |
| **Pose parada** | — | a pose do movimento reduzido (o mesmo que a preferência do sistema): inclinada sobre o almofariz, a mão no pilão |
| **Moagem anterior** | — | a moagem da terceira passada (a volta contínua, 12 poses de um tique), sobre o mesmo cenário; de `anterior/terceira` |
| **Segunda passada** | — | a segunda passada inteira (os maços antigos e o giro só do braço); de `anterior/camadas`. Nenhum script escreve em `anterior/` |

A troca só vale com a cabana aberta: o motor muda o estado e abre a cabana de novo. O serviço é o de produção
(`Servicos.curandeiro`), sem mudar: os cartões, os preços, quem atende e a fala. As duas não aparecem juntas: pela
história, uma atende de cada vez.

## O levantamento

- **O que o jogo estabelece** (`rpg/consequencias.py`, `rpg/missoes.py`, roadmapIDEIAS/11, seção 3): Marta é a
  curandeira, ajudou o herói no passado e está de cama com a febre; Pita, a aprendiz, uma menina de uns catorze anos,
  atende no lugar dela, "mói ervas" e, na noite da água escura, "ferve água para os doentes". Marta volta a atender
  quando a água limpa, "ainda magra da febre", e "arregaça as mangas". Nenhum registro descreve rosto, cabelo ou idade
  de Marta: o lenço de linho e o vestido verde-escuro são aparência desta candidata, não história.
- **O serviço:** tratar ferimentos, um cartão por ferimento. Pontos da cena: quem atende (leva aos cartões, como o
  ferreiro) e a Saída (o Voltar).
- **O lugar:** uma cabana de trabalho, não um laboratório: a pia e os panos junto da porta, a água no balde, as ervas
  secando numa vara, a bancada com o almofariz, a tábua, o pote e a lamparina, as prateleiras de potes e frascos, o
  fogão baixo de pedra com a panela e a coifa, a passagem para o quarto dos fundos com a cortina (só cenário: atrás
  dela, o escuro), o armário de potes, a esteira diante do fogão; o meio do chão livre para circular.

## A composição e a escala

O quadro é o da forja (320×96): a câmera próxima, a sala de frente, quem trabalha na ponta da bancada, voltada para a
porta e para o almofariz. Escala pela figura: Marta tem 52 px dos pés ao alto do lenço (~1,65 m); a bancada tem o
tampo a 27 px do chão (~85 cm); o almofariz, 5 px. Pita é menor (46 px) e pega o pilão mais embaixo. A luz: o fogão
e a lamparina quentes, a porta fria, a sala escurecendo em degraus longe deles (a mesma luz feita por cima da forja).

## A atividade (terceira passada)

Uma rotina de trabalho, decidida pelos apoios antes dos quadros (o passo a passo está na skill, seção 5b):

| Trecho | Conduz | Acompanha | Fica |
|---|---|---|---|
| moer (voltas de 7 poses sustentadas; quarta passada) | a mão no pilão (a ponta de cima numa elipse) | o cotovelo; os ombros 1 px à frente onde o pilão vai longe e 1 px abaixo onde a pedra aperta; a cabeça, um quadro depois | os pés, o quadril, a saia, o almofariz, a mão de longe na borda |
| desacelerar | a última meia volta, dois tiques por pose, até o pilão parar de pé | — | — |
| olhar a mistura | o tronco: o peito à frente, depois o quadril para trás e o peito desce | o rosto vira para dentro do almofariz por último; o alto da saia vai com o quadril | a barra, os pés, a mão no pilão |
| a pitada | a mão: solta o pilão (encostado na borda de longe), tira uma pitada, sobe até o nariz | o corpo se endireita atrás da mão; a cabeça vem encontrar a mão | a mão de longe no almofariz |
| voltar | a mão afasta do rosto, desce e pega o pilão inclinado, que é a pose 1 do giro | a cabeça volta | — |

A volta ao começo não salta: a pega deixa o pilão onde a primeira pose da volta o tem. O braço tem comprimentos fixos
(o cotovelo é calculado; a mão fora do alcance é um erro do desenho), e o pilão tem o mesmo comprimento em todas as
poses. Marta e Pita fazem a mesma rotina no ritmo de cada uma: **Marta** (9,4 s) aperta nas pontas da volta, faz três
voltas (a última desacelera na metade), olha a mistura por 1,2 s e cheira com calma; **Pita** (8,8 s) faz quatro
voltas sem apertar, se inclina mais perto do almofariz e olha menos tempo. Pita trabalha **de pé num banquinho**: a bancada é a de Marta, e
no chão o almofariz ficava na altura do peito dela, com o braço esticado na altura do ombro.

O fogo e o vapor a 200 ms, como antes. Movimento reduzido: a pose de olhar a mistura, parada, com o fogo e o vapor
parados. A linha do tempo sai de `figuras.py` para `camadas/rotina.json` (o quadro de cada tique e a pose parada); a
tela só a lê.

## As fontes

- `botica.py`: os objetos da botica (os potes com o conteúdo, as tinturas, as velas, o alambique, os crânios, as
  proteções da porta, a enfiada).
- `desenho.py`: o ambiente em código (a sala, a porta, a pia, as ervas, a bancada e o almofariz, as prateleiras, a
  coifa e o fogão, a passagem, o armário, a esteira, a luz; o fogo, o vapor e os baldes; a frente).
- `figuras.py`: Pita e Marta (o corpo pelo contorno de cada linha, deslocado entre os ombros e o quadril; a cabeça em
  duas grades à mão por personagem; o braço por segmentos de comprimento fixo), as poses e a rotina.
- `exportar.py`: as camadas de `camadas/` e o `rotina.json` (a demonstração lê delas); com `--ver`, composições
  ampliadas numa pasta `conferencia/` para conferir o desenho (trabalho, não entrega, fora do repositório). Não
  escreve em `anterior/`.
- `anterior/camadas/`: a segunda passada exportada; `anterior/terceira/`: as figuras e a rotina da terceira. Congeladas
  para a comparação na faixa.
- `demo.py` e `tela/` (`cena-curandeira.js`, `curandeira.css`, `faixa.js`): a cena registrada ao lado da forja só na
  página da demonstração, a troca de estado e a faixa.

Ainda é desenho em código: se a candidata for aprovada, a fonte em Aseprite vem antes da integração (skill, seção 6).

## O que mudou durante o trabalho (o que a conferência pegou)

- Os braços de palito e o avental claro dominando a figura: o corpo redesenhado pelo contorno, braços com espessura, o
  avental num linho apagado.
- Os dois braços cruzados na frente do corpo liam como um "Λ": o braço que trabalha passou a ser o de perto (o que se vê
  inteiro); o de longe só aparece na mão que segura o almofariz.
- O almofariz longe do corpo deixava o antebraço reto como uma barra: ele foi para a ponta da bancada.
- O lenço cinza (e depois ruivo) lia como cabelo: linho claro com a linha do cabelo escuro na testa e o nó atrás.
- O vapor em grade de pontos e os maços fechando embaixo como cebolas: fiapos que sobem ondulando; maços estreitos no
  nó e abrindo para baixo, com a ponta irregular.

## Segunda passada (28/10/2026): a botica e o braço

**O que o Jean disse:** o lugar estava genérico ("um mato e potes genéricos"); queria mais personalidade, uma aura de
mandinga e de alquimia com coisas naturais (potes com coisas dentro), sem virar bruxaria. E o braço que mexe no
almofariz tinha poucos quadros perto do ferreiro, com um pedaço do avental virando braço e "sujeira de geração".

**O braço, quadro a quadro:** o antebraço era uma linha de 2 px em degraus, com buracos; o braço de cima sumia no
vestido; a dobra da manga estava na cor do avental (por isso lia como um pedaço dele); a mão de longe era um borrão.
Agora cada pedaço do braço é uma forma cheia (`figuras._capsula`: os pixels até o raio do segmento, luz em cima e
sombra embaixo em cada coluna), o braço de cima e a dobra da manga no pano do vestido, o punho de 3×3 em volta do
pilão (a ponta dele aparece acima da mão em todos os quadros) e a mão de longe como dedos por cima da borda do
almofariz. O giro passou de 8 poses a 200 ms para **12 poses a 100 ms** (o mesmo passo de quadro da forja), maior
(3 px para os lados), quatro voltas e a pausa.

**A botica** (`botica.py`), tudo natural e do ofício:
- na tábua de cima, a cobra enrolada no líquido âmbar, as sanguessugas na água turva (com o pano amarrado), a raiz em
  forma de gente e as velas escorridas, uma delas acesa (com a luz dela);
- na de baixo, os cogumelos secos, as tinturas com etiqueta (rubi, mel e turva), o crânio de passarinho e as penas num
  copo;
- na bancada, o alambique de vidro sobre a lamparina (o balão verde no tripé, o bico descendo até o frasco âmbar), no
  lugar do pote com o ramo;
- o crânio de cervo com a galhada na parede, entre a coifa e o esteio;
- a estrela de palha de proteção sobre a porta e o amuleto de osso, pedra furada e penas no batente;
- a enfiada de cogumelos secos na vara e um maço de bagas vermelhas entre as ervas;
- o caldeirão bojudo com a concha no lugar da panela retangular; no armário, um sapo seco no vidro e as etiquetas.

## Conferido

No navegador (Playwright), a 1920×945 e a 1280×720 (de novo depois da segunda passada, com 14 quadros seguidos da vista para ver o giro no jogo): a vila, a entrada pelo prédio, a cena nos três estados (quem
atende e a fala vindo do motor), a pose parada sem mudar, o ponto de quem atende levando ao cartão, um tratamento
cobrando pelo serviço de produção, o Esc de volta à vila, sem erros no console. A 1280, o segundo cartão de tratamento
pede rolagem, como os da forja.

## Para avaliar (Jean)

A composição e a identidade do lugar; Pita e Marta (aparência, proporção, leitura no tamanho do jogo); o gesto e o
ritmo; a noite da água escura (os baldes e a fervura); se a cabana deve trocar a tela de hoje quando for integrada.

## Terceira passada (28/10/2026): as ervas, o corpo e os rostos

**O que o Jean disse:** gostou da composição, da personalidade nova e dos objetos de alquimia natural. Os maços
pareciam pinhatas (volumes iguais, alinhados, diferenciados pela cor) e Pita e Marta mexiam só o braço, com o resto
parado: um trabalho robótico, que mais quadros do mesmo gesto não resolveram. Durante a rodada: o rosto e o cabelo
podiam ficar mais bonitinhos, com traços simples como os do ferreiro.

**As ervas** (`desenho.MACOS`): cada maço desenhado à mão por planta, com o barbante descendo da vara, a laçada por
cima e as duas voltas da amarração: a sálvia em leque (folhas de pontas para baixo, buracos entre elas, o verde
acinzentado de folha seca), a lavanda (hastes finas e a espiga roxa na ponta, em alturas diferentes), a réstia de alho
(cabeças brancas redondas na trança de palha), o raminho de bagas vermelhas (cachos de bolinhas com o brilho de um
pixel e duas folhas) e a camomila (talos curtos, as flores creme com o miolo amarelo). Comprimentos e espaços
diferentes; a enfiada de cogumelos continua na ponta da vara.

**O corpo:** a rotina descrita em "A atividade". O que a conferência pegou e mudou durante o trabalho: o braço da Pita
virava uma barra horizontal na altura do ombro (veio o banquinho e 2 px mais perto da bancada); as passagens trocavam
tronco, quadril, cabeça e mão no mesmo quadro (vieram as poses de passagem: o peito antes do quadril e do rosto; a mão
antes do corpo); a pega voltava o pilão para trás antes de começar a volta (o giro passou a começar na pose em que a
pega o deixa).

**Os rostos:** Marta com o lenço justo e o nó na nuca, o cabelo escuro na testa, a sobrancelha de 1 px, o olho atrás
da ponte do nariz, a face um pouco funda (magra da febre, sem exagero), a boca e o queixo; Pita com o brilho no alto do
cabelo, a franja de lado, a orelha, a bochecha corada de um pixel e o queixo curto. Nas duas, o pescoço agora cai no
colo do vestido (antes havia uma cunha escura sob o queixo). A aparência e a idade não mudaram.

**Conferido:** no jogo, a 1920×945 e a 1280×720: as ervas e as figuras no tamanho real; a vista quadro a quadro em
três estados (Pita, Marta, a água escura), um relógio só, a 100 ms, depois de sair e voltar três vezes; a pose parada
sem mudar; um tratamento em cada janela cobrando pelo serviço de produção; os nomes de quem atende e da Saída fora da
atividade; sem erros no console. A 1280, a faixa da demonstração cobre o alto da HUD (só na demonstração).

**Para avaliar (Jean):** as ervas no tamanho do jogo; a rotina das duas (o corpo, as pausas, a pitada, a volta); o
banquinho da Pita; os rostos. Compare com o botão **Passada anterior**.

## Quarta passada (28/10/2026): o ritmo da moagem

**O que o Jean disse:** gostou do cenário, dos ingredientes, da personalidade e da rotina; preservar. Jogando, o braço
do almofariz parecia mais contínuo que o resto do corpo e que a linguagem de animação do jogo. Pediu menos poses
intermediárias na moagem, as mais expressivas, a pressão sustentada, os tempos redistribuídos sem acelerar, o corpo
participando como antes e as pausas de olhar e cheirar mantidas. Nada de decoração nova nem caminhada.

**A volta:** 7 poses no lugar de 12, com a mesma duração (Pita 1,2 s, Marta 1,4 s): o pilão inclinado (1 tique); a
pressão longe do corpo, com o peito à frente e embaixo (Marta 3 tiques, Pita 2), e a mesma pressão com a cabeça
terminando de descer (3 e 2); a ponta passando na frente (2); do lado do corpo (2); subindo (2); de pé (1). A última
meia volta segura mais cada pose até o pilão parar. O relógio da cena continua a 100 ms; o fogo e o vapor, a 200 ms.

**Os contatos conferidos:** a mão de longe parada na borda do almofariz em todas as poses; a pitada saindo da boca do
almofariz com o pilão encostado; ao recuperar o pilão, a mão agora alcança o cabo antes de fechar nele (antes saltava
6 px num tique). O banquinho da Pita e a roupa acompanhando o corpo, como antes.

**No jogo, junto (1.217.0, fora do protótipo):** a cabana abre sem ferimento, com "Nenhum ferimento a tratar." na área
do serviço, e tratar o último não tira o jogador dela; os cartões dizem "Vida máxima −10%" (o atributo antes do valor).

**Conferido:** no jogo, a 1920×945 e a 1280×720 (a demonstração subida do zero em cada uma): os cartões, o clique duplo
tratando um só, o último ferimento pelo teclado (Tab e Enter) com o ouro, o ferimento e a vida máxima atualizados, a
cabana continuando com a cena e os pontos, os três estados sem ferimento, sair e voltar três vezes sem ferimento com um
relógio só, a pose parada, a moagem anterior, o Esc, sem erros no console.

**Para avaliar (Jean):** a moagem nova contra a anterior (botão **Moagem anterior**).
