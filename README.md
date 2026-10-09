# Crônicas da Fenda

RPG de texto **offline**, em português. O motor é escrito em **Python puro**, e a tela é uma
interface em HTML que roda localmente, sem internet.
Um RPG **hardcore** e sombrio, no espírito de Diablo: aqui você não é o escolhido.
A fome mata, feridas infeccionam, a noite cega e a morte é permanente. Cada partida gera
um reino diferente: mapa, nomes, chefes, eventos e consequências.

![O dado de Percepção falha, um lobo gélido surge e a luta começa no palco sobre a paisagem](docs/interface.png)

<p align="center">
  <img src="docs/combate.png" width="49%" alt="Combate: as cartas da comitiva e dos inimigos sobre a paisagem; a Bola de Fogo incendeia o alvo">
  <img src="docs/nivel.png" width="49%" alt="Subir de nível: atributos ganhos, ponto de talento e habilidades novas">
</p>
<p align="center">
  <img src="docs/redemoinho.png" width="49%" alt="Redemoinho: a carta do herói vai ao centro e gira quatro vezes">
  <img src="docs/cura.png" width="49%" alt="Odette cura: a carta brilha em verde e o número sobe">
</p>
<p align="center">
  <img src="docs/mapa.png" width="49%" alt="Mapa do reino no estilo da paisagem: regiões pontilhadas com pinheiros, picos e casinhas">
  <img src="docs/comitiva.png" width="49%" alt="Odette aprova muito: o cartão da comitiva surge acima do trecho mais recente, com a ação separada da fala">
</p>
<p align="center">
  <img src="docs/fogueira.png" width="49%" alt="A fogueira: a comitiva em volta do fogo e Yara na reserva, perto da barraca">
  <img src="docs/mural.png" width="49%" alt="Mural de contratos: cartazes de Caça e Procurado pregados no quadro">
</p>
<p align="center">
  <img src="docs/ficha-inimigo.png" width="49%" alt="Ficha do inimigo ao passar o mouse e o clima no topo (Fogo −15%, Gelo +20%)">
  <img src="docs/diario.png" width="49%" alt="Diário como quadro de contratos e o rastreador de contratos no painel da direita">
</p>
<p align="center">
  <img src="docs/talentos.png" width="49%" alt="Árvore de talentos com hover">
  <img src="docs/inventario.png" width="49%" alt="Inventário: boneco com dez espaços e a dica da Agilidade (esquiva, crítico, testes)">
</p>
<p align="center">
  <img src="docs/mercado.png" width="49%" alt="Mercado: quantidade, avisos soltos perto do clique e a seta de voltar">
  <img src="docs/titulo.png" width="49%" alt="Tela de título com uma paisagem sorteada">
</p>
<p align="center">
  <img src="docs/cacada.png" width="49%" alt="Caçada de contrato: a opção Caçar no lugar e o cartão com Seguir os rastros">
  <img src="docs/chamas-mana.png" width="49%" alt="Troll em chamas ×3 e o Meditar enchendo a barra de mana da carta">
</p>
<p align="center">
  <img src="docs/acoes-combate.png" width="49%" alt="Habilidades como cartas: ícone, custo, alvo e dica no hover">
  <img src="docs/chuva-flechas.png" width="49%" alt="Chuva de Flechas: as flechas caem e os três bandidos são atingidos juntos">
</p>

## Como jogar

Precisa do Python 3.8 ou mais novo. Não precisa instalar nada:

```bash
python jogar.py          # ou: python -m rpg
```

O jogo abre no navegador. Ele roda **no seu computador**: o servidor escuta só em
`127.0.0.1` e cada sessão tem uma chave própria. Para jogar numa **janela própria**, como
um programa, instale o `pywebview` (opcional):

```bash
pip install -r requirements.txt   # pywebview (janela própria) e textual (modo terminal)
```

| Opção | O que faz |
|---|---|
| `--navegador` | Abre no navegador mesmo com o `pywebview` instalado |
| `--sem-abrir` | Não abre nada sozinho, só mostra o endereço |
| `--terminal` | Joga dentro do terminal, com painéis (precisa do `textual`) |
| `--classico` | Terminal simples, sem cores especiais e sem dependências |
| `--seed 1234` | Gera sempre o mesmo reino (bom para comparar partidas) |
| `--brando` | Modo brando: ao cair em combate você é resgatado (perde ouro e dois dias) |
| `--velocidade lento\|normal\|rapido\|instantaneo` | Velocidade com que o texto surge |
| `--saves PASTA` | Onde salvar (padrão: `~/.cronicas_da_fenda`) |

O jogo **salva sozinho** sempre que você volta a um local (vila ou região). No modo
hardcore, morrer apaga o save: a morte é permanente de verdade.

### A interface

Pixel art, no espírito de Daggerfall e Tibia, e tudo desenhado em código: não há arquivos de
imagem. Os sprites são grades de pixels no `sprites.js`, sempre desenhados em pixels inteiros da
tela (mesmo com zoom de 125% ou 150% no sistema). As fontes são livres (OFL) e cada uma tem um
papel: a gótica **Jacquard 24** nos títulos e nomes; **Jersey 15** nos números e rótulos curtos;
**Pixelify Sans** na interface; e **Alegreya** na história, feita para leitura longa. O botão "Fonte"
no topo troca só a fonte da história, pela pixel.

