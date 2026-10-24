// O levantamento dos componentes antigos restantes da etapa 2 (24/10/2026; só fotografa, nada muda no jogo): as telas
// e janelas que a campanha mostra, abertas como o jogador abre (as teclas da doca, F1, H), a 1920×945, num Vau do
// Turvo de teste (o cenário `tutorial` com o tutorial desligado e a comitiva junto), o menu do título com saves (o
// cenário `campanha`) e a fogueira. Guarda em capturas/<tela>.png.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/levantamento-etapa2/fotografar.mjs
import { spawn } from "child_process";
import { mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const SAIDA = path.join(aqui, "capturas");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");

async function subir(cenario, amb = {}) {
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", cenario],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error(`o cenário ${cenario} não subiu`);
  return { proc, url };
}
async function parado(p) {
  for (let k = 0; k < 80 && !(await p.$(MENU)); k++) {
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(300);
  }
  await espera(600);
}
const foto = async (p, nome) => { await p.mouse.move(2, 2); await espera(400); await p.screenshot({ path: path.join(SAIDA, `${nome}.png`) }); console.log("  ", nome); };

const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
{
  const { proc, url } = await subir("tutorial", { TUTORIAL: "0", LUGAR: "vau", COMITIVA: "morel,odete" });
  const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
  await p.goto(url); await parado(p);
  await foto(p, "01-vau");
  // as janelas por cima (F1, H) e as telas da doca (cada uma fecha pelo Esc ou pelo Voltar)
  for (const [tecla, nome] of [["F1", "02-ajuda"], ["h", "03-historico"]]) {
    await p.keyboard.press(tecla); await espera(700); await foto(p, nome); await p.keyboard.press(tecla); await espera(500);
  }
  for (const [tecla, nome] of [["m", "04-mapa"], ["d", "05-diario"], ["b", "06-bestiario"], ["c", "07-comitiva"],
    ["t", "08-talentos"], ["i", "09-inventario"], ["q", "10-sair"]]) {
    await p.keyboard.press(tecla); await espera(1200); await foto(p, nome);
    for (let k = 0; k < 3; k++) { await p.keyboard.press("Escape"); await espera(300); }
    const voltar = await p.$(`${MENU}:has-text("Voltar")`); if (voltar) await voltar.click().catch(() => {});
    await parado(p);
  }
  // o Grimório (a doca) e um serviço da vila (o Templo), pelo menu
  const g = await p.$('#doca .atalho[data-rotulo="Grimório"]'); if (g) { await g.click(); await espera(1200); await foto(p, "11-grimorio"); await p.keyboard.press("Escape"); await parado(p); }
  await p.close(); proc.kill();
}
{
  // os prédios da vila (o Templo, a Curandeira, o mural) e a viagem por um dos Caminhos
  const { proc, url } = await subir("tutorial", { TUTORIAL: "0", LUGAR: "vau" });
  const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
  await p.goto(url); await parado(p);
  for (const [predio, nome] of [["templo", "15-templo"], ["curandeira", "16-curandeira"], ["mural", "17-mural"]]) {
    const e = await p.$(`[data-predio="${predio}"]`);
    if (!e) { console.log("   (sem prédio)", predio); continue; }
    await e.click(); await espera(1500); await foto(p, nome);
    for (let k = 0; k < 2; k++) { await p.keyboard.press("Escape"); await espera(300); }
    const voltar = await p.$(`${MENU}:has-text("Voltar")`); if (voltar) await voltar.click().catch(() => {});
    await parado(p);
  }
  const caminho = await p.$("#mundo .caminho, #mundo [data-destino]");
  if (caminho) { await caminho.click(); await espera(1500); await foto(p, "18-viagem"); }
  await p.close(); proc.kill();
}
{
  // a abertura guiada: um quadro de orientação
  const { proc, url } = await subir("tutorial", { LUGAR: "vau" });
  const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
  await p.goto(url);
  for (let k = 0; k < 40 && !(await p.$(".orientacao:not([hidden])")); k++) { const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {}); await espera(300); }
  await espera(800); await foto(p, "19-orientacao");
  await p.close(); proc.kill();
}
{
  const { proc, url } = await subir("campanha");
  const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
  await p.goto(url); await parado(p);
  await foto(p, "12-titulo");
  const carregar = await p.$(`${MENU}:has-text("Carregar")`);
  if (carregar) { await carregar.click(); await espera(1200); await foto(p, "13-saves"); }
  await p.close(); proc.kill();
}
{
  const { proc, url } = await subir("fogueira");
  const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
  await p.goto(url); await parado(p);
  await foto(p, "14-fogueira");
  await p.close(); proc.kill();
}
await b.close();
