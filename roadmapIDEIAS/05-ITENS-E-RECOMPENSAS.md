# 05 — Itens e recompensas

## Base pronta

Geração de equipamento, afixos, raridades, únicos com id/lore, comparação, compra/venda, slots e reforço.

fonte_item integra bônus especiais aos modificadores. Únicos podem declarar mods, mults e gatilhos; há teste dessa capacidade. Os únicos atuais são principalmente atributos e efeitos conhecidos: isso não significa que um catálogo de itens transformadores já esteja pronto.

## Três funções

| Função | Resultado |
|---|---|
| Poder | Melhoria de atributos |
| Ajuste | Favorece comportamento ou sinergia |
| Transformação | Muda uma habilidade ou ciclo de build |

Um raro bem combinado pode ser preferível a um lendário. Cada cor não precisa substituir automaticamente a anterior.

Afixos atuais podem ser ampliados com critérios de compatibilidade e valor. Uma estrutura extensa de prefixos/sufixos com restrições ainda é trabalho de design, não funcionalidade comprovada.

## Único transformador completo

Primeiro especificar um item que use gatilhos existentes. Se ele transformar uma magia, depender da resolução de habilidade efetiva.

Um item completo exige:
- aquisição e identidade estável;
- efeito, limites e condições;
- descrição na ficha;
- indicação do que muda na build;
- feedback durante a luta;
- equipar/retirar e salvar/carregar;
- interação com talentos e efeitos semelhantes.

ficha() hoje expõe principalmente bônus, classe, base, raridade e lore. Estender a apresentação dos efeitos especiais: não deixar um gatilho funcionar invisivelmente.

Exemplo futuro: escudo armazena dano bloqueado. Antes de usá-lo, definir o que conta como bloqueio, limites, consumo e hook necessário. Não inventar a ação de bloqueio só para reproduzir o exemplo.

## Reforço já existente

Ferreiro reforça arma, peito e mão secundária até +5. Incremento previsível, custo crescente, atributo principal e nome +N. Reutilizar.

Revisar economia e feedback; não pedir ao Claude para criar reforço do zero. Brilho persistente ao redor da peça é proposta visual separada, não suporte confirmado.

Manter reforço separado de raridade. Não acrescentar destruição ou falha aleatória como padrão.

## Cor e categorias

Laranja é a intenção visual para lendários. Conferir CSS e telas antes de alterar; não presumir que todas as representações já usam a mesma cor.

Único descreve identidade fixa; lendário pode descrever raridade. Definir categorias sem criar duplicação confusa.

## Saque e economia

Aumentar drop junto de variedade útil e organização. Observar frequência de upgrades, decisões de build, tempo descartando e momentos sem progresso.

Recompensar também com descobertas, conversas, reputação, acesso e habilidades. Preservar expectativa e surpresa.

Avaliar loot, venda, recuperação, reforço e suprimentos juntos. Mochila de 12 espaços cria tensão; mais saque pode transformar isso em atrito. Armazém nas vilas e venda rápida são futuras extensões sob demanda, não pré-requisitos da primeira região.

## Entrega inicial

Usar bases e afixos existentes. Demonstrar um único relevante, depois variar efeitos para Guerreiro, Arqueiro e Mago. Não exigir um item exclusivo por habilidade.

Antes da campanha final, verificar que recompensas cobrem os estilos e que uma escolha de classe não deixa o jogador sem equipamento útil.
