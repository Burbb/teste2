# O Esgotado do mercado (22/10/2026, proposta; nada no jogo)

**Pedido de Jean:** o ícone de Esgotado ainda é o antigo desenho do Firme. Levantar o que ele é e onde aparece, sem
presumir que seja um dos 17 estados, e preparar duas propostas de papel próprio, sem trocar o sprite compartilhado.

## O levantamento

- **O que é nas regras:** não é estado de combate. É o motivo de um **suprimento do mercado sem estoque no dia**
  (`rpg/sistemas/loja.py`, `dados_loja`: `motivo = "Esgotado"` quando o estoque daquele suprimento chega a zero, com o
  detalhe "O mercador reabastece amanhã cedo."). O estoque é sorteado por dia e por vila (`estoque_suprimentos`);
  comprar tudo zera; no dia seguinte volta.
- **Onde aparece e em que tamanho:** no cartão do suprimento, na linha do motivo (`telas/mercado.js`, `motivoHtml`),
  com o ícone a **16×16** (o sprite em escala 1, `.merc-motivo img.sprite`) ao lado do texto de 13 px; o cartão fica
  apagado (`.caro`) e o "Estoque: 0" em vermelho. O detalhe de quando volta fica na dica do cartão. O clique no cartão
  esgotado mostra o aviso "Esgotado" (só texto, `App.recusar`), sem ir ao motor.
- **Como o desenho é escolhido:** não há papel próprio. `motivoHtml` desenha sempre `S("cadeado", 1)`, o sprite
  `cadeado` de `sprites-dados.js`, para **todos** os motivos do mercado (Esgotado, "Ouro insuficiente.", a mochila
  cheia, "Você já carrega o máximo de comida.", os motivos dos equipamentos). O mesmo `cadeado` serve também o Salvar da
  doca, o bloqueio de vida (a fome) na linha das condições, o talento trancado (Armadilheiro) e, até a 1.155.0, o Firme
  (que hoje tem a corrente rompida). Por isso o Esgotado parece "o antigo Firme".

## As duas propostas (16×16, como os estados aprovados: contorno de 1 px, luz de cima e da esquerda)

- **A, o caixote vazio** (`esgotado-caixote`; camadas vazio, madeira, contorno): a caixa de tábuas aberta, vista um
  pouco de cima, com a boca funda (a parede do fundo, as paredes dos lados em cunha, o fundo escuro), a frente de duas
  tábuas com os montantes e a travessa. Diz "não sobrou nada na caixa"; madeira clara, longe do baú (vermelho, ferro e
  fechadura).
- **B, o cesto vazio** (`esgotado-cesto`; camadas vazio, palha, contorno): o cesto de palha com a alça em arco, a boca
  aberta e o fundo escuro, o trançado embaixo. A mercadoria de feira, a cesta sem nada.
- **A distinção:** os dois são objetos de mercado em marrom e palha; o Firme é a corrente cinza, o Atordoado as estrelas
  amarelas, o Enfraquecido a espada e a seta roxa. Nenhum dos dois usa o cadeado.
- **A minha leitura (quem escolhe é o Jean):** o caixote lê mais rápido como "vazio" (a boca escura é metade do
  desenho); o cesto é o mais "de feira", mas a alça toma o alto e o vazio fica menor.

## Processo

- As grades à mão em `auxiliares/grades.py` (um caractere por pixel). **O conector do Aseprite estava preso nesta
  sessão** (o bridge de outra sessão segurava a porta 6515; encerrado só aquele processo, pela recuperação documentada,
  o daqui precisa ser religado pelo `/mcp`): as fontes saíram da linha de comando do Aseprite, com
  `ferramentas/arte/aseprite/montar_camadas.lua` (o do `montar_fontes.py`, com o `pintar.lua`; releitura de cada camada, 0 diferentes). O caminho
  foi conferido antes refazendo a fonte do Esqueleto E1r: o PNG saiu idêntico ao aprovado.
- `python auxiliares/grades.py .` e `python auxiliares/exportar.py --montar`: as fontes em `fontes/<id>/<id>-16.aseprite`,
  o 1× pelo Aseprite igual à grade e o @2x exato em `proposta/`.
- `auxiliares/fotografar.mjs`: o mercado a 1920×945 (`OURO=20`, o Antídoto comprado até o fim; o Unguento e a Pena de
  Fênix já sem estoque) com os três Esgotados e os "Ouro insuficiente." ao lado; a proposta trocada **só na página e só
  no ícone dos motivos "Esgotado"**; o cadeado dos outros motivos igual. Sem erro no console (`capturas/registro.json`).
- A folha `esgotado.png` (`python auxiliares/prancha.py`): o atual, o caixote e o cesto no mercado em tamanho real e a
  3×, e os dois a 1× e 8× ao lado do Firme, do Atordoado e do Enfraquecido.

## Alcance, se aprovado

O motor passa a dizer qual motivo é (o Esgotado com um id próprio, sem a tela deduzir pelo texto) e a tela desenha esse
papel pelo `Icones` (um arquivo `esgotado-16.png`, com o @2x); o `cadeado` continua em todos os outros usos.

## A escolha (22/10/2026) e o jogo (1.180.0)

- **A, o caixote vazio, aprovado pelo Jean sem retoque**, só no motivo do suprimento esgotado: o motor manda
  `motivo_id: "esgotado"` (`loja.py`), a tela desenha `Icones.motivo("esgotado")` (o papel `MOTIVO`,
  `motivo-esgotado-16.png` e o @2x, idênticos aos de `proposta/`); "Ouro insuficiente.", a mochila cheia, o teto da
  comida, o Salvar, o bloqueio de vida e o talento trancado continuam no `cadeado`; o Firme continua com a corrente.
- A fonte em `ferramentas/arte/aseprite/motivo-esgotado/` (a cópia da `fontes/esgotado-caixote/`).
- Conferido no mercado com os arquivos de produção (`criaturas/mercenario_lobo_gelido/capturas-1179/mercado.png`): o
  caixote nos três "Esgotado", o cadeado nos oito "Ouro insuficiente.".
- **B, o cesto vazio, fica guardado como alternativa não escolhida.**
