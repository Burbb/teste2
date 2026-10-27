# Protótipo: reforço, materiais, desmontagem e encantamento (laboratório)

A demonstração jogável da seção 5 do [25](../../../roadmapIDEIAS/25-ETAPA4-REFORCO-E-ENCANTAMENTO.md) (26/10/2026).
**Não é integração.** O jogo de produção não carrega esta pasta (um teste confere); a forja, o mercado e os saves do
jogo não mudaram. Os números são hipóteses desta rodada, não balanceamento.

## Abrir

Dê dois cliques em `demo.bat` (ou `python ferramentas/prototipos/reforco/demo.py` na raiz). O jogo de sempre abre no
navegador num **save temporário** (uma pasta nova a cada vez; os saves pessoais não são lidos nem tocados): o Guerreiro
no nível 4, no Vau, com Morel e Odette, 380 de ouro, dois baús e as peças dos exemplos. Feche a janela do terminal
para parar. Folhas: `folha.png` (reforço e desmontagem) e `folha-encantar.png` (encantamento).

Só nesta execução, `demo.py` troca a forja (o balcão novo), o baú (que pode dar fragmento ou essência), a seção
"Materiais" do Inventário, a venda da peça reforçada, a ficha das peças nas telas (as gravações) e liga os efeitos das
gravações na luta. O resto é o jogo: o Inventário do grupo, o mercado, a luta, a estrada.

## 11ª versão: o resultado em destaque (candidata em avaliação)

Pedido do Jean depois de ver a 10ª: o sucesso escurecia junto com o resto da tela, os feixes paravam, o OK tinha a
estética antiga, o "Sucesso" era pequeno e o quadrado do molde cortava o efeito. Regras, chances, custos e o +4 iguais;
a 10ª está em `tela/historico/v10`. Folha: `folha.png` (a 10ª × a 11ª na mesma tentativa, a sequência nas duas
resoluções, o +3, a falha, o movimento reduzido e os outros botões). A `folha-encantar.png` continua a da 10ª.

- **A bancada clara.** Causa: o recorte do véu da cena era medido antes de a janela ser desenhada e ficava 0×0 no
  canto; o véu cobria a tela inteira, bancada incluída (na captura da 10ª a ordem saiu favorável por acaso). Agora é
  medido no quadro seguinte ao desenho (e ao redimensionar): só o entorno escurece; o título, a peça, o ganho e o
  efeito ficam claros.
- **Os feixes continuam até o OK.** Abrem no impacto e seguem girando, mais curtos e achatados depois do primeiro
  segundo, por trás do título, do ganho e do pé (a leitura fica por cima); as brasas continuam subindo. O selo de
  raios é proporcional ao molde (a 1280 não invade "Sulcos").
- **"Sucesso" grande, no pé**, entre a peça e o OK, no lugar da chance e da falha (o OK continua onde estava o
  Reforçar): entra com um impacto curto e brilho. "Falhou" no mesmo lugar, sóbrio. A faixa do alto saiu.
- **O molde sem corte seco:** no sucesso, o quadrado do encaixe dá lugar a um disco escuro em degraus, como o item no
  achado; o selo de raios aparece inteiro em volta.
- **Os botões do jogo atual** (`.botao-janela`, o mesmo do achado e das janelas) em todas as ações da forja: Reforçar,
  OK, Gravar, Substituir, Desmontar, Cancelar e Fechar. Junto, uma colisão de nome: a janela mora em `#texto`, e a
  regra `#texto .perigo` pintava de vermelho o Desmontar bloqueado; corrigido.
- **Conferido:** a 1920×945 e 1280×720, a sequência contínua da mesma tentativa, o +3 aos 4,0 e 4,6 s (os raios em
  outra posição: continuam girando), a falha, o movimento reduzido (o resultado parado com o OK), os gestos (Enter
  segurado compra uma vez e não dispensa; clique duplo no OK dispensa sem comprar; clique duplo no Reforçar compra uma
  vez; Esc dispensa), a desmontagem e o encantamento com os botões novos.

## 10ª versão: a bancada com o título, o resultado até o OK e as pendências de dados (histórico)

Regras, chances, custos e o limite +4 iguais; o sprite continua em escala inteira (2× a 1920), sem ampliar a 3×. A 9ª
está em `tela/historico/v9` (a faixa abre "v9"). A `folha-encantar.png` é desta versão (casos, identidade das peças,
sulcos e encantamento); a folha da sequência da 10ª está no git.

### A composição do Reforçar

- **Sem a ficha lateral.** No topo da bancada, o nome inteiro da peça com o nível ("Martelo de Ferro +2"), na cor da
  raridade do jogo; embaixo, menores, o dono e os sulcos. A peça no centro do molde, os materiais à esquerda e o ganho à
  direita. A chance e a consequência da falha junto da ação ("Falha: +2 → +1"); o botão diz "Reforçar +2 → +3". A
  ficha completa continua na dica da peça (mouse e foco do teclado).
- **O mesmo eixo e as mesmas dimensões** na oferta, na cena, no resultado e no máximo (700 × 489 a 1920; a 1280 cabe
  sem rolagem). Nome longo, peça única e peça bloqueada conferidos (no máximo duas linhas no título).

### O impacto do nível e o foco

- **O entorno escurece** durante a cena (moderado, sem desfoque nem clarão de tela inteira); a bancada fica clara. O
  véu é a sombra em volta de um recorte do tamanho da janela: a janela mora num contexto de camadas da HUD (a mesa), e
  um véu de tela inteira escurecia a bancada junto (achado na sequência contínua e corrigido).
- **Contenção:** no fim do aquecimento, a luz do molde se fecha num instante antes do impacto, dentro da mesma duração.
- **Sucesso:** o nível antigo fica no título até a revelação; então o número novo entra como uma marca quente (impacto
  breve, brilho e fagulhas pequenas saindo do número); o antigo some. Só o número anima; o nome, a peça e o ganho
  continuam legíveis. **Falha:** sóbria, sem a marca (o número novo em cinza claro).

### O resultado até o OK

- O resultado do reforço fica na tela até **OK**, **Enter** ou **Esc**. A chance, a falha e a nota somem do resultado
  (o espaço fica); o botão vira OK no mesmo lugar. Depois do OK, a próxima oferta ou o máximo. Sem espera forçada.
- O gesto que adianta a animação não dispensa o resultado; tecla segurada e clique duplo não dispensam nem compram de
  novo (testado: Enter compra, Enter adianta, Enter dispensa; Enter segurado 15 vezes compra uma vez; clique duplo no
  Reforçar compra uma vez; clique duplo no OK dispensa uma vez; clique fora do OK no resultado não faz nada).
- Fechar a janela continua possível e não altera a compra. Movimento reduzido: o resultado parado, com o mesmo OK. A
  desmontagem não ganhou confirmação extra.

### Corrigido

- **Retirar pela miniatura:** clicar de novo na miniatura selecionada tira a peça da bancada (como clicar na peça do
  molde).
- **O texto de compatibilidade:** a dica da essência diz "Compatível com: armas, focos e escudos"; junto do Gravar
  bloqueado, o caso da peça: "Incompatível com peitorais". O padrão está na skill `texto-regras-fenda`.
- **Os rastros da borda** das gravações mais longos (a mesma espessura): com três essências, quase se encontram, cada
  um na sua cor, em degraus de pixel.
- **O efeito que piscava** na ficha ao apertar Continuar ou numa ação que não muda o equipamento. Causa: a tela do jogo
  redesenha os painéis a cada atualização, e a aparência da peça (a borda das gravações, a luz do +4) só voltava no
  próximo ciclo do protótipo (até 200 ms depois), com a borda recomeçando a volta. Agora a aparência entra no mesmo
  instante em que o slot é redesenhado, e a borda continua a volta pelo relógio. Medido quadro a quadro num slot com
  gravação ao longo de 5 redesenhos: 27 quadros sem a borda na 9ª, 0 agora.
- **A identidade das peças:** as dicas não acham mais a peça pelo nome. Cada elemento diz qual peça mostra (a forja, o
  Equipado, o Inventário pela aba do personagem e o espaço, a bolsa pela posição, o mercado pela posição na lista da
  loja). Conferido com dois "Martelo de Ferro" (o de Jean com Brasa, o de Morel com 1 sulco vazio) e dois "Broquel
  Enferrujado" no mercado.
- **Quando os sulcos nascem:** com a peça, uma vez (o drop, o mercado, o saque, a recompensa, o único), pela semente
  da própria peça, sem gastar o sorteio do jogo; as peças que já existiam ganham os delas ao começar e ao carregar um
  save antigo. Abrir uma ficha só lê (antes, a primeira ficha decidia). O mercado e o saque importavam a criação pelo
  nome e ficavam sem sulcos: corrigido, com um teste que confere todos os módulos que criam peças.
