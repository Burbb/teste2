/* A cabana da curandeira do Vau: o ambiente da curandeira (o quadro de cima, pelo sistema das cenas, telas/cenas.js),
   desde a 1.218.0. A cabana de trabalho vista de frente: a porta fria e a pia à esquerda, as ervas secando na vara, a
   bancada com o alambique e o almofariz, quem atende na ponta dela, as prateleiras da botica, o fogão com o caldeirão,
   a cortina do quarto dos fundos e o armário. O quadro é o da forja (320×96).

   A arte vem pronta em camadas (static/cenas/curandeira/), exportadas da fonte em
   ferramentas/prototipos/curandeira/aseprite/curandeira.aseprite (fonte.py --jogo): o fundo, o fogo (4 quadros), o
   vapor (4 quadros; o forte na noite da água escura), os baldes (a mesma noite), quem atende (Pita, de pé no banquinho,
   ou Marta: um quadro por desenho da rotina) e a frente. Quem atende e a água vêm do motor (o painel "cena": d.quem,
   d.agua); aqui só se escolhe o quadro de cada camada pelo relógio das cenas (100 ms).

   A rotina (moer em voltas de poses sustentadas, desacelerar, olhar a mistura, levar uma pitada ao nariz, pegar o pilão
   de novo) vem de rotina.json, gerado com a arte: para cada uma, o quadro de cada tique (`tempo`) e a pose do movimento
   reduzido (`parada`: inclinada sobre o almofariz). Movimento reduzido: a pose parada, o fogo e o vapor parados.

   Exporta window.CenaCurandeira = { base, desenhar, pontos, poseDe, QW, QH }: cenas.js a registra como a cena
   "curandeira". */
"use strict";

(() => {
  const QW = 320, QH = 96;
  const IM = {};
  ["fundo", "fogo", "vapor", "vapor-forte", "baldes", "pita", "marta", "frente"].forEach((n) => {
    const i = new Image(); i.src = `/static/cenas/curandeira/${n}.png`; IM[n] = i;
  });
  let ROTINA = null;
  fetch("/static/cenas/curandeira/rotina.json").then((r) => r.json()).then((j) => { ROTINA = j; }).catch(() => {});
  const pronta = (i) => i.complete && i.naturalWidth > 0;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;

  /** O quadro de quem atende no tique q (o da rotina; antes de ela chegar, a pose parada). */
  function poseDe(q, quem) {
    const rot = ROTINA && ROTINA[quem];
    if (!rot) return 0;
    const n = rot.tempo.length;
    return rot.tempo[((q % n) + n) % n];
  }
  const parada = (quem) => (ROTINA && ROTINA[quem] ? ROTINA[quem].parada : 0);

  /** A base é o fundo (a troca de cena parte dela). */
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
  function desenhar(c, W, b, est, quadro) {
    encher(b);
    const quieto = reduzido(), d = b.d || {}, escura = d.agua === "escura";
    const quem = d.quem === "marta" ? "marta" : "pita";
    c.imageSmoothingEnabled = false;
    c.clearRect(0, 0, QW, QH);
    if (pronta(IM.fundo)) c.drawImage(IM.fundo, 0, 0);
    const passo = quieto ? 1 : Math.floor(quadro / 2) % 4;
    tira(c, IM.fogo, passo);
    if (escura && pronta(IM.baldes)) c.drawImage(IM.baldes, 0, 0);
    tira(c, escura ? IM["vapor-forte"] : IM.vapor, passo);
    tira(c, IM[quem], quieto ? parada(quem) : poseDe(quadro, quem));
    if (pronta(IM.frente)) c.drawImage(IM.frente, 0, 0);
  }

  // O nome de quem atende na parede à direita dela (embaixo das prateleiras: não cobre a cabeça, as mãos nem o
  // almofariz); o da Saída na porta.
  const PONTOS = {
    curandeira: { area: [146, 28, 30, 54], balao: [190, 52], foco: [160, 50] },
    saida: { area: [10, 10, 30, 64], balao: [25, 30], foco: [25, 44] },
  };

  window.CenaCurandeira = { base, desenhar, pontos: PONTOS, poseDe, QW, QH };
})();
