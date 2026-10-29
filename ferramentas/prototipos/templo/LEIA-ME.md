# Protótipo: o interior do templo (candidatas A e B)

28/10/2026. **A B é a direção escolhida pelo Jean** (a A fica como histórico); a segunda passada da B corrige o espaço
(seção "B, segunda passada"). **Só no protótipo, esperando a avaliação do Jean; a integração não está autorizada.** O jogo não carrega esta pasta: diante do templo, a
vila continua aproximada, com o balcão. Segundo interior da etapa 5 (Curandeira → Templo → Taverna; a taverna não foi
começada). Feito pelo fluxo da skill `arte-cenas-fenda`.

## Abrir

Dê dois cliques em `demo.bat` (ou `python ferramentas/prototipos/templo/demo.py` na raiz). O jogo abre no navegador
num **save temporário** (uma pasta nova a cada vez; os saves do Jean não são lidos nem tocados), na porta 8794: o
Guerreiro no Vau, com a vida em 40%, Odette na comitiva e ferida, 120 de ouro e o primeiro atendimento do templo por
usar. Clique no **Templo** na vila: a vista mostra o interior no lugar da vila aproximada, e o balcão de sempre fica
embaixo.

A faixa do alto:

| Botão | O que faz |
|---|---|
| **Candidata B / A (histórico)** | troca o interior (a demonstração abre na B; os pontos da cena acompanham) |
| **Ferido, 1º grátis** | o herói com 40% da vida e o primeiro atendimento por usar (o estado de abertura) |
| **Sem ouro** | o herói ferido, sem ouro e com o grátis já usado: o cartão apagado com o motivo |
| **Odette ferida** | só Odette precisa: o cartão "Cuidar de Odette" |
| **Ninguém precisa** | o balcão abre com "O templo está em silêncio. Ninguém aqui precisa de cuidados agora.", e o interior também |
| **Pose parada** | o movimento reduzido (o mesmo que a preferência do sistema) |

A troca de estado vale com a vila à vista (diante do templo, a faixa sai, troca e entra de novo).

## O levantamento (o que o jogo estabelece)

- **Quem atende:** "um clérigo" (masculino, sem nome), "cansado, de mãos firmes"; o balcão diz "Velas, incenso e um
  clérigo cansado, de mãos firmes." (`app/vila.js`). Ele trata "com unguentos e orações" (`servicos.templo`).
- **Os serviços:** cuidar da vida do herói (até o limite de agora, com os ferimentos) e de cada companheiro, um cartão
  por pessoa, cada um com o seu preço (`servicos.opcoes_templo`); o **primeiro atendimento do herói é grátis** na
  campanha ("O clérigo não cobra: é o seu primeiro atendimento aqui."). Depois de cuidar de alguém, o balcão continua
  aberto ("Mais alguém precisa de cuidados?") até a pessoa voltar à vila.
- **Sem ninguém precisando:** o prédio continua clicável e o balcão diz "O templo está em silêncio. Ninguém aqui
  precisa de cuidados agora." (`estado.predios_fechados`). Sem ouro: o cartão apagado com "Ouro insuficiente.".
- **Entrada, saída, tutorial:** o prédio da vila (o sino toca ao entrar), o Voltar à vila e o Esc; o quadro V2 do
  tutorial aponta o prédio ("O Templo recupera sua vida. Seu primeiro atendimento é grátis."). Nenhuma condição da
  campanha fecha o templo.
- **O exterior na vila** (`vista.js`): a igreja pequena, a nave de telhado de duas águas, o campanário à direita com
  o sino e a cruz no alto, a porta escura e **duas janelas estreitas e altas, acesas em amarelo quente** (a cor das
  janelas da vila; não há vitral colorido).
- **Para não confundir:** a capela afogada é outra igreja (abandonada, a água, as colunas, o altar com a cruz raspada,
  a janela grande atrás); o padre dela fugiu. O templo da vila é vivo, seco e cuidado.

Nada disso mudou: o protótipo não toca o motor nem o balcão.

