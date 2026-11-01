# Protótipo de campo livre da etapa 8: o herói em tempo real no meio de tropas pequenas

Jogável e isolado (01/11/2026, versão **Campo Livre 5**; a quarta, com o básico antigo (Corte e Faísca), fica
congelada em `tela-v4/` e abre em `/v4/`; a primeira, **Campo Livre 1**, aprovada pelo Jean como direção, em `tela-v1/`
e `/v1/`; os links estão na tela de escolha; a segunda está no commit `31ea8778` e a terceira no `298dc4bc`). **Não é integração:** o jogo não carrega nada desta pasta (um teste confere) e o combate do jogo não mudou. Os números são de teste. A pesquisa, as decisões, as medições, as
limitações e o que esta direção mudaria no jogo estão no [30](../../../roadmapIDEIAS/30-ETAPA8-CAMPO-LIVRE.md). Os
protótipos anteriores (`etapa8-builds`, `etapa8-tatico`) ficam como histórico.

## Abrir

Dê dois cliques em `demo.bat` (ou rode `python ferramentas/prototipos/etapa8-campo/servidor.py` na raiz). O servidor
tenta a porta **8801**; se ela estiver ocupada, diz quem está nela e usa a próxima livre, e **abre o navegador na porta
que de fato usou**. A versão aparece no terminal, no título da aba, no topo da escolha do herói e no selo da luta: se
não aparecer "Campo Livre 5", não é esta entrega. Um `demo.bat` antigo ainda aberto segura a 8801 (e responde com o
nome antigo em `/api/versao`, embora sirva os arquivos novos): feche a janela dele ou use a porta que o novo anunciar.
`DEMO_PORTA` escolhe outra porta; `DEMO_SEM_NAVEGADOR=1` não abre o navegador.

## Controles

| Tecla | O quê |
|---|---|
| `W` `A` `S` `D` (ou as setas) | andar |
| mouse | mirar (golpes e magias saem na direção ou no ponto do mouse) |
| botão esquerdo (segurar repete a cada 1 s) | ataque principal, fixo: Varredura (Guerreiro; vira para o inimigo mais perto da mira e avança até 32 px para alcançá-lo), Bola de Fogo (Mago) |
| `Espaço` | mobilidade, fixa: Investida (Guerreiro), Piscar (Mago) |
| botão direito, `Q`, `E` | as três habilidades comuns escolhidas na montagem (custam recurso e têm recarga própria) |
| `F` | a ultimate escolhida (sem custo; recarga de 30 s, pronta aos 8 s de luta) |
| `1` `2` `3` | ordens: Acompanhar, Atacar, Defender (no ponto do mouse); valem para a **seleção** e, sem seleção, para todos; funcionam pausado. No modo de comando, `2` com o mouse num inimigo: **atacar este alvo** |
| `Shift` segurado | **modo de comando**: o botão esquerdo arrastado seleciona tropas (não ataca); um clique numa tropa seleciona só ela, no vazio limpa; o botão direito **num inimigo manda atacar esse alvo** (mira vermelha nele; derrubado, voltam à ordem de antes) e **no chão manda defender ali**. Pausado, o mouse já está nesse modo. No comando, o mouse não mexe a câmera, a câmera fica parada durante o arrasto e o tremor se acalma; ao soltar, tudo volta suave |
| `F1` `F2` `F4` | seleciona os soldados, os arqueiros, todas as tropas (`F3` fica indisponível: não há terceiro tipo); com `Ctrl`, soma |
| `X` | limpa a seleção |
| `P` ou `Esc` | pausa (com as opções) |
| `R` | recomeça a mesma batalha |
| `Tab` | registro e diagnóstico (recolhidos por padrão) |
| `M` | som |
| `H` | **traz uma horda** de inimigos comuns na direção do mouse (a quantidade nas opções; até 1200 combatentes no campo) |

Na escolha: o **encontro** (A primeira batalha, Grupos espalhados, Duas frentes, O Capitão e a retaguarda, A horda), o herói
(`1` Guerreiro, `2` Mago), a **montagem** de cada um (três comuns, uma ultimate e talentos até 7 pontos; os atalhos
"Montagens prontas" preenchem tudo e continuam editáveis; a tela rola quando a lista passa da altura da janela) e o
**exército** (1×, 2× ou 4×, experimental; as quantidades reais aparecem logo abaixo); `Enter` luta. Opções (na escolha e na pausa): tremor da
câmera (0 a 150%, começa em 150%; 0 desliga), pausa no impacto, mostrar a área do botão direito, volume, o tamanho da
horda da tecla H e mudo.

