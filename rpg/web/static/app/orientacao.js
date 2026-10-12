/* As orientações da abertura guiada (abertura.py; roadmapIDEIAS/18): um quadro pequeno junto do controle, com uma
   seta discreta, um anel em volta do controle e um véu leve só nas colunas laterais e na doca. O motor diz qual
   orientação vale e o texto; aqui só se acha o controle na tela e se desenha. Nada bloqueia clique nem tecla: o
   quadro some quando a ação acontece. Na luta, os passos C1–C4 seguem o que está na tela (a roda, a janelinha de
   Habilidades, a mira e o golpe dado). A Ajuda (F1, no topo) lista o que já foi visto e liga ou desliga. */
"use strict";

const Orientacao = (() => {
  let quadro = null, anel = null, veus = [], dispensado = false;
  let luta = null;          // a luta de agora: { c4: id da habilidade usada, feito }
  let quadroAtual = "";     // o que o quadro mostra (para não refazer o HTML a cada quadro de animação)
  const texto = (s) => Texto.html(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>");
  const visivel = (e) => { if (!e) return false; const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };

  function montar() {
    if (quadro) return;
    quadro = el("div", "orientacao", "");
    quadro.setAttribute("role", "note");
    anel = el("div", "orientacao-anel", "");
    for (let k = 0; k < 3; k++) veus.push(el("div", "orientacao-veu", ""));
    [...veus, anel, quadro].forEach((x) => { x.hidden = true; document.body.appendChild(x); });
    quadro.addEventListener("click", (ev) => {
      if (!ev.target.closest(".orientacao-dispensar")) return;
      ev.stopPropagation();
      dispensado = true;  // some na hora; o motor confirma no próximo estado
      enviar("dispensar");
      esconder();
    });
  }

  function enviar(acao) {
    fetch("/orientacao", { method: "POST", headers: { "Content-Type": "application/json", "X-Token": TOKEN },
      body: JSON.stringify({ acao }) }).catch((e) => console.error(e));
  }

  function esconder() {
    if (!quadro) return;
    [...veus, anel, quadro].forEach((x) => { x.hidden = true; });
    quadroAtual = "";
  }

  /** O passo de agora e o controle a apontar, ou null. */
  function alvo() {
    const o = estado && estado.orientacao && estado.orientacao.atual;
    if (!o || dispensado || !estado.orientacao.ligado) return null;
    if (document.querySelector(".sobreposicao:not([hidden]), #sobre-achado:not([hidden]), #janela-confirmar")) return null;
    if (o.id === "combate") {
      if (!estado.combate || !luta || luta.feito) return null;
      const p = o.passos;
      if (luta.c4) {
        const barra = document.querySelector('#arena .carta[data-uid="j"] .carta-rec');
        return visivel(barra) ? { el: barra, html: p.C4[luta.c4] || "", lado: "arena", veu: true } : null;
      }
      const linha = document.querySelector(`.roda-janela .rj-linha[data-hab="${o.hab}"]`) || document.querySelector(".roda-janela .rj-linha[data-hab]");
      if (visivel(linha)) return { el: linha, html: p.C2, lado: "direita", veu: true };
      const mira = document.querySelector("#arena .carta.alvejavel");
      if (visivel(mira)) return { el: mira, html: p.C3, lado: "arena", veu: true };
      const hab = document.querySelector('#roda .roda-botao[data-slot="habilidades"]');
      if (visivel(hab) && pergunta) return { el: hab, html: p.C1, lado: "arena", veu: true };
      return null;
    }
    if (o.id === "V1") {
      const mural = document.querySelector('#predios .predio[data-predio="mural"]');
      if (!visivel(mural) || !pergunta || estado.combate) return null;
      return { el: mural, html: o.texto, lado: "baixo", veu: true };
    }
    return null;
  }

  /** Quadro, seta, anel e véu em volta do controle (a cada quadro de animação: a tela muda de tamanho e lugar). */
  function desenhar() {
    const a = alvo();
    if (!a) { esconder(); return; }
    montar();
    const html = `<div class="orientacao-texto">${texto(a.html)}</div><button type="button" class="orientacao-dispensar">Dispensar orientações</button>`;
    if (html !== quadroAtual) { quadro.innerHTML = html; quadroAtual = html; }
    const r = a.el.getBoundingClientRect();
    anel.hidden = quadro.hidden = false;
    Object.assign(anel.style, { left: r.left - 4 + "px", top: r.top - 4 + "px", width: r.width + 8 + "px", height: r.height + 8 + "px" });
    const w = quadro.offsetWidth, h = quadro.offsetHeight, vw = innerWidth, vh = innerHeight, m = 12;
    let lado = a.lado, x, y;
    // Na luta, o quadro fica logo abaixo da arena, alinhado ao controle: nunca por cima das cartas (vida, inimigos).
    const arena = lado === "arena" && document.querySelector("#hud");
    if (lado === "arena") lado = arena ? "baixo" : "direita";
    if (lado === "direita" && r.right + m + w > vw - 8) lado = "esquerda";
    if (lado === "baixo" && r.bottom + m + h > vh - 8) lado = "cima";
    if (lado === "direita") { x = r.right + m; y = r.top + r.height / 2 - h / 2; }
    else if (lado === "esquerda") { x = r.left - m - w; y = r.top + r.height / 2 - h / 2; }
    else if (lado === "baixo") { x = r.left + r.width / 2 - w / 2; y = (arena ? arena.getBoundingClientRect().bottom : r.bottom) + m; }
    else { x = r.left + r.width / 2 - w / 2; y = r.top - m - h; }
    x = Math.max(8, Math.min(vw - w - 8, x));
    y = Math.max(8, Math.min(vh - h - 8, y));
    quadro.className = `orientacao seta-${lado}`;
    // A seta aponta o centro do controle, mesmo com o quadro empurrado para dentro da tela.
    quadro.style.setProperty("--seta", (lado === "direita" || lado === "esquerda"
      ? Math.max(10, Math.min(h - 10, r.top + r.height / 2 - y)) : Math.max(10, Math.min(w - 10, r.left + r.width / 2 - x))) + "px");
    quadro.style.left = x + "px";
    quadro.style.top = y + "px";
    // O véu: só as colunas laterais e a doca (nunca a arena, as cartas, as barras, o topo nem a página).
    ["#heroi", "#mundo", "#doca"].forEach((s, k) => {
      const e = document.querySelector(s), v = veus[k];
      if (!a.veu || !visivel(e) || e.contains(a.el)) { v.hidden = true; return; }
      const q = e.getBoundingClientRect();
      v.hidden = false;
      Object.assign(v.style, { left: q.left + "px", top: q.top + "px", width: q.width + "px", height: q.height + "px" });
    });
  }

  function laco() { desenhar(); requestAnimationFrame(laco); }

  /** O estado novo: uma luta que começa zera os passos dela. */
  function aoEstado(e) {
    const emLuta = !!(e && e.combate);
    if (emLuta && !luta) luta = { c4: null, feito: false };
    if (!emLuta) luta = null;
    if (e && e.orientacao && e.orientacao.ligado) dispensado = false;
    if (!$("#sobre-ajuda").hidden) desenharAjuda();
  }

  /** O golpe do herói (Batalha.lance "acao"): usada uma habilidade, o C4 aponta o recurso que ela gastou. */
  function aoLance(m) {
    if (luta && !luta.feito && m.tipo === "acao" && m.de === "j" && m.hab && m.hab !== "ataque") luta.c4 = m.hab;
  }

  /** Uma resposta da pessoa: com o C4 à vista, a próxima ação encerra a sequência desta luta. */
  function aoResponder() {
    if (luta && luta.c4 && !processando) luta.feito = true;
  }

  // ---------------------------------------------------------------- a Ajuda
  function desenharAjuda() {
    const o = estado && estado.orientacao;
    const corpoAjuda = $("#ajuda-corpo");
    if (!o) { corpoAjuda.innerHTML = '<p class="vazio">Comece ou carregue um jogo para ver as orientações dele.</p>'; return; }
    const grupos = {};
    o.linhas.forEach((l) => { (grupos[l.grupo] = grupos[l.grupo] || []).push(l.texto); });
    const lista = Object.entries(grupos).map(([g, ls]) => `<h3>${Texto.html(g)}</h3><ul>${ls.map((t) => `<li>${texto(t)}</li>`).join("")}</ul>`).join("");
    corpoAjuda.innerHTML = `<button type="button" class="botao-janela ajuda-chave" aria-pressed="${o.ligado}">Mostrar orientações: <b>${o.ligado ? "ligado" : "desligado"}</b></button>
      ${lista || '<p class="vazio">Nenhuma orientação vista ainda neste jogo.</p>'}`;
    corpoAjuda.querySelector(".ajuda-chave").addEventListener("click", (ev) => {
      ev.stopPropagation();
      enviar(o.ligado ? "dispensar" : "ligar");
      o.ligado = !o.ligado;  // a tela responde na hora; o estado do motor confirma
      dispensado = !o.ligado;
      desenharAjuda();
    });
  }

  function alternarAjuda(forcar) {
    const s = $("#sobre-ajuda");
    s.hidden = forcar === undefined ? !s.hidden : !forcar;
    if (!s.hidden) { desenharAjuda(); s.querySelector(".ajuda-chave, button")?.focus(); }
  }

  requestAnimationFrame(laco);
  return { aoEstado, aoLance, aoResponder, alternarAjuda, esconder };
})();
