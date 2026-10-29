/* Os estudos estáticos do interior da taverna (protótipo; nada disto entra no jogo): a candidata B (o salão fundo; a
   avaliação: profundidade demais, o fundo pequeno, a escada um esboço), a C (a profundidade contida, a escada e a
   galeria como estrutura, os grupos redistribuídos), a D (a C refeita nos conjuntos de pessoa, assento e mesa) e a E
   (a sala reconstruída numa projeção só). Cada uma é um fundo com as pessoas paradas (com Morel ou, recrutado, sem ele), o fogo e as velas (4 quadros cada, a
   200 ms), exportados por ferramentas/prototipos/taverna/exportar.py (exportar_estatica) em
   /proto-tav/camadas/<b|c|d|e>/. Movimento reduzido: o fogo e as velas parados. As pessoas ainda não se mexem: a animação
   vem depois de a construção ser aprovada.

   Também exporta window.CenaTaverna, que escolhe entre a E (o padrão), a D, a C, a B e a A (histórico) pela faixa da
   demonstração (body.dataset.tavCand). */
"use strict";

(() => {
  const QW = 320, QH = 96;
  const pronta = (i) => i && i.complete && i.naturalWidth > 0;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches
    || document.body.dataset.tavReduzido === "1";

  /** Uma cena estática: o fundo (com ou sem Morel), o fogo e as velas; `gente` só para a conferência. */
  function estatica(cand, pontos, gente) {
    const raiz = `/proto-tav/camadas/${cand}/`;
    const im = (n) => { const i = new Image(); i.src = raiz + n + ".png"; return i; };
    const IM = { fundo: im("fundo"), semMorel: im("fundo-sem-morel"), fogo: im("fogo"), velas: im("velas") };
    const presentes = (d) => (d && d.morel ? [...gente, "morel"] : gente);
    const fundoDe = (d) => (d && d.morel ? IM.fundo : IM.semMorel);
    function encher(b) {
      const f = fundoDe(b.d);
      if (b.cheia || !pronta(f)) return;
      b.canvas.getContext("2d").drawImage(f, 0, 0); b.cheia = true;
    }
    function base(W, d) {
      const k = document.createElement("canvas"); k.width = QW; k.height = QH;
      const b = { canvas: k, ox: 0, d, cheia: false };
      encher(b);
      return b;
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
    return { base, desenhar, pontos, presentes, QW, QH };
  }

  // B. Os nomes onde não há rosto nem mão: o do Taverneiro nas prateleiras, acima da cabeça; o da Escada na parede,
  // acima dos degraus de cima; o da Despensa acima da porta baixa; o do Homem do canto acima de Morel; o da Saída acima
  // da porta da rua.
  window.CenaTavernaB = estatica("b", {
    taverneiro: { area: [72, 30, 18, 13], balao: [80, 29], foco: [80, 38] },
    escada: { area: [200, 4, 78, 44], balao: [236, 13], foco: [240, 30] },
    despensa: { area: [109, 29, 18, 29], balao: [118, 28], foco: [118, 44] },
    morel: { area: [281, 33, 18, 13], balao: [290, 31], foco: [290, 40] },
    saida: { area: [4, 16, 24, 42], balao: [16, 14], foco: [16, 40] },
  }, ["taverneiro", "freguês do balcão", "freguesa", "freguês de costas", "meio, atrás", "meio, de lado", "junto do fogo"]);

  // C. O da Escada na parte de cima dela e na galeria (o nome em cima da primeira porta dos quartos); o do Homem do
  // canto acima da cabeça de Morel, dentro do quadro; os outros como na B.
  window.CenaTavernaC = estatica("c", {
    taverneiro: { area: [69, 36, 14, 14], balao: [76, 35], foco: [76, 44] },
    escada: { area: [196, 3, 92, 40], balao: [261, 12], foco: [250, 30] },
    despensa: { area: [113, 34, 18, 30], balao: [121, 33], foco: [121, 50] },
    morel: { area: [290, 43, 26, 30], balao: [298, 42], foco: [300, 56] },
    saida: { area: [4, 22, 26, 42], balao: [16, 21], foco: [16, 44] },
  }, ["taverneiro", "freguesa", "ponta", "freguês de costas", "roda, atrás", "roda, de lado", "junto do fogo"]);

  // D. Os nomes nos mesmos lugares da C; o da Escada na galeria, que agora começa no patamar mais à direita, e o do
  // Homem do canto acima de Morel no banco de espaldar.
  window.CenaTavernaD = estatica("d", {
    taverneiro: { area: [69, 36, 14, 14], balao: [76, 35], foco: [76, 44] },
    escada: { area: [194, 3, 96, 40], balao: [261, 12], foco: [250, 30] },
    despensa: { area: [113, 34, 18, 30], balao: [121, 33], foco: [121, 50] },
    morel: { area: [292, 43, 24, 32], balao: [300, 42], foco: [302, 58] },
    saida: { area: [4, 22, 26, 42], balao: [16, 21], foco: [16, 44] },
  }, ["taverneiro", "freguesa", "cabeceira", "freguês de costas", "roda, atrás", "roda, de lado", "junto do fogo"]);

  // E. A sala reconstruída numa projeção só: os nomes em cima das portas do fundo (a despensa, a rua), da escada e da
  // galeria (no guarda-corpo, longe das cabeças), do taverneiro (nas prateleiras) e de Morel (na parede da direita).
  window.CenaTavernaE = estatica("e", {
    taverneiro: { area: [50, 38, 14, 16], balao: [57, 37], foco: [57, 46] },
    escada: { area: [210, 3, 66, 50], balao: [258, 12], foco: [244, 32] },
    despensa: { area: [96, 30, 16, 27], balao: [104, 29], foco: [104, 44] },
    morel: { area: [282, 52, 18, 28], balao: [291, 51], foco: [290, 64] },
    saida: { area: [124, 14, 21, 43], balao: [134, 13], foco: [134, 40] },
  }, ["taverneiro", "freguesa", "cabeceira", "freguês de costas", "roda, atrás", "roda, de lado", "junto do fogo"]);

  // A cena que o jogo registra (telas/cenas.js): a candidata da faixa (E por padrão; D, C, B e A como histórico)
  const CANDS = { a: () => window.CenaTavernaA, b: () => window.CenaTavernaB, c: () => window.CenaTavernaC,
    d: () => window.CenaTavernaD, e: () => window.CenaTavernaE };
  const cand = () => (CANDS[document.body.dataset.tavCand] || CANDS.e)();
  window.CenaTaverna = {
    base: (W, d) => cand().base(W, d),
    desenhar: (...a) => cand().desenhar(...a),
    get pontos() { return cand().pontos; },
    presentes: (d) => cand().presentes(d),
    QW, QH,
  };
})();
