from __future__ import annotations

import importlib
import pkgutil

# Auto-import all modules in the audit directory
for module_info in pkgutil.iter_modules(__path__):
    importlib.import_module(f'{__name__}.{module_info.name}')

__all__ = [name for _, name, _ in pkgutil.iter_modules(__path__)]
