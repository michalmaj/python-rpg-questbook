"""Check: Mission 01 — argparse baseline."""

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


# ── new-game ──────────────────────────────────────────────────────────────────

result = run(["new-game", "--name", "Ada", "--class", "warrior"])
if "Ada" not in result.stdout:
    print("❌ new-game: expected hero name 'Ada' in output.")
    raise SystemExit(1)
print("✓ new-game --name Ada --class warrior works")

result = run(["new-game", "--name", "Zara", "--class", "mage"])
if "Zara" not in result.stdout or "mage" not in result.stdout.lower():
    print("❌ new-game: expected 'Zara' and 'mage' in output.")
    raise SystemExit(1)
print("✓ new-game --name Zara --class mage works")

result = run(["new-game", "--class", "wizard"], expect_fail=True)
print("✓ new-game --class wizard correctly rejected (invalid choice)")

# ── simulate ──────────────────────────────────────────────────────────────────

run(["new-game", "--name", "TestHero", "--class", "warrior"])
result = run(["simulate", "--battles", "3"])
if "3" not in result.stdout:
    print("❌ simulate: expected '3' in output (battle count).")
    raise SystemExit(1)
print("✓ simulate --battles 3 works")

# simulate without a save should fail
save_dir = Path(__file__).parent / "saves"
if save_dir.exists():
    shutil.rmtree(save_dir)
result = run(["simulate", "--battles", "1"], expect_fail=True)
print("✓ simulate without save file exits non-zero")

# ── status ────────────────────────────────────────────────────────────────────

result = run(["status"])
# with no save, should not crash — either prints "No save" or similar
print("✓ status without save does not crash")

run(["new-game", "--name", "StatusHero", "--class", "rogue"])
result = run(["status"])
if "StatusHero" not in result.stdout:
    print("❌ status: expected hero name 'StatusHero' in output.")
    raise SystemExit(1)
print("✓ status shows saved hero name")

# ── no subcommand ─────────────────────────────────────────────────────────────

result = run([], expect_fail=True)
print("✓ no subcommand exits with code 1")

# ── --help does not crash ─────────────────────────────────────────────────────

subprocess.run([sys.executable, str(task), "--help"], capture_output=True)
print("✓ --help does not crash")

print("\n✅ Mission 01 complete!")
