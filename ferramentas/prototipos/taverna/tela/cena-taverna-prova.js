/* A prova de qualidade da taverna (protótipo; nada disto entra no jogo): os dois jogadores, a mesa e os banquinhos em
   duas grades nativas, no mesmo lugar da tela. A sala por baixo é a F sem o conjunto (o entorno provisório, sem
   aprovação), com o fogo e as velas da F; o conjunto vem por cima, numa imagem com a resolução nativa dele:
   - A: 66×42 (a grade atual: um pixel do conjunto por pixel da sala);
   - B: 132×84 (o dobro em cada eixo, na mesma área).
   As duas ocupam exatamente o recorte R da sala (x 174, y 42, 66×42 pixels da sala), escaladas pelo navegador sem
   suavização (image-rendering: pixelated) com a mesma escala da vista (Vista.caixaDaArte). Com "Isolado", um fundo
   neutro cobre a sala e o conjunto aparece sozinho, no mesmo tamanho, com o trecho de piso.

   As camadas vêm de ferramentas/prototipos/taverna/prova/conjunto.py (em /proto-tav/camadas/prova/). Exporta
   window.CenaTavernaProva; a escolha entre as candidatas fica em cena-taverna-b.js. */
"use strict";

(() => {
  const QW = 320, QH = 96, R = [174, 42, 66, 42];
  const RAIZ = "/proto-tav/camadas/";
  const im = (n) => { const i = new Image(); i.src = RAIZ + n + ".png"; return i; };
  const IM = { fundo: im("prova/fundo"), semMorel: im("prova/fundo-sem-morel"), fogo: im("f/fogo"), velas: im("f/velas") };
  const pronta = (i) => i && i.complete && i.naturalWidth > 0;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches || document.body.dataset.tavReduzido === "1";
  const fundoDe = (d) => (d && d.morel ? IM.fundo : IM.semMorel);

  // a camada por cima da vista: o fundo neutro (isolado), o piso e o conjunto, em resolução nativa
  const capa = document.createElement("div");
  capa.id = "tav-prova";
  capa.innerHTML = `<div class="neutro"></div><img class="chao" alt=""><img class="grupo" alt="">`;
  const neutro = capa.querySelector(".neutro"), chao = capa.querySelector(".chao"), grupo = capa.querySelector(".grupo");
  const grade = () => (document.body.dataset.tavProva === "b" ? "b" : "a");
  let ativa = false;

  function posicionar() {
    // Vista é uma constante global do jogo (não fica em window)
    const cena = document.getElementById("cena"), q = typeof Vista !== "undefined" && Vista.caixaDaArte();
    const mostrar = ativa && !!q && !!cena;
    capa.hidden = !mostrar;
    if (!mostrar) return;
    if (capa.parentElement !== cena) cena.insertBefore(capa, document.getElementById("pontos-cena"));
    const g = grade(), iso = document.body.dataset.tavIsolado === "1";
    if (!grupo.src.endsWith(`prova/${g}.png`)) grupo.src = `${RAIZ}prova/${g}.png`;
    if (!chao.src.endsWith(`prova/chao-${g}.png`)) chao.src = `${RAIZ}prova/chao-${g}.png`;
    const caixa = { left: q.esq + q.dx + R[0] * q.ex, top: q.topo + q.dy + R[1] * q.ey, width: R[2] * q.ex, height: R[3] * q.ey };
    for (const e of [grupo, chao]) {
      Object.assign(e.style, { left: caixa.left + "px", top: caixa.top + "px", width: caixa.width + "px", height: caixa.height + "px" });
    }
    Object.assign(neutro.style, { left: q.esq + "px", top: q.topo + "px", width: q.larg + "px", height: q.alt + "px" });
    neutro.hidden = !iso;
    chao.hidden = !iso;
    capa.dataset.grade = g;
  }
  if (typeof Vista !== "undefined" && Vista.aoRedimensionar) Vista.aoRedimensionar(posicionar);
  // a camada só existe com a taverna e a prova à vista; sai quando a cena ou a candidata muda
  setInterval(() => {
    const agora = !!(window.Cenas && Cenas.atual() && Cenas.atual().d.cena === "taverna" && document.body.dataset.tavCand === "prova");
    if (agora !== ativa) { ativa = agora; posicionar(); }
  }, 150);

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
    posicionar();
  }

  window.CenaTavernaProva = {
    base, desenhar, QW, QH,
    get pontos() { return window.CenaTavernaF.pontos; },                // os pontos da F (o entorno é o dela)
    presentes: (d) => window.CenaTavernaF.presentes(d),
    R,
  };
})();
