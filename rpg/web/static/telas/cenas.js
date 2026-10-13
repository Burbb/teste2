/* Cenas interativas: um lugar desenhado em pixel art (como as paisagens: escala inteira, pontilhado de Bayer, dez
   quadros por segundo) com pontos clicáveis por cima. A primeira é o ossuário da capela, com o sarilho
   (roadmapIDEIAS/20). O motor diz o estado (as correntes presas ou soltas) e o que cada ponto faz (a mesma ação do
   menu); clicar aproxima a câmera e manda a ação; a tela não decide nada. A corrente desce na tela só quando o motor
   avisa que o preparo foi gravado (celebrar "correntes"). */
"use strict";

(() => {
  const { h } = Telas;
  const QW = 320, QH = 72;  // o quadro desenhado (o tamanho das paisagens); a tela pode ser mais larga: as paredes continuam
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const pontilha = (x, y, n) => Sprites.pontilha(x, y, n);

  // ---------------------------------------------------------------- o ossuário
  const COR = {
    abobada: "#101317", parede: "#1c2026", junta: "#14171b", pedra: "#2a2f36", pedraLuz: "#3d444d", nicho: "#0b0d10",
    osso: "#c8c0a8", ossoSombra: "#8a8270", chao: "#23272d", chaoJunta: "#181b1f",
    madeira: "#2a2018", madeiraLuz: "#4a3a2a", madeiraEsc: "#120e0a", ferro: "#4a4c54", ferroLuz: "#9a9ca6",
    agua: "#05080a", aguaLuz: "#1f3034", ouro: "#ffd070",
  };
  const PISO = 56;
  const SAR = { x: 196, y: 22 };                   // o canto de cima do sarilho (postes, trave, tambor)
  const BURACO = { x: 240, y: 64, rx: 19, ry: 4 }; // o buraco no chão, com a água parada lá embaixo
  const PONTOS = { sarilho: { area: [186, 14, 110, 56], balao: [240, 12], foco: [238, 48] } };

  function base(W) {
    const k = document.createElement("canvas"); k.width = W; k.height = QH;
    const c = k.getContext("2d"), ox = Math.round((W - QW) / 2);
    const px = (x, y, w = 1, hh = 1, cor) => { c.fillStyle = cor; c.fillRect(Math.round(x), Math.round(y), w, hh); };
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
    // a escada do alçapão, à esquerda, com a luz que desce de cima
    for (let d = 0; d < 9; d++) { const x = ox + 4 + d * 4, y = 10 + d * 5; px(x, y, 30 - d * 3, 2, COR.pedraLuz); px(x, y + 2, 30 - d * 3, PISO - y - 2, COR.pedra); }
    for (let y = 0; y < 36; y++) for (let x = ox + 4; x < ox + 28; x++) if (pontilha(x, y, Math.max(0, 3 - Math.floor(y / 12)))) px(x, y, 1, 1, "#4a4a44");
    // o chão, com os ossos dos que caíram
    for (let y = PISO; y < QH; y++) px(0, y, W, 1, y === PISO ? COR.pedraLuz : COR.chao);
    for (let y = PISO + 3; y < QH; y += 5) for (let x = (y * 3) % 10; x < W; x += 14) px(x, y, 9, 1, COR.chaoJunta);
    [[ox + 66, 64], [ox + 90, 68], [ox + 118, 62], [ox + 150, 66]].forEach(([x, y], i) => {
      px(x, y, 9, 1, COR.osso); px(x + (i % 2 ? 8 : 0), y - 1, 2, 2, COR.osso);
      if (i === 1) { px(x + 12, y - 4, 5, 4, COR.osso); px(x + 13, y - 3, 1, 1, COR.nicho); px(x + 15, y - 3, 1, 1, COR.nicho); }
    });
    // o buraco no chão: a borda de pedra e a água escura lá embaixo
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
    const px = (x, y, w = 1, hh = 1, cor) => { c.fillStyle = cor; c.fillRect(Math.round(x), Math.round(y), w, hh); };
    c.drawImage(b.canvas, 0, 0);
    const ox = b.ox, quieto = reduzido();
    // a tocha na parede, perto da escada, com a luz que treme
    const tx = ox + 44, ty = 22, raio = 30 + (quieto ? 0 : (quadro % 3) - 1);
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

  // ---------------------------------------------------------------- a cena na página
  function cena(d) {
    const pontos = d.pontos.map((p) => {
      const ativo = !!p.acao;
      const rotulo = ativo ? `${p.nome}: ver como soltar as correntes` : `${p.nome}. ${p.estado}`;
      return `<button type="button" class="ci-ponto${ativo ? "" : " parado"}" data-ponto="${h(p.id)}" aria-label="${h(rotulo)}"${ativo ? "" : ' aria-disabled="true" tabindex="-1"'}>
        <span class="ci-balao">${h(p.nome)}</span></button>`;
    }).join("");
    return `<div class="cena-interativa${d.foco ? " perto" : ""}" data-cena="${h(d.cena)}" data-correntes="${h(d.correntes)}">
      <div class="ci-palco"><canvas class="ci-arte" aria-label="${h(d.titulo)}: ${h(d.pontos.map((p) => p.estado).join(" "))}" role="img"></canvas>
      <div class="ci-pontos"${d.foco ? " hidden" : ""}>${pontos}</div></div></div>`;
  }

  function ligarCena(raiz, d) {
    const el = raiz.querySelector(".cena-interativa"), canvas = el.querySelector(".ci-arte"), palco = el.querySelector(".ci-palco");
    const c = canvas.getContext("2d");
    const est = { correntes: d.correntes, soltando: false, passo: 0, onda: 0 };
    let W = QW, b = null, quadro = 0, destaque = null, timer = null, troca = null;
    let cam = d.foco ? focoDe(d.foco) : { x: 0, y: 0, s: 1 };
    const cena = document.createElement("canvas"), quadroAtual = document.createElement("canvas");
    function focoDe(id) {
      const [fx, fy] = PONTOS[id].foco, ox = Math.round((W - QW) / 2);
      return { s: 2, x: Math.max(0, Math.min(W / 2, Math.round(ox + fx - W / 4))), y: Math.max(0, Math.min(QH / 2, Math.round(fy - QH / 4))) };
    }
    // Pixel inteiro: a largura lógica acompanha a página (duas vezes o pixel), e as paredes continuam dos lados.
    function medir() {
      const largura = palco.clientWidth;
      if (!largura) return;
      W = Math.max(QW - 40, Math.round(largura / 2));
      b = base(W);
      canvas.width = W; canvas.height = QH; cena.width = W; cena.height = QH; quadroAtual.width = W; quadroAtual.height = QH;
      if (d.foco) cam = focoDe(d.foco);
      const esc = largura / W, ox = Math.round((W - QW) / 2);
      el.querySelectorAll(".ci-ponto").forEach((bt) => {
        const [x, y, w, hh] = PONTOS[bt.dataset.ponto].area, [bx, by] = PONTOS[bt.dataset.ponto].balao;
        Object.assign(bt.style, { left: (ox + x) * esc + "px", top: y * esc + "px", width: w * esc + "px", height: hh * esc + "px" });
        const bal = bt.querySelector(".ci-balao");
        bal.style.left = (bx - x) * esc + "px"; bal.style.top = (by - y) * esc + "px";
      });
      pintar();
    }
    function pintar() {
      if (!b) return;
      const cc = cena.getContext("2d");
      cc.imageSmoothingEnabled = false;
      desenharOssuario(cc, W, b, est, quadro, destaque);
      const q = quadroAtual.getContext("2d");
      q.imageSmoothingEnabled = false;
      q.clearRect(0, 0, W, QH);
      q.drawImage(cena, cam.x, cam.y, W / cam.s, QH / cam.s, 0, 0, W, QH);
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
    function aproximar(id) {
      return new Promise((fim) => {
        const alvo = focoDe(id);
        if (reduzido() || (alvo.s === cam.s && alvo.x === cam.x && alvo.y === cam.y)) { cam = alvo; pintar(); fim(); return; }
        const velho = document.createElement("canvas"); velho.width = W; velho.height = QH; velho.getContext("2d").drawImage(canvas, 0, 0);
        troca = { inicio: performance.now(), velho };
        cam = alvo;
        el.querySelector(".ci-pontos").hidden = true;
        const passo = () => { pintar(); if (troca) requestAnimationFrame(passo); else fim(); };
        requestAnimationFrame(passo);
      });
    }
    // O relógio da cena: dez quadros por segundo (a tocha, a água, a corrente descendo); parado com movimento reduzido.
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
      if (est.correntes === "soltas") { fim(); return; }
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
    // Os pontos: destaque no mouse e no foco; o clique (ou Enter/espaço) aproxima a câmera e manda a ação do menu.
    el.querySelectorAll(".ci-ponto").forEach((bt) => {
      const p = d.pontos.find((x) => x.id === bt.dataset.ponto);
      const acender = (sim) => { destaque = sim ? p.id : null; bt.classList.toggle("aceso", sim); pintar(); };
      ["mouseenter", "focus"].forEach((t) => bt.addEventListener(t, () => acender(true)));
      ["mouseleave", "blur"].forEach((t) => bt.addEventListener(t, () => acender(false)));
      bt.addEventListener("click", async () => {
        if (!p.acao) { App.som("falha"); App.avisar(p.estado, "ponto"); return; }
        const pode = (App.opcoes() || []).some((o) => o.meta && Object.entries(p.acao).every(([k, v]) => o.meta[k] === v));
        if (!pode) { App.som("falha"); App.avisar("Agora não: termine o que está fazendo primeiro.", "ponto"); return; }
        App.som("escolha");
        await aproximar(p.id);
        if (!App.acao(p.acao)) { cam = { x: 0, y: 0, s: 1 }; el.querySelector(".ci-pontos").hidden = false; pintar(); }
      });
    });
    queueMicrotask(() => { if (typeof recolherArte === "function") recolherArte(true); medir(); });
    // Tela baixa: se embaixo da cena não cabem as escolhas, a página começa na cena (o nome do lugar segue no painel ao
    // lado). Depois que a paisagem de cima terminou de recolher.
    const naCena = () => {
      const pg = document.getElementById("pagina");
      if (d.foco || !pg || !el.isConnected || pg.scrollTop > 0) return;  // de perto, o texto puxa a página; e quem rolou, rolou
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
