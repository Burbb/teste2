# Criaturas, primeiro par: o Afogado e a carta da Ilse (proposta, 21/10/2026)

**Pedido de Jean:** começar as criaturas pelo Afogado e pela carta da Ilse (no lugar do Lobo e do Bandido
recomendados no levantamento, `../LEIA-ME.md`). Só no protótipo: nada integrado, regras e dados iguais.

## O que o jogo diz e o formato

- **Afogado** (`afogado`, morto-vivo do Charco, do Salão Alagado e do sarilho da Capela): "os que o pântano não
  devolveu; agarram e puxam para o fundo"; há o Afogado Inchado, o que prepara o golpe no sarilho. Hoje: a caveira
  genérica (a mesma do esqueleto, do carniçal, do cavaleiro sombrio e da Ilse).
- **Ilse** (a guardiã da Capela, `bruxa_afogada` em `missoes.py`): na cena do fundo, a pele azulada, o cabelo de algas
  com uma mecha molhada cobrindo o olho direito, o vestido escuro (`telas/cenas.js`, `ilseDesenho`, a paleta `CORF`).
  Hoje, na carta da luta, a caveira genérica.
- **Formato:** o dos retratos de carta aprovados da comitiva (`retratos.js`, `ODETE_CARTA` e `YARA_CARTA`): 16×16, a
  cabeça e os ombros enchendo o quadro até a base, sem contorno preto (a caixa da carta é escura), poucos planos, a luz
  da esquerda. O jogo mostra a 2× na carta (32 px) e a 3× no Bestiário e no mural (48 px).

## O desenho

- **Afogado** (`afogado`): a cabeça inchada e larga, a pele cinza-esverdeada de quem ficou na água (quatro tons, a luz
  da esquerda), as órbitas fundas e escuras com um ponto pálido, a boca aberta, fios de alga colados no crânio e caindo
  dos lados, a roupa podre nos ombros. Camadas roupa, pele, olhos, algas.
- **Ilse** (`ilse`): a transposição da figura da cena, com a mesma paleta: o rosto azulado e estreito, o olho esquerdo
  claro, a mecha escura sobre o olho direito, o cabelo de algas em mechas separadas descendo pelos dois lados até o
  peito, o vestido escuro. O cabelo sobe um tom em relação à cena (`#3d5a40` e `#2c4130`), para não sumir na caixa
  escura. Camadas vestido, rosto, cabelo.
- **Na bancada:** a primeira Ilse, com o cabelo como uma massa fechada em volta do rosto, lia como um capuz; o rosto
  ficou mais largo, o cabelo fino no alto da cabeça e as mechas dos lados separadas, com o fundo aparecendo entre elas.

## Processo e conferência

- As grades à mão em `auxiliares/grades.py`; as fontes montadas **no editor pelo MCP** (o `pintar.lua`, 0 diferentes na
  releitura) em `fontes/<id>/<id>-16.aseprite`; a exportação pela linha de comando com a conferência
  (`auxiliares/exportar.py`: o 1× igual à grade, @2x exato, alfa 0/255) em `proposta/`. O conector continuou de pé
  depois da exportação em lote.
- Fotos a 1920×945 (`auxiliares/fotografar.mjs`), atual × proposta com os mesmos dados: o Afogado numa luta com um
  esqueleto e uma sanguessuga (o cenário `tutorial` com `GRUPO`) e no Bestiário (o `covil` com `BESTIARIO`); a Ilse na
  luta real do fundo da capela (o cenário `capela`, do ossuário: "Descer ao fundo alagado" e "Lutar para destruí-la").
  Na proposta, só a página troca o retrato das cartas e do Bestiário pelo nome da criatura; o jogo ainda não tem papel
  por espécie. Sem erro nem aviso no console.
- A folha: `afogado-ilse.png` (as cartas em tamanho real e 2×, o Bestiário, a Ilse com a cena dela, as duas cabeças ao
  lado do Morel e da Odette na mesma caixa, e a 12×).

## Avaliação (a minha leitura em tamanho real; quem aprova é o Jean)

- **O Afogado** lê de imediato como um morto da água, separado da caveira do esqueleto que fica ao lado: a cabeça
  larga e verde e a boca aberta. No Bestiário, a 3×, continua firme. O risco é ler como um "zumbi" genérico; a alga e a
  roupa podre puxam para o pântano.
- **A Ilse** é reconhecível como a mulher da cena (o rosto azulado, a mecha, o cabelo de alga, o vestido) e fica
  coerente com ela no mesmo quadro. É a mais frágil das duas: o cabelo e o vestido escuros sobre a caixa escura deixam
  a leitura apoiada só no rosto claro.
- **Para a integração,** quando houver aprovação: dar ao retrato um papel pela espécie e pelo chefe (a carta pede o
  retrato pela família, `afogado`, e pela chave da Ilse), sem mudar os traços nem as regras, como foi o `ESTADO` dos
  estados.
