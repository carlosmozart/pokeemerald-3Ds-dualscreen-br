# Tarefa do PC da POKéDEX: as 386 descrições

Divisão combinada em 09/10/2026 (ver "Dois PCs ao mesmo tempo" no
[CLAUDE.md](../CLAUDE.md)). Este PC traduz **só** as descrições da POKéDEX.
O outro PC está nos menus de `src/strings.c`, incluindo os textos da tela
da POKéDEX (busca, ordem, ALT./PESO): não mexa em `strings.c.txt`.

## Antes de começar

1. `git pull` (uma vez, para receber os ganchos de sincronização).
2. Abra uma sessão nova do Claude Code no repositório: o gancho de início
   traz os commits do outro PC sozinho. Confirme que `python` funciona no
   terminal; os ganchos dependem dele.
3. Prepare a árvore em português:
   `python tools/bootstrap.py --port-lang pt_br`

## O arquivo

- Catálogo: `tools/locales/pt_br/src/data/pokemon/pokedex_text.h.txt`
  (ainda não existe; crie com um comentário no topo, como os outros).
- Fonte em inglês: `src/data/pokemon/pokedex_text.h`, 386 textos, de
  `gBulbasaurPokedexText` em diante (`gDummyPokedexText` é o de espécie
  desconhecida e também entra).
- Cada entrada leva o rótulo, o hash do inglês e o texto, com `\n` no fim
  de cada linha. O hash e a largura de cada texto em inglês saem de:

  ```
  python tools/localize_portuguese.py --tree build/upstream --show src/data/pokemon/pokedex_text.h
  ```

  (no Windows, com `PYTHONIOENCODING=utf-8` se o console der erro de
  codificação.)

Exemplo de formato:

```
[gBulbasaurPokedexText] b7c713f850 width=224
BULBASAUR pode ser visto cochilando sob\n
o sol forte. Há uma semente nas costas.\n
Ao absorver os raios do sol, a semente\n
cresce cada vez mais.
```

## Regras

- **Até 4 linhas**, como o original, e sem `\p`.
- **Largura**: a janela da POKéDEX tem as linhas largas; em inglês o mais
  largo do arquivo tem 224 px. Num texto de C a ferramenta só aceita a
  largura do próprio inglês; use `width=224` na entrada (ou acrescente
  `src/data/pokemon/pokedex_text.h` a `WIDEST_IN_FILE` em
  `tools/localize_portuguese.py`, num commit próprio). Confira no 3DS
  algumas entradas longas antes de seguir com o resto.
- **Traduzir do Emerald**, não do Ruby/Sapphire (Princípio 5 do roadmap).
  A cópia do wiki tem as de Ruby/Sapphire em
  `tools/locales/pt_br/referencia/hoennkantowiki/gen3/i18n/pt.json`
  (chave `pokedex`): use como apoio só quando o texto for o mesmo.
- Termos e estilo do [GLOSSARIO.md](../tools/locales/pt_br/GLOSSARIO.md) e
  do `CLAUDE.md`: nomes de POKéMON e golpes em maiúsculas, como no jogo
  (BULBASAUR, LANÇA-CHAMAS); "você"; nomes oficiais do Brasil.

## Ritmo

- Lotes pequenos, por ordem da POKéDEX nacional (001–025, 026–050…).
  Depois de cada lote: aplicar (`python tools/bootstrap.py --port-lang
  pt_br`, que para se algo não couber), `git commit`. O gancho faz o push.
- A cada lote, marque o andamento na Fase 5 do
  [roadmap](ROADMAP-PTBR.md) ("Pokédex (386)") e na cópia interativa
  (link no `CLAUDE.md`).
- Para testar no 3DS, compile com
  `python tools/bootstrap.py --make --port-lang pt_br -j8`.
