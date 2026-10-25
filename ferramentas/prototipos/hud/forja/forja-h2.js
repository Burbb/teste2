/* A forja do Vau, H2: a H com o olho ajustado (um pixel mais para trás, a órbita entre a ponte do nariz e o olho); a H: a G com o ferreiro redesenhado no estilo das figuras do jogo (o mercador, a Ilse: três tons
   chapados, sem contorno) e animado com o corpo inteiro (os joelhos dobram, o quadril desce, o tronco inclina, a barriga
   achata, a trança balança; os pés e a mão na tenaz parados), na oficina da G (protótipo, 25/10/2026; nada no jogo).

   A arte vem pronta em camadas (h2/camadas/, exportadas de h2/aseprite/forja-h2.aseprite pelo exportar_h2.py): o fundo,
   o fogo (4 quadros), a bigorna, a espada e o ferreiro com a tenaz (um quadro por estado), o primeiro plano. Aqui só se
   escolhe o quadro de cada uma pelo relógio das cenas e se desenham as faíscas. O ritmo é o da R, sem mudança: 100 ms
   por quadro, 53 quadros, quatro golpes (o alto segurado variando, a descida num quadro, o golpe, o rebote, o
   repouso) e a pausa em que a tenaz vira a espada. Movimento reduzido: a pose do alto, parada, o fogo parado.

   Exporta window.ForjaArte.h2 = { base, desenhar, pontos, poseDe, CICLO, DURACAO, ESTADOS, QW, QH }. */
"use strict";

