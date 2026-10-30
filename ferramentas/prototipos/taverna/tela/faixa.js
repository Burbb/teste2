/* A demonstração da taverna (protótipo): um botão "Protótipo" na barra do alto, entre os sigilos e o menu (no fluxo
   da barra: o clima, a hora e os sigilos não ficam embaixo dele), abre o painel: a G3 (o padrão: a G2 aprovada com as
   correções locais), a G2 e a G original (a troca é imediata, no mesmo estado do jogo), a H e a prova de qualidade
   (histórico), e o estudo livre "Diante de Morel", numa vista à parte (fora da HUD) (os jogadores
   nas grades A e B; na B2, a B refinada pela referência; na B3, a B2 com os braços legíveis; e na B4, a B3 com o
   ombro do de verde suavizado; com a vista isolada), o canto de Morel (o M1, o novo, ou o da F), as candidatas (da F
   à A, o histórico), o estado do save temporário (a despensa esperando, o homem do canto, Morel já conhecido, Morel
   recrutado, sem ouro) e a pose parada. Escolhido, o painel fecha; o botão diz as versões à vista ("Protótipo: G4 ·
   Homem do canto", "Protótipo: prova B4 · Morel M1 · ..."). O interior entra pelo caminho do templo (vila.js, estado.local.interiores, com a taverna
   acrescentada pelo demo.py). */
"use strict";

