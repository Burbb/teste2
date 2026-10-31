/* PROTÓTIPO X1 da etapa 8 (31/10/2026; nada no jogo). A tela só desenha: a validação da montagem, o que cada talento
   muda, as previsões de dano e as cadeias vêm prontas do motor (motor/), pelo servidor. */
(() => {
  "use strict";
  const $ = (s) => document.querySelector(s);
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const api = async (rota, corpo) => {
    const r = await fetch(rota, corpo === undefined ? {} : { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(corpo) });
    return r.json();
  };
  const guardar = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* sem armazenamento */ } };
  const ler = (k) => { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } };
  const pontos = (n) => `${n} ponto${n === 1 ? "" : "s"}`;

  let CAT = null, M = null, FICHA = null, ENC = "lobos", E = null, SEL = null, VER = null, TELA = "montar";

  const retrato = (o, lado = 32) => {
    let h = "";
    try { h = o.lado === "aliado" ? Icones.cabeca(o.retrato, lado) : Icones.criatura(o.retrato, lado); } catch (e) { h = ""; }
    return h || `<span class="sem-retrato">${esc(o.nome[0])}</span>`;
  };

  // ---------------------------------------------------------------- telas
  function mostrar(t) {
    TELA = t;
    for (const id of ["montar", "luta", "registro"]) $("#" + id).hidden = id !== t;
    for (const b of document.querySelectorAll("#abas button")) b.classList.toggle("atual", b.dataset.tela === t);
    if (t === "registro") desenharRegistro();
    if (t === "luta") desenharLuta();
  }

  // ---------------------------------------------------------------- montar
  async function atualizarMontagem() {
    guardar("x1-montagem", M);
    guardar("x1-encontro", ENC);
    FICHA = await api("/api/montagem", { montagem: M });
    desenharMontar();
  }

  function trocar(campo, valor) {
    if (M[campo] === valor) return;
    M = { ...M, [campo]: valor, nos: {}, nome: "Livre" };
    if (campo === "spec") M.kit = [];
    atualizarMontagem();
  }

  function desenharMontar() {
    const est = CAT.estruturas, spec = CAT.specs[M.spec];
    $("#estruturas").innerHTML = Object.entries(est).map(([k, v]) =>
      `<button data-est="${k}" class="${k === M.estrutura ? "atual" : ""}">${esc(v.nome)}</button>`).join("");
    $("#estrutura-frase").textContent = est[M.estrutura].frase;
    $("#specs").innerHTML = Object.entries(CAT.specs).map(([k, v]) =>
      `<button data-spec="${k}" class="${k === M.spec ? "atual" : ""}">${esc(v.nome)} <small>(${esc(v.classe)})</small></button>`).join("");
    const exs = CAT.exemplos.filter((x) => x.estrutura === M.estrutura && x.spec === M.spec);
    $("#exemplos").innerHTML = exs.map((x) =>
      `<button data-ex="${x.id}" title="${esc(x.frase)}">${esc(x.nome)} <small>· ${esc(x.estilo)}</small></button>`).join("") +
      `<button data-ex="" title="Kit e talentos vazios">Vazia</button>` +
      (exs.find((x) => x.nome === M.nome) ? `<p class="frase">${esc(exs.find((x) => x.nome === M.nome).frase)}</p>` : "");
    // o kit
    const cheio = M.kit.length >= CAT.espacos;
    $("#kit-titulo").innerHTML = `Kit · ${M.kit.length}/${CAT.espacos} <small>(e a ultimate: ${esc(spec.ultimate)})</small>`;
    $("#pool").innerHTML = FICHA.pool.map((h) =>
      `<button class="hab ${h.no_kit ? "no-kit" : ""} ${cheio ? "cheio" : ""}" data-hab="${h.id}" aria-pressed="${h.no_kit}">` +
      `<span class="marca">${h.no_kit ? "✓" : ""}</span><span class="nome">${esc(h.nome)}</span>` +
      `<span class="custo">${h.custo ? `${h.custo} de ${esc(spec.recurso)}` : "Grátis"}</span>` +
      `<div class="desc">${esc(h.desc)}</div></button>`).join("");
    // a árvore
    $("#arvore-titulo").innerHTML = `Talentos · ${FICHA.pontos}/${FICHA.orcamento} pontos <small>(${esc(est[M.estrutura].nome)})</small>`;
    const erros = FICHA.erros.filter((e) => !e.startsWith("Kit"));
    $("#erros").hidden = !erros.length;
    $("#erros").innerHTML = erros.map((e) => `<li>${esc(e)}</li>`).join("");
    $("#arvore").innerHTML = M.estrutura === "t4" ? arvoreHibrida() : arvoreVersoes();
    // a build
    const kit = FICHA.kit.length ? FICHA.kit : null;
    $("#kit-final").innerHTML = kit ? kit.map((h) =>
      `<div class="hab"><span class="nome">${esc(h.nome)}</span>${h.versao ? ` <span class="versao">· ${esc(h.versao)}</span>` : ""}` +
      `${h.ultimate ? ' <small>· Ultimate · 1 vez por luta</small>' : ""}` +
      `<span class="custo">${h.custo ? `${h.custo} de ${esc(spec.recurso)}` : "Grátis"}</span>` +
      `<div class="desc">${esc(h.desc)}</div>${h.notas.length ? `<ul>${h.notas.map((n) => `<li>${esc(n)}</li>`).join("")}</ul>` : ""}</div>`).join("")
      : `<p class="vazio">${esc(FICHA.erros.join(" · ") || "Escolha as habilidades.")}</p>`;
    $("#encontros").innerHTML = Object.entries(CAT.encontros).map(([k, v]) =>
      `<button class="enc ${k === ENC ? "atual" : ""}" data-enc="${k}"><span class="nome">${esc(v.nome)}</span>` +
      `<div class="resumo">${esc(v.resumo)}</div><div class="fav">Favorece: ${esc(v.favorece)} · Desfavorece: ${esc(v.desfavorece)}</div></button>`).join("");
    const pronto = FICHA.valida && M.kit.length === CAT.espacos;
    $("#lutar").disabled = !pronto;
    $("#lutar").title = pronto ? "" : (M.kit.length < CAT.espacos ? `Escolha ${CAT.espacos - M.kit.length} habilidade(s) a mais` : FICHA.erros.join("; "));
    $("#build-topo").textContent = `${M.nome} · ${CAT.specs[M.spec].nome} · ${est[M.estrutura].nome} · ${FICHA.pontos}/${FICHA.orcamento} pontos`;
  }

  function cartaNo(n) {
    const preco = n.ranks > 1 ? `${pontos(n.custo)} por nível · até ${n.ranks}` : pontos(n.custo);
    let motivo = "";
    if (!n.pode_mais && n.rank < n.ranks && n.motivo_mais) motivo = n.motivo_mais;
    if (n.rank && !n.pode_menos && n.motivo_menos) motivo = n.motivo_menos;
    const afeta = n.afeta.length ? `<div class="afeta">No seu kit: ${esc(n.afeta.join(", "))}</div>` : "";
    return `<div class="no ${n.rank ? "comprado" : ""}" data-no="${n.id}">` +
      `<div class="t"><span class="tipo ${n.tipo}">${esc(n.nome_tipo)}</span><span class="nome">${esc(n.nome)}</span></div>` +
      `<div class="texto">${esc(n.texto)}</div>${n.aviso ? `<div class="aviso">${esc(n.aviso)}</div>` : afeta}` +
      `<div class="controles"><button data-menos="${n.id}" ${n.pode_menos ? "" : "disabled"} aria-label="Tirar um ponto de ${esc(n.nome)}">−</button>` +
      `<span class="rank">${n.rank}/${n.ranks}</span><button data-mais="${n.id}" ${n.pode_mais ? "" : "disabled"} aria-label="Pôr um ponto em ${esc(n.nome)}">+</button>` +
      `<span class="preco">${preco}</span></div>${motivo ? `<div class="motivo">${esc(motivo)}</div>` : ""}</div>`;
  }

  function arvoreHibrida() {
    const arv = FICHA.arvore, req = CAT.requisito_linha;
    let html = "";
    for (const linha of [1, 2, 3]) {
      const nos = arv.filter((n) => n.linha === linha);
      const antes = arv.filter((n) => n.linha < linha).reduce((s, n) => s + n.custo * n.rank, 0);
      const r = req[linha];
      const rotulo = linha === 1 ? "Linha 1" : `Linha ${linha} · requer ${r} pontos ${linha === 2 ? "na linha 1" : "nas linhas 1 e 2"} (${antes}/${r})`;
      html += `<div class="linha-arvore"><h3 class="${antes < r ? "falta" : ""}">${rotulo}</h3><div class="nos">${nos.map(cartaNo).join("")}</div></div>`;
    }
    return html;
  }

  function arvoreVersoes() {
    const arv = FICHA.arvore;
    const princ = arv.filter((n) => n.tipo === "P");
    const porHab = {};
    for (const n of arv.filter((x) => x.tipo === "V")) (porHab[n.versao] ||= []).push(n);
    return `<div class="linha-arvore"><h3>Princípios · 3 pontos cada</h3><div class="nos">${princ.map(cartaNo).join("")}</div></div>` +
      `<div class="linha-arvore"><h3>Versões · 1 ponto · uma por habilidade</h3>${Object.entries(porHab).map(([h, nos]) =>
        `<div class="grupo-versoes"><h4>${esc(h)}</h4><div class="nos">${nos.map(cartaNo).join("")}</div></div>`).join("")}</div>`;
  }

  // ---------------------------------------------------------------- luta
  async function lutar(semente) {
    if ($("#lutar").disabled && semente === undefined) return;
    const s = semente !== undefined ? semente : ($("#semente").value === "" ? null : Number($("#semente").value));
    const r = await api("/api/luta", { montagem: M, encontro: ENC, semente: s });
    if (r.erro) { alert(r.erro); return; }
    E = r; SEL = null; VER = null;
    mostrar("luta");
  }

  async function agir(acao, alvo) {
    const r = await api("/api/agir", { acao, alvo, turno_id: E.turno_id });
    SEL = null; VER = null;
    if (r.estado) E = r.estado;
    if (!r.ok) console.warn(r.motivo);
    desenharLuta();
  }

  function escolher(a) {
    if (!a || !a.disponivel) return;
    if (a.alvo === "inimigos" || a.alvo === "proprio") return agir(a.id, null);
    if (a.alvos.length === 1) return agir(a.id, a.alvos[0]);
    SEL = SEL && SEL.id === a.id ? null : a;
    desenharLuta();
  }

  function chips(o) {
    const out = [];
    for (const [k, n] of Object.entries(o.fichas)) if (n) out.push(`<span class="chip ${k}" title="${esc(CAT.fichas[k].desc)}">${esc(CAT.fichas[k].nome)} ×${n}</span>`);
    for (const s of o.estados) out.push(`<span class="chip ${s.id}" title="${esc(s.dica)}">${esc(s.texto)}</span>`);
    if (o.calor !== null && o.calor !== undefined) out.push(`<span class="chip calor" title="Com 3, a próxima habilidade de fogo custa 0">Calor ${o.calor}/3</span>`);
    for (const [t, m] of Object.entries(o.res || {})) out.push(`<span class="chip" title="Dano de ${t} ×${m}">${m > 1 ? "Fraco" : "Resiste"} a ${esc(t)}</span>`);
    return out.join("");
  }

  function carta(o) {
    const alvo = SEL && SEL.alvos.includes(o.id);
    const prev = alvo && SEL.previsao && SEL.previsao[o.id];
    const pv = Math.max(0, o.vida) / o.vida_max * 100;
    return `<div class="carta ${o.vivo ? "" : "morto"} ${E.aguardando === o.id ? "vez" : ""} ${alvo ? "alvo" : ""}" data-alvo="${alvo ? o.id : ""}">` +
      `<span class="ret">${retrato(o)}</span><span class="nome">${esc(o.nome)}</span>` +
      (prev ? `<span class="previsto">${esc(prev)}<small>previsto</small></span>` : "<span></span>") +
      `<div><div class="barra"><i style="width:${pv}%"></i></div>` +
      (o.recurso_max ? `<div class="barra rec"><i style="width:${o.recurso / o.recurso_max * 100}%"></i></div>` : "") +
      `<span class="vals">Vida ${o.vida}/${o.vida_max}${o.recurso_max ? ` · ${esc(o.recurso_nome)} ${o.recurso}/${o.recurso_max}` : ""}</span></div>` +
      `<div class="chips">${chips(o)}</div></div>`;
  }

  function desenharLuta() {
    if (!E) { $("#luta-titulo").textContent = "Nenhuma luta. Monte a build e escolha Lutar."; return; }
    const est = CAT.estruturas[E.montagem.estrutura].nome, spec = CAT.specs[E.montagem.spec].nome;
    $("#luta-titulo").innerHTML = `<b>${esc(E.encontro_nome)}</b> · semente ${E.semente} · Rodada ${E.rodada} · ${esc(E.montagem.nome)} (${esc(spec)}, ${esc(est)})`;
    $("#ordem").innerHTML = E.ordem.map((x) =>
      `<span class="${x.lado} ${x.agiu ? "agiu" : ""} ${x.atual ? "atual" : ""} ${x.vivo ? "" : "morto"}">${esc(x.nome)}</span>`).join("");
    $("#grupo").innerHTML = E.combatentes.filter((o) => o.lado === "aliado").map(carta).join("");
    $("#frente").innerHTML = E.combatentes.filter((o) => o.lado === "inimigo").map(carta).join("");
    // a doca
    const quem = E.combatentes.find((o) => o.id === E.aguardando);
    if (quem && !E.fim) {
      const ver = VER || SEL;
      $("#doca").innerHTML = `<div class="quem">${retrato(quem)}<b>${esc(quem.nome)}</b>` +
        (SEL ? `<span>${esc(SEL.nome)}: escolha o alvo (clique na carta). <kbd>Esc</kbd> cancela.</span>` : "<span>Escolha a ação (ou o número).</span>") +
        (E.pode_sair_furia ? ` <button class="botao-x" id="sair-furia" title="Não gasta a ação">Sair da Fúria (+12 de Vigor e 1 Guarda) <kbd>F</kbd></button>` : "") +
        `</div><div class="acoes">${E.acoes.map((a, i) =>
          `<button class="acao ${a.ultimate ? "ult" : ""} ${SEL && SEL.id === a.id ? "escolhida" : ""}" data-acao="${a.id}" ${a.disponivel ? "" : "disabled"}>` +
          `<span class="n">${i + 1}. ${esc(a.nome)}</span>${a.versao ? `<span class="v">${esc(a.versao)}</span> ` : ""}` +
          `<span class="p">${esc(a.pagamento || "Grátis")}${a.ultimate ? " · 1 vez por luta" : ""}</span>${a.motivo ? `<span class="m">${esc(a.motivo)}</span>` : ""}</button>`).join("")}</div>` +
        `<div class="explica">${ver ? `<b>${esc(ver.nome)}</b>${ver.versao ? ` (${esc(ver.versao)})` : ""}: ${esc(ver.desc)}${ver.notas && ver.notas.length ? `<ul>${ver.notas.map((n) => `<li>${esc(n)}</li>`).join("")}</ul>` : ""}` : ""}</div>`;
    } else {
      $("#doca").innerHTML = E.fim ? "" : "<p class='nota'>Os inimigos agem.</p>";
    }
    desenharLog();
    desenharFim();
  }

  function desenharLog() {
    const log = $("#log");
    log.innerHTML = E.eventos.map((e) => {
      const inimigo = e.tipo === "acao" && e.ator && e.ator.includes("#");
      const cad = e.tipo === "gatilho" || e.tipo === "barrado" ? `<span class="cad" title="Cadeia ${e.cadeia}${e.elo ? `, elo ${e.elo}` : ""}">c${e.cadeia}${e.elo ? "·" + e.elo : ""}</span>` : "";
      return `<div class="ev t-${e.tipo} ${inimigo ? "inimigo" : ""}" style="margin-left:${(e.nivel || 0) * 14}px">${cad}${esc(e.texto)}</div>`;
    }).join("");
    log.scrollTop = log.scrollHeight;
  }

  function desenharFim() {
    const f = $("#fim");
    if (!E.fim) { f.hidden = true; return; }
    const r = E.resumo;
    const titulo = { vitoria: "Vitória", derrota: "Derrota", empate: "Empate" }[r.fim];
    const linhas = (obj) => Object.entries(obj).map(([k, v]) => `<tr><td>${esc(k)}</td><td>${esc(v)}</td></tr>`).join("");
    f.innerHTML = `<h2>${titulo}</h2><p>${r.rodadas} rodadas · dano recebido ${r.dano_recebido} · cura ${r.cura}</p>` +
      `<table>${linhas(r.vida_grupo)}</table>` +
      `<h3>Dano causado, por fonte</h3><table>${linhas(r.dano_por_causa)}</table>` +
      `<h3>Ações usadas</h3><table>${linhas(r.usos)}</table>` +
      (r.cadeias.length ? `<h3>Cadeias mais longas</h3><table>${r.cadeias.map((c) =>
        `<tr><td>c${c.n} · rodada ${c.rodada}</td><td>${esc(c.rotulo)}: ${c.elos} efeito${c.elos > 1 ? "s" : ""} disparado${c.elos > 1 ? "s" : ""}${c.barrados ? `, ${c.barrados} barrado${c.barrados > 1 ? "s" : ""} pela regra` : ""}</td></tr>`).join("")}</table>` : "") +
      `<div class="botoes"><button class="botao-x principal" id="repetir">Repetir (semente ${E.semente}) <kbd>R</kbd></button>` +
      `<button class="botao-x" id="outra">Outra semente</button><button class="botao-x" id="voltar">Voltar à montagem <kbd>M</kbd></button>` +
      `<button class="botao-x" id="ver-log">Fechar e ler o registro</button></div>`;
    f.hidden = false;
  }

  // ---------------------------------------------------------------- registro
  async function desenharRegistro() {
    const r = await api("/api/registro");
    $("#pasta").textContent = `Também gravado em ${r.pasta}\\registro.json (com cada decisão, o estado em que foi tomada e todos os eventos).`;
    const nomeEst = (k) => CAT.estruturas[k].nome, nomeSpec = (k) => CAT.specs[k].nome;
    $("#lutas").innerHTML = r.lutas.length ? `<table class="reg"><tr><th>#</th><th>Hora</th><th>Build</th><th>Encontro</th><th>Semente</th><th>Resultado</th><th>Rodadas</th><th>Vida no fim</th><th>Recebido</th><th>Cura</th><th>Maior cadeia</th><th>Ações mais usadas</th></tr>` +
      r.lutas.slice().reverse().map((x) => {
        const s = x.resumo, mc = s.cadeias[0];
        return `<tr><td>${x.n}</td><td>${x.hora}</td><td>${esc(x.montagem.nome)}<br><small>${esc(nomeSpec(x.montagem.spec))} · ${esc(nomeEst(x.montagem.estrutura))}</small></td>` +
          `<td>${esc(CAT.encontros[x.encontro] ? CAT.encontros[x.encontro].nome : x.encontro)}<br><small>${esc(x.inimigos.join(", "))}</small></td><td>${x.semente}</td>` +
          `<td class="${x.fim || ""}">${esc({ vitoria: "Vitória", derrota: "Derrota", empate: "Empate" }[x.fim] || "Abandonada")}</td><td>${s.rodadas}</td>` +
          `<td>${esc(Object.entries(s.vida_grupo).map(([k, v]) => `${k} ${v}`).join(" · "))}</td><td>${s.dano_recebido}</td><td>${s.cura}</td>` +
          `<td>${mc ? `${mc.elos} (${esc(mc.rotulo)})` : "—"}</td><td>${esc(Object.entries(s.usos).slice(0, 4).map(([k, v]) => `${k} ×${v}`).join("; "))}</td></tr>`;
      }).join("") + "</table>" : "<p class='nota'>Nenhuma luta ainda.</p>";
    $("#montagens").innerHTML = r.montagens.length ? `<table class="reg"><tr><th>Hora</th><th>Build</th><th>Kit</th><th>Talentos</th><th>Nota</th></tr>` +
      r.montagens.slice().reverse().map((x) => `<tr><td>${x.hora}</td><td>${esc(x.montagem.nome)}<br><small>${esc(nomeSpec(x.montagem.spec))} · ${esc(nomeEst(x.montagem.estrutura))}</small></td>` +
        `<td>${esc(x.montagem.kit.join(", "))}</td><td>${esc(Object.entries(x.montagem.nos).map(([k, v]) => v > 1 ? `${k} ×${v}` : k).join(", "))}</td><td>${esc(x.nota)}</td></tr>`).join("") + "</table>"
      : "<p class='nota'>Nenhuma montagem salva.</p>";
  }

  // ---------------------------------------------------------------- eventos
  document.addEventListener("click", (ev) => {
    const t = ev.target.closest("button, .carta, [data-alvo]");
    if (!t) return;
    const d = t.dataset;
    if (d.tela) return mostrar(d.tela);
    if (d.est) return trocar("estrutura", d.est);
    if (d.spec) return trocar("spec", d.spec);
    if (d.ex !== undefined) {
      const x = CAT.exemplos.find((e) => e.id === d.ex);
      M = x ? { estrutura: x.estrutura, spec: x.spec, kit: [...x.kit], nos: { ...x.nos }, nome: x.nome }
        : { ...M, kit: [], nos: {}, nome: "Livre" };
      return atualizarMontagem();
    }
    if (d.hab) {
      const kit = M.kit.includes(d.hab) ? M.kit.filter((h) => h !== d.hab) : (M.kit.length < CAT.espacos ? [...M.kit, d.hab] : M.kit);
      M = { ...M, kit, nome: M.nome.endsWith("(editada)") || M.nome === "Livre" ? M.nome : M.nome + " (editada)" };
      return atualizarMontagem();
    }
    if (d.mais || d.menos) {
      const id = d.mais || d.menos, nos = { ...M.nos };
      nos[id] = (nos[id] || 0) + (d.mais ? 1 : -1);
      if (nos[id] <= 0) delete nos[id];
      M = { ...M, nos, nome: M.nome.endsWith("(editada)") || M.nome === "Livre" ? M.nome : M.nome + " (editada)" };
      return atualizarMontagem();
    }
    if (d.enc) { ENC = d.enc; return atualizarMontagem(); }
    if (t.id === "zerar") { M = { ...M, nos: {}, nome: M.nome === "Livre" ? "Livre" : M.nome.replace(/ \(editada\)$/, "") + " (editada)" }; return atualizarMontagem(); }
    if (t.id === "lutar") return lutar();
    if (t.id === "salvar") {
      return api("/api/salvar", { montagem: M, nota: $("#nota").value }).then((r) => { $("#salvo").textContent = `Salva (${r.n}).`; $("#nota").value = ""; });
    }
    if (d.acao) return escolher(E.acoes.find((a) => a.id === d.acao));
    if (d.alvo && SEL) return agir(SEL.id, d.alvo);
    if (t.id === "sair-furia") return api("/api/sair_furia", {}).then((r) => { E = r.estado; desenharLuta(); });
    if (t.id === "repetir") return lutar(E.semente);
    if (t.id === "outra") return lutar(Math.floor(Math.random() * 100000));
    if (t.id === "voltar") return mostrar("montar");
    if (t.id === "ver-log") { $("#fim").hidden = true; return; }
  });
  document.addEventListener("mouseover", (ev) => {
    const b = ev.target.closest("[data-acao]");
    if (!b || !E) return;
    const a = E.acoes.find((x) => x.id === b.dataset.acao);
    if (a && a !== VER) { VER = a; const ex = document.querySelector("#doca .explica"); if (ex) ex.innerHTML = `<b>${esc(a.nome)}</b>${a.versao ? ` (${esc(a.versao)})` : ""}: ${esc(a.desc)}${a.notas.length ? `<ul>${a.notas.map((n) => `<li>${esc(n)}</li>`).join("")}</ul>` : ""}`; }
  });
  document.addEventListener("keydown", (ev) => {
    if (ev.target.matches("input, textarea")) return;
    const k = ev.key.toLowerCase();
    if (k === "m") return mostrar("montar");
    if (k === "l") return mostrar("luta");
    if (k === "g") return mostrar("registro");
    if (TELA === "montar" && ev.key === "Enter") return lutar();
    if (TELA !== "luta" || !E) return;
    if (ev.key === "Escape") { SEL = null; return desenharLuta(); }
    if (k === "r" && E.fim) return lutar(E.semente);
    if (k === "f" && E.pode_sair_furia) return api("/api/sair_furia", {}).then((r) => { E = r.estado; desenharLuta(); });
    const n = Number(ev.key);
    if (n >= 1 && n <= 9) {
      if (SEL) { const alvo = SEL.alvos[n - 1]; if (alvo) return agir(SEL.id, alvo); return; }
      return escolher(E.acoes[n - 1]);
    }
  });

  // ---------------------------------------------------------------- início
  (async () => {
    CAT = await api("/api/catalogo");
    $("#regras").innerHTML = CAT.regras.map((r) => `<li>${esc(r)}</li>`).join("");
    const salvo = ler("x1-montagem");
    M = salvo && CAT.specs[salvo.spec] && CAT.estruturas[salvo.estrutura] ? salvo
      : { estrutura: "t4", spec: "piromante", kit: [...CAT.exemplos[2].kit], nos: { ...CAT.exemplos[2].nos }, nome: CAT.exemplos[2].nome };
    const enc = ler("x1-encontro");
    if (enc && CAT.encontros[enc]) ENC = enc;
    await atualizarMontagem();
  })();
})();
