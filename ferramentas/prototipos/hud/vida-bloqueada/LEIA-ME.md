# A vida máxima bloqueada (etapa 1B: protótipo aprovado, integrado na 1.115.0)

Pedido do Jean: distinguir na barra da vida do herói a vida de agora, o que uma cura ainda pode encher e a capacidade
que uma penalidade tira da vida máxima. Exemplo dele: 30 de vida, limite 45, saudável 65 dá 30 preenchidos, 15
recuperáveis e 20 bloqueados. O protótipo (abaixo) foi aprovado e entrou no jogo na 1.115.0 ("A integração", no fim).

## De onde vêm os números (regras reais, não estimativa da tela)

- **Saudável:** `Jogador.totais()["max_hp"]`, a vida máxima antes das penalidades (base, talentos e equipamento). É o
  mesmo valor que a ficha já usa para mostrar os atributos abaixo do normal (`estado.penalidades_atributos`).
  Acompanha nível, talentos e equipamento.
- **Limite:** `max_hp`, depois de `recalcular` aplicar os fatores.
- **Fontes:** `sobrevivencia.fontes_penalidade(j)["max_hp"]`, na ordem da conta. Os ferimentos que mexem na vida máxima
  são Corte profundo −10%, Mordida dilacerada −10% e Queimadura grave −12%; a Fome tira −10%, −20% ou −35%. Os fatores
  se **multiplicam**. A perda de cada fonte é a diferença que ela faz na ordem em que entra, e a soma fecha com
  saudável − limite. Exemplo do protótipo: 146 → 104, com corte −15, queimadura −15 e fome −12.
- **No protótipo**, `cenario.py` põe isso no estado do herói (`vida_bloqueio`), calculado com essas funções e só
  quando o limite está abaixo do saudável. Integrar seria o mesmo em `rpg/web/estado.py`, ao lado de
  `penalidades_atributos`.

O que as regras fazem com o bloqueio (o protótipo só mostra; conferido com mudanças de verdade):
- **Curandeira** (`curar_ferimento`; o Templo só recupera vida): tira o ferimento e devolve a diferença da vida máxima também como
  vida. O trecho bloqueado volta **cheio**: 91/146 com −15 vira 106/146.
- **O ferimento que sara com descanso:** o máximo sobe e a vida fica. O trecho bloqueado vira **vazio recuperável**.
- **Bandagem:** marca a ferida como tratada (contra infecção), mas a penalidade fica até sarar.
- **Equipamento:** o saudável e o limite sobem juntos. Vestir a peça com +vida máxima levou 146/131 a 171/154, com a
  vida parada em 91 e o bloqueio de −15 para −17 (o mesmo −10% sobre mais vida).

## A proposta

- **A barra mede a vida saudável.** O preenchido é a vida de agora; o vazio de sempre, o que a cura ainda enche; no
  fim, o **trecho bloqueado**, em hachura diagonal cinza fria (a forma distingue, não só a cor). Uma **marca de limite**
  de latão sai um pouco acima e abaixo da barra, onde a cura para.
- **O número** é a vida sobre a saudável (`62/146`, como o Jean sugeriu). No topo, ao lado, uma etiqueta escura com a
  amostra da hachura, o cadeado e o bloqueado (`−42`). Na carta da luta, que é estreita, sem a etiqueta: o número, a
  hachura e a marca bastam.
- **A dica da vida** explica o resto: vida e limite, o limite como teto da cura comum, cada fonte com o percentual e
  os pontos, o saudável e o que devolve cada parte.
- **Sem penalidade,** nada muda: a barra de sempre.
- **O que não muda:** o enchimento e as animações do jogo (o enchimento só é comprimido para a parte útil). Na rodada
  de luta, o número da carta só desceu (62 → 46), sem nenhum "ganho" falso. Parada, a página não reescreve nada.
- **No topo,** as duas linhas (vida e recurso) ganham a mesma coluna de números, e as barras continuam do mesmo
  tamanho.

## Conferido (`fotografar.mjs`, `comparar.py`; 7 cenários em ~26 s, sem erro no console)

| caso | estado do motor | a barra mostra |
|---|---|---|
| sem penalidade | 146 / 146 / 146 | 146 cheio, nada bloqueado; `146/146` |
| no limite (1280 e 1500) | 104 / 104 / 146 | 104 cheio, 0 vazio, 42 bloqueados; `104/146 −42` |
| abaixo do limite | 62 / 104 / 146 | 62 cheio, 42 vazio, 42 bloqueados; `62/146 −42` |
| luta, depois de apanhar | 46 / 104 / 146 | a carta: 46, 59 vazio, 41 bloqueados (±1 do pixel da carta) |
| Curandeira | 91/131/146 → 106/146/146 | o bloqueio some, e a vida devolvida enche |
| vestir a peça | 91/131/146 → 91/154/171 | o saudável e o limite crescem, a vida fica |

