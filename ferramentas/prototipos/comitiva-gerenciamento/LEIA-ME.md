# Comitiva: gerenciamento (proposta, protótipo)

**Nada disto está no jogo.** É a proposta da seção 7 do pedido de 26/10/2026 (depois da integração do combate, 1.211.x):
uma janela só para o herói e a comitiva, com o equipamento de cada um e a bolsa do grupo. Aguarda a avaliação do Jean.

## Abrir

```
python ferramentas/prototipos/comitiva-gerenciamento/servidor.py
```

Abra o endereço impresso. O servidor gera `dados.json` pelo motor (`gerar_dados.py`) e serve o CSS, os ícones e os
scripts de tela do jogo direto de `rpg/web/static` (nada copiado). Recarregar a página volta ao começo.

## O que a página mostra

- **Abas com retratos** (Jean, Odette, Morel, Yara); ← → trocam pelo teclado. A aba de quem está ferido fica apagada,
  mas abre: o equipamento de um indisponível pode ser trocado.
- **A mesma janela** para todos: o boneco e a ficha são os do selecionado (o desenho do inventário de hoje).
- **Bolsa do grupo**: uma só, os 12 espaços da mochila de hoje. Ninguém ganha mochila nem capacidade a mais.
- **A ficha da peça** compara com o que o **selecionado** usa: é a ficha do jogo (`Telas.htmlItem`), com o personagem
  da aba no lugar do herói. Peça que ele não usa: o motivo ("Morel não usa peças de mago").
- **Sem transferência manual**: no espaço marcado, "Do grupo, para este espaço" lista as peças que outros usam e
  serviriam; vestir tira de quem usa e põe no selecionado num passo (a que ele usava volta para a bolsa).
- **Atributos (proposta)**: os seis de cada companheiro, os pontos livres, o "+" e "Distribuir pela sugestão".

Dados de verdade (do motor): o herói (Guerreiro paladino nível 5, vestido como o jogo vestiria), a vida e os números
de hoje dos companheiros (`comitiva.atributos`) e as peças da bolsa (`itens.gerar_equip`, com a ficha da tela).
**Temporários**: as peças vestidas pelos companheiros, quem usa que peça, os atributos deles e Yara ferida.

## Dependências reais (investigadas no código)

| Assunto | Hoje | O que a proposta pede |
|---|---|---|
| Peças permitidas | Cada item tem `classe` (guerreiro, arqueiro, mago) ou nenhuma; só o herói veste (`Inventario.pode_usar`) | Uma classe de peças por companheiro (proposta: Odette e Yara, as de mago; Morel, as de guerreiro) e as sem classe |
| Números dos companheiros | Vida, Ataque, Poder, Defesa e Agilidade do catálogo, pelo nível do herói (`comitiva.atributos`), × a lealdade em luta (`preparar_combate`) | Somar os bônus das peças a esses números, na mesma conta do herói (`Jogador.totais`) |
| Bolsa | A mochila (12) e a bolsa de consumíveis são do herói; a comitiva já usa a bolsa na luta | A mochila vira "a bolsa do grupo", a mesma; nenhuma outra |
| Trocar o grupo | Membros vão para a reserva (acampamento) e voltam (`fogueira.py`) | Quem vai para a reserva leva o que veste; volta vestido |
| Indisponíveis | Ferido fica fora das lutas até descansar; `fora` (longe do grupo) não aparece | O ferido pode ser equipado (aba apagada); quem está longe, não |
| Sair da comitiva | O membro some (`dispensado`, partida por aprovação) | As peças dele voltam para a bolsa; se ela estiver cheia, ficam no chão do acampamento (decidir: perder, guardar, ou um baú no acampamento) |
| Saves | Membros sem `equip` (o migrador já percorre a comitiva à procura de itens) | `equip` por membro, vazio nos saves antigos (uma migração simples) |
| Comparação | `Telas.htmlItem` e `comparar` leem `App.estado.heroi` | O mesmo código, com o personagem da aba (o protótipo prova que basta isso) |

## Atributos dos companheiros (proposta de regra, não implementar ainda)

- **Iniciais pela identidade** (24 pontos, como o herói): Odette FOR 2 AGI 3 CON 4 INT 7 PER 3 VON 5 (fé e cura: Poder
  e Tenacidade); Morel FOR 7 AGI 3 CON 7 INT 1 PER 3 VON 3 (o brigão que protege); Yara FOR 1 AGI 4 CON 3 INT 8 PER 5
  VON 3 (a arcana do Vazio).
- **Pontos pela progressão**: 1 por nível do herói (a metade dos dele), para que eles cresçam sem virar cópias dele.
- **Sugestão**: "Distribuir pela sugestão" põe os pontos na ordem da identidade (Odette: VON › INT › CON; Morel:
  CON › FOR › VON; Yara: INT › PER › VON), para quem não quiser administrar.
- Os números de hoje (catálogo × nível) continuariam a base; os atributos somariam como no herói.

## Roteiro (2 minutos)

1. Jean: veja o boneco e a bolsa de sempre. Clique numa peça da bolsa: a ficha compara com o que ele usa.
2. Aba Odette (← →): clique no Grimório de Ferro da bolsa. A ficha compara com a Maldição Antiga dela. "Vestir em
   Odette": a antiga volta para a bolsa.
3. Aba Morel: o Montante, contra a Maça dele. O arco de arqueiro fica apagado: ele não usa.
4. Ainda em Morel, clique no Peito: "Do grupo, para este espaço" mostra a peça que Jean veste; vestir tira de Jean.
5. "Distribuir pela sugestão": os pontos vão para CON, FOR e VON.
6. Aba Yara: ferida (apagada), mas o equipamento dela abre.
