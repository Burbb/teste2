# Etapa 2, primeiro lote: subida de nível, celebrações e raridade (protótipo)

**Nada disto está no jogo.** O jogo nunca lê `ferramentas/`; as propostas só existem nas páginas do servidor de teste
(a demonstração) e nas do fotógrafo. A base é a 1.200.1.

## Testar no navegador (a demonstração)

`demo.bat` (ou `python ferramentas/prototipos/hud/celebracoes/auxiliares/demo.py`) monta as direções e abre o painel em
**http://127.0.0.1:8765/**. Cada cenário abre em **B4 · Estouro** (o padrão pretendido) e **A4 · Relicário** (as
apresentações desta rodada, em destaque), no **jogo atual** ou no histórico (B3 e A3 aprovados, B2, A2, A, B, C
reservada, 1ª proposta, em cinza); um formulário troca a classe; cada especialização tem a sua linha. Cada botão encerra o cenário anterior e
sobe outro do zero, num processo com saves temporários (o save do jogo não é tocado); na página, "Começar o teste"; no
canto de baixo, "repetir" e "painel" (essa faixa só existe na demonstração). O servidor de teste (`cenarios_teste.py`,
`PROTOTIPO=<direção>`) serve `telas/celebracoes.js` e `telas/achado.js` montados em `prototipo-v2/<direção>/`.
Movimento reduzido: no Chrome/Edge, F12 → ⋮ → More tools → Rendering → "Emulate CSS media feature
prefers-reduced-motion" → reduce, e "repetir" (ou "Mostrar animações" desligado no Windows, para o sistema todo).

## Quarta rodada (24/10/2026): o selo dos itens no Estouro e as identidades das especializações

**Aprovado pelo Jean:** A3 e B3 (com a ressalva do selo dos itens no Estouro) e o Piromante nas duas apresentações.
As versões desta rodada são cópias: **A4 · Relicário** (`v2/relicario4.js`) e **B4 · Estouro** (`v2/estouro4.js`);
A3 e B3 ficam como referência aprovada.

**O selo dos itens (B4):** o miolo colorido e a proximidade da B2 voltam (o selo menor, a cor e a explosão abraçando o
item; o raro em ouro escuro), com só uma separação escura pequena em volta do sprite; o item no mesmo tamanho. Os
botões, o clarão concentrado, o acento do mágico e os outros acabamentos da B3 ficam. Conferido com dois raros e dois
lendários de silhuetas diferentes (peito, anel, pés, mãos; o cenário `itens_estouro`). Nível, Sigilo, especialização e
o Relicário não foram reabertos.

**As identidades** (`v2/identidades.js`; o piloto do fogo virou a primeira de seis). Levantamento do catálogo
(`rpg/classes.py`, SPECS, e as habilidades novas de cada uma) e a direção de cada uma, antes do desenho:

| Especialização | Tema no jogo | Paleta | Comportamento | O que a distingue |
|---|---|---|---|---|
| Piromante (aprovado) | A Chama Viva: Inferno, Combustão, Fênix | ouro, laranja, brasa | chamas nascendo do topo das letras e subindo; brasas | o único que queima: a forma sobe da letra |
| Paladino | Juramento da Luz: Golpe Sagrado, Prece, Julgamento Divino | branco, pergaminho, ouro velho | colunas de luz descendo sobre o nome e pulsando devagar; brilhos nas pontas das letras; partículas de luz subindo | o único que desce: luz vertical, calma, sem fagulha |
| Berserker | Pacto de Sangue: Sede de Sangue, Redemoinho, Fúria Cega | vermelho-sangue, quase preto | fissuras se abrindo dos dois lados do nome; sangue escorrendo e pingando da base das letras; um anel que bate como um coração (dois golpes e uma pausa) | o ritmo pulsado e o peso para baixo |
| Patrulheiro | Guardião das matas: companheiro animal, Fúria da Natureza | verde-folha, verde-escuro, marrom | rajadas de vento da esquerda para a direita levando folhas que giram, com riscos de vento | o único com movimento lateral, orgânico |
| Sombra | Irmandade da Sombra: Desaparecer, Flecha Envenenada, Execução | cinza-fumo, violeta escuro, verde do veneno | fumaça saindo das bordas das letras; véus de sombra rastejando para os lados; um corte de lâmina cruzando o nome de tempos em tempos; gotas de veneno | o contido e furtivo: quase sem cor, o corte como o único clarão |
| Necromante | O Sussurro do Túmulo: Drenar Vida, Erguer Servo, Maldição | verde-espectral, violeta, preto | almas com rastro vindo de longe em espiral e entrando no nome (o dreno); um círculo de maldição com runas girando em degraus no chão | o único que puxa para dentro |

