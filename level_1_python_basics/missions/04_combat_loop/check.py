import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "04_combat_loop"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import task

    assert task.round_number == 4, (
        f"round_number: expected 4 rounds, got {task.round_number!r}\n"
        "  Tip: if check.py hangs, press Ctrl+C — your loop may run forever.\n"
        "  Make sure hero_hp and monster_hp decrease each round."
    )
    assert task.monster_hp == 0, (
        f"monster_hp: expected 0 after battle, got {task.monster_hp!r}"
    )
    assert task.hero_hp == 52, (
        f"hero_hp: expected 52 after 4 rounds of 12 damage, got {task.hero_hp!r}"
    )

    _update_progress("complete")
    print("✅ Mission 04 complete: Combat Loop")
    print("   Next mission: missions/05_arena_challenge/README.md")


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
