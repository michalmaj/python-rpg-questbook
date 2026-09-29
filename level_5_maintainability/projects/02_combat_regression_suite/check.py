"""check.py — Project 02: Combat Regression Suite"""

import ast
import json
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
TEST_FILE = PROJECT_DIR / "tests" / "test_combat.py"
COMBAT_FILE = PROJECT_DIR / "rpg" / "combat.py"
PROGRESS_FILE = Path(__file__).parents[3] / "level_5_maintainability" / ".progress"


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


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(PROJECT_DIR))


def count_decorator(source: str, decorator_name: str) -> int:
    """Count @pytest.mark.<name> or @pytest.fixture decorators in source."""
    tree = ast.parse(source)
    count = 0
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for dec in node.decorator_list:
            dec_str = ast.unparse(dec)
            if decorator_name in dec_str:
                count += 1
    return count


def has_xfail_on_compute_damage(source: str) -> bool:
    """Return True if an xfail-decorated test calls compute_damage with low atk."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        is_xfail = any(
            "xfail" in ast.unparse(d) for d in node.decorator_list
        )
        if not is_xfail:
            continue
        # Check if compute_damage is called inside this function
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                func = child.func
                name = (
                    func.attr if isinstance(func, ast.Attribute) else
                    func.id if isinstance(func, ast.Name) else ""
                )
                if name == "compute_damage":
                    return True
    return False


def main() -> None:
    # ── 1. test file exists ───────────────────────────────────────────────────
    if not TEST_FILE.exists():
        print("❌ tests/test_combat.py not found")
        raise SystemExit(1)
    source = TEST_FILE.read_text(encoding="utf-8")

    # ── 2. pytest passes (xfail counts as pass) ───────────────────────────────
    result = run([sys.executable, "-m", "pytest", "tests/test_combat.py", "-v",
                  "--tb=short"])
    if result.returncode != 0:
        print("❌ pytest tests/test_combat.py failed:")
        print(result.stdout[-2000:])
        raise SystemExit(1)
    print("✓ pytest tests/test_combat.py — all tests pass (xfail counts as pass)")

    # ── 3. Coverage ≥85% ─────────────────────────────────────────────────────
    result = run([sys.executable, "-m", "pytest", "tests/test_combat.py",
                  "--cov=rpg", "--cov-report=term-missing", "-q"])
    output = result.stdout + result.stderr
    # Parse coverage percentage from output
    cov_pct: int | None = None
    for line in output.splitlines():
        if "rpg/combat" in line or "rpg\\combat" in line:
            parts = line.split()
            for part in parts:
                if part.endswith("%"):
                    try:
                        cov_pct = int(part.rstrip("%"))
                    except ValueError:
                        pass
    if cov_pct is None:
        # Try total line
        for line in output.splitlines():
            if line.strip().startswith("TOTAL"):
                parts = line.split()
                for part in parts:
                    if part.endswith("%"):
                        try:
                            cov_pct = int(part.rstrip("%"))
                        except ValueError:
                            pass
    if cov_pct is None:
        print("❌ Could not parse coverage — make sure pytest-cov is installed (uv add --dev pytest-cov)")
        raise SystemExit(1)
    elif cov_pct < 85:
        print(f"❌ Coverage is {cov_pct}% — must be ≥85%")
        print("   Add more parametrized tests to cover edge cases.")
        raise SystemExit(1)
    else:
        print(f"✓ Coverage: {cov_pct}% (≥85%)")

    # ── 4. ≥1 @pytest.mark.parametrize used to cover multiple cases ──────────
    n_param = count_decorator(source, "parametrize")
    if n_param < 1:
        print(f"❌ Need at least 1 @pytest.mark.parametrize to cover multiple cases, found {n_param}")
        raise SystemExit(1)
    print(f"✓ {n_param} @pytest.mark.parametrize use(s)")

    # ── 5. ≥1 @pytest.fixture definition ─────────────────────────────────────
    n_fixture = count_decorator(source, "fixture")
    if n_fixture < 1:
        print(f"❌ Need at least 1 @pytest.fixture definition, found {n_fixture}")
        raise SystemExit(1)
    print(f"✓ {n_fixture} @pytest.fixture definition(s)")

    # ── 6. ≥1 @pytest.mark.xfail(strict=True) that calls compute_damage ──────
    # (cheap structural pre-check — the real proof is behavioral, below)
    if not has_xfail_on_compute_damage(source):
        print("❌ Need ≥1 @pytest.mark.xfail test that calls compute_damage()")
        print("   The bug: compute_damage(1, 0, 10) returns 0 instead of 1.")
        print("   Write a test asserting == 1, mark it xfail(strict=True) so pytest exits 0.")
        raise SystemExit(1)
    if "strict=True" not in source and 'strict = True' not in source:
        print("❌ xfail must use strict=True: @pytest.mark.xfail(strict=True, reason=...)")
        print("   strict=True means: if the bug is accidentally fixed, pytest fails loudly.")
        raise SystemExit(1)
    print("✓ xfail(strict=True) test found, calling compute_damage()")

    # ── 7. The xfail test must document the REAL bug, not just any failure ───
    #
    # An xfail(strict=True) test that asserts something unrelated (e.g.
    # compute_damage(1, 0, 10) == 999999) still "passes" the checks above —
    # it fails today for the wrong reason, and would keep silently "passing"
    # (as XFAIL) forever, even after someone fixes the real bug, since a
    # wrong expected value never becomes true. The only way to tell a test
    # that tracks the *real* documented bug from one that doesn't is to fix
    # the real bug and see whether the test flips to XPASS.
    if not COMBAT_FILE.exists():
        print("❌ rpg/combat.py not found")
        raise SystemExit(1)
    original_combat_src = COMBAT_FILE.read_text()
    buggy_line = "return max(atk + bonus - def_, 0)"
    fixed_line = "return max(atk + bonus - def_, 1)"
    if buggy_line not in original_combat_src:
        print("❌ internal check error: expected buggy line not found in rpg/combat.py "
              "— has the file been modified? It should not be.")
        raise SystemExit(1)

    try:
        COMBAT_FILE.write_text(original_combat_src.replace(buggy_line, fixed_line, 1))
        shutil.rmtree(PROJECT_DIR / "tests" / "__pycache__", ignore_errors=True)
        shutil.rmtree(PROJECT_DIR / "rpg" / "__pycache__", ignore_errors=True)
        fixed_result = run([sys.executable, "-m", "pytest", "tests/test_combat.py",
                            "-v", "--tb=line"])
        shutil.rmtree(PROJECT_DIR / "tests" / "__pycache__", ignore_errors=True)
        shutil.rmtree(PROJECT_DIR / "rpg" / "__pycache__", ignore_errors=True)
    finally:
        COMBAT_FILE.write_text(original_combat_src)

    if COMBAT_FILE.read_text() != original_combat_src:
        print("❌ internal check error: rpg/combat.py was not restored correctly — please re-run")
        raise SystemExit(1)

    if fixed_result.returncode == 0:
        print("❌ Your xfail test still doesn't fail (as XPASS) once the real bug is "
              "fixed — it isn't asserting the actual documented behavior "
              "(compute_damage(1, 0, 10) == 1). Update the assertion to match the "
              "real bug, not an arbitrary failing value.")
        raise SystemExit(1)
    if "XPASS" not in fixed_result.stdout:
        print("❌ pytest failed once the bug was fixed, but not via the expected "
              "XPASS(strict) on your xfail test — something else broke:")
        print(fixed_result.stdout[-1500:])
        raise SystemExit(1)
    print("✓ xfail test correctly flips to XPASS (and fails the suite, via "
          "strict=True) once the real bug is fixed — it documents the actual bug")

    # ── Done ──────────────────────────────────────────────────────────────────
    update_progress("02_combat_regression_suite")
    print()
    print("✅ Project 02 complete: Combat Regression Suite!")
    print()
    print("   85%+ coverage. The hidden bug is documented, not hidden.")
    print("   xfail = 'we know about this, it's tracked' — not 'we gave up'.")


if __name__ == "__main__":
    main()