Em todas: o nome estável, em faixas duras na cor da identidade, com a borda e uma sombra escura; os efeitos nas
bordas e em volta, sobre um poço escuro logo atrás do nome; a descrição, os ícones e o botão fora do alcance. Com o
movimento reduzido, cada uma tem um quadro parado próprio (as chamas, as colunas, as fissuras e gotas, as folhas, a
fumaça e o corte, as almas e o círculo). A identidade vale só para a celebração da especialização; as raridades, o
nível e o Sigilo não mudam. Escolhida pelo nome da especialização (o evento não manda o id; na integração, o id vem do
motor). Nas duas apresentações a identidade é a mesma; a apresentação muda a entrada (os raios girando do Relicário, o
estouro com a base escura do Estouro).

**Conferido:** as seis em 1920×945 e 1280×720 (a entrada aos 150 ms e a sustentação aos 2,6 s), no movimento reduzido;
o nome mais longo (Necromante, Patrulheiro) cabe nas duas. `auxiliares/gestos.mjs` nas duas: o de antes (tecla
segurada, Esc, clique duplo, clique e Enter rápidos, transição sem atravessar, limpeza dos efeitos, sem erros) e,
nas especializações, Sombra (Esc) e Patrulheiro (clique duplo; a escolha do companheiro vem depois e não é escolhida
pelo gesto): a festa fecha, o palco sai, nenhuma escolha mandada.

**Demonstração:** o painel tem uma linha por especialização (cada uma já na classe dela) e a dos itens do Estouro;
B4 e A4 em destaque, A3 e B3 aprovados para comparar.

**Vídeos** (`para-avaliacao/`, sem áudio; os anteriores ficam): `r4-0-estouro-itens-antes-e-depois.webm` (B3 e,
em seguida, B4, com os mesmos quatro itens), `r4-1` e `r4-2` (o Estouro: Piromante, Paladino, Berserker; Patrulheiro,
Sombra, Necromante), `r4-3` e `r4-4` (o Relicário, na mesma ordem). A faixa do canto diz a versão. Folhas em
`capturas-r4/`: `folha-r4-especializacoes.png`, `folha-r4-especializacoes-1280.png`, `folha-r4-itens-estouro.png`.

**Limitações vistas:** o som não foi ouvido; os efeitos são gerados em tempo real (cada repetição é um pouco
diferente); o corte da Sombra passa por cima do nome durante dois quadros (de propósito, é o "golpe"); no Paladino do
Relicário, as colunas e os raios claros juntos pesam mais no alto que nos outros; a identidade depende da fonte do
título carregada para achar o contorno das letras.

## Terceira rodada (24/10/2026): duas apresentações e a identidade do Piromante

**A decisão do Jean:** Relicário e Estouro ficam como duas apresentações disponíveis, com o **Estouro como padrão
pretendido**; a troca entre elas fica registrada para as futuras opções do jogo. Nada integrado nesta rodada. As
versões novas são cópias da A2 e da B2 (`v2/relicario3.js`, `v2/estouro3.js`); A2 e B2 ficam como histórico.

