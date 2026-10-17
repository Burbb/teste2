// O teste do pen.dev (experimento): tira do jogo o seletor de Habilidades de verdade, nas janelas 1280×720 e 1500×950,
// e grava o DOM dele (com as posições e as variáveis que o escolhas.js põe) em dados/seletor-<janela>.json. A bancada
// (bancada.html) monta com isso uma composição pequena e estática: duas faixas (Flecha Envenenada, nome longo e custo
// duplo; e uma indisponível) e a área da descrição, nos três estados, com as folhas de estilo do jogo sem cópia.
// O jogo não muda: é o cenário tutorial (Arqueiro sombra no nível 12, contra lobos, como em fotografar_seletor_d.mjs).
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/pen-composicao/extrair.mjs
import { spawn } from "child_process";
import { mkdirSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const DADOS = path.join(aqui, "dados");
mkdirSync(DADOS, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const AMB = { TUTORIAL: "0", LUTA: "lobo", COMITIVA: "morel,odete", NIVEL: "12", VISTAS: "A1,V2,N1,D1,K1,M1,L1",
  CLASSE: "arqueiro", ESPEC: "sombra", QUANTOS: "3", REC: "0.3" };
const JANELAS = { "1280x720": [1280, 720], "1500x950": [1500, 950] };

async function subir() {
  const proc = spawn(process.env.PYTHON || "python", ["-m", "tests.navegador.cenarios", "tutorial"],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, ...AMB } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[tutorial] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}
const { proc, url } = await subir();
const b = await chromium.launch();
try {
  for (const [nome, [W, H]] of Object.entries(JANELAS)) {
    const p = await b.newPage({ viewport: { width: W, height: H } });
    await p.goto(url);
    for (let k = 0; k < 200; k++) {
      if (await p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando && !!document.querySelector('#roda .roda-botao[data-slot="habilidades"]'))) break;
      for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
      await espera(250);
    }
    await (await p.$('#roda .roda-botao[data-slot="habilidades"]')).click();
    await espera(600);
    // a descrição de cada uma: o mouse em cima e a caixa como o jogo a montou
    const linhas = await p.$$eval(".roda-janela .rj-linha", (ls) => ls.map((l) => ({ hab: l.dataset.hab, nome: l.querySelector(".rj-nome").textContent,
      info: l.querySelector(".rj-info").innerHTML, bloqueada: l.classList.contains("bloqueada") })));
    const desc = {};
    for (const l of linhas) {
      await p.hover(`.roda-janela .rj-linha[data-hab="${l.hab}"]`); await espera(250);
      desc[l.hab] = await p.$eval(".roda-janela .rj-desc-caixa", (c) => ({ html: c.innerHTML, lado: c.dataset.lado, estilo: c.getAttribute("style") }));
    }
    await p.mouse.move(5, H - 5); await espera(200);
    const seletor = await p.evaluate(() => {
      const j = document.querySelector(".roda-janela"), R = j.getBoundingClientRect();
      const zona = j.querySelector(".rj-descricao");
      return { estilo: j.getAttribute("style"), classes: j.className, tipo: j.dataset.tipo, largura: R.width, altura: R.height,
        titulo: j.querySelector(".rj-titulo").outerHTML, voltar: (j.querySelector(":scope > .rj-voltar") || {}).outerHTML || "",
        lista_estilo: j.querySelector(".rj-lista").getAttribute("style"), zona_estilo: zona && zona.getAttribute("style"),
        // a superfície da página atrás (as variáveis da textura alinhada)
        fundo: { cena: getComputedStyle(j).getPropertyValue("--fundo-cena"), palco: getComputedStyle(j).getPropertyValue("--fundo-palco") },
        itens: [...j.querySelectorAll(".rj-lista > li")].map((li) => ({ forma: li.dataset.forma, estilo: li.getAttribute("style"), html: li.innerHTML })) };
    });
    writeFileSync(path.join(DADOS, `seletor-${nome}.json`), JSON.stringify({ janela: [W, H], linhas, desc, seletor }, null, 1));
    console.log(nome, Math.round(seletor.largura), "×", Math.round(seletor.altura), linhas.map((l) => `${l.nome}${l.bloqueada ? " (indisp.)" : ""} [${l.info.replace(/<[^>]+>/g, "")}]`).join(" | "));
    await p.close();
  }
} finally { await b.close(); proc.kill(); }