- **Os sulcos no achado:** a janela "Você encontrou" monta a ficha em pedaços, sem a função das outras telas; os
  sulcos da peça achada entram embaixo das linhas dela (conferido com um saque real de chefe, nas duas resoluções).

### Conferido

- 37 testes do protótipo; a 1920×945 e 1280×720: a sequência contínua da mesma tentativa (oferta, aquecimento,
  contenção, impacto, resultado mantido, próxima oferta), falha, máximo, falta de recursos, nome longo, peça única,
  movimento reduzido; os gestos acima; retirar pela miniatura e pelo molde; Continuar sem piscar; peças homônimas;
  saque real; **salvar pela interface e carregar** (o Martelo +2 com Brasa e os sulcos de cada peça voltam iguais, na
  dica e na forja).

### Pendências

- **Revisão de som adiada:** fica para quando a interface estiver satisfatória como 1.0 (a cena e o resultado mantido
  não tiveram o som revisto; os sons não foram ouvidos nas conferências).
- Os ícones das essências em 16 e 24 px ainda são reduzidos pelo navegador (desenho próprio por tamanho, com a arte).
- A demonstração não tem tela de carregar: o carregamento foi conferido com um lançador de conferência que abre, pelo
  `carregar` do jogo, o save gravado pelo botão Salvar.

### Roteiro (uns 3 minutos)

1. Ferreiro → **Reforçar** → o martelo com **Sucesso (teste)**: o entorno escurece, o número novo entra quente no
   título, o resultado espera o **OK** (Enter). Experimente segurar Enter e o clique duplo.
2. **Falha (teste)**: a falha sóbria. Clique de novo na miniatura selecionada: a peça sai da bancada.
3. **Encantar** no peitoral: passe o mouse na Brasa ("Compatível com: armas") e veja "Incompatível com peitorais"
   junto do Gravar. Grave duas essências no martelo e aperte Continuar na vila: a borda não pisca.

## 9ª versão: consistência visual e de interação (histórico; as folhas desta versão estão no git)

Regras, chances, custos, o limite +4 e as regras candidatas do encantamento iguais; a bancada não foi redesenhada. A 8ª
está em `tela/historico/v8` (a faixa abre "v8").

### Corrigido

- **O sprite borrado.** Causa real, isolada por partes (o normal, um `filter` como o da falha, o deslocamento do tremor,
  o quadro real): não era a falha nem o tremor. A HUD declara `:root body img.desenho { image-rendering: auto }` (os
  desenhos feitos à mão aparecem no tamanho nativo) e essa regra vencia a do protótipo; no molde, o desenho de 40 px
  era esticado a 72 (1,8×) a 1920 e a 44 a 1280, e o navegador o suavizava em todos os estados (no escuro da falha, ficava
  evidente). Agora: escala inteira (80 px = 2× a 1920; 40 px = 1× a 1280), `pixelated` com uma regra que vence a da HUD
  só dentro da janela, e a janela em coordenadas inteiras. Conferido nítido no aquecimento, na falha, no impacto com o
  golpe e na volta à oferta, nas duas resoluções.
- **O efeito do reforço que sumia.** As representações fora da forja descobriam o nível pelo "+N" no fim do nome; a
  peça única tem o rótulo "★ Lamento de Gharbad +2 (Machado)", que não termina em "+N", e ficava sem o efeito (na forja,
  o nível vinha da própria peça, por isso ele "voltava" lá). Agora a ficha das telas leva o `reforco` da peça e todas as
  representações leem dela. Reproduzido: reforçar até +4 → guardar na bolsa → equipar → trocar pela outra arma → abrir e
  fechar o Inventário → trocar de personagem → voltar à forja: em cada passo, a ficha lateral, o Inventário (corpo e
  bolsa) e a forja com o efeito; a peça única equipada, com o reflexo no Equipado. Salvar e carregar: testado nos dados
  (a peça volta com o reforço, os sulcos e as gravações).
- **O tremor que não reiniciava.** O golpe só saía quando o temporizador do desfecho chegava com atraso zero; chega
  alguns milissegundos depois, e às vezes o +4 não tremia. E um redesenho no meio cancelava os passos. Agora o impacto
  sai uma vez por resultado (inclusive adiantado), num relógio próprio que um redesenho não corta; um golpe novo cancela
  o anterior e a volta à oferta zera o deslocamento.
- **Os sulcos nas fichas.** Encaixes quadrados (o vazio escuro com contorno; o ocupado com o símbolo da essência), na
  quantidade real da peça, na dica e na ficha: achado, Inventário (a ficha e as dicas da bolsa e do corpo), Equipado,
  mercado e forja; na forja, os mesmos encaixes são os botões de escolher o sulco. A dica de cada slot pequeno os mostra;
  o ícone da bolsa não. Os sulcos são sorteados uma vez, na primeira ficha em que a peça aparece (no lugar do drop),
  pela própria peça; consultar ou redesenhar não sorteia de novo (testado).
- **O texto do encantamento** (a skill `texto-regras-fenda` ganhou os critérios gerais): a regra num bloco à esquerda,
  de largura controlada, com o nome, o efeito e o limite; a dica da essência "Brasa ×2" (sem o "Tem 2" avulso); a ficha
  com a seção de encantamentos (o nome de cada essência como título, o efeito e o limite embaixo; saiu
  "GravaçãoCarrasco"); a essência que entra como símbolo num encaixe, o nome só no bloco; o motivo de indisponível
  sempre junto do botão; a substituição "Sai Brasa · Entra Carrasco" / "Brasa se perde."; o sucesso em latão ("Gravado"),
  com a cor da essência só no nome (o vermelho do Carrasco lia como falha). O bloco da regra tem altura fixa: a
  bancada do encantamento não muda de tamanho entre essências, peças e confirmações (500 px a 1920; 320 a 1280).
- **Retirar a peça da bancada.** Clique (ou Enter/Espaço) na peça do molde: o encaixe fica vazio, a peça continua onde
  estava, o foco volta para ela na esteira. Durante uma cena, o clique só adianta; o segundo clique de um clique duplo
  não faz nada.
- **A borda luminosa.** Um núcleo claro de 2 px, três tons, um rastro curto em degraus, sem brilho difuso, seguindo a
  borda do slot (os cantos também); sem o tom de base na borda inteira (a quantidade de sulcos está nas fichas).
  Conferida numa bolsa com reforço, gravação, raridade, seleção e foco juntos; parada com movimento reduzido.
- **A desmontagem:** a peça que se desfaz não deixa a linha de raridade no encaixe vazio (duas desmontagens seguidas,
  12 → 13 → 14).
