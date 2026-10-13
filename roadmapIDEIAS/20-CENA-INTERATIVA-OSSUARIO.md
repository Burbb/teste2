# 20 — A primeira cena interativa: o ossuário e o sarilho (1.72.0)

Pedido de Jean (13/10/2026): começar a representação visual da campanha pela capela, com uma cena só: o ossuário, com
a interação do sarilho. Clicar no sarilho enquadra o mecanismo e abre as alternativas que já existiam; quem decide e
resolve é o motor; a cena mostra o resultado confirmado. A referência visual foi o protótipo da capela (artifact de
13/10), usado como linguagem (pixel inteiro, paleta curta, pontilhado, 10 quadros por segundo, câmera que aproxima),
não como regra nem como código.

## Decisões

- **Uma cena, um ponto.** Só o ossuário e só o sarilho. Nada de sala, encontro, recompensa ou pista nova; Passear e
  Explorar ficam como estavam.
- **Onde aparece:** na página da Capela Afogada, depois de o ossuário ter sido visto (a pista `correntes`), entre o
  cabeçalho do lugar e as escolhas. Só na tela gráfica: no terminal nada muda.
- **O ponto faz a ação do menu, não outra.** O sarilho manda a mesma escolha que "Soltar as correntes"
  (`missao` + `acao_missao` na meta da opção). Se a ação não está no menu agora, o clique não faz nada além de dizer
  por quê. Clicar não solta corrente, não gasta tocha nem flecha, não sorteia e não escolhe o método.
- **De perto:** depois do clique, a câmera aproxima o mecanismo (o pontilhado que se fecha, como a câmera da vila) e
  a cena "O Sarilho" abre com o enquadramento no tambor, na trava e nas correntes até o buraco, e as três escolhas
  de antes (à mão, o método da classe, deixar como está), com custos, riscos e testes iguais.
- **O motor diz o estado** (`missoes.cena_ossuario`): correntes `presas` ou `soltas` pelo preparo `corpo_solto`; o
  que o ponto faz (ou nada, com o estado escrito para quem clica). A tela não deduz.
- **A animação mostra, não decide.** A corrente só desce depois que o preparo foi gravado (`_soltar`), por uma
  celebração (`celebrar("correntes")`) que a tela gráfica recebe. Com luta (à mão, ou a trava que não cede), as
  correntes seguem presas na cena durante a luta e só descem depois da vitória. Fugir ou cair deixa tudo como
  estava: presas, e a ação de novo no menu.
- **Recarregar e carregar não repetem nada.** A página refeita (recarga do navegador) e o save carregado desenham as
  correntes já soltas, sem som e sem a descida.
- **Sem regra duplicada na tela:** nada de custo, teste, disponibilidade ou estado calculado no cliente.
- **Componente pequeno, não arquitetura:** `telas/cenas.js` registra o tipo `cena` com uma cena só (`ossuario`). A
  próxima cena entra no mesmo arquivo, com o mesmo contrato (o motor manda `cena`, `pontos` com `acao` e `estado`).
  Sem editor e sem formato genérico de cenas por enquanto.

## Implementação

- `rpg/missoes.py`
  - `cena_ossuario(g, mid, foco)`: o painel (`cena`, `correntes`, `foco`, `pontos`, `titulo`).
  - `mostrar_cena(g)`: manda o painel na página da capela; chamada em `Jogo.menu_selvagem`.
  - `_soltar_correntes` e a vitória da onda de afogados mandam o painel de perto (`foco="sarilho"`).
  - `_soltar`: grava o preparo e, só então, `celebrar("correntes")` (só na tela gráfica: `conquistas_na_tela`).
  - `opcoes()`: a meta de cada ação de missão leva `acao_missao` (o mesmo id), para o ponto achar a opção.
- `rpg/web/static/telas/cenas.js` (novo)
  - O ossuário em pixel art: 320×72 lógicos, pixel 2× (a largura acompanha a página, as paredes continuam dos lados).
    Paredes de pedra, abóbada, nichos com ossos, a escada do alçapão com a luz, a tocha que treme, ossos no chão, o
    buraco com água; o sarilho com postes, trave, tambor com a corrente enrolada, roda dentada com a trava, manivela
    e as duas correntes até o buraco.
  - O ponto clicável é um `<button>` sobre a arte: acende com mouse e com foco de teclado (o desenho fica dourado e o
    contorno tracejado aparece no foco), Enter e espaço funcionam, o nome "Sarilho" fica sempre à vista (não depende
    de passar o mouse) e o `aria-label` diz o que ele faz ou o estado.
  - A descida: 27 quadros (a trava erguida, o tambor girando, os elos correndo para o buraco, um tranco leve, as
    ondas na água) e o som novo `corrente`. Se a cena tiver saído da vista (o resultado empurrou a página), a página
    sobe até ela, a corrente desce e a leitura volta para baixo.
  - Movimento reduzido: sem tocha tremendo, sem aproximação animada e sem descida (as correntes aparecem soltas); o
    som fica, porque não é movimento. Som desligado: o de sempre (`App.som` não toca).
  - Tela baixa: se embaixo da cena não cabem as escolhas, a página do lugar começa na cena (o nome segue no painel ao
    lado). Na cena de perto, o texto puxa a página até as escolhas, como em qualquer cena.