- **A história em primeiro lugar.** Uma cena por página, com uma **paisagem em pixel art** no
  topo que muda com o bioma, o período do dia e o clima (chuva, neve, névoa,
  relâmpagos, fumaça das chaminés, estrelas). O texto surge no ritmo da leitura, e **as escolhas só
  aparecem quando ele termina**. Qualquer tecla ou clique mostra tudo de uma vez.
- **HUD no topo, perto do texto.** Retrato, vida e recurso, e os suprimentos **desenhados** com
  um desenho para "tem" e outro para "acabou": pernil ou osso, moedas ou bolsa vazia, tocha acesa
  (que tremula) ou apagada, frasco cheio ou vazio. O número ao lado diz quanto, e tudo pisca e
  mostra `+3`/`−1` quando muda. Na luta, a linha de suprimentos dá lugar ao palco.
- **Combate em palco.** Ao começar uma luta, a paisagem do lugar vira o chão da batalha: a sua
  carta e a da comitiva de um lado, os inimigos do outro. **Uma ação por vez**: quem age dá um
  passo à frente e avança até o alvo, o alvo treme e mostra o dano. Cada elemento tem cor e som
  próprios: a Bola de Fogo voa e deixa labaredas, o gelo cristaliza, a luz sagrada brilha, a
  sombra escurece. O **Redemoinho** leva a sua carta ao centro e gira quatro vezes, com quatro
  golpes. Cura brilha em **verde**, roubo de vida em **vermelho**, proteção em **azul**, e os
  efeitos (veneno, chamas, guarda, maldição...) ficam como ícones na carta. Para escolher o alvo,
  clique na carta do inimigo. O texto fica enxuto: uma linha curta por golpe, e a página guarda
  só o turno anterior (apagado) e o atual (o histórico guarda tudo).
- **A comitiva reage onde você está lendo.** Quando um companheiro aprova, desaprova ou fala, um
  **cartão** com o retrato surge logo acima do trecho mais recente (`▲ Morel aprova`), com o que
  ele faz em itálico separado do que ele diz, fica alguns segundos e some (clique para fechar).
  Na luta, a fala sai num balão da carta dele.
- **Momentos que importam têm festa.** Vitória com faixa e fanfarra; **subir de nível** abre uma
  tela com os atributos ganhos, o ponto de talento e as habilidades novas; Sigilos,
  especialização e novos companheiros também ganham destaque. O d20 rola na tela nos testes,
  com som de sucesso ou falha.
- **Viaje clicando no mapa.** O mapa (lateral, na página e em tela cheia com `M`) é desenhado no
  mesmo estilo da paisagem: manchas pontilhadas de cada bioma, pinheiros, picos nevados, juncos,
  colunas, casinhas com janela acesa, e a cor muda com a hora do dia. A névoa cobre o resto.
  Clique num destino.
- **Árvore de talentos de verdade:** três colunas, ícones, graus, cadeados, passe o mouse para
  ver o efeito e clique para aprender.
- **Inventário de verdade:** um boneco com **dez espaços** (cabeça, amuleto, peito, mãos, arma,
  mão secundária, pernas, pés e dois anéis) e a mochila em grade. **Arraste** itens para equipar,
  para tirar ou para a caveira (largar); dois cliques também funcionam. Passe o mouse para ver
  os atributos e a **comparação com o que está equipado** (▲ verde, ▼ vermelho).
- **Mercado interativo:** vitrine de suprimentos e equipamentos com preço e comparação.
  Suprimentos têm **quantidade** (`−`/`+`, segurar acelera, Shift+clique compra 5) e **estoque**: cada
  vila tem poucas unidades de cada consumível por dia, e reabastece toda manhã.
  Equipamento comprado para um espaço vazio do corpo **já sai vestido**: o ícone voa da vitrine
  até o espaço do boneco, que brilha ao receber. Na mochila, clicar num item abre um menu com
  **Equipar** ou **Vender**, e nada é vendido sem você confirmar. A venda paga exatamente o
  "Vender por" mostrado (metade do preço), com um som só.
- **Nada some lá embaixo:** nas telas desenhadas (mercado, inventário), o que acontece
  (`−16 ouro`, `Tocha ×4`) aparece **solto na tela, perto de onde você clicou**. E "Voltar" virou
  uma **seta fixa** no canto da página, que também responde ao `Esc`.
- **Telas desenhadas:** Diário (cartas de contratos, rumores e do inimigo), Bestiário (fichas
  com fraquezas) e Comitiva (clique num companheiro para conversar ou mandá-lo ao acampamento).
- **Contratos sempre à vista:** no painel da direita, abaixo do mapa, cada contrato mostra o alvo,
  o lugar, a distância e o progresso, e o lugar ganha um "!" no mapa. Clique para viajar até lá.
  O Diário virou um quadro como o mural, com Abandonar em cada cartaz.
