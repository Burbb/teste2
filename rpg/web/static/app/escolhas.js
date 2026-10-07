"use strict";

/* ------------------------------------------------------------------ escolhas */
function limparPrompt() {
  promptEl.innerHTML = ""; pergunta = null; Batalha.limparAlvos(); Batalha.vez(null); limparRoda();
  document.querySelectorAll(".rastro-contrato.cacavel").forEach((c) => { c.classList.remove("cacavel"); c.querySelector(".rastro-cacar")?.remove(); });
  document.querySelectorAll(".voltar-seta").forEach((b) => b.remove());
  Telas.fecharMenuItem();
}
function atalhoDe(t) { return SISTEMA.find(([re]) => re.test(t)); }

/** O prompt mora no pé da página. (Na luta, as ações vão para a roda em volta da sua carta, dentro da arena.) */
function posicionarPrompt() {
  if (promptEl.parentElement !== folha) folha.appendChild(promptEl);
  if (!corpo.classList.contains("em-combate")) limparRoda();
}

let viaBarra = false;  // a habilidade foi escolhida direto na barra: "Voltar" do alvo volta à barra, não à lista
let habMirando = "";   // o nome do que está sendo mirado, para o lembrete "Bola de Fogo: escolha o alvo"
function mostrarOpcoes(m) {
  posicionarPrompt();
  // Pedido pendente (ex.: clicou num destino do mapa a partir do menu do local): responde sozinho.
  if (pendente) {
    const p = pendente;
    pendente = null;
    const i = p.chave === "_voltar" ? m.opcoes.findIndex(ehVoltar) : m.opcoes.findIndex((o) => o.meta && o.meta[p.chave] === p.valor);
    if (i >= 0) { pergunta = { id: m.id, tipo: "opcoes", opcoes: m.opcoes }; responder(m.id, i); return; }
  }
  promptEl.innerHTML = "";
  pergunta = { id: m.id, tipo: "opcoes", n: m.opcoes.length, opcoes: m.opcoes, numeros: [], letras: {} };
  if (m.opcoes.some((o) => o.meta && o.meta.talento) && Telas.abrirTalentos(m)) {
    const b = el("button", "continuar", "Abrir a árvore de talentos <span>▸</span>");
    b.addEventListener("click", (ev) => { ev.stopPropagation(); Telas.abrirTalentos(m); });
    promptEl.appendChild(b);
    return;
  }
  Telas.fecharTalentos();
  const emLuta = !!(estado && estado.combate);
  if (emLuta && rodaEl() && Batalha.elCarta("j")) {
    // Na luta, as ações aparecem em volta da sua carta; habilidades e itens numa janelinha ao lado; mirando, um lembrete.
    if (m.pergunta === "Sua ação:" && m.opcoes.some((o) => o.meta && o.meta.acao)) { rodaDeAcoes(m); return; }
    if (m.opcoes.some((o) => o.meta && (o.meta.habilidade || o.meta.usar_item || o.meta.trocar !== undefined))) { rodaSubmenu(m); return; }
    if (m.opcoes.some((o) => o.meta && o.meta.alvo)) { rodaMira(m); return; }
  }
  if (m.pergunta) promptEl.appendChild(el("div", "pergunta-rotulo", esc(m.pergunta)));
  const lista = el("ol", "escolhas");
  if (emLuta && m.pergunta === "Sua ação:") { lista.classList.add("acoes-combate"); Batalha.vez("j"); }
  if (emLuta && m.opcoes.some((o) => o.meta && o.meta.alvo)) {
    Batalha.alvos(m.opcoes, (i) => responder(m.id, i));
    promptEl.firstElementChild && promptEl.firstElementChild.classList.add("mira");
  }
  const sistema = m.opcoes.filter((o) => atalhoDe(o.texto)).length >= 4;
  const atalhos = el("div", "atalhos");
  document.querySelectorAll(".voltar-seta").forEach((x) => x.remove());
  const voltar = m.opcoes.length > 1 && !corpo.classList.contains("modo-titulo") ? m.opcoes.findIndex(ehVoltar) : -1;
  if (voltar >= 0 && emLuta) {
    pergunta.voltar = voltar;  // na luta, o Voltar fica dentro da barra (logo abaixo)
    if (viaBarra && m.opcoes.some((o) => o.meta && o.meta.alvo)) pergunta.aoVoltar = () => { pendente = { chave: "_voltar", valor: true }; };
  } else if (voltar >= 0) {
    // "Voltar" vira uma seta fixa no canto da página (e Esc/Backspace), em vez de ficar no fim da lista.
    const b = el("button", "voltar-seta", `<span>◀</span> ${esc(/^Sair do mercado/.test(m.opcoes[voltar].texto) ? "Sair do mercado" : "Voltar")}<kbd>Esc</kbd>`);
    b.type = "button";
    b.addEventListener("click", (ev) => { ev.stopPropagation(); responder(m.id, voltar); });
    folha.prepend(b);
    pergunta.voltar = voltar;
  }
  m.opcoes.forEach((o, i) => {
    if (i === voltar) return;
    if (o.meta && ACOES_OCULTAS.some((k) => o.meta[k] !== undefined)) return;  // feitas pela tela (arrastar, clicar)
    const at = sistema && atalhoDe(o.texto);
    if (at) {
      const pontos = /★\s*(\d+)/.exec(o.texto);
      const carta = /✉/.test(o.texto);
      const qtd = /^Comitiva \((\d+)\)/.exec(o.texto);
      const b = el("button", "atalho" + (pontos || carta ? " destaque" : ""));
      b.type = "button";
      const selo = pontos ? `<b class="selo">★${pontos[1]}</b>` : carta ? '<b class="selo">✉</b>' : "";
      b.innerHTML = `<span class="atalho-icone">${spr(at[3], 2)}${selo}</span><span class="atalho-nome">${esc(at[1])}</span>` +
        (at[2] ? `<kbd>${at[2].toUpperCase()}</kbd>` : "");
      b.title = o.texto + (at[2] ? ` (${at[2].toUpperCase()})` : "");
      if (atalhos.lastElementChild && Number(atalhos.lastElementChild.dataset.grupo) !== at[4]) atalhos.appendChild(el("span", "doca-sep"));
      b.dataset.grupo = at[4];
      b.addEventListener("click", (ev) => { ev.stopPropagation(); responder(m.id, i); });
      atalhos.appendChild(b);
      if (at[2]) pergunta.letras[at[2]] = i;
      if (at[1] === "Talentos") atalhos.appendChild(botaoGrimorio(at[4]));
      return;
    }
    pergunta.numeros.push(i);
    if (emLuta && o.meta && (o.meta.habilidade || o.meta.usar_item || o.meta.trocar !== undefined)) {
      lista.classList.add("grade-acoes");
      const li = el("li");
      li.appendChild(cartaAcao(o, i, m, pergunta.numeros.length - 1));
      lista.appendChild(li);
      return;
    }
    const li = el("li");
    const b = el("button", "escolha");
    b.type = "button";
    b.style.animationDelay = `${replay ? 0 : i * 40}ms`;
    if (/^(Voltar|Sair|Cancelar|Nada|Ignorar|Fechar)/.test(o.texto)) b.classList.add("secundaria");
    const pos = pergunta.numeros.length - 1;
    const tecla = pos < 9 ? String(pos + 1) : pos === 9 ? "0" : "";
    let teste = "", icone = "";
    if (o.teste) {
      const folga = o.teste.mod - (estado ? estado.heroi.dificuldade_extra : 0);
      const nivel = folga >= 6 ? "bom" : folga >= 3 ? "medio" : "ruim";
      const sinal = o.teste.mod >= 0 ? "+" : "−";
      const info = estado && estado.heroi.testes && estado.heroi.testes[o.teste.atributo];
      const partes = info ? info.partes.map(([r, v]) => `<li>${esc(r)}: <b>${v >= 0 ? "+" : "−"}${Math.abs(v)}</b></li>`).join("") : "";
      const chance = Math.max(5, Math.min(95, (21 - (12 + (estado ? estado.heroi.dificuldade_extra : 0) - o.teste.mod)) * 5));
      const dicaTeste = Telas.dica(`<b>Teste de ${esc(o.teste.atributo)} ${sinal}${Math.abs(o.teste.mod)}</b>
        <div class="tipo">d20 + bônus contra a dificuldade</div><ul class="dica-lista">${partes || "<li>sem bônus</li>"}</ul>
        <div class="rodape">Tire 20 e passa sempre; 1 falha sempre. A dificuldade varia com a situação e sobe um pouco a cada dois níveis seus. Numa dificuldade média, sua chance é de cerca de ${chance}%.</div>`);
      teste = `<span class="teste ${nivel}" ${dicaTeste}>${SIGLA[o.teste.atributo] || esc(o.teste.atributo)} ${sinal}${Math.abs(o.teste.mod)}</span>`;
    }
    if (o.meta && o.meta.local !== undefined && estado) {
      const n = estado.mapa.nos.find((x) => x.id === o.meta.local);
      if (n) icone = spr(MapaPx.sprite(n), 1);
    }
    if (o.meta && o.meta.item) icone = spr(Telas.ICONE_ITEM[o.meta.item] || "pocao", 1);
    if (o.meta && o.meta.cacar !== undefined) { icone = spr("arco", 1); b.classList.add("op-contrato"); }
    if (emLuta) icone = iconeAcaoCombate(o.texto) || icone;
    if (o.meta && o.meta.alvo) {
      b.addEventListener("mouseenter", () => Batalha.mirar(o.meta.alvo, true));
      b.addEventListener("mouseleave", () => Batalha.mirar(o.meta.alvo, false));
      b.addEventListener("focus", () => Batalha.mirar(o.meta.alvo, true));
      b.addEventListener("blur", () => Batalha.mirar(o.meta.alvo, false));
    }
    b.innerHTML = `<span class="tecla">${tecla}</span>${icone}<span class="rotulo">${esc(o.texto)}</span>${teste}`;
    b.addEventListener("click", (ev) => { ev.stopPropagation(); responder(m.id, i); });
    li.appendChild(b);
    lista.appendChild(li);
  });
  if (emLuta && voltar >= 0) {
    // Na luta, "Voltar" fica junto das opções, dentro da barra: sem subir o mouse até o topo.
    const li = el("li");
    const grade = lista.classList.contains("grade-acoes");
    const b = el("button", grade ? "escolha carta-acao voltar-carta" : "escolha secundaria voltar-luta",
      grade ? `<span class="acao-icone">◀</span><span class="acao-nome">Voltar</span><span class="acao-rodape"><kbd>Esc</kbd> ou botão direito</span>`
        : `<span class="rotulo">◀ Voltar</span>`);
    b.type = "button";
    b.addEventListener("click", (ev) => { ev.stopPropagation(); voltarPergunta(); });
    li.appendChild(b);
    lista.appendChild(li);
  }
  if (emLuta && m.opcoes.some((o) => o.meta && o.meta.alvo)) {
    // Mirando: o clique é na carta do inimigo (ou as teclas 1, 2...). Na barra fica só o lembrete e o Voltar.
    lista.classList.add("mira-alvo");
    const rot = promptEl.querySelector(".pergunta-rotulo");
    if (rot) rot.innerHTML = `${habMirando ? `<b>${esc(habMirando)}</b>: ` : ""}escolha o alvo <small>clique num inimigo</small>`;
  }
  if (lista.childElementCount) { promptEl.appendChild(lista); Telas.ligarDicas(lista); }
  if (atalhos.childElementCount) promptEl.appendChild(atalhos);
  if (!replay) guardar("cdf-dica", String(Number(ler("cdf-dica") || 0) + 1));
  if (estado) {
    const chave = [...destinosClicaveis()].join(",") + "|" + estado.local.id;
    if (chave !== ultimoMundo) { ultimoMundo = chave; desenharMundo(estado); }
    atualizarMapasDaPagina();
  }
  marcarCacadas();
  rolarFim();
}

