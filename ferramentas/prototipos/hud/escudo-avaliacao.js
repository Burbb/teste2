/* A avaliação do teste do escudo (itens-icones-teste.html mostra), olhada no tamanho real, no jogo
   (capturas-escudo/). É a leitura de quem desenhou; a decisão é do Jean. */
"use strict";

window.AVALIACAO_ESCUDO = (() => {
  const L = [
    ["Volume", "A bossa em cúpula com o ponto de luz e o reflexo grande no gomo de cima dão o volume; o aro é uma linha, sem espessura.",
      "O aro é um rolo, com luz em cima e sombra embaixo, e a lateral do escudo aparece embaixo e à direita; a bossa projeta sombra na face; cada gomo é um plano. Em 48 e 64, o volume é maior que o do atual. Em 32, a espessura do aro ainda aparece, mas o desenho fica cheio de anéis."],
    ["Material", "O ferro lê como metal polido (o reflexo quase branco) e o latão tem brilho forte na cúpula.",
      "O ferro lê como metal mais escuro, com o reflexo correndo dentro de um gomo; o latão do aro lê bem; a cúpula tem menos brilho que a do atual."],
    ["Contraste", "Bom em todos os tamanhos: o reflexo e a bossa se destacam do carvão; o aro fino e o contorno escuro seguram a silhueta.",
      "A silhueta é a mais forte das duas (o aro claro inteiro e o contorno de 1 pixel). Por dentro, o ferro é mais escuro e o contraste fica concentrado no reflexo e na bossa."],
    ["Presença visual", "Maior em 32 px: o reflexo e a bossa grande fazem o objeto ler de longe.",
      "Maior em 64 px (o cartão do saque) e no voo; menor em 32, onde o aro claro e o sulco escuro em volta da bossa disputam com ela."],
    ["Construção", "Os gomos aparecem só pela mudança de tom; a bossa não tem base.",
      "Frente, degrau, aro, sulco da base, bossa e cravos separados, com sombra entre eles: a construção fica clara."],
    ["Convivência com os outros ícones", "É da família pintada (o elmo, a cota, as botas, a espada).",
      "Mais renderizado que a família pintada: ao lado da espada e do elmo atuais, parece de outro conjunto, sobretudo em 64."],
  ];
  return `<table><tr><th></th><th>atual</th><th>candidato</th></tr>${L.map(([c, a, b]) => `<tr><td><b>${c}</b></td><td>${a}</td><td>${b}</td></tr>`).join("")}</table>` +
    `<p class="nota" style="margin-top:10px"><b>Conclusão:</b> o atual continua melhor no tamanho que mais importa (32 px, o
    inventário, o mercado e a ficha): lê mais limpo e tem mais presença, e conversa com o resto da família pintada. O
    candidato mostra o que falta ao atual de perto (a espessura do aro, a lateral, a bossa com base e sombra, os gomos
    como planos) e ganha em 48 e 64 px, mas a cúpula dele tem menos brilho e o conjunto destoa da família. Se essa
    direção servir, o caminho é levar ao atual só o que ele não tem (o aro com espessura e a lateral, a sombra da
    bossa), mantendo o reflexo, a cúpula e o desenho pintado dele, e não trocar o escudo pelo candidato.</p>`;
})();
