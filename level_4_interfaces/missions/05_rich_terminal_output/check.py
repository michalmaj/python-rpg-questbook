"""Check: Mission 05 — Rich terminal output."""

import importlib.util
import io
import json
import sys
from pathlib import Path

from rich.console import Console

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

spec = importlib.util.spec_from_file_location("task05", task_path)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)  # type: ignore[union-attr]

Hero = mod.Hero
HeroClass = mod.HeroClass
Monster = mod.Monster

show_hero_stats = getattr(mod, "show_hero_stats", None)
show_combat_start = getattr(mod, "show_combat_start", None)
show_combat_result = getattr(mod, "show_combat_result", None)
show_error = getattr(mod, "show_error", None)

for fn_name in ("show_hero_stats", "show_combat_start", "show_combat_result", "show_error"):
    if getattr(mod, fn_name, None) is None:
        print(f"❌ {fn_name}() not found in task.py")
        raise SystemExit(1)

# ── console = Console() exists ────────────────────────────────────────────────

task_src = task_path.read_text()
if "Console()" not in task_src:
    print("❌ console = Console() not found in task.py")
    raise SystemExit(1)
print("✓ Console() present")

if "import argparse" in task_src or "print(" in task_src.split("def show_hero_stats")[1].split("def show_combat_start")[0]:
    pass  # we check via output below — don't over-constrain implementation

# ── helper: capture console output ───────────────────────────────────────────

def capture(fn, *args, **kwargs) -> str:
    buf = io.StringIO()
    c = Console(file=buf, highlight=False, markup=False)
    original = mod.console
    mod.console = c
    try:
        fn(*args, **kwargs)
    finally:
        mod.console = original
    return buf.getvalue()


def capture_stdout_and_stderr(fn, *args, **kwargs) -> tuple[str, str]:
    """Swap the real sys.stdout/sys.stderr for buffers and call fn.

    Works regardless of how the implementation routes to stderr — a
    module-level Console(stderr=True) resolves its output stream by
    reading sys.stderr at print time (unless given an explicit file=),
    so this catches any correctly-configured Console, under any variable
    name, without requiring one specific implementation shape.
    """
    out_buf, err_buf = io.StringIO(), io.StringIO()
    original_out, original_err = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = out_buf, err_buf
    try:
        fn(*args, **kwargs)
    finally:
        sys.stdout, sys.stderr = original_out, original_err
    return out_buf.getvalue(), err_buf.getvalue()


# ── sample data ───────────────────────────────────────────────────────────────

hero = Hero(name="Ada", hero_class=HeroClass.WARRIOR,
            hp=96, max_hp=120, atk=12, def_=4,
            gold=30, wins=3, losses=1)
monster = Monster(name="Goblin", hp=30, atk=8, def_=2, gold=10)

# ── show_hero_stats ───────────────────────────────────────────────────────────

try:
    out = capture(show_hero_stats, hero)
except NotImplementedError:
    print("❌ show_hero_stats() not yet implemented")
    raise SystemExit(1)

for expected in ("Ada", "96", "120", "30"):
    if expected not in out:
        print(f"❌ show_hero_stats(): expected '{expected}' in output, got:\n{out}")
        raise SystemExit(1)
print("✓ show_hero_stats() shows name, HP, and gold")

if "Table" not in task_src and "table" not in task_src.lower():
    print("❌ show_hero_stats() does not use Table — use rich.table.Table")
    raise SystemExit(1)
print("✓ Table used in show_hero_stats()")

# ── show_combat_start ─────────────────────────────────────────────────────────

try:
    out = capture(show_combat_start, hero, monster)
except NotImplementedError:
    print("❌ show_combat_start() not yet implemented")
    raise SystemExit(1)

for expected in ("Ada", "Goblin"):
    if expected not in out:
        print(f"❌ show_combat_start(): expected '{expected}' in output")
        raise SystemExit(1)
print("✓ show_combat_start() shows hero and monster names")

if "Panel" not in task_src:
    print("❌ show_combat_start() does not use Panel — use rich.panel.Panel")
    raise SystemExit(1)
print("✓ Panel used in show_combat_start()")

# ── show_combat_result ────────────────────────────────────────────────────────

try:
    out_win = capture(show_combat_result, "hero", 10)
    out_loss = capture(show_combat_result, "monster")
except NotImplementedError:
    print("❌ show_combat_result() not yet implemented")
    raise SystemExit(1)

if not out_win:
    print("❌ show_combat_result('hero') produced no output")
    raise SystemExit(1)
if not out_loss:
    print("❌ show_combat_result('monster') produced no output")
    raise SystemExit(1)
print("✓ show_combat_result() produces output for both win and loss")

# ── show_error goes to stderr, not stdout ─────────────────────────────────────

try:
    out, err = capture_stdout_and_stderr(show_error, "test error message")
except NotImplementedError:
    print("❌ show_error() not yet implemented")
    raise SystemExit(1)

if "test error message" not in err:
    print(f"❌ show_error(): expected the message on stderr, got stderr:\n{err!r}")
    raise SystemExit(1)
print("✓ show_error() writes the message to stderr")

if "test error message" in out:
    print(f"❌ show_error(): message also leaked to stdout:\n{out!r}")
    raise SystemExit(1)
print("✓ show_error() does not write to stdout")

# ── no raw print() in the four functions ─────────────────────────────────────

# check that the implementation bodies don't use print() directly
# (we allow print in main() and run_combat() as fallbacks)
fn_sections = [
    ("show_hero_stats", "show_combat_start"),
    ("show_combat_start", "show_combat_result"),
    ("show_combat_result", "show_error"),
    ("show_error", "compute_damage"),
]
for start_fn, end_fn in fn_sections:
    if start_fn in task_src and end_fn in task_src:
        section = task_src.split(f"def {start_fn}")[1].split(f"def {end_fn}")[0]
        if "\n    print(" in section and "raise NotImplementedError" not in section:
            print(f"❌ {start_fn}() uses print() — use console.print() instead")
            raise SystemExit(1)
print("✓ No raw print() in the four output functions")

update_progress("05_rich_terminal_output")
print("\n✅ Mission 05 complete!")
