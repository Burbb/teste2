/* O interior do templo do Vau (protótipo: só a demonstração carrega este arquivo), as duas candidatas: A (a nave de
   lado, o canto de atendimento entre os bancos e o presbitério) e B (a nave de frente, da composição da referência do
   Jean). O quadro de cima pelo sistema das cenas (telas/cenas.js), como a forja e a curandeira: 320×96.

   A arte vem pronta em camadas (camadas/a, camadas/b, exportadas por exportar.py): o fundo, as velas (4 quadros), o
   incenso (8), o pó nos feixes de luz (8, só na A), o clérigo (um quadro por desenho da rotina, rotina.json) e a frente.
   O relógio é o das cenas (100 ms): as velas a 200 ms, o incenso a 200 ms, o pó a 300 ms; o clérigo, pela rotina.
   Movimento reduzido (ou "Pose parada" na faixa): a pose parada, tudo parado.

   A candidata vem de document.body.dataset.tplCand ("a" ou "b"; a faixa troca). Exporta window.CenaTemplo. */
"use strict";

(() => {
  const QW = 320, QH = 96;
  const IM = { a: {}, b: {} };
  for (const c of ["a", "b"]) {
    ["fundo", "velas", "fumaca", "poeira", "clerigo", "frente"].forEach((n) => {
      if (c === "b" && n === "poeira") return;
      const i = new Image(); i.src = `/proto-tpl/camadas/${c}/${n}.png`; IM[c][n] = i;
    });
  }
  let ROTINA = null;
  fetch("/proto-tpl/camadas/rotina.json").then((r) => r.json()).then((j) => { ROTINA = j; }).catch(() => {});
  const pronta = (i) => i && i.complete && i.naturalWidth > 0;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches || document.body.dataset.tplReduzido === "1";
  const cand = () => (document.body.dataset.tplCand === "b" ? "b" : "a");

  function poseDe(q, c) {
    const rot = ROTINA && ROTINA[c];
    if (!rot) return 0;
    if (reduzido()) return rot.parada;
    const n = rot.tempo.length;
    return rot.tempo[((q % n) + n) % n];
  }

  function base(W, d) {
    const k = document.createElement("canvas"); k.width = QW; k.height = QH;
    const b = { canvas: k, ox: 0, d, cheia: null };
    encher(b);
    return b;
  }
  function encher(b) {
    const c = cand();
    if (b.cheia === c || !pronta(IM[c].fundo)) return;
    const x = b.canvas.getContext("2d"); x.clearRect(0, 0, QW, QH); x.drawImage(IM[c].fundo, 0, 0); b.cheia = c;
  }
  const tira = (c, im, i) => { if (pronta(im)) c.drawImage(im, i * QW, 0, QW, QH, 0, 0, QW, QH); };
  function desenhar(c, W, b, est, quadro) {
    encher(b);
    const quieto = reduzido(), A = IM[cand()];
    c.imageSmoothingEnabled = false;
    c.clearRect(0, 0, QW, QH);
    if (pronta(A.fundo)) c.drawImage(A.fundo, 0, 0);
    tira(c, A.poeira, quieto ? 0 : Math.floor(quadro / 3) % 8);
    tira(c, A.velas, quieto ? 1 : Math.floor(quadro / 2) % 4);
    tira(c, A.fumaca, quieto ? 0 : Math.floor(quadro / 2) % 8);
    tira(c, A.clerigo, poseDe(quadro, cand()));
    if (pronta(A.frente)) c.drawImage(A.frente, 0, 0);
  }

  // Os pontos de cada candidata: o clérigo (leva aos cartões do balcão) e a Saída (a porta da rua). Os nomes ficam na
  // parede, fora do clérigo e das mãos dele.
  const PONTOS = {
    a: { clerigo: { area: [214, 40, 26, 46], balao: [196, 38], foco: [222, 60] },
         saida: { area: [6, 20, 32, 52], balao: [22, 30], foco: [22, 48] } },
    b: { clerigo: { area: [210, 36, 26, 34], balao: [212, 24], foco: [222, 54] },
         saida: { area: [12, 24, 24, 46], balao: [23, 22], foco: [23, 50] } },
  };
  const pontos = new Proxy({}, { get: (_, id) => PONTOS[cand()][id] });

  window.CenaTemplo = { base, desenhar, pontos, poseDe, QW, QH };
})();
