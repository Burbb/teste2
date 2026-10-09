/* Crônicas da Fenda — realce de termos de jogo nos textos de regra (dicas, Grimório, talentos, registro da luta).
   Como nos RPGs atuais: fogo em laranja, sangramento e roubo de vida em vermelho, cura em verde, crítico em amarelo...
   Recebe texto puro e devolve HTML já escapado; só a prosa da história fica de fora (lá "fogo" é paisagem). */
"use strict";

const Realce = (() => {
  const ESC = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
  const h = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ESC[c]);
  const NUM = "[+−-]?\\d+(?:[.,]\\d+)?(?:\\s*[–-]\\s*\\d+(?:[.,]\\d+)?)?%?";
  const COM_NUM = (termo, liga = "de\\s+") => `(?:${NUM}\\s+(?:${liga})?)?(?:${termo})`;

  // [classe, padrão]. A ordem é a prioridade: quando dois trechos se cruzam, vale o que vem antes.
  const REGRAS = [
    ["sangue", COM_NUM("roubo de vida")],
    ["sangue", "rouba(?:m)?\\b[^.;:]{0,40}?vida"],
    ["sangue", COM_NUM("sangramento|sangrar|sangrando|sangra|Sede de Sangue|Sede Insaciável|Pacto de Sangue|Drenar Vida")],
    ["crit", `crítico:?\\s+${NUM}(?:\\s+de\\s+chance)?`],
    ["crit", COM_NUM("(?:chance\\s+de\\s+)?(?:acerto\\s+)?crítico(?:s)?(?:\\s+garantido)?(?:\\s*\\([^)]{1,24}\\))?", "de\\s+")],
    ["fogo", COM_NUM("(?:dano\\s+de\\s+)?(?:fogo|chamas|queimaduras|queimadura|labaredas|Combustão|Bola de Fogo|Inferno|incendeia|acende)")],
    ["gelo", COM_NUM("(?:dano\\s+de\\s+)?(?:gelo|congelamento|congelado|congelada|congelar|congela|Lança de Gelo)")],
    ["veneno", COM_NUM("(?:dano\\s+de\\s+)?(?:veneno|envenenado|envenenada|envenenar|envenena|Flecha Envenenada)")],
    ["sombra", COM_NUM("(?:dano\\s+de\\s+)?(?:sombra|sombrio|maldição|maldito|maldita|amaldiçoa\\p{L}*)")],
    ["sagrado", COM_NUM("(?:dano\\s+)?(?:sagrado|sagrada|luz sagrada)")],
    ["mana", `(?:(?:recupera(?:m)?|devolve)\\s+)?${NUM}\\s+(?:de\\s+)?mana`],
    ["vigor", `(?:(?:recupera(?:m)?|devolve)\\s+)?${NUM}\\s+(?:de\\s+)?vigor`],
    ["foco", `(?:(?:recupera(?:m)?|devolve)\\s+)?${NUM}\\s+(?:de\\s+)?foco`],
    ["cura", `(?:recupera(?:m)?|cura(?:m|r)?|devolve)(?:\\s+${NUM})?(?:\\s+(?:de|da)\\s+vida)?`],
    ["cura", `\\+${NUM}\\s+(?:de\\s+)?vida`],
    ["mana", COM_NUM("mana")],
    ["vigor", COM_NUM("vigor")],
    ["foco", COM_NUM("foco")],
    ["esquiva", `esquiva\\s+${NUM}`],
    ["esquiva", COM_NUM("esquiva|esquivar")],
    ["protecao", "barreira|escudo|absorve(?:m|r)?|absorvido|reduz o dano recebido(?:\\s+pela metade)?"],
    ["controle", "atordoamento|atordoado|atordoada|atordoar|atordoa"],
    ["dano", `${NUM}\\s+de\\s+dano(?:\\s+físico)?`],
    ["num", `${NUM.replace("%?", "%")}|×\\s?\\d+(?:[.,]\\d+)?%?`],
  ].map(([c, src], prio) => [c, new RegExp(`(?<![\\p{L}\\d])(?:${src})(?![\\p{L}])`, "giu"), prio]);

  function texto(s) {
    s = String(s ?? "");
    if (!s) return "";
    const achados = [];
    REGRAS.forEach(([cls, re, prio]) => {
      for (const m of s.matchAll(re)) if (m[0].trim()) achados.push({ a: m.index, b: m.index + m[0].length, cls, prio });
    });
    achados.sort((x, y) => x.prio - y.prio || (y.b - y.a) - (x.b - x.a));
    const escolhidos = [];
    achados.forEach((x) => { if (!escolhidos.some((y) => x.a < y.b && y.a < x.b)) escolhidos.push(x); });
    escolhidos.sort((x, y) => x.a - y.a);
    let out = "", i = 0;
    escolhidos.forEach((x) => { out += h(s.slice(i, x.a)) + `<span class="rx rx-${x.cls}">${h(s.slice(x.a, x.b))}</span>`; i = x.b; });
    return out + h(s.slice(i));
  }

  /** Números com sinal num relance: o que soma em verde, o que tira em vermelho (aprovação +48, "de −100 a +100").
   *  Como nos RPGs atuais: a cor diz o lado antes de a pessoa ler o número. */
  function sinais(s) {
    return h(s).replace(/(?<![\p{L}\d])([+−-])(\d+(?:[.,]\d+)?%?)(?![\p{L}\d])/gu,
      (m, sinal, n) => `<span class="rx rx-${sinal === "+" ? "bom" : "ruim"}">${sinal}${n}</span>`);
  }

  return { texto, sinais };
})();