## As duas candidatas (escolhas visuais, não fatos)

**A (a minha direção):** a nave vista de lado, com a câmera um pouco mais aberta que a da curandeira (o clérigo tem
~42 px): a entrada com a luz fria e o velário de ferro, os bancos (as cabeceiras de lado), as duas janelas altas da
fachada jogando o feixe de luz com pó, o canto de atendimento entre a nave e o presbitério (o catre, a mesa dos
unguentos), o presbitério um degrau acima com o altar, a cruz simples de madeira (a do campanário) e o incensário
pendurado, a base do campanário com a corda do sino. **O clérigo enrola ataduras** na mesa: as mãos giram o rolo, o
tronco recua no puxão de apertar, vai à frente para alisar a tira mais adiante (o braço não alcança sozinho) e, a cada
volta da rotina, ele pousa o rolo, endireita as costas e olha a nave (o cansaço).

**B (da referência do Jean):** a composição de `ferramentas/arte/referencias/cenarios internos/Interior do Templo da
Vila.png` (pedido do Jean, 28/10/2026), medida na escala do jogo com uma grade por cima e redesenhada na grade de
320×96: a nave de frente, o arco de pedra entre duas colunas, o presbitério dois degraus acima com o altar, a janela
alta e o castiçal de muitos braços; os bancos em dois blocos vistos por trás e a passadeira no corredor; a porta da rua
à esquerda com a luz do dia, a arandela e o banquinho; à direita, a mesa, o armário de potes, a porta lateral e a
mesinha do incenso; as silhuetas da frente. O clérigo tem ~31 px. **Não vieram da imagem:** os estandartes com cruz e
a cruz no avental (símbolos gerados; o jogo só tem a cruz do campanário), o vidro azul e amarelo (as janelas da igreja
são amarelo quente), as texturas, as sombras suaves e a aparência gerada do clérigo. **O clérigo dobra os panos
limpos** na ponta da mesa: pega um pano do monte (o tronco vai à frente), ergue, sacode, dobra, assenta na pilha,
alisa; a cada duas vezes, as mãos na beira da mesa, as costas sobem e ele olha a nave.

As duas: o clérigo é o mesmo do jogo (cansado, de mãos firmes, sem nome); a roupa (o hábito, o avental da B) é
escolha. A atividade é o trabalho do lugar (ataduras e panos para os unguentos), sem ritual nem efeito mágico. O
movimento do ambiente é discreto: as chamas a 200 ms, o incenso a 200 ms, o pó dos feixes (A) a 300 ms.

## A atividade pela skill (5b)

| | A: enrolar ataduras | B: dobrar panos |
|---|---|---|
| fica | os pés, a barra do hábito, a mesa, a tira estendida | os pés, a barra, a mesa, o monte e a pilha |
| conduz | as mãos girando o rolo | as mãos (pegar, erguer, dobrar, assentar, alisar) |
| acompanha | os cotovelos (comprimento fixo), a cabeça nas mãos, o tronco no puxão e no alcance | os cotovelos, o tronco (à frente para pegar), a cabeça |
| alcance | o rolo na ponta da mesa, junto do corpo; alisar a tira pede o tronco à frente e embaixo | o braço tem ~13 px: o trabalho fica na ponta da mesa; o monte pede o tronco à frente |
| ritmo | voltas de 4 poses de 2 tiques; apertar (4); alisar (5); a pausa de olhar (1,4 s); 8,5 s | cada pano em 21 tiques (pegar 3, erguer 3, sacudir 4, dobrar 3, assentar 3, alisar 5); a pausa (1,4 s); 6,2 s |
| pose parada | endireitado, as mãos na beira da mesa, olhando a nave | a mesma |

A conferência de alcance é uma conta no código (`cotovelo` falha se a mão não alcança): ela pegou o rolo longe demais
na A (mudou para a ponta da mesa, e o braço passou a ter a proporção humana).

## A interface

