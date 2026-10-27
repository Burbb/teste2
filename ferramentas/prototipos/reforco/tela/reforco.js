/* Protótipo do reforço, 12ª versão (roadmapIDEIAS/25, 5.6 a 5.11): a A · Bancada com o reforço com chance, num eixo
   central e com as mesmas dimensões em todos os estados. A forja (painel "forja_proto", demo.py) e a seção "Materiais"
   do inventário. Só esta demonstração carrega este arquivo; o jogo não. As versões anteriores ficam em historico/.

   A bancada é a tela da tentativa: a peça no molde, os materiais à esquerda e o ganho à direita (colunas de largura
   igual), a chance e o Reforçar no eixo; o aquecimento corre nos condutos. A tentativa é resolvida uma vez pelo motor;
   a tela encena com os dados da tentativa (o nível, a chance, o custo pago, o ganho), para nada contar o resultado nem a
   próxima oferta antes da hora. Na revelação, o resultado sai da bancada para uma apresentação própria (a linguagem do
   achado): o véu na tela inteira, o nome com o nível novo, a peça com os efeitos, as propriedades, "SUCESSO" ou
   "FALHOU" e o OK. A gravação (encantamento) usa a mesma apresentação. O acabamento do reforço (do +1 ao +12) segue a
   peça em todas as telas. */
"use strict";

