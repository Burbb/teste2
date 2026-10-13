/* Cenas interativas: um lugar desenhado em pixel art (como as paisagens: escala inteira, pontilhado de Bayer, dez
   quadros por segundo) com pontos clicáveis por cima. Por enquanto, três ambientes da Capela Afogada (roadmapIDEIAS/20):
   o exterior, o salão alagado e o ossuário com o sarilho. O motor diz qual ambiente, o estado dele (a água do salão
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

  // ================================================================ a sala sem arte própria
  // A sacristia e o fundo ainda não foram desenhados: em vez de mostrar outra sala no lugar deles, um fundo neutro,
  // a parede de pedra e o chão no escuro, com a luz da tocha de quem está ali no meio. Sem objetos nem pontos.
  function baseNeutra(W) {
    const k = camada(W), c = k.getContext("2d"), px = pincel(c), ox = Math.round((W - QW) / 2);
    px(0, 0, W, QH, COR.parede);
    for (let y = 4; y < PISO; y += 6) for (let x = ((y / 6) % 2) * 7 - 14; x < W; x += 14) { px(x, y, 14, 1, COR.junta); px(x, y, 1, 6, COR.junta); }
    for (let y = PISO; y < QH; y++) px(0, y, W, 1, y === PISO ? COR.pedraLuz : COR.chao);
    for (let y = PISO + 3; y < QH; y += 5) for (let x = (y * 3) % 10; x < W; x += 14) px(x, y, 9, 1, COR.chaoJunta);
    escurecer(px, W, ox + QW / 2, 34, 36, 160, 0.8);
    return { canvas: k, ox };
  }
  function desenharNeutra(c, W, b) { c.drawImage(b.canvas, 0, 0); }

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
    neutra: { base: baseNeutra, desenhar: desenharNeutra, pontos: {} },
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

  function mostrar(d) {
    pendente = false;
    const def = CENAS[d.cena];
    if (!def) { limpar(); return; }
    const b = def.base(QW), est = { correntes: d.correntes, agua: d.agua, soltando: false, passo: 0, onda: 0 };
    atual = { d, def, b, est };
    document.getElementById("cena").classList.add("com-ambiente");
    if (typeof recolherArte === "function") recolherArte(false);
    Vista.usarAmbiente({
      base: b.canvas, foco: d.foco ? def.pontos[d.foco].foco : null,
      desenhar: (ctx, quadro, destaque) => {  // a corrente descendo dá trancos no quadro
        const tranco = est.soltando && est.passo > 3 && est.passo < 22 && !reduzido() ? (est.passo % 2 ? 1 : -1) : 0;
        ctx.save(); ctx.translate(tranco, 0);
        def.desenhar(ctx, QW, b, est, quadro, destaque);
        ctx.restore();
        acesos(destaque).forEach((id) => cantos(ctx, def.pontos[id].area));
      },
      andar: () => passo(est),
    });
    montarPontos();
  }
  function limpar() {
    pendente = false;
    if (!atual) return;
    atual = null;
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
    afastar.addEventListener("click", longe);
    capa.appendChild(afastar);
    requestAnimationFrame(posicionar);
  }
  /** O ponto: destaque no mouse e no foco. Com ação: o clique (ou Enter/espaço) aproxima a câmera e manda a mesma ação
   *  do menu. De olhar: só aproxima, e "Afastar" volta. Sem nada: diz o estado. */
  function ligarPonto(bt, p) {
    const acender = (sim) => { bt.classList.toggle("aceso", sim); Vista.destacar(sim ? p.id : null); };
    ["mouseenter", "focus"].forEach((t) => bt.addEventListener(t, () => acender(true)));
    ["mouseleave", "blur"].forEach((t) => bt.addEventListener(t, () => acender(false)));
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
  function longe() {
    if (!capa) return;
    tirarOlhar();
    const af = capa.querySelector(".ci-afastar");
    if (af) af.hidden = true;
    Vista.focarEm(null).then(() => {
      capa.classList.remove("perto");
      const bt = capa.querySelector(".ci-ponto[data-olhado]");
      if (bt) { bt.removeAttribute("data-olhado"); bt.focus(); }
    });
  }
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
  Object.assign(Telas, { soltarCorrentes });
  window.Cenas = { mostrar, limpar, virou, conferirPendente, aoCombate, aoMenu, posicionar, atual: () => atual,
    alternarDestaque, destacando };
})();