- **Ações de combate como cartas:** Habilidades e Itens abrem cartas com ícone, custo (mana,
  vigor, foco, flechas), alvo e dica no hover; o que você não pode pagar fica apagado. Em
  Itens dá para trocar de arma ou de mão secundária no meio da luta, ao custo do turno
  (armadura não).
- **Área acerta junto:** Chuva de Flechas faz chover flechas sobre todos os alvos ao mesmo
  tempo; o Inferno abre o chão sob todos de uma vez. O Redemoinho avança e corta todos os alvos em cinco giros rápidos, com o total de dano no fim.
- **Contratos do seu tamanho:** o mural sorteia lugares de nível próximo ao seu (de um abaixo
  até dois acima), e ouro e XP crescem com o nível do lugar: trabalho fácil paga pouco.
- **Itens com bom senso:** o jogo avisa em vez de gastar poção com vida cheia ou bandagem sem
  ferida. Fora de combate, poção e bandagem também servem na comitiva (clique na poção e escolha
  em quem); a bandagem põe de pé um companheiro caído.
- **Doca de atalhos:** Talentos, Grimório, Inventário, Comitiva · Mapa, Diário, Bestiário · Salvar, Sair,
  em botões de ícone com a tecla no canto e selos de aviso (pontos de talento, carta). A doca
  é uma barra própria, fixa embaixo da página (fora do texto da história): não pula de lugar a
  cada cena. Ela **continua viva dentro das telas que abre**: do Inventário, clique em Comitiva
  (ou aperte `C`) e o jogo volta e abre a outra sozinho; clicar no atalho da tela aberta (marcado
  em dourado) fecha a tela. O **Mapa** abre por cima de qualquer tela (é consulta; de lá também
  se viaja). **Viajar** continua no menu do lugar: é a ação, e mostra o mapa com os destinos.
- **Flechas na carta:** o arqueiro vê as flechas na própria carta da luta, piscando quando
  estão acabando. Sem flechas, o ataque vira um golpe de adaga fraco e os tiros ficam bloqueados.
- **Voltar sem caçar o botão:** na luta, "Voltar" vira a última carta da grade (e Esc volta um
  passo em qualquer tela).
- **Botão direito faz atalhos:** no mercado, vende o item da mochila na hora (sem abrir o menu);
  no inventário, equipa o item da mochila ou tira o do corpo; na bolsa, usa o consumível em você.
  Ele não volta mais de tela.
- **Poção e bandagem na comitiva, em plena luta:** se alguém ao seu lado (comitiva ou animal) está
  ferido, a poção e a bandagem perguntam em quem usar, e as cartas acendem como na mira de um
  golpe. Gasta o seu turno. A bandagem estanca o sangramento de quem a recebe.
- **Ordem da Fera (Patrulheiro):** no lugar do antigo "Comando: Atacar!", que repetia o que o
  animal já faz sozinho, uma ordem que ele não dá por conta própria: o **urso protege** (ataca e
  provoca: por 2 turnos os inimigos atacam ele, que recebe 30% menos dano), o **lobo dilacera**
  (160% e sangramento forte) e o **falcão cega** (não pode ser esquivado e enfraquece o alvo).
- **Tiro Duplo em rajada:** a segunda flecha sai quando a primeira está chegando: dois acertos
  separados, um logo atrás do outro.
- **Quem age fica por cima:** quando você manda outro agir (Ordem da Fera, poção na comitiva), a
  carta dele e a faixa da ação ("Provocando") passam à frente da sua, mesmo com a sua em foco.
- **O animal do Patrulheiro é da família:** aparece na ficha, na Comitiva (retrato, nome, vida);
  poção e bandagem da bolsa servem nele (a bandagem põe de pé quem caiu); na fogueira ele dorme
  perto do fogo e, clicando nele, dá para **fazer carinho** (corações; uma vez por noite, e ele
  entra na primeira luta do dia seguinte **animado**, com +15% de dano), enfaixar ou dar poção.
  Ele não come das provisões: caça a própria comida.
- **Clique que não se perde:** clicar num atalho (o ponto de talento piscando, Talentos, Inventário,
  ou a tecla dele) enquanto o texto ainda corre ou uma cena espera não é mais ignorado: o texto
  corre de uma vez, o "Continuar" é aceito, um aviso diz que a tela abre assim que a cena terminar,
  e ela abre sozinha quando o lugar voltar. Escolhas da cena (um evento, o item encontrado) vêm
  primeiro.
- **Mapa limpo:** sem a dica do navegador sobre os lugares (o nome e o nível já estão escritos), e o
  lugar com contrato não ganha mais a sombra do cartaz do mural.
- **Trocar pelo item encontrado:** "Equipar agora" faz o ícone voar do cartão até o espaço do
  corpo, que brilha; o cartão vira "Vestido" e o antigo, apagado, "Foi para a mochila".
- **Duelo é duelo:** nos duelos de honra a comitiva e o animal ficam de fora, assistindo.
- **Fogueira sempre:** acampar mostra a fogueira desenhada mesmo quando você está sozinho. Na
  fogueira dá para usar poção e bandagem (em você ou na comitiva) antes de dormir.
