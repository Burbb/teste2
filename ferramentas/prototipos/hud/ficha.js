/* Protótipo da ficha do herói (experimento, fora do jogo): desenha o painel a partir do mesmo dicionário que a ficha
   atual recebe do motor (rpg.web.estado.heroi), gravado em dados.js por gerar_dados.py. Não fala com o motor: as
   combinações dos controles de demonstração já vêm prontas de lá. */
"use strict";

const Ficha = (() => {
  const esc = (t) => String(t ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const ESPACOS = [["cabeca", "armadura", "maos", "pernas", "pes"], ["arma", "secundaria", "amuleto", "anel1", "anel2"]];
  const NOME_ESPACO = { cabeca: "Cabeça", amuleto: "Amuleto", armadura: "Peito", maos: "Mãos", arma: "Arma",
    secundaria: "Escudo", pernas: "Pernas", pes: "Pés", anel1: "Anel 1", anel2: "Anel 2" };  // a secundária do guerreiro
  const VAZIO = { cabeca: "elmo", amuleto: "amuleto", armadura: "armadura", maos: "manopla", arma: "espada",
    secundaria: "escudo", pernas: "calca", pes: "bota", anel1: "anel", anel2: "anel" };
  const ICONE_ATTR = { Ataque: "espada", Defesa: "escudo", Agilidade: "folha", Poder: "chama" };
  const RARIDADE = { comum: "comum", magico: "mágico", raro: "raro", lendario: "lendário" };

  let iconesNovos = true, versao = "anterior";
  // Segunda tentativa ("Assets"): as peças recortadas da imagem de referência (preparar_assets.py), já reduzidas
  // para o tamanho de uso de cada lugar. Só estes quatro ícones têm substituto; o resto continua o catálogo do jogo.
  const ASSETS = ["espada", "escudo", "anel", "pocao"];
  /** O desenho: os quatro novos (espada, escudo, anel, poção) quando ligados; o resto, o catálogo atual do jogo.
   *  `lado`: o tamanho em que aparece (a versão Assets tem um arquivo por tamanho; a Anterior escala o pixel). */
  const icone = (nome, lado = 32) => {
    if (iconesNovos && versao === "assets" && ASSETS.includes(nome)) return `assets/exibicao/${nome}-${lado}.png`;
    if (iconesNovos && versao !== "assets" && Arte.temIcone(nome)) return Arte.icone(nome);  // Anterior e HUD 3
    return Sprites.url(nome);
  };
  const ehAsset = (nome) => iconesNovos && versao === "assets" && ASSETS.includes(nome);
  const img = (nome, lado = 32) => `<img src="${icone(nome, lado)}"${ehAsset(nome) ? ' class="ia"' : ""} alt="" draggable="false">`;

  function dicaItem(it, espaco) {
    const r = it.raridade || "comum";
    return `<b class="t r-${esc(r)}">${esc(it.nome)}</b><div class="sub">${esc(NOME_ESPACO[espaco])} · ${esc(RARIDADE[r] || r)} · nível ${esc(it.nivel)}</div>` +
      `<div>${esc(it.bonus)}</div>${it.lore ? `<div class="rodape">${esc(it.lore)}</div>` : ""}`;
  }

  function desenhar(raiz, h, nome) {
    raiz.classList.toggle("v2", versao === "assets");
    raiz.classList.toggle("v3", versao === "hud3");  // a HUD 3 usa o retrato e os ícones da primeira tentativa
    const espacos = ESPACOS.map((linha) => linha.map((s) => {
      const it = h.equip[s];
      if (!it) return `<button type="button" class="f-slot vazio f-foco" data-espaco="${s}" data-dica="${esc(`<b class="t">${NOME_ESPACO[s]}</b><div class="sub">vazio</div>`)}" aria-label="${NOME_ESPACO[s]}: vazio">${img(VAZIO[s])}</button>`;
      const r = it.raridade && it.raridade !== "comum" ? ` data-r="${esc(it.raridade)}"` : "";
      return `<button type="button" class="f-slot f-foco"${r} data-espaco="${s}" data-dica="${esc(dicaItem(it, s))}" aria-label="${NOME_ESPACO[s]}: ${esc(it.nome)}">${img(it.icone || "saco")}</button>`;
    }).join("")).join("");
    const ocupados = Object.values(h.equip).filter(Boolean).length;
    const attrs = Object.entries(h.atributos).map(([k, v]) => {
      const pen = (h.atributos_penal || {})[k];
      const linhas = (h.atributos_info[k] || []).map((l, i) => `<li${pen && !i ? ' class="pior"' : ""}>${esc(l)}</li>`).join("");
      const dica = `<b class="t">${esc(k)} ${v}${pen ? ` <span class="pior">(−${pen.pct}%)</span>` : ""}</b><ul>${linhas}</ul>`;
      return `<div class="f-attr f-foco${pen ? " abaixo" : ""}" tabindex="0" data-dica="${esc(dica)}">${img(ICONE_ATTR[k], versao === "assets" ? 24 : 16)}<span class="n">${esc(k)}</span><span class="v">${v}${pen ? `<small>−${pen.pct}%</small>` : ""}</span></div>`;
    }).join("");
    const feridas = h.ferimentos.map((f) => {
      const tag = f.aberto ? '<span class="tag aberto">aberto</span>' : f.dias ? `<span class="tag">${f.dias} dias</span>` : "";
      const dica = `<b class="t">${esc(f.nome)}</b><div class="sub">${f.dias ? `${f.dias} dias para sarar` : "não sara sozinha"}${f.aberto ? " · ferida aberta" : ""}</div>` +
        (f.explica || []).map((l, i) => `<div class="${i ? "" : "pior"}">${esc(l)}</div>`).join("");
      return `<div class="f-linha ferida f-foco" tabindex="0" data-dica="${esc(dica)}"><img src="${Sprites.url("gota")}" alt=""><span class="nm">${esc(f.nome)}</span>${tag}</div>`;
    });
    const condicoes = (h.condicoes || []).map((c) => {
      const dica = `<b class="t">${esc(c.texto)}</b>${c.dica.map((l) => `<div>${esc(l)}</div>`).join("")}`;
      return `<div class="f-linha fome${c.grave ? " grave" : ""} f-foco" tabindex="0" data-dica="${esc(dica)}"><img src="${Sprites.url(c.icone)}" alt=""><span class="nm">${esc(c.texto)}</span><span class="tag">${c.grave ? "grave" : "fome"}</span></div>`;
    });
    const estado = [...feridas, ...condicoes].join("") || '<div class="f-nada">Sem ferimentos nem fome.</div>';
    const bolsa = h.bolsa.filter((b) => b.id !== "tocha").map((b) => {
      const dica = `<b class="t">${esc(b.nome)}</b>${b.trata ? `<div class="melhor">${esc(b.trata)}</div>` : ""}<div>${esc(b.desc)}</div>` +
        `<div class="rodape">${b.motivo ? esc(b.motivo) : "Clique para usar."}</div>`;
      return `<button type="button" class="f-slot f-foco${b.motivo ? " inutil" : ""}" data-dica="${esc(dica)}" aria-label="${esc(b.nome)}: ${b.qtd}">${img(ICONES_BOLSA[b.id] || "pocao")}<span class="f-qtd">${b.qtd}</span></button>`;
    }).join("");
    const r = h.reputacao_info, sinal = h.reputacao > 0 ? "mais" : h.reputacao < 0 ? "menos" : "zero";
    const rep = `<div class="f-rep f-foco" tabindex="0" data-dica="${esc(`<b class="t">Reputação</b><div class="sub">${esc(r.titulo)} · ${h.reputacao > 0 ? "+" : ""}${h.reputacao}</div><ul>${r.linhas.map((l) => `<li>${esc(l)}</li>`).join("")}</ul>`)}">` +
      `<img src="${Sprites.url("coroa")}" alt=""><span>${esc(r.titulo)}</span><span class="v ${sinal}">${h.reputacao > 0 ? "+" : h.reputacao < 0 ? "−" : ""}${Math.abs(h.reputacao)}</span></div>`;
    const pct = Math.max(0, Math.min(100, (100 * h.xp) / h.xp_proximo));
    raiz.innerHTML = `
      <header class="f-identidade">
        <div class="f-retrato">${versao === "assets" ? '<img class="ia" src="assets/exibicao/retrato.png" alt="Retrato do Guerreiro">' : `<img src="${Arte.retrato()}" alt="Retrato do Guerreiro">`}</div>
        <div class="f-nome">${esc(nome)}</div><div class="f-titulo">${esc(h.titulo)}<br><b>nível ${h.nivel}</b></div>
        <div class="f-xp"><div class="f-legenda"><span>Experiência</span><b>${h.xp}/${h.xp_proximo}</b></div><div class="f-barra"><i style="width:${pct}%"></i></div></div>
        ${h.pontos_talento ? `<div class="f-talento f-foco" tabindex="0" role="button" data-dica="${esc('<b class="t">Talentos</b><div>Abre a árvore de talentos.</div>')}"><img src="${Sprites.url("estrela")}" alt="">${h.pontos_talento} ${h.pontos_talento === 1 ? "ponto de talento" : "pontos de talento"}</div>` : ""}
      </header>
      <div class="f-corpo">
        <section class="f-secao"><h3 class="f-sec">Atributos</h3><div class="f-atributos">${attrs}</div></section>
        <section class="f-secao"><h3 class="f-sec">Equipamento <small>${ocupados} de 10</small></h3><div class="f-espacos">${espacos}</div></section>
        <section class="f-secao"><h3 class="f-sec">Ferimentos e condições</h3>${estado}</section>
        <section class="f-secao"><h3 class="f-sec">Bolsa</h3>${bolsa ? `<div class="f-bolsa">${bolsa}</div>` : '<div class="f-nada">Vazia.</div>'}</section>
        <section class="f-secao"><h3 class="f-sec">Reputação</h3>${rep}</section>
      </div>`;
    acomodarNome(raiz);
  }

  /** O nome ao lado do retrato; se não cabe (passa da borda ou de duas linhas), uma linha própria em cima; se nem
   *  assim, um passo menor. Como a ficha atual faz (acomodarNome), com o mesmo critério. */
  function acomodarNome(raiz) {
    const id = raiz.querySelector(".f-identidade"), n = id.querySelector(".f-nome");
    id.classList.remove("nome-longo", "nome-enorme");
    const linhas = () => Math.round(n.getBoundingClientRect().height / parseFloat(getComputedStyle(n).lineHeight || 32));
    const sobra = () => n.scrollWidth > n.clientWidth + 1;
    if (sobra() || linhas() > 2) id.classList.add("nome-longo");
    if (sobra() || linhas() > 2) id.classList.add("nome-enorme");
  }

  // ------------------------------------------------------------ a dica: ao lado do painel, à direita
  let dica = null, dono = null;
  function abrirDica(el) {
    if (!dica) { dica = document.createElement("div"); dica.setAttribute("role", "tooltip"); document.body.appendChild(dica); }
    dica.className = { assets: "f-dica v2", hud3: "f-dica v3" }[versao] || "f-dica";
    if (/^\d+$/.test(el.dataset.dica)) return;  // as dicas numeradas da fotografia do jogo (sem o conteúdo delas)
    dono = el;
    dica.innerHTML = el.dataset.dica;
    dica.hidden = false;
    // Na ficha: à direita do painel, na altura do elemento; nunca por cima dele. Se passar do pé da janela, sobe.
    // Fora dela (o topo): logo embaixo do elemento, sem sair da janela.
    const ficha = el.closest("#ficha"), r = el.getBoundingClientRect(), d = dica.getBoundingClientRect();
    const x = ficha ? ficha.getBoundingClientRect().right + 8 : Math.max(8, Math.min(r.left, innerWidth - d.width - 8));
    const y = ficha ? Math.max(8, Math.min(r.top - 6, innerHeight - d.height - 8)) : Math.min(r.bottom + 6, innerHeight - d.height - 8);
    dica.style.left = `${Math.round(x)}px`; dica.style.top = `${Math.round(y)}px`;
  }
  function fecharDica() { if (dica) dica.hidden = true; dono = null; }
  function ligarDicas(raiz) {
    raiz.addEventListener("mouseover", (ev) => { const el = ev.target.closest("[data-dica]"); if (el && el !== dono) abrirDica(el); });
    raiz.addEventListener("mouseout", (ev) => { const el = ev.target.closest("[data-dica]"); if (el && !el.contains(ev.relatedTarget)) fecharDica(); });
    raiz.addEventListener("focusin", (ev) => { const el = ev.target.closest("[data-dica]"); if (el) abrirDica(el); });
    raiz.addEventListener("focusout", fecharDica);
    // A rolagem leva a dica junto quando o foco do teclado continua no elemento (o Tab que desce a lista rola o
    // painel); com o mouse, ela fecha.
    raiz.addEventListener("scroll", () => { if (dono && dono === document.activeElement) abrirDica(dono); else fecharDica(); }, true);
    document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") fecharDica(); });
  }

  return { desenhar, ligarDicas, fecharDica, set iconesNovos(v) { iconesNovos = v; }, set versao(v) { versao = v; } };
})();
