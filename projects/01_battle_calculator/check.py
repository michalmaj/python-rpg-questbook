import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
PROJECT_ID = "01_battle_calculator"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("projects", {})[PROJECT_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    from battle_calculator import (
        get_hero_stats,
        calculate_damage,
        calculate_healing,
        summarize_battle,
    )

    warrior = get_hero_stats("warrior")
    assert warrior is not None, 'get_hero_stats("warrior") returned None'
    assert warrior.get("class") == "Warrior", f'expected "Warrior", got {warrior.get("class")!r}'
    assert warrior.get("hp") == 120, f'warrior hp: expected 120, got {warrior.get("hp")}'
    assert warrior.get("damage") == 15, f'warrior damage: expected 15, got {warrior.get("damage")}'
    assert warrior.get("gold") == 50, f'warrior["gold"]: expected 50, got {warrior.get("gold")}'

    mage = get_hero_stats("mage")
    assert mage is not None, 'get_hero_stats("mage") returned None'
    assert mage.get("hp") == 80, f'mage hp: expected 80, got {mage.get("hp")}'
    assert mage.get("damage") == 25, f'mage damage: expected 25, got {mage.get("damage")}'

    rogue = get_hero_stats("rogue")
    assert rogue is not None, 'get_hero_stats("rogue") returned None'
    assert rogue.get("hp") == 100, f'rogue hp: expected 100, got {rogue.get("hp")}'

    assert get_hero_stats("wizard") is None, 'get_hero_stats("wizard") should return None'

    assert calculate_damage(100, 30) == 70, "calculate_damage(100, 30): expected 70"
    assert calculate_damage(20, 50) == 0, "calculate_damage(20, 50): HP cannot go below 0"

    assert calculate_healing(70, 20, 100) == 90, "calculate_healing(70, 20, 100): expected 90"
    assert calculate_healing(90, 20, 100) == 100, "calculate_healing(90, 20, 100): HP cannot exceed max_hp"

    alive = summarize_battle("Warrior", 65)
    assert "Warrior" in alive and "65" in alive, \
        'summarize_battle("Warrior", 65): should mention "Warrior" and "65"'

    fallen = summarize_battle("Mage", 0)
    assert "Mage" in fallen, 'summarize_battle("Mage", 0): should mention "Mage"'

    _update_progress("complete")
    print("✅ Project 01 complete: Battle Calculator")
    print("   World 1 is clear. Check your progress:")
    print("   uv run python tools/course_status.py")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        _update_progress("in_progress")
        print(f"❌ Not quite: {e}")
    except Exception as e:
        _update_progress("in_progress")
        print(f"❌ Error: {e}")
