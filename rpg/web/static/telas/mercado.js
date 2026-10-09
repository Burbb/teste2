/* Mercado: os suprimentos à venda (a quantidade escolhida sobrevive ao redesenho; segurar +/− repete) e a mochila
   ao lado, para vender. */
"use strict";

(() => {
  const { h, S, dica, dicaItem, esconderDica, fecharMenuItem, iconeItem, moedasPara } = Telas;

  const qtdLoja = {};  // quantidade escolhida em cada suprimento (sobrevive ao redesenho, não à saída do mercado)

  function maxCompra(c, ouro) { return Math.max(0, Math.min(99, c.limite ?? 99, Math.floor(ouro / c.preco))); }
  function loja(d) {
    // Na vitrine, o número no canto do ícone é o que o mercador tem (como nos jogos do gênero); o que você carrega
    // está na bolsa e no topo.
    const cons = d.consumiveis.map((c) => {
      const max = maxCompra(c, d.ouro);
      const q = Math.max(1, Math.min(qtdLoja[c.id] || 1, max || 1));
      const caro = max < 1;
      const icone = c.icone || "pocao";
      return `<div role="button" tabindex="0" class="mercadoria suprimento${caro ? " caro" : ""}" data-comprar="${h(c.id)}" data-preco="${c.preco}" data-max="${max}" ${dica(`<b>${h(c.nome)}</b><div>${Realce.texto(c.desc)}</div><div class="rodape">${caro ? (c.estoque === 0 ? "Esgotado: o mercador reabastece amanhã cedo." : c.limite === 0 ? "Você não carrega mais." : "Ouro insuficiente.") : "Escolha a quantidade e clique para comprar. Shift+clique compra 5."}</div>`)}>
        <span class="slot-px">${S(icone, 2)}${c.estoque ? `<span class="qtd">${c.estoque}</span>` : ""}</span>
        <span class="merc-nome">${h(c.nome)}${c.estoque === 0 ? '<small class="merc-estoque esgotado">esgotado</small>' : ""}</span>
        <span class="preco">${S("moeda", 1)}<span class="total">${c.preco * q}</span></span>
        <span class="qtd-ctrl"><button type="button" data-q="-1" aria-label="menos">−</button><b>${q}</b><button type="button" data-q="1" aria-label="mais">+</button></span></div>`;
    }).join("");
    const equips = d.equipamentos.map((it, i) => {
      const caro = it.preco > d.ouro;
      return `<button type="button" class="mercadoria equip${caro ? " caro" : ""}" data-comprar-item="${i}" ${dicaItem(it, caro ? "Ouro insuficiente." : "Clique para comprar. Se o espaço do corpo estiver vazio, você já sai vestindo.")}>
        <span class="slot-px r-${h(it.raridade)}">${S(iconeItem(it), 2)}</span>
        <span class="merc-nome r-${h(it.raridade)}">${h(it.nome)}</span><span class="merc-bonus">${h(it.bonus)}</span><span class="preco">${S("moeda", 1)}${it.preco}</span></button>`;
    }).join("");
    // A mochila no mercado é para vender: cada item com o preço embaixo; clique vende na hora (o que você vendeu fica no
    // balcão para recomprar pelo mesmo preço, a rede do clique único) e o botão direito equipa, como no inventário.
    const venda = (it) => `<div class="preco-venda">${S("moeda", 1)} O mercador paga <b>${it.preco}</b></div>` +
      `Clique: vender${it.usavel ? " · botão direito: equipar" : " · não é para a sua classe"}`;
    const mochila = d.mochila.map((it, i) => `<div class="venda-item"><div role="button" tabindex="0" class="slot-px celula r-${h(it.raridade)}${it.usavel ? "" : " inutil"}" draggable="true" data-mochila-loja="${i}" ${dicaItem(it, venda(it))}>${S(iconeItem(it), 2)}</div>` +
      `<span class="preco">${S("moeda", 1)}${it.preco}</span></div>`);
    for (let i = d.mochila.length; i < d.limite; i++) mochila.push('<div class="venda-item"><div class="slot-px celula vazia"></div></div>');
    const recompra = (d.recompra || []).map((it, i) => `<div class="venda-item"><div role="button" tabindex="0" class="slot-px celula r-${h(it.raridade)}${it.preco > d.ouro ? " caro" : ""}" data-recomprar="${i}" ${dicaItem(it, `<div class="preco-venda">${S("moeda", 1)} Recomprar por <b>${it.preco}</b></div>Clique para desfazer a venda.`)}>${S(iconeItem(it), 2)}</div>` +
      `<span class="preco">${S("moeda", 1)}${it.preco}</span></div>`).join("");
    return `<div class="tela loja">
      <div class="loja-topo">${S("saco", 3)}<div><b>O mercador</b><span class="lore">"Tudo tem preço. Até você."</span></div>
        <span class="ouro-loja">${S("moedas", 2)}${d.ouro}</span></div>
      <div class="balcao">
        <h4>Suprimentos</h4><div class="vitrine">${cons}</div>
        <h4>Equipamentos</h4><div class="vitrine">${equips || '<span class="vazio">Nada que preste hoje. Volte em alguns dias.</span>'}</div>
      </div>
      <h4>Sua mochila <small>${d.ocupado}/${d.limite} · clique vende (o mercador paga metade) · botão direito equipa</small></h4>
      <div class="mochila-grade mochila-loja">${mochila.join("")}</div>
      ${recompra ? `<h4>Vendidos agora <small>clique para recomprar pelo mesmo preço (até você sair do mercado)</small></h4><div class="mochila-grade mochila-loja recompra">${recompra}</div>` : ""}</div>`;
  }

  let repeticao = null;  // o "segurar +/−" do mercado em andamento
  function pararRepeticao() { clearTimeout(repeticao); repeticao = null; }
  ["pointerup", "pointercancel", "blur"].forEach((t) => window.addEventListener(t, pararRepeticao));
  function ligarLoja(raiz) {
    pararRepeticao();
    const dados = App.ultimaLoja;
    raiz.querySelectorAll("[data-comprar]").forEach((el) => {
      const preco = Number(el.dataset.preco), max = Number(el.dataset.max), id = el.dataset.comprar;
      const num = el.querySelector(".qtd-ctrl b"), total = el.querySelector(".total");
      const mudar = (q) => {
        q = Math.max(1, Math.min(max || 1, q));
        qtdLoja[id] = q; num.textContent = q; total.textContent = preco * q;
      };
      el.querySelectorAll("[data-q]").forEach((b) => {
        const passo = () => mudar(Math.min(qtdLoja[id] || 1, max || 1) + Number(b.dataset.q));
        b.addEventListener("click", (ev) => { ev.stopPropagation(); });
        b.addEventListener("pointerdown", (ev) => {
          ev.stopPropagation(); pararRepeticao(); passo(); App.som("escolha");
          // Segurar acelera. A repetição para ao soltar em qualquer lugar, ao sair da janela, ao chegar no
          // limite e se o botão sumir (a tela se redesenhou): nunca fica rodando sozinha.
          repeticao = setTimeout(function repetir() {
            const antes = qtdLoja[id];
            if (!b.isConnected) { pararRepeticao(); return; }
            passo();
            repeticao = qtdLoja[id] === antes ? null : setTimeout(repetir, 70);
          }, 380);
        });
        ["pointerup", "pointerleave", "pointercancel"].forEach((t) => b.addEventListener(t, pararRepeticao));
      });
      // A roda do mouse só mexe na quantidade em cima do controle (rolar a página não pode mudar a compra).
      const comprar = (ev) => {
        if (el.classList.contains("caro")) { App.som("falha"); return; }
        const q = ev.shiftKey ? Math.min(5, max) : Math.min(qtdLoja[id] || 1, max);
        qtdLoja[id] = 1;
        App.acao({ comprar: id }, "moeda", { qtd: q });
      };
      el.addEventListener("click", (ev) => { if (!ev.target.closest(".qtd-ctrl")) comprar(ev); });
      el.addEventListener("keydown", (ev) => { if (ev.key === "Enter") comprar(ev); });
    });
    raiz.querySelectorAll("[data-comprar-item]").forEach((el) => el.addEventListener("click", (ev) => { ev.stopPropagation(); if (!el.classList.contains("caro")) App.acao({ comprar_item: Number(el.dataset.comprarItem) }, "moeda"); else App.som("falha"); }));
    // Mochila: clique abre um menu (equipar / vender); arrastar só vende se soltar no balcão do mercador.
    let vendendo = null;
    const balcao = raiz.querySelector(".balcao");
    raiz.querySelectorAll("[data-mochila-loja]").forEach((el) => {
      const i = Number(el.dataset.mochilaLoja);
      const it = dados && dados.mochila[i];
      // Clique vende na hora: as moedas voam até o ouro do topo (o tilintar vem do ouro recebido: um som só).
      const vender = () => {
        if (!it) return;
        fecharMenuItem(); esconderDica();
        if (App.acao({ vender: i })) moedasPara(el, document.querySelector('.recurso[data-rec="ouro"]'));
      };
      el.addEventListener("click", (ev) => { ev.stopPropagation(); vender(); });
      el.addEventListener("keydown", (ev) => { if (ev.key === "Enter") vender(); });
      // Botão direito equipa, como no inventário.
      el.addEventListener("contextmenu", (ev) => {
        ev.preventDefault(); fecharMenuItem(); esconderDica();
        if (!it) return;
        if (!it.usavel) { App.som("falha"); App.avisar("Não é para a sua classe.", "equipar"); return; }
        App.acao({ equipar: i }, "equipar");
      });
      el.addEventListener("dragstart", (ev) => { esconderDica(); fecharMenuItem(); vendendo = i; ev.dataTransfer.setData("text/plain", "item"); balcao.classList.add("alvo"); });
      el.addEventListener("dragend", () => { balcao.classList.remove("alvo"); setTimeout(() => { vendendo = null; }, 0); });
    });
    raiz.querySelectorAll("[data-recomprar]").forEach((el) => el.addEventListener("click", (ev) => {
      ev.stopPropagation(); esconderDica();
      if (el.classList.contains("caro")) { App.som("falha"); App.avisar("Ouro insuficiente para recomprar.", "recomprar"); return; }
      App.acao({ recomprar: Number(el.dataset.recomprar) }, "moeda");
    }));
    balcao.addEventListener("dragover", (ev) => { if (vendendo !== null) ev.preventDefault(); });
    balcao.addEventListener("drop", (ev) => {
      ev.preventDefault(); balcao.classList.remove("alvo");
      if (vendendo !== null) App.acao({ vender: vendendo });  // um som só: o do ouro recebido
      vendendo = null;
    });
  }

  Telas.registrar("loja", loja, {
    ligar: (raiz, d) => { App.ultimaLoja = d; ligarLoja(raiz); },
    esquecer: () => { for (const k in qtdLoja) delete qtdLoja[k]; },
  });
})();