**Apresentação × identidade.** A apresentação (Relicário ou Estouro) faz a composição e a entrada; a identidade
(`v2/identidade.js`) diz as cores e o comportamento visual de uma especialização. Piloto só com o **Piromante**, nas
duas apresentações: o nome em ouro quente e laranja, em faixas duras, com a borda incandescente (o contorno vermelho e
brasa piscando em dois tons) e uma sombra escura; chamas pequenas desenhadas à mão (grades em cinco idades) nascem do
contorno de cima das letras (o texto desenhado num canvas com a mesma fonte, para achar os topos) e sobem pouco; um
poço escuro logo atrás do nome, com o calor de brasa na borda; os raios (Relicário) ou o estouro (Estouro) na paleta do
fogo, tremulando; brasas subindo. O corpo das letras fica parado; as chamas não descem sobre a descrição nem os
botões. Com o movimento reduzido, um quadro parado das chamas. As raridades, as outras especializações e as subidas
de nível seguintes não mudam; Patrulheiro, Sombra e as outras ficam para depois da avaliação do piloto e da conferência
do catálogo. A festa da especialização manda o nome, não o id: o piloto escolhe a identidade pelo nome; na integração,
o id vem do motor.

**O acabamento das duas:**
- **Clarão de entrada concentrado na origem** (`FX.claraoLocal`): um halo claro em volta do item ou do selo e só um
  pontilhado baixo na tela inteira por dois quadros (antes, a tela quase toda branca apagava o prêmio); no lendário, um
  escuro logo em volta do sprite. Vale para o lendário das duas e para o golpe do Estouro (o nível e o Sigilo).
- **Botões** (só nestas apresentações): ferro escuro com aresta de latão, sem o cinza em degradê; a tecla em destaque;
  mouse por cima, a aresta acende; o foco do teclado num anel claro; a área, os estados e os atalhos iguais.
- **Mágico:** um acento azul parado junto do item (o fio com o losango, em azul) além do brilho breve, sem aura.
- **Estouro, o título do nível:** a faixa de linhas douradas virou uma base preta irregular (o mesmo poço em
  pontilhado do Relicário); a estrela e o impacto ficam.
- **Estouro, o item no selo:** o miolo do selo é quase preto e maior, com um escuro em volta do sprite; as pontas e a
  energia ficam. O comum e o mágico também ganham um escuro atrás do item (ele caía sobre o texto da página).
- Em 1280×720, o Estouro abre mais espaço entre o selo e um título longo.

Os ícones antigos das habilidades (os sprites do Grimório) ficam registrados para a etapa do Grimório; não foram
redesenhados.

**Conferido:** 1920×945 e 1280×720 (nível, as quatro raridades, Sigilo, Piromante e a simulação de textos longos);
a leitura durante o clarão (os instantes de 60 e 200 ms) e durante as chamas; o movimento reduzido (a composição e o
fogo parados). Gestos, por `auxiliares/gestos.mjs` (na página, nas duas): a tecla segurada não fecha; Esc fecha o
nível 2 e o 3 abre; o clique duplo fecha uma festa só e não atravessa; nenhuma escolha mandada pelo clique que fecha
(nível e Sigilo, até 1,5 s depois); o clique e o Enter rápidos no achado levam os botões a ~85 ms sem escolher; os
palcos dos efeitos saem ao fechar (nenhum acumulado); a tela não fica deslocada pelo tremor; sem erros na página.

**Vídeos** (`para-avaliacao/`, sem áudio; os anteriores ficam): `r3-1-relicario-nivel-e-piromante.webm`,
`r3-2-relicario-raridades-e-sigilo.webm`, `r3-3-estouro-nivel-e-piromante.webm`, `r3-4-estouro-raridades-e-sigilo.webm`.
Folhas em `capturas-r3/`: `folha-r3.png` (A2, A3, B2 e B3 lado a lado) e `folha-r3-apertados.png` (1280×720 e reduzido).

**Limitações vistas:** o som não foi ouvido; no Estouro, os estilhaços da entrada da especialização passam por trás
da descrição durante ~1 s (atrás do texto, não por cima); seis ganhos ainda quebram em duas linhas; a identidade é
escolhida pelo nome da especialização (no protótipo); as chamas dependem da fonte carregada (sem ela, nascem do
contorno da fonte de reserva).

## Refinamento (24/10/2026): A2 · Relicário refinado e B2 · Estouro refinado

