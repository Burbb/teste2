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

  return { AJUSTES, configurar, peso, maisPesado, tremor, parada, golpe };
})();
