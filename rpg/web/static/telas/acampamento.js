/* Acampamento: a cena da fogueira desenhada na arte do topo (o mesmo quadro de 320×72 da paisagem e das salas da capela,
   a mesma escala inteira, o mesmo pontilhado e os mesmos dez quadros por segundo). Só o desenho: a tela, as figuras
   clicáveis e o Dormir moram em telas/fogueira.js.

   A composição (aprovada no protótipo de 15/10/2026, ferramentas/prototipos/acampamento/), em três planos:
   - longe: o lugar. Na Capela Afogada, o entorno desenhado à mão: a outra margem com árvores mortas, a névoa rasteira e
     a capela pequena, afundada até a metade das janelas, apagada à esquerda (não disputa com o fogo). Nos outros
     lugares, a paisagem do próprio lugar (o céu da hora e as silhuetas do bioma, de vista.js), com o que passa nela;
   - meio: um teso de terra seca, com o fogo, a luz dele no chão e a roda, cada um sentado em alguma coisa (um tronco,
     uma pedra, a manta), com a sombra no chão; quem fica no acampamento senta na beira da luz, perto da barraca;
   - perto: o barranco escuro com capim nos dois cantos de baixo.
   Os objetos de viagem são poucos e cada um diz uma coisa: a barraca, a mochila e o cobertor enrolado ao lado dela, o
   cantil encostado no tronco de quem vai com você. Nenhum é clicável nem faz nada. O fogo é o da fogueira de antes (o
   mesmo desenho, movimento e luz), levado para o meio do teso. */
"use strict";

