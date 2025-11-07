#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Flatten LaTeX glossary references by replacing \gls-like commands with plain text,
using definitions extracted from \newglossaryentry{...}{...} blocks.

Features:
- Safe comment stripping (keeps \%)
- Balanced-brace scanning (robust to long descriptions, figures, math, etc.)
- Supports \gls, \glspl, \Gls, \Glspl with *, [options]
- Capitalizes for \Gls/\Glspl
- Works even if the script is called from any folder

USAGE:
    python FlattenGlossary.py
or
    python FlattenGlossary.py -i FILE -g GLOSSARY -o OUTPUT
"""

from __future__ import annotations
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, Tuple


# ------------------ DEFAULT PATHS (one level up) ------------------ #
BASE_DIR = Path(__file__).parent.parent
DEFAULT_INPUT_TEX    = BASE_DIR / "ADictML_Glossary_English.tex"
DEFAULT_GLOSSARY_TEX = BASE_DIR / "ADictML_Glossary_English.tex"
DEFAULT_OUTPUT_TEX   = BASE_DIR / "assets/ADictML_Glossary_Expanded.tex"
# ------------------------------------------------------------------ #


# ----------------------- Utility: comments -------------------------
def remove_comments_keep_escaped_percent(text: str) -> str:
    """Remove LaTeX comments but preserve escaped percent signs (\%)."""
    out_lines = []
    for line in text.splitlines():
        i = 0
        kept = []
        while i < len(line):
            ch = line[i]
            if ch == '%':
                if i > 0 and line[i - 1] == '\\':
                    kept.append('%')
                    i += 1
                else:
                    break  # comment starts
            else:
                kept.append(ch)
                i += 1
        out_lines.append(''.join(kept))
    return '\n'.join(out_lines)


# ----------------- Utility: balanced brace parser ------------------
def extract_balanced(text: str, start: int, open_char='{', close_char='}') -> Tuple[str, int]:
    """Extract text inside a balanced pair of braces starting at 'start'."""
    if text[start] != open_char:
        raise ValueError(f"Expected '{open_char}' at position {start}")
    depth, i = 0, start
    inner = []
    while i < len(text):
        ch = text[i]
        if ch == open_char:
            depth += 1
            if depth > 1:
                inner.append(ch)
        elif ch == close_char:
            depth -= 1
            if depth == 0:
                return ''.join(inner), i + 1
            inner.append(ch)
        else:
            inner.append(ch)
        i += 1
    raise ValueError("No matching closing brace found")


# ----------------- Parse \newglossaryentry blocks ------------------
def parse_glossary_entries(tex: str) -> Dict[str, Dict[str, str]]:
    """Extract all glossary entries into a dict: key -> {fields}."""
    entries = {}
    i, n = 0, len(tex)
    cmd = r"\newglossaryentry"
    while i < n:
        j = tex.find(cmd, i)
        if j == -1:
            break
        k = j + len(cmd)
        while k < n and tex[k].isspace():
            k += 1
        if k >= n or tex[k] != '{':
            i = k
            continue
        key_str, k_after_key = extract_balanced(tex, k, '{', '}')
        k = k_after_key
        while k < n and tex[k].isspace():
            k += 1
        if k >= n or tex[k] != '{':
            i = k
            continue
        body_str, k_after_body = extract_balanced(tex, k, '{', '}')
        i = k_after_body
        fields = parse_glossary_body_fields(body_str)
        entries[key_str.strip()] = fields
    return entries


def parse_glossary_body_fields(body: str) -> Dict[str, str]:
    """Parse top-level field={...} pairs from inside a glossary entry."""
    res = {}
    i, n = 0, len(body)

    def skip_ws(p: int) -> int:
        while p < n and body[p].isspace():
            p += 1
        return p

    i = skip_ws(i)
    while i < n:
        start_name = i
        while i < n and (body[i].isalnum() or body[i] in ('_', '-')):
            i += 1
        field_name = body[start_name:i].strip()
        i = skip_ws(i)
        if i >= n or body[i] != '=':
            i += 1
            i = skip_ws(i)
            continue
        i += 1
        i = skip_ws(i)
        if i >= n or body[i] != '{':
            i += 1
            i = skip_ws(i)
            continue
        val, i_after = extract_balanced(body, i, '{', '}')
        res[field_name] = val
        i = skip_ws(i_after)
        while i < n and (body[i].isspace() or body[i] == ','):
            i += 1
        i = skip_ws(i)
    return res


# -------------------- Glossary replacement logic --------------------
def capitalize_first(s: str) -> str:
    return s[:1].upper() + s[1:] if s else s

def pick_singular(gls: Dict[str, str]) -> str:
    return gls.get('first') or gls.get('name') or gls.get('text') or ''

def pick_plural(gls: Dict[str, str], sing: str) -> str:
    plural = gls.get('firstplural') or gls.get('plural')
    if plural:
        return plural
    if sing.endswith('y') and len(sing) > 1 and sing[-2] not in 'aeiou':
        return sing[:-1] + 'ies'
    return sing + 's'

def build_gls_replacer(glossary: Dict[str, Dict[str, str]]):
    GLS_KEY = r'([^\{\}]+?)'

    def repl_plural_cap(m):
        key = m.group(1).strip()
        d = glossary.get(key, {})
        sing = pick_singular(d) or key
        return capitalize_first(pick_plural(d, sing))

    def repl_singular_cap(m):
        key = m.group(1).strip()
        d = glossary.get(key, {})
        return capitalize_first(pick_singular(d) or key)

    def repl_plural(m):
        key = m.group(1).strip()
        d = glossary.get(key, {})
        sing = pick_singular(d) or key
        return pick_plural(d, sing)

    def repl_singular(m):
        key = m.group(1).strip()
        d = glossary.get(key, {})
        return pick_singular(d) or key

    patterns = [
        (re.compile(r'\\Glspl\*?\s*(?:\[[^\]]*\])?\s*\{'+GLS_KEY+r'\}', re.DOTALL), repl_plural_cap),
        (re.compile(r'\\Gls\*?\s*(?:\[[^\]]*\])?\s*\{'+GLS_KEY+r'\}', re.DOTALL), repl_singular_cap),
        (re.compile(r'\\glspl\*?\s*(?:\[[^\]]*\])?\s*\{'+GLS_KEY+r'\}', re.DOTALL), repl_plural),
        (re.compile(r'\\gls\*?\s*(?:\[[^\]]*\])?\s*\{'+GLS_KEY+r'\}', re.DOTALL), repl_singular),
    ]

    def replace_all(text: str) -> str:
        for pat, fn in patterns:
            text = pat.sub(fn, text)
        return text

    return replace_all


# ------------------------------ Main ---------------------------------
def flatten_tex(input_tex: Path, glossary_tex: Path, output_tex: Path) -> None:
    raw_in = input_tex.read_text(encoding='utf-8')
    raw_gls = glossary_tex.read_text(encoding='utf-8')
    in_nc = remove_comments_keep_escaped_percent(raw_in)
    gls_nc = remove_comments_keep_escaped_percent(raw_gls)
    entries = parse_glossary_entries(gls_nc)
    replacer = build_gls_replacer(entries)
    flattened = replacer(in_nc)
    output_tex.write_text(flattened, encoding='utf-8')
    print(f"[OK] Flattened file written to {output_tex}")


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Flatten \\gls macros in LaTeX files.")
    p.add_argument("-i", "--input", type=Path, default=DEFAULT_INPUT_TEX, help="Input .tex file to flatten")
    p.add_argument("-g", "--glossary", type=Path, default=DEFAULT_GLOSSARY_TEX, help="Glossary .tex with definitions")
    p.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT_TEX, help="Output flattened .tex file")
    return p.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    try:
        flatten_tex(args.input, args.glossary, args.output)
    except Exception as e:
        print("[ERROR]", e, file=sys.stderr)
        sys.exit(1)
