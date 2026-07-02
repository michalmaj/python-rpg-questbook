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

# Flag patterns like: "except Exception:" or "except Exception as e:" followed immediately
# by pass or return None with no logging/re-raise in between
silent_patterns = re.findall(
    r"except Exception(?:\s+as\s+\w+)?\s*:\s*\n\s*(pass|return None)\s*\n",
    src,
)
if silent_patterns:
    print(f"❌ Found {len(silent_patterns)} silent 'except Exception: pass/return None' pattern(s)")
    print("   Either log the error, re-raise as a specific RPGError, or handle meaningfully")
    raise SystemExit(1)
print("✓ No silent except Exception: pass patterns")

# ── raise ... from e used at least once ──────────────────────────────────────

if "from e" not in src and "from exc" not in src and "from err" not in src:
    print("❌ 'raise XError(...) from e' pattern not found — preserve exception chain context")
    raise SystemExit(1)
print("✓ Exception chaining (raise X from e) used")

update_progress("07_error_handling")
print("\n✅ Mission 07 complete!")
