/* PROTÓTIPO da etapa 2, segunda rodada, direção relicario5d (montado por auxiliares/montar_v2.py; nada no jogo). */
const IDENTIDADE_VARIANTE = "d";
/* PROTÓTIPO da etapa 2, segunda rodada (24/10/2026; nada no jogo): FX, os efeitos em pixel das celebrações.
   Um palco de baixa resolução (um canvas em texels de 3 px do aparelho, ampliado sem suavização) e as peças que as três
   direções compõem: raios que giram, feixes, halos, anéis de choque, colunas de luz, clarões e partículas desenhadas à
   mão (grades de texto, como os sprites do jogo). Cor só da paleta do jogo (Sprites.PALETA); degradê só por pontilhado
   ordenado (Sprites.pontilha) e por faixas de cor; movimento em quadros (15 por segundo), sem interpolação suave. */
"use strict";

const FX = (() => {
  const { PALETA, pontilha } = Sprites;
  const cache = {};
  /** "#rrggbb" (ou a letra da paleta) em ABGR, como o ImageData guarda. */
  function cor(c) {
    if (cache[c] !== undefined) return cache[c];
    const hex = c.length === 1 ? PALETA[c] : c;
    const v = parseInt(hex.slice(1), 16);
    return (cache[c] = ((255 << 24) | ((v & 255) << 16) | (v & 0xff00) | (v >> 16)) >>> 0);
  }
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const FPS = 15, QUADRO = 1000 / FPS;

  // As paletas, do miolo (mais claro) para a borda, todas da paleta do jogo.
  const PALETAS = {
    ouro: ["W", "Y", "y", "c", "C"], lendario: ["W", "Y", "O", "o", "r"], raro: ["W", "Y", "y", "c", "C"],
    magico: ["W", "M", "U", "u", "v"], comum: ["W", "w", "G", "g", "d"], sigilo: ["Y", "O", "R", "r", "D"],
    arcano: ["W", "M", "m", "x", "v"],
  };

  // ------------------------------------------------------------------ o palco
  /** Um canvas de baixa resolução cobrindo o `host` (fixo na tela inteira por padrão). */
  function palco(host, { z = 0, classe = "" } = {}) {
    const dpr = window.devicePixelRatio || 1, T = 3 * Math.max(1, Math.round(dpr));
    const W = Math.ceil((innerWidth * dpr) / T), H = Math.ceil((innerHeight * dpr) / T);
    const el = document.createElement("canvas");
    el.width = W; el.height = H;
    el.className = "fx-palco " + classe;
    el.setAttribute("aria-hidden", "true");
    el.style.cssText = `position:fixed;left:0;top:0;width:${(W * T) / dpr}px;height:${(H * T) / dpr}px;` +
      `image-rendering:pixelated;pointer-events:none;z-index:${z}`;
    host.prepend(el);
    const ctx = el.getContext("2d"), img = ctx.createImageData(W, H), buf = new Uint32Array(img.data.buffer);
    const p = {
      el, W, H, buf,
      /** O texel do ponto (x, y) da tela, em px de CSS. */
      tx: (x) => Math.round((x * dpr) / T), ty: (y) => Math.round((y * dpr) / T),
      /** O texel do meio de um elemento (e a meia largura e a meia altura dele, em texels). */
      de(elemento) {
        const r = elemento.getBoundingClientRect();
        return { x: p.tx(r.left + r.width / 2), y: p.ty(r.top + r.height / 2), rx: p.tx(r.width / 2), ry: p.ty(r.height / 2),
          topo: p.ty(r.top), base: p.ty(r.bottom), esq: p.tx(r.left), dir: p.tx(r.right) };
      },
      /** Quantos texels cabem em `px` de CSS. */
      t: (px) => Math.round((px * dpr) / T),
      por(x, y, c) { if (x >= 0 && y >= 0 && x < W && y < H) buf[y * W + x] = c; },
      limpar() { buf.fill(0); },
      mostrar() { ctx.putImageData(img, 0, 0); },
    };
    return p;
  }

  /** Roda `desenhar(t, quadro, parado)` a 15 quadros por segundo até `parar`. `pular(ms)` leva a linha do tempo até
   *  `ms` (o gesto que adianta a entrada). Com o movimento reduzido, um quadro só, em `parado` (a composição fica). */
  function animar(p, desenhar, { parado = 1500 } = {}) {
    let fim = false, t0 = performance.now(), q = -1;
    const um = (t) => { p.limpar(); desenhar(t, Math.round(t / QUADRO), reduzido()); p.mostrar(); };
    if (reduzido()) { um(parado); return { parar() { fim = true; }, pular() {}, agora: () => parado }; }
    const passo = (agora) => {
      if (fim || !p.el.isConnected) return;
      const n = Math.floor((agora - t0) / QUADRO);
      if (n !== q) { q = n; um(n * QUADRO); }
      requestAnimationFrame(passo);
    };
    um(0); q = 0;
    requestAnimationFrame(passo);
    return {
      parar() { fim = true; },
      pular(ms) { const ja = performance.now() - t0; if (ja < ms) t0 = performance.now() - ms; },
      agora: () => performance.now() - t0,
    };
  }

  // ------------------------------------------------------------------ as peças
  const nivelFade = (u, de) => (u <= de ? 16 : Math.max(0, Math.round(16 * (1 - (u - de) / (1 - de)))));

  /** Raios de sol em volta de (cx, cy): `n` cunhas de bordas duras, `larg` (0 a 1) acesa de cada passo, do raio `r0`
   *  ao `r1`, em faixas da paleta (miolo perto do centro, borda longe), com o fio do meio de cada raio mais claro e o
   *  fim apagando em pontilhado a partir de `esbate` (fração de r1). `vis` (0 a 16) apaga tudo por igual. */
  function raios(p, { cx, cy, n, ang = 0, larg = 0.5, r0 = 0, r1, pal, esbate = 0.55, vis = 16, fio = true, achata = 1,
    alterna = 1, alcance = null }) {
    if (r1 <= r0 || vis <= 0) return;
    const passo = (2 * Math.PI) / n, cs = pal.map(cor);
    const y0 = Math.max(0, Math.floor(cy - r1 * achata)), y1 = Math.min(p.H - 1, Math.ceil(cy + r1 * achata));
    const x0 = Math.max(0, Math.floor(cx - r1)), x1 = Math.min(p.W - 1, Math.ceil(cx + r1));
    const r12 = r1 * r1, r02 = r0 * r0;
    for (let y = y0; y <= y1; y++) {
      const dy = (y - cy) / achata;
      for (let x = x0; x <= x1; x++) {
        const dx = x - cx, d2 = dx * dx + dy * dy;
        if (d2 > r12 || d2 < r02) continue;
        const d = Math.sqrt(d2), at = Math.atan2(dy, dx);
        let f = (at - ang) / passo;
        const k = Math.floor(f);
        f -= k;
        if (f > larg) continue;
        // o comprimento deste raio: os ímpares mais curtos (`alterna`) e, se pedido, pela direção (`alcance`)
        const r1e = r1 * (k & 1 ? alterna : 1) * (alcance ? alcance(at) : 1), u = d / r1e;
        if (u > 1) continue;
        if (!pontilha(x, y, Math.min(vis, nivelFade(u, esbate)))) continue;
        const borda = Math.min(f, larg - f) * passo * d;  // texels até a aresta do raio
        let i = u < 0.28 ? 1 : u < 0.55 ? 2 : 3;
        if (fio && Math.abs(f - larg / 2) * passo * d < 0.6 && u < 0.8) i -= 1;  // o fio claro do meio
        else if (borda < 1) i += 1;  // a aresta, um tom abaixo
        p.buf[y * p.W + x] = cs[Math.max(0, Math.min(cs.length - 1, i))];
      }
    }
  }

  /** Feixes de holofote saindo de (cx, cy) nos ângulos `angs` (radianos; 0 = para a direita, -π/2 = para cima), cada um
   *  com meia abertura `meia`, até `r1`; a luz mais forte no eixo, a borda em pontilhado. */
  function feixes(p, { cx, cy, angs, meia, r1, pal, vis = 16, esbate = 0.5 }) {
    const cs = pal.map(cor);
    for (const a of angs) {
      const ca = Math.cos(a), sa = Math.sin(a);
      // a caixa do feixe: a ponta e o fim aberto
      const fx = cx + ca * r1, fy = cy + sa * r1, w = Math.tan(meia) * r1;
      const x0 = Math.max(0, Math.floor(Math.min(cx, fx) - w)), x1 = Math.min(p.W - 1, Math.ceil(Math.max(cx, fx) + w));
      const y0 = Math.max(0, Math.floor(Math.min(cy, fy) - w)), y1 = Math.min(p.H - 1, Math.ceil(Math.max(cy, fy) + w));
      for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
        const dx = x - cx, dy = y - cy, ao = dx * ca + dy * sa;  // ao longo do eixo
        if (ao <= 0 || ao > r1) continue;
        const lado = Math.abs(-dx * sa + dy * ca), meiaAqui = Math.tan(meia) * ao + 0.5;
        if (lado > meiaAqui) continue;
        const u = ao / r1, v = lado / meiaAqui;
        if (!pontilha(x, y, Math.min(vis, nivelFade(u, esbate), v > 0.7 ? 9 : 16))) continue;
        const i = v < 0.2 ? 0 : v < 0.5 ? 1 : v < 0.8 ? 2 : 3;
        p.buf[y * p.W + x] = cs[Math.min(cs.length - 1, i + (u > 0.6 ? 1 : 0))];
      }
    }
  }

  /** Um halo em faixas concêntricas (a mais clara no meio), a última em pontilhado. */
  function halo(p, { cx, cy, r, pal, vis = 16, achata = 1, faixas = null }) {
    if (r <= 0) return;
    const cs = pal.map(cor), nf = faixas || cs.length;
    for (let y = Math.floor(cy - r * achata); y <= cy + r * achata; y++) for (let x = Math.floor(cx - r); x <= cx + r; x++) {
      const dx = x - cx, dy = (y - cy) / achata, u = Math.sqrt(dx * dx + dy * dy) / r;
      if (u > 1) continue;
      const i = Math.min(nf - 1, Math.floor(u * nf));
      const nivel = i === nf - 1 ? 6 : i === nf - 2 ? 11 : 16;
      if (pontilha(x, y, Math.min(vis, nivel))) p.por(x, y, cs[Math.min(cs.length - 1, i)]);
    }
  }

  /** Um anel (a onda de choque): raio `r`, espessura `esp`, achatado em y por `achata`; o rastro por dentro em
   *  pontilhado. */
  function anel(p, { cx, cy, r, esp = 2, pal, achata = 1, rastro = 4, vis = 16 }) {
    const cs = pal.map(cor), ext = r + esp;
    for (let y = Math.floor(cy - ext * achata); y <= cy + ext * achata; y++) for (let x = Math.floor(cx - ext); x <= cx + ext; x++) {
      const dx = x - cx, dy = (y - cy) / achata, d = Math.sqrt(dx * dx + dy * dy);
      if (d > ext || d < r - rastro) continue;
      if (d >= r) { if (pontilha(x, y, vis)) p.por(x, y, cs[d - r < esp / 2 ? 0 : 1]); }
      else if (pontilha(x, y, Math.min(vis, Math.round(10 * (1 - (r - d) / rastro))))) p.por(x, y, cs[2] ?? cs[1]);
    }
  }

  /** Uma coluna de luz de cima até `base`, centrada em `cx`: o miolo, as bordas em faixas e listras que escorrem. */
  function coluna(p, { cx, base, larg, pal, q = 0, vis = 16, topo = 0 }) {
    const cs = pal.map(cor);
    for (let y = Math.max(0, topo); y < Math.min(base, p.H); y++) {
      const extra = ((((y >> 2) - q) % 6) + 6) % 6 === 0 ? 1 : 0, m = larg + extra;
      for (let d = -(m + 6); d <= m + 6; d++) {
        const x = cx + d, a = Math.abs(d);
        if (!pontilha(x, y, vis)) continue;
        if (a <= m * 0.4) p.por(x, y, cs[0]);
        else if (a <= m) p.por(x, y, cs[1]);
        else if (a <= m + 2) p.por(x, y, cs[2]);
        else if (pontilha(x, y, 16 - (a - m - 2) * 4)) p.por(x, y, cs[3]);
      }
    }
  }

  /** Um clarão na tela inteira (ou num retângulo), em pontilhado de `nivel` (0 a 16). */
  function clarao(p, nivel, c = "W", r = null) {
    const v = cor(c), [x0, y0, x1, y1] = r || [0, 0, p.W, p.H];
    for (let y = Math.max(0, y0); y < Math.min(p.H, y1); y++) for (let x = Math.max(0, x0); x < Math.min(p.W, x1); x++)
      if (pontilha(x, y, nivel)) p.buf[y * p.W + x] = v;
  }

  /** Uma estrela de pontas (a placa do estouro): `pontas` pontas entre os raios `ri` e `re`, girada `ang`, preenchida
   *  em faixas da paleta de fora para dentro, com contorno escuro de um texel e o lado de cima-esquerda mais claro. */
  function estrela(p, { cx, cy, pontas, ri, re, ang = 0, pal, contorno = "k", cores = null }) {
    // `cores` ([miolo, meio, aro, luz do aro]) troca as faixas da paleta: o selo de miolo escuro e aro de metal
    const cs = cores ? [cores[3], cores[0], cores[1], cores[2]].map(cor) : pal.map(cor), ck = cor(contorno), passo = (2 * Math.PI) / pontas;
    const raioEm = (a) => {
      let f = (a - ang) / passo; f -= Math.floor(f);
      const t = Math.abs(f - 0.5) * 2;  // 1 na ponta, 0 no vale
      return ri + (re - ri) * t;
    };
    for (let y = Math.floor(cy - re - 1); y <= cy + re + 1; y++) for (let x = Math.floor(cx - re - 1); x <= cx + re + 1; x++) {
      const dx = x - cx, dy = y - cy, d = Math.sqrt(dx * dx + dy * dy), a = Math.atan2(dy, dx), r = raioEm(a);
      if (d > r + 1) continue;
      if (d > r) { p.por(x, y, ck); continue; }
      const u = d / r;
      let i = u < 0.45 ? 1 : u < 0.75 ? 2 : 3;
      if (u > 0.82 && (dx + dy) < 0) i -= 1;  // a luz de cima e da esquerda na borda
      p.por(x, y, cs[Math.max(0, Math.min(cs.length - 1, i))]);
    }
  }

  /** Um poço escuro (uma elipse de raios rx, ry) que apaga em pontilhado do meio para a borda: o efeito passa por
   *  trás da área de leitura sem disputar com o texto. `forca` (0 a 16) é o escuro no meio. */
  function poco(p, { cx, cy, rx, ry, forca = 14, c = "N" }) {
    const v = cor(c);
    for (let y = Math.max(0, Math.floor(cy - ry)); y <= Math.min(p.H - 1, cy + ry); y++)
      for (let x = Math.max(0, Math.floor(cx - rx)); x <= Math.min(p.W - 1, cx + rx); x++) {
        const dx = (x - cx) / rx, dy = (y - cy) / ry, u = Math.sqrt(dx * dx + dy * dy);
        if (u > 1) continue;
        if (pontilha(x, y, Math.round(forca * Math.min(1, (1 - u) * 4)))) p.buf[y * p.W + x] = v;  // cheio até 3/4, depois apaga
      }
  }

  /** O clarão concentrado na origem: um halo claro que abre e apaga em `dur` ms em volta de (cx, cy), e só um
   *  pontilhado baixo (`espalha`, 0 a 16) na tela inteira nos dois primeiros quadros. O prêmio e a leitura continuam
   *  reconhecíveis. */
  function claraoLocal(p, { cx, cy, r, t, dur = 180, espalha = 2, pal = ["W", "W", "Y", "O"] }) {
    if (t > dur) return;
    const u = t / dur;
    if (t < 140 && espalha) clarao(p, espalha, "W");
    halo(p, { cx, cy, r: Math.round(r * (0.7 + u * 0.6)), pal, vis: Math.round(15 * (1 - u)) });
  }

  // ------------------------------------------------------------------ partículas desenhadas à mão
  // Cada grade: "a" é a cor da idade da partícula, "b" a um tom mais claro; "." vazio.
  const DESENHOS = {
    ponto: ["a"],
    duplo: ["ab"],
    cruz: [".a.", "aba", ".a."],
    estrela: ["..a..", "..a..", "aabaa", "..a..", "..a.."],
    brilho: ["...a...", "...a...", "..aba..", "aabbbaa", "..aba..", "...a...", "...a..."],
    losango: ["..a..", ".aba.", "abbba", ".aba.", "..a.."],
    lasca: ["ab", "a."],
    caco: [".ab", "aba", "a.."],
    brasa: ["b", "a"],
    moeda: [".aa.", "abba", "abba", ".aa."],
  };
  /** Um enxame: `soltar(n, gerar)` cria partículas ({x, y, vx, vy, g, arrasto, vida, desenho, pal, piscar}); `passo()`
   *  move um quadro; `desenhar(p)` pinta cada uma pela idade (o tom vai do claro ao escuro da paleta). */
  function enxame() {
    const lista = [];
    return {
      lista,
      soltar(n, gerar) { for (let i = 0; i < n; i++) lista.push({ idade: 0, g: 0, arrasto: 1, piscar: false, ...gerar(i) }); },
      passo() {
        for (let i = lista.length - 1; i >= 0; i--) {
          const s = lista[i];
          s.idade++;
          if (s.idade > s.vida) { lista.splice(i, 1); continue; }
          s.vx *= s.arrasto; s.vy = s.vy * s.arrasto + s.g;
          s.x += s.vx; s.y += s.vy;
        }
      },
      desenhar(p) {
        for (const s of lista) {
          if (s.piscar && s.idade % 3 === 2) continue;
          const g = DESENHOS[s.desenho] || DESENHOS.ponto, cs = s.pal;
          const k = Math.min(cs.length - 1, Math.floor((s.idade / (s.vida + 1)) * cs.length) + (s.tom || 0));
          const a = cor(cs[k]), b = cor(cs[Math.max(0, k - 1)]);
          const ox = Math.round(s.x) - (g[0].length >> 1), oy = Math.round(s.y) - (g.length >> 1);
          for (let y = 0; y < g.length; y++) for (let x = 0; x < g[y].length; x++) {
            const ch = g[y][x];
            if (ch === "a") p.por(ox + x, oy + y, a);
            else if (ch === "b") p.por(ox + x, oy + y, b);
          }
        }
      },
    };
  }

  /** A tela inteira treme alguns quadros (em pixels inteiros, cada vez menos). */
  function tremer(px) {
    if (reduzido() || !px) return;
    const passos = [1, -0.8, 0.6, -0.45, 0.3, -0.15, 0];
    passos.forEach((f, i) => setTimeout(() => {
      document.body.style.translate = f ? `${Math.round(px * f)}px ${Math.round(px * f * -0.5)}px` : "";
    }, i * QUADRO));
  }

  /** Um valor que sai de `a` e chega a `b` em `ms`, em degraus (ease-out), para a linha do tempo dos efeitos. */
  const rampa = (t, de, ms, a = 0, b = 1) => (t <= de ? a : t >= de + ms ? b : a + (b - a) * (1 - Math.pow(1 - (t - de) / ms, 3)));
  const aleatorio = (a, b) => a + Math.random() * (b - a);

  return { cor, reduzido, FPS, QUADRO, PALETAS, DESENHOS, palco, animar, raios, feixes, halo, anel, coluna, clarao, claraoLocal, estrela, poco,
    enxame, tremer, rampa, aleatorio };
})();

/* PROTÓTIPO da etapa 2, segunda rodada (24/10/2026; nada no jogo): Festa, o que as três direções têm em comum.
   - os dados de cada festa já em pedaços (os ganhos com os ícones da HUD, o ponto de talento, as habilidades);
   - a regra dos gestos: o Continuar, o Enter, o Espaço e o Esc fecham a qualquer momento; um clique fora durante a
     entrada só a adianta; não contam o toque que começou antes de a festa abrir, o 2º clique de um clique duplo nem a
     tecla segurada; o gesto que fecha não atravessa para a página (nem para a festa seguinte);
   - o achado: a janela, o adiantar (um clique ou tecla durante a entrada leva ao fim dela; não escolhe nada, os botões
     ainda não estão lá) e a ordem do motor (os botões chegam quando a entrada termina).
   Cada direção (Festa.direcao) só diz o desenho: o HTML e o efeito. */
"use strict";

