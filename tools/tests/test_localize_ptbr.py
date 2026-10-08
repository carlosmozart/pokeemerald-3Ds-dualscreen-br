"""Host tests for tools/localize_ptbr.py: python -m unittest discover -s tools/tests"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import localize_ptbr as loc  # noqa: E402

CHARMAP = "\n".join(
    [f"'{c}'         = {i:02X}" for i, c in enumerate(" ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzáéêíçÍ!?.,…-", 1)]
    + ["'\\''         = B4", "'$'         = FF", "PLAYER      = FD 01", "COLOR       = FC 01",
       "'\\l' = FA @ scroll", "'\\p' = FB @ paragraph", "'\\n' = FE @ new line"]) + "\n"

C_SOURCE = """\
const u8 gText_NewGame[] = _("NEW GAME");
static const u8 sPoundDescription[] = _(
    "Pounds the foe with\\n"
    "forelegs or tail.");
// gText_NewGame mentioned in a comment
const u8 gMoveNames[MOVES_COUNT][MOVE_NAME_LENGTH + 1] = {
    [MOVE_NONE] = _("-"),
    [MOVE_POUND] = _("POUND"), // the first move
};
const struct Item gItems[] = {
    [ITEM_POTION] =
    {
        .name = _("POTION"),
        .description = sPotionDesc,
        .pocket = POCKET_ITEMS,
    },
};
"""

ASM_SOURCE = """\
Route101_Text_HelpMe:
\t.string "H-help me!$"

Route101_Text_PleaseHelp:
\t.string "Hello! You over there!\\n"
\t.string "Please! Help!\\p"
\t.string "{PLAYER}!$"

Route101_Text_After:
\t.string "Unchanged.$"
"""


class LocalizeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tree = Path(self.tmp.name)
        (self.tree / "include/constants").mkdir(parents=True)
        (self.tree / "src").mkdir()
        (self.tree / "data").mkdir()
        (self.tree / "charmap.txt").write_text(CHARMAP, encoding="utf-8")
        (self.tree / loc.Path("include/constants/global.h")).write_text(
            "#define GAME_LANGUAGE (LANGUAGE_ENGLISH)\n", encoding="utf-8")
        (self.tree / "src/strings.c").write_text(C_SOURCE, encoding="utf-8")
        (self.tree / "data/scripts.inc").write_text(ASM_SOURCE, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def run_catalog(self, source, entries):
        return loc.localize(self.tree, {source: {k: (v, "test.toml") for k, v in entries.items()}})

    def written(self, writes, relative):
        return writes[self.tree / relative]

    def test_c_symbol_table_and_field(self):
        writes = self.run_catalog("src/strings.c", {
            "gText_NewGame": "NOVO JOGO",
            "sPoundDescription": "Bate no oponente com\\npatas ou cauda.",
            "gMoveNames[MOVE_POUND]": "PANCADA",
            "gItems[ITEM_POTION].name": "POCA",
        })
        text = self.written(writes, "src/strings.c")
        self.assertIn('gText_NewGame[] = _("NOVO JOGO");', text)
        self.assertIn('_(\n    "Bate no oponente com\\n"\n    "patas ou cauda.");', text)
        self.assertIn('[MOVE_POUND] = _("PANCADA"), // the first move', text)
        self.assertIn('[MOVE_NONE] = _("-")', text)
        self.assertIn('.name = _("POCA"),', text)
        self.assertIn(".description = sPotionDesc", text)

    def test_asm_label(self):
        writes = self.run_catalog("data/scripts.inc", {
            "Route101_Text_PleaseHelp": "Olá! Você aí!\\nSocorro!\\p{PLAYER}!$",
        })
        text = self.written(writes, "data/scripts.inc")
        self.assertIn('Route101_Text_PleaseHelp:\n\t.string "Olá! Você aí!\\n"\n'
                      '\t.string "Socorro!\\p"\n\t.string "{PLAYER}!$"\n\nRoute101_Text_After:', text)
        self.assertIn('\t.string "H-help me!$"', text)

    def test_flag_keeps_english_language(self):
        writes = self.run_catalog("src/strings.c", {"gText_NewGame": "NOVO JOGO"})
        text = self.written(writes, "include/constants/global.h")
        self.assertIn("#define GAME_LANGUAGE (LANGUAGE_ENGLISH)\n#define PORT_LOCALE_PTBR 1", text)

    def test_idempotent(self):
        entries = {"Route101_Text_HelpMe": "S-socorro!$", "Route101_Text_PleaseHelp": "Oi!\\nOi!$"}
        first = self.written(self.run_catalog("data/scripts.inc", entries), "data/scripts.inc")
        (self.tree / "data/scripts.inc").write_text(first, encoding="utf-8")
        second = self.written(self.run_catalog("data/scripts.inc", entries), "data/scripts.inc")
        self.assertEqual(first, second)

    def assertRefused(self, source, entries, message):
        with self.assertRaises(loc.CatalogError) as caught:
            self.run_catalog(source, entries)
        self.assertIn(message, str(caught.exception))

    def test_missing_symbol(self):
        self.assertRefused("src/strings.c", {"gText_Gone": "X"}, "símbolo não encontrado")
        self.assertRefused("src/strings.c", {"gMoveNames[MOVE_TACKLE]": "X"}, "[MOVE_TACKLE] não encontrado")
        self.assertRefused("data/scripts.inc", {"Route101_Text_Gone": "X$"}, "rótulo não encontrado")
        self.assertRefused("src/missing.c", {"gText_NewGame": "X"}, "arquivo não existe")

    def test_charset(self):
        self.assertRefused("src/strings.c", {"gText_NewGame": "OPÇÕES"}, "'Õ' não existe na fonte")
        self.assertRefused("src/strings.c", {"gText_NewGame": "{NOPE}"}, "código {NOPE} desconhecido")
        self.assertRefused("src/strings.c", {"gText_NewGame": 'A "B"'}, "aspas")

    def test_terminator(self):
        self.assertRefused("data/scripts.inc", {"Route101_Text_HelpMe": "Socorro!"}, "falta o $")
        self.assertRefused("src/strings.c", {"gText_NewGame": "A$"}, "$ só no fim")

    def test_nothing_written_on_error(self):
        before = (self.tree / "src/strings.c").read_text(encoding="utf-8")
        with self.assertRaises(loc.CatalogError):
            self.run_catalog("src/strings.c", {"gText_NewGame": "OK", "gText_Gone": "X"})
        self.assertEqual(before, (self.tree / "src/strings.c").read_text(encoding="utf-8"))


class CatalogTest(unittest.TestCase):
    def test_duplicate_reference_across_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("a.toml", "b.toml"):
                (Path(tmp) / name).write_text('["src/strings.c"]\ngText_NewGame = \'X\'\n', encoding="utf-8")
            saved, loc.CATALOG = loc.CATALOG, Path(tmp)
            try:
                with self.assertRaises(loc.CatalogError) as caught:
                    loc.load_catalog()
            finally:
                loc.CATALOG = saved
        self.assertIn("traduzido duas vezes", str(caught.exception))

    def test_shipped_catalog_parses(self):
        catalog = loc.load_catalog()
        self.assertTrue(catalog)


if __name__ == "__main__":
    unittest.main()
