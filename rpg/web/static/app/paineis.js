"use strict";

/* ------------------------------------------------------------------ estado e painéis */
const { pct } = Telas;
/** Uma barra. Com `chave`, ela sai da largura que estava na tela (larguraViva): um estado novo no meio da animação
 *  (a poção e, logo depois, outra mudança) continua de onde a barra está, em vez de saltar para o fim. Parada no lugar
 *  certo (a menos de meio ponto: o arredondamento do pixel), sai exatamente dele e não se mexe. */
function barra(classe, atual, maximo, anterior, chave, bloqueado = 0) {
  const alvo = pct(atual, maximo), viva = chave ? larguraViva[chave] : undefined;
  const de = viva !== undefined ? (Math.abs(viva - alvo) < 0.5 ? alvo : viva) : anterior === undefined ? alvo : pct(anterior, maximo);
  // bloqueado: a parte do máximo que uma penalidade tira (a vida do herói com ferimentos ou fome), no fim da barra
  const bloqueio = bloqueado > 0 ? `<span class="bloqueio" style="width:${pct(bloqueado, maximo)}%"></span>` : "";
  return `<span class="barra-px ${classe}"${chave ? ` data-chave="${chave}"` : ""} data-alvo="${alvo}"><span class="rastro" style="width:${de}%"></span><span class="enchimento" style="width:${de}%"></span>${bloqueio}</span>`;
}
const larguraViva = {};
/** Antes de redesenhar um painel: a largura que cada barra com chave mostra agora, em %. Medida contra o lado de dentro
 *  da barra (sem a borda), o mesmo de onde sai a largura em % do enchimento: contra a barra inteira, uma barra cheia
 *  media 98% e, a cada estado novo (comprar uma tocha manda dois), saía um pouco mais curta e enchia de novo. */
