/* Item achado: a janela do saque, por cima do jogo e fora do log, com o feixe na cor da raridade antes do cartão
   (raro e lendário). */
"use strict";

(() => {
  const { h, S, faiscas, htmlItem, iconeItem, noPalco } = Telas;

  const BRILHO_RARIDADE = { comum: ["#f1e4c4", "#c0b8a8"], magico: ["#7fb0ff", "#c8e0ff", "#ffffff"],
    raro: ["#f2c94c", "#fff3a0", "#ffffff"], lendario: ["#ffb35c", "#e0782f", "#fff3a0", "#ffffff"] };
  /** Item encontrado: o cartão dele (sprite, raridade, bônus, diferença para o seu) e, ao lado, o que você usa. */
  function achado(d) {
    const it = d.item;
    const rar = h(it.raridade);
    const eq = (d.equipados || []).map((e) => `<div class="achado-cartao atual rar-${h(e.raridade)}">
        <span class="achado-selo">Você usa</span>
        <div class="achado-arte pequena">${S(iconeItem(e), 3)}</div>${htmlItem(e, "", false)}</div>`).join("");
    const aviso = !d.pode_usar ? "" : !d.cabe ? '<div class="pior">Mochila cheia: equipar deixa o item antigo para trás.</div>' : "";
    return `<div class="tela achado rar-${rar}">
      <div class="achado-cartao novo rar-${rar}">
        <div class="achado-raios" aria-hidden="true"></div>
        <span class="achado-selo">Você encontrou</span>
        <div class="achado-arte">${S(iconeItem(it), 4)}</div>
        ${htmlItem(it, "", true)}${aviso}
      </div>${eq}</div>`;
  }
  /** O item achado abre numa janela própria, por cima do jogo e fora do log. Como nos ARPGs, o achado é a estrela:
   *  primeiro ele sozinho, no meio da janela (raro e lendário: o feixe de luz cai ali antes); depois ele abre espaço,
   *  o que você usa entra ao lado com a comparação e aparecem os botões (que vêm da pergunta do motor, ver
   *  escolhas.js). A janela já nasce no tamanho final: nada pula, o cartão só começa deslocado para o meio. Ela fecha
   *  quando o ícone pousa (no corpo ou na mochila), ou ao deixar o item. */
  async function abrirAchado(d, semCerimonia = false) {
    fecharAchado();
    const fundo = document.createElement("div");
    fundo.id = "sobre-achado";
    fundo.className = "sobreposicao";
    fundo.innerHTML = `<div class="janela-achado">${achado(d)}<div class="achado-acoes"></div></div>`;
    document.body.appendChild(fundo);
    const janela = fundo.firstElementChild, tela = janela.querySelector(".tela.achado");
    const novo = tela.querySelector(".achado-cartao.novo");
    noPalco(janela);
    if (semCerimonia) return;
    janela.classList.add("so-o-achado");
    const j = janela.getBoundingClientRect(), c = novo.getBoundingClientRect();
    const desvio = Math.round(j.left + j.width / 2 - (c.left + c.width / 2));  // do lugar dele até o meio da janela
    novo.style.translate = `${desvio}px 0`;
    tela.classList.add("esperando-feixe");
    await Sensacao.cerimoniaSaque(d.item.raridade, novo);
    tela.classList.remove("esperando-feixe");
    revelarAchado(tela, d);
    // Um instante só com o achado; então ele vai para o lado dele e a comparação entra.
    const raro = ["raro", "lendario"].includes(d.item.raridade);
    await new Promise((r) => setTimeout(r, App.ritmo(raro ? 900 : 550)));
    if (!janela.isConnected) return;
    janela.classList.remove("so-o-achado");
    novo.style.translate = "";
    if (desvio) novo.animate([{ translate: `${desvio}px 0` }, { translate: "0 0" }], { duration: App.ritmo(380), easing: "cubic-bezier(.3,.7,.3,1)" });
  }
  /** Onde a pergunta "o que fazer com o item?" põe os botões (null se a janela não está aberta). */
  function acoesDoAchado() { return document.querySelector("#sobre-achado .achado-acoes"); }
  function fecharAchado() {
    const f = document.getElementById("sobre-achado");
    if (!f) return;
    f.id = "";  // a próxima janela (outro item logo em seguida) já pode abrir enquanto esta some
    f.classList.add("saindo");
    setTimeout(() => f.remove(), 220);
  }

  /** O cartão do item aparece de vez: o som da raridade e as faíscas (depois da cerimônia, se houve uma). */
  function revelarAchado(raiz, d) {
    const cartao = raiz.querySelector(".achado-cartao.novo");
    if (!cartao) return;
    const raro = ["raro", "lendario"].includes(d.item.raridade);
    App.som(raro ? "achado_raro" : "achado");
    setTimeout(() => { if (cartao.isConnected) faiscas(cartao.querySelector(".achado-arte"), BRILHO_RARIDADE[d.item.raridade] || BRILHO_RARIDADE.comum, raro ? 22 : 12); }, 260);
  }

  Telas.registrar("achado", achado);

  Object.assign(Telas, { abrirAchado, acoesDoAchado, fecharAchado, revelarAchado });
})();
