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
