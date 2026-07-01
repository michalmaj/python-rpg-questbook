"""Check: Mission 02 — Typer CLI."""

import shutil
import subprocess
import sys
from pathlib import Path

task = Path(__file__).parent / "task.py"


def run(args: list[str], *, expect_fail: bool = False) -> subprocess.CompletedProcess:
    result = subprocess.run(
        [sys.executable, str(task)] + args,
        capture_output=True, text=True,
    )
    if expect_fail and result.returncode == 0:
        print(f"❌ Expected non-zero exit for args {args}, but got 0.")
        raise SystemExit(1)
    if not expect_fail and result.returncode != 0:
        print(f"❌ Command failed (exit {result.returncode}) for args {args}:")
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(1)
    return result


# ── verify app = typer.Typer() exists ────────────────────────────────────────

task_src = task.read_text()
if "typer.Typer()" not in task_src:
    print("❌ app = typer.Typer() not found in task.py")
    raise SystemExit(1)
print("✓ typer.Typer() present")

if "app()" not in task_src:
    print("❌ app() call not found — add `if __name__ == '__main__': app()`")
    raise SystemExit(1)
print("✓ app() entry point present")

# ── new-game ──────────────────────────────────────────────────────────────────

result = run(["new-game", "--name", "Ada", "--class", "warrior"])
if "Ada" not in result.stdout:
    print("❌ new-game: expected hero name 'Ada' in output.")
    raise SystemExit(1)
print("✓ new-game --name Ada --class warrior works")

result = run(["new-game", "--name", "Zara", "--class", "mage"])
if "Zara" not in result.stdout:
    print("❌ new-game: expected 'Zara' in output.")
    raise SystemExit(1)
print("✓ new-game --name Zara --class mage works")

result = run(["new-game", "--class", "wizard"], expect_fail=True)
print("✓ new-game --class wizard correctly rejected")

# ── simulate ──────────────────────────────────────────────────────────────────

run(["new-game", "--name", "TestHero", "--class", "warrior"])
result = run(["simulate", "--battles", "3"])
if "3" not in result.stdout:
    print("❌ simulate: expected '3' in output.")
    raise SystemExit(1)
print("✓ simulate --battles 3 works")

save_dir = Path(__file__).parent / "saves"
if save_dir.exists():
    shutil.rmtree(save_dir)
run(["simulate", "--battles", "1"], expect_fail=True)
print("✓ simulate without save exits non-zero")

# ── status ────────────────────────────────────────────────────────────────────

run(["status"])
print("✓ status without save does not crash")

run(["new-game", "--name", "StatusHero", "--class", "rogue"])
result = run(["status"])
if "StatusHero" not in result.stdout:
    print("❌ status: expected 'StatusHero' in output.")
    raise SystemExit(1)
print("✓ status shows saved hero name")

# ── --help ────────────────────────────────────────────────────────────────────

result = subprocess.run(
    [sys.executable, str(task), "--help"], capture_output=True, text=True,
)
help_text = result.stdout + result.stderr
for cmd in ("new-game", "simulate", "status"):
    if cmd not in help_text:
        print(f"❌ --help does not mention '{cmd}'")
        raise SystemExit(1)
print("✓ --help lists all three commands")

# ── no argparse ───────────────────────────────────────────────────────────────

if "import argparse" in task_src:
    print("❌ task.py imports argparse — use Typer only.")
    raise SystemExit(1)
print("✓ no argparse import")

print("\n✅ Mission 02 complete!")
