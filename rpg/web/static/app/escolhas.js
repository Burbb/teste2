"use strict";

/* ------------------------------------------------------------------ escolhas */
/* A doca de atalhos (Talentos, Grimório, Inventário...) mora numa barra fixa sob a página, não no meio do texto.
   Ela acende nos menus de lugar e continua acesa dentro das telas que ela mesma abriu (Inventário, Comitiva...):
   dali, clicar noutro atalho volta ao lugar e abre o outro sozinho. Em eventos e na luta, fica apagada,
   com o Grimório e o Mapa ainda à mão. */
const doca = $("#doca");
let docaSono = 0;
let docaTela = null;  // o atalho cuja tela está aberta agora (null: no menu do lugar ou fora da doca)
function montarDoca(atalhos, manter = false) {
  clearTimeout(docaSono);
  if (!manter) docaTela = null;  // numa tela aberta pela doca (que tem Voltar), ela continua sabendo qual é
  doca.replaceChildren(atalhos);
  doca.classList.remove("inativa");
  doca.dataset.viva = "1";
  Telas.ligarDicas(doca);
}
function marcarDocaAtual() {
  doca.querySelectorAll(".atalho").forEach((b) => b.classList.toggle("atual", !!docaTela && b.dataset.rotulo === docaTela));
}
/* Clicou num atalho (Talentos piscando depois de subir de nível...) enquanto a cena ainda não acabou: o aviso diz
   o que falta, e só. A tela não abre sozinha depois (abrir no meio de outra coisa confundia mais do que ajudava). */
const PARA_ABRIR = { Talentos: "abrir os Talentos", "Inventário": "abrir o Inventário", Comitiva: "abrir a Comitiva", Mapa: "abrir o Mapa",
  "Diário": "abrir o Diário", "Bestiário": "abrir o Bestiário", Salvar: "salvar", Sair: "sair" };
/** "Termine a cena para abrir os Talentos": aparece a cada clique (não só no primeiro), sem empilhar. */
function avisarAtalho(rotulo, onde = estado && estado.combate ? "a luta" : "a cena") {
  aviso(`Termine ${onde} para ${PARA_ABRIR[rotulo] || "abrir " + rotulo}`, "info", rotulo === "Talentos" ? "estrela" : "pergaminho", "atalho");
}
function recusarAtalho(rotulo) {
  Som.tocar("falha");
  avisarAtalho(rotulo);
}
function atalhoNoMenu(opcoes, rotulo) {
  return opcoes.findIndex((o) => { const at = atalhoDe(o); return at && at[1] === rotulo; });
}
const menuDoLugar = (opcoes) => opcoes.filter((o) => atalhoDe(o)).length >= 4;
/** Abrir um atalho de qualquer lugar (aviso de talento no painel, tecla): usa o botão da doca se houver. */
function pedirAtalho(rotulo) {
  const b = doca.querySelector(`.atalho[data-rotulo="${rotulo}"]`);
  if (b) { b.click(); return; }
  if (pergunta && pergunta.tipo === "opcoes" && !processando && menuDoLugar(pergunta.opcoes)) return;
  recusarAtalho(rotulo);
}

/** Clique num atalho da doca: no menu do lugar, escolhe direto; numa tela aberta pela doca, volta e abre o outro. */
function acionarAtalho(rotulo, mid, i) {
  if (estado && estado.combate) { Som.tocar("falha"); avisarAtalho(rotulo); return; }
  if (!pergunta || processando) { recusarAtalho(rotulo); return; }
  if (pergunta.tipo === "continuar" && docaTela) {
    // telas de leitura (Bestiário...) terminam em "Continuar": ele faz as vezes do Voltar
    pendente = rotulo === docaTela ? null : { chave: "_atalho", valor: rotulo, saltos: 4 };
    responder(pergunta.id, null);
    return;
  }
  if (pergunta.tipo === "continuar") { recusarAtalho(rotulo); return; }
  if (pergunta.tipo !== "opcoes") return;
  if (pergunta.id === mid) {
    // O atalho (ou a tecla) da tela que está aberta fecha a tela pelo Voltar dela, como o jogo espera.
    const v = pergunta.opcoes.findIndex(ehVoltar);
    if (rotulo === docaTela && v >= 0) { pendente = null; responder(mid, v); return; }
    docaTela = rotulo; marcarDocaAtual(); responder(mid, i); return;
  }
  const aqui = atalhoNoMenu(pergunta.opcoes, rotulo);
  if (aqui >= 0) { docaTela = rotulo; marcarDocaAtual(); responder(pergunta.id, aqui); return; }
  if (menuDoLugar(pergunta.opcoes)) return;  // o lugar não tem esse atalho (ex.: Comitiva sem ninguém)
  if (!docaTela) {
    // Uma escolha da cena está esperando (um evento, o item encontrado): ela vem primeiro.
    recusarAtalho(rotulo);
    return;
  }
  const v = pergunta.opcoes.findIndex(ehVoltar);
  if (v < 0) return;
  // clicar no atalho da tela aberta fecha a tela (como o Voltar); noutro, volta e abre o outro
  pendente = rotulo === docaTela ? null : { chave: "_atalho", valor: rotulo, saltos: 4 };
  responder(pergunta.id, v);
}
function adormecerDoca() {
  if (docaTela) return;  // dentro de uma tela da doca, ela continua viva
  doca.dataset.viva = "0";
  clearTimeout(docaSono);
  // um instante de folga: entre um menu e o redesenho dele, a doca não pisca
  docaSono = setTimeout(() => { if (doca.dataset.viva === "0") doca.classList.add("inativa"); }, 350);
}

function limparPrompt() {
  // Numa tela desenhada (fogueira, mercado, mural), o lugar das opções segura a altura até as novas chegarem:
  // sem isso a página encolhia, a rolagem era puxada para cima e a pessoa perdia onde estava.
  if (emTela() && promptEl.offsetHeight) { promptEl.style.minHeight = promptEl.offsetHeight + "px"; promptEl.classList.add("segurando"); }
  promptEl.innerHTML = ""; pergunta = null; Batalha.limparAlvos(); Batalha.vez(null); limparRoda(); adormecerDoca();
  document.querySelectorAll(".rastro-contrato.cacavel").forEach((c) => { c.classList.remove("cacavel"); c.querySelector(".rastro-cacar")?.remove(); });
  Telas.fecharMenuItem();
}
/** O atalho da doca de uma opção, pela meta `sistema` (null quando a opção não é de sistema). */
/** O menu deixa conversar com o companheiro: direto ou pela tela da Comitiva. */
function podeConversar(opcoes, cid) {
  return opcoes.some((o) => o.meta && (o.meta.conversar === cid || (atalhoDe(o) && o.meta.sistema === "comitiva")));
}
function atalhoDe(o) { return (o && o.meta && o.meta.sistema && SISTEMA.find(([id]) => id === o.meta.sistema)) || null; }
/** As ações da sua vez na luta (atacar, habilidades, itens...): o motor marca cada uma com a meta `acao`. */
const ehAcaoDaLuta = (m) => m.opcoes.some((o) => o.meta && o.meta.acao);

/** As opções novas chegaram: o lugar delas não precisa mais segurar a altura (ver limparPrompt). */
function soltarAlturaPrompt() { setTimeout(() => { promptEl.style.minHeight = ""; promptEl.classList.remove("segurando"); }, 0); }
/** O prompt mora no pé da página. (Na luta, as ações vão para a roda em volta da sua carta, dentro da arena.) */
function posicionarPrompt() {
  if (promptEl.parentElement !== folha) folha.appendChild(promptEl);
  if (!corpo.classList.contains("em-combate")) limparRoda();
}

