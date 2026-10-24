// As faixas de passagem, duas direções (protótipo, 24/10/2026; nada no jogo). Entra na página só pela demonstração
// (auxiliares/cenarios_faixas.py), depois de telas/celebracoes.js.
//
// O jogo continua fazendo tudo o que faz hoje: o Telas.celebrar de sempre roda inteiro (os mesmos tempos, os sons, a
// ordem, a queda com a carta caindo e o escuro). Daqui só sai o DESENHO: quando a celebração põe a faixa antiga
// (.faixa-festa) na página, ela é trocada, no mesmo instante, pela da proposta, com os dados da mensagem; e as
// partículas antigas da Vitória saem (cada proposta tem os efeitos dela). Nenhuma espera é acrescentada: a faixa nova
// some no fim do tempo que a celebração já segura a fila.
//
//   FaixasProto.usar("a")   A · a faixa integrada ao palco: horizontal, contida no palco, base escura de beiras rasgadas
//   FaixasProto.usar("b")   B · emblema e anúncio: uma placa compacta, o símbolo e o título no centro
//
// Os quatro pesos (a mesma regra nas duas): "comum" (a Vitória: curta, boa de repetir), "marco" (o Guardião, o Mestre
// caçador, quem se junta à comitiva: mais presença), "peso" (Você caiu ou morreu, Exausto: sem cara de festa) e
// "passagem" (Saindo da capela: discreta).
(() => {
  const { h } = Telas;
  const original = Telas.celebrar;
  const TIPOS = ["vitoria", "derrota", "mestre", "exausto", "retirada", "comitiva"];
  // quanto a celebração de hoje segura a fila (telas/celebracoes.js): a faixa nova vive esse tempo e sai
  const SEGURA = { vitoria: 1000, guardiao: 1500, mestre: 1800, exausto: 2300, retirada: 2600, comitiva: 1500, derrota: 2200 };
  const SAIDA = { comum: 260, marco: 340, peso: 520, passagem: 360 };
  let versao = "a", atual = null;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;

  /** O que a faixa diz e o peso dela, pelos dados que o motor manda (os mesmos da faixa de hoje). */
  function ler(m) {
    const d = m.dados || {};
    if (m.tipo === "vitoria") return d.chefe
      ? { peso: "marco", chave: "guardiao", titulo: "Guardião derrotado!", icone: Icones.item("espada", 48) }
      : { peso: "comum", chave: "vitoria", titulo: "Vitória", icone: Icones.item("espada", 48) };
    if (m.tipo === "mestre") return { peso: "marco", chave: "mestre", titulo: "Mestre caçador",
      sub: `${d.plural.charAt(0).toUpperCase() + d.plural.slice(1)}: +10% de dano contra eles`,
      icone: Icones.criatura(d.retrato, 48) };
    if (m.tipo === "comitiva") return { peso: "marco", chave: "comitiva", titulo: `${d.nome} se junta a você`, sub: d.titulo,
      icone: Icones.cabeca(d.id, 48) };
    if (m.tipo === "derrota") return { peso: "peso", tom: "sangue", chave: "derrota", titulo: d.morte ? "Você morreu" : "Você caiu" };
    if (m.tipo === "exausto") return { peso: "peso", tom: "cinza", chave: "exausto", titulo: "Exausto", sub: d.texto };
    if (m.tipo === "retirada") return d.exausto
      ? { peso: "peso", tom: "cinza", chave: "retirada", titulo: "Exausto", sub: d.texto }
      : { peso: "passagem", chave: "retirada", titulo: "Saindo da capela", sub: d.texto, icone: Icones.atalho("Sair", 32) };
    return null;
  }

  /** O palco: a coluna do meio (sem as laterais), e a altura da arte do topo (onde a faixa se apoia). */
  function palco() {
    const c = document.getElementById("cena").getBoundingClientRect(), v = document.getElementById("vista").getBoundingClientRect();
    return { x: c.left, w: c.width, topo: c.top, base: c.bottom, meio: v.height > 40 ? v.top + v.height * 0.5 : c.top + c.height * 0.32 };
  }

  /** O maior tamanho inteiro da letra de título (64, 48, 32: cada pixel da letra cai inteiro) que cabe em `largura`. */
  function tamanhoTitulo(texto, largura, maior) {
    const m = document.createElement("b");
    m.className = "fx-medida";
    m.textContent = texto;
    document.body.appendChild(m);
    let t = 32;
    for (const s of [64, 48, 32]) {
      if (s > maior) continue;
      m.style.fontSize = s + "px";
      if (m.getBoundingClientRect().width <= largura) { t = s; break; }
    }
    m.remove();
    return t;
  }

  // ------------------------------------------------------------------ A · a faixa integrada ao palco
  // As beiras de cima e de baixo, rasgadas à mão (desníveis em múltiplos de 3 px, a grade dos pixels), e as pontas
  // abertas que se desfazem em degraus. O perfil se repete ao longo da faixa, sem sorteio.
  const CIMA = [0, 3, 0, 0, 6, 3, 0, 3, 9, 3, 0, 0, 6, 0, 3, 0];
  const BAIXO = [3, 0, 6, 3, 0, 0, 3, 9, 3, 0, 6, 3, 0, 3, 0, 6];
  // as pontas, de cima para baixo: o quanto cada degrau recua para dentro (a esquerda e a direita diferentes)
  const PONTA_E = [18, 6, 12, 0, 9, 3, 15, 6, 21];
  const PONTA_D = [9, 21, 3, 12, 0, 15, 6, 18, 3];
  function contornoA(w, hgt, r = 0) {
    const pts = [], passo = 24, n = PONTA_E.length - 1;
    for (let x = 24; x <= w - 24; x += passo) pts.push([x, CIMA[(x / passo | 0) % CIMA.length] + r]);
    for (let i = 0; i <= n; i++) pts.push([w - PONTA_D[i] - r, r + ((hgt - 2 * r) * i) / n]);
    for (let x = w - 24; x >= 24; x -= passo) pts.push([x, hgt - BAIXO[(x / passo | 0) % BAIXO.length] - r]);
    for (let i = n; i >= 0; i--) pts.push([PONTA_E[i] + r, r + ((hgt - 2 * r) * i) / n]);
    return `polygon(${pts.map(([x, y]) => `${Math.round(x / 3) * 3}px ${Math.round(y / 3) * 3}px`).join(",")})`;
  }

  function desenharA(f, pal) {
    const larguraTexto = Math.min(pal.w * (f.peso === "passagem" ? 0.7 : 0.82), 900);
    const maior = f.peso === "marco" ? 64 : f.peso === "passagem" ? 32 : f.peso === "peso" ? 64 : 48;
    const t = tamanhoTitulo(f.titulo, larguraTexto - (f.icone ? 64 : 0), maior);
    const el = document.createElement("div");
    el.className = `fx-faixa fa peso-${f.peso} ${f.tom ? "tom-" + f.tom : ""}`;
    el.setAttribute("role", "status");
    el.innerHTML = `<div class="fa-borda"></div><div class="fa-base"></div>
      <div class="fa-corpo"><div class="fa-linha">${f.icone ? `<span class="fa-icone">${f.icone}</span>` : ""}<b class="fa-titulo" style="font-size:${t}px">${h(f.titulo)}</b></div>
      ${f.sub ? `<div class="fa-sub">${h(f.sub)}</div>` : ""}</div>`;
    document.body.appendChild(el);
    const largura = f.peso === "passagem" ? Math.min(pal.w * 0.78, 720) : f.peso === "comum" ? Math.min(pal.w * 0.62, 620) : Math.min(pal.w * 0.92, 980);
    el.style.width = largura + "px";
    el.style.left = Math.round(pal.x + (pal.w - largura) / 2) + "px";
    const alt = el.getBoundingClientRect().height;
    el.style.top = Math.round(f.peso === "passagem" ? Math.min(pal.base - alt - 24, pal.meio + 30) : Math.max(pal.topo + 8, pal.meio - alt / 2)) + "px";  // nunca acima do palco (a barra da vida)
    el.querySelector(".fa-borda").style.clipPath = contornoA(largura, alt);
    el.querySelector(".fa-base").style.clipPath = contornoA(largura, alt, 3);
    return el;
  }

  // ------------------------------------------------------------------ B · emblema e anúncio
  function desenharB(f, pal) {
    const maior = f.peso === "marco" ? 64 : f.peso === "peso" ? 64 : f.peso === "passagem" ? 32 : 48;
    const t = tamanhoTitulo(f.titulo, Math.min(pal.w * 0.8, 760), maior);
    const emblema = f.icone && f.peso !== "passagem" ? `<div class="fb-emblema"><div class="fb-joia">${f.icone}</div></div>` : "";
    const el = document.createElement("div");
    el.className = `fx-faixa fb peso-${f.peso} ${f.tom ? "tom-" + f.tom : ""}`;
    el.setAttribute("role", "status");
    el.innerHTML = `${emblema}<div class="fb-placa"><div class="fb-dentro">
      <b class="fb-titulo" style="font-size:${t}px">${f.peso === "passagem" && f.icone ? `<span class="fb-icone">${f.icone}</span>` : ""}${h(f.titulo)}</b>
      ${f.sub ? `<div class="fb-sub">${h(f.sub)}</div>` : ""}</div></div>`;
    document.body.appendChild(el);
    el.style.maxWidth = Math.min(pal.w * 0.86, 820) + "px";
    const r = el.getBoundingClientRect();
    el.style.left = Math.round(pal.x + (pal.w - r.width) / 2) + "px";
    el.style.top = Math.round(f.peso === "passagem" ? Math.min(pal.base - r.height - 24, pal.meio + 30) : Math.max(pal.topo + 8, pal.meio - r.height / 2 + (emblema ? 10 : 0))) + "px";  // nunca acima do palco
    return el;
  }

  // ------------------------------------------------------------------ os efeitos (FX das celebrações, só lidos)
  // Num palco de pixel recortado na coluna do meio: nada passa por cima das laterais.
  function efeitos(f, el, pal, vida) {
    if (reduzido() || f.peso === "passagem") return;
    const p = FX.palco(document.body, { z: 38, classe: "fx-faixa-palco" });
    p.el.style.clipPath = `inset(${pal.topo}px ${innerWidth - pal.x - pal.w}px ${innerHeight - pal.base}px ${pal.x}px)`;  // só o palco
    const alvo = el.querySelector(".fa-titulo, .fb-joia, .fb-titulo"), c = p.de(alvo), placa = p.de(el);
    const ouro = FX.PALETAS.ouro, cinza = ["w", "G", "g", "d"], brasa = ["y", "O", "o", "r"];
    const fx = FX.enxame();
    if (f.peso === "comum") {  // a Vitória: um estalo curto de faíscas a partir do título
      fx.soltar(14, (i) => { const a = (i / 14) * Math.PI * 2; return { x: c.x, y: c.y, vx: Math.cos(a) * 3.2, vy: Math.sin(a) * 1.8 - 0.6, g: 0.12, arrasto: 0.86, vida: 9, desenho: i % 3 ? "ponto" : "cruz", pal: ouro }; });
    } else if (f.peso === "marco") {  // mais presença: os raios atrás, o anel da entrada e as faíscas subindo
      fx.soltar(26, (i) => ({ x: placa.esq + ((i * 37) % Math.max(1, placa.dir - placa.esq)), y: placa.base, vx: ((i % 5) - 2) * 0.15, vy: -0.8 - (i % 4) * 0.25, g: -0.01, arrasto: 0.99, vida: 16 + (i % 7), desenho: i % 4 ? "ponto" : "brilho", pal: ouro, piscar: i % 3 === 0 }));
    } else {  // o peso: cinza que cai devagar, sem brilho; na queda, a cinza é de brasa apagando
      fx.soltar(22, (i) => ({ x: placa.esq + ((i * 53) % Math.max(1, placa.dir - placa.esq)), y: placa.topo - 4 - (i % 6) * 3, vx: ((i % 3) - 1) * 0.12, vy: 0.35 + (i % 4) * 0.1, g: 0, arrasto: 1, vida: 26 + (i % 9), desenho: i % 5 ? "ponto" : "duplo", pal: f.tom === "sangue" ? brasa : cinza }));
    }
    const pernas = FX.animar(p, (t) => {
      if (f.peso === "marco") {
        const vis = Math.round(16 * FX.rampa(t, 0, 220) * (1 - FX.rampa(t, vida - 380, 300)));
        FX.raios(p, { cx: c.x, cy: c.y, n: 14, ang: t / 1600, larg: 0.42, r0: 4, r1: Math.max(placa.ry * 2.2, 40), pal: ouro, vis, achata: 0.55 });
        if (t < 420) FX.anel(p, { cx: c.x, cy: c.y, r: Math.round(6 + FX.rampa(t, 0, 420) * placa.rx * 0.9), esp: 2, pal: ouro, achata: 0.5, vis: Math.round(16 * (1 - t / 420)) });
      }
      if (f.peso === "peso") FX.poco(p, { cx: placa.x, cy: placa.y, rx: placa.rx * 1.3, ry: placa.ry * 2.2, forca: Math.round(10 * FX.rampa(t, 0, 400) * (1 - FX.rampa(t, vida - 400, 380))), c: "N" });
      fx.passo(); fx.desenhar(p);
    });
    setTimeout(() => { pernas.parar(); p.el.remove(); }, vida + 80);
  }

  function mostrar(m) {
    const f = ler(m);
    if (!f) return;
    const pal = palco(), vida = SEGURA[f.chave] || 1500;
    document.querySelectorAll(".fx-faixa").forEach((e) => e.remove());
    const el = versao === "b" ? desenharB(f, pal) : desenharA(f, pal);
    el.dataset.chave = f.chave;
    if (!reduzido()) el.classList.add("entra");
    efeitos(f, el, pal, vida);
    const saida = reduzido() ? 0 : SAIDA[f.peso];
    el.style.setProperty("--saida", saida + "ms");
    setTimeout(() => el.classList.add("sai"), Math.max(0, vida - saida));
    setTimeout(() => el.remove(), vida + (reduzido() ? 0 : 60));
  }

  // a troca: a faixa antiga nasce e sai no mesmo instante, a nova entra no lugar dela
  new MutationObserver((ms) => {
    for (const r of ms) for (const n of r.addedNodes) {
      if (!(n instanceof HTMLElement) || !atual) continue;
      if (n.classList.contains("faixa-festa")) { n.remove(); mostrar(atual); }
      else if (n.classList.contains("particula") && atual.tipo === "vitoria") n.remove();
    }
  }).observe(document.body, { childList: true });

  window.FaixasProto = {
    usar(v) {
      versao = v;
      document.documentElement.dataset.faixas = v;
      Telas.celebrar = (m, instantaneo) => { atual = TIPOS.includes(m.tipo) ? m : null; return original(m, instantaneo); };
    },
    versao: () => versao,
    ler,
  };
})();
