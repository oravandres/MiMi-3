"""Multi-Agent / Multi-Model Framework.

A minimal, opinionated framework for building software-engineering agents.
"""

__version__ = "0.1.0"

from . import models
from . import schemas
from . import database
from . import crud
from . import tools
from . import agents

__all__ = ["models", "schemas", "database", "crud", "tools", "agents"]
