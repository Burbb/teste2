/* Sensação: o peso dos momentos do jogo. As telas (batalha.js, telas.js) dizem O QUE aconteceu; aqui mora
   COMO aquilo se sente: quanto o tempo para no impacto, quanto a arena treme, como a câmera chega perto do
   golpe que encerra a luta. Os números ficam todos em AJUSTES, para afinar sem caçar setTimeout pelo código.

   O motor marca os fatos no lance do golpe (crit, abate, final); quem anima só pergunta Sensacao.golpe(). */
"use strict";

const Sensacao = (() => {
  const AJUSTES = {
    // Quanto tempo tudo congela no quadro do impacto (hit-stop, como em Hades e Dead Cells), em ms.
    parada: { critico: 80, abate: 70, final: 300 },
    // Quanto a arena treme, em px (e por quanto tempo, em ms).
    tremor: { leve: 3, critico: 5, abate: 7, final: 11 },
    tremorMs: 340,
    // O golpe final: a câmera chega perto de quem cai, o resto escurece.
    zoomFinal: 1.07,
    // Números que contam subindo (ouro do espólio): duração e o máximo de tiques de som.
    contarMs: 650, tiquesMax: 10,
    // A barra de XP enchendo (por trecho de nível) e quanto o espólio fica na tela depois de tudo.
    barraMs: 700, espolioEsperaMs: 450, espolioFicaMs: 900,
  };
  // O que pesa mais, quando vários golpes caem de uma vez (uma salva em área): o mais pesado dá o tom.
  const ORDEM = ["final", "abate", "critico"];

  let rapido = () => false, pausa = (ms) => ms;
  function configurar(opts) { rapido = opts.rapido; pausa = opts.pausa; }
  const dormir = (ms) => (ms > 0 ? new Promise((r) => setTimeout(r, ms)) : Promise.resolve());

  /** O peso de um golpe pelo que o motor diz dele: o golpe que encerra a luta, o que derruba, o crítico. */
  function peso(m) { return m.final ? "final" : m.abate ? "abate" : m.crit ? "critico" : null; }
  function maisPesado(lances) {
    let melhor = null, nivel = ORDEM.length;
    for (const x of lances) {
      const i = ORDEM.indexOf(peso(x));
      if (i >= 0 && i < nivel) { melhor = x; nivel = i; }
    }
    return melhor;
  }

  /** A arena treme: de um lado para o outro, cada vez menos. */
  function tremor(palco, px, ms = AJUSTES.tremorMs) {
    if (rapido() || !palco || !px) return;
    const passos = [];
    for (let i = 0; i <= 8; i++) {
      const f = px * (1 - i / 8);
      passos.push({ translate: `${(i % 2 ? -1 : 1) * f}px ${(i % 3 - 1) * f * 0.4}px` });
    }
    palco.animate(passos, { duration: pausa(ms), easing: "linear" });
  }

  /** Tudo congela um instante no quadro do impacto; quem levou o golpe pisca em branco. */
  async function parada(palco, alvo, ms) {
    if (rapido() || !palco || !ms) return;
    palco.classList.add("parado");
    if (alvo) alvo.classList.add("lampejo");
    await dormir(pausa(ms));
    palco.classList.remove("parado");
    if (alvo) alvo.classList.remove("lampejo");
  }

  /** O golpe que encerra a luta: a câmera chega perto de quem cai, o resto escurece, o tempo quase para. */
  async function golpeFinal(palco, alvo) {
    const p = palco.getBoundingClientRect(), a = alvo.getBoundingClientRect();
    palco.style.transformOrigin = `${a.left + a.width / 2 - p.left}px ${a.top + a.height / 2 - p.top}px`;
    palco.style.setProperty("--zoom-final", AJUSTES.zoomFinal);
    palco.classList.add("foco-final");
    alvo.classList.add("alvo-final");
    Som.tocar("golpe_final");
    await parada(palco, alvo, AJUSTES.parada.final);
    tremor(palco, AJUSTES.tremor.final, AJUSTES.tremorMs * 1.4);
    palco.classList.remove("foco-final");
    setTimeout(() => alvo.classList.remove("alvo-final"), pausa(500));
  }

  /** Depois que o golpe acertou (o número já subiu): o momento que ele merece. */
  async function golpe(m, palco, alvo) {
    const tipo = m && peso(m);
    if (!tipo || rapido() || !palco || !alvo) return;
    if (tipo === "final") return golpeFinal(palco, alvo);
    await parada(palco, alvo, AJUSTES.parada[tipo]);
    tremor(palco, AJUSTES.tremor[tipo]);
  }

  /* ------------------------------------------------------------ contar e encher */
  /** Um número que sobe contando até o valor, com um tique a cada passo (poucos tiques, para não cansar). */
  function contar(el, ate, ms = AJUSTES.contarMs) {
    if (rapido() || !ate) { el.textContent = ate; return Promise.resolve(); }
    const passos = Math.min(AJUSTES.tiquesMax, ate);
    return new Promise((fim) => {
      const inicio = performance.now();
      let dado = 0;
      const passo = (agora) => {
        const t = Math.min(1, (agora - inicio) / pausa(ms));
        el.textContent = Math.round(ate * (1 - Math.pow(1 - t, 2)));
        const n = Math.floor(t * passos);
        if (n > dado) { dado = n; Som.tocar("tique"); }
        if (t < 1) requestAnimationFrame(passo); else fim();
      };
      requestAnimationFrame(passo);
    });
  }
  /** Uma barra (o preenchimento é o primeiro filho) indo de uma fração a outra. */
  function encher(barra, de, ate, ms) {
    const fill = barra.firstElementChild;
    if (rapido()) { fill.style.width = ate * 100 + "%"; return Promise.resolve(); }
    return fill.animate([{ width: de * 100 + "%" }, { width: ate * 100 + "%" }],
      { duration: pausa(ms), easing: "cubic-bezier(.3,.7,.4,1)", fill: "forwards" }).finished.catch(() => {});
  }

  /* ------------------------------------------------------------ o espólio da vitória */
  /** O ouro conta subindo e voa até a bolsa; a barra de XP enche (e, se o nível vira, enche, brilha e
   *  recomeça). Some sozinho no fim; um clique ou uma tecla adianta. Os trechos da barra vêm do motor. */
  async function espolio(caixa, d) {
    const S = (n, e = 1) => Sprites.img(n, e);
    caixa.innerHTML = `<div class="festa festa-espolio">
      <div class="rotulo-festa">espólio</div>
      ${d.ouro ? `<div class="espolio-ouro">${S("moeda", 2)}<b>+<span class="conta">0</span></b><small>ouro</small></div>` : ""}
      <div class="espolio-xp"><div class="espolio-nivel">Nível <b>${d.nivel}</b></div>
        <div class="espolio-barra"><i></i></div><div class="espolio-mais">+${d.xp} XP</div></div></div>`;
    caixa.classList.add("leve");
    caixa.hidden = false;
    let pular = false;
    const adiantar = (ev) => { if (ev.type === "keydown" && ![" ", "Enter", "Escape"].includes(ev.key)) return; ev.preventDefault(); ev.stopPropagation(); pular = true; };
    document.addEventListener("pointerdown", adiantar, true);
    document.addEventListener("keydown", adiantar, true);
    const festa = caixa.querySelector(".festa-espolio");
    const barra = caixa.querySelector(".espolio-barra"), nivelEl = caixa.querySelector(".espolio-nivel b");
    const primeiro = d.trechos[0];
    if (primeiro) barra.firstElementChild.style.width = (primeiro[0] / primeiro[2]) * 100 + "%";
    await dormir(pausa(AJUSTES.espolioEsperaMs));  // a faixa de "Vitória" sai antes
    if (d.ouro) {
      Som.tocar("moeda");
      await contar(caixa.querySelector(".espolio-ouro .conta"), d.ouro);
      Telas.moedasPara(caixa.querySelector(".espolio-ouro"), document.querySelector('.recurso[data-rec="ouro"]'));
    }
    let nivel = d.nivel;
    for (const [de, ate, total] of d.trechos) {
      if (pular) break;
      await encher(barra, de / total, ate / total, AJUSTES.barraMs);
      if (ate >= total) {  // o nível virou: a barra brilha, o número sobe, e ela recomeça
        nivel += 1;
        nivelEl.textContent = nivel;
        festa.classList.remove("subiu"); void festa.offsetWidth; festa.classList.add("subiu");
        Som.tocar("nivel");
        await dormir(pausa(350));
      }
    }
    if (!pular) await Promise.race([dormir(pausa(AJUSTES.espolioFicaMs)), new Promise((r) => { const t = setInterval(() => { if (pular) { clearInterval(t); r(); } }, 50); })]);
    document.removeEventListener("pointerdown", adiantar, true);
    document.removeEventListener("keydown", adiantar, true);
    festa.classList.add("saindo");
    await dormir(220);
    caixa.hidden = true; caixa.innerHTML = ""; caixa.classList.remove("leve");
  }

  return { AJUSTES, configurar, peso, maisPesado, tremor, parada, golpe, contar, encher, espolio };
})();
