/* Experimento de resolução: veste o jogo de verdade com as amostras de resolucao-teste.js, só para as fotografias
   (fotografar_resolucao.mjs põe este arquivo na página depois de abrir um cenário; o jogo não o carrega).
   window.RESOLUCAO = { itens: "32" | "64", morel: "40" | "80" } escolhe a versão.
   - Os itens: a <img> do martelo e a da Pena de Fênix (o sprite "chama" dentro de um espaço de item, .slot-px) viram a
     amostra da resolução pedida, no tamanho em que o jogo a mostra; a de 64×64 num espaço de 32 px é reduzida pelo
     navegador pixel a pixel (sem suavizar), que é o custo que o experimento quer ver.
   - O Morel ocupa o lugar do retrato do herói (não há ficha de companheiro): o busto da ficha (80 px; 64 em janela
     baixa, pelo mesmo <picture> do jogo), a cabeça do topo (48 px) e a carta da luta (32 px). 40: o aprovado ampliado
     2×; 80: o de 80×80 a 1×, com os recortes e a carta própria de 32×32.
   - R.carta: outra peça para a carta (a anterior, a nova, a redução do 40), sempre em 32 px.
   - R.inteiro: na vez do herói o jogo amplia a carta inteira 1,12× (.carta.foco), e o rosto de 32 px vira 35,84 px,
     com pixels de espessuras desiguais; com R.inteiro, só neste teste, o rosto desfaz essa ampliação e fica em 32 px
     inteiros, centrado no nicho, enquanto a moldura, o nome e as barras continuam ampliados. Os companheiros não passam
     por isso: o foco é só da carta do herói.
   - R.comp: a peça da carta do Morel quando ele é companheiro (32 px, sem foco). */
"use strict";

(() => {
  const R = window.RESOLUCAO || { itens: "32", morel: "40" };
  const N = R.itens === "64" ? 64 : 32;
  const AMOSTRA = { [Sprites.url("martelo")]: "martelo", [Sprites.url("chama")]: "pena" };
  const pixel = "image-rendering: pixelated;";
  function item(i) {
    const nome = AMOSTRA[i.getAttribute("src")];
    if (!nome || !i.closest(".slot-px")) return;
    const lado = i.width || parseInt(i.getAttribute("width"), 10) || 32, e = Math.max(1, Math.round(lado / N));
    i.src = ArteTeste.url(`${nome}-${N}`, e);
    i.srcset = `${ArteTeste.url(`${nome}-${N}`, 2 * e)} 2x`;
    i.width = i.height = lado;
    i.classList.add("arte-teste");
  }
  const oitenta = R.morel === "80";
  const peca = (papel) => (oitenta ? { busto: ["morel-80", 1], baixo: ["morel-80-baixo", 1], cabeca: ["morel-80-cabeca", 1], carta: ["morel-80-carta", 1] }
    : { busto: ["morel", 2], baixo: ["morel-busto-baixo", 2], cabeca: ["morel-cabeca", 2], carta: ["morel-carta", 2] })[papel];
  const um = (papel, cl, alt = "") => {
    let [p, e] = peca(papel);
    if (papel === "carta" && R.carta) { p = R.carta; e = 32 / ArteTeste.PECAS[p].grade.length; }
    return ArteTeste.img(p, e, cl, alt);
  };
  function companheiro(i) {   // a carta do Morel companheiro: o sprite dele (32 px) vira a peça pedida, no mesmo tamanho
    if (!R.comp || i.getAttribute("src") !== Sprites.url("morel") || !i.closest(".carta")) return;
    const n = ArteTeste.PECAS[R.comp].grade.length, e = 32 / n;
    i.src = ArteTeste.url(R.comp, e); i.srcset = `${ArteTeste.url(R.comp, 2 * e)} 2x`; i.width = i.height = 32;
    i.classList.add("arte-teste");
  }
  function vestir() {
    document.querySelectorAll("img:not(.arte-teste)").forEach((i) => { item(i); companheiro(i); });
    document.querySelectorAll("#heroi .retrato-grande").forEach((r) => {
      if (r.querySelector(".candidato")) return;
      const [b, eb] = peca("baixo");
      r.innerHTML = `<picture class="desenho candidato"><source media="(max-height: 800px)" srcset="${ArteTeste.url(b, eb)}, ${ArteTeste.url(b, 2 * eb)} 2x">` +
        um("busto", "original") + "</picture>";
    });
    document.querySelectorAll(".hud-retrato img:not(.arte-teste)").forEach((i) => { i.outerHTML = um("cabeca", "sprite desenho", i.alt); });
    document.querySelectorAll(".carta.heroi .icone img:not(.arte-teste)").forEach((i) => { i.outerHTML = um("carta", "sprite desenho", i.alt); });
  }
  document.head.insertAdjacentHTML("beforeend", `<style>img.arte-teste { ${pixel} }` +
    (R.inteiro ? ".carta.foco .icone img.arte-teste { transform: scale(calc(1 / 1.12)); }" : "") + "</style>");
  new MutationObserver(vestir).observe(document.body, { childList: true, subtree: true });
  vestir();
})();
