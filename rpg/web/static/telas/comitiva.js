/* Comitiva: os cartões dos companheiros com a aprovação de cada um, e os menus de quem está na roda (conversar,
   mandar para o acampamento; o animal do patrulheiro). A fogueira usa os mesmos menus. */
"use strict";

(() => {
  const { h, S, barra, dica, fecharAoClicarFora, fecharMenuItem, iconeConsumivel } = Telas;

  function cartaoMembro(m, reserva) {
    return `<div class="cartao clicavel${reserva ? " na-reserva" : ""}" data-cid="${h(m.id)}"><div class="cab">${S(m.id, 3)}<div><b>${h(m.nome)}</b><span class="sub">${h(m.titulo)}${m.ferido ? " · ferido, fora de combate" : ""}${reserva ? " · no acampamento" : ""}</span></div></div>
      <span class="lore">${h(m.desc)}</span>
      <div class="meter" style="margin-top:6px">Vida ${barra("vida", m.hp, m.max_hp)} ${m.hp}/${m.max_hp}</div>
      ${aprovacao(m)}${m.conversa && !reserva ? '<button type="button" class="tag aviso-conversa">✉ quer conversar · clique aqui</button>' : ""}</div>`;
  }
  function comitiva(d) {
    const cartas = d.membros.map((m) => cartaoMembro(m, false)).join("");
    const reserva = (d.reserva || []).map((m) => cartaoMembro(m, true)).join("");
    return `<div class="tela"><div class="cartas">${cartas}</div>
      ${reserva ? `<h4>No acampamento <small>chame de volta quando montar a fogueira</small></h4><div class="cartas">${reserva}</div>` : ""}
      <div class="dica-uso">Clique num companheiro para conversar ou mandar para o acampamento.</div></div>`;
  }

  function aprovacao(m) {
    // Os números com sinal em cor (a favor em verde, contra em vermelho): o valor se lê de relance, sem garimpar a frase.
    const info = (m.aprovacao_info || []).map((l) => `<li>${Realce.sinais(l)}</li>`).join("");
    const valor = Realce.sinais(`${m.aprovacao > 0 ? "+" : m.aprovacao < 0 ? "−" : ""}${Math.abs(m.aprovacao)}`);
    return `<div class="aprovacao ${h(m.classe)}" ${dica(`<b>Aprovação de ${h(m.nome.split(" ").pop())}</b><div class="aprov-agora">${h(m.nivel)} <span class="aprov-num">${valor}</span></div><ul class="dica-lista">${info}</ul><div class="rodape">Roxo: desconfiança · verde: confiança.</div>`)}><span class="trilho"><span class="marca" style="left:${(m.aprovacao + 100) / 2}%"></span></span><span class="rotulo">${h(m.nivel)}</span></div>`;
  }

  /** O animal do patrulheiro na fogueira: carinho, poção, bandagem (o que estiver disponível agora). */
  function menuFera(ancora) {
    fecharMenuItem();
    const ops = App.opcoes() || [];
    const f = App.estado && App.estado.heroi.companheiro;
    if (!f) return;
    const itens = [];
    ops.forEach((o) => {
      const m = o.meta || {};
      if (m.carinho === "fera") itens.push([`${S("coracao", 1)} Fazer carinho`, { carinho: "fera" }]);
      if (m.em === "fera" && m.usar) itens.push([`${S(iconeConsumivel(m.usar), 1)} ${m.usar === "bandagem" ? "Enfaixar" : "Dar a Poção de Vida"}`, { usar: m.usar, em: "fera" }]);
    });
    if (!itens.length) return;
    const menu = document.createElement("div");
    menu.className = "menu-item m-janela";
    menu.innerHTML = `<b>${h(f.nome)}</b><small class="menu-sub">vida ${Math.max(0, f.hp)}/${f.max_hp}</small>` + itens.map(([t], i) => `<button type="button" data-i="${i}">${t}</button>`).join("") +
      '<button type="button" class="secundaria" data-i="-1">Cancelar</button>';
    document.body.appendChild(menu);
    const r = ancora.getBoundingClientRect();
    menu.style.left = Math.max(8, Math.min(innerWidth - menu.offsetWidth - 8, r.left)) + "px";
    menu.style.top = (r.bottom + 6 + menu.offsetHeight > innerHeight ? r.top - menu.offsetHeight - 6 : r.bottom + 6) + "px";
    menu.addEventListener("click", (ev) => {
      const b = ev.target.closest("button");
      if (!b) return;
      ev.stopPropagation();
      fecharMenuItem();
      const i = Number(b.dataset.i);
      if (i >= 0) App.acao(itens[i][1], itens[i][1].carinho ? "escolha" : "item");
    });
    fecharAoClicarFora();
  }

  function menuFigura(ancora, cid) {
    fecharMenuItem();
    const ops = App.opcoes() || [];
    const nomeDe = (id) => (App.estado.heroi.comitiva.concat(App.ultimaFogueira ? App.ultimaFogueira.reserva : []).find((m) => m.id === id) || {}).nome || id;
    const itens = [];
    ops.forEach((o) => {
      const m = o.meta || {};
      if (m.conversar === cid) itens.push([`${S("pergaminho", 1)} Conversar${/✉/.test(o.texto) ? " ✉" : ""}`, { conversar: cid }]);
      if (m.chamar === cid && !m.sai) itens.push([`${S("espada", 1)} Levar amanhã`, { chamar: cid }]);
      if (m.chamar === cid && m.sai) itens.push([`${S("espada", 1)} Levar no lugar de ${h(nomeDe(m.sai).split(" ").pop())}`, { chamar: cid, sai: m.sai }]);
      if (m.reservar === cid) itens.push([`${S("fogueira", 1)} Deixar no acampamento`, { reservar: cid }]);
      if (m.acampamento === cid) itens.push([`${S("fogueira", 1)} Mandar para o acampamento`, { acampamento: cid }]);
    });
    if (!itens.length) return;
    const menu = document.createElement("div");
    menu.className = "menu-item m-janela";
    menu.innerHTML = `<b>${h(nomeDe(cid))}</b>` + itens.map(([t], i) => `<button type="button" data-i="${i}">${t}</button>`).join("") +
      '<button type="button" class="secundaria" data-i="-1">Cancelar</button>';
    document.body.appendChild(menu);
    const r = ancora.getBoundingClientRect();
    menu.style.left = Math.max(8, Math.min(innerWidth - menu.offsetWidth - 8, r.left)) + "px";
    menu.style.top = (r.bottom + 6 + menu.offsetHeight > innerHeight ? r.top - menu.offsetHeight - 6 : r.bottom + 6) + "px";
    menu.addEventListener("click", (ev) => {
      const b = ev.target.closest("button");
      if (!b) return;
      ev.stopPropagation();
      fecharMenuItem();
      const i = Number(b.dataset.i);
      if (i >= 0) App.acao(itens[i][1], "escolha");
    });
    fecharAoClicarFora();
  }

  function ligarFigurasComitiva(raiz) {
    raiz.querySelectorAll(".dormir-barraca").forEach((b) => b.addEventListener("click", (ev) => {
      ev.stopPropagation(); fecharMenuItem(); App.acao({ dormir: true }, "escolha");
    }));
    raiz.querySelectorAll(".figura.fera").forEach((el) => {
      el.addEventListener("click", (ev) => { ev.stopPropagation(); menuFera(el); });
      el.addEventListener("keydown", (ev) => { if (ev.key === "Enter") menuFera(el); });
    });
    raiz.querySelectorAll("[data-cid].figura, .cartao[data-cid]").forEach((el) => {
      el.addEventListener("click", (ev) => {
        ev.stopPropagation();
        // Clicou no aviso de conversa (✉ do retrato ou "quer conversar"): abre a conversa direto, sem menu.
        if (ev.target.closest(".aviso-conversa, .carta-aviso") && App.acao({ conversar: el.dataset.cid }, "escolha")) return;
        menuFigura(el, el.dataset.cid);
      });
    });
  }

  Telas.registrar("comitiva", comitiva, { ligar: ligarFigurasComitiva });

  Object.assign(Telas, { aprovacao, ligarFigurasComitiva });
})();
