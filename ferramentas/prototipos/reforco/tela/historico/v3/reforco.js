/* Protótipo do reforço, 3ª versão (roadmapIDEIAS/25, seção 5): a forja (painel "forja_proto", demo.py) com duas
   direções de tela para o mesmo serviço, e a seção "Materiais" do inventário. Só esta demonstração carrega este
   arquivo; o jogo não. As versões anteriores ficam em historico/ (a faixa da demonstração abre cada uma).

   A estrutura da 2ª versão continua: o balcão com os serviços (Reforçar, Desmontar) e uma janela por serviço sobre a
   coluna do meio, sem rolar a página; ouro, materiais e a ação sempre à vista; Esc fecha. Muda a composição:
     A · Bancada   a peça num encaixe no centro da bancada, o passo e os materiais em volta dela, a escolha das peças
                   numa esteira embaixo e os donos ao lado; a ficha completa à direita
     B · Arsenal   as peças de todos numa grade por dono, com o reforço no canto de cada uma; uma ficha compacta ao lado
                   com as propriedades, o passo, o custo e a ação
   A comparação contra o Esqueleto de teste fica numa área fechada e marcada "teste", fora do caminho do serviço. */
"use strict";

(() => {
  ACOES_OCULTAS.push("forja");  // o pedido à forja não vira botão na página (nucleo.js)
  const { h, S, dicaItem, iconeItem, cartaoServico, topoBalcao } = Telas;

  const ler = (k, padrao) => { try { return localStorage.getItem(k) || padrao; } catch (e) { return padrao; } };
  let direcao = ler("reforco-direcao", "A");
  let janela = null;       // "reforcar", "desmontar" ou null (o balcão)
  let aba = "heroi";       // de quem são as peças na esteira (A)
  let selUid = null;       // a peça escolhida (sobrevive ao redesenho da forja)
  const veioSel = {};      // a arma do Guerreiro sem veio: o caminho escolhido antes do primeiro reforço
  let confirmando = null;  // {uid, nome}: a desmontagem pedida, esperando a confirmação
  let enviando = false;
  let focoDepois = null;   // o seletor que recebe o foco quando a forja volta desenhada
  let ultimo = null;       // o último desenho (raiz e dados), para a faixa trocar de direção na hora

  const iconeDe = (nome, lado = 32) => Icones.porDesenho(nome, lado) || S(nome, 2);
  const moeda = () => Icones.moeda() || S("moeda", 1);
  const num = (v) => String(v).replace(".", ",");
  const plural = (n, um, varios) => `${n} ${n === 1 ? um : varios}`;
  const iconePeca = (it) => Icones.equipamento(iconeItem(it)) || S(iconeItem(it), 2);
  const retrato = (a) => (a.retrato ? Icones.cabeca(a.retrato, 32) || S(a.retrato, 2) : iconeDe("saco"));
  const valor = (pr, v) => (pr.pct ? `${v}%` : `${v}`);

  // ------------------------------------------------------------------ peças comuns às duas direções
  /** ◆◆◇◇: o reforço de agora no limite. */
  function marcas(p) {
    return `<span class="rf-marcas" aria-label="Reforço +${p.reforco} de ${p.limite}">${Array.from({ length: p.limite }, (_, i) =>
      `<i class="${i < p.reforco ? "cheia" : ""}"></i>`).join("")}</span>`;
  }
  /** O passo de agora: o do veio escolhido (a arma do Guerreiro sem veio pede a escolha) ou o único. */
  function passoDe(p) {
    if (!p.passos) return null;
    if (p.passos.length === 1) return p.passos[0];
    return p.passos.find((x) => x.veio === veioSel[p.uid]) || null;
  }
  /** Todas as propriedades da peça; nas que crescem com o reforço, o valor seguinte. */
  function propriedadesHtml(p, passo) {
    const depois = {};
    (passo ? passo.linhas : []).forEach((l) => { depois[l.nome] = l.depois; });
    const linhas = p.propriedades.map((pr) => {
      const vai = depois[pr.nome];
      return `<li class="${pr.cresce ? "cresce" : ""}"><span>${h(pr.nome)}</span><b>${valor(pr, pr.valor)}${vai !== undefined ? ` → <em>${valor(pr, vai)}</em>` : ""}</b></li>`;
    });
    // o Poder das Runas ainda não está na peça: a linha nova aparece com o valor seguinte
    (passo ? passo.linhas : []).filter((l) => !p.propriedades.some((pr) => pr.nome === l.nome))
      .forEach((l) => linhas.push(`<li class="cresce nova"><span>${h(l.nome)}</span><b>0 → <em>${l.depois}</em></b></li>`));
    return `<ul class="rf-props">${linhas.join("")}</ul>${p.efeito ? `<p class="rf-efeito">${h(p.efeito)}</p>` : ""}`;
  }
  /** Os ganhos do passo, em linha: "Ataque 4 → 5". */
  function ganhoHtml(passo) {
    return passo.linhas.map((l) => `<span class="rf-ganho">${h(l.nome)} <b>${l.antes} → <em>${l.depois}</em></b></span>`).join("");
  }
  /** O custo: cada recurso com o ícone, o custo e o que o grupo tem, com o rótulo de cada número. */
  function custoHtml(passo) {
    const linha = (ic, nome, custo, tem) => `<div class="rf-custo-linha${tem < custo ? " falta" : ""}">
      <span class="rf-encaixe pequeno">${ic}</span><span class="rf-custo-nome">${h(nome)}</span>
      <span class="rf-rot">Custo</span><b>${custo}</b><span class="rf-rot">Tem</span><b>${tem}</b></div>`;
    return `<div class="rf-custo">${linha(moeda(), "Ouro", passo.ouro, passo.ouro_tem)}${linha(iconeDe("saco"), "Fragmentos", passo.fragmentos, passo.tem)}</div>`;
  }
  /** A arma do Guerreiro antes do primeiro reforço: Fio ou Runas, cada um com o que dá. */
  function veioHtml(p) {
    if (!p.passos || p.passos.length < 2) return "";
    return `<div class="rf-veios" role="radiogroup" aria-label="Caminho da arma">${p.passos.map((x) => `<button type="button" role="radio" class="rf-veio${veioSel[p.uid] === x.veio ? " escolhido" : ""}" data-veio="${x.veio}" aria-checked="${veioSel[p.uid] === x.veio}">
      <b>${h(x.rotulo)}</b><span>${x.linhas.map((l) => `${h(l.nome)} ${l.antes} → <em>${l.depois}</em>`).join(", ")}</span></button>`).join("")}</div>`;
  }
  /** A ação principal e o motivo curto quando não dá. */
  function acaoReforco(p, passo) {
    let motivo = p.sem_reforco || (p.no_limite ? "No limite" : null);
    if (!motivo && !passo) motivo = "Escolha Fio ou Runas";
    if (!motivo && passo.motivo) motivo = passo.motivo;
    const rotulo = p.no_limite ? "No limite" : "Reforçar";
    return `<div class="rf-acao"><button type="button" class="rf-botao principal" data-reforcar${motivo ? ` aria-disabled="true" title="${h(motivo)}"` : ""}>${rotulo}</button>
      ${motivo && !p.no_limite ? `<span class="rf-falta">${h(motivo)}</span>` : ""}</div>`;
  }
  /** A comparação contra o alvo de teste e as substitutas: fechada, marcada "teste". */
  function testeHtml(p, passo) {
    const linhas = (c, titulo) => (c && c.linhas.length ? `<div class="rf-teste-bloco"><small>${titulo}</small>${c.linhas.map((l) =>
      `<div class="rf-teste-linha"><span>${h(l.rotulo)}</span><b>${num(l.antes)} → <em class="${l.melhor ? "melhor" : "pior"}">${num(l.depois)}</em></b></div>`).join("")}</div>` : "");
    const blocos = [passo && linhas(passo.luta, "Este reforço"),
      ...(p.substitutas || []).map((s) => linhas(s, `No lugar: ${h(s.nome)}`)),
      ...(p.trocas || []).map((t) => linhas(t, `${h(t.quem)} veste${t.no_lugar ? ` no lugar de ${h(t.no_lugar)}` : ""}`))].filter(Boolean);
    if (!blocos.length) return "";
    const alvo = (passo && passo.luta) || (p.substitutas || [])[0] || (p.trocas || [])[0];
    return `<details class="rf-teste"><summary><span class="rf-selo">teste</span> Comparação · ${h(alvo.alvo)}</summary>
      <p class="rf-teste-nota">Dano médio, sem crítico.</p>${blocos.join("")}</details>`;
  }
  /** Desmontar: o que volta, o aviso curto e a ação (ou a confirmação). */
  function desmonteAcao(p) {
    if (confirmando && confirmando.uid === p.uid) {
      return `<div class="rf-confirmar" role="alertdialog" aria-label="Confirmar a desmontagem"><span>Desmontar <b>${h(p.item.nome)}</b>? <em class="rf-aviso">A peça é destruída.</em></span>
        <button type="button" class="rf-botao perigo" data-desmontar-sim disabled>Confirmar</button>
        <button type="button" class="rf-botao" data-desmontar-nao>Cancelar</button></div>`;
    }
    return `<div class="rf-acao"><button type="button" class="rf-botao perigo" data-desmontar>Desmontar</button><span class="rf-aviso">Destrói a peça.</span></div>`;
  }
  function recebeHtml(p) {
    const d = p.desmontar;
    return `<div class="rf-recebe"><span class="rf-encaixe">${iconeDe("saco")}<b class="rf-qtd">+${d.total}</b></span>
      <div><span class="rf-rot">Recebe</span><b>${plural(d.total, "Fragmento de Têmpera", "Fragmentos de Têmpera")}</b>
      ${d.investimento ? `<small>${d.investimento} do reforço · ${d.da_peca} da peça</small>` : ""}</div></div>`;
  }
  const venda = (p) => (p.venda !== undefined ? `<div class="rf-venda">Venda: ${moeda()} ${p.venda}</div>` : "");
  const dono = (p) => (p.quem ? `Com ${p.onde}` : "Bolsa do grupo");

  /** Um encaixe de peça (a esteira de A, a grade de B): o ícone na raridade, o +N no canto e a marca da seleção. */
  function encaixe(p, extra = "", selo = "") {
    const apagada = janela === "reforcar" ? !!p.sem_reforco : !!p.desmontar.motivo;
    const canto = selo || (p.reforco ? `+${p.reforco}` : "");
    return `<button type="button" class="rf-peca r-${h(p.item.raridade)}${p.uid === selUid ? " marcada" : ""}${apagada ? " apagada" : ""}" data-uid="${h(p.uid)}"
      aria-label="${h(p.item.nome)}" aria-pressed="${p.uid === selUid}" ${dicaItem(p.item, "", false)}>${iconePeca(p.item)}${canto ? `<span class="rf-canto">${h(canto)}</span>` : ""}${extra}</button>`;
  }

  // ------------------------------------------------------------------ o balcão
  function balcao(d) {
    const cartoes = [
      cartaoServico({ icone: "martelo", nome: "Reforçar", efeito: "Arma, peito e apoio", attrs: 'data-servico="reforcar"' }),
      cartaoServico({ icone: "saco", nome: "Desmontar", efeito: "Peças da bolsa → Fragmentos de Têmpera", attrs: 'data-servico="desmontar"' }),
    ];
    return `<div class="tela balcao-servico forja forja-proto">${topoBalcao("martelo", "O ferreiro", "Um homem sem dois dedos cospe na forja. \"Ouro primeiro.\"", d.ouro)}
      <div class="servicos rf-servicos">${cartoes.join("")}</div>${janela ? janelaHtml(d) : ""}</div>`;
  }

  // ------------------------------------------------------------------ a janela
  function janelaHtml(d) {
    const abas = [["reforcar", "Reforçar"], ["desmontar", "Desmontar"]].map(([id, nome]) =>
      `<button type="button" role="tab" class="rf-servico${id === janela ? " ativo" : ""}" data-janela="${id}" aria-selected="${id === janela}">${nome}</button>`).join("");
    const recursos = `<div class="rf-recursos"><span class="rf-rec" title="Ouro">${Icones.ouro() || S("moedas", 2)}<b>${d.ouro}</b></span>
      ${d.materiais.map((m) => `<span class="rf-rec" title="${h(m.nome)}">${iconeDe(m.icone)}<b>${m.qtd}</b><small>${h(m.plural)}</small></span>`).join("")}</div>`;
    const corpo = direcao === "A" ? bancada(d) : arsenal(d);
    return `<div class="rf-janela m-janela rf-${direcao}" role="dialog" aria-modal="true" aria-label="${janela === "reforcar" ? "Reforçar" : "Desmontar"}">
      <header class="rf-cab"><nav class="rf-servicos-abas" role="tablist">${abas}</nav>${recursos}
        <button type="button" class="rf-botao fechar" data-fechar>Fechar <kbd>Esc</kbd></button></header>${corpo}</div>`;
  }

  // ------------------------------------------------------------------ A · Bancada
  function bancada(d) {
    const reforco = janela === "reforcar";
    const lista = d.pecas.filter((p) => (reforco ? p.aba === aba : !p.quem));
    const p = lista.find((x) => x.uid === selUid);
    // os donos ao lado; desmontar é só da bolsa: a coluna mostra só ela (a grade da janela não muda)
    const donos = `<nav class="rf-donos" role="tablist" aria-label="De quem">${d.abas.filter((a) => reforco || a.id === "bolsa").map((a) => {
      const ativo = reforco ? a.id === aba : true;
      const n = d.pecas.filter((x) => (reforco ? x.aba === a.id : !x.quem)).length;
      return `<button type="button" role="tab" class="rf-dono${ativo ? " ativo" : ""}"${reforco ? ` data-aba="${h(a.id)}"` : ""} aria-selected="${ativo}" title="${h(a.nome)}">${retrato(a)}<span>${h(a.nome)}</span><small>${n}</small></button>`;
    }).join("")}</nav>`;
    const esteira = lista.map((x) => encaixe(x, "", reforco ? "" : (x.desmontar.motivo ? "—" : `◆${x.desmontar.total}`))).join("")
      || `<span class="rf-vazio-texto">${reforco ? "Nada aqui." : "Nenhuma peça da bolsa rende material."}</span>`;
    let centro, lado;
    if (!p) {
      centro = `<div class="rf-mesa"><div class="rf-encaixe grande vazio"></div><p class="rf-vazio-texto">Escolha uma peça</p></div>`;
      lado = "";
    } else if (reforco) {
      const passo = passoDe(p);
      centro = `<div class="rf-mesa">
          <div class="rf-nivel">${p.no_limite ? `+${p.reforco} · limite` : `+${p.reforco} → +${p.reforco + 1}`}</div>
          <div class="rf-encaixe grande r-${h(p.item.raridade)}">${iconePeca(p.item)}</div>${marcas(p)}
          ${veioHtml(p)}
          <div class="rf-ganhos">${passo && p.passos.length === 1 ? ganhoHtml(passo) : p.sem_reforco ? `<span class="rf-nota">${h(p.sem_reforco)}</span>` : p.no_limite ? `<span class="rf-nota">No limite (+${p.limite})</span>` : ""}</div>
          ${p.passos ? custoHtml(passo || p.passos[0]) : ""}${acaoReforco(p, passo)}</div>`;
      lado = fichaLado(p, passo);
    } else {
      centro = `<div class="rf-mesa desmonte">
          <div class="rf-linha-desmonte"><div class="rf-encaixe grande r-${h(p.item.raridade)}">${iconePeca(p.item)}</div><span class="rf-seta">→</span>${recebeHtml(p)}</div>
          ${desmonteAcao(p)}</div>`;
      lado = fichaLado(p, null);
    }
    return `<div class="rf-corpo">${donos}<section class="rf-centro">${centro}
        <div class="rf-esteira" role="listbox" aria-label="Peças">${esteira}</div></section>
      <aside class="rf-ficha">${lado || '<p class="rf-vazio-texto">—</p>'}</aside></div>`;
  }
  /** A ficha completa à direita (A): nome, dono, propriedades, venda, comparação de teste. */
  function fichaLado(p, passo) {
    return `<div class="rf-ficha-cab"><b class="r-${h(p.item.raridade)}">${h(p.item.nome)}</b><small>${h(dono(p))}${p.veio ? ` · ${h(p.veio)}` : ""}</small></div>
      <div class="rf-ficha-meio">${propriedadesHtml(p, passo)}${venda(p)}</div>${testeHtml(p, passo)}`;
  }

  // ------------------------------------------------------------------ B · Arsenal
  function arsenal(d) {
    const reforco = janela === "reforcar";
    const grupos = (reforco ? d.abas : d.abas.filter((a) => a.id === "bolsa")).map((a) => {
      const ps = d.pecas.filter((x) => (reforco ? x.aba === a.id : !x.quem));
      if (!ps.length) return "";
      return `<section class="rf-grupo"><h5>${retrato(a)}<span>${h(a.nome)}</span></h5><div class="rf-grade">${ps.map((x) =>
        encaixe(x, "", reforco ? "" : (x.desmontar.motivo ? "—" : `◆${x.desmontar.total}`))).join("")}</div></section>`;
    }).join("");
    const p = d.pecas.find((x) => x.uid === selUid && (reforco || !x.quem));
    let ficha = `<p class="rf-vazio-texto">Escolha uma peça</p>`;
    if (p && reforco) {
      const passo = passoDe(p);
      ficha = `<div class="rf-ficha-cab"><span class="rf-encaixe r-${h(p.item.raridade)}">${iconePeca(p.item)}</span>
          <div><b class="r-${h(p.item.raridade)}">${h(p.item.nome)}</b><small>${h(dono(p))}</small>${marcas(p)}</div></div>
        <div class="rf-ficha-meio">
          <div class="rf-nivel">${p.no_limite ? `+${p.reforco} · limite` : p.sem_reforco ? "Sem reforço" : `+${p.reforco} → +${p.reforco + 1}`}</div>
          ${veioHtml(p)}${propriedadesHtml(p, passo)}${p.sem_reforco ? `<p class="rf-nota">${h(p.sem_reforco)}</p>` : ""}${venda(p)}
          ${testeHtml(p, passo)}</div>
        <footer class="rf-ficha-pe">${p.passos ? custoHtml(passo || p.passos[0]) : ""}${acaoReforco(p, passo)}</footer>`;
    } else if (p) {
      ficha = `<div class="rf-ficha-cab"><span class="rf-encaixe r-${h(p.item.raridade)}">${iconePeca(p.item)}</span>
          <div><b class="r-${h(p.item.raridade)}">${h(p.item.nome)}</b><small>${h(dono(p))}${p.reforco ? ` · +${p.reforco}` : ""}</small></div></div>
        <div class="rf-ficha-meio">${propriedadesHtml(p, null)}${venda(p)}</div>
        <footer class="rf-ficha-pe">${recebeHtml(p)}${desmonteAcao(p)}</footer>`;
    }
    const nenhuma = !reforco && !d.pecas.some((x) => !x.quem) ? '<p class="rf-vazio-texto">A bolsa está vazia.</p>' : "";
    return `<div class="rf-corpo"><section class="rf-arsenal" aria-label="Peças">${grupos}${nenhuma}</section><aside class="rf-ficha">${ficha}</aside></div>`;
  }

  // ------------------------------------------------------------------ ligar
  function pedir(dados, botao, foco) {
    if (enviando) return;
    if (!App.acao({ forja: true }, dados.op === "reforcar" ? "predio_ferreiro" : null, dados)) {
      aviso("Agora não dá para pedir à forja.", "info", "pergaminho");
      return;
    }
    enviando = true;
    focoDepois = foco || null;
    if (botao) botao.disabled = true;
  }

  /** A janela ocupa a coluna do meio (a cena e a página), por cima do balcão: medida a cada desenho e a cada mudança
   *  de tamanho da janela do navegador. */
  function posicionar() {
    const jan = document.querySelector(".rf-janela");
    const cena = document.getElementById("cena");
    if (!jan || !cena) return;
    const r = cena.getBoundingClientRect();
    Object.assign(jan.style, { left: `${r.left + 8}px`, top: `${r.top + 8}px`, width: `${r.width - 16}px`, height: `${r.height - 16}px` });
  }
  window.addEventListener("resize", posicionar);

  function ligar(raiz, d) {
    enviando = false;
    ultimo = { raiz, d };
    const redesenhar = (foco) => {
      if (!raiz.isConnected) return;
      const novo = Telas.painel({ tipo: "forja_proto", dados: d });
      raiz.replaceWith(novo);
      // a primeira opção da lista dada (as listas "a, b" pegam a primeira que existir, não a primeira do documento)
      const alvo = foco && foco.split(",").map((x) => novo.querySelector(x.trim())).find(Boolean);
      if (alvo) alvo.focus();
    };
    const abrir = (qual, foco) => { janela = qual; selUid = null; confirmando = null; redesenhar(foco || ".rf-janela .rf-peca, .rf-janela [data-fechar]"); };
    const fechar = () => { const era = janela; janela = null; confirmando = null; redesenhar(`[data-servico="${era}"]`); };
    raiz.querySelectorAll("[data-servico]").forEach((b) => b.addEventListener("click", () => abrir(b.dataset.servico)));
    const jan = raiz.querySelector(".rf-janela");
    if (!jan) return;
    requestAnimationFrame(posicionar);
    posicionar();
    jan.querySelector("[data-fechar]").addEventListener("click", fechar);
    jan.querySelectorAll("[data-janela]").forEach((b) => b.addEventListener("click", () => {
      if (b.dataset.janela !== janela) abrir(b.dataset.janela, `[data-janela="${b.dataset.janela}"]`);
    }));
    jan.querySelectorAll("[data-aba]").forEach((b) => b.addEventListener("click", () => {
      if (aba !== b.dataset.aba) { aba = b.dataset.aba; selUid = null; redesenhar(`[data-aba="${b.dataset.aba}"]`); }
    }));
    jan.querySelectorAll("[data-uid]").forEach((b) => b.addEventListener("click", () => {
      if (selUid !== b.dataset.uid) { selUid = b.dataset.uid; confirmando = null; redesenhar(`[data-uid="${b.dataset.uid}"]`); }
    }));
    // as setas andam entre as peças (a esteira e a grade); Enter ou Espaço escolhe
    jan.addEventListener("keydown", (ev) => {
      if (!["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"].includes(ev.key) || !ev.target.matches("[data-uid]")) return;
      const todas = [...jan.querySelectorAll("[data-uid]")];
      const i = todas.indexOf(ev.target);
      const passo = ev.key === "ArrowLeft" || ev.key === "ArrowUp" ? -1 : 1;
      ev.preventDefault();
      todas[(i + passo + todas.length) % todas.length].focus();
    });
    const p = d.pecas.find((x) => x.uid === selUid);
    jan.querySelectorAll("[data-veio]").forEach((b) => b.addEventListener("click", () => {
      veioSel[p.uid] = b.dataset.veio;
      redesenhar(`[data-veio="${b.dataset.veio}"]`);
    }));
    const ref = jan.querySelector("[data-reforcar]");
    if (ref) ref.addEventListener("click", (ev) => {
      if (ev.detail > 1) return;  // o segundo clique de um duplo clique não compra outro passo
      if (ref.getAttribute("aria-disabled")) { App.recusar(ref, ref.title); return; }
      const x = passoDe(p);
      pedir({ op: "reforcar", uid: p.uid, ...(x.veio ? { veio: x.veio } : {}) }, ref, "[data-reforcar]");
    });
    const des = jan.querySelector("[data-desmontar]");
    if (des) des.addEventListener("click", () => { confirmando = { uid: p.uid, nome: p.item.nome }; redesenhar("[data-desmontar-nao]"); });
    const nao = jan.querySelector("[data-desmontar-nao]");
    if (nao) nao.addEventListener("click", () => { confirmando = null; redesenhar("[data-desmontar]"); });
    const sim = jan.querySelector("[data-desmontar-sim]");
    if (sim) {
      // a confirmação só arma depois de um instante: o clique que abriu a pergunta não a responde
      const arma = performance.now() + 400;
      setTimeout(() => { if (sim.isConnected) sim.disabled = false; }, 400);
      sim.addEventListener("click", (ev) => {
        if (sim.disabled || performance.now() < arma || ev.detail > 1 || !confirmando) return;
        const c = confirmando;
        confirmando = null;
        selUid = null;
        pedir({ op: "desmontar", uid: c.uid, nome: c.nome, confirmar: true }, sim, ".rf-janela .rf-peca, .rf-janela [data-fechar]");
      });
    }
    jan.addEventListener("keydown", (ev) => {
      if (ev.repeat && (ev.key === "Enter" || ev.key === " ")) ev.preventDefault();  // a tecla segurada não repete
    }, true);
    if (focoDepois) {
      const alvo = focoDepois.split(",").map((x) => jan.querySelector(x.trim())).find(Boolean);
      focoDepois = null;
      if (alvo) requestAnimationFrame(() => alvo.isConnected && alvo.focus());
    }
  }

  // Tab e Shift+Tab ficam dentro da janela aberta (ela é um diálogo: a oficina e a página atrás não recebem o foco)
  document.addEventListener("keydown", (ev) => {
    const jan = document.querySelector(".rf-janela");
    if (ev.key !== "Tab" || !janela || !jan) return;
    const focaveis = [...jan.querySelectorAll("button:not([disabled]), summary, [tabindex]:not([tabindex='-1'])")]
      .filter((el) => el.offsetParent !== null);
    if (!focaveis.length) return;
    const i = focaveis.indexOf(document.activeElement);
    ev.preventDefault();
    const prox = i < 0 ? 0 : (i + (ev.shiftKey ? -1 : 1) + focaveis.length) % focaveis.length;
    focaveis[prox].focus();
  }, true);

  // Esc com a janela aberta: primeiro cancela a confirmação, depois fecha a janela; só então o Voltar da forja.
  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape" || !janela || !document.querySelector(".rf-janela")) return;
    ev.preventDefault();
    ev.stopImmediatePropagation();
    if (confirmando) { document.querySelector("[data-desmontar-nao]")?.click(); return; }
    document.querySelector(".rf-janela [data-fechar]")?.click();
  }, true);

  Telas.registrar("forja_proto", balcao, { ligar, esquecer: () => { janela = null; selUid = null; confirmando = null; aba = "heroi"; } });

  // a faixa da demonstração troca a direção na hora (carregar.js)
  window.ReforcoProto = {
    direcao(nova) {
      if (!nova) return direcao;
      direcao = nova;
      try { localStorage.setItem("reforco-direcao", nova); } catch (e) { /* sem armazenamento: vale até recarregar */ }
      const antes = ultimo && ultimo.raiz;  // o desenho novo troca `ultimo`: guardar o de agora antes
      if (antes && antes.isConnected) antes.replaceWith(Telas.painel({ tipo: "forja_proto", dados: ultimo.d }));
      return direcao;
    },
  };

  /* A seção "Materiais" no inventário: as pilhas do grupo, fora dos espaços da bolsa. */
  function materiaisNoInventario() {
    const lado = document.querySelector(".tela.inventario .inv-lado");
    const mats = App.estado && App.estado.heroi && App.estado.heroi.materiais;
    if (!lado || !mats || lado.querySelector(".ref-mat-inv")) return;
    const bolsa = [...lado.querySelectorAll("h4")].find((x) => /^Bolsa$/.test(x.textContent.trim()));
    const slots = bolsa && bolsa.nextElementSibling;
    if (!slots) return;
    const html = `<h4>Materiais <small>não ocupam a bolsa</small></h4><div class="slots ref-mat-inv">${mats.map((m) =>
      `<div class="slot-px" tabindex="0" ${Telas.dica(`<b>${h(m.nome)}</b><div>${h(m.desc)}</div><div class="rodape">${h(m.fontes)}</div>`)}>${iconeDe(m.icone)}<span class="qtd">${m.qtd}</span></div>`).join("")}</div>`;
    slots.insertAdjacentHTML("afterend", html);
    Telas.ligarDicas(lado.querySelector(".ref-mat-inv"));
  }
  new MutationObserver(materiaisNoInventario).observe(document.body, { childList: true, subtree: true });
})();