Os valores das colunas são vida / limite / saudável. Folhas em tamanho real em `capturas/comparacoes/`: `estados.png`,
`mudancas.png`, `luta.png` e `telas.png` (a dica aberta).

## Pendências e limites

- **Ainda não coberta:** a linha "Em você" do menu de uso de itens (`telas/menus.js`) mostra `hp/max_hp`, e a
  proposta ainda não chega lá.
- **Recurso:** a regra também reduz a vida máxima do Mana, Vigor e Foco (costelas, concussão: −15% do recurso
  máximo). O pedido não cobre o recurso, e nada mudou nele.
- **Companheiros, animal e inimigos:** ficam como estão (sem requisito nem dados).
- **Integrar** pede o campo em `estado.py` e o desenho em `paineis.js` (`barra`) e `batalha.js` (`barra` da carta).
  O protótipo faz isso de fora, observando a página.

## A integração (1.115.0)

O que entrou no jogo, sem nada desta pasta:
- `rpg/sobrevivencia.py`, `vida_bloqueio`: a conta do `cenario.py`, com as frases da dica, levada para o motor.
  `rpg/web/estado.py` põe o resultado em `heroi.vida_bloqueio`.
- `app/paineis.js` (o topo), `batalha.js` (a carta, que troca o limite trazido pelo golpe e pela cura pela vida
  saudável), `telas/menus.js` (a linha "Em você") e `css/02-hud.css` (a hachura, a marca, a etiqueta).

Os dois ajustes pedidos:
- **As barras do topo não mudam de comprimento.** A etiqueta saiu da coluna dos números e foi para a linha das
  condições (a da fome, de altura fixa), como "−42 de vida máxima", com a amostra da hachura, o cadeado e a dica das
  fontes. A medida mostrou que quem encolhia as barras era a gota dos ferimentos, que entra entre os recursos quando
  há ferimento. O lugar dela fica guardado, invisível, sem ferimento. Medido no jogo, as barras de vida e de recurso
  ficam com 242 px em 1280×720 e 302 px em 1500×950: sem penalidade, no limite, abaixo dele, antes e depois da
  Curandeira e da troca de equipamento.
- **"Em você" coerente:** `93/146 · cura até 104`, o mesmo `vida/saudável` do topo e da carta, com o limite da cura
  nomeado. Pelo mesmo motivo:
  - o motivo da poção no limite deixou de ser "Sua vida já está cheia." a 104/146 e passou a dizer o limite e as
    causas ("Sua vida já está no limite de agora (104 de 146): Corte profundo, Queimadura grave e a fome bloqueiam o
    resto.");
  - o efeito do Templo passou de `(104/104)` para `(104/146: o limite de agora)`.

Conferido (`integracao.mjs`, `comparar.py integracao`; 11 cenários em ~35 s, movimento reduzido, sem erro no console;
folhas em `capturas-integracao/comparacoes/`):

| caso | o motor | a tela |
|---|---|---|
| sem penalidade, 1280 e 1500 | 146/146/146 | `146/146`, sem hachura nem etiqueta |
| no limite, 1280 e 1500 | 104/104/146 | 104 cheio, 42 em hachura; `104/146`; etiqueta −42 |
| abaixo do limite | 62/104/146 | 62 cheio, 42 vazio, 42 em hachura; a dica com as três fontes |
| a poção (cura comum) | 93 → 104, limite 104 | para na marca; "Em você" 93/146 · cura até 104 |
| luta, o herói apanha | 62 → 46 | a carta só desce (`62/146 → 46/146`) |
| Curandeira (corte) | 91/131/146 → 106/146/146 | a parte do corte volta cheia; o bloqueio sai |
| vestir a peça | 91/131/146 → 91/154/171 | o saudável e o limite crescem; a vida fica |

Os valores da coluna "o motor" são vida/limite/saudável.

O gabarito mudou só na apresentação (investigado campo a campo antes de atualizar): o estado ganhou `vida_bloqueio`; o
efeito do Templo e o motivo da poção ganharam o limite. Nenhuma partida, lance ou sorteio mudou.

A fumaça rodou duas vezes:
- **Na primeira** (`capturas-integracao/fumaca-1-falha-da-conferencia.log`), uma conferência falhou: ela esperava a
  linha das condições com só "Com fome", e a fome agora também traz ao lado a vida máxima que bloqueia, como
  planejado.
- **O ajuste:** a conferência passou a ler a etiqueta da fome pelo marcador dela e a conferir a do bloqueio ao lado
  (e que as duas somem quando a fome passa).
- **A segunda** (`capturas-integracao/fumaca.log`) rodou com o ajuste.

Pendências:
- as reduções do máximo de Mana, Vigor e Foco, fora desta entrega;
- a comida que tira a fome libera a capacidade sem devolver vida (`recalcular`), o mesmo que o ferimento que sara: não
  há cena de teste direta para isso aqui, e a regra não mudou.
