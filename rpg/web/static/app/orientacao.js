/* As orientações da abertura guiada (abertura.py; roadmapIDEIAS/18). O motor diz qual orientação vale e o texto; aqui
   se acha o controle e se desenha:
   - o destaque: um contorno fino em volta do controle, com o formato dele e um brilho que pulsa devagar (com
     movimento reduzido, só o contorno). Um controle por vez; some quando a ação acontece;
   - o quadro: na luta, numa faixa estável logo abaixo da arena (ou acima das cartas, quando cabe), que fica reservada
     enquanto durar a luta guiada; ele não acompanha a investida, o tremor nem o retorno das cartas: a posição só muda
     quando muda a etapa, o tamanho da janela ou o layout. O ícone de efeito numa carta ganha uma haste da seta até
     ele (a ponta encosta no ícone) e um quadro estreito, que vai para o lado da janelinha de Habilidades aberta (sem
     lado livre, espera ela fechar). Fora da luta, numa faixa da página para os prédios da vila (no alto, abaixo do
     cenário) e para o que mora embaixo (explorar, os atalhos da doca, o Continuar); a faixa entra com a orientação e
     só sai quando a cena muda: nada pula. O resto fica encostado no controle, com a ponta da seta nele: nas colunas
     laterais (o baú, o contrato, os riscos do lugar), dentro da coluna, acima ou abaixo dele; no topo (provisões, o
     botão Texto), logo abaixo, sem cobrir as barras do herói; no Mural, acima do cartão. O encostado acompanha o
     controle quando a coluna ou a página rola e espera ele voltar se sair de vista. O quadro aparece quando o texto
     da cena terminou; se o controle está fora da parte visível da página ou da coluna, ela rola só o necessário, uma
     vez por etapa. No item achado (E1), logo abaixo da janela dele. Depois de um "Entendi", a próxima espera a cena
     seguinte (uma por vez, sem fila);
   - um véu leve só nas colunas laterais e na doca.
   Revelar o texto (A0) aparece com o texto correndo numa cena que acaba em Continuar e passa a apontar o Continuar
   quando ele chega; acelerar a animação (AL), com a animação da vez dos outros correndo na luta. Os dois passam
   quando a pessoa segue e não seguram as outras.
   C1–C3 se encerram pela própria ação (abrir Habilidades, escolher uma, escolher o alvo). O C4 explica o que a
   habilidade gastou, num momento estável depois do golpe (a próxima vez em que a pessoa pode agir), com "Entendi";
   se a habilidade encerrou a luta, ele não aparece (o espólio segue como sempre). As informativas (provisões,
   comitiva, talentos, noite) têm "Entendi"; as outras se encerram pela ação. "Encerrar tutorial" desliga todas as
   orientações; a Ajuda (F1, no topo) religa. */
"use strict";

