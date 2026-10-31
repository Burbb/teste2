/* A taverna do Vau: dois ambientes do quadro de cima, pelo sistema das cenas (telas/cenas.js), desde a 1.220.0.

   - window.CenaTaverna (a cena "taverna"): o balcão de perto, diante do prédio (estado.local.interiores, como o
     templo). O taverneiro atrás do balcão limpando a caneca, com a pausa para olhar os fregueses; os dois fregueses,
     o fogo do caldeirão e o lampião. Camadas em static/cenas/taverna/: o fundo, o fogo e as velas (4 quadros, a 200
     ms), o taverneiro (um quadro por pose; rotina.json: a caixa, a linha do tempo a 100 ms e a pose parada) e a
     frente (o balcão e os fregueses, por cima dele).
   - window.CenaTavernaMesa (a cena "taverna_mesa"): o encontro com Morel, sentado no canto, em primeira pessoa. Ele
     come (rotina.json: as duas faixas dele, atrás e na frente da mesa); cada pagamento que o motor cobra (d.pagamentos,
     contado por ele) lança as moedas na mesa uma vez (moedas.json), e Morel para de comer para olhar; a queda de braço
     (d.queda: "prepara" quando o teste de Força começa, "nos" ou "morel" com o resultado do motor) toca a preparação
     (ele volta ao repouso, solta a colher, varre a tigela, o braço ao meio, o nosso entra, a pega), a espera na disputa
     até o resultado chegar, a disputa e o derrube desse resultado, e o depois, que fica (queda-canto.json). A
     apresentação acompanha o motor; não decide nada.

   A arte vem das fontes em Aseprite do protótipo (ferramentas/prototipos/taverna: g4/aseprite/taverna-g4.aseprite,
   morel/canto/canto.aseprite e morel/queda-canto/queda-canto.aseprite), copiada para cá por
   ferramentas/prototipos/taverna/jogo.py; não se editam as cópias.

   Os marcadores (Cenas.aguardar, pelo `aguardar` de cada cena): "rolagem" segura o dado do teste até as mãos se
   encontrarem e firmarem a pega (a primeira pose `firma` da preparação); "cena" segura a fila, com o resultado
   chegando, até o derrube bater na mesa e ficar à vista um instante (o texto do que aconteceu vem depois). Sem a queda
   de braço, nos dois casos, segue na hora. Com movimento reduzido, nada se espera: a disputa parada enquanto o dado
   rola, e o fim parado com o resultado. A cena que sai (Cenas.limpar, outra cena) solta o que esperava.

   O relógio é o das cenas (100 ms). Movimento reduzido: as poses paradas, as chamas paradas, as moedas já assentadas. */
"use strict";

