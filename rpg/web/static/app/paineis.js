"use strict";

/* ------------------------------------------------------------------ estado e painéis */
const { pct } = Telas;
/** Uma barra. Com `chave`, ela sai da largura que estava na tela (larguraViva): um estado novo no meio da animação
 *  (a poção e, logo depois, outra mudança) continua de onde a barra está, em vez de saltar para o fim. */
function barra(classe, atual, maximo, anterior, chave) {
  const viva = chave ? larguraViva[chave] : undefined;
  const de = viva !== undefined ? viva : anterior === undefined ? pct(atual, maximo) : pct(anterior, maximo);
  return `<span class="barra-px ${classe}"${chave ? ` data-chave="${chave}"` : ""} data-alvo="${pct(atual, maximo)}"><span class="rastro" style="width:${de}%"></span><span class="enchimento" style="width:${de}%"></span></span>`;
}
const larguraViva = {};
/** Antes de redesenhar um painel: a largura que cada barra com chave mostra agora, em %. */
function guardarLarguras(raiz) {
  for (const k in larguraViva) delete larguraViva[k];
  raiz.querySelectorAll(".barra-px[data-chave]").forEach((b) => {
    const total = b.getBoundingClientRect().width;
    if (total) larguraViva[b.dataset.chave] = (100 * b.querySelector(".enchimento").getBoundingClientRect().width) / total;
  });
}
/** As barras vão do valor de antes ao de agora. Subindo (cura, poção), o rastro claro marca logo onde ela vai chegar
 *  e a cor enche devagar até lá; descendo, a cor cai e o rastro vai atrás. */
