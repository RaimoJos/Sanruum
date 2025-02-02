import argparse
import os
import sys
from pathlib import Path

from sanruum.constants import BASE_DIR

try:
    import pathspec
except ImportError:
    print("The 'pathspec' library is required for this script to run.")
    print("Please install it using 'pip install pathspec'")
    sys.exit(1)

try:
    from colorama import Fore, Style, init
except ImportError:
    print("The 'colorama' library is required for colored output.")
    print("Please install it using 'pip install colorama'")
    sys.exit(1)

# Initialize colorama
init(autoreset=True)

# Define default exclusion patterns
DEFAULT_IGNORE_PATTERNS = [
    # Exclude Git metadata
    '.git/',
    # Exclude Python cache directories and compiled files
    '__pycache__/',
    '*.pyc',
    # Exclude virtual environments
    'venv/',
    'env/',
    '.venv/',
    # Exclude Node.js modules
    'node_modules/',
    # Exclude IDE and editor directories
    '.vscode/',
    '.idea/',
    # Exclude OS-specific files
    '.DS_Store',
    'Thumbs.db',
    # Exclude logs and temporary files
    'logs/',
    '*.log',
    'tmp/',
    'temp/',
    # Exclude specific files
    'secret_config.yaml',
]


def load_ignore_patterns(ignore_files, default_patterns):
    """
    Load ignore patterns from default patterns and a list of ignore files.

    :param ignore_files: List of Path objects to ignore files.
    :param default_patterns: List of default exclusion patterns.
    :return: Compiled PathSpec object or None if no patterns are loaded.
    """
    patterns = set(default_patterns)

    for ignore_file in ignore_files:
        if ignore_file.exists():
            with ignore_file.open('r') as f:
                file_patterns = f.read().splitlines()
                # Remove empty lines and comments
                file_patterns = [line.strip() for line in file_patterns if
                                 line.strip() and not line.strip().startswith('#')]
                patterns.update(file_patterns)
            print(f"Loaded exclusion patterns from '{ignore_file}'.")
        else:
            print(f"Ignore file '{ignore_file}' not found. Skipping.")

    if patterns:
        spec = pathspec.PathSpec.from_lines('gitwildmatch', patterns)
        return spec
    return None


def should_ignore(path, spec, initial_root_dir):
    """
    Determine if a given path should be ignored based on the PathSpec.

    :param path: Path to check.
    :param spec: Compiled PathSpec object.
    :param initial_root_dir: Initial root directory for relative paths.
    :return: True if the path should be ignored, False otherwise.
    """
    if spec is None:
        return False

    # Compute the relative path from the initial root directory
    try:
        rel_path = os.path.relpath(path, initial_root_dir)
    except ValueError:
        # If path is on a different drive (Windows), relpath raises ValueError
        return False

    # pathspec expects POSIX-style paths
    rel_path_posix = rel_path.replace(os.sep, '/')
    return spec.match_file(rel_path_posix)


def generate_tree(current_dir, prefix, spec, visited, initial_root_dir, use_color, tree_lines):
    """
    Recursively generates and stores the directory tree structure.

    :param tree_lines: List to store tree structure.
    """
    if visited is None:
        visited = set()

    real_path = os.path.realpath(current_dir)
    if real_path in visited:
        tree_lines.append(prefix + "└── " + f"{os.path.basename(current_dir)}/ (symlink loop)")
        return
    visited.add(real_path)

    try:
        items = sorted(os.listdir(current_dir))
    except PermissionError:
        tree_lines.append(prefix + "└── " + "Permission Denied")
        return

    for index, item in enumerate(items):
        path = os.path.join(current_dir, item)

        if should_ignore(path, spec, initial_root_dir):
            continue

        connector = "├── " if index < len(items) - 1 else "└── "
        new_prefix = prefix + ("    " if index == len(items) - 1 else "│   ")

        if os.path.islink(path):
            try:
                target_path = os.readlink(path)
            except OSError:
                target_path = "unreachable"
            tree_lines.append(prefix + connector + f"{item}@ -> {target_path}")
            continue

        if os.path.isdir(path):
            tree_lines.append(prefix + connector + f"{item}/")
            generate_tree(path, new_prefix, spec, visited, initial_root_dir, use_color, tree_lines)
        else:
            tree_lines.append(prefix + connector + f"{item}")


def update_readme(tree_structure):
    """
    Updates the README.md file with the generated tree structure.
    """
    readme_path = os.path.join(BASE_DIR, "README.md")
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        content = ""

    # Define tree section markers
    start_marker = "<!-- START_TREE -->"
    end_marker = "<!-- END_TREE -->"

    tree_section = f"{start_marker}\n```\n{tree_structure}\n```\n{end_marker}"

    if start_marker in content and end_marker in content:
        # Replace existing tree section
        content = content.split(start_marker)[0] + tree_section + content.split(end_marker)[1]
    else:
        # Append the tree section if not found
        content += f"\n## Project Structure\n{tree_section}\n"

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("README.md updated with the directory tree.")


def main():
    parser = argparse.ArgumentParser(description="Generate a directory tree and update README.md.")
    parser.add_argument("directory", nargs="?", default=".", help="Root directory (default: current directory)")
    args = parser.parse_args()

    root_dir = BASE_DIR
    if not os.path.exists(root_dir):
        print(f"Error: Directory '{root_dir}' does not exist.")
        sys.exit(1)

    ignore_files = [Path(root_dir) / ".treeignore", Path(root_dir) / ".gitignore"]
    spec = load_ignore_patterns(ignore_files, DEFAULT_IGNORE_PATTERNS)

    tree_lines = [os.path.basename(root_dir) + "/"]
    generate_tree(root_dir, "", spec, visited=None, initial_root_dir=root_dir, use_color=False, tree_lines=tree_lines)

    tree_structure = "\n".join(tree_lines)

    update_readme(tree_structure)

    print(tree_structure)  # Print to console


if __name__ == "__main__":
    main()
