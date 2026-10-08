# Glossário PT-BR

A regra do projeto: traduzir o máximo possível, com a **nomenclatura oficial
usada no Brasil** (os jogos localizados em português do Brasil e, quando
eles não têm o termo, o anime, o TCG e o mangá). Fonte de consulta: os nomes
"Brazilian Portuguese" (`pt_br`) do Bulbapedia, conferidos em 08/10/2026.

Antes de usar um termo novo, confira o nome oficial; só invente quando não
houver um, e registre a escolha na segunda tabela.

## Termos oficiais

| Inglês | Português (Brasil) | Observação |
| :--- | :--- | :--- |
| Bag | BOLSA | jogos, TCG, mangá |
| Badge | INSÍGNIA | |
| Berry | FRUTA | jogos, anime |
| Elite Four | ELITE DOS QUATRO | |
| Champion | CAMPEÃO / CAMPEÃ | flexiona: evite quando vale para o jogador |
| Egg | OVO | |
| Evolution | EVOLUÇÃO | |
| Experience | EXPERIÊNCIA | |
| Fainted | DESMAIADO | |
| Gym | GINÁSIO | |
| Gym Leader | LÍDER DE GINÁSIO | |
| HM | MÁQUINA OCULTA (MO) | |
| HP | PONTOS DE SAÚDE (PS) | |
| Item | ITEM | |
| Level | NÍVEL (NV.) | |
| Mom | MAMÃE | |
| Money | POKÉMOEDA | dinheiro do jogo |
| Nature | NATUREZA | |
| Nickname | APELIDO | |
| Poké Ball | POKé BOLA | |
| Great Ball | GRANDE BOLA | |
| Ultra Ball | ULTRA BOLA | |
| Master Ball | BOLA MESTRA | |
| Premier Ball | BOLA PRESENTEADA | |
| Poké Mart | POKé MART | |
| Pokémon Center | CENTRO POKéMON | |
| Pokémon Contest | CONCURSO POKéMON | |
| Pokémon Professor | PROFESSOR POKéMON | |
| Pokémon Trainer | TREINADOR / TREINADORA POKéMON | flexiona |
| Potion | POÇÃO | |
| Super Potion | SUPERPOÇÃO | |
| Antidote | ANTÍDOTO | |
| Repel | REPELENTE | |
| Rival | RIVAL | |
| Route | ROTA | |
| Running Shoes | TÊNIS DE CORRER | Pokémon GO |
| Safari Zone | ZONA DE SAFÁRI | |
| Secret Base | BASE SECRETA | |
| Stat | ATRIBUTO | |
| Ability | HABILIDADE | |
| Status condition | CONDIÇÃO DE STATUS | |
| TM | MÁQUINA TÉCNICA (MT) | |
| Type | TIPO | |

Os tipos: NORMAL, FOGO, ÁGUA, PLANTA, ELÉTRICO, GELO, LUTADOR, VENENOSO,
TERRESTRE, VOADOR, PSÍQUICO, INSETO, PEDRA, FANTASMA, DRAGÃO, SOMBRIO, AÇO.

Os nomes dos POKéMON não se traduzem.

## Sem nome oficial no Brasil (escolhas do projeto)

| Inglês | Português | Motivo |
| :--- | :--- | :--- |
| Battle Frontier | FRONTEIRA DE BATALHA | Hoenn não teve localização no Brasil |
| Littleroot Town e as outras cidades | CIDADE DE LITTLEROOT | o nome fica, a parte genérica se traduz |
| Pokémon Wireless Club | CLUBE SEM FIO POKéMON | |
| Trainer Card (Gold/Silver) | CARTÃO DE OURO / DE PRATA | |
| Key Items | ITENS CHAVE | só "Objeto Chave", num manual; sem hífen para caber no bolso da BOLSA |
| Dad | PAPAI | par de MAMÃE |
| Contest conditions (Cool, Beauty, Cute, Smart, Tough) | ESTILO, BELEZA, FOFURA, ESPERTEZA, FORÇA | |
| Hold item | item segurado (“Se segurado, …”) | |
| Mail | CARTA | |
| Cancel (menus) | VOLTAR | mesma largura de CANCEL, que algumas janelas têm exata |
| Toss | DESCARTAR | |
| Box (PC) | CAIXA | oficial |
| Coins | FICHAS | |

