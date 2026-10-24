/* O d20 dos testes em três apresentações (1.202.0; etapa 2 do plano 23, o protótipo aprovado em
   ferramentas/prototipos/hud/d20/): o Clássico (o de sempre, app/rolagem.js, o padrão), o Marfim e o Vidro. A escolha
   é uma preferência da tela (cdf-d20, como a velocidade do texto), na Ajuda por enquanto; ela vai para o menu de
   configurações quando ele existir. Sem preferência válida, o Clássico. Não mexe em Estouro/Relicário (Festa.usar).

   Todas recebem a mesma mensagem do motor (atributo, cd, d20, mod, total, sucesso, precisa), não sorteiam nada e têm o
   mesmo ritmo (950 ms girando, ritmo(650) no resultado, a descida até a tirinha dentro desse tempo; pular corta). O
   dado do Marfim e do Vidro é pixel art (d20/dados.js, gerado por desenhar_d20.py no protótipo), desenhado num canvas
   no tamanho nativo e ampliado 2× sem suavização; o número sai dos algarismos desenhados à mão, na face da frente.

   Marfim: o dado de osso polido, o número entalhado em tinta escura; tomba de verdade (seis quadros de meia volta); a
       conta numa tirinha só, em quatro casas com rótulo (dado + bônus = total, contra a dificuldade).
   Vidro: o dado de vidro fumê violeta, as quinas de trás à vista e a luz que atravessa; o número aceso por dentro
       (pisca enquanto ele gira); frente a frente: o bônus (depois o total) de um lado, a dificuldade do outro.
   Os dois: a faixa de resultado aprovada (Sucesso, Falha, Crítico!, Desastre), os sons de sempre, a tirinha do texto
   com o dado pequeno, o ícone da ficha. Com movimento reduzido: sem tombo, sem pulo nem anel; o número ainda troca
   enquanto o dado "rola", e o resultado aparece de vez. */
"use strict";

