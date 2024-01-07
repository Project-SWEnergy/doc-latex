import argparse
import os

def get_glossario(path_to_glossario: str):
    glossario = []
    with open(path_to_glossario, 'r') as f:
        for line in f:
            line = line.strip()
            (word, definition) = line.split(',', 1)
            glossario.append((word, definition))

    glossario.sort(key=lambda x: x[0])
    return glossario

def glossary_builder(glossario: list):
    tex = '\\makeglossaries\n'
    prev_letter = ''
    for word, definition in glossario:
        if word[0] != prev_letter:
            prev_letter = word[0]
            tex += f'\n% {word[0]}\n\n'
        tex += f'\\newglossaryentry{{{word}}}{{\n\tname={word},\n\tdescription={{{definition}}}\n}}\n'
    tex += '\\glsaddall\n'
    return tex

def tex_builder(glossario: list):
    tex = ''
    prev_letter = ''
    for word, definition in glossario:
        if word[0] != prev_letter:
            prev_letter = word[0]
            tex += f'\n\\section{{{word[0]}}}\n\n'

        tex += f'\\paragraph{{{word}}}{{{definition}}}\n'
    return tex

def main(src, out):
    glossario = get_glossario(src)
    gls = glossary_builder(glossario)
    document = tex_builder(glossario)
    with open(out + "/gls.tex", 'w') as f:
        f.write(gls)
    with open(out + "/document.tex", 'w') as f:
        f.write(document)

parser = argparse.ArgumentParser(description='Glossario builder')
parser.add_argument('-s', '--source', help='Path to source file', required=True)
parser.add_argument('-o', '--output', help='Path to output file', required=True)

args = parser.parse_args()
src = os.path.abspath(args.source)
out = os.path.abspath(args.output)

main(src, out)
