# Logging configuration — setup_logging, add_file_handler, setup_log_files.
# Port from M03 + M04.

import logging
from pathlib import Path

DEFAULT_FMT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"


def setup_logging(level: str = "INFO") -> None:
    """Configure the root logger with a StreamHandler."""
    # TODO: logging.basicConfig(level=..., format=DEFAULT_FMT)
    raise NotImplementedError


def add_file_handler(
    target_logger: logging.Logger,
    path: Path,
    level: int = logging.INFO,
    fmt: str = DEFAULT_FMT,
) -> None:
    """Add a FileHandler to target_logger that writes to path."""
    # TODO:
    # 1. path.parent.mkdir(parents=True, exist_ok=True)
    # 2. handler = logging.FileHandler(path, encoding="utf-8")
    # 3. handler.setLevel(level); handler.setFormatter(logging.Formatter(fmt))
    # 4. target_logger.addHandler(handler)
    raise NotImplementedError


def setup_log_files(log_dir: Path) -> None:
    """Add file handlers: app.log on root logger, combat.log on combat logger."""
    # TODO:
    # add_file_handler(logging.getLogger(), log_dir / "app.log", logging.INFO)
    # add_file_handler(logging.getLogger("rpg.combat"), log_dir / "combat.log", logging.DEBUG)
    raise NotImplementedError