- **Caçada garantida:** no lugar de um contrato de caça aparece "Caçar … (contrato, 1/3)" (e o
  cartão do contrato pisca com "Seguir os rastros ▸"). Seguir os rastros sempre leva ao bicho; a
  Percepção decide quem vê quem primeiro. Cada abate mostra o progresso.
- **Mana visível:** Meditar, o Tônico e os talentos que devolvem recurso enchem a barra da carta
  com brilho azul e "+N mana".
- **Mural de contratos** como um quadro de cortiça: cada contrato é um cartaz pregado (Caça,
  Procurado, Entrega) com o alvo, o lugar, a distância, o nível do perigo, a recompensa em
  ouro e XP e o botão Aceitar. Os seus contratos aparecem embaixo, com o progresso da caça e o
  botão Abandonar.
- **Atributos explicados:** passe o mouse em Ataque, Defesa, Agilidade e Poder (no painel e na
  tela de personagem) para ver o que cada um faz com os números de agora: quanto a Defesa
  reduz do dano, a chance de esquiva e de crítico da Agilidade, o bônus nos testes e o que
  você ganha com mais um ponto. A Reputação também: título (Respeitado, Malvisto...), desconto
  no mercado, bônus de Carisma e o que muda no mundo.
- **Clima que pesa:** os efeitos do clima e da hora ficam no topo (e no canto da luta) com
  ícone e número, como `Fogo −15%` na neve ou `Inimigos +10%` à noite. Passe o mouse para ler.
- **Ficha do inimigo:** na luta, passe o mouse na carta de um inimigo: traços e, depois de
  algumas caçadas (Bestiário), as fraquezas e resistências por elemento (×1,5 contra fogo...).
- **Item encontrado:** o saque aparece como um cartão com o sprite, a raridade (raios na cor
  dela), os bônus e a diferença para o que você usa, que fica ao lado. Deixar para trás só
  existe com a mochila cheia.
- **Sua vez na luta:** sua carta vem para a frente e cresce, e as ações surgem em arco ao lado
  dela (Atacar, Habilidades, Itens, Fugir, teclas 1–4). Habilidades e Itens abrem uma janelinha
  logo abaixo da arena (os alvos ficam à vista), com ícone, nome e custo; passar o mouse mostra o que
  faz, o dano e acende quem seria atingido. Escolhida a
  habilidade, os inimigos acendem: clique no alvo. Esc ou um clique fora fecham a
  janelinha e desfazem a escolha antes de gastar qualquer coisa; as ações em arco continuam ali.
  O alvo de cada habilidade usa os termos de sempre: **Inimigo único**, **Todos os inimigos**,
  **Você**, **Aliado único**, **Todos os aliados**.
- **Roubo de vida que se vê:** gotas de sangue saem de quem apanhou e voam até quem bateu; só então
  a vida sobe, com `+N ♥` em verde e o nome da fonte (Sede Insaciável, Sede de Sangue, Drenar
  Vida). O roubo passivo arredonda (e é pelo menos 1): antes, golpes pequenos truncavam para zero.
- **Crítico explicado:** o crítico garantido diz de onde veio (`CRÍTICO (Tiro de Abertura)!`,
  Iniciativa, Furtivo), com um selo dourado na carta. O Grimório lista o que soma além da ficha
  (Tiro Certeiro +30%, Execução +20%, primeiro tiro garantido...), e o registro da partida separa
  críticos garantidos dos da sorte.
- **Cores nos textos de regra:** como nos RPGs atuais, dicas, Grimório, talentos e o registro da
  luta destacam cada termo com a sua cor: fogo em laranja, sangramento e roubo de vida em
  vermelho, cura em verde, crítico em amarelo, gelo em azul-claro, veneno em verde-ácido, sombra em
  roxo, mana em azul, esquiva e proteção em tons frios, e os números de dano em negrito. No
  pergaminho do Grimório, as mesmas cores em tinta escura. A prosa da história fica sem realce.
- **Talentos por cima:** a árvore abre sobre a página, como o Grimório, sem trocar a cena de trás.
- **Ritmo do golpe:** quem ataca volta para o lugar logo depois do impacto, sem ficar parado à
  frente esperando o roubo de vida ou o contra-ataque; o contra-ataque também volta inteiro.
- **Grimório (P):** um livro com cada habilidade e o ataque básico: o dano de agora (faixa,
  crítico e chance), de onde ele vem (Poder 40 × 150% × talentos) e quanto cresce a cada ponto de
  atributo, além de efeitos como queimadura, sangramento e cura com os números do seu herói.
- **Comparar com Shift:** passe o mouse num item (mochila, mercado) e segure Shift para ver o que
  você está usando naquele espaço, inteiro, ao lado.
- **Bolsa à mão:** a bolsa do painel esquerdo se usa com um clique, em qualquer menu de lugar; na
  luta, o clique passa pelo "Itens" (e gasta o turno).
- **Ferimentos explicados:** cada ferimento diz o que tira (−25% Ataque...), quanto falta para
  sarar e se pode infeccionar, quando acontece e ao passar o mouse.
