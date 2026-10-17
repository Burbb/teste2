/* Menus de item: em quem usar a poção (com a comitiva por perto), e o vigia único que fecha qualquer
   menu de item com um clique fora dele (a comitiva e a fogueira usam o mesmo). */
"use strict";

(() => {
  const { h, esconderDica, ESPACOS, NOME_ESPACO } = Telas;

  /** A vida do herói como no topo e na carta (vida/saudável); com ferimentos ou fome, o limite da cura junto, nomeado. */
  function vidaHeroi(heroi) {
    const vb = heroi.vida_bloqueio;
    return vb ? `${heroi.hp}/${vb.saudavel} · cura até ${vb.limite}` : `${heroi.hp}/${heroi.max_hp}`;
  }

  /** A poção com a comitiva por perto: em quem usar? (só fora de combate) */
  function menuUso(ancora, b) {
    fecharMenuItem();
    esconderDica();
    const heroi = App.estado.heroi;
    const linha = (rotulo, vida, motivo, attr) => `<button type="button" ${attr}${motivo ? ` disabled title="${h(motivo)}"` : ""}>${rotulo}<small>${vida}</small></button>`;
    const m = document.createElement("div");
    m.className = "menu-item m-janela menu-uso";
    m.innerHTML = `<b>${h(b.nome)}</b>
      ${linha("Em você", vidaHeroi(heroi), b.motivo, 'data-em=""')}
      ${b.alvos.map((a) => linha(`Em ${h(a.nome)}`, a.ferido ? h(a.caido) : `${a.hp}/${a.max_hp}`, a.motivo, `data-em="${h(a.id)}"`)).join("")}
      <button type="button" data-em="-" class="secundaria">Cancelar</button>`;
    document.body.appendChild(m);
    const r = ancora.getBoundingClientRect();
    m.style.left = Math.max(8, Math.min(innerWidth - m.offsetWidth - 8, r.left)) + "px";
    m.style.top = (r.bottom + 6 + m.offsetHeight > innerHeight ? r.top - m.offsetHeight - 6 : r.bottom + 6) + "px";
    m.addEventListener("click", (ev) => {
      const bt = ev.target.closest("button");
      if (!bt || bt.disabled) return;
      ev.stopPropagation();
      fecharMenuItem();
      if (bt.dataset.em === "-") return;
      App.acao(bt.dataset.em ? { usar: b.id, em: bt.dataset.em } : { usar: b.id }, "item");
    });
    fecharAoClicarFora();
  }

  /** Equipar da mochila com dois cliques, o botão direito ou Enter (inventário e mercado). O anel vai para o espaço
   *  vazio; com os dois ocupados, um menu pergunta qual substituir: a escolha é de quem joga (um efeito pode valer mais
   *  para a build do que a soma dos números). */
  function equiparDaMochila(ancora, it, i) {
    const heroi = App.estado.heroi;
    const espacos = ESPACOS[it.slot] || [it.slot];
    if (espacos.length < 2) { App.acao({ equipar: i }, "equipar"); return; }
    const vazio = espacos.find((s) => !heroi.equip[s]);
    if (vazio) { App.acao({ equipar: i, destino: vazio }, "equipar"); return; }
    fecharMenuItem();
    esconderDica();
    const m = document.createElement("div");
    m.className = "menu-item m-janela menu-espaco";
    m.innerHTML = `<b>${h(it.nome)}</b>${espacos.map((s) => `<button type="button" data-destino="${s}">Substituir ${h(heroi.equip[s].nome)}<small>${NOME_ESPACO[s]} · ${h(heroi.equip[s].bonus)}</small></button>`).join("")}
      <button type="button" data-destino="-" class="secundaria">Cancelar</button>`;
    document.body.appendChild(m);
    const r = ancora.getBoundingClientRect();
    m.style.left = Math.max(8, Math.min(innerWidth - m.offsetWidth - 8, r.left)) + "px";
    m.style.top = Math.max(8, r.bottom + 6 + m.offsetHeight > innerHeight ? r.top - m.offsetHeight - 6 : r.bottom + 6) + "px";
    m.addEventListener("click", (ev) => {
      const bt = ev.target.closest("button");
      if (!bt) return;
      ev.stopPropagation();
      fecharMenuItem();
      if (bt.dataset.destino !== "-") App.acao({ equipar: i, destino: bt.dataset.destino }, "equipar");
      else if (ancora.isConnected && ancora.tabIndex >= 0) ancora.focus();
    });
    m.querySelector("button").focus();
    fecharAoClicarFora();
  }

  /* Os menus de item fecham com um clique fora deles. Um só "vigia" por vez: antes, cada abertura deixava um
     ouvinte pendurado e o clique seguinte fechava o menu recém-aberto (a bolsa "às vezes não abria"). */
  let vigiaFora = null;
  function fecharAoClicarFora() {
    setTimeout(() => {
      if (vigiaFora || !document.querySelector(".menu-item")) return;
      vigiaFora = (ev) => { if (!ev.target.closest(".menu-item")) fecharMenuItem(); };
      document.addEventListener("pointerdown", vigiaFora, true);
    }, 0);
  }
  function fecharMenuItem() {
    document.querySelectorAll(".menu-item").forEach((m) => m.remove());
    if (vigiaFora) { document.removeEventListener("pointerdown", vigiaFora, true); vigiaFora = null; }
  }

  Object.assign(Telas, { equiparDaMochila, fecharAoClicarFora, fecharMenuItem, menuUso });
})();
