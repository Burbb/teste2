/* Estudo do conjunto da HUD (em avaliação, nada no jogo): põe a pintura espelhada (conjunto.css) na mesa, como peça
   própria atrás da coluna do mundo, igual à da ficha (../ficha/pintura.js). Só decoração: sem conteúdo, sem clique. */
"use strict";

(() => {
  const mesa = document.getElementById("mesa");
  if (mesa && !mesa.querySelector(".mundo-pintura")) {
    const d = document.createElement("div");
    d.className = "mundo-pintura";
    d.setAttribute("aria-hidden", "true");
    mesa.appendChild(d);
  }
})();
