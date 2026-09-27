import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
PROJECT_ID = "02_turn_based_combat"
PROJECT_DIR = Path(__file__).parent

sys.path.insert(0, str(PROJECT_DIR))


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("projects", {})[PROJECT_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import task

    # ── Unit tests on fight_enemy() with controlled, deterministic inputs ──
    # These don't depend on the hardcoded arena data at all — they prove the
    # combat rule itself is correct, not just that one hardcoded run "looks right."

    # 1) Straightforward kill: hero deals enough to win before taking a fatal hit.
    hp, rounds, won = task.fight_enemy(
        hero_hp=100, enemy_name="Test", enemy_hp=30, enemy_attack=8,
        hero_attack=20, potions=[30, 30, 30],
    )
    assert won is True, f"fight_enemy: hero should win (30 HP enemy vs 20 dmg/round), got won={won}"
    assert rounds == 2, f"fight_enemy: expected 2 rounds (30 -> 10 -> dead), got {rounds}"
    assert hp == 92, (
        f"fight_enemy: expected hero_hp=92 (100 - 8 from round 1 only; the enemy dies in "
        f"round 2 before attacking back), got {hp}"
    )

    # 2) Healing must actually trigger, change HP, and consume a potion.
    potions = [30]
    hp, rounds, won = task.fight_enemy(
        hero_hp=50, enemy_name="Test", enemy_hp=25, enemy_attack=16,
        hero_attack=20, potions=potions,
    )
    assert won is True, f"fight_enemy: hero should win this fight, got won={won}"
    assert rounds == 2, f"fight_enemy: expected 2 rounds, got {rounds}"
    assert len(potions) == 0, (
        f"fight_enemy: hero_hp should have dropped below the heal threshold and used "
        f"the potion (list should be empty afterward), got {len(potions)} potion(s) left"
    )
    assert hp == 64, (
        f"fight_enemy: expected hero_hp=64 (50 - 16 = 34, heal +30 = 64), got {hp} — "
        "is the potion's value actually being added to hero_hp?"
    )

    # 3) Hero can lose, and HP must never go negative.
    hp, rounds, won = task.fight_enemy(
        hero_hp=10, enemy_name="Test", enemy_hp=1000, enemy_attack=50,
        hero_attack=1, potions=[],
    )
    assert won is False, f"fight_enemy: hero should lose (1 dmg vs 1000 HP enemy), got won={won}"
    assert hp == 0, f"fight_enemy: HP should floor at 0, not go negative, got {hp}"
    assert rounds == 1, f"fight_enemy: expected 1 round before the hero fell, got {rounds}"

    # ── Integration test: run_arena() with fresh, independent state ──
    # Verifies the outer wiring (looping over enemies, building battle_log,
    # decrementing potions) matches the real outcome — not just that some
    # expected words appear in stdout.
    hero_hp, battle_log = task.run_arena(
        hero_name="Ada", hero_hp=100, hero_attack=20,
        enemies=[["Wolf", 30, 8], ["Orc Warrior", 55, 13], ["Dragon King", 90, 20]],
        potions=[30, 30, 30],
    )
    assert hero_hp == 46, (
        f"run_arena: expected the hero to finish with 46 HP after all three fights, got {hero_hp}"
    )
    assert battle_log == [
        "Defeated Wolf in 2 rounds",
        "Defeated Orc Warrior in 3 rounds",
        "Defeated Dragon King in 5 rounds",
    ], f"run_arena: battle_log doesn't match the expected outcome, got {battle_log}"

    # ── A losing run must also produce a truthful log, not a hardcoded win ──
    lose_hp, lose_log = task.run_arena(
        hero_name="Doomed", hero_hp=10, hero_attack=1,
        enemies=[["Overwhelming Beast", 1000, 50]],
        potions=[],
    )
    assert lose_hp == 0, f"run_arena: expected the hero to fall (0 HP), got {lose_hp}"
    assert lose_log == ["Fell to Overwhelming Beast"], (
        f"run_arena: a losing fight should log 'Fell to ...', got {lose_log}"
    )

    _update_progress("complete")
    print("✅ Project 02 complete: Turn-Based Combat Arena")
    print()
    print("   for loop, while loop, lists — all three in one fight.")
    print()
    print("   World 2 is clear! Check your progress:")
    print("   uv run python tools/course_status.py")


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
