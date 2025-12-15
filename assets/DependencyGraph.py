#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Build a dependency graph from \\newglossaryentry{...}{...} across multiple ADictML_*.tex files
and export an interactive vis-network HTML with an *auto-roaming camera tour*.

Update (per request):
- The default tour visits the **10 terms with the largest IN-DEGREE**
  (i.e., terms referenced by many other terms).
- If you pass --tour, that curated tour is used instead.

Usage:
  python assets/build_glossary_graph.py
  python assets/build_glossary_graph.py --tour lossfunction,gradientdescent,regularization
  python assets/build_glossary_graph.py --tour-k 12
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities


# ===========================================================
# LaTeX comment handling
# ===========================================================

def strip_comments_preserve_escaped_percent(text: str) -> str:
    """Remove LaTeX comments (%) but preserve escaped \\%."""
    out_lines: List[str] = []
    for line in text.splitlines():
        buf: List[str] = []
        i = 0
        while i < len(line):
            ch = line[i]
            if ch == '%':
                if i > 0 and line[i - 1] == '\\':
                    buf.append('%')
                    i += 1
                else:
                    break
            else:
                buf.append(ch)
                i += 1
        out_lines.append(''.join(buf))
    return '\n'.join(out_lines)


# ===========================================================
# Balanced-brace parsing utilities
# ===========================================================

def find_balanced_block(
    s: str,
    start_idx: int,
    open_char: str = "{",
    close_char: str = "}"
) -> Tuple[str, int]:
    """Return (block_without_outer_braces, index_after_block). Assumes s[start_idx] == open_char."""
    if start_idx >= len(s) or s[start_idx] != open_char:
        raise ValueError(f"Expected '{open_char}' at position {start_idx}")

    depth = 0
    i = start_idx
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
    """Return list of (key, body) for \\newglossaryentry{key}{ body } with balanced 'body'."""
    pattern = re.compile(r"\\newglossaryentry\{")
    pos = 0
    out: List[Tuple[str, str]] = []

    while True:
        m = pattern.search(tex, pos)
        if not m:
            break

        try:
            key, after_key = find_balanced_block(tex, m.end() - 1)
        except ValueError:
            pos = m.end()
            continue

        j = after_key
        while j < len(tex) and tex[j].isspace():
            j += 1

        if j >= len(tex) or tex[j] != "{":
            pos = j
            continue

        try:
            body, after_body = find_balanced_block(tex, j)
        except ValueError:
            pos = j + 1
            continue

        out.append((key.strip(), body))
        pos = after_body

    return out


def get_field_value_kvblock(kv_block: str, field: str) -> str | None:
    """Extract field={...} from a key=value block, allowing nested braces."""
    m = re.search(rf"{re.escape(field)}\s*=", kv_block)
    if not m:
        return None
    i = m.end()
    while i < len(kv_block) and kv_block[i].isspace():
        i += 1
    if i >= len(kv_block) or kv_block[i] != "{":
        return None
    try:
        val, _ = find_balanced_block(kv_block, i)
    except ValueError:
        return None
    return val


# ===========================================================
# Lightweight LaTeX cleanup
# ===========================================================

