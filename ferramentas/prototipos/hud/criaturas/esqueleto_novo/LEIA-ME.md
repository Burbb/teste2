# O Esqueleto do zero (21/10/2026, proposta; nada no jogo)

**Pedido de Jean:** o C2 também não agradou; refazer do zero o retrato do esqueleto inimigo, combinando com a estética
do jogo, sem relação com as tentativas anteriores (A, B, A2, A2n, S1, S2, C e C2, em `../rainha_esqueleto/`, ficam como
histórico); três variações.

## A linguagem (lida nos retratos aprovados)

A cabeça com um pedaço do ombro ou da roupa enchendo o quadro, sem contorno; a paleta contida; os traços do rosto
pequenos (1 ou 2 px); a luz da esquerda; algo da roupa ou do contexto dizendo quem é (o capuz do Bandido, o manto do
Afogado). O osso aqui é mais apagado que o das tentativas anteriores, para não ser o retrato mais claro da fileira.

## As três

- **E1, o guarda morto** (`esqueleto-e1`; ombros, crânio, elmo, cavidades): o elmo de ferro com o nasal e a ferrugem
  sobre a caveira, as órbitas na sombra da aba, a careta dos dentes, a malha nos ombros. Conversa com o Esqueleto de
  Guarda e as ruínas.
- **E2, o encapuzado** (`esqueleto-e2`; capuz, crânio, cavidades): a caveira na sombra de um capuz de pano roído, na
  língua do Bandido.
- **E3, a caveira nua** (`esqueleto-e3`; ombros, crânio, cavidades): em três quartos para a esquerda (a órbita de perto
  maior, o nariz e a boca deslocados), a mandíbula entreaberta, a coluna e as clavículas.
- **Na bancada:** a primeira E3 era de frente, clara, com as órbitas em faixa (óculos escuros): virou o três quartos e
  o crânio escureceu; os dentes da E1 viraram uma careta simples.

## Processo

- As grades em `auxiliares/grades.py`; as fontes no editor pelo conector (`pintar.lua`; releitura das camadas contra a
  grade, 0 diferentes; o composto com a soma das camadas: 155, 214, 143) em `fontes/<id>/<id>-16.aseprite`; a
  exportação conferida (`auxiliares/exportar.py`: igual à grade, @2x exato, o 32 e o 48 em blocos inteiros com os @2x).
- A folha `esqueleto-novo.png` (`python auxiliares/prancha.py`): as três na carta (32) e no Bestiário (48) em tamanho
  real, a 4× e a 12×; a fileira com os retratos do jogo.

## Alcance, se aprovado (o mesmo das propostas anteriores)

Pela família `esqueleto` (o inimigo, os afixos, os líderes, o Esqueleto de Guarda e os que o Lich invoca); o servo
aliado do Necromante, o Lich e os outros mortos-vivos ficam fora.

## A minha leitura (quem aprova é o Jean)

- **E1:** a mais própria do jogo: o elmo e a malha contam um soldado morto, e separam bem do carniçal e do Lich.
- **E2:** a mais sombria; o risco é ler como um cultista ou a Morte, mais que como um esqueleto comum.
- **E3:** a caveira mais pura e viva (o três quartos); a mais genérica das três.

## A escolha (21/10/2026)

- **E1, o guarda morto: a direção escolhida pelo Jean para o esqueleto básico.** O retoque pedido, só local: a ponta
  direita da aba do elmo sobrava (a aba ia um pixel além do domo à esquerda e dois à direita); o pixel da coluna 14,
  linha 4, saiu e a aba ficou simétrica (`esqueleto-e1r`; a E1 preservada). A caveira, a expressão, o elmo, a malha e a
  paleta iguais. Retocado numa cópia da fonte pelo conector (`pintar.lua`; releitura das quatro camadas, 0 diferentes;
  o composto 154); a exportação igual à grade, 32 e 48 em blocos inteiros. O antes × depois na folha
  `../../acampamento_atacar/rodada2.png`. Continua no protótipo.
- **E2, o encapuzado: guardado como conceito reservado para um possível mago esqueleto**, com a fonte
  (`fontes/esqueleto-e2/`) e os PNGs (`proposta/esqueleto-e2-*`); sem espécie, habilidades nem mapeamento.
- **E3, a caveira nua: alternativa não escolhida.**