const Dado20 = (() => {
  const D = D20_DADOS;
  // a preferência (o nome guardado) → o material do desenho; o clássico não tem: é o de app/rolagem.js
  const MAT = { marfim: "marfim", vidro: "vidro" };
  const OPCOES = [["classico", "Clássico"], ["marfim", "Marfim"], ["vidro", "Vidro"]], PREF = "cdf-d20";
  const rolagemClassica = rolagem;  // a de app/rolagem.js, carregada antes
  const ESC = { centro: 2, tirinha: 2, ficha: 1 };
  const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
  let qual = "";
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const cores = new Map();  // "#rrggbb" → [r, g, b], uma vez só (o giro desenha a cada 60 ms)
  const rgb = (h) => cores.get(h) || cores.set(h, [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16))).get(h);

  /** Um canvas no tamanho nativo do dado, ampliado por CSS sem suavização. */
  function tela(mat, tam) {
    const N = D.materiais[mat].tamanhos[tam].repouso.length;
    const cv = document.createElement("canvas");
    cv.width = cv.height = N;
    cv.className = `d20p d20p-${tam} d20p-${mat}`;
    cv.style.width = cv.style.height = N * ESC[tam] + "px";
    cv.setAttribute("aria-hidden", "true");
    return cv;
  }

  /** Os pixels do número `n` no lugar da face da frente (centrado no lugar que o desenho reservou). */
  function algarismos(mat, tam, n) {
    const alg = D.algarismos[tam === "centro" ? "g" : "p"], lugar = D.materiais[mat].tamanhos[tam].numero;
    const s = String(n), w = [...s].reduce((a, c) => a + alg[c][0].length, 0) + s.length - 1;
    let x = lugar.x + Math.floor((lugar.w - w) / 2);
    const y0 = lugar.y, pix = new Set();
    for (const c of s) {
      alg[c].forEach((linha, yy) => [...linha].forEach((ch, xx) => { if (ch === "#") pix.add(`${x + xx},${y0 + yy}`); }));
      x += alg[c][0].length + 1;
    }
    return pix;
  }

  /** Desenha o dado: o repouso (quadro null) ou um quadro do giro; com `n`, o número na tinta do `estado`. */
  function desenhar(cv, mat, tam, { quadro = null, n = null, estado = "neutro" } = {}) {
    const m = D.materiais[mat], t = m.tamanhos[tam];
    const linhas = quadro == null ? t.repouso : t.giro[quadro % t.giro.length];
    const N = linhas.length, ctx = cv.getContext("2d"), img = ctx.createImageData(N, N), px = img.data;
    const por = (x, y, cor) => { const i = (y * N + x) * 4, c = rgb(cor); px[i] = c[0]; px[i + 1] = c[1]; px[i + 2] = c[2]; px[i + 3] = 255; };
    const dentro = (x, y) => x >= 0 && y >= 0 && x < N && y < N && linhas[y][x] !== "." && linhas[y][x] !== "k";
    linhas.forEach((r, y) => [...r].forEach((ch, x) => { if (m.paleta[ch]) por(x, y, m.paleta[ch]); }));
    if (n != null && t.numero) {
      const tinta = D.tintas[mat][estado], pix = algarismos(mat, tam, n), tem = (x, y) => pix.has(`${x},${y}`);
      for (const k of pix) {
        const [x, y] = k.split(",").map(Number);
        if (tinta.luz && dentro(x + 1, y + 1) && !tem(x + 1, y + 1)) por(x + 1, y + 1, tinta.luz);  // o lábio do entalhe
        if (tinta.halo) for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
          if (dentro(x + dx, y + dy) && !tem(x + dx, y + dy)) por(x + dx, y + dy, tinta.halo);  // o brilho em volta
        }
      }
      for (const k of pix) { const [x, y] = k.split(",").map(Number); por(x, y, tinta.tinta); }
      if (tinta.miolo) for (const k of pix) {  // o miolo aceso: a coluna da esquerda de cada traço
        const [x, y] = k.split(",").map(Number);
        if (!tem(x - 1, y) && tem(x + 1, y)) por(x, y, tinta.miolo);
      }
    }
    ctx.putImageData(img, 0, 0);
  }

  /* ---------------------------------------------------------------- o efeito do pouso (pixel, 15 quadros por segundo) */
  // A: a poeira dos dois lados da base e, no Crítico, as estrelas douradas; B: o anel que se abre na cor do resultado.
  const COR_EFEITO = { sucesso: ["#8fbf6a", "#4f9a5b"], falha: ["#e2574c", "#6e0d0d"], critico: ["#fff3a0", "#f2c94c"],
    desastre: ["#b3262b", "#3a0c10"], neutro: ["#f1e4c4", "#8a8070"] };
  const ESTRELA = ["..#..", "..#..", "##W##", "..#..", "..#.."];
  async function pouso(alvo, mat, estado) {
    if (reduzido()) return;
    const N = 96, cv = document.createElement("canvas");
    cv.width = cv.height = N;
    cv.className = "d20p-pouso";
    cv.style.width = cv.style.height = N * 2 + "px";
    alvo.appendChild(cv);
    const ctx = cv.getContext("2d"), [c1, c2] = COR_EFEITO[estado] || COR_EFEITO.neutro;
    const pt = (x, y, cor) => { ctx.fillStyle = cor; ctx.fillRect(x, y, 1, 1); };
    for (let q = 0; q < 4; q++) {
      ctx.clearRect(0, 0, N, N);
      if (mat === "vidro") {  // o anel hexagonal, de pixels, que se abre e se apaga em pontilhado
        const r = 35 + q * 4, nivel = 16 - q * 4;
        for (let a = 0; a < 360; a += 0.6) {
          const t = (a * Math.PI) / 180, k = Math.cos(Math.PI / 6) / Math.cos(((t + Math.PI / 2) % (Math.PI / 3)) - Math.PI / 6);
          const x = Math.round(N / 2 - 0.5 + Math.cos(t) * r * k), y = Math.round(N / 2 - 0.5 + Math.sin(t) * r * k);
          if (BAYER[(y & 3) * 4 + (x & 3)] < nivel) pt(x, y, q < 2 ? c1 : c2);
        }
      } else {  // a poeira: dois punhados que saem de baixo, para os lados
        const cor = q < 2 ? "#c0b8a8" : "#8a8070";
        for (const lado of [-1, 1]) for (let i = 0; i < 4; i++) {
          const x = Math.round(N / 2 + lado * (20 + q * 3 + i * 2)), y = Math.round(N / 2 + 26 - (i % 2) - (q > 1 ? 1 : 0));
          if (q < 3 || i % 2) pt(x, y, cor);
        }
      }
      if (estado === "critico" && q < 3) {  // as estrelas douradas, em volta (as mesmas posições nas duas)
        for (const [ex, ey] of [[14, 20], [78, 26], [20, 74], [74, 70], [48, 6]]) {
          ESTRELA.forEach((l, yy) => [...l].forEach((ch, xx) => { if (ch !== ".") pt(ex + xx - 2, ey + yy - 2, ch === "W" ? "#ffffff" : q ? c2 : c1); }));
        }
      }
      await espera(67);
    }
    cv.remove();
  }

  /* ---------------------------------------------------------------- a rolagem */
  const sinal = (n) => (n >= 0 ? "+" : "−");
  // a regra especial que decidiu o teste (o motor diz se passou; o total dele diz se passaria sem a regra do 20 e do 1)
  function regraEspecial(m) {
    if (m.d20 === 20 && m.total < m.cd) return "o 20 natural sempre passa";
    if (m.d20 === 1 && m.total >= m.cd) return "o 1 natural sempre falha";
    return "";
  }
  const estadoDe = (m) => (m.d20 === 20 ? "critico" : m.d20 === 1 ? "desastre" : m.sucesso ? "sucesso" : "falha");

  function htmlMarfim(m) {
    const det = rolagemPartes(m);
    return `<div class="rc-veu"></div>
      <div class="rc-grupo d20-grupo">
        <div class="rc-cab"><span class="rc-nome">Teste de ${esc(m.atributo)}</span></div>
        <div class="d20-dado"></div>
        <div class="rc-tirinha rc-faixa d20m-conta">${ROLAGEM_CONTORNO}
          <div class="d20m-linha">
            <span class="d20m-casa dado"><b>?</b><i>dado</i></span><span class="d20m-op">${sinal(m.mod)}</span>
            <span class="d20m-casa bonus"><b>${Math.abs(m.mod)}</b><i>bônus</i></span><span class="d20m-op">=</span>
            <span class="d20m-casa total"><b>?</b><i>total</i></span><span class="d20m-op contra">contra</span>
            <span class="d20m-casa cd"><b>${m.cd}</b><i>dificuldade</i></span>
          </div>
          <span class="rc-precisa">${rolagemPrecisa(m)}</span>${det ? `<span class="rc-partes">${det}</span>` : ""}
        </div>
        <div class="rc-resultado rc-faixa">${ROLAGEM_CONTORNO}<b></b></div>
        <div class="d20-regra"></div>
      </div>`;
  }
  function htmlVidro(m) {
    const det = rolagemPartes(m);
    return `<div class="rc-veu"></div>
      <div class="rc-grupo d20-grupo">
        <div class="rc-cab"><span class="rc-nome">Teste de ${esc(m.atributo)}</span></div>
        <div class="d20v-linha">
          <div class="rc-faixa d20v-placa esquerda">${ROLAGEM_CONTORNO}
            <i class="rot">bônus</i><b class="valor">${sinal(m.mod)}${Math.abs(m.mod)}</b>
            <span class="sub">somado ao d20</span>
          </div>
          <div class="d20-dado"></div>
          <div class="rc-faixa d20v-placa direita">${ROLAGEM_CONTORNO}
            <i class="rot">dificuldade</i><b class="valor">${m.cd}</b><span class="sub">${rolagemPrecisa(m)}</span>
          </div>
        </div>
        ${det ? `<span class="rc-partes d20v-partes">${det}</span>` : ""}
        <div class="rc-resultado rc-faixa">${ROLAGEM_CONTORNO}<b></b></div>
        <div class="d20-regra"></div>
      </div>`;
  }

  /** A tirinha do texto com o dado pequeno (a mesma de hoje, com o dado da proposta). */
  function tirinha(m, mat, centro) {
    const sn = sinal(m.mod), abs = Math.abs(m.mod);
    const caixa = el("div", `rolagem rolando d20p-tirinha${centro ? " rc-guardada" : ""}`);
    caixa.innerHTML = `<div class="d20-mini"></div><div class="rol-info"><div class="rol-attr">Teste de ${esc(m.atributo)}</div>
      <div class="rol-conta">d20 ${sn} ${abs} contra dificuldade <b>${m.cd}</b></div></div><div class="rol-res"></div>`;
    const cv = tela(mat, "tirinha");
    caixa.querySelector(".d20-mini").appendChild(cv);
    return { caixa, cv };
  }

  async function rolagemProposta(m) {
    const mat = MAT[qual], sn = sinal(m.mod), abs = Math.abs(m.mod);
    const centro = !(replay || instantaneo() || (estado && estado.combate));
    const { caixa, cv: mini } = tirinha(m, mat, centro);
    anexar(caixa);
    const r = rolagemResultado(m), est = estadoDe(m), regra = regraEspecial(m);
    let quadro = 0;
    const girarMini = (n) => desenhar(mini, mat, "tirinha", reduzido() ? { n, estado: "rolando" } : { quadro: quadro, n: mat === "vidro" ? n : null, estado: "rolando" });
    const fecharTirinha = () => {
      desenhar(mini, mat, "tirinha", { n: m.d20, estado: est });
      caixa.classList.remove("rolando");
      caixa.classList.add(...r.classes);
      caixa.querySelector(".rol-conta").innerHTML = `<b>${m.d20}</b> ${sn} ${abs} = <b>${m.total}</b> contra <b>${m.cd}</b>`;
      caixa.querySelector(".rol-res").textContent = r.nome;
      historico("h-chip", `▸ ${m.atributo} ${m.total} contra ${m.cd} — ${m.sucesso ? "sucesso" : "falha"} (d20 ${m.d20})`);
    };
    girarMini(1 + Math.floor(Math.random() * 20));

    if (!centro) {  // a tirinha sozinha, como hoje (a luta, o texto instantâneo, refazendo a página)
      if (!instantaneo()) {
        Som.tocar("dado");
        const fim = performance.now() + 950;
        while (performance.now() < fim && !pular) { quadro++; girarMini(1 + Math.floor(Math.random() * 20)); await espera(60); }
      }
      fecharTirinha();
      if (!replay) Som.tocar(r.critico ? "critico" : m.sucesso ? "sucesso" : "falha");
      if (!instantaneo()) await espera(ritmo(650));
      return;
    }

    const p = $("#palco").getBoundingClientRect(), c = ($("#cena") || $("#palco")).getBoundingClientRect();
    const palco = el("div", `rolagem-centro d20-pixel d20-${qual}`);
    palco.innerHTML = qual === "marfim" ? htmlMarfim(m) : htmlVidro(m);
    const veu = palco.querySelector(".rc-veu"), grupo = palco.querySelector(".rc-grupo");
    const cv = tela(mat, "centro"), lugar = palco.querySelector(".d20-dado");
    lugar.appendChild(cv);
    Object.assign(veu.style, { left: p.left + "px", top: p.top + "px", width: p.width + "px", height: p.height + "px" });
    document.body.appendChild(palco);
    grupo.style.left = Math.round(p.left + p.width / 2 - grupo.offsetWidth / 2) + "px";
    grupo.style.top = Math.round(Math.max(8, Math.min(innerHeight - grupo.offsetHeight - 8, c.top + c.height / 2 - grupo.offsetHeight / 2))) + "px";
    const gr = grupo.getBoundingClientRect();
    veu.style.setProperty("--cx", `${((gr.left + gr.width / 2 - p.left) / p.width) * 100}%`);
    veu.style.setProperty("--cy", `${((gr.top + gr.height / 2 - p.top) / p.height) * 100}%`);
    palco.classList.add("rc-entra", "rolando");

    // a rolagem: o mesmo som e os mesmos 950 ms; o dado tomba (A) ou tomba com o número aceso por dentro (B)
    const girar = () => {
      const n = 1 + Math.floor(Math.random() * 20);  // enfeite, como hoje: o que pousa é o d20 do motor
      if (reduzido()) desenhar(cv, mat, "centro", { n, estado: "rolando" });
      else desenhar(cv, mat, "centro", { quadro, n: mat === "vidro" ? n : null, estado: "rolando" });
      girarMini(n);
    };
    Som.tocar("dado");
    girar();
    const fim = performance.now() + 950;
    while (performance.now() < fim && !pular) { await espera(60); quadro++; girar(); }

    // o resultado: o d20 do motor
    desenhar(cv, mat, "centro", { n: m.d20, estado: est });
    palco.classList.remove("rolando");
    palco.classList.add(...r.classes, `d20-${est}`);
    if (qual === "marfim") {
      palco.querySelector(".d20m-casa.dado b").textContent = m.d20;
      palco.querySelector(".d20m-casa.total b").textContent = m.total;
    } else {
      const esq = palco.querySelector(".d20v-placa.esquerda");
      esq.querySelector(".rot").textContent = "total";
      esq.querySelector(".valor").textContent = m.total;
      esq.querySelector(".sub").innerHTML = `${m.d20} no dado ${sn} ${abs}`;
    }
    palco.querySelector(".rc-resultado b").textContent = r.nome;
    palco.querySelector(".d20-regra").textContent = regra;
    if (!pular) pouso(lugar, mat, est);
    fecharTirinha();
    Som.tocar(r.critico ? "critico" : m.sucesso ? "sucesso" : "falha");

    // o resultado fica à vista o tempo de sempre; o fim dele é a descida até a tirinha (pular corta)
    const resto = ritmo(650), saida = reduzido() ? 0 : Math.min(220, Math.round(resto * 0.34));
    for (const f = performance.now() + resto - saida; performance.now() < f && !pular;) await espera(Math.min(40, f - performance.now()));
    if (saida && !pular) {
      const a = grupo.getBoundingClientRect(), b = caixa.getBoundingClientRect();
      const dx = b.left + b.width / 2 - (a.left + a.width / 2), dy = b.top + b.height / 2 - (a.top + a.height / 2);
      const s = Math.max(0.3, Math.min(1, b.width / a.width));
      grupo.animate([{ transform: "none", opacity: 1 }, { transform: `translate(${dx}px, ${dy}px) scale(${s})`, opacity: 0 }],
        { duration: saida, easing: "cubic-bezier(.5,0,.8,.4)", fill: "forwards" });
      veu.animate([{ opacity: 1 }, { opacity: 0 }], { duration: saida, fill: "forwards" });
      setTimeout(() => caixa.classList.remove("rc-guardada"), saida * 0.6);
      await espera(saida);
    }
    caixa.classList.remove("rc-guardada");
    palco.remove();
  }

  /* ---------------------------------------------------------------- a ficha (o ícone dos Testes do d20) */
  const icones = {};
  /** O ícone dos Testes do d20 na ficha: o SVG de sempre no Clássico; nos outros, o dado pequeno (22 px, 1×). */
  function icone() {
    if (!qual) return D20;
    if (!icones[qual]) { const cv = tela(MAT[qual], "ficha"); desenhar(cv, MAT[qual], "ficha"); icones[qual] = cv.toDataURL(); }
    return `<img class="d20p d20p-ficha" src="${icones[qual]}" width="22" height="22" alt="">`;
  }

  /** Usa a apresentação `nome` ("classico", "marfim" ou "vidro"; outra coisa vale o Clássico) e guarda a escolha: no
   *  navegador e no disco, pelo jogo (a porta muda a cada abertura, e o armazenamento do navegador com ela). A
   *  guardada no disco chega na abertura, pela /config (controles.js). */
  function usar(nome, guardarEscolha = true) {
    qual = MAT[nome] ? nome : "";
    if (guardarEscolha) {
      guardar(PREF, qual || "classico");
      preferir("d20", qual || "classico");
    }
    document.documentElement.classList.toggle("d20-usa-marfim", qual === "marfim");
    document.documentElement.classList.toggle("d20-usa-vidro", qual === "vidro");
    document.querySelectorAll(".testes-ficha .d20").forEach((s) => { s.innerHTML = icone(); });
    return qual || "classico";
  }
  window.rolagem = (m) => (qual ? rolagemProposta(m) : rolagemClassica(m));
  usar(ler(PREF), false);

  return { usar, icone, desenhar, tela, algarismos, OPCOES, get atual() { return qual || "classico"; } };
})();
