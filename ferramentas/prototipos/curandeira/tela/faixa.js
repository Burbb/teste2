/* A faixa da demonstração da curandeira (protótipo): troca o estado da história no save temporário (quem atende) e
   liga a pose parada do movimento reduzido. A troca é um pedido ao motor, como um clique de cartão: só vale com a
   cabana aberta (o motor muda o estado e abre a cabana de novo). */
"use strict";

(() => {
  // as opções da troca chegam no menu da cabana, mas quem as desenha é esta faixa (não viram botões na página)
  if (typeof ACOES_OCULTAS !== "undefined" && !ACOES_OCULTAS.includes("cur_estado")) ACOES_OCULTAS.push("cur_estado");
  const ESTADOS = [["pita", "Pita (Marta de cama)"], ["pita_escura", "Pita (a água escura)"], ["marta", "Marta (de pé)"]];
  const f = document.createElement("div");
  f.id = "faixa-cur";
  f.innerHTML = `<b>Curandeira (protótipo)</b>${ESTADOS.map(([id, nome]) => `<button type="button" data-cur="${id}">${nome}</button>`).join("")}
    <button type="button" data-reduzido aria-pressed="false">Pose parada</button><span class="aviso"></span>`;
  document.body.appendChild(f);
  const aviso = f.querySelector(".aviso");
  const marcar = () => {
    const d = window.Cenas && Cenas.atual() && Cenas.atual().d;
    const atual = d && d.cena === "curandeira" ? (d.quem === "marta" ? "marta" : d.agua === "escura" ? "pita_escura" : "pita") : null;
    f.querySelectorAll("[data-cur]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.cur === atual)));
  };
  setInterval(marcar, 400);
  f.querySelectorAll("[data-cur]").forEach((b) => b.addEventListener("click", () => {
    const ok = App.acao({ cur_estado: b.dataset.cur });
    aviso.textContent = ok ? "" : "Abra a curandeira (o prédio na vila) para trocar.";
  }));
  f.querySelector("[data-reduzido]").addEventListener("click", (ev) => {
    const sim = document.body.dataset.curReduzido !== "1";
    document.body.dataset.curReduzido = sim ? "1" : "";
    ev.currentTarget.setAttribute("aria-pressed", String(sim));
  });
})();
