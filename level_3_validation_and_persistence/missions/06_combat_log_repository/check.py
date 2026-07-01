"""check.py — Mission 06: Combat Log Repository"""

import json
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).parents[3]
PROGRESS_FILE = REPO_ROOT / "level_3_validation_and_persistence" / ".progress"


def update_progress(mission_id: str) -> None:
    progress: dict = {"missions": {}, "projects": {}}
    if PROGRESS_FILE.exists():
        try:
            progress = json.loads(PROGRESS_FILE.read_text())
        except json.JSONDecodeError:
            pass
    progress["missions"][mission_id] = "complete"
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


def main() -> None:
    task_path = Path(__file__).parent / "task.py"

    import importlib.util
    spec = importlib.util.spec_from_file_location("task", task_path)
    task = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    try:
        spec.loader.exec_module(task)  # type: ignore[union-attr]
    except Exception as e:
        print(f"❌ Could not import task.py: {e}")
        raise SystemExit(1)

    CombatLogRow = getattr(task, "CombatLogRow", None)
    CsvCombatLogRepository = getattr(task, "CsvCombatLogRepository", None)
    InMemoryCombatLogRepository = getattr(task, "InMemoryCombatLogRepository", None)

    for name, obj in [("CombatLogRow", CombatLogRow),
                      ("CsvCombatLogRepository", CsvCombatLogRepository),
                      ("InMemoryCombatLogRepository", InMemoryCombatLogRepository)]:
        if obj is None:
            print(f"❌ {name} not found in task.py.")
            raise SystemExit(1)

    # Build a valid row
    row = CombatLogRow(
        battle_id=1, turn=1,
        hero_name="Ada", hero_class="warrior", monster="Goblin",
        action="attack", damage_dealt=12, damage_taken=4,
        hero_hp=96, monster_hp=18, result="ongoing",
    )

    # CombatLogRow validation
    try:
        CombatLogRow(
            battle_id=0, turn=1,  # battle_id ge=1 → should fail
            hero_name="X", hero_class="warrior", monster="Y",
            action="attack", damage_dealt=0, damage_taken=0,
            hero_hp=100, monster_hp=100, result="ongoing",
        )
        print("❌ CombatLogRow accepted battle_id=0 — Field(ge=1) is missing.")
        raise SystemExit(1)
    except Exception:
        pass

    try:
        CombatLogRow(
            battle_id=1, turn=1,
            hero_name="X", hero_class="warrior", monster="Y",
            action="run",  # not in Literal["attack", "potion"]
            damage_dealt=0, damage_taken=0,
            hero_hp=100, monster_hp=100, result="ongoing",
        )
        print('❌ CombatLogRow accepted action="run" — Literal constraint is missing.')
        raise SystemExit(1)
    except Exception:
        pass

    # CsvCombatLogRepository
    with tempfile.TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "combat_log.csv"
        csv_repo = CsvCombatLogRepository(log_path)

        # read_all on missing file → empty list
        try:
            result = csv_repo.read_all()
        except NotImplementedError:
            print("❌ CsvCombatLogRepository.read_all() is not implemented yet.")
            raise SystemExit(1)
        if result != []:
            print(f"❌ read_all() on missing file should return [], got {result}")
            raise SystemExit(1)

        # append
        try:
            csv_repo.append(row)
        except NotImplementedError:
            print("❌ CsvCombatLogRepository.append() is not implemented yet.")
            raise SystemExit(1)

        row2 = CombatLogRow(
            battle_id=1, turn=2,
            hero_name="Ada", hero_class="warrior", monster="Goblin",
            action="attack", damage_dealt=18, damage_taken=0,
            hero_hp=96, monster_hp=0, result="win",
        )
        csv_repo.append(row2)

        rows = csv_repo.read_all()
        if len(rows) != 2:
            print(f"❌ Expected 2 rows after two appends, got {len(rows)}")
            raise SystemExit(1)
        if not isinstance(rows[0], CombatLogRow):
            print(f"❌ read_all() must return list[CombatLogRow], got {type(rows[0])}")
            raise SystemExit(1)
        if rows[0].damage_dealt != 12:
            print(f"❌ First row damage_dealt should be 12, got {rows[0].damage_dealt}")
            raise SystemExit(1)
        if rows[1].result != "win":
            print(f"❌ Second row result should be 'win', got {rows[1].result!r}")
            raise SystemExit(1)

    # InMemoryCombatLogRepository
    mem_repo = InMemoryCombatLogRepository()

    try:
        empty = mem_repo.read_all()
    except NotImplementedError:
        print("❌ InMemoryCombatLogRepository.read_all() is not implemented yet.")
        raise SystemExit(1)
    if empty != []:
        print(f"❌ read_all() before any append should return [], got {empty}")
        raise SystemExit(1)

    try:
        mem_repo.append(row)
    except NotImplementedError:
        print("❌ InMemoryCombatLogRepository.append() is not implemented yet.")
        raise SystemExit(1)

    rows_mem = mem_repo.read_all()
    if len(rows_mem) != 1 or rows_mem[0].hero_name != "Ada":
        print(f"❌ InMemoryCombatLogRepository stored wrong data: {rows_mem}")
        raise SystemExit(1)

    print("✅ Mission 06 complete — CombatLogRepository implementations work correctly.")
    update_progress("06_combat_log_repository")


if __name__ == "__main__":
    main()
