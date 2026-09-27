import sys
import csv
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]  # level_1_python_basics/, not the git repo root
PROGRESS_FILE = REPO_ROOT / ".progress"
PROJECT_ID = "04_full_rpg"

SAVE_FILE = REPO_ROOT / "save_game.json"
LOG_FILE = REPO_ROOT / "combat_log.csv"

# Ground truth mirrors the class table in rpg.py's TODO 1 — used to verify
# the saved class/hp pairing is real, and to bound each round's damage.
CLASS_STATS = {
    "Warrior": {"hp": 120, "damage_min": 10, "damage_max": 20},
    "Mage": {"hp": 80, "damage_min": 18, "damage_max": 28},
    "Rogue": {"hp": 100, "damage_min": 14, "damage_max": 24},
}
BOSS_DAMAGE_MIN, BOSS_DAMAGE_MAX = 12, 20


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("projects", {})[PROJECT_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    result = subprocess.run(
        [sys.executable, "projects/04_full_rpg/rpg.py"],
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
    assert "wins" in out.lower() or "fallen" in out.lower() or "defeated" in out.lower(), (
        "Expected a result message (win/loss) in the output — did you print TODO 3?"
    )

    # ── save_game.json: real values, not just the right keys ──
    assert SAVE_FILE.exists(), "save_game.json not found — did you add the json.dump() block?"
    save_data = json.loads(SAVE_FILE.read_text())
    for key in ("name", "class", "hp", "max_hp"):
        assert key in save_data, f"save_game.json is missing the '{key}' key"

    assert save_data["name"] == "Ada", f"save_game.json: expected name='Ada', got {save_data['name']!r}"

    hero_class = save_data["class"]
    assert hero_class in CLASS_STATS, (
        f"save_game.json: class {hero_class!r} doesn't match any of the three real classes "
        f"({list(CLASS_STATS)}) — is TODO 1 using the exact stats from the README?"
    )
    expected_max_hp = CLASS_STATS[hero_class]["hp"]
    assert save_data["max_hp"] == expected_max_hp, (
        f"save_game.json: {hero_class} should have max_hp={expected_max_hp}, "
        f"got {save_data['max_hp']} — hp/class/max_hp must be a real, matching triple"
    )
    assert 0 <= save_data["hp"] <= save_data["max_hp"], (
        f"save_game.json: hp={save_data['hp']} is not between 0 and max_hp={save_data['max_hp']}"
    )

    # ── combat_log.csv: real rows, not just a header ──
    assert LOG_FILE.exists(), "combat_log.csv not found — did you add the csv.writer() block?"
    with open(LOG_FILE) as f:
        rows = list(csv.reader(f))
    assert rows[0] == ["round", "hero_hp", "boss_hp"], (
        f"CSV header wrong: expected ['round', 'hero_hp', 'boss_hp'], got {rows[0]}"
    )
    data_rows = rows[1:]
    assert len(data_rows) >= 2, (
        f"combat_log.csv has {len(data_rows)} data row(s) — a 150 HP boss should take "
        "more than one round even in the best case; is the combat loop actually running?"
    )

    parsed = [(int(r), int(hp), int(bhp)) for r, hp, bhp in data_rows]
    assert [p[0] for p in parsed] == list(range(1, len(parsed) + 1)), (
        f"combat_log.csv: round numbers should be 1, 2, 3, ... in order, got {[p[0] for p in parsed]}"
    )

    # Note: apply_damage floors at 0, so a killing blow can produce a delta
    # smaller than the attacker's own minimum damage (e.g. a 15-HP boss hit
    # by an 18-damage roll only "loses" 15). Deltas are validated with that
    # in mind: an exact-range check only when the target survived the round.
    hero_dmg_min = CLASS_STATS[hero_class]["damage_min"]
    hero_dmg_max = CLASS_STATS[hero_class]["damage_max"]
    prev_hero_hp, prev_boss_hp = expected_max_hp, 150
    for round_num, hero_hp, boss_hp in parsed:
        boss_delta = prev_boss_hp - boss_hp
        if boss_hp == 0:
            assert prev_boss_hp <= hero_dmg_max, (
                f"combat_log.csv round {round_num}: boss_hp dropped to 0 from {prev_boss_hp}, "
                f"but {hero_class} can only deal up to {hero_dmg_max} damage per hit"
            )
        else:
            assert hero_dmg_min <= boss_delta <= hero_dmg_max, (
                f"combat_log.csv round {round_num}: boss_hp dropped by {boss_delta}, "
                f"expected between {hero_dmg_min} and {hero_dmg_max} ({hero_class}'s damage "
                "range) — is roll_damage(hero.damage_min, hero.damage_max) actually being used?"
            )

        hero_delta = prev_hero_hp - hero_hp
        if hero_delta == 0:
            assert boss_hp <= 0, (
                f"combat_log.csv round {round_num}: hero_hp is unchanged but the boss "
                f"({boss_hp} HP) is still alive — a live boss should always attack back"
            )
        elif hero_hp == 0:
            assert prev_hero_hp <= BOSS_DAMAGE_MAX, (
                f"combat_log.csv round {round_num}: hero_hp dropped to 0 from {prev_hero_hp}, "
                f"but the boss can only deal up to {BOSS_DAMAGE_MAX} damage per hit"
            )
        else:
            assert BOSS_DAMAGE_MIN <= hero_delta <= BOSS_DAMAGE_MAX, (
                f"combat_log.csv round {round_num}: hero_hp dropped by {hero_delta}, "
                f"expected between {BOSS_DAMAGE_MIN} and {BOSS_DAMAGE_MAX} (the boss's damage range)"
            )
        prev_hero_hp, prev_boss_hp = hero_hp, boss_hp

    final_round_hero_hp, final_round_boss_hp = parsed[-1][1], parsed[-1][2]
    assert final_round_hero_hp <= 0 or final_round_boss_hp <= 0, (
        f"combat_log.csv: the fight ended (round {parsed[-1][0]}) without either side "
        f"reaching 0 HP (hero_hp={final_round_hero_hp}, boss_hp={final_round_boss_hp})"
    )

    # ── Cross-check: the saved JSON must match the CSV's own final row ──
    assert save_data["hp"] == final_round_hero_hp, (
        f"save_game.json hp={save_data['hp']} doesn't match combat_log.csv's final "
        f"hero_hp={final_round_hero_hp} — both should describe the same finished game"
    )

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
