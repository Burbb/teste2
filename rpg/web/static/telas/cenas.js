/* Cenas interativas: um lugar desenhado em pixel art (como as paisagens: escala inteira, pontilhado de Bayer, dez
   quadros por segundo) com pontos clicáveis por cima. Os ambientes da Capela Afogada (roadmapIDEIAS/20): o exterior,
   o salão alagado, a sacristia, o ossuário com o sarilho e o fundo alagado com Ilse. O motor diz qual ambiente, o estado dele (a água do salão
   inquieta ou quieta, as correntes presas ou soltas) e o que cada ponto faz (a mesma ação do menu, ou nada); clicar
   aproxima a câmera e manda a ação; a tela não decide nada. A corrente desce na tela só quando o motor avisa que o
   preparo foi gravado (celebrar "correntes"). Um ponto "de olhar" (os sapos) só aproxima e afasta. */
"use strict";

(() => {
  const { h } = Telas;
  const QW = 320, QH = 72;  // o quadro desenhado (o tamanho das paisagens); a tela pode ser mais larga: o lugar continua
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const pontilha = (x, y, n) => Sprites.pontilha(x, y, n);
  const misturar = (a, b, t) => Sprites.misturar(a, b, t);
  const lerp = (a, b, t) => a + (b - a) * t;
  function rng(s) { s = (s * 9301 + 49297) % 233280 || 1; return () => (s = (s * 16807) % 2147483647) / 2147483647; }
  function camada(W) { const k = document.createElement("canvas"); k.width = W; k.height = QH; return k; }
  const pincel = (c) => (x, y, w = 1, hh = 1, cor) => { c.fillStyle = cor; c.fillRect(Math.round(x), Math.round(y), w, hh); };
  /** O céu do lugar agora (período e clima), o mesmo das paisagens. */
  function ceuAgora() {
    const e = App.estado && App.estado.mundo ? App.estado : { mundo: { periodo_n: 1, clima_id: "limpo" } };
    return Vista.ceuDo(e);
  }
  function corDoCeu(bandas, x, y, alt = 50) {
    const f = (Math.min(Math.max(y, 0), alt) / alt) * (bandas.length - 1), i = Math.floor(f), resto = Math.floor((f - i) * 16);
    return pontilha(x, y, resto) ? bandas[Math.min(i + 1, bandas.length - 1)] : bandas[i];
  }

  // ================================================================ o ossuário
  const COR = {
    abobada: "#101317", parede: "#1c2026", junta: "#14171b", pedra: "#2a2f36", pedraLuz: "#3d444d", pedraSombra: "#181b20",
    nicho: "#0b0d10", osso: "#c8c0a8", ossoSombra: "#8a8270", chao: "#23272d", chaoJunta: "#181b1f",
    madeira: "#2a2018", madeiraLuz: "#4a3a2a", madeiraEsc: "#120e0a", ferro: "#4a4c54", ferroLuz: "#9a9ca6",
    agua: "#05080a", aguaLuz: "#1f3034", ouro: "#ffd070", gelo: "#d0e4f4",
  };
  const PISO = 56;
  const SAR = { x: 196, y: 22 };                   // o canto de cima do sarilho (postes, trave, tambor)
  const BURACO = { x: 240, y: 64, rx: 19, ry: 4 }; // o buraco no chão por onde descem as correntes, com a água lá embaixo
  const DESCIDA = { x0: 50, x1: 80 };              // a boca da escada que segue descendo até a água do fundo
  const TOCHA = { x: 186, y: 12 };                 // a tocha na parede, entre os nichos e o sarilho: a luz da sala

  function baseOssuario(W) {
    const k = camada(W), c = k.getContext("2d"), px = pincel(c), ox = Math.round((W - QW) / 2);
    // a parede de pedra em blocos e a abóbada baixa
    px(0, 0, W, QH, COR.parede);
    for (let y = 8; y < PISO; y += 6) for (let x = ((y / 6) % 2) * 7 - 14; x < W; x += 14) { px(x, y, 14, 1, COR.junta); px(x, y, 1, 6, COR.junta); }
    for (let x = 0; x < W; x++) {
      const t = ((((x - ox) % 80) + 80) % 80) / 80, alt = Math.round(7 - 6 * Math.sin(t * Math.PI));
      px(x, 0, 1, alt, COR.abobada); px(x, alt, 1, 1, COR.pedraLuz);
    }
    // os nichos com os ossos (alguns vazios: os que faltam estavam de pé no meio da sala)
    for (let fila = 0; fila < 2; fila++) for (let k2 = 0; k2 < 8; k2++) {
      const x = ox + 54 + k2 * 16, y = 16 + fila * 15;
      px(x, y, 12, 9, COR.nicho); px(x, y - 1, 12, 1, COR.pedraLuz);
      if ((k2 * 7 + fila * 5) % 6 === 0) continue;  // vazio
      if ((k2 + fila) % 3 === 0) {  // um crânio
        px(x + 3, y + 2, 6, 5, COR.osso); px(x + 4, y + 7, 4, 1, COR.ossoSombra);
        px(x + 4, y + 4, 1, 1, COR.nicho); px(x + 7, y + 4, 1, 1, COR.nicho);
      } else {  // ossos longos empilhados
        px(x + 1, y + 4, 10, 1, COR.osso); px(x + 2, y + 6, 9, 1, COR.ossoSombra); px(x + 1, y + 3, 2, 2, COR.osso); px(x + 9, y + 3, 2, 2, COR.osso);
      }
    }
    // A escada de pedra que desce do alçapão, encostada na parede da esquerda: a boca do alçapão na abóbada, com a luz
    // de cima; os degraus com o piso claro e o espelho na sombra, um abaixo e à direita do outro, apoiados num maciço
    // de pedra que vai até o chão (a lateral da escada, em blocos).
    const ax = ox + 4;
    px(ax, 0, 18, 3, "#050607"); px(ax - 1, 3, 20, 1, COR.pedraLuz); px(ax, 0, 1, 3, COR.pedra); px(ax + 17, 0, 1, 3, COR.pedra);
    const DEGRAUS = 10, passo = (PISO - 6) / DEGRAUS;
    for (let k2 = 0; k2 < DEGRAUS; k2++) {
      const x = ax + 1 + k2 * 4, y = Math.round(5 + k2 * passo), alto = Math.round(5 + (k2 + 1) * passo) - y;
      // o maciço embaixo deste degrau, até o chão, em blocos
      px(x, y + 1, 5, PISO - y - 1, "#22262c");
      for (let yy = y + 3; yy < PISO; yy += 4) px(x + ((yy + k2) % 2 ? 0 : 2), yy, 3, 1, "#181b20");
      px(x, y + 1, 4, alto, "#30363e");                  // o espelho, de frente
      px(x, y + 1, 1, alto, "#3a414a");
      px(x, y, 8, 1, "#59616c");                         // o piso do degrau (passa por cima do próximo)
      px(x + 4, y + 1, 1, alto, "#101215");              // a quina que dá a profundidade
    }
    px(ax + 1 + DEGRAUS * 4, PISO - 1, 6, 1, "#59616c");  // o último degrau encosta no chão
    // Pelo alçapão, só o que vem da sacristia: de dia, um cinza frio nos três primeiros degraus; à noite, nada.
    if (ceuAgora().periodo !== 3) for (let k2 = 0; k2 < 3; k2++) px(ax + 1 + k2 * 4, Math.round(5 + k2 * passo), 7 - k2, 1, misturar("#59616c", "#9aa4ae", 0.35 - k2 * 0.1));
    // a sombra da escada na parede, acompanhando os degraus
    for (let k2 = 0; k2 < DEGRAUS; k2++) { const x = ax + 9 + k2 * 4, y = Math.round(5 + k2 * passo); px(x, y - 3, 1, 3, "#15181c"); }
    // o chão, com os ossos dos que caíram
    for (let y = PISO; y < QH; y++) px(0, y, W, 1, y === PISO ? COR.pedraLuz : COR.chao);
    for (let y = PISO + 3; y < QH; y += 5) for (let x = (y * 3) % 10; x < W; x += 14) px(x, y, 9, 1, COR.chaoJunta);
    [[ox + 98, 64], [ox + 120, 68], [ox + 146, 62], [ox + 170, 66]].forEach(([x, y], i) => {
      px(x, y, 9, 1, COR.osso); px(x + (i % 2 ? 8 : 0), y - 1, 2, 2, COR.osso);
      if (i === 1) { px(x + 12, y - 4, 5, 4, COR.osso); px(x + 13, y - 3, 1, 1, COR.nicho); px(x + 15, y - 3, 1, 1, COR.nicho); }
    });
    // A escada continua: logo depois do último degrau, a boca retangular no chão por onde ela segue descendo até a água
    // do fundo (o caminho de quem desce; o buraco das correntes, redondo, é outro). Dentro, os degraus que somem no
    // escuro.
    const dx0 = ox + DESCIDA.x0, dx1 = ox + DESCIDA.x1;
    for (let y = PISO + 2; y < QH - 1; y++) {
      const recuo = Math.round((QH - 1 - y) * 0.35);
      px(dx0 + recuo, y, dx1 - dx0 - recuo * 2, 1, "#050607");
    }
    px(dx0 + 4, PISO + 1, dx1 - dx0 - 8, 1, COR.pedraLuz);   // a borda de trás
    px(dx0 - 1, QH - 2, dx1 - dx0 + 2, 1, COR.pedraLuz);     // a borda da frente
    [[PISO + 4, 0.75], [PISO + 7, 0.5], [PISO + 10, 0.3], [PISO + 13, 0.15]].forEach(([y, luz], k2) => {
      const x = dx0 + 5 + k2 * 4, w = dx1 - dx0 - 12 - k2 * 2;
      if (y < QH - 2) { px(x, y, w, 1, misturar("#050607", COR.pedraLuz, luz)); px(x, y + 1, w, 1, misturar("#050607", COR.pedra, luz * 0.6)); }
    });
    // o buraco das correntes no chão: a borda de pedra e a água escura lá embaixo
    const bx = ox + BURACO.x;
    for (let y = -BURACO.ry; y <= BURACO.ry; y++) for (let x = -BURACO.rx; x <= BURACO.rx; x++) {
      const d = (x * x) / (BURACO.rx * BURACO.rx) + (y * y) / (BURACO.ry * BURACO.ry);
      if (d <= 1) px(bx + x, BURACO.y + y, 1, 1, d > 0.72 ? COR.pedra : COR.agua);
    }
    // o sarilho: os dois postes e a trave (o tambor, a corrente, a trava e a manivela se mexem: vêm por cima)
    const sx = ox + SAR.x, sy = SAR.y;
    [sx + 4, sx + 84].forEach((x) => { px(x, sy, 4, PISO - sy, COR.madeiraEsc); px(x + 1, sy, 1, PISO - sy, COR.madeiraLuz); });
    px(sx, sy - 3, 92, 4, COR.madeira); px(sx, sy - 3, 92, 1, COR.madeiraLuz); px(sx, sy, 92, 1, COR.madeiraEsc);
    // A luz é a da tocha: longe dela, a sala escurece em degraus pontilhados (a escada e os cantos ficam na penumbra).
    escurecer(px, W, ox + TOCHA.x, TOCHA.y, 58, 150, 0.62);
    return { canvas: k, ox };
  }
  /** Sombra pela distância de uma luz (x, y): nada até `perto`, a mais escura (`max`) a partir de `longe`. Em degraus
   *  de preto translúcido, com o pontilhado de Bayer entre um degrau e outro. */
  function escurecer(px, W, lx, ly, perto, longe, max) {
    for (let y = 0; y < QH; y++) for (let x = 0; x < W; x++) {
      const d = Math.hypot(x - lx, (y - ly) * 1.6), t = Math.min(1, Math.max(0, (d - perto) / (longe - perto)));
      if (!t) continue;
      const f = t * 5, n = Math.floor(f) + (pontilha(x, y, Math.floor((f % 1) * 16)) ? 1 : 0);
      if (n) px(x, y, 1, 1, `rgba(3,4,6,${(max * n / 5).toFixed(3)})`);
    }
  }

  /** O que se mexe: a tocha da parede, o tambor com a corrente, a trava, a manivela e as correntes até o buraco. */
  function desenharOssuario(c, W, b, est, quadro, destaque) {
    const px = pincel(c);
    c.drawImage(b.canvas, 0, 0);
    const ox = b.ox, quieto = reduzido();
    // a tocha na parede, entre os nichos e o sarilho: a luz quente em anéis, que treme e alcança os ossos e o mecanismo
    const tx = ox + TOCHA.x, ty = TOCHA.y, raio = 62 + (quieto ? 0 : (quadro % 3) - 1);
    for (let y = 0; y < QH; y++) for (let x = Math.max(0, tx - raio); x < Math.min(W, tx + raio); x++) {
      const d2 = ((x - tx) ** 2 + ((y - ty) * 1.6) ** 2) / (raio * raio);
      if (d2 < 1) px(x, y, 1, 1, d2 < 0.08 ? "rgba(255,190,110,0.2)" : d2 < 0.3 ? "rgba(255,170,90,0.12)" : d2 < 0.65 ? "rgba(255,160,80,0.07)" : "rgba(255,150,70,0.035)");
    }
    px(tx - 2, ty + 2, 5, 1, "#2a2018"); px(tx - 1, ty + 2, 3, 5, "#3a2a18");
    const chama = quieto ? 0 : quadro % 2;
    px(tx - 1, ty - 2 - chama, 3, 4 + chama, "#e0782f"); px(tx, ty - 1 - chama, 1, 3, "#ffd27a");
    // o tambor: um eixo grosso de madeira preta; com a corrente enrolada (presas) ou nu (soltas)
    const sx = ox + SAR.x, sy = SAR.y, aceso = destaque === "sarilho";
    const t = est.correntes === "soltas" ? 1 : est.soltando ? Math.min(1, est.passo / 26) : 0;
    const giro = est.soltando ? est.passo : 0;
    px(sx + 9, sy + 7, 72, 16, COR.madeira); px(sx + 9, sy + 7, 72, 2, aceso ? COR.ouro : COR.madeiraLuz); px(sx + 9, sy + 22, 72, 1, COR.madeiraEsc);
    px(sx + 8, sy + 5, 3, 20, COR.madeiraEsc); px(sx + 79, sy + 5, 3, 20, COR.madeiraEsc);
    const voltas = Math.round(66 * (1 - t));
    for (let i = 0; i < voltas; i++) {
      const x = sx + 12 + i, y = sy + 9 + ((i * 2 + giro) % 12);
      px(x, y, 1, 2, (i + giro) % 2 ? COR.ferroLuz : COR.ferro);
    }
    // a roda dentada e a trava de ferro: a lingueta caída entre os dentes (presa) ou erguida
    const rx = sx + 1, ry = sy + 15;
    for (let k = 0; k < 12; k++) { const a = k * Math.PI / 6 + giro * 0.45; px(Math.round(rx + Math.cos(a) * 5), Math.round(ry + Math.sin(a) * 5), 2, 2, COR.ferroLuz); }
    px(rx - 1, ry - 1, 3, 3, COR.ferro);
    const erguida = est.correntes === "soltas" || est.soltando;
    px(rx - 12, ry - (erguida ? 12 : 6), 10, 2, aceso ? COR.ouro : COR.ferroLuz); px(rx - 12, ry - (erguida ? 10 : 4), 2, 5, COR.ferro);
    // a manivela, do outro lado: parada, ou girando enquanto a corrente desce
    const ang = est.soltando ? giro * 0.9 : est.correntes === "soltas" ? 2.3 : -0.7, mx = sx + 90, my = sy + 15;
    const hx = Math.round(mx + Math.cos(ang) * 8), hy = Math.round(my + Math.sin(ang) * 7);
    for (let k = 0; k <= 8; k++) px(Math.round(mx + (hx - mx) * k / 8), Math.round(my + (hy - my) * k / 8), 2, 2, COR.ferroLuz);
    px(hx - 1, hy - 2, 3, 4, aceso ? COR.ouro : COR.madeiraLuz); px(mx - 1, my - 1, 3, 3, COR.ferro);
    // as duas correntes, esticadas do tambor até o buraco; descendo, os elos correm para dentro; soltas, sumiram
    if (t < 1) {
      const corre = est.soltando ? giro % 3 : 0;
      [[sx + 30, ox + BURACO.x - 7], [sx + 60, ox + BURACO.x + 7]].forEach(([de, ate]) => {
        const y0 = sy + 23, y1 = BURACO.y, inicio = y0 + Math.round((y1 - y0) * t);
        for (let y = inicio; y < y1; y++) {
          const x = Math.round(de + (ate - de) * (y - y0) / (y1 - y0)), elo = (y + corre) % 3;
          if (elo === 0) px(x - 1, y, 4, 1, aceso ? "#e8d898" : COR.ferroLuz);
          else px(elo === 1 ? x - 1 : x + 2, y, 1, 1, aceso ? "#c8b880" : COR.ferro);
        }
      });
    }
    // a água do buraco: quieta, um brilho de vez em quando; e as rodas que se abrem quando a corrente termina de descer
    const bx = ox + BURACO.x;
    if (!quieto && quadro % 23 < 2) px(bx - 4 + (quadro % 9), BURACO.y, 2, 1, COR.aguaLuz);
    if (est.onda > 0) {
      const r = 12 - est.onda;
      for (let a = 0; a < 20; a++) {
        const x = Math.round(bx + Math.cos(a / 20 * Math.PI * 2) * Math.min(BURACO.rx - 3, r * 1.6)), y = Math.round(BURACO.y + Math.sin(a / 20 * Math.PI * 2) * Math.min(BURACO.ry - 1, r * 0.35));
        px(x, y, 1, 1, "#3a5a60");
      }
    }
  }

  // ================================================================ a capela vista de fora
  // A composição do protótipo da capela (artifact de 13/10): a outra margem com árvores mortas, a névoa rasteira, a
  // capela afundada com o reflexo, o canal do moinho reto até o buraco no muro, a beira de cá com os sapos. Ajustada à
  // descrição do jogo: a porta da frente sob a lama, a torre sem sino, juncos no antigo pátio. A entrada é o buraco.
  const AGUA = 52;
  const BRECHA = { x0: 156, x1: 166 };
  const TORRE = { x: 116, sino: [119, 18, 6, 8] };
  const SAPOS = [[50, false], [69, true], [91, false], [108, true]];  // x, patas a mais

  function baseExterior(W) {
    const k = camada(W), c = k.getContext("2d"), px = pincel(c), ox = Math.round((W - QW) / 2), r = rng(7);
    const ceu = ceuAgora(), bandas = ceu.bandas, p = ceu.periodo, hz = bandas[bandas.length - 1], noite = p === 3;
    // à noite, o luar: as formas saem do horizonte azulado, um pouco mais claras, para a capela não sumir
    const base0 = noite ? misturar(hz, "#6a7a9a", 0.35) : hz, escuro = (t) => misturar(base0, "#050404", noite ? t * 0.85 : t);
    const longe = escuro(0.45), meio = escuro(0.65), perto = escuro(0.82), chao = escuro(0.9);
    const sol = ceu.astro, ladoLuz = noite || !sol ? 0 : sol[0] > 160 ? 1 : -1;
    const face = ladoLuz ? misturar(meio, sol[3], 0.22) : meio, sombra = misturar(meio, perto, 0.55);
    const telha = misturar(meio, "#5a1a10", 0.35), telhaEsc = misturar(telha, perto, 0.4);
    const agua = misturar(hz, "#0a1a18", 0.6), brilho = misturar(hz, "#5a7a78", 0.4);
    const frio = misturar("#7aa4c4", meio, noite ? 0.35 : 0.5), negro = "#07080a";
    const lama = misturar(chao, "#4a3a24", 0.35), bruma = misturar(longe, hz, 0.5);
    const margemCima = (x) => lerp(61, AGUA, Math.max(0, (x - ox) / 156));  // o dique do canal, do lado do brejo
    const margemBaixo = (x) => lerp(67, AGUA, Math.max(0, (x - ox) / 165)); // o outro dique, onde os sapos esperam
    // o céu e o astro
    for (let y = 0; y < QH; y++) for (let x = 0; x < W; x++) px(x, y, 1, 1, corDoCeu(bandas, x, y));
    if (sol) {
      const [sx0, sy, raio, cor, baixo] = sol, sx = ox + sx0, halo = misturar(bandas[bandas.length - 2], cor, 0.45);
      for (let y = sy - raio - 6; y <= sy + raio + 6; y++) for (let x = sx - raio - 6; x <= sx + raio + 6; x++) {
        const d = Math.hypot(x - sx, y - sy);
        if (d <= raio) px(x, y, 1, 1, y > sy + raio / 3 && pontilha(x, y, 8) ? baixo : cor);
        else if (!noite && d < raio + 5 && pontilha(x, y, Math.round(9 - (d - raio) * 1.6))) px(x, y, 1, 1, halo);
      }
      if (noite) for (let y = -raio; y <= raio; y++) for (let x = -raio; x <= raio; x++) {
        if ((x - 3) * (x - 3) + (y + 1) * (y + 1) <= raio * raio * 0.8) px(sx + x, sy + y, 1, 1, bandas[0]);
      }
    }
    // a outra margem, árvores mortas longe, a névoa rasteira e a água do brejo
    let y = 45, v = 0;
    for (let x = 0; x < W; x++) { v += (r() - 0.5) * 0.5; v = Math.max(-1.5, Math.min(1.5, v * 0.92)); y = Math.max(42, Math.min(46, y + v)); px(x, Math.round(y), 1, QH - Math.round(y), longe); }
    [[12, 10], [44, 8], [78, 11], [236, 9], [274, 12], [306, 8], [-14, 9], [340, 10]].forEach(([x, hh], i) => arvoreSeca(px, ox + x, 47, hh, misturar(longe, meio, 0.5), i % 2 ? 1 : -1));
    for (let yy = 44; yy < 52; yy++) for (let x = 0; x < W; x++) {
      const n = Math.round(3 * (1 - Math.abs(yy - 48) / 4) + Math.sin(x / 11) * 1.5);
      if (n > 0 && pontilha(x, yy, n)) px(x, yy, 1, 1, bruma);
    }
    px(0, AGUA, W, QH - AGUA, agua);
    // ---- a capela, numa camada à parte (para o reflexo)
    const Lk = camada(W), L = Lk.getContext("2d"), lp = pincel(L);
    const tx = ox + TORRE.x;
    lp(tx, 14, 12, AGUA - 14, meio);
    lp(ladoLuz < 0 ? tx + 9 : tx, 14, 3, AGUA - 14, sombra);
    const [bx, by, bw, bh] = TORRE.sino;
    L.clearRect(ox + bx, by, bw, bh);  // o campanário vazado: onde estava o sino, o céu
    lp(ox + bx, by, 1, 1, meio); lp(ox + bx + bw - 1, by, 1, 1, meio);
    lp(ox + bx, by + 2, bw, 1, perto);                                  // a trave, vazia
    lp(ox + bx + 3, by + 3, 1, 2, misturar(perto, "#8a7050", 0.35));    // um toco de corda
    lp(tx + 5, 30, 2, 4, negro);
    for (let i = 0; i < 4; i++) lp(tx - 1 + i, 13 - i * 2, 14 - i * 2, 2, i % 2 ? telhaEsc : telha);
    lp(tx + 4, 5, 2, 1, telha); lp(tx + 6, 4, 1, 1, telhaEsc);
    const nx0 = ox + 128, nx1 = ox + 198;
    lp(nx0, 36, nx1 - nx0, AGUA - 36, meio);
    for (let yy = 29; yy <= 35; yy++) { const recuo = Math.round((35 - yy) * 0.5); lp(nx0 - 1 + recuo, yy, nx1 - nx0 + 2 - recuo * 2, 1, yy % 2 ? telha : telhaEsc); }
    lp(nx0 - 1, 35, nx1 - nx0 + 2, 1, misturar(telha, negro, 0.45));
    [7, 6, 5, 3, 2].forEach((meia, kk) => L.clearRect(ox + 166 - meia + (kk % 2), 29 + kk, meia * 2, 1));  // o rombo do telhado
    [161, 164, 167, 170].forEach((x) => lp(ox + x, 29 + (x % 2), 1, 5 - (x % 2), perto));
    [130, 145, 160, 180, 194].forEach((x) => lp(ox + x, 38, 2, AGUA - 38, ladoLuz > 0 ? face : sombra));
    // as janelas: arcos altos cortados pela água na metade
    [135, 149, 170, 185].forEach((x0) => {
      const x = ox + x0;
      lp(x + 1, 41, 3, 1, negro); lp(x, 42, 5, AGUA - 42, negro); lp(x, AGUA - 3, 5, 3, frio); lp(x, AGUA - 4, 5, 1, misturar(frio, negro, 0.5));
      lp(x + 2, 43, 1, AGUA - 43, sombra);
    });
    // o buraco no muro, rente à água, com as pedras caídas em volta: a entrada
    for (let x = BRECHA.x0; x < BRECHA.x1; x++) {
      const topo = Math.round(45 + Math.abs(x - 160.5) * 0.7 + ((x * 7) % 3) * 0.5);
      lp(ox + x, topo, 1, AGUA - topo, "#020303");
    }
    [[154, 50, 2], [167, 50, 2], [166, 49, 1], [153, 51, 1]].forEach(([x, yy, w]) => lp(ox + x, yy, w, 1, face));
    // a fachada de três quartos: a empena, o óculo e só o alto do arco da porta, quase todo sob a lama
    const fx = ox + 198, fw = 17, fc = fx + 8;
    lp(fx, 36, fw, AGUA - 36, ladoLuz > 0 ? face : sombra);
    for (let yy = 27; yy <= 35; yy++) { const meia = yy - 27; lp(fc - meia, yy, meia * 2 + 1, 1, ladoLuz > 0 ? face : sombra); lp(fc - meia - 1, yy, 1, 1, telha); lp(fc + meia + 1, yy, 1, 1, telha); }
    lp(fc, 26, 1, 1, telha);
    lp(fc - 1, 30, 3, 3, negro); lp(fc, 31, 1, 1, sombra);
    lp(fc - 2, 47, 5, 1, sombra); lp(fc - 3, 48, 1, 2, sombra); lp(fc + 3, 48, 1, 2, sombra); lp(fc - 2, 48, 5, 2, negro);
    for (let x = ox + 190; x < ox + 236; x++) {  // o monte de lama que engoliu a porta
      const topo = Math.round(49 + ((x - ox - 210) / 24) ** 2 * 4 + Math.sin(x / 2.2) * 0.5);
      if (topo < AGUA) lp(x, topo, 1, AGUA - topo, lama);
    }
    // o reflexo da capela na água, escuro e rareando
    const d = L.getImageData(0, 0, W, AGUA).data, corReflexo = misturar(agua, perto, 0.75);
    for (let yy = 0; yy < AGUA; yy++) for (let x = 0; x < W; x++) {
      if (!d[(yy * W + x) * 4 + 3]) continue;
      const kk = AGUA - yy, ry = AGUA + kk - 1;
      if (ry < QH && (kk < 10 || pontilha(x, ry, Math.round(16 - (kk - 10) * 1.2)))) px(x, ry, 1, 1, corReflexo);
    }
    for (let yy = AGUA + 1; yy < QH; yy += 2) for (let x = (yy * 7) % 13; x < W; x += 13 + (yy % 5)) px(x, yy, 3 + (x % 4), 1, brilho);
    c.drawImage(Lk, 0, 0);
    // o pátio da frente virou juncal
    juncos(px, r, ox + 186, ox + 262, AGUA, 9, perto, chao, 0.55);
    juncos(px, r, ox + 262, W, AGUA, 6, perto, chao, 0.3);
    juncos(px, r, ox + 100, ox + 128, AGUA, 6, perto, null, 0.35);
    px(ox + 186, AGUA + 1, W - ox - 186, 1, misturar(agua, perto, 0.4));
    px(nx0 - 12, AGUA, nx1 - nx0 + 120, 1, misturar(agua, brilho, 0.5));
    for (let x = BRECHA.x0; x < BRECHA.x1; x++) px(ox + x, AGUA, 1, 1, agua);
    // o canal do moleiro: reto, entre o dique (com estacas) e a beira de cá, apontando para o buraco
    const canal = misturar(agua, brilho, 0.35);
    for (let x = 0; x < ox + BRECHA.x1; x++) {
      const y0 = Math.round(margemCima(x)), y1 = Math.round(margemBaixo(x)), grosso = x - ox < 80 ? 2 : 1;
      if (y1 > y0) px(x, y0, 1, y1 - y0, canal);
      if (x < ox + 154) px(x, y0 - grosso, 1, grosso, perto);
      if (x < ox + 160) px(x, y1, 1, grosso, perto);
      if ((x - ox + 220) % 11 === 3 && x < ox + 150) { const hh = Math.round(lerp(5, 2, Math.max(0, (x - ox) / 150))); px(x, y0 - grosso - hh, 1, hh, perto); px(x + 5, y1 - hh + 1, 1, hh, perto); }
    }
    // a beira de cá: lama e juncos embaixo à esquerda; à direita, o terreno encharcado
    let yb = 69, vb = 0;
    for (let x = 0; x < ox + 120; x++) { vb += (r() - 0.5) * 0.5; vb = Math.max(-1.5, Math.min(1.5, vb * 0.92)); yb = Math.max(67, Math.min(70, yb + vb)); const yy = Math.round(yb) + Math.max(0, Math.round((x - ox - 70) / 12)); if (yy < QH) px(x, yy, 1, QH - yy, chao); }
    juncos(px, r, 0, ox + 90, 70, 6, misturar(chao, perto, 0.5), null, 0.45);
    arvoreSeca(px, ox + 22, 72, 30, perto, 1);
    arvoreSeca(px, ox + 296, 72, 22, perto, -1);
    px(ox + 236, 66, W - ox - 236, QH - 66, chao); for (let x = ox + 228; x < ox + 236; x++) px(x, 66 + (ox + 236 - x > 4 ? 2 : 1), 1, 6, chao);
    juncos(px, r, ox + 236, W, 67, 6, perto, chao, 0.5);
    return { canvas: k, ox, cor: { brilho, perto, meio, agua }, margemCima, margemBaixo, noite, bandas };
  }
  function arvoreSeca(px, x, y, hh, cor, lado = 1) {
    px(x, y - hh, 1, hh, cor);
    for (let i = 0; i < Math.floor(hh / 4); i++) {
      const yy = y - hh + 2 + i * 4, dir = (i + (lado > 0 ? 0 : 1)) % 2 ? 1 : -1, comp = Math.max(2, 5 - i + ((x + i) % 2));
      for (let k = 0; k < comp; k++) px(x + (dir > 0 ? 1 + k : -1 - k), yy - Math.floor(k / 2), 1, 1, cor);
    }
  }
  function juncos(px, r, x0, x1, base, alt, cor, espiga, dens) {
    for (let x = x0; x < x1; x++) {
      if (r() > dens) continue;
      const hh = Math.max(2, Math.round(alt * (0.45 + r() * 0.65)));
      px(x, base - hh, 1, hh, cor);
      if (espiga && r() < 0.25) px(x, base - hh - 1, 1, 2, espiga);
    }
  }

  function desenharExterior(c, W, b, est, quadro, destaque) {
    const px = pincel(c), ox = b.ox, quieto = reduzido(), q = quieto ? 0 : quadro;
    c.drawImage(b.canvas, 0, 0);
    // as nuvens andam devagar; à noite, as estrelas piscam
    const corNuvem = misturar(b.bandas[1], b.bandas[3], 0.35);
    [[30, 9, 70], [150, 6, 50], [250, 14, 90], [90, 22, 44]].forEach(([x0, y, w], i) => {
      const x = Math.floor(((x0 + q * (0.05 + i * 0.01)) % (W + 120)) - 60);
      px(x, y, w, 1, corNuvem); px(x + 6, y - 1, w - 18, 1, corNuvem);
    });
    if (b.noite) for (let i = 0; i < 24; i++) { const x = (i * 97 + 13) % W, y = (i * 53) % 30; if ((q + i * 3) % 23 > 2 && !(x > ox + 112 && x < ox + 218 && y > 3)) px(x, y, 1, 1, "#9aa4c0"); }
    // a água do brejo treme e a correnteza do canal anda até o buraco e some nele
    for (let k = 0; k < 10; k++) { const y = AGUA + 2 + ((k * 7) % 18), x = (k * 61 + Math.floor(q / 3) * 13) % W; if (y > b.margemCima(x) + 2 || x > ox + 170) px(x, y, 2, 1, b.cor.brilho); }
    for (let i = 0; i < 10; i++) {
      const t = (q * 0.01 + i / 10) % 1, x = Math.round(lerp(2, ox + 158, t));
      const y0 = b.margemCima(x), y1 = b.margemBaixo(x), y = Math.round(lerp(y0 + 1, y1 - 1, ((i * 3) % 5) / 4));
      if (y1 - y0 > 2) px(x, y, Math.max(1, Math.round(lerp(4, 1, t))), 1, misturar(b.cor.brilho, "#c8d8d8", 0.3));
    }
    // o buraco, aceso no mouse e no foco
    if (destaque === "buraco") for (let x = BRECHA.x0 - 1; x <= BRECHA.x1; x++) { const topo = Math.round(45 + Math.abs(x - 160.5) * 0.7 + ((x * 7) % 3) * 0.5); px(ox + x, topo - 1, 1, 1, COR.gelo); }
    // os sapos, quietos na beira; os olhos parados, de vez em quando um pisca. Os de patas a mais têm um par de pernas
    // sobrando, saindo de lado, mais claro (de perto, dá para contar).
    SAPOS.forEach(([sx0, mais], i) => {
      const sx = ox + sx0, sy = Math.round(b.margemBaixo(sx + 3)) - 3;
      const corpo = misturar("#4e6a34", b.cor.perto, b.noite ? 0.6 : 0.25), sombra = misturar(corpo, "#0a0c08", 0.45);
      const barriga = misturar(corpo, "#a8b070", 0.35), perna = misturar(corpo, "#b8c080", 0.3);
      const olho = "#d8c860", pisca = !quieto && (quadro + i * 23) % 61 < 2, aceso = destaque === "sapos";
      px(sx + 1, sy + 1, 5, 1, corpo); px(sx, sy + 2, 7, 1, corpo); px(sx + 2, sy + 2, 3, 1, barriga); px(sx, sy + 3, 7, 1, sombra);
      px(sx + 1, sy, 1, 1, corpo); px(sx + 5, sy, 1, 1, corpo);                       // os calombos dos olhos
      px(sx - 1, sy + 3, 2, 1, corpo); px(sx + 6, sy + 3, 2, 1, corpo);               // as patas de trás, dobradas
      px(sx + 1, sy + 4, 1, 1, sombra); px(sx + 5, sy + 4, 1, 1, sombra);             // as da frente
      if (mais) { px(sx - 2, sy + 1, 2, 1, perna); px(sx - 3, sy + 2, 1, 1, perna); px(sx + 7, sy + 1, 2, 1, perna); px(sx + 9, sy + 2, 1, 1, perna); }
      if (!pisca) { px(sx + 1, sy, 1, 1, aceso ? "#fff0a0" : olho); px(sx + 5, sy, 1, 1, aceso ? "#fff0a0" : olho); }
    });
  }

  // ================================================================ o salão alagado
  // A nave do protótipo, sem o sarilho (que é do ossuário): os vãos com as janelas altas e os fachos de luz, o buraco
  // do muro da esquerda por onde entra o canal, as colunas, os bancos podres na água, o presbitério com o altar e,
  // atrás dele, a porta baixa da sacristia, um degrau acima. A água corre do buraco à fenda do piso, perto do altar,
  // e desce por ela (um rasgo no chão, não um portal).
  const COLUNAS = [36, 100, 164];
  const FENDA = { x: 196, y: 58 };
  const AGUA_D = 52, PRESB = 43;
  const PORTA = { x: 288, y: 31 };

  function baseSalao(W) {
    const k = camada(W), c = k.getContext("2d"), px = pincel(c), ox = Math.round((W - QW) / 2);
    const ceu = ceuAgora(), bandas = ceu.bandas, noite = ceu.periodo === 3;
    const parede = "#15181d", vao = "#0b0d10", pedra = "#2a2f36", pedraLuz = "#3d444d", pedraSombra = "#1c2026", chumbo = "#0e1013";
    const luz = noite ? misturar(bandas[4], "#9aa8c8", 0.6) : misturar(bandas[4], "#e8e0d0", 0.3);
    const agua = "#0b1316", aguaFundo = "#06090b";
    px(0, 0, W, QH, parede);
    px(0, 4, W, 1, pedraSombra);
    // os vãos entre as colunas (a nave lateral), e em cada um uma janela alta com o céu da hora
    const vaos = [[-60, ox + COLUNAS[0]], [ox + COLUNAS[0] + 9, ox + COLUNAS[1]], [ox + COLUNAS[1] + 9, ox + COLUNAS[2]], [ox + COLUNAS[2] + 9, ox + 214]];
    const janelas = [];
    vaos.forEach(([a, b], i) => {
      const meio = (a + b) / 2, meia = (b - a) / 2;
      for (let x = Math.max(0, a); x < b; x++) {
        const t = Math.min(1, Math.abs(x + 0.5 - meio) / meia), topo = Math.round(5 + 9 * (1 - Math.sqrt(1 - t * t)));
        px(x, topo, 1, AGUA_D - topo, vao); px(x, topo - 1, 1, 1, pedraLuz);
      }
      if (i > 0) janelas.push([Math.round(meio) - 4, i === 3 ? 18 : 16, 9, i === 3 ? 16 : 20]);
    });
    // a abside, atrás do altar, com a janela grande
    px(ox + 214, 0, W - ox - 214, PRESB, parede);
    janelas.push([ox + 254, 8, 13, 24]);
    janelas.forEach(([jx, jy, jw, jh], kk) => {
      for (let y = jy; y < jy + jh; y++) for (let x = jx; x < jx + jw; x++) {
        const dx = x + 0.5 - (jx + jw / 2), curva = y - jy < jw / 2 && dx * dx + (y - jy - jw / 2) ** 2 * 1.3 > (jw / 2) ** 2;
        if (curva) continue;
        const quebrado = ((x * 13 + y * 7 + kk * 5) % 19) === 0, chumbado = x === jx + Math.floor(jw / 2) || (y - jy) % 7 === 6;
        px(x, y, 1, 1, quebrado || chumbado ? chumbo : corDoCeu(bandas, x, Math.round(((y - jy) / jh) * 50)));
      }
    });
    // os fachos de luz descendo das janelas, ralos, até a água (ambiente: dentro continua escuro, pede tocha)
    janelas.forEach(([jx, jy, jw, jh], kk) => {
      const ate = kk === janelas.length - 1 ? PRESB : AGUA_D + 3;
      for (let y = jy + jh; y < ate; y++) {
        const desv = Math.round((y - jy - jh) * 0.45);
        for (let x = jx + desv; x < jx + jw + desv + 2; x++) if (pontilha(x, y, 2)) px(x, y, 1, 1, misturar(luz, parede, noite ? 0.75 : 0.55));
      }
    });
    // o buraco no muro da esquerda: lá fora, o céu e o brejo; por ele entra a água do canal
    for (let y = 26; y < AGUA_D; y++) for (let x = 2; x < 30; x++) {
      const bb = (x - 15) ** 2 / 150 + (y - AGUA_D) ** 2 / 500 + ((x * 7 + y * 3) % 5) * 0.04;
      if (bb > 1) continue;
      px(ox + x, y, 1, 1, y >= 46 ? misturar(bandas[4], "#0a1a18", 0.65) : misturar(corDoCeu(bandas, ox + x, Math.round(20 + (y - 26) * 1.4)), "#000000", 0.35));
      if (bb > 0.84) px(ox + x, y, 1, 1, pedraLuz);
    }
    const fora = misturar(bandas[4], "#050404", 0.82), r = rng(11);
    for (let x = ox + 4; x < ox + 28; x++) { if (r() > 0.6) continue; const hh = Math.max(2, Math.round(7 * (0.45 + r() * 0.65))); px(x, 47 - hh, 1, hh, fora); }
    px(ox + 3, 46, 26, 1, fora);
    // as colunas, com capitel e base
    COLUNAS.forEach((x0) => {
      const x = ox + x0;
      px(x, 0, 9, AGUA_D, pedra); px(x, 0, 2, AGUA_D, pedraLuz); px(x + 7, 0, 2, AGUA_D, pedraSombra);
      px(x - 1, 13, 11, 2, pedraLuz); px(x - 1, 15, 11, 1, pedraSombra);
      px(x - 1, AGUA_D - 2, 11, 2, pedra); px(x - 1, AGUA_D - 2, 11, 1, pedraLuz);
    });
    // o presbitério: três degraus subindo da água até o chão do altar
    [[208, 50], [216, 47], [224, PRESB + 1]].forEach(([x, y]) => { px(ox + x, y, W - ox - x, AGUA_D - y, pedra); px(ox + x, y, W - ox - x, 1, pedraLuz); });
    px(ox + 224, PRESB, W - ox - 224, 1, pedraLuz);
    // o altar: a pedra, o pano podre, o castiçal caído, a cruz raspada da frente
    const ax = ox + 244;
    px(ax, 33, 28, PRESB - 33, pedra); px(ax - 2, 31, 32, 2, pedraLuz); px(ax - 2, 33, 32, 1, pedraSombra);
    px(ax + 4, 35, 20, 7, pedraSombra); px(ax + 13, 36, 2, 5, pedra); px(ax + 11, 37, 6, 1, pedra);
    px(ax + 2, 33, 6, 1, "#4a1c1a"); px(ax + 3, 34, 2, 5, "#4a1c1a"); px(ax + 6, 34, 1, 2, "#3a1614");
    px(ax + 20, 30, 6, 1, "#6a5a3a"); px(ax + 25, 29, 1, 1, "#8a7a4a");
    // a porta baixa da sacristia, atrás do altar, um degrau acima do chão: o arco, o escuro e a folha de tábuas aberta
    const dx = ox + PORTA.x, dy = PORTA.y, dw = 13, dh = PRESB - PORTA.y;
    px(dx - 2, dy - 2, dw + 4, dh + 2, pedraLuz); px(dx - 1, dy - 1, dw + 2, dh + 1, pedra);
    px(dx, dy, dw, dh, "#050607"); px(dx + 1, dy - 1, dw - 2, 1, "#050607");
    px(dx + dw - 4, dy + 1, 4, dh - 1, "#2c2118"); px(dx + dw - 4, dy + 1, 1, dh - 1, "#45352a"); px(dx + dw - 2, dy + 5, 1, 1, "#6a6a70");
    px(dx - 3, PRESB - 1, dw + 6, 1, pedraLuz); px(dx - 3, PRESB, dw + 6, 1, pedraSombra);  // o degrau
    // a água: escura, mais funda embaixo, com o reflexo das colunas e dos fachos
    for (let y = AGUA_D; y < QH; y++) for (let x = 0; x < W; x++) px(x, y, 1, 1, y > 63 || (y > 59 && pontilha(x, y, (y - 59) * 4)) ? aguaFundo : agua);
    px(0, AGUA_D, W, 1, "#1a2629");
    COLUNAS.forEach((x0) => { for (let kk = 1; kk < 18; kk++) if (kk < 8 || kk % 2) px(ox + x0 + (kk > 8 ? (kk % 4) - 1 : 0), AGUA_D + kk, 9, 1, misturar(pedraSombra, agua, kk / 18)); });
    janelas.slice(0, 3).forEach(([jx, jy, jw, jh]) => {
      const x0 = jx + Math.round((AGUA_D - jy - jh) * 0.45);
      for (let y = AGUA_D + 1; y < QH - 4; y += 2) px(x0 + ((y * 3) % 5) - 2, y, Math.max(2, jw - (y - AGUA_D) / 2), 1, misturar(luz, agua, 0.55 + (y - AGUA_D) / 50));
    });
    for (let y = AGUA_D + 1; y < 60; y += 2) px(ox + 4 + ((y * 5) % 6), y, 20 - (y - AGUA_D), 1, misturar(bandas[4], agua, 0.6));  // o reflexo do buraco
    // a fenda do piso, perto do altar: um rasgo escuro no fundo raso, onde a água desce
    const fx = ox + FENDA.x, fy = FENDA.y;
    px(fx - 5, fy, 11, 1, "#020304"); px(fx - 3, fy - 1, 7, 1, "#020304"); px(fx - 2, fy + 1, 5, 1, "#03050a");
    // Os bancos. A água que se mexe (as rodas, o caminho dela) é desenhada depois, por cima da sala: para ela passar
    // atrás da madeira, os bancos vão também numa camada própria, só o que está acima da linha d'água deles, que
    // volta por cima da água a cada quadro. O que está submerso (o pé das pernas da frente) fica embaixo dela.
    desenharBancos(px, ox);
    const bancos = camada(W), cb = bancos.getContext("2d");
    cb.save(); cb.beginPath(); cb.rect(0, 0, W, LINHA_BANCOS); cb.clip();
    desenharBancos(pincel(cb), ox);
    cb.restore();
    return { canvas: k, ox, bancos, cor: { agua, luz } };
  }

  // A linha d'água dos bancos da frente: deles para cima, madeira à vista; para baixo, a perna dentro da água.
  const LINHA_BANCOS = 60;
  /** Os bancos: uma fileira lá atrás, entre as colunas, e a da frente, maior, podre e torta. */
  function desenharBancos(px, ox) {
    const madeira = "#2c2118", madeiraLuz = "#45352a", madeiraEsc = "#1a130e";
    [[50, 14], [70, 22], [112, 16], [134, 22], [176, 14]].forEach(([x0, w], i) => {
      const x = ox + x0;
      px(x, 48, 1, 4, madeiraEsc); px(x + w - 1, 49, 1, 3, madeiraEsc);
      px(x, 48 + (i === 1 ? 1 : 0), w, 1, madeiraLuz); px(x, 50, w, 2, madeira);
    });
    [[14, 34, 0], [62, 42, 1], [124, 30, 0]].forEach(([x0, w, quebrado]) => {
      const x = ox + x0;
      for (let kk = 0; kk < w; kk++) {
        if (quebrado && kk > 16 && kk < 23) continue;
        const caido = quebrado && kk >= 23 ? Math.floor((kk - 23) / 6) : 0;
        px(x + kk, 56 + caido, 1, 1, madeiraLuz); px(x + kk, 57 + caido, 1, 2, madeira);
      }
      [x, x + w - 2].forEach((bx) => { px(bx, 53, 2, 9, madeiraEsc); px(bx, 53, 2, 1, madeiraLuz); });
      px(x, 52, w - (quebrado ? 26 : 0), 1, madeiraEsc);
    });
  }

  function desenharSalao(c, W, b, est, quadro, destaque) {
    const px = pincel(c), ox = b.ox, quieto = reduzido(), q = quieto ? 0 : quadro, inquieta = est.agua === "inquieta";
    c.drawImage(b.canvas, 0, 0);
    const fx = ox + FENDA.x, fy = FENDA.y;
    if (!inquieta) {
      // quieta: o caminho da água fica à vista, do buraco do muro à fenda: clara na entrada, escura de lodo no fim
      const caminho = [[ox + 16, 54], [ox + 48, 55], [ox + 96, 54], [ox + 140, 55], [ox + 178, 57], [fx - 4, fy]];
      for (let i = 0; i < 14; i++) {
        const u = (q * 0.006 + i / 14) % 1, seg = u * (caminho.length - 1), k = Math.floor(seg), f = seg - k;
        const [x0, y0] = caminho[k], [x1, y1] = caminho[k + 1];
        px(Math.round(lerp(x0, x1, f)) - 1, Math.round(lerp(y0, y1, f)) + ((i % 3) - 1) * 2, 3, 1, misturar("#3a5a5c", "#1a1810", u));
      }
      c.drawImage(b.bancos, 0, 0);
    } else {
      // inquieta: a água se mexe em rodas por todo lado (atrás da madeira); as sanguessugas, grudadas nela
      for (let i = 0; i < 9; i++) {
        const cx = ox + 20 + ((i * 37 + Math.floor(q / 4) * 11) % 180), cy = 54 + (i * 5) % 12, rr = 2 + ((q + i * 3) % 6);
        for (let a = 0; a < 10; a++) px(Math.round(cx + Math.cos(a / 10 * Math.PI * 2) * rr), Math.round(cy + Math.sin(a / 10 * Math.PI * 2) * rr * 0.3), 1, 1, "#1f3438");
      }
      c.drawImage(b.bancos, 0, 0);
      // Cada uma presa num ponto (o encosto do banco da frente, a perna de um banco de trás na linha d'água, a base de
      // uma coluna): o corpo se estica e encolhe devagar, sem sair do lugar; com movimento reduzido, parada.
      SANGUESSUGAS.forEach(([sx, sy, lado], i) => {
        const fase = quieto ? 0 : Math.floor(quadro / 7 + i * 3) % 4, estica = fase === 1 || fase === 2 ? 1 : 0;
        const n = 5 + estica;
        for (let k = 0; k < n; k++) px(ox + sx + lado * k, sy, 1, k === 0 || k === n - 1 ? 1 : 2, k === n - 1 ? "#7a4248" : k % 2 ? "#3a1c22" : "#4e2830");
        px(ox + sx + lado * (n - 1), sy - 1, 1, 1, "#5a3036");  // a ventosa erguida, procurando
      });
    }
    // a fenda: a água gira em volta do rasgo e desce (mais devagar com a sala quieta)
    const velocidade = inquieta ? 0.22 : 0.12;
    for (let anel = 0; anel < 3; anel++) for (let i = 0; i < 6; i++) {
      const a = q * velocidade * (1.6 - anel * 0.4) + i * (Math.PI / 3) + anel, raio = 6 + anel * 4;
      px(Math.round(fx + Math.cos(a) * raio), Math.round(fy + Math.sin(a) * raio * 0.28), 2, 1, anel === 0 ? "#2c4a50" : "#1f3438");
    }
    // a porta da sacristia, acesa no mouse e no foco
    if (destaque === "porta") {
      const dx = ox + PORTA.x, dy = PORTA.y, dw = 13;
      px(dx - 2, dy - 2, dw + 4, 1, COR.ouro); px(dx - 2, dy - 2, 1, PRESB - dy + 2, COR.ouro); px(dx + dw + 1, dy - 2, 1, PRESB - dy + 2, COR.ouro);
    }
  }

  // ================================================================ a sacristia
  // Uma sala pequena e seca, um degrau acima da água do salão: a porta para ele à esquerda (lá dentro, a água mais
  // embaixo), as prateleiras reviradas (a de baixo partida), o livro escondido num buraco da parede, a janela alta com a
  // escada de mão (de madeira, não a de pedra do ossuário), o alçapão no chão e, no canto, o baú pequeno de ferro. O
  // motor diz o momento: a entrada (os dois de capa escura, a lanterna erguida), a luta (eles são as cartas: a lanterna
  // no chão), a vitória e a visita (a lanterna continua no chão, acesa, no mesmo lugar); e o baú (no canto até ser
  // recolhido). A luz: a lanterna e a janela (o período lá fora).
  const SAC = {
    piso: 54,
    porta: { x: 8, w: 26, topo: 18 },          // o vão da porta do salão, em arco
    janela: { x: 197, y: 4, w: 10, h: 17 },     // a janela alta
    buraco: { x: 122, y: 24, w: 13, h: 10 },    // onde estava o livro
    alcapao: { x: 230, y: 58, meia: 16, alt: 9 }, // o centro de cima, a meia largura em cima, a altura
    bau: { x: 274, w: 18, y: 40 },               // o baú no canto: x, largura, o alto da tampa
  };
  const CORS = {
    parede: "#1f1d1c", junta: "#161413", pedra: "#2d2926", pedraLuz: "#47413b", pedraSombra: "#171513",
    chao: "#29251f", chaoLuz: "#3d362d", chaoJunta: "#1c1915", madeira: "#3a2a1c", madeiraLuz: "#5a4430",
    madeiraEsc: "#1c140d", escada: "#6a5236", escadaLuz: "#8a6e48", ferro: "#3a3c42", ferroLuz: "#6a6c74",
    papel: "#b8ae98", couro: "#4a3020", couroEsc: "#2a1a10",
    capa: "#141419", capaBorda: "#2a2a34", escuro: "#06080a",
  };
  /** Onde a luz principal está: a lanterna erguida (entrada) e, da luta em diante, a lanterna no chão, onde o vulto a
   *  largou (a vitória e a visita também: ela ficou ali, acesa). A janela soma a luz do período lá fora (na base). */
  function luzSacristia(d) {
    if (d.momento === "entrada") return { x: 160, y: 31, perto: 40, longe: 150, max: 0.6, quente: true };
    return { x: 150, y: 57, perto: 38, longe: 150, max: 0.6, quente: true };  // largada no chão na luta, e ali ficou
  }


  function baseSacristia(W, d) {
    const k = camada(W), c = k.getContext("2d"), px = pincel(c), ox = Math.round((W - QW) / 2), C = CORS, P = SAC.piso;
    const ceu = ceuAgora(), bandas = ceu.bandas, noite = ceu.periodo === 3;
    d = d || { momento: "visita", bau: "levado", livro: "no_buraco" };
    // a parede em blocos, o teto baixo com duas vigas e o chão seco de lajes
    px(0, 0, W, QH, C.parede);
    for (let y = 6; y < P; y += 6) for (let x = ((y / 6) % 2) * 7 - 14; x < W; x += 14) { px(x, y, 14, 1, C.junta); px(x, y, 1, 6, C.junta); }
    px(0, 0, W, 4, C.madeiraEsc); px(0, 4, W, 1, C.pedraSombra);
    for (let y = P; y < QH; y++) px(0, y, W, 1, y === P ? C.chaoLuz : C.chao);
    for (let y = P + 4; y < QH; y += 5) for (let x = (y * 3) % 12; x < W; x += 16) px(x, y, 12, 1, C.chaoJunta);
    for (let x = 0; x < W; x += 17) px(x + ((x * 7) % 5), P + 1, 1, 3, C.chaoJunta);
    // a porta do salão, à esquerda: o arco de pedra, o escuro, e lá dentro a água do salão, mais embaixo (um degrau)
    const pt = SAC.porta, px0 = ox + pt.x, pmeio = px0 + pt.w / 2;
    for (let x = px0; x < px0 + pt.w; x++) {
      const t = Math.min(1, Math.abs(x + 0.5 - pmeio) / (pt.w / 2)), topo = Math.round(pt.topo + 7 * (1 - Math.sqrt(1 - t * t)));
      px(x, topo, 1, P - topo, C.escuro); px(x, topo - 1, 1, 1, C.pedraLuz); px(x, topo - 2, 1, 1, C.pedra);
    }
    px(px0 + 17, 26, 3, 21, "#0f1215"); px(px0 + 17, 26, 1, 21, "#191d22");          // uma coluna do salão, lá no fundo
    for (let y = 47; y < P - 2; y++) px(px0 + 1, y, pt.w - 2, 1, y === 47 ? "#1a2629" : "#0b1316");  // a água do salão
    px(px0 + 4, 49, 4, 1, "#1f3034"); px(px0 + 14, 50, 3, 1, "#1f3034");
    px(px0 + 1, P - 2, pt.w - 2, 2, C.pedraSombra); px(px0 + 1, P - 2, pt.w - 2, 1, C.pedra);  // o degrau, descendo
    px(px0 - 2, P, pt.w + 4, 1, C.pedraLuz); px(px0 - 1, P + 1, pt.w + 2, 1, C.pedra);          // a soleira
    px(ox + 2, 22, 5, P - 22, C.madeira); px(ox + 2, 22, 1, P - 22, C.madeiraLuz); px(ox + 6, 22, 1, P - 22, C.madeiraEsc);  // a folha, aberta
    px(ox + 3, 30, 3, 1, C.ferro); px(ox + 3, 46, 3, 1, C.ferro);
    // as prateleiras, reviradas: a de baixo partida, um pote caído, uma caixa aberta, papéis no chão
    [ox + 44, ox + 106].forEach((x) => { px(x, 16, 3, P - 16, C.madeiraEsc); px(x, 16, 1, P - 16, C.madeira); });
    [24, 34].forEach((y) => {
      px(ox + 44, y, 65, 1, C.madeiraLuz); px(ox + 44, y + 1, 65, 1, C.madeira); px(ox + 47, y + 2, 59, 1, C.pedraSombra);  // a sombra embaixo
      [ox + 47, ox + 103].forEach((x) => px(x, y + 2, 2, 1, C.ferro));  // os suportes de ferro, junto dos montantes
    });
    // a de baixo partiu no meio: a metade da esquerda ficou no suporte, com a ponta lascada; a da direita escorregou
    // do suporte de lá e ficou inclinada, com uma ponta no chão e a outra apoiada no montante
    px(ox + 44, 44, 34, 1, C.madeiraLuz); px(ox + 44, 45, 33, 1, C.madeira); px(ox + 47, 46, 28, 1, C.pedraSombra);
    px(ox + 78, 44, 1, 1, C.madeiraLuz); px(ox + 77, 45, 1, 1, C.madeiraLuz); px(ox + 79, 43, 1, 1, C.madeira);  // as lascas
    px(ox + 47, 46, 2, 1, C.ferro);
    for (let x = ox + 80; x <= ox + 105; x++) {
      const y = Math.round(lerp(P - 2, 44, (x - ox - 80) / 25));
      px(x, y, 1, 1, C.madeiraLuz); px(x, y + 1, 1, 1, C.madeira); px(x + 1, y + 2, 1, 1, C.pedraSombra);  // e a sombra dela
    }
    px(ox + 80, P - 2, 1, 2, C.madeiraEsc); px(ox + 81, P - 1, 1, 1, C.madeiraLuz);  // a ponta quebrada, no chão
    px(ox + 103, 46, 2, 1, C.ferro);                                                     // o suporte vazio
    px(ox + 52, 19, 4, 5, "#4a4038"); px(ox + 52, 19, 4, 1, "#6a5e50"); px(ox + 53, 18, 2, 1, "#3a3028");    // um pote de pé
    px(ox + 64, 22, 7, 2, "#4a4038"); px(ox + 70, 22, 1, 2, "#2a221c");                                      // outro, deitado
    px(ox + 82, 30, 7, 4, C.madeira); px(ox + 82, 29, 7, 1, C.madeiraLuz); px(ox + 88, 27, 1, 3, C.madeiraLuz); // a caixa, aberta
    px(ox + 84, 29, 2, 1, C.papel);
    px(ox + 92, P + 3, 6, 1, "#6a5a3a"); px(ox + 97, P + 2, 1, 1, "#8a7a4a");                               // o castiçal caído
    [[60, 61, 4], [78, 66, 5], [90, 58, 3]].forEach(([x, y, w]) => { px(ox + x, y, w, 1, C.papel); px(ox + x, y + 1, w, 1, "#8a8270"); });
    px(ox + 100, 60, 2, 1, "#4a4038"); px(ox + 103, 61, 1, 1, "#4a4038");                                    // os cacos
    // o buraco na parede onde o livro estava escondido: pedras arrancadas em volta; o livro lá dentro, no couro (antes
    // da vitória) ou desembrulhado, com o couro aberto caindo pela borda
    const bk = SAC.buraco, bx = ox + bk.x;
    // o contorno roído: cada linha começa e termina num ponto diferente (pedras arrancadas, não um nicho feito)
    const recorte = [3, 1, 0, 0, 1, 0, 0, 2, 1, 3], fim = [2, 0, 1, 0, 0, 0, 1, 0, 2, 4];
    for (let i = 0; i < bk.h; i++) {
      const y = bk.y + i, a = bx + recorte[i], b2 = bx + bk.w - fim[i];
      px(a, y, b2 - a, 1, C.escuro);
      px(a - 1, y, 1, 1, i < 3 ? C.pedraLuz : C.pedra); px(b2, y, 1, 1, C.pedraSombra);
    }
    px(bx + 2, bk.y - 1, bk.w - 3, 1, C.pedraLuz); px(bx + 3, bk.y + bk.h, bk.w - 6, 1, C.pedraLuz);
    px(bx + bk.w - 3, bk.y + 2, 2, 2, C.pedra);  // uma pedra meio solta na borda
    px(bx + 2, P + 2, 3, 2, C.pedra); px(bx + 9, P + 3, 2, 1, C.pedra);  // as pedras que caíram
    if (d.livro === "embrulhado") {
      px(bx + 2, bk.y + 4, 9, 5, C.couro); px(bx + 2, bk.y + 4, 9, 1, "#6a4a30"); px(bx + 6, bk.y + 4, 1, 5, C.couroEsc);
    } else {  // desembrulhado: o livro deitado, a lombada e o corte das folhas à vista; o couro pendendo da borda
      px(bx + 3, bk.y + 5, 8, 3, "#5a3422"); px(bx + 3, bk.y + 5, 8, 1, "#7a4c30");  // a capa
      px(bx + 3, bk.y + 8, 8, 1, C.papel); px(bx + 10, bk.y + 6, 1, 2, "#8a8270");   // as folhas
      px(bx + 1, bk.y + bk.h, 7, 1, C.couro); px(bx + 2, bk.y + bk.h + 1, 5, 2, C.couro);
      px(bx + 3, bk.y + bk.h + 3, 3, 1, C.couroEsc); px(bx + 1, bk.y + bk.h, 7, 1, "#6a4a30");
    }
    // a janela alta, estreita, com o céu da hora e uma barra de ferro; o peitoril de pedra
    const jn = SAC.janela, jx = ox + jn.x;
    for (let y = jn.y; y < jn.y + jn.h; y++) for (let x = jx; x < jx + jn.w; x++) {
      const dx = x + 0.5 - (jx + jn.w / 2);
      if (y - jn.y < jn.w / 2 && dx * dx + (y - jn.y - jn.w / 2) ** 2 > (jn.w / 2) ** 2) continue;
      px(x, y, 1, 1, x === jx + 5 ? "#2a2c30" : corDoCeu(bandas, x, Math.round(((y - jn.y) / jn.h) * 50)));
    }
    px(jx - 2, jn.y + jn.h, jn.w + 4, 2, C.pedraLuz); px(jx - 2, jn.y + jn.h + 2, jn.w + 4, 1, C.pedraSombra);
    // a escada de mão, de madeira, encostada embaixo da janela: dois montantes e os degraus (não é a de pedra do ossuário)
    for (let y = 21; y < P + 4; y++) {
      const t = (y - 21) / (P + 3 - 21), xe = Math.round(lerp(ox + 196, ox + 186, t)), xd = Math.round(lerp(ox + 203, ox + 194, t));
      px(xe, y, 1, 1, C.escada); px(xd, y, 1, 1, C.escada);
      if ((y - 23) % 5 === 0) px(xe + 1, y, xd - xe - 1, 1, C.escadaLuz);
    }
    // o alçapão no chão, para o ossuário: as tábuas num trapézio (a perspectiva do chão), a moldura de pedra, a argola
    const al = SAC.alcapao, ax = ox + al.x;
    for (let i = 0; i < al.alt; i++) {
      const meia = al.meia + Math.round(i * 0.4), y = al.y + i;
      px(ax - meia - 1, y, meia * 2 + 2, 1, C.pedraLuz);
      for (let x = ax - meia; x < ax + meia; x++) px(x, y, 1, 1, (x - ax + 60) % 6 === 0 ? C.madeiraEsc : i === 0 ? C.madeiraLuz : C.madeira);
    }
    px(ax - al.meia - 1, al.y - 1, al.meia * 2 + 2, 1, C.pedraSombra);
    px(ax - 2, al.y + 3, 5, 1, C.ferroLuz); px(ax - 3, al.y + 4, 1, 2, C.ferroLuz); px(ax + 3, al.y + 4, 1, 2, C.ferroLuz); px(ax - 2, al.y + 6, 5, 1, C.ferro);
    [ax - 11, ax + 8].forEach((x) => px(x, al.y, 4, 1, C.ferro));  // as dobradiças
    // o baú: pequeno, de ferro velho, no canto, até ser recolhido; depois, só a marca dele na poeira
    const bu = ox + SAC.bau.x, bw = SAC.bau.w, bt = SAC.bau.y;
    if (d.bau === "no_canto") desenharBau(px, bu, bw, bt, P);
    else { px(bu + 1, P + 1, bw - 2, 1, C.chaoLuz); px(bu, P + 2, 1, 2, C.chaoLuz); px(bu + bw - 1, P + 2, 1, 2, C.chaoLuz); px(bu + 1, P + 4, bw - 2, 1, C.chaoLuz); }
    // a parede da direita, no canto
    px(W - 8, 0, 8, P, C.pedraSombra); px(W - 8, 0, 1, P, C.pedra);
    // a luz: longe da fonte, a sala escurece em degraus pontilhados; as passagens e a janela continuam legíveis
    const L = luzSacristia(d);
    escurecer(px, W, ox + L.x, L.y, L.perto, L.longe, L.max);
    const leitura = "rgba(150,140,120,0.35)";
    for (let x = px0; x < px0 + pt.w; x++) { const t = Math.min(1, Math.abs(x + 0.5 - pmeio) / (pt.w / 2)); px(x, Math.round(pt.topo + 7 * (1 - Math.sqrt(1 - t * t))) - 1, 1, 1, leitura); }
    px(ax - al.meia - 1, al.y, al.meia * 2 + 2, 1, leitura);
    px(jx - 2, jn.y + jn.h, jn.w + 4, 1, leitura);
    if (d.bau === "no_canto") { px(bu + 3, bt, bw - 6, 1, leitura); px(bu, bt + 5, 1, P + 3 - bt - 5, leitura); }  // o baú, legível no canto
    // a luz que entra pela janela: fria, fraca, no peitoril e numa mancha no chão; à noite, quase nada
    const daJanela = noite ? "rgba(150,165,200," : "rgba(225,215,190,";
    px(jx - 2, jn.y + jn.h, jn.w + 4, 1, daJanela + (noite ? "0.25)" : "0.45)"));
    for (let y = P + 1; y < P + 8; y++) {
      const x0 = jx - 10 - (y - P) * 2, x1 = jx + jn.w - (y - P), f = 1 - (y - P) / 8;
      px(x0, y, x1 - x0, 1, daJanela + ((noite ? 0.035 : 0.09) * f).toFixed(3) + ")");
    }
    return { canvas: k, ox, d, luz: L };
  }

  /** O baú de ferro: a tampa abaulada, as cintas com rebites nas pontas, o espelho da fechadura no meio, a ferrugem
   *  nas bordas e a sombra no chão. Fica pousado com a base um pouco à frente da parede (y do chão + 3). */
  function desenharBau(px, x, w, topo, P) {
    const C = CORS, base = P + 3, tampa = topo + 6, ferro = "#45474e", ferroLuz = "#6e7078", ferroEsc = "#2a2b30";
    px(x + 1, base, w, 1, "#120f0c"); px(x + w, base - 3, 1, 3, "#120f0c");                  // a sombra
    for (let y = topo; y < tampa; y++) {                                                      // a tampa, abaulada
      const recuo = [4, 2, 1, 0, 0, 0][y - topo];
      px(x + recuo, y, w - recuo * 2, 1, y - topo < 2 ? ferroLuz : ferro);
    }
    px(x, tampa, w, 1, "#1c1d21");                                                            // a junta da tampa
    px(x, tampa + 1, w, base - tampa - 1, "#38393f"); px(x, tampa + 1, 1, base - tampa - 1, ferroLuz);
    px(x + w - 1, tampa + 1, 1, base - tampa - 1, ferroEsc); px(x, base - 1, w, 1, ferroEsc);
    [x + 2, x + w - 4].forEach((cx) => {                                                      // as cintas e os rebites
      px(cx, topo + (cx === x + 2 ? 2 : 2), 2, base - topo - 3, "#53555c"); px(cx, topo + 2, 1, base - topo - 3, "#62646c");
      px(cx + 1, tampa + 2, 1, 1, "#9a9ca4"); px(cx + 1, base - 3, 1, 1, "#9a9ca4");
    });
    const meio = x + Math.floor(w / 2) - 2;
    px(meio, tampa - 1, 4, 5, "#7a6438"); px(meio, tampa - 1, 4, 1, "#a8904c"); px(meio + 1, tampa + 1, 2, 2, "#120f0c");  // a fechadura
    px(x + 5, base - 2, 3, 1, "#6a3e24"); px(x + w - 9, tampa + 3, 2, 1, "#6a3e24"); px(x + 7, topo + 2, 2, 1, "#6a3e24");  // a ferrugem
  }

  /** Um vulto de capa escura com capuz: sem rosto, sem marca (o que o texto diz dos pulsos fica no texto). `virado`:
   *  -1 olhando para a esquerda (a porta), 1 para a direita, 0 de frente. A borda do lado da luz clareia um pouco. */
  function vulto(px, x, pe, virado, ladoLuz) {
    const C = CORS, topo = pe - 27;
    px(x - 2, topo, 5, 1, C.capa); px(x - 3, topo + 1, 7, 4, C.capa);                          // o capuz
    px(x - 1 + Math.max(0, virado) - (virado < 0 ? 1 : 0), topo + 2, 3, 3, "#050506");            // a sombra do rosto
    for (let y = topo + 5; y < pe; y++) {                                                        // a capa, abrindo para baixo
      const meia = Math.round(3 + (y - topo - 5) * 0.2), barra = y === pe - 1 && (x + y) % 2;
      if (!barra) px(x - meia, y, meia * 2 + 1, 1, C.capa);
      px(ladoLuz > 0 ? x + meia : x - meia, y, 1, 1, C.capaBorda);
    }
    px(x - 1, pe, 1, 1, "#0a0a0d"); px(x + 1, pe, 1, 1, "#0a0a0d");                             // os pés
  }
  /** Na luta, os dois de capa escura continuam na sala, de frente para quem entrou pela porta (à esquerda), com a faca
   *  na mão e um balanço lento, cada um no seu tempo. Cada vulto é um inimigo: a carta dele traz a `figura` (o motor a
   *  dá a cada um, missoes.FIGURAS_SACRISTIA), e o vulto fica enquanto ela está de pé. Caído, ele se desfaz em
   *  pontilhado no tempo da carta (de uma vez com movimento reduzido); fugido, sai. Sem luta no estado (antes da
   *  primeira carta, ou depois de uma fuga ou de uma derrota, até a página virar), vale o que se viu por último: só
   *  quem caiu sai da sala. */
  // os dois avançaram para o meio da sala, à direita da lanterna (o vão entre a roda das ações e as cartas deles, onde
  // a sala aparece em todas as larguras)
  const VULTOS_LUTA = { prateleira: { x: 181, pe: 5, luz: -1, faca: 0 }, lanterna: { x: 199, pe: 6, luz: -1, faca: 3 } };
  const SAIDA_VULTO = 9;  // quadros (dez por segundo): o tempo da carta caindo
  function vultosNaLuta(px, ox, P, est, quadro, quieto) {
    const cb = App.estado && App.estado.combate;
    est.vultos = est.vultos || {};
    const cartas = cb ? cb.inimigos.filter((c) => c.figura) : [];
    Object.keys(VULTOS_LUTA).forEach((id) => {
      const carta = cartas.find((c) => c.figura === id), vivo = cartas.length ? !!(carta && carta.vivo) : true;
      // a primeira vez (a luta começando, ou a página recarregada no meio dela): como está, sem animar a saída
      const v = est.vultos[id] || (est.vultos[id] = { vivo, saiu: null });
      if (cartas.length) {
        if (v.vivo && !vivo) v.saiu = quadro;
        if (vivo) v.saiu = null;
        v.vivo = vivo;
      }
      const f = VULTOS_LUTA[id], resta = v.vivo ? 1 : quieto || v.saiu === null ? 0 : 1 - (quadro - v.saiu) / SAIDA_VULTO;
      if (resta <= 0) return;
      const p = resta >= 1 ? px : (x, y, w = 1, hh = 1, cor) => {  // desfazendo-se: só os pontos do pontilhado que restam
        for (let yy = y; yy < y + hh; yy++) for (let xx = x; xx < x + w; xx++) if (pontilha(xx, yy, Math.round(resta * 16))) px(xx, yy, 1, 1, cor);
      };
      const mexe = quieto ? 0 : Math.floor((quadro + f.faca * 4) / 8) % 2, x = ox + f.x, pe = P + f.pe;
      vulto(p, x, pe, -1, f.luz);
      p(x - 4, pe - 15, 2, 1, CORS.capa); p(x - 6, pe - 16 + mexe, 2, 1, "#c8ccd4");  // o braço para a frente e a faca
    });
  }
  /** A lanterna: a armação de ferro e o vidro aceso (`aceso` 0 apagado, 1 e 2: a chama tremendo). */
  function lanterna(px, x, y, aceso) {
    px(x, y - 2, 3, 1, CORS.ferroLuz); px(x + 1, y - 3, 1, 1, CORS.ferroLuz);
    px(x - 1, y - 1, 5, 5, CORS.ferro);
    px(x, y, 3, 3, aceso ? (aceso === 2 ? "#ffe08a" : "#ffd070") : "#2a2a28");
    if (aceso) px(x + 1, y + 1, 1, 1, "#fff4c8");
  }
  /** Os anéis da luz quente (a lanterna, a tocha), que tremem de leve; parados com movimento reduzido. */
  function aneis(px, W, lx, ly, raio, forca = 1) {
    for (let y = 0; y < QH; y++) for (let x = Math.max(0, lx - raio); x < Math.min(W, lx + raio); x++) {
      const d2 = ((x - lx) ** 2 + ((y - ly) * 1.6) ** 2) / (raio * raio);
      if (d2 >= 1) continue;
      const a = d2 < 0.08 ? 0.18 : d2 < 0.3 ? 0.11 : d2 < 0.65 ? 0.06 : 0.03;
      px(x, y, 1, 1, `rgba(255,${d2 < 0.08 ? 190 : d2 < 0.3 ? 170 : 160},${d2 < 0.08 ? 110 : 90},${(a * forca).toFixed(3)})`);
    }
  }

  function desenharSacristia(c, W, b, est, quadro, destaque) {
    const px = pincel(c), ox = b.ox, d = b.d, quieto = reduzido(), q = quieto ? 0 : quadro, L = b.luz, P = SAC.piso;
    c.drawImage(b.canvas, 0, 0);
    const treme = quieto ? 0 : (q % 3) - 1;
    if (d.momento === "entrada") {
      // os dois de capa escura: um revirando as prateleiras, de lado, com a faca na outra mão; o outro de frente,
      // erguendo a lanterna para quem chega
      const mexe = quieto ? 0 : Math.floor(q / 6) % 2;
      aneis(px, W, ox + L.x, L.y, 58 + treme);
      vulto(px, ox + 92, P + 5, -1, 1);
      px(ox + 88 - mexe, 30 + mexe, 1, 6, CORS.capa); px(ox + 87 - mexe, 29 + mexe, 2, 1, "#5a4a3c");     // o braço na prateleira
      px(ox + 96, 46, 1, 3, CORS.capa); px(ox + 97, 48, 2, 1, "#c8ccd4");                                // a faca, baixa
      vulto(px, ox + 154, P + 6, 0, -1);
      px(ox + 157, 33, 1, 5, CORS.capa); px(ox + 158, 32, 1, 2, CORS.capa);                               // o braço erguido
      lanterna(px, ox + L.x - 1, L.y - 1 + (quieto ? 0 : (Math.floor(q / 9) % 2)), quieto ? 1 : 1 + (q % 2));
    } else {  // da luta em diante, a lanterna fica no chão onde o vulto a largou, acesa, no mesmo lugar e do mesmo jeito
      aneis(px, W, ox + L.x, L.y, 54 + treme);
      lanterna(px, ox + L.x - 1, L.y - 3, quieto ? 1 : 1 + (q % 2));
      if (d.momento === "luta") vultosNaLuta(px, ox, P, est, quadro, quieto);
    }
    // os pontos acesos no mouse e no foco
    const ouro = COR.ouro;
    if (destaque === "porta") { const pt = SAC.porta, x0 = ox + pt.x; px(x0 - 2, pt.topo + 2, 1, P - pt.topo - 2, ouro); px(x0 + pt.w + 1, pt.topo + 2, 1, P - pt.topo - 2, ouro); px(x0 + 4, pt.topo - 2, pt.w - 8, 1, ouro); }
    if (destaque === "alcapao") { const al = SAC.alcapao, ax = ox + al.x; px(ax - al.meia - 2, al.y - 1, al.meia * 2 + 4, 1, ouro); px(ax - al.meia - 4, al.y + al.alt, al.meia * 2 + 8, 1, ouro); }
    if (destaque === "janela") { const jn = SAC.janela, jx = ox + jn.x; px(jx - 1, jn.y + 4, 1, jn.h - 4, ouro); px(jx + jn.w, jn.y + 4, 1, jn.h - 4, ouro); px(jx + 2, jn.y - 1, jn.w - 4, 1, ouro); }
    if (destaque === "livro") { const bk = SAC.buraco, bx = ox + bk.x; px(bx - 2, bk.y - 3, bk.w + 4, 1, ouro); px(bx - 2, bk.y + bk.h + 5, bk.w + 4, 1, ouro); }
    if (destaque === "bau") { const bu = ox + SAC.bau.x, bw = SAC.bau.w; px(bu - 2, SAC.bau.y - 2, bw + 4, 1, ouro); px(bu - 2, P + 5, bw + 4, 1, ouro); }
  }

  // ================================================================ o fundo alagado
  // Um poço baixo e escuro com a água pela cintura: a escada de pedra do ossuário descendo pela esquerda até a água, as
  // duas pedras de moinho no meio, as correntes que descem do buraco do ossuário (o mesmo do sarilho, lá em cima; aqui
  // não há outro sarilho) e Ilse entre as pedras. O motor diz o estado: as correntes presas (esticadas até as pedras e
  // nos pulsos dela, os braços puxados para os lados) ou soltas (frouxas, pendendo, os braços caídos); Ilse presente,
  // ausente (na luta ela é a carta; depois do desfecho, foi embora) ou nas cenas do desfecho; a água escura, ou clara
  // depois do descanso. A luz: a tocha de quem está ali, ao pé da escada; sem ela, só o pouco que desce do buraco do
  // ossuário. Os momentos (os olhos que se abrem, o canto que falha, a fita, afundar, desfazer-se) vêm por celebração,
  // quando o texto chega neles.
  const FUNDO = { agua: 46, cx: 168, pedra: 40, raio: 13, buraco: 168 };
  const CORF = {
    teto: "#0c1012", pedra: "#232a2c", pedraLuz: "#3a4542", pedraSombra: "#141a1b", junta: "#192022", limo: "#25372c",
    agua: "#061012", aguaMeio: "#0a1a1d", aguaLuz: "#1f383c", mo: "#4a4c48", moLuz: "#6a6c64", moSombra: "#2c2e2a",
    moSulco: "#383a36", ferro: "#4a4c54", ferroLuz: "#7a7c86", pele: "#7d98a6", peleSombra: "#55707e", peleLuz: "#a0b8c2",
    peleCalma: "#a4aeb0", peleCalmaSombra: "#7a868a", cabelo: "#1c2b1f", cabeloLuz: "#2c4130", cabeloEsc: "#0d160f",
    veste: "#3a3430", vesteSombra: "#25211e", olhoFechado: "#3a4c56", olho: "#c4d4da", fita: "#a87a76", fitaSombra: "#7a5654",
  };
  /** Onde está a luz: a tocha de quem está ali, ao pé da escada; sem ela, o pouco que desce do buraco do ossuário. */
  function luzFundo(d) {
    return d.luz === "tocha" ? { x: 62, y: 38, perto: 52, longe: 210, max: 0.55, tocha: true }
      : { x: FUNDO.buraco, y: 6, perto: 30, longe: 175, max: 0.6, tocha: false };
  }

  function baseFundo(W, d) {
    const k = camada(W), c = k.getContext("2d"), px = pincel(c), ox = Math.round((W - QW) / 2), C = CORF, A = FUNDO.agua;
    d = d || { correntes: "presas", agua: "escura" };
    // a parede úmida em blocos, o teto baixo e a linha do limo perto da água
    px(0, 0, W, QH, C.pedra);
    for (let y = 9; y < A; y += 6) for (let x = ((y / 6) % 2) * 8 - 16; x < W; x += 16) { px(x, y, 16, 1, C.junta); px(x, y, 1, 6, C.junta); }
    px(0, 0, W, 7, C.teto); px(0, 7, W, 1, C.pedraSombra);
    for (let x = 0; x < W; x++) { const hh = 2 + ((x * 7) % 5 === 0 ? 1 : 0); px(x, A - hh, 1, hh, C.limo); }
    // o buraco do ossuário no teto, por onde as correntes descem (o mesmo do sarilho); um resto de luz quente de cima
    const bx = ox + FUNDO.buraco;
    px(bx - 9, 0, 19, 4, "#020303"); px(bx - 10, 4, 21, 1, C.pedraLuz);
    px(bx - 7, 3, 15, 1, "rgba(255,170,90,0.18)"); px(bx - 4, 2, 9, 1, "rgba(255,170,90,0.1)");
    // a escada de pedra, a do ossuário, descendo pela esquerda desde a boca no teto até a água (e sumindo nela)
    px(ox + 6, 0, 26, 7, "#030405"); px(ox + 5, 7, 28, 1, C.pedraLuz);
    for (let k2 = 0; k2 < 11; k2++) {
      const x = ox + 8 + k2 * 5, y = 9 + k2 * 4;
      px(x, y + 1, 6, QH - y - 1, "#1d2426");
      for (let yy = y + 3; yy < QH; yy += 4) px(x + ((yy + k2) % 2 ? 0 : 3), yy, 3, 1, C.pedraSombra);
      px(x, y + 1, 5, 3, "#2c3436"); px(x, y, 9, 1, "#56605e"); px(x + 5, y + 1, 1, 3, "#0f1314");
    }
    // as duas pedras de moinho, de pé, metade dentro da água: o olho no meio e os sulcos
    const pedras = [ox + FUNDO.cx - FUNDO.pedra, ox + FUNDO.cx + FUNDO.pedra], R = FUNDO.raio, py = A - 8;
    pedras.forEach((mx, lado) => {
      for (let y = -R; y <= R; y++) for (let x = -R; x <= R; x++) {
        const dd = x * x + y * y;
        if (dd > R * R) continue;
        const borda = dd > (R - 1.5) ** 2, luz = (lado ? -x : x) < -4 && y < 0;
        px(mx + x, py + y, 1, 1, borda ? C.moSombra : luz ? C.moLuz : C.mo);
      }
      for (let a = 0; a < 8; a++) {  // os sulcos, retos, do olho para a borda
        const ang = a * Math.PI / 4 + 0.3;
        for (let r = 4; r < R - 2; r += 1) if (r % 3) px(Math.round(mx + Math.cos(ang) * r), Math.round(py + Math.sin(ang) * r), 1, 1, C.moSulco);
      }
      px(mx - 2, py - 2, 4, 4, "#0c0e0c"); px(mx - 2, py - 3, 4, 1, C.moSombra);  // o olho
    });
    // o chão do poço, de pedras soltas (com a água escura, quase não se vê)
    for (let i = 0; i < 26; i++) { const x = ox + 70 + ((i * 37) % 200), y = 60 + ((i * 7) % 11); px(x, y, 3 + (i % 3), 2, i % 2 ? C.pedraLuz : C.pedra); }
    // a água: escura, mais funda embaixo, e o que está dentro dela (as pedras, a escada) fica turvo; clara, depois do
    // descanso, deixa ver o fundo
    const clara = d.agua === "clara";
    for (let y = A; y < QH; y++) {
      const f = (y - A) / (QH - A);
      for (let x = 0; x < W; x++) px(x, y, 1, 1, clara ? `rgba(24,52,54,${(0.3 + f * 0.25).toFixed(2)})`
        : `rgba(${Math.round(lerp(10, 4, f))},${Math.round(lerp(26, 14, f))},${Math.round(lerp(29, 16, f))},${(0.72 + f * 0.2).toFixed(2)})`);
    }
    px(0, A, W, 1, clara ? "#2e5254" : C.aguaLuz);
    // o lodo, ao pé da escada, logo abaixo da superfície: manchas escuras e finas sobre as pedras
    [[72, 2, 6], [79, 3, 5], [85, 2, 7], [93, 3, 5], [76, 5, 9], [89, 5, 6]].forEach(([x, dy, w]) => px(ox + x, A + dy, w, 1, "rgba(34,28,16,0.75)"));
    // os reflexos: as pedras, quebrados em faixas
    pedras.forEach((mx) => { for (let y = A + 2; y < A + 12; y += 2) px(mx - R + ((y * 3) % 4), y, 2 * R - 2, 1, misturar(C.aguaMeio, C.mo, 0.18)); });
    // a luz e a penumbra: longe da fonte, a sala escurece em degraus; as pedras e a escada continuam legíveis
    const L = luzFundo(d);
    escurecer(px, W, ox + L.x, L.y, L.perto, L.longe, L.max);
    pedras.forEach((mx) => { for (let a = 0; a < 18; a++) { const ang = Math.PI + (a / 17) * Math.PI; px(Math.round(mx + Math.cos(ang) * R), Math.round(py + Math.sin(ang) * R), 1, 1, "rgba(150,160,150,0.35)"); } });
    for (let k2 = 0; k2 < 11; k2++) px(ox + 8 + k2 * 5, 9 + k2 * 4, 8, 1, "rgba(150,160,150,0.22)");
    return { canvas: k, ox, d, luz: L, pedras, py };
  }

  /** Uma corrente de (x0, y0) a (x1, y1): reta (esticada) ou com barriga (`folga` em pixels, frouxa). Elos alternados. */
  function corrente(px, x0, y0, x1, y1, folga = 0, balanco = 0) {
    const n = Math.max(2, Math.ceil(Math.hypot(x1 - x0, y1 - y0)));
    for (let i = 0; i <= n; i++) {
      const t = i / n, x = Math.round(lerp(x0, x1, t) + Math.sin(t * Math.PI) * balanco), y = Math.round(lerp(y0, y1, t) + Math.sin(t * Math.PI) * folga);
      if (y >= FUNDO.agua + 1) continue;
      px(x, y, 1, 1, i % 3 === 0 ? CORF.ferroLuz : CORF.ferro);
    }
  }

  /** Ilse, da cintura para cima, entre as pedras. `pose`: "presa" (os braços puxados para as pedras, correntes no corpo),
   *  "solta" (os braços caídos, as correntes pendendo dos pulsos), "calma" (o descanso: a pele menos azul, o cabelo
   *  quieto), com `fita` nas mãos. `olhos`: abertos ou fechados. `desce`: quantos pixels afundou. `some`: 0 a 1, o
   *  quanto já se desfez (pixels faltando no pontilhado). Tudo o que fica abaixo da água não é desenhado. */
  function ilseDesenho(px, cx, pose, olhos, fita, desce, some, q) {
    const C = CORF, A = FUNDO.agua, calma = pose === "calma";
    const pele = calma ? C.peleCalma : C.pele, sombra = calma ? C.peleCalmaSombra : C.peleSombra;
    const p = (x, y, w, hh, cor) => {
      for (let yy = y; yy < y + hh; yy++) for (let xx = x; xx < x + w; xx++) {
        const yd = yy + desce;
        if (yd >= A) continue;
        if (some && pontilha(xx, yd, Math.round(some * 16))) continue;
        px(xx, yd, 1, 1, cor);
      }
    };
    const T = 20, mexe = calma || !q ? 0 : Math.floor(q / 9) % 2;
    // O cabelo de algas, atrás: mechas escuras, soltas, de comprimentos diferentes e mais cheias à esquerda, que descem
    // ondulando até a água (com o descanso, quietas). Não é um bloco: cada mecha tem falhas.
    [[-4, 3, 20], [-5, 4, 23], [-6, 5, 18], [-7, 8, 15], [-8, 12, 9], [4, 4, 13], [5, 6, 16], [6, 9, 10]].forEach(([dx, y0, comp], i) => {
      for (let k = 0; k < comp; k++) {
        if ((k + i) % 7 === 6) continue;
        const onda = calma ? 0 : (Math.floor((k + mexe * 2 + i) / 3) % 2) * (dx < 0 ? -1 : 1);
        p(cx + dx + onda, T + y0 + k, 1, 1, k % 5 === 0 ? C.cabeloLuz : i % 2 ? C.cabelo : C.cabeloEsc);
      }
    });
    // o vestido escuro, os ombros e o pescoço
    p(cx - 4, T + 11, 9, 1, C.veste); p(cx - 5, T + 12, 11, A - T - 12, C.veste);
    p(cx + 3, T + 12, 3, A - T - 12, C.vesteSombra); p(cx - 5, T + 12, 1, A - T - 12, C.vesteSombra);
    p(cx - 1, T + 10, 3, 1, pele); p(cx, T + 11, 1, 1, pele);
    // os braços: presos, puxados para as pedras; soltos, caídos, com as argolas e a corrente pendendo; com a fita, as
    // mãos juntas na frente
    if (pose === "presa") {
      p(cx - 11, T + 13, 6, 2, pele); p(cx + 6, T + 13, 6, 2, pele); p(cx + 6, T + 14, 6, 1, sombra);
      p(cx - 12, T + 13, 1, 2, C.ferroLuz); p(cx + 12, T + 13, 1, 2, C.ferroLuz);
      for (let k = 0; k < 9; k++) { p(cx - 4 + k, T + 15 + Math.floor(k / 2), 1, 1, k % 2 ? C.ferro : C.ferroLuz); p(cx + 4 - k, T + 19 + Math.floor(k / 2), 1, 1, k % 2 ? C.ferroLuz : C.ferro); }
    } else if (fita) {  // os braços dobrados, as mãos juntas na frente do peito, com a fita enrolada nos dedos
      p(cx - 7, T + 12, 2, 5, pele); p(cx + 6, T + 12, 2, 5, sombra);
      for (let k = 0; k < 4; k++) { p(cx - 6 + k, T + 17 + Math.floor(k / 2), 2, 1, pele); p(cx + 5 - k, T + 17 + Math.floor(k / 2), 2, 1, sombra); }
      p(cx - 2, T + 18, 5, 2, pele);
      p(cx - 2, T + 18, 5, 1, C.fita); p(cx - 1, T + 19, 3, 1, C.fitaSombra); p(cx + 1, T + 20, 1, 3, C.fita); p(cx + 2, T + 23, 1, 1, C.fitaSombra);
    } else {
      p(cx - 7, T + 12, 2, 10, pele); p(cx + 6, T + 12, 2, 10, sombra);
      p(cx - 7, T + 22, 2, 1, sombra); p(cx + 6, T + 22, 2, 1, sombra);
      if (pose === "solta") for (const x of [cx - 7, cx + 7]) { p(x, T + 21, 1, 1, C.ferroLuz); for (let k = 0; k < 4; k++) p(x, T + 23 + k, 1, 1, k % 2 ? C.ferroLuz : C.ferro); }
    }
    // a cabeça: o rosto azulado (no descanso, menos azul) e o cabelo molhado colado nele: uma mecha grossa desce do
    // alto da cabeça na frente do rosto e cobre o olho direito; outra, fina, corta a face esquerda; dos lados, a da
    // esquerda vai até o peito e a da direita para antes, num bolo de alga
    p(cx - 2, T, 5, 1, C.cabeloEsc); p(cx - 3, T + 1, 7, 1, C.cabelo); p(cx - 1, T + 1, 2, 1, C.cabeloLuz);
    p(cx - 2, T + 2, 5, 7, pele); p(cx + 2, T + 2, 1, 7, sombra); p(cx - 1, T + 9, 3, 1, pele);
    const olho = olhos === "abertos" ? C.olho : C.olhoFechado;
    p(cx - 1, T + 4, 1, 1, olho);
    p(cx, T + 7, 1, 1, sombra);  // a boca
    p(cx - 2, T + 2, 4, 1, C.cabeloEsc);                                                       // a franja, molhada
    [[2, 2], [1, 3], [1, 4], [1, 5], [1, 6], [2, 7], [2, 8], [2, 9]].forEach(([dx, dy]) => p(cx + dx, T + dy, 1, 1, dy % 3 ? C.cabeloEsc : C.cabelo));
    p(cx, T + 3, 1, 2, C.cabeloEsc);                                                           // a mecha que cobre o olho
    [[-2, 3], [-2, 4], [-2, 5], [-1, 6], [-1, 7]].forEach(([dx, dy]) => p(cx + dx, T + dy, 1, 1, C.cabelo));  // a fina
    p(cx - 3, T + 2, 1, 15, C.cabelo); p(cx - 3, T + 5, 1, 2, C.cabeloLuz); p(cx - 4, T + 14, 1, 4, C.cabeloEsc);
    p(cx + 3, T + 2, 1, 10, C.cabeloEsc); p(cx + 3, T + 11, 2, 2, C.cabelo); p(cx + 4, T + 13, 1, 1, C.cabeloEsc);
    // as mechas que boiam na água, em volta dela
    if (!desce && !some) [[-10, 0], [-8, 1], [8, 0], [10, 1], [12, 0]].forEach(([dx, dy]) => px(cx + dx, A + dy, 2, 1, C.cabeloEsc));
  }

  function desenharFundo(c, W, b, est, quadro, destaque) {
    const px = pincel(c), ox = b.ox, d = b.d, quieto = reduzido(), q = quieto ? 0 : quadro, A = FUNDO.agua, L = b.luz;
    c.drawImage(b.canvas, 0, 0);
    const cx = ox + FUNDO.cx, bx = ox + FUNDO.buraco, [pe, pd] = b.pedras, R = FUNDO.raio;
    // a tocha de quem está ali, ao pé da escada: anéis quentes e o reflexo dela quebrado na água
    if (L.tocha) {
      aneis(px, W, ox + L.x, L.y, 90 + (quieto ? 0 : (q % 3) - 1), 0.75);
      [[3, 7], [6, 5], [10, 4], [15, 3], [21, 2]].forEach(([dy, w], i) => px(ox + L.x - 3 + ((i * 3 + Math.floor(q / 4)) % 5) - 2, A + dy, w, 1, "rgba(255,170,90,0.2)"));
    } else {  // o pouco de luz do buraco: um brilho fraco na água embaixo dele
      for (let y = A + 2; y < A + 10; y += 2) px(bx - 2 + ((y + Math.floor(q / 4)) % 3), y, 3, 1, "rgba(200,170,120,0.12)");
    }
    const mostra = est.ilse !== "ausente";
    const balanco = est.falha > 0 ? Math.sin(est.falha / 2) * 1.2 : 0;
    // as correntes do buraco às pedras: esticadas (presas) ou com barriga, frouxas, caindo na água (soltas)
    if (d.correntes === "presas") {
      corrente(px, bx - 3, 4, pe, b.py - 1, 0, balanco); corrente(px, bx + 3, 4, pd, b.py - 1, 0, balanco);
      if (mostra) {  // nos pulsos dela; desfazendo-se, as pontas caem para a água
        const s = est.some || 0, xs = Math.round(12 - 9 * s), ys = Math.round(34 + (A - 34) * s);
        corrente(px, cx - xs, ys, pe + 2, b.py); corrente(px, cx + xs, ys, pd - 2, b.py);
      } else { corrente(px, pe + 2, b.py, cx - 3, A); corrente(px, pd - 2, b.py, cx + 3, A); }  // até a água entre as pedras
    } else {
      corrente(px, bx - 3, 4, pe + 6, A, 9, balanco); corrente(px, bx + 3, 4, pd - 6, A, 9, balanco);
      corrente(px, pe + 4, b.py - R + 2, pe + 10, A, 3); corrente(px, pd - 4, b.py - R + 2, pd - 10, A, 3);
    }
    // Ilse entre as pedras (ou o lugar vazio dela)
    frenteFundo(c, W, b, est, quadro);
    // a água: rodas devagar; com o canto, anéis que se abrem em volta dela; o canto que falha para tudo um instante
    const canta = mostra && est.canto && est.olhos === "abertos" && !est.desce && !est.some;
    if (!quieto && !est.falha && d.agua !== "clara") for (let i = 0; i < 5; i++) {  // clara, depois do descanso: parada
      const x = (i * 71 + Math.floor(q / 5) * 7) % W, y = A + 3 + ((i * 5) % 14);
      px(x, y, 3, 1, d.agua === "clara" ? "#2c4a50" : CORF.aguaLuz);
    }
    if (canta && !quieto) for (let r0 = 0; r0 < 2; r0++) {
      const r = ((q / 3 + r0 * 8) % 16) + 6;
      for (let a = 0; a < 24; a++) { const ang = a / 24 * Math.PI * 2, y = Math.round(A + 1 + Math.sin(ang) * r * 0.22); if (y > A) px(Math.round(cx + Math.cos(ang) * r), y, 1, 1, "rgba(120,160,165,0.35)"); }
    }
    if (est.falha > 0) {  // o canto falha: um anel só, saindo do lugar dela, e a água parada
      const r = 22 - est.falha;
      for (let a = 0; a < 30; a++) { const ang = a / 30 * Math.PI * 2, y = Math.round(A + 2 + Math.sin(ang) * r * 0.25); if (y > A) px(Math.round(cx + Math.cos(ang) * r), y, 1, 1, "rgba(150,190,195,0.5)"); }
    }
    if (est.desce > 0 && est.desce < 24) for (let a = 0; a < 20; a++) {  // afundando: a roda que ela deixa
      const r = 4 + est.desce * 0.6, ang = a / 20 * Math.PI * 2;
      px(Math.round(cx + Math.cos(ang) * r), Math.round(A + 1 + Math.sin(ang) * r * 0.2), 1, 1, "rgba(150,190,195,0.4)");
    }
    if (est.turvo > 0) {  // desfeita: bolhas subindo e a água turva que se espalha e assenta
      const t = est.turvo / 30;
      for (let y = A + 1; y < QH; y++) for (let x = cx - 40; x < cx + 40; x++) {
        const dd = Math.hypot((x - cx) / 40, (y - A - 6) / 14);
        if (dd < 1 && pontilha(x, y, Math.round((1 - dd) * 12 * t))) px(x, y, 1, 1, "rgba(70,56,36,0.55)");
      }
      for (let i = 0; i < 7; i++) { const y = A - 2 - ((Math.floor(q / 2) + i * 5) % 14); if (t > 0.3) px(cx - 6 + i * 2, y, 1, 1, "rgba(180,200,205,0.6)"); }
    }
    // os pontos acesos no mouse e no foco
    const ouro = COR.ouro;
    if (destaque === "escada") { px(ox + 5, 6, 30, 1, ouro); for (let k2 = 0; k2 < 11; k2++) px(ox + 8 + k2 * 5, 8 + k2 * 4, 9, 1, ouro); }
    if (destaque === "lodo") { px(ox + 68, A + 3, 34, 1, ouro); px(ox + 68, A + 9, 34, 1, ouro); }
  }

  /** Ilse entre as pedras (ou o lugar vazio dela). Na mistura curta de uma troca de momento (da descida para a luta, da
   *  luta para o desfecho), é desenhada de novo por cima dela: ela continua ali, sem a base de antes a cobrir. */
  function frenteFundo(c, W, b, est, quadro) {
    if (est.ilse === "ausente") return;
    const d = b.d, q = reduzido() ? 0 : quadro;
    const pose = est.ilse === "descanso" ? "calma" : est.ilse === "destruida" ? (d.correntes === "soltas" ? "solta" : "presa") : est.ilse;
    ilseDesenho(pincel(c), b.ox + FUNDO.cx, pose, est.olhos, est.fita, est.desce || 0, est.some || 0, q);
  }

  /** O momento de Ilse que o motor acabou de contar (celebrar "ilse"). Recarregando ou com movimento reduzido, o fim
   *  dele de uma vez. A promessa resolve quando termina (o texto seguinte espera). */
  function momentoIlse(dados, instantaneo) {
    const a = atual && atual.d.cena === "fundo" ? atual : null;
    if (!a) return Promise.resolve();
    const est = a.est, m = dados && dados.momento, rapido = instantaneo || reduzido();
    const fim = {
      acorda: () => { est.olhos = "abertos"; est.canto = true; },
      canto_falha: () => { est.falha = 0; est.canto = false; },
      fita: () => { est.fita = true; },
      afunda: () => { est.desce = 0; est.ilse = "ausente"; aguaClara(a); },
      desfaz: () => { est.some = 0; est.turvo = 0; est.ilse = "ausente"; },
    }[m];
    if (m === "grito") {  // o rito deixado: o canto vira grito (o texto acabou de dizer) e não volta
      est.canto = false; cantoDeIlse();
      if (!instantaneo) App.som("grito_ilse");
      return Promise.resolve();
    }
    if (!fim) return Promise.resolve();
    // o som acompanha o começo do momento: o canto entra quando ela começa a cantar e para quando falha ou some
    if (m === "acorda") est.canto = true;
    if (m === "canto_falha" || m === "desfaz") est.canto = false;
    cantoDeIlse();
    if (rapido) { fim(); return Promise.resolve(); }
    if (m === "fita") { fim(); return new Promise((r) => setTimeout(r, 400)); }
    return new Promise((r) => { est.anim = { m, passo: 0, fim, resolver: r }; });
  }
  /** O canto de Ilse, pelo que a cena mostra agora: no fundo, com ela cantando na água (desde que acordou), alto; na
   *  luta e na cena da destruição, baixo (não cobre os golpes); fora do fundo, no descanso e depois, nada. Um canal só
   *  (Som.canto): pedir de novo não soma outro. */
  function cantoDeIlse() {
    const a = atual, est = a && a.est;
    let nivel = null;
    if (a && a.d.cena === "fundo" && est.canto && !est.desce && !est.some) {
      if (["luta", "destruida"].includes(a.d.momento)) nivel = "baixo";
      else if (["presa", "solta"].includes(est.ilse)) nivel = "alto";
    }
    Som.canto(nivel);
  }
  /** Depois do descanso, a água fica parada e clara: a base é refeita com a água clara (o mesmo objeto, para quem
   *  desenha já pegar a nova). */
  function aguaClara(a) {
    a.d = Object.assign({}, a.d, { agua: "clara" });
    Object.assign(a.b, baseFundo(QW, a.d));
  }
  /** Um passo dos momentos de Ilse (dez por segundo). */
  function passoIlse(est) {
    const an = est.anim;
    if (!an) return;
    an.passo++;
    const acabar = () => { est.anim = null; est.desce = 0; est.some = 0; est.turvo = 0; est.falha = 0; an.fim(); an.resolver(); };
    if (an.m === "acorda") { est.olhos = an.passo % 4 < 2 && an.passo < 6 ? "fechados" : "abertos"; if (an.passo >= 8) acabar(); }
    else if (an.m === "canto_falha") { est.canto = false; est.falha = Math.max(1, 22 - an.passo); if (an.passo >= 20) acabar(); }
    else if (an.m === "afunda") { est.desce = Math.min(24, Math.floor(an.passo / 1.5)); if (an.passo >= 40) acabar(); }
    else if (an.m === "desfaz") {
      est.some = Math.min(1, an.passo / 22); est.turvo = an.passo < 22 ? an.passo + 8 : Math.max(0, 30 - (an.passo - 22) * 2);
      if (an.passo >= 37) acabar();
    }
  }

  // As sanguessugas da sala inquieta: [x, y, para que lado o corpo cresce]. No encosto submerso do banco da frente (o
  // de 42 de largura), na perna de um banco de trás onde ela entra na água e no pé de uma coluna.
  const SANGUESSUGAS = [[70, 55, 1], [96, 55, -1], [133, 51, 1], [COLUNAS[2] - 6, 51, 1]];

  // ================================================================ as cenas e os pontos
  // Cada ponto: a área clicável, onde fica o nome e para onde a câmera vai (no quadro de 320×72).
  const CENAS = {
    ossuario: { base: baseOssuario, desenhar: desenharOssuario,
      pontos: { sarilho: { area: [186, 14, 110, 56], balao: [240, 12], foco: [238, 48] },
                escada: { area: [2, 0, 46, 56], balao: [24, 20], foco: [26, 30] },
                descida: { area: [48, 57, 34, 15], balao: [65, 58], foco: [65, 62] } } },
    exterior: { base: baseExterior, desenhar: desenharExterior,
      pontos: { buraco: { area: [146, 36, 30, 20], balao: [161, 69], foco: [161, 44] },
                sapos: { area: [42, 52, 78, 14], balao: [80, 54], foco: [82, 58] } } },
    salao: { base: baseSalao, desenhar: desenharSalao,
      pontos: { porta: { area: [282, 26, 26, 20], balao: [295, 24], foco: [270, 36] },
                brecha: { area: [2, 24, 30, 30], balao: [17, 26], foco: [18, 40] } } },
    sacristia: { base: baseSacristia, desenhar: desenharSacristia,
      pontos: { porta: { area: [4, 16, 34, 42], balao: [21, 14], foco: [24, 40] },
                janela: { area: [184, 2, 24, 54], balao: [222, 14], foco: [198, 26] },
                livro: { area: [116, 19, 24, 22], balao: [128, 18], foco: [128, 30] },
                bau: { area: [270, 36, 26, 24], balao: [283, 35], foco: [283, 48] },
                alcapao: { area: [210, 56, 42, 14], balao: [230, 55], foco: [230, 62] } } },
    fundo: { base: baseFundo, desenhar: desenharFundo, frente: frenteFundo,
      pontos: { escada: { area: [4, 4, 62, 42], balao: [34, 10], foco: [40, 30] },
                lodo: { area: [66, 46, 38, 14], balao: [85, 47], foco: [96, 52] } } },
  };

  /** O contorno de um ponto aceso, no estilo da arte: quatro cantos dourados com a sombra por fora, em volta da área. */
  function cantos(c, [x, y, w, hh]) {
    const px = pincel(c), L = 4, x1 = x + w - 1, y1 = Math.min(QH - 1, y + hh - 1);
    [["#000000", 1], [COR.ouro, 0]].forEach(([cor, d]) => {
      [[x, y, 1, 1], [x1, y, -1, 1], [x, y1, 1, -1], [x1, y1, -1, -1]].forEach(([cx, cy, sx, sy]) => {
        for (let k = 0; k < L; k++) { px(cx + sx * k + d * sx, cy + d * sy, 1, 1, cor); px(cx + d * sx, cy + sy * k + d * sy, 1, 1, cor); }
      });
    });
  }

  // ---------------------------------------------------------------- a cena no topo
  // O painel "cena" não põe imagem no texto: ele troca a arte do topo (o mesmo canvas da paisagem, vista.js) pelo
  // ambiente, e os pontos ficam numa capa por cima dela (como os prédios da vila). Embaixo, só o texto e as escolhas.
  // Uma página nova sem painel de cena (outro lugar, um menu, a sacristia) devolve a paisagem.
  let atual = null;      // { d, def, b, est }: o ambiente à vista
  let pendente = false;  // a página virou: o ambiente sai, a menos que o próximo painel traga outro
  let capa = null;     // os pontos, sobre a arte

  function passo(est) {
    if (est.soltando) {
      est.passo++;
      if (est.passo >= 27) { est.soltando = false; est.correntes = "soltas"; est.onda = 12; if (est.fim) { est.fim(); est.fim = null; } }
    } else if (est.onda > 0) est.onda--;
  }

  // Na mesma sala, um acontecimento novo (a entrada, a luta, a vitória, a visita) não recomeça a cena: o mesmo quadro,
  // a mesma câmera e, no mesmo momento, a mesma animação; o que mudou (a luz, a lanterna, o baú) passa numa mistura
  // curta da base de antes para a nova (instantânea com movimento reduzido).
  const TROCA_MS = 280;
  function mostrar(d) {
    pendente = false;
    const def = CENAS[d.cena];
    if (!def) { limpar(); return; }
    const antes = atual && atual.d.cena === d.cena ? atual : null;
    const mesmo = !!antes && ["momento", "ilse", "correntes"].every((k) => antes.d[k] === d[k]);  // o mesmo acontecimento
    if (mesmo && antes.d.agua === "clara") d = Object.assign({}, d, { agua: "clara" });  // o que a tela já mostrou fica
    const b = def.base(QW, d), est = mesmo ? antes.est : { correntes: d.correntes, agua: d.agua, soltando: false, passo: 0, onda: 0,
      // `canto`: a música de Ilse; começa quando o fundo aparece na descida (os olhos e o canto na água esperam o texto)
      ilse: d.ilse, olhos: d.momento === "descida" ? "fechados" : "abertos", canto: ["descida", "visita"].includes(d.momento) && !!d.ilse && d.ilse !== "ausente",
      fita: false, desce: 0, some: 0, turvo: 0, falha: 0, anim: null };
    if (!mesmo && antes && d.cena === "fundo" && ["luta", "destruida"].includes(d.momento)) est.canto = antes.est.canto;
    const troca = antes && !reduzido() ? { de: antes.b.canvas, inicio: performance.now() } : null;
    atual = { d, def, b, est };
    cantoDeIlse();
    document.getElementById("cena").classList.add("com-ambiente");
    if (typeof recolherArte === "function") recolherArte(false);
    Vista.usarAmbiente({
      base: b.canvas, foco: d.foco ? def.pontos[d.foco].foco : null,
      desenhar: (ctx, quadro, destaque) => {  // a corrente descendo dá trancos no quadro
        const tranco = est.soltando && est.passo > 3 && est.passo < 22 && !reduzido() ? (est.passo % 2 ? 1 : -1) : 0;
        ctx.save(); ctx.translate(tranco, 0);
        def.desenhar(ctx, QW, b, est, quadro, destaque);
        ctx.restore();
        if (troca && troca.de) {  // a base de antes, sumindo por cima da nova
          const t = (performance.now() - troca.inicio) / TROCA_MS;
          if (t >= 1) troca.de = null;
          else {
            ctx.save(); ctx.globalAlpha = 1 - t; ctx.drawImage(troca.de, 0, 0); ctx.restore();
            // quem continua na sala (Ilse) não some por baixo da mistura
            if (def.frente) { ctx.save(); ctx.translate(tranco, 0); def.frente(ctx, QW, b, est, quadro); ctx.restore(); }
          }
        }
        acesos(destaque).forEach((id) => cantos(ctx, def.pontos[id].area));
      },
      andar: () => { passo(est); passoIlse(est); },
    });
    montarPontos();
  }
  function limpar() {
    pendente = false;
    if (!atual) return;
    atual = null;
    cantoDeIlse();  // saiu do fundo: o canto para
    document.getElementById("cena").classList.remove("com-ambiente");
    Vista.usarAmbiente(null);
    montarPontos();
  }
  /** A página virou (nova cena): o ambiente fica até a próxima mensagem; se ela não for um painel de cena, sai. */
  function virou() { if (atual) pendente = true; }
  function conferirPendente(m) {
    if (!["estado", "sincronizado"].includes(m.t)) tirarOlhar();  // o que se viu de perto não fica no meio do que veio
    if (pendente && !["estado", "sincronizado", "nova_cena", "cabecalho"].includes(m.t) && !(m.t === "painel" && m.tipo === "cena")) limpar();
  }

  /** Os pontos com contorno agora: o do mouse ou do foco e, com "Destacar interações", todos os que fazem algo. Só
   *  com os pontos valendo (fora da luta, sem estar de perto). */
  function acesos(destaque) {
    if (!atual || !capa || capa.hidden || capa.classList.contains("perto")) return [];
    const ids = destacando() ? atual.d.pontos.filter((p) => p.acao || p.olhar).map((p) => p.id) : [];
    if (destaque && !ids.includes(destaque) && atual.def.pontos[destaque]) ids.push(destaque);
    return ids.filter((id) => atual.def.pontos[id]);
  }
  // "Destacar interações" (Ajuda e F4): os nomes e os contornos de todos os pontos à vista; sem ele, só no mouse e no
  // foco do teclado. Preferência de quem joga, guardada no navegador.
  let destacar = false;
  try { destacar = localStorage.getItem("cdf-destacar") === "1"; } catch (e) { /* sem armazenamento */ }
  const destacando = () => destacar;
  function alternarDestaque(forcar) {
    destacar = forcar === undefined ? !destacar : !!forcar;
    try { localStorage.setItem("cdf-destacar", destacar ? "1" : "0"); } catch (e) { /* sem armazenamento */ }
    document.body.classList.toggle("destacar-interacoes", destacar);
    return destacar;
  }
  document.body.classList.toggle("destacar-interacoes", destacar);

  /** Onde cada ponto cai na tela: a arte é desenhada com object-fit: cover (centro, 80% para baixo), como na vila. */
  function posicionar() {
    if (!capa || capa.hidden) return;
    const vista = document.getElementById("vista"), cs = getComputedStyle(vista);
    const larg = vista.clientWidth, alt = vista.clientHeight - parseFloat(cs.paddingBottom);
    const esc = Math.max(larg / QW, alt / QH), dx = (larg - QW * esc) * 0.5, dy = (alt - QH * esc) * 0.8;
    Object.assign(capa.style, { left: vista.offsetLeft + "px", top: vista.offsetTop + "px", width: larg + "px", height: alt + "px" });
    capa.querySelectorAll(".ci-ponto").forEach((bt) => {
      const pd = atual && atual.def.pontos[bt.dataset.ponto];
      if (!pd) return;
      const [x, y, w, hh] = pd.area, [bx, by] = pd.balao;
      Object.assign(bt.style, { left: dx + x * esc + "px", top: dy + y * esc + "px", width: w * esc + "px", height: hh * esc + "px" });
      Object.assign(bt.querySelector(".ci-balao").style, { left: Math.round((bx - x) * esc) + "px", top: Math.round((by - y) * esc) + "px" });
    });
  }
  window.addEventListener("resize", posicionar);

  /** Os pontos só valem na página do lugar (no texto de uma cena, a escolha é a do menu dela), fora da luta e com a
   *  arte no topo. */
  function pontosValem() {
    return !!(atual && atual.d.pagina && !document.body.classList.contains("em-combate")
      && document.getElementById("vista").parentElement === document.getElementById("cena"));
  }
  function montarPontos() {
    if (!capa) {
      capa = document.createElement("div");
      capa.id = "pontos-cena";
      document.getElementById("cena").appendChild(capa);
      document.getElementById("vista").addEventListener("transitionend", posicionar);
    }
    fecharLeitura();  // uma página nova fecha o livro aberto
    capa.innerHTML = "";
    capa.classList.remove("perto");
    tirarOlhar();
    const d = atual && atual.d;
    capa.dataset.cena = d ? d.cena : "";
    capa.dataset.correntes = (d && d.correntes) || "";
    capa.dataset.agua = (d && d.agua) || "";
    capa.dataset.foco = (d && d.foco) || "";
    capa.dataset.pagina = d && d.pagina ? "1" : "";
    capa.hidden = !pontosValem();
    if (!d) return;
    const descricao = d.pontos.map((p) => p.estado).join(" ");
    capa.setAttribute("role", "group");
    capa.setAttribute("aria-label", `${d.titulo}${descricao ? ": " + descricao : ""}`);
    d.pontos.forEach((p) => {
      const ativo = !!p.acao || !!p.olhar;
      const rotulo = p.acao ? `${p.nome}: ${p.faz}` : p.olhar ? `${p.nome}: olhar de perto` : `${p.nome}. ${p.estado}`;
      const bt = document.createElement("button");
      bt.type = "button";
      bt.className = "ci-ponto" + (ativo ? "" : " parado");
      bt.dataset.ponto = p.id;
      bt.setAttribute("aria-label", rotulo);
      if (!ativo) { bt.setAttribute("aria-disabled", "true"); bt.tabIndex = -1; }
      bt.innerHTML = `<span class="ci-balao">${h(p.nome)}</span>`;
      ligarPonto(bt, p);
      capa.appendChild(bt);
    });
    const afastar = document.createElement("button");
    afastar.type = "button"; afastar.className = "ci-afastar"; afastar.hidden = true; afastar.textContent = "Afastar";
    afastar.addEventListener("click", (ev) => longe(ev.detail === 0));  // detail 0: Enter ou espaço, pelo teclado
    capa.appendChild(afastar);
    requestAnimationFrame(posicionar);
  }
  /** O ponto: destaque no mouse e no foco. Com ação: o clique (ou Enter/espaço) aproxima a câmera e manda a mesma ação
   *  do menu. De olhar: só aproxima, e "Afastar" volta. Sem nada: diz o estado. */
  function ligarPonto(bt, p) {
    // Três destaques diferentes: o global (F4, em acesos), o do mouse (enquanto ele está em cima) e o do foco do
    // teclado (:focus-visible: o foco que o mouse deixa num botão não acende nada).
    const acender = (sim) => { bt.classList.toggle("aceso", sim); Vista.destacar(sim ? p.id : null); };
    bt.addEventListener("mouseenter", () => acender(true));
    bt.addEventListener("focus", () => acender(bt.matches(":focus-visible")));
    bt.addEventListener("mouseleave", () => acender(bt.matches(":focus-visible")));
    bt.addEventListener("blur", () => acender(bt.matches(":hover")));
    bt.addEventListener("click", async (ev) => {
      ev.stopPropagation();
      if (processando) { pular = true; return; }  // a página ainda corre: o clique adianta, como na arte
      if (!pontosValem()) return;
      const foco = atual.def.pontos[p.id].foco;
      if (p.olhar) {
        App.som("escolha");
        capa.classList.add("perto"); bt.setAttribute("data-olhado", "");
        Vista.destacar(null);
        await Vista.focarEm(foco);
        if (typeof p.olhar === "string") {  // o que se vê de perto, curto, embaixo do texto da página (sai ao afastar)
          tirarOlhar();
          const nota = document.createElement("p");
          nota.className = "olhar-perto"; nota.textContent = p.olhar;
          document.getElementById("texto").appendChild(nota);
        }
        const af = capa.querySelector(".ci-afastar"); af.hidden = false; af.focus();
        return;
      }
      if (!p.acao) { App.som("falha"); App.avisar(p.estado, "ponto"); return; }
      const pode = (App.opcoes() || []).some((o) => o.meta && Object.entries(p.acao).every(([k, v]) => o.meta[k] === v));
      if (!pode) { App.som("falha"); App.avisar("Agora não: termine o que está fazendo primeiro.", "ponto"); return; }
      App.som("escolha");
      capa.classList.add("perto");
      await Vista.focarEm(foco);
      if (!App.acao(p.acao)) { capa.classList.remove("perto"); Vista.focarEm(null); }
    });
  }
  function tirarOlhar() { document.querySelectorAll("#texto .olhar-perto").forEach((e) => e.remove()); }
  /** Afastar: a vista geral volta, com os nomes e contornos como estavam (F4 incluído). Pelo teclado, o foco volta ao
   *  ponto olhado (com o indicador de foco); pelo mouse, nada fica aceso: o ponteiro já está longe dele. */
  function longe(teclado) {
    if (!capa || !capa.classList.contains("perto")) return false;
    tirarOlhar();
    const af = capa.querySelector(".ci-afastar");
    if (af) { if (!teclado && document.activeElement === af) af.blur(); af.hidden = true; }
    Vista.focarEm(null).then(() => {
      capa.classList.remove("perto");
      const bt = capa.querySelector(".ci-ponto[data-olhado]");
      if (bt) {
        bt.removeAttribute("data-olhado");
        bt.classList.remove("aceso"); Vista.destacar(null);  // o destaque do clique de antes não fica
        if (teclado) bt.focus();
      }
    });
    return true;
  }
  // ---------------------------------------------------------------- ler (o livro da sacristia)
  // Um livro aberto, como o Grimório, por cima da sala: o motor manda abrir (a celebração "livro", depois de registrar
  // a descoberta) com o título e as páginas prontos. Fechar (o botão, Esc, Enter, espaço ou o véu em volta) devolve a
  // sala e deixa o texto seguir; nada pede ler até o fim. Recarregando, não abre de novo.
  let leitura = null, aoFecharLeitura = null;
  function lerLivro(d, instantaneo) {
    if (instantaneo || !d || !d.paginas) return Promise.resolve();
    return new Promise((r) => { aoFecharLeitura = r; abrirLeitura(d, false); });
  }
  function abrirLeitura(ler, teclado) {
    if (!leitura) {
      leitura = document.createElement("div");
      leitura.id = "sobre-leitura"; leitura.className = "sobreposicao"; leitura.hidden = true;
      leitura.setAttribute("role", "dialog"); leitura.setAttribute("aria-modal", "true");
      leitura.addEventListener("click", (ev) => { if (ev.target === leitura) fecharLeitura(false); });
      document.body.appendChild(leitura);
    }
    const [p1, ...resto] = ler.paginas, pars = (t) => t.split("\n\n").map((x) => `<p class="leitura-texto">${h(x)}</p>`).join("");
    leitura.setAttribute("aria-label", ler.titulo);
    leitura.innerHTML = `<div class="grimorio-livro leitura-livro">
      <div class="grimorio-pagina esquerda"><div class="grimorio-cab"><b>${h(ler.titulo)}</b></div>${pars(p1)}</div>
      <div class="grimorio-pagina direita">${resto.map((t) => `<div class="leitura-entrada">${pars(t)}</div>`).join("")}</div>
      <button class="grimorio-fechar" type="button">Fechar <kbd>Esc</kbd></button></div>`;
    leitura.querySelector(".grimorio-fechar").addEventListener("click", (ev) => fecharLeitura(ev.detail === 0));
    leitura.hidden = false;
    leitura.dataset.teclado = teclado ? "1" : "";
    document.addEventListener("keydown", teclaLeitura, true);
    leitura.querySelector(".grimorio-fechar").focus({ focusVisible: !!teclado });
  }
  /** Com o livro aberto, as teclas são dele: Esc, Enter e espaço fecham; as outras não escolhem nada embaixo. */
  function teclaLeitura(ev) {
    if (!leitura || leitura.hidden) return;
    if (["Escape", "Enter", " "].includes(ev.key)) { ev.preventDefault(); ev.stopPropagation(); fecharLeitura(true); return; }
    if (ev.key === "Tab") { ev.preventDefault(); return; }  // um só controle: o foco fica nele
    if (!["F4", "F1"].includes(ev.key)) ev.stopPropagation();
  }
  function fecharLeitura() {
    if (!leitura || leitura.hidden) return false;
    leitura.hidden = true;
    document.removeEventListener("keydown", teclaLeitura, true);
    const fim = aoFecharLeitura; aoFecharLeitura = null;
    if (fim) fim();  // o texto segue (o Continuar da leitura)
    return true;
  }

  /** Esc com um ponto de olhar aproximado: afasta (como o botão, pelo teclado). */
  function afastar() { const af = capa && capa.querySelector(".ci-afastar"); return !!(af && !af.hidden && longe(true)); }
  /** Luta: os pontos saem (a arte desce para a arena); a câmera volta à sala inteira, para a arena mostrar o lugar. */
  function aoCombate() {
    if (!capa) return;
    capa.hidden = true;
    if (atual) Vista.focarEm(null);
  }
  /** Fim da luta ou pergunta nova: os pontos voltam se valem. */
  function aoMenu() {
    if (!capa) return;
    const valia = !capa.hidden;
    capa.hidden = !pontosValem();
    if (!capa.hidden && !valia) requestAnimationFrame(posicionar);
  }

  /** O motor gravou que as correntes soltaram: a arte do topo mostra a corrente descendo (refazendo a página, ou com
   *  movimento reduzido, já desenha as correntes soltas; com movimento reduzido o som fica: não é movimento). A arte
   *  está sempre inteira com o ambiente (pagina.js, recolherArte): a descida fica à vista sem a página pular. */
  function soltarCorrentes(instantaneo) {
    const est = atual && atual.d.cena === "ossuario" ? atual.est : null;
    if (!est || est.correntes === "soltas") return Promise.resolve();
    if (capa) capa.dataset.correntes = "soltas";
    if (instantaneo || reduzido()) {
      if (!instantaneo) App.som("corrente");
      est.correntes = "soltas";
      return Promise.resolve();
    }
    App.som("corrente");
    return new Promise((fim) => { est.soltando = true; est.passo = 0; est.fim = fim; });
  }

  Telas.registrar("cena", () => "", {});
  Object.assign(Telas, { soltarCorrentes, momentoIlse, lerLivro });
  window.Cenas = { mostrar, limpar, virou, conferirPendente, aoCombate, aoMenu, posicionar, atual: () => atual,
    alternarDestaque, destacando, afastar };
})();
