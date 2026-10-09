/* Dicas: a caixa que aparece com o mouse em cima (curta, de uma linha; ou com a ficha do item e, segurando Shift, o
   equipado ao lado). Uma caixa só, que lembra quem a abriu e some quando o dono sai da tela. */
"use strict";

(() => {
  const { equipadosPara, htmlItem } = Telas;

  const dicas = new Map();
  let proximaDica = 0;
  /** Guarda o HTML de uma dica e devolve o id (para elementos montados via DOM). Os ids nunca se repetem;
   *  as dicas mais antigas (que já não estão na tela) são esquecidas aos poucos. */
  function guardarDica(html) {
    if (dicas.size > 3000) {
      for (const k of [...dicas.keys()].slice(0, 2000)) { dicas.delete(k); itensDica.delete(k); dicasCurtas.delete(k); }
    }
    dicas.set(proximaDica, html);
    return proximaDica++;
  }
  const dicasCurtas = new Set();  // dicas de uma linha (ouro, barras do HUD): caixinha preta sutil em cima do elemento
  function dica(html, curta = false) {
    const id = guardarDica(html);
    if (curta) dicasCurtas.add(id);
    return `data-dica="${id}"`;
  }
  const itensDica = new Map();  // id da dica → item, para o Shift mostrar o equipado ao lado
  function dicaItem(it, rodape = "", comparando = true) {
    const id = guardarDica(htmlItem(it, rodape, comparando));
    if (comparando) itensDica.set(id, it);
    return `data-dica="${id}"`;
  }

  /** A caixa de dica é uma só; ela lembra quem a abriu. Se esse dono sai da tela (a cena trocou, o combate
   *  acabou) sem o mouse "sair" dele, um vigia fecha a dica em vez de deixá-la presa. */
  function caixaDica() {
    let caixa = document.getElementById("dica-item");
    if (!caixa) { caixa = document.createElement("div"); caixa.id = "dica-item"; caixa.className = "m-janela"; caixa.hidden = true; document.body.appendChild(caixa); }
    return caixa;
  }
  let vigia = 0;
  const mouse = { x: -1, y: -1 };
  window.addEventListener("mousemove", (ev) => { mouse.x = ev.clientX; mouse.y = ev.clientY; }, { capture: true, passive: true });
  /** `presa`: a dica fica presa ao LUGAR onde o dono estava quando o mouse chegou (a carta de um inimigo avança
   *  para atacar e volta; a ficha não vai atrás dela). Some quando o mouse sai daquele lugar. */
  function abrirDica(dono, presa = false) {
    const caixa = caixaDica();
    caixa._dono = dono;
    caixa._area = presa ? dono.getBoundingClientRect() : null;
    caixa.hidden = false;
    clearInterval(vigia);
    vigia = setInterval(() => {
      const dentro = caixa._area ? mouseNaArea() : caixa._dono && caixa._dono.matches(":hover");
      if (caixa.hidden || !caixa._dono || !caixa._dono.isConnected || !dentro) esconderDica();
    }, 250);
    return caixa;
  }
  function mouseNaArea() {
    const c = document.getElementById("dica-item"), r = c && c._area;
    return !!r && mouse.x >= r.left && mouse.x <= r.right && mouse.y >= r.top && mouse.y <= r.bottom;
  }
  function dicaAbertaPor(el) {
    const c = document.getElementById("dica-item");
    return !!c && !c.hidden && c._dono === el;
  }
  function ligarDicas(raiz) {
    const caixa = caixaDica();
    raiz.querySelectorAll("[data-dica]").forEach((el) => {
      el.addEventListener("mouseenter", (ev) => {
        const id = Number(el.dataset.dica);
        caixa.innerHTML = dicas.get(id) || "";
        caixa.classList.remove("ficha-inimigo");
        caixa.classList.toggle("curta", dicasCurtas.has(id));
        caixa._item = itensDica.get(id) || null;
        caixa._esquerda = false;
        abrirDica(el);
        const r = el.getBoundingClientRect();
        if (dicasCurtas.has(id)) {  // centrada logo abaixo do elemento, sem cobrir o que ele mostra
          caixa.style.left = Math.max(6, Math.min(window.innerWidth - caixa.offsetWidth - 6, r.left + r.width / 2 - caixa.offsetWidth / 2)) + "px";
          caixa.style.top = Math.min(window.innerHeight - caixa.offsetHeight - 6, r.bottom + 6) + "px";
          return;
        }
        caixa._esquerda = r.right + 10 + 290 > window.innerWidth;
        const esq = caixa._esquerda ? r.left - 300 : r.right + 10;
        caixa.style.left = Math.max(6, esq) + "px";
        caixa.style.top = Math.max(6, Math.min(window.innerHeight - caixa.offsetHeight - 6, r.top - 6)) + "px";
        mostrarEquipado(ev.shiftKey);
      });
      el.addEventListener("mouseleave", esconderDica);
    });
  }
  /** Com Shift seguro, o item que você usa naquele espaço abre ao lado da dica, inteiro (não só a diferença). */
  function mostrarEquipado(ligado) {
    const caixa = document.getElementById("dica-item");
    let lado = document.getElementById("dica-equipado");
    const eq = ligado && caixa && !caixa.hidden && caixa._item ? equipadosPara(caixa._item) : [];
    if (!eq.length) { if (lado) lado.hidden = true; return; }
    if (!lado) { lado = document.createElement("div"); lado.id = "dica-equipado"; lado.className = "m-janela"; document.body.appendChild(lado); }
    lado.innerHTML = eq.map((it, i) => `<div class="${i ? "outro" : ""}"><span class="selo-equipado">Equipado</span>${htmlItem(it, "", false)}</div>`).join("");
    lado.hidden = false;
    const r = caixa.getBoundingClientRect();
    const larg = lado.offsetWidth || 280;
    // Fica do lado oposto ao do item, para não cobrir o que você está olhando.
    let esq = caixa._esquerda ? r.left - larg - 8 : r.right + 8;
    if (esq + larg > window.innerWidth - 6) esq = r.left - larg - 8;
    if (esq < 6) esq = r.right + 8;
    lado.style.left = Math.max(6, esq) + "px";
    lado.style.top = Math.max(6, Math.min(window.innerHeight - lado.offsetHeight - 6, r.top)) + "px";
  }
  window.addEventListener("keydown", (e) => { if (e.key === "Shift" && !e.repeat) mostrarEquipado(true); });
  // Rolar tira o dono da dica de baixo do mouse: ela some na hora (o navegador demora a avisar que o mouse saiu).
  window.addEventListener("wheel", () => { if (!document.getElementById("dica-item")?.hidden) esconderDica(); }, { capture: true, passive: true });
  document.addEventListener("scroll", (ev) => { if (ev.target !== document && !document.getElementById("dica-item")?.hidden) esconderDica(); }, { capture: true, passive: true });
  window.addEventListener("keyup", (e) => { if (e.key === "Shift") mostrarEquipado(false); });
  window.addEventListener("blur", () => mostrarEquipado(false));
  function esconderDica() {
    clearInterval(vigia);
    const c = document.getElementById("dica-item");
    if (c) { c.hidden = true; c._dono = null; c._item = null; c._area = null; c.classList.remove("ficha-inimigo", "curta"); }
    const lado = document.getElementById("dica-equipado");
    if (lado) lado.hidden = true;
  }

  Object.assign(Telas, { abrirDica, dica, dicaAbertaPor, dicaItem, esconderDica, guardarDica, ligarDicas,
                         mouseNaArea });
})();
