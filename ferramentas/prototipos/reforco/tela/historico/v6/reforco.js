/* Protótipo do reforço, 6ª versão (roadmapIDEIAS/25, 5.6): a A · Bancada com o reforço com chance, a informação
   reorganizada e o desfecho com presença. A forja (painel "forja_proto", demo.py) e a seção "Materiais" do inventário.
   Só esta demonstração carrega este arquivo; o jogo não. As versões anteriores ficam em historico/.

   A ordem de leitura segue Soul Knight Prequel e MapleStory M: os saldos no cabeçalho; na bancada, os materiais (ícone
   e quantidade), a peça com o nível (+1 → +2), o visor com o ganho (Ataque 4 → 5); no pé, a chance numa linha e a
   ação. O que a falha faz, o custo da tentativa e a permanência do atributo escolhido ficam na ajuda (ⓘ), por mouse e
   teclado. A tentativa é resolvida uma vez pelo motor; a tela encena: os condutos e o molde aquecem (1 s), e no
   impacto o desfecho ocupa a região da peça, com o efeito em pixel das celebrações (FX, o mesmo do Estouro): no
   sucesso, o selo, o clarão, o anel e os estilhaços, "SUCESSO" e o +N; na falha, o calor que se desfaz e as cinzas,
   "FALHOU" e o nível que ficou. Depois de um instante (ou de um clique), a bancada volta para a próxima oferta. */
"use strict";

