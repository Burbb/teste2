// PROTÓTIPO de campo livre (nada no jogo), Campo Livre 9: os símbolos das variações dos heróis inimigos, 5 × 5 pixels à
// mão, cada um com uma forma própria (não só a cor): o floco (Gélido), o escudo (Inabalável), a gota (Venenoso), a
// estrela de estilhaços (Rastro Explosivo), as presas (Vampírico), as setas duplas (Implacável). O mesmo desenho vai em
// cima da cabeça dele no campo e na etiqueta da barra; o contorno escuro de 1 px separa de qualquer fundo.
import { VARIACOES } from "./conteudo.js";

const GLIFOS = {
  gelido: ["#.#.#", ".###.", "##.##", ".###.", "#.#.#"],
  inabalavel: ["#####", "#...#", "#.#.#", ".#.#.", "..#.."],
  venenoso: ["..#..", ".###.", "##.##", "#####", ".###."],
  explosivo: ["#.#.#", ".#.#.", "#####", ".#.#.", "#.#.#"],
  vampirico: ["#####", "#.#.#", "#.#.#", ".....", "....."],
  implacavel: ["#..#.", ".#..#", "..#..", ".#..#", "#..#."],
};

/** Pinta o símbolo da variação `id` com o canto de cima à esquerda em (x, y), já em pixels da tela. */
export function pintarMarca(g, id, x, y) {
  const G = GLIFOS[id];
  if (!G) return;
  g.fillStyle = "#15121a";
  for (let j = 0; j < 5; j++) for (let i = 0; i < 5; i++) if (G[j][i] === "#") g.fillRect(x + i - 1, y + j - 1, 3, 3);
  g.fillStyle = VARIACOES[id].cor;
  for (let j = 0; j < 5; j++) for (let i = 0; i < 5; i++) if (G[j][i] === "#") g.fillRect(x + i, y + j, 1, 1);
}

const imagens = new Map();
/** O símbolo como imagem (data URL), ampliado `esc` vezes, para a HUD. */
export function imagemMarca(id, esc = 2) {
  const k = `${id}|${esc}`;
  if (imagens.has(k)) return imagens.get(k);
  const c = document.createElement("canvas");
  c.width = c.height = 7 * esc;
  const g = c.getContext("2d");
  g.scale(esc, esc);
  pintarMarca(g, id, 1, 1);
  const url = c.toDataURL();
  imagens.set(k, url);
  return url;
}
