/* PROTÓTIPO do combate e dos atributos, quarta versão (26/10/2026; nada no jogo; a terceira com o fogo em área e sem a
   Marca): a tela só desenha o que o servidor manda (motor4/regras.py decide tudo: custos, alvos, motivos, previsões por tipo e alvo, chances de resistir).
   Duas telas: Preparar (fora da luta: a construção, o equipamento, o kit e o que eles fazem) e a luta. */
"use strict";
(() => {
  const $ = (s) => document.querySelector(s);
  const esc = (t) => String(t ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const pct = (x) => `${Math.round(x * 100)}%`;
  const guardado = (k, v) => { try { if (v === undefined) return JSON.parse(localStorage.getItem("combate-atr4:" + k)); localStorage.setItem("combate-atr4:" + k, JSON.stringify(v)); } catch (e) { return null; } return null; };
  const ICONE_ESTADO = { atordoado: "atordoado", sangramento: "sangramento", marca: "marcado", defesa: "guarda", escudo: "barreira",
                         comando: "fortalecido", desafio: "provocando", atrai: "provocando", juramento: "firme", queimadura: "queimadura" };
  const TIER = { 1: "Tier 1", 2: "Tier 2", 3: "Tier 3", ultimate: "Ultimate" };
  const PECA = { arma: "Arma", foco: "Foco", manto: "Manto" };
  const ALVOS = ["bruto", "xama", "cao"];

  let cat = null, E = null, anterior = null, vistos = 0, ocupado = false, sel = null, aviso = "", fichaDe = "heroi";
  let cfg = null, F = null;

  async function api(caminho, corpo) {
    const r = await fetch(caminho, corpo ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(corpo) } : undefined);
    return r.json();
  }
  const retrato = (o, lado) => (o.lado === "aliado" ? Icones.cabeca(o.retrato, lado) : Icones.criatura(o.retrato, lado))
    || `<span class="sem-retrato" style="--s:${lado}">${esc(o.nome[0])}</span>`;
  const hab = (id) => cat.habilidades.find((h) => h.id === id);
  const nomeHab = (id) => (hab(id) || cat.basicos.find((h) => h.id === id) || { nome: id }).nome;
  const somaAtr = () => cat.atributos.reduce((s, a) => s + cfg.atributos[a.id], 0);
  const presetIgual = () => { const b = cat.builds.find((x) => x.id === cfg.build); return b && cat.atributos.every((a) => b.atributos[a.id] === cfg.atributos[a.id]); };
  const corpoBuild = () => ({ build: presetIgual() ? cfg.build : null, atributos: cfg.atributos, kit: cfg.kit, equip: cfg.equip, presenca: cfg.presenca });
  const nomeBuild = () => (presetIgual() ? cat.builds.find((x) => x.id === cfg.build).nome : "Livre");
  const nomeBuildId = (id) => (id === "livre" ? "Livre" : cat.builds.find((b) => b.id === id).nome);
  const infoTxt = (i) => (i ? `${i.tipo} · potência: ${i.escala} · defesa: ${i.defesa}` : "");
  const prev = (p) => `<span title="${esc(p.conta)}">${p.normal}${p.chance ? ` <small>crít. ${p.critico} (${pct(p.chance)})</small>` : ""}</span>`;

  // ---------------------------------------------------------------- preparar
  function usarBuild(id) {
    const b = cat.builds.find((x) => x.id === id);
    cfg = { ...cfg, build: id, atributos: { ...b.atributos }, kit: [...b.kit] };
    salvarCfg();
  }
  function salvarCfg() { guardado("cfg", cfg); atualizarFicha(); }
  async function atualizarFicha() { F = await api("/api4/ficha", corpoBuild()); desenharPrep(); }
  function abrirPrep(sim = true) {
    document.body.classList.toggle("preparando", sim);
    $("#prep").hidden = !sim;
    if (sim) { desenharPrep(); const b = $("#prep .lutar"); if (b) b.focus(); }
  }
  function motivoKit(h) {
    if (cfg.kit.includes(h.id)) return null;
    const pts = cfg.kit.reduce((s, k) => s + hab(k).pontos, 0);
    if (h.tier === "ultimate" && cfg.kit.some((k) => hab(k).tier === "ultimate")) return "Já há uma ultimate no kit.";
    if (cfg.kit.length >= cat.kit_espacos) return `Os ${cat.kit_espacos} espaços estão ocupados.`;
    if (pts + h.pontos > cat.kit_pontos) return `Faltam ${pts + h.pontos - cat.kit_pontos} ponto(s) de kit.`;
    return null;
  }

  function tabelaDano() {
    const cab = ALVOS.map((t) => { const a = F.alvos[t]; const r = Object.entries(a.res).map(([k, v]) => `${k} ${pct(v)}`).join(", "); return `<th class="num" title="proteção ${a.protecao}${r ? "; " + r : ""}${a.ponto_fraco ? "; ponto fraco" : ""}">${esc(a.nome)}<small>${r || `proteção ${a.protecao}`}</small></th>`; }).join("");
    const linhas = F.dano.map((d) => `<tr><td title="${esc(infoTxt(d.info))}">${esc(d.nome)}${d.ultimate ? " <small>ult.</small>" : ""}<small class="tipo-dano t-${d.info.tipo_id}">${esc(d.info.tipo)}</small></td><td>${d.custo || "—"}</td>` +
      ALVOS.map((t) => `<td class="num">${prev(d.alvos[t])}</td>`).join("") + "</tr>").join("");
    return `<table class="dano"><thead><tr><th>Golpe</th><th>Custo</th>${cab}</tr></thead><tbody>${linhas}</tbody></table>`;
  }
  function tabelaCombo() {
    if (!F.combo) return "";
    const L = F.combo.bruto;
    return `<h4>A combinação de Queimadura <small>(alvo parado; a Queimadura pinga no turno do alvo, entre os seus)</small></h4>` +
      `<table class="eq"><thead><tr><th>Sequência</th><th>Turnos</th><th>Custo</th><th class="num">Bruto</th><th class="num">Cão (fogo 60%)</th></tr></thead><tbody>` +
      L.map((l, i) => `<tr><td>${esc(l.rotulo)}</td><td>${l.turnos}</td><td>${l.custo}</td><td class="num">${l.dano}</td><td class="num">${F.combo.cao[i].dano}</td></tr>`).join("") +
      `</tbody></table><p class="nota">Risco: se o alvo cair antes da Combustão, o que foi preparado se perde.</p>`;
  }
  const GRUPO_FOGO = { um: "Contra um alvo (Soldado parado)", grupo: "Contra um grupo (três lobos parados)",
                       resistente: "Contra resistência (dois Cães de Brasa, fogo 60%)" };
  function tabelaFogo() {
    if (!F.fogo || !F.fogo.length) return "";
    let g = "";
    const linhas = F.fogo.map((l) => {
      const cab = l.grupo !== g ? `<tr><td class="grupo" colspan="7">${esc(GRUPO_FOGO[l.grupo])}</td></tr>` : "";
      g = l.grupo;
      return cab + `<tr><td>${esc(l.rotulo)}</td><td>${l.acoes}</td><td>${l.custo} de ${l.recurso_antes}</td><td class="num">${l.direto}</td><td class="num">${l.periodico}</td><td class="num"><b>${l.total}</b></td><td class="num">${(l.total / l.custo).toFixed(1).replace(".", ",")}</td></tr>`;
    }).join("");
    return `<h4>O fogo jogado de verdade <small>(lutas com alvos parados, a mesma build; as Queimaduras pingam até apagar ou ser consumidas)</small></h4>` +
      `<table class="eq fogo"><thead><tr><th>Sequência de Jean</th><th>Ações</th><th>Custo / reserva</th><th class="num">Direto</th><th class="num">Periódico</th><th class="num">Total</th><th class="num">Por Vigor</th></tr></thead><tbody>${linhas}</tbody></table>`;
  }
  function tabelaEquip(p) {
    const L = F.equipamento[p].linhas;
    if (p === "manto") {
      return `<table class="eq"><thead><tr><th>Manto</th>${L[0].recebido.map((r) => `<th class="num">${esc(r.nome)}</th>`).join("")}</tr></thead><tbody>` +
        L.map((l) => `<tr class="${cfg.equip.manto === l.id ? "atual" : ""}"><td>${esc(l.nome)}</td>${l.recebido.map((r) => `<td class="num">${r.dano}</td>`).join("")}</tr>`).join("") + "</tbody></table>";
    }
    if (!L[0].dano.length) return `<p class="nota">${p === "arma" ? "Nenhum golpe com a arma no kit." : "Nenhum golpe com o foco no kit: o foco não muda nada nesta construção."}</p>`;
    return `<table class="eq"><thead><tr><th>${PECA[p]}</th>${L[0].dano.map((d) => `<th class="num">${esc(d.nome)}</th>`).join("")}</tr></thead><tbody>` +
      L.map((l) => `<tr class="${cfg.equip[p] === l.id ? "atual" : ""}"><td>${esc(l.nome)} (${l.valor})</td>${l.dano.map((d) => `<td class="num">${d.normal}</td>`).join("")}</tr>`).join("") + "</tbody></table>";
  }

  function desenharPrep() {
    if (!cfg || $("#prep").hidden) return;
    const soma = somaAtr(), pts = cfg.kit.reduce((s, k) => s + hab(k).pontos, 0);
    const b = presetIgual() ? cat.builds.find((x) => x.id === cfg.build) : null;
    const builds = cat.builds.map((x) => `<button class="build${presetIgual() && x.id === cfg.build ? " atual" : ""}" data-build="${x.id}"><b>${esc(x.nome)}</b><span>${esc(x.frase)}</span></button>`).join("")
      + `<button class="build${b ? "" : " atual"}" data-livre="1"><b>Livre</b><span>Distribua os ${cat.orcamento} pontos você mesmo.</span></button>`;
    const atr = cat.atributos.map((a) => {
      const v = cfg.atributos[a.id];
      return `<li><span class="nome">${esc(a.nome)}<small>${esc(a.funcao)}</small></span><button data-atr="${a.id}" data-d="-1" aria-label="menos ${esc(a.nome)}" ${v <= cat.min ? "disabled" : ""}>−</button>` +
        `<b>${v}</b><button data-atr="${a.id}" data-d="1" aria-label="mais ${esc(a.nome)}" ${v >= cat.max || soma >= cat.orcamento ? "disabled" : ""}>+</button><i class="medida" style="--v:${v * 10}%"></i></li>`;
    }).join("");
    const pres = `<li class="presenca"><span class="nome">Presença<small>só fora da luta · fora do orçamento</small></span><button data-pres="-1" aria-label="menos Presença" ${cfg.presenca <= cat.min ? "disabled" : ""}>−</button>` +
      `<b>${cfg.presenca}</b><button data-pres="1" aria-label="mais Presença" ${cfg.presenca >= cat.max ? "disabled" : ""}>+</button><i class="medida" style="--v:${cfg.presenca * 10}%"></i></li>`;
    const equip = Object.keys(PECA).map((p) => `<label>${PECA[p]} <select data-equip="${p}">${cat.equipamento[p].map((o) => {
      const val = p === "manto" ? Object.entries(o.res).map(([k, v]) => `${k} ${pct(v)}`).join(", ") || "sem resistência" : o.valor;
      return `<option value="${o.id}" ${cfg.equip[p] === o.id ? "selected" : ""}>${esc(o.nome)} (${esc(val)})</option>`;
    }).join("")}</select></label>`).join("");

    const grupos = Object.keys(cat.origens).map((orig) => `<h3 class="origem">${esc(cat.origens[orig])}</h3>` + [1, 2, 3, "ultimate"].map((t) => {
      const hs = cat.habilidades.filter((h) => h.tier === t && h.origem === orig);
      if (!hs.length) return "";
      return `<h4>${TIER[t]} · ${hs[0].pontos} ponto${hs[0].pontos > 1 ? "s" : ""}${t === "ultimate" ? " · no máximo uma; uma vez por luta" : ""}</h4>` + hs.map((h) => {
        const tem = cfg.kit.includes(h.id), m = motivoKit(h);
        return `<button class="hab${tem ? " no-kit" : ""}${m ? " nao" : ""}" data-hab="${h.id}" ${m ? 'aria-disabled="true"' : ""} aria-pressed="${tem}" title="${esc(infoTxt(h.info))}">` +
          `<span class="marca">${tem ? "✓" : ""}</span><b>${esc(h.nome)}</b><span class="custo">${h.custo ? `${h.custo} de Vigor` : "sem custo"}</span>` +
          (h.info ? `<span class="linha-tipo"><i class="tipo-dano t-${h.info.tipo_id}">${esc(h.info.tipo)}</i> ${esc(h.info.escala)}</span>` : "") +
          `<span class="desc">${esc(m || h.desc)}</span></button>`;
      }).join("");
    }).join("")).join("");

    let ficha = "<p class='nota'>Calculando…</p>";
    if (F && !F.erro) {
      const der = F.derivados.filter((d) => !["defesa", "ultimate"].includes(d.id)).map((d) => `<li><span>${esc(d.nome)}</span><b>${esc(d.valor)}</b><small>${esc(d.como)}</small></li>`).join("");
      const u = F.ultimate;
      ficha = `<h3>${esc(nomeBuild())}</h3>` + (b ? `<p class="frase">${esc(b.frase)}</p><p class="troca"><b>Ganha:</b> ${esc(b.ganha)}. <b>Abre mão:</b> ${esc(b.abre_mao)}.</p>` : `<p class="frase">Construção livre.</p>`) +
        `<p class="ult-prep">${u ? `Ultimate: <b>${esc(u.nome)}</b>, uma vez por luta, ${u.custo} de Vigor, disponível desde o início.` : "<b>Sem ultimate equipada.</b>"}</p>` +
        (F.erro_atributos ? `<p class="falta">${esc(F.erro_atributos)} A ficha mostra a distribuição como está.</p>` : "") +
        `<ul class="derivados">${der}</ul>` +
        `<h4>Dano previsto por alvo <small>(normal; crítico e chance; passe o mouse para a conta)</small></h4>${tabelaDano()}${tabelaFogo() || tabelaCombo()}` +
        `<h4>Trocando só uma peça <small>(a mesma construção, nível e alvo)</small></h4>${tabelaEquip("arma")}${tabelaEquip("foco")}` +
        `<h4>Dano recebido por manto <small>(Jean, sem defender)</small></h4>${tabelaEquip("manto")}`;
    }
    const ultimate = cfg.kit.find((k) => hab(k).tier === "ultimate");
    $("#prep").innerHTML = `<div class="col m-painel"><h2>Construção</h2><div class="builds">${builds}</div>` +
      `<h4>Atributos de combate <small class="${soma === cat.orcamento ? "ok" : "falta"}">${soma} de ${cat.orcamento} pontos (cada um de ${cat.min} a ${cat.max})</small></h4><ul class="atr">${atr}</ul>` +
      `<ul class="atr">${pres}</ul><h4>Equipamento <small>(peças de laboratório)</small></h4><div class="equip">${equip}</div></div>` +
      `<div class="col m-painel"><h2>Kit</h2><p class="kit-soma"><b class="${pts <= cat.kit_pontos ? "ok" : "falta"}">${pts} de ${cat.kit_pontos} pontos</b> · ${cfg.kit.length} de ${cat.kit_espacos} espaços · ultimate: ${ultimate ? esc(nomeHab(ultimate)) : "nenhuma"}</p>` +
      `<p class="nota">Trocado aqui, fora da luta (como numa cidade ou acampamento). Fora do kit e dos pontos (hipótese): ${cat.basicos.map((x) => esc(x.nome)).join(", ")} e Usar item; os três gastam a ação. A especialização soma-se às habilidades do Guerreiro.</p>` +
      `<div class="habs">${grupos}</div></div>` +
      `<div class="col m-painel fichao">${ficha}</div>` +
      `<div class="rodape"><label>Encontro <select id="prep-encontro">${cat.encontros.map((e) => `<option value="${e.id}" ${e.id === $("#encontro").value ? "selected" : ""}>${esc(e.nome)}</option>`).join("")}</select></label>` +
      `<button class="botao lutar" ${soma === cat.orcamento ? "" : "disabled"}>Lutar com esta construção <kbd>Enter</kbd></button>` +
      (E ? `<button class="botao voltar">Voltar à luta <kbd>Esc</kbd></button>` : "") + `</div>`;
    const P = $("#prep");
    P.querySelectorAll("[data-build]").forEach((x) => x.addEventListener("click", () => usarBuild(x.dataset.build)));
    P.querySelector("[data-livre]").addEventListener("click", () => { cfg.build = null; salvarCfg(); });
    P.querySelectorAll("[data-atr]").forEach((x) => x.addEventListener("click", () => {
      const k = x.dataset.atr, v = cfg.atributos[k] + +x.dataset.d;
      if (v < cat.min || v > cat.max || (+x.dataset.d > 0 && somaAtr() >= cat.orcamento)) return;
      cfg.atributos[k] = v; salvarCfg();
    }));
    P.querySelectorAll("[data-pres]").forEach((x) => x.addEventListener("click", () => {
      const v = cfg.presenca + +x.dataset.pres;
      if (v >= cat.min && v <= cat.max) { cfg.presenca = v; salvarCfg(); }
    }));
    P.querySelectorAll("[data-equip]").forEach((x) => x.addEventListener("change", () => { cfg.equip[x.dataset.equip] = x.value; salvarCfg(); }));
    P.querySelectorAll("[data-hab]").forEach((x) => x.addEventListener("click", () => {
      const id = x.dataset.hab;
      if (cfg.kit.includes(id)) cfg.kit = cfg.kit.filter((k) => k !== id);
      else if (!motivoKit(hab(id))) cfg.kit = [...cfg.kit, id];
      else return;
      salvarCfg();
    }));
    P.querySelector(".lutar").addEventListener("click", () => { $("#encontro").value = $("#prep-encontro").value; iniciar(); });
    const v = P.querySelector(".voltar");
    if (v) v.addEventListener("click", () => abrirPrep(false));
  }

  // ---------------------------------------------------------------- começar e agir
  async function iniciar() {
    if (somaAtr() !== cat.orcamento) { abrirPrep(true); return; }
    const encontro = $("#encontro").value;
    guardado("encontro", encontro);
    const r = await api("/api4/iniciar", { encontro, ...corpoBuild() });
    if (r.erro) { abrirPrep(true); aviso = r.erro; return; }
    E = r; anterior = null; vistos = 0; sel = null; aviso = ""; fichaDe = "heroi";
    abrirPrep(false);
    desenhar();
  }
  async function agir(acao, alvo) {
    if (ocupado || !E || !E.aguardando) return;
    ocupado = true;
    sel = null;
    document.body.classList.add("ocupado");
    try {
      const r = await api("/api4/agir", { turno_id: E.turno_id, acao, alvo });
      if (r.estado) { anterior = E; E = r.estado; }
      aviso = r.ok ? "" : r.motivo === "Essa vez já passou." ? "" : r.motivo;
    } finally {
      ocupado = false;
      document.body.classList.remove("ocupado");
    }
    desenhar();
  }
  function escolher(a) {
    if (ocupado || a.motivo) return;
    if (a.alvos.length === 1) return agir(a.id, a.alvos[0]);
    sel = a;
    desenhar();
  }

  // ---------------------------------------------------------------- a luta
  function desenhar() {
    if (!E) return;
    const t = $("#teste");
    t.hidden = !E.teste;
    t.textContent = E.teste || "";
    $("#objetivo").innerHTML = `<b>${esc(E.nome)}</b> ${esc(E.objetivo)}`;
    $("#objetivo").title = E.objetivo;
    $("#resumo-build").innerHTML = `<b>${esc(nomeBuildId(E.build))}</b> · ${E.kit.map((k) => esc(nomeHab(k))).join(", ")}`;
    desenharOrdem();
    $("#grupo").innerHTML = E.aliados.map(cartaAliado).join("");
    $("#frente").innerHTML = E.inimigos.filter((o) => o.vivo).map(cartaInimigo).join("")
      + (E.inimigos.some((o) => !o.vivo) ? `<p class="caidos">Derrotados: ${E.inimigos.filter((o) => !o.vivo).map((o) => esc(o.nome)).join(", ")}</p>` : "");
    desenharDoca();
    desenharRegistro();
    desenharFicha();
    desenharFim();
    document.querySelectorAll(".carta[data-alvo]").forEach((c) => c.addEventListener("click", () => sel && agir(sel.id, c.dataset.id)));
    vistos = E.eventos.length;
  }
  function desenharOrdem() {
    const passos = E.ordem.map((o, i) => {
      const prep = E.ameacas.some((a) => a.de === o.id);
      const cls = ["passo", o.lado, o.atual ? "atual" : "", o.passou ? "passou" : "", o.fora ? "fora" : "", o.entra ? "espera" : ""].join(" ");
      const nota = o.atual ? "agora" : o.fora ? (o.lado === "aliado" ? `caíd${o.a}` : "fora") : o.entra ? `a partir da rodada ${o.entra}` : o.passou ? "já foi" : "";
      return `<div class="${cls}" title="${esc(o.nome)}"><span class="pos">${i + 1}</span>${retrato(o, 32)}${prep ? '<span class="perigo" aria-label="preparando">!</span>' : ""}` +
        `<span class="nome">${esc(o.nome)}</span><span class="nota">${nota}</span></div>`;
    }).join("");
    $("#ordem").innerHTML = `<div class="rodada"><span>Rodada</span><b>${E.rodada}</b></div>${passos}<div class="fim-rodada">fim da<br>rodada ${E.rodada}</div>`;
  }
  const barra = (classe, v, max, rotulo) => `<div class="barra ${classe}"><span style="width:${max ? Math.round((100 * v) / max) : 0}%"></span><em>${esc(rotulo)}</em><b>${v}/${max}</b></div>`;
  function delta(o) {
    if (!anterior) return "";
    const a = [...anterior.aliados, ...anterior.inimigos].find((x) => x.id === o.id);
    if (!a || a.vida === o.vida) return "";
    const d = o.vida - a.vida;
    return `<span class="delta ${d < 0 ? "perde" : "ganha"}">${d > 0 ? "+" : "−"}${Math.abs(d)}</span>`;
  }
  function estados(o) {
    return o.estados.length ? `<ul class="estados">${o.estados.map((s) => {
      const ic = ICONE_ESTADO[s.id] ? Icones.estado(ICONE_ESTADO[s.id], 16) : "";
      const extra = s.resta != null ? ` (${s.resta})` : s.pilhas ? ` ×${s.pilhas}` : "";
      return `<li class="est-${s.id}">${ic}<b>${esc(s.nome)}${extra}</b><span>${esc(s.ate)}</span></li>`;
    }).join("")}</ul>` : "";
  }
  const marcaAlvo = (o) => (sel && sel.alvos.includes(o.id) ? ` data-alvo="${sel.alvos.indexOf(o.id) + 1}"` : "");
  function previsaoAlvo(o) {
    if (!sel || !sel.alvos.includes(o.id)) return "";
    let t = "";
    if (sel.previsoes && sel.previsoes[o.id]) t = `${esc(sel.nome)}: <b>${prev(sel.previsoes[o.id])}</b> de dano`;
    else if (sel.cura) t = `${esc(sel.nome)}: <b>+${Math.min(sel.cura, o.vida_max - o.vida)}</b> de vida`;
    if (sel.resiste && sel.resiste[o.id] != null) t += ` · atordoa: resiste ${pct(sel.resiste[o.id])}`;
    if (sel.queima && sel.queima[o.id]) { const q = sel.queima[o.id]; t += ` · <span class="queima">Queimadura: ${q.pilhas} pilha${q.pilhas > 1 ? "s" : ""}, ${q.por_pingo} por pingo × ${q.vezes}</span>`; }
    return t ? `<p class="previsto">${t}</p>` : "";
  }
  const ULT = { disponivel: "disponível", recurso: "falta recurso", usada: "já usada nesta luta", alvo: "sem alvo" };
  function cartaAliado(o) {
    const pos = E.ordem.findIndex((x) => x.id === o.id) + 1;
    const ativo = E.aguardando === o.id, passo = E.ordem.find((x) => x.id === o.id);
    const situ = o.caido ? "" : ativo ? '<span class="tag vez">age agora</span>' : passo.passou ? '<span class="tag">já agiu</span>' : "";
    const u = o.ultimate;
    const ult = u ? `<div class="ult ult-${u.estado}" title="${esc(u.motivo || "uma vez por luta")}">Ultimate: <b>${esc(u.nome)}</b> · ${ULT[u.estado]}${u.estado === "recurso" ? ` (${u.custo})` : ""}</div>` : "";
    return `<article class="carta aliado${ativo ? " ativo" : ""}${o.caido ? " caido" : ""}" data-id="${o.id}"${marcaAlvo(o)}>
      <div class="cab">${retrato(o, 48)}<div><h3>${esc(o.nome)} ${situ}</h3><p class="papel">${esc(o.papel)} · ${pos}º na ordem · Tenacidade ${pct(o.tenacidade)}${Object.keys(o.res).length ? " · " + Object.entries(o.res).map(([k, v]) => `${k} ${pct(v)}`).join(", ") : ""}</p></div>${delta(o)}</div>
      ${barra("vida", o.vida, o.vida_max, "Vida")}
      ${o.caido ? `<p class="caido-nota">Caíd${o.a}: não age. Volta só com Reerguer ou a Pena de Fênix, na mesma posição.</p>` : barra("recurso r-" + o.recurso_nome.toLowerCase(), o.recurso, o.recurso_max, o.recurso_nome)}
      ${ult}${estados(o)}${previsaoAlvo(o)}
    </article>`;
  }
  function cartaInimigo(o) {
    const am = E.ameacas.find((a) => a.de === o.id);
    const tags = [];
    if (o.protecao) tags.push(`Proteção ${o.protecao}`);
    Object.entries(o.res).forEach(([k, v]) => tags.push(`Resiste ${k.toLowerCase()} ${pct(v)}`));
    tags.push(`Tenacidade ${pct(o.tenacidade)}`);
    if (o.golpe_tipo !== "Físico") tags.push(`ataca com ${o.golpe_tipo.toLowerCase()}`);
    if (o.ponto_fraco) tags.push(`Ponto fraco: ${o.ponto_fraco}`);
    if (o.entra_rodada > E.rodada) tags.push(`age a partir da rodada ${o.entra_rodada}`);
    return `<article class="carta inimigo${am ? " preparando" : ""}" data-id="${o.id}"${marcaAlvo(o)}>
      <div class="cab">${retrato(o, 48)}<div><h3>${esc(o.nome)}</h3><p class="papel">${E.ordem.findIndex((x) => x.id === o.id) + 1}º na ordem</p></div>${delta(o)}</div>
      ${barra("vida", o.vida, o.vida_max, "Vida")}
      ${o.guarda_max ? barra("guarda", o.guarda, o.guarda_max, o.guarda ? "Guarda: metade do dano físico" : "Guarda rompida") : ""}
      <p class="tags">${tags.map(esc).join(" · ")}</p>
      ${estados(o)}${previsaoAlvo(o)}
      ${am ? ameaca(am) : ""}
    </article>`;
  }
  function controle(c, resiste, nome) {
    const como = c === "atordoado" ? "atordoa" : "aterroriza";
    return `${esc(nome)}: ${como} (perde a próxima vez)` + (resiste >= 1 ? " — o Juramento impede" : resiste ? `, salvo se resistir: <b>${pct(resiste)}</b>` : ", sem chance de resistir");
  }
  function ameaca(a) {
    let alvo, conta = "";
    if (a.area) {
      alvo = "todo o grupo";
      conta = `<ul>${a.alvos.map((x) => `<li>${esc(x.nome)}: ${x.agora != null ? `<b>${x.agora}</b> de dano` : ""}${x.queima ? `, queima ${x.queima} por 2 turnos` : ""}${x.controle ? (x.agora != null ? "; " : "") + controle(x.controle, x.juramento ? 1 : x.resiste, "").replace(/^: /, "") : ""}</li>`).join("")}</ul>`;
    } else if (a.quem) {
      alvo = esc(a.mira_nome);
      conta = (a.quem !== a.mira ? `<p>${esc(a.quem_nome)} protege e recebe <b>${a.agora}</b>.</p>` : `<p>Recebe <b>${a.agora}</b> de dano${a.se_defender != null && a.se_defender < a.agora ? `; se defender, ${a.se_defender}` : ""}.</p>`)
        + (a.controle ? `<p class="efeito">${controle(a.controle, a.juramento ? 1 : a.resiste, a.quem_nome)}.</p>` : "")
        + (a.sangra ? `<p class="efeito">Sangra ${a.sangra} no início dos 2 próximos turnos de ${esc(a.quem_nome)}.</p>` : "");
    } else alvo = "o mais ferido";
    return `<div class="ameaca"><p class="titulo">${esc(a.nome)} em ${alvo} <small>(${esc(a.tipo || "")})</small></p>${conta}` +
      (a.ininterruptivel ? `<p class="efeito"><b>Ininterruptível:</b> não se desfaz, e ele fica firme até soltar.</p>` : `<p class="efeito">Pode ser interrompido.</p>`) +
      `<p class="quando">Resolve ${esc(a.resolve)}.</p></div>`;
  }
  function desenharDoca() {
    const d = $("#doca");
    if (E.fim) { d.innerHTML = ""; return; }
    const o = E.aliados.find((x) => x.id === E.aguardando);
    if (!o) { d.innerHTML = ""; return; }
    if (sel) {
      const nomes = sel.alvos.map((id, i) => `<kbd>${i + 1}</kbd> ${esc([...E.aliados, ...E.inimigos].find((x) => x.id === id).nome)}`).join(" · ");
      d.innerHTML = `<div class="quem">${retrato(o, 32)}<b>${esc(o.nome)}</b></div><div class="escolha-alvo"><p><b>${esc(sel.nome)}</b>${sel.info ? ` <small>(${esc(sel.info.tipo)})</small>` : ""}: escolha o alvo (clique na carta ou o número; o dano previsto aparece em cada carta, a conta no mouse). ${nomes}</p>` +
        `<button class="botao" id="cancelar">Voltar <kbd>Esc</kbd></button></div>`;
      $("#cancelar").addEventListener("click", () => { sel = null; desenhar(); });
      return;
    }
    const botoes = E.acoes.map((a, i) => {
      const custo = a.item ? `${a.qtd} na bolsa` : a.custo ? `${a.custo} de ${a.recurso}` : "sem custo";
      const ic = a.item ? Icones.consumivel(a.icone, 24) : "";
      const tipo = a.basico ? '<i class="tipo">básico</i>' : a.ultimate ? '<i class="tipo ult" title="uma vez por luta">ultimate</i>' : "";
      let previsto = "";
      if (!a.motivo && a.previsoes) {
        const vs = Object.values(a.previsoes).map((p) => p.normal);
        if (a.alvo === "inimigos") previsto = `${vs.join(" + ")} em todos` + (a.queima ? `; Queimadura em ${Object.keys(a.queima).length}` : "");
        else if (vs.length) previsto = Math.min(...vs) === Math.max(...vs) ? `${vs[0]} de dano` : `${Math.min(...vs)}–${Math.max(...vs)} de dano`;
      }
      if (!a.motivo && a.cura) previsto = `cura ${a.cura}`;
      const dica = [a.info ? infoTxt(a.info) : "", a.desc].filter(Boolean).join(" — ");
      return `<button class="acao${a.motivo ? " nao" : ""}${a.item ? " item" : ""}${a.ultimate ? " ult" : ""}" data-i="${i}" ${a.motivo ? 'aria-disabled="true"' : ""} title="${esc(dica)}">` +
        `<span class="tecla">${i + 1}</span>${ic}<b>${esc(a.nome)}</b>${tipo}<span class="custo">${esc(custo)}</span>` +
        (a.info ? `<i class="tipo-dano t-${a.info.tipo_id}">${esc(a.info.tipo)}</i>` : "") +
        (previsto ? `<span class="previsto">${esc(previsto)}</span>` : "") +
        `<span class="desc">${esc(a.motivo || a.desc)}</span></button>`;
    }).join("");
    d.innerHTML = `<div class="quem">${retrato(o, 32)}<b>${esc(o.nome)}</b><span>${o.recurso} de ${o.recurso_max}<br>${esc(o.recurso_nome)}</span></div><div class="acoes">${botoes}</div>` +
      (aviso ? `<p class="aviso">${esc(aviso)}</p>` : "");
    d.querySelectorAll(".acao").forEach((b) => b.addEventListener("click", () => escolher(E.acoes[+b.dataset.i])));
  }
  function desenharRegistro() {
    const r = $("#registro");
    let html = "";
    E.eventos.forEach((ev, i) => {
      if (ev.tipo === "rodada") { html += `<h4>${esc(ev.texto)}</h4>`; return; }
      const novo = i >= vistos && vistos > 0;
      html += `<p class="ev ev-${ev.tipo}${novo ? " novo" : ""}" style="--i:${Math.max(0, i - vistos)}">${esc(ev.texto)}` + (ev.conta ? `<small>${esc(ev.conta)}</small>` : "") + "</p>";
    });
    r.innerHTML = html;
    r.scrollTop = r.scrollHeight;
  }
  function desenharFicha() {
    const o = E.aliados.find((x) => x.id === fichaDe);
    const seletor = E.aliados.map((a) => `<button data-ficha="${a.id}" class="${a.id === fichaDe ? "atual" : ""}">${esc(a.nome)}</button>`).join("");
    const atr = cat.atributos.map((a) => `<li><span>${esc(a.nome)}</span><b>${o.atributos[a.id]}</b></li>`).join("") + (o.id === "heroi" ? `<li class="fora"><span>Presença</span><b>${E.presenca}</b></li>` : "");
    const der = o.derivados.map((d) => `<li><span>${esc(d.nome)}</span><b>${esc(d.valor)}</b><small>${esc(d.como)}</small></li>`).join("");
    const habs = E.aguardando === o.id ? E.acoes.filter((a) => a.info).map((a) => `<li><span>${esc(a.nome)}</span><small>${esc(infoTxt(a.info))}</small></li>`).join("") : "";
    $("#ficha").innerHTML = `<div class="seletor">${seletor}</div>` +
      (o.id === "heroi" ? `<p class="nota">Construção: ${esc(nomeBuildId(E.build))}. Presença não age na luta.</p>` : `<p class="nota">Atributos próprios do companheiro.</p>`) +
      `<h4>Atributos</h4><ul class="atributos">${atr}</ul><h4>O que eles dão agora</h4><ul class="derivados">${der}</ul>` +
      (habs ? `<h4>Os golpes desta vez: tipo, potência e defesa</h4><ul class="derivados habs-info">${habs}</ul>` : "");
    $("#ficha").querySelectorAll("[data-ficha]").forEach((b) => b.addEventListener("click", () => { fichaDe = b.dataset.ficha; desenharFicha(); }));
  }
  function contaAmeacas(r) {
    const c = { anunciadas: r.ameacas.length, interrompida: 0, resolvida: 0, desfeita: 0 };
    r.ameacas.forEach((a) => { if (!a.resultado) return; const k = a.resultado.startsWith("desfeita") ? "desfeita" : a.resultado; c[k] = (c[k] || 0) + 1; });
    return c;
  }
  function desenharFim() {
    const f = $("#fim");
    f.hidden = !E.fim;
    if (!E.fim) return;
    const r = E.resumo, h = r.recurso.heroi, am = contaAmeacas(r), u = r.ultimates.heroi;
    const basicos = (r.acoes.atacar || 0), total = Object.values(r.acoes).reduce((a, b) => a + b, 0);
    f.innerHTML = `<div class="m-janela"><h2>${E.fim === "vitoria" ? "Vitória" : "Derrota"}</h2><p>${E.fim === "vitoria" ? "Na" : "Até a"} rodada ${E.rodada}. ` +
      `Quedas: ${r.quedas}. Ameaças: ${am.anunciadas} anunciadas, ${am.interrompida} interrompidas, ${am.resolvida} resolvidas, ${am.desfeita} desfeitas; ${r.adiamentos.length} adiadas por controle.</p>` +
      `<p>Ultimate de Jean: ${u.equipada ? `${esc(nomeHab(u.equipada))}, ${u.uso ? `usada na rodada ${u.uso.rodada} (turno ${u.uso.turno} dele)` : "não usada"}; disponível em ${u.turnos_disponivel} turno(s), sem recurso em ${u.turnos_sem_recurso}` : "sem ultimate equipada"}.</p>` +
      `<p>Ataques básicos: ${basicos} de ${total} ações. Vigor de Jean: gastou ${h.gasto}, recuperou ${h.turno} nos turnos e ${h.basico} atacando.</p>` +
      `<div class="botoes"><button class="botao" id="fim-reiniciar">Reiniciar <kbd>R</kbd></button><button class="botao" id="fim-preparar">Outra construção <kbd>P</kbd></button><button class="botao" data-abrir="resultados">Resultados da sessão</button></div></div>`;
    $("#fim-reiniciar").addEventListener("click", iniciar);
    $("#fim-preparar").addEventListener("click", () => abrirPrep(true));
    f.querySelector("[data-abrir]").addEventListener("click", () => abrir("resultados"));
  }

  // ---------------------------------------------------------------- janelas
  async function abrir(qual) {
    const m = $("#modal"), c = $("#modal-corpo");
    m.hidden = false;
    m.dataset.qual = qual;
    if (qual === "comparar") await janelaComparar(c);
    if (qual === "situacao") await janelaSituacao(c);
    if (qual === "resultados") await janelaResultados(c);
    m.querySelector(".fechar").focus();
  }
  function fechar() { $("#modal").hidden = true; }
  async function janelaComparar(c) {
    const r = await api("/api4/comparar", { equip: cfg.equip });
    const cols = r.colunas;
    const linha = (rot, vals, cls = "") => `<tr class="${new Set(vals.map(String)).size > 1 ? "difere" : ""} ${cls}"><th>${rot}</th>${vals.map((v) => `<td>${v}</td>`).join("")}</tr>`;
    const nomeD = (id) => cols[0].derivados.find((d) => d.id === id).nome;
    let html = linha("Proposta", cols.map((k) => esc(k.frase)), "texto") + linha("Ganha", cols.map((k) => esc(k.ganha)), "texto") + linha("Abre mão", cols.map((k) => esc(k.abre_mao)), "texto");
    html += cat.atributos.map((a) => linha(esc(a.nome), cols.map((k) => k.atributos[a.id]))).join("");
    html += ["vida", "iniciativa", "recurso_max", "fisico", "arcano", "critico", "ponto_fraco", "tenacidade"].map((id) =>
      linha(esc(nomeD(id)) + (id === "iniciativa" ? " <small>(encontro 2)</small>" : ""), cols.map((k) => esc(k.derivados.find((d) => d.id === id).valor)))).join("");
    html += linha("Ultimate", cols.map((k) => (k.ultimate ? esc(k.ultimate.nome) : "nenhuma")));
    html += `<tr class="sep"><th colspan="${cols.length + 1}">Dano previsto (normal) no Bruto · Xamã · Cão <small>(proteção 2 e ponto fraco · 30% arcano · 60% fogo); ✓ no kit sugerido</small></th></tr>`;
    html += cols[0].dano_todos.map((d, j) => linha(esc(d.nome), cols.map((k) => { const x = k.dano_todos[j].alvos; return `${x.bruto.normal} · ${x.xama.normal} · ${x.cao.normal}${k.kit.includes(d.id) || d.id === "atacar" ? " ✓" : ""}`; }))).join("");
    html += linha("Kit sugerido", cols.map((k) => `${k.kit.map((x) => esc(nomeHab(x))).join(", ")} <small>(${k.pontos_kit} pts)</small>`), "texto");
    c.innerHTML = `<h2>Comparar construções</h2><p class="nota">O mesmo Jean: nível 3, o equipamento escolhido em Preparar, proteção 3, os mesmos companheiros. Só os ${cat.orcamento} pontos (e o kit sugerido) mudam. Em destaque, o que difere.</p>` +
      `<div class="comparar"><table><thead><tr><th></th>${cols.map((k) => `<th>${esc(k.nome)}</th>`).join("")}</tr></thead><tbody>${html}</tbody></table></div>`;
  }
  async function janelaSituacao(c, escolha, ajuda) {
    const s = await api("/api4/situacao", { atributos: cfg.atributos, presenca: cfg.presenca, escolha, ajuda });
    const ops = s.opcoes.map((o) => `<li><button class="botao" data-op="${o.id}">${esc(o.texto)}</button>` +
      `<span class="req ${o.valor >= o.minimo ? "ok" : "falta"}">${esc(o.atributo)} ${o.valor} (a situação pede ${o.minimo})</span>` +
      (o.ajuda ? `<button class="botao" data-op="${o.id}" data-ajuda="1">${esc(o.ajuda.texto)}</button>` : "") + "</li>").join("");
    c.innerHTML = `<h2>${esc(s.titulo)}</h2><p class="nota">Fora da luta, com a construção escolhida (${esc(nomeBuild())}, Presença ${cfg.presenca}). Os companheiros acrescentam, mas a escolha continua sendo de Jean.</p>` +
      `<p class="prosa">${esc(s.texto)}</p><ul class="opcoes">${ops}</ul>` +
      (s.resultado ? `<p class="resultado ${s.resultado.ok ? "ok" : "falta"}">${esc(s.resultado.texto)} <small>${esc(s.resultado.como)}</small></p>` : "");
    c.querySelectorAll("[data-op]").forEach((b) => b.addEventListener("click", () => janelaSituacao(c, b.dataset.op, !!b.dataset.ajuda)));
  }
  async function janelaResultados(c, aberto) {
    const r = await api("/api4/resultados");
    const linhas = r.resultados.map((x, i) => {
      const tot = Object.values(x.acoes).reduce((a, b) => a + b, 0), h = x.recurso.heroi, am = contaAmeacas(x), u = x.ultimates.heroi;
      return `<tr><td>${esc(x.hora)}</td><td>${esc(x.nome)}</td><td>${esc(nomeBuildId(x.build))}<small>${x.kit_nomes.map(esc).join(", ")} · ${esc(Object.values(x.equip).join(", "))}</small></td><td>${esc(x.fim)}</td>` +
        `<td>${x.rodadas}</td><td>${x.quedas}</td><td>${x.acoes.atacar || 0} de ${tot}</td><td>${h.gasto} / ${h.turno} + ${h.basico}</td>` +
        `<td>${am.anunciadas} · ${am.interrompida} · ${am.resolvida} · ${am.desfeita} · ${x.adiamentos.length}</td>` +
        `<td>${u.equipada ? `${esc(nomeHab(u.equipada))}: ${u.uso ? `rodada ${u.uso.rodada}` : "não usada"}<small>disponível ${u.turnos_disponivel}, sem recurso ${u.turnos_sem_recurso}, já usada ${u.turnos_ja_usada}</small>` : "sem ultimate"}</td>` +
        `<td><button class="botao detalhe" data-i="${i}">ver</button></td></tr>`;
    }).join("");
    let det = "";
    if (aberto != null && r.resultados[aberto]) {
      const x = r.resultados[aberto];
      det = `<h3>${esc(x.nome)} · ${esc(nomeBuildId(x.build))} (${esc(x.hora)})</h3><div class="detalhes"><div><h4>Ameaças</h4><ul>${x.ameacas.map((a) => `<li>Rodada ${a.rodada}: ${esc(a.inimigo)} prepara ${esc(a.nome)}${a.ininterruptivel ? " (ininterruptível)" : ""} → ${esc(a.resultado || "em curso")}${a.rodada_fim ? ` na rodada ${a.rodada_fim}` : ""}${a.dano != null ? `, ${a.dano} de dano` : ""}${a.aparada ? ", aparada" : ""}</li>`).join("") || "<li>nenhuma</li>"}</ul>` +
        `<h4>Adiadas por controle</h4><ul>${x.adiamentos.map((a) => `<li>Rodada ${a.rodada}: ${esc(a.inimigo)} ${esc(a.estado)}</li>`).join("") || "<li>nenhuma</li>"}</ul></div>` +
        `<div><h4>Ações (recurso antes → depois)</h4><ol class="linha">${x.linha.map((l) => `<li>R${l.rodada} · ${esc(l.ator)} · ${esc(l.acao.startsWith("item:") ? l.acao.slice(5) : nomeHab(l.acao))}${l.alvo && l.alvo !== l.ator ? ` → ${esc(l.alvo)}` : ""} · ${l.antes} → ${l.depois}</li>`).join("")}</ol></div></div>`;
    }
    c.innerHTML = `<h2>Resultados da sessão</h2><p class="nota">Cada luta terminada ou reiniciada, guardada só nesta execução em <code>${esc(r.pasta)}</code>. "ver" abre as ameaças uma a uma e o recurso antes e depois de cada ação.</p>` +
      (linhas ? `<table class="resultados"><thead><tr><th>Hora</th><th>Encontro</th><th>Build, kit, equipamento</th><th>Fim</th><th>Rodadas</th><th>Quedas</th><th>Básicos</th><th>Vigor de Jean: gasto / turno + básico</th><th>Ameaças: anunc. · interromp. · resolv. · desfeitas · adiadas</th><th>Ultimate de Jean</th><th></th></tr></thead><tbody>${linhas}</tbody></table>${det}`
        : "<p>Nenhuma luta terminada ainda.</p>");
    c.querySelectorAll(".detalhe").forEach((b) => b.addEventListener("click", () => janelaResultados(c, +b.dataset.i)));
  }

  // ---------------------------------------------------------------- teclado
  document.addEventListener("keydown", (e) => {
    if (e.repeat || e.ctrlKey || e.altKey || e.metaKey) return;
    if (!$("#modal").hidden) { if (e.key === "Escape") fechar(); return; }
    if (!$("#prep").hidden) {
      if (e.key === "Escape" && E) abrirPrep(false);
      if (e.key === "Enter" && !(e.target instanceof HTMLButtonElement) && !(e.target instanceof HTMLSelectElement)) { e.preventDefault(); $("#prep .lutar").click(); }
      return;
    }
    if (e.key === "Escape" && sel) { sel = null; desenhar(); return; }
    if (e.key === "r" || e.key === "R") { e.preventDefault(); iniciar(); return; }
    if (e.key === "p" || e.key === "P") { e.preventDefault(); abrirPrep(true); return; }
    const n = parseInt(e.key, 10);
    if (!E || E.fim || !E.aguardando || !(n >= 1)) return;
    if (sel) { if (sel.alvos[n - 1]) agir(sel.id, sel.alvos[n - 1]); return; }
    if (E.acoes[n - 1]) escolher(E.acoes[n - 1]);
  });

  // ---------------------------------------------------------------- abrir
  async function comecar() {
    cat = await api("/api4/catalogo");
    const g = guardado("cfg");
    const b0 = cat.builds[0];
    cfg = { build: b0.id, atributos: { ...b0.atributos }, kit: [...b0.kit], equip: { ...cat.equip_padrao }, presenca: cat.presenca };
    if (g && g.atributos && cat.atributos.every((a) => Number.isInteger(g.atributos[a.id])) && Array.isArray(g.kit) && g.kit.every((k) => hab(k)))
      cfg = { ...cfg, ...g, equip: { ...cfg.equip, ...(g.equip || {}) } };
    $("#encontro").innerHTML = cat.encontros.map((e) => `<option value="${e.id}">${esc(e.nome)}</option>`).join("");
    const enc = guardado("encontro");
    if (cat.encontros.some((e) => e.id === enc)) $("#encontro").value = enc;
    $("#encontro").addEventListener("change", iniciar);
    $("#reiniciar").addEventListener("click", iniciar);
    $("#preparar").addEventListener("click", () => abrirPrep(true));
    document.querySelectorAll("#topo [data-abrir]").forEach((b) => b.addEventListener("click", () => abrir(b.dataset.abrir)));
    $("#modal .fechar").addEventListener("click", fechar);
    $("#modal").addEventListener("click", (e) => { if (e.target.id === "modal") fechar(); });
    document.querySelectorAll("#abas button").forEach((b) => b.addEventListener("click", () => {
      document.querySelectorAll("#abas button").forEach((x) => x.classList.toggle("atual", x === b));
      $("#registro").hidden = b.dataset.aba !== "registro";
      $("#ficha").hidden = b.dataset.aba !== "ficha";
    }));
    document.querySelectorAll("#topo select").forEach((s) => s.addEventListener("keydown", (e) => { if (/^[0-9rRpP]$/.test(e.key)) e.preventDefault(); }));
    F = await api("/api4/ficha", corpoBuild());
    abrirPrep(true);
  }
  window.Demo = { get estado() { return E; }, get cfg() { return cfg; }, get ficha() { return F; }, agir, iniciar, abrir, abrirPrep };
  comecar();
})();
