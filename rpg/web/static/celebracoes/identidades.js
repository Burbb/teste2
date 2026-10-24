/* Identidades: a identidade de fogo do Piromante (o piloto aprovado da etapa 2, 1.201.0) e o contorno das letras, que
   as identidades das outras especializações também usam (especializacoes.js). O nome em ouro quente e laranja, com a
   borda incandescente; chamas desenhadas à mão nascem do topo das letras e sobem; brasas. O corpo das letras fica parado
   e legível; com o movimento reduzido, um quadro parado das chamas. */
"use strict";

const Identidades = (() => {
  // a paleta dos raios (do Relicário) e do estouro (do Estouro), do mais claro ao mais escuro
  const PAL = { fogo: ["W", "Y", "O", "o", "r"] };
  // os estilhaços do Estouro na cor da identidade
  const CACOS = { fogo: ["Y", "O", "o", "r", "D"] };

  // ---------------------------------------------------------------- desenhos à mão (grades; "a" a borda, "b" o miolo)
  const CHAMAS = [
    ["...a...", "...a...", "..aba..", "..aba..", ".abba..", ".abbba.", "abbbbba", "abbbbba", ".aaaaa."],
    ["..a..", "..a..", ".aba.", ".abba", "abbba", "abbba", ".aaa."],
    ["..a..", ".aba.", ".aba.", "abbba", ".aaa."],
    [".a.", "aba", "aba", ".a."],
    ["a", "a"],
  ];
  const COR_CHAMA = [["Y", "W"], ["O", "Y"], ["O", "Y"], ["o", "O"], ["r", "o"]];

  function grade(p, g, ox, oy, ca, cb) {
    for (let y = 0; y < g.length; y++) for (let x = 0; x < g[y].length; x++) {
      const ch = g[y][x];
      if (ch === "a") p.por(ox + x, oy + y, ca); else if (ch === "b") p.por(ox + x, oy + y, cb);
    }
  }

  // ---------------------------------------------------------------- o contorno das letras
  /** Os pontos do contorno das letras de `el` em texels: os topos (onde a tinta começa, vindo de cima) e as bases (onde
   *  ela acaba, indo para baixo). O texto é desenhado num canvas com a mesma fonte e a linha de base do navegador. */
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
    const fa = m.fontBoundingBoxAscent, fd = m.fontBoundingBoxDescent, asc = m.actualBoundingBoxAscent;
    const base = 4 + (tr.height - (fa + fd)) / 2 + fa;
    x.fillText(texto, 4 + (tr.width - m.width) / 2, base);
    const d = x.getImageData(0, 0, c.width, c.height).data, passo = Math.max(1, r.width / Math.max(1, p.t(r.width)));
    const tinta = (px, py) => px >= 0 && py >= 0 && px < c.width && py < c.height && d[(Math.round(py) * c.width + Math.round(px)) * 4 + 3] > 120;
    const topos = [], bases = [], lados = [];
    for (let px = 0; px < c.width; px += passo) for (let py = passo; py < c.height - passo; py += passo) {
      if (!tinta(px, py)) continue;
      const ponto = { x: p.tx(tr.left - 4 + px), y: p.ty(tr.top - 4 + py), alto: py < base - asc * 0.55 };
      if (!tinta(px, py - passo)) topos.push(ponto);
      if (!tinta(px, py + passo)) bases.push(ponto);
      if (!tinta(px - passo, py) || !tinta(px + passo, py)) lados.push(ponto);
    }
    return { topos, bases, lados, todos: topos.concat(bases, lados) };
  }
  const sorteio = (lista) => lista[Math.floor(Math.random() * lista.length)];

  // ---------------------------------------------------------------- o que vale para todas
  /** O poço escuro logo atrás do nome e, na borda dele, um brilho baixo na cor da identidade. */
  function fundoDoNome(p, r, cores, q, parado) {
    const vis = parado ? 6 : 5 + ((q >> 1) % 2);
    FX.halo(p, { cx: r.x, cy: r.y + Math.round(r.ry * 0.2), r: Math.round(r.rx * 1.15), achata: 0.5, pal: cores, vis });
    FX.poco(p, { cx: r.x, cy: r.y, rx: r.rx + 18, ry: r.ry + 16, forca: 16 });
  }
  /** Um enxame simples de partículas desenhadas (a idade escolhe o quadro). */
  function enxame() {
    const lista = [];
    return {
      lista,
      soltar(n, gerar) { for (let i = 0; i < n; i++) lista.push({ idade: 0, ...gerar(i) }); },
      passo() {
        for (let i = lista.length - 1; i >= 0; i--) {
          const s = lista[i];
          if (++s.idade > s.vida) { lista.splice(i, 1); continue; }
          if (s.mover) s.mover(s); else { s.x += s.vx || 0; s.y += s.vy || 0; s.vy = (s.vy || 0) + (s.g || 0); }
        }
      },
      /** Para o movimento reduzido: as partículas em idades variadas, paradas. */
      congelar() { for (const s of lista) { const k = Math.floor(Math.random() * s.vida); for (let i = 0; i < k; i++) { s.idade++; if (s.mover) s.mover(s); else { s.x += s.vx || 0; s.y += s.vy || 0; } } } },
    };
  }

  // ---------------------------------------------------------------- o fogo
  const COMPORTAMENTO = {
    // FOGO: chamas do topo das letras subindo; brasas
    fogo: {
      quadro({ p, r, c, q, t, parado, ex }) {
        fundoDoNome(p, r, ["o", "r", "D"], q, parado);
        if (!parado && c.topos.length) {
          ex.soltar(q < 9 ? 6 : 3, () => { const o = sorteio(Math.random() < 0.7 && c.topos.some((x) => x.alto) ? c.topos.filter((x) => x.alto) : c.topos);
            return { tipo: "chama", x: o.x, y: o.y + 2, vy: -0.55, vida: Math.round(FX.aleatorio(8, 13)), fase: Math.random() * 6 }; });
        }
        if (!parado) {
          if (q % 2 === 0) ex.soltar(1, () => ({ tipo: "brasa", x: r.x + Math.round(FX.aleatorio(-r.rx * 1.1, r.rx * 1.1)), y: r.y + r.ry, vx: FX.aleatorio(-0.3, 0.3), vy: FX.aleatorio(-1.3, -0.6), vida: Math.round(FX.aleatorio(14, 24)) }));
        }
      },
      desenhar(p, s, parado) {
        if (s.tipo === "brasa") { const k = Math.min(4, Math.floor((s.idade / (s.vida + 1)) * 5)); p.por(Math.round(s.x), Math.round(s.y), FX.cor(["Y", "O", "o", "r", "D"][k])); return; }
        const k = Math.min(CHAMAS.length - 1, Math.floor((s.idade / (s.vida + 1)) * CHAMAS.length)), g = CHAMAS[k];
        const [ca, cb] = COR_CHAMA[k].map(FX.cor), bal = parado ? 0 : Math.round(Math.sin(s.idade * 0.9 + s.fase) * 0.6);
        grade(p, g, Math.round(s.x) - (g[0].length >> 1) + bal, Math.round(s.y) - g.length + 1, ca, cb);
      },
      parado: 30,
    },
  };

  /** A identidade para o nome `el`: a apresentação chama `quadro(p, t, q, parado)` depois dos raios ou do estouro. */
  function criar(id, el) {
    const comp = COMPORTAMENTO[id];
    if (!comp) return null;
    const ex = enxame(), dados = {};
    let c = null, congelado = false;
    return {
      id, pal: PAL[id], cacos: CACOS[id],
      /** Os raios tremulam um nível (só o fogo). */
      treme: (q) => (id === "fogo" && (q * 7) % 5 === 0 ? 2 : 0),
      quadro(p, t, q, parado) {
        const r = p.de(el);
        // o contorno depois do carimbo do nome (no carimbo ele está ampliado) e de novo a cada ~2 s
        if (parado || (t >= 300 && (!c || !c.todos.length || q % 30 === 0))) c = contorno(el, p);
        const cont = c || { topos: [], bases: [], lados: [], todos: [] };
        if (parado && !congelado && cont.todos.length) {  // o quadro parado: soltar e envelhecer as partículas
          congelado = true;
          for (let k = 0; k < 40; k++) comp.quadro({ p: { ...p, por() {}, buf: new Uint32Array(0) }, r, c: cont, q: k, t: 600 + k * FX.QUADRO, parado: false, ex, dados: {} });
          while (ex.lista.length > comp.parado) ex.lista.splice(Math.floor(Math.random() * ex.lista.length), 1);
          ex.congelar();
        }
        comp.quadro({ p, r, c: cont, q, t, parado, ex, dados });
        if (!parado) ex.passo();
        for (const s of ex.lista) comp.desenhar(p, s, parado);
      },
    };
  }

  const faixas = (a, b, c) => `background: linear-gradient(${a} 0 34%, ${b} 34% 66%, ${c} 66% 100%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; text-shadow: none !important;`;
  const borda = (l, t, b) => `drop-shadow(2px 0 0 ${l}) drop-shadow(-2px 0 0 ${l}) drop-shadow(0 -2px 0 ${t}) drop-shadow(0 2px 0 ${b}) drop-shadow(0 5px 0 #08090a)`;
  const css = `
  /* os nomes das especializações: faixas duras, a borda da identidade e a sombra escura */
  .idn-fogo { ${faixas("#fff3a0", "#ffb35c", "#f0882f")} filter: ${borda("#b3262b", "#e0782f", "#6e0d0d")}; animation: idn-fogo 0.53s steps(1) infinite; }
  @keyframes idn-fogo { 50% { filter: ${borda("#e0782f", "#ffb35c", "#6e0d0d")}; } }
  .idn-sobre-fogo { color: #ffb35c !important; } .idn-sobre-luz { color: #f1e4c4 !important; } .idn-sobre-sangue { color: #e2574c !important; }
  .idn-sobre-folhas { color: #8fbf6a !important; } .idn-sobre-sombra { color: #a89878 !important; } .idn-sobre-almas { color: #74c4c9 !important; }
  @media (prefers-reduced-motion: reduce) { .idn-fogo { animation: none; } }`;
  document.head.insertAdjacentHTML("beforeend", `<style id="estilo-identidades">${css}</style>`);

  return { PAL, CACOS, criar, contorno };
})();