let viaBarra = false;  // a habilidade foi escolhida direto na barra: "Voltar" do alvo volta à barra, não à lista
let habMirando = "";   // o nome do que está sendo mirado, para o lembrete "Bola de Fogo: escolha o alvo"
function mostrarOpcoes(m) {
  posicionarPrompt();
  soltarAlturaPrompt();
  // Pedido pendente (ex.: clicou num destino do mapa a partir do menu do local): responde sozinho.
  if (pendente) {
    const p = pendente;
    pendente = null;
    if (p.chave === "_atalho") {
      // A caminho de outro atalho da doca: volta quantas telas for preciso até o menu do lugar e escolhe lá.
      const alvo = m.opcoes.findIndex((o) => { const at = atalhoDe(o); return at && at[1] === p.valor; });
      const v = m.opcoes.findIndex(ehVoltar);
      if (alvo >= 0) { docaTela = p.valor; pergunta = { id: m.id, tipo: "opcoes", opcoes: m.opcoes }; responder(m.id, alvo); marcarDocaAtual(); return; }
      if (v >= 0 && p.saltos > 0) { pendente = { ...p, saltos: p.saltos - 1 }; pergunta = { id: m.id, tipo: "opcoes", opcoes: m.opcoes }; responder(m.id, v); return; }
    } else {
      const i = p.chave === "_voltar" ? m.opcoes.findIndex(ehVoltar) : m.opcoes.findIndex((o) => o.meta && o.meta[p.chave] === p.valor);
      if (i >= 0) { pergunta = { id: m.id, tipo: "opcoes", opcoes: m.opcoes }; responder(m.id, i); return; }
    }
  }
  // O toque guardado do acampamento (acao, em nucleo.js): o menu voltou, e a ação vale se ainda estiver nele.
  if (acaoGuardada) {
    const a = acaoGuardada;
    acaoGuardada = null;
    const i = m.opcoes.findIndex((o) => o.meta && Object.entries(a.filtro).every(([k, v]) => o.meta[k] === v));
    if (i >= 0) {
      pergunta = { id: m.id, tipo: "opcoes", opcoes: m.opcoes };
      if (a.som) Som.tocar(a.som);
      responder(m.id, a.extra ? { i, ...a.extra } : i);
      return;
    }
  }
  // As cartas ✉ tocadas no meio de outra coisa (controles.js): cada uma vale num menu do lugar (o que tem os atalhos
  // da doca), na ordem dos cliques, uma conversa depois da outra. Os menus de uma conversa (as respostas) não contam.
  if (conversasGuardadas.length && m.opcoes.some(atalhoDe)) {
    const cid = conversasGuardadas.shift();
    if (podeConversar(m.opcoes, cid)) {
      pergunta = { id: m.id, tipo: "opcoes", opcoes: m.opcoes };
      pedir("Comitiva", "conversar", cid);
      return;
    }
    conversasGuardadas.length = 0;
    Telas.toast("", "Dá para conversar quando estiver num lugar seguro (vila ou acampamento).", cid, true);
  }
  // A próxima compra de suprimento da fila (mercado.js): o mercado voltou a perguntar e ela vai na hora.
  const compra = Telas.proximaCompra(m.opcoes);
  if (compra) {
    pergunta = { id: m.id, tipo: "opcoes", opcoes: m.opcoes };
    Som.tocar("moeda");
    responder(m.id, compra);
    return;
  }
  promptEl.innerHTML = "";
  pergunta = { id: m.id, tipo: "opcoes", n: m.opcoes.length, opcoes: m.opcoes, numeros: [], letras: {} };
  porVoltar(null);  // o da pergunta anterior (sai e volta no mesmo instante, se esta também tiver: a barra não pisca)
  if (m.opcoes.some((o) => o.meta && o.meta.talento) && Telas.abrirTalentos(m)) {
    // A árvore abre por cima, como o Grimório: nada muda na página do lugar. Esc ou o ✕ fecham (= Voltar).
    pergunta.voltar = m.opcoes.findIndex(ehVoltar);
    return;
  }
  Telas.fecharTalentos();
  // Perguntas que moram numa janela por cima: a confirmação (abandonar um contrato...) e o item achado.
  if (m.opcoes.length && m.opcoes.every((o) => o.meta && o.meta.confirmar)) { janelaConfirmar(m); return; }
  if (m.opcoes.some((o) => o.meta && o.meta.achado) && Telas.acoesDoAchado()) { botoesNaJanela(m, Telas.acoesDoAchado()); return; }
  Telas.fecharAchado();  // qualquer outra pergunta: a janela do item (se ficou aberta) sai
  const emLuta = !!(estado && estado.combate);
  if (emLuta && rodaEl() && Batalha.elCarta("j")) {
    // Na luta, as ações aparecem em volta da sua carta; habilidades e itens numa janelinha ao lado; mirando, um lembrete.
    if (ehAcaoDaLuta(m)) { rodaDeAcoes(m); return; }
    if (m.opcoes.some((o) => o.meta && (o.meta.habilidade || o.meta.usar_item || o.meta.trocar !== undefined))) { rodaSubmenu(m); return; }
    if (m.opcoes.some((o) => o.meta && o.meta.alvo)) { rodaMira(m); return; }
  }
  // Na vila, os serviços estão nos prédios da paisagem (vila.js): ficam fora da lista, e a pergunta também.
  const naVila = ehMenuDaVila(m), grupos = {};
  if (!naVila) fecharVila();
  if (m.pergunta && !naVila) promptEl.appendChild(el("div", "pergunta-rotulo", esc(m.pergunta)));
  const lista = el("ol", "escolhas");
  // as escolhas de um lugar selvagem (o motor marca a de explorar): as faixas de pincel (18-seletor-habilidades.css)
  if (!emLuta && m.opcoes.some((o) => o.meta && o.meta.explorar)) lista.classList.add("faixas");
  if (emLuta && ehAcaoDaLuta(m)) { lista.classList.add("acoes-combate"); Batalha.vez("j"); }
  if (emLuta && m.opcoes.some((o) => o.meta && o.meta.alvo)) {
    Batalha.alvos(m.opcoes, (i) => responder(m.id, i));
    promptEl.firstElementChild && promptEl.firstElementChild.classList.add("mira");
  }
  const sistema = m.opcoes.filter((o) => atalhoDe(o)).length >= 4;
  const atalhos = el("div", "atalhos");
  // "Voltar" é navegação nas telas de menu (mesmo sozinho: "Fechar o diário") e na luta; numa cena da história
  // ("Voltar por onde veio") é uma escolha como as outras.
  const v = corpo.classList.contains("modo-titulo") ? -1 : m.opcoes.findIndex(ehVoltar);
  const voltar = v >= 0 && (emLuta ? m.opcoes.length > 1 : emMenu()) ? v : -1;
  if (voltar >= 0 && emLuta) {
    pergunta.voltar = voltar;  // na luta, o Voltar fica dentro da barra (logo abaixo)
    if (viaBarra && m.opcoes.some((o) => o.meta && o.meta.alvo)) pergunta.aoVoltar = () => { pendente = { chave: "_voltar", valor: true }; };
  } else if (voltar >= 0) {
    // Na tela de menu, o Voltar vai para a barra do topo (e Esc/Backspace), em vez de ficar no fim da lista.
    porVoltar(/^Sair do mercado/.test(m.opcoes[voltar].texto) ? "Sair do mercado" : "Voltar", () => responder(m.id, voltar));
    pergunta.voltar = voltar;
  }
  let grupoAnterior = null;
  m.opcoes.forEach((o, i) => {
    if (i === voltar) return;
    if (o.meta && ACOES_OCULTAS.some((k) => o.meta[k] !== undefined)) return;  // feitas pela tela (arrastar, clicar)
    if (naVila && o.meta && o.meta.predio) { (grupos[o.meta.predio] = grupos[o.meta.predio] || []).push({ o, i }); return; }
    if (naVila && o.meta && o.meta.balcao) return;  // o Voltar do balcão aberto mora no próprio balcão (vila.js)
    const at = sistema && atalhoDe(o);
    if (at) {
      const pontos = o.meta.pontos, carta = o.meta.carta;
      const b = el("button", "atalho" + (pontos || carta ? " destaque" : ""));
      b.type = "button";
      const selo = pontos ? `<b class="selo">★${pontos}</b>` : carta ? '<b class="selo">✉</b>' : "";
      b.innerHTML = `<span class="atalho-icone">${Icones.atalho(at[1]) || spr(at[3], 2)}${selo}</span><span class="atalho-nome">${esc(at[1])}</span>` +
        (at[2] ? `<kbd>${at[2].toUpperCase()}</kbd>` : "");
      b.title = o.texto + (at[2] ? ` (${at[2].toUpperCase()})` : "");
      if (atalhos.lastElementChild && Number(atalhos.lastElementChild.dataset.grupo) !== at[4]) atalhos.appendChild(el("span", "doca-sep"));
      b.dataset.grupo = at[4];
      b.dataset.rotulo = at[1];
      if (at[1] === "Mapa") {
        // O mapa é consulta, não uma tela: abre por cima de qualquer coisa (e de lá também se viaja).
        b.dataset.sempre = "1";
        b.addEventListener("click", (ev) => { ev.stopPropagation(); alternarMapa(true); });
        atalhos.appendChild(b);
        return;
      }
      b.addEventListener("click", (ev) => { ev.stopPropagation(); acionarAtalho(at[1], m.id, i); });
      atalhos.appendChild(b);
      if (at[2]) pergunta.letras[at[2]] = i;
      if (at[1] === "Talentos") atalhos.appendChild(botaoGrimorio(at[4]));
      return;
    }
    pergunta.numeros.push(i);
    if (emLuta && o.meta && (o.meta.habilidade || o.meta.usar_item || o.meta.trocar !== undefined)) {
      lista.classList.add("grade-acoes");
      const li = el("li");
      li.appendChild(cartaAcao(o, i, m, pergunta.numeros.length - 1));
      lista.appendChild(li);
      return;
    }
    // As ações da missão e os contratos vêm em grupos com um rótulo (o motor já os manda nessa ordem); o de sempre vem
    // depois de um fio. Nada de etiqueta por linha: o grupo diz o que são.
    const grupo = o.meta && o.meta.missao ? "missao" : o.meta && o.meta.cacar !== undefined ? "contrato" : "geral";
    if (!emLuta && grupo !== grupoAnterior && (grupo !== "geral" || grupoAnterior)) {
      lista.appendChild(el("li", `op-grupo grupo-${grupo}`, { missao: "Missão", contrato: "Contratos", geral: "" }[grupo]));
    }
    grupoAnterior = grupo;
    const li = el("li");
    const b = el("button", "escolha");
    b.type = "button";
    b.style.animationDelay = `${replay ? 0 : i * 40}ms`;
    if (/^(Voltar|Sair|Cancelar|Nada|Ignorar|Fechar)/.test(o.texto)) b.classList.add("secundaria");
    const pos = pergunta.numeros.length - 1;
    const tecla = pos < 9 ? String(pos + 1) : pos === 9 ? "0" : "";
    let teste = "", icone = "";
    if (o.teste) {
      const folga = o.teste.mod - (estado ? estado.heroi.dificuldade_extra : 0);
      const nivel = folga >= 6 ? "bom" : folga >= 3 ? "medio" : "ruim";
      const sinal = o.teste.mod >= 0 ? "+" : "−";
      const info = estado && estado.heroi.testes && estado.heroi.testes[o.teste.atributo];
      const partes = info ? info.partes.map(([r, v]) => `<li>${esc(r)}: <b>${v >= 0 ? "+" : "−"}${Math.abs(v)}</b></li>`).join("") : "";
      const chance = Math.max(5, Math.min(95, (21 - (12 + (estado ? estado.heroi.dificuldade_extra : 0) - o.teste.mod)) * 5));
      const dicaTeste = Telas.dica(`<b>Teste de ${esc(o.teste.atributo)} ${sinal}${Math.abs(o.teste.mod)}</b>
        <div class="tipo">d20 + bônus contra a dificuldade</div><ul class="dica-lista">${partes || "<li>sem bônus</li>"}</ul>
        <div class="rodape">Tire 20 e passa sempre; 1 falha sempre. A dificuldade varia com a situação e sobe um pouco a cada dois níveis seus. Numa dificuldade média, sua chance é de cerca de ${chance}%.</div>`);
      teste = `<span class="teste ${nivel}" ${dicaTeste}>${SIGLA[o.teste.atributo] || esc(o.teste.atributo)} ${sinal}${Math.abs(o.teste.mod)}</span>`;
    }
    if (o.meta && o.meta.local !== undefined && estado) {
      const n = estado.mapa.nos.find((x) => x.id === o.meta.local);
      if (n) icone = spr(MapaPx.sprite(n), 1);
    }
    if (o.meta && o.meta.item) icone = spr(Telas.iconeConsumivel(o.meta.item), 1);
    if (o.meta && o.meta.gasta) icone = spr(Telas.iconeConsumivel(o.meta.gasta), 1);  // o item que a escolha usa
    // Indisponível: fica à vista, apagada, com o motivo escrito (não só a cor) e sem responder a clique ou tecla.
    const indisponivel = o.meta && o.meta.indisponivel;
    if (indisponivel) { b.classList.add("indisponivel"); b.disabled = true; b.setAttribute("aria-disabled", "true"); }
    // A missão e os contratos se distinguem pelo grupo, pela borda e pelo ícone; quem abre outra escolha (de onde se
    // volta) leva uma seta no fim.
    if (o.meta && o.meta.cacar !== undefined) { icone = spr("arco", 1); b.classList.add("op-contrato"); }
    if (o.meta && o.meta.missao) { icone = spr("pergaminho", 1); b.classList.add("op-missao"); }
    const abre = o.meta && o.meta.abre ? '<span class="op-abre" aria-hidden="true">›</span>' : "";
    if (emLuta) icone = iconeAcaoCombate(o.meta) || icone;
    if (o.meta && o.meta.alvo) {
      b.addEventListener("mouseenter", () => Batalha.mirar(o.meta.alvo, true));
      b.addEventListener("mouseleave", () => Batalha.mirar(o.meta.alvo, false));
      b.addEventListener("focus", () => Batalha.mirar(o.meta.alvo, true));
      b.addEventListener("blur", () => Batalha.mirar(o.meta.alvo, false));
    }
    b.innerHTML = `<span class="tecla">${tecla}</span>${icone}<span class="rotulo"><span class="op-texto">${esc(o.texto)}</span>${o.meta && o.meta.nota ? `<small class="op-nota">${esc(o.meta.nota)}</small>` : ""}${riscosDaOpcao(o.meta)}${indisponivel ? `<small class="op-nota op-motivo">${esc(indisponivel)}</small>` : ""}</span>${teste}${abre}`;
    b.addEventListener("click", (ev) => { ev.stopPropagation(); responder(m.id, i); });
    li.appendChild(b);
    lista.appendChild(li);
  });
  if (emLuta && voltar >= 0) {
    // Na luta, "Voltar" fica junto das opções, dentro da barra: sem subir o mouse até o topo.
    const li = el("li");
    const grade = lista.classList.contains("grade-acoes");
    const b = el("button", grade ? "escolha carta-acao voltar-carta" : "escolha secundaria voltar-luta",
      grade ? `<span class="acao-icone">◀</span><span class="acao-nome">Voltar</span><span class="acao-rodape"><kbd>Esc</kbd></span>`
        : `<span class="rotulo">◀ Voltar</span>`);
    b.type = "button";
    b.addEventListener("click", (ev) => { ev.stopPropagation(); voltarPergunta(); });
    li.appendChild(b);
    lista.appendChild(li);
  }
  if (emLuta && m.opcoes.some((o) => o.meta && o.meta.alvo)) {
    // Mirando: o clique é na carta do inimigo (ou as teclas 1, 2...). Na barra fica só o lembrete e o Voltar.
    lista.classList.add("mira-alvo");
    const rot = promptEl.querySelector(".pergunta-rotulo");
    if (rot) rot.innerHTML = `${habMirando ? `<b>${esc(habMirando)}</b>: ` : ""}escolha o alvo <small>clique num inimigo</small>`;
  }
  if (lista.childElementCount) { promptEl.appendChild(lista); Telas.ligarDicas(lista); }
  if (m.caixa) {  // uma caixa marcável que vai junto da escolha ("Mostrar tutorial", abertura.py)
    const c = el("label", "caixa-escolha", `<input type="checkbox"${m.caixa.marcada ? " checked" : ""}><span>${esc(m.caixa.rotulo)}</span>`);
    promptEl.appendChild(c);
    pergunta.caixa = c.querySelector("input");
  }
  if (corpo.classList.contains("modo-titulo")) { focoNoTitulo(lista); docaTela = null; }  // o título fecha a tela da doca
  if (naVila) montarVila(m, grupos);
  if (atalhos.childElementCount) montarDoca(atalhos, !!docaTela && m.opcoes.some(ehVoltar));
  if (!replay) guardar("cdf-dica", String(Number(ler("cdf-dica") || 0) + 1));
  if (estado) {
    const chave = [...destinosClicaveis()].join(",") + "|" + estado.local.id;
    if (chave !== ultimoMundo) { ultimoMundo = chave; desenharMundo(estado); }
    atualizarMapasDaPagina();
  }
  marcarCacadas();
  rolarFim();
}