def strip_latex(text: str) -> str:
    """Lightweight LaTeX cleanup for display text (labels/tooltips)."""
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.DOTALL)
    text = re.sub(r"\$.*?\$", " ", text, flags=re.DOTALL)
    text = re.sub(r"\\\((.*?)\\\)", " ", text, flags=re.DOTALL)
    text = re.sub(r"\\\[(.*?)\\\]", " ", text, flags=re.DOTALL)
    text = re.sub(r"\\[a-zA-Z]+(\*?)\s*(\[[^\]]*\])?\s*\{[^{}]*\}", " ", text)
    text = re.sub(r"\\[a-zA-Z]+(\*?)(\[[^\]]*\])?", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_gls_refs(text: str) -> List[str]:
    """Find \\gls{term}, \\Gls{term}, \\glspl{term}, \\Glspl{term}."""
    return re.findall(r"\\(?:gls|Gls|glspl|Glspl)\{([^{}]+)\}", text)


# ===========================================================
# Source discovery: ADictML_*.tex (one folder above script)
# ===========================================================

def collect_adictml_tex_files(project_root: Path, recursive: bool = False) -> List[Path]:
    """Collect ADictML_*.tex files from project root (optionally recursive)."""
    candidates = sorted(project_root.rglob("ADictML_*.tex") if recursive else project_root.glob("ADictML_*.tex"))
    return [p.resolve() for p in candidates if p.exists() and p.is_file()]


def load_combined_tex(paths: List[Path]) -> str:
    """Concatenate multiple .tex files into one string (with file boundary markers)."""
    chunks: List[str] = []
    for p in paths:
        chunks.append(f"% --- BEGIN FILE: {p.as_posix()} ---\n")
        chunks.append(p.read_text(encoding="utf-8", errors="replace"))
        chunks.append(f"\n% --- END FILE: {p.as_posix()} ---\n")
    return "\n".join(chunks)


# ===========================================================
# Graph building
# ===========================================================

def build_graph(
    glossary: Dict[str, str],
    names: Dict[str, str],
    explicit_refs: Dict[str, List[str]],
    enable_plain_text_links: bool = False
) -> nx.DiGraph:
    """Build a directed graph term -> referenced_term."""
    G = nx.DiGraph()
    G.add_nodes_from(glossary.keys())

    # Explicit edges from \gls references
    for term, refs in explicit_refs.items():
        for r in refs:
            if r in glossary and r != term:
                G.add_edge(term, r)

    # Optional heuristic edges from plain text (off by default)
    if enable_plain_text_links:
        lowered_keys = {t: t.lower() for t in glossary.keys()}
        for term, desc in glossary.items():
            desc_low = f" {desc.lower()} "
            for other in glossary.keys():
                if other == term:
                    continue
                other_key = lowered_keys[other]
                other_name = (names.get(other, other) or other).lower()
                hit_key = re.search(rf"\b{re.escape(other_key)}\b", desc_low) is not None
                hit_name = re.search(rf"(^|[^a-z0-9_]){re.escape(other_name)}([^a-z0-9_]|$)", desc_low) is not None
                if hit_key or hit_name:
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

    def hsl_to_hex(i: int, n: int, s: int = 70, l: int = 70) -> str:
        import colorsys
        h = i / max(1, n)
        r, g, b = colorsys.hls_to_rgb(h, l / 100.0, s / 100.0)
        return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

    palette = [hsl_to_hex(i, len(comms)) for i in range(len(comms))]
    color_map: Dict[str, str] = {}
    for idx, cset in enumerate(comms):
        for node in cset:
            color_map[node] = palette[idx]
    return color_map


# ===========================================================
# HTML export with "roaming camera" (integrated)
# ===========================================================

def graph_to_vis_html(
    G: nx.DiGraph,
    glossary: Dict[str, str],
    names: Dict[str, str],
    color_map: Dict[str, str],
    out_html: Path,
    *,
    roam_enabled: bool = True,
    roam_tour: List[str] | None = None,
    roam_tour_k: int = 10,
    roam_freeze_interaction: bool = True,
    stabilization_iterations: int = 1800,
) -> None:
    """
    Export HTML and integrate an automatic “roaming camera tour”.

    Default tour behavior (requested):
    - If roam_tour is not provided: visit the top-K nodes by **in-degree**.

    roam_tour:
      - If provided: uses this exact list of term keys (ignores missing keys).
      - If empty/None: auto-picks by in-degree (top K).
    """
    # --- Build vis-network node/edge lists (node id = term key) ---
    vis_nodes: List[dict] = []
    vis_edges: List[dict] = []

    # Precompute in-degrees for sizing/tour ranking
    in_deg = {n: int(G.in_degree[n]) for n in G.nodes()}
    tot_deg = {n: int(G.degree[n]) for n in G.nodes()}

    for n in G.nodes():
        vis_nodes.append({
            "id": n,  # string ID == term key
            "label": names.get(n, n),
            "title": glossary.get(n, ""),
            "color": color_map.get(n, "#888888"),
            # Keep node size as total degree (visual density),
            # but we also pass inDeg for ranking and possible UI usage.
            "value": max(1, tot_deg.get(n, 0)),
            "inDeg": in_deg.get(n, 0),
        })

    for u, v in G.edges():
        vis_edges.append({"from": u, "to": v})

    roam_tour = roam_tour or []
    tour_js = json.dumps(roam_tour, ensure_ascii=False)
    roam_enabled_js = "true" if roam_enabled else "false"
    freeze_interaction_js = "true" if roam_freeze_interaction else "false"

    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>ADictML – Glossary Network</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"/>
  <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    body {{ background:#fff; margin:0; }}
    #mynetwork {{ width:100%; height: 100vh; border:1px solid #eee; }}
    #overlay {{
      position: fixed;
      top: 10px;
      left: 10px;
      z-index: 10;
      background: rgba(255,255,255,0.88);
      border: 1px solid #eee;
      border-radius: 10px;
      padding: 8px 10px;
      font: 12px/1.3 Inter, Arial, sans-serif;
      color: #222;
      max-width: 45vw;
    }}
    #overlay .small {{ color:#666; }}
    #progress {{
      width: 240px;
      height: 6px;
      background: #eee;
      border-radius: 6px;
      overflow: hidden;
      margin-top: 6px;
    }}
    #bar {{
      height: 100%;
      width: 0%;
      background: #999;
    }}
  </style>
