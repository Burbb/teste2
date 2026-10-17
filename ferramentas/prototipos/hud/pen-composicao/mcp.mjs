// Cliente MCP mínimo (stdio, JSON-RPC) para o servidor do pen.dev, usado no teste quando a sessão do Claude Code já
// estava aberta antes de o servidor ser configurado (uma sessão em andamento não carrega servidor novo). As ferramentas
// e as respostas são as mesmas que o Claude Code recebe pelo MCP.
//   node mcp.mjs lista                       → as ferramentas e os esquemas
//   node mcp.mjs <ferramenta> '<json>'       → chama uma ferramenta (ou: node mcp.mjs <ferramenta> @arquivo.json)
// PEN_MCP=<caminho do mcp-server-windows-x64.exe> (o padrão é a instalação do Windows em %LOCALAPPDATA%\Programs\Pen)
import { spawn } from "child_process";
import { readFileSync, writeFileSync } from "fs";
import path from "path";
const BIN = process.env.PEN_MCP || path.join(process.env.LOCALAPPDATA, "Programs/Pen/resources/app.asar.unpacked/out/mcp-server-windows-x64.exe");
const [, , acao, arg] = process.argv;
const srv = spawn(BIN, ["--app", "desktop", "--agent", "claudeCodeCLI"], { stdio: ["pipe", "pipe", "inherit"] });
let buf = "", id = 0;
const pendentes = new Map();
srv.stdout.on("data", (d) => {
  buf += d;
  let i;
  while ((i = buf.indexOf("\n")) >= 0) {
    const linha = buf.slice(0, i).trim(); buf = buf.slice(i + 1);
    if (!linha) continue;
    const msg = JSON.parse(linha);
    if (msg.id !== undefined && pendentes.has(msg.id)) { pendentes.get(msg.id)(msg); pendentes.delete(msg.id); }
  }
});
const pedir = (method, params) => new Promise((ok) => { const n = ++id; pendentes.set(n, ok); srv.stdin.write(JSON.stringify({ jsonrpc: "2.0", id: n, method, params }) + "\n"); });
const avisar = (method, params) => srv.stdin.write(JSON.stringify({ jsonrpc: "2.0", method, params }) + "\n");
const t0 = Date.now();
await pedir("initialize", { protocolVersion: "2025-06-18", capabilities: {}, clientInfo: { name: "claude-code-teste-pen", version: "1" } });
avisar("notifications/initialized", {});
let saida;
if (acao === "lista") saida = (await pedir("tools/list", {})).result;
else {
  const args = !arg ? {} : arg.startsWith("@") ? JSON.parse(readFileSync(arg.slice(1), "utf8")) : JSON.parse(arg);
  saida = await pedir("tools/call", { name: acao, arguments: args });
}
// as imagens (screenshot) vão para arquivo; o texto vai para a saída
for (const c of saida?.result?.content || []) if (c.type === "image") {
  const f = process.env.IMAGEM || `pen-${Date.now()}.png`;
  writeFileSync(f, Buffer.from(c.data, "base64")); c.data = `(gravada em ${f})`;
}
console.log(JSON.stringify(saida, null, 1));
console.error(`[${acao}: ${Date.now() - t0} ms]`);
srv.kill();
process.exit(0);