## O que entrou no Campo Livre 5

- **O kit montado antes da luta:** cada herói tem um ataque principal e uma mobilidade fixos e quatro espaços
  equipáveis, três habilidades comuns e uma ultimate. O Guerreiro escolhe entre sete comuns (Salto Esmagador,
  Turbilhão, Golpe Sísmico, Corte Sangrento, Ruptura, Grito de Guerra, Avanço de Escudo) e duas ultimates (Fúria
  Desenfreada, Terremoto); o Mago, entre sete comuns (Lança de Gelo, Corrente de Raios, Muralha de Fogo, Anel de Fogo,
  Campo de Gelo, Vórtice, Ignição) e duas ultimates (Chuva de Meteoros, Nevasca). As regras de cada uma estão na tela
  de escolha, com os números do kit montado (`textos.js`).
- **O recurso** limita o uso concentrado, não o fluxo: começa cheio e regenera rápido (Fúria 16 por segundo, Mana 22);
  o principal e a mobilidade não custam nada; as comuns custam de 16 a 35.
- **Talentos** num orçamento de 7 pontos por herói, redistribuídos à vontade: transformações (Lança Estilhaçante,
  Arrasto, Tremor Residual), regras compartilhadas por **marca** (Frio Cortante vale para o dano direto de gelo;
  Hemorragia), interações entre habilidades (Estilhaçar, Brasa Viva, Explosão de Sangue, Sede de Sangue) e ajustes. Um
  talento que pede uma habilidade fora da montagem não pode ser escolhido.
- **Tipos de dano** (direto, contínuo, secundário) e **cadeias** com limite de regra: 2 estilhaços em sequência, 3
  explosões de Sangue ou de Brasa, 30 explosões por golpe.
- **Montagens prontas:** "Sangria" e "Impacto" (Guerreiro), "Gelo que estilhaça" e "Fogo em cadeia" (Mago).
- **A aproximação inimiga:** soldados e veteranos avançam até 10 px na preparação do golpe (o campeão 14, o Capitão 22),
  na direção marcada no começo: acertam quem fica parado e erram quem sai. O Capitão ficou com 900 de vida e 24 de
  dano no herói.
- **A vida que acabou de sair** fica um instante como um rastro claro na barra do herói.
- Medido e conferido na rodada 5 do [30](../../../roadmapIDEIAS/30-ETAPA8-CAMPO-LIVRE.md).

## O que entrou no Campo Livre 4

- **O básico assistido:** vai no inimigo mais perto da mira; a Faísca o persegue (se ele cai, segue reta, sem trocar de
  alvo) e deixa uma **Fagulha** (+6 no próximo golpe de habilidade nele); o Corte dá um passo curto (até 12 px, nunca
  para trás nem através de quem está no meio) e ficou um combo de 3, 4 e 9.
- **O impacto:** tranco visual em heróis e ameaças em todo acerto, sem parar ninguém; a ameaça interrompida fica firme
  2,5 s; o golpe no herói mostra de onde veio (marca no anel), quanto tirou (número vermelho) e, se pesou, a borda da
  tela daquele lado.
- **O Capitão perigoso:** mais rápido (54), machado de 30 a cada 1,6 s, o **Rodopio** quando o cercam, a Arremetida
  também no meio das tropas, o golpe de sequência depois dela; duela com o herói perto e, longe, vai nas tropas (os
  arqueiros primeiro).
- **Arqueiros e ordens:** os arqueiros avançam até a distância de tiro (a retaguarda sai até 90 px do posto); as três
  ordens ficaram distintas (âncora e coleira), uma ordem longe vai sem parar para lutar, as tropas saem das áreas
  anunciadas, e o novo **atacar um alvo**.
- **A horda:** a tecla H e o encontro "A horda" (ondas de 60 × a escala a cada 9 s).
- Tudo medido e conferido na rodada 4 do [30](../../../roadmapIDEIAS/30-ETAPA8-CAMPO-LIVRE.md).

