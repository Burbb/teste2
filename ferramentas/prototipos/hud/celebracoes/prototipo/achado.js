/* PROTÓTIPO da etapa 2 (23/10/2026; nada no jogo): rpg/web/static/telas/achado.js da 1.200.1 com a proposta da
   raridade (o selo, a aura em pixel do Brilho, o feixe que não segura o cartão, o adiantar). Servido no lugar do do
   jogo só nas fotos. */
/* Item achado: a janela do saque, por cima do jogo e fora do log, com o feixe na cor da raridade antes do cartão
   (raro e lendário). */
"use strict";

(() => {
  const { h, S, faiscas, htmlItem, iconeItem, noPalco, VAZIO } = Telas;

  const BRILHO_RARIDADE = { comum: ["#f1e4c4", "#c0b8a8"], magico: ["#7fb0ff", "#c8e0ff", "#ffffff"],
    raro: ["#f2c94c", "#fff3a0", "#ffffff"], lendario: ["#ffb35c", "#e0782f", "#fff3a0", "#ffffff"] };
  /** O desenho de um item no cartão: o da interface (Icones), ou o sprite do jogo, no mesmo tamanho. */
  const arte = (sprite, escala) => Icones.porDesenho(sprite, 16 * escala) || S(sprite, escala);
  /** Item encontrado: o cartão dele (sprite, raridade, bônus, diferença para o seu) e, ao lado, o que você usa. */
  function achado(d) {
    const it = d.item;
    const rar = h(it.raridade);
    // O anel: os dois espaços empilhados numa coluna ao lado do achado, cada um com o nome do espaço e o anel que está
    // nele (ou vazio), em cartões baixos: três cartões lado a lado não cabiam e o terceiro quebrava de linha.
    const aneis = d.espacos && (d.equipados || []).length;
    const eq = aneis ? `<div class="achado-aneis">${d.espacos.map((e) => e.item
      ? `<div class="achado-cartao atual compacto rar-${h(e.item.raridade)}" data-espaco="${h(e.espaco)}"><span class="achado-selo">${h(e.nome)} · você usa</span>
          <div class="compacto-corpo"><div class="achado-arte pequena">${arte(iconeItem(e.item), 3)}</div><div>${htmlItem(e.item, "", false)}</div></div></div>`
      : `<div class="achado-cartao atual compacto vazio" data-espaco="${h(e.espaco)}"><span class="achado-selo">${h(e.nome)} · vazio</span>
          <div class="compacto-corpo"><div class="achado-arte pequena">${Icones.vazio(e.espaco, 48) || S(VAZIO[e.espaco], 3, "fantasma")}</div></div></div>`).join("")}</div>`
      : (d.equipados || []).map((e) => `<div class="achado-cartao atual rar-${h(e.raridade)}">
        <span class="achado-selo">Você usa</span>
        <div class="achado-arte pequena">${arte(iconeItem(e), 3)}</div>${htmlItem(e, "", false)}</div>`).join("");
    // Mochila cheia: o que sai do corpo fica para trás (o anel que vai para o espaço vazio não tira nada).
    const aviso = !d.pode_usar || d.cabe ? "" : aneis && d.espacos.some((e) => !e.item)
      ? '<div class="pior">Mochila cheia: substituir um anel deixa o antigo para trás.</div>'
      : '<div class="pior">Mochila cheia: equipar deixa o item antigo para trás.</div>';
    return `<div class="tela achado rar-${rar}">
      <div class="achado-cartao novo rar-${rar}">
        <div class="achado-raios px" aria-hidden="true"></div>
        <span class="achado-selo">Você encontrou</span>
        <span class="selo-raridade rar-${rar}">${{ comum: "Comum", magico: "Mágico", raro: "Raro", lendario: "Lendário" }[it.raridade] || rar}</span>
        <div class="achado-arte">${arte(iconeItem(it), 4)}</div>
        ${htmlItem(it).replace(/(<div class="tipo">[^<]*?) · [^<]*<\/div>/, "$1</div>")}${aviso}
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
    // Os botões chegam com a pergunta, depois da revelação; até lá, os mesmos rótulos (que vêm com o cartão) guardam o
    // lugar deles, invisíveis: a moldura já nasce no tamanho final e não cresce quando eles chegam.
    const reserva = (d.acoes || []).map((t, i) => `<button type="button" class="botao-janela reserva" tabindex="-1" aria-hidden="true"><kbd>${i + 1}</kbd>${h(t)}</button>`).join("");
    fundo.innerHTML = `<div class="janela-achado">${achado(d)}<div class="achado-acoes">${reserva}</div></div>`;
    document.body.appendChild(fundo);
    const janela = fundo.firstElementChild, tela = janela.querySelector(".tela.achado");
    const novo = tela.querySelector(".achado-cartao.novo");
    noPalco(janela);
    if (semCerimonia) return;
    janela.classList.add("so-o-achado");
    const j = janela.getBoundingClientRect(), c = novo.getBoundingClientRect();
    const desvio = Math.round(j.left + j.width / 2 - (c.left + c.width / 2));  // do lugar dele até o meio da janela
    novo.style.translate = `${desvio}px 0`;
    // PROTÓTIPO etapa 2: a intensidade pela raridade, sem segurar o jogador. Comum: o cartão e as faíscas; mágico: a aura
    // leve; raro e lendário: o feixe desce e o cartão aparece quando ele bate no chão (antes: só depois do feixe
    // inteiro, 1 a 1,4 s), e o véu escuro sai na mesma hora (não cobre o texto). Um clique ou uma tecla adianta tudo:
    // o cartão de vez, a comparação e os botões (o gesto não escolhe nada: os botões ainda não estão lá).
    const rar = d.item.raridade, comFeixe = ["raro", "lendario"].includes(rar) && !Brilho.reduzido();
    let adiantou = false;
    const adiantar = (ev) => {
      if (ev.type === "keydown" && (ev.repeat || ![" ", "Enter", "Escape"].includes(ev.key))) return;
      ev.preventDefault(); ev.stopPropagation();
      adiantou = true;
      document.querySelectorAll(".cerimonia-saque").forEach((x) => x.remove());
    };
    document.addEventListener("pointerdown", adiantar, true);
    document.addEventListener("keydown", adiantar, true);
    const esperar = async (ms) => { const fim = performance.now() + App.ritmo(ms); while (!adiantou && performance.now() < fim) await new Promise((r) => setTimeout(r, 30)); };
    if (comFeixe) {
      tela.classList.add("esperando-feixe");
      Sensacao.cerimoniaSaque(rar, novo);  // não espera o feixe inteiro
      await esperar(430);
      document.querySelectorAll(".cerimonia-saque").forEach((x) => x.remove());
      tela.classList.remove("esperando-feixe");
    }
    revelarAchado(tela, d);
    if (rar !== "comum" && janela.isConnected) {
      // a aura em volta da arte do item (sem o disco que fica: o nome logo abaixo continua limpo)
      Brilho.explosao(novo, { paleta: rar, intensidade: { magico: 0, raro: 1, lendario: 3 }[rar], coluna: false,
        centro: novo.querySelector(".achado-arte"), tamanho: [220, 150] });
    }
    // Um instante só com o achado (menor que antes: 550 e 900 ms); então ele vai para o lado dele e a comparação entra.
    await esperar(comFeixe ? 450 : 260);
    document.removeEventListener("pointerdown", adiantar, true);
    document.removeEventListener("keydown", adiantar, true);
    if (!janela.isConnected) return;
    janela.classList.remove("so-o-achado");
    novo.style.translate = "";
    if (desvio && !adiantou && !Brilho.reduzido()) novo.animate([{ translate: `${desvio}px 0` }, { translate: "0 0" }], { duration: App.ritmo(260), easing: "cubic-bezier(.3,.7,.3,1)" });
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
