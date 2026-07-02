"""Check: Boss Fight — Full Release Pipeline."""

import json
import re
import subprocess
import sys
from pathlib import Path

project = Path(__file__).parent
pyproject = project / "pyproject.toml"
precommit = project / ".pre-commit-config.yaml"
ci_yml = project / ".github" / "workflows" / "ci.yml"
changelog = project / "CHANGELOG.md"
tests_dir = project / "tests"
rpg_py = project / "rpg.py"
PROGRESS_FILE = Path(__file__).parents[2] / ".progress"


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


print("Checking boss fight: full_release_pipeline")
print("=" * 50)

# ── pyproject.toml ────────────────────────────────────────────────────────────

if not pyproject.exists():
    print("❌ pyproject.toml not found — create it with all tool configs")
    raise SystemExit(1)
pycontent = pyproject.read_text()
for section in ("[tool.ruff]", "[tool.mypy]", "[tool.pyright]", "[tool.coverage"):
    if section not in pycontent:
        print(f"❌ {section} missing from pyproject.toml")
        raise SystemExit(1)
print("✓ pyproject.toml has all required tool sections")

# ── .pre-commit-config.yaml ───────────────────────────────────────────────────

if not precommit.exists():
    print("❌ .pre-commit-config.yaml not found")
    raise SystemExit(1)
pre_content = precommit.read_text()
for kw in ("ruff", "ruff-format", "mypy", "repos:"):
    if kw not in pre_content:
        print(f"❌ '{kw}' not found in .pre-commit-config.yaml")
        raise SystemExit(1)
print("✓ .pre-commit-config.yaml has ruff, ruff-format, mypy hooks")

# ── .github/workflows/ci.yml ─────────────────────────────────────────────────

if not ci_yml.exists():
    print("❌ .github/workflows/ci.yml not found")
    raise SystemExit(1)
ci_content = ci_yml.read_text()
for kw in ("ruff", "mypy", "pytest", "uv", "3.12", "3.13"):
    if kw not in ci_content:
        print(f"❌ '{kw}' not found in ci.yml")
        raise SystemExit(1)
print("✓ .github/workflows/ci.yml has ruff, mypy, pytest, uv, matrix [3.12, 3.13]")

# ── CHANGELOG.md ─────────────────────────────────────────────────────────────

if not changelog.exists():
    print("❌ CHANGELOG.md not found")
    raise SystemExit(1)
if "1.0.0" not in changelog.read_text():
    print("❌ [1.0.0] not found in CHANGELOG.md — add a version 1.0.0 section")
    raise SystemExit(1)
print("✓ CHANGELOG.md has 1.0.0 section")

# ── ruff check passes ─────────────────────────────────────────────────────────

result = subprocess.run(
    [sys.executable, "-m", "ruff", "check", str(rpg_py),
     "--config", str(pyproject)],
    capture_output=True, text=True,
)
if result.returncode != 0:
    print("❌ ruff check fails:")
    print(result.stdout)
    raise SystemExit(1)
print("✓ ruff check passes")

# ── mypy --strict passes ──────────────────────────────────────────────────────

result = subprocess.run(
    [sys.executable, "-m", "mypy", str(rpg_py), "--strict",
     "--config-file", str(pyproject)],
    capture_output=True, text=True,
)
if result.returncode != 0:
    print("❌ mypy --strict fails:")
    print(result.stdout[-2000:])
    raise SystemExit(1)
print("✓ mypy --strict passes")

# ── tests exist and pass ──────────────────────────────────────────────────────

if not tests_dir.exists() or not list(tests_dir.glob("test_*.py")):
    print("❌ tests/ directory not found or has no test_*.py files")
    raise SystemExit(1)
result = subprocess.run(
    [sys.executable, "-m", "pytest", str(tests_dir), "-q", "--tb=short"],
    capture_output=True, text=True, cwd=str(project),
)
if result.returncode != 0:
    print("❌ pytest fails:")
    print(result.stdout[-2000:])
    raise SystemExit(1)
print("✓ All tests pass")

# ── coverage ≥ 80% on rpg.py ─────────────────────────────────────────────────

cov_result = subprocess.run(
    [sys.executable, "-m", "pytest", str(tests_dir),
     "--cov=rpg", "--cov-report=term-missing", "-q"],
    capture_output=True, text=True, cwd=str(project),
)
cov_output = cov_result.stdout + cov_result.stderr
match = re.search(r"rpg\.py\s+\d+\s+\d+\s+(\d+)%", cov_output)
if not match:
    print("❌ Could not determine coverage for rpg.py")
    print(cov_output[-1000:])
    raise SystemExit(1)
pct = int(match.group(1))
if pct < 80:
    print(f"❌ Coverage for rpg.py is {pct}% (need ≥ 80%)")
    raise SystemExit(1)
print(f"✓ Coverage for rpg.py: {pct}%")

update_progress("01_full_release_pipeline")
print()
print("✅ Boss fight complete!")
print("   Your project has: ruff ✓  mypy ✓  pyright config ✓")
print("   pre-commit ✓  CI ✓  tests ✓  coverage ✓  CHANGELOG ✓")
print()
print("   Final step: push your branch, open a PR, and confirm the CI badge goes green.")
print("   Then create a git tag: git tag v1.0.0 && git push origin v1.0.0")
