# Cópia das traduções do HoennKantoWiki

Cópia das traduções PT-BR da Gen 3 do HoennKantoWiki, feita por
`tools/import_wiki_ptbr.py`. O wiki é só lido e nunca é alterado por este
projeto. O commit e a data da cópia estão em `source.json`.

Para atualizar a cópia:

```sh
python tools/import_wiki_ptbr.py --wiki ../HoennKantoWiki
```

Não edite estes arquivos à mão: a próxima cópia sobrescreve tudo. As
adaptações para o jogo (quebra de linha, caixa alta, abreviações, nomes
traduzidos) ficam no catálogo de `tools/locales/ptbr/`, fora desta pasta.

## Arquivos

| Arquivo | Chave | Conteúdo | Observação |
|---|---|---|---|
| `moves.json` | slug do golpe (`thunderbolt`) | descrição em PT | Mesmo texto da Gen 3; precisa quebrar as linhas |
| `abilities.json` | slug da habilidade | descrição em PT | Versão expandida do wiki; o jogo precisa de uma linha curta |
| `pokedex.json` | número nacional | entrada da Pokédex em PT | Entradas de Ruby/Sapphire, não do Emerald; usar só como apoio |
| `genera.json` | categoria em inglês | categoria em PT | Tirar o "Pokémon" (`Pokémon Semente` vira `SEMENTE`) |
| `items.json` | slug do item | nome em inglês e descrição em PT | Só 18 itens |
| `types.json` | tipo | nome em PT (`TIPOS_PT`) | |

O texto em inglês do wiki fica de fora, porque este repositório não guarda
conteúdo do jogo.

## Onde o jogo diverge das regras do wiki

As regras de tradução do wiki (`docs/REGRAS-TRADUCAO.md` daquele projeto)
continuam valendo, menos nestes pontos, decididos para o jogo em
`docs/ROADMAP-PTBR.md`:

- Golpes, itens, habilidades, naturezas e a parte genérica dos lugares são
  traduzidos. No wiki esses nomes ficam em inglês.
- Atributos são traduzidos (`ATAQUE`, `DEFESA`, `VELOCIDADE`). No wiki ficam
  no original.
- Nomes e termos seguem a caixa alta do Emerald (`POKéMON`, `ROTA 104`).
