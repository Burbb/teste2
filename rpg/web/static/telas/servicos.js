/* Serviços da vila: a cabana da curandeira (tratar), em cartões com preço, tempo e o motivo quando não dá, e os
   componentes que a forja (telas/forja.js), o templo e a taverna (vila.js) usam: o topo do balcão e o cartão. */
"use strict";

(() => {
  const { h, S, dica } = Telas;

  /* A cabana da curandeira é uma tela como o mercado; o templo e a taverna usam os mesmos cartões diante do prédio
     (vila.js monta, com as opções que o motor marca com preço e efeito). */
  /** O topo de um balcão: o ícone, quem atende e o que diz, e o seu ouro. */
  function topoBalcao(icone, quem, fala, ouro) {
    return `<div class="loja-topo">${S(icone, 3)}<div><b>${h(quem)}</b><span class="lore">${h(fala)}</span></div>` +
      (ouro === undefined ? "" : `<span class="ouro-loja">${Icones.ouro() || S("moedas", 2)}${ouro}</span>`) + "</div>";
  }
  /** Um serviço num cartão: o ícone, o nome, o que dá, o preço e o tempo. Com `motivo` (sem ouro), apagado; sem preço
   *  nem motivo e com `limite`, é só mostruário. `attrs`: o que identifica a ação (data-...). */
  /** `linhas`: o que o serviço dá em linhas curtas, com ícone ("Custo: 10 ouro", "Recuperação: +21 vida · Vigor
   *  completo"); as notas (só o que afeta este resultado) vêm apagadas. Com elas, o custo mora numa linha e o canto
   *  direito fica livre. */
  function cartaoServico({ icone, raridade, nome, efeito, preco, tempo, motivo, limite, linhas, attrs = "", dicaAttr = "" }) {
    const r = raridade ? ` r-${h(raridade)}` : "";
    const fim = linhas ? "" : (preco === 0 ? '<span class="preco gratis">grátis</span>' : preco != null ? `<span class="preco">${Icones.moeda() || S("moeda", 1)}${preco}</span>` : "") + (tempo ? `<small class="serv-tempo">⧗ ${h(tempo)}</small>` : "");
    const corpo = linhas ? linhas.map((l) => l.nota ? `<span class="serv-nota">${h(l.nota)}</span>`
      : `<span class="serv-linha">${Icones.miudo(l.icone) || S(l.icone, 1)}<span class="serv-rotulo">${h(l.rotulo)}:</span> ${Realce.texto(l.texto)}</span>`).join("")
      : efeito ? `<span class="serv-efeito">${Realce.texto(efeito)}</span>` : "";
    return `<button type="button" class="servico${motivo ? " caro" : ""}${limite ? " limite" : ""}" ${attrs} ${dicaAttr}${motivo ? ` aria-disabled="true" data-motivo="${h(motivo)}"` : ""}>
      <span class="slot-px${r}">${Icones.porDesenho(icone) || S(icone, 2)}</span>
      <span class="serv-texto"><b class="serv-nome${r}">${h(nome)}</b>${corpo}</span>
      <span class="serv-fim">${fim}</span></button>`;
  }
  function curandeira(d) {
    const cartoes = d.ferimentos.map((f) => cartaoServico({
      // O primeiro tratamento grátis (o motor diz): no lugar do efeito, até ser usado; a explicação fica na dica.
      icone: f.id === "infeccao" ? "gota_verde" : "gota", nome: f.nome, efeito: f.gratis || (f.explica || [])[0] || "", preco: f.gratis ? null : f.custo,
      motivo: f.motivo || "", attrs: `data-tratar="${h(f.id)}"`,
      dicaAttr: dica(`<b>${h(f.nome)}</b>${(f.explica || []).map((l, i) => `<div class="${i ? "" : "bonus pior"}">${h(l)}</div>`).join("")}${f.motivo ? `<div class="rodape">${h(f.motivo)}</div>` : ""}`),
    }));
    // Quem atende e o que diz vêm do motor quando não é a curandeira de sempre (no Vau da campanha: Pita ou Marta) e
    // quando não há mais nada para tratar (a fala diz isso; fica só o Voltar).
    return `<div class="tela balcao-servico curandeira">${topoBalcao("unguento", d.quem || "A curandeira", d.fala || "Uma velha de mãos manchadas de sangue seco examina você. \"O que vai ser?\"", d.ouro)}
      ${cartoes.length ? `<h4>Tratar</h4><div class="servicos">${cartoes.join("")}</div>` : ""}</div>`;
  }
  /** Clique (ou Enter) num cartão: a ação, ou o "não" com o motivo do motor, no próprio cartão. */
  function ligarServicos(raiz, chave, som) {
    raiz.querySelectorAll(`[data-${chave}]`).forEach((b) => b.addEventListener("click", (ev) => {
      ev.stopPropagation();
      if (b.classList.contains("caro")) { App.recusar(b, b.dataset.motivo); return; }
      App.acao({ [chave]: b.dataset[chave] }, som);
    }));
  }

  Telas.registrar("curandeira", curandeira, { ligar: (raiz) => ligarServicos(raiz, "tratar", "cura") });

  Object.assign(Telas, { cartaoServico, topoBalcao });
})();
