/* Inventário: a janela do grupo (o herói e a comitiva, um de cada vez pela aba com o retrato), o boneco com o
   equipamento do selecionado, a bolsa do grupo, os atributos com a dica de cada um e a reputação.

   A bolsa é a do grupo (a mochila, os mesmos espaços); o corpo e a ficha são os do selecionado. Um clique escolhe a
   peça e mostra a ficha comparada com o selecionado e as ações; dois cliques equipam nele; o botão direito abre o menu
   com as mesmas ações; arrastar leva da bolsa ao corpo, do corpo à bolsa e de um lugar a outro da bolsa. Toda ação vai
   ao motor pela mesma opção ({equipamento}, com o pedido junto), que confere tudo (comitiva/ficha.py): aqui só se
   desenha e se pede. */
"use strict";

(() => {
  const { h, S, AREA, dica, dicaItem, esconderDica, ESPACOS, fecharAoClicarFora, fecharMenuItem, iconeConsumivel,
          iconeItem, menuUso, NOME_ESPACO, VAZIO } = Telas;

  let selId = "heroi";   // a aba
  let marcado = null;    // a peça escolhida com um clique: {de: "mochila", i} ou {de: "espaco", s}
  let enviando = false;  // um pedido por vez: o segundo clique de um duplo clique não equipa de novo
  let focoDepois = null; // o seletor que recebe o foco quando a janela volta desenhada

  const fichas = () => {
    const e = App.estado;
    return e && e.heroi ? [{ ...e.heroi, id: "heroi" }, ...(e.heroi.grupo || [])] : [];
  };
  const atual = () => { const fs = fichas(); return fs.find((f) => f.id === selId) || fs[0]; };
  const serve = (p, it) => !it.classe || it.classe === p.classe;
  const quemTexto = (p) => (p.id === "heroi" ? "você" : p.nome);
  // a cabeça só nos tamanhos dela (32 e 48: escala inteira); no boneco, o busto, como o do herói (64 dava o xadrez)
  const retratoDe = (p, lado = 32) => Icones.cabeca(p.id === "heroi" ? p.classe : p.id, lado) || S(p.id === "heroi" ? p.classe : p.id, 2);
  const limiteBolsa = () => (App.estado.heroi.limite_mochila || 12);

  function personagem(d) {
    const e = App.estado;
    if (!e) return "";
    enviando = false;
    const fs = fichas();
    if (!fs.some((f) => f.id === selId)) { selId = "heroi"; marcado = null; }
    const p = atual(), heroi = e.heroi;
    const limite = (d && d.limite) || limiteBolsa();
    if (marcado && marcado.de === "mochila" && !heroi.mochila[marcado.i]) marcado = null;
    const grupo = fs.length > 1;
    const abas = grupo ? `<div class="grupo-abas" role="tablist" aria-label="Personagem">${fs.map((f) => {
      const tag = f.indisponivel ? "longe" : f.ferido ? "ferido" : "";
      const pontos = f.id !== "heroi" && f.pontos_atributo ? `<b class="aba-pontos" title="Pontos de atributo para distribuir">+${f.pontos_atributo}</b>` : "";
      return `<button type="button" role="tab" class="grupo-aba${f.id === selId ? " ativa" : ""}${f.indisponivel ? " indisponivel" : ""}" data-aba="${h(f.id)}"
        aria-selected="${f.id === selId}" tabindex="${f.id === selId ? 0 : -1}"${f.indisponivel ? ` title="${h(f.indisponivel)}"` : ""}>
        <span class="aba-retrato">${retratoDe(f)}</span><span class="aba-nome">${h(f.nome)}</span>${tag ? `<small class="aba-tag">${tag}</small>` : ""}${pontos}</button>`;
    }).join("")}</div>` : "";
    const espacos = Object.keys(AREA).map((s) => {
      const it = p.equip[s];
      // o equipamento em 40 px (o desenho que tem arquivo de 40; os outros em 32, centrados); a silhueta vazia em 32
      const conteudo = it ? Icones.equipamento(iconeItem(it)) || S(iconeItem(it), 2) : Icones.vazio(s) || S(VAZIO[s], 2, "fantasma");
      const nome = Telas.nomeEspaco(s, p.classe);
      const extra = it ? `draggable="true" ${dicaItem(it, "", false, p)}`
        : `title="${h(nome)} (vazio): clique para ver as peças que servem"`;
      const sel = marcado && marcado.de === "espaco" && marcado.s === s ? " marcado" : "";
      return `<div class="espaco slot-px ${it ? "r-" + h(it.raridade) : "vazio"}${sel}" data-espaco="${s}" style="grid-area:${AREA[s]}" tabindex="0" role="button" aria-label="${h(nome)}: ${it ? h(it.nome) : "vazio"}" ${extra}>${conteudo}<span class="espaco-nome">${h(nome)}</span></div>`;
    }).join("");
    const celulas = [];
    for (let i = 0; i < limite; i++) {
      const it = heroi.mochila[i];
      const sel = marcado && marcado.de === "mochila" && marcado.i === i ? " marcado" : "";
      celulas.push(it
        ? `<div class="slot-px celula r-${h(it.raridade)}${serve(p, it) ? "" : " inutil"}${sel}" draggable="true" data-mochila="${i}" tabindex="0" role="button" aria-label="${h(it.nome)}" ${dicaItem(it, `Clique para ver as ações. Dois cliques equipam em ${h(quemTexto(p))}.`, true, p)}>${Icones.equipamento(iconeItem(it)) || S(iconeItem(it), 2)}</div>`
        : `<div class="slot-px celula vazia" data-vaga="${i}"></div>`);
    }
    const bolsa = heroi.bolsa.map((b) => `<div class="slot-px clicavel" data-usar="${h(b.id)}" ${dica(`<b>${h(b.nome)}</b><div>${Realce.texto(b.desc)}</div>${b.id === "tocha" ? "" : '<div class="rodape">Clique para usar · botão direito: usar em você.</div>'}`)}>${Icones.consumivel(b.id) || S(iconeConsumivel(b.id), 2)}<span class="qtd">${b.qtd}</span></div>`).join("");
    const heroiSel = p.id === "heroi";
    const subtitulo = heroiSel ? `${h(p.titulo)} · nível&nbsp;${p.nivel} · ${p.xp}/${p.xp_proximo}&nbsp;XP`
      : `${h(p.titulo)} · vida ${p.hp}/${p.max_hp}${p.ferido ? " · ferido, fora das lutas até descansar" : ""}`;
    const sugerir = !heroiSel && p.pontos_atributo
      ? `<button type="button" class="botao-grupo sugerir" data-sugerir="${h(p.id)}"${p.indisponivel ? ` disabled title="${h(p.indisponivel)}"` : ""}>Distribuir pela sugestão <small>${h(p.sugestao)}</small></button>` : "";
    return `<div class="tela inventario${grupo ? " com-grupo" : ""}">${abas}
      <div class="inv-corpo"><div class="boneco">${espacos}<div class="boneco-retrato">${Icones.retrato(heroiSel ? p.classe : p.id, `Retrato: ${h(p.nome)}`) || (heroiSel ? S(p.classe, 6) : retratoDe(p, 48))}</div></div>
        <div class="peca-detalhe" aria-live="polite">${detalheHtml(p)}</div></div>
      <div class="inv-lado">
        <div class="ficha-mini"><div class="heroi-nome">${h(p.nome)}</div><div class="heroi-titulo">${subtitulo}</div>
          ${heroiSel ? "" : `<div class="pecas">${h(p.pecas)}</div>`}${p.indisponivel ? `<div class="pior">${h(p.indisponivel)}</div>` : ""}</div>
        ${baseHtml(p, true)}${sugerir}<div class="atributos">${atributosHtml(p)}</div>
        <h4>${grupo ? "Bolsa do grupo" : "Mochila"} <small>${heroi.mochila.length}/${limite}</small></h4>
        <div class="mochila-grade">${celulas.join("")}<div class="slot-px lixeira" title="Arraste um item aqui para largar">${S("caveira", 2, "fantasma")}<span class="espaco-nome">Largar</span></div></div>
        <h4>Bolsa</h4><div class="slots">${bolsa || '<span class="vazio">vazia</span>'}</div>
      </div></div>`;
  }

  /** A peça marcada (ou null): da bolsa ou do corpo do selecionado. */
  function pecaMarcada(p) {
    if (!marcado) return null;
    if (marcado.de === "mochila") return App.estado.heroi.mochila[marcado.i] || null;
    return p.equip[marcado.s] || null;
  }

  /** O que dá para fazer com uma peça, para os botões da ficha e o menu do botão direito: {rotulo, nota, motivo,
   *  pedido}. O motor confere tudo de novo; aqui é para quem joga ver antes o que vai acontecer e por que não. */
  function acoesDe(alvo, p = atual()) {
    const heroi = App.estado.heroi, fs = fichas();
    const cheia = heroi.mochila.length >= limiteBolsa();
    const acoes = [];
    // vestir `it` em `f`: uma entrada por espaço quando os dois anéis estão ocupados (a escolha é de quem joga)
    const vestir = (it, f, base, saiDe, destino) => {
      const espacos = ESPACOS[it.slot] || [it.slot];
      const motivo = f.indisponivel || (!serve(f, it) ? Telas.naoUsa(it, f) : null);
      const destinos = destino ? [destino]
        : espacos.length > 1 && espacos.every((s) => f.equip[s]) ? espacos : [espacos.find((s) => !f.equip[s]) || espacos[0]];
      destinos.forEach((s) => {
        const antiga = f.equip[s];
        const deOutro = saiDe && saiDe.id !== f.id;
        const nota = [deOutro ? `sai de ${quemTexto(saiDe)}` : "", antiga ? `${antiga.nome} volta para a bolsa` : ""].filter(Boolean).join("; ");
        acoes.push({ rotulo: `Equipar em ${quemTexto(f)}${destinos.length > 1 ? ` · ${NOME_ESPACO[s]}` : ""}`, nota,
          motivo: motivo || (antiga && deOutro && cheia ? `A bolsa está cheia: ${antiga.nome} não teria para onde ir.` : null),
          pedido: { op: "vestir", quem: f.id, ...base, destino: s } });
      });
    };
    if (alvo.de === "mochila") {
      const it = heroi.mochila[alvo.i];
      if (!it) return acoes;
      vestir(it, p, { mochila: alvo.i });
      fs.filter((f) => f.id !== p.id && !f.indisponivel && serve(f, it)).forEach((f) => vestir(it, f, { mochila: alvo.i }));
    } else if (alvo.de === "outro") {  // da lista de um espaço: a peça que outro usa, para este espaço
      vestir(alvo.it, p, { de: alvo.dono.id, de_espaco: alvo.s }, alvo.dono, alvo.destino);
    } else {
      const it = p.equip[alvo.s];
      if (!it) return acoes;
      acoes.push({ rotulo: "Guardar na bolsa", nota: "", motivo: p.indisponivel || (cheia ? `A bolsa está cheia (${limiteBolsa()} de ${limiteBolsa()}).` : null),
        pedido: { op: "tirar", quem: p.id, espaco: alvo.s } });
      fs.filter((f) => f.id !== p.id && !f.indisponivel && serve(f, it))
        .forEach((f) => vestir(it, f, { de: p.id, de_espaco: alvo.s }, p));
      if (p.indisponivel) acoes.forEach((a) => { a.motivo = a.motivo || p.indisponivel; });
    }
    return acoes;
  }

  /** As peças que servem num espaço do selecionado: as da bolsa e as que outros usam (vestir tira de quem usa). */
  function pecasPara(p, s) {
    const heroi = App.estado.heroi, tipo = s.startsWith("anel") ? "anel" : s;
    const lista = [];
    heroi.mochila.forEach((it, i) => { if (it.slot === tipo && serve(p, it)) lista.push({ it, alvo: { de: "mochila", i } }); });
    fichas().filter((f) => f.id !== p.id && !f.indisponivel).forEach((f) => (ESPACOS[tipo] || [tipo]).forEach((e) => {
      const it = f.equip[e];
      if (it && serve(p, it)) lista.push({ it, dono: f, alvo: { de: "outro", it, dono: f, s: e, destino: s } });
    }));
    return lista;
  }

  const botaoAcao = (a, k) => `<button type="button" class="acao-peca${a.motivo ? " bloqueada" : ""}" data-acao="${k}"${a.motivo ? ` aria-disabled="true" title="${h(a.motivo)}"` : ""}>${h(a.rotulo)}${a.nota ? `<small>${h(a.nota)}</small>` : ""}</button>`;

  /** A ficha da peça marcada: a ficha do jogo comparada com o selecionado e as ações à vista (sem depender do botão
   *  direito nem do arrasto). Num espaço marcado, as peças que servem nele. */
  function detalheHtml(p) {
    if (!marcado) return "";  // nada marcado: a caixa fica vazia e oculta (a coluna mantém a largura)
    const it = pecaMarcada(p);
    let html = "";
    if (it) {
      const acoes = acoesDe(marcado, p);
      html += `<div class="detalhe-ficha">${Telas.htmlItem(it, "", marcado.de === "mochila", p)}</div>
        <div class="detalhe-acoes">${acoes.map(botaoAcao).join("")}</div>`;
      // o motivo do bloqueio por extenso, uma vez (no botão ele fica na dica)
      const motivos = [...new Set(acoes.filter((a) => a.motivo).map((a) => a.motivo))].filter((m) => m !== Telas.naoUsa(it, p) && m !== p.indisponivel);  // esses já estão à vista
      if (motivos.length && !acoes.some((a) => !a.motivo)) html += `<div class="pior detalhe-motivo">${motivos.map(h).join("<br>")}</div>`;
    }
    if (marcado.de === "espaco") {
      const lista = pecasPara(p, marcado.s);
      html += `<h5>Peças para ${h(Telas.nomeEspaco(marcado.s, p.classe))}</h5>` + (lista.length
        ? `<div class="pecas-espaco">${lista.map((x, k) => `<button type="button" class="peca-opcao" data-opcao="${k}" ${dicaItem(x.it, "", true, p)}>${Icones.equipamento(iconeItem(x.it)) || S(iconeItem(x.it), 2)}<span>${h(x.it.nome)}<small>${x.dono ? `com ${h(quemTexto(x.dono))}` : "na bolsa"}</small></span></button>`).join("")}</div>`
        : `<div class="detalhe-vazio">Nenhuma peça do grupo serve aqui.</div>`);
    }
    return html;
  }

  const ICONE_ATTR = { Ataque: "espada", Defesa: "escudo", Agilidade: "folha", Poder: "chama" };
  /** Atributos com dica: para que servem e o que você ganha com cada ponto. */
  // Atributos a caminho: enquanto o selo de "+2 Ataque" voa, o painel mostra o valor de antes (ver seloAtributo).
  const chegando = new Map();
  function atributosHtml(p) {
    const info = p.atributos_info || {}, penal = p.atributos_penal || {};
    const heroiSel = !p.id || p.id === "heroi";
    return Object.entries(p.atributos).map(([k, v]) => {
      const linhas = (info[k] || []).map((l, i) => `<li${penal[k] && !i ? ' class="pior"' : ""}>${h(l)}</li>`).join("");
      // Abaixo do normal (ferimento, fome): o número já vem com a penalidade, em vermelho, e quanto ela tira vem do
      // motor (atributos_penal): ao lado do valor e na dica.
      const pen = penal[k] ? ` <span class="penal">(−${penal[k].pct}%)</span>` : "";
      const aoLado = penal[k] ? ` <small class="valor-penal">−${penal[k].pct}%</small>` : "";
      return `<div class="atributo${penal[k] ? " abaixo" : ""}" data-atributo="${h(k)}" ${dica(`<b>${h(k)} ${v}${pen}</b><ul class="dica-lista">${linhas}</ul>`)}>${Icones.atributo(k) || S(ICONE_ATTR[k] || "estrela", 1)}<span class="nome">${h(k)}</span><span class="valor"><span class="num">${heroiSel && chegando.has(k) ? chegando.get(k) : v}</span>${aoLado}</span></div>`;
    }).join("");
  }
  /** Os seis atributos e a Presença (etapa 4): a sigla e o valor, com a dica do motor (o que cada ponto dá, quanto soma
   *  agora, o teste do d20 que usa). Com pontos da subida de nível, o "+" de cada um (o motor diz se dá: `mais`; o clique
   *  é a opção escondida `atributo` ou, num companheiro, o pedido da janela do grupo). A Presença não recebe pontos: sobe
   *  sozinha a cada 3 níveis. */
  function baseHtml(p, conceitos = false) {
    const lista = p.atributos_base || [];
    if (!lista.length) return "";
    const quem = p.id && p.id !== "heroi" ? p.id : "";
    // o "+" vale fora da luta (o motor oferece a distribuição nos menus do lugar e na ficha); na luta, apagado
    const emLuta = !!(App.estado && App.estado.combate);
    const celulas = lista.map((a) => {
      const motivo = a.mais && (a.mais.motivo || (emLuta ? "Distribua fora da luta." : null));
      const mais = a.mais ? `<button type="button" class="attr-mais" data-atributo="${h(a.id)}"${quem ? ` data-quem="${h(quem)}"` : ""}${motivo ? ` disabled title="${h(motivo)}"` : ""} aria-label="+1 de ${h(a.nome)}">+</button>` : "";
      return `<div class="attr-base" tabindex="0" ${dica(`<b>${h(a.nome)} ${a.valor}</b><ul class="dica-lista">${a.linhas.map((l) => `<li>${Realce.texto(l)}</li>`).join("")}</ul>`)}>
        <small>${h(a.sigla)}</small><b>${a.valor}</b>${mais}</div>`;
    }).join("");
    const pontos = p.pontos_atributo ? `<div class="attr-pontos">${Texto.plural(p.pontos_atributo, "ponto")} de atributo para distribuir</div>` : "";
    // o crítico e a Tenacidade: cada um com a dica própria (nascem da Percepção e da Vontade)
    const derivados = conceitos && (p.conceitos || []).length ? `<div class="atributos-conceitos">${p.conceitos.map((c) =>
      `<div class="attr-conceito" tabindex="0" data-conceito="${h(c.id)}" ${dica(`<b>${h(c.nome)} ${h(c.valor)}</b><ul class="dica-lista">${c.linhas.map((l) => `<li>${Realce.texto(l)}</li>`).join("")}</ul>`)}><span>${h(c.nome)}</span><b>${h(c.valor)}</b></div>`).join("")}</div>` : "";
    return `${pontos}<div class="atributos-base">${celulas}</div>${derivados}`;
  }
  /** O "+" de um atributo (a ficha e o quadro da ficha lateral): a ação escondida do motor. */
  function ligarMais(raiz) {
    raiz.querySelectorAll(".attr-mais:not([disabled])").forEach((b) => b.addEventListener("click", (ev) => {
      ev.stopPropagation();
      const pedido = b.dataset.quem ? App.acao({ equipamento: true }, "equipar", { op: "atributo", quem: b.dataset.quem, atributo: b.dataset.atributo })
        : App.acao({ atributo: b.dataset.atributo }, "equipar");
      // sem a opção na pergunta de agora (uma cena no meio, um evento), o motivo em vez de nada
      if (!pedido) aviso("Distribua os pontos num menu do lugar ou na ficha.", "info", "pergaminho");
    }));
  }
  /** Os testes do d20 numa linha da ficha, com a dica: o bônus de cada teste e de onde vem (nível, atributo, classe),
   *  o que a situação de agora muda (sem luz), para que serve e se o atributo de origem está abaixo do normal. Tudo
   *  do motor (estado.heroi.testes; web/estado.py, explicar_testes). Seis números fixos ficam só na dica. */
  function testesHtml(p) {
    const t = p.testes || {};
    const n = (v) => `${v >= 0 ? "+" : "−"}${Math.abs(v)}`;
    const linhas = Object.entries(t).map(([nome, x]) => {
      const de = x.fixas.length ? x.fixas.map(([r, v]) => `${h(r)} ${n(v)}`).join(" · ") : "sem bônus";
      const agora = x.situacao.length ? `<div class="pior">Agora: ${x.situacao.map(([r, v]) => `${h(r)} ${n(v)}`).join(", ")} → <b>${n(x.mod)}</b></div>` : "";
      const abaixo = x.abaixo.map((l) => `<div class="pior">${h(l)}</div>`).join("");
      return `<li><b>${h(nome)} ${n(x.fixo)}</b> <small>${de}</small>${agora}${abaixo}<div class="uso">${h(x.uso)}</div></li>`;
    }).join("");
    const extra = p.dificuldade_extra ? ` (agora +${p.dificuldade_extra})` : "";
    return `<div class="testes-ficha" tabindex="0" ${dica(`<b>Testes do d20</b><div class="tipo">d20 + bônus contra a dificuldade</div>
      <ul class="dica-lista testes-lista">${linhas}</ul>
      <div class="rodape">Tire 20 e passa sempre; 1 falha sempre. A dificuldade depende da situação e sobe 1 a cada dois níveis seus${extra}.</div>`)}>
      <span class="d20">${Dado20.icone()}</span><span class="nome">Testes do d20</span><span class="seta" aria-hidden="true">›</span></div>`;
  }
  function reputacaoHtml(p) {
    const r = p.reputacao_info || { titulo: "", linhas: [] };
    const valor = Realce.sinais(`${p.reputacao > 0 ? "+" : p.reputacao < 0 ? "−" : ""}${Math.abs(p.reputacao)}`);
    return `<div class="reputacao" ${dica(`<b>Reputação</b><div class="aprov-agora">${h(r.titulo)} <span class="aprov-num">${valor}</span></div><ul class="dica-lista">${r.linhas.map((l) => `<li>${Realce.sinais(l)}</li>`).join("")}</ul>`)}>
      <span class="rep-icone">${S("coroa", 2)}</span><b>${p.reputacao > 0 ? "+" : ""}${p.reputacao}</b><span class="rep-titulo">${h(r.titulo)}</span></div>`;
  }

  // ------------------------------------------------------------------ pedidos e menu
  /** Um pedido ao motor (vestir, tirar, mover, atributo, sugestão). Um por vez; a janela volta desenhada. */
  function pedir(pedido, foco) {
    if (enviando) return false;
    fecharMenuItem();
    esconderDica();
    if (!App.acao({ equipamento: true }, pedido.op === "mover" ? null : "equipar", pedido)) {
      aviso("Agora não dá para mexer no equipamento.", "info", "pergaminho");
      return false;
    }
    enviando = true;
    focoDepois = foco || null;
    if (pedido.op !== "mover") marcado = null;
    return true;
  }
  /** Fazer a ação: bloqueada, o motivo no próprio controle (som e aviso); senão, o pedido. */
  function fazer(a, controle, foco) {
    if (a.motivo) { App.recusar(controle, a.motivo); return; }
    pedir(a.pedido, foco);
  }

  /** O menu do botão direito (e da tecla de menu): as ações da peça, na janela de item do jogo. Cabe na tela, anda
   *  com as setas, fecha com Esc e devolve o foco a quem o abriu. */
  function abrirMenu(ancora, alvo, titulo) {
    const acoes = acoesDe(alvo);
    fecharMenuItem();
    esconderDica();
    if (!acoes.length) return;
    const m = document.createElement("div");
    m.className = "menu-item m-janela menu-grupo";
    m.setAttribute("role", "menu");
    m.setAttribute("aria-label", titulo);
    m.innerHTML = `<b>${h(titulo)}</b>${acoes.map((a, k) => `<button type="button" role="menuitem" data-k="${k}"${a.motivo ? ' aria-disabled="true" class="bloqueada"' : ""}>${h(a.rotulo)}${a.nota || a.motivo ? `<span class="menu-nota">${h(a.motivo || a.nota)}</span>` : ""}</button>`).join("")}
      <button type="button" role="menuitem" data-k="-" class="secundaria">Cancelar</button>`;
    document.body.appendChild(m);
    const r = ancora.getBoundingClientRect();
    m.style.left = Math.max(8, Math.min(innerWidth - m.offsetWidth - 8, r.left)) + "px";
    m.style.top = Math.max(8, r.bottom + 6 + m.offsetHeight > innerHeight ? r.top - m.offsetHeight - 6 : r.bottom + 6) + "px";
    const botoes = [...m.querySelectorAll("button")];
    const voltar = () => { fecharMenuItem(); if (ancora.isConnected) ancora.focus(); };
    m.addEventListener("click", (ev) => {
      const bt = ev.target.closest("button");
      if (!bt) return;
      ev.stopPropagation();
      if (bt.dataset.k === "-") { voltar(); return; }
      const a = acoes[Number(bt.dataset.k)];
      if (a.motivo) { App.recusar(bt, a.motivo); return; }
      fazer(a, bt, chaveFoco(ancora));
    });
    m.addEventListener("keydown", (ev) => {
      const i = botoes.indexOf(document.activeElement);
      if (ev.key === "Escape") { ev.preventDefault(); ev.stopPropagation(); voltar(); }
      else if (ev.key === "ArrowDown" || ev.key === "ArrowUp") {
        ev.preventDefault();
        botoes[(i + (ev.key === "ArrowDown" ? 1 : botoes.length - 1)) % botoes.length].focus();
      } else if (ev.key === "Home" || ev.key === "End") { ev.preventDefault(); botoes[ev.key === "Home" ? 0 : botoes.length - 1].focus(); }
      else if (ev.key === "Tab") { ev.preventDefault(); voltar(); }
    });
    botoes[0].focus();
    fecharAoClicarFora();
  }

  /** O seletor de um elemento da janela, para devolver o foco depois do redesenho. */
  function chaveFoco(el) {
    if (!el || !el.dataset) return null;
    for (const k of ["mochila", "espaco", "aba", "vaga"]) if (el.dataset[k] !== undefined) return `[data-${k}="${el.dataset[k]}"]`;
    return null;
  }

  // ------------------------------------------------------------------ ligar
  function ligarInventario(raiz, d) {
    const heroi = App.estado && App.estado.heroi;
    if (!heroi) return;
    const p = atual();
    ligarMais(raiz);
    const redesenhar = (foco) => {
      if (!raiz.isConnected) return;
      const novo = Telas.painel({ tipo: "personagem", dados: d });
      raiz.replaceWith(novo);
      const alvo = foco && novo.querySelector(foco);
      if (alvo) alvo.focus();
    };
    // as abas: clique, ou ← → no teclado (Home e End nas pontas), como as abas de verdade
    raiz.querySelectorAll("[data-aba]").forEach((b) => {
      b.addEventListener("click", () => { if (selId !== b.dataset.aba) { selId = b.dataset.aba; marcado = null; redesenhar(`[data-aba="${b.dataset.aba}"]`); } });
      b.addEventListener("keydown", (ev) => {
        const ids = fichas().map((f) => f.id), i = ids.indexOf(selId);
        const k = { ArrowRight: i + 1, ArrowLeft: i - 1 + ids.length, Home: 0, End: ids.length - 1 }[ev.key];
        if (k === undefined) return;
        ev.preventDefault();
        selId = ids[k % ids.length];
        marcado = null;
        redesenhar(`[data-aba="${selId}"]`);
      });
    });
    // um clique escolhe a peça (ou o espaço) e mostra a ficha: nada de equipar. Só a ficha e a marca mudam, sem
    // redesenhar a janela (o segundo clique de um duplo clique cai no mesmo elemento).
    const detalhe = raiz.querySelector(".peca-detalhe");
    const marcar = (alvo, el) => {
      marcado = alvo;
      raiz.querySelectorAll(".marcado").forEach((x) => x.classList.remove("marcado"));
      el.classList.add("marcado");
      detalhe.innerHTML = detalheHtml(p);
      Telas.ligarDicas(detalhe);
      ligarDetalhe();
    };
    function ligarDetalhe() {
      const acoes = marcado && pecaMarcada(p) ? acoesDe(marcado, p) : [];
      const ancora = () => raiz.querySelector(".marcado");
      detalhe.querySelectorAll("[data-acao]").forEach((b) => b.addEventListener("click", () => fazer(acoes[Number(b.dataset.acao)], b, chaveFoco(ancora()))));
      const lista = marcado && marcado.de === "espaco" ? pecasPara(p, marcado.s) : [];
      detalhe.querySelectorAll("[data-opcao]").forEach((b) => b.addEventListener("click", () => {
        const x = lista[Number(b.dataset.opcao)];
        // a peça vai para ESTE espaço (o anel escolhido é respeitado)
        const a = x.alvo.de === "mochila" ? acoesDe(x.alvo, p).find((y) => y.pedido.quem === p.id) : acoesDe(x.alvo, p)[0];
        if (!a) return;
        fazer({ ...a, pedido: { ...a.pedido, destino: marcado.s } }, b, `[data-espaco="${marcado.s}"]`);
      }));
    }
    ligarDetalhe();
    const sugerir = raiz.querySelector("[data-sugerir]");
    if (sugerir && !sugerir.disabled) sugerir.addEventListener("click", () => pedir({ op: "sugestao", quem: sugerir.dataset.sugerir }));

    // a ação padrão dos dois cliques: equipar no selecionado (a peça da bolsa) ou guardar (a do corpo). O anel com os
    // dois espaços ocupados abre a escolha, em vez de trocar um deles por conta própria.
    const padrao = (alvo, el) => {
      const acoes = acoesDe(alvo, p);
      const minhas = alvo.de === "mochila" ? acoes.filter((a) => a.pedido.quem === p.id) : acoes.filter((a) => a.pedido.op === "tirar");
      if (minhas.length > 1) { abrirMenu(el, alvo, pecaMarcada(p).nome); return; }
      if (minhas.length) fazer(minhas[0], el, chaveFoco(el));
    };
    raiz.querySelectorAll("[data-mochila], [data-espaco]").forEach((el) => {
      const alvo = el.dataset.mochila !== undefined ? { de: "mochila", i: Number(el.dataset.mochila) } : { de: "espaco", s: el.dataset.espaco };
      el.addEventListener("click", () => marcar(alvo, el));
      el.addEventListener("dblclick", (ev) => {
        ev.preventDefault();
        if (alvo.de === "espaco" && !p.equip[alvo.s]) return;
        padrao(alvo, el);
      });
      el.addEventListener("contextmenu", (ev) => {
        ev.preventDefault();
        if (alvo.de === "espaco" && !p.equip[alvo.s]) { marcar(alvo, el); return; }
        marcar(alvo, el);
        abrirMenu(el, alvo, (alvo.de === "mochila" ? heroi.mochila[alvo.i] : p.equip[alvo.s]).nome);
      });
      el.addEventListener("keydown", (ev) => {
        if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); marcar(alvo, el); }
        else if (ev.key === "ContextMenu" || (ev.key === "F10" && ev.shiftKey)) {
          ev.preventDefault();
          marcar(alvo, el);
          if (pecaMarcada(p)) abrirMenu(el, alvo, pecaMarcada(p).nome);
        }
      });
    });

    // arrastar: da bolsa para um espaço que serve (equipar), do corpo para a bolsa (guardar, onde soltar), de um lugar
    // da bolsa a outro (reordenar). Soltar fora ou cancelar (Esc) não muda nada; os destinos que valem acendem.
    let arrastando = null;
    const limpar = () => { raiz.querySelectorAll(".alvo").forEach((x) => x.classList.remove("alvo")); arrastando = null; };
    raiz.querySelectorAll("[draggable=true]").forEach((el) => {
      el.addEventListener("dragstart", (ev) => {
        esconderDica();
        fecharMenuItem();
        arrastando = el.dataset.mochila !== undefined ? { de: "mochila", i: Number(el.dataset.mochila) } : { de: "espaco", espaco: el.dataset.espaco };
        ev.dataTransfer.setData("text/plain", "item");
        ev.dataTransfer.effectAllowed = "move";
        if (arrastando.de === "mochila") {
          const it = heroi.mochila[arrastando.i];
          if (!p.indisponivel && serve(p, it)) {
            (ESPACOS[it.slot] || []).forEach((s) => { const alvo = raiz.querySelector(`[data-espaco="${s}"]`); if (alvo) alvo.classList.add("alvo"); });
          }
          raiz.querySelectorAll("[data-mochila], [data-vaga]").forEach((x) => { if (x !== el) x.classList.add("alvo"); });
          raiz.querySelector(".lixeira").classList.add("alvo");
        } else if (!p.indisponivel) raiz.querySelector(".mochila-grade").classList.add("alvo");
      });
      el.addEventListener("dragend", limpar);
    });
    const aceitar = (alvo, ok) => alvo.addEventListener("dragover", (ev) => { if (arrastando && ok(arrastando)) ev.preventDefault(); });
    raiz.querySelectorAll("[data-espaco]").forEach((alvo) => {
      const s = alvo.dataset.espaco;
      aceitar(alvo, (a) => a.de === "mochila" && !p.indisponivel && serve(p, heroi.mochila[a.i]) && (ESPACOS[heroi.mochila[a.i].slot] || []).includes(s));
      alvo.addEventListener("drop", (ev) => {
        ev.preventDefault();
        const a = arrastando; limpar();
        if (a && a.de === "mochila") pedir({ op: "vestir", quem: p.id, mochila: a.i, destino: s }, `[data-espaco="${s}"]`);
      });
    });
    // cada célula da bolsa (cheia ou vazia) recebe: outra peça da bolsa (reordenar) ou a do corpo (guardar ali)
    raiz.querySelectorAll("[data-mochila], [data-vaga]").forEach((cel) => {
      const k = Number(cel.dataset.mochila ?? cel.dataset.vaga);
      aceitar(cel, (a) => (a.de === "mochila" && a.i !== k) || (a.de === "espaco" && !p.indisponivel));
      cel.addEventListener("drop", (ev) => {
        ev.preventDefault(); ev.stopPropagation();
        const a = arrastando; limpar();
        if (!a) return;
        const para = Math.min(k, heroi.mochila.length - (a.de === "mochila" ? 1 : 0));
        if (a.de === "mochila" && a.i !== para) pedir({ op: "mover", de: a.i, para }, `[data-mochila="${para}"]`);
        else if (a.de === "espaco") pedir({ op: "tirar", quem: p.id, espaco: a.espaco, posicao: Math.min(k, heroi.mochila.length) }, `[data-espaco="${a.espaco}"]`);
      });
    });
    const grade = raiz.querySelector(".mochila-grade");
    aceitar(grade, (a) => a.de === "espaco" && !p.indisponivel);
    grade.addEventListener("drop", (ev) => {
      if (ev.target.closest(".lixeira")) return;
      ev.preventDefault();
      const a = arrastando; limpar();
      if (a && a.de === "espaco") pedir({ op: "tirar", quem: p.id, espaco: a.espaco });
    });
    const lixo = raiz.querySelector(".lixeira");
    aceitar(lixo, (a) => a.de === "mochila");
    lixo.addEventListener("drop", (ev) => {
      ev.preventDefault(); ev.stopPropagation();
      const a = arrastando; limpar();
      if (a && a.de === "mochila" && window.confirm(`Largar ${heroi.mochila[a.i].nome}? Não há volta.`)) App.acao({ largar: a.i });
    });

    raiz.querySelectorAll("[data-usar]").forEach((el) => el.addEventListener("click", (ev) => {
      ev.stopPropagation();
      const b = (App.estado.heroi.bolsa || []).find((x) => x.id === el.dataset.usar);
      if (b && b.alvos && b.alvos.length) { menuUso(el, b); return; }
      if (b && b.motivo) { App.som("falha"); App.avisar(b.motivo, el); return; }
      App.acao({ usar: el.dataset.usar }, "item");
    }));
    // Botão direito num consumível: usa em você, sem o menu de "em quem".
    raiz.querySelectorAll("[data-usar]").forEach((el) => el.addEventListener("contextmenu", (ev) => {
      ev.preventDefault();
      const b = (App.estado.heroi.bolsa || []).find((x) => x.id === el.dataset.usar);
      if (b && b.motivo) { App.som("falha"); App.avisar(b.motivo, el); return; }
      App.acao({ usar: el.dataset.usar }, "item");
    }));
    // o foco volta para onde estava antes do pedido (a janela foi redesenhada pelo motor)
    if (focoDepois) {
      const alvo = raiz.querySelector(focoDepois);
      focoDepois = null;
      if (alvo) requestAnimationFrame(() => { if (alvo.isConnected) alvo.focus({ preventScroll: true }); });
    }
  }

  /** Saiu da janela: volta para o herói, sem peça marcada. */
  function esquecer() { selId = "heroi"; marcado = null; focoDepois = null; }

  Object.assign(Telas, { atributosBaseHtml: baseHtml, ligarMaisAtributo: ligarMais });
  Telas.registrar("personagem", personagem, { ligar: ligarInventario, esquecer });

  Object.assign(Telas, { atributosHtml, chegando, reputacaoHtml, testesHtml });
})();
