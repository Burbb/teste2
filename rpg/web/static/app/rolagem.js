/* A rolagem dos testes de atributo (1.117.0; plano 23, item 1.4; o protótipo aprovado e as alternativas em
   ferramentas/prototipos/hud/rolagem/). Só mostra o que o motor diz na mensagem "rolagem" (sistemas/testes.py, teste):
   atributo, cd (a dificuldade final), d20, mod, total, sucesso e precisa (o menor d20 que passa). Os números que piscam
   no dado enquanto ele gira são enfeite; o que pousa é o d20 do motor. As parcelas do bônus vêm do estado
   (heroi.testes[atributo].partes, as da dica das escolhas) e só aparecem se somam o mod da mensagem.

   Fora da luta, no centro da área principal (#palco, sem as colunas do herói e do mundo), no tempo de sempre (950 ms
   girando + ritmo(650) no resultado), sem clique novo:
   1. o teste: o palco escurece (mais no meio); o nome do teste e a dificuldade;
   2. a rolagem: o dado de sempre, 2×, girando; a tirinha em pincel com "d20 + 2", "precisa de 10 ou mais" e as parcelas;
   3. o resultado: o dado pousa, a conta fecha e a faixa aparece (Sucesso: marfim inteira, o contorno se fecha; Falha:
      carvão rasgada, o texto caído; Crítico e Desastre com mais peso);
   4. o grupo desce até a tirinha no texto, que fica como registro; só então a fila segue para a consequência.
   Pular (tecla ou clique) corta o giro e o resultado. No texto instantâneo, refazendo a página e na luta, só a tirinha
   no texto, como antes. Com movimento reduzido (20-rolagem.css), sem giro nem deslocamento: o grupo aparece e sai. */
"use strict";

// o contorno de latão das faixas, com trechos em falta (o pincel que não fechou); no Sucesso ele se completa (.b)
const ROLAGEM_CONTORNO = `<svg class="rc-contorno" viewBox="0 0 100 20" preserveAspectRatio="none" aria-hidden="true">
  <path class="a" d="M3 3.2 L38 2.6 M46 2.4 L97 3.4 L98.4 10 M98 14 L97 17.2 L61 17.6 M52 17.8 L4 17 L2.4 9"/>
  <path class="b" d="M38 2.6 L46 2.4 M98.4 10 L98 14 M61 17.6 L52 17.8 M2.4 9 L3 3.2"/></svg>`;

const rolagemSinal = (n) => (n >= 0 ? "+" : "−");
// o que precisa sair no dado, pelo número do motor (2: só o 1 falha; 20: só o 20 passa)
function rolagemPrecisa(m) {
  if (m.precisa == null) return "";
  return m.precisa <= 2 ? "só falha com 1" : m.precisa >= 20 ? "só passa com 20" : `precisa de ${m.precisa} ou mais`;
}
function rolagemPartes(m) {
  const t = estado && estado.heroi && estado.heroi.testes && estado.heroi.testes[m.atributo];
  if (!t || !t.partes || t.partes.reduce((s, [, v]) => s + v, 0) !== m.mod) return "";
  return t.partes.map(([r, v]) => `${esc(r)} ${rolagemSinal(v)}${Math.abs(v)}`).join(" · ");
}
// o resultado nos dois lugares (o centro e a tirinha do texto): as classes, a conta, o nome, o som
function rolagemResultado(m) {
  const critico = m.d20 === 20, desastre = m.d20 === 1;
  return { critico, nome: critico ? "Crítico!" : desastre ? "Desastre" : m.sucesso ? "Sucesso" : "Falha",
    classes: ["pousou", m.sucesso ? "ok" : "falha", ...(critico ? ["critico"] : []), ...(desastre ? ["desastre"] : [])] };
}

