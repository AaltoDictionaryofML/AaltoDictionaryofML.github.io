import os
import re
import subprocess
from pathlib import Path
from datetime import date

# Configuration
GLOSSARY_FILE = "ADictML_Glossary_English.tex"
TARGET_LABEL = "generalization"  # <-- Change this to the desired glossary label
BLOG_DIR = Path("blog_posts")
IMG_DIR = BLOG_DIR / "images"

BLOG_TEMPLATE = """---
title: "{title}"
date: {date}
tags: [machine learning, glossary]
---

{content}

![Figure]({img_path})
"""

BLOG_DIR.mkdir(parents=True, exist_ok=True)
IMG_DIR.mkdir(parents=True, exist_ok=True)



def extract_glossary_entry(tex_file, label):
    with open(tex_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Step 1: Find start of \newglossaryentry{label}{
    start_marker = f"\\newglossaryentry{{{label}}}{{"
    start_idx = content.find(start_marker)
    if start_idx == -1:
        raise ValueError(f"No glossary entry found for label '{label}'")

    # Step 2: Read from opening brace after marker
    brace_idx = content.find("{", start_idx + len(start_marker))
    if brace_idx == -1:
        raise ValueError("Malformed glossary entry")

    # Step 3: Find the matching closing brace
    brace_count = 1
    end_idx = brace_idx + 1
    while brace_count > 0 and end_idx < len(content):
        if content[end_idx] == "{":
            brace_count += 1
        elif content[end_idx] == "}":
            brace_count -= 1
        end_idx += 1

    entry_body = content[brace_idx + 1:end_idx - 1]  # everything inside {...}

    # Step 4: Parse description={...} at top level of entry_body
    i = 0
    while i < len(entry_body):
        if entry_body[i:].startswith("description={"):
            # Found start of description
            i += len("description={")
            desc_start = i
            brace_count = 1
            while brace_count > 0 and i < len(entry_body):
                if entry_body[i] == "{":
                    brace_count += 1
                elif entry_body[i] == "}":
                    brace_count -= 1
                i += 1
            description = entry_body[desc_start:i - 1]
            return label, description.strip()
        i += 1

    raise ValueError(f"No description found in entry '{label}'")



def extract_tikz_and_caption(description):
    print(description)
    figure_match = re.search(
        r"\\begin\{figure\}.*?\\begin\{tikzpicture\}(.*?)\\end\{tikzpicture\}.*?\\caption\{(.*?)\}",
        description,
        re.DOTALL
    )
    if figure_match:
        print(figure_match)
        tikz_code = figure_match.group(1)
        caption = figure_match.group(2)
        return tikz_code, caption
    return "", ""


def compile_tikz(tikz_code, fig_name):
    tex_doc = f"""
\\documentclass{{standalone}}
\\usepackage{{tikz}}
\\usepackage{{xcolor}}
\\begin{{document}}
\\begin{{tikzpicture}}[scale=0.8]
{tikz_code}
\\end{{tikzpicture}}
\\end{{document}}
"""
    tex_path = IMG_DIR / f"{fig_name}.tex"
    pdf_path = IMG_DIR / f"{fig_name}.pdf"
    png_path = IMG_DIR / f"{fig_name}.png"

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex_doc)

    subprocess.run(["pdflatex", "-output-directory", str(IMG_DIR), str(tex_path)], check=True)
    subprocess.run(["convert", "-density", "300", str(pdf_path), str(png_path)], check=True)

    return png_path

def sanitize_latex_text(text):
    text = re.sub(r"\\gls(pl)?\{.*?\}", "", text)
    text = re.sub(r"\\index\{.*?\}", "", text)
    text = re.sub(r"\\cite\{.*?\}", "", text)
    text = re.sub(r"\$.*?\$", "", text)
    text = re.sub(r"\\begin\{figure\}.*?\\end\{figure\}", "", text, flags=re.DOTALL)
    text = re.sub(r"\\newpage", "", text)
    return text.strip()

def create_blog_post(term_name, description, image_path):
    clean_text = sanitize_latex_text(description)
    today = date.today().isoformat()
    title = term_name.capitalize()
    img_rel_path = f"./images/{image_path.name}" if image_path else ""

    blog_content = BLOG_TEMPLATE.format(
        title=title,
        date=today,
        content=clean_text,
        img_path=img_rel_path
    )

    post_path = BLOG_DIR / f"{term_name}.md"
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(blog_content)

def main():
    term_name, description = extract_glossary_entry(GLOSSARY_FILE, TARGET_LABEL)
    tikz_code, caption = extract_tikz_and_caption(description)

    if tikz_code:
        fig_path = compile_tikz(tikz_code, term_name)
        create_blog_post(term_name, description, fig_path)
        print(f"✅ Blog post for '{term_name}' created with image.")
    else:
        create_blog_post(term_name, description, None)
        print(f"✅ Blog post for '{term_name}' created without image.")

if __name__ == "__main__":
    main()
