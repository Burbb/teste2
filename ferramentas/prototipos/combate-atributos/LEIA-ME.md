# Protótipo do combate e dos atributos (25/10/2026)

Uma luta jogável com a direção do [25 — Etapa 4](../../../roadmapIDEIAS/25-ETAPA4-REFORCO-E-ENCANTAMENTO.md),
seções 1 a 8. **Não é integração:** o jogo não carrega nada desta pasta (um teste confere), as regras de produção
não mudaram e os números são de teste, não catálogo nem balanceamento da campanha.

## Abrir e jogar

- Dê dois cliques em `demo.bat` (ou rode `python ferramentas/prototipos/combate-atributos/servidor.py` na raiz). O
  navegador abre em http://127.0.0.1:8781/.
- No topo: **Encontro** (os três encontros e os quatro casos de teste), **Construção** (A, B, C ou a livre),
  **Reiniciar** (`R`). **Comparar** mostra os valores derivados das construções lado a lado e monta a livre; **Fora da
  luta** é a situação de aventura; **Resultados** lista as lutas da sessão.
- Na luta: a carta de ouro é quem age. **Número** escolhe a ação; se ela pede alvo, as cartas válidas ganham um
  número (clique ou tecle). `Esc` volta. Uma ação indisponível diz o motivo no lugar da descrição.
- Os resultados ficam numa pasta temporária nova a cada execução (o caminho aparece em Resultados). Os saves do jogo
  não são lidos nem tocados. A construção livre e a última escolha ficam no navegador.

## O que foi respeitado do 25

| Decisão | No protótipo |
|---|---|
| Protagonista + dois companheiros controlados diretamente | Jean, Odette e Morel; o jogador escolhe a ação de cada um na vez dele |
| Agilidade define a ordem, fixa a luta inteira; sem ação extra | A ordem é calculada uma vez no começo (Agilidade; empate: Percepção, depois aliado antes de inimigo, depois a ordem de entrada) e não muda nem se a Agilidade mudar |
| Turnos individuais intercalados; rodada termina depois de todos, inclusive quem perdeu a vez | A faixa da ordem marca quem já foi, quem age, quem está fora e o fim da rodada |
| Uma ação principal por turno | Uma ação (habilidade, ataque, defesa ou item) e a vez passa |
| Ataque básico útil; defesa até o próximo turno | O ataque básico recupera 10 de recurso; Defender vale até o **início** do próximo turno de quem defendeu |
| Ameaças importantes anunciadas, com chance real de resposta | A preparação é anunciada na vez do inimigo e resolve na vez seguinte dele: todos os aliados agem uma vez no meio. A carta mostra alvo, dano previsto (e se o alvo defender), efeito e quando resolve |
| Sem morte de companheiro; volta por ressurreição cara ou item escasso | Caído = pulado na ordem. Volta só por Reerguer (45–50 de Fé, uma vez por luta) ou pela Pena de Fênix (uma na bolsa, só no teste 2) |
| Volta na posição original, sem recuperar vez perdida | Se a posição dele nesta rodada ainda não passou, age nela; se já passou (pulada), só na próxima |
| Pets e invocações | Só do lado inimigo: entram no fim da ordem e agem a partir da rodada seguinte |
| Os sete atributos com valores derivados | Força, Agilidade, Constituição, Intelecto, Percepção, Vontade e Presença; a Ficha e o Comparar mostram cada valor com a conta |
| Potência pela habilidade, nível e equipamento; atributos modulam | O dano é arma + nível × a habilidade. Nenhum atributo soma dano direto; eles mudam ordem, crítico, ponto fraco, defesa, resistências, custo, ruptura de guarda e comando |
| Companheiro contribui fora da luta sem decidir pelo protagonista | "A laje do ossuário": Morel ajuda a erguer (com barulho), Odette lê a inscrição; tocar a laje continua sendo escolha de Jean |

## Os relógios e os marcos

- **Turno** é a vez de um combatente; **rodada** é a ordem inteira, uma vez cada.
- No **início do turno** de alguém expira o que dura "até o início do próximo turno" dele (Defendendo; Protegido e
  Protegendo, pelo turno de quem protege) e o sangramento pinga 4.
- **Atordoado** e **Aterrorizado**: a próxima vez é perdida (gasta ao começar o turno). Uma preparação do inimigo
  atordoado se desfaz.
- **Abalado** (o terror com Vontade 5+): −25% de dano no próximo turno do portador; acaba no fim desse turno.
- **Escudo de Luz, Marcado, Comandado**: até o **fim da rodada seguinte** à aplicação (ou gastos antes, no golpe).
- **Guarda** (Soldado Morto): enquanto houver, o dano cai pela metade; o golpe comum rompe 1, o Golpe Pesado rompe a
  Força de quem bate.
- O protagonista caído é derrota. Inimigo derrotado antes da vez dele: a preparação não sai.

## Fórmulas provisórias

