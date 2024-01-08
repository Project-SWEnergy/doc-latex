import csv
import re
import os
import argparse

# glossario è una lista di termini
def get_glossario(path_to_glossario):
    glossario = set()
    with open(path_to_glossario, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            glossario.add(row[0])
    return glossario

def recursive_apply(src, fn):
    for root, dirs, files in os.walk(src):
        for file in files:
            if file.endswith('.tex'):
                fn(os.path.join(root, file))
        for dir in dirs:
            recursive_apply(dir, fn)

# aggiunge una g a apice ai termini nel glossario
def apix(file):
    # Apre il file e lo legge
    with open(file, 'r') as f:
        text = f.read()

        for termine in glossario:
            # Aggiunge una g a apice ai termini nel glossario
            text = re.sub(termine, termine, text, 
                          flags=re.IGNORECASE)
            text = re.sub(r'\\gls{' + termine + r'}', termine, text)
            text = re.sub(termine, r'\\gls{' + termine + r'}$^G$', text)

    # Scrive il file
    with open(file, 'w') as f:
        f.write(text)


parser = argparse.ArgumentParser(description='Compile LaTeX files.')

parser.add_argument('-o', '--output', help='Destination directory')
parser.add_argument('-s', '--source', help='Source directory')
parser.add_argument('-g', '--glossary', help='Path to glossary file', required=True)

args = parser.parse_args()

destination_directory = os.path.abspath(args.output)
source_directory = os.path.abspath(args.source)
glossary_path = os.path.abspath(args.glossary)

glossario = get_glossario(glossary_path)
recursive_apply(source_directory, apix)
