# -*- coding: utf-8 -*-
"""
Count glossary entries by type for ADictML.
Spyder-friendly version (no CLI args).

Assumptions:
- This script is located in a subfolder (e.g. assets/)
- The main TeX file is one folder above this script
"""

import re
from pathlib import Path
from collections import Counter

# ---------------- Configuration ----------------

MAIN_TEX_NAME = "ADictML_English.tex"
DEFAULT_TYPE = "ML"

# -----------------------------------------------

INPUT_RE = re.compile(r'\\input\{([^}]+)\}')
NEW_ENTRY_RE = re.compile(r'\\newglossaryentry\s*\{[^}]+\}\s*\{', re.MULTILINE)
TYPE_RE = re.compile(r'type\s*=\s*([a-zA-Z]+)')

def read_tex(path):
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin1")

def find_matching_brace(text, start):
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError(f"Unmatched brace in file")

def extract_glossary_entries(text):
    for m in NEW_ENTRY_RE.finditer(text):
        brace_start = m.end() - 1
        brace_end = find_matching_brace(text, brace_start)
        yield text[brace_start + 1 : brace_end]

def collect_tex_files(main_file):
    seen = set()
    stack = [main_file]

    while stack:
        current = stack.pop()
        if current in seen or not current.exists():
            continue
        seen.add(current)

        text = read_tex(current)
        for m in INPUT_RE.finditer(text):
            fname = m.group(1)
            if not fname.endswith(".tex"):
                fname += ".tex"
            stack.append((current.parent / fname).resolve())

    return seen

def main():
    script_dir = Path(__file__).resolve().parent
    main_tex = (script_dir / ".." / MAIN_TEX_NAME).resolve()

    if not main_tex.exists():
        raise FileNotFoundError(f"Main TeX file not found: {main_tex}")

    tex_files = collect_tex_files(main_tex)
    counts = Counter()
    total = 0

    for tex in tex_files:
        text = read_tex(tex)
        for entry_body in extract_glossary_entries(text):
            total += 1
            m = TYPE_RE.search(entry_body)
            if m:
                counts[m.group(1)] += 1
            else:
                counts[DEFAULT_TYPE] += 1

    print("\nGlossary entry counts by type")
    print("--------------------------------")
    for k in sorted(counts):
        print(f"{k:15s}: {counts[k]:4d}")
    print("--------------------------------")
    print(f"{'TOTAL':15s}: {total:4d}")
    print(f"\nScanned {len(tex_files)} TeX files.")

# Run automatically in Spyder
main()
