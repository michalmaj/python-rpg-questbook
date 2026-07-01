"""Check: Mission 04 — log files."""

import importlib.util
import logging
import tempfile
from pathlib import Path

task_path = Path(__file__).parent / "task.py"

spec = importlib.util.spec_from_file_location("task04", task_path)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)  # type: ignore[union-attr]

add_file_handler = getattr(mod, "add_file_handler", None)
setup_log_files = getattr(mod, "setup_log_files", None)

# ── add_file_handler exists ───────────────────────────────────────────────────

if add_file_handler is None:
    print("❌ add_file_handler() not found in task.py")
    raise SystemExit(1)

if setup_log_files is None:
    print("❌ setup_log_files() not found in task.py")
    raise SystemExit(1)

# ── add_file_handler creates the file ────────────────────────────────────────

with tempfile.TemporaryDirectory() as tmp:
    log_path = Path(tmp) / "sub" / "test.log"
    test_logger = logging.getLogger("check04_test")
    # clear any existing handlers
    test_logger.handlers.clear()

    try:
        add_file_handler(test_logger, log_path, logging.DEBUG)
    except NotImplementedError:
        print("❌ add_file_handler() not yet implemented")
        raise SystemExit(1)

    if not log_path.exists():
        print("❌ add_file_handler() did not create the log file")
        raise SystemExit(1)
    print("✓ add_file_handler() creates the log file (including parent dirs)")

    test_logger.setLevel(logging.DEBUG)
    test_logger.info("test message from check")

    content = log_path.read_text()
    if "test message from check" not in content:
        print("❌ Log message not written to file")
        raise SystemExit(1)
    print("✓ Log messages written to file")

    # check the handler uses the formatter
    if "INFO" not in content:
        print("❌ Log level not in formatted output — check your formatter")
        raise SystemExit(1)
    print("✓ Log output includes level name")

    test_logger.handlers.clear()

# ── setup_log_files wires app.log and combat.log ─────────────────────────────

with tempfile.TemporaryDirectory() as tmp:
    log_dir = Path(tmp)

    # reset root and combat logger handlers
    root = logging.getLogger()
    root.handlers = [h for h in root.handlers if not isinstance(h, logging.FileHandler)]
    combat = logging.getLogger(mod.__name__ + ".combat")
    combat.handlers.clear()

    try:
        setup_log_files(log_dir)
    except NotImplementedError:
        print("❌ setup_log_files() not yet implemented")
        raise SystemExit(1)

    app_log = log_dir / "app.log"
    combat_log = log_dir / "combat.log"

    if not app_log.exists():
        print("❌ setup_log_files() did not create app.log")
        raise SystemExit(1)
    print("✓ app.log created")

    if not combat_log.exists():
        print("❌ setup_log_files() did not create combat.log")
        raise SystemExit(1)
    print("✓ combat.log created")

    # write to root logger — should go to app.log
    root.setLevel(logging.DEBUG)
    root.info("app event")
    app_content = app_log.read_text()
    if "app event" not in app_content:
        print("❌ Root logger events not written to app.log")
        raise SystemExit(1)
    print("✓ Root logger writes to app.log")

    # write to combat logger — should go to combat.log
    combat.setLevel(logging.DEBUG)
    combat.debug("combat event")
    combat_content = combat_log.read_text()
    if "combat event" not in combat_content:
        print("❌ Combat logger events not written to combat.log")
        raise SystemExit(1)
    print("✓ Combat logger writes to combat.log")

    # clean up file handlers to avoid side effects
    root.handlers = [h for h in root.handlers if not isinstance(h, logging.FileHandler)]
    combat.handlers.clear()

# ── no USE combat_logger markers remain ──────────────────────────────────────

task_src = task_path.read_text()
remaining = [
    i + 1 for i, line in enumerate(task_src.splitlines())
    if "# USE combat_logger" in line
]
if remaining:
    print(f"❌ {len(remaining)} '# USE combat_logger' markers still present "
          f"(lines {remaining}). Replace each with a combat_logger.* call.")
    raise SystemExit(1)
print("✓ All '# USE combat_logger' markers replaced")

print("\n✅ Mission 04 complete!")
