"use strict";

/* ------------------------------------------------------------------ página */
function anexar(no) { textoEl.appendChild(no); rolarFim(); return no; }
function rolarFim() {
  if (rolagemFixa !== null) pagina.scrollTop = rolagemFixa;
  else if (seguir && !presoNoTopo) pagina.scrollTop = pagina.scrollHeight;
}
/* A página de um lugar fica no topo (a arte, o nome, as ações), mesmo que as ações passem um pouco do pé da tela; o
   que vier depois de uma escolha volta a puxar a página (responder solta). */
let presoNoTopo = false;
/* Telas que se redesenham no lugar (mural, mercado, inventário, fogueira) não podem pular: a rolagem fica onde a
   pessoa estava até as novas opções chegarem, e a altura que a página já teve fica segura enquanto a tela é a mesma
   (se o conteúdo encolhe, sobra espaço embaixo em vez de a página saltar). Só uma cena nova solta a altura. */
let rolagemFixa = null;
let ancora = null;  // onde a tela desenhada (.tela) estava na janela: a nova volta para o mesmo lugar
let cenaInterrompida = false;  // houve luta ou saque desde a última cena (ver novaCena)
const topoTela = () => { const t = textoEl.querySelector(".tela"); return t ? t.getBoundingClientRect().top - pagina.getBoundingClientRect().top : null; };
function fixarRolagem() {
  rolagemFixa = pagina.scrollTop;
  ancora = topoTela();
  // A altura vai na folha inteira, não no texto: no texto, o min-height mudaria a margem da última linha.
  folha.style.minHeight = folha.offsetHeight + "px";
}
function soltarRolagem() {
  if (rolagemFixa === null) return;
  pagina.scrollTop = rolagemFixa;
  // Se algo acima da tela sumiu no redesenho (um aviso da cena anterior), a tela não sobe: a rolagem compensa.
  const agora = topoTela();
  if (ancora !== null && agora !== null) pagina.scrollTop += agora - ancora;
  rolagemFixa = null; ancora = null;
}
pagina.addEventListener("scroll", () => {
  seguir = pagina.scrollTop + pagina.clientHeight >= pagina.scrollHeight - 80;
  if (pagina.scrollTop > 48) recolherArte(true);
}, { passive: true });
// A arte volta inteira rolando para cima já no começo da página (nunca sozinha: crescer de volta encolheria o
// texto, que voltaria a rolar, e a arte ficaria indo e vindo).
pagina.addEventListener("wheel", (ev) => { if (ev.deltaY < 0 && pagina.scrollTop <= 0) recolherArte(false); }, { passive: true });

/** A arte do lugar fica presa no topo da cena. Quando o texto passa a precisar de rolagem, ela se recolhe numa
 *  faixa baixa e o espaço vai para a leitura; volta inteira na cena seguinte. */
function recolherArte(sim) { cenaEl.classList.toggle("recolhido", sim); }

/** O Voltar das telas de menu mora na barra do topo da cena, fora da área que rola: nunca cobre o conteúdo.
 *  Sem `acao`, sai. Entre uma resposta e o redesenho da mesma tela ele fica (um clique ali não vale: a pergunta
 *  já é outra), para a barra não piscar. */
function porVoltar(rotulo, acao) {
  barraTela.querySelector(".voltar-seta")?.remove();
  if (!acao) return;
  const b = el("button", "voltar-seta", `<span>◀</span> ${esc(rotulo)}<kbd>Esc</kbd>`);
  b.type = "button";
  b.addEventListener("click", (ev) => { ev.stopPropagation(); acao(); });
  barraTela.prepend(b);
}
const emMenu = () => cenaEl.dataset.tipo === "menu";

