# 20 — A primeira cena interativa: o ossuário e o sarilho (1.72.0)

Pedido de Jean (13/10/2026): começar a representação visual da campanha pela capela, com uma cena só: o ossuário, com
a interação do sarilho. Clicar no sarilho enquadra o mecanismo e abre as alternativas que já existiam; quem decide e
resolve é o motor; a cena mostra o resultado confirmado. A referência visual foi o protótipo da capela (artifact de
13/10), usado como linguagem (pixel inteiro, paleta curta, pontilhado, 10 quadros por segundo, câmera que aproxima),
não como regra nem como código.

## Decisões

- **Uma cena, um ponto.** Só o ossuário e só o sarilho. Nada de sala, encontro, recompensa ou pista nova; Passear e
  Explorar ficam como estavam.
- **Onde aparece:** na página da Capela Afogada, depois de o ossuário ter sido visto (a pista `correntes`), entre o
  cabeçalho do lugar e as escolhas. Só na tela gráfica: no terminal nada muda.
- **O ponto faz a ação do menu, não outra.** O sarilho manda a mesma escolha que "Soltar as correntes"
  (`missao` + `acao_missao` na meta da opção). Se a ação não está no menu agora, o clique não faz nada além de dizer
  por quê. Clicar não solta corrente, não gasta tocha nem flecha, não sorteia e não escolhe o método.
- **De perto:** depois do clique, a câmera aproxima o mecanismo (o pontilhado que se fecha, como a câmera da vila) e
  a cena "O Sarilho" abre com o enquadramento no tambor, na trava e nas correntes até o buraco, e as três escolhas
  de antes (à mão, o método da classe, deixar como está), com custos, riscos e testes iguais.
- **O motor diz o estado** (`missoes.cena_ossuario`): correntes `presas` ou `soltas` pelo preparo `corpo_solto`; o
  que o ponto faz (ou nada, com o estado escrito para quem clica). A tela não deduz.
- **A animação mostra, não decide.** A corrente só desce depois que o preparo foi gravado (`_soltar`), por uma
  celebração (`celebrar("correntes")`) que a tela gráfica recebe. Com luta (à mão, ou a trava que não cede), as
  correntes seguem presas na cena durante a luta e só descem depois da vitória. Fugir ou cair deixa tudo como
  estava: presas, e a ação de novo no menu.
- **Recarregar e carregar não repetem nada.** A página refeita (recarga do navegador) e o save carregado desenham as
  correntes já soltas, sem som e sem a descida.
- **Sem regra duplicada na tela:** nada de custo, teste, disponibilidade ou estado calculado no cliente.
- **Componente pequeno, não arquitetura:** `telas/cenas.js` registra o tipo `cena` com uma cena só (`ossuario`). A
  próxima cena entra no mesmo arquivo, com o mesmo contrato (o motor manda `cena`, `pontos` com `acao` e `estado`).
  Sem editor e sem formato genérico de cenas por enquanto.

## Implementação

- `rpg/missoes.py`
  - `cena_ossuario(g, mid, foco)`: o painel (`cena`, `correntes`, `foco`, `pontos`, `titulo`).
  - `mostrar_cena(g)`: manda o painel na página da capela; chamada em `Jogo.menu_selvagem`.
  - `_soltar_correntes` e a vitória da onda de afogados mandam o painel de perto (`foco="sarilho"`).
  - `_soltar`: grava o preparo e, só então, `celebrar("correntes")` (só na tela gráfica: `conquistas_na_tela`).
  - `opcoes()`: a meta de cada ação de missão leva `acao_missao` (o mesmo id), para o ponto achar a opção.
- `rpg/web/static/telas/cenas.js` (novo)
  - O ossuário em pixel art: 320×72 lógicos, pixel 2× (a largura acompanha a página, as paredes continuam dos lados).
    Paredes de pedra, abóbada, nichos com ossos, a escada do alçapão com a luz, a tocha que treme, ossos no chão, o
    buraco com água; o sarilho com postes, trave, tambor com a corrente enrolada, roda dentada com a trava, manivela
    e as duas correntes até o buraco.
  - O ponto clicável é um `<button>` sobre a arte: acende com mouse e com foco de teclado (o desenho fica dourado e o
    contorno tracejado aparece no foco), Enter e espaço funcionam, o nome "Sarilho" fica sempre à vista (não depende
    de passar o mouse) e o `aria-label` diz o que ele faz ou o estado.
  - A descida: 27 quadros (a trava erguida, o tambor girando, os elos correndo para o buraco, um tranco leve, as
    ondas na água) e o som novo `corrente`. Se a cena tiver saído da vista (o resultado empurrou a página), a página
    sobe até ela, a corrente desce e a leitura volta para baixo.
  - Movimento reduzido: sem tocha tremendo, sem aproximação animada e sem descida (as correntes aparecem soltas); o
    som fica, porque não é movimento. Som desligado: o de sempre (`App.som` não toca).
  - Tela baixa: se embaixo da cena não cabem as escolhas, a página do lugar começa na cena (o nome segue no painel ao
    lado). Na cena de perto, o texto puxa a página até as escolhas, como em qualquer cena.
- `rpg/web/static/app/nucleo.js`: a página do lugar com a cena não desce sozinha; a de perto segue o texto.
- `telas/celebracoes.js`: a celebração `correntes`. `som.js`: o som `corrente`. `css/08-mercado.css`: o palco, o ponto
  e o nome. `index.html`: o `<script>`.

## Validação

- **Testes:** `tests/test_cena_ossuario.py` (o ponto faz a ação do menu; de perto o ponto não age; só na capela e
  depois do ossuário; abrir e voltar não gasta nem celebra; a corrente desce só depois do preparo, com e sem a trava
  cedendo; fuga e derrota não soltam; o terminal sem celebração) e os de antes (`test_missoes`, `test_guardia`,
  `test_riscos_noite`).
- **Gabarito:** idêntico. Nenhuma das 24 partidas passa pela página da capela com o ossuário visto na tela gráfica, e a
  meta nova das opções não entra nas transcrições.
- **Fumaça:** `cenarioSarilho` ganhou o ossuário desenhado com as correntes presas, o mouse e o foco acendendo o
  sarilho, Enter e clique abrindo as mesmas alternativas sem gastar nada, e a volta com a sala de antes;
  `cenarioGuardia` confere a sala com as correntes soltas e o sarilho sem ação.
- **Conferido na tela (1500×950, 1500×700, 1280×800, 1280×700):**
  - o ponto com mouse e com teclado; a aproximação; "Deixar como está" sem gastar nada (tocha, flecha, hora);
  - o método da classe (paladino, sucesso no teste de Força): a corrente desce depois do resultado, com som;
  - o caminho à mão: a luta com as correntes ainda presas na cena, a vitória, a descida, a tocha gasta e a tarde;
  - a fuga (correntes presas, a ação de volta) e a derrota em nível 1 (resgate no Vau, correntes presas);
  - a recarga do navegador no meio da cena e depois dela, e salvar, sair e carregar: correntes soltas, sem som nem
    descida repetidos;
  - movimento reduzido (sem animação, com o som) e telas baixas (as escolhas à vista);
  - nenhum erro no console.

## Limitações

- A cena de perto, em telas baixas (1280×800 e menores), fica acima do texto e sai da vista quando o texto chega às
  escolhas; ela volta à vista sozinha só para a corrente descer.
- A recuada depois da fuga ("Você sobe pelo alçapão...") mostra a paisagem de fora, não o ossuário: é o texto de
  antes, e a cena da sala volta na página da capela.
- O mago e o arqueiro usam o mesmo desenho da descida; o tiro no pino e o ferro apodrecendo não têm animação
  própria.
- Jean ainda não viu: teste humano pendente.

## Como Jean testa

1. `ETAPA=fundo python -m tests.navegador.cenarios capela` (no PowerShell: `$env:ETAPA="fundo"; python -m
   tests.navegador.cenarios capela`). A página da capela mostra o ossuário com o sarilho e as correntes esticadas
   até o buraco.
2. Passe o mouse no sarilho (ele acende) e depois use Tab até ele (acende igual). Clique ou aperte Enter: a câmera
   aproxima e aparecem as três formas de sempre. Escolha "Deixar como está": nada foi gasto.
3. De novo pelo sarilho, escolha o método da classe. Se passar no teste, a corrente desce na cena depois do
   resultado. Se não passar, vem a luta: repare que as correntes continuam presas até você vencer.