const Festa = (() => {
  const h = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const VITAIS = ["Vida", "Mana", "Vigor", "Foco"];
  const RARIDADE = { comum: "Comum", magico: "Mágico", raro: "Raro", lendario: "Lendário" };
  const CLASSE = { guerreiro: "Guerreiro", arqueiro: "Arqueiro", mago: "Mago" };
  let direcao = null;

  /** O ícone de um ganho de nível (o da HUD: os vitais e os atributos). */
  function icone(k, lado = 24) {
    return (VITAIS.includes(k) ? Icones.vital(k, lado === 24 ? 20 : lado) : Icones.atributo(k, lado)) || "";
  }
  const ganhos = (d) => Object.entries(d.ganhos || {}).map(([k, v]) => ({ k, v, icone: icone(k) }));
  const talento = (lado = 32) => Icones.atalho("Talentos", lado) || "";
  const habilidades = (lista) => (lista || []).map((x) => ({ nome: h(x.nome), desc: Realce.texto(x.desc), icone: Telas.S(x.icone || "estrela", 2) }));
  /** O Continuar no acabamento dos botões do jogo (a face e a aresta da HUD), com a tecla. */
  const continuar = (rotulo = "Continuar") => `<button class="continuar" type="button">${rotulo}<kbd>Enter</kbd></button>`;
  const heroi = () => (App.estado && App.estado.heroi) || {};

  /** A janela da festa aberta em `caixa` (#celebracao) com `html`; `efeito(el)` liga o efeito e devolve o controle dele
   *  ({ parar, revelar }). Resolve quando o jogador fecha. */
  function abrir(caixa, html, efeito, { revelaEm = 900 } = {}) {
    caixa.innerHTML = html;
    caixa.hidden = false;
    caixa.classList.add("festa-v2", "dir-" + direcao.nome);
    const el = caixa.querySelector(".festa"), botao = caixa.querySelector(".continuar");
    const sel = window.getSelection(); if (sel) sel.removeAllRanges();  // a seleção que um clique duplo deixou
    const ctl = efeito ? efeito(el, caixa) || {} : {};
    const nasceu = performance.now();
    let toque = 0, revelado = false;
    const revelar = () => { if (revelado) return; revelado = true; el.classList.add("revelada"); if (ctl.revelar) ctl.revelar(); };
    const auto = setTimeout(revelar, revelaEm);
    botao.focus({ preventScroll: true });
    return new Promise((resolver) => {
      const fechar = () => {
        clearTimeout(auto);
        if (ctl.parar) ctl.parar();
        caixa.hidden = true; caixa.innerHTML = "";
        caixa.classList.remove("festa-v2", "dir-" + direcao.nome);
        document.body.style.translate = "";
        document.removeEventListener("pointerdown", tocou, true);
        document.removeEventListener("click", clique, true);
        document.removeEventListener("keydown", tecla, true);
        resolver();
      };
      const tocou = () => { toque = performance.now(); };
      const clique = (ev) => {
        ev.preventDefault(); ev.stopPropagation();
        if (ev.detail > 1 || toque < nasceu) return;
        if (ev.target.closest(".continuar") || revelado) fechar(); else revelar();
      };
      const tecla = (ev) => {
        if (ev.repeat || ![" ", "Enter", "Escape"].includes(ev.key)) return;
        ev.preventDefault(); ev.stopPropagation(); fechar();
      };
      document.addEventListener("pointerdown", tocou, true);
      document.addEventListener("click", clique, true);
      document.addEventListener("keydown", tecla, true);
    });
  }

  /** O nível, o Sigilo e a especialização, pela direção escolhida. */
  function celebrar(m, caixa, instantaneo) {
    if (!["nivel", "sigilo", "spec"].includes(m.tipo) || instantaneo) return Promise.resolve();
    const d = m.dados, f = direcao[m.tipo](d);
    return abrir(caixa, f.html, f.efeito, f);
  }

  // ------------------------------------------------------------------ o achado
  const adiar = (ms, cancelado) => new Promise((r) => {
    const fim = performance.now() + App.ritmo(ms);
    const ver = () => (cancelado() || performance.now() >= fim ? r() : setTimeout(ver, 20));
    ver();
  });

  /** A janela do achado (no lugar de Telas.abrirAchado): o HTML da direção, os botões reservados (os rótulos que vêm
   *  com o cartão, invisíveis: a janela já nasce no tamanho final) e a entrada da direção. */
  async function abrirAchado(d, semCerimonia = false) {
    Telas.fecharAchado();
    const fundo = document.createElement("div");
    fundo.id = "sobre-achado";
    fundo.className = `sobreposicao achado-v2 dir-${direcao.nome} rar-${h(d.item.raridade)}`;
    const reserva = (d.acoes || []).map((t, i) => `<button type="button" class="botao-janela reserva" tabindex="-1" aria-hidden="true"><kbd>${i + 1}</kbd>${h(t)}</button>`).join("");
    fundo.innerHTML = `<div class="janela-achado">${direcao.achado(d)}<div class="achado-acoes">${reserva}</div></div>`;
    document.body.appendChild(fundo);
    const janela = fundo.firstElementChild;
    if (direcao.noPalco) Telas.noPalco(janela);
    if (semCerimonia) { fundo.classList.add("pronto"); direcao.cerimonia({ fundo, janela, d, parado: true, adiantou: () => true }); return; }
    let adiantou = false;
    const adiantar = (ev) => {
      if (ev.type === "keydown" && (ev.repeat || ![" ", "Enter", "Escape"].includes(ev.key))) return;
      ev.preventDefault(); ev.stopPropagation();
      if (!adiantou) { adiantou = true; fundo.classList.add("adiantado"); }
    };
    document.addEventListener("pointerdown", adiantar, true);
    document.addEventListener("keydown", adiantar, true);
    try {
      await direcao.cerimonia({ fundo, janela, d, adiantou: () => adiantou, esperar: (ms) => adiar(ms, () => adiantou) });
    } finally {
      document.removeEventListener("pointerdown", adiantar, true);
      document.removeEventListener("keydown", adiantar, true);
    }
    fundo.classList.add("pronto");
  }

  /** O texto do item como o jogo escreve (htmlItem), com a raridade fora da linha do tipo: ela tem o selo próprio. */
  const textoItem = (it, comparando = true) => Telas.htmlItem(it, "", comparando).replace(/(<div class="tipo">[^<]*?) · [^<]*<\/div>/, "$1</div>");
  /** O desenho do item: o arquivo de 64 da interface ampliado 2× (fator inteiro), ou o sprite do jogo. */
  const arteItem = (it, lado = 64) => Icones.porDesenho(Telas.iconeItem(it), lado) || Telas.S(Telas.iconeItem(it), lado / 16);
  /** Os cartões do que você usa (um, ou os dois espaços de anel), como no jogo. */
  function equipados(d, classe = "") {
    const aneis = d.espacos && (d.equipados || []).length;
    if (aneis) return `<div class="achado-aneis ${classe}">${d.espacos.map((e) => e.item
      ? `<div class="achado-cartao atual compacto rar-${h(e.item.raridade)}" data-espaco="${h(e.espaco)}"><span class="achado-selo">${h(e.nome)} · você usa</span>
          <div class="compacto-corpo"><div class="achado-arte pequena">${arteItem(e.item, 48)}</div><div>${textoItem(e.item, false)}</div></div></div>`
      : `<div class="achado-cartao atual compacto vazio" data-espaco="${h(e.espaco)}"><span class="achado-selo">${h(e.nome)} · vazio</span>
          <div class="compacto-corpo"><div class="achado-arte pequena">${Icones.vazio(e.espaco, 48) || ""}</div></div></div>`).join("")}</div>`;
    return (d.equipados || []).map((e) => `<div class="achado-cartao atual rar-${h(e.raridade)} ${classe}">
        <span class="achado-selo">Você usa</span>
        <div class="achado-arte pequena">${arteItem(e, 48)}</div>${textoItem(e, false)}</div>`).join("");
  }
  /** O aviso da mochila cheia, como no jogo. */
  function aviso(d) {
    const aneis = d.espacos && (d.equipados || []).length;
    return !d.pode_usar || d.cabe ? "" : aneis && d.espacos.some((e) => !e.item)
      ? '<div class="pior">Mochila cheia: substituir um anel deixa o antigo para trás.</div>'
      : '<div class="pior">Mochila cheia: equipar deixa o item antigo para trás.</div>';
  }

  // As imagens da HUD por caminho absoluto: o estilo das direções é injetado na página, e o url() relativo das variáveis
  // (../hud/...) passaria a contar da página. O gesto não seleciona texto nas janelas.
  document.head.insertAdjacentHTML("beforeend", `<style id="estilo-festa-v2">
    :is(#celebracao, #sobre-achado, .achado-v2) { --m-principal: url(/static/hud/moldura-nove.png); --t-painel: url(/static/hud/textura-painel.png); }
    #celebracao.festa-v2 :is(.festa, .continuar) { user-select: none; }
    #celebracao.festa-v2 { overflow-y: auto; place-items: safe center; }
    .fx-palco { image-rendering: pixelated; }
    /* o item ampliado 2× ocupa a caixa dele (o efeito mira no meio dela); sem o brilho borrado e o pulo suave da produção */
    .achado-v2 .achado-arte { filter: none; animation: none; }
    .achado-v2 .achado-cartao.novo .achado-arte:not(.pequena) { width: 128px; height: 128px; margin: 0; }</style>`);

  /** A ficha do achado em pedaços, para as direções compor sem molduras: o nome, o tipo, os números do prêmio, a troca
   *  (o que muda, linha a linha, pelo Telas.linhasTroca do jogo) e o que você usa (cartões .achado-cartao.atual, que
   *  as celebrações de vestir e guardar procuram). Sem nada no espaço, a troca e o "você usa" ficam vazios. */
  function fichaItem(d) {
    const it = d.item, rar = h(it.raridade), hr = heroi();
    const linhas = (x) => h(x.bonus || "").split(", ").filter(Boolean).map((l) => `<span>${l}</span>`).join("") +
      (x.efeito ? `<span class="efeito">${h(x.efeito)}</span>` : "");
    const naoUsa = it.classe && hr.classe && it.classe !== hr.classe ? `<div class="pior">Só ${h({ guerreiro: "guerreiros", arqueiro: "arqueiros", mago: "magos" }[it.classe] || it.classe)} sabem usar isto.</div>` : "";
    const premio = `<div class="ficha-premio"><span class="ficha-rotulo">${h(Telas.NOME_ESPACO[it.slot] || "")}</span><div class="ficha-linhas">${linhas(it)}</div>${naoUsa}</div>`;
    const aneis = d.espacos && (d.equipados || []).length;
    let troca = "", usa = "";
    if (aneis) {
      usa = d.espacos.map((e) => e.item
        ? `<div class="achado-cartao atual rar-${h(e.item.raridade)}" data-espaco="${h(e.espaco)}"><span class="achado-selo">${h(e.nome)} · você usa</span>
            <div class="ficha-usa-nome">${arteItem(e.item, 32)}<b class="r-${h(e.item.raridade)}">${h(e.item.nome)}</b></div>
            <div class="ficha-troca">${Telas.linhasTroca(it, e.item)}</div></div>`
        : `<div class="achado-cartao atual vazio" data-espaco="${h(e.espaco)}"><span class="achado-selo">${h(e.nome)} · vazio</span></div>`).join("");
    } else if ((d.equipados || []).length) {
      const e = d.equipados[0];
      troca = `<div class="ficha-troca"><span class="ficha-rotulo">na troca</span>${Telas.linhasTroca(it, e)}</div>`;
      usa = `<div class="achado-cartao atual rar-${h(e.raridade)}"><span class="achado-selo">Você usa</span>
        <div class="ficha-usa-nome">${arteItem(e, 32)}<b class="r-${h(e.raridade)}">${h(e.nome)}</b></div>
        <div class="ficha-linhas">${linhas(e)}</div></div>`;
    }
    return {
      rar, nome: `<b class="ficha-nome r-${rar}">${h(it.nome)}</b>`, raridade: `<span class="ficha-raridade rar-${rar}">${RARIDADE[it.raridade] || rar}</span>`,
      premio, troca, usa, compara: !!(troca || usa),
      lore: it.lore ? `<div class="ficha-lore">"${h(it.lore)}"</div>` : "", aviso: aviso(d),
    };
  }

  return {
    h, RARIDADE, fichaItem, CLASSE, icone, ganhos, talento, habilidades, continuar, heroi, abrir, celebrar, abrirAchado, textoItem, arteItem,
    equipados, aviso,
    usar(d) { direcao = d; },
    get direcao() { return direcao; },
  };
})();

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

/* PROTÓTIPO (24/10/2026; nada no jogo): AS IDENTIDADES das especializações, separadas da APRESENTAÇÃO (Relicário ou
   Estouro). O piloto do Piromante (identidade.js, aprovado) virou a primeira de seis; cada uma diz as cores do nome e
   dos raios e o que acontece em volta do nome, com forma e movimento próprios:
   - fogo (Piromante): chamas nascem do topo das letras e sobem; brasas;
   - luz (Paladino): colunas de luz descem sobre o nome; brilhos nas pontas das letras; partículas de luz sobem devagar;
   - sangue (Berserker): fissuras se abrem do nome; o sangue escorre e pinga da base das letras; o fundo bate como um
     coração (dois golpes e uma pausa);
   - folhas (Patrulheiro): rajadas de vento levam folhas que giram em volta do nome, da esquerda para a direita;
   - sombra (Sombra): fumaça escura sai das bordas das letras e se espalha; um corte de lâmina cruza o fundo de tempos em
     tempos; gotas de veneno caem;
   - almas (Necromante): almas com rastro vêm de longe em espiral e entram no nome (o dreno); um círculo de maldição gira
     no chão.
   O corpo das letras fica parado e legível (as cores em faixas duras, a borda e uma sombra escura); tudo acontece nas
   bordas e em volta, num poço escuro logo atrás do nome. Com o movimento reduzido, cada uma tem um quadro parado próprio.
   As cores das raridades não mudam; só a festa da especialização usa isto. */
"use strict";

