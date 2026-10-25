/* PROTÓTIPO do combate e dos atributos (25/10/2026; nada no jogo): a tela só desenha o que o servidor manda
   (motor/regras.py decide tudo, inclusive custos, alvos válidos, motivos e previsões). */
"use strict";
(() => {
  const $ = (s) => document.querySelector(s);
  const esc = (t) => String(t ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const guardado = (k, v) => { try { if (v === undefined) return JSON.parse(localStorage.getItem("combate-atr:" + k)); localStorage.setItem("combate-atr:" + k, JSON.stringify(v)); } catch (e) { return null; } return null; };
  const ICONE_ESTADO = { atordoado: "atordoado", sangramento: "sangramento", marca: "marcado", defesa: "guarda",
                         escudo: "barreira", comando: "fortalecido", abalado: "enfraquecido" };

  let cat = null, E = null, anterior = null, vistos = 0, ocupado = false, sel = null, aviso = "";
  let fichaDe = "heroi", livre = guardado("livre") || null;

  async function api(caminho, corpo) {
    const r = await fetch(caminho, corpo ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(corpo) } : undefined);
    return r.json();
  }

  // ---------------------------------------------------------------- retratos
  const retrato = (o, lado) => (o.lado === "aliado" ? Icones.cabeca(o.retrato, lado) : Icones.criatura(o.retrato, lado))
    || `<span class="sem-retrato" style="--s:${lado}">${esc(o.nome[0])}</span>`;

  // ---------------------------------------------------------------- começar
  async function iniciar() {
    const encontro = $("#encontro").value, distribuicao = $("#distribuicao").value;
    guardado("escolha", { encontro, distribuicao });
    const corpo = { encontro, distribuicao };
    if (distribuicao === "livre") corpo.atributos = livre;
    const r = await api("/api/iniciar", corpo);
    if (r.erro && distribuicao === "livre") { $("#distribuicao").value = "A"; return iniciar(); }
    if (r.erro) { aviso = r.erro; return desenhar(); }
    E = r; anterior = null; vistos = 0; sel = null; aviso = ""; fichaDe = "heroi";
    desenhar();
  }

  async function agir(acao, alvo) {
    if (ocupado || !E || !E.aguardando) return;
    ocupado = true;
    sel = null;
    document.body.classList.add("ocupado");
    try {
      const r = await api("/api/agir", { turno_id: E.turno_id, acao, alvo });
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

  // ---------------------------------------------------------------- desenhar
  function desenhar() {
    if (!E) return;
    const t = $("#teste");
    t.hidden = !E.teste;
    t.textContent = E.teste || "";
    $("#objetivo").innerHTML = `<b>${esc(E.nome)}</b> ${esc(E.objetivo)}`;
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

  function cartaAliado(o) {
    const pos = E.ordem.findIndex((x) => x.id === o.id) + 1;
    const ativo = E.aguardando === o.id, passo = E.ordem.find((x) => x.id === o.id);
    const situ = o.caido ? "" : ativo ? '<span class="tag vez">age agora</span>' : passo.passou ? '<span class="tag">já agiu</span>' : "";
    return `<article class="carta aliado${ativo ? " ativo" : ""}${o.caido ? " caido" : ""}" data-id="${o.id}"${marcaAlvo(o)}>
      <div class="cab">${retrato(o, 48)}<div><h3>${esc(o.nome)} ${situ}</h3><p class="papel">${esc(o.papel)} · ${pos}º na ordem</p></div>${delta(o)}</div>
      ${barra("vida", o.vida, o.vida_max, "Vida")}
      ${o.caido ? '<p class="caido-nota">Caíd${o.a}: não age. Volta só com Reerguer ou a Pena de Fênix, na mesma posição.</p>' : barra("recurso r-" + o.recurso_nome.toLowerCase(), o.recurso, o.recurso_max, o.recurso_nome)}
      ${estados(o)}
    </article>`;
  }

  function cartaInimigo(o) {
    const am = E.ameacas.find((a) => a.de === o.id);
    const tags = [];
    if (o.protecao) tags.push(`Proteção ${o.protecao}`);
    if (o.firme) tags.push("Firme: não fica atordoado");
    if (o.ponto_fraco) tags.push(`Ponto fraco: ${o.ponto_fraco} (Percepção 5+)`);
    if (o.entra_rodada > E.rodada) tags.push(`age a partir da rodada ${o.entra_rodada}`);
    return `<article class="carta inimigo${am ? " preparando" : ""}" data-id="${o.id}"${marcaAlvo(o)}>
      <div class="cab">${retrato(o, 48)}<div><h3>${esc(o.nome)}</h3><p class="papel">${E.ordem.findIndex((x) => x.id === o.id) + 1}º na ordem</p></div>${delta(o)}</div>
      ${barra("vida", o.vida, o.vida_max, "Vida")}
      ${o.guarda_max ? barra("guarda", o.guarda, o.guarda_max, o.guarda ? "Guarda: metade do dano" : "Guarda rompida") : ""}
      ${tags.length ? `<p class="tags">${tags.map(esc).join(" · ")}</p>` : ""}
      ${estados(o)}
      ${am ? ameaca(am) : ""}
    </article>`;
  }

  function ameaca(a) {
    const nome = (id) => E.aliados.find((x) => x.id === id)?.nome || id;
    let alvo, conta = "";
    if (a.area) {
      alvo = "todo o grupo";
      conta = `<ul>${a.alvos.map((x) => `<li>${esc(x.nome)}: ${esc(x.resultado)}</li>`).join("")}</ul>`;
    } else if (a.previsto) {
      const p = a.previsto;
      alvo = esc(a.alvo_nome);
      conta = p.quem !== a.alvo ? `<p>${esc(nome(p.quem))} protege e recebe <b>${p.agora}</b>.</p>`
        : `<p>Recebe <b>${p.agora}</b> de dano${p.se_defender < p.agora ? `; se ${esc(a.alvo_nome)} defender, ${p.se_defender}` : ""}.</p>`;
    } else alvo = "o mais ferido";
    return `<div class="ameaca"><p class="titulo">${esc(a.nome)} em ${alvo}</p>${conta}${a.efeito ? `<p class="efeito">${esc(a.efeito)}</p>` : ""}<p class="quando">Resolve ${esc(a.resolve)}.</p></div>`;
  }

  function desenharDoca() {
    const d = $("#doca");
    if (E.fim) { d.innerHTML = ""; return; }
    const o = E.aliados.find((x) => x.id === E.aguardando);
    if (!o) { d.innerHTML = ""; return; }
    if (sel) {
      const nomes = sel.alvos.map((id, i) => `<kbd>${i + 1}</kbd> ${esc([...E.aliados, ...E.inimigos].find((x) => x.id === id).nome)}`).join(" · ");
      d.innerHTML = `<div class="quem">${retrato(o, 32)}<b>${esc(o.nome)}</b></div><div class="escolha-alvo"><p><b>${esc(sel.nome)}</b>: escolha o alvo (clique na carta ou o número). ${nomes}</p>` +
        `<button class="botao" id="cancelar">Voltar <kbd>Esc</kbd></button></div>`;
      $("#cancelar").addEventListener("click", () => { sel = null; desenhar(); });
      return;
    }
    const botoes = E.acoes.map((a, i) => {
      const custo = a.item ? `${a.qtd} na bolsa` : a.custo ? `${a.custo} de ${a.recurso}` : "sem custo";
      const ic = a.item ? Icones.consumivel(a.icone, 24) : "";
      return `<button class="acao${a.motivo ? " nao" : ""}${a.item ? " item" : ""}" data-i="${i}" ${a.motivo ? 'aria-disabled="true"' : ""}>` +
        `<span class="tecla">${i + 1}</span>${ic}<b>${esc(a.nome)}</b><span class="custo">${esc(custo)}</span>` +
        `<span class="desc">${esc(a.motivo || a.desc)}</span></button>`;
    }).join("");
    d.innerHTML = `<div class="quem">${retrato(o, 32)}<b>${esc(o.nome)}</b><span>${o.recurso} de ${esc(o.recurso_nome)}</span></div><div class="acoes">${botoes}</div>` +
      (aviso ? `<p class="aviso">${esc(aviso)}</p>` : "");
    d.querySelectorAll(".acao").forEach((b) => b.addEventListener("click", () => escolher(E.acoes[+b.dataset.i])));
  }

  function desenharRegistro() {
    const r = $("#registro");
    let html = "", rod = 0;
    E.eventos.forEach((ev, i) => {
      if (ev.tipo === "rodada") { rod = ev.rodada; html += `<h4>${esc(ev.texto)}</h4>`; return; }
      const novo = i >= vistos && vistos > 0;
      html += `<p class="ev ev-${ev.tipo}${novo ? " novo" : ""}" style="--i:${Math.max(0, i - vistos)}">${esc(ev.texto)}` +
        (ev.conta ? `<small>${esc(ev.conta)}</small>` : "") + "</p>";
    });
    r.innerHTML = html;
    r.scrollTop = r.scrollHeight;
    void rod;
  }

  function desenharFicha() {
    const o = E.aliados.find((x) => x.id === fichaDe);
    const seletor = E.aliados.map((a) => `<button data-ficha="${a.id}" class="${a.id === fichaDe ? "atual" : ""}">${esc(a.nome)}</button>`).join("");
    const atr = cat.atributos.map((a) => `<li><span>${esc(a.nome)}</span><b>${o.atributos[a.id]}</b></li>`).join("");
    const der = o.derivados.map((d) => `<li><span>${esc(d.nome)}</span><b>${esc(d.valor)}</b><small>${esc(d.como)}</small></li>`).join("");
    $("#ficha").innerHTML = `<div class="seletor">${seletor}</div>` +
      (o.id === "heroi" ? `<p class="nota">Construção: ${esc(nomeDist(E.distribuicao))}. Mesmo nível, arma, armadura e grupo nas três.</p>` : `<p class="nota">Atributos próprios do companheiro (não se distribuem aqui).</p>`) +
      `<h4>Atributos</h4><ul class="atributos">${atr}</ul><h4>O que eles mudam agora</h4><ul class="derivados">${der}</ul>`;
    $("#ficha").querySelectorAll("[data-ficha]").forEach((b) => b.addEventListener("click", () => { fichaDe = b.dataset.ficha; desenharFicha(); }));
  }

  const nomeDist = (id) => (id === "livre" ? "livre" : cat.distribuicoes.find((d) => d.id === id).nome);

  function desenharFim() {
    const f = $("#fim");
    f.hidden = !E.fim;
    if (!E.fim) return;
    const r = E.resumo;
    f.innerHTML = `<div class="m-janela"><h2>${E.fim === "vitoria" ? "Vitória" : "Derrota"}</h2><p>${E.fim === "vitoria" ? "Na" : "Até a"} rodada ${E.rodada}. ` +
      `Quedas: ${r.quedas}. Preparações: ${r.preparos} anunciadas, ${r.preparos_resolvidos} resolvidas, ${r.preparos_desfeitos} desfeitas.</p>` +
      `<p>Dano recebido: ${E.aliados.map((a) => `${esc(a.nome)} ${r.dano_recebido[a.id]}`).join(" · ")}.</p>` +
      `<div class="botoes"><button class="botao" id="fim-reiniciar">Reiniciar <kbd>R</kbd></button><button class="botao" data-abrir="resultados">Resultados da sessão</button></div></div>`;
    $("#fim-reiniciar").addEventListener("click", iniciar);
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
    if (!livre) livre = { ...cat.distribuicoes[0].atributos };
    const r = await api("/api/comparar", { atributos: somaLivre() === cat.pontos ? livre : null });
    const cols = r.colunas;
    const linhasAtr = cat.atributos.map((a) => {
      const vs = cols.map((k) => k.atributos[a.id]);
      return `<tr class="${new Set(vs).size > 1 ? "difere" : ""}"><th>${esc(a.nome)}</th>${vs.map((v) => `<td>${v}</td>`).join("")}</tr>`;
    }).join("");
    const linhasDer = cols[0].derivados.map((d, j) => {
      const vs = cols.map((k) => k.derivados[j].valor);
      return `<tr class="${new Set(vs.map(String)).size > 1 ? "difere" : ""}"><th>${esc(d.nome)}</th>${vs.map((v) => `<td>${esc(v)}</td>`).join("")}</tr>`;
    }).join("");
    const ordem = `<tr class="difere"><th>Ordem no encontro 1</th>${cols.map((k) => `<td class="ordem">${k.ordem.map(esc).join(" › ")}</td>`).join("")}</tr>`;
    const editor = cat.atributos.map((a) => `<li><span>${esc(a.nome)}</span><button data-mais="${a.id}" data-d="-1" aria-label="menos ${esc(a.nome)}">−</button>` +
      `<b>${livre[a.id]}</b><button data-mais="${a.id}" data-d="1" aria-label="mais ${esc(a.nome)}">+</button></li>`).join("");
    const soma = somaLivre();
    c.innerHTML = `<h2>Comparar construções</h2><p class="nota">O mesmo Jean: nível 3, a mesma arma (8), a mesma armadura (proteção 3), os mesmos companheiros. Só os ${cat.pontos} pontos de atributo mudam. Em destaque, o que difere.</p>` +
      `<div class="comparar"><table><thead><tr><th></th>${cols.map((k) => `<th>${esc(k.nome)}</th>`).join("")}</tr></thead><tbody>${linhasAtr}${ordem}${linhasDer}</tbody></table>` +
      `<div class="editor m-painel"><h3>Construção livre</h3><ul>${editor}</ul><p class="${soma === cat.pontos ? "ok" : "falta"}">${soma} de ${cat.pontos} pontos (cada um de ${cat.min} a ${cat.max})</p>` +
      `<button class="botao" id="usar-livre" ${soma === cat.pontos ? "" : "disabled"}>Lutar com a livre</button></div></div>`;
    c.querySelectorAll("[data-mais]").forEach((b) => b.addEventListener("click", () => {
      const k = b.dataset.mais, v = livre[k] + +b.dataset.d;
      if (v < cat.min || v > cat.max) return;
      livre[k] = v; guardado("livre", livre);
      janelaComparar(c);
    }));
    c.querySelector("#usar-livre").addEventListener("click", () => { $("#distribuicao").value = "livre"; fechar(); iniciar(); });
  }
  const somaLivre = () => (livre ? Object.values(livre).reduce((a, b) => a + b, 0) : 0);

  async function janelaSituacao(c, escolha, ajuda) {
    const dist = $("#distribuicao").value;
    const s = await api("/api/situacao", { distribuicao: dist === "livre" ? "A" : dist, atributos: dist === "livre" ? livre : null, escolha, ajuda });
    const ops = s.opcoes.map((o) => `<li><button class="botao" data-op="${o.id}">${esc(o.texto)}</button>` +
      `<span class="req ${o.valor >= o.minimo ? "ok" : "falta"}">${esc(o.atributo)} ${o.valor} (precisa de ${o.minimo})</span>` +
      (o.ajuda ? `<button class="botao" data-op="${o.id}" data-ajuda="1">${esc(o.ajuda.texto)}</button>` : "") + "</li>").join("");
    c.innerHTML = `<h2>${esc(s.titulo)}</h2><p class="nota">Fora da luta, com a construção escolhida (${esc(nomeDist(dist))}). Os companheiros acrescentam, mas a escolha continua sendo de Jean.</p>` +
      `<p class="prosa">${esc(s.texto)}</p><ul class="opcoes">${ops}</ul>` +
      (s.resultado ? `<p class="resultado ${s.resultado.ok ? "ok" : "falta"}">${esc(s.resultado.texto)} <small>${esc(s.resultado.como)}</small></p>` : "");
    c.querySelectorAll("[data-op]").forEach((b) => b.addEventListener("click", () => janelaSituacao(c, b.dataset.op, !!b.dataset.ajuda)));
  }

  async function janelaResultados(c) {
    const r = await api("/api/resultados");
    const linhas = r.resultados.map((x) => `<tr><td>${esc(x.hora)}</td><td>${esc(x.nome)}</td><td>${esc(x.distribuicao)}</td><td>${esc(x.fim)}</td>` +
      `<td>${x.rodadas}</td><td>${x.quedas}</td><td>${Object.values(x.dano_recebido).join(" / ")}</td><td>${x.preparos_resolvidos}/${x.preparos_desfeitos}</td>` +
      `<td class="acoes-usadas">${Object.entries(x.acoes).sort((a, b) => b[1] - a[1]).map(([k, n]) => `${esc(k)} ${n}`).join(", ")}</td></tr>`).join("");
    c.innerHTML = `<h2>Resultados da sessão</h2><p class="nota">Cada luta terminada ou reiniciada. Guardados só nesta execução, em <code>${esc(r.pasta)}</code>.</p>` +
      (linhas ? `<table class="resultados"><thead><tr><th>Hora</th><th>Encontro</th><th>Constr.</th><th>Fim</th><th>Rodadas</th><th>Quedas</th><th>Dano Jean / Odette / Morel</th><th>Preparos saíram / desfeitos</th><th>Ações</th></tr></thead><tbody>${linhas}</tbody></table>`
        : "<p>Nenhuma luta terminada ainda.</p>");
  }

  // ---------------------------------------------------------------- teclado
  document.addEventListener("keydown", (e) => {
    if (e.repeat || e.ctrlKey || e.altKey || e.metaKey) return;
    if (!$("#modal").hidden) { if (e.key === "Escape") fechar(); return; }
    if (e.key === "Escape" && sel) { sel = null; desenhar(); return; }
    if (e.key === "r" || e.key === "R") { e.preventDefault(); iniciar(); return; }
    const n = parseInt(e.key, 10);
    if (!E || E.fim || !E.aguardando || !(n >= 1)) return;
    if (sel) { if (sel.alvos[n - 1]) agir(sel.id, sel.alvos[n - 1]); return; }
    if (E.acoes[n - 1]) escolher(E.acoes[n - 1]);
  });

  // ---------------------------------------------------------------- abrir
  async function comecar() {
    cat = await api("/api/catalogo");
    const ult = guardado("escolha") || {};
    $("#encontro").innerHTML = cat.encontros.map((e) => `<option value="${e.id}">${esc(e.nome)}</option>`).join("");
    $("#distribuicao").innerHTML = cat.distribuicoes.map((d) => `<option value="${d.id}" title="${esc(d.resumo)}">${esc(d.nome)}</option>`).join("")
      + '<option value="livre">Livre (montada em Comparar)</option>';
    if (cat.encontros.some((e) => e.id === ult.encontro)) $("#encontro").value = ult.encontro;
    if (ult.distribuicao && (ult.distribuicao !== "livre" || livre)) $("#distribuicao").value = ult.distribuicao;
    $("#encontro").addEventListener("change", iniciar);
    $("#distribuicao").addEventListener("change", () => { if ($("#distribuicao").value === "livre" && !livre) return abrir("comparar"); iniciar(); });
    $("#reiniciar").addEventListener("click", iniciar);
    document.querySelectorAll("#topo [data-abrir]").forEach((b) => b.addEventListener("click", () => abrir(b.dataset.abrir)));
    $("#modal .fechar").addEventListener("click", fechar);
    $("#modal").addEventListener("click", (e) => { if (e.target.id === "modal") fechar(); });
    document.querySelectorAll("#abas button").forEach((b) => b.addEventListener("click", () => {
      document.querySelectorAll("#abas button").forEach((x) => x.classList.toggle("atual", x === b));
      $("#registro").hidden = b.dataset.aba !== "registro";
      $("#ficha").hidden = b.dataset.aba !== "ficha";
    }));
    // as teclas de seleção não mudam o select de encontro/construção por acidente
    document.querySelectorAll("#topo select").forEach((s) => s.addEventListener("keydown", (e) => { if (/^[0-9rR]$/.test(e.key)) e.preventDefault(); }));
    await iniciar();
  }
  window.Demo = { get estado() { return E; }, agir, iniciar, abrir };
  comecar();
})();
