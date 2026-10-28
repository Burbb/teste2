/* A demonstração do reforço: a faixa no alto (o que é protótipo fica aqui, fora da tela do jogador) e a tela da forja
   escolhida pelo endereço (?tela=v16, v15, v14, v13, v12, v11, v10, v9, v8, v7, v6, v5, v4, v3, v2 ou v1: as versões antigas, guardadas como histórico;
   sem ele, a atual, a 16ª, com o ganho real em todo reforço, os formatos comuns e o painel de testes). A v3 tem a A anterior e a B, trocadas aqui. Na atual, a faixa também escolhe o caso de teste da próxima
   tentativa (sucesso ou falha forçados, uma vez), separado do sorteio normal, e abre a comparação de teste da peça
   escolhida (o dano contra um alvo fixo: medição do laboratório, fora da tela do jogador). Trocar de versão
   recarrega a página; a partida continua (ela mora no servidor). */
"use strict";

(() => {
  const params = new URLSearchParams(location.search);
  const versao = ["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10", "v11", "v12", "v13", "v14", "v15", "v16"].includes(params.get("tela")) ? params.get("tela") : "atual";
  const base = versao === "atual" ? "/proto/" : `/proto/historico/${versao}/`;
  const css = document.createElement("link");
  css.rel = "stylesheet";
  css.href = `${base}reforco.css`;
  document.head.appendChild(css);
  if (versao === "atual") {  // a candidata das placas de metal (18ª): só vale com "Placas da bancada" no painel
    const placas = document.createElement("link");
    placas.rel = "stylesheet";
    placas.href = "/proto/placas.css";
    document.head.appendChild(placas);
  }
  const js = document.createElement("script");
  js.src = `${base}reforco.js`;
  js.onload = () => faixa();
  document.body.appendChild(js);

  const para = (v) => { const q = new URLSearchParams(location.search); if (v === "atual") q.delete("tela"); else q.set("tela", v); return `?${q}`; };
  function faixa() {
    const f = document.createElement("div");
    f.id = "faixa-demo";
    const P = window.ReforcoProto;
    let extra = "";
    if (versao === "v3" && P && P.direcao) {
      extra = `<span>Forja:</span>${[["A", "A · Bancada"], ["B", "B · Arsenal"]].map(([id, nome]) =>
        `<button type="button" data-direcao="${id}" aria-pressed="${P.direcao() === id}">${nome}</button>`).join("")}`;
    } else if (versao === "atual" && P && P.teste) {
      extra = `<span>Próxima tentativa:</span>${[["", "Sorteio"], ["sucesso", "Sucesso (teste)"], ["falha", "Falha (teste)"]].map(([id, nome]) =>
        `<button type="button" data-teste="${id}" aria-pressed="${(P.teste() || "") === id}">${nome}</button>`).join("")}`;
      if (P.comparacao) extra += `<button type="button" data-comparar aria-pressed="false">Comparação (teste)</button>`;
      if (P.lutaTeste) extra += `<button type="button" data-luta>Luta de teste</button>`;
      if (P.niveisTeste) extra += `<button type="button" data-niveis>Níveis altos (teste)</button>`;
      if (P.essenciasTeste) extra += `<button type="button" data-essteste>Essências (teste)</button>`;
      if (P.nivelTeste) extra += `<button type="button" data-nivteste>Nível +4 (teste)</button>`;
      if (P.transferenciaTeste) extra += `<button type="button" data-trfteste>Transferência (teste)</button>`;
    }
    if (versao === "atual" && P && P.estadoTeste) extra += `<button type="button" data-painel-testes aria-expanded="false" aria-controls="painel-testes">Painel de testes</button>`;
    const versoes = [["atual", "atual"], ["v16", "v16"], ["v15", "v15"], ["v14", "v14"], ["v13", "v13"], ["v12", "v12"], ["v11", "v11"], ["v10", "v10"], ["v9", "v9"], ["v8", "v8"], ["v7", "v7"], ["v6", "v6"], ["v5", "v5"], ["v4", "v4"], ["v3", "v3 (A e B)"], ["v2", "v2"], ["v1", "v1"]].map(([id, nome]) =>
      id === versao ? `<b>${nome}</b>` : `<a href="${para(id)}">${nome}</a>`).join(" · ");
    f.innerHTML = `<strong>Protótipo do reforço</strong>${extra}<span class="faixa-hist">versões: ${versoes}</span>`;
    document.body.appendChild(f);
    f.querySelectorAll("[data-direcao]").forEach((b) => b.addEventListener("click", () => {
      P.direcao(b.dataset.direcao);
      f.querySelectorAll("[data-direcao]").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    }));
    const marcarTeste = () => f.querySelectorAll("[data-teste]").forEach((x) => x.setAttribute("aria-pressed", String((P.teste() || "") === x.dataset.teste)));
    f.querySelectorAll("[data-teste]").forEach((b) => b.addEventListener("click", () => { P.teste(b.dataset.teste); marcarTeste(); }));
    window.addEventListener("reforco-teste", marcarTeste);  // usado uma vez, o caso volta para o sorteio
    // a luta de teste do encantamento: dois Esqueletos, e o grupo volta como estava (só com a forja aberta)
    const luta = f.querySelector("[data-luta]");
    if (luta) luta.addEventListener("click", () => { if (!P.lutaTeste()) aviso("Abra a forja para a luta de teste.", "info", "pergaminho"); });
    // os níveis altos de teste: peças do grupo em +4, +8, +9, +11 e +12 (duas com três gravações), ouro e fragmentos
    const niveis = f.querySelector("[data-niveis]");
    if (niveis) niveis.addEventListener("click", () => { if (!P.niveisTeste()) aviso("Abra a forja para os níveis de teste.", "info", "pergaminho"); });
    // as composições de essências e as peças da transferência (só no save temporário da demonstração)
    f.querySelector("[data-essteste]")?.addEventListener("click", () => { if (!P.essenciasTeste()) aviso("Abra a forja para as essências de teste.", "info", "pergaminho"); });
    f.querySelector("[data-nivteste]")?.addEventListener("click", () => { if (!P.nivelTeste()) aviso("Abra a forja para subir de nível no teste.", "info", "pergaminho"); });
    f.querySelector("[data-trfteste]")?.addEventListener("click", () => { if (!P.transferenciaTeste()) aviso("Abra a forja para a transferência de teste.", "info", "pergaminho"); });
    const botaoPainel = f.querySelector("[data-painel-testes]");
    if (botaoPainel) painelTestes(botaoPainel, P);
    // a comparação de teste: um painel embaixo da faixa, com a peça escolhida (atualizado a cada desenho da forja)
    const comparar = f.querySelector("[data-comparar]");
    if (comparar) {
      const painel = document.createElement("div");
      painel.id = "faixa-comparacao";
      painel.hidden = true;
      document.body.appendChild(painel);
      const encher = () => { painel.innerHTML = P.comparacao() || "<p>Escolha uma peça com reforço disponível.</p>"; };
      comparar.addEventListener("click", () => {
        painel.hidden = !painel.hidden;
        comparar.setAttribute("aria-pressed", String(!painel.hidden));
        encher();
      });
      window.addEventListener("reforco-comparacao", () => { if (!painel.hidden) encher(); });
    }
  }
  /* O painel de testes (16ª; só nesta demonstração, nunca no jogo): editar e aplicar são passos separados. Mexer num
     campo não muda nada; "Aplicar na sessão" leva o ouro e os materiais (validados pelo motor); "Aplicar e reiniciar
     cenário" reconstrói o personagem pelo caminho do jogo com o nível, a classe e a especialização escolhidos e
     descarta a sessão temporária. Nada se aplica com uma tentativa, uma cena ou uma confirmação em andamento. As
     candidatas visuais (acabamento das armaduras, paleta da celebração) trocam na hora: são só aparência. O botão A
     está aprovado e não tem mais escolha. */
  const ferreiro = () => (/(?:^|; )rf-ferreiro=candidata/.test(document.cookie) ? "candidata" : "jogo");
  function painelTestes(botao, P) {
    const el = document.createElement("div");
    el.id = "painel-testes";
    el.hidden = true;
    el.setAttribute("role", "region");
    el.setAttribute("aria-label", "Painel de testes do protótipo");
    document.body.appendChild(el);
    const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
    let base = null;  // os valores de agora, quando o painel foi preenchido
    const opcoesSpec = (t, classe, nivel, atual) => {
      const c = t.classes.find((x) => x.id === classe);
      if (nivel < t.nivel_spec) return `<option value="">— (a partir do nível ${t.nivel_spec})</option>`;
      return c.specs.map((s) => `<option value="${s.id}"${s.id === atual ? " selected" : ""}>${esc(s.nome)}</option>`).join("");
    };
    const grupo = (k, rotulo, ops) => `<div class="pt-linha"><span>${rotulo}</span><span class="pt-seg" role="radiogroup" aria-label="${esc(rotulo)}">${ops.map(([v, n]) =>
      `<button type="button" role="radio" data-pref="${k}" data-valor="${v}" aria-checked="${P.pref(k) === v}">${n}</button>`).join("")}</span></div>`;
    function preencher() {
      const t = P.estadoTeste();
      if (!t) { el.innerHTML = `<p class="pt-aviso">Abra a forja para editar o cenário.</p>${visuais()}`; ligarVisuais(); return; }
      base = t;
      const fr = t.materiais.find((m) => m.id === "fragmento");
      const ess = t.materiais.filter((m) => m.essencia);
      const familias = [...new Set(ess.map((m) => m.nome.replace(/^Essência de /, "").replace(/ I+$/, "")))];
      el.innerHTML = `<div class="pt-cab"><b>Painel de testes</b><button type="button" data-pt-recarregar title="Volta os campos aos valores de agora">Valores de agora</button></div>
        <fieldset><legend>Personagem · reinicia o cenário</legend>
          <label class="pt-linha"><span>Nível</span><input type="number" data-pt="nivel" min="1" max="${t.nivel_max}" value="${t.nivel}"></label>
          <label class="pt-linha"><span>Classe</span><select data-pt="classe">${t.classes.map((c) => `<option value="${c.id}"${c.id === t.classe ? " selected" : ""}>${esc(c.nome)}</option>`).join("")}</select></label>
          <label class="pt-linha"><span>Especialização</span><select data-pt="spec">${opcoesSpec(t, t.classe, t.nivel, t.spec)}</select></label>
          <button type="button" data-pt-aplicar="teste_cenario" class="pt-perigo">Aplicar e reiniciar cenário</button>
          <p class="pt-nota">Descarta a sessão temporária: as peças, os reforços e as gravações voltam ao cenário inicial da classe.</p>
        </fieldset>
        <fieldset><legend>Sessão · aplica sem reiniciar</legend>
          <label class="pt-linha"><span>Ouro</span><input type="number" data-pt="ouro" min="0" max="999999" value="${t.ouro}"></label>
          <label class="pt-linha"><span>Fragmentos de Têmpera</span><input type="number" data-pt-mat="fragmento" min="0" max="${t.pilha}" value="${fr ? fr.qtd : 0}"></label>
          <table class="pt-ess"><thead><tr><th>Essência</th><th>I</th><th>II</th><th>III</th></tr></thead><tbody>${familias.map((nome) => `<tr><th>${esc(nome)}</th>${[1, 2, 3].map((tier) => {
            const m = ess.find((x) => x.nome === `Essência de ${nome} ${["", "I", "II", "III"][tier]}`);
            return `<td><input type="number" data-pt-mat="${m.id}" min="0" max="${t.pilha}" value="${m.qtd}" aria-label="${esc(m.nome)}"></td>`;
          }).join("")}</tr>`).join("")}</tbody></table>
          <button type="button" data-pt-aplicar="teste_sessao">Aplicar na sessão</button>
        </fieldset>
        ${visuais()}
        <p class="pt-estado" role="status" aria-live="polite"></p>`;
      ligar();
    }
    const visuais = () => `<fieldset><legend>Comparação visual · troca na hora</legend>
      ${grupo("armadura", "Armaduras +9 a +12", [["a", "A · Alternadas"], ["b", "B · Gradual"], ["c", "C · Secundário"], ["feixe", "Feixe 17ª"], ["anterior", "Veio"]])}
      ${P.vitrineArmaduras ? `<div class="pt-linha"><span>Vitrine (as mesmas peças)</span><span class="pt-seg"><button type="button" data-vitrine-tam aria-pressed="false">Ampliar 2×</button></span></div>${P.vitrineArmaduras()}` : ""}
      ${grupo("paleta", "Celebração +9 a +12", [["candidata", "Candidata"], ["anterior", "Anterior"], ["referencia13", "Ouro (ref. +13)"]])}
      ${grupo("placas", "Botões e painéis", [["jogo", "Como no jogo"], ["bancada", "Placas da bancada"]])}
      <div class="pt-linha"><span>Ferreiro (recarrega)</span><span class="pt-seg" role="radiogroup" aria-label="Ferreiro">${[["jogo", "Como no jogo"], ["candidata", "Gesto candidato"]].map(([v, n]) =>
        `<button type="button" role="radio" data-ferreiro="${v}" aria-checked="${ferreiro() === v}">${n}</button>`).join("")}</span></div>
      <div class="pt-linha"><span>Festa da especialização</span><span class="pt-seg"><button type="button" data-festa-spec>Mostrar</button></span></div>
      <p class="pt-nota">A festa é só a tela (nada muda na partida). A escolha de verdade: Taverna → Dormir, com o herói no nível 4 sem especialização.</p></fieldset>`;
    function ligarVisuais() {
      // o gesto candidato do ferreiro: o servidor da demonstração troca a tira pelo cookie; a cena lê a tira ao carregar
      el.querySelectorAll("[data-ferreiro]").forEach((b) => b.addEventListener("click", () => {
        if (ferreiro() === b.dataset.ferreiro) return;
        document.cookie = `rf-ferreiro=${b.dataset.ferreiro}; path=/; SameSite=Strict`;
        location.reload();
      }));
      // a festa da especialização com dados de exemplo, para ver o Continuar dela (a tela só; o motor não participa)
      el.querySelector("[data-festa-spec]")?.addEventListener("click", () => {
        Telas.celebrar({ tipo: "spec", dados: { id: "paladino", nome: "Paladino", desc: "Juramento da Luz. Cura a si mesmo, fere mortos-vivos e corrompidos com poder sagrado.",
          habilidades: [{ nome: "Golpe Sagrado", desc: "Causa 130% do Ataque + 80% do Poder em dano sagrado.", icone: "estrela" }] } }, false);
      });
      el.querySelector("[data-vitrine-tam]")?.addEventListener("click", (ev) => {
        const b = ev.currentTarget, grande = b.getAttribute("aria-pressed") !== "true";
        b.setAttribute("aria-pressed", String(grande));
        el.classList.toggle("pt-vitrine-2x", grande);
        // o acabamento se refaz no próximo ciclo da página, no tamanho novo
        el.querySelectorAll(".rf-vitrine-peca > :not(img:first-child)").forEach((x) => x.remove());
      });
      el.querySelectorAll("[data-pref]").forEach((b) => b.addEventListener("click", () => {
        P.preferir(b.dataset.pref, b.dataset.valor);
        el.querySelectorAll(`[data-pref="${b.dataset.pref}"]`).forEach((x) => x.setAttribute("aria-checked", String(x === b)));
      }));
    }
    const estado = (t, ruim = false) => { const s = el.querySelector(".pt-estado"); if (s) { s.textContent = t; s.classList.toggle("ruim", ruim); } };
    function pendentes() {
      // o que difere dos valores de agora fica marcado (editado, ainda não aplicado)
      el.querySelectorAll("[data-pt], [data-pt-mat]").forEach((i) => {
        const atual = i.dataset.pt ? String(base[i.dataset.pt] ?? "") : String((base.materiais.find((m) => m.id === i.dataset.ptMat) || {}).qtd ?? 0);
        i.classList.toggle("pendente", String(i.value) !== atual);
      });
    }
    function ligar() {
      ligarVisuais();
      const nivel = el.querySelector('[data-pt="nivel"]'), classe = el.querySelector('[data-pt="classe"]'), spec = el.querySelector('[data-pt="spec"]');
      const refazerSpec = () => { spec.innerHTML = opcoesSpec(base, classe.value, +nivel.value, spec.value); pendentes(); };
      nivel.addEventListener("input", refazerSpec);
      classe.addEventListener("change", refazerSpec);
      el.querySelectorAll("input, select").forEach((i) => i.addEventListener("input", pendentes));
      el.querySelector("[data-pt-recarregar]").addEventListener("click", preencher);
      el.querySelectorAll("[data-pt-aplicar]").forEach((b) => b.addEventListener("click", () => {
        const op = b.dataset.ptAplicar;
        const materiais = Object.fromEntries([...el.querySelectorAll("[data-pt-mat]")].map((i) => [i.dataset.ptMat, i.value]));
        const dados = { ouro: el.querySelector('[data-pt="ouro"]').value, materiais };
        if (op === "teste_cenario") Object.assign(dados, { nivel: nivel.value, classe: classe.value, spec: spec.value });
        const motivo = P.aplicarTeste(op, dados);
        if (motivo) { estado(motivo, true); return; }
        estado(op === "teste_cenario" ? "Reiniciando o cenário…" : "Aplicando…");
        esperarNovo();
      }));
    }
    // depois de aplicar, os campos voltam aos valores que o motor confirmou (o aviso do motor diz o resultado)
    function esperarNovo() {
      const antes = JSON.stringify(P.estadoTeste());
      let n = 0;
      const t = setInterval(() => {
        n += 1;
        const agora = P.estadoTeste();
        if (JSON.stringify(agora) !== antes || n > 20) { clearInterval(t); preencher(); estado(JSON.stringify(agora) !== antes ? "Aplicado." : "Nada mudou (veja o aviso).", JSON.stringify(agora) === antes); }
      }, 150);
    }
    botao.addEventListener("click", () => {
      el.hidden = !el.hidden;
      botao.setAttribute("aria-expanded", String(!el.hidden));
      if (!el.hidden) preencher();
    });
    document.addEventListener("keydown", (ev) => { if (ev.key === "Escape" && !el.hidden && el.contains(document.activeElement)) { ev.stopImmediatePropagation(); el.hidden = true; botao.setAttribute("aria-expanded", "false"); botao.focus(); } }, true);
  }

  const estilo = document.createElement("style");
  estilo.textContent = `#faixa-demo { position: fixed; z-index: 90; top: 6px; left: 50%; translate: -50% 0; display: flex; align-items: center;
    gap: 8px; padding: 3px 10px; font: 13px/1.3 var(--texto, sans-serif); color: #cfc6b2; background: #1d1407; border: 1px solid #8a6a2a;
    box-shadow: 0 2px 6px rgba(0,0,0,.6); white-space: nowrap; }
  #faixa-demo strong { color: #f2d27a; letter-spacing: .06em; text-transform: uppercase; font-size: 12px; }
  #faixa-demo button { font: inherit; color: #cfc6b2; background: #2a2116; border: 1px solid #5a4632; padding: 1px 8px; cursor: pointer; }
  #faixa-demo button[aria-pressed="true"] { color: #1d1407; background: #f2d27a; border-color: #f2d27a; }
  #faixa-demo button:focus-visible { outline: 2px solid #f2d27a; outline-offset: 1px; }
  #faixa-demo a { color: #f2d27a; }
  #faixa-demo .faixa-hist { color: #9d978b; }
  #faixa-comparacao { position: fixed; z-index: 90; top: 34px; left: 50%; translate: -50% 0; width: 340px; padding: 8px 12px;
    font: 13px/1.35 var(--texto, sans-serif); color: #cfc6b2; background: #1d1407; border: 1px dashed #8a6a2a; box-shadow: 0 2px 6px rgba(0,0,0,.6); }
  #faixa-comparacao .rf-teste { margin: 0; padding: 0; border: 0; }
  #faixa-comparacao b { color: #f2d27a; }
  #faixa-comparacao p { margin: 2px 0 6px; color: #9d978b; }
  #faixa-comparacao .rf-teste-bloco small { color: #9d978b; }
  #faixa-comparacao .rf-teste-linha { display: flex; justify-content: space-between; gap: 8px; }
  #faixa-comparacao .melhor { color: #9fe07c; } #faixa-comparacao .pior { color: #ff8c78; }
  #painel-testes { position: fixed; z-index: 95; top: 34px; right: 8px; width: 380px; max-height: calc(100vh - 44px); overflow: auto; padding: 8px 12px 10px;
    font: 13px/1.35 var(--texto, sans-serif); color: #cfc6b2; background: #1d1407; border: 1px dashed #8a6a2a; box-shadow: 0 2px 8px rgba(0,0,0,.7); }
  #painel-testes .pt-cab { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }
  #painel-testes .pt-cab b { color: #f2d27a; letter-spacing: .06em; text-transform: uppercase; font-size: 12px; }
  #painel-testes fieldset { margin: 6px 0; padding: 6px 8px 8px; border: 1px solid #5a4632; }
  #painel-testes legend { padding: 0 4px; color: #f2d27a; }
  #painel-testes .pt-linha { display: flex; justify-content: space-between; align-items: center; gap: 8px; margin: 3px 0; }
  #painel-testes input, #painel-testes select { font: inherit; color: #f3ead6; background: #120d06; border: 1px solid #5a4632; padding: 1px 4px; }
  #painel-testes input[type=number] { width: 84px; text-align: right; }
  #painel-testes td input[type=number] { width: 46px; }
  #painel-testes .pendente { border-color: #f2d27a; box-shadow: 0 0 0 1px #f2d27a; }
  #painel-testes table { width: 100%; border-collapse: collapse; margin: 4px 0; }
  #painel-testes th { font-weight: 400; text-align: left; color: #9d978b; } #painel-testes thead th { text-align: center; }
  #painel-testes button { font: inherit; color: #cfc6b2; background: #2a2116; border: 1px solid #5a4632; padding: 2px 8px; cursor: pointer; margin-top: 4px; }
  #painel-testes button.pt-perigo { border-color: #8a3328; color: #ffc9be; }
  #painel-testes button:focus-visible, #painel-testes input:focus-visible, #painel-testes select:focus-visible { outline: 2px solid #f2d27a; outline-offset: 1px; }
  #painel-testes .pt-seg { display: inline-flex; flex-wrap: wrap; justify-content: flex-end; gap: 2px; } #painel-testes .pt-seg button { margin: 0; }
  #painel-testes .pt-seg button[aria-checked="true"] { color: #1d1407; background: #f2d27a; border-color: #f2d27a; }
  #painel-testes .pt-nota { margin: 4px 0 0; color: #9d978b; font-size: 12px; }
  #painel-testes .pt-estado { min-height: 18px; margin: 4px 0 0; color: #9fe07c; } #painel-testes .pt-estado.ruim { color: #ff8c78; }
  #painel-testes .pt-aviso { color: #9d978b; }
  #painel-testes .pt-seg button[aria-pressed="true"] { color: #1d1407; background: #f2d27a; border-color: #f2d27a; }
  #painel-testes .rf-vitrine { margin: 4px 0 2px; padding: 6px; background: #0e0b08; border: 1px solid #3a2c1c; }
  #painel-testes .rf-vitrine-linha { display: grid; grid-template-columns: 48px repeat(5, 48px); align-items: center; justify-items: center; }
  #painel-testes .rf-vitrine-linha > span:first-child { justify-self: start; color: #9d978b; font-size: 12px; }
  #painel-testes .rf-vitrine-linha b { color: #f2d27a; font-size: 12px; font-weight: 400; }
  #painel-testes .rf-vitrine-peca { position: relative; display: block; width: 40px; height: 40px; }
  #painel-testes .rf-vitrine-peca > img:first-child { display: block; width: 40px; height: 40px; image-rendering: pixelated; }
  #painel-testes.pt-vitrine-2x { width: 560px; }
  #painel-testes.pt-vitrine-2x .rf-vitrine-linha { grid-template-columns: 48px repeat(5, 88px); }
  #painel-testes.pt-vitrine-2x .rf-vitrine-peca, #painel-testes.pt-vitrine-2x .rf-vitrine-peca > img:first-child { width: 80px; height: 80px; }`;
  document.head.appendChild(estilo);
})();
