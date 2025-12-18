# -*- coding: utf-8 -*-
"""
Count glossary entries by type for ADictML, and update README.md + feed.xml,
using category titles parsed from ADictML_English.tex (\printglossary[...]).

Spyder-friendly (no CLI args).
"""

import re
from pathlib import Path
from collections import Counter
from datetime import datetime
import xml.etree.ElementTree as ET

# ---------------- Configuration ----------------

MAIN_TEX_NAME = "ADictML_English.tex"
DEFAULT_TYPE = "ML"

README_NAME = "README.md"
FEED_NAME = "feed.xml"

README_STATS_BEGIN = "<!-- ADICTML_STATS_BEGIN -->"
README_STATS_END   = "<!-- ADICTML_STATS_END -->"

FEED_STATS_PREFIX = "Current coverage:"

# -----------------------------------------------

INPUT_RE = re.compile(r'\\input\{([^}]+)\}')
NEW_ENTRY_RE = re.compile(r'\\newglossaryentry\s*\{[^}]+\}\s*\{', re.MULTILINE)
TYPE_RE = re.compile(r'type\s*=\s*([a-zA-Z]+)')

# Parse \printglossary[ ... ] blocks
PRINTGLOSSARY_RE = re.compile(r'\\printglossary\s*\[(.*?)\]', re.DOTALL)

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin1")

def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")

def find_matching_brace(text: str, start: int) -> int:
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError("Unmatched brace in file")

def extract_glossary_entries(text: str):
    for m in NEW_ENTRY_RE.finditer(text):
        brace_start = m.end() - 1
        brace_end = find_matching_brace(text, brace_start)
        yield text[brace_start + 1 : brace_end]

def collect_tex_files(main_file: Path):
    seen = set()
    stack = [main_file]

    while stack:
        current = stack.pop()
        if current in seen or not current.exists():
            continue
        seen.add(current)

        text = read_text(current)
        for m in INPUT_RE.finditer(text):
            fname = m.group(1).strip()
            if not fname.endswith(".tex"):
                fname += ".tex"
            stack.append((current.parent / fname).resolve())

    return seen

def _extract_opt_value(opts: str, key: str):
    """
    Extract key=value from a \printglossary option string.
    Handles:
      title={...}  title="..."  title=Word
      type=math
    """
    # title={...}
    m = re.search(rf'\b{re.escape(key)}\s*=\s*\{{([^}}]*)\}}', opts)
    if m:
        return m.group(1).strip()

    # title="..."
    m = re.search(rf'\b{re.escape(key)}\s*=\s*"([^"]*)"', opts)
    if m:
        return m.group(1).strip()

    # title=bareword (until comma or ])
    m = re.search(rf'\b{re.escape(key)}\s*=\s*([^,\]]+)', opts)
    if m:
        return m.group(1).strip()

    return None

def parse_category_titles_from_main(main_tex_text: str):
    """
    Returns a dict: type -> title, based on \printglossary[...] lines.
    For the default glossary (no type=...), we map DEFAULT_TYPE -> its title (if present).
    """
    type_to_title = {}

    for m in PRINTGLOSSARY_RE.finditer(main_tex_text):
        opts = m.group(1)

        gtype = _extract_opt_value(opts, "type")  # e.g., "math"
        title = _extract_opt_value(opts, "title") # e.g., "Mathematical Tools"

        # If no title is present, don't invent one
        if not title:
            continue

        if gtype:
            type_to_title[gtype] = title
        else:
            # This is the "default glossary" => use as label for DEFAULT_TYPE (ML)
            type_to_title[DEFAULT_TYPE] = title

    return type_to_title

def build_stats(counts: Counter, total: int, type_to_title: dict):
    """
    Returns:
      - lines for README bullet list
      - compact one-line stats string for RSS description
    """
    def label_for_type(t: str) -> str:
        return type_to_title.get(t, t)

    items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))

    readme_lines = [f"- **Total terms:** {total}"]
    for t, c in items:
        readme_lines.append(f"- **{label_for_type(t)}:** {c}")

    parts = [f"{label_for_type(t)} {c}" for t, c in items]
    rss_line = f"{FEED_STATS_PREFIX} {total} terms (" + " · ".join(parts) + ")."
    return readme_lines, rss_line

