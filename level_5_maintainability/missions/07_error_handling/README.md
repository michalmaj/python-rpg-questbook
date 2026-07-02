# Mission 07: Error Handling

## Goal

Replace silent `except Exception: pass` patterns with a custom exception hierarchy (`RPGError` → `SaveFileError`, `MonsterLoadError`, `CombatError`) that tells callers *what* went wrong and *why*.

---

## Game Problem

Open `task.py` and look at `load_monsters()`:

```python
def load_monsters() -> list[Monster]:
    try:
        with open(DATA_DIR / "monsters.json") as f:
            raw = json.load(f)
        ...
    except Exception:
        return []   # silent: FileNotFoundError? JSONDecodeError? caller can't tell
```

The function returns an empty list on *every* error. The `simulate` command then prints:

```
No monsters found in data/.
```

Was the file missing? Corrupt? Permission denied? The player and the developer both have no idea. A silent `return []` is technically correct — it runs without crashing — but it is a debugging nightmare. The same pattern in `load_hero()` hides whether a save file is corrupt or simply absent. In `save_hero()` a raw `OSError` message leaks internal paths to the user.

Custom exceptions fix all three: they carry a human-readable message, preserve the original cause via exception chaining, and let callers catch *exactly* the error they can handle.

---

## Python Concept

### Custom exception hierarchy

```python
class RPGError(Exception):
    """Base class for all game errors."""

class MonsterLoadError(RPGError):
    """Raised when monsters.json is missing, corrupt, or contains invalid data."""

class SaveFileError(RPGError):
    """Raised when the save file cannot be read or written."""
```

Inherit from a shared base (`RPGError`) so callers can catch all game errors with one clause, or catch specific ones when needed:

```python
try:
    monsters = load_monsters()
except MonsterLoadError as e:
    console.print(f"[red]Could not load monsters: {e}[/red]")
    raise typer.Exit(1)
```

### Exception chaining — `raise X from e`

```python
try:
    raw = json.load(f)
except json.JSONDecodeError as e:
    raise MonsterLoadError("monsters.json is not valid JSON") from e
```

`from e` sets `__cause__` on the new exception. When Python prints the traceback, it shows:

```
json.decoder.JSONDecodeError: ...
The above exception was the direct cause of the following exception:
MonsterLoadError: monsters.json is not valid JSON
```

The original context is preserved for debugging, but the caller sees a clean, domain-specific message.

### `__cause__` vs `__context__`

| Attribute | Set by | Meaning |
|---|---|---|
| `__cause__` | `raise X from e` | You explicitly declared the cause |
| `__context__` | implicit (any `raise` inside an `except`) | Python attached it automatically |

Use `raise X from e` when the link is intentional. Use `raise X from None` when you *want* to suppress the original traceback entirely (see Side Quest below).

### "Catch what you can handle"

A good rule: catch an exception only at the layer that knows how to respond to it.

- `load_monsters()` knows about `FileNotFoundError` and `json.JSONDecodeError` — it converts them to `MonsterLoadError`.
- `simulate()` knows that a `MonsterLoadError` means "tell the user and exit" — it catches `MonsterLoadError` and prints a friendly message.
- Neither layer swallows the error silently.

---

## Code Example

**Before — silent swallow:**

```python
def load_monsters() -> list[Monster]:
    try:
        with open(DATA_DIR / "monsters.json") as f:
            raw = json.load(f)
        return [MonsterConfig.model_validate(e).to_domain() for e in raw["monsters"]]
    except Exception:
        return []  # caller has no idea what went wrong
```

**After — specific hierarchy with chaining:**

```python
class RPGError(Exception):
    """Base class for all game errors."""

class MonsterLoadError(RPGError):
    """Raised when monsters cannot be loaded from disk."""

def load_monsters() -> list[Monster]:
    try:
        with open(DATA_DIR / "monsters.json") as f:
            raw: dict[str, list[object]] = json.load(f)
    except FileNotFoundError as e:
        raise MonsterLoadError(f"monsters.json not found: {DATA_DIR}") from e
    except json.JSONDecodeError as e:
        raise MonsterLoadError("monsters.json contains invalid JSON") from e
    monsters: list[Monster] = []
    for entry in raw["monsters"]:
        try:
            monsters.append(MonsterConfig.model_validate(entry).to_domain())
        except Exception as e:
            logger.warning("Skipping invalid monster entry: %s", e)
    return monsters
```

The caller in `simulate()` then becomes:

```python
try:
    monsters = load_monsters()
except MonsterLoadError as e:
    console.print(f"[red]Monster data error: {e}[/red]")
    logger.error("Monster load failed: %s", e)
    raise typer.Exit(1)
```

---

## Add It to the Game