Diante do templo, a cena entra no lugar da vila aproximada (a vista mostra o interior; os balões dos prédios saem); o
balcão é o mesmo (os cartões, os preços, o Voltar, o Esc, as teclas 1, 2...). Os pontos da cena: **Clérigo** (leva
aos cartões, como o ferreiro) e **Saída** (faz o que o Voltar à vila faz). Na demonstração, a troca é feita pela
página (`tela/faixa.js`), sem mudar o motor: o templo não tem estado de história, e o balcão já é montado na tela.
Para integrar, a cena poderia vir do motor (como a da curandeira) ou ficar nessa troca da página: decisão para a
integração.

## Conferido

No navegador (Playwright), na demonstração, a 1920×945 e a 1280×720: o interior no lugar da vila com o balcão e os
pontos; cuidar da vida (o primeiro atendimento, grátis) e o balcão continuando com o interior; a candidata B; a Saída
da cena voltando à vila; ninguém precisando (o interior e o balcão abrem, com a frase); o Esc; sem ouro (o cartão
apagado); sair e voltar três vezes com um relógio só, a 100 ms; a pose parada sem mudar; sem erros no console.

## Limites (reais)

- Desenho em código, como a curandeira antes da aprovação: a fonte em Aseprite vem depois que uma candidata for
  aprovada (skill, seção 6).
- A B tem o clérigo pequeno (~31 px, a escala da referência): o rosto e as mãos são poucos pixels; a leitura da
  atividade vem do pano claro mudando de forma.
- A 1280×720, com o primeiro atendimento e Odette, o balcão leva os dois cartões e o Voltar à vista; com mais
  companheiros feridos, pediria rolagem (como hoje).
- Sem som novo (adiado). O tutorial V2 continua apontando o prédio na vila.

## As fontes

- `a/desenho.py`, `a/figura.py`: a candidata A (o ambiente, o clérigo, as poses e a rotina).
- `b/desenho.py`, `b/figura.py`: a candidata B (o ambiente reaproveita as cores e o pincel da A).
- `exportar.py`: as camadas de `camadas/a`, `camadas/b` e o `rotina.json`.
- `demo.py`, `demo.bat`, `tela/` (`cena-templo.js`, `faixa.js`, `templo.css`): a demonstração.

## B, segunda passada (28/10/2026): o piso, os planos e os apoios

**O que o Jean disse:** a composição está boa (a câmera afastada, o arco e o altar no centro, a janela quente, a
entrada à esquerda, os bancos, o atendimento à direita); o problema era a perspectiva e o apoio. O piso da direita
parecia a frente de um degrau ou uma parede baixa; clérigo, mesa, armário e porta terminavam numa faixa escura sem
chão à frente (flutuando ou grudados na parede); a roupa do clérigo se misturava ao pé da mesa.

**A causa:** tudo pisava na linha em que o piso começava (y 70), e o piso, em fiadas desencontradas de largura igual,
lia como as fiadas de uma parede. A referência gerada não resolve isso sozinha: a perspectiva precisou da conferência
própria.

**O que mudou** (`b/desenho.py`, o espaço conferido primeiro sozinho, `so_o_espaco()`):
- o piso contínuo da entrada ao atendimento: as juntas transversais mais juntas no fundo e mais abertas na frente, as
  longitudinais convergindo para o fundo da nave; a parede de fundo encontrando o piso em y 58, atrás de tudo;
- a elevação só no presbitério: o piso dele e o do degrau claros, as frentes dos dois degraus escuras; o altar como um
  bloco de pedra com a base mais larga apoiada no piso dele, a sombra no pé e a toalha só no alto; o castiçal de chão
  apoiado ali também; as colunas de pé no piso da nave, logo à frente dos degraus;
- o armário encostado na parede com o rodapé no piso logo à frente dela; a porta lateral e a da rua com a soleira; a
  luz do dia deitada no piso à frente da entrada; o banquinho e a mesinha do incenso com os pés no piso;
