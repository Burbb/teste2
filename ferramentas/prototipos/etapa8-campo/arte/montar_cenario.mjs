// Campo Livre 8: as fontes em Aseprite do cenário sóbrio (a direção escolhida pelo Jean), que faltavam: a textura do
// chão (16 × 16, à mão), cada construção e cada árvore do trecho da povoação (a casa, os dois trechos da muralha, as
// torres, o muro baixo, as sete árvores). Cada peça é pintada pelo mesmo código do protótipo (tela/arte7.js), pixel a
// pixel, sem redesenhar a composição escolhida: uma tela falsa registra os pixels e o Aseprite, em lote, monta o
// arquivo (uma camada, `pintura`; a textura do chão com as camadas `base`, `baixo` e `alto`, uma por tom). Para o
// protótipo ver um retoque feito no editor, ele precisa voltar para os motivos de arte7.js (a autoridade, por enquanto).
// Uso: node arte/montar_cenario.mjs [caminho do Aseprite.exe]
import { writeFileSync, mkdirSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

// a tela falsa: guarda cada fillRect com a cor da vez (as peças só pintam pixels e retângulos)
class Registro {
  constructor() { this.width = 0; this.height = 0; this.px = new Map(); }
  getContext() {
    const r = this;
    return {
      fillStyle: "#000",
      fillRect(x, y, w, h) {
        if (/rgba\([^)]*,\s*0\)$/.test(this.fillStyle)) return;
        for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) r.px.set(`${Math.round(x + i)},${Math.round(y + j)}`, this.fillStyle);
      },
      beginPath() {}, ellipse() {}, fill() {}, save() {}, restore() {}, drawImage() {},
    };
  }
}
globalThis.document = { createElement: () => new Registro() };

const { predioPintado, TEXTURA, CORES_CENARIO } = await import("../tela/arte7.js");
const { CENARIOS } = await import("../tela/conteudo.js");
const AQUI = dirname(fileURLToPath(import.meta.url));
const EXE = process.argv[2] || "C:/Program Files (x86)/Steam/steamapps/common/Aseprite/Aseprite.exe";
const P = CORES_CENARIO.sobria, pasta = join(AQUI, "fontes", "cenario-sobrio");
mkdirSync(pasta, { recursive: true });

const lua = [`local function cor(h) return Color{ r = tonumber(h:sub(2, 3), 16), g = tonumber(h:sub(4, 5), 16), b = tonumber(h:sub(6, 7), 16), a = 255 } end
local function arquivo(d)
  local s = Sprite(d.w, d.h, ColorMode.RGB)
  s.layers[1].name = d.camadas[1].nome
  for i = 2, #d.camadas do local l = s:newLayer(); l.name = d.camadas[i].nome end
  for i, c in ipairs(d.camadas) do
    local img = Image(d.w, d.h, ColorMode.RGB)
    for _, p in ipairs(c.px) do img:drawPixel(p[1], p[2], cor(p[3])) end
    s:newCel(s.layers[i], 1, img, Point(0, 0))
  end
  s:saveAs(d.saida)
  s:close()
end`];
const feitos = [];
const camada = (nome, px) => `{ nome = "${nome}", px = { ${px.map(([x, y, c]) => `{${x},${y},"${c}"}`).join(",")} } }`;
const hex = (c) => (c.startsWith("#") ? c : "#000000");

// a textura do chão
const base = [], baixo = [], alto = [];
for (let y = 0; y < 16; y++) for (let x = 0; x < 16; x++) {
  base.push([x, y, P.campo]);
  const ch = TEXTURA[y][x];
  if (ch === "a") baixo.push([x, y, P.textura[0]]);
  if (ch === "b") alto.push([x, y, P.textura[1]]);
}
const saidaTex = join(pasta, "chao-textura.aseprite").replaceAll("\\", "/");
lua.push(`arquivo({ w = 16, h = 16, camadas = { ${camada("base", base)}, ${camada("baixo", baixo)}, ${camada("alto", alto)} }, saida = "${saidaTex}" })`);
feitos.push("cenario-sobrio/chao-textura.aseprite");

// as construções e as árvores do trecho da povoação (uma por forma diferente)
const vistos = new Set();
for (const o of CENARIOS.povoado.obstaculos) {
  const chave = `${o.tipo}-${o.w}x${o.h}-${o.alto}${o.copa ? "-c" + o.copa : ""}`;
  if (vistos.has(chave)) continue;
  vistos.add(chave);
  const { c } = predioPintado({ ...o, tiro: o.tipo !== "muro" && o.tipo !== "arvore" }, "sobria");
  const px = [];
  for (const [k, cor] of c.px) { const [x, y] = k.split(",").map(Number); if (x >= 0 && y >= 0 && x < c.width && y < c.height) px.push([x, y, hex(cor)]); }
  const saida = join(pasta, `${chave}.aseprite`).replaceAll("\\", "/");
  lua.push(`arquivo({ w = ${c.width}, h = ${c.height}, camadas = { ${camada("pintura", px)} }, saida = "${saida}" })`);
  feitos.push(`cenario-sobrio/${chave}.aseprite`);
}
const temp = join(tmpdir(), "campo8-cenario.lua");
writeFileSync(temp, lua.join("\n") + "\n");
execFileSync(EXE, ["-b", "--script", temp], { stdio: "inherit" });
console.log(`${feitos.length} fontes do cenário sóbrio:\n  ${feitos.join("\n  ")}`);