- **Espinhos à vista:** o dano devolvido pela armadura com Espinhos salta em farpas até o agressor.
- **Ataque básico alimenta o combo:** cada golpe simples que acerta devolve um pouco de mana,
  vigor ou foco (4% do máximo).
- **Testes de dado explicados:** passe o mouse no selo do teste (`FOR +8`) para ver de onde vem
  o bônus e a chance aproximada. Os atributos ajudam com retorno decrescente e a dificuldade
  sobe um pouco com o seu nível, então o fim de jogo não vira sucesso garantido.
- Som ambiente e efeitos sintetizados na hora. Funciona em monitor largo, notebook e celular.
  Recarregar a página não perde nada.

| Tecla | O que faz |
|---|---|
| `1`–`9`, `0`, setas + Enter, clique | Escolher uma opção |
| clique na carta do inimigo | Escolher o alvo na luta |
| `T` `P` `I` `C` `D` `B` `G` `Q` | Talentos, Grimório, Inventário, Comitiva, Diário, Bestiário, Salvar, Sair (nos menus de local) |
| clique no mapa | Viajar para aquele destino |
| qualquer tecla durante o texto | Mostrar o texto inteiro |
| `Espaço`/`Enter` | Continuar ▸ |
| `M` | Mapa do reino |
| `H` ou `F2` | Histórico completo da partida |
| `V` ou `F3` | Velocidade do texto |
| `S` | Liga/desliga o som |
| `Esc` ou `Backspace` | Voltar (seta ◀) · fecha mapa e histórico |

## Equipamento

Dez espaços no corpo, cada classe com suas peças: o guerreiro usa elmo, manoplas, grevas e
**escudo**; o arqueiro, capuz, braçadeiras e **aljava**; o mago, chapéu ou diadema, luvas de seda
e **tomo**. Amuleto e dois anéis servem a todos. Os itens vêm em quatro raridades (comum,
mágico, raro e lendário) com afixos aleatórios, e há itens únicos com história, como a Égide
do Mártir, as Botas do Andarilho Morto e a Coroa dos Afogados. O ferreiro reforça arma, peito
e mão secundária. A mochila guarda 12 itens.

## A comitiva

Você não precisa caminhar sozinho, e talvez não deva. Três companheiros podem cruzar o seu caminho
(dois andam com você; quem sobra espera no acampamento). Cada um tem **valores próprios**, e eles **discordam entre si**:

| Companheiro | Quem é | Em combate | Admira | Despreza |
|---|---|---|---|---|
| **Sister Odette** | Clériga que fugiu da catedral na noite em que a Fenda se abriu | Cura quem estiver morrendo | misericórdia, fé, honestidade | crueldade, sacrilégio, magia proibida |
| **Bastian Morel** | Ex-capitão mercenário dos Iron Hounds | Atrai os golpes para si e atordoa | coragem, pragmatismo, honra | fuga, autoridade, caridade "inútil" |
| **Yara** | Bruxa do brejo, quase queimada; a Fenda fala com ela | Amaldiçoa e ataca com magia | magia proibida, curiosidade, rebeldia | fé, autoridade, fanatismo, purificar |

- **Aprovação.** 117 escolhas, em 49 eventos, têm peso moral. Quando você escolhe,
  cada companheiro reage (um selo `▼ Odette desaprova muito` salta do retrato) e às vezes diz o
  que pensa, num balão. Na luta também soltam uma frase de vez em quando. Passe o mouse na barra
  de aprovação para ver o que ela muda (força em combate, conversas, partida). Quem confia
  em você luta melhor; abaixo de um certo ponto, vai embora, e nem todos vão em paz.
- **Conversas** no acampamento ou no menu **Comitiva** (`C`): cada um tem uma história que
  só se abre com confiança.
- **Missões pessoais em três atos**, com escolhas que mudam o companheiro para sempre: a
  mãe de um acólito morto, um tenente que sobreviveu à Varn Bridge, um círculo de pedras
  negras onde uma porta pode ser fechada ou aberta de vez. Algumas dessas escolhas mudam
  quem estará ao seu lado (ou contra você) no salão do trono.
- **Discussões** entre companheiros: às vezes você vai ter que tomar partido.
- **O acampamento.** Quem sai da comitiva não some: vai **esperar no acampamento**. Quando
  você acampa à noite, abre a cena da **fogueira**: você e a comitiva em volta do fogo e quem
  está na reserva perto da barraca. Clique em alguém para conversar (o ✉ mostra quem tem algo
  a dizer), levar alguém da reserva no lugar de outro ou deixar alguém descansando. Quem fica
  no acampamento se recupera, não come das suas provisões e não opina nas suas escolhas.
- **O preço:** cada companheiro come uma provisão por dia, Morel cobra soldo, grupos
  atraem mais inimigos, os inimigos resistem mais e o XP é dividido (só quem anda com você). Quem cai em combate
  fica desacordado e só volta a lutar depois de uma noite de descanso (ou de passar pelo templo).

## O objetivo

Uma Fenda para o Vazio se abriu no reino. Três **guardiões** guardam os **Sigilos**
que abrem o caminho até a Cidadela, onde o vilão (gerado a cada partida) espera.

