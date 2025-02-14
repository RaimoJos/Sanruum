from __future__ import annotations

import ast
import os

from sanruum.constants import BASE_DIR

DEFAULT_STATUS = '🔄 in_progress'


def extract_functions_and_classes() -> dict[str, tuple[str, str, str, str | None, str]]:
    """Scan BASE_DIR for all functions and class methods and categorize them."""
    functions = {}

    for root, _, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith('.py') and not file.endswith('_test.py'):
                abs_path = os.path.abspath(os.path.join(root, file))
                module_path = os.path.relpath(abs_path, BASE_DIR).replace('\\', '/')
                module_name = module_path.replace('/', '.').replace('.py', '')

                with (open(abs_path, encoding='utf-8') as f):
                    content = f.read()
                    if file == '__init__.py' and content.strip(
                    ) == 'from __future__ import annotations':
                        continue
                    tree = ast.parse(content, filename=file)

                # Create a URL-friendly absolute path for the link
                url_path = abs_path.replace(' ', '%20').replace(os.sep, '/')
                if isinstance(url_path, bytes):
                    url_path = url_path.decode('utf-8')

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_link = \
                            f'[`{node.name}`](file:///{url_path}#L{node.lineno})'
                        functions[node.name] = (
                            module_name, 'Function', func_link,
                            ast.get_docstring(node) or None,
                            DEFAULT_STATUS,
                        )
                    elif isinstance(node, ast.ClassDef):
                        for method in node.body:
                            if isinstance(method, ast.FunctionDef):
                                method_link = \
                                    (
                                        f'[`{method.name}'
                                        f'`](file:///{url_path}#L{method.lineno})'
                                    )
                                functions[method.name] = (
                                    f'{module_name}.{node.name}', 'Method', method_link,
                                    ast.get_docstring(method) or None,
                                    DEFAULT_STATUS,
                                )

    return functions
