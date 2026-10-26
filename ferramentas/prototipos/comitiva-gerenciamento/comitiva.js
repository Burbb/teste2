/* Proposta: uma janela só para o herói e a comitiva. As abas com retratos escolhem o personagem; o boneco e a ficha
   são os dele; a bolsa é do grupo (uma só, os mesmos 12 espaços); a ficha de cada peça compara com o que o selecionado
   usa (Telas.htmlItem do jogo, com App.estado.heroi apontando para ele). Vestir num companheiro uma peça que outro
   usa sai dele e vai para o selecionado num passo só, sem passar pela bolsa. Tudo em memória: recarregar volta ao
   começo. */
"use strict";

(async () => {
  const $ = (s, r = document) => r.querySelector(s);
  const h = (t) => String(t ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const spr = (n, k = 2, c = "") => (typeof Sprites !== "undefined" ? Sprites.img(n, k, c) : "");
  const dados = await (await fetch("dados.json")).json();
  const inicial = JSON.parse(JSON.stringify(dados));
  const NOMES = { forca: "FOR", agilidade: "AGI", constituicao: "CON", intelecto: "INT", percepcao: "PER", vontade: "VON" };
  const NOME_LONGO = { forca: "Força", agilidade: "Agilidade", constituicao: "Constituição", intelecto: "Intelecto",
    percepcao: "Percepção", vontade: "Vontade" };
  const CLASSE_NOME = { guerreiro: "guerreiro", arqueiro: "arqueiro", mago: "mago" };
  let sel = "j", peca = null;  // peca: {de: "bolsa"|personagem id, slot ou índice}

  const pessoa = (id) => dados.personagens.find((p) => p.id === id);
  const atual = () => pessoa(sel);
  const espacosDe = (slot) => (slot === "anel" ? ["anel1", "anel2"] : [slot]);
  const serve = (p, it) => !it.classe || it.classe === p.pecas;
  const retrato = (p, lado = 32) => ((typeof Icones !== "undefined") && (Icones.cabeca(p.id === "j" ? "guerreiro" : p.id, lado))) || spr(p.id === "j" ? "guerreiro" : "humano", 2);
  const icone = (it) => (typeof Icones !== "undefined" && Icones.equipamento(it.icone)) || spr(it.icone || "saco", 2);

  function abas() {
    $(".abas").innerHTML = dados.personagens.map((p) => `<button type="button" role="tab" class="aba${p.id === sel ? " ativa" : ""}${p.disponivel ? "" : " indisponivel"}"
      aria-selected="${p.id === sel}" data-p="${h(p.id)}" tabindex="${p.id === sel ? 0 : -1}">
      <span class="aba-retrato">${retrato(p)}</span><span class="aba-nome">${h(p.nome)}</span>${p.temporario ? '<small class="aba-tag">proposta</small>' : ""}</button>`).join("");
    $(".abas").querySelectorAll(".aba").forEach((b) => b.addEventListener("click", () => escolher(b.dataset.p)));
  }
  function escolher(id) {
    sel = id;
    peca = null;
    desenhar();
    $(`.aba[data-p="${id}"]`).focus();
  }
  $(".abas").addEventListener("keydown", (ev) => {  // ← → entre as abas, como as abas de verdade
    const ids = dados.personagens.map((p) => p.id), i = ids.indexOf(sel);
    if (ev.key === "ArrowRight" || ev.key === "ArrowLeft") {
      ev.preventDefault();
      escolher(ids[(i + (ev.key === "ArrowRight" ? 1 : ids.length - 1)) % ids.length]);
    }
  });

  // quem usa a peça (para a lista "do grupo" num espaço)
  function vestidas(slot) {
    const lista = [];
    dados.personagens.forEach((p) => espacosDe(slot).forEach((s) => { if (p.id !== sel && p.equip[s]) lista.push({ p, s, it: p.equip[s] }); }));
    return lista;
  }

  function painelPeca() {
    if (!peca) return '<div class="comparar vazio">Escolha uma peça da bolsa ou um espaço do boneco para ver a ficha e comparar com o que <b>' + h(atual().nome) + "</b> usa.</div>";
    const p = atual();
    App.estado.heroi = { ...p, classe: p.pecas };  // a ficha do jogo compara com o selecionado
    let it, dono = null;
    if (peca.de === "bolsa") it = dados.bolsa[peca.i];
    else { dono = pessoa(peca.de); it = dono.equip[peca.s]; }
    if (!it) return "";
    const ficha = Telas.htmlItem(it, "", dono === null || dono.id !== sel);
    let acao = "";
    if (dono && dono.id === sel) {
      const cheia = dados.bolsa.length >= dados.limite;
      acao = `<button type="button" class="botao-janela" data-acao="tirar"${cheia ? " disabled" : ""}>Guardar na bolsa</button>${cheia ? '<p class="pior">A bolsa está cheia (12).</p>' : ""}`;
    } else if (!serve(p, it)) {
      acao = `<p class="pior">${h(p.nome)} não usa peças de ${h(CLASSE_NOME[it.classe] || it.classe)}.</p>`;
    } else {
      acao = `<button type="button" class="botao-janela" data-acao="vestir">Vestir em ${h(p.nome)}</button>` +
        (dono ? `<p class="nota">Sai de ${h(dono.nome)} e vai direto para ${h(p.nome)}.</p>` : "");
    }
    return `<div class="comparar"><div class="ficha-item">${ficha}</div><div class="acoes">${acao}</div></div>`;
  }

  function vestir() {
    const p = atual();
    let it;
    if (peca.de === "bolsa") it = dados.bolsa.splice(peca.i, 1)[0];
    else { const d = pessoa(peca.de); it = d.equip[peca.s]; d.equip[peca.s] = null; }
    const livres = espacosDe(it.slot);
    const s = livres.find((x) => !p.equip[x]) || livres[0];
    if (p.equip[s]) dados.bolsa.push(p.equip[s]);  // a que sai volta para a bolsa
    p.equip[s] = it;
    peca = { de: sel, s };
    desenhar();
  }
  function tirar() {
    const p = atual();
    dados.bolsa.push(p.equip[peca.s]);
    p.equip[peca.s] = null;
    peca = { de: "bolsa", i: dados.bolsa.length - 1 };
    desenhar();
  }

  function atributosHtml(p) {
    if (!p.temporario) {
      return `<div class="atributos-base">${Object.entries(p.atributos).map(([k, v]) => `<div class="attr-base"><small>${(NOMES[k] || "PRE")}</small><b>${v}</b></div>`).join("")}</div>`;
    }
    const livres = p.pontos;
    return `<div class="proposta-attr"><div class="attr-pontos">${livres ? `${livres} ponto${livres > 1 ? "s" : ""} para distribuir (proposta: ${dados.pontos_por_nivel} por nível do herói)` : "Sem pontos livres"}</div>
      <div class="atributos-base">${Object.entries(p.atributos).map(([k, v]) => `<div class="attr-base" title="${h(NOME_LONGO[k])}"><small>${NOMES[k]}</small><b>${v}</b>${livres ? `<button type="button" class="attr-mais" data-mais="${k}" aria-label="+1 de ${h(NOME_LONGO[k])}">+</button>` : ""}</div>`).join("")}</div>
      ${livres ? `<button type="button" class="botao-janela sugerir">Distribuir pela sugestão (${p.sugestao.map((k) => NOMES[k]).join(" › ")})</button>` : ""}</div>`;
  }

  function desenhar() {
    abas();
    const p = atual();
    App.estado.heroi = { ...p, classe: p.pecas };
    const ESPACOS = ["cabeca", "amuleto", "armadura", "maos", "arma", "secundaria", "pernas", "pes", "anel1", "anel2"];
    const boneco = ESPACOS.map((s) => {
      const it = p.equip[s];
      const marcado = peca && peca.de === sel && peca.s === s;
      return `<button type="button" class="espaco slot-px ${it ? "r-" + h(it.raridade) : "vazio"}${marcado ? " marcado" : ""}" data-espaco="${s}" style="grid-area:${Telas.AREA[s]}" aria-label="${h(Telas.NOME_ESPACO[s])}: ${it ? h(it.nome) : "vazio"}">
        ${it ? icone(it) : (Icones.vazio && Icones.vazio(s)) || spr(Telas.VAZIO[s], 2, "fantasma")}<span class="espaco-nome">${h(Telas.NOME_ESPACO[s])}</span></button>`;
    }).join("");
    const celulas = [];
    for (let i = 0; i < dados.limite; i++) {
      const it = dados.bolsa[i];
      const marcado = peca && peca.de === "bolsa" && peca.i === i;
      celulas.push(it ? `<button type="button" class="slot-px celula r-${h(it.raridade)}${serve(p, it) ? "" : " inutil"}${marcado ? " marcado" : ""}" data-bolsa="${i}" aria-label="${h(it.nome)}">${icone(it)}</button>`
        : '<div class="slot-px celula vazia"></div>');
    }
    // as peças que outros usam e serviriam no espaço marcado (vestir direto, sem passar pela bolsa)
    const espacoMarcado = peca && peca.de === sel ? peca.s : null;
    const doGrupo = espacoMarcado ? vestidas(espacoMarcado.startsWith("anel") ? "anel" : espacoMarcado).filter((x) => serve(p, x.it)) : [];
    $("#painel").innerHTML = `<div class="tela inventario">
      <div class="boneco">${boneco}<div class="boneco-retrato">${p.id === "j" ? (Icones.retrato("guerreiro", "Retrato") || retrato(p, 64)) : retrato(p, 32)}</div></div>
      <div class="inv-lado">
        <div class="ficha-mini"><div class="heroi-nome">${h(p.nome)}</div><div class="heroi-titulo">${h(p.titulo)}${p.temporario ? ' · <span class="aba-tag">dados temporários</span>' : ""}</div>
          ${p.disponivel ? "" : `<div class="pior">${h(p.indisponivel || "Indisponível")}</div>`}
          <div class="pecas">Usa peças de ${h(CLASSE_NOME[p.pecas])} e as sem classe.${p.temporario ? " Os números abaixo são os de hoje, sem as peças; com a proposta, elas somariam." : ""}</div></div>
        <div class="atributos">${Object.entries(p.derivados).map(([k, v]) => `<div class="atributo">${Icones.atributo(k) || ""}<span class="nome">${h(k)}</span><span class="valor"><span class="num">${v}</span></span></div>`).join("")}</div>
        <h4>Atributos${p.temporario ? " <small>(proposta)</small>" : ""}</h4>${atributosHtml(p)}
        <h4>Bolsa do grupo <small>${dados.bolsa.length}/${dados.limite}</small></h4>
        <div class="mochila-grade">${celulas.join("")}</div>
        ${doGrupo.length ? `<h4>Do grupo, para este espaço</h4><div class="do-grupo">${doGrupo.map((x) => `<button type="button" class="slot-px celula r-${h(x.it.raridade)}" data-de="${h(x.p.id)}" data-s="${x.s}" aria-label="${h(x.it.nome)}, com ${h(x.p.nome)}">${icone(x.it)}<small>${h(x.p.nome)}</small></button>`).join("")}</div>` : ""}
      </div>
      <div class="lado-ficha">${painelPeca()}</div></div>`;
    ligar();
  }

  function ligar() {
    const raiz = $("#painel");
    raiz.querySelectorAll("[data-espaco]").forEach((b) => b.addEventListener("click", () => { peca = { de: sel, s: b.dataset.espaco }; desenhar(); focar(`[data-espaco="${b.dataset.espaco}"]`); }));
    raiz.querySelectorAll("[data-bolsa]").forEach((b) => b.addEventListener("click", () => { peca = { de: "bolsa", i: +b.dataset.bolsa }; desenhar(); focar(`[data-bolsa="${b.dataset.bolsa}"]`); }));
    raiz.querySelectorAll("[data-de]").forEach((b) => b.addEventListener("click", () => { peca = { de: b.dataset.de, s: b.dataset.s }; desenhar(); focar(".acoes button"); }));
    const v = raiz.querySelector('[data-acao="vestir"]'); if (v) v.addEventListener("click", vestir);
    const t = raiz.querySelector('[data-acao="tirar"]'); if (t) t.addEventListener("click", tirar);
    raiz.querySelectorAll("[data-mais]").forEach((b) => b.addEventListener("click", () => {
      const p = atual(); p.atributos[b.dataset.mais]++; p.pontos--; desenhar(); }));
    const sug = raiz.querySelector(".sugerir");
    if (sug) sug.addEventListener("click", () => {
      const p = atual();
      for (let k = 0; p.pontos > 0; k++) { p.atributos[p.sugestao[k % p.sugestao.length]]++; p.pontos--; }
      desenhar();
    });
  }
  function focar(sel) { const e = $("#painel " + sel); if (e) e.focus(); }
  document.addEventListener("keydown", (ev) => { if (ev.key === "Escape" && peca) { peca = null; desenhar(); } });
  // dois cliques numa peça da bolsa: veste no selecionado, se ele usa (o mesmo gesto do inventário de hoje)
  $("#painel").addEventListener("dblclick", (ev) => {
    const b = ev.target.closest("[data-bolsa]");
    if (b && serve(atual(), dados.bolsa[+b.dataset.bolsa])) { peca = { de: "bolsa", i: +b.dataset.bolsa }; vestir(); }
  });
  window.restaurar = () => { Object.assign(dados, JSON.parse(JSON.stringify(inicial))); sel = "j"; peca = null; desenhar(); };
  desenhar();
})();
