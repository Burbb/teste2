// A guerra do Campo Livre 9 sem tela, com o jogador automático: o resultado, quanto tempo cada herói inimigo durou, o
// que mais tirou da sua vida (por quem bateu), o General (quanto durou, o que acertou), as ondas sorteadas.
// Uso: node ferramentas/guerra9.mjs [encontros] [heróis] [níveis] [sorteios]
//      node ferramentas/guerra9.mjs guerra9,treino9 guerreiro,mago forte,medio 1,2,3,4
const T = new URL("../tela/", import.meta.url).href;
const S = await import(T + "sim.js"), R = await import(T + "robo.js"), C9 = await import(T + "campo9.js");
const [encArg = "guerra9,treino9", heroiArg = "guerreiro,mago", nivelArg = "forte,medio", sortArg = "1,2,3,4"] = process.argv.slice(2);
const r1 = (v) => Math.round(v * 10) / 10;

for (const enc of encArg.split(",")) for (const heroi of heroiArg.split(",")) for (const nivel of nivelArg.split(",")) {
  const linhas = [];
  let vitorias = 0;
  for (const sort of sortArg.split(",").map(Number)) {
    const m = S.criarMundo({ heroi, encontro: enc, sorteio: sort });
    const rb = R.criarRobo({ nivel }), ent = S.entradaVazia();
    const porFonte = {}, entrou = {}, vida = {};
    let controle = 0, maiorControle = 0, seguido = 0;
    while (m.fase !== "fim" && m.t < 400) {
      R.pensar(rb, m, ent);
      S.passo(m, ent);
      for (const e of m.eventos) {
        if (e.tipo === "heroiAtingido") { const k = `${e.fonte || "?"}${e.hab ? ":" + e.hab : ""}`; porFonte[k] = (porFonte[k] || 0) + e.valor; }
        if (e.tipo === "heroi9Entra" || e.tipo === "general9Entra") entrou[e.nome] = m.t;
        if (e.tipo === "heroi9Caiu") vida[e.nome] = r1(m.t - entrou[e.nome]);
      }
      m.eventos.length = 0;
      const h = m.heroi, preso = h.atordoado > 0 || h.imobAte > m.t;
      if (preso) { controle += S.PASSO; seguido += S.PASSO; maiorControle = Math.max(maiorControle, seguido); } else seguido = 0;
    }
    if (m.resultado === "vitoria") vitorias++;
    const z = C9.resumo9(m), st = m.stats;
    const fontes = Object.entries(porFonte).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([k, v]) => `${k} ${Math.round(v)}`).join(", ");
    linhas.push(`  sorteio ${sort}: ${m.resultado} ${Math.round(m.t)} s, herói ${Math.max(0, Math.round(m.heroi.vida))}/${m.heroi.vidaMax}` +
      ` | heróis: ${z.herois.map((e) => `${e.nome.split(",")[0]} (${e.variacoes.join("+")}) ${e.nome in vida ? vida[e.nome] + " s" : e.entrou ? "de pé" : "não veio"}`).join("; ")}` +
      ` | General: ${z.general}${vida["O General"] ? ` caiu em ${vida["O General"]} s` : ""}, acertou o herói ${st.generalNoHeroi || 0}×, quebras ${st.generalQuebras || 0}, derrubou ${st.generalMortos || 0}` +
      ` | o que tirou a sua vida: ${fontes}` +
      ` | controle ${r1(controle)} s (seguido ${r1(maiorControle)}) | barris ${st.barris || 0}, cargas ${st.cargas || 0}, veneno ${Math.round(st.veneno || 0)}, vampiro ${Math.round(st.vampirico || 0)}` +
      ` | ondas: ${z.pelotoes.join(", ") || "-"}`);
  }
  console.log(`${enc} ${heroi} ${nivel}: ${vitorias}/${linhas.length} vitórias`);
  for (const l of linhas) console.log(l);
}