/** No menu do título, o mouse e o teclado mostram a mesma opção: passar o mouse leva o foco junto (as setas andam
 *  a partir dali; Enter confirma), e a primeira já chega em foco. O indicador desenha só o foco (07-titulo). */
function focoNoTitulo(lista) {
  const botoes = [...lista.querySelectorAll(".escolha")];
  botoes.forEach((b) => b.addEventListener("mouseenter", () => b.focus({ preventScroll: true })));
  if (botoes.length && !lista.contains(document.activeElement)) botoes[0].focus({ preventScroll: true });
}

/** Contrato de caça com o alvo aqui: o cartão do rastreador vira atalho para "Caçar". */
function opcaoCacar(id) {
  if (!pergunta || pergunta.tipo !== "opcoes") return -1;
  return pergunta.opcoes.findIndex((o) => o.meta && o.meta.cacar === id);
}
/** O passo da missão que se dá aqui (examinar a fonte nova...): o cartão da missão no rastreador vira atalho para ele. */
function opcaoMissao(id) {
  if (!pergunta || pergunta.tipo !== "opcoes") return -1;
  return pergunta.opcoes.findIndex((o) => o.meta && o.meta.missao === id);
}
function marcarCacadas() {
  document.querySelectorAll(".rastro-contrato").forEach((c) => {
    const i = c.dataset.missao ? opcaoMissao(c.dataset.missao) : opcaoCacar(Number(c.dataset.contrato));
    const pode = i >= 0;
    c.classList.toggle("cacavel", pode);
    const selo = c.querySelector(".rastro-cacar");
    const texto = c.dataset.missao ? `${pode ? esc(pergunta.opcoes[i].texto) : ""} ▸` : "Seguir os rastros ▸";
    if (pode && !selo) c.querySelector(".rastro-info").insertAdjacentHTML("beforeend", `<span class="rastro-cacar">${texto}</span>`);
    else if (!pode && selo) selo.remove();
  });
}

