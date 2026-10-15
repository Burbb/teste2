/* Protótipo do acampamento (não é o jogo): o acampamento do lado de fora da Capela Afogada como cena do topo, no lugar
   da paisagem, como as salas da capela (telas/cenas.js): o mesmo quadro de 320×72, a mesma escala inteira, o mesmo
   pontilhado e os mesmos dez quadros por segundo. Embaixo ficam só a frase da chegada, a instrução, quem vai e quem
   fica: a imagem não se repete no texto.

   Entra só quando o cenário do protótipo pede (cenario_acampamento.py, PROTOTIPO=1, ou a página fotografada): este
   arquivo vai colado ao fim de /static/telas/fogueira.js e registra de novo a tela "acampamento". O motor, as regras e
   o resto da interface não mudam; os mesmos menus de cada companheiro (Telas.ligarFigurasComitiva) e o mesmo "Dormir
   até o amanhecer".

   A composição, em três planos:
   - longe: o céu da hora (Vista.ceuDo, o mesmo das paisagens e da capela), a outra margem com árvores mortas, a névoa
     rasteira e a capela pequena, afundada até a metade das janelas, com a torre sem sino e o rombo no telhado: a mesma
     capela da cena de fora, vista de longe, à esquerda, apagada (não disputa com o fogo);
   - meio: um teso de terra seca acima do brejo, com o fogo no meio, a luz dele no chão, a roda em volta (cada um
     sentado em alguma coisa: um tronco, uma pedra, a manta) e a sombra de cada um no chão; quem fica no acampamento
     senta mais longe, na beira da luz, perto da barraca;
   - perto: um barranco escuro com capim nos dois cantos de baixo, quase preto.
   Os objetos de viagem são poucos e cada um diz uma coisa: a mochila e o cobertor enrolado ao lado da barraca (vocês
   vão dormir aqui), o cantil encostado no tronco de quem vai com você. Nenhum é clicável nem faz nada. */
"use strict";