(() => {
  const QW = 320, QH = 96;
  const pronta = (i) => i && i.complete && i.naturalWidth > 0;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const carregar = (raiz, nomes) => Object.fromEntries(nomes.map((n) => { const i = new Image(); i.src = raiz + n + ".png"; return [n, i]; }));
  const json = (url) => { const r = { pronto: null }; fetch(url).then((x) => x.json()).then((d) => { r.pronto = d; }).catch(() => {}); return r; };
  const tira = (c, i, n) => { if (pronta(i)) c.drawImage(i, n * QW, 0, QW, QH, 0, 0, QW, QH); };
  /** Uma faixa (0: atrás da mesa; 1: por cima dela) de uma figura em duas faixas, na pose `n`. */
  function faixa(c, img, rot, n, f) {
    if (!pronta(img) || !rot) return;
    const [x, y, w, h] = rot.caixa;
    c.drawImage(img, n * w, f * h, w, h, x, y, w, h);
  }
  const base = (W, d) => { const k = document.createElement("canvas"); k.width = QW; k.height = QH; return { canvas: k, ox: 0, d }; };

  // ---------------------------------------------------------------- o balcão
  const RB = "/static/cenas/taverna/";
  const B = carregar(RB, ["fundo", "fogo", "velas", "taverneiro", "frente"]);
  const ROT_B = json(RB + "rotina.json");
  window.CenaTaverna = {
    base,
    desenhar(c, W, b, est, quadro) {
      const quieto = reduzido(), r = ROT_B.pronto;
      c.imageSmoothingEnabled = false;
      c.clearRect(0, 0, QW, QH);
      if (pronta(B.fundo)) c.drawImage(B.fundo, 0, 0);
      tira(c, B.fogo, quieto ? 1 : Math.floor(quadro / 2) % 4);
      tira(c, B.velas, quieto ? 1 : Math.floor(quadro / 2) % 4);
      if (r && pronta(B.taverneiro)) {
        const [x, y, w, h] = r.caixa, n = quieto ? r.parada : r.tempo[quadro % r.tempo.length];
        c.drawImage(B.taverneiro, n * w, 0, w, h, x, y, w, h);
      }
      if (pronta(B.frente)) c.drawImage(B.frente, 0, 0);
    },
    // só o que está desenhado tem ponto: o Taverneiro (o nome na pedra livre debaixo da viga) leva à bebida; a Despensa
    // (só enquanto ela espera: o motor manda) é a porta da direita, com o nome no alto da folha. O Dormir, o Homem do
    // canto e o Voltar ficam nos cartões.
    pontos: {
      taverneiro: { area: [138, 17, 46, 57], balao: [160, 16], foco: [160, 44] },
      despensa: { area: [281, 12, 30, 44], balao: [296, 19], foco: [296, 38] },
    },
    QW, QH,
  };

  // ---------------------------------------------------------------- a mesa de Morel
  const RM = "/static/cenas/taverna-mesa/";
  const MO = carregar(RM, ["fundo", "chamas", "morel", "frente", "moedas", "queda-canto"]);
  const ROT = json(RM + "rotina.json"), MOE = json(RM + "moedas.json"), QC = json(RM + "queda-canto.json");
  const REPOUSO = 17;   // a pose de repouso da rotina de comer (a mão na borda da tigela), de onde a queda começa
  const FIM_VISTO = 8;  // tiques do derrube batido à vista antes de a fila seguir para o texto

  /** A pose de Morel comendo no tique: a da rotina, ou, depois de um pagamento, a reação (moedas.json): a colher volta
   *  ao descanso pelo caminho mais curto, os olhos nas moedas enquanto elas caem e ele conta, o olhar para quem pagou,
   *  e a rotina recomeça do começo. */
  function poseMorel(r, quadro, quieto, lance) {
    if (quieto) return r.parada;
    if (!lance) return r.tempo[quadro % r.tempo.length];
    const t = quadro - lance.inicio;
    return t < lance.reacao.length ? lance.reacao[t] : r.tempo[(t - lance.reacao.length) % r.tempo.length];
  }
  /** Cada pagamento que o motor manda lança as moedas uma vez, no tique em que a cena o recebe; repetir a mesma
   *  mensagem não lança de novo. As moedas ficam na mesa até a cena acabar. */
  function pagamentos(est, d, quadro, r, M) {
    const novos = (d && d.pagamentos) || 0;
    est.lances = est.lances || [];
    while (M && r && est.lances.length < novos) {
      const ultimo = est.lances[est.lances.length - 1];
      const reacao = M.reacao.volta[poseMorel(r.morel, quadro, false, ultimo)].slice();
      M.reacao.depois.forEach(([p, n]) => { for (let k = 0; k < n; k++) reacao.push(p); });
      est.lances.push({ inicio: quadro, reacao, dx: 7 * est.lances.length });
    }
  }
  function moedas(c, M, lance, quadro, quieto) {
    if (!pronta(MO.moedas)) return;
    const q = M.quadros[quieto ? M.quadros.length - 1 : Math.min(quadro - lance.inicio, M.quadros.length - 1)];
    q.forEach(([nome, x, y]) => {
      const [i, w, h] = M.desenhos[nome];
      c.drawImage(MO.moedas, i * M.celula, 0, w, h, x + lance.dx, y, w, h);
    });
  }

  /** A pose da queda de braço no tique (o índice em queda-canto.json), ou -(1 + p) enquanto Morel ainda volta ao
   *  repouso pela pose p da rotina de comer. Marca na queda os dois momentos que a fila espera: `pegou` (a primeira
   *  `firma`) e `visto` (o derrube batido, FIM_VISTO tiques à vista). */
  function poseQueda(Q, q, quadro, quieto) {
    const t = quadro - q.inicio;
    const disputa = Q.poses.indexOf("disputa");
    if (quieto) {   // sem a volta nem as passagens: a disputa parada; com o resultado, o fim parado e o depois
      q.pegou = true;
      if (!q.desfecho) return disputa;
      const red = Q.desfechos[q.desfecho].reduzido;
      if (q.inicioD === undefined) q.inicioD = t;
      q.visto = true;
      const k0 = red.findIndex((p) => p !== disputa);
      return red[Math.min(k0 + t - q.inicioD, red.length - 1)];
    }
    if (t < q.volta.length) return -(1 + q.volta[t]);
    const u = t - q.volta.length;
    if (u < Q.preparo.length) {
      if (Q.poses[Q.preparo[u]] === "firma") q.pegou = true;
      return Q.preparo[u];
    }
    q.pegou = true;
    if (!q.desfecho) return Q.espera[(u - Q.preparo.length) % Q.espera.length];
    if (q.inicioD === undefined) q.inicioD = u;
    const tempo = Q.desfechos[q.desfecho].tempo, k = u - q.inicioD;
    const fim = tempo.findIndex((p) => Q.poses[p] === q.desfecho + "_fim");
    if (k >= fim + FIM_VISTO) q.visto = true;
    return tempo[Math.min(k, tempo.length - 1)];
  }
  /** O que a fila espera já aconteceu? "rolagem": a pega firmada; "cena": o derrube visto. Sem queda pedida, sim. */
  function cumprido(est, d, evento) {
    const pedido = d && d.queda, q = est.queda;
    if (!pedido) return true;
    if (evento === "rolagem") return !!(q && q.pegou);
    if (evento === "cena") return !(pedido === "nos" || pedido === "morel") || !!(q && q.visto);
    return true;
  }
  function conferirEsperas(est, d) {
    if (!est.esperas || !est.esperas.length) return;
    est.esperas = est.esperas.filter((e) => (cumprido(est, d, e.evento) ? (e.fim(true), false) : true));
  }

  function fundoEMesa(c) {
    c.imageSmoothingEnabled = false;
    c.clearRect(0, 0, QW, QH);
    if (pronta(MO.fundo)) c.drawImage(MO.fundo, 0, 0);
  }
  window.CenaTavernaMesa = {
    base,
    desenhar(c, W, b, est, quadro) {
      const quieto = reduzido(), r = ROT.pronto, M = MOE.pronto, Q = QC.pronto, d = b.d || {};
      const chamas = () => tira(c, MO.chamas, quieto ? 1 : Math.floor(quadro / 2) % 4);  // a lareira e a chama da vela
      const asMoedas = () => { if (M) est.lances.forEach((l) => moedas(c, M, l, quadro, quieto)); };  // na frente de tudo
      if (Q && r && d.queda) {
        if (!est.queda) {   // a queda começa da pose em que ele está, voltando ao repouso pelo caminho do pagamento
          const agora = poseMorel(r.morel, quadro, false, est.lances && est.lances[est.lances.length - 1]);
          est.queda = { inicio: quadro, volta: M ? M.reacao.volta[agora].concat([REPOUSO]) : [REPOUSO] };
        }
        if (!est.queda.desfecho && (d.queda === "nos" || d.queda === "morel")) est.queda.desfecho = d.queda;
        const n = poseQueda(Q, est.queda, quadro, quieto);
        est.qcPose = n < 0 ? null : Q.poses[n];   // a pose à vista (para a conferência)
        pagamentos(est, d, quadro, r, M);
        fundoEMesa(c);
        if (n >= 0) {   // a queda: a mesa e a pose da vez na caixa dela (Morel, os braços, a tigela)
          if (pronta(MO.frente)) c.drawImage(MO.frente, 0, 0);
          if (pronta(MO["queda-canto"])) { const [x, y, w, h] = Q.caixa; c.drawImage(MO["queda-canto"], n * w, 0, w, h, x, y, w, h); }
          chamas();
        } else {        // ainda voltando ao repouso: a rotina de comer, na pose da volta
          faixa(c, MO.morel, r.morel, -n - 1, 0);
          if (pronta(MO.frente)) c.drawImage(MO.frente, 0, 0);
          chamas();
          faixa(c, MO.morel, r.morel, -n - 1, 1);
        }
        asMoedas();
        conferirEsperas(est, d);
        return;
      }
      pagamentos(est, d, quadro, r, M);
      fundoEMesa(c);
      if (r) {
        const p = poseMorel(r.morel, quadro, quieto, est.lances && est.lances[est.lances.length - 1]);
        faixa(c, MO.morel, r.morel, p, 0);                     // o corpo e a cabeça de Morel, atrás da mesa
        if (pronta(MO.frente)) c.drawImage(MO.frente, 0, 0);   // a mesa, o que está nela, a mão que descansa
        chamas();
        faixa(c, MO.morel, r.morel, p, 1);                     // o braço da colher, por cima da mesa
      }
      asMoedas();
      conferirEsperas(est, d);
    },
    /** A fila espera a cena (Cenas.aguardar): "rolagem" até a pega, "cena" até o derrube visto (resolve com true).
     *  Com movimento reduzido, sem a arte carregada ou já cumprido, segue na hora (false). */
    aguardar(est, evento, b) {
      const d = (b && b.d) || {};
      if (reduzido() || !QC.pronto || !ROT.pronto || cumprido(est, d, evento)) return Promise.resolve(false);
      return new Promise((fim) => (est.esperas = est.esperas || []).push({ evento, fim }));
    },
    /** O dado da queda de braço fica embaixo da arte: o esforço dos braços enquanto ele gira é parte do que se lê. */
    acaoNaArte: (d) => !!(d && d.queda),
    pontos: {},
    QW, QH,
  };
})();
