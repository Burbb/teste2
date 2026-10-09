/* Menus de item: em quem usar a poção ou a bandagem (com a comitiva por perto), e o vigia único que fecha qualquer
   menu de item com um clique fora dele (a comitiva e a fogueira usam o mesmo). */
"use strict";

(() => {
  const { h, esconderDica } = Telas;

  /** Poção ou bandagem com a comitiva por perto: em quem usar? (só fora de combate) */
  function menuUso(ancora, b) {
    fecharMenuItem();
    esconderDica();
    const heroi = App.estado.heroi;
    const linha = (rotulo, vida, motivo, attr) => `<button type="button" ${attr}${motivo ? ` disabled title="${h(motivo)}"` : ""}>${rotulo}<small>${vida}</small></button>`;
    const m = document.createElement("div");
    m.className = "menu-item m-janela menu-uso";
    m.innerHTML = `<b>${h(b.nome)}</b>
      ${linha("Em você", `${heroi.hp}/${heroi.max_hp}`, b.motivo, 'data-em=""')}
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

  Object.assign(Telas, { fecharAoClicarFora, fecharMenuItem, menuUso });
})();