/** O ícone do ataque básico da classe (classes.py: icone_ataque, no Grimório que o motor manda). */
function iconeAtaque() {
  const g = estado && estado.heroi && estado.heroi.grimorio;
  return (g && g.basico.icone) || "espada";
}

/* Cartas de ação do combate: habilidades e itens com ícone, custo e dica (como numa barra de ações). O ícone e a cor
   de cada habilidade vêm do catálogo do motor (habilidades.py: icone, familia). */
// Alcance como nos RPGs de turno (Final Fantasy, Pokémon): quem, e se é um só ou todos.
const ALVO_TXT = { inimigo: "Inimigo único", todos: "Todos os inimigos", proprio: "Você", aliado: "Aliado único", aliados: "Todos os aliados" };
function cartaAcao(o, i, m, pos) {
  const meta = o.meta;
  const b = el("button", "escolha carta-acao");
  b.type = "button";
  const tecla = pos < 9 ? String(pos + 1) : pos === 9 ? "0" : "";
  let icone, nome, rodape = "", dicaHtml, bloqueio = null;
  if (meta.habilidade) {
    b.classList.add("el-" + (meta.familia || "arcano"));
    icone = spr(meta.icone || "estrela", 2);
    nome = meta.nome;
    const custo = (meta.custo ? `${spr(RECURSO_ICONE[meta.recurso] || "estrela", 1)}<b>${meta.custo}</b>` : `<b class="gratis">grátis</b>`) +
      (meta.flechas ? ` ${spr("flecha", 1)}<b>${meta.flechas}</b>` : "");
    rodape = `<span class="acao-custo">${custo}</span><span class="acao-alvo">${ALVO_TXT[meta.alvo_tipo] || ""}</span>`;
    if (!meta.pode) bloqueio = meta.motivo || "Indisponível";
    dicaHtml = `<b>${esc(meta.nome)}</b><div class="tipo">${meta.custo ? `${meta.custo} de ${esc(meta.recurso)}` : "Sem custo"}${meta.flechas ? ` · ${Texto.plural(meta.flechas, "flecha")}` : ""} · Alvo: ${ALVO_TXT[meta.alvo_tipo] || "—"}</div>
      <div class="bonus">${Realce.texto(meta.desc)}</div>${danoGrimorio(meta.habilidade)}${bloqueio ? `<div class="pior">${esc(bloqueio)}</div>` : ""}`;
  } else if (meta.usar_item) {
    b.classList.add("el-cura");
    icone = Icones.consumivel(meta.usar_item) || spr(Telas.iconeConsumivel(meta.usar_item), 2);
    nome = meta.nome;
    rodape = `<span class="acao-custo"><b>×${meta.qtd}</b></span><span class="acao-alvo">gasta o turno</span>`;
    if (meta.motivo) bloqueio = meta.motivo;
    dicaHtml = `<b>${esc(meta.nome)}</b><div class="tipo">Você tem ${meta.qtd}</div><div class="bonus">${Realce.texto(meta.desc)}</div>${bloqueio ? `<div class="pior">${esc(bloqueio)}</div>` : ""}`;
  } else {
    const it = meta.equip;
    b.classList.add("el-fisico", "troca");
    icone = Icones.item(Telas.iconeItem(it)) || spr(Telas.iconeItem(it), 2);
    nome = "Trocar: " + it.nome;
    rodape = `<span class="acao-alvo">gasta o turno</span>`;
  }
  b.innerHTML = `<span class="tecla">${tecla}</span><span class="acao-icone">${icone}</span><span class="acao-nome">${esc(nome)}</span><span class="acao-rodape">${rodape}</span>`;
  b.dataset.dica = Telas.guardarDica(meta.trocar !== undefined
    ? Telas.htmlItem(meta.equip, "Trocar de arma no meio da luta gasta o seu turno.") : dicaHtml);
  if (bloqueio) b.classList.add("bloqueada");
  b.addEventListener("click", (ev) => {
    ev.stopPropagation();
    // Animação à parte (WAAPI): trocar a classe de animação apagava a de entrada e o botão sumia.
    if (bloqueio) { App.som("falha"); b.animate([{ translate: "0" }, { translate: "-4px 0" }, { translate: "4px 0" }, { translate: "0" }], { duration: 260, easing: "steps(6)" }); return; }
    responder(m.id, i);
  });
  return b;
}

/** Responde "Voltar" na pergunta atual (botão ou Esc), com o desvio da barra de luta. */
function voltarPergunta() {
  if (!pergunta || pergunta.voltar === undefined) return;
  if (pergunta.voltarLocal) { pergunta.voltarLocal(); return; }  // sair de um prédio da vila: sem perguntar ao jogo
  if (pergunta.aoVoltar) pergunta.aoVoltar();
  responder(pergunta.id, pergunta.voltar);
}

// O botão direito não volta mais de tela: ele faz atalhos onde há o que fazer (vender no mercado, equipar,
// usar um consumível em você). O Voltar fica no Esc, na seta do canto e no botão da própria tela.

/* ------------------------------------------------------------------ janelas por cima */
/** As opções de uma pergunta como botões dentro de uma janela (as teclas 1, 2... continuam valendo). */
function botoesNaJanela(m, caixa) {
  caixa.replaceChildren();
  m.opcoes.forEach((o, i) => {
    const pos = pergunta.numeros.push(i);
    const b = el("button", "botao-janela" + (o.meta.perigo ? " perigo" : "") + (o.meta.confirmar === "nao" ? " nao" : ""),
      `<kbd>${pos}</kbd>${esc(o.texto)}`);
    b.type = "button";
    b.addEventListener("click", (ev) => {
      ev.stopPropagation();
      if (o.meta.achado === "deixar") Telas.fecharAchado();  // deixar para trás: nada voa, a janela só fecha
      responder(m.id, i);
    });
    caixa.appendChild(b);
  });
}
/** Uma confirmação (abandonar um contrato, viajar para onde é perigoso): uma janela por cima de tudo, em vez de uma
 *  pergunta no pé da página, que ficava esquecida enquanto a pessoa clicava em outra coisa. Esc ou clicar fora: não. */
function janelaConfirmar(m) {
  fecharConfirmacao();
  const fundo = el("div", "sobreposicao", `<div class="caixa-confirmar"><div class="pergunta-confirmar">${esc(m.pergunta)}</div>
    <div class="botoes-confirmar"></div></div>`);
  fundo.id = "janela-confirmar";
  document.body.appendChild(fundo);
  botoesNaJanela(m, fundo.querySelector(".botoes-confirmar"));
  const nao = m.opcoes.findIndex((o) => o.meta.confirmar === "nao");
  pergunta.voltar = nao;
  fundo.addEventListener("click", (ev) => { if (ev.target === fundo) { ev.stopPropagation(); responder(m.id, nao); } });
  const b = fundo.querySelector(".botao-janela.nao");
  if (b) b.focus();
}
function fecharConfirmacao() { const j = document.getElementById("janela-confirmar"); if (j) j.remove(); }

