import re

def parse_macros_with_args(macros_file):
    """
    Parses \\newcommand macros from a LaTeX file into a dictionary.
    Returns a dict {macro_name: (num_args, body)}.
    """
    macros = {}
    pattern = re.compile(r'\\newcommand\s*{\\([a-zA-Z@]+)}(?:\[(\d+)\])?\s*{(.+)}')

    with open(macros_file, "r", encoding="utf-8") as f:
        for line in f:
            match = pattern.match(line.strip())
            if match:
                name = match.group(1)
                num_args = int(match.group(2)) if match.group(2) else 0
                body = match.group(3)
                macros[name] = (num_args, body)
    return macros

def remove_index_commands(content):
    """
    Removes LaTeX \\index{...} commands (e.g., 'foo\\index{bar}' → 'foo').
    """
    return re.sub(r'\\index\{[^{}]*\}', '', content)

def flatten_glossary_macros(content, glossary_names):
    """
    Replaces \gls{key} with the corresponding name.
    \glspl{key} appends 's' to the name (basic plural).
    """
    # Replace \glspl{key}
    content = re.sub(
        r'\\glspl\{([^\{\}]+)\}',
        lambda m: glossary_names.get(m.group(1), m.group(1)) + 's',
        content
    )
    # Replace \gls{key}
    content = re.sub(
        r'\\gls\{([^\{\}]+)\}',
        lambda m: glossary_names.get(m.group(1), m.group(1)),
        content
    )
    return content

def expand_macro(name, args, body):
    """
    Substitutes #1, #2, ..., #n in macro body with provided args.
    """
    for i, arg in enumerate(args, start=1):
        body = body.replace(f"#{i}", arg)
    return body

def flatten_tex_macros(source_file, macros, output_file, glossary_names):
    """
    Replaces macro invocations in a LaTeX file with their expanded definitions.
    """
    with open(source_file, "r", encoding="utf-8") as f:
        content = f.read()

    changed = True
    while changed:
        previous_content = content

        for name, (num_args, body) in macros.items():
            if num_args == 0:
                # Match \name, even if followed by underscore or braces (e.g., \featureidx_{1})
                pattern = re.compile(rf'\\{name}(?![a-zA-Z@])')
                content = pattern.sub(lambda m: body, content)
            elif num_args == 1:
                # Match both \macro{arg} and \macro_{arg}
                pattern1 = re.compile(rf'\\{name}\{{([^{{}}]*)\}}')
                pattern2 = re.compile(rf'\\{name}_\{{([^{{}}]*)\}}')

                content = pattern1.sub(lambda m: expand_macro(name, [m.group(1)], body), content)
                content = pattern2.sub(lambda m: expand_macro(name, [m.group(1)], body), content)
            else:
                # Match \macro{a}{b}... (n args)
                args_group = ''.join([r'\{([^{}]*)\}'] * num_args)
                pattern = re.compile(rf'\\{name}{args_group}')

                content = pattern.sub(lambda m: expand_macro(name, list(m.groups()), body), content)

        changed = (content != previous_content)
    content = flatten_glossary_macros(content, glossary_names)
    content = remove_index_commands(content)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Flattened file written to: {output_file}")
    
    
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
    raise ValueError("Unbalanced braces")
    
def parse_glossary_names(source_file):
    """
    Parses glossary key → name from \newglossaryentry{key}{...} definitions.
    Handles multiline, nested glossary bodies with spacing.
    Returns a dictionary {key: name}.
    """
    glossary_names = {}

    with open(source_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Match \newglossaryentry{key} and find start of {body}
    entry_start_pattern = re.compile(r'\\newglossaryentry\{([^\}]+)\}\s*\{', re.MULTILINE)
    pos = 0
    while True:
        match = entry_start_pattern.search(content, pos)
        if not match:
            break

        key = match.group(1)
        brace_start = match.end() - 1  # the opening `{` of the body
        try:
            body, next_pos = extract_balanced_braces(content, brace_start)
        except Exception as e:
            print(f"⚠️ Skipping entry '{key}': {e}")
            pos = match.end()
            continue

        # Remove LaTeX comments
        body_cleaned = re.sub(r'%.*', '', body)

        # Find name={...}
        name_match = re.search(r'name\s*=\s*\{([^{}]*)\}', body_cleaned)
        if name_match:
            glossary_names[key.strip()] = name_match.group(1).strip()
        else:
            print(f"⚠️ No name=... found in entry '{key}'")

        pos = next_pos  # continue search from end of current entry

    return glossary_names



# === USAGE EXAMPLE ===
if __name__ == "__main__":
    macros_file = "ml_macros.tex"
    source_file = "../ADictML_Glossary_English.tex"
    output_file = "ADictML_Glossary_Expanded.tex"

    macros = parse_macros_with_args(macros_file)
    glossary_names = parse_glossary_names(source_file)

    flatten_tex_macros(source_file, macros, output_file, glossary_names)
