/* Prova da ficha, rodada 2: põe a pintura (pintura.css) na mesa, como peça própria atrás da coluna da ficha. Só
   decoração: sem conteúdo, sem clique, fora da leitura (aria-hidden). */
"use strict";

(() => {
  const mesa = document.getElementById("mesa");
  if (mesa && !mesa.querySelector(".ficha-pintura")) {
    const d = document.createElement("div");
    d.className = "ficha-pintura";
    d.setAttribute("aria-hidden", "true");
    mesa.prepend(d);
  }
})();
