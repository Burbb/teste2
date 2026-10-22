# O Cão infernal e a Cria do Vazio (22/10/2026, propostas; nada no jogo)

**Pedido do Jean:** continuar a 1E.3 com duas propostas distintas para cada criatura, só no protótipo, depois de
conferir a identidade e os usos de cada uma; esclarecer no levantamento o servo do Necromante e o antagonista (sem
desenhá-los). Produção na 1.184.0; nenhum candidato autorizado para integração.

## A identidade e os usos (conferidos no código)

**Cão infernal** (`cao_infernal`, `rpg/dados.py`): "Cães de brasa com dentes de obsidiana. O fogo é a casa deles."
Traços `demonio` e `fera`; a Mordida Sangrenta (as "Garras", com sangramento) e a Bola de Fogo; resiste ao fogo (0,3),
fraco ao gelo (1,3) e ao sagrado; grupos de 1 a 3, a partir do nível 3. Vive na montanha e na Cidadela e é uma das
criaturas da Fenda (`CRIATURAS_DA_FENDA`: fora do bioma a partir do perigo 4). Hoje no sprite `demonio` (o diabrete
vermelho que o caído e o xamã usavam). **O retrato aparece:** na carta da luta (32), no Bestiário (48), no cartaz do
mural e no rastreador dos contratos de caça (48 e 32) e na faixa do mestre caçador.

**Cria do Vazio** (`cria_vazio`): "Pedaços da Fenda que aprenderam a andar. Quanto mais perto dela, mais delas." Traços
`corrompido` ("tocado pelo Vazio") e `etereo` ("armas físicas atravessam seu corpo"); a Esfera Sombria (à distância) e
o Toque Drenante (rouba vida); ataque de sombra; grupos de 1 a 2, a partir do nível 3; vive na Cidadela e é da Fenda
(perigo 4). Hoje no sprite `etereo` (o fantasminha azul). **Onde aparece:** os encontros comuns e os mesmos usos do cão
(carta, Bestiário, contratos, faixa); o evento dos refugiados ("Crias do Vazio surgem das sombras na retaguarda da
coluna!", duas); o do aprendiz que queria invocar um gato (uma cria com o nome "Gato do Vazio": o retrato é o da
família); a fala da Ponte de Varn (só texto). **A invocação do antagonista** (`instanciar_antagonista`,
`invoca="cria_vazio"`; o Invocar na fase de 66%): `_invocar` cria pela mesma função, `criar(..., "cria_vazio", nível -
2)`, então é a mesma família `cria_vazio`, com a letra e "(invocado)" no nome; o retrato será o mesmo (conferido em
Python e na foto `luta-invocada`).

**O que o projeto descreve × o que eu propus:** os dados dizem só o que está acima (pedaços da Fenda que andam;
corrompidos e etéreos; sombra e dreno) e, nas visões do Vazio, "o mundo perde a cor" e "um céu sem estrelas", narrados
em magenta. **Escolhas minhas:** o miolo escuro com a borda violeta e a Fenda em magenta; a A como um pedaço anguloso
da Fenda; a B como uma fera que anda (que também casa com o "Gato do Vazio").

**As duas pendências do levantamento:**
- **O servo do Necromante** (aliado, não é família inimiga): o Erguer Servo cria um `Aliado` "Esqueleto (Invocado)" e
  o talento Rei dos Mortos ergue o inimigo caído como "<nome> (servo)", ambos de `tipo` servo, sem traços nem família;
  a tela os desenha na `caveira` (`batalha.js`). A família `esqueleto_servo` existe no catálogo, mas nenhum código a
  cria. Fica fora da lista das famílias inimigas.
- **O antagonista** (família `antagonista`, só no mundo gerado; a campanha não tem): sem retrato próprio, cai no
  `humano` pelo traço `conjurador`.

## As propostas

**Cão infernal** (camadas corpo, brasa, boca, dentes, olhos). O corpo de carvão quente com a luz nos planos de cima (o
primeiro rascunho, de carvão escuro, sumia contra a caixa da carta); as rachaduras de brasa seguindo os volumes; a boca
acesa por dentro e os dentes negros de obsidiana contra ela, com um brilho frio azulado numa presa.
- **A, o que rosna de perfil** (`cao-infernal-a`): a cabeça para a esquerda, a orelha deitada para trás, o focinho
  comprido com o nariz, a mandíbula aberta com as presas negras em cima e embaixo; a rachadura sai de trás do olho,
  desce pela mandíbula e segue o pescoço. Na bancada, a cabeça cresceu (o pescoço ocupava metade do quadro) e a
  rachadura reta do pescoço passou a acompanhar a curva.
- **B, o mastim de cabeça baixa** (`cao-infernal-b`): de frente, as orelhas curtas para fora, o sobrolho escuro sobre
  os olhos acesos, o focinho com o nariz, o rosnado largo com as presas negras nos cantos, a rachadura no meio da testa
  e as brasas no pelo dos ombros. Na bancada, a boca de lado a lado fazia da cara uma caixa (sem focinho); com o
  focinho de volta e o rosnado largo, ela lê como cão.

