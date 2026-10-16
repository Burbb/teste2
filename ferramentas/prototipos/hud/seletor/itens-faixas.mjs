// O menu de Itens na linguagem do seletor de habilidades (protótipo; a página da foto recebe esta cópia do escolhas.js
// do jogo, e itens-faixas.css por cima de 18-seletor-habilidades.css; o jogo não muda). Reaproveita o componente: a
// mesma posição embaixo da arena, as faixas, os estados, o teclado, a entrada e a descrição embaixo da coluna. O que é
// do menu de Itens fica explícito (data-menu="itens" e itens-faixas.css):
//   - a quantidade no lugar do custo, à direita ("×2"), e também no texto da descrição ("Você tem 2 · gasta o turno");
//   - o efeito e o motivo de não poder usar são os que o motor já manda (a desc do consumível, motivo_item);
//   - quem recebe: o mesmo caminho de hoje (a poção que pode ir num aliado abre a mira dos aliados, as outras vão);
//   - a troca de arma é uma faixa como as outras, com a ficha da arma na descrição;
//   - bolsa sem nada que sirva: o seletor abre com a frase "Nada na bolsa serve agora." no lugar das faixas (hoje o
//     botão só treme e avisa), e Esc ou o botão fecham.
const TROCAS = [
  ['  const faixas = titulo === "Habilidades";  // o seletor de faixas\n  j.dataset.tipo = faixas ? "habilidades" : "itens";',
    '  const faixas = titulo === "Habilidades" || titulo === "Itens";  // [protótipo] Itens também em faixas\n  j.dataset.tipo = faixas ? "habilidades" : "itens";\n  j.dataset.menu = titulo === "Itens" ? "itens" : "habilidades";'],
  ['  j.appendChild(lista);\n  if (faixas) {',
    '  j.appendChild(lista);\n  if (faixas && !linhas.length) lista.insertAdjacentHTML("afterend", \'<p class="rj-vazio">Nada na bolsa serve agora.</p>\');  // [protótipo]\n  if (faixas) {'],
  ['    if (!itens.length) { tremerNao(b, "Nada na bolsa serve agora."); return; }',
    '    // [protótipo] a bolsa vazia abre o seletor com a frase, no lugar do tremor'],
];

export function escolhasItens(texto) {
  return TROCAS.reduce((t, [a, b]) => {
    if (!t.includes(a)) throw new Error(`escolhas.js mudou: não achei ${a.slice(0, 80)}`);
    return t.replace(a, () => b);
  }, texto);
}
