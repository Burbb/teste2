/* Sensação: o peso dos momentos do jogo. As telas (batalha.js, telas/) dizem O QUE aconteceu; aqui mora
   COMO aquilo se sente: quanto o tempo para no impacto, quanto a arena treme, como a câmera chega perto do
   golpe que encerra a luta. Os números ficam todos em AJUSTES, para afinar sem caçar setTimeout pelo código.

   O motor marca os fatos no lance do golpe (crit, abate, final); quem anima só pergunta Sensacao.golpe(). */
"use strict";

const Sensacao = (() => {
  const AJUSTES = {
    // Quanto tempo tudo congela no quadro do impacto (hit-stop, como em Hades e Dead Cells), em ms. O golpe final
    // não congela: tem câmera lenta (abaixo).
    parada: { critico: 80, abate: 70 },
    // Quanto a arena treme, em px (e por quanto tempo, em ms).
    tremor: { leve: 3, critico: 5, abate: 7, final: 11 },
    tremorMs: 340,
    // O golpe final: em vez de congelar, o tempo da arena desacelera enquanto o golpe chega (ritmo `lento`, em
    // `entradaMs`), segue devagar no choque (`seguraMs`) e volta acelerando (`saidaMs`). A câmera chega perto de
    // quem cai em tempo real, e o resto escurece.
    final: { lento: 0.3, entradaMs: 220, seguraMs: 380, saidaMs: 450, zoom: 1.08, zoomMs: 520 },
    // Números que contam subindo (ouro do espólio): duração e o máximo de tiques de som.
    contarMs: 650, tiquesMax: 10, espolioOuroMs: 500,
    // A barra de XP enchendo (por trecho de nível) e os respiros do espólio, que fica até o Continuar. O ouro do
    // espólio conta mais depressa (`espolioOuroMs`), e a experiência vem logo depois (`espolioEntreMs`).
    barraMs: 700, espolioEsperaMs: 450, espolioEntreMs: 100,
    // Vida por um fio: o compasso do pulso (ms entre batidas), mais rápido quanto mais perto do fim, e quantas
    // vezes o coração soa ao entrar na faixa (depois só a tela pulsa: som contínuo cansa e angustia).
    batimentoLentoMs: 1150, batimentoRapidoMs: 700, batidasAoEntrar: 3,
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

  /* ------------------------------------------------------------ o relógio da arena */
  // Na câmera lenta o tempo da arena anda devagar: as animações dela (as que estão rodando e as que nascerem) e os
  // prazos que a batalha marca com depois() (tirar o tremor da carta, sumir com o número), para nada ser cortado no
  // meio. Fora dela, tudo anda a 1 e depois() é um setTimeout comum. A câmera (TEMPO_REAL) anda no tempo de fora.
  const TEMPO_REAL = "tempo-real";
  let ritmo = 1, palcoLento = null, quadro = null, ultimo = 0;
  let mudanca = 0;  // a mudança de ritmo em curso; repor() a interrompe
  const prazos = new Set();
  function tique(t) {
    const dt = t - ultimo;
    ultimo = t;
    if (palcoLento) {
      for (const a of palcoLento.getAnimations({ subtree: true })) if (a.id !== TEMPO_REAL && a.playbackRate !== ritmo) a.playbackRate = ritmo;
    }
    for (const p of [...prazos]) { p.resta -= dt * ritmo; if (p.resta <= 0) { prazos.delete(p); p.fn(); } }
    quadro = palcoLento || prazos.size ? requestAnimationFrame(tique) : null;
  }
  function andar() { if (!quadro) { ultimo = performance.now(); quadro = requestAnimationFrame(tique); } }
  /** Faz `fn` depois de `ms` do tempo da arena. */
  function depois(ms, fn) {
    if (!palcoLento) return setTimeout(fn, ms);
    prazos.add({ resta: ms, fn });
    andar();
  }
  /** Leva o ritmo da arena até `alvo` em `ms` (tempo de fora), suave. Voltando a 1, a arena se solta. */
  function mudarRitmo(palco, alvo, ms, curva = (k) => 1 - (1 - k) * (1 - k)) {
    palcoLento = palco;
    andar();
    const de = ritmo, t0 = performance.now(), esta = ++mudanca;
    return new Promise((fim) => {
      const passo = (t) => {
        if (esta !== mudanca) return fim();  // outra mudança (ou o repor) tomou o lugar desta
        const k = ms > 0 ? Math.min(1, (t - t0) / ms) : 1;
        ritmo = de + (alvo - de) * curva(k);
        if (k < 1) return requestAnimationFrame(passo);
        if (alvo === 1) soltar();
        fim();
      };
      requestAnimationFrame(passo);
    });
  }
  function soltar() {
    if (!palcoLento) return;
    for (const a of palcoLento.getAnimations({ subtree: true })) if (a.id !== TEMPO_REAL) a.playbackRate = 1;
    palcoLento = null;
    ritmo = 1;
    for (const p of prazos) setTimeout(p.fn, Math.max(0, p.resta));  // o que faltava, agora em tempo normal
    prazos.clear();
  }

  /* ------------------------------------------------------------ o golpe final */
  // Câmera lenta, como nos jogos de luta: o tempo desacelera enquanto o golpe chega (a investida, a flecha no ar),
  // segue devagar no choque e volta acelerando; a câmera chega perto de quem cai e o resto escurece. Nada para de
  // vez: congelar a tela no impacto parecia o jogo travando.
  let foco = null;
  function aproximar(palco, alvo) {
    if (foco) return;
    const cfg = AJUSTES.final;
    const p = palco.getBoundingClientRect(), a = alvo.getBoundingClientRect();
    palco.style.transformOrigin = `${a.left + a.width / 2 - p.left}px ${a.top + a.height / 2 - p.top}px`;
    palco.classList.add("foco-final");
    alvo.classList.add("alvo-final");
    const zoom = palco.animate([{ transform: "scale(1)" }, { transform: `scale(${cfg.zoom})` }],
      { duration: pausa(cfg.zoomMs), easing: "cubic-bezier(.2,.7,.3,1)", fill: "forwards", id: TEMPO_REAL });
    foco = { palco, alvo, zoom };
    mudarRitmo(palco, cfg.lento, pausa(cfg.entradaMs));
  }
  /** Sai da câmera lenta na hora, sem a volta suave. O golpe final pulado no meio (o clique que adianta) não passa
   *  pelo afastar(): sem isto, a arena seguia lenta e de perto até a luta seguinte. */
  function repor() {
    mudanca++;
    if (foco) {
      const { palco, alvo, zoom } = foco;
      foco = null;
      zoom.cancel();
      palco.classList.remove("foco-final");
      alvo.classList.remove("alvo-final");
    }
    soltar();
  }
  async function afastar() {
    if (!foco) return;
    const { palco, alvo, zoom } = foco, cfg = AJUSTES.final;
    foco = null;
    const volta = palco.animate([{ transform: `scale(${cfg.zoom})` }, { transform: "scale(1)" }],
      { duration: pausa(cfg.saidaMs), easing: "ease-in-out", fill: "forwards", id: TEMPO_REAL });
    zoom.cancel();
    palco.classList.remove("foco-final");
    await mudarRitmo(palco, 1, pausa(cfg.saidaMs), (k) => k * k);
    volta.cancel();
    alvo.classList.remove("alvo-final");
  }

  /** Antes de o golpe sair (a carta ainda vai avançar, a flecha ainda vai voar): se é o golpe que encerra a luta,
   *  a câmera chega perto e o tempo desacelera primeiro, para a investida e o choque acontecerem em câmera lenta. */
  async function antesDoGolpe(m, palco, alvo) {
    repor();  // o que sobrou de um golpe final que não chegou ao fim (refletido, pulado) não entra neste
    if (!m || peso(m) !== "final" || rapido() || !palco || !alvo) return;
    aproximar(palco, alvo);
    await dormir(pausa(AJUSTES.final.entradaMs));
  }

  async function golpeFinal(palco, alvo) {
    aproximar(palco, alvo);  // numa salva não há "antes": a câmera lenta começa no impacto
    Som.tocar("golpe_final");
    alvo.classList.add("lampejo");
    setTimeout(() => alvo.classList.remove("lampejo"), pausa(110));
    tremor(palco, AJUSTES.tremor.final, AJUSTES.tremorMs * 1.4);
    await dormir(pausa(AJUSTES.final.seguraMs));
    await afastar();
  }

  /** Depois que o golpe acertou (o número já subiu): o momento que ele merece. */
  async function golpe(m, palco, alvo) {
    const tipo = m && peso(m);
    if (rapido()) { repor(); return; }  // pulou: se a câmera lenta já tinha começado (antesDoGolpe), ela sai agora
    if (!tipo || !palco || !alvo) return;
    if (tipo === "final") return golpeFinal(palco, alvo);
    await parada(palco, alvo, AJUSTES.parada[tipo]);
    tremor(palco, AJUSTES.tremor[tipo]);
  }

  /* ------------------------------------------------------------ vida por um fio */
  // Abaixo do limiar (o motor diz qual: heroi.vida_por_um_fio), a borda da tela e a barra de vida pulsam em
  // vermelho no compasso de um coração, mais depressa quanto menos vida resta. O coração só SOA ao entrar na
  // faixa (o aviso, umas poucas batidas) e se cala; o pulso na tela continua. Acima do limiar, ou caído, nada.
  let limiar = 0.3, desde = null, batidas = null;
  function vidaDoHeroi(hp, max, novoLimiar) {
    if (novoLimiar) limiar = novoLimiar;
    const fracao = max ? hp / max : 1, corpo = document.body;
    if (!(hp > 0 && fracao <= limiar)) {
      if (desde !== null) { desde = null; clearTimeout(batidas); corpo.classList.remove("por-um-fio"); }
      return;
    }
    const urgencia = Math.max(0, Math.min(1, 1 - fracao / limiar));
    const ms = Math.round(AJUSTES.batimentoLentoMs - (AJUSTES.batimentoLentoMs - AJUSTES.batimentoRapidoMs) * urgencia);
    corpo.style.setProperty("--batimento", ms + "ms");
    if (desde === null) {  // acabou de entrar na faixa
      desde = performance.now();
      corpo.classList.add("por-um-fio");
      bater(AJUSTES.batidasAoEntrar, ms);
    }
    // A barra de vida nasce de novo a cada redesenho da HUD; o atraso negativo a põe no compasso da borda.
    corpo.style.setProperty("--fio-fase", -Math.round(performance.now() - desde) + "ms");
  }
  function bater(n, ms) {
    if (!document.hidden) Som.tocar("batimento");
    batidas = n > 1 ? setTimeout(() => bater(n - 1, ms), ms) : null;
  }

  /* ------------------------------------------------------------ contar e encher */
  /** Um número que sobe contando até o valor (a partir de `de`), com um tique a cada passo (poucos tiques, para não
   *  cansar; `tiques: false` conta calado). */
  function contar(el, ate, ms = AJUSTES.contarMs, { de = 0, tiques = true } = {}) {
    if (rapido() || ate === de) { el.textContent = ate; return Promise.resolve(); }
    const passos = tiques ? Math.min(AJUSTES.tiquesMax, ate - de) : 0;
    return new Promise((fim) => {
      const inicio = performance.now();
      let dado = 0;
      const passo = (agora) => {
        const t = Math.min(1, (agora - inicio) / pausa(ms));
        el.textContent = Math.round(de + (ate - de) * (1 - Math.pow(1 - t, 2)));
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
  // O que se acha (o motor manda o id; a tela escolhe o ícone e escreve a quantidade do jeito de cada coisa).
  // As flechas dizem tudo na quantidade ("+2 flechas"): o nome ao lado seria repetido.
  const quantoAchou = (x) => (x.id === "comida" ? `+${Texto.plural(x.qtd, "dia")}` : x.id === "flechas" ? `+${Texto.plural(x.qtd, "flecha")}` : `×${x.qtd}`);
  const esc = Texto.html;

  /** Como a tela de resultado dos jogos, tudo o que a vitória deu num quadro só: uma linha por recompensa (o ouro,
   *  depois a experiência com a barra de nível presa embaixo dela), e por fim o que se achou (comida, bandagem,
   *  flechas; o equipamento tem a janela dele, logo depois) e os contratos que andaram. O ouro conta e voa
   *  até a bolsa; a barra enche (se o nível vira: enche, brilha e recomeça). Um clique ou uma tecla adianta os
   *  números; o quadro só sai no Continuar. Os trechos da barra vêm do motor. */
  async function espolio(caixa, d) {
    const S = (n, e = 1) => Sprites.img(n, e);
    const trechos = d.trechos || [], ultimo = trechos[trechos.length - 1] || [0, 0, 1], primeiro = trechos[0] || ultimo;
    const achados = (d.itens || []).map((x) => `<span class="achado-espolio">${Icones.consumivel(x.id) || S(Telas.iconeConsumivel(x.id, "saco"), 2)}${x.id === "flechas" ? "" : esc(x.nome)}<b>${quantoAchou(x)}</b></span>`);
    // Cada contrato: o nome (o que ele pede), o estado curto à direita e, cumprido, onde a recompensa sai, embaixo do
    // nome e em segundo plano (ela é paga sozinha na chegada a uma vila: aqui não há o que clicar).
    const contratos = (d.contratos || []).map((c) => `<div class="espolio-contrato${c.concluido ? " feito" : ""}">${S("pergaminho", 2)}
      <span class="ec-texto"><span class="ec-nome">${esc(c.desc.replace(/\.$/, ""))}</span>${c.concluido ? '<small class="ec-onde">Recompensa ao chegar a qualquer vila</small>' : ""}</span>
      <b>${c.concluido ? "Concluído" : esc(c.progresso)}</b></div>`).join("");
    // Vários baús abertos juntos: os equipamentos que saíram ficam listados no resumo (cada um vem depois, na janela
    // dele, para comparar e decidir).
    const equips = (d.equipamentos || []).map((it) => `<span class="achado-espolio equip-espolio rar-${esc(it.raridade)}">${Icones.item(it.icone) || S(it.icone, 2)}${esc(it.nome)}</span>`);
    const extras = achados.length || contratos || equips.length;
    // Vários baús abertos juntos: a pilha (um ícone por baú, até cinco, caindo um depois do outro) e o ×N grande ao
    // lado, para ver de relance quantos foram. N é o que o motor abriu (saiu da bolsa).
    const pilha = d.baus > 1 ? `<div class="espolio-baus" style="--n:${Math.min(d.baus, 5)}">
      <span class="eb-pilha">${Array.from({ length: Math.min(d.baus, 5) }, (_, i) => `<span style="--i:${i}">${Icones.consumivel("bau", 48) || S(Telas.iconeConsumivel("bau", "bau"), 3)}</span>`).join("")}</span>
      <b class="eb-qtd">×${d.baus}</b></div>` : "";
    caixa.innerHTML = `<div class="festa festa-espolio">
      <div class="rotulo-festa">${esc(d.titulo || "espólio")}</div>${pilha}
      ${d.frase ? `<p class="espolio-frase">${esc(d.frase)}</p>` : ""}
      ${d.ouro ? `<div class="espolio-linha ouro">${Icones.moeda(32) || S("moeda", 2)}<span class="nome">Ouro</span><b>+<span class="conta">0</span></b></div>` : ""}
      ${d.xp ? `<div class="espolio-xp${d.ouro ? " esperando" : ""}">
        <div class="espolio-linha xp">${S("estrela", 2)}<span class="nome">Experiência</span><b>+<span class="conta">0</span> <small>XP</small></b></div>
        <div class="espolio-nivel"><span>Nível <b>${d.nivel}</b></span><div class="espolio-barra"><i></i></div>
          <span class="espolio-faltam"><span class="conta">${primeiro[0]}</span>/<span class="total">${primeiro[2]}</span></span></div>
      </div>` : ""}
      ${extras ? `<div class="espolio-extras${d.ouro || d.xp ? " esperando" : ""}">${achados.length ? `<div class="espolio-achados">${achados.join("")}</div>` : ""}${equips.length ? `<div class="espolio-equips"><div class="espolio-equips-rotulo">${equips.length === 1 ? "Equipamento" : `${equips.length} equipamentos`}</div><div class="espolio-achados">${equips.join("")}</div></div>` : ""}${contratos}</div>` : ""}
    </div>`;
    caixa.classList.add("leve");
    caixa.hidden = false;
    const festa = caixa.querySelector(".festa-espolio");
    Telas.noPalco(festa);
    let pular = false;
    const adiantar = (ev) => { if (ev.type === "keydown" && ![" ", "Enter", "Escape"].includes(ev.key)) return; ev.preventDefault(); ev.stopPropagation(); pular = true; };
    document.addEventListener("pointerdown", adiantar, true);
    document.addEventListener("keydown", adiantar, true);
    const mostrar = (el) => el && el.classList.remove("esperando");
    if (d.titulo) Som.tocar("bau");  // um baú aberto: o tilintar da recompensa antes das moedas
    await dormir(pausa(AJUSTES.espolioEsperaMs));  // a faixa de "Vitória" sai antes
    if (d.ouro) {
      Som.tocar("moeda");
      await contar(caixa.querySelector(".espolio-linha.ouro .conta"), d.ouro, AJUSTES.espolioOuroMs);
      Telas.moedasPara(caixa.querySelector(".espolio-linha.ouro"), document.querySelector('.recurso[data-rec="ouro"]'));
      await dormir(pausa(AJUSTES.espolioEntreMs));
    }
    if (d.xp) {
      mostrar(caixa.querySelector(".espolio-xp"));  // a experiência chega depois do ouro, numa linha dela
      const barra = caixa.querySelector(".espolio-barra"), nivelEl = caixa.querySelector(".espolio-nivel b");
      const noNivel = caixa.querySelector(".espolio-faltam .conta"), totalEl = caixa.querySelector(".espolio-faltam .total");
      barra.firstElementChild.style.width = (primeiro[0] / primeiro[2]) * 100 + "%";
      contar(caixa.querySelector(".espolio-linha.xp .conta"), d.xp, AJUSTES.barraMs * trechos.length, { tiques: false });
      let nivel = d.nivel;
      for (const [de, ate, total] of trechos) {
        if (pular) break;
        totalEl.textContent = total;
        contar(noNivel, ate, AJUSTES.barraMs, { de, tiques: false });
        await encher(barra, de / total, ate / total, AJUSTES.barraMs);
        if (ate >= total) {  // o nível virou: a barra brilha, o número sobe, e ela recomeça
          nivel += 1;
          nivelEl.textContent = nivel;
          festa.classList.remove("subiu"); void festa.offsetWidth; festa.classList.add("subiu");
          Som.tocar("nivel");
          await dormir(pausa(350));
        }
      }
      if (pular) {  // adiantou: os números vão direto ao fim
        caixa.querySelector(".espolio-linha.xp .conta").textContent = d.xp;
        noNivel.textContent = ultimo[1]; totalEl.textContent = ultimo[2];
      }
    }
    if (extras) {
      if (!pular) await dormir(pausa(AJUSTES.espolioEntreMs));
      mostrar(caixa.querySelector(".espolio-extras"));
      Som.tocar("item");
    }
    // Tudo à vista: o quadro espera o Continuar (qualquer clique, Espaço, Enter ou Esc), sem relógio, pela regra dos
    // gestos das telas (Gesto, em nucleo.js): o primeiro gesto novo fecha na hora. Não fecham o toque que começou
    // antes de o botão aparecer (o que adiantava os números), o 2º clique de um clique duplo nem a tecla segurada.
    // Antes, todo clique no primeiro 0,9 s era ignorado (e cada um estendia a espera): o primeiro Continuar se perdia.
    festa.insertAdjacentHTML("beforeend", '<button class="continuar" type="button">Continuar <span>▸</span></button>');
    // O quadro é uma janela: o foco vai para o Continuar dele (o Tab não precisa atravessar a página escondida atrás) e,
    // fechado o quadro, volta para onde estava. O anel só aparece se o último gesto foi do teclado (:focus-visible).
    const focoAntes = document.activeElement, botao = festa.querySelector(".continuar");
    const prender = (ev) => { if (ev.key === "Tab") { ev.preventDefault(); botao.focus({ preventScroll: true }); } };  // um botão só: o Tab fica nele
    document.addEventListener("keydown", prender, true);
    botao.focus({ preventScroll: true });
    const nasceu = performance.now();
    let toque = 0, fechar = null;
    const tocou = () => { toque = performance.now(); };
    document.addEventListener("pointerdown", tocou, true);
    await new Promise((r) => {
      fechar = (ev) => {
        if (ev.type === "keydown" ? ev.repeat || ![" ", "Enter", "Escape"].includes(ev.key) : ev.detail !== 1 || toque < nasceu) return;
        ev.preventDefault(); ev.stopPropagation();  // o gesto que fecha não atravessa para a página
        r();
      };
      document.addEventListener("click", fechar, true);
      document.addEventListener("keydown", fechar, true);
    });
    document.removeEventListener("pointerdown", tocou, true);
    document.removeEventListener("click", fechar, true);
    document.removeEventListener("keydown", fechar, true);
    document.removeEventListener("pointerdown", adiantar, true);
    document.removeEventListener("keydown", adiantar, true);
    document.removeEventListener("keydown", prender, true);
    festa.classList.add("saindo");
    await dormir(220);
    caixa.hidden = true; caixa.innerHTML = ""; caixa.classList.remove("leve");
    if (focoAntes && focoAntes !== document.body && focoAntes.isConnected) focoAntes.focus({ preventScroll: true });
  }

  return { AJUSTES, configurar, peso, maisPesado, tremor, parada, antesDoGolpe, golpe, repor, depois, contar, encher,
    espolio, vidaDoHeroi };
})();
