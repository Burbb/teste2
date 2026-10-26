# Protótipo: reforço, materiais e desmontagem

A demonstração jogável da seção 5 do [25](../../../roadmapIDEIAS/25-ETAPA4-REFORCO-E-ENCANTAMENTO.md) (26/10/2026).
**Não é integração.** O jogo de produção não carrega esta pasta (um teste confere); a forja, o mercado e os saves do
jogo não mudaram. Os números são hipóteses desta rodada, não balanceamento.

## Abrir

Dê dois cliques em `demo.bat` (ou `python ferramentas/prototipos/reforco/demo.py` na raiz). O jogo de sempre abre no
navegador num **save temporário** (uma pasta nova a cada vez; os saves pessoais não são lidos nem tocados): o Guerreiro
no nível 4, no Vau, com Morel e Odette, 380 de ouro, dois baús e as peças dos exemplos. Feche a janela do terminal
para parar. Folha compacta: `folha.png`.

Só nesta execução, `demo.py` troca a forja (o balcão novo), o baú (que pode dar fragmento), a seção "Materiais" do
Inventário e a venda da peça reforçada. O resto é o jogo: o Inventário do grupo, o mercado, a luta, a estrada.

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
- Na tela (1920×945 e 1280×720): o duplo clique em "Reforçar" compra um passo só; a confirmação da desmontagem só arma
  depois de um instante e ignora o clique que a abriu; depois de desmontar, nada fica selecionado; a tecla segurada
  não repete; Esc cancela a confirmação.

```bash
python -m unittest discover -s ferramentas/prototipos/reforco/testes -t ferramentas/prototipos/reforco
```

## Roteiro (uns 5 minutos)

1. **Recompensa de teste:** o quadro mostra 8 Fragmentos de Têmpera. "Ir para a vila".
2. **Inventário** (`i`): a seção "Materiais" embaixo da bolsa, com 8; a bolsa continua 6/12.
3. **Forja** (Ferreiro → o ferreiro na oficina): escolha o **Martelo de Ferro** de Jean. Veja os dois caminhos (Fio e
   Runas), o ganho, o custo, quanto o grupo tem e a comparação na luta. **Reforçar · Fio** duas vezes (tente o duplo
   clique: compra um passo só). A ficha à esquerda mostra o Ataque subir.
4. Escolha o **Martelo de Aço** na bolsa: "Se você vestir no lugar do Martelo de Ferro +2" mostra a substituta.
5. Escolha o **Lamento de Gharbad**: a especializada (os especiais na ficha; +2 por passo).
6. No **Inventário**, vista o Martelo de Aço em você e passe o Martelo de Ferro +2 para Morel (o reforço vai junto).
7. Volte à forja e **desmonte** uma peça da bolsa (Desmontar… → a confirmação nomeia a peça e o retorno). Esc ou
   Cancelar desfaz o pedido.
8. **Mercado:** venda uma peça reforçada (o preço inclui 25% do ouro investido). Abra um **baú** (às vezes 1
   fragmento). Tente reforçar sem fragmento suficiente: o botão diz o que falta e não cobra.
