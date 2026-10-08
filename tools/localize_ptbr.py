#!/usr/bin/env python3
"""Stage the Brazilian Portuguese (PT-BR) texts into a bootstrapped tree.

The catalog is tools/locales/ptbr/*.toml (the wiki/ copy is source material,
not catalog). Each table is a source file of the tree; each key names a text by
its symbol and each value is the text in the decomp's own string syntax:

    ["src/data/text/move_descriptions.h"]
    sThunderboltDescription = 'Um forte raio elétrico\\nque pode paralisar o alvo.'

    ["src/data/text/move_names.h"]
    "gMoveNames[MOVE_POUND]" = 'PANCADA'

    ["src/data/items.h"]
    "gItems[ITEM_POTION].name" = 'POÇÃO'

    ["data/maps/Route101/scripts.inc"]
    Route101_Text_HelpMe = 'S-socorro!$'

Use TOML literal strings ('...' or '''...''') so \\n, \\p and \\l stay as
written. Texts the catalog does not name stay in English. Every reference and
every character is checked before the tree is touched; a missing symbol means
the upstream changed and the catalog needs updating.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "tools/locales/ptbr"
MARKER = ".emerald3ds-locale"
LANGUAGE_LINE = "#define GAME_LANGUAGE (LANGUAGE_ENGLISH)"
FLAG = "#define PORT_LOCALE_PTBR 1"


class CatalogError(ValueError):
    pass


def catalog_files() -> list[Path]:
    return sorted(CATALOG.glob("*.toml"))


def catalog_digest() -> str:
    """Changes whenever a catalog file or this script changes."""
    digest = hashlib.sha256(Path(__file__).read_bytes())
    for path in catalog_files():
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()[:16]


def load_catalog() -> dict[str, dict[str, tuple[str, str]]]:
    """{source file: {reference: (text, catalog file)}}"""
    merged: dict[str, dict[str, tuple[str, str]]] = {}
    for path in catalog_files():
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as error:
            raise CatalogError(f"{path.name}: {error}") from None
        for source, texts in data.items():
            if not isinstance(texts, dict):
                raise CatalogError(f"{path.name}: [{source}] must be a table of texts")
            entries = merged.setdefault(source, {})
            for ref, text in texts.items():
                if not isinstance(text, str):
                    raise CatalogError(f"{path.name}: {ref} must be a string")
                if ref in entries:
                    raise CatalogError(f"{ref} traduzido duas vezes ({entries[ref][1]}, {path.name})")
                entries[ref] = (text, path.name)
    return merged


# --- charset -----------------------------------------------------------------

@dataclass
class Charset:
    chars: set[str]
    escapes: set[str]
    names: set[str]

    @classmethod
    def read(cls, path: Path) -> "Charset":
        chars, escapes, names = set(), set(), set()
        for line in path.read_text(encoding="utf-8").splitlines():
            if m := re.match(r"^'(\\?.)'\s*=", line):
                c = m.group(1)
                if c == "\\'":
                    chars.add("'")  # written '\'' in the charmap, plain ' in texts
                else:
                    (escapes if c.startswith("\\") else chars).add(c)
            elif m := re.match(r"^([A-Z_][A-Z0-9_]*)\s*=", line):
                names.add(m.group(1))
        return cls(chars, escapes, names)

    def problems(self, text: str) -> list[str]:
        found, i = [], 0
        while i < len(text):
            c = text[i]
            if c == "{":
                end = text.find("}", i)
                if end < 0:
                    return found + ["'{' sem '}'"]
                word = text[i + 1:end].split()
                if not word or word[0] not in self.names:
                    found.append("código {" + text[i + 1:end] + "} desconhecido")
                i = end + 1
            elif c == "\\":
                if text[i:i + 2] not in self.escapes:
                    found.append("escape " + text[i:i + 2] + " desconhecido")
                i += 2
            else:
                if c == '"':
                    found.append('aspas " (use “ ”)')
                elif c not in self.chars:
                    found.append(f"caractere {c!r} não existe na fonte do jogo")
                i += 1
        return found


# --- C sources -----------------------------------------------------------------

def skip_literal(text: str, i: int) -> int:
    """Index after the string or char literal starting at text[i]."""
    quote, i = text[i], i + 1
    while text[i] != quote:
        i += 2 if text[i] == "\\" else 1
    return i + 1


def skip_comment(text: str, i: int) -> int:
    if text.startswith("//", i):
        end = text.find("\n", i)
        return len(text) if end < 0 else end
    return text.index("*/", i) + 2


def matching(text: str, i: int) -> int:
    """Index of the bracket closing the one at text[i]."""
    pairs = {"(": ")", "{": "}", "[": "]"}
    stack = [pairs[text[i]]]
    i += 1
    while stack:
        c = text[i]
        if c in "\"'":
            i = skip_literal(text, i)
            continue
        if text.startswith("//", i) or text.startswith("/*", i):
            i = skip_comment(text, i)
            continue
        if c in pairs:
            stack.append(pairs[c])
        elif c in ")}]":
            if c != stack.pop():
                raise CatalogError("brackets do not match")
        i += 1
    return i - 1


def top_level(text: str, start: int, end: int, pattern: re.Pattern) -> list[re.Match]:
    """Matches of pattern at the first nesting level of text[start:end]."""
    found, i = [], start
    while i < end:
        c = text[i]
        m = pattern.match(text, i, end)
        if m:
            found.append(m)
            i = m.end()
        elif c in "\"'":
            i = skip_literal(text, i)
        elif text.startswith("//", i) or text.startswith("/*", i):
            i = skip_comment(text, i)
        elif c in "({[":
            i = matching(text, i) + 1
        else:
            i += 1
    return found


def string_call(text: str, at: int) -> tuple[int, int, str]:
    """(start, end, original text) of the _( ... ) call starting at text[at]."""
    if not text.startswith("_(", at):
        raise CatalogError("não é um texto _(\"...\")")
    close = matching(text, at + 1)
    parts, i = [], at + 2
    while i < close:
        if text[i] == '"':
            end = skip_literal(text, i)
            parts.append(text[i + 1:end - 1])
            i = end
        elif text.startswith("//", i) or text.startswith("/*", i):
            i = skip_comment(text, i)
        elif text[i].isspace():
            i += 1
        else:
            raise CatalogError("_( ) com algo além de textos")
    return at, close + 1, "".join(parts)


REF = re.compile(r"^([A-Za-z_]\w*)(?:\[\s*([A-Za-z_0-9]+)\s*\])?(?:\.([A-Za-z_]\w*))?$")


def locate_c(text: str, ref: str) -> tuple[int, int, str]:
    m = REF.match(ref)
    if not m:
        raise CatalogError("referência inválida (use nome, nome[INDICE] ou nome[INDICE].campo)")
    name, index, field = m.groups()
    if field and not index:
        raise CatalogError("campo sem índice")
    head = rf"\b{name}\s*(?:\[[^\]]*\]\s*)+=\s*"
    if index is None:
        defs = list(re.finditer(head + r"_\(", text))
        if len(defs) != 1:
            raise CatalogError("símbolo não encontrado" if not defs else "símbolo definido mais de uma vez")
        return string_call(text, defs[0].end() - 2)
    defs = list(re.finditer(head + r"\{", text))
    if len(defs) != 1:
        raise CatalogError("tabela não encontrada" if not defs else "tabela definida mais de uma vez")
    open_brace = defs[0].end() - 1
    close_brace = matching(text, open_brace)
    entries = top_level(text, open_brace + 1, close_brace,
                        re.compile(rf"\[\s*{index}\s*\]\s*=\s*"))
    if len(entries) != 1:
        raise CatalogError(f"[{index}] não encontrado na tabela" if not entries else f"[{index}] repetido")
    at = entries[0].end()
    if field is None:
        return string_call(text, at)
    if text[at] != "{":
        raise CatalogError(f"[{index}] não é uma estrutura")
    fields = top_level(text, at + 1, matching(text, at), re.compile(rf"\.{field}\s*=\s*"))
    if len(fields) != 1:
        raise CatalogError(f".{field} não encontrado")
    return string_call(text, fields[0].end())


# --- assembly sources ------------------------------------------------------------

STRING_LINE = re.compile(r'[ \t]*\.string[ \t]+"((?:[^"\\]|\\.)*)"[ \t]*(?:@.*)?\n?')


def locate_asm(text: str, ref: str) -> tuple[int, int, str]:
    labels = list(re.finditer(rf"^{re.escape(ref)}::?[ \t]*\n", text, re.M))
    if len(labels) != 1:
        raise CatalogError("rótulo não encontrado" if not labels else "rótulo repetido")
    start = i = labels[0].end()
    parts = []
    while m := STRING_LINE.match(text, i):
        parts.append(m.group(1))
        i = m.end()
    if not parts:
        raise CatalogError("o rótulo não é seguido de .string")
    return start, i, "".join(parts)


# --- staging -----------------------------------------------------------------------

def render(value: str, asm: bool) -> str:
    """The text in the decomp's layout: one source line per line of the game."""
    lines = [line for line in re.split(r"(?<=\\[npl])", value) if line]
    if asm:
        return "".join(f'\t.string "{line}"\n' for line in lines)
    if len(lines) == 1:
        return f'_("{value}")'
    return "_(\n" + "\n".join(f'    "{line}"' for line in lines) + ")"


