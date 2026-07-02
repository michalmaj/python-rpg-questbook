"""Check: Mission 08 — pre-commit."""

import json
import subprocess
from pathlib import Path

mission = Path(__file__).parent
config = mission / ".pre-commit-config.yaml"
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


# ── .pre-commit-config.yaml exists ───────────────────────────────────────────

if not config.exists():
    print("❌ .pre-commit-config.yaml not found in this mission folder")
    print("   Create it and add hooks for ruff (check + format) and mypy")
    raise SystemExit(1)
content = config.read_text()
print("✓ .pre-commit-config.yaml found")

# ── required structure ────────────────────────────────────────────────────────

required = {
    "repos:": "top-level 'repos:' key",
    "ruff": "ruff hook (ruff-pre-commit or ruff-check)",
    "ruff-format": "ruff-format hook",
    "mypy": "mypy hook",
    "rev:": "at least one pinned revision (rev:)",
}
for keyword, label in required.items():
    if keyword not in content:
        print(f"❌ {label} ({keyword!r}) not found in .pre-commit-config.yaml")
        raise SystemExit(1)
print("✓ .pre-commit-config.yaml has repos, ruff, ruff-format, mypy, pinned revs")

# ── pre-commit run --all-files passes ─────────────────────────────────────────

result = subprocess.run(
    ["pre-commit", "run", "--all-files", "--config", str(config)],
    capture_output=True, text=True, cwd=str(mission),
)
if result.returncode != 0:
    print("❌ pre-commit run --all-files fails:")
    print(result.stdout[-2000:])
    print(result.stderr[-500:])
    raise SystemExit(1)
print("✓ pre-commit run --all-files passes")

update_progress("08_pre_commit")
print("\n✅ Mission 08 complete!")
