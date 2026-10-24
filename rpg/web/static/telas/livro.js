/* Um livro aberto para ler (1.204.0): as duas páginas de um documento escrito por alguém do mundo, por cima da cena.
   O motor manda abrir (a celebração "livro") com o título, as páginas e o acabamento do documento; a tela só desenha.
   Fechar (o botão, Esc, Enter, espaço ou o véu em volta) devolve a cena e deixa o texto seguir; nada pede ler até o
   fim. Recarregando, não abre de novo.

   O livro é a base aprovada dos livros do jogo (a "A refinada" de ferramentas/prototipos/hud/livro-capela/): o couro
   e as folhas em pixel art (livros/<acabamento>.png, escala 3), a letra Fondamento (fontes/OFL-Fondamento.txt), a
   pauta desenhada pelo próprio bloco de texto (22-livro.css, .livro-regua) e o texto descendo até a linha de base
   cair nela, pela métrica da fonte (medirTopo): qualquer texto, qualquer quebra; um texto maior que a página rola com
   a pauta junto. A página da esquerda tem a primeira entrada; a da direita, as outras, depois de um traço de pena.

   Os acabamentos (o documento escolhe o dele; não há escolha do jogador):
   - "base": o livro limpo, o padrão;
   - "capela": o registro da sacristia depois de anos na capela alagada (os rasgos, a água, o bolor, o couro gasto).
     A máscara de cada página (livros/capela-mascara-<lado>.png) tira a pauta e a tinta onde falta papel e as desbota
     sob o bolor e a água; ela é do bloco que rola, então o dano fica preso à página. Um texto novo neste livro pede a
     conferência dos rasgos (ferramentas/prototipos/hud/livro-capela/auxiliares/dano.mjs). */
"use strict";

(() => {
  const { h } = Telas;
  const ESCALA = 3, PASSO = 33, PAUTA = 30;  // a escala do desenho; a linha (11 px do desenho) e a primeira pauta
  // as páginas em coordenadas do desenho: a caixa da pauta e onde a escrita começa e termina (desenhar_livro.py)
  const REGUAS = { esquerda: { caixa: [14, 15, 137, 147], texto: [22, 133] }, direita: { caixa: [149, 15, 273, 147], texto: [155, 265] } };
  const ACABAMENTOS = {
    base: { imagem: "livros/base.png", tamanho: [290, 170] },
    capela: { imagem: "livros/capela.png", tamanho: [290, 170],
      mascaras: { esquerda: "livros/capela-mascara-esquerda.png", direita: "livros/capela-mascara-direita.png" } },
  };

  // o quanto o texto desce para a linha de base da Fondamento cair na pauta (a métrica da fonte, medida uma vez)
  let topo = null;
  function medirTopo() {
    if (topo !== null) return topo;
    const t = document.createElement("div");
    t.className = "livro-pagina livro-regua livro-sonda";
    t.innerHTML = '<div class="livro-texto"><p>Ág<span style="display:inline-block;width:0;height:0"></span></p></div>';
    document.body.appendChild(t);
    const linha = t.querySelector("p").getBoundingClientRect().top, base = t.querySelector("span").getBoundingClientRect().bottom;
    t.remove();
    topo = Math.round(PAUTA - (base - linha));
    return topo;
  }

  const pars = (t) => t.split("\n\n").map((x) => `<p>${h(x)}</p>`).join("");
  function pagina(lado, n, texto, mascara) {
    const { caixa: [x0, y0, x1, y1], texto: [t0, t1] } = REGUAS[lado];
    const m = mascara ? `;--mascara:url('/static/${mascara}')` : "";
    return `<div class="livro-pagina livro-regua livro-entrada${n}${mascara ? " livro-mascarada" : ""}" style="left:${x0 * ESCALA}px;top:${y0 * ESCALA}px;width:${(x1 - x0) * ESCALA}px;height:${(y1 - y0) * ESCALA}px${m}">
      <div class="livro-texto" style="--esq:${(t0 - x0) * ESCALA}px;padding:${medirTopo() + (n === 2 ? PASSO : 0)}px ${(x1 - t1) * ESCALA}px 0 var(--esq)">${texto}</div></div>`;
  }

  let sobre = null, aoFechar = null;
  function montar() {
    if (sobre) return;
    sobre = document.createElement("div");
    sobre.id = "sobre-leitura"; sobre.className = "sobreposicao livro"; sobre.hidden = true;
    sobre.setAttribute("role", "dialog"); sobre.setAttribute("aria-modal", "true");
    sobre.addEventListener("click", (ev) => { if (ev.target === sobre) fecharLivro(); });
    // um clique fora do botão (no véu, na página) não tira o foco do livro: o teclado continua no Fechar
    sobre.addEventListener("mousedown", (ev) => { if (!ev.target.closest("button")) ev.preventDefault(); });
    document.body.appendChild(sobre);
  }

  /** Com o livro aberto, as teclas são dele: Esc, Enter e espaço fecham; as outras não escolhem nada embaixo. */
  function tecla(ev) {
    if (!sobre || sobre.hidden) return;
    if (["Escape", "Enter", " "].includes(ev.key)) { ev.preventDefault(); ev.stopPropagation(); fecharLivro(); return; }
    if (ev.key === "Tab") { ev.preventDefault(); return; }  // um só controle: o foco fica nele
    if (!["F4", "F1"].includes(ev.key)) ev.stopPropagation();
  }

  function fecharLivro() {
    if (!sobre || sobre.hidden) return false;
    sobre.hidden = true;
    document.removeEventListener("keydown", tecla, true);
    const fim = aoFechar; aoFechar = null;
    if (fim) fim();  // o texto segue (o Continuar da leitura)
    return true;
  }

  async function lerLivro(d, instantaneo) {
    if (instantaneo || !d || !d.paginas) return;
    await document.fonts.load('21px "Fondamento"');
    montar();
    const a = ACABAMENTOS[d.acabamento] || ACABAMENTOS.base, ms = a.mascaras || {};
    const [p1, ...resto] = d.paginas;
    sobre.setAttribute("aria-label", d.titulo);
    sobre.innerHTML = `<div class="livro-quadro">
      <div class="livro-rotulo">${h(d.titulo)}</div>
      <div class="livro-livro" style="width:${a.tamanho[0] * ESCALA}px;height:${a.tamanho[1] * ESCALA}px;background-image:url('/static/${a.imagem}')">
        ${pagina("esquerda", 1, pars(p1), ms.esquerda)}${pagina("direita", 2, resto.map(pars).join(""), ms.direita)}</div>
      <button class="continuar livro-fechar" type="button">Fechar <kbd>Esc</kbd></button></div>`;
    sobre.querySelector(".livro-fechar").addEventListener("click", () => fecharLivro());
    sobre.hidden = false;
    document.addEventListener("keydown", tecla, true);
    sobre.querySelector(".livro-fechar").focus({ focusVisible: false });
    await new Promise((r) => { aoFechar = r; });
  }

  Object.assign(Telas, { lerLivro, fecharLivro });
})();
