/* O interior da taverna, candidata B (protótipo, estudo estático; nada disto entra no jogo). O salão em
   profundidade: a parede do balcão mais perto, à esquerda (a porta da rua, as prateleiras, o taverneiro sob o
   lampião, a porta da despensa); o salão fundo à direita (a lareira, a escada até a galeria dos quartos, o canto de
   Morel debaixo dela); as mesas em três distâncias, com gente de frente, de três quartos, de costas e de perfil.

   As camadas vêm de ferramentas/prototipos/taverna/exportar.py (exportar_b, em /proto-tav/camadas/b/): o fundo com as
   pessoas paradas (com Morel ou, recrutado, sem ele), o fogo e as velas (4 quadros cada, a 200 ms). Movimento
   reduzido: o fogo e as velas parados. As pessoas ainda não se mexem: a animação vem depois de a construção ser
   aprovada.

   Também exporta window.CenaTaverna, que escolhe entre esta e a A (histórico) pela faixa da demonstração
   (body.dataset.tavCand). */
"use strict";

(() => {
  const QW = 320, QH = 96;
  const RAIZ = "/proto-tav/camadas/b/";
  const im = (n) => { const i = new Image(); i.src = RAIZ + n + ".png"; return i; };
  const IM = { fundo: im("fundo"), semMorel: im("fundo-sem-morel"), fogo: im("fogo"), velas: im("velas") };
  const pronta = (i) => i && i.complete && i.naturalWidth > 0;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches
    || document.body.dataset.tavReduzido === "1";
  // quem está na sala (para a conferência): as sete pessoas do estudo e Morel, quando o motor diz que ele está no canto
  const GENTE = ["taverneiro", "freguês do balcão", "freguesa", "freguês de costas", "meio, atrás", "meio, de lado",
    "junto do fogo"];
  const presentes = (d) => (d && d.morel ? [...GENTE, "morel"] : GENTE);
  const fundoDe = (d) => (d && d.morel ? IM.fundo : IM.semMorel);

  function base(W, d) {
    const k = document.createElement("canvas"); k.width = QW; k.height = QH;
    const b = { canvas: k, ox: 0, d, cheia: false };
    encher(b);
    return b;
  }
  function encher(b) {
    const f = fundoDe(b.d);
    if (b.cheia || !pronta(f)) return;
    b.canvas.getContext("2d").drawImage(f, 0, 0); b.cheia = true;
  }
  const tira = (c, i, n) => { if (pronta(i)) c.drawImage(i, n * QW, 0, QW, QH, 0, 0, QW, QH); };
  function desenhar(c, W, b, est, quadro) {
    encher(b);
    const quieto = reduzido(), f = fundoDe(b.d);
    c.imageSmoothingEnabled = false;
    c.clearRect(0, 0, QW, QH);
    if (pronta(f)) c.drawImage(f, 0, 0);
    tira(c, IM.fogo, quieto ? 1 : Math.floor(quadro / 2) % 4);
    tira(c, IM.velas, quieto ? 1 : Math.floor(quadro / 2) % 4);
  }

  // Os pontos em cima do que representam, e os nomes onde não há rosto nem mão: o do Taverneiro nas prateleiras, acima
  // da cabeça dele; o da Escada na parede, acima dos degraus de cima (a galeria e as portas dos quartos ficam na área);
  // o da Despensa acima da porta baixa; o do Homem do canto na parede, acima de Morel; o da Saída acima da porta da rua.
  const PONTOS = {
    taverneiro: { area: [72, 30, 18, 13], balao: [80, 29], foco: [80, 38] },
    escada: { area: [200, 4, 78, 44], balao: [236, 13], foco: [240, 30] },
    despensa: { area: [109, 29, 18, 29], balao: [118, 28], foco: [118, 44] },
    morel: { area: [281, 33, 18, 13], balao: [290, 31], foco: [290, 40] },
    saida: { area: [4, 16, 24, 42], balao: [16, 14], foco: [16, 40] },
  };

  window.CenaTavernaB = { base, desenhar, pontos: PONTOS, presentes, QW, QH };

  // A cena que o jogo registra (telas/cenas.js): a candidata da faixa (B por padrão; a A como histórico)
  const cand = () => (document.body.dataset.tavCand === "a" ? window.CenaTavernaA : window.CenaTavernaB);
  window.CenaTaverna = {
    base: (W, d) => cand().base(W, d),
    desenhar: (...a) => cand().desenhar(...a),
    get pontos() { return cand().pontos; },
    presentes: (d) => cand().presentes(d),
    QW, QH,
  };
})();
