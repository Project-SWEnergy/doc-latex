# Questo programma è diviso in tre parti:
# - la prima parte accumula i termini in un set
# - la seconda parte controlla i file e segna i termini nel glossario con una g
# a apice
# - la terza parte controlla per i termini segnati con una g a apice e segnala i
# termini che non sono stati trovati nel glossario
#
# Il glossario è un csv con due colonne: termine, definizione

import csv
import re
import os
import argparse

# Prima parte: accumula i termini in un set
# -----------------------------------------
def get_glossario(path_to_glossario):
    glossario = set()
    with open(path_to_glossario, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            glossario.add(row[0])
    return glossario

# Seconda parte: controlla i file e segna i termini nel glossario con una g a
# apice
# -------------------------------------------------------------------------
# Ricorsivamente, per ogni file nella directory corrente e nelle sottodirectory
# controlla se il file è un file .tex e se lo è, controlla se ci sono termini
# nel glossario. Se ci sono, segna i termini con una g a apice.

# Funzione che ricorsivamente entra i tutte le sottodirectory, prende una
# funzione come argomento e la applica a tutti i file .tex
def recursive_apply(src, fn, glossario):
    for root, dirs, files in os.walk(src):
        for file in files:
            if file.endswith('.tex'):
                fn(os.path.join(root, file), glossario)
        for dir in dirs:
            recursive_apply(dir, fn, glossario)

# Funzione che controlla se ci sono termini nel glossario e li segna con una g
# a apice
def check_glossario(file, glossario):
    # Apre il file e lo legge
    with open(file, 'r') as f:
        text = f.read()
    # Controlla se ci sono termini nel glossario
    for termine in glossario:
        # Se il termine è nel testo, lo segna con una g a apice
        if re.search(r'\b' + termine + r'\b', text):
            text = re.sub(r'\b' + termine + r'\b', termine + r'\\g', text)

    # Scrive il file
    with open(file, 'w') as f:
        f.write(text)

# Terza parte: controlla per i termini segnati con una g a apice e segnala i
# termini che non sono stati trovati nel glossario
# -------------------------------------------------------------------------
# Ricorsivamente, per ogni file nella directory corrente e nelle sottodirectory
# controlla se il file è un file .tex e se lo è, controlla se ci sono termini
# segnati con una g a apice. Se ci sono, segnala i termini che non sono stati
# trovati nel glossario.

# Funzione che controlla se ci sono termini segnati con una g a apice e segnala
# i termini che non sono stati trovati nel glossario
def check_glossario_g(file, glossario):
    # Apre il file e lo legge
    with open(file, 'r') as f:
        text = f.read()
    # Controlla se ci sono termini segnati con una g a apice
    for termine in extract_words_before_g(text):
        # Se il termine non è nel glossario, lo segnala
        if termine not in glossario:
            print('Il termine ' + termine + ' non è nel glossario')

def extract_words_before_g(string):
    pattern = r'(\w+)\s*\\g'
    matches = re.findall(pattern, string)

    return matches

# Main
# ----

parser = argparse.ArgumentParser(description='Compile LaTeX files.')

parser.add_argument('-o', '--output', help='Destination directory')
parser.add_argument('-s', '--source', help='Source directory')

args = parser.parse_args()

destination_directory = os.path.abspath(args.output)
source_directory = os.path.abspath(args.source)

glossario = get_glossario('glossario.csv')

recursive_apply(source_directory, check_glossario, glossario)
recursive_apply(source_directory, check_glossario_g, glossario)
