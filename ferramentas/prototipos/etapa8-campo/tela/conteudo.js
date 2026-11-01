// PROTÓTIPO de campo livre da etapa 8 (nada no jogo): os números e os kits. Tudo de teste; as regras que usam estes
// números estão em sim.js. Unidades: distância em pixels nativos (o campo é desenhado 1:1 e ampliado inteiro), tempo
// em segundos, empurrão em px/s (a unidade desliza cerca de empurrão/9 px, ver ATRITO_EMPURRAO).
export const VERSAO = "Campo Livre 7";

export const CAMPO = { largura: 960, altura: 560, margem: 8 };
export const ATRITO_EMPURRAO = 9;      // o empurrão perde velocidade a e^(-9t): desliza v/9 px
export const SEMENTE = 20261031;       // a mesma batalha a cada repetição

// Combatentes comuns e as ameaças. `vagas`: quantos inimigos atacam ao mesmo tempo esta unidade (o resto procura
// outra): é o que espalha a multidão em vez de empilhar todos no mesmo alvo.
export const TIPOS = {
  soldado: { nome: "Soldado", papel: "perto", raio: 3.5, vida: 12, vidaAliado: 16, vel: 34, massa: 1, dano: 2, danoAliado: 2.5, alcance: 3,
    preparo: 0.28, recarga: 1.1, vagas: 3, estica: 10, compromete: 0.6 },
  // `busca`: até onde o arqueiro procura alvo quando nada o prende (ele avança até a distância de tiro, `alcance` ×
  // `tiro`, sem passar dela); `posto`: o quanto a retaguarda de um encontro pode sair do posto para atirar.
  arqueiro: { nome: "Arqueiro", papel: "longe", raio: 3.5, vida: 7, vel: 32, massa: 1, dano: 2, alcance: 150,
    ideal: 105, perto: 46, preparo: 0.45, recarga: 1.9, vagas: 3, flecha: 170, busca: 420, tiro: 0.9, posto: 90 },
  // A ameaça que pede atenção: o golpe de machado se anuncia no chão (0,75 s), varre um arco e lança os soldados;
  // é interrompido pelos golpes fortes do herói. Resiste ao empurrão (massa) e ao atordoamento.
  // O inimigo resistente: aguenta um golpe forte (é empurrado e atordoado, não morre); pede dois ou um combo.
  veterano: { nome: "Veterano", papel: "perto", raio: 4, vida: 32, vel: 30, massa: 2, dano: 3, alcance: 3,
    preparo: 0.32, recarga: 1.2, vagas: 3, estica: 10, compromete: 0.6 },
  // `firme`: depois de ter uma preparação interrompida, por quantos segundos um golpe forte não o interrompe de novo
  // (a reação visual continua): nenhuma ameaça fica presa numa sequência de interrupções.
  campeao: { nome: "Campeão", papel: "perto", raio: 6, vida: 220, vel: 30, massa: 6, dano: 6, danoHeroi: 28,
    alcance: 22, abertura: 160, preparo: 0.75, recarga: 2.6, vagas: 7, elite: true, empurrao: 210, firme: 2, estica: 14,
    compromete: 0.6 },
  // O líder inimigo (Campo Livre 4). Ameaça o herói e o campo. A escolha (`foco`), revista a cada 3 s no mínimo: duela
  // com o herói quando ele está a até 150 px ou o feriu nos últimos 4 s; senão, vai no grupo nosso mais denso a até
  // 170 px (4 ou mais a 40 px uns dos outros; arqueiro conta 1,5); senão, persegue o herói a até 320 px; senão, a tropa
  // mais perto. Repertório: o Machado (arco de 160° anunciado 0,8 s, recarga 1,6 s: 24 no herói, 14 nas tropas; com
  // uma tropa nossa entre ele e o herói, golpeia através dela), o Rodopio (círculo de 46 px anunciado 0,75 s quando 3
  // ou mais dos nossos estão colados nele: 34 no herói, 14 nas tropas), a Arremetida (círculo no caminho do herói ou no
  // meio do grupo, a até 220 px, salto 0,7 s depois: 30 no herói, 14 nas tropas; ao cair, 0,5 s com o machado cravado
  // levando +50%, e o machado seguinte se anuncia em 0,6 s), a Carga (contra o herói ou o grupo; 16 nas tropas;
  // ofegante 0,9 s depois) e a Presença (a até 90 px, os soldados dele atacam mais rápido, são menos empurrados e não se
  // abalam). 14 nas tropas: dois golpes derrubam um soldado nosso, um derruba um arqueiro. Entre duas habilidades, pelo
  // menos 1,5 s. Golpe fraco não o faz cambalear (reage, sem parar); golpe forte interrompe a preparação, e depois ele
  // fica `firme` 2,5 s. Os soldados dele abrem caminho. Derrubado, a tropa a até 150 px foge, a retaguarda deixa o
  // posto e o resto se abala por 3 s.
  lider: { nome: "Harg, o Capitão", papel: "perto", raio: 6.5, vida: 900, estica: 22, compromete: 0.6, vel: 54, massa: 7, dano: 14, danoHeroi: 24,
    alcance: 26, abertura: 160, preparo: 0.8, recarga: 1.6, vagas: 8, elite: true, lider: true, empurrao: 240, firme: 2.5,
    foco: { perto: 150, memoria: 4, minimo: 3, persegue: 320, abates: 200,
      grupo: { alcance: 170, raio: 40, min: 4, arqueiro: 1.5 } }, intervalo: 1.5,
    rodopio: { recarga: 5, primeira: 2, raio: 46, preparo: 0.75, min: 3, dano: 14, danoHeroi: 34, empurrao: 260 },
    arremetida: { recarga: 6, primeira: 3, min: 40, max: 220, preparo: 0.7, adianta: 0.5, voo: 0.45, raio: 30, dano: 14,
      danoHeroi: 30, empurrao: 220, cravado: 0.5, sequencia: 0.6, vooRapido: 0.32, cravadoLongo: 0.7 },
    carga: { recarga: 8, primeira: 5, reunir: 0.8, raioReunir: 70, max: 8, distancia: 150, distanciaMax: 210, vel: 170,
      largura: 10, dano: 16, danoHeroi: 30, empurrao: 230, ofegante: 0.9, vulneravel: 1.5, impeto: 2 },
    presenca: 90, presencaRitmo: 0.75, presencaFirmeza: 0.5, derrota: { foge: 150, abala: 3 }, heroiInimigo: true,
    // Campo Livre 6 (campo6.ajustarLider): a Investida Curta, a Fúria e o Rodopio logo depois da Arremetida
    // (a Investida Curta só a partir de 120 px e a cada 7 s: com 90 px e 4 s, o jogador automático forte perdia o duelo sozinho)
    dash: { vel: 300, dura: 0.28, min: 120, max: 220, recarga: 7 }, furia: { vida: 0.35, dura: 8, ritmo: 1.4 }, combo: true,
    // Campo Livre 7 (campo7.js), nos encontros com Morel e Odette. A Investida Curta em três tempos: a preparação (ele
    // se abaixa e a faixa aparece no chão: `preparo` s, a direção fica marcada), a execução (`vel` px/s em linha reta,
    // sem corrigir: para no primeiro que atinge, na parede ou ao fim do `alcance`) e a recuperação (`recupera` s parado,
    // levando +50% de dano). Atinge: dano, empurra e interrompe a preparação de quem for herói. A Arremetida voa mais
    // rápido (`vooRapido`) e fica cravada mais tempo (`cravadoLongo`).
    investida7: { preparo: 0.35, vel: 520, alcance: 190, min: 70, max: 190, recupera: 0.55, recarga: 6, dano: 12, danoHeroi: 20,
      empurrao: 230, largura: 9 },
    // O Brado de Desafio (a provocação contra você): a preparação se anuncia num anel de `raio` px por `preparo` s; quem
    // estiver dentro e à vista quando ele brada fica provocado por `dura` s (com a proteção contra repetição).
    brado: { raio: 130, preparo: 0.45, dura: 2.5, recarga: 15 },
    focoIA: { base: { heroi: 30, morel: 8, odette: 16, tropas: 6 }, tempo: 10, pressao: 0.9, apoio: 0.5, ferido: 25, isolado: 12,
      concentracao: 3.5, oportunidade: 12, inercia: 22, ruido: 10, minimo: 2, revisao: [0.8, 1.2], protege: 0.8 } },
  // A outra: fica atrás da linha e fortalece quem está na aura (+50% de dano, ataca 25% mais rápido); derrubado,
  // abala os inimigos em volta por 2 s (recuam, não atacam).
  // ---- Campo Livre 6: as tropas avançadas (campo6.js). Mudam o confronto, não só a vida.
  // A cavalaria: chega rápido (64), carrega em linha a 165 px/s atropelando (7; 12 no herói), passa 46 px do ponto e
  // precisa se reposicionar (1,8 s, 90 px para trás) antes da próxima carga (4,5 s). Empina 0,35 s antes de carregar.
  // Bater num pesado (massa 5 ou mais) encerra a carga e a deixa atordoada 0,8 s. Parada, luta mal (dano 3).
  cavaleiro: { nome: "Cavaleiro", papel: "perto", especial: true, raio: 5, vida: 34, vidaAliado: 38, vel: 64, massa: 4, dano: 3,
    alcance: 3, preparo: 0.25, recarga: 1, vagas: 4, estica: 8, compromete: 0.6,
    carga: { vel: 165, min: 55, max: 240, passa: 46, dano: 7, danoHeroi: 12, empurrao: 170, atordoa: 0.45, recarga: 4.5, recua: 90,
      reposiciona: 1.8, prepara: 0.35, barrado: 0.8, derruba: 0.45 } },
  // A infantaria pesada: lenta (24), aguenta (56) e segura a linha: o golpe que vem da frente (do lado para onde ela
  // olha) causa metade; empurra pouco (massa 5) e para a carga da cavalaria. De lado ou por trás, cai como os outros.
  pesado: { nome: "Infantaria pesada", papel: "perto", raio: 4.5, vida: 56, vidaAliado: 64, vel: 24, massa: 5, dano: 4, alcance: 3,
    preparo: 0.4, recarga: 1.4, vagas: 4, estica: 6, compromete: 0.6, escudoFrente: 0.5,
    // Campo Livre 7: a Escudada, num herói ou numa ameaça colada na frente dele: empurra e deixa lento (não atordoa)
    escudada: { recarga: 6, alcance: 9, dano: 3, empurrao: 150, lento: { fator: 0.4, dura: 1.5 } } },
  // O mago de batalha: frágil (16), fica a até 140 px com visão, atrás da própria linha; a Bola de Batalha cai no ponto
  // que pega mais gente, anunciada 0,9 s no chão (6; 16 no herói; empurra); a cada 9 s, se três ou mais dos seus estão
  // lutando a até 60 px, põe neles um escudo que absorve 8 por 6 s.
  magoBatalha: { nome: "Mago de batalha", papel: "longe", especial: true, raio: 3.5, vida: 16, vidaAliado: 20, vel: 30, massa: 1, dano: 1,
    alcance: 140, ideal: 110, perto: 52, preparo: 0.4, recarga: 4.2, vagas: 3, flecha: 170, busca: 420, tiro: 0.85, posto: 90,
    bola: { nome: "bolaBatalha", raio: 22, preparo: 0.9, dano: 6, danoHeroi: 16, empurrao: 130, atordoa: 0.3, cor: "fogo",
      lento: { fator: 0.3, dura: 2 } },
    escudo: { raio: 60, absorve: 8, dura: 6, recarga: 9 } },
  // ---- Morel e Odette, autônomos (campo6.js): semi-heróis da comitiva, com mais vida e habilidades próprias.
  morel: { nome: "Morel", papel: "perto", especial: true, companheiro: true, elite: true, raio: 5.5, vida: 240, vel: 58, massa: 6,
    dano: 7, alcance: 4, preparo: 0.25, recarga: 0.8, vagas: 6, estica: 10, compromete: 0.6, escudoFrente: 0.6, coleira: 150,
    golpeEscudo: { raio: 26, abertura: 150, dano: 9, empurrao: 210, atordoa: 0.6, recarga: 4, min: 3 },
    provocar: { raio: 80, dura: 4, recarga: 12 },
    // Campo Livre 7: o Desafio, a provocação num herói inimigo que pressiona você ou Odette (a IA espera esse momento):
    // o herói inimigo passa a mirar Morel por `dura` s; Morel ergue o escudo e leva `reducao` do dano nesse tempo.
    desafio: { alcance: 110, dura: 3, recarga: 15, reducao: 0.75, vidaMin: 0.35 } },
  odette: { nome: "Odette", papel: "longe", especial: true, companheiro: true, elite: true, raio: 4.5, vida: 160, vel: 54, massa: 3,
    dano: 2, alcance: 120, ideal: 100, perto: 40, preparo: 0.3, recarga: 1.2, vagas: 4, busca: 300, tiro: 0.9, posto: 80, atras: 42,
    prece: { cura: 42, alcance: 150, recarga: 6, min: 30 }, bencao: { raio: 50, cura: 6, recarga: 9, min: 4, minFalta: 4 },
    clarao: { raio: 40, atordoa: 1.4, dano: 4, recarga: 8, min: 2 }, luz: { alcance: 130, vel: 260, dano: 5, recarga: 1.1, cor: "luz" } },
  // ---- Ardis, a Feiticeira de Guerra: o segundo herói inimigo (campo6.ardis). De longe e sempre em movimento.
  ardis: { nome: "Ardis, a Feiticeira de Guerra", papel: "longe", especial: true, elite: true, heroiInimigo: true, raio: 5, vida: 600,
    vel: 56, massa: 4, dano: 4, alcance: 170, ideal: 125, perto: 50, preparo: 0.4, recarga: 1.2, vagas: 6, busca: 400, tiro: 0.9,
    posto: 100, firme: 2, reacao: 0.3, primeiras: { colunaCd: 3, correnteCd: 5, passoCd: 0, barreiraCd: 0, dardoCd: 0.5 },
    dardo: { alcance: 190, vel: 240, dano: 6, danoHeroi: 11, recarga: 1.1, cor: "arcano" },
    coluna: { nome: "coluna", alcance: 230, raio: 32, preparo: 0.9, dano: 14, danoHeroi: 26, empurrao: 200, atordoa: 0.4, recarga: 5.5, cor: "fogo" },
    corrente: { preparo: 0.5, salto: 42, alvos: 6, dano: 8, danoHeroi: 14, recarga: 7 },
    passo: { distancia: 130, recarga: 6 }, barreira: { absorve: 60, dura: 4, recarga: 20 },
    // Campo Livre 7: o Grilhão Arcano (as mãos brilham `preparo` s, o projétil sai devagar e pode ser evitado): imobiliza
    // quem acerta por `dura` s (não anda nem usa a mobilidade; ataca e lança no lugar)
    grilhao: { alcance: 170, preparo: 0.45, vel: 230, dura: 1, recarga: 9, dano: 4, cor: "grilhao" },
    focoIA: { base: { heroi: 24, morel: 2, odette: 22, tropas: 14 }, tempo: 6, pressao: 0.7, apoio: 0.8, ferido: 20, isolado: 8,
      concentracao: 4.5, oportunidade: 10, inercia: 20, ruido: 10, minimo: 2, revisao: [0.9, 1.3], protege: 0 } },
  estandarte: { nome: "Porta-estandarte", papel: "apoio", raio: 3.5, vida: 30, vel: 30, massa: 1.5, dano: 2,
    alcance: 3, preparo: 0.3, recarga: 1.2, vagas: 3, elite: true, aura: 70, auraDano: 1.3, auraRitmo: 0.85,
    abala: 120, abalaTempo: 2 },
};

