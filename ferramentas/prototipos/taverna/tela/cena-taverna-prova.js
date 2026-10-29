/* A prova de qualidade da taverna (protótipo; nada disto entra no jogo): os dois jogadores, a mesa e os banquinhos em
   duas grades nativas, no mesmo lugar da tela. A sala por baixo é a F sem o conjunto (o entorno provisório, sem
   aprovação), com o fogo e as velas da F; o conjunto vem por cima, numa imagem com a resolução nativa dele:
   - A: 66×42 (a grade atual: um pixel do conjunto por pixel da sala);
   - B: 132×84 (o dobro em cada eixo, na mesma área);
   - B2: a B refinada pela referência "Jogo de tabuleiro na taverna" (132×84; a fonte em prova/b2/aseprite);
   - B3: a B2 com os ombros e os braços redesenhados (132×84; a fonte em prova/b3/aseprite);
   - B4: a B3 com o ombro de cá do de verde suavizado (132×84; a fonte em prova/b4/aseprite).
   Todas ocupam exatamente o recorte R da sala (x 174, y 42, 66×42 pixels da sala), escaladas pelo navegador sem
   suavização (image-rendering: pixelated) com a mesma escala da vista (Vista.caixaDaArte). Com "Isolado", um fundo
   neutro cobre a sala e o conjunto aparece sozinho, no mesmo tamanho, com o trecho de piso.

   O canto de Morel: no M1 (o padrão), Morel, a cadeira e a mesa dele desenhados juntos na densidade da B4 (144×112, no
   recorte M da sala: x 248, y 36, 72×56), numa segunda imagem por cima da vista; a sala por baixo é a F sem o canto
   (fundo-m1) e a chama da vela dele fica no castiçal novo (velas-m1). Com Morel recrutado, a imagem sem ele (m1-sem: a
   cadeira e a mesa). Na versão anterior ("f"), o canto da F, como estava. O ponto do Homem do canto segue a versão.

   As camadas vêm de ferramentas/prototipos/taverna/prova (conjunto.py e o fonte.py de cada versão), servidas em
   /proto-tav/camadas/prova/. Exporta window.CenaTavernaProva; a escolha entre as candidatas fica em cena-taverna-b.js. */
"use strict";

(() => {
  const QW = 320, QH = 96, R = [174, 42, 66, 42], M = [248, 36, 72, 56];
  const RAIZ = "/proto-tav/camadas/";
  const im = (n) => { const i = new Image(); i.src = RAIZ + n + ".png"; return i; };
  const IM = { fundo: im("prova/fundo"), semMorel: im("prova/fundo-sem-morel"), fogo: im("f/fogo"), velas: im("f/velas"),
    fundoM1: im("prova/fundo-m1"), velasM1: im("prova/velas-m1") };
  const canto = () => (document.body.dataset.tavMorel === "f" ? "f" : "m1");
  // o ponto de Morel no M1: a área no tronco e nas coxas, o balão acima da cabeça, o foco no peito (longe das mãos)
  const MOREL_M1 = { area: [270, 56, 18, 26], balao: [280, 45], foco: [276, 64] };
  const pronta = (i) => i && i.complete && i.naturalWidth > 0;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches || document.body.dataset.tavReduzido === "1";
  const fundoDe = (d) => (canto() === "m1" ? IM.fundoM1 : d && d.morel ? IM.fundo : IM.semMorel);

  // a camada por cima da vista: o fundo neutro (isolado), o piso e o conjunto, em resolução nativa
  const capa = document.createElement("div");
  capa.id = "tav-prova";
  capa.innerHTML = `<div class="neutro"></div><img class="chao" alt=""><img class="grupo" alt=""><img class="morel" alt="">`;
  const neutro = capa.querySelector(".neutro"), chao = capa.querySelector(".chao"), grupo = capa.querySelector(".grupo");
  const morel = capa.querySelector(".morel");
  const grade = () => (["b", "b2", "b3", "b4"].includes(document.body.dataset.tavProva) ? document.body.dataset.tavProva : "a");
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
    const d = window.Cenas && Cenas.atual() && Cenas.atual().d, m1 = canto() === "m1";
    const arq = `prova/${d && d.morel ? "m1" : "m1-sem"}.png`;
    if (m1 && !morel.src.endsWith(arq)) morel.src = RAIZ + arq;
    morel.hidden = !m1;
    Object.assign(morel.style, { left: q.esq + q.dx + M[0] * q.ex + "px", top: q.topo + q.dy + M[1] * q.ey + "px",
      width: M[2] * q.ex + "px", height: M[3] * q.ey + "px" });
    capa.dataset.canto = m1 ? `m1-${d && d.morel ? "presente" : "ausente"}` : "f";
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
    tira(c, canto() === "m1" ? IM.velasM1 : IM.velas, quieto ? 1 : Math.floor(quadro / 2) % 4);
    posicionar();
  }

  window.CenaTavernaProva = {
    base, desenhar, QW, QH,
    get pontos() {                                                      // os pontos da F (o entorno é o dela)
      const p = window.CenaTavernaF.pontos;
      return canto() === "m1" ? { ...p, morel: MOREL_M1 } : p;
    },
    presentes: (d) => window.CenaTavernaF.presentes(d),
    R, M,
  };
})();
