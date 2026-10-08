/* Sprites em pixel art desenhados em código: cada sprite é uma grade de letras (paleta abaixo).
   Renderizados uma vez em canvas e reaproveitados como imagens nítidas (image-rendering: pixelated). */
"use strict";

const Sprites = (() => {
  const PALETA = {
    k: "#0d0b0a", K: "#2a2420", d: "#4a4038", g: "#8a8070", G: "#c0b8a8", w: "#f1e4c4", W: "#ffffff",
    r: "#b3262b", R: "#e2574c", D: "#6e0d0d", o: "#e0782f", O: "#ffb35c", y: "#f2c94c", Y: "#fff3a0",
    b: "#8a5a2c", B: "#5a3a1c", n: "#c08a50", p: "#e8a0a0", u: "#3d63c9", U: "#7fb0ff", v: "#1c2a6b",
    e: "#4f9a5b", E: "#8fbf6a", f: "#1f4a25", m: "#8e6fd8", M: "#c8b0ff", s: "#3a3128", c: "#d4af37",
    C: "#8a6a14", t: "#2e5f63", T: "#74c4c9", h: "#f0c8a0", H: "#c89070", x: "#5a2a6e",
  };

  const S = SPRITES_GRADES;  // os desenhos moram em sprites-dados.js

  const cache = {};
  function canvas(nome) {
    if (cache[nome]) return cache[nome];
    const grade = S[nome];
    if (!grade) return null;
    const c = document.createElement("canvas");
    c.width = grade[0].length; c.height = grade.length;
    const ctx = c.getContext("2d");
    grade.forEach((linha, y) => {
      for (let x = 0; x < linha.length; x++) {
        const cor = PALETA[linha[x]];
        if (cor) { ctx.fillStyle = cor; ctx.fillRect(x, y, 1, 1); }
      }
    });
    cache[nome] = c;
    return c;
  }
  const urls = {};
  function url(nome) {
    if (!urls[nome]) { const c = canvas(nome); urls[nome] = c ? c.toDataURL() : ""; }
    return urls[nome];
  }
  /** HTML de um sprite. escala: tamanho em px de cada pixel. */
  function img(nome, escala = 2, classe = "") {
    return `<img class="sprite ${classe}" src="${url(nome)}" width="${16 * escala}" height="${16 * escala}" style="--s:${16 * escala}" alt="" draggable="false">`;
  }
  return { img, url, canvas, existe: (n) => !!S[n], PALETA };
})();