/** Contrato de caça com o alvo aqui: o cartão do rastreador vira atalho para "Caçar". */
function opcaoCacar(id) {
  if (!pergunta || pergunta.tipo !== "opcoes") return -1;
  return pergunta.opcoes.findIndex((o) => o.meta && o.meta.cacar === id);
}
function marcarCacadas() {
  document.querySelectorAll(".rastro-contrato").forEach((c) => {
    const pode = opcaoCacar(Number(c.dataset.contrato)) >= 0;
    c.classList.toggle("cacavel", pode);
    const selo = c.querySelector(".rastro-cacar");
    if (pode && !selo) c.querySelector(".rastro-info").insertAdjacentHTML("beforeend", '<span class="rastro-cacar">Seguir os rastros ▸</span>');
    else if (!pode && selo) selo.remove();
  });
}

/* Cartas de ação do combate: habilidades e itens com ícone, custo e dica (como numa barra de ações). */
const HAB_ICONE = {
  golpe_pesado: ["martelo", "fisico"], erguer_escudo: ["escudo", "protecao"], investida: ["espada", "fisico"],
  grito_guerra: ["manopla", "forca"], golpe_sagrado: ["orbe_luz", "sagrado"], prece: ["coracao", "sagrado"],
  julgamento: ["raio", "sagrado"], sede_sangue: ["gota", "sangue"], redemoinho: ["machado", "fisico"],
  furia_cega: ["caveira", "sangue"], tiro_certeiro: ["flecha", "fisico"], marcar_presa: ["olho", "forca"],
  chuva_flechas: ["aljava", "fisico"], passo_agil: ["fuga", "protecao"], tiro_duplo: ["arco", "fisico"],
  comando_fera: ["fera", "natureza"], furia_natureza: ["folha", "natureza"], desaparecer: ["capuz", "sombra"],
  flecha_envenenada: ["gota_verde", "veneno"], execucao: ["caveira", "sangue"], bola_fogo: ["chama", "fogo"],
  meditar: ["lua", "arcano"], lanca_gelo: ["gelo", "gelo"], barreira: ["escudo_azul", "arcano"],
  inferno: ["fogueira", "fogo"], combustao: ["estrela", "fogo"], fenix: ["voador", "fogo"],
  drenar_vida: ["gota_roxa", "sombra"], erguer_servo: ["osso", "sombra"], maldicao: ["orbe_sombra", "sombra"],
};
const ALVO_TXT = { inimigo: "um inimigo", todos: "todos os inimigos", proprio: "você" };
function cartaAcao(o, i, m, pos) {
  const meta = o.meta;
  const b = el("button", "escolha carta-acao");
  b.type = "button";
  const tecla = pos < 9 ? String(pos + 1) : pos === 9 ? "0" : "";
  let icone, nome, rodape = "", dicaHtml, bloqueio = null;
  if (meta.habilidade) {
    const [ic, fam] = HAB_ICONE[meta.habilidade] || ["estrela", "arcano"];
    b.classList.add("el-" + fam);
    icone = spr(ic, 2);
    nome = meta.nome;
    const custo = (meta.custo ? `${spr(RECURSO_ICONE[meta.recurso] || "estrela", 1)}<b>${meta.custo}</b>` : `<b class="gratis">grátis</b>`) +
      (meta.flechas ? ` ${spr("flecha", 1)}<b>${meta.flechas}</b>` : "");
    rodape = `<span class="acao-custo">${custo}</span><span class="acao-alvo">${ALVO_TXT[meta.alvo_tipo] || ""}</span>`;
    if (!meta.pode) bloqueio = meta.motivo || "Indisponível";
    dicaHtml = `<b>${esc(meta.nome)}</b><div class="tipo">${meta.custo ? `${meta.custo} de ${esc(meta.recurso)}` : "Sem custo"}${meta.flechas ? ` · ${meta.flechas} flecha${meta.flechas > 1 ? "s" : ""}` : ""} · alvo: ${ALVO_TXT[meta.alvo_tipo] || "—"}</div>
      <div class="bonus">${esc(meta.desc)}</div>${danoGrimorio(meta.habilidade)}${bloqueio ? `<div class="pior">${esc(bloqueio)}</div>` : ""}`;
  } else if (meta.usar_item) {
    b.classList.add("el-cura");
    icone = spr(Telas.ICONE_ITEM[meta.usar_item] || "pocao", 2);
    nome = meta.nome;
    rodape = `<span class="acao-custo"><b>×${meta.qtd}</b></span><span class="acao-alvo">gasta o turno</span>`;
    if (meta.motivo) bloqueio = meta.motivo;
    dicaHtml = `<b>${esc(meta.nome)}</b><div class="tipo">Você tem ${meta.qtd}</div><div class="bonus">${esc(meta.desc)}</div>${bloqueio ? `<div class="pior">${esc(bloqueio)}</div>` : ""}`;
  } else {
    const it = meta.equip;
    b.classList.add("el-fisico", "troca");
    icone = spr(Telas.iconeItem(it), 2);
    nome = "Trocar: " + it.nome;
    rodape = `<span class="acao-alvo">gasta o turno</span>`;
  }
  b.innerHTML = `<span class="tecla">${tecla}</span><span class="acao-icone">${icone}</span><span class="acao-nome">${esc(nome)}</span><span class="acao-rodape">${rodape}</span>`;
  b.dataset.dica = Telas.guardarDica(meta.trocar !== undefined
    ? Telas.htmlItem(meta.equip, "Trocar de arma no meio da luta gasta o seu turno.") : dicaHtml);
  if (bloqueio) b.classList.add("bloqueada");
  b.addEventListener("click", (ev) => {
    ev.stopPropagation();
    // Animação à parte (WAAPI): trocar a classe de animação apagava a de entrada e o botão sumia.
    if (bloqueio) { App.som("falha"); b.animate([{ translate: "0" }, { translate: "-4px 0" }, { translate: "4px 0" }, { translate: "0" }], { duration: 260, easing: "steps(6)" }); return; }
    responder(m.id, i);
  });
  return b;
}