(() => {
  const { h, S, ligarFigurasComitiva } = Telas;
  const { pontilha, misturar } = Sprites;
  const QW = 320, QH = 72;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const lerp = (a, b, t) => a + (b - a) * t;
  function rng(s) { s = (s * 9301 + 49297) % 233280 || 1; return () => (s = (s * 16807) % 2147483647) / 2147483647; }
  const pincel = (c) => (x, y, w = 1, hh = 1, cor) => { c.fillStyle = cor; c.fillRect(Math.round(x), Math.round(y), w, hh); };
  function corDoCeu(bandas, x, y, alt = 50) {
    const f = (Math.min(Math.max(y, 0), alt) / alt) * (bandas.length - 1), i = Math.floor(f), resto = Math.floor((f - i) * 16);
    return pontilha(x, y, resto) ? bandas[Math.min(i + 1, bandas.length - 1)] : bandas[i];
  }

  // ---------------------------------------------------------------- onde fica cada coisa (pixels da arte, 320×72)
  // As figuras pelos pés (o meio de baixo do desenho de 16×16). O fogo um pouco à direita do meio: à esquerda dele, o
  // herói e o animal; à direita, quem vai com você (um na frente, outro do outro lado do fogo, mais longe); quem fica,
  // na beira da luz, perto da barraca.
  const FOGO = [166, 60];                      // o meio das toras, na base das chamas
  const HEROI = [140, 63];
  const ATIVOS = [[196, 64], [183, 55]];
  const RESERVA = [[234, 61], [255, 63], [273, 58]];
  const FERA = [120, 66];
  const AGUA = 44;                             // o brejo, atrás do teso
  const CAPELA = 52;                           // o canto esquerdo da nave da capela, longe
  const BARRACA = { x: 298, base: 60, alto: 17, meia: 15 };
  const teso = (x) => Math.round(46 + ((x - 175) / 165) ** 2 * 7 + Math.sin(x / 9) * 0.6);  // a beira de cima da terra seca

  // ---------------------------------------------------------------- a base (o que não se mexe)
  function base(e) {
    const k = document.createElement("canvas"); k.width = QW; k.height = QH;
    const c = k.getContext("2d"), px = pincel(c), r = rng(11);
    const ceu = Vista.ceuDo(e), bandas = ceu.bandas, p = ceu.periodo, noite = p === 3, hz = bandas[bandas.length - 1];
    // as formas saem do horizonte, escurecendo para perto (à noite, com o luar azulado, como a capela de fora)
    const base0 = noite ? misturar(hz, "#6a7a9a", 0.35) : hz, escuro = (t) => misturar(base0, "#050404", noite ? t * 0.85 : t);
    const longe = escuro(0.5), meio = escuro(0.66), perto = escuro(0.86), negro = "#07080a";
    const bruma = misturar(longe, hz, 0.5), agua = misturar(hz, "#0a1a18", 0.62), brilho = misturar(hz, "#5a7a78", 0.4);
    const telha = misturar(meio, "#5a1a10", 0.3);
    const terra = misturar(escuro(0.84), "#3a2a18", noite ? 0.3 : 0.45), terraEsc = misturar(terra, negro, 0.35);
    // o céu e o astro (a lua em quarto sem pintar a sombra: o céu de verdade fica à vista)
    for (let y = 0; y < QH; y++) for (let x = 0; x < QW; x++) px(x, y, 1, 1, corDoCeu(bandas, x, y));
    if (ceu.astro) {
      const [sx, sy, raio, cor, baixo] = ceu.astro, halo = misturar(bandas[bandas.length - 2], cor, 0.45);
      const sombra = (x, y) => noite && (x - sx - 3) ** 2 + (y - sy + 1) ** 2 <= raio * raio * 0.8;
      for (let y = sy - raio - 6; y <= sy + raio + 6; y++) for (let x = sx - raio - 6; x <= sx + raio + 6; x++) {
        const d = Math.hypot(x - sx, y - sy);
        if (d <= raio) { if (!sombra(x, y)) px(x, y, 1, 1, y > sy + raio / 3 && pontilha(x, y, 8) ? baixo : cor); }
        else if (!noite && d < raio + 5 && pontilha(x, y, Math.round(9 - (d - raio) * 1.6))) px(x, y, 1, 1, halo);
      }
    }
    // longe: a outra margem, baixa, com as árvores mortas; a névoa rasteira; a água do brejo
    let y = 41, v = 0;
    for (let x = 0; x < QW; x++) { v += (r() - 0.5) * 0.5; v = Math.max(-1.5, Math.min(1.5, v * 0.92)); y = Math.max(39, Math.min(42, y + v)); px(x, Math.round(y), 1, QH - Math.round(y), longe); }
    [[14, 7], [118, 6], [214, 8], [246, 6], [308, 9]].forEach(([x, hh], i) => arvoreSeca(px, x, 42, hh, misturar(longe, meio, 0.4), i % 2 ? 1 : -1));
    px(0, AGUA, QW, QH - AGUA, agua);
    // a capela, longe: a mesma da cena de fora em miniatura, afundada até a metade das janelas
    capela(px, c, { meio, perto, telha, negro, agua, frio: misturar("#7aa4c4", meio, noite ? 0.45 : 0.6) });
    for (let yy = 40; yy < 47; yy++) for (let x = 0; x < QW; x++) {
      const n = Math.round(2.5 * (1 - Math.abs(yy - 43.5) / 3.5) + Math.sin(x / 13) * 1.5);
      if (n > 0 && pontilha(x, yy, n)) px(x, yy, 1, 1, bruma);
    }
    for (let yy = AGUA + 1; yy < 54; yy += 2) for (let x = (yy * 7) % 11; x < QW; x += 11 + (yy % 4)) px(x, yy, 3 + (x % 4), 1, brilho);
    juncos(px, r, 0, 60, AGUA + 1, 5, meio, 0.35);
    juncos(px, r, 96, 128, AGUA + 1, 4, meio, 0.3);
    juncos(px, r, 214, 320, AGUA + 1, 5, meio, 0.3);
    // meio: o teso de terra seca, de onde a água não chega, com o capim da beira e o chão pisado em volta do fogo
    const beira = misturar(terra, hz, noite ? 0.22 : 0.3);
    for (let x = 0; x < QW; x++) {
      const t = teso(x);
      px(x, t, 1, QH - t, terra);
      px(x, t, 1, 1, beira);                                   // o capim da beira, pegando o céu
      px(x, t + 1, 1, 1, terraEsc);                            // e o barranquinho logo abaixo
      if (t - 1 > AGUA) px(x, t - 1, 1, 1, misturar(agua, brilho, 0.5));  // a água encostando na beira
    }
    for (let yy = 50; yy < QH; yy += 2) for (let x = (yy * 7) % 5; x < QW; x += 5) if (yy > teso(x) + 2) px(x, yy, 1, 1, terraEsc);
    juncos(px, r, 0, 320, 0, 3, misturar(terra, meio, 0.55), 0.22, teso);
    // perto: o barranco escuro nos dois cantos de baixo, mais alto no canto e baixando para dentro, com capim
    const barranco = (x0, x1, alto, lado) => (x) => {
      const t = lado < 0 ? (x - x0) / (x1 - x0) : (x1 - x) / (x1 - x0);  // 0 no canto da tela, 1 na ponta de dentro
      return t >= 1 ? QH : Math.round(QH - alto * (1 - t * t) + Math.sin(x / 3.1) * 0.6);
    };
    const esq = barranco(0, 84, 9, -1), dir = barranco(262, 320, 8, 1);
    for (let x = 0; x < QW; x++) { const yy = Math.min(esq(x), dir(x)); if (yy < QH) px(x, yy, 1, QH - yy, negro); }
    juncos(px, r, 0, 76, 0, 6, negro, 0.5, esq);
    juncos(px, r, 268, 320, 0, 5, negro, 0.45, dir);
    return { canvas: k, noite, periodo: p, bandas, cor: { terra, terraEsc, perto, negro, meio, brilho }, chuva: e.mundo.clima_id };
  }

  /** A capela de longe: a torre com o campanário vazado, a nave com o telhado vermelho apagado e o rombo, as janelas
   *  em arco cortadas pela água, a fachada de lado e o reflexo curto. Poucos pixels, todos da capela da cena de fora. */
  function capela(px, c, k) {
    const x0 = CAPELA, tx = x0 - 7;
    // a torre: o corpo, a ponta do telhado e o vão do sino (o céu aparece nele)
    px(tx, 22, 6, AGUA - 22, k.meio);
    for (let i = 0; i < 3; i++) px(tx - 1 + i, 21 - i * 2, 8 - i * 2, 2, k.telha);
    px(tx + 2, 15, 2, 1, k.telha);
    c.clearRect(tx + 1, 24, 4, 4);
    px(tx + 1, 25, 4, 1, k.perto);
    // a nave: as paredes, o telhado em degraus e o rombo
    px(x0, 33, 34, AGUA - 33, k.meio);
    for (let yy = 29; yy <= 32; yy++) { const recuo = 32 - yy; px(x0 - 1 + recuo, yy, 36 - recuo * 2, 1, k.telha); }
    c.clearRect(x0 + 21, 29, 4, 1); c.clearRect(x0 + 22, 30, 2, 1);
    [x0 + 22, x0 + 24].forEach((x) => px(x, 29, 1, 2, k.perto));
    // as janelas: arcos cortados pela água na metade, com o frio da água dentro
    [x0 + 4, x0 + 12, x0 + 27].forEach((x) => { px(x, 37, 3, AGUA - 37, k.negro); px(x + 1, 36, 1, 1, k.negro); px(x, AGUA - 2, 3, 2, k.frio); });
    // o buraco no muro, rente à água (a entrada)
    px(x0 + 19, 40, 4, AGUA - 40, "#020303");
    // a fachada de lado, com a empena
    px(x0 + 34, 33, 6, AGUA - 33, k.perto);
    for (let i = 0; i < 3; i++) px(x0 + 34 + i, 32 - i, 6 - i * 2, 1, k.perto);
    // o reflexo, escuro e curto
    const ref = misturar(k.agua, k.perto, 0.65);
    for (let i = 1; i < 6; i++) {
      if (i > 3 && i % 2) continue;
      px(tx, AGUA + i, 6, 1, ref); px(x0, AGUA + i, 40, 1, ref);
    }
  }
  function arvoreSeca(px, x, y, hh, cor, lado = 1) {
    px(x, y - hh, 1, hh, cor);
    for (let i = 0; i < Math.floor(hh / 4); i++) {
      const yy = y - hh + 2 + i * 4, dir = (i + (lado > 0 ? 0 : 1)) % 2 ? 1 : -1, comp = Math.max(2, 4 - i);
      for (let k = 0; k < comp; k++) px(x + (dir > 0 ? 1 + k : -1 - k), yy - Math.floor(k / 2), 1, 1, cor);
    }
  }
  /** Juncos (ou capim) em fila: `chao` diz onde cada um nasce (um número fixo ou uma função de x). */
  function juncos(px, r, x0, x1, chao, alt, cor, dens, onde) {
    for (let x = x0; x < x1; x++) {
      if (r() > dens) continue;
      const hh = Math.max(1, Math.round(alt * (0.45 + r() * 0.65))), y0 = onde ? onde(x) : chao;
      px(x, y0 - hh, 1, hh, cor);
    }
  }

  // ---------------------------------------------------------------- o que se mexe
  /** O fogo da fogueira de produção (telas/fogueira.js), com o mesmo desenho, o mesmo movimento e a mesma luz no chão,
   *  só levado para o novo lugar (o centro das toras em FOGO, em vez de 160,98 no palco de 320×120). */
  function luz(px, quadro, b) {
    const [fx, fy] = FOGO, raio = 46 + Math.sin(quadro / 2) * 2 + (reduzido() ? 0 : Math.random() * 2);
    const forca = b.noite ? 1 : b.periodo === 2 ? 0.8 : 0.45;  // de dia, o fogo quase não ilumina o chão
    const tons = ["#5a2e12", "#3a2010", "#24160c"].map((t) => misturar(b.cor.terra, t, forca));
    for (let y = teso(fx) - 2; y < QH; y++) for (let i = fx - 80; i < fx + 80; i++) {
      if (y < teso(i)) continue;
      const dx = (i - fx) / raio, dy = (y - (fy + 2)) / (raio * 0.32), d2 = dx * dx + dy * dy;
      if (d2 < 1 && ((i + y) % 2 === 0 || d2 < 0.45)) px(i, y, 1, 1, d2 < 0.2 ? tons[0] : d2 < 0.5 ? tons[1] : tons[2]);
    }
  }
  function fogo(px, quadro) {
    const dx = FOGO[0] - 160, dy = FOGO[1] - 98, parado = reduzido();
    px(148 + dx, 100 + dy, 24, 3, "#4a2c14"); px(152 + dx, 98 + dy, 16, 2, "#5a3a1c");
    for (let i = 0; i < 9; i++) {
      const fx = 150 + dx + i * 2.4, alt = 6 + (parado ? 5 : Math.random() * 10) + (i > 2 && i < 7 ? 6 : 0);
      px(fx, 98 + dy - alt, 2, alt, "#b3262b"); px(fx, 98 + dy - alt * 0.75, 2, alt * 0.75, "#e0782f");
      if (i > 1 && i < 8) px(fx, 98 + dy - alt * 0.45, 2, alt * 0.45, "#ffd27a");
    }
    for (let i = 0; i < 4; i++) {  // fagulhas e fumaça
      const t = (quadro * 2 + i * 13) % 40;
      if (80 + dy - t < 0) continue;
      px(158 + dx + Math.sin((quadro + i * 7) / 3) * 4, 80 + dy - t, 1, 1, t < 20 ? "#ffb35c" : "rgba(160,150,140,0.5)");
    }
  }

  /** O que cada um usa para sentar (desenhado por cima do pé do desenho: assim a figura fica atrás do tronco ou da pedra,
   *  sentada, e não flutuando) e a sombra no chão, que vai para o lado de fora do fogo. */
  function assento(px, tipo, x, y) {
    const lado = x < FOGO[0] ? -1 : 1, sombra = "rgba(0,0,0,0.42)";
    // a sombra no chão, puxada para o lado de fora do fogo
    px(x - 9 + lado * 3, y + 1, 18, 1, sombra); px(x - 6 + lado * 4, y + 2, 12, 1, "rgba(0,0,0,0.25)");
    if (tipo === "tronco") {  // deitado, mais largo que quem senta: as pontas aparecem dos dois lados, o corte claro
      px(x - 11, y - 2, 22, 2, "#3a2616"); px(x - 11, y - 2, 22, 1, "#55381f"); px(x - 10, y, 20, 1, "#1e140b");
      const fora = lado < 0 ? x - 12 : x + 11, dentro = lado < 0 ? x + 10 : x - 11;
      px(fora, y - 2, 1, 2, "#7a5634"); px(dentro, y - 2, 1, 1, "#8a5a2a");  // o corte de fora; a ponta virada para o fogo, acesa
    } else if (tipo === "pedra") {  // uma pedra chata, a borda de cima acesa do lado do fogo
      px(x - 9, y - 2, 18, 2, "#34343a"); px(x - 7, y - 3, 14, 1, "#4a4846"); px(x - 8, y, 16, 1, "#1a1a1e");
      px(lado < 0 ? x + 3 : x - 7, y - 3, 4, 1, "#6a5a48");
    } else if (tipo === "manta") {  // a manta estendida no chão, de lã escura com uma faixa, saindo para os lados
      px(x - 10, y - 1, 21, 2, "#4a2a2a"); px(x - 10, y - 1, 21, 1, "#6a3a30"); px(x - 9, y + 1, 20, 1, "#2a1818");
      px(x + 7, y - 1, 1, 2, "#8a6a40");
    }
  }
  /** Os objetos de viagem, fixos: a mochila e o cobertor enrolado ao lado da barraca; o cantil encostado no tronco. */
  function bagagem(px) {
    const { x, base: yb } = BARRACA;
    // a barraca: lona esticada num pau, a boca aberta para o fogo, escura por dentro
    for (let k = 0; k < BARRACA.alto; k++) {
      const meia = Math.round((k / BARRACA.alto) * BARRACA.meia);
      px(x - meia, yb - BARRACA.alto + k, meia * 2 + 1, 1, "#2e2418");
      px(x - meia, yb - BARRACA.alto + k, 1, 1, "#5a4630");                  // o lado do fogo, aceso
      px(x + meia, yb - BARRACA.alto + k, 1, 1, "#1a140e");
    }
    for (let k = 4; k < BARRACA.alto; k++) { const m = Math.round(((k - 4) / BARRACA.alto) * 7); px(x - 2 - m, yb - BARRACA.alto + k, m + 1, 1, "#0d0b0a"); }
    px(x, yb - BARRACA.alto - 2, 1, 3, "#5a4630");                           // a ponta do pau
    // a mochila encostada na barraca, com a aba e a alça
    px(x - 20, yb - 6, 6, 6, "#4a3420"); px(x - 20, yb - 6, 6, 2, "#6a4a2c"); px(x - 18, yb - 4, 2, 1, "#2a1c10");
    px(x - 21, yb - 3, 1, 3, "#2a1c10");
    // o cobertor enrolado, amarrado
    px(x - 13, yb - 3, 7, 3, "#5a3030"); px(x - 13, yb - 3, 7, 1, "#7a4438"); px(x - 11, yb - 3, 1, 3, "#2a1810"); px(x - 8, yb - 3, 1, 3, "#2a1810");
  }
  function cantil(px, x, y) { px(x, y - 4, 3, 4, "#5a4a30"); px(x, y - 4, 1, 4, "#7a6440"); px(x + 1, y - 5, 1, 1, "#2a1c10"); }

  /** A luz do fogo em quem está perto: um calor leve na metade do desenho virada para o fogo, só sobre os pixels da
   *  figura (o rosto, o cabelo, o capuz e as cores ficam os mesmos, um pouco mais quentes). Longe da luz, nada. */
  const luzes = new Map();
  function aceso(spr, x, b) {
    const dist = Math.abs(x - FOGO[0]), forca = (b.noite ? 0.22 : b.periodo === 2 ? 0.16 : 0.08) * Math.max(0, 1 - dist / 70);
    if (forca < 0.02) return spr;
    const chave = spr, k = luzes.get(chave) || document.createElement("canvas");
    k.width = k.height = 16;
    const c = k.getContext("2d");
    c.clearRect(0, 0, 16, 16); c.drawImage(spr, 0, 0, 16, 16);
    c.globalCompositeOperation = "source-atop";
    c.fillStyle = `rgba(255,150,70,${forca.toFixed(3)})`;
    if (x < FOGO[0]) c.fillRect(8, 0, 8, 16); else c.fillRect(0, 0, 8, 16);
    c.fillStyle = `rgba(255,150,70,${(forca * 0.5).toFixed(3)})`;
    c.fillRect(0, 0, 16, 16);
    c.globalCompositeOperation = "source-over";
    luzes.set(chave, k);
    return k;
  }

  function desenhar(c, b, d, quadro) {
    const px = pincel(c), q = reduzido() ? 0 : quadro;
    c.drawImage(b.canvas, 0, 0);
    // as nuvens andam devagar; à noite, as estrelas piscam (as mesmas da capela)
    const corNuvem = misturar(b.bandas[1], b.bandas[3], 0.35);
    [[30, 9, 70], [150, 6, 50], [250, 14, 90], [90, 22, 44]].forEach(([x0, y, w], i) => {
      const x = Math.floor(((x0 + q * (0.05 + i * 0.01)) % (QW + 120)) - 60);
      px(x, y, w, 1, corNuvem); px(x + 6, y - 1, w - 18, 1, corNuvem);
    });
    if (b.noite) for (let i = 0; i < 24; i++) { const x = (i * 97 + 13) % QW, y = (i * 53) % 30; if ((q + i * 3) % 23 > 2) px(x, y, 1, 1, "#9aa4c0"); }
    // a água treme
    for (let k = 0; k < 6; k++) { const y = AGUA + 1 + ((k * 3) % 5), x = (k * 61 + Math.floor(q / 3) * 13) % QW; if (y < teso(x)) px(x, y, 2, 1, b.cor.brilho); }
    luz(px, quadro, b);
    bagagem(px);
    // quem senta, de trás para a frente (o de trás do fogo fica atrás das chamas)
    const heroi = App.estado && App.estado.heroi;
    const quem = [{ spr: heroi ? heroi.classe : "guerreiro", p: HEROI, sobre: "tronco" }];
    d.ativos.forEach((m, i) => quem.push({ spr: m.id, p: ATIVOS[i % 2], sobre: i % 2 ? "pedra" : "tronco" }));
    d.reserva.forEach((m, i) => quem.push({ spr: m.id, p: RESERVA[i % 3], sobre: i % 3 === 0 ? "manta" : "pedra", longe: true }));
    if (d.fera) quem.push({ spr: d.fera.tipo === "falcao" ? "voador" : "fera", p: FERA, sobre: null });
    const atras = quem.filter((f) => f.p[1] < FOGO[1]), frente = quem.filter((f) => f.p[1] >= FOGO[1]);
    const figura = (f) => {
      const [x, y] = f.p, spr = Icones.figura(f.spr);
      if (!f.sobre) { px(x - 7, y, 14, 1, "rgba(0,0,0,0.45)"); px(x - 5, y + 1, 10, 1, "rgba(0,0,0,0.3)"); }
      if (spr) c.drawImage(aceso(spr, x, b), x - 8, y - 16, 16, 16);
      if (f.longe) {  // na beira da luz, um véu de penumbra (de leve: o rosto continua reconhecível)
        c.save(); c.globalAlpha = 0.18; px(x - 8, y - 16, 16, 16, "#05060a"); c.restore(); }
      if (f.sobre) assento(px, f.sobre, x, y);
    };
    atras.sort((a, z) => a.p[1] - z.p[1]).forEach(figura);
    if (d.ativos.length) cantil(px, ATIVOS[0][0] + 10, ATIVOS[0][1]);
    fogo(px, quadro);
    frente.sort((a, z) => a.p[1] - z.p[1]).forEach(figura);
    // chuva ou neve por cima de tudo (o fogo continua: a cena é a mesma)
    if (["chuva", "tempestade"].includes(b.chuva)) for (let i = 0; i < 40; i++) { const x = (i * 37 + q * 3) % QW, y = (i * 23 + q * 6) % QH; px(x, y, 1, 3, "rgba(170,190,220,0.6)"); }
    if (b.chuva === "neve") for (let i = 0; i < 30; i++) { const x = (i * 41 + Math.floor(q / 2)) % QW, y = (i * 29 + q) % QH; px(x, y, 1, 1, "#f0f4ff"); }
  }

  // ---------------------------------------------------------------- a tela (embaixo) e os pontos (sobre a arte)
  function rodape(d) {
    const quem = (m) => `<span class="fr-nome">${h(m.nome.split(" ").pop())}${m.ferido_txt ? ` <small>(${h(m.ferido_txt)})</small>` : ""}${m.fora ? ` <small>(${h(m.fora.curto)})</small>` : ""}</span>`;
    const lista = (ms) => ms.length ? ms.map(quem).join(", ") : '<span class="fr-ninguem">ninguém</span>';
    return `<div class="fogueira-rodape">
        <div class="fr-cab"><span class="fr-instrucao">Clique num companheiro para conversar ou ajustar a comitiva.</span><span class="fr-contador">${h(d.contador)}</span></div>
        <div class="fr-linha vai"><b>Vai com você:</b> ${lista(d.ativos)}</div>
        ${d.reserva.length ? `<div class="fr-linha fica"><b>No acampamento:</b> ${lista(d.reserva)}</div>` : ""}
      </div>`;
  }
  function tela(d) {
    const figuras = d.ativos.length + d.reserva.length;
    return `<div class="tela acampamento proto-acampamento">${d.intro ? `<p class="sussurro">${h(d.intro)}</p>` : ""}
      ${figuras ? rodape(d) : '<div class="dica-uso">Só você, o fogo e os barulhos da mata. Quem você encontrar pelo caminho pode se sentar aqui um dia.</div>'}</div>`;
  }

  let atual = null;  // { d, b, capa }
  function capaDe(d) {
    const capa = document.createElement("div");
    capa.id = "acamp-capa";
    const figuras = [];
    d.ativos.forEach((m, i) => figuras.push({ ...m, onde: "ativo", p: ATIVOS[i % 2] }));
    d.reserva.forEach((m, i) => figuras.push({ ...m, onde: "reserva", p: RESERVA[i % 3] }));
    capa.innerHTML = figuras.map((f) => `<button type="button" class="figura ${f.onde}${f.conversa ? " tem-conversa" : ""}" data-cid="${h(f.id)}" data-x="${f.p[0]}" data-y="${f.p[1]}">
        <span class="figura-nome">${h(f.nome.split(" ").pop())}${f.conversa ? '<i class="carta-aviso">✉</i>' : ""}</span></button>`).join("")
      + (d.fera ? `<span class="figura fera" role="button" tabindex="0" data-fera="1" data-x="${FERA[0]}" data-y="${FERA[1]}"><span class="figura-nome">${h(d.fera.nome.split(" ").pop())}</span></span>` : "")
      + `<button type="button" class="dormir-barraca">${S("lua", 1)} Dormir até o amanhecer</button>`;
    return capa;
  }
  /** As figuras e os nomes sobre a arte, pela mesma conta do desenho (Vista.caixaDaArte), a cada mudança de tamanho. */
  function posicionar() {
    if (!atual || !atual.capa.isConnected) return;
    const q = Vista.caixaDaArte();
    if (!q) return;
    const capa = atual.capa;
    Object.assign(capa.style, { left: q.esq + "px", top: q.topo + "px", width: q.larg + "px", height: q.alt + "px" });
    capa.querySelectorAll(".figura").forEach((f) => {
      const x = +f.dataset.x, y = +f.dataset.y;
      Object.assign(f.style, { left: q.dx + (x - 8) * q.ex + "px", top: q.dy + (y - 16) * q.ey + "px", width: 16 * q.ex + "px", height: 16 * q.ey + "px" });
    });
    acomodarNomes(capa, q);
  }
  /** Os nomes onde couberem, como na fogueira de produção (acomodarNomes, telas/fogueira.js), na caixa da arte. */
  function acomodarNomes(capa, q) {
    const P = capa.getBoundingClientRect();
    const ret = (x, y, w, hh) => ({ l: x, t: y, r: x + w, b: y + hh });
    const daArte = (x, y, w, hh) => ret(q.dx + x * q.ex, q.dy + y * q.ey, w * q.ex, hh * q.ey);
    const relativo = (r) => ret(r.left - P.left, r.top - P.top, r.width, r.height);
    const area = (a, b) => Math.max(0, Math.min(a.r, b.r) - Math.max(a.l, b.l)) * Math.max(0, Math.min(a.b, b.b) - Math.max(a.t, b.t));
    const figuras = [...capa.querySelectorAll(".figura")];
    const obstaculos = [daArte(HEROI[0] - 8, HEROI[1] - 16, 16, 16), daArte(FOGO[0] - 14, FOGO[1] - 22, 28, 26),
      ...figuras.map((f) => relativo(f.getBoundingClientRect()))];
    const dormir = capa.querySelector(".dormir-barraca");
    if (dormir) obstaculos.push(relativo(dormir.getBoundingClientRect()));
    figuras.forEach((f) => {
      const nome = f.querySelector(".figura-nome");
      if (!nome) return;
      nome.classList.remove("posto"); nome.style.left = nome.style.top = "";
      const s = relativo(f.getBoundingClientRect()), w = nome.offsetWidth, hh = nome.offsetHeight, cx = (s.l + s.r) / 2;
      const opcoes = [ret(cx - w / 2, s.t - hh - 2, w, hh), ret(cx - w / 4, s.t - hh - 2, w, hh), ret(cx - (3 * w) / 4, s.t - hh - 2, w, hh),
        ret(s.r + 2, s.t + 2, w, hh), ret(s.r + 2, s.b - hh, w, hh), ret(s.l - w - 2, s.t + 2, w, hh), ret(s.l - w - 2, s.b - hh, w, hh),
        ret(cx - w / 2, s.b + 1, w, hh)];
      const dentro = (c) => c.l >= 2 && c.t >= 2 && c.r <= P.width - 2 && c.b <= P.height - 2;
      const custo = (c) => (dentro(c) ? 0 : 1e6) + obstaculos.reduce((n, o) => n + (o === s ? 0 : area(c, o)), 0);
      const livre = opcoes.find((c) => custo(c) === 0) || opcoes.reduce((m, c) => (custo(c) < custo(m) ? c : m));
      nome.classList.add("posto");
      nome.style.left = livre.l - s.l + "px";
      nome.style.top = livre.t - s.t + "px";
      obstaculos.push(livre);
    });
  }
  Vista.aoRedimensionar(posicionar);

  function ligar(raiz, d) {
    App.ultimaFogueira = d;
    requestAnimationFrame(() => mostrar(d));
  }
  function mostrar(d) {
    const cena = document.getElementById("cena");
    if (atual && atual.capa) atual.capa.remove();
    const e = App.estado || { mundo: { periodo_n: 3, clima_id: "limpo" } };
    const b = base(e), capa = capaDe(d);
    atual = { d, b, capa };
    cena.classList.add("acamp-proto", "com-ambiente");
    cena.classList.remove("recolhido");
    cena.appendChild(capa);
    Vista.usarAmbiente(atual.ambiente = { base: b.canvas, foco: null, desenhar: (ctx, quadro) => desenhar(ctx, b, d, quadro) });
    ligarFigurasComitiva(capa, d);
    requestAnimationFrame(posicionar);
  }
  function desligar() {
    if (!atual) return;
    atual.capa.remove();
    const cena = document.getElementById("cena");
    cena.classList.remove("acamp-proto");
    if (!(window.Cenas && Cenas.atual())) { cena.classList.remove("com-ambiente"); Vista.usarAmbiente(null); }
    atual = null;
  }
  // a tela saiu (a conversa, a manhã, outro lugar): a paisagem volta; a tela voltou com outro ambiente por cima: o
  // acampamento volta para o topo
  setInterval(() => {
    const aqui = document.querySelector("#texto .proto-acampamento");
    if (!aqui) { desligar(); return; }
    if (atual && !Vista.temAmbiente()) mostrar(atual.d);
  }, 250);

  const estilo = document.createElement("style");
  estilo.textContent = `
    #cena.acamp-proto[data-tipo="menu"] #vista { display: block; }
    #acamp-capa { position: absolute; z-index: 2; pointer-events: none; }
    #acamp-capa .figura { position: absolute; transform: none; pointer-events: auto; }
    #acamp-capa .dormir-barraca { pointer-events: auto; }
    body.em-combate #acamp-capa { display: none; }`;
  document.head.appendChild(estilo);

  Telas.registrar("acampamento", tela, { ligar });
  window.AcampamentoProto = { FOGO, HEROI, ATIVOS, RESERVA, FERA, atual: () => atual };
})();