- O **nível dos inimigos depende da região**, não do seu. Quanto mais longe da vila
  inicial, mais perigoso (o mapa mostra o "Nv." de cada lugar). Os guardiões têm nível
  fixo e o chefe final é nível 11. Correr direto para os chefes não funciona:
  é preciso evoluir, equipar-se, aprender fraquezas e recrutar aliados.
- **Quanto mais perto da Fenda**, a leste, rumo à Cidadela, mais criaturas dela (caídos, cães
  infernais, crias do Vazio, abominações) e mais feras tocadas pelo Vazio.
- **A morte é permanente.** (No modo `--brando`, alguém te resgata e você acorda numa
  vila, perdendo ouro e dois dias.)

## Sobrevivência

- **Fome:** cada dia consome 1 provisão. Sem comida você fica fraco, não se recupera
  dormindo e, depois de alguns dias, começa a morrer. Compre comida nas vilas, cace ou
  saqueie.
- **Ferimentos:** golpes pesados deixam marcas que duram dias (costelas quebradas,
  braço fraturado, perna torcida, cortes, queimaduras...) e reduzem seus atributos.
  Feridas abertas precisam de bandagem, ou podem **infeccionar**. A infecção causa febre
  e mata se não for tratada com unguento ou por um curandeiro.
- **Escuridão:** à noite, nas ruínas e na Cidadela, você precisa de tochas. Sem luz, você
  fica pior em percepção e destreza e é emboscado com mais facilidade.
- **Cura lenta:** acampar recupera 30% da vida (18% na chuva, neve ou tempestade); a
  taverna, 35%; para voltar inteiro, o templo cobra. Poções são caras e o mercado de cada vila tem
  poucas (o estoque reabastece toda manhã). Depois de uma luta, vigor e foco voltam só pela metade, e a
  mana do mago, 20%. Uma noite ao relento devolve 75% do vigor/foco e metade da mana; só a
  cama da taverna enche tudo.
- **Inimigos perigosos:** bandos de **campeões** (vários inimigos com o mesmo afixo),
  **únicos** nomeados com escolta, caídos com xamãs que **ressuscitam** os irmãos,
  carniçais que **devoram** cadáveres para se curar.

## Saque

Itens têm raridade, como em Diablo:
**comum** · mágico (azul, 1 afixo) · raro (amarelo, 2–3 afixos, nome próprio) ·
**★ lendário** (itens únicos com nome, história e efeitos especiais).
Afixos especiais: roubo de vida, chance de crítico, espinhos, vida por turno e vida por abate.

## Mapa

O reino é gerado no espaço: regiões de bioma contínuas e estradas que não se cruzam.
O mapa mostra o que você já descobriu (o resto fica na névoa):

```
   ⌂1─────────@5───          @ você   ⌂ vila   ♣ floresta   ≈ pântano
              ╲  ╲──Π4        ▲ montanha   ∴ planície   Π ruínas
               ╲              ☠ covil   ✓ covil vencido   ♜ cidadela
                ∴7─────☠9
```

Os números do mapa são os mesmos do menu de viagem, que avisa quando um destino é
perigoso demais para o seu nível.

## Árvore de talentos

Cada classe tem uma árvore em 3 colunas: o **tronco comum** no meio e, nas laterais,
talentos que **só funcionam com uma das especializações**. Você ganha 1 ponto por nível
e 1 por guardião derrotado (não dá para pegar tudo):

```
            ← PALADINO          TRONCO COMUM          BERSERKER →
Nv.2    [Pele de Ferro 2/3]  [Golpe Brutal 1/3]    [Fôlego 0/2]
Nv.4    [Luz Curativa 1/2]   [Contra-ataque 0/2]   [Sede Insaciável 0/2✗]
Nv.6    [Aura de Proteção]   [Muralha 0/1]         [Frenesi 0/2✗]
Nv.9    [Martírio 0/1]                             [Imortal 0/1✗]
```

## Classes e especializações

No **nível 4** um evento narrativo da sua classe te obriga a escolher um caminho:

```
Guerreiro (Vigor) ──┬── Paladino     cura, dano sagrado, forte contra mortos-vivos
                    └── Berserker    quanto mais ferido, mais forte; rouba vida; ataques em área
Arqueiro  (Foco)  ──┬── Patrulheiro  companheiro animal (lobo, falcão ou urso), tiro duplo
                    └── Sombra       furtividade, veneno, execuções e críticos devastadores
Mago      (Mana)  ──┬── Piromante    acende chamas em camadas e detona com a Combustão
                    └── Necromante   drenar vida, erguer servos esqueletos, maldições
```

Cada classe tem uma mecânica própria:
- **Guerreiro:** o vigor regenera rápido; erguer o escudo reduz o dano pela metade.
- **Arqueiro:** usa **flechas** (que acabam). Começa com 20, e a aljava leva 30 (+5 por ponto
  em Aljava Funda). Esquiva e crítico têm teto de 60% (nem o mais ágil é intocável). Depois da luta dá para recolher cerca de um terço do que atirou; o
  resto se compra em feixes de 5 ou se acha com bandidos. É ótimo contra voadores.
  Quando avista inimigos antes, escolhe entre **atacar de surpresa** (turno livre e o
  primeiro golpe é crítico) e **subir num ponto alto** (teste de Destreza: quem luta corpo a
  corpo perde o 1º turno escalando e você causa +15% por 3 turnos; não adianta contra quem
  voa ou conjura).