</head>
<body>
  <div id="overlay">
    <div><strong>ADictML Term Network</strong></div>
    <div class="small" id="status">Stabilizing layout…</div>
    <div id="progress"><div id="bar"></div></div>
  </div>
  <div id="mynetwork"></div>

  <script>
    // ---------------------------
    // Data
    // ---------------------------
    const nodes = new vis.DataSet({json.dumps(vis_nodes, ensure_ascii=False)});
    const edges = new vis.DataSet({json.dumps(vis_edges, ensure_ascii=False)});
    const container = document.getElementById('mynetwork');
    const data = {{ nodes, edges }};

    // ---------------------------
    // Options
    // ---------------------------
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
        stabilization: {{
          enabled: true,
          iterations: {stabilization_iterations},
          updateInterval: 25,
          fit: true
        }}
      }},
      interaction: {{
        hover: true,
        tooltipDelay: 120,
        navigationButtons: true,
        keyboard: true
      }}
    }};

    const network = new vis.Network(container, data, options);

    // ---------------------------
    // Overlay helpers
    // ---------------------------
    const statusEl = document.getElementById("status");
    const barEl = document.getElementById("bar");
    function setStatus(msg) {{ statusEl.textContent = msg; }}
    function setProgress(frac) {{ barEl.style.width = Math.max(0, Math.min(1, frac)) * 100 + "%"; }}

    // ---------------------------
    // Roaming camera utilities
    // ---------------------------
    const ROAM_ENABLED = {roam_enabled_js};
    const CURATED_TOUR = {tour_js};        // term keys, may be empty
    const AUTO_TOUR_K = {int(roam_tour_k)};
    const FREEZE_INTERACTION = {freeze_interaction_js};

    function sleep(ms) {{
      return new Promise(resolve => setTimeout(resolve, ms));
    }}

    function filterExisting(ids) {{
      const existing = new Set(nodes.getIds());
      return ids.filter(x => existing.has(x));
    }}

    // Default tour: top-K by in-degree (many terms refer to it)
    function pickTourNodesByInDegree(k) {{
      const all = nodes.get(); // contains fields like {{id,label,value,inDeg}}
      all.sort((a,b) => (b.inDeg || 0) - (a.inDeg || 0));

      // Take top-k, but try to reduce near-duplicates by sampling every other from top 2k
      const top = all.slice(0, Math.min(all.length, k * 2));
      const pick = [];
      for (let i=0; i<top.length && pick.length<k; i+=2) pick.push(top[i].id);
      if (pick.length < k) {{
        for (let i=1; i<top.length && pick.length<k; i+=2) pick.push(top[i].id);
      }}
      return pick;
    }}

    async function focusNode(nodeId, scale, ms) {{
      const pos = network.getPositions([nodeId])[nodeId];
      if (!pos) return;
      network.selectNodes([nodeId]);
      network.focus(nodeId, {{
        scale: scale,
        animation: {{ duration: ms, easingFunction: "easeInOutQuad" }}
      }});
      await sleep(ms + 140);
    }}

    async function microRoam(nodeId, baseScale) {{
      const pos = network.getPositions([nodeId])[nodeId];
      if (!pos) return;

      const jitter = [
        {{ dx:  40, dy: -20, s: baseScale * 1.05 }},
        {{ dx: -30, dy:  25, s: baseScale * 0.98 }},
        {{ dx:  20, dy:  30, s: baseScale * 1.03 }},
      ];

      for (const j of jitter) {{
        network.moveTo({{
          position: {{ x: pos.x + j.dx, y: pos.y + j.dy }},
          scale: j.s,
          animation: {{ duration: 900, easingFunction: "easeInOutQuad" }}
        }});
        await sleep(980);
      }}
    }}

    async function roamTour() {{
      setStatus("Roaming… (auto camera)");
      setProgress(1.0);

      // Start with a wide view
      network.unselectAll();
      network.fit({{
        animation: {{ duration: 900, easingFunction: "easeInOutQuad" }}
      }});
      await sleep(1050);

      let tour = [];
      if (CURATED_TOUR && CURATED_TOUR.length > 0) {{
        tour = filterExisting(CURATED_TOUR);
      }} else {{
        tour = pickTourNodesByInDegree(AUTO_TOUR_K);
      }}

      if (tour.length === 0) {{
        setStatus("No tour nodes found.");
        return;
      }}

      // Pleasant zoom schedule (varies shots)
      const scales = [2.4, 1.9, 2.8, 1.7, 2.2, 3.0, 1.8, 2.5, 2.0, 2.7];

      for (let i = 0; i < tour.length; i++) {{
        const nodeId = tour[i];
        const sc = scales[i % scales.length];

        await focusNode(nodeId, sc, 1200);
        await microRoam(nodeId, sc);

        // Every 3 nodes, zoom out to re-contextualize
        if ((i + 1) % 3 === 0) {{
          network.unselectAll();
          network.fit({{
            animation: {{ duration: 900, easingFunction: "easeInOutQuad" }}
          }});
          await sleep(1050);
        }}
      }}

      // End on a wide shot
      network.unselectAll();
      network.fit({{
        animation: {{ duration: 1200, easingFunction: "easeInOutQuad" }}
      }});
      setStatus("Done. (Layout frozen)");
    }}

    // ---------------------------
    // Stabilization callbacks
    // ---------------------------
    network.on("stabilizationProgress", function (params) {{
      const frac = params.iterations / Math.max(1, params.total);
      setProgress(frac);
      setStatus(`Stabilizing layout… ${{Math.round(frac * 100)}}%`);
    }});

    network.once("stabilizationIterationsDone", async function () {{
      setStatus("Stabilized. Freezing layout…");
      setProgress(1.0);

      // Freeze node positions (no more motion)
      network.setOptions({{ physics: {{ enabled: false }} }});

      // Optional: prevent accidental dragging/zoom during recording
      if (FREEZE_INTERACTION) {{
        network.setOptions({{
          interaction: {{
            dragNodes: false,
            dragView: false,
            zoomView: false,
            navigationButtons: false,
            keyboard: false
          }}
        }});
      }}

      await sleep(250);

      if (ROAM_ENABLED) {{
        roamTour();
      }} else {{
        setStatus("Stabilized. (Roam disabled)");
      }}
    }});
  </script>
