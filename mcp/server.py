"""
Aalto Dictionary of Machine Learning — MCP Server
Parses all .tex glossary files from the ADictML repo and exposes
them via five MCP tools: list_all_terms, lookup_term, search_terms,
get_related_terms, get_style_guide.

Location: AaltoDictionaryofML.github.io/mcp/server.py

Usage:
    pip install -r requirements.txt
    python server.py

Register with Claude Code:
    claude mcp add --scope user aalto-dictionary \\
      -- python ~/AaltoDictionaryofML.github.io/mcp/server.py
"""

import os
import re
import asyncio
from pathlib import Path
from difflib import SequenceMatcher

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

# ── Config ────────────────────────────────────────────────────────────────────
# Repo root is one level above this file (mcp/server.py → repo root)
REPO_DIR = Path(os.environ.get(
    "ADDICTML_REPO",
    Path(__file__).parent.parent
))

# All glossary files with their category labels
GLOSSARY_FILES = {
    "ML Concepts":           "ADictML_CoreML.tex",
    "Math":                  "ADictML_Math.tex",
    "ML Systems":            "ADictML_MLSystems.tex",
    "Reinforcement Learning":"ADictML_RL.tex",
    "Regulation":            "ADictML_Regulation.tex",
}

# Style guide source (CLAUDE.md in the dictionary working repo)
STYLE_GUIDE_PATH = Path(os.environ.get(
    "ADDICTML_STYLE_GUIDE",
    Path.home() / "dictionaryappliedml" / "CLAUDE.md"
))
# ─────────────────────────────────────────────────────────────────────────────


def parse_style_guide(path: Path) -> dict[str, str]:
    """
    Parse CLAUDE.md into a topic-indexed dictionary.

    Splits on '### ' headings within the '## AMS style rules' section.
    Each topic key is the heading text (lowercased, stripped of parentheticals),
    and the value is the full markdown content under that heading.
    """
    if not path.exists():
        print(f"[WARN] Style guide not found: {path}")
        return {}

    text = path.read_text(encoding="utf-8")
    topics: dict[str, str] = {}

    # Find the AMS style rules section
    ams_start = text.find("## AMS style rules")
    if ams_start < 0:
        print("[WARN] No '## AMS style rules' section found in CLAUDE.md")
        return {}

    # Find the next ## section (end of AMS rules)
    next_section = text.find("\n## ", ams_start + 1)
    ams_text = text[ams_start:next_section] if next_section > 0 else text[ams_start:]

    # Split by ### headings
    heading_re = re.compile(r"^### (.+)$", re.MULTILINE)
    matches = list(heading_re.finditer(ams_text))

    for i, m in enumerate(matches):
        raw_title = m.group(1).strip()
        # Normalize: lowercase, strip parentheticals like "(Springer requirement)"
        key = re.sub(r"\s*\([^)]*\)\s*", "", raw_title).strip().lower()
        # Content runs from end of this heading to start of next (or end of section)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(ams_text)
        content = ams_text[start:end].strip()
        topics[key] = f"### {raw_title}\n\n{content}"

    return topics


def strip_latex(text: str) -> str:
    """Remove common LaTeX commands for cleaner plain-text output."""
    text = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", text)  # \cmd{arg} → arg
    text = re.sub(r"\\[a-zA-Z]+\b", "", text)               # lone \cmd
    text = re.sub(r"[{}]", "", text)                         # stray braces
    text = re.sub(r"\$([^$]*)\$", r"\1", text)              # inline math
    return " ".join(text.split())                            # normalise whitespace


def parse_glossary(repo_dir: Path) -> dict[str, dict]:
    """
    Parse \\newglossaryentry blocks from all ADictML .tex files.

    Handles multi-line descriptions with nested braces, e.g.:
        \\newglossaryentry{key}{
            name={Term Name},
            description={Definition text with $math$ and \\emph{emphasis}},
            see={related1, related2}
        }
    """
    entries: dict[str, dict] = {}
    entry_start = re.compile(r"\\newglossaryentry\{([^}]+)\}\s*\{")

    for category, filename in GLOSSARY_FILES.items():
        path = repo_dir / filename
        if not path.exists():
            print(f"[WARN] Not found: {path}")
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        pos = 0

        while True:
            m = entry_start.search(text, pos)
            if not m:
                break

            key = m.group(1).strip()

            # Walk forward collecting the full brace-balanced body
            depth = 1
            i = m.end()
            while i < len(text) and depth > 0:
                if text[i] == "{":
                    depth += 1
                elif text[i] == "}":
                    depth -= 1
                i += 1
            body = text[m.end(): i - 1]
            pos = i

            # Extract named fields (one level of nested braces)
            fields: dict[str, str] = {}
            field_re = re.compile(
                r"(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", re.DOTALL
            )
            for fm in field_re.finditer(body):
                fields[fm.group(1)] = fm.group(2).strip()

            name = strip_latex(fields.get("name", key))
            description = strip_latex(
                fields.get("description", fields.get("text", ""))
            )
            related_raw = fields.get("see", fields.get("seealso", ""))
            related = [r.strip() for r in related_raw.split(",") if r.strip()]

            entries[key] = {
                "key":         key,
                "name":        name,
                "description": description,
                "related":     related,
                "category":    category,
            }

    return entries


