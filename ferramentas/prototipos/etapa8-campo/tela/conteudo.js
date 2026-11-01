// PROTÓTIPO de campo livre da etapa 8 (nada no jogo): os números e os kits. Tudo de teste; as regras que usam estes
// números estão em sim.js. Unidades: distância em pixels nativos (o campo é desenhado 1:1 e ampliado inteiro), tempo
// em segundos, empurrão em px/s (a unidade desliza cerca de empurrão/9 px, ver ATRITO_EMPURRAO).
export const VERSAO = "Campo Livre 2";

export const CAMPO = { largura: 960, altura: 560, margem: 8 };
export const ATRITO_EMPURRAO = 9;      // o empurrão perde velocidade a e^(-9t): desliza v/9 px
export const SEMENTE = 20261031;       // a mesma batalha a cada repetição

// Combatentes comuns e as ameaças. `vagas`: quantos inimigos atacam ao mesmo tempo esta unidade (o resto procura
// outra): é o que espalha a multidão em vez de empilhar todos no mesmo alvo.
export const TIPOS = {
  soldado: { nome: "Soldado", papel: "perto", raio: 3.5, vida: 12, vidaAliado: 16, vel: 34, massa: 1, dano: 2, danoAliado: 2.5, alcance: 3,
    preparo: 0.28, recarga: 1.1, vagas: 3 },
  arqueiro: { nome: "Arqueiro", papel: "longe", raio: 3.5, vida: 7, vel: 32, massa: 1, dano: 2, alcance: 150,
    ideal: 105, perto: 46, preparo: 0.45, recarga: 1.9, vagas: 3, flecha: 170 },
  // A ameaça que pede atenção: o golpe de machado se anuncia no chão (0,75 s), varre um arco e lança os soldados;
  // é interrompido pelos golpes fortes do herói. Resiste ao empurrão (massa) e ao atordoamento.
  // O inimigo resistente: aguenta um golpe forte (é empurrado e atordoado, não morre); pede dois ou um combo.
  veterano: { nome: "Veterano", papel: "perto", raio: 4, vida: 32, vel: 30, massa: 2, dano: 3, alcance: 3,
    preparo: 0.32, recarga: 1.2, vagas: 3 },
  campeao: { nome: "Campeão", papel: "perto", raio: 6, vida: 220, vel: 30, massa: 6, dano: 6, danoHeroi: 28,
    alcance: 22, abertura: 160, preparo: 0.75, recarga: 2.6, vagas: 7, elite: true, empurrao: 210 },
  // O líder inimigo (os encontros novos): o golpe de machado do campeão, a Carga (reúne até 10 soldados por 1 s, com a
  // faixa marcada no chão, e atravessa 150 px atropelando quem estiver nela; um golpe forte na reunião a desfaz; depois
  // da carga, fica ofegante 1,2 s e leva +50% de dano) e a Presença (a até 90 px, os soldados dele atacam mais rápido,
  // são menos empurrados e não se abalam). Derrubado, a tropa a até 150 px foge do campo e o resto se abala por 3 s.
  lider: { nome: "Harg, o Capitão", papel: "perto", raio: 6.5, vida: 380, vel: 32, massa: 7, dano: 8, danoHeroi: 26,
    alcance: 22, abertura: 150, preparo: 0.7, recarga: 2.4, vagas: 8, elite: true, lider: true, empurrao: 220,
    carga: { recarga: 11, primeira: 6, reunir: 1, raioReunir: 70, max: 10, distancia: 150, vel: 150, largura: 10,
      dano: 14, danoHeroi: 22, empurrao: 230, ofegante: 1.2, vulneravel: 1.5, impeto: 2 },
    presenca: 90, presencaRitmo: 0.75, presencaFirmeza: 0.5, derrota: { foge: 150, abala: 3 } },
  // A outra: fica atrás da linha e fortalece quem está na aura (+50% de dano, ataca 25% mais rápido); derrubado,
  // abala os inimigos em volta por 2 s (recuam, não atacam).
  estandarte: { nome: "Porta-estandarte", papel: "apoio", raio: 3.5, vida: 30, vel: 30, massa: 1.5, dano: 2,
    alcance: 3, preparo: 0.3, recarga: 1.2, vagas: 3, elite: true, aura: 70, auraDano: 1.3, auraRitmo: 0.85,
    abala: 120, abalaTempo: 2 },
};