## Nomes de itens

Os nomes dos itens cabem em 13 bytes (`src/data/items.h`). Quando o nome
oficial não cabe, ele é abreviado no estilo do jogo: REPELENTE MÁX, REPELENTE
SUP, BOLA PRESENT. (BOLA PRESENTEADA nos diálogos), BOLA REPETIÇ., CURA
PARALIS., MÁX. REVIVER. As frutas são FRUTA + nome (FRUTA ORAN), como nos
jogos oficiais; as MÁQUINAS são MT01–MT50 e MO01–MO08. A lista completa, com
o nome escolhido para cada item, está em `src/data/items.h.txt`.

## Nomes de golpes

Os golpes têm o nome oficial brasileiro (o primeiro nome “games” do
Bulbapedia), em até 12 bytes (`src/data/text/move_names.h`): abreviado no
estilo do jogo quando não cabe (GOLPE CARATÊ, REV. D'ÁGUA, DANÇA ESPADA,
ATAQ. RÁPIDO). Quando há mais de um nome oficial, vale o dos jogos; quando
dois golpes ficariam iguais, um deles usa a alternativa do anime (SOCO
TROVÃO, VENTO GELADO, LANÇA GELO). A lista completa está em
`src/data/text/move_names.h.txt`.

## Nomes de habilidades

As habilidades seguem a mesma regra, em até 12 bytes
(`src/data/text/abilities.h`): ARM. BATALHA, ABS.VOLTAICA, INDULG. SER.,
SUPERCRESC. Quando o Bulbapedia não traz nome brasileiro (STENCH, SHIELD
DUST, ARENA TRAP, LIQUID OOZE, WHITE SMOKE, AIR LOCK, CACOPHONY), vale o da
cópia do HoennKantoWiki ou a tradução direta: FEDOR, PÓ ESCUDO, ARMAD.
ARENA, LODO LÍQUIDO, FUM. BRANCA, ECLUSA DE AR, CACOFONIA. FORECAST vira
PREV. TEMPO para não repetir o golpe PREVISÃO. A lista completa está em
`src/data/text/abilities.h.txt`.

## Mensagens de batalha

Localizadas, não traduzidas ao pé da letra: o que um narrador brasileiro
diria (“É super efetivo!”, “Não é muito efetivo…”, “Acerto crítico!”,
“Não dá pra fugir!”, “Manda ver, {B_BUFF1}!”).

- O POKéMON do oponente: “ZIGZAGOON selvagem”, “POLIWAG inimigo” (sufixo,
  patch 0041). Os POKéMON são tratados no masculino (o POKéMON).
- O lado de cada um: “a equipe aliada” / “a equipe inimiga”.
- Posse: “ATAQUE de MUDKIP”, “INTIMIDAÇÃO de GYARADOS” (a coisa antes do dono).
- Atributos nas mensagens: PS, ATAQUE, DEFESA, VELOC., ATQ. ESP., DEF. ESP.,
  precisão, evasão; na caixa de nível, ATQ.ESP. e DEF.ESP.
- Menus: LUTAR, BOLSA, POKéMON, FUGIR; no SAFÁRI, BOLA e CHEGAR.
- SAFARI BALL é BOLA SAFÁRI (como o item). REFEREE é JUIZ.

## Tipos e categorias

Os nomes dos tipos têm 6 bytes no jogo (a janela de golpes da batalha, o
resumo): NORMAL, LUTA, VOADOR, VENENO, TERRA, PEDRA, INSETO, FANTAS, AÇO,
FOGO, ÁGUA, PLANTA, ELÉTR., PSÍQ., GELO, DRAGÃO, SOMBR. Onde há espaço (as
mensagens, as descrições), os nomes inteiros da primeira tabela.

As categorias da POKéDEX vêm dos gêneros da cópia do HoennKantoWiki, em até
11 bytes, com “POKéMON” antes (patch 0042). Quando o nome não cabe, a
palavra portuguesa mais próxima: MIRMELEÃO (antlion), ERMITÃO, TATURANA,
BANANEIRA (handstand), OTÁRIA (sea lion), GUAXININHO, TOURO BRAVO.
