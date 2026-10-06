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
papel: a gótica **Jacquard 24** só nos títulos grandes; **Alegreya SC** (versalete) nos
cabeçalhos, nomes e botões; **Alegreya** na história, feita para leitura longa; **Alegreya Sans**
na interface miúda; **Jersey 15** nos números. O botão "Fonte" no topo volta às fontes pixel.

- **A história em primeiro lugar.** Uma cena por página, com uma **paisagem em pixel art** no
  topo que muda com o bioma, o período do dia, o clima e a corrupção (chuva, neve, névoa,
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
  Suprimentos têm **quantidade** (`−`/`+`, segurar acelera, rodinha do mouse, Shift+clique compra 5).
  Equipamento comprado para um espaço vazio do corpo **já sai vestido**. Na mochila, clicar num
  item abre um menu com **Equipar** ou **Vender**, e nada é vendido sem você confirmar.
- **Nada some lá embaixo:** nas telas desenhadas (mercado, inventário), o que acontece
  (`−16 ouro`, `Tocha ×4`) aparece **solto na tela, perto de onde você clicou**. E "Voltar" virou
  uma **seta fixa** no canto da página, que também responde ao `Esc`.
- **Telas desenhadas:** Diário (cartas de contratos, rumores e do inimigo), Bestiário (fichas
  com fraquezas) e Comitiva (clique num companheiro para conversar ou mandá-lo ao acampamento).
- **Contratos sempre à vista:** no painel da direita, abaixo do mapa, cada contrato mostra o alvo,
  o lugar, a distância e o progresso, e o lugar ganha um "!" no mapa. Clique para viajar até lá.
  O Diário virou um quadro como o mural, com Abandonar em cada cartaz.
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
- **Ficha do inimigo:** na luta, passe o mouse na carta de um inimigo: traços, fraquezas e
  resistências por elemento (×1,5 contra fogo...) e os golpes que ele usa, se você já conhece a
  espécie (Bestiário).
- **Testes de dado explicados:** passe o mouse no selo do teste (`FOR +8`) para ver de onde vem
  o bônus e a chance aproximada. Os atributos ajudam com retorno decrescente e a dificuldade
  sobe um pouco com o seu nível, então o fim de jogo não vira sucesso garantido.
- Som ambiente e efeitos sintetizados na hora. Funciona em monitor largo, notebook e celular.
  Recarregar a página não perde nada.

| Tecla | O que faz |
|---|---|
| `1`–`9`, `0`, setas + Enter, clique | Escolher uma opção |
| clique na carta do inimigo | Escolher o alvo na luta |
| `T` `P` `C` `D` `B` `G` `Q` | Talentos, Personagem, Comitiva, Diário, Bestiário, Salvar, Sair (nos menus de local) |
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
  pode morrer de verdade (Odette por perto ajuda a evitar).

## O objetivo

Uma Fenda para o Vazio se abriu no reino. Três **guardiões** guardam os **Sigilos**
que abrem o caminho até a Cidadela, onde o vilão (gerado a cada partida) espera.

- O **nível dos inimigos depende da região**, não do seu. Quanto mais longe da vila
  inicial, mais perigoso (o mapa mostra o "Nv." de cada lugar). Os guardiões têm nível
  fixo e o chefe final é nível 11 ou mais. Correr direto para os chefes não funciona:
  é preciso evoluir, equipar-se, aprender fraquezas e recrutar aliados.
- A **corrupção** cresce todo dia. Derrotar um guardião faz ela recuar 20 pontos.
  Se chegar a 100%, o reino está perdido. Ela também deixa os inimigos mais fortes.
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
- **Cura lenta:** acampar recupera pouca vida (menos ainda na chuva); a taverna, mais.
  Poções são caras. A mana do mago **não** volta sozinha depois das lutas: só aos poucos
  ou descansando.
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
Mago      (Mana)  ──┬── Piromante    fogo em área, queimaduras fortes, combustão
                    └── Necromante   drenar vida, erguer servos esqueletos, maldições
```

Cada classe tem uma mecânica própria:
- **Guerreiro:** o vigor regenera rápido; erguer o escudo reduz o dano pela metade.
- **Arqueiro:** usa **flechas** (que acabam). Dá para recolher flechas depois da luta,
  fabricá-las em eventos ou comprá-las. É ótimo contra voadores.
- **Mago:** a mana é escassa: regenera pouco durante a luta, recupera só 20% depois dela e
  enche de verdade apenas descansando. O Dardo Arcano é de graça; cada Inferno é uma
  decisão.

Novas habilidades chegam nos níveis 2, 3, 4 e 7 (a habilidade suprema da especialização).

## O que deixa as jornadas diferentes

- **Mundo procedural:** mapa em grafo com vilas, regiões selvagens, covis e a Cidadela.
  Nomes de lugares, NPCs, guardiões e do vilão são gerados a cada partida.
- **88 eventos** com pesos dinâmicos. O que pode acontecer depende de classe,
  especialização, bioma, clima, período do dia, reputação, corrupção e das suas escolhas
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
  (voador, blindado, etéreo, morto-vivo...) e **fraquezas**. Use *Analisar inimigos*.
- **Clima e período do dia:** chuva enfraquece o fogo, a névoa ajuda a esquivar, a
  tempestade atrapalha disparos e à noite os monstros ficam mais fortes.
- **Contratos** no mural das vilas: caçadas, alvos com recompensa e entregas (com
  imprevistos no caminho). Dá para abandoná-los pelo Diário, perdendo reputação.

## Estrutura do código

```
rpg/
  jogo.py        estado, ciclo principal, vilas, loja, contratos, salvar/carregar
  comitiva.py    companheiros: valores, aprovação, reações, combate, conversas, partida e morte
  web/           interface principal: servidor local (só biblioteca padrão) + página
    ponte.py     WebUI: cada chamada da UI vira uma mensagem JSON (cenas, texto, dados, escolhas)
    estado.py    fotografia do jogo em JSON (herói, mapa, combate) para os painéis
    servidor.py  HTTP + SSE em 127.0.0.1, com token por sessão
    static/      index.html, estilo.css, app.js (fila, HUD, texto), batalha.js (palco da luta,
                 balões e selos), telas.js (talentos, fichas, celebrações), sprites.js (pixel art),
                 vista.js (paisagem), mapa.js, som.js, fontes OFL
  tui.py         interface de terminal com painéis (Textual), via --terminal
  ui.py          interface clássica (cores ANSI, menus) e o "jogador robô" dos testes
  mapa.py        desenho do mapa em caracteres
  talentos.py    árvores de talentos
  legado.py      registro de heróis anteriores
  sobrevivencia.py  fome, ferimentos, infecção e escuridão
  telemetria.py  registro da partida e resumo para análise de equilíbrio
  combate.py     combate por turnos, efeitos, traços e fraquezas
  classes.py     classes, especializações, habilidades e companheiros
  inimigos.py    geração de inimigos, guardiões, chefe final e habilidades inimigas
  mundo.py       geração espacial do mundo e nível de cada região
  itens.py       consumíveis e equipamentos procedurais
  dados.py       biomas, criaturas, afixos, clima e guardiões
  texto.py       nomes procedurais e utilidades de texto
  eventos/
    motor.py     registro e sorteio de eventos (condições, pesos, anti-repetição)
    comuns.py    encontros, estranhos na estrada, consequências
    biomas.py    eventos de floresta, pântano, montanha, planície, ruínas e clima
    classe.py    eventos de classe e especialização, e as encruzilhadas
    noite.py     eventos do acampamento
    vila.py      eventos de vila e gerador de rumores
    comitiva.py  recrutamento, conversas, missões pessoais e discussões da comitiva
```

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