/** Responde "Voltar" na pergunta atual (botão, Esc ou botão direito), com o desvio da barra de luta. */
function voltarPergunta() {
  if (!pergunta || pergunta.voltar === undefined) return;
  if (pergunta.aoVoltar) pergunta.aoVoltar();
  responder(pergunta.id, pergunta.voltar);
}

// Botão direito em qualquer lugar da página volta um passo (quando a tela atual tem "Voltar").
document.addEventListener("contextmenu", (ev) => {
  if (ev.target.closest("input, textarea")) return;
  if (fecharJanela()) { ev.preventDefault(); return; }
  if (!pergunta || pergunta.voltar === undefined) return;
  ev.preventDefault();
  voltarPergunta();
});

/* ------------------------------------------------------------------ roda de ações da luta */
/* Na sua vez, sua carta vem para a frente e as ações (Atacar, Habilidades, Itens, Fugir) surgem em arco ao lado dela.
   Habilidades e Itens abrem uma janelinha com ícone, nome e custo (passe o mouse para ver o que fazem). */
function rodaEl() { return document.getElementById("roda"); }
let janelaAberta = null;  // { fechar } da janelinha de habilidades/itens
function limparRoda() {
  const r = rodaEl();
  if (r && r.childElementCount) { Telas.esconderDica(); r.replaceChildren(); }
  janelaAberta = null;
  Batalha.foco(null);
}
/** Fecha a janelinha (Esc, botão direito, ×). Devolve true se havia uma aberta. */
function fecharJanela() {
  if (!janelaAberta) return false;
  const j = janelaAberta;
  janelaAberta = null;
  j.fechar();
  return true;
}
function tremerNao(b, motivo) {
  App.som("falha");
  b.animate([{ translate: "0" }, { translate: "-4px 0" }, { translate: "4px 0" }, { translate: "0" }], { duration: 240, easing: "ease-in-out" });
  aviso(motivo, "info", "pergaminho");
}
/** Geometria da carta do herói dentro da arena (sem contar o zoom do foco). */
function geometriaHeroi() {
  const c = Batalha.elCarta("j"), arena = rodaEl().parentElement;
  return { x: c.offsetLeft, y: c.offsetTop, w: c.offsetWidth, h: c.offsetHeight, W: arena.clientWidth, H: arena.clientHeight };
}
function prepararRoda() {
  limparRoda();
  Batalha.vez("j");
  Batalha.foco("j");
  promptEl.appendChild(el("span", "marca-roda"));  // a próxima mensagem limpa o prompt, e com ele a roda
  pergunta.teclasNum = [];
}

