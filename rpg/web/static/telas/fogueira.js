/* Fogueira: a cena do acampamento em pixel art, com a comitiva em roda e os nomes que se acomodam sozinhos. */
"use strict";

(() => {
  const { h, S, ligarFigurasComitiva } = Telas;

  // Em roda, colados no fogo (o herói em 128,93, o fogo em 160): quem vai com você do outro lado e na frente, o animal
  // deitado ao lado do herói, quem fica no acampamento perto da barraca. Os nomes se acomodam sozinhos (acomodarNomes).
  const HEROI_FOGUEIRA = [128, 93];
  const PONTOS_ATIVOS = [[198, 93], [176, 104]];
  const PONTOS_RESERVA = [[256, 98], [284, 102], [270, 108]];
  const PONTO_FERA = [108, 104];
  function acampamento(d) {
    const figuras = [];
    d.ativos.forEach((m, i) => figuras.push({ ...m, onde: "ativo", p: PONTOS_ATIVOS[i % 2] }));
    d.reserva.forEach((m, i) => figuras.push({ ...m, onde: "reserva", p: PONTOS_RESERVA[i % 3] }));
    // O nome logo acima da cabeça (moldura de ouro: vai com você amanhã; cinza: fica no acampamento) e o ✉ preso no
    // canto do nome, sem ocupar uma linha a mais. Sem dica no passar do mouse: o que ela dizia (vai com você, fica no
    // acampamento, a vida do animal) está no menu que abre no clique.
    const botoes = figuras.map((f) => `<button type="button" class="figura ${f.onde}${f.conversa ? " tem-conversa" : ""}" data-cid="${h(f.id)}"
        style="left:${(f.p[0] / 320) * 100}%;top:${((f.p[1] + 8) / 120) * 100}%">
        <span class="figura-nome">${h(f.nome.split(" ").pop())}${f.conversa ? '<i class="carta-aviso">✉</i>' : ""}</span></button>`).join("");
    const fera = d.fera ? `<span class="figura fera" role="button" tabindex="0" data-fera="1" style="left:${(PONTO_FERA[0] / 320) * 100}%;top:${((PONTO_FERA[1] + 8) / 120) * 100}%">
        <span class="figura-nome">${h(d.fera.nome.split(" ").pop())}</span></span>` : "";
    // Dormir: um selo que balança de leve dentro do palco (o fim da noite fica na cena, não numa lista). Mora no céu,
    // no canto de cima: em cima da barraca ele encostava no nome de quem senta ali perto.
    const dormir = `<button type="button" class="dormir-barraca">${S("lua", 1)} Dormir até o amanhecer</button>`;
    return `<div class="tela acampamento">${d.intro ? `<p class="sussurro">${h(d.intro)}</p>` : ""}<div class="fogueira-palco"><canvas class="fogueira-cena" width="320" height="120"></canvas>${botoes}${fera}${dormir}</div>
      <div class="dica-uso">${figuras.length ? `Clique em alguém para conversar ou decidir quem vai com você amanhã (nome com moldura de ouro). Quem fica no acampamento descansa, não come das suas provisões e não opina nas suas escolhas. ${d.ativos.length}/${d.limite} na comitiva.` : "Só você, o fogo e os barulhos da mata. Quem você encontrar pelo caminho pode se sentar aqui um dia."}</div></div>`;
  }

  function desenharFogueira(canvas, d) {
    const x = canvas.getContext("2d");
    const W = 320, H = 120;
    const px = (cx, cy, w, hh, cor) => { x.fillStyle = cor; x.fillRect(cx | 0, cy | 0, w, hh); };
    const heroi = App.estado && App.estado.heroi;
    const quem = [[heroi ? heroi.classe : "guerreiro", ...HEROI_FOGUEIRA]];
    d.ativos.forEach((m, i) => quem.push([m.id, ...PONTOS_ATIVOS[i % 2]]));
    d.reserva.forEach((m, i) => quem.push([m.id, ...PONTOS_RESERVA[i % 3]]));
    if (d.fera) quem.push([d.fera.tipo === "falcao" ? "voador" : "fera", ...PONTO_FERA]);
    let quadro = 0, timer = null;
    function cena(primeira) {
      if (!primeira && !canvas.isConnected) { clearInterval(timer); return; }  // a tela saiu: para de animar
      quadro++;
      // O céu vem da arte da paisagem em 320x72, que anda mesmo escondida; o canvas da página fica parado enquanto
      // a fogueira está na tela (copiado dele, a chuva congelava).
      const ceu = typeof Vista !== "undefined" && Vista.arte();
      if (ceu) x.drawImage(ceu, 0, 0, W, 72); else px(0, 0, W, 72, "#080b1a");
      // chão escuro com pontilhado
      for (let y = 72; y < H; y++) px(0, y, W, 1, y < 76 ? "#14100c" : "#0d0b09");
      for (let y = 78; y < H; y += 2) for (let i = (y * 7) % 5; i < W; i += 5) px(i, y, 1, 1, "#1a140f");
      // luz da fogueira: anéis pontilhados que tremem
      const raio = 46 + Math.sin(quadro / 2) * 2 + (Math.random() * 2);
      for (let y = 74; y < H; y++) for (let i = 80; i < 240; i++) {
        const dx = (i - 160) / raio, dy = (y - 98) / (raio * 0.45), d2 = dx * dx + dy * dy;
        if (d2 < 1 && ((i + y) % 2 === 0 || d2 < 0.45)) px(i, y, 1, 1, d2 < 0.2 ? "#5a2e12" : d2 < 0.5 ? "#3a2010" : "#24160c");
      }
      // barraca do acampamento
      for (let k = 0; k < 18; k++) px(262 - k, 80 + k, k * 2 + 1 > 36 ? 36 : 1, 1, "#2a2016");
      for (let k = 0; k < 18; k++) { px(262 - k, 80 + k, 1, 1, "#4a3a28"); px(262 + k, 80 + k, 1, 1, "#4a3a28"); px(263 - k, 80 + k, k * 2 - 1 > 0 ? k * 2 - 1 : 0, 1, "#1a140e"); }
      px(259, 90, 6, 8, "#0d0b0a");
      // toras e fogo
      px(148, 100, 24, 3, "#4a2c14"); px(152, 98, 16, 2, "#5a3a1c");
      for (let i = 0; i < 9; i++) {
        const fx = 150 + i * 2.4, alt = 6 + Math.random() * 10 + (i > 2 && i < 7 ? 6 : 0);
        px(fx, 98 - alt, 2, alt, "#b3262b"); px(fx, 98 - alt * 0.75, 2, alt * 0.75, "#e0782f");
        if (i > 1 && i < 8) px(fx, 98 - alt * 0.45, 2, alt * 0.45, "#ffd27a");
      }
      for (let i = 0; i < 4; i++) {  // fagulhas e fumaça
        const t = (quadro * 2 + i * 13) % 40;
        px(158 + Math.sin((quadro + i * 7) / 3) * 4, 80 - t, 1, 1, t < 20 ? "#ffb35c" : "rgba(160,150,140,0.5)");
      }
      // figuras, iluminadas pelo fogo
      quem.forEach(([nomeSpr, fx, fy]) => {
        const spr = Sprites.canvas(nomeSpr);
        px(fx - 7, fy + 6, 14, 2, "rgba(0,0,0,0.5)");
        if (spr) x.drawImage(spr, fx - 8, fy - 9, 16, 16);
      });
    }
    cena(true);
    timer = setInterval(() => { if (!document.hidden) cena(); }, 125);
  }

  /** Os nomes de quem senta em volta do fogo, pequenos, cada um onde couber: acima da cabeça, ao lado ou embaixo da
   *  figura, sem cobrir outro nome, outra figura, o fogo nem o "Dormir" (como os balões da luta). Assim a roda fica
   *  colada no fogo e ninguém precisa sentar longe para o nome caber. */
  function acomodarNomes(raiz) {
    const palco = raiz.querySelector(".fogueira-palco");
    if (!palco) return;
    const P = palco.getBoundingClientRect(), esc = P.width / 320;
    const ret = (x, y, w, h) => ({ l: x, t: y, r: x + w, b: y + h });
    const daArte = (x, y, w, h) => ret(x * esc, y * esc, w * esc, h * esc);
    const relativo = (r) => ret(r.left - P.left, r.top - P.top, r.width, r.height);
    const area = (a, b) => Math.max(0, Math.min(a.r, b.r) - Math.max(a.l, b.l)) * Math.max(0, Math.min(a.b, b.b) - Math.max(a.t, b.t));
    const figuras = [...palco.querySelectorAll(".figura")];
    const obstaculos = [
      daArte(HEROI_FOGUEIRA[0] - 8, HEROI_FOGUEIRA[1] - 9, 16, 16),  // o herói
      daArte(146, 78, 28, 26),                                          // o fogo
      ...figuras.map((f) => relativo(f.getBoundingClientRect())),
    ];
    const dormir = palco.querySelector(".dormir-barraca");
    if (dormir) obstaculos.push(relativo(dormir.getBoundingClientRect()));
    figuras.forEach((f) => {
      const nome = f.querySelector(".figura-nome");
      if (!nome) return;
      const s = relativo(f.getBoundingClientRect()), w = nome.offsetWidth, h = nome.offsetHeight, cx = (s.l + s.r) / 2;
      const opcoes = [
        ret(cx - w / 2, s.t - h - 2, w, h),          // acima da cabeça
        ret(cx - w / 4, s.t - h - 2, w, h),          // acima, puxado para a direita
        ret(cx - (3 * w) / 4, s.t - h - 2, w, h),    // acima, puxado para a esquerda
        ret(s.r + 2, s.t + 2, w, h),                 // à direita, na altura dos ombros
        ret(s.r + 2, s.b - h, w, h),                 // à direita, na altura dos pés
        ret(s.l - w - 2, s.t + 2, w, h),             // à esquerda
        ret(s.l - w - 2, s.b - h, w, h),
        ret(cx - w / 2, s.b + 1, w, h),              // embaixo
      ];
      const dentro = (c) => c.l >= 2 && c.t >= 2 && c.r <= P.width - 2 && c.b <= P.height - 2;
      const custo = (c) => (dentro(c) ? 0 : 1e6) + obstaculos.reduce((n, o) => n + (o === s ? 0 : area(c, o)), 0);
      const livre = opcoes.find((c) => custo(c) === 0) || opcoes.reduce((m, c) => (custo(c) < custo(m) ? c : m));
      nome.classList.add("posto");
      nome.style.left = livre.l - s.l + "px";
      nome.style.top = livre.t - s.t + "px";
      obstaculos.push(livre);
    });
  }

  Telas.registrar("acampamento", acampamento, {
    ligar: (raiz, d) => {
      App.ultimaFogueira = d;
      desenharFogueira(raiz.querySelector(".fogueira-cena"), d);
      requestAnimationFrame(() => acomodarNomes(raiz));
      ligarFigurasComitiva(raiz);
    },
  });
})();
