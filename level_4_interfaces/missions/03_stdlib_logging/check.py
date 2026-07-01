"""Check: Mission 03 — stdlib logging."""

import importlib.util
import logging
from pathlib import Path

task_path = Path(__file__).parent / "task.py"

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

print("\n✅ Mission 03 complete!")
