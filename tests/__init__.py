"""Test package configuration."""
import os
import sys
from pathlib import Path

# Ensure the ``src`` directory is on ``sys.path`` so the package can be
# imported without installation.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

# Set testing environment for database setup
os.environ["TESTING"] = "True"
