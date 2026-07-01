import csv
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
PROJECT_ID = "04_full_rpg"

SAVE_FILE = REPO_ROOT / "save_game.json"
LOG_FILE = REPO_ROOT / "combat_log.csv"


def _update_progress(status: str) -> None:
    import json as _json
    data = {}
    if PROGRESS_FILE.exists():
        data = _json.loads(PROGRESS_FILE.read_text())
    data.setdefault("projects", {})[PROJECT_ID] = status
    PROGRESS_FILE.write_text(_json.dumps(data, indent=2))


def main() -> None:
    result = subprocess.run(
        ["uv", "run", "python", "projects/04_full_rpg/rpg.py"],
        input="Ada\n",
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )

    assert result.returncode == 0, (
        f"rpg.py crashed — check your TODOs:\n{result.stderr}"
    )

    out = result.stdout
    assert "Ada" in out, "Hero name 'Ada' not found in output — did you create the Hero?"
    assert "Round 1" in out, "'Round 1' not in output — did you write the combat loop?"
    assert "wins" in out or "fallen" in out, (
        "'wins' or 'fallen' not in output — did you print the result?"
    )

    assert SAVE_FILE.exists(), (
        "save_game.json not found — did you add the json.dump() block?"
    )
    save_data = json.loads(SAVE_FILE.read_text())
    assert "name" in save_data, "save_game.json is missing the 'name' key"
    assert "hp" in save_data, "save_game.json is missing the 'hp' key"

    assert LOG_FILE.exists(), (
        "combat_log.csv not found — did you add the csv.writer() block?"
    )
    with open(LOG_FILE) as f:
        reader = csv.reader(f)
        rows = list(reader)
    assert rows[0] == ["round", "hero_hp", "boss_hp"], (
        f"CSV header wrong: expected ['round', 'hero_hp', 'boss_hp'], got {rows[0]}"
    )
    assert len(rows) >= 2, "combat_log.csv has no data rows — did the combat loop run?"

    _update_progress("complete")
    print("✅ Project 04 complete: Full Terminal RPG")
    print("   World 4 boss fight cleared! Part 2 coming soon.")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        _update_progress("in_progress")
        print(f"❌ Not quite: {e}")
        raise SystemExit(1)
    except Exception as e:
        _update_progress("in_progress")
        print(f"❌ Error: {e}")
        raise SystemExit(1)
