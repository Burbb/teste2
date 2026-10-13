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
    // a luz que desce pelo alçapão, nos primeiros degraus
    for (let y = 3; y < 34; y++) for (let x = ax + 1; x < ax + 16 + Math.floor(y / 3); x++) if (pontilha(x, y, Math.max(0, 4 - Math.floor(y / 9)))) px(x, y, 1, 1, "rgba(150,150,130,0.35)");
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
    return { canvas: k, ox };
  }

  /** O que se mexe: a tocha da parede, o tambor com a corrente, a trava, a manivela e as correntes até o buraco. */
  function desenharOssuario(c, W, b, est, quadro, destaque) {
    const px = pincel(c);
    c.drawImage(b.canvas, 0, 0);
    const ox = b.ox, quieto = reduzido();
    // a tocha na parede, ao lado da escada, com a luz que treme
    const tx = ox + 47, ty = 11, raio = 30 + (quieto ? 0 : (quadro % 3) - 1);
    for (let y = Math.max(0, ty - raio); y < Math.min(QH, ty + raio); y++) for (let x = tx - raio; x < tx + raio; x++) {
      const d2 = ((x - tx) ** 2 + (y - ty) ** 2) / (raio * raio);
      if (d2 < 1 && pontilha(x, y, Math.round((1 - d2) * 6))) px(x, y, 1, 1, "rgba(255,170,90,0.16)");
    }
    px(tx - 1, ty + 2, 3, 5, "#3a2a18");
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
    // os bancos: uma fileira lá atrás, entre as colunas, e a da frente, maior, podre e torta
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
    return { canvas: k, ox, cor: { agua, luz } };
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
    } else {
      // inquieta: a água se mexe em rodas por todo lado; um afogado se ergue entre os bancos; as sanguessugas no raso
      for (let i = 0; i < 9; i++) {
        const cx = ox + 20 + ((i * 37 + Math.floor(q / 4) * 11) % 180), cy = 54 + (i * 5) % 12, rr = 2 + ((q + i * 3) % 6);
        for (let a = 0; a < 10; a++) px(Math.round(cx + Math.cos(a / 10 * Math.PI * 2) * rr), Math.round(cy + Math.sin(a / 10 * Math.PI * 2) * rr * 0.3), 1, 1, "#1f3438");
      }
      // o afogado sobe devagar entre os bancos (uns três segundos, o tempo do texto chegar nele); parado, já de pé
      const sobe = quieto ? 1 : Math.min(1, Math.max(0, (quadro - 12) / 30));
      const ax = ox + 118, ay = Math.round(AGUA_D + 1 - sobe * 9) + (quieto || sobe < 1 ? 0 : Math.round(Math.sin(quadro / 6))), pele = "#2e4038", peleLuz = "#4a5e50";
      c.save(); c.beginPath(); c.rect(0, 0, W, AGUA_D); c.clip();  // o que está embaixo da água não aparece
      px(ax - 5, ay + 3, 12, 8, pele); px(ax - 2, ay - 4, 7, 7, pele); px(ax - 2, ay - 4, 2, 4, peleLuz); px(ax - 5, ay + 3, 2, 3, peleLuz);
      px(ax - 7, ay + 1, 2, 5, pele); px(ax + 7, ay + 1, 2, 5, pele); px(ax - 8, ay, 2, 2, peleLuz); px(ax + 8, ay, 2, 2, pele);
      px(ax - 1, ay - 2, 1, 1, "#c8d8a0"); px(ax + 2, ay - 2, 1, 1, "#c8d8a0");
      c.restore();
      if (sobe > 0) px(ax - 8, AGUA_D, 18, 1, "#2a4448");  // a água aberta em volta do corpo
      // as sanguessugas, no raso, ondulando
      [[ox + 74, 57], [ox + 150, 59]].forEach(([sx, sy], i) => {
        for (let k = 0; k < 8; k++) px(sx + k, sy + Math.round(Math.sin((quieto ? 0 : quadro * 0.6) + k * 0.9 + i)), 1, 2, k === 0 ? "#6a3a40" : k % 2 ? "#3a1c22" : "#4a2a30");
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

  // ================================================================ as cenas e os pontos
  // Cada ponto: a área clicável, onde fica o nome e para onde a câmera vai (no quadro de 320×72).
  const CENAS = {
    ossuario: { base: baseOssuario, desenhar: desenharOssuario,
      pontos: { sarilho: { area: [186, 14, 110, 56], balao: [240, 12], foco: [238, 48] } } },
    exterior: { base: baseExterior, desenhar: desenharExterior,
      pontos: { buraco: { area: [146, 36, 30, 20], balao: [161, 69], foco: [161, 44] },
                sapos: { area: [42, 52, 78, 14], balao: [80, 54], foco: [82, 58] } } },
    salao: { base: baseSalao, desenhar: desenharSalao,
      pontos: { porta: { area: [282, 26, 26, 20], balao: [295, 24], foco: [270, 36] } } },
  };

  // ---------------------------------------------------------------- a cena na página
  function cena(d) {
    const pontos = d.pontos.map((p) => {
      const ativo = !!p.acao || !!p.olhar;
      const rotulo = p.acao ? `${p.nome}: ${p.faz}` : p.olhar ? `${p.nome}: olhar de perto` : `${p.nome}. ${p.estado}`;
      return `<button type="button" class="ci-ponto${ativo ? "" : " parado"}" data-ponto="${h(p.id)}" aria-label="${h(rotulo)}"${ativo ? "" : ' aria-disabled="true" tabindex="-1"'}>
        <span class="ci-balao">${h(p.nome)}</span></button>`;
    }).join("");
    const descricao = d.pontos.map((p) => p.estado).join(" ");
    return `<div class="cena-interativa${d.foco ? " perto" : ""}" data-cena="${h(d.cena)}"${d.correntes ? ` data-correntes="${h(d.correntes)}"` : ""}${d.agua ? ` data-agua="${h(d.agua)}"` : ""}>
      <div class="ci-palco"><canvas class="ci-arte" aria-label="${h(d.titulo)}${descricao ? ": " + h(descricao) : ""}" role="img"></canvas>
      <div class="ci-pontos"${d.foco ? " hidden" : ""}>${pontos}</div>
      <button type="button" class="ci-afastar" hidden>Afastar</button></div></div>`;
  }

  function ligarCena(raiz, d) {
    const def = CENAS[d.cena];
    if (!def) return;
    const el = raiz.querySelector(".cena-interativa"), canvas = el.querySelector(".ci-arte"), palco = el.querySelector(".ci-palco");
    const camadaPontos = el.querySelector(".ci-pontos"), afastar = el.querySelector(".ci-afastar");
    const c = canvas.getContext("2d");
    const est = { correntes: d.correntes, agua: d.agua, soltando: false, passo: 0, onda: 0 };
    let W = QW, b = null, quadro = 0, destaque = null, timer = null, troca = null;
    let cam = d.foco ? focoDe(d.foco) : { x: 0, y: 0, s: 1 };
    const cenaK = document.createElement("canvas"), quadroAtual = document.createElement("canvas");
    function focoDe(id) {
      if (!id) return { x: 0, y: 0, s: 1 };
      const [fx, fy] = def.pontos[id].foco, ox = Math.round((W - QW) / 2);
      return { s: 2, x: Math.max(0, Math.min(W / 2, Math.round(ox + fx - W / 4))), y: Math.max(0, Math.min(QH / 2, Math.round(fy - QH / 4))) };
    }
    // Pixel inteiro: a largura lógica acompanha a página (duas vezes o pixel), e o lugar continua dos lados.
    function medir() {
      const largura = palco.clientWidth;
      if (!largura) return;
      W = Math.max(QW - 40, Math.round(largura / 2));
      b = def.base(W);
      canvas.width = W; canvas.height = QH; cenaK.width = W; cenaK.height = QH; quadroAtual.width = W; quadroAtual.height = QH;
      if (d.foco) cam = focoDe(d.foco);
      const esc = largura / W, ox = Math.round((W - QW) / 2);
      el.querySelectorAll(".ci-ponto").forEach((bt) => {
        const [x, y, w, hh] = def.pontos[bt.dataset.ponto].area, [bx, by] = def.pontos[bt.dataset.ponto].balao;
        Object.assign(bt.style, { left: (ox + x) * esc + "px", top: y * esc + "px", width: w * esc + "px", height: hh * esc + "px" });
        const bal = bt.querySelector(".ci-balao");
        bal.style.left = (bx - x) * esc + "px"; bal.style.top = (by - y) * esc + "px";
      });
      pintar();
    }
    function pintar() {
      if (!b) return;
      const cc = cenaK.getContext("2d");
      cc.imageSmoothingEnabled = false;
      def.desenhar(cc, W, b, est, quadro, destaque);
      const q = quadroAtual.getContext("2d");
      q.imageSmoothingEnabled = false;
      q.clearRect(0, 0, W, QH);
      q.drawImage(cenaK, cam.x, cam.y, W / cam.s, QH / cam.s, 0, 0, W, QH);
      c.imageSmoothingEnabled = false;
      c.clearRect(0, 0, W, QH);
      if (troca) {  // o quadro novo cobre o velho num pontilhado que se fecha, como a câmera da vila
        const n = Math.min(16, Math.ceil(((performance.now() - troca.inicio) / 380) * 16));
        c.drawImage(troca.velho, 0, 0);
        const img = q.getImageData(0, 0, W, QH), velho = c.getImageData(0, 0, W, QH);
        for (let y = 0; y < QH; y++) for (let x = 0; x < W; x++) if (pontilha(x, y, n)) { const i = (y * W + x) * 4; velho.data[i] = img.data[i]; velho.data[i + 1] = img.data[i + 1]; velho.data[i + 2] = img.data[i + 2]; velho.data[i + 3] = 255; }
        c.putImageData(velho, 0, 0);
        if (n >= 16) troca = null;
        return;
      }
      const tranco = est.soltando && est.passo > 3 && est.passo < 22 && !reduzido() ? (est.passo % 2 ? 1 : -1) : 0;
      c.drawImage(quadroAtual, tranco, 0);
    }
    /** A câmera vai até o ponto (ou volta à vista inteira, com `id` nulo), num pontilhado; parada com movimento
     *  reduzido. Enquanto está perto, os pontos saem de cima da arte. */
    function aproximar(id) {
      return new Promise((fim) => {
        const alvo = focoDe(id);
        camadaPontos.hidden = !!id;
        if (reduzido() || (alvo.s === cam.s && alvo.x === cam.x && alvo.y === cam.y)) { cam = alvo; pintar(); fim(); return; }
        const velho = document.createElement("canvas"); velho.width = W; velho.height = QH; velho.getContext("2d").drawImage(canvas, 0, 0);
        troca = { inicio: performance.now(), velho };
        cam = alvo;
        const passo = () => { pintar(); if (troca) requestAnimationFrame(passo); else fim(); };
        requestAnimationFrame(passo);
      });
    }
    // O relógio da cena: dez quadros por segundo (a luz, a água, a corrente descendo); parado com movimento reduzido.
    function relogio() {
      if (!canvas.isConnected) { clearInterval(timer); return; }
      if (document.hidden) return;
      quadro++;
      if (est.soltando) {
        est.passo++;
        if (est.passo >= 27) { est.soltando = false; est.correntes = "soltas"; est.onda = 12; el.dataset.correntes = "soltas"; if (est.fim) { est.fim(); est.fim = null; } }
      } else if (est.onda > 0) est.onda--;
      if (!troca) pintar();
    }
    if (!reduzido()) timer = setInterval(relogio, 100);
    el._soltar = (instantaneo) => new Promise((fim) => {
      if (d.cena !== "ossuario" || est.correntes === "soltas") { fim(); return; }
      if (instantaneo || reduzido()) {  // refazendo a página: sem som; com movimento reduzido, o som fica (não é movimento)
        if (!instantaneo) App.som("corrente");
        est.correntes = "soltas"; el.dataset.correntes = "soltas"; pintar(); fim(); return;
      }
      // O resultado já empurrou a página: a cena volta à vista para a corrente descer, e a leitura desce de novo depois.
      const pg = document.getElementById("pagina"), topo = el.getBoundingClientRect().top - pg.getBoundingClientRect().top;
      const subiu = topo < 0;
      if (subiu) pg.scrollTo({ top: pg.scrollTop + topo - 8, behavior: "smooth" });
      App.som("corrente");
      est.soltando = true; est.passo = 0;
      est.fim = () => {
        if (!subiu) { fim(); return; }
        pg.scrollTo({ top: pg.scrollHeight, behavior: "smooth" });
        setTimeout(() => { pg.scrollTop = pg.scrollHeight; fim(); }, 450);
      };
    });
    // Os pontos: destaque no mouse e no foco. Com ação: o clique (ou Enter/espaço) aproxima a câmera e manda a mesma
    // ação do menu. De olhar: só aproxima, e "Afastar" (ou um clique na arte) volta. Sem nada: diz o estado.
    const longe = () => { afastar.hidden = true; aproximar(null).then(() => { const bt = el.querySelector(".ci-ponto[data-olhado]"); if (bt) { bt.removeAttribute("data-olhado"); bt.focus(); } }); };
    afastar.addEventListener("click", longe);
    canvas.addEventListener("click", () => { if (!afastar.hidden) longe(); });
    el.querySelectorAll(".ci-ponto").forEach((bt) => {
      const p = d.pontos.find((x) => x.id === bt.dataset.ponto);
      const acender = (sim) => { destaque = sim ? p.id : null; bt.classList.toggle("aceso", sim); pintar(); };
      ["mouseenter", "focus"].forEach((t) => bt.addEventListener(t, () => acender(true)));
      ["mouseleave", "blur"].forEach((t) => bt.addEventListener(t, () => acender(false)));
      bt.addEventListener("click", async () => {
        if (p.olhar) {
          App.som("escolha"); bt.setAttribute("data-olhado", "");
          await aproximar(p.id);
          afastar.hidden = false; afastar.focus();
          return;
        }
        if (!p.acao) { App.som("falha"); App.avisar(p.estado, "ponto"); return; }
        const pode = (App.opcoes() || []).some((o) => o.meta && Object.entries(p.acao).every(([k, v]) => o.meta[k] === v));
        if (!pode) { App.som("falha"); App.avisar("Agora não: termine o que está fazendo primeiro.", "ponto"); return; }
        App.som("escolha");
        await aproximar(p.id);
        if (!App.acao(p.acao)) { cam = { x: 0, y: 0, s: 1 }; camadaPontos.hidden = false; pintar(); }
      });
    });
    queueMicrotask(() => { if (typeof recolherArte === "function") recolherArte(true); medir(); });
    // Tela baixa: na página do lugar, se embaixo da cena não cabem as escolhas, a página começa na cena (o nome do lugar
    // segue no painel ao lado). Depois que a paisagem de cima terminou de recolher. Dentro de uma cena, o texto puxa a
    // página até as escolhas, como sempre.
    const naCena = () => {
      const pg = document.getElementById("pagina");
      if (!d.pagina || !pg || !el.isConnected || pg.scrollTop > 0) return;  // e quem rolou, rolou
      const r = el.getBoundingClientRect(), rp = pg.getBoundingClientRect();
      if (rp.bottom - r.bottom < 230 && r.top - rp.top > 12) pg.scrollTop = Math.round(r.top - rp.top - 8);
    };
    setTimeout(naCena, 420); setTimeout(naCena, 1200);  // as escolhas podem chegar depois: só então a página tem altura
    if (typeof ResizeObserver !== "undefined") {
      let largura = 0;
      const obs = new ResizeObserver(() => {
        if (!canvas.isConnected) { obs.disconnect(); return; }
        if (Math.abs(palco.clientWidth - largura) > 1) { largura = palco.clientWidth; medir(); }
      });
      obs.observe(palco);
    }
  }

  /** O motor gravou que as correntes soltaram: a cena à vista mostra a corrente descendo (ou, refazendo a página ou
   *  no instantâneo, já desenha as correntes soltas). */
  function soltarCorrentes(instantaneo) {
    const cenas = document.querySelectorAll('#texto .cena-interativa[data-cena="ossuario"]');
    const el = cenas[cenas.length - 1];
    return el && el._soltar ? el._soltar(instantaneo) : Promise.resolve();
  }

  Telas.registrar("cena", cena, { ligar: ligarCena });
  Object.assign(Telas, { soltarCorrentes });
})();
