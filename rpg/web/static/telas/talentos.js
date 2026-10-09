/* Árvore de talentos: a grade sai dos dados (talentos.py, mandados à parte em guardarArvore) e as opções da pergunta
   do motor dizem o que dá para aprender agora. */
"use strict";

(() => {
  const { h, S, faiscas } = Telas;

  let arvore = null, ranksAntes = {};
  function guardarArvore(a) { arvore = a; }
  function abrirTalentos(m) {
    if (!arvore) return false;
    const caixa = document.getElementById("sobre-talentos");
    const idx = {};
    let voltar = null;
    m.opcoes.forEach((o, i) => { if (o.meta && o.meta.talento) idx[o.meta.talento] = i; if (o.meta && o.meta.voltar) voltar = i; });
    App.acaoFecharTalentos = () => App.responder(m.id, voltar);
    const a = arvore;
    document.getElementById("talentos-titulo").textContent = `Talentos · ${a.classe}`;
    // A grade sai dos dados (talentos.py): cada ramo ocupa tantas colunas quanto o maior número de talentos lado a lado
    // numa camada dele; as fileiras são as camadas usadas, cada uma com o nível que pede. Sem teto de tamanho.
    const base = a.nos.filter((n) => n.ramo === "base"), dosRamos = a.nos.filter((n) => n.ramo !== "base");
    const largura = {};
    a.ramos.forEach((r) => { largura[r.id] = 1; });
    dosRamos.forEach((n) => { largura[n.ramo] = Math.max(largura[n.ramo] || 1, n.pos + 1); });
    const total = a.ramos.reduce((soma, r) => soma + largura[r.id], 0);
    const camadasDe = (nos) => [...new Set(nos.map((n) => n.camada))].sort((x, y) => x - y);
    const nivel = (c) => `<div class="arvore-nivel${a.nivel >= a.camadas[String(c)] ? " ok" : ""}">Nv.${a.camadas[String(c)]}</div>`;
    function celula(n, acima) {
      const conecta = n && acima ? " conecta" + (acima.rank > 0 ? " aceso" : "") : "";
      if (!n) return `<div class="arvore-celula${conecta}"></div>`;
      const pode = n.estado === "disponivel" && a.pontos > 0 && idx[n.id] !== undefined;
      const classe = n.estado === "comprado" ? "comprado" : n.estado === "disponivel" ? "disponivel" : n.estado === "bloqueado" ? "bloqueado" : "trancado";
      const novo = ranksAntes[n.id] !== undefined && n.rank > ranksAntes[n.id] ? " aprendeu" : "";
      return `<div class="arvore-celula${conecta}"><div class="no-talento ${classe}${pode ? " pode" : ""}${novo}" data-id="${h(n.id)}">
          ${S(n.icone || "estrela", 3)}<span class="rank">${n.rank}/${n.max}</span></div></div>`;
    }
    // A base, de todos (vem antes da especialização), numa faixa própria acima dos caminhos. Debaixo do título
    // "Paladino", ela parecia do paladino, e um berserker achava que pegava talento alheio.
    const colsBase = Math.max(1, ...base.map((n) => n.pos + 1));
    const grade = (cols) => `style="grid-template-columns: 64px repeat(${cols}, 1fr)"`;
    let html = `<div class="arvore-topo"><span>Nível ${a.nivel} · passe o mouse num talento para ver o que ele faz</span>
      <span class="pontos${a.pontos ? "" : " zero"}">${S("estrela", 2)} ${Texto.plural(a.pontos, "ponto")}</span></div>`;
    if (base.length) {
      html += `<div class="arvore-grade arvore-base" ${grade(colsBase)}><div></div><div class="arvore-base-titulo">Base<small>para todos, antes da especialização</small></div>` +
        camadasDe(base).map((c) => nivel(c) + Array.from({ length: colsBase }, (_, i) => celula(base.find((n) => n.camada === c && n.pos === i))).join("")).join("") + "</div>";
    }
    html += `<div class="arvore-grade" ${grade(total)}><div></div>` + a.ramos.map((r) =>
      `<div class="arvore-col-titulo${r.trancado ? " trancada" : ""}" style="grid-column: span ${largura[r.id]}">${h(r.nome)}<small>${h(r.sub)}</small></div>`).join("");
    const fileiras = camadasDe(dosRamos);
    fileiras.forEach((c, k) => {
      html += nivel(c);
      a.ramos.forEach((r) => {
        for (let p = 0; p < largura[r.id]; p++) {
          const n = dosRamos.find((x) => x.ramo === r.id && x.camada === c && x.pos === p);
          const acima = k > 0 && dosRamos.find((x) => x.ramo === r.id && x.camada === fileiras[k - 1] && x.pos === p);
          html += celula(n, acima);
        }
      });
    });
    html += "</div>";
    document.getElementById("arvore").innerHTML = html;
    ranksAntes = Object.fromEntries(a.nos.map((n) => [n.id, n.rank]));
    const info = document.getElementById("talento-info");
    document.querySelectorAll("#arvore .no-talento").forEach((el) => {
      const n = a.nos.find((x) => x.id === el.dataset.id);
      el.addEventListener("mouseenter", () => {
        info.innerHTML = `<b>${h(n.nome)}</b><div class="r">Grau ${n.rank} de ${n.max}${n.spec ? " · " + h(n.spec) : ""}</div><div>${Realce.texto(n.desc)}</div>` +
          (n.motivo ? `<div class="req">${h(n.motivo[0].toUpperCase() + n.motivo.slice(1))}</div>` : "") +
          (n.estado === "comprado" ? '<div class="acao">Aprendido por completo.</div>' :
            n.estado === "disponivel" ? (a.pontos ? '<div class="acao">Clique para aprender (1 ponto).</div>' : '<div class="req">Sem pontos de talento.</div>') : "");
        info.hidden = false;
        const r = el.getBoundingClientRect();
        info.style.left = Math.min(window.innerWidth - 320, r.right + 12) + "px";
        info.style.top = Math.max(10, r.top - 10) + "px";
      });
      el.addEventListener("mouseleave", () => { info.hidden = true; });
      if (el.classList.contains("pode")) el.addEventListener("click", () => {
        info.hidden = true;
        // Resposta na hora do clique, como no mercado: pop, faíscas, som e o ganho subindo perto do nó.
        App.som("aprender");
        el.animate([{ scale: 1 }, { scale: 1.28, filter: "brightness(2.2)" }, { scale: 1 }], { duration: 260, easing: "cubic-bezier(.2,.8,.3,1.2)" });
        faiscas(el, ["#f2c94c", "#fff3a0", "#8fbf6a"], 18);
        App.avisar(`+1 ${n.nome} (${n.rank + 1}/${n.max})`);
        const pontos = document.querySelector("#arvore .pontos");
        if (pontos) pontos.animate([{ scale: 1 }, { scale: 0.8, filter: "brightness(2)" }, { scale: 1 }], { duration: 220 });
        App.responder(m.id, idx[n.id]);
      });
    });
    caixa.hidden = false;
    return true;
  }

  function fecharTalentos() {
    document.getElementById("sobre-talentos").hidden = true;
    document.getElementById("talento-info").hidden = true;
  }

  Object.assign(Telas, { abrirTalentos, fecharTalentos, guardarArvore });
})();