**Cria do Vazio** (camadas corpo, fenda).
- **A, o caco da Fenda** (`cria-vazio-a`): um pedaço anguloso e irregular, como vidro escuro quebrado, atravessado por
  uma rachadura acesa em zigue-zague, com dois braços e duas pernas de caco. Na bancada, o primeiro era um losango com
  contorno magenta e uma fenda curta no meio: lia como emblema, e a fenda como um olho único (a construção do
  Espectro). A rachadura passou a atravessar o corpo todo.
- **B, a fera que anda** (`cria-vazio-b`): magra, de perfil para a esquerda, a cabeça baixa com um olho pequeno e a
  bocarra em fenda acesa, o dorso se desfazendo em fiapos e um buraco de vazio no flanco, as garras acesas. Na bancada,
  a primeira, de frente, era um bichinho de pelúcia com pernas de aranha; a de perfil com pernas finas (`CRIA_B_FINA`,
  guardada em `grades.py`, fora da exportação) virava um emaranhado na carta e ficou mais encorpada.

## A minha leitura (quem escolhe é o Jean)

- **Cão infernal: prefiro o A.** O perfil separa o cão do Lobo e do Lobo Gélido (os dois de frente) pela construção, não
  só pela cor, e a 32 a mandíbula aberta com os dentes negros contra a goela acesa é a forma mais legível.
  **Limitação:** a orelha única e o focinho fino lembram um chacal; o olho é um pixel.
  - B: a ameaça mais direta (os olhos acesos, o rosnado); **limitação:** é de frente como os lobos, e a distinção vem
    mais do carvão e da brasa; a 32 as orelhas e os olhos lembram um pouco uma coruja.
- **Cria do Vazio: prefiro a A.** A silhueta é única entre os retratos (nada de manto nem de olho), lê a 32 como um
  pedaço escuro rasgado com a Fenda acesa por dentro e casa com "pedaços da Fenda". **Limitação:** é abstrata (lê mais
  como "coisa" do que como criatura que anda), e a rachadura em zigue-zague pode ser lida como um raio.
  - B: mais bicho e mais legível como algo que anda (e casa com o "Gato do Vazio"); **limitação:** a silhueta de fera
    magra é comum, o violeta escuro pesa sobre a caixa escura e, a 32, o buraco do flanco é pequeno.

## Processo

- As grades à mão em `auxiliares/grades.py` (uma letra por pixel); as fontes pelo conector do Aseprite (`pintar.lua`,
  0 diferentes na releitura; o composto 175, 170, 164 e 148 = a soma das camadas); sem guia, porque nesta rodada não
  houve referência externa. A exportação (`python auxiliares/exportar.py`): igual à grade, o @2x exato, o 32 e o 48 em
  blocos inteiros do 16.
- As fotos a 1920×945 (`auxiliares/fotografar.mjs`, os modos atual, a e b, trocados só na página pelo nome): a luta do
  cão (com o lobo gélido, um caído e o xamã), a das crias (com o espectro e um cultista), as crias invocadas pelo
  antagonista (`auxiliares/cenario_vazio.py`: o `tutorial` dos testes com `ANTAGONISTA=1`, só no protótipo) e o
  Bestiário; sem erro no console.
- As folhas (`python auxiliares/prancha.py`): `cao.png` e `cria.png`, com o jogo de hoje × A × B na carta (real e 2×; a
  da cria também como invocada), no Bestiário (48), a fileira com os aprovados e a 12×.

# A segunda passada: a Cria A2 e o Cão T (22/10/2026, propostas; nada no jogo)

**A avaliação do Jean:** da Cria, a A é a direção (o caco flutuante, rachado, com a energia saindo de dentro), com uma
alternativa de mais volume nos planos sólidos; do Cão, o A e o B não foram escolhidos, e a imagem gerada `Cão infernal
em pixel art.png` (registrada no LEIA-ME das referências) passa a ser a principal. As A e B continuam aqui como estavam.

## A Cria A2 (`cria-vazio-a2`)

- **O problema da A:** o miolo escuro dos cacos se misturava ao fundo da carta, e a leitura dependia só da borda e da
  fissura.
- **O refinamento:** a silhueta, os fragmentos, a fissura e a paleta da A pixel a pixel (conferido); cada caco ganha um
  plano de luz violeta (`p`, 46356e) junto da borda de fora (o da esquerda em cima, o da direita no meio), e o escuro
  fundo fica junto da fissura, como a profundidade da abertura entre eles. Sem rosto, olhos, inscrições nem acessórios.
- Na bancada, um plano mais escuro (34284f) quase não se distinguia da A na carta; o 46356e continua escuro o bastante
  para a cria seguir etérea, e o centro aceso continua o ponto principal.

