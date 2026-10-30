/* As vistas animadas da taverna (protótipo; nada disto entra no jogo).

   - window.CenaTavernaG4: o balcão aprovado (a G3) com o taverneiro limpando a caneca (window.CenaTavernaG4V1, a
     atuação anterior, em /proto-tav/camadas/g4-v1/, para comparar). Camadas de
     /proto-tav/camadas/g4/ (g4/fonte.py): o fundo, o fogo e as velas (4 quadros, a 200 ms), a pose do taverneiro pela
     linha do tempo (rotina.json, um índice por tique de 100 ms), e o balcão com os fregueses por cima.
   - window.CenaTavernaMorel: a vista diante de Morel (morel/vista/exportar.py), na mesma moldura (320×96): o fundo, a
     pose do taverneiro ao fundo, o corpo e a cabeça de Morel, a mesa, as chamas e o braço da colher por cima;
     window.CenaTavernaMorelV2 (camadas/morel-vista-v2, antes do estudo do braço) e window.CenaTavernaMorelV1 (a
     primeira, camadas/morel-vista-v1), para comparar. Na atual, cada pagamento do evento lança as moedas na mesa
     (moedas.json) e Morel para de comer para olhar; demo.py registra a mesma vista como a cena `taverna_mesa`.

   O tempo é o relógio da vista do jogo (o `quadro` que a cena recebe, a 100 ms): sair e entrar não cria outro relógio.
   Movimento reduzido (a preferência do sistema ou a "Pose parada" do painel): a pose parada de cada um e as chamas
   paradas. */
"use strict";