/* ------------------------------------------------------------------ roda de ações da luta */
/* Na sua vez, sua carta vem para a frente e as ações (Atacar, Habilidades, Itens, Fugir) surgem em arco ao lado dela.
   Habilidades e Itens abrem uma janelinha com ícone, nome e custo (passe o mouse para ver o que fazem). */
function rodaEl() { return document.getElementById("roda"); }
let janelaAberta = null;  // { fechar } da janelinha de habilidades/itens
function limparRoda() {
  previaAlvos(null);
  if (janelaAberta && janelaAberta.soltar) janelaAberta.soltar();
  const r = rodaEl();
  if (r && r.childElementCount) { Telas.esconderDica(); r.replaceChildren(); }
  janelaAberta = null;
  Batalha.foco(null);
}
/** Fecha a janelinha (Esc, clique fora, ×). Devolve true se havia uma aberta. */
function fecharJanela() {
  if (!janelaAberta) return false;
  const j = janelaAberta;
  janelaAberta = null;
  j.fechar();
  return true;
}
function tremerNao(b, motivo) {
  App.som("falha");
  b.animate([{ translate: "0" }, { translate: "-4px 0" }, { translate: "4px 0" }, { translate: "0" }], { duration: 240, easing: "ease-in-out" });
  aviso(motivo, "info", "pergaminho");
}
/** Geometria da carta do herói dentro da arena (sem contar o zoom do foco). Com a arena se acomodando (uma carta
 *  entrou, batalha.js), vale o lugar final da carta e a altura final da arena: a roda não fica no meio do caminho. */
function geometriaHeroi() {
  const c = Batalha.elCarta("j"), arena = rodaEl().parentElement;
  return { x: c.offsetLeft - (c._acX || 0), y: c.offsetTop - (c._acY || 0), w: c.offsetWidth, h: c.offsetHeight,
    W: arena.clientWidth, H: arena._altura || arena.clientHeight };
}
function prepararRoda() {
  limparRoda();
  Batalha.vez("j");
  Batalha.foco("j");
  promptEl.appendChild(el("span", "marca-roda"));  // a próxima mensagem limpa o prompt, e com ele a roda
  pergunta.teclasNum = [];
  requestAnimationFrame(() => Batalha.abrirCaminho());  // a roda já montada: balão de fala que a cubra sai da frente
}

function rodaDeAcoes(m) {
  prepararRoda();
  viaBarra = false;
  habMirando = "";
  const roda = rodaEl();
  const acaoIdx = (a) => m.opcoes.findIndex((o) => o.meta && o.meta.acao === a);
  const heroi = estado.heroi;
  const atk = m.opcoes[acaoIdx("atacar")];
  const habs = m.opcoes[acaoIdx("habilidades")].meta.habilidades || [];
  const basico = heroi.grimorio && heroi.grimorio.basico.linhas.find((l) => l.tipo === "dano");
  const botoes = [];
  const botao = (id, icone, rotulo, dica, aoClicar) => {
    const b = el("button", "roda-botao");
    b.type = "button";
    b.dataset.slot = id;
    const n = pergunta.teclasNum.length + 1;
    b.innerHTML = `<span class="rb-icone">${icone}<span class="tecla">${n}</span></span><span class="rb-nome">${esc(rotulo)}</span>`;
    if (dica) b.dataset.dica = Telas.guardarDica(dica);
    b.addEventListener("click", (ev) => { ev.stopPropagation(); aoClicar(b); });
    pergunta.teclasNum.push(() => aoClicar(b));
    roda.appendChild(b);
    botoes.push(b);
    return b;
  };
  const arma = iconeAtaque();
  botao("atacar", Icones.acao(arma) || spr(arma, 2), "Atacar", `<b>${esc(atk.meta.nome)}</b><div class="tipo">grátis · devolve um pouco de ${esc(heroi.recurso.toLowerCase())}</div>` +
    (basico ? `<div class="melhor">Dano: ${basico.min}–${basico.max} (crítico ${basico.critico})</div>` : ""),
    () => { App.som("escolha"); habMirando = atk.meta.nome; responder(m.id, acaoIdx("atacar")); });
  if (habs.length) {
    const hb = botao("habilidades", Icones.acao("grimorio") || spr("grimorio", 2), "Habilidades", "", (b) => {
      if (janelaAberta && b.classList.contains("ativo")) { fecharJanela(); return; }
      App.som("pagina");
      abrirJanela(b, "Habilidades", habs.map((h) => linhaHabilidade(h, () => {
        App.som("escolha");
        viaBarra = true;
        habMirando = h.nome;
        pendente = { chave: "habilidade", valor: h.habilidade };
        responder(m.id, acaoIdx("habilidades"));
      })));
    });
    hb.dataset.alterna = "";  // abre e fecha a cada clique, mesmo seguidos (Gesto, em nucleo.js)
  }
  const itens = m.opcoes[acaoIdx("itens")].meta.itens || [];
  const ib = botao("itens", Icones.acao("pocao") || spr("pocao", 2), "Itens", "<b>Itens</b><div>Poções, tônicos, bandagens e troca de arma. Usar gasta o turno.</div>", (b) => {
    if (janelaAberta && b.classList.contains("ativo")) { fecharJanela(); return; }
    App.som("pagina");  // sem nada que sirva, o seletor abre com a frase que diz isso
    abrirJanela(b, "Itens", itens.map((meta) => linhaItem(meta, () => {
      App.som(meta.trocar !== undefined ? "equipar" : "item");
      habMirando = meta.nome || "";  // a poção pode pedir em quem: o lembrete diz o quê
      pendente = meta.trocar !== undefined ? { chave: "trocar", valor: meta.trocar } : { chave: "usar_item", valor: meta.usar_item };
      responder(m.id, acaoIdx("itens"));
    })));
  });
  ib.dataset.alterna = "";
  if (acaoIdx("analisar") >= 0) botao("analisar", spr("olho", 2), "Analisar", "", () => responder(m.id, acaoIdx("analisar")));
  if (acaoIdx("fugir") >= 0) {
    botao("fugir", Icones.acao("fuga") || spr("fuga", 2), "Fugir", "<b>Fugir</b><div>A chance depende da sua Agilidade contra a dos inimigos. Falhar custa o turno.</div>",
      () => { App.som("escolha"); responder(m.id, acaoIdx("fugir")); });
  }
  arcoDeBotoes(botoes);
  Telas.ligarDicas(roda);
}

/** Os botões em arco, colados à direita da carta (que cresceu 12% com o foco). */
function arcoDeBotoes(botoes) {
  const g = geometriaHeroi();
  const cx = g.x + g.w / 2, cy = g.y + g.h / 2;
  const direita = cx + (g.w / 2) * 1.12;
  const passo = 50, total = (botoes.length - 1) * passo;
  const topo = Math.max(28, Math.min(g.H - 28 - total, cy - total / 2));
  botoes.forEach((b, i) => {
    const y = topo + i * passo;
    const t = total ? (y - (topo + total / 2)) / (total / 2) : 0;
    const x = direita + 12 + 22 * (1 - t * t);  // um arco ")": os do meio mais afastados
    b.style.left = x + "px";
    b.style.top = y + "px";
    b.style.setProperty("--dx", (cx - x) + "px");
    b.style.setProperty("--dy", (cy - y) + "px");
    b.style.animationDelay = i * 35 + "ms";
  });
}

function linhaHabilidade(h, aoClicar) {
  const custo = h.custo ? `${spr(RECURSO_ICONE[h.recurso] || "estrela", 1)}${h.custo}` : '<span class="gratis">grátis</span>';
  return { icone: spr(h.icone || "estrela", 2), fam: h.familia || "arcano", nome: h.nome, alvo: h.alvo_tipo, info: custo + (h.flechas ? ` ${spr("flecha", 1)}${h.flechas}` : ""), dica: dicaHabilidade(h),
    bloqueio: h.pode ? null : (h.motivo || "Indisponível"), hab: h.habilidade, aoClicar };
}
function linhaItem(meta, aoClicar) {
  if (meta.trocar !== undefined) {
    return { icone: Icones.item(Telas.iconeItem(meta.equip)) || spr(Telas.iconeItem(meta.equip), 2), fam: "fisico", nome: "Trocar: " + meta.equip.nome, info: "turno", slot: "troca",
      dica: Telas.htmlItem(meta.equip, "Trocar de arma no meio da luta gasta o seu turno."), aoClicar };
  }
  return { icone: Icones.consumivel(meta.usar_item) || spr(Telas.iconeConsumivel(meta.usar_item), 2), fam: "cura", nome: meta.nome, info: `×${meta.qtd}`, slot: "item",
    dica: `<b>${esc(meta.nome)}</b><div class="tipo">Você tem ${meta.qtd} · gasta o turno</div><div class="bonus">${Realce.texto(meta.desc)}</div>${meta.motivo ? `<div class="pior">${esc(meta.motivo)}</div>` : ""}`,
    bloqueio: meta.motivo, aoClicar };  // apagado, a dica já diz por quê (como nas habilidades)
}
function dicaHabilidade(h) {
  return `<b>${esc(h.nome)}</b><div class="tipo">${h.custo ? `${h.custo} de ${esc(h.recurso)}` : "Sem custo"}${h.flechas ? ` · ${Texto.plural(h.flechas, "flecha")}` : ""} · Alvo: ${ALVO_TXT[h.alvo_tipo] || "—"}</div>
    <div class="bonus">${Realce.texto(h.desc)}</div>${danoGrimorio(h.habilidade)}${h.pode ? "" : `<div class="pior">${esc(h.motivo || "Indisponível")}</div>`}`;
}