# ── Load entries and style guide at startup ──────────────────────────────────
print(f"[INFO] Loading ADictML from {REPO_DIR} ...")
ENTRIES = parse_glossary(REPO_DIR)
print(f"[INFO] Loaded {len(ENTRIES)} terms across {len(GLOSSARY_FILES)} categories.")

print(f"[INFO] Loading style guide from {STYLE_GUIDE_PATH} ...")
STYLE_GUIDE = parse_style_guide(STYLE_GUIDE_PATH)
print(f"[INFO] Loaded {len(STYLE_GUIDE)} style topics.")


# ── Helpers ───────────────────────────────────────────────────────────────────
def fuzzy_score(query: str, text: str) -> float:
    return SequenceMatcher(None, query.lower(), text.lower()).ratio()


def resolve(term: str) -> dict | None:
    """Resolve a term by exact key first, then case-insensitive name match."""
    if term in ENTRIES:
        return ENTRIES[term]
    tl = term.lower()
    for e in ENTRIES.values():
        if e["name"].lower() == tl:
            return e
    return None


def fmt_entry(e: dict, snippet_len: int = 150) -> str:
    desc = e["description"]
    if len(desc) > snippet_len:
        desc = desc[:snippet_len] + "..."
    return f"- **{e['name']}** (`{e['key']}`, {e['category']}): {desc}"


