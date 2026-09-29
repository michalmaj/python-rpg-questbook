"""Check: Mission 07 — error handling.

Verifies the exception-handling contract behaviorally: for each smell the
mission names (load_monsters, load_hero, save_hero), this checker triggers
the real failure condition (missing file, corrupt JSON, a write that raises
OSError) against the actual functions, and asserts that a real RPGError
subclass is genuinely raised — with __cause__ pointing at the real
underlying exception — instead of the old silent return. A solution that
defines the exception hierarchy but still swallows errors (or chains only
inside a dead helper function nothing calls) fails every assertion below.
"""

import importlib.util
import json
import tempfile
from pathlib import Path

task = Path(__file__).parent / "task.py"
PROGRESS_FILE = Path(__file__).parents[2] / ".progress"


def update_progress(mission_id: str) -> None:
    progress: dict = {"missions": {}, "projects": {}}
    if PROGRESS_FILE.exists():
        try:
            progress = json.loads(PROGRESS_FILE.read_text())
        except json.JSONDecodeError:
            pass
    progress["missions"][mission_id] = "complete"
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


# ── import task.py as a module we can poke at ─────────────────────────────────

spec = importlib.util.spec_from_file_location("task07", task)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
except SystemExit:
    pass  # Typer may raise SystemExit for --help-style side effects; fine
except Exception as e:
    print(f"❌ Failed to import task.py: {e}")
    raise SystemExit(1)


def _require(cond: bool, message: str) -> None:
    if not cond:
        print(f"❌ {message}")
        raise SystemExit(1)


# ── RPGError base class + at least 2 specific subclasses ─────────────────────

_require(hasattr(mod, "RPGError"), "RPGError base class not found in task.py")
_require(issubclass(mod.RPGError, Exception), "RPGError must inherit from Exception")
print("✓ RPGError(Exception) base class defined")

subclasses = [
    name for name in dir(mod)
    if isinstance(getattr(mod, name), type)
    and issubclass(getattr(mod, name), mod.RPGError)
    and getattr(mod, name) is not mod.RPGError
]
_require(
    len(subclasses) >= 2,
    f"Only {len(subclasses)} RPGError subclasses found (need >= 2). "
    f"Expected something like SaveFileError, MonsterLoadError.",
)
print(f"✓ {len(subclasses)} RPGError subclasses: {subclasses}")

# ── fixture: an isolated data/save directory ──────────────────────────────────

tmp_root = Path(tempfile.mkdtemp())
data_dir = tmp_root / "data"
data_dir.mkdir()
saves_dir = tmp_root / "saves"

(data_dir / "monsters.json").write_text(json.dumps({
    "monsters": [{"name": "Goblin", "hp": 30, "atk": 8, "def": 2, "gold": 10}]
}))
(data_dir / "hero_classes.json").write_text(json.dumps({
    "warrior": {"hp": 120, "atk": 15, "def": 8, "description": "Tough"},
}))

mod.DATA_DIR = data_dir
mod.SAVES_DIR = saves_dir
mod.SAVE_FILE = saves_dir / "save_game.json"
mod.LOG_FILE = saves_dir / "app.log"


# ── load_monsters(): missing data file must raise an RPGError, chained ───────

mod.DATA_DIR = tmp_root / "does_not_exist"
try:
    result = mod.load_monsters()
except mod.RPGError as e:
    _require(
        e.__cause__ is not None and isinstance(e.__cause__, Exception),
        "load_monsters(): the RPGError raised for a missing monsters.json has "
        "no __cause__ — use 'raise XError(...) from e' to chain the real "
        "FileNotFoundError, not a bare raise",
    )
    print(f"✓ load_monsters() with a missing data file raises {type(e).__name__} "
          f"chained from {type(e.__cause__).__name__}")
except Exception as e:
    print(f"❌ load_monsters() with a missing data file raised {type(e).__name__}, "
          f"which is not an RPGError subclass — use your custom hierarchy")
    raise SystemExit(1)
else:
    print(f"❌ load_monsters() with a missing data file returned {result!r} instead "
          f"of raising — Smell A: this is the exact silent-swallow this mission "
          f"asks you to fix")
    raise SystemExit(1)
mod.DATA_DIR = data_dir


# ── load_monsters(): corrupt JSON must raise an RPGError, chained ────────────

mod.DATA_DIR = tmp_root / "corrupt_data"
mod.DATA_DIR.mkdir()
(mod.DATA_DIR / "monsters.json").write_text("{not valid json")
try:
    result = mod.load_monsters()
except mod.RPGError as e:
    _require(
        e.__cause__ is not None,
        "load_monsters(): the RPGError raised for corrupt monsters.json has "
        "no __cause__ — chain the real json.JSONDecodeError with 'from e'",
    )
    print(f"✓ load_monsters() with corrupt JSON raises {type(e).__name__} "
          f"chained from {type(e.__cause__).__name__}")
except Exception as e:
    print(f"❌ load_monsters() with corrupt JSON raised {type(e).__name__}, "
          f"which is not an RPGError subclass")
    raise SystemExit(1)