/** Prévia de quem a habilidade atinge: um inimigo (todos acendem de leve, você escolhe depois), todos, ou você. */
function previaAlvos(tipo) {
  document.querySelectorAll("#batalha .carta.previa").forEach((c) => c.classList.remove("previa", "previa-area"));
  if (!tipo) return;
  const cartas = tipo === "proprio" ? document.querySelectorAll('#batalha .carta[data-uid="j"]')
    : document.querySelectorAll("#batalha .carta.inimigo:not(.morta)");
  cartas.forEach((c) => c.classList.add("previa", ...(tipo === "todos" ? ["previa-area"] : [])));
}

/** O seletor das ações (Habilidades e Itens): uma faixa por habilidade ou item (tecla, ícone, nome, custo ou
 *  quantidade). Teclas 1–9 escolhem. O componente está em css/18-seletor-habilidades.css: da largura da arena, logo
 *  embaixo dela, por cima do registro, em duas colunas na ordem das teclas, sem título de janela nem ×. data-tipo diz
 *  qual dos dois menus é (o de Itens tem a quantidade no lugar do custo e a frase quando nada serve). */
function abrirJanela(ancora, titulo, linhas, aoFechar) {
  fecharJanela();
  const roda = rodaEl();
  const teclasAntes = pergunta.teclasNum;
  pergunta.teclasNum = [];
  const j = el("div", "roda-janela seletor");
  j.dataset.tipo = titulo === "Itens" ? "itens" : "habilidades";
  j.innerHTML = `<div class="rj-titulo"><span>${esc(titulo)}</span></div>`;
  const lista = el("ul", "rj-lista");
  linhas.forEach((l, i) => {
    const li = el("li");
    const b = el("button", `rj-linha el-${l.fam || "fisico"}${l.bloqueio ? " bloqueada" : ""}`);
    b.type = "button";
    if (l.hab) b.dataset.hab = l.hab;
    if (l.slot) b.dataset.slot = l.slot;
    b.innerHTML = `<span class="tecla">${i < 9 ? i + 1 : ""}</span><span class="rj-icone">${l.icone}</span><span class="rj-texto"><span class="rj-nome">${esc(l.nome)}</span>${l.bloqueio ? `<span class="rj-motivo">${esc(l.bloqueio)}</span>` : ""}</span><span class="rj-info">${l.info || ""}</span>`;
    // as pontas da faixa vêm da posição (três pares que se repetem, nunca ao acaso); --i é a ordem de entrada
    li.dataset.forma = i % 3;
    li.style.setProperty("--i", i);
    // a descrição (l.dica) mora dentro do seletor, embaixo da coluna (descricoes): as faixas não têm dica ao lado
    const usar = () => (l.bloqueio ? tremerNao(b, l.bloqueio) : l.aoClicar());
    b.addEventListener("click", (ev) => { ev.stopPropagation(); previaAlvos(null); usar(); });
    if (l.alvo) {  // passar o mouse mostra quem a habilidade atingiria
      b.addEventListener("mouseenter", () => previaAlvos(l.alvo));
      b.addEventListener("mouseleave", () => previaAlvos(null));
    }
    pergunta.teclasNum.push(usar);
    li.appendChild(b);
    lista.appendChild(li);
  });
  j.appendChild(lista);
  if (!linhas.length) lista.insertAdjacentHTML("afterend", '<p class="rj-vazio">Nada na bolsa serve agora.</p>');  // só Itens chega vazio
  // duas colunas na ordem das teclas (1, 2, 3 descendo; depois a segunda coluna)
  const filas = Math.ceil(linhas.length / 2);
  lista.style.setProperty("--filas", filas);
  [...lista.children].forEach((li, k) => li.style.setProperty("--fila", k % filas));
  const v = el("button", "rj-fechar rj-voltar", "<kbd>Esc</kbd><span>Voltar</span>");
  v.type = "button";
  v.title = "Fechar (Esc)";
  j.appendChild(v);
  roda.appendChild(j);
  ancora.classList.add("ativo");
  // Desce do botão para baixo da arena, por cima do texto: os alvos ficam à vista enquanto você escolhe.
  const g = geometriaHeroi();
  const topoTela = j.offsetParent.getBoundingClientRect().top;
  // da largura da arena, colado embaixo dela (nada se mexe); a lista rola dentro se não couber
  j.style.left = "0px";
  j.style.width = g.W + "px";
  j.style.top = g.H + "px";
  j.style.maxHeight = Math.max(170, innerHeight - topoTela - g.H - 14) + "px";
  // onde caem as texturas da página (a leitura da cena e o carvão do palco): o fundo do seletor continua a página
  const pj = j.getBoundingClientRect(), cena = document.getElementById("cena"), palco = document.getElementById("palco");
  if (cena && palco) {
    const c = cena.getBoundingClientRect(), pa = palco.getBoundingClientRect();
    j.style.setProperty("--fundo-cena", `${c.left + 64 - pj.left}px ${c.top + 32 - pj.top}px`);
    j.style.setProperty("--fundo-palco", `${pa.left + 12 - pj.left}px ${pa.top + 12 - pj.top}px`);
  }
  const fechar = () => {
    Telas.esconderDica();
    previaAlvos(null);
    const devolver = j.contains(document.activeElement);  // fechou pelo teclado: o foco volta ao botão
    j.remove();
    ancora.classList.remove("ativo");
    if (devolver && ancora.isConnected && ancora.focus) ancora.focus({ preventScroll: true });
    if (pergunta) pergunta.teclasNum = teclasAntes;
    if (aoFechar) aoFechar();
  };
  j.querySelector(".rj-fechar").addEventListener("click", (ev) => { ev.stopPropagation(); fecharJanela(); });
  // Clique fora da janelinha (e fora dos botões de ação, que têm o próprio comportamento) também fecha.
  const fora = (ev) => { if (!ev.target.closest(".roda-janela, .roda-botao, #dica-item")) { ev.stopPropagation(); ev.preventDefault(); fecharJanela(); } };
  setTimeout(() => { if (janelaAberta && janelaAberta.fechar === fecharTudoJanela) document.addEventListener("pointerdown", fora, true); }, 0);
  const fecharTudoJanela = () => { document.removeEventListener("pointerdown", fora, true); fechar(); };
  janelaAberta = { fechar: fecharTudoJanela, soltar: () => document.removeEventListener("pointerdown", fora, true) };
  Telas.ligarDicas(j);
  descricoes(j, linhas, lista);
  faixasTeclado(j, linhas);
  bordaLimpa(j);
}
/** A descrição da habilidade examinada (mouse ou teclado), dentro do seletor, embaixo da coluna dela: o que a dica
 *  de antes mostrava (custo, alvo, o que faz, o dano, o motivo de não poder). Uma por vez; ela fica na última
 *  examinada até outra ser examinada. O lugar é reservado ao abrir, na altura da maior descrição daquela luta: trocar de
 *  habilidade não mexe em nada. Se a descrição por coluna não couber na janela, vira uma área só, embaixo das duas
 *  colunas (mais larga, logo mais baixa); se nem assim couber, a lista rola dentro e a descrição fica inteira. */
