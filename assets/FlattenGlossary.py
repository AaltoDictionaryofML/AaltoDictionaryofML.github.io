#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate *_expanded.tex variants for all reachable LaTeX files (NO HASHES)
and generate a main file ADictML_English_Expanded.tex that is identical to
ADictML_English.tex except it inputs the expanded variants.

Assumptions (your repo layout)
------------------------------
- This script lives in: <repo>/assets/FlattenGlossary.py
- Repo root is:         <repo>/
- Main file is:         ADictML_English.tex (in repo root)

Outputs (all written to assets/)
-------------------------------
- For each reachable .tex file: <stem>_expanded.tex
  Example: ADictML_Glossary_English.tex -> assets/ADictML_Glossary_English_expanded.tex
- Special main output: assets/ADictML_English_Expanded.tex
  (same as original main, but inputs expanded variants)

What "expanded" means
---------------------
- Strip comments (preserving escaped %)
- Expand macros from a macros file (\\newcommand/\\renewcommand/\\providecommand)
- Replace \\gls/\\Gls/\\glspl/\\Glspl (and *-variants) with plain text using \\newglossaryentry database
- Rewrite \\input/\\include arguments to point to expanded file stems (no .tex extension)

Run
---
From repo root:
    python assets/FlattenGlossary.py -i ADictML_English.tex -g ADictML_English.tex -m assets/ml_macros.tex

Compile
-------
    cd assets
    latexmk -pdf ADictML_English_Expanded.tex
