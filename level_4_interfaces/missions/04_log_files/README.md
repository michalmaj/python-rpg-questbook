# Mission 04: Log Files

## Goal

Add file handlers to the logger so events are written to persistent log files — even after the process exits:

```
logs/
├── app.log      ← all events INFO and above
└── combat.log   ← combat events only (INFO and above, from the combat logger)
```

## You will learn

- `logging.FileHandler` — write log records to a file
- Multiple handlers on one logger — console and file can coexist
- Logger hierarchy — child loggers inherit from parent loggers
- How to route different events to different files

## Game problem

After Mission 03 the logger writes to the console. That is useful while the game is running, but once the process exits, those log lines are gone. If a simulation runs overnight and crashes, there is no record.

A `FileHandler` writes the same records to a file that persists between runs. You can come back the next day and read what happened.

## Python concept

```python
import logging
from pathlib import Path

def add_file_handler(
    logger: logging.Logger,
    path: Path,
    level: int = logging.INFO,
    fmt: str = "%(asctime)s %(levelname)-8s %(name)s: %(message)s",
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(path, encoding="utf-8")
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
```

**Logger hierarchy** — loggers are organised as a tree by `.`-separated names:

```
root
└── task04              (logging.getLogger("task04") or __name__)
    └── task04.combat   (logging.getLogger("task04.combat"))
```

A child logger propagates records up to its parent. If you add a `FileHandler` to the root logger, all child loggers write to that file too. If you add it to only `task04.combat`, only combat events reach that file.

```python
# app.log gets everything from the root down
add_file_handler(logging.getLogger(), LOG_DIR / "app.log")

# combat.log gets only records from "task04.combat" and its children
add_file_handler(logging.getLogger(__name__ + ".combat"), LOG_DIR / "combat.log")
```

## Your task

Open `task.py`. `setup_logging()` from M03 is already implemented.

Implement:

1. **`add_file_handler(logger, path, level, fmt) -> None`** — create a `FileHandler`, set its level and formatter, add it to the logger. Create parent directories if needed.

2. **`setup_log_files(log_dir) -> None`** — call `add_file_handler` twice:
   - `app.log` on the **root logger** at `INFO` level (captures everything)
   - `combat.log` on `logging.getLogger(__name__ + ".combat")` at `DEBUG` level (combat detail only)

3. **Use `combat_logger` in combat functions** — the combat functions already have `# USE combat_logger` markers. Replace them with `combat_logger.debug(...)` or `combat_logger.info(...)`.

## Run

```bash
uv run python level_4_interfaces/missions/04_log_files/task.py
```

Then inspect the log files:

```bash
cat level_4_interfaces/missions/04_log_files/logs/app.log
cat level_4_interfaces/missions/04_log_files/logs/combat.log
```

## Check

```bash
uv run python level_4_interfaces/missions/04_log_files/check.py
```

## Break it on purpose

Delete `logs/app.log` while the game is running. Nothing crashes — `FileHandler` keeps the file open. The log continues writing.

Now comment out `log_dir.mkdir(parents=True, exist_ok=True)` in `add_file_handler`. Run the game. You get a `FileNotFoundError`. That is why `mkdir` is needed before `FileHandler`.

## Fix it

Uncomment `mkdir`. The directory is created automatically.

## Side quest

Replace `FileHandler` with `RotatingFileHandler` from `logging.handlers`:

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    path,
    maxBytes=1_000_000,   # 1 MB per file
    backupCount=3,         # keep 3 old files: app.log.1, app.log.2, app.log.3
    encoding="utf-8",
)
```

This prevents log files from growing indefinitely. A long simulation session will rotate the file automatically.

## Real-world translation

Every production service logs to files. In containers the logs go to stdout and a sidecar collects them; in bare-metal services they go directly to disk. The `FileHandler` pattern is the same in both cases. `RotatingFileHandler` is what keeps servers from filling their disks overnight.

## Checklist

- [ ] `add_file_handler()` creates the file's parent directory if needed
- [ ] `add_file_handler()` sets level and formatter on the handler
- [ ] `setup_log_files()` adds `app.log` to the root logger
- [ ] `setup_log_files()` adds `combat.log` to the combat logger
- [ ] After a run, both log files exist and contain records
- [ ] `combat.log` contains only combat events, not startup/load messages

---

Next mission: `level_4_interfaces/missions/05_rich_terminal_output/README.md`
