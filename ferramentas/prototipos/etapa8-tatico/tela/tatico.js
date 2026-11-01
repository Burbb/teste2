/* PROTÓTIPO tático da etapa 8 (nada no jogo). A tela só desenha: as casas alcançáveis, o alcance, os alvos, a visão e
   a área de cada ação vêm prontas do motor (motor/combate.py), pelo servidor. Cada comando leva o tempo desde o último
   desenho (ms), para o registro comparar o tempo de decidir onde andar com o de decidir o que fazer. */
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

  let CAT = null, PREP = null, E = null, SEL = null, HOVER = null, VER = null, TELA = "preparar", T0 = performance.now();

  const sigla = (u) => {
    if (u.invocacao) return "S";
    const p = u.nome.split(" ");
    const letra = p[p.length - 1].length === 1 ? p[p.length - 1] : "";
    return (u.lado === "aliado" ? u.nome[0] : u.nome.slice(0, 2)) + letra;
  };
  const retrato = (u, lado) => {
    let h = "";
    try { h = u.invocacao ? "" : (u.lado === "aliado" ? Icones.cabeca(u.retrato, lado) : Icones.criatura(u.retrato, lado)); } catch (e) { h = ""; }
    return h;
  };

  function mostrar(t) {
    TELA = t;
    for (const id of ["preparar", "luta", "registro"]) $("#" + id).hidden = id !== t;
    for (const b of document.querySelectorAll("#abas button")) b.classList.toggle("atual", b.dataset.tela === t);
    if (t === "registro") desenharRegistro();
    if (t === "luta") desenharLuta();
  }

  // ---------------------------------------------------------------- preparar
  function desenharPreparar() {
    guardar("tatico-prep", PREP);
    $("#specs").innerHTML = Object.entries(CAT.specs).map(([k, v]) =>
      `<button data-spec="${k}" class="${k === PREP.spec ? "atual" : ""}">${esc(v.nome)}</button>`).join("");
    $("#talentos").innerHTML = CAT.talentos[PREP.spec].map((par) =>
      `<div class="par"><h3>${esc(par.titulo)}</h3>` +
      `<label><input type="radio" name="${par.id}" value="" ${!PREP.talentos[par.id] ? "checked" : ""}> Nenhum</label>` +
      par.opcoes.map((o) => `<label><input type="radio" name="${par.id}" value="${o.id}" ${PREP.talentos[par.id] === o.id ? "checked" : ""}> <b>${esc(o.nome)}</b>: ${esc(o.texto)}</label>`).join("") +
      `</div>`).join("");
    if (!$("#encontro").options.length) {
      $("#encontro").innerHTML = Object.entries(CAT.encontros).map(([k, v]) => `<option value="${k}">${esc(v.nome)}</option>`).join("");
    }
    $("#encontro").value = PREP.encontro;
    const en = CAT.encontros[PREP.encontro];
    $("#encontro-desc").innerHTML = `${esc(en.objetivo)}<br><small>Inimigos: ${esc(en.inimigos.join(", "))}. No X1 de cards: o encontro equivalente.</small>`;
    $("#zona").checked = !!PREP.zona;
    $("#mover-depois").checked = !!PREP.mover_depois;
    const spec = CAT.specs[PREP.spec];
    const escolhidos = Object.values(PREP.talentos).filter(Boolean);
    const notas = (hid) => CAT.talentos[PREP.spec].flatMap((p) => p.opcoes).filter((o) => escolhidos.includes(o.id) && (o.afeta || []).includes(hid));
    $("#kit").innerHTML = `<p class="nota">${esc(spec.pm)} PM por vez; ${esc(spec.recurso)} como recurso. Também Atacar (corpo a corpo) e Defender.</p>` +
      spec.kit.map((h) => `<div class="hab"><span class="n">${esc(h.nome)}</span><span class="c">${h.custo} de ${esc(spec.recurso)}</span>` +
        `<div class="a">${esc(h.alcance)}</div><div class="d">${esc(h.desc)}</div>` +
        notas(h.id).map((o) => `<div class="d" style="color:var(--bom)">${esc(o.nome)}: ${esc(o.texto)}</div>`).join("") +
        `<div class="f">Função: ${esc(h.funcao)}</div></div>`).join("");
    $("#companheiros").innerHTML = Object.values(CAT.companheiros).map((c) =>
      `<div class="hab"><span class="n">${esc(c.nome)}</span>${c.kit.map((h) => `<div class="d"><b>${esc(h.nome)}</b> (${esc(h.alcance)}): ${esc(h.desc)}</div>`).join("")}</div>`).join("");
    $("#resumo-topo").textContent = `${spec.nome}${escolhidos.length ? " · " + escolhidos.map((t) => CAT.talentos[PREP.spec].flatMap((p) => p.opcoes).find((o) => o.id === t).nome).join(", ") : ""}`;
  }

  async function lutar(semente) {
    const s = semente !== undefined ? semente : ($("#semente").value === "" ? null : Number($("#semente").value));
    const r = await api("/api/luta", { spec: PREP.spec, talentos: Object.values(PREP.talentos), encontro: PREP.encontro,
      semente: s, zona: PREP.zona ? 1 : 0, mover_depois: !!PREP.mover_depois });
    if (r.erro) { alert(r.erro); return; }
    E = r; SEL = null; HOVER = null; VER = null;
    mostrar("luta");
  }

  // ---------------------------------------------------------------- luta
  const ms = () => Math.round(performance.now() - T0);
  async function comando(rota, corpo) {
    const r = await api(rota, { ...corpo, ms: ms(), turno_id: E.turno_id });
    if (r.estado) E = r.estado;
    if (!r.ok) console.warn(r.motivo);
    SEL = null; HOVER = null;
    desenharLuta();
  }

  function selecionar(a) {
    if (!a || !a.disponivel) return;
    if (a.alvo === "proprio" && a.alvos.length === 1) { SEL = a; HOVER = a.alvos[0]; desenharLuta(); return; }
    SEL = SEL && SEL.id === a.id ? null : a;
    HOVER = null;
    desenharLuta();
  }

  function desenharGrade() {
    const A = E.arena, rochas = new Set(A.rochas), agua = new Set(A.agua);
    const porCasa = Object.fromEntries(E.unidades.map((u) => [u.pos, u]));
    const mov = !SEL && E.aguardando && !E.fim ? E.movimento : {};
    const rota = !SEL && HOVER && mov[HOVER] ? new Set(mov[HOVER].rota) : new Set();
    const alc = SEL ? new Set(SEL.alcance) : new Set(), alvos = SEL ? new Set(SEL.alvos) : new Set(), semv = SEL ? new Set(SEL.sem_visao) : new Set();
    const prev = SEL && HOVER && SEL.previas[HOVER];
    const area = prev ? new Set(prev.casas) : new Set();
    let html = "";
    for (let y = 0; y < A.altura; y++) {
      for (let x = 0; x < A.largura; x++) {
        const c = `${x},${y}`, u = porCasa[c];
        const cl = ["casa"];
        if (rochas.has(c)) cl.push("rocha");
        if (agua.has(c)) cl.push("agua");
        if (c in A.chamas) cl.push("chamas");
        if (A.marcadas[c]) cl.push("marcada");
        if (c in mov) cl.push("mov");
        if (rota.has(c)) cl.push("rota");
        if (alc.has(c)) cl.push("alcance");
        if (semv.has(c)) cl.push("semvisao");
        if (alvos.has(c)) cl.push("alvo");
        if (area.has(c)) cl.push("area");
        if (prev && u && prev.aliados.includes(u.id)) cl.push("area-aliado");
        const chamas = c in A.chamas ? (A.chamas[c] === null ? "∞" : `${A.chamas[c] - E.rodada + 1}`) : "";
        let ficha = "";
        if (u) {
          const r = retrato(u, 32);
          const marcas = [u.estados.find((s) => s.id === "queimadura") ? "🔥" + u.estados.find((s) => s.id === "queimadura").texto.split(" ")[1] : "",
            u.estados.some((s) => s.id === "prep") ? "!" : "", u.estados.some((s) => s.id === "atordoado") ? "z" : ""].join(" ").trim();
          ficha = `<div class="ficha ${u.lado} ${u.id === "heroi" ? "heroi" : ""} ${u.invocacao ? "invocacao" : ""} ${u.id === E.aguardando ? "vez" : ""}" title="${esc(dicaUnidade(u))}">` +
            (r ? `<span class="ret">${r}</span>` : "") + `<span class="sigla">${esc(sigla(u))}</span>` +
            (marcas ? `<span class="marcas">${esc(marcas)}</span>` : "") +
            `<span class="pv"><i style="width:${100 * u.vida / u.vida_max}%"></i></span></div>`;
          if (prev && prev.dano[u.id] !== undefined) ficha += `<span class="dano-prev ${u.lado === "aliado" ? "aliado" : ""}">−${prev.dano[u.id]}</span>`;
        }
        const titulo = [rochas.has(c) ? "Rocha: bloqueia passagem e visão" : "", agua.has(c) ? "Água: bloqueia passagem, deixa ver" : "",
          chamas ? `Chamas no chão (${chamas === "∞" ? "até o fim" : chamas + " rodada(s)"})` : "", A.marcadas[c] ? `Marcada: Golpe Esmagador de ${A.marcadas[c]}` : "",
          c in mov ? `Andar até aqui: ${mov[c].custo} PM` : "", semv.has(c) ? "No alcance, sem visão" : ""].filter(Boolean).join(" · ");
        html += `<div class="${cl.join(" ")}" data-casa="${c}" data-custo="${c in mov ? mov[c].custo : ""}" data-chamas="${chamas}" title="${esc(titulo)}">${ficha}</div>`;
      }
    }
    $("#grade").innerHTML = html;
    $("#legenda").textContent = SEL
      ? `${SEL.nome}: azul é o alcance (${SEL.alcance_txt}); contorno claro, os alvos válidos; hachura cinza, sem visão. Passe o mouse num alvo para ver a área.`
      : "Verde: onde dá para parar (o número é o custo em PM). Laranja: chamas no chão. Listras vermelhas: casas marcadas por um golpe preparado.";
  }

  function dicaUnidade(u) {
    const f = Object.entries(u.fichas).filter(([, n]) => n).map(([k, n]) => `${k} ×${n}`);
    return `${u.nome} · Vida ${u.vida}/${u.vida_max}${u.recurso_max ? ` · ${u.recurso_nome} ${u.recurso}/${u.recurso_max}` : ""} · ${u.pm_max} PM` +
      (u.estados.length ? " · " + u.estados.map((s) => s.texto).join(", ") : "") + (f.length ? " · " + f.join(", ") : "");
  }

  function explica(a) {
    if (!a) return "";
    return `<b>${esc(a.nome)}</b> · ${esc(a.alcance_txt)} · ${esc(a.pagamento)}<br>${esc(a.desc)}` +
      (a.notas && a.notas.length ? `<ul>${a.notas.map((n) => `<li>${esc(n)}</li>`).join("")}</ul>` : "");
  }

  function desenharLuta() {
    if (!E) { $("#luta-titulo").textContent = "Nenhuma luta. Prepare e escolha Lutar."; return; }
    $("#luta-titulo").innerHTML = `<b>${esc(E.encontro_nome)}</b> · semente ${E.semente} · Rodada ${E.rodada} · zona de controle ${E.zona ? "ligada" : "desligada"} · ${E.mover_depois ? "anda depois de agir" : "agir encerra o movimento"}`;
    $("#ordem").innerHTML = E.ordem.map((x) => `<span class="${x.lado} ${x.agiu ? "agiu" : ""} ${x.atual ? "atual" : ""} ${x.vivo ? "" : "morto"}">${esc(x.nome)}</span>`).join("");
    desenharGrade();
    const u = E.unidades.find((x) => x.id === E.aguardando);
    if (u && !E.fim) {
      $("#vez").innerHTML = `<div class="quem">${retrato(u, 32)}<b>${esc(u.nome)}</b><span class="vals">Vida ${u.vida}/${u.vida_max} · ${esc(u.recurso_nome || "")} ${u.recurso}/${u.recurso_max} · <b>${u.pm}</b> PM · ação ${u.acao_usada ? "usada" : "livre"}</span></div>` +
        `<p class="dica">${SEL ? `${esc(SEL.nome)}: clique num alvo. <kbd>Esc</kbd> cancela.` : "Clique numa casa verde para andar, ou escolha a ação."}</p>`;
      $("#acoes").innerHTML = E.acoes.map((a, i) =>
        `<button class="acao ${SEL && SEL.id === a.id ? "escolhida" : ""}" data-acao="${a.id}" ${a.disponivel ? "" : "disabled"} title="${esc(a.motivo || a.alcance_txt)}">` +
        `<span class="n">${i + 1}. ${esc(a.nome)}</span><span class="p">${esc(a.pagamento)} · ${esc(a.alcance_txt)}</span>${a.motivo ? `<span class="m">${esc(a.motivo)}</span>` : ""}</button>`).join("") +
        `<button class="acao encerrar" id="encerrar">Encerrar a vez <kbd>E</kbd></button>`;
      $("#explica").innerHTML = explica(VER || SEL);
    } else {
      $("#vez").innerHTML = E.fim ? "" : "<p class='nota'>Os inimigos agem.</p>";
      $("#acoes").innerHTML = "";
      $("#explica").innerHTML = "";
    }
    desenharLog();
    desenharFim();
    T0 = performance.now();
  }

  function desenharLog() {
    const log = $("#log");
    log.innerHTML = E.eventos.map((e) => {
      const inimigo = e.ator && e.ator.includes("#") && !e.ator.startsWith("sentinela");
      return `<div class="ev t-${e.tipo} ${inimigo ? "inimigo" : ""}" style="margin-left:${(e.nivel || 0) * 12}px">${esc(e.texto)}</div>`;
    }).join("");
    log.scrollTop = log.scrollHeight;
  }

  function desenharFim() {
    const f = $("#fim");
    if (!E.fim) { f.hidden = true; return; }
    const r = E.resumo, m = r.metricas;
    const titulo = { vitoria: "Vitória", derrota: "Derrota", empate: "Empate" }[r.fim];
    const linha = (k, v) => `<tr><td>${esc(k)}</td><td>${esc(v)}</td></tr>`;
    const seg = (v) => `${(v / 1000).toFixed(1)} s`;
    f.innerHTML = `<h2>${titulo}</h2><table>` +
      Object.entries(r.vida_grupo).map(([k, v]) => linha(k, v)).join("") +
      linha("Rodadas", r.rodadas) + linha("Comandos (andar, agir, encerrar)", `${r.comandos} · ${r.comandos_por_vez} por vez`) +
      linha("Casas andadas pelo grupo", m.casas_grupo) + linha("PM usados / disponíveis", `${m.pm_grupo} / ${m.pm_grupo_disp}`) +
      linha("Vezes sem andar", `${m.vezes_sem_mover} de ${m.vezes_grupo}`) + linha("PM pagos à zona de controle", m.zona_paga) +
      linha("Tempo decidindo onde andar", seg(m.ms_mover)) + linha("Tempo decidindo a ação", seg(m.ms_acao)) +
      linha("Tempo até encerrar", seg(m.ms_encerrar)) + linha("Colisões e empurrões", `${m.colisoes} colisões · ${m.empurroes} casas empurradas`) +
      linha("Áreas que pegaram aliados", m.areas_em_aliados) + linha("Inimigos sem ação na vez", `${m.inimigo_sem_acao} de ${m.vezes_inimigo}`) +
      `</table><div class="botoes"><button class="botao-x principal" id="repetir">Repetir (semente ${E.semente}) <kbd>R</kbd></button>` +
      `<button class="botao-x" id="outra">Outra semente</button><button class="botao-x" id="voltar">Voltar a Preparar <kbd>P</kbd></button>` +
      `<button class="botao-x" id="ver-log">Fechar e ler o registro</button></div>`;
    f.hidden = false;
  }

  async function desenharRegistro() {
    const r = await api("/api/registro");
    $("#pasta").textContent = `Também gravado em ${r.pasta}\\registro.json (cada comando, com a casa, o custo e o tempo, e todos os eventos).`;
    $("#lutas").innerHTML = r.lutas.length ? `<table class="reg"><tr><th>#</th><th>Hora</th><th>Build</th><th>Encontro</th><th>Regras</th><th>Semente</th><th>Resultado</th><th>Rodadas</th><th>Cmd/vez</th><th>Casas</th><th>Andar / agir</th><th>Inimigos sem ação</th></tr>` +
      r.lutas.slice().reverse().map((x) => {
        const m = x.resumo.metricas;
        return `<tr><td>${x.n}</td><td>${x.hora}</td><td>${esc(CAT.specs[x.spec].nome)}<br><small>${esc(x.talentos.join(", ") || "sem talentos")}</small></td>` +
          `<td>${esc(CAT.encontros[x.encontro].nome)}</td><td>${x.zona ? "zona" : "sem zona"} · ${x.mover_depois ? "anda depois" : "agir encerra"}</td><td>${x.semente}</td>` +
          `<td class="${x.fim || ""}">${esc({ vitoria: "Vitória", derrota: "Derrota", empate: "Empate" }[x.fim] || "Abandonada")}</td><td>${x.resumo.rodadas}</td>` +
          `<td>${x.resumo.comandos_por_vez}</td><td>${m.casas_grupo}</td><td>${(m.ms_mover / 1000).toFixed(0)} s / ${(m.ms_acao / 1000).toFixed(0)} s</td><td>${m.inimigo_sem_acao}/${m.vezes_inimigo}</td></tr>`;
      }).join("") + "</table>" : "<p class='nota'>Nenhuma luta ainda.</p>";
  }

  // ---------------------------------------------------------------- eventos
  document.addEventListener("click", (ev) => {
    const t = ev.target.closest("button, .casa");
    if (!t) return;
    const d = t.dataset;
    if (d.tela) return mostrar(d.tela);
    if (d.spec) { PREP = { ...PREP, spec: d.spec, talentos: {} }; return desenharPreparar(); }
    if (t.id === "lutar") return lutar();
    if (d.acao) return selecionar(E.acoes.find((a) => a.id === d.acao));
    if (t.id === "encerrar") return comando("/api/encerrar", {});
    if (d.casa && E && !E.fim && E.aguardando) {
      if (SEL) {
        if (SEL.alvos.includes(d.casa)) return comando("/api/agir", { acao: SEL.id, casa: d.casa });
        SEL = null; HOVER = null; return desenharLuta();
      }
      if (d.casa in E.movimento) return comando("/api/mover", { casa: d.casa });
    }
    if (t.id === "repetir") return lutar(E.semente);
    if (t.id === "outra") return lutar(Math.floor(Math.random() * 100000));
    if (t.id === "voltar") return mostrar("preparar");
    if (t.id === "ver-log") { $("#fim").hidden = true; }
  });
  document.addEventListener("contextmenu", (ev) => { if (TELA === "luta" && SEL) { ev.preventDefault(); SEL = null; HOVER = null; desenharLuta(); } });
  document.addEventListener("change", (ev) => {
    const t = ev.target;
    if (t.type === "radio") { PREP.talentos = { ...PREP.talentos, [t.name]: t.value }; desenharPreparar(); }
    if (t.id === "encontro") { PREP.encontro = t.value; desenharPreparar(); }
    if (t.id === "zona") { PREP.zona = t.checked; desenharPreparar(); }
    if (t.id === "mover-depois") { PREP.mover_depois = t.checked; desenharPreparar(); }
  });
  document.addEventListener("mouseover", (ev) => {
    if (TELA !== "luta" || !E) return;
    const c = ev.target.closest(".casa");
    const novo = c ? c.dataset.casa : null;
    if (novo !== HOVER && !(SEL && SEL.alvo === "proprio")) { HOVER = novo; desenharGrade(); }
    const b = ev.target.closest("[data-acao]");
    if (b) { const a = E.acoes.find((x) => x.id === b.dataset.acao); if (a && a !== VER) { VER = a; $("#explica").innerHTML = explica(a); } }
  });
  document.addEventListener("keydown", (ev) => {
    if (ev.target.matches("input, select")) return;
    const k = ev.key.toLowerCase();
    if (k === "p") return mostrar("preparar");
    if (k === "l") return mostrar("luta");
    if (k === "g") return mostrar("registro");
    if (TELA === "preparar" && ev.key === "Enter") return lutar();
    if (TELA !== "luta" || !E) return;
    if (ev.key === "Escape") { SEL = null; HOVER = null; return desenharLuta(); }
    if (k === "r" && E.fim) return lutar(E.semente);
    if (k === "e" && E.aguardando && !E.fim) return comando("/api/encerrar", {});
    if (k === "enter" && SEL && HOVER && SEL.alvos.includes(HOVER)) return comando("/api/agir", { acao: SEL.id, casa: HOVER });
    const n = Number(ev.key);
    if (n >= 1 && n <= 9 && E.acoes[n - 1]) return selecionar(E.acoes[n - 1]);
  });

  // ---------------------------------------------------------------- início
  (async () => {
    CAT = await api("/api/catalogo");
    $("#versao").textContent = CAT.versao;
    document.title = `Etapa 8 · Protótipo tático · ${CAT.versao}`;
    const salvo = ler("tatico-prep");
    PREP = salvo && CAT.specs[salvo.spec] && CAT.encontros[salvo.encontro] ? salvo
      : { spec: "piromante", talentos: {}, encontro: "aberto", zona: !!CAT.regras.zona, mover_depois: !!CAT.regras.mover_depois };
    desenharPreparar();
  })();
})();
