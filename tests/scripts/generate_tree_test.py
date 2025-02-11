from __future__ import annotations

import os
import tempfile
from pathlib import Path

from scripts.generate_tree import generate_tree
from scripts.generate_tree import load_ignore_patterns
from scripts.generate_tree import should_ignore


def test_generate_tree() -> None:
    """Test the directory tree generation function."""
    with tempfile.TemporaryDirectory() as temp_dir:
        os.makedirs(os.path.join(temp_dir, 'folder/subfolder'))
        with open(os.path.join(temp_dir, 'folder/file.txt'), 'w') as f:
            f.write('test')

        tree_lines = [os.path.basename(temp_dir) + '/']
        generate_tree(temp_dir, '', None, None, temp_dir, tree_lines)

        assert 'folder/' in tree_lines
        assert 'folder/file.txt' in tree_lines


def test_load_ignore_patterns() -> None:
    """Test loading ignore patterns from a file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        ignore_file = Path(temp_dir) / '.treeignore'
        ignore_file.write_text('ignored_folder/\n*.log')

        spec = load_ignore_patterns([ignore_file], [])
        assert spec is not None
        assert spec.match_file('ignored_folder/')
        assert spec.match_file('logs/error.log')


def test_should_ignore() -> None:
    """Test whether paths are correctly ignored based on patterns."""
    spec = load_ignore_patterns([], ['ignored_dir/', '*.log'])
    assert should_ignore('ignored_dir/file.txt', spec, '/')
    assert should_ignore('logs/error.log', spec, '/')
    assert not should_ignore('valid_folder/file.txt', spec, '/')