O Jean gostou da presença dos efeitos (os feixes do Relicário, o lendário e o Sigilo) e pediu para refinar A e B, sem
misturar as duas; a C fica reservada. As versões anteriores ficam como histórico (no painel, em cinza). O que mudou nas
duas (`v2/relicario2.js`, `v2/estouro2.js`; o comum em `v2/festas.js`):

- **Os itens no tamanho de uso:** o arquivo de 64 do cartão do saque, sem ampliar (antes, 128). O efeito continua
  grande e conduz o olhar ao item.
- **A informação sem molduras repetidas:** os ganhos numa linha (ícone, valor, nome alinhados; separados por fios ou
  pontos, sem caixas), o ponto de talento na mesma composição com o atalho (T), a habilidade nova pelo ícone do
  Grimório, nome e descrição (sem o retângulo roxo) e o Continuar dos botões do jogo, com a tecla (Enter). Sem a placa
  externa: os raios passam por trás da leitura num poço escuro em pontilhado (`FX.poco`), que une o alto e o pé.
- **A especialização:** o nome é o protagonista (grande, com o sol ou o estouro atrás), fora da medalha.
- **A comparação:** o nome do achado no alto, com a raridade; embaixo, numa peça só, três colunas: o prêmio, a troca
  (linha a linha, pelo `Telas.linhasTroca` do jogo) e o que você usa. O nome longo tem a largura da janela (uma ou duas
  linhas).
- **Comum e mágico:** o item fica junto da ficha; o comum entra sem aura (pousa com um pouco de poeira e um brilho
  só); o mágico tem um brilho breve e localizado (um anel curto e faíscas) que some. Raro, lendário e Sigilo continuam
  fortes.
- **A sustentação:** a entrada continua a mesma; depois de ~1,4 s, o efeito baixa um pouco e segue vivo (os raios em
  pontilhado mais aberto na A2; na B2, o selo respira, um pulso fino a cada 2,2 s e poucas brasas).
- **A2:** o rótulo de cima e a informação ficam sobre o poço escuro, ligados à medalha por um fio de latão com um
  losango.
- **B2:** o selo do impacto tem miolo escuro e aro de ouro (a mesma silhueta de pontas), o número em ouro sem o
  contorno grosso, a fita virou uma faixa reta de ferro com fios de latão; o achado é horizontal (o item no selo ao lado
  da ficha); o talento e a habilidade ficam lado a lado.
- **O ícone da habilidade:** a festa do jogo só manda nome e descrição, e a página ainda tem o estado de antes do
  nível. No protótipo, o servidor de teste acrescenta o ícone ao evento (`com_icones` em `cenarios_teste.py`); na
  integração, o campo entra no motor (`progressao.py`).

**Conferido:** 1920×945 e 1280×720 (casos reais e a simulação de textos longos), movimento reduzido, teclado (o foco no
Continuar; Enter fecha), clique duplo (fecha uma festa só), clique rápido (medido na página: ~85 ms até os botões, sem
escolher nada) e o clique que fecha a festa sem atravessar para o achado seguinte (medido na página: o achado abre
10 ms depois e os botões chegam no tempo normal). A folha `capturas-refino/folha-refino.png` põe A, A2, B e B2 lado a
lado; `folha-refino-1280.png`, as refinadas em 1280×720.

**Vídeos para avaliação** (`para-avaliacao/`, 1920×945, **sem áudio**: a gravação do navegador de teste não tem trilha
de som), cada um com o ciclo completo e uns 4 s depois de cada entrada:
`1-relicario-refinado-nivel-e-especializacao.webm`, `2-relicario-refinado-raridades-e-sigilo.webm`,
`3-estouro-refinado-nivel-e-especializacao.webm`, `4-estouro-refinado-raridades-e-sigilo.webm`. As sequências são
cenários de teste (`nivel_especializacao`, `raridades_sigilo`): festas reais encadeadas para caber num vídeo.

**Limitações vistas:** seis ganhos ainda quebram em duas linhas (5 + 1) nas duas; na B2, em 1280×720, os raios da aura do
lendário encostam no começo de um título longo; o som não foi ouvido; na A2, o mágico some rápido e pode passar despercebido para quem não
olha o item; os efeitos grandes continuam gerados por regra (as partículas são desenhadas à mão).

