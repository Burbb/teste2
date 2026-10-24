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
