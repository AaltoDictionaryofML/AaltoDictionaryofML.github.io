import re

def parse_macros_with_args(macros_file):
    """
    Parses \newcommand macros from a LaTeX file into a dictionary.
    Supports macros with up to 9 arguments.
    Returns: {name: (num_args, body)}
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

def expand_macro(name, args, body):
    """Substitute #1..#n in macro body with provided args"""
    for i, arg in enumerate(args, start=1):
        body = body.replace(f"#{i}", arg)
    return body

def flatten_tex_macros(source_file, macros, output_file):
    with open(source_file, "r", encoding="utf-8") as f:
        content = f.read()

    for name, (num_args, body) in macros.items():
        if num_args == 0:
            pattern = re.compile(rf'\\{name}\b')
            content = pattern.sub(lambda m: body, content)
        else:
            # Match \name{...}{...} (as many args as needed)
            args_pattern = r'\\' + name + ''.join([r'\{([^{}]*)\}'] * num_args)
            pattern = re.compile(args_pattern)

            def replacer(match):
                args = match.groups()
                return expand_macro(name, args, body)

            content = pattern.sub(replacer, content)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Flattened file written to: {output_file}")

# === USAGE ===
macros_file = "assets/ml_macros.tex"
source_file = "ADictML_Glossary_English.tex"
output_file = "ADictML_Glossary_Expanded.tex"

macros = parse_macros_with_args(macros_file)
flatten_tex_macros(source_file, macros, output_file)