## Segunda rodada (24/10/2026): três direções

O Jean achou a primeira proposta contida demais: gostava dos feixes girando atrás, o problema era o acabamento de
vetor. Pedido: três direções completas, mais carregadas, em pixel art, com o modal livre para ser refeito.

### Referências vistas (imagens reais; nada copiado)

- **Vampire Survivors**, o baú (miniaturas de vídeos de jogo): feixes largos saindo em leque do baú, moedas voando e o
  prêmio subindo pelo feixe. Ensina que a luz pode nascer de onde o prêmio vem, que o excesso funciona se a moldura
  segura o centro, e que o ritmo cresce em degraus (quanto mais prêmios, mais fanfarra), sempre pulável.
- **Sea of Stars**, a subida de nível (captura da IGN): tela inteira escura, o título em cima, medalhões com halo em
  pixel e uma barra de números embaixo com os "+N" coloridos. Ensina a hierarquia título → símbolos → números, e que o
  fundo escuro deixa o brilho ser lido sem ofuscar o texto.
- **Diablo III**, o lendário (imagem do Diablo Wiki): uma coluna de luz da cor da raridade. Ensina que a raridade se
  lê de longe pela cor e pela forma (a coluna), antes do texto.
- **Pokémon (Gold/Silver/Crystal)**, a evolução (miniatura): raios de luz em volta do sprite, o momento cerimonial
  que segura a atenção e revela. Ensina o centro como altar e a luz como moldura.
- **Octopath Traveler**, o resultado da batalha: a cena continua visível e a lista dos ganhos fica de lado, em
  tipografia contida. Ensina a não esconder o mundo e a ler os números numa coluna.
- **Blasphemous**, o item recebido: uma faixa escura atravessando a tela com o nome em fonte gótica. Ensina a
  apresentação de "título de ato", sóbria e solene, que combina com o tom do The Unquiet.
- A busca no Game UI Database pedia verificação anti-robô; ficou de fora.

### As três direções

Todas usam o mesmo motor de efeitos (`v2/fx.js`): um palco de baixa resolução (texels de 3 px, ampliado sem
suavização, 15 quadros por segundo), só cores da paleta do jogo, degradê só por pontilhado ordenado e faixas de cor, e
partículas desenhadas à mão como grades de texto (cruz, estrela, brilho, lasca, caco, brasa). O comum de cada uma
(`v2/festas.js`): os gestos, a janela do achado e os textos (os ganhos com os ícones da HUD, o ponto de talento com o
atalho, a raridade num selo próprio e fora da linha do tipo). `auxiliares/montar_v2.py` junta tudo com os arquivos de
produção em `prototipo-v2/<direção>/`.

- **A · Relicário (cerimonial).** O ganho posto num altar: uma medalha em pixel com o número (ou o item, ampliado 2×)
  no centro de um sol de raios que gira devagar enquanto a janela está aberta (raios largos e finos em sentidos
  contrários, os que descem mais curtos), e embaixo uma placa com a moldura da HUD. Entrada: o clarão na medalha, o
  sol se abrindo, as faíscas; depois só o giro e um cintilar. Raridade = tamanho do sol: comum, só o halo; mágico, oito
  raios frios; raro, doze de ouro; lendário, dois sóis de brasa, o clarão e as brasas subindo.
- **B · Estouro (explosivo).** O ganho chega como um golpe: clarão de dois quadros, a tela treme, anéis de choque
  correm, linhas de velocidade e estilhaços voam e caem; o número bate (carimbo em quatro quadros) no meio de uma
  estrela de pontas, com uma fita vermelha atravessada. Ganhos em fichas grossas que estalam uma a uma. Depois, a
  estrela respira e solta brasas. Raridade = força do golpe: comum, poeira; mágico, anel e faíscas; raro, uma coluna
  de luz cai no item e quebra; lendário, a coluna larga, a tela pisca e treme, dois anéis e a chuva de cacos.
