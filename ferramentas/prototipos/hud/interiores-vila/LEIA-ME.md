# Etapa 5: interiores da Curandeira, do Templo e da Taverna (levantamento e esboço inicial)

> **Histórico.** O estado atual está no código e nos registros recentes: a curandeira foi integrada na 1.218.0 (`ferramentas/prototipos/curandeira`); o templo tem duas candidatas em `ferramentas/prototipos/templo`. Os trechos abaixo sobre a curandeira e a forja descrevem o ponto de partida, já superado.

28/10/2026, sobre a 1.214.0. **Nada desenhado e nada mudado no jogo.** É o ponto de partida da seção 5 do
[23](../../../../roadmapIDEIAS/23-PLANO-DE-ARTE-INTERFACE-E-COMBATE.md) ("Templo/igreja, Curandeira e Taverna, cada
interior com composição e identidade próprias; não fazer três cópias da capela"), feito pela skill `arte-cenas-fenda`.
A etapa 4 (a forja) continua aberta: o Jean ainda avalia o feixe das armaduras, a paleta da celebração e o equilíbrio.

`fotografar_hoje.mjs` fotografa os três lugares como estão (cenário `grupo`, 1920×945) em `capturas-hoje/`;
`folha-hoje.png` junta a taverna, o templo, a curandeira e a forja (a única com interior) na mesma escala.

## Como o jogo mostra os três hoje

| Lugar | O que acontece ao entrar | Serviços (cartões) | Quem atende (o que o jogo diz) |
|---|---|---|---|
| Taverna | a câmera da vila aproxima o prédio; embaixo, o balcão com os cartões | Dormir até o amanhecer; Uma bebida e os rumores | o taverneiro ("nem levanta os olhos"); dentro, a bebida pode virar briga, queda de braço ou a conversa com o homem do canto (Morel, enquanto não foi recrutado); Vó Berta aparece "na janela da taverna" no retorno |
| Templo | a câmera aproxima a igreja (foco na cruz do campanário); o balcão | cuidar da vida (o herói, com o primeiro atendimento grátis) e de cada companheiro, cada um com o seu preço | "um clérigo cansado, de mãos firmes"; "velas, incenso"; o sino no som de entrar |
| Curandeira | uma tela própria, como o mercado (o cabeçalho com o atendente e a fala), sem cena: a vista continua a vila aproximada | um cartão por ferimento, com o preço | no Vau: Pita, a aprendiz (14 anos, mói ervas, ferve água), e depois Marta, "ainda magra da febre", quando a água limpa (`consequencias.atendente`); fora do Vau, "uma velha de mãos manchadas de sangue seco" |

A forja é a referência do caminho técnico: o motor anuncia a cena (`ui.cena("A forja", …)`), a tela desenha o
interior por camadas (`telas/cena-forja.js`, `cenas/forja/*.png`, 320×96) e os cartões ficam embaixo, com o Voltar
e o Esc. Os três lugares não precisam de serviço novo: a cena entra no lugar da vila aproximada.

## O uso de cada cena (esboço; não decidido)

**Curandeira: um ofício de perto.** Uma pessoa trabalhando (a câmera da forja, ~55 px de figura): a cabana baixa e
escura, a bancada de ervas com o pilão, o caldeirão ou a chaleira no fogo (a "água fervendo para os doentes"), os
maços pendurados em pregos nas vigas, as prateleiras de potes, a esteira ou a cama de palha de um doente no canto. A
atividade: moer ervas ou mexer a água (ciclo curto, sem o ritmo da martelada). **Dois estados do mesmo lugar:** Pita
sozinha (Marta deitada, ao fundo, enquanto está de cama) e Marta de pé, magra, atendendo; a cena muda com a missão,
como a fala já muda. Foco: a mesa de tratar, onde o cartão do ferimento "acontece".

**Templo: um espaço de pé-direito alto, quieto.** A nave vista de frente ou um pouco de lado: a luz dos vitrais (os
mesmos do prédio na vila) cortando o escuro, o altar com as velas, o banco de madeira, o incenso subindo, o clérigo
cansado junto de uma maca ou de um banco onde se senta quem é tratado. A câmera mais aberta que a da curandeira: a
arquitetura é o assunto; a figura menor. Movimento discreto: chamas, fumaça, a luz que pisca, o clérigo que reza ou
enrola uma atadura. Cuidado com a capela afogada (lugar da campanha, outra igreja): esta é viva, seca e cuidada.

**Taverna: um salão com várias pessoas.** A vista mais distante (rostos simplificados, figura de ~25 px, como a Ilse):
o balcão com o taverneiro, a lareira, duas ou três mesas com fregueses, palha no chão, a escada para os quartos (o
Dormir), a fumaça. O canto escuro com o homem sozinho (Morel antes de ser recrutado; depois, a mesa vazia). Pontos que
podem virar "lugares" dos cartões: o balcão (a bebida e os rumores), a escada (o quarto). Os acontecimentos que já
existem (briga, queda de braço) pedem só que a cena não os contradiga; não precisam de animação própria agora.

**Quadro:** 320 de largura; a altura da forja (96) serve às três e mantém os cartões no mesmo lugar nas duas janelas
(conferir na 1280×720 antes de aprovar). As câmeras diferem de propósito (a curandeira de perto, a taverna de longe);
a proporção se confere dentro de cada cena, não entre elas.

## Recomendação de ordem

1. **Curandeira primeiro.** É a menor (uma figura, um cômodo), já é uma tela própria como a forja (a cena entra no
   mesmo lugar sem mexer no fluxo) e testa o que é novo nesta etapa: um interior que muda com a história (Pita e
   Marta).
2. **Templo.** A taverna e o templo hoje abrem o balcão sobre a vila aproximada; trocar isso por um interior é uma
   decisão de fluxo (o Jean precisa ver a primeira para decidir), e o templo, com uma figura e pouca ação, é o passo
   mais curto.
3. **Taverna** por último: várias figuras, a escala mais distante e os acontecimentos.

## O que espera o Jean (as três aprovações da skill, uma de cada vez)

- **A ordem** acima (ou outra).
- **As referências de composição** de cada lugar (imagens que ele escolher ou aprovar; guardadas sem alteração em
  `ferramentas/arte/referencias/<lugar>/`, com a origem). O acabamento vem das cenas aprovadas do jogo (a forja H2, a
  capela, a prisão da Ilse, a cidade, o mercado).
- **A troca do balcão sobre a vila por um interior** na taverna e no templo, quando houver uma candidata para ver.

Depois disso, a primeira candidata (provavelmente a curandeira) numa pasta própria, com a folha ao lado das cenas
aprovadas e a demonstração no navegador para o movimento.
