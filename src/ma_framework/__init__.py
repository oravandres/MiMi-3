"""Compatibility wrapper for legacy imports.

This package re-exports the public API from :mod:`mimi3` so that existing
imports using ``ma_framework`` continue to work.
"""

from mimi3 import *  # noqa: F401,F403
from mimi3 import __version__, models, schemas, database, tools, agents, crud
import sys

# Expose submodules so ``import ma_framework.database`` works
sys.modules[__name__ + ".models"] = models
sys.modules[__name__ + ".schemas"] = schemas
sys.modules[__name__ + ".database"] = database
sys.modules[__name__ + ".tools"] = tools
sys.modules[__name__ + ".agents"] = agents
sys.modules[__name__ + ".crud"] = crud

__all__ = [
    "__version__",
    "models",
    "schemas",
    "database",
    "tools",
    "agents",
]