- a mesa dos panos mais à frente: o tampo (o claro de cima e a espessura), as pernas até o piso, a travessa, a caixa
  embaixo; os bancos em três fileiras pisando cada uma mais à frente, com o vão até o piso, as cabeceiras e um pé no
  meio; chão à vista entre as coisas;
- as sombras de contato de um pixel, depois da geometria;
- o primeiro plano só nos cantos; a caixa preta do meio saiu (os potes dos cantos viraram bancos na terceira passada).

**O clérigo** (`b/figura.py`): a mesa acaba em x 219 e a barra do hábito começa em x 220, com 2 px de chão entre o pé
da mesa e a roupa; o hábito passou a uma lã crua acinzentada (o pé da mesa é madeira escura e quente) e o pano ficou
mais claro que o avental. O monte e a pilha vieram para perto (o alcance: a conta do cotovelo pegou a pega no monte
0,3 px além do braço, e o monte veio 1 px, em vez de o braço esticar). Uma conta confere que nenhum pixel da figura cai
nas pernas da mesa em nenhuma das 8 poses do ciclo. A atividade, o ritmo e a participação do corpo são os de antes.

**Conferido:** o espaço sozinho e a cena inteira ampliados sem suavização; as 8 poses do ciclo, uma a uma; no jogo,
pela demonstração, a 1920×945 e a 1280×720: o interior no lugar da vila com o balcão e os pontos (Clérigo, Saída),
cuidar da vida com o balcão continuando, as duas candidatas, a Saída e o Esc, ninguém precisando, sem ouro, sair e
voltar com um relógio só, a pose parada, sem erros no console.

**Limites:** o rosto do clérigo continua de poucos pixels (a escala da referência); o piso não segue uma perspectiva
matemática exata (as juntas convergem para um ponto só e as transversais foram postas à mão), de propósito, pela
leitura no tamanho do jogo.

## B, terceira passada (28/10/2026): cada coisa com um motivo

**O que o Jean disse:** gostou; pediu para perguntar, de cada coisa na tela, o que ela é e por que está ali. Os postes
tinham "braços" só em alguns, e tortos; uma chama solta em cima do armário; ao lado da porta da rua, um sarrafo que
não lia como porta; outra chama minúscula perto do clérigo; os dois vasos pretos da frente, avulsos.

| O quê | Antes | Agora |
|---|---|---|
| os postes do vigamento | cinco, só dois com escora, tortas | cada um com a mão-francesa reta (45°) para cada vão que sustenta; os de canto, só para o lado do vão |
| a chama em cima do armário | sem vela | a vela num pires de latão em cima da cornija (a luz do canto do atendimento) |
| a chama perto do clérigo | solta junto da coluna | uma arandela de ferro com a vela, presa no poste; a da entrada no mesmo desenho, acima do banquinho |
| ao lado da porta da rua | uma tábua de 5 px | a folha da porta aberta para dentro, de quina: a ponta livre mais perto, as tábuas, as duas ferragens e a argola |
| a toalha | por cima das prateleiras | num cravo do lado de fora do armário |
| o primeiro plano | dois vasos pretos avulsos | as pontas da fileira de bancos mais perto de quem olha, cortadas pela borda, com a cabeceira dos bancos da nave |

O resto foi conferido com a mesma pergunta e fica: o altar com o livro e as velas, o castiçal de chão, a jarra e a
bacia (a água para limpar), a caixa dos panos, a mesinha do incenso, o banquinho de esperar, a passadeira.

**Conferido:** no jogo, pela demonstração, nas duas resoluções (o interior, os pontos, os serviços, a Saída e o Esc,
ninguém precisando, sem ouro, o relógio, a pose parada, sem erros no console).

## B, quarta passada (28/10/2026): construção e identidade dos objetos

**O que o Jean pediu:** preservar a composição e o piso; revisar a construção e a identidade: a estrutura de madeira
coerente, as portas reconhecíveis, o fogo com suporte e recipiente, um primeiro plano com propósito, a luz quadriculada
da entrada; poucos objetos legíveis, de um templo em uso; pode remover o que não ajuda, sem substituir cada coisa.

