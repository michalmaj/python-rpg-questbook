# level_6_api/missions/06_api_errors_and_status_codes/task/config.py
"""Shared paths — import DATA_DIR in router files."""
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
