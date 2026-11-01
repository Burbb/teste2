# Protótipo tático da etapa 8: o combate numa grade

Jogável e isolado (31/10/2026, versão **Tático 1**). **Não é integração:** o jogo não carrega nada desta pasta (um teste
confere) e o combate do jogo não mudou. Os números partem do X1 e são de teste. O estudo de viabilidade, as regras
provisórias, a fuga repetida, a comparação com os cards e o trabalho necessário estão no
[29](../../../roadmapIDEIAS/29-ETAPA8-COMBATE-TATICO.md). **A direção espacial está em avaliação.**

## Abrir

Dê dois cliques em `demo.bat` (ou rode `python ferramentas/prototipos/etapa8-tatico/servidor.py` na raiz). O servidor
tenta a porta 8799; se ela estiver ocupada, diz quem está nela e usa a próxima livre, e **abre o navegador na porta que
de fato usou**. A versão aparece no terminal, no título da aba e no topo da página: se não aparecer "Tático 1", não é
esta entrega. `DEMO_PORTA` escolhe outra porta; `DEMO_SEM_NAVEGADOR=1` não abre o navegador.

Teclado: `P` Preparar, `L` Luta, `G` Registro; em Preparar, `Enter` luta. Na luta: clique numa casa verde para andar;
escolha a ação (ou o número) e clique no alvo (`Enter` confirma o alvo sob o mouse); `Esc` ou o botão direito cancela;
`E` encerra a vez; `R` repete no fim.

## O que tem

- **Arena 9 × 7** vista de cima, com rocha (bloqueia passagem e visão) e água (bloqueia passagem, deixa ver).
- **Uma ação e PM por vez**; por padrão, agir encerra o movimento (interruptor "Andar depois de agir" em Preparar).
  **Zona de controle** (+1 PM para sair de perto de um inimigo), também com interruptor.
- **Berserker** (Golpe Pesado, Investida, Golpe de Escudo, Corrente, Redemoinho, Guarda-costas) e **Piromante** (Bola
  de Fogo, Chuva de Brasas, Muralha de Fogo, Combustão, Explosão de Calor, Sentinela de Gelo), com Morel (flanquear,
  proteger lado a lado) e Odette (luz à distância, cura e Bênção com visão).
- **Talentos em pares** (um de cada, ou nenhum), escolhidos por mudar o uso do espaço.
- **Quatro encontros** com os inimigos do X1: campo aberto (três lobos), a passagem (mercenário e dois bandidos),
  perto e longe (bruxa, bandido e sapo), o troll. Cada um diz o objetivo e tem equivalente no X1.
- **Na grade:** casas alcançáveis em verde com o custo; o caminho sob o mouse; ao escolher uma ação, o alcance em azul,
  os alvos com contorno, as casas sem visão hachuradas, e, sob o mouse, a área em vermelho, os aliados atingidos em
  amarelo e o dano previsto em cada um; chamas no chão com as rodadas que faltam; casas marcadas por golpe preparado.
- **Repetir** com a mesma semente; **Registro** de cada luta (comandos, casas andadas, PM, tempo decidindo andar e
  agir, colisões, áreas em aliados, inimigos sem ação) na tela e em JSON, com cada comando.

## Arquivos

| Arquivo | O que é |
|---|---|
| `motor/grade.py` | A geometria: distância, linha de visão, caminhos com zona de controle, áreas |
| `motor/conteudo.py` | Regras numéricas, habilidades, talentos, inimigos, encontros |
| `motor/combate.py` | A luta: a vez, movimento, ações, empurrões, chamas, invocação, a IA dos inimigos, o registro |
| `servidor.py`, `tela/` | O servidor local (versão, porta livre) e a tela provisória |
| `testes/test_tatico.py` | Geometria, limites da vez, deslocamentos, ocupação, prévia igual ao efeito, chão, preparos, IA, fuga |
| `ferramentas/simular.py` | Jogadores automáticos "luta" e "recuo" nas três variantes de regra |
| `ferramentas/fotografar.mjs` | Capturas nas duas janelas de referência; confere que a grade cabe |
| `capturas/` | Preparar, movimento, alcance e visão, área que pega aliado, meio e fim da luta, nas duas janelas |

```
python -m unittest discover -s ferramentas/prototipos/etapa8-tatico/testes -t ferramentas/prototipos/etapa8-tatico
python ferramentas/prototipos/etapa8-tatico/ferramentas/simular.py 12
```
