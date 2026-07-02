"""Check: Mission 07 — error handling."""

import importlib.util
import json
import re
import sys
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


# ── import task.py to inspect exception classes ───────────────────────────────

spec = importlib.util.spec_from_file_location("task07", task)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
sys.modules["task07"] = mod
try:
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
except SystemExit:
    pass  # Typer raises SystemExit for --help; that's fine
except Exception as e:
    print(f"❌ Failed to import task.py: {e}")
    raise SystemExit(1)

# ── RPGError base class ───────────────────────────────────────────────────────

if not hasattr(mod, "RPGError"):
    print("❌ RPGError base class not found in task.py")
    raise SystemExit(1)
if not issubclass(mod.RPGError, Exception):
    print("❌ RPGError must inherit from Exception")
    raise SystemExit(1)
print("✓ RPGError(Exception) base class defined")

# ── at least 2 specific subclasses ───────────────────────────────────────────

subclasses = [
    name for name in dir(mod)
    if isinstance(getattr(mod, name), type)
    and issubclass(getattr(mod, name), mod.RPGError)
    and getattr(mod, name) is not mod.RPGError
]
if len(subclasses) < 2:
    print(f"❌ Only {len(subclasses)} RPGError subclasses found (need ≥ 2)")
    print("   Expected: SaveFileError, MonsterLoadError (at minimum)")
    raise SystemExit(1)
print(f"✓ {len(subclasses)} RPGError subclasses: {subclasses}")

# ── no bare except ────────────────────────────────────────────────────────────

src = task.read_text()
if "except:" in src:
    print("❌ Bare 'except:' found — use specific exception types")
    raise SystemExit(1)
print("✓ No bare except:")

# ── no silent except Exception: pass ─────────────────────────────────────────

# Find lines that are ONLY pass/return-nothing after an except Exception block
silent_count = len(re.findall(
    r"except Exception(?:\s+as\s+\w+)?\s*:\s*\n\s*(pass\b|return \[\]|return None\b)[^\n]*\n",
    src,
))
if silent_count > 0:
    print(f"❌ Found {silent_count} silent exception handler(s) — use 'raise XError(...) from e' instead")
    raise SystemExit(1)
print(f"✓ No silent exception swallowing found")

# ── no raw error printing in save_hero (Smell C) ─────────────────────────────

if 'print(f"Save failed:' in src or "print(f'Save failed:" in src:
    print("❌ Smell C not fixed: save_hero still prints raw error to the user")
    print("   Replace 'print(f\"Save failed: {e}\")' with 'raise SaveFileError(...) from e'")
    raise SystemExit(1)
print("✓ No raw error printing found in save_hero")

# ── raise ... from e used at least once ──────────────────────────────────────

if not re.search(r"\braise\s+\w+[^#\n]*\bfrom\s+(?:e|exc|err)\b", src):
    print("❌ 'raise XError(...) from e' pattern not found — use 'raise SubError(...) from e' in except blocks")
    raise SystemExit(1)
print("✓ Exception chaining with 'from e' found")

update_progress("07_error_handling")
print("\n✅ Mission 07 complete!")