// Os heróis (Campo Livre 5). Cada um tem um ataque principal fixo (botão esquerdo, segurar repete), uma mobilidade fixa
// (Espaço) e quatro espaços equipáveis antes da luta: três habilidades comuns (botão direito, Q, E) e uma ultimate (F).
// O recurso limita o abuso concentrado, não o fluxo: regenera rápido e começa cheio; o principal e a mobilidade não
// custam nada; as comuns custam 16 a 35 e têm recarga própria; a ultimate não custa recurso, só espera a recarga
// longa (pronta aos 8 s de luta). `vagas` 7: até sete soldados batem nele de uma vez.
export const HEROIS = {
  guerreiro: {
    nome: "Guerreiro", raio: 5, vida: 260, vel: 72, massa: 6, vagas: 7, critico: { chance: 0.1, mult: 1.5 },
    recurso: { nome: "Fúria", max: 100, inicial: 100, regen: 16, porAcerto: 1 },
    curaPorAbate: 0.5, principal: "varredura", mobilidade: "investida",
  },
  mago: {
    nome: "Mago", raio: 4.5, vida: 170, vel: 68, massa: 4, vagas: 7, critico: { chance: 0.1, mult: 1.5 },
    recurso: { nome: "Mana", max: 100, inicial: 100, regen: 22 },
    principal: "bola", mobilidade: "piscar",
  },
};