- **Mago:** a mana é escassa: regenera pouco durante a luta, recupera só 20% depois dela e
  enche de verdade apenas descansando. O Dardo Arcano é de graça; cada Inferno é uma
  decisão.
- **Fogo em camadas (Piromante):** Bola de Fogo e Inferno acendem o alvo; cada acerto soma uma
  camada (até ×3), e uma camada sozinha arde pouco. A **Combustão** detona tudo o que ainda
  arderia, de uma vez, e fica mais forte com mais camadas. Sem chamas, é um estalo fraco.

Novas habilidades chegam nos níveis 2, 3, 4 e 7 (a habilidade suprema da especialização).

## O que deixa as jornadas diferentes

- **Mundo procedural:** mapa em grafo com vilas, regiões selvagens, covis e a Cidadela.
  Nomes de lugares, NPCs, guardiões e do vilão são gerados a cada partida.
- **88 eventos** com pesos dinâmicos. O que pode acontecer depende de classe,
  especialização, bioma, clima, período do dia, reputação, perigo do lugar e das suas escolhas
  anteriores. Eventos vistos recentemente perdem peso, para não repetir.
- **Eventos de classe e especialização:** caçar, fabricar flechas, derrubar um falcão
  mensageiro ou disputar torneios de tiro como arqueiro; duelos de honra e um ferreiro
  itinerante para o guerreiro; anomalias arcanas, grimórios e linhas ley para o mago;
  contratos da Irmandade para a Sombra; cemitérios para o Necromante...
- **Consequências que voltam:** quem você ajuda (ou rouba) pode reaparecer dias depois:
  um viajante grato com um presente, um bandido poupado que vira aliado (ou traidor), um
  ladrão que fugiu com seu ouro, a família da criança perdida...
- **Aliados na batalha final:** muitas boas ações recrutam ajuda para o confronto final.
- **Nêmesis:** se você fugir de uma criatura de elite, ela volta mais forte para te caçar.
- **Rumores:** nas tavernas você ouve sobre tesouros, feras lendárias, mercadores raros e
  pontos fracos dos guardiões (+25% de dano). Alguns rumores são falsos.
- **Bestiário:** fraquezas e habilidades de cada criatura só aparecem depois de você
  derrotar algumas (magos estudam à primeira vista). Com 5 abates você vira mestre
  caçador daquela criatura (+10% de dano).
- **Legado entre partidas:** heróis anteriores deixam marcas no próximo mundo: o túmulo
  de quem caiu (com a arma dele e um espírito aliado), a estátua de quem venceu e
  baladas nas tavernas.
- **Inimigos com afixos** (feroz, ancião, corrompido, flamejante...), **traços**
  (voador, blindado, etéreo, morto-vivo...) e **fraquezas**. Passe o mouse na carta do
  inimigo (ou use *Analisar inimigos* no terminal).
- **Clima e período do dia:** chuva enfraquece o fogo, a névoa ajuda a esquivar, a
  tempestade atrapalha disparos e à noite os monstros ficam mais fortes.
- **Contratos** no mural das vilas: caçadas, alvos com recompensa e entregas (com
  imprevistos no caminho). Dá para abandoná-los pelo Diário, perdendo reputação. Caçadas e
  alvos ganham a ação "Caçar"/"Rastrear" no próprio lugar, com encontro garantido.

## Estrutura do código