| O quê | Decisão |
|---|---|
| os postes de madeira rente à parede de pedra | **saíram** (não sustentavam nada que se visse); o frechal, a viga do alto que recebe o telhado, passou a apoiar em cinco mísulas de pedra saindo da parede, no mesmo espaçamento |
| a porta da rua | o vão de pedra em arco, como o da porta lateral (antes, um batente de madeira na pedra); o lado de fora em faixas chapadas (o céu, o muro ao longe, a neve), fora do escurecimento pontilhado da sala; a folha aberta fica |
| a luz da entrada | a mancha no piso chapada, de borda firme, em dois tons (mais clara junto da soleira); o pontilhado frio do piso saiu |
| a porta lateral | as duas dobradiças de ferro e a argola |
| o castiçal de chão | cada vela no seu copo, em cima da barra |
| o incenso | o fogareiro passou de uma caixa a uma tigela de ferro com a borda, as brasas e o pé; a vela solta ao lado **saiu** |
| o armário | **saíram** a toalha e a caixinha de cima; ficam os potes, a jarra e a vela no pires |
| o primeiro plano | **saiu**: as pontas de banco dos cantos não se alinhavam com os dois blocos de bancos (seriam um terceiro bloco fora do corredor); sem ele, o piso fica todo à vista |

As fontes de fogo, agora: as velas do altar nos castiçais de latão, as do castiçal de chão nos copos, as duas arandelas
de ferro chumbadas na pedra, a vela no pires em cima do armário e o fogareiro do incenso. Cada chama tem a vela ou as
brasas embaixo e o que as segura.

**Conferido:** os recortes ampliados (a entrada, o altar, o atendimento); no jogo, pela demonstração, nas duas
resoluções (o interior, os pontos, os serviços, a Saída e o Esc, ninguém precisando, sem ouro, o relógio, a pose
parada, sem erros no console). Integração não autorizada.

## B, quinta passada (28/10/2026): o arco, as vigas e os bancos

**O que o Jean pediu:** preservar o ambiente, os objetos e o piso; o encontro das vigas com o arco com apoio ou
sobreposição real (não um recorte seco); os bancos com tábuas retas, espessura consistente e fileiras na mesma
perspectiva (a redução pela distância, não deformação da madeira); no arco, a passagem do pilar para a curva e a
espessura interna com poucos planos, sem textura miúda.

- **As vigas:** cada uma termina antes do arco, com o topo da madeira aceso e a sombra dela na parede, em cima de uma
  mísula; entre a ponta e o arco, parede. As mísulas passaram a um espaçamento regular, com uma sob cada ponta. Antes, a
  viga acabava onde começava o desenho do arco, cortada.
- **O arco:** o pilar recebe a imposta (a pedra saliente onde o arco nasce); a face do arco sai dela com a mesma
  largura do pilar e se curva para dentro (abatido, como na referência; o alto fica acima do quadro), com as juntas
  das aduelas em raio; por dentro da face, o intradorso (a espessura da parede, mais escuro) continua pelo lado de
  dentro dos pilares até o piso. Três planos: a face, a espessura, a parede.
- **Os bancos:** desenhados pela mesma conta do piso (`pela_distancia`, o mesmo VP): as pontas de cada bloco seguem
  duas linhas que vão ao fundo, e a altura do banco e do encosto (duas tábuas retas, com a junta no meio) encolhem com
  a distância. A passadeira do corredor também segue o VP. Antes, as pontas e as alturas eram postas à mão, fileira a
  fileira.

**Conferido:** os recortes ampliados do arco e dos bancos; no jogo, pela demonstração, nas duas resoluções (as 20
checagens: o interior, os pontos, os serviços, a Saída e o Esc, ninguém precisando, sem ouro, o relógio, a pose
parada, sem erros no console). Integração não autorizada.

## B, sexta passada (28/10/2026): a altura dos bancos pela escala do clérigo

