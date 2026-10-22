# A Harpia e o Grifo (22/10/2026, propostas; nada no jogo)

**Pedido de Jean:** duas propostas por criatura, só no protótipo, na linguagem dos retratos finais, comparadas na carta
e no Bestiário com os mesmos dados, a Harpia e o Grifo junto do Falcão Peregrino aprovado.

## O que o jogo diz e o alcance

- **Harpia** (`harpia`, família): "Metade mulher, metade abutre, inteira cruel. Difíceis de acertar com uma espada.";
  voadora; Grito de Terror e Mordida Sangrenta; nas montanhas, a partir do nível 2, em bando de até três. Não invoca,
  não é invocada, não tem chefe próprio.
- **Grifo** (`grifo`, família): "Rei dos céus das montanhas. Protege o ninho até a morte."; voador e fera; Investida e
  Mordida Sangrenta; nas montanhas, a partir do nível 4, sozinho; é também a mãe do evento do ninho (o ovo dourado; o
  Patrulheiro pode tentar domá-la).
- **Hoje** os dois saem do traço `voador` (o morcego), que também serve o Dragão de Gelo (guardião, fora deste par).
- **Alcance, se aprovado:** pela família (`RETRATO_FAMILIA`, o papel `CRIATURA`): a carta (32), o Bestiário (48), o
  cartaz do mural e o rastreador (contratos de caça e de alvo), a faixa do mestre caçador, os afixos e os de nome
  próprio da família. O Dragão de Gelo e os outros voadores continuam no `voador`.

## As propostas (16×16; o 32 e o 48 são o 16 ×2 e ×3)

- **HA, a que grita** (`harpia-ha`; camadas penas, cabelo, rosto): de frente, o rosto de mulher magro e cinzento, os
  olhos vermelhos, a boca aberta no grito, o cabelo desgrenhado, o pescoço nu e vermelho de abutre dentro da gola de
  penas, as asas castanhas nos ombros.
- **HB, a de perfil** (`harpia-hb`; camadas penas, asa, cabelo, rosto): virada para a esquerda, o nariz em gancho, a
  boca aberta, o pescoço de abutre, a asa erguida atrás dela em penas pontudas.
- **GA, a águia-leão** (`grifo-ga`; camadas pelo, cabeça, bico, olho): em três quartos para a direita (o Falcão olha
  para a esquerda), a cabeça branca e dourada com os tufos, o bico amarelo pesado em gancho, o olho feroz, o peito e o
  ombro de leão.
- **GB, o de asas abertas** (`grifo-gb`; camadas asas, pelo, cabeça, bico, olho): de frente, as asas erguidas atrás da
  cabeça, a cabeça dourada estreita, as sobrancelhas fechadas, o bico longo descendo até o queixo, o pelo de leão.
- **A distinção do Falcão:** o Falcão é pequeno, de perfil para a esquerda, cinza-azulado, de capuz escuro e peito
  creme; os grifos são dourados e marrons, maiores no quadro, com o bico pesado e o leão embaixo.

## A minha leitura (quem escolhe é o Jean)

- **Harpia: prefiro a HA.** Na carta, o grito de frente e a gola de penas dizem "criatura que ataca"; a HB lê bem de
  perfil, mas a asa toma metade do quadro e o rosto fica pequeno a 32. **Limitação no tamanho real:** a HA é uma
  velha cinzenta gritando; o "abutre" depende da gola e do pescoço vermelho, que a 32 são poucos pixels; e ela fica
  perto da Bruxa do pântano na fileira (o tom da pele separa, o verde da Bruxa contra o cinza).
- **Grifo: prefiro o GA.** É o mais legível dos quatro a 32: a cabeça de águia com o bico em gancho é inconfundível e
  se separa do Falcão pela direção, pela cor e pelo peso. O GB tem mais presença (as asas), mas de frente o bico fica
  estreito e, a 32, a cabeça ainda lembra uma coruja. **Limitação no tamanho real do GA:** o "leão" é só o peito
  dourado; quem não conhece o grifo vê uma águia.

## Histórico da bancada (o que não funcionou)

- HA: a primeira tinha a boca larga, que ria em vez de gritar, e a gola clara parecia barba; o pescoço vermelho, logo
  embaixo da boca, lia como língua até o queixo fechar em pele.
- HB: a primeira asa era um bloco reto (uma tábua); virou penas pontudas na borda.
- GB: a primeira, de cara redonda com tufos, era uma coruja; os tufos saíram, a cabeça estreitou e ganhou sobrancelhas e
  o bico longo.

## Processo

- As grades à mão em `auxiliares/grades.py` (um caractere por pixel). **O conector do Aseprite estava indisponível
  nesta sessão** (o `aseprite-bridge` em "Connection closed", sem ferramentas; a porta 6515 livre, nenhum processo a
  encerrar; religar é pelo `/mcp`): as fontes saíram da linha de comando do Aseprite (`python auxiliares/exportar.py
  --montar`, pelo `ferramentas/arte/aseprite/montar_camadas.lua` com o `pintar.lua`; releitura de cada camada, 0
  diferentes), em `fontes/<id>/<id>-16.aseprite`; o composto exportado pelo Aseprite igual à grade, o @2x exato, o 32
  e o 48 em blocos inteiros, em `proposta/`. Sem guias.
- As fotos (`auxiliares/fotografar.mjs`, a 1920×945): a luta (o Arqueiro patrulheiro nível 4 com o Falcão do lado,
  contra a Harpia, o Grifo, o Lobo Gélido, o Troll e o Lobo) e o Bestiário, nos modos atual, A e B, trocados só na
  página pelo nome; sem erro no console (`capturas/registro.json`).
- As folhas `harpia.png` e `grifo.png` (`python auxiliares/prancha.py`).
- **Anotado, sem mexer:** na luta, "Falcão Peregrino rosna ao seu lado." (o verbo do lobo para o falcão).

## Depois da avaliação (23/10/2026)

- **A HA e a HB não foram escolhidas e ficam como histórico** (a HA parecia uma máscara sorridente numa mulher
  fantasiada; a asa da HB, uma peça rígida atrás da cabeça). Três Harpias novas, do zero, em `../rodada_23_10/`.
- **O GA agradou**; a limpeza da ponta do bico (o GA2) está em `../rodada_23_10/`, aguardando a avaliação.