Escala de 1 a 8; o protagonista distribui **24 pontos**; os companheiros têm atributos próprios. **5 é o limiar** das
regras de sim/não.

| Atributo | O que muda | Conta |
|---|---|---|
| Força | Golpe Pesado rompe Guarda; aguentar golpe que atordoa | rompe = FOR; FOR 5+ não fica atordoado |
| Agilidade | Posição na ordem | só a ordem, uma vez |
| Constituição | Vida; sangramento | vida = classe + 6 × nível + 5 × (CON − 3); CON 5+ sangra 1 vez em vez de 2 |
| Intelecto | Custo das habilidades | −5% por ponto acima de 3, até −25% (sem encarecer abaixo de 3) |
| Percepção | Crítico; ponto fraco | 5% + 4% × (PER − 3), até 25%, dano × 1,5; PER 5+ aproveita ponto fraco (+25%) |
| Vontade | Defender; terror | Defender reduz 40% + 5% × (VON − 3), até 65%; VON 5+ só fica abalado |
| Presença | Grito de Comando | +15% + 5% × (PRE − 3) no próximo golpe do aliado; tira o terror |

Dano de um golpe aliado: (arma + nível) × habilidade → comando → marca → abalado → ponto fraco → crítico → guarda
(metade) → defesa do alvo → − proteção (mínimo 1) → escudo. Os inimigos não têm crítico; a previsão da ameaça usa a
mesma conta.

### As três construções (mesmo nível 3, arma 8, proteção 3, mesmos companheiros)

| | A · Força e Constituição | B · Agilidade e Percepção | C · Vontade e Presença |
|---|---|---|---|
| Atributos | FOR 7 AGI 2 CON 6 INT 2 PER 2 VON 3 PRE 2 | FOR 3 AGI 6 CON 3 INT 2 PER 6 VON 2 PRE 2 | FOR 3 AGI 3 CON 3 INT 3 PER 2 VON 6 PRE 4 |
| Vida | 73 | 58 | 58 |
| Ordem (encontro 1) | 5º | 1º | 5º |
| Crítico / ponto fraco | 1% / não | 17% / sim | 1% / não |
| Defender | 40% | 35% | 55% |
| Terror / atordoar / sangrar | perde a vez / aguenta / 1 vez | perde a vez / atordoado / 2 | abalado / atordoado / 2 |
| Golpe Pesado rompe / Comando | 7 / +10% | 3 / +10% | 3 / +20% |

## O conteúdo

- **Jean** (Guerreiro): Atacar, Golpe Pesado (25), Proteger (15), Grito de Comando (20), Defender.
- **Odette** (curandeira): Bastão, Curar (20 → 18 com INT 5), Escudo de Luz (15 → 14), Reerguer (50 → 45, uma vez),
  Defender.
- **Morel** (mercenário): Golpe, Golpe no Joelho (30: desfaz a preparação e atordoa quem não é firme), Marcar (10),
  Defender.
- Itens: Poção de Vida (1 por encontro); Pena de Fênix (só no teste 2).
- **Encontro 1 · Os lobos da estrada** (tutorial): Lobo Alfa (anuncia o Bote: 20 de dano e sangramento) e Lobo.
- **Encontro 2 · O bruto anunciado**: Bandido Bruto (110 de vida, ponto fraco; anuncia o Golpe Esmagador a cada duas
  rodadas: 34 e atordoa) e dois Besteiros.
- **Encontro 3 · O xamã e o soldado**: Xamã Caído (chama Afogados nas rodadas 1, 4, 7, até 2; anuncia o Grito de
  Terror) e Soldado Morto (Guarda 6, firme, ponto fraco).
- **Testes** (a faixa vermelha diz a condição artificial): 1 · Jean começa atordoado (perde a vez, a rodada fecha);
  2 · Morel caído e Jean com Agilidade 6 e uma Pena (volta antes da posição: age na mesma rodada); 3 · Morel caído e
  Odette com Fé cheia (Reerguer depois da posição: só na próxima); 4 · Lobo Alfa com 8 de vida, Agilidade 1 e o Bote
  já preparado (derrubado antes, o Bote não sai).

## Reproduzir e comparar

- Cada encontro tem semente fixa: as mesmas escolhas dão a mesma luta. Para comparar construções, jogue o mesmo
  encontro com A, B e C (o seletor reinicia) e abra **Resultados**: rodadas, quedas, dano por personagem, preparações
  que saíram e que foram desfeitas, e as ações usadas.
- **Comparar** põe as três construções e a livre lado a lado, com o que difere em destaque e a ordem do encontro 1.
- Medição por um jogador automático (`python` com as regras; não substitui jogar): três estilos em cada encontro.

| Encontro / construção | Sensato | Sem o Golpe no Joelho | Ignorando as ameaças |
|---|---|---|---|
| 1 · A / B / C | vitória em 3 / 3 / 3 | 3 / 3 / 3 | 3 / 3 / 3 |
| 2 · A / B / C | 10 / 8 / derrota na 5 | 10 / 10 / derrota na 5 | 10 com 2 quedas / derrota na 5 / derrota na 5 |
| 3 · A / B / C | 6 / 7 / 6 | 7 / 10 / 7 | 7 / 10 / 7 |

