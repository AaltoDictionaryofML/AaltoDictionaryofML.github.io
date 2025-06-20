#this document will print all the missing definitions in your translation by comparing it to the original english version
import re

def extract_keys(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return set(re.findall(r'\\newglossaryentry{([^}]+)}', content))

en_file = 'ADictML_Glossary_English.tex' #include the english one here
es_file = 'translations/es/ADictML_Glossary_ES.tex' #include your translation here

en_keys = extract_keys(en_file)
es_keys = extract_keys(es_file)

missing_in_es = en_keys - es_keys
print("Missing entries in ES version:")
for key in sorted(missing_in_es):
    print(f"- {key}")


# to run this, open the terminal in vscode, and type the command : python3 glossary_diff.py and it will list you the missing defintions.