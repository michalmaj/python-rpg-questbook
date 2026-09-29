"""Check: Mission 02 — mypy type checking."""

import importlib.util
import json
import subprocess
import sys
import typing
from pathlib import Path

task = Path(__file__).parent / "task.py"
pyproject = Path(__file__).parent / "pyproject.toml"
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


# ── pyproject.toml has [tool.mypy] ───────────────────────────────────────────

if not pyproject.exists():
    print("❌ pyproject.toml not found in this mission folder")
    raise SystemExit(1)
if "[tool.mypy]" not in pyproject.read_text():
    print("❌ [tool.mypy] section not found in pyproject.toml")
    raise SystemExit(1)
print("✓ pyproject.toml has [tool.mypy]")

# ── ruff must still pass ──────────────────────────────────────────────────────

result = subprocess.run(
    [sys.executable, "-m", "ruff", "check", str(task), "--config", str(pyproject)],
    capture_output=True, text=True,
)
if result.returncode != 0:
    print("❌ ruff check fails (regression — task.py should stay ruff-clean):")
    print(result.stdout)
    raise SystemExit(1)
print("✓ ruff check still passes")

# ── mypy --strict must pass ───────────────────────────────────────────────────

result = subprocess.run(
    [sys.executable, "-m", "mypy", str(task), "--strict",
     "--config-file", str(pyproject)],
    capture_output=True, text=True,
)
if result.returncode != 0:
    print("❌ mypy --strict fails:")
    print(result.stdout)
    raise SystemExit(1)
print("✓ mypy --strict passes")

# ── at least 8 annotated function signatures ──────────────────────────────────

src = task.read_text()
annotated = [ln for ln in src.splitlines() if "def " in ln and " -> " in ln]
if len(annotated) < 8:
    print(f"❌ Only {len(annotated)} annotated function signatures (need ≥ 8)")
    print("   Make sure all top-level functions and class methods have return types")
    raise SystemExit(1)
print(f"✓ {len(annotated)} annotated function signatures")

# ── Any is not a substitute for the required types ────────────────────────────
#
# mypy --strict does not forbid explicit `Any` — a solution that types every
# parameter and return as `Any` passes it. That defeats the point of this
# mission (meaningful types), so check the resolved runtime type hints of the
# specific signatures the README's table asks for, and reject any of them
# that resolve to (or contain) `Any` anywhere — bare `Any`, `list[Any]`,
# `dict[str, Any]`, `Any | None`, etc.

spec = importlib.util.spec_from_file_location("task02", task)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
except SystemExit:
    pass  # Typer may raise SystemExit for --help-style side effects; fine
except Exception as e:
    print(f"❌ Failed to import task.py: {e}")
    raise SystemExit(1)


def _contains_any(tp: object) -> bool:
    if tp is typing.Any:
        return True
    return any(_contains_any(a) for a in typing.get_args(tp))


def _check_hints(label: str, hints: dict[str, object], required: set[str]) -> None:
    missing = required - hints.keys()
    if missing:
        print(f"❌ {label}: missing annotation(s) for {sorted(missing)}")
        raise SystemExit(1)
    widened = [name for name in required if _contains_any(hints[name])]
    if widened:
        print(
            f"❌ {label}: {sorted(widened)} typed as (or contains) Any — "
            f"use the real type from the Mission 02 table, not Any"
        )
        raise SystemExit(1)


targets: list[tuple[str, typing.Callable[[], dict[str, object]], set[str]]] = [
    ("compute_damage", lambda: typing.get_type_hints(mod.compute_damage),
     {"atk", "def_", "roll", "return"}),
    ("load_monsters", lambda: typing.get_type_hints(mod.load_monsters), {"return"}),
    ("load_hero_classes", lambda: typing.get_type_hints(mod.load_hero_classes), {"return"}),
    ("save_hero", lambda: typing.get_type_hints(mod.save_hero), {"hero", "return"}),
    ("load_hero", lambda: typing.get_type_hints(mod.load_hero), {"return"}),
    ("make_hero", lambda: typing.get_type_hints(mod.make_hero),
     {"name", "hero_class", "return"}),
    ("simulate_one", lambda: typing.get_type_hints(mod.simulate_one),
     {"hero", "monster", "return"}),
    ("generate_reports", lambda: typing.get_type_hints(mod.generate_reports),
     {"session", "return"}),
    ("Hero.is_alive", lambda: typing.get_type_hints(mod.Hero.is_alive.fget), {"return"}),
    ("Hero.take_damage", lambda: typing.get_type_hints(mod.Hero.take_damage),
     {"amount", "return"}),
    ("Hero.use_potion", lambda: typing.get_type_hints(mod.Hero.use_potion), {"return"}),
    ("Monster.is_alive", lambda: typing.get_type_hints(mod.Monster.is_alive.fget), {"return"}),
    ("Monster.take_damage", lambda: typing.get_type_hints(mod.Monster.take_damage),
     {"amount", "return"}),
]

for label, get_hints, required in targets:
    try:
        hints = get_hints()
    except Exception as e:
        print(f"❌ Could not resolve type hints for {label}: {e}")
        raise SystemExit(1)
    _check_hints(label, hints, required)

print(f"✓ {len(targets)} required signatures use real types, not Any")

# ── no bare except ────────────────────────────────────────────────────────────

if "except:" in src:
    print("❌ Bare 'except:' still present — use 'except Exception as e:'")
    raise SystemExit(1)
print("✓ No bare except:")

# ── no old typing syntax ──────────────────────────────────────────────────────

for old in ("Optional[", "List[", "Dict[", "from typing import Optional"):
    if old in src:
        print(f"❌ Old typing syntax '{old}' found — use X | None, list[...], dict[...]")
        raise SystemExit(1)
print("✓ No deprecated typing syntax")

update_progress("02_mypy_type_checking")
print("\n✅ Mission 02 complete!")