// Os heróis. `vagas` 7: até sete soldados batem nele de uma vez (cercado, ele sente).
export const HEROIS = {
  guerreiro: {
    nome: "Guerreiro", raio: 5, vida: 260, vel: 72, massa: 6, vagas: 7, critico: { chance: 0.1, mult: 1.5 },
    recurso: { nome: "Fúria", max: 100, inicial: 0, regen: 0, porAcerto: 1, porAbate: 1.5 },
    curaPorAbate: 0.5,
    kit: {
      basico: { nome: "Corte", tecla: "Botão esquerdo", preparo: 0.07, rec: 0.2, raio: 22, abertura: 110, dano: 3,
        empurrao: 25, atordoa: 0.15, mover: 0.6,
        arremate: { cada: 3, janela: 0.9, dano: 8, raio: 26, abertura: 130, empurrao: 150, atordoa: 0.35, pausa: 25,
          tremor: 0.12 } },
      varredura: { nome: "Varredura", tecla: "Botão direito", preparo: 0.2, rec: 0.28, recarga: 6, raio: 32,
        abertura: 220, dano: 13, empurrao: 190, atordoa: 0.5, pausa: 45, pausaPorAbate: 8, pausaMax: 90,
        tremor: 0.26, tremorPorAbate: 0.03, tremorMax: 0.5 },
      investida: { nome: "Investida", tecla: "Espaço", recarga: 6, distancia: 100, duracao: 0.2, largura: 9, dano: 4,
        empurrao: 170, atordoa: 0.45, fimRaio: 20, fimEmpurrao: 120, tremor: 0.18 },
      salto: { nome: "Salto Esmagador", tecla: "Q", custo: 100, alcance: 130, preparo: 0.12, voo: 0.42, rec: 0.25,
        raio: 44, dano: 24, empurrao: 240, atordoa: 0.7, pausa: 100, tremor: 0.7 },
    },
  },
  mago: {
    nome: "Mago", raio: 4.5, vida: 170, vel: 68, massa: 4, vagas: 7, critico: { chance: 0.1, mult: 1.5 },
    recurso: { nome: "Mana", max: 100, inicial: 100, regen: 7 },
    kit: {
      basico: { nome: "Faísca", tecla: "Botão esquerdo", preparo: 0.05, rec: 0.22, vel: 300, alcance: 175, dano: 4,
        empurrao: 50, atordoa: 0.12, mover: 0.75 },
      bola: { nome: "Bola de Fogo", tecla: "Botão direito", custo: 30, recarga: 1.5, preparo: 0.18, rec: 0.2,
        alcance: 180, vel: 480, raio: 24, dano: 13, empurrao: 200, atordoa: 0.5, chao: { duracao: 2, tique: 3 },
        pausa: 50, pausaPorAbate: 6, pausaMax: 85, tremor: 0.3, tremorPorAbate: 0.03, tremorMax: 0.5 },
      piscar: { nome: "Piscar", tecla: "Espaço", recarga: 6, distancia: 95, raio: 28, dano: 3, empurrao: 200,
        atordoa: 0.6, invul: 0.15, tremor: 0.15 },
      muralha: { nome: "Muralha de Fogo", tecla: "Q", custo: 40, recarga: 9, alcance: 150, comprimento: 96,
        duracao: 5, tique: 7, preparo: 0.15, rec: 0.15, tremor: 0.1 },
    },
  },
};

// As versões de habilidade escolhidas antes da luta (a original continua como opção). Cada uma muda o uso, não só os
// números: a Sangrenta não empurra (os inimigos ficam onde as tropas os seguram) e mata depois; o Grito troca a
// mobilidade por apoio às tropas; a Incendiária troca o arremesso por um chão que os inimigos contornam; o Anel prende
// (ou protege) quem está dentro em vez de cortar o campo.
export const VARIANTES = {
  guerreiro: {
    varredura: { sangrenta: { nome: "Varredura Sangrenta", tecla: "Botão direito", preparo: 0.2, rec: 0.22, recarga: 6,
      raio: 32, abertura: 220, dano: 7, empurrao: 30, atordoa: 0, sangra: { duracao: 3, tique: 3 }, pausa: 35,
      pausaPorAbate: 0, pausaMax: 35, tremor: 0.2, tremorPorAbate: 0, tremorMax: 0.2 } },
    investida: { grito: { nome: "Grito de Guerra", tecla: "Espaço", preparo: 0.15, rec: 0.15, recarga: 10, raio: 70,
      inspira: 6, ritmo: 0.6, cura: 2, abala: 1.5, raioAbala: 45, tremor: 0.15 } },
  },
  mago: {
    bola: { incendiaria: { nome: "Bola Incendiária", tecla: "Botão direito", custo: 30, recarga: 1.5, preparo: 0.18,
      rec: 0.2, alcance: 180, vel: 480, raio: 24, dano: 6, empurrao: 40, atordoa: 0, chao: { duracao: 4, tique: 3,
        raio: 38, repele: true }, pausa: 30, pausaPorAbate: 0, pausaMax: 30, tremor: 0.18, tremorPorAbate: 0,
      tremorMax: 0.18 } },
    muralha: { anel: { nome: "Anel de Fogo", tecla: "Q", custo: 45, recarga: 10, alcance: 150, raio: 32, duracao: 5,
      tique: 4, preparo: 0.15, rec: 0.15, tremor: 0.1 } },
  },
};

