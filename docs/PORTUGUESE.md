# Pokémon Emerald em português do Brasil

A compilação em português (`--port-lang pt_br`) tem duas partes:

- **A interface do port**, toda em português: os rótulos da tela de baixo
  (MAPA, os atributos, as opções de 3D), as abas OPÇÕES, MELHORIAS e
  TRAPAÇAS com suas células, e as mensagens de erro do pacote de dados.
- **O texto do jogo**, em tradução: por enquanto a fala do Prof. Birch, o
  menu principal, o menu START e SIM/NÃO. O que ainda não foi traduzido fica
  em inglês. `python tools/localize_portuguese.py --tree build/upstream
  --status` mostra o progresso.

O jogo continua vindo da ROM americana/europeia (BPEE). Ainda não foi testada
num 3DS.

## Compilar

Com os requisitos da [guia de desenvolvimento](DEVELOPMENT.md):

```sh
python tools/bootstrap.py --make --port-lang pt_br -j8
```

Ou, numa árvore já preparada, `make -C 3ds_port PORT_LANG=pt_br`. Trocar
`PORT_LANG` recompila todos os objetos (o Makefile compara os flags em
`build/config`). `--port-lang pt_br` não se combina com `--spanish-rom`.

## Como funciona

`3ds_port/include/3ds_locale.h` escolhe cada texto do port com
`CTR_TEXT(inglês, espanhol, português)`, ou `CTR_TEXT_PT(inglês, português)`
para os que a interface espanhola ainda mostra em inglês. Os rótulos da tela
de baixo passam por `Ascii()` (`3ds_bottom_ui.c`), que aceita as letras
acentuadas em UTF-8: á à â ã é ê í ó ô õ ú ç e as maiúsculas. As mensagens
de erro saem pelo console do libctru, que é ASCII: vão sem acentos.

## ã, õ, Ã e Õ

As fontes do jogo não têm essas letras. O patch
`patches/pokeemerald/0040-portuguese-tilde-letters.patch` dá a elas os
códigos livres 0x2F a 0x32 do charmap (`'Ã'`, `'Õ'`, `'ã'`, `'õ'`, e
`CHAR_A_TILDE`, `CHAR_O_TILDE`, `CHAR_a_TILDE`, `CHAR_o_TILDE`) e as larguras
de A/O/a/o nas cinco fontes latinas. Os desenhos não estão no repositório:
quando cada fonte é carregada do pacote, `3ds_compat.c` copia a letra e põe
sobre ela o til do ñ (ou do Ñ) da mesma fonte, isto é, as linhas que o ñ
pinta e o n deixa em branco, centradas na largura da letra. Assim cada fonte
ganha um til no seu próprio estilo, e o texto do jogo pode usar
`_("não")` depois do patch.

Limites a respeitar ao traduzir:

- Células de opção: até 17 caracteres; abas: até 12 (com "1/2").
- Linhas das mensagens de erro: até 40 caracteres.

## Traduzir o texto do jogo

Não existe Pokémon Emerald oficial em português: a tradução é deste projeto.
Ela fica em `tools/locales/pt_br/`, um arquivo por fonte do pret (os textos
de `data/text/birch_speech.inc` em
`tools/locales/pt_br/data/text/birch_speech.inc.txt`), e
`tools/localize_portuguese.py` a aplica na árvore do bootstrap antes da
compilação. Cada entrada é o rótulo do texto, o hash do texto inglês e o
texto em português, escrito como no pret:

```text
[gText_Birch_BoyOrGirl] 904f2ae23a
Você é um menino?\n
Ou é uma menina?$
```

As linhas da entrada se juntam como estão (uma linha em branco termina a
entrada); `\n` quebra a linha, `\l` rola o texto, `\p` abre um novo
parágrafo, e os textos dos `.inc` terminam em `$`. O inglês não é copiado
para cá: para traduzir um arquivo, veja seus textos e hashes com

```sh
python tools/localize_portuguese.py --tree build/upstream --show data/text/save.inc
```

Antes de mudar a árvore, a ferramenta confere tudo e não aplica nada se algo
falhar:

- o hash: se o texto inglês mudou, a tradução precisa ser revista;
- cada caractere existe no charmap (com ã, õ, Ã e Õ do patch 0040);
- os mesmos placeholders do inglês (`{PLAYER}`, `{STR_VAR_1}`...);
- a largura de cada linha na fonte normal: até 208 px nos textos dos `.inc`
  (as caixas de mensagem têm 216), e nas strings de C, que costumam ser
  menus, a largura do inglês. `width=N` no cabeçalho permite N pixels, para
  uma entrada de menu que cabe na janela (`[gText_MenuBag] 332c000cf7
  width=42`: as entradas do menu START cabem na largura de POKéMON).

`--check` só valida. Convenções: nomes próprios em maiúsculas como no jogo
(POKéMON, BIRCH, LITTLEROOT), os termos oficiais brasileiros quando existem
(MOCHILA, OPÇÕES), e texto neutro quando o jogador ainda não escolheu o
gênero.

## O pacote de dados

O texto do jogo faz parte dos dados que o builder monta a partir da ROM. Um
executável em português precisa de um pacote gerado para ele: a receita da
compilação em português leva os textos traduzidos como bytes literais (não
estão na ROM), e `tools/gen_recipe.py` recusa mais de 64 KiB de literais
(`--max-literal`), o que a tradução completa vai passar. Releases em
português e o builder para elas ainda estão por fazer; por enquanto, use os
dados soltos ou embutidos da compilação de desenvolvimento
([guia de desenvolvimento](DEVELOPMENT.md)).
