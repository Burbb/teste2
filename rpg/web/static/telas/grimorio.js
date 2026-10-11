/* Grimório: o livro das habilidades do herói, uma por página, com os números que o motor manda prontos. */
"use strict";

(() => {
  const { h, S } = Telas;

  const COR_ELEMENTO = { "físico": "#e8dcc0", fogo: "#ff9a4a", gelo: "#8fc4ff", sagrado: "#f2c94c", sombra: "#b08ae0", arcano: "#c8b0ff", veneno: "#8fbf6a" };
  let paginaGrimorio = "ataque";
  let desenhado = "";  // o que a página aberta mostra (dados e a troca oferecida): muda, redesenha sem virar a folha
  /** O livro de habilidades: índice à esquerda; à direita, a habilidade aberta com o dano de agora, de onde ele vem
   *  e como cresce. Os números chegam prontos do motor (grimorio.py), no estado do herói. */
  /** A troca de versão (E6): o motor a oferece como opção escondida (meta `versao`) só na vila e no acampamento. */
  const trocaOferecida = (id) => (App.opcoes() || []).some((o) => o.meta && o.meta.versao === id);
  /** As duas versões sempre na mesma ordem; a marca "Em uso" diz qual vale, e a página inteira é a dela. A troca é
   *  o botão (só onde o motor a oferece) e se confirma na própria página: ela vira a da outra versão. */
  function caixaVersao(x) {
    const v = x.versao;
    if (!v) return "";
    const pode = trocaOferecida(x.id);
    return `<div class="g-versao"><p class="g-versao-origem">${Realce.texto(v.origem)}</p>
      <ul class="g-versao-lista">${v.versoes.map((c) => `<li${c.em_uso ? ' class="em-uso"' : ""}>${c.em_uso ? '<span class="g-versao-tag">Em uso</span>' : ""}${Realce.texto(c.texto)}</li>`).join("")}</ul>
      ${pode ? `<button type="button" class="g-versao-trocar" data-versao="${h(x.id)}">Usar ${h(v.outra)}</button>`
        : `<p class="g-versao-onde">${h(v.onde)}</p>`}</div>`;
  }
  function abrirGrimorio(id, quieto) {
    const g = App.estado && App.estado.heroi && App.estado.heroi.grimorio;
    if (!g) return;
    if (id) paginaGrimorio = id;
    const todas = [g.basico, ...g.habilidades, ...(g.passivas || [])];
    if (!todas.some((x) => x.id === paginaGrimorio)) paginaGrimorio = "ataque";
    const heroi = App.estado.heroi;
    const icone = (x) => x.icone || "estrela";
    const custo = (x) => x.passiva ? (x.rotulo || "Passiva") : x.custo ? `${x.custo} ${h(g.recurso.toLowerCase())}` : "grátis";
    document.getElementById("grimorio-indice").innerHTML = `
      <div class="grimorio-cab"><b>Grimório</b><small>${h(heroi.titulo)} · nível ${heroi.nivel}</small></div>
      <ul class="grimorio-lista">${todas.map((x) => `<li><button type="button" class="grimorio-item${x.id === paginaGrimorio ? " aberto" : ""}" data-pagina="${h(x.id)}">
        <span class="gi-icone">${S(icone(x), 2)}</span><span class="gi-nome">${h(x.nome)}</span><span class="gi-custo${x.passiva ? " passiva" : ""}">${custo(x)}</span></button></li>`).join("")}</ul>
      <div class="grimorio-atributos">${Object.entries(g.atributos).map(([k, v]) => `<span><small>${h(k)}</small><b>${v}</b></span>`).join("")}</div>
      <ul class="grimorio-gerais">${g.gerais.map((l) => `<li>${Realce.texto(l)}</li>`).join("")}</ul>`;
    const x = todas.find((t) => t.id === paginaGrimorio);
    const linhas = x.linhas.map((l) => l.tipo === "efeito" ? `<li class="g-efeito">${Realce.texto(l.texto)}</li>` : `
      <li class="g-dano"><div class="g-rotulo">${h(l.rotulo)} <i style="color:${COR_ELEMENTO[l.elemento] || "#e8dcc0"}">${h(l.elemento)}</i></div>
        <div class="g-faixa"><b>${l.min}–${l.max}</b><span class="rx rx-crit">crítico <b>${l.critico}</b> · ${l.chance_critico}% de chance</span></div>
        <div class="g-formula">${h(l.formula)}</div>
        <div class="g-escala">${l.escala.map((e) => `<span>▲ ${h(e)}</span>`).join("")}</div>
        ${l.nota ? `<div class="g-nota">${h(l.nota)}</div>` : ""}</li>`).join("");
    const det = document.getElementById("grimorio-detalhe");
    det.innerHTML = `<div class="g-topo"><span class="g-icone">${S(icone(x), 4)}</span>
        <div><b class="g-nome">${h(x.nome)}</b><div class="g-meta">${custo(x)}${x.flechas_por_alvo ? ` · ${x.flechas_por_alvo} flecha por inimigo` : x.flechas ? ` · ${Texto.plural(x.flechas, "flecha")}` : ""}${x.alvo ? ` · Alvo: ${h(x.alvo)}` : ""}</div></div></div>
      <p class="g-desc">${Realce.texto(x.desc)}</p><ul class="g-linhas">${linhas}</ul>${caixaVersao(x)}
      ${x.passiva ? "" : '<p class="g-rodape">Números antes da defesa do inimigo e de efeitos do momento (fortalecido, clima, alvo marcado).</p>'}`;
    desenhado = assinatura(g, x);
    if (!quieto) { det.classList.remove("virando"); void det.offsetWidth; det.classList.add("virando"); }
    const troca = det.querySelector(".g-versao-trocar");
    if (troca) troca.addEventListener("click", (ev) => { ev.stopPropagation(); App.acao({ versao: troca.dataset.versao }, "pagina"); });
    const caixa = document.getElementById("sobre-grimorio");
    if (caixa.hidden) { caixa.hidden = false; App.som("pagina"); }
    caixa.querySelectorAll("[data-pagina]").forEach((b) => b.addEventListener("click", (ev) => {
      ev.stopPropagation();
      if (b.dataset.pagina !== paginaGrimorio) { App.som("pagina"); abrirGrimorio(b.dataset.pagina); }
    }));
  }
  const assinatura = (g, x) => JSON.stringify(g) + (x && trocaOferecida(x.id) ? "+troca" : "");
  /** Com o livro aberto, um estado ou um menu novo (a troca feita, a volta à vila) redesenha a página, sem virar. */
  function atualizarGrimorio() {
    const caixa = document.getElementById("sobre-grimorio");
    const g = App.estado && App.estado.heroi && App.estado.heroi.grimorio;
    if (!caixa || caixa.hidden || !g) return;
    const x = [g.basico, ...g.habilidades, ...(g.passivas || [])].find((t) => t.id === paginaGrimorio);
    if (assinatura(g, x) !== desenhado) abrirGrimorio(null, true);
  }
  function alternarGrimorio() {
    const caixa = document.getElementById("sobre-grimorio");
    if (caixa.hidden) abrirGrimorio(); else caixa.hidden = true;
  }

  Object.assign(Telas, { abrirGrimorio, alternarGrimorio, atualizarGrimorio });
})();
