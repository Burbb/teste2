/* O estudo da ocupação dos ícones no inventário (experimento): a alternativa mostra o equipamento do corpo e da
   mochila em 40 px em vez de 32 (a regra .slot-px img.desenho de 14-hud.css fixa 32), com os arquivos nativos de 40 (ocupacao_icones.py), sem mexer no espaço (60 px no
   corpo, 56 na mochila), na borda, na raridade, no foco nem nos números. Só para as fotografias
   (fotografar_ocupacao.mjs põe este arquivo na página; o jogo não o carrega). As silhuetas dos espaços vazios, a bolsa,
   a doca, os atributos e a luta ficam como estão. */
"use strict";

(() => {
  const LADO = 40, PECAS = ["escudo", "anel", "cota", "espada"];
  const ARQ = new RegExp(`/hud/icones/(${PECAS.join("|")})-32\\.png$`);
  function trocar(i) {
    const m = (i.getAttribute("src") || "").match(ARQ);
    if (!m || i.classList.contains("fantasma") || !i.closest(".tela.inventario .espaco, .tela.inventario .celula")) return;
    i.src = `/__prototipo/ocupacao/${m[1]}-${LADO}.png`;
    i.srcset = `/__prototipo/ocupacao/${m[1]}-${LADO}@2x.png 2x`;
    i.width = i.height = LADO;
    // o CSS da HUD fixa 32 px em toda imagem de espaço (14-hud.css: .slot-px img.desenho): aqui, só nestas
    i.style.setProperty("--s", LADO);
    i.style.setProperty("width", `${LADO}px`, "important");
    i.style.setProperty("height", `${LADO}px`, "important");
    i.classList.add("ocupacao");
  }
  const tudo = () => document.querySelectorAll("img:not(.ocupacao)").forEach(trocar);
  new MutationObserver(tudo).observe(document.body, { childList: true, subtree: true });
  tudo();
})();
