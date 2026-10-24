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

  const CONCEITOS = { luz: PALADINO, sangue: BERSERKER, folhas: PATRULHEIRO, sombra: SOMBRA_ID, almas: NECROMANTE };
  const NOMES = {
    luz: { a: "Luz do alto", b: "Asas" }, sangue: { a: "O nome sangra", b: "Garras" }, folhas: { a: "Vendaval", b: "Clareira" },
    sombra: { a: "Corte", b: "Invisível" }, almas: { a: "Erguer", b: "Almas" },
    // as candidatas finais
    final: { luz: "Luz e penas", sangue: "Garras, sangue líquido", folhas: "Vendaval verde", sombra: "Invisível com o corte", almas: "Erguer com a fumaça" },
  };

  /** A identidade `id` na versão `v` ("a" ou "b") para o nome `el`; a apresentação chama `quadro(p, t, q, parado)`
   *  depois do fundo dela e lê `atenua` (quanto baixar os raios dela) e `pal`/`cacos`. */
  function criar(id, el, v) {
    const conc = CONCEITOS[id] && CONCEITOS[id][v];
    if (!conc) return null;
    el.className = el.className.replace(/\bidn-\S+/g, "").trim() + ` idv ${conc.classe}`;
    const alvoContorno = conc.nome ? conc.nome(el) : el;
    const ex = enxame(), dados = {}, rotulo = el.closest(".festa")?.querySelector(".fa2-sobre, .fb2-faixa span");
    let c = null, pronto = false, luz = null;
    const vazio = { topos: [], bases: [], lados: [], todos: [] };
    return {
      id, versao: v, pal: conc.pal, cacos: conc.cacos, atenua: conc.atenua || 0, semClarao: !!conc.semClarao, claros: conc.claros || null,
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
        if (rotulo) { const l = p.de(rotulo); FX.poco(p, { cx: l.x, cy: l.y, rx: l.rx + 10, ry: l.ry + 5, forca: 16 }); }
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
