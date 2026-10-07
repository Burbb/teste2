"use strict";

/* ------------------------------------------------------------------ estado e painéis */
function pct(a, b) { return b ? Math.max(0, Math.min(100, (100 * a) / b)) : 0; }
function barra(classe, atual, maximo, anterior) {
  const de = anterior === undefined ? pct(atual, maximo) : pct(anterior, maximo);
  return `<span class="barra-px ${classe}" data-alvo="${pct(atual, maximo)}"><span class="rastro" style="width:${de}%"></span><span class="enchimento" style="width:${de}%"></span></span>`;
}
function animarBarras(raiz) {
  requestAnimationFrame(() => requestAnimationFrame(() => {
    raiz.querySelectorAll(".barra-px[data-alvo]").forEach((b) => b.querySelectorAll(".rastro, .enchimento").forEach((x) => { x.style.width = b.dataset.alvo + "%"; }));
  }));
}
function flutuar(alvo, texto, classe) {
  if (!alvo || replay) return;
  const f = el("span", "flutua " + classe, esc(texto));
  alvo.appendChild(f);
  setTimeout(() => f.remove(), 1300);
}

let ultimoHeroi = "", ultimoMundo = "";
function aplicarEstado(e) {
  const antes = estado;
  estado = e;
  corpo.classList.remove("sem-heroi");
  const bioma = e.local.tipo === "vila" ? "vila" : e.local.bioma;
  corpo.dataset.bioma = bioma;
  corpo.dataset.periodo = e.mundo.periodo_n;
  corpo.classList.toggle("escuro", !!e.mundo.escuro);
  corpo.classList.toggle("em-combate", !!e.combate);
  corpo.style.setProperty("--corrupcao", (e.mundo.corrupcao / 100).toFixed(2));
  Som.ambiente(bioma);
  Vista.atualizar(e);
  if (corpo.classList.contains("modo-titulo")) {
    // Carregou um save ainda na tela de título: o céu inteiro passa a ser o do lugar e da hora do save.
    const [r, g, b] = Vista.corDoCeu();
    corpo.style.setProperty("--ceu-titulo", `rgb(${r}, ${g}, ${b})`);
  }
  MapaPx.ambiente(e.mundo);
  $("#tempo").textContent = `Dia ${e.mundo.dia} · ${e.mundo.periodo} · ${e.mundo.clima}`;
  $("#corrupcao-topo .enchimento").style.width = e.mundo.corrupcao + "%";
  $("#corrupcao-topo .valor").textContent = e.mundo.corrupcao + "%";
  $("#sigilos-topo").innerHTML = [0, 1, 2].map((i) => `<i class="sigilo${i < e.heroi.sigilos ? " tem" : ""}"></i>`).join("");
  desenharHud(e.heroi, antes && antes.heroi);
  Batalha.desenhar(e.combate, e.heroi, replay);
  desenharModificadores(e.mundo.modificadores || []);
  const chaveHeroi = JSON.stringify(e.heroi);
  if (chaveHeroi !== ultimoHeroi) { ultimoHeroi = chaveHeroi; desenharHeroi(e.heroi); }
  const mudouMapa = !antes || antes.local.id !== e.local.id || JSON.stringify(antes.mapa) !== JSON.stringify(e.mapa) || antes.heroi.nivel !== e.heroi.nivel ||
    antes.mundo.periodo_n !== e.mundo.periodo_n || antes.mundo.clima_id !== e.mundo.clima_id ||
    JSON.stringify(antes.contratos) !== JSON.stringify(e.contratos);
  if (mudouMapa) { desenharMundo(e); ultimoMundo = ""; }
  if (!$("#sobre-mapa").hidden && mudouMapa) desenharMapaGrande();
}

let ultimosMods = "";
/** Clima e hora que mexem nos números: ícone + porcentagem no topo (e no canto do palco, na luta). */
function desenharModificadores(mods) {
  const chave = JSON.stringify(mods) + !!(estado && estado.combate);
  if (chave === ultimosMods) return;
  ultimosMods = chave;
  const html = mods.map((m) => `<span class="mod" ${Telas.dica(`<b>${esc(m.texto)}</b><div>${esc(m.detalhe)}</div>`)}>${spr(m.icone, 1)}${esc(m.texto)}</span>`).join("");
  const topo = $("#modificadores");
  topo.innerHTML = html;
  Telas.ligarDicas(topo);
  const arena = $("#arena");
  if (arena) {
    let canto = arena.querySelector(".mods-arena");
    if (!canto) { canto = el("div", "mods-arena"); arena.appendChild(canto); }
    canto.innerHTML = html;
    Telas.ligarDicas(canto);
  }
}

