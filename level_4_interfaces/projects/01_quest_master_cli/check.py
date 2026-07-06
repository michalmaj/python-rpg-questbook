"""check.py — Project 01: Quest Master CLI"""

import json
import subprocess
import sys
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


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TASK_FILE)] + args,
        capture_output=True,
        text=True,
    )


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
        print("❌ typer not installed — run: uv add typer")
        raise SystemExit(1)

    if not isinstance(_task.app, typer.Typer):
        print("❌ 'app' must be a typer.Typer() instance")
        raise SystemExit(1)
    print("✓ app is a typer.Typer instance")

    # ── 3. App has exactly 3 commands ─────────────────────────────────────────
    command_names = {cmd.name or cmd.callback.__name__
                     for cmd in _task.app.registered_commands}
    for expected in ("hero", "monsters", "battle"):
        if expected not in command_names:
            print(f"❌ Missing command: '{expected}' (found: {sorted(command_names)})")
            raise SystemExit(1)
    print(f"✓ App has commands: {sorted(command_names)}")

    # ── 4. Scaffold guard ─────────────────────────────────────────────────────
    result = run(["hero", "--name", "Ada"])
    if result.returncode != 0 and "NotImplementedError" in (result.stdout + result.stderr):
        print("❌ task.py is not implemented yet — replace NotImplementedError with real code")
        raise SystemExit(1)

    # ── 5. hero --name Ada ────────────────────────────────────────────────────
    result = run(["hero", "--name", "Ada"])
    if result.returncode != 0:
        print(f"❌ 'hero --name Ada' exited {result.returncode}")
        print(result.stdout or result.stderr)
        raise SystemExit(1)
    output = result.stdout + result.stderr
    if "Ada" not in output:
        print(f"❌ 'hero --name Ada' output must contain 'Ada', got:\n{output}")
        raise SystemExit(1)
    print("✓ 'hero --name Ada' exits 0 and prints hero info")

    # ── 6. monsters lists at least 2 names ───────────────────────────────────
    result = run(["monsters"])
    if result.returncode != 0:
        print(f"❌ 'monsters' exited {result.returncode}")
        print(result.stdout or result.stderr)
        raise SystemExit(1)
    output = result.stdout + result.stderr
    words = output.lower()
    found = sum(1 for m in ("goblin", "orc", "dragon") if m in words)
    if found < 2:
        print(f"❌ 'monsters' must print at least 2 monster names, found {found} in:\n{output}")
        raise SystemExit(1)
    print(f"✓ 'monsters' exits 0 and lists at least 2 monsters")

    # ── 7. battle known hero + monster ────────────────────────────────────────
    result = run(["battle", "--hero", "Ada", "--monster", "Goblin"])
    if result.returncode != 0:
        print(f"❌ 'battle --hero Ada --monster Goblin' exited {result.returncode}")
        print(result.stdout or result.stderr)
        raise SystemExit(1)
    output = result.stdout + result.stderr
    if len(output.strip()) == 0:
        print("❌ 'battle' produced no output")
        raise SystemExit(1)
    print("✓ 'battle --hero Ada --monster Goblin' exits 0 and prints result")

    # ── 8. battle unknown hero → friendly error, non-zero exit ───────────────
    result = run(["battle", "--hero", "Unknown", "--monster", "Goblin"])
    if result.returncode == 0:
        print("❌ 'battle --hero Unknown' should exit non-zero for an unknown hero")
        raise SystemExit(1)
    combined = (result.stdout + result.stderr).lower()
    if "traceback" in combined or "keyerror" in combined:
        print("❌ Unknown hero must produce a friendly message, not a Python traceback")
        print(result.stdout or result.stderr)
        raise SystemExit(1)
    if len(combined.strip()) == 0:
        print("❌ Unknown hero should print an error message, got empty output")
        raise SystemExit(1)
    print("✓ Unknown hero → friendly message, non-zero exit (no traceback)")

    # ── Done ──────────────────────────────────────────────────────────────────
    update_progress("01_quest_master_cli")
    print()
    print("✅ Project 01 complete: Quest Master CLI works!")
    print()
    print("   Three commands, type hints as contract, friendly errors.")
    print("   This is what a well-designed CLI looks like.")


if __name__ == "__main__":
    main()
