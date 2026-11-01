# Protótipo de campo livre da etapa 8: o herói em tempo real no meio de tropas pequenas

Jogável e isolado (01/11/2026, versão **Campo Livre 3**; a primeira, **Campo Livre 1**, aprovada pelo Jean como
direção, fica congelada em `tela-v1/` e abre em `/v1/`, com o link na tela de escolha; a segunda está no commit
`31ea8778`). **Não é integração:** o jogo não carrega nada desta pasta (um teste confere) e o combate do jogo não mudou. Os números são de teste. A pesquisa, as decisões, as medições, as
limitações e o que esta direção mudaria no jogo estão no [30](../../../roadmapIDEIAS/30-ETAPA8-CAMPO-LIVRE.md). Os
protótipos anteriores (`etapa8-builds`, `etapa8-tatico`) ficam como histórico.

## Abrir

Dê dois cliques em `demo.bat` (ou rode `python ferramentas/prototipos/etapa8-campo/servidor.py` na raiz). O servidor
tenta a porta **8801**; se ela estiver ocupada, diz quem está nela e usa a próxima livre, e **abre o navegador na porta
que de fato usou**. A versão aparece no terminal, no título da aba, no topo da escolha do herói e no selo da luta: se
não aparecer "Campo Livre 3", não é esta entrega. Um `demo.bat` antigo ainda aberto segura a 8801 (e responde com o
nome antigo em `/api/versao`, embora sirva os arquivos novos): feche a janela dele ou use a porta que o novo anunciar.
`DEMO_PORTA` escolhe outra porta; `DEMO_SEM_NAVEGADOR=1` não abre o navegador.

## Controles

| Tecla | O quê |
|---|---|
| `W` `A` `S` `D` (ou as setas) | andar |
| mouse | mirar (golpes e magias saem na direção ou no ponto do mouse) |
| botão esquerdo (segurar repete) | ataque básico: Corte (Guerreiro), Faísca (Mago) |
| botão direito | Varredura (Guerreiro), Bola de Fogo (Mago) |
| `Espaço` | Investida (Guerreiro), Piscar (Mago) |
| `Q` (ou `E`) | Salto Esmagador (Guerreiro, com 100 de Fúria), Muralha de Fogo (Mago) |
| `1` `2` `3` | ordens: Acompanhar, Atacar, Defender (no ponto do mouse); valem para a **seleção** e, sem seleção, para todos; funcionam pausado |
| `Shift` segurado | **modo de comando**: o botão esquerdo arrastado seleciona tropas (não ataca); um clique numa tropa seleciona só ela, no vazio limpa; o botão direito manda a seleção (ou todos) defender ali. Pausado, o mouse já está nesse modo. No comando, o mouse não mexe a câmera, a câmera fica parada durante o arrasto e o tremor se acalma; ao soltar, tudo volta suave |
| `F1` `F2` `F4` | seleciona os soldados, os arqueiros, todas as tropas (`F3` fica indisponível: não há terceiro tipo); com `Ctrl`, soma |
| `X` | limpa a seleção |
| `P` ou `Esc` | pausa (com as opções) |
| `R` | recomeça a mesma batalha |
| `Tab` | registro e diagnóstico (recolhidos por padrão) |
| `M` | som |

Na escolha: o **encontro** (A primeira batalha, Grupos espalhados, Duas frentes, O Capitão e a retaguarda), o herói
(`1` Guerreiro, `2` Mago), a **versão** de cada habilidade (a original continua como opção) e o **exército** (1×, 2× ou
4×, experimental; as quantidades reais aparecem logo abaixo); `Enter` luta. Opções (na escolha e na pausa): tremor da
câmera (0 a 150%, começa em 150%; 0 desliga), pausa no impacto, mostrar a área do botão direito, volume e mudo.

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
| `tela/som.js` | Sons sintetizados na hora (Web Audio), sem arquivos de terceiros |
| `tela/robo.js` | O jogador automático (testes e medição): `?robo=1` (forte) ou `?robo=medio`; vê os avisos do Capitão com 0,15 s ou 0,35 s de atraso |
| `servidor.py`, `demo.bat` | O lançador (porta livre, versão) |
| `testes/sim.test.mjs` | 27 testes da simulação (Node); `testes/test_campo.py` roda-os e confere o isolamento |
| `tela-v1/` | O Campo Livre 1 congelado, servido em `/v1/` para comparar |
| `ferramentas/simular.mjs` | Batalhas sem tela com o jogador automático, por escala e kit (duração, abates, custo do passo) |
| `ferramentas/lider.mjs` | O comportamento do Capitão sem tela: foco, trocas de alvo, distância, habilidades e o que acertam, dano |
| `ferramentas/conferir3.mjs` | Playwright, Campo Livre 3: a câmera no comando, o custo do 4×, a escolha e um quadro de cada habilidade nova |
| `ferramentas/medir.mjs` | Playwright, v2: resposta, pausa, seleção e ordens, desempenho, capturas, sequências e vídeos (os vídeos só quando o Jean pedir) |
| `ferramentas/olhar.mjs` | Capturas rápidas de uma batalha em andamento |
| `capturas/` | As da v3 (`cl3-*.png`, `conferir3.json`); as da v2 nas duas janelas, a seleção, as sequências e `medicao.json`; as da v1 em `campo-livre-1/` |
| `videos/` | Os vídeos da v2 e, em `campo-livre-1/`, os da v1. **Vídeos novos só quando o Jean pedir** |

```
node --test ferramentas/prototipos/etapa8-campo/testes/sim.test.mjs
python -m unittest discover -s ferramentas/prototipos/etapa8-campo/testes -t ferramentas/prototipos/etapa8-campo
node ferramentas/prototipos/etapa8-campo/ferramentas/simular.mjs 1 4 forte
node ferramentas/prototipos/etapa8-campo/ferramentas/lider.mjs ambos 1 medio
```

Parâmetros de endereço (para testes e demonstração): `?heroi=mago&qtd=4&enc=capitao&kit=raios,gelo&auto=1&robo=1`
(`qtd`: 1, 2 ou 4; `kit`: sangrenta, grito, escudo, turbilhao, incendiaria, anel, raios, gelo).
