# 07 — Sequência de trabalho

Não são datas nem tarefas já autorizadas. São etapas propostas; cada uma deve ser dividida em entregas pequenas. Não executar tudo numa solicitação ao Claude.

## E0 — Encerrar a refatoração e conferir a base

**Objetivo:** conhecer o estado atual sem misturar mudanças de comportamento.
**Entrega:** leitura atualizada do roadmap técnico, sistemas disponíveis e limitações.
**Pronto quando:** a refatoração planejada está concluída/validada e há clareza sobre o que pode ser reaproveitado.
**Fora do escopo:** novas classes, campanha completa e balanceamento incidental.

## E1 — Especificar a região demonstrativa

**Depende de:** E0.
**Entrega:** documento curto com uma vila, algumas áreas externas, uma masmorra, conflito principal, conclusão local e dois companheiros.
**Definir:** duas classes de teste, identidades reconhecidas, soluções da missão, estados da vila e recompensas.
**Pronto quando:** existe um percurso completo descrito e alternativas com consequências observáveis.
**Fora do escopo:** escrever todos os capítulos ou todas as raças.

## E2 — Suportar mundo fixo e missão pequena

**Depende de:** E1.
**Entrega:** carregar a região escrita, registrar etapas/estados e apresentar progresso no Diário.
**Pronto quando:** a mesma missão pode seguir dois percursos, salvar/carregar e manter consequências corretas.
**Fora do escopo:** apagar previamente o procedural, criar editor universal ou simular rotina de todos os NPCs.
**Implementação:** adaptar o núcleo existente; conferir a etapa técnica de mundo/narrativa como dados.

## E3 — Demonstrar identidade e consequência

**Depende de:** E2.
**Entrega:** uma oportunidade de solução específica por identidade selecionada, uma reação de companheiro e uma mudança posterior no lugar.
**Pronto quando:** repetir o trecho com outra identidade permite uma experiência reconhecivelmente diferente.
**Fora do escopo:** campanhas separadas por personagem.

## E4 — Provar dois estilos de combate

**Depende de:** E0 e da especificação de E1; pode ser desenvolvido separadamente de E2–E3.
**Entrega:** ciclos distintos, escolhas de habilidade e um marco de especialização por estilo.
**Pronto quando:** Jean usa estratégias diferentes e entende custos/efeitos.
**Fora do escopo:** seis classes completas ou 300 habilidades.

## E5 — Acrescentar escolhas de build

**Depende de:** E4.
**Entrega:** talentos condicionais, transformação de habilidade e experiência de preparação a testar.
**Pronto quando:** duas configurações da mesma especialização alteram prioridades durante a luta.
**Fora do escopo:** árvore enorme e reespecialização sem design definido.

## E6 — Conectar loot à build

**Depende de:** E5.
**Entrega:** afixos pertinentes, alguns efeitos transformadores e um aprimoramento simples.
**Pronto quando:** encontrar uma peça pode motivar experimentar outra configuração; economia e inventário não geram atrito excessivo.
**Fora do escopo:** dilúvio de itens, destruição aleatória ou centenas de únicos.

## E7 — Jogar a região completa e ajustar ritmo

**Depende de:** E2–E6.
**Entrega:** percurso integrado, sobrevivência, morte e recompensas avaliados na mesma sessão.
**Pronto quando:** Jean consegue concluir o conflito local, perceber consequências e apontar motivos para uma segunda partida.
**Registrar:** tempo aproximado, trechos repetitivos, decisões memoráveis, builds usadas e dificuldades de compreensão.
**Fora do escopo:** acrescentar sistemas para encobrir problemas de ritmo.

## E8 — Expandir com evidência

**Depende de:** E7.
**Entrega:** próximo trecho de campanha OU próximo conjunto de classes; escolher uma frente por vez.
**Pronto quando:** a extensão preserva os pilares e o trabalho continua sustentável.
**Regra:** ampliar quantidade depois de comprovar utilidade; rever escopo se a expansão prejudicar consistência.

## Regra de conclusão

Entrega técnica funcionando não significa design aprovado. Validar regras e interface com os checks pertinentes; Jean testa diversão e clareza jogando. Atualizar estado da etapa somente com evidência, sem marcar implementação a partir destes textos.
