/* As vistas animadas da taverna (protótipo; nada disto entra no jogo).

   - window.CenaTavernaG4: o balcão aprovado (a G3) com o taverneiro limpando a caneca (window.CenaTavernaG4V1, a
     atuação anterior, em /proto-tav/camadas/g4-v1/, para comparar). Camadas de
     /proto-tav/camadas/g4/ (g4/fonte.py): o fundo, o fogo e as velas (4 quadros, a 200 ms), a pose do taverneiro pela
     linha do tempo (rotina.json, um índice por tique de 100 ms), e o balcão com os fregueses por cima.
   - window.CenaTavernaMorel: a vista diante de Morel (morel/vista/exportar.py), na mesma moldura (320×96): o fundo, a
     pose do taverneiro ao fundo, o corpo e a cabeça de Morel, a mesa, as chamas e o braço da colher por cima;
     window.CenaTavernaMorelV2 (camadas/morel-vista-v2, antes do estudo do braço) e window.CenaTavernaMorelV1 (a
     primeira, camadas/morel-vista-v1), para comparar. Na atual, cada pagamento do evento lança as moedas na mesa
     (moedas.json) e Morel para de comer para olhar.
   - window.CenaTavernaMorelCanto: Morel comendo no canto da taverna (morel/canto/, a nova direção; a vista diante do
     balcão fica reservada para a Vó Berta), pela mesma função; window.CenaTavernaMesa escolhe entre as duas pela faixa
     (o canto por padrão) e é a que demo.py registra como a cena `taverna_mesa`, a do encontro.
   - window.CenaTavernaQuedaVista.nos e .morel: a queda de braço na vista aprovada (o "queda 1" refinado,
     morel/queda-vista/; a candidata em avaliação): a sequência de um desfecho (a pega se firma, a disputa, o derrube,
     o impacto, a pausa), pela linha do tempo de queda-vista.json, a partir do momento em que a cena aparece; o fundo
     da disputa, a pose da vez na caixa dela e as chamas da vista por cima. Movimento reduzido: a pose do meio
     enquanto dura a disputa e a final depois, sem passagens, e as chamas paradas.
   - window.CenaTavernaQueda3: a pose central da queda de braço, a terceira proposta (desenhada à mão sobre a
     construção; para a avaliação); window.CenaTavernaQueda2 (a vista de detalhe calculada) e window.CenaTavernaQueda
     (na câmera da conversa), as anteriores, como histórico.

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
  /** A queda de braço no canto (morel/queda-canto/, candidata): o pose da sequência no tique, ou um número negativo
   *  -(1 + p) enquanto Morel ainda volta ao repouso pela pose p da rotina de comer. A sequência começa quando o pedido
   *  chega (o motor: `prepara` quando o teste de Força começa, `nos` ou `morel` com o resultado; ou o painel): a volta
   *  ao repouso pelo caminho mais curto (o mesmo do pagamento), a preparação (a colher solta, a tigela para a direita, o
   *  braço ao meio, o nosso entrando, a pega), a espera (a disputa) até o motor dizer o resultado, a disputa e o derrube
   *  desse resultado, e o depois, que fica. A apresentação acompanha o resultado do motor; não o decide. */
  function poseQuedaCanto(Q, est, quadro, quieto) {
    const q = est.tavQueda;
    const t = quadro - q.inicio - (q.pausa || 0);
    const disputa = Q.poses.indexOf("disputa");
    if (quieto) {   // movimento reduzido: sem a volta nem as passagens; a disputa, o fim e o depois, parados
      const red = q.desfecho && Q.desfechos[q.desfecho].reduzido;
      return red ? red[Math.max(0, Math.min(t, red.length - 1))] : disputa;
    }
    if (t < 0) return -(1 + 17);                          // o reinício pelo painel: o repouso, parado, antes de recomeçar
    if (t < q.volta.length) return -(1 + q.volta[t]);
    const u = t - q.volta.length;
    if (u < Q.preparo.length) return Q.preparo[u];
    if (!q.desfecho) return Q.espera[(u - Q.preparo.length) % Q.espera.length];
    if (q.inicioD === undefined) q.inicioD = u;
    const tempo = Q.desfechos[q.desfecho].tempo;
    return tempo[Math.min(u - q.inicioD, tempo.length - 1)];
  }
  /** A vista diante de Morel a partir das camadas de uma pasta (a atual e a anterior, para comparar). `comMoedas`: a
   *  atual, a única com o pagamento; `comQueda`: o canto, com a queda de braço candidata. */
  function vistaMorel(raiz, pontos, comMoedas, semTaverneiro, comQueda) {
    const MO = carregar(raiz, ["fundo", "chamas", "morel", "frente"].concat(semTaverneiro ? [] : ["taverneiro"])
      .concat(comMoedas ? ["moedas"] : []).concat(comQueda ? ["queda-canto"] : []));
    const ROT = json(raiz + "rotina.json");
    const MOE = comMoedas ? json(raiz + "moedas.json") : { pronto: null };
    const QC = comQueda ? json(raiz + "queda-canto.json") : { pronto: null };
    return {
      base: (W, d) => Object.assign(base(), { d }),
      desenhar(c, W, b, est, quadro) {
        const quieto = reduzido(), r = ROT.pronto, M = MOE.pronto, Q = QC.pronto;
        const pedido = est.qcForcado || (b.d && b.d.queda);
        if (Q && r && pedido) {
          if (!est.tavQueda) {
            const agora = poseMorel(r.morel, quadro, false, est.tavLances && est.tavLances[est.tavLances.length - 1]);
            est.tavQueda = { inicio: quadro, volta: M ? M.reacao.volta[agora].concat([17]) : [17], pausa: est.qcPausa || 0 };
          }
          if (!est.tavQueda.desfecho && (pedido === "nos" || pedido === "morel")) est.tavQueda.desfecho = pedido;
          const n = poseQuedaCanto(Q, est, quadro, quieto);
          est.qcPose = n < 0 ? null : Q.poses[n];   // a pose à vista (para a conferência)
          if (n >= 0 && pronta(MO["queda-canto"])) {
            pagamentos(est, b.d, quadro, r, M);
            const [x, y, w, h] = Q.caixa;
            c.imageSmoothingEnabled = false;
            c.clearRect(0, 0, QW, QH);
            if (pronta(MO.fundo)) c.drawImage(MO.fundo, 0, 0);
            if (pronta(MO.frente)) c.drawImage(MO.frente, 0, 0);
            c.drawImage(MO["queda-canto"], n * w, 0, w, h, x, y, w, h);
            tira(c, MO.chamas, quieto ? 1 : Math.floor(quadro / 2) % 4);
            if (M) (est.tavLances || []).forEach((l) => moedas(c, MO.moedas, M, l, quadro, quieto));
            return;
          }
          if (n < 0) {   // ainda voltando ao repouso: a rotina de comer, na pose da volta
            const p = -n - 1;
            const morel = Object.assign({}, r.morel, { tempo: [p], parada: p });
            c.imageSmoothingEnabled = false;
            c.clearRect(0, 0, QW, QH);
            if (pronta(MO.fundo)) c.drawImage(MO.fundo, 0, 0);
            faixa(c, MO.morel, morel, 0, true, 0);
            if (pronta(MO.frente)) c.drawImage(MO.frente, 0, 0);
            tira(c, MO.chamas, quieto ? 1 : Math.floor(quadro / 2) % 4);
            faixa(c, MO.morel, morel, 0, true, 1);
            return;
          }
        } else if (est.tavQueda && !pedido) {
          delete est.tavQueda;
        }
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
  // Morel no canto da taverna (morel/canto/, a nova direção, 30/10/2026; a candidata em avaliação): a mesma vista na
  // tela (as duas faixas de Morel, a mesa, a chama, as moedas e a reação ao pagamento), sem o balcão e o taverneiro
  // atrás dele; o ponto de Morel sobre ele, o balão na parede à direita, longe do rosto
  window.CenaTavernaMorelCanto = vistaMorel("/proto-tav/camadas/morel-canto/", {
    morel: { area: [118, 2, 102, 70], balao: [250, 40], foco: [171, 30] },
  }, true, true, true);
  // a queda de braço no canto pelo painel (candidatas): a cena do canto com o desfecho pedido, do repouso ao depois, uma
  // vez (o depois fica); "Repetir do começo" recomeça com uma pausa no repouso, um reinício separado da sequência
  let qcRepetir = false;
  const quedaCanto = (desfecho) => ({
    base: (W, d) => window.CenaTavernaMorelCanto.base(W, d),
    desenhar(c, W, b, est, quadro) {
      if (qcRepetir || est.qcDesfecho !== desfecho) {
        delete est.tavQueda;
        est.qcPausa = qcRepetir ? 12 : 0;
        est.qcDesfecho = desfecho;
        qcRepetir = false;
      }
      est.qcForcado = desfecho;   // só durante este desenho: a cena do encontro não herda o pedido do painel
      window.CenaTavernaMorelCanto.desenhar(c, W, b, est, quadro);
      delete est.qcForcado;
    },
    pontos: {},
    presentes: () => ["Morel"],
    QW, QH,
  });
  window.CenaTavernaQuedaCanto = { nos: quedaCanto("nos"), morel: quedaCanto("morel"), repetir: () => { qcRepetir = true; } };
  // a primeira candidata do canto (antes da revisão da mastigação, do tronco e da parede da esquerda), com os mesmos
  // pontos, para comparar no mesmo estado do encontro
  window.CenaTavernaMorelCantoV1 = vistaMorel("/proto-tav/camadas/morel-canto-v1/", window.CenaTavernaMorelCanto.pontos,
    true, true);
  // a candidata revisada antes das correções da alimentação (a colher de madeira, a coleta na borda da tigela, o
  // cotovelo sobre a caneca), para comparar no mesmo estado do encontro
  window.CenaTavernaMorelCantoV2 = vistaMorel("/proto-tav/camadas/morel-canto-v2/", window.CenaTavernaMorelCanto.pontos,
    true, true);
  // a mesa do encontro (demo.py registra a cena `taverna_mesa` como esta): o canto (o padrão), a primeira candidata do
  // canto ou a vista diante do balcão (a anterior, reservada para a Vó Berta), pela faixa do protótipo
  const mesa = () => ({ balcao: window.CenaTavernaMorel, canto1: window.CenaTavernaMorelCantoV1, canto2: window.CenaTavernaMorelCantoV2 })[document.body.dataset.tavMesa]
    || window.CenaTavernaMorelCanto;
  window.CenaTavernaMesa = {
    base: (W, d) => mesa().base(W, d),
    desenhar: (...a) => mesa().desenhar(...a),
    get pontos() { return mesa().pontos; },
    presentes: () => ["Morel"],
    QW, QH,
  };
  // as três poses da queda de braço (morel/queda/poses.py), paradas, para a avaliação: a disputa, nós vencendo, Morel
  // vencendo, cada uma na moldura da vista (sem pontos; a animação espera as poses aprovadas)
  const QUEDA = carregar("/proto-tav/camadas/morel-vista/", ["queda", "queda2", "queda3"]);
  // a primeira proposta (a câmera da conversa: histórico) e a vista de detalhe (morel/queda2/poses.py, a atual)
  const poseQueda = (img, i) => ({
    base: (W, d) => Object.assign(base(), { d }),
    desenhar(c) {
      c.imageSmoothingEnabled = false;
      c.clearRect(0, 0, QW, QH);
      tira(c, img, i);
    },
    pontos: {},
    presentes: () => ["Morel"],
    QW, QH,
  });
  window.CenaTavernaQueda3 = poseQueda(QUEDA.queda3, 0);  // a terceira proposta: só a disputa, desenhada à mão
  // a queda de braço na vista aprovada (morel/queda-vista/exportar.py): um desfecho do começo ao fim, em volta
  const CHAMAS = carregar("/proto-tav/camadas/morel-vista/", ["chamas"]).chamas;
  const quedaVista = (desfecho, raiz) => {
    const QV = carregar(raiz, ["queda-vista-fundo", "queda-vista"]);
    const ROT_QV = json(raiz + "queda-vista.json");
    return {
      base: (W, d) => Object.assign(base(), { d }),
      desenhar(c, W, b, est, quadro) {
        const r = ROT_QV.pronto, quieto = reduzido();
        if (est.qvInicio === undefined || est.qvDesfecho !== desfecho) { est.qvInicio = quadro; est.qvDesfecho = desfecho; }
        c.imageSmoothingEnabled = false;
        c.clearRect(0, 0, QW, QH);
        if (pronta(QV["queda-vista-fundo"])) c.drawImage(QV["queda-vista-fundo"], 0, 0);
        if (r && pronta(QV["queda-vista"])) {
          const D = r.desfechos[desfecho], linha = quieto ? D.reduzido : D.tempo;
          // est.qvFixo: um tique fixo da linha do tempo (só a conferência, morel/queda-vista/conferir.mjs, o usa)
          const t = est.qvFixo !== undefined ? est.qvFixo : quadro - est.qvInicio;
          const n = linha[t % linha.length];
          est.qvPose = n;  // a pose à vista (para a conferência)
          const [x, y, w, h] = r.caixa;
          c.drawImage(QV["queda-vista"], n * w, 0, w, h, x, y, w, h);
        }
        tira(c, CHAMAS, quieto ? 1 : Math.floor(quadro / 2) % 4);  // a lareira e a vela, como na vista
      },
      pontos: {},
      presentes: () => ["Morel", "taverneiro"],
      QW, QH,
    };
  };
  const RAIZ_QV = "/proto-tav/camadas/morel-vista/";
  // nosV1 e morelV1: a primeira candidata (Morel na postura da conversa), camadas/morel-vista-qv1
  const RAIZ_QV1 = "/proto-tav/camadas/morel-vista-qv1/";
  window.CenaTavernaQuedaVista = { nos: quedaVista("nos", RAIZ_QV), morel: quedaVista("morel", RAIZ_QV),
    nosV1: quedaVista("nos", RAIZ_QV1), morelV1: quedaVista("morel", RAIZ_QV1) };
  window.CenaTavernaQueda2 = [0, 1, 2].map((i) => poseQueda(QUEDA.queda2, i));
  window.CenaTavernaQueda = [0, 1, 2].map((i) => poseQueda(QUEDA.queda, i));
  // a terceira versão (antes do acabamento da manga: o ombro e o cotovelo por segmentos), com os mesmos pontos
  window.CenaTavernaMorelV3 = vistaMorel("/proto-tav/camadas/morel-vista-v3/", window.CenaTavernaMorel.pontos);
  // a segunda versão (antes do estudo de construção do braço), com os mesmos pontos
  window.CenaTavernaMorelV2 = vistaMorel("/proto-tav/camadas/morel-vista-v2/", window.CenaTavernaMorel.pontos);
  // a primeira versão (antes das correções do espaço, da mesa e do braço), para comparar no mesmo estado
  window.CenaTavernaMorelV1 = vistaMorel("/proto-tav/camadas/morel-vista-v1/", {
    taverneiro: { area: [92, 20, 20, 17], balao: [102, 19], foco: [102, 28] },
    morel: { area: [186, 4, 64, 56], balao: [272, 40], foco: [218, 30] },
    despensa: { area: [283, 6, 23, 32], balao: [294, 18], foco: [294, 22] },
  });
})();
