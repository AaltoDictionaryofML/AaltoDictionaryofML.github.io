
import re
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import tempfile
import os
import subprocess
from pdf2image import convert_from_path

def extract_tikz_from_entry(entry_text):
    match = re.search(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', entry_text, re.DOTALL)
    if match:
        return match.group(0)
    else:
        # Try fallback for your custom {tikzpicture} ... {tikzpicture} style
        match = re.search(r'\{tikzpicture\}.*?\{tikzpicture\}', entry_text, re.DOTALL)
        if match:
            tikz_inner = match.group(0)[13:-13].strip()  # remove {tikzpicture} ... {tikzpicture}
            return f"\\begin{{tikzpicture}}\n{tikz_inner}\n\\end{{tikzpicture}}"
    raise ValueError("No tikzpicture found")
    

def compile_tikz_to_png(tikz_code, filename="tikz_figure", output_dir="blog_posts/images"):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Output path (e.g., blog_posts/images/generalization.png)
    output_png_path = os.path.join(output_dir, f"{filename}.png")

    # LaTeX document wrapper
    latex_code = f"""
\\documentclass[tikz]{{standalone}}
\\usepackage{{tikz}}
\\usetikzlibrary{{positioning, arrows.meta, calc, decorations.pathreplacing}}
\\begin{{document}}
{tikz_code}
\\end{{document}}
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "figure.tex")
        with open(tex_path, "w") as f:
            f.write(latex_code)

        # Compile LaTeX to PDF
        subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_path],
                       cwd=tmpdir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        pdf_path = os.path.join(tmpdir, "figure.pdf")

        # Convert PDF to PNG using ImageMagick
        subprocess.run([
            "convert", "-density", "300", pdf_path, "-quality", "90", output_png_path
        ])

    print(f"✅ Saved PNG to: {output_png_path}")
    
    

        

# --- Step 1: Load LaTeX glossary content ---
with open("ADictML_Glossary_English.tex", "r", encoding="utf-8") as f:
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
for key, body in entries:
    body_cleaned = re.sub(r"%.*", "", body)          # remove comments
    body_cleaned = re.sub(r"[ \t]+", " ", body)      # collapse horizontal whitespace only
    body_cleaned = re.sub(r"\s+\n", "\n", body_cleaned)  # optional: clean trailing space before linebreak

    
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

    print(desc_text+"\n")
    glossary[key.strip()] = desc_text


entry_text = glossary["generalization"]
try:
    tikz_code = extract_tikz_from_entry(entry_text)
    compile_tikz_to_png(tikz_code, "generalization_tikz")
except Exception as e:
    print("Error:", e)