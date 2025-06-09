import re

def remove_comments(text):
    """
    Removes LaTeX comments starting with %, including inline comments.
    Skips escaped percent signs (\%).
    """
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        # Remove everything after a % unless it’s escaped as \%
        pos = 0
        while True:
            idx = line.find('%', pos)
            if idx == -1:
                cleaned_lines.append(line)
                break
            elif idx > 0 and line[idx-1] == '\\':
                pos = idx + 1  # skip escaped %
            else:
                cleaned_lines.append(line[:idx])
                break
    return '\n'.join(cleaned_lines)

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

def flatten_glossary_macros(content, glossary_data):
    """
    Replaces glossary macros with plain text:
    - \gls{key}    → name
    - \glspl{key}  → firstplural
    - \Gls{key}    → Name (capitalized)
    - \Glspl{key}  → Firstplural (capitalized)
    """

    def capitalize_first(s):
        return s[0].upper() + s[1:] if s else s

    content = re.sub(
        r'\\Glspl\{([^\{\}]+)\}',
        lambda m: capitalize_first(glossary_data.get(m.group(1), {}).get("firstplural", m.group(1) + "s")),
        content
    )

    content = re.sub(
        r'\\Gls\{([^\{\}]+)\}',
        lambda m: capitalize_first(glossary_data.get(m.group(1), {}).get("name", m.group(1))),
        content
    )

    content = re.sub(
        r'\\glspl\{([^\{\}]+)\}',
        lambda m: glossary_data.get(m.group(1), {}).get("firstplural", m.group(1) + "s"),
        content
    )

    content = re.sub(
        r'\\gls\{([^\{\}]+)\}',
        lambda m: glossary_data.get(m.group(1), {}).get("name", m.group(1)),
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

def replace_macro_calls_with_nested_args(text, name, num_args, body):
    pattern = re.compile(rf'\\{name}(?![a-zA-Z@])')
    pos = 0
    result = []

    while pos < len(text):
        match = pattern.search(text, pos)
        if not match:
            result.append(text[pos:])
            break

        start = match.start()
        end = match.end()
        args = []
        current_pos = end

        try:
            for _ in range(num_args):
                # Skip whitespace
                while current_pos < len(text) and text[current_pos].isspace():
                    current_pos += 1

                if current_pos >= len(text) or text[current_pos] != '{':
                    context = text[start:start+50].replace('\n', ' ')
                    print(f"⚠️ Could not expand \\{name} at pos {start}: expected '{{' at pos {current_pos}")
                    print(f"    ↪ Context: '{context.strip()}...'")
                    raise ValueError("Expected '{'")

                arg, current_pos = extract_balanced_braces(text, current_pos)
                args.append(arg)

            expansion = expand_macro(name, args, body)
            result.append(text[pos:start])
            result.append(expansion)
            pos = current_pos

        except Exception:
            result.append(text[pos:end])
            pos = end

    return ''.join(result)


def flatten_tex_macros(source_file, macros, output_file, glossary_names):
    """
    Replaces macro invocations in a LaTeX file with their expanded definitions.
    """
    with open(source_file, "r", encoding="utf-8") as f:
        content = remove_comments(f.read())
    
        

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

               # content = pattern1.sub(lambda m: expand_macro(name, [m.group(1)], body), content)
                #content = pattern2.sub(lambda m: expand_macro(name, [m.group(1)], body), content)
                content = replace_macro_calls_with_nested_args(content, name, num_args, body)
            else:
                # Match \macro{a}{b}... (n args)
               # args_group = ''.join([r'\{([^{}]*)\}'] * num_args)
               # pattern = re.compile(rf'\\{name}{args_group}')

               # content = pattern.sub(lambda m: expand_macro(name, list(m.groups()), body), content)
                content = replace_macro_calls_with_nested_args(content, name, num_args, body)

        changed = (content != previous_content)
    content = flatten_glossary_macros(content, glossary_names)
    content = remove_index_commands(content)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Flattened file written to: {output_file}")
    
    
def extract_balanced_braces(text, start_index):
    """
    Extracts a block enclosed in balanced braces starting at start_index.
    Returns (block_content, index_after_block).
    """
    if text[start_index] != '{':
        raise ValueError("Expected opening brace at start_index")

    depth = 0
    pos = start_index
    while pos < len(text):
        if text[pos] == '{':
            depth += 1
        elif text[pos] == '}':
            depth -= 1
            if depth == 0:
                return text[start_index + 1:pos], pos + 1
        pos += 1

    raise ValueError("No matching closing brace found")

    
def parse_glossary_names(source_file):
    """
    Parses glossary key → {'name': ..., 'firstplural': ...} from \newglossaryentry definitions.
    Handles multiline and nested braces.
    """
    glossary_data = {}

    with open(source_file, "r", encoding="utf-8") as f:
        content = remove_comments(f.read())

    entry_start_pattern = re.compile(r'\\newglossaryentry\{([^\}]+)\}\s*\{', re.MULTILINE)
    pos = 0
    while True:
        match = entry_start_pattern.search(content, pos)
        if not match:
            break

        key = match.group(1)
        brace_start = match.end() - 1
        try:
            body, next_pos = extract_balanced_braces(content, brace_start)
        except Exception as e:
            print(f"⚠️ Skipping entry '{key}': {e}")
            pos = match.end()
            continue

        body_cleaned = re.sub(r'%.*', '', body)

        name_match = re.search(r'text\s*=\s*\{([^{}]*)\}', body_cleaned)
        plural_match = re.search(r'plural\s*=\s*\{([^{}]*)\}', body_cleaned)

        if name_match:
            glossary_data[key.strip()] = {
                'name': name_match.group(1).strip(),
                'firstplural': plural_match.group(1).strip() if plural_match else name_match.group(1).strip() + 's'
            }
        else:
            print(body)
            print(f"⚠️ No name=... found in entry '{key}'")

        pos = next_pos

    return glossary_data



# === USAGE EXAMPLE ===
if __name__ == "__main__":
    macros_file = "ml_macros.tex"
    source_file = "../ADictML_Glossary_English.tex"
    output_file = "ADictML_Glossary_Expanded.tex"

    macros = parse_macros_with_args(macros_file)
    glossary_names = parse_glossary_names(source_file)

    flatten_tex_macros(source_file, macros, output_file, glossary_names)
