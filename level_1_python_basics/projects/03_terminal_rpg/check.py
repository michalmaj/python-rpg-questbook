import random
import sys
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
PROJECT_ID = "03_terminal_rpg"
PROJECT_DIR = Path(__file__).parent

sys.path.insert(0, str(PROJECT_DIR))

GOBLIN_KING = {"name": "Goblin King", "hp": 80, "min_dmg": 8, "max_dmg": 15}


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("projects", {})[PROJECT_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import rpg

    # ── roll_damage: bounds hold across many rolls, not just one lucky call ──
    for _ in range(200):
        r = rpg.roll_damage(10, 20)
        assert 10 <= r <= 20, f"roll_damage(10, 20) produced {r}, outside [10, 20]"

    # ── create_hero: exact stats per class, and None for unknown ──
    expected_heroes = {
        "warrior": {"name": "Warrior", "hp": 120, "min_dmg": 10, "max_dmg": 20},
        "mage": {"name": "Mage", "hp": 80, "min_dmg": 18, "max_dmg": 28},
        "rogue": {"name": "Rogue", "hp": 100, "min_dmg": 14, "max_dmg": 24},
    }
    for hero_class, expected in expected_heroes.items():
        hero = rpg.create_hero(hero_class)
        assert hero == expected, f"create_hero({hero_class!r}) should be {expected}, got {hero}"
    assert rpg.create_hero("bard") is None, "create_hero('bard') should return None for an unknown class"

    # ── run_battle: a deterministic edge case (no randomness involved) ──
    # min_dmg == max_dmg removes the RNG entirely, so this must hold exactly.
    titan = {"name": "Titan", "hp": 1000, "min_dmg": 100, "max_dmg": 100}
    slime = {"name": "Slime", "hp": 10, "min_dmg": 0, "max_dmg": 0}
    hero_hp, monster_hp, rounds = rpg.run_battle(titan, slime)
    assert monster_hp <= 0, f"a one-shot-kill hero should defeat the monster, got monster_hp={monster_hp}"
    assert hero_hp == 1000, f"a monster dealing 0 damage should never hurt the hero, got hero_hp={hero_hp}"
    assert rounds == 1, f"expected exactly 1 round for a one-shot kill, got {rounds}"

    # ── run_battle: self-consistent outcomes across many seeded runs ──
    # Seeding random makes each run reproducible without hardcoding exact
    # numbers pulled from a specific RNG sequence.
    for seed in range(20):
        random.seed(seed)
        hero = rpg.create_hero("warrior")
        hero_hp, monster_hp, rounds = rpg.run_battle(hero, dict(GOBLIN_KING))
        assert 0 <= hero_hp <= 120, f"seed={seed}: hero_hp out of range: {hero_hp}"
        assert 0 <= monster_hp <= 80, f"seed={seed}: monster_hp out of range: {monster_hp}"
        assert rounds >= 1, f"seed={seed}: a battle should take at least 1 round"
        assert hero_hp <= 0 or monster_hp <= 0, (
            f"seed={seed}: battle ended with both sides still alive "
            f"(hero_hp={hero_hp}, monster_hp={monster_hp}) — check the while loop condition"
        )

    # ── UX smoke test: the interactive CLI wiring works end to end ──
    # A light substring check — not the main evidence, just confirms
    # input() -> create_hero -> run_battle -> print is actually wired up.
    def run_cli(hero_class: str) -> str:
        result = subprocess.run(
            [sys.executable, "rpg.py"],
            input=hero_class + "\n",
            capture_output=True,
            text=True,
            cwd=PROJECT_DIR,
        )
        return result.stdout

    out = run_cli("warrior")
    assert "Warrior" in out, f"warrior: expected 'Warrior' in CLI output\n{out}"
    assert "wins" in out.lower() or "fallen" in out.lower(), (
        f"warrior: expected an ending message in CLI output\n{out}"
    )

    out = run_cli("dragon")
    assert "unknown" in out.lower() or "dragon" in out.lower(), (
        f"unknown class: expected an error message in CLI output\n{out}"
    )

    _update_progress("complete")
    print("✅ Project 03 complete: Terminal RPG")
    print("\n   World 3 is clear! Check your progress:")
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