/** Gótico em CAIXA ALTA é ilegível: "O ÚLTIMO GUARDA" vira "O Último Guarda". */
const MIUDAS = new Set(["de", "da", "do", "das", "dos", "e", "em", "of", "the", "a", "o", "os", "as"]);
function suavizar(t) {
  t = String(t ?? "");
  // Palavra a palavra: "GUARDIÃO: Ulric, o Lich Menor" vira "Guardião: Ulric, o Lich Menor".
  // Siglas curtas (PV, XP) ficam; palavras já em caixa baixa ou capitalizadas também.
  return t.replace(/[\p{L}']+/gu, (p, i) => {
    const baixa = p.toLowerCase();
    if (p.length < 2 || (p.length < 3 && !MIUDAS.has(baixa)) || p !== p.toUpperCase() || p === baixa) return p;
    return i > 0 && MIUDAS.has(baixa) ? baixa : baixa[0].toUpperCase() + baixa.slice(1);
  });
}
App.suavizar = suavizar;

let ultimoLugar = "";  // o último lugar com título no histórico
function cabecalho(m) {
  Telas.esconderDica();
  cab.dataset.tipo = cenaEl.dataset.tipo = m.tipo || "evento";
  // Telas de menu (mercado, inventário, mural...): o título vai para a barra do topo, junto do Voltar, e a arte sai;
  // a cena inteira fica para a tela. Nas cenas da história, o título abre a página, embaixo da arte.
  if (m.tipo === "menu") { if (cab.parentElement !== barraTela) barraTela.appendChild(cab); }
  else if (cab.parentElement !== folha) folha.prepend(cab);
  cab.innerHTML = `<h1 class="cena-titulo">${esc(suavizar(m.titulo))}</h1><div class="ornamento"><i></i><b></b><i></i></div>` +
    (m.subtitulo ? `<div class="cena-sub">${esc(m.subtitulo)}</div>` : "");
  corpo.classList.toggle("modo-titulo", m.tipo === "titulo");
  if (m.tipo === "titulo") {
    corpo.classList.add("sem-heroi"); corpo.classList.remove("em-combate"); estado = null; ultimoLugar = "";
    Sensacao.vidaDoHeroi(1, 1);  // no título não há herói: sem borda vermelha nem coração
    const [r, g, b] = Vista.titulo();  // a paisagem desce até o rodapé; o céu de cima continua na mesma cor
    corpo.style.setProperty("--ceu-titulo", `rgb(${r}, ${g}, ${b})`);
  }
  capitular = ["evento", "local", "chefe", "vitoria", "morte"].includes(m.tipo);
  // O histórico é o diário da jornada: tela de menu não ganha título (a escolha que levou até ela já conta), e o
  // nome do lugar só volta quando o lugar muda (voltar ao menu da vila depois do mercado não repete o nome).
  if (m.tipo === "local") { if (m.titulo !== ultimoLugar) historico("h-cena", m.titulo); ultimoLugar = m.titulo; }
  else if (m.tipo !== "menu") historico("h-cena", m.titulo);
  if (m.titulo !== "Talentos") Telas.fecharTalentos();
}

/** O fim de um evento ou de uma luta cai direto no lugar, sem Continuar: o que aconteceu fica o tempo de ler (um fio
 *  vai se enchendo embaixo; clique ou tecla adianta) e a página vira limpa, no topo, com a arte inteira, o nome do
 *  lugar e as ações. O texto não fica sobrando em cima do lugar: quem quiser rever abre o histórico (H). */
const GUARDA_LEITURA = 700;  // ms em que um clique não vira a página: o resultado aparece e fica à vista
async function virarParaLugar(m) {
  const novo = [...textoEl.querySelectorAll(":scope > :not(.lido):not(.eco):not(.passado)")]
    .reduce((n, x) => n + x.textContent.trim().length, 0);
  if (!replay && novo) {
    // Leu enquanto o texto corria: o tempo desde a escolha conta. Depois de uma luta, a faixa da vitória e o espólio
    // já foram a leitura.
    const ja = performance.now() - ultimaResposta;
    const ms = cenaInterrompida ? 1000 : novo < 80 ? Math.max(700, Math.min(1500, 800 + novo * 30 - ja))
      : Math.max(1300, Math.min(5500, 800 + novo * 30 - ja));
    Telas.esconderDica();
    promptEl.innerHTML = `<div class="virando" aria-hidden="true"><i style="--dura:${Math.round(ms)}ms"></i></div>`;
    // O clique que caiu enquanto o texto corria só terminou o texto: a leitura começa agora. E nos primeiros instantes
    // a página não aceita clique, para um clique certeiro na hora em que o resultado aparece não o pular sem ser lido.
    pular = false;
    const agora = performance.now(), guarda = agora + GUARDA_LEITURA, ate = agora + ms;
    while (performance.now() < ate) {
      if (pular) { if (performance.now() < guarda) pular = false; else break; }
      await espera(40);
    }
  }
  await novaCena(Object.assign({}, m, { virar: false }));
}