// As marcas: propriedades compartilhadas entre habilidades (e, no futuro, itens). Um talento vale para as habilidades
// de uma marca ("o dano direto de habilidades de gelo..."), sem citar cada uma: uma habilidade ou um item novo com a
// marca entra na regra sozinho.
export const MARCAS = {
  fogo: "Fogo", gelo: "Gelo", raio: "Raio", arcano: "Arcano", sangue: "Sangue", impacto: "Impacto", corte: "Corte",
};

// Os tipos de dano, para as regras que reagem a eles (os talentos e, no futuro, os itens):
// `direto`: o efeito principal de uma habilidade (a área, o arco, o projétil, a onda, o pouso, a explosão da Lança
// Estilhaçante); `continuo`: os tiques (o chão em chamas, a Muralha, o Anel, a Nevasca, o Sangramento); `secundario`:
// as explosões que os talentos provocam (o Estilhaçar, a Brasa, a Explosão de Sangue). Cada lançamento de uma
// habilidade tem um número próprio (`lanc`): "outro lançamento da mesma habilidade" é outro número.
export const CADEIA = { maxPorGolpe: 30 };

// O catálogo das habilidades. `tipo`: principal, mobilidade, comum ou ultimate. `marcas`: as propriedades. `ia`: como
// o jogador automático a usa (só para os testes e as medições). Os números das regras estão aqui; sim.js as aplica.
export const HABILIDADES = {
  guerreiro: {
    // o ataque principal: o arco largo contra grupos, com a aproximação assistida (até `avanca` px na preparação, em
    // direção ao inimigo mais perto da mira, dentro de `assist.alcance` e do cone; fora disso, golpeia para onde aponta)
    varredura: { nome: "Varredura", tipo: "principal", marcas: ["corte", "impacto"], preparo: 0.16, rec: 0.2, recarga: 1,
      raio: 32, abertura: 220, dano: 13, empurrao: 190, atordoa: 0.5, assist: { alcance: 64, cone: 40 }, avanca: 32,
      pausa: 40, pausaPorAbate: 6, pausaMax: 80, tremor: 0.24, tremorPorAbate: 0.03, tremorMax: 0.45 },
    investida: { nome: "Investida", tipo: "mobilidade", marcas: ["impacto"], recarga: 4, distancia: 100, duracao: 0.2,
      largura: 9, dano: 4, empurrao: 170, atordoa: 0.45, fimRaio: 20, fimEmpurrao: 120, tremor: 0.18 },
    salto: { nome: "Salto Esmagador", tipo: "comum", marcas: ["impacto"], custo: 35, recarga: 6, alcance: 130, preparo: 0.12,
      voo: 0.42, rec: 0.25, raio: 44, dano: 24, empurrao: 240, atordoa: 0.7, pausa: 100, tremor: 0.7,
      ia: { usa: "grupo", min: 6 } },
    turbilhao: { nome: "Turbilhão", tipo: "comum", marcas: ["impacto"], custo: 30, recarga: 7, preparo: 0.35, rec: 0.25,
      puxa: 70, puxaPara: 12, raio: 30, dano: 9, empurrao: 70, atordoa: 0.5, pausa: 60, pausaPorAbate: 4, pausaMax: 90,
      tremor: 0.35, tremorPorAbate: 0.02, tremorMax: 0.5, ia: { usa: "perto", raio: 70, min: 8 } },
    // atravessar uma linha: uma onda que corre `comprimento` px pelo chão, a `vel` px/s, e pega cada inimigo a até
    // `largura` px dela uma vez, jogando-os para os lados
    sismico: { nome: "Golpe Sísmico", tipo: "comum", marcas: ["impacto"], custo: 22, recarga: 5, preparo: 0.18, rec: 0.2,
      comprimento: 170, largura: 14, vel: 420, dano: 12, empurrao: 170, atordoa: 0.45, tremor: 0.3,
      ia: { usa: "linha", min: 5 } },
    corteSangrento: { nome: "Corte Sangrento", tipo: "comum", marcas: ["corte", "sangue"], custo: 18, recarga: 4,
      preparo: 0.14, rec: 0.2, raio: 34, abertura: 200, dano: 6, acumulos: 2, empurrao: 40, atordoa: 0, pausa: 35,
      tremor: 0.2, ia: { usa: "perto", raio: 32, min: 4 } },
    // detonar os marcados: cada inimigo com Sangramento a até `raio` px leva `porAcumulo` × os acúmulos (dano direto)
    // e explode num círculo de `explosao.raio` px, causando `explosao.porAcumulo` × os acúmulos aos outros (secundário)
    ruptura: { nome: "Ruptura", tipo: "comum", marcas: ["sangue"], custo: 25, recarga: 7, preparo: 0.2, rec: 0.2, raio: 80,
      porAcumulo: 7, explosao: { raio: 22, porAcumulo: 3 }, tremor: 0.35, ia: { usa: "sangue", min: 5 } },
    grito: { nome: "Grito de Guerra", tipo: "comum", marcas: [], custo: 20, recarga: 10, preparo: 0.15, rec: 0.15, raio: 70,
      inspira: 6, ritmo: 0.6, cura: 2, abala: 1.5, raioAbala: 45, tremor: 0.15, ia: { usa: "aliados", min: 6 } },
    escudo: { nome: "Avanço de Escudo", tipo: "comum", marcas: ["impacto"], custo: 20, recarga: 9, escudo: 2.5, mover: 0.7,
      raio: 30, abertura: 150, dano: 2, empurrao: 90, atordoa: 0.3, protege: 50, reducao: 0.5, tremor: 0.1,
      ia: { usa: "arqueiros", min: 4 } },
    furia: { nome: "Fúria Desenfreada", tipo: "ultimate", marcas: [], recarga: 30, primeira: 8, preparo: 0.15, rec: 0.1,
      duracao: 6, recargaPrincipal: 0.35, raioExtra: 8, curaPorAbate: 1.5, tremor: 0.3, ia: { usa: "perto", raio: 50, min: 8 } },
    // três anéis que se abrem em volta do herói: cada inimigo é pego uma vez, pelo primeiro anel que o alcança
    terremoto: { nome: "Terremoto", tipo: "ultimate", marcas: ["impacto"], recarga: 30, primeira: 8, preparo: 0.25, rec: 0.3,
      aneis: [50, 95, 140], intervalo: 0.22, dano: 18, empurrao: 230, atordoa: 0.7, pausa: 90, tremor: 0.6,
      ia: { usa: "perto", raio: 120, min: 15 } },
  },
  mago: {
    bola: { nome: "Bola de Fogo", tipo: "principal", marcas: ["fogo"], preparo: 0.14, rec: 0.18, recarga: 1, alcance: 190,
      vel: 480, raio: 26, dano: 13, empurrao: 200, atordoa: 0.5, chao: { duracao: 2, tique: 3 }, pausa: 50,
      pausaPorAbate: 6, pausaMax: 85, tremor: 0.3, tremorPorAbate: 0.03, tremorMax: 0.5 },
    piscar: { nome: "Piscar", tipo: "mobilidade", marcas: ["arcano"], recarga: 5, distancia: 95, raio: 28, dano: 3,
      empurrao: 200, atordoa: 0.6, invul: 0.15, tremor: 0.15 },
    // atravessar uma linha: atravessa todos os inimigos no caminho (cada um uma vez) até `alcance` px
    lanca: { nome: "Lança de Gelo", tipo: "comum", marcas: ["gelo"], custo: 16, recarga: 2.5, preparo: 0.12, rec: 0.15,
      alcance: 220, vel: 420, largura: 4, dano: 11, empurrao: 60, atordoa: 0.25, explosao: { raio: 30, dano: 14 },
      tremor: 0.12, ia: { usa: "linha", min: 3 } },
    raios: { nome: "Corrente de Raios", tipo: "comum", marcas: ["raio"], custo: 16, recarga: 3, preparo: 0.12, rec: 0.2,
      alcance: 170, largura: 6, alvos: 12, salto: 48, dano: 14, queda: 1, danoMin: 7, empurrao: 60, atordoa: 0.25,
      pausa: 35, pausaPorAbate: 4, pausaMax: 70, tremor: 0.2, tremorPorAbate: 0.02, tremorMax: 0.4, ia: { usa: "grupo", min: 3 } },
    muralha: { nome: "Muralha de Fogo", tipo: "comum", marcas: ["fogo"], custo: 28, recarga: 8, alcance: 150,
      comprimento: 96, duracao: 5, tique: 7, preparo: 0.15, rec: 0.15, tremor: 0.1, ia: { usa: "parede", min: 5 } },
    anel: { nome: "Anel de Fogo", tipo: "comum", marcas: ["fogo"], custo: 30, recarga: 9, alcance: 150, raio: 32,
      duracao: 5, tique: 4, preparo: 0.15, rec: 0.15, tremor: 0.1, ia: { usa: "grupo", min: 8 } },
    campoGelo: { nome: "Campo de Gelo", tipo: "comum", marcas: ["gelo"], custo: 28, recarga: 8, alcance: 170, raio: 44,
      duracao: 5, dano: 5, atordoa: 0.3, lento: 0.35, ritmo: 0.5, lentoElite: 0.6, ritmoElite: 0.75, preparo: 0.2,
      rec: 0.15, tremor: 0.15, ia: { usa: "grupo", min: 6 } },
    // reunir: por `duracao` s puxa para o centro os inimigos a até `raio` px (o campeão e o Capitão, a 30%) e, no fim,
    // implode: `implosao.dano` num círculo de `implosao.raio` px
    vortice: { nome: "Vórtice", tipo: "comum", marcas: ["arcano"], custo: 30, recarga: 8, alcance: 170, raio: 60,
      duracao: 1.4, puxaPara: 10, preparo: 0.15, rec: 0.15, implosao: { raio: 34, dano: 16, empurrao: 60, atordoa: 0.4 },
      tremor: 0.35, ia: { usa: "grupo", min: 8 } },
    // detonações em cadeia: marca com Brasa por `brasa.duracao` s quem está no círculo (e causa `dano`); quem morre com
    // Brasa explode num círculo de `brasa.raio` px, causando `brasa.dano` aos outros (dano secundário)
    ignicao: { nome: "Ignição", tipo: "comum", marcas: ["fogo"], custo: 24, recarga: 7, alcance: 170, raio: 50, dano: 4,
      preparo: 0.15, rec: 0.15, brasa: { duracao: 6, raio: 28, dano: 10, empurrao: 120 }, tremor: 0.15,
      ia: { usa: "grupo", min: 8 } },
    // `n` meteoros, um a cada `intervalo` s, em pontos sorteados a até `area` px do ponto escolhido; cada um marca o
    // círculo `aviso` s antes de cair
    meteoros: { nome: "Chuva de Meteoros", tipo: "ultimate", marcas: ["fogo"], recarga: 30, primeira: 8, preparo: 0.2,
      rec: 0.2, alcance: 200, area: 80, n: 7, intervalo: 0.35, aviso: 0.6, raio: 28, dano: 22, empurrao: 240, atordoa: 0.6,
      chao: { duracao: 2, tique: 3 }, pausa: 60, tremor: 0.45, ia: { usa: "grupo", min: 15 } },
    nevasca: { nome: "Nevasca", tipo: "ultimate", marcas: ["gelo"], recarga: 30, primeira: 8, preparo: 0.2, rec: 0.2,
      alcance: 180, raio: 95, duracao: 6, dano: 8, atordoa: 0.3, tique: 2, lento: 0.4, ritmo: 0.6, lentoElite: 0.7,
      ritmoElite: 0.8, tremor: 0.3, ia: { usa: "grupo", min: 15 } },
  },
};

