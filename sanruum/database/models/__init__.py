from __future__ import annotations

import importlib
import pkgutil

# Auto-import all modules in the models directory and its subdirectories
for module_info in pkgutil.iter_modules(__path__):
    importlib.import_module(f'{__name__}.{module_info.name}')

# Auto-import subdirectories (like 'health', 'audit', etc.)
for subdir in ['audit', 'consent', 'core', 'health', 'media']:
    try:
        importlib.import_module(f'{__name__}.{subdir}')
    except ModuleNotFoundError:
        pass

__all__ = [name for _, name, _ in pkgutil.iter_modules(__path__)]