4. Em outra rodada, desenrole à mão e fuja da luta: a sala continua com as correntes presas e "Soltar as correntes"
   volta ao menu.
5. Com as correntes soltas, recarregue a página (F5) e depois salve, saia e carregue: as correntes aparecem soltas,
   sem som e sem a descida de novo.
6. Para ver direto a sala com as correntes soltas: `$env:PREPARO="correntes"` antes do mesmo comando.

---

# A capela por partes: o exterior, o salão alagado e a escada (1.76.0)

Pedido de Jean (13/10/2026): continuar a representação da Capela Afogada por partes. Nesta entrega: a escada do
ossuário, o exterior, o salão alagado e a cena certa em cada momento da narrativa. Regras, custos, encontros,
recompensas, sorteios e progressão não mudaram; a sacristia e o fundo (com Ilse) ficam para a entrega deles.

## O mapa dos cinco ambientes

A sequência é a do jogo: **Exterior → Salão alagado → Sacristia → Ossuário → Fundo alagado**. Nenhuma sala nova, nenhum
mapa interno, nenhum sistema de navegação: cada ambiente é desenhado quando o motor manda (`g.ui.painel("cena", ...)`).

| Ambiente | O que tem | Arte | Ponto (a mesma ação do menu) | Onde aparece |
|---|---|---|---|---|
| Exterior | a capela afundada até a metade das janelas, juncos no antigo pátio, a porta da frente sob a lama, a torre sem sino, o canal entrando pelo buraco do muro, sapos na margem (alguns com patas a mais) | 1.76.0 | **Buraco no muro**: "Entrar na capela pelo buraco do canal" (etapa `capela`). **Sapos**: só olhar (aproxima e afasta) | a cena de chegada; a página do lugar até vencer o salão (também numa visita antes da hora, sem ação); o recuo pela brecha (fuga do salão ou da sacristia) |
| Salão alagado | a entrada pelo buraco do canal, água pelos joelhos, colunas, bancos podres, o altar, a fenda do piso perto do altar (por onde a água desce), a porta baixa da sacristia atrás do altar, um degrau acima | 1.76.0 | **Sacristia** (a porta): "Atravessar o salão alagado" (etapa `sacristia`) | a cena de entrada, com a água **inquieta** (as sanguessugas presas na madeira que sai da água; até a 1.77.0, também um afogado subindo); a cena da vitória, com a água **quieta** e o caminho dela à vista; a página do lugar depois de vencer o salão (e, até a sacristia ter arte, também na etapa `ossuario`, sem ação na porta) |
| Sacristia | acima da água, os cultistas, o livro, o baú, o alçapão para o ossuário; a escada de mão na janela alta | **planejada** | — | sem arte (como antes): a paisagem do lugar |
| Ossuário | a escada de pedra do alçapão, os nichos com ossos, a boca da escada que segue descendo ao fundo, o sarilho e o buraco redondo das correntes | 1.72.0 (escada refeita na 1.76.0) | **Sarilho**: "Soltar as correntes" (etapa `fundo`) | a cena da vitória na sala dos ossos (sem ação); a página do lugar depois de achar as correntes; "O Sarilho" de perto |
| Fundo alagado | a água pela cintura, as duas pedras de moinho, Ilse | **planejado** | — | sem arte (como antes) |

**Gatilhos** (`rpg/missoes.py`):

- `mostrar_cena(g)` (a página do lugar, só na tela gráfica): achadas as correntes, o ossuário; vencido o salão (etapa
  depois de `capela`), o salão quieto; senão, o exterior. O painel leva `pagina: true` e os pontos ativos só quando a
  ação vale agora (`_vale`, o mesmo teste do menu).
- `_capela_exterior` (chegada): o exterior, sem ação.
- `_nave`: na entrada, o salão inquieto; na vitória, o salão quieto (o texto da água e da vila logo embaixo).
- `_recuo(..., fora=True)`: a fuga do salão e a da sacristia terminam do lado de fora ("pela brecha"): o exterior. As
  outras fugas (ossuário, sarilho) seguem como eram.
- `_ossuario` (vitória): o ossuário com o sarilho, sem ação.
- Derrota: o resgate de sempre, fora da capela; a sala continua por vencer e a página volta ao ambiente da etapa.
- Nada disso grava estado: a arte lê a etapa, as pistas e os preparos que o motor já tem. Recarregar ou carregar
  redesenha o mesmo ambiente, sem som nem animação de conclusão.

## O que entrou nesta entrega

- **A escada do ossuário:** a boca do alçapão na abóbada, com a luz de cima; dez degraus de pedra, cada um com o piso
  claro, o espelho de frente e a quina, um abaixo e à direita do outro, apoiados num maciço de pedra em blocos até o
  chão. Logo depois do último degrau, a boca retangular no chão por onde a escada continua descendo até a água (o
  caminho de quem desce), separada do buraco redondo por onde passam as correntes. A tocha mudou para o lado da
  escada. O resto do ossuário e a animação das correntes ficaram como estavam.
- **O exterior** (`baseExterior`, `desenharExterior` em `telas/cenas.js`): o céu e o astro das paisagens
  (`Vista.ceuDo`: o período e o clima), a outra margem com árvores mortas, a névoa rasteira, a capela com o reflexo,
  o canal reto até o buraco, a beira de cá. Animação: nuvens, a água do brejo, a correnteza do canal entrando no
  buraco, estrelas à noite, os sapos piscando. À noite, o luar clareia as formas o bastante para a capela não sumir.
- **O salão** (`baseSalao`, `desenharSalao`): os vãos com as janelas altas e os fachos de luz do período, o buraco do
  muro da esquerda com o pântano lá fora, as colunas, os bancos, o presbitério com o altar e a porta baixa da
  sacristia, a água com os reflexos e a fenda do piso girando. Inquieta: rodas na água, o afogado que sobe devagar
  entre os bancos (uns três segundos, o tempo do texto chegar nele) e as duas sanguessugas — só o grupo da sala, sem
  inimigo a mais. Quieta: o caminho da água à vista, claro na entrada e escurecendo de lodo até a fenda.
- **Os pontos:** o mesmo componente do sarilho. O nome fica sempre à vista; o ponto acende no mouse e no foco do
  teclado; Enter e espaço funcionam. Com ação: aproxima e manda a mesma ação do menu (o motor diz se vale; a tela não
  repete regra). Sem ação: diz o estado. **De olhar** (os sapos): aproxima a vista e mostra "Afastar" (que recebe o
  foco); afastar, ou clicar na arte, volta. Olhar não dá pista, não gasta tempo e não muda nada.
- **A rolagem:** o painel da página do lugar (`pagina`) não puxa a página; o painel dentro de um texto segue o texto
  até as escolhas, como antes fazia só a cena de perto do sarilho. Na tela baixa, a página do lugar começa na cena.
- `tests/navegador/cenarios.py`: `CHEGADA=1` deixa a cena de chegada por ver (com `ETAPA=capela`, ela abre ao
  carregar).

## O protótipo consultado

Do artifact da capela (13/10), lido como referência de linguagem, não como regra:

- **Reaproveitado:**
  - a vista de fora (`fora`): a composição, a torre com o campanário vazado, a nave com o rombo do telhado, as
    janelas cortadas pela água, o buraco no muro rente à água, a fachada com o alto da porta sob a lama, o reflexo,
    o canal com as estacas, os juncos, as árvores mortas, os sapos e o desenho das nuvens, da água e da correnteza;
  - a nave por dentro (`dentro`): os vãos, as janelas com o céu da hora, os fachos de luz, o buraco do muro, as
    colunas, o presbitério, o altar, a água com os reflexos, os bancos e o redemoinho (aqui, a fenda do piso);
  - a câmera em dobro com o pontilhado que se fecha, e o destaque no mouse.
- **Deixado de fora ou mudado:**
  - o sarilho na nave (ele é do ossuário);
  - o azul que pulsa na fenda depois de soltar as correntes (a fenda é um rasgo no piso, não um portal);
  - o "bafo frio" azulado saindo do buraco (seria um sinal sobrenatural antes de o texto falar dele);
  - os textos e as ações de teste do protótipo;
  - os pontos de torre, porta e canal (não são ações da campanha);
  - os sapos foram redesenhados maiores, para as patas a mais aparecerem na aproximação;
  - a porta baixa da sacristia foi acrescentada atrás do altar, um degrau acima.

