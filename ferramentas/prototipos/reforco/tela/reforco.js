/* Protótipo do reforço (roadmapIDEIAS/25, seção 5): a forja (painel "forja_proto", demo.py) e a seção "Materiais" do
   inventário. Só esta demonstração carrega este arquivo; o jogo não.

   O balcão da forja tem três serviços: Reforçar, Desmontar e Encantar (só o lugar, reservado). Cada serviço abre uma
   janela própria sobre a coluna do meio, do tamanho dela, sem rolar a página: no topo, o ouro e os fragmentos sempre
   à vista; à esquerda, as abas e a lista das peças (só a lista rola); à direita, a peça escolhida e, embaixo, o custo
   e o botão, sempre visíveis. Esc fecha a janela e volta ao balcão. Cada pedido é um clique deliberado: o botão trava
   até a forja voltar desenhada, a tecla segurada não repete e a desmontagem pede uma confirmação que nomeia a peça. */
"use strict";

(() => {
  ACOES_OCULTAS.push("forja");  // o pedido à forja não vira botão na página (nucleo.js)
  const { h, S, dicaItem, iconeItem, cartaoServico, topoBalcao } = Telas;

  let janela = null;       // "reforcar", "desmontar" ou null (o balcão)
  let aba = "heroi";       // na janela de reforço: de quem são as peças da lista
  let selUid = null;       // a peça escolhida (sobrevive ao redesenho da forja)
  let confirmando = null;  // {uid, nome}: a desmontagem pedida, esperando a confirmação
  let enviando = false;
  let focoDepois = null;   // o seletor que recebe o foco quando a forja volta desenhada

  const icone = (nome) => Icones.porDesenho(nome) || S(nome, 2);
  const num = (v) => String(v).replace(".", ",");
  const frag = (n) => `${n} ${n === 1 ? "Fragmento" : "Fragmentos"} de Têmpera`;
  const iconeItemHtml = (it) => Icones.equipamento(iconeItem(it)) || S(iconeItem(it), 2);
  const retrato = (a) => (a.retrato ? Icones.cabeca(a.retrato, 32) || S(a.retrato, 2) : Icones.porDesenho("saco") || S("saco", 2));

  // ------------------------------------------------------------------ o balcão
  function balcao(d) {
    const cartoes = [
      cartaoServico({ icone: "martelo", nome: "Reforçar", efeito: "Arma, peito e apoio: ouro e Fragmentos de Têmpera, sem risco.",
        attrs: 'data-servico="reforcar"' }),
      cartaoServico({ icone: "saco", nome: "Desmontar", efeito: "Uma peça da bolsa vira Fragmentos de Têmpera.",
        attrs: 'data-servico="desmontar"' }),
      cartaoServico({ icone: "estrela", nome: "Encantar", efeito: "Ainda não existe: as regras estão em conversa.",
        motivo: "O encantamento ainda não existe neste protótipo.", attrs: 'data-servico="encantar"' }),
    ];
    return `<div class="tela balcao-servico forja forja-proto">${topoBalcao("martelo", "O ferreiro (protótipo)", "\"Ouro e fragmento. Sem sorte: o que eu prometo, a peça ganha.\"", d.ouro)}
      <div class="servicos ref-servicos">${cartoes.join("")}</div>${janela ? janelaHtml(d) : ""}</div>`;
  }

  // ------------------------------------------------------------------ a janela de serviço
  function recursosHtml(d) {
    return `<div class="ref-recursos" aria-label="O que o grupo tem">
      <span class="ref-rec" title="Ouro">${Icones.ouro() || S("moedas", 2)}<b>${d.ouro}</b></span>
      ${d.materiais.map((m) => `<span class="ref-rec" title="${h(m.nome)}: ${h(m.desc)} ${h(m.fontes)}">${icone(m.icone)}<b>${m.qtd}</b><small>${h(m.plural)}</small></span>`).join("")}</div>`;
  }

  function janelaHtml(d) {
    const servicos = [["reforcar", "Reforçar"], ["desmontar", "Desmontar"], ["encantar", "Encantar"]];
    const abasServico = servicos.map(([id, nome]) => `<button type="button" class="ref-aba-servico${id === janela ? " ativa" : ""}" data-janela="${id}"${id === "encantar" ? ' aria-disabled="true" title="O encantamento ainda não existe neste protótipo."' : ""}>${nome}</button>`).join("");
    const corpo = janela === "reforcar" ? reforcoHtml(d) : desmonteHtml(d);
    return `<div class="ref-janela m-janela" role="dialog" aria-modal="true" aria-label="${janela === "reforcar" ? "Reforçar" : "Desmontar"}">
      <header class="ref-cab"><nav class="ref-abas-servico">${abasServico}</nav>${recursosHtml(d)}
        <button type="button" class="ref-fechar" data-fechar title="Voltar ao balcão">Fechar <kbd>Esc</kbd></button></header>
      ${corpo}</div>`;
  }

  /** Uma peça na lista: o ícone, o nome, o reforço e uma linha curta (o estado ou o retorno). */
  function linhaPeca(p, sub) {
    return `<button type="button" class="ref-peca${p.uid === selUid ? " marcada" : ""}${p.sem_reforco && janela === "reforcar" ? " apagada" : ""}" data-uid="${h(p.uid)}" ${dicaItem(p.item, "", false)}>
      <span class="slot-px r-${h(p.item.raridade)}">${iconeItemHtml(p.item)}</span>
      <span class="ref-nome">${h(p.item.nome.replace(/ \+\d+$/, ""))}${p.reforco ? ` <span class="ref-n">+${p.reforco}</span>` : ""}<small>${h(sub)}</small></span></button>`;
  }

  // ------------------------------------------------------------------ Reforçar
  function reforcoHtml(d) {
    const abas = d.abas.map((a) => `<button type="button" role="tab" class="ref-aba${a.id === aba ? " ativa" : ""}" data-aba="${h(a.id)}" aria-selected="${a.id === aba}">${retrato(a)}<span>${h(a.nome)}</span></button>`).join("");
    const lista = d.pecas.filter((p) => p.aba === aba);
    const estado = (p) => (p.sem_reforco ? "sem reforço" : p.no_limite ? `no limite (+${p.limite})` : p.passos[0].motivo ? "falta material" : p.item.bonus);
    const p = lista.find((x) => x.uid === selUid);
    return `<div class="ref-corpo">
      <aside class="ref-lado"><div class="ref-abas" role="tablist" aria-label="De quem">${abas}</div>
        <div class="ref-lista">${lista.map((x) => linhaPeca(x, estado(x))).join("") || '<div class="detalhe-vazio">Nada aqui.</div>'}</div></aside>
      <section class="ref-principal">${p ? reforcoPeca(p) : `<div class="ref-vazio">Escolha uma peça à esquerda.</div>`}</section></div>`;
  }

  function lutaHtml(c, titulo) {
    if (!c || !c.linhas.length) return "";
    return `<div class="ref-luta"><small>${titulo || `Na luta, contra ${h(c.alvo)}`} (dano médio, sem crítico)</small>${c.linhas.map((l) =>
      `<div class="ref-luta-linha"><span>${h(l.rotulo)}</span><b>${num(l.antes)} → <span class="${l.melhor ? "melhor" : "pior"}">${num(l.depois)}</span></b></div>`).join("")}</div>`;
  }

  function reforcoPeca(p) {
    const cab = `<div class="ref-peca-cab"><span class="slot-px r-${h(p.item.raridade)}">${iconeItemHtml(p.item)}</span>
      <div><b class="r-${h(p.item.raridade)}">${h(p.item.nome)}</b><small>${h(p.onde)}${p.reforco ? ` · reforço +${p.reforco} de ${p.limite}${p.veio ? ` (${h(p.veio)})` : ""}` : ` · sem reforço (limite +${p.limite})`}</small>
      <div class="ref-bonus">${h(p.item.bonus)}</div></div></div>`;
    if (p.sem_reforco) return `${cab}<div class="ref-meio"><div class="ref-nota">${h(p.sem_reforco)}</div></div>`;
    if (p.no_limite) return `${cab}<div class="ref-meio"><div class="ref-nota">No limite (+${p.limite}): a forja não tira mais nada dela.</div></div>`;
    const subs = (p.substitutas || []).length ? `<details class="ref-comparar"><summary>Comparar com uma peça da bolsa (${p.substitutas.length})</summary>${p.substitutas.map((s) =>
      lutaHtml(s, `No lugar dela: ${h(s.nome)}`) || `<div class="ref-nota">${h(s.nome)}: não muda o golpe nem a defesa.</div>`).join("")}</details>` : "";
    const passos = p.passos.map((x) => `<div class="ref-passo">
        <div class="ref-passo-cab">${x.rotulo ? `<b>${h(x.rotulo)}</b> · ` : ""}+${p.reforco} → +${p.reforco + 1}</div>
        <div class="ref-antes-depois">${x.linhas.map((l) => `<span>${h(l.nome)} <b>${l.antes} → <span class="melhor">${l.depois}</span></b></span>`).join("")}</div>
        ${lutaHtml(x.luta)}</div>`).join("");
    const rodape = p.passos.map((x, k) => {
      const ouroFalta = x.ouro_tem < x.ouro, fragFalta = x.tem < x.fragmentos;
      return `<div class="ref-acao">
        <span class="ref-custo"><span class="${ouroFalta ? "pior" : ""}">${Icones.moeda() || S("moeda", 1)}${x.ouro} <small>(tem ${x.ouro_tem})</small></span>
          <span class="${fragFalta ? "pior" : ""}">${icone("saco")}${x.fragmentos} <small>(tem ${x.tem})</small></span></span>
        <button type="button" class="acao-peca ref-reforcar${x.motivo ? " bloqueada" : ""}" data-passo="${k}"${x.motivo ? ` aria-disabled="true" title="${h(x.motivo)}"` : ""}>Reforçar${x.rotulo ? ` · ${h(x.rotulo)}` : ""}</button>
        ${x.motivo ? `<span class="pior ref-falta">${h(x.motivo)}</span>` : ""}</div>`;
    }).join("");
    return `${cab}<div class="ref-meio">${passos}${subs}</div><footer class="ref-rodape">${rodape}</footer>`;
  }

  // ------------------------------------------------------------------ Desmontar
  function desmonteHtml(d) {
    const bolsa = d.pecas.filter((p) => !p.quem);
    const rendem = bolsa.filter((p) => !p.desmontar.motivo);
    const fora = bolsa.length - rendem.length;
    const p = rendem.find((x) => x.uid === selUid);
    const retorno = (x) => (x.desmontar.investimento ? `${x.desmontar.total}: ${x.desmontar.investimento} do reforço e ${x.desmontar.da_peca} da peça` : `${x.desmontar.total} da peça`);
    const lista = rendem.map((x) => linhaPeca(x, `rende ${retorno(x)}`)).join("") || '<div class="detalhe-vazio">Nenhuma peça da bolsa rende material.</div>';
    const nota = fora ? `<div class="ref-nota ref-fora">${fora} ${fora === 1 ? "peça da bolsa não rende" : "peças da bolsa não rendem"} material (comuns sem reforço): venda no mercado.</div>` : "";
    let principal = `<div class="ref-vazio">Escolha uma peça da bolsa à esquerda. As vestidas não aparecem: guarde na bolsa antes (Inventário).</div>`;
    if (p) {
      const conf = confirmando && confirmando.uid === p.uid;
      principal = `<div class="ref-peca-cab"><span class="slot-px r-${h(p.item.raridade)}">${iconeItemHtml(p.item)}</span>
          <div><b class="r-${h(p.item.raridade)}">${h(p.item.nome)}</b><small>Bolsa do grupo${p.reforco ? ` · reforço +${p.reforco}` : ""}</small><div class="ref-bonus">${h(p.item.bonus)}</div></div></div>
        <div class="ref-meio"><div class="ref-retorno">${icone("saco")}<span>Rende <b>${frag(p.desmontar.total)}</b>${p.desmontar.investimento ? ` (${p.desmontar.investimento} do reforço, ${p.desmontar.da_peca} da peça)` : ""}.</span></div>
          <div class="ref-nota">A peça some. No mercado, ela vende por ${p.venda} de ouro.</div></div>
        <footer class="ref-rodape"><div class="ref-acao">${conf
          ? `<span class="ref-pergunta">Desmontar <b>${h(p.item.nome)}</b>?</span>
             <button type="button" class="acao-peca perigo" data-desmontar-sim disabled>Desmontar</button>
             <button type="button" class="acao-peca" data-desmontar-nao>Cancelar</button>`
          : `<button type="button" class="acao-peca" data-desmontar>Desmontar…</button>`}</div></footer>`;
    }
    return `<div class="ref-corpo"><aside class="ref-lado"><div class="ref-lista">${lista}</div>${nota}</aside>
      <section class="ref-principal">${principal}</section></div>`;
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
    const jan = document.querySelector(".ref-janela");
    const cena = document.getElementById("cena");
    if (!jan || !cena) return;
    const r = cena.getBoundingClientRect();
    Object.assign(jan.style, { left: `${r.left + 8}px`, top: `${r.top + 8}px`, width: `${r.width - 16}px`, height: `${r.height - 16}px` });
  }
  window.addEventListener("resize", posicionar);

  function ligar(raiz, d) {
    enviando = false;
    const redesenhar = (foco) => {
      if (!raiz.isConnected) return;
      const novo = Telas.painel({ tipo: "forja_proto", dados: d });
      raiz.replaceWith(novo);
      const alvo = foco && novo.querySelector(foco);
      if (alvo) alvo.focus();
    };
    const abrir = (qual, foco) => { janela = qual; selUid = null; confirmando = null; redesenhar(foco || ".ref-janela .ref-peca, .ref-janela [data-fechar]"); };
    const fechar = () => { const era = janela; janela = null; confirmando = null; redesenhar(`[data-servico="${era}"]`); };
    raiz.querySelectorAll("[data-servico]").forEach((b) => b.addEventListener("click", () => {
      if (b.classList.contains("caro")) { App.recusar(b, b.dataset.motivo); return; }
      abrir(b.dataset.servico);
    }));
    const jan = raiz.querySelector(".ref-janela");
    if (!jan) return;
    requestAnimationFrame(posicionar);
    posicionar();
    jan.querySelector("[data-fechar]").addEventListener("click", fechar);
    jan.querySelectorAll("[data-janela]").forEach((b) => b.addEventListener("click", () => {
      if (b.getAttribute("aria-disabled")) { App.recusar(b, b.title); return; }
      if (b.dataset.janela !== janela) abrir(b.dataset.janela, `[data-janela="${b.dataset.janela}"]`);
    }));
    jan.querySelectorAll("[data-aba]").forEach((b) => b.addEventListener("click", () => {
      if (aba !== b.dataset.aba) { aba = b.dataset.aba; selUid = null; redesenhar(`[data-aba="${b.dataset.aba}"]`); }
    }));
    jan.querySelectorAll("[data-uid]").forEach((b) => b.addEventListener("click", () => {
      if (selUid !== b.dataset.uid) { selUid = b.dataset.uid; confirmando = null; redesenhar(`[data-uid="${b.dataset.uid}"]`); }
    }));
    const p = d.pecas.find((x) => x.uid === selUid);
    jan.querySelectorAll("[data-passo]").forEach((b) => b.addEventListener("click", (ev) => {
      if (ev.detail > 1) return;  // o segundo clique de um duplo clique não compra outro passo
      const x = p.passos[Number(b.dataset.passo)];
      if (x.motivo) { App.recusar(b, x.motivo); return; }
      pedir({ op: "reforcar", uid: p.uid, ...(x.veio ? { veio: x.veio } : {}) }, b, `[data-uid="${p.uid}"]`);
    }));
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
        pedir({ op: "desmontar", uid: c.uid, nome: c.nome, confirmar: true }, sim, ".ref-janela .ref-peca, .ref-janela [data-fechar]");
      });
    }
    jan.addEventListener("keydown", (ev) => {
      if (ev.repeat && (ev.key === "Enter" || ev.key === " ")) ev.preventDefault();  // a tecla segurada não repete
    }, true);
    if (focoDepois) {
      const alvo = jan.querySelector(focoDepois);
      focoDepois = null;
      if (alvo) requestAnimationFrame(() => alvo.isConnected && alvo.focus());
    }
  }

  // Esc com a janela aberta: primeiro cancela a confirmação, depois fecha a janela; só então o Voltar da forja.
  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape" || !janela || !document.querySelector(".ref-janela")) return;
    ev.preventDefault();
    ev.stopImmediatePropagation();
    if (confirmando) { document.querySelector("[data-desmontar-nao]")?.click(); return; }
    document.querySelector(".ref-janela [data-fechar]")?.click();
  }, true);

  Telas.registrar("forja_proto", balcao, { ligar, esquecer: () => { janela = null; selUid = null; confirmando = null; aba = "heroi"; } });

  /* A seção "Materiais" no inventário: as pilhas do grupo, fora dos espaços da bolsa. */
  function materiaisNoInventario() {
    const lado = document.querySelector(".tela.inventario .inv-lado");
    const mats = App.estado && App.estado.heroi && App.estado.heroi.materiais;
    if (!lado || !mats || lado.querySelector(".ref-mat-inv")) return;
    const bolsa = [...lado.querySelectorAll("h4")].find((x) => /^Bolsa$/.test(x.textContent.trim()));
    const slots = bolsa && bolsa.nextElementSibling;
    if (!slots) return;
    const html = `<h4>Materiais <small>não ocupam a bolsa</small></h4><div class="slots ref-mat-inv">${mats.map((m) =>
      `<div class="slot-px" tabindex="0" ${Telas.dica(`<b>${h(m.nome)}</b><div>${h(m.desc)}</div><div class="rodape">${h(m.fontes)}</div>`)}>${icone(m.icone)}<span class="qtd">${m.qtd}</span></div>`).join("")}</div>`;
    slots.insertAdjacentHTML("afterend", html);
    Telas.ligarDicas(lado.querySelector(".ref-mat-inv"));
  }
  new MutationObserver(materiaisNoInventario).observe(document.body, { childList: true, subtree: true });
})();