(() => {
  const QW = 320, QH = 96;
  const RAIZ = (document.currentScript && document.currentScript.src.replace(/[^/]*$/, "")) || "";
  const ESTADOS = ["repouso", "sobe1", "sobe2", "alto", "desce", "golpe", "volta", "ajuste", "ajuste_virada"];
  const IM = {};
  ["fundo", "bigorna", "frente", "fogo", "espada", "ferreiro"].forEach((n) => { const i = new Image(); i.src = `${RAIZ}h2/camadas/${n}.png`; IM[n] = i; });
  const pronta = (i) => i.complete && i.naturalWidth > 0;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;

  // A linha do tempo da R (o ritmo aprovado), quadro a quadro de 100 ms. O último quadro emenda no primeiro.
  const GOLPE = (alto, repouso) => [["sobe1", 1], ["sobe2", 1], ["alto", alto], ["desce", 1], ["golpe", 1], ["volta", 1], ["repouso", repouso]];
  const CICLO = [["repouso", 3], ...GOLPE(3, 2), ...GOLPE(2, 2), ...GOLPE(3, 1), ...GOLPE(4, 3), ["ajuste", 6], ["repouso", 4]];
  const DURACAO = CICLO.reduce((n, [, d]) => n + d, 0);
  function poseDe(q) {
    let r = ((q % DURACAO) + DURACAO) % DURACAO, golpes = 0;
    for (const [nome, d] of CICLO) {
      if (r < d) return { nome, t: r, golpe: golpes, volta: Math.floor(q / DURACAO) };
      if (nome === "golpe") golpes++;
      r -= d;
    }
    return { nome: "repouso", t: 0, golpe: 0, volta: 0 };
  }
  /** O quadro das tiras (espada e ferreiro): a pausa com a espada virada tem o dela. */
  const estadoDe = (p) => ESTADOS.indexOf(p.nome === "ajuste" && p.t >= 1 && p.t < 5 ? "ajuste_virada" : p.nome);

  // ---------------------------------------------------------------- as faíscas (a mesma conta da R e de cena_f.py)
  const CONTATO = [141, 58];
  const FOGO = ["#3f1006", "#7a240a", "#b8400f", "#e86a18", "#ff9a30", "#ffcc66", "#fff2c4"];
  function faiscas(c, semente, idade) {
    const px = (x, y, cor) => { c.fillStyle = cor; c.fillRect(Math.round(x), Math.round(y), 1, 1); };
    let s = (semente * 9301 + 49297) % 233280 || 7;
    const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
    const [x, y] = CONTATO;
    for (let i = 0; i < 9; i++) {
      const ang = Math.PI * (1.05 + rnd() * 0.9), vel = 2.5 + rnd() * 4.5, sobe = -1.2 - rnd() * 1.5;
      const d = idade * vel + 1.5, lado = rnd() < 0.5 ? 1 : -0.6;
      const qx = x + Math.cos(ang) * d * lado, qy = y + Math.sin(ang) * d * 0.55 + idade * idade * 0.8 + sobe * (idade > 0 ? 0.5 : 0);
      if (idade === 2 && i % 2) continue;
      px(qx, qy, idade === 0 ? FOGO[6] : idade === 1 ? FOGO[5] : FOGO[4]);
      if (idade > 0) px(qx + (qx > x ? -1 : 1), qy + 0.5, idade === 1 ? FOGO[4] : FOGO[3]);
    }
    if (idade === 0) { px(x - 1, y - 1, FOGO[6]); px(x, y - 1, FOGO[6]); px(x + 1, y - 1, FOGO[6]); px(x, y - 2, FOGO[6]); }
  }

  // ---------------------------------------------------------------- a base e o quadro
  /** A base é o fundo (o que a vista lê para a cor do chão que continua embaixo da arte). */
  function base(W, d) {
    const k = document.createElement("canvas"); k.width = QW; k.height = QH;
    const b = { canvas: k, ox: 0, d, cheia: false };
    encher(b);
    return b;
  }
  function encher(b) {
    if (b.cheia || !pronta(IM.fundo)) return;
    b.canvas.getContext("2d").drawImage(IM.fundo, 0, 0); b.cheia = true;
  }
  const tira = (c, im, i) => { if (pronta(im)) c.drawImage(im, i * QW, 0, QW, QH, 0, 0, QW, QH); };
  function desenhar(c, W, b, est, quadro, destaque) {
    encher(b);
    const quieto = reduzido();
    c.imageSmoothingEnabled = false;
    c.clearRect(0, 0, QW, QH);
    if (pronta(IM.fundo)) c.drawImage(IM.fundo, 0, 0);
    tira(c, IM.fogo, quieto ? 1 : Math.floor(quadro / 2) % 4);
    if (pronta(IM.bigorna)) c.drawImage(IM.bigorna, 0, 0);
    const p = quieto ? { nome: "alto", t: 0, golpe: 0, volta: 0 } : poseDe(quadro);
    const e = estadoDe(p);
    tira(c, IM.espada, e);
    tira(c, IM.ferreiro, e);
    if (!quieto) {
      const n = p.golpe + p.volta * 4;
      if (p.nome === "golpe") faiscas(c, n, 0);
      else if (p.nome === "volta") faiscas(c, n - 1, 1);
      else if (p.nome === "repouso" && p.t === 0 && p.golpe > 0) faiscas(c, n - 1, 2);  // logo depois do rebote
    }
    if (pronta(IM.frente)) c.drawImage(IM.frente, 0, 0);
  }

  // ---------------------------------------------------------------- os pontos
  // O nome do Ferreiro na parede à direita dele (sobre o suporte de ferramentas: não cobre a cabeça, a barba, o
  // martelo nem a espada); o da Saída na porta. As áreas ficam acima da linha 72 (o contorno das cenas para ali).
  const PONTOS = {
    ferreiro: { area: [144, 14, 48, 58], balao: [199, 47], foco: [166, 50] },
    saida: { area: [12, 12, 28, 58], balao: [26, 30], foco: [26, 44] },
  };

  window.ForjaArte = window.ForjaArte || {};
  window.ForjaArte.h2 = { base, desenhar, pontos: PONTOS, poseDe, CICLO, DURACAO, ESTADOS, QW, QH, imagens: IM };
})();
