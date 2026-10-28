/* A cabana da curandeira do Vau, candidata A (protótipo: só a demonstração carrega este arquivo). O quadro de cima pelo
   sistema das cenas (telas/cenas.js), como a forja: 320×96, a vista crescendo na proporção.

   A arte vem pronta em camadas (ferramentas/prototipos/curandeira/camadas, exportadas por exportar.py): o fundo, o
   fogo (4 quadros), o vapor (4 quadros, o forte na noite da água escura), os baldes (a mesma noite), quem atende (Pita
   ou Marta, um quadro por pose do giro do pilão) e a frente. Quem atende e a água vêm do motor (o painel "cena":
   d.quem, d.agua); aqui só se escolhe o quadro de cada camada pelo relógio das cenas (100 ms).

   O ritmo: o pilão gira devagar (2 tiques por pose, 1,6 s por volta), três voltas e uma pausa de 1,2 s com a mão
   parada; nada da martelada da forja. Movimento reduzido (ou o botão da faixa): a pose parada, o fogo e o vapor parados.

   Exporta window.CenaCurandeira = { base, desenhar, pontos, poseDe, DURACAO, QW, QH }. */
"use strict";

(() => {
  const QW = 320, QH = 96, POSES = 8, TIQUES = 2, VOLTAS = 3, PAUSA = 12;
  const DURACAO = POSES * TIQUES * VOLTAS + PAUSA;
  const IM = {};
  ["fundo", "fogo", "vapor", "vapor-forte", "baldes", "pita", "marta", "frente"].forEach((n) => {
    const i = new Image(); i.src = `/proto-cur/camadas/${n}.png`; IM[n] = i;
  });
  const pronta = (i) => i.complete && i.naturalWidth > 0;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches || document.body.dataset.curReduzido === "1";

  /** A pose do quadro: a do giro, ou a parada (0) na pausa. */
  function poseDe(q) {
    const r = ((q % DURACAO) + DURACAO) % DURACAO;
    return r < POSES * TIQUES * VOLTAS ? Math.floor(r / TIQUES) % POSES : 0;
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
  const tira = (c, im, i) => { if (pronta(im)) c.drawImage(im, i * QW, 0, QW, QH, 0, 0, QW, QH); };
  function desenhar(c, W, b, est, quadro) {
    encher(b);
    const quieto = reduzido(), d = b.d || {}, escura = d.agua === "escura";
    c.imageSmoothingEnabled = false;
    c.clearRect(0, 0, QW, QH);
    if (pronta(IM.fundo)) c.drawImage(IM.fundo, 0, 0);
    const passo = quieto ? 1 : Math.floor(quadro / 2) % 4;
    tira(c, IM.fogo, passo);
    if (escura && pronta(IM.baldes)) c.drawImage(IM.baldes, 0, 0);
    tira(c, escura ? IM["vapor-forte"] : IM.vapor, passo);
    tira(c, d.quem === "marta" ? IM.marta : IM.pita, quieto ? 0 : poseDe(quadro));
    if (pronta(IM.frente)) c.drawImage(IM.frente, 0, 0);
  }

  // O nome de quem atende na parede à direita dela (embaixo das prateleiras: não cobre a cabeça, as mãos nem o
  // almofariz); o da Saída na porta.
  const PONTOS = {
    curandeira: { area: [146, 28, 30, 54], balao: [190, 52], foco: [160, 50] },
    saida: { area: [10, 10, 30, 64], balao: [25, 30], foco: [25, 44] },
  };

  window.CenaCurandeira = { base, desenhar, pontos: PONTOS, poseDe, DURACAO, QW, QH };
})();
