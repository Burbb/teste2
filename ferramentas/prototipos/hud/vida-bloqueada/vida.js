// Protótipo: a vida máxima bloqueada (etapa 1B). Lê `estado.heroi.vida_bloqueio` (cenario.py: as contas do motor) e
// marca as barras da vida do herói: a do topo (HUD) e a da carta na luta. Não mexe em número nenhum do jogo: a vida, o
// limite e o saudável vêm do estado; o enchimento continua com as animações do jogo. Sem bloqueio, desfaz tudo.
(() => {
  const info = () => (typeof estado !== "undefined" && estado && estado.heroi && estado.heroi.vida_bloqueio) || null;
  const dicas = new WeakMap();
  function dicaDe(b, hp) {
    const fontes = b.fontes.map((f) => `${esc(f.nome)} −${f.pct}% (−${f.perda})`).join("<br>");
    return `<b>Vida ${hp} de ${b.limite}</b><div>${b.limite} é o limite agora: uma cura comum não passa dele.</div>` +
      `<div class="bonus pior">${b.saudavel - b.limite} bloqueados na vida máxima:<br>${fontes}</div>` +
      `<div class="rodape">Saudável: ${b.saudavel}. ${[
        b.fontes.some((f) => f.nome !== "Fome") ? "Um ferimento devolve a sua parte quando sara (descansando) ou na Curandeira; a bandagem só evita a infecção." : "",
        b.fontes.some((f) => f.nome === "Fome") ? "A fome devolve a dela quando você come." : ""].filter(Boolean).join(" ")}</div>`;
  }
  function decorar(bar, num, hp, b, comDica) {
    if (!bar) return;
    let z = bar.querySelector(":scope > .bloqueio");
    if (!b) {
      bar.classList.remove("com-bloqueio");
      if (z) z.remove();
      if (num && num.querySelector(".bloq-num")) num.querySelector(".bloq-num").remove();
      if (num) num._bloq = undefined;
      return;
    }
    const lim = b.limite / b.saudavel;
    bar.classList.add("com-bloqueio");
    if (bar.style.getPropertyValue("--lim") !== String(lim)) bar.style.setProperty("--lim", lim);
    if (!z) { z = document.createElement("span"); z.className = "bloqueio"; bar.appendChild(z); }
    if (num && hp !== null) {
      const html = hp > 0 ? `${hp}/${b.saudavel}<span class="bloq-num">${spr("cadeado", 1)}−${b.saudavel - b.limite}</span>` : "caído";
      // compara com o que foi escrito (o navegador normaliza o HTML da imagem: comparar com innerHTML voltaria sempre)
      if (num._bloq !== html || !num.querySelector(".bloq-num") === hp > 0) { num._bloq = html; num.innerHTML = html; window.__vidaEscritas = (window.__vidaEscritas || 0) + 1; }
    }
    if (comDica) {
      const alvo = bar.closest("[data-dica]");
      const html = dicaDe(b, hp);
      if (alvo && dicas.get(alvo) !== html) { dicas.set(alvo, html); alvo.setAttribute("data-dica", Telas.dica(html).match(/"(.*)"/)[1]); }
    }
  }
  function tudo() {
    const b = info();
    const vital = document.querySelector('#hud-linha .vital[data-vital="hp"]');
    if (vital) decorar(vital.querySelector(".barra-px"), vital.querySelector(".num"), estado ? estado.heroi.hp : null, b, true);
    const c = typeof Batalha !== "undefined" && Batalha.elCarta("j");
    if (c) decorar(c.querySelector(".carta-hp .barra-px"), c.querySelector(".carta-hp .num"), c._hp !== undefined ? c._hp : estado.heroi.hp, b, false);
  }
  let agendado = false;
  new MutationObserver(() => { if (!agendado) { agendado = true; queueMicrotask(() => { agendado = false; tudo(); }); } })
    .observe(document.getElementById("hud"), { childList: true, subtree: true, characterData: true });
  tudo();
  window.__vidaBloqueada = tudo;
})();
