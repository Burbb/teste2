/* Protótipo do reforço, 7ª versão (roadmapIDEIAS/25, 5.6): a A · Bancada com o reforço com chance, num eixo central e
   com as mesmas dimensões em todos os estados. A forja (painel "forja_proto", demo.py) e a seção "Materiais" do
   inventário. Só esta demonstração carrega este arquivo; o jogo não. As versões anteriores ficam em historico/.

   A bancada é sempre a mesma estrutura: o nível, a peça no molde, a chance e o Reforçar num eixo vertical; os
   materiais à esquerda e o ganho à direita, em colunas de largura igual (a largura deles não desloca a peça). Oferta,
   aquecimento, desfecho, falta, reforço máximo e peça sem reforço só mudam o conteúdo. A tentativa é resolvida uma vez
   pelo motor; a tela encena com os dados da tentativa (o nível, a chance, o custo pago, o ganho e, na ficha, os valores
   de antes), para nada contar o resultado nem a próxima oferta antes da hora. No impacto, o efeito em pixel das
   celebrações (FX, o do Estouro) sai da peça e passa da bancada; "SUCESSO", o +N e o ganho formam um conjunto junto
   dela; na falha, "FALHOU" e a queda, sóbrios. A peça reforçada tem um reflexo diagonal pela cor do nível. */
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
  let pago = null;         // a tentativa pedida, como a oferta a mostrava: {de, chance, linhas, ouro, fragmentos}
  let brilharSel = false;  // a peça acabou de ser escolhida: o reflexo passa uma vez no molde
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

  /** A tentativa em cena desta peça (o resultado do motor), ou null. */
  const emCena = (p, u) => (u && u.tipo === "reforco" && u.uid === p.uid && cena && cena.id === u.id && fase() ? u : null);
  /** Um valor que muda com a tentativa: o de antes (no aquecimento) e o de agora (do desfecho em diante), trocados
   *  pela classe "aquecendo" da janela, sem redesenhar. */
  const antesAgora = (antes, agora) => `<span class="rf-v-antes">${antes}</span><span class="rf-v-agora">${agora}</span>`;

  /** Um encaixe da esteira: o ícone, o +N no canto e, ao desmontar, o material que rende (ícone e quantidade). */
  function encaixe(p, u) {
    const reforco = janela === "reforcar";
    const apagada = reforco ? !!p.sem_reforco : !!p.desmontar.motivo;
    const t = reforco ? emCena(p, u) : null;
    let canto = "";
    if (t) canto = `<span class="rf-canto${t.de ? "" : " sem-antes"}${p.reforco ? "" : " sem-agora"}">${antesAgora(`+${t.de}`, `+${p.reforco}`)}</span>`;
    else if (reforco) canto = p.reforco ? `<span class="rf-canto">+${p.reforco}</span>` : "";
    else canto = p.desmontar.motivo ? "" : `<span class="rf-canto mat">${Icones.porDesenho("saco", 16) || S("saco", 1)}×${p.desmontar.total}</span>`;
    return `<button type="button" class="rf-peca r-${h(p.item.raridade)}${p.uid === selUid ? " marcada" : ""}${apagada ? " apagada" : ""}" data-uid="${h(p.uid)}"
      data-reforco="${reforco ? p.reforco : 0}" aria-label="${h(p.item.nome)}" aria-pressed="${p.uid === selUid}" ${t ? "" : dicaItem(p.item, "", false)}>${iconePeca(p.item)}${canto}</button>`;
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
    const u = d.ultimo && d.ultimo.id === mostrarId ? d.ultimo : null;
    const esteira = lista.map((x) => encaixe(x, u)).join("")
      || `<span class="rf-vazio-texto">${reforco ? "Nada aqui." : "Nenhuma peça da bolsa rende material."}</span>`;
    const chapa = reforco ? chapaReforco(p, u) : !p ? chapaVazia() : chapaDesmonte(p);
    // no reforço, o resultado é a cena na própria bancada; a placa fica só para a desmontagem
    return `<div class="rf-corpo">${donos}<section class="rf-centro"><div class="rf-mesa">${reforco ? "" : placa(u, p)}${chapa}</div>
        <div class="rf-esteira" role="listbox" aria-label="Peças">${esteira}</div></section>
      <aside class="rf-ficha">${p ? ficha(p, u) : ""}</aside></div>`;
  }

  /** A placa da desmontagem: altura fixa acima da bancada (nada se desloca quando ela muda); com a seleção vazia, o
   *  que a última desmontagem rendeu, até a próxima ação. */
  function placa(u, p) {
    let txt = "";
    if (u && u.tipo === "desmonte" && !p) {
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
        <div class="rf-encaixe grande${p ? ` r-${h(p.item.raridade)}` : " vazio"}"${p ? ` data-reforco="${p.reforco || 0}"` : ""}>${p ? iconePeca(p.item) : ""}</div>
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
  /** O desfecho: um conjunto junto da peça. No sucesso, "Sucesso", o +N e o ganho; na falha, "Falhou", a queda e o
   *  que se perdeu, sóbrios (o nível que ficou não pode parecer prêmio). */
  function desfecho(u) {
    const ganho = u.linhas.map((l) => `<span>${h(l.nome)} ${l.antes} → <em>${l.depois}</em></span>`).join("");
    return u.sucesso
      ? `<div class="rf-dsf ok"><b class="rf-dsf-palavra">Sucesso</b><b class="rf-dsf-nivel">+${u.para}</b>${ganho ? `<small>${ganho}</small>` : ""}</div>`
      : `<div class="rf-dsf mau"><b class="rf-dsf-palavra">Falhou</b><b class="rf-dsf-nivel">+${u.de} → +${u.para}</b>${ganho ? `<small>${ganho}</small>` : ""}</div>`;
  }

  /** A bancada do reforço: a mesma estrutura em todos os estados (oferta, cena, falta, máximo, peça sem reforço, sem
   *  peça), para a peça e o Reforçar não mudarem de lugar. O nível, a peça, a chance e o botão no eixo do meio; os
   *  materiais e o ganho nas colunas dos lados, de largura igual. */
  function bancada({ p, classe = "", nivel = "", marcasDe, esq, dir, dsf = "", chance = "", ajudas = [], botao = "Reforçar", trava = "", nota = "", neutra = false }) {
    const m = p ? marcas({ ...p, reforco: marcasDe ?? p.reforco }) : marcas({ reforco: 0, limite: 4 });
    return `<div class="rf-chapa${classe}">
      <div class="rf-leito"><div class="rf-lado esq">${esq}${conduto(false)}</div>
        ${molde(p, m, `<span class="rf-nivel">${nivel}</span>`)}
        <div class="rf-lado dir">${conduto(true)}${dir}${dsf}</div></div>
      <div class="rf-pe-chapa"><div class="rf-linha-chance">${chance}${ajuda(ajudas)}</div>
        <button type="button" class="rf-botao principal" data-reforcar${trava ? ` aria-disabled="true"${trava === true ? "" : ` title="${h(trava)}"`}` : ""}>${botao}</button>
        <span class="rf-nota${neutra ? " neutra" : ""}">${h(nota)}</span></div></div>`;
  }
  const semCusto = () => insumos();
  const chanceHtml = (c) => (c >= 100 ? `<span class="rf-chance">Sucesso garantido</span>` : `<span class="rf-chance">Sucesso <b>${c}%</b></span>`);

  function chapaReforco(p, u) {
    if (!p) return bancada({ p: null, esq: semCusto(), dir: visor([]), trava: "Escolha uma peça", nota: "Escolha uma peça", neutra: true });
    // a cena: tudo da tentativa, como a oferta mostrava antes do clique (o motor já resolveu e já calculou a próxima)
    const t = emCena(p, u);
    if (t) {
      const x = cena.pago || { de: t.de, chance: 0, linhas: [] };
      const classe = ` forjando ${t.sucesso ? "ok" : "falhou"}${fase() === "desfecho" ? " desfecho" : ""}${t.sucesso && t.para >= 3 ? " forte" : ""}`;
      return bancada({ p, classe, nivel: `+${t.de} → +${t.de + 1}`, marcasDe: t.de, esq: insumos(x.ouro, Infinity, x.fragmentos, Infinity),
        dir: visor(x.linhas), dsf: desfecho(t), chance: chanceHtml(x.chance), trava: true });
    }
    if (p.no_limite) {
      return bancada({ p, nivel: `+${p.reforco}`, esq: semCusto(), dir: visor([]), botao: "Reforço máximo", trava: true });
    }
    if (p.sem_reforco) {
      return bancada({ p, esq: semCusto(), dir: visor([]), trava: true, nota: p.sem_reforco, neutra: true });
    }
    const passo = passoDe(p);
    const custo = passo || p.passos[0];  // o custo e a chance são os mesmos nos dois caminhos
    const escolha = p.passos.length > 1;
    const dir = escolha
      ? `<div class="rf-resultado veios" role="radiogroup" aria-label="Atributo que a arma reforça">${p.passos.map((x) => `<button type="button" role="radio" class="rf-veio${veioSel[p.uid] === x.veio ? " escolhido" : ""}" data-veio="${x.veio}" aria-checked="${veioSel[p.uid] === x.veio}">
          ${x.linhas.map(linhaGanho).join("")}</button>`).join("")}</div>`
      : visor(passo.linhas);
    const ajudas = [];
    if (custo.chance < 100) ajudas.push(`Se falhar: +${p.reforco} → +${custo.falha}. O equipamento não quebra.`);
    ajudas.push("A tentativa custa o mesmo, dê certo ou não.");
    if (escolha) ajudas.push("O atributo escolhido fica com a arma, mesmo se ela voltar a +0.");
    const motivo = !passo ? "Escolha o atributo" : passo.motivo;
    return bancada({ p, nivel: `+${p.reforco} → +${p.reforco + 1}`, esq: insumos(custo.ouro, custo.ouro_tem, custo.fragmentos, custo.tem), dir,
      chance: chanceHtml(custo.chance), ajudas, trava: motivo || "", nota: motivo || "", neutra: !passo });
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

  /** O efeito do desfecho, em pixel (FX das celebrações): no sucesso, o selo de raios atrás do molde, o halo intenso
   *  em volta da peça, um anel curto e os estilhaços, que passam do leito, da chapa e um pouco da moldura da janela
   *  (mais fortes no +3 e no +4, com a chapa tremendo); na falha, um anel fraco que apaga e cinzas caindo. O recorte é a
   *  janela com uma margem (nada na tela inteira); a peça, o desfecho, o pé da bancada e a ficha ficam por cima do
   *  efeito, e o canvas não recebe cliques. `desde`: quanto do desfecho já passou (um redesenho no meio). */
  function efeito(jan, u, desde = 0) {
    pararFx();
    if (typeof FX === "undefined") return;
    const leito = jan.querySelector(".rf-chapa .rf-leito"), alvo = jan.querySelector(".rf-chapa .rf-encaixe.grande");
    if (!leito || !alvo) return;
    palco = FX.palco(jan, { z: 2, classe: "rf-fx" });
    const r = jan.getBoundingClientRect(), folga = 22;
    palco.el.style.clipPath = `inset(${Math.max(0, r.top - folga)}px ${Math.max(0, innerWidth - r.right - folga)}px ${Math.max(0, innerHeight - r.bottom - folga)}px ${Math.max(0, r.left - folga)}px)`;
    const enx = FX.enxame(), forte = u.sucesso && u.para >= 3, grupo = jan.querySelector(".rf-chapa .rf-dsf");
    const pal = forte ? FX.PALETAS.lendario : ["W", "Y", "O", "o", "C"];
    if (u.sucesso && forte && !desde) tremerChapa(leito.closest(".rf-chapa"), 3);
    ctl = FX.animar(palco, (t, q, parado) => {
      const a = palco.de(alvo), R = Math.max(a.rx, a.ry);
      if (u.sucesso) {
        const re = R + palco.t(forte ? 46 : 34);
        const vis = parado ? 12 : Math.round(FX.rampa(t, 500, 700, 16, 11));
        FX.raios(palco, { cx: a.x, cy: a.y, n: 18, ang: 0.15 + (parado ? 0 : q * 0.012), larg: 0.32, r0: R, r1: Math.round(re * (forte ? 3.4 : 2.6)), pal: pal.slice(1), esbate: 0.3, achata: 0.72, alterna: 0.62, vis });
        FX.estrela(palco, { cx: a.x, cy: a.y, pontas: 14, ri: R + 2, re, pal, cores: ["z", "o", "O", "Y"] });
        // um poço escuro atrás do conjunto do resultado: os raios e o selo passam por trás da leitura sem disputar com ela
        if (grupo) { const g = palco.de(grupo); FX.poco(palco, { cx: g.x, cy: g.y, rx: g.rx + palco.t(14), ry: g.ry + palco.t(10), forca: 14 }); }
        if (parado) return;
        // o clarão intenso só em volta da peça (sem o pontilhado na área inteira) e um anel achatado, que não desce até a chance
        FX.claraoLocal(palco, { cx: a.x, cy: a.y, r: R + palco.t(forte ? 30 : 24), t, dur: forte ? 200 : 160, espalha: 0 });
        if (t < 420) FX.anel(palco, { cx: a.x, cy: a.y, r: re + Math.round(FX.rampa(t, 0, 400) * palco.t(forte ? 70 : 50)), esp: 2, pal: ["W", pal[1], pal[2]], achata: 0.6, rastro: 3, vis: Math.round(14 * (1 - t / 420)) });
        if (q === 1) enx.soltar(forte ? 42 : 24, (i) => {
          const ang = FX.aleatorio(0, Math.PI * 2), v = FX.aleatorio(3, 7.5) * (forte ? 1.25 : 0.95);
          return { x: a.x + Math.cos(ang) * re * 0.8, y: a.y + Math.sin(ang) * re * 0.7, vx: Math.cos(ang) * v, vy: Math.sin(ang) * v - 2, g: 0.36, arrasto: 0.97,
            vida: Math.round(FX.aleatorio(18, 32)), desenho: ["lasca", "caco", "cruz", "duplo"][i % 4], pal: ["W", "Y", "O", "o", "r"], piscar: i % 5 === 0 };
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
    jan.classList.add("em-cena", "revelou");
    jan.classList.remove("aquecendo");  // a ficha, o nome e o +N da esteira passam ao resultado
    efeito(jan, u, cena && !reduzido() ? Math.max(0, performance.now() - cena.t0 - IMPACTO) : 0);
    if (u.sucesso) relogios.push(setTimeout(() => reflexo(jan.querySelector(".rf-chapa .rf-encaixe.grande"), u.para, true), reduzido() ? 0 : 280));
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
    jan?.classList.remove("em-cena", "aquecendo", "revelou");
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
    if (parado && ja && ja.classList.contains("passa") && ja.dataset.nivel === String(Math.min(nivel, 4))) return;
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
    r.dataset.nivel = Math.min(nivel, 4);
    r.classList.remove("passa");
    void r.offsetWidth;  // recomeça a passada
    r.classList.add("passa");
  }
  function apagarReflexo() {}  // parado (movimento reduzido), o reflexo fica: é o acabamento da peça reforçada
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
     horário de cada uma fica guardado pelo lugar dela, para um redesenho da tela não recomeçar a espera. Durante a cena
     do reforço, todas esperam (a cor do nível novo não pode aparecer antes do desfecho). Só nesta demonstração. */
  const PRIMEIRA = 2000, PERIODO = 3000, DEFASAGEM = 450;
  const agenda = new Map();  // lugar → {proxima, visto}
  const nivelDoNome = (nome) => { const m = / \+(\d+)$/.exec(nome || ""); return m ? +m[1] : 0; };
  function pecasReforcadas() {
    const lista = [];
    const heroi = App.estado && App.estado.heroi;
    document.querySelectorAll(".slot-px.mini[data-mini]").forEach((el) => {
      const it = heroi && heroi.equip && heroi.equip[el.dataset.mini];
      lista.push([el, `mini:${el.dataset.mini}:${it ? it.nome : ""}`, nivelDoNome(it && it.nome)]);
    });
    document.querySelectorAll(".tela.inventario .slot-px[aria-label]").forEach((el) => {
      const nome = el.getAttribute("aria-label").replace(/^[^:]*: /, "");
      lista.push([el, `inv:${el.dataset.espaco || "m" + el.dataset.mochila}:${nome}`, nivelDoNome(nome)]);
    });
    document.querySelectorAll(".tela.inventario .peca-opcao").forEach((el, i) => {
      const nome = el.querySelector("span") ? el.querySelector("span").firstChild.textContent : "";
      lista.push([el, `opcao:${i}:${nome}`, nivelDoNome(nome)]);
    });
    document.querySelectorAll(".rf-janela .rf-esteira .rf-peca, .rf-janela .rf-chapa .rf-encaixe.grande[data-reforco]").forEach((el) => {
      lista.push([el, `forja:${el.dataset.uid || "molde"}:${el.getAttribute("aria-label") || ""}:${el.dataset.reforco}`, +el.dataset.reforco || 0]);
    });
    return lista.filter((x) => x[2] > 0);
  }
  function ciclo() {
    if (fase()) return;  // durante a cena, nenhuma peça brilha (nem a da ficha lateral, que já tem o nome novo)
    const agora = performance.now();
    pecasReforcadas().forEach(([el, lugar, n], i) => {
      let a = agenda.get(lugar);
      if (!a || agora - a.visto > 8000) {  // apareceu (ou voltou depois de um tempo fora): a espera de 2 s
        a = { proxima: agora + PRIMEIRA + (i % 8) * DEFASAGEM };
        agenda.set(lugar, a);
      }
      a.visto = agora;
      if (reduzido()) { reflexo(el, n, true, true); return; }  // parado, sempre à vista
      if (agora >= a.proxima) { reflexo(el, n, true); a.proxima = agora + PERIODO + (i % 3) * 150; }
    });
  }
  setInterval(ciclo, 200);

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
    const p0 = janela === "reforcar" ? d.pecas.find((x) => x.uid === selUid && x.aba === aba) : null;
    comparacao = p0 && !p0.no_limite && !p0.sem_reforco ? teste(p0, passoDe(p0)) : "";
    limparRelogios();
    pararFx();
    if (f) {
      jan.classList.add("em-cena");
      const e = performance.now() - cena.t0;
      if (f === "forja") {
        jan.classList.add("aquecendo");
        relogios.push(setTimeout(() => entrarDesfecho(u), IMPACTO - e));
        relogios.push(setTimeout(assentar, IMPACTO + SEGURA - e));
      } else {
        // um quadro depois: a janela recém-desenhada já está na página e no lugar (o efeito mede a peça)
        requestAnimationFrame(() => entrarDesfecho(u));
        relogios.push(setTimeout(assentar, (reduzido() ? SEGURA : IMPACTO + SEGURA) - e));
      }
    } else if (brilharSel) {
      brilharSel = false;
      const sel = p0 && jan.querySelector(".rf-chapa .rf-encaixe.grande");
      if (sel) requestAnimationFrame(() => reflexo(sel, p0.reforco));
    }
    ligarReflexos(jan);
    window.dispatchEvent(new Event("reforco-comparacao"));
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
      if (selUid !== b.dataset.uid) { selUid = b.dataset.uid; confirmando = null; brilharSel = true; limpar(); redesenhar(`[data-uid="${b.dataset.uid}"]`); }
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
      pago = { de: p.reforco, chance: x.chance, linhas: x.linhas, ouro: x.ouro, fragmentos: x.fragmentos };
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
  // e mostra a comparação de teste da peça escolhida (um controle de laboratório, fora da tela do jogador)
  let comparacao = "";
  window.ReforcoProto = {
    teste(modo) { if (modo !== undefined) testeProximo = modo || null; return testeProximo; },
    comparacao: () => comparacao,
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
