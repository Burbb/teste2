# A vida máxima bloqueada (etapa 1B, protótipo em avaliação)

Pedido do Jean: distinguir na barra da vida do herói a vida de agora, o que uma cura ainda pode encher e a capacidade
que uma penalidade tira da vida máxima. Exemplo dele: 30 de vida, limite 45, saudável 65 dá 30 preenchidos, 15
recuperáveis e 20 bloqueados. **Nada disto entrou no jogo.**

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