(() => {
  ACOES_OCULTAS.push("forja");  // o pedido à forja não vira botão na página (nucleo.js)
  const { h, S, dicaItem, iconeItem, cartaoServico, topoBalcao } = Telas;
  const IMPACTO = 1050;   // do clique ao desfecho (o aquecimento)

  let janela = null;       // "reforcar", "desmontar" ou null (o balcão)
  let aba = "heroi";       // de quem são as peças na esteira
  let selUid = null;       // a peça escolhida (sobrevive ao redesenho da forja)
  let confirmando = null;  // {uid, nome}: a desmontagem pedida, esperando a confirmação
  let enviando = false;
  let focoDepois = null;   // o seletor que recebe o foco quando a forja volta desenhada
  let mostrarId = 0;       // o resultado (forja_ultimo.id) que a placa mostra; 0: nenhum
  let cena = null;         // {id, t0, fim, pago}: a cena do último resultado (o aquecimento e o desfecho)
  let pago = null;         // a tentativa pedida, como a oferta a mostrava: {de, chance, linhas, ouro, fragmentos}
  let brilharSel = false;  // a peça acabou de ser escolhida: o reflexo passa uma vez no molde
  let desmonte = null;     // {id, t0, icone, raridade}: a transformação da última desmontagem (a peça já saiu da bolsa)
  let pedidoDesmonte = null;  // {icone, raridade}: a peça que a desmontagem pedida vai transformar
  const DESMONTE_MS = 700;
  let essSel = null;          // a essência escolhida no trilho (fica entre as peças)
  let sulcoSel = 0, sulcoDe = null;  // o sulco escolhido (e de que peça: outra peça começa no primeiro vazio)
  let confirmandoGrav = null; // {uid}: a substituição pedida, esperando a confirmação
  let gravando = null;        // {id, t0, uid, de, para}: a cena da última gravação
  const GRAVA_TRACO = 900;  // a essência percorre a borda; depois o resultado em destaque, até o OK
  function faseGrav() {
    if (!gravando || gravando.fim) return "";
    if (reduzido()) return "gravado";
    return performance.now() - gravando.t0 < GRAVA_TRACO ? "traco" : "gravado";
  }
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
    if (reduzido()) return "desfecho";  // o resultado parado, com a mesma confirmação
    return performance.now() - cena.t0 < IMPACTO ? "forja" : "desfecho";  // o desfecho fica até OK, Enter ou Esc
  }

  /** O passo de agora (um só: a peça inteira melhora, sem caminho a escolher). */
  const passoDe = (p) => (p.passos ? p.passos[0] : null);

  // ------------------------------------------------------------------ o balcão
  /** Um resultado novo do motor (o do último pedido): a placa passa a mostrá-lo; a cena toca uma vez (sem ela com
   *  movimento reduzido). Lido no desenho, antes de montar a bancada. */
  function receber(d) {
    if (d.ultimo && d.ultimo.id > vistoId && d.ultimo.id === esperandoId) {
      vistoId = mostrarId = d.ultimo.id;  // recebido uma vez: limpar a placa não o traz de volta nem repete a cena
      if (d.ultimo.tipo === "reforco") cena = { id: d.ultimo.id, t0: performance.now(), fim: false, pago };
      if (d.ultimo.tipo === "desmonte" && pedidoDesmonte) desmonte = { id: d.ultimo.id, t0: performance.now(), ...pedidoDesmonte };
      if (d.ultimo.tipo === "encanto") gravando = { id: d.ultimo.id, t0: performance.now(), uid: d.ultimo.uid, sulco: d.ultimo.sulco, de: d.ultimo.de, para: d.ultimo.para };
    }
  }
  function balcao(d) {
    receber(d);
    const cartoes = [
      cartaoServico({ icone: "martelo", nome: "Reforçar", efeito: "Arma, peito e apoio", attrs: 'data-servico="reforcar"' }),
      cartaoServico({ icone: "livro", nome: "Encantar", efeito: "Grava essências nos sulcos da peça (laboratório)", attrs: 'data-servico="encantar"' }),
      cartaoServico({ icone: "saco", nome: "Desmontar", efeito: "Peças da bolsa → Fragmentos de Têmpera", attrs: 'data-servico="desmontar"' }),
    ];
    return `<div class="tela balcao-servico forja forja-proto">${topoBalcao("martelo", "O ferreiro", "Um homem sem dois dedos cospe na forja. \"Ouro primeiro.\"", d.ouro)}
      <div class="servicos rf-servicos">${cartoes.join("")}</div>${janela ? janelaHtml(d) : ""}</div>`;
  }

  // ------------------------------------------------------------------ a janela
  function janelaHtml(d) {
    const abas = [["reforcar", "Reforçar"], ["encantar", "Encantar"], ["desmontar", "Desmontar"]].map(([id, nome]) =>
      `<button type="button" role="tab" class="rf-servico${id === janela ? " ativo" : ""}" data-janela="${id}" aria-selected="${id === janela}">${nome}</button>`).join("");
    const recursos = `<div class="rf-recursos"><span class="rf-rec" data-rec="ouro" title="Ouro">${Icones.ouro() || S("moedas", 2)}<b>${d.ouro}</b></span>
      ${d.materiais.filter((m) => (janela === "encantar") === m.id.startsWith("essencia_")).map((m) => `<span class="rf-rec${janela === "encantar" ? " ess" : ""}" data-rec="${h(m.id)}" ${Telas.dica(`<b>${h(m.plural)}</b><div>Tem ${m.qtd}</div>`, true)}>${iconeDe(m.icone)}<b>${m.qtd}</b>${janela === "encantar" ? "" : `<small>${h(m.plural)}</small>`}</span>`).join("")}</div>`;
    const rotulo = { reforcar: "Reforçar", desmontar: "Desmontar", encantar: "Encantar" }[janela];
    // a janela nasce no lugar da anterior: sem isso, num redesenho ela passa um quadro fora do lugar, e o segundo clique
    // de um clique duplo atravessava para o balcão atrás dela (o cartão Desmontar)
    const pos = ultimaPos ? ` style="left:${ultimaPos.left};top:${ultimaPos.top};width:${ultimaPos.width};height:${ultimaPos.height}"` : "";
    return `<div class="rf-janela m-janela${janela === "encantar" ? " rf-encantar" : ""}" role="dialog" aria-modal="true" aria-label="${rotulo}"${pos}>
      <header class="rf-cab"><nav class="rf-servicos-abas" role="tablist">${abas}</nav>${recursos}
        <button type="button" class="botao-janela rf-botao fechar" data-fechar>Fechar <kbd>Esc</kbd></button></header>${corpo(d)}</div>`;
  }

  /** A tentativa em cena desta peça (o resultado do motor), ou null. */
  const emCena = (p, u) => (u && u.tipo === "reforco" && u.uid === p.uid && cena && cena.id === u.id && fase() ? u : null);
  /** Um valor que muda com a tentativa: o de antes (no aquecimento) e o de agora (do desfecho em diante), trocados
   *  pela classe "aquecendo" da janela, sem redesenhar. */
  const antesAgora = (antes, agora) => `<span class="rf-v-antes">${antes}</span><span class="rf-v-agora">${agora}</span>`;

  /** Um encaixe da esteira: o ícone, o +N no canto e, ao desmontar, o material que rende (ícone e quantidade). */
  function encaixe(p, u) {
    const reforco = janela !== "desmontar";  // o +N no canto (o reforço e o encantamento são por dono)
    const apagada = janela === "reforcar" ? !!p.sem_reforco : janela === "encantar" ? !!p.encantar.motivo : !!p.desmontar.motivo;
    const t = reforco ? emCena(p, u) : null;
    let canto = "";
    if (t) canto = `<span class="rf-canto${t.de ? "" : " sem-antes"}${p.reforco ? "" : " sem-agora"}">${antesAgora(`+${t.de}`, `+${p.reforco}`)}</span>`;
    else if (reforco) canto = p.reforco ? `<span class="rf-canto">+${p.reforco}</span>` : "";
    else canto = p.desmontar.motivo ? "" : `<span class="rf-canto mat">${Icones.porDesenho("saco", 16) || S("saco", 1)}×${p.desmontar.total}</span>`;
    return `<button type="button" class="rf-peca r-${h(p.item.raridade)}${p.uid === selUid ? " marcada" : ""}${apagada ? " apagada" : ""}" data-uid="${h(p.uid)}"
      data-reforco="${reforco ? p.reforco : 0}" aria-label="${h(p.item.nome)}" aria-pressed="${p.uid === selUid}" ${t ? "" : dicaItem(p.item, "", false)}>${iconePeca(p.item)}${canto}${gravura(p.encantos)}</button>`;
  }

  /** A borda de luz da gravação: um trecho de luz na cor da essência percorre a borda própria do encaixe (por dentro,
   *  sem tocar a raridade, a seleção nem o foco). Só a existência da gravação: não há níveis de encantamento. */
  const gravura = (lista) => (lista || []).filter(Boolean).map((e, i, todas) =>
    `<i class="rf-gravura" aria-hidden="true" style="--ess:${h(e.cor)};animation-delay:-${(((performance.now() / 1000) + i * 4.2 / todas.length) % 4.2).toFixed(2)}s"></i>`).join("");

  /** Os sulcos de uma peça como encaixes quadrados, na quantidade real dela: o vazio escuro com contorno; o ocupado com
   *  o símbolo da essência. Com `sel` (a forja), cada um é um botão: escolher onde gravar. */
  function filaSulcos(lista, sel = null) {
    return (lista || []).map((x, i) => {
      const cor = x ? ` style="--ess:${h(x.cor)}"` : "";
      if (sel === null) return `<i class="rf-sq${x ? "" : " vazio"}"${cor} title="${x ? h(x.nome) : "Sulco vazio"}">${x ? iconeDe(x.icone) : ""}</i>`;
      return `<button type="button" role="radio" class="rf-sq${x ? "" : " vazio"}${i === sel ? " escolhido" : ""}" data-sulco="${i}" aria-checked="${i === sel}"
        aria-label="Sulco ${i + 1}: ${x ? h(x.nome) : "vazio"}"${cor} ${Telas.dica(x ? `<b>${h(x.nome)}</b><div>${h(x.efeito)}</div>${x.limite ? `<div class="rodape">${h(x.limite)}</div>` : ""}` : "<b>Sulco vazio</b>", true)}>${x ? iconeDe(x.icone) : ""}</button>`;
    }).join("");
  }
  /** A seção de encantamentos de uma ficha: os sulcos e, para cada gravação, o nome da essência como título e, embaixo,
   *  o efeito e o limite. Vazia quando a peça não aceita gravação. */
  function secaoEncantos(lista) {
    if (!Array.isArray(lista) || !lista.length) return "";
    const n = lista.length, k = lista.filter(Boolean).length;
    return `<div class="rf-encantos"><div class="rf-encantos-cab"><span>Sulcos</span><span class="rf-sq-fila" aria-label="${n} ${n > 1 ? "sulcos" : "sulco"}, ${k} ${k === 1 ? "gravado" : "gravados"}">${filaSulcos(lista)}</span></div>
      ${lista.filter(Boolean).map((e) => `<div class="rf-encanto" style="--ess:${h(e.cor)}"><b>${h(e.nome)}</b><p>${h(e.efeito)}</p>${e.limite ? `<p class="lim">${h(e.limite)}</p>` : ""}</div>`).join("")}</div>`;
  }

  function corpo(d) {
    const reforco = janela !== "desmontar";  // as abas de dono valem no reforço e no encantamento
    const lista = d.pecas.filter((p) => (reforco ? p.aba === aba : !p.quem));
    const p = lista.find((x) => x.uid === selUid);
    const donos = `<nav class="rf-donos" role="tablist" aria-label="De quem">${d.abas.filter((a) => reforco || a.id === "bolsa").map((a) => {
      const ativo = reforco ? a.id === aba : true;
      const n = d.pecas.filter((x) => (reforco ? x.aba === a.id : !x.quem)).length;
      return `<button type="button" role="tab" class="rf-dono${ativo ? " ativo" : ""}"${reforco ? ` data-aba="${h(a.id)}"` : ""} aria-selected="${ativo}" title="${h(a.nome)}">${retrato(a)}<span>${h(a.nome)}</span><small>${n}</small></button>`;
    }).join("")}</nav>`;
    const u = d.ultimo && d.ultimo.id === mostrarId ? d.ultimo : null;
    const esteira = lista.map((x) => encaixe(x, u)).join("")
      || `<span class="rf-vazio-texto">${reforco ? "Nada aqui." : "Nenhuma peça da bolsa rende material."}</span>`;
    const chapa = janela === "reforcar" ? chapaReforco(p, u) : janela === "encantar" ? chapaEncanto(p, u, d) : chapaDesmonte(p, u);
    // no reforço, o resultado é a cena na própria bancada; a placa fica só para a desmontagem
    const semFicha = janela === "reforcar";  // a ficha do reforço está na bancada (o título) e na dica da peça
    return `<div class="rf-corpo${semFicha ? " sem-ficha" : ""}">${donos}<section class="rf-centro"><div class="rf-mesa">${chapa}</div>
        <div class="rf-esteira" role="listbox" aria-label="Peças">${esteira}</div></section>
      ${semFicha ? "" : `<aside class="rf-ficha">${p ? ficha(p, u) : ""}</aside>`}</div>`;
  }

  // ------------------------------------------------------------------ a chapa (a bancada)
  /** O molde da peça: o encaixe afundado num berço de ferro com garras dos lados, assentado na chapa. A luz da cena
   *  percorre as quatro barras do molde; as fagulhas e as cinzas nascem em volta dele. */
  function molde(p, extra = "", topo = "", dicaPeca = true) {
    const faiscas = Array.from({ length: 8 }, (_, i) => `<i class="rf-fagulha f${i}"></i>`).join("");
    const cinzas = Array.from({ length: 4 }, (_, i) => `<i class="rf-cinza c${i}"></i>`).join("");
    return `<div class="rf-molde">${topo}<span class="rf-garra e" aria-hidden="true"></span>
      <div class="rf-berco"><span class="rf-barra t"></span><span class="rf-barra r"></span><span class="rf-barra b"></span><span class="rf-barra l"></span>
        <div class="rf-encaixe grande${p ? ` r-${h(p.item.raridade)}` : " vazio"}"${p ? ` data-reforco="${p.reforco || 0}" data-retirar data-peca="${h(p.uid)}" role="button" tabindex="0" aria-label="Retirar ${h(p.item.nome)} da bancada"${dicaPeca ? ` ${dicaItem(p.item, "", false)}` : ""}` : ""}>${p ? iconePeca(p.item) + gravura(p.encantos) : ""}</div>
        <span class="rf-faiscas" aria-hidden="true">${faiscas}${cinzas}</span></div>
      <span class="rf-garra d" aria-hidden="true"></span>${extra}</div>`;
  }
  const conduto = (seta) => `<span class="rf-conduto${seta ? " seta" : ""}" aria-hidden="true"><i class="rf-canal"></i></span>`;
  function chapaVazia() {
    return `<div class="rf-chapa vazia"><div class="rf-leito so">${molde(null)}</div><p class="rf-instrucao">Escolha uma peça</p></div>`;
  }
  /** Um material: o ícone e a quantidade exigida. O nome e quanto o grupo tem ficam na dica (mouse e teclado); faltando,
   *  o encaixe e o número ficam vermelhos. Sem `custo` (nada a pagar: reforço máximo, sem peça), só o encaixe apagado. */
  function insumo(ic, nome, custo, tem) {
    if (custo === undefined) return `<div class="rf-insumo vazio" aria-hidden="true"><span class="rf-encaixe pequeno">${ic}</span><b></b></div>`;
    const dica = Telas.dica(`<b>${h(nome)}</b><div>Custo ${custo} · Tem ${tem}</div>`, true);
    return `<div class="rf-insumo${tem < custo ? " falta" : ""}" tabindex="0" ${dica} aria-label="${h(nome)}: custo ${custo}, tem ${tem}">
      <span class="rf-encaixe pequeno">${ic}</span><b>${custo}</b></div>`;
  }
  const insumos = (ouro, ouroTem, frag, fragTem) => `<div class="rf-insumos" aria-label="Custo">${insumo(moeda(), "Ouro", ouro, ouroTem)}${insumo(iconeDe("saco"), "Fragmento de Têmpera", frag, fragTem)}</div>`;
  const linhaGanho = (l) => `<div class="rf-ganho"><span>${h(l.nome)}</span><b>${l.antes} → <em>${l.depois}</em></b></div>`;
  const visor = (linhas) => `<div class="rf-resultado${linhas.length ? "" : " vazio"}">${linhas.map(linhaGanho).join("")}</div>`;
  /** A ajuda (ⓘ): o que a tela não mostra mas pesa na decisão, curto. Mouse e teclado. Fica ao lado da chance, fora
   *  do eixo (a chance continua centrada). */
  function ajuda(linhas) {
    if (!linhas.length) return "";
    return `<button type="button" class="rf-ajuda" aria-label="Detalhes" ${Telas.dica(`<ul class="dica-lista">${linhas.map((l) => `<li>${h(l)}</li>`).join("")}</ul>`, true)}>i</button>`;
  }


  /** A bancada do reforço: a mesma estrutura em todos os estados (oferta, cena, falta, máximo, peça sem reforço, sem
   *  peça), para a peça e o Reforçar não mudarem de lugar. O nível, a peça, a chance e o botão no eixo do meio; os
   *  materiais e o ganho nas colunas dos lados, de largura igual. */
  /** O título da bancada: o nome da peça com o reforço, na cor da raridade; embaixo, o dono e os sulcos. Na cena, o
   *  número de antes (o novo entra na apresentação do resultado). */
  function tituloPeca(p, t) {
    if (!p) return `<div class="rf-titulo vazio"><b>&nbsp;</b><small>&nbsp;</small><div class="rf-tit-sulcos"></div></div>`;
    const nome = p.item.nome, m = / \+(\d+)/.exec(nome);
    const base = m ? nome.slice(0, m.index) : nome, resto = m ? nome.slice(m.index + m[0].length) : "";
    const n = t ? t.de : p.reforco;  // na cena, o nível de antes (o novo aparece na apresentação do resultado)
    const num = n ? `<span class="rf-n">+${n}</span>` : "";
    const sulcos = (p.encantos || []).length ? `<span>Sulcos</span><span class="rf-sq-fila">${filaSulcos(p.encantos)}</span>` : "";
    return `<div class="rf-titulo"><b class="r-${h(p.item.raridade)}">${h(base)} ${num}${h(resto)}</b><small>${h(dono(p))}</small><div class="rf-tit-sulcos">${sulcos}</div></div>`;
  }
  function bancada({ p, classe = "", nivel = "", marcasDe, esq, dir, dsf = "", chance = "", falha = "", ajudas = [], botao = "Reforçar", trava = "", nota = "", neutra = false, titulo = "", dicaPeca = true }) {
    const m = p ? marcas({ ...p, reforco: marcasDe ?? p.reforco }) : marcas({ reforco: 0, limite: 4 });
    return `<div class="rf-chapa${titulo ? " com-titulo" : ""}${classe}">${titulo || ""}
      <div class="rf-leito"><div class="rf-lado esq">${esq}${conduto(false)}</div>
        ${molde(p, m, nivel === null ? "" : `<span class="rf-nivel">${nivel}</span>`, dicaPeca)}
        <div class="rf-lado dir">${conduto(true)}${dir}${dsf}</div></div>
      <div class="rf-pe-chapa"><div class="rf-linha-chance">${chance}${ajuda(ajudas)}</div>${titulo ? `<span class="rf-falha">${falha}</span>` : ""}
        <div class="rf-acao"><button type="button" class="botao-janela rf-botao principal" data-reforcar${trava ? ` aria-disabled="true"${trava === true ? "" : ` title="${h(trava)}"`}` : ""}>${botao}</button></div>
        <span class="rf-nota${neutra ? " neutra" : ""}">${h(nota)}</span></div></div>`;
  }
  const semCusto = () => insumos();
  const chanceHtml = (c) => (c >= 100 ? `<span class="rf-chance">Sucesso garantido</span>` : `<span class="rf-chance">Sucesso <b>${c}%</b></span>`);

  function chapaReforco(p, u) {
    const comum = { nivel: null, titulo: tituloPeca(p, null) };
    if (!p) return bancada({ ...comum, p: null, esq: semCusto(), dir: visor([]), botao: "Reforçar", trava: "Escolha uma peça", nota: "Escolha uma peça", neutra: true });
    // a cena: tudo da tentativa, como a oferta mostrava antes do clique (o motor já resolveu e já calculou a próxima)
    const t = emCena(p, u);
    if (t) {
      const x = cena.pago || { de: t.de, chance: 0, linhas: [] };
      // a bancada da tentativa, como a oferta estava (o resultado aparece na apresentação em destaque, por cima)
      const classe = ` forjando ${t.sucesso ? "ok" : "falhou"}${t.sucesso && t.para >= 3 ? " forte" : ""}`;
      return bancada({ p, classe, nivel: null, titulo: tituloPeca(p, t), marcasDe: t.de, esq: insumos(x.ouro, Infinity, x.fragmentos, Infinity),
        dir: visor(x.linhas), chance: chanceHtml(x.chance), falha: x.chance >= 100 ? "" : `Falha: +${t.de} → +${Math.max(0, t.de - 1)}`,
        botao: `Reforçar +${t.de} → +${t.de + 1}`, trava: true, dicaPeca: false });
    }
    if (p.no_limite) {
      return bancada({ ...comum, p, esq: semCusto(), dir: visor([]), botao: "Reforço máximo", trava: true });
    }
    if (p.sem_reforco) {
      return bancada({ ...comum, p, esq: semCusto(), dir: visor([]), trava: true, nota: p.sem_reforco, neutra: true });
    }
    const passo = passoDe(p);
    const ajudas = ["O equipamento não quebra.", "A tentativa custa o mesmo, dê certo ou não."];  // a falha está à vista
    const motivo = passo.motivo;
    return bancada({ ...comum, p, esq: insumos(passo.ouro, passo.ouro_tem, passo.fragmentos, passo.tem), dir: visor(passo.linhas),
      chance: chanceHtml(passo.chance), falha: passo.chance >= 100 ? "" : `Falha: +${p.reforco} → +${passo.falha}`, ajudas,
      botao: `Reforçar +${p.reforco} → +${p.reforco + 1}`, trava: motivo || "", nota: motivo || "" });
  }
  /** A desmontagem na mesma bancada do reforço: a peça no molde, no eixo do botão; à direita, o encaixe do que ela
   *  rende (ícone e quantidade). O botão vira a confirmação no próprio pé, com o nome da peça e a destruição. Depois de
   *  desmontar, a transformação (DESMONTE_MS): a peça se desfaz em fragmentos de pixel e o material chega ao encaixe; a
   *  seleção fica vazia (nada é escolhido sozinho) e o encaixe do resultado mostra o que chegou até a próxima ação. */
  function chapaDesmonte(p, u) {
    const chegou = !p && u && u.tipo === "desmonte" ? u : null;
    const t = chegou && desmonte && desmonte.id === u.id && performance.now() - desmonte.t0 < DESMONTE_MS ? desmonte : null;
    const saco = iconeDe("saco");
    let n = null, motivo = "", pe;
    if (p) {
      n = p.desmontar.total;
      motivo = p.desmontar.motivo || "";
      const conf = confirmando && confirmando.uid === p.uid;
      pe = conf
        ? `<div class="rf-confirmar" role="alertdialog" aria-label="Confirmar a desmontagem"><b>Desmontar ${h(p.item.nome)}?</b>
            <span class="rf-aviso">O equipamento será destruído.</span>
            <div class="rf-botoes"><button type="button" class="botao-janela rf-botao" data-desmontar-nao>Cancelar</button>
            <button type="button" class="botao-janela rf-botao perigo" data-desmontar-sim disabled>Desmontar</button></div></div>`
        : `<div class="rf-linha-chance"></div><button type="button" class="botao-janela rf-botao principal perigo" data-desmontar${motivo ? ` aria-disabled="true" title="${h(motivo)}"` : ""}>Desmontar</button>
            <span class="rf-nota neutra">${h(motivo)}</span>`;
    } else {
      if (chegou) n = chegou.total;
      pe = `<div class="rf-linha-chance"></div><button type="button" class="botao-janela rf-botao principal perigo" aria-disabled="true" title="Escolha uma peça">Desmontar</button>
          <span class="rf-nota neutra">Escolha uma peça</span>`;
    }
    const resultado = `<div class="rf-recebe${n === null ? " vazio" : ""}${chegou ? " chegou" : ""}" ${n ? Telas.dica(`<b>Fragmento de Têmpera ×${n}</b>`, true) : ""}
        aria-label="${n ? `Recebe ${n} Fragmento${n > 1 ? "s" : ""} de Têmpera` : "Nada a receber"}"><span class="rf-encaixe pequeno">${saco}</span><b>${n === null ? "" : `×${n}`}</b></div>`;
    // a peça desmontada, guardada no clique, fica no molde só durante a transformação
    const fantasma = t ? `<div class="rf-encaixe grande r-${h(t.raridade)} rf-desfaz">${t.icone}</div>` : "";
    const nivel = '<span class="rf-nivel"></span>';  // a linha do nível, vazia: a bancada tem a altura da do reforço
    const vazio = marcas({ reforco: 0, limite: 4 }).replace('class="rf-marcas"', 'class="rf-marcas" style="visibility:hidden"');
    const m = p ? molde(p, marcas(p), nivel)
      : (fantasma ? molde(null, vazio, nivel).replace('<div class="rf-encaixe grande vazio"></div>', fantasma) : molde(null, vazio, nivel));
    return `<div class="rf-chapa desmonte${t ? " transformando" : ""}">
      <div class="rf-leito"><div class="rf-lado esq"></div>${m}
        <div class="rf-lado dir">${conduto(true)}${resultado}</div></div>
      <div class="rf-pe-chapa">${pe}</div></div>`;
  }


  // ------------------------------------------------------------------ a bancada do encantamento (laboratório)
  /** Gravar uma essência: a mesma chapa, outra operação. À esquerda, a essência escolhida e o ouro (o que se gasta); a
   *  peça no molde, com a gravação atual em cima ("Sem gravação" ou o nome); à direita, a essência que entra. Embaixo
   *  do leito, o trilho das essências (escolher é clicar numa) e a regra dela, curta; no pé, Gravar ou Substituir. A
   *  substituição pede a confirmação no próprio pé, dizendo o que se perde. A gravação nunca falha: a cena só mostra a
   *  essência entrando na borda da peça. */
  function chapaEncanto(p, u, d) {
    const g = gravando && p && gravando.uid === p.uid && faseGrav() ? gravando : null;
    const ess = p ? p.encantar.essencias : [];
    const e = ess.find((x) => x.id === essSel) || null;
    const sulcos = p ? p.encantos || [] : [];
    if (p && (sulcoDe !== p.uid || sulcoSel >= sulcos.length)) {  // outra peça: o primeiro sulco vazio (ou o primeiro)
      sulcoDe = p.uid;
      sulcoSel = Math.max(0, sulcos.findIndex((x) => !x));
    }
    const atual = p ? sulcos[sulcoSel] : null;
    const custo = d.custo_encanto;
    const motivoPeca = p ? p.encantar.motivo : "Escolha uma peça";
    const motivo = motivoPeca || (!e ? "Escolha uma essência" : e.motivo || (e.qtd < 1 ? `Falta 1 Essência de ${e.nome}` : null)
      || (d.ouro < custo ? `Faltam ${custo - d.ouro} de ouro` : null));
    const insumosHtml = e && !motivoPeca
      ? `<div class="rf-insumos" aria-label="Custo">${insumo(iconeDe(e.icone), `Essência de ${e.nome}`, 1, g ? Infinity : e.qtd)}${insumo(moeda(), "Ouro", custo, g ? Infinity : d.ouro)}</div>`
      : insumos();
    // à direita, o encaixe da essência que entra (o símbolo; o nome e a regra ficam no bloco embaixo, uma vez só)
    const visorHtml = `<div class="rf-recebe rf-ess-entra${e && !motivoPeca ? "" : " vazio"}"${e ? ` style="--ess:${h(e.cor)}"` : ""}><span class="rf-encaixe pequeno">${e && !motivoPeca ? iconeDe(e.icone) : ""}</span></div>`;
    const trilho = `<div class="rf-essencias" role="radiogroup" aria-label="Essência">${ess.map((x) => `<button type="button" role="radio" class="rf-essencia${x.id === essSel ? " escolhida" : ""}${x.motivo || x.qtd < 1 ? " apagada" : ""}${atual && atual.id === x.id ? " gravada" : ""}"
        data-essencia="${h(x.id)}" aria-checked="${x.id === essSel}" style="--ess:${h(x.cor)}" ${Telas.dica(`<b>${h(x.nome)} <span class="rf-qtd">×${x.qtd}</span></b><div>${h(x.efeito)}</div>${x.limite ? `<div class="rodape">${h(x.limite)}</div>` : ""}<div class="rf-compat">${h(x.compativel)}</div>${x.motivo ? `<div class="pior">${h(x.motivo)}</div>` : ""}`, true)}
        aria-label="${h(x.nome)} ×${x.qtd}">${iconeDe(x.icone)}<span class="rf-canto">${x.qtd}</span></button>`).join("")}</div>`;
    // a regra da essência escolhida: um bloco de largura controlada, à esquerda: o nome, o efeito, o limite
    const regra = `<div class="rf-ess-regra">${e && p ? `<b style="--ess:${h(e.cor)}">${h(e.nome)}</b><p>${h(e.efeito)}</p>${e.limite ? `<p class="lim">${h(e.limite)}</p>` : ""}` : ""}</div>`;
    const conf = confirmandoGrav && p && confirmandoGrav.uid === p.uid;
    let pe;
    if (conf) {
      pe = `<div class="rf-confirmar" role="alertdialog" aria-label="Confirmar a substituição"><span class="rf-troca">Sai <b style="color:${h(atual.cor)}">${h(atual.nome)}</b> · Entra <b style="color:${h(e.cor)}">${h(e.nome)}</b></span>
          <span class="rf-aviso">${h(atual.nome)} se perde.</span>
          <div class="rf-botoes"><button type="button" class="botao-janela rf-botao" data-gravar-nao>Cancelar</button>
          <button type="button" class="botao-janela rf-botao principal" data-gravar-sim disabled>Substituir</button></div></div>`;
    } else {
      const troca = atual && e && !motivo ? `<span class="rf-chance">Substitui <b style="color:${h(atual.cor)}">${h(atual.nome)}</b></span>` : "";
      pe = `<div class="rf-linha-chance">${troca}</div>
        <button type="button" class="botao-janela rf-botao principal" data-gravar${motivo || g ? ` aria-disabled="true"${motivo ? ` title="${h(motivo)}"` : ""}` : ""}>${atual ? "Substituir" : "Gravar"}</button>
        <span class="rf-nota${!motivo || /^Falta/.test(motivo) ? "" : " neutra"}">${h(motivo && p ? motivo : !p ? "Escolha uma peça" : "")}</span>`;
    }
    const nome = `<div class="rf-nivel rf-sulcos" role="radiogroup" aria-label="Sulcos">${filaSulcos(sulcos, sulcoSel)}</div>`;
    if (g) sulcoSel = gravando.sulco ?? sulcoSel;
    const classe = g ? ` gravando${faseGrav() === "gravado" ? " gravado" : ""}` : "";
    return `<div class="rf-chapa encanto${classe}"${g ? ` style="--ess:${h(g.para.cor)}"` : e ? ` style="--ess:${h(e.cor)}"` : ""}>
      <div class="rf-leito"><div class="rf-lado esq">${insumosHtml}${conduto(false)}</div>
        ${molde(p, p ? marcas(p) : marcas({ reforco: 0, limite: 4 }), nome)}
        <div class="rf-lado dir">${conduto(true)}${visorHtml}</div></div>
      ${trilho}${regra}
      <div class="rf-pe-chapa">${pe}</div></div>`;
  }

  // ------------------------------------------------------------------ a ficha
  /** Nome, dono e as propriedades, cada valor junto do nome. Durante o aquecimento, o nome e os valores de antes da
   *  tentativa (o motor já trocou; a tela ainda não conta); no desfecho, os novos, e a propriedade que mudou acende um
   *  instante. A que o próximo reforço muda tem o valor num nicho de latão. */
  function ficha(p, u) {
    const t = janela === "reforcar" ? emCena(p, u) : null;
    const passo = janela === "reforcar" && !t ? passoDe(p) : null;
    const muda = new Set((t ? (cena.pago && cena.pago.linhas) || [] : passo ? passo.linhas : []).map((l) => l.nome));
    const antes = new Map(t ? t.linhas.map((l) => [l.nome, l.antes]) : []);
    const linhas = p.propriedades.map((pr) => `<li class="${muda.has(pr.nome) ? "muda" : ""}${antes.has(pr.nome) ? " tocou" : ""}">
      <span>${h(pr.nome)}</span><b>${antes.has(pr.nome) ? antesAgora(valor(pr, antes.get(pr.nome)), valor(pr, pr.valor)) : valor(pr, pr.valor)}</b></li>`);
    (passo ? passo.linhas : []).filter((l) => !p.propriedades.some((pr) => pr.nome === l.nome))
      .forEach((l) => linhas.push(`<li class="muda"><span>${h(l.nome)}</span><b>0</b></li>`));
    const nome = t ? antesAgora(h(p.item.nome.replace(/ \+\d+$/, "") + (t.de ? ` +${t.de}` : "")), h(p.item.nome)) : h(p.item.nome);
    return `<div class="rf-ficha-cab"><b class="r-${h(p.item.raridade)}">${nome}</b><small>${h(dono(p))}</small></div>
      <ul class="rf-props">${linhas.join("")}</ul>${p.efeito ? `<p class="rf-efeito">${h(p.efeito)}</p>` : ""}
      ${secaoEncantos(p.encantos)}
      ${p.venda !== undefined ? `<div class="rf-venda">Venda: ${moeda()} ${p.venda}</div>` : ""}`;
  }
  /** A comparação contra o alvo de teste e as substitutas: um controle de laboratório, mostrado pela faixa da
   *  demonstração (carregar.js), fora da tela do jogador. */
  function teste(p, passo) {
    const linhas = (c, titulo) => (c && c.linhas.length ? `<div class="rf-teste-bloco"><small>${titulo}</small>${c.linhas.map((l) =>
      `<div class="rf-teste-linha"><span>${h(l.rotulo)}</span><b>${num(l.antes)} → <em class="${l.melhor ? "melhor" : "pior"}">${num(l.depois)}</em></b></div>`).join("")}</div>` : "");
    const blocos = [passo && linhas(passo.luta, "Se der certo"),
      ...(p.substitutas || []).map((s) => linhas(s, `No lugar: ${h(s.nome)}`)),
      ...(p.trocas || []).map((t) => linhas(t, `${h(t.quem)} veste${t.no_lugar ? ` no lugar de ${h(t.no_lugar)}` : ""}`))].filter(Boolean);
    if (!blocos.length) return "";
    const alvo = (passo && passo.luta) || (p.substitutas || [])[0] || (p.trocas || [])[0];
    return `<div class="rf-teste"><b>${h(p.item.nome)} · ${h(alvo.alvo)}</b>
      <p class="rf-teste-nota">Dano médio, sem crítico.</p>${blocos.join("")}</div>`;
  }

  // ------------------------------------------------------------------ a cena do resultado
  let relogios = [], ctl = null, palco = null;
  const limparRelogios = () => { relogios.forEach(clearTimeout); relogios = []; };
  function pararFx() { if (ctl) ctl.parar(); ctl = null; if (palco) palco.el.remove(); palco = null; }

  /** Um golpe seco na bancada: só a chapa, só na vertical, um deslocamento por quadro (`passos`, em px). Por top, não
   *  por translate: um translate faria da chapa um contexto de empilhamento, e a peça e o resultado passariam para
   *  baixo do efeito. A desmontagem: um toque (o reforço treme a tela na apresentação do resultado, nos marcos altos). */
  const BAQUE = { desmonte: [2, 0] };
  // Num relógio próprio: o redesenho da forja (limparRelogios) não corta o golpe no meio, e cada passo vale para a
  // chapa que estiver na tela. Um golpe novo cancela o anterior; sem `passos`, a chapa volta ao lugar na hora.
  let baqueRel = [];
  const impactados = new Set();  // os resultados que já tiveram o impacto (um por resultado, mesmo adiantado)
  function baque(passos) {
    baqueRel.forEach(clearTimeout);
    baqueRel = [];
    const pos = (y) => { const c = document.querySelector(".rf-janela .rf-chapa"); if (c) c.style.top = y ? `${y}px` : ""; };
    if (reduzido() || !passos) { pos(0); return; }
    passos.forEach((y, i) => baqueRel.push(setTimeout(() => pos(y), i * FX.QUADRO)));
  }
  /** Os sons do jogo (Som, sintetizados; respeitam o som desligado): o martelo na bigorna no reforço, o golpe junto no
   *  +3 e no +4, o golpe leve na falha, os estalos de metal na desmontagem. */
  function soar(...nomes) { if (typeof Som !== "undefined") nomes.forEach((n) => Som.tocar(n)); }

  // ------------------------------------------------------------------ o resultado em destaque (12ª versão)
  /* Na revelação, o resultado sai da bancada e ganha uma apresentação própria, na linguagem do achado: um véu na tela
     inteira (a mesma força do véu do achado) e, por cima, o nome com o nível no alto, a peça com o acabamento e os efeitos
     à esquerda, as propriedades à direita, o resultado grande embaixo e o OK. A bancada fica atrás, escurecida e sem
     interação; OK, Enter ou Esc a devolvem, com a próxima oferta. O mesmo molde serve à gravação (encantamento). */
  let res = null;  // {id, el, ctl, palco}: a apresentação aberta
  let calmaAte = 0;  // logo depois de dispensar, o resto do gesto (o 2º clique, o Espaço que solta) não chega à bancada
  /** A faixa de intensidade do nível alcançado: 0 (+1, +2), 1 (+3, +4), 2 (+5 a +8), 3 (+9 a +11), 4 (+12). */
  const faixaNivel = (n) => (n >= 12 ? 4 : n >= 9 ? 3 : n >= 5 ? 2 : n >= 3 ? 1 : 0);
  // as cores do efeito pelo nível: o ouro até o +4 (já aprovado); do +5 ao +8, a cor do nível (a mesma do acabamento);
  // do +9, o prisma (os raios em várias cores, mais cores a cada nível)
  const COR_NIVEL = {
    5: ["W", "#c8fff4", "#46e2cc", "#1f9a8c", "#0e4a46"], 6: ["W", "#c8dcff", "#5a8cff", "#2a4cc0", "#14205a"],
    7: ["W", "#ecd2ff", "#b064ff", "#6a2cb0", "#2c1050"], 8: ["W", "#ffd0d8", "#ff3c60", "#a8102e", "#4a0614"],
  };
  const PRISMA = ["#ff3c60", "#ffb032", "#46e2a0", "#468cff", "#aa64ff", "#ff6edc"];
  const paletaNivel = (n) => (n >= 9 ? ["W", "#fff4c8", "#ffb032", "#ff3c60", "#5a1030"] : COR_NIVEL[n] || (n >= 3 ? FX.PALETAS.lendario : ["W", "Y", "O", "o", "C"]));

  /** As propriedades da peça, como a ficha do achado: as que mudaram com antes → depois (o novo em verde; na queda,
   *  em vermelho), as outras secundárias, sem seta. */
  function linhasRes(p, mudou, perde) {
    const muda = new Map((mudou || []).map((l) => [l.nome, l]));
    const linha = (nome, b, classe = "") => `<div class="rf-res-linha${classe}"><span>${h(nome)}</span><b>${b}</b></div>`;
    const html = p.propriedades.map((pr) => {
      const l = muda.get(pr.nome);
      return l ? linha(pr.nome, `${h(String(l.antes))} → <em>${h(String(l.depois))}</em>`, perde ? " muda perde" : " muda") : linha(pr.nome, valor(pr, pr.valor));
    });
    (mudou || []).filter((l) => !p.propriedades.some((pr) => pr.nome === l.nome))
      .forEach((l) => html.push(linha(l.nome, `${h(String(l.antes))} → <em>${h(String(l.depois))}</em>`, perde ? " muda perde" : " muda")));
    return html.join("");
  }
  /** Os sulcos da peça: os encaixes e o nome de cada gravação, na cor dela (o efeito inteiro fica na dica). `nova`: o
   *  sulco que acabou de receber a gravação (em destaque); `saiu`: a gravação substituída. */
  function sulcosRes(lista, nova = -1, saiu = null) {
    if (!Array.isArray(lista) || !lista.length) return "";
    const nomes = lista.map((e, i) => e ? `<span class="rf-res-grav${i === nova ? " nova" : ""}" style="--ess:${h(e.cor)}">${i === nova ? `${iconeDe(e.icone)}` : ""}${h(e.nome)}</span>` : "").filter(Boolean);
    return `<div class="rf-res-sulcos"><div class="rf-res-sulcos-cab"><span class="rf-res-rotulo">Sulcos</span><span class="rf-sq-fila">${lista.map((x, i) => filaSulcos([x]).replace('class="rf-sq', `class="rf-sq${i === nova ? " nova" : ""}`)).join("")}</span></div>
      ${nomes.length ? `<div class="rf-res-gravs">${nomes.join("")}</div>` : ""}${saiu ? `<div class="rf-res-saiu">Saiu <b style="color:${h(saiu.cor)}">${h(saiu.nome)}</b></div>` : ""}</div>`;
  }
  /** O nome com o nível: o de antes some e o novo entra como marca quente (sucesso) ou sóbria (falha). */
  function nomeRes(p, t) {
    const nome = p.item.nome, m = / \+(\d+)/.exec(nome);
    const base = m ? nome.slice(0, m.index) : nome, resto = m ? nome.slice(m.index + m[0].length) : "";
    const num = t ? `<span class="rf-n"><span class="rf-n-antes">${t.de ? `+${t.de}` : ""}</span><span class="rf-n-agora ${t.sucesso ? "rf-quente" : "rf-sobrio"}">${p.reforco ? `+${p.reforco}` : ""}</span></span>`
      : p.reforco ? `<span class="rf-n">+${p.reforco}</span>` : "";
    return `<b class="rf-res-nome r-${h(p.item.raridade)}">${h(base)} ${num}${h(resto)}</b>`;
  }
  const rotuloPeca = (p) => `<span class="rf-res-rotulo">${h(Telas.nomeEspaco(p.item.slot, p.item.classe) || "")} · ${h(dono(p))}</span>`;

  /** O relógio dos efeitos da apresentação: 30 quadros por segundo (o FX das celebrações roda a 15; com a apresentação
   *  parada na tela, o giro contínuo dos raios a 15 parecia lento perto do resto do jogo). Os raios, anéis e clarões
   *  seguem o tempo a cada quadro; as partículas e o que nasce num quadro marcado (`passo`) continuam no compasso de 15
   *  do FX, para a física e as contagens serem as mesmas. */
  const QUADRO_RES = 1000 / 30;
  function animarRes(p, desenhar) {
    let fim = false, t0 = performance.now(), n = -1, q = -1;
    const um = (t) => {
      const nq = Math.floor(t / FX.QUADRO), passo = nq !== q;
      q = nq;
      p.limpar(); desenhar(t, q, false, passo); p.mostrar();
    };
    if (reduzido()) { p.limpar(); desenhar(1500, 0, true, false); p.mostrar(); return { parar() { fim = true; }, pular() {} }; }
    const laco = (agora) => {
      if (fim || !p.el.isConnected) return;
      const k = Math.floor((agora - t0) / QUADRO_RES);
      if (k !== n) { n = k; um(k * QUADRO_RES); }
      requestAnimationFrame(laco);
    };
    um(0); n = 0;
    requestAnimationFrame(laco);
    return { parar() { fim = true; }, pular(ms) { const ja = performance.now() - t0; if (ja < ms) t0 = performance.now() - ms; } };
  }

  /** Abre a apresentação (uma por resultado: um redesenho da forja não a repete nem recomeça o efeito). */
  function abrirRes({ id, classe, aria, titulo, arte, ficha, banner, nivel, fx }) {
    if (res && res.id === id && res.el.isConnected) return res;
    fecharRes();
    const el = document.createElement("div");
    el.id = "rf-res";
    el.className = `rf-res ${classe}`;
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-modal", "true");
    el.setAttribute("aria-label", aria);
    el.innerHTML = `<div class="rf-res-conj"><header class="rf-res-tit">${titulo}</header>
      <div class="rf-res-meio"><div class="rf-res-peca">${arte}</div><div class="rf-res-ficha">${ficha}</div></div>
      <div class="rf-res-pe">${banner}<button type="button" class="botao-janela rf-botao principal" data-res-ok>OK <kbd>Enter</kbd></button></div></div>`;
    document.body.appendChild(el);
    // a peça em pixel inteiro: o conjunto centrado pode cair em meio pixel, e a peça ampliada sairia borrada
    const conj = el.querySelector(".rf-res-conj"), r = el.querySelector(".rf-res-arte").getBoundingClientRect();
    conj.style.translate = `${Math.round(r.left) - r.left}px ${Math.round(r.top) - r.top}px`;
    document.body.classList.add("rf-res-aberto");  // o nome e a peça da bancada saem do fundo (não aparecem duas vezes)
    res = { id, el, ctl: null, palco: null };
    const caixa = el.querySelector(".rf-res-arte");
    acabamento(caixa, nivel);  // o acabamento do nível novo já na revelação
    if (nivel) relogios.push(setTimeout(() => reflexo(caixa, nivel, true), reduzido() ? 0 : 280));
    // nada passa para trás: um clique fora do OK não faz nada; o 2º clique de um clique duplo no OK não chega à bancada
    el.addEventListener("click", (ev) => {
      ev.stopPropagation();
      if (ev.target.closest("[data-res-ok]") && ev.detail <= 1) dispensarRes();
    });
    el.addEventListener("pointerdown", (ev) => ev.stopPropagation());
    el.querySelector("[data-res-ok]").focus({ preventScroll: true });
    if (fx && typeof FX !== "undefined") {
      res.palco = FX.palco(el, { z: 0, classe: "rf-fx" });
      res.ctl = fx(res.palco, el);
    }
    return res;
  }
  function fecharRes() {
    if (!res) return;
    if (res.ctl) res.ctl.parar();
    res.el.remove();
    res = null;
    document.body.classList.remove("rf-res-aberto");
  }
  /** OK, Enter ou Esc: a apresentação sai e a bancada volta (o reforço ou a gravação). */
  function dispensarRes() {
    if (fase() === "desfecho") dispensar();
    else if (faseGrav() === "gravado") dispensarGrav();
    else fecharRes();
  }

  /** O efeito do resultado do reforço, no palco da apresentação: no sucesso, o selo de raios atrás da peça, o clarão,
   *  os anéis e os estilhaços, mais fortes e mais coloridos nos marcos (+3, +5, +9, +12) sem durar mais; depois do
   *  impacto, os raios acomodam numa intensidade que deixa ler e continuam girando até o OK. Na falha, um anel fraco que
   *  apaga, cinzas e o esfriar, sem dourado. */
  function efeitoReforco(u, desde) {
    return (palco, el) => {
      const alvo = el.querySelector(".rf-res-arte"), ficha = el.querySelector(".rf-res-ficha"), numero = el.querySelector(".rf-res-nome .rf-n-agora");
      const f = faixaNivel(u.para), pal = paletaNivel(u.para), enx = FX.enxame();
      const cores = u.para >= 9 ? PRISMA.slice(0, u.para >= 12 ? 6 : u.para - 7) : null;
      const estrelaCores = u.para >= 9 ? ["z", "#5a1030", "#ffb032", "#fff4c8"] : u.para >= 5 ? ["z", pal[4], pal[2], pal[1]] : ["z", "o", "O", "Y"];
      if (!impactados.has(u.id) && desde < 400) {
        impactados.add(u.id);
        if (u.sucesso) { soar("predio_ferreiro", ...(f >= 1 ? ["golpe"] : [])); if (f >= 1) FX.tremer([0, 3, 4, 6, 9][f]); }
        else soar("golpe_leve");
      }
      const ctl = animarRes(palco, (t, q, parado, passo) => {
        const a = palco.de(alvo), R = Math.max(a.rx, a.ry);
        if (ficha) { const g = palco.de(ficha); FX.poco(palco, { cx: g.x, cy: g.y, rx: g.rx + palco.t(26), ry: g.ry + palco.t(16), forca: 15 }); }
        if (!u.sucesso) {
          FX.poco(palco, { cx: a.x, cy: a.y, rx: R + palco.t(30), ry: R + palco.t(24), forca: 10 });
          if (parado) return;
          const re = R + palco.t(20);
          if (t < 700) FX.anel(palco, { cx: a.x, cy: a.y, r: re + Math.round(FX.rampa(t, 0, 700) * palco.t(40)), esp: 2, pal: ["G", "g", "d"], achata: 0.8, rastro: 3, vis: Math.round(12 * (1 - t / 700)) });
          if (passo && q === 1) enx.soltar(14, () => ({ x: a.x + FX.aleatorio(-re, re), y: a.y - re * 0.5, vx: FX.aleatorio(-0.4, 0.4), vy: FX.aleatorio(-0.6, 0.2), g: 0.12, arrasto: 0.95,
            vida: Math.round(FX.aleatorio(18, 30)), desenho: "brasa", pal: ["o", "r", "G", "g", "d"] }));
          if (passo && q > 2 && q % 4 === 0) enx.soltar(1, () => ({ x: a.x + FX.aleatorio(-re, re), y: a.y + FX.aleatorio(-re * 0.6, 0), vx: FX.aleatorio(-0.2, 0.2), vy: FX.aleatorio(0.3, 0.8), g: 0.02, arrasto: 0.98,
            vida: Math.round(FX.aleatorio(20, 30)), desenho: Math.random() < 0.5 ? "ponto" : "duplo", pal: ["w", "G", "g", "d"] }));
          if (passo) enx.passo();
        enx.desenhar(palco);
          return;
        }
        const re = R + Math.round(R * [0.71, 0.96, 1.04, 1.12, 1.22][f]);
        const longo = [2.6, 3.4, 3.6, 3.9, 4.3][f], calmo = [1.9, 2.1, 2.2, 2.35, 2.55][f];
        const n = 18 + 2 * Math.max(0, f - 1);
        const vis = parado ? 9 : t < 900 ? Math.round(FX.rampa(t, 500, 400, 16, 11)) : 10 + Math.round(Math.sin(t / 420));
        const r1 = Math.round(re * (parado ? calmo : t < 900 ? longo : FX.rampa(t, 900, 500, longo, calmo)));
        const achata = parado ? 0.6 : t < 900 ? 0.72 : FX.rampa(t, 900, 500, 0.72, 0.6);
        const ang = 0.15 + (parado ? 0 : (t / FX.QUADRO) * 0.012);  // contínuo: gira a cada quadro de 30
        if (cores) {  // o prisma: os raios repartidos entre as cores do nível, cada cor no seu lugar da volta
          const m = Math.max(2, Math.round(n / cores.length));
          cores.forEach((c, i) => FX.raios(palco, { cx: a.x, cy: a.y, n: m, ang: ang + (i * Math.PI * 2) / (m * cores.length),
            larg: 0.32 / cores.length, r0: R, r1, pal: ["W", "#fff4c8", c, c], esbate: 0.3, achata, alterna: 0.62, vis }));
        } else FX.raios(palco, { cx: a.x, cy: a.y, n, ang, larg: 0.32, r0: R, r1, pal: pal.slice(1), esbate: 0.3, achata, alterna: 0.62, vis });
        FX.estrela(palco, { cx: a.x, cy: a.y, pontas: 14 + 2 * Math.max(0, f - 1), ri: R + 2, re, pal, cores: estrelaCores });
        FX.poco(palco, { cx: a.x, cy: a.y, rx: R + 2, ry: R + 2, forca: 14 });  // a peça lê sobre o selo
        if (parado) return;
        FX.claraoLocal(palco, { cx: a.x, cy: a.y, r: R + palco.t([24, 30, 34, 38, 44][f]), t, dur: f >= 3 ? 240 : 200, espalha: 0 });
        // os anéis do impacto: um até o +2, dois do +3, três do +9 (um só golpe, sem repetir)
        [0, 110, 220].slice(0, f >= 3 ? 3 : f >= 1 ? 2 : 1).forEach((d, i) => {
          const tt = t - d;
          if (tt >= 0 && tt < 420) FX.anel(palco, { cx: a.x, cy: a.y, r: re + Math.round(FX.rampa(tt, 0, 400) * palco.t([50, 70, 80, 96, 110][f] - i * 12)), esp: 2,
            pal: cores ? ["W", cores[i % cores.length], cores[(i + 1) % cores.length]] : ["W", pal[1], pal[2]], achata: 0.6, rastro: 3, vis: Math.round(14 * (1 - tt / 420)) });
        });
        if (passo && q === 1) enx.soltar([24, 42, 52, 64, 84][f], (i) => {
          const g = FX.aleatorio(0, Math.PI * 2), v = FX.aleatorio(3, 7.5) * [0.95, 1.25, 1.3, 1.4, 1.5][f];
          return { x: a.x + Math.cos(g) * re * 0.8, y: a.y + Math.sin(g) * re * 0.7, vx: Math.cos(g) * v, vy: Math.sin(g) * v - 2, g: 0.36, arrasto: 0.97,
            vida: Math.round(FX.aleatorio(18, 32)), desenho: ["lasca", "caco", "cruz", "duplo"][i % 4],
            pal: cores ? ["W", cores[i % cores.length], cores[(i + 2) % cores.length]] : ["W", pal[1], pal[2], pal[3]], piscar: i % 5 === 0 };
        });
        // depois do golpe: brasas subindo e, nos níveis altos, pontos de brilho em volta (sem repetir o golpe)
        if (passo && q > 6 && q % [3, 3, 3, 2, 2][f] === 0) enx.soltar(1, () => ({ x: a.x + FX.aleatorio(-re, re), y: a.y + re * 0.6, vx: FX.aleatorio(-0.3, 0.3), vy: FX.aleatorio(-1.4, -0.7), vida: 16,
          desenho: "brasa", pal: cores ? ["W", cores[q % cores.length], "D"] : ["Y", "O", "o", "r", "D"] }));
        if (passo && f >= 2 && q > 10 && q % (f >= 3 ? 5 : 8) === 0) { const g = FX.aleatorio(0, Math.PI * 2); enx.soltar(1, () => ({ x: a.x + Math.cos(g) * re * 1.3, y: a.y + Math.sin(g) * re * 0.9,
          vx: 0, vy: 0, vida: 7, desenho: "brilho", pal: cores ? ["W", cores[q % cores.length]] : ["W", pal[1], pal[2]] })); }
        // a marca quente no título: poucas fagulhas saindo do número novo
        if (passo && numero && q === 2) { const m = palco.de(numero); enx.soltar([8, 12, 14, 16, 18][f], () => ({ x: m.x + FX.aleatorio(-m.rx, m.rx), y: m.y + FX.aleatorio(-m.ry * 0.5, m.ry * 0.5),
          vx: FX.aleatorio(-1.6, 1.6), vy: FX.aleatorio(-2.6, -0.8), g: 0.2, arrasto: 0.95, vida: Math.round(FX.aleatorio(8, 16)), desenho: Math.random() < 0.5 ? "ponto" : "brasa",
          pal: cores ? ["W", cores[0], cores[1]] : ["W", "Y", "O", "o"] })); }
        if (passo) enx.passo();
        enx.desenhar(palco);
      });
      if (desde > 0 && ctl.pular) ctl.pular(desde);
      return ctl;
    };
  }

  /** A apresentação do resultado do reforço (a mesma organização no sucesso e na falha). */
  function apresentarReforco(u) {
    const d = ultimoDesenho, p = d && d.pecas.find((x) => x.uid === u.uid);
    if (!p) return;
    const maximo = u.sucesso && u.para >= p.limite;
    const sub = u.sucesso ? (maximo ? `<span class="rf-res-sub">Reforço máximo</span>` : "") : `<span class="rf-res-queda">+${u.de} → +${u.para}</span>`;
    abrirRes({
      id: `r${u.id}`, classe: `reforco ${u.sucesso ? "ok" : "mau"} f${faixaNivel(u.para)}${maximo ? " maximo" : ""}`,
      aria: `Reforço: ${u.sucesso ? "sucesso" : "falhou"}, ${p.item.nome}`,
      titulo: `${nomeRes(p, u)}${sub}`,
      arte: `<div class="rf-res-arte r-${h(p.item.raridade)}">${iconePeca(p.item)}${gravura(p.encantos)}</div>`,
      ficha: `${rotuloPeca(p)}<div class="rf-res-linhas">${linhasRes(p, u.linhas, !u.sucesso)}</div>${p.efeito ? `<p class="rf-res-efeito">${h(p.efeito)}</p>` : ""}${sulcosRes(p.encantos)}`,
      banner: `<span class="rf-banner ${u.sucesso ? "ok" : "mau"}">${u.sucesso ? "Sucesso" : "Falhou"}</span>`,
      nivel: p.reforco,
      fx: efeitoReforco(u, cena && !reduzido() ? Math.max(0, performance.now() - cena.t0 - IMPACTO) : 0),
    });
  }

  /** A gravação concluída, em destaque: o nome da peça, a peça com a borda de luz das gravações e o acabamento do
   *  reforço, os sulcos ao lado com a gravação nova em destaque (o nome, o símbolo e o efeito dela; as outras só pelo
   *  nome), a que saiu (na substituição), "Gravado" na cor da essência e o OK. Sem sorteio: nada de suspense. */
  function apresentarGravacao(g) {
    const d = ultimoDesenho, p = d && d.pecas.find((x) => x.uid === g.uid);
    if (!p) return;
    const nova = (p.encantos || [])[g.sulco];
    abrirRes({
      id: `g${g.id}`, classe: "gravacao", aria: `Gravação: ${g.para.nome} em ${p.item.nome}`,
      titulo: nomeRes(p, null),
      arte: `<div class="rf-res-arte r-${h(p.item.raridade)}">${iconePeca(p.item)}${gravura(p.encantos)}</div>`,
      ficha: `${rotuloPeca(p)}${sulcosRes(p.encantos, g.sulco, g.de)}${nova ? `<p class="rf-res-ess" style="--ess:${h(nova.cor)}">${h(nova.efeito)}${nova.limite ? ` <span>${h(nova.limite)}</span>` : ""}</p>` : ""}`,
      banner: `<span class="rf-banner grav" style="--ess:${h(g.para.cor)}">Gravado</span>`,
      nivel: p.reforco,
      fx: efeitoGravacao(g, reduzido() ? 0 : Math.max(0, performance.now() - g.t0 - GRAVA_TRACO)),
    });
  }
  /** O efeito da gravação: a inscrição termina num anel curto na cor da essência e num punhado de brilhos; depois,
   *  poucos brilhos em volta da peça até o OK (sem raios: não é sorte, é trabalho). */
  function efeitoGravacao(g, desde) {
    return (palco, el) => {
      const alvo = el.querySelector(".rf-res-arte"), ficha = el.querySelector(".rf-res-ficha"), enx = FX.enxame();
      const pal = g.para.fx || ["W", "Y", "O", "o"], cor = g.para.cor;
      const ctl = animarRes(palco, (t, q, parado, passo) => {
        const a = palco.de(alvo), R = Math.max(a.rx, a.ry) + palco.t(8);
        if (ficha) { const f = palco.de(ficha); FX.poco(palco, { cx: f.x, cy: f.y, rx: f.rx + palco.t(26), ry: f.ry + palco.t(16), forca: 15 }); }
        FX.poco(palco, { cx: a.x, cy: a.y, rx: R + 2, ry: R + 2, forca: 12 });
        if (parado) return;
        const tp = (t - 900) % 2400;  // depois da entrada, um anel fino de tempos em tempos (a gravação acesa)
        if (t > 900 && tp < 520) FX.anel(palco, { cx: a.x, cy: a.y, r: R + Math.round((tp / 520) * palco.t(34)), esp: 1, pal: [cor, cor, cor], achata: 0.85, rastro: 2, vis: Math.round(9 * (1 - tp / 520)) });
        if (t < 420) FX.anel(palco, { cx: a.x, cy: a.y, r: R + Math.round(FX.rampa(t, 0, 400) * palco.t(60)), esp: 2, pal: ["W", cor, cor], achata: 0.85, rastro: 3, vis: Math.round(14 * (1 - t / 420)) });
        if (passo && q === 1) enx.soltar(14, () => ({ x: a.x + FX.aleatorio(-R, R), y: a.y + FX.aleatorio(-R, R * 0.4), vx: FX.aleatorio(-1, 1), vy: FX.aleatorio(-1.8, -0.6), g: 0.05,
          vida: Math.round(FX.aleatorio(10, 18)), desenho: Math.random() < 0.4 ? "brilho" : "ponto", pal }));
        if (passo && q > 8 && q % 6 === 0) { const ang = FX.aleatorio(0, Math.PI * 2); enx.soltar(1, () => ({ x: a.x + Math.cos(ang) * R * 1.3, y: a.y + Math.sin(ang) * R,
          vx: 0, vy: -0.2, vida: 9, desenho: "brilho", pal })); }
        if (passo) enx.passo();
        enx.desenhar(palco);
      });
      if (desde > 0 && ctl.pular) ctl.pular(desde);
      return ctl;
    };
  }

  /** A desmontagem: um toque na bancada, a peça se desfaz em fragmentos de pixel que voam para o encaixe do material,
   *  e um clarão pequeno onde ela estava. Sem raios nem celebração. Com movimento reduzido, nada se move. */
  function fragmentar(jan) {
    pararFx();
    const alvo = jan.querySelector(".rf-chapa .rf-desfaz"), destino = jan.querySelector(".rf-chapa .rf-recebe .rf-encaixe");
    soar("equipar");
    if (typeof FX === "undefined" || !alvo || !destino || reduzido()) return;
    baque(BAQUE.desmonte);
    palco = FX.palco(jan, { z: 2, classe: "rf-fx" });
    const enx = FX.enxame();
    ctl = FX.animar(palco, (t, q) => {
      const a = palco.de(alvo), d = palco.de(destino), R = Math.max(a.rx, a.ry);
      if (t < 120) FX.claraoLocal(palco, { cx: a.x, cy: a.y, r: R + palco.t(10), t, dur: 120, espalha: 0, pal: ["W", "w", "G", "g"] });
      if (q === 1) enx.soltar(26, (i) => {
        const x = a.x + FX.aleatorio(-R, R), y = a.y + FX.aleatorio(-R, R), voo = FX.aleatorio(6, 9);
        return { x, y, vx: (d.x - x) / voo + FX.aleatorio(-0.6, 0.6), vy: (d.y - y) / voo - FX.aleatorio(0.5, 1.6), g: 0.18, arrasto: 0.94,
          vida: Math.round(voo + FX.aleatorio(1, 4)), desenho: ["caco", "lasca", "ponto", "duplo"][i % 4], pal: ["w", "G", "g", "d"] };
      });
      enx.passo(); enx.desenhar(palco);
    });
  }

  /** A gravação: a luz da essência percorre a borda do molde (as quatro barras, uma a uma, como um buril), fagulhas
   *  na cor dela; no fim do traço, um anel curto sai da peça e a borda de luz fica. Sem raios: não é sorte, é trabalho. */
  function gravar(jan, g) {
    pararFx();
    if (typeof FX === "undefined" || reduzido()) return;
    const alvo = jan.querySelector(".rf-chapa .rf-encaixe.grande");
    if (!alvo) return;
    palco = FX.palco(jan, { z: 2, classe: "rf-fx" });
    const enx = FX.enxame(), pal = g.para.fx || ["W", "Y", "O", "o"];
    const desde = performance.now() - g.t0;
    ctl = FX.animar(palco, (t, q) => {
      const a = palco.de(alvo), R = Math.max(a.rx, a.ry) + palco.t(8);
      if (t < GRAVA_TRACO) {
        // o ponto do buril dá a volta na borda (em cima, à direita, embaixo, à esquerda) e solta fagulhas
        const u = t / GRAVA_TRACO, lado = Math.min(3, Math.floor(u * 4)), f = u * 4 - lado;
        const pts = [[a.x - R + 2 * R * f, a.y - R], [a.x + R, a.y - R + 2 * R * f], [a.x + R - 2 * R * f, a.y + R], [a.x - R, a.y + R - 2 * R * f]][lado];
        if (q % 1 === 0) enx.soltar(2, () => ({ x: pts[0], y: pts[1], vx: FX.aleatorio(-1.2, 1.2), vy: FX.aleatorio(-1.6, 0.4), g: 0.12, arrasto: 0.95,
          vida: Math.round(FX.aleatorio(6, 12)), desenho: Math.random() < 0.5 ? "ponto" : "duplo", pal }));
      }
      enx.passo(); enx.desenhar(palco);
    });
    if (desde > 0 && ctl.pular) ctl.pular(desde);
  }
  /** O fim da gravação: a bancada volta à oferta, com a peça já gravada e a mesma seleção. */
  function assentarGrav() {
    if (!gravando || gravando.fim) return;
    document.body.classList.remove("rf-em-cena");
    gravando.fim = true;
    sulcoDe = null;  // a seleção vai para o próximo sulco vazio (ou o primeiro, se a peça está cheia)
    limparRelogios();
    pararFx();
    fecharRes();
    if (ultimoRaiz && ultimoRaiz.isConnected && ultimoDesenho) ultimoRaiz.replaceWith(Telas.painel({ tipo: "forja_proto", dados: ultimoDesenho }));
    const jan = document.querySelector(".rf-janela");
    if (jan && (document.activeElement === document.body || !jan.contains(document.activeElement))) {
      // o foco volta à ação da bancada (a próxima oferta), à peça escolhida, ou ao Fechar
      const alvo = primeiro(jan, focoDepois || "[data-reforcar]:not([aria-disabled]), [data-gravar]:not([aria-disabled]), [data-uid].marcada, [data-fechar]");
      if (alvo) alvo.focus();
    }
  }
  /** Encerra a cena da gravação sem redesenhar (quem chama redesenha logo depois): a gravação já está feita. */
  function encerrarGrav() {
    if (!gravando || gravando.fim) return;
    gravando.fim = true;
    sulcoDe = null;
    pararFx();
    fecharRes();
  }
  function adiantarGrav() {
    const f = faseGrav();
    if (f === "traco") { gravando.t0 = performance.now() - GRAVA_TRACO; if (ultimoRaiz && ultimoDesenho) ultimoRaiz.replaceWith(Telas.painel({ tipo: "forja_proto", dados: ultimoDesenho })); }
  }
  function dispensarGrav() { if (faseGrav() === "gravado") { calmaAte = performance.now() + 450; assentarGrav(); } }

  /** O impacto: o resultado sai da bancada para a apresentação em destaque (o efeito, o nome com o nível novo, as
   *  propriedades, o resultado e o OK). Só classes, a apresentação e o canvas; nada é pedido ao motor. */
  function entrarDesfecho(u) {
    const jan = document.querySelector(".rf-janela");
    if (!jan || !cena || cena.fim) return;
    jan.classList.add("em-cena", "revelou");
    jan.classList.remove("aquecendo");  // a esteira passa ao resultado (atrás do véu)
    apresentarReforco(u);
  }
  /** Fim da cena: a bancada volta para a próxima oferta, a placa resume o resultado e o foco volta à ação. */
  function assentar() {
    limparRelogios();
    pararFx();
    fecharRes();
    baque(null);  // a oferta volta sem deslocamento, mesmo se o golpe ainda corria
    const estava = cena && !cena.fim;
    if (cena) cena.fim = true;
    // a bancada é desenhada de novo com a próxima oferta (durante a cena, os encaixes mostravam o que foi pago)
    if (estava && ultimoRaiz && ultimoRaiz.isConnected && ultimoDesenho) {
      ultimoRaiz.replaceWith(Telas.painel({ tipo: "forja_proto", dados: ultimoDesenho }));
    }
    const jan = document.querySelector(".rf-janela");
    jan?.classList.remove("em-cena", "aquecendo", "revelou");
    document.body.classList.remove("rf-em-cena");
    if (jan && (document.activeElement === document.body || !jan.contains(document.activeElement))) {
      // o foco volta à ação da bancada (a próxima oferta), à peça escolhida, ou ao Fechar
      const alvo = primeiro(jan, focoDepois || "[data-reforcar]:not([aria-disabled]), [data-gravar]:not([aria-disabled]), [data-uid].marcada, [data-fechar]");
      if (alvo) alvo.focus();
    }
  }
  /** Um clique, Enter, Espaço ou Esc durante a cena: do aquecimento vai ao desfecho; do desfecho, à próxima oferta. */
  /** Adiantar só leva do aquecimento ao resultado; o resultado fica até a confirmação (OK, Enter ou Esc: dispensar). */
  function adiantar(u) {
    if (fase() === "forja") { cena.t0 = performance.now() - IMPACTO; limparRelogios(); entrarDesfecho(u); }
  }
  function dispensar() { if (fase() === "desfecho") { calmaAte = performance.now() + 450; assentar(); } }
  const revelar = assentar;  // os gestos que interrompem (trocar de peça, fechar) assentam a cena

  // ------------------------------------------------------------------ o reflexo do reforço
  /** Um reflexo diagonal curto atravessa a silhueta da peça (o próprio desenho é a máscara: só o que tem pixel
   *  brilha), na cor do nível: +1 claro e discreto, +2 esverdeado, +3 azul, +4 dourado. A borda de raridade do encaixe
   *  não muda. Passa no sucesso, na escolha da peça, no mouse e no foco, e sozinho em ciclo (abaixo); um gesto não o
   *  repete antes de 1,5 s. Com movimento reduzido, fica parado e discreto. */
  function reflexo(caixa, nivel, fixo = false, parado = false) {
    if (!caixa || !nivel) return;
    const img = caixa.querySelector("img, canvas");
    if (!img) return;
    const ja = caixa.querySelector(".rf-reflexo");
    if (parado && ja && ja.classList.contains("passa") && ja.dataset.nivel === String(Math.min(nivel, 12))) return;
    const agora = performance.now();
    if (!fixo && caixa._reflexo && agora - caixa._reflexo < 1500) return;
    caixa._reflexo = agora;
    let r = caixa.querySelector(".rf-reflexo");
    if (!r) {
      r = document.createElement("i");
      r.className = "rf-reflexo";
      r.setAttribute("aria-hidden", "true");
      const src = img.tagName === "IMG" ? img.currentSrc || img.src : img.toDataURL();
      r.style.maskImage = r.style.webkitMaskImage = `url("${src}")`;
      caixa.appendChild(r);
    }
    Object.assign(r.style, { left: `${img.offsetLeft}px`, top: `${img.offsetTop}px`, width: `${img.offsetWidth}px`, height: `${img.offsetHeight}px` });
    r.dataset.nivel = Math.min(nivel, 12);
    r.classList.remove("passa");
    void r.offsetWidth;  // recomeça a passada
    r.classList.add("passa");
  }
  function apagarReflexo() {}  // parado (movimento reduzido), o reflexo fica: é o acabamento da peça reforçada

  /** O acabamento permanente do reforço sobre o desenho da peça (o próprio desenho é a máscara: só os pixels dela
   *  recebem cor e brilho; a borda de raridade, a seleção, o foco e os rastros das gravações não mudam):
   *    +4        o contorno dourado de 1 px (já aprovado);
   *    +5 a +8   o contorno na cor do nível (turquesa, safira, ametista, rubi) e um veio da mesma cor que atravessa
   *              a peça devagar, mais presente a cada nível; o +8 com um ponto de brilho;
   *    +9 a +12  o veio em várias cores, contínuo (2, 3, 4 cores; o +12 em todas, como pedra lapidada), o contorno
   *              trocando de cor em degraus e pontos de brilho (1 a 4).
   *  A presença sobe pela cor e pelo brilho, não pela velocidade: a mesma volta lenta em todos. Cada peça começa num
   *  ponto diferente da volta (nada pisca em sincronia). `n` 0 a 3 tira tudo (uma queda também tira). */
  const BRILHOS = { 8: 1, 9: 1, 10: 2, 11: 3, 12: 4 };
  // o veio de cada nível: a sequência de cores ao longo da diagonal, um pixel do desenho por entrada (0: sem cor)
  const R_ = "#ff3c60", O_ = "#ffb032", E_ = "#46e2a0", A_ = "#468cff", V_ = "#aa64ff", M_ = "#ff6edc", W_ = "#fff4c8";
  const z = (n) => Array(n).fill(0), x = (c, n) => Array(n).fill(c);
  const VEIOS = {
    5: [...x("#46e2cc", 2), ...z(18)],
    6: [...x("#5a8cff", 2), ...z(6), "#a8c4ff", ...z(11)],
    7: [...x("#b064ff", 2), ...z(5), "#d9a8ff", ...z(10)],
    8: [...x(R_, 3), ...z(3), "#ff8090", ...z(11)],
    9: [...x(R_, 3), ...z(5), ...x(O_, 3), ...z(9)],
    10: [...x(R_, 3), ...z(3), ...x(O_, 3), ...z(3), ...x(A_, 3), ...z(7)],
    11: [...x(R_, 3), ...x(O_, 3), ...z(3), ...x(E_, 3), ...x(A_, 3), ...z(7)],
    12: [...x(R_, 3), ...x(O_, 3), W_, ...z(3), ...x(E_, 3), ...x(A_, 3), W_, ...z(3), ...x(V_, 3), ...x(M_, 2), W_, ...z(4)],
  };
  /** O veio em pixel: a peça inteira na resolução do desenho, ampliada sem suavização; a cada passo, as cores andam um
   *  pixel na diagonal (um relógio só para todas as peças, cada uma na sua fase). */
  function pintarVeio(cv) {
    const seq = VEIOS[cv.dataset.nivel], ctx = cv.getContext("2d");
    if (!seq || !ctx) return;
    const w = cv.width, hh = cv.height, fase = (cv._fase || 0) + (reduzido() ? 0 : cv._passo || 0);
    ctx.clearRect(0, 0, w, hh);
    for (let d = 0; d < w + hh; d++) {
      const cor = seq[((d + fase) % seq.length + seq.length) % seq.length];
      if (!cor) continue;
      ctx.fillStyle = cor;
      for (let x = Math.max(0, d - hh + 1); x <= Math.min(d, w - 1); x++) ctx.fillRect(x, d - x, 1, 1);
    }
  }
  setInterval(() => {
    if (document.hidden) return;
    document.querySelectorAll("canvas.rf-acab").forEach((cv) => { cv._passo = (cv._passo || 0) + 1; pintarVeio(cv); });
  }, 250);
  function acabamento(caixa, n) {
    if (!caixa) return;
    const img = caixa.querySelector(":scope > img, :scope > canvas, :scope > .icone-px > img") || caixa.querySelector("img, canvas");
    const nivel = Math.min(n || 0, 12);
    if (nivel >= 4) caixa.dataset.acab = nivel; else delete caixa.dataset.acab;
    const veio = caixa.querySelector(":scope > .rf-acab"), pontos = caixa.querySelector(":scope > .rf-acab-brilhos");
    if (nivel < 5 || !img) { veio?.remove(); pontos?.remove(); return; }
    const src = img.tagName === "IMG" ? img.currentSrc || img.src : img.toDataURL();
    const pos = { left: `${img.offsetLeft}px`, top: `${img.offsetTop}px`, width: `${img.offsetWidth}px`, height: `${img.offsetHeight}px` };
    const camada = (atual, classe, tag = "i") => {
      let el = atual;
      if (!el || el._src !== src) {
        el?.remove();
        el = document.createElement(tag);
        el.className = classe;
        el.setAttribute("aria-hidden", "true");
        el.style.maskImage = el.style.webkitMaskImage = `url("${src}")`;
        el._src = src;
        el.style.animationDelay = `-${(Math.random() * 9).toFixed(2)}s`;  // cada peça num ponto da volta
        caixa.appendChild(el);
      }
      Object.assign(el.style, pos);
      return el;
    };
    const cv = camada(veio, "rf-acab", "canvas");
    const lado = img.naturalWidth || img.width || 32;
    if (cv.width !== lado) { cv.width = lado; cv.height = img.naturalHeight || img.height || lado; cv._fase = Math.floor(Math.random() * 24); }
    if (cv.dataset.nivel !== String(nivel)) { cv.dataset.nivel = nivel; pintarVeio(cv); }
    const k = BRILHOS[nivel] || 0;
    if (!k) { pontos?.remove(); return; }
    const b = camada(pontos, "rf-acab-brilhos");
    const px = Math.max(1, Math.round(img.offsetWidth / (img.naturalWidth || img.width || 32)));  // um pixel do desenho
    b.style.setProperty("--px-peca", `${px}px`);
    if (b.childElementCount !== k) {
      b.innerHTML = Array.from({ length: k }, (_, i) => `<i style="animation-delay:-${(Math.random() * 2.4 + i * 0.6).toFixed(2)}s"></i>`).join("");
      b.querySelectorAll("i").forEach((p) => {
        const mover = () => {  // um ponto novo da peça a cada volta (perto do miolo, onde o desenho tem pixel)
          p.style.left = `${Math.round(20 + Math.random() * 60)}%`;
          p.style.top = `${Math.round(18 + Math.random() * 62)}%`;
        };
        mover();
        p.addEventListener("animationiteration", mover);
      });
    }
  }
  /** Mouse e foco do teclado nas peças da esteira: cada uma brilha sozinha, só quando é a vez dela. */
  function ligarReflexos(jan) {
    jan.querySelectorAll(".rf-esteira .rf-peca").forEach((b) => {
      const n = +b.dataset.reforco;
      if (!n) return;
      b.addEventListener("mouseenter", () => { if (!fase()) reflexo(b, n); });
      b.addEventListener("focus", () => { if (!fase() && b.matches(":focus-visible")) reflexo(b, n); });
      b.addEventListener("mouseleave", () => apagarReflexo(b));
      b.addEventListener("blur", () => apagarReflexo(b));
    });
  }

  /* O ciclo: toda peça reforçada à vista brilha sozinha, de tempos em tempos. Na forja (a esteira e o molde), no
     Inventário (o equipado e a bolsa, e as opções de um espaço) e no "Equipado" da ficha lateral. A primeira passada
     vem 2 s depois de a peça aparecer; depois, a cada ~3 s, cada peça na sua vez (defasadas, nunca todas juntas). O
     horário de cada uma fica guardado pelo lugar dela, para um redesenho da tela não recomeçar a espera. Durante o
     aquecimento, todas esperam (a cor do nível novo não pode aparecer antes do desfecho); no resultado mantido, já
     brilham com o nível novo (o +4 com a luz dele). Só nesta demonstração. */
  const PRIMEIRA = 2000, PERIODO = 3000, DEFASAGEM = 450;
  const agenda = new Map();  // lugar → {proxima, visto}
  function pecasReforcadas() {
    const lista = [];
    const heroi = App.estado && App.estado.heroi;
    const nivel = (it) => (it && +it.reforco) || 0;
    document.querySelectorAll(".slot-px.mini[data-mini]").forEach((el) => {
      const it = heroi && heroi.equip && heroi.equip[el.dataset.mini];
      lista.push([el, `mini:${el.dataset.mini}:${it ? it.nome : ""}`, nivel(it)]);
    });
    document.querySelectorAll(".tela.inventario .slot-px[aria-label], .tela.inventario .peca-opcao").forEach((el, i) => {
      const it = pecaDoDono(el);
      lista.push([el, `inv:${el.dataset.espaco || el.dataset.mochila || "o" + i}:${it ? it.nome : ""}`, nivel(it)]);
    });
    document.querySelectorAll(".rf-janela .rf-esteira .rf-peca, .rf-janela .rf-chapa .rf-encaixe.grande[data-reforco]").forEach((el) => {
      lista.push([el, `forja:${el.dataset.uid || "molde"}:${el.getAttribute("aria-label") || ""}:${el.dataset.reforco}`, +el.dataset.reforco || 0]);
    });
    return lista.filter((x) => x[2] > 0 && x[0].offsetParent !== null);  // só o que está à vista
  }
  function bordasGravadas() {
    const marcar = (el, lista) => {
      const html = gravura(lista);
      if (el._gravuras === html) return;  // nada mudou: a borda continua a volta dela (sem recomeçar)
      el._gravuras = html;
      el.querySelectorAll(":scope > .rf-gravura").forEach((r) => r.remove());
      if (html) el.insertAdjacentHTML("beforeend", html);
    };
    const heroi = App.estado && App.estado.heroi;
    document.querySelectorAll(".slot-px.mini[data-mini]").forEach((el) => {
      const it = heroi && heroi.equip && heroi.equip[el.dataset.mini];
      marcar(el, it && it.encantos);
    });
    document.querySelectorAll(".tela.inventario .slot-px[aria-label]").forEach((el) => {
      const it = pecaDoDono(el);
      marcar(el, it && it.encantos);
    });
  }

  /** A aparência persistente da peça (a borda das gravações, a luz do +4, o reflexo parado do movimento reduzido):
   *  aplicada na hora em que um slot aparece ou é redesenhado (o observador da página chama), não no próximo ciclo. A
   *  tela do jogo redesenha os painéis a cada atualização (Continuar, uma ação qualquer): antes, o slot novo ficava até
   *  200 ms sem a aparência e a borda recomeçava a volta, e isso piscava. */
  function decorar() {
    bordasGravadas();
    if (fase() === "forja") return;  // no aquecimento, o nível novo ainda não apareceu; do desfecho em diante, sim
    pecasReforcadas().forEach(([el, , n]) => {
      acabamento(el, n);
      if (reduzido() && n) reflexo(el, n, true, true);
    });
    acabamentoNoAchado();
    nivelNaDica();
  }
  function ciclo() {
    decorar();
    const luta = !!(App.estado && App.estado.combate);
    document.querySelectorAll(".forja-proto").forEach((f) => f.classList.toggle("rf-em-luta", luta));
    if (fase() === "forja" || document.hidden) return;  // no aquecimento, nenhuma peça brilha (a cor do nível novo vem no desfecho)
    const agora = performance.now();
    for (const [k, a] of agenda) if (agora - a.visto > 8000) agenda.delete(k);  // o que saiu da tela não fica na agenda
    pecasReforcadas().forEach(([el, lugar, n], i) => {
      let a = agenda.get(lugar);
      if (!a || agora - a.visto > 8000) {  // apareceu (ou voltou depois de um tempo fora): a espera de 2 s
        a = { proxima: agora + PRIMEIRA + (i % 8) * DEFASAGEM };
        agenda.set(lugar, a);
      }
      a.visto = agora;
      if (reduzido()) return;  // parado, sempre à vista
      if (agora >= a.proxima) { reflexo(el, n, true); a.proxima = agora + PERIODO + (i % 3) * 150; }
    });
  }
  setInterval(ciclo, 200);
  /** O véu da cena: um recorte do tamanho da janela com a sombra para fora. A janela mora num contexto de camadas
   *  (a mesa da HUD), e um véu de tela inteira por cima escureceria a bancada junto com o entorno. */
  function vela() {
    requestAnimationFrame(() => {
      const v = document.getElementById("rf-vela"), jan = document.querySelector(".rf-janela");
      if (!v || !jan) return;
      const r = jan.getBoundingClientRect();
      Object.assign(v.style, { left: `${Math.round(r.left)}px`, top: `${Math.round(r.top)}px`, width: `${Math.round(r.width)}px`, height: `${Math.round(r.height)}px` });
    });
  }
  addEventListener("resize", vela);
  if (!document.getElementById("rf-vela")) document.body.insertAdjacentHTML("beforeend", '<div id="rf-vela" aria-hidden="true"></div>');

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
    ultimaPos = { left: `${Math.round(r.left + 8)}px`, top: `${Math.round(r.top + 8)}px`, width: `${Math.round(r.width - 16)}px`, height: `${Math.round(r.height - 16)}px` };
    Object.assign(jan.style, ultimaPos);
  }
  window.addEventListener("resize", posicionar);
  const primeiro = (raiz, foco) => foco && foco.split(",").map((x) => raiz.querySelector(x.trim())).find(Boolean);

  let ultimoDesenho = null, ultimoRaiz = null, saldoAntes = null, ultimaPos = null;
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
    // a próxima ação (fechar, trocar de serviço, de dono, de peça) encerra a cena que estiver tocando
    const limpar = () => { revelar(); encerrarGrav(); mostrarId = 0; focoDepois = null; };
    const abrir = (qual, foco) => { janela = qual; selUid = null; confirmando = null; limpar(); redesenhar(foco || ".rf-janela .rf-peca, .rf-janela [data-fechar]"); };
    const fechar = () => { const era = janela; janela = null; confirmando = null; limpar(); redesenhar(`[data-servico="${era}"]`); };
    raiz.querySelectorAll("[data-servico]").forEach((b) => b.addEventListener("click", () => {
      if (App.estado && App.estado.combate) { App.recusar(b, "Durante a luta, a forja espera."); return; }
      abrir(b.dataset.servico);
    }));
    const jan = raiz.querySelector(".rf-janela");
    if (!jan) return;
    requestAnimationFrame(posicionar);
    posicionar();
    // o saldo que mudou desde o último desenho acende um instante (a cobrança do reforço, o que a desmontagem rendeu)
    const saldos = { ouro: d.ouro, ...Object.fromEntries(d.materiais.map((m) => [m.id, m.qtd])) };
    if (saldoAntes) jan.querySelectorAll(".rf-rec[data-rec]").forEach((el) => {
      const k = el.dataset.rec;
      if (saldoAntes[k] !== undefined && saldoAntes[k] !== saldos[k]) el.classList.add(saldos[k] < saldoAntes[k] ? "desce" : "sobe");
    });
    saldoAntes = saldos;
    const u = d.ultimo;
    const f = cena && u && cena.id === u.id ? fase() : "";
    const p0 = janela === "reforcar" ? d.pecas.find((x) => x.uid === selUid && x.aba === aba) : null;
    comparacao = p0 && !p0.no_limite && !p0.sem_reforco ? teste(p0, passoDe(p0)) : "";
    limparRelogios();
    pararFx();
    document.body.classList.toggle("rf-em-cena", !!f || (janela === "encantar" && !!faseGrav()));
    vela();
    if (f) {
      jan.classList.add("em-cena");
      const e = performance.now() - cena.t0;
      if (f === "forja") {
        jan.classList.add("aquecendo");
        relogios.push(setTimeout(() => entrarDesfecho(u), IMPACTO - e));
      } else {
        // um quadro depois: a janela recém-desenhada já está na página e no lugar (o efeito mede a peça)
        requestAnimationFrame(() => entrarDesfecho(u));
      }
    } else if (brilharSel) {
      brilharSel = false;
      const sel = p0 && jan.querySelector(".rf-chapa .rf-encaixe.grande");
      if (sel) requestAnimationFrame(() => reflexo(sel, p0.reforco));
    }
    const fg = janela === "encantar" ? faseGrav() : "";
    if (fg) {
      jan.classList.add("em-cena");
      const e = performance.now() - gravando.t0;
      if (fg === "traco") {
        if (!gravando.som) { gravando.som = true; soar("predio_ferreiro"); }
        requestAnimationFrame(() => gravar(jan, gravando));
        relogios.push(setTimeout(() => { if (raiz.isConnected) redesenhar(focoDepois); }, GRAVA_TRACO - e));
      } else {
        if (!gravando.somFim) { gravando.somFim = true; soar("aprender"); }
        requestAnimationFrame(() => apresentarGravacao(gravando));  // a gravação concluída, em destaque até o OK
      }
    }
    if (desmonte && janela === "desmontar" && performance.now() - desmonte.t0 < DESMONTE_MS) {
      if (!desmonte.fx) { desmonte.fx = true; requestAnimationFrame(() => fragmentar(jan)); }
      relogios.push(setTimeout(() => { desmonte.t0 = -Infinity; pararFx(); redesenhar(focoDepois); }, DESMONTE_MS - (performance.now() - desmonte.t0)));
    }
    ligarReflexos(jan);
    window.dispatchEvent(new Event("reforco-comparacao"));
    // durante a cena, um clique na bancada só revela: não compra, não escolhe, não desmonta (Enter e Espaço, no
    // ouvinte do documento, lá embaixo). Fechar, trocar de serviço, de dono ou de peça continuam valendo (o motor já
    // resolveu a tentativa).
    jan.addEventListener("click", (ev) => {
      if (performance.now() < calmaAte) { ev.preventDefault(); ev.stopPropagation(); return; }  // o resto do gesto que dispensou
      if (!fase() && !faseGrav()) return;
      if (ev.detail > 1) { ev.preventDefault(); ev.stopPropagation(); return; }  // o 2º clique de um clique duplo: nada
      if (ev.target.closest("[data-fechar], [data-janela], [data-aba], [data-uid]")) return;
      ev.preventDefault();
      ev.stopPropagation();
      if (faseGrav() === "traco") adiantarGrav(); else if (fase() === "forja") adiantar(d.ultimo);  // no resultado, só o OK
    }, true);
    jan.querySelector("[data-fechar]").addEventListener("click", fechar);
    // as dicas dos materiais e da ajuda também abrem pelo foco do teclado (o jogo só faz isso no mercado)
    jan.querySelectorAll(".rf-insumo, .rf-ajuda, .rf-chapa [data-retirar][data-dica]").forEach((el) => {
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
    jan.querySelectorAll("[data-uid]").forEach((b) => b.addEventListener("click", (ev) => {
      if (selUid !== b.dataset.uid) { selUid = b.dataset.uid; confirmando = null; brilharSel = true; limpar(); redesenhar(`[data-uid="${b.dataset.uid}"]`); }
      else if (ev.detail <= 1) { selUid = null; confirmando = null; confirmandoGrav = null; limpar(); redesenhar(`[data-uid="${b.dataset.uid}"]`); }  // de novo: retira
    }));
    jan.addEventListener("keydown", (ev) => {
      if (!["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"].includes(ev.key) || !ev.target.matches("[data-uid]")) return;
      const todas = [...jan.querySelectorAll("[data-uid]")];
      const i = todas.indexOf(ev.target);
      ev.preventDefault();
      todas[(i + (ev.key === "ArrowLeft" || ev.key === "ArrowUp" ? -1 : 1) + todas.length) % todas.length].focus();
    });
    const p = d.pecas.find((x) => x.uid === selUid);
    const ref = jan.querySelector("[data-reforcar]");
    if (ref) ref.addEventListener("click", (ev) => {
      if (ev.detail > 1) return;  // o segundo clique de um duplo clique não compra outro passo
      if (ref.getAttribute("aria-disabled")) { App.recusar(ref, ref.title); return; }
      const x = passoDe(p);
      pago = { de: p.reforco, chance: x.chance, linhas: x.linhas, ouro: x.ouro, fragmentos: x.fragmentos };
      const pedido = `t${Date.now()}`;
      const teste = testeProximo;
      if (pedir({ op: "reforcar", uid: p.uid, pedido, ...(teste ? { teste } : {}) }, ref,
        "[data-reforcar]:not([aria-disabled]), [data-uid].marcada")) {
        esperandoId = (d.ultimo ? d.ultimo.id : 0) + 1;
        testeProximo = null;
        window.dispatchEvent(new Event("reforco-teste"));
      }
    });
    // o encantamento: escolher a essência, gravar (ou pedir a confirmação da substituição), confirmar
    jan.querySelectorAll("[data-essencia]").forEach((b) => b.addEventListener("click", () => {
      if (essSel !== b.dataset.essencia) { essSel = b.dataset.essencia; confirmandoGrav = null; limpar(); redesenhar(`[data-essencia="${b.dataset.essencia}"]`); }
    }));
    jan.querySelectorAll("[data-sulco]").forEach((b) => b.addEventListener("click", () => {
      if (sulcoSel !== +b.dataset.sulco) { sulcoSel = +b.dataset.sulco; confirmandoGrav = null; limpar(); redesenhar(`[data-sulco="${b.dataset.sulco}"]`); }
    }));
    jan.querySelectorAll(".rf-essencias").forEach((grupo) => grupo.addEventListener("keydown", (ev) => {
      if (!["ArrowLeft", "ArrowRight"].includes(ev.key)) return;
      const todas = [...grupo.querySelectorAll("[data-essencia]")], i = todas.indexOf(document.activeElement);
      ev.preventDefault();
      todas[(i + (ev.key === "ArrowLeft" ? -1 : 1) + todas.length) % todas.length].focus();
    }));
    const pedirGravacao = (botao) => {
      const pedido = `g${Date.now()}`;
      const atual = (p.encantos || [])[sulcoSel];
      if (pedir({ op: "encantar", uid: p.uid, essencia: essSel, sulco: sulcoSel, pedido, substitui: atual ? atual.id : null }, botao,
        "[data-gravar]:not([aria-disabled]), [data-uid].marcada")) {
        esperandoId = (d.ultimo ? d.ultimo.id : 0) + 1;
      }
    };
    const grav = jan.querySelector("[data-gravar]");
    if (grav) grav.addEventListener("click", (ev) => {
      if (ev.detail > 1) return;
      if (grav.getAttribute("aria-disabled")) { if (grav.title) App.recusar(grav, grav.title); return; }
      if ((p.encantos || [])[sulcoSel]) { confirmandoGrav = { uid: p.uid }; redesenhar("[data-gravar-nao]"); return; }
      pedirGravacao(grav);
    });
    const gNao = jan.querySelector("[data-gravar-nao]");
    if (gNao) gNao.addEventListener("click", () => { confirmandoGrav = null; redesenhar("[data-gravar]"); });
    const gSim = jan.querySelector("[data-gravar-sim]");
    if (gSim) {
      const arma = performance.now() + 400;  // o clique que abriu a pergunta não a responde
      setTimeout(() => { if (gSim.isConnected) gSim.disabled = false; }, 400);
      gSim.addEventListener("click", (ev) => {
        if (gSim.disabled || performance.now() < arma || ev.detail > 1 || !confirmandoGrav) return;
        confirmandoGrav = null;
        pedirGravacao(gSim);
      });
    }
    // retirar a peça: o encaixe fica vazio; a peça continua onde estava (no corpo ou na bolsa). Durante uma cena, o clique
    // é do adiantar (o ouvinte de captura acima para ele aqui), e o segundo clique de um clique duplo não faz nada.
    const ret = jan.querySelector(".rf-chapa [data-retirar]");
    if (ret) {
      const tirar = () => {
        const uid = selUid;
        selUid = null; confirmando = null; confirmandoGrav = null;
        limpar();
        redesenhar(`[data-uid="${uid}"]`);
      };
      ret.addEventListener("click", (ev) => { if (ev.detail <= 1) tirar(); });
      ret.addEventListener("keydown", (ev) => { if ((ev.key === "Enter" || ev.key === " ") && !ev.repeat) { ev.preventDefault(); tirar(); } });
    }
    const des = jan.querySelector("[data-desmontar]");
    if (des) des.addEventListener("click", (ev) => {
      if (ev.detail > 1) return;
      if (des.getAttribute("aria-disabled")) { App.recusar(des, des.title); return; }
      confirmando = { uid: p.uid, nome: p.item.nome }; limpar(); redesenhar("[data-desmontar-nao]");
    });
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
        pedidoDesmonte = { icone: iconePeca(p.item), raridade: p.item.raridade };
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
    const jan = document.getElementById("rf-res") || document.querySelector(".rf-janela");  // a apresentação aberta prende o foco
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
    if ((ev.key !== "Enter" && ev.key !== " ") || !janela || (!fase() && !faseGrav()) || !document.querySelector(".rf-janela")) return;
    ev.preventDefault();
    ev.stopImmediatePropagation();
    if (!ev.repeat) {
      if (faseGrav() === "traco") adiantarGrav(); else if (faseGrav()) dispensarGrav();
      else if (fase() === "forja") adiantar(ultimoDesenho && ultimoDesenho.ultimo); else dispensar();
    }
  }, true);

  // Esc com a janela aberta: revela a cena, cancela a confirmação, fecha a janela; só então o Voltar da forja.
  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape" || !janela || !document.querySelector(".rf-janela")) return;
    ev.preventDefault();
    ev.stopImmediatePropagation();
    if (fase() === "forja") { adiantar(ultimoDesenho && ultimoDesenho.ultimo); return; }
    if (fase() === "desfecho") { dispensar(); return; }
    if (faseGrav() === "traco") { adiantarGrav(); return; }
    if (faseGrav()) { dispensarGrav(); return; }
    if (confirmando) { document.querySelector("[data-desmontar-nao]")?.click(); return; }
    if (confirmandoGrav) { document.querySelector("[data-gravar-nao]")?.click(); return; }
    document.querySelector(".rf-janela [data-fechar]")?.click();
  }, true);

  Telas.registrar("forja_proto", balcao, { ligar, esquecer: () => { janela = null; selUid = null; confirmando = null; confirmandoGrav = null; revelar(); assentarGrav(); mostrarId = 0; aba = "heroi"; } });

  // a faixa da demonstração escolhe o caso de teste da próxima tentativa (carregar.js); vale uma vez
  // e mostra a comparação de teste da peça escolhida (um controle de laboratório, fora da tela do jogador)
  let comparacao = "";
  window.ReforcoProto = {
    teste(modo) { if (modo !== undefined) testeProximo = modo || null; return testeProximo; },
    comparacao: () => comparacao,
    /** A luta de teste (laboratório): dois Esqueletos; o grupo volta como estava. Só com a forja aberta. */
    lutaTeste() {
      if (!document.querySelector(".forja-proto")) return false;
      document.querySelector(".rf-janela [data-fechar]")?.click();  // a janela fecha antes (a luta não acontece sob ela)
      return !!App.acao({ forja: true }, null, { op: "luta_teste" });
    },
    /** O acabamento de um nível num elemento qualquer (a folha de comparação da demonstração). */
    acabamento(el, n, passar = false) { acabamento(el, n); if (passar && n) reflexo(el, n, true); },
    /** Os níveis altos de teste (laboratório): peças do grupo levadas direto a níveis altos. Só com a forja aberta. */
    niveisTeste() {
      if (!document.querySelector(".forja-proto")) return false;
      revelar();
      return !!App.acao({ forja: true }, null, { op: "niveis_teste" });
    },
  };

  /* Os sulcos nas fichas e dicas de item de todas as telas (achado, Inventário, Equipado, mercado, forja). A ficha do
     Inventário chama Telas.htmlItem na hora: ela ganha a seção. As dicas guardam a função delas desde o começo: a seção
     entra na caixa da dica quando ela abre, pela peça do dono (a forja, o Equipado, a bolsa) ou pelo nome. */
  const htmlItemJogo = Telas.htmlItem;
  Telas.htmlItem = (it, ...resto) => {
    const html = htmlItemJogo(it, ...resto), sec = secaoEncantos(it && it.encantos);
    return sec ? html.replace(/(<div class="bonus">[\s\S]*?<\/div>)/, `$1${sec}`) : html;
  };
  /* O achado (a janela "Você encontrou") monta a ficha em pedaços (Festa.fichaItem), sem o htmlItem: os sulcos da peça
     achada entram debaixo das linhas dela quando a janela aparece, pela peça que a mensagem trouxe. */
  let achado = null;
  const abrirAchadoJogo = Telas.abrirAchado;
  Telas.abrirAchado = (d, ...resto) => { achado = d && d.item; return abrirAchadoJogo(d, ...resto); };
  /** O acabamento do reforço no item achado (a arte grande da janela "Você encontrou"). */
  function acabamentoNoAchado() {
    const arte = achado && achado.reforco && document.querySelector("#sobre-achado .achado-cartao.novo .achado-arte");
    if (arte) { arte.style.position ||= "relative"; acabamento(arte, achado.reforco); }
  }
  /** Na dica da peça, o +N do nome na cor do nível (a dica não tem o desenho; o nível se reconhece pela cor). */
  function nivelNaDica() {
    const t = document.querySelector("#dica-item:not([hidden]) > b");
    if (!t || t.querySelector(".rf-n-dica")) return;
    const m = / \+(\d+)/.exec(t.textContent);
    if (!m || +m[1] < 1) return;
    const no = [...t.childNodes].find((x) => x.nodeType === 3 && x.textContent.includes(m[0]));
    if (!no) return;
    const i = no.textContent.indexOf(m[0]);
    const resto = no.splitText(i);
    resto.textContent = resto.textContent.slice(m[0].length);
    no.after(" ", Object.assign(document.createElement("span"), { className: "rf-n-dica", textContent: `+${m[1]}` }));
    t.querySelector(".rf-n-dica").dataset.nivel = Math.min(+m[1], 12);
  }
  function sulcosNoAchado() {
    const alvo = achado && document.querySelector("#sobre-achado :is(.ficha-premio, .ficha-grupo) > .ficha-linhas");
    if (!alvo || (alvo.nextElementSibling && alvo.nextElementSibling.classList.contains("rf-encantos"))) return;
    const sec = secaoEncantos(achado.encantos);
    if (sec) alvo.insertAdjacentHTML("afterend", sec);
  }
  const paineis = {};  // os últimos dados de cada painel (o mercado, o espólio...): as peças que não estão no estado
  const painelJogo = Telas.painel;
  Telas.painel = (m) => { if (m && m.tipo) paineis[m.tipo] = m.dados; return painelJogo(m); };
  /** A peça que um elemento mostra, pelo contexto dele: a forja (o id da peça), o Equipado e o Inventário (o espaço do
   *  personagem da aba ativa, a posição na bolsa, a opção com o dono), o mercado (a posição na lista da loja). Nunca
   *  pelo nome sozinho: duas peças de mesmo nome mostram cada uma os seus dados. */
  function pecaDoDono(dono) {
    const ds = (dono && dono.dataset) || {};
    const id = ds.uid || ds.peca;
    if (id && ultimoDesenho) { const x = ultimoDesenho.pecas.find((q) => q.uid === id); if (x) return { ...x.item, encantos: x.encantos, reforco: x.reforco }; }
    const heroi = App.estado && App.estado.heroi;
    if (!heroi) return null;
    if (ds.mini) return heroi.equip[ds.mini];
    const loja = paineis.loja;
    if (loja) {
      if (ds.comprarItem !== undefined) return (loja.equipamentos || [])[+ds.comprarItem];
      if (ds.mochilaLoja !== undefined) return (loja.mochila || [])[+ds.mochilaLoja];
      if (ds.recomprar !== undefined) return (loja.recompra || [])[+ds.recomprar];
    }
    if (ds.mochila !== undefined) return heroi.mochila[+ds.mochila];
    const inv = dono.closest && dono.closest(".tela.inventario");
    if (inv) {
      const aba = inv.querySelector(".grupo-aba.ativa");
      const quem = !aba || aba.dataset.aba === "heroi" ? heroi : (heroi.grupo || []).find((m) => m.id === aba.dataset.aba);
      if (ds.espaco && quem) return quem.equip[ds.espaco];
      if (ds.opcao !== undefined) {  // a opção de um espaço: o nome e o dono escritos nela ("na bolsa", "com Morel")
        const nome = dono.querySelector("span") ? dono.querySelector("span").firstChild.textContent : "";
        const onde = (dono.querySelector("small") || {}).textContent || "";
        if (onde === "na bolsa") return heroi.mochila.find((x) => x && x.nome === nome) || null;
        const dele = [heroi, ...(heroi.grupo || [])].find((m) => onde === `com ${m.id === "heroi" ? "você" : m.nome}`);
        return dele ? Object.values(dele.equip || {}).find((x) => x && x.nome === nome) || null : null;
      }
    }
    return null;
  }
  function sulcosNaDica() {
    const caixa = document.getElementById("dica-item");
    if (!caixa || caixa.hidden || caixa.querySelector(".rf-encantos")) return;
    const titulo = caixa.querySelector(":scope > b");
    if (!titulo) return;
    const it = pecaDoDono(caixa._dono);  // o achado usa a ficha do jogo (Telas.htmlItem), com a peça inteira
    const sec = it && secaoEncantos(it.encantos);
    if (sec) (caixa.querySelector(":scope > .bonus") || titulo).insertAdjacentHTML("afterend", sec);
  }

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
  new MutationObserver(() => { materiaisNoInventario(); sulcosNaDica(); sulcosNoAchado(); decorar(); }).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ["hidden"] });
})();
