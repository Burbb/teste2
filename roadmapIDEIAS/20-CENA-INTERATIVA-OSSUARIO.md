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
| Sacristia | **fundo neutro**: parede e chão no escuro, a luz no meio, sem objetos (sem arte própria) | nenhum: o caminho fica no menu |
| Ossuário | o ossuário (1.72.0; luz na 1.78.0) | **Escada do alçapão** (subir), **Sarilho** (a ação), **Descida ao fundo** (a ação ou a passagem) |
| Fundo | **fundo neutro** (sem arte própria) | nenhum |

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

## Planejado (não feito): a sacristia e o fundo com Ilse

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
