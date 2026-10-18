/* Protótipo (plano 23, item 1.4): a rolagem narrativa no centro da área principal. Nada do jogo muda: abrir.mjs e
   fotografar.mjs anexam este arquivo e rolagem.css à página, e ele troca só a função global rolagem (app/pagina.js).

   O que entra: a mesma mensagem "rolagem" do motor (ui.rolagem: atributo, cd, d20, mod, total, sucesso). Nada é
   sorteado de novo: os números que piscam no dado enquanto ele gira são enfeite, como já são hoje, e o que pousa é o
   d20 do motor. As parcelas do bônus vêm do estado (heroi.testes[atributo].partes, as mesmas da dica das escolhas) e
   só aparecem se somam o mod da mensagem.

   A sequência, com a duração de hoje (950 ms girando + ritmo(650) no resultado):
   1. o teste: o palco escurece um pouco e o grupo entra no centro (o nome do teste, a dificuldade, o dado, a tirinha);
   2. a rolagem: o dado grande gira e pisca, a tirinha diz a conta e o que é preciso tirar;
   3. o resultado: o dado pousa no d20 do motor, a tirinha fecha a conta e a faixa de resultado aparece
      (Sucesso: inteira, o contorno se fecha; Falha: rasgada no meio, caída; Crítico e Desastre, idem com mais peso);
   4. o grupo desce até a tirinha de sempre no texto, que fica como registro, e só então vem a consequência (a fila de
      mensagens espera esta função terminar, como hoje).
   Pular (tecla ou clique) e o texto instantâneo cortam como hoje; refazendo a página, nada aparece no centro. Na luta,
   a rolagem de sempre. Com movimento reduzido, sem giro, sem deslocamento: o grupo aparece e sai. */
"use strict";