- **A luta de teste:** durante a luta, os cartões da forja ficam apagados e não respondem ("Durante a luta, a forja
  espera."); o botão da faixa fecha a janela antes de começar.

### Investigado, sem mudança

- O tremor em si (`top` na chapa, não `translate`) não borrava o sprite; o filtro da falha também não (o borrão estava
  em todos os estados). O brilho difuso do impacto do sucesso (`drop-shadow` de 4 px) é o clarão da peça, não do
  sprite: ficou.
- O achado (o espólio de uma luta com saque) usa o mesmo caminho das dicas que foi conferido no Equipado, na bolsa e
  no mercado; não foi exercitado na tela nesta rodada (a luta de teste não tem saque).

### Pendências

- Os ícones das essências em tamanhos pequenos (16 e 24 px a partir de desenhos de 32) ainda são reduzidos pelo
  navegador; um desenho próprio por tamanho fica com a arte das essências.
- Na dica por nome, duas peças com o mesmo nome e sulcos diferentes podem trocar a seção (a forja, o Equipado e a bolsa
  usam a peça do dono; o mercado e o achado usam o nome).
- Sons não ouvidos (sem saída de áudio nas conferências).

### Roteiro (uns 3 minutos)

1. Ferreiro → **Reforçar** → o martelo até o +4 com **Sucesso (teste)**: o sprite nítido, o golpe do +3 e o do +4.
2. Clique na peça do molde: ela sai da bancada. Feche a forja; no Inventário (`i`), guarde e equipe o martelo, troque
   pelo Martelo de Aço, mude para Morel e volte: o efeito do +4 em todos os lugares.
3. Passe o mouse no Equipado e na bolsa: os sulcos na dica. No **Encantar**: a regra à esquerda, "Brasa ×2", os sulcos
   como encaixes, uma substituição ("Sai · Entra") e a ficha com a seção de encantamentos.

## 8ª versão: acabamento do reforço, desmontagem refeita e o Encantar de laboratório (histórico; as folhas desta versão estão no git)

Duas frentes, cada uma com a sua folha: `folha.png` (Lote 1: reforço e desmontagem, v7 × v8 com os mesmos dados) e
`folha-encantar.png` (Lote 2: o encantamento). A 7ª está em `tela/historico/v7` (a faixa abre "v7"). As regras,
chances, custos e o limite +4 do reforço são os da 5ª versão; o +5 continua só registrado.

### Lote 1: reforço e desmontagem

**Desmontagem (refeita):** a mesma bancada do reforço, com as mesmas dimensões (640 × 342 a 1920; 404 × 238 a 1280): a
peça no molde, no eixo do botão; à direita, o conduto e o encaixe do que ela rende (ícone e quantidade). Saíram o
título "Desmontar" na borda, o conduto solto e a faixa "Desmontado · material · nome". A confirmação fica no pé, com o
nome da peça e "O equipamento será destruído.". Depois de confirmar, uma transformação de 0,7 s (hipótese): um toque na
bancada e um clarão pequeno, a peça clareia e se parte, fragmentos de pixel voam ao encaixe do material, que aparece com
a quantidade; o saldo de Fragmentos acende em verde. A seleção fica vazia (nada é escolhido sozinho) e o encaixe
do material mostra o que chegou até a próxima ação. Achado e corrigido: desmontar uma peça única (o Lamento) falhava
com "A peça mudou desde a confirmação" (a tela mandava o rótulo com ★; o motor esperava o nome).

**Reforço:**
- Golpe seco na bancada no +3 e no +4, só a chapa e só na vertical (+3: desce e volta; +4: desce mais, um rebote menor
  e assenta), na mesma duração; a página não treme.
- O máximo: no sucesso que chega ao +4, o contorno do molde se completa barra a barra e fica aceso ~1,5 s.
- A falha mais legível a 1280 ("+3 → +2" claro, maior; "Falhou" num vermelho apagado; nada dourado).
- No desfecho, os dados da tentativa (materiais, chance, botão, nota) ficam no lugar, apagados: o resultado domina.
- Movimento reduzido: um quadro assentado (selo pequeno, raios curtos e apagados), não o pico do efeito.
- Os saldos acendem quando mudam (a cobrança em cor de custo; o que entra em verde); o +N da peça na esteira acende no
  desfecho, sem perder a seleção.
- A janela nasce já no lugar: antes, num redesenho, ela passava um quadro sem posição e o segundo clique de um clique
  duplo atravessava para o balcão atrás (o cartão Desmontar). Achado nesta rodada; corrigido.

**Reflexo e acabamento:**
- Conferido nos níveis reais, lado a lado (`CASOS=1` agora põe peças da bolsa no +1, +2 e +3, além da armadura de Morel
  no +4): +1 claro e discreto, +2 verde, +3 azul, +4 dourado, cada peça na sua vez (as passadas registradas aos 1,6 s,
  2,2 s e 2,6 s, depois em ciclo; nunca juntas).
- A faixa como luz que atravessa o material: o miolo claro, as bordas na cor do nível, a textura por baixo (mistura
  "screen"), mascarada pelo desenho da peça.
- O +4 tem também uma luz baixa e permanente na própria peça (um contorno de 1 px dourado, sem borrão).
- O ciclo só anima o que está à vista, para em aba oculta e esquece o que saiu da tela há 8 s; a raridade, o +N, a
  seleção e o foco não mudam.
- Sons do jogo (sintetizados, respeitam o som desligado): o martelo na bigorna no sucesso, o golpe junto no +3 e no +4,
  o golpe leve na falha, os estalos de metal na desmontagem. **Não ouvidos:** as conferências rodam sem saída de áudio;
  o jogo não tem um som de fragmentação (usei os estalos de metal, que existem).

**Produção (separado, 1.213.2):** o Inventário não mostra mais "Clique numa peça da bolsa ou num espaço do corpo…";
sem peça marcada, a caixa da ficha fica oculta (a coluna mantém a largura).

### Lote 2: encantamento (gravação), proposta de laboratório

**Não é regra aprovada nem integração.** O código é `encanto.py` (regras e a ligação com a luta) e a janela Encantar em
`tela/reforco.js`; o jogo não carrega nada disso (o teste de isolamento confere).

**Pesquisa (capturas observadas):** a Forja do Last Epoch (wiki oficial, captura da tela): a peça no centro, os
modificadores dos lados, um canal aceso ligando o escolhido à peça, o custo e um botão, e o resultado escrito no
próprio painel; aproveitei o canal aceso (os condutos da bancada) e o resultado no painel. O item encantado do Diablo
III (wiki, captura da ficha): a propriedade encantada fica na lista da peça, com um marcador diferente; aproveitei a
gravação dentro da ficha da peça, com a cor da essência. Sem captura de interface nesta rodada: Maxroll (404), UESP
(Skyrim) e Fextralife (Elden Ring) só tinham ícones e guias. Nada foi copiado; o acabamento é o da bancada e o efeito é
o do jogo.

**Decisão do Jean (27/10):** uma peça pode ter mais de um espaço de gravação, sorteado no drop como os outros
efeitos; a ordem dos serviços é Reforçar, Encantar, Desmontar.

**Hipóteses desta rodada (provisórias):**

| Assunto | Hipótese |
|---|---|
| Sulcos | 1 a 3 por peça, sorteados pela raridade (comum 1–2; incomum 1–3; raro 1–3; lendário 2–3). No laboratório, o sorteio acontece na primeira vez que a peça aparece (semeado pela peça); a arma do herói tem 2 no cenário |
| Elegíveis | As peças que aceitam reforço (arma, peito, escudo, foco), de qualquer um do grupo ou da bolsa; cada essência diz em que tipo entra |
| Custo | 1 essência + 30 de ouro (com a reputação); nunca falha; não rebaixa nada; não herda a chance do reforço |
| Substituir | Gravar num sulco ocupado custa o mesmo e apaga a gravação daquele sulco; a essência antiga não volta. Confirmação no pé: "Substituir X por Y? A gravação X se perde." |
| Repetição | A mesma essência não entra duas vezes na mesma peça; o mesmo efeito conta uma vez por corpo |
| Essências | Materiais do grupo, fora da bolsa. Fontes: recompensa de teste (2 de cada, marcada teste); baú (25%, 1 aleatória) |
| A peça | A gravação vai junto quando a peça troca de dono; desmontar perde a gravação (não devolve essência); vender não muda o preço |
| Coexistência | Reforço na superfície (o reflexo); gravação na borda própria do slot (a luz que percorre a borda, um trecho por gravação, defasados), sem níveis de encantamento |

**As seis essências:**

| Essência | Alvo | Gatilho | Magnitude | Duração | Limite | Interação |
|---|---|---|---|---|---|---|
| Brasa | arma | golpe do portador que acerta (não reações nem tiques) | 35%: 1 camada de Queimadura (até 3), valor 25% do maior entre Ataque e Poder (mín. 2) | a da Queimadura | 1 por rodada | soma com a Queimadura do Mago; o tique não dispara nada |
| Carrasco | arma | golpe num inimigo abaixo de 35% da vida | +30% de dano | — | — | multiplica com os outros bônus; não vale em tiques nem reações |
| Eco | arma, foco, escudo | inimigo abatido pelo portador | 25% da Mana, Vigor ou Foco máximos | — | 2 por luta | soma com Colheita e Assassino |
| Vigília | peito, escudo, foco | começo da luta | barreira de 15% da vida máxima | 3 turnos do portador | 1 por luta | não soma com outra barreira: vale a maior |
| Revide | peito, escudo | golpe corpo a corpo de um inimigo que acerta | 25%: golpe de 60% do Ataque | — | 1 resposta por golpe | o revide não aciona revide nem Brasa |
| Geada | peito | golpe corpo a corpo de um inimigo que acerta | 30%: congela o atacante (perde a próxima vez) | 1 turno dele | 1 por luta | chefes e gigantes resistem metade das vezes |

Sem ciclos: os efeitos secundários (o revide, o tique da Queimadura) não passam pelo gatilho. Na luta, os efeitos
valem para o herói e para os companheiros (os envoltórios do golpe, do início da luta e da morte de um inimigo, só
nesta demonstração); o que dura fica na memória da luta e some com ela.

**A janela:** a bancada (a essência escolhida e o ouro à esquerda, a peça no eixo, a essência que entra à direita), os
sulcos em cima da peça ("Vazio" ou o nome, na cor da essência; escolher é clicar), o trilho das seis essências com a
quantidade no canto, a regra curta da escolhida e, no pé, Gravar ou Substituir com a nota (falta, inelegível). A
gravação (2,3 s, adiantável): as barras do molde acendem na cor da essência uma a uma, um ponto de luz percorre a
borda soltando fagulhas, um anel curto, "GRAVADO" e o nome junto da peça; a borda de luz fica. O saldo, a ficha (cada
gravação com a regra), a esteira, o Inventário e o Equipado da ficha lateral mostram o resultado. A 1280, as essências
saem do cabeçalho (a quantidade está no trilho) e a bancada encolhe para caber sem rolar.

**Luta de teste:** o botão "Luta de teste" na faixa do protótipo (com a forja aberta): dois Esqueletos do nível do
herói; o grupo volta com a vida, o recurso, a experiência e o ouro de antes. Um aviso resume o que disparou.

### Conferido (8ª versão)

- 34 testes do protótipo (22 do reforço, 12 do encantamento): uma cobrança por gravação; o mesmo pedido de novo não
  grava; substituir pede a gravação vista e apaga a anterior; os sulcos sorteados (1 a 3) e o segundo sulco; a mesma
  essência recusada no outro sulco; elegibilidade e falta sem cobrança; a gravação vai com a peça a Morel; desmontar
  não devolve essência; Brasa, Vigília, Revide e Geada disparando em lutas de verdade (o robô); Carrasco (+30% abaixo de
  35%) e Eco (2 por luta) numa luta montada; uma barreira por luta, nada acumulando entre lutas; a luta de teste devolve o
  grupo como estava.
- Na tela, 1920×945 e 1280×720: o eixo e as dimensões medidos iguais no reforço e na desmontagem; a desmontagem (12 →
  15, uma vez, nada selecionado depois); o reforço até o máximo; o encantamento com quatro gravações e quatro cobranças
  (380 → 350 → 320 → 290 → 260), dois sulcos e uma substituição; fechar no meio da gravação mantém a gravação e não
  cobra de novo; Enter grava, adianta e assenta; Esc adianta e cancela a confirmação; Enter segurado e clique duplo sem
  repetir; movimento reduzido nos três serviços; a borda de luz no Inventário e na ficha lateral; a luta de teste.

### Roteiros (uns 3 minutos cada)

**Lote 1:** `demo.bat` → Continuar → Ir para a vila → Ferreiro → **Reforçar**: o martelo, Ataque, Reforçar; na faixa,
**Sucesso (teste)** até o +3 (o golpe seco) e o +4 (o rebote e o contorno aceso); uma **Falha (teste)** no caminho.
**Desmontar**: o Lamento de Gharbad → Desmontar → confirme (a peça se desfaz, ×3 chega, o saldo acende). Com
`CASOS=1`, a bolsa mostra o reflexo em +1, +2, +3 e a armadura de Morel em +4.

**Lote 2:** Ferreiro → **Encantar**: o Peitoral, **Vigília**, Gravar; o Martelo (2 sulcos): **Brasa** no primeiro,
**Eco** no segundo; clique no sulco da Brasa, escolha **Carrasco** e Substituir (a confirmação diz o que se perde).
Feche: o Inventário (`i`) e o Equipado mostram a borda de luz. Volte à forja e use **Luta de teste** na faixa.

### Pendências

- As regras do encantamento são candidatas: a quantidade e a distribuição dos sulcos, os custos, as fontes de
  essência, a recuperação ao desmontar, a remoção sem substituir (não há) e o equilíbrio dos seis efeitos.
- Os ícones das essências são desenhos que o jogo já tem (chama, caveira, poção azul, escudo, espada, gota); arte
  própria fica para depois da aprovação das regras.
- Sons não ouvidos (sem saída de áudio nas conferências); um som de fragmentação próprio não existe.
- Ideias registradas, não feitas: laranja para um eventual +5; os níveis de encantamento não existem.

## 7ª versão: eixo central, bancada fixa, efeitos soltos e reflexo (histórico)

Só a tela mudou: regras, chances, custos, consequências e o limite +4 são os da 5ª versão. A 6ª está em
`tela/historico/v6` (a faixa abre "v6"). A folha desta versão (v6 × v7 com os mesmos itens e saldos; a sequência real até o
máximo a 1920×945 e a 1280×720; os casos; as quatro cores do reflexo) foi substituída pela da 8ª (está no histórico do
git). A tela desta versão está em `tela/historico/v7`.

### A candidata

- **Um eixo:** o nível, o centro da peça, a chance e o Reforçar ficam na mesma vertical. O leito tem três colunas, as
  dos lados de largura igual (os materiais à esquerda, o ganho à direita), e a largura delas não desloca a peça; o pé
  empilha a chance, o botão e a nota também a 1280, e a ajuda (i) fica ao lado da chance, fora do eixo. Medido em
  todos os estados: a 1920, x = 852 e a bancada 640 × 342; a 1280, x = 560 e 404 × 238.
- **A mesma bancada em todos os estados:** oferta, aquecimento, desfecho, falta, reforço máximo, peça que ninguém usa e
  sem peça escolhida. No máximo, a bancada inteira fica, com "+4", as quatro marcas, os encaixes de material apagados e
  o botão indisponível "Reforço máximo". O Reforçar não se desloca nem some durante a cena (fica indisponível).
- **A cena mostra a tentativa, não o resultado:** no aquecimento, a bancada tem o nível, o custo pago, o ganho e a
  chance da tentativa, e a ficha, o nome, o +N da esteira e o valor do atributo de antes ("Ataque" nunca fica sem
  número). No desfecho, a ficha passa aos valores novos e a propriedade que mudou acende um instante; depois, a
  próxima oferta. Nada mostra antes da hora o sucesso, a falha ou a chegada ao máximo (a dica da peça na esteira
  também espera).
- **Sem a faixa do resultado:** "Reforço bem-sucedido · +N · Ataque…" saiu; o resultado é a cena. A placa ficou só na
  desmontagem.
- **A ficha:** um cartão compacto no alto da coluna (mais estreita: 260 px a 1920, 196 a 1280) com o nome, o dono e as
  propriedades, cada valor junto do nome.
- **A comparação de teste** ("Esqueleto nível 4…") saiu da tela: é o botão "Comparação (teste)" da faixa do
  protótipo, que abre um painel com a peça escolhida.
- **O desfecho:** o efeito (FX do Estouro) não é mais recortado no leito: os raios, os estilhaços e as fagulhas passam
  da bancada e um pouco da moldura (recorte: a janela com 22 px de folga; nada na tela inteira). O halo intenso fica
  junto da peça e o anel é achatado, para não descer até a chance. A peça, o conjunto do resultado, o pé, o cabeçalho,
  a ficha e a esteira ficam por cima do efeito; o canvas não recebe cliques nem muda o tamanho de nada. Um poço escuro
  atrás do conjunto do resultado mantém a leitura sobre os raios. O sprite tem o tamanho de antes.
- **Sucesso:** "SUCESSO", o +N grande e o ganho (o valor novo em verde) num conjunto à direita da peça.
- **Falha:** "FALHOU" num vermelho apagado, a queda "+3 → +2" e o ganho perdido em cinza, menores; nada dourado nem
  grande.
- **Movimento reduzido:** o desfecho parado com o selo de raios e o contorno do molde, sem tremor nem movimento; o
  reflexo parado e discreto.
- **O reflexo do reforço:** uma faixa diagonal curta atravessa a silhueta da peça (o próprio desenho é a máscara: só os
  pixels da peça brilham), na cor do nível: +1 claro e discreto, +2 verde, +3 azul, +4 dourado. A borda de raridade
  não muda. **Em todo slot onde a peça reforçada aparece** (na forja, a esteira e o molde; no Inventário, o corpo, a
  bolsa e as opções de um espaço; na ficha lateral, o Equipado), ele passa sozinho: a primeira vez 2 s depois de a peça
  aparecer, depois a cada ~3 s, cada peça na sua vez (defasadas). Também passa ao concluir um sucesso, ao escolher a
  peça e no mouse ou no foco do teclado. Durante a cena do reforço, nenhuma brilha (a cor do nível novo esperaria o
  desfecho). Com movimento reduzido, fica parado e discreto em todos esses slots. Só na demonstração: o código está no
  script do protótipo, e o jogo não muda.

**Referências:** Epic Seven (a estrutura mantida no máximo), Ragnarok Origin (a peça perto do resultado) e Guardian
Tales (o ganho compacto), pelas indicações do Jean. Não achei capturas dessas telas nesta rodada (as buscas só deram
guias de regra), então apliquei esses princípios sem copiar nada; o acabamento e os efeitos seguem o jogo e o Estouro.

### Conferido (7ª versão)

- A sequência real até o máximo, a 1920×945 (mouse) e a 1280×720 (teclado): +1, +2, +3, falha (+3 → +2), +3, +4 e o
  "Reforço máximo". Em cada quadro (oferta, aquecimento, impacto, desfecho, próxima oferta), nível, atributo, saldos e
  custo da mesma tentativa; uma cobrança por tentativa (380/12 → 360/11 → 325/10 → 270/8 → 190/6 → 135/4 → 55/2).
- O eixo e as dimensões, medidos (acima), iguais em todos os estados nas duas resoluções, sem rolar a mesa.
- Gestos: Enter compra, adianta e volta à oferta com o foco no Reforçar; 15 repetições seguradas e o clique duplo
  compram uma vez; Esc adianta e depois fecha; o Fechar funciona no meio da cena; no centro do desfecho, o elemento
  sob o ponteiro é a bancada, não o efeito.
- `CASOS=1`: a falta ("Falta 1 Fragmento", a ajuda) e a armadura de Morel no +4; o arco que ninguém usa; o movimento
  reduzido em toda a sequência; o reflexo no mouse, no foco do teclado, na escolha e no sucesso.
- O reflexo em ciclo (registro das passadas): na forja, o molde, a esteira e a ficha lateral; no Inventário, o espaço
  Arma aos 3,2 s (2 s + a defasagem) e depois a cada ~3 s, alternando com a ficha lateral; durante a cena, só a passada
  do próprio sucesso, no desfecho; com movimento reduzido, parado (sem animação) no Inventário e na ficha lateral.

### Roteiro (uns 3 minutos)

1. `demo.bat` → Continuar → Ir para a vila → Ferreiro → **Reforçar** → o **Martelo de Ferro** (o reflexo passa se ele
   já tiver reforço). Escolha **Ataque** e Reforçar.
2. Na faixa, **Sucesso (teste)** duas vezes: o +2 (reflexo verde) e o +3 (efeito forte, reflexo azul). Repare que a
   peça, a chance e o botão não mudam de lugar e que a ficha só muda no desfecho.
3. **Falha (teste)**: "FALHOU", +3 → +2, sóbrio. Depois **Sucesso (teste)** até o +4: a bancada fica inteira, com
   "Reforço máximo".
4. Espere uns segundos: as peças reforçadas brilham sozinhas na cor do nível, uma de cada vez. Feche a forja e abra o
   **Inventário** (`i`): o mesmo no espaço da arma e no Equipado da ficha lateral.
5. **Comparação (teste)** na faixa abre a medição de laboratório da peça escolhida.

### Para depois (ideias, não feitas)

- **+5 em laranja:** a cor do reflexo para um eventual +5. O nível não existe; o limite continua +4.
- **Encantamento:** uma luz percorrendo uma borda própria da peça, distinta do reflexo do reforço. Depende da definição
  do sistema de encantamento.
- O reflexo no resto do jogo (mercado, loot, comitiva) e de verdade na produção, só depois de aprovado aqui.

## 6ª versão: a informação reorganizada e o desfecho (histórico)

Só a tela mudou: as regras, as chances, os custos e as consequências são os da 5ª versão (abaixo). A estrutura da
bancada, o molde, os encaixes e a seleção das peças ficaram. A 5ª versão está em `tela/historico/v5` (a faixa abre
"v5"). A folha desta versão foi substituída pela da 7ª (está no histórico do git).

- **Os dados, na ordem de leitura** (referências: Soul Knight Prequel e MapleStory M): os saldos no cabeçalho; na
  bancada, os materiais como ícone e quantidade (o nome e quanto o grupo tem na dica, por mouse e teclado; faltando, o
  número fica vermelho e o pé diz "Falta 1 Fragmento"); o nível junto da peça ("+1 → +2"); o ganho no visor ("Ataque
  4 → 5"); no pé, a chance numa linha ("Sucesso 85%") e o Reforçar. O que a falha faz, que a tentativa custa o mesmo
  e que o atributo escolhido fica com a arma estão na ajuda (i). Saíram a tabela Custo/Tem, "Próxima tentativa" e
  "Cada tentativa consome o custo.". Na arma do Guerreiro, a escolha aparece como **Ataque** ou **Poder** (o ganho de
  cada um), não Fio e Runas.
- **A cena (1,05 s de aquecimento + 1,7 s de desfecho):** os condutos e o molde aquecem; no impacto, o desfecho ocupa a
  região da peça com a biblioteca FX das celebrações aprovadas do Estouro: no sucesso, o selo de raios, o clarão, um
  anel curto e os estilhaços, "SUCESSO" sobre a peça e o +N grande com o ganho; na falha, o calor que se desfaz, as
  cinzas e "FALHOU" com o nível que ficou. No +3 e no +4, a paleta lendária, mais estilhaços e a chapa treme. Depois, a
  bancada volta sozinha para a próxima oferta, com a placa resumindo o resultado.
- **O impacto fica na peça:** o efeito é recortado no leito (a área funda da peça e do resultado); o clarão é um halo
  em volta da peça, sem o pontilhado sobre a bancada inteira que a primeira montagem desta versão tinha no +3 e no +4,
  e o anel não passa muito do selo. O tremor é só da chapa (o do Estouro sacode a página).
- **Uma tentativa por quadro:** durante a cena, os encaixes mostram o custo pago (o motor já calculou a próxima), a
  ficha mantém o nome e os valores de antes (o +N novo só aparece no desfecho) e o cabeçalho já mostra os saldos
  cobrados; no fim, a bancada é redesenhada com a próxima oferta.
- **Gestos:** clique duplo e tecla segurada compram uma tentativa; durante a cena, um clique, Enter ou Espaço (com o
  foco em qualquer lugar) adianta: do aquecimento ao desfecho, do desfecho à oferta; Esc faz o mesmo e, na oferta,
  fecha. Com movimento reduzido, o desfecho aparece parado e a bancada volta depois de 1,7 s; o foco volta ao
  Reforçar (ou à peça, se o Reforçar ficou indisponível).

### Conferido (6ª versão)

Na demonstração, a 1920×945 (mouse) e a 1280×720 (teclado), uma sequência contínua cada: +0 → +1 garantido, sucesso
no +2, sucesso no +3, falha no +4. Em cada quadro (oferta, aquecimento, impacto, desfecho, próxima oferta), o nível, o
atributo, os saldos e o custo são da mesma tentativa: 380/12 → 360/11 → 325/10 → 270/8 → 190/6, uma cobrança por
tentativa. Também: 15 repetições de Enter seguradas compram uma vez; clique duplo, uma; Enter e clique durante a cena
adiantam sem comprar; Esc → desfecho → oferta → fecha; `CASOS=1` para a falta (o Reforçar indisponível, "Falta 1
Fragmento", a ajuda) e o reforço máximo (o nome longo em duas linhas, sem corte); movimento reduzido nas duas.

**Achados e corrigidos nesta conferência:** o nome da ficha mostrava o nível novo já no aquecimento (até na falha); o
Enter durante a cena não adiantava porque o foco caía na página; o clarão pontilhado cobria a bancada no +3 e no +4.

### Roteiro (uns 3 minutos)

1. `demo.bat` → Continuar → Ir para a vila → Ferreiro → **Reforçar**. Na aba Jean, o **Martelo de Ferro**: escolha
   **Ataque** e Reforçar (o +1 é garantido).
2. Na faixa, **Sucesso (teste)** e Reforçar: o aquecimento, "SUCESSO +2" e a volta à oferta (+2 → +3, 70%).
3. **Sucesso (teste)** de novo: o +3, com o efeito mais forte e a chapa tremendo.
4. **Falha (teste)**: "FALHOU +2" e a oferta de novo em +2 → +3. Repare nos saldos do topo: uma cobrança por vez.
5. Pelo teclado: Tab até o Reforçar, Enter; Enter de novo adianta, Esc volta à oferta, outro Esc fecha.
6. Passe o mouse no (i) e nos materiais. Com `CASOS=1`: a falta de fragmento e a armadura de Morel no +4.

## 5ª versão: o reforço com chance (direção aprovada; números e tela em avaliação)

**Decisões aprovadas (25, 5.6):** o +1 é garantido; depois a chance cai com o nível pretendido e, menos, com a
raridade; sucesso +1; falha −1, sem passar de +0; a peça nunca quebra; afixos, especiais e Fio/Runas ficam, também no
+0; a tela mostra antes de pagar a chance, o nível, a falha, o custo e o que o grupo tem; cada tentativa consome o
custo; a desmontagem conta o reforço conservado; sem proteção paga, failstacks ou garantia acumulada. O reforço
garantido das versões 1 a 4 fica **substituído** (histórico em `tela/historico/v4`, com as regras daquela versão).

### Hipóteses numéricas desta rodada

| Tentar | Chance (comum / incomum / raro / lendário) | Ouro | Fragmentos |
|---|---|---|---|
| +1 | 100% (todas) | 20 | 1 |
| +2 | 85 / 81 / 77 / 73% | 35 | 1 |
| +3 | 70 / 66 / 62 / 58% | 55 | 2 |
| +4 | 55 / 51 / 47 / 43% | 80 | 2 |

A raridade tira 4 pontos por degrau (12 no lendário), menos que os 15 que separam um nível do seguinte. Os preços
ficaram **mais baixos** que os da 4ª versão (25/50/90/140 e 1/2/3/4) porque agora se paga por tentativa: o caminho
feliz até o +4 custa 190 de ouro e 6 fragmentos (antes 305 e 10).

**Custo real de +0 a +4** (simulação, 40.000 caminhos por raridade, preços sem a reputação; mediana · 90% · 99%):

| Raridade | Tentativas | Ouro | Fragmentos | Quedas |
|---|---|---|---|---|
| Comum | 6 · 14 · 24 | 325 · 695 · 1.235 | 10 · 22 · 39 | 1 · 5 · 10 |
| Incomum | 8 · 16 · 28 | 335 · 820 · 1.460 | 11 · 25 · 46 | 2 · 6 · 12 |
| Raro | 8 · 20 · 34 | 390 · 955 · 1.725 | 13 · 30 · 55 | 2 · 8 · 15 |
| Lendário | 10 · 24 · 44 | 460 · 1.135 · 2.120 | 14 · 36 · 68 | 3 · 10 · 20 |

Leitura: a mediana fica entre 1,7 e 2,4 vezes o caminho feliz; 1 em 10 jogadores paga de 3,7 a 6 vezes; o pior 1%
de um lendário passa de 2.000 de ouro. Uma primeira hipótese mais dura (80/60/45 no comum) dava 48 tentativas no 90%
de um lendário: repetição demais; ficou a atual. O +4 continua sendo uma aposta (43–55%); parar no +3 é uma escolha
legítima. Para avaliar: se o pior caso do lendário é aceitável quando a campanha crescer, ou se o +4 de raros e
lendários pede mais chance.

**Recuperação:** desmontar devolve metade dos fragmentos **nominais** dos níveis que a peça conserva (+1: 1, +2: 1,
+3: 2, +4: 3), mais o da peça (comum 0, incomum 1, raro 2, lendário 3); vender devolve 25% do ouro nominal desses
níveis (+4: 47). As tentativas perdidas não contam. Testado: qualquer sequência de sucessos e falhas seguida de
desmontar ou vender deixa o grupo com menos ouro e com no máximo o material da própria peça a mais.

### A tela e a cena

- **Antes de pagar:** "Próxima tentativa +2 → +3 · Sucesso: 70% · Falha: +2 → +1"; no +1, "Sucesso garantido"; o
  custo em encaixes com Custo e Tem; "Cada tentativa consome o custo." sob o botão.
- **A cena (1,35 s):** os condutos aquecem (vermelho fundo → laranja → amarelo); a luz percorre as quatro barras do
  molde com fagulhas; no sucesso, o contorno fecha, pulsa e acende a peça; na falha, a luz apaga em trechos e caem
  cinzas, sem quebrar nada. No +3 e no +4 há mais fagulhas, na mesma duração. Durante a cena, a oferta, o botão, as
  marcas e o valor da ficha esperam (sem deslocar nada). Um clique, Enter, Espaço ou Esc revela; com movimento
  reduzido, o resultado aparece direto.
- **O resultado** fica numa placa de altura fixa acima da bancada: "Reforço bem-sucedido · +3" ou "Reforço falhou ·
  +2 → +1", com o ganho ou a perda real. A próxima oferta fica embaixo, separada.
- **Uma vez só:** o motor resolve e cobra no pedido; a tela só encena. Cada pedido leva um id; repetido, não tenta de
  novo. Fechar, trocar de aba, adiantar ou repetir a entrada não cancela, não rerrola e não compra outra vez.
- **Acabamento:** a chapa em três planos (a oferta, o leito afundado onde a operação acontece, o pé); o molde é um
  berço de ferro com garras e barras, não um pedestal; os condutos têm colares e o canal que aquece; os botões seguem
  a família da HUD; o indisponível mantém o corpo do botão, apagado. "Escolha Fio ou Runas" em cor neutra, com "O
  caminho fica com a peça." Desmontar mostra "Fragmento de Têmpera ×N"; depois, "Desmontado · Fragmento de Têmpera ×1
  · [peça]" e a seleção vazia. A seleção vazia mostra só "Escolha uma peça".
- **Casos de teste:** na faixa, "Próxima tentativa: Sorteio / Sucesso (teste) / Falha (teste)", uma vez; a placa
  marca "teste". `CASOS=1` abre com a armadura de Morel no +4 e 1 fragmento.

### Resultados observados

- 22 testes: chance exibida = calculada; o +1 garantido mesmo forçando a falha; cobrança na falha; queda até +0 com a
  base, os afixos e o nome restaurados; Fio/Runas preservado no +0; pedido repetido; o sorteio dentro de 3 pontos da
  chance em 2.000 tentativas; o único cresce pela base original; limite; falta de recurso sem cobrança; recuperação
  pelo nível conservado; ciclos; o jogo não carrega o protótipo.
- Na tela, 1920×945 e 1280×720: duplo clique, tecla segurada (15 repetições) e clique durante a cena compraram um passo
  só; Esc revela, cancela e fecha nessa ordem; fechar no meio da cena manteve a cobrança e o resultado. Achados e
  corrigidos: o foco do teclado sumia depois da compra (o botão ficava oculto na cena; agora volta ao Reforçar na
  revelação) e a tentativa quebrava depois do `CASOS=1`. A 1280 a bancada cabe sem rolar.

### Pendências

Calibrar as chances com partida de verdade (o robô não representa); decidir o pior caso dos lendários; elevação de
base e encantamento; arte do material (o saco segue provisório); som; integração.

## A tela, 4ª versão: a A · Bancada refinada (candidata em avaliação)

**Direção escolhida pelo Jean: A · Bancada.** Esta versão é a candidata refinada dela, ainda não aprovada nem
integrada. A A anterior e a B ficam em `tela/historico/v3` (a faixa da demonstração abre: "v3 (A e B)", com a troca
entre elas). Folha: `folha.png` (A anterior × A refinada com os mesmos dados, e o fluxo com recursos).

- **A bancada é um objeto:** uma chapa de ferro rebitada com espessura e sombra. Nela, da esquerda para a direita, os
  materiais (ouro e Fragmentos em encaixes, o custo grande e "Tem" embaixo), um conduto, a peça num encaixe sobre um
  pé de ferro com sombra de contato, as marcas do reforço sob ela, outro conduto com a seta e o visor do resultado; no
  pé da chapa, a ação. Princípio tirado da Forja de Stardew Valley ([wiki](https://stardewvalleywiki.com/Forge),
  captura da interface examinada): os encaixes ligados por canos e uma seta numa chapa única fazem a operação parecer
  parte de uma máquina. Não copiei a máquina nem a paleta.
- **Papéis separados:** o centro tem o próximo reforço, o ganho ("Ataque 4 → 5"), o custo e a ação; a ficha (mais
  larga: 360 px a 1920, 270 a 1280) tem o nome, o dono e todas as propriedades; a que o reforço muda tem o valor
  destacado num nicho de latão, sem repetir o "→".
- **Fio e Runas:** o visor do resultado vira duas opções ("Fio · Ataque 3 → 4", "Runas · Poder 0 → 1"); escolher é
  clicar numa; o custo é o mesmo.
- **Símbolos:** as marcas sob a peça são só o reforço; o material aparece pelo ícone com a quantidade (no canto das
  peças ao desmontar e no visor "Recebe"); a propriedade afetada é destacada pelo valor. O losango saiu.
- **Limite:** "Reforço máximo +4", as quatro marcas cheias, sem botão.
- **Desmontar:** a peça → "Recebe" (o ícone com a quantidade); a confirmação no ferro da chapa: "Desmontar [nome]?",
  "O equipamento será destruído." (em vermelho), Cancelar · Desmontar (o Desmontar em vermelho). A proteção continua
  (a confirmação arma depois de um instante; Cancelar não muda peça, recursos nem seleção).
- **Resultado do reforço:** um clique compra um passo; o custo cai, o próximo preço aparece, a peça continua
  escolhida e o foco volta ao Reforçar; a peça, a marca nova e o valor na ficha acendem por um instante (passos de
  pixel, 0,9 s, sem som, sem espera). Com movimento reduzido, o contorno da marca e do valor fica até a próxima ação.
  Os avisos genéricos "−N ouro" e "Peça +N" do jogo não aparecem por cima da janela (o topo conta).

## A tela, 3ª versão: duas direções (A · Bancada, B · Arsenal)

A estrutura da 2ª versão continua (uma janela por serviço, sem rolar a página, ouro e Fragmentos no topo, a ação
sempre à vista, Esc fecha). Mudam a apresentação e a escrita. A **faixa da demonstração**, no alto da tela, troca a
direção na hora (A ou B) e abre as versões antigas (v2, v1), guardadas em `tela/historico/`. Folha comparativa:
`folha.png` (os mesmos itens e recursos nas duas, a 1920×945 e a 1280×720, com o Mercado aprovado ao lado).

- **A · Bancada:** a peça num encaixe afundado no centro, o passo em cima ("+1 → +2"), as quatro marcas do reforço
  embaixo, os ganhos, o custo e o botão logo abaixo dela; a esteira das peças embaixo; os donos (retratos) à esquerda;
  a ficha completa à direita. Desmontar: a peça → o que recebe, a confirmação embaixo.
- **B · Arsenal:** as peças de todos numa grade por dono, com o +N no canto; a ficha compacta à direita (cabeçalho,
  passo, propriedades, venda, teste) e, fixos no pé dela, o custo e o botão. Desmontar: só a grade da bolsa, cada peça
  com o que rende no canto (◆1, ◆3; "—" não rende).
- **Em comum:** planos de ferro chapados com a textura dos botões do jogo e arestas duras (luz em cima, sombra embaixo),
  encaixes escuros para as peças, a raridade no fio de baixo do encaixe, a seleção pelos quatro cantos de latão,
  botões com quatro estados com forma (mouse clareia, pressionado afunda 1 px, indisponível tracejado, foco no anel de
  latão), a ação principal em latão. Tab fica dentro da janela; as setas andam entre as peças.
- **Escrita:** "+1 → +2", "Ataque 4 → 5", custo com rótulos ("Ouro · Custo 50 · Tem 355"), "Falta 1 Fragmento",
  "Recebe 1 Fragmento de Têmpera", "Destrói a peça." / "A peça é destruída.", "Venda: [moeda] 42" como dado
  secundário. "Encantar" saiu. A comparação contra o Esqueleto está numa área fechada, marcada **teste**. A ficha mostra
  todas as propriedades; as que o reforço faz crescer têm o ◆. Os casos estão na skill `texto-regras-fenda`.
- `CASOS=1` no `demo.py` abre a conferência: a armadura de Morel já no limite (+4) e 2 fragmentos (material
  insuficiente no segundo passo).

### Pesquisa visual (capturas abertas e examinadas)

| Captura | O que aproveitei | O que não |
|---|---|---|
| Soul Knight Prequel, Forja · Reforjar ([anúncio oficial](https://prequel.chillyroom.com/et/article/base/135), imagem 11) | A peça num encaixe no alto do painel central, sobre um suporte (A); a grade de equipamentos à direita com o "+N" no canto de cada peça (B); a quantidade de material "1/10" logo acima do botão | As abas laterais de muitos serviços, a paleta marrom e laranja, as barras verdes |
| Soul Knight Prequel, confirmação de Fundir (imagem 9) | A confirmação por cima da operação, com Cancelar e Confirmar lado a lado e o aviso de que não se desfaz | O texto longo explicando a regra |
| Soul Knight Prequel, ficha da peça (imagem 4) | As ações da peça juntas no pé da ficha | — |
| Elona Mobile, fornalha de encantamento ([blog](https://pzdl-hiraku.hatenablog.com/entry/2021/08/12/185946), a 3ª captura) | Peça à esquerda, material à direita, o resultado no meio: "a peça → o que vem" (o desmontar de A); o valor de agora e o ganho na mesma linha ("耐久 + 8 → +4") | A densidade (duas listas cheias de números e capacidades), a moeda paga (diamantes) |

O acabamento seguiu a HUD aprovada, não esses jogos: nada da paleta alegre, da monetização ou dos sistemas deles.

## A tela (2ª versão, depois do primeiro teste do Jean)

O primeiro balcão punha tudo na página da forja, embaixo da oficina: a página rolava, a arte piscava ao rolar (o
recolhimento ia e voltava em torno do mesmo ponto) e o ouro e os fragmentos sumiam do alto. Pesquisei como Elden
Ring, Diablo IV, Last Epoch e Darkest Dungeon organizam esses serviços (registrado no 25, seção 5.5) e refiz assim:

- **O balcão** tinha três serviços: **Reforçar**, **Desmontar** e **Encantar** (reservado, apagado; saiu na 3ª versão).
- **Cada serviço abre uma janela própria** sobre a coluna do meio, com a moldura das janelas principais do jogo. A
  página não rola; o pisca acabou porque o recolhimento da arte saiu.
- **No topo, sempre à vista:** as abas dos serviços, o ouro e os Fragmentos de Têmpera, e o Fechar (Esc).
- **À esquerda:** em Reforçar, as abas de quem (Jean, Morel, Odette, Bolsa) e a lista das peças; em Desmontar, só as
  peças da bolsa que rendem, cada uma com o retorno. Só a lista rola.
- **À direita:** a peça grande, o passo seguinte linha por linha ("Ataque 4 → 5"), a luta, e "Comparar com uma peça
  da bolsa" (as substitutas que quem usa poderia vestir). **Embaixo, fixo:** o custo como "50 (tem 355) · 2 (tem 7)",
  em vermelho o que falta, e o botão.
- **Esc:** cancela a confirmação; depois fecha a janela (o foco volta ao cartão do serviço); depois sai da forja.

## Decisões aprovadas (seção 5 do 25)

Reforço garantido, sem falha, quebra ou perda; melhora a função principal da peça e não os afixos nem os especiais;
qualidade da base separada do nível de reforço; desmontar devolve parte dos materiais investidos e não transfere o +N;
ouro e material no custo; materiais do grupo, em pilhas, fora dos 12 espaços; exploração e recompensas também dão
material; poucos materiais, de função clara.

## Hipóteses desta rodada (provisórias)

### O que cada peça reforça

| Peça | O que cresce | Por quê |
|---|---|---|
| Arma do Guerreiro | **Fio**: Ataque; ou **Runas**: Poder (escolhido no primeiro reforço, fixo depois) | O caminho arcano (Lâmina Rúnica, Golpe Sagrado, Julgamento Divino) usa Poder; as armas do Guerreiro só têm Ataque na base. A escolha dá identidade à peça sem material por classe |
| Arma do Arqueiro | Ataque | A Agilidade da arma é secundária |
| Arma do Mago (Odette e Yara também) | Poder | — |
| Peito (todas as classes) | Defesa e Vida | As duas linhas da base: a proteção |
| Escudo (apoio do Guerreiro, Morel) | Defesa e Vida | Idem |
| Tomo / Foco Arcano (apoio do Mago) | Poder e Mana | Idem |
| Aljava | **Não neste teste** | Linhas de 1 e 2: qualquer passo inteiro dobra ou triplica o valor. A propriedade dela (por exemplo, a capacidade de flechas) fica para decidir |
| Cabeça, mãos, pernas, pés | Não | Peças complementares, linhas pequenas (65% da força, divididas em duas) |
| Anel, amuleto | Não | A identidade deles são os afixos |

Afixos (do Lobo, da Coruja, da Tartaruga...) e especiais (crítico, roubo de vida, espinhos, vida por turno e por
abate) **não crescem**. A Couraça da Regeneração reforçada ganha Defesa e Vida; a regeneração fica igual.

### A fórmula

Cada + vale **1,5 nível de peça** na linha da base, na mesma proporção que a base tem (o material e o peso da linha
no gerador do jogo): `ganho total no +N = arredonda(qualidade × 0,75 × K × N)`, com `K = 1,5` em arma e peito e
`K = 3` nos apoios (linhas menores). Na arma, a linha única ganha **pelo menos +1 por passo** (senão uma arma
Enferrujada ficava igual do +3 para o +4). Arredondamento meio para cima. Uma base melhor ganha mais por passo; um +4
equivale a uma base do mesmo material uns 6 níveis acima.

| Peça (do gerador) | +1 | +2 | +3 | +4 |
|---|---|---|---|---|
| Martelo Enferrujado, nível 1 (Ataque 2) | +1 | +2 | +3 | +4 → 6 |
| Martelo de Aço, nível 6 (Ataque 6) | +1 | +2 | +3 | +5 → 11 |
| Brigantina de Ferro, nível 1 (Defesa 1, Vida 4) | +1/+2 | +1/+4 | +2/+6 | +3/+8 |
| Manto de Lã Negra, nível 6 (Defesa 2, Vida 12) | +2 Vida | +1/+5 | +1/+7 | +2/+9 |
| Escudo de Aço, nível 3 (Defesa 1, Vida 2) | +1/+1 | +2/+2 | +2/+4 | +3/+5 |
| Tomo, nível 6 (Poder 2, Mana 6) | +1/+2 | +1/+4 | +2/+7 | +3/+9 |
| Lamento de Gharbad, nível 3 (lendário, Ataque 7) | +2 | +4 | +6 | +8 → 15 |

Todo passo melhora pelo menos uma linha (testado do nível 1 ao 12, nos materiais do jogo).

### Custos, limite e materiais

- **Limite:** +4 (o +5 de hoje não é decisão).
- **Custo por passo:** 25 / 50 / 90 / 140 de ouro (com o desconto ou acréscimo da reputação) e 1 / 2 / 3 / 4
  **Fragmentos de Têmpera**. Do +0 ao +4: 305 de ouro e 10 fragmentos. O custo não sobe com o nível da peça:
  reforçar uma base nova rende mais pelo mesmo preço, o que empurra a troca.
- **Um material só nesta rodada:** o Fragmento de Têmpera, para o reforço comum (a função 1 da seção 5.2). Ícone
  provisório (o saco do jogo); sem arte nova. Pilha de até 99, fora da bolsa.
- **Fontes nesta demonstração:** a recompensa de teste no começo (8, identificada como cenário de teste); o baú (metade
  das vezes, 1); a desmontagem. Contratos, chefes e eventos ficam como fontes possíveis, sem números.

### Desmontar, vender e o que fica com a peça

- **Desmontar** (só na forja, só peça da bolsa): devolve **metade dos fragmentos investidos, arredondada para cima**
  (+1: 1 de 1; +2: 2 de 3; +3: 3 de 6; +4: 5 de 10), mais o **material da própria peça** pela raridade (comum 0,
  incomum 1, raro 2, lendário 3). Não devolve ouro. A peça comum sem reforço não rende nada ("venda ou largue").
- **Vender** (no mercado de sempre): a peça reforçada vende por metade do preço, e o preço subiu metade do ouro
  investido: a venda devolve **25% do ouro investido**. Não devolve fragmentos.
- **Equipada:** reforça no corpo de quem usa (herói ou companheiro); para vender ou desmontar, guarda-se na bolsa antes
  (o Inventário do grupo, com as regras de troca da comitiva). A peça que ninguém do grupo usa (o arco, com Morel e
  Odette) não recebe reforço: "Ninguém do grupo usa peças de arqueiro. Venda ou desmonte."
- **Passar a outro integrante:** a peça leva o reforço junto (é a mesma peça), pelo Inventário do grupo.

### Os ciclos (sem criação de recurso)

Reforçar e depois desmontar ou vender sempre deixa o grupo com menos ouro e menos fragmentos do que antes (testado de
+1 a +4, nos dois caminhos). Comprar uma peça no mercado e desmontar troca ouro por no máximo 1 a 3 fragmentos, ao
preço inteiro da peça, limitado ao estoque do mercado (4 peças a cada 3 dias, quase todas comuns, que não rendem).
Nenhum ciclo devolve ouro e fragmentos juntos.

## Resultados observados (na demonstração)

O mesmo alvo em todas as comparações: um Esqueleto do nível do herói (nível 4, defesa 6), sorteio fixo, dano médio do
golpe comum, sem crítico.

- **Investimento inicial:** o Martelo de Ferro do herói (Ataque 3) com Fio: +1 → 8,0 para 8,7; +2 → 9,3 (Ataque do
  herói 12 para 14 na ficha); +3 → 10,0; +4 → 10,7. Custo até o +2: 75 de ouro e 3 fragmentos.
- **A substituta:** o Martelo de Aço do nível 7 (Ataque 7, sem reforço) dá 10,7 no lugar do Martelo de Ferro +2
  (9,3): a base nova já vale mais que o investimento de 75 de ouro. Com o Martelo de Ferro no +4, empatam; reforçar a
  nova passa à frente (+5 no +4). É o "competir por um tempo".
- **A peça especializada:** o Lamento de Gharbad (lendário, nível 3) dá 10,7 contra o Martelo +2, e ainda tem roubo de
  vida e vida por abate, que o reforço não mexe. Ganha +2 de Ataque por passo (a base dele é forte). Vale manter e
  reforçar; a comparação mostra o Ataque, e a ficha mostra os especiais.
- **Companheiros:** o Cajado de Odette (Poder 3) ganha +1 de Poder por passo; Morel compara a substituta pelo golpe
  dele (8,3 → 10,4).
- **Desmontar:** o Arco Curto do Carniceiro (incomum, ninguém usa) rende 1 fragmento; a confirmação nomeia a peça e o
  que volta.

## Para depois (registrado, não feito)

- **Elevar a base de uma peça excepcional** (função 2 dos materiais): um material mais raro ligado a avanço e
  desafios. **Exemplo numérico, simulação:** o Lamento de Gharbad do nível 3 (Ataque 7, roubo 7%, vida por abate 6)
  elevado ao nível 9 viraria Ataque 16, roubo 9%, vida por abate 8, a mesma identidade. Elegibilidade, marcos, custo,
  o material e o que acontece com o reforço que ela já tem (manter, rebaixar, converter) seguem abertos.
- **Encantamento:** efeitos, quantidade por peça, receitas, consumo e substituição, em conversa própria.
- Arte final do material, celebração da melhoria, som novo.
- A propriedade da aljava; o texto do prédio do Ferreiro na vila ("até +5"), que é o da produção.
- Fontes concretas na campanha (contratos, chefes, eventos), coleta, revisão do loot.

## Conferido

- 15 testes (`testes/test_reforco.py`): todo passo melhora algo e nunca cai, do nível 1 ao 12; afixos não crescem;
  peças sem reforço; pagar e aplicar juntos; o veio uma vez; falta de ouro ou de fragmento não cobra nada; o limite;
  companheiro; peça que ninguém usa; desmontar (a conta, a seleção antiga, a peça vestida, a comum que não rende, a
  pilha cheia, a bolsa cheia); os ciclos; o jogo não carrega o protótipo.
- Na tela (1920×945 e 1280×720): a janela cabe sem rolar a página; o duplo clique em "Reforçar" compra um passo só; a confirmação da desmontagem só arma
  depois de um instante e ignora o clique que a abriu; depois de desmontar, nada fica selecionado; a tecla segurada
  não repete; Esc cancela a confirmação.

```bash
python -m unittest discover -s ferramentas/prototipos/reforco/testes -t ferramentas/prototipos/reforco
```

## Roteiro (uns 5 minutos)

1. **Recompensa de teste:** o quadro mostra 8 Fragmentos de Têmpera. "Ir para a vila".
2. **Inventário** (`i`): a seção "Materiais" embaixo da bolsa, com 8; a bolsa continua 6/12.
3. **Forja** (Ferreiro → o ferreiro na oficina) → **Reforçar**. Na aba Jean, o **Martelo de Ferro**: os dois
   caminhos (Fio e Runas), "Ataque 3 → 4", a luta, e embaixo o custo com quanto o grupo tem. **Reforçar · Fio** duas
   vezes (tente o duplo clique: compra um passo só). A ficha lateral mostra o Ataque subir; o topo da janela, o ouro e
   os fragmentos caírem.
4. Ainda no martelo, **Comparar com uma peça da bolsa**: o Martelo de Aço e o Lamento de Gharbad no lugar dele.
5. Aba **Bolsa**, o **Lamento de Gharbad**: a especializada (os especiais na ficha; +2 por passo).
6. Esc fecha a janela. No **Inventário**, vista o Martelo de Aço em você e passe o Martelo de Ferro +2 para Morel (o
   reforço vai junto); na forja, a aba Morel mostra a peça com ele.
7. **Desmontar**: escolha uma peça (cada uma diz quanto rende) → Desmontar… → a confirmação nomeia a peça. Esc ou
   Cancelar desfaz; Esc de novo fecha a janela.
8. **Mercado:** venda uma peça reforçada (o preço inclui 25% do ouro investido). Abra um **baú** (às vezes 1
   fragmento). Tente reforçar sem fragmento suficiente: o botão diz o que falta e não cobra.
