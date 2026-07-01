"""
Boss Fight: Installable CLI Tool

Wire everything from Missions 01-06 into one installable CLI tool.

Run commands:
    uv run python task.py --help
    uv run python task.py new-game --name Ada --class warrior
    uv run python task.py simulate --battles 5
    uv run python task.py status
    uv run python task.py report

After registering in pyproject.toml [project.scripts]:
    uv sync
    uv run rpg --help
"""

import sys
from pathlib import Path

# Add parent dirs to path for the package import
sys.path.insert(0, str(Path(__file__).parent))

from rpg.cli import app  # noqa: E402

if __name__ == "__main__":
    app()