(() => {
  const original = window.rolagem;
  const VARS = ["--sh-ponta-e1", "--sh-ponta-d2", "--sh-meio", "--sh-grao", "--sh-grao-claro", "--sh-texto", "--sh-latao", "--sh-latao-claro"];
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const sinalDe = (n) => (n >= 0 ? "+" : "−");
  // uma espera que o pular corta (a tecla ou o clique que adianta o texto)
  const aguardar = async (ms) => { const f = performance.now() + ms; while (performance.now() < f && !pular) await espera(Math.min(40, f - performance.now())); };
  // o contorno de latão em volta das faixas, com trechos em falta (o pincel que não fechou); na Sucesso ele se completa
  const CONTORNO = `<svg class="rp-contorno" viewBox="0 0 100 20" preserveAspectRatio="none" aria-hidden="true">
    <path class="a" d="M3 3.2 L38 2.6 M46 2.4 L97 3.4 L98.4 10 M98 14 L97 17.2 L61 17.6 M52 17.8 L4 17 L2.4 9"/>
    <path class="b" d="M38 2.6 L46 2.4 M98.4 10 L98 14 M61 17.6 L52 17.8 M2.4 9 L3 3.2"/></svg>`;

  // o que precisa sair no dado (a regra do motor, sistemas/testes.py: 20 sempre passa, 1 sempre falha). Na
  // integração, este número viria pronto do motor na mensagem; aqui o protótipo deriva de cd e mod.
  function preciso(m) {
    const n = m.cd - m.mod;
    if (n <= 2) return "só falha com 1";
    if (n >= 20) return "só passa com 20";
    return `precisa de ${n} ou mais`;
  }
  function partes(m) {
    const t = estado && estado.heroi && estado.heroi.testes && estado.heroi.testes[m.atributo];
    if (!t || !t.partes || t.partes.reduce((s, [, v]) => s + v, 0) !== m.mod) return "";
    return t.partes.map(([r, v]) => `${esc(r)} ${sinalDe(v)}${Math.abs(v)}`).join(" · ");
  }
  function copiarPincel(alvo) {
    const fonte = document.querySelector("#prompt") || document.querySelector("#roda");
    if (!fonte) return;
    const cs = getComputedStyle(fonte);
    VARS.forEach((v) => { const x = cs.getPropertyValue(v); if (x) alvo.style.setProperty(v, x); });
  }
  // o centro: a área principal (#palco, sem as colunas do herói e do mundo); na altura, o meio da cena
  function centro() {
    const p = document.getElementById("palco").getBoundingClientRect(), c = (document.getElementById("cena") || document.getElementById("palco")).getBoundingClientRect();
    return { p, x: p.left + p.width / 2, y: c.top + c.height / 2 };
  }

  window.rolagem = async function rolagemCentral(m) {
    if (replay || instantaneo() || (estado && estado.combate)) return original(m);
    const sinal = sinalDe(m.mod), abs = Math.abs(m.mod);
    // a tirinha de sempre, no texto: guardada (ocupa o lugar, invisível) até o grupo descer até ela
    const caixa = el("div", "rolagem rolando rp-guardada");
    caixa.innerHTML = `<div class="d20">${D20}</div><div class="rol-info"><div class="rol-attr">Teste de ${esc(m.atributo)}</div>
      <div class="rol-conta">d20 ${sinal} ${abs} contra dificuldade <b>${m.cd}</b></div></div><div class="rol-res"></div>`;
    anexar(caixa);

    const { p, x, y } = centro();
    const palco = el("div", "rp-palco");
    copiarPincel(palco);
    const det = partes(m);
    palco.innerHTML = `<div class="rp-veu"></div>
      <div class="rp-grupo">
        <div class="rp-cab"><span class="rp-nome">Teste de ${esc(m.atributo)}</span><span class="rp-cd">Dificuldade <b>${m.cd}</b></span></div>
        <div class="rp-dado d20">${D20}</div>
        <div class="rp-tirinha rp-faixa">${CONTORNO}<span class="rp-conta">d20 <i>${sinal} ${abs}</i></span><span class="rp-precisa">${preciso(m)}</span>
          ${det ? `<span class="rp-partes">${det}</span>` : ""}</div>
        <div class="rp-resultado rp-faixa">${CONTORNO}<b></b></div>
      </div>`;
    const veu = palco.querySelector(".rp-veu");
    Object.assign(veu.style, { left: p.left + "px", top: p.top + "px", width: p.width + "px", height: p.height + "px" });
    const grupo = palco.querySelector(".rp-grupo");
    document.body.appendChild(palco);
    grupo.style.left = Math.round(x - grupo.offsetWidth / 2) + "px";
    grupo.style.top = Math.round(Math.max(8, Math.min(innerHeight - grupo.offsetHeight - 8, y - grupo.offsetHeight / 2))) + "px";
    // o meio do véu (o mais escuro) atrás do grupo
    const gr = grupo.getBoundingClientRect();
    veu.style.setProperty("--cx", `${((gr.left + gr.width / 2 - p.left) / p.width) * 100}%`);
    veu.style.setProperty("--cy", `${((gr.top + gr.height / 2 - p.top) / p.height) * 100}%`);
    palco.classList.add("rp-entra", "rolando");

    // a rolagem: como hoje (o mesmo som, os mesmos 950 ms, pular corta)
    const num = palco.querySelector(".rp-dado text"), numPagina = caixa.querySelector("text");
    Som.tocar("dado");
    const fim = performance.now() + 950;
    while (performance.now() < fim && !pular) { num.textContent = 1 + Math.floor(Math.random() * 20); await espera(60); }

    // o resultado: o d20 do motor
    const critico = m.d20 === 20, desastre = m.d20 === 1, nome = critico ? "Crítico!" : desastre ? "Desastre" : m.sucesso ? "Sucesso" : "Falha";
    const classes = ["pousou", m.sucesso ? "ok" : "falha", ...(critico ? ["critico"] : []), ...(desastre ? ["desastre"] : [])];
    num.textContent = numPagina.textContent = m.d20;
    palco.classList.remove("rolando");
    palco.classList.add(...classes);
    palco.querySelector(".rp-conta").innerHTML = `<b>${m.d20}</b> <i>${sinal} ${abs}</i> = <b>${m.total}</b>`;
    palco.querySelector(".rp-precisa").textContent = `contra ${m.cd}`;
    palco.querySelector(".rp-resultado b").textContent = nome;
    caixa.classList.remove("rolando");
    caixa.classList.add(...classes);
    caixa.querySelector(".rol-conta").innerHTML = `<b>${m.d20}</b> ${sinal} ${abs} = <b>${m.total}</b> contra <b>${m.cd}</b>`;
    caixa.querySelector(".rol-res").textContent = nome;
    historico("h-chip", `▸ ${m.atributo} ${m.total} contra ${m.cd} — ${m.sucesso ? "sucesso" : "falha"} (d20 ${m.d20})`);
    Som.tocar(critico ? "critico" : m.sucesso ? "sucesso" : "falha");

    // o resultado fica à vista o tempo de hoje; o fim dele é a descida até a tirinha do texto
    const resto = ritmo(650), saida = reduzido() ? 0 : Math.min(220, Math.round(resto * 0.34));
    await aguardar(resto - saida);
    if (saida && !pular) {
      const a = grupo.getBoundingClientRect(), b = caixa.getBoundingClientRect();
      const dx = b.left + b.width / 2 - (a.left + a.width / 2), dy = b.top + b.height / 2 - (a.top + a.height / 2);
      const s = Math.max(0.3, Math.min(1, b.width / a.width));
      grupo.animate([{ transform: "none", opacity: 1 }, { transform: `translate(${dx}px, ${dy}px) scale(${s})`, opacity: 0 }],
        { duration: saida, easing: "cubic-bezier(.5,0,.8,.4)", fill: "forwards" });
      veu.animate([{ opacity: 1 }, { opacity: 0 }], { duration: saida, fill: "forwards" });
      setTimeout(() => caixa.classList.remove("rp-guardada"), saida * 0.6);
      await espera(saida);
    }
    caixa.classList.remove("rp-guardada");
    palco.remove();
  };
})();
