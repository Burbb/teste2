# Protótipo do acampamento (fora do jogo)

**Integrado na 1.98.0** (`rpg/web/static/telas/acampamento.js` e `telas/fogueira.js`): o que está aqui fica como
registro da proposta aprovada; o jogo não lê nada desta pasta.

Um protótipo visual, para avaliar. O acampamento de produção (`rpg/web/static/telas/fogueira.js`) continua como está;
nada aqui é lido pelo jogo.

**O pedido de Jean (15/10/2026):** aproximar a composição do acampamento da qualidade dos ambientes da Capela Afogada,
começando pelo acampamento do lado de fora da capela. O fogo e a luz já funcionam; o que se busca é composição,
profundidade e a relação dos personagens com o espaço (um grupo acomodado para descansar), em estilo minimalista: cada
elemento ajuda a entender o lugar ou a presença dos viajantes. Os personagens são os fechados na 1.97.0 (o Mago com a
figura sentada da fogueira, o Morel com a figura recuperada e a espada corrigida, os outros como estão), com a aljava
do Arqueiro da 1.97.1. Nada de mecânica nova.

## Como abrir

O protótipo roda dentro do jogo, num cenário preparado (o herói do lado de fora da capela, à noite, com a comitiva):

```
python ferramentas/prototipos/acampamento/cenario_acampamento.py capela_fora
```

Abra o endereço que aparecer e escolha **Acampar e descansar até o amanhecer**. Variações pelo ambiente (no PowerShell,
`$env:NOME="valor"` antes do comando; `Remove-Item Env:NOME` para limpar):

| Variável | O que faz |
|---|---|
| `PROTOTIPO=0` | o jogo como está (a fogueira de produção), para comparar |
| `CLASSE` | a classe do herói (padrão `mago`) |
| `COMITIVA`, `RESERVA` | quem vai com você e quem fica no acampamento (padrão `morel,odete` e `yara`) |
| `FERIDO` | quem está ferido (`odete`) |
| `FERA=1` | o lobo do patrulheiro (com `CLASSE=arqueiro`) |
| `PERIODO`, `CLIMA` | a hora (0 manhã, 2 crepúsculo, 3 noite, o padrão) e o clima (`chuva`, `neve`...) |

O cenário serve uma cópia da pasta `static` com `acampamento-no-jogo.js` colado ao fim de `telas/fogueira.js`; a pasta
do jogo não muda.

## O que o protótipo faz

- **A cena no topo, como a capela.** O acampamento ocupa a área de cenário do topo (o mesmo quadro de 320×72 da
  paisagem e das salas da capela, pela `Vista.usarAmbiente`), com as figuras clicáveis por cima, na mesma conta das
  salas (`Vista.caixaDaArte`). Embaixo, só a frase da chegada, a instrução, o contador e quem vai e quem fica. A imagem
  não se repete no texto, e o palco com moldura da produção sai.
- **Três planos.** Longe: o céu da hora (o mesmo da paisagem e da capela), a outra margem com árvores mortas, a névoa e
  a capela pequena, afundada até a metade das janelas, com a torre sem sino, o rombo no telhado e o reflexo, apagada à
  esquerda para não disputar com o fogo. Meio: um teso de terra seca acima do brejo (a água fica atrás, encostando na
  beira), com o fogo, a luz dele no chão e a roda. Perto: o barranco escuro com capim nos dois cantos de baixo.
- **O fogo da produção.** O mesmo desenho, o mesmo movimento, as mesmas fagulhas e os mesmos anéis de luz, levados para
  o novo lugar (o centro das toras em 166,60). De dia, a luz no chão fica mais fraca.
- **A roda.** O herói num tronco à esquerda do fogo; quem vai com você à direita (um num tronco, na frente; o outro numa
  pedra, do outro lado do fogo, mais longe); quem fica no acampamento na beira da luz, perto da barraca (na manta ou numa
  pedra), com um véu leve de penumbra; o animal deitado ao lado do herói. Cada assento é mais largo que a figura (as
  pontas aparecem dos dois lados) e tem sombra no chão, puxada para fora do fogo. As figuras de perto ganham um calor
  leve na metade virada para o fogo, só por cima dos pixels delas: rosto, cabelo, capuz e cores continuam os mesmos.
- **Poucos objetos.** A barraca (já existia), a mochila e o cobertor enrolado ao lado dela (vocês vão dormir aqui) e o
  cantil encostado no tronco de quem vai com você. Nenhum é clicável nem faz nada.
- **O mesmo jogo.** Os menus de cada companheiro (`Telas.ligarFigurasComitiva`): conversar, deixar no acampamento,
  levar amanhã, o carinho no animal; o "Dormir até o amanhecer" no canto de cima; os nomes que se acomodam sozinhos
  (a mesma regra da produção). A cena mostra quem está presente agora: deixar alguém no acampamento muda o lugar dele
  na cena. A conversa abre no cartão de sempre; ao sair da fogueira (dormir, viajar), a paisagem ou a capela voltam.

## O que fica para depois

- Só o lado de fora da Capela Afogada. Outros biomas e lugares usariam a mesma organização (o céu, o fundo do lugar, o
  teso com a roda, o primeiro plano), cada um com o fundo desenhado à mão, como as salas da capela; nada genérico foi
  antecipado.
- A posição das figuras é fixa por vaga (como na produção). Com mais companheiros, as vagas precisariam crescer.
- A orientação D3 do tutorial aponta o "Dormir" dentro do texto; no protótipo ele mora na cena (a orientação não o
  acha). Se o protótipo for aprovado, a orientação passa a apontar para a cena.

## O que tem aqui

| Arquivo | O que é |
|---|---|
| `acampamento-no-jogo.js` | O protótipo: a cena (`base`, `desenhar`), a tela de baixo e as figuras sobre a arte. |
| `cenario_acampamento.py` | O cenário: o herói do lado de fora da capela, com a comitiva, e a cópia da pasta `static` com o protótipo. |
| `fotografar_acampamento.mjs` | As fotos (Playwright): atual × protótipo, as interações e as condições, em 1500×950 e 1280×720. |
| `capturas/` | As fotos desta rodada; `*-comparacao-atual-prototipo.png` põe as duas lado a lado, em tamanho real. |