- **C · Estandarte (apresentação de palco).** Uma faixa de lado a lado da tela, como o título de um ato: abre de um
  corte de luz, barras de cinema escurecem o alto e o pé, e holofotes em pixel nascem atrás da faixa e varrem para
  cima e para baixo, cruzando-se; a luz vaza pelos fios. Na faixa: quem (o retrato do herói em 160 px, ou o item no
  pedestal sob a coluna de luz), o quê (o nível; o nome e a raridade) e o quanto (os ganhos; os números e a
  comparação). Raridade = luz do palco: comum, a faixa sem luz; mágico, uma coluna fria; raro, a coluna e dois
  holofotes; lendário, a coluna de brasa, cinco holofotes, as barras, o corte e as brasas.

### O que vale nas três

- **Ler sem esperar:** o nível, os ganhos, o item, a raridade e a comparação estão na tela desde o primeiro quadro; o
  efeito é em volta. Na B, só o desenho do item raro e lendário espera a coluna bater (160 ms).
- **Gestos:** o Continuar, o Enter, o Espaço e o Esc fecham a festa a qualquer momento; um clique fora durante a
  entrada a completa; não contam o toque que começou antes da festa, o 2º clique de um clique duplo nem a tecla
  segurada; o gesto não atravessa para a festa seguinte nem seleciona texto. No achado, um clique ou tecla durante a
  entrada a encurta e não escolhe nada (os botões ainda não estão lá).
- **Os botões do achado** chegam quando a entrada termina: medidos na página (1920×945, do cartão aos botões),
  comum / mágico / raro / lendário: A 0,22 / 0,34 / 0,49 / 0,64 s; B 0,21 / 0,28 / 0,43 / 0,57 s; C 0,23 / 0,32 /
  0,44 / 0,58 s; o jogo atual 0,55 / 0,55 / 2,3 / 2,7 s. Um clique logo que o cartão surge leva os botões a ~0,09 s
  nas três (medido na página: o fotógrafo clica tarde demais para mostrar isso).
- **Movimento reduzido:** a mesma composição parada (os raios, a estrela, os holofotes num quadro só), sem clarão,
  tremor, partículas nem entrada.
- **Telas baixas (1280×720):** A e B compactam a medalha, a estrela e as caixas; a janela rola se ainda faltar espaço.

### Cenários

`auxiliares/cenarios_teste.py`. **Casos reais** (pelos caminhos do jogo, sem mudar regras): um nível (dois lobos),
dois níveis seguidos (a Ilse e dois afogados), as quatro raridades (`gerar_equip` com a raridade pedida), o nível 4
da encruzilhada, o Sigilo (`receber_sigilo`) e a especialização (`especializar`). **Simulação** (identificada assim
no jogo e no painel): `limites`, uma festa de nível 12 com seis ganhos de dois dígitos e duas habilidades de nome e
texto longos, e um lendário de nome longo; não acontece nas regras, só testa a tela.

### Capturas

`capturas-v2/`: `folha-v2.png` (cada momento: o jogo atual, A, B e C), `folha-v2-ritmo.png` (o nível e o lendário em
seis instantes), `folha-v2-apertados.png` (1280×720 e movimento reduzido); por direção, `1920/` (vídeos `.webm` do
ciclo e os quadros), `1280/`, `reduzido/` e `rapido/` (o clique rápido). Refazer: `auxiliares/fotografar.mjs` com
`PROTOTIPO=<direção>` e `PULAR_TEXTO=1` (o texto de abertura adiantado por uma tecla), depois `auxiliares/folhas_v2.py`.

### Limitações vistas

- **Som:** é o atual (subir, achado, achado raro, fanfarra), tocado no primeiro quadro (na B, no impacto da coluna).
  Não foi ouvido nesta máquina; o sincronismo foi conferido pelos tempos do código, não pelo ouvido.
- **A entrada nas fotos:** o fotógrafo pega a janela 0,1 a 0,2 s depois de ela abrir; o clarão e os primeiros quadros
  só aparecem nos vídeos e na demonstração.
- **A:** o sol cobre a tela inteira, a HUD inclusive (de propósito); o comum tem só um halo discreto e pode parecer
  pouco ao lado do resto.
