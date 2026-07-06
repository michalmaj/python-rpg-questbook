"""check.py — Project 02: Observable Battle Runner"""

import ast
import json
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
PROGRESS_FILE = Path(__file__).parents[3] / "level_4_interfaces" / ".progress"
TASK_FILE = PROJECT_DIR / "task.py"


def update_progress(project_id: str) -> None:
    progress: dict = {"missions": {}, "projects": {}}
    if PROGRESS_FILE.exists():
        try:
            progress = json.loads(PROGRESS_FILE.read_text())
        except json.JSONDecodeError:
            pass
    progress["projects"][project_id] = "complete"
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


def run_battle(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TASK_FILE)] + args,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )


def _uses_getLogger(source: str) -> bool:
    """Return True if source calls logging.getLogger at module level or in setup_logging."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr == "getLogger":
                return True
    return False


def main() -> None:
    # ── 1. Import without side effects ────────────────────────────────────────
    sys.path.insert(0, str(PROJECT_DIR))
    try:
        import task as _task
    except ImportError as exc:
        print(f"❌ Cannot import task.py: {exc}")
        raise SystemExit(1)

    # ── 2. app is a Typer instance ────────────────────────────────────────────
    try:
        import typer
    except ImportError:
        print("❌ typer not installed")
        raise SystemExit(1)
    if not isinstance(_task.app, typer.Typer):
        print("❌ 'app' must be a typer.Typer() instance")
        raise SystemExit(1)
    print("✓ app is a typer.Typer instance")

    # ── 3. AST check — logging.getLogger used ────────────────────────────────
    source = TASK_FILE.read_text(encoding="utf-8")
    if not _uses_getLogger(source):
        print("❌ task.py must use logging.getLogger() — don't replace loggers with print()")
        raise SystemExit(1)
    print("✓ logging.getLogger() is called in task.py")

    # ── 4. Scaffold guard ─────────────────────────────────────────────────────
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_battle(["battle", "--hero", "Ada", "--monster", "Goblin"],
                            cwd=Path(tmpdir))
        if "NotImplementedError" in (result.stdout + result.stderr):
            print("❌ task.py is not implemented yet — replace NotImplementedError with real code")
            raise SystemExit(1)

    # ── 5. Both log files are created after a battle ──────────────────────────
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        result = run_battle(["battle", "--hero", "Ada", "--monster", "Goblin"],
                            cwd=tmppath)
        if result.returncode != 0:
            print(f"❌ 'battle --hero Ada --monster Goblin' exited {result.returncode}")
            print(result.stdout or result.stderr)
            raise SystemExit(1)

        app_log = tmppath / "app.log"
        combat_log = tmppath / "combat.log"

        if not app_log.exists():
            print("❌ app.log was not created after a battle")
            raise SystemExit(1)
        if not combat_log.exists():
            print("❌ combat.log was not created after a battle")
            raise SystemExit(1)
        print("✓ Both app.log and combat.log are created after a battle")

        # ── 6. app.log contains battle info ──────────────────────────────────
        app_content = app_log.read_text(encoding="utf-8").lower()
        if not any(kw in app_content for kw in ("battle", "combat", "ada", "goblin")):
            print("❌ app.log must contain battle-related info (hero name, monster, result)")
            raise SystemExit(1)
        print("✓ app.log contains battle-related info")

        # ── 7. combat.log contains round-by-round entries ────────────────────
        combat_content = combat_log.read_text(encoding="utf-8")
        combat_lines = [ln for ln in combat_content.splitlines() if ln.strip()]
        if len(combat_lines) < 1:
            print("❌ combat.log must contain at least one round entry per battle")
            raise SystemExit(1)
        print(f"✓ combat.log contains {len(combat_lines)} line(s) of combat events")

    # ── 8. Unknown monster → friendly stderr, non-zero exit, no traceback ────
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_battle(["battle", "--hero", "Ada", "--monster", "Unknown"],
                            cwd=Path(tmpdir))
        if result.returncode == 0:
            print("❌ Unknown monster should exit non-zero")
            raise SystemExit(1)
        combined = result.stdout + result.stderr
        if "Traceback" in combined or "KeyError" in combined:
            print("❌ Unknown monster must produce a friendly message, not a traceback")
            print(combined)
            raise SystemExit(1)
        if len(combined.strip()) == 0:
            print("❌ Unknown monster should print an error message, got empty output")
            raise SystemExit(1)
        print("✓ Unknown monster → friendly message, non-zero exit, no traceback")

        # Check app.log received error info
        app_log = Path(tmpdir) / "app.log"
        if app_log.exists():
            app_content = app_log.read_text(encoding="utf-8").lower()
            if any(kw in app_content for kw in ("error", "unknown", "not found")):
                print("✓ app.log received error info")

    # ── Done ──────────────────────────────────────────────────────────────────
    update_progress("02_observable_battle_runner")
    print()
    print("✅ Project 02 complete: Observable Battle Runner works!")
    print()
    print("   Structured logs in two files. The terminal stays clean.")
    print("   Errors reach the log — not the user's screen as tracebacks.")


if __name__ == "__main__":
    main()
