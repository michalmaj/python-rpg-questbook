"""
Boss Fight: SQLite Repository Backend

Wire everything together. Show that swapping the backend is a one-line change
and the game logic doesn't need to know which backend is running.
"""

from pathlib import Path

from rpg.domain import Hero, HeroClass
from rpg.schemas import CombatLogRow
from rpg.log_repo import CsvCombatLogRepository, SqliteCombatLogRepository
from rpg.save_repo import JsonSaveRepository, SqliteSaveRepository

DB_PATH = Path(__file__).parent / "saves.db"
JSON_PATH = Path(__file__).parent / "save_game.json"
CSV_LOG = Path(__file__).parent / "combat_log.csv"


def run_demo(label: str, save_repo, log_repo) -> None:  # noqa: ANN001
    print(f"\n=== {label} ===")

    hero = Hero(
        name="Ada",
        hero_class=HeroClass.WARRIOR,
        hp=100,
        max_hp=120,
        atk=12,
        def_=4,
        potions=2,
        gold=0,
        wins=0,
        losses=0,
    )

    # Save
    save_repo.save(hero)
    print(f"  Saved {hero.name}")

    # Modify and save again
    hero.gold += 50
    hero.wins += 1
    save_repo.save(hero)

    # Load
    loaded = save_repo.load()
    assert loaded is not None
    print(f"  Loaded: {loaded.name}, gold={loaded.gold}, wins={loaded.wins}")

    # Log combat
    row = CombatLogRow(
        battle_id=1, turn=1,
        hero_name=hero.name, hero_class=hero.hero_class.value, monster="Goblin",
        action="attack", damage_dealt=12, damage_taken=4,
        hero_hp=96, monster_hp=18, result="ongoing",
    )
    log_repo.append(row)
    log_repo.append(row.model_copy(update={"turn": 2, "monster_hp": 0, "result": "win"}))

    rows = log_repo.read_all()
    print(f"  Logged {len(rows)} combat rows. Final result: {rows[-1].result}")


def main() -> None:
    # --- JSON backend ---
    run_demo(
        "JSON backend",
        save_repo=JsonSaveRepository(JSON_PATH),
        log_repo=CsvCombatLogRepository(CSV_LOG),
    )

    # --- SQLite backend ---
    # Swap here — game logic in run_demo() doesn't change.
    run_demo(
        "SQLite backend",
        save_repo=SqliteSaveRepository(DB_PATH),
        log_repo=SqliteCombatLogRepository(DB_PATH),
    )


if __name__ == "__main__":
    main()