// Os talentos: um orçamento de `ORCAMENTO` pontos por herói, redistribuídos à vontade antes da luta. `requer`: a
// habilidade que precisa estar equipada (sem ela, o talento não pode ser escolhido). `tipo`: transformação (muda o
// comportamento de uma habilidade), compartilhado (vale para uma marca ou um tipo de dano), interação (liga efeitos de
// habilidades diferentes) ou ajuste. As regras estão em sim.js (`tem(h, id)`); os textos, aqui.
export const ORCAMENTO = 7;
export const TALENTOS = {
  mago: {
    lancaEstilhacante: { nome: "Lança Estilhaçante", custo: 2, tipo: "transformação", requer: "lanca",
      texto: "A Lança de Gelo deixa de atravessar: explode no primeiro inimigo que atinge, ou no fim do alcance, e causa 14 de dano num círculo de 30 px (dano direto da Lança em todos)." },
    frioCortante: { nome: "Frio Cortante", custo: 2, tipo: "compartilhado", marca: "gelo", chance: 0.35, duracao: 2,
      eliteCongela: 0.5, enregela: 3, enregeladoLento: 0.6,
      texto: "O dano direto de habilidades de gelo tem 35% de chance de congelar o inimigo por 2 s: ele não anda nem ataca. O campeão e o Capitão ficam congelados 0,5 s e depois enregelados por 3 s (andam a 60%)." },
    estilhacar: { nome: "Estilhaçar", custo: 3, tipo: "interação", bonus: 8, raio: 28, dano: 10, profundidade: 2,
      texto: "Um inimigo congelado ou enregelado que leva dano direto de outro lançamento (de outra habilidade ou da mesma, menos o lançamento que o congelou) se estilhaça: perde o gelo, leva +8 e explode num círculo de 28 px, causando 10 aos outros (dano secundário). A explosão pode estilhaçar outros congelados, até 2 explosões em sequência e 30 por golpe. Dano contínuo não estilhaça." },
    brasaViva: { nome: "Brasa Viva", custo: 2, tipo: "interação", requer: "ignicao", profundidade: 3,
      texto: "Quem é atingido pela explosão de uma Brasa também fica com Brasa: as explosões encadeiam, até 3 em sequência e 30 por golpe." },
    fogoAlastrado: { nome: "Fogo Alastrado", custo: 1, tipo: "ajuste", duracao: 2, raio: 1.25,
      texto: "O chão em chamas da Bola de Fogo fica 2 s a mais e 25% maior." },
    vorticeDenso: { nome: "Vórtice Denso", custo: 2, tipo: "ajuste", requer: "vortice", duracao: 0.6, dano: 10,
      texto: "O Vórtice puxa por 0,6 s a mais e a implosão causa +10." },
    menteRapida: { nome: "Mente Rápida", custo: 1, tipo: "ajuste", recarga: 0.85,
      texto: "As recargas das habilidades comuns ficam 15% menores." },
  },
  guerreiro: {
    hemorragia: { nome: "Hemorragia", custo: 2, tipo: "compartilhado", acumulos: 1,
      texto: "A Varredura aplica 1 acúmulo de Sangramento em quem atinge." },
    explosaoSangue: { nome: "Explosão de Sangue", custo: 3, tipo: "interação", raio: 26, porAcumulo: 3, profundidade: 3,
      texto: "Um inimigo que morre com Sangramento explode num círculo de 26 px: 3 por acúmulo nos outros (dano secundário) e 1 acúmulo de Sangramento em cada um. As explosões encadeiam até 3 em sequência e 30 por golpe." },
    arrasto: { nome: "Arrasto", custo: 2, tipo: "transformação",
      texto: "A Investida arrasta os inimigos comuns que atinge: eles vão junto até o fim e caem amontoados na sua frente, cada um com 1 acúmulo de Sangramento." },
    sedeSangue: { nome: "Sede de Sangue", custo: 1, tipo: "interação", furia: 3, investida: 0.3,
      texto: "Derrubar um inimigo com Sangramento devolve 3 de Fúria e 0,3 s da recarga da Investida." },
    bracoLargo: { nome: "Braço Largo", custo: 1, tipo: "ajuste", raio: 6, abertura: 20,
      texto: "A Varredura alcança 6 px a mais e abre 20° a mais." },
    tremorResidual: { nome: "Tremor Residual", custo: 2, tipo: "transformação", requer: "salto", duracao: 3, raio: 44, tique: 3,
      texto: "O Salto Esmagador deixa o chão rachado por 3 s onde caiu: quem está nele leva 3 a cada 0,5 s e anda a 50%." },
  },
};

