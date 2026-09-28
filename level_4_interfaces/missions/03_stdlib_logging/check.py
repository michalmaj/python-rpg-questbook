"""Check: Mission 03 — stdlib logging.

Verifies the event -> log level contract behaviorally: for each event the
mission's own task.py comments name a specific level for (e.g.
"# REPLACE WITH LOGGING (logger.warning)"), this checker triggers that exact
code path with a fake `logger` object standing in for the real one, and
confirms the *right* level was actually used — not just that some logger.*
call exists somewhere. A solution that routes everything through
logger.debug() (with one incidental logger.exception() elsewhere to look
busy) fails every assertion below except the ones that genuinely expect
debug.
"""

import ast
import json
import logging
import tempfile
from pathlib import Path

task_path = Path(__file__).parent / "task.py"
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


# ── load task.py as a module we can poke at ───────────────────────────────────

import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location("task03", task_path)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)  # type: ignore[union-attr]


class LoggerSpy:
    """Stands in for the module's `logger`. Records which level method was
    called, not the exact message text — the mission's contract is about
    choosing the right level, not wording."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def debug(self, *a, **kw) -> None:
        self.calls.append("debug")

    def info(self, *a, **kw) -> None:
        self.calls.append("info")

    def warning(self, *a, **kw) -> None:
        self.calls.append("warning")

    def error(self, *a, **kw) -> None:
        self.calls.append("error")

    def exception(self, *a, **kw) -> None:
        self.calls.append("exception")

    def levels_used(self) -> set[str]:
        return set(self.calls)


def _spy_call(fn, *args, **kwargs) -> LoggerSpy:
    """Swap mod.logger for a spy, call fn, restore, return the spy.

    Works because functions defined in `mod` look up the bare name `logger`
    in the module's global namespace at call time — the same trick already
    used for `console` in the Mission 05 checker.
    """
    spy = LoggerSpy()
    original = mod.logger
    mod.logger = spy
    try:
        fn(*args, **kwargs)
    finally:
        mod.logger = original
    return spy


def _make_input(*responses: str):
    it = iter(responses)

    def _input(prompt: str = "") -> str:
        return next(it)

    return _input


def _spy_call_with_input(fn, responses: tuple[str, ...], *args, **kwargs) -> LoggerSpy:
    spy = LoggerSpy()
    original_logger = mod.logger
    mod.logger = spy
    mod.input = _make_input(*responses)
    try:
        fn(*args, **kwargs)
    finally:
        mod.logger = original_logger
        del mod.input
    return spy


def _require(spy: LoggerSpy, level: str, event: str) -> None:
    if level not in spy.levels_used():
        print(
            f"❌ {event}: expected logger.{level}(...) to be called, "
            f"but only {sorted(spy.levels_used()) or ['nothing']} was logged."
        )
        raise SystemExit(1)
    print(f"✓ {event} → logger.{level}()")


# ── setup_logging exists and works ────────────────────────────────────────────

setup_logging = getattr(mod, "setup_logging", None)
if setup_logging is None:
    print("❌ setup_logging() not found in task.py")
    raise SystemExit(1)

try:
    setup_logging("DEBUG")
except NotImplementedError:
    print("❌ setup_logging() not yet implemented (raises NotImplementedError)")
    raise SystemExit(1)
except Exception as e:
    print(f"❌ setup_logging('DEBUG') raised an unexpected error: {e}")
    raise SystemExit(1)
print("✓ setup_logging('DEBUG') runs without error")

root_level = logging.getLogger().level
if root_level > logging.DEBUG:
    print(f"❌ Expected root logger level <= DEBUG ({logging.DEBUG}), got {root_level}")
    raise SystemExit(1)
print("✓ Root logger level set correctly")

setup_logging("WARNING")
root_level = logging.getLogger().level
if root_level != logging.WARNING:
    print(f"❌ setup_logging('WARNING') should set level to {logging.WARNING}, got {root_level}")
    raise SystemExit(1)
print("✓ setup_logging('WARNING') sets correct level")

setup_logging("DEBUG")  # back to permissive for the rest of this check

# ── logger = logging.getLogger(__name__) present ─────────────────────────────

task_src = task_path.read_text()
if "logging.getLogger(" not in task_src:
    print("❌ logging.getLogger() not found in task.py")
    raise SystemExit(1)
print("✓ logging.getLogger() present")

# ── no REPLACE WITH LOGGING markers remain ───────────────────────────────────

remaining = [
    i + 1 for i, line in enumerate(task_src.splitlines())
    if "# REPLACE WITH LOGGING" in line
]
if remaining:
    print(f"❌ {len(remaining)} '# REPLACE WITH LOGGING' markers still present "
          f"(lines {remaining}). Replace each with a logger.* call.")
    raise SystemExit(1)
print("✓ All '# REPLACE WITH LOGGING' markers replaced")

# ── fixture: a small, self-contained data/save directory ─────────────────────

tmp_root = Path(tempfile.mkdtemp())
data_dir = tmp_root / "data"
data_dir.mkdir()
saves_dir = tmp_root / "saves"

(data_dir / "monsters.json").write_text(json.dumps({
    "monsters": [
        {"name": "Goblin", "hp": 30, "atk": 8, "def": 2, "gold": 10},
        {"name": "Broken", "hp": -5, "atk": 8, "def": 2, "gold": 10},  # invalid: hp <= 0
    ]
}))
(data_dir / "hero_classes.json").write_text(json.dumps({
    "warrior": {"hp": 120, "atk": 15, "def": 8, "description": "Tough"},
    "mage":    {"hp": 80,  "atk": 20, "def": 3, "description": "Fragile"},
    "rogue":   {"hp": 100, "atk": 17, "def": 5, "description": "Balanced"},
}))

mod.DATA_DIR = data_dir
mod.SAVES_DIR = saves_dir
mod.SAVE_FILE = saves_dir / "save_game.json"
mod.LOG_FILE = saves_dir / "combat_log.csv"

# ── load_monsters(): a skipped invalid entry must warn ────────────────────────

spy = _spy_call(mod.load_monsters)
_require(spy, "warning", "load_monsters() skipping an invalid entry")

# ── load_monsters(): a totally broken data dir must log with traceback ───────

mod.DATA_DIR = tmp_root / "does_not_exist"
spy = _spy_call(mod.load_monsters)
_require(spy, "exception", "load_monsters() failing to read the data file")
mod.DATA_DIR = data_dir

# ── load_hero_classes(): broken data dir must log with traceback ─────────────

mod.DATA_DIR = tmp_root / "does_not_exist"
spy = _spy_call(mod.load_hero_classes)
_require(spy, "exception", "load_hero_classes() failing to read the data file")
mod.DATA_DIR = data_dir

# ── save_game(): a successful save is a normal event, not noise ──────────────

hero = mod.Hero(name="Tester", hero_class=mod.HeroClass.WARRIOR,
                hp=100, max_hp=100, atk=100, def_=10)
spy = _spy_call(mod.save_game, hero)
_require(spy, "info", "save_game() after a successful save")

# ── load_game(): no save file is routine, not worth INFO/WARNING ─────────────

mod.SAVE_FILE.unlink(missing_ok=True)
spy = _spy_call(mod.load_game)
_require(spy, "debug", "load_game() when no save file exists")

# ── load_game(): a normal successful load is a normal event ──────────────────

mod.save_game(hero)  # writes a valid, current-schema save file
spy = _spy_call(mod.load_game)
_require(spy, "info", "load_game() after a successful load")

# ── load_game(): an old schema_version is unexpected but handled ─────────────

raw = json.loads(mod.SAVE_FILE.read_text())
raw["schema_version"] = 99
mod.SAVE_FILE.write_text(json.dumps(raw))
spy = _spy_call(mod.load_game)
_require(spy, "warning", "load_game() with a schema_version mismatch")

# ── load_game(): corrupt save data must log with traceback ───────────────────

mod.SAVE_FILE.write_text("{not valid json")
spy = _spy_call(mod.load_game)
_require(spy, "exception", "load_game() with a corrupt save file")

# ── _append_log_row(): per-turn detail is DEBUG, not user-facing noise ───────

monster = mod.Monster(name="Goblin", hp=10, atk=5, def_=2, gold=3)
spy = _spy_call(
    mod._append_log_row, 1, 1, hero, monster, "attack", 5, 0, "ongoing",
)
_require(spy, "debug", "_append_log_row() recording a turn")

# ── choose_hero(): an invalid class choice is unexpected but recoverable ─────

spy = _spy_call_with_input(mod.choose_hero, ("Tester", "9"))
_require(spy, "warning", "choose_hero() with an out-of-range class choice")

# ── run_combat(): battle start (INFO) and per-attack detail (DEBUG) ──────────

strong_hero = mod.Hero(name="Tester", hero_class=mod.HeroClass.WARRIOR,
                       hp=100, max_hp=100, atk=100, def_=10)
weak_monster = mod.Monster(name="Weakling", hp=1, atk=1, def_=0, gold=1)
spy = _spy_call_with_input(mod.run_combat, ("a",), strong_hero, weak_monster, battle_id=1)
_require(spy, "info", "run_combat() announcing the battle")
_require(spy, "debug", "run_combat() logging the hero's attack")

# ── main() calls setup_logging() ─────────────────────────────────────────────

try:
    tree = ast.parse(task_src)
except SyntaxError:
    pass
else:
    main_func = next(
        (node for node in ast.walk(tree)
         if isinstance(node, ast.FunctionDef) and node.name == "main"),
        None,
    )
    if main_func:
        calls_in_main = [
            node for node in ast.walk(main_func)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "setup_logging"
        ]
        if not calls_in_main:
            print("❌ main() does not call setup_logging() — logging is defined but never activated when the game runs")
            raise SystemExit(1)
        print("✓ main() calls setup_logging()")

update_progress("03_stdlib_logging")
print("\n✅ Mission 03 complete!")