def update_readme(readme_path: Path, readme_lines, last_updated_str: str) -> bool:
    if not readme_path.exists():
        print(f"[WARN] README not found: {readme_path}")
        return False

    original = read_text(readme_path)

    block = "\n".join([
        README_STATS_BEGIN,
        "## 📘 Dictionary at a Glance",
        "",
        *readme_lines,
        f"- **Last updated:** {last_updated_str}",
        "",
        README_STATS_END,
        ""
    ])

    if README_STATS_BEGIN in original and README_STATS_END in original:
        pattern = re.compile(
            re.escape(README_STATS_BEGIN) + r".*?" + re.escape(README_STATS_END),
            flags=re.DOTALL
        )
        updated = pattern.sub(block.strip("\n"), original)
    else:
        if "\n---\n" in original:
            updated = original.replace("\n---\n", "\n---\n\n" + block, 1)
        else:
            lines = original.splitlines()
            if lines:
                updated = "\n".join([lines[0], "", block, *lines[1:]]) + "\n"
            else:
                updated = block

    if updated != original:
        write_text(readme_path, updated)
        return True
    return False

def update_feed(feed_path: Path, rss_stats_line: str) -> bool:
    if not feed_path.exists():
        print(f"[WARN] feed.xml not found: {feed_path}")
        return False

    original = read_text(feed_path)

    try:
        tree = ET.ElementTree(ET.fromstring(original))
    except ET.ParseError as e:
        print(f"[ERROR] Could not parse feed.xml as XML: {e}")
        return False

    root = tree.getroot()
    channel = root.find("channel")
    if channel is None:
        print("[ERROR] feed.xml missing <channel>.")
        return False

    desc = channel.find("description")
    if desc is None:
        print("[ERROR] feed.xml missing <description>.")
        return False

    base_desc = (desc.text or "").strip()

    # Remove previous stats line (strip everything after prefix)
    if FEED_STATS_PREFIX in base_desc:
        base_desc = base_desc.split(FEED_STATS_PREFIX, 1)[0].strip()
        base_desc = base_desc.rstrip(" .")

    new_desc = (base_desc + " " if base_desc else "") + rss_stats_line

    if new_desc != (desc.text or "").strip():
        desc.text = new_desc
        xml_bytes = ET.tostring(root, encoding="utf-8", xml_declaration=True)
        updated = xml_bytes.decode("utf-8")

        if updated != original:
            write_text(feed_path, updated)
            return True

    return False

def main():
    script_dir = Path(__file__).resolve().parent
    repo_root = (script_dir / "..").resolve()

    main_tex = (repo_root / MAIN_TEX_NAME).resolve()
    readme_path = (repo_root / README_NAME).resolve()
    feed_path = (repo_root / FEED_NAME).resolve()

    if not main_tex.exists():
        raise FileNotFoundError(f"Main TeX file not found: {main_tex}")

    main_tex_text = read_text(main_tex)

    # NEW: category titles from \printglossary[...] in ADictML_English.tex
    type_to_title = parse_category_titles_from_main(main_tex_text)
    if type_to_title:
        print("[INFO] Category titles from ADictML_English.tex:")
        for k in sorted(type_to_title):
            print(f"  - {k} -> {type_to_title[k]}")
    else:
        print("[WARN] No \\printglossary[...] titles found; falling back to raw type names.")

    tex_files = collect_tex_files(main_tex)

    counts = Counter()
    total = 0

    for tex in tex_files:
        text = read_text(tex)
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

    now = datetime.now()
    last_updated_str = now.strftime("%Y-%m-%d")

    readme_lines, rss_stats_line = build_stats(counts, total, type_to_title)

    changed_readme = update_readme(readme_path, readme_lines, last_updated_str)
    changed_feed = update_feed(feed_path, rss_stats_line)

    print(f"[OK] {readme_path.name} {'updated' if changed_readme else 'unchanged'}")
    print(f"[OK] {feed_path.name} {'updated' if changed_feed else 'unchanged'}")

# Run automatically in Spyder
main()