- **B:** o tremor move a tela inteira por ~0,4 s no nível e no lendário (no raro, menos); pode cansar se os níveis
  vierem em sequência. A fita vermelha e as fichas grossas puxam para um tom mais de fliperama que o resto do jogo.
- **C:** os holofotes que descem passam sobre o texto da página (escurecido); em 1920 a faixa fica larga e vazia nas
  laterais; o retrato é o busto do herói ampliado 2× (fator inteiro).
- **As formas grandes** (o sol, a estrela, os holofotes) são geradas por regra em baixa resolução; as partículas são
  desenhadas à mão. Se uma direção for aprovada, a medalha ou a estrela podem virar peças desenhadas no Aseprite.
- **Dois níveis seguidos:** cada nível tem a sua festa inteira; a segunda não é mais curta.
- **Fora deste lote:** a vitória, os contratos, o mestre caçador e as faixas continuam como no jogo.
- **Desempenho:** ~5 ms por quadro no pior caso (A, no navegador de teste, sem placa de vídeo); não medido numa
  máquina fraca.

## O levantamento (o que existe hoje; vale para as duas rodadas)

- **Como o jogador avança:** o XP vem das lutas (o quadro do espólio, `Jogo.abrir_espolio`/`ganhar_xp`), dos contratos
  e das missões; cada nível dá vida, recurso e atributos pela classe, um ponto de talento e, em alguns níveis, uma
  habilidade nova e o aviso da especialização. O motor manda o evento `celebracao` (`tipo: nivel`) com os ganhos
  prontos; vários níveis de uma vez viram festas seguidas.
- **A festa de nível** (`#celebracao`, compartilhada com o **Sigilo** e a **especialização**): raios cônicos em CSS,
  um anel borrado, partículas em `div` soltas, os ganhos com os sprites 16 antigos contando de zero, e as teclas
  ignoradas por 600 ms. O Continuar fechava; o clique duplo já fechava uma festa só.
- **As fagulhas soltas** (`particulas`): a mesma função na vitória, nos contratos, no Sigilo e na especialização.
- **O achado** (`telas/achado.js`): a raridade só na cor do nome e na linha do tipo ("Peito · Lendário"); raro e
  lendário esperam o feixe inteiro (1 a 1,4 s) e mais 0,55 a 0,9 s com o cartão sozinho antes da comparação e dos
  botões. Nada adianta isso.
- **O quadro do espólio:** já segue a regra do gesto (`Gesto`) e não muda neste lote.
- **Movimento reduzido:** quase não tratado (os raios e as partículas continuavam).


# Primeira rodada (23/10/2026): o Brilho (histórico)

Recusada como contida demais (24/10/2026); fica como referência no painel ("1ª proposta"), em `prototipo/` e em
`capturas/`.

## A proposta da primeira rodada

Uma direção só: **o efeito em pixel da HUD (o Brilho) e o ganho legível na primeira olhada**.

- **O Brilho** (`prototipo/brilho.js`): um canvas de baixa resolução (texel de 3 px, 15 quadros por segundo), com o
  pontilhado ordenado do `Sprites` e paletas agrupadas (ouro, mágico, raro, lendário, arcano, Sigilo). Uma aura em
  volta do que importa (o número do nível, a arte do item, o "Sigilo n/3") e um estouro curto; nada de disco ou coluna
  atrás de texto. Dura 0,9 s e apaga em degraus.
- **A festa de nível:** "Nível N" com o número carimbado; os ganhos em placas com os ícones da HUD (os vitais em 20, os
  atributos em 24), já com o valor final (sem contar de zero); o ponto de talento com o ícone dos Talentos e o atalho
  (T); a habilidade nova; a cascata leva ~0,6 s.
- **Os gestos** (sem bloqueio de clique e sem espera para clicar de novo): o Continuar, o Enter, o Espaço e o Esc
  fecham a qualquer momento; um clique fora durante a revelação só a completa; como no espólio, não contam o toque que
  começou antes de a festa abrir, o 2º clique de um clique duplo nem a tecla segurada, e o gesto que fecha não
  atravessa para a festa seguinte. A seleção de texto que o clique duplo deixava no botão da festa seguinte (no jogo
  também) sai.