function rodaDeAcoes(m) {
  prepararRoda();
  viaBarra = false;
  habMirando = "";
  const roda = rodaEl();
  const acaoIdx = (a) => m.opcoes.findIndex((o) => o.meta && o.meta.acao === a);
  const heroi = estado.heroi;
  const atk = m.opcoes[acaoIdx("atacar")];
  const habs = m.opcoes[acaoIdx("habilidades")].meta.habilidades || [];
  const basico = heroi.grimorio && heroi.grimorio.basico.linhas.find((l) => l.tipo === "dano");
  const botoes = [];
  const botao = (id, icone, rotulo, dica, aoClicar) => {
    const b = el("button", "roda-botao");
    b.type = "button";
    b.dataset.slot = id;
    const n = pergunta.teclasNum.length + 1;
    b.innerHTML = `<span class="rb-icone">${icone}<span class="tecla">${n}</span></span><span class="rb-nome">${esc(rotulo)}</span>`;
    if (dica) b.dataset.dica = Telas.guardarDica(dica);
    b.addEventListener("click", (ev) => { ev.stopPropagation(); aoClicar(b); });
    pergunta.teclasNum.push(() => aoClicar(b));
    roda.appendChild(b);
    botoes.push(b);
    return b;
  };
  const arma = { guerreiro: "espada", arqueiro: "arco", mago: "cajado" }[heroi.classe] || "espada";
  botao("atacar", spr(arma, 2), "Atacar", `<b>${esc(atk.meta.nome)}</b><div class="tipo">grátis · devolve um pouco de ${esc(heroi.recurso.toLowerCase())}</div>` +
    (basico ? `<div class="melhor">Dano: ${basico.min}–${basico.max} (crítico ${basico.critico})</div>` : ""),
    () => { App.som("escolha"); habMirando = atk.meta.nome; responder(m.id, acaoIdx("atacar")); });
  if (habs.length) {
    botao("habilidades", spr("grimorio", 2), "Habilidades", "", (b) => {
      if (janelaAberta && b.classList.contains("ativo")) { fecharJanela(); return; }
      App.som("pagina");
      abrirJanela(b, "Habilidades", habs.map((h) => linhaHabilidade(h, () => {
        App.som("escolha");
        viaBarra = true;
        habMirando = h.nome;
        pendente = { chave: "habilidade", valor: h.habilidade };
        responder(m.id, acaoIdx("habilidades"));
      })));
    });
  }
  botao("itens", spr("pocao", 2), "Itens", "<b>Itens</b><div>Poções, tônicos, bandagens e troca de arma. Usar gasta o turno.</div>",
    () => { App.som("pagina"); responder(m.id, acaoIdx("itens")); });
  if (acaoIdx("analisar") >= 0) botao("analisar", spr("olho", 2), "Analisar", "", () => responder(m.id, acaoIdx("analisar")));
  if (acaoIdx("fugir") >= 0) {
    botao("fugir", spr("fuga", 2), "Fugir", "<b>Fugir</b><div>A chance depende da sua Agilidade contra a dos inimigos. Falhar custa o turno.</div>",
      () => { App.som("escolha"); responder(m.id, acaoIdx("fugir")); });
  }
  arcoDeBotoes(botoes);
  Telas.ligarDicas(roda);
}

