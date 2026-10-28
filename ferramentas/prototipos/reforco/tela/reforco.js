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
  /* A desmontagem (18ª): a peça se desfaz (0 a 260 ms), os fragmentos voam até o encaixe do material e chegam entre
     DESMONTE_CHEGA e ~640 ms, o +N e o saldo novo acendem na chegada, e aos DESMONTE_MS a bancada assenta parada. */
  const DESMONTE_MS = 1000, DESMONTE_CHEGA = 440;
  let essSel = null;          // a essência escolhida no trilho (fica entre as peças)
  let sulcoSel = 0, sulcoDe = null;  // o sulco escolhido (e de que peça: outra peça começa no primeiro vazio)
  let confirmandoGrav = null; // {uid}: a substituição pedida, esperando a confirmação
  let confirmandoRem = null;  // {uid, sulco}: a remoção pedida (18ª), esperando a confirmação
  let removido = null;        // {id, uid, sulco, t0, cor}: a gravação que acabou de sair (o sulco apaga uma vez)
  let trOrigem = null, trDestino = null;  // a transferência: as duas peças escolhidas (pelos seletores)
  let trSeletor = null;        // "origem" ou "destino": o seletor aberto
  let trAviso = "";            // o destino limpo quando a origem nova não o aceita (dito uma vez)
  let confirmandoTransf = null; // {origem, destino}: a transferência pedida, esperando a confirmação
  let transf = null;           // {id, t0, fim, u}: a cena da última transferência (já resolvida pelo motor)
  const TRANSF_MS = 1400;      // a luz sai da origem, percorre o conduto e chega ao destino; depois o resultado até o OK
  function faseTransf() {
    if (!transf || transf.fim) return "";
    if (reduzido()) return "resultado";
    return performance.now() - transf.t0 < TRANSF_MS ? "anim" : "resultado";
  }
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
  /* As candidatas visuais desta rodada, escolhidas no painel de testes (carregar.js) e lembradas neste navegador:
     o acabamento das armaduras do +9 ao +12 (18ª: A · passadas alternadas, B · cor gradual, C · reflexo principal e
     secundário; o feixe da 17ª e o veio anterior para comparar), a paleta da celebração do +9 ao +12 e a interface de
     metal da bancada (18ª; "jogo" é a de agora). Nenhuma é escolhida pelo jogo: só a comparação. */
  const PREF = { botoes: ["a"], armadura: ["a", "b", "c", "feixe", "anterior"], paleta: ["candidata", "anterior", "referencia13"], placas: ["jogo", "bancada"] };
  const pref = (k) => { let v = null; try { v = localStorage.getItem(`rf16-${k}`); } catch (e) { /* sem armazenamento */ } return PREF[k].includes(v) ? v : PREF[k][0]; };
  function preferir(k, v) {
    if (!PREF[k] || !PREF[k].includes(v)) return pref(k);
    try { localStorage.setItem(`rf16-${k}`, v); } catch (e) { /* sem armazenamento: vale até recarregar */ }
    aplicarPref();
    return v;
  }
  function aplicarPref() {
    document.body.dataset.rfBotoes = pref("botoes");
    document.body.dataset.rfArmadura = pref("armadura");
    document.body.dataset.rfPaleta = pref("paleta");
    document.body.dataset.rfPlacas = pref("placas");
  }
  aplicarPref();
  const iconeDe = (nome) => Icones.porDesenho(nome) || S(nome, 2);
  /** O símbolo da essência com o tier no canto de cima à direita (I, II, III); a quantidade, quando há, fica em outro
   *  canto, fora do símbolo (o tier III e três unidades não se confundem). */
  const icEss = (x) => `<span class="rf-ess-ic" style="--ess:${h(x.cor)}">${iconeDe(x.icone)}<span class="rf-tier-selo">${x.numeral}</span></span>`;
  /** "Requer nível 9", na cor de falta quando quem está na tela não chega lá (o herói e os companheiros crescem juntos). */
  const nivelGrupo = () => (App.estado && App.estado.heroi && App.estado.heroi.nivel) || 1;
  const reqHtml = (req) => (req > 1 ? `<div class="rf-req${req > nivelGrupo() ? " falta" : ""}">Requer nível ${req}</div>` : "");
  const moeda = () => Icones.moeda() || S("moeda", 1);
  const num = (v) => String(v).replace(".", ",");
  const iconePeca = (it) => Icones.equipamento(iconeItem(it)) || S(iconeItem(it), 2);
  const retrato = (a) => (a.retrato ? Icones.cabeca(a.retrato, 32) || S(a.retrato, 2) : iconeDe("saco"));
  const valor = (pr, v) => (pr.pct ? `${v}%` : `${v}`);
  const dono = (p) => (p.quem ? `Com ${p.onde}` : "Bolsa do grupo");
  const marcas = (p) => `<span class="rf-marcas" aria-label="Reforço +${p.reforco} de ${p.limite}">${Array.from({ length: p.limite }, (_, i) =>
    `<i class="${i < p.reforco ? "cheia" : ""}"></i>`).join("")}</span>`;
  const fragmentos = (n) => `<span class="rf-material">${iconeDe("saco")}<span>Fragmento de Têmpera <b>×${n}</b></span></span>`;

  // ------------------------------------------------------------------ os formatos comuns das telas da forja (16ª)
  /* Um formato por tipo de informação, igual nas quatro abas (a skill texto-regras-fenda, "Formatos comuns"):
     - o que a operação consome: "Requer:" e cada material como disponível/necessário ("14/2"), a falta em vermelho no
       próprio valor; a dica (mouse e foco) diz a ordem dos números e quanto falta. O nível, quando é requisito da
       operação, entra no mesmo grupo ("Nível 5", vermelho quando impede);
     - o ouro: só no botão da ação, numa área reservada à direita (o saldo fica no cabeçalho);
     - a confirmação: a ação principal não sai do lugar; a pergunta aparece em cima e o Cancelar num espaço já
       reservado ao lado. */
  function requerHtml(lista) {
    const itens = (lista || []).filter(Boolean);
    if (!itens.length) return `<div class="rf-requer vazio" aria-hidden="true"></div>`;
    return `<div class="rf-requer" role="group" aria-label="Requer"><span class="rf-requer-rot">Requer:</span>${itens.map((x) => {
      const nivel = x.id === "nivel", titulo = nivel ? x.valor : x.nome;
      const ic = nivel ? "" : `<span class="rf-encaixe pequeno">${x.numeral ? icEss(x) : iconeDe(x.icone)}</span>`;
      return `<span class="rf-req-item${x.falta ? " falta" : ""}${nivel ? " nivel" : ""}" tabindex="0" ${Telas.dica(`<b>${h(titulo)}</b><div>${h(x.dica)}</div>`, true)}
        aria-label="${h(titulo)}: ${h(x.dica)}">${ic}<b>${h(x.valor)}</b></span>`;
    }).join("")}</div>`;
  }
  /** O botão de uma ação: o nome na área principal e, nas pagas, a moeda e o valor numa área reservada à direita (o
   *  valor não empurra o nome nem muda a largura). `preco`: o número, "" (a área reservada vazia: sem peça) ou null
   *  (ação sem preço). `falta`: o ouro não chega (o valor em vermelho; o motivo no title e no aria). */
  function botaoAcao({ rotulo, preco = null, falta = false, attrs = "", classe = "principal", motivo = "" }) {
    const pago = preco !== null;
    const area = pago ? `<span class="rf-bp-preco${falta ? " falta" : ""}"${preco === "" ? ' aria-hidden="true"' : ""}>${preco === "" ? "" : `${moeda()}<b>${preco}</b>`}</span>` : "";
    const aria = pago && preco !== "" ? ` aria-label="${h(rotulo.replace(/<[^>]+>/g, ""))}, ${preco} de ouro${motivo ? `. ${h(motivo)}` : ""}"` : "";
    return `<button type="button" class="botao-janela rf-botao ${classe}${pago ? " com-preco" : ""}" ${attrs}${motivo ? ` aria-disabled="true" title="${h(motivo)}"` : ""}${aria}><span class="rf-bp-rot">${rotulo}</span>${area}</button>`;
  }
  /** O pé de uma ação: [o que ela consome] [ação principal, no eixo] [Cancelar reservado], a pergunta em cima e a nota
   *  embaixo, cada um com a altura guardada. Pedir a confirmação só revela a pergunta e o Cancelar: a ação fica onde
   *  estava (as duas laterais têm a mesma largura, então nada se recentra). */
  function peAcao({ principal, esquerda = "", cancelar = "", pergunta = "", nota = "", neutra = true }) {
    return `<div class="rf-pe-fixo${pergunta ? " confirmando" : ""}"${pergunta ? ` role="alertdialog" aria-label="${h(pergunta.replace(/<[^>]+>/g, ""))}"` : ""}>
      <div class="rf-pe-pergunta">${pergunta}</div>
      <div class="rf-pe-botoes"><span class="rf-pe-esq">${esquerda}</span>${principal}<span class="rf-pe-cancelar">${cancelar}</span></div>
      <span class="rf-nota${neutra ? " neutra" : ""}">${nota}</span></div>`;
  }
  const cancelarBtn = (attr) => `<button type="button" class="botao-janela rf-botao" ${attr}><span class="rf-bp-rot">Cancelar</span></button>`;

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
      if (d.ultimo.tipo === "transfere") transf = { id: d.ultimo.id, t0: performance.now(), fim: false, u: d.ultimo };
      if (d.ultimo.tipo === "remove") removido = { id: d.ultimo.id, uid: d.ultimo.uid, sulco: d.ultimo.sulco, t0: performance.now(), cor: d.ultimo.de && d.ultimo.de.cor };
      if (d.ultimo.tipo === "encanto") gravando = { id: d.ultimo.id, t0: performance.now(), uid: d.ultimo.uid, sulco: d.ultimo.sulco, de: d.ultimo.de, para: d.ultimo.para };
    }
  }
  function balcao(d) {
    receber(d);
    const cartoes = [
      cartaoServico({ icone: "martelo", nome: "Reforçar", efeito: "Todo equipamento, do +1 ao +12", attrs: 'data-servico="reforcar"' }),
      cartaoServico({ icone: "livro", nome: "Encantar", efeito: "Grava essências nos sulcos da peça", attrs: 'data-servico="encantar"' }),
      cartaoServico({ icone: "saco", nome: "Desmontar", efeito: "Peças da bolsa → Fragmentos de Têmpera", attrs: 'data-servico="desmontar"' }),
      cartaoServico({ icone: "martelo", nome: "Transferir", efeito: "O reforço de uma peça para outra do mesmo tipo", attrs: 'data-servico="transferir"' }),
    ];
    return `<div class="tela balcao-servico forja forja-proto">${topoBalcao("martelo", "O ferreiro", "Um homem sem dois dedos cospe na forja. \"Ouro primeiro.\"", d.ouro)}
      <div class="servicos rf-servicos">${cartoes.join("")}</div>${janela ? janelaHtml(d) : ""}</div>`;
  }

  // ------------------------------------------------------------------ a janela
  function janelaHtml(d) {
    const abas = [["reforcar", "Reforçar"], ["encantar", "Encantar"], ["transferir", "Transferir"], ["desmontar", "Desmontar"]].map(([id, nome]) =>
      `<button type="button" role="tab" class="rf-servico${id === janela ? " ativo" : ""}" data-janela="${id}" aria-selected="${id === janela}">${nome}</button>`).join("");
    // no cabeçalho, só o ouro (comum aos quatro serviços); os materiais aparecem junto da operação que os consome
    const recursos = `<div class="rf-recursos"><span class="rf-rec" data-rec="ouro" title="Ouro">${Icones.ouro() || S("moedas", 2)}<b>${d.ouro}</b></span></div>`;
    const rotulo = { reforcar: "Reforçar", desmontar: "Desmontar", encantar: "Encantar", transferir: "Transferir" }[janela];
    // a janela nasce no lugar da anterior: sem isso, num redesenho ela passa um quadro fora do lugar, e o segundo clique
    // de um clique duplo atravessava para o balcão atrás dela (o cartão Desmontar)
    const pos = ultimaPos ? ` style="left:${ultimaPos.left};top:${ultimaPos.top};width:${ultimaPos.width};height:${ultimaPos.height}"` : "";
    return `<div class="rf-janela m-janela${janela === "encantar" ? " rf-encantar" : ""}" role="dialog" aria-modal="true" aria-label="${rotulo}"${pos}>
      <header class="rf-cab"><nav class="rf-servicos-abas" role="tablist">${abas}</nav>${recursos}
        <button type="button" class="botao-janela rf-botao fechar" data-fechar><span class="rf-bp-rot">Fechar <kbd>Esc</kbd></span></button></header>${corpo(d)}</div>`;
  }

  /** A tentativa em cena desta peça (o resultado do motor), ou null. */
  const emCena = (p, u) => (u && u.tipo === "reforco" && u.uid === p.uid && cena && cena.id === u.id && fase() ? u : null);
  /** Um valor que muda com a tentativa: o de antes (no aquecimento) e o de agora (do desfecho em diante), trocados
   *  pela classe "aquecendo" da janela, sem redesenhar. */
  const antesAgora = (antes, agora) => `<span class="rf-v-antes">${antes}</span><span class="rf-v-agora">${agora}</span>`;

  /** Um encaixe da esteira: o ícone, o +N no canto e, ao desmontar, o material que rende (ícone e quantidade). */
  function encaixe(p, u) {
    const reforco = janela !== "desmontar";  // o +N no canto (o reforço e o encantamento são por dono)
    const apagada = janela === "reforcar" ? !!p.sem_reforco : janela === "encantar" ? !!p.encantar.motivo
      : janela === "transferir" ? !p.transferir.destinos.some((x) => !x.motivo) : !!p.desmontar.motivo;
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
   *  o símbolo da essência e o tier no canto. Com `sel` (a forja), cada um é um botão: escolher onde gravar. */
  function filaSulcos(lista, sel = null) {
    return (lista || []).map((x, i) => {
      const cor = x ? ` style="--ess:${h(x.cor)}"` : "";
      const dentro = x ? iconeDe(x.icone) + `<span class="rf-sq-tier">${x.numeral}</span>` : "";
      if (sel === null) return `<i class="rf-sq${x ? "" : " vazio"}"${cor} title="${x ? h(x.titulo) : "Sulco vazio"}">${dentro}</i>`;
      return `<button type="button" role="radio" class="rf-sq${x ? "" : " vazio"}${i === sel ? " escolhido" : ""}" data-sulco="${i}" aria-checked="${i === sel}"
        aria-label="Sulco ${i + 1}: ${x ? h(x.titulo) : "vazio"}"${cor} ${Telas.dica(x ? `<b>${h(x.titulo)}</b><div>${h(x.efeito)}</div>${x.limite ? `<div class="rodape">${h(x.limite)}</div>` : ""}` : "<b>Sulco vazio</b>", true)}>${dentro}</button>`;
    }).join("");
  }
  /** Os efeitos que a peça fornece, um por essência (as repetidas somadas pelo motor, até o limite do efeito): o nome
   *  com os tiers, pequeno, numa linha; embaixo, o gatilho, o efeito e o limite. É a descrição da peça, igual na bolsa e
   *  no corpo: o total de quem veste aparece na prévia do Encantar, não aqui. */
  function efeitosGravacao(lista, efeitos) {
    return (efeitos || []).map((f) => {
      // as gravações desta essência, do tier maior ao menor: iguais com ×N ("Brasa I ×2"), diferentes somadas
      // ("Brasa II + Brasa I"); cada sulco continua inspecionável na fila de cima
      const conta = new Map();
      (lista || []).filter((x) => x && x.essencia === f.id).forEach((x) => conta.set(x.tier, { x, n: (conta.get(x.tier)?.n || 0) + 1 }));
      const nome = [...conta.values()].sort((a, b) => b.x.tier - a.x.tier).map(({ x, n }) => `${h(x.titulo)}${n > 1 ? ` ×${n}` : ""}`).join(" + ");
      return `<div class="rf-ef" style="--ess:${h(f.cor)}"><span class="rf-ef-nome">${nome || h(f.nome)}</span>
        <span class="rf-ef-txt">${h(f.efeito)}${f.limite ? ` <span class="lim">${h(f.limite)}</span>` : ""}${f.excede ? ` <small class="rf-ef-teto">Limite ${h(f.teto)}.</small>` : ""}</span></div>`;
    }).join("");
  }
  /** O complemento, fora da leitura principal (clique e teclado; nas dicas, que somem, não aparece): uma frase por
   *  efeito com a condição ou a interação que muda a decisão, e o limite da repetição. */
  function detalhesGravacao(efeitos) {
    if (!(efeitos || []).length) return "";
    return `<details class="rf-detalhes"><summary>Detalhes</summary><ul>${efeitos.map((f) => `<li style="--ess:${h(f.cor)}"><b>${h(f.nome)}:</b> ${h(f.nota || "")} Repetida, soma até ${h(f.teto)}.</li>`).join("")}
      <li>Só vale na peça vestida.</li></ul></details>`;
  }
  /** A seção dos sulcos de uma ficha: os encaixes (os vazios também; o tier no canto) e, embaixo, os efeitos da peça e
   *  os detalhes. Vazia quando a peça não tem sulcos. */
  function secaoEncantos(lista, efeitos, detalhes = true) {
    if (!Array.isArray(lista) || !lista.length) return "";
    const n = lista.length, k = lista.filter(Boolean).length;
    return `<div class="rf-encantos"><div class="rf-encantos-cab"><span>Sulcos</span><span class="rf-sq-fila" aria-label="${n} ${n > 1 ? "sulcos" : "sulco"}, ${k} ${k === 1 ? "gravado" : "gravados"}">${filaSulcos(lista)}</span></div>
      ${efeitosGravacao(lista, efeitos)}${detalhes ? detalhesGravacao(efeitos) : ""}</div>`;
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
    // a transferência escolhe as duas peças nos seletores da própria bancada (sem a esteira nem as abas de dono)
    if (janela === "transferir") {
      return `<div class="rf-corpo sem-ficha so-mesa"><section class="rf-centro"><div class="rf-mesa">${chapaTransfere(d, u)}</div></section></div>`;
    }
    const chapa = janela === "reforcar" ? chapaReforco(p, u) : janela === "encantar" ? chapaEncanto(p, u, d) : chapaDesmonte(p, u, d);
    // a ficha completa da peça fica na inspeção (a dica do molde e da esteira, por mouse e teclado), não numa coluna
    return `<div class="rf-corpo sem-ficha">${donos}<section class="rf-centro"><div class="rf-mesa">${chapa}</div>
        <div class="rf-esteira" role="listbox" aria-label="Peças">${esteira}</div></section></div>`;
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
  function bancada({ p, classe = "", nivel = "", marcasDe, esq, dir, dsf = "", chance = "", falha = "", ajudas = [], botao = "Reforçar", trava = "", nota = "", neutra = false, titulo = "", dicaPeca = true, preco = "", faltaOuro = false }) {
    const m = p ? marcas({ ...p, reforco: marcasDe ?? p.reforco }) : marcas({ reforco: 0, limite: 4 });
    return `<div class="rf-chapa${titulo ? " com-titulo" : ""}${classe}">${titulo || ""}
      <div class="rf-leito"><div class="rf-lado esq">${esq}${conduto(false)}</div>
        ${molde(p, m, nivel === null ? "" : `<span class="rf-nivel">${nivel}</span>`, dicaPeca)}
        <div class="rf-lado dir">${conduto(true)}${dir}${dsf}</div></div>
      <div class="rf-pe-chapa"><div class="rf-linha-chance">${chance}${ajuda(ajudas)}</div>${titulo ? `<span class="rf-falha">${falha}</span>` : ""}
        <div class="rf-acao">${botaoAcao({ rotulo: botao, preco, falta: faltaOuro, attrs: `data-reforcar${trava === true ? ' aria-disabled="true"' : ""}`, motivo: trava === true ? "" : trava })}</div>
        <span class="rf-nota${neutra ? " neutra" : ""}">${h(nota)}</span></div></div>`;
  }
  const semCusto = () => requerHtml([]);
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
      return bancada({ p, classe, nivel: null, titulo: tituloPeca(p, t), marcasDe: t.de, esq: requerHtml(x.requer),
        dir: visor(x.linhas), chance: chanceHtml(x.chance), falha: x.chance >= 100 ? "" : `Falha: +${t.de} → +${Math.max(0, t.de - 1)}`,
        botao: `Reforçar +${t.de} → +${t.de + 1}`, preco: x.ouro ?? "", trava: true, dicaPeca: false });
    }
    if (p.no_limite) {
      return bancada({ ...comum, p, esq: semCusto(), dir: visor([]), botao: "Reforço máximo", trava: true });
    }
    if (p.sem_reforco) {
      return bancada({ ...comum, p, esq: semCusto(), dir: visor([]), trava: true, nota: p.sem_reforco, neutra: true });
    }
    const passo = passoDe(p);
    const ajudas = ["O equipamento não quebra.", "A tentativa custa o mesmo, dê certo ou não."];  // a falha está à vista
    // a falta já aparece no valor (o material em vermelho no Requer, o preço em vermelho no botão): o motivo por extenso
    // fica no title e no aria do botão, sem repetir numa nota embaixo; a nota só diz o que não está marcado em outro lugar
    const motivo = passo.motivo, marcado = (passo.falta || []).length > 0;
    return bancada({ ...comum, p, esq: requerHtml(passo.requer), dir: visor(passo.linhas),
      chance: chanceHtml(passo.chance), falha: passo.chance >= 100 ? "" : `Falha: +${p.reforco} → +${passo.falha}`, ajudas,
      botao: `Reforçar +${p.reforco} → +${p.reforco + 1}`, preco: passo.ouro, faltaOuro: passo.ouro_tem < passo.ouro,
      trava: motivo || "", nota: motivo && !marcado ? motivo : "" });
  }
  /** A desmontagem na mesma bancada do reforço: a peça no molde, no eixo do botão; à direita, o encaixe do que ela
   *  rende (ícone e quantidade). O botão vira a confirmação no próprio pé, com o nome da peça e a destruição. Depois de
   *  desmontar, a transformação (DESMONTE_MS): a peça se desfaz em fragmentos de pixel e o material chega ao encaixe; a
   *  seleção fica vazia (nada é escolhido sozinho) e o encaixe do resultado mostra o que chegou até a próxima ação. */
  function chapaDesmonte(p, u, d) {
    const chegou = !p && u && u.tipo === "desmonte" ? u : null;
    const t = chegou && desmonte && desmonte.id === u.id && performance.now() - desmonte.t0 < DESMONTE_MS ? desmonte : null;
    const saco = iconeDe("saco");
    let n = null, motivo = "", pe;
    if (p) {
      n = p.desmontar.total;
      motivo = p.desmontar.motivo || "";
      const conf = confirmando && confirmando.uid === p.uid;
      const perde = (p.encantos || []).filter(Boolean).map((e) => h(e.titulo)).join(", ");
      pe = peAcao({
        principal: botaoAcao({ rotulo: "Desmontar", classe: "principal perigo", attrs: conf ? "data-desmontar-sim" : "data-desmontar", motivo: conf ? "" : motivo }),
        cancelar: conf ? cancelarBtn("data-desmontar-nao") : "",
        pergunta: conf ? "<b>Destruir a peça?</b>" : "",
        nota: conf ? (perde ? `Perde as gravações: ${perde}.` : "") : h(motivo || (p.venda !== undefined ? `No mercado, vende por ${p.venda}.` : "")),
        neutra: !conf });
    } else {
      if (chegou) n = chegou.total;
      pe = peAcao({ principal: botaoAcao({ rotulo: "Desmontar", classe: "principal perigo", attrs: "data-desmontar", motivo: "Escolha uma peça" }), nota: "Escolha uma peça" });
    }
    // antes de confirmar: a previsão (×N, neutra); depois: o recebimento (+N em verde, o saldo novo aceso embaixo e
    // o nome da peça desmontada no título), até a próxima ação (17ª)
    const saldo = (d.materiais.find((m) => m.id === "fragmento") || {}).qtd;
    const resultado = chegou
      ? `<div class="rf-recebe chegou recebido" role="status" aria-label="Recebeu ${n} ${n > 1 ? "Fragmentos" : "Fragmento"} de Têmpera. Agora: ${saldo}">
          <span class="rf-encaixe pequeno">${saco}</span><b>+${n}</b><small class="rf-saldo-novo">Fragmentos: <em>${t ? `<span class="antes">${saldo - n}</span>` : ""}<span class="depois">${saldo}</span></em></small></div>`
      : `<div class="rf-recebe${n === null ? " vazio" : ""}" ${n ? Telas.dica(`<b>Fragmento de Têmpera ×${n}</b>`, true) : ""}
        aria-label="${n ? `Recebe ${n} Fragmento${n > 1 ? "s" : ""} de Têmpera` : "Nada a receber"}"><span class="rf-encaixe pequeno">${saco}</span><b>${n === null ? "" : `×${n}`}</b></div>`;
    // a peça desmontada, guardada no clique, fica no molde só durante a transformação
    const fantasma = t ? `<div class="rf-encaixe grande r-${h(t.raridade)} rf-desfaz">${t.icone}</div>` : "";
    const nivel = '<span class="rf-nivel"></span>';  // a linha do nível, vazia: a bancada tem a altura da do reforço
    const vazio = marcas({ reforco: 0, limite: 4 }).replace('class="rf-marcas"', 'class="rf-marcas" style="visibility:hidden"');
    const m = p ? molde(p, marcas(p), nivel)
      : (fantasma ? molde(null, vazio, nivel).replace('<div class="rf-encaixe grande vazio"></div>', fantasma) : molde(null, vazio, nivel));
    // o título: a peça escolhida; depois de desmontar, a que virou material (o nome guardado no resultado do motor)
    const titulo = !p && chegou ? `<div class="rf-titulo"><b>${h(chegou.nome)}</b><small>Desmontado</small><div class="rf-tit-sulcos"></div></div>` : tituloPeca(p, null);
    const decorrido = t ? ` style="--rf-e:-${Math.round(performance.now() - t.t0)}ms"` : "";
    return `<div class="rf-chapa desmonte com-titulo${t ? " transformando" : ""}"${decorrido}>${titulo}
      <div class="rf-leito"><div class="rf-lado esq"></div>${m}
        <div class="rf-lado dir">${conduto(true)}${resultado}</div></div>
      <div class="rf-pe-chapa">${pe}</div></div>`;
  }


  // ------------------------------------------------------------------ a transferência (laboratório)
  /** Transferir o reforço: duas peças de mesma importância, a origem e o destino, ligadas por um conduto que dá a direção.
   *  Cada encaixe abre um seletor (ícone, nome, raridade, reforço e dono): primeiro a origem, depois os destinos que ela
   *  aceita (os que não aceitam aparecem apagados, com o motivo). Embaixo, o preço e Transferir; a confirmação mostra os
   *  dois resultados e o preço. Depois de concluída, a cena e o resultado; as escolhas voltam vazias (nada é escolhido
   *  sozinho). Mesmo nome não confunde: cada linha é uma peça (o id), com o dono e os números dela. */
  function chapaTransfere(d, u) {
    const t = faseTransf() && u && u.tipo === "transfere" && transf && transf.id === u.id ? transf : null;
    const peca = (uid) => d.pecas.find((x) => x.uid === uid) || null;
    const o = peca(t ? t.u.origem : trOrigem);
    const dsts = o ? o.transferir.destinos : [];
    const dest = t ? peca(t.u.destino) : dsts.find((x) => x.uid === trDestino) ? peca(trDestino) : null;
    const dx = dest && !t ? dsts.find((x) => x.uid === dest.uid) : null;
    // os níveis de cada lado: na cena, os da transação (o motor já a resolveu); antes, os previstos
    const nivelO = t ? [t.u.de_origem, 0] : o ? [o.reforco, dx && !dx.motivo ? 0 : null] : null;
    const nivelD = t ? [t.u.de_destino, t.u.novo] : dest ? [dest.reforco, dx && !dx.motivo ? dx.novo : null] : null;
    const slot = (lado, p, niveis) => {
      const vazio = !p, desliga = lado === "destino" && !o && !t;
      const rot = lado === "origem" ? "Origem" : "Destino";
      const muda = niveis && niveis[1] !== null ? `<small>Após transferir</small><em class="${lado === "origem" ? "perde" : "ganha"}">+${niveis[1]}</em>` : "";
      const canto = p && niveis && niveis[0] ? `<span class="rf-canto">+${niveis[0]}</span>` : "";
      return `<button type="button" class="rf-tr-slot ${lado}${vazio ? " vazio" : ""}${trSeletor === lado ? " aberto" : ""}" data-tr-abrir="${lado}"${desliga || t ? ' aria-disabled="true"' : ""}
          aria-label="${rot}: ${p ? h(p.item.nome) : "escolher"}" ${p && !t ? dicaItem(p.item, "", false) : ""}>
        <span class="rf-tr-rotulo">${rot}</span>
        <span class="rf-encaixe grande${p ? ` r-${h(p.item.raridade)}` : " vazio"}" data-reforco="${t ? niveis[0] : p ? p.reforco : 0}" data-tr-peca="${lado}"${p ? ` data-slot="${h(p.item.slot)}"` : ""}>${p ? iconePeca(p.item) + canto + gravura(p.encantos) : ""}</span>
        <span class="rf-tr-nome">${p ? `<b class="r-${h(p.item.raridade)}">${h(p.item.nome.replace(/ \+\d+/, ""))}</b><small>${h(dono(p))}</small>` : `<small>${desliga ? "Escolha a origem primeiro" : `Escolher ${lado === "origem" ? "a origem" : "o destino"}`}</small>`}</span>
        <span class="rf-tr-nivel">${muda}</span></button>`;
    };
    const motivo = t ? "" : !o ? "Escolha a origem" : !o.reforco ? "A origem não tem reforço." : !dsts.length ? o.transferir.motivo
      : !dest ? "Escolha o destino" : dx.motivo || (d.ouro < dx.ouro ? `Faltam ${dx.ouro - d.ouro} de ouro` : null);
    // o preço dentro do botão; na confirmação, o mesmo botão no mesmo lugar (a pergunta em cima, o Cancelar ao lado)
    const conf = !!(confirmandoTransf && o && dest && dx && confirmandoTransf.origem === o.uid && confirmandoTransf.destino === dest.uid);
    const preco = t ? t.u.ouro : dx && !dx.motivo ? dx.ouro : "";
    const faltaOuro = !t && dx && !dx.motivo && d.ouro < dx.ouro;
    const pe = peAcao({
      principal: botaoAcao({ rotulo: "Transferir", preco, falta: faltaOuro, attrs: `${conf ? "data-transferir-sim" : "data-transferir"}${t ? ' aria-disabled="true"' : ""}`,
        motivo: conf || t ? "" : motivo || "" }),
      cancelar: conf ? cancelarBtn("data-transferir-nao") : "",
      pergunta: conf ? "<b>Transferir o reforço?</b>" : "",
      // a falta de ouro já está no preço (vermelho); a nota fica para o que não aparece em outro lugar
      nota: conf ? "" : h(trAviso || (faltaOuro ? "" : motivo) || ""), neutra: !trAviso });
    return `<div class="rf-chapa transfere tr2${t ? " transferindo" : ""}${trSeletor && !t ? " com-seletor" : ""}">
      <div class="rf-tr-par">${slot("origem", o, nivelO)}<span class="rf-tr-conduto" aria-hidden="true"><i class="rf-canal"></i></span>${slot("destino", dest, nivelD)}</div>
      ${trSeletor && !t ? seletorTransf(d, o, dsts) : ""}
      <div class="rf-pe-chapa">${pe}</div></div>`;
  }
  /** O seletor de um lado da transferência: uma lista com ícone, nome, raridade, reforço e dono. A origem lista as peças
   *  do grupo (as com reforço primeiro); o destino, as que a origem aceita, as válidas primeiro e as outras apagadas, com
   *  o motivo. Fecha com Esc, com a escolha ou com o mesmo encaixe. */
  const RARIDADE_NOME = { comum: "Comum", magico: "Incomum", raro: "Raro", lendario: "Lendário" };
  function seletorTransf(d, o, dsts) {
    const linha = (p, extra, motivo, ativo) => `<button type="button" role="option" class="rf-tr-op${motivo ? " apagada" : ""}${ativo ? " escolhida" : ""}" data-tr-escolher="${h(p.uid)}"${motivo ? ` aria-disabled="true" title="${h(motivo)}"` : ""} aria-selected="${ativo}">
        <span class="rf-encaixe pequeno r-${h(p.item.raridade)}">${iconePeca(p.item)}</span>
        <span class="rf-tr-op-nome"><b class="r-${h(p.item.raridade)}">${h(p.item.nome)}</b><small>${RARIDADE_NOME[p.item.raridade] || ""} · ${h(dono(p))} · ${h(p.item.bonus || "")}</small></span>
        <span class="rf-tr-op-fim">${extra}${motivo ? `<small>${h(motivo)}</small>` : ""}</span></button>`;
    let itens;
    if (trSeletor === "origem") {
      const lista = d.pecas.filter((p) => !p.sem_reforco).sort((a, b) => (b.reforco > 0) - (a.reforco > 0) || b.reforco - a.reforco);
      itens = lista.map((p) => linha(p, `<em>+${p.reforco}</em>`, !p.reforco ? "Sem reforço" : !p.transferir.destinos.some((x) => !x.motivo) ? "Nenhum destino no grupo" : "", p.uid === trOrigem)).join("");
    } else {
      const lista = [...dsts].sort((a, b) => !!a.motivo - !!b.motivo || (b.novo || 0) - (a.novo || 0));
      itens = lista.length ? lista.map((x) => { const p = d.pecas.find((q) => q.uid === x.uid);
        return linha(p, x.motivo ? `<em>+${x.de}</em>` : `<em>+${x.de} → +${x.novo}</em>`, x.motivo, x.uid === trDestino); }).join("")
        : `<p class="rf-nota neutra">${h((o && o.transferir.motivo) || "Nenhuma peça do mesmo espaço e da mesma raridade no grupo.")}</p>`;
    }
    return `<div class="rf-tr-seletor ${trSeletor}" role="listbox" aria-label="${trSeletor === "origem" ? "Peça de origem" : "Peça de destino"}">
      <div class="rf-tr-sel-cab"><b>${trSeletor === "origem" ? "Escolha a origem" : "Escolha o destino"}</b><small>${trSeletor === "destino" ? "Mesma raridade e mesmo espaço da origem" : "A peça que cede o reforço"}</small>
        <button type="button" class="botao-janela rf-botao" data-tr-fechar-lista>Fechar a lista <kbd>Esc</kbd></button></div>
      <div class="rf-tr-lista">${itens}</div></div>`;
  }

  // ------------------------------------------------------------------ a bancada do encantamento (laboratório)
  /** Gravar: duas áreas lado a lado. À esquerda, a peça (nome, dono, o molde) e os sulcos grandes, selecionáveis, cada
   *  ocupado com o símbolo e o tier da essência. À direita, a família da essência, o tier (o tier e a quantidade
   *  separados) e a previsão: a contribuição, o nível em quem veste e o que muda no efeito, com os valores do motor. No
   *  pé, estáveis, o custo e Gravar ou Substituir. A substituição pede a confirmação no pé. A gravação nunca falha. */
  function chapaEncanto(p, u, d) {
    const g = gravando && p && gravando.uid === p.uid && faseGrav() ? gravando : null;
    const ess = p ? p.encantar.essencias : [];
    const e = ess.find((x) => x.id === essSel) || null;
    const sulcos = p ? p.encantos || [] : [];
    if (p && (sulcoDe !== p.uid || sulcoSel >= sulcos.length)) {  // outra peça: o primeiro sulco vazio (ou o primeiro)
      sulcoDe = p.uid;
      sulcoSel = Math.max(0, sulcos.findIndex((x) => !x));
    }
    if (g) sulcoSel = gravando.sulco ?? sulcoSel;
    const atual = p ? sulcos[sulcoSel] : null;
    const custo = d.custo_encanto;
    const motivoPeca = p ? p.encantar.motivo : "Escolha uma peça";
    const prev = p && e && !e.motivo ? (p.encantar.previsao || {})[`${sulcoSel}|${e.id}`] : null;
    const motivo = motivoPeca || (!e ? "Escolha uma essência" : e.motivo || (prev && prev.bloqueio) || (e.qtd < 1 ? `Falta 1 Essência de ${e.titulo}` : null)
      || (d.ouro < custo ? `Faltam ${custo - d.ouro} de ouro` : null));
    // à esquerda: a peça e os sulcos
    const tituloEnc = p ? `<div class="rf-titulo"><b class="r-${h(p.item.raridade)}">${h(p.item.nome)}</b><small>${h(dono(p))}</small></div>` : `<div class="rf-titulo vazio"><b>&nbsp;</b><small>Escolha uma peça</small></div>`;
    // 18ª: o sulco que acabou de ser esvaziado apaga a cor da essência uma vez (pelo tempo decorrido: um redesenho continua)
    const esvaziou = (i) => removido && p && removido.uid === p.uid && removido.sulco === i && performance.now() - removido.t0 < 600;
    const sulcoBtns = sulcos.map((x, i) => `<button type="button" role="radio" class="rf-sulco-op${x ? "" : " vazio"}${i === sulcoSel ? " escolhido" : ""}${!x && esvaziou(i) ? " esvaziou" : ""}" data-sulco="${i}" aria-checked="${i === sulcoSel}"
        ${!x && esvaziou(i) ? `style="--ess:${h(removido.cor || "#888")};--rf-e:-${Math.round(performance.now() - removido.t0)}ms"` : ""}
        aria-label="Sulco ${i + 1}: ${x ? h(x.titulo) : "vazio"}"${x ? ` style="--ess:${h(x.cor)}"` : ""} ${Telas.dica(x ? `<b>${h(x.titulo)}</b><div>${h(x.efeito)}</div>${x.limite ? `<div class="rodape">${h(x.limite)}</div>` : ""}` : "<b>Sulco vazio</b>", true)}>
        <span class="rf-sulco-ic">${x ? icEss(x) : ""}</span><span class="rf-sulco-nome">${x ? h(x.titulo) : "Vazio"}</span></button>`).join("");
    // 18ª: remover a gravação do sulco escolhido (o sulco fica vazio; a essência se perde; sem custo). O lugar fica
    // reservado mesmo sem gravação, para nada pular ao trocar de sulco.
    const confRem = !!(confirmandoRem && p && atual && confirmandoRem.uid === p.uid && confirmandoRem.sulco === sulcoSel);
    const remBtn = p ? `<button type="button" class="rf-remover" data-remover${!atual || g ? ' aria-disabled="true" tabindex="-1"' : ""}${confRem ? ' aria-pressed="true"' : ""}
        aria-label="${atual ? `Remover ${h(atual.titulo)} do sulco ${sulcoSel + 1}` : "Sulco vazio"}">Remover gravação</button>` : "";
    const itemArea = `<section class="rf-enc-item">${tituloEnc}${molde(p, "", "")}${p ? `<div class="rf-sulcos-op" role="radiogroup" aria-label="Sulcos">${sulcoBtns}</div>${remBtn}` : ""}</section>`;
    // à direita: a família, o tier, a previsão
    const familias = [...new Set(ess.map((x) => x.essencia))].map((k) => ess.filter((x) => x.essencia === k));
    const famHtml = `<div class="rf-familias" role="radiogroup" aria-label="Essência">${familias.map((ts) => {
      const x = ts.find((t) => t.id === essSel) || ts.find((t) => t.qtd > 0) || ts[0], qtd = ts.reduce((a, t) => a + t.qtd, 0);
      const marcada = e && e.essencia === x.essencia;
      return `<button type="button" role="radio" class="rf-familia${marcada ? " escolhida" : ""}${x.motivo || qtd < 1 ? " apagada" : ""}" data-essencia="${h(x.id)}" aria-checked="${marcada}" style="--ess:${h(x.cor)}"
        aria-label="${h(x.nome)}: ${qtd} no total${x.motivo ? `. ${h(x.motivo)}` : ""}" ${Telas.dica(`${h(x.nome)}${x.motivo ? ` · <span class="pior">${h(x.motivo)}</span>` : ""}`, true)}><span class="rf-familia-ic">${iconeDe(x.icone)}</span><span class="rf-familia-nome">${h(x.nome)}</span></button>`;
    }).join("")}</div>`;
    const tierHtml = e ? `<div class="rf-tiers" role="radiogroup" aria-label="Tier">${ess.filter((x) => x.essencia === e.essencia).map((x) => `<button type="button" role="radio"
        class="rf-tier-op${x.id === e.id ? " escolhido" : ""}${x.qtd < 1 ? " apagada" : ""}" data-essencia="${h(x.id)}" aria-checked="${x.id === e.id}" style="--ess:${h(x.cor)}">
        ${icEss(x)}<span class="rf-tier-qtd" aria-label="${x.qtd} ${x.qtd === 1 ? "unidade" : "unidades"}">×${x.qtd}</span></button>`).join("")}</div>` : "";
    const rem = confRem ? (p.encantar.remocao || {})[sulcoSel] : null;
    const essArea = `<section class="rf-enc-ess">${famHtml}${tierHtml}${rem ? previsaoRemocao(rem) : e && p && !motivoPeca ? previsaoGravacao(p, e, atual, prev) : `<p class="rf-nota neutra">${h(motivoPeca || "Escolha uma essência")}</p>`}</section>`;
    // o pé: o que a gravação consome (Requer: a essência e, numa peça vestida, o nível de quem veste), a ação com o
    // preço dentro e, na substituição, a confirmação no mesmo lugar
    // o Requer só quando a operação existe (uma gravação idêntica ou incompatível não consome nada)
    const requer = e && !motivoPeca && !e.motivo && !(prev && prev.bloqueio && !prev.nivel) ? [e.requer, prev && prev.nivel] : [];
    const faltaOuro = !!(e && !motivoPeca && d.ouro < custo);
    // o que já aparece marcado (a essência e o nível no Requer, o ouro no preço) não volta numa nota
    const marcado = !!e && ((e.qtd < 1) || faltaOuro || !!(prev && prev.bloqueio && prev.nivel));
    const conf = confirmandoGrav && p && confirmandoGrav.uid === p.uid;
    // a confirmação da remoção: no mesmo pé, a pergunta numa frase (a essência e a perda) e o Remover no lugar da ação
    const pe = confRem ? `<div class="rf-pe-linha enc">${peAcao({
      principal: botaoAcao({ rotulo: "Remover", classe: "principal perigo", attrs: "data-remover-sim" }),
      cancelar: cancelarBtn("data-remover-nao"),
      pergunta: `<span class="rf-troca">Remover? <b style="color:${h(atual.cor)}">${h(atual.titulo)}</b> se perde.</span>`,
      neutra: false })}</div>` : `<div class="rf-pe-linha enc">${peAcao({
      esquerda: requerHtml(requer),
      principal: botaoAcao({ rotulo: atual ? "Substituir" : "Gravar", preco: e && !motivoPeca ? custo : "", falta: faltaOuro,
        attrs: `${conf ? "data-gravar-sim" : "data-gravar"}${g ? ' aria-disabled="true"' : ""}`, motivo: conf || g ? "" : motivo || "" }),
      cancelar: conf ? cancelarBtn("data-gravar-nao") : "",
      // a troca já está na prévia ("Sai Carrasco I · entra Brasa II"): a pergunta diz só o que é irreversível
      pergunta: conf ? `<span class="rf-troca">Substituir? <b style="color:${h(atual.cor)}">${h(atual.titulo)}</b> se perde.</span>` : "",
      nota: conf ? "" : h(!p ? "Escolha uma peça" : motivo && !marcado ? motivo : ""),
      neutra: !conf && !/^(Falta|Requer)/.test(motivo || "") })}</div>`;
    const classe = g ? ` gravando${faseGrav() === "gravado" ? " gravado" : ""}` : "";
    return `<div class="rf-chapa encanto enc2${classe}"${g ? ` style="--ess:${h(g.para.cor)}"` : e ? ` style="--ess:${h(e.cor)}"` : ""}>
      <div class="rf-enc-corpo">${itemArea}${essArea}</div>
      <div class="rf-pe-chapa">${pe}</div></div>`;
  }

  /** A prévia da gravação escolhida, pronta do motor: a essência com o tier e o requisito; o efeito dela (o valor deste
   *  tier); numa substituição, os valores que mudam (nesta peça e, quando outra peça de quem veste também
   *  soma ou o limite corta, em quem veste); a troca; o limite. Nada de contas na tela. */
  function previsaoGravacao(p, e, atual, prev) {
    // o requisito de nível fica no "Requer:" do pé (quando a peça é vestida) ou na nota da consequência (na bolsa)
    const linhas = ((prev && prev.linhas) || []).map((l) => [l.rotulo, `${l.antes} → ${l.depois}`, l.melhor ? "melhor" : "pior"]);
    return `<div class="rf-prev"><div class="rf-prev-tit">${icEss(e)}<b style="--ess:${h(e.cor)}">${h(e.titulo)}</b></div>
      <p class="rf-prev-ef">${h(e.efeito)}${e.limite ? ` <span class="lim">${h(e.limite)}</span>` : ""}</p>
      ${linhas.length ? `<dl class="rf-prev-linhas">${linhas.map(([k, v, c]) => `<dt>${h(k)}</dt><dd${c ? ` class="${c}"` : ""}>${h(v)}</dd>`).join("")}</dl>` : ""}
      ${atual && atual.id !== e.id ? `<p class="rf-prev-troca">Sai <b style="color:${h(atual.cor)}">${h(atual.titulo)}</b> · entra <b style="color:${h(e.cor)}">${h(e.titulo)}</b></p>` : ""}
      ${prev && prev.aviso ? `<p class="pior">${h(prev.aviso)}</p>` : ""}${prev && prev.nota ? `<p class="rf-prev-nota">${h(prev.nota)}</p>` : ""}</div>`;
  }

  /** A prévia da remoção (18ª), pronta do motor: a gravação que sai e o que muda (o efeito na peça, o total de quem
   *  veste quando outra peça dele também soma, o requisito novo da peça quando cai). A perda fica na pergunta do pé. */
  function previsaoRemocao(r) {
    const x = r.sai, linhas = (r.linhas || []).map((l) => `<dt>${h(l.rotulo)}</dt><dd class="pior">${h(l.antes)} → ${h(l.depois)}</dd>`).join("");
    return `<div class="rf-prev rf-prev-rem"><div class="rf-prev-tit">${icEss(x)}<b style="--ess:${h(x.cor)}">${h(x.titulo)}</b></div>
      ${linhas ? `<dl class="rf-prev-linhas">${linhas}</dl>` : ""}${r.nota ? `<p class="rf-prev-nota">${h(r.nota)}</p>` : ""}</div>`;
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
      ${secaoEncantos(p.encantos, p.efeitos)}${reqHtml(p.requisito)}
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
  /* O resto do gesto que já agiu não age de novo: o 2º clique de um clique duplo (event.detail 2) e o clique que o
     Espaço gera ao soltar a tecla que dispensou. Do 3º clique em diante é uma ação nova: o Windows segue contando
     (3, 4, 5…) enquanto os cliques caem no mesmo ponto a menos de meio segundo, e tratar todo "detail > 1" como o resto
     do gesto travava quem clicava de novo logo depois do OK, até parar de clicar. Nada de pausa por tempo. */
  let teclaDispensou = null;  // a tecla (Enter, Espaço) que dispensou o resultado, até ser solta
  const resto = (ev) => ev.detail === 2 || (ev.detail === 0 && !!teclaDispensou);
  /** A faixa de intensidade do nível alcançado: 0 (+1, +2), 1 (+3, +4), 2 (+5 a +8), 3 (+9 a +11), 4 (+12). */
  const faixaNivel = (n) => (n >= 12 ? 4 : n >= 9 ? 3 : n >= 5 ? 2 : n >= 3 ? 1 : 0);
  // as cores do efeito pelo nível: o ouro até o +4 (já aprovado); do +5 ao +8, a cor do nível (a mesma do acabamento);
  // do +9, o prisma (os raios em várias cores, mais cores a cada nível)
  const COR_NIVEL = {
    5: ["W", "#c8fff4", "#46e2cc", "#1f9a8c", "#0e4a46"], 6: ["W", "#c8dcff", "#5a8cff", "#2a4cc0", "#14205a"],
    7: ["W", "#ecd2ff", "#b064ff", "#6a2cb0", "#2c1050"], 8: ["W", "#ffd0d8", "#ff3c60", "#a8102e", "#4a0614"],
  };
  const PRISMA = ["#ff3c60", "#ffb032", "#46e2a0", "#468cff", "#aa64ff", "#ff6edc"];
  /* A paleta da celebração do +9 ao +12 (17ª; o +8 e os de baixo não mudam). A da 16ª (violeta, depois ouro) ficou
     desligada do acabamento da peça; agora a celebração sai das mesmas cores do veio e do feixe daquele nível: o rubi
     e o âmbar sempre na frente (a direção quente que o contorno do +9 já tem), e a cor fria que o nível acrescenta ao
     veio como secundária (o azul no +10, a esmeralda no +11, o violeta e o marfim no +12). O prisma inteiro só em
     alguns estilhaços. A grandeza sobe pela forma: o +10 ganha um leque de raios finos, o +11 raios mais longos, o
     +12 dois leques. dom = [W, claro, médio, escuro, fundo], sec = a secundária. */
  const CELEBRA = {
    9: { dom: ["W", "#ffd0d8", "#ff3c60", "#a8102e", "#4a0614"], sec: "#ffb032", leque: 0, longo: 1 },
    10: { dom: ["W", "#ffe0b0", "#ff7a3c", "#a8102e", "#4a0614"], sec: "#468cff", leque: 1, longo: 1.03 },
    11: { dom: ["W", "#fff0c0", "#ffb032", "#c0441c", "#4a1408"], sec: "#46e2a0", leque: 1, longo: 1.06 },
    12: { dom: ["W", "#fff4c8", "#ffb032", "#d0402a", "#4a1408"], sec: "#aa64ff", leque: 2, longo: 1.08 },
  };
  /* A celebração dourada que a 16ª mostrava no +12 (o Jean gostou): guardada como referência de um possível +13, que
     não existe (sem custo, chance nem marco). O painel de testes a mostra no +12 só para comparar. */
  const CELEBRA_REF13 = { dom: ["W", "#fff4c8", "#ffd060", "#e09a20", "#6a3a08"], sec: "#ffb032", leque: 2, longo: 1.08 };
  const celebraNova = (n) => {
    const pal = document.body.dataset.rfPaleta;
    if (n < 9 || pal === "anterior") return null;
    return pal === "referencia13" && n >= 12 ? CELEBRA_REF13 : CELEBRA[Math.min(n, 12)];
  };
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
    const n = nova >= 0 ? lista[nova] : null;  // a gravação: a que entrou, com o efeito dela, e a que saiu
    return `<div class="rf-res-sulcos"><div class="rf-res-sulcos-cab"><span class="rf-res-rotulo">Sulcos</span><span class="rf-sq-fila">${lista.map((x, i) => filaSulcos([x]).replace('class="rf-sq', `class="rf-sq${i === nova ? " nova" : ""}`)).join("")}</span></div>
      ${n ? `<div class="rf-ef nova" style="--ess:${h(n.cor)}"><span class="rf-ef-nome">${h(n.titulo)}</span><span class="rf-ef-txt">${h(n.efeito)}${n.limite ? ` <span class="lim">${h(n.limite)}</span>` : ""}</span></div>` : ""}
      ${saiu ? `<div class="rf-res-saiu">Saiu <b style="color:${h(saiu.cor)}">${h(saiu.titulo)}</b></div>` : ""}</div>`;
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

  /** A peça do resultado nítida e parada, em pixels reais da tela: a ampliação é um múltiplo inteiro do desenho em
   *  pixels do aparelho (numa tela a 125%, 80 px de CSS seriam 2,5× e cada pixel do desenho sairia com 2 ou 3 de largura,
   *  conforme a posição), e o conjunto é deslocado até a peça cair num pixel inteiro do aparelho (lá, 566 px de CSS
   *  são 707,5). Sem isso, qualquer redesenho (a passada do reflexo) mudava o arredondamento, e a peça tremia. O
   *  deslocamento é de layout (left/top), não uma transformação: com `translate` fracionário, o navegador reamostrava o
   *  canvas do veio (do +5) com suavização, e a peça borrava e tremia no resultado. */
  function nitida(el) {
    const img = el.querySelector(".rf-res-arte > img, .rf-res-arte > canvas"), conj = el.querySelector(".rf-res-conj");
    if (!img || !conj) return;
    // o tamanho do desenho: o do arquivo, ou, antes de ele carregar, o que o jogo declara na imagem (width="40")
    const dpr = window.devicePixelRatio || 1, nat = img.naturalWidth || +img.getAttribute("width") || img.width;
    if (!nat) { img.addEventListener("load", () => nitida(el), { once: true }); return; }
    img.style.width = img.style.height = "";  // a medida do CSS (80 a 1920, 40 a 1280), antes do ajuste
    const vez = Math.max(1, Math.round((img.getBoundingClientRect().width * dpr) / nat));
    img.style.width = img.style.height = `${(nat * vez) / dpr}px`;
    conj.style.left = conj.style.top = "0px";
    const r = img.getBoundingClientRect();
    conj.style.left = `${(Math.round(r.left * dpr) - r.left * dpr) / dpr}px`;
    conj.style.top = `${(Math.round(r.top * dpr) - r.top * dpr) / dpr}px`;
  }
  addEventListener("resize", () => { const el = document.getElementById("rf-res"); if (el) nitida(el); });

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
      <div class="rf-res-pe">${banner}<button type="button" class="botao-janela rf-botao principal" data-res-ok><span class="rf-bp-rot">OK<kbd class="rf-tecla">Enter</kbd></span></button></div></div>`;
    document.body.appendChild(el);
    nitida(el);
    document.body.classList.add("rf-res-aberto");  // o nome e a peça da bancada saem do fundo (não aparecem duas vezes)
    res = { id, el, ctl: null, palco: null };
    const caixa = el.querySelector(".rf-res-arte");
    acabamento(caixa, nivel);  // o acabamento do nível novo já na revelação
    if (nivel) {
      // num relógio próprio: o redesenho da forja (limparRelogios) não a cancela
      setTimeout(() => { if (caixa.isConnected) reflexo(caixa, nivel, true); }, reduzido() ? 0 : 280);
      // depois da passada da entrada, o ciclo de todas as peças (a cada ~3 s), sem a espera de quem acabou de aparecer
      agenda.set(`resultado:${nivel}`, { proxima: performance.now() + 280 + PERIODO, visto: performance.now() });
    }
    // nada passa para trás: um clique fora do OK não faz nada; o 2º clique de um clique duplo no OK não chega à bancada
    el.addEventListener("click", (ev) => {
      ev.stopPropagation();
      if (ev.target.closest("[data-res-ok]") && !resto(ev)) dispensarRes();
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
    else if (faseTransf() === "resultado") dispensarTransf();
    else fecharRes();
  }

  /** O efeito do resultado do reforço, no palco da apresentação: no sucesso, o selo de raios atrás da peça, o clarão,
   *  os anéis e os estilhaços, mais fortes e mais coloridos nos marcos (+3, +5, +9, +12) sem durar mais; depois do
   *  impacto, os raios acomodam numa intensidade que deixa ler e continuam girando até o OK. Na falha, um anel fraco que
   *  apaga, cinzas e o esfriar, sem dourado. */
  function efeitoReforco(u, desde) {
    return (palco, el) => {
      const alvo = el.querySelector(".rf-res-arte"), ficha = el.querySelector(".rf-res-ficha"), numero = el.querySelector(".rf-res-nome .rf-n-agora");
      const nova = u.sucesso ? celebraNova(u.para) : null;
      const f = faixaNivel(u.para), pal = nova ? nova.dom : paletaNivel(u.para), enx = FX.enxame();
      const cores = u.para >= 9 && !nova ? PRISMA.slice(0, u.para >= 12 ? 6 : u.para - 7) : null;
      const estrelaCores = nova ? ["z", pal[4], pal[2], pal[1]] : u.para >= 9 ? ["z", "#5a1030", "#ffb032", "#fff4c8"] : u.para >= 5 ? ["z", pal[4], pal[2], pal[1]] : ["z", "o", "O", "Y"];
      // na candidata: os estilhaços e as brasas na dominante, um em três na secundária, um em nove no prisma
      const palEstilhaco = (i) => (!nova ? null : i % 9 === 0 ? ["W", PRISMA[i % 6], PRISMA[(i + 2) % 6]] : i % 3 === 0 ? ["W", nova.sec, pal[3]] : ["W", pal[1], pal[2], pal[3]]);
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
        const longo = [2.6, 3.4, 3.6, 3.9, 4.3][f] * (nova ? nova.longo : 1), calmo = [1.9, 2.1, 2.2, 2.35, 2.55][f] * (nova ? nova.longo : 1);
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
        // a candidata: leques de raios finos na secundária, entre os da dominante (o +10 um, o +12 dois)
        for (let k = 0; nova && k < nova.leque; k++) {
          FX.raios(palco, { cx: a.x, cy: a.y, n: Math.round(n / 2), ang: ang + Math.PI / n + k * Math.PI / (2 * n), larg: 0.1, r0: R,
            r1: Math.round(r1 * (0.78 + 0.1 * k)), pal: ["W", nova.sec, nova.sec], esbate: 0.4, achata, alterna: 0.7, vis: Math.max(4, vis - 3 - 2 * k) });
        }
        FX.estrela(palco, { cx: a.x, cy: a.y, pontas: 14 + 2 * Math.max(0, f - 1), ri: R + 2, re, pal, cores: estrelaCores });
        FX.poco(palco, { cx: a.x, cy: a.y, rx: R + 2, ry: R + 2, forca: 14 });  // a peça lê sobre o selo
        if (parado) return;
        FX.claraoLocal(palco, { cx: a.x, cy: a.y, r: R + palco.t([24, 30, 34, 38, 44][f]), t, dur: f >= 3 ? 240 : 200, espalha: 0 });
        // os anéis do impacto: um até o +2, dois do +3, três do +9 (um só golpe, sem repetir)
        [0, 110, 220].slice(0, f >= 3 ? 3 : f >= 1 ? 2 : 1).forEach((d, i) => {
          const tt = t - d;
          if (tt >= 0 && tt < 420) FX.anel(palco, { cx: a.x, cy: a.y, r: re + Math.round(FX.rampa(tt, 0, 400) * palco.t([50, 70, 80, 96, 110][f] - i * 12)), esp: 2,
            pal: cores ? ["W", cores[i % cores.length], cores[(i + 1) % cores.length]] : nova && i === 2 ? ["W", nova.sec, pal[2]] : ["W", pal[1], pal[2]], achata: 0.6, rastro: 3, vis: Math.round(14 * (1 - tt / 420)) });
        });
        if (passo && q === 1) enx.soltar([24, 42, 52, 64, 84][f], (i) => {
          const g = FX.aleatorio(0, Math.PI * 2), v = FX.aleatorio(3, 7.5) * [0.95, 1.25, 1.3, 1.4, 1.5][f];
          return { x: a.x + Math.cos(g) * re * 0.8, y: a.y + Math.sin(g) * re * 0.7, vx: Math.cos(g) * v, vy: Math.sin(g) * v - 2, g: 0.36, arrasto: 0.97,
            vida: Math.round(FX.aleatorio(18, 32)), desenho: ["lasca", "caco", "cruz", "duplo"][i % 4],
            pal: cores ? ["W", cores[i % cores.length], cores[(i + 2) % cores.length]] : palEstilhaco(i) || ["W", pal[1], pal[2], pal[3]], piscar: i % 5 === 0 };
        });
        // depois do golpe: brasas subindo e, nos níveis altos, pontos de brilho em volta (sem repetir o golpe)
        if (passo && q > 6 && q % [3, 3, 3, 2, 2][f] === 0) enx.soltar(1, () => ({ x: a.x + FX.aleatorio(-re, re), y: a.y + re * 0.6, vx: FX.aleatorio(-0.3, 0.3), vy: FX.aleatorio(-1.4, -0.7), vida: 16,
          desenho: "brasa", pal: cores ? ["W", cores[q % cores.length], "D"] : nova ? ["W", q % 3 === 0 ? nova.sec : pal[2], pal[3], "D"] : ["Y", "O", "o", "r", "D"] }));
        if (passo && f >= 2 && q > 10 && q % (f >= 3 ? 5 : 8) === 0) { const g = FX.aleatorio(0, Math.PI * 2); enx.soltar(1, () => ({ x: a.x + Math.cos(g) * re * 1.3, y: a.y + Math.sin(g) * re * 0.9,
          vx: 0, vy: 0, vida: 7, desenho: "brilho", pal: cores ? ["W", cores[q % cores.length]] : nova ? ["W", u.para >= 12 && q % 2 ? "#fffbe8" : pal[1]] : ["W", pal[1], pal[2]] })); }
        // a marca quente no título: poucas fagulhas saindo do número novo
        if (passo && numero && q === 2) { const m = palco.de(numero); enx.soltar([8, 12, 14, 16, 18][f], () => ({ x: m.x + FX.aleatorio(-m.rx, m.rx), y: m.y + FX.aleatorio(-m.ry * 0.5, m.ry * 0.5),
          vx: FX.aleatorio(-1.6, 1.6), vy: FX.aleatorio(-2.6, -0.8), g: 0.2, arrasto: 0.95, vida: Math.round(FX.aleatorio(8, 16)), desenho: Math.random() < 0.5 ? "ponto" : "brasa",
          pal: cores ? ["W", cores[0], cores[1]] : nova ? ["W", pal[1], pal[2]] : ["W", "Y", "O", "o"] })); }
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
      arte: `<div class="rf-res-arte r-${h(p.item.raridade)}" data-reforco="${p.reforco}" data-slot="${h(p.item.slot)}">${iconePeca(p.item)}</div>`,  // sem o rastro quadrado das gravações (corta o selo); elas estão nos sulcos
      ficha: `${rotuloPeca(p)}<div class="rf-res-linhas">${linhasRes(p, u.linhas, !u.sucesso)}</div>${p.efeito ? `<p class="rf-res-efeito">${h(p.efeito)}</p>` : ""}${sulcosRes(p.encantos)}`,
      banner: `<span class="rf-banner ${u.sucesso ? "ok" : "mau"}">${u.sucesso ? "Sucesso" : "Falhou"}</span>`,
      nivel: p.reforco,
      fx: efeitoReforco(u, cena && !reduzido() ? Math.max(0, performance.now() - cena.t0 - IMPACTO) : 0),
    });
  }

  /** A transferência concluída, em destaque: "Transferência concluída", o destino (com o acabamento do nível novo já
   *  na revelação) e as duas peças, antes → depois. Garantida: um anel dourado curto e poucos brilhos, sem a explosão
   *  do reforço. Fica até o OK. */
  function apresentarTransferencia(tr) {
    const d = ultimoDesenho, u = tr.u;
    const o = d && d.pecas.find((x) => x.uid === u.origem), ds = d && d.pecas.find((x) => x.uid === u.destino);
    if (!o || !ds) return;
    abrirRes({
      id: `x${u.id}`, classe: "transferencia", aria: `Transferência concluída: ${ds.item.nome}`,
      titulo: `<b class="rf-res-nome">Transferência concluída</b>`,
      arte: `<div class="rf-res-arte r-${h(ds.item.raridade)}" data-reforco="${ds.reforco}" data-slot="${h(ds.item.slot)}">${iconePeca(ds.item)}${gravura(ds.encantos)}</div>`,
      ficha: `<span class="rf-res-rotulo">Destino · ${h(dono(ds))}</span>
        <div class="rf-res-linhas"><div class="rf-res-linha muda"><span class="r-${h(ds.item.raridade)}">${h(ds.item.nome.replace(/ \+\d+/, ""))}</span><b>+${u.de_destino} → <em class="ganha">+${u.novo}</em></b></div></div>
        <span class="rf-res-rotulo">Origem · ${h(dono(o))}</span>
        <div class="rf-res-linhas"><div class="rf-res-linha"><span>${h(o.item.nome.replace(/ \+\d+/, ""))}</span><b>+${u.de_origem} → <em class="perde">+0</em></b></div></div>`,
      banner: "",
      nivel: ds.reforco,
      fx: efeitoTransfere(reduzido() ? 0 : Math.max(0, performance.now() - tr.t0 - TRANSF_MS)),
    });
  }
  function efeitoTransfere(desde) {
    return (palco, el) => {
      const alvo = el.querySelector(".rf-res-arte"), ficha = el.querySelector(".rf-res-ficha"), enx = FX.enxame();
      const ctl = animarRes(palco, (t, q, parado, passo) => {
        const a = palco.de(alvo), R = Math.max(a.rx, a.ry) + palco.t(8);
        if (ficha) { const f = palco.de(ficha); FX.poco(palco, { cx: f.x, cy: f.y, rx: f.rx + palco.t(26), ry: f.ry + palco.t(16), forca: 15 }); }
        FX.poco(palco, { cx: a.x, cy: a.y, rx: R + 2, ry: R + 2, forca: 12 });
        if (parado) return;
        if (t < 480) FX.anel(palco, { cx: a.x, cy: a.y, r: R + Math.round(FX.rampa(t, 0, 460) * palco.t(56)), esp: 2, pal: ["W", "Y", "O"], achata: 0.85, rastro: 3, vis: Math.round(14 * (1 - t / 480)) });
        const tp = (t - 900) % 2600;  // depois, um anel fino de tempos em tempos (o destino aceso)
        if (t > 900 && tp < 520) FX.anel(palco, { cx: a.x, cy: a.y, r: R + Math.round((tp / 520) * palco.t(30)), esp: 1, pal: ["Y", "y", "c"], achata: 0.85, rastro: 2, vis: Math.round(8 * (1 - tp / 520)) });
        if (passo && q === 1) enx.soltar(10, () => ({ x: a.x + FX.aleatorio(-R, R), y: a.y + FX.aleatorio(-R, R * 0.4), vx: FX.aleatorio(-1, 1), vy: FX.aleatorio(-1.6, -0.5), g: 0.05,
          vida: Math.round(FX.aleatorio(10, 16)), desenho: Math.random() < 0.4 ? "brilho" : "ponto", pal: ["W", "Y", "O"] }));
        if (passo) enx.passo();
        enx.desenhar(palco);
      });
      if (desde > 0 && ctl.pular) ctl.pular(desde);
      return ctl;
    };
  }
  function adiantarTransf() {
    if (faseTransf() === "anim") { transf.t0 = performance.now() - TRANSF_MS; if (ultimoRaiz && ultimoDesenho) ultimoRaiz.replaceWith(Telas.painel({ tipo: "forja_proto", dados: ultimoDesenho })); }
  }
  function dispensarTransf() {
    if (faseTransf() !== "resultado") return;
    transf.fim = true;
    trOrigem = trDestino = null; trSeletor = null; trAviso = "";  // nada é escolhido sozinho depois da operação
    fecharRes();
    document.body.classList.remove("rf-em-cena");
    if (ultimoRaiz && ultimoRaiz.isConnected && ultimoDesenho) ultimoRaiz.replaceWith(Telas.painel({ tipo: "forja_proto", dados: ultimoDesenho }));
    document.querySelector(".rf-janela [data-tr-abrir='origem']")?.focus();
  }

  /** A gravação concluída, em destaque: o nome da peça, a peça com a borda de luz das gravações e o acabamento do
   *  reforço, os sulcos ao lado com a gravação nova em destaque (o nome, o símbolo e o efeito dela; as outras só pelo
   *  nome), a que saiu (na substituição), "Gravado" na cor da essência e o OK. Sem sorteio: nada de suspense. */
  function apresentarGravacao(g) {
    const d = ultimoDesenho, p = d && d.pecas.find((x) => x.uid === g.uid);
    if (!p) return;
    abrirRes({
      id: `g${g.id}`, classe: "gravacao", aria: `Gravação: ${g.para.nome} em ${p.item.nome}`,
      titulo: nomeRes(p, null),
      arte: `<div class="rf-res-arte r-${h(p.item.raridade)}" data-reforco="${p.reforco}" data-slot="${h(p.item.slot)}">${iconePeca(p.item)}${gravura(p.encantos)}</div>`,
      ficha: `${rotuloPeca(p)}${sulcosRes(p.encantos, g.sulco, g.de)}`,
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
   *  e um clarão pequeno onde ela estava. Sem raios nem celebração. Com movimento reduzido, nada se move.
   *  18ª: antes, o efeito corria a 15 quadros por segundo (o ritmo das celebrações), as partículas saltavam vários pixels
   *  por quadro, e qualquer redesenho da forja (a volta do motor desenha mais de uma vez) parava o palco no meio do voo.
   *  Agora tem o palco e o relógio próprios, fora da janela (um redesenho não o corta), um quadro a cada atualização da
   *  tela e cada fragmento numa curva com hora de saída e de chegada; as posições vêm da tela a cada quadro. */
  let fxDesmonte = null;  // {el, fim}: o palco da desmontagem
  function pararDesmonte() { if (fxDesmonte) { fxDesmonte.fim = true; fxDesmonte.p.el.remove(); } fxDesmonte = null; }
  function fragmentar() {
    pararDesmonte();
    soar("equipar");
    if (typeof FX === "undefined" || reduzido() || !desmonte) return;
    const t0 = desmonte.t0, sel = (q) => document.querySelector(`.rf-janela .rf-chapa.desmonte ${q}`);
    if (!sel(".rf-desfaz") || !sel(".rf-recebe .rf-encaixe")) return;
    baque(BAQUE.desmonte);
    const p = FX.palco(document.body, { z: 80, classe: "rf-fx" }), eu = { p, fim: false };
    fxDesmonte = eu;
    const a0 = p.de(sel(".rf-desfaz")), R = Math.max(a0.rx, a0.ry) * 0.8;
    const pal = ["W", "w", "G", "g"], forma = ["caco", "lasca", "ponto", "duplo"];
    const cacos = Array.from({ length: 22 }, (_, i) => ({
      dx: FX.aleatorio(-R, R), dy: FX.aleatorio(-R, R), arco: FX.aleatorio(0.6, 1.4),
      sai: 60 + FX.aleatorio(0, 120), dura: FX.aleatorio(320, 440), desenho: forma[i % 4], tom: i % 3 === 0 ? 0 : 1,
    }));
    const quadro = (agora) => {
      if (eu.fim) return;
      const tt = agora - t0, alvo = sel(".rf-desfaz") || null, destino = sel(".rf-recebe .rf-encaixe");
      if (tt > DESMONTE_MS || !destino) { pararDesmonte(); return; }
      const a = alvo ? p.de(alvo) : a0, d = p.de(destino);
      p.limpar();
      if (tt < 140) FX.claraoLocal(p, { cx: a.x, cy: a.y, r: R + p.t(10), t: tt, dur: 140, espalha: 0, pal });
      for (const c of cacos) {
        const u = (tt - c.sai) / c.dura;
        if (u < 0 || u > 1) continue;
        const e = u * u * (3 - 2 * u);  // sai devagar, acelera no meio e assenta no encaixe
        const x0 = a.x + c.dx, y0 = a.y + c.dy, mx = (x0 + d.x) / 2, my = Math.min(y0, d.y) - p.t(26) * c.arco;
        const x = (1 - e) * (1 - e) * x0 + 2 * (1 - e) * e * mx + e * e * d.x, y = (1 - e) * (1 - e) * y0 + 2 * (1 - e) * e * my + e * e * d.y;
        const g = FX.DESENHOS[c.desenho], k = Math.min(2, c.tom + Math.floor(u * 2)), cor = { a: FX.cor(pal[k]), b: FX.cor(pal[k + 1]) };
        const ox = Math.round(x) - (g[0].length >> 1), oy = Math.round(y) - (g.length >> 1);
        for (let yy = 0; yy < g.length; yy++) for (let xx = 0; xx < g[yy].length; xx++) if (cor[g[yy][xx]]) p.por(ox + xx, oy + yy, cor[g[yy][xx]]);
      }
      p.mostrar();
      requestAnimationFrame(quadro);
    };
    requestAnimationFrame(quadro);
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
  function dispensarGrav() { if (faseGrav() === "gravado") assentarGrav(); }

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
  function dispensar() { if (fase() === "desfecho") assentar(); }
  const revelar = assentar;  // os gestos que interrompem (trocar de peça, fechar) assentam a cena

  // ------------------------------------------------------------------ o reflexo do reforço
  /** Um reflexo diagonal curto atravessa a silhueta da peça (o próprio desenho é a máscara: só o que tem pixel
   *  brilha), na cor do nível: +1 claro e discreto, +2 esverdeado, +3 azul, +4 dourado. A borda de raridade do encaixe
   *  não muda. Passa no sucesso, na escolha da peça, no mouse e no foco, e sozinho em ciclo (abaixo); um gesto não o
   *  repete antes de 1,5 s. Com movimento reduzido, fica parado e discreto. */
  function reflexo(caixa, nivel, fixo = false, parado = false) {
    if (!caixa || !nivel) return;
    // o feixe da 17ª nas armaduras do +9 ao +12 não tinha a passada larga; as alternativas da 18ª têm, como o +8
    if (nivel >= 9 && ARMADURAS.has(espacoDe(caixa)) && document.body.dataset.rfArmadura === "feixe") { caixa.querySelector(".rf-reflexo")?.remove(); return; }
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
    corDaPassada(caixa, r, nivel);
    r.classList.remove("passa");
    void r.offsetWidth;  // recomeça a passada
    r.classList.add("passa");
  }
  /** A passada nas armaduras do +9 ao +12 (18ª) na cor da alternativa escolhida, com a mesma forma da do +8 (a faixa
   *  com o miolo claro e o fio atrás): A, uma cor por passada, na ordem do nível; B, a cor do momento (a mesma das
   *  faixas); C, a principal na faixa e a secundária no fio. Nas outras peças e níveis, a cor do CSS. */
  function corDaPassada(caixa, r, nivel) {
    const v = document.body.dataset.rfArmadura, n = Math.min(nivel, 12);
    const tem = n >= 9 && ["a", "b", "c"].includes(v) && ARMADURAS.has(espacoDe(caixa));
    if (!tem) { ["--borda", "--miolo", "--seg"].forEach((k) => r.style.removeProperty(k)); return; }
    const rgba = (c, a) => `rgba(${hexRgb(c).join(",")},${a})`;
    let cor = ARM_PAR[n][0], seg = null;
    if (v === "a") { caixa._passada = (caixa._passada || 0) + 1; cor = ARM_CORES[n][(caixa._passada - 1) % ARM_CORES[n].length]; }
    else if (v === "b") {
      const lista = ARM_CORES[n], por = PERIODO_8 * ARM_GRADUAL, i = passoAgora() % (por * lista.length);
      const k = Math.floor(i / por), tt = (i % por) / por;
      cor = misturar(lista[k], lista[(k + 1) % lista.length], tt * tt * (3 - 2 * tt));
    } else seg = ARM_PAR[n][1];
    r.style.setProperty("--borda", rgba(cor, 0.8));
    r.style.setProperty("--miolo", rgba(n >= 12 ? W_ : clarear(cor), 0.95));
    if (seg) r.style.setProperty("--seg", rgba(seg, 0.95)); else r.style.removeProperty("--seg");
  }
  function apagarReflexo() {}  // parado (movimento reduzido), o reflexo fica: é o acabamento da peça reforçada

  /** O acabamento permanente do reforço sobre o desenho da peça (o próprio desenho é a máscara: só os pixels dela
   *  recebem cor e brilho; a borda de raridade, a seleção, o foco e os rastros das gravações não mudam):
   *    +4        o contorno dourado de 1 px (já aprovado);
   *    +5 a +8   o contorno na cor do nível (turquesa, safira, ametista, rubi) e um veio da mesma cor que atravessa
   *              a peça devagar, mais presente a cada nível; o +8 com um ponto de brilho;
   *    +9 a +12  o veio em várias cores, contínuo (2, 3, 4 cores; o +12 em todas, como pedra lapidada), o contorno
   *              trocando de cor continuamente e pontos de brilho (1 a 4).
   *  A presença sobe pela cor e pelo brilho, não pela velocidade: o mesmo ritmo em todos. Cada peça começa num
   *  ponto diferente da volta (nada pisca em sincronia). `n` 0 a 3 tira tudo (uma queda também tira). */
  const BRILHOS = { 8: 1, 9: 1, 10: 2, 11: 3, 12: 4 };
  // o contorno do nível (do +4): a cor e a luz de cima; do +9, a cor gira pelo matiz (CSS)
  const CONTORNO = {
    4: ["rgba(255,196,70,0.45)", "rgba(255,220,120,0.5)"], 5: ["rgba(70,226,204,0.55)", "rgba(170,255,240,0.6)"],
    6: ["rgba(80,130,255,0.65)", "rgba(170,200,255,0.7)"], 7: ["rgba(180,100,255,0.7)", "rgba(225,190,255,0.75)"],
    8: ["rgba(255,60,96,0.75)", "rgba(255,180,190,0.8)"], 9: ["rgba(255,60,96,0.8)", "rgba(255,200,120,0.85)"],
  };
  /** A silhueta de fora do desenho, em pixels do desenho: o que é transparente e alcançável pela borda é "fora"; um
   *  vazado fechado (o furo do anel) conta como dentro. Guardada por desenho. */
  const silhuetas = new Map();
  function silhueta(img) {
    const src = img.tagName === "IMG" ? img.currentSrc || img.src : null;
    if (src && silhuetas.has(src)) return silhuetas.get(src);
    if (img.tagName === "IMG" && !img.complete) return null;  // ainda carregando: tenta na próxima passada
    const w = img.naturalWidth || img.width, hh = img.naturalHeight || img.height;
    if (!w || !hh) return null;
    const cv = document.createElement("canvas");
    cv.width = w; cv.height = hh;
    const ctx = cv.getContext("2d");
    try { ctx.drawImage(img, 0, 0); } catch (e) { return null; }
    let dados;
    try { dados = ctx.getImageData(0, 0, w, hh).data; } catch (e) { return null; }
    const cheio = new Uint8Array(w * hh), fora = new Uint8Array(w * hh), fila = [];
    let algum = 0;
    for (let i = 0; i < w * hh; i++) algum += cheio[i] = dados[i * 4 + 3] > 0 ? 1 : 0;
    if (!algum) return null;  // nada desenhado ainda (a imagem não decodificou): não guarda o vazio
    const entra = (x, y) => { const i = y * w + x; if (!cheio[i] && !fora[i]) { fora[i] = 1; fila.push(i); } };
    for (let x = 0; x < w; x++) { entra(x, 0); entra(x, hh - 1); }
    for (let y = 0; y < hh; y++) { entra(0, y); entra(w - 1, y); }
    while (fila.length) {
      const i = fila.pop(), x = i % w, y = (i / w) | 0;
      if (x > 0) entra(x - 1, y); if (x < w - 1) entra(x + 1, y); if (y > 0) entra(x, y - 1); if (y < hh - 1) entra(x, y + 1);
    }
    const r = { w, hh, fora };
    if (src) silhuetas.set(src, r);
    return r;
  }
  /** O contorno de 1 pixel do desenho em volta da silhueta de fora (sem contornar furos), na cor do nível; a luz nas
   *  bordas de cima. Pintado num canvas fora da tela, um pixel maior de cada lado, e mostrado como imagem ampliada sem
   *  suavização junto com a peça (guardada por desenho e nível). */
  const contornos = new Map();
  function pintarContorno(el, sil, nivel, chave) {
    if (!contornos.has(chave)) {
      const [cor, luz] = CONTORNO[Math.min(nivel, 9)];
      const { w, hh, fora } = sil, cv = document.createElement("canvas");
      cv.width = w + 2; cv.height = hh + 2;
      const ctx = cv.getContext("2d");
      const dentro = (x, y) => x >= 0 && y >= 0 && x < w && y < hh && !fora[y * w + x];
      for (let y = -1; y <= hh; y++) for (let x = -1; x <= w; x++) {
        if (dentro(x, y)) continue;
        const baixo = dentro(x, y + 1), cima = dentro(x, y - 1), lado = dentro(x - 1, y) || dentro(x + 1, y);
        if (!baixo && !cima && !lado) continue;
        ctx.fillStyle = baixo && !cima && !lado ? luz : cor;  // a borda de cima, mais clara
        ctx.fillRect(x + 1, y + 1, 1, 1);
      }
      contornos.set(chave, cv.toDataURL());
    }
    el.src = contornos.get(chave);
  }
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
  /** O veio em pixel: as cores andam um pixel do desenho na diagonal a cada passo (um relógio só para todas as peças,
   *  cada uma na sua fase). Cada passo é um quadro pronto: o desenho, as faixas misturadas por cima em "overlay" (a
   *  mesma conta da mistura que antes era do CSS, mais forte nos níveis altos) e o recorte pela própria peça, pintados
   *  num canvas fora da tela, na resolução do desenho, e mostrados como imagem ampliada sem suavização por cima da peça.
   *  Com a mistura no CSS, o navegador compunha a peça num grupo à parte e a reamostrava: no resultado em destaque, o
   *  desenho borrava (a 125%, quase todo) e o borrão mudava quando o reflexo ou os brilhos passavam, como se a peça
   *  tremesse. Com o canvas na tela, a 125% ele também saía suavizado (a posição do resultado não cai num pixel inteiro
   *  e o navegador não encaixa o canvas como encaixa a imagem). Os quadros são guardados por desenho e nível. */
  const VEIO_FORCA = { 5: 0.45, 6: 0.5, 7: 0.5, 11: 0.6, 12: 0.65 };
  const quadrosVeio = new Map();
  function quadroVeio(img, nivel, fase) {
    const seq = VEIOS[nivel];
    if (!seq) return "";
    const chave = `${img.tagName === "IMG" ? img.currentSrc || img.src : (img._chave ||= img.toDataURL())}|${nivel}`;
    if (!quadrosVeio.has(chave)) quadrosVeio.set(chave, []);
    const lista = quadrosVeio.get(chave), i = ((fase % seq.length) + seq.length) % seq.length;
    if (lista[i]) return lista[i];
    const w = img.naturalWidth || img.width, hh = img.naturalHeight || img.height, cv = document.createElement("canvas");
    cv.width = w; cv.height = hh;
    const ctx = cv.getContext("2d");
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(img, 0, 0, w, hh);
    ctx.globalCompositeOperation = "overlay";
    ctx.globalAlpha = VEIO_FORCA[nivel] || 0.55;
    for (let d = 0; d < w + hh; d++) {
      const cor = seq[(d + i) % seq.length];
      if (!cor) continue;
      ctx.fillStyle = cor;
      for (let x = Math.max(0, d - hh + 1); x <= Math.min(d, w - 1); x++) ctx.fillRect(x, d - x, 1, 1);
    }
    ctx.globalCompositeOperation = "destination-in";  // só onde a peça tem pixel
    ctx.globalAlpha = 1;
    ctx.drawImage(img, 0, 0, w, hh);
    return (lista[i] = cv.toDataURL());
  }
  /* As armaduras do +9 ao +12 (capacete, peito, luvas, pernas, botas), 18ª: três alternativas jogáveis, escolhidas no
     painel de testes. O feixe da 17ª (uma passada estreita por volta) ficou discreto demais: do +8 para o +9 parecia
     perder força. As três partem da faixa do +8, que fica exatamente como está: a mesma presença (a força da mistura),
     a mesma largura (3 pixels do desenho e um pixel claro atrás) e a mesma frequência (uma faixa a cada 18 diagonais, o
     mesmo passo de 70 ms), sem intervalo longo. O nível cresce pelas cores, pela força (do +11) e pelos pontos de
     brilho, como nas armas; a passada periódica do reflexo também volta, como no +8. Cada passo é um quadro pronto
     (como o veio: sem mistura no CSS, sem ampliar); o contorno aprovado continua por cima.
       A · passadas alternadas: uma cor por faixa, na ordem do nível (o +9 rubi e depois âmbar; o +10 acrescenta o
           azul; o +11, a esmeralda; o +12, o violeta), nunca várias cores na mesma faixa;
       B · cor gradual: todas as faixas da peça na mesma cor, que passa devagar de uma cor do nível para a seguinte (três
           faixas por cor, ~3,8 s), sem faixas de cores diferentes ao mesmo tempo;
       C · reflexo principal e secundário: a faixa na cor principal do nível e, logo atrás, um reflexo de 1 pixel (2 no
           +11 e +12) na cor secundária: as duas cores da celebração daquele nível (+9 rubi e âmbar, +10 laranja e azul,
           +11 âmbar e esmeralda, +12 âmbar e violeta).
     No +12, o pixel claro de trás é marfim nas três. O feixe da 17ª e o veio anterior ficam no painel para comparar. */
  const ARMADURAS = new Set(["armadura", "cabeca", "maos", "pernas", "pes"]);
  const FEIXE = {  // a 17ª: as faixas do feixe, de um pixel cada, da frente para trás
    9: [R_, O_], 10: [R_, O_, A_], 11: [R_, O_, E_, A_], 12: [W_, R_, O_, E_, A_, V_],
  };
  const PERIODO_8 = 18;  // a faixa do +8 (VEIOS[8]): 3 pixels, 3 vazios, o pixel claro e 11 vazios
  const ARM_CORES = { 9: [R_, O_], 10: [R_, O_, A_], 11: [R_, O_, E_, A_], 12: [R_, O_, E_, A_, V_] };
  const ARM_PAR = { 9: [R_, O_], 10: ["#ff7a3c", A_], 11: [O_, E_], 12: [O_, V_] };  // C: as cores da celebração
  const ARM_GRADUAL = 3;  // B: faixas por cor
  const hexRgb = (c) => [1, 3, 5].map((k) => parseInt(c.slice(k, k + 2), 16));
  const rgbHex = (v) => `#${v.map((n) => Math.round(n).toString(16).padStart(2, "0")).join("")}`;
  const misturar = (a, b, t) => { const p = hexRgb(a), q = hexRgb(b); return rgbHex(p.map((v, k) => v + (q[k] - v) * t)); };
  const clarear = (c) => misturar(c, "#ffffff", 0.45);
  /** A faixa de uma alternativa no passo `i`: a cor de cada diagonal `d` (ou 0). O ciclo inteiro da alternativa. */
  function faixaArmadura(variante, nivel) {
    const n = Math.min(Math.max(nivel, 9), 12), luz = (c) => (n >= 12 ? W_ : clarear(c));
    // uma faixa de 18 diagonais, como a do +8: 3 pixels, 3 vazios, o pixel claro e o resto vazio
    const faixa = (c) => [...x(c, 3), ...z(3), luz(c), ...z(PERIODO_8 - 7)];
    if (variante === "a") return { seq: ARM_CORES[n].flatMap(faixa), ciclo: PERIODO_8 * ARM_CORES[n].length };
    if (variante === "c") {
      // C: a principal, um vazio e o secundário no lugar do pixel claro (no +12, o marfim ainda atrás dele)
      const [c1, c2] = ARM_PAR[n], larg = n >= 11 ? 2 : 1;
      const seq = [...x(c1, 3), 0, ...x(c2, larg), ...(n >= 12 ? [W_] : []), ...z(PERIODO_8 - 4 - larg - (n >= 12 ? 1 : 0))];
      return { seq, ciclo: PERIODO_8 };
    }
    return { gradual: ARM_CORES[n], ciclo: PERIODO_8 * ARM_GRADUAL * ARM_CORES[n].length };
  }
  function quadroArmadura(img, nivel, fase, variante) {
    const w = img.naturalWidth || img.width, hh = img.naturalHeight || img.height;
    const feixe17 = variante === "feixe", f = feixe17 ? null : faixaArmadura(variante, nivel);
    const ciclo = feixe17 ? w + hh : f.ciclo;  // a 17ª: uma passada por volta
    const i = ((fase % ciclo) + ciclo) % ciclo;
    const chave = `${img.currentSrc || img.src}|arm-${variante}|${nivel}`;
    if (!quadrosVeio.has(chave)) quadrosVeio.set(chave, []);
    const lista = quadrosVeio.get(chave);
    if (lista[i]) return lista[i];
    const cv = document.createElement("canvas");
    cv.width = w; cv.height = hh;
    const ctx = cv.getContext("2d");
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(img, 0, 0, w, hh);
    ctx.globalCompositeOperation = "overlay";  // a mesma mistura do veio
    ctx.globalAlpha = feixe17 ? VEIO_FORCA[8] || 0.55 : VEIO_FORCA[Math.min(nivel, 12)] || 0.55;
    const diagonal = (d, cor) => {
      ctx.fillStyle = cor;
      for (let x = Math.max(0, d - hh + 1); x <= Math.min(d, w - 1); x++) ctx.fillRect(x, d - x, 1, 1);
    };
    if (feixe17) (FEIXE[nivel] || FEIXE[9]).forEach((cor, k) => diagonal(i - k, cor));
    else if (f.gradual) {
      // B: a cor de agora entre duas do nível (suave na troca); as faixas andam como as do +8
      const por = PERIODO_8 * ARM_GRADUAL, k = Math.floor(i / por), t = (i % por) / por;
      const a = f.gradual[k % f.gradual.length], b = f.gradual[(k + 1) % f.gradual.length];
      const cor = misturar(a, b, t * t * (3 - 2 * t));
      const seq = [...x(cor, 3), ...z(3), nivel >= 12 ? W_ : clarear(cor), ...z(PERIODO_8 - 7)];
      for (let d = 0; d < w + hh; d++) { const c = seq[(d + i) % PERIODO_8]; if (c) diagonal(d, c); }
    } else for (let d = 0; d < w + hh; d++) { const c = f.seq[(d + i) % f.seq.length]; if (c) diagonal(d, c); }
    ctx.globalCompositeOperation = "destination-in";  // só onde a peça tem pixel
    ctx.globalAlpha = 1;
    ctx.drawImage(img, 0, 0, w, hh);
    return (lista[i] = cv.toDataURL());
  }
  /** A fase de uma peça: o relógio comum (um passo a cada PASSO_VEIO) mais um desvio fixo pelo lugar dela; um redesenho
   *  da tela não recomeça o ciclo nem o faz saltar (antes, cada elemento novo sorteava a fase). */
  const passoAgora = () => Math.floor(performance.now() / PASSO_VEIO);
  const desvio = (k) => { let h = 7; for (const c of String(k)) h = (h * 31 + c.charCodeAt(0)) >>> 0; return h % 97; };
  function pintarVeio(el) {
    const img = el._img;
    if (!img || (img.tagName === "IMG" && !(img.complete && img.naturalWidth))) return;
    const fase = (el._fase || 0) + (reduzido() ? 0 : passoAgora());
    const url = el._armadura ? quadroArmadura(img, +el.dataset.nivel, fase, el._armadura) : quadroVeio(img, el.dataset.nivel, fase);
    if (url && el.getAttribute("src") !== url) el.src = url;
  }
  // um passo a cada 70 ms (~14 por segundo): as faixas correm sobre a peça no ritmo das animações do jogo (a 250 ms,
  // o primeiro valor, pareciam paradas e aos saltos)
  const PASSO_VEIO = 70;
  setInterval(() => {
    if (document.hidden || reduzido()) return;
    document.querySelectorAll("img.rf-acab").forEach(pintarVeio);
  }, PASSO_VEIO);
  /** O espaço da peça de um encaixe (para o acabamento das armaduras): o que o elemento diz, ou a peça do dono. */
  const espacoDe = (caixa) => caixa.dataset.slot || (pecaDoDono(caixa) || {}).slot || "";
  function acabamento(caixa, n) {
    if (!caixa) return;
    const img = caixa.querySelector(":scope > img, :scope > canvas, :scope > .icone-px > img") || caixa.querySelector("img, canvas");
    const nivel = Math.min(n || 0, 12);
    if (nivel >= 4) caixa.dataset.acab = nivel; else delete caixa.dataset.acab;
    // o contorno do nível (do +4): só a silhueta de fora (antes, uma sombra contornava também o furo do anel)
    let contorno = caixa.querySelector(":scope > .rf-contorno");
    const sil = nivel >= 4 && img ? silhueta(img) : null;
    if (!sil) contorno?.remove();
    else {
      const chave = `${img.currentSrc || img.src || ""}|${Math.min(nivel, 9)}`;
      if (!contorno) {
        contorno = document.createElement("img");
        contorno.className = "rf-contorno";
        contorno.alt = "";
        contorno.draggable = false;
        contorno.setAttribute("aria-hidden", "true");
        caixa.appendChild(contorno);
      }
      if (contorno._chave !== chave) { contorno._chave = chave; pintarContorno(contorno, sil, nivel, chave); }
      const s = img.offsetWidth / sil.w;
      Object.assign(contorno.style, { left: `${img.offsetLeft - s}px`, top: `${img.offsetTop - s}px`, width: `${img.offsetWidth + 2 * s}px`, height: `${img.offsetHeight + 2 * s}px` });
    }
    const veio = caixa.querySelector(":scope > .rf-acab"), pontos = caixa.querySelector(":scope > .rf-acab-brilhos");
    if (nivel < 5 || !img) { veio?.remove(); pontos?.remove(); return; }
    // o desenho ainda carregando: o veio espera por ele (antes, a largura na tela, 80, passava pela do desenho, 40, e as
    // faixas saíam com meio pixel da peça)
    if (img.tagName === "IMG" && !(img.complete && img.naturalWidth)) { img.addEventListener("load", () => acabamento(caixa, n), { once: true }); return; }
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
        // cada peça num ponto da volta, pelo relógio comum (um redesenho continua de onde estava)
        el.style.animationDelay = `-${(((performance.now() / 1000) + desvio(src) / 11) % 9).toFixed(2)}s`;
        caixa.appendChild(el);
      }
      Object.assign(el.style, pos);
      return el;
    };
    const cv = camada(veio, "rf-acab", "img");
    cv._img = img;
    cv.alt = "";
    cv.draggable = false;
    // a fase fixa pelo lugar da peça (o id, o espaço, a posição na bolsa): o mesmo ponto da volta depois do redesenho
    const ds = caixa.dataset || {};
    cv._fase = desvio(`${ds.uid || ds.peca || ds.espaco || ds.mini || ds.mochila || ds.trPeca || ""}|${src}`);
    cv.dataset.nivel = nivel;
    const espaco = nivel >= 9 ? espacoDe(caixa) : "";
    // a armadura do +9 ao +12 com a alternativa escolhida no painel (A, B, C, o feixe da 17ª ou o veio anterior)
    const variante = document.body.dataset.rfArmadura;
    cv._armadura = ARMADURAS.has(espaco) && variante !== "anterior" ? variante : "";
    caixa.classList.toggle("rf-arm-feixe", !!cv._armadura);
    pintarVeio(cv);
    const k = cv._armadura === "feixe" ? (nivel >= 12 ? 1 : 0) : BRILHOS[nivel] || 0;  // o feixe da 17ª: só o marfim do +12
    if (!k) { pontos?.remove(); return; }
    const b = camada(pontos, "rf-acab-brilhos");
    const px = Math.max(1, Math.round(img.offsetWidth / (img.naturalWidth || img.width || 32)));  // um pixel do desenho
    b.style.setProperty("--px-peca", `${px}px`);
    if (b.childElementCount !== k) {
      b.innerHTML = Array.from({ length: k }, (_, i) => `<i style="animation-delay:-${(((performance.now() / 1000) + i * 0.4) % 1.6).toFixed(2)}s"></i>`).join("");
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
    // a vitrine das armaduras do painel de testes (18ª)
    document.querySelectorAll("#painel-testes .rf-vitrine-peca[data-reforco]").forEach((el) => lista.push([el, `vitrine:${el.dataset.vitrine}`, +el.dataset.reforco]));
    // a peça da apresentação do resultado também (o reflexo continua passando enquanto ela está na tela)
    document.querySelectorAll(".rf-janela .rf-esteira .rf-peca, .rf-janela .rf-chapa .rf-encaixe.grande[data-reforco], #rf-res .rf-res-arte[data-reforco]").forEach((el) => {
      lista.push([el, el.closest("#rf-res") ? `resultado:${el.dataset.reforco}` : `forja:${el.dataset.uid || "molde"}:${el.getAttribute("aria-label") || ""}:${el.dataset.reforco}`, +el.dataset.reforco || 0]);
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

  /* A piscada ao reforçar (16ª): a cada pedido, o motor redesenha a forja como uma cena nova (a página se limpa) e o
     painel chega na mensagem seguinte; se elas não caem no mesmo quadro (o motor demora a calcular o painel, a
     mensagem chega em outro pedaço), o navegador pintava a oficina sem a janela. A janela que estava na tela fica
     onde está, parada e sem receber cliques, até a nova estar montada (ligar). Nada espera tempo nenhum: ela sai no
     mesmo passo em que a outra entra. */
  let segura = null;
  function segurarJanela() {
    const velha = document.querySelector(".tela.forja-proto");
    if (!velha || !velha.querySelector(".rf-janela") || segura) return;
    segura = document.createElement("div");
    segura.className = "rf-segura";
    segura.setAttribute("aria-hidden", "true");
    document.body.appendChild(segura);
    segura.appendChild(velha);  // a janela é fixa na tela: sai do texto sem sair do lugar
  }
  function soltarJanela() { if (segura) { segura.remove(); segura = null; } }
  if (typeof novaCena === "function" && !window.__rfNovaCena) {
    window.__rfNovaCena = true;
    const novaCenaJogo = novaCena;
    window.novaCena = (m) => {
      if (m && m.tipo === "menu" && janela) segurarJanela(); else soltarJanela();
      return novaCenaJogo(m);
    };
  }

  let ultimoDesenho = null, ultimoRaiz = null, saldoAntes = null, ultimaPos = null;
  const saldoMudou = {};  // o recurso → {t0, sentido}: o último saldo que mudou (o destaque dura 1,4 s)
  function ligar(raiz, d) {
    enviando = false;
    // a janela nova já está montada: a antiga, guardada na troca de cena, sai no mesmo passo (requestAnimationFrame
    // depois do anexo, para nenhum quadro ficar sem as duas)
    if (segura) { const s = segura; segura = null; requestAnimationFrame(() => s.remove()); }
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
    const limpar = () => { revelar(); encerrarGrav(); if (transf) { transf.fim = true; fecharRes(); } mostrarId = 0; focoDepois = null; };
    const abrir = (qual, foco) => { janela = qual; selUid = null; confirmando = null; trOrigem = trDestino = trSeletor = null; trAviso = ""; confirmandoTransf = null; limpar(); redesenhar(foco || ".rf-janela .rf-peca, .rf-janela [data-tr-abrir='origem'], .rf-janela [data-fechar]"); };
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
    // 18ª: o destaque continua pelo tempo decorrido nos redesenhos seguintes (antes, o segundo desenho o cortava no meio)
    const agoraS = performance.now();
    if (saldoAntes) Object.keys(saldos).forEach((k) => {
      if (saldoAntes[k] !== undefined && saldoAntes[k] !== saldos[k]) saldoMudou[k] = { t0: agoraS, sentido: saldos[k] < saldoAntes[k] ? "desce" : "sobe" };
    });
    jan.querySelectorAll(".rf-rec[data-rec]").forEach((el) => {
      const m = saldoMudou[el.dataset.rec];
      if (!m || agoraS - m.t0 > 1400) return;
      el.classList.add(m.sentido);
      el.style.setProperty("--rf-e", `-${Math.round(agoraS - m.t0)}ms`);
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
    const ft = janela === "transferir" ? faseTransf() : "";
    if (ft) {
      jan.classList.add("em-cena");
      document.body.classList.add("rf-em-cena");
      if (ft === "anim") {
        // a luz sai da origem e chega ao destino; a origem perde o acabamento e o destino recebe o nível novo (a transação
        // já está feita: as etapas só mostram)
        const e = performance.now() - transf.t0, u = transf.u;
        const caixa = (lado) => jan.querySelector(`[data-tr-peca="${lado}"]`);
        relogios.push(setTimeout(() => { const c = caixa("origem"); if (c) reflexo(c, u.de_origem, true); }, Math.max(0, 80 - e)));
        relogios.push(setTimeout(() => { const c = caixa("origem"); if (c) { c.dataset.reforco = 0; acabamento(c, 0); c.querySelector(".rf-reflexo")?.remove(); } }, Math.max(0, 760 - e)));
        relogios.push(setTimeout(() => { const c = caixa("destino"); if (c) { c.dataset.reforco = u.novo; acabamento(c, u.novo); reflexo(c, u.novo, true); } }, Math.max(0, 1000 - e)));
        relogios.push(setTimeout(() => { if (raiz.isConnected) redesenhar(); }, TRANSF_MS - e));
      } else requestAnimationFrame(() => apresentarTransferencia(transf));
    }
    if (desmonte && janela === "desmontar" && performance.now() - desmonte.t0 < DESMONTE_MS) {
      if (!desmonte.fx) { desmonte.fx = true; requestAnimationFrame(() => fragmentar()); }
      relogios.push(setTimeout(() => { desmonte.t0 = -Infinity; pararDesmonte(); redesenhar(focoDepois); }, DESMONTE_MS - (performance.now() - desmonte.t0)));
    } else if (fxDesmonte) pararDesmonte();
    ligarReflexos(jan);
    window.dispatchEvent(new Event("reforco-comparacao"));
    // durante a cena, um clique na bancada só revela: não compra, não escolhe, não desmonta (Enter e Espaço, no
    // ouvinte do documento, lá embaixo). Fechar, trocar de serviço, de dono ou de peça continuam valendo (o motor já
    // resolveu a tentativa).
    jan.addEventListener("click", (ev) => {
      if (resto(ev) && !ev.target.closest("[data-fechar], [data-janela]")) { ev.preventDefault(); ev.stopPropagation(); return; }  // o resto do gesto que agiu
      if (faseTransf() && !ev.target.closest("[data-fechar], [data-janela]")) {  // Fechar e as abas continuam valendo
        ev.preventDefault(); ev.stopPropagation();
        adiantarTransf();
        return;
      }
      if (!fase() && !faseGrav()) return;
      if (ev.target.closest("[data-fechar], [data-janela], [data-aba], [data-uid]")) return;
      ev.preventDefault();
      ev.stopPropagation();
      if (faseGrav() === "traco") adiantarGrav(); else if (fase() === "forja") adiantar(d.ultimo);  // no resultado, só o OK
    }, true);
    jan.querySelector("[data-fechar]").addEventListener("click", fechar);
    // as dicas dos materiais e da ajuda também abrem pelo foco do teclado (o jogo só faz isso no mercado)
    jan.querySelectorAll(".rf-req-item, .rf-ajuda, .rf-chapa [data-retirar][data-dica]").forEach((el) => {
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
      if (selUid !== b.dataset.uid) { selUid = b.dataset.uid; confirmando = null; confirmandoTransf = null; brilharSel = true; limpar(); redesenhar(`[data-uid="${b.dataset.uid}"]`); }
      else if (!resto(ev)) { selUid = null; confirmando = null; confirmandoGrav = null; confirmandoRem = null; limpar(); redesenhar(`[data-uid="${b.dataset.uid}"]`); }  // de novo: retira
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
      if (resto(ev)) return;  // o segundo clique de um duplo clique não compra outro passo
      if (ref.getAttribute("aria-disabled")) { App.recusar(ref, ref.title); return; }
      const x = passoDe(p);
      pago = { de: p.reforco, chance: x.chance, linhas: x.linhas, ouro: x.ouro, fragmentos: x.fragmentos, requer: x.requer };
      const pedido = `t${Date.now()}`;
      const teste = testeProximo;
      if (pedir({ op: "reforcar", uid: p.uid, pedido, ...(teste ? { teste } : {}) }, ref,
        "[data-reforcar]:not([aria-disabled]), [data-uid].marcada")) {
        esperandoId = d.proximo_id;  // o número que o motor vai dar (não recomeça depois dos cenários de teste)
        testeProximo = null;
        window.dispatchEvent(new Event("reforco-teste"));
      }
    });
    // a transferência: abrir o seletor de um lado, escolher a peça, pedir a confirmação, confirmar
    jan.querySelectorAll("[data-tr-abrir]").forEach((b) => b.addEventListener("click", (ev) => {
      if (resto(ev) || b.getAttribute("aria-disabled")) return;
      trSeletor = trSeletor === b.dataset.trAbrir ? null : b.dataset.trAbrir;
      confirmandoTransf = null;
      redesenhar(trSeletor ? `.rf-tr-seletor .rf-tr-op:not(.apagada), [data-tr-abrir="${b.dataset.trAbrir}"]` : `[data-tr-abrir="${b.dataset.trAbrir}"]`);
    }));
    jan.querySelectorAll("[data-tr-escolher]").forEach((b) => b.addEventListener("click", (ev) => {
      if (resto(ev) || b.getAttribute("aria-disabled")) { if (b.title) App.recusar(b, b.title); return; }
      const uid = b.dataset.trEscolher;
      trAviso = "";
      if (trSeletor === "origem") {
        if (trOrigem !== uid) {
          trOrigem = uid;
          const o = d.pecas.find((x) => x.uid === uid), ok = o && o.transferir.destinos.find((x) => x.uid === trDestino && !x.motivo);
          if (trDestino && !ok) { trDestino = null; trAviso = "O destino escolhido não serve para esta origem: escolha outro."; }
        }
        trSeletor = trDestino ? null : "destino";  // depois da origem, os destinos que ela aceita
      } else { trDestino = uid; trSeletor = null; }
      confirmandoTransf = null;
      redesenhar(trSeletor ? ".rf-tr-seletor .rf-tr-op:not(.apagada), [data-tr-abrir='destino']" : "[data-transferir]:not([aria-disabled]), [data-tr-abrir='destino']");
    }));
    jan.querySelector("[data-tr-fechar-lista]")?.addEventListener("click", () => { const lado = trSeletor; trSeletor = null; redesenhar(`[data-tr-abrir="${lado}"]`); });
    jan.querySelector(".rf-tr-lista")?.addEventListener("keydown", (ev) => {
      if (!["ArrowUp", "ArrowDown"].includes(ev.key)) return;
      const todas = [...jan.querySelectorAll(".rf-tr-op")], i = todas.indexOf(document.activeElement);
      ev.preventDefault();
      todas[(i + (ev.key === "ArrowUp" ? -1 : 1) + todas.length) % todas.length]?.focus();
    });
    const trf = jan.querySelector("[data-transferir]");
    if (trf) trf.addEventListener("click", (ev) => {
      if (resto(ev)) return;
      if (trf.getAttribute("aria-disabled")) { if (trf.title) App.recusar(trf, trf.title); return; }
      confirmandoTransf = { origem: trOrigem, destino: trDestino };
      redesenhar("[data-transferir-nao]");
    });
    const tNao = jan.querySelector("[data-transferir-nao]");
    if (tNao) tNao.addEventListener("click", () => { confirmandoTransf = null; redesenhar("[data-transferir]"); });
    const tSim = jan.querySelector("[data-transferir-sim]");
    if (tSim) {
      const arma = performance.now() + 400;  // o clique que abriu a pergunta não a responde
      setTimeout(() => { if (tSim.isConnected) tSim.disabled = false; }, 400);
      tSim.addEventListener("click", (ev) => {
        if (tSim.disabled || performance.now() < arma || resto(ev) || !confirmandoTransf) return;
        const c = confirmandoTransf;
        confirmandoTransf = null;
        if (pedir({ op: "transferir", origem: c.origem, destino: c.destino, pedido: `x${Date.now()}`, confirmar: true }, tSim, "[data-tr-abrir='origem']")) {
          esperandoId = d.proximo_id;  // o número que o motor vai dar (não recomeça depois dos cenários de teste)
        }
      });
    }
    // o encantamento: escolher a essência, gravar (ou pedir a confirmação da substituição), confirmar
    jan.querySelectorAll("[data-essencia]").forEach((b) => b.addEventListener("click", () => {
      if (essSel !== b.dataset.essencia) { essSel = b.dataset.essencia; confirmandoGrav = null; confirmandoRem = null; limpar(); redesenhar(`[data-essencia="${b.dataset.essencia}"]`); }
    }));
    jan.querySelectorAll("[data-sulco]").forEach((b) => b.addEventListener("click", () => {
      if (sulcoSel !== +b.dataset.sulco) { sulcoSel = +b.dataset.sulco; confirmandoGrav = null; confirmandoRem = null; limpar(); redesenhar(`[data-sulco="${b.dataset.sulco}"]`); }
    }));
    // a remoção (18ª): pedir a confirmação, cancelar, confirmar (uma vez: o pedido leva um número e a gravação que a tela
    // mostrava; o motor recusa o repetido e a gravação que já mudou)
    const remB = jan.querySelector("[data-remover]");
    if (remB) remB.addEventListener("click", (ev) => {
      if (resto(ev) || remB.getAttribute("aria-disabled")) return;
      if (confirmandoRem) { confirmandoRem = null; redesenhar("[data-remover]"); return; }
      confirmandoRem = { uid: p.uid, sulco: sulcoSel }; confirmandoGrav = null; redesenhar("[data-remover-nao]");
    });
    const rNao = jan.querySelector("[data-remover-nao]");
    if (rNao) rNao.addEventListener("click", () => { confirmandoRem = null; redesenhar("[data-remover]"); });
    const rSim = jan.querySelector("[data-remover-sim]");
    if (rSim) {
      const arma = performance.now() + 400;  // o clique que abriu a pergunta não a responde
      setTimeout(() => { if (rSim.isConnected) rSim.disabled = false; }, 400);
      rSim.addEventListener("click", (ev) => {
        if (rSim.disabled || performance.now() < arma || resto(ev) || !confirmandoRem) return;
        const c = confirmandoRem, atual = (p.encantos || [])[c.sulco];
        confirmandoRem = null;
        if (!atual) return;
        if (pedir({ op: "remover_encanto", uid: p.uid, sulco: c.sulco, pedido: `r${Date.now()}`, remove: atual.id }, rSim, `[data-sulco="${c.sulco}"]`)) {
          esperandoId = d.proximo_id;
        }
      });
    }
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
        esperandoId = d.proximo_id;  // o número que o motor vai dar (não recomeça depois dos cenários de teste)
      }
    };
    const grav = jan.querySelector("[data-gravar]");
    if (grav) grav.addEventListener("click", (ev) => {
      if (resto(ev)) return;
      if (grav.getAttribute("aria-disabled")) { if (grav.title) App.recusar(grav, grav.title); return; }
      if ((p.encantos || [])[sulcoSel]) { confirmandoGrav = { uid: p.uid }; confirmandoRem = null; redesenhar("[data-gravar-nao]"); return; }
      pedirGravacao(grav);
    });
    const gNao = jan.querySelector("[data-gravar-nao]");
    if (gNao) gNao.addEventListener("click", () => { confirmandoGrav = null; redesenhar("[data-gravar]"); });
    const gSim = jan.querySelector("[data-gravar-sim]");
    if (gSim) {
      const arma = performance.now() + 400;  // o clique que abriu a pergunta não a responde
      setTimeout(() => { if (gSim.isConnected) gSim.disabled = false; }, 400);
      gSim.addEventListener("click", (ev) => {
        if (gSim.disabled || performance.now() < arma || resto(ev) || !confirmandoGrav) return;
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
        selUid = null; confirmando = null; confirmandoGrav = null; confirmandoRem = null;
        limpar();
        redesenhar(`[data-uid="${uid}"]`);
      };
      ret.addEventListener("click", (ev) => { if (!resto(ev)) tirar(); });
      ret.addEventListener("keydown", (ev) => { if ((ev.key === "Enter" || ev.key === " ") && !ev.repeat) { ev.preventDefault(); tirar(); } });
    }
    const des = jan.querySelector("[data-desmontar]");
    if (des) des.addEventListener("click", (ev) => {
      if (resto(ev)) return;
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
        if (sim.disabled || performance.now() < arma || resto(ev) || !confirmando) return;
        const c = confirmando;
        confirmando = null;
        selUid = null;  // depois de desmontar, nada fica escolhido
        pedidoDesmonte = { icone: iconePeca(p.item), raridade: p.item.raridade };
        if (pedir({ op: "desmontar", uid: c.uid, nome: c.nome, confirmar: true }, sim, ".rf-janela .rf-peca, .rf-janela [data-fechar]")) {
          esperandoId = d.proximo_id;  // o número que o motor vai dar (não recomeça depois dos cenários de teste)
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
    if ((ev.key !== "Enter" && ev.key !== " ") || !janela || (!fase() && !faseGrav() && !faseTransf()) || !document.querySelector(".rf-janela")) return;
    ev.preventDefault();
    ev.stopImmediatePropagation();
    if (!ev.repeat) {
      if (faseTransf() === "anim") adiantarTransf(); else if (faseTransf()) { teclaDispensou = ev.key; dispensarTransf(); }
      else if (faseGrav() === "traco") adiantarGrav(); else if (faseGrav()) { teclaDispensou = ev.key; dispensarGrav(); }
      else if (fase() === "forja") adiantar(ultimoDesenho && ultimoDesenho.ultimo); else { teclaDispensou = ev.key; dispensar(); }
    }
  }, true);
  // a tecla que dispensou, ao ser solta, não aperta o botão que recebeu o foco (o Espaço clica no keyup)
  document.addEventListener("keyup", (ev) => {
    if (!teclaDispensou || ev.key !== teclaDispensou) return;
    ev.preventDefault();
    setTimeout(() => { teclaDispensou = null; });  // depois do clique que o keyup geraria
  }, true);

  // Esc com a janela aberta: revela a cena, cancela a confirmação, fecha a janela; só então o Voltar da forja.
  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape" || !janela || !document.querySelector(".rf-janela")) return;
    ev.preventDefault();
    ev.stopImmediatePropagation();
    if (fase() === "forja") { adiantar(ultimoDesenho && ultimoDesenho.ultimo); return; }
    if (fase() === "desfecho") { dispensar(); return; }
    if (faseTransf() === "anim") { adiantarTransf(); return; }
    if (faseTransf()) { dispensarTransf(); return; }
    if (trSeletor) { const lado = trSeletor; trSeletor = null; if (ultimoRaiz && ultimoDesenho) ultimoRaiz.replaceWith(Telas.painel({ tipo: "forja_proto", dados: ultimoDesenho })); document.querySelector(`[data-tr-abrir="${lado}"]`)?.focus(); return; }
    if (faseGrav() === "traco") { adiantarGrav(); return; }
    if (faseGrav()) { dispensarGrav(); return; }
    if (confirmando) { document.querySelector("[data-desmontar-nao]")?.click(); return; }
    if (confirmandoGrav) { document.querySelector("[data-gravar-nao]")?.click(); return; }
    if (confirmandoRem) { document.querySelector("[data-remover-nao]")?.click(); return; }
    if (confirmandoTransf) { document.querySelector("[data-transferir-nao]")?.click(); return; }
    document.querySelector(".rf-janela [data-fechar]")?.click();
  }, true);

  Telas.registrar("forja_proto", balcao, { ligar, esquecer: () => { janela = null; selUid = null; confirmando = null; confirmandoGrav = null; confirmandoRem = null; trOrigem = trDestino = trSeletor = null; confirmandoTransf = null; if (transf) transf.fim = true; revelar(); assentarGrav(); mostrarId = 0; aba = "heroi"; } });

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
    /** As composições de essências de teste (laboratório). Só com a forja aberta. */
    essenciasTeste() {
      if (!document.querySelector(".forja-proto")) return false;
      revelar();
      return !!App.acao({ forja: true }, null, { op: "essencias_teste" });
    },
    /** O grupo 4 níveis acima, sem a festa (laboratório: os requisitos de tier II e III). Só com a forja aberta. */
    nivelTeste() {
      if (!document.querySelector(".forja-proto")) return false;
      revelar();
      return !!App.acao({ forja: true }, null, { op: "nivel_teste" });
    },
    /** As peças de teste da transferência (laboratório). Só com a forja aberta. */
    transferenciaTeste() {
      if (!document.querySelector(".forja-proto")) return false;
      revelar();
      return !!App.acao({ forja: true }, null, { op: "transferencia_teste" });
    },
    /** O painel de testes (16ª): os valores de agora (do motor), as candidatas visuais e o pedido de aplicar. */
    estadoTeste: () => (ultimoDesenho && ultimoDesenho.teste) || null,
    /** O último resultado do motor (a conferência dos gestos conta por ele: uma tentativa, um número). */
    ultimo: () => (ultimoDesenho && ultimoDesenho.ultimo) || null,
    pref, preferir,
    /** Por que o painel não pode aplicar agora (uma tentativa, uma cena ou uma confirmação em andamento), ou "". */
    ocupado() {
      if (!document.querySelector(".forja-proto")) return "Abra a forja para aplicar.";
      if (enviando || fase() || faseGrav() || faseTransf() || res) return "Espere o resultado atual (OK) para aplicar.";
      if (confirmando || confirmandoGrav || confirmandoRem || confirmandoTransf) return "Responda à confirmação aberta antes de aplicar.";
      return "";
    },
    aplicarTeste(op, dados) {
      const motivo = this.ocupado();
      if (motivo) return motivo;
      if (op === "teste_cenario") { selUid = null; trOrigem = trDestino = null; essSel = null; }  // as peças de antes saem
      return App.acao({ forja: true }, null, { op, ...dados }) ? "" : "Agora não dá para pedir à forja.";
    },
    /** A vitrine das armaduras (18ª, painel de testes): as cinco peças que o herói veste (ou as do jogo, se faltar uma),
     *  cada uma do +8 ao +12, com a alternativa escolhida; o ciclo da página anima e passa o reflexo como nas outras. */
    vitrineArmaduras() {
      const eq = (App.estado && App.estado.heroi && App.estado.heroi.equip) || {};
      const padrao = { cabeca: "elmo", armadura: "armadura", maos: "manopla", pernas: "calca", pes: "bota_ferro" };
      const nomes = { cabeca: "Cabeça", armadura: "Peito", maos: "Mãos", pernas: "Pernas", pes: "Pés" };
      return `<div class="rf-vitrine" role="img" aria-label="Armaduras do +8 ao +12 com o acabamento escolhido">
        <div class="rf-vitrine-linha"><span></span>${[8, 9, 10, 11, 12].map((n) => `<b>+${n}</b>`).join("")}</div>
        ${Object.keys(padrao).map((slot) => {
          const ic = (eq[slot] && eq[slot].icone) || padrao[slot];
          return `<div class="rf-vitrine-linha"><span>${nomes[slot]}</span>${[8, 9, 10, 11, 12].map((n) =>
            `<span class="rf-vitrine-peca" data-slot="${slot}" data-reforco="${n}" data-vitrine="${slot}-${n}">${Icones.equipamento(ic, 40)}</span>`).join("")}</div>`;
        }).join("")}</div>`;
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
  /** A ficha de item na ordem da forja (as fichas do Diablo como referência de hierarquia, com a arte do jogo): o nome
   *  com o reforço; o tipo e a raridade (a base sai dos parênteses do nome e vai para a linha do tipo: "Machado ·
   *  Lendário", sem "(Machado)" no título); os atributos e afixos; os sulcos e os efeitos; o requisito de nível; depois o
   *  resto do jogo (a comparação, o motivo de não usar, o texto de sabor). Em DOM: serve à ficha montada (htmlItem), à
   *  dica que abre e ao achado. `detalhes`: os Detalhes por clique (não nas dicas, que somem). */
  function arrumarFicha(raiz, it, detalhes = true) {
    if (!raiz || !it || raiz.querySelector(":scope > .rf-encantos, :scope > .rf-req, :scope > .rf-arrumada")) return;
    const titulo = raiz.querySelector(":scope > b"), tipo = raiz.querySelector(":scope > .tipo");
    const base = it.base && titulo && titulo.lastChild && titulo.lastChild.nodeType === 3 && titulo.lastChild.textContent.endsWith(` (${it.base})`);
    if (base && tipo) {
      titulo.lastChild.textContent = titulo.lastChild.textContent.slice(0, -(it.base.length + 3));
      tipo.textContent = tipo.textContent.replace(/^[^·]*·/, `${it.base} ·`);
    }
    const depois = raiz.querySelector(":scope > .efeito-item") || raiz.querySelector(":scope > .bonus") || tipo || titulo;
    if (!depois) return;
    depois.insertAdjacentHTML("afterend", `${secaoEncantos(it.encantos, it.efeitos, detalhes)}${reqHtml(it.requisito)}<i class="rf-arrumada" hidden></i>`);
  }
  const htmlItemJogo = Telas.htmlItem;
  Telas.htmlItem = (it, ...resto) => {
    const t = document.createElement("div");
    t.innerHTML = htmlItemJogo(it, ...resto);
    arrumarFicha(t, it);
    return t.innerHTML;
  };
  /* O achado (a janela "Você encontrou") monta a ficha em pedaços (Festa.fichaItem), sem o htmlItem: os sulcos da peça
     achada entram debaixo das linhas dela quando a janela aparece, pela peça que a mensagem trouxe. */
  let achado = null;
  const abrirAchadoJogo = Telas.abrirAchado;
  Telas.abrirAchado = (d, ...resto) => { achado = d && d.item; return abrirAchadoJogo(d, ...resto); };
  /** O acabamento do reforço no item achado (a arte grande da janela "Você encontrou"). */
  function acabamentoNoAchado() {
    const arte = achado && achado.reforco && document.querySelector("#sobre-achado .achado-cartao.novo .achado-arte");
    if (arte) { arte.style.position ||= "relative"; arte.dataset.slot = achado.slot || ""; acabamento(arte, achado.reforco); }
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
    if (!alvo || (alvo.nextElementSibling && alvo.nextElementSibling.matches(".rf-encantos, .rf-req"))) return;
    const sec = secaoEncantos(achado.encantos, achado.efeitos) + reqHtml(achado.requisito);
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
    if (id && ultimoDesenho) { const x = ultimoDesenho.pecas.find((q) => q.uid === id); if (x) return { ...x.item, encantos: x.encantos, efeitos: x.efeitos, requisito: x.requisito, reforco: x.reforco }; }
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
  /** Na dica: tira o rodapé fixo de instrução ("Clique para ver as ações…", "Clique para comprar…"): os gestos
   *  continuam, a instrução fica no controle e na ajuda. No Inventário, a peça já marcada tem a ficha ao lado: a dica
   *  completa em cima dela repetiria a mesma ficha, então não abre. */
  function dicaSemRepeticao() {
    const caixa = document.getElementById("dica-item");
    if (!caixa || caixa.hidden) return;
    caixa.querySelectorAll(".rodape").forEach((r) => { if (/^Clique/.test(r.textContent.trim())) r.remove(); });
    const dono = caixa._dono;
    if (dono && dono.classList && dono.classList.contains("marcado") && dono.closest(".tela.inventario")) caixa.hidden = true;
  }
  function sulcosNaDica() {
    const caixa = document.getElementById("dica-item");
    if (!caixa || caixa.hidden || caixa.querySelector(":scope > .rf-arrumada")) return;
    if (!caixa.querySelector(":scope > b")) return;
    // a peça pelo dono da dica (a forja, o Equipado, a bolsa, o mercado) ou pela que a dica guardou
    const it = pecaDoDono(caixa._dono) || caixa._item;
    if (it && (it.encantos || it.requisito > 1)) arrumarFicha(caixa, it, false);
    dentroDaJanela(caixa);
  }
  /** A dica inteira na janela: acima da doca e do fim da tela; quando a ficha cresce (os sulcos entram depois de ela
   *  abrir), ela sobe até caber; maior que o espaço, rola por dentro, sem diminuir a letra. */
  function dentroDaJanela(caixa) {
    caixa.style.maxHeight = "";
    caixa.classList.remove("rf-rola");
    const r = caixa.getBoundingClientRect(), doca = document.getElementById("doca");
    const d = doca && doca.offsetParent ? doca.getBoundingClientRect() : null;
    const fundo = (d && r.left < d.right && r.right > d.left ? Math.min(d.top, innerHeight) : innerHeight) - 6;
    const alto = fundo - 6;
    if (r.height > alto) { caixa.style.maxHeight = `${alto}px`; caixa.classList.add("rf-rola"); }
    const h = Math.min(r.height, alto);
    if (r.top + h > fundo || r.top < 6) caixa.style.top = `${Math.max(6, fundo - h)}px`;
  }
  /** O requisito à vista no Inventário: as peças da bolsa (e as opções de um espaço) acima do nível do grupo ficam
   *  apagadas, e o Equipar da peça marcada fica bloqueado com o motivo (o motor recusa de qualquer jeito). */
  function requisitoNoInventario() {
    const tela = document.querySelector(".tela.inventario");
    if (!tela) return;
    const nv = nivelGrupo();
    tela.querySelectorAll("[data-mochila], .peca-opcao").forEach((el) => {
      const it = pecaDoDono(el);
      el.classList.toggle("rf-req-falta", !!it && (it.requisito || 0) > nv);
    });
    const marcada = tela.querySelector(".marcado");
    const it = marcada && pecaDoDono(marcada);
    if (!it || (it.requisito || 0) <= nv) return;
    tela.querySelectorAll(".detalhe-acoes .acao-peca").forEach((b) => {
      if (!/^Equipar/.test(b.textContent) || b.classList.contains("rf-req-bloq")) return;
      b.classList.add("bloqueada", "rf-req-bloq");
      b.setAttribute("aria-disabled", "true");
      b.title = `Requer nível ${it.requisito}.`;
    });
  }
  // o Equipar bloqueado pelo nível diz o motivo e não pede nada
  document.addEventListener("click", (ev) => {
    const b = ev.target.closest && ev.target.closest(".acao-peca.rf-req-bloq");
    if (!b) return;
    ev.preventDefault();
    ev.stopImmediatePropagation();
    App.recusar(b, b.title);
  }, true);
  /** O tier no canto das essências achadas (o quadro do espólio mostra o símbolo e o nome). */
  function tierNoEspolio() {
    document.querySelectorAll(".achado-espolio:not(.rf-ess-visto)").forEach((el) => {
      el.classList.add("rf-ess-visto");
      const m = /Essência de \S+ (I{1,3})\b/.exec(el.textContent);
      const ic = el.querySelector("img, canvas, svg");
      if (!m || !ic) return;
      const caixa = Object.assign(document.createElement("span"), { className: "rf-ess-ic" });
      ic.replaceWith(caixa);
      caixa.append(ic, Object.assign(document.createElement("span"), { className: "rf-tier-selo", textContent: m[1] }));
    });
  }

  /* A seção "Materiais" no inventário: as pilhas do grupo, fora dos espaços da bolsa. */
  function materiaisNoInventario() {
    const lado = document.querySelector(".tela.inventario .inv-lado");
    const mats = App.estado && App.estado.heroi && App.estado.heroi.materiais;
    if (!lado || !mats || lado.querySelector(".ref-mat-inv")) return;
    const bolsa = [...lado.querySelectorAll("h4")].find((x) => /^Bolsa$/.test(x.textContent.trim()));
    const slots = bolsa && bolsa.nextElementSibling;
    if (!slots) return;
    const html = `<h4>Materiais</h4><div class="slots ref-mat-inv">${mats.map((m) =>
      `<div class="slot-px" tabindex="0" ${Telas.dica(`<b>${h(m.nome)}</b><div>${h(m.desc)}</div>${m.requisito > 1 ? `<div>Requer nível ${m.requisito}.</div>` : ""}<div class="rodape">${h(m.fontes)}</div>`)}>${m.numeral ? icEss(m) : iconeDe(m.icone)}<span class="qtd">${m.qtd}</span></div>`).join("")}</div>`;
    slots.insertAdjacentHTML("afterend", html);
    Telas.ligarDicas(lado.querySelector(".ref-mat-inv"));
  }
  new MutationObserver(() => { materiaisNoInventario(); sulcosNaDica(); dicaSemRepeticao(); sulcosNoAchado(); requisitoNoInventario(); tierNoEspolio(); decorar(); }).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ["hidden"] });
})();
