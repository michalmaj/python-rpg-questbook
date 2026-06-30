import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "01_hero_stats"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    from task import get_hero_stats

    stats = get_hero_stats()

    assert isinstance(stats, dict), "get_hero_stats() must return a dict, not None or pass"
    assert stats.get("name") == "Ada", f'name: expected "Ada", got {stats.get("name")!r}'
    assert stats.get("hp") == 100, f"hp: expected 100, got {stats.get('hp')!r}"
    assert stats.get("damage") == 15, f"damage: expected 15, got {stats.get('damage')!r}"
    assert stats.get("gold") == 50, f"gold: expected 50, got {stats.get('gold')!r}"

    _update_progress("complete")
    print("✅ Mission 01 complete: Hero Stats")
    print("   Next mission: missions/02_damage_and_healing/README.md")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        _update_progress("in_progress")
        print(f"❌ Not quite: {e}")
    except Exception as e:
        _update_progress("in_progress")
        print(f"❌ Error: {e}")
