/* Fogueira: a tela do acampamento. A cena (o lugar, o fogo e a roda) é desenhada na arte do topo, como as salas da
   capela (telas/acampamento.js); embaixo ficam só a frase da chegada, a instrução e quem vai e quem fica. Por cima da
   arte, numa camada como a dos pontos da capela, cada companheiro (e o animal) é um ponto clicável com o mesmo menu de
   sempre (Telas.ligarFigurasComitiva), e o "Dormir até o amanhecer" fica no canto de cima. O nome de cada um aparece
   com o mouse, com o foco do teclado ou com "Destacar interações" (F4), junto do contorno dourado na arte. */
"use strict";

(() => {
  const { h, S, ligarFigurasComitiva } = Telas;

  function acampamento(d) {
    const figuras = d.ativos.length + d.reserva.length;
    return `<div class="tela acampamento">${d.intro ? `<p class="sussurro">${h(d.intro)}</p>` : ""}
      ${figuras ? rodape(d) : '<div class="dica-uso">Só você, o fogo e os barulhos da mata. Quem você encontrar pelo caminho pode se sentar aqui um dia.</div>'}</div>`;
  }

  /** Embaixo da cena, cada coisa no seu lugar: a instrução e o contador numa linha; quem vai com você e quem fica no
   *  acampamento, por escrito, com o estado de cada um e o ✉ de quem quer conversar (na cena, o nome só aparece com o
   *  mouse, o foco ou o F4). O que muda para quem fica vai no menu de cada um, junto do "Deixar no acampamento". */
  function rodape(d) {
    const quem = (m) => `<span class="fr-nome">${h(m.nome.split(" ").pop())}${m.conversa ? ' <i class="fr-carta" title="Quer conversar">✉</i>' : ""}${m.ferido_txt ? ` <small>(${h(m.ferido_txt)})</small>` : ""}${m.fora ? ` <small>(${h(m.fora.curto)})</small>` : ""}</span>`;
    const lista = (ms) => ms.length ? ms.map(quem).join(", ") : '<span class="fr-ninguem">ninguém</span>';
    return `<div class="fogueira-rodape">
        <div class="fr-cab"><span class="fr-instrucao">Clique num companheiro para conversar ou ajustar a comitiva.</span><span class="fr-contador">${h(d.contador)}</span></div>
        <div class="fr-linha vai"><b>Vai com você:</b> ${lista(d.ativos)}</div>
        ${d.reserva.length ? `<div class="fr-linha fica"><b>No acampamento:</b> ${lista(d.reserva)}</div>` : ""}
      </div>`;
  }

  // ---------------------------------------------------------------- a cena no topo e os pontos por cima
  let atual = null;  // { d, pontos, capa }: o acampamento à vista

  /** Os pontos: um botão por companheiro (e o animal), na área do desenho dele, com o nome (escondido até o mouse, o
   *  foco ou o F4); o Dormir no canto. */
  function capaDe(d, pontos) {
    const capa = document.createElement("div");
    capa.id = "acampamento-pontos";
    capa.setAttribute("role", "group");
    capa.setAttribute("aria-label", "A roda em volta do fogo");
    const quem = [...d.ativos.map((m) => ({ ...m, onde: "ativo" })), ...d.reserva.map((m) => ({ ...m, onde: "reserva" }))];
    capa.innerHTML = pontos.map((p) => {
      if (p.id === "fera") {
        const nome = h(d.fera.nome.split(" ").pop());
        return `<span class="figura fera" role="button" tabindex="0" data-fera="1" data-ponto="fera" aria-label="${nome}: carinho e cuidados"><span class="ac-nome">${nome}</span></span>`;
      }
      const m = quem.find((x) => x.id === p.id), nome = h(m.nome.split(" ").pop());
      const onde = m.onde === "ativo" ? "vai com você" : "fica no acampamento";
      return `<button type="button" class="figura ${m.onde}${m.conversa ? " tem-conversa" : ""}" data-cid="${h(m.id)}" data-ponto="${h(m.id)}"
        aria-label="${nome}, ${onde}${m.conversa ? ", quer conversar" : ""}"><span class="ac-nome">${nome}${m.conversa ? '<i class="carta-aviso">✉</i>' : ""}</span></button>`;
    }).join("") + `<button type="button" class="dormir-barraca">${S("lua", 1)} Dormir até o amanhecer</button>`;
    // o destaque na arte: o contorno de quem está sob o mouse ou o foco do teclado (o foco que o mouse deixa não acende)
    capa.querySelectorAll("[data-ponto]").forEach((el) => {
      const acender = (sim) => Vista.destacar(sim ? el.dataset.ponto : null);
      el.addEventListener("mouseenter", () => acender(true));
      el.addEventListener("focus", () => acender(el.matches(":focus-visible")));
      el.addEventListener("mouseleave", () => acender(el.matches(":focus-visible")));
      el.addEventListener("blur", () => acender(el.matches(":hover")));
    });
    return capa;
  }

  /** Onde cada ponto cai na tela: a caixa da arte (Vista.caixaDaArte), a mesma conta do desenho, refeita a cada mudança
   *  de tamanho (inclusive durante a animação da altura); os nomes se acomodam de novo. */
  function posicionar() {
    if (!atual || !atual.capa.isConnected) return;
    const q = Vista.caixaDaArte();
    if (!q) return;
    const capa = atual.capa;
    Object.assign(capa.style, { left: q.esq + "px", top: q.topo + "px", width: q.larg + "px", height: q.alt + "px" });
    atual.pontos.forEach((p) => {
      const el = capa.querySelector(`[data-ponto="${p.id}"]`), [x, y, w, hh] = p.area;
      if (el) Object.assign(el.style, { left: q.dx + x * q.ex + "px", top: q.dy + y * q.ey + "px", width: w * q.ex + "px", height: hh * q.ey + "px" });
    });
    acomodarNomes(capa, q);
  }
  Vista.aoRedimensionar(posicionar);

  /** O nome de cada um onde couber, como se todos aparecessem juntos (com F4 é o que acontece): acima da cabeça, ao
   *  lado ou embaixo, sem cobrir outro nome, outra figura (o rosto de ninguém), o fogo nem o Dormir, e dentro da arte.
   *  Acima e no meio, o balão aponta para a figura; nos outros lugares, fica sem o bico. */
  function acomodarNomes(capa, q) {
    const P = capa.getBoundingClientRect();
    const ret = (x, y, w, hh) => ({ l: x, t: y, r: x + w, b: y + hh });
    const daArte = (x, y, w, hh) => ret(q.dx + x * q.ex, q.dy + y * q.ey, w * q.ex, hh * q.ey);
    const relativo = (r) => ret(r.left - P.left, r.top - P.top, r.width, r.height);
    const area = (a, b) => Math.max(0, Math.min(a.r, b.r) - Math.max(a.l, b.l)) * Math.max(0, Math.min(a.b, b.b) - Math.max(a.t, b.t));
    const figuras = [...capa.querySelectorAll("[data-ponto]")];
    const [hx, hy] = Acampamento.HEROI, [fx, fy] = Acampamento.FOGO;
    const obstaculos = [daArte(hx - 8, hy - 17, 16, 19), daArte(fx - 14, fy - 22, 28, 26), ...figuras.map((f) => relativo(f.getBoundingClientRect()))];
    const dormir = capa.querySelector(".dormir-barraca");
    if (dormir) obstaculos.push(relativo(dormir.getBoundingClientRect()));
    figuras.forEach((f) => {
      const nome = f.querySelector(".ac-nome");
      if (!nome) return;
      nome.classList.add("com-bico");  // o tamanho do bico vem do CSS (a escala do pixel da interface)
      const bico = parseFloat(getComputedStyle(nome, "::after").height) || 8;
      const s = relativo(f.getBoundingClientRect()), w = nome.offsetWidth, hh = nome.offsetHeight, cx = (s.l + s.r) / 2;
      const opcoes = [
        [ret(cx - w / 2, s.t - hh - bico, w, hh), true],      // acima da cabeça, com o bico
        [ret(cx - w / 4, s.t - hh - 2, w, hh), false],        // acima, puxado para a direita
        [ret(cx - (3 * w) / 4, s.t - hh - 2, w, hh), false],  // acima, puxado para a esquerda
        [ret(s.r + 2, s.t + 2, w, hh), false],                // à direita
        [ret(s.l - w - 2, s.t + 2, w, hh), false],            // à esquerda
        [ret(cx - w / 2, s.b + 1, w, hh), false],             // embaixo
      ];
      const dentro = (c) => c.l >= 2 && c.t >= 2 && c.r <= P.width - 2 && c.b <= P.height - 2;
      const custo = (c) => (dentro(c) ? 0 : 1e6) + obstaculos.reduce((n, o) => n + (o === s ? 0 : area(c, o)), 0);
      const [livre, comBico] = opcoes.find(([c]) => custo(c) === 0) || opcoes.reduce((m, o) => (custo(o[0]) < custo(m[0]) ? o : m));
      nome.classList.toggle("com-bico", comBico);
      nome.style.left = livre.l - s.l + "px";
      nome.style.top = livre.t - s.t + "px";
      obstaculos.push(livre);
    });
  }

  /** O acampamento vai para o topo: a arte troca a paisagem pela cena, a barra de título das telas de menu sai (o chão
   *  da cena desce em pontilhado direto até a leitura, como na capela) e os pontos ficam por cima. Redesenhar a tela (o
   *  carinho, trocar quem vai) monta de novo com o que o motor mandou. */
  function mostrar(d) {
    const cena = document.getElementById("cena"), pagina = document.getElementById("pagina");
    const heroi = App.estado && App.estado.heroi ? App.estado.heroi.classe : null;
    const e = App.estado && App.estado.mundo ? App.estado : { mundo: { periodo_n: 3, clima_id: "limpo" } };
    const m = Acampamento.montar(e, d, heroi);
    if (atual) atual.capa.remove();
    const capa = capaDe(d, m.pontos);
    atual = { d, pontos: m.pontos, capa };
    cena.classList.add("acampando", "com-ambiente");
    cena.classList.remove("recolhido");
    cena.insertBefore(capa, pagina);  // antes da página: o Tab passa pela roda e pelo Dormir antes das opções
    Vista.usarAmbiente({ base: m.base, foco: null, desenhar: (ctx, quadro, destaque) => m.desenhar(ctx, quadro, destaque) });
    ligarFigurasComitiva(capa, d);
    posicionar();
    requestAnimationFrame(posicionar);  // a arte acabou de aparecer: a caixa dela muda no quadro seguinte
  }
  /** Saiu da fogueira (dormiu, foi a outra tela): a paisagem volta ao topo, com a barra das telas de menu. */
  function sair() {
    if (!atual) return;
    atual.capa.remove();
    atual = null;
    const cena = document.getElementById("cena");
    cena.classList.remove("acampando");
    if (!(window.Cenas && Cenas.atual())) { cena.classList.remove("com-ambiente"); Vista.usarAmbiente(null); }
  }
  // A tela da fogueira saiu do texto e não voltou logo (o redesenho dela volta no mesmo instante): o acampamento sai.
  let conferir = null;
  new MutationObserver(() => {
    if (!atual || conferir) return;
    conferir = setTimeout(() => { conferir = null; if (!document.querySelector("#texto .tela.acampamento")) sair(); }, 150);
  }).observe(document.getElementById("texto"), { childList: true });

  Telas.registrar("acampamento", acampamento, {
    ligar: (raiz, d) => {
      App.ultimaFogueira = d;
      mostrar(d);
    },
  });
})();
