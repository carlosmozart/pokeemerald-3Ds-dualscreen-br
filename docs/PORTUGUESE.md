# Pokémon Emerald em português do Brasil

**Etapa 1: a interface do port.** A compilação `PORT_LANG=pt_br` mostra em
português tudo o que é do próprio port: os rótulos da tela de baixo (MAPA, os
atributos, as opções de 3D), as abas AJUSTES, MELHORIAS e TRAPAÇAS com suas
células, e as mensagens de erro do pacote de dados. O jogo em si (diálogos,
menus, nomes) continua em inglês, vindo da ROM americana/europeia (BPEE), e
usa o mesmo `emerald3ds.pak` da versão inglesa.

Ainda não foi testada num 3DS.

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

## Próximas etapas

1. O texto do jogo. Não existe Pokémon Emerald oficial em português, e este
   repositório não distribui conteúdo do jogo; o caminho para isso ainda está
   em aberto.
