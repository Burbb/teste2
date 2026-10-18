/* Prova de fidelidade da coluna da ficha (em avaliação, nada no jogo): só pede os desenhos de sempre em tamanhos
   maiores. O busto do herói em 120 px (o desenho de 40×40 a ×3, pixel a pixel; ×6 na tela 2x) e os ícones dos
   atributos em 32 px (os arquivos de 32 que já existem). Nenhum desenho novo. */
"use strict";

(() => {
  Icones.retrato = function retrato(nome, alt = "") {
    if (!Retratos.tem(nome)) return "";
    const u = (x) => Retratos.url(nome, "busto", (x * 120) / Retratos.lado(nome, "busto"));
    return `<picture class="desenho pixel"><img class="original" src="${u(1)}" srcset="${u(2)} 2x" width="120" height="120" alt="${alt}" draggable="false"></picture>`;
  };
  const atributo = Icones.atributo;
  Icones.atributo = (nome, lado = 32) => atributo(nome, lado);
})();