## O Cão T, a transposição da referência (`cao-infernal-t`)

- **A guia** (`guias/cao-infernal-t-guia-16.png`, a camada `guia` oculta na fonte, fora da exportação): o recorte
  quadrado de 1200 px a partir de (50, 40) da referência (1254×1254, ampliada; não é grade nativa), reduzido a 16 por
  média, sem esticar (75 px por pixel); a silhueta medida pelo alfa da referência no mesmo recorte.
- **Medido e redesenhado à mão:** a orelha dobrada no alto (colunas 2 a 5, linhas 0 a 2); a testa pesada como a faixa
  de luz (linha 4) sobre o sobrolho escuro (linha 5); o olho de trás em (3,5) e o da frente, estreito e aceso, em (8,6)
  e (9,6); o focinho largo nas colunas 0 a 6 com as rugas do rosnado; o nariz grande nas linhas 7 a 9 (cinza escuro com
  o brilho: o negro da referência sumia na caixa escura); a gengiva do lábio levantado; a goela acesa nas linhas 10 e
  11, cortada pela presa negra grande (coluna 5, linhas 10 a 12) e a da frente com o reflexo; a mandíbula e o queixo; a
  orelha de trás à direita com o vermelho dentro; o pescoço escuro com a rachadura em poucos pontos, da nuca até
  embaixo. A boca não vira faixa de dentes nem sorriso: a presa atravessa a goela na vertical.
- **Simplificado de propósito:** as rugas e as rachaduras da imagem viram três faixas de luz (a testa, o focinho, o
  lábio de baixo) e sete pontos de brasa.
- **Na bancada:** a primeira separava o rosto marrom e o pescoço de carvão como dois objetos, e o nariz negro sumia; o
  marrom virou luz em faixas horizontais sobre uma massa escura só, o nariz clareou para o cinza com o brilho, e a
  rachadura pontilhada do pescoço caiu pela metade.

## A minha leitura (quem escolhe é o Jean)

- **Cria A2:** os cacos passam a ter espessura e a fissura lê como a abertura entre eles, sem a cria ficar clara ou
  sólida demais. Prefiro a A2. **Limitação:** a 32 o ganho é discreto; a A continua disponível.
- **Cão T:** a construção da referência aparece a 48 (o Bestiário): o focinho largo com o nariz, os olhos estreitos sob
  a testa, a goela acesa com a presa negra, o pescoço com a brasa. **Limitação:** a 32 (a carta) a cabeça em três
  quartos fica pesada e escura; lê como uma cabeça rosnando, mas o "cão" depende do nariz e da boca, e a orelha dobrada
  lê como um tufo.

## Processo

- As grades em `auxiliares/grades.py` (`CRIA_A2`, `CAO_T`; as paletas `cria` com o `p` e `cao_t`); as fontes pelo
  conector do Aseprite (0 diferentes na releitura; o composto 164 e 178 = as camadas visíveis; a guia oculta no Cão); a
  exportação igual à grade, sem a guia, o @2x exato, o 32 e o 48 em blocos inteiros.
- As fotos no modo `c` (`MODOS=c`), a 1920×945, com os mesmos dados, sem erro no console. As folhas (`python
  auxiliares/prancha.py cria-a2 cao-t`): `cria-a2.png` (A × A2 na carta, como invocada, no Bestiário, a fileira e a
  12×) e `cao-t.png` (a referência, a guia e a T a 12×; o jogo de hoje × a T na carta e no Bestiário; a fileira).

## A Cria do Vazio no jogo (1.185.0)

- **Aprovada pelo Jean e integrada sem retoque:** a A2 (`cria-vazio-a2`, a fonte do `71e2c80d`), pela família
  (`RETRATO_FAMILIA`, o papel `CRIATURA` e os `TAMANHOS` em `icones.js`), com os afixos, o "Gato do Vazio" do aprendiz e
  as crias que o antagonista invoca (a mesma família). O antagonista continua no `humano`; quem só tem o traço etéreo
  (o Lich na fase 2), no `etereo`. A A, a B e a primeira B ficam aqui como histórico.
- A fonte em `ferramentas/arte/aseprite/retrato-cria-vazio/`, a cópia byte a byte; o 32 e o 48 em `DERIVADOS`.
  Exportados primeiro numa pasta temporária e comparados com a proposta (os seis, byte a byte iguais) antes de gravar
  no jogo; depois, `--conferir`: tudo igual ao jogo.
- Conferido a 1920×945 com os arquivos de produção (`capturas-1185/`, `auxiliares/fotografar_jogo.mjs`, com o
  `cenario_vazio.py` para a invocação): as crias com o espectro e o cultista, as crias invocadas pelo antagonista, o
  Bestiário, o cartaz e o rastreador; nenhum pedido a `ferramentas/`; sem erro no console. A folha:
  `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1185.png`.

