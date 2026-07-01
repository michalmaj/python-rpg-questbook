"""Check: Mission 03 — stdlib logging."""

import ast
import importlib.util
import json
import logging
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

# ── load the module without running main() ────────────────────────────────────

spec = importlib.util.spec_from_file_location("task03", task_path)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)  # type: ignore[union-attr]

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

# ── root logger level was set ─────────────────────────────────────────────────

root_level = logging.getLogger().level
if root_level > logging.DEBUG:
    print(f"❌ Expected root logger level <= DEBUG ({logging.DEBUG}), got {root_level}")
    raise SystemExit(1)
print("✓ Root logger level set correctly")

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

# ── logger is used (not just defined) ────────────────────────────────────────

logger_calls = [ln for ln in task_src.splitlines()
                if "logger." in ln and not ln.strip().startswith("#")]
if len(logger_calls) < 5:
    print(f"❌ Expected at least 5 logger.* calls, found {len(logger_calls)}.")
    raise SystemExit(1)
print(f"✓ {len(logger_calls)} logger.* calls found")

# ── logger.exception used in at least one except block ───────────────────────

if "logger.exception(" not in task_src:
    print("❌ logger.exception() not found — use it in except blocks so the traceback is recorded.")
    raise SystemExit(1)
print("✓ logger.exception() present")

# ── setup_logging also handles WARNING ───────────────────────────────────────

setup_logging("WARNING")
root_level = logging.getLogger().level
if root_level != logging.WARNING:
    print(f"❌ setup_logging('WARNING') should set level to {logging.WARNING}, got {root_level}")
    raise SystemExit(1)
print("✓ setup_logging('WARNING') sets correct level")

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