(() => {
  ACOES_OCULTAS.push("forja");  // o pedido à forja não vira botão na página (nucleo.js)
  const { h, S, dicaItem, iconeItem, cartaoServico, topoBalcao } = Telas;
  const IMPACTO = 1050;   // do clique ao desfecho (o aquecimento)
  const SEGURA = 1700;    // o desfecho à vista antes de a bancada voltar para a próxima oferta

  let janela = null;       // "reforcar", "desmontar" ou null (o balcão)
  let aba = "heroi";       // de quem são as peças na esteira
  let selUid = null;       // a peça escolhida (sobrevive ao redesenho da forja)
  const veioSel = {};      // a arma do Guerreiro sem veio: o caminho escolhido antes do primeiro reforço
  let confirmando = null;  // {uid, nome}: a desmontagem pedida, esperando a confirmação
  let enviando = false;
  let focoDepois = null;   // o seletor que recebe o foco quando a forja volta desenhada
  let mostrarId = 0;       // o resultado (forja_ultimo.id) que a placa mostra; 0: nenhum
  let cena = null;         // {id, t0, fim, pago}: a cena do último resultado (o aquecimento e o desfecho)
  let pago = null;         // {ouro, fragmentos}: o custo da tentativa pedida (a cena mostra este, não o da próxima)
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

  /** A fase da cena: "forja" (aquecendo), "desfecho" (o resultado em destaque) ou "" (a bancada com a próxima oferta).
   *  Com movimento reduzido, não há aquecimento: o desfecho aparece parado. */
  function fase() {
    if (!cena || cena.fim) return "";
    const e = performance.now() - cena.t0;
    if (reduzido()) return e < SEGURA ? "desfecho" : "";
    return e < IMPACTO ? "forja" : e < IMPACTO + SEGURA ? "desfecho" : "";
  }

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
      if (d.ultimo.tipo === "reforco") cena = { id: d.ultimo.id, t0: performance.now(), fim: false, pago };
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
  function molde(p, extra = "", topo = "") {
    const faiscas = Array.from({ length: 8 }, (_, i) => `<i class="rf-fagulha f${i}"></i>`).join("");
    const cinzas = Array.from({ length: 4 }, (_, i) => `<i class="rf-cinza c${i}"></i>`).join("");
    return `<div class="rf-molde">${topo}<span class="rf-garra e" aria-hidden="true"></span>
      <div class="rf-berco"><span class="rf-barra t"></span><span class="rf-barra r"></span><span class="rf-barra b"></span><span class="rf-barra l"></span>
        <div class="rf-encaixe grande${p ? ` r-${h(p.item.raridade)}` : " vazio"}">${p ? iconePeca(p.item) : ""}</div>
        <span class="rf-faiscas" aria-hidden="true">${faiscas}${cinzas}</span></div>
      <span class="rf-garra d" aria-hidden="true"></span>${extra}</div>`;
  }
  const conduto = (seta) => `<span class="rf-conduto${seta ? " seta" : ""}" aria-hidden="true"><i class="rf-canal"></i></span>`;
  function chapaVazia() {
    return `<div class="rf-chapa vazia"><div class="rf-leito so">${molde(null)}</div><p class="rf-instrucao">Escolha uma peça</p></div>`;
  }
  /** Um material: o ícone e a quantidade exigida. O nome e quanto o grupo tem ficam na dica (mouse e teclado); faltando,
   *  o encaixe e o número ficam vermelhos. */
  function insumo(ic, nome, custo, tem) {
    const dica = Telas.dica(`<b>${h(nome)}</b><div>Custo ${custo} · Tem ${tem}</div>`, true);
    return `<div class="rf-insumo${tem < custo ? " falta" : ""}" tabindex="0" ${dica} aria-label="${h(nome)}: custo ${custo}, tem ${tem}">
      <span class="rf-encaixe pequeno">${ic}</span><b>${custo}</b></div>`;
  }
  const linhaGanho = (l) => `<div class="rf-ganho"><span>${h(l.nome)}</span><b>${l.antes} → <em>${l.depois}</em></b></div>`;
  /** A ajuda (ⓘ): o que a tela não mostra mas pesa na decisão, curto. Mouse e teclado. */
  function ajuda(linhas) {
    if (!linhas.length) return "";
    return `<button type="button" class="rf-ajuda" aria-label="Detalhes" ${Telas.dica(`<ul class="dica-lista">${linhas.map((l) => `<li>${h(l)}</li>`).join("")}</ul>`, true)}>i</button>`;
  }
  /** O desfecho: a palavra centrada sobre a peça (no lugar do nível), o +N e o ganho à direita dela. */
  function desfecho(u) {
    if (!u) return ["", ""];
    const palavra = `<div class="rf-dsf palavra ${u.sucesso ? "ok" : "mau"}"><b>${u.sucesso ? "Sucesso" : "Falhou"}</b></div>`;
    const ganho = u.linhas.map((l) => `<span>${h(l.nome)} ${l.antes} → ${l.depois}</span>`).join("");
    const numero = `<div class="rf-dsf numero ${u.sucesso ? "ok" : "mau"}"><b>+${u.para}</b>${ganho ? `<small>${ganho}</small>` : ""}</div>`;
    return [palavra, numero];
  }
  function chapaReforco(p, u) {
    const passo = passoDe(p);
    const meu = u && u.uid === p.uid && u.tipo === "reforco" && cena && cena.id === u.id ? u : null;
    const f = meu ? fase() : "";
    const classeCena = f === "forja" ? ` forjando ${meu.sucesso ? "ok" : "falhou"}` : f === "desfecho" ? ` forjando desfecho ${meu.sucesso ? "ok" : "falhou"}` : "";
    const [palavra, numero] = desfecho(meu);
    if (p.no_limite) {
      return `<div class="rf-chapa${classeCena}"><div class="rf-leito so"><div class="rf-lado esq"></div>
        ${molde(p, marcas(p), `<span class="rf-nivel">Reforço máximo +${p.limite}</span>${palavra}`)}<div class="rf-lado dir">${numero}</div></div></div>`;
    }
    if (p.sem_reforco) {
      return `<div class="rf-chapa"><div class="rf-leito so">${molde(p)}</div><p class="rf-instrucao">${h(p.sem_reforco)}</p></div>`;
    }
    const custo = passo || p.passos[0];  // o custo e a chance são os mesmos nos dois caminhos
    // durante a cena, os encaixes mostram o que esta tentativa consumiu (o motor já calculou a próxima)
    const mostra = f && meu && cena.pago ? { ...custo, ouro: cena.pago.ouro, fragmentos: cena.pago.fragmentos, ouro_tem: Infinity, tem: Infinity } : custo;
    const materiais = `<div class="rf-insumos" aria-label="Custo">${insumo(moeda(), "Ouro", mostra.ouro, mostra.ouro_tem)}${insumo(iconeDe("saco"), "Fragmento de Têmpera", mostra.fragmentos, mostra.tem)}</div>`;
    const escolha = p.passos.length > 1;
    const visor = escolha
      ? `<div class="rf-resultado veios" role="radiogroup" aria-label="Atributo que a arma reforça">${p.passos.map((x) => `<button type="button" role="radio" class="rf-veio${veioSel[p.uid] === x.veio ? " escolhido" : ""}" data-veio="${x.veio}" aria-checked="${veioSel[p.uid] === x.veio}">
          ${x.linhas.map(linhaGanho).join("")}</button>`).join("")}</div>`
      : `<div class="rf-resultado">${passo.linhas.map(linhaGanho).join("")}</div>`;
    const ajudas = [];
    if (custo.chance < 100) ajudas.push(`Se falhar: +${p.reforco} → +${custo.falha}. O equipamento não quebra.`);
    ajudas.push("A tentativa custa o mesmo, dê certo ou não.");
    if (escolha) ajudas.push("O atributo escolhido fica com a arma, mesmo se ela voltar a +0.");
    const motivo = !passo ? "Escolha o atributo" : passo.motivo;
    const chance = custo.chance >= 100 ? `<span class="rf-chance">Sucesso garantido</span>` : `<span class="rf-chance">Sucesso <b>${custo.chance}%</b></span>`;
    return `<div class="rf-chapa${classeCena}">
      <div class="rf-leito"><div class="rf-lado esq">${materiais}</div>${conduto(false)}
        ${molde(p, marcas(p), `<span class="rf-nivel">+${p.reforco} → +${p.reforco + 1}</span>${palavra}`)}${conduto(true)}<div class="rf-lado dir">${visor}${numero}</div></div>
      <div class="rf-pe-chapa"><div class="rf-linha-chance">${chance}${ajuda(ajudas)}</div>
        <button type="button" class="rf-botao principal" data-reforcar${motivo ? ` aria-disabled="true" title="${h(motivo)}"` : ""}>Reforçar</button>
        ${passo && passo.motivo ? `<span class="rf-falta">${h(passo.motivo)}</span>` : ""}</div></div>`;
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
    // durante a cena, o nome mostra o nível de antes da tentativa (o motor já trocou o +N; a tela ainda não conta)
    const antes = tocou.size ? `<span class="rf-nome-antes">${h(p.item.nome.replace(/ \+\d+$/, "") + (u.de ? ` +${u.de}` : ""))}</span>` : "";
    return `<div class="rf-ficha-cab"><b class="r-${h(p.item.raridade)}"><span class="rf-nome-agora">${h(p.item.nome)}</span>${antes}</b><small>${h(dono(p))}</small></div>
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
  let relogios = [], ctl = null, palco = null;
  const limparRelogios = () => { relogios.forEach(clearTimeout); relogios = []; };
  function pararFx() { if (ctl) ctl.parar(); ctl = null; if (palco) palco.el.remove(); palco = null; }

  /** A bancada treme alguns quadros (o FX.tremer sacode a página inteira; aqui, só a chapa do impacto). Por left/top,
   *  não por translate: um translate faria da chapa um contexto de empilhamento, e a peça e o "SUCESSO" passariam para
   *  baixo do efeito enquanto ela treme. */
  function tremerChapa(chapa, px) {
    if (reduzido()) return;
    [1, -0.8, 0.6, -0.45, 0.3, -0.15, 0].forEach((f, i) => relogios.push(setTimeout(() => {
      chapa.style.left = f ? `${Math.round(px * f)}px` : "";
      chapa.style.top = f ? `${Math.round(px * f * -0.5)}px` : "";
    }, i * FX.QUADRO)));
  }

  /** O efeito do desfecho, em pixel (FX das celebrações), recortado no leito (a área funda da peça e do resultado; o
   *  resto da janela fica parado e legível): no sucesso, o selo de raios atrás do molde, o halo, um anel curto e os
   *  estilhaços (mais fortes no +3 e no +4, com a chapa tremendo); na falha, um anel fraco que apaga e cinzas caindo. A
   *  peça fica por cima do efeito. `desde`: quanto do desfecho já passou (um redesenho no meio). */
  function efeito(jan, u, desde = 0) {
    pararFx();
    if (typeof FX === "undefined") return;
    const leito = jan.querySelector(".rf-chapa .rf-leito"), alvo = jan.querySelector(".rf-chapa .rf-encaixe.grande");
    if (!leito || !alvo) return;
    palco = FX.palco(jan, { z: 2, classe: "rf-fx" });
    const r = leito.getBoundingClientRect();
    palco.el.style.clipPath = `inset(${r.top}px ${innerWidth - r.right}px ${innerHeight - r.bottom}px ${r.left}px)`;
    const enx = FX.enxame(), forte = u.sucesso && u.para >= 3;
    const pal = forte ? FX.PALETAS.lendario : ["W", "Y", "O", "o", "C"];
    if (u.sucesso && forte && !desde) tremerChapa(leito.closest(".rf-chapa"), 3);
    ctl = FX.animar(palco, (t, q, parado) => {
      const a = palco.de(alvo), R = Math.max(a.rx, a.ry);
      if (u.sucesso) {
        const re = R + palco.t(forte ? 46 : 34);
        const vis = parado ? 12 : Math.round(FX.rampa(t, 500, 700, 16, 11));
        FX.raios(palco, { cx: a.x, cy: a.y, n: 18, ang: 0.15 + (parado ? 0 : q * 0.012), larg: 0.32, r0: R, r1: Math.round(re * (forte ? 2.1 : 1.8)), pal: pal.slice(1), esbate: 0.35, achata: 0.8, vis });
        FX.estrela(palco, { cx: a.x, cy: a.y, pontas: 14, ri: R + 2, re, pal, cores: ["z", "o", "O", "Y"] });
        if (parado) return;
        // o clarão só em volta da peça (sem o pontilhado na área inteira) e um anel que não passa muito do selo
        FX.claraoLocal(palco, { cx: a.x, cy: a.y, r: re, t, dur: forte ? 200 : 160, espalha: 0 });
        if (t < 420) FX.anel(palco, { cx: a.x, cy: a.y, r: re + Math.round(FX.rampa(t, 0, 400) * palco.t(forte ? 70 : 50)), esp: 2, pal: ["W", pal[1], pal[2]], achata: 0.8, rastro: 3, vis: Math.round(14 * (1 - t / 420)) });
        if (q === 1) enx.soltar(forte ? 34 : 20, (i) => {
          const ang = FX.aleatorio(0, Math.PI * 2), v = FX.aleatorio(2.5, 6) * (forte ? 1.1 : 0.85);
          return { x: a.x + Math.cos(ang) * re * 0.8, y: a.y + Math.sin(ang) * re * 0.7, vx: Math.cos(ang) * v, vy: Math.sin(ang) * v - 2, g: 0.36, arrasto: 0.97,
            vida: Math.round(FX.aleatorio(16, 28)), desenho: ["lasca", "caco", "cruz", "duplo"][i % 4], pal: ["W", "Y", "O", "o", "r"], piscar: i % 5 === 0 };
        });
        if (q > 6 && q % 3 === 0) enx.soltar(1, () => ({ x: a.x + FX.aleatorio(-re, re), y: a.y + re * 0.6, vx: FX.aleatorio(-0.3, 0.3), vy: FX.aleatorio(-1.4, -0.7), vida: 16, desenho: "brasa", pal: ["Y", "O", "o", "r", "D"] }));
      } else {
        if (parado) { FX.poco(palco, { cx: a.x, cy: a.y, rx: R + palco.t(30), ry: R + palco.t(24), forca: 10 }); return; }
        const re = R + palco.t(20);
        if (t < 700) FX.anel(palco, { cx: a.x, cy: a.y, r: re + Math.round(FX.rampa(t, 0, 700) * palco.t(40)), esp: 2, pal: ["o", "r", "D"], achata: 0.8, rastro: 3, vis: Math.round(12 * (1 - t / 700)) });
        if (q === 1) enx.soltar(12, () => ({ x: a.x + FX.aleatorio(-re, re), y: a.y - re * 0.5, vx: FX.aleatorio(-0.4, 0.4), vy: FX.aleatorio(-0.6, 0.2), g: 0.12, arrasto: 0.95,
          vida: Math.round(FX.aleatorio(18, 30)), desenho: "brasa", pal: ["O", "o", "r", "G", "g"] }));
        if (q > 2 && q < 18 && q % 2 === 0) enx.soltar(2, () => ({ x: a.x + FX.aleatorio(-re, re), y: a.y + FX.aleatorio(-re * 0.4, re * 0.2), vx: FX.aleatorio(-0.2, 0.2), vy: FX.aleatorio(0.4, 1), g: 0.04, arrasto: 0.98,
          vida: Math.round(FX.aleatorio(18, 26)), desenho: Math.random() < 0.5 ? "ponto" : "duplo", pal: ["w", "G", "g", "d"] }));
      }
      enx.passo(); enx.desenhar(palco);
    });
    if (desde > 0 && ctl.pular) ctl.pular(desde);
  }

  /** O impacto: a chapa passa ao desfecho e o efeito começa. Só classes e o canvas; nada é pedido ao motor. */
  function entrarDesfecho(u) {
    const jan = document.querySelector(".rf-janela"), chapa = jan && jan.querySelector(".rf-chapa.forjando");
    if (!chapa) return;
    chapa.classList.add("desfecho");
    jan.classList.add("em-cena");
    efeito(jan, u, cena && !reduzido() ? Math.max(0, performance.now() - cena.t0 - IMPACTO) : 0);
  }
  /** Fim da cena: a bancada volta para a próxima oferta, a placa resume o resultado e o foco volta à ação. */
  function assentar() {
    limparRelogios();
    pararFx();
    const estava = cena && !cena.fim;
    if (cena) cena.fim = true;
    // a bancada é desenhada de novo com a próxima oferta (durante a cena, os encaixes mostravam o que foi pago)
    if (estava && ultimoRaiz && ultimoRaiz.isConnected && ultimoDesenho) {
      ultimoRaiz.replaceWith(Telas.painel({ tipo: "forja_proto", dados: ultimoDesenho }));
    }
    const jan = document.querySelector(".rf-janela");
    jan?.classList.remove("em-cena");
    if (jan && focoDepois && (document.activeElement === document.body || !jan.contains(document.activeElement))) {
      const alvo = primeiro(jan, focoDepois);
      if (alvo) alvo.focus();
    }
  }
  /** Um clique, Enter, Espaço ou Esc durante a cena: do aquecimento vai ao desfecho; do desfecho, à próxima oferta. */
  function adiantar(u) {
    const f = fase();
    if (f === "forja") { cena.t0 = performance.now() - IMPACTO; limparRelogios(); entrarDesfecho(u); relogios.push(setTimeout(assentar, SEGURA)); }
    else if (f === "desfecho") assentar();
  }
  const revelar = assentar;  // os gestos que interrompem (trocar de peça, fechar) assentam a cena

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

  let ultimoDesenho = null, ultimoRaiz = null;
  function ligar(raiz, d) {
    enviando = false;
    ultimoDesenho = d;
    ultimoRaiz = raiz;
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
    const u = d.ultimo;
    const f = cena && u && cena.id === u.id ? fase() : "";
    limparRelogios();
    pararFx();
    if (f) {
      jan.classList.add("em-cena");
      const e = performance.now() - cena.t0;
      if (f === "forja") {
        relogios.push(setTimeout(() => entrarDesfecho(u), IMPACTO - e));
        relogios.push(setTimeout(assentar, IMPACTO + SEGURA - e));
      } else {
        entrarDesfecho(u);
        relogios.push(setTimeout(assentar, (reduzido() ? SEGURA : IMPACTO + SEGURA) - e));
      }
    }
    // durante a cena, um clique na bancada só revela: não compra, não escolhe, não desmonta (Enter e Espaço, no
    // ouvinte do documento, lá embaixo). Fechar, trocar de serviço, de dono ou de peça continuam valendo (o motor já
    // resolveu a tentativa).
    jan.addEventListener("click", (ev) => {
      if (!fase() || ev.target.closest("[data-fechar], [data-janela], [data-aba], [data-uid]")) return;
      ev.preventDefault();
      ev.stopPropagation();
      adiantar(d.ultimo);
    }, true);
    jan.querySelector("[data-fechar]").addEventListener("click", fechar);
    // as dicas dos materiais e da ajuda também abrem pelo foco do teclado (o jogo só faz isso no mercado)
    jan.querySelectorAll(".rf-insumo, .rf-ajuda").forEach((el) => {
      el.addEventListener("focus", () => {
        if (!el.matches(":focus-visible")) return;
        el.dispatchEvent(new MouseEvent("mouseenter"));
        const caixa = document.getElementById("dica-item");
        if (caixa) caixa._foco = true;
      });
      el.addEventListener("blur", () => el.dispatchEvent(new MouseEvent("mouseleave")));
    });
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
      pago = { ouro: x.ouro, fragmentos: x.fragmentos };
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

  // Durante a cena, Enter e Espaço adiantam onde quer que esteja o foco (o pé da bancada fica oculto e o Reforçar,
  // que tinha o foco, o perde até a cena acabar); a repetição de quem segura a tecla não adianta nem compra.
  document.addEventListener("keydown", (ev) => {
    if ((ev.key !== "Enter" && ev.key !== " ") || !janela || !fase() || !document.querySelector(".rf-janela")) return;
    ev.preventDefault();
    ev.stopImmediatePropagation();
    if (!ev.repeat) adiantar(ultimoDesenho && ultimoDesenho.ultimo);
  }, true);

  // Esc com a janela aberta: revela a cena, cancela a confirmação, fecha a janela; só então o Voltar da forja.
  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape" || !janela || !document.querySelector(".rf-janela")) return;
    ev.preventDefault();
    ev.stopImmediatePropagation();
    if (fase()) { adiantar(ultimoDesenho && ultimoDesenho.ultimo); return; }
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
