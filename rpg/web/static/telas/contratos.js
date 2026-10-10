/* Contratos: o mural da vila, o diário (os contratos aceitos, os rumores e quem te persegue) e o rastreador do
   painel do herói. */
"use strict";

(() => {
  const { h, S, barra } = Telas;

  /** A missão da campanha no diário: o nome, o objetivo de agora, onde ele leva e as pistas que você já tem. */
  function missaoDiario(m) {
    const lugar = m.lugar ? `${S(MapaPx.sprite({ tipo: m.lugar_tipo, bioma: m.bioma }), 1)} ${h(m.lugar)}${m.distancia ? ` · ${Texto.plural(m.distancia, "trecho")}` : m.distancia === 0 ? " · você está aqui" : ""}` : "";
    const pistas = m.pistas.map((p) => `<li>${h(p)}</li>`).join("");
    return `<div class="missao-diario" data-missao="${h(m.id)}"><div class="missao-cab">${S("pergaminho", 2)}<b>${h(m.nome)}</b></div>
      <div class="missao-objetivo">${h(m.objetivo)}</div><div class="missao-lugar">${lugar}</div>
      ${pistas ? `<div class="missao-pistas"><span>Pistas</span><ul>${pistas}</ul></div>` : ""}</div>`;
  }

  function diario(d) {
    const missoes = (d.missoes || []).map(missaoDiario).join("");
    const contratos = d.contratos.map((c) => cartaz(c, true, false, d.nivel_heroi)).join("");
    const rumores = d.rumores.map((r) => `<div class="bilhete"><span class="prego"></span>${S("olho", 1)} ${h(r.texto)}<small>${r.expira > 0 ? `some em ${Texto.plural(r.expira, "dia")}` : "some hoje"}</small></div>`).join("");
    const losangos = [0, 1, 2].map((i) => `<i class="sigilo${i < d.sigilos ? " tem" : ""}"></i>`).join("");
    return `<div class="tela diario">
      <div class="faixa-jornada"><span>Dia ${d.dia}</span><span class="sigilos-diario" title="Sigilos dos guardiões">${losangos} ${d.sigilos}/3</span></div>
      ${missoes ? `<div class="quadro quadro-missao"><div class="quadro-cab"><b>Missão</b><span>o lugar fica marcado no mapa</span></div>${missoes}</div>` : ""}
      <div class="quadro"><div class="quadro-cab"><b>Contratos</b><span>${d.contratos.length}/${d.limite} · os lugares ficam marcados no mapa</span></div>
        <div class="cartazes">${contratos || '<span class="vazio">Nenhum contrato. Procure o mural de uma vila.</span>'}</div></div>
      ${rumores ? `<h4>Rumores</h4><div class="bilhetes">${rumores}</div>` : ""}
      ${d.nemesis ? `<h4>Quem te persegue</h4><div class="bilhete inimigo">${S("fera", 1)} ${h(d.nemesis.nome)}, ${h(d.nemesis.familia)}. Ele não esqueceu de você.</div>` : ""}
    </div>`;
  }

  const TIPO_CONTRATO = { caca: "Caça", alvo: "Procurado", entrega: "Entrega" };
  function cartaz(c, ativo, cheio, nivelHeroi) {
    const arte = c.tipo === "entrega" ? "saco" : c.retrato || "caveira";
    const titulo = c.tipo === "alvo" ? c.alvo : c.tipo === "entrega" ? (c.objeto || "Entrega") : c.desc.replace(/^Eliminar /, "").replace(/ em .*$/, "");
    const perigo = c.nivel == null ? "" : c.nivel - nivelHeroi >= 2 ? "alto" : c.nivel >= nivelHeroi ? "medio" : "baixo";
    const lugar = `${S(MapaPx.sprite({ tipo: c.lugar_tipo, bioma: c.bioma }), 1)} ${h(c.lugar)}${c.distancia != null ? ` · ${Texto.plural(c.distancia, "trecho")}` : ""}${c.nivel != null ? ` <span class="perigo-tag ${perigo}">Nv.${c.nivel}</span>` : ""}`;
    let progresso = "";
    if (ativo && c.tipo === "caca" && c.progresso && !c.recebendo) {
      const [feito, total] = c.progresso.split("/").map(Number);
      progresso = `<div class="contrato-progresso">${barra("xp", feito, total)}<span>${feito}/${total}</span></div>`;
    }
    let botao;
    if (c.recebendo) botao = '<span class="carimbo">Cumprido</span>';  // no quadro de pagamento: o carimbo bate
    else if (ativo) botao = c.concluido ? '<span class="contrato-feito">Feito! Volte a uma vila para receber</span>'
      : `<button type="button" class="contrato-botao abandonar" data-abandonar="${c.id}" title="Reputação −${c.penalidade}">Abandonar</button>`;
    else botao = `<button type="button" class="contrato-botao${cheio ? " bloqueado" : ""}" data-aceitar="${c.id}"${cheio ? ' aria-disabled="true"' : ""}>Aceitar</button>`;
    const recem = ativo && contratosVistos && !contratosVistos.has(c.id);
    return `<div class="contrato tipo-${h(c.tipo)}${ativo ? " ativo" : ""}${c.concluido && !c.recebendo ? " concluido" : ""}${recem ? " recem" : ""}">
      <span class="prego"></span><div class="contrato-tipo">${TIPO_CONTRATO[c.tipo] || h(c.tipo)}</div>
      <div class="contrato-arte">${S(arte, 3)}</div>
      <div class="contrato-titulo">${h(titulo)}</div>
      <div class="contrato-desc">${h(c.desc)}</div>
      <div class="contrato-lugar">${lugar}</div>${progresso}
      <div class="contrato-premio"><span>${S("moeda", 1)} ${c.ouro}</span><span>${S("estrela", 1)} ${c.xp} XP</span></div>
      ${botao}</div>`;
  }
  let contratosVistos = null;  // os contratos que você já tinha: o recém-aceito chega pregado com destaque
  function mural(d) {
    const cheio = d.ativos.length >= d.limite;
    const oferta = d.oferta.map((c) => cartaz(c, false, cheio, d.nivel_heroi)).join("");
    const ativos = d.ativos.map((c) => cartaz(c, true, cheio, d.nivel_heroi)).join("");
    contratosVistos = new Set(d.ativos.map((c) => c.id));
    return `<div class="tela mural">
      <div class="quadro"><div class="quadro-cab"><b>Contratos</b><span>${d.renova ? `novos cartazes em ${Texto.plural(d.renova, "dia")}` : "cartazes novos amanhã"}</span></div>
        <div class="cartazes">${oferta || '<span class="vazio">O mural está vazio. Volte em alguns dias.</span>'}</div></div>
      <h4>Seus contratos <small>${d.ativos.length}/${d.limite}</small></h4>
      <div class="cartazes seus">${ativos || '<span class="vazio">Nenhum. Pegue um cartaz do mural.</span>'}</div></div>`;
  }
  function ligarMural(raiz, d) {
    // No limite de contratos, aceitar não vai ao jogo: o "não" e o aviso de por quê, perto do clique, a cada tentativa.
    const cheio = d && d.limite && (d.ativos || []).length >= d.limite;
    raiz.querySelectorAll("[data-aceitar]").forEach((b) => b.addEventListener("click", (ev) => {
      ev.stopPropagation();
      if (cheio) { App.som("falha"); App.avisar(`Você já tem ${d.limite} contratos: entregue ou abandone um antes.`, "contratos"); return; }
      App.acao({ aceitar: Number(b.dataset.aceitar) }, "pagina");
    }));
    raiz.querySelectorAll("[data-abandonar]").forEach((b) => b.addEventListener("click", (ev) => { ev.stopPropagation(); App.acao({ abandonar: Number(b.dataset.abandonar) }, "escolha"); }));
  }

  /** Rastreador sempre à vista: alvo, lugar, distância e progresso de cada contrato. */
  /** O rastreador do painel do mundo: a missão da campanha (se houver) e os contratos aceitos. */
  function rastreador(contratos, nivelHeroi, missoes) {
    const linhasMissao = (missoes || []).map((m) => `<div class="rastro-contrato rastro-missao" data-local="${m.lugar_id}" data-missao="${h(m.id)}" title="${h(m.objetivo)}">
        <span class="rastro-arte">${S("pergaminho", 2)}</span>
        <span class="rastro-info"><b>${h(m.nome)}</b><span class="rastro-objetivo">${h(m.objetivo)}</span>
          <span class="rastro-lugar">${h(m.lugar || "")}${m.distancia ? ` · ${Texto.plural(m.distancia, "trecho")}` : m.distancia === 0 ? " · você está aqui" : ""}</span></span></div>`).join("");
    const missao = linhasMissao ? `<div class="secao rastreador"><h3>Missão</h3>${linhasMissao}</div>` : "";
    if (!contratos || !contratos.length) return missao;
    return missao + `<div class="secao rastreador"><h3>Contratos</h3>${contratos.map((c) => {
      const arte = c.tipo === "entrega" ? "saco" : c.retrato || "caveira";
      const alvo = c.tipo === "alvo" ? c.alvo : c.tipo === "entrega" ? `Levar ${c.objeto}` : c.desc.replace(/^Eliminar /, "").replace(/ em .*$/, "");
      let prog = "";
      if (c.tipo === "caca" && c.progresso) { const [f, t] = c.progresso.split("/").map(Number); prog = `${barra("xp", f, t)}<small>${f}/${t}</small>`; }
      const perigo = c.nivel == null ? "" : c.nivel - nivelHeroi >= 2 ? "alto" : c.nivel >= nivelHeroi ? "medio" : "baixo";
      return `<div class="rastro-contrato${c.concluido ? " feito" : ""}" data-local="${c.lugar_id}" data-contrato="${c.id}" title="${h(c.desc)}">
        <span class="rastro-arte">${S(arte, 2)}</span>
        <span class="rastro-info"><b>${h(alvo)}</b>
          <span class="rastro-lugar">${c.concluido ? "Feito! Receba numa vila" : `${h(c.lugar)}${c.distancia ? ` · ${Texto.plural(c.distancia, "trecho")}` : c.distancia === 0 ? " · você está aqui" : ""}`}${c.nivel != null && !c.concluido ? ` <span class="perigo-tag ${perigo}">Nv.${c.nivel}</span>` : ""}</span>
          ${prog ? `<span class="rastro-prog">${prog}</span>` : ""}</span></div>`;
    }).join("")}</div>`;
  }

  Telas.registrar("mural", mural, { ligar: ligarMural, esquecer: () => { contratosVistos = null; } });
  Telas.registrar("diario", diario, { ligar: ligarMural });

  Object.assign(Telas, { cartaz, rastreador });
})();
