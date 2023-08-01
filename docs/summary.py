import os


##
# creating lazy docs lazydocs --overview-file="mar_python.md" --src-base-url="https://github.com/Schwarzam/MAR/blob/master" --output-path="docs/mar_python"  mar/mar


# Define the directory you want to scan for Markdown files
docs_dir = "./mar_python"

# Define the name of the summary file
summary_filename = "SUMMARY.md"

def generate_summary(dir_path, f, depth=0):
    # Find all markdown files in the directory, sort them alphabetically
    md_files = sorted([entry for entry in os.listdir(dir_path) if entry.endswith(".md") and entry != summary_filename])

    for md_file in md_files:
        # Write the relative link to the file, with indentation based on the depth
        f.write(f"{'  ' * depth}- [{os.path.splitext(md_file)[0]}]({os.path.join(dir_path, md_file).replace('./', '')})\n")

    # Find all directories in the directory, sort them alphabetically
    directories = sorted([entry for entry in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, entry))])

    for directory in directories:
        # Write the directory name as a header, with indentation based on the depth
        f.write(f"{'  ' * depth}- {directory}\n")

        # Recursively generate the summary for the subdirectory
        generate_summary(os.path.join(dir_path, directory), f, depth + 1)

# Create a summary file with a tree-like structure linking to each markdown file
with open(summary_filename, 'w') as f:
    f.write("# Summary\n")
    generate_summary(docs_dir, f)