- **A raridade no achado:** um selo com o nome da raridade abaixo de "Você encontrou" (a linha do tipo fica só com o
  espaço, sem repetir); intensidade proporcional: comum, só o cartão e as faíscas; mágico, a aura leve; raro, a aura e
  o feixe; lendário, a aura maior e o feixe. O cartão aparece quando o feixe bate (0,43 s), e um clique ou tecla
  adianta tudo (o gesto não escolhe: os botões ainda não estão lá).
- **O Sigilo e a especialização** usam o mesmo Brilho (paletas Sigilo e arcano); as fagulhas da vitória e dos
  contratos viram o estouro em pixel.
- **Movimento reduzido:** sem cascata, sem estouro, sem feixe; a aura fica parada, as informações e o selo iguais.

## Os números (do `registro.json` de cada pasta, 1920×945)

| Do anterior fechado até os botões | atual | proposta | proposta, movimento reduzido |
|---|---|---|---|
| comum, mágico | ~0,37 s | ~0,36 s | ~0,36 s |
| raro | 2,2 s | 1,2 s | 0,37 s |
| lendário | 2,8 s | 1,2 s | 0,37 s |
| raro/lendário com um clique logo que surgem (`rapido-*`) | 0,5 a 0,9 s | ~0,14 s | — |

A festa de nível chega no mesmo tempo nos dois (o motor manda); o que muda é que ela pode ser fechada na hora.

## As capturas

- `capturas/folha-estados.png`: cada momento, atual × proposta, em 1× (o meio da tela, 900 ms depois de aparecer).
- `capturas/folha-ritmo.png`: os cinco instantes (60, 250, 500, 900, 1600 ms), atual e proposta.
- `capturas/folha-apertados.png`: 1280×720 e movimento reduzido, atual × proposta.
- `capturas/<atual|proposta>[-1280|-reduzido]/`: os vídeos (`.webm`, o ritmo), o registro e os quadros de 250 e 900 ms
  (1920) ou de 900 ms (os outros); os demais instantes foram tirados depois de montar as folhas (refazer: rodar o
  fotógrafo e `auxiliares/folhas.py`).
- `capturas/rapido-<atual|proposta>/`: o clique rápido, em vídeo e registro.

## Os cenários de teste

`auxiliares/cenarios_teste.py` (**cenários de teste**, fora do jogo e de `tests/`): o herói a 25 de 30 XP no Vau e os
caminhos reais do motor. `nivel`: dois lobos (nível 2, Investida). `dois_niveis`: a Ilse (nível 3) e dois afogados
(do 1 ao 3, a festa duas vezes, o clique duplo na primeira, o Enter na segunda). `raridades`: quatro achados seguidos,
um de cada raridade, pelo `gerar_equip` com a raridade pedida. Nenhuma chance, recompensa ou progressão muda.

```
PLAYWRIGHT_MODULO=<file:// do index.mjs> PROTOTIPO=1 node auxiliares/fotografar.mjs <raiz> capturas/proposta
#   MOVIMENTO=reduzido, JANELA=1280x720; sem PROTOTIPO, o jogo atual; "rapido,rapido-nivel" para o clique rápido
python auxiliares/folhas.py capturas
```

## Limitações vistas no uso

- **O Sigilo e a especialização** não têm cenário aqui: usam o mesmo código e o mesmo Brilho, mas não foram
  fotografados. Nem as fagulhas da vitória e dos contratos.
- **O som** é o de antes (subir, fanfarra, o da raridade): nada foi feito para ele.
- **A aura do achado** é pequena a 1920 (o cartão tem 300 px); a diferença entre raro e lendário está mais no feixe e
  na cor do que no tamanho.
- **Movimento reduzido:** a aura parada ainda tem pontos em volta da arte (estáticos); se preferir nada, é tirar.
- **A especialização no nível 5** e uma habilidade de nome longo na festa não apareceram nos cenários; o nome longo
  de item ("Lamento do Corvo (Besta Leve Enferrujada)") quebra em três linhas no cartão, como no atual.
- Os tempos da tabela incluem as esperas do fotógrafo entre um gesto e outro (iguais nos dois lados).
