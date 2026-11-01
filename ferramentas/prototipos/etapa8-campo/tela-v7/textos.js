// PROTÓTIPO de campo livre: os textos de regra das habilidades, com os números do kit montado (depois dos talentos que
// mudam números). A tela não calcula regra nenhuma: só escreve o que conteudo.js e montarKit dizem. Critério: o efeito
// primeiro, verbo no indicativo, os números que decidem, a condição como condição; sem conselho de uso.
import { HEROIS } from "./conteudo.js";

const n = (v) => String(Math.round(v * 100) / 100).replace(".", ",");
const pct = (v) => `${Math.round(v * 100)}%`;

/** As teclas de cada espaço do kit. */
export const TECLAS_ESPACO = { principal: "Botão esquerdo", mobilidade: "Espaço", h1: "Botão direito", h2: "Q", h3: "E", ult: "F" };

/** O custo e a recarga, no formato comum ("30 de Mana · Recarga 8 s"; a ultimate, "Ultimate · Recarga 30 s"). */
export function custoDe(heroi, k) {
  const rec = HEROIS[heroi].recurso.nome, partes = [];
  if (k.tipo === "ultimate") partes.push("Ultimate");
  if (k.custo) partes.push(`${k.custo} de ${rec}`);
  if (k.recarga) partes.push(`Recarga ${n(k.recarga)} s`);
  if (k.tipo === "principal") partes.push("Segure para repetir");
  return partes.join(" · ");
}

