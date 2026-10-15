/* O padrão das cartas de combate no jogo de verdade, só para as fotografias (fotografar_cartas.mjs põe este arquivo na
   página depois de abrir uma luta; o jogo não o carrega). window.CARTAS = { versao: "anterior" | "candidata" }:
   - anterior: a carta aprovada de 16×16 a 2× (a do herói é a mesma de retratos.js; a dos companheiros, a de arte-teste.js);
   - candidata: o padrão novo, "<nome>-c32" de cartas-teste.js, a 1×.
   A carta do herói e a dos companheiros (Morel, Odette e Yara) ficam em 32 px. Na vez do herói, o jogo amplia a carta
   1,12× (.carta.foco); aqui, só neste teste, o nicho do retrato (a moldura e o rosto) desfaz a ampliação e fica em 36 px
   com o rosto em 32 px exatos, alinhado ao pixel inteiro da tela (sem o meio pixel), enquanto o resto da carta continua
   ampliado. Usa as propriedades `scale` e `translate`, que não brigam com as animações do jogo (que usam `transform`).
   A fogueira, o topo, o Inventário e os retratos grandes não mudam. */
"use strict";

(() => {
  const V = (window.CARTAS && window.CARTAS.versao) || "candidata";
  const peca = (n) => (V === "anterior" ? [`${n}-carta`, 2] : [`${n}-c32`, 1]);
  const COMP = { morel: "morel", odete: "odette", yara: "yara" };
  const srcs = {};
  Object.keys(COMP).forEach((id) => { srcs[Sprites.url(id)] = id; });
  const classe = () => (App.estado && App.estado.heroi && App.estado.heroi.classe) || "guerreiro";
  function trocar(i, n) {
    const [p, e] = peca(n);
    i.src = ArteTeste.url(p, e); i.srcset = `${ArteTeste.url(p, 2 * e)} 2x`;
    i.width = i.height = 32; i.style.width = i.style.height = "32px";
    i.classList.add("arte-teste", "carta-teste");
  }
  function vestir() {
    document.querySelectorAll(".carta.heroi .icone img:not(.carta-teste)").forEach((i) => trocar(i, classe()));
    document.querySelectorAll(".carta:not(.heroi) .icone img:not(.carta-teste)").forEach((i) => {
      const id = srcs[i.getAttribute("src")]; if (id) trocar(i, COMP[id]);
    });
  }
  // o nicho do herói em foco: desfaz a ampliação e alinha ao pixel inteiro
  const ESCALA = 1.12;
  function alinhar() {
    document.querySelectorAll(".carta.heroi .icone").forEach((ic) => {
      const foco = ic.closest(".carta").classList.contains("foco");
      ic.style.translate = "";
      ic.style.scale = foco ? String(1 / ESCALA) : "";
      if (!foco) return;
      const r = ic.getBoundingClientRect();
      ic.style.translate = `${(Math.round(r.x) - r.x) / ESCALA}px ${(Math.round(r.y) - r.y) / ESCALA}px`;
    });
  }
  let espera = null;
  const depois = () => { clearTimeout(espera); espera = setTimeout(alinhar, 320); };   // depois da transição da carta (.25s)
  document.head.insertAdjacentHTML("beforeend", "<style>img.carta-teste { image-rendering: pixelated; }</style>");
  new MutationObserver((ms) => {
    vestir();
    if (ms.some((m) => m.type === "attributes" && m.target.classList && m.target.classList.contains("carta"))) { alinhar(); depois(); }
  }).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ["class"] });
  window.addEventListener("resize", depois);
  vestir(); alinhar(); depois();
})();
