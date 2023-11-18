//! # Main
//!
//! This is the main file of the project. It is used to generate the use cases
//! from the `use_cases.csv` file.
//! The use cases are generated in the `use_cases/` folder.
//! The `use_cases.csv` file is a CSV file with the following format:
//!
//! ```csv
//! name, actor, generalization1, generalization2, ...
//! ...
//! ```
//!
//! It may contain blank lines and lines starting with `#` are ignored.
//! The `name` field is the name of the use case, it is used for:
//! - the name of the file
//! - the name of the use case
//! - the name of the label
//!
//! The `actor` field is the name of the main actor of the use case.
//! The `generalization` fields are the names of the generalizations of the use
//! case. They are sub-use cases of the main use case.
//!
//! A use case is a file with the following format:
//! ```tex
//! \usecase{name}
//! \label{usecase:name}
//! \begin{itemize}
//! \item \textbf{Attore principale:} actor
//! \item \textbf{Precondizioni:}
//! \item \textbf{Postcondizioni:}
//! \item \textbf{Scenario principale:}
//! name:
//! \begin{enumerate}
//! \end{enumerate}
//! \item \textbf{Generalizzazioni:}
//! \begin{itemize}
//! \item generalization1 (vedi \autoref{usecase:generalization1})
//! ...
//! \end{itemize}
//! \end{itemize}
//! ```
//!
use std::env;
use std::fs;
use std::io::Write;
use std::path::PathBuf;

fn main() -> Result<(), std::io::Error> {
    let mut dest = "use_cases.csv".to_string();
    let mut target = "use_cases/".to_string();

    let args = env::args().collect::<Vec<_>>();
    let mut args_iter = args[1..].iter();
    while let Some(arg) = args_iter.next() {
        match arg.as_str() {
            "-d" => dest = args_iter.next().unwrap().to_string(),
            "-t" => target = args_iter.next().unwrap().to_string(),
            _ => {
                // help
                println!("Usage: {} [-d destination] [-t target]", args[0]);
                return Ok(());
            }
        }
    }

    // create the destination directory if it doesn't already exist
    if !PathBuf::from(&dest).exists() {
        fs::create_dir(&dest)?;
    }

    let use_cases = fs::read_to_string(target)?;

    let layout_head = "\\usecase{name}
\\label{usecase:name}
\\begin{itemize}
\\item \\textbf{Attore principale:} actor
\\item \\textbf{Precondizioni:}
\\item \\textbf{Postcondizioni:}
\\item \\textbf{Scenario principale:}
\\begin{itemize}
\\item actor:
\\begin{enumerate}
\\item needed
\\end{enumerate}
\\end{itemize}
";
    let layout_bottom = "\\end{itemize}";

    use_cases
        .lines()
        .filter(|line| !line.starts_with('#') || line.is_empty())
        .map(|line| line.split(',').collect::<Vec<_>>())
        .filter(|line| line.len() > 1)
        .map(|data| (data[0].to_string(), data[1].to_string(), data[2..].to_vec()))
        .map(|(name, actor, generizations)| {
            let mut use_case = layout_head.replace("name", &name);
            use_case = use_case.replace("actor", &actor);

            if !generizations.is_empty() {
                use_case += "\\item \\textbf{Generalizzazioni:}\n\\begin{itemize}\n";
            }
            for generization in &generizations {
                use_case += &format!(
                    "\\item {} (vedi \\autoref{{usecase:{}}})\n",
                    generization, generization
                );
            }

            if !generizations.is_empty() {
                use_case += "\\end{itemize}\n";
            }

            use_case += &layout_bottom;
            (name, use_case)
        })
        .for_each(|(name, use_case)| {
            let mut file = fs::File::create(format!("{}/{}.tex", dest, name)).unwrap();
            file.write_all(use_case.as_bytes()).unwrap();
        });

    Ok(())
}
