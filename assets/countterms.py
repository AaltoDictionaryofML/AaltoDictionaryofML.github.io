# -*- coding: utf-8 -*-
"""
Count glossary entries by type for ADictML, and update README.md + feed.xml.

Spyder-friendly (no CLI args).

What it does
------------
1) Scans ADictML_English.tex and all reachable \\input{...} files.
2) Counts \\newglossaryentry{...}{...} by "type=..." (default type is ML).
3) Updates:
   - README.md: inserts/updates a "Dictionary at a Glance" block (idempotent)
   - feed.xml: appends counts to <channel><description> (idempotent-ish via a prefix)

Assumptions
-----------
- This script is in a subfolder (e.g. assets/)
- Repository root is one folder above this script
- Files exist in repo root:
    ADictML_English.tex
    README.md
    feed.xml
"""

import re
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone, timedelta
import xml.etree.ElementTree as ET

# ---------------- Configuration ----------------

MAIN_TEX_NAME = "ADictML_English.tex"
DEFAULT_TYPE = "ML"

README_NAME = "README.md"
FEED_NAME = "feed.xml"

# README insertion markers (idempotent update)
README_STATS_BEGIN = "<!-- ADICTML_STATS_BEGIN -->"
README_STATS_END   = "<!-- ADICTML_STATS_END -->"

# For feed.xml description update
FEED_STATS_PREFIX = "Current coverage:"

# If you want to rename types in the README/RSS (optional)
TYPE_LABEL_OVERRIDES = {
    "ML": "Core ML",
    # Example:
    # "MathTools": "Math & Optimization",
    # "Regulation": "Regulation & Governance",
}

# -----------------------------------------------

INPUT_RE = re.compile(r'\\input\{([^}]+)\}')
NEW_ENTRY_RE = re.compile(r'\\newglossaryentry\s*\{[^}]+\}\s*\{', re.MULTILINE)
TYPE_RE = re.compile(r'type\s*=\s*([a-zA-Z]+)')

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
    """
    Yields the *body* of the second argument of \\newglossaryentry{key}{BODY}.
    """
    for m in NEW_ENTRY_RE.finditer(text):
        brace_start = m.end() - 1  # points to '{' starting BODY
        brace_end = find_matching_brace(text, brace_start)
        yield text[brace_start + 1 : brace_end]

def collect_tex_files(main_file: Path):
    """
    Collect reachable .tex files via \\input{...} recursion.
    """
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

def format_rfc822_helsinki(dt: datetime) -> str:
    """
    Format as RFC 822 / RSS pubDate style with +0200 offset (EET).
    """
    # Finland in December is typically EET (+0200).
    helsinki = timezone(timedelta(hours=2))
    dt = dt.astimezone(helsinki)
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z")

def label_for_type(t: str) -> str:
    return TYPE_LABEL_OVERRIDES.get(t, t)

def build_stats(counts: Counter, total: int):
    """
    Returns:
      - lines for README bullet list
      - a compact one-line stats string for RSS description
    """
    # Sort by count desc, then name asc (stable and informative)
    items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))

    # README bullet lines
    readme_lines = [f"- **Total terms:** {total}"]
    for t, c in items:
        readme_lines.append(f"- **{label_for_type(t)}:** {c}")

    # RSS one-liner
    parts = [f"{label_for_type(t)} {c}" for t, c in items]
    rss_line = f"{FEED_STATS_PREFIX} {total} terms (" + " · ".join(parts) + ")."

    return readme_lines, rss_line

def update_readme(readme_path: Path, readme_lines, last_updated_str: str) -> bool:
    """
    Insert or replace the stats block in README.md using markers.
    Returns True if file changed.
    """
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
        # Insert right after the first horizontal rule '---' if possible,
        # otherwise append at top after the title.
        if "\n---\n" in original:
            updated = original.replace("\n---\n", "\n---\n\n" + block, 1)
        else:
            # Fallback: after the first line (title) and possible blank line
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
    """
    Updates <channel><description> to include stats.
    Returns True if file changed.
    """
    if not feed_path.exists():
        print(f"[WARN] feed.xml not found: {feed_path}")
        return False

    original = read_text(feed_path)

    # Parse XML (preserve main structure)
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

    # Remove any previous stats line we added
    # Strategy: if FEED_STATS_PREFIX appears, strip from there to end (simple, robust).
    if FEED_STATS_PREFIX in base_desc:
        base_desc = base_desc.split(FEED_STATS_PREFIX, 1)[0].strip()
        # Remove trailing punctuation/space artifacts
        base_desc = base_desc.rstrip(" .")

    new_desc = base_desc
    if new_desc:
        new_desc = new_desc.rstrip()
        new_desc += " "
    new_desc += rss_stats_line

    if new_desc != (desc.text or "").strip():
        desc.text = new_desc

        # Optionally update lastBuildDate as well (uncomment if desired)
        # lbd = channel.find("lastBuildDate")
        # if lbd is not None:
        #     lbd.text = format_rfc822_helsinki(datetime.now())

        # Write back. ElementTree doesn't preserve original formatting perfectly,
        # but keeps valid RSS. If you care about exact whitespace, we can switch
        # to a minimal regex update instead.
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

    # Console output (kept from your original script)
    print("\nGlossary entry counts by type")
    print("--------------------------------")
    for k in sorted(counts):
        print(f"{k:15s}: {counts[k]:4d}")
    print("--------------------------------")
    print(f"{'TOTAL':15s}: {total:4d}")
    print(f"\nScanned {len(tex_files)} TeX files.")

    # Build text for README + RSS
    now = datetime.now()
    last_updated_str = now.strftime("%Y-%m-%d")
    readme_lines, rss_stats_line = build_stats(counts, total)

    changed_readme = update_readme(readme_path, readme_lines, last_updated_str)
    changed_feed = update_feed(feed_path, rss_stats_line)

    if changed_readme:
        print(f"[OK] Updated {readme_path.name}")
    else:
        print(f"[OK] {readme_path.name} unchanged")

    if changed_feed:
        print(f"[OK] Updated {feed_path.name}")
    else:
        print(f"[OK] {feed_path.name} unchanged")

# Run automatically in Spyder
main()