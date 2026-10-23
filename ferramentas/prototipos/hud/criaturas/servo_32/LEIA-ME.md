# O servo esquelético: o estudo nativo de 32 e a proposta de 16 (23/10/2026, protótipo; nada no jogo)

**Pedido do Jean:** o servo precisa de desenho próprio, não o Esqueleto inimigo com os olhos recoloridos. Sem elmo, capuz
ou armadura: o crânio descoberto, a mandíbula e os dentes legíveis, as vértebras e o começo das clavículas ou costelas
sustentando a cabeça, o osso envelhecido, e um sinal contido da necromancia nos olhos (sem depender só dele). A cabeça
domina o quadro; nada de dentes em xadrez, sorriso de foto, nariz saliente ou órbitas de óculos. Primeiro em 32 nativos,
depois à mão em 16. A SV1, a SV2 e a SV2b (de elmo) ficam em `chefes_e_especiais/`; o Esqueleto E2 continua reservado
para um possível mago esqueleto, sem atribuição nova.

## O que vem do jogo: os dois servos (conferido no código)

- **O servo esquelético** é o "Esqueleto (Invocado)" do Erguer Servo (`habilidades.py`, `_erguer_servo`):
  `cb.invocar_aliado("Esqueleto (Invocado)", ..., tipo="servo")`; a vida e o ataque pelo Poder do Necromante; entra
  provocando.
- **As criaturas que o talento Rei dos Mortos ergue** (`talentos.py`, `_senhor_mortos`): o primeiro inimigo que cai (não
  chefe) volta como `cb.invocar_aliado(f"{c.nome} (servo)", ...)`, por exemplo "Lobo (servo)". O tipo padrão de
  `invocar_aliado` (`combate/luta.py`) também é `"servo"`.
- **Hoje** os dois são `Aliado` com o tipo `"servo"` e caem no mesmo sprite: `batalha.js`, `icone(c)`, devolve `"caveira"`
  para qualquer aliado de tipo servo. O aliado erguido **não guarda a espécie** de que veio (nem a família, nem o retrato).

## A seleção que a integração vai precisar (documentada; nenhuma regra nem mapeamento mudou)

O retrato humanoide novo deve valer **só** para o servo do Erguer Servo; a criatura erguida pelo Rei dos Mortos deve manter
o retrato da espécie dela. Como o tipo é o mesmo, o tipo não serve para escolher. O caminho mais curto, no padrão das
outras exceções (`RETRATO_ORIGEM`):

1. o Erguer Servo marcar a origem do invocado (por exemplo, um papel próprio, `servo_esqueletico`), que a ficha da carta
   repassa ao retrato;
2. o Rei dos Mortos passar ao invocado o retrato da criatura que caiu (o mesmo `retrato(...)` do inimigo, calculado no
   motor), para a carta aliada desenhar o lobo, o bandido etc.;
3. a tela continuar só desenhando o que vem pronto (o `icone(c)` aliado usaria esse campo antes do `"caveira"`).

**A demonstração, só no protótipo** (`auxiliares/cenario_servos.py`, `auxiliares/fotografar.mjs`): uma luta contra o
Esqueleto inimigo com os dois servos de pé, pelo mesmo `invocar_aliado` do jogo. Nos modos de proposta, a página troca o
retrato do "Esqueleto (Invocado)" pelo desenho novo e o do "Lobo (servo)" pelo retrato do lobo do jogo, mostrando a seleção
futura lado a lado com o estado de hoje (os dois na caveira).

## Como foi feito

- **A referência:** `ferramentas/arte/referencias/icones/Caveira esquelética sombria em pixel art.png` (a caveira nua: a
  anatomia, o osso envelhecido, as vértebras e as clavículas); a referência de elmo (a 7) não determina mais o figurino. A
  guia (`guias/servo-guia-32.png` e `-16.png`, a imagem inteira reduzida por média) fica oculta nas fontes.
- **O estudo nativo de 32** (`servo-n32`), à mão:
  1. **o que não funcionou:** a primeira passada, um crânio enorme sobre uma haste fina, lia como um alienígena num palito
     (o mesmo erro de fantoche da Hidra);
  2. a proporção de caveira adulta: o crânio menos alto, o rosto largo (as maçãs e a mandíbula), as órbitas grandes e
     fundas, de tamanhos diferentes, o nariz como buraco, as vértebras grossas e as clavículas na base;
  3. as órbitas pareciam caixas e a boca, uma faixa embaçada: as órbitas inclinadas para o nariz (o canto de dentro
     coberto pela testa, sem cara de óculos), a mordida fechada numa linha escura com os dentes em grupos irregulares
     (claros, com as juntas escuras), a parte de baixo do rosto uma linha mais curta;
  4. o crânio ainda alto e redondo demais: o desenho subiu duas linhas (o alto sai do quadro) e o espaço de baixo ficou
     para o começo das costelas.
  O violeta: um ponto claro com um escuro em cima, no fundo de cada órbita.
- **A proposta de 16** (`servo-n16`), redesenhada à mão com o 32 como mapa: o crânio cortado no alto, as órbitas com o
  violeta, a cavidade do nariz, a fileira de dentes, a mordida, a mandíbula, uma vértebra e as clavículas. O violeta claro
  de um pixel virou uma lâmpada acesa no 16 (o "olho recolorido" que se queria evitar); ficou o violeta escuro.
- **As fontes, pelo Aseprite em lote** (`python auxiliares/grade.py ..` e `python auxiliares/exportar.py --montar`; o
  conector sem editor, a janela aberta do Jean não foi tocada): 0 diferentes na releitura; reabertas com as camadas guia
  (oculta), ossos, sombras, feitiço e contorno; a exportação igual ao composto, alfa só 0 ou 255, os derivados em blocos
  inteiros que voltam ao original.
- **As fotos** (`capturas/`), a 1920×945, com os mesmos dados nos quatro modos (o jogo, a SV2b, o N32 e o N16), sem erro
  no console. **A folha:** `comparacao.png` (a referência, a guia e o Esqueleto inimigo; a coluna aliada com os dois servos;
  a carta a 2× com o inimigo embaixo; a fileira com os aprovados; o diagnóstico).

## A minha leitura (quem decide é o Jean)

- **Conferência técnica** passou; isso não é aprovação visual.
- **O N32** lê na carta como um crânio nu de servo, com as órbitas fundas e o violeta contido, a mordida fechada, a coluna e
  as clavículas: não se confunde com o Esqueleto inimigo (o elmo, o rosto frontal). As órbitas ainda são um pouco
  quadradas, e o rosto, mais neutro que sinistro.
- **O N16 preservou** o crânio descoberto, as órbitas com o violeta escuro, o nariz, a fileira de dentes com a mordida, a
  vértebra e as clavículas. **Perdeu** as costelas, a inclinação das órbitas e a forma da mandíbula; a boca a 1× vira uma
  faixa clara e escura. O que mais o separa do inimigo no 16 é a ausência do elmo e o osso claro, não o violeta.
- **Na fileira:** o N16 tem o grão dos vizinhos; o N32 destoa, como os outros estudos de 32.