let tituloAtual = "";
async function novaCena(m) {
  if (m.virar) { await virarParaLugar(m); return; }
  // Inventário e mercado se redesenham sem piscar. Mas se no meio houve luta ou saque, a página mudou de verdade:
  // aí é cena nova, e o texto do que aconteceu (a noite caiu, o item equipado) fica na página em vez de virar aviso.
  const mesmaTela = m.tipo === "menu" && m.titulo === tituloAtual && !cenaInterrompida;
  cenaInterrompida = false;
  tituloAtual = m.titulo;
  if (mesmaTela) {
    // O que aconteceu na ação (equipou, comprou...) vira um aviso rápido antes de a tela se redesenhar.
    const avisos = [...textoEl.querySelectorAll(":scope > p:not(.eco):not(.lido)")].map((p) => p.textContent).filter(Boolean).slice(-2);
    if (!replay) avisos.forEach((t) => Telas.toast("", t, "estrela", true));
    fixarRolagem();
    seguir = false;  // a tela se redesenha no lugar: crescer (o contrato aceito desce para "Seus contratos") não puxa a página
    textoEl.innerHTML = ""; promptEl.innerHTML = "";
    cabecalho(m);
    return;
  }
  soltarRolagem();
  porVoltar(null);
  folha.style.minHeight = "";
  promptEl.style.minHeight = ""; promptEl.classList.remove("segurando");
  Telas.novaVisita();  // saiu da tela: a quantidade do mercado volta a 1 na próxima visita
  if (!instantaneo() && textoEl.childElementCount) { folha.classList.add("saindo"); await espera(200); }
  textoEl.innerHTML = "";
  promptEl.innerHTML = "";
  folha.classList.remove("saindo");
  recolherArte(false);  // antes do cabeçalho: vindo de uma tela de menu (sem arte), ela já aparece inteira
  cabecalho(m);
  folha.classList.remove("entrando"); void folha.offsetWidth; folha.classList.add("entrando");
  pagina.scrollTop = 0;
  seguir = true;
  presoNoTopo = m.tipo === "local";
  if (!replay) Som.tocar("pagina");
}

async function revelar(no, texto) {
  if (instantaneo() || !cps()) { no.textContent = texto; rolarFim(); return; }
  await new Promise((fim) => {
    let i = 0, antes = performance.now();
    function passo(agora) {
      if (pular) { no.textContent = texto; rolarFim(); fim(); return; }
      i = Math.min(texto.length, i + Math.max(0.5, ((agora - antes) / 1000) * cps()));
      antes = agora;
      no.textContent = texto.slice(0, Math.floor(i));
      rolarFim();
      if (i >= texto.length) fim(); else requestAnimationFrame(passo);
    }
    requestAnimationFrame(passo);
  });
}

