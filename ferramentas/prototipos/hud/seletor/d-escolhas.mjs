// Proposta D (faixas de tinta): o que muda no escolhas.js, só na página do protótipo (fotografar_seletor_d.mjs serve
// esta cópia no lugar do arquivo do jogo; o jogo não muda). Só a janelinha de Habilidades vira o seletor de faixas; a
// de Itens fica como no jogo. O que as linhas fazem (escolher, tremer na indisponível, as teclas 1 a 9, a prévia dos
// alvos, a dica, o Esc e o clique fora) é o código do jogo: a proposta mexe na marcação, na posição e no teclado.
//   - a marcação: a tecla, o ícone, o nome (com o motivo da indisponível embaixo) e o custo, cada um no seu elemento
//     (nada de texto em imagem: a tradução troca só o texto); a forma da faixa vem da posição (li.dataset.forma, três
//     formas que se repetem), nunca do acaso, e a ordem de entrada (--i) e a fila na coluna (--fila) vão para o CSS;
//   - sem título de janela nem ×: "Habilidades" pequeno em cima e "Esc · Voltar" embaixo (o mesmo fechar de antes);
//   - a posição: da largura da arena, logo embaixo dela, por cima do registro (a arena e as cartas não se mexem); se
//     não couber, a lista rola dentro; o lugar das texturas da página vai em --fundo-cena e --fundo-palco (a D
//     refinada continua a superfície da página por baixo das faixas);
//   - o teclado: aberta pela tecla, a primeira faixa já chega com o foco; as setas andam pelas faixas (cima e baixo na
//     ordem, lados entre as colunas); o foco também mostra a prévia dos alvos; fechar pelo Esc devolve o foco ao botão;
//   - a dica de uma faixa abre ao lado do painel, não por cima da outra coluna.
const TROCAS = [
  ['  const j = el("div", "roda-janela");\n  j.innerHTML = `<div class="rj-titulo"><span>${esc(titulo)}</span><button type="button" class="rj-fechar" title="Fechar (Esc)">×</button></div>`;',
    `  const j = el("div", "roda-janela");
  const faixas = titulo === "Habilidades";  // [proposta D] o seletor de faixas embaixo da arena
  j.dataset.tipo = faixas ? "habilidades" : "itens";
  j.innerHTML = faixas ? \`<div class="rj-titulo"><span>\${esc(titulo)}</span></div>\`
    : \`<div class="rj-titulo"><span>\${esc(titulo)}</span><button type="button" class="rj-fechar" title="Fechar (Esc)">×</button></div>\`;`],
  ['    b.innerHTML = `<span class="rj-icone">${l.icone}</span><span class="rj-nome">${esc(l.nome)}</span><span class="rj-info">${l.info || ""}</span>${i < 9 ? `<span class="tecla">${i + 1}</span>` : ""}`;',
    `    b.innerHTML = faixas
      ? \`<span class="tecla">\${i < 9 ? i + 1 : ""}</span><span class="rj-icone">\${l.icone}</span><span class="rj-texto"><span class="rj-nome">\${esc(l.nome)}</span>\${l.bloqueio ? \`<span class="rj-motivo">\${esc(l.bloqueio)}</span>\` : ""}</span><span class="rj-info">\${l.info || ""}</span>\`
      : \`<span class="rj-icone">\${l.icone}</span><span class="rj-nome">\${esc(l.nome)}</span><span class="rj-info">\${l.info || ""}</span>\${i < 9 ? \`<span class="tecla">\${i + 1}</span>\` : ""}\`;
    if (faixas) { li.dataset.forma = i % 3; li.style.setProperty("--i", i); }`],
  ['  j.appendChild(lista);\n  roda.appendChild(j);',
    `  j.appendChild(lista);
  if (faixas) {  // duas colunas na ordem das teclas (1, 2, 3 descendo; depois a segunda coluna)
    const filas = Math.ceil(linhas.length / 2);
    lista.style.setProperty("--filas", filas);
    [...lista.children].forEach((li, k) => li.style.setProperty("--fila", k % filas));
    const v = el("button", "rj-fechar rj-voltar", "<kbd>Esc</kbd><span>Voltar</span>");
    v.type = "button";
    v.title = "Fechar (Esc)";
    j.appendChild(v);
  }
  roda.appendChild(j);`],
  [`  const g = geometriaHeroi();
  const x = ancora.offsetLeft - 8;
  j.style.left = Math.max(6, Math.min(x, g.W - j.offsetWidth - 6)) + "px";
  const topoTela = j.offsetParent.getBoundingClientRect().top;
  const teto = (document.getElementById("topo")?.getBoundingClientRect().bottom || 0) + 6 - topoTela;  // nunca sob o cabeçalho
  const y = Math.max(teto, Math.min(g.H + 4, innerHeight - topoTela - j.offsetHeight - 8));
  j.style.top = y + "px";`,
  `  const g = geometriaHeroi();
  const topoTela = j.offsetParent.getBoundingClientRect().top;
  if (faixas) {  // [proposta D] da largura da arena, colado embaixo dela; a lista rola dentro se não couber
    j.style.left = "0px";
    j.style.width = g.W + "px";
    j.style.top = g.H + "px";
    j.style.maxHeight = Math.max(170, innerHeight - topoTela - g.H - 14) + "px";
    // onde caem as texturas da página (a leitura da cena e o carvão do palco), para um fundo que continue a página
    // sem emenda (a D refinada usa; a D atual ignora)
    const pj = j.getBoundingClientRect(), cena = document.getElementById("cena"), palco = document.getElementById("palco");
    if (cena && palco) {
      const c = cena.getBoundingClientRect(), pa = palco.getBoundingClientRect();
      j.style.setProperty("--fundo-cena", \`\${c.left + 64 - pj.left}px \${c.top + 32 - pj.top}px\`);
      j.style.setProperty("--fundo-palco", \`\${pa.left + 12 - pj.left}px \${pa.top + 12 - pj.top}px\`);
    }
  } else {
    const x = ancora.offsetLeft - 8;
    j.style.left = Math.max(6, Math.min(x, g.W - j.offsetWidth - 6)) + "px";
    const teto = (document.getElementById("topo")?.getBoundingClientRect().bottom || 0) + 6 - topoTela;  // nunca sob o cabeçalho
    const y = Math.max(teto, Math.min(g.H + 4, innerHeight - topoTela - j.offsetHeight - 8));
    j.style.top = y + "px";
  }`],
  ['    previaAlvos(null);\n    j.remove();\n    ancora.classList.remove("ativo");',
    `    previaAlvos(null);
    const devolver = faixas && j.contains(document.activeElement);  // fechou pelo teclado: o foco volta ao botão
    j.remove();
    ancora.classList.remove("ativo");
    if (devolver && ancora.isConnected && ancora.focus) ancora.focus({ preventScroll: true });`],
  ['  janelaAberta = { fechar: fecharTudoJanela, soltar: () => document.removeEventListener("pointerdown", fora, true) };\n  Telas.ligarDicas(j);\n}',
    `  janelaAberta = { fechar: fecharTudoJanela, soltar: () => document.removeEventListener("pointerdown", fora, true) };
  Telas.ligarDicas(j);
  if (faixas) faixasTeclado(j, linhas);
}
/** [proposta D] O teclado nas faixas, a prévia dos alvos no foco e a dica ao lado do painel. */
function faixasTeclado(j, linhas) {
  const bs = [...j.querySelectorAll(".rj-linha")], n = bs.length, filas = Math.ceil(n / 2);
  bs.forEach((b, k) => {
    b.addEventListener("mouseenter", () => {  // a dica sai do painel: ao lado dele, não por cima da outra coluna
      const c = document.getElementById("dica-item");
      if (!c || c.hidden || c._dono !== b) return;
      const p = j.getBoundingClientRect(), w = c.offsetWidth;
      c.style.left = (p.right + 8 + w <= innerWidth - 6 ? p.right + 8 : Math.max(6, p.left - w - 8)) + "px";
    });
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
    if (novo >= 0 && novo < n) bs[novo].focus({ preventScroll: true });
  });
  if (performance.now() - gestoTecla < 400 && bs[0]) bs[0].focus({ preventScroll: true });  // aberta pela tecla
}
let gestoTecla = 0;  // [proposta D] quando foi a última tecla (o clique zera): a janelinha aberta pela tecla já chega com o foco
document.addEventListener("keydown", () => { gestoTecla = performance.now(); }, true);
document.addEventListener("pointerdown", () => { gestoTecla = 0; }, true);`],
];

/** O escolhas.js do jogo com as trocas da proposta D; para se o arquivo do jogo mudou e uma troca não acha o texto. */
export function escolhasD(texto) {
  return TROCAS.reduce((t, [a, b]) => {
    if (!t.includes(a)) throw new Error(`escolhas.js mudou: não achei ${a.slice(0, 80)}`);
    return t.replace(a, () => b);
  }, texto);
}
