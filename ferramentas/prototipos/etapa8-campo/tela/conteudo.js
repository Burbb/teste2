// PROTÓTIPO de campo livre da etapa 8 (nada no jogo): os números e os kits. Tudo de teste; as regras que usam estes
// números estão em sim.js. Unidades: distância em pixels nativos (o campo é desenhado 1:1 e ampliado inteiro), tempo
// em segundos, empurrão em px/s (a unidade desliza cerca de empurrão/9 px, ver ATRITO_EMPURRAO).
export const VERSAO = "Campo Livre 1";

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
  // A outra: fica atrás da linha e fortalece quem está na aura (+50% de dano, ataca 25% mais rápido); derrubado,
  // abala os inimigos em volta por 2 s (recuam, não atacam).
  estandarte: { nome: "Porta-estandarte", papel: "apoio", raio: 3.5, vida: 30, vel: 30, massa: 1.5, dano: 2,
    alcance: 3, preparo: 0.3, recarga: 1.2, vagas: 3, elite: true, aura: 70, auraDano: 1.3, auraRitmo: 0.85,
    abala: 120, abalaTempo: 2 },
};

// Os heróis. `vagas` 7: até sete soldados batem nele de uma vez (cercado, ele sente).
export const HEROIS = {
  guerreiro: {
    nome: "Guerreiro", raio: 5, vida: 260, vel: 72, massa: 6, vagas: 7,
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
    nome: "Mago", raio: 4.5, vida: 170, vel: 68, massa: 4, vagas: 7,
    recurso: { nome: "Mana", max: 100, inicial: 100, regen: 7 },
    kit: {
      basico: { nome: "Faísca", tecla: "Botão esquerdo", preparo: 0.05, rec: 0.22, vel: 300, alcance: 175, dano: 4,
        empurrao: 50, atordoa: 0.12, mover: 0.75 },
      bola: { nome: "Bola de Fogo", tecla: "Botão direito", custo: 30, recarga: 1.5, preparo: 0.18, rec: 0.2,
        alcance: 180, vel: 480, raio: 24, dano: 13, empurrao: 200, atordoa: 0.5, chao: { duracao: 2, dps: 5 },
        pausa: 50, pausaPorAbate: 6, pausaMax: 85, tremor: 0.3, tremorPorAbate: 0.03, tremorMax: 0.5 },
      piscar: { nome: "Piscar", tecla: "Espaço", recarga: 6, distancia: 95, raio: 28, dano: 3, empurrao: 200,
        atordoa: 0.6, invul: 0.15, tremor: 0.15 },
      muralha: { nome: "Muralha de Fogo", tecla: "Q", custo: 40, recarga: 9, alcance: 150, comprimento: 96,
        duracao: 5, dps: 14, preparo: 0.15, rec: 0.15, tremor: 0.1 },
    },
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