function animarBarras(raiz) {
  requestAnimationFrame(() => requestAnimationFrame(() => {
    raiz.querySelectorAll(".barra-px[data-alvo]").forEach((b) => {
      const enc = b.querySelector(".enchimento"), alvo = Number(b.dataset.alvo);
      b.classList.toggle("subindo", alvo > parseFloat(enc.style.width) + 0.01);
      b.querySelectorAll(".rastro, .enchimento").forEach((x) => { x.style.width = alvo + "%"; });
    });
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
  Realce.glossario(e.glossario);
  corpo.classList.remove("sem-heroi");
  const bioma = e.local.tipo === "vila" ? "vila" : e.local.bioma;
  corpo.dataset.bioma = bioma;
  corpo.dataset.periodo = e.mundo.periodo_n;
  corpo.classList.toggle("escuro", !!e.mundo.escuro);
  corpo.classList.toggle("em-combate", !!e.combate);
  if (!e.combate) posicionarPrompt();  // a luta acabou: as opções voltam ao pé da página
  corpo.classList.toggle("recurso-vigor", e.heroi.recurso === "Vigor");
  corpo.classList.toggle("recurso-foco", e.heroi.recurso === "Foco");
  Som.ambiente(bioma);
  Vista.atualizar(e);
  if (corpo.classList.contains("modo-titulo")) {
    // Carregou um save ainda na tela de título: o céu inteiro passa a ser o do lugar e da hora do save.
    const [r, g, b] = Vista.corDoCeu();
    corpo.style.setProperty("--ceu-titulo", `rgb(${r}, ${g}, ${b})`);
  }
  MapaPx.ambiente(e.mundo);
  $("#tempo").textContent = `Dia ${e.mundo.dia} · ${e.mundo.periodo} · ${e.mundo.clima}`;
  $("#sigilos-topo").innerHTML = [0, 1, 2].map((i) => `<i class="sigilo${i < e.heroi.sigilos ? " tem" : ""}"></i>`).join("");
  desenharHud(e.heroi, antes && antes.heroi);
  Batalha.catalogo(e.estados);
  Batalha.desenhar(e.combate, e.heroi, replay);
  desenharModificadores(e.mundo.modificadores || []);
  const chaveHeroi = JSON.stringify(e.heroi);
  if (chaveHeroi !== ultimoHeroi) { ultimoHeroi = chaveHeroi; desenharHeroi(e.heroi, antes && antes.heroi); }
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
  const dica = opts.titulo ? Telas.dica(esc(opts.titulo), true) : "";
  return `<div class="recurso${opts.alerta ? " alerta" : ""}${opts.vazio ? " vazio" : ""}" data-rec="${id}" ${dica}>
    <div class="icones">${imgs}</div><div class="qtd">${qtd}</div></div>`;
}

function desenharHud(h, antes) {
  // Um desenho para "acabou" e outro para "tem": o número ao lado diz quanto.
  const comida = [h.provisoes ? "pernil" : "osso_diag"];
  const tochas = [h.tochas ? "tocha" : "tocha_apagada"];
  const ouro = [h.ouro ? "moedas" : "bolsa_vazia"];
  const pocoes = [h.pocoes ? "pocao" : "frasco_vazio"];
  Sensacao.vidaDoHeroi(h.hp, h.max_hp, h.vida_por_um_fio);
  guardarLarguras($("#hud-linha"));
  const feridas = h.ferimentos.length ? `<div class="recurso alerta" data-rec="feridas" ${Telas.dica(h.ferimentos.map((f) => `<b>${esc(f.nome)}</b><div class="bonus pior">${esc((f.explica || [""])[0])}</div>`).join("") + '<div class="rodape">Detalhes no painel do herói, à esquerda.</div>')}><div class="icones">${spr("gota", 2)}</div><div class="qtd">${h.ferimentos.length}</div></div>` : "";
  $("#hud-linha").innerHTML = `
    <div class="hud-retrato" title="${esc(h.titulo)} nível ${h.nivel}">${spr(h.classe, 3)}<span class="nivel">${h.nivel}</span></div>
    <div class="hud-vitais">
      ${h.fome ? '<span class="hud-fome">com fome</span>' : ""}
      <div class="vital" data-vital="hp" ${Telas.dica("Vida", true)}>${spr("coracao", 1)}${barra("vida", h.hp, h.max_hp, antes ? antes.hp : undefined, "hud-hp")}<span class="num">${h.hp}/${h.max_hp}</span></div>
      <div class="vital" data-vital="rec" ${Telas.dica(esc(h.recurso), true)}>${spr(RECURSO_ICONE[h.recurso] || "estrela", 1)}${barra(RECURSO_BARRA[h.recurso] || "mana", h.rec, h.max_rec, antes ? antes.rec : undefined, "hud-rec")}<span class="num">${h.rec}/${h.max_rec}</span></div>
    </div>
    <div class="hud-recursos">
      ${recurso("provisoes", comida, `${h.provisoes}<small>d</small>`, { alerta: h.provisoes <= 1, vazio: !h.provisoes, titulo: h.provisoes ? `Comida para ${Texto.plural(h.provisoes, "dia")}. Cada dia consome 1 (e cada companheiro come também).` : "Sem comida! Você vai passar fome." })}
      ${recurso("tochas", tochas, h.tochas, { alerta: h.tochas === 0, vazio: !h.tochas, titulo: "Tochas: luz para a noite, ruínas e a cidadela." })}
      ${recurso("ouro", ouro, h.ouro, { vazio: !h.ouro, titulo: h.ouro ? `Ouro: ${Texto.plural(h.ouro, "moeda")}` : "Sem ouro" })}
      ${recurso("pocoes", pocoes, h.pocoes, { vazio: !h.pocoes, titulo: "Poções de vida (35% da vida)" })}
      ${recurso("bandagens", ["bandagem"], h.bandagens, { vazio: !h.bandagens, alerta: !h.bandagens && h.ferimentos.some((f) => f.aberto), titulo: "Bandagens: estancam sangramento e tratam feridas abertas" })}
      ${h.flechas !== null && h.flechas !== undefined ? recurso("flechas", ["aljava"], h.flechas, { alerta: h.flechas <= 8, titulo: `Flechas (a aljava leva ${h.max_flechas || 30})` }) : ""}
      ${feridas}
    </div>`;
  animarBarras($("#hud-linha"));
  Telas.ligarDicas($("#hud-linha"));
  // Feedback: o que mudou desde o último estado
  const agora = { provisoes: h.provisoes, tochas: h.tochas, ouro: h.ouro, pocoes: h.pocoes, bandagens: h.bandagens, flechas: h.flechas };
  if (antes && !replay) {
    for (const [k, v] of Object.entries(agora)) {
      const velho = ultimosRecursos[k];
      if (velho === undefined || v === null || v === undefined || v === velho) continue;
      const alvo = $(`.recurso[data-rec="${k}"]`);
      if (!alvo) continue;
      if (itensChegando.has(k) && v > velho) { ganhosAdiados[k] = (ganhosAdiados[k] || 0) + v - velho; continue; }  // o ícone ainda voa
      alvo.classList.add(v > velho ? "ganhou" : "perdeu");
      flutuar(alvo, `${v > velho ? "+" : "−"}${Math.abs(v - velho)}`, v > velho ? "mais" : "menos");
    }
    const emLuta = estado && estado.combate;
    if (h.hp !== antes.hp && !emLuta) flutuar($('.vital[data-vital="hp"]'), `${h.hp > antes.hp ? "+" : "−"}${Math.abs(h.hp - antes.hp)}`, h.hp > antes.hp ? "cura" : "menos");
    if (h.hp < antes.hp && !emLuta) { doer(); Som.tocar("dor"); }
  }
  ultimosRecursos = agora;
}

function desenharHeroi(h, antes) {
  guardarLarguras($("#heroi"));
  const attrs = Telas.atributosHtml(h);
  const slot = (s) => {
    const it = h.equip[s];
    if (!it) return `<div class="slot-px mini vazio" data-mini="${s}" title="${esc(Telas.NOME_ESPACO[s])} (vazio)">${spr(Telas.VAZIO[s], 2, "fantasma")}</div>`;
    return `<div class="slot-px mini r-${esc(it.raridade)}" data-mini="${s}" ${Telas.dicaItem(it, "", false)}>${spr(Telas.iconeItem(it), 2)}</div>`;
  };
  const feridas = h.ferimentos.length ? h.ferimentos.map((f) => `<div class="ferimento${f.aberto ? " aberto" : ""}" ${Telas.dica(`<b>${esc(f.nome)}</b><div class="tipo">${f.dias ? `${Texto.plural(f.dias, "dia")} para sarar` : "não sara sozinha"}${f.aberto ? " · ferida aberta" : ""}</div>${(f.explica || []).map((l, i) => `<div class="${i ? "" : "bonus pior"}">${esc(l)}</div>`).join("")}`)}>${spr("gota", 1)}${esc(f.nome)} <small>${f.dias ? f.dias + "d" : ""}${f.aberto ? " · aberto" : ""}</small></div>`).join("")
    : '<div class="vazio">Nenhum, por enquanto.</div>';
  const bolsa = h.bolsa.filter((b) => b.id !== "tocha").map((b) => {
    const bau = b.id === "bau";  // o baú se abre (e, onde dá para abrir, ganha o anel dourado)
    const dica = `<b>${esc(b.nome)}</b><div>${Realce.texto(b.desc)}</div><div class="rodape">${b.motivo ? esc(b.motivo) : bau ? (b.qtd > 1 ? `Clique para abrir os ${b.qtd} de uma vez.` : "Clique para abrir.") : estado && estado.combate ? "Clique para usar (gasta o turno)." : "Clique para usar."}</div>`;
    return `<div role="button" tabindex="0" class="slot-px usavel${b.motivo && !(b.alvos || []).some((a) => !a.motivo) ? " inutil" : ""}${bau && !b.motivo ? " pronto" : ""}" data-bolsa="${esc(b.id)}" ${Telas.dica(dica)}>${spr(Telas.iconeConsumivel(b.id), 2)}<span class="qtd">${b.qtd}</span></div>`;
  }).join("");
  // Comitiva e animal no mesmo molde: retrato e nome com a ficha no hover, a vida em números no canto (como os
  // atributos), a barra, e embaixo a aprovação (só companheiros). O ♥ do carinho fica ao lado da vida do animal.
  const vida = (hp, max) => `<b class="membro-vida">${Math.max(0, hp)}/${max}</b>`;
  const linhaNome = (nome, extra, hp, max, dicaAttr) =>
    `<div class="membro-nome"><span class="membro-quem" ${dicaAttr}>${esc(nome)}${extra}</span>${vida(hp, max)}</div>`;
  const f = h.companheiro;
  const ESPECIE = { lobo: "Lobo", urso: "Urso", falcao: "Falcão" };
  const dicaFera = f ? Telas.dica(`<b>${esc(f.nome)}</b><div class="tipo">${ESPECIE[f.tipo] || "Animal"} · seu companheiro</div>` +
    (f.hp <= 0 ? "<div>Ferido: não luta até descansar.</div>" : "") +
    (f.animado ? '<div class="melhor">Animado: +15% de dano na próxima luta.</div>' : "") +
    '<div class="rodape">Poção e bandagem da bolsa também servem nele. Na fogueira, um carinho.</div>') : "";
  const fera = f ? `<div class="membro fera${f.hp <= 0 ? " ferido" : ""}" data-fera="1">
      <div class="icone" ${dicaFera}>${spr(f.tipo === "falcao" ? "voador" : "fera", 2)}</div>
      ${linhaNome(f.nome, f.animado ? ' <b class="fera-animado" title="animado">♥</b>' : "", f.hp, f.max_hp, dicaFera)}
      ${barra("vida fina", Math.max(0, f.hp), f.max_hp, antes && antes.companheiro ? Math.max(0, antes.companheiro.hp) : undefined, "fera")}</div>` : "";
  const membros = (h.comitiva || []).map((m) => {
    const d = Telas.dica(`<b>${esc(m.nome)}</b><div class="tipo">${esc(m.titulo)}</div><div>${esc(m.desc || "")}</div>` +
      (m.ferido ? "<div class=\"bonus pior\">Ferido: fora de combate até descansar.</div>" : "") +
      `<div class="rodape">${m.conversa ? "Quer conversar: clique no ✉." : "Mais na aba Comitiva."}</div>`);
    const carta = m.conversa ? ` <button type="button" class="membro-carta" data-conversar="${esc(m.id)}" title="${esc(m.nome.split(" ").pop())} quer conversar">✉</button>` : "";
    const velho = antes && (antes.comitiva || []).find((x) => x.id === m.id);  // a barra sai de onde estava
    return `<div class="membro${m.ferido ? " ferido" : ""}" data-cid="${esc(m.id)}">
      <div class="icone" ${d}>${spr(m.id, 2)}</div>
      ${linhaNome(m.nome, carta, m.hp, m.max_hp, d)}
      ${barra("vida fina", m.hp, m.max_hp, velho ? velho.hp : undefined, "m-" + m.id)}${Telas.aprovacao(m)}</div>`;
  }).join("");
  const comitiva = membros || fera ? `<div class="secao"><h3>Comitiva</h3>${membros}${fera}</div>` : "";
  $("#heroi").innerHTML = `
    <div class="identidade"><div class="retrato-grande">${spr(h.classe, 3)}</div>
      <div><div class="heroi-nome">${esc(h.nome)}</div><div class="heroi-titulo">${esc(h.titulo)} • nível ${h.nivel}</div></div></div>
    <div class="xp-linha"><div class="legenda-linha"><span>Experiência</span><span>${h.xp}/${h.xp_proximo}</span></div>${barra("xp", h.xp, h.xp_proximo, antes && antes.nivel === h.nivel ? antes.xp : undefined, antes && antes.nivel === h.nivel ? "xp" : undefined)}</div>
    ${h.pontos_talento ? `<div class="talento-linha"><div class="talento-aviso" role="button" tabindex="0" data-atalho="Talentos"><span class="estrela">${spr("estrela", 2)}</span><span>${Texto.plural(h.pontos_talento, "ponto de talento", "pontos de talento")}</span></div><span class="seta-pendencia" aria-hidden="true">${spr("seta_esq", 2)}</span></div>` : ""}
    <div class="secao"><h3>Atributos</h3><div class="atributos">${attrs}</div></div>
    <div class="secao"><h3>Equipado</h3><div class="equip-mini">${Object.keys(Telas.AREA).map(slot).join("")}</div></div>
    ${comitiva}
    <div class="secao"><h3>Ferimentos</h3>${feridas}</div>
    <div class="secao"><h3>Bolsa</h3><div class="slots">${bolsa || '<span class="vazio">vazia</span>'}</div></div>
    <div class="secao"><h3>Reputação</h3>${Telas.reputacaoHtml(h)}</div>`;
  animarBarras($("#heroi"));
  Telas.ligarDicas($("#heroi"));
  // O aviso de ponto de talento abre a árvore (ou guarda o pedido, se ainda houver cena correndo).
  $("#heroi").querySelectorAll("[data-atalho]").forEach((el) => el.addEventListener("click", (ev) => { ev.stopPropagation(); pedirAtalho(el.dataset.atalho); }));
  $("#heroi").querySelectorAll("[data-bolsa]").forEach((el) => {
    const usar = () => usarDaBolsa(h.bolsa.find((b) => b.id === el.dataset.bolsa), el);
    el.addEventListener("click", usar);
    el.addEventListener("keydown", (ev) => { if (ev.key === "Enter") usar(); });
    el.addEventListener("contextmenu", (ev) => {  // botão direito: usa em você, sem perguntar em quem
      ev.preventDefault();
      const b = h.bolsa.find((x) => x.id === el.dataset.bolsa);
      if (!b) return;
      if (estado && estado.combate) { usarDaBolsa(b, el); return; }  // na luta, o mesmo caminho do clique
      if (b.motivo) { Som.tocar("falha"); aviso(b.motivo, "info", "pergaminho"); return; }
      App.acao({ usar: b.id }, "item");
    });
  });
}

/** A bolsa do painel lateral: clicou, usou. Na luta, é o mesmo caminho do "Itens" das ações (gasta o turno e,
 *  se um aliado precisa, pergunta em quem); o motor manda o motivo de não servir já pensando na luta.
 *  Fora dela, vale em qualquer menu de lugar. Se agora não dá (no meio de um evento, fora da sua vez), diz por quê. */
function usarDaBolsa(b, el) {
  if (!b) return;
  const alvosBons = (b.alvos || []).some((a) => !a.motivo);
  if (b.motivo && !alvosBons) { Som.tocar("falha"); aviso(b.motivo, "info", "pergaminho"); return; }
  const opcoes = (pergunta && pergunta.tipo === "opcoes" && pergunta.opcoes) || [];
  if (estado && estado.combate) {
    if (!opcoes.some((o) => o.meta && (o.meta.usar_item === b.id || o.meta.acao === "itens"))) {
      Som.tocar("falha"); aviso("Espere a sua vez.", "info", "pergaminho"); return;
    }
    Som.tocar("item");
    habMirando = b.nome;  // se pedir em quem, o lembrete diz o quê ("Poção de Vida · escolha o alvo")
    pedir("Itens", "usar_item", b.id);
    return;
  }
  if (alvosBons && b.alvos.length && opcoes.some((o) => o.meta && o.meta.usar === b.id)) { Telas.menuUso(el, b); return; }
  if (!acao({ usar: b.id }, "item")) { Som.tocar("falha"); aviso("Agora não: termine o que está fazendo primeiro.", "info", "pergaminho"); }
}

function nivelPerigo(nivel) {
  if (nivel === null || nivel === undefined || !estado) return "";
  const d = nivel - estado.heroi.nivel;
  return d >= 2 ? "alto" : d >= 0 ? "medio" : "baixo";
}

const maiuscula = (t) => (t ? t[0].toUpperCase() + t.slice(1) : t);  // "vila" → "Vila" no painel do mundo
function marcasContrato(e) { return new Set((e.contratos || []).filter((c) => !c.concluido).map((c) => c.lugar_id)); }
/** A dica de um lugar no mapa (hover): o nome, o tipo, o perigo, a distância e os contratos que você tem lá. */
function dicaDoLugar(e, clic) {
  const porLugar = {};
  (e.contratos || []).filter((c) => !c.concluido).forEach((c) => { (porLugar[c.lugar_id] = porLugar[c.lugar_id] || []).push(c); });
  return (n) => `<b>${esc(n.nome)}</b><div class="tipo">${esc(maiuscula(n.descricao))}` +
    (n.nivel ? ` · <span class="nivel-cam ${nivelPerigo(n.nivel)}">${n.tipo === "vila" ? "arredores" : "inimigos"} Nv.${n.nivel}</span>` : "") +
    (n.distancia ? ` · ${Texto.plural(n.distancia, "trecho")}` : n.atual ? " · você está aqui" : "") + "</div>" +
    (porLugar[n.id] || []).map((c) => `<div class="dica-contrato">${spr("pergaminho", 1)}<span>${esc(c.desc)}</span></div>`).join("") +
    (clic.has(n.id) ? '<div class="rodape">Clique para viajar</div>' : "");
}

function desenharMundo(e) {
  const l = e.local;
  const clic = destinosClicaveis();
  const caminhos = e.mapa.nos.filter((n) => n.distancia).sort((a, b) => a.distancia - b.distancia || a.nome.localeCompare(b.nome))
    .map((n) => `<div class="caminho${clic.has(n.id) ? " clicavel" : ""}" data-local="${n.id}">${spr(MapaPx.sprite(n), 2)}
      <span class="nome">${esc(n.nome)}<small>${n.nivel ? `<span class="nivel-cam ${nivelPerigo(n.nivel)}">Nível ${n.nivel}</span> · ` : ""}${esc(n.descricao)}</small></span>
      <span class="dist">${Texto.plural(n.distancia, "trecho")}</span></div>`).join("");
  const raiz = $("#mundo");
  raiz.innerHTML = `<div class="local-nome">${esc(l.nome)}</div><div class="local-desc">${esc(maiuscula(l.descricao))}</div>
    ${l.nivel ? `<span class="perigo-tag ${nivelPerigo(l.nivel)}">${l.tipo === "vila" ? "Arredores" : "Inimigos"} Nv.${l.nivel}</span>` : ""}<div id="mapa-mini"></div>
    ${Telas.rastreador(e.contratos, e.heroi.nivel)}
    <div class="secao"><h3>Caminhos</h3><div class="caminhos">${caminhos || '<div class="vazio">nenhum</div>'}</div></div>`;
  const mini = MapaPx.criar(e.mapa, { clicaveis: clic, aoClicar: viajarPara, nivelHeroi: e.heroi.nivel, marcas: marcasContrato(e), dicaDe: dicaDoLugar(e, clic) });
  mini.title = "Abrir o mapa (M)";
  mini.addEventListener("click", (ev) => { if (!ev.target.closest(".clicavel")) alternarMapa(true); });
  $("#mapa-mini").appendChild(mini);
  if (clic.size) $("#mapa-mini").appendChild(el("div", "mapa-dica", "Clique num destino para viajar"));
  raiz.querySelectorAll(".caminho.clicavel").forEach((c) => c.addEventListener("click", () => viajarPara(Number(c.dataset.local))));
  // Passar o mouse num caminho da lista acende o lugar no mapa (os nomes dos vizinhos não estão mais escritos nele).
  raiz.querySelectorAll(".caminho").forEach((c) => {
    c.addEventListener("mouseenter", () => document.querySelectorAll(`.no-btn[data-id="${c.dataset.local}"]`).forEach((b) => b.classList.add("destacado")));
    c.addEventListener("mouseleave", () => document.querySelectorAll(".no-btn.destacado").forEach((b) => b.classList.remove("destacado")));
  });
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
    dicaDe: dicaDoLugar(estado, destinosClicaveis()),
    aoClicar: (id) => { alternarMapa(false); viajarPara(id); } }));
  $("#mapa-legenda").innerHTML = legendaMapa();
}