## O que entrou no Campo Livre 3

- **A câmera no modo de comando** fica estável (acima, no Shift); medido na R3.1 do 30.
- **Harg, o Capitão, enfrenta o herói:** foco estável nele (por perto, ou quando o herói o fere ou derruba a tropa dele),
  a **Arremetida** (círculo vermelho marcado no caminho do herói, salto 0,75 s depois; dá para sair; ao cair, fica com o
  machado cravado levando +50%), a **Carga** na direção do herói, o machado que atravessa a tropa no caminho, os
  soldados dele abrindo caminho, imune a cambalear com golpe fraco; vida 480.
- **Escalas 1×, 2× e 4×:** os comuns se repetem em alas ao longo da frente (os especiais não se multiplicam); em 4×, as
  alas de fora começam defendendo o próprio lugar.
- **Quatro habilidades novas:** Avanço de Escudo (Espaço) e Turbilhão (Q) no Guerreiro; Corrente de Raios (botão
  direito) e Campo de Gelo (Q) no Mago. As regras estão na tela de escolha e na R3.4 do 30.

## O que entrou no Campo Livre 2

- **Números de dano do herói** no alvo atingido, no impacto (branco no básico, amarelo no golpe forte, laranja e maior
  com "!" no crítico, que é novo: 10% de chance de 1,5×); o dano contínuo soma por alvo.
- **Harg, o Capitão** (no encontro dele): machado anunciado; a **Carga** (reúne soldados, marca a faixa no chão, corre
  atropelando; um golpe forte na reunião a desfaz; depois fica ofegante e leva +50%); a **Presença** (a tropa perto ataca
  mais rápido e não se abala). Derrubado, a tropa a até 150 px foge e o resto se abala; enquanto vive, ninguém foge.
- **Seleção por tipo e por arrasto**, ordens por grupo, a seleção marcada no pé e contada no placar.
- **Leitura:** sombra tingida pelo lado, vão maior entre as linhas, seta dourada no herói, barras menores, avisos por
  cima da multidão.
- **Três encontros novos** e **quatro versões de habilidade** (Varredura Sangrenta, Grito de Guerra, Bola Incendiária,
  Anel de Fogo); o fim mostra também o que as tropas fizeram além de matar.

## O que tem (desde o Campo Livre 1)

- **Campo aberto de 960 × 560 px nativos**, visto de cima, personagens em três quartos; ampliação inteira (2× em
  1280×720, 3× em 1920×945), pixels nítidos. A câmera segue o herói olhando para onde o mouse aponta.
- **Uma batalha fixa** (mesma semente): 42 aliados (30 soldados, 12 arqueiros) contra 94 inimigos em duas levas. A
  primeira (soldados, veteranos, arqueiros e o **porta-estandarte**, que fortalece quem está na aura) espera em
  formação; a segunda chega pela direita aos 30 s (ou antes, se a primeira cair a 20%) com o **campeão**, que anuncia
  o golpe de machado no chão e é interrompido pelos golpes fortes. Com 20% dos inimigos de pé, o resto foge: vitória.
  O herói cai: derrota.
- **Guerreiro** (Corte com arremate no terceiro, Varredura, Investida, Salto Esmagador com Fúria) e **Mago** (Faísca,
  Bola de Fogo, Piscar, Muralha de Fogo com mana).
- **Impacto:** preparação com a área no chão, contato no quadro certo, clarão no alvo, recuo e atordoamento de quem
  vive, corpos arremessados girando (efeito, não física), quique e poeira, fogo e brasas, marcas no chão, pausa de
  impacto curta (até 100 ms, com intervalo mínimo entre uma e outra), tremor proporcional (com controle).
- **Tropas** que lutam sozinhas, com alvo por vagas (não empilham), arqueiros que mantêm distância, e três ordens.
- **Fim de batalha** com o resumo (derrubados por você e pelas tropas, perdas, maior golpe, cada habilidade).

## Arquivos

