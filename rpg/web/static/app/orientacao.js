/* As orientações da abertura guiada (abertura.py; roadmapIDEIAS/18). O motor diz qual orientação vale e o texto; aqui
   se acha o controle e se desenha:
   - o destaque: um contorno fino em volta do controle, com o formato dele e um brilho que pulsa devagar (com
     movimento reduzido, só o contorno). Um controle por vez; some quando a ação acontece;
   - o quadro: na luta, numa faixa estável logo abaixo da arena (ou acima das cartas, quando cabe), que fica reservada
     enquanto durar a luta guiada; ele não acompanha a investida, o tremor nem o retorno das cartas: a posição só muda
     quando muda a etapa, o tamanho da janela ou o layout. Fora da luta, numa faixa da página: no alto para o que
     mora em cima ou ao lado (os prédios da vila, as provisões do topo, o aviso da noite) e embaixo, junto da doca,
     para o que mora embaixo (explorar, os atalhos da doca). A faixa entra com a orientação, antes de o texto correr,
     e só sai quando a cena muda: nada pula, e o quadro não troca de lugar durante a leitura (sobre a paisagem ele
     trocava quando o cenário encolhia com o texto). O quadro aparece quando o texto da cena terminou; se o controle
     está fora da parte visível da página, a página rola só o necessário, uma vez por etapa. No item achado (E1),
     logo abaixo da janela dele. Depois de um "Entendi", a próxima espera a cena seguinte (uma por vez, sem fila);
   - um véu leve só nas colunas laterais e na doca.
   C1–C3 se encerram pela própria ação (abrir Habilidades, escolher uma, escolher o alvo). O C4 explica o que a
   habilidade gastou, num momento estável depois do golpe (a próxima vez em que a pessoa pode agir), com "Entendi";
   se a habilidade encerrou a luta, ele não aparece (o espólio segue como sempre). As informativas (provisões,
   comitiva, talentos, noite) têm "Entendi"; as outras se encerram pela ação. "Encerrar tutorial" desliga todas as
   orientações; a Ajuda (F1, no topo) religa. */
"use strict";

