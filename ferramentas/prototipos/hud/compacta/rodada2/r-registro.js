// [protótipo R, rodada 2] O registro na coluna do mundo nas lutas que não deixariam espaço para ele.
// No começo de cada luta, uma vez: se a coluna mais alta da arena, com uma linha de efeitos em cada carta (o que o
// motor produz de verdade num bando de caídos com uma Maldição ou um Grito, efeitos-reais.json), deixasse menos de
// MINIMO px para o registro embaixo, o registro (#cena) passa para a coluna do mundo, embaixo do nome do lugar, da
// região, do nível e dos avisos da noite, por cima do minimapa, da missão e dos caminhos (que não servem durante a
// luta e voltam quando ela acaba). A decisão vale até o fim da luta: o registro não troca de lugar no meio dela, e as
// cartas não se mexem por causa dele. Sem a coluna do mundo à vista (janelas abaixo de 1100 px), nada muda.
(() => {
  const MINIMO = 140;   // ~5 linhas do registro
  const LINHA_EF = 28;  // a linha de efeitos de uma carta (03-batalha.css: margem, fio, ícone de 16 px com a borda)
  let decidido = false, ativo = false, fora = null;
  const $ = (s) => document.querySelector(s);
  function projetar() {
    const arena = $("#arena"), cena = $("#cena");
    if (!arena || !cena) return false;
    const crescer = (col) => (col ? [...col.querySelectorAll(".carta")].filter((c) => !c.querySelector(".carta-efeitos .ef")).length * LINHA_EF : 0);
    // numa coluna só, cada carta sem efeitos ganharia uma linha; em duas colunas (1920), metade disso
    const ini = $("#batalha .inimigos"), al = $("#batalha .aliados");
    const duas = ini && getComputedStyle(ini).gridTemplateColumns.split(" ").length > 1;
    const cresce = Math.max(crescer(al), duas ? crescer(ini) / 2 : crescer(ini));
    return cena.getBoundingClientRect().height - cresce < MINIMO;
  }
  function colocar() {
    const mundo = $("#mundo"), cena = $("#cena"), mapa = $("#mapa-mini");
    if (!mundo || !cena || !mundo.getClientRects().length) return false;
    const m = mundo.getBoundingClientRect(), topo = Math.round((mapa ? mapa.getBoundingClientRect().top : m.top + 220) - 4);
    Object.assign(cena.style, { position: "fixed", left: Math.round(m.left) + "px", top: topo + "px", width: Math.round(m.width) + "px",
      height: Math.round(m.bottom - topo) + "px", maxWidth: "none", zIndex: 6 });
    // o que fica por baixo (minimapa, missão, caminhos) não recebe clique nem foco enquanto o registro está ali
    [...mundo.children].filter((e) => e.getBoundingClientRect().bottom > topo + 1).forEach((e) => { e.inert = true; });
    return true;
  }
  function ligar() {
    if (!colocar()) return;
    ativo = true;
    document.body.classList.add("registro-no-mundo");
    fora = new MutationObserver(() => { if (ativo) colocar(); });  // o painel do mundo é redesenhado a cada estado
    fora.observe($("#mundo"), { childList: true });
    addEventListener("resize", colocar);
  }
  function desligar() {
    ativo = false;
    if (fora) fora.disconnect();
    removeEventListener("resize", colocar);
    document.body.classList.remove("registro-no-mundo");
    const cena = $("#cena");
    if (cena) ["position", "left", "top", "width", "height", "maxWidth", "zIndex"].forEach((k) => { cena.style[k] = ""; });
    $("#mundo") && [...$("#mundo").children].forEach((e) => { e.inert = false; });
  }
  new MutationObserver(() => {
    const emLuta = document.body.classList.contains("em-combate");
    if (!emLuta) { decidido = false; if (ativo) desligar(); return; }
    if (decidido || !$("#batalha .carta")) return;
    decidido = true;
    if (projetar()) ligar();
  }).observe(document.body, { attributes: true, attributeFilter: ["class"], childList: false, subtree: false });
  // a primeira carta pode chegar depois da classe: confere também quando a arena muda
  const tentar = () => { if (document.body.classList.contains("em-combate") && !decidido && $("#batalha .carta")) { decidido = true; if (projetar()) ligar(); } };
  new MutationObserver(tentar).observe(document.getElementById("batalha") || document.body, { childList: true, subtree: true });
  tentar();
})();
