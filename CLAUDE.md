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

## HoennKantoWiki

- **Nunca altere o HoennKantoWiki.** Só leia e copie o que precisar para
  `tools/locales/pt_br/referencia/hoennkantowiki/`.

## Roadmap

- Ao mudar uma decisão ou concluir uma fase, atualize
  `docs/ROADMAP-PTBR.md` e a cópia interativa
  (https://claude.ai/artifact/WJbeUGCNxyDJkuTXj6bADW), mantendo as duas
  iguais.
