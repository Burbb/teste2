/* As orientações da abertura guiada (abertura.py; roadmapIDEIAS/18). O motor diz qual orientação vale e o texto; aqui
   se acha o controle e se desenha:
   - o destaque: um contorno fino em volta do controle, com o formato dele e um brilho que pulsa devagar (com
     movimento reduzido, só o contorno). Um controle por vez; some quando a ação acontece;
   - o quadro: na luta, numa faixa estável logo abaixo da arena (ou acima das cartas, quando cabe), que fica reservada
     enquanto durar a luta guiada; ele não acompanha a investida, o tremor nem o retorno das cartas: a posição só muda
     quando muda a etapa, o tamanho da janela ou o layout. Fora da luta (o Mural), junto do prédio;
   - um véu leve só nas colunas laterais e na doca.
   C1–C3 se encerram pela própria ação (abrir Habilidades, escolher uma, escolher o alvo). O C4 explica o que a
   habilidade gastou, num momento estável depois do golpe (a próxima vez em que a pessoa pode agir), com "Entendi";
   se a habilidade encerrou a luta, ele não aparece (o espólio segue como sempre). "Encerrar tutorial" desliga todas
   as orientações; a Ajuda (F1, no topo) religa. */
"use strict";

const Orientacao = (() => {
  let quadro = null, anel = null, faixa = null, veus = [], dispensado = false;
  let luta = null;           // a luta de agora: { c4: id da habilidade usada, feito, guiada }
  let passo = "";            // a etapa à vista (o quadro só se reposiciona quando ela muda, ou o layout)
  let layout = "";           // o tamanho da janela e da área do quadro, quando a posição foi calculada
  let controle = null;       // o controle destacado
  const esc = Texto.html;
  const visivel = (e) => { if (!e) return false; const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const negrito = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>");

  function montar() {
    if (quadro) return;
    quadro = el("div", "orientacao", "");
    quadro.setAttribute("role", "note");
    anel = el("div", "orientacao-anel", "");
    for (let k = 0; k < 3; k++) veus.push(el("div", "orientacao-veu", ""));
    [...veus, anel, quadro].forEach((x) => { x.hidden = true; document.body.appendChild(x); });
    // O clique no quadro é dele: não adianta texto nem escolhe ação (o documento não fica sabendo).
    quadro.addEventListener("click", (ev) => {
      ev.stopPropagation();
      if (ev.target.closest(".orientacao-encerrar")) encerrar();
      else if (ev.target.closest(".orientacao-entendi")) entendi();
    });
    quadro.addEventListener("pointerdown", (ev) => ev.stopPropagation());
    quadro.addEventListener("keydown", (ev) => {
      // Enter e espaço no "Entendi" fecham só o quadro (a mesma tecla não escolhe uma ação nem fecha a próxima cena).
      if (ev.target.closest(".orientacao-entendi") && (ev.key === "Enter" || ev.key === " ")) {
        ev.preventDefault(); ev.stopPropagation(); entendi();
      }
    });
  }

  function enviar(acao) {
    fetch("/orientacao", { method: "POST", headers: { "Content-Type": "application/json", "X-Token": TOKEN },
      body: JSON.stringify({ acao }) }).catch((e) => console.error(e));
  }

  function encerrar() {
    dispensado = true;  // some na hora; o motor confirma no próximo estado
    enviar("dispensar");
    esconder();
    soltarFaixa();
  }

  function entendi() {
    if (luta) luta.feito = true;
    esconder();
  }

  function esconder() {
    if (!quadro) return;
    [...veus, anel, quadro].forEach((x) => { x.hidden = true; });
    passo = "";
    controle = null;
  }

  // ---------------------------------------------------------------- a faixa da luta guiada
  /** A faixa abaixo da arena, reservada enquanto durar a luta guiada: o quadro mora nela e nada da página fica por
   *  baixo dele. Se a arena tem espaço acima das cartas para o quadro, ela não é criada. */
  function reservarFaixa() {
    if (faixa || acimaDasCartas()) return;
    const pagina = document.querySelector("#cena #pagina");
    if (!pagina) return;
    faixa = el("div", "orientacao-faixa", "");
    faixa.setAttribute("aria-hidden", "true");
    // A altura do maior quadro da luta (o C4 da classe), medida antes: a faixa não muda de tamanho entre as etapas.
    faixa.style.height = alturaDoMaior() + 16 + "px";
    pagina.parentNode.insertBefore(faixa, pagina);
  }
  function alturaDoMaior() {
    const o = estado.orientacao.atual, c4 = Object.values(o.passos.C4 || {});
    const prova = el("div", "orientacao c4", "");
    Object.assign(prova.style, { visibility: "hidden", left: "-9999px", top: "0" });
    document.body.appendChild(prova);
    let h = 60;
    c4.forEach((c) => { prova.innerHTML = htmlC4(c); h = Math.max(h, prova.offsetHeight); });
    prova.remove();
    return h;
  }
  function soltarFaixa() { if (faixa) { faixa.remove(); faixa = null; } }

  /** A área livre acima das cartas da arena, se couber o maior quadro (o do C4); senão null. */
  function acimaDasCartas() {
    const arena = document.querySelector("#arena");
    const cartas = [...document.querySelectorAll("#arena .carta")];
    if (!arena || !cartas.length) return null;
    const a = arena.getBoundingClientRect();
    const topo = Math.min(...cartas.map((c) => c.getBoundingClientRect().top));
    return topo - a.top >= 140 ? { left: a.left + 8, top: a.top + 6, width: a.width - 16, height: topo - a.top - 12 } : null;
  }

  // ---------------------------------------------------------------- qual passo, onde
  /** O passo de agora: o controle a destacar, o HTML do quadro e onde ele mora. Ou null. */
  function alvo() {
    const o = estado && estado.orientacao && estado.orientacao.atual;
    if (!o || dispensado || !estado.orientacao.ligado) return null;
    if (document.querySelector(".sobreposicao:not([hidden]), #sobre-achado:not([hidden]), #janela-confirmar")) return null;
    if (o.id === "combate") {
      if (!estado.combate || !luta || luta.feito) return null;
      const p = o.passos;
      if (luta.c4) {
        // Só num momento estável: o golpe já foi, e a pessoa pode agir de novo (a roda voltou).
        const barra = document.querySelector('#arena .carta[data-uid="j"] .carta-rec');
        if (!visivel(barra) || !pergunta || processando || !p.C4[luta.c4]) return null;
        return { id: "C4", el: barra, html: htmlC4(p.C4[luta.c4]), luta: true };
      }
      const linha = document.querySelector(`.roda-janela .rj-linha[data-hab="${o.hab}"]`) || document.querySelector(".roda-janela .rj-linha[data-hab]");
      if (visivel(linha)) return { id: "C2", el: linha, html: botoes(negrito(p.C2)), luta: true, aoLado: linha.closest(".roda-janela") };
      const mira = document.querySelector("#arena .carta.alvejavel");
      if (visivel(mira)) return { id: "C3", el: mira, html: botoes(negrito(p.C3)), luta: true };
      const hab = document.querySelector('#roda .roda-botao[data-slot="habilidades"]');
      if (visivel(hab) && pergunta && !processando) return { id: "C1", el: hab, html: botoes(negrito(p.C1)), luta: true };
      return null;
    }
    if (o.id === "V1") {
      const mural = document.querySelector('#predios .predio[data-predio="mural"]');
      if (!visivel(mural) || !pergunta || estado.combate) return null;
      return { id: "V1", el: mural.querySelector(".balao-nome") || mural, html: botoes(negrito(o.texto)), luta: false };
    }
    return null;
  }

  const ENCERRAR = '<button type="button" class="orientacao-encerrar" title="Desliga todas as orientações; a Ajuda (F1) religa">Encerrar tutorial</button>';
  function botoes(html, entendi = false) {
    return `<div class="orientacao-texto">${html}</div><div class="orientacao-botoes">${entendi ? '<button type="button" class="orientacao-entendi">Entendi</button>' : ""}${ENCERRAR}</div>`;
  }

  /** O C4 em linhas curtas: o nome da habilidade; os custos com o ícone e a cor do recurso; o Atacar. */
  function parte(x) {
    if (x.rec) return `<span class="o-valor rec-${RECURSO_BARRA[x.rec] || "mana"}">${spr(RECURSO_ICONE[x.rec] || "estrela", 1)}${esc(x.t)}</span>`;
    if (x.flecha) return `<span class="o-valor flecha">${spr("flecha", 1)}${esc(x.t)}</span>`;
    return esc(x.t);
  }
  function htmlC4(c) {
    return botoes(`<div class="o-nome">${esc(c.nome)}</div><div class="o-custos">${c.gasto.map(parte).join(" ")}</div>
      <div class="o-atacar">${c.atacar.map(parte).join("")}</div>`, true);
  }

  // ---------------------------------------------------------------- desenhar
  function desenhar() {
    const a = alvo();
    if (!a) { esconder(); destacar(null); return; }
    montar();
    if (a.luta) reservarFaixa();
    const chave = a.id + "|" + a.html;
    const zona = a.luta ? (faixa ? faixa.getBoundingClientRect() : acimaDasCartas()) : null;
    const lay = `${innerWidth}x${innerHeight}|${zona ? [zona.left, zona.top, zona.width, zona.height].map(Math.round).join(",") : ""}`;
    if (chave !== passo || lay !== layout) {
      if (chave !== passo) {
        quadro.innerHTML = a.html;
        if (a.id === "C4") requestAnimationFrame(() => quadro.querySelector(".orientacao-entendi")?.focus({ preventScroll: true }));
      }
      passo = chave;
      layout = lay;
      quadro.hidden = false;
      posicionar(a, zona);
    }
    destacar(a.el);
    veu(a);
  }

  /** Onde o quadro fica: calculado na mudança de etapa ou de layout, nunca a cada quadro da animação. */
  function posicionar(a, zona) {
    const r = a.el.getBoundingClientRect(), w = quadro.offsetWidth, h = quadro.offsetHeight, vw = innerWidth, vh = innerHeight;
    let x, y, lado;
    if (a.luta && zona) {
      // Na faixa (ou acima das cartas): alinhado ao controle; ao lado da janelinha de Habilidades quando ela está aberta.
      // A janelinha de Habilidades desce sobre a faixa: o quadro vai para o lado dela que tem espaço.
      const jan = a.aoLado && a.aoLado.getBoundingClientRect();
      if (jan) x = jan.right + 12 + w <= zona.left + zona.width ? jan.right + 12 : jan.left - 12 - w;
      else x = r.left + r.width / 2 - w / 2;
      x = Math.max(zona.left + 4, Math.min(zona.left + zona.width - w - 4, x));
      y = zona.top + Math.max(4, (zona.height - h) / 2);
      lado = jan ? (x >= jan.right ? "direita" : "esquerda") : zona.top >= r.bottom ? "baixo" : "cima";
    } else {
      x = r.left + r.width / 2 - w / 2;
      y = r.bottom + 12;
      lado = "baixo";
      if (y + h > vh - 8) { y = r.top - 12 - h; lado = "cima"; }
    }
    x = Math.max(8, Math.min(vw - w - 8, x));
    y = Math.max(8, Math.min(vh - h - 8, y));
    quadro.className = `orientacao seta-${lado}${a.id === "C4" ? " c4" : ""}`;
    quadro.style.setProperty("--seta", (lado === "direita" || lado === "esquerda" ? Math.max(10, Math.min(h - 10, r.top + r.height / 2 - y))
      : Math.max(12, Math.min(w - 12, r.left + r.width / 2 - x))) + "px");
    quadro.style.left = Math.round(x) + "px";
    quadro.style.top = Math.round(y) + "px";
  }

  /** O contorno acompanha o controle (ele pode se mexer: o anel é dele, o quadro não). Um controle por vez. */
  function destacar(e) {
    controle = e;
    if (!anel) return;
    if (!e) { anel.hidden = true; return; }
    const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
    anel.hidden = false;
    Object.assign(anel.style, { left: r.left - 3 + "px", top: r.top - 3 + "px", width: r.width + 6 + "px", height: r.height + 6 + "px",
      borderRadius: cs.borderRadius && cs.borderRadius !== "0px" ? `calc(${cs.borderRadius} + 3px)` : "0" });
  }

  /** O véu: só as colunas laterais e a doca (nunca a arena, as cartas, as barras, o topo nem a página). */
  function veu(a) {
    ["#heroi", "#mundo", "#doca"].forEach((s, k) => {
      const e = document.querySelector(s), v = veus[k];
      if (!visivel(e) || e.contains(a.el)) { v.hidden = true; return; }
      const q = e.getBoundingClientRect();
      v.hidden = false;
      Object.assign(v.style, { left: q.left + "px", top: q.top + "px", width: q.width + "px", height: q.height + "px" });
    });
  }

  function laco() { desenhar(); requestAnimationFrame(laco); }

  /** O estado novo: uma luta que começa zera os passos dela; o fim da luta solta a faixa. */
  function aoEstado(e) {
    const emLuta = !!(e && e.combate);
    if (emLuta && !luta) luta = { c4: null, feito: false };
    if (!emLuta) { luta = null; soltarFaixa(); }
    if (e && e.orientacao && e.orientacao.ligado) dispensado = false;
    if (!$("#sobre-ajuda").hidden) desenharAjuda();
  }

  /** O golpe do herói (Batalha.lance "acao"): usada uma habilidade, o C4 vem na próxima vez em que se pode agir. */
  function aoLance(m) {
    if (luta && !luta.feito && m.tipo === "acao" && m.de === "j" && m.hab && m.hab !== "ataque") luta.c4 = m.hab;
  }

  /** Uma resposta da pessoa: com o C4 à vista, agir também o fecha (Entendi não é obrigatório). */
  function aoResponder() {
    if (luta && luta.c4 && passo.startsWith("C4")) luta.feito = true;
  }

  // ---------------------------------------------------------------- a Ajuda
  function desenharAjuda() {
    const o = estado && estado.orientacao;
    const corpoAjuda = $("#ajuda-corpo");
    if (!o) { corpoAjuda.innerHTML = '<p class="vazio">Comece ou carregue um jogo para ver as orientações dele.</p>'; return; }
    const grupos = {};
    o.linhas.forEach((l) => { (grupos[l.grupo] = grupos[l.grupo] || []).push(l.texto); });
    const lista = Object.entries(grupos).map(([g, ls]) => `<h3>${esc(g)}</h3><ul>${ls.map((t) => `<li>${negrito(t)}</li>`).join("")}</ul>`).join("");
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