/** Os botões em arco, colados à direita da carta (que cresceu 12% com o foco). */
function arcoDeBotoes(botoes) {
  const g = geometriaHeroi();
  const cx = g.x + g.w / 2, cy = g.y + g.h / 2;
  const direita = cx + (g.w / 2) * 1.12;
  const passo = 50, total = (botoes.length - 1) * passo;
  const topo = Math.max(28, Math.min(g.H - 28 - total, cy - total / 2));
  botoes.forEach((b, i) => {
    const y = topo + i * passo;
    const t = total ? (y - (topo + total / 2)) / (total / 2) : 0;
    const x = direita + 12 + 22 * (1 - t * t);  // um arco ")": os do meio mais afastados
    b.style.left = x + "px";
    b.style.top = y + "px";
    b.style.setProperty("--dx", (cx - x) + "px");
    b.style.setProperty("--dy", (cy - y) + "px");
    b.style.animationDelay = i * 35 + "ms";
  });
}

function linhaHabilidade(h, aoClicar) {
  const [ic, fam] = HAB_ICONE[h.habilidade] || ["estrela", "arcano"];
  const custo = h.custo ? `${spr(RECURSO_ICONE[h.recurso] || "estrela", 1)}${h.custo}` : '<span class="gratis">grátis</span>';
  return { icone: spr(ic, 2), fam, nome: h.nome, info: custo + (h.flechas ? ` ${spr("flecha", 1)}${h.flechas}` : ""), dica: dicaHabilidade(h),
    bloqueio: h.pode ? null : (h.motivo || "Indisponível"), hab: h.habilidade, aoClicar };
}
function dicaHabilidade(h) {
  return `<b>${esc(h.nome)}</b><div class="tipo">${h.custo ? `${h.custo} de ${esc(h.recurso)}` : "Sem custo"}${h.flechas ? ` · ${h.flechas} flecha${h.flechas > 1 ? "s" : ""}` : ""} · alvo: ${ALVO_TXT[h.alvo_tipo] || "—"}</div>
    <div class="bonus">${esc(h.desc)}</div>${danoGrimorio(h.habilidade)}${h.pode ? "" : `<div class="pior">${esc(h.motivo || "Indisponível")}</div>`}`;
}

