// O livro da capela, as três propostas (protótipo, 24/10/2026; nada no jogo). Entra na página só pela demonstração
// (auxiliares/cenarios_livro.py), depois de telas/cenas.js, e troca Telas.lerLivro: o motor manda a celebração "livro"
// com o título e as páginas de sempre (LIVRO_DA_CAPELA), e daqui sai só a apresentação. As pistas, a releitura, o
// Continuar depois de fechar e o texto continuam os do jogo.
//
//   LivroProto.usar("a")   A · o registro: as duas páginas pautadas, a segunda entrada em outra tinta e outro começo
//   LivroProto.usar("b")   B · o registro que vira confissão: a segunda entrada na mesma mão, mais depressa
//   LivroProto.usar("c")   C · a leitura próxima: uma página, uma entrada por vez, Anterior e Próxima
//
// O texto é da página (HTML), nunca da imagem: a imagem é só o livro (desenhar_livro.py, escala 3).
(() => {
  const BASE = "/static/prototipo-livro/";
  const ESCALA = 3;
  let areas = null, versao = "a";
  const pronto = fetch(BASE + "propostas/areas.json").then((r) => r.json()).then((a) => { areas = a; });

  const h = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const pars = (t) => t.split("\n\n").map((x) => `<p>${h(x)}</p>`).join("");

  // B: a mão da segunda entrada oscila um pouco por palavra (meio pixel para cima ou para baixo), sempre igual: uma
  // sequência fixa, não um sorteio a cada abertura. Nenhuma letra entorta sozinha.
  const OSCILA = [0, -0.5, 0.5, 0, 1, -0.5, 0, 0.5, -1, 0, 0.5, 0, -0.5, 1, 0, -0.5];
  const maoApressada = (t) => t.split("\n\n").map((x, j) => {
    let i = j * 5;
    const palavras = x.split(" ").map((p) => `<span style="--y:${OSCILA[i++ % OSCILA.length]}px">${h(p)}</span>`);
    return `<p>${palavras.join(" ")}</p>`;
  }).join("");

  function caixa(area, ex = {}) {
    const [x0, y0, x1, y1] = area;
    const s = ESCALA;
    return `left:${x0 * s + (ex.l || 0)}px;top:${y0 * s + (ex.t || 0)}px;width:${(x1 - x0) * s + (ex.w || 0)}px;height:${(y1 - y0) * s + (ex.h || 0)}px`;
  }

  // ---------------------------------------------------------------- a sobreposição (a mesma para as três)
  let sobre = null, aoFechar = null, entrada = 0, ler = null;
  function montar() {
    if (sobre) return;
    sobre = document.createElement("div");
    sobre.id = "sobre-leitura"; sobre.className = "sobreposicao lv"; sobre.hidden = true;
    sobre.setAttribute("role", "dialog"); sobre.setAttribute("aria-modal", "true");
    // A e B fecham no véu, como hoje; C não (um clique que erra o Anterior ou o Próxima não fecha o livro). Em
    // nenhuma o clique chega ao jogo: a sobreposição cobre a tela inteira.
    sobre.addEventListener("click", (ev) => { if (ev.target === sobre && versao !== "c") fechar(); });
    // um clique fora dos botões (no véu, na página) não tira o foco do livro: o teclado continua onde estava
    sobre.addEventListener("mousedown", (ev) => { if (!ev.target.closest("button")) ev.preventDefault(); });
    document.body.appendChild(sobre);
  }

  function desenhar(foco) {
    const [p1, p2] = ler.paginas;
    const a = areas[versao === "c" ? (entrada ? "c2" : "c1") : versao];
    const [W, H] = a.tamanho;
    const img = versao === "c" ? `livro-c-${entrada + 1}.png` : `livro-${versao}.png`;
    let paginas;
    if (versao === "c") {
      const t = entrada ? p2 : p1;
      paginas = `<div class="lv-pagina lv-entrada${entrada + 1}" style="${caixa(a.paginas.direita)}" aria-live="polite">
        ${entrada ? maoApressada(t) : pars(t)}</div>`;
    } else {
      const ajuste = versao === "a" ? { t: (a.pauta.primeira - a.paginas.esquerda[1]) * ESCALA - 25 } : {};
      paginas = `<div class="lv-pagina lv-entrada1" style="${caixa(a.paginas.esquerda, ajuste)}">${pars(p1)}</div>
        <div class="lv-pagina lv-entrada2" style="${caixa(a.paginas.direita, versao === "b" ? { w: 12 } : ajuste)}">
        ${versao === "b" ? maoApressada(p2) : pars(p2)}</div>`;
    }
    const nav = versao === "c" ? `<div class="lv-nav">
        <button class="continuar lv-ant" type="button" ${entrada ? "" : "disabled"}><span>◂</span> Anterior</button>
        <span class="lv-conta" aria-live="polite">Entrada ${entrada + 1} de ${ler.paginas.length}</span>
        <button class="continuar lv-prox" type="button" ${entrada < ler.paginas.length - 1 ? "" : "disabled"}>Próxima <span>▸</span></button>
      </div>` : "";
    sobre.className = `sobreposicao lv lv-${versao}`;
    sobre.setAttribute("aria-label", ler.titulo);
    sobre.innerHTML = `<div class="lv-quadro">
      <div class="lv-rotulo">${h(ler.titulo)}</div>
      <div class="lv-livro" style="width:${W * ESCALA}px;height:${H * ESCALA}px;background-image:url('${BASE}propostas/${img}')">${paginas}</div>
      <div class="lv-baixo">${nav}<button class="continuar lv-fechar" type="button">Fechar <kbd>Esc</kbd></button></div>
    </div>`;
    sobre.querySelector(".lv-fechar").addEventListener("click", () => fechar());
    const ant = sobre.querySelector(".lv-ant"), prox = sobre.querySelector(".lv-prox");
    if (ant) ant.addEventListener("click", () => ir(-1));
    if (prox) prox.addEventListener("click", () => ir(+1));
    // o foco: na A e na B, o Fechar (o único controle); na C, o Próxima enquanto houver, depois o Fechar
    const alvo = foco || (prox && !prox.disabled ? prox : sobre.querySelector(".lv-fechar"));
    alvo.focus({ focusVisible: !!sobre.dataset.teclado });
  }

  function ir(passo) {
    const nova = Math.max(0, Math.min(ler.paginas.length - 1, entrada + passo));
    if (nova === entrada) return;
    entrada = nova;
    const voltando = passo < 0;
    desenhar();
    if (voltando && entrada === 0) sobre.querySelector(".lv-prox").focus({ focusVisible: !!sobre.dataset.teclado });
    const pg = sobre.querySelector(".lv-pagina");
    if (!reduzido()) { pg.classList.add(voltando ? "vira-volta" : "vira"); }
  }

  /** As teclas são do livro: Esc fecha; na A e na B, Enter e espaço também (como hoje); na C, as setas e PageUp/
   *  PageDown mudam de entrada, Enter e espaço apertam o botão com o foco. Tab circula só entre os botões do livro. */
  function tecla(ev) {
    if (!sobre || sobre.hidden) return;
    sobre.dataset.teclado = "1";
    const k = ev.key;
    if (k === "Escape") { ev.preventDefault(); ev.stopPropagation(); fechar(); return; }
    if (versao !== "c" && (k === "Enter" || k === " ")) { ev.preventDefault(); ev.stopPropagation(); fechar(); return; }
    if (versao === "c" && ["ArrowRight", "PageDown", "ArrowLeft", "PageUp"].includes(k)) {
      ev.preventDefault(); ev.stopPropagation();
      ir(k === "ArrowRight" || k === "PageDown" ? +1 : -1);
      return;
    }
    if (k === "Tab") {
      const bts = [...sobre.querySelectorAll("button:not([disabled])")];
      const i = bts.indexOf(document.activeElement);
      ev.preventDefault();
      bts[(i + (ev.shiftKey ? -1 : 1) + bts.length) % bts.length].focus({ focusVisible: true });
    }
    if (!["F4", "F1"].includes(k)) ev.stopPropagation();  // as teclas do menu não escolhem nada embaixo do livro
  }

  function fechar() {
    if (!sobre || sobre.hidden) return false;
    sobre.hidden = true;
    document.removeEventListener("keydown", tecla, true);
    const fim = aoFechar; aoFechar = null;
    if (fim) fim();  // o texto segue (o Continuar da leitura), como no jogo
    return true;
  }

  async function lerLivro(d, instantaneo) {
    if (instantaneo || !d || !d.paginas) return;
    await pronto;
    montar();
    ler = d; entrada = 0;
    sobre.dataset.teclado = "";
    sobre.hidden = false;
    if (!reduzido()) { sobre.classList.remove("abre"); void sobre.offsetWidth; }
    desenhar();
    if (!reduzido()) sobre.classList.add("abre");
    document.addEventListener("keydown", tecla, true);
    await new Promise((r) => { aoFechar = r; });
  }

  window.LivroProto = {
    usar(v) { versao = v; Telas.lerLivro = lerLivro; document.documentElement.dataset.livro = v; },
    versao: () => versao,
  };
})();