const Orientacao = (() => {
  let quadro = null, anel = null, haste = null, faixa = null, faixaDe = "", faixaCena = "", veus = [], dispensado = false;
  const fechados = new Set();  // as informativas fechadas com "Entendi" (o motor confirma no próximo estado)
  let pausa = "";             // a cena em que se deu o último "Entendi": nela, nenhum quadro novo
  let luta = null;           // a luta de agora: { c4: id da habilidade usada, feito, guiada }
  let passo = "";            // a etapa à vista (o quadro só se reposiciona quando ela muda, ou o layout)
  let layout = "";           // o tamanho da janela e da área do quadro, quando a posição foi calculada
  let controle = null;       // o controle destacado
  let rolado = "";           // a etapa cujo controle já foi trazido à vista (uma rolagem por etapa)
  let a0Ativo = false;       // o A0 apareceu com o texto correndo: fica até o Continuar que fecha esse texto
  let animando = false;      // na luta, a animação do turno dos outros está correndo (o AL vale)
  let escondido = false;     // o quadro não coube sem cobrir a janelinha aberta: espera ela fechar
  let alMostrado = false;    // o AL já apareceu nesta luta (fica até a próxima ação da pessoa)
  const esc = Texto.html;
  const visivel = (e) => { if (!e) return false; const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const negrito = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>");
  // Uma linha por parágrafo do motor (o efeito da carta: o nome, o efeito de agora e, na primeira vez, a duração).
  // As notas (o que só complementa: a duração do ícone, a fome desta noite) chegam com "_" na frente e saem apagadas.
  const linhas = (s) => s.split("\n").map((l) => l.startsWith("_") ? `<div class="o-nota">${negrito(l.slice(1))}</div>` : `<div>${negrito(l)}</div>`).join("");

  function montar() {
    if (quadro) return;
    quadro = el("div", "orientacao", "");
    quadro.setAttribute("role", "note");
    anel = el("div", "orientacao-anel", "");
    haste = el("div", "orientacao-haste", "");
    for (let k = 0; k < 3; k++) veus.push(el("div", "orientacao-veu", ""));
    [...veus, anel, haste, quadro].forEach((x) => { x.hidden = true; document.body.appendChild(x); });
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

  /** Uma orientação da apresentação que apareceu e a pessoa seguiu: não volta (o motor confirma). */
  function passou(id) {
    if (id === "AL") alMostrado = false;
    if (id === "A0") a0Ativo = false;
    if (fechados.has(id)) return;
    fechados.add(id);
    enviar("visto:" + id);
  }

  function entendi() {
    const id = passo.split("|")[0];
    if (id === "C4") { if (luta) luta.feito = true; }
    else if (id === "AL") passou("AL");  // na luta: sem pausa (os ícones de efeito seguem podendo aparecer)
    else if (id) { fechados.add(id); pausa = cenaAgora(); enviar("visto:" + id); }
    esconder();
  }

  function esconder() {
    if (!quadro) return;
    [...veus, anel, quadro, haste].forEach((x) => { x.hidden = true; });
    passo = "";
    controle = null;
    document.body.classList.remove("orientando-texto");
  }

  // ---------------------------------------------------------------- a faixa do quadro
  /** A faixa logo abaixo da arena (ou do cenário da vila), reservada enquanto durar a luta guiada (ou o V1): o quadro
   *  mora nela e nada da página fica por baixo dele. Na luta, se a arena tem espaço acima das cartas, ela não é criada. */
  function reservarFaixa(de, htmls, classe) {
    if (faixa && faixaDe === de) {
      faixaCena = cenaAgora();
      // Na luta, um quadro maior que o da faixa (o ícone de efeito depois do aviso da animação): ela cresce, uma vez.
      const alt = alturaDoMaior(htmls, classe) + 16;
      if (de === "luta" && alt > faixa.offsetHeight) faixa.style.height = alt + "px";
      return;
    }
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
      // A janelinha de Habilidades (ou Itens) aberta desce sobre a faixa: o quadro vai para o lado dela.
      return { id: o.id, el: selo, html: botoes(linhas(o.texto), true), luta: true, haste: true,
        aoLado: document.querySelector(".roda-janela:not([hidden])") };
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
    // O prédio da vila mora na paisagem, acima da faixa; a opção do menu pode ficar acima da faixa de baixo: uma haste
    // leva a ponta da seta até eles.
    return a ? { id: o.id, el: a.el, onde: a.onde, prefere: a.prefere, haste: a.onde === "vila" || a.onde === "baixo", html: botoes(linhas(o.texto), !!o.entendi), luta: false } : null;
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
    // "junto": o quadro encostado no controle, a seta tocando nele (nas colunas, dentro da coluna dele).
    if (tipo === "provisoes") return ok(document.querySelector('#hud .recurso[data-rec="provisoes"]'), "junto");
    if (tipo === "aceitar") {  // no Mural: o cartão do contrato inteiro (o Aceitar está nele)
      const b = document.querySelector(`#texto [data-aceitar="${valor}"]`);
      return ok(b && (b.closest(".contrato") || b), "junto");
    }
    if (tipo === "contrato") return ok(document.querySelector(`#mundo .rastro-contrato[data-contrato="${valor}"]`), "junto");
    if (tipo === "bolsa") {
      // Só quando o menu de agora aceita a abertura (não enquanto a página espera Continuar): o clique funciona.
      if (pergunta.tipo !== "opcoes" || !pergunta.opcoes.some((x) => x.meta && x.meta.usar === valor)) return null;
      // Abaixo da bolsa, quando cabe: acima ficam os ferimentos, que a bandagem trata (o quadro não os cobre).
      const r = ok(document.querySelector(`#heroi .slot-px[data-bolsa="${valor}"]`), "junto");
      return r && { ...r, prefere: "baixo" };
    }
    if (tipo === "topo") return ok(document.querySelector(`[data-acao="${valor}"]`), "junto");
    if (tipo === "ferimento") return ok(document.querySelector(`#heroi .ferimento[data-ferimento="${valor}"]`), "junto");  // na ficha
    if (tipo === "tratar") return ok(document.querySelector(`#texto .curandeira [data-tratar="${valor}"]`), "junto");  // o cartão
    if (tipo === "servico") return ok(document.querySelector(`#prompt .balcao-predio .servico[data-servico="${valor}"]`), "junto");
    if (tipo === "dormir") {
      // Na fogueira: o botão fica no alto do cenário; o quadro vai à esquerda dele, sobre o céu, sem cobrir a roda.
      const r = ok(document.querySelector("#texto .dormir-barraca"), "junto");
      return r && { ...r, prefere: "esquerda" };
    }
    if (tipo === "risco") {  // os riscos do lugar, à direita: a linha da noite e, junto, a da tocha
      const linha = document.querySelector(`#mundo .risco-lugar.${valor}`);
      return ok(linha && linha.closest(".riscos-lugar"), "junto");
    }
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
    // O AL à vista fica até o Entendi ou a próxima ação da pessoa: um ícone novo na carta espera ele (não o tira da
    // tela antes de dar para ler).
    const a = (alMostrado && apresentacao()) || alvo() || apresentacao() || contextual();
    // Fora da luta, a faixa entra assim que a orientação vale (antes de o texto correr: nada pula quando o menu chega)
    // e sai quando a cena muda sem que ela continue valendo (não a cada piscar da pergunta, nem logo no "Entendi").
    const o = estado && estado.orientacao;
    const pedida = o && o.ligado ? faixaPedida(o.atual) : "";
    if (pedida) reservarFaixa(pedida, [botoes(linhas(o.atual.texto), !!o.atual.entendi)], "orientacao");
    else if (faixa && faixaDe !== "luta" && (cenaAgora() !== faixaCena || dispensado || !o || !o.ligado)) soltarFaixa();
    document.body.classList.toggle("orientando-mural", !!a && a.id === "V1");
    if (!a) { esconder(); destacar(null); return; }
    montar();
    if (a.id === "A0") reservarFaixa("baixo", [a.html], "orientacao");
    if (a.luta) {
      const pss = estado.orientacao.atual && estado.orientacao.atual.passos;  // a primeira luta mede pelo maior C4
      reservarFaixa("luta", pss ? Object.values(pss.C4 || {}).map(htmlC4) : [a.html], pss ? "orientacao c4" : a.haste ? "orientacao efeito" : "orientacao");
    }
    const chave = a.id + "|" + a.html;
    if (!a.luta && a.el && chave !== rolado) { trazerAVista(a.el); rolado = chave; }  // uma vez por etapa
    // O controle encostado (ou a opção do menu, sobre a faixa de baixo) que a pessoa rolou para fora da parte visível:
    // o quadro espera ele voltar (não rola de novo nem aponta para o que ficou escondido).
    if ((a.onde === "junto" || a.onde === "baixo") && !aVista(a.el)) { esconder(); destacar(null); return; }
    const zona = a.luta ? (faixa ? faixa.getBoundingClientRect() : acimaDasCartas())
      : faixa && a.onde !== "achado" && a.onde !== "junto" ? faixa.getBoundingClientRect() : null;
    // Fora da luta, o prédio pode andar com a câmera (a vila se monta): a posição horizontal dele entra na conta (a
    // vertical, não: rolar a página para ler não mexe no quadro da faixa). O quadro encostado acompanha o controle
    // inteiro (rolando a coluna ou a página, a seta continua tocando nele). Na luta, nada: a carta avança e treme, e
    // o quadro fica parado.
    const ra = a.el && a.el.getBoundingClientRect();
    const ancora = a.luta || !ra ? "" : (a.onde === "junto" ? [ra.left, ra.top, ra.width, ra.height] : [ra.left, ra.width]).map(Math.round).join(",");
    const janela = a.aoLado ? [a.aoLado.getBoundingClientRect()].map((r) => [r.left, r.right].map(Math.round).join(","))[0] : "";
    const lay = `${innerWidth}x${innerHeight}|${zona ? [zona.left, zona.top, zona.width, zona.height].map(Math.round).join(",") : ""}|${ancora}|${janela}`;
    if (chave !== passo || lay !== layout) {
      if (chave !== passo) {
        quadro.innerHTML = a.html;
        document.body.classList.toggle("orientando-texto", a.id === "A0");
        // O Entendi recebe o foco (Enter e espaço fecham só o quadro, sem escolher ação nem adiantar a animação).
        if (a.id === "C4" || a.id === "AL") requestAnimationFrame(() => quadro.querySelector(".orientacao-entendi")?.focus({ preventScroll: true }));
      }
      passo = chave;
      layout = lay;
      quadro.hidden = false;
      escondido = !posicionar(a, zona);
      if (escondido) { quadro.hidden = true; haste.hidden = true; }
    }
    if (escondido) { destacar(null); veus.forEach((v) => { v.hidden = true; }); return; }
    if (a.haste) esticarHaste(a.el);
    // Um destaque por controle: o que o jogo já acende (os Talentos com ponto, ★; o baú pronto, com o anel dourado)
    // fica só com a seta do quadro. Sem controle (o texto correndo, a animação), sem destaque nem véu.
    destacar(!a.el || a.semAnel || a.el.classList.contains("destaque") || a.el.classList.contains("pronto") ? null : a.el);
    if (a.el) veu(a); else veus.forEach((v) => { v.hidden = true; });
  }

  /** O retângulo do controle cortado pela coluna ou página que rola: o anel e a haste não passam da borda dela (a
   *  opção que a pessoa rolou até a faixa do quadro fica contornada só na parte que aparece). */
  function parteVisivel(e) {
    const r = e.getBoundingClientRect(), caixa = rolavel(e);
    if (!caixa) return r;
    const c = caixa.getBoundingClientRect(), top = Math.max(r.top, c.top), bottom = Math.min(r.bottom, c.bottom);
    return { left: r.left, right: r.right, width: r.width, top, bottom: Math.max(top, bottom), height: Math.max(0, bottom - top) };
  }

  /** O controle à vista dentro da coluna ou da página que rola (pelo menos metade dele). */
  function aVista(e) {
    const r = e.getBoundingClientRect(), caixa = rolavel(e);
    if (!caixa) return r.width > 0;
    const c = caixa.getBoundingClientRect();
    return Math.min(r.bottom, c.bottom) - Math.max(r.top, c.top) >= r.height / 2;
  }
  /** A coluna ou a página que rola em volta do controle (a página do meio, as colunas laterais), ou null. */
  function rolavel(e) {
    for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) {
      const o = getComputedStyle(p).overflowY;
      if ((o === "auto" || o === "scroll") && p.scrollHeight > p.clientHeight) return p;
    }
    return null;
  }

  // ---------------------------------------------------------------- a apresentação (A0, AL)
  /** Revelar o texto (A0) e acelerar a animação da luta (AL): o motor diz se ainda valem; a ocasião é daqui. O A0
   *  aparece com o texto correndo numa cena que acaba em Continuar e fica até o Continuar dela (a seta passa para
   *  ele quando ele chega); o AL, com a animação do turno dos outros correndo, até a próxima ação da pessoa. Nenhum
   *  dos dois aparece por cima de outra orientação. */
  function apresentacao() {
    const o = estado && estado.orientacao;
    const ap = o && o.ligado && !dispensado && o.apresentacao;
    if (!ap || replay || velocidade === "instantaneo") return null;
    if (document.querySelector(".sobreposicao:not([hidden]), #janela-confirmar")) return null;
    if (estado.combate) {
      if (pergunta) animando = false;
      if (!ap.AL || fechados.has("AL") || (o.atual && o.atual.id === "combate") || !(animando || (alMostrado && pergunta))) return null;
      alMostrado = true;
      return { id: "AL", el: null, html: botoes(negrito(ap.AL), true), luta: true };
    }
    // O A0 mora na faixa de baixo, junto do Continuar: não quando a orientação da vez já reservou a do alto.
    if (!ap.A0 || fechados.has("A0") || !["", "baixo"].includes(faixaPedida(o.atual))) return null;
    const cont = document.querySelector("#prompt .continuar");
    if (pergunta && pergunta.tipo !== "continuar") a0Ativo = false;  // a cena acabou num menu: a ocasião passou
    if (pergunta && pergunta.tipo === "continuar" && cont && a0Ativo)
      return { id: "A0", el: cont, onde: "baixo", haste: true, html: botoes(negrito(ap.A0)) };  // a seta vai até ele
    if (processando && !pergunta && continuarAdiante()) {
      a0Ativo = true;
      return { id: "A0", el: document.querySelector("#pagina"), onde: "baixo", semAnel: true, html: botoes(negrito(ap.A0)) };
    }
    return null;
  }
  /** As que valem quando o alvo aparece, sem segurar a fila (o cartão Dormir com a taverna aberta: D1): só quando
   *  nenhuma outra está à vista. */
  function contextual() {
    const o = estado && estado.orientacao;
    if (!o || !o.ligado || dispensado || estado.combate || (pausa && pausa === cenaAgora())) return null;
    for (const c of o.contextuais || []) {
      if (fechados.has(c.id)) continue;
      const a = ancora(c);
      if (a) return { id: c.id, el: a.el, onde: a.onde, html: botoes(linhas(c.texto), !!c.entendi), luta: false };
    }
    return null;
  }
  /** O que vem na fila depois do texto de agora termina num Continuar (não num menu nem numa pergunta). */
  function continuarAdiante() {
    const fim = fila.find((m) => ["opcoes", "continuar", "pergunta", "combate"].includes(m.t));
    return !!fim && fim.t === "continuar";
  }

  /** O controle dentro da página ou da coluna que rola (a opção do menu, o baú) e fora da parte visível dela: ela
   *  rola só o necessário para ele aparecer inteiro, com uma folga. Chamada uma vez por etapa: a leitura não é interrompida
   *  por rolagens repetidas, e quem rolar depois fica onde rolou. */
  function trazerAVista(e) {
    const pg = rolavel(e);  // a página do meio ou a coluna lateral (o baú, o contrato) que rola
    if (!pg) return;
    // Na página, antes de rolar, a arte do lugar se recolhe (como faria rolando à mão): o espaço vai para o texto, e a
    // rolagem é medida depois que ela termina de encolher.
    const cena = pg.id === "pagina" && document.querySelector("#cena");
    if (cena && !cena.classList.contains("recolhido") && !cena.classList.contains("vila-hub")
        && e.getBoundingClientRect().bottom > pg.getBoundingClientRect().bottom - 8 && typeof recolherArte === "function") {
      recolherArte(true);
      setTimeout(() => rolarAte(e, pg), 400);
      return;
    }
    rolarAte(e, pg);
  }
  /** Rola só o necessário para o controle aparecer inteiro, com uma folga. Uma opção do menu traz o menu inteiro,
   *  quando ele cabe: a opção seguinte não fica escondida atrás da faixa do quadro. */
  function rolarAte(e, pg) {
    if (!e.isConnected) return;
    const lista = e.closest(".escolhas"), folga = 8;
    const alvo = lista && lista.getBoundingClientRect().height <= pg.clientHeight - 2 * folga ? lista : e;
    const r = alvo.getBoundingClientRect(), v = pg.getBoundingClientRect();
    if (r.bottom > v.bottom - folga) pg.scrollTop += Math.ceil(r.bottom - v.bottom + folga);
    else if (e.getBoundingClientRect().top < v.top + folga) pg.scrollTop -= Math.ceil(v.top + folga - e.getBoundingClientRect().top);
  }

  /** Onde o quadro fica: calculado na mudança de etapa ou de layout, nunca a cada quadro da animação. */
  function posicionar(a, zona) {
    // Encostado num controle de coluna lateral (o baú, o contrato): o quadro cabe na largura da coluna.
    const col = a.onde === "junto" ? a.el.closest("#heroi, #mundo") : null;
    quadro.style.width = col ? Math.min(330, col.getBoundingClientRect().width - 12) + "px" : "";
    quadro.style.maxWidth = "";
    const tipo = `orientacao${a.id === "C4" ? " c4" : ""}${a.haste && a.luta ? " efeito" : ""}${a.onde === "achado" ? " sobre-janela" : ""}`;
    quadro.className = tipo;  // a largura do tipo vale já na medida
    const vw = innerWidth, vh = innerHeight;
    let w = quadro.offsetWidth, h = quadro.offsetHeight;
    const r = a.el ? a.el.getBoundingClientRect() : null;
    const PERTO = 8;  // do controle à borda do quadro: a ponta da seta encosta nele
    let x, y, lado;
    haste.hidden = true;
    if (!r) {
      // Sem controle (a animação da luta): no meio da faixa, sem seta.
      const z = zona || { left: 0, top: vh / 2, width: vw, height: 0 };
      x = z.left + (z.width - w) / 2;
      y = z.top + Math.max(4, (z.height - h) / 2);
      lado = "nenhuma";
    } else if (a.onde === "junto") {
      // Encostado: na coluna lateral, acima do controle (ou abaixo, se não couber), dentro da coluna; no topo, logo
      // abaixo; na página (o cartão do Mural), acima dele, sem subir sobre o cabeçalho.
      const cx = r.left + r.width / 2;
      let acima;
      if (col) {
        const c = col.getBoundingClientRect();
        x = Math.max(c.left + 6, Math.min(c.right - w - 6, cx - w / 2));
        acima = r.top - PERTO - h >= Math.max(c.top, 8);
        if (a.prefere === "baixo" && r.bottom + PERTO + h <= Math.min(c.bottom, vh - 8)) acima = false;
      } else {
        x = cx - w / 2;
        const pg = a.el.closest("#pagina"), p = pg && pg.getBoundingClientRect();
        // Na página: acima do controle, dentro dela; senão abaixo, se couber nela; senão acima mesmo (sobre o cenário),
        // nunca descendo sobre o Voltar e a doca.
        acima = p ? r.top - PERTO - h >= p.top || !(r.bottom + PERTO + h <= p.bottom) && r.top - PERTO - h >= 8
          : r.bottom + PERTO + h > vh - 8;
      }
      y = acima ? r.top - PERTO - h : r.bottom + PERTO;
      lado = acima ? "cima" : "baixo";
      const pg = !col && a.prefere === "esquerda" && a.el.closest("#pagina");
      if (pg && r.left - PERTO - w >= pg.getBoundingClientRect().left + 8) {
        // Largo até onde o céu deixa: menos linhas, e o quadro não desce sobre os nomes da comitiva.
        quadro.style.width = quadro.style.maxWidth = Math.min(420, r.left - PERTO - pg.getBoundingClientRect().left - 8) + "px";
        w = quadro.offsetWidth; h = quadro.offsetHeight;
        x = r.left - PERTO - w; y = r.top; lado = "esquerda";  // a seta sai da borda direita
      }
      // Do topo da janela (o botão Texto), o quadro desce sem cobrir as barras e os números do herói: vai para o lado
      // delas, se a seta ainda alcança o controle.
      const hud = !col && !a.el.closest("#hud") && document.querySelector("#hud");
      if (hud) {
        const u = hud.getBoundingClientRect(), cobre = (v) => v < u.right && v + w > u.left && y < u.bottom && y + h > u.top;
        const livre = vw - 8 - (u.right + 6);  // à direita delas, estreitando o quadro se preciso
        if (cobre(x) && livre >= 200 && cx >= u.right + 18) {
          quadro.style.width = Math.min(w, livre) + "px";
          w = quadro.offsetWidth; h = quadro.offsetHeight;
          x = u.right + 6;
        }
      }
    } else if (a.onde === "achado") {
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
    } else if (zona && a.haste) {
      // O ícone de efeito numa carta: o quadro na faixa (ou acima das cartas), alinhado a ele, e uma haste da seta até
      // ele (a carta anda e treme; o quadro não). Com a janelinha de Habilidades aberta sobre a faixa, o quadro vai
      // para o lado dela que ainda deixa o ícone ao alcance da seta; sem lado assim, ele espera a janelinha fechar.
      const cx = r.left + r.width / 2, zr = zona.left + zona.width;
      x = Math.max(zona.left + 4, Math.min(zr - w - 4, cx - w / 2));
      const jan = a.aoLado && a.aoLado.getBoundingClientRect();
      if (jan && jan.bottom > zona.top && x < jan.right + PERTO && x + w > jan.left - PERTO) {
        x = [jan.left - PERTO - w, jan.right + PERTO].find((v) => v >= zona.left && v + w <= zr && cx >= v + 12 && cx <= v + w - 12);
        if (x === undefined) return false;
      }
      y = zona.top + Math.max(4, (zona.height - h) / 2);
      lado = zona.top >= r.bottom ? "baixo" : "cima";
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
    quadro.className = `${tipo} seta-${lado}`;
    anel.classList.toggle("sobre-janela", a.onde === "achado");
    const seta = !r ? 0 : lado === "direita" || lado === "esquerda" ? Math.max(10, Math.min(h - 10, r.top + r.height / 2 - y))
      : Math.max(12, Math.min(w - 12, r.left + r.width / 2 - x));
    quadro.style.setProperty("--seta", seta + "px");
    quadro.style.left = Math.round(x) + "px";
    quadro.style.top = Math.round(y) + "px";
    if (a.haste) { haste.dataset.x = Math.round(x + seta); haste.dataset.lado = lado; esticarHaste(a.el); }
    return true;
  }
  /** A haste vai da ponta da seta (6px fora do quadro) até a borda do ícone, e acompanha o ícone quando a carta
   *  cresce ou treme (o quadro fica parado). */
  function esticarHaste(e) {
    const r = parteVisivel(e), q = quadro.getBoundingClientRect(), baixo = haste.dataset.lado === "baixo";
    const de = baixo ? r.bottom + 1 : q.bottom + 6, ate = baixo ? q.top - 6 : r.top - 1;
    haste.hidden = ate - de <= 2;
    Object.assign(haste.style, { left: haste.dataset.x - 1 + "px", top: Math.round(de) + "px", height: Math.max(0, Math.round(ate - de)) + "px" });
  }

  /** O contorno acompanha o controle (ele pode se mexer: o anel é dele, o quadro não). Um controle por vez. */
  function destacar(e) {
    controle = e;
    if (!anel) return;
    if (!e) { anel.hidden = true; return; }
    const r = parteVisivel(e), cs = getComputedStyle(e);
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
    if (!emLuta) {
      luta = null; animando = false;
      if (alMostrado && !fechados.has("AL")) alMostrado = false;  // a luta acabou com ele à vista: volta na próxima
      if (faixaDe === "luta") soltarFaixa();
    }
    if (e && e.orientacao && e.orientacao.ligado) dispensado = false;
    const agora = e && e.orientacao && e.orientacao.atual;
    const ap = (e && e.orientacao && e.orientacao.apresentacao) || {};
    const ctx = ((e && e.orientacao && e.orientacao.contextuais) || []).map((c) => c.id);
    fechados.forEach((id) => { if ((!agora || agora.id !== id) && !(id in ap) && !ctx.includes(id)) fechados.delete(id); });  // o motor já confirmou
    if (!$("#sobre-ajuda").hidden) desenharAjuda();
  }

  /** O golpe do herói (Batalha.lance "acao"): usada uma habilidade, o C4 vem na próxima vez em que se pode agir. */
  function aoLance(m) {
    if (luta && !luta.feito && m.tipo === "acao" && m.de === "j" && m.hab && m.hab !== "ataque") luta.c4 = m.hab;
    if (m.tipo === "acao" && m.de !== "j") animando = true;  // a vez dos outros: a animação que um clique acelera
  }

  /** Uma resposta da pessoa: com o C4 à vista, agir também o fecha (Entendi não é obrigatório). */
  function aoResponder() {
    if (luta && luta.c4 && passo.startsWith("C4")) luta.feito = true;
    if (alMostrado) passou("AL");
    if (a0Ativo && passo.startsWith("A0")) passou("A0");
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