## Conferido na tela

- 1500×950 e 1280×700 (e 1280×800 com movimento reduzido).
- O exterior e o salão nos quatro períodos (manhã, tarde, anoitecer, noite).
- A visita antes da hora (etapa `canal`): o exterior sem ação; clicar no buraco só diz o que é, sem cena nem avanço.
- A chegada, com o exterior.
- O buraco pelo mouse; o salão inquieto, a luta, a vitória com o salão quieto e a página depois dele.
- A fuga, com o recuo mostrando o exterior e a página de fora, e a nova tentativa.
- A porta da sacristia levando à cena da sacristia, que segue sem arte.
- Os sapos pelo teclado: aproximar, afastar e o foco de volta.
- A escada e a aproximação do sarilho.
- Guerreiro (paladino), mago e arqueiro do buraco à vitória.
- Salvar, sair e carregar no salão: o salão quieto, sem som.
- O movimento reduzido: o afogado já de pé, nada se mexe.
- Nenhum erro no console.

## Limitações

- A sacristia e o fundo ainda não têm arte; até lá, a página do lugar na etapa `ossuario` mostra o salão (o caminho),
  sem ação na porta, e a cena da sacristia, a do fundo e a coleta do lodo usam a paisagem de sempre.
- A luta usa a arena de sempre, não o salão desenhado.
- A derrota leva ao resgate como antes; não há uma cena da capela para ela.
- Clima de chuva ou neblina só escurece o céu do exterior (sem gotas).
- Os sapos de perto ficam pequenos: as patas a mais são um par de pixels claros de cada lado.
- Jean ainda não viu: teste humano pendente.

## Como Jean testa (1.76.0)

1. `$env:ETAPA="capela"; $env:CHEGADA="1"; python -m tests.navegador.cenarios capela`:
   - a chegada com a capela por fora; depois do Continuar, a página com o buraco e os sapos;
   - aproxime os sapos (clique ou Tab e Enter) e afaste.
2. Clique no buraco (ou use o menu): o salão com a água inquieta e o afogado subindo. Vença a luta: a água fica
   quieta e o caminho dela aparece. Numa outra rodada, fuja: o recuo mostra a capela por fora.
3. `$env:ETAPA="sacristia"` (janela nova): a página mostra o salão quieto com a porta da sacristia.
4. `$env:ETAPA="fundo"`: o ossuário com a escada nova; o sarilho de perto como antes.
5. `$env:PERIODO` 0 a 3 com qualquer um deles: manhã, tarde, anoitecer e noite. `$env:CLASSE="mago"` ou
   `"arqueiro"` para as outras classes.

---

# A capela no cenário principal (1.77.0)

Pedido de Jean (13/10/2026), primeira de três entregas: a cena da capela vinha como uma imagem dentro do texto, com
as ruínas genéricas da paisagem em cima. Duas imagens do mesmo lugar, e a de cima errada.

## Como ficou

- **Uma representação só, no topo.** O painel `cena` não põe nada no texto: ele troca a arte do topo (o canvas da
  paisagem, `#vista`) pelo ambiente da capela. Embaixo, só o título da cena, a descrição, a resposta e as escolhas.
  `Vista.usarAmbiente(a)` desenha o ambiente no lugar da paisagem, com a mesma câmera (o pontilhado ao aproximar), o
  mesmo destaque e a mesma cor de chão continuando para o pergaminho.
- **Os pontos** ficam numa camada sobre a arte (`#pontos-cena`), posicionados como os prédios da vila (a arte é
  desenhada com `object-fit: cover`). Só valem na página do lugar, fora da luta e com a arte no topo; o clique
  enquanto a página ainda corre adianta o texto, como na arte. O balão do nome tem o estilo dos prédios.
- **Quando sai:** a página vira (`nova_cena`) e o que vem depois não é um painel de cena (outro lugar, um menu, a
  sacristia, o fundo): a paisagem volta. O motor manda o painel logo depois do título da cena, antes de qualquer
  texto, para a arte não piscar entre os dois. Na página do lugar, `mostrar_cena` foi para o começo do menu.
- **Na luta:** a arte do topo vira o chão da arena como a paisagem viraria; com o ambiente, a luta do salão é no
  salão e a do ossuário no ossuário (o painel do ossuário passou a vir antes da luta também). A câmera volta à sala
  inteira e os pontos saem enquanto a luta dura; as cartas e as animações são as de sempre.
- **Tela baixa:** com o ambiente, a arte não se recolhe na faixa de 52 px ao rolar (é ali que se vê a sala, o sarilho
  de perto e a corrente descendo); a altura dela já é limitada a 22% da janela, e só o texto rola. A página do lugar
  refeita ao recarregar começa no topo, como a nova (antes descia até o fim).
- **O sarilho:** de perto, no topo; a corrente desce ali mesmo, com os trancos de antes, sem a página rolar até a
  imagem e voltar.

## Conferido

1500×950 e 1280×700: o exterior, os sapos de perto e Afastar, o buraco levando ao salão inquieto, a luta do salão e a
do ossuário (mago) com o ambiente de fundo e as cartas legíveis, a vitória com o salão quieto, o sarilho de perto e a
corrente descendo, recarregar com as correntes soltas (sem som), movimento reduzido. Fumaça completa.

## Limitações (até as próximas entregas)

- A sacristia e o fundo ainda usam a paisagem genérica; a página do lugar na etapa `ossuario` mostra o salão.
- Os nomes dos pontos ainda ficam sempre à vista; o afogado verde e o facho pontilhado do
  alçapão saíram na 1.78.0.

---

# Luz do ossuário e criaturas do salão (1.78.0)

Segunda entrega do mesmo pedido. Só desenho: a luz não muda o gasto de tocha, a emboscada nem os riscos; as
criaturas desenhadas não são inimigos (a luta, as cartas e o texto seguem iguais).

- **Ossuário:** saiu o facho pontilhado que descia do alçapão e se misturava com a luz da tocha. A tocha da parede
  foi para entre os nichos e o sarilho (`TOCHA`) e é a luz da sala: anéis quentes que tremem, e longe dela a sala
  escurece em degraus pontilhados (`escurecer`), de modo que a escada e os cantos ficam na penumbra e o sarilho
  continua legível. Do alçapão, só o que vem da sacristia: de dia, um cinza frio nos três primeiros degraus; à
  noite, nada. A escada e o mecanismo não mudaram.