function guardarLarguras(raiz) {
  for (const k in larguraViva) delete larguraViva[k];
  raiz.querySelectorAll(".barra-px[data-chave]").forEach((b) => {
    const cs = getComputedStyle(b);
    const dentro = b.getBoundingClientRect().width - parseFloat(cs.borderLeftWidth) - parseFloat(cs.borderRightWidth);
    if (dentro > 0) larguraViva[b.dataset.chave] = (100 * b.querySelector(".enchimento").getBoundingClientRect().width) / dentro;
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
  Orientacao.aoEstado(e);
  Realce.glossario(e.glossario);
  Telas.atualizarGrimorio();
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
    JSON.stringify(antes.contratos) !== JSON.stringify(e.contratos) || JSON.stringify(antes.missoes) !== JSON.stringify(e.missoes) ||
    JSON.stringify(antes.capitulo) !== JSON.stringify(e.capitulo);
  if (mudouMapa) { desenharMundo(e); ultimoMundo = ""; }
  if (!$("#sobre-mapa").hidden && mudouMapa) desenharMapaGrande();
  acomodarRegistro();
  Turnos.aoEstado(e);  // a placa do turno e a iniciativa (turnos.js)
}

/* ------------------------------------------------------------------ o registro nas lutas cheias */
/* Numa luta cheia, cada carta com um efeito ganha uma linha de ícones, e o motor produz isso de verdade (um bando de
   caídos com a Maldição ou o enfraquecer em área: as seis cartas de uma vez, já no segundo turno). Numa janela baixa,
   a arena cresce até o registro embaixo dela sumir. Então, no começo da luta, a conta é feita uma vez: se a coluna
   mais alta, com uma linha de efeitos em cada carta que ainda não tem, deixasse menos de REGISTRO_MIN para o registro,
   ele vai para uma coluna ao lado, embaixo do cabeçalho dela: a do mundo (por cima do minimapa, da missão e dos
   caminhos, que não servem durante a luta; o nome do lugar, o nível e os avisos da noite continuam à vista) ou, sem
   ela (janela abaixo de 1100 px), a da ficha (por cima de atributos, equipamento e bolsa; o nome, o nível e a
   experiência continuam). O que fica por baixo não recebe clique nem foco. A decisão vale enquanto a janela tiver o
   mesmo tamanho: efeitos que entram e saem não mudam nada de lugar. Redimensionar refaz a conta (do jeito que a
   janela ficou), e o fim da luta devolve tudo. Sem coluna ao lado (abaixo de 920 px), o registro fica embaixo da
   arena com a altura de leitura, e a página rola até ele (nessa largura ela já rola). */
const REGISTRO_MIN = 140;   // ~5 linhas do registro
const LINHA_EFEITOS = 28;   // a linha de ícones de uma carta (03-batalha.css: a margem, o fio e o ícone com a borda)
const registroAoLado = { chave: null, coluna: null, cobertos: [] };
function registroSemEspaco() {
  const arena = $("#arena"), pagina = $("#pagina");
  if (!arena || !pagina) return false;
  const colunas = [...document.querySelectorAll("#batalha .aliados, #batalha .inimigos")];
  // a altura que as cartas de cada coluna ocupam (pelo lugar no layout, sem os movimentos) e quanto ela cresceria: uma
  // linha por carta sem efeitos (em duas colunas de inimigos, 1920 px, uma por fileira)
  const ocupa = (c) => {
    const cs = [...c.querySelectorAll(".carta")];
    return cs.length ? Math.max(...cs.map((x) => x.offsetTop + x.offsetHeight)) - Math.min(...cs.map((x) => x.offsetTop)) : 0;
  };
  const crescer = (c) => {
    const sem = [...c.querySelectorAll(".carta")].filter((x) => !x.querySelector(".carta-efeitos .ef")).length;
    return (c.classList.contains("duas") ? Math.ceil(sem / 2) : sem) * LINHA_EFEITOS;
  };
  const hoje = Math.max(0, ...colunas.map(ocupa)), depois = Math.max(0, ...colunas.map((c) => ocupa(c) + crescer(c)));
  // o registro de agora, com a arena já na altura final (ela pode estar crescendo neste instante: batalha.js, acomodar)
  const livre = pagina.getBoundingClientRect().height - ((arena._altura || arena.offsetHeight) - arena.getBoundingClientRect().height);
  return livre - (depois - hoje) < REGISTRO_MIN;
}
/** Onde o registro vai: a coluna à vista (o mundo antes da ficha) e o primeiro pedaço dela que ele cobre. */
function colunaParaRegistro() {
  const visivel = (x) => x && x.getClientRects().length;
  const mundo = $("#mundo"), ficha = $("#heroi");
  if (visivel(mundo) && !corpo.classList.contains("mostrar-mundo")) return { painel: mundo, desde: () => $("#mapa-mini") };
  if (visivel(ficha) && !corpo.classList.contains("mostrar-heroi")) {
    return { painel: ficha, desde: () => { const xp = ficha.querySelector(".xp-linha"); return xp && xp.nextElementSibling; } };
  }
  return null;
}
function soltarRegistro() {
  const cena = $("#cena");
  if (cena) ["position", "left", "top", "width", "height", "maxWidth", "zIndex"].forEach((k) => { cena.style[k] = ""; });
  registroAoLado.cobertos.forEach((x) => { x.inert = false; });
  registroAoLado.cobertos = [];
  corpo.classList.remove("registro-ao-lado", "registro-rola");
  delete corpo.dataset.registro;
}
function colocarRegistro(col) {
  const cena = $("#cena"), desde = col.desde();
  const p = col.painel.getBoundingClientRect();
  const topo = Math.round((desde ? desde.getBoundingClientRect().top : p.top + p.height / 3) - 4);
  Object.assign(cena.style, { position: "fixed", left: Math.round(p.left) + "px", top: topo + "px", width: Math.round(p.width) + "px",
    height: Math.round(p.bottom - topo) + "px", maxWidth: "none", zIndex: 6 });
  // o painel é redesenhado a cada estado: o que está embaixo do registro fica inerte de novo
  registroAoLado.cobertos.forEach((x) => { x.inert = false; });
  registroAoLado.cobertos = [...col.painel.children].filter((x) => x.getBoundingClientRect().bottom > topo + 1);
  registroAoLado.cobertos.forEach((x) => { x.inert = true; });
  corpo.classList.add("registro-ao-lado");
  corpo.dataset.registro = col.painel.id;
}
function acomodarRegistro() {
  if (!corpo.classList.contains("em-combate") || !$("#batalha .carta")) {
    if (registroAoLado.chave) { soltarRegistro(); registroAoLado.chave = registroAoLado.coluna = null; }
    return;
  }
  const chave = `${innerWidth}x${innerHeight}`;
  if (registroAoLado.chave !== chave) {  // o começo da luta ou a janela de outro tamanho: a conta de novo
    registroAoLado.chave = chave;
    soltarRegistro();
    const falta = registroSemEspaco();
    registroAoLado.coluna = falta ? colunaParaRegistro() : null;
    if (falta && !registroAoLado.coluna) { corpo.classList.add("registro-rola"); corpo.dataset.registro = "embaixo, a página rola"; }
  }
  if (registroAoLado.coluna) colocarRegistro(registroAoLado.coluna);
}
let ajusteRegistro = 0;  // depois do batalha.js reacomodar a arena (150 ms depois do último resize)
addEventListener("resize", () => { clearTimeout(ajusteRegistro); ajusteRegistro = setTimeout(acomodarRegistro, 200); });

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
  const imgs = icones.map((n) => Icones.recurso(n) || spr(n, 2)).join("");
  const dica = opts.titulo ? Telas.dica(esc(opts.titulo), true) : "";
  return `<div class="recurso${opts.alerta ? " alerta" : ""}${opts.vazio ? " vazio" : ""}" data-rec="${id}" ${dica}>
    <div class="icones">${imgs}</div><div class="qtd">${qtd}</div></div>`;
}

/* O kit equipado na barra (1.211.1): consulta. Cada habilidade é um botão com a dica (nome, custo, o que faz; a
   ultimate marcada); fora da luta, o clique abre a página dela no Grimório, que diz se dá para trocar ali (o motor
   oferece a troca só na vila e na fogueira). Na luta a barra some (09-comitiva.css): as ações seguem na roda, na sua
   vez. Sem espaço (a janela estreita), a fileira vira o botão "Kit · N", que abre a mesma lista. */
let kitAberto = false;
function dicaKit(k, h) {
  const emLuta = !!(estado && estado.combate);
  return `<b>${esc(k.nome)}</b>${k.ultimate ? ' <span class="tag-ultimate">Ultimate · 1 vez por luta</span>' : ""}` +
    `<div class="tipo">${k.custo ? `${k.custo} de ${esc(h.recurso)}` : "Sem custo"}</div><div class="bonus">${Realce.texto(k.desc)}</div>` +
    (k.usada ? '<div class="pior">Já usada nesta luta.</div>' : "") +
    `<div class="rodape">${emLuta ? "Na sua vez, pela ação Habilidades." : "O kit se troca na vila ou na fogueira."}</div>`;
}
function botaoKit(k, h, lista) {
  return `<button type="button" class="kit-hab${k.ultimate ? " ultimate" : ""}${k.usada ? " usada" : ""} el-${esc(k.familia || "arcano")}" data-kit-hab="${esc(k.id)}" aria-label="${esc(k.nome)}" ${Telas.dica(dicaKit(k, h))}>` +
    `${spr(k.icone || "estrela", 2)}${lista ? `<span class="kit-nome">${esc(k.nome)}</span><span class="kit-custo">${k.custo || "grátis"}</span>` : ""}</button>`;
}
function kitHud(h) {
  const kit = h.kit || [];
  if (!kit.length) return `<div class="hud-kit vazio"><button type="button" class="kit-vazio" data-kit-hab="" ${Telas.dica("<b>Kit vazio</b><div>Nenhuma habilidade vai para a luta. Monte o kit no Grimório, na vila ou na fogueira.</div>")}>Kit vazio</button></div>`;
  const ult = kit.some((k) => k.ultimate);
  return `<div class="hud-kit${kitAberto ? " aberto" : ""}" role="group" aria-label="Kit equipado">
    <div class="kit-fileira">${kit.map((k) => botaoKit(k, h)).join("")}</div>
    <button type="button" class="kit-recolhido" aria-expanded="${kitAberto}" aria-controls="kit-lista" aria-label="Kit: ${Texto.plural(kit.length, "habilidade")}${ult ? ", com a ultimate" : ""}">Kit · ${kit.length}<span class="kit-palavra"> ${kit.length === 1 ? "habilidade" : "habilidades"}</span>${ult ? ' <i class="kit-ult" aria-hidden="true">◆</i>' : ""}</button>
    <div class="kit-lista" id="kit-lista">${kit.map((k) => botaoKit(k, h, true)).join("")}</div></div>`;
}
function ligarKitHud(h) {
  const caixa = $("#hud-linha .hud-kit");
  if (!caixa) return;
  medirKit();
  caixa.querySelectorAll("[data-kit-hab]").forEach((b) => b.addEventListener("click", (ev) => {
    ev.stopPropagation();
    if (estado && estado.combate) return;  // na luta, só consulta: a ação é na roda, na sua vez
    Telas.abrirGrimorio(b.dataset.kitHab || null);
  }));
  const rec = caixa.querySelector(".kit-recolhido");
  if (rec) rec.addEventListener("click", (ev) => {
    ev.stopPropagation();
    kitAberto = !kitAberto;
    caixa.classList.toggle("aberto", kitAberto);
    rec.setAttribute("aria-expanded", String(kitAberto));
    if (kitAberto) { const p = caixa.querySelector(".kit-lista [data-kit-hab]"); if (p) p.focus(); }
  });
  caixa.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape" && kitAberto) { ev.stopPropagation(); kitAberto = false; caixa.classList.remove("aberto"); if (rec) { rec.setAttribute("aria-expanded", "false"); rec.focus(); } }
  });
}
/** Recolhe a fileira só quando ela não cabe: a linha da barra, com a fileira aberta, transbordaria (as barras já no
 *  mínimo delas, 180 px). Mede só com a barra à vista (na luta ela some: largura zero não decide nada) e de novo a
 *  cada mudança de largura (a janela, o zoom, a barra voltando depois da luta: o ResizeObserver abaixo). */