| Arquivo | O que é |
|---|---|
| `tela/conteudo.js` | Todos os números: tipos de tropa, heróis e kits, contingentes, limites do impacto, a versão |
| `tela/sim.js` | A simulação (sem DOM, roda no Node): herói, tropas, projéteis, chão, empurrões, separação |
| `tela/efeitos.js` | O que só se vê: corpos arremessados, partículas, cortes, explosões, marcas, tremor, pausa |
| `tela/desenho.js` | O desenho em pixels nativos; as áreas pintadas pela mesma função que decide quem é atingido |
| `tela/sprites.js` | Os combatentes em grade de pixels, à mão (provisórios); `tela/folha.html` mostra a folha |
| `tela/main.js`, `index.html`, `campo.css` | O laço, os comandos, a câmera, a HUD e as telas |
| `tela/textos.js` | O texto de regra de cada habilidade e o custo, a partir dos números do kit montado (a tela não calcula regra) |
| `tela/som.js` | Sons sintetizados na hora (Web Audio), sem arquivos de terceiros |
| `tela/robo.js` | O jogador automático (testes e medição): `?robo=1` (forte) ou `?robo=medio`; vê os avisos do Capitão com 0,15 s ou 0,35 s de atraso |
| `servidor.py`, `demo.bat` | O lançador (porta livre, versão) |
| `testes/sim.test.mjs` | 40 testes da simulação (Node); `testes/test_campo.py` roda-os e confere o isolamento |
| `tela-v1/`, `tela-v4/` | O Campo Livre 1 e o 4 congelados, servidos em `/v1/` e `/v4/` para comparar |
| `ferramentas/simular.mjs` | Batalhas sem tela com o jogador automático, por escala e montagem (duração, abates, custo do passo) |
| `ferramentas/recursos.mjs` | O recurso no uso normal e no concentrado, por montagem: o menor valor e as esperas por recurso |
| `ferramentas/contato.mjs` | Os ataques inimigos no herói do começo ao fim: acertos, erros (o herói saiu) e cancelados |
| `ferramentas/cadeias.mjs` | O custo das cadeias (Estilhaçar, Brasa, Sangue) na horda 4×: o tempo do passo e as explosões |
| `ferramentas/lider.mjs` | O comportamento do Capitão sem tela: onde gasta o tempo, a escolha, as habilidades e o que acertam, o dano |
| `ferramentas/ordens.mjs` | A mesma batalha com estratégias de ordens diferentes: as consequências (perdas, arqueiros vivos, resultado) |
| `ferramentas/conferir3.mjs` | Playwright, Campo Livre 3: a câmera no comando, o custo do 4×, a escolha e um quadro de cada habilidade nova |
| `ferramentas/conferir4.mjs` | Playwright, Campo Livre 4: atacar um alvo com teclado e mouse, o golpe no herói, a horda e o custo dela |
| `ferramentas/medir.mjs` | Playwright, v2: resposta, pausa, seleção e ordens, desempenho, capturas, sequências e vídeos (os vídeos só quando o Jean pedir) |
| `ferramentas/olhar.mjs` | Capturas rápidas de uma batalha em andamento |
| `capturas/` | As da v5 (`cl5-*.png`: a escolha e o modo de comando nas duas janelas); as da v4 (`cl4-*.png`, `conferir4.json`); as da v3 (`cl3-*.png`, `conferir3.json`); as da v2 nas duas janelas, a seleção, as sequências e `medicao.json`; as da v1 em `campo-livre-1/` |
| `videos/` | Os vídeos da v2 e, em `campo-livre-1/`, os da v1. **Vídeos novos só quando o Jean pedir** |

```
node --test ferramentas/prototipos/etapa8-campo/testes/sim.test.mjs
python -m unittest discover -s ferramentas/prototipos/etapa8-campo/testes -t ferramentas/prototipos/etapa8-campo
node ferramentas/prototipos/etapa8-campo/ferramentas/simular.mjs 1 4 forte
node ferramentas/prototipos/etapa8-campo/ferramentas/lider.mjs ambos 1 medio
node ferramentas/prototipos/etapa8-campo/ferramentas/ordens.mjs forte
```

Parâmetros de endereço (para testes e demonstração): `?heroi=mago&qtd=4&enc=horda&montagem=Fogo em cadeia&auto=1&robo=1`
(`qtd`: 1, 2 ou 4; `enc`: original, espalhados, duasFrentes, capitao, horda; `montagem`: o nome de uma montagem pronta;
`hab`: as três comuns e a ultimate, como `hab=lanca,campoGelo,raios,nevasca`; `tal`: os talentos, separados por
vírgula, vazio para nenhum).
