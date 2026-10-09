/* Celebrações: as festas por cima do jogo (nível, Sigilo, especialização, espólio, contratos pagos, atributo
   permanente, chegada, amanhecer), os itens que voam até onde moram e a linha que cada festa deixa no histórico. */
"use strict";

(() => {
  const { h, S, cartaz, chegando, fecharAchado, iconeItem, moedasPara, noPalco } = Telas;

  function particulas(cores, n = 60) {
    const cx = window.innerWidth / 2, cy = window.innerHeight * 0.42;
    for (let i = 0; i < n; i++) {
      const p = document.createElement("i");
      p.className = "particula";
      const ang = Math.random() * Math.PI * 2, dist = 120 + Math.random() * 320;
      p.style.left = cx + "px"; p.style.top = cy + "px";
      p.style.background = cores[i % cores.length];
      p.style.setProperty("--dx", Math.cos(ang) * dist + "px");
      p.style.setProperty("--dy", Math.sin(ang) * dist * 0.7 + "px");
      p.style.animationDelay = Math.random() * 0.25 + "s";
      document.body.appendChild(p);
      setTimeout(() => p.remove(), 1600);
    }
  }

  /** Um atributo para sempre (+2 Ataque de um evento): um selo surge no meio da tela, voa até o atributo (no painel;
   *  vida e recurso máximos, na barra da HUD), que brilha e conta até o valor novo. Não segura o jogo: o texto segue
   *  enquanto o selo voa. */
  const ICONE_SELO = { atk: "espada", defesa: "escudo", agi: "folha", poder: "chama", max_hp: "coracao", max_rec: "estrela" };
  function destinoAtributo(d) {
    if (d.stat === "max_hp" || d.stat === "max_rec") return document.querySelector(`#hud .vital[data-vital="${d.stat === "max_hp" ? "hp" : "rec"}"]`);
    return document.querySelector(`#heroi .atributo[data-atributo="${d.nome}"]`);
  }
  function seloAtributo(d) {
    const selo = document.createElement("div");
    selo.className = "selo-atributo";
    selo.innerHTML = `${S(ICONE_SELO[d.stat] || "estrela", 4)}<b>+${d.valor}</b><span>${h(d.nome)}<small>permanente</small></span>`;
    document.body.appendChild(selo);
    selo.style.left = (innerWidth - selo.offsetWidth) / 2 + "px";  // centrado sem transform: o voo usa translate e scale
    App.som("aprender");
    const antes = d.total - d.valor, noPainel = !["max_hp", "max_rec"].includes(d.stat);
    if (noPainel) {  // o painel espera o selo chegar para mostrar o valor novo
      chegando.set(d.nome, antes);
      const v = destinoAtributo(d)?.querySelector(".valor");
      if (v) v.textContent = antes;
    }
    const voar = async () => {
      await new Promise((r) => setTimeout(r, 900));  // o selo fica um instante no meio, para ser lido
      const alvo = destinoAtributo(d), visivel = alvo && alvo.offsetParent;
      if (visivel) {
        const a = selo.getBoundingClientRect(), b = alvo.getBoundingClientRect();
        const dx = b.left + b.width / 2 - (a.left + a.width / 2), dy = b.top + b.height / 2 - (a.top + a.height / 2);
        await selo.animate([{ translate: "0 0", scale: 1, opacity: 1 }, { translate: `${dx}px ${dy}px`, scale: 0.25, opacity: 0.6 }],
          { duration: 520, easing: "cubic-bezier(.5,0,.75,0)", fill: "forwards" }).finished.catch(() => {});
      } else await selo.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 300, fill: "forwards" }).finished.catch(() => {});
      selo.remove();
      if (noPainel) chegando.delete(d.nome);
      const aqui = destinoAtributo(d);  // o painel pode ter sido redesenhado enquanto o selo voava
      if (!aqui) return;
      aqui.classList.remove("ganhou"); void aqui.offsetWidth; aqui.classList.add("ganhou");
      setTimeout(() => aqui.classList.remove("ganhou"), 1100);
      const valor = aqui.querySelector(".valor");
      if (valor && noPainel) Sensacao.contar(valor, d.total, 520, { de: antes });
    };
    // O próximo só aparece quando este chega ao painel (dois seguidos, +1 Poder e +4 Vida, um tampava o outro
    // enquanto o primeiro ainda saía do meio).
    return voar().then(() => new Promise((r) => setTimeout(r, 150)));
  }

  /** Chegar a um lugar: o nome surge no meio da tela entre dois fios dourados, como o título de área dos jogos
   *  (Elden Ring, Diablo). Na primeira vez, "lugar descoberto", som e um pouco mais de tempo; na volta, curto. O nível
   *  da região vem na cor do perigo (o aviso por extenso fica no texto). Some sozinho; um clique ou uma tecla adianta. */
  function chegada(d) {
    const el = document.createElement("div");
    el.className = "chegada" + (d.primeira ? " primeira" : "");
    const tag = d.nivel ? `<span class="perigo-tag ${nivelPerigo(d.nivel)}">${d.tipo === "vila" ? "Arredores" : "Inimigos"} Nv.${d.nivel}</span>` : "";
    el.innerHTML = `${d.primeira ? '<div class="rotulo-festa">lugar descoberto</div>' : ""}<i class="linha-ouro"></i>
      <div class="nome-lugar">${h(d.nome)}</div><i class="linha-ouro"></i>
      <div class="sub-lugar">${h(d.sub)}${tag}</div>`;
    document.body.appendChild(el);
    if (d.primeira) App.som("achado");
    return new Promise((resolver) => {
      let feito = false;
      const fechar = () => {
        if (feito) return;
        feito = true;
        document.removeEventListener("keydown", tecla, true);
        document.removeEventListener("pointerdown", clique, true);
        el.classList.add("saindo");
        setTimeout(() => { el.remove(); resolver(); }, 420);
      };
      const tecla = (ev) => { if ([" ", "Enter", "Escape"].includes(ev.key)) { ev.preventDefault(); ev.stopPropagation(); fechar(); } };
      const clique = (ev) => { ev.preventDefault(); ev.stopPropagation(); fechar(); };
      setTimeout(() => { document.addEventListener("keydown", tecla, true); document.addEventListener("pointerdown", clique, true); }, 300);
      setTimeout(fechar, d.primeira ? 2400 : 1300);
    });
  }

  function faixa(titulo, sub, icone, classe = "") {
    const f = document.createElement("div");
    f.className = "faixa-festa " + classe;
    f.innerHTML = `<b>${icone ? S(icone, 3) : ""}${h(titulo)}${icone ? S(icone, 3) : ""}</b>${sub ? `<span>${h(sub)}</span>` : ""}`;
    document.body.appendChild(f);
    // Sai quando a animação acaba (a sombria, do exausto, dura mais: um tempo fixo a cortava no meio da frase).
    f.addEventListener("animationend", (ev) => { if (ev.target === f) f.remove(); });
    setTimeout(() => f.remove(), 4000);
  }

  /** Mostra a celebração. Devolve uma Promise que resolve quando o jogador fecha (ou na hora, se rápida). */
  /** Os ganhos do nível contam de 0 até o valor, cada um com um tique. */
  function contarGanhos(caixa) {
    caixa.querySelectorAll(".conta").forEach((b) => {
      const alvo = Number(b.dataset.alvo), atraso = Number(b.dataset.atraso);
      setTimeout(() => {
        App.som("tique");
        const inicio = performance.now(), dur = 320;
        const passo = (agora) => {
          const t = Math.min(1, (agora - inicio) / dur);
          b.textContent = "+" + Math.round(alvo * (1 - Math.pow(1 - t, 3)));
          if (t < 1) requestAnimationFrame(passo);
        };
        requestAnimationFrame(passo);
      }, atraso);
    });
  }

  /** O ícone de um item voando de um ponto da tela até um elemento (o espaço do corpo, a mochila), num arco. */
  function voarIcone(item, origem, alvo) {
    const r = alvo.getBoundingClientRect();
    const voo = document.createElement("div");
    voo.className = "voo-item";
    voo.innerHTML = S(iconeItem(item), 3);
    document.body.appendChild(voo);
    const dx = r.left + r.width / 2 - origem.x, dy = r.top + r.height / 2 - origem.y;
    voo.style.left = origem.x - 24 + "px"; voo.style.top = origem.y - 24 + "px";
    return voo.animate([{ transform: "translate(0, 0) scale(1.2)", opacity: 1 },
      { transform: `translate(${dx * 0.5}px, ${dy * 0.5 - 60}px) scale(1)`, opacity: 1 },
      { transform: `translate(${dx}px, ${dy}px) scale(.45)`, opacity: 0.9 }],
      { duration: 560, easing: "cubic-bezier(.4,0,.2,1)" }).finished.catch(() => {}).then(() => voo.remove());
  }
  /** O cartão do item achado (na janela) recebe o selo do destino; devolve de onde o ícone sai. */
  function seloDoAchado(texto, classe, velhoTexto) {
    const tela = document.querySelector("#sobre-achado .tela.achado");
    if (!tela) return null;
    const novo = tela.querySelector(".achado-cartao.novo"), velho = tela.querySelector(".achado-cartao.atual");
    if (novo) { novo.classList.add(classe); const selo = novo.querySelector(".achado-selo"); if (selo) selo.textContent = texto; }
    if (velho && velhoTexto) { velho.classList.add("guardado"); const selo = velho.querySelector(".achado-selo"); if (selo) selo.textContent = velhoTexto; }
    const a = novo && novo.querySelector(".achado-arte").getBoundingClientRect();
    return a && a.width ? { x: a.left + a.width / 2, y: a.top + a.height / 2 } : null;
  }
  /** Vestiu (comprou no mercado ou achou): o ícone voa até o espaço do corpo no painel, que brilha ao receber. Achado:
   *  o cartão vira "Vestido", o antigo "Foi para a mochila", o ícone sai do próprio cartão e a janela fecha. */
  async function voarParaEspaco(d) {
    const alvo = document.querySelector(`#heroi [data-mini="${d.espaco}"]`);
    let origem = App.ultimoClique && performance.now() - App.ultimoClique.t < 4000 ? App.ultimoClique : { x: innerWidth / 2, y: innerHeight / 2 };
    if (d.achado) origem = seloDoAchado("Vestido", "vestido", "Foi para a mochila") || origem;
    if (alvo) {
      App.som("equipar");
      await voarIcone(d.item, origem, alvo);
      const novo = document.querySelector(`#heroi [data-mini="${d.espaco}"]`);
      if (novo) { novo.classList.remove("recebeu"); void novo.offsetWidth; novo.classList.add("recebeu"); setTimeout(() => novo.classList.remove("recebeu"), 900); }
    }
    if (d.achado) fecharAchado();
  }
  /** Guardou o item achado: o cartão vira "Na mochila", o ícone voa até o Inventário e a janela fecha. */
  async function voarParaMochila(d) {
    const origem = seloDoAchado("Na mochila", "na-mochila");
    const alvo = document.querySelector('.atalho[data-rotulo="Inventário"]');
    App.som("item");
    if (origem && alvo && alvo.offsetParent) {
      await voarIcone(d.item, origem, alvo);
      alvo.classList.remove("recebeu"); void alvo.offsetWidth; alvo.classList.add("recebeu");
      setTimeout(() => alvo.classList.remove("recebeu"), 900);
    } else await new Promise((r) => setTimeout(r, 500));
    fecharAchado();
  }

  /** O balão da reação do animal: acima dele, no palco da fogueira. Some sozinho ou com qualquer clique. */
  function balaoFera(alvo, d) {
    document.querySelectorAll(".balao.da-fera").forEach((b) => b.remove());
    const b = document.createElement("div");
    b.className = "balao narrado da-fera";
    b.innerHTML = `<i>${h(d.texto)}</i>${d.efeito ? `<small class="balao-efeito">${h(d.efeito)}</small>` : ""}`;
    document.body.appendChild(b);
    const r = alvo.getBoundingClientRect();
    // Sobre o animal, alinhado pela esquerda (o rabicho aponta para ele): o meio do palco e a barraca ficam livres.
    b.style.left = Math.max(8, r.left + r.width / 2 - 22) + "px";
    b.style.top = Math.max(8, r.top + r.height * 0.35 - b.offsetHeight - 10) + "px";
    const nasceu = performance.now();
    const sair = () => { b.classList.add("sumindo"); setTimeout(() => b.remove(), 300); document.removeEventListener("pointerdown", aoClicar, true); };
    const aoClicar = () => { if (performance.now() - nasceu > 300) sair(); };
    document.addEventListener("pointerdown", aoClicar, true);
    setTimeout(sair, Math.min(9000, 3000 + d.texto.length * 45));
  }

  function celebrar(m, instantaneo) {
    const d = m.dados;
    if (m.tipo === "equipou") return instantaneo ? (fecharAchado(), Promise.resolve()) : voarParaEspaco(d);
    if (m.tipo === "guardou") return instantaneo ? (fecharAchado(), Promise.resolve()) : voarParaMochila(d);
    if (m.tipo === "carinho") {
      // corações subindo do animal na fogueira, e a reação num balão sobre ele (não tampa nada; um clique dispensa)
      if (instantaneo) return Promise.resolve();
      const alvos = document.querySelectorAll("#texto .figura.fera");
      const alvo = alvos[alvos.length - 1];
      if (alvo && d.texto) balaoFera(alvo, d);
      if (d.repetido) return Promise.resolve();
      App.som("cura");
      if (alvo) for (let i = 0; i < 6; i++) {
        const c = document.createElement("span");
        c.className = "coracao-carinho";
        c.textContent = "♥";
        c.style.left = 20 + Math.random() * 60 + "%";
        c.style.animationDelay = i * 110 + "ms";
        alvo.appendChild(c);
        setTimeout(() => c.remove(), 1600);
      }
      return new Promise((r) => setTimeout(r, 700));
    }
    if (m.tipo === "vitoria") {
      if (instantaneo) return Promise.resolve();
      App.som("vitoria");
      faixa(d.chefe ? "Guardião derrotado!" : "Vitória", null, "espada");
      particulas(["#f2c94c", "#fff3a0", "#d4af37"], d.chefe ? 70 : 30);
      return new Promise((r) => setTimeout(r, d.chefe ? 1500 : 1000));
    }
    if (m.tipo === "mestre") {  // mestre caçador de uma espécie: a faixa de ouro com a criatura dos dois lados
      if (instantaneo) return Promise.resolve();
      App.som("nivel");
      faixa("Mestre caçador", `${d.plural.charAt(0).toUpperCase() + d.plural.slice(1)}: +10% de dano contra eles`, d.retrato || "caveira");
      return new Promise((r) => setTimeout(r, 1800));
    }
    if (m.tipo === "exausto") {  // o dia acabou à força: uma faixa sombria, devagar, e a fogueira (ou o feno) em seguida
      if (instantaneo) return Promise.resolve();
      App.som("exausto");
      faixa("Exausto", d.texto, "lua", "sombria");
      return new Promise((r) => setTimeout(r, 2300));
    }
    if (m.tipo === "comitiva") {
      if (instantaneo) return Promise.resolve();
      App.som("nivel");
      faixa(`${d.nome} se junta a você`, d.titulo, d.id);
      return new Promise((r) => setTimeout(r, 1500));
    }
    const caixa = document.getElementById("celebracao");
    if (m.tipo === "contratos") return instantaneo ? Promise.resolve() : pagarContratos(caixa, d);
    if (m.tipo === "amanhecer") return instantaneo ? Promise.resolve() : amanhecer(caixa, d);
    if (m.tipo === "espolio") return instantaneo ? Promise.resolve() : Sensacao.espolio(caixa, d);
    if (m.tipo === "atributo") return instantaneo ? Promise.resolve() : seloAtributo(d);
    if (m.tipo === "chegada") return instantaneo ? Promise.resolve() : chegada(d);
    let html = "";
    if (m.tipo === "nivel") {
      const icones = { Vida: "coracao", Ataque: "espada", Defesa: "escudo", Agilidade: "folha", Poder: "chama", Mana: "pocao_azul", Vigor: "chama", Foco: "olho" };
      const ganhos = Object.entries(d.ganhos).map(([k, v], i) => `<span class="ganho" style="animation-delay:${0.75 + i * 0.12}s">${S(icones[k] || "estrela", 1)}<b class="conta" data-alvo="${v}" data-atraso="${750 + i * 120}">+0</b>${h(k)}</span>`).join("");
      const atraso = 0.75 + Object.keys(d.ganhos).length * 0.12;
      const habs = d.habilidades.map((x, i) => `<div class="habilidade-nova" style="animation-delay:${atraso + 0.35 + i * 0.2}s"><span class="rotulo-festa">nova habilidade</span><b>${h(x.nome)}</b>${Realce.texto(x.desc)}</div>`).join("");
      html = `<div class="festa festa-nivel m-janela"><div class="raios"></div><div class="anel"></div>
        <div class="rotulo-festa">você subiu de nível</div>
        <div class="nivel-bloco"><span class="nivel-palavra">Nível</span><span class="nivel-numero">${d.nivel}</span></div>
        <div class="lista">${ganhos}<span class="ganho ouro" style="animation-delay:${atraso + 0.08}s">${S("estrela", 1)}+1 ponto de talento</span></div>${habs}
        ${d.especializacao ? '<div class="texto-festa" style="color:var(--arcano)">Uma encruzilhada se aproxima: em breve você escolherá sua especialização.</div>' : ""}
        <button class="continuar" type="button">Continuar <span>▸</span></button></div>`;
      App.som("subir");
      particulas(["#f2c94c", "#fff3a0", "#ff9d4d", "#8fbf6a"], 90);
      setTimeout(() => contarGanhos(caixa), 0);
    } else if (m.tipo === "sigilo") {
      const los = [0, 1, 2].map((i) => `<i class="${i < d.sigilos ? "tem" : ""}${i === d.sigilos - 1 ? " novo" : ""}"></i>`).join("");
      html = `<div class="festa m-janela"><div class="rotulo-festa">${h(d.guardiao)} caiu</div><div class="grande">Sigilo ${d.sigilos}/3</div>
        <div class="losangos">${los}</div><div class="texto-festa">Uma runa ardente se grava na sua mão.</div>
        <div class="lista"><span class="ganho ouro">${S("estrela", 1)}+1 ponto de talento</span></div>
        <button class="continuar" type="button">Continuar <span>▸</span></button></div>`;
      App.som("fanfarra");
      particulas(["#f2c94c", "#ff4020", "#fff3a0"], 110);
    } else if (m.tipo === "spec") {
      const habs = d.habilidades.map((x, i) => `<div class="habilidade-nova" style="animation-delay:${0.6 + i * 0.25}s"><span class="rotulo-festa">nova habilidade</span><b>${h(x.nome)}</b>${Realce.texto(x.desc)}</div>`).join("");
      html = `<div class="festa m-janela"><div class="rotulo-festa">você agora é</div><div class="grande arcano">${h(d.nome)}</div>
        <div class="texto-festa">${h(d.desc)}</div>${habs}<button class="continuar" type="button">Continuar <span>▸</span></button></div>`;
      App.som("fanfarra");
      particulas(["#b49cff", "#c8b0ff", "#ffffff"], 90);
    } else {
      return Promise.resolve();
    }
    if (instantaneo) return Promise.resolve();
    caixa.innerHTML = html;
    caixa.hidden = false;
    return new Promise((resolver) => {
      const fechar = () => {
        caixa.hidden = true; caixa.innerHTML = "";
        document.removeEventListener("keydown", tecla, true);
        resolver();
      };
      const tecla = (ev) => {
        if ([" ", "Enter", "Escape"].includes(ev.key)) { ev.preventDefault(); ev.stopPropagation(); fechar(); }
      };
      setTimeout(() => document.addEventListener("keydown", tecla, true), 600);
      caixa.querySelector(".continuar").addEventListener("click", (ev) => { ev.stopPropagation(); fechar(); });
    });
  }

  /** Contratos cumpridos: os cartazes chegam, o carimbo bate em cada um, o total aparece, e "Receber" faz as
   *  moedas voarem até o seu ouro. Um momento só, em vez de três blocos de texto no registro. */
  function pagarContratos(caixa, d) {
    const um = d.contratos.length === 1;
    const cartazes = d.contratos.map((c, i) => `<div class="pago" style="--i:${i}">${cartaz({ ...c, recebendo: true }, true, false, App.estado ? App.estado.heroi.nivel : 1)}</div>`).join("");
    const atraso = 0.5 + d.contratos.length * 0.35;
    const ganhos = [[d.ouro, "moeda", "ouro", "ouro"], [d.xp, "estrela", "XP", ""], [d.reputacao, "coroa", "reputação", "rep"]]
      .filter(([v]) => v > 0)
      .map(([v, ic, nome, cls], i) => `<span class="ganho ${cls}" style="animation-delay:${atraso + i * 0.15}s">${S(ic, 1)}+${v} ${nome}</span>`).join("");
    caixa.innerHTML = `<div class="festa festa-contratos m-janela">
      <div class="rotulo-festa">${um ? "contrato cumprido" : `${d.contratos.length} contratos cumpridos`}</div>
      <div class="cartazes-pagos">${cartazes}</div>
      <div class="lista">${ganhos}</div>
      <button class="continuar" type="button">Receber recompensa <span>▸</span></button></div>`;
    caixa.hidden = false;
    App.som("achado");
    d.contratos.forEach((_, i) => setTimeout(() => App.som("equipar"), (0.45 + i * 0.35) * 1000));
    return new Promise((resolver) => {
      let feito = false;
      const receber = () => {
        if (feito) return;
        feito = true;
        document.removeEventListener("keydown", tecla, true);
        App.som("moeda");
        moedasPara(caixa.querySelector(".ganho.ouro") || caixa.querySelector(".continuar"), document.querySelector('.recurso[data-rec="ouro"]'));
        particulas(["#f2c94c", "#fff3a0", "#d4af37"], 40);
        setTimeout(() => { caixa.hidden = true; caixa.innerHTML = ""; resolver(); }, 650);
      };
      const tecla = (ev) => { if ([" ", "Enter", "Escape"].includes(ev.key)) { ev.preventDefault(); ev.stopPropagation(); receber(); } };
      setTimeout(() => document.addEventListener("keydown", tecla, true), 600);
      caixa.querySelector(".continuar").addEventListener("click", (ev) => { ev.stopPropagation(); receber(); });
    });
  }

  /** A virada do dia: a aurora na paisagem, a faixa "Dia N" e o que a noite fez, em ícones (verde o que fez bem,
   *  amarelo o que pede atenção, vermelho o que dói). Noite tranquila: some sozinho; noite ruim: espera o clique. */
  const ICONE_NOITE = { bom: "bom", neutro: "", aviso: "aviso", perigo: "perigo" };

  function amanhecer(caixa, d) {
    if (typeof Vista !== "undefined") Vista.amanhecer(1800);
    App.som("amanhecer");
    const ruim = d.itens.some((x) => x.tipo === "perigo");
    const itens = d.itens.map((x, i) => `<span class="noite-item ${ICONE_NOITE[x.tipo] || ""}" style="animation-delay:${0.55 + i * 0.12}s"${x.texto && x.texto !== x.curto ? ` title="${h(x.texto)}"` : ""}>${S(x.icone, 1)}${h(x.curto)}</span>`).join("");
    caixa.innerHTML = `<div class="festa festa-amanhecer">
      <div class="rotulo-festa">amanhece</div>
      <div class="dia-numero">Dia ${d.dia}</div>
      <div class="dia-clima">${h(d.clima)}</div>
      ${itens ? `<div class="noite">${itens}</div>` : ""}
      ${ruim ? '<button class="continuar" type="button">Continuar <span>▸</span></button>' : ""}</div>`;
    caixa.classList.add("leve");
    caixa.hidden = false;
    noPalco(caixa.querySelector(".festa-amanhecer"), true);
    return new Promise((resolver) => {
      let feito = false;
      const fechar = () => {
        if (feito) return;
        feito = true;
        document.removeEventListener("keydown", tecla, true);
        document.removeEventListener("pointerdown", clique, true);
        const festa = caixa.querySelector(".festa-amanhecer");
        if (festa) festa.classList.add("saindo");
        setTimeout(() => { caixa.hidden = true; caixa.innerHTML = ""; caixa.classList.remove("leve"); resolver(); }, 260);
      };
      const tecla = (ev) => { if ([" ", "Enter", "Escape"].includes(ev.key)) { ev.preventDefault(); ev.stopPropagation(); fechar(); } };
      const clique = (ev) => { ev.preventDefault(); ev.stopPropagation(); fechar(); };
      setTimeout(() => { document.addEventListener("keydown", tecla, true); document.addEventListener("pointerdown", clique, true); }, 500);
      if (!ruim) setTimeout(fechar, 2400 + d.itens.length * 350);
    });
  }

  /** Uma linha curta para o registro (histórico) de cada festa: o registro guarda o fato, a festa mostra. */
  function resumoCelebracao(m) {
    const d = m.dados || {};
    if (m.tipo === "nivel") return `▸ Nível ${d.nivel}: +1 ponto de talento${(d.habilidades || []).length ? ", " + d.habilidades.map((x) => x.nome).join(", ") : ""}`;
    if (m.tipo === "contratos") return `▸ ${d.contratos.length === 1 ? "Contrato cumprido" : d.contratos.length + " contratos cumpridos"}: +${d.ouro} ouro, +${d.xp} XP`;
    if (m.tipo === "sigilo") return `▸ Sigilo ${d.sigilos}/3 (${d.guardiao}): +1 ponto de talento`;
    if (m.tipo === "spec") return `▸ Você agora é ${d.nome}`;
    if (m.tipo === "espolio") return `▸ Espólio: ${d.ouro ? `+${d.ouro} ouro, ` : ""}+${d.xp} XP`;
    if (m.tipo === "atributo") return `▸ +${d.valor} ${d.nome} permanente`;
    if (m.tipo === "chegada") return `▸ ${d.primeira ? "Descoberto" : "Chegada"}: ${d.nome}`;
    if (m.tipo === "exausto") return `▸ Exausto: ${d.texto}`;
    if (m.tipo === "mestre") return `▸ Mestre caçador: ${d.plural} (+10% de dano contra eles)`;
    if (m.tipo === "equipou" && d.achado) return `▸ Vestiu: ${d.item.nome}`;
    if (m.tipo === "guardou") return `▸ Na mochila: ${d.item.nome}`;
    if (m.tipo === "amanhecer") return `▸ Dia ${d.dia} · ${d.clima}${d.itens.length ? " · " + d.itens.map((x) => x.curto).join(", ") : ""}`;
    return "";
  }

  Object.assign(Telas, { celebrar, resumoCelebracao });
})();
