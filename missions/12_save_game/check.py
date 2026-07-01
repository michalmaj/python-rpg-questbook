import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "12_save_game"
SAVE_FILE = REPO_ROOT / "save_game.json"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import task

    # Check the file was written
    assert SAVE_FILE.exists(), (
        "save_game.json not found — did you call json.dump() to write the file?"
    )

    saved = json.loads(SAVE_FILE.read_text())
    assert saved.get("name") == "Ada", (
        f'save_game.json: expected name="Ada", got {saved.get("name")!r}'
    )
    assert saved.get("hp") == 52, (
        f'save_game.json: expected hp=52, got {saved.get("hp")!r}'
    )
    assert saved.get("gold") == 75, (
        f'save_game.json: expected gold=75, got {saved.get("gold")!r}'
    )

    # Check the data was loaded back correctly
    assert task.loaded_hero is not None, (
        "loaded_hero is None — did you call json.load() to read the file back?"
    )
    assert task.loaded_hero.get("name") == "Ada", (
        f'loaded_hero["name"]: expected "Ada", got {task.loaded_hero.get("name")!r}'
    )
    assert task.loaded_hero.get("hp") == 52, (
        f'loaded_hero["hp"]: expected 52, got {task.loaded_hero.get("hp")!r}'
    )

    _update_progress("complete")
    print("✅ Mission 12 complete: Save Game")
    print("   Next mission: missions/13_split_the_game/README.md")


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