async function texto(m) {
  if (m.mono) {
    let pre = textoEl.lastElementChild;
    if (!pre || !pre.classList.contains("mono")) pre = anexar(el("pre", "mono"));
    pre.textContent += (pre.textContent ? "\n" : "") + m.texto;
    historico("", m.texto);
    return;
  }
  if (m.detalhe) {
    const p = el("p", "detalhe " + (COR_PROSA[(m.cor || "").split("+")[0]] || ""));
    p.innerHTML = Realce.texto(m.texto.replace(/\[[^\]]+\]\s*/g, ""));  // registro da luta: dano, fogo, crítico em cor
    anexar(p);
    historico("", m.texto);
    if (!instantaneo()) await espera(ritmo(160));
    return;
  }
  if (emTela()) {  // numa tela desenhada, frases curtas viram aviso solto
    const tipo = /^(vermelho)/.test(m.cor || "") ? "perda" : /^(verde)/.test(m.cor || "") ? "item" : "info";
    aviso(m.texto, tipo, tipo === "perda" ? "caveira" : tipo === "item" ? "estrela" : "pergaminho");
    historico("", m.texto);
    return;
  }
  const p = el("p");
  const [base, ...mods] = (m.cor || "").split("+");
  if (COR_PROSA[base]) p.classList.add(COR_PROSA[base]);
  if (mods.includes("negrito")) p.classList.add("forte");
  const limpo = m.texto.trim();
  if (/^["“—«]/.test(limpo)) p.classList.add("fala");
  if (capitular && !m.cor && limpo.length > 80 && /^[A-ZÀ-Ý]/.test(limpo)) { p.classList.add("capitular"); capitular = false; }
  anexar(p);
  mostrarDica();
  await revelar(p, m.texto);
  historico("", m.texto);
  if (!instantaneo()) await espera(Math.min(240, 20000 / (cps() || 120)));
}

async function fala(m) {
  historico("h-fala", `${m.nome}: ${m.texto}`);
  if (replay) return;
  const ms = Batalha.balao(m.cid, m.nome, m.texto);
  if (!instantaneo()) await espera(ritmo(ms));
}
async function opiniao(m) {
  const bom = m.delta > 0;
  historico("h-chip", `▸ ${m.nome} ${bom ? "aprova" : "desaprova"}${Math.abs(m.delta) >= 8 ? " muito" : ""}`);
  if (replay) return;
  Batalha.opiniao(m.cid, m.nome, m.delta);
  if (!instantaneo()) await espera(ritmo(220));  // vários reagindo ao mesmo fato: os cartões chegam quase juntos
}

function iconeChip(m) {
  const t = m.texto;
  const porNome = [["Odette", "odete"], ["Morel", "morel"], ["Yara", "yara"]].find(([n]) => t.includes(n));
  if ((m.tipo === "aprova" || m.tipo === "desaprova") && porNome) return porNome[1];
  if (m.tipo === "item") {
    if (/comida|Provis/i.test(t)) return "pernil";
    if (/Tocha/.test(t)) return "tocha";
    if (/Bandagem/.test(t)) return "bandagem";
    if (/Tônico|Unguento/.test(t)) return "pocao_azul";
    if (/Poção/.test(t)) return "pocao";
    if (/[Ff]lecha/.test(t)) return "aljava";
    return "saco";
  }
  return { ouro: "moeda", perda: "bolsa_vazia", xp: "estrela", dano: "gota", cura: "coracao", rep: "escudo",
    ferimento: "gota", nivel: "estrela", info: "pergaminho" }[m.tipo] || "pergaminho";
}

/* Avisos soltos na tela: nas telas desenhadas (mercado, inventário), o que aconteceu aparece
   perto de onde você clicou, e não lá embaixo da página. */
let ultimoClique = { x: 0, y: 0, t: -1e9 }, avisosAtivos = 0;
document.addEventListener("pointerdown", (ev) => {
  ultimoClique = { x: ev.clientX, y: ev.clientY, t: performance.now() };
  dispensarAvisosLongos();
}, true);
/** Aviso longo (o carinho no animal, um acontecimento na fogueira) fica o tempo de ler, mas quem já leu (ou já
 *  conhece de cor) clica em qualquer lugar e ele esvai na hora. O clique que fez o aviso aparecer não conta. */
function dispensarAvisosLongos() {
  document.querySelectorAll(".aviso-flutuante.longo:not(.saindo)").forEach((a) => {
    if (performance.now() - (a._nasceu || 0) < 400) return;
    clearTimeout(a._t);
    a.classList.add("saindo");
    avisosAtivos = Math.max(0, avisosAtivos - 1);
    setTimeout(() => a.remove(), 250);
  });
}
function emTela() { return !!textoEl.querySelector(".tela:not(.achado):not(.saves)") && !(estado && estado.combate); }
const avisosPorChave = {};
/** Aviso flutuante perto do clique. Com `chave`, clicar de novo troca o aviso aberto por um novo (aparece toda vez,
 *  sem empilhar cópias). */
function aviso(texto, tipo, icone, chave) {
  if (replay) return;
  const velho = chave && avisosPorChave[chave];
  if (velho && velho.isConnected) { clearTimeout(velho._t); velho.remove(); avisosAtivos = Math.max(0, avisosAtivos - 1); }
  // Frase longa (o carinho no animal, um acontecimento na fogueira) quebra em linhas e fica o tempo de ler.
  const longo = String(texto).length > 60;
  const dura = longo ? Math.min(9000, Math.max(3500, 1500 + String(texto).length * 55)) : 2400;
  const a = el("div", `aviso-flutuante ${tipo || "info"}${longo ? " longo" : ""}`, (icone ? spr(icone, 1) : "") + `<span>${esc(texto)}</span>`);
  a.style.setProperty("--dura", dura + "ms");
  a._nasceu = performance.now();
  document.body.appendChild(a);
  if (chave) avisosPorChave[chave] = a;
  const n = avisosAtivos++;
  const perto = performance.now() - ultimoClique.t < 5000;
  const x = perto ? ultimoClique.x : innerWidth / 2, y = (perto ? ultimoClique.y - 40 : 110) - n * 32;
  a.style.left = Math.max(8, Math.min(innerWidth - a.offsetWidth - 8, x - a.offsetWidth / 2)) + "px";
  a.style.top = Math.max(54, y) + "px";
  a._t = setTimeout(() => { a.remove(); avisosAtivos = Math.max(0, avisosAtivos - 1); }, dura);
}

async function efeito(m) {
  if (emTela()) {
    aviso(m.texto, m.tipo, iconeChip(m));
    historico("h-chip", "▸ " + m.texto);
    if (replay) return;
    Som.tocar({ ouro: "moeda", perda: "moeda", item: "item", cura: "item", nivel: "nivel" }[m.tipo] || "item");
    if (!instantaneo()) await espera(ritmo(90));
    return;
  }
  let linha = textoEl.lastElementChild;
  if (!linha || !linha.classList.contains("chips") || linha.classList.contains("passado")) linha = anexar(el("div", "chips"));
  linha.appendChild(el("span", `chip ${m.tipo || "info"}`, spr(iconeChip(m), 1) + esc(m.texto)));
  rolarFim();
  historico("h-chip", "▸ " + m.texto);
  if (replay) return;
  if (m.tipo === "ouro") Som.tocar("moeda");
  else if (m.tipo === "nivel") Som.tocar("nivel");
  else if (m.tipo === "item" || m.tipo === "cura") Som.tocar("item");
  else if (m.tipo === "aprova") Som.tocar("aprova");
  else if (m.tipo === "desaprova") Som.tocar("desaprova");
  else if (m.tipo === "ferimento") { Som.tocar("dor"); doer(); Telas.toast("Ferimento", m.texto, "gota"); }
  else if (m.tipo === "perda") Som.tocar("moeda");
  else if (m.tipo === "dano") { Som.tocar("dor"); doer(); }
  await espera(ritmo(m.tipo === "ferimento" ? 700 : 320));
}

async function rolagem(m) {
  const caixa = el("div", "rolagem rolando");
  const sinal = m.mod >= 0 ? "+" : "−";
  caixa.innerHTML = `<div class="d20">${D20}</div><div class="rol-info"><div class="rol-attr">Teste de ${esc(m.atributo)}</div>
    <div class="rol-conta">d20 ${sinal} ${Math.abs(m.mod)} contra dificuldade <b>${m.cd}</b></div></div><div class="rol-res"></div>`;
  anexar(caixa);
  const num = caixa.querySelector("text");
  if (!instantaneo()) {
    Som.tocar("dado");
    const fim = performance.now() + 950;
    while (performance.now() < fim && !pular) { num.textContent = 1 + Math.floor(Math.random() * 20); await espera(60); }
  }
  num.textContent = m.d20;
  caixa.classList.remove("rolando");
  const critico = m.d20 === 20, desastre = m.d20 === 1;
  caixa.classList.add("pousou", m.sucesso ? "ok" : "falha");
  if (critico) caixa.classList.add("critico");
  caixa.querySelector(".rol-conta").innerHTML = `<b>${m.d20}</b> ${sinal} ${Math.abs(m.mod)} = <b>${m.total}</b> contra <b>${m.cd}</b>`;
  caixa.querySelector(".rol-res").textContent = critico ? "Crítico!" : desastre ? "Desastre" : m.sucesso ? "Sucesso" : "Falha";
  historico("h-chip", `▸ ${m.atributo} ${m.total} contra ${m.cd} — ${m.sucesso ? "sucesso" : "falha"} (d20 ${m.d20})`);
  if (!replay) Som.tocar(critico ? "critico" : m.sucesso ? "sucesso" : "falha");
  if (!instantaneo()) await espera(ritmo(650));
}

function faixaCombate(m) {
  anexar(el("div", "faixa-combate", `⚔ ${esc(suavizar(m.titulo))}`));
  if (m.subtitulo) anexar(el("div", "faixa-combate-sub", esc(m.subtitulo)));
  historico("h-cena", "⚔ " + m.titulo);
  if (!replay) Som.tocar("golpe");
}

function turno(m) {
  // A página guarda só o turno anterior (apagado) e o atual; o resto fica no histórico (H).
  if (m.n > 1) {
    textoEl.querySelectorAll(".passado").forEach((x) => x.remove());
    for (const filho of textoEl.children) filho.classList.add("passado");
  }
  anexar(el("div", "divisor-turno", `turno ${m.n}`));
  historico("h-turno", `— turno ${m.n} —`);
}

function bloco(m) {
  const pre = el("pre");
  pre.innerHTML = m.linhas.map((linha) => linha.map(([t, cor]) => cor ? `<span class="${cor.split("+").map((c) => "c-" + c).join(" ")}">${esc(t)}</span>` : esc(t)).join("")).join("\n");
  anexar(pre);
}

function eco(m) {
  // Navegação (Voltar, abrir Talentos ou outra tela da doca, o menu do título) não é um passo da história: não vira
  // eco na página nem entra no histórico. Na luta, a carta que avança e o registro do golpe já contam a escolha.
  if (m.navegacao || atalhoDe(m.texto) || corpo.classList.contains("modo-titulo") || (estado && estado.combate)) return;
  historico("h-eco", "› " + m.texto);
  if (emTela()) return;  // nas telas desenhadas (mercado, inventário), o aviso solto já contou o que aconteceu
  anexar(el("p", "eco", esc(m.texto)));
}

function historico(classe, t) {
  const p = el("p", classe);
  p.textContent = t;
  histLista.appendChild(p);
  while (histLista.childElementCount > 4000) histLista.firstElementChild.remove();
}

function mostrarDica() {
  if (replay || velocidade === "instantaneo" || promptEl.childElementCount) return;
  if (Number(ler("cdf-dica") || 0) > 25) return;
  promptEl.innerHTML = '<div class="dica-pular">qualquer tecla ou clique adianta o texto</div>';
}

let ultimaDor = 0;
function doer() {
  const agora = performance.now();
  if (agora - ultimaDor < 400) return;
  ultimaDor = agora;
  const d = $(".camada.dor");
  d.classList.remove("ativa"); void d.offsetWidth; d.classList.add("ativa");
}
