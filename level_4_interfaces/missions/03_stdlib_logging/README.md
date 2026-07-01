# Mission 03: stdlib logging

## Goal

Replace `print()` calls for technical events with a proper logger, so the game can record what happened at different severity levels:

```python
# before
print("Warning: skipped bad monster entry: ...")
print("DEBUG: invalid choice, defaulting to warrior")

# after
logger.warning("Skipped bad monster entry: ...")
logger.debug("Invalid class choice, defaulting to warrior")
```

## You will learn

- `logging.getLogger(__name__)` — the standard way to create a logger
- Log levels: `DEBUG < INFO < WARNING < ERROR < CRITICAL`
- `logging.basicConfig()` and format strings
- `logger.exception()` — logs an error with the full traceback
- The difference between `print()` (user output) and `logging` (technical events)

## Game problem

The starter RPG mixes two very different kinds of output:

- **User output** — what the player needs to see: "You deal 12 damage", "Game saved"
- **Technical events** — what a developer needs: "Bad monster entry skipped", "Load failed"

Both go to `print()`. This means:

- You cannot suppress technical noise without removing player-facing output
- If the game crashes at 2 AM in a simulation, there is no log file — the error is gone
- You cannot filter by severity: info vs warning vs error all look the same

`logging` separates these concerns. The logger handles technical events. User-facing output stays as `print()` (or in Mission 05, Rich).

## Python concept

```python
import logging

# Get a named logger — use __name__ so the log knows which module logged it
logger = logging.getLogger(__name__)

# Configure the root logger once, at startup
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
)

# Log at different levels
logger.debug("Dice roll: %d", dice)          # developer detail
logger.info("Combat started: %s vs %s", ...) # normal event
logger.warning("Bad monster data skipped")   # something unexpected
logger.error("Could not load save file")     # something went wrong
logger.exception("Crash during load")        # error + full traceback
```

**`logger.exception()`** is the most important one for error handling. It logs at ERROR level and automatically attaches the current exception's traceback:

```python
try:
    data = json.loads(text)
except json.JSONDecodeError:
    logger.exception("Failed to parse save file")  # traceback attached automatically
```

## Your task

Open `task.py`. It contains the same game code as the starter with `print()` calls scattered through it. Technical events are already marked with `# REPLACE WITH LOGGING`.

Implement:

1. **`setup_logging(level: str = "INFO") -> None`** — configure the root logger using `basicConfig` with a format that includes time, level, and logger name

2. **Replace each marked `print()`** with the appropriate `logger.debug/info/warning/error/exception()` call. User-facing output (`"Game saved."`, `"You deal 12 damage"`) stays as `print()`.

3. **Call `setup_logging()`** at the start of `main()`

## Run

```bash
uv run python level_4_interfaces/missions/03_stdlib_logging/task.py
```

Run with different levels:

```bash
RPG_LOG_LEVEL=DEBUG uv run python level_4_interfaces/missions/03_stdlib_logging/task.py
```

## Check

```bash
uv run python level_4_interfaces/missions/03_stdlib_logging/check.py
```

## Break it on purpose

Add a deliberate exception in `load_game()`:

```python
raise ValueError("corrupted save")
```

Without `logger.exception()`, the error disappears into a silent `except`. With it, you see the full traceback in the log. That traceback is the difference between a 5-minute debug session and a 5-hour one.

## Fix it

Remove the deliberate exception. The `logger.exception()` call stays — it will only fire if something actually goes wrong.

## Side quest

Use `logging.getLevelName(level_str)` to convert the string `"DEBUG"` or `"WARNING"` to the integer constant. Then pass it as `level=` to `basicConfig`. This lets you control the log level without changing code — just set the environment variable.

## Real-world translation

Every production Python application uses the `logging` module (or a library built on top of it). Django, FastAPI, SQLAlchemy — they all log via `logging.getLogger(__name__)`. When you set up a log handler, you see their output too. This is why module-level loggers use `__name__`: it makes the log show exactly which file produced each line.

## Checklist

- [ ] `setup_logging()` calls `logging.basicConfig()` with a format including time, level, name
- [ ] `logger = logging.getLogger(__name__)` is present at module level
- [ ] All `# REPLACE WITH LOGGING` prints are replaced with logger calls
- [ ] Error-path `except` blocks use `logger.exception()` or `logger.error()`
- [ ] User-facing prints (game messages) remain as `print()`
- [ ] `setup_logging()` is called at the start of `main()`

---

Next mission: `level_4_interfaces/missions/04_log_files/README.md`
