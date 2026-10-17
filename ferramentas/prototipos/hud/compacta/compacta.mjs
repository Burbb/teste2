// A composição compacta das lutas cheias (protótipo; nada disto entra no jogo): as trocas no escolhas.js e no
// batalha.js da página da foto, para as duas alternativas. Cada troca procura o texto exato do jogo e para se ele mudou.
// O checkout do Windows traz CRLF: tudo é comparado em LF.
//   A "arena compacta": a partir de 5 cartas num lado, a arena fica compacta (a-arena.css: os efeitos na linha do nome,
//     o espaço entre as cartas menor) e, se as duas colunas do seletor não couberem embaixo, ele abre em três.
//   B "seletor na ficha": a arena e as cartas como estão; quando o seletor não cabe inteiro embaixo da arena (a lista
//     toda e uma descrição legível), ele abre sobre a coluna da ficha do herói, numa coluna só (b-seletor.css).
const LF = (t) => t.split("\r\n").join("\n");
function trocar(texto, trocas, arquivo) {
  return trocas.reduce((t, [a, b]) => {
    if (!t.includes(a)) throw new Error(`${arquivo} mudou: não achei ${a.slice(0, 70)}...`);
    return t.replace(a, b);
  }, LF(texto));
}

// o seletor: quanto ele precisa (o título, a lista inteira, a descrição mínima de 60 px que o seletor já aceita, o
// Voltar) contra o que sobra embaixo. Onde a produção já mostra a lista inteira (as lutas pequenas), nada muda.
const MEDIR = `  const precisaInteiro = j.querySelector(".rj-titulo").offsetHeight + lista.scrollHeight + 60 + 44;
  const cabeEmbaixo = precisaInteiro <= parseFloat(j.style.maxHeight);
`;
const TECLADO = [
  '  const bs = [...j.querySelectorAll(".rj-linha")], n = bs.length, filas = Math.ceil(n / 2);',
  '  const bs = [...j.querySelectorAll(".rj-linha")], n = bs.length, filas = Number(j.querySelector(".rj-lista").style.getPropertyValue("--filas")) || Math.ceil(n / 2);',
];

const ESCOLHAS = {
  a: [
    ['  j.style.maxHeight = Math.max(170, innerHeight - topoTela - g.H - 14) + "px";\n',
      `  j.style.maxHeight = Math.max(170, innerHeight - topoTela - g.H - 14) + "px";
  // [protótipo A] na arena compacta, se as duas colunas não couberem embaixo, a lista abre em três
${MEDIR}  if (!cabeEmbaixo && document.getElementById("arena").classList.contains("compacta") && linhas.length > 4) {
    j.classList.add("tres");
    const f3 = Math.ceil(linhas.length / 3);
    lista.style.setProperty("--filas", f3);
    [...lista.children].forEach((li, k) => li.style.setProperty("--fila", k % f3));
  }
`],
    ['  const esq = coluna(lis[0]), dir = n > 1 ? coluna(lis[filas] || lis[n - 1]) : esq;',
      '  const tres = j.classList.contains("tres");  // [protótipo A] três colunas: a descrição embaixo de todas\n  const esq = coluna(lis[0]), dir = n > 1 ? coluna(tres ? lis[n - 1] : lis[filas] || lis[n - 1]) : esq;'],
    ['  if (alt > livre) {\n    modo = "junto";', '  if (alt > livre || tres) {\n    modo = "junto";'],
    TECLADO,
  ],
  b: [
    ['  j.style.maxHeight = Math.max(170, innerHeight - topoTela - g.H - 14) + "px";\n',
      `  j.style.maxHeight = Math.max(170, innerHeight - topoTela - g.H - 14) + "px";
  // [protótipo B] o seletor que não cabe inteiro embaixo da arena abre sobre a coluna da ficha do herói, numa coluna
${MEDIR}  const ficha = document.getElementById("heroi");
  if (!cabeEmbaixo && ficha && ficha.offsetParent) {
    const f = ficha.getBoundingClientRect();
    j.classList.add("lateral");
    document.body.appendChild(j);
    lista.style.setProperty("--filas", linhas.length);
    [...lista.children].forEach((li) => li.style.setProperty("--fila", 0));
    j.style.left = Math.round(f.left) + "px"; j.style.top = Math.round(f.top) + "px";
    j.style.width = Math.round(f.width) + "px"; j.style.maxHeight = Math.round(f.height) + "px";
  }
`],
    // na coluna da ficha a descrição fica sempre embaixo da lista (o arranjo "junto" põe o título ao lado do texto,
    // pensado para a largura da arena: na ficha, espremia o texto numa tira); se for longa, rola dentro, como já faz
    ['  if (alt > livre) {\n    modo = "junto";', '  if (alt > livre && !j.classList.contains("lateral")) {\n    modo = "junto";'],
    ['  descricoes(j, linhas, lista);\n  faixasTeclado(j, linhas);\n  bordaLimpa(j);\n',
      '  descricoes(j, linhas, lista);\n  faixasTeclado(j, linhas);\n  // [protótipo B] ao lado, o seletor cobre a ficha inteira e não encosta no registro\n  if (j.classList.contains("lateral")) j.style.minHeight = j.style.maxHeight; else bordaLimpa(j);\n'],
    TECLADO,
  ],
};
const BATALHA = {
  a: [
    ['    colInimigos.style.setProperty("--coluna", Math.max(150, Math.min(COLUNA, Math.floor(livre))) + "px");\n',
      `    colInimigos.style.setProperty("--coluna", Math.max(150, Math.min(COLUNA, Math.floor(livre))) + "px");
    // [protótipo A] a partir de 5 cartas num lado, a arena compacta (e fica assim até o fim da luta)
    if (Math.max(colAliados.children.length, n) >= 5) arena.classList.add("compacta");
`],
    ['      colunasInimigos = 1; linhasInimigos = 0;\n', '      colunasInimigos = 1; linhasInimigos = 0;\n      if (arena) arena.classList.remove("compacta");\n'],
  ],
  b: [],
};
export const escolhas = (js, v) => trocar(js, ESCOLHAS[v], "escolhas.js");
export const batalha = (js, v) => trocar(js, BATALHA[v], "batalha.js");
export const FOLHAS = { a: ["a-arena.css"], b: ["b-seletor.css"] };
