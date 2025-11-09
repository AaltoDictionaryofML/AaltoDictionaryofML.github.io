#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Flatten LaTeX glossary references by replacing \\gls-like commands with plain text,
and expand \\newcommand-style macros from a macros file.

New features:
- Expands macros defined via \\newcommand/\\renewcommand/\\providecommand in assets/ml_macros.tex
  * Supports forms: \\newcommand{\\cmd}{...}, \\newcommand{\\cmd}[n]{...},
                   \\newcommand{\\cmd}[n][default]{...}
  * Optional arg (when a default is given) maps to #1; required args fill #2..#n.
- Macro expansion is applied to:
  (1) the glossary source (before parsing \\newglossaryentry), and
  (2) the main input .tex (before replacing \\gls* commands).
- Balanced parsing for braces/brackets; iterative expansion with safety cap.

USAGE:
    python FlattenGlossary.py
or
    python FlattenGlossary.py -i FILE -g GLOSSARY -m MACROS -o OUTPUT
"""

from __future__ import annotations
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, Tuple, Optional

# ------------------ DEFAULT PATHS (one level up) ------------------ #
BASE_DIR = Path(__file__).parent.parent
DEFAULT_INPUT_TEX    = BASE_DIR / "ADictML_Glossary_English.tex"
DEFAULT_GLOSSARY_TEX = BASE_DIR / "ADictML_Glossary_English.tex"
DEFAULT_MACROS_TEX   = BASE_DIR / "assets/ml_macros.tex"
DEFAULT_OUTPUT_TEX   = BASE_DIR / "assets/ADictML_Glossary_Expanded.tex"
# ------------------------------------------------------------------ #

# ----------------------- Utility: comments -------------------------
def remove_comments_keep_escaped_percent(text: str) -> str:
    """Remove LaTeX comments but preserve escaped percent signs (\\%)."""
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
                    break  # start of comment
            else:
                kept.append(ch)
                i += 1
        out_lines.append(''.join(kept))
    return '\n'.join(out_lines)

# ----------------- Utility: balanced block parsers ------------------
def extract_balanced(text: str, start: int, open_char='{', close_char='}') -> Tuple[str, int]:
    """Extract text inside a balanced pair of braces starting at 'start'."""
    if start >= len(text) or text[start] != open_char:
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
    raise ValueError("No matching closing delimiter found")

def extract_bracketed(text: str, start: int) -> Tuple[str, int]:
    """Extract text inside [ ... ] starting at 'start' (balanced not required, but we do simple)."""
    # Allow nested [] rarely appear in LaTeX optionals; we treat them as flat.
    if start >= len(text) or text[start] != '[':
        raise ValueError(f"Expected '[' at position {start}")
    i = start + 1
    buf = []
    while i < len(text):
        ch = text[i]
        if ch == ']':
            return ''.join(buf), i + 1
        buf.append(ch)
        i += 1
    raise ValueError("No matching ']' found for optional argument")

# ----------------- Parse \\newglossaryentry blocks ------------------
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
        i += 1  # skip '='
        i = skip_ws(i)
        if i >= n or body[i] != '{':
            i += 1
            i = skip_ws(i)
            continue
        val, i_after = extract_balanced(body, i, '{', '}')
        res[field_name] = val
        i = i_after
        # consume whitespace and commas separating fields
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

# ---------------------- Macro parsing & expansion --------------------
class MacroDef:
    __slots__ = ("name", "nargs", "opt_default", "body")
    def __init__(self, name: str, nargs: int, opt_default: Optional[str], body: str):
        self.name = name               # without leading backslash
        self.nargs = nargs             # total args (#1..#n); if opt_default is not None, #1 is optional
        self.opt_default = opt_default # string or None
        self.body = body               # body with #1..#n placeholders

def parse_newcommand_block(tex: str, i: int) -> Tuple[Optional[MacroDef], int]:
    """
    Parse a single \\newcommand/\\renewcommand/\\providecommand occurrence starting at index i.
    Returns (MacroDef or None if malformed, new_index).
    """
    n = len(tex)
    # skip the command itself
    while i < n and not tex[i].isspace() and tex[i] != '{':
        i += 1
    while i < n and tex[i].isspace():
        i += 1
    if i >= n or tex[i] != '{':
        return None, i
    # {\\name}
    cmd_name_block, j = extract_balanced(tex, i, '{', '}')
    name = cmd_name_block.strip()
    if not name.startswith('\\'):
        return None, j
    name = name[1:]  # drop leading backslash

    # optional [nargs]
    nargs = 0
    opt_default: Optional[str] = None
    k = j
    while k < n and tex[k].isspace():
        k += 1
    if k < n and tex[k] == '[':
        # [n]
        count_str, k = extract_bracketed(tex, k)
        try:
            nargs = int(count_str.strip())
        except ValueError:
            nargs = 0
        while k < n and tex[k].isspace():
            k += 1
        # optional [default]
        if k < n and tex[k] == '[':
            opt_default, k = extract_bracketed(tex, k)
        j = k
    else:
        j = k

    # body { ... }
    while j < n and tex[j].isspace():
        j += 1
    if j >= n or tex[j] != '{':
        return None, j
    body, j_after = extract_balanced(tex, j, '{', '}')

    # If no explicit nargs was given, LaTeX default is 0
    # If nargs==0 but default provided -> treat as 1 with optional? LaTeX doesn't allow [default] without [n]; keep strict.
    return MacroDef(name=name, nargs=nargs, opt_default=opt_default, body=body), j_after

def parse_macros(tex: str) -> Dict[str, MacroDef]:
    """
    Find all \\newcommand/\\renewcommand/\\providecommand definitions and return a dict.
    """
    macros: Dict[str, MacroDef] = {}
    # allow starred forms: \newcommand* etc.
    cmd_pattern = re.compile(r'\\(newcommand|renewcommand|providecommand)\*?')
    i = 0
    while True:
        m = cmd_pattern.search(tex, i)
        if not m:
            break
        start = m.end()
        try:
            macro, j = parse_newcommand_block(tex, start)
        except Exception:
            # skip this occurrence if malformed
            j = start + 1
            macro = None
        if macro and macro.name:
            macros[macro.name] = macro
        i = j
    return macros

def _replace_args(body: str, args: Dict[int, str]) -> str:
    # Replace #1..#9 (simple global replace, no recursion here)
    out = body
    # Replace higher indices first to avoid #1 inside #10 confusion
    for idx in sorted(args.keys(), reverse=True):
        out = out.replace(f"#{idx}", args[idx])
    return out

def expand_macros_once(text: str, macros: Dict[str, MacroDef]) -> Tuple[str, int]:
    """
    Do a single pass expansion over 'text'.
    Returns (new_text, num_expansions_done).
    """
    if not macros:
        return text, 0

    # Build alternation for fast detection
    name_alt = "|".join(re.escape(nm) for nm in sorted(macros.keys(), key=len, reverse=True))
    trigger_re = re.compile(r'\\(' + name_alt + r')\b')

    i = 0
    n = len(text)
    out = []
    expansions = 0

    while True:
        m = trigger_re.search(text, i)
        if not m:
            out.append(text[i:])
            break

        # keep text up to command
        out.append(text[i:m.start()])

        name = m.group(1)
        macro = macros.get(name)
        pos = m.end()

        # Save position in case parsing fails; we then output the literal and continue
        fail_rewind = text[m.start():pos]

        # Optional argument only if macro has an opt_default
        opt_val: Optional[str] = None
        try:
            # skip whitespace
            while pos < n and text[pos].isspace():
                pos += 1

            if macro.opt_default is not None:
                if pos < n and text[pos] == '[':
                    opt_val, pos = extract_bracketed(text, pos)
                else:
                    opt_val = macro.opt_default

                required = macro.nargs - 1
            else:
                required = macro.nargs

            args: Dict[int, str] = {}
            next_idx = 1
            if macro.opt_default is not None:
                args[next_idx] = opt_val if opt_val is not None else ""
                next_idx += 1

            # parse required {arg} blocks
            for _ in range(required):
                while pos < n and text[pos].isspace():
                    pos += 1
                if pos >= n or text[pos] != '{':
                    raise ValueError("Missing required argument")
                val, pos = extract_balanced(text, pos, '{', '}')
                args[next_idx] = val
                next_idx += 1

            # Build replacement
            replacement = _replace_args(macro.body, args)
            out.append(replacement)
            expansions += 1
            i = pos
        except Exception:
            # could not parse this occurrence; emit it literally and move on one char
            out.append(fail_rewind)
            i = m.end()

    return ''.join(out), expansions

def expand_macros(text: str, macros: Dict[str, MacroDef], max_passes: int = 10) -> str:
    """
    Iteratively expand macros until no more changes or max_passes reached.
    """
    current = text
    for _ in range(max_passes):
        current, n_exp = expand_macros_once(current, macros)
        if n_exp == 0:
            break
    return current

# ------------------------------ Main ---------------------------------
def flatten_tex(input_tex: Path, glossary_tex: Path, macros_tex: Path, output_tex: Path) -> None:
    # Load raw files
    raw_in = input_tex.read_text(encoding='utf-8')
    raw_gls = glossary_tex.read_text(encoding='utf-8')
    raw_mac = macros_tex.read_text(encoding='utf-8') if macros_tex.exists() else ""

    # Strip comments
    in_nc  = remove_comments_keep_escaped_percent(raw_in)
    gls_nc = remove_comments_keep_escaped_percent(raw_gls)
    mac_nc = remove_comments_keep_escaped_percent(raw_mac)

    # Parse macro definitions
    macros = parse_macros(mac_nc)

    # Expand macros within glossary source BEFORE parsing entries
    gls_expanded = expand_macros(gls_nc, macros)

    # Parse glossary entries (with macros already expanded inside fields)
    entries = parse_glossary_entries(gls_expanded)

    # Build glossary replacer
    replacer = build_gls_replacer(entries)

    # Expand macros in the input file, then replace \\gls* commands
    in_mac_expanded = expand_macros(in_nc, macros)
    flattened = replacer(in_mac_expanded)

    output_tex.write_text(flattened, encoding='utf-8')
    print(f"[OK] Flattened file written to {output_tex}")

def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Expand \\newcommand macros and flatten \\gls macros in LaTeX files.")
    p.add_argument("-i", "--input", type=Path, default=DEFAULT_INPUT_TEX, help="Input .tex file to process")
    p.add_argument("-g", "--glossary", type=Path, default=DEFAULT_GLOSSARY_TEX, help="Glossary .tex with \\newglossaryentry")
    p.add_argument("-m", "--macros", type=Path, default=DEFAULT_MACROS_TEX, help="Macros .tex with \\newcommand definitions")
    p.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT_TEX, help="Output flattened .tex file")
    return p.parse_args(argv)

if __name__ == "__main__":
    args = parse_args()
    try:
        flatten_tex(args.input, args.glossary, args.macros, args.output)
    except Exception as e:
        print("[ERROR]", e, file=sys.stderr)
        sys.exit(1)
