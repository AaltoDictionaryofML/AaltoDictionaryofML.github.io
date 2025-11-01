#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Build a dependency graph from \newglossaryentry{...}{...} in a LaTeX glossary
and export an interactive vis-network HTML.

Key improvements vs. original:
- No matplotlib/pyvis (avoids NumPy 1.x wheels / ABI issues).
- Robust parsing of balanced braces for entries, name={}, description={}.
- Handles \gls, \Gls, \glspl, \Glspl references.
- Optional plain-text linking with whole-word, case-insensitive matching.
- CLI arguments; safer path handling; no chdir side effects.
"""

from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
from typing import Dict, List, Tuple

# ------------------------------ LaTeX parsing helpers ------------------------------

def find_balanced_block(s: str, start_idx: int, open_char: str = "{", close_char: str = "}") -> Tuple[str, int]:
    """Return (block_without_outer_braces, index_after_block). Assumes s[start_idx] == open_char."""
    if start_idx >= len(s) or s[start_idx] != open_char:
        raise ValueError(f"Expected '{open_char}' at position {start_idx}")
    depth, i = 0, start_idx
    while i < len(s):
        c = s[i]
        if c == open_char:
            depth += 1
        elif c == close_char:
            depth -= 1
            if depth == 0:
                return s[start_idx + 1:i], i + 1
        i += 1
    raise ValueError("Unbalanced braces.")

def iter_glossary_entries(tex: str) -> List[Tuple[str, str]]:
    """
    Yield (key, body) for \newglossaryentry{key}{ body } with fully balanced 'body'.
    Avoids brittle DOTALL regex by scanning.
    """
    pattern = re.compile(r"\\newglossaryentry\{")
    pos = 0
    out = []
    while True:
        m = pattern.search(tex, pos)
        if not m:
            break
        i = m.end()  # at '{'
        key, after_key = find_balanced_block(tex, i - 1)  # include brace
        # after_key is index after '}', expect immediately '{' for body (allow spaces/newlines)
        j = after_key
        while j < len(tex) and tex[j].isspace():
            j += 1
        if j >= len(tex) or tex[j] != "{":
            # malformed entry; skip gently
            pos = j
            continue
        body, after_body = find_balanced_block(tex, j)
        out.append((key.strip(), body))
        pos = after_body
    return out

def get_field_value_kvblock(kv_block: str, field: str) -> str | None:
    """
    Extract field={...} from a comma-separated key=value block, allowing whitespace
    and nested balanced braces. Returns string inside the braces or None.
    """
    # Find "<field>\s*="
    m = re.search(rf"{re.escape(field)}\s*=", kv_block)
    if not m:
        return None
    i = m.end()
    # Skip spaces
    while i < len(kv_block) and kv_block[i].isspace():
        i += 1
    if i >= len(kv_block) or kv_block[i] != "{":
        return None
    val, _ = find_balanced_block(kv_block, i)
    return val

def strip_latex(text: str) -> str:
    """Lightweight LaTeX cleanup for display text."""
    # Remove math: $...$, \(...\), \[...\]
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.DOTALL)
    text = re.sub(r"\$.*?\$", " ", text, flags=re.DOTALL)
    text = re.sub(r"\\\((.*?)\\\)", " ", text, flags=re.DOTALL)
    text = re.sub(r"\\\[(.*?)\\\]", " ", text, flags=re.DOTALL)
    # Remove common formatting commands \emph{...}, \textbf{...}, etc.
    text = re.sub(r"\\[a-zA-Z]+(\*?)\s*(\[[^\]]*\])?\s*\{[^{}]*\}", " ", text)
    # Remove standalone commands like \LaTeX, \alpha, \gls* (already handled separately)
    text = re.sub(r"\\[a-zA-Z]+(\*?)(\[[^\]]*\])?", " ", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_gls_refs(text: str) -> List[str]:
    """Find \gls{term}, \Gls{term}, \glspl{term}, \Glspl{term}."""
    return re.findall(r"\\(?:gls|Gls|glspl|Glspl)\{([^{}]+)\}", text)

# ------------------------------ Graph building ------------------------------

def build_graph(glossary: Dict[str, str],
                names: Dict[str, str],
                explicit_refs: Dict[str, List[str]],
                enable_plain_text_links: bool = False) -> nx.DiGraph:
    G = nx.DiGraph()
    G.add_nodes_from(glossary.keys())

    # Explicit edges from \gls references
    for term, refs in explicit_refs.items():
        for r in refs:
            if r in glossary and r != term:
                G.add_edge(term, r)

    # Optional: heuristic plain-text edges (can be noisy; off by default)
    if enable_plain_text_links:
        lowered_terms = {t: t.lower() for t in glossary.keys()}
        for term, desc in glossary.items():
            desc_low = f" {desc.lower()} "
            for other in glossary.keys():
                if other == term:
                    continue
                # Match whole-word by key or by display name
                other_key = lowered_terms[other]
                other_name = names.get(other, other).lower()
                # word boundaries for keys; for names allow spaces
                if re.search(rf"\b{re.escape(other_key)}\b", desc_low) or \
                   re.search(rf"(^|[^a-z0-9_]){re.escape(other_name)}([^a-z0-9_]|$)", desc_low):
                    G.add_edge(term, other)

    return G

def compute_communities(G: nx.DiGraph) -> Dict[str, str]:
    """Assign a color per undirected community using a generated palette."""
    if G.number_of_nodes() == 0:
        return {}
    undirected = nx.Graph()
    undirected.add_nodes_from(G.nodes())
    undirected.add_edges_from(G.to_undirected().edges())

    comms = list(greedy_modularity_communities(undirected)) if undirected.number_of_edges() > 0 else [set(G.nodes())]

    # Generate a distinct color palette (HSL to hex)
    def hsl(i, n, s=70, l=70):
        import colorsys
        h = i / max(1, n)
        r, g, b = colorsys.hls_to_rgb(h, l/100.0, s/100.0)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

    palette = [hsl(i, len(comms)) for i in range(len(comms))]
    color_map = {}
    for idx, cset in enumerate(comms):
        for node in cset:
            color_map[node] = palette[idx]
    return color_map

# ------------------------------ HTML export ------------------------------

def graph_to_vis_html(G: nx.DiGraph,
                      glossary: Dict[str, str],
                      names: Dict[str, str],
                      color_map: Dict[str, str],
                      out_html: Path) -> None:
    node_id = {n: i+1 for i, n in enumerate(G.nodes())}
    vis_nodes = []
    vis_edges = []

    for n in G.nodes():
        vis_nodes.append({
            "id": node_id[n],
            "label": names.get(n, n),
            "title": glossary.get(n, ""),
            "color": color_map.get(n, "#888888"),
            # encode degree as size for subtle emphasis
            "value": max(1, G.degree[n]),
        })
    for u, v in G.edges():
        vis_edges.append({"from": node_id[u], "to": node_id[v]})

    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>ADictML – Glossary Network</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"/>
  <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    body {{ background:#fff; }}
    #mynetwork {{ width:100%; height: 100vh; border:1px solid #eee; }}
  </style>
</head>
<body>
  <div class="container-fluid py-2">
    <h1 class="h4 text-center">The Aalto Dictionary of Machine Learning – Glossary Network</h1>
    <div id="mynetwork"></div>
  </div>
  <script>
    const nodes = new vis.DataSet({json.dumps(vis_nodes, ensure_ascii=False)});
    const edges = new vis.DataSet({json.dumps(vis_edges, ensure_ascii=False)});
    const container = document.getElementById('mynetwork');
    const data = {{ nodes, edges }};
    const options = {{
      nodes: {{
        shape: 'dot',
        scaling: {{ min: 5, max: 30 }},
        font: {{ size: 14, face: 'Inter, Arial, sans-serif' }}
      }},
      edges: {{
        arrows: 'to',
        color: '#999',
        smooth: true
      }},
      physics: {{
        enabled: true,
        solver: 'forceAtlas2Based',
        stabilization: {{ iterations: 200 }}
      }},
      interaction: {{
        hover: true,
        tooltipDelay: 120,
        navigationButtons: true,
        keyboard: true
      }}
    }};
    const network = new vis.Network(container, data, options);
  </script>
</body>
</html>"""
    out_html.write_text(html, encoding="utf-8")