(() => {
  const QW = 320, QH = 96;
  const pronta = (i) => i && i.complete && i.naturalWidth > 0;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches || document.body.dataset.tavReduzido === "1";
  const carregar = (raiz, nomes) => Object.fromEntries(nomes.map((n) => { const i = new Image(); i.src = raiz + n + ".png"; return [n, i]; }));
  const json = (url) => { const r = { pronto: null }; fetch(url).then((x) => x.json()).then((d) => { r.pronto = d; }); return r; };
  const tira = (c, i, n) => { if (pronta(i)) c.drawImage(i, n * QW, 0, QW, QH, 0, 0, QW, QH); };
  /** Uma figura animada recortada na caixa dela: a pose da vez pela linha do tempo, ou a parada. */
  function figura(c, img, rot, quadro, quieto) {
    if (!pronta(img) || !rot) return;
    const [x, y, w, h] = rot.caixa;
    const n = quieto ? rot.parada : rot.tempo[quadro % rot.tempo.length];
    c.drawImage(img, n * w, 0, w, h, x, y, w, h);
  }
  /** Uma das faixas (0: atrás da mesa; 1: por cima dela) de uma figura em duas faixas, na pose da vez. */
  function faixa(c, img, rot, quadro, quieto, f) {
    if (!pronta(img) || !rot) return;
    const [x, y, w, h] = rot.caixa;
    const n = quieto ? rot.parada : rot.tempo[quadro % rot.tempo.length];
    c.drawImage(img, n * w, f * h, w, h, x, y, w, h);
  }
  function base() {
    const k = document.createElement("canvas"); k.width = QW; k.height = QH;
    return { canvas: k, ox: 0, d: null };
  }

  // ---------------------------------------------------------------- o balcão animado (G4)
  /** O balcão animado a partir das camadas de uma pasta (a atuação atual e a anterior, para comparar). */
  const balcao = (raiz) => {
    const G4 = carregar(raiz, ["fundo", "fogo", "velas", "taverneiro", "frente"]);
    const ROT_G4 = json(raiz + "rotina.json");
    return {
    base: (W, d) => Object.assign(base(), { d }),
    desenhar(c, W, b, est, quadro) {
      const quieto = reduzido();
      c.imageSmoothingEnabled = false;
      c.clearRect(0, 0, QW, QH);
      if (pronta(G4.fundo)) c.drawImage(G4.fundo, 0, 0);
      tira(c, G4.fogo, quieto ? 1 : Math.floor(quadro / 2) % 4);
      tira(c, G4.velas, quieto ? 1 : Math.floor(quadro / 2) % 4);
      figura(c, G4.taverneiro, ROT_G4.pronto, quadro, quieto);
      if (pronta(G4.frente)) c.drawImage(G4.frente, 0, 0);
    },
    get pontos() { return window.CenaTavernaG.pontos; },
    presentes: () => ["taverneiro", "freguês da esquerda", "freguês da direita"],
    QW, QH,
    };
  };
  // a atuação atual (as mãos conduzem, o tronco fica) e a anterior (o tronco e a cabeça desciam a cada passada)
  window.CenaTavernaG4 = balcao("/proto-tav/camadas/g4/");
  window.CenaTavernaG4V1 = balcao("/proto-tav/camadas/g4-v1/");

  // ---------------------------------------------------------------- diante de Morel
  /** A pose de Morel no tique: a da rotina, ou, depois de um pagamento, a reação (moedas.json): a colher volta ao
   *  descanso pelo caminho mais curto entre as poses que existem, os olhos nas moedas enquanto elas caem e ele conta, o
   *  olhar para quem pagou, e a rotina recomeça do começo (o descanso emenda nela). */
  function poseMorel(r, quadro, quieto, lance) {
    if (quieto) return r.parada;
    if (!lance) return r.tempo[quadro % r.tempo.length];
    const t = quadro - lance.inicio;
    return t < lance.reacao.length ? lance.reacao[t] : r.tempo[(t - lance.reacao.length) % r.tempo.length];
  }
  /** O pagamento sobre a mesa: cada pagamento que o motor manda (d.pagamentos, contado por ele) lança as moedas uma vez,
   *  no tique em que a cena o recebe; repetir a mesma mensagem não lança de novo. As moedas ficam na mesa até a cena
   *  acabar; com movimento reduzido, já assentadas. */
  function pagamentos(est, d, quadro, r, M) {
    const novos = (d && d.pagamentos) || 0;
    est.tavLances = est.tavLances || [];
    while (M && r && est.tavLances.length < novos) {
      const ultimo = est.tavLances[est.tavLances.length - 1];
      const agora = poseMorel(r.morel, quadro, false, ultimo);
      const reacao = M.reacao.volta[agora].slice();
      M.reacao.depois.forEach(([p, n]) => { for (let k = 0; k < n; k++) reacao.push(p); });
      est.tavLances.push({ inicio: quadro, reacao, dx: 7 * est.tavLances.length });
    }
  }
  function moedas(c, img, M, lance, quadro, quieto) {
    if (!pronta(img)) return;
    const q = M.quadros[quieto ? M.quadros.length - 1 : Math.min(quadro - lance.inicio, M.quadros.length - 1)];
    q.forEach(([nome, x, y]) => {
      const [i, w, h] = M.desenhos[nome];
      c.drawImage(img, i * M.celula, 0, w, h, x + lance.dx, y, w, h);
    });
  }
  /** A vista diante de Morel a partir das camadas de uma pasta (a atual e a anterior, para comparar). `comMoedas`: a
   *  atual, a única com o pagamento. */
  function vistaMorel(raiz, pontos, comMoedas) {
    const MO = carregar(raiz, ["fundo", "chamas", "morel", "taverneiro", "frente"].concat(comMoedas ? ["moedas"] : []));
    const ROT = json(raiz + "rotina.json");
    const MOE = comMoedas ? json(raiz + "moedas.json") : { pronto: null };
    return {
      base: (W, d) => Object.assign(base(), { d }),
      desenhar(c, W, b, est, quadro) {
        const quieto = reduzido(), r = ROT.pronto, M = MOE.pronto;
        pagamentos(est, b.d, quadro, r, M);
        const lance = est.tavLances && est.tavLances[est.tavLances.length - 1];
        const morel = r && Object.assign({}, r.morel, { tempo: [poseMorel(r.morel, quadro, quieto, lance)], parada: poseMorel(r.morel, quadro, quieto, lance) });
        c.imageSmoothingEnabled = false;
        c.clearRect(0, 0, QW, QH);
        if (pronta(MO.fundo)) c.drawImage(MO.fundo, 0, 0);
        if (r) figura(c, MO.taverneiro, r.taverneiro, quadro, quieto);
        if (r) faixa(c, MO.morel, morel, 0, true, 0);               // o corpo e a cabeça de Morel, atrás da mesa
        if (pronta(MO.frente)) c.drawImage(MO.frente, 0, 0);         // a mesa, o que está nela, a mão que descansa
        tira(c, MO.chamas, quieto ? 1 : Math.floor(quadro / 2) % 4); // a lareira e a chama da vela (no pavio, por cima)
        if (r) faixa(c, MO.morel, morel, 0, true, 1);               // o braço da colher, por cima da mesa
        if (M) (est.tavLances || []).forEach((l) => moedas(c, MO.moedas, M, l, quadro, quieto));  // na frente de tudo
      },
      pontos,
      presentes: () => ["Morel", "taverneiro"],
      QW, QH,
    };
  }
  // os pontos sobre o que está desenhado: o taverneiro, ao fundo, leva à bebida (como no balcão); Morel, ao cartão do
  // encontro, só quando o motor o manda (o Homem do canto), com o balão no balcão ao lado, longe do rosto; a porta da
  // despensa, à direita dele, só enquanto ela espera
  window.CenaTavernaMorel = vistaMorel("/proto-tav/camadas/morel-vista/", {
    taverneiro: { area: [142, 15, 18, 21], balao: [151, 15], foco: [151, 24] },
    morel: { area: [182, 4, 72, 58], balao: [280, 46], foco: [218, 30] },
    despensa: { area: [274, 7, 25, 29], balao: [286, 18], foco: [286, 22] },
  }, true);
  // a segunda versão (antes do estudo de construção do braço), com os mesmos pontos
  window.CenaTavernaMorelV2 = vistaMorel("/proto-tav/camadas/morel-vista-v2/", window.CenaTavernaMorel.pontos);
  // a primeira versão (antes das correções do espaço, da mesa e do braço), para comparar no mesmo estado
  window.CenaTavernaMorelV1 = vistaMorel("/proto-tav/camadas/morel-vista-v1/", {
    taverneiro: { area: [92, 20, 20, 17], balao: [102, 19], foco: [102, 28] },
    morel: { area: [186, 4, 64, 56], balao: [272, 40], foco: [218, 30] },
    despensa: { area: [283, 6, 23, 32], balao: [294, 18], foco: [294, 22] },
  });
})();
