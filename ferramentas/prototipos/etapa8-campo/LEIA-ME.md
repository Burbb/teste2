# Protótipo de campo livre da etapa 8: o herói em tempo real no meio de tropas pequenas

Jogável e isolado (31/10/2026, versão **Campo Livre 1**). **Não é integração:** o jogo não carrega nada desta pasta (um
teste confere) e o combate do jogo não mudou. Os números são de teste. A pesquisa, as decisões, as medições, as
limitações e o que esta direção mudaria no jogo estão no [30](../../../roadmapIDEIAS/30-ETAPA8-CAMPO-LIVRE.md). Os
protótipos anteriores (`etapa8-builds`, `etapa8-tatico`) ficam como histórico.

## Abrir

Dê dois cliques em `demo.bat` (ou rode `python ferramentas/prototipos/etapa8-campo/servidor.py` na raiz). O servidor
tenta a porta **8801**; se ela estiver ocupada, diz quem está nela e usa a próxima livre, e **abre o navegador na porta
que de fato usou**. A versão aparece no terminal, no título da aba, no topo da escolha do herói e no selo da luta: se
não aparecer "Campo Livre 1", não é esta entrega. `DEMO_PORTA` escolhe outra porta; `DEMO_SEM_NAVEGADOR=1` não abre o
navegador.

## Controles

| Tecla | O quê |
|---|---|
| `W` `A` `S` `D` (ou as setas) | andar |
| mouse | mirar (golpes e magias saem na direção ou no ponto do mouse) |
| botão esquerdo (segurar repete) | ataque básico: Corte (Guerreiro), Faísca (Mago) |
| botão direito | Varredura (Guerreiro), Bola de Fogo (Mago) |
| `Espaço` | Investida (Guerreiro), Piscar (Mago) |
| `Q` (ou `E`) | Salto Esmagador (Guerreiro, com 100 de Fúria), Muralha de Fogo (Mago) |
| `1` `2` `3` | ordens às tropas: Acompanhar, Atacar, Defender (no ponto do mouse); funcionam pausado |
| `P` ou `Esc` | pausa (com as opções) |
| `R` | recomeça a mesma batalha |
| `Tab` | registro e diagnóstico (recolhidos por padrão) |
| `M` | som |

Na escolha do herói: `1` Guerreiro, `2` Mago, `Enter` luta. Opções (na escolha e na pausa): tremor da câmera (0 a
150%, 0 desliga), pausa no impacto, mostrar a área do botão direito, volume e mudo; tropas Normal ou Maior.

## O que tem

- **Campo aberto de 960 × 560 px nativos**, visto de cima, personagens em três quartos; ampliação inteira (2× em
  1280×720, 3× em 1920×945), pixels nítidos. A câmera segue o herói olhando para onde o mouse aponta.
- **Uma batalha fixa** (mesma semente): 42 aliados (30 soldados, 12 arqueiros) contra 94 inimigos em duas levas. A
  primeira (soldados, veteranos, arqueiros e o **porta-estandarte**, que fortalece quem está na aura) espera em
  formação; a segunda chega pela direita aos 30 s (ou antes, se a primeira cair a 20%) com o **campeão**, que anuncia
  o golpe de machado no chão e é interrompido pelos golpes fortes. Com 20% dos inimigos de pé, o resto foge: vitória.
  O herói cai: derrota. **Maior**: o dobro (≈ 270 combatentes).
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
| `tela/robo.js` | O jogador automático (testes, medição, vídeos): `?robo=1` (forte) ou `?robo=medio` |
| `servidor.py`, `demo.bat` | O lançador (porta livre, versão) |
| `testes/sim.test.mjs` | 14 testes da simulação (Node); `testes/test_campo.py` roda-os e confere o isolamento |
| `ferramentas/simular.mjs` | Batalhas sem tela com o jogador automático (duração, abates, custo do passo) |
| `ferramentas/medir.mjs` | Playwright: resposta, pausa, desempenho, capturas, sequências quadro a quadro e vídeos |
| `ferramentas/olhar.mjs` | Capturas rápidas de uma batalha em andamento |
| `capturas/` | As capturas nas duas janelas, as sequências dos golpes e `medicao.json` |
| `videos/` | Os vídeos (Guerreiro, Mago, Guerreiro na batalha maior), 1280×720 |

```
node --test ferramentas/prototipos/etapa8-campo/testes
python -m unittest discover -s ferramentas/prototipos/etapa8-campo/testes -t ferramentas/prototipos/etapa8-campo
node ferramentas/prototipos/etapa8-campo/ferramentas/simular.mjs 3
```

Parâmetros de endereço (para testes e demonstração): `?heroi=mago&qtd=maior&auto=1&robo=1`.
