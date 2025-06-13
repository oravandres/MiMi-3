"""Tests package for mimi3."""
import os
import sys
from pathlib import Path

# Set testing environment for database setup
os.environ["TESTING"] = "True"
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
