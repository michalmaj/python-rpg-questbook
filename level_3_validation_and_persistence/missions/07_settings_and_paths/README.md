# Mission 07: Settings and Paths

## Goal

Replace scattered hardcoded path strings with a single `GameSettings` object, validated by Pydantic, optionally overridable via environment variables.

## You will learn

- `pydantic-settings` and `BaseSettings` for config that reads from env vars and `.env` files
- `env_prefix` to namespace your variables (`RPG_DATA_DIR`)
- `Path` as a field type in Pydantic
- The "single source of truth" principle for configuration
- A simple caching pattern for settings (`get_settings()`)

## Game problem

The starter RPG defines paths like this in every file:

```python
DATA_DIR = "level_3_validation_and_persistence/starter_raw_rpg/data"
SAVES_DIR = "level_3_validation_and_persistence/starter_raw_rpg/saves"
LOG_PATH  = "..."
```

Problems:

- These are strings — no type safety, no validation that the path is even a valid `Path`
- Each module defines its own paths — no single source of truth
- Running the game from a different working directory breaks everything
- To run tests with a temp directory you must monkey-patch these module-level variables
- Deploying to a different machine requires editing source code

The fix: one `GameSettings` object that all modules import.

## Python concept

**`pydantic-settings`** extends Pydantic with automatic loading from environment variables and `.env` files:

```python
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class GameSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="RPG_",    # env var name is RPG_<FIELD_NAME>
        env_file=".env",      # also load from .env if it exists
    )

    data_dir:    Path = Path("data")
    saves_dir:   Path = Path("saves")
    max_potions: int  = 5
```

Now you can override `saves_dir` by setting the environment variable `RPG_SAVES_DIR`:

```bash
RPG_SAVES_DIR=/tmp/test_saves uv run python task.py
```

Or in a `.env` file:

```
RPG_SAVES_DIR=/tmp/test_saves
```

**`get_settings()` caching pattern:**

```python
_settings: GameSettings | None = None

def get_settings() -> GameSettings:
    global _settings
    if _settings is None:
        _settings = GameSettings()
    return _settings
```

All modules call `get_settings()` — the settings object is created once and shared.

## Your task

Open `task.py`.

1. **Define `GameSettings`** with fields: `data_dir`, `saves_dir`, `log_file`, `max_potions`. Add `model_config` with `env_prefix="RPG_"`.

3. **Define `get_settings() -> GameSettings`** with module-level caching.

4. Uncomment the lines in `main()` and run.

## Run

```bash
uv run python level_3_validation_and_persistence/missions/07_settings_and_paths/task.py
```

Override a value:

```bash
RPG_SAVES_DIR=/tmp/my_saves uv run python level_3_validation_and_persistence/missions/07_settings_and_paths/task.py
```

## Check

```bash
uv run python level_3_validation_and_persistence/missions/07_settings_and_paths/check.py
```

## Break it on purpose

Set `RPG_MAX_POTIONS=abc` and run. Pydantic should raise a `ValidationError` because `abc` cannot be coerced to `int`.

## Fix it

Use a valid integer: `RPG_MAX_POTIONS=3`.

## Side quest

Add a `debug: bool = False` field to `GameSettings`. When `RPG_DEBUG=true` is set, `GameSettings().debug` should be `True`. Use it to print extra output in `run_combat()`.

## Real-world translation

FastAPI apps use `BaseSettings` for database URLs, secret keys, and environment names. The 12-factor app methodology (https://12factor.net) says config should come from environment variables, not source code. `pydantic-settings` is the standard Python implementation of this.

## Checklist

- [ ] I defined `GameSettings` with `Path` fields and a `max_potions: int`
- [ ] I implemented `get_settings()` with module-level caching
- [ ] I understand that `env_prefix="RPG_"` maps `data_dir` to `RPG_DATA_DIR`
- [ ] I know what a `.env` file is and how `env_file=".env"` loads it
- [ ] I can explain: why is one central settings object better than per-file path constants?

---

**Level complete!** Next: `level_3_validation_and_persistence/projects/01_sqlite_repository_backend/README.md`