const Identidades = (() => {
  // a festa da especialização manda o nome (o motor não manda o id)
  const POR_NOME = { Piromante: "fogo", Paladino: "luz", Berserker: "sangue", Patrulheiro: "folhas", Sombra: "sombra", Necromante: "almas" };
  const qual = (nome) => POR_NOME[nome] || null;
  // a paleta dos raios (do Relicário) e do estouro (do Estouro), do mais claro ao mais escuro
  const PAL = {
    fogo: ["W", "Y", "O", "o", "r"], luz: ["W", "W", "w", "G", "g"], sangue: ["p", "R", "r", "D", "D"],
    folhas: ["Y", "E", "e", "f", "B"], sombra: ["W", "G", "m", "x", "K"], almas: ["W", "T", "t", "x", "k"],
  };
  // os estilhaços do Estouro na cor da identidade
  const CACOS = {
    fogo: ["Y", "O", "o", "r", "D"], luz: ["W", "w", "Y", "c", "C"], sangue: ["R", "r", "D", "D", "k"],
    folhas: ["E", "e", "f", "B", "B"], sombra: ["G", "g", "x", "K", "k"], almas: ["T", "t", "x", "K", "k"],
  };

  // ---------------------------------------------------------------- desenhos à mão (grades; "a" a borda, "b" o miolo)
  const CHAMAS = [
    ["...a...", "...a...", "..aba..", "..aba..", ".abba..", ".abbba.", "abbbbba", "abbbbba", ".aaaaa."],
    ["..a..", "..a..", ".aba.", ".abba", "abbba", "abbba", ".aaa."],
    ["..a..", ".aba.", ".aba.", "abbba", ".aaa."],
    [".a.", "aba", "aba", ".a."],
    ["a", "a"],
  ];
  const COR_CHAMA = [["Y", "W"], ["O", "Y"], ["O", "Y"], ["o", "O"], ["r", "o"]];
  const FOLHAS = [  // a folha girando em quatro quadros
    ["..aa", ".aba", "aba.", "a..."],
    ["...", "aba", "bba", "aa."],
    ["a...", "aba.", ".aba", "..aa"],
    [".a.", "aba", "aba", ".a."],
  ];
  const GOTA = [["a"], ["a", "a"], [".a.", "aba", ".a."]];  // a gota se alongando e a gota caindo
  const ALMA = [".a.", "aba", "aba", "a.a"];  // a alma: um vulto pequeno com a barra rasgada
  const RUNAS = [["a.a", ".a.", "a.a"], ["aaa", "a..", "aaa"], [".a.", "aaa", ".a."], ["a..", "aaa", "..a"]];

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

  // ---------------------------------------------------------------- as seis
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
    // LUZ: colunas descendo sobre o nome, que pulsam devagar; brilhos nas pontas das letras; partículas de luz subindo
    luz: {
      quadro({ p, r, c, q, t, parado, ex, dados }) {
        if (!dados.colunas) dados.colunas = [-0.78, -0.42, -0.1, 0.22, 0.55, 0.85].map((f, i) => ({ x: r.x + Math.round(f * r.rx), larg: i % 2 ? 1 : 2, fase: i * 1.3 }));
        const desce = parado ? 1 : FX.rampa(t, 0, 420);
        for (const col of dados.colunas) {
          const pulso = parado ? 12 : 10 + Math.round(4 * (0.5 + 0.5 * Math.sin(t / 700 + col.fase)));
          FX.coluna(p, { cx: col.x, base: Math.round(r.topo * desce), larg: col.larg, pal: ["W", "w", "G", "g"], q: parado ? 0 : q >> 1, vis: pulso });
        }
        fundoDoNome(p, r, ["w", "G", "g"], q, parado);
        if (!parado) {
          if (q % 3 === 0) ex.soltar(1, () => ({ tipo: "mote", x: r.x + Math.round(FX.aleatorio(-r.rx * 1.2, r.rx * 1.2)), y: r.y + Math.round(FX.aleatorio(-r.ry, r.ry * 1.3)), vx: 0, vy: -0.35, vida: Math.round(FX.aleatorio(20, 34)) }));
          if (q % 4 === 0 && c.topos.length) ex.soltar(1, () => { const o = sorteio(c.topos.filter((x) => x.alto).length ? c.topos.filter((x) => x.alto) : c.topos); return { tipo: "brilho", x: o.x, y: o.y - 1, vida: 6 }; });
        }
      },
      desenhar(p, s) {
        if (s.tipo === "mote") { const k = s.idade / (s.vida + 1); if (Sprites.pontilha(Math.round(s.x), Math.round(s.y), Math.round(16 * (1 - k)))) p.por(Math.round(s.x), Math.round(s.y), FX.cor(k < 0.5 ? "W" : "Y")); return; }
        const g = s.idade < 2 || s.idade > 4 ? FX.DESENHOS.cruz : FX.DESENHOS.brilho;
        grade(p, g, Math.round(s.x) - (g[0].length >> 1), Math.round(s.y) - (g.length >> 1), FX.cor("Y"), FX.cor("W"));
      },
      parado: 14,
    },
    // SANGUE: fissuras saindo do nome (paradas depois de abrir); gotas escorrendo e pingando da base das letras; o fundo
    // batendo como um coração
    sangue: {
      quadro({ p, r, c, q, t, parado, ex, dados }) {
        // o coração: dois golpes (0 e 180 ms) a cada 1,1 s; no movimento reduzido, parado no meio
        const fase = t % 1100, batida = parado ? 0.5 : fase < 120 ? 1 : fase > 180 && fase < 280 ? 0.7 : 0;
        FX.halo(p, { cx: r.x, cy: r.y, r: Math.round(r.rx * (1.35 + 0.12 * batida)), achata: 0.55, pal: ["R", "r", "D", "D"], vis: 4 + Math.round(5 * batida) });
        fundoDoNome(p, r, ["r", "D", "D"], q, parado);
        // o anel do coração em volta do nome: cresce e acende nos dois golpes
        FX.anel(p, { cx: r.x, cy: r.y, r: Math.round(r.rx * (1.12 + 0.06 * batida)), esp: 2, pal: ["R", "r", "D"], achata: 0.5, rastro: 3, vis: 5 + Math.round(11 * batida) });
        if (!dados.fissuras) dados.fissuras = fissuras(r);
        const abre = parado ? 1 : FX.rampa(t, 0, 380);
        for (const f of dados.fissuras) for (let i = 0; i < Math.round(f.length * abre); i++) {
          const [x, y] = f[i], claro = i < 6 || i % 9 === 0;
          p.por(x, y - 1, FX.cor("k")); p.por(x, y, FX.cor(claro ? "R" : "r")); p.por(x, y + 1, FX.cor("D")); p.por(x, y + 2, FX.cor("k"));
        }
        if (!parado && c.bases.length) ex.soltar(q % 2 === 0 ? 2 : 1, () => { const o = sorteio(c.bases);
          return { tipo: "gota", x: o.x, y: o.y + 1, x0: o.x, vida: Math.round(FX.aleatorio(14, 22)), pinga: Math.round(FX.aleatorio(5, 9)),
            mover: (s) => { if (s.idade > s.pinga) { s.vy = (s.vy || 0) + 0.18; s.y += s.vy; } } }; });
      },
      desenhar(p, s) {
        const caindo = s.idade > s.pinga, g = caindo ? GOTA[2] : s.idade > s.pinga / 2 ? GOTA[1] : GOTA[0];
        grade(p, g, Math.round(s.x) - (g[0].length >> 1), Math.round(s.y), FX.cor(caindo ? "r" : "R"), FX.cor("R"));
      },
      parado: 10,
    },
    // FOLHAS: rajadas de vento da esquerda para a direita levam folhas que giram em volta do nome; riscos de vento
    folhas: {
      quadro({ p, r, q, t, parado, ex }) {
        fundoDoNome(p, r, ["e", "f", "f"], q, parado);
        const rajada = parado ? true : (t % 2400) < 900;  // uma rajada a cada 2,4 s; entre elas, uma folha ou outra
        if (!parado && (rajada ? q % 1 === 0 : q % 5 === 0)) ex.soltar(rajada ? 2 : 1, () => {
          const y0 = r.y + Math.round(FX.aleatorio(-r.ry * 1.7, r.ry * 0.8));
          return { tipo: "folha", x: r.esq - p.t(120) + Math.round(FX.aleatorio(-20, 20)), y: y0, y0, vx: FX.aleatorio(2.4, 4.2), vida: Math.round(FX.aleatorio(24, 40)),
            fase: Math.random() * 6, cor: Math.random() < 0.2 ? 1 : 0, mover: (s) => { s.x += s.vx; s.y = s.y0 + Math.round(Math.sin(s.idade * 0.35 + s.fase) * 6) - Math.round(s.idade * 0.1); } };
        });
        if (!parado && rajada && q % 3 === 0) ex.soltar(1, () => ({ tipo: "risco", x: r.esq - p.t(60), y: r.y + Math.round(FX.aleatorio(-r.ry * 1.4, r.ry * 1.4)), vx: 6, vida: 8, larg: Math.round(FX.aleatorio(6, 14)) }));
      },
      desenhar(p, s) {
        if (s.tipo === "risco") { const c = FX.cor("E"); for (let i = 0; i < s.larg; i++) if (Sprites.pontilha(Math.round(s.x) - i, Math.round(s.y), 12 - i)) p.por(Math.round(s.x) - i, Math.round(s.y), c); return; }
        const g = FOLHAS[Math.floor(s.idade / 2 + s.fase) % FOLHAS.length];
        grade(p, g, Math.round(s.x), Math.round(s.y), FX.cor(s.cor ? "b" : "e"), FX.cor(s.cor ? "n" : "E"));
      },
      parado: 16,
    },
    // SOMBRA: fumaça saindo das bordas das letras e se espalhando; o corte de lâmina; gotas de veneno
    sombra: {
      quadro({ p, r, c, q, t, parado, ex, dados }) {
        fundoDoNome(p, r, ["x", "K", "k"], q, parado);
        // o corte: a cada 2,2 s, um risco claro em diagonal atrás do nome, dois quadros, e o brilho na ponta
        const ciclo = parado ? 60 : (t - 500) % 2200;
        if (t > 500 && ciclo < 140) {
          const u = Math.min(1, ciclo / 70), x0 = r.esq - 10, y0 = r.topo + 1, x1 = r.dir + 10, y1 = r.base - 1, n = Math.round((x1 - x0) * u);
          for (let i = 0; i < n; i++) { const x = x0 + i, y = Math.round(y0 + ((y1 - y0) * i) / (x1 - x0)); p.por(x, y - 1, FX.cor("G")); p.por(x, y, FX.cor(i > n - 8 ? "W" : "G")); p.por(x, y + 1, FX.cor("m")); }
          if (!dados.cortou || dados.cortou !== Math.floor((t - 500) / 2200)) { dados.cortou = Math.floor((t - 500) / 2200); ex.soltar(1, () => ({ tipo: "faisca", x: x1, y: y1, vida: 5 })); }
        }
        if (!parado) {
          if (c.lados.length) ex.soltar(3, () => { const o = sorteio(c.todos);
            return { tipo: "fumo", x: o.x, y: o.y, vx: FX.aleatorio(-0.9, 0.9), vy: FX.aleatorio(-1.1, -0.45), vida: Math.round(FX.aleatorio(16, 26)), tam: Math.random() < 0.5 ? 2 : 1 }; });
          // os véus: sombras que rastejam rente ao chão, dos dois lados do nome para fora
          if (q % 2 === 0) ex.soltar(1, (i) => { const lado = Math.random() < 0.5 ? -1 : 1;
            return { tipo: "veu", x: lado < 0 ? r.esq + 4 : r.dir - 4, y: r.base - Math.round(FX.aleatorio(0, r.ry * 0.8)), vx: lado * FX.aleatorio(1.2, 2.2), vy: FX.aleatorio(-0.15, 0.15), vida: Math.round(FX.aleatorio(14, 22)), larg: Math.round(FX.aleatorio(8, 16)) }; });
          if (q % 7 === 0 && c.bases.length) ex.soltar(1, () => { const o = sorteio(c.bases); return { tipo: "veneno", x: o.x, y: o.y + 1, vy: 0.2, g: 0.15, vida: 16 }; });
        }
      },
      desenhar(p, s) {
        if (s.tipo === "faisca") { grade(p, FX.DESENHOS.brilho, Math.round(s.x) - 3, Math.round(s.y) - 3, FX.cor("G"), FX.cor("W")); return; }
        if (s.tipo === "veu") {  // uma faixa de fumaça escura que se alonga para trás e apaga
          const k = s.idade / (s.vida + 1), dir = Math.sign(s.vx) || 1;
          for (let i = 0; i < s.larg; i++) for (let y = 0; y < 2; y++) { const x = Math.round(s.x) - dir * i;
            if (Sprites.pontilha(x, Math.round(s.y) + y, Math.round((12 - i * 0.6) * (1 - k)))) p.por(x, Math.round(s.y) + y, FX.cor(i < 3 ? "g" : "m")); }
          return;
        }
        if (s.tipo === "veneno") { grade(p, GOTA[2], Math.round(s.x) - 1, Math.round(s.y), FX.cor("e"), FX.cor("E")); return; }
        const k = s.idade / (s.vida + 1), cor = FX.cor(k < 0.3 ? "G" : k < 0.6 ? "g" : "m"), t = s.tam + (k > 0.4 ? 1 : 0) + (k > 0.75 ? 1 : 0);
        for (let y = 0; y <= t; y++) for (let x = 0; x <= t; x++) if (Sprites.pontilha(Math.round(s.x) + x, Math.round(s.y) + y, Math.round(13 * (1 - k)))) p.por(Math.round(s.x) + x, Math.round(s.y) + y, cor);
      },
      parado: 40,
    },
    // ALMAS: almas que vêm de longe em espiral e entram no nome, com rastro; o círculo de maldição girando no chão
    almas: {
      quadro({ p, r, q, t, parado, ex }) {
        // o círculo: um anel achatado debaixo do nome, com runas que andam em degraus
        const cy = r.base - 3, rx = Math.round(r.rx * 1.08), ang = parado ? 0 : Math.floor(t / 260) * 0.12;
        FX.anel(p, { cx: r.x, cy, r: rx, esp: 1, pal: ["T", "t", "x"], achata: 0.1, rastro: 2, vis: parado ? 12 : 10 + ((q >> 2) % 2) * 3 });
        for (let i = 0; i < 8; i++) { const a = ang + (i / 8) * Math.PI * 2, x = r.x + Math.round(Math.cos(a) * rx), y = cy + Math.round(Math.sin(a) * rx * 0.1);
          grade(p, RUNAS[i % RUNAS.length], x - 1, y - 1, FX.cor(Math.sin(a) > 0 ? "T" : "t"), 0); }
        fundoDoNome(p, r, ["t", "x", "k"], q, parado);
        if (!parado && q % 3 === 0) ex.soltar(1, () => {
          const a0 = Math.random() * Math.PI * 2, d0 = r.rx * FX.aleatorio(1.3, 1.8);
          return { tipo: "alma", vida: Math.round(FX.aleatorio(22, 30)), a0, d0, rastro: [], x: r.x, y: r.y,
            mover: (s) => { const u = s.idade / s.vida, a = s.a0 + u * 3.2, d = s.d0 * (1 - u * 0.92);
              s.rastro.unshift([s.x, s.y]); if (s.rastro.length > 4) s.rastro.pop();
              s.x = r.x + Math.cos(a) * d; s.y = r.y + Math.sin(a) * d * 0.5 - (1 - u) * 6; } };
        });
      },
      desenhar(p, s) {
        s.rastro.forEach(([x, y], i) => { if (Sprites.pontilha(Math.round(x), Math.round(y), 12 - i * 3)) p.por(Math.round(x), Math.round(y), FX.cor(i < 2 ? "T" : "t")); });
        const perto = s.idade / s.vida > 0.75;
        grade(p, ALMA, Math.round(s.x) - 1, Math.round(s.y) - 2, FX.cor(perto ? "W" : "T"), FX.cor(perto ? "T" : "W"));
      },
      parado: 8,
    },
  };

  /** As fissuras do Berserker: linhas quebradas saindo dos dois lados do nome, perto da base, para fora e um pouco
   *  para baixo (pontos em texels). */
  function fissuras(r) {
    const linhas = [];
    for (const lado of [-1, 1]) for (let k = 0; k < 3; k++) {
      let x = lado < 0 ? r.esq - 2 : r.dir + 2, y = r.base - 2 - k * Math.round(r.ry * 0.5);
      const pts = [], comp = 30 + k * 10;
      for (let i = 0; i < comp; i++) { x += lado; if (i % 4 === 0) y += Math.random() < 0.5 ? 1 : Math.random() < 0.5 ? -1 : 0; pts.push([x, y]);
        if (i === Math.round(comp * 0.5) && k === 0) linhas.push(pts.slice(-1).concat(Array.from({ length: 10 }, (_, j) => [x + lado * j, y + Math.round(j * 0.6)]))); }
      linhas.push(pts);
    }
    return linhas;
  }

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
  .idn-luz { ${faixas("#ffffff", "#f1e4c4", "#c0b8a8")} filter: ${borda("#8a6a14", "#f2c94c", "#4a4038")}; }
  .idn-sangue { ${faixas("#f1e4c4", "#e8c8b0", "#e2574c")} filter: ${borda("#6e0d0d", "#b3262b", "#2a0a0a")}; }
  .idn-folhas { ${faixas("#d8eeb0", "#8fbf6a", "#4f9a5b")} filter: ${borda("#5a3a1c", "#8a5a2c", "#1f2a12")}; }
  .idn-sombra { ${faixas("#e2ddd2", "#c0b8a8", "#8a8070")} filter: ${borda("#2a1238", "#5a2a6e", "#08090a")} drop-shadow(0 0 0 #08090a); }
  .idn-almas { ${faixas("#f1fff8", "#c8ece6", "#74c4c9")} filter: ${borda("#2e5f63", "#74c4c9", "#1c1428")}; }
  .idn-sobre-fogo { color: #ffb35c !important; } .idn-sobre-luz { color: #f1e4c4 !important; } .idn-sobre-sangue { color: #e2574c !important; }
  .idn-sobre-folhas { color: #8fbf6a !important; } .idn-sobre-sombra { color: #a89878 !important; } .idn-sobre-almas { color: #74c4c9 !important; }
  @media (prefers-reduced-motion: reduce) { .idn-fogo { animation: none; } }`;
  document.head.insertAdjacentHTML("beforeend", `<style id="estilo-identidades">${css}</style>`);

  return { qual, PAL, CACOS, criar, contorno };
})();

/* PROTÓTIPO (24/10/2026; nada no jogo): IDENTIDADES, segunda rodada. Duas propostas para cada especialização que não
   é o Piromante (aprovado, em identidades.js), com símbolos e movimentos próprios; a mesma identidade serve às duas
   apresentações (Relicário e Estouro). Cada uma tem três tempos: a identidade aparece (antecipação), o nome é revelado
   com impacto, e o efeito se acomoda num nível mais baixo para a leitura. O nome termina parado e legível; os efeitos
   ficam atrás dele (o palco é desenhado por baixo do texto), num poço escuro, e não descem até a descrição.

     Paladino    1 · Luz do alto: um cone largo de luz desce e se abre sobre o nome; um anel claro no pouso; poeira
                     de luz; o nome sai incandescente e esfria para marfim.
                 2 · Asas: duas asas de penas se abrem atrás do nome, uma auréola acende; penas brancas caem pela
                     composição inteira.
     Berserker   1 · O nome sangra: respingos pintam o fundo; o sangue tinge as letras de cima para baixo e escorre
                     delas em fios que formam gotas, caem e empoçam sob o nome.
                 2 · Garras: o nome despenca e três garras rasgam o fundo; as feridas vertem; o sangue pinga das
                     letras; as bordas da tela batem como um coração.
     Patrulheiro 1 · Vendaval: uma rajada atravessa a composição inteira e revela o nome da esquerda para a direita,
                     levando folhas; outras rajadas voltam de tempos em tempos.
                 2 · Clareira: dois ramos crescem dos lados e abraçam o nome, brotando folhas; raios de sol entram
                     pela copa; folhas caem devagar.
     Sombra      1 · Corte: a lâmina corta o nome; as duas metades se separam e se recompõem; fica a cicatriz atrás.
                 2 · Invisível: no escuro, dois olhos; o nome aparece aos pedaços, uma letra falha e some antes de
                     firmar; de vez em quando, olhos nas laterais.
     Necromante  1 · Erguer: um círculo se desenha sob o nome e caveiras sobem dele, acendendo os olhos.
                 2 · Almas: almas com rosto chegam das bordas e entram nas letras, que clareiam a cada uma; três
                     ficam rondando o nome.

   Movimento reduzido: cada uma tem o seu quadro parado (o estado acomodado). */
"use strict";

const Identidades2 = (() => {
  const C = (l) => FX.cor(l);
  const pt = (x, y, n) => Sprites.pontilha(x, y, n);
  const sorteio = (l) => l[Math.floor(Math.random() * l.length)];
  const al = FX.aleatorio, rampa = FX.rampa;
  /** Uma grade desenhada à mão; `mapa` diz a cor (letra da paleta) de cada caractere; "." é vazio. */
  function pintar(p, g, ox, oy, mapa, e = 1) {  // e: a escala inteira (cada pixel do desenho, e × e texels)
    for (let y = 0; y < g.length; y++) for (let x = 0; x < g[y].length; x++) {
      const ch = g[y][x];
      if (ch === "." || !mapa[ch]) continue;
      const c = C(mapa[ch]);
      for (let j = 0; j < e; j++) for (let i = 0; i < e; i++) p.por(ox + x * e + i, oy + y * e + j, c);
    }
  }
  const espelho = (g) => g.map((l) => [...l].reverse().join(""));

  // ---------------------------------------------------------------- os desenhos (à mão, em texels)
  const PENA = [  // a pena caindo: em pé, inclinada, deitada (a ponta "q" é o cálamo)
    ["..o..", ".obo.", ".obo.", "obbo.", "obbo.", ".obo.", ".ob..", "..o..", "..q.."],
    ["....o", "...ob", "..obo", ".obo.", "obbo.", "obo..", "ob...", "q...."],
    [".ooooo..", "obbbbbbq", ".ooooo.."],
  ];
  const PENA_COR = { o: "w", b: "W", q: "c" };
  const FOLHA = [  // a folha girando no vento: deitada, inclinada para cima, de lado (fina), inclinada para baixo
    ["..ooo..", ".obbboo", "qmmmmmb", ".obbboo", "..ooo.."],
    [".....oo", "...obbo", "..obmb.", ".obmo..", "obmo...", "mo.....", "q......"],
    ["qmmmmmo"],
    null,
  ];
  FOLHA[3] = [...FOLHA[1]].reverse();
  const TOM_FOLHA = [  // a mesma folha em três luzes da mata (sem marrom)
    { o: "e", b: "E", m: "f", q: "f" }, { o: "f", b: "e", m: "E", q: "f" }, { o: "f", b: "E", m: "e", q: "f" },
  ];
  const CAVEIRA = [
    ".kkkkk.", "kbbbbbk", "kbbbbbk", "keebeek", "keebeek", "kbbkbbk", ".kbbbk.", ".kbkbk.", "..kkk..",
  ];
  const ALMA = [  // a alma: cabeça redonda, olhos e boca abertos, a barra rasgada
    "..ooo..", ".obbbo.", "obbbbbo", "obkbkbo", "obbbbbo", "obbkbbo", "obbbbbo", ".bobob.", "..o.o..",
  ];
  const OLHO = ["ooo"], OLHO_FECHADO = ["kok"];
  const RUNAS = [["a.a", ".a.", "a.a"], ["aaa", "a..", "aaa"], [".a.", "aaa", ".a."], ["a..", "aaa", "..a"]];

  // ---------------------------------------------------------------- o que todas usam
  /** O poço escuro logo atrás do nome (as letras leem sobre ele). */
  const poco = (p, r, folga = 18, forca = 16, c = "N") => FX.poco(p, { cx: r.x, cy: r.y, rx: r.rx + folga, ry: r.ry + Math.round(folga * 0.9), forca, c });
  /** Um enxame de partículas: cada uma pode ter `mover(s)` e `morre(s)`; senão anda por vx, vy e gravidade g. */
  function enxame() {
    const lista = [];
    return {
      lista,
      soltar(n, gerar) { for (let i = 0; i < n; i++) lista.push({ idade: 0, vx: 0, vy: 0, g: 0, ...gerar(i) }); },
      passo() {
        for (let i = lista.length - 1; i >= 0; i--) {
          const s = lista[i];
          s.idade++;
          if (s.mover) s.mover(s); else { s.x += s.vx; s.y += s.vy; s.vy += s.g; }
          if (s.idade > s.vida || (s.morre && s.morre(s))) lista.splice(i, 1);
        }
      },
    };
  }

  // ================================================================ PALADINO
  const LUZ = { pal: ["W", "w", "Y", "c", "C"], cacos: ["W", "w", "Y", "c", "C"] };
  /** O cone de luz: do alto da tela até o pouso, mais largo embaixo, com faixas verticais que respiram. */
  function cone(p, r, t, parado, forca = 1) {
    const base = r.base + 2, desce = parado ? 1 : rampa(t, 0, 380), fim = Math.round(base * desce);
    const wt = r.rx * 0.85, wb = r.rx * 1.9;
    for (let y = 0; y < fim; y++) {
      const v = y / base, w = wt + (wb - wt) * v;
      for (let x = Math.max(0, Math.floor(r.x - w)); x <= Math.min(p.W - 1, r.x + w); x++) {
        const dx = (x - r.x) / w, u = Math.abs(dx);
        const faixa = Math.sin(dx * 9 + (parado ? 0 : t / 1100)) > 0.35 ? 2 : 0;
        if (u > 0.94) { if (pt(x, y, Math.round(9 * forca))) p.por(x, y, C("c")); continue; }
        const n = Math.round((3.5 - u * 2.5 + faixa * 0.8 + v * 1.5) * forca);
        if (pt(x, y, n)) p.por(x, y, C(u < 0.3 && faixa ? "W" : u < 0.6 ? "w" : u < 0.85 ? "Y" : "c"));
      }
    }
  }
  /** A asa: penas em leque saindo de (px, py) para o lado `lado` (-1 esquerda, 1 direita); `abre` de 0 a 1. */
  function asa(p, px, py, lado, R, abre) {
    const n = 11;
    for (let i = n - 1; i >= 0; i--) {
      const f = i / (n - 1), alvo = (-12 + f * 92) * (Math.PI / 180), fechado = 86 * (Math.PI / 180);
      const a = fechado + (alvo - fechado) * abre, L = R * (0.62 + 0.38 * Math.sin(Math.PI * (0.25 + f * 0.6))) * (0.55 + 0.45 * abre);
      const dx = Math.cos(a) * lado, dy = -Math.sin(a), s0 = L * 0.22, larg = 3.4 + (1 - f) * 1.2;
      const xs = [px, px + dx * L], ys = [py, py + dy * L];
      const x0 = Math.floor(Math.min(...xs) - 4), x1 = Math.ceil(Math.max(...xs) + 4), y0 = Math.floor(Math.min(...ys) - 4), y1 = Math.ceil(Math.max(...ys) + 4);
      for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
        const rx = x - px, ry = y - py, s = rx * dx + ry * dy;
        if (s < s0 || s > L) continue;
        const d = -rx * dy + ry * dx, w = larg * Math.pow(Math.sin(Math.PI * (s - s0) / (L - s0)), 0.55);
        const ad = Math.abs(d * lado);
        if (ad > w + 1) continue;
        p.por(x, y, C(ad > w ? (d * lado > 0 ? "c" : "g") : ad < w * 0.35 ? "W" : "w"));
      }
    }
  }
  const penaCaindo = (x, y, lim, vy = al(0.25, 0.45)) => ({ tipo: "pena", x, y, x0: x, vy, vida: 260, fase: Math.random() * 6,
    mover: (s) => { s.y += s.vy; s.x = s.x0 + Math.sin(s.idade * 0.11 + s.fase) * 5; }, morre: (s) => s.y > lim });
  function desenharPena(p, s) {
    const k = Math.cos(s.idade * 0.11 + s.fase), g = Math.abs(k) < 0.35 ? PENA[0] : Math.abs(k) < 0.75 ? PENA[1] : PENA[2];
    pintar(p, k < 0 && g !== PENA[0] ? espelho(g) : g, Math.round(s.x) - (g[0].length >> 1), Math.round(s.y), PENA_COR);
  }
  const motes = (ex, r, n, t) => ex.soltar(n, () => ({ tipo: "mote", x: r.x + Math.round(al(-r.rx * 1.2, r.rx * 1.2)), y: Math.round(al(0, r.base)), vy: al(0.1, 0.3), vida: Math.round(al(25, 45)) }));

  const PALADINO = {
    a: {
      ...LUZ, atenua: 5, classe: "idv-luz-a",
      quadro({ p, r, t, q, parado, ex }) {
        cone(p, r, t, parado);
        poco(p, r, 16, 16);
        // o pouso: um anel claro que corre para fora, rente ao nome
        if (!parado && t > 360 && t < 900) {
          const u = (t - 360) / 540;
          FX.anel(p, { cx: r.x, cy: r.y, r: Math.round(r.rx * (0.9 + u * 0.6)), esp: 2, pal: ["W", "Y", "w"], achata: 0.32, rastro: 4, vis: Math.round(16 * (1 - u)) });
        }
        if (!parado) { if (q % 2 === 0) motes(ex, r, 1, t); if (q > 6 && q % 5 === 0) ex.soltar(1, () => ({ tipo: "brilho", x: r.x + Math.round(al(-r.rx, r.rx)), y: r.topo + Math.round(al(-2, 3)), vida: 6 })); }
      },
      desenhar(p, s) {
        if (s.tipo === "mote") { const k = s.idade / s.vida; if (pt(Math.round(s.x), Math.round(s.y), Math.round(14 * (1 - k)))) p.por(Math.round(s.x), Math.round(s.y), C(k < 0.5 ? "W" : "Y")); return; }
        pintar(p, s.idade < 2 || s.idade > 4 ? FX.DESENHOS.cruz : FX.DESENHOS.brilho, Math.round(s.x) - 3, Math.round(s.y) - 3, { a: "Y", b: "W" });
      },
    },
    b: {
      ...LUZ, atenua: 3, classe: "idv-luz-b",
      quadro({ p, r, t, q, parado, ex, dados }) {
        const abre = parado ? 1 : rampa(t, 60, 560), R = r.rx * 1.35;
        const px = r.x, py = r.topo + Math.round(r.ry * 0.4);
        // a luz atrás das asas
        FX.halo(p, { cx: px, cy: py, r: Math.round(R * 0.8), achata: 0.55, pal: ["w", "G", "g"], vis: parado ? 4 : Math.round(5 * abre) });
        asa(p, px - 3, py, -1, R, abre); asa(p, px + 3, py, 1, R, abre);
        poco(p, r, 14, 16);
        // a auréola acende quando as asas abrem
        if (parado || t > 520) {
          const vis = parado ? 14 : Math.min(16, Math.round((t - 520) / 25));
          FX.anel(p, { cx: r.x, cy: r.topo - 17, r: Math.round(r.ry * 1.6), esp: 1, pal: ["Y", "c", "C"], achata: 0.28, rastro: 1, vis });
        }
        if (parado) return;
        if (!dados.soltou && t > 560) {  // as penas soltas pelo bater das asas
          dados.soltou = true;
          ex.soltar(12, (i) => { const lado = i % 2 ? 1 : -1, x = r.x + lado * Math.round(al(r.rx * 0.5, R * 0.9));
            return penaCaindo(x, py - Math.round(al(5, R * 0.6)), r.base + 6, al(0.35, 0.6)); });
        }
        if (q % 5 === 0) ex.soltar(1, () => penaCaindo(r.x + Math.round(al(-r.rx * 1.6, r.rx * 1.6)), Math.round(al(-8, r.topo * 0.5)), r.base + 6));
      },
      desenhar(p, s) { desenharPena(p, s); },
      parado: 12,
    },
  };

  // ================================================================ BERSERKER
  const SANGUE = { pal: ["p", "R", "r", "D", "D"], cacos: ["R", "r", "D", "D", "k"] };
  /** Um fio que escorre da base de uma letra: cresce, forma a gota, a gota cai e empoça no chão. */
  function fio(x, y, chao, grosso = false) {
    return { tipo: "fio", x, y, chao, L: 0, Lmax: Math.round(al(4, 11)), grosso, vida: 160, gota: null };
  }
  function moverFio(s, dados) {
    if (!s.gota) {
      s.L += 0.4;
      if (s.L >= s.Lmax) s.gota = { y: s.y + s.L, vy: 0 };
    } else {
      s.gota.vy += 0.22; s.gota.y += s.gota.vy; s.L = Math.max(1, s.L - 0.15);
      if (s.gota.y >= s.chao) {  // empoça: o chão guarda a mancha
        for (let dx = -2 - (s.grosso ? 1 : 0); dx <= 2 + (s.grosso ? 1 : 0); dx++) dados.poca.set(s.x + dx, Math.min(3, (dados.poca.get(s.x + dx) || 0) + 1));
        dados.respingos.push({ x: s.x, y: s.chao, idade: 0 });
        return true;
      }
    }
    return false;
  }
  function desenharFio(p, s) {
    const L = Math.round(s.L);
    for (let i = 0; i < L; i++) { p.por(s.x, s.y + i, C(i === 0 ? "D" : "r")); p.por(s.x + 1, s.y + i, C(s.grosso ? "r" : "D")); if (s.grosso && i < L - 2) p.por(s.x - 1, s.y + i, C("D")); }
    const gy = s.gota ? Math.round(s.gota.y) : s.y + L - 1;
    pintar(p, ["..r..", ".rRr.", "rRpRr", "rRRRr", "rRRRr", ".rrr."], s.x - 2, gy, { r: "r", R: "R", p: "p" });  // a gota, com o brilho
  }
  function desenharChao(p, r, dados) {
    for (const [x, n] of dados.poca) { for (let k = 0; k < n; k++) p.por(x, dados.chao + 1 - k, C(k === n - 1 ? "r" : "D")); p.por(x, dados.chao + 2, C("k")); }
    for (let i = dados.respingos.length - 1; i >= 0; i--) {
      const s = dados.respingos[i]; s.idade++;
      if (s.idade > 4) { dados.respingos.splice(i, 1); continue; }
      p.por(s.x - 1 - s.idade, s.y - 1, C("R")); p.por(s.x + 1 + s.idade, s.y - 1, C("R")); if (s.idade < 2) p.por(s.x, s.y - 2, C("p"));
    }
  }
  /** As bases das letras (a tinta acaba indo para baixo), só na metade de baixo do nome. */
  const basesBaixas = (c, r) => c.bases.filter((o) => o.y > r.y);
  function iniciarSangue(r, dados) {
    if (dados.chao === undefined) { dados.chao = r.base + 3; dados.poca = new Map(); dados.respingos = []; dados.manchas = []; }
  }
  /** As bordas da tela batem como um coração (dois golpes e uma pausa); `forca` 0 a 1. */
  function veias(p, t, parado) {
    const fase = t % 1100, b = parado ? 0.45 : fase < 110 ? 1 : fase > 190 && fase < 290 ? 0.7 : 0.25, faixa = 26;
    for (let y = 0; y < p.H; y++) {
      const dy = Math.min(y, p.H - 1 - y);
      for (let x = 0; x < p.W; x++) {
        if (dy >= faixa && x >= faixa && x < p.W - faixa) { x = p.W - faixa - 1; continue; }
        const d = Math.min(dy, x, p.W - 1 - x);
        const n = Math.round((1 - d / faixa) * 10 * b);
        if (pt(x, y, n)) p.buf[y * p.W + x] = C(d < 6 ? "D" : "r");
      }
    }
  }
  /** As garras: três rasgos em diagonal atrás do nome, que se abrem em três quadros e ficam. */
  function garras(r) {
    return [-1, 0, 1].map((k) => {
      const x0 = r.x - 22 + k * 26, y0 = r.topo - 26 + Math.abs(k) * 4, x1 = r.x + 18 + k * 26, y1 = r.base + 8 - Math.abs(k) * 3;
      return { x0, y0, x1, y1, n: Math.round(Math.hypot(x1 - x0, y1 - y0)) };
    });
  }
  function desenharGarra(p, g, u) {
    const n = Math.round(g.n * u);
    for (let i = 0; i < n; i++) {
      const f = i / g.n, x = Math.round(g.x0 + (g.x1 - g.x0) * f), y = Math.round(g.y0 + (g.y1 - g.y0) * f);
      const w = Math.round(4 * Math.sin(Math.PI * f));  // o rasgo: fino nas pontas, aberto no meio
      for (let d = -w - 1; d <= w + 1; d++) p.por(x + d, y, C(d === -w - 1 ? "p" : d === w + 1 ? "D" : Math.abs(d) <= w - 1 ? "k" : "R"));
    }
  }
  const BERSERKER = {
    a: {
      ...SANGUE, atenua: 3, classe: "idv-sangue-a",
      quadro({ p, r, c, t, q, parado, ex, dados }) {
        iniciarSangue(r, dados);
        // os respingos da entrada pintam o fundo em volta do nome e ficam
        for (const m of dados.manchas) FX.halo(p, { cx: m.x, cy: m.y, r: m.r, pal: ["r", "D", "D"], vis: 12 });
        poco(p, r, 12, 16);
        desenharChao(p, r, dados);
        if (!parado && q === 2) ex.soltar(34, () => { const a = al(-Math.PI * 0.95, -Math.PI * 0.05) + (Math.random() < 0.3 ? Math.PI : 0), v = al(3, 7);
          return { tipo: "respingo", x: r.x + al(-r.rx * 0.6, r.rx * 0.6), y: r.y, vx: Math.cos(a) * v * 1.6, vy: Math.sin(a) * v, g: 0.45, vida: Math.round(al(8, 14)),
            morre: (s) => { if (s.idade === s.vida) dados.manchas.push({ x: Math.round(s.x), y: Math.round(s.y), r: Math.round(al(1, 3)) }); return false; } }; });
        const bases = basesBaixas(c, r);
        if (bases.length && (parado || t > 420) && !parado) ex.soltar(q % 3 === 0 ? 2 : 1, () => { const o = sorteio(bases); return { ...fio(o.x, o.y, dados.chao, Math.random() < 0.3) }; });
      },
      mover(s, dados) { return s.tipo === "fio" ? moverFio(s, dados) : null; },
      desenhar(p, s) {
        if (s.tipo === "fio") return desenharFio(p, s);
        p.por(Math.round(s.x), Math.round(s.y), C("R")); p.por(Math.round(s.x - s.vx * 0.4), Math.round(s.y - s.vy * 0.4), C("r"));
      },
      parado: 18,
    },
    b: {
      ...SANGUE, atenua: 4, classe: "idv-sangue-b",
      quadro({ p, r, c, t, q, parado, ex, dados }) {
        iniciarSangue(r, dados);
        veias(p, t, parado);
        if (!dados.garras) dados.garras = garras(r);
        poco(p, r, 10, 16);
        const u = parado ? 1 : rampa(t, 170, 200);
        if (u > 0) dados.garras.forEach((g, i) => desenharGarra(p, g, Math.min(1, u * 1.3 - i * 0.15)));
        desenharChao(p, r, dados);
        if (parado) return;
        // as feridas vertem pela borda de baixo
        if (t > 400 && q % 2 === 0) ex.soltar(1, () => { const g = sorteio(dados.garras), f = al(0.15, 0.85);
          return { tipo: "verte", x: Math.round(g.x0 + (g.x1 - g.x0) * f) + 2, y: Math.round(g.y0 + (g.y1 - g.y0) * f) + 2, g: 0.2, vy: 0, vida: 14 }; });
        const bases = basesBaixas(c, r);
        if (bases.length && t > 450 && q % 2 === 1) ex.soltar(1, () => { const o = sorteio(bases); return fio(o.x, o.y, dados.chao, true); });
      },
      mover(s, dados) { return s.tipo === "fio" ? moverFio(s, dados) : null; },
      desenhar(p, s) {
        if (s.tipo === "fio") return desenharFio(p, s);
        pintar(p, [".r.", "rRr", ".r."], Math.round(s.x) - 1, Math.round(s.y), { r: "r", R: "R" });
      },
      parado: 14,
    },
  };

  // ================================================================ PATRULHEIRO
  const MATA = { pal: ["W", "E", "e", "f", "f"], cacos: ["E", "e", "f", "f", "f"] };
  /** Uma folha levada pelo vento da esquerda para a direita, atravessando a composição inteira. */
  const folhaNoVento = (r, p, x, y, vx) => ({ tipo: "folha", x, y, y0: y, vx, vida: 400, fase: Math.random() * 6, tom: Math.floor(Math.random() * 3), e: Math.random() < 0.4 ? 2 : 1,
    giro: al(0.25, 0.45), mover: (s) => { s.x += s.vx; s.y = s.y0 + Math.sin(s.idade * 0.3 + s.fase) * 4 + s.idade * 0.04; },
    morre: (s) => s.x > Math.min(p.W - 2, r.dir + p.t(220)) });
  function desenharFolha(p, s) {
    const g = FOLHA[Math.floor(s.idade * s.giro + s.fase) % 4], e = s.e || 1;
    pintar(p, g, Math.round(s.x) - 3 * e, Math.round(s.y) - (g.length >> 1) * e, TOM_FOLHA[s.tom], e);
  }
  const risco = (r, p, y) => ({ tipo: "risco", x: r.esq - p.t(260), y, vx: 13, vida: 400, larg: Math.round(al(12, 26)), morre: (s) => s.x - s.larg > r.dir + p.t(260) });
  function desenharRisco(p, s) { for (let i = 0; i < s.larg; i++) if (pt(Math.round(s.x) - i, s.y, Math.round(12 - (i / s.larg) * 10))) p.por(Math.round(s.x) - i, s.y, C(i < 3 ? "T" : "t")); }
  /** O ramo: um caminho que sai de baixo, ao lado do nome, e se curva por cima dele (pontos em texels). */
  function ramo(r, lado) {
    const pts = [], x0 = lado < 0 ? r.esq - 40 : r.dir + 40, y0 = r.y + 6, x1 = lado < 0 ? r.esq + r.rx * 0.5 : r.dir - r.rx * 0.5, y1 = r.topo - 12;
    const cx = lado < 0 ? r.esq - 22 : r.dir + 22, cy = r.topo - 22;
    for (let i = 0; i <= 80; i++) { const u = i / 80, x = (1 - u) * (1 - u) * x0 + 2 * (1 - u) * u * cx + u * u * x1, y = (1 - u) * (1 - u) * y0 + 2 * (1 - u) * u * cy + u * u * y1; pts.push([Math.round(x), Math.round(y)]); }
    return pts;
  }
  function desenharRamo(p, pts, u, q, parado, lado) {
    const n = Math.round(pts.length * u);
    for (let i = 0; i < n; i++) { const [x, y] = pts[i], grosso = i < pts.length * 0.6; p.por(x, y, C("f")); p.por(x, y - 1, C("e")); if (grosso) p.por(x, y + 1, C("f")); }
    for (let i = 17; i < n; i += 9) {  // as folhas brotam ao longo do ramo, alternando os lados
      const [x, y] = pts[i], cima = (i / 9) % 2 === 0, mexe = parado ? 0 : ((q + i) >> 3) % 2;
      const g = mexe ? FOLHA[1] : FOLHA[0];
      pintar(p, lado < 0 ? g : espelho(g), x - 6, cima ? y - 11 : y + 1, TOM_FOLHA[(i / 9) % 3 | 0], 2);
    }
  }
  const PATRULHEIRO = {
    a: {
      ...MATA, atenua: 4, classe: "idv-folhas-a",
      quadro({ p, r, t, q, parado, ex }) {
        poco(p, r, 16, 15);
        if (parado) return;
        // a primeira rajada (revela o nome) e uma nova a cada 2,6 s
        const rajada = t < 1100 || (t - 1100) % 2600 < 700, forte = t < 1100;
        if (rajada) {
          ex.soltar(forte ? 3 : 1, () => folhaNoVento(r, p, r.esq - p.t(al(140, 260)), r.y + Math.round(al(-r.ry * 2.4, r.ry * 1.2)), al(7, 11)));
          if (q % 2 === 0) ex.soltar(1, () => risco(r, p, r.y + Math.round(al(-r.ry * 2.2, r.ry * 1.4))));
        } else if (q % 6 === 0) ex.soltar(1, () => folhaNoVento(r, p, r.esq - p.t(200), r.y + Math.round(al(-r.ry * 2, r.ry)), al(4, 6)));
      },
      desenhar(p, s) { if (s.tipo === "risco") desenharRisco(p, s); else desenharFolha(p, s); },
      parado: 16,
      // o quadro parado: folhas espalhadas pela largura toda
      preparar(ex, r, p) { for (let i = 0; i < 16; i++) ex.soltar(1, () => ({ ...folhaNoVento(r, p, r.esq - 30 + Math.round((i / 15) * (r.dir - r.esq + 60)), r.y + Math.round(al(-r.ry * 2.2, r.ry)), 0), idade: Math.floor(Math.random() * 8) })); },
    },
    b: {
      ...MATA, atenua: 5, classe: "idv-folhas-b",
      quadro({ p, r, t, q, parado, ex, dados }) {
        // os raios de sol entrando pela copa, do alto à esquerda
        const sol = parado ? 4 : t < 500 ? Math.round(rampa(t, 150, 350, 0, 4)) : t < 900 ? 8 : 4 + ((q >> 3) % 2);
        FX.feixes(p, { cx: r.x - r.rx * 1.6, cy: -60, angs: [0.66, 0.74, 0.83, 0.92, 1.0], meia: 0.022, r1: r.base + 140, pal: ["Y", "E", "E", "e"], vis: sol, esbate: 0.6 });
        poco(p, r, 14, 16);
        if (!dados.ramos) dados.ramos = [ramo(r, -1), ramo(r, 1)];
        const cresce = parado ? 1 : rampa(t, 0, 620);
        desenharRamo(p, dados.ramos[0], cresce, q, parado, -1); desenharRamo(p, dados.ramos[1], cresce, q, parado, 1);
        if (!parado && q % 4 === 0) ex.soltar(1, () => { const x = r.x + Math.round(al(-r.rx * 1.6, r.rx * 1.6));
          return { tipo: "folha", x, y: Math.round(al(-6, r.topo - 20)), x0: x, vida: 140, fase: Math.random() * 6, tom: Math.floor(Math.random() * 3), giro: 0.2, e: Math.random() < 0.5 ? 2 : 1,
            mover: (s) => { s.y += 0.45; s.x = s.x0 + Math.sin(s.idade * 0.12 + s.fase) * 7; }, morre: (s) => s.y > r.base + 20 }; });
      },
      desenhar(p, s) { desenharFolha(p, s); },
      parado: 10,
    },
  };

  // ================================================================ SOMBRA
  const SOMBRA = { pal: ["G", "m", "x", "K", "k"], cacos: ["G", "g", "x", "K", "k"] };
  const fumo = (x, y, vx, vy) => ({ tipo: "fumo", x, y, vx, vy, vida: Math.round(al(16, 28)), tam: Math.random() < 0.5 ? 2 : 1 });
  function desenharFumo(p, s) {
    const k = s.idade / (s.vida + 1), cor = C(k < 0.3 ? "g" : k < 0.65 ? "x" : "K"), t = s.tam + (k > 0.4 ? 1 : 0) + (k > 0.75 ? 1 : 0);
    for (let y = 0; y <= t; y++) for (let x = 0; x <= t; x++) if (pt(Math.round(s.x) + x, Math.round(s.y) + y, Math.round(13 * (1 - k)))) p.por(Math.round(s.x) + x, Math.round(s.y) + y, cor);
  }
  /** A linha do corte, a mesma diagonal do recorte das metades do nome (de 78% embaixo à esquerda a 30% em cima à
   *  direita), estendida para fora do nome. */
  const linhaCorte = (r) => { const h = r.base - r.topo, ya = r.topo + h * 0.78, yb = r.topo + h * 0.3, m = (yb - ya) / (r.dir - r.esq);
    return { x0: r.esq - 46, y0: ya - 46 * m, x1: r.dir + 46, y1: yb + 46 * m }; };
  function desenharLinha(p, l, u, cores, larg = 1, de = 0) {
    const n = Math.round(Math.hypot(l.x1 - l.x0, l.y1 - l.y0));
    for (let i = Math.round(n * de); i < Math.round(n * u); i++) {
      const x = Math.round(l.x0 + ((l.x1 - l.x0) * i) / n), y = Math.round(l.y0 + ((l.y1 - l.y0) * i) / n);
      for (let d = -larg; d <= larg; d++) p.por(x, y + d, C(d === 0 ? cores[0] : cores[1]));
    }
  }
  const SOMBRA_ID = {
    a: {
      ...SOMBRA, atenua: 7, classe: "idv-sombra-a", semClarao: true,
      nome(el) {  // as duas metades do nome, recortadas na diagonal, que se separam no corte e voltam
        const t = el.textContent;
        el.innerHTML = `<span class="idv-camada idv-cima">${t}</span><span class="idv-camada idv-baixo" aria-hidden="true">${t}</span>`;
        return el.querySelector(".idv-cima");
      },
      quadro({ p, r, t, q, parado, ex, dados }) {
        poco(p, r, 30, 16);
        const l = dados.l || (dados.l = linhaCorte(r));
        if (parado || t > 330) desenharLinha(p, l, 1, ["x", "K"], 0);  // a cicatriz que fica
        if (!parado && t >= 230 && t < 360) desenharLinha(p, l, Math.min(1, (t - 230) / 60), ["W", "G"], 1);  // o golpe: dois quadros
        if (!parado && t >= 290 && t < 520) desenharLinha(p, l, 1, ["G", "m"], 1, 0.15);
        if (parado) return;
        if (!dados.golpe && t >= 290) {
          dados.golpe = true;
          for (const [x, y] of [[l.x0, l.y0], [l.x1, l.y1]]) ex.soltar(8, () => ({ tipo: "faisca", x, y, vx: al(-2.5, 2.5), vy: al(-2.5, 1.5), g: 0.2, vida: Math.round(al(5, 9)) }));
          ex.soltar(26, () => { const f = Math.random(); return fumo(l.x0 + (l.x1 - l.x0) * f, l.y0 + (l.y1 - l.y0) * f, al(-0.8, 0.8), al(-1, 0.3)); });
        }
        // o brilho que corre pela cicatriz a cada 3 s, só nas pontas de fora do nome
        const cg = (t - 1400) % 3000;
        if (t > 1400 && cg < 500) { const f = cg / 500, x = l.x0 + (l.x1 - l.x0) * f, y = l.y0 + (l.y1 - l.y0) * f;
          if (x < r.esq - 2 || x > r.dir + 2) pintar(p, FX.DESENHOS.cruz, Math.round(x) - 1, Math.round(y) - 1, { a: "G", b: "W" }); }
        if (t > 700 && q % 3 === 0) ex.soltar(1, () => { const lado = Math.random() < 0.5 ? -1 : 1; return fumo(lado < 0 ? r.esq - 2 : r.dir + 2, r.y + al(-r.ry, r.ry), lado * al(0.4, 1), al(-0.5, -0.1)); });
      },
      desenhar(p, s) {
        if (s.tipo === "faisca") { p.por(Math.round(s.x), Math.round(s.y), C(s.idade < 3 ? "W" : "G")); return; }
        desenharFumo(p, s);
      },
      parado: 12,
    },
    b: {
      ...SOMBRA, atenua: 8, classe: "idv-sombra-b", semClarao: true,
      nome(el) {  // as letras aparecem aos pedaços, cada uma no seu tempo; uma falha e some antes de firmar
        const letras = [...el.textContent], ordem = letras.map((_, i) => i).sort(() => Math.random() - 0.5), falha = ordem[Math.floor(letras.length / 2)];
        el.innerHTML = letras.map((ch, i) => `<span class="idv-letra${i === falha ? " idv-falha" : ""}" style="--d:${(0.42 + (ordem.indexOf(i) / letras.length) * 0.55).toFixed(2)}s">${ch}</span>`).join("");
        el.setAttribute("aria-label", letras.join(""));
        return el;
      },
      quadro({ p, r, t, q, parado, ex, dados }) {
        FX.poco(p, { cx: r.x, cy: r.y, rx: Math.round(r.rx * 1.7), ry: Math.round(r.ry * 4), forca: 15 });
        poco(p, r, 16, 16);
        // os olhos: no meio, antes do nome; depois, de vez em quando, nas laterais do escuro
        const olhos = (x, y, fechado) => { pintar(p, fechado ? OLHO_FECHADO : OLHO, x - 10, y, { o: "Y", k: "k" }, 2); pintar(p, fechado ? OLHO_FECHADO : OLHO, x + 4, y, { o: "Y", k: "k" }, 2); };
        if (!parado && t < 480) olhos(r.x, r.y - 2, t > 300 && t < 360);
        if (!dados.lado) dados.lado = { x: r.esq - 34, y: r.y - 6 };
        const cl = (t - 1600) % 3200;
        if (parado) { olhos(r.esq - 34, r.y - 6, false); olhos(r.dir + 34, r.y + 2, true); }
        else if (t > 1600 && cl < 900) { if (cl < 30) dados.lado = Math.random() < 0.5 ? { x: r.esq - Math.round(al(26, 46)), y: r.y + Math.round(al(-10, 6)) } : { x: r.dir + Math.round(al(26, 46)), y: r.y + Math.round(al(-10, 6)) };
          olhos(dados.lado.x, dados.lado.y, cl > 420 && cl < 500); }
        if (parado) return;
        // a névoa: espessa sobre o nome no começo, sai para fora enquanto as letras aparecem
        if (t < 900 && q % 1 === 0) ex.soltar(t < 400 ? 4 : 2, () => fumo(r.x + al(-r.rx, r.rx), r.y + al(-r.ry, r.ry), al(-1.2, 1.2), al(-0.6, 0.4)));
        else if (q % 3 === 0) ex.soltar(1, () => { const lado = Math.random() < 0.5 ? -1 : 1; return fumo(lado < 0 ? r.esq - 4 : r.dir + 4, r.y + al(-r.ry, r.ry), lado * al(0.3, 0.8), al(-0.4, 0)); });
      },
      desenhar(p, s) { desenharFumo(p, s); },
      parado: 14,
    },
  };

  // ================================================================ NECROMANTE
  const TUMULO = { pal: ["E", "e", "f", "f", "N"], cacos: ["E", "e", "f", "K", "k"] };
  function circulo(p, r, t, parado, q) {
    const cy = r.base - 2, rx = Math.round(r.rx * 1.12), u = parado ? 1 : rampa(t, 0, 420), n = 120;
    for (let i = 0; i < Math.round(n * u); i++) { const a = (i / n) * Math.PI * 2, x = r.x + Math.round(Math.cos(a) * rx), y = cy + Math.round(Math.sin(a) * rx * 0.12);
      p.por(x, y, C(Math.sin(a) > 0 ? "e" : "f")); }
    const passo = parado ? 0 : Math.floor(t / 300) * 0.1;
    if (u >= 1) for (let i = 0; i < 10; i++) { const a = passo + (i / 10) * Math.PI * 2, x = r.x + Math.round(Math.cos(a) * rx), y = cy + Math.round(Math.sin(a) * rx * 0.12);
      pintar(p, RUNAS[i % 4], x - 1, y - 1, { a: Math.sin(a) > 0 ? ((q + i) % 9 === 0 ? "E" : "e") : "f" }); }
  }
  const NECROMANTE = {
    a: {
      ...TUMULO, atenua: 4, classe: "idv-almas-a", semClarao: true,
      quadro({ p, r, t, q, parado, ex, dados, semFundo }) {
        if (!semFundo) FX.poco(p, { cx: r.x, cy: r.y, rx: Math.round(r.rx * 1.6), ry: Math.round(r.ry * 4), forca: 12, c: "N" });
        if (!dados.caveiras) dados.caveiras = Array.from({ length: 6 }, (_, i) => {
          const f = i / 5, x = Math.round(r.esq - 30 + f * (r.dir - r.esq + 60)), alto = r.topo - 26 - Math.round(Math.sin(Math.PI * f) * 16);
          return { x, alto, de: 220 + [3, 1, 5, 0, 4, 2][i] * 110 };
        });
        // as caveiras sobem do círculo para o arco acima do nome e acendem os olhos ao chegar
        for (const [i, k] of dados.caveiras.entries()) {
          const u = parado ? 1 : rampa(t, k.de, 420);
          if (u <= 0) continue;
          const y = Math.round(r.base - 2 + (k.alto - (r.base - 2)) * u) + (u >= 1 && !parado ? ((q + i * 3) >> 3) % 2 : 0);
          const aceso = u >= 1, pisca = !parado && aceso && (q + i * 11) % 47 === 0;
          pintar(p, CAVEIRA, k.x - 7, y, { k: "k", b: "G", e: aceso && !pisca ? (t - k.de < 520 ? "W" : "E") : "k" }, 2);
          if (u < 1) for (let w = 1; w < 12; w++) if (pt(k.x, y + 18 + w, 14 - w)) p.por(k.x + (w % 2 ? -1 : 1), y + 18 + w, C("e"));  // o rastro de quem sobe
        }
        if (!semFundo) poco(p, r, 12, 16);
        circulo(p, r, t, parado, q);
        if (!parado && t > 500 && q % 2 === 0) ex.soltar(1, () => ({ tipo: "fio", x: r.x + Math.round(al(-r.rx, r.rx)), y: r.base - 2, vy: al(-0.8, -0.4), vida: Math.round(al(10, 18)) }));
      },
      desenhar(p, s) { const k = s.idade / s.vida; for (let i = 0; i < 3; i++) if (pt(Math.round(s.x), Math.round(s.y) + i, Math.round(12 * (1 - k)) - i * 3)) p.por(Math.round(s.x), Math.round(s.y) + i, C(i === 0 && k < 0.4 ? "E" : "e")); },
      parado: 8,
    },
    b: {
      ...TUMULO, atenua: 5, classe: "idv-almas-b", semClarao: true,
      quadro({ p, r, c, t, q, parado, ex, dados }) {
        FX.poco(p, { cx: r.x, cy: r.y, rx: Math.round(r.rx * 1.8), ry: Math.round(r.ry * 4.5), forca: 13, c: "N" });
        poco(p, r, 14, 16);
        // as que ficam: três almas rondando o nome numa elipse (atrás quando passam por cima)
        const ronda = parado ? 1 : rampa(t, 1100, 500);
        if (ronda > 0) for (let i = 0; i < 3; i++) {
          const a = (parado ? 0.6 : t / 1900) + (i / 3) * Math.PI * 2, x = r.x + Math.cos(a) * r.rx * 1.3, y = r.y - 8 + Math.sin(a) * r.ry * 1.3;
          const frente = Math.sin(a) > 0;
          pintar(p, Math.cos(a) > 0 ? ALMA : espelho(ALMA), Math.round(x) - 7, Math.round(y) - 9, frente ? { o: "e", b: "E", k: "k" } : { o: "f", b: "e", k: "k" }, 2);
        }
        if (parado || !c.todos.length) return;
        // as que chegam: das bordas da tela, em curva, entram nas letras
        if (!dados.chamou) {
          dados.chamou = true;
          ex.soltar(10, (i) => { const alvo = sorteio(c.topos.length ? c.topos : c.todos), lado = i % 2 ? 1 : -1;
            const x0 = lado < 0 ? -10 : p.W + 10, y0 = Math.round(al(10, p.H * 0.7)), de = i * 2, dur = Math.round(al(14, 20));
            return { tipo: "alma", x: x0, y: y0, x0, y0, alvo, de, dur, vida: de + dur + 4, rastro: [],
              mover: (s) => { const u = Math.max(0, (s.idade - s.de) / s.dur); if (u <= 0) return;
                s.rastro.unshift([s.x, s.y]); if (s.rastro.length > 5) s.rastro.pop();
                const e = Math.min(1, u), cx = (s.x0 + s.alvo.x) / 2, cy = Math.min(s.y0, s.alvo.y) - 40;
                s.x = (1 - e) * (1 - e) * s.x0 + 2 * (1 - e) * e * cx + e * e * s.alvo.x; s.y = (1 - e) * (1 - e) * s.y0 + 2 * (1 - e) * e * cy + e * e * s.alvo.y; } }; });
        }
      },
      desenhar(p, s) {
        if (s.idade < s.de) return;
        const u = (s.idade - s.de) / s.dur;
        s.rastro.forEach(([x, y], i) => { if (pt(Math.round(x), Math.round(y), 12 - i * 2)) p.por(Math.round(x), Math.round(y), C(i < 2 ? "E" : "e")); });
        if (u >= 1) { pintar(p, FX.DESENHOS.brilho, Math.round(s.x) - 3, Math.round(s.y) - 3, { a: "E", b: "W" }); return; }  // entrou na letra
        pintar(p, s.x < s.alvo.x ? ALMA : espelho(ALMA), Math.round(s.x) - 7, Math.round(s.y) - 9, { o: "e", b: "E", k: "k" }, 2);
      },
      parado: 0,
    },
  };

  // ================================================================ AS CANDIDATAS FINAIS (versão "c", 24/10/2026)
  // As direções escolhidas pelo Jean, refinadas: o Paladino com a luz do alto em faixas amplas e as penas caindo; o
  // Berserker das garras com o sangue líquido; a Sombra do invisível com o corte; o Patrulheiro do vendaval em verde;
  // o Necromante das caveiras com a fumaça escura saindo das letras.

  // ---- PALADINO: a luz sagrada numa camada própria, translúcida (faixas amplas de marfim e ouro pálido, poucos níveis,
  // pontilhado só nas transições, sem contorno nem base reta) e as penas caindo devagar
  const hash = (n) => { const x = Math.sin(n * 127.1) * 43758.5453; return x - Math.floor(x); };
  const FAIXAS = [  // ângulo a partir da vertical, meia abertura, cor
    [-0.33, 0.05, "#fff1d6"], [-0.2, 0.075, "#f2cf8a"], [-0.07, 0.05, "#fff1d6"], [0.05, 0.085, "#f2cf8a"], [0.18, 0.05, "#fff1d6"], [0.31, 0.065, "#f2cf8a"],
  ];
  function luzSagrada(lp, r, t, parado, rot) {
    const ox = r.x, oy = -lp.t(260), desce = parado ? 1 : rampa(t, 0, 460), fundo = r.base - 2;
    const x0 = Math.max(0, Math.floor(r.x - r.rx * 2.4)), x1 = Math.min(lp.W - 1, Math.ceil(r.x + r.rx * 2.4));
    const mexe = (i) => (parado ? 0 : Math.sin(t / 2700 + i * 1.7) * 0.012);
    for (let y = 0; y < Math.min(lp.H, Math.round(fundo * desce) + 16); y++) for (let x = x0; x <= x1; x++) {
      // o pé de cada coluna é irregular e apaga em pontilhado (sem base reta)
      const pe = fundo - Math.round(hash(x >> 2) * 10), falta = pe - y;
      if (falta < -12) continue;
      // o nome e o rótulo ficam no escuro: a luz contorna os dois
      const ex = (x - r.x) / (r.rx + 16), ey = (y - r.y) / (r.ry + 14), dn = ex * ex + ey * ey;
      if (dn < 1) continue;
      if (rot) { const lx = (x - rot.x) / (rot.rx + 12), ly = (y - rot.y) / (rot.ry + 6); if (lx * lx + ly * ly < 1) continue; }
      const a = Math.atan2(x - ox, y - oy);
      let cor = null, n = 0;
      for (let i = 0; i < FAIXAS.length; i++) {
        const [ai, wi, ci] = FAIXAS[i], d = Math.abs(a - ai - mexe(i));
        if (d > wi) continue;
        n++;
        if (!cor || d < wi * 0.6) cor = ci;
        if (d > wi * 0.78 && !pt(x, y, 8)) { n--; if (n === 0) cor = null; }  // a borda da faixa: um pontilhado só
      }
      if (!cor) continue;
      if (falta < 0 && !pt(x, y, Math.round(14 + falta))) continue;  // o pé apagando
      if (dn < 1.2 && !pt(x, y, 9)) continue;  // a transição para o escuro em volta do nome
      lp.por(x, y, C(n > 1 ? "#fffbe6" : cor));
    }
    // a camada inteira respira devagar (poucos níveis de transparência)
    const op = parado ? 0.5 : t < 700 ? 0.5 + Math.round(6 * (1 - t / 700)) * 0.02 : 0.47 + Math.round(2 + 2 * Math.sin(t / 1100)) * 0.01;
    lp.el.style.opacity = op.toFixed(2);
  }
  PALADINO.c = {
    ...LUZ, pal: ["W", "w", "Y", "w", "G"], atenua: 9, classe: "idv-luz-a", semClarao: true, claros: ["W", "w"],
    luz: luzSagrada,
    quadro({ p, r, t, q, parado, ex, dados }) {
      poco(p, r, 16, 16);
      if (!parado && t > 380 && t < 920) {  // o pouso da luz: um anel de marfim rente ao nome
        const u = (t - 380) / 540;
        FX.anel(p, { cx: r.x, cy: r.y, r: Math.round(r.rx * (0.9 + u * 0.55)), esp: 1, pal: ["W", "w", "G"], achata: 0.3, rastro: 3, vis: Math.round(13 * (1 - u)) });
      }
      if (parado) return;
      if (!dados.soltou && t > 300) {  // as primeiras penas, soltas quando a luz chega
        dados.soltou = true;
        ex.soltar(9, () => penaCaindo(r.x + Math.round(al(-r.rx * 1.7, r.rx * 1.7)), Math.round(al(-10, r.topo * 0.6)), r.base + 6, al(0.3, 0.5)));
      }
      if (q % 6 === 0) ex.soltar(1, () => penaCaindo(r.x + Math.round(al(-r.rx * 1.9, r.rx * 1.9)), -8, r.base + 6));
      if (q % 3 === 0) motes(ex, r, 1, t);
    },
    desenhar(p, s) {
      if (s.tipo === "pena") return desenharPena(p, s);
      const k = s.idade / s.vida; if (pt(Math.round(s.x), Math.round(s.y), Math.round(12 * (1 - k)))) p.por(Math.round(s.x), Math.round(s.y), C(k < 0.5 ? "W" : "w"));
    },
    parado: 10,
  };

  // ---- BERSERKER: as garras e o ritmo da identidade 2, com o sangue líquido: acumula em pontos das letras, estica num
  // fio fino, se desprende e cai; poucas gotas ao mesmo tempo, cada uma no seu tempo; vermelho fundo, quase sem brilho
  // a gota: corpo vermelho fundo, um só ponto de luz (sem rosado); presa ela é curta, caindo se alonga
  const GOTA_PRESA = [".b.", "bcb", "bbb", ".b."], GOTA_CAINDO = [".b.", "bcb", "bbb", "bbb", ".b."];
  const COR_GOTA = { b: "r", c: "R" };
  function pontosDeSangue(c, r) {
    const bases = basesBaixas(c, r).sort((m, n) => m.x - n.x);
    if (!bases.length) return null;
    const n = 7, pts = [];
    for (let i = 0; i < n; i++) { const o = bases[Math.min(bases.length - 1, Math.floor(((i + al(0.2, 0.8)) / n) * bases.length))];
      pts.push({ x: o.x, y: o.y + 1, estado: "espera", ate: 300 + Math.round(al(0, 1700)), L: 0, Lmax: 0, inchaco: 0, gy: 0, vy: 0 }); }
    return pts;
  }
  function moverSangue(pt0, t, dados) {
    const s = pt0;
    if (s.estado === "espera") { if (t >= s.ate) { s.estado = "acumula"; s.inchaco = 0; s.Lmax = Math.round(al(5, 15)); s.lenta = al(0.18, 0.4); } return; }
    if (s.estado === "acumula") { s.inchaco += 0.08; if (s.inchaco >= 1) { s.estado = "estica"; s.L = 1; } return; }
    if (s.estado === "estica") { s.L += s.lenta; s.lenta *= 1.04; if (s.L >= s.Lmax) { s.estado = "cai"; s.gy = s.y + s.L; s.vy = 0.6; } return; }
    if (s.estado === "cai") {
      s.vy += 0.32; s.gy += s.vy; s.L = Math.max(0, s.L - 1.5);  // o fio volta para a letra
      if (s.gy >= dados.chao) {
        dados.poca.set(s.x, Math.min(2, (dados.poca.get(s.x) || 0) + 1)); dados.poca.set(s.x + 1, Math.min(2, (dados.poca.get(s.x + 1) || 0) + 1));
        dados.respingos.push({ x: s.x, y: dados.chao, idade: 0 });
        s.estado = "espera"; s.ate = t + Math.round(al(500, 2200));
      }
    }
  }
  function desenharSangue(p, s) {
    if (s.estado === "espera") return;
    if (s.estado === "acumula") {  // o sangue junta embaixo da letra: uma lâmina que engrossa e vira gota
      p.por(s.x - 1, s.y, C("r")); p.por(s.x, s.y, C("r")); p.por(s.x + 1, s.y, C("D"));
      if (s.inchaco > 0.4) p.por(s.x, s.y + 1, C("r"));
      if (s.inchaco > 0.75) pintar(p, GOTA_PRESA, s.x - 1, s.y, COR_GOTA);
      return;
    }
    const L = Math.round(s.L);
    for (let i = 0; i < L; i++) p.por(s.x, s.y + i, C("r"));  // o fio: fino, mais grosso junto da letra
    if (L > 1) { p.por(s.x + 1, s.y, C("r")); p.por(s.x - 1, s.y, C("D")); }
    if (s.estado === "estica") pintar(p, GOTA_PRESA, s.x - 1, s.y + L - 1, COR_GOTA);
    else pintar(p, s.vy > 2 ? GOTA_CAINDO : GOTA_PRESA, s.x - 1, Math.round(s.gy), COR_GOTA);
  }
  function chaoFundo(p, dados) {
    for (const [x, n] of dados.poca) for (let k = 0; k < n; k++) p.por(x, dados.chao + 1 - k, C(k === n - 1 ? "r" : "D"));
    for (let i = dados.respingos.length - 1; i >= 0; i--) {
      const s = dados.respingos[i]; s.idade++;
      if (s.idade > 3) { dados.respingos.splice(i, 1); continue; }
      p.por(s.x - 1 - s.idade, s.y - 1, C("r")); p.por(s.x + 1 + s.idade, s.y - 1, C("r"));
    }
  }
  BERSERKER.c = {
    ...SANGUE, atenua: 4, classe: "idv-sangue-b",
    quadro({ p, r, c, t, q, parado, ex, dados }) {
      iniciarSangue(r, dados);
      veias(p, t, parado);
      if (!dados.garras) dados.garras = garras(r);
      poco(p, r, 10, 16);
      const u = parado ? 1 : rampa(t, 170, 200);
      if (u > 0) dados.garras.forEach((g, i) => desenharGarra(p, g, Math.min(1, u * 1.3 - i * 0.15)));
      chaoFundo(p, dados);
      if (!dados.pontos && c.bases.length) dados.pontos = pontosDeSangue(c, r);
      if (dados.pontos) for (const s of dados.pontos) { if (!parado) moverSangue(s, t, dados); desenharSangue(p, s); }
      // as feridas das garras vertem pouco: uma gota de cada vez, escorrendo pela borda de baixo
      if (!parado && t > 500 && q % 7 === 0) ex.soltar(1, () => { const g = sorteio(dados.garras), f = al(0.2, 0.8);
        return { tipo: "verte", x: Math.round(g.x0 + (g.x1 - g.x0) * f) + 3, y: Math.round(g.y0 + (g.y1 - g.y0) * f), g: 0.12, vy: 0.2, vida: 12 }; });
    },
    desenhar(p, s) { pintar(p, s.vy > 1.2 ? GOTA_CAINDO : GOTA_PRESA, Math.round(s.x) - 1, Math.round(s.y), COR_GOTA); },
    parado: 3,
  };

  // ---- SOMBRA: o invisível com o corte. Olhos no escuro → o nome aparece aos pedaços → um instante inteiro → o corte
  // (uma vez) → as metades se afastam e se recompõem → os efeitos discretos do invisível continuam
  const CORTE_MS = 1050;
  SOMBRA_ID.c = {
    ...SOMBRA, atenua: 8, classe: "idv-sombra-c", semClarao: true,
    nome(el) {
      const texto = el.textContent, letras = [...texto], ordem = letras.map((_, i) => i).sort(() => Math.random() - 0.5);
      const atraso = letras.map((_, i) => (0.3 + (ordem.indexOf(i) / letras.length) * 0.42).toFixed(2));
      const camada = (cls, oculto) => `<span class="idv-camada ${cls}"${oculto ? ' aria-hidden="true"' : ""}>${letras.map((ch, i) => `<span class="idv-letra" style="--d:${atraso[i]}s">${ch}</span>`).join("")}</span>`;
      el.innerHTML = camada("idv-cima") + camada("idv-baixo", true);
      el.setAttribute("aria-label", texto);
      return el.querySelector(".idv-cima");
    },
    quadro({ p, r, t, q, parado, ex, dados }) {
      FX.poco(p, { cx: r.x, cy: r.y, rx: Math.round(r.rx * 1.7), ry: Math.round(r.ry * 4), forca: 15 });
      poco(p, r, 26, 16);
      const l = dados.l || (dados.l = linhaCorte(r));
      const olhos = (x, y, fechado) => { pintar(p, fechado ? OLHO_FECHADO : OLHO, x - 10, y, { o: "Y", k: "k" }, 2); pintar(p, fechado ? OLHO_FECHADO : OLHO, x + 4, y, { o: "Y", k: "k" }, 2); };
      if (!parado && t < 330) olhos(r.x, r.y - 2, t > 200 && t < 250);  // os olhos antes do nome
      if (parado || t > CORTE_MS + 80) desenharLinha(p, l, 1, ["x", "K"], 0);  // a cicatriz que fica
      if (!parado && t >= CORTE_MS - 30 && t < CORTE_MS + 100) desenharLinha(p, l, Math.min(1, (t - CORTE_MS + 30) / 60), ["W", "G"], 1);  // o golpe
      if (!parado && t >= CORTE_MS + 40 && t < CORTE_MS + 260) desenharLinha(p, l, 1, ["G", "m"], 1, 0.15);
      // depois, olhos nas laterais do escuro, de vez em quando
      const cl = (t - 2300) % 3200;
      if (parado) { olhos(r.esq - 34, r.y - 6, false); olhos(r.dir + 34, r.y + 2, true); }
      else if (t > 2300 && cl < 900) { if (!dados.lado || cl < 70) dados.lado = Math.random() < 0.5 ? { x: r.esq - Math.round(al(26, 46)), y: r.y + Math.round(al(-10, 6)) } : { x: r.dir + Math.round(al(26, 46)), y: r.y + Math.round(al(-10, 6)) };
        olhos(dados.lado.x, dados.lado.y, cl > 420 && cl < 500); }
      if (parado) return;
      if (!dados.golpe && t >= CORTE_MS) {
        dados.golpe = true;
        for (const [x, y] of [[l.x0, l.y0], [l.x1, l.y1]]) ex.soltar(8, () => ({ tipo: "faisca", x, y, vx: al(-2.5, 2.5), vy: al(-2.5, 1.5), g: 0.2, vida: Math.round(al(5, 9)) }));
        ex.soltar(22, () => { const f = Math.random(); return fumo(l.x0 + (l.x1 - l.x0) * f, l.y0 + (l.y1 - l.y0) * f, al(-0.8, 0.8), al(-1, 0.3)); });
      }
      const cg = (t - 2600) % 3000;  // o brilho que corre pela cicatriz, só nas pontas de fora do nome
      if (t > 2600 && cg < 500) { const f = cg / 500, x = l.x0 + (l.x1 - l.x0) * f, y = l.y0 + (l.y1 - l.y0) * f;
        if (x < r.esq - 2 || x > r.dir + 2) pintar(p, FX.DESENHOS.cruz, Math.round(x) - 1, Math.round(y) - 1, { a: "G", b: "W" }); }
      if (t < 800) ex.soltar(t < 350 ? 4 : 2, () => fumo(r.x + al(-r.rx, r.rx), r.y + al(-r.ry, r.ry), al(-1.2, 1.2), al(-0.6, 0.4)));  // a névoa sai enquanto o nome aparece
      else if (q % 3 === 0) ex.soltar(1, () => { const lado = Math.random() < 0.5 ? -1 : 1; return fumo(lado < 0 ? r.esq - 4 : r.dir + 4, r.y + al(-r.ry, r.ry), lado * al(0.3, 0.8), al(-0.4, 0)); });
    },
    desenhar(p, s) {
      if (s.tipo === "faisca") { p.por(Math.round(s.x), Math.round(s.y), C(s.idade < 3 ? "W" : "G")); return; }
      desenharFumo(p, s);
    },
    parado: 12,
  };

  // ---- PATRULHEIRO: o vendaval, em verde. O fundo da composição em verde quase negro (o céu do cenário não aparece
  // pelos vãos do pontilhado), os raios em verde de folhagem e os pontos de luz em verde pálido; sem dourado
  const VERDE_PALIDO = "#dcefb4";
  PATRULHEIRO.c = {
    ...PATRULHEIRO.a, pal: [VERDE_PALIDO, "E", "e", "f", "f"], cacos: ["E", "e", "e", "f", "f"], semClarao: true, claros: [VERDE_PALIDO, "E"], classe: "idv-folhas-a",
    antes({ p, r }) {  // por baixo dos raios da apresentação: o fundo verde-escuro da composição
      FX.poco(p, { cx: r.x, cy: r.y - r.ry * 3, rx: Math.round(r.rx * 2.4), ry: Math.round(r.ry * 9), forca: 16, c: "#07100a" });
      FX.halo(p, { cx: r.x, cy: r.y - r.ry, r: Math.round(r.rx * 1.8), achata: 0.55, pal: ["#10261a", "#10261a", "#10261a"], vis: 5 });
    },
    quadro(ctx) {
      const { p, r, t, q, parado, ex } = ctx;
      PATRULHEIRO.a.quadro(ctx);
      if (!parado && t < 220) FX.claraoLocal(p, { cx: r.x, cy: r.y, r: r.ry * 2.6, t, dur: 220, espalha: 0, pal: [VERDE_PALIDO, VERDE_PALIDO, "E", "e"] });
      if (!parado && q % 4 === 0) ex.soltar(1, () => ({ tipo: "luz", x: r.x + Math.round(al(-r.rx * 1.5, r.rx * 1.5)), y: r.y + Math.round(al(-r.ry * 3, r.ry * 0.5)), vy: -0.15, vida: Math.round(al(18, 30)) }));
    },
    desenhar(p, s) {
      if (s.tipo === "luz") { const k = s.idade / s.vida; if (pt(Math.round(s.x), Math.round(s.y), Math.round(14 * (1 - k)))) p.por(Math.round(s.x), Math.round(s.y), C(k < 0.5 ? VERDE_PALIDO : "E")); return; }
      PATRULHEIRO.a.desenhar(p, s);
    },
  };

  // ---- NECROMANTE: as caveiras e o círculo, com a fumaça escura saindo das letras em massas que crescem e sobem
  const FUMO_BORDA = "#365a3e", FUMO_MEIO = "#1a2c1f", FUMO_FUNDO = "#0e1711";
  function fumacaNegra(p, dados, r, c, t, q, parado) {
    const lista = dados.fumaca || (dados.fumaca = []);
    if (!parado && c.todos.length && t > 250) {
      // as massas saem do alto e dos lados das letras; algumas rastejam do círculo para fora
      if (q % 2 === 0) { const o = sorteio(c.topos.length && Math.random() < 0.7 ? c.topos : c.lados.length ? c.lados : c.todos);
        lista.push({ x: o.x, y: o.y, vx: ((o.x - r.x) / r.rx) * al(0.15, 0.45), vy: al(-0.55, -0.25), raio: 1.5, max: al(4, 8), idade: 0, vida: Math.round(al(26, 42)) }); }
      if (q % 5 === 0) { const lado = Math.random() < 0.5 ? -1 : 1;
        lista.push({ x: r.x + lado * r.rx * al(0.6, 1.05), y: r.base - 3, vx: lado * al(0.35, 0.7), vy: al(-0.12, -0.03), raio: 1.5, max: al(4, 7), idade: 0, vida: Math.round(al(26, 40)) }); }
    }
    for (let i = lista.length - 1; i >= 0; i--) {
      const s = lista[i];
      if (!parado) { s.idade++; s.x += s.vx; s.y += s.vy; s.raio = Math.min(s.max, s.raio + 0.22); if (s.idade > s.vida) { lista.splice(i, 1); continue; } }
      const k = s.idade / s.vida, R = s.raio, nivel = Math.round(16 * Math.min(1, (1 - k) * 2.2));
      for (let y = Math.floor(-R - 1); y <= R + 1; y++) for (let x = Math.floor(-R - 1); x <= R + 1; x++) {
        const d = Math.sqrt(x * x + y * y);
        if (d > R + 0.5) continue;
        const px = Math.round(s.x) + x, py = Math.round(s.y) + y;
        if (!pt(px, py, nivel)) continue;
        p.por(px, py, C(d > R - 0.8 ? (y < 0 ? FUMO_BORDA : FUMO_MEIO) : d < R * 0.45 ? FUMO_FUNDO : FUMO_MEIO));
      }
    }
  }
  NECROMANTE.c = {
    ...NECROMANTE.a, semClarao: true, claros: ["E", "e"],
    quadro(ctx) {
      const { p, r, c, t, q, parado, dados } = ctx;
      // a ordem: o escuro em volta, a fumaça saindo das letras, e então as caveiras e o círculo por cima dela
      FX.poco(p, { cx: r.x, cy: r.y, rx: Math.round(r.rx * 1.6), ry: Math.round(r.ry * 4), forca: 12, c: "N" });
      poco(p, r, 12, 16);
      fumacaNegra(p, dados, r, c, t, q, parado);
      NECROMANTE.a.quadro({ ...ctx, semFundo: true });
    },
    parado: 8,
  };

  // ================================================================ AS ALTERNATIVAS DE DETALHE (versões "d", "e", "f")
  // Só dois detalhes: o escorrimento do Berserker e a relação entre a luz e o nome do Paladino. O resto de cada
  // celebração é o da candidata final (versão "c"); as outras especializações usam a final aprovada.

  // ---- BERSERKER: o sangue numa camada logo acima do nome (pode escorrer pela borda das letras). A sequência é sempre
  // a mesma: acumula na letra → escorre um pouco → forma a gota → a ligação se rompe (um vão visível) → a gota cai
  // separada e some antes da descrição. Sem poças.
  const GOTAS = {  // b o corpo, c o ponto de luz, a a sombra do lado de baixo e da direita
    1: { presa: ["b.", "bc", "ba"], caindo: ["b.", "bc", "bb", ".a"] },
    2: { presa: [".b.", "bbc", "bba", ".a."], caindo: [".b.", ".bc", "bbb", "bba", ".a."] },
    3: { presa: ["..b..", ".bbc.", "bbbcb", "bbbba", ".bba."], caindo: ["..b..", ".bbc.", ".bbbc", "bbbbb", "bbbba", ".aaa."] },
  };
  const COR_SANGUE = { b: "r", c: "R", a: "D" };
  const ESCORRE = {
    // A: gotas pequenas, escorrimento curto, desprendimento rápido e irregular
    d: { pontos: 9, tam: () => 1, espera: () => al(150, 1300), acumula: () => al(4, 8), desce: () => Math.round(al(1, 3)), pescoco: () => Math.round(al(1, 2)), satelite: 0.35 },
    // B: filetes: o sangue percorre a borda de algumas letras antes de juntar e soltar a gota
    e: { pontos: 6, tam: () => (Math.random() < 0.7 ? 2 : 1), espera: () => al(400, 1900), acumula: () => al(6, 10), desce: () => Math.round(al(2, 4)), pescoco: () => Math.round(al(2, 3)), satelite: 0.2, filete: true },
    // C: volumes variados: poucas quedas, tamanhos e intervalos diferentes
    f: { pontos: 5, tam: () => sorteio([1, 1, 2, 2, 3]), espera: () => al(700, 3200), acumula: (k) => 5 + k * 4 + al(0, 4), desce: (k) => Math.round(1 + k + al(0, 2)), pescoco: (k) => Math.round(1 + k * 0.7 + al(0, 1.5)), satelite: 0.5 },
  };
  function pontosEscorre(c, r, cfg) {
    const bases = c.bases.filter((o) => o.y > r.y).sort((m, n) => m.x - n.x);
    if (!bases.length) return null;
    const pts = [];
    for (let i = 0; i < cfg.pontos; i++) {
      const o = bases[Math.min(bases.length - 1, Math.floor(((i + al(0.15, 0.85)) / cfg.pontos) * bases.length))];
      // o filete: as bordas da mesma letra, acima da base, de cima para baixo
      const borda = cfg.filete ? c.lados.filter((l) => Math.abs(l.x - o.x) <= 1 && l.y < o.y && l.y > r.y - r.ry * 0.7).sort((m, n) => m.y - n.y) : [];
      pts.push({ x: o.x, y: o.y, borda, estado: "espera", ate: 250 + Math.round(al(0, 1500)) + i * 60 });
    }
    return pts;
  }
  function moverEscorre(s, t, cfg, limite) {
    if (s.estado === "espera") {
      if (t < s.ate) return;
      s.tam = cfg.tam(); s.k = 0; s.durAc = cfg.acumula(s.tam); s.desce = cfg.desce(s.tam); s.pesc = cfg.pescoco(s.tam); s.d = 0;
      s.estado = s.borda && s.borda.length > 2 && Math.random() < 0.75 ? "filete" : "acumula"; s.f = 0;
      return;
    }
    if (s.estado === "filete") { s.f += 0.9; if (s.f >= s.borda.length) s.estado = "acumula"; return; }
    if (s.estado === "acumula") { s.k += 1 / s.durAc; if (s.k >= 1) s.estado = "escorre"; return; }
    if (s.estado === "escorre") { s.d += 0.35 + s.tam * 0.05; if (s.d >= s.desce + s.pesc) { s.estado = "rompe"; s.romp = 0; } return; }
    if (s.estado === "rompe") { s.romp++; if (s.romp >= 2) { s.estado = "cai"; s.gy = s.y + s.d; s.vy = 0.5; s.resto = s.pesc; s.sat = Math.random() < cfg.satelite ? s.y + s.desce : null; s.satVy = 0; } return; }
    if (s.estado === "cai") {
      s.vy += 0.34; s.gy += s.vy; s.resto = Math.max(0, s.resto - 0.7);  // o resto da ligação volta para a letra
      if (s.sat !== null) { s.satVy += 0.3; s.sat += s.satVy * (s.idadeCai > 1 ? 1 : 0); }
      s.idadeCai = (s.idadeCai || 0) + 1;
      if (s.gy > limite + 3) { s.estado = "espera"; s.ate = t + Math.round(cfg.espera()); s.idadeCai = 0; }
    }
  }
  function desenharEscorre(p, s, limite) {
    if (s.estado === "espera") return;
    const sangra = (x, y, cor = "r") => p.por(x, y, C(cor));
    if (s.estado === "filete") {  // o sangue correndo pela borda da letra, de cima para baixo, com a ponta mais clara
      const n = Math.floor(s.f);
      for (let i = Math.max(0, n - 6); i <= Math.min(n, s.borda.length - 1); i++) sangra(s.borda[i].x, s.borda[i].y, i === n ? "R" : "r");
      return;
    }
    const tam = s.tam, g = GOTAS[tam], meio = tam === 3 ? 2 : tam === 2 ? 1 : 0;
    if (s.estado === "acumula") {  // junta na borda de baixo da letra: uma lâmina que engrossa
      const w = Math.max(1, Math.round(s.k * (tam + 1)));
      for (let i = 0; i < w; i++) sangra(s.x - (w >> 1) + i, s.y, i === 0 ? "R" : "r");
      if (s.k > 0.6) sangra(s.x, s.y + 1);
      return;
    }
    if (s.estado === "escorre" || s.estado === "rompe") {
      const d = Math.round(s.d), corpo = Math.max(0, d - s.pesc);
      sangra(s.x - 1, s.y); sangra(s.x, s.y); sangra(s.x + 1, s.y, "D");
      for (let i = 1; i <= corpo; i++) sangra(s.x, s.y + i);  // o pouco que escorre
      for (let i = corpo + 1; i <= d; i++) if (!(s.estado === "rompe" && i === corpo + Math.ceil((d - corpo) / 2))) sangra(s.x, s.y + i, "D");  // o pescoço; ao romper, abre um vão
      pintar(p, g.presa, s.x - meio, s.y + d + 1, COR_SANGUE);
      return;
    }
    // caindo: a gota separada, o resto da ligação subindo para a letra, e às vezes uma gotinha de satélite
    sangra(s.x, s.y); for (let i = 1; i <= Math.round(s.resto); i++) sangra(s.x, s.y + i, "D");
    const forma = s.vy > 1.6 ? g.caindo : g.presa, gy = Math.round(s.gy);
    const some = gy > limite ? Math.max(0, 14 - (gy - limite) * 5) : 16;  // apaga em degraus logo antes da descrição
    for (let y = 0; y < forma.length; y++) for (let x = 0; x < forma[y].length; x++) {
      const ch = forma[y][x], px = s.x - meio + x, py = gy + y;
      if (ch !== "." && pt(px, py, some)) p.por(px, py, C(COR_SANGUE[ch]));
    }
    if (s.sat !== null && s.sat < limite) sangra(s.x, Math.round(s.sat), "r");
  }
  for (const v of ["d", "e", "f"]) {
    const cfg = ESCORRE[v];
    BERSERKER[v] = {
      ...BERSERKER.c,
      quadro(ctx) {  // a mesma composição da final (garras, veias, queda do nome), sem as poças nem as gotas antigas
        const { p, r, c, t, q, parado, ex, dados } = ctx;
        iniciarSangue(r, dados);
        veias(p, t, parado);
        if (!dados.garras) dados.garras = garras(r);
        poco(p, r, 10, 16);
        const u = parado ? 1 : rampa(t, 170, 200);
        if (u > 0) dados.garras.forEach((g, i) => desenharGarra(p, g, Math.min(1, u * 1.3 - i * 0.15)));
        dados.limite = r.base + 6;
        if (!dados.pts && c.bases.length) dados.pts = pontosEscorre(c, r, cfg);
        if (dados.pts && !parado) for (const s of dados.pts) moverEscorre(s, t, cfg, dados.limite);
        if (!parado && t > 500 && q % 9 === 0) ex.soltar(1, () => { const g = sorteio(dados.garras), f = al(0.2, 0.8);
          return { tipo: "verte", x: Math.round(g.x0 + (g.x1 - g.x0) * f) + 3, y: Math.round(g.y0 + (g.y1 - g.y0) * f), g: 0.12, vy: 0.2, vida: 12 }; });
      },
      sobre(p, dados) { if (dados.pts) for (const s of dados.pts) desenharEscorre(p, s, dados.limite); },
      desenhar(p, s) { pintar(p, s.vy > 1.2 ? GOTAS[1].caindo : GOTAS[1].presa, Math.round(s.x), Math.round(s.y), COR_SANGUE); },
      parado: 3,
    };
  }

  // ---- PALADINO: a luz e as penas da final, sem o recorte preto atrás do nome. As letras ficam à frente da luz (a
  // luz é desenhada por baixo do texto), com o contorno escuro e a sombra delas.
  const VITRAL = [  // por faixa, os vidros de cima para baixo (marfim, ouro envelhecido e nuances dessaturadas)
    ["#efe2c4", "#c9a35a", "#b48c86", "#efe2c4"], ["#c9a35a", "#efe2c4", "#8fa59c", "#c9a35a"], ["#efe2c4", "#d8c08c", "#efe2c4", "#a99bb0"],
    ["#d8c08c", "#efe2c4", "#c9a35a", "#efe2c4"], ["#a99bb0", "#efe2c4", "#c9a35a", "#d8c08c"], ["#c9a35a", "#8fa59c", "#efe2c4", "#b48c86"],
  ];
  function luzSemRecorte(modo) {
    return (lp, r, t, parado) => {
      const ox = r.x, oy = -lp.t(260), desce = parado ? 1 : rampa(t, 0, 460), fundo = r.base + 2;
      const x0 = Math.max(0, Math.floor(r.x - r.rx * 2.4)), x1 = Math.min(lp.W - 1, Math.ceil(r.x + r.rx * 2.4));
      const mexe = (i) => (parado ? 0 : Math.sin(t / 2700 + i * 1.7) * 0.012);
      // C: a região ampla e regular de menos luz atrás do título (uma elipse grande, em três degraus)
      const Ex = r.rx * 1.45, Ey = r.ry * 3.4, Ecy = r.y - r.ry * 0.6;
      for (let y = 0; y < Math.min(lp.H, Math.round(fundo * desce) + 16); y++) for (let x = x0; x <= x1; x++) {
        const pe = fundo - Math.round(hash(x >> 2) * 10), falta = pe - y;
        if (falta < -12) continue;
        const a = Math.atan2(x - ox, y - oy), dist = Math.hypot(x - ox, y - oy);
        let cor = null, n = 0, faixa = -1;
        for (let i = 0; i < FAIXAS.length; i++) {
          const [ai, wi, ci] = FAIXAS[i], d = Math.abs(a - ai - mexe(i));
          if (d > wi) continue;
          n++;
          if (!cor || d < wi * 0.6) { cor = ci; faixa = i; }
          if (d > wi * 0.78 && !pt(x, y, 8)) { n--; if (n === 0) cor = null; }
        }
        if (!cor) continue;
        if (falta < 0 && !pt(x, y, Math.round(14 + falta))) continue;
        if (modo === "vitral") {
          // os vidros: a cor muda ao longo da faixa, com um fio escuro (o chumbo) entre um vidro e outro
          const desl = dist + faixa * 13 + (faixa % 2) * 7, vidro = Math.floor(desl / 34), resto = desl % 34;  // os vidros desencontrados entre as faixas
          if (resto < 1) continue;
          cor = VITRAL[faixa][vidro % VITRAL[faixa].length];
          if (n > 1) cor = "#fbf0d8";
        } else if (n > 1) cor = "#fffbe6";
        if (modo === "suave") {
          const e = Math.pow((x - r.x) / Ex, 2) + Math.pow((y - Ecy) / Ey, 2);
          if (e < 1) cor = e < 0.45 ? "#5e4e36" : e < 0.75 ? "#8a7550" : "#b39a68";  // menos luz no centro, em degraus regulares
        }
        lp.por(x, y, C(cor));
      }
      const op = parado ? 0.5 : t < 700 ? 0.5 + Math.round(6 * (1 - t / 700)) * 0.02 : 0.47 + Math.round(2 + 2 * Math.sin(t / 1100)) * 0.01;
      lp.el.style.opacity = op.toFixed(2);
    };
  }
  const LUZ_MODO = { d: "continua", e: "vitral", f: "suave" };
  for (const v of ["d", "e", "f"]) {
    PALADINO[v] = {
      ...PALADINO.c, classe: "idv-luz-a idv-luz-legivel", semPocoRotulo: true,
      luz: luzSemRecorte(LUZ_MODO[v]),
      quadro(ctx) {  // a final sem o poço escuro atrás do nome
        const { p, r, t, q, parado, ex, dados } = ctx;
        if (!parado && t > 380 && t < 920) {
          const u = (t - 380) / 540;
          FX.anel(p, { cx: r.x, cy: r.y, r: Math.round(r.rx * (0.9 + u * 0.55)), esp: 1, pal: ["W", "w", "G"], achata: 0.3, rastro: 3, vis: Math.round(13 * (1 - u)) });
        }
        if (parado) return;
        if (!dados.soltou && t > 300) { dados.soltou = true; ex.soltar(9, () => penaCaindo(r.x + Math.round(al(-r.rx * 1.7, r.rx * 1.7)), Math.round(al(-10, r.topo * 0.6)), r.base + 6, al(0.3, 0.5))); }
        if (q % 6 === 0) ex.soltar(1, () => penaCaindo(r.x + Math.round(al(-r.rx * 1.9, r.rx * 1.9)), -8, r.base + 6));
        if (q % 3 === 0) motes(ex, r, 1, t);
      },
    };
  }

  const CONCEITOS = { luz: PALADINO, sangue: BERSERKER, folhas: PATRULHEIRO, sombra: SOMBRA_ID, almas: NECROMANTE };
  const NOMES = {
    luz: { a: "Luz do alto", b: "Asas" }, sangue: { a: "O nome sangra", b: "Garras" }, folhas: { a: "Vendaval", b: "Clareira" },
    sombra: { a: "Corte", b: "Invisível" }, almas: { a: "Erguer", b: "Almas" },
    // as candidatas finais
    detalhe: { luz: { d: "A · luz contínua", e: "B · vitral", f: "C · centro menos intenso" },
      sangue: { d: "A · gotas pequenas", e: "B · filetes", f: "C · volumes variados" } },
    final: { luz: "Luz e penas", sangue: "Garras, sangue líquido", folhas: "Vendaval verde", sombra: "Invisível com o corte", almas: "Erguer com a fumaça" },
  };

  /** A identidade `id` na versão `v` ("a" ou "b") para o nome `el`; a apresentação chama `quadro(p, t, q, parado)`
   *  depois do fundo dela e lê `atenua` (quanto baixar os raios dela) e `pal`/`cacos`. */
  function criar(id, el, v) {
    const conc = CONCEITOS[id] && (CONCEITOS[id][v] || (/[def]/.test(v) ? CONCEITOS[id].c : null));
    if (!conc) return null;
    el.className = el.className.replace(/\bidn-\S+/g, "").trim() + ` idv ${conc.classe}`;
    const alvoContorno = conc.nome ? conc.nome(el) : el;
    const ex = enxame(), dados = {}, rotulo = el.closest(".festa")?.querySelector(".fa2-sobre, .fb2-faixa span");
    let c = null, pronto = false, luz = null, sobre = null;
    if (conc.semPocoRotulo && rotulo) rotulo.classList.add("idv-rotulo-legivel");
    const vazio = { topos: [], bases: [], lados: [], todos: [] };
    return {
      id, versao: v, semPocoRotulo: !!conc.semPocoRotulo, pal: conc.pal, cacos: conc.cacos, atenua: conc.atenua || 0, semClarao: !!conc.semClarao, claros: conc.claros || null,
      /** Chamado pela apresentação antes do fundo dela (os raios): o que fica por baixo de tudo. */
      antes(p, t, q, parado) { if (conc.antes) conc.antes({ p, r: p.de(el), t, q, parado }); },
      treme: () => 0,
      quadro(p, t, q, parado) {
        const r = p.de(el);
        if (parado || (t >= 300 && (!c || !c.todos.length || q % 30 === 0))) c = Identidades.contorno(alvoContorno, p);
        if (parado && !pronto) {  // o quadro parado: o efeito simulado até acomodar, sem desenhar, e então parado
          pronto = true;
          const mudo = { ...p, por() {}, buf: new Uint32Array(0) };
          for (let k = 0; k < 44; k++) { conc.quadro({ p: mudo, r, c: c || vazio, t: 600 + k * FX.QUADRO, q: 40 + k, parado: false, ex, dados }); avancar(); }
          if (conc.preparar) { ex.lista.length = 0; conc.preparar(ex, r, p); }
          while (ex.lista.length > (conc.parado ?? 12)) ex.lista.splice(Math.floor(Math.random() * ex.lista.length), 1);
        }
        conc.quadro({ p, r, c: c || vazio, t: parado ? 3000 : t, q, parado, ex, dados });
        if (conc.luz) {  // a luz numa camada própria, translúcida, logo acima do palco (abaixo do texto)
          if (!luz) { luz = FX.palco(p.el.parentElement); p.el.after(luz.el); }
          luz.limpar(); conc.luz(luz, r, parado ? 3000 : t, parado, rotulo ? luz.de(rotulo) : null); luz.mostrar();
        }
        if (!parado) avancar();
        for (const s of ex.lista) conc.desenhar(p, s, parado);
        if (rotulo && !conc.semPocoRotulo) { const l = p.de(rotulo); FX.poco(p, { cx: l.x, cy: l.y, rx: l.rx + 10, ry: l.ry + 5, forca: 16 }); }
        if (conc.sobre) {  // a camada logo acima do texto (o sangue que escorre pela borda das letras)
          if (!sobre) { sobre = FX.palco(p.el.parentElement, { z: 2 }); p.el.parentElement.append(sobre.el); }
          sobre.limpar(); conc.sobre(sobre, dados); sobre.mostrar();
        }
      },
    };
    function avancar() {
      for (let i = ex.lista.length - 1; i >= 0; i--) {
        const s = ex.lista[i];
        s.idade++;
        let acabou = false;
        if (s.tipo === "fio" && conc.mover) acabou = conc.mover(s, dados);
        else if (s.mover) s.mover(s); else { s.x += s.vx; s.y += s.vy; s.vy += s.g; }
        if (acabou || s.idade > s.vida || (s.morre && s.morre(s))) ex.lista.splice(i, 1);
      }
    }
  }

  const faixas = (a, b, c) => `background: linear-gradient(${a} 0 34%, ${b} 34% 66%, ${c} 66% 100%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; text-shadow: none !important;`;
  const borda = (l, t, b) => `drop-shadow(2px 0 0 ${l}) drop-shadow(-2px 0 0 ${l}) drop-shadow(0 -2px 0 ${t}) drop-shadow(0 2px 0 ${b}) drop-shadow(0 5px 0 #08090a)`;
  const css = `
  /* PALADINO: marfim e ouro; na luz do alto, o nome sai incandescente e esfria */
  .idv-luz-a, .idv-luz-b { ${faixas("#fffdf4", "#f1e4c4", "#e0b870")} filter: ${borda("#8a6a14", "#fff3a0", "#4a3a10")}; }
  :root body .idv.idv-luz-a { animation: idv-esfria 0.8s steps(1) both !important; }
  @keyframes idv-esfria { 0% { filter: brightness(2.6) ${borda("#fff3a0", "#ffffff", "#c0b8a8")}; } 35% { filter: brightness(1.7) ${borda("#f2c94c", "#ffffff", "#8a6a14")}; }
    65% { filter: brightness(1.25) ${borda("#d4af37", "#fff3a0", "#4a3a10")}; } 100% { filter: ${borda("#8a6a14", "#fff3a0", "#4a3a10")}; } }
  :root body .idv.idv-luz-b { animation: idv-sobe 0.6s 0.1s steps(4) both !important; }
  @keyframes idv-sobe { from { translate: 0 14px; opacity: 0; } 30% { opacity: 1; } to { translate: 0 0; opacity: 1; } }
  /* BERSERKER: o osso e o sangue; no primeiro, o sangue tinge as letras de cima para baixo */
  .idv-sangue-a { background: linear-gradient(#f1e4c4 0 45%, #e8c8b0 45% 50%, #e2574c 50% 56%, #b3262b 56% 100%); background-size: 100% 300%;
    -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; text-shadow: none !important; background-position: 0 50%;
    filter: ${borda("#6e0d0d", "#b3262b", "#2a0a0a")}; }
  :root body .idv.idv-sangue-a { animation: idv-carimbo 0.27s steps(4) both, idv-tinge 0.6s 0.25s steps(4) both !important; }
  @keyframes idv-carimbo { from { scale: 1.4; } to { scale: 1; } }
  @keyframes idv-tinge { from { background-position: 0 0; } to { background-position: 0 50%; } }
  .idv-sangue-b { ${faixas("#f1e4c4", "#e8c8b0", "#e2574c")} filter: ${borda("#6e0d0d", "#e2574c", "#2a0a0a")}; }
  :root body .idv.idv-sangue-b { animation: idv-despenca 0.42s steps(1) both !important; }
  @keyframes idv-despenca { 0% { translate: 0 -70px; } 25% { translate: 0 -30px; } 40% { translate: 0 6px; scale: 1.06 0.88; } 55% { translate: 0 -3px; scale: 0.98 1.03; } 75%, 100% { translate: 0 0; scale: 1; } }
  /* PATRULHEIRO: o verde da mata, com luz; no vendaval, o nome aparece com a rajada, da esquerda para a direita */
  .idv-folhas-a, .idv-folhas-b { ${faixas("#e8f6c8", "#8fbf6a", "#4f9a5b")} filter: ${borda("#1f4a25", "#8fbf6a", "#0d2010")}; }
  :root body .idv.idv-folhas-a { animation: idv-rajada 0.9s 0.3s steps(9) both !important; }
  @keyframes idv-rajada { from { clip-path: inset(-20% 100% -20% 0); } to { clip-path: inset(-20% -2% -20% 0); } }
  :root body .idv.idv-folhas-b { animation: idv-clareia 0.7s 0.2s steps(4) both !important; }
  @keyframes idv-clareia { from { filter: brightness(0.25) ${borda("#1f4a25", "#8fbf6a", "#0d2010")}; } to { filter: brightness(1) ${borda("#1f4a25", "#8fbf6a", "#0d2010")}; } }
  /* SOMBRA: cinza de pedra, borda quase preta; o corte separa as duas metades e elas voltam */
  .idv-sombra-a, .idv-sombra-b { filter: ${borda("#08090a", "#3a3448", "#08090a")}; }
  .idv-sombra-b .idv-letra, .idv-sombra-a .idv-camada { ${faixas("#e2ddd2", "#b0a898", "#7a7080")} }
  :root body .idv.idv-sombra-a { display: inline-grid; animation: none !important; background: none; }
  .idv-sombra-a > .idv-camada { grid-area: 1 / 1; }
  .idv-sombra-a > .idv-cima { clip-path: polygon(-5% -20%, 105% -20%, 105% 30%, -5% 78%); animation: idv-corte-cima 1s steps(1) both; }
  .idv-sombra-a > .idv-baixo { clip-path: polygon(-5% 78%, 105% 30%, 105% 120%, -5% 120%); animation: idv-corte-baixo 1s steps(1) both; }
  @keyframes idv-corte-cima { 0%, 28% { translate: 0 0; } 29%, 36% { translate: -7px -3px; } 37%, 62% { translate: -14px -6px; } 63%, 70% { translate: -4px -2px; } 71%, 76% { translate: 1px 0; } 77%, 100% { translate: 0 0; } }
  @keyframes idv-corte-baixo { 0%, 28% { translate: 0 0; } 29%, 36% { translate: 7px 3px; } 37%, 62% { translate: 14px 6px; } 63%, 70% { translate: 4px 2px; } 71%, 76% { translate: -1px 0; } 77%, 100% { translate: 0 0; } }
  :root body .idv.idv-sombra-b { animation: none !important; background: none; }
  .idv-sombra-b .idv-letra { display: inline-block; animation: idv-surge 0.5s var(--d) steps(1) both; }
  .idv-sombra-b .idv-letra.idv-falha { animation: idv-surge 0.5s var(--d) steps(1) both, idv-falha 0.45s 1.25s steps(1) both; }
  @keyframes idv-surge { 0% { opacity: 0; } 20% { opacity: 0.25; } 40% { opacity: 0; } 60% { opacity: 0.55; } 80%, 100% { opacity: 1; } }
  @keyframes idv-falha { 0% { opacity: 1; } 20% { opacity: 0.15; } 45% { opacity: 0; } 70% { opacity: 0.5; } 85%, 100% { opacity: 1; } }
  /* SOMBRA, a final: o invisível (as letras aos pedaços) dentro das duas metades do corte, que se separam uma vez */
  :root body .idv.idv-sombra-c { display: inline-grid; animation: none !important; background: none; filter: ${borda("#08090a", "#3a3448", "#08090a")}; }
  .idv-sombra-c > .idv-camada { grid-area: 1 / 1; }
  .idv-sombra-c .idv-letra { display: inline-block; ${faixas("#e2ddd2", "#b0a898", "#7a7080")} animation: idv-surge-c 0.36s var(--d) steps(1) both; }
  @keyframes idv-surge-c { 0% { opacity: 0; } 25% { opacity: 0.3; } 50% { opacity: 0.1; } 75% { opacity: 0.7; } 100% { opacity: 1; } }
  .idv-sombra-c > .idv-cima { clip-path: polygon(-5% -20%, 105% -20%, 105% 30%, -5% 78%); animation: idv-corte-c-cima 1.6s steps(1) both; }
  .idv-sombra-c > .idv-baixo { clip-path: polygon(-5% 78%, 105% 30%, 105% 120%, -5% 120%); animation: idv-corte-c-baixo 1.6s steps(1) both; }
  @keyframes idv-corte-c-cima { 0%, 65% { translate: 0 0; } 66%, 69% { translate: -7px -3px; } 70%, 84% { translate: -14px -6px; } 85%, 88% { translate: -4px -2px; } 89%, 91% { translate: 1px 0; } 92%, 100% { translate: 0 0; } }
  @keyframes idv-corte-c-baixo { 0%, 65% { translate: 0 0; } 66%, 69% { translate: 7px 3px; } 70%, 84% { translate: 14px 6px; } 85%, 88% { translate: 4px 2px; } 89%, 91% { translate: -1px 0; } 92%, 100% { translate: 0 0; } }
  /* PALADINO, as alternativas sem o recorte: as letras à frente da luz, com o contorno escuro e a sombra delas; o
     rótulo com o contorno, sem a placa */
  .idv-luz-legivel { filter: drop-shadow(2px 0 0 #3a2a0c) drop-shadow(-2px 0 0 #3a2a0c) drop-shadow(0 -2px 0 #6b4b18) drop-shadow(0 2px 0 #1a1206) drop-shadow(0 5px 0 #08090a) !important; }
  :root body .idv.idv-luz-a.idv-luz-legivel { animation: none !important; }
  .idv-rotulo-legivel { text-shadow: 2px 0 #08090a, -2px 0 #08090a, 0 2px #08090a, 0 -2px #08090a, 2px 2px #08090a, -2px 2px #08090a, 2px -2px #08090a, -2px -2px #08090a !important; }
  /* NECROMANTE: verde de túmulo, profundo, com o claro só no alto das letras */
  .idv-almas-a, .idv-almas-b { ${faixas("#e6f2d8", "#a8d48a", "#4f9a5b")} filter: ${borda("#0d2a14", "#4f9a5b", "#050a06")}; }
  :root body .idv.idv-almas-b { animation: idv-almas 1.2s 0.2s steps(6) both !important; }
  @keyframes idv-almas { from { filter: brightness(0.3) ${borda("#0d2a14", "#4f9a5b", "#050a06")}; } to { filter: brightness(1) ${borda("#0d2a14", "#4f9a5b", "#050a06")}; } }
  @media (prefers-reduced-motion: reduce) {
    :root body .idv, .idv .idv-camada, .idv .idv-letra { animation: none !important; }
  }`;
  document.head.insertAdjacentHTML("beforeend", `<style id="estilo-identidades2">${css}</style>`);

  return { criar, NOMES, suporta: (id) => !!CONCEITOS[id] };
})();

/* PROTÓTIPO, direção A5: RELICÁRIO (o A4 aprovado; só a especialização usa as identidades da segunda rodada, versão 1 ou 2) (24/10/2026). O sol de raios e a medalha da A, com o que o Jean pediu:
   - os itens no tamanho de uso do cartão do saque (o arquivo de 64 da produção, sem ampliar); o sol conduz o olhar;
   - a informação sem molduras repetidas: os raios passam por trás dela num poço escuro em pontilhado (o alto e o pé
     viram uma peça só), os ganhos alinhados numa linha (ícone, valor, nome), o ponto de talento na mesma composição com
     o atalho, a habilidade pelo ícone do Grimório, nome e descrição, e o Continuar dos botões do jogo;
   - a especialização com o nome como protagonista (o sol atrás do nome, sem a medalha);
   - o achado: o item, a raridade e o nome no alto; embaixo, numa composição só, o prêmio, a troca e o que você usa;
   - o comum entra sem aura (desce ao altar com um pouco de poeira e um brilho só); o mágico tem um brilho breve e
     localizado; raro, lendário e Sigilo continuam com o sol inteiro;
   - depois da entrada, o efeito continua vivo e um pouco mais baixo (os raios em pontilhado mais aberto), para ler. */
"use strict";

(() => {
  const { h, ganhos, talento, habilidades, continuar, fichaItem, arteItem } = Festa;
  const P = FX.PALETAS;
  const SUSTENTA = 1400;  // ms: depois da entrada, o sol baixa um pouco

  function medalha(p, cx, cy, R, pal) {
    const [, claro, meio, escuro, fundo] = pal.map(FX.cor);
    const k = FX.cor("k"), q = FX.cor("z"), Q = FX.cor("q");
    for (let y = cy - R - 1; y <= cy + R + 1; y++) for (let x = cx - R - 1; x <= cx + R + 1; x++) {
      const dx = x - cx, dy = y - cy, d = Math.sqrt(dx * dx + dy * dy);
      if (d > R + 0.5) continue;
      if (d > R - 0.7) { p.por(x, y, k); continue; }
      const luz = (-dx - dy) / (d || 1);
      if (d > R - 3.5) p.por(x, y, luz > 0.45 ? claro : luz < -0.45 ? escuro : meio);
      else if (d > R - 4.5) p.por(x, y, luz > 0 ? fundo : k);
      else p.por(x, y, Sprites.pontilha(x, y, d < R * 0.55 ? 3 : 1) ? Q : q);
    }
  }
  const ALCANCE = (a) => 1 - 0.35 * Math.max(0, Math.sin(a));
  /** O sol: os raios largos e os finos girando ao contrário; `vis` baixa na sustentação. */
  function sol(p, { cx, cy, R, r1, ang, n = 14, pal, fino = true, vis = 16 }) {
    FX.raios(p, { cx, cy, n, ang, larg: 0.4, r0: R, r1, pal: pal.slice(1), esbate: 0.4, vis, alterna: 0.68, alcance: ALCANCE });
    if (fino) FX.raios(p, { cx, cy, n: n * 2, ang: -ang * 1.7 + 0.11, larg: 0.09, r0: R, r1: R + (r1 - R) * 0.78, pal, esbate: 0.3, fio: false, vis: Math.min(vis, 14), alcance: ALCANCE });
  }
  const vivo = (t, parado) => (parado ? 12 : Math.round(FX.rampa(t, SUSTENTA, 900, 16, 12)));
  function faiscas(enx, cx, cy, R, n, pal) {
    enx.soltar(n, (i) => {
      const a = (i / n) * Math.PI * 2 + FX.aleatorio(-0.2, 0.2), v = FX.aleatorio(2.2, 4.2);
      return { x: cx + Math.cos(a) * R, y: cy + Math.sin(a) * R, vx: Math.cos(a) * v, vy: Math.sin(a) * v, arrasto: 0.86,
        vida: Math.round(FX.aleatorio(9, 16)), desenho: i % 4 ? "cruz" : "brilho", pal };
    });
  }
  function cintilar(enx, cx, cy, R, r1, pal) {
    const a = FX.aleatorio(0, Math.PI * 2), d = FX.aleatorio(R * 1.4, r1 * 0.8);
    enx.soltar(1, () => ({ x: cx + Math.cos(a) * d, y: cy + Math.sin(a) * d, vx: 0, vy: 0, vida: 9, desenho: Math.random() < 0.5 ? "brilho" : "estrela", pal }));
  }
  /** O poço escuro atrás da informação: os raios passam por trás dela, apagados. */
  function poco(p, el, folga = 90, forca = 16) {
    if (!el) return;
    const i = p.de(el);
    FX.poco(p, { cx: i.x, cy: i.y, rx: i.rx + p.t(folga), ry: i.ry + p.t(folga * 0.6), forca });
  }

  /** A festa: no alto, o que celebra (a medalha, ou o nome na especialização) no sol; embaixo, a informação. */
  function festa({ classe, sobre, palavra, numero, titulo, info, pal, som, identidade = null }) {
    const alto = titulo
      ? `<div class="fa2-coroa fa2-centro"><span class="fa2-sobre${identidade ? ` idn-sobre-${identidade}` : ""}">${sobre}</span><b class="fa2-titulo${identidade ? ` idn-${identidade}` : ""}">${titulo}</b></div>`
      : `<div class="fa2-coroa"><span class="fa2-sobre">${sobre}</span>
          <div class="fa2-medalha fa2-centro">${palavra ? `<span class="fa2-palavra">${palavra}</span>` : ""}<span class="fa2-numero">${numero}</span></div></div>`;
    const html = `<div class="festa fa2 ${classe}">${alto}<div class="fa2-info"><i class="fa2-fio"></i>${info}${continuar()}</div></div>`;
    const efeito = (el, caixa) => {
      const p = FX.palco(caixa), enx = FX.enxame(), centro = el.querySelector(".fa2-centro"), inf = el.querySelector(".fa2-info");
      const nome = el.querySelector(".fa2-titulo"), ident = identidade ? (Identidades2.suporta(identidade) && typeof IDENTIDADE_VARIANTE !== "undefined" ? Identidades2.criar(identidade, nome, IDENTIDADE_VARIANTE) : Identidades.criar(identidade, nome)) : null;
      App.som(som);
      const claros = (ident && ident.claros) || ["W", "Y"];
      if (ident && ident.versao === "c") pal = ident.pal;  // as finais trazem a paleta delas (as antigas tinham marrom e roxo)
      const ctl = FX.animar(p, (t, q, parado) => {
        if (ident && ident.antes) ident.antes(p, t, q, parado);
        const m = p.de(centro), R = titulo ? Math.round(Math.min(m.rx, m.ry) * 0.5) : Math.round(m.rx * 0.92);
        const r1 = Math.max(R + 10, p.t(Math.min(innerHeight * 0.7, 600))), abre = parado ? 1 : FX.rampa(t, 0, 520);
        // o fogo: os raios tremulam (um nível a menos de vez em quando) e o calor fica atrás do nome
        const treme = ident && !parado ? ident.treme(q) : 0;
        sol(p, { cx: m.x, cy: m.y, R, r1: R + (r1 - R) * abre, ang: parado ? 0.12 : q * (ident && ident.id === "fogo" ? 0.045 : 0.035), pal, vis: vivo(t, parado) - treme - (ident ? Math.round((ident.atenua || 0) * 1.5) : 0) });  // no Relicário, o sol baixa mais: a identidade conduz
        if (!parado && t < 330) FX.halo(p, { cx: m.x, cy: m.y, r: R * (2.6 - (t / 330) * 1.2), pal: [claros[0], claros[0], claros[1], pal[1]], vis: Math.round(16 * (1 - t / 330)) });
        poco(p, inf);
        if (!(ident && ident.semPocoRotulo)) poco(p, el.querySelector(".fa2-sobre"), 50, 16);  // o rótulo de cima, legível sobre os raios
        if (!titulo) medalha(p, m.x, m.y, R, pal);
        if (ident) ident.quadro(p, t, q, parado);  // a identidade da especialização, em volta do nome
        if (parado) return;
        if (q === 1) faiscas(enx, m.x, m.y, R, 18, [...claros, pal[2], pal[3]]);
        if (q > 10 && q % 5 === 0) cintilar(enx, m.x, m.y, R, r1, [...claros, pal[2]]);
        enx.passo(); enx.desenhar(p);
      });
      return { parar: ctl.parar, revelar: () => { ctl.pular(520); el.classList.add("pulou"); } };
    };
    return { html, efeito };
  }

  const linhaGanhos = (d) => `<div class="fa2-ganhos">${ganhos(d).map((x) => `<span class="fa2-ganho">${x.icone}<b>+${x.v}</b><span>${h(x.k)}</span></span>`).join("")}</div>`;
  const linhaTalento = () => `<div class="fa2-talento">${talento(32)}<b>+1</b><span>ponto de talento</span><kbd>T</kbd></div>`;
  const blocoHabs = (lista) => habilidades(lista).map((x) => `<div class="fa2-hab"><span class="fa2-hab-icone">${x.icone}</span>
    <div><span class="fa2-rotulo">nova habilidade</span><b>${x.nome}</b><p>${x.desc}</p></div></div>`).join("");

  const direcao = {
    nome: "relicario5",
    nivel: (d) => festa({ classe: "fa2-nivel", sobre: "você subiu de nível", palavra: "Nível", numero: d.nivel, pal: P.ouro, som: "subir",
      info: `${linhaGanhos(d)}${linhaTalento()}${blocoHabs(d.habilidades)}
        ${d.especializacao ? '<p class="fa2-aviso">Uma encruzilhada se aproxima: em breve você escolherá sua especialização.</p>' : ""}` }),
    sigilo: (d) => festa({ classe: "fa2-sigilo", sobre: `${h(d.guardiao)} caiu`, palavra: "Sigilo", numero: `${d.sigilos}/3`, pal: P.sigilo, som: "fanfarra",
      info: `<div class="fa2-losangos">${[0, 1, 2].map((i) => `<i class="${i < d.sigilos ? "tem" : ""}"></i>`).join("")}</div>
        <p class="fa2-texto">Uma runa ardente se grava na sua mão.</p>${linhaTalento()}` }),
    spec: (d) => festa({ classe: "fa2-spec", sobre: "você agora é", titulo: h(d.nome), som: "fanfarra", identidade: Identidades.qual(d.nome),
      pal: Identidades.PAL[Identidades.qual(d.nome)] || P.arcano,
      info: `<p class="fa2-texto">${h(d.desc)}</p>${blocoHabs(d.habilidades)}` }),

    achado(d) {
      const f = fichaItem(d);
      return `<div class="tela achado fa2-achado rar-${f.rar}">
        <div class="achado-cartao novo rar-${f.rar}">
          <div class="fa2-altar"><div class="achado-arte">${arteItem(d.item, 64)}</div></div>
          <div class="fa2-cabeca"><span class="achado-selo">Você encontrou</span>${f.raridade}${f.nome}</div>
        </div>
        <div class="fa2-ficha${f.compara ? " compara" : ""}">${f.premio}${f.troca}${f.usa ? `<div class="fa2-usa">${f.usa}</div>` : ""}</div>
        ${f.lore}${f.aviso}</div>`;
    },
    SOL: {
      raro: { n: 12, raio: 260, pal: P.raro, fino: true, faiscas: 14 },
      lendario: { n: 14, raio: 380, pal: P.lendario, fino: true, faiscas: 26, clarao: true, brasas: true },
    },
    async cerimonia({ fundo, janela, d, parado, esperar }) {
      const rar = d.item.raridade, cfg = direcao.SOL[rar], p = FX.palco(fundo), enx = FX.enxame();
      const arte = janela.querySelector(".achado-cartao.novo .achado-arte"), ficha = janela.querySelector(".fa2-ficha"), cabeca = janela.querySelector(".fa2-cabeca");
      if (!parado) App.som(["raro", "lendario"].includes(rar) ? "achado_raro" : "achado");
      fundo.classList.add("entrando");
      const brasa = ["Y", "O", "o", "r", "D"];
      FX.animar(p, (t, q, quieto) => {
        const a = p.de(arte), R = Math.round(a.rx * 1.05);
        if (cfg) {
          const abre = quieto ? 1 : FX.rampa(t, 60, 520), r1 = p.t(cfg.raio);
          sol(p, { cx: a.x, cy: a.y, R: R + 2, r1: R + 2 + (r1 - R) * abre, ang: quieto ? 0.1 : q * (rar === "lendario" ? 0.04 : 0.03), n: cfg.n, pal: cfg.pal, fino: cfg.fino, vis: vivo(t, quieto) });
          poco(p, ficha);
          poco(p, cabeca, 60, 15);
        }
        if (quieto) return;
        if (cfg) {
          if (cfg.clarao) FX.claraoLocal(p, { cx: a.x, cy: a.y, r: R * 4, t, dur: 220, espalha: 2, pal: ["W", "Y", "Y", "O"] });
          FX.poco(p, { cx: a.x, cy: a.y, rx: R + 5, ry: R + 5, forca: 16 });
          if (q === 2) faiscas(enx, a.x, a.y, R, cfg.faiscas, ["W", cfg.pal[1], cfg.pal[2], cfg.pal[3]]);
          if (q > 10 && q % 6 === 0) cintilar(enx, a.x, a.y, R, p.t(cfg.raio), ["W", cfg.pal[1], cfg.pal[2]]);
          if (cfg.brasas && q % 2 === 0) enx.soltar(1, () => ({ x: a.x + Math.round(FX.aleatorio(-R * 3, R * 3)), y: a.y + R + Math.round(FX.aleatorio(0, 10)),
            vx: FX.aleatorio(-0.2, 0.2), vy: FX.aleatorio(-1.1, -0.6), vida: Math.round(FX.aleatorio(14, 24)), desenho: "brasa", pal: brasa }));
        } else if (rar === "magico") {
          // um brilho breve, só em volta do item: um anel curto, raios que piscam e somem, sem nada que fique
          if (t < 640) {
            FX.raios(p, { cx: a.x, cy: a.y, n: 8, ang: 0.2, larg: 0.18, r0: R + 1, r1: R + 2 + Math.round(FX.rampa(t, 0, 300) * p.t(46)), pal: P.magico.slice(1), esbate: 0.3, vis: Math.round(16 * (1 - FX.rampa(t, 260, 380))) });
            FX.anel(p, { cx: a.x, cy: a.y, r: R + Math.round(FX.rampa(t, 0, 420) * p.t(40)), esp: 1, pal: ["W", "M", "U"], rastro: 2, vis: Math.round(14 * (1 - t / 640)) });
          }
          if (q === 3) faiscas(enx, a.x, a.y, R, 6, ["W", "M", "U", "u"]);
        } else if (q === 3) {
          // comum: o item pousa e levanta um pouco de poeira; um brilho só no metal, e mais nada
          enx.soltar(10, (i) => ({ x: a.x + FX.aleatorio(-R, R), y: a.y + R - 1, vx: (i % 2 ? 1 : -1) * FX.aleatorio(0.4, 1.6), vy: FX.aleatorio(-0.9, -0.2),
            g: 0.08, arrasto: 0.9, vida: Math.round(FX.aleatorio(8, 13)), desenho: "ponto", pal: ["G", "g", "d"] }));
          enx.soltar(1, () => ({ x: a.x + Math.round(R * 0.4), y: a.y - Math.round(R * 0.4), vx: 0, vy: 0, vida: 6, desenho: "brilho", pal: ["W", "w", "G"] }));
        }
        enx.passo(); enx.desenhar(p);
      });
      if (parado) return;
      await esperar({ comum: 240, magico: 320, raro: 480, lendario: 620 }[rar] || 300);
    },
  };

  const PRETO = "#0d0b0a";
  const contorno = (px, c = PRETO) => [[px, 0], [-px, 0], [0, px], [0, -px], [px, px], [-px, px], [px, -px], [-px, -px]].map(([x, y]) => `${x}px ${y}px 0 ${c}`).join(", ");
  const css = `
  /* ---- A2: Relicário refinado ---- */
  #celebracao.dir-relicario5 { background: rgba(4, 3, 2, 0.9); }
  .festa.fa2 { position: relative; z-index: 1; display: flex; flex-direction: column; align-items: center; width: min(920px, 96vw);
    background: none; border: 0; box-shadow: none; padding: 0; text-align: center; }
  .fa2-coroa { display: flex; flex-direction: column; align-items: center; gap: 22px; margin-bottom: 40px; }
  .fa2-sobre { font: 700 15px/1 var(--texto); letter-spacing: 0.34em; text-transform: uppercase; color: #fff3a0; text-shadow: ${contorno(2)}; }
  .fa2-medalha { width: 160px; height: 160px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
  .fa2-palavra { font: 22px/1 var(--titulo); color: #c0b8a8; text-shadow: 2px 2px 0 #000; margin-top: 6px; }
  .fa2-numero { font: 84px/0.9 var(--titulo); color: #ffe27a; text-shadow: ${contorno(3)}, 0 6px 0 #000; }
  .fa2-sigilo .fa2-numero { font-size: 54px; }
  .fa2-titulo { display: block; padding: 6px 18px; font: 400 92px/1 var(--titulo); color: #f1e4ff; text-shadow: ${contorno(4, "#1c0f2a")}, 0 8px 0 #000; }
  .fa2-spec .fa2-coroa { gap: 14px; margin: 40px 0 34px; }
  .fa2-info { display: flex; flex-direction: column; align-items: center; gap: 14px; width: 100%; }
  /* o fio de latão com o losango no meio: separa o alto da leitura sem moldura */
  .fa2-fio { position: relative; display: block; width: min(560px, 80%); height: 2px; background: #6b4b31; box-shadow: 0 1px 0 #000; }
  .fa2-fio::before { content: ""; position: absolute; left: 50%; top: -3px; width: 4px; height: 4px; translate: -2px 0;
    background: #f2c94c; box-shadow: -2px 2px 0 #d4af37, 2px 2px 0 #d4af37, 0 4px 0 #f2c94c, 0 2px 0 #8a6a14; }
  .fa2-ganhos { display: flex; flex-wrap: wrap; justify-content: center; gap: 6px 0; }
  .fa2-ganho { display: inline-flex; align-items: center; gap: 6px; padding: 0 11px; }
  .fa2-ganho + .fa2-ganho { border-left: 1px solid #3a3128; }
  .fa2-ganho b { font: 30px/1 var(--titulo); color: #8fbf6a; text-shadow: 2px 2px 0 #000; }
  .fa2-ganho > span { font: 700 12px/1 var(--texto); letter-spacing: 0.16em; text-transform: uppercase; color: #c0b8a8; }
  .fa2-talento { display: inline-flex; align-items: center; gap: 9px; font: 20px/1 var(--texto); color: #f2d27a; text-shadow: 1px 1px 0 #000; }
  .fa2-talento b { font: 30px/1 var(--titulo); color: #fff3a0; text-shadow: 2px 2px 0 #000; }
  .fa2 kbd, .dir-relicario5 kbd { font: 13px/1 var(--num); color: #c0b8a8; border: 1px solid #4a4d53; background: #0b0c0e; padding: 2px 5px; margin-left: 4px; }
  .fa2-hab { display: flex; align-items: flex-start; gap: 14px; max-width: 620px; text-align: left; margin-top: 2px; }
  .fa2-hab-icone { flex: none; display: grid; place-items: center; width: 44px; height: 44px; margin-top: 4px; background: #120c1a; box-shadow: inset 0 0 0 1px #5a2a6e; }
  .fa2-hab b { display: block; font: 28px/1.05 var(--titulo); color: #e4d8ff; text-shadow: 2px 2px 0 #000; }
  .fa2-hab p { margin: 3px 0 0; font: 16px/1.4 var(--texto); color: #e8dcbe; }
  .fa2-rotulo { font: 700 11px/1 var(--texto); letter-spacing: 0.24em; text-transform: uppercase; color: #8e6fd8; }
  .fa2-aviso { margin: 0; font: italic 16px/1.4 var(--texto); color: #c8b0ff; }
  .fa2-texto { margin: 0; max-width: 620px; font: 17px/1.45 var(--texto); color: #e8dcbe; }
  .fa2-losangos { display: flex; gap: 14px; } .fa2-losangos i { width: 16px; height: 16px; rotate: 45deg; border: 3px solid #6e0d0d; background: #17120f; }
  .fa2-losangos i.tem { background: #e2574c; border-color: #ffb35c; }
  :root body .fa2 .continuar { margin-top: 6px; display: inline-flex; align-items: center; gap: 6px; }
  .fa2 .fa2-medalha { animation: fa2-carimbo 0.27s steps(4) both; }
  @keyframes fa2-carimbo { from { scale: 1.45; } to { scale: 1; } }
  .fa2 .fa2-titulo { animation: fa2-carimbo 0.27s steps(4) both; }
  .fa2 .fa2-info { animation: fa2-sobe 0.2s 0.08s steps(3) both; }
  @keyframes fa2-sobe { from { translate: 0 16px; } to { translate: 0 0; } }
  .fa2.pulou :is(.fa2-medalha, .fa2-titulo, .fa2-info) { animation: none; }

  /* o achado: o item no tamanho do saque, a ficha numa peça só */
  :root body #sobre-achado.dir-relicario5 { background: rgba(4, 3, 2, 0.88); }
  :root body #sobre-achado.dir-relicario5 .janela-achado { position: relative; z-index: 1; background: none; border: 0; box-shadow: none; padding: 0;
    max-height: none; overflow: visible; width: min(900px, 96vw); }
  :root body #sobre-achado .fa2-achado.tela.achado { display: flex; flex-direction: column; align-items: center; gap: 12px; }
  :root body #sobre-achado .fa2-achado .achado-cartao.novo { display: flex; flex-direction: column; align-items: center; gap: 8px; width: auto;
    background: none; border: 0; box-shadow: none; padding: 0; overflow: visible; animation: none; }
  :root body #sobre-achado .fa2-achado .achado-cartao.novo .achado-arte { width: 64px; height: 64px; margin: 0; }
  .fa2-cabeca { display: flex; flex-direction: column; align-items: center; gap: 8px; }
  .fa2-altar { display: grid; place-items: center; height: 150px; }
  #sobre-achado.dir-relicario5:is(.rar-comum, .rar-magico) .fa2-altar { height: 84px; }
  :root body #sobre-achado .fa2-achado .achado-cartao.novo > .achado-selo { font: 700 13px/1 var(--texto); letter-spacing: 0.32em; text-transform: uppercase; color: #f2d27a; text-shadow: ${contorno(2)}; }
  .ficha-raridade { display: inline-flex; align-items: center; gap: 10px; font: 700 13px/1 var(--texto); letter-spacing: 0.26em; text-transform: uppercase; }
  .ficha-raridade::before, .ficha-raridade::after { content: ""; width: 34px; height: 2px; background: currentColor; box-shadow: 0 1px 0 #000; }
  .ficha-raridade.rar-comum { color: #c0b8a8; } .ficha-raridade.rar-magico { color: #7fb0ff; } .ficha-raridade.rar-raro { color: #f2c94c; } .ficha-raridade.rar-lendario { color: #ffb35c; }
  .ficha-nome { display: block; max-width: 820px; font: 400 40px/1.05 var(--titulo); text-shadow: ${contorno(2)}, 0 4px 0 #000; text-wrap: balance; }
  .ficha-nome.r-comum { color: #f1e4c4; }
  .fa2-ficha { display: grid; grid-template-columns: 1fr; justify-items: center; gap: 0 26px; padding-top: 12px; width: 100%; box-shadow: inset 0 2px 0 #2b2219; }
  .fa2-ficha.compara { grid-template-columns: 1fr auto 1fr; align-items: start; justify-items: stretch; }
  .ficha-premio, .fa2-ficha .ficha-troca, .fa2-usa { display: flex; flex-direction: column; gap: 3px; }
  .ficha-premio { align-items: center; } .fa2-ficha.compara .ficha-premio { align-items: flex-end; text-align: right; }
  .ficha-rotulo { font: 700 11px/1.4 var(--texto); letter-spacing: 0.22em; text-transform: uppercase; color: #8a8070; }
  .ficha-linhas { display: flex; flex-direction: column; font: 19px/1.25 var(--num, var(--texto)); color: #f1e4c4; }
  .ficha-linhas .efeito { color: #c8b0ff; font-size: 16px; }
  .fa2-ficha .ficha-troca { align-items: center; padding: 0 22px; border-left: 1px solid #3a3128; border-right: 1px solid #3a3128; font: 17px/1.3 var(--num, var(--texto)); }
  .ficha-troca .melhor { color: #8fbf6a; } .ficha-troca .pior { color: #e2574c; }
  :root body #sobre-achado .fa2-usa .achado-cartao.atual { width: auto; padding: 0; background: none; border: 0; box-shadow: none; text-align: left; overflow: visible; animation: none; opacity: 0.92; }
  .fa2-usa { gap: 10px; } .fa2-usa .achado-selo { font: 700 11px/1.4 var(--texto); letter-spacing: 0.22em; text-transform: uppercase; color: #8a8070; }
  .ficha-usa-nome { display: flex; align-items: center; gap: 8px; } .ficha-usa-nome b { font: 400 22px/1.05 var(--titulo); }
  .fa2-usa .ficha-linhas { font-size: 17px; } .fa2-usa .ficha-troca { border: 0; padding: 0; align-items: flex-start; font-size: 15px; }
  .ficha-lore { max-width: 620px; font: italic 15px/1.4 var(--texto); color: #a89878; }
  .dir-relicario5 .achado-acoes { display: flex; justify-content: center; gap: 10px; margin-top: 16px; }
  .dir-relicario5.entrando .fa2-altar .achado-arte { animation: fa2-desce 0.27s steps(4) both; }
  @keyframes fa2-desce { from { translate: 0 -40px; } 75% { translate: 0 3px; } to { translate: 0 0; } }
  .dir-relicario5.adiantado .fa2-altar .achado-arte { animation: none; }

  /* os botões destas apresentações: ferro escuro com aresta de latão, sem o cinza em degradê; o foco do teclado
     num anel claro; a área, os estados e as teclas iguais */
  :root body :is(#celebracao, #sobre-achado).dir-relicario5 :is(.continuar, .botao-janela:not(.reserva)) { border: 1px solid #6b5426; border-radius: 0;
    background: #120e0b; color: #eadbb4; text-shadow: 0 1px 0 #000; font: 700 17px/1.1 var(--texto); padding: 9px 16px 9px 12px; min-width: 0;
    box-shadow: inset 0 1px 0 #3a2c18, inset 0 -2px 0 #070504, 0 0 0 1px #000, 0 3px 0 #000; }
  :root body :is(#celebracao, #sobre-achado).dir-relicario5 :is(.continuar, .botao-janela:not(.reserva)):hover { border-color: #d4af37; background: #1d1610; color: #fff3d6; }
  :root body :is(#celebracao, #sobre-achado).dir-relicario5 :is(.continuar, .botao-janela:not(.reserva)):focus-visible { border-color: #f2d27a; color: #fff3d6; outline: 2px solid #f2d27a; outline-offset: 3px; }
  :root body :is(#celebracao, #sobre-achado).dir-relicario5 :is(.continuar, .botao-janela:not(.reserva)):active { translate: 0 1px; box-shadow: inset 0 1px 0 #2b2219, 0 0 0 1px #000, 0 2px 0 #000; }
  :root body :is(#celebracao, #sobre-achado).dir-relicario5 :is(.continuar, .botao-janela) kbd { font: 13px/1 var(--num); color: #f2d27a; border: 1px solid #6b5426; background: #070504; padding: 2px 5px; margin: 0 2px; }
  /* o mágico: um acento azul parado junto do item (o fio com o losango, em azul), sem aura */
  #sobre-achado.dir-relicario5.rar-magico .achado-cartao.novo .achado-arte { position: relative; }
  #sobre-achado.dir-relicario5.rar-magico .achado-cartao.novo .achado-arte::after { content: ""; position: absolute; left: 50%; bottom: -10px; width: 64px; height: 3px;
    translate: -50% 0; background: #3d63c9; box-shadow: 0 1px 0 #000; }
  #sobre-achado.dir-relicario5.rar-magico .achado-cartao.novo .achado-arte::before { content: ""; position: absolute; left: 50%; bottom: -14px; width: 4px; height: 4px; z-index: 1;
    translate: -2px 0; background: #c8e0ff; box-shadow: -2px 2px 0 #7fb0ff, 2px 2px 0 #7fb0ff, 0 4px 0 #c8e0ff, 0 2px 0 #3d63c9; }
  @media (max-height: 760px) {
    .fa2-coroa { gap: 14px; margin-bottom: 14px; } .fa2-medalha { width: 128px; height: 128px; } .fa2-numero { font-size: 64px; }
    .fa2-titulo { font-size: 70px; } .fa2-info { gap: 10px; } .fa2-hab b { font-size: 24px; } .fa2-hab p { font-size: 15px; }
    .fa2-altar { height: 112px; } .ficha-nome { font-size: 32px; }
  }
  @media (prefers-reduced-motion: reduce) {
    .fa2 :is(.fa2-medalha, .fa2-titulo, .fa2-info), .dir-relicario5 .fa2-altar .achado-arte { animation: none !important; }
  }`;
  document.head.insertAdjacentHTML("beforeend", `<style id="estilo-relicario5">${css}</style>`);
  Festa.usar(direcao);
})();

/* Item achado: a janela do saque, por cima do jogo e fora do log, com o feixe na cor da raridade antes do cartão
   (raro e lendário). */
"use strict";

(() => {
  const { h, S, faiscas, htmlItem, iconeItem, noPalco, VAZIO } = Telas;

  const BRILHO_RARIDADE = { comum: ["#f1e4c4", "#c0b8a8"], magico: ["#7fb0ff", "#c8e0ff", "#ffffff"],
    raro: ["#f2c94c", "#fff3a0", "#ffffff"], lendario: ["#ffb35c", "#e0782f", "#fff3a0", "#ffffff"] };
  /** O desenho de um item no cartão: o da interface (Icones), ou o sprite do jogo, no mesmo tamanho. */
  const arte = (sprite, escala) => Icones.porDesenho(sprite, 16 * escala) || S(sprite, escala);
  /** Item encontrado: o cartão dele (sprite, raridade, bônus, diferença para o seu) e, ao lado, o que você usa. */
  function achado(d) {
    const it = d.item;
    const rar = h(it.raridade);
    // O anel: os dois espaços empilhados numa coluna ao lado do achado, cada um com o nome do espaço e o anel que está
    // nele (ou vazio), em cartões baixos: três cartões lado a lado não cabiam e o terceiro quebrava de linha.
    const aneis = d.espacos && (d.equipados || []).length;
    const eq = aneis ? `<div class="achado-aneis">${d.espacos.map((e) => e.item
      ? `<div class="achado-cartao atual compacto rar-${h(e.item.raridade)}" data-espaco="${h(e.espaco)}"><span class="achado-selo">${h(e.nome)} · você usa</span>
          <div class="compacto-corpo"><div class="achado-arte pequena">${arte(iconeItem(e.item), 3)}</div><div>${htmlItem(e.item, "", false)}</div></div></div>`
      : `<div class="achado-cartao atual compacto vazio" data-espaco="${h(e.espaco)}"><span class="achado-selo">${h(e.nome)} · vazio</span>
          <div class="compacto-corpo"><div class="achado-arte pequena">${Icones.vazio(e.espaco, 48) || S(VAZIO[e.espaco], 3, "fantasma")}</div></div></div>`).join("")}</div>`
      : (d.equipados || []).map((e) => `<div class="achado-cartao atual rar-${h(e.raridade)}">
        <span class="achado-selo">Você usa</span>
        <div class="achado-arte pequena">${arte(iconeItem(e), 3)}</div>${htmlItem(e, "", false)}</div>`).join("");
    // Mochila cheia: o que sai do corpo fica para trás (o anel que vai para o espaço vazio não tira nada).
    const aviso = !d.pode_usar || d.cabe ? "" : aneis && d.espacos.some((e) => !e.item)
      ? '<div class="pior">Mochila cheia: substituir um anel deixa o antigo para trás.</div>'
      : '<div class="pior">Mochila cheia: equipar deixa o item antigo para trás.</div>';
    return `<div class="tela achado rar-${rar}">
      <div class="achado-cartao novo rar-${rar}">
        <div class="achado-raios" aria-hidden="true"></div>
        <span class="achado-selo">Você encontrou</span>
        <div class="achado-arte">${arte(iconeItem(it), 4)}</div>
        ${htmlItem(it)}${aviso}
      </div>${eq}</div>`;
  }
  /** O item achado abre numa janela própria, por cima do jogo e fora do log. Como nos ARPGs, o achado é a estrela:
   *  primeiro ele sozinho, no meio da janela (raro e lendário: o feixe de luz cai ali antes); depois ele abre espaço,
   *  o que você usa entra ao lado com a comparação e aparecem os botões (que vêm da pergunta do motor, ver
   *  escolhas.js). A janela já nasce no tamanho final: nada pula, o cartão só começa deslocado para o meio. Ela fecha
   *  quando o ícone pousa (no corpo ou na mochila), ou ao deixar o item. */
  async function abrirAchado(d, semCerimonia = false) {
    fecharAchado();
    const fundo = document.createElement("div");
    fundo.id = "sobre-achado";
    fundo.className = "sobreposicao";
    // Os botões chegam com a pergunta, depois da revelação; até lá, os mesmos rótulos (que vêm com o cartão) guardam o
    // lugar deles, invisíveis: a moldura já nasce no tamanho final e não cresce quando eles chegam.
    const reserva = (d.acoes || []).map((t, i) => `<button type="button" class="botao-janela reserva" tabindex="-1" aria-hidden="true"><kbd>${i + 1}</kbd>${h(t)}</button>`).join("");
    fundo.innerHTML = `<div class="janela-achado">${achado(d)}<div class="achado-acoes">${reserva}</div></div>`;
    document.body.appendChild(fundo);
    const janela = fundo.firstElementChild, tela = janela.querySelector(".tela.achado");
    const novo = tela.querySelector(".achado-cartao.novo");
    noPalco(janela);
    if (semCerimonia) return;
    janela.classList.add("so-o-achado");
    const j = janela.getBoundingClientRect(), c = novo.getBoundingClientRect();
    const desvio = Math.round(j.left + j.width / 2 - (c.left + c.width / 2));  // do lugar dele até o meio da janela
    novo.style.translate = `${desvio}px 0`;
    tela.classList.add("esperando-feixe");
    await Sensacao.cerimoniaSaque(d.item.raridade, novo);
    tela.classList.remove("esperando-feixe");
    revelarAchado(tela, d);
    // Um instante só com o achado; então ele vai para o lado dele e a comparação entra.
    const raro = ["raro", "lendario"].includes(d.item.raridade);
    await new Promise((r) => setTimeout(r, App.ritmo(raro ? 900 : 550)));
    if (!janela.isConnected) return;
    janela.classList.remove("so-o-achado");
    novo.style.translate = "";
    if (desvio) novo.animate([{ translate: `${desvio}px 0` }, { translate: "0 0" }], { duration: App.ritmo(380), easing: "cubic-bezier(.3,.7,.3,1)" });
  }
  /** Onde a pergunta "o que fazer com o item?" põe os botões (null se a janela não está aberta). */
  function acoesDoAchado() { return document.querySelector("#sobre-achado .achado-acoes"); }
  function fecharAchado() {
    const f = document.getElementById("sobre-achado");
    if (!f) return;
    f.id = "";  // a próxima janela (outro item logo em seguida) já pode abrir enquanto esta some
    f.classList.add("saindo");
    setTimeout(() => f.remove(), 220);
  }

  /** O cartão do item aparece de vez: o som da raridade e as faíscas (depois da cerimônia, se houve uma). */
  function revelarAchado(raiz, d) {
    const cartao = raiz.querySelector(".achado-cartao.novo");
    if (!cartao) return;
    const raro = ["raro", "lendario"].includes(d.item.raridade);
    App.som(raro ? "achado_raro" : "achado");
    setTimeout(() => { if (cartao.isConnected) faiscas(cartao.querySelector(".achado-arte"), BRILHO_RARIDADE[d.item.raridade] || BRILHO_RARIDADE.comum, raro ? 22 : 12); }, 260);
  }

  Telas.registrar("achado", achado);

  Object.assign(Telas, { abrirAchado: Festa.abrirAchado, acoesDoAchado, fecharAchado, revelarAchado });  // PROTÓTIPO: a direção
})();