function recurso(id, icones, qtd, opts = {}) {
  const imgs = icones.map((n) => spr(n, 2)).join("");
  return `<div class="recurso${opts.alerta ? " alerta" : ""}${opts.vazio ? " vazio" : ""}" data-rec="${id}" title="${esc(opts.titulo || "")}">
    <div class="icones">${imgs}</div><div class="qtd">${qtd}</div></div>`;
}

function desenharHud(h, antes) {
  // Um desenho para "acabou" e outro para "tem": o número ao lado diz quanto.
  const comida = [h.provisoes ? "pernil" : "osso_diag"];
  const tochas = [h.tochas ? "tocha" : "tocha_apagada"];
  const ouro = [h.ouro ? "moedas" : "bolsa_vazia"];
  const pocoes = [h.pocoes ? "pocao" : "frasco_vazio"];
  const vidaCritica = h.hp <= h.max_hp * 0.3;
  const feridas = h.ferimentos.length ? `<div class="recurso alerta" data-rec="feridas" title="${esc(h.males.join(" · "))}"><div class="icones">${spr("gota", 2)}</div><div class="qtd">${h.ferimentos.length}</div></div>` : "";
  $("#hud-linha").innerHTML = `
    <div class="hud-retrato" title="${esc(h.titulo)} nível ${h.nivel}">${spr(h.classe, 3)}<span class="nivel">${h.nivel}</span></div>
    <div class="hud-vitais">
      <div class="hud-nome"><b>${esc(h.nome)}</b><span>${esc(h.titulo)}${h.fome ? " · com fome" : ""}</span></div>
      <div class="vital${vidaCritica ? " critico" : ""}" data-vital="hp">${spr("coracao", 1)}${barra("vida", h.hp, h.max_hp, antes ? antes.hp : undefined)}<span class="num">${h.hp}/${h.max_hp}</span></div>
      <div class="vital" data-vital="rec">${spr(RECURSO_ICONE[h.recurso] || "estrela", 1)}${barra(RECURSO_BARRA[h.recurso] || "mana", h.rec, h.max_rec, antes ? antes.rec : undefined)}<span class="num">${h.rec}/${h.max_rec}</span></div>
    </div>
    <div class="hud-recursos">
      ${recurso("provisoes", comida, `${h.provisoes}<small>d</small>`, { alerta: h.provisoes <= 1, vazio: !h.provisoes, titulo: h.provisoes ? `Comida para ${h.provisoes} dia(s). Cada dia consome 1 (e cada companheiro come também).` : "Sem comida! Você vai passar fome." })}
      ${recurso("tochas", tochas, h.tochas, { alerta: h.tochas === 0, vazio: !h.tochas, titulo: "Tochas: luz para a noite, ruínas e a cidadela." })}
      ${recurso("ouro", ouro, h.ouro, { vazio: !h.ouro, titulo: "Ouro" })}
      ${recurso("pocoes", pocoes, h.pocoes, { vazio: !h.pocoes, titulo: "Poções de vida (35% da vida)" })}
      ${recurso("bandagens", ["bandagem"], h.bandagens, { vazio: !h.bandagens, alerta: !h.bandagens && h.ferimentos.some((f) => f.aberto), titulo: "Bandagens: estancam sangramento e tratam feridas abertas" })}
      ${h.flechas !== null && h.flechas !== undefined ? recurso("flechas", ["aljava"], h.flechas, { alerta: h.flechas <= 8, titulo: `Flechas (a aljava leva ${h.max_flechas || 30})` }) : ""}
      ${feridas}
    </div>`;
  animarBarras($("#hud-linha"));
  // Feedback: o que mudou desde o último estado
  const agora = { provisoes: h.provisoes, tochas: h.tochas, ouro: h.ouro, pocoes: h.pocoes, bandagens: h.bandagens, flechas: h.flechas };
  if (antes && !replay) {
    for (const [k, v] of Object.entries(agora)) {
      const velho = ultimosRecursos[k];
      if (velho === undefined || v === null || v === undefined || v === velho) continue;
      const alvo = $(`.recurso[data-rec="${k}"]`);
      if (!alvo) continue;
      alvo.classList.add(v > velho ? "ganhou" : "perdeu");
      flutuar(alvo, `${v > velho ? "+" : "−"}${Math.abs(v - velho)}`, v > velho ? "mais" : "menos");
    }
    const emLuta = estado && estado.combate;
    if (h.hp !== antes.hp && !emLuta) flutuar($('.vital[data-vital="hp"]'), `${h.hp > antes.hp ? "+" : "−"}${Math.abs(h.hp - antes.hp)}`, h.hp > antes.hp ? "cura" : "menos");
    if (h.hp < antes.hp && !emLuta) { doer(); Som.tocar("dor"); }
  }
  ultimosRecursos = agora;
}

