/* A Encruzilhada: os dois caminhos da classe lado a lado, para comparar antes de escolher. Tudo vem pronto do motor
   (especializacao.py: a prévia é calculada numa cópia do herói já especializado); a tela só desenha. "Olhar de perto"
   responde à opção do motor (meta `caminho`) e não escolhe nada; a confirmação vem nas opções de baixo. */
"use strict";

(() => {
  const { h, S } = Telas;

  function sinal(v) { return (v > 0 ? "+" : "−") + String(Math.abs(v)).replace(".", ","); }

  // As linhas do Grimório (dano com a faixa, ou um efeito), curtas: o detalhe completo fica no Grimório depois.
  function linha(l) {
    return l.tipo === "dano"
      ? `<li><span>${h(l.rotulo)}</span> <b>${l.min}–${l.max}</b> <small>média ${l.medio} · crítico ${l.critico} em ${l.chance_critico}%</small></li>`
      : `<li>${Realce.texto(l.texto)}</li>`;
  }

  function habilidade(x) {
    const quando = x.agora ? "agora" : `nível ${x.nivel}`;
    return `<li class="esp-hab${x.agora ? "" : " futura"}"><span class="esp-hab-icone">${S(x.icone, 2)}</span>
      <div><b>${h(x.nome)}</b> <small>${quando} · ${x.custo} ${h(x.recurso.toLowerCase())}${x.flechas ? ` · ${Texto.plural(x.flechas, "flecha")}` : ""}</small>
      <div class="esp-desc">${Realce.texto(x.desc)}</div></div></li>`;
  }

  function cartao(p, d) {
    const foco = d.foco === p.id, apagado = d.foco && !foco;
    const attrs = p.atributos.map((a) => `<li><span>${h(a.stat)}</span><b class="${a.delta > 0 ? "melhor" : "pior"}">${sinal(a.delta)}</b><small>${a.antes} → ${a.depois}</small></li>`).join("");
    const detalhe = `<details class="esp-detalhe"${foco ? " open" : ""}><summary>Números das habilidades e talentos do caminho</summary>
        <p class="esp-ref">${h(p.referencia)}</p>
        ${p.habilidades.map((x) => `<div class="esp-num"><b>${h(x.nome)}</b> <small>${x.agora ? "agora" : `nível ${x.nivel}`}</small><ul>${x.linhas.map(linha).join("")}</ul></div>`).join("")}
        ${p.animais.length ? `<div class="esp-num"><b>Os animais</b> <small>no seu nível</small><ul>${p.animais.map((a) => `<li><span>${h(a.nome)}</span> <b>vida ${a.max_hp} · ataque ${String(Math.round(a.atk * 10) / 10).replace(".", ",")}</b> <small>${h(a.desc)}</small></li>`).join("")}</ul></div>` : ""}
        <div class="esp-num"><b>Talentos do caminho</b><ul>${p.talentos.map((t) => `<li><span>${h(t.nome)}</span> <small>nível ${t.nivel} · até ${t.max}</small> ${Realce.texto(t.desc)}</li>`).join("")}</ul></div>
      </details>`;
    return `<div class="cartao esp-caminho${foco ? " foco" : ""}${apagado ? " apagado" : ""}">
      <div class="cab"><div><b>${h(p.nome)}</b><span class="sub">${h(p.estilo)}</span></div></div>
      <div class="esp-secao"><div class="esp-titulo">Atributos</div><ul class="esp-attrs">${attrs}</ul>
        ${p.por_nivel.length ? `<div class="esp-pequeno">Por nível, a mais: ${h(p.por_nivel.join(", "))}</div>` : ""}</div>
      <div class="esp-secao"><div class="esp-titulo">Habilidades</div><ul class="esp-habs">${p.habilidades.map(habilidade).join("")}</ul></div>
      ${p.beneficios.length ? `<div class="esp-secao"><div class="esp-titulo bom">O que o caminho dá</div><ul class="esp-lista mais">${p.beneficios.map((b) => `<li>${Realce.texto(b)}</li>`).join("")}</ul></div>` : ""}
      ${p.limites.length ? `<div class="esp-secao"><div class="esp-titulo ruim">Limites</div><ul class="esp-lista menos">${p.limites.map((b) => `<li>${Realce.texto(b)}</li>`).join("")}</ul></div>` : ""}
      ${foco ? `<button type="button" class="botao-janela esp-confirmar" data-confirmar="${h(p.id)}">Confirmar: ${h(p.nome)}</button>` : ""}
      ${detalhe}
      ${d.foco ? "" : `<button type="button" class="botao-janela esp-olhar" data-caminho="${h(p.id)}">Olhar de perto</button>`}
    </div>`;
  }

  function especializacao(d) {
    const aviso = d.foco ? `Confirme nas opções abaixo, ou use Voltar (Esc) para comparar de novo. ${d.definitiva}`
      : `Compare os dois caminhos. Olhar um de perto não o escolhe. ${d.definitiva}`;
    return `<div class="tela especializacao"><div class="esp-aviso">${h(aviso)}</div>
      <div class="esp-cartas">${d.caminhos.map((p) => cartao(p, d)).join("")}</div></div>`;
  }

  function ligar(raiz) {
    raiz.querySelectorAll("[data-caminho]").forEach((b) => b.addEventListener("click", (ev) => {
      ev.stopPropagation();
      App.acao({ caminho: b.dataset.caminho }, "escolha");
    }));
    raiz.querySelectorAll("[data-confirmar]").forEach((b) => b.addEventListener("click", (ev) => {
      ev.stopPropagation();
      App.acao({ confirmar: b.dataset.confirmar }, "escolha");
    }));
  }

  Telas.registrar("especializacao", especializacao, { ligar });
})();
