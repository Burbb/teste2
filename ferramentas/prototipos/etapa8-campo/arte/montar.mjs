// Campo Livre 7: as fontes em Aseprite do estudo de arte das miniaturas, montadas em lote a partir das grades à mão
// (tela/sprites7.js e, na direção sóbria, as grades atuais de tela/sprites.js com a paleta nova). Um arquivo por
// unidade e direção, com uma camada por equipe (aliados, inimigos) e um quadro por pose, cada quadro com a etiqueta da
// pose: parado, andarA, andarB, preparo, golpe, recuo. As grades continuam sendo a autoridade (o protótipo as lê); a
// fonte .aseprite é para abrir, conferir e retocar no editor, e se refaz com este script.
// Uso: node arte/montar.mjs [caminho do Aseprite.exe]
import { writeFileSync, mkdirSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { MODELOS, PALETA, EQUIPES, montar } from "../tela/sprites.js";
import { PALETAS, EQUIPES_ARTE, CORES_ARTE, MODELOS_SOMBRIOS, MODELOS_MENORES } from "../tela/sprites7.js";

const AQUI = dirname(fileURLToPath(import.meta.url));
const EXE = process.argv[2] || "C:/Program Files (x86)/Steam/steamapps/common/Aseprite/Aseprite.exe";
const AMOSTRA = ["guerreiro", "mago", "morel", "odette", "lider", "soldado", "arqueiro", "cavaleiro", "pesado"];
const POSES = ["parado", "andarA", "andarB", "preparo", "golpe", "recuo"];

// as mesmas regras de sprites.prepararSprites: as pernas trocadas nas passadas, a pose de golpe do herói de pernas abertas
function quadros(mod) {
  const def = mod.pernas || "juntas";
  return {
    parado: montar(mod, "parado", def), andarA: montar(mod, mod.andarA ? "andarA" : "parado", mod.pernas ? def : "abertas"),
    andarB: montar(mod, mod.andarB ? "andarB" : "parado", mod.pernas ? def : "cruzadas"), preparo: montar(mod, "preparo", def),
    golpe: montar(mod, "golpe", mod.heroi ? "abertas" : def), recuo: montar(mod, mod.recuo ? "recuo" : "parado", def),
  };
}

const lua = [];
lua.push(`local function hex(h) return Color{ r = tonumber(h:sub(2, 3), 16), g = tonumber(h:sub(4, 5), 16), b = tonumber(h:sub(6, 7), 16), a = 255 } end`);
lua.push(`local function montarArquivo(d)
  local s = Sprite(d.w, d.h, ColorMode.RGB)
  s.layers[1].name = d.camadas[1]
  for i = 2, #d.camadas do local l = s:newLayer(); l.name = d.camadas[i] end
  for f = 2, #d.poses do s:newEmptyFrame() end
  for f, pose in ipairs(d.poses) do
    for c = 1, #d.camadas do
      local img = Image(d.w, d.h, ColorMode.RGB)
      for _, p in ipairs(d.px[c][f]) do img:drawPixel(p[1], p[2], hex(p[3])) end
      s:newCel(s.layers[c], f, img, Point(0, 0))
    end
    local t = s:newTag(f, f); t.name = pose
  end
  s.layers[2].isVisible = false
  s:saveAs(d.saida)
  s:close()
end`);
const feitos = [];
for (const direcao of ["sobria", "sombria"]) for (const escala of ["atual", "menor"]) {
  for (const tipo of AMOSTRA) {
    if (escala === "menor" && !MODELOS_MENORES[tipo]) continue;
    const mod = escala === "menor" ? MODELOS_MENORES[tipo] : direcao === "sombria" && MODELOS_SOMBRIOS[tipo] || MODELOS[tipo];
    const paleta = PALETAS[direcao], q = quadros(mod);
    const w = Math.max(...POSES.map((p) => q[p][0].length)), h = Math.max(...POSES.map((p) => q[p].length));
    const px = [0, 1].map((eq) => POSES.map((p) => {
      const cores = (CORES_ARTE[direcao] && CORES_ARTE[direcao][tipo]) || mod.cores || EQUIPES_ARTE[direcao][eq] || EQUIPES[eq], l = [];
      q[p].forEach((linha, y) => [...linha].forEach((ch, x) => { if (ch !== ".") l.push(`{${x},${y},"${cores[ch] || paleta[ch] || PALETA[ch]}"}`); }));
      return `{${l.join(",")}}`;
    }));
    const nome = `${tipo}${escala === "menor" ? "-menor" : ""}`, pasta = join(AQUI, "fontes", direcao);
    mkdirSync(pasta, { recursive: true });
    const saida = join(pasta, `${nome}.aseprite`).replaceAll("\\", "/");
    lua.push(`montarArquivo({ w = ${w}, h = ${h}, camadas = { "aliados", "inimigos" }, poses = { ${POSES.map((p) => `"${p}"`).join(", ")} },
  px = { ${px.map((c) => `{ ${c.join(", ")} }`).join(", ")} }, saida = "${saida}" })`);
    feitos.push(`${direcao}/${nome}.aseprite`);
  }
}
// o Aseprite não roda um script com espaço no caminho: o .lua vai para uma pasta temporária
const temp = join(tmpdir(), "campo7-montar.lua");
writeFileSync(temp, lua.join("\n") + "\n");
execFileSync(EXE, ["-b", "--script", temp], { stdio: "inherit" });
console.log(`${feitos.length} fontes:\n  ${feitos.join("\n  ")}`);
