/* Especializações: a identidade visual da festa de cada especialização (etapa 2, 1.201.0), separada da apresentação
   (Estouro ou Relicário: as duas usam as mesmas). Escolhida pelo id da especialização que o motor manda na festa.
     Piromante   o fogo (identidades.js): chamas do topo das letras, brasas.
     Paladino    a luz do alto, em faixas de vitral (marfim, ouro envelhecido, vidros dessaturados), contínua por trás
                 do nome (as letras à frente, com contorno escuro), e penas brancas caindo.
     Berserker   o nome despenca, três garras rasgam o fundo, as bordas batem como um coração; o sangue acumula na
                 letra, escorre um pouco, forma a gota, rompe e cai separado (gotas pequenas, sem poças).
     Patrulheiro o vendaval em verde: uma rajada revela o nome e leva folhas pela composição inteira.
     Sombra      olhos no escuro, o nome aparece aos pedaços, o corte (uma vez) separa e recompõe as metades; depois,
                 a névoa e os olhos em volta.
     Necromante  um círculo de runas se desenha sob o nome, caveiras sobem dele e acendem os olhos, fumaça escura sai
                 das letras.
   Cada uma tem a entrada, o impacto e a acomodação para a leitura; o nome termina parado e legível; com o movimento
   reduzido, um quadro parado próprio. As fontes, as versões descartadas e as alternativas estão em
   ferramentas/prototipos/hud/celebracoes (o jogo não lê essa pasta). */
"use strict";