```
rpg/
  jogo.py          o estado da partida e o ciclo principal (menus do lugar, explorar, viajar)
  sistemas/        cada sistema do jogo é um mixin da classe Jogo:
    loja.py          mercado: regras de compra e venda (as mesmas para terminal e web)
    contratos.py     mural, caçadas, recompensa, diário e abandono
    inventario.py    equipamento, mochila, consumíveis e a tela de personagem
    confronto.py     inimigos do lugar, grupos, o combate em si, abates e saque
    progressao.py    níveis, talentos, habilidades, especialização
    tempo.py         clima, períodos, dias, descanso, acampamento e taverna
    recompensas.py   ouro, XP, vida, itens, reputação, sementes e rumores
    testes.py        testes de atributo (d20 + bônus contra a dificuldade)
    navegacao.py     viagem e mapa · chefes.py guardiões e batalha final
    bestiario.py     legado e bestiário · servicos.py ferreiro, curandeiro, rumores
    finais.py        morte, vitória e resumo · persistencia.py salvar, carregar, sair
  balanceamento.py todos os números de dificuldade e generosidade, num lugar só
  migracoes.py     versão do save e as migrações de saves antigos
  regras.py        constantes e exceções compartilhadas
  combate.py       combate por turnos, efeitos, traços, fraquezas e os "lances" para a tela
  comitiva.py      companheiros: valores, aprovação, reações, combate, conversas, partida e morte
  web/             interface principal: servidor local (só biblioteca padrão) + página
    ponte.py       WebUI: cada chamada da UI vira uma mensagem JSON (cenas, texto, dados, escolhas)
    estado.py      fotografia do jogo em JSON (herói, mapa, combate) para os painéis
    servidor.py    HTTP + SSE em 127.0.0.1, com token por sessão
    static/
      css/         estilos por componente (01-base ... 13-realce), carregados nessa ordem
      app/         a aplicação: nucleo (conexão e fila), pagina, escolhas, paineis, controles
      realce.js    cores dos termos de jogo nos textos de regra
      batalha.js   palco da luta, balões e selos · telas.js talentos, fichas, mercado, fogueira
      sprites-dados.js os desenhos em pixel art · sprites.js quem os desenha
      vista.js, mapa.js, som.js, fontes OFL
  tui.py           interface de terminal com painéis (Textual), via --terminal
  ui.py            interface clássica (cores ANSI, menus) e o "jogador robô" dos testes
  habilidades.py   habilidades como dados: blocos que executam na luta e se descrevem no Grimório
  grimorio.py      o livro de habilidades e a conta de crítico (a mesma do combate e da ficha)
  classes.py, inimigos.py, itens.py, talentos.py, dados.py, mundo.py, mapa.py, texto.py,
  legado.py, sobrevivencia.py, telemetria.py
  eventos/         motor de eventos e os eventos (comuns, biomas, classe, noite, vila, comitiva)
tests/
  test_simulacao.py  robôs jogando, sistemas, saves antigos
  gabarito.py        18 partidas de referência: refatorar não pode mudar nenhuma (veja abaixo)
  navegador/         teste de fumaça da interface web (Playwright), pulado se não houver Node
```

Mais detalhes em [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md) (como o motor funciona),
[`docs/COMO_CRIAR.md`](docs/COMO_CRIAR.md) (receitas: habilidade, evento, número) e
[`docs/ROADMAP.md`](docs/ROADMAP.md) (as etapas da refatoração e o que vem depois).

### Refatorar com segurança

`python -m tests.gabarito` joga 18 partidas com sementes fixas (3 classes × 3 sementes, pelo
terminal e simulando a interface web) e compara a transcrição completa de cada uma (texto,
opções, escolhas, lances de combate e o save final) com `tests/gabarito.json`. Uma refatoração
que não muda a jogabilidade passa sem tocar no gabarito. Quando a mudança de jogabilidade é de
propósito (um número em `balanceamento.py`, por exemplo), rode `python -m tests.gabarito
--atualizar` e diga no commit o que mudou. `--mostrar` grava as transcrições para comparar com
`diff`.

### Criando um evento novo

```python
from .motor import evento

@evento(contextos=("explorar", "viagem"), peso=6, cooldown=10,
        cond=lambda g: g.j.classe == "arqueiro" and g.clima == "nevoa")
def vulto_na_nevoa(g):
    g.dizer("Um vulto se move na névoa...")
    op = g.menu("O que faz?", [("Atirar", "atirar"), ("Esperar", "esperar")])
    if op == "atirar" and g.teste("percepcao", 13):
        g.ganhar_xp(15)
    else:
        g.combate(g.grupo())
```

Ferramentas úteis dentro de um evento: `g.menu`, `g.teste`, `g.combate`, `g.grupo`,
`g.inimigo`, `g.ganhar_ouro`, `g.ganhar_xp`, `g.dar`, `g.oferecer_equip`,
`g.mudar_reputacao`, `g.plantar`/`g.colher` (consequências futuras) e `g.aliado_final`.

## Registro da partida (para análise de equilíbrio)

O jogo grava automaticamente, só no seu computador, um registro de cada partida em
`~/.cronicas_da_fenda/runs/` (ou na pasta passada em `--saves`):

- `AAAA-MM-DD_HHMM_nome_classe.md` — resumo legível: progressão por nível, ordem dos
  talentos, combates por nível (dano causado e recebido, vida perdida, maior golpe,
  recurso no fim, turnos), e o detalhe do que cura e protege (defesa no início da luta, cura
  recebida, roubo de vida, dano absorvido, críticos, erros, esquivas, dano e quedas dos
  aliados), dano por elemento e por aliado, chefes, economia (compras, vendas, ferreiro), saque
  encontrado e o que você fez com ele, equipamento no fim, comitiva, ferimentos e eventos.
  O cabeçalho diz a versão do registro, a versão do jogo e a interface usada.
- `AAAA-MM-DD_HHMM_nome_classe.jsonl` — tudo, evento por evento.

O registro é atualizado ao morrer, vencer, salvar ou sair. Para reler um `.jsonl`:
`python -m rpg.telemetria ARQUIVO.jsonl`.

## Testes

```bash
python -m unittest discover tests
```

Um "jogador robô" joga dezenas de partidas com escolhas aleatórias, força cada evento
em todas as classes e especializações, testa as árvores de talentos e o mapa, joga uma
partida inteira pela interface web (por HTTP, como um navegador faria, conferindo também o
token e a recarga da página) e testa a interface Textual em modo headless.
