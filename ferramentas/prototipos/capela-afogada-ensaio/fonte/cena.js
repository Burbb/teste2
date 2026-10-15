"use strict";
/* A Capela Afogada, fora do jogo: duas vistas em 320x72 com as mesmas peças de vista.js (o céu em faixas pontilhadas,
   o astro, as silhuetas tiradas do horizonte, a água do pântano em riscos), mais o que a vila faz com os prédios:
   pontos clicáveis com balão, o lugar que acende no hover e a câmera que chega perto em dobro, num pontilhado. */
(() => {
  const W = 320, H = 72;
  const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
  const pontilha = (x, y, n) => BAYER[(y & 3) * 4 + (x & 3)] < n;
  const rgbDe = (c) => [1, 3, 5].map((i) => parseInt(c.slice(i, i + 2), 16));
  function misturar(a, b, t) {
    const x = rgbDe(a), y = rgbDe(b);
    return "#" + x.map((v, i) => Math.round(v + (y[i] - v) * t).toString(16).padStart(2, "0")).join("");
  }
  function rng(s) { s = (s * 9301 + 49297) % 233280 || 1; return () => (s = (s * 16807) % 2147483647) / 2147483647; }
  function px(c, x, y, w = 1, h = 1, cor) { c.fillStyle = cor; c.fillRect(x | 0, y | 0, w, h); }
  const lerp = (a, b, t) => a + (b - a) * t;
  function novaCamada() { const k = document.createElement("canvas"); k.width = W; k.height = H; return k.getContext("2d"); }

  // ------------------------------------------------------------------ as peças de vista.js
  const CEUS = [
    ["#2c4470", "#45648f", "#7a90b0", "#c09a80", "#e8b88a"],
    ["#24508c", "#33649e", "#4f80b6", "#79a4c8", "#a8c4d6"],
    ["#22163a", "#43264a", "#82363e", "#bc5630", "#ec8c3c"],
    ["#04050c", "#080b1a", "#0d1328", "#121a33", "#18223f"],
  ];
  const ASTROS = [[60, 30, 7, "#ffe8a0", "#f0c890"], [210, 12, 6, "#fff6c8", "#ece2b4"], [248, 40, 10, "#e8784a", "#d8603a"], [70, 14, 5, "#e8ecf4", "#c8ccd8"]];
  /** A cor do céu num ponto (as faixas e a passagem pontilhada entre elas); `alt` estica o céu numa janela. */
  function corDoCeu(bandas, x, y, alt = 50) {
    const f = (Math.min(Math.max(y, 0), alt) / alt) * (bandas.length - 1), i = Math.floor(f), resto = Math.floor((f - i) * 16);
    return pontilha(x, y, resto) ? bandas[Math.min(i + 1, bandas.length - 1)] : bandas[i];
  }
  function ceu(c, p) {
    const bandas = CEUS[p];
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) px(c, x, y, 1, 1, corDoCeu(bandas, x, y));
    const [sx, sy, raio, cor, baixo] = ASTROS[p], halo = misturar(bandas[bandas.length - 2], cor, 0.45);
    for (let y = sy - raio - 6; y <= sy + raio + 6; y++) for (let x = sx - raio - 6; x <= sx + raio + 6; x++) {
      const d = Math.hypot(x - sx, y - sy);
      if (d <= raio) px(c, x, y, 1, 1, y > sy + raio / 3 && pontilha(x, y, 8) ? baixo : cor);
      else if (p !== 3 && d < raio + 5 && pontilha(x, y, Math.round(9 - (d - raio) * 1.6))) px(c, x, y, 1, 1, halo);
    }
    if (p === 3) for (let y = -raio; y <= raio; y++) for (let x = -raio; x <= raio; x++) {
      if ((x - 3) * (x - 3) + (y + 1) * (y + 1) <= raio * raio * 0.8) px(c, sx + x, sy + y, 1, 1, bandas[0]);
    }
    return bandas;
  }
  function perfil(r, base, amp, rug) {
    const ys = []; let y = base, v = 0;
    for (let x = 0; x < W; x++) { v += (r() - 0.5) * rug; v = Math.max(-1.5, Math.min(1.5, v * 0.92)); y += v; y = Math.max(base - amp, Math.min(base + amp * 0.4, y)); ys.push(Math.round(y)); }
    return ys;
  }
  function silhueta(c, ys, cor) { ys.forEach((y, x) => px(c, x, y, 1, H - y, cor)); }
  function nevoa(c, y0, y1, cor, forca, x0 = 0, x1 = W, fase = 0) {
    const meio = (y0 + y1) / 2, meia = (y1 - y0) / 2;
    for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) {
      const n = Math.round(forca * (1 - Math.abs(y - meio) / meia) + Math.sin((x + fase) / 11) * 1.5);
      if (n > 0 && pontilha(x, y, n)) px(c, x, y, 1, 1, cor);
    }
  }
  function arvoreSeca(c, x, y, h, cor, lado = 1) {
    px(c, x, y - h, 1, h, cor);
    for (let i = 0; i < Math.floor(h / 4); i++) {
      const yy = y - h + 2 + i * 4, dir = (i + (lado > 0 ? 0 : 1)) % 2 ? 1 : -1, comp = Math.max(2, 5 - i + ((x + i) % 2));
      for (let k = 0; k < comp; k++) px(c, x + (dir > 0 ? 1 + k : -1 - k), yy - Math.floor(k / 2), 1, 1, cor);
    }
  }
  /** Juncos: talos de um pixel, em tufos; alguns com a espiga no alto. */
  function juncos(c, r, x0, x1, base, alt, cor, espiga, dens) {
    for (let x = x0; x < x1; x++) {
      if (r() > dens) continue;
      const h = Math.max(2, Math.round(alt * (0.45 + r() * 0.65)));
      px(c, x, base - h, 1, h, cor);
      if (espiga && r() < 0.25) px(c, x, base - h - 1, 1, 2, espiga);
    }
  }
  /** O reflexo na água: cada pixel da camada acima da linha d'água, espelhado, escurecido e rareando com a distância. */
  function refletir(c, camada, linha, cor, forca = 9) {
    const d = camada.getImageData(0, 0, W, linha).data;
    for (let y = 0; y < linha; y++) for (let x = 0; x < W; x++) {
      if (!d[(y * W + x) * 4 + 3]) continue;
      const k = linha - y, ry = linha + k - 1;
      if (ry < H && (k < forca || pontilha(x, ry, Math.round(16 - (k - forca) * 1.2)))) px(c, x, ry, 1, 1, cor);
    }
  }

  // ------------------------------------------------------------------ cena 1: a capela vista de fora
  const AGUA = 52;
  const BURACO = { x0: 156, x1: 166 };
  const margemCima = (x) => lerp(61, AGUA, x / 156);  // o dique do canal, do lado do brejo
  const margemBaixo = (x) => lerp(67, AGUA, x / 165);  // o outro dique, onde os sapos esperam
  const SAPOS = [[50, false], [69, true], [91, false], [108, true]];  // x, patas a mais
  const sapoY = (x) => Math.round(margemBaixo(x + 2));
  const TORRE = { x: 116, sino: [119, 18, 6, 8] };

  function fora(p) {
    const c = novaCamada(), r = rng(7);
    const bandas = ceu(c, p), hz = bandas[4], noite = p === 3, sol = ASTROS[p];
    const escuro = (t) => misturar(hz, "#050404", t);
    const longe = escuro(0.45), meio = escuro(0.65), perto = escuro(0.82), chao = escuro(0.9);
    const ladoLuz = noite ? 0 : sol[0] > 160 ? 1 : -1;  // de que lado o sol bate na capela
    const face = noite ? meio : misturar(meio, sol[3], 0.22), sombra = misturar(meio, perto, 0.55);
    const telha = misturar(meio, "#5a1a10", 0.35), telhaEsc = misturar(telha, perto, 0.4);
    const agua = misturar(hz, "#0a1a18", 0.6), brilho = misturar(hz, "#5a7a78", 0.4);
    const frio = misturar("#7aa4c4", meio, noite ? 0.35 : 0.5), negro = "#07080a";
    const lama = misturar(chao, "#4a3a24", 0.35), bruma = misturar(longe, hz, 0.5);
    const cor = { hz, longe, meio, perto, chao, agua, brilho, frio, negro };

    // a outra margem, árvores mortas longe e a névoa rasteira
    silhueta(c, perfil(r, 45, 3, 0.5), longe);
    [[12, 10], [44, 8], [78, 11], [236, 9], [274, 12], [306, 8]].forEach(([x, h], i) => arvoreSeca(c, x, 47, h, misturar(longe, meio, 0.5), i % 2 ? 1 : -1));
    nevoa(c, 44, 52, bruma, 3);
    px(c, 0, AGUA, W, H - AGUA, agua);

    // ---- a capela, numa camada à parte (para o reflexo)
    const L = novaCamada();
    // a torre: o corpo, o lado na sombra, o campanário vazado (o céu aparece onde estava o sino) e a ponta quebrada
    const tx = TORRE.x;
    px(L, tx, 14, 12, AGUA - 14, meio);
    px(L, ladoLuz < 0 ? tx + 9 : tx, 14, 3, AGUA - 14, sombra);
    const [bx, by, bw, bh] = TORRE.sino;
    L.clearRect(bx, by, bw, bh);
    px(L, bx, by, 1, 1, meio); px(L, bx + bw - 1, by, 1, 1, meio);  // o arco do vão
    px(L, bx, by + 2, bw, 1, perto);                                   // a trave do sino
    px(L, bx + 3, by + 3, 1, 2, misturar(perto, "#8a7050", 0.35));     // um toco de corda
    px(L, tx + 5, 30, 2, 4, negro);                                    // a seteira
    for (let i = 0; i < 4; i++) px(L, tx - 1 + i, 13 - i * 2, 14 - i * 2, 2, i % 2 ? telhaEsc : telha);
    px(L, tx + 4, 5, 2, 1, telha); px(L, tx + 6, 4, 1, 1, telhaEsc);  // o que sobrou da ponta, torto
    // a nave: o corpo enfiado na água, o telhado comprido com um rombo (o céu e os caibros), contrafortes
    const nx0 = 128, nx1 = 198;
    px(L, nx0, 36, nx1 - nx0, AGUA - 36, meio);
    for (let y = 29; y <= 35; y++) { const recuo = Math.round((35 - y) * 0.5); px(L, nx0 - 1 + recuo, y, nx1 - nx0 + 2 - recuo * 2, 1, y % 2 ? telha : telhaEsc); }
    px(L, nx0 - 1, 35, nx1 - nx0 + 2, 1, misturar(telha, negro, 0.45));
    [7, 6, 5, 3, 2].forEach((meia, k) => L.clearRect(166 - meia + (k % 2), 29 + k, meia * 2, 1));  // o rombo
    [161, 164, 167, 170].forEach((x) => px(L, x, 29 + (x % 2), 1, 5 - (x % 2), perto));              // os caibros à mostra
    [130, 145, 160, 180, 194].forEach((x) => px(L, x, 38, 2, AGUA - 38, ladoLuz > 0 ? face : sombra));
    // as janelas: arcos altos cortados pela água na metade; dentro, um frio azulado subindo da água
    [135, 149, 170, 185].forEach((x) => {
      px(L, x + 1, 41, 3, 1, negro);
      px(L, x, 42, 5, AGUA - 42, negro); px(L, x, AGUA - 3, 5, 3, frio); px(L, x, AGUA - 4, 5, 1, misturar(frio, negro, 0.5));
      px(L, x + 2, 43, 1, AGUA - 43, sombra);  // o montante do meio
    });
    // o buraco no muro, rente à água: escuro de verdade, com as pedras caídas em volta
    for (let x = BURACO.x0; x < BURACO.x1; x++) {
      const topo = Math.round(45 + Math.abs(x - 160.5) * 0.7 + ((x * 7) % 3) * 0.5);
      px(L, x, topo, 1, AGUA - topo, "#020303");
    }
    [[154, 50, 2], [167, 50, 2], [166, 49, 1], [153, 51, 1]].forEach(([x, y, w]) => px(L, x, y, w, 1, face));
    // a fachada, de três quartos: a empena virada para o sol, o óculo e o arco da porta quase todo sob a lama
    const fx = 198, fw = 17, fc = fx + 8;
    px(L, fx, 36, fw, AGUA - 36, ladoLuz > 0 ? face : sombra);
    for (let y = 27; y <= 35; y++) { const meia = Math.round((y - 27) * 1.0); px(L, fc - meia, y, meia * 2 + 1, 1, ladoLuz > 0 ? face : sombra); px(L, fc - meia - 1, y, 1, 1, telha); px(L, fc + meia + 1, y, 1, 1, telha); }
    px(L, fc, 26, 1, 1, telha);
    px(L, fc - 1, 30, 3, 3, negro); px(L, fc, 31, 1, 1, sombra);  // o óculo
    px(L, fc - 2, 47, 5, 1, sombra); px(L, fc - 3, 48, 1, 2, sombra); px(L, fc + 3, 48, 1, 2, sombra); px(L, fc - 2, 48, 5, 2, negro);  // o alto da porta
    for (let x = 190; x < 236; x++) {  // o monte de lama na frente
      const topo = Math.round(49 + ((x - 210) / 24) ** 2 * 4 + Math.sin(x / 2.2) * 0.5);
      if (topo < AGUA) px(L, x, topo, 1, AGUA - topo, lama);
    }
    refletir(c, L, AGUA, misturar(agua, perto, 0.75), 10);
    for (let y = AGUA + 1; y < H; y += 2) for (let x = (y * 7) % 13; x < W; x += 13 + (y % 5)) px(c, x, y, 3 + (x % 4), 1, brilho);
    c.drawImage(L.canvas, 0, 0);
    // o pátio da frente virou juncal (o reflexo dos juncos é só um risco escuro)
    juncos(c, r, 186, 262, AGUA, 9, perto, chao, 0.55);
    juncos(c, r, 262, 300, AGUA, 6, perto, chao, 0.3);
    juncos(c, r, 100, 128, AGUA, 6, perto, null, 0.35);
    px(c, 186, AGUA + 1, 114, 1, misturar(agua, perto, 0.4));
    px(c, nx0 - 12, AGUA, nx1 - nx0 + 120, 1, misturar(agua, brilho, 0.5));  // a linha d'água no pé das paredes
    for (let x = BURACO.x0; x < BURACO.x1; x++) px(c, x, AGUA, 1, 1, agua);

    // ---- o canal do moleiro: reto, entre o dique (com estacas) e a beira de cá, apontando para o buraco
    const canal = misturar(agua, brilho, 0.35);
    for (let x = 0; x < BURACO.x1; x++) {
      const y0 = Math.round(margemCima(x)), y1 = Math.round(margemBaixo(x)), grosso = x < 80 ? 2 : 1;
      if (y1 > y0) px(c, x, y0, 1, y1 - y0, canal);
      if (x < 154) px(c, x, y0 - grosso, 1, grosso, perto);
      if (x < 160) px(c, x, y1, 1, grosso, perto);
      if (x % 11 === 3 && x < 150) { const h = Math.round(lerp(5, 2, x / 150)); px(c, x, y0 - grosso - h, 1, h, perto); px(c, x + 5, y1 - h + 1, 1, h, perto); }
    }
    // a beira de cá: uma faixa de lama com juncos, embaixo à esquerda
    const beira = perfil(r, 69, 2, 0.5);
    for (let x = 0; x < 120; x++) { const y = beira[x] + Math.max(0, Math.round((x - 70) / 12)); if (y < H) px(c, x, y, 1, H - y, chao); }
    juncos(c, r, 0, 90, 70, 6, misturar(chao, perto, 0.5), null, 0.45);
    arvoreSeca(c, 22, 72, 30, perto, 1);
    arvoreSeca(c, 296, 72, 22, perto, -1);
    juncos(c, r, 250, W, 72, 5, misturar(chao, perto, 0.5), null, 0.4);
    px(c, 236, 66, W - 236, H - 66, chao); for (let x = 228; x < 236; x++) px(c, x, 66 + (236 - x > 4 ? 2 : 1), 1, 6, chao);
    juncos(c, r, 236, W, 67, 6, perto, chao, 0.5);

    return { camada: c, cor, p };
  }

  // ------------------------------------------------------------------ cena 2: a nave alagada, por dentro
  const COLUNAS = [36, 100, 164];
  const REDEMOINHO = { x: 196, y: 58 };
  const SARILHO = { x: 282, y: 24 };  // o alto do poste da esquerda
  const PISO = 43;                     // o chão do presbitério, onde ficam o altar e o sarilho
  function dentro(p) {
    const c = novaCamada(), r = rng(11), bandas = CEUS[p], noite = p === 3;
    const parede = "#15181d", vao = "#0b0d10", pedra = "#2a2f36", pedraLuz = "#3d444d", pedraSombra = "#1c2026", chumbo = "#0e1013";
    const luz = noite ? misturar(bandas[4], "#9aa8c8", 0.6) : misturar(bandas[4], "#e8e0d0", 0.3);
    const agua = "#0b1316", aguaFundo = "#06090b";
    px(c, 0, 0, W, H, parede);
    px(c, 0, 4, W, 1, pedraSombra);
    // os vãos entre as colunas, escuros (a nave lateral), e em cada um uma janela alta com o céu da hora
    const vaos = [[0, COLUNAS[0]], [COLUNAS[0] + 9, COLUNAS[1]], [COLUNAS[1] + 9, COLUNAS[2]], [COLUNAS[2] + 9, 214]];
    const janelas = [];
    vaos.forEach(([a, b], i) => {
      const meio = (a + b) / 2, meia = (b - a) / 2;
      for (let x = a; x < b; x++) {
        const t = Math.min(1, Math.abs(x + 0.5 - meio) / meia), topo = Math.round(5 + 9 * (1 - Math.sqrt(1 - t * t)));
        px(c, x, topo, 1, AGUA_DENTRO - topo, vao);
        px(c, x, topo - 1, 1, 1, pedraLuz);
      }
      if (i > 0) janelas.push([Math.round(meio) - 4, i === 3 ? 18 : 16, 9, i === 3 ? 16 : 20]);
    });
    // a abside, atrás do altar: a janela grande
    px(c, 214, 0, W - 214, PISO, parede);
    janelas.push([254, 8, 13, 24]);
    janelas.forEach(([jx, jy, jw, jh], k) => {
      for (let y = jy; y < jy + jh; y++) for (let x = jx; x < jx + jw; x++) {
        const dx = x + 0.5 - (jx + jw / 2), curva = y - jy < jw / 2 && dx * dx + (y - jy - jw / 2) ** 2 * 1.3 > (jw / 2) ** 2;
        if (curva) continue;
        const quebrado = ((x * 13 + y * 7 + k * 5) % 19) === 0;
        const chumbado = x === jx + Math.floor(jw / 2) || (y - jy) % 7 === 6;
        px(c, x, y, 1, 1, quebrado ? chumbo : chumbado ? chumbo : corDoCeu(bandas, x, Math.round(((y - jy) / jh) * 50)));
      }
    });
    // os fachos de luz descendo das janelas, ralos, até a água
    janelas.forEach(([jx, jy, jw, jh], k) => {
      const ate = k === janelas.length - 1 ? PISO : AGUA_DENTRO + 3;
      for (let y = jy + jh; y < ate; y++) {
        const desv = Math.round((y - jy - jh) * 0.45);
        for (let x = jx + desv; x < jx + jw + desv + 2; x++) if (pontilha(x, y, 2)) px(c, x, y, 1, 1, misturar(luz, parede, noite ? 0.75 : 0.55));
      }
    });
    // o buraco no muro da esquerda: lá fora, o céu e o brejo; por ele entra a água do canal
    for (let y = 26; y < AGUA_DENTRO; y++) for (let x = 2; x < 30; x++) {
      const b = (x - 15) ** 2 / 150 + (y - AGUA_DENTRO) ** 2 / 500 + ((x * 7 + y * 3) % 5) * 0.04;
      if (b > 1) continue;
      px(c, x, y, 1, 1, y >= 46 ? misturar(bandas[4], "#0a1a18", 0.65) : misturar(corDoCeu(bandas, x, Math.round(20 + (y - 26) * 1.4)), "#000000", 0.35));
      if (b > 0.84) px(c, x, y, 1, 1, pedraLuz);
    }
    const fora = misturar(bandas[4], "#050404", 0.82);
    juncos(c, r, 4, 28, 47, 7, fora, null, 0.6);
    px(c, 3, 46, 26, 1, fora);
    // as colunas na frente de tudo, com capitel e base
    COLUNAS.forEach((x) => {
      px(c, x, 0, 9, AGUA_DENTRO, pedra); px(c, x, 0, 2, AGUA_DENTRO, pedraLuz); px(c, x + 7, 0, 2, AGUA_DENTRO, pedraSombra);
      px(c, x - 1, 13, 11, 2, pedraLuz); px(c, x - 1, 15, 11, 1, pedraSombra);
      px(c, x - 1, AGUA_DENTRO - 2, 11, 2, pedra); px(c, x - 1, AGUA_DENTRO - 2, 11, 1, pedraLuz);
    });
    // o presbitério: três degraus subindo da água, e o chão onde ficam o altar e o sarilho
    [[208, 50], [216, 47], [224, PISO + 1]].forEach(([x, y]) => { px(c, x, y, W - x, AGUA_DENTRO - y, pedra); px(c, x, y, W - x, 1, pedraLuz); });
    px(c, 224, PISO, W - 224, 1, pedraLuz);
    // o altar: a pedra, o pano podre, o castiçal caído; a cruz raspada da frente
    px(c, 244, 33, 28, PISO - 33, pedra); px(c, 242, 31, 32, 2, pedraLuz); px(c, 242, 33, 32, 1, pedraSombra);
    px(c, 248, 35, 20, 7, pedraSombra);
    px(c, 257, 36, 2, 5, pedra); px(c, 255, 37, 6, 1, pedra);
    px(c, 246, 33, 6, 1, "#4a1c1a"); px(c, 247, 34, 2, 5, "#4a1c1a"); px(c, 250, 34, 1, 2, "#3a1614");
    px(c, 264, 30, 6, 1, "#6a5a3a"); px(c, 269, 29, 1, 1, "#8a7a4a");
    // a água: escura, mais funda embaixo, com o reflexo das colunas e dos fachos
    for (let y = AGUA_DENTRO; y < H; y++) for (let x = 0; x < W; x++) px(c, x, y, 1, 1, y > 63 || (y > 59 && pontilha(x, y, (y - 59) * 4)) ? aguaFundo : agua);
    px(c, 0, AGUA_DENTRO, W, 1, "#1a2629");
    COLUNAS.forEach((x) => { for (let k = 1; k < 18; k++) if (k < 8 || k % 2) px(c, x + (k > 8 ? (k % 4) - 1 : 0), AGUA_DENTRO + k, 9, 1, misturar(pedraSombra, agua, k / 18)); });
    janelas.slice(0, 3).forEach(([jx, jy, jw, jh]) => {
      const x0 = jx + Math.round((AGUA_DENTRO - jy - jh) * 0.45);
      for (let y = AGUA_DENTRO + 1; y < H - 4; y += 2) px(c, x0 + ((y * 3) % 5) - 2, y, Math.max(2, jw - (y - AGUA_DENTRO) / 2), 1, misturar(luz, agua, 0.55 + (y - AGUA_DENTRO) / 50));
    });
    for (let y = AGUA_DENTRO + 1; y < 60; y += 2) px(c, 4 + ((y * 5) % 6), y, 20 - (y - AGUA_DENTRO), 1, misturar(bandas[4], agua, 0.6));  // o reflexo do buraco
    // os bancos: uma fileira lá atrás, entre as colunas, e a da frente, maior, podre e torta
    const madeira = "#2c2118", madeiraLuz = "#45352a", madeiraEsc = "#1a130e";
    [[50, 14], [70, 22], [112, 16], [134, 22], [176, 14]].forEach(([x, w], i) => {
      px(c, x, 48, 1, 4, madeiraEsc); px(c, x + w - 1, 49, 1, 3, madeiraEsc);
      px(c, x, 48 + (i === 1 ? 1 : 0), w, 1, madeiraLuz); px(c, x, 50, w, 2, madeira);
    });
    [[14, 34, 0], [62, 42, 1], [124, 30, 0]].forEach(([x, w, quebrado]) => {
      for (let k = 0; k < w; k++) {
        if (quebrado && k > 16 && k < 23) continue;
        const caido = quebrado && k >= 23 ? Math.floor((k - 23) / 6) : 0;
        px(c, x + k, 56 + caido, 1, 1, madeiraLuz); px(c, x + k, 57 + caido, 1, 2, madeira);
      }
      [x, x + w - 2].forEach((bx) => { px(c, bx, 53, 2, 9, madeiraEsc); px(c, bx, 53, 2, 1, madeiraLuz); });
      px(c, x, 52, w - (quebrado ? 26 : 0), 1, madeiraEsc);
      for (let k = 0; k < w; k++) if (pontilha(x + k, 63, 6)) px(c, x + k, 63, 1, 1, madeiraEsc);
    });
    return { camada: c, cor: { agua, luz, pedra, pedraLuz, pedraSombra, madeira, madeiraLuz, madeiraEsc } };
  }
  const AGUA_DENTRO = 52;

  // ------------------------------------------------------------------ o que anda
  let quadro = 0, base = null;
  const estado = { cena: "fora", hora: 2, sarilho: "travado", solto: 0, destaque: null, cam: { x: 0, y: 0, s: 1 } };
  const nuvens = [], aves = [], sopros = [], gotas = [], ondas = [];
  (() => {
    const r = rng(3);
    for (let i = 0; i < 5; i++) nuvens.push({ x: r() * (W + 80), y: 6 + Math.floor(r() * 22), w: 40 + r() * 70, v: 0.04 + r() * 0.05 });
    for (let i = 0; i < 2; i++) aves.push({ x: 40 + r() * 200, y: 10 + r() * 14, v: 0.15 + r() * 0.2, f: Math.floor(r() * 8) });
  })();
  function montar() { base = estado.cena === "fora" ? fora(estado.hora) : dentro(estado.hora); }

  function desenharFora(c) {
    const { cor, p } = base;
    c.drawImage(base.camada.canvas, 0, 0);
    const corNuvem = misturar(CEUS[p][1], CEUS[p][3], 0.35);
    nuvens.forEach((n) => { const x = Math.floor(n.x - n.w); px(c, x, n.y, n.w, 1, corNuvem); px(c, x + 6, n.y - 1, n.w - 18, 1, corNuvem); });
    if (p === 3) for (let i = 0; i < 24; i++) { const x = (i * 97 + 13) % W, y = (i * 53) % 30; if ((quadro + i * 3) % 23 > 2 && !(x > 112 && x < 218 && y > 3)) px(c, x, y, 1, 1, "#9aa4c0"); }
    aves.forEach((a, k) => {
      const x = Math.floor(a.x) - 10, y = Math.round(a.y + Math.sin((quadro + k * 9) / 12)), asa = (Math.floor(quadro / 4) + a.f) % 2;
      px(c, x, y, 1, 1, "#0c0606"); px(c, x - 2, y - asa, 2, 1, "#0c0606"); px(c, x + 1, y - asa, 2, 1, "#0c0606");
    });
    // a água do brejo treme: alguns riscos acendem e apagam
    for (let k = 0; k < 10; k++) { const y = AGUA + 2 + ((k * 7) % 18), x = (k * 61 + Math.floor(quadro / 3) * 13) % W; if (y > margemCima(x) + 2 || x > 170) px(c, x, y, 2, 1, cor.brilho); }
    // a correnteza do canal: riscos que andam até o buraco e somem nele
    for (let i = 0; i < 10; i++) {
      const t = (quadro * 0.01 + i / 10) % 1, x = Math.round(lerp(2, 158, t));
      const y0 = margemCima(x), y1 = margemBaixo(x), y = Math.round(lerp(y0 + 1, y1 - 1, ((i * 3) % 5) / 4));
      if (y1 - y0 > 2) px(c, x, y, Math.max(1, Math.round(lerp(4, 1, t))), 1, misturar(cor.brilho, "#c8d8d8", 0.3));
    }
    // o frio do buraco: um bafo azulado e ralo, rente à água, que se espalha e some
    for (let i = 0; i < 7; i++) {
      const t = (quadro * 0.012 + i / 7) % 1, cx = 161 + (i % 2 ? 1 : -1) * t * 20 + Math.sin(i * 2.1 + quadro / 14) * 2, cy = AGUA - 3 - t * 4;
      const raio = 2 + t * 5, n = Math.round(9 * (1 - t));
      for (let y = Math.floor(cy - raio / 2); y <= cy + raio / 2; y++) for (let x = Math.floor(cx - raio); x <= cx + raio; x++) {
        const d = ((x - cx) / raio) ** 2 + ((y - cy) / (raio / 2)) ** 2;
        if (d < 1 && pontilha(x, y, Math.round(n * (1 - d)))) px(c, x, y, 1, 1, "#a8c0d4");
      }
    }
    // os sapos, quietos na beira; os olhos parados, de vez em quando um pisca
    SAPOS.forEach(([sx, mais], i) => {
      const sy = sapoY(sx), corpo = misturar(cor.perto, "#3a4a2a", 0.4), olho = misturar("#c8b860", cor.meio, 0.25);
      const pisca = (quadro + i * 23) % 61 < 2, aceso = estado.destaque === "sapos";
      px(c, sx, sy, 5, 2, corpo); px(c, sx + 1, sy - 1, 3, 1, corpo);
      px(c, sx - 1, sy + 1, 1, 1, corpo); px(c, sx + 5, sy + 1, 1, 1, corpo);
      if (mais) { px(c, sx - 1, sy, 1, 1, corpo); px(c, sx - 2, sy + 1, 1, 1, corpo); px(c, sx + 2, sy + 2, 1, 1, corpo); }
      if (!pisca) { px(c, sx + 1, sy - 1, 1, 1, aceso ? "#fff0a0" : olho); px(c, sx + 3, sy - 1, 1, 1, aceso ? "#fff0a0" : olho); }
    });
    acenderFora(c);
  }
  /** Com o mouse em cima, o lugar acende: alguns pixels, como as janelas da vila. */
  function acenderFora(c) {
    const d = estado.destaque, ouro = "#ffd070", gelo = "#d0e4f4";
    if (d === "buraco") for (let x = BURACO.x0 - 1; x <= BURACO.x1; x++) { const topo = Math.round(45 + Math.abs(x - 160.5) * 0.7 + ((x * 7) % 3) * 0.5); px(c, x, topo - 1, 1, 1, gelo); }
    if (d === "torre") { const [bx, by, bw] = TORRE.sino; px(c, bx, by + 2, bw, 1, ouro); px(c, bx + 3, by + 3, 1, 2, ouro); }
    if (d === "porta") { px(c, 204, 47, 5, 1, ouro); px(c, 203, 48, 1, 2, ouro); px(c, 209, 48, 1, 2, ouro); }
    if (d === "canal") for (let x = 0; x < 150; x += 3) px(c, x, Math.round(margemCima(x)) - 1, 2, 1, ouro);
  }

  // o caminho da corrente: do tambor do sarilho, por cima dos degraus, até o meio do redemoinho
  function pontoDaCorrente(t) {
    const a = [SARILHO.x + 2, SARILHO.y + 9], b = [REDEMOINHO.x, REDEMOINHO.y];
    return [Math.round(lerp(a[0], b[0], t)), Math.round(lerp(a[1], b[1], t) + Math.sin(t * Math.PI) * -2 + (t > 0.55 ? (t - 0.55) * 6 : 0))];
  }
  function desenharDentro(c) {
    const cor = base.cor;
    c.drawImage(base.camada.canvas, 0, 0);
    const soltando = estado.sarilho === "soltando", solto = estado.sarilho === "solto";
    const t = soltando ? Math.min(1, estado.solto / 26) : solto ? 1 : 0;
    // a água do canal entra pelo buraco e corre devagar entre os bancos, até o redemoinho
    const caminho = [[16, 54], [48, 55], [96, 54], [140, 55], [178, 57], [REDEMOINHO.x - 4, REDEMOINHO.y]];
    for (let i = 0; i < 14; i++) {
      const u = (quadro * 0.006 + i / 14) % 1, seg = u * (caminho.length - 1), k = Math.floor(seg), f = seg - k;
      const [x0, y0] = caminho[k], [x1, y1] = caminho[k + 1];
      px(c, Math.round(lerp(x0, x1, f)) - 1, Math.round(lerp(y0, y1, f)) + ((i % 3) - 1) * 2, 3, 1, "#1f3438");
    }
    // o redemoinho: anéis achatados girando em volta de um rasgo escuro
    const { x: rx, y: ry } = REDEMOINHO, velocidade = solto ? 0.06 : 0.16;
    px(c, rx - 4, ry, 9, 1, "#020304"); px(c, rx - 2, ry - 1, 5, 1, "#020304"); px(c, rx - 2, ry + 1, 4, 1, "#03050a");
    for (let anel = 0; anel < 3; anel++) for (let i = 0; i < 6; i++) {
      const a = quadro * velocidade * (1.6 - anel * 0.4) + i * (Math.PI / 3) + anel, raio = 6 + anel * 4;
      px(c, Math.round(rx + Math.cos(a) * raio), Math.round(ry + Math.sin(a) * raio * 0.28), 2, 1, anel === 0 ? "#2c4a50" : "#1f3438");
    }
    if (solto) {  // a corrente foi: lá embaixo, um azul frio que pulsa, e bolhas
      const pulso = 5 + Math.round(3 * Math.sin(quadro / 5));
      for (let y = ry - 2; y <= ry + 2; y++) for (let x = rx - 12; x <= rx + 12; x++) {
        const d = ((x - rx) / 12) ** 2 + ((y - ry) / 2.5) ** 2;
        if (d < 1 && pontilha(x, y, Math.round(pulso * (1 - d)))) px(c, x, y, 1, 1, "#6f9ec0");
      }
      for (let i = 0; i < 4; i++) { const k = (quadro + i * 5) % 12; if (k < 7) px(c, rx - 6 + i * 4, ry - Math.floor(k / 2), 1, 1, "#9ac0d8"); }
    }
    // o sarilho: dois postes, a trave, o tambor com a corrente enrolada, a roda dentada com a trava e a manivela
    const sx = SARILHO.x, sy = SARILHO.y, madeira = "#4a3624", madeiraLuz = "#6a5034", madeiraEsc = "#24190f", ferro = "#3c3e46", ferroLuz = "#8a8c96";
    const giro = soltando ? estado.solto : solto ? 26 : 0, aceso = estado.destaque === "sarilho", ouro = "#ffd070";
    px(c, sx, sy, 2, PISO - sy, madeiraEsc); px(c, sx + 20, sy, 2, PISO - sy, madeiraEsc);
    px(c, sx - 2, sy - 2, 26, 2, madeira); px(c, sx - 2, sy - 2, 26, 1, aceso ? ouro : madeiraLuz);
    px(c, sx + 2, sy + 4, 18, 7, madeira); px(c, sx + 2, sy + 4, 18, 1, madeiraLuz); px(c, sx + 2, sy + 10, 18, 1, madeiraEsc);
    px(c, sx + 2, sy + 3, 1, 9, madeiraEsc); px(c, sx + 19, sy + 3, 1, 9, madeiraEsc);  // as bordas do tambor
    px(c, sx - 1, PISO - 1, 4, 1, madeiraEsc); px(c, sx + 19, PISO - 1, 4, 1, madeiraEsc);  // os pés
    px(c, sx + 2, sy + 2, 1, 1, madeiraEsc); px(c, sx + 19, sy + 2, 1, 1, madeiraEsc); px(c, sx + 1, sy + 14, 20, 1, madeiraEsc);  // a trava de baixo
    const voltas = Math.round(17 * (1 - t));
    for (let i = 0; i < voltas; i++) { const y = sy + 5 + ((i + giro) % 5); px(c, sx + 3 + i, y, 1, 1, (i + giro) % 2 ? ferroLuz : ferro); }
    // a roda dentada do lado de fora do poste e a lingueta: caída entre os dentes (travado) ou erguida (solta)
    for (let k = 0; k < 8; k++) { const a = k * Math.PI / 4 + giro * 0.45; px(c, Math.round(sx - 4 + Math.cos(a) * 3), Math.round(sy + 7 + Math.sin(a) * 3), 1, 1, ferroLuz); }
    px(c, sx - 4, sy + 7, 1, 1, ferro);
    const erguida = estado.sarilho !== "travado";
    px(c, sx - 10, sy + (erguida ? 0 : 3), 5, 1, aceso ? ouro : ferroLuz); px(c, sx - 10, sy + (erguida ? 1 : 4), 1, 2, ferro);
    // a manivela do outro lado: parada, ou girando enquanto a corrente desce
    const ang = soltando ? giro * 0.9 : solto ? 2.3 : -0.7, mx = sx + 23, my = sy + 7;
    const hx = Math.round(mx + Math.cos(ang) * 5), hy = Math.round(my + Math.sin(ang) * 4);
    for (let k = 0; k <= 5; k++) px(c, Math.round(lerp(mx, hx, k / 5)), Math.round(lerp(my, hy, k / 5)), 1, 1, ferroLuz);
    px(c, hx, hy - 1, 2, 2, aceso ? ouro : madeiraLuz); px(c, mx, my, 1, 1, ferro);
    // a corrente: esticada do tambor até o redemoinho; soltando, ela corre elo a elo para dentro; solta, sumiu
    if (t < 1) {
      const passo = 0.022, corre = soltando ? (estado.solto * 0.006) % (passo * 2) : 0;
      for (let u = t; u <= 1; u += passo) {
        const [x, y] = pontoDaCorrente(Math.min(1, u + corre));
        if (Math.round(u / passo) % 2) px(c, x, y, 2, 1, aceso ? "#c8b880" : ferroLuz); else px(c, x, y - 1, 1, 2, ferro);
      }
    }
    // as gotas do teto e as rodas que elas abrem na água
    if (quadro % 8 === 0) gotas.push({ x: [70, 132, 150, 82][(quadro / 8) % 4] + (quadro % 5), y: 4 });
    for (const g of gotas) { g.y += 3; if (g.y < AGUA_DENTRO) px(c, g.x, g.y, 1, 1, "#4a6470"); else if (!g.fim) { g.fim = true; ondas.push({ x: g.x, y: AGUA_DENTRO + 2 + (g.x % 5), r: 0 }); } }
    while (gotas.length && gotas[0].fim) gotas.shift();
    for (const o of ondas) { o.r += 0.5; for (let a = 0; a < 12; a++) { const x = Math.round(o.x + Math.cos(a / 12 * Math.PI * 2) * o.r * 2.4), y = Math.round(o.y + Math.sin(a / 12 * Math.PI * 2) * o.r * 0.5); if (pontilha(x, y, 12 - Math.round(o.r * 3))) px(c, x, y, 1, 1, "#2a4248"); } }
    while (ondas.length && ondas[0].r > 4) ondas.shift();
    acenderDentro(c);
  }
  function acenderDentro(c) {
    const d = estado.destaque, ouro = "#ffd070", gelo = "#d0e4f4";
    if (d === "buraco") for (let y = 26; y < AGUA_DENTRO; y++) for (let x = 1; x < 31; x++) { const b = (x - 15) ** 2 / 150 + (y - AGUA_DENTRO) ** 2 / 500 + ((x * 7 + y * 3) % 5) * 0.04; if (b > 0.84 && b <= 1) px(c, x, y, 1, 1, gelo); }
    if (d === "redemoinho") for (let i = 0; i < 20; i++) { const a = i / 20 * Math.PI * 2; px(c, Math.round(REDEMOINHO.x + Math.cos(a) * 15), Math.round(REDEMOINHO.y + Math.sin(a) * 4), 1, 1, gelo); }
    if (d === "altar") { px(c, 242, 31, 32, 1, ouro); px(c, 257, 36, 2, 5, ouro); px(c, 255, 37, 6, 1, ouro); }
    if (d === "bancos") [[14, 34], [62, 17], [124, 30]].forEach(([x, w]) => px(c, x, 56, w, 1, ouro));
  }

  // ------------------------------------------------------------------ a tela: pixel inteiro, câmera, troca pontilhada
  const canvas = document.getElementById("arte"), palco = document.getElementById("palco"), pontosEl = document.getElementById("pontos");
  const tela = canvas.getContext("2d"), cena = novaCamada(), quadroAtual = novaCamada(), mascara = novaCamada();
  const reduzir = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let escala = 1, troca = null;
  function medir() {
    const dpr = window.devicePixelRatio || 1, k = Math.max(1, Math.floor((palco.clientWidth * dpr) / W));
    escala = k / dpr;
    canvas.width = W * k; canvas.height = H * k;
    canvas.style.width = W * escala + "px"; canvas.style.height = H * escala + "px";
    pontosEl.style.left = (palco.clientWidth - W * escala) / 2 + "px";
    pontosEl.style.width = W * escala + "px"; pontosEl.style.right = "auto";
    posicionarPontos(); pintar();
  }
  function enquadrar(dest, cam) {
    dest.imageSmoothingEnabled = false;
    dest.clearRect(0, 0, W, H);
    dest.drawImage(cena.canvas, cam.x, cam.y, W / cam.s, H / cam.s, 0, 0, W, H);
  }
  function pintar() {
    cena.clearRect(0, 0, W, H);
    (estado.cena === "fora" ? desenharFora : desenharDentro)(cena);
    enquadrar(quadroAtual, estado.cam);
    let fonte = quadroAtual.canvas;
    if (troca) {  // o quadro novo cobre o velho num pontilhado que fecha, como a câmera da vila
      const n = Math.min(16, Math.ceil(((performance.now() - troca.inicio) / 400) * 16));
      mascara.clearRect(0, 0, W, H); mascara.drawImage(quadroAtual.canvas, 0, 0);
      for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (!pontilha(x, y, n)) { const i = (y * W + x) * 4; mascara.fillStyle = `rgb(${troca.velho[i]},${troca.velho[i + 1]},${troca.velho[i + 2]})`; mascara.fillRect(x, y, 1, 1); }
      fonte = mascara.canvas;
      if (n >= 16) troca = null;
    }
    let dx = 0;
    if (estado.sarilho === "soltando" && estado.cena === "dentro" && estado.solto > 4 && estado.solto < 22 && !reduzir) dx = estado.solto % 2 ? 1 : -1;  // o tranco
    tela.imageSmoothingEnabled = false;
    tela.clearRect(0, 0, canvas.width, canvas.height);
    tela.drawImage(fonte, dx, 0, W, H, 0, 0, canvas.width, canvas.height);
  }
  function animarTroca(mudar) {
    troca = { inicio: performance.now(), velho: quadroAtual.getImageData(0, 0, W, H).data };
    mudar();
    const passo = () => { pintar(); if (troca) requestAnimationFrame(passo); };
    requestAnimationFrame(passo);
  }
  /** A câmera chega perto (em dobro, centrada em `foco`) ou volta ao quadro inteiro. */
  function focar(foco) {
    const cam = foco ? { s: 2, x: Math.max(0, Math.min(W / 2, Math.round(foco[0] - W / 4))), y: Math.max(0, Math.min(H / 2, Math.round(foco[1] - H / 4))) } : { s: 1, x: 0, y: 0 };
    const c = estado.cam;
    if (c.s === cam.s && c.x === cam.x && c.y === cam.y) return;
    animarTroca(() => { estado.cam = cam; });
    pontosEl.classList.toggle("focado", !!foco);
  }

  // ------------------------------------------------------------------ o texto, os pontos e as opções
  const TEXTO_FORA = [
    "A capela está afundada até a metade das janelas. Juncos crescem no que foi o pátio da frente, e a porta sumiu sob a lama. O sino não está mais na torre.",
    "O canal que você seguiu desde o moinho termina aqui: a água entra por um buraco no muro e desaparece no escuro lá dentro, sem barulho. Do buraco vem um frio que não é do pântano.",
    "Na beira da água, os sapos estão quietos. Alguns têm patas a mais.",
  ];
  const TEXTO_DENTRO = [
    "Você entra pelo buraco no muro, com a água do canal pelos joelhos. Lá dentro, o salão principal da capela é um lago escuro entre colunas. A água corre devagar entre os bancos podres e some numa fenda do piso, perto do altar.",
  ];
  const SOLTANDO = "Você ergue a lingueta da roda dentada. A manivela dá um tranco e gira sozinha; a corrente corre pelo tambor e desce, elo a elo, para dentro da fenda.";
  const SOLTO = "A ponta some na água. Lá embaixo, alguma coisa pesada se arrasta na pedra, e a fenda acende um azul frio que não estava ali.";
  const PONTOS = {
    fora: [
      { id: "buraco", nome: "Buraco no muro", area: [152, 42, 18, 11], balao: [161, 44], opcao: "Entrar pelo buraco no muro", ir: "dentro" },
      { id: "torre", nome: "Torre", area: [113, 3, 18, 49], balao: [122, 15], foco: [122, 24], opcao: "Olhar a torre",
        texto: "No alto da torre, o vão do sino está vazio. Da trave onde ele pendia sobra um toco de corda podre." },
      { id: "porta", nome: "Porta", area: [192, 40, 36, 12], balao: [206, 45], opcao: "Procurar a porta",
        texto: "A lama subiu até o arco da porta. Só a pedra de cima aparece, e os juncos crescem por cima dela." },
      { id: "canal", nome: "Canal", area: [0, 56, 42, 15], balao: [24, 60], opcao: "Olhar o canal",
        texto: "As estacas do moleiro seguram as margens até aqui. A água vai reta para o buraco, sem fazer onda." },
      { id: "sapos", nome: "Sapos", area: [44, 55, 74, 13], balao: [80, 60], foco: [84, 58], opcao: "Olhar os sapos de perto",
        texto: "Nenhum coaxa. Dois têm patas a mais, nascendo de lado, e não parecem se importar. Todos olham para o buraco." },
    ],
    dentro: [
      { id: "sarilho", nome: "Sarilho", area: [270, 20, 42, 24], balao: [293, 22], foco: [256, 39], opcao: "Soltar a corrente do sarilho", acao: "soltar" },
      { id: "redemoinho", nome: "Fenda", area: [180, 53, 34, 10], balao: [196, 55], opcao: "Olhar onde a água some",
        texto: "A água gira devagar e desce por uma fenda no piso, sem espirrar, como se lá embaixo houvesse muito espaço. A corrente do sarilho entra por ela." },
      { id: "altar", nome: "Altar", area: [240, 28, 36, 15], balao: [258, 30], foco: [256, 34], opcao: "Examinar o altar",
        texto: "O altar ficou acima da água. Alguém raspou a cruz da pedra. Um pano vermelho apodrece no canto." },
      { id: "bancos", nome: "Bancos", area: [12, 52, 146, 12], balao: [80, 55], opcao: "Atravessar entre os bancos",
        texto: "As tábuas cedem com o peso da mão. A água passa por baixo delas, sempre na mesma direção: o altar." },
      { id: "buraco", nome: "Saída", area: [2, 26, 28, 26], balao: [15, 28], opcao: "Voltar pelo buraco no muro", ir: "fora" },
    ],
  };
  const tituloEl = document.getElementById("titulo"), subEl = document.getElementById("sub"), prosaEl = document.getElementById("prosa"), opcoesEl = document.getElementById("opcoes");
  const HORAS = ["Manhã", "Tarde", "Crepúsculo", "Noite"];
  const CENAS = {
    fora: { titulo: "A Capela Afogada", sub: () => `Pântano · ${HORAS[estado.hora]}`, prosa: TEXTO_FORA },
    dentro: { titulo: "Nave Alagada", sub: () => `A Capela Afogada · ${HORAS[estado.hora]}`, prosa: TEXTO_DENTRO },
  };
  let resposta = [];  // os parágrafos de resultado do último clique: [texto, classe]
  function escrever() {
    const cena = CENAS[estado.cena];
    tituloEl.textContent = cena.titulo;
    subEl.textContent = cena.sub();
    prosaEl.replaceChildren();
    cena.prosa.forEach((t) => paragrafo(t));
    resposta.forEach(([t, classe]) => paragrafo(t, classe, true));
    opcoesEl.replaceChildren();
    const lista = opcoesAgora();
    lista.forEach((p, i) => {
      const li = document.createElement("li"), b = document.createElement("button");
      b.type = "button"; b.id = `opcao-${estado.cena}-${p.id}`;
      b.innerHTML = `<kbd>${i + 1}</kbd><span></span>`;
      b.querySelector("span").textContent = p.rotulo || p.opcao;
      b.disabled = !!p.travado;
      b.addEventListener("click", () => escolher(p));
      b.addEventListener("mouseenter", () => destacar(p.id));
      b.addEventListener("mouseleave", () => destacar(null));
      li.appendChild(b); opcoesEl.appendChild(li);
    });
  }
  /** Com a câmera perto, as opções são só a do lugar e o Afastar (como a vila, diante de um prédio). */
  function opcoesAgora() {
    const pontos = PONTOS[estado.cena].map((p) => p.acao === "soltar" ? { ...p, rotulo: rotuloSarilho(), travado: estado.sarilho === "soltando" } : p);
    if (estado.cam.s === 1) return pontos;
    const aqui = pontos.filter((p) => p.id === estado.perto && p.acao);
    return [...aqui, { id: "afastar", opcao: "◀ Afastar", afastar: true }];
  }
  function paragrafo(texto, classe, provisorio) {
    const p = document.createElement("p");
    if (classe) p.className = classe;
    p.textContent = texto;
    if (provisorio) { const s = document.createElement("span"); s.className = "prov"; s.textContent = "texto de teste"; p.appendChild(s); }
    prosaEl.appendChild(p);
  }
  function rotuloSarilho() { return { travado: "Soltar a corrente do sarilho", soltando: "A corrente está descendo…", solto: "Travar de novo (recomeçar o teste)" }[estado.sarilho]; }
  function destacar(id) { if (estado.destaque !== id) { estado.destaque = id; pintar(); } }
  function posicionarPontos() {
    pontosEl.replaceChildren();
    PONTOS[estado.cena].forEach((p) => {
      const b = document.createElement("button");
      b.type = "button"; b.className = "ponto"; b.id = `ponto-${estado.cena}-${p.id}`;
      b.setAttribute("aria-label", p.nome);
      const [x, y, w, h] = p.area;
      Object.assign(b.style, { left: x * escala + "px", top: y * escala + "px", width: w * escala + "px", height: h * escala + "px" });
      const bal = document.createElement("span");
      bal.className = "balao"; bal.textContent = p.nome;
      Object.assign(bal.style, { left: Math.round((p.balao[0] - x) * escala) + "px", top: Math.round((p.balao[1] - y) * escala) + "px" });
      b.appendChild(bal);
      b.addEventListener("mouseenter", () => destacar(p.id));
      b.addEventListener("mouseleave", () => destacar(null));
      b.addEventListener("focus", () => destacar(p.id));
      b.addEventListener("blur", () => destacar(null));
      b.addEventListener("click", () => escolher(p));
      pontosEl.appendChild(b);
    });
  }
  function escolher(p) {
    if (p.afastar) { estado.perto = null; resposta = []; focar(null); escrever(); return; }
    if (p.ir) { irPara(p.ir); return; }
    destacar(null);
    if (p.foco) { estado.perto = p.id; focar(p.foco); }
    if (p.acao === "soltar") {
      if (estado.sarilho === "soltando") return;
      if (estado.sarilho === "solto") { estado.sarilho = "travado"; estado.solto = 0; resposta = []; escrever(); return; }
      estado.sarilho = "soltando"; estado.solto = 0;
      resposta = [[SOLTANDO, "resultado"]];
      escrever();
      return;
    }
    resposta = [[p.texto, "resultado"]];
    escrever();
  }
  function irPara(nome) {
    animarTroca(() => {
      estado.cena = nome; estado.destaque = null; estado.perto = null; estado.cam = { x: 0, y: 0, s: 1 };
      pontosEl.classList.remove("focado");
      montar();
    });
    resposta = [];
    document.querySelectorAll(".abas button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.cena === nome)));
    posicionarPontos(); escrever();
  }

  document.querySelectorAll(".abas button").forEach((b) => b.addEventListener("click", () => { if (b.dataset.cena !== estado.cena) irPara(b.dataset.cena); }));
  document.querySelectorAll(".horas button[data-hora]").forEach((b) => b.addEventListener("click", () => {
    estado.hora = Number(b.dataset.hora);
    document.querySelectorAll(".horas button[data-hora]").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    animarTroca(montar);
    subEl.textContent = CENAS[estado.cena].sub();
  }));
  document.addEventListener("keydown", (ev) => {
    if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
    const lista = opcoesAgora();
    if (ev.key === "Escape" && estado.cam.s !== 1) { escolher({ afastar: true }); return; }
    const p = lista[Number(ev.key) - 1];
    if (p && !p.travado) { ev.preventDefault(); escolher(p); }
  });

  // o relógio da cena: dez passos por segundo
  setInterval(() => {
    if (document.hidden) return;
    quadro++;
    nuvens.forEach((n) => { n.x = (n.x + n.v) % (W + n.w); });
    aves.forEach((a) => { a.x = (a.x + a.v) % (W + 20); });
    if (estado.sarilho === "soltando") {
      estado.solto++;
      if (estado.solto === 27) { estado.sarilho = "solto"; resposta = [[SOLTANDO, "resultado"], [SOLTO, "resultado frio"]]; escrever(); }
    }
    if (!troca) pintar();
  }, 100);

  montar(); escrever();
  new ResizeObserver(medir).observe(palco);
  medir();
})();
