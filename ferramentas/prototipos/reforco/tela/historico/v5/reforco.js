/* Protótipo do reforço, 5ª versão (roadmapIDEIAS/25, 5.6): a A · Bancada com o reforço com chance. A forja (painel
   "forja_proto", demo.py) e a seção "Materiais" do inventário. Só esta demonstração carrega este arquivo; o jogo não.
   As versões anteriores ficam em historico/ (a faixa da demonstração abre cada uma).

   A janela por serviço continua (Reforçar, Desmontar; sem rolar a página; ouro e Fragmentos no topo; Esc fecha). A
   bancada é uma chapa de ferro: os materiais à esquerda, a peça num molde no meio, o resultado à direita, ligados por
   condutos, e a ação no pé. Antes de pagar: a chance, o nível pretendido, o que a falha faz e o custo. O motor resolve
   a tentativa uma vez; a tela só a encena: os condutos aquecem, a luz percorre o molde, e então o sucesso fecha o
   contorno ou a falha apaga em trechos. Um clique durante a cena revela o resultado (sem comprar de novo); com
   movimento reduzido, o resultado aparece direto. O resultado fica numa placa de altura fixa acima da bancada. */
"use strict";

(() => {
  ACOES_OCULTAS.push("forja");  // o pedido à forja não vira botão na página (nucleo.js)
  const { h, S, dicaItem, iconeItem, cartaoServico, topoBalcao } = Telas;
  const CENA_MS = 1350;  // do clique à revelação (hipótese: 1,2–1,5 s)

  let janela = null;       // "reforcar", "desmontar" ou null (o balcão)
  let aba = "heroi";       // de quem são as peças na esteira
  let selUid = null;       // a peça escolhida (sobrevive ao redesenho da forja)
  const veioSel = {};      // a arma do Guerreiro sem veio: o caminho escolhido antes do primeiro reforço
  let confirmando = null;  // {uid, nome}: a desmontagem pedida, esperando a confirmação
  let enviando = false;
  let focoDepois = null;   // o seletor que recebe o foco quando a forja volta desenhada
  let mostrarId = 0;       // o resultado (forja_ultimo.id) que a placa mostra; 0: nenhum
  let animarId = 0;        // o resultado que ainda tem a cena para tocar
  let revelado = true;     // a cena do resultado de agora já terminou (ou foi adiantada)
  let testeProximo = null; // "sucesso" ou "falha": o caso de teste da faixa para a próxima tentativa (só uma)
  let esperandoId = 0;     // o id do resultado que o último pedido vai produzir (só ele acende a placa e a cena)
  let vistoId = 0;         // o último resultado já recebido

  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const iconeDe = (nome) => Icones.porDesenho(nome) || S(nome, 2);
  const moeda = () => Icones.moeda() || S("moeda", 1);
  const num = (v) => String(v).replace(".", ",");
  const iconePeca = (it) => Icones.equipamento(iconeItem(it)) || S(iconeItem(it), 2);
  const retrato = (a) => (a.retrato ? Icones.cabeca(a.retrato, 32) || S(a.retrato, 2) : iconeDe("saco"));
  const valor = (pr, v) => (pr.pct ? `${v}%` : `${v}`);
  const dono = (p) => (p.quem ? `Com ${p.onde}` : "Bolsa do grupo");
  const marcas = (p) => `<span class="rf-marcas" aria-label="Reforço +${p.reforco} de ${p.limite}">${Array.from({ length: p.limite }, (_, i) =>
    `<i class="${i < p.reforco ? "cheia" : ""}"></i>`).join("")}</span>`;
  const fragmentos = (n) => `<span class="rf-material">${iconeDe("saco")}<span>Fragmento de Têmpera <b>×${n}</b></span></span>`;

  /** O passo de agora: o do veio escolhido (a arma do Guerreiro sem veio pede a escolha) ou o único. */
  function passoDe(p) {
    if (!p.passos) return null;
    if (p.passos.length === 1) return p.passos[0];
    return p.passos.find((x) => x.veio === veioSel[p.uid]) || null;
  }

  // ------------------------------------------------------------------ o balcão
  /** Um resultado novo do motor (o do último pedido): a placa passa a mostrá-lo; a cena toca uma vez (sem ela com
   *  movimento reduzido). Lido no desenho, antes de montar a bancada. */
  function receber(d) {
    if (d.ultimo && d.ultimo.id > vistoId && d.ultimo.id === esperandoId) {
      vistoId = mostrarId = d.ultimo.id;  // recebido uma vez: limpar a placa não o traz de volta nem repete a cena
      if (d.ultimo.tipo === "reforco" && !reduzido()) { animarId = d.ultimo.id; revelado = false; }
    }
  }
  function balcao(d) {
    receber(d);
    const cartoes = [
      cartaoServico({ icone: "martelo", nome: "Reforçar", efeito: "Arma, peito e apoio", attrs: 'data-servico="reforcar"' }),
      cartaoServico({ icone: "saco", nome: "Desmontar", efeito: "Peças da bolsa → Fragmentos de Têmpera", attrs: 'data-servico="desmontar"' }),
    ];
    return `<div class="tela balcao-servico forja forja-proto">${topoBalcao("martelo", "O ferreiro", "Um homem sem dois dedos cospe na forja. \"Ouro primeiro.\"", d.ouro)}
      <div class="servicos rf-servicos">${cartoes.join("")}</div>${janela ? janelaHtml(d) : ""}</div>`;
  }

  // ------------------------------------------------------------------ a janela
  function janelaHtml(d) {
    const abas = [["reforcar", "Reforçar"], ["desmontar", "Desmontar"]].map(([id, nome]) =>
      `<button type="button" role="tab" class="rf-servico${id === janela ? " ativo" : ""}" data-janela="${id}" aria-selected="${id === janela}">${nome}</button>`).join("");
    const recursos = `<div class="rf-recursos"><span class="rf-rec" title="Ouro">${Icones.ouro() || S("moedas", 2)}<b>${d.ouro}</b></span>
      ${d.materiais.map((m) => `<span class="rf-rec" title="${h(m.nome)}">${iconeDe(m.icone)}<b>${m.qtd}</b><small>${h(m.plural)}</small></span>`).join("")}</div>`;
    return `<div class="rf-janela m-janela" role="dialog" aria-modal="true" aria-label="${janela === "reforcar" ? "Reforçar" : "Desmontar"}">
      <header class="rf-cab"><nav class="rf-servicos-abas" role="tablist">${abas}</nav>${recursos}
        <button type="button" class="rf-botao fechar" data-fechar>Fechar <kbd>Esc</kbd></button></header>${corpo(d)}</div>`;
  }

  /** Um encaixe da esteira: o ícone, o +N no canto e, ao desmontar, o material que rende (ícone e quantidade). */
  function encaixe(p) {
    const reforco = janela === "reforcar";
    const apagada = reforco ? !!p.sem_reforco : !!p.desmontar.motivo;
    const canto = reforco ? (p.reforco ? `<span class="rf-canto">+${p.reforco}</span>` : "")
      : (p.desmontar.motivo ? "" : `<span class="rf-canto mat">${Icones.porDesenho("saco", 16) || S("saco", 1)}×${p.desmontar.total}</span>`);
    return `<button type="button" class="rf-peca r-${h(p.item.raridade)}${p.uid === selUid ? " marcada" : ""}${apagada ? " apagada" : ""}" data-uid="${h(p.uid)}"
      aria-label="${h(p.item.nome)}" aria-pressed="${p.uid === selUid}" ${dicaItem(p.item, "", false)}>${iconePeca(p.item)}${canto}</button>`;
  }

  function corpo(d) {
    const reforco = janela === "reforcar";
    const lista = d.pecas.filter((p) => (reforco ? p.aba === aba : !p.quem));
    const p = lista.find((x) => x.uid === selUid);
    const donos = `<nav class="rf-donos" role="tablist" aria-label="De quem">${d.abas.filter((a) => reforco || a.id === "bolsa").map((a) => {
      const ativo = reforco ? a.id === aba : true;
      const n = d.pecas.filter((x) => (reforco ? x.aba === a.id : !x.quem)).length;
      return `<button type="button" role="tab" class="rf-dono${ativo ? " ativo" : ""}"${reforco ? ` data-aba="${h(a.id)}"` : ""} aria-selected="${ativo}" title="${h(a.nome)}">${retrato(a)}<span>${h(a.nome)}</span><small>${n}</small></button>`;
    }).join("")}</nav>`;
    const esteira = lista.map(encaixe).join("")
      || `<span class="rf-vazio-texto">${reforco ? "Nada aqui." : "Nenhuma peça da bolsa rende material."}</span>`;
    const u = d.ultimo && d.ultimo.id === mostrarId ? d.ultimo : null;
    const chapa = !p ? chapaVazia() : reforco ? chapaReforco(p, u) : chapaDesmonte(p);
    return `<div class="rf-corpo">${donos}<section class="rf-centro"><div class="rf-mesa">${placa(u, p)}${chapa}</div>
        <div class="rf-esteira" role="listbox" aria-label="Peças">${esteira}</div></section>
      <aside class="rf-ficha">${p ? ficha(p, u) : ""}</aside></div>`;
  }

  /** A placa do resultado: altura fixa acima da bancada (nada se desloca quando ela muda). Mostra o último resultado
   *  da peça escolhida (ou a desmontagem, com a seleção vazia) até a próxima ação. */
  function placa(u, p) {
    let txt = "";
    if (u && u.tipo === "reforco" && p && u.uid === p.uid) {
      const linhas = u.linhas.map((l) => `<span class="rf-placa-linha">${h(l.nome)} <b>${l.antes} → ${l.depois}</b></span>`).join("");
      txt = u.sucesso ? `<b class="rf-placa-titulo bom">Reforço bem-sucedido · +${u.para}</b>${linhas}`
        : `<b class="rf-placa-titulo mau">Reforço falhou · +${u.de} → +${u.para}</b>${linhas}`;
      if (u.teste) txt += `<span class="rf-selo">teste</span>`;
    } else if (u && u.tipo === "desmonte" && !p) {
      txt = `<b class="rf-placa-titulo">Desmontado</b>${fragmentos(u.total)}<span class="rf-placa-nome" title="${h(u.nome)}">${h(u.nome)}</span>`;
    }
    return `<div class="rf-placa${txt ? "" : " vazia"}" aria-live="polite">${txt}</div>`;
  }

  // ------------------------------------------------------------------ a chapa (a bancada)
  /** O molde da peça: o encaixe afundado num berço de ferro com garras dos lados, assentado na chapa. A luz da cena
   *  percorre as quatro barras do molde; as fagulhas e as cinzas nascem em volta dele. */
  function molde(p, extra = "") {
    const faiscas = Array.from({ length: 8 }, (_, i) => `<i class="rf-fagulha f${i}"></i>`).join("");
    const cinzas = Array.from({ length: 4 }, (_, i) => `<i class="rf-cinza c${i}"></i>`).join("");
    return `<div class="rf-molde"><span class="rf-garra e" aria-hidden="true"></span>
      <div class="rf-berco"><span class="rf-barra t"></span><span class="rf-barra r"></span><span class="rf-barra b"></span><span class="rf-barra l"></span>
        <div class="rf-encaixe grande${p ? ` r-${h(p.item.raridade)}` : " vazio"}">${p ? iconePeca(p.item) : ""}</div>
        <span class="rf-faiscas" aria-hidden="true">${faiscas}${cinzas}</span></div>
      <span class="rf-garra d" aria-hidden="true"></span>${extra}</div>`;
  }
  const conduto = (seta) => `<span class="rf-conduto${seta ? " seta" : ""}" aria-hidden="true"><i class="rf-canal"></i></span>`;
  function chapaVazia() {
    return `<div class="rf-chapa vazia"><div class="rf-leito so">${molde(null)}</div><p class="rf-instrucao">Escolha uma peça</p></div>`;
  }
  /** Um insumo: o ícone e, ao lado, o custo e o que o grupo tem, cada número com o seu rótulo. */
  function insumo(ic, nome, custo, tem) {
    return `<div class="rf-insumo${tem < custo ? " falta" : ""}" title="${h(nome)}"><span class="rf-encaixe pequeno">${ic}</span>
      <dl><div><dt>Custo</dt><dd>${custo}</dd></div><div><dt>Tem</dt><dd>${tem}</dd></div></dl></div>`;
  }
  const linhaGanho = (l) => `<div class="rf-ganho"><span>${h(l.nome)}</span><b>${l.antes} → <em>${l.depois}</em></b></div>`;
  function chapaReforco(p, u) {
    const passo = passoDe(p);
    const cena = u && u.uid === p.uid && u.tipo === "reforco" && animarId === u.id && !revelado;
    const classeCena = cena ? ` forjando ${u.sucesso ? "ok" : "falhou"} alvo${u.sucesso ? u.para : u.de + 1}` : "";
    if (p.no_limite) {
      return `<div class="rf-chapa${classeCena}"><div class="rf-oferta"><b class="rf-alvo">Reforço máximo +${p.limite}</b>${p.veio ? `<small>${h(p.veio)}</small>` : ""}</div>
        <div class="rf-leito so">${molde(p, marcas(p))}</div></div>`;
    }
    if (p.sem_reforco) {
      return `<div class="rf-chapa"><div class="rf-oferta"><span class="rf-instrucao">${h(p.sem_reforco)}</span></div>
        <div class="rf-leito so">${molde(p)}</div></div>`;
    }
    const custo = passo || p.passos[0];  // o custo e a chance são os mesmos nos dois caminhos
    const materiais = `<div class="rf-insumos" aria-label="Custo por tentativa">${insumo(moeda(), "Ouro", custo.ouro, custo.ouro_tem)}${insumo(iconeDe("saco"), "Fragmentos de Têmpera", custo.fragmentos, custo.tem)}</div>`;
    const resultado = p.passos.length > 1
      ? `<div class="rf-resultado veios"><div role="radiogroup" aria-label="Caminho da arma">${p.passos.map((x) => `<button type="button" role="radio" class="rf-veio${veioSel[p.uid] === x.veio ? " escolhido" : ""}" data-veio="${x.veio}" aria-checked="${veioSel[p.uid] === x.veio}">
          <span class="rf-veio-nome">${h(x.rotulo)}</span>${x.linhas.map(linhaGanho).join("")}<span class="rf-veio-attr">${x.linhas.map((l) => h(l.nome)).join(", ")}</span></button>`).join("")}</div>
          <small class="rf-nota-veio">O caminho fica com a peça.</small></div>`
      : `<div class="rf-resultado">${passo.linhas.map(linhaGanho).join("")}</div>`;
    const motivo = !passo ? "Escolha Fio ou Runas" : passo.motivo;
    const instrucao = !passo;  // uma instrução, não um erro: cor neutra
    const risco = custo.chance >= 100 ? `<span class="rf-chance">Sucesso garantido</span>`
      : `<span class="rf-chance">Sucesso: <b>${custo.chance}%</b></span><span class="rf-risco">Falha: +${p.reforco} → +${custo.falha}</span>`;
    return `<div class="rf-chapa${classeCena}">
      <div class="rf-oferta"><span class="rf-rot">Próxima tentativa</span><b class="rf-alvo">+${p.reforco} → +${p.reforco + 1}</b>${p.veio ? `<small>${h(p.veio)}</small>` : ""}${risco}</div>
      <div class="rf-leito">${materiais}${conduto(false)}${molde(p, marcas(p))}${conduto(true)}${resultado}</div>
      <div class="rf-pe-chapa"><button type="button" class="rf-botao principal" data-reforcar${motivo ? ` aria-disabled="true" title="${h(motivo)}"` : ""}>Reforçar</button>
        <span class="${motivo ? (instrucao ? "rf-instrucao" : "rf-falta") : "rf-nota-custo"}">${h(motivo || "Cada tentativa consome o custo.")}</span></div></div>`;
  }
  function chapaDesmonte(p) {
    const d = p.desmontar;
    const recebe = `<div class="rf-resultado recebe"><span class="rf-rot">Recebe</span>${fragmentos(d.total)}</div>`;
    const conf = confirmando && confirmando.uid === p.uid;
    const pe = conf
      ? `<div class="rf-confirmar" role="alertdialog" aria-label="Confirmar a desmontagem"><b>Desmontar ${h(p.item.nome)}?</b>
          <span class="rf-aviso">O equipamento será destruído.</span>
          <div class="rf-botoes"><button type="button" class="rf-botao" data-desmontar-nao>Cancelar</button>
          <button type="button" class="rf-botao perigo" data-desmontar-sim disabled>Desmontar</button></div></div>`
      : `<button type="button" class="rf-botao perigo" data-desmontar>Desmontar</button>`;
    return `<div class="rf-chapa"><div class="rf-oferta"><b class="rf-alvo">Desmontar</b></div>
      <div class="rf-leito">${molde(p)}${conduto(true)}${recebe}</div>
      <div class="rf-pe-chapa">${pe}</div></div>`;
  }

  // ------------------------------------------------------------------ a ficha
  /** Nome, dono e todas as propriedades; a que o próximo reforço muda vem destacada pelo valor (o "→" está na
   *  bancada). O Poder das Runas, que a peça ainda não tem, aparece como a linha que vai nascer, com 0. */
  function ficha(p, u) {
    const passo = janela === "reforcar" ? passoDe(p) : null;
    const muda = new Set((passo ? passo.linhas : []).map((l) => l.nome));
    const tocou = u && u.tipo === "reforco" && u.uid === p.uid ? new Set(u.linhas.map((l) => l.nome)) : new Set();
    const linhas = p.propriedades.map((pr) => `<li class="${muda.has(pr.nome) ? "muda" : ""}${tocou.has(pr.nome) ? " tocou" : ""}">
      <span>${h(pr.nome)}</span><b>${valor(pr, pr.valor)}</b></li>`);
    (passo ? passo.linhas : []).filter((l) => !p.propriedades.some((pr) => pr.nome === l.nome))
      .forEach((l) => linhas.push(`<li class="muda"><span>${h(l.nome)}</span><b>0</b></li>`));
    return `<div class="rf-ficha-cab"><b class="r-${h(p.item.raridade)}">${h(p.item.nome)}</b><small>${h(dono(p))}</small></div>
      <div class="rf-ficha-meio"><ul class="rf-props">${linhas.join("")}</ul>${p.efeito ? `<p class="rf-efeito">${h(p.efeito)}</p>` : ""}
        ${p.venda !== undefined ? `<div class="rf-venda">Venda: ${moeda()} ${p.venda}</div>` : ""}</div>${teste(p, passo)}`;
  }
  /** A comparação contra o alvo de teste e as substitutas: fechada, marcada "teste". */
  function teste(p, passo) {
    const linhas = (c, titulo) => (c && c.linhas.length ? `<div class="rf-teste-bloco"><small>${titulo}</small>${c.linhas.map((l) =>
      `<div class="rf-teste-linha"><span>${h(l.rotulo)}</span><b>${num(l.antes)} → <em class="${l.melhor ? "melhor" : "pior"}">${num(l.depois)}</em></b></div>`).join("")}</div>` : "");
    const blocos = [passo && linhas(passo.luta, "Se der certo"),
      ...(p.substitutas || []).map((s) => linhas(s, `No lugar: ${h(s.nome)}`)),
      ...(p.trocas || []).map((t) => linhas(t, `${h(t.quem)} veste${t.no_lugar ? ` no lugar de ${h(t.no_lugar)}` : ""}`))].filter(Boolean);
    if (!blocos.length) return "";
    const alvo = (passo && passo.luta) || (p.substitutas || [])[0] || (p.trocas || [])[0];
    return `<details class="rf-teste"><summary><span class="rf-selo">teste</span> Comparação · ${h(alvo.alvo)}</summary>
      <p class="rf-teste-nota">Dano médio, sem crítico.</p>${blocos.join("")}</details>`;
  }

  // ------------------------------------------------------------------ a cena do resultado
  let relogio = 0;
  /** Termina a cena: a chapa perde o "forjando" e a placa, a ficha e as marcas aparecem. Só mexe em classes: nada é
   *  redesenhado nem pedido de novo ao motor. */
  function revelar() {
    clearTimeout(relogio);
    revelado = true;
    document.querySelectorAll(".rf-chapa.forjando").forEach((c) => c.classList.remove("forjando"));
    const jan = document.querySelector(".rf-janela");
    jan?.classList.remove("em-cena");
    // o pé da bancada estava oculto na cena (e um botão oculto não recebe o foco): o foco pedido vem agora
    if (jan && focoDepois && (document.activeElement === document.body || !jan.contains(document.activeElement))) {
      const alvo = primeiro(jan, focoDepois);
      if (alvo) alvo.focus();
    }
  }

  // ------------------------------------------------------------------ ligar
  function pedir(dados, botao, foco) {
    if (enviando) return false;
    if (!App.acao({ forja: true }, dados.op === "reforcar" ? "predio_ferreiro" : null, dados)) {
      aviso("Agora não dá para pedir à forja.", "info", "pergaminho");
      return false;
    }
    enviando = true;
    focoDepois = foco || null;
    if (botao) botao.disabled = true;
    return true;
  }

  /** A janela ocupa a coluna do meio (a cena e a página), por cima do balcão. */
  function posicionar() {
    const jan = document.querySelector(".rf-janela");
    const cena = document.getElementById("cena");
    if (!jan || !cena) return;
    const r = cena.getBoundingClientRect();
    Object.assign(jan.style, { left: `${r.left + 8}px`, top: `${r.top + 8}px`, width: `${r.width - 16}px`, height: `${r.height - 16}px` });
  }
  window.addEventListener("resize", posicionar);
  const primeiro = (raiz, foco) => foco && foco.split(",").map((x) => raiz.querySelector(x.trim())).find(Boolean);

  function ligar(raiz, d) {
    enviando = false;
    const redesenhar = (foco) => {
      if (!raiz.isConnected) return;
      const novo = Telas.painel({ tipo: "forja_proto", dados: d });
      raiz.replaceWith(novo);
      const alvo = primeiro(novo, foco);
      if (alvo) alvo.focus();
    };
    const limpar = () => { revelar(); mostrarId = 0; focoDepois = null; };  // a próxima ação tira o resultado da placa
    const abrir = (qual, foco) => { janela = qual; selUid = null; confirmando = null; limpar(); redesenhar(foco || ".rf-janela .rf-peca, .rf-janela [data-fechar]"); };
    const fechar = () => { const era = janela; janela = null; confirmando = null; limpar(); redesenhar(`[data-servico="${era}"]`); };
    raiz.querySelectorAll("[data-servico]").forEach((b) => b.addEventListener("click", () => abrir(b.dataset.servico)));
    const jan = raiz.querySelector(".rf-janela");
    if (!jan) return;
    requestAnimationFrame(posicionar);
    posicionar();
    if (!revelado) {
      jan.classList.add("em-cena");
      clearTimeout(relogio);
      relogio = setTimeout(revelar, CENA_MS);
    }
    // durante a cena, um clique (ou Enter/Espaço) na bancada só revela: não compra, não escolhe, não desmonta.
    // Fechar, trocar de serviço, de dono ou de peça continuam valendo (o motor já resolveu a tentativa).
    jan.addEventListener("click", (ev) => {
      if (revelado || ev.target.closest("[data-fechar], [data-janela], [data-aba], [data-uid]")) return;
      ev.preventDefault();
      ev.stopPropagation();
      revelar();
    }, true);
    jan.addEventListener("keydown", (ev) => {
      if (!revelado && (ev.key === "Enter" || ev.key === " ")) { ev.preventDefault(); ev.stopPropagation(); revelar(); }
    }, true);
    jan.querySelector("[data-fechar]").addEventListener("click", fechar);
    jan.querySelectorAll("[data-janela]").forEach((b) => b.addEventListener("click", () => {
      if (b.dataset.janela !== janela) abrir(b.dataset.janela, `[data-janela="${b.dataset.janela}"]`);
    }));
    jan.querySelectorAll("[data-aba]").forEach((b) => b.addEventListener("click", () => {
      if (aba !== b.dataset.aba) { aba = b.dataset.aba; selUid = null; limpar(); redesenhar(`[data-aba="${b.dataset.aba}"]`); }
    }));
    jan.querySelectorAll("[data-uid]").forEach((b) => b.addEventListener("click", () => {
      if (selUid !== b.dataset.uid) { selUid = b.dataset.uid; confirmando = null; limpar(); redesenhar(`[data-uid="${b.dataset.uid}"]`); }
    }));
    jan.addEventListener("keydown", (ev) => {
      if (!["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"].includes(ev.key) || !ev.target.matches("[data-uid]")) return;
      const todas = [...jan.querySelectorAll("[data-uid]")];
      const i = todas.indexOf(ev.target);
      ev.preventDefault();
      todas[(i + (ev.key === "ArrowLeft" || ev.key === "ArrowUp" ? -1 : 1) + todas.length) % todas.length].focus();
    });
    const p = d.pecas.find((x) => x.uid === selUid);
    jan.querySelectorAll("[data-veio]").forEach((b) => b.addEventListener("click", () => {
      veioSel[p.uid] = b.dataset.veio;
      limpar();
      redesenhar(`[data-veio="${b.dataset.veio}"]`);
    }));
    const ref = jan.querySelector("[data-reforcar]");
    if (ref) ref.addEventListener("click", (ev) => {
      if (ev.detail > 1) return;  // o segundo clique de um duplo clique não compra outro passo
      if (ref.getAttribute("aria-disabled")) { App.recusar(ref, ref.title); return; }
      const x = passoDe(p);
      const pedido = `t${Date.now()}`;
      const teste = testeProximo;
      if (pedir({ op: "reforcar", uid: p.uid, pedido, ...(x.veio ? { veio: x.veio } : {}), ...(teste ? { teste } : {}) }, ref,
        "[data-reforcar]:not([aria-disabled]), [data-uid].marcada")) {
        esperandoId = (d.ultimo ? d.ultimo.id : 0) + 1;
        testeProximo = null;
        window.dispatchEvent(new Event("reforco-teste"));
      }
    });
    const des = jan.querySelector("[data-desmontar]");
    if (des) des.addEventListener("click", () => { confirmando = { uid: p.uid, nome: p.item.nome }; limpar(); redesenhar("[data-desmontar-nao]"); });
    const nao = jan.querySelector("[data-desmontar-nao]");
    if (nao) nao.addEventListener("click", () => { confirmando = null; redesenhar("[data-desmontar]"); });
    const sim = jan.querySelector("[data-desmontar-sim]");
    if (sim) {
      // a confirmação só arma depois de um instante: o clique que abriu a pergunta não a responde
      const arma = performance.now() + 400;
      setTimeout(() => { if (sim.isConnected) sim.disabled = false; }, 400);
      sim.addEventListener("click", (ev) => {
        if (sim.disabled || performance.now() < arma || ev.detail > 1 || !confirmando) return;
        const c = confirmando;
        confirmando = null;
        selUid = null;  // depois de desmontar, nada fica escolhido
        if (pedir({ op: "desmontar", uid: c.uid, nome: c.nome, confirmar: true }, sim, ".rf-janela .rf-peca, .rf-janela [data-fechar]")) {
          esperandoId = (d.ultimo ? d.ultimo.id : 0) + 1;
        }
      });
    }
    jan.addEventListener("keydown", (ev) => {
      if (ev.repeat && (ev.key === "Enter" || ev.key === " ")) ev.preventDefault();  // a tecla segurada não repete
    }, true);
    // o foco pedido volta a cada desenho (a volta do motor desenha a forja mais de uma vez) até a próxima ação
    if (focoDepois) {
      const alvo = primeiro(jan, focoDepois);
      if (alvo) { alvo.focus(); requestAnimationFrame(() => alvo.isConnected && document.activeElement === document.body && alvo.focus()); }
    }
    jan.addEventListener("pointerdown", () => { focoDepois = null; }, true);
    jan.addEventListener("keydown", (ev) => { if (ev.key === "Tab" || ev.key.startsWith("Arrow")) focoDepois = null; }, true);
  }

  // Tab e Shift+Tab ficam dentro da janela aberta (ela é um diálogo: a oficina atrás não recebe o foco)
  document.addEventListener("keydown", (ev) => {
    const jan = document.querySelector(".rf-janela");
    if (ev.key !== "Tab" || !janela || !jan) return;
    const focaveis = [...jan.querySelectorAll("button:not([disabled]), summary, [tabindex]:not([tabindex='-1'])")]
      .filter((el) => el.offsetParent !== null);
    if (!focaveis.length) return;
    const i = focaveis.indexOf(document.activeElement);
    ev.preventDefault();
    focaveis[i < 0 ? 0 : (i + (ev.shiftKey ? -1 : 1) + focaveis.length) % focaveis.length].focus();
  }, true);

  // Esc com a janela aberta: revela a cena, cancela a confirmação, fecha a janela; só então o Voltar da forja.
  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape" || !janela || !document.querySelector(".rf-janela")) return;
    ev.preventDefault();
    ev.stopImmediatePropagation();
    if (!revelado) { revelar(); return; }
    if (confirmando) { document.querySelector("[data-desmontar-nao]")?.click(); return; }
    document.querySelector(".rf-janela [data-fechar]")?.click();
  }, true);

  Telas.registrar("forja_proto", balcao, { ligar, esquecer: () => { janela = null; selUid = null; confirmando = null; revelar(); mostrarId = 0; aba = "heroi"; } });

  // a faixa da demonstração escolhe o caso de teste da próxima tentativa (carregar.js); vale uma vez
  window.ReforcoProto = {
    teste(modo) { if (modo !== undefined) testeProximo = modo || null; return testeProximo; },
  };

  /* A seção "Materiais" no inventário: as pilhas do grupo, fora dos espaços da bolsa. */
  function materiaisNoInventario() {
    const lado = document.querySelector(".tela.inventario .inv-lado");
    const mats = App.estado && App.estado.heroi && App.estado.heroi.materiais;
    if (!lado || !mats || lado.querySelector(".ref-mat-inv")) return;
    const bolsa = [...lado.querySelectorAll("h4")].find((x) => /^Bolsa$/.test(x.textContent.trim()));
    const slots = bolsa && bolsa.nextElementSibling;
    if (!slots) return;
    const html = `<h4>Materiais <small>não ocupam a bolsa</small></h4><div class="slots ref-mat-inv">${mats.map((m) =>
      `<div class="slot-px" tabindex="0" ${Telas.dica(`<b>${h(m.nome)}</b><div>${h(m.desc)}</div><div class="rodape">${h(m.fontes)}</div>`)}>${iconeDe(m.icone)}<span class="qtd">${m.qtd}</span></div>`).join("")}</div>`;
    slots.insertAdjacentHTML("afterend", html);
    Telas.ligarDicas(lado.querySelector(".ref-mat-inv"));
  }
  new MutationObserver(materiaisNoInventario).observe(document.body, { childList: true, subtree: true });
})();