function desenharHeroi(h) {
  const attrs = Telas.atributosHtml(h);
  const slot = (s) => {
    const it = h.equip[s];
    if (!it) return `<div class="slot-px mini vazio" title="${esc(Telas.NOME_ESPACO[s])} (vazio)">${spr(Telas.VAZIO[s], 1, "fantasma")}</div>`;
    return `<div class="slot-px mini r-${esc(it.raridade)}" ${Telas.dicaItem(it, "", false)}>${spr(Telas.iconeItem(it), 1)}</div>`;
  };
  const feridas = h.ferimentos.length ? h.ferimentos.map((f) => `<div class="ferimento">${spr("gota", 1)}${esc(f.nome)} <small>${f.dias ? f.dias + "d" : ""}${f.aberto ? " · aberto" : ""}</small></div>`).join("")
    : '<div class="vazio">nenhum, por enquanto</div>';
  const habs = h.habilidades.map((x) => `<div class="habilidade" title="${esc(x.desc)}"><span>${esc(x.nome)}</span><small>${x.custo} ${esc(h.recurso)}</small></div>`).join("");
  const bolsa = h.bolsa.filter((b) => b.id !== "tocha").map((b) => `<div class="slot-px" title="${esc(b.nome)}: ${esc(b.desc)}">${spr(Telas.ICONE_ITEM[b.id] || "pocao", 2)}<span class="qtd">${b.qtd}</span></div>`).join("");
  const comitiva = h.comitiva && h.comitiva.length ? `<div class="secao"><h3>Comitiva</h3>${h.comitiva.map((m) =>
    `<div class="membro${m.ferido ? " ferido" : ""}" data-cid="${esc(m.id)}">
      <div class="icone">${spr(m.id, 2)}</div>
      <div class="membro-nome"><span>${esc(m.nome)}</span>${m.conversa ? `<button type="button" class="membro-carta" data-conversar="${esc(m.id)}" title="${esc(m.nome.split(" ").pop())} quer conversar">✉</button>` : ""}</div>
      ${barra("vida fina", m.hp, m.max_hp)}${Telas.aprovacao(m)}</div>`).join("")}</div>` : "";
  $("#heroi").innerHTML = `
    <div class="identidade"><div class="retrato-grande">${spr(h.classe, 3)}</div>
      <div><div class="heroi-nome">${esc(h.nome)}</div><div class="heroi-titulo">${esc(h.titulo)} · nível ${h.nivel}</div></div></div>
    <div class="xp-linha"><div class="legenda-linha"><span>Experiência</span><span>${h.xp}/${h.xp_proximo}</span></div>${barra("xp", h.xp, h.xp_proximo)}</div>
    ${h.pontos_talento ? `<div class="talento-aviso" title="Abra Talentos (T) num local">${spr("estrela", 1)} ${h.pontos_talento} ponto(s) de talento</div>` : ""}
    <div class="secao"><h3>Atributos</h3><div class="atributos">${attrs}</div></div>
    <div class="secao"><h3>Equipado</h3><div class="equip-mini" title="Abra Personagem (P) para trocar">${Object.keys(Telas.AREA).map(slot).join("")}</div></div>
    ${comitiva}
    <div class="secao"><h3>Ferimentos</h3>${feridas}</div>
    <div class="secao"><h3>Habilidades</h3>${habs}</div>
    <div class="secao"><h3>Bolsa</h3><div class="slots">${bolsa || '<span class="vazio">vazia</span>'}</div></div>
    <div class="secao"><div class="linhas">${Telas.reputacaoHtml(h)}</div></div>`;
  animarBarras($("#heroi"));
  Telas.ligarDicas($("#heroi"));
}

