# Crônicas da Fenda

RPG de texto **offline**, em português, feito em **Python puro** (sem dependências).
Um RPG **hardcore** e sombrio, no espírito de Diablo: aqui você não é o escolhido.
A fome mata, feridas infeccionam, a noite cega e a morte é permanente. Cada partida gera
um reino diferente: mapa, nomes, chefes, eventos e consequências.

![Interface moderna: log, opções, painel do herói e mapa](docs/interface.png)

## Como jogar

Precisa do Python 3.8 ou mais novo. Para a **interface moderna** (painel do herói, mapa
sempre visível, opções clicáveis), instale uma dependência:

```bash
pip install -r requirements.txt   # instala o textual (opcional)
python jogar.py                   # ou: python -m rpg
```

Sem o `textual` (ou com `--classico`) o jogo usa a interface clássica, em Python puro.

| Opção | O que faz |
|---|---|
| `--classico` | Interface de terminal simples, sem dependências |
| `--seed 1234` | Gera sempre o mesmo reino (bom para comparar partidas) |
| `--brando` | Modo brando: ao cair em combate você é resgatado (perde ouro e dois dias) |
| `--rapido` / `--sem-cor` | Sem pausas / sem cores (interface clássica) |
| `--saves PASTA` | Onde salvar (padrão: `~/.cronicas_da_fenda`) |

Na interface moderna, o painel de combate e a faixa de condição (vida, recurso, comida,
tochas, ferimentos) ficam logo acima das opções, sem precisar desviar o olhar. Tecle o
número/letra da opção, use as setas + Enter, ou clique.
`PageUp`/`PageDown` rolam o histórico e `Ctrl+Q` sai.

## O objetivo

Uma Fenda para o Vazio se abriu no reino. Três **guardiões** guardam os **Sigilos**
que abrem o caminho até a Cidadela, onde o vilão (gerado a cada partida) espera.

- O **nível dos inimigos depende da região**, não do seu. Quanto mais longe da vila
  inicial, mais perigoso (o mapa mostra o "Nv." de cada lugar). Os guardiões têm nível
  fixo e o chefe final é nível 11 ou mais. Correr direto para os chefes não funciona:
  é preciso evoluir, equipar-se, aprender fraquezas e recrutar aliados.
- A **corrupção** cresce todo dia. Derrotar um guardião faz ela recuar 20 pontos.
  Se chegar a 100%, o reino está perdido. Ela também deixa os inimigos mais fortes.
- **A morte é permanente.** (No modo `--brando`, alguém te resgata e você acorda numa
  vila, perdendo ouro e dois dias.)

## Sobrevivência

- **Fome:** cada dia consome 1 provisão. Sem comida você fica fraco, não se recupera
  dormindo e, depois de alguns dias, começa a morrer. Compre comida nas vilas, cace ou
  saqueie.
- **Ferimentos:** golpes pesados deixam marcas que duram dias (costelas quebradas,
  braço fraturado, perna torcida, cortes, queimaduras...) e reduzem seus atributos.
  Feridas abertas precisam de bandagem, ou podem **infeccionar**. A infecção causa febre
  e mata se não for tratada com unguento ou por um curandeiro.
- **Escuridão:** à noite, nas ruínas e na Cidadela, você precisa de tochas. Sem luz, você
  fica pior em percepção e destreza e é emboscado com mais facilidade.
- **Cura lenta:** acampar recupera pouca vida (menos ainda na chuva); a taverna, mais.
  Poções são caras. A mana do mago **não** volta sozinha depois das lutas: só aos poucos
  ou descansando.
- **Inimigos perigosos:** bandos de **campeões** (vários inimigos com o mesmo afixo),
  **únicos** nomeados com escolta, caídos com xamãs que **ressuscitam** os irmãos,
  carniçais que **devoram** cadáveres para se curar.

## Saque

Itens têm raridade, como em Diablo:
**comum** · mágico (azul, 1 afixo) · raro (amarelo, 2–3 afixos, nome próprio) ·
**★ lendário** (itens únicos com nome, história e efeitos especiais).
Afixos especiais: roubo de vida, chance de crítico, espinhos, vida por turno e vida por abate.

## Mapa

