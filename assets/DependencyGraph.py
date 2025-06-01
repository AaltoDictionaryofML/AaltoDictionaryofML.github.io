
import re
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from networkx.algorithms.community import greedy_modularity_communities
from jinja2 import Environment, FileSystemLoader
import json

# Change working directory to the directory of this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- Step 1: Load LaTeX glossary content ---
with open("../ADictML_Glossary_English.tex", "r", encoding="utf-8") as f:
    content = f.read()

# --- Step 2: Match glossary entries ---
entry_pattern = re.compile(r"\\newglossaryentry\{([^}]+)\}\s*\{(.*?)\n\}", re.DOTALL)
entries = entry_pattern.findall(content)



# --- Step 3: Extract content inside balanced braces ---
def extract_balanced_braces(s, start):
    assert s[start] == '{'
    depth = 0
    for i in range(start, len(s)):
        if s[i] == '{':
            depth += 1
        elif s[i] == '}':
            depth -= 1
            if depth == 0:
                return s[start + 1:i], i + 1
    raise ValueError("Unbalanced braces in LaTeX description.")

# --- Step 4: Parse glossary entries ---
glossary = {}
glossary_names = {}
glossary_references = {}

for key, body in entries:
    body_cleaned = re.sub(r"%.*", "", body)
    body_cleaned = " ".join(body_cleaned.split())
    
    # --- Extract name ---
    name_start = body_cleaned.find("name=") 
    try:
        name_text, _ = extract_balanced_braces(body_cleaned, name_start + len("name="))
    except:
        name_text = key  # fallback

    # --- Extract description ---
    desc_start = body_cleaned.find("description={")
    if desc_start == -1:
        continue

    try:
        desc_text, _ = extract_balanced_braces(body_cleaned, desc_start + len("description="))
    except ValueError:
        continue

    # --- Step 5: Extract \gls{} references before cleanup ---
    gls_refs = re.findall(r"\\(?:gls|Gls)\{([^{}]+)\}", desc_text)

    # --- Step 6: Clean LaTeX macros for final display text ---
    desc = re.sub(r"\\(gls|Gls|index|cite|textbf|textit|emph)\{[^{}]*\}", "", desc_text)
    desc = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", "", desc)  # remove commands
    desc = re.sub(r"\$[^$]*\$", "", desc)  # remove inline math
    desc = " ".join(desc.split())
    print(desc_text+"\n")
    glossary[key.strip()] = desc
    glossary_names[key.strip()] = name_text.strip()
    glossary_references[key.strip()] = gls_refs

# --- Step 7: Build dependency graph ---
G = nx.DiGraph()
G.add_nodes_from(glossary.keys())

for term, desc in glossary.items():
    # Edges from explicit \gls{} references
    for referenced in glossary_references.get(term, []):
        if referenced in glossary and referenced != term:
            G.add_edge(term, referenced)

    # Edges from plain-text mentions
    for other_term in glossary:
        if other_term != term and re.search(rf"\b{re.escape(other_term)}\b", desc):
            G.add_edge(term, other_term)
            
            
            
# --- Step 1: Community Detection ---
communities = list(greedy_modularity_communities(G))
color_palette = ["lightblue", "lightgreen", "salmon", "orange", "violet", "khaki", "lightcoral"]

color_map = {}
for i, community in enumerate(communities):
    for node in community:
        color_map[node] = color_palette[i % len(color_palette)]

node_colors = [color_map.get(n, "gray") for n in G.nodes]

# --- Step 2: Custom labels (hide low-degree terms) ---
labels = {node: glossary_names[node] for node in G.nodes if G.degree[node] > 1}

# --- Step 3: Node size by degree ---
node_sizes = [300 + 150 * G.degree[n] for n in G.nodes]

# --- Step 4: Layout and Plotting ---
plt.figure(figsize=(24, 20))
pos = nx.kamada_kawai_layout(G)  # or try spring_layout(G, k=0.8)
pos = nx.spring_layout(G, k=0.9)

nx.draw(
    G,
    pos,
    node_color=node_colors,
    node_size=node_sizes,
    edge_color="gray",
    with_labels=False,
    arrows=True
)

nx.draw_networkx_labels(G, pos, labels=labels, font_size=20)

plt.title("Glossary Dependency Graph (Community-Colored, Label Filtered)", fontsize=20)
plt.tight_layout()
plt.show()

def generate_html(G, glossary, glossary_names, filename="glossary_network.html"):
    import json

    node_id_map = {node: i+1 for i, node in enumerate(G.nodes())}
    vis_nodes = []
    vis_edges = []

    for node in G.nodes():
        vis_nodes.append({
            "id": node_id_map[node],
            "label": glossary_names.get(node, node),
            "title": glossary.get(node, ""),
            "color": color_map.get(node, "gray")
        })

    for u, v in G.edges():
        vis_edges.append({
            "from": node_id_map[u],
            "to": node_id_map[v]
        })

    html_template = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Glossary Network</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" />
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js"></script>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
      #mynetwork {{
        width: 100%;
        height: 1000px;
        background-color: #ffffff;
        border: 1px solid lightgray;
      }}
    </style>
  </head>
  <body>
    <center><h1>The Aalto Dictionary of Machine Learning</h1></center>
    <div id="mynetwork"></div>
    <script type="text/javascript">
      const nodes = new vis.DataSet({json.dumps(vis_nodes, indent=2)});
      const edges = new vis.DataSet({json.dumps(vis_edges, indent=2)});
      const container = document.getElementById("mynetwork");
      const data = {{ nodes: nodes, edges: edges }};
      const options = {{
        nodes: {{
          shape: "dot",
          size: 20,
          font: {{ size: 14, color: "#000" }}
        }},
        edges: {{
          arrows: "to",
          color: "gray",
          smooth: true
        }},
        physics: {{
          enabled: true,
          solver: "forceAtlas2Based",
          stabilization: {{
            enabled: true,
            iterations: 200,
            fit: true
          }}
        }},
        interaction: {{
          navigationButtons: true,
          keyboard: true,
          zoomView: true,
          dragView: true
        }}
      }};
      const network = new vis.Network(container, data, options);
    </script>
  </body>
</html>"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"✅ HTML saved as {filename}")

# --- Generate HTML ---
generate_html(G, glossary, glossary_names)
