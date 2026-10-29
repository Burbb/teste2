/* O interior da taverna (protótipo, candidata A; nada disto entra no jogo): o ambiente da taverna no quadro de cima,
   pelo sistema das cenas (telas/cenas.js), como o templo. A sala vista de frente, um pouco mais de longe que o
   templo: a porta da rua à esquerda, o balcão com o barril e as prateleiras no fundo, as mesas em profundidade, a
   lareira com o caldeirão, a escada para os quartos e, debaixo dela, o canto de Morel.

   As camadas vêm de ferramentas/prototipos/taverna/exportar.py (servidas pela demonstração em /proto-tav/camadas/): o
   fundo, o fogo (4 quadros), as mesas e o balcão da frente, as velas (4) e uma tira por pessoa (taverna.json: a caixa,
   a rotina, a pose parada, a fase). A ordem do desenho: fundo, fogo, os corpos, os móveis da frente, as mãos, as velas
   (ninguém atravessa um tampo). O relógio é o das cenas (100 ms): o fogo e as velas a 200 ms; as pessoas, um passo
   da rotina a cada 200 ms, cada uma com a sua fase. Movimento reduzido: as poses paradas, tudo parado.

   Morel só aparece quando o motor manda `d.morel` (está no canto). Exporta window.CenaTaverna. */
"use strict";

(() => {
  const QW = 320, QH = 96;
  const RAIZ = "/proto-tav/camadas/";
  const im = (n) => { const i = new Image(); i.src = RAIZ + n + ".png"; return i; };
  const IM = { fundo: im("fundo"), fogo: im("fogo"), frente: im("frente"), velas: im("velas") };
  let DADOS = null;
  const GENTE = {};
  fetch(RAIZ + "taverna.json").then((r) => r.json()).then((j) => {
    DADOS = j.gente;
    Object.keys(DADOS).forEach((n) => { GENTE[n] = im("gente/" + n); });
  }).catch(() => {});
  const pronta = (i) => i && i.complete && i.naturalWidth > 0;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches
    || document.body.dataset.tavReduzido === "1";  // a faixa da demonstração liga a pose parada

  /** O desenho de uma pessoa no tique q (a rotina dela a 200 ms, a partir da fase; parado: a pose parada). */
  function poseDe(nome, q) {
    const p = DADOS && DADOS[nome];
    if (!p) return 0;
    if (reduzido()) return p.parada;
    const n = p.tempo.length, i = Math.floor(q / 2) + p.fase;
    return p.tempo[((i % n) + n) % n];
  }

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
  const tira = (c, i, n) => { if (pronta(i)) c.drawImage(i, n * QW, 0, QW, QH, 0, 0, QW, QH); };
  /** Quem está na sala agora: todos, e Morel só quando o motor diz que ele está no canto. */
  const presentes = (d) => (DADOS ? Object.keys(DADOS).filter((n) => !DADOS[n].so_com || (d && d[DADOS[n].so_com])) : []);
  function gente(c, d, q, linha) {
    presentes(d).forEach((n) => {
      const p = DADOS[n], i = GENTE[n];
      if (!pronta(i)) return;
      c.drawImage(i, poseDe(n, q) * p.w, linha * p.h, p.w, p.h, p.x, p.y, p.w, p.h);
    });
  }
  function desenhar(c, W, b, est, quadro) {
    encher(b);
    const quieto = reduzido(), d = b.d;
    c.imageSmoothingEnabled = false;
    c.clearRect(0, 0, QW, QH);
    if (pronta(IM.fundo)) c.drawImage(IM.fundo, 0, 0);
    tira(c, IM.fogo, quieto ? 1 : Math.floor(quadro / 2) % 4);
    gente(c, d, quadro, 0);
    if (pronta(IM.frente)) c.drawImage(IM.frente, 0, 0);
    gente(c, d, quadro, 1);
    tira(c, IM.velas, quieto ? 1 : Math.floor(quadro / 2) % 4);
  }

  // Os nomes em cima de cada ponto, fora das cabeças e das mãos: o do Taverneiro na prateleira de baixo, acima da
  // cabeça dele; o da Escada no alto dela (os degraus de cima e a galeria: os de baixo ficam sobre o canto de Morel);
  // o da Despensa no piso, embaixo do alçapão (em cima, cobria a cabeça de quem come à esquerda); o do Homem do canto
  // acima da cabeça dele; o da Saída na porta.
  const PONTOS = {
    taverneiro: { area: [96, 26, 26, 16], balao: [108, 27], foco: [108, 36] },
    escada: { area: [276, 8, 40, 24], balao: [296, 10], foco: [290, 22] },
    despensa: { area: [102, 58, 20, 7], balao: [114, 74], foco: [112, 61] },
    morel: { area: [278, 34, 20, 14], balao: [287, 28], foco: [287, 42] },
    saida: { area: [10, 18, 24, 40], balao: [21, 14], foco: [21, 44] },
  };

  window.CenaTaverna = { base, desenhar, pontos: PONTOS, poseDe, presentes, QW, QH };
})();
