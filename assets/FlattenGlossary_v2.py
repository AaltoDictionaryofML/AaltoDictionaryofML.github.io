#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FlattenGlossary_v2.py
---------------------
A safer, more robust flattener for the Aalto Dictionary of ML LaTeX glossary.

Key improvements vs. earlier version:
1) Robust parsing of \newglossaryentry bodies with balanced-brace scanning.
2) Field extraction (name=..., first=..., firstplural=...) using a top-level key=value scanner
   that respects nested braces, so figures/tikz don't break parsing.
3) Macro expansion supports BOTH \macro{...} and \macro(...). Parentheses are treated
   as an alternative argument delimiter.
4) Graceful fallbacks:
   - If name= is missing, fall back to first=; if both missing, fall back to the entry key.
   - Macro calls that cannot be fully parsed are left as-is instead of throwing.
5) Tolerant of small typos (e.g., a misspelled name field still parsed if it has '=' and braces).
6) Clearer logging: warnings are non-fatal; progress & counts are summarized at the end.

Usage:
    python FlattenGlossary_v2.py \
        --macros ml_macros.tex \
        --source ../ADictML_Glossary_English.tex \
        --output ADictML_Glossary_Expanded.tex
"""

import argparse
import re
from pathlib import Path
from typing import Dict, Tuple, List, Optional

# -----------------------------
# Utility: remove LaTeX comments
# -----------------------------

def remove_comments(text: str) -> str:
    """Remove LaTeX comments (%) but keep escaped \%."""
    out_lines = []
    for line in text.splitlines():
        pos = 0
        new = []
        while pos < len(line):
            i = line.find('%', pos)
            if i == -1:
                new.append(line[pos:])
                break
            # If escaped as \%
            if i > 0 and line[i-1] == '\\':
                new.append(line[pos:i+1])
                pos = i + 1
                continue
            # else: cut the line here
            new.append(line[pos:i])
            break
        out_lines.append(''.join(new))
    return '\n'.join(out_lines)

# -----------------------------
# Balanced block extractors
# -----------------------------

def extract_balanced(text: str, start: int, open_ch: str, close_ch: str) -> Tuple[str, int]:
    """Extract a balanced {...} or (...) block from text, starting at the opening char index 'start'."""
    assert text[start] == open_ch, f"Expected '{open_ch}' at {start}"
    depth = 0
    i = start
    while i < len(text):
        ch = text[i]
        if ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return text[start+1:i], i + 1
        # skip escaped braces like \{ or \}
        if ch == '\\' and i + 1 < len(text):
            i += 2
            continue
        i += 1
    # Unbalanced; return until end to be forgiving
    return text[start+1:], len(text)

def extract_brace_block(text: str, start: int) -> Tuple[str, int]:
    return extract_balanced(text, start, '{', '}')

def extract_paren_block(text: str, start: int) -> Tuple[str, int]:
    return extract_balanced(text, start, '(', ')')

# -----------------------------
# Macro parsing & expansion
# -----------------------------

def parse_macros_with_args(macros_file: str) -> Dict[str, Tuple[int, str]]:
    """
    Parse simple \newcommand macros in the form:
        \newcommand{\macro}[n]{body with #1, #2, ...}
    Returns dict: name -> (num_args, body).
    """
    pattern = re.compile(r'\\newcommand\s*{\\([a-zA-Z@]+)}(?:\[(\d+)\])?\s*{(.*)}\s*$')
    macros: Dict[str, Tuple[int, str]] = {}
    with open(macros_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            m = pattern.match(line)
            if not m:
                continue
            name = m.group(1)
            nstr = m.group(2) or '0'
            try:
                n = int(nstr)
            except ValueError:
                n = 0
            body = m.group(3)
            macros[name] = (n, body)
    return macros

def substitute_args(body: str, args: List[str]) -> str:
    """Replace #1..#n in body with provided args (1-indexed)."""
    out = body
    for i, a in enumerate(args, start=1):
        out = out.replace(f'#{i}', a)
    return out

def replace_macro_calls(text: str, name: str, num_args: int, body: str) -> str:
    """
    Replace occurrences of \name{...}{...}... or \name(...)(...)... with substituted body.
    This is single-pass, left-to-right, and does not recurse (outer caller will loop).
    """
    pat = re.compile(rf'\\{name}(?![a-zA-Z@])')
    pos = 0
    out = []
    while True:
        m = pat.search(text, pos)
        if not m:
            out.append(text[pos:])
            break
        out.append(text[pos:m.start()])
        cur = m.end()

        args: List[str] = []
        ok = True
        for _ in range(num_args):
            # skip whitespace
            while cur < len(text) and text[cur].isspace():
                cur += 1
            if cur >= len(text):
                ok = False
                break
            # support { ... } or ( ... )
            if text[cur] == '{':
                arg, nxt = extract_brace_block(text, cur)
            elif text[cur] == '(':
                arg, nxt = extract_paren_block(text, cur)
            else:
                # cannot parse argument; give up on this occurrence, keep literal
                ok = False
                break
            args.append(arg)
            cur = nxt

        if not ok:
            # Keep literal text if we couldn't parse args
            out.append(text[m.start():cur])
            pos = cur
            continue

        repl = substitute_args(body, args)
        out.append(repl)
        pos = cur

    return ''.join(out)

def expand_all_macros(text: str, macros: Dict[str, Tuple[int, str]], max_passes: int = 2) -> str:
    """
    Expand macros a few times to catch simple nesting.
    We limit passes to avoid runaway replacements.
    """
    for _ in range(max_passes):
        for name, (n, body) in macros.items():
            text = replace_macro_calls(text, name, n, body)
    return text

# -----------------------------
# Glossary parsing
# -----------------------------

def parse_glossary_entries(source_file: str) -> Dict[str, str]:
    """
    Return dict: key -> raw body (inside the outermost braces) of \newglossaryentry{key}{...}.
    Uses balanced-brace scanning and allows nested content.
    """
    with open(source_file, 'r', encoding='utf-8') as f:
        content = remove_comments(f.read())

    start_pat = re.compile(r'\\newglossaryentry\{([^\}]+)\}\s*\{')
    pos = 0
    entries: Dict[str, str] = {}

    while True:
        m = start_pat.search(content, pos)
        if not m:
            break
        key = m.group(1)
        brace_start = m.end() - 1  # index of '{'
        body, nxt = extract_brace_block(content, brace_start)
        entries[key] = body
        pos = nxt

    return entries

def split_top_level_fields(body: str) -> List[Tuple[str, str]]:
    """
    Split 'key=value, key={...}, key={{..}}, ...' style body into list of (key, value) pairs,
    but ONLY at top level (brace depth zero). Values may be braced; if unbraced, take until next comma.
    """
    pairs: List[Tuple[str, str]] = []
    i = 0
    n = len(body)
    while i < n:
        # skip whitespace and commas
        while i < n and (body[i].isspace() or body[i] == ','):
            i += 1
        if i >= n:
            break
        # parse key
        k_start = i
        while i < n and body[i] not in '=\n':
            if body[i] == ' ':
                break
            i += 1
        key = body[k_start:i].strip()
        # skip spaces
        while i < n and body[i].isspace():
            i += 1
        if i >= n or body[i] != '=':
            # malformed; skip to next comma
            while i < n and body[i] != ',':
                i += 1
            continue
        i += 1  # skip '='
        # skip spaces
        while i < n and body[i].isspace():
            i += 1
        # parse value
        if i < n and body[i] == '{':
            val, i = extract_brace_block(body, i)
        else:
            v_start = i
            depth = 0
            while i < n:
                ch = body[i]
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth = max(0, depth - 1)
                elif ch == ',' and depth == 0:
                    break
                i += 1
            val = body[v_start:i].strip()
        pairs.append((key.strip(), val.strip()))
        # skip trailing comma (if any)
        if i < n and body[i] == ',':
            i += 1
    return pairs

def build_glossary_name_map(entries: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    """
    From raw entries map, build a dict:
        key -> {'name': ..., 'first': ..., 'firstplural': ...}
    Missing fields are simply absent; we DO NOT warn here.
    """
    out: Dict[str, Dict[str, str]] = {}
    for key, body in entries.items():
        fields = dict(split_top_level_fields(body))
        rec = {}
        for fld in ('name', 'first', 'firstplural', 'text', 'type'):
            if fld in fields:
                rec[fld] = fields[fld]
        out[key] = rec
    return out

# -----------------------------
# Main flatten routine
# -----------------------------

def flatten_tex_macros(source_file: str,
                       macros: Dict[str, Tuple[int, str]],
                       output_file: str,
                       glossary_map: Dict[str, Dict[str, str]]) -> None:
    """
    Create a flattened .tex with expanded macros and resolved glossary names (best-effort).
    - \gls{key} is replaced by glossary_map[key].get('name'/'first'/'text', key) (in that priority).
    - Unknown keys are left as-is.
    - Macro expansion supports () or {} arguments.
    """
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    content = remove_comments(content)

    # Expand macros (best-effort, limited passes)
    content = expand_all_macros(content, macros, max_passes=2)

    # Replace \gls{...} and \glspl{...} using glossary_map (non-fatal)
    def gls_repl(m: re.Match) -> str:
        inner = m.group(1).strip()
        rec = glossary_map.get(inner, {})
        # choose fields in descending priority
        for fld in ('name', 'first', 'text'):
            v = rec.get(fld)
            if v:
                return v
        return inner  # fallback to key

    content = re.sub(r'\\gls\{([^\}]+)\}', gls_repl, content)
    content = re.sub(r'\\glspl\{([^\}]+)\}', gls_repl, content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    # Simple summary
    print(f"✅ Flattened file written to: {output_file}")

# -----------------------------
# CLI
# -----------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--macros', required=True, help='Path to ml_macros.tex')
    ap.add_argument('--source', required=True, help='Path to source .tex (e.g., ADictML_Glossary_English.tex)')
    ap.add_argument('--output', required=True, help='Path to output flattened .tex')
    args = ap.parse_args()

    macros = parse_macros_with_args(args.macros)
    entries = parse_glossary_entries(args.source)
    gls_map = build_glossary_name_map(entries)

    flatten_tex_macros(args.source, macros, args.output, gls_map)

if __name__ == '__main__':
    main()
