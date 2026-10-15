/* Teste do retrato (experimento): veste o Guerreiro do jogo de verdade com o candidato de arte-teste.js, só para a
   comparação (fotografar_retrato.mjs põe este arquivo na página depois de abrir um cenário). O jogo não carrega este
   arquivo: o retrato de produção continua o de hud/icones/. Troca as três imagens que Icones dá ao Guerreiro, nos
   mesmos lugares e com as mesmas classes (as regras de tamanho da HUD valem igual): o busto da ficha (80 px; 64 em
   janela baixa, pelo mesmo <picture>), a cabeça do topo (48 px) e a da carta da luta (32 px). Como os painéis se
   redesenham a cada mudança do jogo, um observador refaz a troca. */
"use strict";

(() => {
  const uma = (peca, escala, classe, alt = "") => ArteTeste.img(peca, escala, classe, alt);
  function busto(alt) {
    const baixo = ArteTeste.url("guerreiro-busto-baixo", 2), baixo2 = ArteTeste.url("guerreiro-busto-baixo", 4);
    return `<picture class="desenho candidato"><source media="(max-height: 800px)" srcset="${baixo}, ${baixo2} 2x">` +
      uma("guerreiro", 2, "original", alt) + "</picture>";
  }
  function vestir() {
    document.querySelectorAll("#heroi .retrato-grande picture.desenho:not(.candidato)").forEach((p) => {
      p.outerHTML = busto(p.querySelector("img") ? p.querySelector("img").alt : "");
    });
    document.querySelectorAll(".hud-retrato img.desenho:not(.arte-teste)").forEach((i) => {
      i.outerHTML = uma("guerreiro-cabeca", 2, "sprite desenho", i.alt);
    });
    document.querySelectorAll(".carta.heroi .icone img.desenho:not(.arte-teste)").forEach((i) => {
      i.outerHTML = uma("guerreiro-carta", 2, "sprite desenho", i.alt);
    });
  }
  // pixel a pixel, sem suavizar, em qualquer tamanho
  document.head.insertAdjacentHTML("beforeend", "<style>img.arte-teste { image-rendering: pixelated; }</style>");
  new MutationObserver(vestir).observe(document.body, { childList: true, subtree: true });
  vestir();
})();