"""

from __future__ import annotations

import re
import sys
import argparse
from pathlib import Path
from typing import Dict, Tuple, Optional, Set, List

# -------------------------------------------------------------------
# Paths: script sits in <repo>/assets/
# -------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent          # .../assets
PROJECT_ROOT = SCRIPT_DIR.parent                      # .../ (repo root)

# Defaults (relative to repo root)
DEFAULT_MAIN = Path("ADictML_English.tex")
DEFAULT_GLOSSARY = Path("ADictML_English.tex")        # often simplest: parse glossary from same tree
DEFAULT_MACROS = Path("assets/ml_macros.tex")

SPECIAL_MAIN_OUT_NAME = "ADictML_English_Expanded.tex"  # exact name requested

# -------------------------------------------------------------------
# Utility: interpret CLI paths relative to repo root (NOT current cwd)
# -------------------------------------------------------------------
def resolve_cli_path(p: Path) -> Path:
    return (PROJECT_ROOT / p).resolve() if not p.is_absolute() else p.resolve()

# ----------------------- Utility: comments -------------------------
def remove_comments_keep_escaped_percent(text: str) -> str:
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
                    break
            else:
                kept.append(ch)
                i += 1
        out_lines.append(''.join(kept))
    return '\n'.join(out_lines)

# ----------------- Utility: balanced block parsers ------------------
def extract_balanced(text: str, start: int, open_char='{', close_char='}') -> Tuple[str, int]:
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
    raise ValueError("No matching ']' found")

# ------------------ \\input / \\include handling --------------------
_INPUTLIKE_RE = re.compile(r'\\(input|include)\s*\{([^}]+)\}', re.IGNORECASE)

def _resolve_tex_path(ref: str, base_dir: Path) -> Optional[Path]:
    """
    Resolve \\input{...}/\\include{...} into an existing .tex file.
    Strategy:
      1) relative to including file directory
      2) relative to repo root
      3) relative to assets
    Supports missing .tex extension.
    """
    ref = ref.strip()
    if not ref:
        return None

    if (ref.startswith('"') and ref.endswith('"')) or (ref.startswith("'") and ref.endswith("'")):
        ref = ref[1:-1].strip()

    candidates: List[Path] = []

    # relative to including file
    p = (base_dir / ref).expanduser()
    candidates.append(p)
    if p.suffix == "":
        candidates.append(p.with_suffix(".tex"))

    # relative to repo root
    q = (PROJECT_ROOT / ref).expanduser()
    candidates.append(q)
    if q.suffix == "":
        candidates.append(q.with_suffix(".tex"))

    # relative to assets
    r = (SCRIPT_DIR / ref).expanduser()
    candidates.append(r)
    if r.suffix == "":
        candidates.append(r.with_suffix(".tex"))

    for c in candidates:
        if c.exists() and c.is_file():
            return c.resolve()

    return None

def collect_tex_files(entry: Path, visited: Optional[Set[Path]] = None, unresolved: Optional[List[str]] = None) -> Set[Path]:
    if visited is None:
        visited = set()
    if unresolved is None:
        unresolved = []

    entry = entry.resolve()
    if entry in visited or not entry.exists():
        return visited
    visited.add(entry)

    try:
        raw = entry.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw = entry.read_text(encoding="latin-1")

    no_comments = remove_comments_keep_escaped_percent(raw)
    base_dir = entry.parent

    for m in _INPUTLIKE_RE.finditer(no_comments):
        ref = m.group(2)
        child = _resolve_tex_path(ref, base_dir)
        if child is None:
            unresolved.append(f"{entry}: \\{m.group(1)}{{{ref}}}")
            continue
        collect_tex_files(child, visited, unresolved)

    return visited

def load_tex_with_inputs(entry_file: Path, visited: Optional[Set[Path]] = None) -> str:
    """Inline inputs recursively (used for building glossary dict)."""
    if visited is None:
        visited = set()

    entry_file = entry_file.resolve()
    if entry_file in visited or not entry_file.exists():
        return ""
    visited.add(entry_file)

    try:
        raw = entry_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw = entry_file.read_text(encoding="latin-1")

    no_comments = remove_comments_keep_escaped_percent(raw)
    base_dir = entry_file.parent

    out_parts: List[str] = []
    pos = 0
    for m in _INPUTLIKE_RE.finditer(no_comments):
        out_parts.append(no_comments[pos:m.start()])
        ref = m.group(2)
        child = _resolve_tex_path(ref, base_dir)
        if child is not None:
            out_parts.append(load_tex_with_inputs(child, visited))
        else:
            out_parts.append(no_comments[m.start():m.end()])
        pos = m.end()
    out_parts.append(no_comments[pos:])
    return "\n".join(out_parts)

def load_glossary_source(glossary_src: Path) -> str:
    glossary_src = glossary_src.resolve()
    if glossary_src.is_dir():
        parts = []
        for f in sorted(glossary_src.rglob("*.tex")):
            parts.append(load_tex_with_inputs(f))
        return "\n".join(parts)
    return load_tex_with_inputs(glossary_src)

# ----------------- Parse \\newglossaryentry blocks ------------------
def parse_glossary_entries(tex: str) -> Dict[str, Dict[str, str]]:
    entries: Dict[str, Dict[str, str]] = {}
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
        entries[key_str.strip()] = parse_glossary_body_fields(body_str)
    return entries

def parse_glossary_body_fields(body: str) -> Dict[str, str]:
    res: Dict[str, str] = {}
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
        i = i_after
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
        self.name = name
        self.nargs = nargs
        self.opt_default = opt_default
        self.body = body

def parse_newcommand_block(tex: str, i: int) -> Tuple[Optional[MacroDef], int]:
    n = len(tex)
    while i < n and not tex[i].isspace() and tex[i] != '{':
        i += 1
    while i < n and tex[i].isspace():
        i += 1
    if i >= n or tex[i] != '{':
        return None, i

    cmd_name_block, j = extract_balanced(tex, i, '{', '}')
    name = cmd_name_block.strip()
    if not name.startswith('\\'):
        return None, j
    name = name[1:]

    nargs = 0
    opt_default: Optional[str] = None
    k = j
    while k < n and tex[k].isspace():
        k += 1
    if k < n and tex[k] == '[':
        count_str, k = extract_bracketed(tex, k)
        try:
            nargs = int(count_str.strip())
        except ValueError:
            nargs = 0
        while k < n and tex[k].isspace():
            k += 1
        if k < n and tex[k] == '[':
            opt_default, k = extract_bracketed(tex, k)
        j = k
    else:
        j = k

    while j < n and tex[j].isspace():
        j += 1
    if j >= n or tex[j] != '{':
        return None, j
    body, j_after = extract_balanced(tex, j, '{', '}')
    return MacroDef(name=name, nargs=nargs, opt_default=opt_default, body=body), j_after

def parse_macros(tex: str) -> Dict[str, MacroDef]:
    macros: Dict[str, MacroDef] = {}
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
            j = start + 1
            macro = None
        if macro and macro.name:
            macros[macro.name] = macro
        i = j
    return macros

def _replace_args(body: str, args: Dict[int, str]) -> str:
    out = body
    for idx in sorted(args.keys(), reverse=True):
        out = out.replace(f"#{idx}", args[idx])
    return out

def expand_macros_once(text: str, macros: Dict[str, MacroDef]) -> Tuple[str, int]:
    if not macros:
        return text, 0
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

        out.append(text[i:m.start()])
        name = m.group(1)
        macro = macros.get(name)
        pos = m.end()
        fail_rewind = text[m.start():pos]

        opt_val: Optional[str] = None
        try:
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

            for _ in range(required):
                while pos < n and text[pos].isspace():
                    pos += 1
                if pos >= n or text[pos] != '{':
                    raise ValueError("Missing required argument")
                val, pos = extract_balanced(text, pos, '{', '}')
                args[next_idx] = val
                next_idx += 1

            out.append(_replace_args(macro.body, args))
            expansions += 1
            i = pos
        except Exception:
            out.append(fail_rewind)
            i = m.end()

    return ''.join(out), expansions

def expand_macros(text: str, macros: Dict[str, MacroDef], max_passes: int = 10) -> str:
    cur = text
    for _ in range(max_passes):
        cur, n_exp = expand_macros_once(cur, macros)
        if n_exp == 0:
            break
    return cur

# ---------------------- naming + input rewriting ----------------------
def expanded_filename(original: Path) -> str:
    """No hashes: <stem>_expanded.tex"""
    return f"{original.stem}_expanded.tex"

def rewrite_inputs_to_expanded(text: str, this_file: Path, mapping: Dict[Path, str], unresolved: List[str]) -> str:
    base_dir = this_file.resolve().parent

    def _repl(m: re.Match) -> str:
        cmd = m.group(1)
        ref = m.group(2)
        target = _resolve_tex_path(ref, base_dir)
        if target is None:
            unresolved.append(f"{this_file}: \\{cmd}{{{ref}}}")
            return m.group(0)
        target = target.resolve()
        if target not in mapping:
            unresolved.append(f"{this_file}: \\{cmd}{{{ref}}} (resolved to {target} but not in mapping)")
            return m.group(0)
        exp_stem = Path(mapping[target]).stem  # input by stem (no .tex)
        return f"\\{cmd}{{{exp_stem}}}"

    return _INPUTLIKE_RE.sub(_repl, text)

# ------------------------------ pipeline ------------------------------
def build_glossary_dict(glossary_src: Path, macros: Dict[str, MacroDef]) -> Dict[str, Dict[str, str]]:
    raw_gls = load_glossary_source(glossary_src)
    count_ng = raw_gls.count(r"\newglossaryentry")
    print(f"[INFO] Glossary raw: {count_ng} occurrences of \\newglossaryentry")
    gls_nc = remove_comments_keep_escaped_percent(raw_gls)
    gls_exp = expand_macros(gls_nc, macros)
    return parse_glossary_entries(gls_exp)

def expand_and_write(tex_file: Path,
                     glossary: Dict[str, Dict[str, str]],
                     macros: Dict[str, MacroDef],
                     mapping: Dict[Path, str],
                     unresolved: List[str]) -> Path:
    tex_file = tex_file.resolve()
    out_path = SCRIPT_DIR / mapping[tex_file]

    try:
        raw = tex_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw = tex_file.read_text(encoding="latin-1")

    nc = remove_comments_keep_escaped_percent(raw)
    mac_exp = expand_macros(nc, macros)

    replacer = build_gls_replacer(glossary)
    flattened = replacer(mac_exp)

    flattened = rewrite_inputs_to_expanded(flattened, tex_file, mapping, unresolved)

    header = (
        "%% ------------------------------------------------------------------\n"
        f"%% AUTO-GENERATED by {Path(__file__).name}\n"
        f"%% Source: {tex_file}\n"
        f"%% Repo root: {PROJECT_ROOT}\n"
        "%% ------------------------------------------------------------------\n\n"
    )
    out_path.write_text(header + flattened, encoding="utf-8")
    return out_path

def write_special_main(main_tex: Path,
                       glossary: Dict[str, Dict[str, str]],
                       macros: Dict[str, MacroDef],
                       mapping: Dict[Path, str]) -> Path:
    """
    Write assets/ADictML_English_Expanded.tex which is identical to the original main,
    except its \\input/\\include point to the expanded variants.
    We still apply macro expansion + gls replacement + comment stripping
    (so it is consistent with the other expanded files).
    """
    main_tex = main_tex.resolve()
    out_path = SCRIPT_DIR / SPECIAL_MAIN_OUT_NAME

    raw = main_tex.read_text(encoding="utf-8")
    nc = remove_comments_keep_escaped_percent(raw)
    mac_exp = expand_macros(nc, macros)
    replacer = build_gls_replacer(glossary)
    flattened = replacer(mac_exp)

    unresolved: List[str] = []
    flattened = rewrite_inputs_to_expanded(flattened, main_tex, mapping, unresolved)

    header = (
        "%% ------------------------------------------------------------------\n"
        f"%% AUTO-GENERATED by {Path(__file__).name}\n"
        f"%% Source main: {main_tex}\n"
        "%% This file is identical to the source main except that it inputs *_expanded.tex files.\n"
        "%% ------------------------------------------------------------------\n\n"
    )
    out_path.write_text(header + flattened, encoding="utf-8")

    if unresolved:
        print("\n[WARN] In special main, some \\input/\\include could not be rewritten (showing up to 20):")
        for line in unresolved[:20]:
            print("  ", line)

    return out_path

def run(main_tex: Path, glossary_src: Path, macros_tex: Path) -> None:
    main_tex = resolve_cli_path(main_tex)
    glossary_src = resolve_cli_path(glossary_src)
    macros_tex = resolve_cli_path(macros_tex)

    if not main_tex.exists():
        raise FileNotFoundError(f"Main input not found: {main_tex}")
    if not glossary_src.exists():
        raise FileNotFoundError(f"Glossary source not found: {glossary_src}")
    if not macros_tex.exists():
        raise FileNotFoundError(f"Macros file not found: {macros_tex}")

    # load macros
    raw_mac = macros_tex.read_text(encoding="utf-8")
    macros = parse_macros(remove_comments_keep_escaped_percent(raw_mac))

    # collect reachable files
    unresolved_collect: List[str] = []
    files: Set[Path] = set(collect_tex_files(main_tex, unresolved=unresolved_collect))

    if glossary_src.is_dir():
        for f in glossary_src.rglob("*.tex"):
            files |= set(collect_tex_files(f, unresolved=unresolved_collect))
    else:
        files |= set(collect_tex_files(glossary_src, unresolved=unresolved_collect))

    # ensure main is included
    files.add(main_tex.resolve())

    all_files = sorted({p.resolve() for p in files})

    # mapping (no hashes)
    mapping: Dict[Path, str] = {}
    collisions: Dict[str, List[Path]] = {}
    for p in all_files:
        name = expanded_filename(p)
        mapping[p] = name
        collisions.setdefault(name.lower(), []).append(p)

    bad = {k: v for k, v in collisions.items() if len(v) > 1}
    if bad:
        print("[ERROR] Filename collisions detected with no-hash naming:")
        for outname, paths in bad.items():
            print(f"  {outname}:")
            for pp in paths:
                print(f"    - {pp}")
        raise RuntimeError("Refusing to overwrite colliding expanded filenames. Rename sources or reintroduce disambiguation.")

    # glossary dict
    glossary = build_glossary_dict(glossary_src, macros)
    print(f"[OK] Found {len(all_files)} .tex files to expand.")
    print(f"[OK] Parsed {len(glossary)} glossary entries.")

    # expand/write all files
    unresolved_rewrite: List[str] = []
    for f in all_files:
        outp = expand_and_write(f, glossary, macros, mapping, unresolved_rewrite)
        print(f"[OK] {f.name} -> {outp.name}")

    # special main
    special = write_special_main(main_tex, glossary, macros, mapping)
    print(f"[OK] Special expanded main written: {special}")

    unresolved = unresolved_collect + unresolved_rewrite
    if unresolved:
        print("\n[WARN] Unresolved/unchanged \\input/\\include directives (showing up to 50):")
        for line in unresolved[:50]:
            print("  ", line)
        if len(unresolved) > 50:
            print(f"  ... and {len(unresolved) - 50} more")

    print("\n[DONE]")
    print(f"Compile from assets/: latexmk -pdf {SPECIAL_MAIN_OUT_NAME}")

# ------------------------------ CLI ---------------------------------
def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Generate no-hash *_expanded.tex into assets/ and a special ADictML_English_Expanded.tex that inputs expanded variants."
    )
    p.add_argument("-i", "--input", type=Path, default=DEFAULT_MAIN,
                   help="Main input .tex file (relative to repo root if not absolute)")
    p.add_argument("-g", "--glossary", type=Path, default=DEFAULT_GLOSSARY,
                   help="Glossary root (.tex or directory); relative to repo root if not absolute")
    p.add_argument("-m", "--macros", type=Path, default=DEFAULT_MACROS,
                   help="Macros file; relative to repo root if not absolute")
    return p.parse_args(argv)

if __name__ == "__main__":
    args = parse_args()
    try:
        run(args.input, args.glossary, args.macros)
    except Exception as e:
        print("[ERROR]", e, file=sys.stderr)
        sys.exit(1)