/** A janelinha ao lado dos botões: uma linha por habilidade ou item (ícone, nome, custo). Teclas 1–9 escolhem. */
function abrirJanela(ancora, titulo, linhas, aoFechar) {
  fecharJanela();
  const roda = rodaEl();
  const teclasAntes = pergunta.teclasNum;
  pergunta.teclasNum = [];
  const j = el("div", "roda-janela");
  j.innerHTML = `<div class="rj-titulo"><span>${esc(titulo)}</span><button type="button" class="rj-fechar" title="Fechar (Esc)">×</button></div>`;
  const lista = el("ul", "rj-lista");
  linhas.forEach((l, i) => {
    const li = el("li");
    const b = el("button", `rj-linha el-${l.fam || "fisico"}${l.bloqueio ? " bloqueada" : ""}`);
    b.type = "button";
    if (l.hab) b.dataset.hab = l.hab;
    if (l.slot) b.dataset.slot = l.slot;
    b.innerHTML = `<span class="rj-icone">${l.icone}</span><span class="rj-nome">${esc(l.nome)}</span><span class="rj-info">${l.info || ""}</span>${i < 9 ? `<span class="tecla">${i + 1}</span>` : ""}`;
    if (l.dica) b.dataset.dica = Telas.guardarDica(l.dica);
    const usar = () => (l.bloqueio ? tremerNao(b, l.bloqueio) : l.aoClicar());
    b.addEventListener("click", (ev) => { ev.stopPropagation(); usar(); });
    pergunta.teclasNum.push(usar);
    li.appendChild(b);
    lista.appendChild(li);
  });
  j.appendChild(lista);
  roda.appendChild(j);
  ancora.classList.add("ativo");
  // Ao lado dos botões, na altura da sua carta, sem sair da tela.
  const g = geometriaHeroi();
  const x = ancora.offsetLeft + ancora.offsetWidth + 10;
  j.style.left = Math.min(x, g.W - j.offsetWidth - 6) + "px";
  const topoTela = j.offsetParent.getBoundingClientRect().top;
  const teto = (document.getElementById("topo")?.getBoundingClientRect().bottom || 0) + 6 - topoTela;  // nunca sob o cabeçalho
  const y = Math.max(teto, Math.min(g.y + g.h / 2 - j.offsetHeight / 2, innerHeight - topoTela - j.offsetHeight - 8));
  j.style.top = y + "px";
  const fechar = () => {
    Telas.esconderDica();
    j.remove();
    ancora.classList.remove("ativo");
    if (pergunta) pergunta.teclasNum = teclasAntes;
    if (aoFechar) aoFechar();
  };
  j.querySelector(".rj-fechar").addEventListener("click", (ev) => { ev.stopPropagation(); fecharJanela(); });
  janelaAberta = { fechar };
  Telas.ligarDicas(j);
}