else:
    print(f"❌ load_monsters() with corrupt JSON returned {result!r} instead of "
          f"raising")
    raise SystemExit(1)
mod.DATA_DIR = data_dir


# ── load_hero(): no save file is routine, not an error ────────────────────────

mod.SAVE_FILE.unlink(missing_ok=True)
try:
    result = mod.load_hero()
except Exception as e:
    print(f"❌ load_hero() with no save file should return None (routine — "
          f"there's simply no save yet), but raised {type(e).__name__} instead. "
          f"Only a corrupt/unreadable save file should raise.")
    raise SystemExit(1)
_require(result is None, "load_hero() with no save file should return None")
print("✓ load_hero() with no save file returns None (not an error)")


# ── load_hero(): a corrupt save file must raise an RPGError, chained ─────────

mod.SAVES_DIR.mkdir(parents=True, exist_ok=True)
mod.SAVE_FILE.write_text("{not valid json")
try:
    result = mod.load_hero()
except mod.RPGError as e:
    _require(
        e.__cause__ is not None,
        "load_hero(): the RPGError raised for a corrupt save file has no "
        "__cause__ — chain the real parse error with 'from e'",
    )
    print(f"✓ load_hero() with a corrupt save file raises {type(e).__name__} "
          f"chained from {type(e.__cause__).__name__}")
except Exception as e:
    print(f"❌ load_hero() with a corrupt save file raised {type(e).__name__}, "
          f"which is not an RPGError subclass")
    raise SystemExit(1)
else:
    print(f"❌ load_hero() with a corrupt save file returned {result!r} instead "
          f"of raising — Smell B: the caller can't tell 'corrupt' from 'missing'")
    raise SystemExit(1)
mod.SAVE_FILE.unlink(missing_ok=True)


# ── save_hero(): a real write failure must raise an RPGError, chained ────────
# (not just print a raw message to the user — Smell C)

class _ExplodingPath:
    """Stands in for SAVE_FILE: .write_text() raises a real OSError."""

    def write_text(self, *args: object, **kwargs: object) -> int:
        raise OSError("simulated disk full")


hero = mod.Hero(
    name="Tester", hero_class=mod.HeroClass.warrior,
    hp=100, max_hp=100, atk=10, def_=5,
)

original_save_file = mod.SAVE_FILE
mod.SAVE_FILE = _ExplodingPath()
import io  # noqa: E402
import contextlib  # noqa: E402

captured_stdout = io.StringIO()
try:
    with contextlib.redirect_stdout(captured_stdout):
        try:
            mod.save_hero(hero)
        except mod.RPGError as e:
            _require(
                e.__cause__ is not None and isinstance(e.__cause__, OSError),
                "save_hero(): the RPGError raised on a write failure has no "
                "__cause__ pointing at the real OSError — chain it with 'from e'",
            )
        except Exception as e:
            print(f"❌ save_hero() on a write failure raised {type(e).__name__}, "
                  f"which is not an RPGError subclass")
            raise SystemExit(1)
        else:
            print("❌ save_hero() on a write failure did not raise anything — "
                  "Smell C: the failure must not be silently absorbed")
            raise SystemExit(1)
finally:
    mod.SAVE_FILE = original_save_file

leaked = captured_stdout.getvalue()
_require(
    "Save failed" not in leaked and "simulated disk full" not in leaked,
    "save_hero() still print()s the raw error message directly (Smell C) "
    "instead of only raising — log it with logger.error(...) if you want a "
    "record, but let the exception (not a print) carry the failure",
)
print("✓ save_hero() on a write failure raises (chained), not a raw print()")


# ── simulate(): the CLI layer must catch MonsterLoadError, not crash ─────────

from typer.testing import CliRunner  # noqa: E402

mod.SAVES_DIR.mkdir(parents=True, exist_ok=True)
mod.SAVE_FILE = saves_dir / "save_game.json"
mod.save_hero(hero)
mod.DATA_DIR = tmp_root / "does_not_exist"

runner = CliRunner()
result = runner.invoke(mod.app, ["simulate", "--battles", "1"])

_require(
    result.exit_code != 0,
    "'rpg simulate' should exit non-zero when monster data can't load",
)
_require(
    result.exception is None or isinstance(result.exception, SystemExit),
    f"'rpg simulate' let {type(result.exception).__name__ if result.exception else None} "
    f"escape uncaught — catch your MonsterLoadError (or RPGError) in simulate() "
    f"and print a friendly message instead of crashing",
)
_require(
    "Traceback (most recent call last)" not in result.output,
    "'rpg simulate' printed a raw Python traceback — catch the error in the "
    "CLI layer instead of letting it crash the command",
)
print("✓ 'rpg simulate' catches the load error at the CLI layer (no crash, no traceback)")

mod.DATA_DIR = data_dir


# ── no bare except ────────────────────────────────────────────────────────────

src = task.read_text()
_require("except:" not in src, "Bare 'except:' found — use specific exception types")
print("✓ No bare except:")

update_progress("07_error_handling")
print("\n✅ Mission 07 complete!")
