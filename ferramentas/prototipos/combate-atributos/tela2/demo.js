/* PROTÓTIPO do combate e dos atributos, segunda versão (26/10/2026; nada no jogo): a tela só desenha o que o servidor
   manda (motor2/regras.py decide tudo, inclusive custos, alvos, motivos, previsões de dano e chances de resistir).
   Duas telas: Preparar (a construção, o kit e o que eles fazem) e a luta. */
"use strict";
(() => {
  const $ = (s) => document.querySelector(s);
  const esc = (t) => String(t ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const pct = (x) => `${Math.round(x * 100)}%`;
  const guardado = (k, v) => { try { if (v === undefined) return JSON.parse(localStorage.getItem("combate-atr2:" + k)); localStorage.setItem("combate-atr2:" + k, JSON.stringify(v)); } catch (e) { return null; } return null; };
  const ICONE_ESTADO = { atordoado: "atordoado", sangramento: "sangramento", marca: "marcado", defesa: "guarda",
                         escudo: "barreira", comando: "fortalecido", desafio: "provocando", juramento: "firme" };
  const TIER = { 1: "Tier 1", 2: "Tier 2", 3: "Tier 3", ultimate: "Ultimate" };

  let cat = null, E = null, anterior = null, vistos = 0, ocupado = false, sel = null, aviso = "", fichaDe = "heroi";
  let cfg = null, F = null;  // a construção escolhida e a ficha dela

  async function api(caminho, corpo) {
    const r = await fetch(caminho, corpo ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(corpo) } : undefined);
    return r.json();
  }
  const retrato = (o, lado) => (o.lado === "aliado" ? Icones.cabeca(o.retrato, lado) : Icones.criatura(o.retrato, lado))
    || `<span class="sem-retrato" style="--s:${lado}">${esc(o.nome[0])}</span>`;
  const nomeHab = (id) => (cat.habilidades.find((h) => h.id === id) || cat.basicos.find((h) => h.id === id) || { nome: id }).nome;
  const somaAtr = () => cat.atributos.reduce((s, a) => s + cfg.atributos[a.id], 0);
  const presetIgual = () => { const b = cat.builds.find((x) => x.id === cfg.build); return b && cat.atributos.every((a) => b.atributos[a.id] === cfg.atributos[a.id]); };
  const corpoBuild = () => ({ build: presetIgual() ? cfg.build : null, atributos: cfg.atributos, kit: cfg.kit, equip: cfg.equip, presenca: cfg.presenca });
  const nomeBuild = () => (presetIgual() ? cat.builds.find((x) => x.id === cfg.build).nome : "Livre");
  const prev = (p) => `${p.normal}${p.chance ? ` <small>crít. ${p.critico} (${pct(p.chance)})</small>` : ""}`;

  // ---------------------------------------------------------------- preparar: a construção e o kit
  function usarBuild(id) {
    const b = cat.builds.find((x) => x.id === id);
    cfg = { ...cfg, build: id, atributos: { ...b.atributos }, kit: [...b.kit] };
    salvarCfg();
  }
  function salvarCfg() { guardado("cfg", cfg); atualizarFicha(); }
  async function atualizarFicha() {
    F = await api("/api2/ficha", corpoBuild());
    desenharPrep();
  }
  function abrirPrep(sim = true) {
    document.body.classList.toggle("preparando", sim);
    $("#prep").hidden = !sim;
    if (sim) { desenharPrep(); const b = $("#prep .lutar"); if (b) b.focus(); }
  }

  function motivoKit(h) {
    if (cfg.kit.includes(h.id)) return null;
    const pts = cfg.kit.reduce((s, k) => s + cat.habilidades.find((x) => x.id === k).pontos, 0);
    if (h.tier === "ultimate" && cfg.kit.some((k) => cat.habilidades.find((x) => x.id === k).tier === "ultimate")) return "Já há uma ultimate no kit.";
    if (cfg.kit.length >= cat.kit_espacos) return `Os ${cat.kit_espacos} espaços estão ocupados.`;
    if (pts + h.pontos > cat.kit_pontos) return `Faltam ${pts + h.pontos - cat.kit_pontos} ponto(s) de kit.`;
    return null;
  }

  function desenharPrep() {
    if (!cfg || $("#prep").hidden) return;
    const soma = somaAtr(), pts = cfg.kit.reduce((s, k) => s + cat.habilidades.find((x) => x.id === k).pontos, 0);
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
    const equip = ["arma", "foco"].map((p) => `<label>${p === "arma" ? "Arma" : "Foco"} <select data-equip="${p}">${cat.equipamento[p].map((o) => `<option value="${o.id}" ${cfg.equip[p] === o.id ? "selected" : ""}>${esc(o.nome)} (${o.valor})</option>`).join("")}</select></label>`).join("");

    const grupos = [1, 2, 3, "ultimate"].map((t) => {
      const hs = cat.habilidades.filter((h) => h.tier === t);
      return `<h4>${TIER[t]} · ${hs[0].pontos} ponto${hs[0].pontos > 1 ? "s" : ""}${t === "ultimate" ? " · no máximo uma; pede Ímpeto, não recurso" : ""}</h4>` + hs.map((h) => {
        const tem = cfg.kit.includes(h.id), m = motivoKit(h);
        return `<button class="hab${tem ? " no-kit" : ""}${m ? " nao" : ""}" data-hab="${h.id}" ${m ? 'aria-disabled="true"' : ""} aria-pressed="${tem}">` +
          `<span class="marca">${tem ? "✓" : ""}</span><b>${esc(h.nome)}</b><span class="custo">${h.custo ? `${h.custo} de Vigor` : t === "ultimate" ? `${cat.impeto} de Ímpeto` : "sem custo"}</span>` +
          `<span class="desc">${esc(m || h.desc)}</span></button>`;
      }).join("");
    }).join("");

    let ficha = "<p class='nota'>Calculando…</p>";
    if (F && !F.erro) {
      const der = F.derivados.filter((d) => d.id !== "defesa").map((d) => `<li><span>${esc(d.nome)}</span><b>${esc(d.valor)}</b><small>${esc(d.como)}</small></li>`).join("");
      const dano = F.dano.map((d) => `<tr><td>${esc(d.nome)}${d.ultimate ? " <small>ult.</small>" : ""}</td><td>${d.custo ? d.custo : d.ultimate ? "Ímpeto" : "—"}</td><td class="num">${d.normal}</td><td class="num">${d.chance ? `${d.critico} <small>(${pct(d.chance)})</small>` : "—"}</td></tr>`).join("");
      const eq = (p) => {
        const L = F.equipamento[p].linhas;
        if (!L[0].dano.length) return `<p class="nota">${p === "arma" ? "Nenhum golpe físico no kit." : "Nenhum golpe sobrenatural no kit: o foco não muda nada nesta construção."}</p>`;
        return `<table class="eq"><thead><tr><th>${p === "arma" ? "Arma" : "Foco"}</th>${L[0].dano.map((d) => `<th>${esc(d.nome)}</th>`).join("")}</tr></thead><tbody>` +
          L.map((l) => `<tr class="${cfg.equip[p] === l.id ? "atual" : ""}"><td>${esc(l.nome)} (${l.valor})</td>${l.dano.map((d) => `<td class="num">${d.normal}</td>`).join("")}</tr>`).join("") + "</tbody></table>";
      };
      ficha = `<h3>${esc(nomeBuild())}</h3>` + (b ? `<p class="frase">${esc(b.frase)}</p><p class="troca"><b>Ganha:</b> ${esc(b.ganha)}. <b>Abre mão:</b> ${esc(b.abre_mao)}.</p>` : `<p class="frase">Construção livre.</p>`) +
        (F.erro_atributos ? `<p class="falta">${esc(F.erro_atributos)} A ficha mostra a distribuição como está.</p>` : "") +
        `<ul class="derivados">${der}</ul>` +
        `<h4>Dano previsto no ${esc(F.alvo.nome)} <small>(proteção ${F.alvo.protecao}, ponto fraco)</small></h4>` +
        `<table class="dano"><thead><tr><th>Golpe</th><th>Vigor</th><th>Normal</th><th>Crítico</th></tr></thead><tbody>${dano}</tbody></table>` +
        `<h4>Trocando só uma peça <small>(a mesma construção, nível e alvo)</small></h4>${eq("arma")}${eq("foco")}`;
    }
    const ultimate = cfg.kit.find((k) => cat.habilidades.find((x) => x.id === k).tier === "ultimate");
    $("#prep").innerHTML = `<div class="col m-painel"><h2>Construção</h2><div class="builds">${builds}</div>` +
      `<h4>Atributos de combate <small class="${soma === cat.orcamento ? "ok" : "falta"}">${soma} de ${cat.orcamento} pontos (cada um de ${cat.min} a ${cat.max})</small></h4><ul class="atr">${atr}</ul>` +
      `<ul class="atr">${pres}</ul><h4>Equipamento</h4><div class="equip">${equip}</div></div>` +
      `<div class="col m-painel"><h2>Kit</h2><p class="kit-soma"><b class="${pts <= cat.kit_pontos ? "ok" : "falta"}">${pts} de ${cat.kit_pontos} pontos</b> · ${cfg.kit.length} de ${cat.kit_espacos} espaços · ultimate: ${ultimate ? esc(nomeHab(ultimate)) : "nenhuma"}</p>` +
      `<p class="nota">Fora do kit e dos pontos (hipótese desta versão): ${cat.basicos.map((x) => esc(x.nome)).join(", ")} e Usar item. Os três gastam a ação do turno. Pontos de kit não são de aprender nem o recurso da luta.</p>` +
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
      const id = x.dataset.hab, h = cat.habilidades.find((y) => y.id === id);
      if (cfg.kit.includes(id)) cfg.kit = cfg.kit.filter((k) => k !== id);
      else if (!motivoKit(h)) cfg.kit = [...cfg.kit, id];
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
    const r = await api("/api2/iniciar", { encontro, ...corpoBuild() });
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
      const r = await api("/api2/agir", { turno_id: E.turno_id, acao, alvo });
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
    $("#resumo-build").innerHTML = `<b>${esc(E.build === "livre" ? "Livre" : cat.builds.find((b) => b.id === E.build).nome)}</b> · ${E.kit.map((k) => esc(nomeHab(k))).join(", ")}`;
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

  function barra(classe, v, max, rotulo) {
    return `<div class="barra ${classe}"><span style="width:${max ? Math.round((100 * v) / max) : 0}%"></span><em>${esc(rotulo)}</em><b>${v}/${max}</b></div>`;
  }
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
      const extra = s.resta != null ? ` (${s.resta})` : "";
      return `<li class="est-${s.id}">${ic}<b>${esc(s.nome)}${extra}</b><span>${esc(s.ate)}</span></li>`;
    }).join("")}</ul>` : "";
  }
  function marcaAlvo(o) {
    if (!sel || !sel.alvos.includes(o.id)) return "";
    return ` data-alvo="${sel.alvos.indexOf(o.id) + 1}"`;
  }
  function previsaoAlvo(o) {
    if (!sel || !sel.alvos.includes(o.id)) return "";
    if (sel.previsoes && sel.previsoes[o.id]) return `<p class="previsto">${esc(sel.nome)}: <b>${prev(sel.previsoes[o.id])}</b> de dano</p>`;
    if (sel.cura) return `<p class="previsto">${esc(sel.nome)}: <b>+${Math.min(sel.cura, o.vida_max - o.vida)}</b> de vida</p>`;
    return "";
  }

  function cartaAliado(o) {
    const pos = E.ordem.findIndex((x) => x.id === o.id) + 1;
    const ativo = E.aguardando === o.id, passo = E.ordem.find((x) => x.id === o.id);
    const situ = o.caido ? "" : ativo ? '<span class="tag vez">age agora</span>' : passo.passou ? '<span class="tag">já agiu</span>' : "";
    const imp = o.id === "heroi" && o.tem_ultimate ? `<div class="impeto" title="Sobe quando um inimigo cai ou uma ameaça é desfeita ou aparada">Ímpeto ${"◆".repeat(o.impeto)}${"◇".repeat(E.impeto_max - o.impeto)} <small>${o.impeto} de ${E.impeto_max}</small></div>` : "";
    return `<article class="carta aliado${ativo ? " ativo" : ""}${o.caido ? " caido" : ""}" data-id="${o.id}"${marcaAlvo(o)}>
      <div class="cab">${retrato(o, 48)}<div><h3>${esc(o.nome)} ${situ}</h3><p class="papel">${esc(o.papel)} · ${pos}º na ordem · Tenacidade ${pct(o.tenacidade)}</p></div>${delta(o)}</div>
      ${barra("vida", o.vida, o.vida_max, "Vida")}
      ${o.caido ? `<p class="caido-nota">Caíd${o.a}: não age. Volta só com Reerguer ou a Pena de Fênix, na mesma posição.</p>` : barra("recurso r-" + o.recurso_nome.toLowerCase(), o.recurso, o.recurso_max, o.recurso_nome)}
      ${imp}${estados(o)}${previsaoAlvo(o)}
    </article>`;
  }

  function cartaInimigo(o) {
    const am = E.ameacas.find((a) => a.de === o.id);
    const tags = [];
    if (o.protecao) tags.push(`Proteção ${o.protecao}`);
    tags.push(`Tenacidade ${pct(o.tenacidade)}`);
    if (o.ponto_fraco) tags.push(`Ponto fraco: ${o.ponto_fraco}`);
    if (o.interrompido) tags.push("já interrompido: a próxima preparação é firme");
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
      conta = `<ul>${a.alvos.map((x) => `<li>${controle(a.controle || "aterrorizado", x.juramento ? 1 : x.resiste, x.nome)}</li>`).join("")}</ul>`;
    } else if (a.quem) {
      alvo = esc(a.mira_nome);
      conta = (a.quem !== a.mira ? `<p>${esc(a.quem_nome)} protege e recebe <b>${a.agora}</b>.</p>` : `<p>Recebe <b>${a.agora}</b> de dano${a.se_defender != null && a.se_defender < a.agora ? `; se defender, ${a.se_defender}` : ""}.</p>`)
        + (a.controle ? `<p class="efeito">${controle(a.controle, a.juramento ? 1 : a.resiste, a.quem_nome)}.</p>` : "")
        + (a.sangra ? `<p class="efeito">Sangra ${a.sangra} no início dos 2 próximos turnos de ${esc(a.quem_nome)}.</p>` : "");
    } else alvo = "o mais ferido";
    return `<div class="ameaca"><p class="titulo">${esc(a.nome)} em ${alvo}</p>${conta}` +
      (a.firme ? `<p class="efeito"><b>Firme:</b> já foi interrompido uma vez; desta vez não se desfaz.</p>` : "") +
      `<p class="quando">Resolve ${esc(a.resolve)}.</p></div>`;
  }

  function desenharDoca() {
    const d = $("#doca");
    if (E.fim) { d.innerHTML = ""; return; }
    const o = E.aliados.find((x) => x.id === E.aguardando);
    if (!o) { d.innerHTML = ""; return; }
    if (sel) {
      const nomes = sel.alvos.map((id, i) => `<kbd>${i + 1}</kbd> ${esc([...E.aliados, ...E.inimigos].find((x) => x.id === id).nome)}`).join(" · ");
      d.innerHTML = `<div class="quem">${retrato(o, 32)}<b>${esc(o.nome)}</b></div><div class="escolha-alvo"><p><b>${esc(sel.nome)}</b>: escolha o alvo (clique na carta ou o número; o dano previsto aparece em cada carta). ${nomes}</p>` +
        `<button class="botao" id="cancelar">Voltar <kbd>Esc</kbd></button></div>`;
      $("#cancelar").addEventListener("click", () => { sel = null; desenhar(); });
      return;
    }
    const botoes = E.acoes.map((a, i) => {
      const custo = a.item ? `${a.qtd} na bolsa` : a.ultimate ? `${E.impeto_max} de Ímpeto` : a.custo ? `${a.custo} de ${a.recurso}` : "sem custo";
      const ic = a.item ? Icones.consumivel(a.icone, 24) : "";
      const tipo = a.basico ? '<i class="tipo">básico</i>' : a.ultimate ? '<i class="tipo ult">ultimate</i>' : "";
      let previsto = "";
      if (!a.motivo && a.previsoes) {
        const vs = Object.entries(a.previsoes);
        if (a.alvo === "inimigos") previsto = `${vs.map(([, p]) => p.normal).join(" + ")} em todos`;
        else if (vs.length) {
          const ns = vs.map(([, p]) => p.normal);
          previsto = Math.min(...ns) === Math.max(...ns) ? `${ns[0]} de dano` : `${Math.min(...ns)}–${Math.max(...ns)} de dano`;
        }
      }
      if (!a.motivo && a.cura) previsto = `cura ${a.cura}`;
      return `<button class="acao${a.motivo ? " nao" : ""}${a.item ? " item" : ""}${a.ultimate ? " ult" : ""}" data-i="${i}" ${a.motivo ? 'aria-disabled="true"' : ""}>` +
        `<span class="tecla">${i + 1}</span>${ic}<b>${esc(a.nome)}</b>${tipo}<span class="custo">${esc(custo)}</span>` +
        (previsto ? `<span class="previsto">${esc(previsto)}</span>` : "") +
        `<span class="desc">${esc(a.motivo || a.desc)}</span></button>`;
    }).join("");
    d.innerHTML = `<div class="quem">${retrato(o, 32)}<b>${esc(o.nome)}</b><span>${o.recurso} de ${esc(o.recurso_nome)}</span></div><div class="acoes">${botoes}</div>` +
      (aviso ? `<p class="aviso">${esc(aviso)}</p>` : "");
    d.querySelectorAll(".acao").forEach((b) => b.addEventListener("click", () => escolher(E.acoes[+b.dataset.i])));
  }

  function desenharRegistro() {
    const r = $("#registro");
    let html = "";
    E.eventos.forEach((ev, i) => {
      if (ev.tipo === "rodada") { html += `<h4>${esc(ev.texto)}</h4>`; return; }
      const novo = i >= vistos && vistos > 0;
      html += `<p class="ev ev-${ev.tipo}${novo ? " novo" : ""}" style="--i:${Math.max(0, i - vistos)}">${esc(ev.texto)}` +
        (ev.conta ? `<small>${esc(ev.conta)}</small>` : "") + "</p>";
    });
    r.innerHTML = html;
    r.scrollTop = r.scrollHeight;
  }

  function desenharFicha() {
    const o = E.aliados.find((x) => x.id === fichaDe);
    const seletor = E.aliados.map((a) => `<button data-ficha="${a.id}" class="${a.id === fichaDe ? "atual" : ""}">${esc(a.nome)}</button>`).join("");
    const atr = cat.atributos.map((a) => `<li><span>${esc(a.nome)}</span><b>${o.atributos[a.id]}</b></li>`).join("")
      + (o.id === "heroi" ? `<li class="fora"><span>Presença</span><b>${E.presenca}</b></li>` : "");
    const der = o.derivados.map((d) => `<li><span>${esc(d.nome)}</span><b>${esc(d.valor)}</b><small>${esc(d.como)}</small></li>`).join("");
    $("#ficha").innerHTML = `<div class="seletor">${seletor}</div>` +
      (o.id === "heroi" ? `<p class="nota">Construção: ${esc(E.build === "livre" ? "livre" : cat.builds.find((b) => b.id === E.build).nome)}. Presença não age na luta.</p>` : `<p class="nota">Atributos próprios do companheiro (não se distribuem aqui).</p>`) +
      `<h4>Atributos</h4><ul class="atributos">${atr}</ul><h4>O que eles dão agora</h4><ul class="derivados">${der}</ul>`;
    $("#ficha").querySelectorAll("[data-ficha]").forEach((b) => b.addEventListener("click", () => { fichaDe = b.dataset.ficha; desenharFicha(); }));
  }

  function desenharFim() {
    const f = $("#fim");
    f.hidden = !E.fim;
    if (!E.fim) return;
    const r = E.resumo, h = r.recurso.heroi;
    const basicos = (r.acoes.atacar || 0), total = Object.values(r.acoes).reduce((a, b) => a + b, 0);
    f.innerHTML = `<div class="m-janela"><h2>${E.fim === "vitoria" ? "Vitória" : "Derrota"}</h2><p>${E.fim === "vitoria" ? "Na" : "Até a"} rodada ${E.rodada}. ` +
      `Quedas: ${r.quedas}. Ameaças: ${r.preparos} anunciadas, ${r.preparos_desfeitos} desfeitas, ${r.preparos_aparados} aparadas, ${r.preparos_resolvidos - r.preparos_aparados} acertaram em cheio.</p>` +
      `<p>Ataques básicos: ${basicos} de ${total} ações do grupo. Vigor de Jean: gastou ${h.gasto}, recuperou ${h.turno} nos turnos e ${h.basico} atacando.</p>` +
      `<p>Dano recebido: ${E.aliados.map((a) => `${esc(a.nome)} ${r.dano_recebido[a.id]}`).join(" · ")}.</p>` +
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
    const r = await api("/api2/comparar", { equip: cfg.equip });
    const cols = r.colunas;
    const linha = (rot, vals, cls = "") => `<tr class="${new Set(vals.map(String)).size > 1 ? "difere" : ""} ${cls}"><th>${rot}</th>${vals.map((v) => `<td>${v}</td>`).join("")}</tr>`;
    const nomeD = (id) => cols[0].derivados.find((d) => d.id === id).nome;
    let html = linha("Proposta", cols.map((k) => esc(k.frase)), "texto") + linha("Ganha", cols.map((k) => esc(k.ganha)), "texto") + linha("Abre mão", cols.map((k) => esc(k.abre_mao)), "texto");
    html += cat.atributos.map((a) => linha(esc(a.nome), cols.map((k) => k.atributos[a.id]))).join("");
    html += ["vida", "iniciativa", "fisico", "sobrenatural", "critico", "ponto_fraco", "corporal", "tenacidade"].map((id) =>
      linha(esc(nomeD(id)) + (id === "iniciativa" ? " <small>(encontro 2)</small>" : ""), cols.map((k) => esc(k.derivados.find((d) => d.id === id).valor)))).join("");
    html += `<tr class="sep"><th colspan="${cols.length + 1}">Dano previsto no Bandido Bruto (proteção 2, ponto fraco): normal e crítico · <small>✓ no kit sugerido</small></th></tr>`;
    html += cols[0].dano_todos.map((d, j) => linha(esc(d.nome), cols.map((k) => { const x = k.dano_todos[j]; return `${x.normal} <small>/ ${x.critico}</small>${k.kit.includes(d.id) || d.id === "atacar" ? " ✓" : ""}`; }))).join("");
    html += linha("Kit sugerido", cols.map((k) => `${k.kit.map((x) => esc(nomeHab(x))).join(", ")} <small>(${k.pontos_kit} pts)</small>`), "texto");
    c.innerHTML = `<h2>Comparar construções</h2><p class="nota">O mesmo Jean: nível 3, ${esc(cat.equipamento.arma.find((o) => o.id === cfg.equip.arma).nome)}, ${esc(cat.equipamento.foco.find((o) => o.id === cfg.equip.foco).nome)}, proteção 3, os mesmos companheiros. Só os ${cat.orcamento} pontos (e o kit sugerido) mudam. Em destaque, o que difere.</p>` +
      `<div class="comparar"><table><thead><tr><th></th>${cols.map((k) => `<th>${esc(k.nome)}</th>`).join("")}</tr></thead><tbody>${html}</tbody></table></div>` +
      `<p class="nota">Presença não entra: fica fora do orçamento e só vale fora da luta.</p>`;
  }

  async function janelaSituacao(c, escolha, ajuda) {
    const s = await api("/api2/situacao", { atributos: cfg.atributos, presenca: cfg.presenca, escolha, ajuda });
    const ops = s.opcoes.map((o) => `<li><button class="botao" data-op="${o.id}">${esc(o.texto)}</button>` +
      `<span class="req ${o.valor >= o.minimo ? "ok" : "falta"}">${esc(o.atributo)} ${o.valor} (a situação pede ${o.minimo})</span>` +
      (o.ajuda ? `<button class="botao" data-op="${o.id}" data-ajuda="1">${esc(o.ajuda.texto)}</button>` : "") + "</li>").join("");
    c.innerHTML = `<h2>${esc(s.titulo)}</h2><p class="nota">Fora da luta, com a construção escolhida (${esc(nomeBuild())}, Presença ${cfg.presenca}). Os companheiros acrescentam, mas a escolha continua sendo de Jean.</p>` +
      `<p class="prosa">${esc(s.texto)}</p><ul class="opcoes">${ops}</ul>` +
      (s.resultado ? `<p class="resultado ${s.resultado.ok ? "ok" : "falta"}">${esc(s.resultado.texto)} <small>${esc(s.resultado.como)}</small></p>` : "");
    c.querySelectorAll("[data-op]").forEach((b) => b.addEventListener("click", () => janelaSituacao(c, b.dataset.op, !!b.dataset.ajuda)));
  }

  async function janelaResultados(c) {
    const r = await api("/api2/resultados");
    const linhas = r.resultados.map((x) => {
      const tot = Object.values(x.acoes).reduce((a, b) => a + b, 0), h = x.recurso.heroi;
      return `<tr><td>${esc(x.hora)}</td><td>${esc(x.nome)}</td><td>${esc(x.build === "livre" ? "Livre" : cat.builds.find((b) => b.id === x.build).nome)}<small>${x.kit_nomes.map(esc).join(", ")}</small></td><td>${esc(x.fim)}</td>` +
        `<td>${x.rodadas}</td><td>${x.quedas}</td><td>${x.acoes.atacar || 0} de ${tot}</td><td>${h.gasto} / ${h.turno} + ${h.basico}</td>` +
        `<td>${x.preparos} · ${x.preparos_desfeitos} · ${x.preparos_aparados} · ${x.preparos_resolvidos - x.preparos_aparados}</td><td>${x.controles.sofridos} / ${x.controles.resistidos}</td><td>${x.ultimate}</td>` +
        `<td>${Object.values(x.dano_recebido).join(" / ")}</td>` +
        `<td class="acoes-usadas">${Object.entries(x.acoes).sort((a, b) => b[1] - a[1]).map(([k, n]) => `${esc(k.startsWith("item:") ? k.slice(5) : nomeHab(k))} ${n}`).join(", ")}</td></tr>`;
    }).join("");
    c.innerHTML = `<h2>Resultados da sessão</h2><p class="nota">Cada luta terminada ou reiniciada. Guardados só nesta execução, em <code>${esc(r.pasta)}</code>.</p>` +
      (linhas ? `<table class="resultados"><thead><tr><th>Hora</th><th>Encontro</th><th>Build e kit</th><th>Fim</th><th>Rodadas</th><th>Quedas</th><th>Básicos</th><th>Vigor de Jean: gasto / turno + básico</th><th>Ameaças: anunc. · desfeitas · aparadas · em cheio</th><th>Controles sofridos / resistidos</th><th>Ultimate</th><th>Dano Jean / Odette / Morel</th><th>Ações</th></tr></thead><tbody>${linhas}</tbody></table>`
        : "<p>Nenhuma luta terminada ainda.</p>");
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
    cat = await api("/api2/catalogo");
    const g = guardado("cfg");
    const b0 = cat.builds[0];
    cfg = { build: b0.id, atributos: { ...b0.atributos }, kit: [...b0.kit], equip: { ...cat.equip_padrao }, presenca: cat.presenca };
    if (g && g.atributos && cat.atributos.every((a) => Number.isInteger(g.atributos[a.id])) && Array.isArray(g.kit)) cfg = { ...cfg, ...g, equip: { ...cfg.equip, ...(g.equip || {}) } };
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
    F = await api("/api2/ficha", corpoBuild());
    abrirPrep(true);
  }
  window.Demo = { get estado() { return E; }, get cfg() { return cfg; }, get ficha() { return F; }, agir, iniciar, abrir, abrirPrep };
  comecar();
})();
