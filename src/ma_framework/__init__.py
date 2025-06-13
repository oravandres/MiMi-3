"""Compatibility wrapper for Mimi-3 under the legacy 'ma_framework' name."""
import sys
import importlib

# Import core package
import mimi3 as _mimi3

# Re-export public API from mimi3
from mimi3 import *
from mimi3 import __all__ as _mimi_all
__all__ = list(_mimi_all)

# Additional submodules expected under the old name
for _name in ("crud",):
    module = importlib.import_module(f"mimi3.{_name}")
    globals()[_name] = module
    __all__.append(_name)
    sys.modules[f"{__name__}.{_name}"] = module

# Register existing submodules from mimi3
for _name in _mimi_all:
    module = getattr(_mimi3, _name, None)
    if module is not None:
        sys.modules[f"{__name__}.{_name}"] = module
