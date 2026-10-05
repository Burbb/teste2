# Crônicas da Fenda

RPG de texto **offline**, em português, feito em **Python puro** (sem dependências).
Cada partida gera um reino diferente: mapa, nomes, chefes, eventos e consequências.

## Como jogar

Precisa apenas do Python 3.8 ou mais novo.

```bash
python jogar.py            # ou: python -m rpg
```

Opções:

| Opção | O que faz |
|---|---|
| `--seed 1234` | Gera sempre o mesmo reino (bom para comparar partidas) |
| `--hardcore` | Morte permanente: cair em combate encerra o jogo |
| `--rapido` | Sem pausas dramáticas no texto |
| `--sem-cor` | Desliga as cores (terminais antigos) |
| `--saves PASTA` | Onde salvar (padrão: `~/.cronicas_da_fenda`) |

Tudo é feito digitando o número da opção e apertando Enter.

## O objetivo

Uma Fenda para o Vazio se abriu no reino. Três **guardiões** guardam os **Sigilos**
que abrem o caminho até a Cidadela, onde o vilão (gerado a cada partida) espera.

A **corrupção** cresce todo dia e cresce mais rápido enquanto houver guardiões vivos.
Derrotar um guardião faz a corrupção recuar. Se ela chegar a 100%, o reino está perdido.

Se você cair em combate, alguém te resgata e você acorda numa vila, mas perde ouro e
dois dias (e a corrupção avança). No modo `--hardcore` não há resgate.

## Classes e especializações

No **nível 4** um evento narrativo da sua classe te obriga a escolher um caminho:

```
Guerreiro (Vigor) ──┬── Paladino     cura, dano sagrado, forte contra mortos-vivos
                    └── Berserker    quanto mais ferido, mais forte; rouba vida; ataques em área
Arqueiro  (Foco)  ──┬── Patrulheiro  companheiro animal (lobo, falcão ou urso), tiro duplo
                    └── Sombra       furtividade, veneno, execuções e críticos devastadores
Mago      (Mana)  ──┬── Piromante    fogo em área, queimaduras fortes, combustão
                    └── Necromante   drenar vida, erguer servos esqueletos, maldições
```

Cada classe tem uma mecânica própria:
- **Guerreiro:** o vigor regenera rápido; erguer o escudo reduz o dano pela metade.
- **Arqueiro:** usa **flechas** (que acabam). Dá para recolher flechas depois da luta,
  fabricá-las em eventos ou comprá-las. É ótimo contra voadores.
- **Mago:** a mana regenera devagar e só volta pela metade depois de cada luta. As magias
  exploram fraquezas elementais.

Novas habilidades chegam nos níveis 2, 3, 4 e 7 (a habilidade suprema da especialização).

## O que deixa as jornadas diferentes

- **Mundo procedural:** mapa em grafo com vilas, regiões selvagens, covis e a Cidadela.
  Nomes de lugares, NPCs, guardiões e do vilão são gerados a cada partida.
- **87 eventos** com pesos dinâmicos. O que pode acontecer depende de classe,
  especialização, bioma, clima, período do dia, reputação, corrupção e das suas escolhas
  anteriores. Eventos vistos recentemente perdem peso, para não repetir.
- **Eventos de classe e especialização:** caçar, fabricar flechas, derrubar um falcão
  mensageiro ou disputar torneios de tiro como arqueiro; duelos de honra e um ferreiro
  itinerante para o guerreiro; anomalias arcanas, grimórios e linhas ley para o mago;
  contratos da Irmandade para a Sombra; cemitérios para o Necromante...
- **Consequências que voltam:** quem você ajuda (ou rouba) pode reaparecer dias depois:
  um viajante grato com um presente, um bandido poupado que vira aliado (ou traidor), um
  ladrão que fugiu com seu ouro, a família da criança perdida...
- **Aliados na batalha final:** muitas boas ações recrutam ajuda para o confronto final.
- **Nêmesis:** se você fugir de uma criatura de elite, ela volta mais forte para te caçar.
- **Rumores:** nas tavernas você ouve sobre tesouros, feras lendárias, mercadores raros e
  pontos fracos dos guardiões (+25% de dano). Alguns rumores são falsos.
- **Inimigos com afixos** (feroz, ancião, corrompido, flamejante...), **traços**
  (voador, blindado, etéreo, morto-vivo...) e **fraquezas**. Use *Analisar inimigos*.
- **Clima e período do dia:** chuva enfraquece o fogo, a névoa ajuda a esquivar, a
  tempestade atrapalha disparos e à noite os monstros ficam mais fortes.
- **Contratos** no mural das vilas: caçadas, alvos com recompensa e entregas (com
  imprevistos no caminho).

## Estrutura do código

```
rpg/
  jogo.py        estado, ciclo principal, vilas, loja, contratos, salvar/carregar
  combate.py     combate por turnos, efeitos, traços e fraquezas
  classes.py     classes, especializações, habilidades e companheiros
  inimigos.py    geração de inimigos, guardiões, chefe final e habilidades inimigas
  mundo.py       geração do mapa
  itens.py       consumíveis e equipamentos procedurais
  dados.py       biomas, criaturas, afixos, clima e guardiões
  texto.py       nomes procedurais e utilidades de texto
  ui.py          terminal (cores, menus) e o "jogador robô" dos testes
  eventos/
    motor.py     registro e sorteio de eventos (condições, pesos, anti-repetição)
    comuns.py    encontros, estranhos na estrada, consequências
    biomas.py    eventos de floresta, pântano, montanha, planície, ruínas e clima
    classe.py    eventos de classe e especialização, e as encruzilhadas
    noite.py     eventos do acampamento
    vila.py      eventos de vila e gerador de rumores
```

### Criando um evento novo

```python
from .motor import evento

@evento(contextos=("explorar", "viagem"), peso=6, cooldown=10,
        cond=lambda g: g.j.classe == "arqueiro" and g.clima == "nevoa")
def vulto_na_nevoa(g):
    g.dizer("Um vulto se move na névoa...")
    op = g.menu("O que faz?", [("Atirar", "atirar"), ("Esperar", "esperar")])
    if op == "atirar" and g.teste("percepcao", 13):
        g.ganhar_xp(15)
    else:
        g.combate(g.grupo())
```

Ferramentas úteis dentro de um evento: `g.menu`, `g.teste`, `g.combate`, `g.grupo`,
`g.inimigo`, `g.ganhar_ouro`, `g.ganhar_xp`, `g.dar`, `g.oferecer_equip`,
`g.mudar_reputacao`, `g.plantar`/`g.colher` (consequências futuras) e `g.aliado_final`.

## Testes

```bash
python -m unittest discover tests
```

Um "jogador robô" joga dezenas de partidas com escolhas aleatórias e força cada evento
em todas as classes e especializações, para garantir que nada quebre.
