// Tira de retratos.js (o jogo) as grades e cores de cada papel, para comparar e desenhar fora do jogo, sem mudar nada:
//   node ferramentas/prototipos/hud/personagens/extrair.mjs > atuais.json
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../../..");
const fonte = readFileSync(path.join(raiz, "rpg/web/static/retratos.js"), "utf8");
const visto = {};
const Sprites = { grade: (nome, grade, cores) => { visto[nome] = { grade, cores }; return nome; }, gradeCanvas: () => null };
const Retratos = new Function("Sprites", fonte + "\nreturn Retratos;")(Sprites);
const saida = {};
for (const n of ["guerreiro", "mago", "arqueiro", "morel", "odete", "yara"])
  for (const p of ["busto", "bustoBaixo", "cabeca", "carta", "figura"]) {
    Retratos.url(n, p, 1);
    saida[`${n}-${p}`] = visto[`retrato-${n}-${p}`];
  }
console.log(JSON.stringify(saida));