</body>
</html>"""

    out_html.write_text(html, encoding="utf-8")


# ===========================================================
# Main
# ===========================================================

def main() -> None:
    SCRIPT_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = SCRIPT_DIR.parent  # one folder above this script

    p = argparse.ArgumentParser(description="Build ADictML glossary dependency graph (HTML + JSON), with roaming camera.")
    p.add_argument("--out", type=Path, default=SCRIPT_DIR / "glossary_network.html",
                   help="Output HTML path (defaults next to this script).")
    p.add_argument("--plain-text-links", action="store_true",
                   help="Also add heuristic edges from plain-text mentions (may be noisy).")
    p.add_argument("--recursive-root-scan", action="store_true",
                   help="Also include ADictML_*.tex from subdirectories under the project root.")
    p.add_argument("--last-wins", action="store_true",
                   help="If a glossary key is defined multiple times, keep the last definition.")
    # Roaming controls
    p.add_argument("--no-roam", action="store_true",
                   help="Disable camera roaming; only show the interactive network.")
    p.add_argument("--tour", type=str, default="",
                   help="Comma-separated list of term keys to visit (curated tour). Example: lossfunction,gradientdescent")
    p.add_argument("--tour-k", type=int, default=10,
                   help="If no --tour is provided, visit top-k nodes by IN-DEGREE (default 10).")
    p.add_argument("--stabilize-iters", type=int, default=1800,
                   help="Physics stabilization iterations (default 1800). Increase for longer ‘physics’ evolution.")
    p.add_argument("--no-freeze-interaction", action="store_true",
                   help="Do NOT disable interaction after freezing (useful if you want to roam manually).")
    args = p.parse_args()

    sources = collect_adictml_tex_files(PROJECT_ROOT, recursive=args.recursive_root_scan)
    if not sources:
        raise SystemExit(f"No ADictML_*.tex files found under: {PROJECT_ROOT}")

    combined_tex = strip_comments_preserve_escaped_percent(load_combined_tex(sources))
    entries = iter_glossary_entries(combined_tex)

    glossary: Dict[str, str] = {}
    names: Dict[str, str] = {}
    explicit_refs: Dict[str, List[str]] = {}

    for key, body in entries:
        body_nocom = strip_comments_preserve_escaped_percent(body)
        body_nocom = re.sub(r"\s+", " ", body_nocom).strip()

        desc_raw = get_field_value_kvblock(body_nocom, "description")
        if not desc_raw:
            continue

        name_raw = get_field_value_kvblock(body_nocom, "name") or key
        refs = extract_gls_refs(desc_raw)

        if (key in glossary) and (not args.last_wins):
            continue

        glossary[key] = strip_latex(desc_raw)
        names[key] = strip_latex(name_raw) or key
        explicit_refs[key] = refs

    G = build_graph(glossary, names, explicit_refs, enable_plain_text_links=args.plain_text_links)
    color_map = compute_communities(G)

    # Parse curated tour list
    tour_list: List[str] = []
    if args.tour.strip():
        tour_list = [t.strip() for t in args.tour.split(",") if t.strip()]

    # Export HTML (with integrated roam tour)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    graph_to_vis_html(
        G,
        glossary,
        names,
        color_map,
        args.out,
        roam_enabled=(not args.no_roam),
        roam_tour=tour_list,
        roam_tour_k=max(1, args.tour_k),
        roam_freeze_interaction=(not args.no_freeze_interaction),
        stabilization_iterations=max(50, args.stabilize_iters),
    )

    # JSON export (useful for other tooling)
    graph_json = {
        "project_root": PROJECT_ROOT.as_posix(),
        "sources_scanned": [p.as_posix() for p in sources],
        "settings": {
            "recursive_root_scan": bool(args.recursive_root_scan),
            "plain_text_links": bool(args.plain_text_links),
            "duplicate_policy": "last-wins" if args.last_wins else "first-wins",
            "roam_enabled": bool(not args.no_roam),
            "tour": tour_list,
            "tour_k": int(max(1, args.tour_k)),
            "stabilize_iters": int(max(50, args.stabilize_iters)),
        },
        "nodes": [
            {
                "id": n,
                "name": names.get(n, n),
                "desc": glossary.get(n, ""),
                "deg": int(G.degree[n]),
                "in_deg": int(G.in_degree[n]),
                "out_deg": int(G.out_degree[n]),
            }
            for n in G.nodes()
        ],
        "edges": [{"source": u, "target": v} for u, v in G.edges()],
    }
    args.out.with_suffix(".json").write_text(json.dumps(graph_json, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ HTML saved to: {args.out}")
    print(f"📄 JSON saved to: {args.out.with_suffix('.json')}")
    print(f"📚 Sources scanned: {len(sources)} (pattern: ADictML_*.tex)")
    print(f"🧠 Terms parsed: {len(glossary)} | Edges: {G.number_of_edges()}")


if __name__ == "__main__":
    main()
