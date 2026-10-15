/* Teste do retrato (experimento): veste o herói do jogo de verdade com o candidato da classe dele (arte-teste.js), só
   para a comparação (fotografar_retrato.mjs e fotografar_retratos_classes.mjs põem este arquivo na página depois de
   abrir um cenário). O jogo não carrega este arquivo: o retrato de produção continua o de retratos.js (o Guerreiro) e
   o sprite da classe (Mago e Arqueiro). Troca as três imagens do herói, nos mesmos lugares e com as classes que as
   regras de tamanho da HUD usam: o busto da ficha (80 px; 64 em janela baixa, pelo mesmo <picture>), a cabeça do
   topo (48 px) e a da carta da luta (32 px). Como os painéis se redesenham a cada mudança do jogo, um observador
   refaz a troca. */
"use strict";

(() => {
  const classe = () => (App.estado && App.estado.heroi && App.estado.heroi.classe) || "guerreiro";
  const uma = (peca, escala, cl, alt = "") => ArteTeste.img(peca, escala, cl, alt);
  function busto(c, alt) {
    const baixo = ArteTeste.url(`${c}-busto-baixo`, 2), baixo2 = ArteTeste.url(`${c}-busto-baixo`, 4);
    return `<picture class="desenho candidato"><source media="(max-height: 800px)" srcset="${baixo}, ${baixo2} 2x">` +
      uma(c, 2, "original", alt) + "</picture>";
  }
  function vestir() {
    const c = classe();
    if (!ArteTeste.PECAS[c]) return;
    document.querySelectorAll("#heroi .retrato-grande").forEach((r) => {
      if (r.querySelector(".candidato")) return;
      const velho = r.querySelector("img");
      r.innerHTML = busto(c, velho ? velho.alt : "");
    });
    document.querySelectorAll(".hud-retrato img:not(.arte-teste)").forEach((i) => {
      i.outerHTML = uma(`${c}-cabeca`, 2, "sprite desenho", i.alt);
    });
    document.querySelectorAll(".carta.heroi .icone img:not(.arte-teste)").forEach((i) => {
      i.outerHTML = uma(`${c}-carta`, 2, "sprite desenho", i.alt);
    });
  }
  // pixel a pixel, sem suavizar, em qualquer tamanho
  document.head.insertAdjacentHTML("beforeend", "<style>img.arte-teste { image-rendering: pixelated; }</style>");
  new MutationObserver(vestir).observe(document.body, { childList: true, subtree: true });
  vestir();
})();