// As ordens coletivas das tropas aliadas (teclas 1, 2, 3).
export const ORDENS = {
  acompanhar: { nome: "Acompanhar", tecla: "1", engaja: 75, engajaHeroi: 100 },
  atacar: { nome: "Atacar", tecla: "2" },
  defender: { nome: "Defender aqui", tecla: "3", engaja: 85, coleira: 120 },
};

// Os contingentes fixos. `normal`: 42 aliados e 94 inimigos em duas levas (≈ 137 com o herói); `maior`: o dobro
// (≈ 270), o teste de leitura e desempenho. A segunda leva entra pela direita aos 30 s, ou antes, se a primeira
// cair a 20%: é ela que traz o campeão.
export const CONTINGENTES = {
  normal: { aliados: { soldado: 30, arqueiro: 12 },
    inimigos: { soldado: 28, veterano: 14, arqueiro: 12, estandarte: 1 },
    reforco: { soldado: 20, veterano: 10, arqueiro: 8, campeao: 1 } },
  maior: { aliados: { soldado: 60, arqueiro: 24 },
    inimigos: { soldado: 56, veterano: 28, arqueiro: 24, estandarte: 2 },
    reforco: { soldado: 40, veterano: 20, arqueiro: 16, campeao: 2 } },
};

// Os encontros. A batalha original continua igual (`original`, montada por CONTINGENTES e pelo código de antes); os
// novos são blocos fixos: [tipo, quantos, x, y, colunas, grupo, leva]. Cada grupo acorda no tempo dele (`ativa`, em
// segundos), quando alguém chega a 80 px ou quando um dos seus apanha; `posto` segura o grupo no lugar (a retaguarda
// de arqueiros atira de lá). As levas entram no tempo `t` ou quando a primeira cai a `quando`. Na opção "Maior", cada
// bloco comum dobra; líder, campeão e porta-estandarte não.
export const ENCONTROS = {
  original: {
    original: true, nome: "A primeira batalha",
    descricao: "A batalha do Campo Livre 1: a primeira leva espera em formação; a segunda chega pela direita aos 30 s, com o campeão.",
    regra: "Com 20% dos inimigos de pé, depois da segunda leva, o resto foge.",
  },
  espalhados: {
    nome: "Grupos espalhados",
    descricao: "Sete grupos pequenos, longe uns dos outros, acordam em tempos diferentes (ou quando alguém chega perto). Cada área pega menos gente; quem decide é onde você está.",
    regra: "Aos 35 s, mais um grupo chega pelo norte. Com 20% dos inimigos de pé, o resto foge.",
    heroi: [300, 280],
    aliados: [["soldado", 30, 262, 280, 4], ["arqueiro", 12, 200, 280, 2]],
    grupos: { a: { ativa: 6 }, b: { ativa: 10 }, c: { ativa: 4, posto: true }, d: { ativa: 14 }, e: { ativa: 8, posto: true },
      f: { ativa: 18 }, g: { ativa: 22 }, norte: {} },
    inimigos: [["soldado", 8, 560, 140, 3, "a"], ["veterano", 6, 610, 420, 2, "b"], ["arqueiro", 6, 720, 90, 2, "c"],
      ["soldado", 10, 770, 300, 3, "d"], ["arqueiro", 6, 860, 470, 2, "e"], ["soldado", 8, 430, 490, 3, "f"],
      ["estandarte", 1, 880, 210, 1, "g"], ["soldado", 6, 860, 180, 2, "g"],
      ["soldado", 12, 480, 14, 6, "norte", 1], ["veterano", 4, 520, 14, 2, "norte", 1]],
    levas: [{ id: 1, t: 35, quando: 0.15, x: 480, y: 14, aviso: "Mais um grupo chega pelo norte." }],
  },
  duasFrentes: {
    nome: "Duas frentes",
    descricao: "Você e as tropas no meio do campo; um exército vem do oeste, outro do leste, e o campeão chega depois pelo sul. Divida: uma parte segura um lado enquanto você resolve o outro.",
    regra: "O campeão chega pelo sul aos 25 s. Com 20% dos inimigos de pé, o resto foge.",
    heroi: [480, 280],
    aliados: [["soldado", 30, 486, 280, 5], ["arqueiro", 12, 480, 200, 6]],
    grupos: { oeste: { ativa: 3 }, leste: { ativa: 3 }, sul: {} },
    inimigos: [["soldado", 16, 70, 280, 3, "oeste"], ["veterano", 6, 104, 280, 1, "oeste"], ["arqueiro", 4, 40, 280, 1, "oeste"],
      ["soldado", 16, 890, 280, 3, "leste"], ["veterano", 4, 856, 280, 1, "leste"], ["arqueiro", 6, 924, 280, 1, "leste"],
      ["estandarte", 1, 910, 230, 1, "leste"],
      ["campeao", 1, 480, 540, 1, "sul", 1], ["soldado", 10, 480, 548, 5, "sul", 1]],
    levas: [{ id: 1, t: 25, quando: 0.3, x: 480, y: 546, aviso: "O campeão chega pelo sul." }],
  },
  capitao: {
    nome: "O Capitão e a retaguarda",
    descricao: "Uma linha de soldados protege Harg, o Capitão, e a guarda dele; atrás, uma retaguarda de 22 arqueiros atira do posto. Harg reúne soldados e carrega pela faixa marcada no chão; um golpe forte na reunião desfaz a carga.",
    regra: "Enquanto Harg estiver de pé, ninguém foge. Se ele cair, a tropa a até 150 px dele foge do campo e o resto se abala por 3 s; a batalha continua até restarem 20%, e esses fogem. Aos 40 s chega um reforço pela direita.",
    heroi: [300, 280],
    aliados: [["soldado", 30, 262, 280, 4], ["arqueiro", 12, 200, 280, 2]],
    grupos: { frente: { ativa: 3 }, guarda: { ativa: 5 }, retaguarda: { ativa: 0, posto: true }, reforco: {} },
    inimigos: [["soldado", 18, 600, 280, 2, "frente"], ["veterano", 8, 626, 280, 1, "frente"],
      ["lider", 1, 700, 280, 1, "guarda"], ["soldado", 10, 724, 280, 2, "guarda"],
      ["arqueiro", 22, 830, 280, 3, "retaguarda"],
      ["soldado", 12, 940, 160, 2, "reforco", 1]],
    levas: [{ id: 1, t: 40, quando: 0.15, x: 940, y: 160, aviso: "Um reforço do Capitão chega pela direita." }],
  },
};

