# Protótipo X1 da etapa 8: montagem de builds e estrutura dos talentos

Jogável e isolado (31/10/2026). **Não é integração:** o jogo não carrega nada desta pasta (um teste confere), e nenhuma
regra daqui vale no jogo. Os números são de teste. A especificação, as regras provisórias e as perguntas estão nas
seções [15](../../../roadmapIDEIAS/28-ETAPA8-HABILIDADES-TALENTOS-E-BUILDS.md#15-o-x1-implementado-especificação-corrigida)
(a primeira rodada: cadeias, independência) e
[16](../../../roadmapIDEIAS/28-ETAPA8-HABILIDADES-TALENTOS-E-BUILDS.md#16-o-x1-ampliado-repertório-para-descobrir)
(a segunda: o repertório ampliado, a matriz, os talentos, as limitações) do 28.

## Abrir

Dê dois cliques em `demo.bat` (ou rode `python ferramentas/prototipos/etapa8-builds/servidor.py` na raiz). Abre em
http://127.0.0.1:8797/ (outra porta: `DEMO_PORTA`). O registro vai para uma pasta temporária nova a cada execução
(`DEMO_SAVES` fixa uma); os saves do jogo não são lidos nem tocados. As montagens salvas na tela ficam no navegador
(e também vão para o registro).

Teclado: `M` Montar, `L` Luta, `G` Registro; na montagem, `Enter` luta; na luta, o número escolhe a ação e depois o
alvo, `Esc` cancela, `F` sai da Fúria, `R` repete no fim.

## O que tem

- **Duas especializações, 16 habilidades cada** (14 e duas ultimates): o kit leva cinco e uma ultimate. Berserker
  (7 do Guerreiro, 7 do Berserker) e Piromante (5 do Mago, 9 do Piromante).
- **Um vocabulário compartilhado:** fichas (Guarda, Força, Exposto), camadas nos inimigos (Queimadura, Sangramento,
  Frio; Queimadura e Frio se anulam), invocações (Estandarte, Fogo-fátuo, Sentinela) e a Fúria.
- **Duas estruturas de talentos com o mesmo orçamento (9 pontos, sem ordem de compra):** a **híbrida** (regras que
  valem para todas as habilidades com uma propriedade, versões e números) e a de **versões e princípios** (os mesmos
  efeitos presos a uma habilidade ou juntos em princípios; os mesmos números). Berserker: 21 e 18 talentos; Piromante:
  19 e 16.
- **Exemplos** (nove na híbrida, seis na de versões): atalhos editáveis. "Vazia" limpa.
- **Montagem livre e legível:** filtros por função e por propriedade (a propriedade filtra também os talentos);
  cada talento diz o que afeta no repertório inteiro (em destaque o que está no kit) ou por que não faz nada agora;
  passar o mouse num talento acende as habilidades que ele muda, e numa habilidade, os talentos que a mudam; cada
  habilidade mostra a descrição como os talentos a deixam. **Redistribuir** é de graça. **Salvar, Duplicar, abrir e
  apagar** montagens (na coluna da esquerda).
- **Seis encontros** com inimigos do jogo: três lobos, o mercenário e dois bandidos, a bruxa com o bandido e o sapo,
  o troll sozinho, o cultista com dois esqueletos (que não sangram) e um grupo sorteado pela semente. Cada um diz o
  que favorece e desfavorece.
- **Repetir com a mesma semente:** os sorteios dos inimigos (alvo, habilidade) e as chances (atordoar, prender,
  sangrar) vêm de sementes separadas. As mesmas ações dão a mesma luta.
- **Registro:** cada luta (terminada ou abandonada) com a montagem, a semente, o resultado, o dano por fonte, as ações
  usadas e as cadeias mais longas; no JSON, cada decisão com o estado em que foi tomada e todos os eventos.

## Arquivos

| Arquivo | O que é |
|---|---|
| `motor/conteudo.py` | Habilidades, árvores, exemplos, inimigos, encontros, regras da luta |
| `motor/montagem.py` | Validação (orçamento, exclusões), o alcance de cada nó, a descrição efetiva, as bandeiras de efeito |
| `motor/combate.py` | A luta, as camadas, as invocações e a regra das cadeias (identidade dos efeitos) |
| `servidor.py`, `tela/` | O servidor local e a tela (provisória) |
| `testes/test_x1.py` | Montagem, cadeias e interações |
| `ferramentas/simular.py` | Jogador automático simples: confere que nada trava e mede a duração das lutas |
| `ferramentas/fotografar.mjs` | Capturas nas duas janelas de referência (1920×945 e 1280×720); confere também que a doca não anda com o mouse |
| `capturas/` | As capturas da rodada 2: a montagem nas duas estruturas (com filtro e realce, e em 1280×720), o Invocador com as duas invocações nas duas janelas, a Fúria contra o troll, o fim e o registro |

```
python -m unittest discover -s ferramentas/prototipos/etapa8-builds/testes -t ferramentas/prototipos/etapa8-builds
python ferramentas/prototipos/etapa8-builds/ferramentas/simular.py 30
```

## Fora deste protótipo

Intenção geral dos inimigos (X2), travas e chefe abalado (X3), ambientes, Revezamento (recusado pelo Jean) e Esperar
(hipótese futura). Grimório definitivo, ícones e animações esperam o sistema.
