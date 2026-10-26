/* Protótipo do reforço (roadmapIDEIAS/25, seção 5): a tela da forja (painel "forja_proto", demo.py) e a seção
   "Materiais" do inventário. Só esta demonstração carrega este arquivo; o jogo não.

   A forja: à esquerda, as peças do grupo (no corpo de cada um e na bolsa); à direita, a peça escolhida com o passo
   seguinte (ganho, custo, quanto o grupo tem e o que falta) e a comparação na luta, e, para a peça da bolsa, a venda,
   a troca com quem pode usar e a desmontagem. Cada pedido é um clique deliberado: o botão trava até a forja voltar
   desenhada, a tecla segurada não repete e a desmontagem pede uma confirmação que nomeia a peça. */
"use strict";

(() => {
  ACOES_OCULTAS.push("forja");  // o pedido à forja não vira botão na página (nucleo.js)
  const { h, S, dicaItem, iconeItem, topoBalcao } = Telas;

  let selUid = null;       // a peça escolhida (sobrevive ao redesenho da forja)
  let confirmando = null;  // {uid, nome}: a desmontagem pedida, esperando a confirmação
  let enviando = false;

  const icone = (nome) => Icones.porDesenho(nome) || S(nome, 2);
  const num = (v) => String(v).replace(".", ",");
  const frag = (n) => `${n} ${n === 1 ? "Fragmento" : "Fragmentos"} de Têmpera`;

  function cartao(p) {
    const marca = p.reforco ? ` <span class="ref-n">+${p.reforco}</span>` : "";
    const estado = p.sem_reforco ? "sem reforço" : p.no_limite ? `no limite (+${p.reforco})`
      : p.passos && p.passos[0].motivo ? "falta material" : "";
    return `<button type="button" class="ref-peca${p.uid === selUid ? " marcada" : ""}${p.sem_reforco ? " apagada" : ""}" data-uid="${h(p.uid)}" ${dicaItem(p.item, "", false)}>
      <span class="slot-px r-${h(p.item.raridade)}">${Icones.equipamento(iconeItem(p.item)) || S(iconeItem(p.item), 2)}</span>
      <span class="ref-nome">${h(p.item.nome.replace(/ \+\d+$/, ""))}${marca}<small>${estado ? h(estado) : h(p.item.bonus)}</small></span></button>`;
  }

  function lutaHtml(c) {
    if (!c || !c.linhas.length) return "";
    return `<div class="ref-luta"><small>Na luta, contra ${h(c.alvo)} (dano médio, sem crítico):</small>${c.linhas.map((l) =>
      `<div class="ref-luta-linha"><span>${h(l.rotulo)}</span><b>${num(l.antes)} → <span class="${l.melhor ? "melhor" : "pior"}">${num(l.depois)}</span></b></div>`).join("")}</div>`;
  }

  function passoHtml(p, x, k) {
    const custo = `<span class="ref-custo">${Icones.moeda() || S("moeda", 1)}${x.ouro} · ${icone("saco")}${x.fragmentos} <small>(o grupo tem ${x.tem})</small></span>`;
    const titulo = x.rotulo ? `${h(x.rotulo)}: ` : "";
    return `<div class="ref-passo">
      <div class="ref-passo-cab"><b>+${p.reforco} → +${p.reforco + 1}</b> ${titulo}<span class="melhor">${h(x.ganho)}</span></div>
      ${custo}${x.falta.length ? `<div class="pior">Falta ${h(x.falta.join(" e "))}.</div>` : ""}
      ${lutaHtml(x.luta)}
      <button type="button" class="acao-peca ref-reforcar${x.motivo ? " bloqueada" : ""}" data-passo="${k}"${x.motivo ? ` aria-disabled="true" title="${h(x.motivo)}"` : ""}>Reforçar${x.rotulo ? ` · ${h(x.rotulo)}` : ""}</button></div>`;
  }

  function detalhe(d) {
    const p = d.pecas.find((x) => x.uid === selUid);
    if (!p) return `<div class="detalhe-vazio">Escolha uma peça para ver o reforço${d.pecas.some((x) => !x.quem) ? ", a troca e a desmontagem" : ""}.</div>`;
    let html = `<div class="detalhe-ficha">${Telas.htmlItem(p.item, "", false)}</div>
      <div class="ref-onde">${h(p.onde)}${p.reforco ? ` · reforço +${p.reforco} de ${p.limite}${p.veio ? ` (${h(p.veio)})` : ""}: ${h(p.acumulado)}` : ""}</div>`;
    if (p.sem_reforco) html += `<div class="detalhe-vazio">${h(p.sem_reforco)}</div>`;
    else if (p.no_limite) html += `<div class="detalhe-vazio">No limite (+${p.limite}).</div>`;
    else html += p.passos.map((x, k) => passoHtml(p, x, k)).join("");
    if (p.desmontar && p.desmontar.equipada) {
      html += `<div class="ref-nota">Para vender ou desmontar, guarde na bolsa antes (Inventário).</div>`;
    } else if (p.desmontar) {
      const des = p.desmontar;
      (p.trocas || []).forEach((t) => { html += `<h5>Se ${h(t.quem === "Jean" ? "você vestir" : t.quem + " vestir")}${t.no_lugar ? ` no lugar de ${h(t.no_lugar)}` : ""}</h5>${lutaHtml(t)}`; });
      html += `<h5>Vender ou desmontar</h5><div class="ref-nota">No mercado, vende por ${p.venda} de ouro${p.reforco ? " (inclui 25% do ouro investido)" : ""}.</div>`;
      if (confirmando && confirmando.uid === p.uid) {
        html += `<div class="ref-confirmar" role="alertdialog" aria-label="Confirmar a desmontagem">
          <b>Desmontar ${h(p.item.nome)}?</b><div>A peça some. Você recebe ${frag(des.total)}${des.investimento ? ` (${des.investimento} do reforço, ${des.da_peca} da peça)` : ""}.</div>
          <div class="ref-botoes"><button type="button" class="acao-peca perigo" data-desmontar-sim disabled>Desmontar</button>
          <button type="button" class="acao-peca" data-desmontar-nao>Cancelar</button></div></div>`;
      } else {
        const rende = des.total ? `Rende ${frag(des.total)}${des.investimento ? `: ${des.investimento} do reforço e ${des.da_peca} da peça` : " (da peça)"}.` : "";
        html += `<div class="ref-nota">${h(des.motivo || rende)}</div><button type="button" class="acao-peca ref-desmontar${des.motivo ? " bloqueada" : ""}" data-desmontar${des.motivo ? ` aria-disabled="true" title="${h(des.motivo)}"` : ""}>Desmontar…</button>`;
      }
    }
    return html;
  }

  function forja(d) {
    if (selUid && !d.pecas.some((p) => p.uid === selUid)) selUid = null;  // a peça saiu (desmontada): nada marcado
    if (confirmando && !d.pecas.some((p) => p.uid === confirmando.uid)) confirmando = null;
    enviando = false;
    const mats = d.materiais.map((m) => `<span class="ref-mat" title="${h(m.nome)}: ${h(m.desc)} ${h(m.fontes)}">${icone(m.icone)}<b>${m.qtd}</b> ${h(m.plural)}</span>`).join("");
    const grupos = {};
    d.pecas.forEach((p) => { (grupos[p.onde] = grupos[p.onde] || []).push(p); });
    const listas = Object.entries(grupos).map(([onde, ps]) => `<h4>${h(onde)}</h4><div class="ref-lista">${ps.map(cartao).join("")}</div>`).join("");
    return `<div class="tela balcao-servico forja forja-proto">${topoBalcao("martelo", "O ferreiro (protótipo)", "\"Ouro e fragmento. Sem sorte: o que eu prometo, a peça ganha.\"", d.ouro)}
      <div class="ref-materiais"><small>Materiais do grupo:</small>${mats}</div>
      <div class="ref-corpo"><div class="ref-pecas">${listas}</div><div class="peca-detalhe ref-detalhe" aria-live="polite">${detalhe(d)}</div></div></div>`;
  }

  function pedir(dados, botao) {
    if (enviando) return;
    if (!App.acao({ forja: true }, dados.op === "reforcar" ? "predio_ferreiro" : null, dados)) {
      aviso("Agora não dá para pedir à forja.", "info", "pergaminho");
      return;
    }
    enviando = true;
    if (botao) botao.disabled = true;
  }

  function ligar(raiz, d) {
    const redesenhar = (foco) => {
      if (!raiz.isConnected) return;
      const novo = Telas.painel({ tipo: "forja_proto", dados: d });
      raiz.replaceWith(novo);
      const alvo = foco && novo.querySelector(foco);
      if (alvo) alvo.focus();
    };
    raiz.querySelectorAll("[data-uid]").forEach((b) => b.addEventListener("click", () => {
      if (selUid !== b.dataset.uid) { selUid = b.dataset.uid; confirmando = null; redesenhar(`[data-uid="${b.dataset.uid}"]`); }
    }));
    const p = d.pecas.find((x) => x.uid === selUid);
    raiz.querySelectorAll("[data-passo]").forEach((b) => b.addEventListener("click", (ev) => {
      if (ev.detail > 1) return;  // o segundo clique de um duplo clique não compra outro passo
      const x = p.passos[Number(b.dataset.passo)];
      if (x.motivo) { App.recusar(b, x.motivo); return; }
      pedir({ op: "reforcar", uid: p.uid, ...(x.veio ? { veio: x.veio } : {}) }, b);
    }));
    const des = raiz.querySelector("[data-desmontar]");
    if (des) des.addEventListener("click", () => {
      if (p.desmontar.motivo) { App.recusar(des, p.desmontar.motivo); return; }
      confirmando = { uid: p.uid, nome: p.item.nome };
      redesenhar("[data-desmontar-nao]");
    });
    const nao = raiz.querySelector("[data-desmontar-nao]");
    if (nao) nao.addEventListener("click", () => { confirmando = null; redesenhar("[data-desmontar]"); });
    const sim = raiz.querySelector("[data-desmontar-sim]");
    if (sim) {
      // a confirmação só arma depois de um instante: o clique que abriu a pergunta não a responde
      const arma = performance.now() + 400;
      setTimeout(() => { if (sim.isConnected) sim.disabled = false; }, 400);
      sim.addEventListener("click", (ev) => {
        // a trava vale no ouvinte, não só no atributo: nada antes do instante, nem com o botão ainda travado
        if (sim.disabled || performance.now() < arma || ev.detail > 1 || !confirmando) return;
        const c = confirmando;
        confirmando = null;
        selUid = null;
        pedir({ op: "desmontar", uid: c.uid, nome: c.nome, confirmar: true }, sim);
      });
    }
    raiz.addEventListener("keydown", (ev) => {
      if (ev.repeat && (ev.key === "Enter" || ev.key === " ")) ev.preventDefault();  // a tecla segurada não repete
      if (ev.key === "Escape" && confirmando) { ev.preventDefault(); ev.stopPropagation(); confirmando = null; redesenhar("[data-desmontar]"); }
    }, true);
  }

  /* Rolar o balcão recolhe a oficina na faixa de cima, como as outras páginas do jogo fazem com a arte (pagina.js); no
     topo, ela volta inteira. Nas cenas com ambiente o jogo não recolhe; aqui, o balcão precisa do espaço. */
  const paginaEl = document.getElementById("pagina"), cenaEl = document.getElementById("cena");
  paginaEl.addEventListener("scroll", () => {
    if (!document.querySelector(".forja-proto")) return;
    cenaEl.classList.toggle("recolhido", paginaEl.scrollTop > 48);
  }, { passive: true });

  Telas.registrar("forja_proto", forja, { ligar, esquecer: () => { selUid = null; confirmando = null; } });

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
