"""Check: Boss Fight — Installable CLI Tool."""

import json
import subprocess
import sys
from pathlib import Path

project_dir = Path(__file__).parent
task = project_dir / "task.py"
rpg_dir = project_dir / "rpg"
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


# ── domain purity check ───────────────────────────────────────────────────────

domain_src = (rpg_dir / "domain.py").read_text()
for forbidden in ("BaseModel", "from pydantic", "import typer", "from rich"):
    if forbidden in domain_src:
        print(f"❌ rpg/domain.py contains '{forbidden}' — domain must be pure dataclasses/enums")
        raise SystemExit(1)
print("✓ rpg/domain.py is pure (no Pydantic, no Typer, no Rich)")

# ── cli.py has app = typer.Typer(...) ────────────────────────────────────────

cli_src = (rpg_dir / "cli.py").read_text()
if "typer.Typer(" not in cli_src:
    print("❌ rpg/cli.py: typer.Typer(...) not found")
    raise SystemExit(1)
print("✓ rpg/cli.py has typer.Typer()")

for cmd in ("new-game", "play", "simulate", "report", "status"):
    if cmd not in cli_src:
        print(f"❌ rpg/cli.py: command '{cmd}' not found")
        raise SystemExit(1)
print("✓ All five commands present in cli.py")

# ── task.py --help does not crash ─────────────────────────────────────────────

result = subprocess.run(
    [sys.executable, str(task), "--help"],
    capture_output=True, text=True,
)
if result.returncode != 0:
    print(f"❌ task.py --help failed (exit {result.returncode}):")
    print(result.stderr)
    raise SystemExit(1)
help_text = result.stdout
for cmd in ("new-game", "simulate", "status"):
    if cmd not in help_text:
        print(f"❌ --help does not mention '{cmd}'")
        raise SystemExit(1)
print("✓ task.py --help works and lists commands")

# ── new-game command ──────────────────────────────────────────────────────────

result = subprocess.run(
    [sys.executable, str(task), "new-game", "--name", "CheckHero", "--class", "warrior"],
    capture_output=True, text=True, cwd=str(project_dir),
)
if result.returncode != 0:
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
    if "NotImplementedError" in stderr or "TODO" in stdout:
        print("⚠  new-game not yet implemented — skipping functional check")
    else:
        print(f"❌ new-game failed:\n{stdout}\n{stderr}")
        raise SystemExit(1)
elif "CheckHero" in result.stdout or "warrior" in result.stdout.lower():
    print("✓ new-game creates hero")
else:
    print("✓ new-game ran without error")

# ── schemas.py has SessionSummary and SaveGameModel ──────────────────────────

schemas_src = (rpg_dir / "schemas.py").read_text()
for cls in ("SessionSummary", "SaveGameModel"):
    if cls not in schemas_src:
        print(f"❌ rpg/schemas.py: {cls} not found")
        raise SystemExit(1)
print("✓ rpg/schemas.py has SaveGameModel and SessionSummary")

# ── output.py has the four functions ─────────────────────────────────────────

output_src = (rpg_dir / "output.py").read_text()
for fn in ("show_hero_stats", "show_combat_start", "show_combat_result", "show_error"):
    if fn not in output_src:
        print(f"❌ rpg/output.py: {fn}() not found")
        raise SystemExit(1)
print("✓ rpg/output.py has all four output functions")

# ── logging_setup.py has the three functions ──────────────────────────────────

log_src = (rpg_dir / "logging_setup.py").read_text()
for fn in ("setup_logging", "add_file_handler", "setup_log_files"):
    if fn not in log_src:
        print(f"❌ rpg/logging_setup.py: {fn}() not found")
        raise SystemExit(1)
print("✓ rpg/logging_setup.py has setup_logging, add_file_handler, setup_log_files")

# ── [project.scripts] required in pyproject.toml ─────────────────────────────

pyproject = Path(__file__).parents[3] / "pyproject.toml"
if not pyproject.exists():
    print("❌ pyproject.toml not found at repo root")
    raise SystemExit(1)
content = pyproject.read_text()
if "project.scripts" not in content or "rpg" not in content:
    print("❌ [project.scripts] with 'rpg' not found in pyproject.toml")
    print("   Add this to pyproject.toml and run 'uv sync':")
    print("   [project.scripts]")
    print("   rpg = \"rpg.cli:app\"")
    raise SystemExit(1)
print("✓ [project.scripts] with 'rpg' found in pyproject.toml")

# ── uv run rpg --help works ───────────────────────────────────────────────────

result = subprocess.run(
    ["uv", "run", "rpg", "--help"],
    capture_output=True, text=True,
    cwd=str(Path(__file__).parents[3]),
)
if result.returncode != 0:
    print("❌ 'uv run rpg --help' failed — run 'uv sync' first, then re-check")
    print(result.stderr)
    raise SystemExit(1)
uv_help = result.stdout + result.stderr
for cmd in ("new-game", "simulate", "status"):
    if cmd not in uv_help:
        print(f"❌ 'uv run rpg --help' does not mention '{cmd}'")
        raise SystemExit(1)
print("✓ 'uv run rpg --help' works and lists commands")

update_progress("01_installable_cli_tool")
print("\n✅ Boss fight structure verified!")
print("   Implement the TODO sections in rpg/game.py, rpg/cli.py, rpg/output.py,")
print("   rpg/logging_setup.py, and rpg/schemas.py to complete the boss fight.")
