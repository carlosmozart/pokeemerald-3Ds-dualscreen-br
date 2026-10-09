# Regras da tradução PT-BR

Este fork traduz o port 3DS do Pokémon Emerald para o português do Brasil.
Plano, fases e decisões: [docs/ROADMAP-PTBR.md](docs/ROADMAP-PTBR.md).
Como compilar: [docs/PORTUGUESE.md](docs/PORTUGUESE.md).

## Termos

- A referência única de termos é
  [tools/locales/pt_br/GLOSSARIO.md](tools/locales/pt_br/GLOSSARIO.md).
- Vale a **nomenclatura oficial do Brasil**, conferida nos nomes `pt_br` do
  Bulbapedia (jogos; quando eles não têm o termo, anime, TCG e mangá). Ela
  vale mais que o HoennKantoWiki e que qualquer escolha antiga: BOLSA (não
  Mochila), POKé BOLA, PS (não HP), tipos PLANTA e AÇO (não GRAMA e METAL).
- Só invente um termo quando não houver nome oficial, e registre a escolha
  na segunda tabela do glossário.
- Atributos: ATAQUE, DEFESA, AT. ESP., DEF. ESP. (AT.ESP. e DEF.ESP. em
  janelas estreitas), VELOC., PS, PRECISÃO, EVASÃO.

## Estilo

- Caixa do Emerald: termos do jogo em maiúsculas (`POKéMON`, `POÇÃO`,
  `ROTA 101`).
- Traduzir o máximo: golpes, itens, habilidades, naturezas e a parte
  genérica dos lugares (`CIDADE DE LITTLEROOT`). Espécies, personagens e o
  nome próprio dos lugares ficam como estão.
- "Você" e tom informal. Mensagens de batalha localizadas, não ao pé da
  letra.
- Quando não couber, abreviar no estilo do jogo (e registrar no glossário),
  em vez de deixar em inglês.

## Fluxo

- Há um só fluxo: `python tools/bootstrap.py --make --port-lang pt_br`, que
  aplica os catálogos de `tools/locales/pt_br/` com
  `tools/localize_portuguese.py`. Não crie um fluxo paralelo.
- `python tools/localize_portuguese.py --tree build/upstream --status`
  mostra o progresso; a aplicação para se um texto não couber ou se o inglês
  do pret mudou.
- Nenhum conteúdo da ROM no repositório: o catálogo guarda só o português e o
  hash do inglês.

## Dois PCs ao mesmo tempo

A tradução avança em dois PCs, os dois no `main`. O GitHub é o ponto de
encontro, e os ganchos de `.claude/settings.json` cuidam da rotina:

- **Ao abrir uma sessão**, `tools/sync_pcs.py start` traz os commits do
  outro PC (`pull --rebase`). Leia o que ele disser antes de começar.
- **Depois de cada `git commit`**, `sync_pcs.py push` faz o rebase sobre o
  que o outro PC enviou e o push. Faça commits pequenos e frequentes (um
  mapa, um arquivo do catálogo), nunca um lote de horas.
- **Ao terminar uma resposta**, `sync_pcs.py check` avisa de commits ou
  arquivos que ainda não estão no GitHub.
- Se o rebase der conflito, o script desfaz o rebase sem perder nada e
  avisa: resolva com o usuário antes de seguir.

Para não pisar no trabalho do outro PC:

- **Patches novos**: antes de escolher o número, rode
  `python tools/sync_pcs.py start` e use o próximo número livre em
  `patches/pokeemerald/`; faça o commit e o push do patch logo em seguida,
  para o número ficar reservado.
- **Divida o trabalho por arquivo do catálogo** (um PC nos mapas, o outro
  em `src/strings.c.txt`, por exemplo). Dois PCs editando o mesmo arquivo
  de catálogo geram conflito.
- **Decisões** (glossário, roadmap) entram num commit próprio e são
  enviadas na hora, antes de traduzir com base nelas.
- **Roadmap: cada PC só edita a sua fase** em `docs/ROADMAP-PTBR.md` e na
  cópia interativa: o PC dos menus, a Fase 6; o PC dos mapas, a Fase 7.
  Os dois PCs marcando o roadmap a cada lote, em linhas vizinhas, geraram
  conflitos. Mudança em outra fase (uma decisão, um risco), num commit
  próprio e combinada com o usuário.

**Divisão atual** (09/10/2026, revista no mesmo dia e de novo com os treinadores e os `data/scripts` para o PC dos mapas; o usuário diz qual PC é qual ao abrir a
sessão, ou pergunte):

| PC | Fica com | Arquivos do catálogo |
|---|---|---|
| Menus | Os menus e mensagens de `src/strings.c`, incluindo os textos da tela da POKéDEX (busca, ordem, HT/WT), que também estão nele | `src/strings.c.txt` |
| Mapas | Os diálogos dos mapas (todos os `data/maps` com texto ficaram prontos em 09/10, com a FRONTEIRA DE BATALHA); agora as falas de mundo fora dos mapas: os treinadores comuns, a ZONA DE SAFÁRI e os scripts compartilhados (LIQUIDIFICADOR, CENTRO DE CUIDADOS, homem de MAUVILLE, moça de LILYCOVE, salão de concursos, BASES SECRETAS, árvores de FRUTA, golpes de campo…) | `data/maps/<Mapa>/scripts.inc.txt`, `data/text/trainers.inc.txt` e `data/scripts/*.inc.txt` |

Ao terminar uma parte, combine a próxima com o usuário e atualize esta
tabela num commit próprio.

## HoennKantoWiki

- **Nunca altere o HoennKantoWiki.** Só leia e copie o que precisar para
  `tools/locales/pt_br/referencia/hoennkantowiki/`.

## Roadmap

- Ao mudar uma decisão ou concluir uma fase, atualize
  `docs/ROADMAP-PTBR.md` e a cópia interativa
  (https://claude.ai/artifact/WJbeUGCNxyDJkuTXj6bADW), mantendo as duas
  iguais.
