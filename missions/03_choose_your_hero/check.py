import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "03_choose_your_hero"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    from task import choose_hero_class

    warrior = choose_hero_class("warrior")
    assert warrior is not None, 'choose_hero_class("warrior") returned None'
    assert warrior.get("class") == "Warrior", f'warrior["class"]: expected "Warrior", got {warrior.get("class")!r}'
    assert warrior.get("hp") == 120, f'warrior["hp"]: expected 120, got {warrior.get("hp")}'
    assert warrior.get("damage") == 15, f'warrior["damage"]: expected 15, got {warrior.get("damage")}'
    assert warrior.get("bonus") == "armor", f'warrior["bonus"]: expected "armor", got {warrior.get("bonus")!r}'

    mage = choose_hero_class("mage")
    assert mage is not None, 'choose_hero_class("mage") returned None'
    assert mage.get("class") == "Mage", f'mage["class"]: expected "Mage", got {mage.get("class")!r}'
    assert mage.get("hp") == 80, f'mage["hp"]: expected 80, got {mage.get("hp")}'
    assert mage.get("damage") == 25, f'mage["damage"]: expected 25, got {mage.get("damage")}'
    assert mage.get("bonus") == "spell", f'mage["bonus"]: expected "spell", got {mage.get("bonus")!r}'

    rogue = choose_hero_class("rogue")
    assert rogue is not None, 'choose_hero_class("rogue") returned None'
    assert rogue.get("class") == "Rogue", f'rogue["class"]: expected "Rogue", got {rogue.get("class")!r}'
    assert rogue.get("hp") == 100, f'rogue["hp"]: expected 100, got {rogue.get("hp")}'
    assert rogue.get("damage") == 20, f'rogue["damage"]: expected 20, got {rogue.get("damage")}'
    assert rogue.get("bonus") == "crit", f'rogue["bonus"]: expected "crit", got {rogue.get("bonus")!r}'

    unknown = choose_hero_class("wizard")
    assert unknown is None, 'choose_hero_class("wizard") should return None, not a dict'

    _update_progress("complete")
    print("✅ Mission 03 complete: Choose Your Hero")
    print("   Next up: projects/01_battle_calculator/README.md")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        _update_progress("in_progress")
        print(f"❌ Not quite: {e}")
    except Exception as e:
        _update_progress("in_progress")
        print(f"❌ Error: {e}")
