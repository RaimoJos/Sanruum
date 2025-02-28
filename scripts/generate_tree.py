from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from sanruum.config import BaseConfig

BASE_DIR = BaseConfig.BASE_DIR

try:
    import pathspec
except ImportError:
    print("The 'pathspec' library is required for this script to run.")
    print("Please install it using 'pip install pathspec'")
    sys.exit(1)

try:
    from colorama import init
except ImportError:
    print("The 'colorama' library is required for colored output.")
    print("Please install it using 'pip install colorama'")
    sys.exit(1)

# Initialize colorama for automatic resetting
init(autoreset=True)

# Define default exclusion patterns
DEFAULT_IGNORE_PATTERNS = [
    '.git/',
    '__pycache__/',
    '*.pyc',
    'venv/',
    'env/',
    '.venv/',
    'node_modules/',
    '.vscode/',
    '.idea/',
    '.DS_Store',
    'Thumbs.db',
    'logs/',
    '*.log',
    'tmp/',
    'temp/',
    'secret_config.yaml',
]


def load_ignore_patterns(
        ignore_files: list[Path], default_patterns: list[str],
) -> pathspec.PathSpec | None:
    """
    Load ignore patterns from default patterns and a list of ignore files.
    """
    patterns = set(default_patterns)
    for ignore_file in ignore_files:
        if ignore_file.exists():
            with ignore_file.open('r') as f:
                file_patterns = [
                    line.strip()
                    for line in f.read().splitlines()
                    if line.strip() and not line.startswith('#')
                ]
                patterns.update(file_patterns)
            print(f"Loaded exclusion patterns from '{ignore_file}'.")
    return pathspec.PathSpec.from_lines('gitwildmatch', patterns) if patterns else None


def should_ignore(
        path: str, spec: pathspec.PathSpec | None, initial_root_dir: str,
) -> bool:
    """Determine if a given path should be ignored based on the PathSpec."""
    if spec is None:
        return False
    rel_path = os.path.relpath(path, initial_root_dir).replace(os.sep, '/')
    return bool(spec.match_file(rel_path))


def generate_tree(
        current_dir: str,
        prefix: str,
        spec: pathspec.PathSpec | None,
        visited: set[str] | None,
        initial_root_dir: str,
        tree_lines: list[str],
) -> None:
    """Recursively generates and stores the directory tree structure."""
    if visited is None:
        visited = set()
    real_path = os.path.realpath(current_dir)
    if real_path in visited:
        tree_lines.append(
            prefix + '└── '
            + os.path.basename(current_dir) + '/ (symlink loop)',
        )
        return
    visited.add(real_path)
    try:
        items = sorted(os.listdir(current_dir))
    except PermissionError:
        tree_lines.append(prefix + '└── Permission Denied')
        return
    for index, item in enumerate(items):
        path = os.path.join(current_dir, item)
        if should_ignore(path, spec, initial_root_dir):
            continue
        connector = '├── ' if index < len(items) - 1 else '└── '
        new_prefix = prefix + ('│   ' if index < len(items) - 1 else '    ')
        if os.path.isdir(path):
            tree_lines.append(prefix + connector + item + '/')
            generate_tree(path, new_prefix, spec, visited, initial_root_dir, tree_lines)
        else:
            tree_lines.append(prefix + connector + item)


def update_readme(tree_structure: str) -> None:
    """Updates the README.md file with the generated tree structure."""
    stats_path = os.path.join(BASE_DIR, 'STATS.md')
    start_marker, end_marker = '<!-- START_TREE -->', '<!-- END_TREE -->'
    tree_section = f'{start_marker}\n```\n{tree_structure}\n```\n{end_marker}'

    try:
        with open(stats_path, encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        content = ''

    if start_marker in content and end_marker in content:
        content = content.split(start_marker)[0] + \
            tree_section + content.split(end_marker)[1]
    else:
        content += f'\n## Project Structure\n{tree_section}\n'

    # Handle file write errors
    try:
        with open(stats_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('README.md updated with the directory tree.')
    except OSError as e:
        print(f'Error writing to README.md: {e}')


def main() -> None:
    """Main function to generate the directory tree and update README.md."""
    parser = argparse.ArgumentParser(
        description='Generate a directory tree and update README.md.',
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default=BASE_DIR,  # Ensure it starts from project root
        help='Root directory (default: project root)',
    )
    args = parser.parse_args()
    root_dir = os.path.abspath(args.directory)
    if not os.path.exists(root_dir):
        print(f"Error: Directory '{root_dir}' does not exist.")
        sys.exit(1)
    ignore_files = [Path(root_dir) / '.treeignore', Path(root_dir) / '.gitignore']
    spec = load_ignore_patterns(ignore_files, DEFAULT_IGNORE_PATTERNS)
    tree_lines = [os.path.basename(root_dir) + '/']
    generate_tree(root_dir, '', spec, None, root_dir, tree_lines)
    tree_structure = '\n'.join(tree_lines)
    update_readme(tree_structure)
    print(tree_structure)


if __name__ == '__main__':
    main()
