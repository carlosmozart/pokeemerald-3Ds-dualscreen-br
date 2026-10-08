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
acentuadas em UTF-8 que a fonte do jogo tem: á à â é ê í ó ô ú ç e as
maiúsculas. As mensagens de erro saem pelo console do libctru, que é ASCII:
vão sem acentos.

Limites a respeitar ao traduzir:

- A fonte do jogo **não tem ã, õ, Ã nem Õ**; os textos desta etapa evitam
  essas letras.
- Células de opção: até 17 caracteres; abas: até 12 (com "1/2").
- Linhas das mensagens de erro: até 40 caracteres.

## Próximas etapas

1. Desenhar ã/õ/Ã/Õ em códigos livres do charmap e na fonte do jogo.
2. O texto do jogo. Não existe Pokémon Emerald oficial em português, e este
   repositório não distribui conteúdo do jogo; o caminho para isso ainda está
   em aberto.