### Step 1 — Define the exception hierarchy

At the top of `task.py`, after the imports, add:

```python
class RPGError(Exception):
    """Base class for all RPG errors."""

class MonsterLoadError(RPGError):
    """Raised when monsters cannot be loaded from disk."""

class SaveFileError(RPGError):
    """Raised when the save file cannot be read or written."""
```

You may also add `CombatError` for future use.

### Step 2 — Fix `load_monsters()` (Smell A)

Replace the outer `except Exception: return []` with specific clauses:

```python
def load_monsters() -> list[Monster]:
    try:
        with open(DATA_DIR / "monsters.json") as f:
            raw: dict[str, list[object]] = json.load(f)
    except FileNotFoundError as e:
        raise MonsterLoadError(f"monsters.json not found: {DATA_DIR}") from e
    except json.JSONDecodeError as e:
        raise MonsterLoadError("monsters.json contains invalid JSON") from e
    monsters: list[Monster] = []
    for entry in raw["monsters"]:
        try:
            monsters.append(MonsterConfig.model_validate(entry).to_domain())
        except Exception as e:
            logger.warning("Skipping invalid monster entry: %s", e)
    return monsters
```

Update `simulate()` to catch `MonsterLoadError` instead of checking for an empty list.

### Step 3 — Fix `load_hero()` (Smell B)

```python
def load_hero() -> Hero | None:
    if not SAVE_FILE.exists():
        return None
    try:
        model = SaveGameModel.model_validate_json(SAVE_FILE.read_text())
        if model.schema_version != CURRENT_SCHEMA_VERSION:
            return None
        return model.to_hero()
    except Exception as e:
        raise SaveFileError(f"Save file is corrupt or unreadable: {SAVE_FILE}") from e
```

### Step 4 — Fix `save_hero()` (Smell C)

```python
def save_hero(hero: Hero) -> None:
    try:
        SAVES_DIR.mkdir(parents=True, exist_ok=True)
        SAVE_FILE.write_text(SaveGameModel.from_hero(hero).model_dump_json(indent=2))
        logger.info("Saved hero: %s", hero.name)
    except OSError as e:
        logger.error("Failed to save hero: %s", e)
        raise SaveFileError(f"Could not write save file: {SAVE_FILE}") from e
```

### Step 5 — Run `check.py`

```bash
uv run python check.py
```

---

## Try It Yourself

1. Add `RPGError`, `MonsterLoadError`, and `SaveFileError` to `task.py`.
2. Fix `load_monsters()` to raise `MonsterLoadError` on file or JSON errors.
3. Fix `load_hero()` to raise `SaveFileError` instead of returning `None` on parse errors.
4. Fix `save_hero()` to log and re-raise as `SaveFileError` instead of printing the raw message.
5. Use `raise XError(...) from e` in at least one place.
6. Run `uv run python check.py` to verify.

---

## Break It

Delete `data/monsters.json`. Run:

```bash
uv run python task.py simulate
```

**Before (Smell A):** The command silently prints `No monsters found in data/.` — no stack trace, no file path, no cause.

**After (your fix):** You should see a `MonsterLoadError` with the exact path that was missing. Debug time: seconds.

---

## Fix It

Restore `data/monsters.json` (copy it from `level_5_maintainability/starter_unqualified_rpg/data/`). Re-run `check.py`.

---

## Side Quest: `raise X from None`

Sometimes you *want* to hide the original cause — for example, when the internal exception contains sensitive paths or implementation details you don't want leaking to users:

```python
except PermissionError:
    raise SaveFileError("Save file is not writable") from None
```

`from None` sets `__suppress_context__ = True`. Python will not print the original `PermissionError` in the traceback. Use this sparingly — it makes debugging harder. Prefer `from e` unless you have a specific reason to suppress.

---

## Real-World Translation

| Game mechanic | Production use |
|---|---|
| `RPGError` base class | `AppError` / `DomainError` in a service layer |
| `MonsterLoadError` | `ConfigLoadError` raised when config.yaml is missing or malformed |
| `SaveFileError` | `StorageError` raised by a repository when writes fail |
| `raise X from e` | Preserving DB driver errors while raising domain exceptions |
| Catching at the right layer | HTTP handlers catch domain errors and convert to 4xx/5xx responses |

---

## Checklist

- [ ] `RPGError(Exception)` base class defined in `task.py`
- [ ] At least 2 specific subclasses defined (e.g. `SaveFileError`, `MonsterLoadError`)
- [ ] No bare `except:` in `task.py`
- [ ] No silent `except Exception: pass` or `except Exception: return None` patterns
- [ ] `raise XError(...) from e` used at least once (exception chaining)
- [ ] `uv run python check.py` prints `✅ Mission 07 complete!`
