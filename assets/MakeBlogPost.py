
import re
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import tempfile
import os
from pathlib import Path
from datetime import date
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
    
def replace_tikz_with_includegraphics(description, image_path):
    """
    Replace the TikZ block in the description with a single \includegraphics command.
    """
    include_cmd = fr"\\includegraphics[width=0.8\\linewidth]{{{image_path}}}"
    print(include_cmd)
    print(re.sub(
        r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',
        include_cmd,
        description,
        count=1,
        flags=re.DOTALL
    ))
    return re.sub(
        r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',
        include_cmd,
        description,
        count=1,
        flags=re.DOTALL
    )


def compile_tikz_to_png(tikz_code, filename="tikz_figure", output_dir="blog_posts/images"):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Output path (e.g., blog_posts/images/generalization.png)
    output_png_path = os.path.join(output_dir, f"{filename}.png")

    # LaTeX document wrapper
    latex_code = f"""
\\documentclass[tikz]{{standalone}}
\\usepackage{{tikz}}
\\usepackage[dvipsnames]{{xcolor}}
\\usetikzlibrary{{positioning, arrows.meta, calc, decorations.pathreplacing}}
\\definecolor{{lightblue}}{{RGB}}{{173, 216, 230}}
\\begin{{document}}
{tikz_code}
\\end{{document}}
"""
    tex_path ="figure.tex"
    with open(tex_path, "w") as f:
        f.write(latex_code)
        print(latex_code)

        # Compile LaTeX to PDF
    subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_path])
    print(tex_path)

    pdf_path = "figure.pdf"

        # Convert PDF to PNG using ImageMagick
    subprocess.run([
            "convert", "-density", "300", pdf_path, "-quality", "90", output_png_path
        ])

    print(f"✅ Saved PNG to: {output_png_path}")
    
    
def generate_texfile_with_image(term, description, image_path, output_dir="blog_posts"):
    """
    Generate a LaTeX file containing the full glossary description with the TikZ replaced by image.
    """
    from pathlib import Path

    tex_output_path = Path(output_dir) / f"{term}.tex"
    os.makedirs(tex_output_path.parent, exist_ok=True)

    # Replace TikZ block with includegraphics
    description_with_image = replace_tikz_with_includegraphics(description, image_path)

    # Generate LaTeX document
    tex_code = f"""\\documentclass{{article}}
\\usepackage{{graphicx}}
\\usepackage{{caption}}
\\usepackage{{amsmath, amssymb}}
\\usepackage[margin=2.5cm]{{geometry}}

\\begin{{document}}

\\section*{{{term.capitalize()}}}

{description_with_image}

\\end{{document}}
"""

    with open(tex_output_path, "w", encoding="utf-8") as f:
        f.write(tex_code)
        print(f"✅ LaTeX file written to: {tex_output_path}")

        


def generate_blog_post(
    tex_file,
    bib_file,
    output_dir="blog_posts",
    title="Dictionary of ML – Geometric Median",
    seo_title="Geometric Median – A Robust Alternative to the Mean in Machine Learning",
    seo_description="Understand the geometric median, a key concept in robust statistics and machine learning, minimizing total distance to data points and outperforming the mean under outliers.",
    post_slug="geometric-median",
    post_date=None
):
    """
    Converts a LaTeX file to Markdown using Pandoc and adds Jekyll front matter.

    Args:
        tex_file (str): Path to LaTeX file.
        bib_file (str): Path to BibTeX file.
        output_dir (str): Directory to save generated .md post.
        title (str): Title for the blog post.
        seo_title (str): SEO title for the blog post.
        seo_description (str): SEO description.
        post_slug (str): Filename slug.
        post_date (str): Publication date (YYYY-MM-DD), defaults to today.
    """
    post_date = post_date or date.today().isoformat()
    filename = f"{post_date}-{post_slug}.md"
    output_path = Path(output_dir) / filename

    os.makedirs(output_path.parent, exist_ok=True)

    # Temporary file for Pandoc output (without front matter)
    temp_md_path = Path("temp_pandoc_output.md")

    # Build and run Pandoc command
    command = [
        "pandoc",
        tex_file,
        "-o", str(temp_md_path),
        "--from=latex",
        "--to=markdown",
        "--standalone",
        "--citeproc",
        f"--bibliography={bib_file}"
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("❌ Pandoc conversion failed:", e)
        return

    # Read and wrap with front matter
    with open(temp_md_path, "r", encoding="utf-8") as f:
        markdown_body = f.read()

    front_matter = f"""---
layout: post
title: "{title}"
date: {post_date}
seo_title: "{seo_title}"
seo_description: "{seo_description}"
markdown: kramdown
---

"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(front_matter + markdown_body)

    os.remove(temp_md_path)

    print(f"✅ Blog post written to: {output_path}")





# --- Step 1: Load LaTeX glossary content ---
with open("ADictML_Glossary_Expanded.tex", "r", encoding="utf-8") as f:
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


blog_sample_term= "generalization"
entry_text = glossary[blog_sample_term]
try:
    tikz_code = extract_tikz_from_entry(entry_text)
    compile_tikz_to_png(tikz_code, blog_sample_term+"_tikz")
    generate_texfile_with_image(
        term=blog_sample_term,
        description=entry_text,
        image_path="blog_posts/images/"+blog_sample_term+"_tikz.png"
    )
    generate_blog_post(
       tex_file="blog_posts/"+blog_sample_term+".tex" ,
       bib_file="Literature.bib",
       post_slug="generalization",
       title="Aalto Dictionary of ML – "+blog_sample_term,
       seo_title="Generalization – How Machine Learning Models Handle Unseen Data",
       seo_description="Explore the concept of generalization in machine learning: how models trained on a dataset perform on new, unseen data.",
       output_dir="blog_posts"
   )

except Exception as e:
    print("Error:", e)