async function rolagem(m) {
  // o teste que a cena encena (a queda de braço da taverna): o dado espera as mãos se firmarem (Cenas.aguardar), mesmo
  // com o texto adiantado; o adiantar de antes da espera não corta o dado que vem depois dela
  if (!replay && velocidade !== "instantaneo" && window.Cenas && await Cenas.aguardar("rolagem")) pular = false;
  const sinal = rolagemSinal(m.mod), abs = Math.abs(m.mod);
  const centro = !(replay || instantaneo() || (estado && estado.combate));
  // a tirinha no texto; com o centro, guardada (ocupa o lugar, invisível) até o grupo descer até ela
  const caixa = el("div", `rolagem rolando${centro ? " rc-guardada" : ""}`);
  caixa.innerHTML = `<div class="d20">${D20}</div><div class="rol-info"><div class="rol-attr">Teste de ${esc(m.atributo)}</div>
    <div class="rol-conta">d20 ${sinal} ${abs} contra dificuldade <b>${m.cd}</b></div></div><div class="rol-res"></div>`;
  anexar(caixa);
  const numTexto = caixa.querySelector("text");
  const r = rolagemResultado(m);
  const fecharTirinha = () => {
    numTexto.textContent = m.d20;
    caixa.classList.remove("rolando");
    caixa.classList.add(...r.classes);
    caixa.querySelector(".rol-conta").innerHTML = `<b>${m.d20}</b> ${sinal} ${abs} = <b>${m.total}</b> contra <b>${m.cd}</b>`;
    caixa.querySelector(".rol-res").textContent = r.nome;
    historico("h-chip", `▸ ${m.atributo} ${m.total} contra ${m.cd} — ${m.sucesso ? "sucesso" : "falha"} (d20 ${m.d20})`);
  };

  if (!centro) {  // a tirinha sozinha, como antes
    if (!instantaneo()) {
      Som.tocar("dado");
      const fim = performance.now() + 950;
      while (performance.now() < fim && !pular) { numTexto.textContent = 1 + Math.floor(Math.random() * 20); await espera(60); }
    }
    fecharTirinha();
    if (!replay) Som.tocar(r.critico ? "critico" : m.sucesso ? "sucesso" : "falha");
    if (!instantaneo()) await espera(ritmo(650));
    return;
  }

  const p = $("#palco").getBoundingClientRect(), c = ($("#cena") || $("#palco")).getBoundingClientRect();
  const palco = el("div", "rolagem-centro");
  const det = rolagemPartes(m);
  palco.innerHTML = `<div class="rc-veu"></div>
    <div class="rc-grupo">
      <div class="rc-cab"><span class="rc-nome">Teste de ${esc(m.atributo)}</span><span class="rc-cd">Dificuldade <b>${m.cd}</b></span></div>
      <div class="rc-dado d20">${D20}</div>
      <div class="rc-tirinha rc-faixa">${ROLAGEM_CONTORNO}<span class="rc-conta">d20 <i>${sinal} ${abs}</i></span><span class="rc-precisa">${rolagemPrecisa(m)}</span>
        ${det ? `<span class="rc-partes">${det}</span>` : ""}</div>
      <div class="rc-resultado rc-faixa">${ROLAGEM_CONTORNO}<b></b></div>
    </div>`;
  const veu = palco.querySelector(".rc-veu"), grupo = palco.querySelector(".rc-grupo");
  Object.assign(veu.style, { left: p.left + "px", top: p.top + "px", width: p.width + "px", height: p.height + "px" });
  document.body.appendChild(palco);
  // no meio do palco; na altura, o meio da cena. Com uma ação na arte que o dado não deve cobrir (a queda de braço,
  // Cenas.acaoNaArte), o grupo fica logo embaixo da arte (inteiro na janela) e o véu cobre só a página, não a arte.
  const acao = window.Cenas && Cenas.acaoNaArte();
  grupo.style.left = Math.round(p.left + p.width / 2 - grupo.offsetWidth / 2) + "px";
  if (acao) {
    const arte = $("#vista").getBoundingClientRect();
    grupo.style.top = Math.round(Math.max(8, Math.min(arte.bottom + 6, innerHeight - grupo.offsetHeight - 4))) + "px";
    Object.assign(veu.style, { top: Math.round(arte.bottom) + "px", height: Math.max(0, Math.round(p.bottom - arte.bottom)) + "px" });
  } else grupo.style.top = Math.round(Math.max(8, Math.min(innerHeight - grupo.offsetHeight - 8, c.top + c.height / 2 - grupo.offsetHeight / 2))) + "px";
  const gr = grupo.getBoundingClientRect();  // o meio do véu (o mais escuro) atrás do grupo
  veu.style.setProperty("--cx", `${((gr.left + gr.width / 2 - p.left) / p.width) * 100}%`);
  veu.style.setProperty("--cy", acao ? "40%" : `${((gr.top + gr.height / 2 - p.top) / p.height) * 100}%`);
  palco.classList.add("rc-entra", "rolando");

  // a rolagem: o mesmo som e os mesmos 950 ms de sempre; pular corta
  const num = palco.querySelector(".rc-dado text");
  Som.tocar("dado");
  const fim = performance.now() + 950;
  while (performance.now() < fim && !pular) { num.textContent = 1 + Math.floor(Math.random() * 20); await espera(60); }

  // o resultado: o d20 do motor
  num.textContent = m.d20;
  palco.classList.remove("rolando");
  palco.classList.add(...r.classes);
  palco.querySelector(".rc-conta").innerHTML = `<b>${m.d20}</b> <i>${sinal} ${abs}</i> = <b>${m.total}</b>`;
  palco.querySelector(".rc-precisa").textContent = `contra ${m.cd}`;
  palco.querySelector(".rc-resultado b").textContent = r.nome;
  fecharTirinha();
  Som.tocar(r.critico ? "critico" : m.sucesso ? "sucesso" : "falha");

  // o resultado fica à vista o tempo de sempre; o fim dele é a descida até a tirinha (pular corta)
  const resto = ritmo(650), saida = matchMedia("(prefers-reduced-motion: reduce)").matches ? 0 : Math.min(220, Math.round(resto * 0.34));
  for (const f = performance.now() + resto - saida; performance.now() < f && !pular;) await espera(Math.min(40, f - performance.now()));
  if (saida && !pular) {
    const a = grupo.getBoundingClientRect(), b = caixa.getBoundingClientRect();
    const dx = b.left + b.width / 2 - (a.left + a.width / 2), dy = b.top + b.height / 2 - (a.top + a.height / 2);
    const s = Math.max(0.3, Math.min(1, b.width / a.width));
    grupo.animate([{ transform: "none", opacity: 1 }, { transform: `translate(${dx}px, ${dy}px) scale(${s})`, opacity: 0 }],
      { duration: saida, easing: "cubic-bezier(.5,0,.8,.4)", fill: "forwards" });
    veu.animate([{ opacity: 1 }, { opacity: 0 }], { duration: saida, fill: "forwards" });
    setTimeout(() => caixa.classList.remove("rc-guardada"), saida * 0.6);
    await espera(saida);
  }
  caixa.classList.remove("rc-guardada");
  palco.remove();
}