/** Itens (ou habilidades pela tecla): a mesma janelinha, aberta pelo motor; fechar é "Voltar". */
function rodaSubmenu(m) {
  prepararRoda();
  const voltar = m.opcoes.findIndex(ehVoltar);
  if (voltar >= 0) pergunta.voltar = voltar;
  const linhas = [];
  m.opcoes.forEach((o, i) => {
    const meta = o.meta;
    if (!meta || i === voltar) return;
    if (meta.habilidade) {
      linhas.push(linhaHabilidade(meta, () => { App.som("escolha"); habMirando = meta.nome; responder(m.id, i); }));
    } else if (meta.usar_item) {
      linhas.push({ icone: spr(Telas.ICONE_ITEM[meta.usar_item] || "pocao", 2), fam: "cura", nome: meta.nome, info: `×${meta.qtd}`, slot: "item",
        dica: `<b>${esc(meta.nome)}</b><div class="tipo">Você tem ${meta.qtd} · gasta o turno</div><div class="bonus">${esc(meta.desc)}</div>`,
        bloqueio: meta.motivo, aoClicar: () => { App.som("item"); responder(m.id, i); } });
    } else if (meta.trocar !== undefined) {
      linhas.push({ icone: spr(Telas.iconeItem(meta.equip), 2), fam: "fisico", nome: "Trocar: " + meta.equip.nome, info: "turno",
        dica: Telas.htmlItem(meta.equip, "Trocar de arma no meio da luta gasta o seu turno."), aoClicar: () => { App.som("equipar"); responder(m.id, i); } });
    }
  });
  // Uma âncora invisível onde ficaria o botão de Itens, para a janelinha abrir no mesmo lugar.
  const g = geometriaHeroi();
  const ancora = el("span", "roda-ancora");
  ancora.style.left = g.x + g.w * 1.06 + 20 + "px";
  ancora.style.top = g.y + g.h / 2 + "px";
  rodaEl().appendChild(ancora);
  abrirJanela(ancora, m.pergunta && /item/i.test(m.pergunta) ? "Itens" : "Habilidades", linhas, () => { if (voltar >= 0) voltarPergunta(); });
}

/** Mirando: os inimigos acendem; no alto da arena, o lembrete e o Voltar. As teclas 1, 2... escolhem o alvo. */
function rodaMira(m) {
  prepararRoda();
  Batalha.alvos(m.opcoes, (i) => responder(m.id, i));
  m.opcoes.forEach((o, i) => { if (o.meta && o.meta.alvo) pergunta.teclasNum.push(() => responder(m.id, i)); });
  const voltar = m.opcoes.findIndex(ehVoltar);
  const chip = el("div", "roda-mira", `<span>${habMirando ? `<b>${esc(habMirando)}</b> · ` : ""}escolha o alvo</span>`);
  if (voltar >= 0) {
    pergunta.voltar = voltar;
    if (viaBarra) pergunta.aoVoltar = () => { pendente = { chave: "_voltar", valor: true }; };
    const v = el("button", "mira-voltar", "◀ Voltar");
    v.type = "button";
    v.addEventListener("click", (ev) => { ev.stopPropagation(); voltarPergunta(); });
    chip.appendChild(v);
  }
  rodaEl().appendChild(chip);
}

function iconeAcaoCombate(t) {
  if (/^Atacar/.test(t)) return spr({ guerreiro: "espada", arqueiro: "arco", mago: "cajado" }[estado.heroi.classe] || "espada", 2);
  if (/^Habilidades/.test(t)) return spr("grimorio", 2);
  if (/^Itens/.test(t)) return spr("pocao", 2);
  if (/^Analisar/.test(t)) return spr("olho", 2);
  if (/^Fugir/.test(t)) return spr("fuga", 2);
  return "";
}

