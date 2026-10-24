/* PROTÓTIPO (24/10/2026; nada no jogo): IDENTIDADE da especialização, separada da APRESENTAÇÃO. A apresentação
   (Relicário ou Estouro) faz a composição e a entrada; a identidade diz as cores e o comportamento visual da
   especialização. Piloto só com o Piromante (fogo); as outras especializações ficam para depois da avaliação.
   - o nome em ouro quente e laranja, em faixas duras (sem degradê suave), com a borda incandescente (um contorno
     vermelho e brasa que pisca em dois tons) e uma sombra escura para o contraste;
   - chamas pequenas desenhadas à mão (grades de texto, em quatro idades) nascem do contorno de cima das letras e
     sobem pouco: o corpo das letras fica parado e legível, e as chamas não descem sobre a descrição nem os botões;
   - a paleta do fogo para o fundo (os raios, as brasas). Com o movimento reduzido, um quadro parado das chamas. */
"use strict";

const Identidade = (() => {
  const POR_ESPECIALIZACAO = { Piromante: "fogo" };  // a festa da especialização manda o nome (o motor não manda o id)
  const FOGO = { pal: ["W", "Y", "O", "o", "r"], brasas: ["Y", "O", "o", "r", "D"] };
  // As chamas, da mais nova à que se apaga ("b" o miolo claro, "a" a borda); desenhadas à mão, em texels.
  const CHAMAS = [
    ["...a...", "...a...", "..aba..", "..aba..", ".abba..", ".abbba.", "abbbbba", "abbbbba", ".aaaaa."],
    ["..a..", "..a..", ".aba.", ".abba", "abbba", "abbba", ".aaa."],
    ["..a..", ".aba.", ".aba.", "abbba", ".aaa."],
    [".a.", "aba", "aba", ".a."],
    ["a", "a"],
  ];
  const CORES = [["Y", "W"], ["O", "Y"], ["O", "Y"], ["o", "O"], ["r", "o"]];  // [borda, miolo] por idade

  const qual = (nomeEspecializacao) => POR_ESPECIALIZACAO[nomeEspecializacao] || null;

  /** Os pontos do contorno de cima das letras de `el` (em texels do palco): o texto desenhado num canvas com a mesma
   *  fonte e, em cada coluna de um texel, onde a tinta começa (e os topos de dentro das letras, como o da curva). */
  function contorno(el, p) {
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    const faixa = document.createRange(); faixa.selectNodeContents(el);
    const tr = faixa.getBoundingClientRect();
    const c = document.createElement("canvas");
    c.width = Math.ceil(tr.width) + 8; c.height = Math.ceil(tr.height) + 8;
    const x = c.getContext("2d");
    x.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    x.textBaseline = "alphabetic"; x.fillStyle = "#fff";
    const texto = el.textContent, m = x.measureText(texto);
    // a linha de base como o navegador põe: a meia entrelinha mais a subida da fonte (a métrica da fonte, não a da tinta)
    const fa = m.fontBoundingBoxAscent, fd = m.fontBoundingBoxDescent, asc = m.actualBoundingBoxAscent;
    const base = 4 + (tr.height - (fa + fd)) / 2 + fa;
    x.fillText(texto, 4 + (tr.width - m.width) / 2, base);
    const d = x.getImageData(0, 0, c.width, c.height).data, passo = Math.max(1, (r.width / Math.max(1, p.t(r.width))));
    const tinta = (px, py) => px >= 0 && py >= 0 && px < c.width && py < c.height && d[(Math.round(py) * c.width + Math.round(px)) * 4 + 3] > 120;
    const pontos = [];
    for (let px = 0; px < c.width; px += passo) for (let py = passo; py < c.height; py += passo)
      if (tinta(px, py) && !tinta(px, py - passo)) pontos.push({ x: p.tx(tr.left - 4 + px), y: p.ty(tr.top - 4 + py), alto: py < base - asc * 0.55 });
    return pontos;
  }

  /** As chamas: nascem nos pontos do contorno (mais nos topos das letras), sobem devagar balançando e envelhecem. */
  function chamas() {
    const lista = [];
    return {
      soltar(pontos, n) {
        if (!pontos.length) return;
        for (let i = 0; i < n; i++) {
          const altos = pontos.filter((q) => q.alto), de = altos.length && Math.random() < 0.7 ? altos : pontos;
          const q = de[Math.floor(Math.random() * de.length)];
          lista.push({ x: q.x, y: q.y + 2, vida: Math.round(FX.aleatorio(8, 13)), idade: 0, fase: Math.random() * 6 });
        }
      },
      passo() {
        for (let i = lista.length - 1; i >= 0; i--) {
          const f = lista[i];
          if (++f.idade > f.vida) { lista.splice(i, 1); continue; }
          f.y -= 0.55;
        }
      },
      /** `parado`: um quadro de chamas em idades variadas, para o movimento reduzido. */
      desenhar(p, parado = false) {
        for (const f of lista) {
          const k = Math.min(CHAMAS.length - 1, Math.floor((f.idade / (f.vida + 1)) * CHAMAS.length));
          const g = CHAMAS[k], [ca, cb] = CORES[k].map(FX.cor);
          const balanco = parado ? 0 : Math.round(Math.sin(f.idade * 0.9 + f.fase) * 0.6);
          const ox = Math.round(f.x) - (g[0].length >> 1) + balanco, oy = Math.round(f.y) - g.length + 1;
          for (let y = 0; y < g.length; y++) for (let x = 0; x < g[y].length; x++) {
            const ch = g[y][x];
            if (ch === "a") p.por(ox + x, oy + y, ca); else if (ch === "b") p.por(ox + x, oy + y, cb);
          }
        }
      },
      lista,
    };
  }

  /** O calor atrás do nome: um poço escuro logo atrás das letras (os raios ficam em volta; as letras e as chamas leem
   *  no escuro) e, na borda dele, um brilho baixo de brasa em pontilhado que tremula entre dois níveis. */
  function calor(p, el, q, parado) {
    const r = p.de(el), vis = parado ? 6 : 5 + ((q >> 1) % 2);
    FX.halo(p, { cx: r.x, cy: r.y + Math.round(r.ry * 0.2), r: Math.round(r.rx * 1.15), achata: 0.5, pal: ["o", "r", "D"], vis });
    FX.poco(p, { cx: r.x, cy: r.y, rx: r.rx + 18, ry: r.ry + 16, forca: 16 });
  }

  const css = `
  /* o nome do Piromante: ouro quente em faixas, borda incandescente, sombra para o contraste */
  .id-fogo { color: #ffd27a; background: linear-gradient(#fff3a0 0 34%, #ffb35c 34% 66%, #f0882f 66% 100%); -webkit-background-clip: text;
    background-clip: text; -webkit-text-fill-color: transparent; text-shadow: none !important;
    filter: drop-shadow(2px 0 0 #b3262b) drop-shadow(-2px 0 0 #b3262b) drop-shadow(0 -2px 0 #e0782f) drop-shadow(0 2px 0 #6e0d0d) drop-shadow(0 5px 0 #120604);
    animation: id-fogo-borda 0.53s steps(1) infinite; }
  @keyframes id-fogo-borda {
    50% { filter: drop-shadow(2px 0 0 #e0782f) drop-shadow(-2px 0 0 #b3262b) drop-shadow(0 -2px 0 #ffb35c) drop-shadow(0 2px 0 #6e0d0d) drop-shadow(0 5px 0 #120604); } }
  .id-fogo-sobre { color: #ffb35c !important; }
  @media (prefers-reduced-motion: reduce) { .id-fogo { animation: none; } }`;
  document.head.insertAdjacentHTML("beforeend", `<style id="estilo-identidade">${css}</style>`);

  return { qual, FOGO, contorno, chamas, calor };
})();
