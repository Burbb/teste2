/* PROTÓTIPO X1 da etapa 8 (31/10/2026; nada no jogo). A tela só desenha: a validação da montagem, o que cada talento
   muda, a descrição efetiva das habilidades, as previsões de dano e as cadeias vêm prontas do motor (motor/), pelo
   servidor. As montagens salvas ficam no navegador (localStorage) e vão também para o registro do servidor. */
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
  let FILTRO = { funcao: "", prop: "", kit: false };
  let SALVAS = ler("x1-salvas") || [];

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
    M.ultimate = FICHA.montagem.ultimate;
    desenharMontar();
  }

  const editada = (nome) => (nome.endsWith("(editada)") || nome === "Livre" ? nome : nome + " (editada)");

  function trocar(campo, valor) {
    if (M[campo] === valor) return;
    M = { ...M, [campo]: valor, nos: {}, nome: "Livre", salva: null };
    if (campo === "spec") { M.kit = []; M.ultimate = null; }
    atualizarMontagem();
  }

  function passa(item) {
    if (FILTRO.funcao && !(item.funcao || []).includes(FILTRO.funcao)) return false;
    if (FILTRO.prop && !(item.props || []).includes(FILTRO.prop)) return false;
    return true;
  }

  function desenharMontar() {
    const est = CAT.estruturas;
    $("#estruturas").innerHTML = Object.entries(est).map(([k, v]) =>
      `<button data-est="${k}" class="${k === M.estrutura ? "atual" : ""}">${esc(v.nome)}</button>`).join("");
    $("#estrutura-frase").textContent = est[M.estrutura].frase;
    $("#specs").innerHTML = Object.entries(CAT.specs).map(([k, v]) =>
      `<button data-spec="${k}" class="${k === M.spec ? "atual" : ""}">${esc(v.nome)} <small>(${esc(v.classe)})</small></button>`).join("");
    if (document.activeElement !== $("#nome")) $("#nome").value = M.nome;
    desenharSalvas();
    const exs = CAT.exemplos.filter((x) => x.estrutura === M.estrutura && x.spec === M.spec);
    $("#exemplos").innerHTML = exs.map((x) =>
      `<button data-ex="${x.id}" title="${esc(x.frase)}">${esc(x.nome)} <small>· ${esc(x.estilo)}</small></button>`).join("") +
      `<button data-ex="" title="Kit e talentos vazios">Vazia</button>`;
    // o encontro
    if (!$("#encontro").options.length) {
      $("#encontro").innerHTML = Object.entries(CAT.encontros).map(([k, v]) => `<option value="${k}">${esc(v.nome)}</option>`).join("");
    }
    $("#encontro").value = ENC;
    const en = CAT.encontros[ENC];
    $("#encontro-desc").innerHTML = `${esc(en.resumo)}<br><small>Favorece: ${esc(en.favorece)} · Desfavorece: ${esc(en.desfavorece)}</small>`;
    const pronto = FICHA.valida && M.kit.length === CAT.espacos;
    $("#lutar").disabled = !pronto;
    $("#lutar").title = pronto ? "" : (M.kit.length < CAT.espacos ? `Escolha ${CAT.espacos - M.kit.length} habilidade(s) a mais` : FICHA.erros.join("; "));
    desenharRepertorio();
    desenharArvore();
    $("#build-topo").textContent = `${M.nome} · ${CAT.specs[M.spec].nome} · ${est[M.estrutura].nome} · ${FICHA.pontos}/${FICHA.orcamento} pontos · kit ${M.kit.length}/${CAT.espacos}`;
  }

  function desenharFiltros() {
    const chip = (tipo, v, rotulo) => `<button class="chip-f ${FILTRO[tipo] === v ? "atual" : ""}" data-filtro="${tipo}" data-valor="${esc(v)}">${esc(rotulo)}</button>`;
    $("#filtros").innerHTML =
      `<div class="linha-f"><span>Função</span>${chip("funcao", "", "Todas")}${CAT.funcoes.map((f) => chip("funcao", f, f)).join("")}</div>` +
      `<div class="linha-f"><span>Propriedade</span>${chip("prop", "", "Todas")}${CAT.propriedades.map((p) => chip("prop", p, p)).join("")}</div>` +
      `<div class="linha-f"><label><input type="checkbox" id="so-kit" ${FILTRO.kit ? "checked" : ""}> Só o que está no kit</label>` +
      `<span class="nota">A propriedade filtra também os talentos.</span></div>`;
  }

  function cartaHabilidade(h, ult) {
    const cheio = !h.no_kit && !ult && M.kit.length >= CAT.espacos;
    const recurso = CAT.specs[M.spec].recurso;
    const origem = h.origem === "classe" ? FICHA.classe : FICHA.spec_nome;
    return `<button class="hab ${h.no_kit ? "no-kit" : ""} ${cheio ? "cheio" : ""} ${ult ? "ult" : ""}" data-${ult ? "ult" : "hab"}="${h.id}" data-hab-id="${h.id}" aria-pressed="${h.no_kit}">` +
      `<span class="marca">${h.no_kit ? "✓" : ""}</span><span class="nome">${esc(h.nome)}</span>${h.versao ? ` <span class="versao">· ${esc(h.versao)}</span>` : ""}` +
      `<span class="custo">${h.custo ? `${h.custo} de ${esc(recurso)}` : "Grátis"}</span>` +
      `<div class="meta">${esc(origem)}${ult ? " · Ultimate · 1 vez por luta" : ""}${h.funcao.length ? " · " + esc(h.funcao.join(", ")) : ""}</div>` +
      `<div class="desc">${esc(h.desc)}</div>${h.notas.length ? `<ul>${h.notas.map((n) => `<li>${esc(n)}</li>`).join("")}</ul>` : ""}</button>`;
  }

  function desenharRepertorio() {
    desenharFiltros();
    const rep = FICHA.repertorio, ults = CAT.specs[M.spec].ultimates;
    $("#kit-titulo").innerHTML = `Repertório de ${esc(FICHA.spec_nome)} · kit ${M.kit.length}/${CAT.espacos} <small>(14 habilidades e 2 ultimates; leve 5 e 1 ultimate)</small>`;
    const kit = rep.filter((h) => h.no_kit);
    $("#kit-faixa").innerHTML = `<span>No kit:</span> ${kit.map((h) => `<b data-hab-id="${h.id}">${esc(h.nome)}${h.versao ? ` (${esc(h.versao)})` : ""}</b>`).join(" · ") || "<i>nada</i>"}`;
    const normais = rep.filter((h) => !ults.includes(h.id) && passa(h) && (!FILTRO.kit || h.no_kit));
    const finais = rep.filter((h) => ults.includes(h.id) && passa(h) && (!FILTRO.kit || h.no_kit));
    $("#pool").innerHTML = `<div class="grade-hab">${normais.map((h) => cartaHabilidade(h, false)).join("")}</div>` +
      (finais.length ? `<h3 class="sub">Ultimate (escolha uma)</h3><div class="grade-hab">${finais.map((h) => cartaHabilidade(h, true)).join("")}</div>` : "") +
      (!normais.length && !finais.length ? "<p class='nota'>Nada com esse filtro.</p>" : "");
  }

  function cartaNo(n) {
    const preco = n.ranks > 1 ? `${pontos(n.custo)} por nível · até ${n.ranks}` : pontos(n.custo);
    const motivo = !n.pode_mais && n.rank < n.ranks && n.motivo_mais ? n.motivo_mais : "";
    const alc = n.alcance.length || n.outros.length
      ? `<div class="afeta">Afeta: ${n.alcance.map((h) => h.no_kit ? `<b>${esc(h.nome)}</b>` : `<span class="fora">${esc(h.nome)}</span>`).join(", ")}${n.outros.length ? (n.alcance.length ? "; " : "") + esc(n.outros.join("; ")) : ""}</div>` : "";
    return `<div class="no ${n.rank ? "comprado" : ""}" data-no="${n.id}" data-afeta="${esc(n.alcance.map((h) => h.id).join(" "))}">` +
      `<div class="t"><span class="tipo ${n.tipo}">${esc(n.nome_tipo)}</span><span class="nome">${esc(n.nome)}</span></div>` +
      `<div class="texto">${esc(n.texto)}</div>${alc}${n.aviso ? `<div class="aviso">${esc(n.aviso)}</div>` : ""}` +
      (M.estrutura === "t1" && n.equivale && n.tipo !== "N" ? `<div class="equivale">Na híbrida: ${esc(n.equivale)}</div>` : "") +
      `<div class="controles"><button data-menos="${n.id}" ${n.pode_menos ? "" : "disabled"} aria-label="Tirar um ponto de ${esc(n.nome)}">−</button>` +
      `<span class="rank">${n.rank}/${n.ranks}</span><button data-mais="${n.id}" ${n.pode_mais ? "" : "disabled"} aria-label="Pôr um ponto em ${esc(n.nome)}">+</button>` +
      `<span class="preco">${preco}</span></div>${motivo ? `<div class="motivo">${esc(motivo)}</div>` : ""}</div>`;
  }

  function desenharArvore() {
    const est = CAT.estruturas;
    $("#arvore-titulo").innerHTML = `Talentos · ${FICHA.pontos}/${FICHA.orcamento} pontos <small>(${esc(est[M.estrutura].nome)})</small>`;
    const erros = FICHA.erros.filter((e) => !e.startsWith("Kit"));
    $("#erros").hidden = !erros.length;
    $("#erros").innerHTML = erros.map((e) => `<li>${esc(e)}</li>`).join("");
    const arv = FICHA.arvore.filter((n) => !FILTRO.prop || n.props.includes(FILTRO.prop) || n.rank);
    const grupo = (titulo, nos) => (nos.length ? `<div class="linha-arvore"><h3>${titulo}</h3><div class="nos">${nos.map(cartaNo).join("")}</div></div>` : "");
    let html;
    if (M.estrutura === "t4") {
      html = grupo("Regras · 2 pontos · valem para todas as habilidades com a propriedade", arv.filter((n) => n.tipo === "R")) +
        grupo("Versões · 1 ponto · mudam o papel de uma habilidade", arv.filter((n) => n.tipo === "V")) +
        grupo("Números · 1 ponto por nível", arv.filter((n) => n.tipo === "N"));
    } else {
      html = grupo("Princípios · 3 pontos · dois efeitos juntos", arv.filter((n) => n.tipo === "P")) +
        grupo("Versões · 1 ponto · uma por habilidade", arv.filter((n) => n.tipo === "V")) +
        grupo("Números · 1 ponto por nível", arv.filter((n) => n.tipo === "N"));
    }
    $("#arvore").innerHTML = (FILTRO.prop ? `<p class="nota">Mostrando os talentos com ${esc(FILTRO.prop)} (e os já comprados).</p>` : "") + html;
  }

  function desenharSalvas() {
    const minhas = SALVAS.filter((s) => s.montagem.spec === M.spec && s.montagem.estrutura === M.estrutura);
    const outras = SALVAS.length - minhas.length;
    $("#salvas").innerHTML = (minhas.length ? `<ul class="salvas">${minhas.map((s) =>
      `<li class="${s.id === M.salva ? "atual" : ""}"><button class="link" data-abrir="${s.id}" title="Abrir para editar">${esc(s.nome)}</button>` +
      `<small>${s.hora}</small><button class="mini" data-dup="${s.id}" title="Duplicar">⧉</button><button class="mini" data-apagar="${s.id}" title="Apagar da lista">×</button></li>`).join("")}</ul>`
      : "<p class='nota'>Nenhuma montagem salva desta especialização e estrutura.</p>") +
      (outras ? `<p class="nota">${outras} salva${outras > 1 ? "s" : ""} em outra especialização ou estrutura.</p>` : "");
  }

  function salvar(nova) {
    const nome = ($("#nome").value || "Sem nome").trim();
    const hora = new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
    const dados = { estrutura: M.estrutura, spec: M.spec, kit: [...M.kit], ultimate: M.ultimate, nos: { ...M.nos }, nome };
    let id = M.salva;
    if (nova || !id || !SALVAS.find((s) => s.id === id)) {
      id = "s" + Date.now();
      SALVAS.push({ id, nome: nova && M.salva ? nome + " (cópia)" : nome, hora, montagem: dados });
    } else {
      Object.assign(SALVAS.find((s) => s.id === id), { nome, hora, montagem: dados });
    }
    const s = SALVAS.find((x) => x.id === id);
    M = { ...M, nome: s.nome, salva: id };
    guardar("x1-salvas", SALVAS);
    api("/api/salvar", { montagem: s.montagem, nota: "" });
    $("#salvo").textContent = `Salva: ${s.nome}.`;
    atualizarMontagem();
  }

  function realcar(ids, ligar) {
    for (const id of ids) for (const el of document.querySelectorAll(`[data-hab-id="${id}"]`)) el.classList.toggle("realce", ligar);
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
    return `<div class="carta ${o.vivo ? "" : "morto"} ${o.invocacao ? "invocada" : ""} ${E.aguardando === o.id ? "vez" : ""} ${alvo ? "alvo" : ""}" data-alvo="${alvo ? o.id : ""}">` +
      `<span class="ret">${o.invocacao ? `<span class="sem-retrato">${esc(o.nome[0])}</span>` : retrato(o)}</span><span class="nome">${esc(o.nome)}${o.invocacao ? ` <small>· invocação de ${esc(o.dono)}</small>` : ""}</span>` +
      (prev ? `<span class="previsto">${esc(prev)}<small>previsto</small></span>` : "<span></span>") +
      `<div><div class="barra"><i style="width:${pv}%"></i></div>` +
      (o.recurso_max ? `<div class="barra rec"><i style="width:${o.recurso / o.recurso_max * 100}%"></i></div>` : "") +
      `<span class="vals">Vida ${o.vida}/${o.vida_max}${o.recurso_max ? ` · ${esc(o.recurso_nome)} ${o.recurso}/${o.recurso_max}` : ""}</span></div>` +
      `<div class="chips">${chips(o)}</div></div>`;
  }

  function explica(a) {
    return a ? `<b>${esc(a.nome)}</b>${a.versao ? ` (${esc(a.versao)})` : ""}: ${esc(a.desc)}${a.notas && a.notas.length ? `<ul>${a.notas.map((n) => `<li>${esc(n)}</li>`).join("")}</ul>` : ""}` : "";
  }

  function desenharLuta() {
    if (!E) { $("#luta-titulo").textContent = "Nenhuma luta. Monte a build e escolha Lutar."; return; }
    const est = CAT.estruturas[E.montagem.estrutura].nome, spec = CAT.specs[E.montagem.spec].nome;
    $("#luta-titulo").innerHTML = `<b>${esc(E.encontro_nome)}</b> · semente ${E.semente} · Rodada ${E.rodada} · ${esc(E.montagem.nome)} (${esc(spec)}, ${esc(est)})`;
    $("#ordem").innerHTML = E.ordem.map((x) =>
      `<span class="${x.lado} ${x.agiu ? "agiu" : ""} ${x.atual ? "atual" : ""} ${x.vivo ? "" : "morto"}">${esc(x.nome)}</span>`).join("") +
      (E.combatentes.some((o) => o.invocacao) ? `<span class="nota-ordem">Invocações agem no fim da vez de Jean</span>` : "");
    $("#grupo").innerHTML = E.combatentes.filter((o) => o.lado === "aliado").map(carta).join("");
    $("#frente").innerHTML = E.combatentes.filter((o) => o.lado === "inimigo").map(carta).join("");
    const quem = E.combatentes.find((o) => o.id === E.aguardando);
    if (quem && !E.fim) {
      const furia = E.pode_sair_furia
        ? ` <button class="botao-x" id="sair-furia" ${E.motivo_sair_furia ? "disabled" : ""} title="Não gasta a ação">Sair da Fúria (+12 de Vigor e 1 Guarda) <kbd>F</kbd></button>${E.motivo_sair_furia ? ` <span class="m">${esc(E.motivo_sair_furia)}</span>` : ""}`
        : "";
      $("#doca").innerHTML = `<div class="quem">${retrato(quem)}<b>${esc(quem.nome)}</b>` +
        (SEL ? `<span>${esc(SEL.nome)}: escolha o alvo (clique na carta). <kbd>Esc</kbd> cancela.</span>` : "<span>Escolha a ação (ou o número).</span>") + furia +
        `</div><div class="acoes">${E.acoes.map((a, i) =>
          `<button class="acao ${a.ultimate ? "ult" : ""} ${SEL && SEL.id === a.id ? "escolhida" : ""}" data-acao="${a.id}" ${a.disponivel ? "" : "disabled"}>` +
          `<span class="n">${i + 1}. ${esc(a.nome)}</span>${a.versao ? `<span class="v">${esc(a.versao)}</span> ` : ""}` +
          `<span class="p">${esc(a.pagamento || "Grátis")}${a.ultimate ? " · 1 vez por luta" : ""}</span>${a.motivo ? `<span class="m">${esc(a.motivo)}</span>` : ""}</button>`).join("")}</div>` +
        `<div class="explica">${explica(VER || SEL)}</div>`;
    } else {
      $("#doca").innerHTML = E.fim ? "" : "<p class='nota'>Os inimigos agem.</p>";
    }
    desenharLog();
    desenharFim();
  }

  function desenharLog() {
    const log = $("#log");
    log.innerHTML = E.eventos.map((e) => {
      const inimigo = e.tipo === "acao" && e.ator && e.ator.includes("#") && !/^(fogo_fatuo|sentinela|estandarte)#/.test(e.ator);
      const cad = e.tipo === "gatilho" || e.tipo === "barrado" ? `<span class="cad" title="Cadeia ${e.cadeia}${e.elo ? `, efeito ${e.elo}` : ""}">c${e.cadeia}${e.elo ? "·" + e.elo : ""}</span>` : "";
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
    $("#montagens").innerHTML = r.montagens.length ? `<table class="reg"><tr><th>Hora</th><th>Build</th><th>Kit</th><th>Talentos</th></tr>` +
      r.montagens.slice().reverse().map((x) => `<tr><td>${x.hora}</td><td>${esc(x.montagem.nome)}<br><small>${esc(nomeSpec(x.montagem.spec))} · ${esc(nomeEst(x.montagem.estrutura))}</small></td>` +
        `<td>${esc(x.montagem.kit.join(", "))} · ${esc(x.montagem.ultimate || "")}</td><td>${esc(Object.entries(x.montagem.nos).map(([k, v]) => v > 1 ? `${k} ×${v}` : k).join(", "))}</td></tr>`).join("") + "</table>"
      : "<p class='nota'>Nenhuma montagem salva nesta sessão do servidor.</p>";
  }

  // ---------------------------------------------------------------- eventos
  document.addEventListener("click", (ev) => {
    const t = ev.target.closest("button, .carta, [data-alvo]");
    if (!t) return;
    const d = t.dataset;
    if (d.tela) return mostrar(d.tela);
    if (d.est) return trocar("estrutura", d.est);
    if (d.spec) return trocar("spec", d.spec);
    if (d.filtro) { FILTRO = { ...FILTRO, [d.filtro]: d.valor }; return desenharMontar(); }
    if (d.ex !== undefined) {
      const x = CAT.exemplos.find((e) => e.id === d.ex);
      M = x ? { estrutura: x.estrutura, spec: x.spec, kit: [...x.kit], ultimate: x.ultimate, nos: { ...x.nos }, nome: x.nome, salva: null }
        : { ...M, kit: [], nos: {}, nome: "Livre", salva: null };
      return atualizarMontagem();
    }
    if (d.abrir || d.dup) {
      const s = SALVAS.find((x) => x.id === (d.abrir || d.dup));
      if (!s) return;
      M = { ...s.montagem, kit: [...s.montagem.kit], nos: { ...s.montagem.nos }, nome: s.nome, salva: d.abrir ? s.id : null };
      if (d.dup) { $("#nome").value = s.nome + " (cópia)"; M.nome = s.nome + " (cópia)"; return salvar(true); }
      return atualizarMontagem();
    }
    if (d.apagar) {
      SALVAS = SALVAS.filter((x) => x.id !== d.apagar);
      if (M.salva === d.apagar) M.salva = null;
      guardar("x1-salvas", SALVAS);
      return desenharMontar();
    }
    if (t.id === "salvar") return salvar(false);
    if (t.id === "duplicar") return salvar(true);
    if (d.ult) { M = { ...M, ultimate: d.ult, nome: editada(M.nome) }; return atualizarMontagem(); }
    if (d.hab) {
      const kit = M.kit.includes(d.hab) ? M.kit.filter((h) => h !== d.hab) : (M.kit.length < CAT.espacos ? [...M.kit, d.hab] : M.kit);
      M = { ...M, kit, nome: editada(M.nome) };
      return atualizarMontagem();
    }
    if (d.mais || d.menos) {
      const id = d.mais || d.menos, nos = { ...M.nos };
      nos[id] = (nos[id] || 0) + (d.mais ? 1 : -1);
      if (nos[id] <= 0) delete nos[id];
      M = { ...M, nos, nome: editada(M.nome) };
      return atualizarMontagem();
    }
    if (t.id === "zerar") { M = { ...M, nos: {}, nome: editada(M.nome) }; return atualizarMontagem(); }
    if (t.id === "lutar") return lutar();
    if (d.acao) return escolher(E.acoes.find((a) => a.id === d.acao));
    if (d.alvo && SEL) return agir(SEL.id, d.alvo);
    if (t.id === "sair-furia") return api("/api/sair_furia", {}).then((r) => { E = r.estado; desenharLuta(); });
    if (t.id === "repetir") return lutar(E.semente);
    if (t.id === "outra") return lutar(Math.floor(Math.random() * 100000));
    if (t.id === "voltar") return mostrar("montar");
    if (t.id === "ver-log") { $("#fim").hidden = true; return; }
  });
  document.addEventListener("change", (ev) => {
    if (ev.target.id === "so-kit") { FILTRO = { ...FILTRO, kit: ev.target.checked }; desenharMontar(); }
    if (ev.target.id === "encontro") { ENC = ev.target.value; atualizarMontagem(); }
    if (ev.target.id === "nome") { M = { ...M, nome: ev.target.value.trim() || "Sem nome" }; guardar("x1-montagem", M); }
  });
  // passar o mouse num talento acende as habilidades que ele muda; numa habilidade, os talentos que a mudam
  document.addEventListener("mouseover", (ev) => {
    const no = ev.target.closest("[data-no]");
    const hab = ev.target.closest("[data-hab-id]");
    for (const el of document.querySelectorAll(".realce")) el.classList.remove("realce");
    if (no) realcar(no.dataset.afeta.split(" ").filter(Boolean), true);
    if (hab && TELA === "montar") {
      for (const n of document.querySelectorAll("[data-no]")) if (n.dataset.afeta.split(" ").includes(hab.dataset.habId)) n.classList.add("realce");
    }
    const b = ev.target.closest("[data-acao]");
    if (b && E) {
      const a = E.acoes.find((x) => x.id === b.dataset.acao);
      if (a && a !== VER) { VER = a; const ex = document.querySelector("#doca .explica"); if (ex) ex.innerHTML = explica(a); }
    }
  });
  document.addEventListener("keydown", (ev) => {
    if (ev.target.matches("input, textarea, select")) return;
    const k = ev.key.toLowerCase();
    if (k === "m") return mostrar("montar");
    if (k === "l") return mostrar("luta");
    if (k === "g") return mostrar("registro");
    if (TELA === "montar" && ev.key === "Enter") return lutar();
    if (TELA !== "luta" || !E) return;
    if (ev.key === "Escape") { SEL = null; return desenharLuta(); }
    if (k === "r" && E.fim) return lutar(E.semente);
    if (k === "f" && E.pode_sair_furia && !E.motivo_sair_furia) return api("/api/sair_furia", {}).then((r) => { E = r.estado; desenharLuta(); });
    const n = Number(ev.key);
    if (n >= 1 && n <= 9) {
      if (SEL) { const alvo = SEL.alvos[n - 1]; if (alvo) return agir(SEL.id, alvo); return; }
      return escolher(E.acoes[n - 1]);
    }
  });

  // ---------------------------------------------------------------- início
  (async () => {
    CAT = await api("/api/catalogo");
    $("#versao").textContent = CAT.versao;
    document.title = `Etapa 8 · X1 · ${CAT.versao}`;
    $("#regras").innerHTML = CAT.regras.map((r) => `<li>${esc(r)}</li>`).join("");
    const salvo = ler("x1-montagem");
    const ex = CAT.exemplos.find((x) => x.id === "pavio");
    M = salvo && CAT.specs[salvo.spec] && CAT.estruturas[salvo.estrutura] && salvo.ultimate !== undefined ? salvo
      : { estrutura: "t4", spec: "piromante", kit: [...ex.kit], ultimate: ex.ultimate, nos: { ...ex.nos }, nome: ex.nome, salva: null };
    const enc = ler("x1-encontro");
    if (enc && CAT.encontros[enc]) ENC = enc;
    await atualizarMontagem();
  })();
})();
