// PROTÓTIPO de campo livre da etapa 8 (nada no jogo): os números e os kits. Tudo de teste; as regras que usam estes
// números estão em sim.js. Unidades: distância em pixels nativos (o campo é desenhado 1:1 e ampliado inteiro), tempo
// em segundos, empurrão em px/s (a unidade desliza cerca de empurrão/9 px, ver ATRITO_EMPURRAO).
export const VERSAO = "Campo Livre 4";

export const CAMPO = { largura: 960, altura: 560, margem: 8 };
export const ATRITO_EMPURRAO = 9;      // o empurrão perde velocidade a e^(-9t): desliza v/9 px
export const SEMENTE = 20261031;       // a mesma batalha a cada repetição

// Combatentes comuns e as ameaças. `vagas`: quantos inimigos atacam ao mesmo tempo esta unidade (o resto procura
// outra): é o que espalha a multidão em vez de empilhar todos no mesmo alvo.
export const TIPOS = {
  soldado: { nome: "Soldado", papel: "perto", raio: 3.5, vida: 12, vidaAliado: 16, vel: 34, massa: 1, dano: 2, danoAliado: 2.5, alcance: 3,
    preparo: 0.28, recarga: 1.1, vagas: 3 },
  // `busca`: até onde o arqueiro procura alvo quando nada o prende (ele avança até a distância de tiro, `alcance` ×
  // `tiro`, sem passar dela); `posto`: o quanto a retaguarda de um encontro pode sair do posto para atirar.
  arqueiro: { nome: "Arqueiro", papel: "longe", raio: 3.5, vida: 7, vel: 32, massa: 1, dano: 2, alcance: 150,
    ideal: 105, perto: 46, preparo: 0.45, recarga: 1.9, vagas: 3, flecha: 170, busca: 420, tiro: 0.9, posto: 90 },
  // A ameaça que pede atenção: o golpe de machado se anuncia no chão (0,75 s), varre um arco e lança os soldados;
  // é interrompido pelos golpes fortes do herói. Resiste ao empurrão (massa) e ao atordoamento.
  // O inimigo resistente: aguenta um golpe forte (é empurrado e atordoado, não morre); pede dois ou um combo.
  veterano: { nome: "Veterano", papel: "perto", raio: 4, vida: 32, vel: 30, massa: 2, dano: 3, alcance: 3,
    preparo: 0.32, recarga: 1.2, vagas: 3 },
  // `firme`: depois de ter uma preparação interrompida, por quantos segundos um golpe forte não o interrompe de novo
  // (a reação visual continua): nenhuma ameaça fica presa numa sequência de interrupções.
  campeao: { nome: "Campeão", papel: "perto", raio: 6, vida: 220, vel: 30, massa: 6, dano: 6, danoHeroi: 28,
    alcance: 22, abertura: 160, preparo: 0.75, recarga: 2.6, vagas: 7, elite: true, empurrao: 210, firme: 2 },
  // O líder inimigo (Campo Livre 4). Ameaça o herói e o campo. A escolha (`foco`), revista a cada 3 s no mínimo: duela
  // com o herói quando ele está a até 150 px ou o feriu nos últimos 4 s; senão, vai no grupo nosso mais denso a até
  // 170 px (4 ou mais a 40 px uns dos outros; arqueiro conta 1,5); senão, persegue o herói a até 320 px; senão, a tropa
  // mais perto. Repertório: o Machado (arco de 160° anunciado 0,8 s, recarga 1,6 s: 30 no herói, 14 nas tropas; com
  // uma tropa nossa entre ele e o herói, golpeia através dela), o Rodopio (círculo de 46 px anunciado 0,75 s quando 3
  // ou mais dos nossos estão colados nele: 34 no herói, 14 nas tropas), a Arremetida (círculo no caminho do herói ou no
  // meio do grupo, a até 220 px, salto 0,7 s depois: 30 no herói, 14 nas tropas; ao cair, 0,5 s com o machado cravado
  // levando +50%, e o machado seguinte se anuncia em 0,6 s), a Carga (contra o herói ou o grupo; 16 nas tropas;
  // ofegante 0,9 s depois) e a Presença (a até 90 px, os soldados dele atacam mais rápido, são menos empurrados e não se
  // abalam). 14 nas tropas: dois golpes derrubam um soldado nosso, um derruba um arqueiro. Entre duas habilidades, pelo
  // menos 1,5 s. Golpe fraco não o faz cambalear (reage, sem parar); golpe forte interrompe a preparação, e depois ele
  // fica `firme` 2,5 s. Os soldados dele abrem caminho. Derrubado, a tropa a até 150 px foge, a retaguarda deixa o
  // posto e o resto se abala por 3 s.
  lider: { nome: "Harg, o Capitão", papel: "perto", raio: 6.5, vida: 500, vel: 54, massa: 7, dano: 14, danoHeroi: 30,
    alcance: 26, abertura: 160, preparo: 0.8, recarga: 1.6, vagas: 8, elite: true, lider: true, empurrao: 240, firme: 2.5,
    foco: { perto: 150, memoria: 4, minimo: 3, persegue: 320, abates: 200,
      grupo: { alcance: 170, raio: 40, min: 4, arqueiro: 1.5 } }, intervalo: 1.5,
    rodopio: { recarga: 5, primeira: 2, raio: 46, preparo: 0.75, min: 3, dano: 14, danoHeroi: 34, empurrao: 260 },
    arremetida: { recarga: 6, primeira: 3, min: 40, max: 220, preparo: 0.7, adianta: 0.5, voo: 0.45, raio: 30, dano: 14,
      danoHeroi: 30, empurrao: 220, cravado: 0.5, sequencia: 0.6 },
    carga: { recarga: 8, primeira: 5, reunir: 0.8, raioReunir: 70, max: 8, distancia: 150, distanciaMax: 210, vel: 170,
      largura: 10, dano: 16, danoHeroi: 30, empurrao: 230, ofegante: 0.9, vulneravel: 1.5, impeto: 2 },
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
      // O Corte: três golpes seguidos (3, 4 e o arremate de 9, que arremessa) num arco que pega um grupo pequeno. A
      // assistência (`assist`): o golpe vira para o inimigo mais perto da direção do mouse a até `alcance` px (num cone
      // de `cone`° para cada lado) e, se ele está um pouco além do arco, o herói dá um passo de até `estica` px na
      // preparação (nunca para trás, nunca contra a direção em que o jogador anda, nunca através de quem está no meio).
      basico: { nome: "Corte", tecla: "Botão esquerdo", preparo: 0.07, rec: 0.2, raio: 22, abertura: 120, dano: 3,
        danos: [3, 4], empurrao: 25, atordoa: 0.15, mover: 0.6, assist: { alcance: 36, cone: 40, estica: 12 },
        arremate: { cada: 3, janela: 0.9, dano: 9, raio: 28, abertura: 160, empurrao: 160, atordoa: 0.35, pausa: 30,
          tremor: 0.14 } },
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
      // A Faísca: sai para o inimigo mais perto da direção do mouse dentro do alcance (cone de `assist.cone`°) e o
      // persegue, virando no máximo `curva` rad/s; se ele morre no caminho, segue reto no último rumo e acerta só quem
      // tocar até o fim do alcance (não procura outro). Sem ninguém no cone, vai reto para onde o mouse aponta. Quem
      // leva uma Faísca fica com uma Fagulha por 3 s: o próximo golpe de habilidade do Mago nele causa +6 e a consome.
      basico: { nome: "Faísca", tecla: "Botão esquerdo", preparo: 0.05, rec: 0.22, vel: 300, alcance: 175, dano: 4,
        empurrao: 50, atordoa: 0.12, mover: 0.75, assist: { cone: 15 }, curva: 14, fagulha: { duracao: 3, bonus: 6 } },
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
// (ou protege) quem está dentro em vez de cortar o campo. Campo Livre 3: o Avanço de Escudo (anda com as tropas atrás
// de um escudo que barra flechas), o Turbilhão (puxa os comuns para perto e golpeia o monte), a Corrente de Raios (um
// raio que salta de inimigo em inimigo) e o Campo de Gelo (uma região onde os inimigos andam e atacam devagar).
export const VARIANTES = {
  guerreiro: {
    varredura: { sangrenta: { nome: "Varredura Sangrenta", tecla: "Botão direito", preparo: 0.2, rec: 0.22, recarga: 6,
      raio: 32, abertura: 220, dano: 7, empurrao: 30, atordoa: 0, sangra: { duracao: 3, tique: 3 }, pausa: 35,
      pausaPorAbate: 0, pausaMax: 35, tremor: 0.2, tremorPorAbate: 0, tremorMax: 0.2 } },
    investida: {
      grito: { nome: "Grito de Guerra", tecla: "Espaço", preparo: 0.15, rec: 0.15, recarga: 10, raio: 70,
        inspira: 6, ritmo: 0.6, cura: 2, abala: 1.5, raioAbala: 45, tremor: 0.15 },
      // anda a 70% por 2,5 s com o escudo virado para o mouse: barra as flechas que o cruzam, empurra quem está na
      // frente (2 de dano na primeira vez) e os aliados a até 50 px levam metade do dano; outra habilidade o encerra
      escudo: { nome: "Avanço de Escudo", tecla: "Espaço", recarga: 9, escudo: 2.5, mover: 0.7, raio: 30, abertura: 150,
        dano: 2, empurrao: 90, atordoa: 0.3, protege: 50, reducao: 0.5, tremor: 0.1 },
    },
    salto: {
      // prende os pés por 0,35 s puxando os inimigos comuns a até 70 px para perto e, no fim, golpeia o monte
      turbilhao: { nome: "Turbilhão", tecla: "Q", custo: 50, preparo: 0.35, rec: 0.25, puxa: 70, puxaPara: 12,
        raio: 30, dano: 9, empurrao: 70, atordoa: 0.5, pausa: 60, pausaPorAbate: 4, pausaMax: 90, tremor: 0.35,
        tremorPorAbate: 0.02, tremorMax: 0.5 },
    },
  },
  mago: {
    bola: {
      incendiaria: { nome: "Bola Incendiária", tecla: "Botão direito", custo: 30, recarga: 1.5, preparo: 0.18,
        rec: 0.2, alcance: 180, vel: 480, raio: 24, dano: 6, empurrao: 40, atordoa: 0, chao: { duracao: 4, tique: 3,
          raio: 38, repele: true }, pausa: 30, pausaPorAbate: 0, pausaMax: 30, tremor: 0.18, tremorPorAbate: 0,
        tremorMax: 0.18 },
      // o raio sai na direção do mouse (até 170 px, numa faixa de 6 px), pega o primeiro inimigo e salta para o mais
      // perto ainda não atingido (até 48 px), até 12 alvos; cada salto tira 1 do dano (14, 13, 12... no mínimo 7)
      raios: { nome: "Corrente de Raios", tecla: "Botão direito", custo: 16, recarga: 1, preparo: 0.12, rec: 0.2,
        alcance: 170, largura: 6, alvos: 12, salto: 48, dano: 14, queda: 1, danoMin: 7, empurrao: 60, atordoa: 0.25,
        pausa: 35, pausaPorAbate: 4, pausaMax: 70, tremor: 0.2, tremorPorAbate: 0.02, tremorMax: 0.4 },
    },
    muralha: {
      anel: { nome: "Anel de Fogo", tecla: "Q", custo: 45, recarga: 10, alcance: 150, raio: 32, duracao: 5,
        tique: 4, preparo: 0.15, rec: 0.15, tremor: 0.1 },
      // um círculo de gelo no ponto do mouse: 5 de dano e 0,3 s de atordoamento ao surgir; por 5 s, quem está dentro
      // anda a 35% e ataca na metade do ritmo (o Capitão e o campeão, a 60% e a 75%)
      gelo: { nome: "Campo de Gelo", tecla: "Q", custo: 35, recarga: 9, alcance: 170, raio: 44, duracao: 5, dano: 5,
        atordoa: 0.3, lento: 0.35, ritmo: 0.5, lentoElite: 0.6, ritmoElite: 0.75, preparo: 0.2, rec: 0.15,
        tremor: 0.15 },
    },
  },
};

// As ordens das tropas aliadas (teclas 1, 2, 3; no modo de comando, o botão direito). Cada ordem tem uma âncora e uma
// coleira: quem luta perto não se afasta mais que `coleira` px da âncora; quem atira, `coleiraLonge`, e escolhe alvos
// até onde alcança de lá. Acompanhar: a âncora é o herói (os soldados em volta, os arqueiros atrás dele, do lado
// oposto aos inimigos). Defender aqui: a âncora é o ponto (os soldados em volta, os arqueiros atrás). Atacar: sem
// âncora; os soldados vão aos inimigos mais perto e os arqueiros avançam até a distância de tiro. Atacar um alvo (o
// botão direito num inimigo, no modo de comando): todos os selecionados nele; quem luta perto e está trancado por outro
// inimigo luta com ele; o alvo derrubado, fugido ou a mais de `coleiraAlvo` px de onde a ordem foi dada por `perdeAlvo`
// s encerra a ordem, e cada um volta à ordem que tinha. Uma ordem com âncora longe (mais que a coleira + `desloca`)
// faz a tropa ir até lá sem parar para lutar: é como tirar um grupo do caminho de uma ameaça.
export const ORDENS = {
  acompanhar: { nome: "Acompanhar", tecla: "1", coleira: 90, coleiraLonge: 50 },
  atacar: { nome: "Atacar", tecla: "2", coleiraAlvo: 280, perdeAlvo: 2 },
  defender: { nome: "Defender aqui", tecla: "3", coleira: 70, coleiraLonge: 25 },
};
export const DESLOCA = 30;

// Os contingentes do encontro normal (1×): 42 aliados e 94 inimigos em duas levas (≈ 137 com o herói). A segunda leva
// entra pela direita aos 30 s, ou antes, se a primeira cair a 20%: é ela que traz o campeão.
export const CONTINGENTES = {
  normal: { aliados: { soldado: 30, arqueiro: 12 },
    inimigos: { soldado: 28, veterano: 14, arqueiro: 12, estandarte: 1 },
    reforco: { soldado: 20, veterano: 10, arqueiro: 8, campeao: 1 } },
};

// As escalas do exército (escolhidas antes da luta). Os blocos comuns se repetem em alas lado a lado, ao longo da
// frente (na vertical; os blocos da borda de cima ou de baixo, para os lados), a `ALA` px uma da outra, sem sair do
// campo; nos grupos espalhados, cada grupo cresce no próprio lugar. Líder, campeão e porta-estandarte não se
// multiplicam; a vida e o dano de cada um não mudam. Com 4×, as alas de fora (a mais de `BATALHA.alaPerto` do herói)
// começam com a ordem Atacar (lutam na frente delas) e as de perto o acompanham: a linha inteira entra na luta em vez de
// correr toda para ele (Campo Livre 4; na v3 as de fora defendiam e ficavam paradas). 4× é experimental (30, R3).
export const ESCALAS = { 1: { nome: "1× (o encontro normal)" }, 2: { nome: "2×" }, 4: { nome: "4× (experimental)" } };
export const ALA = 130;
export const ESPECIAIS = ["lider", "campeao", "estandarte"];

// Os encontros. A batalha original continua igual (`original`, montada por CONTINGENTES e pelo código de antes); os
// novos são blocos fixos: [tipo, quantos, x, y, colunas, grupo, leva]. Cada grupo acorda no tempo dele (`ativa`, em
// segundos), quando alguém chega a 80 px ou quando um dos seus apanha; `posto` segura o grupo no lugar (a retaguarda
// de arqueiros atira de lá). As levas entram no tempo `t` ou quando a primeira cai a `quando`. `escala: "grupos"`: nas
// escalas maiores, cada grupo cresce no lugar (alas atravessariam os outros grupos).
export const ENCONTROS = {
  original: {
    original: true, nome: "A primeira batalha",
    descricao: "A batalha do Campo Livre 1: a primeira leva espera em formação; a segunda chega pela direita aos 30 s, com o campeão.",
    regra: "Com 20% dos inimigos de pé, depois da segunda leva, o resto foge.",
  },
  espalhados: {
    nome: "Grupos espalhados", escala: "grupos",
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
    descricao: "Uma linha de soldados protege Harg, o Capitão, e a guarda dele; atrás, uma retaguarda de 22 arqueiros. Harg enfrenta você quando você está perto ou o fere; longe, vai para as suas tropas (os arqueiros primeiro). Ele salta no círculo vermelho marcado no chão, gira o machado quando o cercam e carrega pela faixa; um golpe forte na preparação desfaz cada um, e logo depois ele fica firme por 2,5 s.",
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
  // A horda (Campo Livre 4): ondas de gente frágil, ao estilo musou, para o herói derrubar em quantidade. Nas escalas
  // 2× e 4×, cada onda também se multiplica.
  horda: {
    nome: "A horda",
    descricao: "Você e as tropas no meio do campo; a cada 9 s, uma onda de 60 soldados comuns (um veterano a cada dez) chega por um lado (leste, norte, oeste, sul), durante 100 s.",
    regra: "Enquanto vierem ondas, ninguém foge. Depois da última, com 20% dos inimigos de pé, o resto foge. Nas escalas 2× e 4×, as ondas também dobram ou quadruplicam (no máximo 1200 combatentes no campo).",
    heroi: [480, 280],
    aliados: [["soldado", 30, 486, 280, 5], ["arqueiro", 12, 480, 200, 6]],
    grupos: { leste: { ativa: 2 } },
    inimigos: [["soldado", 40, 820, 280, 4, "leste"], ["veterano", 4, 790, 280, 1, "leste"]],
    levas: [],
    ondas: { cada: 9, n: 60, ate: 100, lados: ["oeste", "norte", "leste", "sul"] },
  },
};

// A horda: a tecla H (para testar batalhas maiores) e as ondas do encontro "A horda". `n`: a quantidade padrão da tecla;
// `distancia`: a que distância do herói, na direção do mouse; `limite`: o máximo de combatentes no campo (medido:
// ~660 a 60 qps; ~1400 a 53 qps com quadros de 33 ms, por isso 1200).
export const HORDA = { n: 60, distancia: 220, limite: 1200, veteranos: 0.1 };

export const BATALHA = {
  reacaoAviso: 0.3,  // as nossas tropas saem de uma área anunciada de ameaça depois de 0,3 s dela no chão
  alaPerto: 100,      // com 4×, as alas a até 100 px do herói (ao longo da frente) o acompanham; as outras atacam
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