# ------------------------------ Main ------------------------------

def main():
    p = argparse.ArgumentParser(description="Build interactive glossary dependency graph (HTML).")
    p.add_argument("--tex", type=Path, default=Path(__file__).parent.parent / "ADictML_Glossary_English.tex",
                   help="Path to the glossary .tex file")
    p.add_argument("--out", type=Path, default=Path("assets/glossary_network.html"),
                   help="Output HTML path")
    p.add_argument("--plain-text-links", action="store_true",
                   help="Also add heuristic edges from plain-text mentions (may be noisy)")
    args = p.parse_args()

    tex = args.tex.read_text(encoding="utf-8")

    # Remove LaTeX comments to reduce noise (but keep line structure broadly)
    tex = re.sub(r"(?m)^[ \t]*%.*$", "", tex)

    entries = iter_glossary_entries(tex)

    glossary: Dict[str, str] = {}
    names: Dict[str, str] = {}
    explicit_refs: Dict[str, List[str]] = {}

    for key, body in entries:
        # Strip trailing comments inside body
        body_nocom = re.sub(r"(?m)%.*$", "", body)
        body_nocom = re.sub(r"\s+", " ", body_nocom).strip()

        name_raw = get_field_value_kvblock(body_nocom, "name") or key
        desc_raw = get_field_value_kvblock(body_nocom, "description")
        if not desc_raw:
            # skip entries without description
            continue

        refs = extract_gls_refs(desc_raw)
        desc_clean = strip_latex(desc_raw)

        glossary[key] = desc_clean
        names[key] = strip_latex(name_raw) or key
        explicit_refs[key] = refs

    # Build graph
    G = build_graph(glossary, names, explicit_refs, enable_plain_text_links=args.plain_text_links)
    color_map = compute_communities(G)

    # Export HTML
    args.out.parent.mkdir(parents=True, exist_ok=True)
    graph_to_vis_html(G, glossary, names, color_map, args.out)

    # Optional: dump raw graph JSON next to HTML
    graph_json = {
        "nodes": [{"id": n, "name": names.get(n, n), "desc": glossary.get(n, ""), "deg": int(G.degree[n])} for n in G.nodes()],
        "edges": [{"source": u, "target": v} for u, v in G.edges()],
    }
    (args.out.with_suffix(".json")).write_text(json.dumps(graph_json, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ HTML saved to: {args.out}")
    print(f"📄 JSON saved to: {args.out.with_suffix('.json')}")
    print(f"🧠 Terms parsed: {len(glossary)} | Edges: {G.number_of_edges()}")

if __name__ == "__main__":
    main()
