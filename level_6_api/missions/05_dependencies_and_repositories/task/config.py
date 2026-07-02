# level_6_api/missions/05_dependencies_and_repositories/task/config.py
"""Shared paths — import DATA_DIR in router files."""
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
