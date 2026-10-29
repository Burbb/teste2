/* O interior do templo: o ambiente do templo (o quadro de cima, pelo sistema das cenas, telas/cenas.js), desde a
   1.219.0. A nave vista de frente: o arco de pedra sobre os dois pilares, o presbitério com o altar e a janela alta, os
   bancos dos dois lados do corredor, a porta da rua à esquerda, o atendimento à direita (a mesa dos panos, o armário, a
   porta lateral, o fogareiro do incenso), e o clérigo dobrando os panos na mesa. O quadro é o da forja (320×96).

   A arte vem pronta em camadas (static/cenas/templo/), exportadas da fonte em
   ferramentas/prototipos/templo/aseprite/templo.aseprite (fonte.py --jogo): o fundo, as velas (4 quadros), o incenso
   (8) e o clérigo (um quadro por desenho da rotina, rotina.json: pegar o pano, erguer, sacudir, dobrar, assentar,
   alisar; a cada dois panos, as mãos na beira da mesa e o olhar para a nave). O relógio é o das cenas (100 ms): as
   velas e o incenso a 200 ms; o clérigo, pela rotina. Movimento reduzido: a pose parada, tudo parado.

   A cena entra pelo vila.js (estado.local.interiores, do motor) diante do prédio. Exporta window.CenaTemplo. */
"use strict";

(() => {
  const QW = 320, QH = 96;
  const IM = {};
  ["fundo", "velas", "fumaca", "clerigo"].forEach((n) => { const i = new Image(); i.src = `/static/cenas/templo/${n}.png`; IM[n] = i; });
  let ROTINA = null;
  fetch("/static/cenas/templo/rotina.json").then((r) => r.json()).then((j) => { ROTINA = j; }).catch(() => {});
  const pronta = (i) => i.complete && i.naturalWidth > 0;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;

  /** O quadro do clérigo no tique q (o da rotina; antes de ela chegar e no movimento reduzido, a pose parada). */
  function poseDe(q) {
    if (!ROTINA) return 0;
    if (reduzido()) return ROTINA.parada;
    const n = ROTINA.tempo.length;
    return ROTINA.tempo[((q % n) + n) % n];
  }

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
    const quieto = reduzido();
    c.imageSmoothingEnabled = false;
    c.clearRect(0, 0, QW, QH);
    if (pronta(IM.fundo)) c.drawImage(IM.fundo, 0, 0);
    tira(c, IM.velas, quieto ? 1 : Math.floor(quadro / 2) % 4);
    tira(c, IM.fumaca, quieto ? 0 : Math.floor(quadro / 2) % 8);
    tira(c, IM.clerigo, poseDe(quadro));
  }

  // O nome do Clérigo na parede acima dele (fora das mãos e do pano); o da Saída na porta da rua.
  const PONTOS = {
    clerigo: { area: [210, 36, 26, 34], balao: [212, 24], foco: [222, 54] },
    saida: { area: [12, 24, 24, 46], balao: [23, 22], foco: [23, 50] },
  };

  window.CenaTemplo = { base, desenhar, pontos: PONTOS, poseDe, QW, QH };
})();