def localize(tree: Path, catalog: dict[str, dict[str, tuple[str, str]]]) -> dict[Path, str]:
    charset = Charset.read(tree / "charmap.txt")
    errors, writes = [], {}
    for source, entries in sorted(catalog.items()):
        path = tree / source
        if not path.is_file():
            errors.append(f"{source}: arquivo não existe na árvore")
            continue
        text = path.read_text(encoding="utf-8")
        asm = path.suffix in (".inc", ".s")
        spans = []
        for ref, (value, origin) in sorted(entries.items()):
            where = f"{origin}: [{source}] {ref}"
            try:
                start, end, original = (locate_asm if asm else locate_c)(text, ref)
            except CatalogError as error:
                errors.append(f"{where}: {error}")
                continue
            problems = charset.problems(value)
            if asm and original.endswith("$") and not value.endswith("$"):
                problems.append("falta o $ no fim, como no original")
            if "$" in value[:-1] or (not asm and value.endswith("$")):
                problems.append("$ só no fim de um texto de script")
            if problems:
                errors.append(f"{where}: " + "; ".join(problems))
                continue
            spans.append((start, end, render(value, asm)))
        spans.sort()
        for (_, end_a, _), (start_b, _, _) in zip(spans, spans[1:]):
            if start_b < end_a:
                errors.append(f"{source}: duas referências apontam para o mesmo texto")
        for start, end, replacement in reversed(spans):
            text = text[:start] + replacement + text[end:]
        writes[path] = text
    if errors:
        raise CatalogError("\n".join(errors))

    global_h = tree / "include/constants/global.h"
    text = global_h.read_text(encoding="utf-8")
    if FLAG not in text:
        if LANGUAGE_LINE not in text:
            raise CatalogError("include/constants/global.h: GAME_LANGUAGE não está em inglês")
        text = text.replace(LANGUAGE_LINE, LANGUAGE_LINE + "\n" + FLAG)
    writes[global_h] = text
    return writes


def stage(tree: Path) -> int:
    catalog = load_catalog()
    writes = localize(tree, catalog)
    changed = 0
    for path, text in writes.items():
        data = text.encode("utf-8")
        if path.read_bytes() != data:
            path.write_bytes(data)
            changed += 1
    (tree / MARKER).write_text("PTBR " + catalog_digest() + "\n")
    count = sum(len(entries) for entries in catalog.values())
    print(f"localize_ptbr: {count} textos em {len(catalog)} arquivos, {changed} arquivos alterados")
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tree", type=Path, required=True)
    args = parser.parse_args()
    try:
        stage(args.tree.resolve())
    except CatalogError as error:
        print("localize_ptbr: o catálogo não foi aplicado:\n" + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
