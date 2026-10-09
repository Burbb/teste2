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
    N: "#08090a", A: "#121110",                 // o fundo da página e o dos painéis, quase pretos
    j: "#48311f", J: "#6b4b31", a: "#d9a05c",  // o bronze dos quadros (sombra e luz) e o ouro velho dos espaços de item
  };
  /** Limiar de Bayer 4×4 (0 a 15): o pontilhado ordenado de toda a arte. */
  const BAYER4 = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
  const S = SPRITES_GRADES;  // os desenhos moram em sprites-dados.js
  /** As molduras em 9-slice (sprites-dados.js), publicadas como --anel-k, --placa-C, --janela-y... */
  const MOLDURAS = Object.keys(S).filter((n) => /^(anel|placa|janela|quadro|retrato)_\w$/.test(n));

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
  /** Uma cor que some em n texels: a luz no topo de um painel, a sombra sob a barra do topo. A i texels do lado denso
   *  acendem os k de menor limiar de uma linha do Bayer escolhida por i: a cobertura só diminui (4, 3, 2, 2, 1, 0 em
   *  seis), e as direções opostas são o espelho uma da outra. */
  function rampa(letra, n, sentido = "desce") {
    const vertical = sentido === "desce" || sentido === "sobe", invertida = sentido === "sobe" || sentido === "esquerda";
    return tile(`rp${letra}${n}${sentido}`, vertical ? 4 : n, vertical ? n : 4, (set) => {
      for (let i = 0; i < n; i++) {
        const k = Math.round(4 * (1 - (i + 0.5) / n)), linha = BAYER4.slice((i & 3) * 4, (i & 3) * 4 + 4);
        if (k <= 0) continue;
        const corte = [...linha].sort((a, b) => a - b)[k - 1], p = invertida ? n - 1 - i : i;
        for (let j = 0; j < 4; j++) if (linha[j] <= corte) set(...(vertical ? [j, p] : [p, j]), letra);
      }
    });
  }
  /** Ruído de valor periódico, de 0 a 1, liso dentro de células de `celula` texels: o ladrilho emenda nas bordas. */
  function ruido(tam, semente, celula) {
    if (tam % celula) throw new Error("a célula do ruído precisa dividir o ladrilho (senão aparece a emenda)");
    const per = tam / celula, suave = (t) => t * t * (3 - 2 * t);
    const h = (i, j) => { const v = Math.sin((i % per) * 127.1 + (j % per) * 311.7 + semente * 74.7) * 43758.5453; return v - Math.floor(v); };
    return (x, y) => {
      const gx = x / celula, gy = y / celula, i = Math.floor(gx), j = Math.floor(gy), ux = suave(gx - i), uy = suave(gy - j);
      const a = h(i, j), b = h(i + 1, j), c = h(i, j + 1), d = h(i + 1, j + 1);
      return a + (b - a) * ux + (c - a) * uy + (a - b - c + d) * ux * uy;
    };
  }
  /** Pedra (ou pergaminho) granulada: o ruído em três tons. O claro e o escuro vão para o ladrilho; o do meio fica
   *  transparente, porque é a cor de fundo do próprio material. */
  function pedra([claro, escuro], tam, semente, celula = 4, faixa = 0.3) {
    const r = ruido(tam, semente, celula);
    return tile(`pd${claro}${escuro}${tam}.${semente}.${celula}.${faixa}`, tam, tam, (set) => {
      for (let y = 0; y < tam; y++) for (let x = 0; x < tam; x++) {
        const n = r(x, y) + (BAYER4[(y & 3) * 4 + (x & 3)] / 16 - 0.5) * 0.15;
        if (n > 0.5 + faixa) set(x, y, claro); else if (n < 0.5 - faixa) set(x, y, escuro);
      }
    });
  }
  /** Fuligem: manchas grandes e suaves de uma cor, pontilhadas pelo Bayer, com no máximo `forca` de cobertura. É o
   *  esfumado da pixel art: a pedra escurece em nuvens, sem gradiente nem faixa. */
  function fumo(letra, tam, semente, celula = 32, forca = 0.5) {
    const grosso = ruido(tam, semente, celula), fino = ruido(tam, semente, celula / 2);
    return tile(`fm${letra}${tam}.${semente}.${celula}.${forca}`, tam, tam, (set) => {
      for (let y = 0; y < tam; y++) for (let x = 0; x < tam; x++) {
        const n = grosso(x, y) * 0.7 + fino(x, y) * 0.3, t = Math.min(1, Math.max(0, (n - 0.3) / 0.55)) * forca;
        if (BAYER4[(y & 3) * 4 + (x & 3)] < Math.floor(t * 16)) set(x, y, letra);
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
    raiz.setProperty("--tx-pedra", u(pedra(["z", "k"], 64, 11, 4, 0.4)));    // painéis (fundo A): grão quase invisível
    raiz.setProperty("--tx-perg", u(pedra(["Q", "z"], 64, 23, 4, 0.38)));    // cena: pergaminho manchado, atrás da prosa (fundo q)
    raiz.setProperty("--tx-placa", u(pedra(["d", "K"], 32, 3)));             // placas (fundo s)
    raiz.setProperty("--tx-funda", u(pedra(["K", "k"], 32, 5)));             // nichos (fundo z)
    raiz.setProperty("--tx-fundo", u(pedra(["K", "k"], 128, 7, 4, 0.44)));   // a página (fundo z)
    // Fuligem por cima da pedra: os painéis afundam na sombra e a luz fica na cena; a página, mais escura ainda.
    raiz.setProperty("--fumo-painel", u(fumo("k", 128, 5, 32, 0.5)));
    raiz.setProperty("--fumo-fundo", u(fumo("k", 128, 9, 32, 0.75)));
    for (const n of MOLDURAS) raiz.setProperty(`--${n.replace("_", "-")}`, u(url(n)));
    for (const n of [4, 8, 12]) raiz.setProperty(`--veu-${n}`, u(pontilhado("k", n)));
    // O relevo dos painéis: a luz vem de cima e da esquerda; a direita e o pé ficam na sombra.
    raiz.setProperty("--luz-topo", u(rampa("s", 6)));
    raiz.setProperty("--luz-esq", u(rampa("s", 4, "direita")));
    raiz.setProperty("--sombra-dir", u(rampa("k", 4, "esquerda")));
    raiz.setProperty("--sombra-baixo", u(rampa("k", 4, "sobe")));
    raiz.setProperty("--sombra-desce", u(rampa("k", 4)));
    for (const n of ["caveira", "cadeado", "lanterna", "estrelinha", "fio_cabeca", "fim_cabeca", "fio", "ponta"]) raiz.setProperty(`--${n.replace("_", "-")}`, u(url(n)));
  }

  return { img, url, canvas, existe: (n) => !!S[n], PALETA, BAYER4, MOLDURAS, tex: { tile, pontilhado, rampa, pedra, fumo }, publicar };
})();
