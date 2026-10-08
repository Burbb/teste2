/* Sprites em pixel art desenhados em código: cada sprite é uma grade de letras (paleta abaixo).
   Renderizados uma vez em canvas e reaproveitados como imagens nítidas (image-rendering: pixelated).
   Daqui saem também os materiais da interface (pedra, pergaminho, pontilhado, molduras), na mesma paleta
   indexada dos sprites: publicar() os põe no :root como variáveis CSS. */
"use strict";

const Sprites = (() => {
  const PALETA = {
    k: "#0d0b0a", K: "#2a2420", d: "#4a4038", g: "#8a8070", G: "#c0b8a8", w: "#f1e4c4", W: "#ffffff",
    r: "#b3262b", R: "#e2574c", D: "#6e0d0d", o: "#e0782f", O: "#ffb35c", y: "#f2c94c", Y: "#fff3a0",
    b: "#8a5a2c", B: "#5a3a1c", n: "#c08a50", p: "#e8a0a0", u: "#3d63c9", U: "#7fb0ff", v: "#1c2a6b",
    e: "#4f9a5b", E: "#8fbf6a", f: "#1f4a25", m: "#8e6fd8", M: "#c8b0ff", s: "#3a3128", c: "#d4af37",
    C: "#8a6a14", t: "#2e5f63", T: "#74c4c9", h: "#f0c8a0", H: "#c89070", x: "#5a2a6e",
    z: "#17120f", q: "#211a14", Q: "#2b2219",  // fundos da interface: pedra funda, pergaminho escuro e o grão dele
  };
  /** Limiar de Bayer 4×4 (0 a 15): o pontilhado ordenado de toda a arte. */
  const BAYER4 = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
  /** As molduras em 9-slice (sprites-dados.js), publicadas como --<nome>. */
  const MOLDURAS = ["mold", "janela", "janela_magico", "janela_raro", "janela_lendario"];

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
  /** O sprite com 1 texel de sombra preta para baixo e para a direita: o contorno "crocante" de um ícone sobre placa. */
  function comSombra(nome) {
    const chave = nome + ":sombra";
    if (cache[chave]) return cache[chave];
    const base = canvas(nome);
    if (!base) return null;
    const c = document.createElement("canvas");
    c.width = base.width + 1; c.height = base.height + 1;
    const x = c.getContext("2d");
    x.drawImage(base, 1, 1);
    x.globalCompositeOperation = "source-in"; x.fillStyle = PALETA.k; x.fillRect(0, 0, c.width, c.height);
    x.globalCompositeOperation = "source-over"; x.drawImage(base, 0, 0);
    return (cache[chave] = c);
  }
  const urls = {};
  function url(nome, sombra = false) {
    const chave = sombra ? nome + ":sombra" : nome;
    if (!urls[chave]) { const c = sombra ? comSombra(nome) : canvas(nome); urls[chave] = c ? c.toDataURL() : ""; }
    return urls[chave];
  }
  /** HTML de um sprite. escala: tamanho em px de cada pixel. Com sombra, a imagem tem 1 texel a mais de cada lado. */
  function img(nome, escala = 2, classe = "", { sombra = false } = {}) {
    const lado = (sombra ? 17 : 16) * escala;
    return `<img class="sprite ${classe}" src="${url(nome, sombra)}" width="${lado}" height="${lado}" style="--s:${lado}" alt="" draggable="false">`;
  }

  // ------------------------------------------------------------ materiais da interface
  const tiles = {};
  /** Um ladrilho pequeno pintado texel a texel, só com cores da PALETA: letra fora dela é erro, na hora. */
  function tile(chave, w, h, pintar) {
    if (tiles[chave]) return tiles[chave];
    const c = document.createElement("canvas");
    c.width = w; c.height = h;
    const x = c.getContext("2d");
    pintar((px, py, letra) => {
      const cor = PALETA[letra];
      if (!cor) throw new Error(`cor fora da paleta: ${letra}`);
      x.fillStyle = cor; x.fillRect(px, py, 1, 1);
    });
    return (tiles[chave] = c.toDataURL());
  }
  /** nivel/16 dos texels de um bloco 4×4 na cor (o resto transparente): véus de 25%, 50% e 75%. */
  function pontilhado(letra, nivel) {
    return tile(`pt${letra}${nivel}`, 4, 4, (set) => {
      for (let i = 0; i < 16; i++) if (BAYER4[i] < nivel) set(i & 3, i >> 2, letra);
    });
  }
  /** Uma cor que some em n texels pelo limiar de Bayer: a luz no topo de um painel, a sombra sob a barra do topo. */
  function rampa(letra, n, sentido = "desce") {
    const vertical = sentido === "desce" || sentido === "sobe", invertida = sentido === "sobe" || sentido === "esquerda";
    return tile(`rp${letra}${n}${sentido}`, vertical ? 4 : n, vertical ? n : 4, (set) => {
      for (let i = 0; i < n; i++) {
        const nivel = Math.round(16 * (1 - (i + 0.5) / n)), p = invertida ? n - 1 - i : i;
        for (let j = 0; j < 4; j++) {
          const [x, y] = vertical ? [j, p] : [p, j];
          if (BAYER4[(y & 3) * 4 + (x & 3)] < nivel) set(x, y, letra);
        }
      }
    });
  }
  /** Pedra (ou pergaminho) granulada que emenda nas bordas: ruído de valor periódico em três tons. O claro e o
   *  escuro vão para o ladrilho; o do meio fica transparente, porque é a cor de fundo do próprio material. */
  function pedra([claro, escuro], tam, semente, celula = 4, faixa = 0.3) {
    if (tam % celula) throw new Error("a célula da pedra precisa dividir o ladrilho (senão aparece a emenda)");
    return tile(`pd${claro}${escuro}${tam}.${semente}.${celula}.${faixa}`, tam, tam, (set) => {
      const per = tam / celula, suave = (t) => t * t * (3 - 2 * t);
      const h = (i, j) => { const v = Math.sin((i % per) * 127.1 + (j % per) * 311.7 + semente * 74.7) * 43758.5453; return v - Math.floor(v); };
      for (let y = 0; y < tam; y++) for (let x = 0; x < tam; x++) {
        const gx = x / celula, gy = y / celula, i = Math.floor(gx), j = Math.floor(gy), ux = suave(gx - i), uy = suave(gy - j);
        const a = h(i, j), b = h(i + 1, j), c = h(i, j + 1), d = h(i + 1, j + 1);
        const n = a + (b - a) * ux + (c - a) * uy + (a - b - c + d) * ux * uy + (BAYER4[(y & 3) * 4 + (x & 3)] / 16 - 0.5) * 0.15;
        if (n > 0.5 + faixa) set(x, y, claro); else if (n < 0.5 - faixa) set(x, y, escuro);
      }
    });
  }

  /** Unidade de pixel da arte: um número inteiro de pixels do aparelho (com zoom de 125% ou 150% no sistema, 1px de
   *  CSS não é 1 pixel de verdade, e a pixel art fica torta). Um texel da interface (--P) vale dois disso. */
  function unidade() {
    const dpr = window.devicePixelRatio || 1;
    document.documentElement.style.setProperty("--px", Math.max(1, Math.round(dpr)) / dpr + "px");
  }
  let publicado = false;
  /** Põe no :root a unidade de pixel, a paleta (--p-<letra>), as texturas, os pontilhados, as molduras e os sprites
   *  que o CSS usa. Uma vez só: cada troca no :root recalcula o estilo da página inteira. */
  function publicar() {
    unidade();
    if (publicado) return;
    publicado = true;
    window.addEventListener("resize", unidade);
    const raiz = document.documentElement.style, u = (d) => `url(${d})`;
    for (const [letra, cor] of Object.entries(PALETA)) raiz.setProperty(`--p-${letra}`, cor);
    // Grão fino e esparso (só os extremos do ruído viram pinta): granito, e não camuflagem.
    raiz.setProperty("--tx-pedra", u(pedra(["s", "z"], 64, 11, 4, 0.32)));   // painéis (fundo K)
    raiz.setProperty("--tx-perg", u(pedra(["Q", "z"], 64, 23, 4, 0.36)));    // cena e janelas: quase liso, atrás da prosa
    raiz.setProperty("--tx-placa", u(pedra(["d", "K"], 32, 3)));             // placas (fundo s)
    raiz.setProperty("--tx-funda", u(pedra(["K", "k"], 32, 5)));             // nichos (fundo z)
    raiz.setProperty("--tx-fundo", u(pedra(["K", "k"], 128, 7, 4, 0.32)));   // a página (fundo z)
    for (const n of MOLDURAS) raiz.setProperty(`--${n}`, u(url(n)));
    for (const n of [4, 8, 12]) raiz.setProperty(`--veu-${n}`, u(pontilhado("k", n)));
    raiz.setProperty("--luz-topo", u(rampa("s", 6)));
    raiz.setProperty("--sombra-desce", u(rampa("k", 4)));
    for (const n of ["caveira", "cadeado"]) raiz.setProperty(`--${n}`, u(url(n)));
  }

  return { img, url, canvas, existe: (n) => !!S[n], PALETA, BAYER4, MOLDURAS, tex: { tile, pontilhado, rampa, pedra }, publicar };
})();