function descricoes(j, linhas, lista) {
  const lis = [...lista.children], n = lis.length, filas = Math.ceil(n / 2);
  if (!n) return;
  const zona = el("div", "rj-descricao"), caixa = el("div", "rj-desc-caixa");
  zona.appendChild(caixa);
  j.insertBefore(zona, j.querySelector(".rj-voltar"));
  const Z = zona.getBoundingClientRect();
  const coluna = (li) => { const r = li.getBoundingClientRect(); return { esq: r.left - Z.left + 12, larg: r.width - 12 }; };  // a faixa começa 12 px depois da tecla
  const esq = coluna(lis[0]), dir = n > 1 ? coluna(lis[filas] || lis[n - 1]) : esq;
  const junto = { esq: esq.esq, larg: dir.esq + dir.larg - esq.esq };
  // a área de baixo das duas colunas tem outro arranjo: o nome, o custo e o rodapé à esquerda, o texto à direita
  const arranjar = (dica, lado) => {
    if (lado !== "junto") return dica || "";
    const t = document.createElement("div");
    t.innerHTML = dica || "";
    const a = el("div", "rj-desc-a"), d = el("div", "rj-desc-b");
    [...t.children].forEach((c) => (c.matches("b, .tipo, .rodape") ? a : d).appendChild(c));
    return a.outerHTML + d.outerHTML;
  };
  const medir = (larg, lado) => {
    caixa.style.width = larg + "px";
    caixa.dataset.lado = lado;
    let h = 0;
    linhas.forEach((l) => { caixa.innerHTML = arranjar(l.dica, lado); h = Math.max(h, caixa.offsetHeight); });
    caixa.innerHTML = "";
    return h;
  };
  let livre = parseFloat(j.style.maxHeight) - j.offsetHeight;
  let modo = "coluna", alt = medir(esq.larg, "esquerda");
  if (alt > livre) {
    modo = "junto";
    alt = medir(junto.larg, "junto");
    // janela baixa: o "Esc · Voltar" sobe para a linha do título, e a descrição ganha a altura dele
    const v = j.querySelector(".rj-voltar");
    if (v) { j.querySelector(".rj-titulo").appendChild(v); livre = parseFloat(j.style.maxHeight) - j.offsetHeight; }
  }
  // se nem assim couber, as faixas ficam inteiras (as opções antes de tudo) e a descrição rola dentro da área dela
  if (alt > livre) { alt = Math.max(60, livre); caixa.classList.add("rola"); }
  zona.style.height = alt + "px";
  caixa.style.maxHeight = alt + "px";
  j.dataset.descricao = modo;
  // com um número ímpar, a coluna da direita acaba uma faixa antes: a descrição dela começa logo embaixo dessa faixa
  const subir = modo === "coluna" && n % 2 && n > 1 ? lis[n - 1].getBoundingClientRect().bottom - zona.getBoundingClientRect().top : 0;
  const mostrar = (k) => {
    const l = linhas[k];
    if (!l || !l.dica) return;
    const lado = modo === "junto" ? junto : k < filas ? esq : dir;
    caixa.style.left = lado.esq + "px";
    caixa.style.width = lado.larg + "px";
    caixa.style.top = (modo === "coluna" && k >= filas ? Math.min(0, subir) : 0) + "px";
    caixa.dataset.lado = modo === "junto" ? "junto" : k < filas ? "esquerda" : "direita";
    caixa.innerHTML = arranjar(l.dica, caixa.dataset.lado);
  };
  lis.forEach((li, k) => {
    const b = li.querySelector(".rj-linha");
    b.addEventListener("mouseenter", () => mostrar(k));
    b.addEventListener("focus", () => mostrar(k));
  });
}
/** O registro continua por baixo do seletor. A linha que a borda de baixo cortaria ao meio fica inteira coberta (o
 *  seletor desce até o fim dela, com o mesmo fundo), para não sobrar meio texto encostado na divisória. Só o seletor
 *  cresce: o registro, a rolagem e as cartas não se mexem; se o registro rolar com ele aberto, a conta é refeita. */
function bordaLimpa(j) {
  const pagina = document.getElementById("pagina");
  if (!pagina) return;
  const pad = parseFloat(getComputedStyle(j).paddingBottom), teto = parseFloat(j.style.maxHeight);
  const acertar = () => {
    if (!j.isConnected) { pagina.removeEventListener("scroll", acertar); return; }
    j.style.paddingBottom = "";
    j.style.maxHeight = teto + "px";
    const borda = j.getBoundingClientRect().bottom;
    // as caixas de cada linha (um parágrafo quebrado tem várias) e as imagens do registro
    const caixas = [], trecho = document.createRange(), passeio = document.createTreeWalker(pagina, NodeFilter.SHOW_TEXT);
    for (let t = passeio.nextNode(); t; t = passeio.nextNode()) {
      if (!t.textContent.trim()) continue;
      trecho.selectNodeContents(t);
      caixas.push(...trecho.getClientRects());
    }
    pagina.querySelectorAll("img").forEach((im) => caixas.push(im.getBoundingClientRect()));
    // a borda desce até o pé da linha cortada; se ali começar a cortar a seguinte (as caixas das letras se encostam),
    // desce de novo. A folga de 3 px separa o corte de verdade do encosto das caixas de linhas vizinhas
    let ate = borda;
    for (let volta = 0; volta < 6; volta++) {
      const cortadas = caixas.filter((q) => q.height && q.top < ate - 3 && q.bottom > ate + 3);
      if (!cortadas.length) break;
      ate = Math.max(...cortadas.map((q) => q.bottom));
    }
    const mais = Math.min(ate, innerHeight - 4) - borda;
    if (mais > 0) {
      j.style.paddingBottom = pad + mais + "px";
      j.style.maxHeight = teto + mais + "px";
    }
  };
  acertar();
  pagina.addEventListener("scroll", acertar, { passive: true });
}
/** As faixas pelo teclado e a prévia dos alvos no foco. */
function faixasTeclado(j, linhas) {
  const bs = [...j.querySelectorAll(".rj-linha")], n = bs.length, filas = Math.ceil(n / 2);
  bs.forEach((b, k) => {
    const alvo = linhas[k].alvo;
    if (alvo) {
      b.addEventListener("focus", () => previaAlvos(alvo));
      b.addEventListener("blur", () => previaAlvos(null));
    }
  });
  j.addEventListener("keydown", (ev) => {  // cima e baixo na ordem; os lados trocam de coluna
    const passo = { ArrowDown: 1, ArrowUp: -1, ArrowRight: filas, ArrowLeft: -filas }[ev.key];
    if (!passo) return;
    ev.preventDefault();
    ev.stopPropagation();
    const k = bs.indexOf(document.activeElement), novo = k < 0 ? 0 : k + passo;
    if (novo < 0 || novo >= n) return;
    bs[novo].focus({ preventScroll: true });
    const L = bs[novo].closest(".rj-lista"), r = bs[novo].getBoundingClientRect(), lr = L.getBoundingClientRect();
    if (r.top < lr.top) L.scrollTop -= lr.top - r.top;  // a lista que rola dentro acompanha o foco (só ela: a página fica)
    else if (r.bottom > lr.bottom) L.scrollTop += r.bottom - lr.bottom;
  });
  if (performance.now() - gestoTecla < 400 && bs[0]) bs[0].focus({ preventScroll: true });  // aberta pela tecla
}
let gestoTecla = 0;  // quando foi a última tecla (o clique zera): o seletor aberto pela tecla já chega com o foco
document.addEventListener("keydown", () => { gestoTecla = performance.now(); }, true);
document.addEventListener("pointerdown", () => { gestoTecla = 0; }, true);

/** Itens (ou habilidades pela tecla): a mesma janelinha, aberta pelo motor; fechar é "Voltar". */
function rodaSubmenu(m) {
  prepararRoda();
  const voltar = m.opcoes.findIndex(ehVoltar);
  if (voltar >= 0) pergunta.voltar = voltar;
  const linhas = [];
  m.opcoes.forEach((o, i) => {
    const meta = o.meta;
    if (!meta || i === voltar) return;
    if (meta.habilidade) linhas.push(linhaHabilidade(meta, () => { App.som("escolha"); habMirando = meta.nome; responder(m.id, i); }));
    else if (meta.usar_item || meta.trocar !== undefined) linhas.push(linhaItem(meta, () => { App.som("item"); responder(m.id, i); }));
  });
  // Uma âncora invisível onde ficaria o botão de Itens, para a janelinha abrir no mesmo lugar.
  const g = geometriaHeroi();
  const ancora = el("span", "roda-ancora");
  ancora.style.left = g.x + g.w * 1.06 + 20 + "px";
  ancora.style.top = g.y + g.h / 2 + "px";
  rodaEl().appendChild(ancora);
  abrirJanela(ancora, m.pergunta && /item/i.test(m.pergunta) ? "Itens" : "Habilidades", linhas, () => { if (voltar >= 0) voltarPergunta(); });
}