- **Salão inquieto:** saiu o afogado verde subindo da água. As sanguessugas (`SANGUESSUGAS`) ficam presas na
  madeira que sai da água (o banco da frente, a perna de um banco de trás na linha d'água, o pé de uma coluna) e se
  esticam e encolhem devagar sem sair do lugar; com movimento reduzido, paradas. A água continua em rodas.
- **Salão vencido:** a água quieta com o caminho dela, sem criatura nenhuma (já era assim; conferido).

Conferido: a arte ampliada de dia e de noite; o salão inquieto, a luta com o salão de fundo e o salão quieto a 1280×700.

---

# Navegação entre as salas e os pontos (1.79.0)

Terceira entrega do mesmo pedido. A capela passa a ter **onde o personagem está**, separado do **passo da missão**.

## Como funciona

- **A posição** fica no registro da missão (`m["sala"]`): `exterior`, `salao`, `sacristia`, `ossuario` ou `fundo`
  (`missoes.sala_atual`). Ela vai no save. Um save de antes da 1.79.0 não tem a sala: ela vem do passo da missão
  (`SALA_DA_ETAPA`: a última sala vencida; antes do salão e depois da guardiã, do lado de fora), sem refazer nada.
- **A sequência física:** exterior ↔ salão ↔ sacristia ↔ ossuário ↔ fundo (`PASSAGENS`). Sem atalho: cada sala só
  leva às vizinhas.
- **Sala vencida:** passar por ela é uma opção do menu do lugar ("Entrar no salão pelo buraco do muro", "Sair pela
  brecha do muro", "Ir à sacristia", "Voltar ao salão alagado", "Descer ao ossuário pelo alçapão", "Subir à
  sacristia", "Descer ao fundo alagado", "Subir ao ossuário") e um ponto da cena com o mesmo endereço
  (`{"capela_ir": sala}`). Só troca a sala: sem luta, texto, Continuar, tempo, tocha, cura, recurso, recompensa nem
  pista. Os inimigos da capela são os das salas; andar não sorteia nada.
- **Sala por vencer:** entrar continua sendo a ação da missão, com o encontro, a tocha e o texto de sempre. Cada ação
  da capela agora vale só na sala dela (`onde` em `ACOES`): entrar no salão, de fora; atravessar para a sacristia, do
  salão; descer ao ossuário, da sacristia; o sarilho e a descida ao fundo, do ossuário; o lodo de Caspar, do ossuário
  ou do fundo.
- **Quem muda a sala:** vencer o salão, a sacristia, o ossuário ou a guardiã deixa o personagem nela. A fuga do salão
  e a da sacristia terminam do lado de fora (pela brecha, como o texto dizia); a do ossuário e a da onda do sarilho, na
  sacristia (pelo alçapão). "Voltar por enquanto", diante de Ilse, fica no ossuário. Chegar viajando, o resgate,
  explorar e acampar deixam do lado de fora. Carregar um save não simula viagem: volta à sala salva.
- **O que fica:** salas vencidas, correntes soltas, baú, pistas, Sigilo e desfecho não dependem de onde se está.
  Voltar do ossuário à sacristia e descer de novo mostra as correntes como estão. A luta com Ilse segue sem fuga.
- **O subtítulo da página** diz a sala ("Ruínas • Sacristia • inimigos Nv.3 • ..."); o título continua o do lugar. No
  terminal, as passagens são opções do menu como as outras.

## O que cada sala mostra

| Sala | Arte no topo | Pontos (só na página do lugar) |
|---|---|---|
| Exterior | a capela por fora (1.76.0) | **Buraco no muro** (entrar: a ação da missão ou a passagem), **Sapos** (só olhar) |
| Salão | o salão quieto, depois de vencido (1.76.0; inquieto só na cena da luta) | **Brecha do muro** (sair), **Sacristia** (a porta: a ação ou a passagem) |
| Sacristia | **fundo neutro** até a 1.82.1; desenhada na 1.83.0 (abaixo) | nenhum até a 1.82.1; porta, janela, livro e alçapão na 1.83.0 |
| Ossuário | o ossuário (1.72.0; luz na 1.78.0) | **Escada do alçapão** (subir), **Sarilho** (a ação), **Descida ao fundo** (a ação ou a passagem) |
| Fundo | **fundo neutro** até a 1.83.0; desenhado na 1.84.0 (abaixo) | nenhum até a 1.83.0; escada e lodo na 1.84.0 |

As cenas de texto usam a mesma regra: a luta da sacristia, a descida ao fundo, a guardiã, o desfecho e o lodo de
Caspar trazem o fundo neutro (antes, as ruínas genéricas), e nenhuma sala aparece no lugar de outra.

## Os pontos

- **Sem nome fixo** sobre a arte. O nome aparece, com um contorno de quatro cantos dourados em volta do ponto, com o
  mouse em cima ou com o foco do teclado (Tab).
- **Destacar interações** (opcional): na Ajuda (F1) ou com **F4**, os nomes e os contornos de todos os pontos ficam à
  vista. A preferência fica no navegador. Nenhuma instrução escrita sobre a arte.
- As portas, a escada e a brecha se reconhecem pelo desenho; tudo que a missão exige continua nas opções embaixo.
- **Os sapos:** o clique (ou Enter) aproxima a arte do topo e põe uma linha curta embaixo do texto, com o que se vê de
  perto e a chegada não disse (`OLHAR_SAPOS`); "Afastar" volta e tira a linha. Sem Continuar, tempo, recurso nem pista.
- Nada escondido, sem sorteio de clique e sem pista nova nos pontos.

## Conferido

1500×950 e 1280×700; guerreiro, mago e arqueiro; movimento reduzido. Do ossuário à sacristia (fundo neutro), ao salão,
à brecha, de volta pelo buraco, à sacristia e ao ossuário, pelo mouse e pelo menu, sem gastar nada nem mudar dia ou
período; a sala pendente pedindo o encontro; F4 e o botão da Ajuda; os sapos com a linha de perto; salvar e carregar
na sacristia; a fuga do salão e a da sacristia terminando fora; a derrota levando ao resgate (e a volta, por fora).
Fumaça completa (`cenarioCapelaSalas` novo). Testes novos em `test_cenas_capela.py` (`TestNavegacao`).

## Limitações

- A sacristia e o fundo não têm arte própria: o fundo neutro é provisório e não tem pontos.
- O destaque dos pontos vale só nas cenas da capela (a vila já mostra os nomes dos prédios).
- A sala não aparece no mapa nem no painel lateral; só no subtítulo da página.
- Jean ainda não viu: teste humano pendente.

## Como Jean testa (1.79.0)

1. `$env:ETAPA="fundo"; python -m tests.navegador.cenarios capela` (janela nova do PowerShell, ou
   `Remove-Item Env:SALA` antes, se sobrou de outro teste):
   - no ossuário, passe o mouse e use Tab: os nomes aparecem só no ponto da vez, com os cantos dourados;
   - F4 (ou a Ajuda, F1): todos os nomes e contornos; F4 de novo desliga;
   - clique na escada: a sacristia (fundo neutro); pelo menu, salão, brecha, e o buraco de volta. Repare que a tocha,
     o dia e o período não mudam;
   - volte ao ossuário e solte as correntes; suba e desça de novo: continuam soltas.
2. `$env:ETAPA="sacristia"`: fuja da luta da sacristia; a página fica do lado de fora, e entrar no salão é só passar.
3. `$env:ETAPA="capela"`: os sapos de perto, com a linha embaixo do texto, e Afastar.
4. `$env:SALA="sacristia"` com `$env:ETAPA="fundo"`: começar já na sacristia; salve, saia e carregue.
5. `$env:DESFECHO="descansada"`: a guardiã resolvida; desça até o fundo (fundo neutro) e suba.

## Planejado: a sacristia e o fundo com Ilse (feitos na 1.83.0 e na 1.84.0, no fim deste documento)

- **Sacristia:** acima da água, a lanterna, as prateleiras reviradas, o buraco na parede onde estava o livro, o baú
  embaixo do pano (aberto ou não, pelo estado), o alçapão para o ossuário e a escada de mão na janela alta. Pontos:
  a porta do salão e o alçapão (passagens).
- **Fundo:** a água pela cintura, as duas pedras de moinho, as correntes (presas ou frouxas, pelo preparo) e Ilse
  antes da luta; depois do desfecho, a água parada e clara (descanso) ou turva (destruída). Ponto: a escada para o
  ossuário. Nada disso entra antes de Jean pedir.

---

# Ajustes sobre a 1.79.0

Pedido de Jean (13/10/2026): quatro ajustes, preservando a composição, a navegação e as animações.

## A água atrás dos bancos (1.79.1)

- **O problema:** as rodas da água inquieta e o caminho da água quieta eram desenhados por cima da sala inteira, e
  passavam por cima das tábuas dos bancos da frente.
- **Feito:** os bancos (`desenharBancos`) vão também numa camada própria, recortada na linha d'água dos bancos da
  frente (`LINHA_BANCOS`, y 60): assentos, encostos e a parte das pernas acima da água. A cada quadro, a água animada
  é desenhada e essa camada volta por cima; as sanguessugas vêm depois, grudadas na madeira. O pé das pernas
  (abaixo da linha) continua embaixo da água. A animação, as cores e a composição são as mesmas.
- **Conferido:** a arte ampliada em quatro momentos da animação, inquieta e quieta (antes: as rodas atravessavam as
  tábuas; depois: passam atrás delas); a luta do salão com a sala como fundo da arena.

## Referência de iluminação para os próximos cenários

A luz do ossuário (1.78.0) é a referência para os cenários desenhados que vierem, a começar pela **sacristia** e pelo
**fundo com Ilse**. Não é uma regra de código (cada cenário desenha a sua luz); é o critério para desenhar e revisar.

1. **Uma fonte de luz que se identifica.** Quem olha sabe de onde vem a luz: uma tocha na parede, uma lamparina, uma
   janela, o céu. A fonte aparece desenhada (a chama, o vidro) e tem a cor dela (quente para fogo, fria para
   luar e dia nublado).
2. **Luz concentrada em volta dela.** Anéis de pixel inteiro, do mais forte (perto da chama) ao mais fraco, que tremem
   de leve com a chama (parados com movimento reduzido). Nada de facho pontilhado atravessando a cena nem de brilho
   espalhado por igual.
3. **Penumbra gradual longe dela.** A sala escurece em degraus de preto translúcido com o pontilhado de Bayer entre um
   degrau e outro (`escurecer` em `telas/cenas.js`): os cantos e o que está longe ficam na penumbra, não no preto.
4. **A leitura vem antes do clima.** O escuro nunca esconde o que importa: os objetos com ação (o sarilho), as
   passagens (a escada, a porta, a brecha) e quem está na sala continuam legíveis, com a forma inteira à vista. Se
   algo importante cai longe da fonte, a fonte muda de lugar (foi o que aconteceu com a tocha do ossuário), não o
   objeto.
5. **Luz secundária discreta e coerente com a hora.** O que vem de fora (um alçapão, uma fresta) é fraco, segue o
   período e some à noite; nunca um sol forte numa cena noturna.
6. **A luz é só desenho.** Ela não mexe em tocha, emboscada, risco nem em nada do motor.

**Cada ambiente com o que é dele:** nos interiores, tochas, lamparinas e janelas (a janela segue o período e o clima
lá de fora); nos exteriores, o período e o clima das paisagens (`Vista.ceuDo`), sem uma tocha inventada.

**Para a sacristia:** a lanterna dos cultistas (ou a que sobrou, depois da luta) como fonte, a janela alta com a luz do
período, a penumbra nos cantos das prateleiras; o alçapão e a porta do salão legíveis. **Para o fundo:** a tocha de
quem desce como fonte (o reflexo dela na água), a água pela cintura escurecendo para longe, as pedras de moinho e Ilse
legíveis na luz; depois do descanso, a água clara; depois da destruição, turva.

**O mercado (decidido nesta entrega: fica como está).** A banca do Vale já segue o mesmo princípio onde ele faz
sentido: a lamparina à esquerda do mercador é a fonte de dentro, e ao anoitecer e à noite a loja escurece em degraus
longe dela (`LUZ_DE_FORA` em `telas/mercado.js`). De dia, a luz principal é a da janela e da porta, como pede um
interior com janela. Trocar para a luz do ossuário também de dia escureceria a mercadoria (que precisa ser lida) e
destoaria da vila clara lá fora. Não foi redesenhada.

## O lodo se recolhe no fundo (1.80.0)

- **O problema (reproduzido):** com a navegação, "Recolher uma amostra do lodo" aparecia no menu do ossuário, mas o
  texto levava o personagem até a água do fundo.
- **Feito:**
  - A ação de Caspar vale só com o personagem no fundo (`onde="fundo"`). Os requisitos são os de antes
    (`_chegou_ao_fundo`: a febre no fundo ou depois de Ilse, Caspar ainda por responder; sem o frasco).
  - **Antes de Ilse:** "Descer ao fundo alagado" põe o personagem no fundo e mostra a cena de sempre, com Ilse ainda
    na água. Entre as escolhas dela (chamar pelo nome, lutar, voltar por enquanto) entra "Recolher uma amostra do
    lodo". Recolher não começa a luta: a amostra é recolhida (a página do fundo, fundo neutro), Ilse continua na água
    e as escolhas voltam, sem a amostra. "Voltar por enquanto" sobe ao ossuário (a sala registrada passa a ser o
    ossuário, como o texto diz). Descer de novo repete a cena, sem a amostra se ela já está no frasco.
  - **Depois de Ilse:** a amostra fica na página do fundo, aonde se chega pelas passagens; no ossuário ela não aparece.
  - O texto da coleta diz o que se faz estando lá ("Você se abaixa na água do fundo e enche um frasco...").
  - Iguais: a análise do mago (uma vez), a força da prova, o teste da denúncia, e nenhum tempo, tocha, encontro,
    recompensa ou sorteio na coleta. Quem já tinha o frasco (inclusive em save antigo) continua com ele, e nada é
    entregue de novo.
- **Conferido:** testes (`TestLodoNoFundo`), fumaça (`cenarioCapelaSalas`: a descida, a coleta sem luta, a volta ao
  ossuário sem tempo nem gasto, a escolha que some); a tela a 1280×700 com o mago.

## Sair da capela para acampar (1.81.0)

- **O problema (reproduzido):** exausto dentro da capela, o personagem caía na fogueira (que é lá fora) sem nada
  dizer que saiu; e a sala registrada continuava a de dentro (amanhecia no ossuário). O "Acampar" do menu tirava o
  personagem da capela em silêncio.
- **Feito:** uma saída só, `missoes.sair_para_acampar`, usada pelo menu e pela exaustão (`tempo.exausto`):
  - dentro da capela, a opção do menu se chama **"Sair e acampar"** (do lado de fora, o "Acampar e descansar até o
    amanhecer" de sempre);
  - antes da fogueira, a arte do topo passa à capela por fora e uma faixa conta o caminho de verdade, pela sala em que
    se está: "Você volta pelo caminho já aberto: sobe pelo alçapão, atravessa o salão alagado e sai pela brecha do
    muro para acampar, perto da capela." Exausto, a faixa é "Exausto", com "...para descansar". No terminal, a frase
    inteira ("Você está exausto. Volta pelo caminho já aberto...");
  - já do lado de fora, a exaustão segue com a faixa de sempre ("Não dá para seguir: é preciso acampar.");
  - a faixa passa sozinha (como a do "Exausto"): sem Continuar antes da fogueira; a arte da capela também não pede
    leitura (`ponte.painel`);
  - a sala passa a ser o exterior: o acampamento é lá fora, o amanhecer também, e a volta é pelas passagens abertas,
    sem encontro nem custo.
- **Iguais:** a passagem do tempo de cada ação, o descanso, o clima, as provisões, os eventos do acampamento e a
  comitiva. A saída não gasta período nem tocha e não tem luta, teste nem sorteio (o teste compara, com o mesmo
  sorteio, acampar saindo do ossuário e acampar do lado de fora: tudo igual). A exaustão continua no começo da volta
  seguinte do jogo, depois que a ação, a luta e as recompensas terminaram. Nenhuma fogueira dentro das salas.
- **Conferido também (os ajustes juntos), a 1280×700:** descer ao fundo, recolher a amostra, voltar ao ossuário, subir
  à sacristia, salvar, sair e carregar: a sacristia de volta, a tocha e o tempo iguais, e na nova descida a amostra não
  é oferecida de novo (o frasco ficou no save).
- **Conferido:** testes (`TestSairParaAcampar`), fumaça (`cenarioCapelaAcampar`), e na tela: a exaustão depois da luta
  do ossuário à noite (mago, 1500×950: a vitória, o Continuar do resultado, a faixa "Exausto" com a capela por fora
  no topo, a fogueira, o amanhecer); a saída manual do ossuário a 1280×700 e com movimento reduzido.

## Limitações destes ajustes

- (Resolvido na 1.81.1: "Explorar a região" de dentro da capela levava para fora sem contar a saída.)
- A faixa conta a saída por uns dois segundos e meio; quem quiser reler acha a frase no Histórico (H).

## Como Jean testa (ajustes da 1.79.0)

1. `$env:ETAPA="capela"; python -m tests.navegador.cenarios capela`: entre no salão e repare nas rodas da água
   passando atrás dos bancos, também durante a luta.
2. `$env:ETAPA="fundo"`: desça ao fundo, recolha a amostra (Ilse não levanta), volte por enquanto e desça de novo.
   `$env:CLASSE="mago"` para a análise. `$env:DESFECHO="descansada"`: a amostra na página do fundo.
3. `$env:ETAPA="fundo"; $env:PERIODO="1"`: "Sair e acampar" no ossuário; a faixa, a fogueira, o amanhecer fora.
4. `$env:ETAPA="ossuario"; $env:CLASSE="mago"; $env:PERIODO="3"`: desça ao ossuário e vença: a exaustão vem depois
   do resultado, com a saída contada.

## Explorar só do lado de fora (1.81.1)

- **Pedido de Jean:** "Explorar a região" só aparece do lado de fora da capela.
- **Feito (`missoes.pode_explorar`):**
  - o menu do salão, da sacristia, do ossuário e do fundo não tem mais "Explorar a região". Para explorar, sai-se
    antes pelas passagens; não há "Sair e explorar" nem saída automática;
  - o motor tem a mesma regra: `Jogo.explorar` não faz nada dentro da capela (um pedido de uma tela desatualizada ou
    de atalho não explora, não gasta período, tocha nem sorteio, e não leva para fora);
  - o tutorial (V5, que aponta "Explorar a região") só aparece do lado de fora; dentro, ele espera. A fala de Morel
    sobre explorar também só vem lá fora;
  - antes, escolher Explorar dentro levava para fora em silêncio; isso saiu junto com a opção.
- **Iguais:** "Sair e acampar", a exaustão, a navegação entre as salas; os outros lugares e o mundo gerado (fora da
  capela, `pode_explorar` é sempre verdadeiro).
- **Conferido:** testes (`TestExplorarSoLaFora`: as quatro salas e o exterior, o pedido atrasado sem gasto nem sorteio,
  o tutorial, salvar e carregar em cada sala); fumaça (`cenarioCapelaSalas`); na tela, as quatro salas e o exterior,
  salvar e carregar no fundo e voltar até a brecha, e o tutorial ligado: sem quadro dentro, o quadro do Explorar
  apontando a opção do lado de fora.

---

# A sacristia desenhada (1.83.0)

Pedido de Jean (13/10/2026): completar as artes da capela, a sacristia primeiro e o fundo com Ilse depois, em entregas
separadas. Nesta, a sacristia. Regras, custos, tempo, encontros, recompensas, equilíbrio e história iguais.

## O que a sala mostra

Uma sala pequena e seca (lajes de pedra, teto baixo), na mesma paleta das outras salas, um pouco mais quente por ser
seca (`baseSacristia`, `desenharSacristia` em `telas/cenas.js`):

- **A porta do salão**, à esquerda: o arco de pedra, a folha de tábuas aberta e, lá dentro, a água do salão mais
  embaixo, com o degrau descendo e a soleira (o "degrau a mais" do texto).
- **As prateleiras reviradas** pelos dois homens: uma tábua torta, um pote de pé e outro deitado, uma caixa aberta, o
  castiçal caído, cacos e três folhas no chão. Nada repetido.
- **A janela alta**, estreita, com o céu da hora (o mesmo das paisagens) e uma barra; **a escada de mão** de madeira
  encostada embaixo dela (montantes e degraus claros, diferente da escada de pedra do ossuário).
- **O buraco na parede** onde estava o livro, de pedras arrancadas (contorno irregular, uma pedra meio solta, duas no
  chão).
- **O baú pequeno de ferro** no canto, embaixo de um pano, com a quina e um rebite à vista.
- **O alçapão** no chão, em perspectiva, com a moldura de pedra, as tábuas, as dobradiças e a argola.

## Os estados (o motor manda: `missoes.cena_sacristia`)

| Momento | Quando | O que muda |
|---|---|---|
| `entrada` | a cena "A Sacristia", antes da luta | os dois vultos de capa escura e capuz (sem rosto, sem marca, sem símbolo): um nas prateleiras, de lado, com a faca baixa; o outro de frente, erguendo a lanterna. O livro ainda no buraco, embrulhado em couro |
| `luta` | logo antes da luta (um segundo painel) | eles são as cartas: a arte fica sem eles, com a lanterna no chão, acesa |
| `vitoria` | a cena depois da luta | a lanterna caída e apagada; o livro aberto no chão, embaixo do buraco; o baú ainda embaixo do pano (o texto chega nele e o motor o põe na bolsa) |
| `visita` | a página da sacristia (e o recuo do ossuário) | o baú já está na bolsa: o pano largado no chão e a marca do baú na poeira. Nada para pegar |

**A luz** (`luz` no painel e `luzSacristia` na tela), pela referência do ossuário:

- na entrada, a lanterna erguida (anéis quentes que tremem; com movimento reduzido, parados); na luta, a lanterna no
  chão;
- depois, a janela (o período lá fora: um peitoril claro e uma mancha fraca no chão, sem facho pontilhado; à noite,
  quase nada) e, se a luta acendeu a tocha de quem está ali, a luz dela vindo de perto da porta (`luz: "tocha"`,
  guardada em `Jogo.luz_na_sala` só para a cena seguinte; não vai no save). Na visita sem tocha, só a janela: a sala
  escurece menos e a porta, o peitoril e o alçapão ganham uma borda clara, para a leitura vir antes do clima, também
  à noite.

## Os pontos (só na página do lugar)

| Ponto | Faz |
|---|---|
| **Porta do salão** | "Voltar ao salão alagado" (passagem, sem custo) |
| **Alçapão** | "Descer ao ossuário" (a ação da missão, com a luta) enquanto o ossuário não foi vencido; depois, "Descer ao ossuário pelo alçapão" (passagem) |
| **Janela** | só olhar: "Uma escada de mão, de madeira, encostada na parede até a janela alta." |
| **Livro** | só olhar: "O livro da capela, no couro duro. O que ele conta, você já leu." |

Os de olhar aproximam a arte e põem a linha embaixo do texto, como os sapos: sem tempo, custo, pista ou repetição do
livro. Nomes no mouse e no foco; F4 mostra todos. Na luta e dentro das cenas, nenhum ponto.

## Conferido

- Testes: `TestSacristia` (os quatro momentos, a luz com e sem tocha, o baú uma vez, os pontos, olhar sem mudar nada,
  o alçapão como passagem depois do ossuário, a fuga do ossuário subindo com a tocha, a luz fora do save) e os de antes
  ajustados (a sacristia no lugar do fundo neutro).
- Fumaça: `cenarioCapela` (a vitória desenhada; carregado, o baú levado) e `cenarioCapelaSalas` (a escada sobe à
  sacristia; o livro pelo teclado; a porta ao salão; o alçapão ao ossuário). Gabarito idêntico.
- Na tela: a entrada, a luta, a vitória e a página nas três classes (guerreiro, mago e arqueiro), a 1280×720,
  1500×950, 1500×700 e 1280×600 com movimento reduzido; a fuga (o exterior) e a volta pelo buraco e pela porta; a
  derrota do mago (o resgate no Vau, a paisagem da vila no topo); a visita de dia e à noite; F4 e o mouse nos pontos.

## Limitações

- O vulto com a lanterna olha para a frente; quem olha "para o seu rosto" é o personagem fora do quadro.
- A tocha de quem está ali é uma luz vinda de baixo, à esquerda, sem o personagem desenhado.
- Jean ainda não viu: teste humano pendente.

## Como Jean testa (1.83.0)

1. `$env:ETAPA="sacristia"; $env:SALA="salao"; python -m tests.navegador.cenarios capela`: clique na porta do salão; a
   sacristia com os dois e a lanterna; na luta, só a lanterna no chão. Fuja: o exterior. Volte e vença: a lanterna
   caída, o livro no chão, o baú embaixo do pano.
2. Depois do Continuar, a página: o pano no chão. Passe o mouse na porta, na janela, no livro e no alçapão; F4 mostra
   todos. A janela e o livro só aproximam (Afastar volta).
3. `$env:ETAPA="ossuario"; $env:SALA="sacristia"; $env:PERIODO="3"`: a sacristia à noite, legível.

---

# O fundo alagado com Ilse (1.84.0)

Segunda entrega do pedido de 13/10/2026 (a sacristia foi a primeira). Regras, custos, tempo, encontros, recompensas,
equilíbrio e história iguais: só a arte do fundo, os estados que o motor manda e os momentos de Ilse.

## O que a sala mostra

Um poço baixo e escuro, na paleta das outras salas, mais frio (`baseFundo`, `desenharFundo` em `telas/cenas.js`):

- **A escada de pedra** do ossuário, no alto à esquerda, descendo degrau por degrau até sumir na água.
- **A água pela cintura**, escura, com rodas devagar e reflexos; o lodo escuro em manchas na beira (onde se recolhe).
- **As duas pedras de moinho** no meio, com o olho e os sulcos, saindo da água.
- **As correntes** descendo do buraco redondo do ossuário no teto (o mesmo buraco do sarilho, visto de baixo, com uma
  borda fraca de luz): **presas**, esticadas até as pedras e delas aos pulsos de Ilse, de braços abertos; **soltas**
  (o preparo `corpo_solto`), frouxas, com barriga, caindo na água, e um pedaço pendendo de cada pulso. Nenhum segundo
  sarilho.
- **Ilse** entre as pedras: silhueta de mulher com a água pela cintura, pele azulada, cabelo de algas caindo pelos
  ombros, o vestido escuro molhado. Sem brilho em volta, sem portal, sem Fenda.

## Os estados (o motor manda: `missoes.cena_fundo`)

| Momento | Quando | O que se vê |
|---|---|---|
| `descida` | "Descer ao fundo alagado" | Ilse de olhos fechados, presa ou solta pelas correntes; o momento `acorda` abre os olhos quando o texto chega em "Ela abre os olhos" |
| `visita` | a coleta do lodo antes dela; a página do fundo | antes do desfecho, Ilse acordada, cantando baixo (anéis na água); depois, o fundo sem ela |
| `luta` | logo antes da luta | ela é a carta: a arte fica sem ela (as correntes presas descem até a água entre as pedras), com a tocha se a luta a acendeu |
| `descanso` | a cena "Ilse" depois do rito | ela calma; `fita`: os braços dobrados, a fita entre os dedos; `afunda`: ela desce devagar e a água fica parada e clara |
| `destruida` | a cena "A Guardiã Destruída" | `desfaz`: ela se desfaz em bolhas e a água turva um instante, assentando; as pontas das correntes caem na água |

- `ilse`: `presa`, `solta`, `ausente` (na luta e depois do desfecho), `descanso`, `destruida`. `correntes`: `presas`
  ou `soltas`. `agua`: `clara` só na página depois do descanso; senão, escura (a turbidez da destruição é só o instante
  que o texto conta). `luz`: a tocha de quem está ali (`Jogo.luz_na_sala`, como na sacristia); sem ela, só o pouco que
  desce do buraco do ossuário, com a escada, as pedras e a beira com borda clara para a leitura vir antes do clima.
- **Os momentos de Ilse** são a celebração `ilse` (`missoes._ilse`), mandada logo depois do texto que os conta e só na
  tela gráfica: `acorda` (na descida), `canto_falha` (no momento do rito, na arena: um anel só na água, que para de se
  mexer; a escolha continua sendo o menu), `fita` e `afunda` (no descanso), `desfaz` (na destruição). Só mostram: o
  desfecho, o Sigilo, a veste e o rito são do motor, antes ou depois; nada se deduz da vida da carta. Recarregando ou
  com movimento reduzido, o fim do momento de uma vez (`Telas.momentoIlse`).
- Recolher o lodo antes dela não começa a luta nem muda a pose: a página da coleta é `visita` com Ilse na água.

## Os pontos (só na página do lugar)

| Ponto | Faz |
|---|---|
| **Escada** | "Subir ao ossuário" (passagem, sem custo) |
| **Lodo** | "Recolher uma amostra do lodo" (a ação de Caspar) quando vale; senão, só diz o que se vê |

Nomes no mouse e no foco; F4 mostra todos. Na luta e dentro das cenas, nenhum ponto ativo. Nada se pega no fundo
depois do desfecho.

## Conferido

- Testes: `TestFundo` (destruir com ela presa; descanso com ela solta; desistir do rito; cada momento logo depois do
  seu texto; a tela de texto sem momentos e com o mesmo jogo; a luta sem tocha sem luz; voltar por enquanto) e os do
  lodo ajustados (a coleta no fundo desenhado). Gabarito idêntico. Fumaça completa, com o fundo desenhado na descida,
  Ilse presa e acordada depois da coleta, e, carregado o save depois do descanso, o fundo sem ela, a água clara,
  nada animando de novo e os pontos escada e lodo.
- Na tela: a descida (olhos fechados e depois abertos, o canto), a coleta sem luta, a luta com a arena no fundo e Ilse
  só na carta, o rito (o canto que falha), o descanso (a fita, afundar, a água clara), a destruição (o desfazer, a
  turbidez, as correntes caindo), a desistência do rito, a página depois de cada desfecho (F4, escada, lodo), a
  derrota do guerreiro (o resgate no Vau); guerreiro, mago e arqueiro; 1500×950, 1500×700, 1280×720 e 1280×600; de
  dia e à noite, com e sem tocha; movimento reduzido; recarregar a página na descida, no descanso e na página depois.

## Limitações

- Recarregar a página no meio de uma cena mostra o fim dos momentos que o motor já mandou, mesmo que o texto ainda não
  tenha chegado neles (o texto também volta inteiro, como nas outras celebrações).
- O canto que falha acontece na arena, onde Ilse é a carta: a reação é só na água.
- Voltar por enquanto e descer de novo repete o texto da descida; os olhos abrem de novo junto com ele.
- Jean ainda não viu: teste humano pendente.

## Como Jean testa (1.84.0)

1. `$env:ETAPA="fundo"; python -m tests.navegador.cenarios capela`: desça ao fundo; Ilse presa, de olhos fechados,
   abre os olhos com o texto. Recolha o lodo (ela fica), volte por enquanto, desça e lute para destruí-la: a arena com
   o fundo, depois ela se desfaz; a página sem ela, com a escada e o lodo.
2. `$env:PREPARO="pronto"; $env:NIVEL="8"` (com `ETAPA=fundo`): as correntes soltas; chame Ilse pelo nome; no momento
   do rito, a água para; diga o nome: a fita, ela afunda, a água clara. Salve, saia e carregue: o fundo sem ela.
3. `$env:PERIODO="3"; $env:TOCHAS="0"`: o fundo no escuro, legível.

---

# Acabamento sobre a 1.84.0 (1.84.1 a 1.86.1)

Pedido de Jean (14/10/2026): continuidade visual, aproximações, detalhes de Ilse, o livro, o baú e a barra branca do
modal de equipamento. Regras, custos, progressão, encontros e recompensas iguais (a quantidade de baús também: só
mudou a forma de recolher o da sacristia). Cada problema foi reproduzido antes de corrigir; cada parte, um commit.

## De perto, sem a vista geral (1.84.1)

- **Reproduzido:** com F4 ligado, olhar a janela mostrava os quatro nomes da vista geral flutuando sobre a arte
  aproximada (o balão do F4, `visibility: visible`, vencia o `hidden` do ponto). Afastando pelo mouse, a janela
  ficava com o contorno pontilhado e o nome aceso mesmo com F4 desligado: o código devolvia o foco ao ponto, e o
  navegador o tratava como foco de teclado (a última tecla tinha sido o F4).
- **Feito:** de perto ficam só o objeto, o texto (ou o livro aberto) e "Afastar"; nenhum nome, contorno ou ponto da
  vista geral, com ou sem F4. Afastar devolve a vista geral com o F4 como estava. Três destaques separados: o global
  (F4), o do mouse (enquanto ele está em cima) e o do foco de teclado (`:focus-visible`); o foco que o mouse deixa
  não acende nada. Afastar pelo teclado devolve o foco ao ponto, visível; pelo mouse, nada fica aceso. Esc afasta.
- **Conferido:** janela, livro, sapos (1280×600) e o sarilho (a aproximação dele é a da ação: os pontos saem), com F4
  ligado e desligado antes, durante e depois; afastar pelo mouse e pelo teclado.

## O livro, o baú e a tábua (1.85.0)

- **O livro fica no buraco da parede:** embrulhado no couro antes da vitória; depois, desembrulhado ali, com o couro
  pendendo da borda. A vitória conta só o essencial ("Um padre anotou nele que Ilse guardava esta casa e o Sigilo do
  Turvo, deixado com ela pela Igreja. A vila a acusou de bruxaria e a entregou à água; o padre escreveu que ela não
  fez nada do que disseram. O Sigilo foi com ela."); as pistas continuam desta primeira vez. O ponto **Livro** abre o
  relato inteiro (`missoes.LIVRO_DA_CAPELA`, o texto de antes, sem nada novo) num livro aberto como o Grimório: Fechar,
  Esc, Enter, espaço ou o véu em volta fecham e devolvem a sala; as teclas do menu não escolhem nada embaixo. Reler
  não fala com o motor: nada de Diário, baú, tempo, recompensa ou sorteio. Não é item.
- **O baú** (de ferro, sem o pano: tampa abaulada, cintas com rebites, fechadura, ferrugem) fica no canto até ser
  recolhido. O ponto **Baú** e a opção **Recolher o baú** são a mesma ação (`bau`): entrega o mesmo baú, uma vez, pela
  bolsa como sempre, sem tempo, tocha nem sorteio; depois, o canto fica só com a marca na poeira e a ação some. Na
  entrada e na luta não se recolhe (a ação vale na página da sacristia vencida). A missão segue sem ele; dá para
  voltar depois. O estado fica na missão (`bau`: "no_canto", "recolhido"). **Saves de antes:** quem venceu a
  sacristia já recebeu o baú na vitória (aberto ou gasto); a migração 3→4 marca "recolhido" pela etapa da missão, sem
  olhar a bolsa. O gabarito mudou só no número do formato dentro dos saves (3 para 4).
- **A tábua de baixo da estante** partiu no meio: a metade da esquerda ficou no suporte, com a ponta lascada; a outra
  escorregou e ficou inclinada do montante ao chão, com sombra e o suporte vazio. O castiçal que estava nela caiu.
- **Defeito antigo achado no caminho:** depois de Sair → Carregar, a doca guardava "Sair" como tela aberta, e o menu
  da sacristia tem "Voltar ao salão alagado", que era tomado pelo Voltar dessa tela: clicar Sair levava ao salão.
  Uma passagem da capela não é mais um Voltar de tela, e o título fecha a tela da doca.

## A mesma sala sem saltos (1.85.1)

Reproduzido gravando, a cada quadro, o que estava no topo (ambiente, momento, Ilse, luz) desde a entrada real:

- **Sacristia:** nenhuma paisagem no meio, mas a lanterna da luta (no chão) reaparecia caída em outro lugar na
  vitória, e a luz da tocha sumia de uma vez na página logo depois. Agora a lanterna fica aos pés de onde o vulto
  estava e tomba ali, apagada; a tocha acesa na luta continua acesa na sala enquanto se está nela (`Jogo.luz_onde`,
  `missoes.luz_da_sala`; sai com quem sai, não vai no save; carregado, a sala volta sem ela).
- **Fundo:** a luta acabava e, durante a faixa da vitória e o espólio (uns 8 s), a arte ficava sem Ilse; depois ela
  reaparecia na resolução. Agora a vitória sobre ela chama um gancho do combate (`ao_vencer`, só dela): a arena sai e
  a resolução (descanso ou destruição) entra com ela presente, antes da faixa. O desfecho e a proteção contra
  recompensa repetida continuam em `_resolver`, gravados como antes: só o momento visual veio antes. Na luta ela
  continua só na carta. A sala vazia vem depois da fita e de afundar, ou de se desfazer (as correntes caem na água).
- **Na tela:** um painel novo da mesma sala não recomeça a cena. No mesmo acontecimento (o mesmo momento, Ilse e
  correntes) a animação continua; nos outros, a base de antes some numa mistura curta (280 ms, em degraus do quadro;
  instantânea com movimento reduzido), o que suaviza sobretudo a troca de luz.

## Ilse: o texto, o cabelo e o canto (1.86.0)

- **A descida conta as correntes como estão:** presas, "uma forma presa às pedras pelas correntes, que puxam os
  pulsos dela"; soltas, "uma forma na água. As correntes que você soltou pendem frouxas dos pulsos dela, sem prendê-la
  às pedras". "Ela ainda não se levantou da água" virou "Ela permanece entre as pedras, cantando baixo" (a arte a
  mostra pela cintura); depois da coleta do lodo, "Ilse não se mexe entre as pedras. O canto continua, baixo."
- **O cabelo:** mechas mais escuras e assimétricas (mais cheias à esquerda; à direita, um bolo de alga mais curto),
  uma mecha grossa descendo do alto da cabeça na frente do rosto e cobrindo o olho direito, outra fina cortando a
  face esquerda. Um olho à vista; a silhueta humana continua. A carta da luta segue o sistema de cartas (o ícone da
  espécie), como as outras guardiãs.
- **O canto** (`Som.canto`, sintetizado como o resto do som do jogo): uma canção de ninar sem palavras, melodia
  própria em poucas notas graves, lenta, num timbre abafado (triângulo com uma oitava abaixo, filtro baixo, vibrato
  lento). Um canal só: pedir de novo só muda o nível, nunca soma outro; passa pelo volume mestre (som desligado,
  silêncio). Entra quando o texto diz que ela começa a cantar (o momento `acorda`) e segue na coleta do lodo; na
  luta e na cena da destruição fica baixo; para quando o canto falha no rito; desistindo, o momento novo `grito`
  (logo depois de "o canto vira um grito") toca um grito curto e o canto não volta; no descanso já parou; na
  destruição para ao se desfazer; voltar por enquanto manda logo a arte do ossuário (antes ela ficava no fundo até o
  Continuar) e o canto para; sair da cena para. Recarregar refaz um canal só. Nenhuma fala nova nem pausa.

## A barra branca do modal (1.86.1)

- **Reproduzido** na entrega real do Broquel do Vigia (o guerreiro vencendo o ossuário), medindo a janela a cada
  quadro: quando a comparação entra, a largura do conteúdo passava 6 px da largura visível por uns 0,4 s. Causa: o
  cartão do que se usa entrava vindo de 24 px à direita (`achado-lado`), além do recuo de 18 px da janela; como a
  janela rola na vertical (`overflow-y: auto`, que leva o x junto), ela ganhava rolagem de lado nesse instante: a
  barra branca, nos sistemas com barra de rolagem clássica. Ícones e fontes não mudavam a largura.
- **Feito:** o cartão entra de dentro para fora (saindo de trás do achado), nunca além da borda. A rolagem vertical
  das janelas baixas continua; nada foi escondido. O Broquel, os atributos e as regras de equipar não mudaram.
- **Conferido:** o Broquel a 1500×950, 1280×600, 1280×480 (rolando na vertical) e com movimento reduzido; os anéis
  (dois espaços) a 1500×950 e 1280×600, e um anel com movimento reduzido: nenhum quadro com largura excedente.
  Uma guarda nos testes impede a animação de voltar a começar à direita.

## Conferido (o conjunto)

- Testes novos: `TestBauDaSacristia` (menu e ponto, uma vez, sem tempo nem sorteio, só na sacristia, a missão sem
  ele, salvar e carregar antes e depois, save antigo migrado), `TestContinuidade` (a resolução logo depois da luta,
  antes do espólio, com o desfecho gravado depois; a tocha que fica na sala e sai com quem sai), `TestDescidaConta`,
  o livro (ler não muda nada; a vitória resume e as pistas vêm dela), o `grito`, e a guarda do modal. Fumaça: F4 de
  perto, afastar pelo mouse e pelo teclado (Esc), o livro pelo teclado (as teclas do menu não passam), reler pelo
  mouse, o baú com clique duplo e salvar/carregar antes e depois, o canto entrando e parando ao voltar.
- Na tela: a sacristia da entrada à visita (entrada, luta, vitória com a lanterna no mesmo lugar, página com a tocha),
  o baú de dia e à noite, o livro aberto a 1500×950 e 1280×600; o fundo preso e solto, a coleta sem luta, o descanso,
  a destruição e a desistência gravados quadro a quadro (sem sala vazia antes da resolução); o canto em cada passo,
  com som desligado e recarregando.

## Limitações

- A mistura de luz anda no passo da animação do ambiente (dez quadros por segundo): são três degraus, no estilo da
  arte, não um degradê contínuo.
- O áudio só começa depois do primeiro toque que chega à página (uma tecla, um clique fora dos botões), como o
  resto do som do jogo; o canto pedido antes disso entra nesse toque.
- Carregar um save dentro da sacristia logo depois da luta mostra a sala sem a tocha (a luz não vai no save).
- Jean ainda não viu nem ouviu: teste humano pendente.

## Como Jean testa (1.86.1)

1. `$env:ETAPA="sacristia"; $env:SALA="salao"; python -m tests.navegador.cenarios capela`: entre na sacristia e
   vença; repare na lanterna e na luz entre a luta, a vitória e a página. Clique no livro (Esc fecha), no baú (vai
   para a bolsa, o canto fica vazio). Ligue o F4, olhe a janela e afaste: nada fica aceso depois de desligar o F4.
2. `$env:ETAPA="fundo"; $env:PREPARO="pronto"; $env:NIVEL="8"`: com som ligado, desça (o canto começa com o texto),
   chame Ilse, no momento do rito ouça o canto falhar; desista uma vez (o grito) ou diga o nome (a fita, afundar).
   Repare que, ao fim da luta, Ilse já está na arte.
3. `$env:ETAPA="ossuario"; $env:SALA="sacristia"; $env:CLASSE="guerreiro"`: desça e vença o ossuário; o Broquel abre
   sem a barra branca embaixo.
4. `$env:BAU="1"` com `ETAPA=ossuario` e `SALA=sacristia`: o baú ainda no canto, para recolher.