/** A linha de dano do Grimório na dica da carta de habilidade: "Dano 16–22 (crítico 31)". */
function danoGrimorio(id) {
  const g = estado && estado.heroi.grimorio;
  const x = g && g.habilidades.find((h) => h.id === id);
  const d = x && x.linhas.find((l) => l.tipo === "dano");
  return d ? `<div class="melhor">${esc(d.rotulo === "Dano" ? "Dano" : d.rotulo)}: ${d.min}–${d.max} (crítico ${d.critico})</div><div class="rodape">Detalhes no Grimório (P).</div>` : "";
}

/** O Grimório não é um menu do jogo: abre por cima de qualquer tela, como o mapa. */
function botaoGrimorio(grupo) {
  const b = el("button", "atalho");
  b.type = "button";
  b.dataset.grupo = grupo;
  b.title = "Grimório: suas habilidades e o dano de cada uma (P)";
  b.innerHTML = `<span class="atalho-icone">${spr("grimorio", 2)}</span><span class="atalho-nome">Grimório</span><kbd>P</kbd>`;
  b.addEventListener("click", (ev) => { ev.stopPropagation(); Telas.abrirGrimorio(); });
  return b;
}

function ehVoltar(o) {
  return (o.meta && o.meta.voltar) || /^(Voltar|Sair do mercado|Cancelar|Fechar)\b/.test(o.texto);
}

function mostrarContinuar(m) {
  posicionarPrompt();
  promptEl.innerHTML = "";
  const b = el("button", "continuar", "Continuar <span>▸</span>");
  b.type = "button";
  b.addEventListener("click", (ev) => { ev.stopPropagation(); responder(m.id, null); });
  promptEl.appendChild(b);
  pergunta = { id: m.id, tipo: "continuar" };
  rolarFim();
}

function mostrarPergunta(m) {
  posicionarPrompt();
  promptEl.innerHTML = "";
  promptEl.appendChild(el("div", "pergunta-rotulo", esc(m.pergunta)));
  const linha = el("div", "entrada-texto");
  const input = el("input");
  input.placeholder = m.padrao || "";
  input.maxLength = 40;
  input.addEventListener("keydown", (ev) => { if (ev.key === "Enter") { ev.preventDefault(); responder(m.id, input.value || m.padrao || ""); } });
  const ok = el("button", "continuar", "Confirmar <span>▸</span>");
  ok.addEventListener("click", (ev) => { ev.stopPropagation(); responder(m.id, input.value || m.padrao || ""); });
  linha.append(input, ok);
  if (m.voltar) {
    document.querySelectorAll(".voltar-seta").forEach((x) => x.remove());
    const volta = el("button", "voltar-seta", "<span>◀</span> Voltar<kbd>Esc</kbd>");
    volta.type = "button";
    volta.addEventListener("click", (ev) => { ev.stopPropagation(); responder(m.id, { voltar: true }); });
    input.addEventListener("keydown", (ev) => { if (ev.key === "Escape") { ev.preventDefault(); responder(m.id, { voltar: true }); } });
    folha.prepend(volta);
  }
  promptEl.appendChild(linha);
  pergunta = { id: m.id, tipo: "pergunta" };
  setTimeout(() => input.focus(), 50);
  rolarFim();
}

/* ------------------------------------------------------------------ viagem pelo mapa */
function destinosClicaveis() {
  if (!pergunta || pergunta.tipo !== "opcoes" || !estado) return new Set();
  const diretos = pergunta.opcoes.filter((o) => o.meta && o.meta.local !== undefined).map((o) => o.meta.local);
  if (diretos.length) return new Set(diretos);
  if (pergunta.opcoes.some((o) => o.texto === "Viajar")) return new Set(estado.mapa.nos.filter((n) => n.distancia).map((n) => n.id));
  return new Set();
}
function viajarPara(id) { pedir("Viajar", "local", id); }

function mapaNaPagina() {
  if (!estado) return;
  const caixa = el("div", "mapa-pagina");
  caixa.dataset.mapa = "1";
  anexar(caixa);
  atualizarMapasDaPagina();
}
function atualizarMapasDaPagina() {
  if (!estado) return;
  textoEl.querySelectorAll("[data-mapa]").forEach((caixa) => {
    const clic = destinosClicaveis();
    caixa.innerHTML = "";
    caixa.appendChild(MapaPx.criar(estado.mapa, { grande: true, clicaveis: clic, aoClicar: viajarPara, nivelHeroi: estado.heroi.nivel, marcas: marcasContrato(estado) }));
    if (clic.size) caixa.appendChild(el("div", "mapa-dica", "Clique num destino no mapa para viajar"));
  });
}