## O que observei jogando

Joguei o encontro 2 com a B à mão até o fim (vitória na rodada 6) e li os registros dos outros:

- **Decisões reais.** O Golpe Esmagador anunciado em Odette (25 de vida, 33 previstos) abriu cinco respostas
  diferentes: Joelho de Morel, Proteger de Jean (ele levaria 31 e ficaria atordoado: FOR 3), Defender de Odette (16),
  Escudo de Luz nela (17 e atordoada), Curar antes. Usei o Escudo numa rodada e o Joelho na outra. O recurso pesa: o
  Golpe Pesado de Jean deixa 5 de Vigor e só o ataque básico nas duas vezes seguintes; gastar cedo ou guardar para
  Proteger é uma escolha.
- **Opção dominante (corrigida).** Na primeira calibragem o Golpe no Joelho a 20 desfazia toda preparação: o jogador
  automático nunca deixou uma sair. A 30, Morel desfaz uma, talvez duas por luta; depois precisa de outra resposta.
  Ainda é a resposta mais limpa contra o Bruto; vale observar se continua a primeira escolha sempre.
- **As construções mudam o jogo.** A aguenta o Esmagador (FOR 7) e rompe a guarda do Soldado de uma vez; B age
  primeiro, pega o ponto fraco do Bruto e critica, mas cai atordoada e sangra o dobro; C defende 55%, só fica abalada
  no grito e comanda melhor. C sofreu no encontro 2 com o jogador automático (derrota): sem Força e sem iniciativa, ela
  depende de Defender e Comandar na hora certa, o que a heurística não faz.
- **Repetição e espera.** O Soldado Morto com a guarda que só caía com o Golpe Pesado virou 4 rodadas de 2–4 de dano;
  agora o golpe comum também rompe 1. Ainda há rodadas de ataque básico quando o Vigor zera: é o lugar para observar se
  arrasta.
- **Informação.** A previsão de dano na carta da ameaça bate com o dano real (teste). O que faltava apareceu jogando e
  foi corrigido: nomes iguais (Besteiro 1 e 2), concordância (Odette atordoada), o Abalado que expirava antes de valer.
  Não há dica de "respostas possíveis" na carta: o jogador deduz pelas ações; vale ver se o Jean sente falta.
- **O encontro 3 ficou o mais leve** (sem quedas em nenhum estilo). As prioridades competem (derrubar o xamã antes do
  grito, os afogados, o soldado), mas sem punição forte; é o primeiro número a mexer se a sensação for de folga.

## Limitações

- Números de teste; o jogador automático escolhe por regra fixa, não como uma pessoa, e serve para ordens de
  grandeza.
- Sem animação de ataque nem números flutuando: a vida muda na carta (com o −N ao lado) e o registro mostra a conta de
  cada golpe. Os eventos novos chegam em sequência no registro (sem animação com movimento reduzido).
- Os inimigos escolhem o alvo do golpe comum ao acaso (com semente) e o da preparação pelo mais ferido; não há
  provocação.
- Sem talentos, equipamento trocável, níveis, ultimate, pets aliados ou fuga. A ficha dos companheiros é fixa.
- A situação fora da luta é uma só, sem consequência depois.

## Verificar

```
python -m unittest discover -s ferramentas/prototipos/combate-atributos/testes -t ferramentas/prototipos/combate-atributos
PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/combate-atributos/auxiliares/conferir.mjs
python ferramentas/prototipos/combate-atributos/auxiliares/folha.py
```

Os testes (26) cobrem: a ordem calculada uma vez e os desempates; a invocação no fim e agindo na rodada seguinte; a
vez perdida e o fim da rodada; a defesa, o escudo, a marca e o abalado expirando no marco certo; o inimigo derrotado
antes da preparação; o Joelho; a previsão igual ao dano real; a queda e a volta antes e depois da posição; a mesma
vez enviada duas vezes; reiniciar sem acumular; os derivados iguais ao estado real; o servidor; o jogo sem nada do
protótipo. O roteiro do navegador confere a 1920×945 e a 1280×720 (sem rolagem, sem corte, teclado, tecla segurada,
clique duplo, reinício, movimento reduzido) e grava `capturas/`; a `folha.png` junta as principais.

## Arquivos

- `motor/conteudo.py` (grupo, construções, habilidades, inimigos, encontros, testes, a situação) e `motor/regras.py`
  (as regras e o estado para a tela).
- `servidor.py` (a API e os arquivos; os estáticos do jogo só leitura), `tela/` (index, demo.js, demo.css), `demo.bat`.
- `testes/`, `auxiliares/conferir.mjs`, `auxiliares/folha.py`, `capturas/`, `folha.png`.