const Orientacao = (() => {
  let quadro = null, anel = null, faixa = null, faixaDe = "", faixaCena = "", veus = [], dispensado = false;
  const fechados = new Set();  // as informativas fechadas com "Entendi" (o motor confirma no próximo estado)
  let pausa = "";             // a cena em que se deu o último "Entendi": nela, nenhum quadro novo
  let luta = null;           // a luta de agora: { c4: id da habilidade usada, feito, guiada }
  let passo = "";            // a etapa à vista (o quadro só se reposiciona quando ela muda, ou o layout)
  let layout = "";           // o tamanho da janela e da área do quadro, quando a posição foi calculada
  let controle = null;       // o controle destacado
  const esc = Texto.html;
  const visivel = (e) => { if (!e) return false; const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const negrito = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>");

  function montar() {
    if (quadro) return;
    quadro = el("div", "orientacao", "");
    quadro.setAttribute("role", "note");
    anel = el("div", "orientacao-anel", "");
    for (let k = 0; k < 3; k++) veus.push(el("div", "orientacao-veu", ""));
    [...veus, anel, quadro].forEach((x) => { x.hidden = true; document.body.appendChild(x); });
    // O clique no quadro é dele: não adianta texto nem escolhe ação (o documento não fica sabendo).
    quadro.addEventListener("click", (ev) => {
      ev.stopPropagation();
      if (ev.target.closest(".orientacao-encerrar")) encerrar();
      else if (ev.target.closest(".orientacao-entendi")) entendi();
    });
    quadro.addEventListener("pointerdown", (ev) => ev.stopPropagation());
    quadro.addEventListener("keydown", (ev) => {
      // Enter e espaço no "Entendi" fecham só o quadro (a mesma tecla não escolhe uma ação nem fecha a próxima cena).
      if (ev.target.closest(".orientacao-entendi") && (ev.key === "Enter" || ev.key === " ")) {
        ev.preventDefault(); ev.stopPropagation(); entendi();
      }
    });
  }

  function enviar(acao) {
    fetch("/orientacao", { method: "POST", headers: { "Content-Type": "application/json", "X-Token": TOKEN },
      body: JSON.stringify({ acao }) }).catch((e) => console.error(e));
  }

  function encerrar() {
    dispensado = true;  // some na hora; o motor confirma no próximo estado
    enviar("dispensar");
    esconder();
    soltarFaixa();
  }

  function entendi() {
    const id = passo.split("|")[0];
    if (id === "C4") { if (luta) luta.feito = true; }
    else if (id) { fechados.add(id); pausa = cenaAgora(); enviar("visto:" + id); }
    esconder();
  }

  function esconder() {
    if (!quadro) return;
    [...veus, anel, quadro].forEach((x) => { x.hidden = true; });
    passo = "";
    controle = null;
  }

  // ---------------------------------------------------------------- a faixa do quadro
  /** A faixa logo abaixo da arena (ou do cenário da vila), reservada enquanto durar a luta guiada (ou o V1): o quadro
   *  mora nela e nada da página fica por baixo dele. Na luta, se a arena tem espaço acima das cartas, ela não é criada. */
  function reservarFaixa(de, htmls, classe) {
    if (faixa && faixaDe === de) { faixaCena = cenaAgora(); return; }
    soltarFaixa();
    if (de === "luta" && acimaDasCartas()) return;
    const pagina = document.querySelector("#cena #pagina");
    if (!pagina) return;
    faixa = el("div", "orientacao-faixa", "");
    faixaDe = de;
    faixaCena = cenaAgora();
    faixa.setAttribute("aria-hidden", "true");
    // A altura do maior quadro que vai morar nela (na luta, o C4 da classe), medida antes: a faixa não muda de tamanho
    // entre as etapas.
    faixa.style.height = alturaDoMaior(htmls, classe) + 16 + "px";
    // "baixo": depois da página, junto da doca (o que mora embaixo); as outras, antes dela (logo abaixo do cenário).
    pagina.parentNode.insertBefore(faixa, de === "baixo" ? pagina.nextSibling : pagina);
  }
  /** A cena à vista (o título e o tipo): a faixa de fora da luta fica até ela mudar, mesmo depois do "Entendi". */
  const cenaAgora = () => { const c = document.querySelector("#cena"); const h = document.querySelector("#cena-cab");
    return (c ? c.dataset.tipo || "" : "") + "|" + (h ? h.textContent : ""); };
  function alturaDoMaior(htmls, classe) {
    const prova = el("div", classe, "");
    Object.assign(prova.style, { visibility: "hidden", left: "-9999px", top: "0" });
    document.body.appendChild(prova);
    let h = 40;
    htmls.forEach((x) => { prova.innerHTML = x; h = Math.max(h, prova.offsetHeight); });
    prova.remove();
    return h;
  }
  function soltarFaixa() { if (faixa) { faixa.remove(); faixa = null; faixaDe = ""; faixaCena = ""; } }
  /** A vila à vista, com os prédios clicáveis (não diante de um balcão nem com a câmera num prédio). */
  const vilaAVista = () => { const p = document.querySelector("#predios"); return !!p && !p.hidden && !p.classList.contains("focado"); };

  /** A área livre acima das cartas da arena, se couber o maior quadro (o do C4); senão null. */
  function acimaDasCartas() {
    const arena = document.querySelector("#arena");
    const cartas = [...document.querySelectorAll("#arena .carta")];
    if (!arena || !cartas.length) return null;
    const a = arena.getBoundingClientRect();
    const topo = Math.min(...cartas.map((c) => c.getBoundingClientRect().top));
    return topo - a.top >= 140 ? { left: a.left + 8, top: a.top + 6, width: a.width - 16, height: topo - a.top - 12 } : null;
  }

  // ---------------------------------------------------------------- qual passo, onde
  /** O passo de agora: o controle a destacar, o HTML do quadro e onde ele mora. Ou null. */
  function alvo() {
    const o = estado && estado.orientacao && estado.orientacao.atual;
    if (!o || dispensado || !estado.orientacao.ligado) return null;
    if (fechados.has(o.id) || (pausa && pausa === cenaAgora())) return null;
    pausa = "";
    // Uma janela por cima (Ajuda, mapa, confirmação) esconde o quadro; a do item achado, só se ele não é sobre ela.
    if (document.querySelector(".sobreposicao:not([hidden]):not(#sobre-achado), #janela-confirmar")) return null;
    if (o.id !== "E1" && document.querySelector("#sobre-achado")) return null;
    if (o.ancora && o.ancora.startsWith("selo:")) {
      // Um selo novo numa carta (Firme, um mal, um bem): num momento parado da luta, perto da arena, com "Entendi".
      const [, uid, ef] = o.ancora.split(":");
      const selo = document.querySelector(`#arena .carta[data-uid="${uid}"] .ef[data-ef="${ef}"]`);
      if (!estado.combate || !visivel(selo) || !pergunta || processando) return null;
      return { id: o.id, el: selo, html: botoes(negrito(o.texto), true), luta: true };
    }
    if (o.id === "combate") {
      if (!estado.combate || !luta || luta.feito) return null;
      const p = o.passos;
      if (luta.c4) {
        // Só num momento estável: o golpe já foi, e a pessoa pode agir de novo (a roda voltou).
        const barra = document.querySelector('#arena .carta[data-uid="j"] .carta-rec');
        if (!visivel(barra) || !pergunta || processando || !p.C4[luta.c4]) return null;
        return { id: "C4", el: barra, html: htmlC4(p.C4[luta.c4]), luta: true };
      }
      const linha = document.querySelector(`.roda-janela .rj-linha[data-hab="${o.hab}"]`) || document.querySelector(".roda-janela .rj-linha[data-hab]");
      if (visivel(linha)) return { id: "C2", el: linha, html: botoes(negrito(p.C2)), luta: true, aoLado: linha.closest(".roda-janela") };
      const mira = document.querySelector("#arena .carta.alvejavel");
      if (visivel(mira)) return { id: "C3", el: mira, html: botoes(negrito(p.C3)), luta: true };
      const hab = document.querySelector('#roda .roda-botao[data-slot="habilidades"]');
      if (visivel(hab) && pergunta && !processando) return { id: "C1", el: hab, html: botoes(negrito(p.C1)), luta: true };
      return null;
    }
    const a = ancora(o);
    return a ? { id: o.id, el: a.el, onde: a.onde, html: botoes(negrito(o.texto), !!o.entendi), luta: false } : null;
  }

  /** Onde mora cada orientação de fora da luta: o controle e a faixa (vila: a do alto, abaixo do cenário; topo: a do
   *  alto; baixo: a de baixo; achado: junto da janela do item). Só quando ele está à vista e a pergunta é de agora. */
  function ancora(o) {
    if (!o.ancora || estado.combate || !pergunta || processando) return null;  // o texto da cena já terminou
    const [tipo, valor] = o.ancora.split(":");
    const ok = (e, onde) => (visivel(e) ? { el: e, onde } : null);
    if (tipo === "mural" || tipo === "predio") {
      if (!vilaAVista()) return null;
      return ok(document.querySelector(`#predios .predio[data-predio="${tipo === "mural" ? "mural" : valor}"]`), "vila");
    }
    if (tipo === "provisoes") return ok(document.querySelector('#hud .recurso[data-rec="provisoes"]'), "topo");
    if (tipo === "aceitar") return ok(document.querySelector(`#texto [data-aceitar="${valor}"]`), "topo");  // no Mural
    if (tipo === "contrato") return ok(document.querySelector(`#mundo .rastro-contrato[data-contrato="${valor}"]`), "topo");
    if (tipo === "bolsa") return ok(document.querySelector(`#heroi .slot-px[data-bolsa="${valor}"]`), "topo");
    if (tipo === "topo") return ok(document.querySelector(`[data-acao="${valor}"]`), "topo");
    if (tipo === "membro") return ok(document.querySelector(`#heroi .membro[data-cid="${valor}"]`), "topo");
    if (tipo === "mod") return ok([...document.querySelectorAll("#modificadores .mod")].find((m) => /Inimigos/.test(m.textContent)), "topo");
    if (tipo === "opcao") return ok([...document.querySelectorAll("#prompt .escolhas:not(.escolhido) .escolha")].find((e) => e.textContent.includes(valor)), "baixo");
    if (tipo === "doca") {
      if (document.querySelector("#doca.inativa")) return null;
      return ok(document.querySelector(`#doca .atalho[data-rotulo="${valor}"]`), "baixo");
    }
    if (tipo === "achado") {  // a comparação, quando os botões da decisão já chegaram
      if (!document.querySelector("#sobre-achado .achado-acoes button:not(.reserva)")) return null;
      return ok(document.querySelector("#sobre-achado .achado-cartao.novo .comparacao") || document.querySelector("#sobre-achado .achado-cartao.atual"), "achado");
    }
    return null;
  }
  /** A faixa que a orientação de agora pede (antes de a âncora aparecer: a faixa entra antes de o texto correr). */
  function faixaPedida(o) {
    if (!o || !o.ancora || dispensado || fechados.has(o.id) || estado.combate) return "";
    const tipo = o.ancora.split(":")[0];
    if (tipo === "mural" || tipo === "predio") return estado.local.tipo === "vila" && visivel(document.querySelector("#vista")) ? "alto" : "";
    if (["provisoes", "membro", "mod", "aceitar", "contrato", "bolsa", "topo"].includes(tipo)) return "alto";
    if (tipo === "opcao" || tipo === "doca") return "baixo";
    return "";
  }

  const ENCERRAR = '<button type="button" class="orientacao-encerrar" title="Desliga todas as orientações; a Ajuda (F1) religa">Encerrar tutorial</button>';
  function botoes(html, entendi = false) {
    return `<div class="orientacao-texto">${html}</div><div class="orientacao-botoes">${entendi ? '<button type="button" class="orientacao-entendi">Entendi</button>' : ""}${ENCERRAR}</div>`;
  }

  /** O C4 em linhas curtas: o nome da habilidade; os custos com o ícone e a cor do recurso; o Atacar. */
  function parte(x) {
    if (x.rec) return `<span class="o-valor rec-${RECURSO_BARRA[x.rec] || "mana"}">${spr(RECURSO_ICONE[x.rec] || "estrela", 1)}${esc(x.t)}</span>`;
    if (x.flecha) return `<span class="o-valor flecha">${spr("flecha", 1)}${esc(x.t)}</span>`;
    return esc(x.t);
  }
  function htmlC4(c) {
    return botoes(`<div class="o-nome">${esc(c.nome)}</div><div class="o-custos">${c.gasto.map(parte).join(" ")}</div>
      <div class="o-atacar">${c.atacar.map(parte).join("")}</div>`, true);
  }

  // ---------------------------------------------------------------- desenhar
  function desenhar() {
    const a = alvo();
    // Fora da luta, a faixa entra assim que a orientação vale (antes de o texto correr: nada pula quando o menu chega)
    // e sai quando a cena muda sem que ela continue valendo (não a cada piscar da pergunta, nem logo no "Entendi").
    const o = estado && estado.orientacao;
    const pedida = o && o.ligado ? faixaPedida(o.atual) : "";
    if (pedida) reservarFaixa(pedida, [botoes(negrito(o.atual.texto), !!o.atual.entendi)], "orientacao");
    else if (faixa && faixaDe !== "luta" && (cenaAgora() !== faixaCena || dispensado || !o || !o.ligado)) soltarFaixa();
    document.body.classList.toggle("orientando-mural", !!a && a.id === "V1");
    if (!a) { esconder(); destacar(null); return; }
    montar();
    if (a.luta) {
      const pss = estado.orientacao.atual.passos;  // a sequência da primeira luta mede pelo maior C4; um selo, por ele
      reservarFaixa("luta", pss ? Object.values(pss.C4 || {}).map(htmlC4) : [a.html], pss ? "orientacao c4" : "orientacao");
    }
    const chave = a.id + "|" + a.html;
    if (!a.luta && chave !== passo) trazerAVista(a.el);  // uma vez por etapa, antes de medir
    const zona = a.luta ? (faixa ? faixa.getBoundingClientRect() : acimaDasCartas())
      : faixa && a.onde !== "achado" ? faixa.getBoundingClientRect() : null;
    // Fora da luta, o prédio pode andar com a câmera (a vila se monta): a posição horizontal dele entra na conta (a
    // vertical, não: rolar a página para ler não mexe no quadro). Na luta, nada: a carta avança e treme, e o quadro
    // fica parado.
    const ancora = a.luta ? "" : [a.el.getBoundingClientRect()].map((r) => [r.left, r.width].map(Math.round).join(",")).join("");
    const lay = `${innerWidth}x${innerHeight}|${zona ? [zona.left, zona.top, zona.width, zona.height].map(Math.round).join(",") : ""}|${ancora}`;
    if (chave !== passo || lay !== layout) {
      if (chave !== passo) {
        quadro.innerHTML = a.html;
        if (a.id === "C4") requestAnimationFrame(() => quadro.querySelector(".orientacao-entendi")?.focus({ preventScroll: true }));
      }
      passo = chave;
      layout = lay;
      quadro.hidden = false;
      posicionar(a, zona);
    }
    // Um destaque por controle: o que o jogo já acende (os Talentos com ponto, ★; o baú pronto, com o anel dourado)
    // fica só com a seta do quadro.
    destacar(a.el.classList.contains("destaque") || a.el.classList.contains("pronto") ? null : a.el);
    veu(a);
  }

  /** O controle dentro da página que rola (a opção do menu) e fora da parte visível dela: a página rola só o
   *  necessário para ele aparecer inteiro, com uma folga. Chamada uma vez por etapa: a leitura não é interrompida
   *  por rolagens repetidas, e quem rolar depois fica onde rolou. */
  function trazerAVista(e) {
    const pg = e.closest("#pagina");
    if (!pg) return;
    const r = e.getBoundingClientRect(), v = pg.getBoundingClientRect(), folga = 8;
    if (r.bottom > v.bottom - folga) pg.scrollTop += Math.ceil(r.bottom - v.bottom + folga);
    else if (r.top < v.top + folga) pg.scrollTop -= Math.ceil(v.top + folga - r.top);
  }

  /** Onde o quadro fica: calculado na mudança de etapa ou de layout, nunca a cada quadro da animação. */
  function posicionar(a, zona) {
    const r = a.el.getBoundingClientRect(), w = quadro.offsetWidth, h = quadro.offsetHeight, vw = innerWidth, vh = innerHeight;
    let x, y, lado;
    if (a.onde === "achado") {
      // O item achado: logo abaixo da janela dele (ou acima, se não couber), com a seta para a comparação.
      const jan = document.querySelector("#sobre-achado .janela-achado").getBoundingClientRect();
      x = r.left + r.width / 2 - w / 2;
      y = jan.bottom + 12;
      lado = "baixo";
      if (y + h > vh - 8) { y = jan.top - 12 - h; lado = "cima"; }
    } else if (zona && !a.luta && (r.right <= zona.left || r.left >= zona.left + zona.width) && r.bottom > zona.top) {
      // O controle mora numa coluna ao lado (o cartão da comitiva): o quadro na ponta da zona, a seta para o lado.
      const esquerda = r.right <= zona.left;
      x = esquerda ? zona.left + 4 : zona.left + zona.width - w - 4;
      y = zona.top + Math.max(4, (zona.height - h) / 2);
      lado = esquerda ? "direita" : "esquerda";
    } else if (zona && !a.luta) {
      // Na faixa: alinhado ao controle, do lado dele (acima ou abaixo), a seta apontando para ele.
      x = r.left + r.width / 2 - w / 2;
      x = Math.max(zona.left + 4, Math.min(zona.left + zona.width - w - 4, x));
      const abaixo = r.top + r.height / 2 < zona.top + zona.height / 2;  // o controle está acima da zona
      y = zona.top + Math.max(4, (zona.height - h) / 2);
      lado = abaixo ? "baixo" : "cima";
    } else if (zona) {
      // Na faixa (ou acima das cartas): alinhado ao controle; ao lado da janelinha de Habilidades quando ela está aberta.
      // A janelinha de Habilidades desce sobre a faixa: o quadro vai para o lado dela que tem espaço.
      const jan = a.aoLado && a.aoLado.getBoundingClientRect();
      if (jan) x = jan.right + 12 + w <= zona.left + zona.width ? jan.right + 12 : jan.left - 12 - w;
      else x = r.left + r.width / 2 - w / 2;
      x = Math.max(zona.left + 4, Math.min(zona.left + zona.width - w - 4, x));
      y = zona.top + Math.max(4, (zona.height - h) / 2);
      lado = jan ? (x >= jan.right ? "direita" : "esquerda") : zona.top >= r.bottom ? "baixo" : "cima";
    } else {
      x = r.left + r.width / 2 - w / 2;
      y = r.bottom + 12;
      lado = "baixo";
      if (y + h > vh - 8) { y = r.top - 12 - h; lado = "cima"; }
    }
    x = Math.max(8, Math.min(vw - w - 8, x));
    y = Math.max(8, Math.min(vh - h - 8, y));
    quadro.className = `orientacao seta-${lado}${a.id === "C4" ? " c4" : ""}${a.onde === "achado" ? " sobre-janela" : ""}`;
    anel.classList.toggle("sobre-janela", a.onde === "achado");
    quadro.style.setProperty("--seta", (lado === "direita" || lado === "esquerda" ? Math.max(10, Math.min(h - 10, r.top + r.height / 2 - y))
      : Math.max(12, Math.min(w - 12, r.left + r.width / 2 - x))) + "px");
    quadro.style.left = Math.round(x) + "px";
    quadro.style.top = Math.round(y) + "px";
  }

  /** O contorno acompanha o controle (ele pode se mexer: o anel é dele, o quadro não). Um controle por vez. */
  function destacar(e) {
    controle = e;
    if (!anel) return;
    if (!e) { anel.hidden = true; return; }
    const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
    anel.hidden = false;
    Object.assign(anel.style, { left: r.left - 3 + "px", top: r.top - 3 + "px", width: r.width + 6 + "px", height: r.height + 6 + "px",
      borderRadius: cs.borderRadius && cs.borderRadius !== "0px" ? `calc(${cs.borderRadius} + 3px)` : "0" });
  }

  /** O véu: só as colunas laterais e a doca (nunca a arena, as cartas, as barras, o topo nem a página). */
  function veu(a) {
    ["#heroi", "#mundo", "#doca"].forEach((s, k) => {
      const e = document.querySelector(s), v = veus[k];
      if (!visivel(e) || e.contains(a.el) || a.onde === "achado") { v.hidden = true; return; }
      const q = e.getBoundingClientRect();
      v.hidden = false;
      Object.assign(v.style, { left: q.left + "px", top: q.top + "px", width: q.width + "px", height: q.height + "px" });
    });
  }

  function laco() { desenhar(); requestAnimationFrame(laco); }

  /** O estado novo: uma luta que começa zera os passos dela; o fim da luta solta a faixa. */
  function aoEstado(e) {
    const emLuta = !!(e && e.combate);
    if (emLuta && !luta) luta = { c4: null, feito: false };
    if (!emLuta) { luta = null; if (faixaDe === "luta") soltarFaixa(); }
    if (e && e.orientacao && e.orientacao.ligado) dispensado = false;
    const agora = e && e.orientacao && e.orientacao.atual;
    fechados.forEach((id) => { if (!agora || agora.id !== id) fechados.delete(id); });  // o motor já confirmou
    if (!$("#sobre-ajuda").hidden) desenharAjuda();
  }

  /** O golpe do herói (Batalha.lance "acao"): usada uma habilidade, o C4 vem na próxima vez em que se pode agir. */
  function aoLance(m) {
    if (luta && !luta.feito && m.tipo === "acao" && m.de === "j" && m.hab && m.hab !== "ataque") luta.c4 = m.hab;
  }

  /** Uma resposta da pessoa: com o C4 à vista, agir também o fecha (Entendi não é obrigatório). */
  function aoResponder() {
    if (luta && luta.c4 && passo.startsWith("C4")) luta.feito = true;
  }

  // ---------------------------------------------------------------- a Ajuda
  function desenharAjuda() {
    const o = estado && estado.orientacao;
    const corpoAjuda = $("#ajuda-corpo");
    if (!o) { corpoAjuda.innerHTML = '<p class="vazio">Comece ou carregue um jogo para ver as orientações dele.</p>'; return; }
    const grupos = {};
    o.linhas.forEach((l) => { (grupos[l.grupo] = grupos[l.grupo] || []).push(l.texto); });
    const lista = Object.entries(grupos).map(([g, ls]) => `<h3>${esc(g)}</h3><ul>${ls.map((t) => `<li>${negrito(t)}</li>`).join("")}</ul>`).join("");
    corpoAjuda.innerHTML = `<button type="button" class="botao-janela ajuda-chave" aria-pressed="${o.ligado}">Mostrar orientações: <b>${o.ligado ? "ligado" : "desligado"}</b></button>
      ${lista || '<p class="vazio">Nenhuma orientação vista ainda neste jogo.</p>'}`;
    corpoAjuda.querySelector(".ajuda-chave").addEventListener("click", (ev) => {
      ev.stopPropagation();
      enviar(o.ligado ? "dispensar" : "ligar");
      o.ligado = !o.ligado;  // a tela responde na hora; o estado do motor confirma
      dispensado = !o.ligado;
      desenharAjuda();
    });
  }

  function alternarAjuda(forcar) {
    const s = $("#sobre-ajuda");
    s.hidden = forcar === undefined ? !s.hidden : !forcar;
    if (!s.hidden) { desenharAjuda(); s.querySelector(".ajuda-chave, button")?.focus(); }
  }

  requestAnimationFrame(laco);
  return { aoEstado, aoLance, aoResponder, alternarAjuda, esconder };
})();
