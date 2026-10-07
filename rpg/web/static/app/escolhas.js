"use strict";

/* ------------------------------------------------------------------ escolhas */
function limparPrompt() {
  promptEl.innerHTML = ""; pergunta = null; Batalha.limparAlvos(); Batalha.vez(null);
  document.querySelectorAll(".rastro-contrato.cacavel").forEach((c) => { c.classList.remove("cacavel"); c.querySelector(".rastro-cacar")?.remove(); });
  document.querySelectorAll(".voltar-seta").forEach((b) => b.remove());
  Telas.fecharMenuItem();
}
function atalhoDe(t) { return SISTEMA.find(([re]) => re.test(t)); }

function mostrarOpcoes(m) {
  // Pedido pendente (ex.: clicou num destino do mapa a partir do menu do local): responde sozinho.
  if (pendente) {
    const p = pendente;
    pendente = null;
    const i = m.opcoes.findIndex((o) => o.meta && o.meta[p.chave] === p.valor);
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
  if (m.pergunta) promptEl.appendChild(el("div", "pergunta-rotulo", esc(m.pergunta)));
  const lista = el("ol", "escolhas");
  const emLuta = !!(estado && estado.combate);
  if (emLuta && m.pergunta === "Sua ação:") { lista.classList.add("acoes-combate"); Batalha.vez("j"); }
  if (emLuta && m.opcoes.some((o) => o.meta && o.meta.alvo)) {
    Batalha.alvos(m.opcoes, (i) => responder(m.id, i));
    promptEl.firstElementChild && promptEl.firstElementChild.classList.add("mira");
  }
  const sistema = m.opcoes.filter((o) => atalhoDe(o.texto)).length >= 4;
  const atalhos = el("div", "atalhos");
  document.querySelectorAll(".voltar-seta").forEach((x) => x.remove());
  const voltar = m.opcoes.length > 1 && !corpo.classList.contains("modo-titulo") ? m.opcoes.findIndex(ehVoltar) : -1;
  if (voltar >= 0) {
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
  if (emLuta && voltar >= 0 && lista.classList.contains("grade-acoes")) {
    // Na luta, "Voltar" fica junto das cartas: ir de Habilidades para Itens sem subir o mouse até o topo.
    const li = el("li");
    const b = el("button", "escolha carta-acao voltar-carta", `<span class="acao-icone">◀</span><span class="acao-nome">Voltar</span><span class="acao-rodape"><kbd>Esc</kbd> ou botão direito</span>`);
    b.type = "button";
    b.addEventListener("click", (ev) => { ev.stopPropagation(); responder(m.id, voltar); });
    li.appendChild(b);
    lista.appendChild(li);
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
      <div class="bonus">${esc(meta.desc)}</div>${bloqueio ? `<div class="pior">${esc(bloqueio)}</div>` : ""}`;
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

// Botão direito em qualquer lugar da página volta um passo (quando a tela atual tem "Voltar").
document.addEventListener("contextmenu", (ev) => {
  if (!pergunta || pergunta.voltar === undefined || ev.target.closest("input, textarea")) return;
  ev.preventDefault();
  responder(pergunta.id, pergunta.voltar);
});

function iconeAcaoCombate(t) {
  if (/^Atacar/.test(t)) return spr({ guerreiro: "espada", arqueiro: "arco", mago: "cajado" }[estado.heroi.classe] || "espada", 2);
  if (/^Habilidades/.test(t)) return spr("estrela", 2);
  if (/^Itens/.test(t)) return spr("pocao", 2);
  if (/^Analisar/.test(t)) return spr("olho", 2);
  if (/^Fugir/.test(t)) return spr("fuga", 2);
  return "";
}

function ehVoltar(o) {
  return (o.meta && o.meta.voltar) || /^(Voltar|Sair do mercado|Cancelar|Fechar)\b/.test(o.texto);
}

function mostrarContinuar(m) {
  promptEl.innerHTML = "";
  const b = el("button", "continuar", "Continuar <span>▸</span>");
  b.type = "button";
  b.addEventListener("click", (ev) => { ev.stopPropagation(); responder(m.id, null); });
  promptEl.appendChild(b);
  pergunta = { id: m.id, tipo: "continuar" };
  rolarFim();
}

function mostrarPergunta(m) {
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
