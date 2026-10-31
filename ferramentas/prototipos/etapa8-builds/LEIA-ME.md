# Protótipo X1 da etapa 8: montagem de builds e estrutura dos talentos

Jogável e isolado (31/10/2026). **Não é integração:** o jogo não carrega nada desta pasta (um teste confere), e nenhuma
regra daqui vale no jogo. Os números são de teste. A especificação, as regras provisórias e as perguntas estão na
[seção 15 do 28](../../../roadmapIDEIAS/28-ETAPA8-HABILIDADES-TALENTOS-E-BUILDS.md#15-o-x1-implementado-especificação-corrigida).

## Abrir

Dê dois cliques em `demo.bat` (ou rode `python ferramentas/prototipos/etapa8-builds/servidor.py` na raiz). Abre em
http://127.0.0.1:8797/ (outra porta: `DEMO_PORTA`). O registro vai para uma pasta temporária nova a cada execução
(`DEMO_SAVES` fixa uma); os saves do jogo não são lidos nem tocados.

Teclado: `M` Montar, `L` Luta, `G` Registro; na montagem, `Enter` luta; na luta, o número escolhe a ação e depois o
alvo, `Esc` cancela, `F` sai da Fúria, `R` repete no fim.

## O que tem

- **Duas estruturas de talentos com o mesmo orçamento (7 pontos):** a **híbrida** (regras que valem para famílias de
  habilidades, versões em habilidades centrais e números, em três linhas) e a de **versões e princípios** (uma versão
  por habilidade a 1 ponto, princípios a 3).
- **Duas especializações:** Berserker e Piromante. Oito habilidades cada; o kit leva cinco, mais a ultimate fixa.
- **Exemplos** (Fúria, Quebrador, Pavio, Fornalha, Choque Térmico, e os quatro primeiros também na estrutura de
  versões): carregam kit e talentos; tudo continua editável. "Vazia" limpa.
- **Montagem livre:** cada talento mostra o custo, a linha, o que muda no seu kit ("No seu kit: ...") ou por que não
  faz nada agora; o botão diz por que não dá para pôr ou tirar um ponto. "A build" mostra cada habilidade como os
  talentos a deixam. **Redistribuir** é de graça.
- **Cinco encontros** com inimigos do jogo: três lobos, o mercenário e dois bandidos, a bruxa com o bandido e o sapo,
  o troll sozinho e um grupo sorteado pela semente. Cada um diz quem favorece e desfavorece.
- **Repetir com a mesma semente:** os sorteios dos inimigos (alvo, habilidade) e as chances (atordoar, prender,
  sangrar) vêm de sementes separadas. As mesmas ações dão a mesma luta.
- **Registro:** cada luta (terminada ou abandonada) com a montagem, a semente, o resultado, o dano por fonte, as ações
  usadas e as cadeias mais longas; no JSON, cada decisão com o estado em que foi tomada e todos os eventos. As
  montagens salvas levam uma nota opcional.

## Arquivos

| Arquivo | O que é |
|---|---|
| `motor/conteudo.py` | Habilidades, árvores, exemplos, inimigos, encontros, regras da luta |
| `motor/montagem.py` | Validação (orçamento, linhas, exclusões), o que cada nó muda no kit, as bandeiras de efeito |
| `motor/combate.py` | A luta e a regra das cadeias (identidade dos efeitos) |
| `servidor.py`, `tela/` | O servidor local e a tela (provisória) |
| `testes/test_x1.py` | Montagem, cadeias e interações |
| `ferramentas/simular.py` | Jogador automático simples: confere que nada trava e mede a duração das lutas |
| `ferramentas/fotografar.mjs` | Capturas nas duas janelas de referência (1920×945 e 1280×720); confere também que a doca não anda com o mouse |
| `capturas/` | As capturas da entrega: montagem nas duas estruturas, luta, Fúria contra o troll, registro da luta, fim e registro |

```
python -m unittest discover -s ferramentas/prototipos/etapa8-builds/testes -t ferramentas/prototipos/etapa8-builds
python ferramentas/prototipos/etapa8-builds/ferramentas/simular.py 30
```

## Fora deste protótipo

Intenção geral dos inimigos (X2), travas e chefe abalado (X3), ambientes, Revezamento (recusado pelo Jean) e Esperar
(hipótese futura). Grimório definitivo, ícones e animações esperam o sistema.