function nivelPerigo(nivel) {
  if (nivel === null || nivel === undefined || !estado) return "";
  const d = nivel - estado.heroi.nivel;
  return d >= 2 ? "alto" : d >= 0 ? "medio" : "baixo";
}

function marcasContrato(e) { return new Set((e.contratos || []).filter((c) => !c.concluido).map((c) => c.lugar_id)); }

function desenharMundo(e) {
  const l = e.local;
  const clic = destinosClicaveis();
  const caminhos = e.mapa.nos.filter((n) => n.distancia).sort((a, b) => a.distancia - b.distancia || a.nome.localeCompare(b.nome))
    .map((n) => `<div class="caminho${clic.has(n.id) ? " clicavel" : ""}" data-local="${n.id}">${spr(MapaPx.sprite(n), 2)}
      <span class="nome">${esc(n.nome)} ${n.nivel ? `<span class="perigo-tag ${nivelPerigo(n.nivel)}">Nv.${n.nivel}</span>` : ""}<small>${esc(n.descricao)}</small></span>
      <span class="dist">${n.distancia} trecho${n.distancia > 1 ? "s" : ""}</span></div>`).join("");
  const raiz = $("#mundo");
  raiz.innerHTML = `<div class="local-nome">${esc(l.nome)}</div><div class="local-desc">${esc(l.descricao)}</div>
    ${l.nivel ? `<span class="perigo-tag ${nivelPerigo(l.nivel)}">inimigos Nv.${l.nivel}</span>` : ""}<div id="mapa-mini"></div>
    ${Telas.rastreador(e.contratos, e.heroi.nivel)}
    <div class="secao"><h3>Caminhos</h3><div class="caminhos">${caminhos || '<div class="vazio">nenhum</div>'}</div></div>`;
  const mini = MapaPx.criar(e.mapa, { clicaveis: clic, aoClicar: viajarPara, nivelHeroi: e.heroi.nivel, marcas: marcasContrato(e) });
  mini.title = "Abrir o mapa (M)";
  mini.addEventListener("click", (ev) => { if (!ev.target.closest(".clicavel")) alternarMapa(true); });
  $("#mapa-mini").appendChild(mini);
  if (clic.size) $("#mapa-mini").appendChild(el("div", "mapa-dica", "Clique num destino para viajar"));
  raiz.querySelectorAll(".caminho.clicavel").forEach((c) => c.addEventListener("click", () => viajarPara(Number(c.dataset.local))));
  raiz.querySelectorAll(".rastro-contrato").forEach((c) => {
    const id = Number(c.dataset.local);
    if (clic.has(id)) c.classList.add("clicavel");
    c.addEventListener("click", () => {
      const i = opcaoCacar(Number(c.dataset.contrato));
      if (i >= 0) responder(pergunta.id, i);
      else if (clic.has(id)) viajarPara(id);
    });
    c.addEventListener("mouseenter", () => document.querySelectorAll(`.no-btn[data-id="${id}"]`).forEach((b) => b.classList.add("destacado")));
    c.addEventListener("mouseleave", () => document.querySelectorAll(".no-btn.destacado").forEach((b) => b.classList.remove("destacado")));
  });
}

function legendaMapa() {
  return [["floresta", "floresta"], ["pantano", "pântano"], ["montanha", "montanha"], ["planicie", "planície"], ["ruinas", "ruínas"],
    ["cidadela", "cidadela"], ["vila", "vila"], ["covil", "covil de guardião"], ["vencido", "covil vencido"]]
    .map(([s, n]) => `<span>${spr(s, 1)} ${n}</span>`).join("");
}
function desenharMapaGrande() {
  if (!estado) return;
  const caixa = $("#mapa-grande");
  caixa.innerHTML = "";
  caixa.appendChild(MapaPx.criar(estado.mapa, { grande: true, clicaveis: destinosClicaveis(), nivelHeroi: estado.heroi.nivel, marcas: marcasContrato(estado),
    aoClicar: (id) => { alternarMapa(false); viajarPara(id); } }));
  $("#mapa-legenda").innerHTML = legendaMapa();
}