// O Sangramento em acúmulos: cada acúmulo causa `tique` a cada 0,5 s por `duracao` s; um acúmulo novo renova a
// duração; no máximo `max`.
export const SANGUE = { tique: 2, duracao: 3, max: 5 };

// As montagens prontas (atalhos; tudo continua editável na escolha).
export const MONTAGENS = {
  mago: {
    "Gelo que estilhaça": { comuns: ["lanca", "campoGelo", "raios"], ultimate: "nevasca",
      talentos: ["lancaEstilhacante", "frioCortante", "estilhacar"] },
    "Fogo em cadeia": { comuns: ["ignicao", "vortice", "muralha"], ultimate: "meteoros",
      talentos: ["brasaViva", "vorticeDenso", "fogoAlastrado", "menteRapida"] },
  },
  guerreiro: {
    "Sangria": { comuns: ["corteSangrento", "ruptura", "sismico"], ultimate: "terremoto",
      talentos: ["hemorragia", "explosaoSangue", "arrasto"] },
    "Impacto": { comuns: ["salto", "turbilhao", "sismico"], ultimate: "furia",
      talentos: ["tremorResidual", "bracoLargo", "hemorragia", "sedeSangue"] },
  },
};
export const MONTAGEM_PADRAO = { mago: "Gelo que estilhaça", guerreiro: "Sangria" };

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
export const ESPECIAIS = ["lider", "campeao", "estandarte", "ardis"];

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
  // ---- Campo Livre 6: os encontros novos (com Morel e Odette ao seu lado e a composição escolhida dos dois lados)
  vila: {
    nome: "A vila: a horda e a linha", cenario: "vila", companheiros: true, composicao: true,
    descricao: "O exército da vila forma na estrada, diante do portão; ondas de soldados frágeis saem pelo portão, pela brecha, pela estrada do norte e pelo sul. As casas e a muralha barram flechas e magias.",
    regra: "Ondas a cada 12 s até os 96 s; depois da última, com 20% dos inimigos de pé, o resto foge.",
    heroi: [170, 276], linhaAliada: [214, 276], exercito: { x: 640, y: 276, grupo: "linha" },
    grupos: { linha: { ativa: 5 }, portao: { ativa: 8 } },
    inimigos: [["pesado", 6, 772, 276, 1, "portao"]],
    levas: [],
    ondas: { cada: 12, primeira: 10, n: 36, ate: 96, lados: ["portao", "norte", "brecha", "sul"],
      pontos: { portao: [900, 276], norte: [485, 20], brecha: [900, 428], sul: [614, 540] } },
  },
  carga: {
    nome: "A carga de cavalaria", cenario: "aberto", companheiros: true, composicao: true, escala: "grupos",
    descricao: "Campo aberto. Duas alas de cavalaria inimiga carregam pelos flancos enquanto a infantaria avança pelo centro; aos 30 s, outra carga vem do norte. A infantaria pesada segura a carga; os cavaleiros que passam precisam dar a volta.",
    regra: "Aos 30 s, mais uma ala chega pelo norte. Com 20% dos inimigos de pé, o resto foge.",
    heroi: [230, 280], linhaAliada: [270, 280], exercito: { x: 640, y: 280, grupo: "centro" },
    grupos: { centro: { ativa: 6 }, alaNorte: { ativa: 2 }, alaSul: { ativa: 4 }, norte: {} },
    inimigos: [["cavaleiro", 16, 820, 110, 4, "alaNorte"], ["cavaleiro", 16, 820, 450, 4, "alaSul"],
      ["cavaleiro", 18, 480, 16, 6, "norte", 1]],
    levas: [{ id: 1, t: 30, quando: 0.3, x: 480, y: 16, aviso: "Outra ala de cavalaria carrega pelo norte." }],
  },
  // Campo Livre 7: a amostra de arte, jogável. O mesmo conteúdo nas três aparências (F8 troca) e nas duas escalas do
  // seu herói (F9); as regras não mudam entre elas.
  amostra: {
    nome: "O portão da povoação", cenario: "povoado", companheiros: true,
    descricao: "Um trecho de uma povoação fortificada: a muralha com o portão, uma casa do lado de dentro, árvores do lado de fora. Harg defende o portão com uma amostra de cada tropa (infantaria, arqueiros, cavalaria e pesados). F8 troca a aparência e F9 a escala do seu herói, no meio da luta, sem mudar as regras.",
    regra: "Enquanto Harg estiver de pé, ninguém foge. Aos 40 s, reforços saem pelo portão.",
    heroi: [400, 280],
    aliados: [["soldado", 10, 356, 280, 3], ["arqueiro", 6, 318, 280, 2], ["pesado", 4, 378, 244, 2], ["cavaleiro", 4, 344, 330, 2]],
    grupos: { frente: { ativa: 4 }, portao: { ativa: 6 }, reforco: {} },
    inimigos: [["soldado", 12, 498, 280, 3, "frente"], ["arqueiro", 6, 528, 206, 2, "frente"], ["cavaleiro", 4, 500, 372, 2, "frente"],
      ["pesado", 4, 592, 280, 2, "portao"], ["lider", 1, 624, 300, 1, "portao"], ["soldado", 16, 720, 280, 4, "reforco", 1]],
    levas: [{ id: 1, t: 40, quando: 0.3, x: 720, y: 280, aviso: "Reforços saem pelo portão." }],
  },
  herois: {
    nome: "Harg e Ardis", cenario: "vila", companheiros: true, composicao: true,
    descricao: "Harg, o Capitão, e Ardis, a Feiticeira de Guerra, lutam juntos diante do portão, com a tropa deles. Harg mergulha em você e nas suas tropas; Ardis bombardeia os grupos, some quando você chega perto e Harg vem protegê-la.",
    regra: "Enquanto Harg ou Ardis estiverem de pé, ninguém foge. Aos 45 s, reforços saem pelo portão e pela brecha.",
    heroi: [170, 276], linhaAliada: [214, 276], exercito: { x: 640, y: 276, grupo: "tropa" },
    grupos: { tropa: { ativa: 4 }, herois: { ativa: 6 }, reforco: {} },
    inimigos: [["lider", 1, 700, 250, 1, "herois"], ["ardis", 1, 740, 300, 1, "herois"], ["pesado", 6, 716, 276, 2, "herois"],
      ["soldado", 20, 900, 276, 4, "reforco", 1], ["arqueiro", 8, 900, 428, 2, "reforco", 1]],
    levas: [{ id: 1, t: 45, quando: 0.3, x: 900, y: 276, aviso: "Reforços saem pelo portão e pela brecha." }],
  },
};

