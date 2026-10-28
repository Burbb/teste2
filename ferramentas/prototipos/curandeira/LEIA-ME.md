# Protótipo: o interior da curandeira (candidata A)

28/10/2026. **Só no protótipo, esperando a avaliação do Jean.** O jogo não carrega esta pasta; a cabana do jogo
continua a tela de sempre, sem ambiente. Nada do templo nem da taverna foi começado. Feito pelo fluxo da skill
`arte-cenas-fenda`.

## Abrir

Dê dois cliques em `demo.bat` (ou `python ferramentas/prototipos/curandeira/demo.py` na raiz). O jogo abre no navegador
num **save temporário** (uma pasta nova a cada vez; os saves do Jean não são lidos nem tocados), na porta 8793: o
Guerreiro no Vau, com a campanha começada, um corte e uma mordida para tratar e 120 de ouro. Entre na **curandeira pelo
prédio da vila**. A faixa do alto troca o estado da história e mostra a pose parada:

| Botão | O estado (no save temporário) | Quem atende e o que a cena mostra |
|---|---|---|
| **Pita (Marta de cama)** | a chegada: a missão sem desfecho | Pita no almofariz ("mói ervas no lugar de Marta, que está de cama"); a cortina dos fundos fechada, sem mostrar Marta |
| **Pita (a água escura)** | a noite em que a fonte corre escura (Destruir, no mesmo dia) | Pita no almofariz; a panela fervendo forte e dois baldes de água junto do fogão ("ferve água para os doentes") |
| **Marta (de pé)** | a água limpou (Dar descanso, três dias depois) | Marta, magra, de lenço e mangas arregaçadas, no almofariz |
| **Pose parada** | — | a pose do movimento reduzido (o mesmo que a preferência do sistema) |

A troca só vale com a cabana aberta: o motor muda o estado e abre a cabana de novo. O serviço é o de produção
(`Servicos.curandeiro`), sem mudar: os cartões, os preços, quem atende e a fala. As duas não aparecem juntas: pela
história, uma atende de cada vez.

## O levantamento

- **O que o jogo estabelece** (`rpg/consequencias.py`, `rpg/missoes.py`, roadmapIDEIAS/11, seção 3): Marta é a
  curandeira, ajudou o herói no passado e está de cama com a febre; Pita, a aprendiz, uma menina de uns catorze anos,
  atende no lugar dela, "mói ervas" e, na noite da água escura, "ferve água para os doentes". Marta volta a atender
  quando a água limpa, "ainda magra da febre", e "arregaça as mangas". Nenhum registro descreve rosto, cabelo ou idade
  de Marta: o lenço de linho e o vestido verde-escuro são aparência desta candidata, não história.
- **O serviço:** tratar ferimentos, um cartão por ferimento. Pontos da cena: quem atende (leva aos cartões, como o
  ferreiro) e a Saída (o Voltar).
- **O lugar:** uma cabana de trabalho, não um laboratório: a pia e os panos junto da porta, a água no balde, as ervas
  secando numa vara, a bancada com o almofariz, a tábua, o pote e a lamparina, as prateleiras de potes e frascos, o
  fogão baixo de pedra com a panela e a coifa, a passagem para o quarto dos fundos com a cortina (só cenário: atrás
  dela, o escuro), o armário de potes, a esteira diante do fogão; o meio do chão livre para circular.

## A composição e a escala

O quadro é o da forja (320×96): a câmera próxima, a sala de frente, quem trabalha na ponta da bancada, voltada para a
porta e para o almofariz. Escala pela figura: Marta tem 52 px dos pés ao alto do lenço (~1,65 m); a bancada tem o
tampo a 27 px do chão (~85 cm); o almofariz, 5 px. Pita é menor (46 px) e pega o pilão mais embaixo. A luz: o fogão
e a lamparina quentes, a porta fria, a sala escurecendo em degraus longe deles (a mesma luz feita por cima da forja).

## O gesto

Moer no almofariz, decidido pelos apoios antes do ciclo: o almofariz parado no tampo; a mão de longe segurando a
borda dele; a ponta de baixo do pilão dentro da boca; só a ponta de cima gira numa elipse pequena (8 poses), e a mão
de perto e o antebraço acompanham (o cotovelo, meio passo). Tronco, cabeça e saia parados. Ritmo próprio: 200 ms por
pose (1,6 s por volta), três voltas e uma pausa de 1,2 s; o fogo e o vapor a 200 ms. Movimento reduzido: a primeira
pose, parada, com o fogo e o vapor parados.

## As fontes

- `desenho.py`: o ambiente em código (a sala, a porta, a pia, as ervas, a bancada e o almofariz, as prateleiras, a
  coifa e o fogão, a passagem, o armário, a esteira, a luz; o fogo, o vapor e os baldes; a frente).
- `figuras.py`: Pita e Marta (o corpo pelo contorno de cada linha, a cabeça numa grade à mão, os braços por segmentos)
  e as poses do giro.
- `exportar.py`: as camadas de `camadas/` (a demonstração lê delas); com `--ver`, composições ampliadas numa pasta
  `conferencia/` para conferir o desenho (trabalho, não entrega).
- `demo.py` e `tela/` (`cena-curandeira.js`, `curandeira.css`, `faixa.js`): a cena registrada ao lado da forja só na
  página da demonstração, a troca de estado e a faixa.

Ainda é desenho em código: se a candidata for aprovada, a fonte em Aseprite vem antes da integração (skill, seção 6).

## O que mudou durante o trabalho (o que a conferência pegou)

- Os braços de palito e o avental claro dominando a figura: o corpo redesenhado pelo contorno, braços com espessura, o
  avental num linho apagado.
- Os dois braços cruzados na frente do corpo liam como um "Λ": o braço que trabalha passou a ser o de perto (o que se vê
  inteiro); o de longe só aparece na mão que segura o almofariz.
- O almofariz longe do corpo deixava o antebraço reto como uma barra: ele foi para a ponta da bancada.
- O lenço cinza (e depois ruivo) lia como cabelo: linho claro com a linha do cabelo escuro na testa e o nó atrás.
- O vapor em grade de pontos e os maços fechando embaixo como cebolas: fiapos que sobem ondulando; maços estreitos no
  nó e abrindo para baixo, com a ponta irregular.

## Conferido

No navegador (Playwright), a 1920×945 e a 1280×720: a vila, a entrada pelo prédio, a cena nos três estados (quem
atende e a fala vindo do motor), a pose parada sem mudar, o ponto de quem atende levando ao cartão, um tratamento
cobrando pelo serviço de produção, o Esc de volta à vila, sem erros no console. A 1280, o segundo cartão de tratamento
pede rolagem, como os da forja.

## Para avaliar (Jean)

A composição e a identidade do lugar; Pita e Marta (aparência, proporção, leitura no tamanho do jogo); o gesto e o
ritmo; a noite da água escura (os baldes e a fervura); se a cabana deve trocar a tela de hoje quando for integrada.
