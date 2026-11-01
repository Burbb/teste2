# Protótipo tático por turnos da etapa 8 (Tático 2): Dofus como referência

Jogável e isolado (01/11/2026, versão **Tático 2**). **Não é integração:** o jogo não carrega nada desta pasta (um teste
confere) e o combate do jogo não mudou. Os números são de teste. A pesquisa (Dofus e Baldur's Gate 3), as regras
escolhidas, adaptadas e deixadas de fora, as medições e as limitações estão no
[31](../../../roadmapIDEIAS/31-ETAPA8-TATICO-POR-TURNOS.md). O Tático 1 (vista de cima, Python) continua em
`../etapa8-tatico/` como histórico; o campo livre, em `../etapa8-campo/`. **As duas direções estão em avaliação.**

## Abrir

Dê dois cliques em `demo.bat` (ou rode `python ferramentas/prototipos/etapa8-tatico2/servidor.py` na raiz). O servidor
tenta a porta **8807**; se ela estiver ocupada, diz quem está nela e usa a próxima livre, e **abre o navegador na porta
que de fato usou**. A versão aparece no terminal, no título da aba, no topo da preparação e no selo da luta: se não
aparecer "Tático 2", não é esta entrega. `DEMO_PORTA` escolhe outra porta; `DEMO_SEM_NAVEGADOR=1` não abre o navegador.

## Controles

| Tecla | O quê |
|---|---|
| clique numa casa verde | andar (o caminho e o custo em PM aparecem sob o mouse) |
| `1`–`6` ou clique na habilidade | mirar: alcance em azul, casas sem visão hachuradas; sob o mouse, a área e a prévia (dano, cura, quem cai, estados, onde o empurrado para) |
| clique num alvo | lançar |
| `Esc` ou botão direito | cancelar a mira |
| `Espaço` (ou `E`) | encerrar o turno |
| `Tab` | registro |
| `R` / `P` | no fim: repetir a luta / voltar à preparação (`P` também durante a luta) |

Passe o mouse sobre um combatente (na arena ou na ordem) para ver vida, PA, PM, kit e estados com a duração; sobre uma
habilidade, para a regra completa ("3 PA · Alcance 1–6 · Recarga 2 turnos") e a descrição.

## O que tem

- **Preparação:** o encontro (Campo aberto, A passagem, Perto longe e apoio), a classe do herói (Guerreiro, Mago,
  Arqueiro), **6 habilidades de 10** e **2 talentos de 5**, com duas montagens prontas por classe; os kits fixos de
  Morel e Odette à vista.
- **A luta:** arena de 14 × 14 casas em losango; o herói, Morel e Odette (você controla os três, cada um na sua vez)
  contra cinco inimigos com IA. Ordem por iniciativa, alternando os lados. 6 PA e 3 PM (4 no Arqueiro) por vez, em
  qualquer ordem; sair do contato custa PM a mais (1 por inimigo; 2 se for pesado).
- **Espaço:** pilares (bloqueiam passagem e visão), rochas baixas e água (bloqueiam passagem, deixam ver), barris de
  óleo (explodem com fogo), chão em chamas ou envenenado, armadilhas, golpe preparado em casas marcadas, empurrar e
  puxar com dano de colisão.
- **Fim:** vitória (os cinco caem) ou derrota (os três caem); repetir com o mesmo encontro ou voltar à preparação.

## Arquivos

| Arquivo | O que é |
|---|---|
| `tela/conteudo.js` | Todos os números e textos: regras, estados, habilidades, talentos, classes, companheiros, inimigos, montagens, arenas, encontros, a versão |
| `tela/regras.js` | As regras sem DOM (navegador e Node): geometria, visão, caminhos com bloqueio, áreas, efeitos, a vez, a prévia (`prever`: a ação numa cópia) |
| `tela/ia.js` | A IA de uma vez (inimigos e o jogador automático) |
| `tela/desenho.js` | A arena em losangos, os combatentes, as marcas e os efeitos |
| `tela/sprites.js` | Os combatentes à mão na grade (copiado do Campo Livre 5 e ampliado: Arqueiro, Morel, Odette, lobo, xamã, bruxa) |
| `tela/main.js`, `index.html`, `tatico.css` | A preparação, a HUD, a entrada, as animações |
| `servidor.py`, `demo.bat` | O lançador (porta livre, versão) |
| `testes/regras.test.mjs` | 18 testes das regras e da IA (Node); `testes/test_tatico2.py` roda-os e confere o isolamento |
| `ferramentas/simular.mjs` | Lutas sem tela com a IA dos dois lados: resultado, rodadas, vida, tempo da IA |
| `ferramentas/conferir.mjs` | Playwright: o fluxo real nas duas janelas (preparação, andar, mirar, prévia = efeito, vezes de Morel e Odette, inimigos, console) |
| `capturas/` | `t2-preparar-1920`, `t2-mirar-1280` e `-1920`, `t2-vez-morel-1920`, `t2-passagem-1280` |

```
node --test ferramentas/prototipos/etapa8-tatico2/testes/regras.test.mjs
python -m unittest discover -s ferramentas/prototipos/etapa8-tatico2/testes -t ferramentas/prototipos/etapa8-tatico2
node ferramentas/prototipos/etapa8-tatico2/ferramentas/simular.mjs
```

Parâmetros de endereço (testes e demonstração): `?classe=mago&build=Piromante&enc=passagem&auto=1` (`auto`: começa a
luta direto; `robo=1`: a IA joga também pelos aliados; `rapido=1`: animações curtas).
