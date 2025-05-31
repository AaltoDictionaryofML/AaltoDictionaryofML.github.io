#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 31 10:55:54 2025

@author: junga1
"""

import os
import re
import subprocess
from pathlib import Path
from datetime import date

# Configurations
GLOSSARY_FILE = "glossary_entries.tex"
BLOG_DIR = Path("blog_posts")
IMG_DIR = BLOG_DIR / "images"

BLOG_TEMPLATE = """---
title: "{title}"
date: {date}
tags: [machine learning, glossary]
math: true
---

{content}

{img_section}
"""

BLOG_DIR.mkdir(parents=True, exist_ok=True)
IMG_DIR.mkdir(parents=True, exist_ok=True)

def extract_all_entries(tex_file):
    with open(tex_file, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"\\newglossaryentry\{(.*?)\}\{.*?description=\{(.*?)\},\s*first="  # capture label and description
    return re.findall(pattern, content, re.DOTALL)

def extract_tikz_and_caption(description):
    tikz_match = re.search(r"\\begin{tikzpicture}(.*?)\\end{tikzpicture}", description, re.DOTALL)
    caption_match = re.search(r"\\caption\{(.*?)\}", description, re.DOTALL)
    return tikz_match.group(1) if tikz_match else "", caption_match.group(1) if caption_match else ""

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

def sanitize_text_for_blog(text):
    # Convert LaTeX math mode to MathJax-style `$...$`
    text = re.sub(r"\$(.*?)\$", r"\\(\1\\)", text, flags=re.DOTALL)
    # Clean glossary and citation commands
    text = re.sub(r"\\gls(pl)?\{.*?\}", "", text)
    text = re.sub(r"\\index\{.*?\}", "", text)
    text = re.sub(r"\\cite\{.*?\}", "", text)
    text = re.sub(r"\\newpage", "", text)
    text = re.sub(r"\\label\{.*?\}", "", text)
    return text.strip()

def create_blog_post(term_name, description, image_path=None, caption=""):
    clean_text = sanitize_text_for_blog(description)

    img_rel_path = f"./images/{image_path.name}" if image_path else ""
    img_section = f"![{caption}]({img_rel_path})" if image_path else ""

    post = BLOG_TEMPLATE.format(
        title=term_name.capitalize(),
        date=date.today().isoformat(),
        content=clean_text,
        img_section=img_section
    )

    post_path = BLOG_DIR / f"{term_name}.md"
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(post)

def main():
    entries = extract_all_entries(GLOSSARY_FILE)
    for term_name, description in entries:
        print(f"Processing term: {term_name}")
        tikz_code, caption = extract_tikz_and_caption(description)
        fig_path = None
        if tikz_code:
            fig_path = compile_tikz(tikz_code, term_name)
        create_blog_post(term_name, description, fig_path, caption)

if __name__ == "__main__":
    main()