- `rpg/web/static/app/nucleo.js`: a página do lugar com a cena não desce sozinha; a de perto segue o texto.
- `telas/celebracoes.js`: a celebração `correntes`. `som.js`: o som `corrente`. `css/08-mercado.css`: o palco, o ponto
  e o nome. `index.html`: o `<script>`.

## Validação

- **Testes:** `tests/test_cena_ossuario.py` (o ponto faz a ação do menu; de perto o ponto não age; só na capela e
  depois do ossuário; abrir e voltar não gasta nem celebra; a corrente desce só depois do preparo, com e sem a trava
  cedendo; fuga e derrota não soltam; o terminal sem celebração) e os de antes (`test_missoes`, `test_guardia`,
  `test_riscos_noite`).
- **Gabarito:** idêntico. Nenhuma das 24 partidas passa pela página da capela com o ossuário visto na tela gráfica, e a
  meta nova das opções não entra nas transcrições.
- **Fumaça:** `cenarioSarilho` ganhou o ossuário desenhado com as correntes presas, o mouse e o foco acendendo o
  sarilho, Enter e clique abrindo as mesmas alternativas sem gastar nada, e a volta com a sala de antes;
  `cenarioGuardia` confere a sala com as correntes soltas e o sarilho sem ação.
- **Conferido na tela (1500×950, 1500×700, 1280×800, 1280×700):**
  - o ponto com mouse e com teclado; a aproximação; "Deixar como está" sem gastar nada (tocha, flecha, hora);
  - o método da classe (paladino, sucesso no teste de Força): a corrente desce depois do resultado, com som;
  - o caminho à mão: a luta com as correntes ainda presas na cena, a vitória, a descida, a tocha gasta e a tarde;
  - a fuga (correntes presas, a ação de volta) e a derrota em nível 1 (resgate no Vau, correntes presas);
  - a recarga do navegador no meio da cena e depois dela, e salvar, sair e carregar: correntes soltas, sem som nem
    descida repetidos;
  - movimento reduzido (sem animação, com o som) e telas baixas (as escolhas à vista);
  - nenhum erro no console.

## Limitações

- A cena de perto, em telas baixas (1280×800 e menores), fica acima do texto e sai da vista quando o texto chega às
  escolhas; ela volta à vista sozinha só para a corrente descer.
- A recuada depois da fuga ("Você sobe pelo alçapão...") mostra a paisagem de fora, não o ossuário: é o texto de
  antes, e a cena da sala volta na página da capela.
- O mago e o arqueiro usam o mesmo desenho da descida; o tiro no pino e o ferro apodrecendo não têm animação
  própria.
- Jean ainda não viu: teste humano pendente.

## Como Jean testa

1. `ETAPA=fundo python -m tests.navegador.cenarios capela` (no PowerShell: `$env:ETAPA="fundo"; python -m
   tests.navegador.cenarios capela`). A página da capela mostra o ossuário com o sarilho e as correntes esticadas
   até o buraco.
2. Passe o mouse no sarilho (ele acende) e depois use Tab até ele (acende igual). Clique ou aperte Enter: a câmera
   aproxima e aparecem as três formas de sempre. Escolha "Deixar como está": nada foi gasto.
3. De novo pelo sarilho, escolha o método da classe. Se passar no teste, a corrente desce na cena depois do
   resultado. Se não passar, vem a luta: repare que as correntes continuam presas até você vencer.
4. Em outra rodada, desenrole à mão e fuja da luta: a sala continua com as correntes presas e "Soltar as correntes"
   volta ao menu.
5. Com as correntes soltas, recarregue a página (F5) e depois salve, saia e carregue: as correntes aparecem soltas,
   sem som e sem a descida de novo.
6. Para ver direto a sala com as correntes soltas: `$env:PREPARO="correntes"` antes do mesmo comando.
