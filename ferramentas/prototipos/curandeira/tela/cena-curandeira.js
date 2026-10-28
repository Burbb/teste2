/* A cabana da curandeira do Vau, candidata A (protótipo: só a demonstração carrega este arquivo). O quadro de cima pelo
   sistema das cenas (telas/cenas.js), como a forja: 320×96, a vista crescendo na proporção.

   A arte vem pronta em camadas (ferramentas/prototipos/curandeira/camadas, exportadas por exportar.py): o fundo, o
   fogo (4 quadros), o vapor (4 quadros, o forte na noite da água escura), os baldes (a mesma noite), quem atende (Pita
   ou Marta, um quadro por desenho diferente da rotina) e a frente. Quem atende e a água vêm do motor (o painel "cena":
   d.quem, d.agua); aqui só se escolhe o quadro de cada camada pelo relógio das cenas (100 ms).

   A rotina (moer, desacelerar, olhar a mistura, a pitada no nariz, pegar o pilão de novo) vem de figuras.py, em
   camadas/rotina.json: para cada uma, o quadro de cada tique (`tempo`) e a pose do movimento reduzido (`parada`).
   Movimento reduzido (ou o botão da faixa): a pose parada, o fogo e o vapor parados.

   A faixa pode mostrar a passada anterior (anterior/camadas: o giro do braço, 12 poses, quatro voltas e a pausa) para
   comparar; essa pasta não é escrita por nenhum script.

   Exporta window.CenaCurandeira = { base, desenhar, pontos, poseDe, QW, QH }. */
"use strict";

(() => {
  const QW = 320, QH = 96;
  const NOMES = ["fundo", "fogo", "vapor", "vapor-forte", "baldes", "pita", "marta", "frente"];
  const carregar = (pasta) => {
    const im = {};
    NOMES.forEach((n) => { const i = new Image(); i.src = `/proto-cur/${pasta}/${n}.png`; im[n] = i; });
    return im;
  };
  const IM = carregar("camadas"), ANT = carregar("anterior");
  let ROTINA = null;
  fetch("/proto-cur/camadas/rotina.json").then((r) => r.json()).then((j) => { ROTINA = j; }).catch(() => {});
  const pronta = (i) => i.complete && i.naturalWidth > 0;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches || document.body.dataset.curReduzido === "1";
  const anterior = () => document.body.dataset.curAnterior === "1";

  /** O quadro de quem atende no tique q: o da rotina (ou, na passada anterior, o do giro com a pausa). */
  function poseDe(q, quem) {
    if (anterior()) {
      const D = 12 * 4 + 12, r = ((q % D) + D) % D;
      return r < 48 ? r % 12 : 0;
    }
    const rot = ROTINA && ROTINA[quem];
    if (!rot) return 0;
    const n = rot.tempo.length;
    return rot.tempo[((q % n) + n) % n];
  }
  const parada = (quem) => (anterior() || !ROTINA ? 0 : ROTINA[quem].parada);

  function base(W, d) {
    const k = document.createElement("canvas"); k.width = QW; k.height = QH;
    const b = { canvas: k, ox: 0, d, cheia: false };
    encher(b);
    return b;
  }
  function encher(b) {  // o fundo também na base (a troca de cena parte dela)
    if (b.cheia || !pronta(IM.fundo)) return;
    b.canvas.getContext("2d").drawImage(IM.fundo, 0, 0); b.cheia = true;
  }
  const tira = (c, im, i) => { if (pronta(im)) c.drawImage(im, i * QW, 0, QW, QH, 0, 0, QW, QH); };
  function desenhar(c, W, b, est, quadro) {
    encher(b);
    const quieto = reduzido(), d = b.d || {}, escura = d.agua === "escura", A = anterior() ? ANT : IM;
    const quem = d.quem === "marta" ? "marta" : "pita";
    c.imageSmoothingEnabled = false;
    c.clearRect(0, 0, QW, QH);
    if (pronta(A.fundo)) c.drawImage(A.fundo, 0, 0);
    const passo = quieto ? 1 : Math.floor(quadro / 2) % 4;
    tira(c, A.fogo, passo);
    if (escura && pronta(A.baldes)) c.drawImage(A.baldes, 0, 0);
    tira(c, escura ? A["vapor-forte"] : A.vapor, passo);
    tira(c, A[quem], quieto ? parada(quem) : poseDe(quadro, quem));
    if (pronta(A.frente)) c.drawImage(A.frente, 0, 0);
  }

  // O nome de quem atende na parede à direita dela (embaixo das prateleiras: não cobre a cabeça, as mãos nem o
  // almofariz); o da Saída na porta.
  const PONTOS = {
    curandeira: { area: [146, 28, 30, 54], balao: [190, 52], foco: [160, 50] },
    saida: { area: [10, 10, 30, 64], balao: [25, 30], foco: [25, 44] },
  };

  window.CenaCurandeira = { base, desenhar, pontos: PONTOS, poseDe, QW, QH };
})();
