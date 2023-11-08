import os
import subprocess
import re


# Define the source (target) directory where your LaTeX files are located
source_directory = input("Enter the source directory: ")
source_directory = os.path.abspath(source_directory)

# Define the destination directory for the generated PDF files
destination_directory = input("Enter the destination directory: ")
destination_directory = os.path.abspath(destination_directory)

print("Source directory: ", source_directory)
print("Destination directory: ", destination_directory)

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
            stdout=subprocess.DEVNULL,  # no output in the terminal
            stderr=subprocess.DEVNULL,  # no output in the terminal
        )

        # Delete intermediate files except for the PDF file
        intermediate_files = [file for file in os.listdir("./") if file in to_delete]
        for intermediate_file in intermediate_files:
            os.remove(intermediate_file)

        # Rename the PDF file to include the version number, if applicable
        # Move the PDF file to the destination directory
        isVersioned, version = get_version(source_directory)
        if isVersioned:
            os.rename(
                latex_file.replace(".tex", ".pdf"),
                destination_directory.replace(".pdf", f"-{version}.pdf"),
            )
        else:
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

    # recurse to each directory in the specified path
    for d in dirs:
        dirs.remove(d)
        dirs.extend(get_src_dir(d))

    # return the list of directories which contain the main.tex file
    return dirs


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