// ------------------------------------------------------------------------------------------------ Campo Livre 6
// Os cenários. Cada construção é um retângulo no chão (a colisão) com a altura do desenho (`alto`). Regras: casas,
// muralha e torres bloqueiam passagem, flechas, projéteis e áreas; o muro baixo bloqueia só a passagem (campo6.js).
// A vila: os arredores de uma povoação fortificada. A muralha corre de norte a sul a leste (x 790), com o portão
// entre as duas torres (72 px), uma brecha mais ao sul (48 px) e passagens nas duas pontas; casas dos dois lados da
// estrada que sai do portão para o oeste; dois muros baixos; o campo aberto a oeste para as hordas.
export const CENARIOS = {
  aberto: { nome: "Campo aberto", obstaculos: [] },
  vila: { nome: "Arredores da vila",
    estradas: [{ x: 0, y: 258, w: 960, h: 36 }, { x: 470, y: 0, w: 30, h: 258 }, { x: 600, y: 294, w: 28, h: 266 }],
    obstaculos: [
      { tipo: "muralha", x: 790, y: 30, w: 18, h: 202, alto: 30 }, { tipo: "muralha", x: 790, y: 320, w: 18, h: 84, alto: 30 },
      { tipo: "muralha", x: 790, y: 452, w: 18, h: 76, alto: 30 },
      { tipo: "torre", x: 784, y: 214, w: 30, h: 26, alto: 42 }, { tipo: "torre", x: 784, y: 312, w: 30, h: 26, alto: 42 },
      { tipo: "casa", x: 590, y: 64, w: 56, h: 40, alto: 26 }, { tipo: "casa", x: 672, y: 118, w: 48, h: 38, alto: 24 },
      { tipo: "casa", x: 548, y: 170, w: 44, h: 34, alto: 22 }, { tipo: "casa", x: 686, y: 350, w: 52, h: 40, alto: 26 },
      { tipo: "casa", x: 586, y: 404, w: 56, h: 38, alto: 24 }, { tipo: "casa", x: 520, y: 470, w: 46, h: 34, alto: 22 },
      { tipo: "casa", x: 690, y: 464, w: 44, h: 34, alto: 22 },
      { tipo: "casa", x: 858, y: 96, w: 64, h: 50, alto: 30 }, { tipo: "casa", x: 868, y: 412, w: 52, h: 44, alto: 28 },
      { tipo: "muro", x: 420, y: 118, w: 96, h: 6, alto: 6 }, { tipo: "muro", x: 430, y: 446, w: 80, h: 6, alto: 6 },
    ] },
  // Campo Livre 7: o trecho da amostra de arte. A muralha corre de norte a sul (x 560), com o portão entre as torres
  // (64 px) e a estrada passando por ele; do lado de dentro, uma casa e o muro baixo de um quintal; do lado de fora,
  // árvores (o tronco bloqueia a passagem; a copa não barra flechas) e o campo aberto para lutar. Cabe numa tela a
  // 1920 × 1080 com o herói na estrada. `luzes`: as tochas e a janela (só a direção sombria as acende).
  povoado: { nome: "O portão da povoação",
    estradas: [{ x: 0, y: 264, w: 960, h: 32 }, { x: 680, y: 0, w: 22, h: 264 }],
    obstaculos: [
      { tipo: "muralha", x: 560, y: 24, w: 18, h: 212, alto: 30 }, { tipo: "muralha", x: 560, y: 326, w: 18, h: 210, alto: 30 },
      { tipo: "torre", x: 554, y: 222, w: 30, h: 26, alto: 42 }, { tipo: "torre", x: 554, y: 312, w: 30, h: 26, alto: 42 },
      { tipo: "casa", x: 612, y: 178, w: 58, h: 42, alto: 26 }, { tipo: "muro", x: 612, y: 352, w: 64, h: 6, alto: 6 },
      { tipo: "arvore", x: 286, y: 168, w: 6, h: 4, alto: 34, copa: 13 }, { tipo: "arvore", x: 330, y: 146, w: 6, h: 4, alto: 30, copa: 11 },
      { tipo: "arvore", x: 246, y: 396, w: 6, h: 4, alto: 36, copa: 14 }, { tipo: "arvore", x: 300, y: 424, w: 6, h: 4, alto: 30, copa: 11 },
      { tipo: "arvore", x: 470, y: 150, w: 6, h: 4, alto: 32, copa: 12 }, { tipo: "arvore", x: 462, y: 430, w: 6, h: 4, alto: 34, copa: 13 },
      { tipo: "arvore", x: 180, y: 220, w: 6, h: 4, alto: 30, copa: 11 },
    ],
    luzes: [{ x: 569, y: 238, raio: 44 }, { x: 569, y: 328, raio: 44 }, { x: 622, y: 206, raio: 30 }] },
};