(() => {
  if (typeof ACOES_OCULTAS !== "undefined") ["tav_estado", "tav_dado", "tav_bebida"].forEach((k) => { if (!ACOES_OCULTAS.includes(k)) ACOES_OCULTAS.push(k); });
  const naTaverna = () => !!(window.Cenas && Cenas.atual() && Cenas.atual().d.cena === "taverna");
  const ESTADOS = [["despensa", "Despensa esperando"], ["homem_do_canto", "Homem do canto (60 de ouro)"],
    ["pouco_ouro", "Homem do canto, 30 de ouro (sem os 40)"], ["quase_sem_ouro", "Homem do canto, 10 de ouro (nem os 25)"],
    ["conhecido", "Morel conhecido"], ["recrutado", "Morel recrutado"], ["sem_ouro", "Sem ouro"]];
  // os casos de teste do encontro (demo.py): o dado da queda de braço e Morel na próxima bebida, só onde as regras deixam
  const DADOS = [["sorteio", "Queda de braço: o sorteio"], ["ganhar", "Queda de braço: o dado em 20 (vence)"],
    ["perder", "Queda de braço: o dado em 1 (perde)"]];
  const BEBIDAS = [["sorteio", "Bebida: o sorteio de sempre"], ["morel", "Bebida: Morel puxa conversa (se ele pode)"]];
  const f = document.createElement("div");
  f.id = "faixa-tav";
  document.body.dataset.tavCand = document.body.dataset.tavCand || "g4";  // o balcão animado; as outras para comparar
  document.body.dataset.tavProva = document.body.dataset.tavProva || "b4";
  document.body.dataset.tavMorel = document.body.dataset.tavMorel || "m1";
  const CANDS = [["g4", "Balcão animado (G4, a atuação ajustada)"], ["g4v1", "Balcão animado, a atuação anterior"],
    ["morel", "Diante de Morel (animada)"],
    ["morel2", "Diante de Morel, a segunda versão (antes do estudo do braço)"],
    ["morel1", "Diante de Morel, a primeira versão"], ["g3", "G3 estática"],
    ["g2", "G2 aprovada (antes das correções)"], ["g", "G original"], ["h", "Candidata H (histórico)"], ["prova", "Prova: os jogadores (histórico)"], ["f", "Candidata F (histórico)"], ["e", "Candidata E (histórico)"],
    ["d", "Candidata D (histórico)"], ["c", "Candidata C (histórico)"], ["b", "Candidata B (histórico)"], ["a", "Candidata A (histórico)"]];
  const GRADES = [["a", "Grade A: a atual (66×42)"], ["b", "Grade B: o dobro (132×84)"],
                  ["b2", "Grade B2: a B refinada pela referência (132×84)"],
                  ["b3", "Grade B3: a B2 com ombros e braços legíveis (132×84)"],
                  ["b4", "Grade B4: a B3 com o ombro de cá do de verde suavizado (132×84)"]];
  const MORELS = [["m1", "Morel M1: Morel, a cadeira e a mesa novos"], ["f", "Morel F: o canto anterior"]];
  f.innerHTML = `<button type="button" class="abre" aria-expanded="false" aria-controls="faixa-tav-painel"></button>
    <div id="faixa-tav-painel" hidden><b>Taverna (protótipo): a candidata</b>
    ${CANDS.map(([id, nome]) => `<button type="button" data-cand="${id}" aria-pressed="${id === document.body.dataset.tavCand}">${nome}</button>`).join("")}
    <b>A prova de qualidade (os jogadores, histórico)</b>
    ${GRADES.map(([id, nome]) => `<button type="button" data-grade="${id}" aria-pressed="${id === document.body.dataset.tavProva}">${nome}</button>`).join("")}
    <button type="button" data-isolado aria-pressed="false">Isolado (fundo neutro, mesmo tamanho)</button>
    <b>O canto de Morel</b>
    ${MORELS.map(([id, nome]) => `<button type="button" data-morel="${id}" aria-pressed="${id === document.body.dataset.tavMorel}">${nome}</button>`).join("")}
    <b>O estado do save temporário</b>
    ${ESTADOS.map(([id, nome]) => `<button type="button" data-tav="${id}" aria-pressed="${id === "homem_do_canto"}">${nome}</button>`).join("")}
    <b>O encontro com Morel (casos de teste)</b>
    ${DADOS.map(([id, nome]) => `<button type="button" data-dado="${id}" aria-pressed="${id === "sorteio"}">${nome}</button>`).join("")}
    ${BEBIDAS.map(([id, nome]) => `<button type="button" data-bebida="${id}" aria-pressed="${id === "sorteio"}">${nome}</button>`).join("")}
    <button type="button" data-reduzido aria-pressed="false">Pose parada</button>
    <b>Inspeção ampliada (fora da HUD)</b>
    <button type="button" data-estudo="vista">Diante de Morel: a vista adaptada (pose parada)</button>
    <button type="button" data-estudo="construcao">Diante de Morel: o estudo de construção e a aplicação</button>
    <button type="button" data-estudo="trajetorias">Diante de Morel: as trajetórias do cotovelo, da mão e da colher</button>
    <button type="button" data-estudo="estudo">Diante de Morel: o estudo livre (histórico)</button></div><span class="aviso"></span>`;
  const topo = document.getElementById("topo");
  topo.insertBefore(f, document.getElementById("acoes-topo"));
  const abre = f.querySelector(".abre"), painel = f.querySelector("#faixa-tav-painel"), aviso = f.querySelector(".aviso");
  document.body.appendChild(painel);  // o painel fica fora da barra (que rola na janela estreita) e cai embaixo do botão
  const abrir = (sim) => {
    const r = abre.getBoundingClientRect();
    Object.assign(painel.style, { left: Math.round(r.left) + "px", top: Math.round(r.bottom + 3) + "px" });
    painel.hidden = !sim; abre.setAttribute("aria-expanded", String(sim));
  };
  abre.addEventListener("click", () => abrir(painel.hidden));
  const rotulo = () => {
    const e = painel.querySelector('[data-tav][aria-pressed="true"]');
    const c = document.body.dataset.tavCand;
    const qual = c === "prova"
      ? `prova ${document.body.dataset.tavProva.toUpperCase()} · Morel ${document.body.dataset.tavMorel.toUpperCase()}` : c.toUpperCase();
    abre.textContent = `Protótipo: ${qual} · ${e ? e.textContent : ""}`;
  };
  rotulo();                                                     // a versão à vista desde a entrada
  painel.querySelectorAll("[data-cand]").forEach((b) => b.addEventListener("click", () => {
    abrir(false);
    document.body.dataset.tavCand = b.dataset.cand;
    painel.querySelectorAll("[data-cand]").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    rotulo();
    if (naTaverna()) Cenas.mostrar(Cenas.atual().d);  // a outra sala, com os pontos dela
  }));
  document.addEventListener("keydown", (ev) => { if (ev.key === "Escape" && !painel.hidden) { ev.stopPropagation(); abrir(false); abre.focus(); } }, true);
  painel.querySelectorAll("[data-tav]").forEach((b) => b.addEventListener("click", () => {
    abrir(false);
    const volta = naTaverna();
    if (volta && pergunta && pergunta.voltarLocal) pergunta.voltarLocal();
    setTimeout(() => {
      const ok = App.acao({ tav_estado: b.dataset.tav });
      aviso.textContent = ok ? "" : "Volte à vila para trocar o estado.";
      if (!ok) return;
      painel.querySelectorAll("[data-tav]").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      rotulo();
      if (volta) predioPedido = "taverna";  // a vila se remonta e entra de novo na taverna
    }, volta ? 60 : 0);
  }));
  // o dado e a bebida (sem mexer no save): o balcão é o próprio menu da vila, então a resposta vai direto; a vila se
  // remonta e entra de novo na taverna
  [["dado", "tav_dado"], ["bebida", "tav_bebida"]].forEach(([d, meta]) => painel.querySelectorAll(`[data-${d}]`).forEach((b) => b.addEventListener("click", () => {
    abrir(false);
    const volta = naTaverna();
    if (volta) predioPedido = "taverna";
    const ok = App.acao({ [meta]: b.dataset[d] });
    aviso.textContent = ok ? "" : "Termine a conversa para trocar o caso de teste.";
    if (!ok) { if (volta) predioPedido = null; return; }
    painel.querySelectorAll(`[data-${d}]`).forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
  })));
  painel.querySelectorAll("[data-grade]").forEach((b) => b.addEventListener("click", () => {
    abrir(false);
    document.body.dataset.tavProva = b.dataset.grade;            // a troca é imediata, no mesmo lugar (a camada lê a cada quadro)
    painel.querySelectorAll("[data-grade]").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    rotulo();
  }));
  painel.querySelectorAll("[data-morel]").forEach((b) => b.addEventListener("click", () => {
    abrir(false);
    document.body.dataset.tavMorel = b.dataset.morel;            // o fundo, as velas e a camada trocam no quadro seguinte
    painel.querySelectorAll("[data-morel]").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    rotulo();
    if (naTaverna()) Cenas.mostrar(Cenas.atual().d);              // o ponto do Homem do canto segue a versão
  }));
  painel.querySelector("[data-isolado]").addEventListener("click", (ev) => {
    abrir(false);
    const sim = document.body.dataset.tavIsolado !== "1";
    document.body.dataset.tavIsolado = sim ? "1" : "";
    ev.currentTarget.setAttribute("aria-pressed", String(sim));
  });
  // O estudo de Morel: uma vista à parte, por cima de tudo, na resolução dele (360×120), em ampliação inteira (o padrão
  // é a maior que cabe na janela) ou no tamanho nativo; "Caber na janela" é uma prévia reduzida, dita na legenda, para
  // não confundir um problema de exibição com a qualidade do desenho. Esc ou Fechar voltam ao jogo.
  const estudo = document.createElement("div");
  estudo.id = "estudo-morel"; estudo.hidden = true;
  estudo.innerHTML = `<div class="barra"><b class="titulo"></b>
    <span class="tam"></span><span class="zooms"></span><button type="button" data-fechar>Fechar (Esc)</button></div>
    <div class="quadro"><img alt="Estudo: sentado diante de Morel, na taverna" src="/proto-tav/camadas/morel/estudo.png"></div>`;
  document.body.appendChild(estudo);
  const img = estudo.querySelector("img"), tam = estudo.querySelector(".tam"), zooms = estudo.querySelector(".zooms");
  const VISTAS = {
    vista: { src: "/proto-tav/camadas/morel-vista/parada.png", nat: [320, 96], titulo: "Diante de Morel: a vista adaptada (pose parada)" },
    construcao: { src: "/proto-tav/camadas/morel-vista/construcao.png", nat: [480, 192],
      titulo: "Diante de Morel: o estudo de construção (em cima) e a aplicação (embaixo), pose a pose" },
    trajetorias: { src: "/proto-tav/camadas/morel-vista/trajetorias.png", nat: [192, 96],
      titulo: "Diante de Morel: as trajetórias de uma volta (cotovelo, mão, ponta da colher), antes e depois" },
    estudo: { src: "/proto-tav/camadas/morel/estudo.png", nat: [360, 120], titulo: "Diante de Morel: o estudo livre (histórico)" },
  };
  let NAT = [360, 120];
  const maior = () => Math.max(1, Math.floor(Math.min((innerWidth - 32) / NAT[0], (innerHeight - 90) / NAT[1])));
  function zoom(z) {
    const caber = z === "caber";
    const k = caber ? Math.min((innerWidth - 32) / NAT[0], (innerHeight - 90) / NAT[1]) : z;
    Object.assign(img.style, { width: Math.round(NAT[0] * k) + "px", height: Math.round(NAT[1] * k) + "px" });
    tam.textContent = caber && !Number.isInteger(k)
      ? `prévia ajustada à janela (${k.toFixed(2)}×): não é a arte fiel`
      : `${k}× (${NAT[0] * k}×${NAT[1] * k}), fiel: cada pixel da arte em ${k}×${k}`;
    zooms.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(String(z) === b.dataset.z)));
  }
  zooms.innerHTML = [1, 2, 3, 4, 5, 6].map((z) => `<button type="button" data-z="${z}">${z === 1 ? "Nativo (1×)" : z + "×"}</button>`).join("")
    + `<button type="button" data-z="caber">Caber na janela</button>`;
  zooms.querySelectorAll("button").forEach((b) => b.addEventListener("click", () => zoom(b.dataset.z === "caber" ? "caber" : +b.dataset.z)));
  const fecharEstudo = () => { estudo.hidden = true; abre.focus(); };
  estudo.querySelector("[data-fechar]").addEventListener("click", fecharEstudo);
  document.addEventListener("keydown", (ev) => { if (ev.key === "Escape" && !estudo.hidden) { ev.stopPropagation(); ev.preventDefault(); fecharEstudo(); } }, true);
  painel.querySelectorAll("[data-estudo]").forEach((bt) => bt.addEventListener("click", () => {
    abrir(false);
    const v = VISTAS[bt.dataset.estudo];
    NAT = v.nat; img.src = v.src; estudo.querySelector(".titulo").textContent = v.titulo;
    estudo.hidden = false;
    zoom(maior());
    estudo.querySelector("[data-fechar]").focus();
  }));
  painel.querySelector("[data-reduzido]").addEventListener("click", (ev) => {
    const sim = document.body.dataset.tavReduzido !== "1";
    document.body.dataset.tavReduzido = sim ? "1" : "";
    ev.currentTarget.setAttribute("aria-pressed", String(sim));
  });
})();