/** Mirando: os inimigos acendem; o lembrete e o Voltar ficam na faixa dos comandos, ao lado da sua carta, onde a roda
 *  estava (nenhuma carta entra nela: batalha.js, distribuir). As teclas 1, 2... escolhem o alvo. */
function rodaMira(m) {
  prepararRoda();
  Batalha.alvos(m.opcoes, (i) => responder(m.id, i));
  m.opcoes.forEach((o, i) => { if (o.meta && o.meta.alvo) pergunta.teclasNum.push(() => responder(m.id, i)); });
  const voltar = m.opcoes.findIndex(ehVoltar);
  const chip = el("div", "roda-mira", `<span>${habMirando ? `<b>${esc(habMirando)}</b> ` : ""}escolha o alvo</span>`);
  if (voltar >= 0) {
    pergunta.voltar = voltar;
    if (viaBarra) pergunta.aoVoltar = () => { pendente = { chave: "_voltar", valor: true }; };
    const v = el("button", "mira-voltar", "◀ Voltar");
    v.type = "button";
    v.addEventListener("click", (ev) => { ev.stopPropagation(); voltarPergunta(); });
    chip.appendChild(v);
  }
  rodaEl().appendChild(chip);
  // no meio da faixa dos comandos, na altura da sua carta (sem passar do alto nem do pé da arena)
  const g = geometriaHeroi(), meia = chip.offsetHeight / 2;
  chip.style.left = Math.round(g.x + g.w * 1.06 + 12) + "px";
  chip.style.top = Math.round(Math.max(6 + meia, Math.min(g.H - 6 - meia, g.y + g.h / 2))) + "px";
}

/** Os riscos de uma ação (a luz e a noite numa sala da capela): indicadores curtos com o ícone, a cor do tipo (custo,
 *  perigo, noite) e a dica com o detalhe. Vêm prontos do motor (sobrevivencia.riscos_sala). */
function riscosDaOpcao(meta) {
  if (!meta || !meta.riscos || !meta.riscos.length) return "";
  return `<span class="op-riscos">${meta.riscos.map((r) => `<span class="op-risco ${esc(r.tipo)}" ${Telas.dica(esc(r.dica), true)}>${spr(r.icone, 1)}${esc(r.texto)}</span>`).join("")}</span>`;
}

const ICONE_ACAO = { habilidades: "grimorio", itens: "pocao", analisar: "olho", fugir: "fuga" };
function iconeAcaoCombate(meta) {
  const acao = meta && meta.acao;
  if (acao === "atacar") return spr(iconeAtaque(), 2);
  return ICONE_ACAO[acao] ? spr(ICONE_ACAO[acao], 2) : "";
}

/** A linha de dano do Grimório na dica da carta de habilidade: "Dano 16–22 (crítico 31)". */
function danoGrimorio(id) {
  const g = estado && estado.heroi.grimorio;
  const x = g && g.habilidades.find((h) => h.id === id);
  const d = x && x.linhas.find((l) => l.tipo === "dano");
  return d ? `<div class="melhor">${esc(d.rotulo === "Dano" ? "Dano" : d.rotulo)}: ${d.min}–${d.max} (crítico ${d.critico})</div><div class="rodape">Detalhes no Grimório (P).</div>` : "";
}

/** O Grimório não é um menu do jogo: abre por cima de qualquer tela, como o mapa. */
function botaoGrimorio(grupo) {
  const b = el("button", "atalho");
  b.type = "button";
  b.dataset.grupo = grupo;
  b.title = "Grimório: suas habilidades e o dano de cada uma (P)";
  b.dataset.sempre = "1";  // funciona com a doca apagada
  b.innerHTML = `<span class="atalho-icone">${Icones.atalho("Grimório") || spr("grimorio", 2)}</span><span class="atalho-nome">Grimório</span><kbd>P</kbd>`;
  b.addEventListener("click", (ev) => { ev.stopPropagation(); Telas.abrirGrimorio(); });
  return b;
}

function ehVoltar(o) {
  // Uma passagem da capela ("Voltar ao salão alagado") anda pelo lugar: não é o Voltar de uma tela.
  if (o.meta && o.meta.capela_ir) return false;
  return (o.meta && o.meta.voltar) || /^(Voltar|Sair do mercado|Cancelar|Fechar)\b/.test(o.texto);
}

function mostrarContinuar(m) {
  acaoGuardada = null;  // um toque guardado do acampamento não atravessa um Continuar
  Telas.descartarCompras();  // nem as compras do mercado que ainda esperavam a vez
  posicionarPrompt();
  soltarAlturaPrompt();
  if (pendente && pendente.chave === "_atalho" && docaTela) {  // a caminho de um atalho
    pergunta = { id: m.id, tipo: "continuar" };
    responder(m.id, null);
    return;
  }
  promptEl.innerHTML = "";
  porVoltar(null);
  const b = el("button", "continuar", "Continuar <span>▸</span>");
  b.type = "button";
  pergunta = { id: m.id, tipo: "continuar", confirmar: !!m.confirmar };
  if (m.confirmar) {
    // Cena que pede confirmação (as de missão): adiantar o texto e continuar são gestos distintos. O gesto que adiantou
    // termina aqui, com o botão à vista; o próximo clique (ou Enter/espaço) explícito continua na hora. Quem separa os
    // gestos é o Gesto (nucleo.js): o toque que começou antes do botão, o segundo clique do clique duplo e a tecla
    // segurada não contam. Sem guarda de tempo: tentar de novo não prolonga nada.
    b.classList.add("confirmar");
  }
  const p = pergunta;
  b.addEventListener("click", (ev) => { ev.stopPropagation(); responder(p.id, null); });
  promptEl.appendChild(b);
  rolarFim();
}

function mostrarPergunta(m) {
  acaoGuardada = null;
  Telas.descartarCompras();
  posicionarPrompt();
  soltarAlturaPrompt();
  promptEl.innerHTML = "";
  promptEl.appendChild(el("div", "pergunta-rotulo", esc(m.pergunta)));
  const linha = el("div", "entrada-texto");
  const input = el("input");
  input.placeholder = m.padrao || "";
  input.maxLength = 40;
  input.addEventListener("keydown", (ev) => { if (ev.key === "Enter") { ev.preventDefault(); responder(m.id, input.value || m.padrao || ""); } });
  const ok = el("button", "continuar", "Confirmar <span>▸</span>");
  ok.addEventListener("click", (ev) => { ev.stopPropagation(); responder(m.id, input.value || m.padrao || ""); });
  linha.append(input, ok);
  porVoltar("Voltar", m.voltar ? () => responder(m.id, { voltar: true }) : null);
  if (m.voltar) input.addEventListener("keydown", (ev) => { if (ev.key === "Escape") { ev.preventDefault(); responder(m.id, { voltar: true }); } });
  promptEl.appendChild(linha);
  pergunta = { id: m.id, tipo: "pergunta" };
  setTimeout(() => input.focus(), 50);
  rolarFim();
}

/* ------------------------------------------------------------------ viagem pelo mapa */
function destinosClicaveis() {
  if (!pergunta || pergunta.tipo !== "opcoes" || !estado) return new Set();
  const diretos = pergunta.opcoes.filter((o) => o.meta && o.meta.local !== undefined).map((o) => o.meta.local);
  if (diretos.length) return new Set(diretos);
  if (pergunta.opcoes.some((o) => o.texto === "Viajar")) return new Set(estado.mapa.nos.filter((n) => n.distancia).map((n) => n.id));
  return new Set();
}
function viajarPara(id) { pedir("Viajar", "local", id); }

function mapaNaPagina() {
  if (!estado) return;
  const caixa = el("div", "mapa-pagina");
  caixa.dataset.mapa = "1";
  anexar(caixa);
  atualizarMapasDaPagina();
}
function atualizarMapasDaPagina() {
  if (!estado) return;
  textoEl.querySelectorAll("[data-mapa]").forEach((caixa) => {
    const clic = destinosClicaveis();
    caixa.innerHTML = "";
    caixa.appendChild(MapaPx.criar(estado.mapa, { grande: true, clicaveis: clic, aoClicar: viajarPara, nivelHeroi: estado.heroi.nivel, marcas: marcasContrato(estado) }));
    if (clic.size) caixa.appendChild(el("div", "mapa-dica", "Clique num destino no mapa para viajar"));
  });
}
