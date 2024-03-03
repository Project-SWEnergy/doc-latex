import os
import subprocess
import re
import argparse

to_delete = [
    "main.aux",
    "main.log",
    "main.out",
    "main.synctex.gz",
    "main.fdb_latexmk",
    "main.fls",
    "main.toc",
]


def get_version(path):
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    for d in dirs:
        files = os.listdir(os.path.join(path, d))
        if "registro_modifiche.tex" in files:
            with open(os.path.join(path, d, "registro_modifiche.tex")) as f:
                # Define a regular expression pattern to match version numbers
                version_pattern = r"\d+\.\d+\.\d+"

                # Find all matches of version numbers in the text
                versions = re.findall(version_pattern, f.read())

                if versions:
                    # The latest version is the first match in the list
                    latest_version = versions[0]
                    return (True, ("v" + latest_version))
    return (False, "v0")  # No version found in the text


def convert_file(source_directory, destination_directory, to_delete):
    # Define the name of the LaTeX file to be compiled
    # there needs to be for how get_dir works
    latex_file = "main.tex"
    os.chdir(source_directory)
    print("Compiling ", os.path.basename(destination_directory), "...")

    try:
        # Run pdflatex to compile the LaTeX file into a PDF and specify the output directory
        subprocess.check_call(
            [
                "pdflatex",
                latex_file,
            ],
        )

        subprocess.check_call(
            [
                "pdflatex",
                latex_file,
            ],
        )

        subprocess.check_call(
            [
                "pdflatex",
                latex_file,
            ],
        )
        # Delete intermediate files except for the PDF file
        intermediate_files = [file for file in os.listdir("./") if file in to_delete]
        for intermediate_file in intermediate_files:
            os.remove(intermediate_file)

        # Rename the PDF file to include the version number, if applicable
        # Move the PDF file to the destination directory
        isVersioned, version = get_version(source_directory)
        if isVersioned:
            destination_directory = destination_directory.replace(".pdf", f"-{version}.pdf")

        os.rename(latex_file.replace(".tex", ".pdf"), destination_directory)
        print("Compiled ", os.path.basename(destination_directory), " successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling {latex_file}: {e}")


# Get a list of all directories in the specified path which contain the main.tex file
def get_src_dir(path):
    # list all the files (and directories) in the specified path
    dirs = os.listdir(path)

    # if the main.tex file is in the specified path, return the path
    if "main.tex" in dirs:
        return [path]

    # add path to each directory
    dirs = [os.path.join(path, d) for d in dirs if os.path.isdir(os.path.join(path, d))]

    return [src_dir for d in dirs for src_dir in get_src_dir(d)]

## MAIN ##

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Compile LaTeX files.')

# Add the arguments you want to parse
parser.add_argument('-o', '--output', help='Destination directory')
parser.add_argument('-s', '--source', help='Source directory')

# Parse the arguments
args = parser.parse_args()

# Access the values using the specified flags
destination_directory = os.path.abspath(args.output)
source_directory = os.path.abspath(args.source)

# Check if the arguments were provided
if destination_directory is None or source_directory is None:
    print("Please provide both destination and source directories using -o and -s flags.")
    exit()


# src: folder in which is located the main.tex file
for src_dir in get_src_dir(source_directory):
    print("src_dir: ", src_dir)
    # file name without extension and without path
    destination_path = src_dir.replace(source_directory, "")

    # add path to destination directory and extension
    destination_path = destination_directory + destination_path + ".pdf"

    # create directory if it doesn't exist (all parent directories will be
    # created, if necessary)
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    convert_file(src_dir, destination_path, to_delete)


print("Compilation complete.")
