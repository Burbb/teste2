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
    selo.innerHTML = `${Icones.atributo(d.nome, 64) || S(ICONE_SELO[d.stat] || "estrela", 4)}<b>+${d.valor}</b><span>${h(d.nome)}<small>permanente</small></span>`;
    document.body.appendChild(selo);
    selo.style.left = (innerWidth - selo.offsetWidth) / 2 + "px";  // centrado sem transform: o voo usa translate e scale
    App.som("aprender");
    const antes = d.total - d.valor, noPainel = !["max_hp", "max_rec"].includes(d.stat);
    if (noPainel) {  // o painel espera o selo chegar para mostrar o valor novo
      chegando.set(d.nome, antes);
      const v = destinoAtributo(d)?.querySelector(".valor .num");
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
      const valor = aqui.querySelector(".valor .num");
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

  // ---------------------------------------------------------------- as faixas de passagem (1.205.0)
  // A tarja larga de lado a lado (a 38% da altura, por cima da interface), o título de 80 px com um símbolo de cada
  // lado e o subtítulo legível (quebra a linha; o título nunca diminui por ele). O peso de cada situação, na mesma
  // família: "comum" (a Vitória), "marco" (o Guardião, o Mestre caçador, quem chega: um acento breve na entrada),
  // "derrota" e "peso" (a queda e o cansaço: entram descendo, sem ouro), "passagem" (a saída da capela). A tarja é
  // desenhada em pixel (texels de 3 px): a transparência de 0,94 no miolo, as pontas em degraus de borda dura e o fio
  // de cima só no miolo. Uma faixa que chega com outra na tela tira a anterior em 100 ms (antes, o "Guardião derrotado!"
  // e o "Mestre caçador" ficavam um sobre o outro). Os tempos de cada uma são os de sempre (a duração da animação aqui;
  // quanto ela segura a fila, em `celebrar`). O protótipo e as alternativas: ferramentas/prototipos/hud/faixas/.
  const DURA_FAIXA = { comum: 1600, marco: 1600, peso: 2400, passagem: 2400, derrota: 2600 };
  const TARJA = {  // o miolo e o fio de cima (quase o miolo: só uma beira); no marco, o acento que corre pelo fio
    comum: { miolo: [13, 11, 10], cima: [27, 23, 18] },
    marco: { miolo: [13, 11, 10], cima: [40, 33, 21], acento: [242, 210, 122] },
    derrota: { miolo: [30, 7, 6], cima: [50, 15, 12] },
    peso: { miolo: [12, 12, 15], cima: [27, 28, 33] },
    passagem: { miolo: [13, 11, 10], cima: [24, 21, 17] },
  };
  const DEGRAUS = [0.14, 0.3, 0.46, 0.62, 0.78, 0.94];  // a transparência das pontas, em degraus (o miolo: 0,94)
  /** A tarja no canvas: as pontas em seis degraus ao longo de 20% da largura (24% no peso e na queda), o fio de cima
   *  só no miolo. No marco, com `t` (ms desde a entrada): dois brilhos curtos correm do centro pelo fio e somem. */
  function tarja(cv, peso, t = null) {
    const c = TARJA[peso], W = cv.width, H = cv.height, g = cv.getContext("2d"), img = g.createImageData(W, H), b = img.data;
    const ponta = peso === "derrota" || peso === "peso" ? 0.24 : 0.2;
    const por = (x, y, [r, gg, bb], a) => { const i = (y * W + x) * 4; b[i] = r; b[i + 1] = gg; b[i + 2] = bb; b[i + 3] = Math.round(a * 255); };
    for (let x = 0; x < W; x++) {
      const u = Math.min(x, W - 1 - x) / (W * ponta);
      const a = u >= 1 ? DEGRAUS[DEGRAUS.length - 1] : DEGRAUS[Math.min(DEGRAUS.length - 1, Math.floor(u * DEGRAUS.length))];
      const fio = Math.min(x, W - 1 - x) > W * 0.3;
      for (let y = 0; y < H; y++) por(x, y, y === 0 && fio ? c.cima : c.miolo, a);
    }
    if (c.acento && t !== null && t < 480) {
      const meio = W >> 1, alcance = Math.round((t / 480) * W * 0.32), vis = 1 - t / 480;
      for (let k = -3; k <= 3; k++) for (const x of [meio - alcance + k, meio + alcance + k]) if (x >= 0 && x < W) {
        const f = (Math.abs(k) <= 1 ? 1 : 0.5) * vis;
        por(x, 0, c.cima.map((v, i) => Math.round(v + (c.acento[i] - v) * f)), 0.94);
      }
    }
    g.putImageData(img, 0, 0);
  }
  const espelhado = (html) => html.replace("<img ", '<img style="transform:scaleX(-1)" ');
  /** A faixa de passagem: `titulo`, `sub` (ou nada), `icone` (o símbolo da esquerda; a direita, o mesmo espelhado se
   *  `espelhar`) e o `peso`. Sai sozinha no fim da animação (e por um tempo de segurança, também com o movimento
   *  reduzido, em que ela fica inteira e parada). */
  function faixa(titulo, sub, icone, peso, espelhar = true) {
    document.querySelectorAll(".faixa-festa").forEach((e) => { e.classList.add("troca"); setTimeout(() => e.remove(), 110); });
    const f = document.createElement("div"), dura = DURA_FAIXA[peso];
    f.className = `faixa-festa peso-${peso}`;
    f.setAttribute("role", "status");
    f.style.setProperty("--dura", dura + "ms");
    const dir = icone && espelhar ? espelhado(icone) : icone;
    f.innerHTML = `<canvas class="faixa-tarja" aria-hidden="true"></canvas><b>${icone ? `<span class="faixa-icone">${icone}</span>` : ""}${h(titulo)}${icone ? `<span class="faixa-icone">${dir}</span>` : ""}</b>${sub ? `<span class="faixa-sub">${h(sub)}</span>` : ""}`;
    document.body.appendChild(f);
    const cv = f.querySelector(".faixa-tarja"), r = f.getBoundingClientRect();
    cv.width = Math.ceil(r.width / 3); cv.height = Math.ceil(r.height / 3);
    if (TARJA[peso].acento && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
      const t0 = performance.now();
      const passo = () => { const t = performance.now() - t0; tarja(cv, peso, t); if (t < 520 && f.isConnected) setTimeout(passo, 66); };
      passo();
    } else tarja(cv, peso);
    f.addEventListener("animationend", (ev) => { if (ev.target === f && ev.animationName !== "faixa-troca") f.remove(); });
    setTimeout(() => f.remove(), dura + 40);
  }

  /** O ícone de um item voando de um ponto da tela até um elemento (o espaço do corpo, a mochila), num arco. */
  function voarIcone(item, origem, alvo) {
    const r = alvo.getBoundingClientRect();
    const voo = document.createElement("div");
    voo.className = "voo-item";
    voo.innerHTML = Icones.item(iconeItem(item), 48) || S(iconeItem(item), 3);
    document.body.appendChild(voo);
    const dx = r.left + r.width / 2 - origem.x, dy = r.top + r.height / 2 - origem.y;
    voo.style.left = origem.x - 24 + "px"; voo.style.top = origem.y - 24 + "px";
    return voo.animate([{ transform: "translate(0, 0) scale(1.2)", opacity: 1 },
      { transform: `translate(${dx * 0.5}px, ${dy * 0.5 - 60}px) scale(1)`, opacity: 1 },
      { transform: `translate(${dx}px, ${dy}px) scale(.45)`, opacity: 0.9 }],
      { duration: 560, easing: "cubic-bezier(.4,0,.2,1)" }).finished.catch(() => {}).then(() => voo.remove());
  }
  /** O cartão do item achado (na janela) recebe o selo do destino; devolve de onde o ícone sai. */
  function seloDoAchado(texto, classe, velhoTexto, espaco) {
    const tela = document.querySelector("#sobre-achado .tela.achado");
    if (!tela) return null;
    // o cartão do que estava no espaço que recebeu o achado (os anéis têm um cartão por espaço; os outros, um só)
    const novo = tela.querySelector(".achado-cartao.novo");
    const velho = tela.querySelector(`.achado-cartao.atual[data-espaco="${espaco}"]`) || tela.querySelector(".achado-cartao.atual:not([data-espaco])");
    if (novo) { novo.classList.add(classe); const selo = novo.querySelector(".achado-selo"); if (selo) selo.textContent = texto; }
    if (velho && velhoTexto) { velho.classList.add("guardado"); const selo = velho.querySelector(".achado-selo"); if (selo) selo.textContent = velhoTexto; }
    const a = novo && novo.querySelector(".achado-arte").getBoundingClientRect();
    return a && a.width ? { x: a.left + a.width / 2, y: a.top + a.height / 2 } : null;
  }
  /** Vestiu (comprou no mercado ou achou): o ícone voa até o espaço do corpo no painel, que brilha ao receber. Achado:
   *  o cartão vira "Vestido" e o do que estava naquele espaço diz para onde ele foi, como o motor contou ("Foi para a
   *  mochila", ou "Ficou para trás" com a mochila cheia; espaço vazio, nada); o ícone sai do cartão e a janela fecha. */
  async function voarParaEspaco(d) {
    const alvo = document.querySelector(`#heroi [data-mini="${d.espaco}"]`);
    let origem = App.ultimoClique && performance.now() - App.ultimoClique.t < 4000 ? App.ultimoClique : { x: innerWidth / 2, y: innerHeight / 2 };
    const velho = { mochila: "Foi para a mochila", ficou: "Ficou para trás" }[d.antigo] || null;
    if (d.achado) origem = seloDoAchado("Vestido", "vestido", velho, d.espaco) || origem;
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

  /** A derrota que encerra a luta (o motor só a manda nessa hora: a Pena de Fênix e a proteção não chegam aqui): a
   *  carta do herói cai e se apaga, a tela pulsa vermelho, a faixa diz o resultado ("Você caiu": vem o resgate; "Você
   *  morreu": modo hardcore) e um som curto. Depois, o cenário fica escuro (sem os prédios da vila) até o herói
   *  acordar (o amanhecer do resgate) ou o próximo menu: a vila não aparece como se ele já estivesse de pé. Cerca de
   *  2 s, adiantável pelo clique ou tecla de sempre; em seguida, a página nova do resgate (ou da morte), sem Continuar
   *  no meio (ponte.py: depois_da_queda). No replay e no instantâneo, só o escuro. */
  const QUEDA_MS = 2200;  // a queda inteira (a faixa dura um pouco mais e some sobre a página nova)
  function queda(d, instantaneo) {
    document.body.classList.add("derrotado");
    if (instantaneo) return Promise.resolve();
    document.querySelector('#arena .carta[data-uid="j"]')?.classList.add("caida");
    App.som("derrota");
    doer();
    faixa(d.morte ? "Você morreu" : "Você caiu", null, S("caveira", 3), "derrota", false);
    return (async () => { for (let t = 0; t < QUEDA_MS && !pular; t += 50) await new Promise((r) => setTimeout(r, 50)); })();
  }
  /** O herói acordou (o amanhecer do resgate) ou um menu chegou: o cenário volta à luz de sempre. */
  function fimDaQueda() { document.body.classList.remove("derrotado"); }

  function celebrar(m, instantaneo) {
    const d = m.dados;
    if (m.tipo === "equipou") return instantaneo ? (fecharAchado(), Promise.resolve()) : voarParaEspaco(d);
    if (m.tipo === "guardou") return instantaneo ? (fecharAchado(), Promise.resolve()) : voarParaMochila(d);
    if (m.tipo === "carinho") {
      // corações subindo do animal na cena da fogueira, e a reação num balão sobre ele (não tampa nada; um clique dispensa)
      if (instantaneo) return Promise.resolve();
      const alvos = document.querySelectorAll("#acampamento-pontos .figura.fera");
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
    if (m.tipo === "derrota") return queda(d, instantaneo);
    if (m.tipo === "correntes") return Telas.soltarCorrentes(instantaneo);  // o preparo gravado: a corrente desce
    if (m.tipo === "ilse") return Telas.momentoIlse(d, instantaneo);  // o que o texto acabou de contar de Ilse, no fundo
    if (m.tipo === "livro") return Telas.lerLivro(d, instantaneo);  // o livro da capela aberto, até o jogador fechar
    if (m.tipo === "vitoria") {
      if (instantaneo) return Promise.resolve();
      App.som("vitoria");
      faixa(d.chefe ? "Guardião derrotado!" : "Vitória", null, Icones.item("espada", 48), d.chefe ? "marco" : "comum");
      particulas(["#f2c94c", "#fff3a0", "#d4af37"], d.chefe ? 70 : 30);
      return new Promise((r) => setTimeout(r, d.chefe ? 1500 : 1000));
    }
    if (m.tipo === "mestre") {  // mestre caçador de uma espécie: a faixa de ouro com a criatura dos dois lados
      if (instantaneo) return Promise.resolve();
      App.som("nivel");
      faixa("Mestre caçador", `${d.plural.charAt(0).toUpperCase() + d.plural.slice(1)}: +10% de dano contra eles`,
        Icones.criatura(d.retrato, 48) || S("caveira", 3), "marco");
      return new Promise((r) => setTimeout(r, 1800));
    }
    if (m.tipo === "exausto") {  // o dia acabou à força: uma faixa sombria, devagar, e a fogueira (ou o feno) em seguida
      if (instantaneo) return Promise.resolve();
      App.som("exausto");
      faixa("Exausto", d.texto, S("lua", 3), "peso", false);
      return new Promise((r) => setTimeout(r, 2300));
    }
    if (m.tipo === "retirada") {  // a saída da capela antes de acampar (a arte do topo já passou ao lado de fora)
      if (instantaneo) return Promise.resolve();
      App.som(d.exausto ? "exausto" : "retirada");  // os passos que se afastam
      if (d.exausto) faixa("Exausto", d.texto, S("lua", 3), "peso", false);
      else faixa("Saindo da capela", d.texto, Icones.atalho("Sair", 36), "passagem", false);  // o Sair da doca
      return new Promise((r) => setTimeout(r, 2600));
    }
    if (m.tipo === "comitiva") {
      if (instantaneo) return Promise.resolve();
      App.som("nivel");
      faixa(`${d.nome} se junta a você`, d.titulo, Icones.cabeca(d.id, 48), "marco");
      return new Promise((r) => setTimeout(r, 1500));
    }
    const caixa = document.getElementById("celebracao");
    if (m.tipo === "contratos") return instantaneo ? Promise.resolve() : pagarContratos(caixa, d);
    if (m.tipo === "amanhecer") { fimDaQueda(); return instantaneo ? Promise.resolve() : amanhecer(caixa, d); }
    if (m.tipo === "espolio") return instantaneo ? Promise.resolve() : Sensacao.espolio(caixa, d);
    if (m.tipo === "atributo") return instantaneo ? Promise.resolve() : seloAtributo(d);
    if (m.tipo === "chegada") return instantaneo ? Promise.resolve() : chegada(d);
    // O nível, o Sigilo e a especialização: a festa da apresentação (celebracoes/festa.js; Estouro, ou Relicário)
    return Festa.celebrar(m, caixa, instantaneo);
  }

  /** Contratos cumpridos: os cartazes chegam, o carimbo bate em cada um, o total aparece, e "Receber" faz as
   *  moedas voarem até o seu ouro. Um momento só, em vez de três blocos de texto no registro. */
  function pagarContratos(caixa, d) {
    const um = d.contratos.length === 1;
    const cartazes = d.contratos.map((c, i) => `<div class="pago" style="--i:${i}">${cartaz({ ...c, recebendo: true }, true, false, App.estado ? App.estado.heroi.nivel : 1)}</div>`).join("");
    const atraso = 0.5 + d.contratos.length * 0.35;
    const ganhos = [[d.ouro, "moeda", "ouro", "ouro"], [d.xp, "estrela", "XP", ""], [d.reputacao, "coroa", "reputação", "rep"]]
      .filter(([v]) => v > 0)
      .map(([v, ic, nome, cls], i) => `<span class="ganho ${cls}" style="animation-delay:${atraso + i * 0.15}s">${Icones.miudo(ic) || S(ic, 1)}+${v} ${nome}</span>`).join("");
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
    if (m.tipo === "nivel") return `▸ Nível ${d.nivel}: +1 ponto de talento${d.pontos_atributo ? ", +2 pontos de atributo" : ""}${(d.habilidades || []).length ? ", " + d.habilidades.map((x) => x.nome).join(", ") : ""}`;
    if (m.tipo === "contratos") return `▸ ${d.contratos.length === 1 ? "Contrato cumprido" : d.contratos.length + " contratos cumpridos"}: +${d.ouro} ouro, +${d.xp} XP`;
    if (m.tipo === "sigilo") return `▸ Sigilo ${d.sigilos}/3 (${d.guardiao}): +1 ponto de talento`;
    if (m.tipo === "spec") return `▸ Você agora é ${d.nome}`;
    if (m.tipo === "espolio") return `▸ Espólio: ${d.ouro ? `+${d.ouro} ouro, ` : ""}+${d.xp} XP`;
    if (m.tipo === "atributo") return `▸ +${d.valor} ${d.nome} permanente`;
    if (m.tipo === "chegada") return `▸ ${d.primeira ? "Descoberto" : "Chegada"}: ${d.nome}`;
    if (m.tipo === "exausto") return `▸ Exausto: ${d.texto}`;
    if (m.tipo === "retirada") return `▸ ${d.exausto ? "Exausto: " : ""}${d.texto}`;
    if (m.tipo === "derrota") return d.morte ? "▸ Você morreu" : "▸ Você caiu";
    if (m.tipo === "livro") return d.primeira ? "▸ Leu o livro da capela" : "";  // reler não repete a linha
    if (m.tipo === "mestre") return `▸ Mestre caçador: ${d.plural} (+10% de dano contra eles)`;
    if (m.tipo === "equipou" && d.achado) return `▸ Vestiu: ${d.item.nome}`;
    if (m.tipo === "guardou") return `▸ Na mochila: ${d.item.nome}`;
    if (m.tipo === "amanhecer") return `▸ Dia ${d.dia} · ${d.clima}${d.itens.length ? " · " + d.itens.map((x) => x.curto).join(", ") : ""}`;
    return "";
  }

  Object.assign(Telas, { celebrar, resumoCelebracao, fimDaQueda });
})();
