/* O dado dos testes durante a queda de braço (protótipo; nada disto entra no jogo).

   No jogo, a rolagem do centro (app/rolagem.js) põe o grupo do dado no meio da altura da cena e um véu escuro sobre o
   palco, e a arte fica escura atrás dele. Na queda de braço, o esforço dos braços enquanto o dado gira é parte do que se
   lê. Com uma pose da queda de braço à vista (a faixa do protótipo; depois, a cena da disputa), o grupo desce para logo
   embaixo da arte (inteiro na janela; a doca fica atrás dele por um instante) e o véu cobre só a página, não a arte.
   O dado, o tempo, o som, o resultado e a descida até a tirinha são os do jogo: só a posição muda. Se a apresentação
   for integrada, isso vira uma opção da rolagem (uma cena com ação). */
"use strict";

(() => {
  const naQueda = () => /^(qd|q3|qv)/.test(document.body.dataset.tavCand || "")
    || !!(window.Cenas && Cenas.atual() && Cenas.atual().d.cena === "taverna_queda");
  new MutationObserver((mudancas) => {
    for (const m of mudancas) for (const n of m.addedNodes) {
      if (!(n instanceof HTMLElement) || !n.classList.contains("rolagem-centro") || !naQueda()) continue;
      const grupo = n.querySelector(".rc-grupo"), veu = n.querySelector(".rc-veu");
      const arte = document.getElementById("vista").getBoundingClientRect();
      const palco = document.getElementById("palco").getBoundingClientRect();
      const topo = Math.round(Math.min(arte.bottom + 6, innerHeight - grupo.offsetHeight - 4));
      grupo.style.top = topo + "px";
      Object.assign(veu.style, { top: Math.round(arte.bottom) + "px", height: Math.max(0, Math.round(palco.bottom - arte.bottom)) + "px" });
      veu.style.setProperty("--cy", "40%");
      n.classList.add("tav-queda");
    }
  }).observe(document.body, { childList: true });
})();