const Acampamento = (() => {
  const { pontilha, misturar } = Sprites;
  const QW = 320, QH = 72;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  function rng(s) { s = (s * 9301 + 49297) % 233280 || 1; return () => (s = (s * 16807) % 2147483647) / 2147483647; }
  const pincel = (c) => (x, y, w = 1, hh = 1, cor) => { c.fillStyle = cor; c.fillRect(Math.round(x), Math.round(y), w, hh); };
  function camada() { const k = document.createElement("canvas"); k.width = QW; k.height = QH; return k; }
  function corDoCeu(bandas, x, y, alt = 50) {
    const f = (Math.min(Math.max(y, 0), alt) / alt) * (bandas.length - 1), i = Math.floor(f), resto = Math.floor((f - i) * 16);
    return pontilha(x, y, resto) ? bandas[Math.min(i + 1, bandas.length - 1)] : bandas[i];
  }

  // ---------------------------------------------------------------- onde fica cada coisa (pixels da arte, 320×72)
  // As figuras pelos pés (o meio de baixo do desenho de 16×16). O fogo um pouco à direita do meio: à esquerda dele, o
  // herói e o animal; à direita, quem vai com você (um na frente, outro do outro lado do fogo, mais longe); quem fica,
  // na beira da luz, perto da barraca. As áreas de 16×16 não se encostam (os pontos clicáveis são elas).
  const FOGO = [166, 60];                      // o meio das toras, na base das chamas
  const HEROI = [140, 63];
  const ATIVOS = [[200, 64], [183, 55]];
  const RESERVA = [[234, 61], [255, 63], [273, 58]];
  const FERA = [120, 66];
  const BARRACA = { x: 298, base: 60, alto: 17, meia: 15 };
  const teso = (x) => Math.round(46 + ((x - 175) / 165) ** 2 * 7 + Math.sin(x / 9) * 0.6);  // a beira de cima da terra seca

  /** As cores da hora: as formas saem do horizonte e escurecem para perto (à noite, com o luar azulado, como a capela
   *  de fora). */
  function paleta(e) {
    const ceu = Vista.ceuDo(e), bandas = ceu.bandas, p = ceu.periodo, noite = p === 3, hz = bandas[bandas.length - 1];
    const base0 = noite ? misturar(hz, "#6a7a9a", 0.35) : hz, escuro = (t) => misturar(base0, "#050404", noite ? t * 0.85 : t);
    const longe = escuro(0.5), meio = escuro(0.66), perto = escuro(0.86), negro = "#07080a";
    const terra = misturar(escuro(0.84), "#3a2a18", noite ? 0.3 : 0.45);
    return { ceu, bandas, p, noite, hz, longe, meio, perto, negro, terra, terraEsc: misturar(terra, negro, 0.35),
      agua: misturar(hz, "#0a1a18", 0.62), brilho: misturar(hz, "#5a7a78", 0.4) };
  }

  // ---------------------------------------------------------------- longe: o entorno de cada lugar
  // A Capela Afogada tem o entorno desenhado à mão; os outros lugares, a paisagem deles (vista.js). Um lugar novo com
  // fundo próprio entra aqui, pela chave do lugar que o motor manda (dados.lugar).
  const AGUA = 44;    // o brejo da capela, atrás do teso
  const CAPELA = 52;  // o canto esquerdo da nave da capela, longe
  const ENTORNOS = {
    capela_afogada: {
      fundo: fundoCapela,
      // as nuvens andam devagar; à noite, as estrelas piscam (as mesmas da capela de fora); a água do brejo treme
      vivo(c, q, k) {
        const px = pincel(c), corNuvem = misturar(k.bandas[1], k.bandas[3], 0.35);
        [[30, 9, 70], [150, 6, 50], [250, 14, 90], [90, 22, 44]].forEach(([x0, y, w], i) => {
          const x = Math.floor(((x0 + q * (0.05 + i * 0.01)) % (QW + 120)) - 60);
          px(x, y, w, 1, corNuvem); px(x + 6, y - 1, w - 18, 1, corNuvem);
        });
        if (k.noite) for (let i = 0; i < 24; i++) { const x = (i * 97 + 13) % QW, y = (i * 53) % 30; if ((q + i * 3) % 23 > 2) px(x, y, 1, 1, "#9aa4c0"); }
        for (let i = 0; i < 6; i++) { const y = AGUA + 1 + ((i * 3) % 5), x = (i * 61 + Math.floor(q / 3) * 13) % QW; if (y < teso(x)) px(x, y, 2, 1, k.brilho); }
      },
      agua: AGUA,
    },
  };
  function fundoCapela(k) {
    const t = camada(), c = t.getContext("2d"), px = pincel(c), r = rng(11);
    const { bandas, noite, longe, meio, perto, negro, agua, brilho, hz } = k;
    const bruma = misturar(longe, hz, 0.5), telha = misturar(meio, "#5a1a10", 0.3);
    // o céu e o astro (a lua em quarto sem pintar a sombra: o céu de verdade fica à vista)
    for (let y = 0; y < QH; y++) for (let x = 0; x < QW; x++) px(x, y, 1, 1, corDoCeu(bandas, x, y));
    if (k.ceu.astro) {
      const [sx, sy, raio, cor, baixo] = k.ceu.astro, halo = misturar(bandas[bandas.length - 2], cor, 0.45);
      const sombra = (x, y) => noite && (x - sx - 3) ** 2 + (y - sy + 1) ** 2 <= raio * raio * 0.8;
      for (let y = sy - raio - 6; y <= sy + raio + 6; y++) for (let x = sx - raio - 6; x <= sx + raio + 6; x++) {
        const d = Math.hypot(x - sx, y - sy);
        if (d <= raio) { if (!sombra(x, y)) px(x, y, 1, 1, y > sy + raio / 3 && pontilha(x, y, 8) ? baixo : cor); }
        else if (!noite && d < raio + 5 && pontilha(x, y, Math.round(9 - (d - raio) * 1.6))) px(x, y, 1, 1, halo);
      }
    }
    // a outra margem, baixa, com as árvores mortas; a névoa rasteira; a água do brejo
    let y = 41, v = 0;
    for (let x = 0; x < QW; x++) { v += (r() - 0.5) * 0.5; v = Math.max(-1.5, Math.min(1.5, v * 0.92)); y = Math.max(39, Math.min(42, y + v)); px(x, Math.round(y), 1, QH - Math.round(y), longe); }
    [[14, 7], [118, 6], [214, 8], [246, 6], [308, 9]].forEach(([x, hh], i) => arvoreSeca(px, x, 42, hh, misturar(longe, meio, 0.4), i % 2 ? 1 : -1));
    px(0, AGUA, QW, QH - AGUA, agua);
    capela(px, c, { meio, perto, telha, negro, agua, frio: misturar("#7aa4c4", meio, noite ? 0.45 : 0.6) });
    for (let yy = 40; yy < 47; yy++) for (let x = 0; x < QW; x++) {
      const n = Math.round(2.5 * (1 - Math.abs(yy - 43.5) / 3.5) + Math.sin(x / 13) * 1.5);
      if (n > 0 && pontilha(x, yy, n)) px(x, yy, 1, 1, bruma);
    }
    for (let yy = AGUA + 1; yy < 54; yy += 2) for (let x = (yy * 7) % 11; x < QW; x += 11 + (yy % 4)) px(x, yy, 3 + (x % 4), 1, brilho);
    juncos(px, r, 0, 60, AGUA + 1, 5, meio, 0.35);
    juncos(px, r, 96, 128, AGUA + 1, 4, meio, 0.3);
    juncos(px, r, 214, 320, AGUA + 1, 5, meio, 0.3);
    return t;
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
  /** Nos outros lugares, a paisagem do próprio lugar atrás do teso: parada para a base, viva (nuvens, névoa, corvos) no
   *  desenho de cada quadro. */
  function fundoDaPaisagem(k) {
    const t = camada(), c = t.getContext("2d"), cam = Vista.camadas();
    if (cam) { c.drawImage(cam.fundo, 0, 0); c.drawImage(cam.frente, 0, 0); }
    else for (let y = 0; y < QH; y++) for (let x = 0; x < QW; x++) pincel(c)(x, y, 1, 1, corDoCeu(k.bandas, x, y));
    return t;
  }
  function arvoreSeca(px, x, y, hh, cor, lado = 1) {
    px(x, y - hh, 1, hh, cor);
    for (let i = 0; i < Math.floor(hh / 4); i++) {
      const yy = y - hh + 2 + i * 4, dir = (i + (lado > 0 ? 0 : 1)) % 2 ? 1 : -1, comp = Math.max(2, 4 - i);
      for (let j = 0; j < comp; j++) px(x + (dir > 0 ? 1 + j : -1 - j), yy - Math.floor(j / 2), 1, 1, cor);
    }
  }
  /** Juncos (ou capim) em fila: cada um nasce em `chao` (ou onde `onde(x)` disser). */
  function juncos(px, r, x0, x1, chao, alt, cor, dens, onde) {
    for (let x = x0; x < x1; x++) {
      if (r() > dens) continue;
      const hh = Math.max(1, Math.round(alt * (0.45 + r() * 0.65))), y0 = onde ? onde(x) : chao;
      px(x, y0 - hh, 1, hh, cor);
    }
  }

  // ---------------------------------------------------------------- meio e perto: o teso e o barranco
  /** O teso de terra seca, com o capim da beira e o chão pisado; `agua`: a altura da água atrás (a beira molhada). */
  function camadaTeso(k, agua) {
    const t = camada(), px = pincel(t.getContext("2d")), r = rng(11);
    const beira = misturar(k.terra, k.hz, k.noite ? 0.22 : 0.3);
    for (let x = 0; x < QW; x++) {
      const y = teso(x);
      px(x, y, 1, QH - y, k.terra);
      px(x, y, 1, 1, beira);                                                        // o capim da beira, pegando o céu
      px(x, y + 1, 1, 1, k.terraEsc);                                               // e o barranquinho logo abaixo
      if (agua && y - 1 > agua) px(x, y - 1, 1, 1, misturar(k.agua, k.brilho, 0.5));  // a água encostando na beira
    }
    for (let yy = 50; yy < QH; yy += 2) for (let x = (yy * 7) % 5; x < QW; x += 5) if (yy > teso(x) + 2) px(x, yy, 1, 1, k.terraEsc);
    juncos(px, r, 0, 320, 0, 3, misturar(k.terra, k.meio, 0.55), 0.22, teso);
    return t;
  }
  /** O barranco escuro nos dois cantos de baixo, mais alto no canto e baixando para dentro, com capim. */
  function camadaPerto(k) {
    const t = camada(), px = pincel(t.getContext("2d")), r = rng(23);
    const barranco = (x0, x1, alto, lado) => (x) => {
      const u = lado < 0 ? (x - x0) / (x1 - x0) : (x1 - x) / (x1 - x0);  // 0 no canto da tela, 1 na ponta de dentro
      return u >= 1 ? QH : Math.round(QH - alto * (1 - u * u) + Math.sin(x / 3.1) * 0.6);
    };
    const esq = barranco(0, 84, 9, -1), dir = barranco(262, 320, 8, 1);
    for (let x = 0; x < QW; x++) { const yy = Math.min(esq(x), dir(x)); if (yy < QH) px(x, yy, 1, QH - yy, k.negro); }
    juncos(px, r, 0, 76, 0, 6, k.negro, 0.5, esq);
    juncos(px, r, 268, 320, 0, 5, k.negro, 0.45, dir);
    return t;
  }

  // ---------------------------------------------------------------- o fogo e a roda
  /** A luz da fogueira no chão: os anéis pontilhados que tremem, como antes; de dia, mais fraca. */
  function luz(px, quadro, k) {
    const [fx, fy] = FOGO, raio = 46 + Math.sin(quadro / 2) * 2 + (reduzido() ? 0 : Math.random() * 2);
    const forca = k.noite ? 1 : k.p === 2 ? 0.8 : 0.45;
    const tons = ["#5a2e12", "#3a2010", "#24160c"].map((t) => misturar(k.terra, t, forca));
    for (let y = teso(fx) - 2; y < QH; y++) for (let i = fx - 80; i < fx + 80; i++) {
      if (y < teso(i)) continue;
      const dx = (i - fx) / raio, dy = (y - (fy + 2)) / (raio * 0.32), d2 = dx * dx + dy * dy;
      if (d2 < 1 && ((i + y) % 2 === 0 || d2 < 0.45)) px(i, y, 1, 1, d2 < 0.2 ? tons[0] : d2 < 0.5 ? tons[1] : tons[2]);
    }
  }
  /** As toras, as chamas e as fagulhas, com o desenho e o movimento da fogueira de antes (o centro das toras em FOGO,
   *  onde antes era 160,98 no palco de 320×120). Com movimento reduzido, as chamas ficam paradas. */
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
  /** O que cada um usa para sentar, desenhado por cima do pé do desenho (a figura fica sentada atrás do tronco ou da
   *  pedra, não flutuando), e a sombra no chão, puxada para o lado de fora do fogo. */
  function assento(px, tipo, x, y) {
    const lado = x < FOGO[0] ? -1 : 1;
    px(x - 9 + lado * 3, y + 1, 18, 1, "rgba(0,0,0,0.42)"); px(x - 6 + lado * 4, y + 2, 12, 1, "rgba(0,0,0,0.25)");
    if (tipo === "tronco") {  // deitado, mais largo que quem senta: as pontas aparecem dos dois lados, o corte claro
      px(x - 11, y - 2, 22, 2, "#3a2616"); px(x - 11, y - 2, 22, 1, "#55381f"); px(x - 10, y, 20, 1, "#1e140b");
      const fora = lado < 0 ? x - 12 : x + 11, dentro = lado < 0 ? x + 10 : x - 11;
      px(fora, y - 2, 1, 2, "#7a5634"); px(dentro, y - 2, 1, 1, "#8a5a2a");  // o corte de fora; a ponta do lado do fogo, acesa
    } else if (tipo === "pedra") {  // uma pedra chata, a borda de cima acesa do lado do fogo
      px(x - 9, y - 2, 18, 2, "#34343a"); px(x - 7, y - 3, 14, 1, "#4a4846"); px(x - 8, y, 16, 1, "#1a1a1e");
      px(lado < 0 ? x + 3 : x - 7, y - 3, 4, 1, "#6a5a48");
    } else if (tipo === "manta") {  // a manta estendida no chão, de lã escura com uma faixa, saindo para os lados
      px(x - 10, y - 1, 21, 2, "#4a2a2a"); px(x - 10, y - 1, 21, 1, "#6a3a30"); px(x - 9, y + 1, 20, 1, "#2a1818");
      px(x + 7, y - 1, 1, 2, "#8a6a40");
    }
  }
  /** A barraca, a mochila e o cobertor enrolado ao lado dela: fixos, ninguém mexe neles. */
  function bagagem(px) {
    const { x, base: yb } = BARRACA;
    for (let i = 0; i < BARRACA.alto; i++) {  // a lona esticada num pau, a boca aberta para o fogo
      const meia = Math.round((i / BARRACA.alto) * BARRACA.meia);
      px(x - meia, yb - BARRACA.alto + i, meia * 2 + 1, 1, "#2e2418");
      px(x - meia, yb - BARRACA.alto + i, 1, 1, "#5a4630");                    // o lado do fogo, aceso
      px(x + meia, yb - BARRACA.alto + i, 1, 1, "#1a140e");
    }
    for (let i = 4; i < BARRACA.alto; i++) { const m = Math.round(((i - 4) / BARRACA.alto) * 7); px(x - 2 - m, yb - BARRACA.alto + i, m + 1, 1, "#0d0b0a"); }
    px(x, yb - BARRACA.alto - 2, 1, 3, "#5a4630");                             // a ponta do pau
    px(x - 20, yb - 6, 6, 6, "#4a3420"); px(x - 20, yb - 6, 6, 2, "#6a4a2c"); px(x - 18, yb - 4, 2, 1, "#2a1c10");  // a mochila
    px(x - 21, yb - 3, 1, 3, "#2a1c10");
    px(x - 13, yb - 3, 7, 3, "#5a3030"); px(x - 13, yb - 3, 7, 1, "#7a4438"); px(x - 11, yb - 3, 1, 3, "#2a1810"); px(x - 8, yb - 3, 1, 3, "#2a1810");  // o cobertor
  }
  function cantil(px, x, y) { px(x, y - 4, 3, 4, "#5a4a30"); px(x, y - 4, 1, 4, "#7a6440"); px(x + 1, y - 5, 1, 1, "#2a1c10"); }
  /** A luz do fogo em quem está perto: um calor leve na metade do desenho virada para o fogo, só sobre os pixels da
   *  figura (rosto, cabelo, capuz e cores ficam os mesmos, um pouco mais quentes). Longe da luz, nada. */
  function aquecido(spr, x, k) {
    const forca = (k.noite ? 0.22 : k.p === 2 ? 0.16 : 0.08) * Math.max(0, 1 - Math.abs(x - FOGO[0]) / 70);
    if (forca < 0.02) return spr;
    const t = document.createElement("canvas"); t.width = t.height = 16;
    const c = t.getContext("2d");
    c.drawImage(spr, 0, 0, 16, 16);
    c.globalCompositeOperation = "source-atop";
    c.fillStyle = `rgba(255,150,70,${forca.toFixed(3)})`;
    if (x < FOGO[0]) c.fillRect(8, 0, 8, 16); else c.fillRect(0, 0, 8, 16);
    c.fillStyle = `rgba(255,150,70,${(forca * 0.5).toFixed(3)})`;
    c.fillRect(0, 0, 16, 16);
    return t;
  }

  /** Quem senta onde: o herói, quem vai com você, quem fica e o animal, cada um com a vaga, o assento e o id do ponto
   *  clicável (o herói não tem ponto). */
  function roda(d, heroi) {
    const quem = [{ spr: heroi || "guerreiro", p: HEROI, sobre: "tronco" }];
    d.ativos.forEach((m, i) => quem.push({ id: m.id, spr: m.id, p: ATIVOS[i % 2], sobre: i % 2 ? "pedra" : "tronco" }));
    d.reserva.forEach((m, i) => quem.push({ id: m.id, spr: m.id, p: RESERVA[i % 3], sobre: i % 3 === 0 ? "manta" : "pedra", longe: true }));
    if (d.fera) quem.push({ id: "fera", spr: d.fera.tipo === "falcao" ? "voador" : "fera", tipo: d.fera.tipo, p: FERA, sobre: null });
    return quem;
  }
  /** A área de um ponto na arte (o desenho e o assento): o contorno do destaque e o botão por cima. */
  const area = ([x, y]) => [x - 8, y - 17, 16, 19];

  /** A cena montada para o que o motor mandou (`d`, o painel "acampamento") e o estado de agora (`e`): a base parada
   *  (a cor do chão que continua embaixo da arte sai da última linha dela) e o desenho de cada quadro. */
  function montar(e, d, heroi) {
    const k = paleta(e), ent = ENTORNOS[d.lugar];
    const longe = ent ? ent.fundo(k) : fundoDaPaisagem(k), meio = camadaTeso(k, ent && ent.agua), perto = camadaPerto(k);
    const base = camada(), bc = base.getContext("2d");
    [longe, meio, perto].forEach((t) => bc.drawImage(t, 0, 0));
    // o animal pela figura do tipo (Icones.figuraAnimal; o lobo desde a 1.170.0, o urso e o falcão desde a 1.176.0), senão o sprite; enquanto o arquivo
    // carrega, a figura entra no primeiro quadro em que estiver pronta
    const quem = roda(d, heroi).map((f) => {
      const animal = f.tipo ? Icones.figuraAnimal(f.tipo) : "";
      const spr = animal === "" ? Icones.figura(f.spr) : animal;
      return { ...f, spr: spr && aquecido(spr, f.p[0], k), pendente: animal === null };
    });
    const atras = quem.filter((f) => f.p[1] < FOGO[1]).sort((a, z) => a.p[1] - z.p[1]);
    const frente = quem.filter((f) => f.p[1] >= FOGO[1]).sort((a, z) => a.p[1] - z.p[1]);
    function desenhar(c, quadro, destaque) {
      const px = pincel(c), q = reduzido() ? 0 : quadro;
      if (ent) { c.drawImage(longe, 0, 0); ent.vivo(c, q, k); } else Vista.paisagem(c);
      c.drawImage(meio, 0, 0);
      luz(px, quadro, k);
      bagagem(px);
      const figura = (f) => {
        const [x, y] = f.p;
        if (f.pendente) {
          const spr = Icones.figuraAnimal(f.tipo);
          if (spr) { f.spr = aquecido(spr, x, k); f.pendente = false; }
        }
        if (!f.sobre) { px(x - 7, y, 14, 1, "rgba(0,0,0,0.45)"); px(x - 5, y + 1, 10, 1, "rgba(0,0,0,0.3)"); }
        if (f.spr) c.drawImage(f.spr, x - 8, y - 16, 16, 16);
        if (f.longe) { c.save(); c.globalAlpha = 0.18; px(x - 8, y - 16, 16, 16, "#05060a"); c.restore(); }  // a penumbra, de leve
        if (f.sobre) assento(px, f.sobre, x, y);
      };
      atras.forEach(figura);
      if (d.ativos.length) cantil(px, ATIVOS[0][0] + 12, ATIVOS[0][1]);
      fogo(px, quadro);
      frente.forEach(figura);
      c.drawImage(perto, 0, 0);
      Vista.chuva(c);
      // o destaque: o contorno dourado das salas da capela em quem está sob o mouse ou o foco, ou em todos com F4
      const acesos = document.body.classList.contains("destacar-interacoes") ? quem.filter((f) => f.id) : quem.filter((f) => f.id && f.id === destaque);
      if (window.Cenas) acesos.forEach((f) => Cenas.cantos(c, area(f.p)));
    }
    return { base, desenhar, pontos: quem.filter((f) => f.id).map((f) => ({ id: f.id, area: area(f.p) })) };
  }

  return { montar, FOGO, HEROI, area };
})();