const Especializacoes = (() => {
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
  const penaCaindo = (x, y, lim, vy = al(0.25, 0.45)) => ({ tipo: "pena", x, y, x0: x, vy, vida: 260, fase: Math.random() * 6,
    mover: (s) => { s.y += s.vy; s.x = s.x0 + Math.sin(s.idade * 0.11 + s.fase) * 5; }, morre: (s) => s.y > lim });
  function desenharPena(p, s) {
    const k = Math.cos(s.idade * 0.11 + s.fase), g = Math.abs(k) < 0.35 ? PENA[0] : Math.abs(k) < 0.75 ? PENA[1] : PENA[2];
    pintar(p, k < 0 && g !== PENA[0] ? espelho(g) : g, Math.round(s.x) - (g[0].length >> 1), Math.round(s.y), PENA_COR);
  }
  const motes = (ex, r, n, t) => ex.soltar(n, () => ({ tipo: "mote", x: r.x + Math.round(al(-r.rx * 1.2, r.rx * 1.2)), y: Math.round(al(0, r.base)), vy: al(0.1, 0.3), vida: Math.round(al(25, 45)) }));

  // ================================================================ BERSERKER
  const SANGUE = { pal: ["p", "R", "r", "D", "D"], cacos: ["R", "r", "D", "D", "k"] };
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
  const BERSERKER = {};

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
  const SOMBRA_ID = {};

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
  };

  // ---- PALADINO: a luz sagrada numa camada própria, translúcida (faixas amplas de marfim e ouro pálido, poucos níveis,
  // pontilhado só nas transições, sem contorno nem base reta) e as penas caindo devagar
  const hash = (n) => { const x = Math.sin(n * 127.1) * 43758.5453; return x - Math.floor(x); };
  const FAIXAS = [  // ângulo a partir da vertical, meia abertura, cor
    [-0.33, 0.05, "#fff1d6"], [-0.2, 0.075, "#f2cf8a"], [-0.07, 0.05, "#fff1d6"], [0.05, 0.085, "#f2cf8a"], [0.18, 0.05, "#fff1d6"], [0.31, 0.065, "#f2cf8a"],
  ];
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

  // ---- BERSERKER: o sangue numa camada logo acima do nome (pode escorrer pela borda das letras). A sequência é sempre
  // a mesma: acumula na letra → escorre um pouco → forma a gota → a ligação se rompe (um vão visível) → a gota cai
  // separada e some antes da descrição. Sem poças.
  const GOTAS = {  // b o corpo, c o ponto de luz, a a sombra do lado de baixo e da direita
    1: { presa: ["b.", "bc", "ba"], caindo: ["b.", "bc", "bb", ".a"] },
    2: { presa: [".b.", "bbc", "bba", ".a."], caindo: [".b.", ".bc", "bbb", "bba", ".a."] },
    3: { presa: ["..b..", ".bbc.", "bbbcb", "bbbba", ".bba."], caindo: ["..b..", ".bbc.", ".bbbc", "bbbbb", "bbbba", ".aaa."] },
  };
  const COR_SANGUE = { b: "r", c: "R", a: "D" };
  // gotas pequenas, escorrimento curto, desprendimento rápido e irregular
  const ESCORRE = {
    d: { pontos: 9, tam: () => 1, espera: () => al(150, 1300), acumula: () => al(4, 8), desce: () => Math.round(al(1, 3)), pescoco: () => Math.round(al(1, 2)), satelite: 0.35 },
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
  BERSERKER.d = {
    ...SANGUE, atenua: 4, classe: "idv-sangue-b",
    quadro(ctx) {  // as garras, as veias e a queda do nome; o sangue escorre na camada de cima (sobre)
      const { p, r, c, t, q, parado, ex, dados } = ctx, cfg = ESCORRE.d;
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

  // ---- PALADINO: a luz do alto com as penas, sem o recorte preto atrás do nome. As letras ficam à frente da luz (a
  // luz é desenhada por baixo do texto), com o contorno escuro e a sombra delas.
  const VITRAL = [  // por faixa, os vidros de cima para baixo (marfim, ouro envelhecido e nuances dessaturadas)
    ["#efe2c4", "#c9a35a", "#b48c86", "#efe2c4"], ["#c9a35a", "#efe2c4", "#8fa59c", "#c9a35a"], ["#efe2c4", "#d8c08c", "#efe2c4", "#a99bb0"],
    ["#d8c08c", "#efe2c4", "#c9a35a", "#efe2c4"], ["#a99bb0", "#efe2c4", "#c9a35a", "#d8c08c"], ["#c9a35a", "#8fa59c", "#efe2c4", "#b48c86"],
  ];
  /** A luz do Paladino: "vitral" (a escolhida) ou "continua" (a alternativa A da sétima rodada, as mesmas faixas sem
   *  os vidros; guardada só para o desenvolvimento, sem opção no jogo; ver o LEIA-ME de ferramentas/prototipos/hud/
   *  celebracoes). */
  const LUZ_DO_PALADINO = "vitral";
  function luzSemRecorte(modo) {
    return (lp, r, t, parado) => {
      const ox = r.x, oy = -lp.t(260), desce = parado ? 1 : rampa(t, 0, 460), fundo = r.base + 2;
      const x0 = Math.max(0, Math.floor(r.x - r.rx * 2.4)), x1 = Math.min(lp.W - 1, Math.ceil(r.x + r.rx * 2.4));
      const mexe = (i) => (parado ? 0 : Math.sin(t / 2700 + i * 1.7) * 0.012);
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
        lp.por(x, y, C(cor));
      }
      const op = parado ? 0.5 : t < 700 ? 0.5 + Math.round(6 * (1 - t / 700)) * 0.02 : 0.47 + Math.round(2 + 2 * Math.sin(t / 1100)) * 0.01;
      lp.el.style.opacity = op.toFixed(2);
    };
  }
  const PALADINO = {
    e: {
      ...LUZ, pal: ["W", "w", "Y", "w", "G"], atenua: 9, semClarao: true, claros: ["W", "w"],
      classe: "idv-luz-a idv-luz-legivel", semPocoRotulo: true,
      luz: luzSemRecorte(LUZ_DO_PALADINO),
      quadro(ctx) {  // a luz numa camada própria (luz); aqui, o anel do pouso, as penas caindo e a poeira de luz
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
      desenhar(p, s) {
        if (s.tipo === "pena") return desenharPena(p, s);
        const k = s.idade / s.vida; if (pt(Math.round(s.x), Math.round(s.y), Math.round(12 * (1 - k)))) p.por(Math.round(s.x), Math.round(s.y), C(k < 0.5 ? "W" : "w"));
      },
      parado: 10,
    },
  };

  // A identidade de cada especialização (as letras são os nomes das versões no protótipo: c a final da sexta rodada,
  // d e e as alternativas da sétima). A paleta é a dos raios ou do estouro da apresentação.
  const POR_CHAVE = { luz: PALADINO.e, sangue: BERSERKER.d, folhas: PATRULHEIRO.c, sombra: SOMBRA_ID.c, almas: NECROMANTE.c };
  const CHAVE = { piromante: "fogo", paladino: "luz", berserker: "sangue", patrulheiro: "folhas", sombra: "sombra", necromante: "almas" };
  const PAL = { fogo: Identidades.PAL.fogo, luz: ["W", "W", "w", "G", "g"], sangue: ["p", "R", "r", "D", "D"],
    folhas: PATRULHEIRO.c.pal, sombra: SOMBRA_ID.c.pal, almas: NECROMANTE.c.pal };

  /** A identidade `id` (a chave: fogo, luz...) para o nome `el`; a apresentação chama `antes` antes do fundo dela e
   *  `quadro(p, t, q, parado)` depois, e lê `atenua` (quanto baixar os raios dela), `pal`/`cacos` e `claros`. */
  function criar(id, el) {
    if (id === "fogo") return Identidades.criar("fogo", el);
    const conc = POR_CHAVE[id];
    if (!conc) return null;
    el.className = el.className.replace(/\bidn-\S+/g, "").trim() + ` idv ${conc.classe}`;
    const alvoContorno = conc.nome ? conc.nome(el) : el;
    const ex = enxame(), dados = {}, rotulo = el.closest(".festa")?.querySelector(".fa2-sobre, .fb2-faixa span");
    let c = null, pronto = false, luz = null, sobre = null;
    if (conc.semPocoRotulo && rotulo) rotulo.classList.add("idv-rotulo-legivel");
    const vazio = { topos: [], bases: [], lados: [], todos: [] };
    return {
      id, semPocoRotulo: !!conc.semPocoRotulo, pal: conc.pal, cacos: conc.cacos, atenua: conc.atenua || 0, semClarao: !!conc.semClarao, claros: conc.claros || null,
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
  /* PALADINO: marfim e ouro (a animação de esfriar fica desligada pelo idv-luz-legivel) */
  .idv-luz-a { ${faixas("#fffdf4", "#f1e4c4", "#e0b870")} filter: ${borda("#8a6a14", "#fff3a0", "#4a3a10")}; }
  :root body .idv.idv-luz-a { animation: idv-esfria 0.8s steps(1) both !important; }
  @keyframes idv-esfria { 0% { filter: brightness(2.6) ${borda("#fff3a0", "#ffffff", "#c0b8a8")}; } 35% { filter: brightness(1.7) ${borda("#f2c94c", "#ffffff", "#8a6a14")}; }
    65% { filter: brightness(1.25) ${borda("#d4af37", "#fff3a0", "#4a3a10")}; } 100% { filter: ${borda("#8a6a14", "#fff3a0", "#4a3a10")}; } }
  /* BERSERKER: o osso e o sangue; o nome despenca */
  .idv-sangue-b { ${faixas("#f1e4c4", "#e8c8b0", "#e2574c")} filter: ${borda("#6e0d0d", "#e2574c", "#2a0a0a")}; }
  :root body .idv.idv-sangue-b { animation: idv-despenca 0.42s steps(1) both !important; }
  @keyframes idv-despenca { 0% { translate: 0 -70px; } 25% { translate: 0 -30px; } 40% { translate: 0 6px; scale: 1.06 0.88; } 55% { translate: 0 -3px; scale: 0.98 1.03; } 75%, 100% { translate: 0 0; scale: 1; } }
  /* PATRULHEIRO: o verde da mata, com luz; no vendaval, o nome aparece com a rajada, da esquerda para a direita */
  .idv-folhas-a { ${faixas("#e8f6c8", "#8fbf6a", "#4f9a5b")} filter: ${borda("#1f4a25", "#8fbf6a", "#0d2010")}; }
  :root body .idv.idv-folhas-a { animation: idv-rajada 0.9s 0.3s steps(9) both !important; }
  @keyframes idv-rajada { from { clip-path: inset(-20% 100% -20% 0); } to { clip-path: inset(-20% -2% -20% 0); } }
  /* SOMBRA: o invisível (as letras aos pedaços) dentro das duas metades do corte, que se separam uma vez */
  :root body .idv.idv-sombra-c { display: inline-grid; animation: none !important; background: none; filter: ${borda("#08090a", "#3a3448", "#08090a")}; }
  .idv-sombra-c > .idv-camada { grid-area: 1 / 1; }
  .idv-sombra-c .idv-letra { display: inline-block; ${faixas("#e2ddd2", "#b0a898", "#7a7080")} animation: idv-surge-c 0.36s var(--d) steps(1) both; }
  @keyframes idv-surge-c { 0% { opacity: 0; } 25% { opacity: 0.3; } 50% { opacity: 0.1; } 75% { opacity: 0.7; } 100% { opacity: 1; } }
  .idv-sombra-c > .idv-cima { clip-path: polygon(-5% -20%, 105% -20%, 105% 30%, -5% 78%); animation: idv-corte-c-cima 1.6s steps(1) both; }
  .idv-sombra-c > .idv-baixo { clip-path: polygon(-5% 78%, 105% 30%, 105% 120%, -5% 120%); animation: idv-corte-c-baixo 1.6s steps(1) both; }
  @keyframes idv-corte-c-cima { 0%, 65% { translate: 0 0; } 66%, 69% { translate: -7px -3px; } 70%, 84% { translate: -14px -6px; } 85%, 88% { translate: -4px -2px; } 89%, 91% { translate: 1px 0; } 92%, 100% { translate: 0 0; } }
  @keyframes idv-corte-c-baixo { 0%, 65% { translate: 0 0; } 66%, 69% { translate: 7px 3px; } 70%, 84% { translate: 14px 6px; } 85%, 88% { translate: 4px 2px; } 89%, 91% { translate: -1px 0; } 92%, 100% { translate: 0 0; } }
  /* PALADINO, sem o recorte: as letras à frente da luz, com o contorno escuro e a sombra delas; o
     rótulo com o contorno, sem a placa */
  .idv-luz-legivel { filter: drop-shadow(2px 0 0 #3a2a0c) drop-shadow(-2px 0 0 #3a2a0c) drop-shadow(0 -2px 0 #6b4b18) drop-shadow(0 2px 0 #1a1206) drop-shadow(0 5px 0 #08090a) !important; }
  :root body .idv.idv-luz-a.idv-luz-legivel { animation: none !important; }
  .idv-rotulo-legivel { text-shadow: 2px 0 #08090a, -2px 0 #08090a, 0 2px #08090a, 0 -2px #08090a, 2px 2px #08090a, -2px 2px #08090a, 2px -2px #08090a, -2px -2px #08090a !important; }
  /* NECROMANTE: verde de túmulo, profundo, com o claro só no alto das letras */
  .idv-almas-a { ${faixas("#e6f2d8", "#a8d48a", "#4f9a5b")} filter: ${borda("#0d2a14", "#4f9a5b", "#050a06")}; }
  @media (prefers-reduced-motion: reduce) {
    :root body .idv, .idv .idv-camada, .idv .idv-letra { animation: none !important; }
  }`;
  document.head.insertAdjacentHTML("beforeend", `<style id="estilo-especializacoes">${css}</style>`);

  return {
    criar,
    /** A chave da identidade da especialização `spec` (o id do motor: "piromante", "paladino"...). */
    chave: (spec) => CHAVE[spec] || null,
    /** A paleta dos raios ou do estouro para a especialização `spec`. */
    pal: (spec) => PAL[CHAVE[spec]] || null,
  };
})();