/** A descrição de uma habilidade do kit montado (`k`, com os números já ajustados). */
export function descricao(heroi, k) {
  switch (k.id) {
    case "varredura": return `Prende os pés por ${n(k.preparo)} s e varre ${k.abertura}° à frente (${k.raio} px): causa ${k.dano} de dano, arremessa quem cai, empurra e atordoa os outros. Vira para o inimigo mais perto da mira (até ${k.assist.alcance} px) e avança até ${k.avanca} px para alcançá-lo; sem ninguém, golpeia para onde o mouse aponta.`;
    case "investida": return `Avança ${k.distancia} px na direção do mouse sem receber dano. Joga para os lados quem está no caminho (${k.dano} de dano). O campeão e o Capitão param a investida.`;
    case "salto": return `Salta até o mouse (até ${k.alcance} px) sem receber dano e cai num círculo de ${k.raio} px: causa ${k.dano} de dano, arremessa e atordoa.`;
    case "turbilhao": return `Prende os pés por ${n(k.preparo)} s e puxa para perto de você os inimigos comuns a até ${k.puxa} px (o campeão e o Capitão, não); no fim, causa ${k.dano} de dano num círculo de ${k.raio} px, arremessa quem cai e atordoa os outros.`;
    case "sismico": return `Manda uma onda pelo chão na direção do mouse: corre ${k.comprimento} px e causa ${k.dano} de dano a cada inimigo a até ${k.largura} px dela, uma vez, jogando-os para os lados e atordoando.`;
    case "corteSangrento": return `Varre ${k.abertura}° à frente (${k.raio} px): causa ${k.dano} de dano e aplica ${k.acumulos} acúmulos de Sangramento (cada acúmulo causa 2 a cada 0,5 s por 3 s; até 5).`;
    case "ruptura": return `Cada inimigo com Sangramento a até ${k.raio} px de você leva ${k.porAcumulo} de dano por acúmulo, perde o Sangramento e explode num círculo de ${k.explosao.raio} px, causando ${k.explosao.porAcumulo} por acúmulo aos outros.`;
    case "grito": return `Inspira os aliados a até ${k.raio} px por ${k.inspira} s (atacam ${pct(1 / k.ritmo - 1)} mais rápido e recuperam ${k.cura} de vida por segundo) e abala por ${n(k.abala)} s os inimigos comuns a até ${k.raioAbala} px.`;
    case "escudo": return `Ergue o escudo por ${n(k.escudo)} s, virado para o mouse, andando a ${pct(k.mover)} da velocidade: barra as flechas inimigas que cruzam o arco (${k.raio} px, ${k.abertura}°) vindo da frente e empurra quem está nele (${k.dano} de dano na primeira vez). Os aliados a até ${k.protege} px levam ${pct(1 - k.reducao)} menos dano. Outra habilidade o encerra.`;
    case "furia": return `Por ${k.duracao} s, a Varredura volta a cada ${n(k.recargaPrincipal)} s e alcança ${k.raioExtra} px a mais.`;
    case "terremoto": return `Abre ${k.aneis.length} anéis em volta de você, um a cada ${n(k.intervalo)} s, até ${k.aneis[k.aneis.length - 1]} px: cada inimigo é pego uma vez, pelo primeiro anel que o alcança, e leva ${k.dano} de dano, é arremessado e atordoado.`;
    case "bola": return `Explode no ponto do mouse (até ${k.alcance} px) num círculo de ${k.raio} px: causa ${k.dano} de dano e arremessa quem cai. O chão queima por ${k.chao.duracao} s (${k.chao.tique} a cada 0,5 s).`;
    case "piscar": return `Reaparece até ${k.distancia} px na direção do mouse. Onde estava, uma onda de ${k.raio} px causa ${k.dano} de dano, empurra e atordoa.`;
    case "lanca": return `Lança uma lança de gelo na direção do mouse: atravessa todos os inimigos no caminho até ${k.alcance} px e causa ${k.dano} de dano a cada um, uma vez.`;
    case "raios": return `Lança um raio na direção do mouse (até ${k.alcance} px): acerta o primeiro inimigo da linha e salta para o inimigo mais perto ainda não atingido (até ${k.salto} px), até ${k.alvos} alvos. Causa ${k.dano} de dano no primeiro e ${k.queda} a menos a cada salto (no mínimo ${k.danoMin}).`;
    case "muralha": return `Ergue uma parede de fogo de ${k.comprimento} px no ponto do mouse (até ${k.alcance} px), de lado para você, por ${k.duracao} s. Desvia os inimigos e causa ${k.tique} a cada 0,5 s a quem entra.`;
    case "anel": return `Ergue um anel de fogo de ${k.raio} px de raio no ponto do mouse (até ${k.alcance} px) por ${k.duracao} s. Ninguém atravessa a linha: quem está dentro fica dentro. A linha causa ${k.tique} a cada 0,5 s.`;
    case "campoGelo": return `Cobre de gelo um círculo de ${k.raio} px no ponto do mouse (até ${k.alcance} px) por ${k.duracao} s. Ao surgir, causa ${k.dano} de dano e atordoa. Dentro dele, os inimigos andam a ${pct(k.lento)} e atacam com ${pct(k.ritmo)} da frequência (o campeão e o Capitão, ${pct(k.lentoElite)} e ${pct(k.ritmoElite)}).`;
    case "vortice": return `Abre um vórtice de ${k.raio} px no ponto do mouse (até ${k.alcance} px) que puxa os inimigos para o centro por ${n(k.duracao)} s (o campeão e o Capitão, a 30%); no fim, implode: ${k.implosao.dano} de dano num círculo de ${k.implosao.raio} px.`;
    case "ignicao": return `Causa ${k.dano} de dano num círculo de ${k.raio} px no ponto do mouse (até ${k.alcance} px) e deixa uma Brasa em cada um por ${k.brasa.duracao} s. Um inimigo que morre com Brasa explode num círculo de ${k.brasa.raio} px e causa ${k.brasa.dano} aos outros.`;
    case "meteoros": return `Chama ${k.n} meteoros, um a cada ${n(k.intervalo)} s, em pontos sorteados a até ${k.area} px do mouse (até ${k.alcance} px de você). Cada um marca o chão ${n(k.aviso)} s antes de cair: ${k.dano} de dano num círculo de ${k.raio} px, arremessa, e o chão queima por ${k.chao.duracao} s.`;
    case "nevasca": return `Cobre de neve um círculo de ${k.raio} px no ponto do mouse (até ${k.alcance} px) por ${k.duracao} s. Ao surgir, causa ${k.dano} de dano; dentro dele, ${k.tique} a cada 0,5 s, e os inimigos andam a ${pct(k.lento)} e atacam com ${pct(k.ritmo)} da frequência (o campeão e o Capitão, ${pct(k.lentoElite)} e ${pct(k.ritmoElite)}).`;
  }
  return "";
}

/** As marcas e os tipos da habilidade, numa linha curta ("Comum · Gelo"). */
export function rotulo(k, MARCAS) {
  const tipo = { principal: "Ataque principal", mobilidade: "Mobilidade", comum: "Comum", ultimate: "Ultimate" }[k.tipo];
  return [tipo, ...(k.marcas || []).map((m) => MARCAS[m])].join(" · ");
}
