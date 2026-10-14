/* Controles de desenvolvimento da HUD experimental (avaliação, não são configuração do jogador e não vão para o save).
   Superfície (jogo/superficies.css): pelo endereço (&superficie=escura ou &superficie=escura-transicao) ou, com o jogo
   aberto, Ctrl+Alt+S passa de uma para a outra (atual, escura, escura com transição); um aviso curto diz qual ficou.
   Teste de arte (arte-teste.js: o mercador no balcão e o baú na bolsa): ligado; &arte=jogo ou Ctrl+Alt+A mostram o que
   era antes, para comparar. */
"use strict";

(() => {
  const SUPERFICIES = ["atual", "escura", "escura-transicao"];
  const NOMES = { atual: "atual", escura: "mais escura", "escura-transicao": "mais escura, com transição embaixo da arte" };
  function usar(s) {
    if (s === "atual" || !SUPERFICIES.includes(s)) delete document.body.dataset.superficie;
    else document.body.dataset.superficie = s;
  }
  const pedido = new URLSearchParams(location.search);
  usar(pedido.get("superficie") || "atual");
  if (pedido.get("arte") === "jogo") document.body.dataset.arte = "jogo";

  let aviso = null, tempo = 0;
  function avisar(texto) {
    if (!aviso) {
      aviso = document.createElement("div");
      aviso.className = "hud-dev-aviso";
      aviso.setAttribute("role", "status");
      document.body.appendChild(aviso);
    }
    aviso.textContent = texto;
    aviso.hidden = false;
    clearTimeout(tempo);
    tempo = setTimeout(() => { aviso.hidden = true; }, 1800);
  }
  document.addEventListener("keydown", (ev) => {
    if (ev.ctrlKey && ev.altKey && ev.code === "KeyA") {
      ev.preventDefault(); ev.stopPropagation();
      if (document.body.dataset.arte === "jogo") delete document.body.dataset.arte; else document.body.dataset.arte = "jogo";
      if (window.HUD_PASSAR) window.HUD_PASSAR();
      avisar(`Teste de arte: ${document.body.dataset.arte === "jogo" ? "desligado (o desenho de antes)" : "ligado (mercador e baú)"}`);
      return;
    }
    if (!(ev.ctrlKey && ev.altKey && ev.code === "KeyS")) return;
    ev.preventDefault(); ev.stopPropagation();
    const agora = document.body.dataset.superficie || "atual";
    const prox = SUPERFICIES[(SUPERFICIES.indexOf(agora) + 1) % SUPERFICIES.length];
    usar(prox);
    avisar(`Superfície (teste): ${NOMES[prox]}`);
  }, true);
})();
