# Estudo de caso: a curandeira do Vau (28/10/2026, em avaliação)

O histórico está em `ferramentas/prototipos/curandeira/LEIA-ME.md`. Aqui, o que cada passada ensinou. **Nada aprovado
ainda:** é a candidata A em avaliação pelo Jean; as medidas e o ritmo são desta cena.

| Passada | O que era | O que o Jean disse | O que ficou de lição |
|---|---|---|---|
| 1ª | a cabana em código na linguagem da forja; o giro do pilão em 8 poses, só o braço | — | — |
| 2ª | a botica (potes com coisas dentro, alambique, proteções); o braço em formas cheias, 12 poses a 100 ms | gostou da composição e da botica; os maços pareciam pinhatas; o trabalho, robótico (só o braço) | limpeza e número de quadros não fazem atuação |
| 3ª | os maços à mão; a rotina com o corpo; os rostos refeitos | (em avaliação) | 5b da skill |

## O que funcionou na 3ª passada

- **Os maços** (`desenho.MACOS`): uma grade à mão por planta, com o barbante descendo da vara, a laçada por cima dela e
  duas voltas de amarração em volta dos talos. A sálvia em leque de folhas com as pontas para baixo e buracos entre
  elas; a lavanda em hastes de 1 px com a espiga roxa na ponta, em alturas diferentes; a réstia de alho em cabeças
  redondas na trança de palha; o raminho de bagas em cachos de 2×2 com o brilho de um pixel e duas folhas; a camomila
  em talos curtos com as flores miúdas (creme com o miolo amarelo). Comprimentos de 11 a 18 px, espaços de 9 a 11.
- **O corpo** (`figuras.py`): o braço com comprimentos fixos e o cotovelo calculado (o `assert` pega a mão fora do
  alcance); o tronco desenhado linha a linha com o desvio de cada linha entre os ombros e o quadril; a saia indo do
  quadril (que se mexe) à barra (parada); a cabeça em duas grades por personagem ("frente" e "baixo") e um deslocamento
  por pose; o antebraço de longe aparecendo até a mão na borda do almofariz.
- **A rotina** (`figuras.rotina`, exportada em `camadas/rotina.json`): voltas de 12 poses (os ombros 1 px à frente onde
  o pilão vai longe e 1 px abaixo onde aperta, a cabeça um quadro depois); a última volta desacelera e para de pé;
  inclinar (o peito, depois o quadril e o rosto); olhar; soltar o pilão encostado; a pitada; erguer, endireitar e
  cheirar; afastar a mão, descer, pegar o pilão inclinado, que é a pose 1 do giro. Marta: 9,4 s; Pita: 8,8 s.
- **O banquinho da Pita:** a bancada é a de Marta; de pé no chão, o almofariz ficava na altura do peito da menina.
- **Os rostos:** o pescoço da grade caindo no colo do vestido; o olho atrás da ponte do nariz; a sobrancelha de 1 px;
  na Pita, a franja de lado, a orelha, a bochecha corada de um pixel; na Marta, o lenço justo com o nó e o cabelo
  escuro na testa.
- **A conferência:** a folha das poses-chave (o corpo inteiro), a sequência tique a tique fora do giro, o zoom das
  poses de contato, e o jogo nas duas janelas (a vista quadro a quadro, um relógio só depois de sair e voltar).