**O que o Jean perguntou:** se a altura dos bancos estava certa em relação ao clérigo. Não estava: medidos pela mesma
conta de distância do piso, eles tinham ~0,45 m (8, 10 e 11 px), a altura de um assento sem encosto. O clérigo, ~1,70
m, tem 32 px pisando em y 70: 1 m vale 28,2 px na borda de baixo do quadro (`METRO`). A mesa dos panos já estava certa
(0,74 m).

- **A altura:** os bancos saem de medidas em metros (`BANCO_ALTO` 0,90 m até o alto do encosto, `ASSENTO` 0,45 m) na
  escala do clérigo e pela distância: 18, 20 e 23 px, com o encosto de duas tábuas do alto até o assento.
- **O lugar:** com a altura certa, a fileira do fundo cobria os degraus e a base do altar; as fileiras vieram para mais
  perto (pisam em 72, 80 e 90), e os degraus aparecem pelo corredor, como na referência. O bloco da direita acaba antes
  do pé da mesa dos panos (o apoio dela continua à vista).

**Conferido:** no jogo, pela demonstração, nas duas resoluções (as 20 checagens). Integração não autorizada.

## B, sétima passada (28/10/2026): a simetria no eixo da nave

**O que o Jean perguntou:** por que os bancos de um lado eram mais compridos. Não era perspectiva (o ponto de fuga fica
no meio do corredor): o bloco da direita tinha sido encurtado para não cobrir o pé da mesa dos panos, e a cena ficou
sem razão para a diferença. Ele autorizou mexer no que fosse preciso para a simetria.

- **O eixo** (`EIXO`, x 134): o altar, a janela, a passadeira e o ponto de fuga já estavam nele; as colunas e o arco
  estavam 1 px fora e foram para ele. A convenção: o pixel x tem a imagem em 267 - x.
- **Os bancos:** os dois blocos com o mesmo comprimento, curtos; o da direita é o espelho exato do da esquerda. Os
  dois acabam antes do pé da mesa dos panos (à direita) e deixam livre a passagem entre a porta da rua e os bancos
  (à esquerda).
- **As mísulas, as pontas das vigas e as arandelas:** espelhadas no eixo.
- **Fica assimétrico de propósito:** o atendimento à direita, a porta da rua à esquerda e o castiçal de chão de um lado
  só (como na referência); a luz (que vem da esquerda em cada objeto).

**Conferido:** por conta, a forma das colunas, do arco e dos bancos espelhada no eixo, sem pixel fora; no jogo, pela
demonstração, nas duas resoluções (as 20 checagens). Integração não autorizada.

## B, oitava passada (28/10/2026): o corpo do clérigo sem quebra

**O que o Jean notou:** o corpo do clérigo "se quebra" quadro a quadro; dava para ver o encaixe.

**A causa (pose a pose):** a inclinação era feita fatiando o tronco (cada linha andava um pouco mais que a de baixo)
sobre uma cintura e um hábito parados. Na pega (o tronco 3 px à frente) e no olhar (1 px para trás), a frente do
peito, o avental e a amarra viravam degraus, e o tronco deslizava sobre a cintura. Da pega para o erguer, o tronco
ainda saltava 3 px num tique.

**A correção** (`b/figura.py`): o tronco, os ombros e a cabeça inclinam como um bloco; o hábito absorve a inclinação,
da cintura (levada pelo tronco) até a barra (parada no chão), numa diagonal suave, com um arredondamento só por linha;
a amarra vai com a cintura; a cabeça sobe com o tronco ao erguer. Uma pose de passagem (puxar o pano do monte, o
tronco a meio caminho) entre a pega e o erguer, na mesma duração.

**Conferido:** pose a pose, o contorno das costas sem degrau de mais de 1 px (fora a curva do pescoço para o ombro,
igual em todas); a sequência tique a tique; nenhuma pose encostando no pé da mesa; no jogo, pela demonstração, nas duas
resoluções (as 20 checagens). Integração não autorizada.
