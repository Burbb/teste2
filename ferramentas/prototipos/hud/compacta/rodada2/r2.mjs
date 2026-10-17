// A composição compacta, rodada 2 (protótipo; nada disto entra no jogo): a B aprovada como direção, com o que a
// rodada 1 deixou de fora, e as duas perguntas desta rodada.
//   b   a B da rodada 1 (o seletor sobre a ficha quando não cabe embaixo), CORRIGIDA: a ficha coberta fica inerte
//       (sem clique nem foco por trás), redimensionar acompanha a coluna da ficha, e o seletor sai junto quando a
//       roda é limpa (escolher uma habilidade). Na rodada 1 ele ficava na tela durante a mira: movido para o body,
//       a limpeza da roda não o alcançava.
//   b2  a b com o custo numa linha própria, embaixo do nome, só na coluna da ficha (b2-seletor.css), e o Voltar na
//       linha do título.
//   r   a b2 com o registro na coluna do mundo nas lutas que não deixariam espaço para ele (r-registro.js).
// As trocas procuram o texto exato do jogo (e o da B, de ../compacta.mjs) e param se ele mudou.
import { escolhas as escolhasR1, batalha as batalhaR1 } from "../compacta.mjs";

const LF = (t) => t.split("\r\n").join("\n");
function trocar(texto, trocas, arquivo) {
  return trocas.reduce((t, [a, b]) => {
    if (!t.includes(a)) throw new Error(`${arquivo} mudou: não achei ${a.slice(0, 70)}...`);
    return t.replace(a, b);
  }, LF(texto));
}

const LATERAL = `
// [protótipo B, rodada 2] o seletor sobre a ficha: a ficha coberta não recebe clique nem foco (inert); redimensionar
// acompanha a coluna da ficha (a habilidade examinada e o foco ficam, a fileira com o foco continua à vista); fechar,
// escolher ou limpar a roda devolve a ficha
let lateralAberto = null;
function prenderLateral(j, ficha) {
  ficha.inert = true;
  const seguir = () => {
    if (!j.isConnected) { soltarLateral(); return; }
    if (!ficha.getClientRects().length) { fecharJanela(); return; }  // a coluna da ficha sumiu (janela estreita)
    const f = ficha.getBoundingClientRect();
    j.style.left = Math.round(f.left) + "px"; j.style.top = Math.round(f.top) + "px";
    j.style.width = Math.round(f.width) + "px"; j.style.maxHeight = j.style.minHeight = Math.round(f.height) + "px";
    const a = document.activeElement, L = j.querySelector(".rj-lista");
    if (a && j.contains(a) && a.closest(".rj-linha") && L) {
      const r = a.getBoundingClientRect(), lr = L.getBoundingClientRect();
      if (r.top < lr.top) L.scrollTop -= lr.top - r.top; else if (r.bottom > lr.bottom) L.scrollTop += r.bottom - lr.bottom;
    }
  };
  addEventListener("resize", seguir);
  lateralAberto = { j, ficha, seguir };
}
function soltarLateral() {
  if (!lateralAberto) return;
  const { j, ficha, seguir } = lateralAberto;
  lateralAberto = null;
  ficha.inert = false;
  removeEventListener("resize", seguir);
  if (j.isConnected) j.remove();
}
`;

const ESCOLHAS = [
  // logo depois da ficha (e não no fim da página): o Tab segue do seletor para a arena, como o seletor embaixo
  ['    document.body.appendChild(j);\n', '    ficha.after(j);\n'],
  ['    j.style.width = Math.round(f.width) + "px"; j.style.maxHeight = Math.round(f.height) + "px";\n  }\n',
    '    j.style.width = Math.round(f.width) + "px"; j.style.maxHeight = Math.round(f.height) + "px";\n    prenderLateral(j, ficha);\n  }\n'],
  ['    j.remove();\n    ancora.classList.remove("ativo");', '    j.remove();\n    soltarLateral();\n    ancora.classList.remove("ativo");'],
  ['  if (r && r.childElementCount) { Telas.esconderDica(); r.replaceChildren(); }',
    '  soltarLateral();\n  if (r && r.childElementCount) { Telas.esconderDica(); r.replaceChildren(); }'],
];

// b2: na coluna da ficha, o "Esc · Voltar" sobe para a linha do título (como a produção já faz na janela baixa), e a
// descrição ganha a altura dele
const VOLTAR_NO_TITULO = [['    prenderLateral(j, ficha);\n',
  '    prenderLateral(j, ficha);\n    j.querySelector(".rj-titulo").appendChild(j.querySelector(".rj-voltar"));\n'],
  // a descrição entra antes do Voltar, se ele ainda estiver embaixo; no título, ela vai para o fim
  ['  j.insertBefore(zona, j.querySelector(".rj-voltar"));', '  j.insertBefore(zona, j.querySelector(":scope > .rj-voltar"));']];

export const VERSOES = { b: { r1: "b", css: ["../b-seletor.css"], js: [] },
  b2: { r1: "b", css: ["../b-seletor.css", "b2-seletor.css"], js: [] },
  r: { r1: "b", css: ["../b-seletor.css", "b2-seletor.css", "r-registro.css"], js: ["r-registro.js"] } };
export const escolhas = (js, v) => (v === "producao" ? js
  : trocar(escolhasR1(js, VERSOES[v].r1), v === "b" ? ESCOLHAS : [...ESCOLHAS, ...VOLTAR_NO_TITULO], "escolhas.js (B)") + LATERAL);
export const batalha = (js, v) => (v === "producao" ? js : batalhaR1(js, VERSOES[v].r1));
