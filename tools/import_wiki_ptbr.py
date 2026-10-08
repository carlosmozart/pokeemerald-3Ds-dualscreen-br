#!/usr/bin/env python3
"""Copy the Gen 3 PT-BR translations of the HoennKantoWiki into this project.

The wiki is only read, never modified. The copy keeps the Portuguese text and
the keys needed to match it; the wiki's English game text is left out, because
this repository holds no game content. Run it again to refresh the copy:

    python tools/import_wiki_ptbr.py --wiki ../HoennKantoWiki
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tools/locales/ptbr/wiki"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(name: str, data) -> int:
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                            encoding="utf-8")
    return len(data)


def tipos_pt(wiki: Path) -> dict[str, str]:
    source = (wiki / "js/core/types.js").read_text(encoding="utf-8")
    block = re.search(r"const TIPOS_PT = \{(.*?)\};", source, re.S)
    if block is None:
        raise ValueError("TIPOS_PT not found in js/core/types.js")
    return dict(re.findall(r'(\w+):\s*"([^"]+)"', block.group(1)))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki", type=Path, required=True)
    wiki = parser.parse_args().wiki.resolve()
    pt = load(wiki / "data/gen3/i18n/pt.json")
    items = load(wiki / "data/gen3/item-descriptions.json")
    commit = subprocess.run(["git", "-C", str(wiki), "rev-parse", "HEAD"],
                            capture_output=True, text=True, check=True).stdout.strip()

    OUT.mkdir(parents=True, exist_ok=True)
    counts = {
        "moves.json": write("moves.json", {k: v for k, v in pt["moves"].items() if v}),
        "abilities.json": write("abilities.json", {k: v for k, v in pt["abilities"].items() if v}),
        "pokedex.json": write("pokedex.json", {k: v for k, v in pt["pokedex"].items() if v}),
        "genera.json": write("genera.json", {k: v for k, v in pt["genera"].items() if v}),
        "items.json": write("items.json", {k: {"name": v["name"], "pt": v["pt"]}
                                           for k, v in items.items() if v.get("pt")}),
        "types.json": write("types.json", tipos_pt(wiki)),
    }
    write("source.json", {"repository": "HoennKantoWiki", "commit": commit,
                          "copied": date.today().isoformat(), "counts": counts})
    for name, count in counts.items():
        print(f"{name}: {count}")
    print("wiki commit", commit)


if __name__ == "__main__":
    main()