O reino é gerado no espaço: regiões de bioma contínuas e estradas que não se cruzam.
O mapa mostra o que você já descobriu (o resto fica na névoa):

```
   ⌂1─────────@5───          @ você   ⌂ vila   ♣ floresta   ≈ pântano
              ╲  ╲──Π4        ▲ montanha   ∴ planície   Π ruínas
               ╲              ☠ covil   ✓ covil vencido   ♜ cidadela
                ∴7─────☠9
```

Os números do mapa são os mesmos do menu de viagem, que avisa quando um destino é
perigoso demais para o seu nível.

## Árvore de talentos

Cada classe tem uma árvore em 3 colunas: o **tronco comum** no meio e, nas laterais,
talentos que **só funcionam com uma das especializações**. Você ganha 1 ponto por nível
e 1 por guardião derrotado (não dá para pegar tudo):

```
            ← PALADINO          TRONCO COMUM          BERSERKER →
Nv.2    [Pele de Ferro 2/3]  [Golpe Brutal 1/3]    [Fôlego 0/2]
Nv.4    [Luz Curativa 1/2]   [Contra-ataque 0/2]   [Sede Insaciável 0/2✗]
Nv.6    [Aura de Proteção]   [Muralha 0/1]         [Frenesi 0/2✗]
Nv.9    [Martírio 0/1]                             [Imortal 0/1✗]
```

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
- **Mago:** a mana é escassa: regenera pouco durante a luta, recupera só 20% depois dela e
  enche de verdade apenas descansando. O Dardo Arcano é de graça; cada Inferno é uma
  decisão.

Novas habilidades chegam nos níveis 2, 3, 4 e 7 (a habilidade suprema da especialização).

## O que deixa as jornadas diferentes

- **Mundo procedural:** mapa em grafo com vilas, regiões selvagens, covis e a Cidadela.
  Nomes de lugares, NPCs, guardiões e do vilão são gerados a cada partida.
- **88 eventos** com pesos dinâmicos. O que pode acontecer depende de classe,
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
- **Bestiário:** fraquezas e habilidades de cada criatura só aparecem depois de você
  derrotar algumas (magos estudam à primeira vista). Com 5 abates você vira mestre
  caçador daquela criatura (+10% de dano).
- **Legado entre partidas:** heróis anteriores deixam marcas no próximo mundo: o túmulo
  de quem caiu (com a arma dele e um espírito aliado), a estátua de quem venceu e
  baladas nas tavernas.
- **Inimigos com afixos** (feroz, ancião, corrompido, flamejante...), **traços**
  (voador, blindado, etéreo, morto-vivo...) e **fraquezas**. Use *Analisar inimigos*.
- **Clima e período do dia:** chuva enfraquece o fogo, a névoa ajuda a esquivar, a
  tempestade atrapalha disparos e à noite os monstros ficam mais fortes.
- **Contratos** no mural das vilas: caçadas, alvos com recompensa e entregas (com
  imprevistos no caminho). Dá para abandoná-los pelo Diário, perdendo reputação.

## Estrutura do código

```
rpg/
  jogo.py        estado, ciclo principal, vilas, loja, contratos, salvar/carregar
  tui.py         interface moderna (Textual): log, opções, painel do herói e mapa
  ui.py          interface clássica (cores ANSI, menus) e o "jogador robô" dos testes
  mapa.py        desenho do mapa em caracteres
  talentos.py    árvores de talentos
  legado.py      registro de heróis anteriores
  sobrevivencia.py  fome, ferimentos, infecção e escuridão
  combate.py     combate por turnos, efeitos, traços e fraquezas
  classes.py     classes, especializações, habilidades e companheiros
  inimigos.py    geração de inimigos, guardiões, chefe final e habilidades inimigas
  mundo.py       geração espacial do mundo e nível de cada região
  itens.py       consumíveis e equipamentos procedurais
  dados.py       biomas, criaturas, afixos, clima e guardiões
  texto.py       nomes procedurais e utilidades de texto
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

Um "jogador robô" joga dezenas de partidas com escolhas aleatórias, força cada evento
em todas as classes e especializações, testa as árvores de talentos, o mapa e a
interface Textual (em modo headless).
