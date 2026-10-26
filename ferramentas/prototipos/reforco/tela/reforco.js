/* Protótipo do reforço, 4ª versão (roadmapIDEIAS/25, seção 5): a direção A · Bancada, escolhida, refinada. A forja
   (painel "forja_proto", demo.py) e a seção "Materiais" do inventário. Só esta demonstração carrega este arquivo; o
   jogo não. As versões anteriores ficam em historico/ (a v3 tem a A anterior e a B; a faixa da demonstração abre cada
   uma).

   A janela por serviço continua (Reforçar, Desmontar; sem rolar a página; ouro e Fragmentos no topo; Esc fecha). No
   centro, uma chapa de ferro rebitada é a bancada: os materiais à esquerda, a peça num suporte no meio, o resultado à
   direita, ligados por um conduto, e a ação no pé da chapa. A ficha à direita tem o nome, o dono e as propriedades
   completas; a que o reforço muda vem destacada pelo valor. O reforço feito acende a peça, a marca nova e o valor por
   um instante (com movimento reduzido, a marca e o valor ficam destacados sem animar). */
"use strict";

(() => {
  ACOES_OCULTAS.push("forja");  // o pedido à forja não vira botão na página (nucleo.js)
  const { h, S, dicaItem, iconeItem, cartaoServico, topoBalcao } = Telas;

  let janela = null;       // "reforcar", "desmontar" ou null (o balcão)
  let aba = "heroi";       // de quem são as peças na esteira
  let selUid = null;       // a peça escolhida (sobrevive ao redesenho da forja)
  const veioSel = {};      // a arma do Guerreiro sem veio: o caminho escolhido antes do primeiro reforço
  let confirmando = null;  // {uid, nome}: a desmontagem pedida, esperando a confirmação
  let enviando = false;
  let focoDepois = null;   // o seletor que recebe o foco quando a forja volta desenhada
  let recem = null;        // {uid, reforco, nomes}: o reforço que acabou de acontecer (o retorno visual)

  const iconeDe = (nome) => Icones.porDesenho(nome) || S(nome, 2);
  const moeda = () => Icones.moeda() || S("moeda", 1);
  const num = (v) => String(v).replace(".", ",");
  const plural = (n, um, varios) => `${n} ${n === 1 ? um : varios}`;
  const iconePeca = (it) => Icones.equipamento(iconeItem(it)) || S(iconeItem(it), 2);
  const retrato = (a) => (a.retrato ? Icones.cabeca(a.retrato, 32) || S(a.retrato, 2) : iconeDe("saco"));
  const valor = (pr, v) => (pr.pct ? `${v}%` : `${v}`);
  const dono = (p) => (p.quem ? `Com ${p.onde}` : "Bolsa do grupo");
  // o reforço acabou de acontecer nesta peça: ela voltou do motor com o nível acima do que tinha no clique
  const acabou = (p) => !!(recem && p && recem.uid === p.uid && p.reforco > recem.reforco);
  /** O reforço de agora no limite: uma marca por nível, cheia ou vazia (as marcas só dizem isso). */
  const marcas = (p) => `<span class="rf-marcas" aria-label="Reforço +${p.reforco} de ${p.limite}">${Array.from({ length: p.limite }, (_, i) =>
    `<i class="${i < p.reforco ? "cheia" : ""}${acabou(p) && i === p.reforco - 1 ? " nova" : ""}"></i>`).join("")}</span>`;

  /** O passo de agora: o do veio escolhido (a arma do Guerreiro sem veio pede a escolha) ou o único. */
  function passoDe(p) {
    if (!p.passos) return null;
    if (p.passos.length === 1) return p.passos[0];
    return p.passos.find((x) => x.veio === veioSel[p.uid]) || null;
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
    return `<div class="rf-janela m-janela" role="dialog" aria-modal="true" aria-label="${janela === "reforcar" ? "Reforçar" : "Desmontar"}">
      <header class="rf-cab"><nav class="rf-servicos-abas" role="tablist">${abas}</nav>${recursos}
        <button type="button" class="rf-botao fechar" data-fechar>Fechar <kbd>Esc</kbd></button></header>${corpo(d)}</div>`;
  }

  /** Um encaixe da esteira: o ícone, o +N no canto e, ao desmontar, o material que rende (ícone e quantidade). */
  function encaixe(p) {
    const reforco = janela === "reforcar";
    const apagada = reforco ? !!p.sem_reforco : !!p.desmontar.motivo;
    const canto = reforco ? (p.reforco ? `<span class="rf-canto">+${p.reforco}</span>` : "")
      : (p.desmontar.motivo ? "" : `<span class="rf-canto mat">${Icones.porDesenho("saco", 16) || S("saco", 1)}${p.desmontar.total}</span>`);
    return `<button type="button" class="rf-peca r-${h(p.item.raridade)}${p.uid === selUid ? " marcada" : ""}${apagada ? " apagada" : ""}" data-uid="${h(p.uid)}"
      aria-label="${h(p.item.nome)}" aria-pressed="${p.uid === selUid}" ${dicaItem(p.item, "", false)}>${iconePeca(p.item)}${canto}</button>`;
  }

  function corpo(d) {
    const reforco = janela === "reforcar";
    const lista = d.pecas.filter((p) => (reforco ? p.aba === aba : !p.quem));
    const p = lista.find((x) => x.uid === selUid);
    // os donos ao lado; desmontar é só da bolsa: a coluna mostra só ela
    const donos = `<nav class="rf-donos" role="tablist" aria-label="De quem">${d.abas.filter((a) => reforco || a.id === "bolsa").map((a) => {
      const ativo = reforco ? a.id === aba : true;
      const n = d.pecas.filter((x) => (reforco ? x.aba === a.id : !x.quem)).length;
      return `<button type="button" role="tab" class="rf-dono${ativo ? " ativo" : ""}"${reforco ? ` data-aba="${h(a.id)}"` : ""} aria-selected="${ativo}" title="${h(a.nome)}">${retrato(a)}<span>${h(a.nome)}</span><small>${n}</small></button>`;
    }).join("")}</nav>`;
    const esteira = lista.map(encaixe).join("")
      || `<span class="rf-vazio-texto">${reforco ? "Nada aqui." : "Nenhuma peça da bolsa rende material."}</span>`;
    const chapa = !p ? chapaVazia() : reforco ? chapaReforco(p) : chapaDesmonte(p);
    return `<div class="rf-corpo">${donos}<section class="rf-centro"><div class="rf-mesa">${chapa}</div>
        <div class="rf-esteira" role="listbox" aria-label="Peças">${esteira}</div></section>
      <aside class="rf-ficha">${p ? ficha(p) : '<p class="rf-vazio-texto">Nenhuma peça escolhida.</p>'}</aside></div>`;
  }

  // ------------------------------------------------------------------ a chapa (a bancada)
  /** O suporte da peça: o encaixe afundado sobre um pé de ferro com espessura e sombra de contato. */
  function suporte(p, extra = "") {
    return `<div class="rf-suporte${acabou(p) ? " acabou" : ""}">
      <div class="rf-encaixe grande${p ? ` r-${h(p.item.raridade)}` : " vazio"}">${p ? iconePeca(p.item) : ""}</div>
      <div class="rf-pe" aria-hidden="true"></div>${extra}</div>`;
  }
  function chapaVazia() {
    return `<div class="rf-chapa vazia"><div class="rf-linha so">${suporte(null)}</div><p class="rf-vazio-texto">Escolha uma peça</p></div>`;
  }
  /** Um insumo: o ícone num encaixe pequeno, o custo grande e, embaixo, quanto o grupo tem, com o rótulo. */
  function insumo(ic, nome, custo, tem) {
    return `<div class="rf-insumo${tem < custo ? " falta" : ""}" title="${h(nome)}"><span class="rf-encaixe pequeno">${ic}</span>
      <span class="rf-insumo-num"><b>${custo}</b><small><span class="rf-rot">Tem</span> ${tem}</small></span></div>`;
  }
  const linhaGanho = (l, novo) => `<div class="rf-ganho${novo ? " acabou" : ""}"><span>${h(l.nome)}</span><b>${l.antes} → <em>${l.depois}</em></b></div>`;
  function chapaReforco(p) {
    const passo = passoDe(p);
    if (p.no_limite) {
      return `<div class="rf-chapa"><div class="rf-topo"><b>Reforço máximo +${p.limite}</b>${p.veio ? `<small>${h(p.veio)}</small>` : ""}</div>
        <div class="rf-linha so">${suporte(p, marcas(p))}</div></div>`;
    }
    if (p.sem_reforco) {
      return `<div class="rf-chapa"><div class="rf-topo"><span class="rf-nota">${h(p.sem_reforco)}</span></div>
        <div class="rf-linha so">${suporte(p)}</div></div>`;
    }
    const custo = passo || p.passos[0];  // o custo é o mesmo nos dois caminhos
    const materiais = `<div class="rf-insumos" aria-label="Custo"><span class="rf-rot">Custo</span>${insumo(moeda(), "Ouro", custo.ouro, custo.ouro_tem)}${insumo(iconeDe("saco"), "Fragmentos de Têmpera", custo.fragmentos, custo.tem)}</div>`;
    // o resultado: o ganho do passo; a arma do Guerreiro sem veio mostra os dois caminhos, e escolher é clicar num deles
    const resultado = p.passos.length > 1
      ? `<div class="rf-resultado veios" role="radiogroup" aria-label="Caminho da arma">${p.passos.map((x) => `<button type="button" role="radio" class="rf-veio${veioSel[p.uid] === x.veio ? " escolhido" : ""}" data-veio="${x.veio}" aria-checked="${veioSel[p.uid] === x.veio}">
          <span class="rf-veio-nome">${h(x.rotulo)}</span>${x.linhas.map((l) => linhaGanho(l)).join("")}</button>`).join("")}</div>`
      : `<div class="rf-resultado">${passo.linhas.map((l) => linhaGanho(l)).join("")}</div>`;
    const motivo = !passo ? "Escolha Fio ou Runas" : passo.motivo;
    return `<div class="rf-chapa"><div class="rf-topo"><b>+${p.reforco} → +${p.reforco + 1}</b>${p.veio ? `<small>${h(p.veio)}</small>` : ""}</div>
      <div class="rf-linha">${materiais}<span class="rf-conduto" aria-hidden="true"></span>${suporte(p, marcas(p))}<span class="rf-conduto seta" aria-hidden="true"></span>${resultado}</div>
      <div class="rf-pe-chapa"><button type="button" class="rf-botao principal" data-reforcar${motivo ? ` aria-disabled="true" title="${h(motivo)}"` : ""}>Reforçar</button>
        ${motivo ? `<span class="rf-falta">${h(motivo)}</span>` : ""}</div></div>`;
  }
  function chapaDesmonte(p) {
    const d = p.desmontar;
    const recebe = `<div class="rf-resultado recebe"><span class="rf-rot">Recebe</span>
      <span class="rf-encaixe medio" title="${h(plural(d.total, "Fragmento de Têmpera", "Fragmentos de Têmpera"))}">${iconeDe("saco")}<b class="rf-qtd">${d.total}</b></span></div>`;
    const conf = confirmando && confirmando.uid === p.uid;
    const pe = conf
      ? `<div class="rf-confirmar" role="alertdialog" aria-label="Confirmar a desmontagem"><b>Desmontar ${h(p.item.nome)}?</b>
          <span class="rf-aviso">O equipamento será destruído.</span>
          <div class="rf-botoes"><button type="button" class="rf-botao" data-desmontar-nao>Cancelar</button>
          <button type="button" class="rf-botao perigo" data-desmontar-sim disabled>Desmontar</button></div></div>`
      : `<button type="button" class="rf-botao perigo" data-desmontar>Desmontar</button>`;
    return `<div class="rf-chapa"><div class="rf-topo"><b>Desmontar</b></div>
      <div class="rf-linha">${suporte(p)}<span class="rf-conduto seta" aria-hidden="true"></span>${recebe}</div>
      <div class="rf-pe-chapa">${pe}</div></div>`;
  }

  // ------------------------------------------------------------------ a ficha
  /** Nome, dono e todas as propriedades; a que o reforço muda vem destacada pelo valor (o valor seguinte está na
   *  bancada). O Poder das Runas, que a peça ainda não tem, aparece como a linha que vai nascer, com 0. */
  function ficha(p) {
    const passo = janela === "reforcar" ? passoDe(p) : null;
    const muda = new Set((passo ? passo.linhas : []).map((l) => l.nome));
    const novo = acabou(p) ? new Set(recem.nomes) : new Set();
    const linhas = p.propriedades.map((pr) => `<li class="${muda.has(pr.nome) ? "muda" : ""}${novo.has(pr.nome) ? " acabou" : ""}">
      <span>${h(pr.nome)}</span><b>${valor(pr, pr.valor)}</b></li>`);
    (passo ? passo.linhas : []).filter((l) => !p.propriedades.some((pr) => pr.nome === l.nome))
      .forEach((l) => linhas.push(`<li class="muda"><span>${h(l.nome)}</span><b>0</b></li>`));
    return `<div class="rf-ficha-cab"><b class="r-${h(p.item.raridade)}">${h(p.item.nome)}</b><small>${h(dono(p))}</small></div>
      <div class="rf-ficha-meio"><ul class="rf-props">${linhas.join("")}</ul>${p.efeito ? `<p class="rf-efeito">${h(p.efeito)}</p>` : ""}
        ${p.venda !== undefined ? `<div class="rf-venda">Venda: ${moeda()} ${p.venda}</div>` : ""}</div>${teste(p, passo)}`;
  }
  /** A comparação contra o alvo de teste e as substitutas: fechada, marcada "teste". */
  function teste(p, passo) {
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

  // ------------------------------------------------------------------ ligar
  function pedir(dados, botao, foco) {
    if (enviando) return false;
    if (!App.acao({ forja: true }, dados.op === "reforcar" ? "predio_ferreiro" : null, dados)) {
      aviso("Agora não dá para pedir à forja.", "info", "pergaminho");
      return false;
    }
    enviando = true;
    focoDepois = foco || null;
    if (botao) botao.disabled = true;
    return true;
  }

  /** A janela ocupa a coluna do meio (a cena e a página), por cima do balcão. */
  function posicionar() {
    const jan = document.querySelector(".rf-janela");
    const cena = document.getElementById("cena");
    if (!jan || !cena) return;
    const r = cena.getBoundingClientRect();
    Object.assign(jan.style, { left: `${r.left + 8}px`, top: `${r.top + 8}px`, width: `${r.width - 16}px`, height: `${r.height - 16}px` });
  }
  window.addEventListener("resize", posicionar);
  const primeiro = (raiz, foco) => foco && foco.split(",").map((x) => raiz.querySelector(x.trim())).find(Boolean);

  function ligar(raiz, d) {
    enviando = false;
    const redesenhar = (foco) => {
      if (!raiz.isConnected) return;
      const novo = Telas.painel({ tipo: "forja_proto", dados: d });
      raiz.replaceWith(novo);
      const alvo = primeiro(novo, foco);
      if (alvo) alvo.focus();
    };
    const limpar = () => { recem = null; };
    const abrir = (qual, foco) => { janela = qual; selUid = null; confirmando = null; limpar(); redesenhar(foco || ".rf-janela .rf-peca, .rf-janela [data-fechar]"); };
    const fechar = () => { const era = janela; janela = null; confirmando = null; limpar(); redesenhar(`[data-servico="${era}"]`); };
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
      if (aba !== b.dataset.aba) { aba = b.dataset.aba; selUid = null; limpar(); redesenhar(`[data-aba="${b.dataset.aba}"]`); }
    }));
    jan.querySelectorAll("[data-uid]").forEach((b) => b.addEventListener("click", () => {
      if (selUid !== b.dataset.uid) { selUid = b.dataset.uid; confirmando = null; limpar(); redesenhar(`[data-uid="${b.dataset.uid}"]`); }
    }));
    // as setas andam entre as peças da esteira
    jan.addEventListener("keydown", (ev) => {
      if (!["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"].includes(ev.key) || !ev.target.matches("[data-uid]")) return;
      const todas = [...jan.querySelectorAll("[data-uid]")];
      const i = todas.indexOf(ev.target);
      ev.preventDefault();
      todas[(i + (ev.key === "ArrowLeft" || ev.key === "ArrowUp" ? -1 : 1) + todas.length) % todas.length].focus();
    });
    const p = d.pecas.find((x) => x.uid === selUid);
    jan.querySelectorAll("[data-veio]").forEach((b) => b.addEventListener("click", () => {
      veioSel[p.uid] = b.dataset.veio;
      limpar();
      redesenhar(`[data-veio="${b.dataset.veio}"]`);
    }));
    const ref = jan.querySelector("[data-reforcar]");
    if (ref) ref.addEventListener("click", (ev) => {
      if (ev.detail > 1) return;  // o segundo clique de um duplo clique não compra outro passo
      if (ref.getAttribute("aria-disabled")) { App.recusar(ref, ref.title); return; }
      const x = passoDe(p);
      const antes = { uid: p.uid, reforco: p.reforco, nomes: x.linhas.map((l) => l.nome) };
      if (pedir({ op: "reforcar", uid: p.uid, ...(x.veio ? { veio: x.veio } : {}) }, ref, "[data-reforcar]:not([aria-disabled]), [data-uid].marcada")) recem = antes;
    });
    const des = jan.querySelector("[data-desmontar]");
    if (des) des.addEventListener("click", () => { confirmando = { uid: p.uid, nome: p.item.nome }; limpar(); redesenhar("[data-desmontar-nao]"); });
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
      const alvo = primeiro(jan, focoDepois);
      focoDepois = null;
      if (alvo) requestAnimationFrame(() => alvo.isConnected && alvo.focus());
    }
  }

  // Tab e Shift+Tab ficam dentro da janela aberta (ela é um diálogo: a oficina atrás não recebe o foco)
  document.addEventListener("keydown", (ev) => {
    const jan = document.querySelector(".rf-janela");
    if (ev.key !== "Tab" || !janela || !jan) return;
    const focaveis = [...jan.querySelectorAll("button:not([disabled]), summary, [tabindex]:not([tabindex='-1'])")]
      .filter((el) => el.offsetParent !== null);
    if (!focaveis.length) return;
    const i = focaveis.indexOf(document.activeElement);
    ev.preventDefault();
    focaveis[i < 0 ? 0 : (i + (ev.shiftKey ? -1 : 1) + focaveis.length) % focaveis.length].focus();
  }, true);

  // Esc com a janela aberta: primeiro cancela a confirmação, depois fecha a janela; só então o Voltar da forja.
  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape" || !janela || !document.querySelector(".rf-janela")) return;
    ev.preventDefault();
    ev.stopImmediatePropagation();
    if (confirmando) { document.querySelector("[data-desmontar-nao]")?.click(); return; }
    document.querySelector(".rf-janela [data-fechar]")?.click();
  }, true);

  Telas.registrar("forja_proto", balcao, { ligar, esquecer: () => { janela = null; selUid = null; confirmando = null; recem = null; aba = "heroi"; } });

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
