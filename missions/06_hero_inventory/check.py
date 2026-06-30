import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "06_hero_inventory"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import task

    assert len(task.inventory) == 5, (
        f"inventory: expected 5 items, got {len(task.inventory)} — "
        f"did you append all three new items?"
    )
    assert "sword" in task.inventory, '"sword" should still be in inventory'
    assert "health potion" in task.inventory, '"health potion" should still be in inventory'
    assert "shield" in task.inventory, '"shield" not found — use inventory.append("shield")'
    assert "magic scroll" in task.inventory, '"magic scroll" not found — use inventory.append("magic scroll")'
    assert "gold coin" in task.inventory, '"gold coin" not found — use inventory.append("gold coin")'

    _update_progress("complete")
    print("✅ Mission 06 complete: Hero Inventory")
    print("   Next mission: missions/07_monster_dictionary/README.md")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        _update_progress("in_progress")
        print(f"❌ Not quite: {e}")
    except Exception as e:
        _update_progress("in_progress")
        print(f"❌ Error: {e}")