export const BATALHA = {
  formacao: 2.5,      // os inimigos esperam em formação antes de avançar
  fugaQuando: 0.2,    // com 20% ou menos dos inimigos de pé, o resto foge
  fugaDura: 2.5,      // depois disso, a vitória
  derrotaDura: 1.6,
  reforcoT: 30,       // a segunda leva chega aos 30 s
  reforcoQuando: 0.2, // ou quando restam 20% da primeira
  reavaliar: [0.3, 0.6],   // de quanto em quanto tempo cada unidade reavalia o alvo (sorteado no intervalo)
  custoFila: 22,      // quanto "pesa", na escolha do alvo, cada atacante que já está nele
  danoNoHeroi: 1.5,   // as tropas batem 50% mais forte no herói (ele precisa sentir quando fica cercado)
};

// O que limita o impacto, para muitos golpes juntos não travarem a tela nem a câmera.
export const IMPACTO = {
  pausaMax: 100,          // nenhuma pausa de impacto passa disto (ms)
  pausaRefratario: 150,   // depois de uma pausa, outra só depois de 150 ms
  tremorQueda: 1.8,       // o "trauma" da câmera cai 1,8 por segundo
  tremorMaxPx: 6,         // deslocamento máximo em px nativos, com intensidade 100% e trauma 1
};