// As composições dos exércitos (nos encontros novos), escolhidas antes da luta, uma para cada lado: [tipo, quantos,
// profundidade atrás da frente, deslocamento em y, colunas]. Os soldados e arqueiros frágeis continuam em todas.
export const COMPOSICOES = {
  comum: { nome: "Comum (soldados e arqueiros)",
    aliados: [["soldado", 30, 0, 0, 4], ["arqueiro", 12, 62, 0, 2]],
    inimigos: [["soldado", 30, 0, 0, 4], ["veterano", 8, 52, 0, 2], ["arqueiro", 12, 106, 0, 2]] },
  cavalaria: { nome: "Com cavalaria",
    aliados: [["soldado", 22, 0, 0, 4], ["arqueiro", 12, 62, 0, 2], ["cavaleiro", 12, 20, -110, 3]],
    inimigos: [["soldado", 24, 0, 0, 4], ["arqueiro", 10, 80, 0, 2], ["cavaleiro", 16, 30, -120, 4]] },
  pesada: { nome: "Linha pesada e magos",
    aliados: [["pesado", 12, 0, 0, 2], ["soldado", 16, 26, 0, 4], ["arqueiro", 10, 70, 0, 2], ["magoBatalha", 4, 92, 0, 1]],
    inimigos: [["pesado", 14, 0, 0, 2], ["soldado", 16, 28, 0, 4], ["magoBatalha", 6, 70, 0, 2], ["arqueiro", 8, 96, 0, 2]] },
  completa: { nome: "Completa (todos os tipos)",
    aliados: [["pesado", 8, 0, 0, 2], ["soldado", 14, 24, 0, 4], ["arqueiro", 10, 66, 0, 2], ["magoBatalha", 4, 88, 0, 1], ["cavaleiro", 10, 20, -110, 3]],
    inimigos: [["pesado", 10, 0, 0, 2], ["soldado", 18, 26, 0, 4], ["magoBatalha", 5, 70, 0, 1], ["arqueiro", 8, 94, 0, 2], ["cavaleiro", 14, 30, -120, 4]] },
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

// Campo Livre 7: os controles (CC) e a proteção contra repetição. Cada controle forte (atordoamento, imobilização,
// interrupção, provocação) num herói (o seu, Morel, Odette, Harg, Ardis) conta numa janela de `janela` s: o primeiro
// vale inteiro, o segundo `fatores[1]`, o terceiro `fatores[2]`; o quarto não pega ("firme") até a janela fechar (ela
// se renova a cada controle que pega). A lentidão não conta e não acumula: vale a mais forte. As tropas comuns não têm
// proteção. A interrupção cancela a preparação do golpe e segura `interrompe` s.
export const CONTROLE = { janela: 6, fatores: [1, 0.6, 0.3, 0], interrompe: 0.25,
  nomes: { atordoado: "Atordoado", imobilizado: "Imobilizado", interrupcao: "Interrompido", provocacao: "Provocado", lento: "Lento" } };

// O que limita o impacto, para muitos golpes juntos não travarem a tela nem a câmera.
export const IMPACTO = {
  pausaMax: 100,          // nenhuma pausa de impacto passa disto (ms)
  pausaRefratario: 150,   // depois de uma pausa, outra só depois de 150 ms
  tremorQueda: 1.8,       // o "trauma" da câmera cai 1,8 por segundo
  tremorMaxPx: 6,         // deslocamento máximo em px nativos, com intensidade 100% e trauma 1
};