# ── MCP Server ────────────────────────────────────────────────────────────────
server = Server("aalto-dictionary")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_all_terms",
            description=(
                "List all terms in the Aalto Dictionary of Machine Learning, "
                "grouped by category. Optionally filter by category: "
                "'ML Concepts', 'Math', 'ML Systems', 'Reinforcement Learning', 'Regulation'."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Optional category filter (leave empty for all)",
                    }
                },
                "required": [],
            },
        ),
        types.Tool(
            name="lookup_term",
            description=(
                "Get the full definition of a term by its glossary key or display name. "
                "Returns name, category, description, and cross-references."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "term": {
                        "type": "string",
                        "description": "Glossary key (e.g. 'fed_learning') or display name",
                    }
                },
                "required": ["term"],
            },
        ),
        types.Tool(
            name="search_terms",
            description=(
                "Fuzzy/keyword search across term names and descriptions. "
                "Returns the top matching terms with short snippets."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query, e.g. 'Byzantine robustness'",
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default 5)",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="get_related_terms",
            description=(
                "Get terms cross-referenced from a given term via its 'see' field. "
                "Useful for exploring concept neighbourhoods."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "term": {
                        "type": "string",
                        "description": "Glossary key or display name",
                    }
                },
                "required": ["term"],
            },
        ),
        types.Tool(
            name="get_style_guide",
            description=(
                "Look up AMS style guide rules for a given notation or editorial topic. "
                "Topics include: 'impersonal voice', 'american english spelling', "
                "'precise use of model', 'consistent terminology', 'precise mathematical english', "
                "'article before abbreviations', 'math mode', 'integration variable', "
                "'punctuation in equations', 'vectors and matrices', 'subscripts vs superscripts', "
                "'transpose', 'cross-references', 'see also block', 'figures', "
                "'theorem environments', 'application examples'. "
                "Pass an empty topic to list all available topics."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": (
                            "Style topic to look up, e.g. 'subscripts' or 'impersonal voice'. "
                            "Fuzzy matching is supported. Leave empty to list all topics."
                        ),
                    }
                },
                "required": [],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:

    # ── list_all_terms ────────────────────────────────────────────────────────
    if name == "list_all_terms":
        category = arguments.get("category", "").strip()
        filtered = {
            k: e for k, e in ENTRIES.items()
            if not category or e["category"].lower() == category.lower()
        }
        if not filtered:
            available = ", ".join(GLOSSARY_FILES.keys())
            msg = (
                f"No terms found for category '{category}'. "
                f"Available categories: {available}"
            ) if category else "No terms loaded. Check that REPO_DIR points to the repo."
            return [types.TextContent(type="text", text=msg)]

        by_cat: dict[str, list] = {}
        for e in filtered.values():
            by_cat.setdefault(e["category"], []).append(e)

        lines: list[str] = [f"**{len(filtered)} terms**\n"]
        for cat in GLOSSARY_FILES:           # preserve canonical order
            terms = by_cat.get(cat, [])
            if not terms:
                continue
            lines.append(f"### {cat} ({len(terms)})")
            for e in sorted(terms, key=lambda x: x["name"].lower()):
                lines.append(f"- **{e['name']}** (`{e['key']}`)")
            lines.append("")
        return [types.TextContent(type="text", text="\n".join(lines))]

    # ── lookup_term ───────────────────────────────────────────────────────────
    elif name == "lookup_term":
        term = arguments.get("term", "").strip()
        entry = resolve(term)
        if not entry:
            return [types.TextContent(type="text", text=f"Term '{term}' not found.")]
        related_str = ", ".join(f"`{r}`" for r in entry["related"]) or "none"
        text = (
            f"**{entry['name']}** (`{entry['key']}`)\n"
            f"*Category:* {entry['category']}\n\n"
            f"{entry['description']}\n\n"
            f"*See also:* {related_str}"
        )
        return [types.TextContent(type="text", text=text)]

    # ── search_terms ──────────────────────────────────────────────────────────
    elif name == "search_terms":
        query = arguments.get("query", "").strip()
        top_k = max(1, int(arguments.get("top_k", 5)))

        scored: list[tuple[float, dict]] = []
        for entry in ENTRIES.values():
            score = max(
                fuzzy_score(query, entry["name"]),
                fuzzy_score(query, entry["description"]),
            )
            # Boost exact substring matches
            if query.lower() in entry["name"].lower() or \
               query.lower() in entry["description"].lower():
                score = max(score, 0.85)
            scored.append((score, entry))

        scored.sort(key=lambda x: x[0], reverse=True)
        top = [e for s, e in scored[:top_k] if s > 0.2]

        if not top:
            return [types.TextContent(type="text", text=f"No results for '{query}'.")]

        lines = [f"**Top {len(top)} results for '{query}':**\n"]
        lines += [fmt_entry(e) for e in top]
        return [types.TextContent(type="text", text="\n".join(lines))]

    # ── get_related_terms ─────────────────────────────────────────────────────
    elif name == "get_related_terms":
        term = arguments.get("term", "").strip()
        entry = resolve(term)
        if not entry:
            return [types.TextContent(type="text", text=f"Term '{term}' not found.")]
        if not entry["related"]:
            return [types.TextContent(type="text",
                text=f"No related terms listed for '{entry['name']}'.")]

        lines = [f"**Terms related to '{entry['name']}':**\n"]
        for rel_key in entry["related"]:
            rel = resolve(rel_key)
            if rel:
                lines.append(fmt_entry(rel))
            else:
                lines.append(f"- `{rel_key}` (key not found in dictionary)")
        return [types.TextContent(type="text", text="\n".join(lines))]

    # ── get_style_guide ──────────────────────────────────────────────────────
    elif name == "get_style_guide":
        topic = arguments.get("topic", "").strip().lower()

        if not STYLE_GUIDE:
            return [types.TextContent(type="text",
                text="Style guide not loaded. Check ADDICTML_STYLE_GUIDE path.")]

        # No topic → list all available topics
        if not topic:
            lines = [f"**{len(STYLE_GUIDE)} style topics available:**\n"]
            for key in sorted(STYLE_GUIDE.keys()):
                # Show first line of content as preview
                preview = STYLE_GUIDE[key].split("\n\n", 1)[-1][:80] + "..."
                lines.append(f"- **{key}**: {preview}")
            return [types.TextContent(type="text", text="\n".join(lines))]

        # Exact match first
        if topic in STYLE_GUIDE:
            return [types.TextContent(type="text", text=STYLE_GUIDE[topic])]

        # Fuzzy match: find best topic by substring then similarity
        best_key, best_score = None, 0.0
        for key in STYLE_GUIDE:
            # Substring boost
            if topic in key or key in topic:
                score = 0.9
            else:
                score = fuzzy_score(topic, key)
            if score > best_score:
                best_score = score
                best_key = key

        if best_key and best_score > 0.3:
            header = f"*(Matched topic: '{best_key}')*\n\n"
            return [types.TextContent(type="text",
                text=header + STYLE_GUIDE[best_key])]

        available = ", ".join(sorted(STYLE_GUIDE.keys()))
        return [types.TextContent(type="text",
            text=f"No style topic matching '{topic}'. Available: {available}")]

    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


# ── Entrypoint ────────────────────────────────────────────────────────────────
async def main():
    async with mcp.server.stdio.stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
