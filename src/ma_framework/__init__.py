"""Compatibility wrapper for the legacy ``ma_framework`` import path."""
from __future__ import annotations
import sys
import mimi3

# Re-export the public API of mimi3
from mimi3 import *  # noqa: F401,F403

# Register submodules under this package name for backwards compatibility
sys.modules[__name__ + ".models"] = mimi3.models
sys.modules[__name__ + ".schemas"] = mimi3.schemas
sys.modules[__name__ + ".database"] = mimi3.database
sys.modules[__name__ + ".tools"] = mimi3.tools
sys.modules[__name__ + ".agents"] = mimi3.agents
sys.modules[__name__ + ".crud"] = mimi3.crud
