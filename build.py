import os
import subprocess

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


def convert_file(source_directory, destination_directory, to_delete):
    # List all LaTeX files in the source directory
    print("Compiling in ", source_directory, "...")
    latex_files = [
        file for file in os.listdir(source_directory) if file.endswith(".tex")
    ]

    current_working_directory = os.getcwd()
    os.chdir(source_directory)

    for latex_file in latex_files:
        latex_file_path = os.path.join(latex_file)

        try:
            # Run pdflatex to compile the LaTeX file into a PDF and specify the output directory
            subprocess.check_call(
                [
                    "pdflatex",
                    latex_file_path,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            # Delete intermediate files except for the PDF file
            intermediate_files = [
                file for file in os.listdir("./") if file in to_delete
            ]
            for intermediate_file in intermediate_files:
                intermediate_file_path = os.path.join(
                    source_directory, intermediate_file
                )
                os.remove(intermediate_file_path)

            # Move the PDF file to the destination directory
            pdf_file = latex_file.replace(".tex", ".pdf")
            destination_file_path = os.path.join(
                destination_directory, os.path.basename(source_directory + ".pdf")
            )
            os.rename(pdf_file, destination_file_path)

            print("Compiled ", latex_file, " successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error compiling {latex_file}: {e}")
    os.chdir(current_working_directory)


# Get a list of all directories in the specified path
# directories = [
#    d
#    for d in os.listdir(source_directory)
#    if os.path.isdir(os.path.join(source_directory, d))
# ]
def get_dir(path):
    dirs = os.listdir(path)
    for d in dirs:
        if ".tex" in d:
            return [path]
    dirs = [os.path.join(path, d) for d in dirs]
    for d in dirs:
        dirs.remove(d)
        dirs.extend(get_dir(d))
    return dirs


for directory in get_dir(source_directory):
    destination_path = directory.replace(source_directory, "")
    destination_path = os.path.dirname(destination_path)
    destination_path = destination_directory + destination_path
    os.makedirs(destination_path, exist_ok=True)
    convert_file(directory, destination_path, to_delete)


print("Compilation complete.")
