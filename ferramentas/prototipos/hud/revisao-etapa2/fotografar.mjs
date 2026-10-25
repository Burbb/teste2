// A revisão delimitada para fechar a etapa 2 (25/10/2026, sobre a 1.209.0; só fotografa e mede, nada muda no jogo): o
// roteiro do levantamento (levantamento-etapa2/fotografar.mjs) a 1920×945 e a 1280×720 (JANELA=1920 ou 1280), as telas
// abertas como o jogador abre, mais a auditoria do foco: em cada tela, o Tab por até 30 elementos, anotando os que
// recebem o foco sem anel visível (outline, sombra ou borda que muda). Guarda capturas/<janela>-<tela>.png e
// capturas/<janela>-foco.json.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/revisao-etapa2/fotografar.mjs
import { spawn } from "child_process";
import { mkdirSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const SAIDA = path.join(aqui, "capturas");
const JAN = process.env.JANELA || "1920";
const VISTA = JAN === "1920" ? { width: 1920, height: 945 } : { width: 1280, height: 720 };
const FOCO = {};
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
const foto = async (p, nome) => { await p.mouse.move(2, 2); await espera(400); await p.screenshot({ path: path.join(SAIDA, `${JAN}-${nome}.png`) }); console.log("  ", nome); };
/** O Tab por até 30 elementos: os que recebem o foco sem nada visível (comparando o estilo com e sem o foco). */
async function auditarFoco(p, nome) {
  const sem = [];
  await p.evaluate(() => document.activeElement && document.activeElement.blur());
  for (let k = 0; k < 30; k++) {
    await p.keyboard.press("Tab");
    const r = await p.evaluate(() => {
      const e = document.activeElement; if (!e || e === document.body) return null;
      const c = getComputedStyle(e);
      const anel = (c.outlineStyle !== "none" && parseFloat(c.outlineWidth) > 0) || (c.boxShadow !== "none");
      const id = (e.id ? "#" + e.id : "") + (e.className && typeof e.className === "string" ? "." + e.className.trim().split(/\s+/).slice(0, 2).join(".") : "") || e.tagName;
      const txt = (e.innerText || e.getAttribute("aria-label") || "").replace(/\s+/g, " ").trim().slice(0, 30);
      const rr = e.getBoundingClientRect();
      return { id, txt, anel, fora: rr.bottom < 0 || rr.top > innerHeight || rr.width === 0 };
    });
    if (!r) break;
    if (!r.anel || r.fora) sem.push(r);
  }
  FOCO[nome] = sem;
  console.log("   foco", nome, sem.length ? JSON.stringify(sem) : "ok");
}

const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
{
  const { proc, url } = await subir("tutorial", { TUTORIAL: "0", LUGAR: "vau", COMITIVA: "morel,odete" });
  const p = await b.newPage({ viewport: VISTA });
  await p.goto(url); await parado(p);
  await foto(p, "01-vau");
  await auditarFoco(p, "vau");
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
  const p = await b.newPage({ viewport: VISTA });
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
  const p = await b.newPage({ viewport: VISTA });
  await p.goto(url);
  for (let k = 0; k < 40 && !(await p.$(".orientacao:not([hidden])")); k++) { const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {}); await espera(300); }
  await espera(800); await foto(p, "19-orientacao");
  await p.close(); proc.kill();
}
{
  const { proc, url } = await subir("campanha");
  const p = await b.newPage({ viewport: VISTA });
  await p.goto(url); await parado(p);
  await foto(p, "12-titulo");
  await auditarFoco(p, "titulo");
  const carregar = await p.$(`${MENU}:has-text("Carregar")`);
  if (carregar) { await carregar.click(); await espera(1200); await foto(p, "13-saves"); await auditarFoco(p, "saves"); }
  await p.close(); proc.kill();
}
{
  const { proc, url } = await subir("fogueira");
  const p = await b.newPage({ viewport: VISTA });
  await p.goto(url); await parado(p);
  await foto(p, "14-fogueira");
  await auditarFoco(p, "fogueira");
  await p.close(); proc.kill();
}
await b.close();
writeFileSync(path.join(SAIDA, `${JAN}-foco.json`), JSON.stringify(FOCO, null, 1));