function medirKit() {
  const linha = $("#hud-linha"), caixa = linha && linha.querySelector(".hud-kit");
  if (!caixa || !linha.offsetParent || !linha.clientWidth) return;
  caixa.classList.remove("recolhida", "curta");
  if (linha.scrollWidth > linha.clientWidth + 1) caixa.classList.add("recolhida");
  if (linha.scrollWidth > linha.clientWidth + 1) caixa.classList.add("curta");  // nem o botão cabe: "Kit · 4"
}
if (window.ResizeObserver) {
  let quadro = 0;
  const obs = new ResizeObserver(() => { cancelAnimationFrame(quadro); quadro = requestAnimationFrame(medirKit); });
  const ligar = () => { const l = $("#hud-linha"); if (l) obs.observe(l); else setTimeout(ligar, 200); };
  ligar();
}

document.addEventListener("click", (ev) => {  // clicar fora fecha a lista do kit recolhido
  if (!kitAberto || ev.target.closest(".hud-kit")) return;
  kitAberto = false;
  const c = document.querySelector("#hud-linha .hud-kit"); if (c) c.classList.remove("aberto");
});

function desenharHud(h, antes) {
  // Um desenho para "acabou" e outro para "tem": o número ao lado diz quanto.
  const comida = [h.provisoes ? "pernil" : "osso_diag"];
  const tochas = [h.tochas ? "tocha" : "tocha_apagada"];  // as duas em 24, pelo Icones.recurso (a apagada: 1.136.0)
  const ouro = [h.ouro ? "moedas" : "bolsa_vazia"];
  const pocoes = [h.pocoes ? "pocao" : "frasco_vazio"];
  Sensacao.vidaDoHeroi(h.hp, h.max_hp, h.vida_por_um_fio);
  guardarLarguras($("#hud-linha"));
  // Ferimentos e fome tiram parte da vida máxima (o motor: vida_bloqueio): a barra mede a vida saudável, com a parte
  // bloqueada no fim, e o número é vida/saudável. O quanto e por quê ficam na linha das condições (a coluna dos números
  // e as barras não mudam de tamanho quando o bloqueio entra ou sai) e na dica da vida.
  const vb = h.vida_bloqueio, vidaMax = vb ? vb.saudavel : h.max_hp;
  const dicaVida = () => (vb ? Telas.dica(`<b>Vida ${h.hp} de ${vb.limite}</b><div>${esc(vb.dica[0])}</div>` +
    `<div class="bonus pior">${vb.fontes.map((f) => `${esc(f.nome)} −${f.pct}% (−${f.perda})`).join("<br>")}</div>` +
    `<div class="rodape">${esc(vb.dica[1])}</div>`) : Telas.dica("Vida", true));
  const bloqueioVida = vb ? `<span class="condicao bloqueio-vida" ${dicaVida()}><i class="amostra"></i>${spr("cadeado", 1)}−${vb.bloqueado} de vida máxima</span>` : "";
  const feridas = h.ferimentos.length ? `<div class="recurso alerta" data-rec="feridas" ${Telas.dica(h.ferimentos.map((f) => `<b>${esc(f.nome)}</b><div class="bonus pior">${esc((f.explica || [""])[0])}</div>`).join("") + '<div class="rodape">Detalhes no painel do herói, à esquerda.</div>')}><div class="icones">${spr("gota", 2)}</div><div class="qtd">${h.ferimentos.length}</div></div>`
    // sem ferimento, o lugar da gota fica guardado (invisível): as barras não mudam de comprimento quando um ferimento
    // chega ou sara (a hachura da vida bloqueada já mostra a mudança; o conjunto não encolhe junto)
    : `<div class="recurso reserva" aria-hidden="true"><div class="icones">${spr("gota", 2)}</div><div class="qtd">0</div></div>`;
  $("#hud-linha").innerHTML = `
    <div class="hud-retrato" title="${esc(h.titulo)} nível ${h.nivel}">${Icones.cabeca(h.classe) || spr(h.classe, 3)}<span class="nivel">${h.nivel}</span></div>
    <div class="hud-vitais">
      <div class="vital" data-vital="hp" ${dicaVida()}>${Icones.vital("Vida") || spr("coracao", 1)}${barra("vida", h.hp, vidaMax, antes ? antes.hp : undefined, "hud-hp", vb ? vb.bloqueado : 0)}<span class="num">${h.hp}/${vidaMax}</span></div>
      <div class="vital" data-vital="rec" ${Telas.dica(esc(h.recurso), true)}>${Icones.vital(h.recurso) || spr(RECURSO_ICONE[h.recurso] || "estrela", 1)}${barra(RECURSO_BARRA[h.recurso] || "mana", h.rec, h.max_rec, antes ? antes.rec : undefined, "hud-rec")}<span class="num">${h.rec}/${h.max_rec}</span></div>
      <div class="hud-condicoes">${bloqueioVida}${(h.condicoes || []).map((c) => `<span class="condicao${c.grave ? " grave" : ""}" data-condicao="${esc(c.id)}" ${Telas.dica(`<b>${esc(c.texto)}</b>${c.dica.map((l) => `<div>${esc(l)}</div>`).join("")}`)}>${spr(c.icone, 1)}${esc(c.texto)}</span>`).join("")}</div>
    </div>
    ${kitHud(h)}
    <div class="hud-recursos">
      ${recurso("provisoes", comida, `${h.provisoes}<small>d</small>`, { alerta: h.provisoes <= 1, vazio: !h.provisoes, titulo: h.provisoes ? `Comida para ${Texto.plural(h.provisoes, "dia")}. Cada dia consome 1 (e cada companheiro come também).` : "Sem comida! Você vai passar fome." })}
      ${recurso("tochas", tochas, h.tochas, { alerta: h.tochas === 0, vazio: !h.tochas, titulo: "Tochas: luz para a noite, ruínas e a cidadela." })}
      ${recurso("ouro", ouro, h.ouro, { vazio: !h.ouro, titulo: h.ouro ? `Ouro: ${Texto.plural(h.ouro, "moeda")}` : "Sem ouro" })}
      ${recurso("pocoes", pocoes, h.pocoes, { vazio: !h.pocoes, titulo: "Poções de vida (35% da vida)" })}
      ${recurso("bandagens", ["bandagem"], h.bandagens, { vazio: !h.bandagens, alerta: !h.bandagens && h.ferimentos.some((f) => f.aberto), titulo: "Bandagens: enfaixam feridas abertas contra infecção" })}
      ${h.flechas !== null && h.flechas !== undefined ? recurso("flechas", ["aljava"], h.flechas, { alerta: h.flechas <= 8, titulo: `Flechas (a aljava leva ${h.max_flechas || 30})` }) : ""}
      ${feridas}
    </div>`;
  animarBarras($("#hud-linha"));
  ligarKitHud(h);
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

// O quadro dos atributos na ficha lateral (1.211.1): os seis e a Presença, o crítico e a Tenacidade, e o "+" quando há
// pontos; o mesmo desenho e os mesmos dados da ficha (inventario.js, baseHtml). Aberto ou fechado, fica como você deixou.
let atributosAbertos = false;

function desenharHeroi(h, antes) {
  guardarLarguras($("#heroi"));
  const attrs = Telas.atributosHtml(h);
  const slot = (s) => {
    const it = h.equip[s];
    if (!it) return `<div class="slot-px mini vazio" data-mini="${s}" title="${esc(Telas.NOME_ESPACO[s])} (vazio)">${Icones.vazio(s, 32) || spr(Telas.VAZIO[s], 2, "fantasma")}</div>`;
    return `<div class="slot-px mini r-${esc(it.raridade)}" data-mini="${s}" ${Telas.dicaItem(it, "", false)}>${Icones.item(Telas.iconeItem(it)) || spr(Telas.iconeItem(it), 2)}</div>`;
  };
  const feridas = h.ferimentos.length ? h.ferimentos.map((f) => `<div class="ferimento${f.aberto ? " aberto" : ""}" data-ferimento="${esc(f.id)}" ${Telas.dica(`<b>${esc(f.nome)}</b><div class="tipo">${f.dias ? `${Texto.plural(f.dias, "dia")} para sarar` : "não sara sozinha"}${f.aberto ? " · ferida aberta" : ""}</div>${(f.explica || []).map((l, i) => `<div class="${i ? "" : "bonus pior"}">${esc(l)}</div>`).join("")}`)}>${spr("gota", 1)}${esc(f.nome)} <small>${f.dias ? f.dias + "d" : ""}${f.aberto ? " · aberto" : ""}</small></div>`).join("")
    : '<div class="vazio">Nenhum, por enquanto.</div>';
  const bolsa = h.bolsa.filter((b) => b.id !== "tocha").map((b) => {
    const bau = b.id === "bau";  // o baú se abre (e, onde dá para abrir, ganha o anel dourado)
    // O que ele trata agora (o motor diz): a dica abre com isso, e o espaço pulsa até ser usado. Sem nada a tratar
    // (a bandagem sem ferida aberta), o espaço fica apagado e o rodapé diz por quê.
    const trata = !b.motivo && b.trata;
    const dica = `<b>${esc(b.nome)}</b>${trata ? `<div class="bonus melhor">${esc(b.trata)}</div>` : ""}<div>${Realce.texto(b.desc)}</div>${(() => { const r = b.motivo ? esc(b.motivo) : bau ? (b.qtd > 1 ? `Abre os ${b.qtd} de uma vez.` : "") : estado && estado.combate ? "Gasta o turno." : ""; return r ? `<div class="rodape">${r}</div>` : ""; })()}`;
    return `<div role="button" tabindex="0" class="slot-px usavel${b.motivo && !(b.alvos || []).some((a) => !a.motivo) ? " inutil" : ""}${bau && !b.motivo ? " pronto" : ""}${trata ? " trata" : ""}" data-bolsa="${esc(b.id)}" ${Telas.dica(dica)}>${Icones.consumivel(b.id) || spr(Telas.iconeConsumivel(b.id), 2)}<span class="qtd">${b.qtd}</span></div>`;
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
    '<div class="rodape">A poção da bolsa também serve nele. Na fogueira, um carinho.</div>') : "";
  const fera = f ? `<div class="membro fera${f.hp <= 0 ? " ferido" : ""}" data-fera="1">
      <div class="icone" ${dicaFera}>${Icones.animal(f.tipo, 32) || spr(f.tipo === "falcao" ? "voador" : "fera", 2)}</div>
      ${linhaNome(f.nome, f.animado ? ' <b class="fera-animado" title="animado">♥</b>' : "", f.hp, f.max_hp, dicaFera)}
      ${barra("vida fina", Math.max(0, f.hp), f.max_hp, antes && antes.companheiro ? Math.max(0, antes.companheiro.hp) : undefined, "fera")}</div>` : "";
  const membros = (h.comitiva || []).map((m) => {
    const d = Telas.dica(`<b>${esc(m.nome)}</b><div class="tipo">${esc(m.titulo)}</div><div>${esc(m.desc || "")}</div>` +
      (m.ferido ? "<div class=\"bonus pior\">Ferido: fora de combate até descansar.</div>" : "") +
      (m.fora ? `<div class="bonus pior">${esc(m.fora.texto)}</div>` : "") +
      `<div class="rodape">${m.conversa ? "Quer conversar: clique no ✉." : "Mais na aba Comitiva."}</div>`);
    const carta = m.conversa ? ` <button type="button" class="membro-carta" data-conversar="${esc(m.id)}" title="${esc(m.nome.split(" ").pop())} quer conversar">✉</button>` : "";
    const velho = antes && (antes.comitiva || []).find((x) => x.id === m.id);  // a barra sai de onde estava
    return `<div class="membro${m.ferido || m.fora ? " ferido" : ""}" data-cid="${esc(m.id)}">
      <div class="icone" ${d}>${Icones.cabeca(m.id, 32) || spr(m.id, 2)}</div>
      ${linhaNome(m.nome, carta, m.hp, m.max_hp, d)}
      ${barra("vida fina", m.hp, m.max_hp, velho ? velho.hp : undefined, "m-" + m.id)}${Telas.aprovacao(m)}</div>`;
  }).join("");
  const comitiva = membros || fera ? `<div class="secao"><h3>Comitiva</h3>${membros}${fera}</div>` : "";
  $("#heroi").innerHTML = `
    <div class="identidade"><div class="retrato-grande">${Icones.retrato(h.classe, "Retrato do herói") || spr(h.classe, 3)}</div>
      <div><div class="heroi-nome">${esc(h.nome)}</div><div class="heroi-titulo">${esc(h.titulo)} • nível&nbsp;${h.nivel}</div></div></div>
    <div class="xp-linha"><div class="legenda-linha"><span>Experiência</span><span>${h.xp}/${h.xp_proximo}</span></div>${barra("xp", h.xp, h.xp_proximo, antes && antes.nivel === h.nivel ? antes.xp : undefined, antes && antes.nivel === h.nivel ? "xp" : undefined)}</div>
    ${h.pontos_talento ? `<div class="talento-linha"><button type="button" class="talento-aviso" data-atalho="Talentos"><span class="estrela">${Icones.atalho("Talentos", 32) || spr("estrela", 2)}</span><span class="talento-texto">${Texto.plural(h.pontos_talento, "ponto de talento", "pontos de talento").replace(/^\d+/, (n) => `<b>${n}</b>`)}</span><span class="talento-abrir" aria-hidden="true">▸</span></button></div>` : ""}
    <div class="secao"><h3>Atributos</h3><div class="atributos">${attrs}</div>${Telas.testesHtml(h)}
      <button type="button" class="atributos-abrir${h.pontos_atributo ? " com-pontos" : ""}" aria-expanded="${atributosAbertos}" aria-controls="atributos-quadro">
        <span class="icone-attr" aria-hidden="true">${spr("estrela", 1)}</span><span class="nome">Atributos</span>${h.pontos_atributo ? `<b class="attr-livres">· +${h.pontos_atributo}</b>` : ""}<span class="seta" aria-hidden="true">›</span></button>
      <div class="atributos-quadro" id="atributos-quadro"${atributosAbertos ? "" : " hidden"}>${Telas.atributosBaseHtml(h, true)}</div></div>
    <div class="secao"><h3>Equipado</h3><div class="equip-mini">${Object.keys(Telas.AREA).map(slot).join("")}</div></div>
    ${comitiva}
    <div class="secao"><h3>Ferimentos</h3>${feridas}</div>
    <div class="secao"><h3>Bolsa</h3><div class="slots">${bolsa || '<span class="vazio">vazia</span>'}</div></div>
    <div class="secao"><h3>Reputação</h3>${Telas.reputacaoHtml(h)}</div>`;
  acomodarNome();
  const abrir = $("#heroi .atributos-abrir");
  if (abrir) abrir.addEventListener("click", (ev) => {
    ev.stopPropagation();
    atributosAbertos = !atributosAbertos;
    abrir.setAttribute("aria-expanded", String(atributosAbertos));  // a seta gira pelo CSS (14-hud.css)
    $("#atributos-quadro").hidden = !atributosAbertos;
  });
  Telas.ligarMaisAtributo($("#heroi"));
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

/** O nome do herói ao lado do retrato, no tamanho de sempre. Se não cabe ali (passa da borda, ou quebra em mais de duas
 *  linhas), ganha uma linha própria acima do retrato, na largura do painel, no mesmo tamanho; só uma palavra que nem
 *  assim cabe (ou que ainda passa de duas linhas) desce ao passo de pixel seguinte (16). Os nomes que cabem não mudam. */
function acomodarNome() {
  const id = $("#heroi .identidade"), n = id && id.querySelector(".heroi-nome");
  if (!n) return;
  id.classList.remove("nome-longo", "nome-enorme");
  const linhas = () => Math.round(n.getBoundingClientRect().height / parseFloat(getComputedStyle(n).lineHeight));
  const sobra = () => n.scrollWidth > n.clientWidth + 1;
  if (sobra() || linhas() > 2) id.classList.add("nome-longo");
  if (sobra() || linhas() > 2) id.classList.add("nome-enorme");
}
window.addEventListener("resize", () => { if (estado) acomodarNome(); });

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
    habMirando = b.nome;  // se pedir em quem, o lembrete diz o quê ("Poção de Vida", "escolha o alvo")
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
/** Os lugares com "!" no mapa: os dos contratos em andamento e o do objetivo da missão. */
function marcasContrato(e) {
  return new Set([...(e.contratos || []).filter((c) => !c.concluido).map((c) => c.lugar_id),
    ...(e.missoes || []).map((m) => m.lugar_id).filter((id) => id !== null && id !== undefined)]);
}
/** A dica de um lugar no mapa (hover): o nome, o tipo, o perigo, a distância e os contratos que você tem lá. */
function dicaDoLugar(e, clic) {
  const porLugar = {};
  (e.contratos || []).filter((c) => !c.concluido).forEach((c) => { (porLugar[c.lugar_id] = porLugar[c.lugar_id] || []).push(c); });
  return (n) => `<b>${esc(n.nome)}</b><div class="tipo">${esc(maiuscula(n.descricao))}` +
    (n.nivel ? ` · <span class="nivel-cam ${nivelPerigo(n.nivel)}">${n.tipo === "vila" ? "arredores" : "inimigos"} Nv.${n.nivel}</span>` : "") +
    (n.distancia ? ` · ${Texto.plural(n.distancia, "trecho")}` : n.atual ? " · você está aqui" : "") + "</div>" +
    (porLugar[n.id] || []).map((c) => `<div class="dica-contrato">${spr("pergaminho", 1)}<span>${esc(c.desc)}</span></div>`).join("") +
    (e.missoes || []).filter((m) => m.lugar_id === n.id).map((m) => `<div class="dica-contrato">${spr("pergaminho", 1)}<span>${esc(m.nome)}: ${esc(m.objetivo)}</span></div>`).join("") +
    "";
}

function desenharMundo(e) {
  const l = e.local;
  const clic = destinosClicaveis();
  const caminhos = e.mapa.nos.filter((n) => n.distancia).sort((a, b) => a.distancia - b.distancia || a.nome.localeCompare(b.nome))
    // o símbolo do minimapa (32, 1:1; desde a 1.200.1), as marcas do mapa ao lado do nome e a cancela no destino que a
    // viagem recusa (o `bloqueio` do motor)
    .map((n) => `<div class="caminho${clic.has(n.id) ? " clicavel" : ""}${n.bloqueio ? " bloqueado" : ""}" data-local="${n.id}">${MapaPx.simboloHTML(n)}
      <span class="nome"><span class="caminho-nome">${esc(n.nome)}${MapaPx.marcasHTML(n.id)}${n.bloqueio ? MapaPx.bloqueioHTML(n.bloqueio) : ""}</span><small>${n.nivel ? `<span class="nivel-cam ${nivelPerigo(n.nivel)}">Nível ${n.nivel}</span> · ` : ""}${esc(n.descricao)}</small></span>
      <span class="dist">${Texto.plural(n.distancia, "trecho")}</span></div>`).join("");
  const raiz = $("#mundo");
  raiz.innerHTML = `<div class="local-nome">${esc(l.nome)}</div><div class="local-desc">${esc(maiuscula(l.descricao))}</div>
    ${l.nivel ? `<span class="perigo-tag ${nivelPerigo(l.nivel)}">${l.tipo === "vila" ? "Arredores" : "Inimigos"} Nv.${l.nivel}</span>` : ""}
    ${(l.riscos || []).length ? `<div class="riscos-lugar">${l.riscos.map((r) => `<div class="risco-lugar ${esc(r.tipo || "")}">${Icones.miudo(r.icone) || spr(r.icone, 1)}<span>${esc(r.texto)}</span></div>`).join("")}</div>` : ""}<div id="mapa-mini"></div>
    ${Telas.rastreador(e.contratos, e.heroi.nivel, e.missoes, e.capitulo)}
    <div class="secao"><h3>Caminhos</h3><div class="caminhos">${caminhos || '<div class="vazio">nenhum</div>'}</div></div>`;
  const mini = MapaPx.criar(e.mapa, { caixa: $("#mapa-mini"), clicaveis: clic, aoClicar: viajarPara, nivelHeroi: e.heroi.nivel, marcas: marcasContrato(e), dicaDe: dicaDoLugar(e, clic) });
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
      const i = c.dataset.missao ? opcaoMissao(c.dataset.missao) : opcaoCacar(Number(c.dataset.contrato));
      if (i >= 0) responder(pergunta.id, i);
      else if (clic.has(id)) viajarPara(id);
    });
    c.addEventListener("mouseenter", () => document.querySelectorAll(`.no-btn[data-id="${id}"]`).forEach((b) => b.classList.add("destacado")));
    c.addEventListener("mouseleave", () => document.querySelectorAll(".no-btn.destacado").forEach((b) => b.classList.remove("destacado")));
  });
}

function desenharMapaGrande() {
  if (!estado) return;
  const caixa = $("#mapa-grande");
  caixa.innerHTML = "";
  caixa.appendChild(MapaPx.criar(estado.mapa, { grande: true, caixa, clicaveis: destinosClicaveis(), nivelHeroi: estado.heroi.nivel, marcas: marcasContrato(estado),
    dicaDe: dicaDoLugar(estado, destinosClicaveis()),
    aoClicar: (id) => { alternarMapa(false); viajarPara(id); } }));
  $("#mapa-legenda").innerHTML = MapaPx.legenda(estado);  // só o que o mapa conhecido mostra, e as marcas
}
